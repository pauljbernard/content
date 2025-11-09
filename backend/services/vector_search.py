"""
Vector search service using pgvector for semantic search.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy import text, Column
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import Float
import logging
import json
import anthropic

from core.config import settings
from models.content_type import ContentInstanceModel

logger = logging.getLogger(__name__)


class VectorSearchService:
    """Service for generating embeddings and performing vector search."""

    def __init__(self, db_session=None):
        """
        Initialize Vector Search service.

        Args:
            db_session: Optional database session to load configuration from database.
                       If not provided, uses .env configuration.
        """
        # Try to load configuration from database first
        api_key_from_db = None
        model_from_db = None
        self.embedding_dimensions = 1536  # Default for text-embedding-3-small

        if db_session:
            try:
                from models.llm_config import LLMProvider, LLMModel

                # Get default embedding model from database
                default_model = db_session.query(LLMModel).filter(
                    LLMModel.is_default_for_embeddings == True,
                    LLMModel.is_active == True
                ).first()

                if default_model:
                    model_from_db = default_model.model_id
                    logger.info(f"Using embedding model from database: {model_from_db}")

                    # Set dimensions based on model
                    if "text-embedding-3-large" in model_from_db:
                        self.embedding_dimensions = 3072
                    elif "text-embedding-3-small" in model_from_db or "text-embedding-ada-002" in model_from_db:
                        self.embedding_dimensions = 1536

                    # Get the provider for this model
                    provider = db_session.query(LLMProvider).filter(
                        LLMProvider.id == default_model.provider_id,
                        LLMProvider.is_active == True
                    ).first()

                    if provider and provider.api_key:
                        api_key_from_db = provider.api_key
                        logger.info(f"Using API key from database provider: {provider.name}")
                else:
                    logger.warning("No default embedding model found in database, falling back to .env config")
            except Exception as e:
                logger.warning(f"Failed to load embedding config from database: {e}. Falling back to .env config")

        # Use database config if available, otherwise fall back to .env
        self.api_key = api_key_from_db or getattr(settings, 'OPENAI_API_KEY', None) or ""
        self.default_model = model_from_db or "text-embedding-3-small"

        if self.api_key:
            logger.info(f"VectorSearchService initialized with model: {self.default_model}, dimensions: {self.embedding_dimensions}")
        else:
            logger.warning("No OpenAI API key available. Vector embeddings will not work. Configure LLM provider in database or set OPENAI_API_KEY in .env")

    async def generate_embedding(self, text: str, model: Optional[str] = None) -> Optional[List[float]]:
        """
        Generate vector embedding for text using OpenAI embeddings API.

        Args:
            text: Text to generate embedding for
            model: Optional model override (uses default_model if not specified)

        Returns:
            List of floats representing the embedding vector, or None if failed
        """
        try:
            if not self.api_key:
                logger.warning("Vector embeddings not configured. Please set up OpenAI API key.")
                return None

            # Use OpenAI embeddings
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.api_key)

            response = await client.embeddings.create(
                model=model or self.default_model,
                input=text
            )

            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")
            return embedding

        except ImportError:
            logger.error("OpenAI package not installed. Run: pip install openai")
            return None
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None

    async def generate_content_embedding(self, content_data: dict) -> Optional[List[float]]:
        """
        Generate embedding for content instance by combining relevant fields.
        """
        # Extract text from content data
        text_parts = []

        # Common fields to include
        text_fields = ["title", "name", "description", "content", "body", "text", "learning_objectives", "summary"]

        for field in text_fields:
            if field in content_data and content_data[field]:
                value = content_data[field]
                if isinstance(value, str):
                    text_parts.append(value)
                elif isinstance(value, list):
                    text_parts.extend([str(v) for v in value if v])

        # Combine all text
        combined_text = " ".join(text_parts)

        if not combined_text.strip():
            logger.warning("No text content found for embedding generation")
            return None

        # Truncate if too long (embeddings usually have token limits)
        max_chars = 8000  # Roughly 2000 tokens
        if len(combined_text) > max_chars:
            combined_text = combined_text[:max_chars]

        return await self.generate_embedding(combined_text)

    async def add_embedding_column(self, db: Session, table_name: str = "content_instances", create_global_index: bool = False):
        """
        Add vector embedding column to a table using pgvector.

        This requires PostgreSQL with pgvector extension enabled.

        Args:
            db: Database session
            table_name: Name of table to add embedding column to
            create_global_index: If True, creates a global index (not recommended for content_instances).
                                 Use create_content_type_vector_index() instead for per-type indexes.
        """
        try:
            # Check if column already exists
            check_query = text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                AND column_name = 'embedding'
            """)

            result = db.execute(check_query)
            exists = result.fetchone() is not None

            if exists:
                logger.info(f"Embedding column already exists in {table_name}")
                return True

            # Add vector column with dimensions from configured model
            alter_query = text(f"""
                ALTER TABLE {table_name}
                ADD COLUMN embedding vector({self.embedding_dimensions})
            """)

            db.execute(alter_query)
            db.commit()

            # Optionally create global index (not recommended for content_instances)
            if create_global_index:
                index_query = text(f"""
                    CREATE INDEX IF NOT EXISTS {table_name}_embedding_idx
                    ON {table_name}
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100)
                """)

                db.execute(index_query)
                db.commit()
                logger.info(f"✓ Added embedding column and global index to {table_name}")
            else:
                logger.info(f"✓ Added embedding column to {table_name} (no global index)")

            return True

        except Exception as e:
            logger.error(f"Failed to add embedding column: {e}")
            db.rollback()
            return False

    async def create_content_type_vector_index(
        self,
        db: Session,
        content_type_id: str,
        table_name: str = "content_instances"
    ) -> bool:
        """
        Create a filtered vector index for a specific content type.

        This creates a partial index that only includes rows for this content type,
        making vector searches much faster when filtering by content type.

        Args:
            db: Database session
            content_type_id: UUID of the content type
            table_name: Name of table (default: content_instances)

        Returns:
            True if index created successfully or already exists
        """
        try:
            # Sanitize content_type_id for use in index name (replace hyphens with underscores)
            safe_id = content_type_id.replace("-", "_")
            index_name = f"{table_name}_embedding_ct_{safe_id}_idx"

            # Check if index already exists
            check_query = text("""
                SELECT indexname
                FROM pg_indexes
                WHERE tablename = :table_name
                AND indexname = :index_name
            """)

            result = db.execute(check_query, {"table_name": table_name, "index_name": index_name})
            exists = result.fetchone() is not None

            if exists:
                logger.debug(f"Vector index already exists for content type {content_type_id}")
                return True

            # Ensure embedding column exists first
            await self.add_embedding_column(db, table_name, create_global_index=False)

            # Create filtered partial index for this content type
            # This index only contains embeddings for instances of this content type
            index_query = text(f"""
                CREATE INDEX {index_name}
                ON {table_name}
                USING ivfflat (embedding vector_cosine_ops)
                WHERE content_type_id = :content_type_id
                WITH (lists = 100)
            """)

            db.execute(index_query, {"content_type_id": content_type_id})
            db.commit()

            logger.info(f"✓ Created vector index for content type {content_type_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to create content type vector index: {e}")
            db.rollback()
            return False

    async def ensure_content_type_indexes_exist(
        self,
        db: Session,
        content_type_ids: List[str],
        table_name: str = "content_instances"
    ) -> bool:
        """
        Ensure vector indexes exist for all specified content types.

        This should be called before performing semantic search to ensure
        efficient index usage.

        Args:
            db: Database session
            content_type_ids: List of content type UUIDs
            table_name: Name of table (default: content_instances)

        Returns:
            True if all indexes exist or were created successfully
        """
        try:
            all_success = True
            for content_type_id in content_type_ids:
                success = await self.create_content_type_vector_index(
                    db, content_type_id, table_name
                )
                if not success:
                    all_success = False

            return all_success

        except Exception as e:
            logger.error(f"Failed to ensure content type indexes: {e}")
            return False

    async def update_instance_embedding(
        self,
        db: Session,
        instance_id: str,
        content_data: dict
    ) -> bool:
        """
        Generate and store embedding for a content instance.
        """
        try:
            # Generate embedding
            embedding = await self.generate_content_embedding(content_data)

            if not embedding:
                logger.warning(f"Could not generate embedding for instance {instance_id}")
                return False

            # Convert to PostgreSQL array format
            embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

            # Update instance
            update_query = text("""
                UPDATE content_instances
                SET embedding = :embedding::vector
                WHERE id = :instance_id
            """)

            db.execute(update_query, {"embedding": embedding_str, "instance_id": instance_id})
            db.commit()

            logger.info(f"✓ Updated embedding for instance {instance_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update instance embedding: {e}")
            db.rollback()
            return False

    async def batch_generate_embeddings(
        self,
        db: Session,
        batch_size: int = 10,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, int]:
        """
        Generate embeddings for all content instances that don't have them.

        Returns statistics: {"total": int, "generated": int, "failed": int}
        """
        try:
            # Find instances without embeddings
            query = text("""
                SELECT id, data
                FROM content_instances
                WHERE embedding IS NULL
                ORDER BY created_at DESC
            """)

            result = db.execute(query)
            instances = result.fetchall()

            total = len(instances)
            generated = 0
            failed = 0

            logger.info(f"Generating embeddings for {total} instances...")

            for i, row in enumerate(instances):
                instance_id = row[0]
                content_data = row[1]

                # Parse JSON data if needed
                if isinstance(content_data, str):
                    content_data = json.loads(content_data)

                # Generate embedding
                success = await self.update_instance_embedding(db, instance_id, content_data)

                if success:
                    generated += 1
                else:
                    failed += 1

                # Progress callback
                if progress_callback and (i + 1) % batch_size == 0:
                    progress_callback({
                        "total": total,
                        "processed": i + 1,
                        "generated": generated,
                        "failed": failed,
                        "progress_pct": int(((i + 1) / total) * 100)
                    })

            logger.info(f"✓ Batch embedding complete: {generated} generated, {failed} failed")

            return {
                "total": total,
                "generated": generated,
                "failed": failed
            }

        except Exception as e:
            logger.error(f"Batch embedding generation failed: {e}")
            return {"total": 0, "generated": 0, "failed": 0, "error": str(e)}

    async def semantic_search(
        self,
        db: Session,
        query_text: str,
        content_type_ids: Optional[List[str]] = None,
        limit: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using vector similarity.

        This method automatically ensures per-content-type vector indexes exist
        before searching, enabling efficient multi-type searches.

        Args:
            db: Database session
            query_text: Search query
            content_type_ids: Optional filter by content type IDs
            limit: Maximum number of results
            similarity_threshold: Minimum cosine similarity (0-1)

        Returns:
            List of matching instances with similarity scores
        """
        try:
            # Ensure vector indexes exist for requested content types
            if content_type_ids:
                await self.ensure_content_type_indexes_exist(db, content_type_ids)

            # Generate query embedding
            query_embedding = await self.generate_embedding(query_text)

            if not query_embedding:
                logger.warning("Could not generate query embedding, falling back to no results")
                return []

            # Convert to PostgreSQL array format
            embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

            # Build query
            # PostgreSQL will automatically use the filtered partial indexes
            # when it detects the WHERE clause matches the index conditions
            content_type_filter = ""
            if content_type_ids:
                ids_str = "','".join(content_type_ids)
                content_type_filter = f"AND content_type_id IN ('{ids_str}')"

            search_query = text(f"""
                SELECT
                    id,
                    content_type_id,
                    data,
                    1 - (embedding <=> :query_embedding::vector) AS similarity
                FROM content_instances
                WHERE embedding IS NOT NULL
                {content_type_filter}
                AND 1 - (embedding <=> :query_embedding::vector) >= :threshold
                ORDER BY embedding <=> :query_embedding::vector
                LIMIT :limit
            """)

            result = db.execute(
                search_query,
                {
                    "query_embedding": embedding_str,
                    "threshold": similarity_threshold,
                    "limit": limit
                }
            )

            rows = result.fetchall()

            # Format results
            results = []
            for row in rows:
                instance_id, content_type_id, data, similarity = row

                # Parse JSON data if needed
                if isinstance(data, str):
                    data = json.loads(data)

                results.append({
                    "id": instance_id,
                    "content_type_id": content_type_id,
                    "data": data,
                    "similarity": float(similarity)
                })

            logger.info(f"Semantic search returned {len(results)} results (searched {len(content_type_ids) if content_type_ids else 'all'} content types)")
            return results

        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []


# Global vector search service instance
_vector_search_service: Optional[VectorSearchService] = None


def get_vector_search_service(db_session=None) -> VectorSearchService:
    """
    Get or create the Vector Search service singleton.

    Args:
        db_session: Optional database session to load configuration.
                   If provided on first call, will load config from database.

    Returns:
        VectorSearchService instance
    """
    global _vector_search_service
    if _vector_search_service is None:
        # On first initialization, try to get database session if not provided
        if db_session is None:
            try:
                from database.session import SessionLocal
                db_session = SessionLocal()
                _vector_search_service = VectorSearchService(db_session=db_session)
                db_session.close()
            except Exception as e:
                logger.warning(f"Could not access database for embedding config: {e}. Using .env config.")
                _vector_search_service = VectorSearchService(db_session=None)
        else:
            _vector_search_service = VectorSearchService(db_session=db_session)

    return _vector_search_service


# For backward compatibility
vector_search_service = get_vector_search_service()
