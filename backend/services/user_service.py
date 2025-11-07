"""
User service for database operations.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from models.user import User, UserCreate, UserUpdate
from core.security import get_password_hash


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get list of users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        is_active=True,
        is_superuser=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user information."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)

    # Hash password if updating
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


def update_last_login(db: Session, user_id: int) -> bool:
    """Update user's last login timestamp."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    db_user.last_login = datetime.utcnow()
    db.commit()
    return True


def create_initial_superuser(db: Session, email: str, password: str, full_name: str = "Admin") -> User:
    """Create initial superuser if it doesn't exist."""
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return existing_user

    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role="knowledge_engineer",
        is_active=True,
        is_superuser=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
