"""
Content authoring and management API endpoints.
"""
import json
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


@router.get("/")
async def list_content(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = Query(None),
    content_type: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    grade_level: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    author_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List content with optional filters and pagination.

    Returns:
    - **items**: List of content items
    - **total**: Total count of items matching filters
    - **skip**: Current offset
    - **limit**: Page size

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

    # Apply filters (convert empty strings to None)
    if status and status.strip():
        try:
            status_enum = ContentStatus(status)
            query = query.filter(Content.status == status_enum)
        except ValueError:
            pass  # Invalid status value, ignore filter
    if content_type and content_type.strip():
        try:
            content_type_enum = ContentType(content_type)
            query = query.filter(Content.content_type == content_type_enum)
        except ValueError:
            pass  # Invalid content_type value, ignore filter
    if subject and subject.strip():
        query = query.filter(Content.subject == subject)
    if grade_level and grade_level.strip():
        query = query.filter(Content.grade_level == grade_level)
    if state and state.strip():
        query = query.filter(Content.state == state)
    if author_id:
        query = query.filter(Content.author_id == author_id)

    # Get total count BEFORE applying pagination (should not be affected by skip/limit)
    total = query.count()

    # Debug logging
    import sys
    print(f"[DEBUG] Content list - User: {current_user.email}, Role: {current_user.role}", file=sys.stderr, flush=True)
    print(f"[DEBUG] Pagination params - skip: {skip}, limit: {limit}", file=sys.stderr, flush=True)
    print(f"[DEBUG] Total count (before pagination): {total}", file=sys.stderr, flush=True)

    # Apply pagination - this should NOT affect the total count above
    content_list = query.offset(skip).limit(limit).all()
    print(f"[DEBUG] Items returned after pagination: {len(content_list)}", file=sys.stderr, flush=True)

    # Deserialize JSON strings back to lists for all items in response
    for content in content_list:
        if isinstance(content.standards_aligned, str):
            content.standards_aligned = json.loads(content.standards_aligned)
        if isinstance(content.learning_objectives, str):
            content.learning_objectives = json.loads(content.learning_objectives)

    # Calculate pagination metadata
    total_pages = (total + limit - 1) // limit if limit > 0 else 1  # Ceiling division
    current_page = (skip // limit) + 1 if limit > 0 else 1
    has_previous = skip > 0
    has_next = skip + limit < total

    return {
        "items": content_list,
        "total": total,
        "page": current_page,
        "page_size": limit,
        "total_pages": total_pages,
        "has_previous": has_previous,
        "has_next": has_next,
        "skip": skip,
        "limit": limit,
    }


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
    # Convert content to dict and serialize list fields to JSON
    content_dict = content.dict()

    # Serialize list fields to JSON strings for SQLite
    if content_dict.get("standards_aligned"):
        content_dict["standards_aligned"] = json.dumps(content_dict["standards_aligned"])
    else:
        content_dict["standards_aligned"] = json.dumps([])

    if content_dict.get("learning_objectives"):
        content_dict["learning_objectives"] = json.dumps(content_dict["learning_objectives"])
    else:
        content_dict["learning_objectives"] = json.dumps([])

    db_content = Content(
        **content_dict, author_id=current_user.id, status=ContentStatus.DRAFT
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    # Deserialize JSON strings back to lists for response
    if isinstance(db_content.standards_aligned, str):
        db_content.standards_aligned = json.loads(db_content.standards_aligned)
    if isinstance(db_content.learning_objectives, str):
        db_content.learning_objectives = json.loads(db_content.learning_objectives)

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

    # Deserialize JSON strings back to lists for response
    if isinstance(content.standards_aligned, str):
        content.standards_aligned = json.loads(content.standards_aligned)
    if isinstance(content.learning_objectives, str):
        content.learning_objectives = json.loads(content.learning_objectives)

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

    # Serialize list fields to JSON strings for SQLite
    if "standards_aligned" in update_data and update_data["standards_aligned"] is not None:
        update_data["standards_aligned"] = json.dumps(update_data["standards_aligned"])
    if "learning_objectives" in update_data and update_data["learning_objectives"] is not None:
        update_data["learning_objectives"] = json.dumps(update_data["learning_objectives"])

    for key, value in update_data.items():
        setattr(content, key, value)

    db.commit()
    db.refresh(content)

    # Deserialize JSON strings back to lists for response
    if isinstance(content.standards_aligned, str):
        content.standards_aligned = json.loads(content.standards_aligned)
    if isinstance(content.learning_objectives, str):
        content.learning_objectives = json.loads(content.learning_objectives)

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
