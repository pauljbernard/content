"""
Secrets Helper Service

Provides helper functions for retrieving secrets from the Secrets management system.
Used by other services (like standards_importer) to access API keys and credentials.
"""
import logging
from typing import Optional, Dict
from sqlalchemy.orm import Session

from models.content_type import ContentTypeModel, ContentInstanceModel
from utils.validation import decrypt_password_secret_fields

logger = logging.getLogger(__name__)


class SecretsHelper:
    """Helper service for retrieving and using secrets."""

    def __init__(self, db: Session):
        """
        Initialize secrets helper.

        Args:
            db: Database session
        """
        self.db = db
        self._secret_content_type = None

    def _get_secret_content_type(self) -> Optional[ContentTypeModel]:
        """Get the Secret content type."""
        if not self._secret_content_type:
            self._secret_content_type = self.db.query(ContentTypeModel).filter(
                ContentTypeModel.name == "Secret"
            ).first()

        return self._secret_content_type

    def get_secret_by_name(
        self,
        secret_name: str,
        api_key: Optional[str] = None
    ) -> Optional[Dict[str, str]]:
        """
        Get a secret by name, optionally filtered by API key.

        Args:
            secret_name: The secret name to search for (e.g., "CASE API", "OpenAI")
            api_key: Optional API key to filter by for exact match

        Returns:
            Dict with decrypted secret values:
                {
                    "id": instance_id,
                    "secret_name": service name,
                    "api_key": decrypted API key,
                    "secret_value": decrypted secret value,
                    "description": description,
                    "category": category,
                    "environment": environment,
                    "is_active": boolean
                }

            Returns None if not found or not active.
        """
        content_type = self._get_secret_content_type()
        if not content_type:
            logger.error("Secret content type not found. Run init_secret_content_type.py")
            return None

        # Get all instances for Secret content type
        instances = self.db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == content_type.id
        ).all()

        # Find matching secret
        for instance in instances:
            if instance.data.get("secret_name") == secret_name:
                # Decrypt password_secret fields
                decrypted_data = decrypt_password_secret_fields(
                    content_type.attributes,
                    instance.data
                )

                # Check if inactive
                if not decrypted_data.get("is_active", True):
                    logger.warning(f"Secret '{secret_name}' found but is inactive")
                    continue

                # If api_key filter specified, check if it matches
                if api_key and decrypted_data.get("api_key") != api_key:
                    continue

                return {
                    "id": instance.id,
                    "secret_name": decrypted_data.get("secret_name", ""),
                    "api_key": decrypted_data.get("api_key", ""),
                    "secret_value": decrypted_data.get("secret_value", ""),
                    "description": decrypted_data.get("description"),
                    "category": decrypted_data.get("category"),
                    "environment": decrypted_data.get("environment"),
                    "is_active": decrypted_data.get("is_active", True)
                }

        logger.warning(f"Secret '{secret_name}' not found or inactive")
        return None

    def get_case_network_credentials(self) -> Optional[Dict[str, str]]:
        """
        Get CASE Network API credentials.

        Returns:
            Dict with:
                {
                    "api_key": client ID,
                    "secret_value": client secret
                }

            Returns None if credentials not found.
        """
        secret = self.get_secret_by_name("case_network_key")
        if not secret:
            logger.error("CASE Network credentials not found. Please add 'case_network_key' secret.")
            return None

        return {
            "client_id": secret["api_key"],
            "client_secret": secret["secret_value"]
        }


def get_secrets_helper(db: Session) -> SecretsHelper:
    """
    Get a secrets helper instance.

    Args:
        db: Database session

    Returns:
        SecretsHelper instance
    """
    return SecretsHelper(db)
