"""
Test that VectorSearchService loads configuration from database.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from services.vector_search import get_vector_search_service
from models.llm_config import LLMProvider, LLMModel
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_embedding_config():
    """Test VectorSearchService configuration loading."""
    print("=" * 80)
    print("TESTING VECTOR SEARCH SERVICE CONFIGURATION")
    print("=" * 80)

    db = SessionLocal()

    try:
        # Check database configuration
        print("\n" + "=" * 60)
        print("DATABASE CONFIGURATION")
        print("=" * 60)

        default_model = db.query(LLMModel).filter(
            LLMModel.is_default_for_embeddings == True,
            LLMModel.is_active == True
        ).first()

        if default_model:
            print(f"\n✓ Default Embedding Model Found:")
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
            print("\n✗ No default embedding model found in database!")

        # Test VectorSearchService initialization
        print("\n" + "=" * 60)
        print("VECTOR SEARCH SERVICE INITIALIZATION")
        print("=" * 60)

        # Clear any existing singleton
        from services import vector_search as vs_module
        vs_module._vector_search_service = None

        # Initialize with database session
        service = get_vector_search_service(db_session=db)

        print(f"\n✓ VectorSearchService Initialized:")
        print(f"  Default Model: {service.default_model}")
        print(f"  Embedding Dimensions: {service.embedding_dimensions}")
        if service.api_key:
            masked_key = service.api_key[:8] + "..." + service.api_key[-4:]
            print(f"  API Key (masked): {masked_key}")

        # Compare with database
        print("\n" + "=" * 60)
        print("CONFIGURATION COMPARISON")
        print("=" * 60)

        if default_model and service.default_model == default_model.model_id:
            print(f"\n✓ USING DATABASE MODEL: {service.default_model}")
            print("  Status: SUCCESS - VectorSearchService is using database configuration!")
        else:
            print(f"\n⚠ Model mismatch:")
            print(f"  Database: {default_model.model_id if default_model else 'None'}")
            print(f"  Service: {service.default_model}")
            print("  Status: FALLBACK - Using .env configuration")

        if provider and provider.api_key:
            # We can't directly compare API keys for security, but we can check if they're different lengths
            if len(service.api_key) == len(provider.api_key):
                print(f"\n✓ API KEY LENGTH MATCH: Likely using database API key")
            else:
                print(f"\n⚠ API key length mismatch - may be using .env")

        # Check dimensions match model type
        expected_dims = 3072 if "large" in service.default_model else 1536
        if service.embedding_dimensions == expected_dims:
            print(f"\n✓ DIMENSIONS CORRECT: {service.embedding_dimensions} for {service.default_model}")
        else:
            print(f"\n⚠ Dimensions mismatch: {service.embedding_dimensions} (expected {expected_dims})")

        # Test embedding generation
        print("\n" + "=" * 60)
        print("EMBEDDING GENERATION TEST")
        print("=" * 60)

        test_text = "This is a test sentence for embedding generation."
        print(f"\nTest text: '{test_text}'")
        print("Generating embedding...")

        embedding = await service.generate_embedding(test_text)

        if embedding:
            print(f"\n✓ EMBEDDING GENERATED SUCCESSFULLY")
            print(f"  Dimensions: {len(embedding)}")
            print(f"  First 5 values: {embedding[:5]}")
            print(f"  Status: SUCCESS - OpenAI embeddings are working!")
        else:
            print(f"\n✗ EMBEDDING GENERATION FAILED")
            print(f"  Status: FAILURE - Check OpenAI API key and package installation")

        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)

        # Return True if all tests pass
        config_match = service.default_model == (default_model.model_id if default_model else None)
        embedding_success = embedding is not None
        return config_match and embedding_success

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = asyncio.run(test_embedding_config())
    sys.exit(0 if success else 1)
