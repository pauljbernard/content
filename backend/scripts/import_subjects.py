#!/usr/bin/env python3
"""
Import Subjects to Content Type system

This script imports subjects from the knowledge base directory structure
into the new dynamic content type system as Subject instances.

Usage:
    python import_subjects.py
"""

import requests
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# API Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

# Login credentials
LOGIN_EMAIL = "admin@hmhco.com"
LOGIN_PASSWORD = "changeme"

# Path to knowledge base subjects
KNOWLEDGE_BASE_ROOT = Path(__file__).parent.parent.parent / "reference" / "hmh-knowledge"
SUBJECTS_PATH = KNOWLEDGE_BASE_ROOT / "subjects"


# Subject metadata mapping
SUBJECT_METADATA = {
    "computer-science": {
        "name": "Computer Science",
        "abbreviation": "CS",
        "description": "Computer science, programming, computational thinking, and technology education",
        "category": "stem",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["CSTA", "ISTE"],
        "icon": "computer",
        "color": "#10B981",
        "display_order": 5,
    },
    "early-literacy": {
        "name": "Early Literacy",
        "abbreviation": "Early Lit",
        "description": "Foundational literacy skills for Pre-K and Kindergarten learners",
        "category": "language",
        "grade_levels": ["Pre-K", "K"],
        "standards_frameworks": ["State-Specific"],
        "icon": "book-open",
        "color": "#F59E0B",
        "display_order": 11,
    },
    "early-mathematics": {
        "name": "Early Mathematics",
        "abbreviation": "Early Math",
        "description": "Foundational mathematics skills for Pre-K and Kindergarten learners",
        "category": "stem",
        "grade_levels": ["Pre-K", "K"],
        "standards_frameworks": ["State-Specific"],
        "icon": "calculator",
        "color": "#8B5CF6",
        "display_order": 12,
    },
    "ela": {
        "name": "English Language Arts",
        "abbreviation": "ELA",
        "description": "Reading, writing, speaking, listening, and language skills",
        "category": "core",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["CCSS", "TEKS", "State-Specific"],
        "icon": "book-open",
        "color": "#EF4444",
        "display_order": 2,
    },
    "fine-arts": {
        "name": "Fine Arts",
        "abbreviation": "Arts",
        "description": "Visual arts, music, theater, and creative expression",
        "category": "arts",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["National Core Arts Standards"],
        "icon": "palette",
        "color": "#EC4899",
        "display_order": 7,
    },
    "mathematics": {
        "name": "Mathematics",
        "abbreviation": "Math",
        "description": "Numbers, operations, algebra, geometry, measurement, data analysis, and problem-solving",
        "category": "core",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["CCSS-M", "TEKS", "State-Specific"],
        "icon": "calculator",
        "color": "#3B82F6",
        "display_order": 1,
    },
    "physical-education": {
        "name": "Physical Education & Health",
        "abbreviation": "PE/Health",
        "description": "Physical fitness, motor skills, health education, and wellness",
        "category": "wellness",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["SHAPE America", "National Health Education Standards"],
        "icon": "heart",
        "color": "#F97316",
        "display_order": 8,
    },
    "science": {
        "name": "Science",
        "abbreviation": "Sci",
        "description": "Physical science, life science, earth/space science, and scientific practices",
        "category": "core",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["NGSS", "TEKS", "State-Specific"],
        "icon": "beaker",
        "color": "#10B981",
        "display_order": 3,
    },
    "social-studies": {
        "name": "Social Studies",
        "abbreviation": "SS",
        "description": "History, geography, civics, economics, and social sciences",
        "category": "humanities",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["C3 Framework", "TEKS", "State-Specific"],
        "icon": "globe",
        "color": "#F59E0B",
        "display_order": 4,
    },
    "world-languages": {
        "name": "World Languages",
        "abbreviation": "WL",
        "description": "Foreign language acquisition, cultural competence, and communication",
        "category": "language",
        "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "standards_frameworks": ["ACTFL", "State-Specific"],
        "icon": "language",
        "color": "#8B5CF6",
        "display_order": 6,
    },
}


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


def get_or_create_subject_content_type(token: str) -> str:
    """Get existing Subject content type or create from template"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Check if Subject content type already exists
    print("\n📋 Checking for Subject content type...")
    response = requests.get(f"{API_BASE}/content-types", headers=headers)

    if response.status_code == 200:
        content_types = response.json()
        for ct in content_types:
            if ct["name"] == "Subject":
                print(f"✅ Found existing Subject content type: {ct['id']}")
                return ct["id"]

    # Need to create it - import from template
    print("📦 Subject content type not found, creating from template...")

    # Get the template from contentTypeTemplates.js
    template_data = {
        "name": "Subject",
        "description": "Academic subject area or discipline. Defines core subject taxonomies used for organizing knowledge base files and categorizing content.",
        "icon": "academic-cap",
        "is_system": False,
        "attributes": [
            {
                "name": "subject_code",
                "label": "Subject Code",
                "type": "text",
                "required": True,
                "help_text": "Unique identifier (e.g., \"mathematics\", \"ela\", \"science\")",
                "config": {"maxLength": 100},
                "order_index": 0,
            },
            {
                "name": "name",
                "label": "Subject Name",
                "type": "text",
                "required": True,
                "help_text": "Full display name (e.g., \"Mathematics\", \"English Language Arts\")",
                "config": {"maxLength": 200},
                "order_index": 1,
            },
            {
                "name": "abbreviation",
                "label": "Abbreviation",
                "type": "text",
                "required": False,
                "help_text": "Short abbreviation (e.g., \"Math\", \"ELA\", \"Sci\")",
                "config": {"maxLength": 20},
                "order_index": 2,
            },
            {
                "name": "description",
                "label": "Description",
                "type": "long_text",
                "required": False,
                "help_text": "Detailed description of the subject area",
                "config": {"maxLength": 2000},
                "order_index": 3,
            },
            {
                "name": "parent_subject",
                "label": "Parent Subject",
                "type": "reference",
                "required": False,
                "help_text": "Parent subject if this is a specialized area",
                "config": {"targetContentType": "__SELF__", "multiple": False},
                "order_index": 4,
            },
            {
                "name": "subject_category",
                "label": "Category",
                "type": "choice",
                "required": True,
                "help_text": "Broad category classification",
                "config": {
                    "choices": ["core", "stem", "humanities", "arts", "wellness", "language", "technical", "other"],
                    "multiple": False,
                },
                "order_index": 5,
            },
            {
                "name": "grade_levels",
                "label": "Applicable Grade Levels",
                "type": "choice",
                "required": False,
                "help_text": "Grade levels where this subject is taught",
                "config": {
                    "choices": ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "Higher Ed"],
                    "multiple": True,
                },
                "order_index": 6,
            },
            {
                "name": "knowledge_base_path",
                "label": "Knowledge Base Path",
                "type": "text",
                "required": False,
                "help_text": "Path to subject directory in knowledge base",
                "config": {"maxLength": 200},
                "order_index": 7,
            },
            {
                "name": "standards_frameworks",
                "label": "Common Standards Frameworks",
                "type": "json",
                "required": False,
                "help_text": "Array of standards frameworks used",
                "config": {},
                "order_index": 8,
            },
            {
                "name": "icon",
                "label": "Icon",
                "type": "text",
                "required": False,
                "help_text": "Icon name or emoji for UI display",
                "config": {"maxLength": 50},
                "order_index": 9,
            },
            {
                "name": "color",
                "label": "Display Color",
                "type": "text",
                "required": False,
                "help_text": "Hex color code for UI",
                "config": {"maxLength": 20},
                "order_index": 10,
            },
            {
                "name": "active",
                "label": "Active",
                "type": "boolean",
                "required": False,
                "help_text": "Whether this subject is currently active",
                "config": {"default": True},
                "order_index": 11,
            },
            {
                "name": "display_order",
                "label": "Display Order",
                "type": "number",
                "required": False,
                "help_text": "Order for sorting in UI (lower numbers first)",
                "config": {"min": 0, "max": 1000, "step": 1},
                "order_index": 12,
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
    print(f"✅ Created Subject content type: {ct_id}")

    return ct_id


def create_content_instance(token: str, content_type_id: str, subject_code: str) -> Optional[str]:
    """Create a content instance for a subject"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Get metadata for this subject
    metadata = SUBJECT_METADATA.get(subject_code)
    if not metadata:
        print(f"⚠️  No metadata found for subject: {subject_code}")
        return None

    # Create instance data
    instance_data = {
        "subject_code": subject_code,
        "name": metadata["name"],
        "abbreviation": metadata["abbreviation"],
        "description": metadata["description"],
        "subject_category": metadata["category"],
        "grade_levels": metadata["grade_levels"],
        "knowledge_base_path": f"/subjects/{subject_code}",
        "standards_frameworks": metadata["standards_frameworks"],
        "icon": metadata["icon"],
        "color": metadata["color"],
        "active": True,
        "display_order": metadata["display_order"],
    }

    # Create the instance
    payload = {
        "data": instance_data,
        "status": "published",  # These are reference data
    }

    response = requests.post(
        f"{API_BASE}/content-types/{content_type_id}/instances",
        json=payload,
        headers=headers,
    )

    if response.status_code != 201:
        print(f"❌ Failed to create instance for {subject_code}: {response.status_code}")
        print(response.text)
        return None

    instance = response.json()
    return instance["id"]


def import_subjects(token: str):
    """Main import process"""
    # 1. Get or create Subject content type
    content_type_id = get_or_create_subject_content_type(token)

    # 2. Find all subject directories
    print(f"\n📁 Searching for subjects in {SUBJECTS_PATH}...")
    if not SUBJECTS_PATH.exists():
        print(f"❌ Subjects path does not exist: {SUBJECTS_PATH}")
        sys.exit(1)

    subjects = []
    for item in SUBJECTS_PATH.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            subjects.append(item.name)

    subjects = sorted(subjects)
    print(f"✅ Found {len(subjects)} subjects")

    # 3. Import each subject
    print(f"\n📝 Importing {len(subjects)} subjects...")
    imported = []

    for i, subject_code in enumerate(subjects, 1):
        print(f"   [{i}/{len(subjects)}] {subject_code}")

        try:
            instance_id = create_content_instance(token, content_type_id, subject_code)

            if instance_id:
                imported.append({
                    "subject_code": subject_code,
                    "name": SUBJECT_METADATA[subject_code]["name"],
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
    print(f"✅ Subjects Imported: {len(imported)}/{len(subjects)}")
    print()

    if imported:
        print("Imported Subjects:")
        for item in imported:
            print(f"  ✓ {item['subject_code']} → {item['name']} ({item['instance_id']})")
        print()


def main():
    """Main entry point"""
    print("=" * 70)
    print("Subjects Import to Content Type System")
    print("=" * 70)
    print()

    # Login
    token = login()

    # Import
    import_subjects(token)


if __name__ == "__main__":
    main()
