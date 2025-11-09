"""
Secrets Management API - Secure storage for API keys and sensitive configuration.

This is a specialized wrapper around the content type system that adds encryption
for the Secret content type.
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database.session import get_db
from core.security import get_current_active_user, get_current_superuser
from models.user import User
from models.content_type import ContentTypeModel, ContentInstanceModel
from utils.validation import (
    validate_instance_data,
    encrypt_password_secret_fields,
    mask_password_secret_fields
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/secrets", tags=["secrets"])


# Pydantic schemas
class SecretCreate(BaseModel):
    """Schema for creating a secret."""
    secret_name: str = Field(..., description="Service/category name (e.g., 'CASE API')")
    api_key: str = Field(..., description="API key or username")
    secret_value: str = Field(..., description="Secret value or password")
    description: Optional[str] = Field(None, description="What this secret is used for")
    category: Optional[str] = Field(None, description="Category (API_KEY, DATABASE, INTEGRATION, CREDENTIALS, OTHER)")
    environment: Optional[str] = Field(None, description="Environment (PRODUCTION, STAGING, DEVELOPMENT, TEST)")
    is_active: bool = Field(True, description="Whether secret is active")


class SecretUpdate(BaseModel):
    """Schema for updating a secret."""
    secret_name: Optional[str] = None
    api_key: Optional[str] = None
    secret_value: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    environment: Optional[str] = None
    is_active: Optional[bool] = None


class SecretResponse(BaseModel):
    """Schema for secret response (values masked)."""
    id: str
    secret_name: str
    api_key_masked: str
    secret_value_masked: str
    description: Optional[str]
    category: Optional[str]
    environment: Optional[str]
    is_active: bool
    created_by: int
    created_at: str
    updated_at: str


def get_secret_content_type(db: Session) -> ContentTypeModel:
    """Get the Secret content type."""
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == "Secret"
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Secret content type not found. Run init_secret_content_type.py"
        )

    return content_type


@router.get("/", response_model=List[SecretResponse])
async def list_secrets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_superuser),  # Only admins can view secrets
    db: Session = Depends(get_db),
):
    """
    List all secrets (values masked).

    Requires superuser access.
    """
    content_type = get_secret_content_type(db)

    instances = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type.id
    ).offset(skip).limit(limit).all()

    results = []
    for instance in instances:
        # Mask password_secret fields
        masked_data = mask_password_secret_fields(content_type.attributes, instance.data)

        results.append(SecretResponse(
            id=instance.id,
            secret_name=masked_data.get("secret_name", ""),
            api_key_masked=masked_data.get("api_key", "***"),
            secret_value_masked=masked_data.get("secret_value", "***"),
            description=masked_data.get("description"),
            category=masked_data.get("category"),
            environment=masked_data.get("environment"),
            is_active=masked_data.get("is_active", True),
            created_by=instance.created_by,
            created_at=instance.created_at.isoformat(),
            updated_at=instance.updated_at.isoformat() if instance.updated_at else instance.created_at.isoformat()
        ))

    return results


@router.post("/", response_model=SecretResponse, status_code=status.HTTP_201_CREATED)
async def create_secret(
    secret: SecretCreate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Create a new secret.

    The secret value will be encrypted before storing in the database.
    Requires superuser access.
    """
    content_type = get_secret_content_type(db)

    # Check if secret with this (secret_name, api_key) combination already exists
    existing = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type.id
    ).all()

    from utils.validation import decrypt_password_secret_fields

    for inst in existing:
        # Decrypt to compare api_key (since it's encrypted)
        decrypted = decrypt_password_secret_fields(content_type.attributes, inst.data)
        if (decrypted.get("secret_name") == secret.secret_name and
            decrypted.get("api_key") == secret.api_key):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Secret with name '{secret.secret_name}' and API key already exists"
            )

    # Prepare instance data
    instance_data = {
        "secret_name": secret.secret_name,
        "api_key": secret.api_key,
        "secret_value": secret.secret_value,
        "description": secret.description,
        "category": secret.category,
        "environment": secret.environment,
        "is_active": secret.is_active
    }

    # Validate
    errors = validate_instance_data(content_type.attributes, instance_data)
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )

    # Encrypt password_secret fields
    encrypted_data = encrypt_password_secret_fields(content_type.attributes, instance_data)

    # Create instance
    instance = ContentInstanceModel(
        content_type_id=content_type.id,
        data=encrypted_data,
        status="published",  # Secrets are always published
        created_by=current_user.id
    )

    db.add(instance)
    db.commit()
    db.refresh(instance)

    # Return masked response
    masked_data = mask_password_secret_fields(content_type.attributes, instance.data)

    return SecretResponse(
        id=instance.id,
        secret_name=masked_data.get("secret_name", ""),
        api_key_masked=masked_data.get("api_key", "***"),
        secret_value_masked=masked_data.get("secret_value", "***"),
        description=masked_data.get("description"),
        category=masked_data.get("category"),
        environment=masked_data.get("environment"),
        is_active=masked_data.get("is_active", True),
        created_by=instance.created_by,
        created_at=instance.created_at.isoformat(),
        updated_at=instance.updated_at.isoformat() if instance.updated_at else instance.created_at.isoformat()
    )


@router.put("/{secret_id}", response_model=SecretResponse)
async def update_secret(
    secret_id: str,
    secret: SecretUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Update a secret.

    If value is provided, it will be encrypted before storing.
    Requires superuser access.
    """
    content_type = get_secret_content_type(db)

    instance = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.id == secret_id,
        ContentInstanceModel.content_type_id == content_type.id
    ).first()

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secret not found"
        )

    # Update data
    update_data = secret.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            instance.data[key] = value

    # Encrypt password_secret fields
    instance.data = encrypt_password_secret_fields(content_type.attributes, instance.data)

    instance.updated_by = current_user.id
    db.commit()
    db.refresh(instance)

    # Return masked response
    masked_data = mask_password_secret_fields(content_type.attributes, instance.data)

    return SecretResponse(
        id=instance.id,
        secret_name=masked_data.get("secret_name", ""),
        api_key_masked=masked_data.get("api_key", "***"),
        secret_value_masked=masked_data.get("secret_value", "***"),
        description=masked_data.get("description"),
        category=masked_data.get("category"),
        environment=masked_data.get("environment"),
        is_active=masked_data.get("is_active", True),
        created_by=instance.created_by,
        created_at=instance.created_at.isoformat(),
        updated_at=instance.updated_at.isoformat() if instance.updated_at else instance.created_at.isoformat()
    )


@router.delete("/{secret_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_secret(
    secret_id: str,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Delete a secret.

    Requires superuser access.
    """
    content_type = get_secret_content_type(db)

    instance = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.id == secret_id,
        ContentInstanceModel.content_type_id == content_type.id
    ).first()

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secret not found"
        )

    db.delete(instance)
    db.commit()

    return None


@router.get("/{secret_id}/value")
async def get_secret_value(
    secret_id: str,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Get the decrypted secret values.

    This endpoint returns the actual API key and secret value for use by the system.
    Requires superuser access.

    Returns:
        {"api_key": "decrypted-api-key", "secret_value": "decrypted-secret-value"}
    """
    from utils.validation import decrypt_password_secret_fields

    content_type = get_secret_content_type(db)

    instance = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.id == secret_id,
        ContentInstanceModel.content_type_id == content_type.id
    ).first()

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secret not found"
        )

    # Decrypt password_secret fields
    decrypted_data = decrypt_password_secret_fields(content_type.attributes, instance.data)

    return {
        "secret_name": decrypted_data.get("secret_name", ""),
        "api_key": decrypted_data.get("api_key", ""),
        "secret_value": decrypted_data.get("secret_value", "")
    }


@router.get("/by-name/{secret_name}")
async def get_secrets_by_name(
    secret_name: str,
    api_key: Optional[str] = Query(None, description="Optional API key to filter by"),
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Get secrets by name, optionally filtered by API key.

    Since multiple secrets can have the same secret_name (e.g., different environments),
    this returns all matching secrets or a specific one if api_key is provided.

    Requires superuser access.

    Returns:
        List of decrypted secrets or single secret if api_key specified
    """
    from utils.validation import decrypt_password_secret_fields

    content_type = get_secret_content_type(db)

    instances = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type.id
    ).all()

    matches = []
    for instance in instances:
        if instance.data.get("secret_name") == secret_name:
            # Decrypt password_secret fields
            decrypted_data = decrypt_password_secret_fields(content_type.attributes, instance.data)

            # If api_key filter specified, check if it matches
            if api_key and decrypted_data.get("api_key") != api_key:
                continue

            matches.append({
                "id": instance.id,
                "secret_name": decrypted_data.get("secret_name", ""),
                "api_key": decrypted_data.get("api_key", ""),
                "secret_value": decrypted_data.get("secret_value", ""),
                "description": decrypted_data.get("description"),
                "category": decrypted_data.get("category"),
                "environment": decrypted_data.get("environment"),
                "is_active": decrypted_data.get("is_active", True)
            })

    if not matches:
        detail = f"Secret '{secret_name}'" + (f" with API key '{api_key}'" if api_key else "") + " not found"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

    # If api_key was specified, return single result
    if api_key:
        return matches[0]

    # Otherwise return all matches
    return matches
