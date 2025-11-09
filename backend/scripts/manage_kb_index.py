#!/usr/bin/env python3
"""
Knowledge Base Index Management Script

Initializes and maintains the vector index for knowledge base files.

Usage:
    python scripts/manage_kb_index.py init         # Initialize tables and index
    python scripts/manage_kb_index.py index        # Index all files
    python scripts/manage_kb_index.py reindex      # Force re-index all files
    python scripts/manage_kb_index.py status       # Show index status
"""
import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.session import SessionLocal, engine
from services.knowledge_base_indexer import get_kb_indexer
from models.knowledge_base import KnowledgeBaseEmbeddingModel
from sqlalchemy import text


async def init_index():
    """Initialize tables and vector index."""
    print("=" * 70)
    print("KNOWLEDGE BASE INDEX INITIALIZATION")
    print("=" * 70)
    print()

    db = SessionLocal()
    try:
        indexer = get_kb_indexer(db)

        print("Step 1: Ensuring tables exist...")
        # Tables are created automatically from models
        print("✓ Tables created from models")

        print("\nStep 2: Ensuring vector index exists...")
        success = await indexer.ensure_table_and_index_exist()

        if success:
            print("\n" + "=" * 70)
            print("✓ INITIALIZATION COMPLETE")
            print("=" * 70)
            print("\nYou can now index files with:")
            print("  python scripts/manage_kb_index.py index")
        else:
            print("\n" + "=" * 70)
            print("❌ INITIALIZATION FAILED")
            print("=" * 70)
            print("\nPlease check:")
            print("  1. PostgreSQL with pgvector extension is installed")
            print("  2. Database connection is configured correctly")
            print("  3. User has permissions to create tables/indexes")

    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


async def index_files(force_reindex=False):
    """Index all knowledge base files."""
    print("=" * 70)
    print("KNOWLEDGE BASE INDEXING")
    print("=" * 70)
    print()

    db = SessionLocal()
    try:
        indexer = get_kb_indexer(db)

        def progress_callback(stats):
            """Print progress updates."""
            print(f"\rProgress: {stats['progress_pct']}% ({stats['processed']}/{stats['total']}) - "
                  f"Indexed: {stats['indexed']}, Failed: {stats['failed']}", end='')

        print("Starting indexing...")
        if force_reindex:
            print("(Force re-index enabled - will re-process all files)")
        print()

        stats = await indexer.index_all_files(
            force_reindex=force_reindex,
            progress_callback=progress_callback
        )

        print("\n")
        print("=" * 70)
        print("INDEXING COMPLETE")
        print("=" * 70)
        print(f"Total files: {stats['total']}")
        print(f"Indexed: {stats['indexed']}")
        print(f"Failed: {stats['failed']}")

        if stats.get('error'):
            print(f"\n❌ Error: {stats['error']}")

    except Exception as e:
        print(f"\n❌ Error during indexing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def show_status():
    """Show indexing status."""
    print("=" * 70)
    print("KNOWLEDGE BASE INDEX STATUS")
    print("=" * 70)
    print()

    db = SessionLocal()
    try:
        # Check if table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'knowledge_base_embeddings'
            )
        """))
        table_exists = result.scalar()

        if not table_exists:
            print("❌ Knowledge base embeddings table does not exist")
            print("\nRun initialization first:")
            print("  python scripts/manage_kb_index.py init")
            return

        # Check if embedding column exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns
                WHERE table_name = 'knowledge_base_embeddings'
                AND column_name = 'embedding'
            )
        """))
        embedding_exists = result.scalar()

        print("Table Status:")
        print(f"  knowledge_base_embeddings table: {'✓ Exists' if table_exists else '❌ Missing'}")
        print(f"  embedding column: {'✓ Exists' if embedding_exists else '❌ Missing'}")
        print()

        # Get file counts
        result = db.execute(text("""
            SELECT
                COUNT(*) as total,
                COUNT(embedding) as with_embeddings,
                COUNT(*) - COUNT(embedding) as without_embeddings,
                MAX(last_indexed) as last_indexed
            FROM knowledge_base_embeddings
        """))
        row = result.fetchone()

        if row and row[0] > 0:
            print("Files Indexed:")
            print(f"  Total files: {row[0]}")
            print(f"  With embeddings: {row[1]}")
            print(f"  Without embeddings: {row[2]}")
            print(f"  Last indexed: {row[3]}")
            print()

            # Category breakdown
            result = db.execute(text("""
                SELECT category, COUNT(*) as count
                FROM knowledge_base_embeddings
                GROUP BY category
                ORDER BY count DESC
            """))

            print("By Category:")
            for cat_row in result:
                print(f"  {cat_row[0]}: {cat_row[1]} files")
        else:
            print("No files indexed yet")
            print("\nRun indexing:")
            print("  python scripts/manage_kb_index.py index")

    except Exception as e:
        print(f"❌ Error checking status: {e}")
    finally:
        db.close()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/manage_kb_index.py init      # Initialize tables and index")
        print("  python scripts/manage_kb_index.py index     # Index all files")
        print("  python scripts/manage_kb_index.py reindex   # Force re-index all files")
        print("  python scripts/manage_kb_index.py status    # Show index status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        asyncio.run(init_index())
    elif command == "index":
        asyncio.run(index_files(force_reindex=False))
    elif command == "reindex":
        asyncio.run(index_files(force_reindex=True))
    elif command == "status":
        show_status()
    else:
        print(f"Unknown command: {command}")
        print("\nValid commands: init, index, reindex, status")
        sys.exit(1)


if __name__ == "__main__":
    main()
