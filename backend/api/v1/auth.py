"""
Authentication API endpoints.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.config import settings
from core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
    get_current_user,
)
from database.session import get_db
from models.user import Token, UserCreate, UserInDB, User as UserModel
from services import user_service
from services.audit_service import audit_service

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - **email**: Valid email address
    - **password**: Strong password (min 8 characters)
    - **full_name**: User's full name
    - **role**: User role (teacher, author, editor, knowledge_engineer)
    """
    # Check if user already exists
    existing_user = user_service.get_user_by_email(db, user.email)
    if existing_user:
        # Log failed registration attempt
        audit_service.log_event(
            db=db,
            who=user.email,
            action="register",
            resource="authentication",
            decision="deny",
            reason="Email already registered"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create user
    db_user = user_service.create_user(db, user)

    # Log successful registration
    audit_service.log_event(
        db=db,
        who=f"user-{db_user.id}",
        action="register",
        resource="authentication",
        decision="allow",
        reason="User registration successful",
        created_by_id=db_user.id
    )

    return db_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login with email and password to get access token.

    Returns:
    - access_token: JWT token for API authentication
    - refresh_token: Token to refresh access token
    - token_type: "bearer"
    """
    # Authenticate user
    user = user_service.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Log failed login attempt
        audit_service.log_event(
            db=db,
            who=form_data.username,
            action="login",
            resource="authentication",
            decision="deny",
            reason="Incorrect email or password"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Update last login
    user_service.update_last_login(db, user.id)

    # Log successful login
    audit_service.log_login(db, user, success=True)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.

    - **refresh_token**: Valid refresh token
    """
    # Verify refresh token
    payload = verify_token(refresh_token, "refresh")
    if not payload:
        # Log failed token refresh
        audit_service.log_event(
            db=db,
            who="unknown",
            action="token_refresh",
            resource="authentication",
            decision="deny",
            reason="Invalid refresh token"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")
    if not user_id:
        # Log failed token refresh
        audit_service.log_event(
            db=db,
            who="unknown",
            action="token_refresh",
            resource="authentication",
            decision="deny",
            reason="Invalid token payload"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # Get user
    user = user_service.get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        # Log failed token refresh
        audit_service.log_event(
            db=db,
            who=f"user-{user_id}",
            action="token_refresh",
            resource="authentication",
            decision="deny",
            reason="User not found or inactive"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Create new tokens
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Log successful token refresh
    audit_service.log_event(
        db=db,
        who=f"user-{user.id}",
        action="token_refresh",
        resource="authentication",
        decision="allow",
        reason="Token refreshed successfully",
        created_by_id=user.id
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout user (client should discard tokens).

    Note: JWT tokens cannot be invalidated on the server side.
    The client must discard the tokens to complete logout.
    """
    # Log logout event
    audit_service.log_logout(db, current_user)

    return {"message": "Successfully logged out. Please discard your tokens."}
