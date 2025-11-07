"""
User database model and Pydantic schemas.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from database.session import Base


class User(Base):
    """User database model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(
        String, nullable=False, default="teacher"
    )  # author, editor, knowledge_engineer, teacher
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    preferences = Column(Text, nullable=True)  # JSON string

    # Relationships
    agent_jobs = relationship("AgentJob", back_populates="user")


# Pydantic schemas


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: Optional[str] = None
    role: str = "teacher"


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "author@example.com",
                "full_name": "Jane Smith",
                "role": "author",
                "password": "SecureP@ssw0rd",
            }
        }


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "email": "jane.doe@example.com",
            }
        }


class UserInDB(UserBase):
    """User schema with database fields."""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    """Public user schema (no sensitive data)."""

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }


class TokenData(BaseModel):
    """Token payload data."""

    user_id: Optional[int] = None
