"""
Security utilities for authentication and authorization.

Supports both legacy User model and new content type system (UserAccount/UserProfile).
"""
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import base64
import logging

from core.config import settings
from database.session import get_db
from models.user import User
from services.content_instance_service import content_instance_service

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret encryption
# Use SECRET_KEY from settings to derive Fernet key
def _get_fernet_key() -> bytes:
    """Derive a Fernet key from the SECRET_KEY."""
    # Fernet requires exactly 32 url-safe base64-encoded bytes
    # Hash the SECRET_KEY to get consistent 32 bytes
    import hashlib
    key_hash = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key_hash)

_fernet = Fernet(_get_fernet_key())

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user.

    Supports both legacy User model and new content type system.
    Enriches User object with tenant_id, user_id_str, and role from content types.
    """
    # Import here to avoid circular dependency
    from services import user_service

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token, "access")
    if payload is None:
        raise credentials_exception

    # Get user_id from JWT (supports both int and string)
    user_id_from_token: str = payload.get("sub")
    if user_id_from_token is None:
        raise credentials_exception

    # Try to parse as integer for legacy support
    try:
        legacy_user_id = int(user_id_from_token)
        user = user_service.get_user_by_id(db, legacy_user_id)
    except ValueError:
        # Not an integer, must be new user_id format (e.g., "user-1")
        # Extract the numeric part for backward compatibility
        if user_id_from_token.startswith("user-"):
            legacy_user_id = int(user_id_from_token.split("-")[1])
            user = user_service.get_user_by_id(db, legacy_user_id)
        else:
            raise credentials_exception

    if user is None or not user.is_active:
        raise credentials_exception

    # Enrich user with content type data
    # Get UserAccount and UserProfile
    user_id_str = f"user-{user.id}"  # Standard format

    user_account = content_instance_service.get_user_account_by_user_id(db, user_id_str)
    user_profile = content_instance_service.get_user_profile_by_user_id(db, user_id_str)

    # Add enriched data to user object (as dynamic attributes)
    if user_account:
        user.tenant_id = user_account.data.get("tenant_id")
        user.primary_org_id = user_account.data.get("primary_org_id")
        user.account_status = user_account.data.get("status")
    else:
        user.tenant_id = None
        user.primary_org_id = None
        user.account_status = None

    if user_profile:
        # Add UserProfile role as separate attribute (don't override user.role)
        content_role = user_profile.data.get("role")
        user.content_role = content_role if content_role else user.role

        # Add superuser flag from profile
        attrs = user_profile.data.get("attrs", {})
        if attrs.get("is_superuser"):
            user.is_superuser = True

        user.profile_data = user_profile.data
    else:
        user.content_role = user.role  # Use legacy role if no profile
        user.profile_data = None

    # Add user_id string for content type system
    user.user_id_str = user_id_str

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(*allowed_roles: str):
    """
    Dependency to require specific roles.

    Supports both legacy role names and new content type roles.
    Legacy roles: author, editor, knowledge_engineer, teacher
    New roles: content_author, admin, teacher, student, parent

    Role mapping:
    - author → content_author
    - editor → content_author
    - knowledge_engineer → admin
    """

    # Role mapping from legacy to new
    ROLE_MAP = {
        "author": "content_author",
        "editor": "content_author",
        "knowledge_engineer": "admin",
        "teacher": "teacher",
        "admin": "admin"
    }

    async def role_checker(current_user: User = Depends(get_current_active_user)):
        # Superusers bypass all role checks
        if current_user.is_superuser:
            return current_user

        # Get user's current role
        # Use content_role if available (from UserProfile), otherwise use legacy role
        user_role = getattr(current_user, 'content_role', current_user.role)

        # Normalize allowed roles (map legacy to new)
        normalized_allowed_roles = set()
        for role in allowed_roles:
            normalized_allowed_roles.add(ROLE_MAP.get(role, role))

        # Normalize user role
        normalized_user_role = ROLE_MAP.get(user_role, user_role)

        # Check if user's role is in allowed roles
        # Also check the original user.role for backward compatibility
        if normalized_user_role not in normalized_allowed_roles and current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(allowed_roles)} (you have: {user_role})",
            )

        return current_user

    return role_checker


# Role-specific dependencies
get_author = require_role("author", "editor", "knowledge_engineer")
get_editor = require_role("editor", "knowledge_engineer")
get_knowledge_engineer = require_role("knowledge_engineer")


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Require superuser access."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires superuser privileges",
        )
    return current_user


# Secret encryption/decryption utilities
def encrypt_secret(plaintext: str) -> str:
    """
    Encrypt a secret value using Fernet encryption.

    Args:
        plaintext: The secret value to encrypt

    Returns:
        Base64-encoded encrypted string
    """
    try:
        encrypted_bytes = _fernet.encrypt(plaintext.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to encrypt secret: {e}")
        raise ValueError("Failed to encrypt secret value")


def decrypt_secret(encrypted: str) -> str:
    """
    Decrypt a secret value using Fernet encryption.

    Args:
        encrypted: Base64-encoded encrypted string

    Returns:
        Decrypted plaintext secret
    """
    try:
        decrypted_bytes = _fernet.decrypt(encrypted.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to decrypt secret: {e}")
        raise ValueError("Failed to decrypt secret value")


def mask_secret(secret: str, visible_chars: int = 4) -> str:
    """
    Mask a secret for display, showing only first few and last few characters.

    Args:
        secret: The secret to mask
        visible_chars: Number of characters to show at start and end

    Returns:
        Masked string like "sk-12...ef"
    """
    if len(secret) <= visible_chars * 2:
        return "*" * len(secret)

    start = secret[:visible_chars]
    end = secret[-visible_chars:]
    return f"{start}...{end}"
