"""
Prepare for migration: clean up pending jobs and ensure schema is ready
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.database_config import DatabaseConfig, MigrationJob, DatabaseType
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


def prepare_migration():
    """Prepare the database for migration."""
    print("=" * 80)
    print("PREPARING FOR MIGRATION")
    print("=" * 80)

    db = SessionLocal()

    try:
        # 1. Clean up pending migration jobs
        print("\n1. Cleaning up pending migration jobs...")
        pending_jobs = db.query(MigrationJob).filter(MigrationJob.status == "pending").all()

        if pending_jobs:
            for job in pending_jobs:
                print(f"   Deleting pending job: {job.id}")
                db.delete(job)
            db.commit()
            print(f"   ✓ Deleted {len(pending_jobs)} pending job(s)")
        else:
            print("   ✓ No pending jobs to clean up")

        # 2. Get PostgreSQL config
        print("\n2. Getting PostgreSQL configuration...")
        pg_config = db.query(DatabaseConfig).filter(
            DatabaseConfig.db_type == DatabaseType.POSTGRESQL
        ).first()

        if not pg_config:
            print("   ❌ No PostgreSQL configuration found!")
            return

        print(f"   ✓ Found config: {pg_config.name}")

        # 3. Ensure schema is initialized
        print("\n3. Checking PostgreSQL schema...")
        conn_str = pg_config.get_connection_string()
        pg_engine = create_engine(conn_str)

        with pg_engine.connect() as conn:
            # Get list of existing tables
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            pg_tables = [row[0] for row in result]

            print(f"   PostgreSQL tables ({len(pg_tables)}):")
            for table in pg_tables:
                print(f"     - {table}")

            # Check for missing critical tables
            critical_tables = [
                'users',
                'content_types',
                'content_instances',
                'llm_providers',
                'llm_models',
                'database_configs',
                'migration_jobs'
            ]

            missing_tables = [t for t in critical_tables if t not in pg_tables]

            if missing_tables:
                print(f"\n   ⚠ Missing critical tables:")
                for table in missing_tables:
                    print(f"     - {table}")
                print("\n   Run schema initialization first!")
                print("   Use the Database Settings UI -> Initialize Schema button")
            else:
                print(f"\n   ✓ All critical tables present")

        # 4. Show migration command
        print("\n" + "=" * 80)
        print("READY TO MIGRATE")
        print("=" * 80)
        print(f"""
Database is prepared for migration.

To proceed:

1. STOP the application:
   pkill -f "uvicorn main:app"

2. BACKUP your SQLite database:
   cp content.db content.db.backup-$(date +%Y%m%d-%H%M%S)

3. Use the Database Settings UI:
   - Navigate to System -> Database Settings
   - Click "Migrate Data" on the novadb configuration
   - Select tables to migrate (or leave empty for all)
   - Click "Start Migration"

4. Monitor progress in the UI

5. Once complete, activate PostgreSQL:
   - Click "Activate" on the novadb configuration
   - Application will restart with PostgreSQL

Statistics:
- Source: SQLite with 958 records
- Target: PostgreSQL (novadb) at {pg_config.host}:{pg_config.port}
- pgvector: {"Enabled" if pg_config.pgvector_enabled else "Disabled"}
""".format(pg_config=pg_config))

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    prepare_migration()
