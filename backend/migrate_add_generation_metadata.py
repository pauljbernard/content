"""
Migration script to add generation metadata columns to content table.
Run this once to update the database schema.
"""
import sqlite3

def migrate():
    # Connect to database
    conn = sqlite3.connect('content.db')
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(content)")
        columns = [col[1] for col in cursor.fetchall()]

        # Add generated_by_agent column if it doesn't exist
        if 'generated_by_agent' not in columns:
            print("Adding generated_by_agent column...")
            cursor.execute("ALTER TABLE content ADD COLUMN generated_by_agent VARCHAR")
            print("✓ Added generated_by_agent column")
        else:
            print("✓ generated_by_agent column already exists")

        # Add generated_using_skills column if it doesn't exist
        if 'generated_using_skills' not in columns:
            print("Adding generated_using_skills column...")
            cursor.execute("ALTER TABLE content ADD COLUMN generated_using_skills TEXT")
            print("✓ Added generated_using_skills column")
        else:
            print("✓ generated_using_skills column already exists")

        # Commit changes
        conn.commit()
        print("\n✅ Migration completed successfully!")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
