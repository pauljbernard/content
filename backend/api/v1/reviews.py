"""
Content review and approval workflow API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database.session import get_db
from core.security import get_current_active_user, get_editor
from models.user import User
from models.content import (
    Content,
    ContentReview,
    ContentReviewCreate,
    ContentReviewInDB,
    ContentStatus,
)

router = APIRouter(prefix="/reviews")


@router.get("/pending", response_model=List[dict])
async def get_pending_reviews(
    current_user: User = Depends(get_editor), db: Session = Depends(get_db)
):
    """
    Get content pending review (editors only).

    Returns all content items with status 'in_review'.
    """
    pending_content = (
        db.query(Content).filter(Content.status == ContentStatus.IN_REVIEW).all()
    )

    return [
        {
            "content_id": content.id,
            "title": content.title,
            "content_type": content.content_type,
            "subject": content.subject,
            "grade_level": content.grade_level,
            "author_id": content.author_id,
            "submitted_at": content.submitted_at,
        }
        for content in pending_content
    ]


@router.post("/", response_model=ContentReviewInDB, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ContentReviewCreate,
    current_user: User = Depends(get_editor),
    db: Session = Depends(get_db),
):
    """
    Create a content review (editors only).

    Required fields:
    - **content_id**: ID of content being reviewed
    - **status**: Review outcome (approved, needs_revision, rejected)
    - **comments**: Review comments and feedback
    - **checklist_results**: Results of quality checklist
    - **rating**: Quality rating (1-5)
    """
    # Check if content exists
    content = db.query(Content).filter(Content.id == review.content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Create review
    db_review = ContentReview(**review.dict(), reviewer_id=current_user.id)
    db.add(db_review)

    # Update content status based on review
    if review.status == "approved":
        content.status = ContentStatus.APPROVED
        content.approved_at = datetime.utcnow()
    elif review.status == "needs_revision":
        content.status = ContentStatus.NEEDS_REVISION
    elif review.status == "rejected":
        content.status = ContentStatus.DRAFT

    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/content/{content_id}", response_model=List[ContentReviewInDB])
async def get_content_reviews(
    content_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all reviews for a content item."""
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

    reviews = (
        db.query(ContentReview).filter(ContentReview.content_id == content_id).all()
    )
    return reviews


@router.post("/content/{content_id}/approve", response_model=dict)
async def approve_content(
    content_id: int,
    current_user: User = Depends(get_editor),
    db: Session = Depends(get_db),
):
    """Approve content for publication (editors only)."""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.status != ContentStatus.APPROVED:
        raise HTTPException(
            status_code=400, detail="Content must be approved before publishing"
        )

    content.status = ContentStatus.PUBLISHED
    content.published_at = datetime.utcnow()

    db.commit()
    return {"message": "Content published successfully", "content_id": content_id}


@router.get("/my-reviews", response_model=List[ContentReviewInDB])
async def get_my_reviews(
    current_user: User = Depends(get_editor), db: Session = Depends(get_db)
):
    """Get all reviews created by current user (editors only)."""
    reviews = (
        db.query(ContentReview)
        .filter(ContentReview.reviewer_id == current_user.id)
        .all()
    )
    return reviews
