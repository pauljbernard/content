#!/usr/bin/env python3
"""
Re-import Georgia Math and Science standards with hierarchical structure.

This script deletes and re-imports the Math and Science standards
to add grade-level-based hierarchical structure.
"""

import requests
import time
import sys

# API Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

# Login credentials
LOGIN_EMAIL = "admin@hmhco.com"
LOGIN_PASSWORD = "changeme"

# Georgia CASE API base URL
GEORGIA_CASE_BASE = "https://case.georgiastandards.org/ims/case/v1p0"

# Standards to re-import
GEORGIA_STANDARDS = [
    {
        "identifier": "e9dd7229-3558-4df2-85c6-57b8938f6180",
        "name": "Georgia Standards of Excellence - Mathematics (SY2023-2024)",
        "short_name": "GSE Mathematics",
        "code": "GSE-MATH-GA",
        "subject": "mathematics",
        "description": "K-12 Mathematics standards",
    },
    {
        "identifier": "27a08dc6-416e-11e7-ba71-02bd89fdd987",
        "name": "Georgia Standards of Excellence - Science",
        "short_name": "GSE Science",
        "code": "GSE-SCI-GA",
        "subject": "science",
        "description": "K-12 Science standards plus advanced high school courses",
    },
]


def login():
    """Authenticate and get access token"""
    print("Logging in...")
    response = requests.post(
        f"{API_BASE}/auth/login",
        data={"username": LOGIN_EMAIL, "password": LOGIN_PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        sys.exit(1)

    data = response.json()
    token = data.get("access_token")
    print(f"✓ Logged in successfully")
    return token


def find_standard_by_code(token, code):
    """Find a standard by its code"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/standards/", headers=headers)

    if response.status_code != 200:
        print(f"Failed to list standards: {response.status_code}")
        return None

    standards = response.json()
    for std in standards:
        if std.get("code") == code:
            return std.get("id")

    return None


def delete_standard(token, standard_id, name):
    """Delete a standard by ID"""
    print(f"  Deleting existing standard (ID: {standard_id})...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(
        f"{API_BASE}/standards/{standard_id}",
        headers=headers,
    )

    if response.status_code == 204:
        print(f"  ✓ Deleted {name}")
        return True
    else:
        print(f"  ✗ Failed to delete: {response.status_code}")
        print(response.text)
        return False


def create_import_job(token, standard):
    """Create an import job for a Georgia standard"""
    print(f"\nImporting: {standard['name']}")

    # Construct CASE API URL
    case_url = f"{GEORGIA_CASE_BASE}/CFPackages/{standard['identifier']}"

    import_data = {
        "source_type": "api",
        "source_location": case_url,
        "format": "case",
        "name": standard["name"],
        "short_name": standard["short_name"],
        "code": standard["code"],
        "type": "state",
        "subject": standard["subject"],
        "source_organization": "Georgia Department of Education",
        "state": "georgia",
        "district": "",
        "country": "United States",
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{API_BASE}/standards/import",
        json=import_data,
        headers=headers,
    )

    if response.status_code != 201:
        print(f"✗ Import failed: {response.status_code}")
        print(response.text)
        return None

    job = response.json()
    job_id = job.get("id")
    print(f"✓ Import job created: #{job_id}")
    return job_id


def poll_job_status(token, job_id, max_wait=300):
    """Poll import job status until complete or failed"""
    headers = {"Authorization": f"Bearer {token}"}
    start_time = time.time()
    last_status = None
    last_progress = None

    while (time.time() - start_time) < max_wait:
        response = requests.get(
            f"{API_BASE}/standards/import/{job_id}",
            headers=headers,
        )

        if response.status_code != 200:
            print(f"✗ Failed to get job status: {response.status_code}")
            return False

        job = response.json()
        status = job.get("status")
        progress = job.get("progress_percentage", 0)
        message = job.get("progress_message", "")

        # Only print if status or progress changed
        if status != last_status or progress != last_progress:
            print(f"  Status: {status} ({progress}%) - {message}")
            last_status = status
            last_progress = progress

        if status == "completed":
            standards_count = job.get("standards_extracted", 0)
            standard_id = job.get("standard_id")
            print(f"✓ Import completed! Imported {standards_count} standards (ID: {standard_id})")
            return True
        elif status == "failed":
            error = job.get("error_message", "Unknown error")
            print(f"✗ Import failed: {error}")
            return False
        elif status in ["queued", "running"]:
            time.sleep(2)  # Poll every 2 seconds
        else:
            print(f"✗ Unknown status: {status}")
            return False

    print(f"✗ Import timed out after {max_wait} seconds")
    return False


def main():
    """Main re-import process"""
    print("=" * 70)
    print("Georgia Math & Science - Re-import with Hierarchical Structure")
    print("=" * 70)
    print(f"\nRe-importing {len(GEORGIA_STANDARDS)} standards with grade-level hierarchy")
    print()

    # Login
    token = login()

    # Process each standard
    results = []
    for i, standard in enumerate(GEORGIA_STANDARDS, 1):
        print(f"\n[{i}/{len(GEORGIA_STANDARDS)}] {standard['short_name']}")
        print("-" * 70)

        # Check if standard exists
        existing_id = find_standard_by_code(token, standard["code"])
        if existing_id:
            delete_success = delete_standard(token, existing_id, standard["short_name"])
            if not delete_success:
                results.append((standard['short_name'], False, "Failed to delete existing"))
                continue
            time.sleep(1)  # Brief pause after delete

        # Import
        job_id = create_import_job(token, standard)
        if job_id is None:
            results.append((standard['short_name'], False, "Failed to create job"))
            continue

        success = poll_job_status(token, job_id, max_wait=300)
        results.append((standard['short_name'], success, "Success" if success else "Failed"))

        # Wait between imports
        if i < len(GEORGIA_STANDARDS):
            time.sleep(3)

    # Print summary
    print("\n" + "=" * 70)
    print("RE-IMPORT SUMMARY")
    print("=" * 70)

    success_count = sum(1 for _, success, _ in results if success)
    failed_count = len(results) - success_count

    for name, success, message in results:
        status = "✓" if success else "✗"
        print(f"{status} {name}: {message}")

    print()
    print(f"Total: {len(results)} | Success: {success_count} | Failed: {failed_count}")
    print()

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
