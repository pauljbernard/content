"""
Indexing Management API endpoints.

Provides UI-accessible endpoints for managing vector indexes and embeddings.
"""
import logging
import json
import asyncio
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from database.session import get_db
from core.security import get_current_active_user
from models.user import User
from models.content_type import ContentTypeModel, ContentInstanceModel
from services.vector_search import get_vector_search_service
from services.knowledge_base_indexer import get_kb_indexer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/indexing")


# ============================================================================
# STATUS ENDPOINT
# ============================================================================

@router.get("/status")
async def get_indexing_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get current status of all vector indexes and embeddings.

    Returns information about:
    - Content instance embeddings (overall and per content type)
    - Knowledge base embeddings
    - Vector indexes created

    Requires knowledge_engineer role.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only knowledge engineers can access indexing status"
        )

    try:
        # Content instance embedding status
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns
                WHERE table_name = 'content_instances'
                AND column_name = 'embedding'
            )
        """))
        content_embedding_column_exists = result.scalar()

        content_stats = {"column_exists": content_embedding_column_exists}

        if content_embedding_column_exists:
            # Get overall stats
            result = db.execute(text("""
                SELECT
                    COUNT(*) as total,
                    COUNT(embedding) as with_embeddings,
                    COUNT(*) - COUNT(embedding) as without_embeddings
                FROM content_instances
            """))
            row = result.fetchone()

            if row:
                total, with_emb, without_emb = row
                content_stats.update({
                    "total_instances": total,
                    "with_embeddings": with_emb,
                    "without_embeddings": without_emb,
                    "coverage_percent": (with_emb / total * 100) if total > 0 else 0
                })

            # Get per-content-type stats
            result = db.execute(text("""
                SELECT
                    ct.id,
                    ct.name,
                    COUNT(ci.id) as total,
                    COUNT(ci.embedding) as with_embeddings,
                    COUNT(*) - COUNT(ci.embedding) as without_embeddings
                FROM content_types ct
                LEFT JOIN content_instances ci ON ct.id = ci.content_type_id
                GROUP BY ct.id, ct.name
                ORDER BY total DESC
            """))

            content_types = []
            for ct_row in result:
                ct_id, ct_name, ct_total, ct_with_emb, ct_without_emb = ct_row
                content_types.append({
                    "content_type_id": ct_id,
                    "content_type_name": ct_name,
                    "total_instances": ct_total,
                    "with_embeddings": ct_with_emb,
                    "without_embeddings": ct_without_emb,
                    "coverage_percent": (ct_with_emb / ct_total * 100) if ct_total > 0 else 0
                })

            content_stats["by_content_type"] = content_types

            # Check vector indexes
            result = db.execute(text("""
                SELECT indexname
                FROM pg_indexes
                WHERE tablename = 'content_instances'
                AND indexname LIKE 'content_instances_embedding_ct_%'
            """))
            indexes = [row[0] for row in result.fetchall()]
            content_stats["vector_indexes"] = {
                "count": len(indexes),
                "indexes": indexes
            }

        # Knowledge base embedding status
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'knowledge_base_embeddings'
            )
        """))
        kb_table_exists = result.scalar()

        kb_stats = {"table_exists": kb_table_exists}

        if kb_table_exists:
            # Check if embedding column exists
            result = db.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns
                    WHERE table_name = 'knowledge_base_embeddings'
                    AND column_name = 'embedding'
                )
            """))
            kb_embedding_column_exists = result.scalar()
            kb_stats["column_exists"] = kb_embedding_column_exists

            if kb_embedding_column_exists:
                result = db.execute(text("""
                    SELECT
                        COUNT(*) as total,
                        COUNT(embedding) as with_embeddings,
                        COUNT(*) - COUNT(embedding) as without_embeddings
                    FROM knowledge_base_embeddings
                """))
                row = result.fetchone()

                if row:
                    total, with_emb, without_emb = row
                    kb_stats.update({
                        "total_files": total,
                        "with_embeddings": with_emb,
                        "without_embeddings": without_emb,
                        "coverage_percent": (with_emb / total * 100) if total > 0 else 0
                    })

                # Category breakdown
                result = db.execute(text("""
                    SELECT category, COUNT(*) as count
                    FROM knowledge_base_embeddings
                    GROUP BY category
                    ORDER BY count DESC
                """))
                kb_stats["by_category"] = [
                    {"category": row[0], "count": row[1]}
                    for row in result.fetchall()
                ]
            else:
                # Table exists but no embedding column yet
                result = db.execute(text("""
                    SELECT COUNT(*) as total
                    FROM knowledge_base_embeddings
                """))
                row = result.fetchone()
                if row:
                    kb_stats["total_files"] = row[0]
                    kb_stats["with_embeddings"] = 0
                    kb_stats["without_embeddings"] = row[0]
                    kb_stats["coverage_percent"] = 0

        return {
            "content_instances": content_stats,
            "knowledge_base": kb_stats,
            "ready_to_index": content_embedding_column_exists and kb_table_exists
        }

    except Exception as e:
        logger.error(f"Error getting indexing status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get indexing status: {str(e)}"
        )


# ============================================================================
# CONTENT INSTANCE INDEXING ENDPOINTS
# ============================================================================

@router.post("/content/initialize")
async def initialize_content_indexes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Initialize content instance embeddings system.

    - Creates embedding column if missing
    - Creates vector indexes for all existing content types

    Requires knowledge_engineer role.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only knowledge engineers can initialize indexes"
        )

    try:
        vector_service = get_vector_search_service(db)

        # Step 1: Ensure embedding column exists
        success = await vector_service.add_embedding_column(
            db=db,
            table_name="content_instances",
            create_global_index=False
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create embedding column. Check PostgreSQL pgvector extension is installed."
            )

        # Step 2: Create indexes for all content types
        content_types = db.query(ContentTypeModel).all()
        created_count = 0
        failed_count = 0
        failed_types = []

        for ct in content_types:
            try:
                success = await vector_service.create_content_type_vector_index(
                    db=db,
                    content_type_id=ct.id
                )
                if success:
                    created_count += 1
                else:
                    failed_count += 1
                    failed_types.append(ct.name)
            except Exception as e:
                logger.error(f"Failed to create index for {ct.name}: {e}")
                failed_count += 1
                failed_types.append(ct.name)

        return {
            "success": True,
            "message": f"Initialized content instance indexes: {created_count} created, {failed_count} failed",
            "total_content_types": len(content_types),
            "indexes_created": created_count,
            "indexes_failed": failed_count,
            "failed_types": failed_types
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initializing content indexes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize content indexes: {str(e)}"
        )


@router.post("/content/generate-embeddings")
async def generate_content_embeddings(
    force_reindex: bool = False,
    stream: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Generate embeddings for content instances.

    - If force_reindex=False: Only generates embeddings for instances without them
    - If force_reindex=True: Regenerates ALL embeddings (expensive!)
    - If stream=True: Returns SSE stream with progress updates

    Requires knowledge_engineer role.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only knowledge engineers can generate embeddings"
        )

    if stream:
        # Return SSE stream
        async def generate():
            try:
                vector_service = get_vector_search_service(db)

                # Clear embeddings if force reindex
                if force_reindex:
                    logger.info("Force reindex: Clearing all embeddings")
                    db.execute(text("UPDATE content_instances SET embedding = NULL"))
                    db.commit()
                    yield f"data: {json.dumps({'type': 'info', 'message': 'Cleared existing embeddings'})}\n\n"
                    await asyncio.sleep(0)

                # Progress callback queue for SSE
                progress_queue = []

                def progress_callback(stats):
                    progress_data = {
                        "type": "progress",
                        "progress": stats['progress_pct'],
                        "processed": stats['processed'],
                        "total": stats['total'],
                        "generated": stats['generated'],
                        "failed": stats['failed']
                    }
                    progress_queue.append(f"data: {json.dumps(progress_data)}\n\n")

                # Generate embeddings with progress tracking
                # Note: batch_generate_embeddings is synchronous in its callback calls
                stats = await vector_service.batch_generate_embeddings(
                    db=db,
                    batch_size=5,  # Smaller batches for more frequent updates
                    progress_callback=progress_callback
                )

                # Send any remaining progress updates
                for progress_msg in progress_queue:
                    yield progress_msg
                    await asyncio.sleep(0)

                # Send final result
                yield f"data: {json.dumps({'type': 'complete', 'stats': stats})}\n\n"

            except Exception as e:
                logger.error(f"Error generating content embeddings: {e}")
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )

    # Non-streaming response
    try:
        vector_service = get_vector_search_service(db)

        # Clear embeddings if force reindex
        if force_reindex:
            logger.info("Force reindex: Clearing all embeddings")
            db.execute(text("UPDATE content_instances SET embedding = NULL"))
            db.commit()

        # Generate embeddings
        stats = await vector_service.batch_generate_embeddings(
            db=db,
            batch_size=10,
            progress_callback=None
        )

        return {
            "success": True,
            "message": f"Generated {stats['generated']} embeddings, {stats['failed']} failed",
            "total_instances": stats['total'],
            "generated": stats['generated'],
            "failed": stats['failed'],
            "force_reindex": force_reindex
        }

    except Exception as e:
        logger.error(f"Error generating content embeddings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embeddings: {str(e)}"
        )


# ============================================================================
# KNOWLEDGE BASE INDEXING ENDPOINTS
# ============================================================================

@router.post("/knowledge-base/initialize")
async def initialize_kb_index(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Initialize knowledge base embeddings system.

    - Creates knowledge_base_embeddings table if missing
    - Creates embedding column and vector index

    Requires knowledge_engineer role.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only knowledge engineers can initialize knowledge base index"
        )

    try:
        kb_indexer = get_kb_indexer(db)

        success = await kb_indexer.ensure_table_and_index_exist()

        if success:
            return {
                "success": True,
                "message": "Knowledge base index initialized successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize knowledge base index. Check PostgreSQL pgvector extension is installed."
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initializing KB index: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize knowledge base index: {str(e)}"
        )


@router.post("/knowledge-base/index-files")
async def index_kb_files(
    force_reindex: bool = False,
    stream: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Index all knowledge base markdown files.

    - If force_reindex=False: Only indexes new/changed files (uses SHA-256 hash)
    - If force_reindex=True: Reindexes ALL files (expensive!)
    - If stream=True: Returns SSE stream with progress updates

    Requires knowledge_engineer role.
    """
    if current_user.role != "knowledge_engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only knowledge engineers can index knowledge base files"
        )

    if stream:
        # Return SSE stream
        async def generate():
            try:
                kb_indexer = get_kb_indexer(db)

                # Progress callback queue for SSE
                progress_queue = []

                def progress_callback(stats):
                    progress_data = {
                        "type": "progress",
                        "progress": stats['progress_pct'],
                        "processed": stats['processed'],
                        "total": stats['total'],
                        "indexed": stats['indexed'],
                        "failed": stats['failed']
                    }
                    progress_queue.append(f"data: {json.dumps(progress_data)}\n\n")

                # Index files with progress tracking
                stats = await kb_indexer.index_all_files(
                    force_reindex=force_reindex,
                    progress_callback=progress_callback
                )

                # Send any remaining progress updates
                for progress_msg in progress_queue:
                    yield progress_msg
                    await asyncio.sleep(0)

                if stats.get("error"):
                    yield f"data: {json.dumps({'type': 'error', 'message': stats['error']})}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'complete', 'stats': stats})}\n\n"

            except Exception as e:
                logger.error(f"Error indexing KB files: {e}")
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )

    # Non-streaming response
    try:
        kb_indexer = get_kb_indexer(db)

        stats = await kb_indexer.index_all_files(
            force_reindex=force_reindex,
            progress_callback=None
        )

        if stats.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=stats["error"]
            )

        return {
            "success": True,
            "message": f"Indexed {stats['indexed']} files, {stats['failed']} failed",
            "total_files": stats['total'],
            "indexed": stats['indexed'],
            "failed": stats['failed'],
            "force_reindex": force_reindex
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error indexing KB files: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index knowledge base files: {str(e)}"
        )
