"""
Database migration service for copying data between databases.
"""
from sqlalchemy import inspect, MetaData, Table, select, text
from sqlalchemy.orm import Session
from typing import List, Optional, Callable
import logging
import json
from datetime import datetime

from models.database_config import DatabaseConfig, MigrationJob, DatabaseType
from services.database_manager import db_manager
from database.session import SessionLocal

logger = logging.getLogger(__name__)


class DatabaseMigrationService:
    """Service for migrating data between databases."""

    def __init__(self):
        self.progress_callback: Optional[Callable] = None

    def set_progress_callback(self, callback: Callable):
        """Set callback function for progress updates."""
        self.progress_callback = callback

    def _update_progress(self, migration_job: MigrationJob, db: Session):
        """Update migration job progress in database."""
        if migration_job.total_records > 0:
            migration_job.progress_pct = int(
                (migration_job.migrated_records / migration_job.total_records) * 100
            )
        db.commit()

        if self.progress_callback:
            self.progress_callback(migration_job.to_dict())

    def _clear_target_database(
        self,
        target_config: DatabaseConfig,
        target_engine,
        tables_to_clear: List[str]
    ) -> tuple[bool, Optional[str]]:
        """
        Clear all data from target database tables before migration.

        Args:
            target_config: Target database configuration
            target_engine: SQLAlchemy engine for target database
            tables_to_clear: List of table names to clear

        Returns:
            (success, error_message)
        """
        try:
            logger.info(f"Clearing {len(tables_to_clear)} tables in target database...")

            with target_engine.begin() as conn:
                if target_config.db_type == DatabaseType.POSTGRESQL:
                    # For PostgreSQL: Disable foreign key checks temporarily
                    # and use TRUNCATE CASCADE for efficient clearing

                    # Build list of tables to truncate (excluding metadata tables)
                    exclude_tables = {"database_configs", "migration_jobs", "alembic_version"}
                    tables_to_truncate = [t for t in tables_to_clear if t not in exclude_tables]

                    if tables_to_truncate:
                        # Truncate all tables in one statement with CASCADE
                        table_list = ", ".join(tables_to_truncate)
                        truncate_sql = f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE"

                        logger.info(f"Executing: {truncate_sql}")
                        conn.execute(text(truncate_sql))

                        logger.info(f"✓ Cleared {len(tables_to_truncate)} tables successfully")

                elif target_config.db_type == DatabaseType.SQLITE:
                    # For SQLite: Delete from each table individually
                    exclude_tables = {"database_configs", "migration_jobs", "alembic_version"}

                    for table_name in tables_to_clear:
                        if table_name not in exclude_tables:
                            conn.execute(text(f"DELETE FROM {table_name}"))
                            logger.info(f"✓ Cleared table: {table_name}")

            return True, None

        except Exception as e:
            error_msg = f"Failed to clear target database: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg

    async def migrate_database(
        self,
        source_config_id: str,
        target_config_id: str,
        migration_job_id: str,
        tables_to_migrate: Optional[List[str]] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Migrate data from source database to target database.

        This method runs as a background task and creates its own database session.

        Args:
            source_config_id: Source database configuration ID
            target_config_id: Target database configuration ID
            migration_job_id: Migration job ID
            tables_to_migrate: Optional list of table names to migrate (defaults to all)

        Returns:
            (success, error_message)
        """
        # Create own database session (not request-scoped)
        db = SessionLocal()

        try:
            # Load objects from database
            migration_job = db.query(MigrationJob).filter(MigrationJob.id == migration_job_id).first()
            source_config = db.query(DatabaseConfig).filter(DatabaseConfig.id == source_config_id).first()
            target_config = db.query(DatabaseConfig).filter(DatabaseConfig.id == target_config_id).first()

            if not migration_job or not source_config or not target_config:
                raise ValueError("Migration job or configs not found")

            # Update job status
            migration_job.status = "running"
            migration_job.started_at = datetime.utcnow()
            db.commit()

            # Create engines
            source_engine = db_manager.create_engine_from_config(source_config)
            target_engine = db_manager.create_engine_from_config(target_config)

            # Get table names
            inspector = inspect(source_engine)
            all_tables = inspector.get_table_names()

            # Filter tables
            if tables_to_migrate:
                tables = [t for t in all_tables if t in tables_to_migrate]
            else:
                # Exclude migration-related tables from source
                exclude_tables = {"database_configs", "migration_jobs", "alembic_version"}
                tables = [t for t in all_tables if t not in exclude_tables]

            # Order tables by dependency (parents before children)
            # This prevents foreign key violations during migration
            dependency_order = [
                # Core tables (no dependencies)
                "users",

                # Tables dependent on users
                "llm_providers",
                "llm_models",
                "content_types",
                "database_configs",

                # Tables dependent on content_types
                "content_instances",
                "content_relationships",

                # Other tables
                "agent_jobs",
                "agent_workflows",
                "workflow_executions",
                "standards",
                "standard_import_jobs",
                "content",
                "content_reviews",
            ]

            # Sort tables by dependency order
            ordered_tables = []
            for table_name in dependency_order:
                if table_name in tables:
                    ordered_tables.append(table_name)

            # Add any remaining tables not in dependency_order
            for table_name in tables:
                if table_name not in ordered_tables:
                    ordered_tables.append(table_name)

            tables = ordered_tables

            migration_job.tables_to_migrate = json.dumps(tables)
            db.commit()

            # Clear target database before migration to avoid duplicate key errors
            logger.info("Clearing target database before migration...")
            clear_success, clear_error = self._clear_target_database(
                target_config,
                target_engine,
                tables
            )

            if not clear_success:
                raise Exception(f"Failed to clear target database: {clear_error}")

            logger.info("Target database cleared successfully")

            # Count total records
            total_records = 0
            for table_name in tables:
                count = db_manager.get_table_row_count(source_config, table_name)
                total_records += count

            migration_job.total_records = total_records
            db.commit()

            logger.info(f"Migrating {len(tables)} tables with {total_records} total records")

            # Migrate each table
            migrated_count = 0
            failed_count = 0

            for table_name in tables:
                migration_job.current_table = table_name
                db.commit()

                try:
                    # Reflect table from source
                    metadata = MetaData()
                    source_table = Table(table_name, metadata, autoload_with=source_engine)
                    target_table = Table(table_name, metadata, autoload_with=target_engine)

                    # Read data from source
                    with source_engine.connect() as source_conn:
                        result = source_conn.execute(select(source_table))
                        rows = result.fetchall()

                        logger.info(f"Migrating {len(rows)} rows from {table_name}")

                        # Write data to target in batches
                        batch_size = 100
                        with target_engine.begin() as target_conn:
                            for i in range(0, len(rows), batch_size):
                                batch = rows[i:i + batch_size]

                                # Convert rows to dictionaries
                                data_batch = [dict(row._mapping) for row in batch]

                                # Insert batch
                                if data_batch:
                                    target_conn.execute(target_table.insert(), data_batch)

                                migrated_count += len(batch)
                                migration_job.migrated_records = migrated_count
                                self._update_progress(migration_job, db)

                        logger.info(f"✓ Migrated {len(rows)} rows from {table_name}")

                except Exception as e:
                    error_msg = f"Error migrating table {table_name}: {str(e)}"
                    logger.error(error_msg)
                    failed_count += len(rows) if 'rows' in locals() else 0
                    migration_job.failed_records = failed_count

                    # Append to error log
                    if migration_job.error_log:
                        migration_job.error_log += f"\n{error_msg}"
                    else:
                        migration_job.error_log = error_msg

                    db.commit()
                    # Continue with next table

            # Clean up
            source_engine.dispose()
            target_engine.dispose()

            # Update final status
            migration_job.status = "completed" if failed_count == 0 else "completed_with_errors"
            migration_job.completed_at = datetime.utcnow()
            migration_job.progress_pct = 100
            db.commit()

            success_msg = f"Migration completed: {migrated_count} records migrated"
            if failed_count > 0:
                success_msg += f", {failed_count} failed"

            logger.info(success_msg)
            return True, None

        except Exception as e:
            error_msg = f"Migration failed: {str(e)}"
            logger.error(error_msg, exc_info=True)

            # Try to update job status
            try:
                migration_job = db.query(MigrationJob).filter(MigrationJob.id == migration_job_id).first()
                if migration_job:
                    migration_job.status = "failed"
                    migration_job.error_log = error_msg
                    migration_job.completed_at = datetime.utcnow()
                    db.commit()
            except Exception as update_error:
                logger.error(f"Failed to update job status: {update_error}")

            return False, error_msg

        finally:
            # Always close the session
            db.close()

    def get_migration_statistics(
        self,
        source_config: DatabaseConfig,
        tables: Optional[List[str]] = None
    ) -> dict:
        """
        Get statistics about data to be migrated.

        Returns:
            {
                "total_tables": int,
                "total_records": int,
                "table_counts": {"table_name": count, ...},
                "estimated_time_minutes": float
            }
        """
        try:
            inspector = inspect(db_manager.create_engine_from_config(source_config))
            all_tables = inspector.get_table_names()

            if tables:
                tables_to_count = [t for t in all_tables if t in tables]
            else:
                exclude_tables = {"database_configs", "migration_jobs", "alembic_version"}
                tables_to_count = [t for t in all_tables if t not in exclude_tables]

            table_counts = {}
            total_records = 0

            for table_name in tables_to_count:
                count = db_manager.get_table_row_count(source_config, table_name)
                table_counts[table_name] = count
                total_records += count

            # Estimate time (rough: 1000 records per second)
            estimated_seconds = total_records / 1000
            estimated_minutes = estimated_seconds / 60

            return {
                "total_tables": len(tables_to_count),
                "total_records": total_records,
                "table_counts": table_counts,
                "estimated_time_minutes": round(estimated_minutes, 2)
            }

        except Exception as e:
            logger.error(f"Failed to get migration statistics: {e}")
            return {
                "total_tables": 0,
                "total_records": 0,
                "table_counts": {},
                "estimated_time_minutes": 0,
                "error": str(e)
            }


# Global migration service instance
migration_service = DatabaseMigrationService()
