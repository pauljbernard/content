"""
Test that ClaudeClient loads configuration from database.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from services.claude_client import get_claude_client
from models.llm_config import LLMProvider, LLMModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_claude_client_config():
    """Test ClaudeClient configuration loading."""
    print("=" * 80)
    print("TESTING CLAUDE CLIENT CONFIGURATION")
    print("=" * 80)

    db = SessionLocal()

    try:
        # Check database configuration
        print("\n" + "=" * 60)
        print("DATABASE CONFIGURATION")
        print("=" * 60)

        default_model = db.query(LLMModel).filter(
            LLMModel.is_default_for_agents == True,
            LLMModel.is_active == True
        ).first()

        if default_model:
            print(f"\n✓ Default Agent Model Found:")
            print(f"  Model ID: {default_model.model_id}")
            print(f"  Display Name: {default_model.display_name}")
            print(f"  Type: {default_model.model_type}")

            provider = db.query(LLMProvider).filter(
                LLMProvider.id == default_model.provider_id
            ).first()

            if provider:
                print(f"\n✓ Provider Found:")
                print(f"  Name: {provider.name}")
                print(f"  Type: {provider.provider_type}")
                print(f"  Has API Key: {'Yes' if provider.api_key else 'No'}")
                if provider.api_key:
                    masked_key = provider.api_key[:8] + "..." + provider.api_key[-4:]
                    print(f"  API Key (masked): {masked_key}")
            else:
                print("\n✗ Provider not found!")
        else:
            print("\n✗ No default agent model found in database!")

        # Test ClaudeClient initialization
        print("\n" + "=" * 60)
        print("CLAUDE CLIENT INITIALIZATION")
        print("=" * 60)

        # Clear any existing singleton
        from services import claude_client as cc_module
        cc_module._claude_client = None

        # Initialize with database session
        client = get_claude_client(db_session=db)

        print(f"\n✓ ClaudeClient Initialized:")
        print(f"  Default Model: {client.default_model}")
        print(f"  Max Tokens: {client.max_tokens}")
        if client.api_key:
            masked_key = client.api_key[:8] + "..." + client.api_key[-4:]
            print(f"  API Key (masked): {masked_key}")

        # Compare with database
        print("\n" + "=" * 60)
        print("CONFIGURATION COMPARISON")
        print("=" * 60)

        if default_model and client.default_model == default_model.model_id:
            print(f"\n✓ USING DATABASE MODEL: {client.default_model}")
            print("  Status: SUCCESS - ClaudeClient is using database configuration!")
        else:
            print(f"\n⚠ Model mismatch:")
            print(f"  Database: {default_model.model_id if default_model else 'None'}")
            print(f"  Client: {client.default_model}")
            print("  Status: FALLBACK - Using .env configuration")

        if provider and provider.api_key:
            # We can't directly compare API keys for security, but we can check if they're different lengths
            if len(client.api_key) == len(provider.api_key):
                print(f"\n✓ API KEY LENGTH MATCH: Likely using database API key")
            else:
                print(f"\n⚠ API key length mismatch - may be using .env")

        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)

        return client.default_model == (default_model.model_id if default_model else None)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = test_claude_client_config()
    sys.exit(0 if success else 1)
