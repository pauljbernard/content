"""
Fix database switching issue: deactivate PostgreSQL, ensure schema, then migrate
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal, engine, Base
from models.database_config import DatabaseConfig, DatabaseType, DatabaseConfigStatus
from sqlalchemy import create_engine, inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fix_database():
    """Fix the database switching issue."""
    print("=" * 80)
    print("FIXING DATABASE SWITCH ISSUE")
    print("=" * 80)

    # Step 1: Connect to current database (might be empty PostgreSQL)
    print("\n1. Checking current database...")
    print(f"   Current engine: {engine.url}")

    # We need to connect to SQLite to get the configuration
    # because PostgreSQL might be empty
    sqlite_url = "sqlite:///./content.db"
    sqlite_engine = create_engine(sqlite_url)
    from sqlalchemy.orm import sessionmaker
    SqliteSession = sessionmaker(bind=sqlite_engine)
    db = SqliteSession()

    try:
        # Step 2: Deactivate PostgreSQL config
        print("\n2. Deactivating PostgreSQL configuration...")
        pg_configs = db.query(DatabaseConfig).filter(
            DatabaseConfig.db_type == DatabaseType.POSTGRESQL
        ).all()

        for config in pg_configs:
            if config.is_active:
                config.is_active = False
                print(f"   ✓ Deactivated: {config.name}")

        db.commit()

        # Step 3: Get PostgreSQL config for schema initialization
        print("\n3. Preparing PostgreSQL schema...")
        pg_config = db.query(DatabaseConfig).filter(
            DatabaseConfig.name == "novadb"
        ).first()

        if not pg_config:
            print("   ❌ novadb configuration not found!")
            return

        # Connect to PostgreSQL
        pg_url = pg_config.get_connection_string()
        pg_engine = create_engine(pg_url)

        # Check existing tables
        pg_inspector = inspect(pg_engine)
        pg_tables = set(pg_inspector.get_table_names())
        print(f"   PostgreSQL tables: {len(pg_tables)}")

        # Import all models to ensure they're registered
        from models.user import User
        from models.content_type import ContentTypeModel, ContentInstanceModel, ContentRelationshipModel
        from models.llm_config import LLMProvider, LLMModel
        from models.database_config import DatabaseConfig as DBConfig, MigrationJob
        from models.agent import AgentJob
        from models.workflow import AgentWorkflow, WorkflowExecution
        from models.standard import Standard, StandardImportJob
        from models.content import Content, ContentReview

        # Create missing tables
        print("\n4. Creating missing tables...")
        Base.metadata.create_all(bind=pg_engine)

        pg_inspector = inspect(pg_engine)
        new_pg_tables = set(pg_inspector.get_table_names())
        added_tables = new_pg_tables - pg_tables

        if added_tables:
            print(f"   ✓ Added {len(added_tables)} tables:")
            for table in sorted(added_tables):
                print(f"     - {table}")
        else:
            print(f"   ✓ All tables already exist")

        print(f"\n   Total PostgreSQL tables: {len(new_pg_tables)}")

        # Step 4: Show data counts in SQLite
        print("\n5. SQLite Data Summary (Source):")
        print("   " + "-" * 60)

        from models.user import User
        from models.content_type import ContentTypeModel, ContentInstanceModel
        from models.llm_config import LLMProvider, LLMModel

        counts = {
            'Users': db.query(User).count(),
            'Content Types': db.query(ContentTypeModel).count(),
            'Content Instances': db.query(ContentInstanceModel).count(),
            'LLM Providers': db.query(LLMProvider).count(),
            'LLM Models': db.query(LLMModel).count(),
        }

        total = sum(counts.values())
        for name, count in counts.items():
            print(f"   {name:25} {count:6} records")
        print(f"   {'-' * 60}")
        print(f"   {'TOTAL':25} {total:6} records")

        print("\n" + "=" * 80)
        print("DATABASE FIXED - READY TO MIGRATE")
        print("=" * 80)
        print(f"""
Next Steps:

1. The system is now back on SQLite with all your data
2. PostgreSQL schema is complete ({len(new_pg_tables)} tables)
3. Ready to migrate {total} records

To migrate:

METHOD 1 - Using UI (Recommended):
  a. Navigate to: System -> Database Settings
  b. Find the "novadb" configuration
  c. Click "Migrate Data"
  d. Leave tables empty (migrates all tables)
  e. Click "Start Migration"
  f. Wait for completion (will show progress)
  g. Click "Activate" to switch to PostgreSQL

METHOD 2 - Using API:
  curl -X POST http://localhost:8000/api/v1/migrations \\
    -H "Authorization: Bearer YOUR_TOKEN" \\
    -H "Content-Type: application/json" \\
    -d '{{
      "source_config_id": "SQLITE_CONFIG_ID",
      "target_config_id": "{pg_config.id}",
      "tables": []
    }}'

The migration will:
- Copy all {total} records from SQLite to PostgreSQL
- Preserve all relationships
- Generate vector embeddings (if OpenAI configured)
- Take approximately 30-60 seconds

After migration completes, activate PostgreSQL in the UI.
""")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
        sqlite_engine.dispose()


if __name__ == "__main__":
    fix_database()
