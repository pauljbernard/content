"""
Rollback script to remove generation metadata columns from content table.
Run this to undo the previous migration.
"""
import sqlite3

def rollback():
    # Connect to database
    conn = sqlite3.connect('content.db')
    cursor = conn.cursor()

    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(content)")
        columns = [col[1] for col in cursor.fetchall()]

        # Note: SQLite doesn't support DROP COLUMN directly in older versions
        # We need to recreate the table without these columns

        if 'generated_by_agent' in columns or 'generated_using_skills' in columns:
            print("Removing generation metadata columns...")

            # Get all other columns
            cursor.execute("PRAGMA table_info(content)")
            all_columns = cursor.fetchall()

            # Filter out the columns we want to remove
            keep_columns = [col for col in all_columns if col[1] not in ['generated_by_agent', 'generated_using_skills']]
            column_names = [col[1] for col in keep_columns]
            column_defs = [f"{col[1]} {col[2]}" + (" PRIMARY KEY" if col[5] else "") + (" NOT NULL" if col[3] else "") for col in keep_columns]

            # Create temporary table without the unwanted columns
            cursor.execute(f"""
                CREATE TABLE content_temp (
                    {', '.join(column_defs)}
                )
            """)

            # Copy data
            cursor.execute(f"""
                INSERT INTO content_temp ({', '.join(column_names)})
                SELECT {', '.join(column_names)} FROM content
            """)

            # Drop old table and rename temp
            cursor.execute("DROP TABLE content")
            cursor.execute("ALTER TABLE content_temp RENAME TO content")

            print("✓ Removed generation metadata columns")
        else:
            print("✓ Columns already removed or don't exist")

        # Commit changes
        conn.commit()
        print("\n✅ Rollback completed successfully!")

    except Exception as e:
        print(f"\n❌ Rollback failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    rollback()
