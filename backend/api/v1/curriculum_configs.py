"""
Curriculum configuration API endpoints.
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from core.config import settings
from core.security import get_current_active_user, get_knowledge_engineer
from models.user import User

router = APIRouter(prefix="/curriculum-configs")


# Pydantic models


class CurriculumConfig(BaseModel):
    """Curriculum configuration schema."""

    id: str
    name: str
    grades: List[str]
    subject: str
    district: Optional[str] = None
    course: Optional[str] = None
    knowledge_resolution: Dict[str, List[str]]
    standards: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class CurriculumConfigCreate(BaseModel):
    """Schema for creating curriculum config."""

    id: str
    name: str
    grades: List[str]
    subject: str
    district: Optional[str] = None
    course: Optional[str] = None
    knowledge_resolution: Dict[str, List[str]]
    standards: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = {}


# Helper functions


def get_config_path() -> Path:
    """Get curriculum config directory path."""
    path = Path(settings.CURRICULUM_CONFIG_PATH)
    if not path.exists():
        raise HTTPException(status_code=500, detail="Config path not found")
    return path


def load_config(config_id: str) -> Dict[str, Any]:
    """Load curriculum config by ID."""
    config_file = get_config_path() / f"{config_id}.json"

    if not config_file.exists():
        raise HTTPException(status_code=404, detail="Config not found")

    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid config file format")


def save_config(config_id: str, config_data: Dict[str, Any]):
    """Save curriculum config."""
    config_file = get_config_path() / f"{config_id}.json"

    try:
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving config: {str(e)}"
        )


# API endpoints


@router.get("/", response_model=List[CurriculumConfig])
async def list_curriculum_configs(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    district: Optional[str] = Query(None, description="Filter by district/state"),
    current_user: User = Depends(get_current_active_user),
):
    """
    List all curriculum configurations.

    Optional filters:
    - **subject**: Filter by subject (mathematics, ela, science, etc.)
    - **district**: Filter by district/state
    """
    config_path = get_config_path()
    configs = []

    for config_file in config_path.glob("*.json"):
        try:
            with open(config_file, "r") as f:
                config_data = json.load(f)

            # Apply filters
            if subject and config_data.get("subject") != subject:
                continue
            if district and config_data.get("district") != district:
                continue

            configs.append(CurriculumConfig(**config_data))
        except (json.JSONDecodeError, KeyError):
            # Skip invalid config files
            continue

    return configs


@router.get("/{config_id}", response_model=CurriculumConfig)
async def get_curriculum_config(
    config_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Get curriculum configuration by ID.

    - **config_id**: Configuration ID (e.g., "hmh-math-tx", "hmh-algebra1-tx")
    """
    config_data = load_config(config_id)
    return CurriculumConfig(**config_data)


@router.post("/", response_model=CurriculumConfig, status_code=201)
async def create_curriculum_config(
    config: CurriculumConfigCreate,
    current_user: User = Depends(get_knowledge_engineer),
):
    """
    Create new curriculum configuration (knowledge engineers only).

    Required fields:
    - **id**: Unique config ID
    - **name**: Display name
    - **grades**: List of grade levels
    - **subject**: Subject area
    - **knowledge_resolution**: Resolution order paths
    """
    # Check if config already exists
    config_file = get_config_path() / f"{config.id}.json"
    if config_file.exists():
        raise HTTPException(status_code=400, detail="Config ID already exists")

    # Save config
    config_dict = config.dict()
    save_config(config.id, config_dict)

    return CurriculumConfig(**config_dict)


@router.put("/{config_id}", response_model=CurriculumConfig)
async def update_curriculum_config(
    config_id: str,
    config: CurriculumConfigCreate,
    current_user: User = Depends(get_knowledge_engineer),
):
    """Update curriculum configuration (knowledge engineers only)."""
    # Verify config exists
    load_config(config_id)

    # Save updated config
    config_dict = config.dict()
    save_config(config_id, config_dict)

    return CurriculumConfig(**config_dict)


@router.delete("/{config_id}", status_code=204)
async def delete_curriculum_config(
    config_id: str, current_user: User = Depends(get_knowledge_engineer)
):
    """Delete curriculum configuration (knowledge engineers only)."""
    config_file = get_config_path() / f"{config_id}.json"

    if not config_file.exists():
        raise HTTPException(status_code=404, detail="Config not found")

    try:
        config_file.unlink()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting config: {str(e)}"
        )

    return None


@router.get("/{config_id}/resolve", response_model=Dict[str, Any])
async def resolve_knowledge_for_config(
    config_id: str,
    topic: Optional[str] = Query(None, description="Specific topic to resolve"),
    current_user: User = Depends(get_current_active_user),
):
    """
    Resolve knowledge files for a curriculum configuration.

    Returns the list of knowledge files that apply to this configuration
    based on the resolution order.
    """
    config_data = load_config(config_id)
    resolution_order = config_data.get("knowledge_resolution", {}).get("order", [])

    # This would integrate with the knowledge base to actually resolve files
    # For now, return the resolution order
    return {
        "config_id": config_id,
        "resolution_order": resolution_order,
        "message": "Knowledge resolution order (actual file resolution to be implemented)",
    }
