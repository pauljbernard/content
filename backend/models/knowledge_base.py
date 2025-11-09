"""
Knowledge Base embeddings model for vector search.

Stores vector embeddings for knowledge base markdown files
to enable semantic search across curriculum knowledge.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, Field
from typing import Optional

from database.session import Base


class KnowledgeBaseEmbeddingModel(Base):
    """
    Vector embeddings for knowledge base files.

    Enables semantic search across curriculum knowledge, frameworks,
    instructional routines, and educational guidance.
    """
    __tablename__ = "knowledge_base_embeddings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # File identification
    file_path = Column(String(500), nullable=False, unique=True, index=True)
    file_name = Column(String(255), nullable=False)

    # Content
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)  # SHA-256 hash for change detection

    # Vector embedding column (added by vector_search service)
    # embedding = Column(Vector(1536))  # Created dynamically by add_embedding_column()

    # Categorization
    category = Column(String(50), nullable=False, index=True)  # universal, district, subject, etc.
    subject = Column(String(50))  # mathematics, ela, science, etc.
    state = Column(String(50))  # texas, california, etc.

    # Metadata
    file_size_bytes = Column(Integer)
    last_modified = Column(DateTime)
    last_indexed = Column(DateTime, default=datetime.utcnow)
    indexed_by = Column(String(50), default="system")  # service or user that indexed

    # Index status
    index_version = Column(String(20), default="1.0")  # For tracking schema changes


class KnowledgeBaseEmbeddingCreate(BaseModel):
    """Schema for creating knowledge base embedding."""
    file_path: str = Field(..., min_length=1)
    file_name: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    content_hash: str = Field(..., min_length=64, max_length=64)
    category: str
    subject: Optional[str] = None
    state: Optional[str] = None
    file_size_bytes: Optional[int] = None
    last_modified: Optional[datetime] = None


class KnowledgeBaseEmbeddingInDB(BaseModel):
    """Knowledge base embedding with database fields."""
    id: str
    file_path: str
    file_name: str
    content: str
    content_hash: str
    category: str
    subject: Optional[str]
    state: Optional[str]
    file_size_bytes: Optional[int]
    last_modified: Optional[datetime]
    last_indexed: datetime
    indexed_by: str
    index_version: str

    class Config:
        from_attributes = True


class KnowledgeBaseSearchResult(BaseModel):
    """Knowledge base search result with similarity score."""
    id: str
    file_path: str
    file_name: str
    content: str
    category: str
    subject: Optional[str]
    state: Optional[str]
    similarity: float

    class Config:
        from_attributes = True
