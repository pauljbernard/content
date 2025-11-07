"""
Agent job models for Professor Framework integration.
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum as PyEnum
from database.session import Base


# Enums
class AgentType(str, PyEnum):
    """Available Professor Framework agents (22 total)."""

    # Curriculum Design
    CURRICULUM_ARCHITECT = "curriculum-architect"
    INSTRUCTIONAL_DESIGNER = "instructional-designer"

    # Content Creation
    CONTENT_DEVELOPER = "content-developer"
    ASSESSMENT_DESIGNER = "assessment-designer"
    ADAPTIVE_LEARNING = "adaptive-learning"
    PLATFORM_TRAINING = "platform-training"
    CORPORATE_TRAINING = "corporate-training"

    # Quality Assurance
    PEDAGOGICAL_REVIEWER = "pedagogical-reviewer"
    QUALITY_ASSURANCE = "quality-assurance"
    ACCESSIBILITY_VALIDATOR = "accessibility-validator"
    STANDARDS_COMPLIANCE = "standards-compliance"

    # Packaging & Validation
    SCORM_VALIDATOR = "scorm-validator"

    # Analytics
    LEARNING_ANALYTICS = "learning-analytics"
    AB_TESTING = "ab-testing"

    # Project & Workflow Management
    PROJECT_PLANNING = "project-planning"
    REVIEW_WORKFLOW = "review-workflow"
    CONTENT_LIBRARY = "content-library"

    # Technical & Operations
    PERFORMANCE_OPTIMIZATION = "performance-optimization"
    RIGHTS_MANAGEMENT = "rights-management"

    # Business & Strategy
    MARKET_INTELLIGENCE = "market-intelligence"
    SALES_ENABLEMENT = "sales-enablement"

    # Internationalization
    LOCALIZATION = "localization"


class AgentJobStatus(str, PyEnum):
    """Agent job execution status."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Database Models
class AgentJob(Base):
    """Agent job execution record."""

    __tablename__ = "agent_jobs"

    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False, default=AgentJobStatus.QUEUED, index=True)

    # Task configuration
    task_description = Column(Text, nullable=False)
    parameters = Column(JSON, nullable=True)  # Grade levels, subjects, etc.

    # Execution details
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    progress_percentage = Column(Integer, default=0)
    progress_message = Column(Text, nullable=True)

    # Results
    output_content = Column(Text, nullable=True)  # Generated content
    output_metadata = Column(JSON, nullable=True)  # Metadata, standards, etc.
    error_message = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="agent_jobs")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Pydantic Schemas
class AgentJobCreate(BaseModel):
    """Schema for creating an agent job."""

    agent_type: AgentType
    task_description: str = Field(..., min_length=10, description="Description of the task")
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional parameters (grade_levels, subjects, state, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "agent_type": "curriculum-architect",
                "task_description": "Create a 5th grade Texas math curriculum for fractions",
                "parameters": {
                    "grade_levels": ["5"],
                    "subject": "mathematics",
                    "state": "texas",
                    "topics": ["fractions", "decimals"],
                    "standards": ["TEKS.5.3.K", "TEKS.5.3.L"]
                }
            }
        }


class AgentJobUpdate(BaseModel):
    """Schema for updating agent job status."""

    status: Optional[AgentJobStatus] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    progress_message: Optional[str] = None
    output_content: Optional[str] = None
    output_metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class AgentJobInDB(BaseModel):
    """Schema for agent job from database."""

    id: int
    agent_type: str
    user_id: int
    status: str
    task_description: str
    parameters: Optional[Dict[str, Any]]

    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    progress_percentage: int
    progress_message: Optional[str]

    output_content: Optional[str]
    output_metadata: Optional[Dict[str, Any]]
    error_message: Optional[str]

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class AgentInfo(BaseModel):
    """Information about an available agent."""

    id: str
    name: str
    description: str
    category: str
    estimated_time: str  # "2-3 hours", "30-60 minutes", etc.
    productivity_gain: str  # "10x", "5-7x", etc.
    capabilities: List[str]
    required_role: str  # Minimum role required

    class Config:
        json_schema_extra = {
            "example": {
                "id": "curriculum-architect",
                "name": "Curriculum Architect",
                "description": "Design complete curriculum structures with standards alignment",
                "category": "curriculum-design",
                "estimated_time": "2-4 hours",
                "productivity_gain": "10x",
                "capabilities": [
                    "Scope and sequence development",
                    "Learning objectives writing",
                    "Standards alignment",
                    "Assessment blueprint creation"
                ],
                "required_role": "author"
            }
        }


class AgentJobResult(BaseModel):
    """Complete agent job result with content."""

    job: AgentJobInDB
    generated_content: Optional[str]
    metadata: Optional[Dict[str, Any]]
    suggestions: Optional[List[str]]  # Suggested next steps

    class Config:
        json_schema_extra = {
            "example": {
                "job": {"id": 1, "status": "completed", "progress_percentage": 100},
                "generated_content": "# Lesson: Introduction to Fractions\n\n## Learning Objectives...",
                "metadata": {
                    "standards_aligned": ["TEKS.5.3.K"],
                    "grade_level": "5",
                    "estimated_duration": "45 minutes"
                },
                "suggestions": [
                    "Create assessment for this lesson",
                    "Generate practice activities",
                    "Add scaffolding for ELs"
                ]
            }
        }
