#!/usr/bin/env python3
"""
Content Instance Embeddings Management Script

Initializes and maintains vector embeddings for content instances.

Usage:
    python scripts/manage_content_embeddings.py init         # Initialize embedding column and indexes
    python scripts/manage_content_embeddings.py index        # Generate embeddings for instances without them
    python scripts/manage_content_embeddings.py reindex      # Force regenerate all embeddings
    python scripts/manage_content_embeddings.py status       # Show embedding status
"""
import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.session import SessionLocal
from services.vector_search import get_vector_search_service
from models.content_type import ContentTypeModel, ContentInstanceModel
from sqlalchemy import text


async def init_embeddings():
    """Initialize embedding column and vector indexes for all content types."""
    print("=" * 70)
    print("CONTENT INSTANCE EMBEDDINGS INITIALIZATION")
    print("=" * 70)
    print()

    db = SessionLocal()
    try:
        vector_service = get_vector_search_service(db)

        print("Step 1: Ensuring embedding column exists...")
        success = await vector_service.add_embedding_column(
            db=db,
            table_name="content_instances",
            create_global_index=False  # Use per-content-type indexes instead
        )

        if not success:
            print("\n" + "=" * 70)
            print("❌ INITIALIZATION FAILED")
            print("=" * 70)
            print("\nPlease check:")
            print("  1. PostgreSQL with pgvector extension is installed")
            print("  2. Database connection is configured correctly")
            print("  3. User has permissions to create columns/indexes")
            return

        print("✓ Embedding column created")

        print("\nStep 2: Creating vector indexes for all content types...")
        # Get all content types
        content_types = db.query(ContentTypeModel).all()
        print(f"Found {len(content_types)} content types")

        created_count = 0
        failed_count = 0

        for ct in content_types:
            try:
                success = await vector_service.create_content_type_vector_index(
                    db=db,
                    content_type_id=ct.id
                )
                if success:
                    created_count += 1
                    print(f"  ✓ Created index for: {ct.name}")
                else:
                    failed_count += 1
                    print(f"  ❌ Failed to create index for: {ct.name}")
            except Exception as e:
                failed_count += 1
                print(f"  ❌ Error creating index for {ct.name}: {e}")

        print(f"\n✓ Created {created_count} vector indexes, {failed_count} failed")

        print("\n" + "=" * 70)
        print("✓ INITIALIZATION COMPLETE")
        print("=" * 70)
        print("\nYou can now generate embeddings with:")
        print("  python scripts/manage_content_embeddings.py index")

    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


async def index_embeddings(force_reindex=False):
    """Generate embeddings for all content instances."""
    print("=" * 70)
    print("CONTENT INSTANCE EMBEDDING GENERATION")
    print("=" * 70)
    print()

    db = SessionLocal()
    try:
        vector_service = get_vector_search_service(db)

        def progress_callback(stats):
            """Print progress updates."""
            print(f"\rProgress: {stats['progress_pct']}% ({stats['processed']}/{stats['total']}) - "
                  f"Generated: {stats['generated']}, Failed: {stats['failed']}", end='')

        print("Starting embedding generation...")
        if force_reindex:
            print("(Force re-index enabled - will regenerate all embeddings)")
            # Clear all embeddings first
            db.execute(text("UPDATE content_instances SET embedding = NULL"))
            db.commit()
        print()

        stats = await vector_service.batch_generate_embeddings(
            db=db,
            batch_size=10,
            progress_callback=progress_callback
        )

        print("\n")
        print("=" * 70)
        print("EMBEDDING GENERATION COMPLETE")
        print("=" * 70)
        print(f"Total instances: {stats['total']}")
        print(f"Generated: {stats['generated']}")
        print(f"Failed: {stats['failed']}")

        if stats.get('error'):
            print(f"\n❌ Error: {stats['error']}")

    except Exception as e:
        print(f"\n❌ Error during embedding generation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def show_status():
    """Show embedding status."""
    print("=" * 70)
    print("CONTENT INSTANCE EMBEDDING STATUS")
    print("=" * 70)
    print()

    db = SessionLocal()
    try:
        # Check if embedding column exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns
                WHERE table_name = 'content_instances'
                AND column_name = 'embedding'
            )
        """))
        embedding_exists = result.scalar()

        print("Table Status:")
        print(f"  embedding column: {'✓ Exists' if embedding_exists else '❌ Missing'}")
        print()

        if not embedding_exists:
            print("❌ Embedding column does not exist")
            print("\nRun initialization first:")
            print("  python scripts/manage_content_embeddings.py init")
            return

        # Get instance counts
        result = db.execute(text("""
            SELECT
                COUNT(*) as total,
                COUNT(embedding) as with_embeddings,
                COUNT(*) - COUNT(embedding) as without_embeddings
            FROM content_instances
        """))
        row = result.fetchone()

        if row and row[0] > 0:
            total, with_emb, without_emb = row
            pct_complete = (with_emb / total * 100) if total > 0 else 0

            print("Embeddings Status:")
            print(f"  Total instances: {total}")
            print(f"  With embeddings: {with_emb} ({pct_complete:.1f}%)")
            print(f"  Without embeddings: {without_emb}")
            print()

            # Breakdown by content type
            result = db.execute(text("""
                SELECT
                    ct.name as content_type,
                    COUNT(ci.id) as total,
                    COUNT(ci.embedding) as with_embeddings
                FROM content_instances ci
                JOIN content_types ct ON ci.content_type_id = ct.id
                GROUP BY ct.name
                ORDER BY total DESC
            """))

            print("By Content Type:")
            for ct_row in result:
                ct_name, ct_total, ct_with_emb = ct_row
                ct_pct = (ct_with_emb / ct_total * 100) if ct_total > 0 else 0
                print(f"  {ct_name}: {ct_with_emb}/{ct_total} ({ct_pct:.1f}%)")

            # Check vector indexes
            print("\nVector Indexes:")
            result = db.execute(text("""
                SELECT indexname
                FROM pg_indexes
                WHERE tablename = 'content_instances'
                AND indexname LIKE 'content_instances_embedding_ct_%'
                ORDER BY indexname
            """))

            indexes = result.fetchall()
            if indexes:
                print(f"  {len(indexes)} content type indexes created")
                for idx in indexes[:5]:  # Show first 5
                    print(f"    • {idx[0]}")
                if len(indexes) > 5:
                    print(f"    ... and {len(indexes) - 5} more")
            else:
                print("  ❌ No content type indexes found")
                print("  Run: python scripts/manage_content_embeddings.py init")

        else:
            print("No content instances exist yet")

        if without_emb and without_emb > 0:
            print("\n💡 Tip: Generate missing embeddings with:")
            print("  python scripts/manage_content_embeddings.py index")

    except Exception as e:
        print(f"❌ Error checking status: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/manage_content_embeddings.py init      # Initialize column and indexes")
        print("  python scripts/manage_content_embeddings.py index     # Generate missing embeddings")
        print("  python scripts/manage_content_embeddings.py reindex   # Force regenerate all embeddings")
        print("  python scripts/manage_content_embeddings.py status    # Show embedding status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        asyncio.run(init_embeddings())
    elif command == "index":
        asyncio.run(index_embeddings(force_reindex=False))
    elif command == "reindex":
        asyncio.run(index_embeddings(force_reindex=True))
    elif command == "status":
        show_status()
    else:
        print(f"Unknown command: {command}")
        print("\nValid commands: init, index, reindex, status")
        sys.exit(1)


if __name__ == "__main__":
    main()
