"""
Database reload utilities for dynamic database switching.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

logger = logging.getLogger(__name__)


def reload_database_engine(new_url: str):
    """
    Reload the database engine with a new connection URL.

    This allows switching databases without restarting the application.
    Properly disposes of the old engine before creating a new one.

    Args:
        new_url: New database connection string

    Returns:
        tuple: (new_engine, new_SessionLocal)
    """
    # Import here to avoid circular dependency
    from database import session as db_session

    try:
        logger.info(f"[Database Reload] Disposing old engine...")

        # Close all existing connections in the pool
        if hasattr(db_session, 'engine'):
            db_session.engine.dispose()
            logger.info(f"[Database Reload] Old engine disposed")

        # Create new engine with the new URL
        logger.info(f"[Database Reload] Creating new engine...")
        new_engine = create_engine(
            new_url,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            echo=settings.LOG_LEVEL == "DEBUG",
            pool_pre_ping=True,  # Enable connection health checks
        )

        # Create new session factory
        new_session_local = sessionmaker(autocommit=False, autoflush=False, bind=new_engine)

        # Replace module-level variables
        db_session.engine = new_engine
        db_session.SessionLocal = new_session_local
        db_session.DATABASE_URL = new_url

        logger.info(f"[Database Reload] Engine reloaded successfully")
        logger.info(f"[Database Reload] New database: {new_engine.url}")

        return new_engine, new_session_local

    except Exception as e:
        logger.error(f"[Database Reload] Error reloading engine: {e}")
        raise


def reload_from_active_config():
    """
    Reload database engine from the currently active database configuration.

    Queries the database for the active configuration and reloads the engine.
    Falls back to default SQLite if no active configuration exists.

    Returns:
        dict: Status information about the reload
    """
    from database import session as db_session
    from models.database_config import DatabaseConfig

    try:
        # Use current session to query for active config
        temp_session = db_session.SessionLocal()

        try:
            active_config = temp_session.query(DatabaseConfig).filter(
                DatabaseConfig.is_active == True
            ).first()

            if active_config:
                # Reload with active configuration
                new_url = active_config.get_connection_string()
                reload_database_engine(new_url)

                return {
                    "success": True,
                    "database": active_config.name,
                    "type": active_config.db_type.value,
                    "url": str(db_session.engine.url)
                }
            else:
                # No active config, reload with default
                reload_database_engine(settings.DATABASE_URL)

                return {
                    "success": True,
                    "database": "default",
                    "type": "sqlite",
                    "url": settings.DATABASE_URL
                }

        finally:
            temp_session.close()

    except Exception as e:
        logger.error(f"[Database Reload] Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }
