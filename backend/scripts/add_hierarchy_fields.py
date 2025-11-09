"""
Add hierarchical content type support fields.

This migration adds:
- is_hierarchical: Boolean flag to mark hierarchical content types
- hierarchy_config: JSON field with hierarchy configuration
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from database.session import engine

def run_migration():
    """Add hierarchical fields to content_types table."""

    with engine.connect() as conn:
        # Check if columns already exist
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'content_types'
            AND column_name IN ('is_hierarchical', 'hierarchy_config')
        """))
        existing_columns = {row[0] for row in result}

        if 'is_hierarchical' not in existing_columns:
            print("Adding is_hierarchical column...")
            conn.execute(text("""
                ALTER TABLE content_types
                ADD COLUMN is_hierarchical BOOLEAN DEFAULT FALSE
            """))
            conn.commit()
            print("✓ Added is_hierarchical column")
        else:
            print("✓ is_hierarchical column already exists")

        if 'hierarchy_config' not in existing_columns:
            print("Adding hierarchy_config column...")
            conn.execute(text("""
                ALTER TABLE content_types
                ADD COLUMN hierarchy_config JSON
            """))
            conn.commit()
            print("✓ Added hierarchy_config column")
        else:
            print("✓ hierarchy_config column already exists")

        # Update CASE Standard content type to be hierarchical
        print("\nConfiguring CASE Standard content type as hierarchical...")
        import json
        config = json.dumps({
            "identifier_field": "identifier",
            "parent_field": "parent",
            "children_field": "children",
            "display_field": "full_statement",
            "secondary_display_field": "human_coding_scheme",
            "supports_lazy_loading": True
        })
        result = conn.execute(text("""
            UPDATE content_types
            SET is_hierarchical = TRUE,
                hierarchy_config = :config
            WHERE name = 'CASE Standard'
            RETURNING id, name
        """), {"config": config})

        updated = result.fetchone()
        if updated:
            conn.commit()
            print(f"✓ Updated '{updated[1]}' (ID: {updated[0]}) to be hierarchical")
        else:
            print("⚠ CASE Standard content type not found (will be configured on first import)")

if __name__ == "__main__":
    print("=" * 60)
    print("Adding Hierarchical Content Type Support")
    print("=" * 60)
    run_migration()
    print("\n✓ Migration complete!")
