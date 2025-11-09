#!/usr/bin/env python3
"""
Import CASE standards package to Content Type system

This script imports a CASE (Competencies and Academic Standards Exchange) package
into the new dynamic content type system as hierarchical content instances.

Usage:
    python import_case_to_content_type.py <case_package_url>

Example:
    python import_case_to_content_type.py https://case.georgiastandards.org/ims/case/v1p0/CFPackages/27a08dc6-416e-11e7-ba71-02bd89fdd987
"""

import requests
import sys
import json
from typing import Dict, List, Optional
import time

# API Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

# Login credentials
LOGIN_EMAIL = "admin@hmhco.com"
LOGIN_PASSWORD = "changeme"


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


def get_or_create_case_content_type(token: str) -> str:
    """Get existing CASE Standard content type or create from template"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Check if CASE Standard content type already exists
    print("\n📋 Checking for CASE Standard content type...")
    response = requests.get(f"{API_BASE}/content-types", headers=headers)

    if response.status_code == 200:
        content_types = response.json()
        for ct in content_types:
            if ct["name"] == "CASE Standard":
                print(f"✅ Found existing CASE Standard content type: {ct['id']}")
                return ct["id"]

    # Need to create it - import from template
    print("📦 CASE Standard content type not found, creating from template...")

    # Template definition (matching frontend template)
    template_data = {
        "name": "CASE Standard",
        "description": "IMS Global CASE (Competencies and Academic Standards Exchange) format standard. Full support for hierarchical standards frameworks with CASE-compliant metadata for interoperability.",
        "icon": "clipboard-document-check",
        "is_system": False,
        "attributes": [
            # Core CASE CFItem Fields
            {
                "name": "identifier",
                "label": "CASE Identifier (GUID)",
                "type": "text",
                "required": True,
                "help_text": 'Unique GUID identifier for this CFItem',
                "config": {"maxLength": 255},
                "order_index": 0,
            },
            {
                "name": "uri",
                "label": "CASE URI",
                "type": "url",
                "required": False,
                "help_text": 'Canonical URI for this standard',
                "config": {},
                "order_index": 1,
            },
            {
                "name": "human_coding_scheme",
                "label": "Human Coding Scheme",
                "type": "text",
                "required": True,
                "help_text": 'Human-readable code (e.g., "CCSS.MATH.K.CC.A.1")',
                "config": {"maxLength": 100},
                "order_index": 2,
            },
            {
                "name": "list_enumeration",
                "label": "List Enumeration",
                "type": "text",
                "required": False,
                "help_text": 'Enumeration in list (e.g., "1", "1.a")',
                "config": {"maxLength": 50},
                "order_index": 3,
            },
            {
                "name": "full_statement",
                "label": "Full Statement",
                "type": "long_text",
                "required": True,
                "help_text": 'Complete text of the standard/competency',
                "config": {"maxLength": 10000},
                "order_index": 4,
            },
            {
                "name": "abbreviated_statement",
                "label": "Abbreviated Statement",
                "type": "text",
                "required": False,
                "help_text": 'Shortened version of the statement',
                "config": {"maxLength": 500},
                "order_index": 5,
            },
            {
                "name": "concept_keywords",
                "label": "Concept Keywords",
                "type": "json",
                "required": False,
                "help_text": 'Array of concept keywords',
                "config": {},
                "order_index": 6,
            },
            {
                "name": "notes",
                "label": "Notes",
                "type": "long_text",
                "required": False,
                "help_text": 'Additional notes or clarifications',
                "config": {"maxLength": 5000},
                "order_index": 7,
            },
            {
                "name": "language",
                "label": "Language",
                "type": "text",
                "required": False,
                "help_text": 'ISO 639-1 language code',
                "config": {"maxLength": 10},
                "order_index": 8,
            },
            # Hierarchical Relationships (placeholder - will be updated after creation)
            {
                "name": "parent",
                "label": "Parent CFItem",
                "type": "reference",
                "required": False,
                "help_text": 'Parent standard in CASE hierarchy',
                "config": {"targetContentType": "__PLACEHOLDER__", "multiple": False},
                "order_index": 9,
            },
            {
                "name": "children",
                "label": "Child CFItems",
                "type": "reference",
                "required": False,
                "help_text": 'Child standards',
                "config": {"targetContentType": "__PLACEHOLDER__", "multiple": True},
                "order_index": 10,
            },
            {
                "name": "related_items",
                "label": "Related CFItems",
                "type": "reference",
                "required": False,
                "help_text": 'Related standards',
                "config": {"targetContentType": "__PLACEHOLDER__", "multiple": True},
                "order_index": 11,
            },
            {
                "name": "prerequisite_items",
                "label": "Prerequisite CFItems",
                "type": "reference",
                "required": False,
                "help_text": 'Standards that are prerequisites',
                "config": {"targetContentType": "__PLACEHOLDER__", "multiple": True},
                "order_index": 12,
            },
            # CASE Metadata
            {
                "name": "cf_item_type",
                "label": "CFItem Type",
                "type": "choice",
                "required": True,
                "help_text": 'Type of competency framework item',
                "config": {
                    "choices": [
                        "Standard", "Benchmark", "Strand", "Topic", "Indicator",
                        "LearningObjective", "Competency", "Concept", "Domain",
                        "ClusterHeading", "GradeLevel", "SubjectArea"
                    ],
                    "multiple": False,
                },
                "order_index": 13,
            },
            {
                "name": "education_level",
                "label": "Education Level",
                "type": "choice",
                "required": False,
                "help_text": 'Target education levels',
                "config": {
                    "choices": [
                        "Pre-K", "K",
                        "01", "02", "03", "04", "05",
                        "06", "07", "08",
                        "09", "10", "11", "12",
                        "UG", "PG", "VO", "AE"
                    ],
                    "multiple": True,
                },
                "order_index": 14,
            },
            {
                "name": "cf_item_type_uri",
                "label": "CFItemType URI",
                "type": "url",
                "required": False,
                "help_text": 'URI reference to CFItemType vocabulary',
                "config": {},
                "order_index": 15,
            },
            {
                "name": "license_uri",
                "label": "License URI",
                "type": "url",
                "required": False,
                "help_text": 'License for this item',
                "config": {},
                "order_index": 16,
            },
            {
                "name": "status_start_date",
                "label": "Status Start Date",
                "type": "date",
                "required": False,
                "help_text": 'Date when this item becomes effective',
                "config": {"includeTime": True},
                "order_index": 17,
            },
            {
                "name": "status_end_date",
                "label": "Status End Date",
                "type": "date",
                "required": False,
                "help_text": 'Date when this item is deprecated',
                "config": {"includeTime": True},
                "order_index": 18,
            },
            {
                "name": "last_change_date_time",
                "label": "Last Change DateTime",
                "type": "date",
                "required": False,
                "help_text": 'Timestamp of last modification',
                "config": {"includeTime": True},
                "order_index": 19,
            },
            # Framework Context
            {
                "name": "cf_document_uri",
                "label": "CFDocument URI",
                "type": "url",
                "required": False,
                "help_text": 'URI of the parent CFDocument',
                "config": {},
                "order_index": 20,
            },
            {
                "name": "framework_title",
                "label": "Framework Title",
                "type": "text",
                "required": False,
                "help_text": 'Title of the parent framework',
                "config": {"maxLength": 300},
                "order_index": 21,
            },
            {
                "name": "subject",
                "label": "Subject",
                "type": "choice",
                "required": False,
                "help_text": 'Subject area(s)',
                "config": {
                    "choices": [
                        "Mathematics", "English Language Arts", "Science",
                        "Social Studies", "Computer Science", "Arts",
                        "Physical Education", "Health", "World Languages",
                        "Career & Technical Education"
                    ],
                    "multiple": True,
                },
                "order_index": 22,
            },
            {
                "name": "alternative_label",
                "label": "Alternative Label",
                "type": "text",
                "required": False,
                "help_text": 'Alternative human-readable label',
                "config": {"maxLength": 200},
                "order_index": 23,
            },
            # Extended Metadata
            {
                "name": "statement_notation",
                "label": "Statement Notation",
                "type": "text",
                "required": False,
                "help_text": 'Additional notation or classification',
                "config": {"maxLength": 100},
                "order_index": 24,
            },
            {
                "name": "statement_label",
                "label": "Statement Label",
                "type": "text",
                "required": False,
                "help_text": 'Label for the statement',
                "config": {"maxLength": 200},
                "order_index": 25,
            },
            {
                "name": "alignment_type",
                "label": "Alignment Type",
                "type": "choice",
                "required": False,
                "help_text": 'Type of alignment',
                "config": {
                    "choices": [
                        "assesses", "teaches", "requires", "isRelatedTo",
                        "isPartOf", "isPeerOf", "hasSkillLevel", "isChildOf",
                        "isParentOf", "precedes", "replacedBy"
                    ],
                    "multiple": False,
                },
                "order_index": 26,
            },
            {
                "name": "case_json",
                "label": "Full CASE JSON",
                "type": "json",
                "required": False,
                "help_text": 'Complete CASE CFItem JSON representation',
                "config": {},
                "order_index": 27,
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
    print(f"✅ Created CASE Standard content type: {ct_id}")

    # Now update the self-referencing fields
    print("🔗 Updating self-referencing fields...")
    updated_attributes = template_data["attributes"].copy()
    for attr in updated_attributes:
        if attr["type"] == "reference" and attr["config"].get("targetContentType") == "__PLACEHOLDER__":
            attr["config"]["targetContentType"] = ct_id

    response = requests.put(
        f"{API_BASE}/content-types/{ct_id}",
        json={"attributes": updated_attributes},
        headers=headers,
    )

    if response.status_code != 200:
        print(f"⚠️  Warning: Failed to update self-references: {response.status_code}")
        print(response.text)
    else:
        print(f"✅ Updated self-referencing fields")

    return ct_id


def fetch_case_package(case_url: str) -> Dict:
    """Fetch CASE package from URL"""
    print(f"\n📥 Fetching CASE package from: {case_url}")

    response = requests.get(case_url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch CASE package: {response.status_code}")
        sys.exit(1)

    package = response.json()
    print(f"✅ Fetched CASE package successfully")

    # Extract key info
    cf_document = package.get("CFDocument", {})
    cf_items = package.get("CFItems", [])
    cf_associations = package.get("CFAssociations", [])

    print(f"   📄 Document: {cf_document.get('title', 'Unknown')}")
    print(f"   📊 Items: {len(cf_items)}")
    print(f"   🔗 Associations: {len(cf_associations)}")

    return package


def create_content_instance(token: str, content_type_id: str, cf_item: Dict, framework_info: Dict) -> Optional[str]:
    """Create a content instance from a CASE CFItem"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Valid CFItemTypes from template
    VALID_CF_ITEM_TYPES = [
        "Standard", "Benchmark", "Strand", "Topic", "Indicator",
        "LearningObjective", "Competency", "Concept", "Domain",
        "ClusterHeading", "GradeLevel", "SubjectArea"
    ]

    # Map CASE CFItemType to our valid types
    cf_item_type = cf_item.get("CFItemType", "Standard")
    if cf_item_type not in VALID_CF_ITEM_TYPES:
        # Map common variations
        cf_item_type_lower = cf_item_type.lower()
        if "standard" in cf_item_type_lower:
            cf_item_type = "Standard"
        elif "task" in cf_item_type_lower:
            cf_item_type = "LearningObjective"
        elif "element" in cf_item_type_lower:
            cf_item_type = "Indicator"
        elif "course" in cf_item_type_lower:
            cf_item_type = "SubjectArea"
        else:
            cf_item_type = "Standard"  # Default fallback

    # Valid education levels from template
    VALID_EDUCATION_LEVELS = [
        "Pre-K", "K",
        "01", "02", "03", "04", "05",
        "06", "07", "08",
        "09", "10", "11", "12",
        "UG", "PG", "VO", "AE"
    ]

    # Map education levels (KG -> K, etc.)
    education_levels = cf_item.get("educationLevel", [])
    if isinstance(education_levels, str):
        education_levels = [education_levels]

    mapped_education_levels = []
    for level in education_levels:
        if level == "KG":
            mapped_education_levels.append("K")
        elif level in VALID_EDUCATION_LEVELS:
            mapped_education_levels.append(level)
        # Otherwise skip invalid levels

    # Map CASE fields to content instance data
    instance_data = {
        "identifier": cf_item.get("identifier"),
        "uri": cf_item.get("uri"),
        "human_coding_scheme": cf_item.get("humanCodingScheme") or cf_item.get("identifier", ""),
        "list_enumeration": cf_item.get("listEnumeration"),
        "full_statement": cf_item.get("fullStatement", ""),
        "abbreviated_statement": cf_item.get("abbreviatedStatement"),
        "concept_keywords": cf_item.get("conceptKeywords", []),
        "notes": cf_item.get("notes"),
        "language": cf_item.get("language"),

        # Will set relationships later in second pass
        "parent": None,
        "children": [],
        "related_items": [],
        "prerequisite_items": [],

        # Metadata
        "cf_item_type": cf_item_type,
        "education_level": mapped_education_levels,
        "cf_item_type_uri": cf_item.get("CFItemTypeURI", {}).get("uri") if isinstance(cf_item.get("CFItemTypeURI"), dict) else cf_item.get("CFItemTypeURI"),
        "license_uri": cf_item.get("licenseURI", {}).get("uri") if isinstance(cf_item.get("licenseURI"), dict) else cf_item.get("licenseURI"),
        "status_start_date": cf_item.get("statusStartDate"),
        "status_end_date": cf_item.get("statusEndDate"),
        "last_change_date_time": cf_item.get("lastChangeDateTime"),

        # Framework context
        "cf_document_uri": framework_info.get("uri"),
        "framework_title": framework_info.get("title"),
        "subject": [framework_info.get("subject")] if framework_info.get("subject") else [],
        "alternative_label": cf_item.get("alternativeLabel"),

        # Extended
        "statement_notation": cf_item.get("statementNotation"),
        "statement_label": cf_item.get("statementLabel"),
        "alignment_type": None,

        # Full CASE JSON for fidelity
        "case_json": cf_item,
    }

    # Create the instance
    payload = {
        "data": instance_data,
        "status": "published",  # These are official standards
    }

    response = requests.post(
        f"{API_BASE}/content-types/{content_type_id}/instances",
        json=payload,
        headers=headers,
    )

    if response.status_code != 201:
        print(f"❌ Failed to create instance for {instance_data.get('human_coding_scheme')}: {response.status_code}")
        print(response.text)
        return None

    instance = response.json()
    return instance["id"]


def import_case_package(token: str, case_url: str):
    """Main import process"""
    # 1. Get or create CASE Standard content type
    content_type_id = get_or_create_case_content_type(token)

    # 2. Fetch CASE package
    package = fetch_case_package(case_url)

    cf_document = package.get("CFDocument", {})
    cf_items = package.get("CFItems", [])
    cf_associations = package.get("CFAssociations", [])

    framework_info = {
        "uri": cf_document.get("uri"),
        "title": cf_document.get("title"),
        "subject": cf_document.get("subject", [None])[0] if cf_document.get("subject") else None,
    }

    # 3. Create content instances (first pass - no relationships)
    print(f"\n📝 Creating {len(cf_items)} content instances...")
    identifier_to_instance_id = {}

    for i, cf_item in enumerate(cf_items, 1):
        cf_identifier = cf_item.get("identifier")
        human_code = cf_item.get("humanCodingScheme", cf_identifier[:8])

        if i % 10 == 0 or i == 1 or i == len(cf_items):
            print(f"   [{i}/{len(cf_items)}] {human_code}")

        instance_id = create_content_instance(token, content_type_id, cf_item, framework_info)
        if instance_id:
            identifier_to_instance_id[cf_identifier] = instance_id

    print(f"✅ Created {len(identifier_to_instance_id)} content instances")

    # 4. Update relationships (second pass)
    print(f"\n🔗 Establishing {len(cf_associations)} relationships...")

    # Build associations map
    parent_map = {}  # child_id -> parent_id
    children_map = {}  # parent_id -> [child_ids]

    for assoc in cf_associations:
        assoc_type = assoc.get("associationType")
        origin_id = assoc.get("originNodeURI", {}).get("identifier")
        dest_id = assoc.get("destinationNodeURI", {}).get("identifier")

        if assoc_type == "isChildOf":
            parent_map[origin_id] = dest_id
            if dest_id not in children_map:
                children_map[dest_id] = []
            children_map[dest_id].append(origin_id)

    # Update instances with relationships
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    updated_count = 0
    for cf_identifier, instance_id in identifier_to_instance_id.items():
        parent_cf_id = parent_map.get(cf_identifier)
        child_cf_ids = children_map.get(cf_identifier, [])

        # Keep CASE identifiers for hierarchical relationships (not instance IDs)
        # The tree view expects parent/children to contain CASE identifiers
        # IMPORTANT: If parent doesn't exist in imported set, set to None (makes it a root)
        parent_identifier = parent_cf_id if parent_cf_id in identifier_to_instance_id else None
        child_identifiers = child_cf_ids  # CASE identifiers, not instance IDs

        if parent_identifier is not None or child_identifiers:
            # Fetch current instance to get data
            response = requests.get(
                f"{API_BASE}/content-types/instances/{instance_id}",
                headers=headers,
            )

            if response.status_code == 200:
                instance = response.json()
                data = instance["data"]

                # Update relationships using CASE identifiers (for hierarchical tree view)
                data["parent"] = parent_identifier  # CASE identifier
                data["children"] = child_identifiers  # List of CASE identifiers

                # Update instance
                response = requests.put(
                    f"{API_BASE}/content-types/instances/{instance_id}",
                    json={"data": data},
                    headers=headers,
                )

                if response.status_code == 200:
                    updated_count += 1

    print(f"✅ Updated {updated_count} instances with hierarchical relationships")

    # 5. Ensure root node exists - create synthetic root if needed
    print(f"\n🌳 Ensuring root node exists...")

    # Check if any root nodes exist (parent = None or null)
    root_count = 0
    for instance_id in identifier_to_instance_id.values():
        response = requests.get(
            f"{API_BASE}/content-types/instances/{instance_id}",
            headers=headers,
        )
        if response.status_code == 200:
            instance = response.json()
            data = instance.get("data", {})
            parent = data.get("parent")
            if parent is None or parent == "" or parent == "null":
                root_count += 1
                if root_count == 1:
                    print(f"   Found existing root: {data.get('full_statement', 'Unknown')[:60]}...")

    if root_count == 0:
        print(f"   ⚠️  No root node found - creating synthetic root...")

        # Create synthetic root from CFDocument metadata
        synthetic_root_data = {
            "identifier": f"ROOT-{cf_document.get('identifier', 'unknown')}",
            "uri": cf_document.get("uri"),
            "human_coding_scheme": cf_document.get("identifier", "ROOT"),
            "full_statement": cf_document.get("title", "Framework Root"),
            "abbreviated_statement": cf_document.get("title", "Framework Root"),
            "concept_keywords": [],
            "notes": cf_document.get("description", "Synthetic root node for framework"),
            "language": cf_document.get("language", "en"),

            # Root has no parent
            "parent": None,
            "children": [],
            "related_items": [],
            "prerequisite_items": [],

            # Metadata from CFDocument
            "cf_item_type": "Domain",  # Root is typically a domain
            "education_level": [],
            "license_uri": cf_document.get("licenseURI", {}).get("uri") if isinstance(cf_document.get("licenseURI"), dict) else cf_document.get("licenseURI"),
            "status_start_date": cf_document.get("statusStartDate"),
            "status_end_date": cf_document.get("statusEndDate"),
            "last_change_date_time": cf_document.get("lastChangeDateTime"),

            # Framework context
            "cf_document_uri": cf_document.get("uri"),
            "framework_title": cf_document.get("title"),
            "subject": cf_document.get("subject", [None])[0] if cf_document.get("subject") else None,

            # Full CASE JSON
            "case_json": cf_document,
        }

        # Create the synthetic root instance
        response = requests.post(
            f"{API_BASE}/content-types/instances",
            json={
                "content_type_id": content_type_id,
                "data": synthetic_root_data,
                "status": "published",
            },
            headers=headers,
        )

        if response.status_code == 201:
            synthetic_root = response.json()
            synthetic_root_id = synthetic_root["id"]
            synthetic_root_identifier = synthetic_root_data["identifier"]
            print(f"   ✅ Created synthetic root: {synthetic_root_data['full_statement'][:60]}...")

            # Update all orphaned items to have this synthetic root as parent
            orphaned_count = 0
            for cf_identifier, instance_id in identifier_to_instance_id.items():
                # Check if this item has no parent or orphaned parent
                parent_cf_id = parent_map.get(cf_identifier)

                if parent_cf_id is None or parent_cf_id not in identifier_to_instance_id:
                    # This is an orphaned item - attach to synthetic root
                    response = requests.get(
                        f"{API_BASE}/content-types/instances/{instance_id}",
                        headers=headers,
                    )

                    if response.status_code == 200:
                        instance = response.json()
                        data = instance["data"]
                        data["parent"] = synthetic_root_identifier

                        # Update instance
                        response = requests.put(
                            f"{API_BASE}/content-types/instances/{instance_id}",
                            json={"data": data},
                            headers=headers,
                        )

                        if response.status_code == 200:
                            orphaned_count += 1

            print(f"   ✅ Attached {orphaned_count} orphaned items to synthetic root")
        else:
            print(f"   ❌ Failed to create synthetic root: {response.status_code}")
            print(f"   {response.text}")
    else:
        print(f"   ✅ Root node(s) already exist: {root_count}")

    # Summary
    print("\n" + "=" * 70)
    print("IMPORT SUMMARY")
    print("=" * 70)
    print(f"✅ Framework: {framework_info['title']}")
    print(f"✅ Content Type ID: {content_type_id}")
    print(f"✅ Standards Imported: {len(identifier_to_instance_id)}")
    print(f"✅ Relationships Established: {updated_count}")
    print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python import_case_to_content_type.py <case_package_url>")
        print()
        print("Example:")
        print("  python import_case_to_content_type.py https://case.georgiastandards.org/ims/case/v1p0/CFPackages/27a08dc6-416e-11e7-ba71-02bd89fdd987")
        sys.exit(1)

    case_url = sys.argv[1]

    print("=" * 70)
    print("CASE Package Import to Content Type System")
    print("=" * 70)
    print()

    # Login
    token = login()

    # Import
    import_case_package(token, case_url)


if __name__ == "__main__":
    main()
