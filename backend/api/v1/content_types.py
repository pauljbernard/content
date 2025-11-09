"""
Content Type System API endpoints - flexible schema-less CMS.

This module provides Contentful/Strapi-like content modeling capabilities:
- CRUD operations for content type definitions
- CRUD operations for content instances
- Dynamic validation based on content type schema
- Content relationships management
"""
import json
import uuid
import logging
import sys
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database.session import get_db
from core.security import get_current_active_user, get_editor
from models.user import User
from utils.validation import validate_instance_data
from services.content_instance_service import content_instance_service
from services.vector_search import get_vector_search_service
from models.content_type import (
    ContentTypeModel,
    ContentInstanceModel,
    ContentRelationshipModel,
    ContentTypeCreate,
    ContentTypeUpdate,
    ContentTypeInDB,
    ContentInstanceCreate,
    ContentInstanceUpdate,
    ContentInstanceInDB,
    ContentInstanceWithType,
    AttributeDefinition,
    ContentStatsResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content-types")

# ============================================================================
# STATS ENDPOINT
# ============================================================================

@router.get("/stats", response_model=ContentStatsResponse)
async def get_content_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get statistics about content types and instances.

    Returns:
    - total_content_types: Total number of content types
    - total_instances: Total number of content instances across all types
    - instances_by_status: Breakdown of instances by status (draft, in_review, published, archived)
    - instances_by_type: Count of instances per content type
    """
    # Total content types
    total_content_types = db.query(ContentTypeModel).count()

    # Total instances
    total_instances = db.query(ContentInstanceModel).count()

    # Instances by status
    status_counts = db.query(
        ContentInstanceModel.status,
        func.count(ContentInstanceModel.id)
    ).group_by(ContentInstanceModel.status).all()

    instances_by_status = {
        status: count for status, count in status_counts
    }

    # Instances by content type
    type_counts = db.query(
        ContentTypeModel.id,
        ContentTypeModel.name,
        func.count(ContentInstanceModel.id).label('count')
    ).outerjoin(
        ContentInstanceModel,
        ContentTypeModel.id == ContentInstanceModel.content_type_id
    ).group_by(
        ContentTypeModel.id,
        ContentTypeModel.name
    ).all()

    instances_by_type = [
        {
            "content_type_id": type_id,
            "content_type_name": type_name,
            "count": count
        }
        for type_id, type_name, count in type_counts
    ]

    return ContentStatsResponse(
        total_content_types=total_content_types,
        total_instances=total_instances,
        instances_by_status=instances_by_status,
        instances_by_type=instances_by_type
    )


# ============================================================================
# CONTENT TYPE ENDPOINTS
# ============================================================================

@router.get("/instances/all")
async def list_all_content_instances(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=500, description="Maximum items to return (1-500)"),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    content_type_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List all content instances across all content types with pagination.

    **Pagination (REQUIRED)**:
    - **skip**: Offset for pagination (default: 0, min: 0)
    - **limit**: Maximum items to return (default: 50, min: 1, max: 500)

    **Filters**:
    - **status**: Filter by status (draft, in_review, published, archived)
    - **search**: Search in instance data (basic JSON text search)
    - **content_type_id**: Filter by content type ID

    **Returns**:
    Paginated response with items, total count, and pagination metadata.
    """
    query = db.query(ContentInstanceModel).options(
        joinedload(ContentInstanceModel.content_type)
    )

    # Apply content type filter
    if content_type_id:
        query = query.filter(ContentInstanceModel.content_type_id == content_type_id)

    # Apply status filter
    if status:
        query = query.filter(ContentInstanceModel.status == status)

    # Apply search filter
    if search:
        query = query.filter(
            func.json_extract(ContentInstanceModel.data, '$').contains(search)
        )

    # Apply role-based filtering
    if current_user.role == "author":
        query = query.filter(
            (ContentInstanceModel.status == "published") |
            (ContentInstanceModel.created_by == current_user.id)
        )

    # Get total count
    total = query.count()

    # Apply pagination and order by updated_at desc
    instances = query.order_by(ContentInstanceModel.updated_at.desc()).offset(skip).limit(limit).all()

    # Transform to response model with content type info
    items = []
    for instance in instances:
        instance_dict = {
            "id": instance.id,
            "content_type_id": instance.content_type_id,
            "data": json.loads(instance.data) if isinstance(instance.data, str) else instance.data,
            "status": instance.status,
            "created_by": instance.created_by,
            "updated_by": instance.updated_by,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "published_at": instance.published_at,
            "content_type": {
                "id": instance.content_type.id,
                "name": instance.content_type.name,
                "description": instance.content_type.description,
                "icon": instance.content_type.icon,
                "is_system": instance.content_type.is_system,
                "attributes": [AttributeDefinition(**attr) for attr in instance.content_type.attributes],
                "created_by": instance.content_type.created_by,
                "created_at": instance.content_type.created_at,
                "updated_at": instance.content_type.updated_at,
                "instance_count": 0
            }
        }
        items.append(instance_dict)

    # Return paginated response with metadata
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": skip,
        "has_more": (skip + len(items)) < total
    }


@router.get("/")
async def list_content_types(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum items to return (1-500)"),
    include_system: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List all content type definitions with pagination.

    **Pagination (REQUIRED)**:
    - **skip**: Offset for pagination (default: 0, min: 0)
    - **limit**: Maximum items to return (default: 100, min: 1, max: 500)

    **Filters**:
    - **include_system**: Whether to include system content types (default: true)

    **Returns**:
    Paginated response with items, total count, and pagination metadata.
    """
    query = db.query(ContentTypeModel)

    if not include_system:
        query = query.filter(ContentTypeModel.is_system == False)

    # Get total count
    total = query.count()

    # Get content types with pagination
    content_types = query.offset(skip).limit(limit).all()

    # Add instance counts
    items = []
    for ct in content_types:
        ct_dict = {
            "id": ct.id,
            "name": ct.name,
            "description": ct.description,
            "icon": ct.icon,
            "is_system": ct.is_system,
            "attributes": ct.attributes,
            "is_hierarchical": ct.is_hierarchical,
            "hierarchy_config": ct.hierarchy_config,
            "created_by": ct.created_by,
            "created_at": ct.created_at,
            "updated_at": ct.updated_at,
            "instance_count": db.query(ContentInstanceModel).filter(
                ContentInstanceModel.content_type_id == ct.id
            ).count()
        }
        items.append(ContentTypeInDB(**ct_dict))

    # Return paginated response with metadata
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": skip,
        "has_more": (skip + len(items)) < total
    }


@router.post("/", response_model=ContentTypeInDB, status_code=status.HTTP_201_CREATED)
async def create_content_type(
    content_type: ContentTypeCreate,
    current_user: User = Depends(get_editor),  # Only editors can create types
    db: Session = Depends(get_db),
):
    """
    Create a new content type definition.

    Requires editor or knowledge_engineer role.
    """
    # Check if content type with this name already exists
    existing = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == content_type.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content type with name '{content_type.name}' already exists"
        )

    # Validate attribute definitions
    attribute_names = set()
    for attr in content_type.attributes:
        if attr.name in attribute_names:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate attribute name: '{attr.name}'"
            )
        attribute_names.add(attr.name)

    # Create content type
    db_content_type = ContentTypeModel(
        name=content_type.name,
        description=content_type.description,
        icon=content_type.icon,
        is_system=False,
        attributes=[attr.model_dump() for attr in content_type.attributes],
        created_by=current_user.id
    )

    db.add(db_content_type)
    db.commit()
    db.refresh(db_content_type)

    # Create filtered vector index for this content type
    # This enables efficient semantic search on instances of this type
    try:
        vector_service = get_vector_search_service(db)
        await vector_service.create_content_type_vector_index(db, db_content_type.id)
        logger.info(f"✓ Created vector index for content type: {db_content_type.name}")
    except Exception as e:
        # Non-fatal - log warning but don't fail content type creation
        logger.warning(f"Could not create vector index for content type {db_content_type.id}: {e}")

    return ContentTypeInDB(
        id=db_content_type.id,
        name=db_content_type.name,
        description=db_content_type.description,
        icon=db_content_type.icon,
        is_system=db_content_type.is_system,
        attributes=[AttributeDefinition(**attr) for attr in db_content_type.attributes],
        created_by=db_content_type.created_by,
        created_at=db_content_type.created_at,
        updated_at=db_content_type.updated_at,
        instance_count=0
    )


@router.get("/{content_type_id}", response_model=ContentTypeInDB)
async def get_content_type(
    content_type_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific content type by ID."""
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    instance_count = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type_id
    ).count()

    return ContentTypeInDB(
        id=content_type.id,
        name=content_type.name,
        description=content_type.description,
        icon=content_type.icon,
        is_system=content_type.is_system,
        attributes=[AttributeDefinition(**attr) for attr in content_type.attributes],
        created_by=content_type.created_by,
        created_at=content_type.created_at,
        updated_at=content_type.updated_at,
        instance_count=instance_count
    )


@router.put("/{content_type_id}", response_model=ContentTypeInDB)
async def update_content_type(
    content_type_id: str,
    content_type_update: ContentTypeUpdate,
    current_user: User = Depends(get_editor),
    db: Session = Depends(get_db),
):
    """
    Update a content type definition.

    Only non-system content types can be updated.
    Requires editor or knowledge_engineer role.
    """
    db_content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not db_content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    if db_content_type.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify system content types"
        )

    # Update fields
    update_data = content_type_update.model_dump(exclude_unset=True)

    if "name" in update_data:
        # Check for name conflicts
        existing = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == update_data["name"],
            ContentTypeModel.id != content_type_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Content type with name '{update_data['name']}' already exists"
            )
        db_content_type.name = update_data["name"]

    if "description" in update_data:
        db_content_type.description = update_data["description"]

    if "icon" in update_data:
        db_content_type.icon = update_data["icon"]

    if "attributes" in update_data:
        # Validate attribute definitions
        attribute_names = set()
        for attr in update_data["attributes"]:
            attr_def = attr if isinstance(attr, AttributeDefinition) else AttributeDefinition(**attr)
            if attr_def.name in attribute_names:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Duplicate attribute name: '{attr_def.name}'"
                )
            attribute_names.add(attr_def.name)

        db_content_type.attributes = [
            attr.model_dump() if isinstance(attr, AttributeDefinition) else attr
            for attr in update_data["attributes"]
        ]

    db.commit()
    db.refresh(db_content_type)

    instance_count = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type_id
    ).count()

    return ContentTypeInDB(
        id=db_content_type.id,
        name=db_content_type.name,
        description=db_content_type.description,
        icon=db_content_type.icon,
        is_system=db_content_type.is_system,
        attributes=[AttributeDefinition(**attr) for attr in db_content_type.attributes],
        created_by=db_content_type.created_by,
        created_at=db_content_type.created_at,
        updated_at=db_content_type.updated_at,
        instance_count=instance_count
    )


@router.delete("/{content_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content_type(
    content_type_id: str,
    current_user: User = Depends(get_editor),
    db: Session = Depends(get_db),
):
    """
    Delete a content type.

    Only non-system content types can be deleted.
    Cannot delete if instances exist (use CASCADE carefully).
    Requires editor or knowledge_engineer role.
    """
    db_content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not db_content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    if db_content_type.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete system content types"
        )

    # Check for existing instances
    instance_count = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type_id
    ).count()

    if instance_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete content type with {instance_count} existing instances. Delete instances first."
        )

    db.delete(db_content_type)
    db.commit()


# ============================================================================
# CONTENT INSTANCE ENDPOINTS
# ============================================================================

@router.get("/{content_type_id}/instances")
async def list_content_instances(
    content_type_id: str,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=500, description="Maximum items to return (1-500)"),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List content instances of a specific type with pagination.

    **Pagination (REQUIRED)**:
    - **skip**: Offset for pagination (default: 0, min: 0)
    - **limit**: Maximum items to return (default: 50, min: 1, max: 500)

    **Filters**:
    - **status**: Filter by status (draft, in_review, published, archived)
    - **search**: Search in instance data (basic JSON text search)

    **Returns**:
    Paginated response with items, total count, and pagination metadata.
    """
    # Verify content type exists
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    query = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type_id
    )

    # Apply status filter
    if status:
        query = query.filter(ContentInstanceModel.status == status)

    # Apply search filter (basic JSON text search)
    if search:
        # For SQLite/PostgreSQL JSON contains search
        query = query.filter(
            func.json_extract(ContentInstanceModel.data, '$').contains(search)
        )

    # Apply tenant isolation (except for superusers and system content types)
    is_system_type = content_instance_service.is_system_content_type(db, content_type_id)
    is_superuser = hasattr(current_user, 'is_superuser') and current_user.is_superuser

    if not is_superuser and not is_system_type:
        # Get user's tenant_id
        user_tenant_id = getattr(current_user, 'tenant_id', None)
        if user_tenant_id:
            # Filter by tenant_id in the instance data JSON
            # Note: This is a Python-level filter since JSON querying is database-specific
            logger.info(f"Applying tenant filter: {user_tenant_id} for content type {content_type.name}")

    # Apply role-based filtering
    if current_user.role == "author":
        query = query.filter(
            (ContentInstanceModel.status == "published") |
            (ContentInstanceModel.created_by == current_user.id)
        )
    elif current_user.role == "teacher":
        query = query.filter(ContentInstanceModel.status == "published")

    # Get total count (before tenant filtering)
    total_db_count = query.count()

    # Execute query with pagination
    # Note: For tenant filtering, we fetch more than limit and filter at Python level
    fetch_limit = limit * 2 if (not is_superuser and not is_system_type) else limit
    instances = query.order_by(ContentInstanceModel.created_at.desc()).offset(skip).limit(fetch_limit).all()

    # Apply tenant filtering at Python level (for non-system types)
    if not is_superuser and not is_system_type:
        user_tenant_id = getattr(current_user, 'tenant_id', None)
        if user_tenant_id:
            instances = [
                inst for inst in instances
                if inst.data.get("tenant_id") == user_tenant_id
            ][:limit]  # Re-apply limit after filtering
    else:
        instances = instances[:limit]

    # Convert to response models
    items = [ContentInstanceInDB.model_validate(inst) for inst in instances]

    # Return paginated response with metadata
    return {
        "items": items,
        "total": total_db_count,  # Note: This is total in DB, not after tenant filtering
        "limit": limit,
        "offset": skip,
        "has_more": (skip + len(items)) < total_db_count
    }


@router.post("/{content_type_id}/instances", response_model=ContentInstanceInDB, status_code=status.HTTP_201_CREATED)
async def create_content_instance(
    content_type_id: str,
    instance: ContentInstanceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a new content instance.

    Validates instance data against content type schema.
    """
    # Get content type
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    # Validate instance data using advanced validation system
    errors = validate_instance_data(content_type.attributes, instance.data)

    # Check for unknown fields
    attributes = {attr["name"]: attr for attr in content_type.attributes}
    for data_key in instance.data.keys():
        if data_key not in attributes:
            errors.append(f"Unknown attribute '{data_key}'")

    if errors:
        sys.stderr.write(f"\n{'='*80}\n")
        sys.stderr.write(f"[VALIDATION ERROR] Errors: {errors}\n")
        sys.stderr.write(f"[VALIDATION ERROR] Instance data: {instance.data}\n")
        sys.stderr.write(f"[VALIDATION ERROR] Content type attributes: {content_type.attributes}\n")
        sys.stderr.write(f"{'='*80}\n")
        sys.stderr.flush()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"validation_errors": errors}
        )

    # Automatically add tenant_id to non-system content types
    instance_data = instance.data.copy()
    is_system_type = content_instance_service.is_system_content_type(db, content_type_id)

    if not is_system_type:
        user_tenant_id = getattr(current_user, 'tenant_id', None)
        if user_tenant_id:
            instance_data["tenant_id"] = user_tenant_id
            logger.info(f"Auto-injecting tenant_id {user_tenant_id} for new {content_type.name} instance")

    # Create instance
    db_instance = ContentInstanceModel(
        content_type_id=content_type_id,
        data=instance_data,
        status=instance.status or "draft",
        created_by=current_user.id,
        updated_by=current_user.id
    )

    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)

    # Generate and store vector embedding for semantic search
    # This happens asynchronously and non-blocking
    try:
        vector_service = get_vector_search_service(db)
        await vector_service.update_instance_embedding(
            db=db,
            instance_id=db_instance.id,
            content_data=instance_data
        )
        logger.info(f"✓ Generated embedding for new instance {db_instance.id}")
    except Exception as e:
        # Non-fatal - log warning but don't fail instance creation
        logger.warning(f"Could not generate embedding for instance {db_instance.id}: {e}")

    return ContentInstanceInDB.model_validate(db_instance)


@router.get("/{content_type_id}/instances/tree")
async def list_content_instances_tree(
    content_type_id: str,
    parent_id: Optional[str] = Query(None, description="Parent identifier to get children of (null for root nodes)"),
    skip: int = Query(0, ge=0, description="Number of items to skip at this level"),
    limit: int = Query(100, ge=1, le=500, description="Maximum items to return at this level"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List content instances in tree/hierarchical structure.

    For hierarchical content types (like CASE Standards), this endpoint:
    - Returns root nodes when parent_id is null
    - Returns children when parent_id is specified
    - Includes children_count for each node
    - Supports lazy-loading children on-demand

    **Query Parameters**:
    - **parent_id**: Filter by parent identifier (null/empty for root nodes)
    - **skip**: Offset for pagination
    - **limit**: Maximum items to return

    **Returns**:
    Paginated response with hierarchical metadata for each item.
    """
    from sqlalchemy import cast, String, or_, and_, func

    # Verify content type exists and is hierarchical
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    if not content_type.is_hierarchical:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content type '{content_type.name}' is not hierarchical. Use the regular list endpoint instead."
        )

    # Get hierarchy configuration
    hierarchy_config = content_type.hierarchy_config or {}
    parent_field = hierarchy_config.get("parent_field", "parent")
    children_field = hierarchy_config.get("children_field", "children")
    identifier_field = hierarchy_config.get("identifier_field", "id")
    display_field = hierarchy_config.get("display_field", "name")

    # Build query for instances at this level
    query = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type_id,
        ContentInstanceModel.status == "published"  # Only show published items in tree
    )

    # Filter by parent
    if parent_id is None or parent_id == "" or parent_id == "null":
        # Get root nodes (parent is null, empty, or missing)
        # Use raw SQL for proper ->> operator support
        from sqlalchemy import text as sql_text
        query = query.filter(
            sql_text(f"(data->>'{parent_field}' IS NULL OR data->>'{parent_field}' = '' OR data->>'{parent_field}' = 'null')")
        )
    else:
        # Get children of specific parent
        from sqlalchemy import text as sql_text
        query = query.filter(
            sql_text(f"data->>'{parent_field}' = :parent_val")
        ).params(parent_val=parent_id)

    # Get total count at this level
    total = query.count()

    # Debug logging
    logger.info(f"Tree query: content_type={content_type_id}, parent_id={parent_id}, total={total}")

    # Apply pagination
    items = query.order_by(ContentInstanceModel.created_at).offset(skip).limit(limit).all()
    logger.info(f"Tree query returned {len(items)} items")

    # Build response with hierarchical metadata
    tree_items = []
    for item in items:
        item_data = item.data if isinstance(item.data, dict) else {}
        item_identifier = item_data.get(identifier_field, "")

        # Count children for this node
        children_ids = item_data.get(children_field, [])
        children_count = len(children_ids) if isinstance(children_ids, list) else 0

        # Alternatively, count actual child instances in database
        if children_count == 0 and item_identifier:
            from sqlalchemy import text as sql_text
            children_count = db.query(func.count(ContentInstanceModel.id)).filter(
                ContentInstanceModel.content_type_id == content_type_id,
                sql_text(f"data->>'{parent_field}' = :parent_val")
            ).params(parent_val=item_identifier).scalar()

        tree_items.append({
            "id": item.id,
            "identifier": item_identifier,
            "display_text": item_data.get(display_field, "Untitled"),
            "data": item_data,
            "status": item.status,
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "children_count": children_count,
            "has_children": children_count > 0,
            "is_leaf": children_count == 0
        })

    return {
        "items": tree_items,
        "total": total,
        "limit": limit,
        "offset": skip,
        "has_more": (skip + limit) < total,
        "parent_id": parent_id,
        "level_info": {
            "is_root_level": parent_id is None or parent_id == "" or parent_id == "null",
            "hierarchy_config": hierarchy_config
        }
    }


# Generic content instance endpoints (not type-specific)

@router.get("/instances/{instance_id}", response_model=ContentInstanceWithType)
async def get_content_instance(
    instance_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific content instance with its content type definition."""
    instance = db.query(ContentInstanceModel).options(
        joinedload(ContentInstanceModel.content_type)
    ).filter(ContentInstanceModel.id == instance_id).first()

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content instance not found"
        )

    # Check tenant isolation (except for superusers and system content types)
    is_superuser = hasattr(current_user, 'is_superuser') and current_user.is_superuser
    is_system_type = content_instance_service.is_system_content_type(db, instance.content_type_id)

    if not is_superuser and not is_system_type:
        user_tenant_id = getattr(current_user, 'tenant_id', None)
        if not content_instance_service.instance_belongs_to_tenant(instance, user_tenant_id, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content instance not found"  # Don't reveal it exists in another tenant
            )

    # Check permissions
    if current_user.role == "author" and instance.created_by != current_user.id and instance.status != "published":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own unpublished content"
        )
    elif current_user.role == "teacher" and instance.status != "published":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teachers can only view published content"
        )

    # Prepare response
    content_type_data = ContentTypeInDB(
        id=instance.content_type.id,
        name=instance.content_type.name,
        description=instance.content_type.description,
        icon=instance.content_type.icon,
        is_system=instance.content_type.is_system,
        attributes=[AttributeDefinition(**attr) for attr in instance.content_type.attributes],
        created_by=instance.content_type.created_by,
        created_at=instance.content_type.created_at,
        updated_at=instance.content_type.updated_at,
        instance_count=0
    )

    return ContentInstanceWithType(
        id=instance.id,
        content_type_id=instance.content_type_id,
        data=instance.data,
        status=instance.status,
        created_by=instance.created_by,
        updated_by=instance.updated_by,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
        published_at=instance.published_at,
        content_type=content_type_data
    )


@router.put("/instances/{instance_id}", response_model=ContentInstanceInDB)
async def update_content_instance(
    instance_id: str,
    instance_update: ContentInstanceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update a content instance.

    Authors can update their own content.
    Editors can update any content.
    """
    db_instance = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.id == instance_id
    ).first()

    if not db_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content instance not found"
        )

    # Check tenant isolation (except for superusers and system content types)
    is_superuser = hasattr(current_user, 'is_superuser') and current_user.is_superuser
    is_system_type = content_instance_service.is_system_content_type(db, db_instance.content_type_id)

    if not is_superuser and not is_system_type:
        user_tenant_id = getattr(current_user, 'tenant_id', None)
        if not content_instance_service.instance_belongs_to_tenant(db_instance, user_tenant_id, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content instance not found"  # Don't reveal it exists in another tenant
            )

    # Check permissions
    if current_user.role == "author" and db_instance.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own content"
        )

    # Get content type for validation
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == db_instance.content_type_id
    ).first()

    # Update data
    update_data = instance_update.model_dump(exclude_unset=True)

    if "data" in update_data:
        # Merge new data with existing data
        merged_data = {**db_instance.data, **update_data["data"]}

        # Validate merged data using advanced validation system
        errors = validate_instance_data(content_type.attributes, merged_data)

        # Check for unknown fields
        attributes = {attr["name"]: attr for attr in content_type.attributes}
        for data_key in merged_data.keys():
            if data_key not in attributes:
                errors.append(f"Unknown attribute '{data_key}'")

        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": errors}
            )

        db_instance.data = merged_data

    if "status" in update_data:
        db_instance.status = update_data["status"]

    db_instance.updated_by = current_user.id

    db.commit()
    db.refresh(db_instance)

    # Regenerate vector embedding if data was updated
    # This keeps the semantic search index up-to-date
    if "data" in update_data:
        try:
            vector_service = get_vector_search_service(db)
            await vector_service.update_instance_embedding(
                db=db,
                instance_id=db_instance.id,
                content_data=db_instance.data
            )
            logger.info(f"✓ Regenerated embedding for updated instance {db_instance.id}")
        except Exception as e:
            # Non-fatal - log warning but don't fail instance update
            logger.warning(f"Could not regenerate embedding for instance {db_instance.id}: {e}")

    return ContentInstanceInDB.model_validate(db_instance)


@router.delete("/instances/{instance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content_instance(
    instance_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a content instance.

    Authors can delete their own content.
    Editors can delete any content.
    """
    db_instance = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.id == instance_id
    ).first()

    if not db_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content instance not found"
        )

    # Check tenant isolation (except for superusers and system content types)
    is_superuser = hasattr(current_user, 'is_superuser') and current_user.is_superuser
    is_system_type = content_instance_service.is_system_content_type(db, db_instance.content_type_id)

    if not is_superuser and not is_system_type:
        user_tenant_id = getattr(current_user, 'tenant_id', None)
        if not content_instance_service.instance_belongs_to_tenant(db_instance, user_tenant_id, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content instance not found"  # Don't reveal it exists in another tenant
            )

    # Check permissions
    if current_user.role == "author" and db_instance.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own content"
        )

    db.delete(db_instance)
    db.commit()


# ============================================================================
# EXPORT/IMPORT ENDPOINTS
# ============================================================================

@router.get("/{content_type_id}/export")
async def export_content_type(
    content_type_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Export a content type as JSON template.

    This can be imported later or shared with others.
    Useful for backing up content types or creating portable templates.
    """
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    # Export format (without DB-specific fields)
    export_data = {
        "name": content_type.name,
        "description": content_type.description,
        "icon": content_type.icon,
        "attributes": content_type.attributes,
        "is_system": content_type.is_system,
        "exported_at": datetime.utcnow().isoformat(),
        "exported_by": current_user.email,
        "version": "1.0",
    }

    return export_data


@router.post("/import")
async def import_content_type(
    import_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Import a content type from JSON template.

    Creates a new content type from exported data.
    Editors and knowledge engineers only.
    """
    if current_user.role not in ["editor", "knowledge_engineer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only editors and knowledge engineers can import content types"
        )

    # Validate required fields
    required_fields = ["name", "attributes"]
    missing_fields = [f for f in required_fields if f not in import_data]

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    # Check if name already exists
    existing = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == import_data["name"]
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Content type with name '{import_data['name']}' already exists"
        )

    # Create new content type
    new_content_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name=import_data["name"],
        description=import_data.get("description"),
        icon=import_data.get("icon"),
        is_system=False,  # Imported types are never system types
        attributes=import_data["attributes"],
        created_by=current_user.id,
    )

    db.add(new_content_type)
    db.commit()
    db.refresh(new_content_type)

    return {
        "message": f"Content type '{new_content_type.name}' imported successfully",
        "content_type_id": new_content_type.id,
        "imported_from": import_data.get("exported_by", "unknown"),
    }


@router.get("/{content_type_id}/instances/export")
async def export_content_instances(
    content_type_id: str,
    include_content_type: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Export all instances of a content type as JSON.

    Optionally includes the content type definition.
    Useful for backing up content or migrating between environments.
    """
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    # Get all instances
    instances = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type_id
    ).all()

    export_data = {
        "exported_at": datetime.utcnow().isoformat(),
        "exported_by": current_user.email,
        "content_type_id": content_type_id,
        "content_type_name": content_type.name,
        "instance_count": len(instances),
        "version": "1.0",
    }

    if include_content_type:
        export_data["content_type"] = {
            "name": content_type.name,
            "description": content_type.description,
            "icon": content_type.icon,
            "attributes": content_type.attributes,
        }

    export_data["instances"] = [
        {
            "data": instance.data,
            "status": instance.status,
            "created_at": instance.created_at.isoformat(),
            "updated_at": instance.updated_at.isoformat(),
        }
        for instance in instances
    ]

    return export_data


@router.post("/{content_type_id}/instances/import")
async def import_content_instances(
    content_type_id: str,
    import_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Import content instances from JSON export.

    Creates new instances from exported data.
    Authors, editors, and knowledge engineers can import.
    """
    if current_user.role not in ["author", "editor", "knowledge_engineer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to import content"
        )

    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.id == content_type_id
    ).first()

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content type not found"
        )

    if "instances" not in import_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Import data must contain 'instances' array"
        )

    instances_data = import_data["instances"]
    imported_count = 0
    errors = []

    for idx, instance_data in enumerate(instances_data):
        try:
            # Validate instance data structure
            if "data" not in instance_data:
                errors.append(f"Instance {idx}: Missing 'data' field")
                continue

            # Validate instance data using advanced validation system
            validation_errors = validate_instance_data(content_type.attributes, instance_data["data"])

            # Check for unknown fields
            attributes = {attr["name"]: attr for attr in content_type.attributes}
            for data_key in instance_data["data"].keys():
                if data_key not in attributes:
                    validation_errors.append(f"Unknown attribute '{data_key}'")

            if validation_errors:
                errors.append(f"Instance {idx}: {'; '.join(validation_errors)}")
                continue

            # Create instance
            new_instance = ContentInstanceModel(
                id=str(uuid.uuid4()),
                content_type_id=content_type_id,
                data=instance_data["data"],
                status=instance_data.get("status", "draft"),
                created_by=current_user.id,
            )

            db.add(new_instance)
            imported_count += 1

        except Exception as e:
            errors.append(f"Instance {idx}: {str(e)}")

    if imported_count > 0:
        db.commit()

    return {
        "message": f"Imported {imported_count} of {len(instances_data)} instances",
        "imported": imported_count,
        "failed": len(errors),
        "errors": errors[:10],  # Return first 10 errors
    }


# ============================================================================
# AGENT-ASSISTED CONTENT GENERATION
# ============================================================================

from fastapi.responses import StreamingResponse
import asyncio

@router.post("/instances/{instance_id}/generate-field")
async def generate_field_with_agent(
    instance_id: str,
    field_name: str = Query(..., description="Name of the field to populate"),
    agent_config_id: str = Query(None, description="Optional: ID of the Agent Configuration to use. If not provided, uses default configuration."),
    stream: bool = Query(True, description="Enable streaming response"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Generate content for a specific field using an AI agent.

    This endpoint:
    1. Loads the agent configuration
    2. Retrieves relevant context from content types and knowledge base (RAG)
    3. Executes Claude Code agent with the context
    4. Returns generated content for user review

    The RAG subsystem provides context to Claude Code's existing skills and agents,
    creating a feedback loop where CMS knowledge informs content generation.

    Args:
        instance_id: ID of the content instance being edited
        field_name: Name of the field to populate
        agent_config_id: ID of the Agent Configuration content instance

    Returns:
        Generated content with metadata for user review
    """
    from services.agent_execution import get_agent_executor

    # 1. Load the content instance
    instance = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.id == instance_id
    ).first()

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content instance not found: {instance_id}"
        )

    # 2. Check user has permission to edit this instance
    if instance.created_by != current_user.id and current_user.role not in ["editor", "knowledge_engineer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this content"
        )

    # 3. Execute the agent
    try:
        agent_executor = get_agent_executor(db)

        # Use streaming if requested
        if stream:
            import asyncio

            async def generate():
                async for chunk in agent_executor.execute_agent_stream(
                    field_name=field_name,
                    current_data=instance.data,
                    content_type_id=instance.content_type_id,
                    agent_config_id=agent_config_id
                ):
                    yield chunk
                    # Force flush to client
                    await asyncio.sleep(0)

            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",  # Disable nginx buffering
                    "Access-Control-Allow-Origin": "*",  # CORS for streaming
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                }
            )

        # Non-streaming fallback
        result = await agent_executor.execute_agent(
            field_name=field_name,
            current_data=instance.data,
            content_type_id=instance.content_type_id,
            agent_config_id=agent_config_id  # Optional: uses default if None
        )

        return {
            "instance_id": instance_id,
            "field_name": field_name,
            "generated_value": result["generated_value"],
            "confidence": result["confidence"],
            "context_metadata": result["context_used"],
            "model": result.get("model"),
            "usage": result.get("usage"),
            "message": "Content generated successfully. Please review before saving."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating field content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )


@router.get("/instances/{instance_id}/available-agents")
async def get_available_agents_for_instance(
    instance_id: str,
    field_name: Optional[str] = Query(None, description="Filter agents by field name"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get list of available agents for a content instance.

    Returns agents that:
    1. Target this content type
    2. Can populate the specified field (if field_name provided)
    3. Have all dependencies met
    4. Are active

    Args:
        instance_id: ID of the content instance
        field_name: Optional field name to filter agents

    Returns:
        List of available agent configurations
    """
    # 1. Load the content instance
    instance = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.id == instance_id
    ).first()

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content instance not found: {instance_id}"
        )

    # 2. Find Agent Configuration content type
    agent_config_ct = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == "Agent Configuration"
    ).first()

    if not agent_config_ct:
        # No agent configurations exist yet
        return []

    # 3. Query for active agent configurations targeting this content type
    all_agents = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == agent_config_ct.id,
        ContentInstanceModel.status == "published"
    ).all()

    # 4. Filter agents
    available_agents = []
    for agent_instance in all_agents:
        agent_data = agent_instance.data

        # Check if agent is active
        if not agent_data.get("active", True):
            continue

        # Check if agent targets this content type
        target_types = agent_data.get("target_content_types", [])
        if instance.content_type_id not in target_types:
            continue

        # Check if agent can populate this field
        if field_name:
            target_fields = agent_data.get("target_fields", [])
            if field_name not in target_fields:
                continue

        available_agents.append({
            "agent_id": agent_instance.id,
            "agent_name": agent_data.get("agent_name"),
            "description": agent_data.get("description"),
            "target_fields": agent_data.get("target_fields", []),
            "trigger_mode": agent_data.get("trigger_mode"),
            "required_inputs": agent_data.get("required_user_inputs", []),
        })

    return available_agents
