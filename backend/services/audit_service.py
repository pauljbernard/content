"""
Audit logging service using AuditEvent content type.

Provides comprehensive audit logging for security and compliance.
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.content_type import ContentTypeModel, ContentInstanceModel
from models.user import User
import uuid
import logging

logger = logging.getLogger(__name__)


class AuditService:
    """Service for audit logging."""

    @staticmethod
    def log_event(
        db: Session,
        who: str,
        action: str,
        resource: str,
        decision: str = "allow",
        reason: Optional[str] = None,
        created_by_id: Optional[int] = None
    ) -> Optional[ContentInstanceModel]:
        """
        Log an audit event.

        Args:
            db: Database session
            who: User ID who performed the action (e.g., "user-1" or email)
            action: Action performed (e.g., "login", "create", "update", "delete", "view")
            resource: Affected resource (e.g., "content:123", "profile", "settings")
            decision: Access decision ("allow" or "deny")
            reason: Optional reason for the decision
            created_by_id: Legacy user ID for created_by field

        Returns:
            AuditEvent instance or None if logging fails
        """
        try:
            # Get AuditEvent content type
            audit_event_type = db.query(ContentTypeModel).filter(
                ContentTypeModel.name == "AuditEvent"
            ).first()

            if not audit_event_type:
                logger.error("AuditEvent content type not found!")
                return None

            # Create audit event data
            event_data = {
                "who": who,
                "action": action,
                "resource": resource,
                "decision": decision,
                "reason": reason or "",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Create audit event instance
            audit_event = ContentInstanceModel(
                id=str(uuid.uuid4()),
                content_type_id=audit_event_type.id,
                data=event_data,
                status="published",
                created_by=created_by_id or 1  # Default to system admin
            )

            db.add(audit_event)
            db.commit()

            logger.debug(f"Audit event logged: {who} → {action} on {resource} ({decision})")
            return audit_event

        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            db.rollback()
            return None

    @staticmethod
    def log_login(db: Session, user: User, success: bool = True):
        """Log user login event."""
        user_id_str = f"user-{user.id}" if user else "unknown"
        decision = "allow" if success else "deny"
        reason = "Successful login" if success else "Failed login attempt"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action="login",
            resource="authentication",
            decision=decision,
            reason=reason,
            created_by_id=user.id if user else None
        )

    @staticmethod
    def log_logout(db: Session, user: User):
        """Log user logout event."""
        user_id_str = f"user-{user.id}"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action="logout",
            resource="authentication",
            decision="allow",
            reason="User logged out",
            created_by_id=user.id
        )

    @staticmethod
    def log_create(db: Session, user: User, resource_type: str, resource_id: str):
        """Log resource creation event."""
        user_id_str = f"user-{user.id}"
        resource = f"{resource_type}:{resource_id}"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action="create",
            resource=resource,
            decision="allow",
            reason=f"Created {resource_type}",
            created_by_id=user.id
        )

    @staticmethod
    def log_update(db: Session, user: User, resource_type: str, resource_id: str):
        """Log resource update event."""
        user_id_str = f"user-{user.id}"
        resource = f"{resource_type}:{resource_id}"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action="update",
            resource=resource,
            decision="allow",
            reason=f"Updated {resource_type}",
            created_by_id=user.id
        )

    @staticmethod
    def log_delete(db: Session, user: User, resource_type: str, resource_id: str):
        """Log resource deletion event."""
        user_id_str = f"user-{user.id}"
        resource = f"{resource_type}:{resource_id}"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action="delete",
            resource=resource,
            decision="allow",
            reason=f"Deleted {resource_type}",
            created_by_id=user.id
        )

    @staticmethod
    def log_view(db: Session, user: User, resource_type: str, resource_id: str):
        """Log resource view event."""
        user_id_str = f"user-{user.id}"
        resource = f"{resource_type}:{resource_id}"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action="view",
            resource=resource,
            decision="allow",
            reason=f"Viewed {resource_type}",
            created_by_id=user.id
        )

    @staticmethod
    def log_access_denied(
        db: Session,
        user: User,
        action: str,
        resource: str,
        reason: str = "Insufficient permissions"
    ):
        """Log access denied event."""
        user_id_str = f"user-{user.id}" if user else "anonymous"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action=action,
            resource=resource,
            decision="deny",
            reason=reason,
            created_by_id=user.id if user else None
        )

    @staticmethod
    def log_permission_check(
        db: Session,
        user: User,
        action: str,
        resource: str,
        granted: bool,
        reason: Optional[str] = None
    ):
        """Log permission check result."""
        user_id_str = f"user-{user.id}"
        decision = "allow" if granted else "deny"
        default_reason = f"Permission {'granted' if granted else 'denied'} for {action} on {resource}"

        return AuditService.log_event(
            db=db,
            who=user_id_str,
            action=f"check:{action}",
            resource=resource,
            decision=decision,
            reason=reason or default_reason,
            created_by_id=user.id
        )

    @staticmethod
    def get_user_audit_trail(
        db: Session,
        user_id_str: str,
        limit: int = 100
    ):
        """
        Get audit trail for a specific user.

        Args:
            db: Database session
            user_id_str: User ID string (e.g., "user-1")
            limit: Maximum number of events to return

        Returns:
            List of audit events
        """
        try:
            audit_event_type = db.query(ContentTypeModel).filter(
                ContentTypeModel.name == "AuditEvent"
            ).first()

            if not audit_event_type:
                return []

            # Get all audit events
            all_events = db.query(ContentInstanceModel).filter(
                ContentInstanceModel.content_type_id == audit_event_type.id
            ).order_by(ContentInstanceModel.created_at.desc()).limit(limit * 2).all()

            # Filter by user
            user_events = []
            for event in all_events:
                if event.data.get("who") == user_id_str:
                    user_events.append(event)
                    if len(user_events) >= limit:
                        break

            return user_events

        except Exception as e:
            logger.error(f"Failed to get user audit trail: {e}")
            return []

    @staticmethod
    def get_recent_events(db: Session, limit: int = 100):
        """
        Get recent audit events across all users.

        Args:
            db: Database session
            limit: Maximum number of events to return

        Returns:
            List of audit events
        """
        try:
            audit_event_type = db.query(ContentTypeModel).filter(
                ContentTypeModel.name == "AuditEvent"
            ).first()

            if not audit_event_type:
                return []

            events = db.query(ContentInstanceModel).filter(
                ContentInstanceModel.content_type_id == audit_event_type.id
            ).order_by(ContentInstanceModel.created_at.desc()).limit(limit).all()

            return events

        except Exception as e:
            logger.error(f"Failed to get recent audit events: {e}")
            return []


# Global instance
audit_service = AuditService()
