"""
Service layer for content instance operations (UserAccount, UserProfile, etc.)
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from models.content_type import ContentTypeModel, ContentInstanceModel
import logging

logger = logging.getLogger(__name__)


class ContentInstanceService:
    """Service for working with content instances."""

    # System content types that should NOT be tenant-isolated
    SYSTEM_CONTENT_TYPES = {
        "Tenant", "Organization", "UserAccount", "UserProfile",
        "Group", "RosterMembership", "RoleDefinition", "Permission",
        "PolicyRule", "Entitlement", "AuditEvent"
    }

    @staticmethod
    def get_content_type_by_name(db: Session, name: str) -> Optional[ContentTypeModel]:
        """Get content type by name."""
        return db.query(ContentTypeModel).filter(ContentTypeModel.name == name).first()

    @staticmethod
    def is_system_content_type(db: Session, content_type_id: str) -> bool:
        """Check if a content type is a system type (should not be tenant-isolated)."""
        content_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.id == content_type_id
        ).first()

        if not content_type:
            return False

        return content_type.name in ContentInstanceService.SYSTEM_CONTENT_TYPES

    @staticmethod
    def get_instances_by_type(
        db: Session,
        content_type_id: str,
        tenant_id: Optional[str] = None,
        include_system_types: bool = True
    ) -> List[ContentInstanceModel]:
        """
        Get all instances of a content type with optional tenant filtering.

        Args:
            db: Database session
            content_type_id: Content type ID
            tenant_id: Optional tenant ID for filtering
            include_system_types: If False, system content types will also be filtered by tenant

        Returns:
            List of content instances
        """
        query = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == content_type_id
        )

        # Apply tenant filtering for non-system content types
        if tenant_id and (not include_system_types or not ContentInstanceService.is_system_content_type(db, content_type_id)):
            # Filter instances by tenant_id in the data JSON
            # Note: This requires instances to have tenant_id in their data
            all_instances = query.all()
            return [inst for inst in all_instances if inst.data.get("tenant_id") == tenant_id]

        return query.all()

    @staticmethod
    def find_instance(
        db: Session,
        content_type_name: str,
        filter_field: str,
        filter_value: Any,
        tenant_id: Optional[str] = None
    ) -> Optional[ContentInstanceModel]:
        """
        Find a content instance by type and field value with optional tenant filtering.

        Args:
            db: Database session
            content_type_name: Name of content type (e.g., "UserAccount")
            filter_field: Field name in data JSON (e.g., "email")
            filter_value: Value to match
            tenant_id: Optional tenant ID for filtering

        Returns:
            ContentInstanceModel or None
        """
        # Get content type
        content_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == content_type_name
        ).first()

        if not content_type:
            logger.error(f"Content type not found: {content_type_name}")
            return None

        # Check if this is a system content type
        is_system = content_type_name in ContentInstanceService.SYSTEM_CONTENT_TYPES

        # Get all instances and filter in Python (for simplicity)
        instances = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == content_type.id
        ).all()

        for instance in instances:
            # Check field match
            if instance.data.get(filter_field) != filter_value:
                continue

            # Apply tenant filtering for non-system types
            if tenant_id and not is_system:
                if instance.data.get("tenant_id") != tenant_id:
                    continue

            return instance

        return None

    @staticmethod
    def instance_belongs_to_tenant(
        instance: ContentInstanceModel,
        tenant_id: str,
        db: Session
    ) -> bool:
        """
        Check if a content instance belongs to a specific tenant.

        System content types (UserAccount, Tenant, etc.) are not tenant-isolated.

        Args:
            instance: Content instance to check
            tenant_id: Tenant ID to check against
            db: Database session

        Returns:
            True if instance belongs to tenant or is a system type
        """
        # Check if this is a system content type
        if ContentInstanceService.is_system_content_type(db, instance.content_type_id):
            return True

        # Check tenant_id in instance data
        instance_tenant_id = instance.data.get("tenant_id")
        return instance_tenant_id == tenant_id

    @staticmethod
    def get_user_account_by_email(db: Session, email: str) -> Optional[ContentInstanceModel]:
        """Get UserAccount instance by email."""
        return ContentInstanceService.find_instance(db, "UserAccount", "email", email)

    @staticmethod
    def get_user_account_by_user_id(db: Session, user_id: str) -> Optional[ContentInstanceModel]:
        """Get UserAccount instance by user_id."""
        return ContentInstanceService.find_instance(db, "UserAccount", "user_id", user_id)

    @staticmethod
    def get_user_profile_by_user_id(db: Session, user_id: str) -> Optional[ContentInstanceModel]:
        """Get UserProfile instance by user_id."""
        return ContentInstanceService.find_instance(db, "UserProfile", "user_id", user_id)

    @staticmethod
    def get_user_role(db: Session, user_id: str) -> Optional[str]:
        """Get user's role from UserProfile."""
        profile = ContentInstanceService.get_user_profile_by_user_id(db, user_id)
        if profile:
            return profile.data.get("role")
        return None

    @staticmethod
    def is_user_superuser(db: Session, user_id: str) -> bool:
        """Check if user is a superuser (has cross-tenant access)."""
        profile = ContentInstanceService.get_user_profile_by_user_id(db, user_id)
        if profile:
            attrs = profile.data.get("attrs", {})
            return attrs.get("is_superuser", False)
        return False

    @staticmethod
    def get_user_tenant_id(db: Session, user_id: str) -> Optional[str]:
        """Get user's tenant_id from UserAccount."""
        account = ContentInstanceService.get_user_account_by_user_id(db, user_id)
        if account:
            return account.data.get("tenant_id")
        return None

    @staticmethod
    def get_user_org_id(db: Session, user_id: str) -> Optional[str]:
        """Get user's primary org_id from UserAccount."""
        account = ContentInstanceService.get_user_account_by_user_id(db, user_id)
        if account:
            return account.data.get("primary_org_id")
        return None

    @staticmethod
    def check_user_permission(
        db: Session,
        user_id: str,
        action: str,
        resource: str
    ) -> bool:
        """
        Check if user has permission for an action on a resource.

        This is a simplified implementation. Full RBAC would involve:
        1. Getting user's role(s)
        2. Getting role's permissions (with inheritance)
        3. Evaluating permission rules with conditions

        Args:
            user_id: User ID string (e.g., "user-1")
            action: Action to perform (e.g., "read", "write", "delete")
            resource: Resource pattern (e.g., "content:*", "users:123")

        Returns:
            True if permitted, False otherwise
        """
        # Get user's role
        role = ContentInstanceService.get_user_role(db, user_id)
        if not role:
            return False

        # Superusers have all permissions
        if ContentInstanceService.is_user_superuser(db, user_id):
            return True

        # Get RoleDefinition
        role_def = ContentInstanceService.find_instance(db, "RoleDefinition", "role_id", role)
        if not role_def:
            return False

        # Check permissions (simplified - just string matching)
        default_permissions = role_def.data.get("default_permissions", [])

        # Check for exact match or wildcard
        permission_pattern = f"{action}:{resource}"

        for perm in default_permissions:
            # Exact match
            if perm == permission_pattern:
                return True
            # Wildcard action
            if perm.startswith("*:") and permission_pattern.endswith(perm[2:]):
                return True
            # Wildcard resource
            if perm.endswith(":*") and permission_pattern.startswith(perm[:-1]):
                return True
            # Full wildcard
            if perm == "*:*:*":
                return True

        # Check inherited roles
        inherits = role_def.data.get("inherits", [])
        for parent_role in inherits:
            parent_role_def = ContentInstanceService.find_instance(db, "RoleDefinition", "role_id", parent_role)
            if parent_role_def:
                parent_permissions = parent_role_def.data.get("default_permissions", [])
                for perm in parent_permissions:
                    if perm == permission_pattern or perm == "*:*:*":
                        return True

        return False


# Global instance
content_instance_service = ContentInstanceService()
