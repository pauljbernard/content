"""
Initialize the Secret content type for storing API keys and sensitive configuration.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.content_type import ContentTypeModel
from models.user import User
from core.config import settings
import json


def init_secret_content_type():
    """Create the Secret content type if it doesn't exist."""
    print("Initializing Secret content type...")

    db = SessionLocal()

    try:
        # Check if Secret content type already exists
        existing = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "Secret"
        ).first()

        if existing:
            print("✓ Secret content type already exists")
            return

        # Get admin user
        admin = db.query(User).filter(
            User.email == settings.FIRST_SUPERUSER_EMAIL
        ).first()

        if not admin:
            print("✗ Admin user not found. Run init_db.py first.")
            return

        # Create Secret content type
        secret_content_type = ContentTypeModel(
            name="Secret",
            description="Secure storage for API keys and sensitive configuration values",
            icon="KeyIcon",
            is_system=True,  # System type, can't be deleted
            attributes=[
                {
                    "name": "name",
                    "label": "Secret Name",
                    "type": "text",
                    "required": True,
                    "config": {
                        "maxLength": 100,
                        "pattern": "^[A-Z][A-Z0-9_]*$",
                        "patternMessage": "Secret name must be UPPERCASE_SNAKE_CASE (e.g., CASE_API_KEY)"
                    },
                    "help_text": "Unique identifier for this secret (e.g., CASE_API_KEY, OPENAI_API_KEY)",
                    "order_index": 0
                },
                {
                    "name": "value",
                    "label": "Secret Value",
                    "type": "password_secret",
                    "required": True,
                    "config": {
                        "minLength": 1
                    },
                    "help_text": "The secret value (will be encrypted in database)",
                    "order_index": 1
                },
                {
                    "name": "description",
                    "label": "Description",
                    "type": "long_text",
                    "required": False,
                    "config": {
                        "maxLength": 500
                    },
                    "help_text": "What this secret is used for",
                    "order_index": 2
                },
                {
                    "name": "category",
                    "label": "Category",
                    "type": "choice",
                    "required": False,
                    "config": {
                        "choices": ["API_KEY", "DATABASE", "INTEGRATION", "OTHER"],
                        "multiple": False
                    },
                    "help_text": "Category of secret for organization",
                    "order_index": 3
                },
                {
                    "name": "is_active",
                    "label": "Active",
                    "type": "boolean",
                    "required": False,
                    "config": {},
                    "help_text": "Whether this secret is currently active/in use",
                    "default_value": True,
                    "order_index": 4
                }
            ],
            created_by=admin.id
        )

        db.add(secret_content_type)
        db.commit()
        db.refresh(secret_content_type)

        print(f"✓ Created Secret content type (ID: {secret_content_type.id})")
        print(f"  - Attributes: name, value (encrypted), description, category, is_active")
        print(f"  - System type: True (cannot be deleted)")

    except Exception as e:
        print(f"✗ Error creating Secret content type: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_secret_content_type()
