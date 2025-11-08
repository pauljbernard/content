"""
Migration endpoints for system setup and data migration.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.content_type import ContentTypeModel
from models.user import User
from core.security import get_current_active_user
import uuid

router = APIRouter()


@router.post("/setup-legacy-content-type")
async def setup_legacy_content_type(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a system content type for legacy Content model.
    This allows migration from the old hardcoded Content system to the flexible content type system.

    Only knowledge engineers can run migrations.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=403,
            detail="Only knowledge engineers can run migrations"
        )

    # Check if it already exists
    existing = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == "Legacy Content"
    ).first()

    if existing:
        return {
            "message": "Legacy Content type already exists",
            "content_type_id": existing.id
        }

    # Create the Legacy Content type matching the old Content model schema
    legacy_content_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Legacy Content",
        description="System content type for legacy lessons, assessments, activities, and guides. This type matches the original Content model schema.",
        icon="document-text",
        is_system=True,
        created_by=current_user.id,
        attributes=[
            {
                "name": "title",
                "label": "Title",
                "type": "text",
                "required": True,
                "help_text": "Content title",
                "config": {"maxLength": 200},
                "order_index": 0,
            },
            {
                "name": "content_type",
                "label": "Content Type",
                "type": "choice",
                "required": True,
                "help_text": "Type of content",
                "config": {
                    "choices": ["lesson", "assessment", "activity", "guide", "framework"],
                    "multiple": False,
                },
                "order_index": 1,
            },
            {
                "name": "subject",
                "label": "Subject",
                "type": "choice",
                "required": True,
                "help_text": "Subject area",
                "config": {
                    "choices": ["mathematics", "ela", "science", "social_studies", "computer_science", "other"],
                    "multiple": False,
                },
                "order_index": 2,
            },
            {
                "name": "grade_level",
                "label": "Grade Level",
                "type": "text",
                "required": False,
                "help_text": "Grade level or range (e.g., '5' or '9-12')",
                "config": {"maxLength": 20},
                "order_index": 3,
            },
            {
                "name": "state",
                "label": "State",
                "type": "text",
                "required": False,
                "help_text": "State/district (leave blank for national content)",
                "config": {"maxLength": 50},
                "order_index": 4,
            },
            {
                "name": "curriculum_id",
                "label": "Curriculum ID",
                "type": "text",
                "required": False,
                "help_text": "Reference to curriculum config (e.g., 'hmh-math-tx')",
                "config": {"maxLength": 100},
                "order_index": 5,
            },
            {
                "name": "learning_objectives",
                "label": "Learning Objectives",
                "type": "json",
                "required": False,
                "help_text": "Array of learning objectives",
                "config": {},
                "order_index": 6,
            },
            {
                "name": "standards_aligned",
                "label": "Standards Aligned",
                "type": "json",
                "required": False,
                "help_text": "Array of standard IDs (e.g., ['TEKS.5.3A', 'TEKS.5.3B'])",
                "config": {},
                "order_index": 7,
            },
            {
                "name": "duration_minutes",
                "label": "Duration (minutes)",
                "type": "number",
                "required": False,
                "help_text": "Estimated duration in minutes",
                "config": {"min": 0, "step": 5},
                "order_index": 8,
            },
            {
                "name": "file_content",
                "label": "Content",
                "type": "rich_text",
                "required": True,
                "help_text": "Main content (Markdown or HTML)",
                "config": {},
                "order_index": 9,
            },
            {
                "name": "knowledge_files_used",
                "label": "Knowledge Files Used",
                "type": "json",
                "required": False,
                "help_text": "Array of knowledge base file paths used in creating this content",
                "config": {},
                "order_index": 10,
            },
        ]
    )

    db.add(legacy_content_type)
    db.commit()
    db.refresh(legacy_content_type)

    return {
        "message": "Legacy Content type created successfully",
        "content_type_id": legacy_content_type.id,
        "attributes_count": len(legacy_content_type.attributes),
        "next_steps": [
            "Legacy content can now be migrated to content instances",
            "Future content should be created as instances of flexible content types",
            "The old /content endpoint can eventually be deprecated"
        ]
    }


@router.post("/migrate-legacy-content")
async def migrate_legacy_content(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Migrate existing Content records to the flexible content type system.

    This creates content instances from the legacy Content table.
    Run this after creating the Legacy Content type.

    Only knowledge engineers can run migrations.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=403,
            detail="Only knowledge engineers can run migrations"
        )

    from models.content import Content
    from models.content_type import ContentInstanceModel
    import json

    # Get the Legacy Content type
    legacy_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == "Legacy Content"
    ).first()

    if not legacy_type:
        raise HTTPException(
            status_code=404,
            detail="Legacy Content type not found. Run /setup-legacy-content-type first."
        )

    # Get legacy content records
    legacy_content = db.query(Content).offset(offset).limit(limit).all()

    migrated_count = 0
    skipped_count = 0
    errors = []

    for content in legacy_content:
        try:
            # Check if already migrated (by checking for instance with same ID)
            existing = db.query(ContentInstanceModel).filter(
                ContentInstanceModel.id == f"legacy-{content.id}"
            ).first()

            if existing:
                skipped_count += 1
                continue

            # Parse JSON fields
            try:
                standards_aligned = json.loads(content.standards_aligned) if content.standards_aligned else []
            except:
                standards_aligned = []

            try:
                knowledge_files_used = json.loads(content.knowledge_files_used) if content.knowledge_files_used else []
            except:
                knowledge_files_used = []

            try:
                learning_objectives = json.loads(content.learning_objectives) if content.learning_objectives else []
            except:
                learning_objectives = []

            # Create instance data matching the Legacy Content type schema
            instance_data = {
                "title": content.title,
                "content_type": content.content_type.value,
                "subject": content.subject,
                "grade_level": content.grade_level,
                "state": content.state,
                "curriculum_id": content.curriculum_id,
                "learning_objectives": learning_objectives,
                "standards_aligned": standards_aligned,
                "duration_minutes": content.duration_minutes,
                "file_content": content.file_content,
                "knowledge_files_used": knowledge_files_used,
            }

            # Map status
            status_mapping = {
                "draft": "draft",
                "in_review": "draft",
                "needs_revision": "draft",
                "approved": "published",
                "published": "published",
                "archived": "archived",
            }

            # Create instance
            instance = ContentInstanceModel(
                id=f"legacy-{content.id}",  # Prefix to track migration
                content_type_id=legacy_type.id,
                data=instance_data,
                status=status_mapping.get(content.status.value, "draft"),
                created_by=content.author_id,
                created_at=content.created_at,
                updated_at=content.updated_at,
            )

            db.add(instance)
            migrated_count += 1

        except Exception as e:
            errors.append({
                "content_id": content.id,
                "title": content.title,
                "error": str(e)
            })

    if migrated_count > 0:
        db.commit()

    return {
        "migrated": migrated_count,
        "skipped": skipped_count,
        "errors": errors,
        "total_processed": len(legacy_content),
        "offset": offset,
        "limit": limit,
        "message": f"Migrated {migrated_count} content items to flexible content type system"
    }


@router.get("/migration-status")
async def get_migration_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get status of legacy content migration.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=403,
            detail="Only knowledge engineers can view migration status"
        )

    from models.content import Content
    from models.content_type import ContentInstanceModel

    # Check if Legacy Content type exists
    legacy_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == "Legacy Content"
    ).first()

    if not legacy_type:
        return {
            "legacy_type_created": False,
            "message": "Run /setup-legacy-content-type to create the Legacy Content type"
        }

    # Count legacy content
    total_legacy = db.query(Content).count()

    # Count migrated instances
    migrated_count = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == legacy_type.id
    ).count()

    return {
        "legacy_type_created": True,
        "legacy_type_id": legacy_type.id,
        "total_legacy_content": total_legacy,
        "migrated_instances": migrated_count,
        "remaining_to_migrate": total_legacy - migrated_count,
        "migration_complete": migrated_count >= total_legacy,
    }
