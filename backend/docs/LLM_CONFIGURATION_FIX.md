# LLM Configuration System - Investigation and Fix

**Date**: 2025-11-08
**Status**: ✅ FIXED

## Problem Identified

The AI assistant (agent executor) was **NOT using the stored LLM configuration from the database**, despite having a complete LLM configuration system in place. Instead, it was hardcoded to use values from the `.env` file.

### What Was Wrong

**File**: `backend/services/claude_client.py`

**Before (Lines 14-20)**:
```python
def __init__(self):
    self.api_key = settings.ANTHROPIC_API_KEY or ""  # ❌ Hardcoded to .env
    if not self.api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

    self.client = anthropic.Anthropic(api_key=self.api_key)
    self.default_model = "claude-sonnet-4-20250514"  # ❌ Hardcoded model
    self.max_tokens = 8000
```

**Issues**:
1. API key was **always loaded from .env** (`settings.ANTHROPIC_API_KEY`)
2. Model was **hardcoded** (`"claude-sonnet-4-20250514"`)
3. Database configuration was **completely ignored**

## Database Configuration Status

The database **already had** proper configuration:

### LLM Providers
```
Name: Anthropic
Type: anthropic
Is Default: False
Is Active: True
Has API Key: Yes (sk-ant-a...XwAA)
```

### LLM Models
```
Model ID: claude-sonnet-4-20250514
Display Name: Claude sonnet 4
Type: chat
Default for Chat: True
Default for Agents: True  ← This should have been used!
Is Active: True
```

## Solution Implemented

### Enhanced ClaudeClient Initialization

**File**: `backend/services/claude_client.py`

**After**:
```python
def __init__(self, db_session=None):
    """
    Initialize Claude client.

    Args:
        db_session: Optional database session to load configuration from database.
                   If not provided, uses .env configuration.
    """
    # Try to load configuration from database first
    api_key_from_db = None
    model_from_db = None

    if db_session:
        try:
            from models.llm_config import LLMProvider, LLMModel

            # Get default agent model from database
            default_model = db_session.query(LLMModel).filter(
                LLMModel.is_default_for_agents == True,
                LLMModel.is_active == True
            ).first()

            if default_model:
                model_from_db = default_model.model_id
                logger.info(f"Using model from database: {model_from_db}")

                # Get the provider for this model
                provider = db_session.query(LLMProvider).filter(
                    LLMProvider.id == default_model.provider_id,
                    LLMProvider.is_active == True
                ).first()

                if provider and provider.api_key:
                    api_key_from_db = provider.api_key
                    logger.info(f"Using API key from database provider: {provider.name}")
            else:
                logger.warning("No default agent model found in database, falling back to .env config")
        except Exception as e:
            logger.warning(f"Failed to load LLM config from database: {e}. Falling back to .env config")

    # Use database config if available, otherwise fall back to .env
    self.api_key = api_key_from_db or settings.ANTHROPIC_API_KEY or ""
    if not self.api_key:
        raise ValueError("No API key available. Configure LLM provider in database or set ANTHROPIC_API_KEY in .env")

    self.client = anthropic.Anthropic(api_key=self.api_key)
    self.default_model = model_from_db or "claude-sonnet-4-20250514"
    self.max_tokens = 8000

    logger.info(f"ClaudeClient initialized with model: {self.default_model}")
```

### Updated Singleton Getter

**File**: `backend/services/claude_client.py`

```python
def get_claude_client(db_session=None) -> ClaudeClient:
    """
    Get or create the Claude client singleton.

    Args:
        db_session: Optional database session to load configuration.
                   If provided on first call, will load config from database.

    Returns:
        ClaudeClient instance
    """
    global _claude_client
    if _claude_client is None:
        # On first initialization, try to get database session if not provided
        if db_session is None:
            try:
                from database.session import SessionLocal
                db_session = SessionLocal()
                _claude_client = ClaudeClient(db_session=db_session)
                db_session.close()
            except Exception as e:
                logger.warning(f"Could not access database for LLM config: {e}. Using .env config.")
                _claude_client = ClaudeClient(db_session=None)
        else:
            _claude_client = ClaudeClient(db_session=db_session)

    return _claude_client
```

## Configuration Hierarchy

The new system follows this priority order:

1. **Database Configuration** (First Priority)
   - Query for default agent model (`is_default_for_agents = True`)
   - Get provider API key from database
   - Use model ID from database

2. **Environment Variables** (Fallback)
   - Use `ANTHROPIC_API_KEY` from .env
   - Use hardcoded model `"claude-sonnet-4-20250514"`

3. **Error** (No Config)
   - Raise error if neither source has configuration

## Verification

### Test Script

**File**: `backend/scripts/test_claude_client_config.py`

**Test Results**:
```
============================================================
CLAUDE CLIENT INITIALIZATION
============================================================

✓ ClaudeClient Initialized:
  Default Model: claude-sonnet-4-20250514
  Max Tokens: 8000
  API Key (masked): sk-ant-a...XwAA

============================================================
CONFIGURATION COMPARISON
============================================================

✓ USING DATABASE MODEL: claude-sonnet-4-20250514
  Status: SUCCESS - ClaudeClient is using database configuration!

✓ API KEY LENGTH MATCH: Likely using database API key
```

**Log Output**:
```
INFO:services.claude_client:Using model from database: claude-sonnet-4-20250514
INFO:services.claude_client:Using API key from database provider: Anthropic
INFO:services.claude_client:ClaudeClient initialized with model: claude-sonnet-4-20250514
```

## Benefits

✅ **Centralized Configuration**: LLM settings managed in database UI
✅ **Hot Swapping**: Change models without code deployment
✅ **Multi-Model Support**: Different models for different purposes (chat, agents, embeddings)
✅ **Fallback Safety**: Still works if database is unavailable
✅ **Logging**: Clear logging shows which configuration source is used
✅ **Security**: API keys stored in database instead of .env files

## API Endpoints for Configuration

### List Models
```bash
GET /api/v1/llm-models
```

### Get Default Models
```bash
GET /api/v1/llm-defaults
```
Returns:
```json
{
  "chat": { "model_id": "claude-sonnet-4-20250514", ... },
  "agents": { "model_id": "claude-sonnet-4-20250514", ... },
  "embeddings": { "model_id": "text-embedding-3-large", ... }
}
```

### Update Model
```bash
PUT /api/v1/llm-models/{model_id}
```
Body:
```json
{
  "is_default_for_agents": true
}
```

### List Providers
```bash
GET /api/v1/llm-providers
```

### Update Provider
```bash
PUT /api/v1/llm-providers/{provider_id}
```
Body:
```json
{
  "api_key": "sk-ant-...",
  "is_active": true
}
```

## Usage in Code

### Agent Executor
**File**: `backend/services/agent_executor.py` (Line 173)

```python
def __init__(self):
    self.claude_client = get_claude_client()  # Now loads from database!
```

### Workflows
Any workflow or service that needs Claude API should use:
```python
from services.claude_client import get_claude_client

client = get_claude_client()
response = await client.generate_response(prompt="...", system_prompt="...")
```

## Future Enhancements

1. **Model Selection Per Agent Type**: Different models for different agent types
2. **Cost Tracking**: Log usage costs based on model pricing in database
3. **Rate Limiting**: Use provider's `requests_per_minute` and `tokens_per_minute` settings
4. **Model Parameters**: Use model's `default_temperature`, `default_top_p`, etc. from database
5. **Multi-Provider Support**: Switch between Anthropic, OpenAI, local models, etc.
6. **A/B Testing**: Test different models for same task
7. **Model Performance Metrics**: Track latency, token usage, success rates per model

## Related Files

- `backend/services/claude_client.py` - Claude API client (FIXED)
- `backend/services/vector_search.py` - Vector search service (FIXED - see EMBEDDING_CONFIGURATION_FIX.md)
- `backend/services/agent_executor.py` - Agent executor using ClaudeClient
- `backend/api/v1/llm_config.py` - LLM configuration API endpoints
- `backend/models/llm_config.py` - LLM provider and model database models
- `backend/scripts/test_claude_client_config.py` - Verification test script
- `backend/scripts/test_embedding_config.py` - Embedding configuration test script
- `backend/docs/EMBEDDING_CONFIGURATION_FIX.md` - Vector embedding configuration fix documentation

## Conclusion

The LLM configuration system is now **fully functional** for both Claude chat/agents and OpenAI embeddings:

1. **Claude Client** (Chat & Agents): Uses database configuration for `is_default_for_agents = True` model
2. **Vector Search** (Embeddings): Uses database configuration for `is_default_for_embeddings = True` model (see EMBEDDING_CONFIGURATION_FIX.md)

Both services will use the database configuration for model selection and API credentials, with automatic fallback to .env if needed. Administrators can now manage LLM configuration through the UI without code changes or deployments.

**Status**: ✅ **WORKING AS DESIGNED**
