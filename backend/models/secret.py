"""
Secret management models for storing API keys and sensitive configuration.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from database.session import Base


class Secret(Base):
    """Secret storage for API keys and sensitive configuration."""

    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    encrypted_value = Column(Text, nullable=False)  # Encrypted secret value

    # Multi-tenant support
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])


# Pydantic Schemas
class SecretCreate(BaseModel):
    """Schema for creating a secret."""

    name: str = Field(..., min_length=1, max_length=255, description="Secret name (e.g., 'CASE_API_KEY')")
    description: Optional[str] = Field(None, description="Description of what this secret is for")
    value: str = Field(..., min_length=1, description="Secret value (will be encrypted)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "CASE_API_KEY",
                "description": "API key for Georgia CASE standards access",
                "value": "sk-1234567890abcdef"
            }
        }


class SecretUpdate(BaseModel):
    """Schema for updating a secret."""

    description: Optional[str] = None
    value: Optional[str] = Field(None, min_length=1, description="New secret value (will be encrypted)")
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Updated API key for CASE standards",
                "value": "sk-newkey1234567890",
                "is_active": True
            }
        }


class SecretInDB(BaseModel):
    """Schema for secret from database (value masked)."""

    id: int
    name: str
    description: Optional[str]
    value_masked: str  # Masked value like "sk-12...ef"
    created_by: int
    is_active: bool
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class SecretPublic(BaseModel):
    """Public secret schema (value completely hidden)."""

    id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]

    class Config:
        from_attributes = True


class SecretWithValue(BaseModel):
    """Secret schema with decrypted value (only for internal use)."""

    id: int
    name: str
    value: str  # Decrypted value
    description: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
