"""
Knowledge Base Indexer Service

Scans, indexes, and maintains vector embeddings for knowledge base markdown files.
Enables semantic search across curriculum knowledge, frameworks, and instructional routines.
"""
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from models.knowledge_base import (
    KnowledgeBaseEmbeddingModel,
    KnowledgeBaseEmbeddingCreate
)
from services.vector_search import VectorSearchService

logger = logging.getLogger(__name__)

# Knowledge base root path
KNOWLEDGE_BASE_ROOT = Path(__file__).parent.parent.parent / "reference" / "hmh-knowledge"


class KnowledgeBaseIndexer:
    """Indexes knowledge base files for vector semantic search."""

    def __init__(self, db: Session, vector_service: Optional[VectorSearchService] = None):
        """
        Initialize indexer.

        Args:
            db: Database session
            vector_service: Optional vector search service (creates new if not provided)
        """
        self.db = db
        self.vector_service = vector_service or VectorSearchService(db_session=db)

    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content for change detection."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _categorize_path(self, relative_path: str) -> tuple[str, Optional[str], Optional[str]]:
        """
        Categorize a knowledge file path.

        Returns: (category, subject, state)
        """
        parts = relative_path.split("/")

        if parts[0] == "universal":
            return ("universal", None, None)
        elif parts[0] == "districts" and len(parts) >= 2:
            state = parts[1]
            return ("district", None, state)
        elif parts[0] == "subjects" and len(parts) >= 2:
            subject = parts[1]
            if len(parts) >= 4 and parts[2] == "districts":
                state = parts[3]
                return ("subject-district", subject, state)
            else:
                return ("subject-common", subject, None)
        elif parts[0] == "international":
            return ("international", None, None)

        return ("other", None, None)

    async def ensure_table_and_index_exist(self) -> bool:
        """
        Ensure knowledge base embeddings table and vector index exist.

        Returns:
            True if table and index exist or were created successfully
        """
        try:
            # Ensure table exists (should already exist from model import)
            logger.info("Checking if knowledge_base_embeddings table exists...")

            # Check if embedding column exists, add if missing
            success = await self.vector_service.add_embedding_column(
                self.db,
                table_name="knowledge_base_embeddings"
            )

            if success:
                logger.info("✓ Knowledge base vector index is ready")
                return True
            else:
                logger.error("Failed to initialize knowledge base vector index")
                return False

        except Exception as e:
            logger.error(f"Error ensuring table and index exist: {e}")
            return False

    def get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Get file metadata for indexing."""
        try:
            stat = file_path.stat()
            relative_path = str(file_path.relative_to(KNOWLEDGE_BASE_ROOT))
            category, subject, state = self._categorize_path(relative_path)

            return {
                "file_path": relative_path,
                "file_name": file_path.name,
                "category": category,
                "subject": subject,
                "state": state,
                "file_size_bytes": stat.st_size,
                "last_modified": datetime.fromtimestamp(stat.st_mtime)
            }
        except Exception as e:
            logger.error(f"Error getting metadata for {file_path}: {e}")
            return None

    async def index_file(self, file_path: Path, force_reindex: bool = False) -> bool:
        """
        Index a single knowledge base file.

        Args:
            file_path: Path to markdown file
            force_reindex: If True, reindex even if content hasn't changed

        Returns:
            True if successfully indexed
        """
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                logger.warning(f"Skipping empty file: {file_path}")
                return False

            # Calculate content hash
            content_hash = self._calculate_hash(content)

            # Get file metadata
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                return False

            relative_path = metadata["file_path"]

            # Check if already indexed with same content
            existing = self.db.query(KnowledgeBaseEmbeddingModel).filter(
                KnowledgeBaseEmbeddingModel.file_path == relative_path
            ).first()

            if existing and existing.content_hash == content_hash and not force_reindex:
                logger.debug(f"File unchanged, skipping: {relative_path}")
                return True

            # Generate embedding
            embedding = await self.vector_service.generate_embedding(content)

            if not embedding:
                logger.warning(f"Could not generate embedding for: {relative_path}")
                return False

            # Convert embedding to PostgreSQL format
            embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

            if existing:
                # Update existing
                update_query = text("""
                    UPDATE knowledge_base_embeddings
                    SET content = :content,
                        content_hash = :content_hash,
                        file_name = :file_name,
                        category = :category,
                        subject = :subject,
                        state = :state,
                        file_size_bytes = :file_size_bytes,
                        last_modified = :last_modified,
                        last_indexed = NOW(),
                        embedding = :embedding::vector
                    WHERE file_path = :file_path
                """)

                self.db.execute(update_query, {
                    "content": content,
                    "content_hash": content_hash,
                    "file_name": metadata["file_name"],
                    "category": metadata["category"],
                    "subject": metadata["subject"],
                    "state": metadata["state"],
                    "file_size_bytes": metadata["file_size_bytes"],
                    "last_modified": metadata["last_modified"],
                    "embedding": embedding_str,
                    "file_path": relative_path
                })

                logger.info(f"✓ Updated: {relative_path}")
            else:
                # Insert new
                insert_query = text("""
                    INSERT INTO knowledge_base_embeddings
                    (id, file_path, file_name, content, content_hash, category,
                     subject, state, file_size_bytes, last_modified, last_indexed, embedding)
                    VALUES
                    (:id, :file_path, :file_name, :content, :content_hash, :category,
                     :subject, :state, :file_size_bytes, :last_modified, NOW(), :embedding::vector)
                """)

                import uuid
                self.db.execute(insert_query, {
                    "id": str(uuid.uuid4()),
                    "file_path": relative_path,
                    "file_name": metadata["file_name"],
                    "content": content,
                    "content_hash": content_hash,
                    "category": metadata["category"],
                    "subject": metadata["subject"],
                    "state": metadata["state"],
                    "file_size_bytes": metadata["file_size_bytes"],
                    "last_modified": metadata["last_modified"],
                    "embedding": embedding_str
                })

                logger.info(f"✓ Indexed: {relative_path}")

            self.db.commit()
            return True

        except Exception as e:
            logger.error(f"Error indexing {file_path}: {e}")
            self.db.rollback()
            return False

    async def index_all_files(
        self,
        force_reindex: bool = False,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, int]:
        """
        Index all markdown files in the knowledge base.

        Args:
            force_reindex: If True, reindex all files even if unchanged
            progress_callback: Optional callback function for progress updates

        Returns:
            Statistics: {"total": int, "indexed": int, "updated": int, "failed": int}
        """
        try:
            # Ensure table and index exist
            success = await self.ensure_table_and_index_exist()
            if not success:
                return {"total": 0, "indexed": 0, "updated": 0, "failed": 0, "error": "Failed to initialize index"}

            # Find all .md files
            if not KNOWLEDGE_BASE_ROOT.exists():
                logger.error(f"Knowledge base root not found: {KNOWLEDGE_BASE_ROOT}")
                return {"total": 0, "indexed": 0, "updated": 0, "failed": 0, "error": "Knowledge base not found"}

            md_files = list(KNOWLEDGE_BASE_ROOT.rglob("*.md"))
            total = len(md_files)
            indexed = 0
            failed = 0

            logger.info(f"Found {total} markdown files in knowledge base")

            for i, file_path in enumerate(md_files):
                success = await self.index_file(file_path, force_reindex=force_reindex)

                if success:
                    indexed += 1
                else:
                    failed += 1

                # Progress callback
                if progress_callback and (i + 1) % 10 == 0:
                    progress_callback({
                        "total": total,
                        "processed": i + 1,
                        "indexed": indexed,
                        "failed": failed,
                        "progress_pct": int(((i + 1) / total) * 100)
                    })

            logger.info(f"✓ Knowledge base indexing complete: {indexed}/{total} files indexed, {failed} failed")

            return {
                "total": total,
                "indexed": indexed,
                "updated": indexed,  # Updated count same as indexed for now
                "failed": failed
            }

        except Exception as e:
            logger.error(f"Error during batch indexing: {e}")
            return {"total": 0, "indexed": 0, "updated": 0, "failed": 0, "error": str(e)}

    async def semantic_search(
        self,
        query_text: str,
        categories: Optional[List[str]] = None,
        subjects: Optional[List[str]] = None,
        states: Optional[List[str]] = None,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on knowledge base files.

        Args:
            query_text: Search query
            categories: Optional filter by categories (e.g., ["universal", "subject-common"])
            subjects: Optional filter by subjects (e.g., ["mathematics", "ela"])
            states: Optional filter by states (e.g., ["texas", "california"])
            limit: Maximum number of results
            similarity_threshold: Minimum cosine similarity (0-1)

        Returns:
            List of matching files with similarity scores
        """
        try:
            # Generate query embedding
            query_embedding = await self.vector_service.generate_embedding(query_text)

            if not query_embedding:
                logger.warning("Could not generate query embedding")
                return []

            # Convert to PostgreSQL format
            embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

            # Build filters
            filters = []
            params = {
                "query_embedding": embedding_str,
                "threshold": similarity_threshold,
                "limit": limit
            }

            if categories:
                filters.append(f"category = ANY(:categories)")
                params["categories"] = categories

            if subjects:
                filters.append(f"subject = ANY(:subjects)")
                params["subjects"] = subjects

            if states:
                filters.append(f"state = ANY(:states)")
                params["states"] = states

            filter_clause = " AND ".join(filters) if filters else "TRUE"

            # Semantic search query
            search_query = text(f"""
                SELECT
                    id,
                    file_path,
                    file_name,
                    content,
                    category,
                    subject,
                    state,
                    1 - (embedding <=> :query_embedding::vector) AS similarity
                FROM knowledge_base_embeddings
                WHERE embedding IS NOT NULL
                AND {filter_clause}
                AND 1 - (embedding <=> :query_embedding::vector) >= :threshold
                ORDER BY embedding <=> :query_embedding::vector
                LIMIT :limit
            """)

            result = self.db.execute(search_query, params)
            rows = result.fetchall()

            # Format results
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "file_path": row[1],
                    "file_name": row[2],
                    "content": row[3],
                    "category": row[4],
                    "subject": row[5],
                    "state": row[6],
                    "similarity": float(row[7])
                })

            logger.info(f"Knowledge base search returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Knowledge base semantic search failed: {e}")
            return []


# Singleton instance getter
_kb_indexer_instance: Optional[KnowledgeBaseIndexer] = None


def get_kb_indexer(db: Session) -> KnowledgeBaseIndexer:
    """Get or create knowledge base indexer instance."""
    return KnowledgeBaseIndexer(db)
