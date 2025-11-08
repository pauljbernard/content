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
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database.session import get_db
from core.security import get_current_active_user, get_author
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

router = APIRouter(prefix="/standards")


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
    if isinstance(standard.structure, str):
        standard.structure = json.loads(standard.structure) if standard.structure else {}
    if isinstance(standard.standards_list, str):
        standard.standards_list = json.loads(standard.standards_list) if standard.standards_list else []

    return standard


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

    The import job will be processed asynchronously by the standards-importer agent.
    """
    # Check for duplicate code
    existing = db.query(Standard).filter(Standard.code == job.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A standard with code '{job.code}' already exists"
        )

    # Create import job
    job_dict = job.dict()
    job_dict["status"] = "queued"

    db_job = StandardImportJob(**job_dict)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # TODO: Trigger standards-importer agent to process this job
    # This would be done via the agent system, similar to how content generation works

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
