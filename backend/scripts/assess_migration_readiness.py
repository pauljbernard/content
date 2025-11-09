"""
Assess readiness for migrating from SQLite to PostgreSQL
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal, engine
from models.database_config import DatabaseConfig, MigrationJob, DatabaseConfigStatus, DatabaseType
from models.user import User
from models.content_type import ContentTypeModel, ContentInstanceModel
from models.llm_config import LLMProvider, LLMModel
from sqlalchemy import create_engine, inspect, text
import psycopg2


def assess_readiness():
    """Comprehensive migration readiness assessment."""
    print("=" * 80)
    print("DATABASE MIGRATION READINESS ASSESSMENT")
    print("=" * 80)

    db = SessionLocal()
    issues = []
    warnings = []

    try:
        # 1. Check source database (SQLite)
        print("\n1. SOURCE DATABASE (SQLite)")
        print("-" * 80)

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✓ Tables: {len(tables)}")

        # Count critical data
        user_count = db.query(User).count()
        content_type_count = db.query(ContentTypeModel).count()
        content_instance_count = db.query(ContentInstanceModel).count()
        provider_count = db.query(LLMProvider).count()
        model_count = db.query(LLMModel).count()

        print(f"✓ Users: {user_count}")
        print(f"✓ Content Types: {content_type_count}")
        print(f"✓ Content Instances: {content_instance_count}")
        print(f"✓ LLM Providers: {provider_count}")
        print(f"✓ LLM Models: {model_count}")

        total_records = user_count + content_type_count + content_instance_count + provider_count + model_count
        print(f"\n  TOTAL CRITICAL RECORDS: {total_records}")

        # 2. Check target database configuration
        print("\n2. TARGET DATABASE (PostgreSQL)")
        print("-" * 80)

        pg_config = db.query(DatabaseConfig).filter(
            DatabaseConfig.db_type == DatabaseType.POSTGRESQL
        ).first()

        if not pg_config:
            issues.append("❌ No PostgreSQL configuration found!")
            print("❌ No PostgreSQL configuration found")
        else:
            print(f"✓ Configuration found: {pg_config.name}")
            print(f"  Host: {pg_config.host}:{pg_config.port}")
            print(f"  Database: {pg_config.database_name}")
            print(f"  Status: {pg_config.status}")
            print(f"  pgvector enabled: {pg_config.pgvector_enabled}")

            if pg_config.status != DatabaseConfigStatus.TESTED:
                issues.append(f"❌ PostgreSQL status is {pg_config.status}, should be TESTED")

            # 3. Test PostgreSQL connection
            print("\n3. POSTGRESQL CONNECTION TEST")
            print("-" * 80)

            try:
                conn_str = pg_config.get_connection_string()
                pg_engine = create_engine(conn_str)

                with pg_engine.connect() as conn:
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"✓ Connection successful")
                    print(f"  PostgreSQL version: {version.split(',')[0]}")

                    # Check if pgvector is installed
                    result = conn.execute(text(
                        "SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector'"
                    ))
                    pgvector_installed = result.fetchone()[0] > 0

                    if pgvector_installed:
                        print(f"✓ pgvector extension installed")
                    else:
                        if pg_config.pgvector_enabled:
                            issues.append("❌ pgvector enabled in config but extension not installed in database")
                            print(f"❌ pgvector extension NOT installed (but enabled in config)")
                        else:
                            warnings.append("⚠ pgvector not installed (semantic search will be unavailable)")
                            print(f"⚠ pgvector extension not installed")

                    # Check if schema exists
                    pg_inspector = inspect(pg_engine)
                    pg_tables = pg_inspector.get_table_names()
                    print(f"\n  PostgreSQL tables: {len(pg_tables)}")

                    if len(pg_tables) == 0:
                        warnings.append("⚠ PostgreSQL database is empty - schema needs to be initialized")
                        print(f"  ⚠ Database is empty (schema initialization will be required)")
                    elif len(pg_tables) < len(tables):
                        warnings.append(f"⚠ PostgreSQL has {len(pg_tables)} tables but SQLite has {len(tables)}")
                        print(f"  ⚠ PostgreSQL has fewer tables than SQLite")
                    else:
                        print(f"  ✓ PostgreSQL schema appears initialized")

                        # Check if there's existing data
                        try:
                            result = conn.execute(text("SELECT COUNT(*) FROM users"))
                            pg_users = result.fetchone()[0]
                            if pg_users > 0:
                                warnings.append(f"⚠ PostgreSQL already contains {pg_users} users - migration may conflict")
                                print(f"  ⚠ PostgreSQL contains {pg_users} existing users")
                        except:
                            pass

            except Exception as e:
                issues.append(f"❌ PostgreSQL connection failed: {e}")
                print(f"❌ Connection failed: {e}")

        # 4. Check previous migration jobs
        print("\n4. MIGRATION HISTORY")
        print("-" * 80)

        jobs = db.query(MigrationJob).all()
        if jobs:
            print(f"Found {len(jobs)} previous migration job(s):")
            for job in jobs:
                print(f"\n  Job {job.id}:")
                print(f"    Status: {job.status}")
                print(f"    Progress: {job.progress_pct}%")
                print(f"    Records: {job.migrated_records}/{job.total_records}")

                if job.status == "pending":
                    warnings.append(f"⚠ Found pending migration job {job.id}")
                elif job.status == "failed":
                    warnings.append(f"⚠ Found failed migration job {job.id}")
        else:
            print("No previous migration jobs")

        # 5. Check application dependencies
        print("\n5. APPLICATION DEPENDENCIES")
        print("-" * 80)

        # Check if application is currently running
        import subprocess
        try:
            result = subprocess.run(['lsof', '-i', ':8000'], capture_output=True, text=True)
            if result.returncode == 0:
                warnings.append("⚠ Application appears to be running on port 8000")
                print("⚠ Application is currently running on port 8000")
                print("  Recommendation: Stop application before migration")
            else:
                print("✓ Application not detected on port 8000")
        except:
            print("  (Could not check if application is running)")

        # 6. Check critical constraints
        print("\n6. CRITICAL CONSTRAINTS CHECK")
        print("-" * 80)

        # Check for content instances without content types
        orphaned_instances = db.execute(text("""
            SELECT COUNT(*) FROM content_instances ci
            WHERE NOT EXISTS (
                SELECT 1 FROM content_types ct WHERE ct.id = ci.content_type_id
            )
        """)).fetchone()[0]

        if orphaned_instances > 0:
            issues.append(f"❌ Found {orphaned_instances} orphaned content instances")
            print(f"❌ Found {orphaned_instances} orphaned content instances (no matching content type)")
        else:
            print(f"✓ No orphaned content instances")

        # Check for LLM models without providers
        orphaned_models = db.execute(text("""
            SELECT COUNT(*) FROM llm_models m
            WHERE NOT EXISTS (
                SELECT 1 FROM llm_providers p WHERE p.id = m.provider_id
            )
        """)).fetchone()[0]

        if orphaned_models > 0:
            issues.append(f"❌ Found {orphaned_models} orphaned LLM models")
            print(f"❌ Found {orphaned_models} orphaned LLM models (no matching provider)")
        else:
            print(f"✓ No orphaned LLM models")

        # Summary
        print("\n" + "=" * 80)
        print("ASSESSMENT SUMMARY")
        print("=" * 80)

        if issues:
            print("\n❌ CRITICAL ISSUES (must fix before migration):")
            for issue in issues:
                print(f"  {issue}")

        if warnings:
            print("\n⚠ WARNINGS (should review):")
            for warning in warnings:
                print(f"  {warning}")

        if not issues and not warnings:
            print("\n✓✓✓ ALL CHECKS PASSED - READY FOR MIGRATION ✓✓✓")
        elif not issues:
            print("\n✓ No critical issues - READY with warnings")
        else:
            print(f"\n❌ NOT READY - {len(issues)} critical issue(s) must be fixed")

        # Recommendations
        print("\n" + "=" * 80)
        print("MIGRATION RECOMMENDATIONS")
        print("=" * 80)

        if not issues:
            print("""
1. BACKUP: Create a backup of your current SQLite database
   cp content.db content.db.backup

2. STOP APPLICATION: Ensure the application is not running

3. INITIALIZE SCHEMA (if needed): Run schema initialization on PostgreSQL

4. RUN MIGRATION: Use the Database Settings UI or API to start migration
   - This will migrate all {total_records} records
   - Vector embeddings will be generated (requires OpenAI API key if configured)

5. VERIFY: Check the migration job status in the UI

6. ACTIVATE: Set the PostgreSQL config as active once migration completes

7. TEST: Thoroughly test all functionality before committing to PostgreSQL

8. ROLLBACK PLAN: Keep SQLite backup for at least 7 days
            """.format(total_records=total_records))
        else:
            print("\nFix critical issues before proceeding with migration.")

    finally:
        db.close()


if __name__ == "__main__":
    assess_readiness()
