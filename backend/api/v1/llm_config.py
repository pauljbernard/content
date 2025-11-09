"""
LLM Configuration API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from database.session import get_db
from models.llm_config import LLMProvider, LLMModel
from models.user import User
from core.security import get_current_user, require_role
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic schemas for request/response
class LLMProviderCreate(BaseModel):
    """Schema for creating LLM provider."""
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    provider_type: str = Field(..., pattern="^(openai|anthropic|local|azure|cohere|huggingface)$")
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    organization_id: Optional[str] = None
    api_version: Optional[str] = None
    supports_chat: bool = True
    supports_embeddings: bool = False
    supports_function_calling: bool = False
    supports_streaming: bool = False
    requests_per_minute: Optional[int] = None
    tokens_per_minute: Optional[int] = None


class LLMProviderUpdate(BaseModel):
    """Schema for updating LLM provider."""
    display_name: Optional[str] = None
    description: Optional[str] = None
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    organization_id: Optional[str] = None
    api_version: Optional[str] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    supports_chat: Optional[bool] = None
    supports_embeddings: Optional[bool] = None
    supports_function_calling: Optional[bool] = None
    supports_streaming: Optional[bool] = None
    requests_per_minute: Optional[int] = None
    tokens_per_minute: Optional[int] = None


class LLMModelCreate(BaseModel):
    """Schema for creating LLM model."""
    provider_id: str
    model_id: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    model_type: str = Field(..., pattern="^(chat|embedding|completion)$")
    context_window: Optional[int] = None
    max_output_tokens: Optional[int] = None
    supports_vision: bool = False
    supports_json_mode: bool = False
    supports_tools: bool = False
    default_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    default_top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    default_max_tokens: Optional[int] = None
    input_cost_per_1m: Optional[float] = None
    output_cost_per_1m: Optional[float] = None
    is_default_for_chat: bool = False
    is_default_for_embeddings: bool = False
    is_default_for_agents: bool = False
    custom_params: Optional[dict] = None


class LLMModelUpdate(BaseModel):
    """Schema for updating LLM model."""
    display_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_default_for_chat: Optional[bool] = None
    is_default_for_embeddings: Optional[bool] = None
    is_default_for_agents: Optional[bool] = None
    default_temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    default_top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    default_max_tokens: Optional[int] = None
    custom_params: Optional[dict] = None


# Provider endpoints
@router.get("/llm-providers")
async def list_providers(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """List all LLM providers."""
    providers = db.query(LLMProvider).order_by(LLMProvider.name).all()
    return [provider.to_dict() for provider in providers]


@router.post("/llm-providers")
async def create_provider(
    provider_data: LLMProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Create a new LLM provider."""
    # Check for duplicate name
    existing = db.query(LLMProvider).filter(LLMProvider.name == provider_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Provider with this name already exists")

    # Create provider
    provider = LLMProvider(
        name=provider_data.name,
        display_name=provider_data.display_name,
        description=provider_data.description,
        provider_type=provider_data.provider_type,
        api_key=provider_data.api_key,
        api_base_url=provider_data.api_base_url,
        organization_id=provider_data.organization_id,
        api_version=provider_data.api_version,
        supports_chat=provider_data.supports_chat,
        supports_embeddings=provider_data.supports_embeddings,
        supports_function_calling=provider_data.supports_function_calling,
        supports_streaming=provider_data.supports_streaming,
        requests_per_minute=provider_data.requests_per_minute,
        tokens_per_minute=provider_data.tokens_per_minute,
        created_by=current_user.id
    )

    db.add(provider)
    db.commit()
    db.refresh(provider)

    logger.info(f"Created LLM provider: {provider.name}")

    return provider.to_dict()


@router.get("/llm-providers/{provider_id}")
async def get_provider(
    provider_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Get LLM provider by ID."""
    provider = db.query(LLMProvider).filter(LLMProvider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider.to_dict()


@router.put("/llm-providers/{provider_id}")
async def update_provider(
    provider_id: str,
    provider_data: LLMProviderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Update LLM provider."""
    provider = db.query(LLMProvider).filter(LLMProvider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # Update fields
    for field, value in provider_data.dict(exclude_unset=True).items():
        setattr(provider, field, value)

    # If setting as default, unset other defaults
    if provider_data.is_default and provider_data.is_default == True:
        db.query(LLMProvider).filter(LLMProvider.id != provider_id).update({LLMProvider.is_default: False})

    provider.updated_at = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(provider)

    logger.info(f"Updated LLM provider: {provider.name}")

    return provider.to_dict()


@router.delete("/llm-providers/{provider_id}")
async def delete_provider(
    provider_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Delete LLM provider."""
    provider = db.query(LLMProvider).filter(LLMProvider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # Check if any models use this provider
    models_count = db.query(LLMModel).filter(LLMModel.provider_id == provider_id).count()
    if models_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete provider with {models_count} associated models. Delete models first."
        )

    db.delete(provider)
    db.commit()

    logger.info(f"Deleted LLM provider: {provider.name}")

    return {"message": "Provider deleted successfully"}


@router.post("/llm-providers/{provider_id}/test")
async def test_provider(
    provider_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Test LLM provider connection."""
    provider = db.query(LLMProvider).filter(LLMProvider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # TODO: Implement actual provider testing
    # For now, just check if API key is set
    if not provider.api_key:
        provider.last_error = "API key not configured"
        provider.last_tested_at = datetime.utcnow().isoformat()
        db.commit()
        raise HTTPException(status_code=400, detail="API key not configured")

    provider.last_tested_at = datetime.utcnow().isoformat()
    provider.last_error = None
    db.commit()

    return {
        "success": True,
        "message": f"Provider {provider.name} configuration is valid",
        "provider_type": provider.provider_type
    }


# Model endpoints
@router.get("/llm-models")
async def list_models(
    provider_id: Optional[str] = None,
    model_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all LLM models, optionally filtered by provider or type."""
    query = db.query(LLMModel)

    if provider_id:
        query = query.filter(LLMModel.provider_id == provider_id)

    if model_type:
        query = query.filter(LLMModel.model_type == model_type)

    models = query.order_by(LLMModel.display_name).all()
    return [model.to_dict() for model in models]


@router.post("/llm-models")
async def create_model(
    model_data: LLMModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Create a new LLM model."""
    # Verify provider exists
    provider = db.query(LLMProvider).filter(LLMProvider.id == model_data.provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # Create model
    model = LLMModel(
        provider_id=model_data.provider_id,
        model_id=model_data.model_id,
        display_name=model_data.display_name,
        description=model_data.description,
        model_type=model_data.model_type,
        context_window=model_data.context_window,
        max_output_tokens=model_data.max_output_tokens,
        supports_vision=model_data.supports_vision,
        supports_json_mode=model_data.supports_json_mode,
        supports_tools=model_data.supports_tools,
        default_temperature=model_data.default_temperature,
        default_top_p=model_data.default_top_p,
        default_max_tokens=model_data.default_max_tokens,
        input_cost_per_1m=model_data.input_cost_per_1m,
        output_cost_per_1m=model_data.output_cost_per_1m,
        is_default_for_chat=model_data.is_default_for_chat,
        is_default_for_embeddings=model_data.is_default_for_embeddings,
        is_default_for_agents=model_data.is_default_for_agents,
        custom_params=model_data.custom_params
    )

    # If setting as default, unset other defaults of same type
    if model_data.is_default_for_chat:
        db.query(LLMModel).filter(LLMModel.model_type == "chat").update({LLMModel.is_default_for_chat: False})

    if model_data.is_default_for_embeddings:
        db.query(LLMModel).filter(LLMModel.model_type == "embedding").update({LLMModel.is_default_for_embeddings: False})

    if model_data.is_default_for_agents:
        db.query(LLMModel).update({LLMModel.is_default_for_agents: False})

    db.add(model)
    db.commit()
    db.refresh(model)

    logger.info(f"Created LLM model: {model.model_id} ({provider.name})")

    return model.to_dict()


@router.get("/llm-models/{model_id}")
async def get_model(
    model_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get LLM model by ID."""
    model = db.query(LLMModel).filter(LLMModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    return model.to_dict()


@router.put("/llm-models/{model_id}")
async def update_model(
    model_id: str,
    model_data: LLMModelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Update LLM model."""
    model = db.query(LLMModel).filter(LLMModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # If setting as default, unset other defaults
    if model_data.is_default_for_chat and model_data.is_default_for_chat == True:
        db.query(LLMModel).filter(LLMModel.id != model_id, LLMModel.model_type == "chat").update({LLMModel.is_default_for_chat: False})

    if model_data.is_default_for_embeddings and model_data.is_default_for_embeddings == True:
        db.query(LLMModel).filter(LLMModel.id != model_id, LLMModel.model_type == "embedding").update({LLMModel.is_default_for_embeddings: False})

    if model_data.is_default_for_agents and model_data.is_default_for_agents == True:
        db.query(LLMModel).filter(LLMModel.id != model_id).update({LLMModel.is_default_for_agents: False})

    # Update fields
    for field, value in model_data.dict(exclude_unset=True).items():
        setattr(model, field, value)

    model.updated_at = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(model)

    logger.info(f"Updated LLM model: {model.model_id}")

    return model.to_dict()


@router.delete("/llm-models/{model_id}")
async def delete_model(
    model_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Delete LLM model."""
    model = db.query(LLMModel).filter(LLMModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    db.delete(model)
    db.commit()

    logger.info(f"Deleted LLM model: {model.model_id}")

    return {"message": "Model deleted successfully"}


# Utility endpoints
@router.get("/llm-defaults")
async def get_defaults(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get default models for each purpose."""
    default_chat = db.query(LLMModel).filter(LLMModel.is_default_for_chat == True).first()
    default_embedding = db.query(LLMModel).filter(LLMModel.is_default_for_embeddings == True).first()
    default_agent = db.query(LLMModel).filter(LLMModel.is_default_for_agents == True).first()

    return {
        "chat": default_chat.to_dict() if default_chat else None,
        "embeddings": default_embedding.to_dict() if default_embedding else None,
        "agents": default_agent.to_dict() if default_agent else None,
    }
