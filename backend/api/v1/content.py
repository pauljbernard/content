"""
Content authoring and management API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database.session import get_db
from core.security import get_current_active_user, get_author
from models.user import User
from models.content import (
    Content,
    ContentCreate,
    ContentUpdate,
    ContentInDB,
    ContentPublic,
    ContentStatus,
    ContentType,
)

router = APIRouter(prefix="/content")


@router.get("/", response_model=List[ContentPublic])
async def list_content(
    skip: int = 0,
    limit: int = 20,
    status: Optional[ContentStatus] = None,
    content_type: Optional[ContentType] = None,
    subject: Optional[str] = None,
    grade_level: Optional[str] = None,
    state: Optional[str] = None,
    author_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List content with optional filters.

    Filters:
    - **status**: Filter by status (draft, in_review, approved, etc.)
    - **content_type**: Filter by type (lesson, assessment, activity)
    - **subject**: Filter by subject
    - **grade_level**: Filter by grade level
    - **state**: Filter by state
    - **author_id**: Filter by author

    Teachers and authors see only published/their own content.
    Editors see all content in review or approved.
    """
    query = db.query(Content)

    # Apply role-based filtering
    if current_user.role == "teacher":
        query = query.filter(Content.status == ContentStatus.PUBLISHED)
    elif current_user.role == "author":
        query = query.filter(
            (Content.status == ContentStatus.PUBLISHED)
            | (Content.author_id == current_user.id)
        )

    # Apply filters
    if status:
        query = query.filter(Content.status == status)
    if content_type:
        query = query.filter(Content.content_type == content_type)
    if subject:
        query = query.filter(Content.subject == subject)
    if grade_level:
        query = query.filter(Content.grade_level == grade_level)
    if state:
        query = query.filter(Content.state == state)
    if author_id:
        query = query.filter(Content.author_id == author_id)

    content_list = query.offset(skip).limit(limit).all()
    return content_list


@router.post("/", response_model=ContentInDB, status_code=status.HTTP_201_CREATED)
async def create_content(
    content: ContentCreate,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """
    Create new content (authors and above).

    Required fields:
    - **title**: Content title
    - **content_type**: Type (lesson, assessment, activity)
    - **subject**: Subject area
    - **file_content**: The actual content (markdown/text)
    """
    db_content = Content(
        **content.dict(), author_id=current_user.id, status=ContentStatus.DRAFT
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content


@router.get("/{content_id}", response_model=ContentInDB)
async def get_content(
    content_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get content by ID."""
    content = db.query(Content).filter(Content.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Check permissions
    if current_user.role == "teacher" and content.status != ContentStatus.PUBLISHED:
        raise HTTPException(status_code=403, detail="Access denied")
    elif (
        current_user.role == "author"
        and content.author_id != current_user.id
        and content.status != ContentStatus.PUBLISHED
    ):
        raise HTTPException(status_code=403, detail="Access denied")

    return content


@router.put("/{content_id}", response_model=ContentInDB)
async def update_content(
    content_id: int,
    content_update: ContentUpdate,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """Update content (author or editor)."""
    content = db.query(Content).filter(Content.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Check permissions
    if current_user.role == "author" and content.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Update fields
    update_data = content_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(content, key, value)

    db.commit()
    db.refresh(content)
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """Delete content (author or knowledge engineer)."""
    content = db.query(Content).filter(Content.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Check permissions
    if (
        current_user.role == "author"
        and content.author_id != current_user.id
        and not current_user.is_superuser
    ):
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(content)
    db.commit()
    return None


@router.post("/{content_id}/submit", response_model=ContentInDB)
async def submit_content_for_review(
    content_id: int,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """
    Submit content for editorial review.

    Content can be submitted if it's in DRAFT or NEEDS_REVISION status.
    This allows authors to resubmit content after addressing reviewer feedback.
    """
    content = db.query(Content).filter(Content.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Allow submission from DRAFT or NEEDS_REVISION status
    if content.status not in [ContentStatus.DRAFT, ContentStatus.NEEDS_REVISION]:
        raise HTTPException(
            status_code=400,
            detail=f"Content must be in draft or needs_revision status to submit. Current status: {content.status}"
        )

    content.status = ContentStatus.IN_REVIEW
    from datetime import datetime

    content.submitted_at = datetime.utcnow()

    db.commit()
    db.refresh(content)
    return content
