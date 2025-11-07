"""
Content models for lessons, assessments, and activities.
"""
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
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from enum import Enum
from database.session import Base


class ContentType(str, Enum):
    """Content type enumeration."""

    LESSON = "lesson"
    ASSESSMENT = "assessment"
    ACTIVITY = "activity"
    GUIDE = "guide"
    FRAMEWORK = "framework"


class ContentStatus(str, Enum):
    """Content status enumeration."""

    DRAFT = "draft"
    IN_REVIEW = "in_review"
    NEEDS_REVISION = "needs_revision"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Content(Base):
    """Content database model."""

    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT)

    # Curriculum information
    subject = Column(String, nullable=False)
    grade_level = Column(String)  # Can be range like "9-12"
    state = Column(String, nullable=True)  # None for national content
    curriculum_id = Column(String, nullable=True)  # Reference to config ID

    # Content metadata
    standards_aligned = Column(Text)  # JSON array of standard IDs
    knowledge_files_used = Column(Text)  # JSON array of file paths
    learning_objectives = Column(Text)  # JSON array
    duration_minutes = Column(Integer, nullable=True)

    # File information
    file_path = Column(String, nullable=True)  # Path to markdown/content file
    file_content = Column(Text, nullable=True)  # Actual content

    # Authoring
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)

    # Relationships
    author = relationship("User", foreign_keys=[author_id])
    reviews = relationship("ContentReview", back_populates="content")


class ContentReview(Base):
    """Content review database model."""

    __tablename__ = "content_reviews"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Review details
    status = Column(String, nullable=False)  # approved, needs_revision, rejected
    comments = Column(Text)
    checklist_results = Column(Text)  # JSON object of checklist items
    rating = Column(Integer, nullable=True)  # 1-5 stars

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content = relationship("Content", back_populates="reviews")
    reviewer = relationship("User")


# Pydantic schemas


class ContentBase(BaseModel):
    """Base content schema."""

    title: str
    content_type: ContentType
    subject: str
    grade_level: Optional[str] = None
    state: Optional[str] = None
    curriculum_id: Optional[str] = None


class ContentCreate(ContentBase):
    """Schema for creating content."""

    file_content: Optional[str] = None
    standards_aligned: Optional[List[str]] = []
    learning_objectives: Optional[List[str]] = []
    duration_minutes: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Introduction to Fractions",
                "content_type": "lesson",
                "subject": "mathematics",
                "grade_level": "5",
                "state": "texas",
                "curriculum_id": "hmh-math-tx",
                "file_content": "# Introduction to Fractions\n\n## Learning Objectives\n- Understand fractions as parts of a whole\n- Compare and order fractions\n\n## Lesson Content\n...",
                "standards_aligned": ["TEKS.5.3A", "TEKS.5.3B"],
                "learning_objectives": [
                    "Students will identify fractions as parts of a whole",
                    "Students will compare fractions with like denominators"
                ],
                "duration_minutes": 60
            }
        }


class ContentUpdate(BaseModel):
    """Schema for updating content."""

    title: Optional[str] = None
    file_content: Optional[str] = None
    standards_aligned: Optional[List[str]] = None
    learning_objectives: Optional[List[str]] = None
    duration_minutes: Optional[int] = None
    status: Optional[ContentStatus] = None


class ContentInDB(ContentBase):
    """Content schema with database fields."""

    id: int
    status: ContentStatus
    file_path: Optional[str]
    file_content: Optional[str]
    standards_aligned: Optional[List[str]] = []
    knowledge_files_used: Optional[List[str]] = []
    learning_objectives: Optional[List[str]] = []
    duration_minutes: Optional[int]
    author_id: int
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime]
    approved_at: Optional[datetime]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class ContentPublic(ContentBase):
    """Public content schema."""

    id: int
    status: ContentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentReviewCreate(BaseModel):
    """Schema for creating a content review."""

    content_id: int
    status: str = Field(..., regex="^(approved|needs_revision|rejected)$")
    comments: Optional[str] = None
    checklist_results: Optional[Dict[str, Any]] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

    class Config:
        json_schema_extra = {
            "example": {
                "content_id": 42,
                "status": "approved",
                "comments": "Excellent lesson with clear objectives and engaging activities. Standards alignment is accurate.",
                "rating": 5,
                "checklist_results": {
                    "standards_aligned": True,
                    "objectives_clear": True,
                    "accessibility_compliant": True,
                    "culturally_responsive": True
                }
            }
        }


class ContentReviewInDB(BaseModel):
    """Content review schema with database fields."""

    id: int
    content_id: int
    reviewer_id: int
    status: str
    comments: Optional[str]
    checklist_results: Optional[Dict[str, Any]]
    rating: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
