"""
Context Retrieval Service for RAG-based Agent System

This service retrieves relevant context from:
1. Content Type instances (Subjects, States, Curricula, etc.)
2. Knowledge base files (markdown documentation)
3. Related content instances

The retrieved context is assembled into a structured format for LLM prompting.
Supports vector search for semantic similarity when pgvector is enabled.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.content_type import ContentTypeModel, ContentInstanceModel
from services.vector_search import vector_search_service
from services.knowledge_base_indexer import get_kb_indexer

logger = logging.getLogger(__name__)

# Knowledge base root path
KNOWLEDGE_BASE_ROOT = Path(__file__).parent.parent.parent / "reference" / "hmh-knowledge"


class ContextRetriever:
    """Retrieves and assembles context for agent prompting with vector search support."""

    def __init__(self, db: Session):
        self.db = db
        self.vector_search = vector_search_service
        self.kb_indexer = get_kb_indexer(db)

    async def retrieve_content_instances(
        self,
        content_type_ids: List[str],
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        semantic_query: Optional[str] = None,
        use_vector_search: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Retrieve content instances from specified content types.
        Uses vector semantic search if semantic_query is provided and pgvector is available.

        Args:
            content_type_ids: List of content type IDs to query
            filters: Dictionary of field:value filters to apply
            limit: Maximum number of instances to return
            semantic_query: Optional query text for semantic search
            use_vector_search: Whether to attempt vector search (default: True)

        Returns:
            List of content instances with their data
        """
        # Try vector search first if query provided and enabled
        if semantic_query and use_vector_search:
            try:
                logger.info(f"Attempting vector search for query: {semantic_query[:100]}")
                results = await self.vector_search.semantic_search(
                    db=self.db,
                    query_text=semantic_query,
                    content_type_ids=content_type_ids,
                    limit=limit,
                    similarity_threshold=0.7
                )

                if results:
                    logger.info(f"Vector search returned {len(results)} results")
                    return [
                        {
                            "id": result["id"],
                            "content_type_id": result["content_type_id"],
                            "data": result["data"],
                            "metadata": {
                                "similarity_score": result["similarity"],
                                "retrieval_method": "vector_search"
                            }
                        }
                        for result in results
                    ]
                else:
                    logger.info("Vector search returned no results, falling back to standard retrieval")

            except Exception as e:
                logger.warning(f"Vector search failed, falling back to standard retrieval: {e}")

        # Fall back to standard SQL query
        logger.info(f"Using standard SQL retrieval for content types: {content_type_ids}")
        query = self.db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id.in_(content_type_ids),
            ContentInstanceModel.status == "published"
        )

        # Apply filters if provided
        if filters:
            for field, value in filters.items():
                # This is a simplified filter - in production, you'd want more sophisticated JSON querying
                query = query.filter(
                    ContentInstanceModel.data.contains({field: value})
                )

        instances = query.limit(limit).all()

        return [
            {
                "id": instance.id,
                "content_type_id": instance.content_type_id,
                "data": instance.data,
                "metadata": {
                    "created_at": instance.created_at.isoformat(),
                    "updated_at": instance.updated_at.isoformat(),
                    "retrieval_method": "sql_query"
                }
            }
            for instance in instances
        ]

    def retrieve_by_field_value(
        self,
        content_type_id: str,
        field_name: str,
        field_value: Any
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific content instance by field value.

        Args:
            content_type_id: Content type to search in
            field_name: Field name to match
            field_value: Value to match

        Returns:
            Content instance data or None
        """
        instance = self.db.query(ContentInstanceModel).filter(
            and_(
                ContentInstanceModel.content_type_id == content_type_id,
                ContentInstanceModel.status == "published",
                ContentInstanceModel.data[field_name].as_string() == str(field_value)
            )
        ).first()

        if instance:
            return {
                "id": instance.id,
                "data": instance.data,
            }
        return None

    def retrieve_knowledge_files(
        self,
        paths: List[str],
        max_files: int = 20
    ) -> Dict[str, str]:
        """
        Retrieve knowledge base markdown files from specified paths.

        Args:
            paths: List of knowledge base paths (e.g., ["/subjects/mathematics/common/"])
            max_files: Maximum number of files to retrieve

        Returns:
            Dictionary mapping file paths to their content
        """
        knowledge_files = {}
        file_count = 0

        for path in paths:
            if file_count >= max_files:
                break

            # Resolve path relative to knowledge base root
            if path.startswith("/"):
                path = path[1:]  # Remove leading slash

            full_path = KNOWLEDGE_BASE_ROOT / path

            if not full_path.exists():
                logger.warning(f"Knowledge base path not found: {full_path}")
                continue

            # If it's a directory, get all markdown files
            if full_path.is_dir():
                for md_file in full_path.rglob("*.md"):
                    if file_count >= max_files:
                        break

                    try:
                        relative_path = md_file.relative_to(KNOWLEDGE_BASE_ROOT)
                        with open(md_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            knowledge_files[str(relative_path)] = content
                            file_count += 1
                    except Exception as e:
                        logger.error(f"Error reading file {md_file}: {e}")

            # If it's a file, read it directly
            elif full_path.is_file() and full_path.suffix == ".md":
                try:
                    relative_path = full_path.relative_to(KNOWLEDGE_BASE_ROOT)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        knowledge_files[str(relative_path)] = content
                        file_count += 1
                except Exception as e:
                    logger.error(f"Error reading file {full_path}: {e}")

        return knowledge_files

    async def retrieve_knowledge_files_semantic(
        self,
        query_text: str,
        categories: Optional[List[str]] = None,
        subjects: Optional[List[str]] = None,
        states: Optional[List[str]] = None,
        limit: int = 10
    ) -> Dict[str, str]:
        """
        Retrieve knowledge base files using vector semantic search.

        Args:
            query_text: Semantic search query (from content instance attributes)
            categories: Optional filter by categories (e.g., ["universal", "subject-common"])
            subjects: Optional filter by subjects (e.g., ["mathematics", "ela"])
            states: Optional filter by states (e.g., ["texas", "california"])
            limit: Maximum number of files to return

        Returns:
            Dictionary mapping file paths to their content
        """
        try:
            # Perform semantic search
            results = await self.kb_indexer.semantic_search(
                query_text=query_text,
                categories=categories,
                subjects=subjects,
                states=states,
                limit=limit,
                similarity_threshold=0.7
            )

            # Convert results to dict format
            knowledge_files = {}
            for result in results:
                knowledge_files[result["file_path"]] = result["content"]

            logger.info(f"KB semantic search returned {len(knowledge_files)} files")
            return knowledge_files

        except Exception as e:
            logger.error(f"KB semantic search failed: {e}")
            return {}

    async def assemble_context(
        self,
        retrieval_config: Dict[str, Any],
        user_inputs: Dict[str, Any],
        field_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assemble complete context from retrieval configuration and user inputs.
        Uses vector search for semantic retrieval when available.

        Args:
            retrieval_config: Configuration specifying what to retrieve
                {
                    "content_types": ["uuid1", "uuid2"],
                    "knowledge_base_paths": ["/subjects/math/common/"],
                    "filters": {"subject": "mathematics"},
                    "field_mappings": {"subject": "Subject.subject_code"}
                }
            user_inputs: User-provided field values
            field_name: Optional field name being generated (for semantic search)

        Returns:
            Assembled context dictionary
        """
        context = {
            "user_inputs": user_inputs,
            "content_instances": {},
            "knowledge_files": {},
            "metadata": {
                "total_instances": 0,
                "total_knowledge_files": 0,
                "retrieval_method": "unknown"
            }
        }

        # Build semantic query from user inputs for vector search (used by both content and KB search)
        semantic_query = None
        if user_inputs:
            # Combine relevant user input fields into a search query
            query_parts = []
            for key, value in user_inputs.items():
                if value and isinstance(value, str) and len(value.strip()) > 0:
                    query_parts.append(f"{key}: {value}")

            if query_parts:
                semantic_query = " ".join(query_parts)
                logger.info(f"Generated semantic query: {semantic_query[:200]}")

        # 1. Retrieve content instances
        content_type_ids = retrieval_config.get("content_types", [])
        filters = retrieval_config.get("filters", {})

        # Apply user inputs to filters
        resolved_filters = {}
        for key, value in filters.items():
            if isinstance(value, str) and value.startswith("$"):
                # Value is a reference to user input (e.g., "$subject")
                input_key = value[1:]  # Remove $
                resolved_filters[key] = user_inputs.get(input_key)
            else:
                resolved_filters[key] = value

        if content_type_ids:
            instances = await self.retrieve_content_instances(
                content_type_ids=content_type_ids,
                filters=resolved_filters,
                limit=10,
                semantic_query=semantic_query,
                use_vector_search=True
            )
            context["content_instances"] = {
                f"instance_{i}": instance
                for i, instance in enumerate(instances)
            }
            context["metadata"]["total_instances"] = len(instances)

            # Track retrieval method from first instance
            if instances and "metadata" in instances[0]:
                context["metadata"]["retrieval_method"] = instances[0]["metadata"].get("retrieval_method", "unknown")

        # 2. Retrieve knowledge base files
        use_kb_vector_search = retrieval_config.get("use_kb_vector_search", False)
        knowledge_paths = retrieval_config.get("knowledge_base_paths", [])

        if use_kb_vector_search and semantic_query:
            # Use vector semantic search on knowledge base
            logger.info("Using KB vector search")

            # Extract filters from user inputs (subject, state, etc.)
            kb_subjects = user_inputs.get("subject") or user_inputs.get("subjects")
            kb_states = user_inputs.get("state") or user_inputs.get("states")

            # Convert to lists if single values
            kb_subjects = [kb_subjects] if kb_subjects and isinstance(kb_subjects, str) else (kb_subjects or None)
            kb_states = [kb_states] if kb_states and isinstance(kb_states, str) else (kb_states or None)

            knowledge_files = await self.retrieve_knowledge_files_semantic(
                query_text=semantic_query,
                subjects=kb_subjects,
                states=kb_states,
                limit=10
            )
            context["knowledge_files"] = knowledge_files
            context["metadata"]["total_knowledge_files"] = len(knowledge_files)
            context["metadata"]["kb_retrieval_method"] = "vector_search"

        elif knowledge_paths:
            # Use path-based retrieval (existing behavior)
            logger.info("Using KB path-based retrieval")

            # Resolve path placeholders (e.g., /subjects/{subject}/ → /subjects/mathematics/)
            resolved_paths = []
            for path in knowledge_paths:
                resolved_path = path
                for key, value in user_inputs.items():
                    placeholder = f"{{{key}}}"
                    if placeholder in resolved_path:
                        resolved_path = resolved_path.replace(placeholder, str(value))
                resolved_paths.append(resolved_path)

            knowledge_files = self.retrieve_knowledge_files(
                paths=resolved_paths,
                max_files=20
            )
            context["knowledge_files"] = knowledge_files
            context["metadata"]["total_knowledge_files"] = len(knowledge_files)
            context["metadata"]["kb_retrieval_method"] = "path_based"

        return context

    def format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format assembled context into a string suitable for LLM prompting.

        Args:
            context: Assembled context from assemble_context()

        Returns:
            Formatted context string
        """
        sections = []

        # User Inputs
        sections.append("## User Inputs")
        for key, value in context["user_inputs"].items():
            sections.append(f"- **{key}**: {value}")

        # Content Instances
        if context["content_instances"]:
            sections.append("\n## Retrieved Content")
            for instance_id, instance in context["content_instances"].items():
                sections.append(f"\n### {instance_id}")
                sections.append(f"```json\n{json.dumps(instance['data'], indent=2)}\n```")

        # Knowledge Files
        if context["knowledge_files"]:
            sections.append("\n## Knowledge Base Files")
            for file_path, content in context["knowledge_files"].items():
                sections.append(f"\n### {file_path}")
                # Truncate very long files
                if len(content) > 5000:
                    content = content[:5000] + "\n\n... (truncated for brevity) ..."
                sections.append(f"```markdown\n{content}\n```")

        # Metadata
        sections.append(f"\n## Context Metadata")
        sections.append(f"- Total Content Instances: {context['metadata']['total_instances']}")
        sections.append(f"- Total Knowledge Files: {context['metadata']['total_knowledge_files']}")

        return "\n".join(sections)


def get_context_retriever(db: Session) -> ContextRetriever:
    """Factory function to create a context retriever."""
    return ContextRetriever(db)
