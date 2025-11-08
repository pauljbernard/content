"""
Delete all legacy content records from the old content system.
This script removes all records from the 'content' table (old hard-coded system)
while preserving the new content_instances table (new dynamic system).
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from core.config import settings

def delete_legacy_content():
    """Delete all legacy content records."""
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        # Check if content table exists
        result = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='content'"
        ))

        if result.fetchone():
            # Get count of records before deletion
            count_result = conn.execute(text("SELECT COUNT(*) FROM content"))
            count = count_result.fetchone()[0]

            print(f"Found {count} legacy content records in the database")

            if count > 0:
                # Ask for confirmation
                response = input(f"Are you sure you want to delete {count} legacy content records? (yes/no): ")

                if response.lower() == 'yes':
                    # Check if reviews table exists
                    reviews_table = conn.execute(text(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name='reviews'"
                    ))

                    if reviews_table.fetchone():
                        # Delete reviews related to legacy content first
                        conn.execute(text("DELETE FROM reviews WHERE content_id IN (SELECT id FROM content)"))
                        reviews_deleted = conn.execute(text("SELECT changes()")).fetchone()[0]
                        print(f"Deleted {reviews_deleted} related reviews")

                    # Delete all content records
                    conn.execute(text("DELETE FROM content"))
                    conn.commit()

                    print(f"✅ Successfully deleted {count} legacy content records")
                    print("The 'content' table structure remains for backwards compatibility")
                else:
                    print("❌ Deletion cancelled")
            else:
                print("✅ No legacy content records found - database is already clean")
        else:
            print("✅ Legacy 'content' table does not exist - nothing to delete")

if __name__ == "__main__":
    print("=" * 60)
    print("Legacy Content Deletion Script")
    print("=" * 60)
    print("\nThis script will delete all records from the old 'content' table.")
    print("The new content_instances table will NOT be affected.\n")

    try:
        delete_legacy_content()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
