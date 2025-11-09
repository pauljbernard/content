"""
Database configuration model for managing multiple database connections.
"""
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from database.session import Base
import uuid
import enum


class DatabaseType(str, enum.Enum):
    """Supported database types."""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class DatabaseConfigStatus(str, enum.Enum):
    """Database configuration status."""
    CONFIGURED = "configured"  # Configuration saved
    TESTED = "tested"  # Connection tested successfully
    ACTIVE = "active"  # Currently active database
    MIGRATING = "migrating"  # Data migration in progress
    ERROR = "error"  # Connection or migration error


class DatabaseConfig(Base):
    """Database configuration model."""
    __tablename__ = "database_configs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Database type
    db_type = Column(SQLEnum(DatabaseType), nullable=False)

    # Connection details (for PostgreSQL)
    host = Column(String(255), nullable=True)
    port = Column(Integer, nullable=True)
    database_name = Column(String(255), nullable=True)
    schema_name = Column(String(255), nullable=True, default="public")
    username = Column(String(255), nullable=True)
    password = Column(Text, nullable=True)  # Should be encrypted in production
    ssl_mode = Column(String(50), nullable=True, default="prefer")

    # SQLite path (for SQLite)
    sqlite_path = Column(String(500), nullable=True)

    # Status
    status = Column(SQLEnum(DatabaseConfigStatus), nullable=False, default=DatabaseConfigStatus.CONFIGURED)
    is_active = Column(Boolean, default=False)

    # Vector search capability
    pgvector_enabled = Column(Boolean, default=False)

    # Connection pool settings
    pool_size = Column(Integer, default=5)
    max_overflow = Column(Integer, default=10)

    # Error tracking
    last_error = Column(Text, nullable=True)
    last_tested_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String, nullable=True)

    def to_dict(self):
        """Convert to dictionary (excluding sensitive data)."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "db_type": self.db_type.value if self.db_type else None,
            "host": self.host,
            "port": self.port,
            "database_name": self.database_name,
            "schema_name": self.schema_name,
            "username": self.username,
            "password": "***" if self.password else None,  # Masked
            "ssl_mode": self.ssl_mode,
            "sqlite_path": self.sqlite_path,
            "status": self.status.value if self.status else None,
            "is_active": self.is_active,
            "pgvector_enabled": self.pgvector_enabled,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "last_error": self.last_error,
            "last_tested_at": self.last_tested_at.isoformat() if self.last_tested_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
        }

    def get_connection_string(self):
        """Generate SQLAlchemy connection string."""
        if self.db_type == DatabaseType.SQLITE:
            return f"sqlite:///{self.sqlite_path}"
        elif self.db_type == DatabaseType.POSTGRESQL:
            conn_str = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"
            if self.ssl_mode:
                conn_str += f"?sslmode={self.ssl_mode}"
            return conn_str
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")


class MigrationJob(Base):
    """Track database migration jobs."""
    __tablename__ = "migration_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_config_id = Column(String, nullable=False)
    target_config_id = Column(String, nullable=False)

    # Migration status
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    progress_pct = Column(Integer, default=0)

    # Statistics
    total_records = Column(Integer, default=0)
    migrated_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)

    # Details
    tables_to_migrate = Column(Text, nullable=True)  # JSON list of table names
    current_table = Column(String(255), nullable=True)
    error_log = Column(Text, nullable=True)

    # Vector embedding generation
    generate_embeddings = Column(Boolean, default=True)
    embeddings_generated = Column(Integer, default=0)

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "source_config_id": self.source_config_id,
            "target_config_id": self.target_config_id,
            "status": self.status,
            "progress_pct": self.progress_pct,
            "total_records": self.total_records,
            "migrated_records": self.migrated_records,
            "failed_records": self.failed_records,
            "tables_to_migrate": self.tables_to_migrate,
            "current_table": self.current_table,
            "error_log": self.error_log,
            "generate_embeddings": self.generate_embeddings,
            "embeddings_generated": self.embeddings_generated,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }
