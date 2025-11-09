"""
Test migration workflow with fixed background task issue.
"""
import requests
import time
import json

# Test configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "email": "admin@hmhco.com",
    "password": "changeme"
}

def get_auth_token():
    """Login and get auth token."""
    response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]}
    )
    response.raise_for_status()
    return response.json()["access_token"]

def test_migration():
    """Test the migration workflow."""
    print("=" * 60)
    print("Testing Database Migration (Fixed Background Task)")
    print("=" * 60)

    # Get auth token
    print("\n1. Authenticating...")
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Read config IDs from temp files
    with open("/tmp/source_config_id.txt", "r") as f:
        source_config_id = f.read().strip()

    with open("/tmp/test_config_id.txt", "r") as f:
        target_config_id = f.read().strip()

    print(f"   Source Config ID: {source_config_id}")
    print(f"   Target Config ID: {target_config_id}")

    # Clear target database first
    print("\n2. Clearing target database...")
    import sqlite3
    conn = sqlite3.connect("/Users/colossus/development/content/backend/test_content.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = cursor.fetchall()
    for table in tables:
        if table[0] not in ["database_configs", "migration_jobs"]:
            cursor.execute(f"DELETE FROM {table[0]}")
    conn.commit()
    conn.close()
    print("   ✓ Target database cleared")

    # Start migration
    print("\n3. Starting migration...")
    migration_data = {
        "source_config_id": source_config_id,
        "target_config_id": target_config_id,
        "generate_embeddings": False,
        "tables": None  # All tables
    }

    response = requests.post(
        f"{BASE_URL}/migrations",
        headers=headers,
        json=migration_data
    )
    response.raise_for_status()
    job = response.json()
    job_id = job["id"]

    print(f"   ✓ Migration job started: {job_id}")
    print(f"     Status: {job['status']}")

    # Monitor progress
    print("\n4. Monitoring migration progress...")
    max_wait = 60  # 60 seconds max
    check_interval = 2  # Check every 2 seconds

    for i in range(max_wait // check_interval):
        time.sleep(check_interval)

        response = requests.get(
            f"{BASE_URL}/migrations/{job_id}",
            headers=headers
        )
        response.raise_for_status()
        job = response.json()

        status = job["status"]
        progress = job["progress_pct"]
        migrated = job["migrated_records"]
        total = job["total_records"]
        current_table = job.get("current_table", "None")

        print(f"   [{progress}%] {migrated}/{total} records | Table: {current_table}")

        if status in ["completed", "completed_with_errors", "failed"]:
            print(f"\n   ✓ Migration {status}")
            if job.get("error_log"):
                print(f"   Error log: {job['error_log']}")
            break
    else:
        print(f"\n   ⚠ Migration still running after {max_wait} seconds...")
        print(f"     Final status: {job['status']}")
        print(f"     Progress: {job['progress_pct']}%")

    # Verify migrated data
    print("\n5. Verifying migrated data...")
    conn = sqlite3.connect("/Users/colossus/development/content/backend/test_content.db")
    cursor = conn.cursor()

    # Check content_instances count
    cursor.execute("SELECT COUNT(*) FROM content_instances")
    count = cursor.fetchone()[0]

    print(f"   Target database has {count} content instances")

    if count > 0:
        print("   ✓ Migration successful!")
    else:
        print("   ✗ Migration failed - no data copied")

    conn.close()

    return job

if __name__ == "__main__":
    try:
        result = test_migration()
        print("\n" + "=" * 60)
        print("Migration Test Complete")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
