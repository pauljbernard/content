#!/usr/bin/env python3
"""
Import Curriculum Configurations to Content Type system

This script imports all curriculum JSON configuration files from /config/curriculum/
into the new dynamic content type system as Curriculum Configuration instances.

Usage:
    python import_curriculum_configs.py
"""

import requests
import sys
import json
import glob
from pathlib import Path
from typing import Dict, List, Optional

# API Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

# Login credentials
LOGIN_EMAIL = "admin@hmhco.com"
LOGIN_PASSWORD = "changeme"

# Path to curriculum configs
CURRICULUM_CONFIG_DIR = Path(__file__).parent.parent.parent / "config" / "curriculum"


def login():
    """Authenticate and get access token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{API_BASE}/auth/login",
        data={"username": LOGIN_EMAIL, "password": LOGIN_PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        sys.exit(1)

    data = response.json()
    token = data.get("access_token")
    print(f"✅ Logged in successfully")
    return token


def get_or_create_curriculum_content_type(token: str) -> str:
    """Get existing Curriculum Configuration content type or create from template"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Check if Curriculum Configuration content type already exists
    print("\n📋 Checking for Curriculum Configuration content type...")
    response = requests.get(f"{API_BASE}/content-types", headers=headers)

    if response.status_code == 200:
        content_types = response.json()
        for ct in content_types:
            if ct["name"] == "Curriculum Configuration":
                print(f"✅ Found existing Curriculum Configuration content type: {ct['id']}")
                return ct["id"]

    # Need to create it - import from template
    print("📦 Curriculum Configuration content type not found, creating from template...")

    # Template definition (matching frontend template)
    template_data = {
        "name": "Curriculum Configuration",
        "description": "Knowledge base curriculum configuration defining content standards, knowledge resolution paths, and program metadata. Used by content generation systems to align materials to state/district requirements.",
        "icon": "cog",
        "is_system": False,
        "attributes": [
            # Core Identification
            {
                "name": "curriculum_id",
                "label": "Curriculum ID",
                "type": "text",
                "required": True,
                "help_text": "Unique identifier",
                "config": {"maxLength": 100},
                "order_index": 0,
            },
            {
                "name": "name",
                "label": "Curriculum Name",
                "type": "text",
                "required": True,
                "help_text": "Full display name",
                "config": {"maxLength": 200},
                "order_index": 1,
            },
            {
                "name": "publisher",
                "label": "Publisher",
                "type": "text",
                "required": True,
                "help_text": "Publisher code",
                "config": {"maxLength": 50},
                "order_index": 2,
            },
            {
                "name": "program",
                "label": "Program",
                "type": "text",
                "required": True,
                "help_text": "Program identifier",
                "config": {"maxLength": 100},
                "order_index": 3,
            },
            {
                "name": "subject",
                "label": "Subject",
                "type": "choice",
                "required": True,
                "help_text": "Subject area",
                "config": {
                    "choices": [
                        "mathematics", "ela", "science", "social_studies",
                        "computer_science", "world_languages", "arts", "physical_education"
                    ],
                    "multiple": False,
                },
                "order_index": 4,
            },
            {
                "name": "district",
                "label": "District/State",
                "type": "text",
                "required": True,
                "help_text": "State or district code",
                "config": {"maxLength": 100},
                "order_index": 5,
            },
            {
                "name": "grades",
                "label": "Grade Levels",
                "type": "json",
                "required": True,
                "help_text": "Array of grade levels",
                "config": {},
                "order_index": 6,
            },
            {
                "name": "course",
                "label": "Course Name",
                "type": "text",
                "required": False,
                "help_text": "Specific course name for high school",
                "config": {"maxLength": 100},
                "order_index": 7,
            },
            {
                "name": "version",
                "label": "Version/Year",
                "type": "text",
                "required": True,
                "help_text": "Version or adoption year",
                "config": {"maxLength": 50},
                "order_index": 8,
            },
            # Knowledge Resolution
            {
                "name": "knowledge_resolution_order",
                "label": "Knowledge Resolution Order",
                "type": "json",
                "required": True,
                "help_text": "Array of knowledge base paths in resolution order",
                "config": {},
                "order_index": 9,
            },
            # Standards Configuration
            {
                "name": "standards_config",
                "label": "Standards Configuration",
                "type": "json",
                "required": False,
                "help_text": "Standards alignment configuration",
                "config": {},
                "order_index": 10,
            },
            # Compliance Configuration
            {
                "name": "compliance_config",
                "label": "Compliance Configuration",
                "type": "json",
                "required": False,
                "help_text": "State/district compliance requirements",
                "config": {},
                "order_index": 11,
            },
            # Features Configuration
            {
                "name": "features_config",
                "label": "Features Configuration",
                "type": "json",
                "required": False,
                "help_text": "Program features and capabilities",
                "config": {},
                "order_index": 12,
            },
            # Metadata
            {
                "name": "metadata_config",
                "label": "Metadata Configuration",
                "type": "json",
                "required": False,
                "help_text": "Additional metadata",
                "config": {},
                "order_index": 13,
            },
            # Administrative
            {
                "name": "active",
                "label": "Active",
                "type": "boolean",
                "required": False,
                "help_text": "Whether this curriculum is currently active",
                "config": {"default": True},
                "order_index": 14,
            },
            {
                "name": "notes",
                "label": "Notes",
                "type": "long_text",
                "required": False,
                "help_text": "Internal notes or documentation",
                "config": {"maxLength": 5000},
                "order_index": 15,
            },
        ]
    }

    # Create the content type
    response = requests.post(
        f"{API_BASE}/content-types",
        json=template_data,
        headers=headers,
    )

    if response.status_code != 201:
        print(f"❌ Failed to create content type: {response.status_code}")
        print(response.text)
        sys.exit(1)

    new_ct = response.json()
    ct_id = new_ct["id"]
    print(f"✅ Created Curriculum Configuration content type: {ct_id}")

    return ct_id


def load_curriculum_json(file_path: Path) -> Dict:
    """Load and parse a curriculum JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def normalize_subject(subject: str) -> str:
    """Normalize subject names to match content type choices"""
    if not subject:
        return "other"

    subject_lower = subject.lower()

    # Direct mappings
    subject_map = {
        "physical education and health": "physical_education",
        "physical education": "physical_education",
        "world languages": "world_languages",
        "spanish": "world_languages",
        "fine arts": "arts",
        "visual arts": "arts",
    }

    if subject_lower in subject_map:
        return subject_map[subject_lower]

    # Remove spaces and hyphens for standard subjects
    normalized = subject_lower.replace(" ", "_").replace("-", "_")

    # Check if it's a valid choice
    valid_choices = [
        "mathematics", "ela", "science", "social_studies",
        "computer_science", "world_languages", "arts", "physical_education"
    ]

    if normalized in valid_choices:
        return normalized

    return "other"


def create_content_instance(token: str, content_type_id: str, curriculum_data: Dict, filename: str) -> Optional[str]:
    """Create a content instance from a curriculum JSON file"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Map curriculum JSON to content instance data with defaults for missing fields
    instance_data = {
        "curriculum_id": curriculum_data.get("id"),
        "name": curriculum_data.get("name"),
        "publisher": curriculum_data.get("publisher", "hmh"),  # Default to HMH
        "program": curriculum_data.get("program", curriculum_data.get("id", "unknown")),  # Use ID as fallback
        "subject": normalize_subject(curriculum_data.get("subject")),
        "district": curriculum_data.get("district") or "national",  # Default to national if null
        "grades": curriculum_data.get("grades", []),
        "course": curriculum_data.get("course"),
        "version": curriculum_data.get("version") or curriculum_data.get("metadata", {}).get("version", "1.0"),

        # Knowledge resolution
        "knowledge_resolution_order": curriculum_data.get("knowledge_resolution", {}).get("order", []),

        # Standards configuration
        "standards_config": curriculum_data.get("standards"),

        # Compliance configuration
        "compliance_config": curriculum_data.get("compliance"),

        # Features configuration
        "features_config": curriculum_data.get("features"),

        # Metadata configuration
        "metadata_config": curriculum_data.get("metadata"),

        # Administrative
        "active": True,
        "notes": f"Imported from {filename}",
    }

    # Create the instance
    payload = {
        "data": instance_data,
        "status": "published",  # These are official configurations
    }

    response = requests.post(
        f"{API_BASE}/content-types/{content_type_id}/instances",
        json=payload,
        headers=headers,
    )

    if response.status_code != 201:
        print(f"❌ Failed to create instance for {instance_data.get('curriculum_id')}: {response.status_code}")
        print(response.text)
        return None

    instance = response.json()
    return instance["id"]


def import_curriculum_configs(token: str):
    """Main import process"""
    # 1. Get or create Curriculum Configuration content type
    content_type_id = get_or_create_curriculum_content_type(token)

    # 2. Find all curriculum JSON files
    print(f"\n📁 Searching for curriculum configs in {CURRICULUM_CONFIG_DIR}...")
    curriculum_files = list(CURRICULUM_CONFIG_DIR.glob("*.json"))

    if not curriculum_files:
        print(f"⚠️  No curriculum JSON files found in {CURRICULUM_CONFIG_DIR}")
        return

    print(f"✅ Found {len(curriculum_files)} curriculum configurations")

    # 3. Import each curriculum config
    print(f"\n📝 Importing {len(curriculum_files)} curriculum configurations...")
    imported = []

    for i, file_path in enumerate(curriculum_files, 1):
        filename = file_path.name
        print(f"   [{i}/{len(curriculum_files)}] {filename}")

        try:
            curriculum_data = load_curriculum_json(file_path)
            curriculum_id = curriculum_data.get("id", filename)

            instance_id = create_content_instance(
                token,
                content_type_id,
                curriculum_data,
                filename
            )

            if instance_id:
                imported.append({
                    "filename": filename,
                    "curriculum_id": curriculum_id,
                    "instance_id": instance_id,
                })
                print(f"      ✓ Imported as {instance_id}")
            else:
                print(f"      ✗ Failed to import")

        except Exception as e:
            print(f"      ✗ Error: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("IMPORT SUMMARY")
    print("=" * 70)
    print(f"✅ Content Type ID: {content_type_id}")
    print(f"✅ Curricula Imported: {len(imported)}/{len(curriculum_files)}")
    print()

    if imported:
        print("Imported Curricula:")
        for item in imported:
            print(f"  ✓ {item['curriculum_id']} ({item['filename']}) → {item['instance_id']}")
        print()


def main():
    """Main entry point"""
    print("=" * 70)
    print("Curriculum Configurations Import to Content Type System")
    print("=" * 70)
    print()

    # Login
    token = login()

    # Import
    import_curriculum_configs(token)


if __name__ == "__main__":
    main()
