"""
Standards management API endpoints.

Provides CRUD operations for educational standards including:
- List all imported standards
- Get standard details with full hierarchical structure
- Import new standards from CASE, PDF, XML, etc.
- Update existing standards
- Delete/archive standards
- Search within standards
"""
import json
import logging
from typing import List, Optional, Generic, TypeVar
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.session import get_db
from core.security import get_current_active_user, get_author, get_editor
from models.user import User
from models.standard import (
    Standard,
    StandardCreate,
    StandardUpdate,
    StandardInDB,
    StandardPublic,
    StandardStatus,
    StandardType,
    StandardSubject,
    StandardImportJob,
    StandardImportJobCreate,
    StandardImportJobInDB,
)
from models.content_type import ContentTypeModel, ContentInstanceModel

router = APIRouter(prefix="/standards")
logger = logging.getLogger(__name__)

# Generic pagination response model
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: List[T]
    total: int
    limit: int
    offset: int
    has_more: bool


@router.get("/", response_model=List[StandardPublic])
async def list_standards(
    skip: int = 0,
    limit: int = 50,
    type: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List all imported standards with optional filters and pagination.

    Returns:
    - List of standard summaries with metadata

    Filters:
    - **type**: Filter by standard type (state, national, international, district)
    - **subject**: Filter by subject area
    - **state**: Filter by state (for state standards)
    - **status**: Filter by status (draft, imported, published, archived)
    - **search**: Search in name, short_name, description

    All authenticated users can view published standards.
    Authors and above can see draft/imported standards.
    """
    query = db.query(Standard)

    # Role-based filtering
    if current_user.role in ["teacher"]:
        query = query.filter(Standard.status == StandardStatus.PUBLISHED)

    # Apply filters
    if type and type.strip():
        try:
            type_enum = StandardType(type)
            query = query.filter(Standard.type == type_enum)
        except ValueError:
            pass

    if subject and subject.strip():
        try:
            subject_enum = StandardSubject(subject)
            query = query.filter(Standard.subject == subject_enum)
        except ValueError:
            pass

    if state and state.strip():
        query = query.filter(Standard.state == state)

    if status and status.strip():
        try:
            status_enum = StandardStatus(status)
            query = query.filter(Standard.status == status_enum)
        except ValueError:
            pass

    if search and search.strip():
        search_pattern = f"%{search}%"
        query = query.filter(
            (Standard.name.ilike(search_pattern))
            | (Standard.short_name.ilike(search_pattern))
            | (Standard.description.ilike(search_pattern))
            | (Standard.code.ilike(search_pattern))
        )

    # Order by most recent first
    query = query.order_by(Standard.updated_at.desc())

    # Apply pagination
    total = query.count()
    standards_list = query.offset(skip).limit(limit).all()

    # Deserialize JSON fields
    for standard in standards_list:
        if isinstance(standard.grade_levels, str):
            standard.grade_levels = json.loads(standard.grade_levels) if standard.grade_levels else []
        elif standard.grade_levels is None:
            standard.grade_levels = []

    return standards_list


@router.get("/{standard_id}", response_model=StandardInDB)
async def get_standard(
    standard_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get full standard details including hierarchical structure.

    Returns complete standard with:
    - Full hierarchical structure (domains, strands, standards)
    - Flat list of all individual standards for easy reference
    - Metadata and source information
    """
    standard = db.query(Standard).filter(Standard.id == standard_id).first()

    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found"
        )

    # Role-based access: teachers can only view published
    if current_user.role == "teacher" and standard.status != StandardStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this standard"
        )

    # Deserialize JSON fields
    if isinstance(standard.grade_levels, str):
        standard.grade_levels = json.loads(standard.grade_levels) if standard.grade_levels else []
    elif standard.grade_levels is None:
        standard.grade_levels = []

    if isinstance(standard.structure, str):
        standard.structure = json.loads(standard.structure) if standard.structure else {}
    elif standard.structure is None:
        standard.structure = {}

    if isinstance(standard.standards_list, str):
        standard.standards_list = json.loads(standard.standards_list) if standard.standards_list else []
    elif standard.standards_list is None:
        standard.standards_list = []

    return standard


@router.delete("/{standard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_standard(
    standard_id: int,
    current_user: User = Depends(get_editor),  # Only editors and knowledge_engineers can delete
    db: Session = Depends(get_db),
):
    """
    Delete a standard and all associated data.

    This will:
    - Delete the standard record
    - Delete associated import jobs
    - Delete any alignments to this standard

    Only editors and knowledge engineers can delete standards.
    """
    standard = db.query(Standard).filter(Standard.id == standard_id).first()

    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found"
        )

    # Delete associated import jobs
    db.query(StandardImportJob).filter(StandardImportJob.standard_id == standard_id).delete()

    # Delete the standard
    db.delete(standard)
    db.commit()

    return None


@router.post("/", response_model=StandardInDB, status_code=status.HTTP_201_CREATED)
async def create_standard(
    standard: StandardCreate,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """
    Create a new standard (manual import).

    This is typically used for manually entering standards or
    when an import job has completed and is ready to be saved.

    Required fields:
    - **name**: Full standard name
    - **short_name**: Abbreviated name
    - **code**: Unique identifier code
    - **type**: Standard type (state, national, international)
    - **subject**: Subject area
    - **source_organization**: Issuing organization
    - **structure**: Hierarchical structure (domains, strands, etc.)
    - **standards_list**: Flat list of all individual standards
    """
    # Check for duplicate code
    existing = db.query(Standard).filter(Standard.code == standard.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A standard with code '{standard.code}' already exists"
        )

    # Convert standard to dict and serialize fields
    standard_dict = standard.dict()

    # Serialize JSON fields
    if standard_dict.get("grade_levels"):
        standard_dict["grade_levels"] = json.dumps(standard_dict["grade_levels"])
    else:
        standard_dict["grade_levels"] = json.dumps([])

    if standard_dict.get("structure"):
        standard_dict["structure"] = json.dumps(standard_dict["structure"])
    else:
        standard_dict["structure"] = json.dumps({})

    if standard_dict.get("standards_list"):
        standard_dict["standards_list"] = json.dumps(standard_dict["standards_list"])
        # Count total standards
        standard_dict["total_standards_count"] = len(standard_dict["standards_list"])
    else:
        standard_dict["standards_list"] = json.dumps([])
        standard_dict["total_standards_count"] = 0

    # Add metadata
    standard_dict["imported_by_id"] = current_user.id
    standard_dict["status"] = StandardStatus.DRAFT

    # Create standard
    db_standard = Standard(**standard_dict)
    db.add(db_standard)
    db.commit()
    db.refresh(db_standard)

    # Deserialize for response
    if isinstance(db_standard.grade_levels, str):
        db_standard.grade_levels = json.loads(db_standard.grade_levels)
    if isinstance(db_standard.structure, str):
        db_standard.structure = json.loads(db_standard.structure)
    if isinstance(db_standard.standards_list, str):
        db_standard.standards_list = json.loads(db_standard.standards_list)

    return db_standard


@router.patch("/{standard_id}", response_model=StandardInDB)
async def update_standard(
    standard_id: int,
    standard_update: StandardUpdate,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """
    Update an existing standard.

    Authors and above can update standards.
    Only knowledge engineers can publish standards.
    """
    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()

    if not db_standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found"
        )

    # Only knowledge engineers can publish
    if standard_update.status == StandardStatus.PUBLISHED and current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only knowledge engineers can publish standards"
        )

    # Update fields
    update_data = standard_update.dict(exclude_unset=True)

    # Serialize JSON fields if present
    if "structure" in update_data and update_data["structure"] is not None:
        update_data["structure"] = json.dumps(update_data["structure"])

    if "standards_list" in update_data and update_data["standards_list"] is not None:
        standards_list = update_data["standards_list"]
        update_data["standards_list"] = json.dumps(standards_list)
        update_data["total_standards_count"] = len(standards_list)

    for field, value in update_data.items():
        setattr(db_standard, field, value)

    db.commit()
    db.refresh(db_standard)

    # Deserialize for response
    if isinstance(db_standard.grade_levels, str):
        db_standard.grade_levels = json.loads(db_standard.grade_levels)
    if isinstance(db_standard.structure, str):
        db_standard.structure = json.loads(db_standard.structure)
    if isinstance(db_standard.standards_list, str):
        db_standard.standards_list = json.loads(db_standard.standards_list)

    return db_standard


@router.delete("/{standard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_standard(
    standard_id: int,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """
    Delete a standard (knowledge engineers only).

    This is a hard delete. Consider archiving instead by updating status to 'archived'.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only knowledge engineers can delete standards"
        )

    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()

    if not db_standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found"
        )

    db.delete(db_standard)
    db.commit()

    return None


@router.get("/{standard_id}/search")
async def search_within_standard(
    standard_id: int,
    query: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Search for specific standards within a standard set.

    Searches across:
    - Standard codes
    - Standard text/descriptions
    - Domain names
    - Strand names

    Returns matching standards from the flat standards_list.
    """
    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()

    if not db_standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found"
        )

    # Deserialize standards_list
    if isinstance(db_standard.standards_list, str):
        standards_list = json.loads(db_standard.standards_list) if db_standard.standards_list else []
    else:
        standards_list = db_standard.standards_list

    # Search in standards
    query_lower = query.lower()
    matching_standards = []

    for std in standards_list:
        # Check if query matches code, text, domain, or strand
        if (
            query_lower in std.get("code", "").lower()
            or query_lower in std.get("text", "").lower()
            or query_lower in std.get("domain", "").lower()
            or query_lower in std.get("strand", "").lower()
        ):
            matching_standards.append(std)

    return {
        "standard_id": standard_id,
        "standard_name": db_standard.name,
        "query": query,
        "matches": matching_standards,
        "total_matches": len(matching_standards)
    }


# Import job endpoints

@router.post("/import", response_model=StandardImportJobInDB, status_code=status.HTTP_201_CREATED)
async def create_import_job(
    job: StandardImportJobCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """
    Create a new standard import job.

    Supported formats:
    - **case**: IMS Global CASE format (JSON/API)
    - **pdf**: PDF documents (requires parsing)
    - **html**: HTML documents
    - **xml**: XML documents
    - **json**: Custom JSON format
    - **csv**: CSV spreadsheets
    - **manual**: Manual entry (no automatic parsing)

    The import job will be processed asynchronously by the standards-importer service.
    """
    # Create import job (store full metadata in import_log for later processing)
    import json
    job_data = job.dict()
    job_data["user_id"] = current_user.id  # Store user ID for later use

    db_job = StandardImportJob(
        source_type=job.source_type,
        source_location=job.source_location,
        format=job.format,
        status="queued",
        import_log=json.dumps(job_data)  # Store all metadata for processing
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # Trigger standards import processing in background
    background_tasks.add_task(process_standards_import_job, db_job.id)

    # Parse import_log back to dict for response validation
    if db_job.import_log:
        db_job.import_log = json.loads(db_job.import_log)

    return db_job


@router.get("/import/{job_id}", response_model=StandardImportJobInDB)
async def get_import_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get the status of a standard import job.

    Use this to poll for completion status and progress updates.
    """
    job = db.query(StandardImportJob).filter(StandardImportJob.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import job not found"
        )

    # Deserialize import_log if present
    if isinstance(job.import_log, str):
        job.import_log = json.loads(job.import_log) if job.import_log else {}

    return job


@router.get("/import", response_model=List[StandardImportJobInDB])
async def list_import_jobs(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List all standard import jobs.

    Filters:
    - **status**: Filter by job status (queued, running, completed, failed)
    """
    query = db.query(StandardImportJob)

    if status and status.strip():
        query = query.filter(StandardImportJob.status == status)

    query = query.order_by(StandardImportJob.created_at.desc())

    total = query.count()
    jobs = query.offset(skip).limit(limit).all()

    # Deserialize import_log for all jobs
    for job in jobs:
        if isinstance(job.import_log, str):
            job.import_log = json.loads(job.import_log) if job.import_log else {}

    return jobs


@router.get("/case-network/frameworks")
async def get_case_network_frameworks(
    limit: int = Query(100, ge=1, le=500, description="Maximum number of frameworks to return"),
    offset: int = Query(0, ge=0, description="Number of frameworks to skip"),
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db),
):
    """
    Get list of available CASE frameworks from CASE Network with pagination.

    Requires CASE Network credentials to be configured in Secrets.

    Pagination:
    - **limit**: Maximum number of frameworks to return (1-500, default 100)
    - **offset**: Number of frameworks to skip (default 0)

    Returns:
        {
            "success": true,
            "frameworks": [...],
            "total": total_count,
            "limit": requested_limit,
            "offset": requested_offset,
            "has_more": boolean
        }
    """
    from services.standards_importer import get_standards_import_service
    from services.secrets_helper import get_secrets_helper

    # Get CASE Network credentials
    secrets_helper = get_secrets_helper(db)
    credentials = secrets_helper.get_case_network_credentials()

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "CASE Network credentials not found. "
                "Please add 'case_network_key' secret with client ID and secret."
            )
        )

    # Get frameworks list
    try:
        import_service = get_standards_import_service()
        case_parser = import_service.parsers.get("case")

        frameworks = await case_parser.get_available_frameworks(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            limit=limit,
            offset=offset
        )

        # Note: CASE Network API may not provide total count, so we estimate
        # has_more based on whether we received the full limit
        has_more = len(frameworks) >= limit

        return {
            "success": True,
            "frameworks": frameworks,
            "total": len(frameworks) + offset,  # Estimated total (at least this many)
            "limit": limit,
            "offset": offset,
            "has_more": has_more
        }

    except Exception as e:
        logger.exception("Error fetching CASE Network frameworks")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch CASE Network frameworks: {str(e)}"
        )


# Background task execution
async def process_standards_import_job(job_id: int):
    """
    Process standards import job in background.

    This function:
    1. Invokes the StandardsImportService
    2. Parses the source format (CASE, PDF, etc.)
    3. Creates the Standard database record
    4. Updates job status and progress
    5. Handles errors and timeouts
    """
    from database.session import SessionLocal
    from services.standards_importer import get_standards_import_service

    db = SessionLocal()

    try:
        job = db.query(StandardImportJob).filter(StandardImportJob.id == job_id).first()
        if not job:
            return

        # Update status to running
        job.status = "running"
        job.started_at = datetime.utcnow()
        job.progress_percentage = 10
        job.progress_message = "Initializing import..."
        db.commit()

        # Get import service
        import_service = get_standards_import_service()

        job.progress_percentage = 30
        job.progress_message = f"Parsing {job.format.upper()} format..."
        db.commit()

        # Process the import - get metadata from import_log
        import_log_data = json.loads(job.import_log) if isinstance(job.import_log, str) else job.import_log or {}

        metadata = {
            "name": import_log_data.get("name", "Unknown Standard"),
            "short_name": import_log_data.get("short_name", ""),
            "code": import_log_data.get("code", ""),
            "description": import_log_data.get("description", ""),
            "type": import_log_data.get("type", "national"),
            "subject": import_log_data.get("subject", "general"),
            "source_organization": import_log_data.get("source_organization", ""),
            "version": import_log_data.get("version"),
            "year": import_log_data.get("year"),
            "state": import_log_data.get("state"),
            "district": import_log_data.get("district"),
            "country": import_log_data.get("country"),
            "grade_levels": import_log_data.get("grade_levels"),
        }

        result = await import_service.process_import_job(
            job_id=job_id,
            source_type=job.source_type,
            source_location=job.source_location,
            format=job.format,
            metadata=metadata,
            db_session=db  # Pass database session for secrets retrieval
        )

        job.progress_percentage = 70
        job.progress_message = "Saving standard to database..."
        db.commit()

        # Check if processing was successful
        if result["success"]:
            # Get the raw CASE data for creating individual standard instances
            # The parser returns simplified data, but we need to re-fetch the full CFItems
            import aiohttp

            # Get the CASE Standard content type
            case_standard_type = db.query(ContentTypeModel).filter(
                ContentTypeModel.name == "CASE Standard"
            ).first()

            if not case_standard_type:
                job.status = "failed"
                job.completed_at = datetime.utcnow()
                job.error_message = "CASE Standard content type not found in database"
                job.import_log = json.dumps({
                    "success": False,
                    "error": "missing_content_type",
                    "message": job.error_message
                })
                db.commit()
                return

            # Re-fetch the CASE data to get full CFItems
            # (The parser simplified it too much - we need all fields for each standard)
            from services.standards_importer import get_standards_import_service
            import_svc = get_standards_import_service()
            case_parser = import_svc.parsers.get("case")

            # Fetch with OAuth if needed
            use_oauth = job.source_type == "case_network"
            client_id = None
            client_secret = None

            if use_oauth:
                from services.secrets_helper import get_secrets_helper
                secrets_helper = get_secrets_helper(db)
                credentials = secrets_helper.get_case_network_credentials()
                if credentials:
                    client_id = credentials["client_id"]
                    client_secret = credentials["client_secret"]

            # Fetch raw CASE data
            headers = {}
            if use_oauth and client_id:
                access_token = await case_parser._get_oauth2_token(client_id, client_secret)
                headers["Authorization"] = f"Bearer {access_token}"

            async with aiohttp.ClientSession() as session:
                async with session.get(job.source_location, headers=headers) as response:
                    if response.status == 200:
                        case_data = await response.json()
                    else:
                        raise ValueError(f"Failed to re-fetch CASE data: HTTP {response.status}")

            cf_document = case_data.get("CFDocument", {})
            cf_items = case_data.get("CFItems", [])
            cf_associations = case_data.get("CFAssociations", [])

            # Framework-level metadata to include in each instance
            framework_title = cf_document.get("title", "")
            framework_uri = cf_document.get("uri", "")

            # Build parent-child relationships from associations
            # Map of child_identifier -> parent_identifier
            parent_map = {}
            # Map of parent_identifier -> [child_identifiers]
            children_map = {}

            for assoc in cf_associations:
                if assoc.get("associationType") == "isChildOf":
                    # originNodeURI is the child, destinationNodeURI is the parent
                    child_uri = assoc.get("originNodeURI", {})
                    parent_uri = assoc.get("destinationNodeURI", {})

                    # Extract identifiers from URIs
                    child_id = child_uri.get("identifier") if isinstance(child_uri, dict) else None
                    parent_id = parent_uri.get("identifier") if isinstance(parent_uri, dict) else None

                    if child_id and parent_id:
                        parent_map[child_id] = parent_id

                        if parent_id not in children_map:
                            children_map[parent_id] = []
                        children_map[parent_id].append(child_id)

            # Create one content instance per CFItem
            created_count = 0
            skipped_count = 0

            for cf_item in cf_items:
                # Extract identifier for duplicate check
                identifier = cf_item.get("identifier", "")
                if not identifier:
                    continue

                # Check if this CFItem already exists
                from sqlalchemy import cast, String, or_
                existing = db.query(ContentInstanceModel).filter(
                    ContentInstanceModel.content_type_id == case_standard_type.id,
                    or_(
                        cast(ContentInstanceModel.data, String).like(f'%"identifier": "{identifier}"%'),
                        cast(ContentInstanceModel.data, String).like(f'%"uri": "{cf_item.get("uri", "")}"%')
                    )
                ).first()

                if existing:
                    skipped_count += 1
                    continue

                # Get parent and children from association maps
                item_parent = parent_map.get(identifier)  # None if root node
                item_children = children_map.get(identifier, [])  # Empty list if leaf node

                # Build content instance data from full CFItem
                # Store the complete CFItem data plus framework context
                instance_data = {
                    "identifier": cf_item.get("identifier", ""),
                    "uri": cf_item.get("uri", ""),
                    "human_coding_scheme": cf_item.get("humanCodingScheme", ""),
                    "list_enumeration": cf_item.get("listEnumeration"),
                    "full_statement": cf_item.get("fullStatement", ""),
                    "abbreviated_statement": cf_item.get("abbreviatedStatement"),
                    "concept_keywords": cf_item.get("conceptKeywords", []),
                    "notes": cf_item.get("notes"),
                    "language": cf_item.get("language", "en"),
                    "parent": item_parent,  # Parent identifier from associations
                    "children": item_children,  # List of child identifiers from associations
                    "related_items": [],
                    "prerequisite_items": [],
                    "cf_item_type": cf_item.get("CFItemType", "Standard"),
                    "education_level": cf_item.get("educationLevel", []),
                    "cf_item_type_uri": cf_item.get("CFItemTypeURI", {}).get("uri") if isinstance(cf_item.get("CFItemTypeURI"), dict) else cf_item.get("CFItemTypeURI"),
                    "license_uri": cf_item.get("licenseURI", {}).get("uri") if isinstance(cf_item.get("licenseURI"), dict) else cf_item.get("licenseURI"),
                    "status_start_date": cf_item.get("statusStartDate"),
                    "status_end_date": cf_item.get("statusEndDate"),
                    "last_change_date_time": cf_item.get("lastChangeDateTime"),
                    "cf_document_uri": framework_uri,
                    "framework_title": framework_title,
                    "subject": cf_item.get("subjectURI", []),
                    "alternative_label": cf_item.get("alternativeLabel"),
                    "statement_notation": cf_item.get("statementNotation"),
                    "statement_label": cf_item.get("statementLabel"),
                    "alignment_type": None,  # For future use
                    "case_json": cf_item  # Store raw CASE data
                }

                # Create content instance
                db_instance = ContentInstanceModel(
                    content_type_id=case_standard_type.id,
                    data=instance_data,
                    status="published",  # Auto-publish imported standards
                    created_by=import_log_data.get("user_id")
                )
                db.add(db_instance)
                created_count += 1

            # Commit all instances at once
            db.commit()

            # Update job as completed
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.progress_percentage = 100
            job.progress_message = f"Import complete: {created_count} created, {skipped_count} skipped"
            job.standard_id = None  # No longer using standards table
            job.standards_extracted = created_count
            job.import_log = json.dumps({
                "success": True,
                "created_count": created_count,
                "skipped_count": skipped_count,
                "total_cf_items": len(cf_items)
            })
        else:
            # Import failed
            job.status = "failed"
            job.completed_at = datetime.utcnow()
            job.error_message = result["error_message"]
            job.import_log = json.dumps({
                "success": False,
                "error": result["error_message"]
            })

        db.commit()

    except Exception as e:
        # Rollback any pending transaction before updating job status
        db.rollback()

        try:
            # Refresh job object to get latest state
            db.refresh(job)

            job.status = "failed"
            job.completed_at = datetime.utcnow()
            job.error_message = str(e)
            job.import_log = json.dumps({
                "success": False,
                "error": str(e),
                "traceback": str(e)
            })
            db.commit()
        except Exception as update_error:
            logger.error(f"Failed to update job status after error: {update_error}")
            db.rollback()
    finally:
        db.close()
