"""
Database session management with support for dynamic database configuration.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Base class for models (must be defined before imports)
Base = declarative_base()


def get_active_database_url():
    """
    Get the active database URL from configuration.

    Checks for an active database configuration in the database.
    Falls back to default settings.DATABASE_URL if:
    - No active configuration exists
    - Error accessing the configuration
    - This is the first startup (tables don't exist yet)
    """
    # First, try the default SQLite database to check for active config
    default_url = settings.DATABASE_URL

    try:
        # Create temporary engine to check for active configuration
        temp_engine = create_engine(default_url, echo=False)
        temp_session = sessionmaker(bind=temp_engine)()

        # Check if database_configs table exists (avoid circular import)
        with temp_engine.connect() as conn:
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='database_configs'"
            ))
            if not result.fetchone():
                # Table doesn't exist yet (first startup)
                temp_session.close()
                temp_engine.dispose()
                return default_url

        # Import here to avoid circular dependency
        from models.database_config import DatabaseConfig

        # Query for active database configuration
        active_config = temp_session.query(DatabaseConfig).filter(
            DatabaseConfig.is_active == True
        ).first()

        temp_session.close()
        temp_engine.dispose()

        if active_config:
            # Use active configuration
            db_url = active_config.get_connection_string()
            print(f"[Database] Using active configuration: {active_config.name} ({active_config.db_type.value})")
            return db_url
        else:
            # No active configuration, use default
            print(f"[Database] No active configuration found, using default SQLite")
            return default_url

    except Exception as e:
        # Error checking configuration, fall back to default
        print(f"[Database] Error loading active configuration: {e}")
        print(f"[Database] Falling back to default SQLite")
        return default_url


# Get the database URL (checks for active configuration)
DATABASE_URL = get_active_database_url()

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=settings.LOG_LEVEL == "DEBUG",
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
