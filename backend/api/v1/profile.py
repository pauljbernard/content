"""
User Profile API endpoints.

Provides access to the current user's profile data using the content type system
(UserAccount and UserProfile instances).
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field

from database.session import get_db
from models.user import User
from models.content_type import ContentInstanceModel
from core.security import get_current_user
from services.content_instance_service import content_instance_service
from services.audit_service import audit_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic schemas
class UserAccountData(BaseModel):
    """User account data schema."""
    user_id: str
    tenant_id: str
    primary_org_id: Optional[str] = None
    email: EmailStr
    locale: Optional[str] = "en-US"
    status: str = "active"


class UserProfileAttrs(BaseModel):
    """User profile attributes schema."""
    full_name: Optional[str] = None
    original_role: Optional[str] = None
    is_superuser: bool = False
    migrated_from_user_id: Optional[int] = None
    preferences: Optional[str] = "{}"


class UserProfileData(BaseModel):
    """User profile data schema."""
    user_id: str
    role: str
    attrs: UserProfileAttrs
    accommodations: Optional[List[str]] = None
    grades: Optional[List[str]] = []
    subjects: Optional[List[str]] = []


class ProfileResponse(BaseModel):
    """Complete user profile response."""
    account: UserAccountData
    profile: UserProfileData
    legacy_user_id: int


class ProfileUpdateRequest(BaseModel):
    """Profile update request schema."""
    full_name: Optional[str] = None
    locale: Optional[str] = None
    grades: Optional[List[str]] = None
    subjects: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile.

    Returns complete profile data from UserAccount and UserProfile content instances.
    """
    user_id_str = f"user-{current_user.id}"

    # Get UserAccount instance
    user_account = content_instance_service.get_user_account_by_user_id(db, user_id_str)
    if not user_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found in content type system"
        )

    # Get UserProfile instance
    user_profile = content_instance_service.get_user_profile_by_user_id(db, user_id_str)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found in content type system"
        )

    # Extract data
    account_data = user_account.data
    profile_data = user_profile.data

    # Log profile view
    audit_service.log_view(db, current_user, "profile", user_id_str)

    # Build response
    return {
        "account": {
            "user_id": account_data.get("user_id"),
            "tenant_id": account_data.get("tenant_id"),
            "primary_org_id": account_data.get("primary_org_id"),
            "email": account_data.get("email"),
            "locale": account_data.get("locale", "en-US"),
            "status": account_data.get("status", "active")
        },
        "profile": {
            "user_id": profile_data.get("user_id"),
            "role": profile_data.get("role"),
            "attrs": profile_data.get("attrs", {}),
            "accommodations": profile_data.get("accommodations"),
            "grades": profile_data.get("grades", []),
            "subjects": profile_data.get("subjects", [])
        },
        "legacy_user_id": current_user.id
    }


@router.put("/profile")
async def update_profile(
    profile_update: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile.

    Allows updating:
    - Full name (stored in UserProfile.attrs.full_name)
    - Locale (stored in UserAccount.locale)
    - Grades (stored in UserProfile.grades)
    - Subjects (stored in UserProfile.subjects)
    - Preferences (stored in UserProfile.attrs.preferences)
    """
    user_id_str = f"user-{current_user.id}"

    # Get UserAccount instance
    user_account = content_instance_service.get_user_account_by_user_id(db, user_id_str)
    if not user_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found in content type system"
        )

    # Get UserProfile instance
    user_profile = content_instance_service.get_user_profile_by_user_id(db, user_id_str)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found in content type system"
        )

    # Update UserAccount fields
    if profile_update.locale is not None:
        account_data = user_account.data.copy()
        account_data["locale"] = profile_update.locale
        user_account.data = account_data
        user_account.updated_by = current_user.id

    # Update UserProfile fields
    profile_data = user_profile.data.copy()
    attrs = profile_data.get("attrs", {})

    if profile_update.full_name is not None:
        attrs["full_name"] = profile_update.full_name

    if profile_update.preferences is not None:
        import json
        attrs["preferences"] = json.dumps(profile_update.preferences)

    profile_data["attrs"] = attrs

    if profile_update.grades is not None:
        profile_data["grades"] = profile_update.grades

    if profile_update.subjects is not None:
        profile_data["subjects"] = profile_update.subjects

    user_profile.data = profile_data
    user_profile.updated_by = current_user.id

    # Commit changes
    db.commit()
    db.refresh(user_account)
    db.refresh(user_profile)

    logger.info(f"Profile updated for user {user_id_str}")

    # Log profile update
    audit_service.log_update(db, current_user, "profile", user_id_str)

    # Return updated profile
    return {
        "success": True,
        "message": "Profile updated successfully",
        "account": {
            "user_id": user_account.data.get("user_id"),
            "tenant_id": user_account.data.get("tenant_id"),
            "primary_org_id": user_account.data.get("primary_org_id"),
            "email": user_account.data.get("email"),
            "locale": user_account.data.get("locale", "en-US"),
            "status": user_account.data.get("status", "active")
        },
        "profile": {
            "user_id": user_profile.data.get("user_id"),
            "role": user_profile.data.get("role"),
            "attrs": user_profile.data.get("attrs", {}),
            "accommodations": user_profile.data.get("accommodations"),
            "grades": user_profile.data.get("grades", []),
            "subjects": user_profile.data.get("subjects", [])
        }
    }


@router.get("/profile/tenant")
async def get_tenant_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's tenant and organization information.

    Returns tenant and organization details from content type instances.
    """
    user_id_str = f"user-{current_user.id}"

    # Get tenant_id and org_id
    tenant_id = content_instance_service.get_user_tenant_id(db, user_id_str)
    org_id = content_instance_service.get_user_org_id(db, user_id_str)

    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant information not found"
        )

    # Get Tenant instance
    tenant = content_instance_service.find_instance(db, "Tenant", "tenant_id", tenant_id)
    if not tenant:
        return {
            "tenant_id": tenant_id,
            "tenant_name": "Unknown Tenant",
            "org_id": org_id,
            "org_name": "Unknown Organization"
        }

    # Get Organization instance
    org = None
    if org_id:
        org = content_instance_service.find_instance(db, "Organization", "org_id", org_id)

    return {
        "tenant_id": tenant_id,
        "tenant_name": tenant.data.get("name"),
        "tenant_plan": tenant.data.get("plan_tier"),
        "org_id": org_id,
        "org_name": org.data.get("name") if org else "Unknown Organization",
        "org_type": org.data.get("type") if org else None,
        "is_superuser": content_instance_service.is_user_superuser(db, user_id_str)
    }
