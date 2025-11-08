"""
Content type system models - flexible schema-less CMS.

This module provides a Contentful/Strapi-like content modeling system where:
1. Users can define custom content types with attributes
2. Content instances are created based on these content types
3. All attribute data is stored in JSON for maximum flexibility
"""
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, Field, field_validator
from database.session import Base


class ContentTypeModel(Base):
    """
    Content type definition model.

    Defines the schema for a type of content (e.g., "Lesson Plan", "Assessment", "Activity").
    Each content type has a collection of attributes that define what fields instances will have.
    """
    __tablename__ = "content_types"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    icon = Column(String(50))  # Icon name from heroicons

    # Whether this is a system-defined type (can't be deleted/modified)
    is_system = Column(Boolean, default=False)

    # Attribute definitions stored as JSON
    # Structure: [{"name": "title", "label": "Title", "type": "text", "required": true, "config": {...}}, ...]
    attributes = Column(JSON, nullable=False)

    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    instances = relationship("ContentInstanceModel", back_populates="content_type", cascade="all, delete-orphan")


class ContentInstanceModel(Base):
    """
    Content instance model.

    An instance of a content type with actual data values.
    All attribute values are stored in the 'data' JSONB field.
    """
    __tablename__ = "content_instances"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content_type_id = Column(String(36), ForeignKey("content_types.id", ondelete="RESTRICT"), nullable=False, index=True)

    # All attribute values stored as JSON
    # Structure: {"title": "My Lesson", "grade_levels": ["3", "4"], "duration": 45, ...}
    data = Column(JSON, nullable=False)

    # Workflow status
    status = Column(String(50), default="draft", index=True)

    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)

    # Relationships
    content_type = relationship("ContentTypeModel", back_populates="instances")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    relationships_source = relationship(
        "ContentRelationshipModel",
        foreign_keys="ContentRelationshipModel.source_instance_id",
        back_populates="source_instance",
        cascade="all, delete-orphan"
    )
    relationships_target = relationship(
        "ContentRelationshipModel",
        foreign_keys="ContentRelationshipModel.target_instance_id",
        back_populates="target_instance"
    )


class ContentRelationshipModel(Base):
    """
    Content relationship model.

    Tracks relationships between content instances for reference fields.
    E.g., a Lesson referencing Standards, or a Unit referencing Lessons.
    """
    __tablename__ = "content_relationships"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_instance_id = Column(String(36), ForeignKey("content_instances.id", ondelete="CASCADE"), nullable=False, index=True)
    source_attribute = Column(String(100), nullable=False)  # Which attribute holds the reference
    target_instance_id = Column(String(36), ForeignKey("content_instances.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    source_instance = relationship(
        "ContentInstanceModel",
        foreign_keys=[source_instance_id],
        back_populates="relationships_source"
    )
    target_instance = relationship(
        "ContentInstanceModel",
        foreign_keys=[target_instance_id],
        back_populates="relationships_target"
    )


# Pydantic schemas

class AttributeDefinition(BaseModel):
    """Schema for an attribute definition in a content type."""
    name: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$", description="Attribute name (snake_case)")
    label: str = Field(..., description="Human-readable label")
    type: str = Field(..., description="Attribute type (text, number, boolean, date, choice, reference, media, json, etc.)")
    required: bool = Field(default=False, description="Whether this attribute is required")
    config: Dict[str, Any] = Field(default_factory=dict, description="Type-specific configuration")
    help_text: Optional[str] = Field(None, description="Help text shown to users")
    default_value: Optional[Any] = Field(None, description="Default value for this attribute")
    order_index: Optional[int] = Field(None, description="Display order in forms")

    # AI Assist configuration
    ai_assist_enabled: bool = Field(default=False, description="Whether AI assistance is available for this field")
    ai_agents: List[str] = Field(default_factory=list, description="List of agent IDs that can assist with this field")
    ai_output_schema: Optional[str] = Field(None, description="JSON schema/sample for AI to produce structured output (for JSON fields)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "title",
                "label": "Lesson Title",
                "type": "text",
                "required": True,
                "config": {"maxLength": 200},
                "help_text": "A concise, descriptive title for the lesson",
                "default_value": None,
                "order_index": 0,
                "ai_assist_enabled": False,
                "ai_agents": [],
                "ai_output_schema": None
            }
        }


class ContentTypeCreate(BaseModel):
    """Schema for creating a content type."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    attributes: List[AttributeDefinition] = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Lesson Plan",
                "description": "A structured lesson plan for K-12 education",
                "icon": "BookOpenIcon",
                "attributes": [
                    {
                        "name": "title",
                        "label": "Lesson Title",
                        "type": "text",
                        "required": True,
                        "config": {"maxLength": 200}
                    },
                    {
                        "name": "grade_levels",
                        "label": "Grade Levels",
                        "type": "choice",
                        "required": True,
                        "config": {
                            "multiple": True,
                            "choices": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
                        }
                    },
                    {
                        "name": "duration",
                        "label": "Duration (minutes)",
                        "type": "number",
                        "required": True,
                        "config": {"min": 1, "max": 180}
                    }
                ]
            }
        }


class ContentTypeUpdate(BaseModel):
    """Schema for updating a content type."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    attributes: Optional[List[AttributeDefinition]] = None


class ContentTypeInDB(BaseModel):
    """Content type schema with database fields."""
    id: str
    name: str
    description: Optional[str]
    icon: Optional[str]
    is_system: bool
    attributes: List[AttributeDefinition]
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    instance_count: Optional[int] = 0  # Computed field

    class Config:
        from_attributes = True


class ContentInstanceCreate(BaseModel):
    """Schema for creating a content instance."""
    data: Dict[str, Any] = Field(..., description="Attribute values matching the content type schema")
    status: Optional[str] = Field("draft", pattern=r"^(draft|in_review|published|archived)$")

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "title": "Introduction to Fractions",
                    "grade_levels": ["3", "4"],
                    "duration": 45,
                    "learning_objectives": "Students will understand the concept of fractions as parts of a whole..."
                },
                "status": "draft"
            }
        }


class ContentInstanceUpdate(BaseModel):
    """Schema for updating a content instance."""
    data: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, pattern=r"^(draft|in_review|published|archived)$")


class ContentInstanceInDB(BaseModel):
    """Content instance schema with database fields."""
    id: str
    content_type_id: str
    data: Dict[str, Any]
    status: str
    created_by: int
    updated_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class ContentInstanceWithType(ContentInstanceInDB):
    """Content instance with its content type definition."""
    content_type: ContentTypeInDB

    class Config:
        from_attributes = True


class ContentRelationshipCreate(BaseModel):
    """Schema for creating a content relationship."""
    source_instance_id: str
    source_attribute: str
    target_instance_id: str


class ContentRelationshipInDB(BaseModel):
    """Content relationship schema with database fields."""
    id: str
    source_instance_id: str
    source_attribute: str
    target_instance_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ContentStatsResponse(BaseModel):
    """Statistics about content types and instances."""
    total_content_types: int
    total_instances: int
    instances_by_status: Dict[str, int]
    instances_by_type: List[Dict[str, Any]]
