#!/usr/bin/env python3
"""
Import Georgia Standards of Excellence from Georgia SuitCASE

This script imports all core academic standards from Georgia's CASE API
into the standards database via the import API.
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

# Core academic standards to import (adopted, current standards)
GEORGIA_STANDARDS = [
    {
        "identifier": "00fcf0e2-b9c3-11e7-a4ad-47f36833e889",
        "name": "Georgia Standards of Excellence - Computer Science",
        "short_name": "GSE Computer Science",
        "code": "GSE-CS-GA",
        "subject": "computer_science",
        "description": "K-12 Computer Science standards blending core concepts with practices",
    },
    {
        "identifier": "391c3abe-c1ec-4a4a-a942-c9e152b35102",
        "name": "Georgia Standards of Excellence - English Language Arts (SY2025-2026)",
        "short_name": "GSE ELA",
        "code": "GSE-ELA-GA",
        "subject": "ela",
        "description": "K-12 English Language Arts standards",
    },
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
    {
        "identifier": "a446e74c-463e-11e7-94f5-b49cee8b2d8c",
        "name": "Georgia Standards of Excellence - Social Studies",
        "short_name": "GSE Social Studies",
        "code": "GSE-SS-GA",
        "subject": "social_studies",
        "description": "K-12 Social Studies standards",
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
    """Main import process"""
    print("=" * 70)
    print("Georgia Standards of Excellence - Batch Import")
    print("=" * 70)
    print(f"\nImporting {len(GEORGIA_STANDARDS)} core academic standards from Georgia SuitCASE")
    print()

    # Login
    token = login()

    # Import each standard
    results = []
    for i, standard in enumerate(GEORGIA_STANDARDS, 1):
        print(f"\n[{i}/{len(GEORGIA_STANDARDS)}] {standard['short_name']}")
        print("-" * 70)

        job_id = create_import_job(token, standard)
        if job_id is None:
            results.append((standard['short_name'], False, "Failed to create job"))
            continue

        success = poll_job_status(token, job_id, max_wait=300)
        results.append((standard['short_name'], success, "Success" if success else "Failed"))

        # Wait a bit between imports to avoid overloading
        if i < len(GEORGIA_STANDARDS):
            time.sleep(3)

    # Print summary
    print("\n" + "=" * 70)
    print("IMPORT SUMMARY")
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
