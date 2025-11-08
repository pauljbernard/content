# RAG-Based AI Agent System

## Overview

This system integrates Claude Code with a Retrieval-Augmented Generation (RAG) architecture to provide AI-assisted content generation within the Content Type system. The RAG subsystem retrieves relevant context from content instances and knowledge base files, then provides this context to Claude Code for intelligent content generation.

## Architecture

### Key Components

1. **Context Retrieval Service** (`backend/services/context_retrieval.py`)
   - Retrieves content instances from specified content types
   - Loads markdown files from the knowledge base
   - Assembles context with placeholder resolution
   - Formats context for LLM prompting

2. **Agent Execution Service** (`backend/services/agent_execution.py`)
   - Orchestrates AI-powered content generation
   - Manages agent configurations (built-in defaults + optional custom configs)
   - Constructs prompts with retrieved context
   - Calls Anthropic Claude API
   - Returns generated content for user review

3. **API Endpoints** (`backend/api/v1/content_types.py`)
   - `POST /content-types/instances/{instance_id}/generate-field`
   - `GET /content-types/instances/{instance_id}/available-agents`

4. **Frontend Components**
   - `AgentAssist.jsx` - UI component for AI generation with preview modal
   - `DynamicFormField.jsx` - Integrates AgentAssist into form fields
   - `ContentInstanceEditor.jsx` - Passes instanceId to enable AI assistance

## How It Works

### Content Generation Flow

1. **User Action**: User clicks "Generate with AI" button on a field
2. **Context Retrieval**: Backend retrieves relevant context:
   - Content instances from specified content types
   - Knowledge base markdown files from specified paths
   - User inputs and current instance data
3. **Prompt Assembly**: System builds prompt with:
   - Retrieved context (formatted)
   - Current instance data
   - Field-specific instructions
   - Few-shot examples (optional)
4. **AI Generation**: Calls Anthropic Claude API with assembled prompt
5. **User Review**: Generated content displayed in modal for review
6. **Acceptance**: User accepts or rejects generated content

### Default Configuration

When no agent configuration is specified, the system uses a smart default:

```python
{
    "retrieval_config": {
        "content_types": [],
        "knowledge_base_paths": ["/universal/frameworks/"],
        "filters": {}
    },
    "model_config": {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7,
        "max_tokens": 4096
    }
}
```

The default prompt template:
- Identifies as Claude Code
- Uses retrieved context
- Shows current instance data
- Provides clear task instructions
- Requests appropriate output format

## Enabling AI Assistance for a Field

In the Content Type attribute definition, set:

```json
{
  "name": "learning_objectives",
  "label": "Learning Objectives",
  "type": "json",
  "ai_assist_enabled": true,
  "ai_agents": []  // Optional: For future use with multiple agent types
}
```

**Note**: The `ai_agents` array is reserved for future use when multiple agent types are supported. Currently, all fields use the default Claude Code agent configuration.

## Knowledge Base Integration

The RAG system retrieves context from the hierarchical knowledge base:

### Placeholder Resolution

Knowledge base paths support placeholders that are resolved from instance data:

- `/subjects/{subject}/common/` → `/subjects/mathematics/common/`
- `/districts/{state}/` → `/districts/texas/`

### Example Retrieval Configuration

```json
{
  "retrieval_config": {
    "content_types": [],
    "knowledge_base_paths": [
      "/subjects/{subject}/common/",
      "/districts/{state}/",
      "/universal/frameworks/"
    ],
    "filters": {}
  }
}
```

## Built-In Agent System

The system uses **built-in Claude Code agents** - there are no separate agent configuration content instances to manage.

### How It Works

1. **Fields are marked as AI-assisted**: Set `ai_assist_enabled: true` in the attribute definition
2. **Default agent is used**: Claude Code with smart defaults based on field type and content
3. **Context is retrieved**: RAG system pulls relevant knowledge base files and content instances
4. **Prompt is assembled**: Default prompt template + retrieved context + current instance data
5. **Claude generates content**: Using Anthropic API with the assembled prompt

### Future: Multiple Agent Types

The `ai_agents` array in attribute definitions is reserved for future use:
```json
{
  "ai_agents": ["curriculum-architect", "lesson-planner", "assessment-designer"]
}
```

This would allow users to choose from different built-in agent specializations, each with optimized prompts and behaviors. For now, all fields use the same general-purpose Claude Code agent.

## API Usage

### Generate Field Content

```javascript
// Frontend
const result = await contentTypesAPI.generateField(
  instanceId,
  'learning_objectives',
  agentConfigId  // Optional: null uses default
);

// Returns:
{
  "field_name": "learning_objectives",
  "generated_value": [...],
  "confidence": 0.85,
  "context_metadata": {
    "total_instances": 5,
    "total_knowledge_files": 12
  },
  "model": "claude-3-5-sonnet-20241022",
  "usage": {
    "input_tokens": 2500,
    "output_tokens": 400
  }
}
```

## Security & Permissions

- Requires `ANTHROPIC_API_KEY` environment variable
- Users must have edit permission on the content instance
- Generated content requires user review before acceptance
- Full prompt and context metadata returned for transparency

## Context Metadata

Each generation returns metadata about the context used:

```json
{
  "total_instances": 5,
  "total_knowledge_files": 12,
  "retrieval_config": {...}
}
```

This provides transparency about what knowledge informed the generation.

## Human-in-the-Loop

The system is designed with human oversight:

1. Generated content is **never** automatically saved
2. User reviews content in modal preview
3. User can accept (populate field) or reject (try again)
4. Full prompt shown for debugging and trust

## Performance Considerations

- Knowledge base files are read from disk (cached by OS)
- Content instance queries use database indexes
- Context limited to configurable max files/instances
- Prompt assembly is efficient (string replacement)
- API calls to Anthropic are async

## Future Enhancements

Potential improvements:
- **Auto-suggest mode**: Generate suggestions as user types
- **Auto-populate mode**: Automatically fill dependent fields
- **Confidence-based auto-acceptance**: If confidence > threshold, auto-accept
- **Caching**: Cache retrieved context for similar requests
- **Vector search**: Use embeddings for semantic retrieval
- **Multi-agent workflows**: Chain multiple agents together
- **Feedback loop**: Learn from accepted/rejected generations

## Files Modified

### Backend
- `/backend/services/context_retrieval.py` (NEW)
- `/backend/services/agent_execution.py` (NEW)
- `/backend/api/v1/content_types.py` (MODIFIED - added agent endpoints)
- `/backend/models/content_type.py` (MODIFIED - AttributeDefinition already had ai_assist fields)

### Frontend
- `/frontend/src/components/AgentAssist.jsx` (NEW)
- `/frontend/src/components/DynamicFormField.jsx` (MODIFIED - integrated AgentAssist)
- `/frontend/src/pages/ContentInstanceEditor.jsx` (MODIFIED - passes instanceId)
- `/frontend/src/services/api.js` (MODIFIED - added generateField, getAvailableAgents)

### Documentation
- `/docs/RAG_AGENT_SYSTEM.md` (NEW - this file)

## Key Insights

### Self-Referential Architecture

The system creates a feedback loop:
- **CMS as Knowledge Store**: Content instances and knowledge base provide context
- **CMS as Output Target**: Generated content becomes new content instances
- **Knowledge Reuse**: 85-95% knowledge reuse from hierarchical knowledge base
- **Continuous Improvement**: New content enriches the knowledge base

### Claude Code as Agent

- **Built-in Agent**: Claude Code is the AI agent (not a separate system)
- **Skills & Subagents**: Uses existing Claude Code framework extensions
- **RAG as Context Provider**: RAG system provides relevant context to Claude Code
- **No Separate Agent Definitions**: Agents are part of Claude Code, not content instances

### Design Philosophy

1. **Human Oversight**: AI assists, humans decide
2. **Transparency**: Show what context was used, full prompt available
3. **Flexibility**: Default configurations + optional custom configs
4. **Knowledge Integration**: Leverage hierarchical knowledge base
5. **Extensibility**: Easy to add new agent configurations

---

**Status**: ✅ Complete and ready for testing
**Version**: 1.0.0
**Date**: 2025-11-08
