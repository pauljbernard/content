"""
Standards models for educational standards management.

Supports importing and managing standards from various sources:
- State standards (TEKS, MAFS, etc.)
- National standards (CCSS, NGSS, etc.)
- International standards (IB, Cambridge, etc.)
"""
import json
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


class StandardType(str, Enum):
    """Standard type enumeration."""

    STATE = "state"
    NATIONAL = "national"
    INTERNATIONAL = "international"
    DISTRICT = "district"


class StandardStatus(str, Enum):
    """Standard import/publication status."""

    DRAFT = "draft"
    IMPORTING = "importing"
    IMPORTED = "imported"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class StandardSubject(str, Enum):
    """Subject area enumeration."""

    MATHEMATICS = "mathematics"
    ELA = "ela"
    SCIENCE = "science"
    SOCIAL_STUDIES = "social_studies"
    COMPUTER_SCIENCE = "computer_science"
    WORLD_LANGUAGES = "world_languages"
    FINE_ARTS = "fine_arts"
    PHYSICAL_EDUCATION = "physical_education"
    HEALTH = "health"
    CTE = "career_technical_education"
    GENERAL = "general"  # Cross-curricular standards


class Standard(Base):
    """Educational Standard database model."""

    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, index=True)

    # Identity
    name = Column(String, nullable=False, index=True)
    short_name = Column(String, nullable=False, index=True)  # e.g., "TEKS Math"
    code = Column(String, nullable=False, unique=True, index=True)  # e.g., "TEKS-MATH-TX"

    # Classification
    type = Column(SQLEnum(StandardType), nullable=False, index=True)
    subject = Column(SQLEnum(StandardSubject), nullable=False, index=True)
    grade_levels = Column(Text)  # JSON array, e.g., ["K", "1", "2"] or ["9-12"]

    # Source information
    source_organization = Column(String, nullable=False)  # e.g., "Texas Education Agency"
    source_url = Column(String, nullable=True)
    version = Column(String, nullable=True)  # e.g., "2023", "2.0"
    year = Column(Integer, nullable=True)

    # Geographic scope
    state = Column(String, nullable=True)  # For state standards
    district = Column(String, nullable=True)  # For district standards
    country = Column(String, nullable=True)  # For international standards

    # Content
    description = Column(Text, nullable=True)
    scope_notes = Column(Text, nullable=True)

    # Hierarchical structure stored as JSON
    # Example: {
    #   "domains": [
    #     {
    #       "id": "NUM",
    #       "name": "Number and Operations",
    #       "strands": [
    #         {
    #           "id": "NUM.1",
    #           "name": "Understand place value",
    #           "standards": [
    #             {
    #               "id": "NUM.1.A",
    #               "code": "TEKS.3.2A",
    #               "text": "Compose and decompose numbers...",
    #               "grade_level": "3"
    #             }
    #           ]
    #         }
    #       ]
    #     }
    #   ]
    # }
    structure = Column(Text, nullable=False)  # JSON hierarchical structure

    # Flat list of all individual standards for quick lookup
    # Example: [
    #   {
    #     "code": "TEKS.3.2A",
    #     "text": "Compose and decompose numbers...",
    #     "grade_level": "3",
    #     "domain": "Number and Operations",
    #     "strand": "Understand place value"
    #   }
    # ]
    standards_list = Column(Text, nullable=False)  # JSON flat list for easy reference

    # Metadata
    status = Column(SQLEnum(StandardStatus), default=StandardStatus.DRAFT, index=True)
    imported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    import_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    # Statistics
    total_standards_count = Column(Integer, default=0)  # Total number of individual standards

    # Relationships
    imported_by = relationship("User", foreign_keys=[imported_by_id])


class StandardImportJob(Base):
    """Track standard import jobs."""

    __tablename__ = "standard_import_jobs"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, ForeignKey("standards.id"), nullable=True)

    # Job details
    source_type = Column(String, nullable=False)  # url, file, api, manual
    source_location = Column(String, nullable=False)  # URL, file path, API endpoint
    format = Column(String, nullable=False)  # pdf, html, xml, json, csv

    # Processing
    status = Column(String, nullable=False, default="queued")  # queued, running, completed, failed
    progress_percentage = Column(Integer, default=0)
    progress_message = Column(String, nullable=True)

    # Results
    standards_extracted = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    import_log = Column(Text, nullable=True)  # JSON log of import process

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    standard = relationship("Standard", foreign_keys=[standard_id])


# Pydantic schemas


class StandardBase(BaseModel):
    """Base standard schema."""

    name: str
    short_name: str
    code: str
    type: StandardType
    subject: StandardSubject
    source_organization: str
    source_url: Optional[str] = None
    version: Optional[str] = None
    year: Optional[int] = None
    state: Optional[str] = None
    district: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    scope_notes: Optional[str] = None


class StandardCreate(StandardBase):
    """Schema for creating a standard."""

    grade_levels: List[str] = []
    structure: Dict[str, Any]
    standards_list: List[Dict[str, Any]]
    import_notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Texas Essential Knowledge and Skills - Mathematics",
                "short_name": "TEKS Mathematics",
                "code": "TEKS-MATH-TX",
                "type": "state",
                "subject": "mathematics",
                "source_organization": "Texas Education Agency",
                "source_url": "https://tea.texas.gov/academics/curriculum-standards/teks",
                "version": "2023",
                "year": 2023,
                "state": "texas",
                "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                "description": "The Texas Essential Knowledge and Skills for Mathematics",
                "structure": {
                    "domains": [
                        {
                            "id": "NUM",
                            "name": "Number and Operations",
                            "strands": [
                                {
                                    "id": "NUM.1",
                                    "name": "Understand place value",
                                    "standards": [
                                        {
                                            "id": "NUM.1.A",
                                            "code": "TEKS.3.2A",
                                            "text": "Compose and decompose numbers up to 100,000",
                                            "grade_level": "3"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "standards_list": [
                    {
                        "code": "TEKS.3.2A",
                        "text": "Compose and decompose numbers up to 100,000",
                        "grade_level": "3",
                        "domain": "Number and Operations",
                        "strand": "Understand place value"
                    }
                ]
            }
        }


class StandardUpdate(BaseModel):
    """Schema for updating a standard."""

    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    scope_notes: Optional[str] = None
    status: Optional[StandardStatus] = None
    structure: Optional[Dict[str, Any]] = None
    standards_list: Optional[List[Dict[str, Any]]] = None


class StandardInDB(StandardBase):
    """Standard schema with database fields."""

    id: int
    grade_levels: List[str] = []
    structure: Dict[str, Any]
    standards_list: List[Dict[str, Any]]
    status: StandardStatus
    imported_by_id: int
    import_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    total_standards_count: int

    @classmethod
    def model_validate(cls, obj: Any, **kwargs):
        """Custom validation to deserialize JSON strings from database."""
        if hasattr(obj, 'grade_levels') and isinstance(obj.grade_levels, str):
            obj.grade_levels = json.loads(obj.grade_levels) if obj.grade_levels else []
        if hasattr(obj, 'structure') and isinstance(obj.structure, str):
            obj.structure = json.loads(obj.structure) if obj.structure else {}
        if hasattr(obj, 'standards_list') and isinstance(obj.standards_list, str):
            obj.standards_list = json.loads(obj.standards_list) if obj.standards_list else []
        return super().model_validate(obj, **kwargs)

    class Config:
        from_attributes = True


class StandardPublic(BaseModel):
    """Public standard schema (summary for lists)."""

    id: int
    name: str
    short_name: str
    code: str
    type: StandardType
    subject: StandardSubject
    grade_levels: List[str]
    source_organization: str
    version: Optional[str]
    year: Optional[int]
    state: Optional[str]
    status: StandardStatus
    total_standards_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StandardImportJobCreate(BaseModel):
    """Schema for creating a standard import job."""

    source_type: str = Field(..., pattern="^(url|file|api|manual|case_network)$")
    source_location: str
    format: str = Field(..., pattern="^(case|pdf|html|xml|json|csv|manual)$")

    # Initial standard metadata
    name: str
    short_name: str
    code: str
    type: StandardType
    subject: StandardSubject
    source_organization: str
    state: Optional[str] = None
    district: Optional[str] = None
    country: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "source_type": "url",
                "source_location": "https://case.georgiastandards.org/api/v1/CFPackages/123abc",
                "format": "case",
                "name": "Texas Essential Knowledge and Skills - Mathematics",
                "short_name": "TEKS Mathematics",
                "code": "TEKS-MATH-TX",
                "type": "state",
                "subject": "mathematics",
                "source_organization": "Texas Education Agency",
                "state": "texas"
            }
        }


class StandardImportJobInDB(BaseModel):
    """Standard import job schema with database fields."""

    id: int
    standard_id: Optional[int]
    source_type: str
    source_location: str
    format: str
    status: str
    progress_percentage: int
    progress_message: Optional[str]
    standards_extracted: int
    error_message: Optional[str]
    import_log: Optional[Dict[str, Any]]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    @classmethod
    def model_validate(cls, obj: Any, **kwargs):
        """Custom validation to deserialize JSON strings from database."""
        if hasattr(obj, 'import_log') and isinstance(obj.import_log, str):
            obj.import_log = json.loads(obj.import_log) if obj.import_log else {}
        return super().model_validate(obj, **kwargs)

    class Config:
        from_attributes = True
