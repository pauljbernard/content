"""
Update the Secret content type to support triplet model (secret_name, api_key, secret_value).
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.content_type import ContentTypeModel
from models.user import User
from core.config import settings


def update_secret_content_type():
    """Update the Secret content type to triplet model."""
    print("Updating Secret content type to triplet model...")

    db = SessionLocal()

    try:
        # Get Secret content type
        secret_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "Secret"
        ).first()

        if not secret_type:
            print("✗ Secret content type not found. Run init_secret_content_type.py first.")
            return

        # Update to triplet model
        secret_type.attributes = [
            {
                "name": "secret_name",
                "label": "Secret Name",
                "type": "text",
                "required": True,
                "config": {
                    "maxLength": 100
                },
                "help_text": "Service or category name (e.g., 'CASE API', 'OpenAI', 'Database')",
                "order_index": 0
            },
            {
                "name": "api_key",
                "label": "API Key / Username",
                "type": "password_secret",
                "required": True,
                "config": {
                    "minLength": 1
                },
                "help_text": "The API key, username, or identifier (will be encrypted)",
                "order_index": 1
            },
            {
                "name": "secret_value",
                "label": "Secret Value / Password",
                "type": "password_secret",
                "required": True,
                "config": {
                    "minLength": 1
                },
                "help_text": "The secret value or password (will be encrypted)",
                "order_index": 2
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
                "order_index": 3
            },
            {
                "name": "category",
                "label": "Category",
                "type": "choice",
                "required": False,
                "config": {
                    "choices": ["API_KEY", "DATABASE", "INTEGRATION", "CREDENTIALS", "OTHER"],
                    "multiple": False
                },
                "help_text": "Category of secret for organization",
                "order_index": 4
            },
            {
                "name": "environment",
                "label": "Environment",
                "type": "choice",
                "required": False,
                "config": {
                    "choices": ["PRODUCTION", "STAGING", "DEVELOPMENT", "TEST"],
                    "multiple": False
                },
                "help_text": "Which environment this secret is for",
                "order_index": 5
            },
            {
                "name": "is_active",
                "label": "Active",
                "type": "boolean",
                "required": False,
                "config": {},
                "help_text": "Whether this secret is currently active/in use",
                "default_value": True,
                "order_index": 6
            }
        ]

        db.commit()
        db.refresh(secret_type)

        print(f"✓ Updated Secret content type (ID: {secret_type.id})")
        print(f"  - Triplet model: secret_name + api_key + secret_value")
        print(f"  - Both api_key and secret_value are encrypted")
        print(f"  - Added environment field for multi-environment support")

    except Exception as e:
        print(f"✗ Error updating Secret content type: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    update_secret_content_type()
