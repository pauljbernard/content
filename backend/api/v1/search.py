"""
Search API endpoints for knowledge base and content.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from pathlib import Path
from core.config import settings
from core.security import get_current_active_user
from models.user import User

router = APIRouter(prefix="/search")


# Pydantic models


class SearchResult(BaseModel):
    """Search result schema."""

    type: str  # "knowledge_file", "config", "content"
    title: str
    path: str
    excerpt: str
    score: float
    metadata: dict


# API endpoints


@router.get("/", response_model=List[SearchResult])
async def search(
    q: str = Query(..., min_length=2, description="Search query"),
    type: Optional[str] = Query(None, description="Filter by type"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    state: Optional[str] = Query(None, description="Filter by state"),
    limit: int = Query(20, le=100, description="Max results"),
    current_user: User = Depends(get_current_active_user),
):
    """
    Search across knowledge base, curriculum configs, and content.

    - **q**: Search query (minimum 2 characters)
    - **type**: Filter results by type (knowledge_file, config, content)
    - **subject**: Filter by subject
    - **state**: Filter by state/district
    - **limit**: Maximum number of results

    Returns ranked search results with excerpts and metadata.
    """
    # Simple file-based search implementation
    # For production, integrate with Whoosh or Elasticsearch
    results = []
    kb_root = Path(settings.KNOWLEDGE_BASE_PATH)

    if type is None or type == "knowledge_file":
        # Search knowledge base files
        for md_file in kb_root.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8").lower()
                if q.lower() in content:
                    # Extract excerpt around match
                    idx = content.find(q.lower())
                    start = max(0, idx - 50)
                    end = min(len(content), idx + len(q) + 50)
                    excerpt = content[start:end].replace("\n", " ")

                    results.append(
                        SearchResult(
                            type="knowledge_file",
                            title=md_file.name,
                            path=str(md_file.relative_to(kb_root)),
                            excerpt=f"...{excerpt}...",
                            score=1.0,  # Simplified scoring
                            metadata={"size": md_file.stat().st_size},
                        )
                    )

                    if len(results) >= limit:
                        break
            except Exception:
                continue

    return results[:limit]


@router.get("/suggest", response_model=List[str])
async def search_suggestions(
    q: str = Query(..., min_length=2, description="Query prefix"),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get search suggestions based on query prefix.

    Returns list of suggested search terms.
    """
    # Simple suggestion implementation
    # In production, use dedicated suggestion index
    suggestions = [
        "mathematics",
        "ela",
        "science",
        "social studies",
        "texas",
        "california",
        "florida",
        "lesson plan",
        "assessment",
        "rubric",
    ]

    return [s for s in suggestions if q.lower() in s.lower()][:10]
