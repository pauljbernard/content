"""
Knowledge Base API endpoints for browsing and accessing knowledge files.
"""
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from core.config import settings
from core.security import get_current_active_user
from models.user import User

router = APIRouter(prefix="/knowledge")


# Pydantic models


class KnowledgeFile(BaseModel):
    """Knowledge file metadata."""

    path: str
    name: str
    type: str  # "file" or "directory"
    size: Optional[int] = None
    category: str  # "universal", "district", "subject", "program"
    subject: Optional[str] = None
    state: Optional[str] = None
    modified: Optional[str] = None


class KnowledgeFileContent(BaseModel):
    """Knowledge file with content."""

    path: str
    name: str
    content: str
    metadata: Dict[str, Any]


class KnowledgeStats(BaseModel):
    """Knowledge base statistics."""

    total_files: int
    total_directories: int
    files_by_category: Dict[str, int]
    files_by_subject: Dict[str, int]
    files_by_state: Dict[str, int]
    total_size_mb: float


# Helper functions


def get_knowledge_base_root() -> Path:
    """Get knowledge base root directory."""
    root = Path(settings.KNOWLEDGE_BASE_PATH)
    if not root.exists():
        raise HTTPException(status_code=500, detail="Knowledge base path not found")
    return root


def categorize_path(relative_path: str) -> tuple[str, Optional[str], Optional[str]]:
    """
    Categorize a knowledge file path.

    Returns: (category, subject, state)
    """
    parts = relative_path.split("/")

    if parts[0] == "universal":
        return ("universal", None, None)
    elif parts[0] == "districts" and len(parts) >= 2:
        state = parts[1]
        return ("district", None, state)
    elif parts[0] == "subjects" and len(parts) >= 2:
        subject = parts[1]
        if len(parts) >= 4 and parts[2] == "districts":
            state = parts[3]
            return ("subject-district", subject, state)
        else:
            return ("subject-common", subject, None)
    elif parts[0] == "international":
        return ("international", None, None)

    return ("other", None, None)


def scan_directory(root: Path, relative_path: str = "") -> List[KnowledgeFile]:
    """Scan directory and return file/directory list."""
    current_path = root / relative_path if relative_path else root
    items = []

    try:
        for item in current_path.iterdir():
            if item.name.startswith("."):
                continue

            rel_path = str(item.relative_to(root))
            category, subject, state = categorize_path(rel_path)

            if item.is_file() and item.suffix == ".md":
                items.append(
                    KnowledgeFile(
                        path=rel_path,
                        name=item.name,
                        type="file",
                        size=item.stat().st_size,
                        category=category,
                        subject=subject,
                        state=state,
                        modified=str(item.stat().st_mtime),
                    )
                )
            elif item.is_dir():
                items.append(
                    KnowledgeFile(
                        path=rel_path,
                        name=item.name,
                        type="directory",
                        category=category,
                        subject=subject,
                        state=state,
                    )
                )
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")

    return items


# API endpoints


@router.get("/stats", response_model=KnowledgeStats)
async def get_knowledge_stats(current_user: User = Depends(get_current_active_user)):
    """
    Get knowledge base statistics.

    Returns counts of files, directories, and breakdowns by category, subject, and state.
    """
    root = get_knowledge_base_root()
    total_files = 0
    total_directories = 0
    total_size = 0
    by_category = {}
    by_subject = {}
    by_state = {}

    for file_path in root.rglob("*.md"):
        if file_path.name.startswith("."):
            continue

        total_files += 1
        total_size += file_path.stat().st_size

        rel_path = str(file_path.relative_to(root))
        category, subject, state = categorize_path(rel_path)

        by_category[category] = by_category.get(category, 0) + 1
        if subject:
            by_subject[subject] = by_subject.get(subject, 0) + 1
        if state:
            by_state[state] = by_state.get(state, 0) + 1

    for dir_path in root.rglob("*"):
        if dir_path.is_dir() and not dir_path.name.startswith("."):
            total_directories += 1

    return KnowledgeStats(
        total_files=total_files,
        total_directories=total_directories,
        files_by_category=by_category,
        files_by_subject=by_subject,
        files_by_state=by_state,
        total_size_mb=round(total_size / (1024 * 1024), 2),
    )


@router.get("/browse", response_model=List[KnowledgeFile])
async def browse_knowledge_base(
    path: str = Query("", description="Relative path to browse"),
    current_user: User = Depends(get_current_active_user),
):
    """
    Browse knowledge base directory structure.

    - **path**: Relative path from knowledge base root (empty for root)

    Returns list of files and directories at the specified path.
    """
    root = get_knowledge_base_root()

    # Validate path is within knowledge base
    try:
        target_path = (root / path).resolve()
        target_path.relative_to(root.resolve())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid path")

    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Path not found")

    if not target_path.is_dir():
        raise HTTPException(status_code=400, detail="Path is not a directory")

    return scan_directory(root, path)


@router.get("/file", response_model=KnowledgeFileContent)
async def get_knowledge_file(
    path: str = Query(..., description="Relative path to file"),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get knowledge file content.

    - **path**: Relative path to the file from knowledge base root

    Returns file content and metadata.
    """
    root = get_knowledge_base_root()

    # Validate path
    try:
        file_path = (root / path).resolve()
        file_path.relative_to(root.resolve())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid path")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Path is not a file")

    # Read file content
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    # Extract metadata
    category, subject, state = categorize_path(path)
    metadata = {
        "category": category,
        "subject": subject,
        "state": state,
        "size": file_path.stat().st_size,
        "modified": str(file_path.stat().st_mtime),
    }

    return KnowledgeFileContent(
        path=path, name=file_path.name, content=content, metadata=metadata
    )


@router.get("/categories", response_model=List[str])
async def get_categories(current_user: User = Depends(get_current_active_user)):
    """Get list of knowledge base categories."""
    root = get_knowledge_base_root()
    categories = set()

    for item in root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            categories.add(item.name)

    return sorted(list(categories))


@router.get("/subjects", response_model=List[str])
async def get_subjects(current_user: User = Depends(get_current_active_user)):
    """Get list of subjects in knowledge base."""
    root = get_knowledge_base_root()
    subjects_path = root / "subjects"

    if not subjects_path.exists():
        return []

    subjects = []
    for item in subjects_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            subjects.append(item.name)

    return sorted(subjects)


@router.get("/states", response_model=List[str])
async def get_states(current_user: User = Depends(get_current_active_user)):
    """Get list of states/districts in knowledge base."""
    root = get_knowledge_base_root()
    districts_path = root / "districts"

    if not districts_path.exists():
        return []

    states = []
    for item in districts_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            states.append(item.name)

    return sorted(states)
