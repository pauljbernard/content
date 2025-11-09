"""
LLM Configuration models for managing AI providers and API keys.
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, JSON
from sqlalchemy.ext.mutable import MutableDict
from database.session import Base
from datetime import datetime
import uuid


class LLMProvider(Base):
    """LLM Provider configuration (OpenAI, Anthropic, etc.)"""
    __tablename__ = "llm_providers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)  # "OpenAI", "Anthropic", etc.
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    provider_type = Column(String(50), nullable=False)  # "openai", "anthropic", "local", "azure"

    # API Configuration
    api_key = Column(Text, nullable=True)  # Encrypted in production
    api_base_url = Column(String(500), nullable=True)  # For custom endpoints/proxies
    organization_id = Column(String(255), nullable=True)  # For OpenAI orgs
    api_version = Column(String(50), nullable=True)  # For Azure OpenAI

    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)  # Default provider for embeddings/chat
    last_tested_at = Column(String, nullable=True)
    last_error = Column(Text, nullable=True)

    # Capabilities
    supports_chat = Column(Boolean, default=True)
    supports_embeddings = Column(Boolean, default=False)
    supports_function_calling = Column(Boolean, default=False)
    supports_streaming = Column(Boolean, default=False)

    # Rate Limiting
    requests_per_minute = Column(Integer, nullable=True)
    tokens_per_minute = Column(Integer, nullable=True)

    # Metadata
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    created_by = Column(String, nullable=True)

    def to_dict(self):
        """Convert to dictionary (masks API key)."""
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "provider_type": self.provider_type,
            "api_key_configured": bool(self.api_key),
            "api_key_masked": f"{self.api_key[:8]}...{self.api_key[-4:]}" if self.api_key and len(self.api_key) > 12 else None,
            "api_base_url": self.api_base_url,
            "organization_id": self.organization_id,
            "api_version": self.api_version,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "last_tested_at": self.last_tested_at,
            "last_error": self.last_error,
            "supports_chat": self.supports_chat,
            "supports_embeddings": self.supports_embeddings,
            "supports_function_calling": self.supports_function_calling,
            "supports_streaming": self.supports_streaming,
            "requests_per_minute": self.requests_per_minute,
            "tokens_per_minute": self.tokens_per_minute,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class LLMModel(Base):
    """LLM Model configuration (gpt-4, claude-3-opus, etc.)"""
    __tablename__ = "llm_models"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String, nullable=False)  # Foreign key to LLMProvider

    # Model Details
    model_id = Column(String(100), nullable=False)  # "gpt-4-turbo-preview", "claude-3-opus-20240229"
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    model_type = Column(String(50), nullable=False)  # "chat", "embedding", "completion"

    # Capabilities
    context_window = Column(Integer, nullable=True)  # Max tokens (e.g., 128000)
    max_output_tokens = Column(Integer, nullable=True)  # Max response tokens
    supports_vision = Column(Boolean, default=False)
    supports_json_mode = Column(Boolean, default=False)
    supports_tools = Column(Boolean, default=False)

    # Default Parameters
    default_temperature = Column(Float, default=0.7)
    default_top_p = Column(Float, default=1.0)
    default_max_tokens = Column(Integer, nullable=True)

    # Pricing (per 1M tokens)
    input_cost_per_1m = Column(Float, nullable=True)  # USD
    output_cost_per_1m = Column(Float, nullable=True)  # USD

    # Usage Preferences
    is_active = Column(Boolean, default=True)
    is_default_for_chat = Column(Boolean, default=False)
    is_default_for_embeddings = Column(Boolean, default=False)
    is_default_for_agents = Column(Boolean, default=False)

    # Custom Settings (JSON)
    custom_params = Column(MutableDict.as_mutable(JSON), nullable=True)  # Additional provider-specific params

    # Metadata
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "model_id": self.model_id,
            "display_name": self.display_name,
            "description": self.description,
            "model_type": self.model_type,
            "context_window": self.context_window,
            "max_output_tokens": self.max_output_tokens,
            "supports_vision": self.supports_vision,
            "supports_json_mode": self.supports_json_mode,
            "supports_tools": self.supports_tools,
            "default_temperature": self.default_temperature,
            "default_top_p": self.default_top_p,
            "default_max_tokens": self.default_max_tokens,
            "input_cost_per_1m": self.input_cost_per_1m,
            "output_cost_per_1m": self.output_cost_per_1m,
            "is_active": self.is_active,
            "is_default_for_chat": self.is_default_for_chat,
            "is_default_for_embeddings": self.is_default_for_embeddings,
            "is_default_for_agents": self.is_default_for_agents,
            "custom_params": self.custom_params,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
