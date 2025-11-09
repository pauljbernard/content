"""
Database manager service for handling multiple database connections and migrations.
"""
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, ProgrammingError
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

from models.database_config import DatabaseConfig, DatabaseType, DatabaseConfigStatus
from database.session import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manage multiple database connections and migrations."""

    def __init__(self):
        self._engines: Dict[str, Any] = {}
        self._session_makers: Dict[str, sessionmaker] = {}

    def create_engine_from_config(self, config: DatabaseConfig):
        """Create SQLAlchemy engine from database configuration."""
        connection_string = config.get_connection_string()

        # Additional connection arguments
        connect_args = {}
        if config.db_type == DatabaseType.SQLITE:
            connect_args = {"check_same_thread": False}

        engine = create_engine(
            connection_string,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            connect_args=connect_args,
            echo=False,  # Set to True for SQL logging
        )

        return engine

    def test_connection(self, config: DatabaseConfig) -> tuple[bool, Optional[str]]:
        """
        Test database connection.
        Returns (success, error_message)
        """
        try:
            engine = self.create_engine_from_config(config)

            # Try to connect
            with engine.connect() as conn:
                if config.db_type == DatabaseType.POSTGRESQL:
                    # Test PostgreSQL connection
                    result = conn.execute(text("SELECT version()"))
                    version = result.scalar()
                    logger.info(f"Connected to PostgreSQL: {version}")

                    # Check for pgvector extension
                    result = conn.execute(
                        text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')")
                    )
                    has_pgvector = result.scalar()

                    if has_pgvector:
                        logger.info("pgvector extension is installed")
                        return True, None
                    else:
                        return True, "Warning: pgvector extension not installed. Vector search will not be available."

                elif config.db_type == DatabaseType.SQLITE:
                    # Test SQLite connection
                    result = conn.execute(text("SELECT sqlite_version()"))
                    version = result.scalar()
                    logger.info(f"Connected to SQLite: {version}")
                    return True, None

            engine.dispose()
            return True, None

        except OperationalError as e:
            error_msg = f"Connection failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def initialize_schema(self, config: DatabaseConfig, enable_pgvector: bool = True) -> tuple[bool, Optional[str]]:
        """
        Initialize database schema (create all tables).
        For PostgreSQL, optionally enable pgvector extension.
        """
        try:
            engine = self.create_engine_from_config(config)

            # For PostgreSQL, enable pgvector extension
            if config.db_type == DatabaseType.POSTGRESQL and enable_pgvector:
                with engine.connect() as conn:
                    try:
                        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                        conn.commit()
                        logger.info("pgvector extension enabled")
                    except ProgrammingError as e:
                        logger.warning(f"Could not enable pgvector: {e}")
                        return False, f"Failed to enable pgvector extension: {str(e)}"

            # Create all tables
            Base.metadata.create_all(bind=engine)
            logger.info("Database schema initialized successfully")

            engine.dispose()
            return True, None

        except Exception as e:
            error_msg = f"Schema initialization failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def get_table_names(self, config: DatabaseConfig) -> List[str]:
        """Get list of all tables in the database."""
        try:
            engine = self.create_engine_from_config(config)
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            engine.dispose()
            return tables
        except Exception as e:
            logger.error(f"Failed to get table names: {e}")
            return []

    def get_table_row_count(self, config: DatabaseConfig, table_name: str) -> int:
        """Get row count for a specific table."""
        try:
            engine = self.create_engine_from_config(config)
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                engine.dispose()
                return count or 0
        except Exception as e:
            logger.error(f"Failed to get row count for {table_name}: {e}")
            return 0

    def get_session(self, config: DatabaseConfig) -> Session:
        """Get a database session for the given configuration."""
        config_id = config.id

        # Create engine if not cached
        if config_id not in self._engines:
            self._engines[config_id] = self.create_engine_from_config(config)
            self._session_makers[config_id] = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engines[config_id]
            )

        # Return new session
        return self._session_makers[config_id]()

    def dispose_engine(self, config_id: str):
        """Dispose of a cached engine."""
        if config_id in self._engines:
            self._engines[config_id].dispose()
            del self._engines[config_id]
            del self._session_makers[config_id]
            logger.info(f"Disposed engine for config {config_id}")

    def dispose_all_engines(self):
        """Dispose of all cached engines."""
        for config_id in list(self._engines.keys()):
            self.dispose_engine(config_id)
        logger.info("Disposed all engines")


# Global database manager instance
db_manager = DatabaseManager()
