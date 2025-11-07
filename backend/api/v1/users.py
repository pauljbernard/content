"""
User management API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from core.security import get_current_active_user, get_current_superuser
from models.user import User, UserCreate, UserUpdate, UserInDB, UserPublic
from services import user_service

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserInDB)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user's information."""
    return current_user


@router.put("/me", response_model=UserInDB)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update current user's information."""
    updated_user = user_service.update_user(db, current_user.id, user_update)
    return updated_user


@router.get("/", response_model=List[UserPublic])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """List all users (superuser only)."""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserInDB)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """Get user by ID (superuser only)."""
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """Update user by ID (superuser only)."""
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = user_service.update_user(db, user_id, user_update)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """Delete user by ID (superuser only)."""
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_service.delete_user(db, user_id)
    return None
