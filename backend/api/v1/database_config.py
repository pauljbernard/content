"""
Database configuration API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from database.session import get_db
from models.database_config import (
    DatabaseConfig,
    DatabaseType,
    DatabaseConfigStatus,
    MigrationJob
)
from models.user import User
from core.security import get_current_user, require_role
from services.database_manager import db_manager
from services.database_migration import migration_service
from services.vector_search import vector_search_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic schemas for request/response
class DatabaseConfigCreate(BaseModel):
    """Schema for creating database configuration."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    db_type: DatabaseType

    # PostgreSQL fields
    host: Optional[str] = None
    port: Optional[int] = 5432
    database_name: Optional[str] = None
    schema_name: Optional[str] = "public"
    username: Optional[str] = None
    password: Optional[str] = None
    ssl_mode: Optional[str] = "prefer"

    # SQLite field
    sqlite_path: Optional[str] = None

    # Connection pool
    pool_size: int = 5
    max_overflow: int = 10


class DatabaseConfigUpdate(BaseModel):
    """Schema for updating database configuration."""
    name: Optional[str] = None
    description: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database_name: Optional[str] = None
    schema_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    ssl_mode: Optional[str] = None
    sqlite_path: Optional[str] = None
    pool_size: Optional[int] = None
    max_overflow: Optional[int] = None


class MigrationJobCreate(BaseModel):
    """Schema for creating migration job."""
    source_config_id: str
    target_config_id: str
    generate_embeddings: bool = True
    tables: Optional[List[str]] = None


@router.get("/database-configs")
async def list_database_configs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """List all database configurations."""
    configs = db.query(DatabaseConfig).order_by(DatabaseConfig.created_at.desc()).all()
    return [config.to_dict() for config in configs]


@router.post("/database-configs")
async def create_database_config(
    config_data: DatabaseConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Create a new database configuration."""
    # Validate fields based on database type
    if config_data.db_type == DatabaseType.POSTGRESQL:
        if not all([config_data.host, config_data.port, config_data.database_name, config_data.username]):
            raise HTTPException(
                status_code=400,
                detail="PostgreSQL requires host, port, database_name, and username"
            )
    elif config_data.db_type == DatabaseType.SQLITE:
        if not config_data.sqlite_path:
            raise HTTPException(
                status_code=400,
                detail="SQLite requires sqlite_path"
            )

    # Check for duplicate name
    existing = db.query(DatabaseConfig).filter(DatabaseConfig.name == config_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Database configuration with this name already exists")

    # Create configuration
    config = DatabaseConfig(
        name=config_data.name,
        description=config_data.description,
        db_type=config_data.db_type,
        host=config_data.host,
        port=config_data.port,
        database_name=config_data.database_name,
        schema_name=config_data.schema_name,
        username=config_data.username,
        password=config_data.password,
        ssl_mode=config_data.ssl_mode,
        sqlite_path=config_data.sqlite_path,
        pool_size=config_data.pool_size,
        max_overflow=config_data.max_overflow,
        status=DatabaseConfigStatus.CONFIGURED,
        created_by=current_user.id
    )

    db.add(config)
    db.commit()
    db.refresh(config)

    logger.info(f"Created database config: {config.name} ({config.db_type})")

    return config.to_dict()


@router.get("/database-configs/{config_id}")
async def get_database_config(
    config_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Get database configuration by ID."""
    config = db.query(DatabaseConfig).filter(DatabaseConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Database configuration not found")

    return config.to_dict()


@router.put("/database-configs/{config_id}")
async def update_database_config(
    config_id: str,
    config_data: DatabaseConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Update database configuration."""
    config = db.query(DatabaseConfig).filter(DatabaseConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Database configuration not found")

    # Update fields
    for field, value in config_data.dict(exclude_unset=True).items():
        setattr(config, field, value)

    db.commit()
    db.refresh(config)

    logger.info(f"Updated database config: {config.name}")

    return config.to_dict()


@router.delete("/database-configs/{config_id}")
async def delete_database_config(
    config_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Delete database configuration."""
    config = db.query(DatabaseConfig).filter(DatabaseConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Database configuration not found")

    if config.is_active:
        raise HTTPException(status_code=400, detail="Cannot delete active database configuration")

    db.delete(config)
    db.commit()

    logger.info(f"Deleted database config: {config.name}")

    return {"message": "Database configuration deleted successfully"}


@router.post("/database-configs/{config_id}/test")
async def test_database_connection(
    config_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Test database connection."""
    config = db.query(DatabaseConfig).filter(DatabaseConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Database configuration not found")

    # Test connection
    success, error_msg = db_manager.test_connection(config)

    # Update config
    config.last_tested_at = datetime.utcnow()

    if success:
        config.status = DatabaseConfigStatus.TESTED
        config.last_error = None
    else:
        config.status = DatabaseConfigStatus.ERROR
        config.last_error = error_msg

    db.commit()

    if success:
        return {"success": True, "message": "Connection successful", "warning": error_msg}
    else:
        raise HTTPException(status_code=400, detail=error_msg)


@router.post("/database-configs/{config_id}/initialize")
async def initialize_database_schema(
    config_id: str,
    enable_pgvector: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Initialize database schema (create all tables)."""
    config = db.query(DatabaseConfig).filter(DatabaseConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Database configuration not found")

    # Initialize schema
    success, error_msg = db_manager.initialize_schema(config, enable_pgvector)

    if success:
        config.pgvector_enabled = enable_pgvector if config.db_type == DatabaseType.POSTGRESQL else False
        db.commit()

        return {
            "success": True,
            "message": "Database schema initialized successfully",
            "pgvector_enabled": config.pgvector_enabled
        }
    else:
        raise HTTPException(status_code=400, detail=error_msg)


@router.post("/database-configs/{config_id}/activate")
async def activate_database_config(
    config_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """
    Set database configuration as active and reload the database connection.

    This switches the active database without requiring a server restart.
    """
    config = db.query(DatabaseConfig).filter(DatabaseConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Database configuration not found")

    # Verify the database is accessible before activating
    if config.status not in [DatabaseConfigStatus.TESTED, DatabaseConfigStatus.ACTIVE]:
        raise HTTPException(
            status_code=400,
            detail=f"Database must be tested before activation. Current status: {config.status}"
        )

    # Deactivate all other configs
    db.query(DatabaseConfig).update({DatabaseConfig.is_active: False})

    # Activate this config
    config.is_active = True
    config.status = DatabaseConfigStatus.ACTIVE

    db.commit()
    db.close()  # Close current session before reload

    logger.info(f"Activated database config: {config.name}")

    # Reload database engine with new configuration
    try:
        from database.reload import reload_database_engine

        new_url = config.get_connection_string()
        reload_database_engine(new_url)

        logger.info(f"Database engine reloaded successfully: {config.name}")

        return {
            "success": True,
            "message": f"Database '{config.name}' is now active and connected",
            "database": config.name,
            "type": config.db_type.value
        }
    except Exception as e:
        logger.error(f"Error reloading database engine: {e}")
        return {
            "success": True,  # Config was activated
            "message": f"Database '{config.name}' activated but reload failed: {str(e)}. Server restart recommended.",
            "warning": "Engine reload failed",
            "database": config.name,
            "type": config.db_type.value
        }


@router.get("/database-configs/{config_id}/statistics")
async def get_database_statistics(
    config_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Get database statistics (table counts, etc.)."""
    config = db.query(DatabaseConfig).filter(DatabaseConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Database configuration not found")

    stats = migration_service.get_migration_statistics(config)
    return stats


# Migration endpoints
@router.post("/migrations")
async def create_migration_job(
    migration_data: MigrationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Create and start a database migration job."""
    # Get configs
    source_config = db.query(DatabaseConfig).filter(
        DatabaseConfig.id == migration_data.source_config_id
    ).first()
    target_config = db.query(DatabaseConfig).filter(
        DatabaseConfig.id == migration_data.target_config_id
    ).first()

    if not source_config:
        raise HTTPException(status_code=404, detail="Source database configuration not found")
    if not target_config:
        raise HTTPException(status_code=404, detail="Target database configuration not found")

    # Create migration job
    migration_job = MigrationJob(
        source_config_id=migration_data.source_config_id,
        target_config_id=migration_data.target_config_id,
        generate_embeddings=migration_data.generate_embeddings,
        created_by=current_user.id
    )

    db.add(migration_job)
    db.commit()
    db.refresh(migration_job)

    # Start migration in background (pass IDs, not objects)
    background_tasks.add_task(
        migration_service.migrate_database,
        source_config.id,
        target_config.id,
        migration_job.id,
        migration_data.tables
    )

    logger.info(f"Started migration job {migration_job.id}")

    return migration_job.to_dict()


@router.get("/migrations/{job_id}")
async def get_migration_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Get migration job status."""
    job = db.query(MigrationJob).filter(MigrationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Migration job not found")

    return job.to_dict()


@router.get("/migrations")
async def list_migration_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """List all migration jobs."""
    jobs = db.query(MigrationJob).order_by(MigrationJob.created_at.desc()).limit(50).all()
    return [job.to_dict() for job in jobs]


# Vector search endpoints
@router.post("/vector-search/generate-embeddings")
async def generate_all_embeddings(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["knowledge_engineer", "admin"]))
):
    """Generate vector embeddings for all content instances."""
    # This runs in background
    background_tasks.add_task(vector_search_service.batch_generate_embeddings, db)

    return {
        "success": True,
        "message": "Embedding generation started in background"
    }


@router.post("/vector-search/search")
async def vector_semantic_search(
    query: str,
    content_type_ids: Optional[List[str]] = None,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Perform semantic search using vector embeddings."""
    results = await vector_search_service.semantic_search(
        db=db,
        query_text=query,
        content_type_ids=content_type_ids,
        limit=limit
    )

    return {
        "query": query,
        "results": results,
        "count": len(results)
    }
