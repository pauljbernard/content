"""
Workflow models for Professor Framework multi-agent orchestration.

Workflows allow users to chain multiple agents together in sequence,
passing outputs from one agent as inputs to the next.
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum as PyEnum
from database.session import Base


# Enums
class WorkflowStatus(str, PyEnum):
    """Workflow execution status."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class WorkflowExecutionStatus(str, PyEnum):
    """Workflow execution run status."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIALLY_COMPLETED = "partially_completed"


# Database Models
class AgentWorkflow(Base):
    """Multi-agent workflow definition."""

    __tablename__ = "agent_workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Ownership
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_template = Column(Boolean, default=False)  # Is this a pre-built template?
    is_public = Column(Boolean, default=False)  # Can other users use this?

    # Workflow definition
    status = Column(String(20), nullable=False, default=WorkflowStatus.DRAFT)
    steps = Column(JSON, nullable=False)  # List of workflow steps

    # Metadata
    tags = Column(JSON, nullable=True)  # Tags for categorization
    estimated_duration = Column(String(50), nullable=True)  # e.g., "2-4 hours"

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class WorkflowExecution(Base):
    """Workflow execution run record."""

    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("agent_workflows.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(String(30), nullable=False, default=WorkflowExecutionStatus.QUEUED, index=True)

    # Execution tracking
    current_step_index = Column(Integer, default=0)
    step_results = Column(JSON, nullable=True)  # Results from each step

    # Input/Output
    input_parameters = Column(JSON, nullable=True)
    final_output = Column(Text, nullable=True)

    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Error handling
    error_message = Column(Text, nullable=True)
    failed_step_index = Column(Integer, nullable=True)

    # Relationships
    workflow = relationship("AgentWorkflow", back_populates="executions")
    user = relationship("User")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Pydantic Schemas
class WorkflowStep(BaseModel):
    """Single step in a workflow."""

    agent_type: str = Field(..., description="Agent to invoke")
    name: str = Field(..., description="Human-readable step name")
    description: Optional[str] = Field(None, description="What this step does")

    # Configuration
    task_template: str = Field(..., description="Task description template (can use {previous_output})")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Static parameters")

    # Flow control
    use_previous_output: bool = Field(True, description="Pass previous step output as context")
    required: bool = Field(True, description="If False, continue even if this step fails")

    class Config:
        json_schema_extra = {
            "example": {
                "agent_type": "content-developer",
                "name": "Generate Lesson",
                "description": "Create initial lesson content",
                "task_template": "Create a {subject} lesson for grade {grade_level}",
                "parameters": {"subject": "mathematics", "grade_level": "5"},
                "use_previous_output": False,
                "required": True
            }
        }


class WorkflowCreate(BaseModel):
    """Schema for creating a workflow."""

    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    steps: List[WorkflowStep] = Field(..., min_items=2, description="At least 2 steps required")
    tags: Optional[List[str]] = None
    is_public: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Complete Content Development",
                "description": "Generate content, review pedagogy, and validate accessibility",
                "steps": [
                    {
                        "agent_type": "content-developer",
                        "name": "Generate Content",
                        "task_template": "Create a lesson on {topic}",
                        "parameters": {"topic": "fractions"},
                        "use_previous_output": False
                    },
                    {
                        "agent_type": "pedagogical-reviewer",
                        "name": "Review Pedagogy",
                        "task_template": "Review the following content for pedagogical soundness: {previous_output}",
                        "use_previous_output": True
                    }
                ],
                "tags": ["lesson-development", "quality-assurance"]
            }
        }


class WorkflowUpdate(BaseModel):
    """Schema for updating a workflow."""

    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    steps: Optional[List[WorkflowStep]] = Field(None, min_items=2)
    tags: Optional[List[str]] = None
    status: Optional[WorkflowStatus] = None
    is_public: Optional[bool] = None


class WorkflowInDB(BaseModel):
    """Workflow database schema."""

    id: int
    name: str
    description: Optional[str]
    created_by: int
    is_template: bool
    is_public: bool
    status: str
    steps: List[Dict[str, Any]]
    tags: Optional[List[str]]
    estimated_duration: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class WorkflowExecutionCreate(BaseModel):
    """Schema for starting a workflow execution."""

    workflow_id: int
    input_parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters to pass to workflow")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": 1,
                "input_parameters": {
                    "topic": "fractions",
                    "grade_level": "5",
                    "subject": "mathematics",
                    "state": "texas"
                }
            }
        }


class WorkflowExecutionInDB(BaseModel):
    """Workflow execution database schema."""

    id: int
    workflow_id: int
    user_id: int
    status: str
    current_step_index: int
    step_results: Optional[List[Dict[str, Any]]]
    input_parameters: Optional[Dict[str, Any]]
    final_output: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    failed_step_index: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class WorkflowExecutionDetail(WorkflowExecutionInDB):
    """Detailed workflow execution with workflow info."""

    workflow: WorkflowInDB

    class Config:
        from_attributes = True
