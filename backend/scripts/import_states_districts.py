#!/usr/bin/env python3
"""
Import States/Districts to Content Type system

This script imports states and districts from the knowledge base directory structure
into the new dynamic content type system as State/District instances.

Usage:
    python import_states_districts.py
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

# Path to knowledge base districts
KNOWLEDGE_BASE_ROOT = Path(__file__).parent.parent.parent / "reference" / "hmh-knowledge"
DISTRICTS_PATH = KNOWLEDGE_BASE_ROOT / "districts"


# State/District metadata mapping
# Format: code: {name, abbreviation, type, parent_state_code, region, population, standards_framework, language_standards, website, display_order}
STATE_DISTRICT_METADATA = {
    # States (alphabetical)
    "alabama": {"name": "Alabama", "abbreviation": "AL", "type": "state", "region": "Southeast", "population": 750000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 1},
    "alaska": {"name": "Alaska", "abbreviation": "AK", "type": "state", "region": "Pacific", "population": 130000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 2},
    "arizona": {"name": "Arizona", "abbreviation": "AZ", "type": "state", "region": "Southwest", "population": 1100000, "standards_framework": "CCSS", "language_standards": "ELD", "display_order": 3},
    "arkansas": {"name": "Arkansas", "abbreviation": "AR", "type": "state", "region": "Southeast", "population": 490000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 4},
    "california": {"name": "California", "abbreviation": "CA", "type": "state", "region": "West", "population": 6200000, "standards_framework": "CCSS", "language_standards": "ELD", "display_order": 5},
    "colorado": {"name": "Colorado", "abbreviation": "CO", "type": "state", "region": "West", "population": 900000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 6},
    "connecticut": {"name": "Connecticut", "abbreviation": "CT", "type": "state", "region": "Northeast", "population": 540000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 7},
    "delaware": {"name": "Delaware", "abbreviation": "DE", "type": "state", "region": "Northeast", "population": 140000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 8},
    "district-of-columbia": {"name": "District of Columbia", "abbreviation": "DC", "type": "state", "region": "Northeast", "population": 90000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 9},
    "florida": {"name": "Florida", "abbreviation": "FL", "type": "state", "region": "Southeast", "population": 2900000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 10},
    "georgia": {"name": "Georgia", "abbreviation": "GA", "type": "state", "region": "Southeast", "population": 1800000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 11},
    "hawaii": {"name": "Hawaii", "abbreviation": "HI", "type": "state", "region": "Pacific", "population": 180000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 12},
    "idaho": {"name": "Idaho", "abbreviation": "ID", "type": "state", "region": "West", "population": 310000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 13},
    "illinois": {"name": "Illinois", "abbreviation": "IL", "type": "state", "region": "Midwest", "population": 2000000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 14},
    "indiana": {"name": "Indiana", "abbreviation": "IN", "type": "state", "region": "Midwest", "population": 1050000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 15},
    "iowa": {"name": "Iowa", "abbreviation": "IA", "type": "state", "region": "Midwest", "population": 530000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 16},
    "kansas": {"name": "Kansas", "abbreviation": "KS", "type": "state", "region": "Midwest", "population": 500000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 17},
    "kentucky": {"name": "Kentucky", "abbreviation": "KY", "type": "state", "region": "Southeast", "population": 680000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 18},
    "louisiana": {"name": "Louisiana", "abbreviation": "LA", "type": "state", "region": "Southeast", "population": 730000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 19},
    "maine": {"name": "Maine", "abbreviation": "ME", "type": "state", "region": "Northeast", "population": 180000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 20},
    "maryland": {"name": "Maryland", "abbreviation": "MD", "type": "state", "region": "Northeast", "population": 900000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 21},
    "massachusetts": {"name": "Massachusetts", "abbreviation": "MA", "type": "state", "region": "Northeast", "population": 960000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 22},
    "michigan": {"name": "Michigan", "abbreviation": "MI", "type": "state", "region": "Midwest", "population": 1500000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 23},
    "minnesota": {"name": "Minnesota", "abbreviation": "MN", "type": "state", "region": "Midwest", "population": 890000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 24},
    "mississippi": {"name": "Mississippi", "abbreviation": "MS", "type": "state", "region": "Southeast", "population": 480000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 25},
    "missouri": {"name": "Missouri", "abbreviation": "MO", "type": "state", "region": "Midwest", "population": 920000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 26},
    "montana": {"name": "Montana", "abbreviation": "MT", "type": "state", "region": "West", "population": 150000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 27},
    "nebraska": {"name": "Nebraska", "abbreviation": "NE", "type": "state", "region": "Midwest", "population": 330000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 28},
    "nevada": {"name": "Nevada", "abbreviation": "NV", "type": "state", "region": "West", "population": 500000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 29},
    "new-hampshire": {"name": "New Hampshire", "abbreviation": "NH", "type": "state", "region": "Northeast", "population": 180000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 30},
    "new-jersey": {"name": "New Jersey", "abbreviation": "NJ", "type": "state", "region": "Northeast", "population": 1400000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 31},
    "new-mexico": {"name": "New Mexico", "abbreviation": "NM", "type": "state", "region": "Southwest", "population": 330000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 32},
    "new-york": {"name": "New York", "abbreviation": "NY", "type": "state", "region": "Northeast", "population": 2800000, "standards_framework": "CCSS", "language_standards": "NYSESLAT", "display_order": 33},
    "north-carolina": {"name": "North Carolina", "abbreviation": "NC", "type": "state", "region": "Southeast", "population": 1550000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 34},
    "north-dakota": {"name": "North Dakota", "abbreviation": "ND", "type": "state", "region": "Midwest", "population": 110000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 35},
    "ohio": {"name": "Ohio", "abbreviation": "OH", "type": "state", "region": "Midwest", "population": 1700000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 36},
    "oklahoma": {"name": "Oklahoma", "abbreviation": "OK", "type": "state", "region": "Southwest", "population": 700000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 37},
    "oregon": {"name": "Oregon", "abbreviation": "OR", "type": "state", "region": "West", "population": 600000, "standards_framework": "CCSS", "language_standards": "ELD", "display_order": 38},
    "pennsylvania": {"name": "Pennsylvania", "abbreviation": "PA", "type": "state", "region": "Northeast", "population": 1800000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 39},
    "rhode-island": {"name": "Rhode Island", "abbreviation": "RI", "type": "state", "region": "Northeast", "population": 140000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 40},
    "south-carolina": {"name": "South Carolina", "abbreviation": "SC", "type": "state", "region": "Southeast", "population": 800000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 41},
    "south-dakota": {"name": "South Dakota", "abbreviation": "SD", "type": "state", "region": "Midwest", "population": 140000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 42},
    "tennessee": {"name": "Tennessee", "abbreviation": "TN", "type": "state", "region": "Southeast", "population": 1000000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 43},
    "texas": {"name": "Texas", "abbreviation": "TX", "type": "state", "region": "Southwest", "population": 5400000, "standards_framework": "TEKS", "language_standards": "ELPS", "display_order": 44},
    "utah": {"name": "Utah", "abbreviation": "UT", "type": "state", "region": "West", "population": 680000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 45},
    "vermont": {"name": "Vermont", "abbreviation": "VT", "type": "state", "region": "Northeast", "population": 88000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 46},
    "virginia": {"name": "Virginia", "abbreviation": "VA", "type": "state", "region": "Southeast", "population": 1300000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 47},
    "washington": {"name": "Washington", "abbreviation": "WA", "type": "state", "region": "West", "population": 1150000, "standards_framework": "CCSS", "language_standards": "ELD", "display_order": 48},
    "west-virginia": {"name": "West Virginia", "abbreviation": "WV", "type": "state", "region": "Southeast", "population": 270000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 49},
    "wisconsin": {"name": "Wisconsin", "abbreviation": "WI", "type": "state", "region": "Midwest", "population": 870000, "standards_framework": "State-Specific", "language_standards": "WIDA", "display_order": 50},
    "wyoming": {"name": "Wyoming", "abbreviation": "WY", "type": "state", "region": "West", "population": 95000, "standards_framework": "CCSS", "language_standards": "WIDA", "display_order": 51},

    # Large Urban Districts
    "broward-county": {"name": "Broward County Public Schools", "abbreviation": "Broward", "type": "large_urban_district", "parent_state": "florida", "region": "Southeast", "population": 270000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.browardschools.com", "display_order": 52},
    "charlotte-mecklenburg": {"name": "Charlotte-Mecklenburg Schools", "abbreviation": "CMS", "type": "large_urban_district", "parent_state": "north-carolina", "region": "Southeast", "population": 147000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.cms.k12.nc.us", "display_order": 53},
    "chicago-public-schools": {"name": "Chicago Public Schools", "abbreviation": "CPS", "type": "large_urban_district", "parent_state": "illinois", "region": "Midwest", "population": 340000, "standards_framework": "CCSS", "language_standards": "WIDA", "website": "https://www.cps.edu", "display_order": 54},
    "clark-county-nevada": {"name": "Clark County School District", "abbreviation": "CCSD", "type": "large_urban_district", "parent_state": "nevada", "region": "West", "population": 320000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.ccsd.net", "display_order": 55},
    "cypress-fairbanks": {"name": "Cypress-Fairbanks ISD", "abbreviation": "CFISD", "type": "large_urban_district", "parent_state": "texas", "region": "Southwest", "population": 116000, "standards_framework": "TEKS", "language_standards": "ELPS", "website": "https://www.cfisd.net", "display_order": 56},
    "dallas-isd": {"name": "Dallas Independent School District", "abbreviation": "Dallas ISD", "type": "large_urban_district", "parent_state": "texas", "region": "Southwest", "population": 150000, "standards_framework": "TEKS", "language_standards": "ELPS", "website": "https://www.dallasisd.org", "display_order": 57},
    "fairfax-county": {"name": "Fairfax County Public Schools", "abbreviation": "FCPS", "type": "large_urban_district", "parent_state": "virginia", "region": "Southeast", "population": 180000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.fcps.edu", "display_order": 58},
    "gwinnett-county": {"name": "Gwinnett County Public Schools", "abbreviation": "GCPS", "type": "large_urban_district", "parent_state": "georgia", "region": "Southeast", "population": 180000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.gcpsk12.org", "display_order": 59},
    "hillsborough-county": {"name": "Hillsborough County Public Schools", "abbreviation": "HCPS", "type": "large_urban_district", "parent_state": "florida", "region": "Southeast", "population": 220000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.sdhc.k12.fl.us", "display_order": 60},
    "houston-isd": {"name": "Houston Independent School District", "abbreviation": "Houston ISD", "type": "large_urban_district", "parent_state": "texas", "region": "Southwest", "population": 200000, "standards_framework": "TEKS", "language_standards": "ELPS", "website": "https://www.houstonisd.org", "display_order": 61},
    "los-angeles-unified": {"name": "Los Angeles Unified School District", "abbreviation": "LAUSD", "type": "large_urban_district", "parent_state": "california", "region": "West", "population": 540000, "standards_framework": "CCSS", "language_standards": "ELD", "website": "https://www.lausd.net", "display_order": 62},
    "miami-dade-county": {"name": "Miami-Dade County Public Schools", "abbreviation": "M-DCPS", "type": "large_urban_district", "parent_state": "florida", "region": "Southeast", "population": 330000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.dadeschools.net", "display_order": 63},
    "new-york-city": {"name": "New York City Department of Education", "abbreviation": "NYC DOE", "type": "large_urban_district", "parent_state": "new-york", "region": "Northeast", "population": 1000000, "standards_framework": "CCSS", "language_standards": "NYSESLAT", "website": "https://www.schools.nyc.gov", "display_order": 64},
    "northside-isd": {"name": "Northside ISD", "abbreviation": "NISD", "type": "large_urban_district", "parent_state": "texas", "region": "Southwest", "population": 106000, "standards_framework": "TEKS", "language_standards": "ELPS", "website": "https://www.nisd.net", "display_order": 65},
    "orange-county-florida": {"name": "Orange County Public Schools", "abbreviation": "OCPS", "type": "large_urban_district", "parent_state": "florida", "region": "Southeast", "population": 210000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.ocps.net", "display_order": 66},
    "palm-beach-county": {"name": "School District of Palm Beach County", "abbreviation": "SDPBC", "type": "large_urban_district", "parent_state": "florida", "region": "Southeast", "population": 195000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.palmbeachschools.org", "display_order": 67},
    "philadelphia-schools": {"name": "School District of Philadelphia", "abbreviation": "SDP", "type": "large_urban_district", "parent_state": "pennsylvania", "region": "Northeast", "population": 200000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.philasd.org", "display_order": 68},
    "prince-georges-county": {"name": "Prince George's County Public Schools", "abbreviation": "PGCPS", "type": "large_urban_district", "parent_state": "maryland", "region": "Northeast", "population": 135000, "standards_framework": "CCSS", "language_standards": "WIDA", "website": "https://www.pgcps.org", "display_order": 69},
    "san-diego-unified": {"name": "San Diego Unified School District", "abbreviation": "SDUSD", "type": "large_urban_district", "parent_state": "california", "region": "West", "population": 120000, "standards_framework": "CCSS", "language_standards": "ELD", "website": "https://www.sandiegounified.org", "display_order": 70},
    "wake-county": {"name": "Wake County Public School System", "abbreviation": "WCPSS", "type": "large_urban_district", "parent_state": "north-carolina", "region": "Southeast", "population": 160000, "standards_framework": "State-Specific", "language_standards": "WIDA", "website": "https://www.wcpss.net", "display_order": 71},
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


def get_or_create_state_district_content_type(token: str) -> str:
    """Get existing State/District content type or create from template"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Check if State/District content type already exists
    print("\n📋 Checking for State/District content type...")
    response = requests.get(f"{API_BASE}/content-types", headers=headers)

    if response.status_code == 200:
        content_types = response.json()
        for ct in content_types:
            if ct["name"] == "State/District":
                print(f"✅ Found existing State/District content type: {ct['id']}")
                return ct["id"]

    # Need to create it - import from template
    print("📦 State/District content type not found, creating from template...")

    template_data = {
        "name": "State/District",
        "description": "Geographic region, state, or school district. Defines geographic taxonomies for organizing state-specific knowledge base files and compliance requirements.",
        "icon": "map-pin",
        "is_system": False,
        "attributes": [
            {
                "name": "district_code",
                "label": "District Code",
                "type": "text",
                "required": True,
                "help_text": "Unique identifier",
                "config": {"maxLength": 100},
                "order_index": 0,
            },
            {
                "name": "name",
                "label": "District Name",
                "type": "text",
                "required": True,
                "help_text": "Full display name",
                "config": {"maxLength": 200},
                "order_index": 1,
            },
            {
                "name": "abbreviation",
                "label": "Abbreviation",
                "type": "text",
                "required": False,
                "help_text": "Short abbreviation",
                "config": {"maxLength": 20},
                "order_index": 2,
            },
            {
                "name": "district_type",
                "label": "District Type",
                "type": "choice",
                "required": True,
                "help_text": "Type of geographic region",
                "config": {
                    "choices": ["state", "large_urban_district", "county", "region", "national"],
                    "multiple": False,
                },
                "order_index": 3,
            },
            {
                "name": "parent_state",
                "label": "Parent State",
                "type": "reference",
                "required": False,
                "help_text": "Parent state if this is a district",
                "config": {"targetContentType": "__SELF__", "multiple": False},
                "order_index": 4,
            },
            {
                "name": "region",
                "label": "Region",
                "type": "choice",
                "required": False,
                "help_text": "US region classification",
                "config": {
                    "choices": ["Northeast", "Southeast", "Midwest", "Southwest", "West", "Pacific", "Non-US"],
                    "multiple": False,
                },
                "order_index": 5,
            },
            {
                "name": "population",
                "label": "Student Population",
                "type": "number",
                "required": False,
                "help_text": "Approximate number of students served",
                "config": {"min": 0, "max": 10000000, "step": 1},
                "order_index": 6,
            },
            {
                "name": "knowledge_base_path",
                "label": "Knowledge Base Path",
                "type": "text",
                "required": False,
                "help_text": "Path to district directory in knowledge base",
                "config": {"maxLength": 200},
                "order_index": 7,
            },
            {
                "name": "standards_framework",
                "label": "Primary Standards Framework",
                "type": "choice",
                "required": False,
                "help_text": "Primary standards framework used",
                "config": {
                    "choices": ["TEKS", "CCSS", "NGSS", "State-Specific", "Custom"],
                    "multiple": False,
                },
                "order_index": 8,
            },
            {
                "name": "compliance_requirements",
                "label": "Compliance Requirements",
                "type": "json",
                "required": False,
                "help_text": "Array of state/district compliance requirements",
                "config": {},
                "order_index": 9,
            },
            {
                "name": "language_standards",
                "label": "Language Support Standards",
                "type": "text",
                "required": False,
                "help_text": "ELL/ESOL standards used",
                "config": {"maxLength": 100},
                "order_index": 10,
            },
            {
                "name": "website",
                "label": "Official Website",
                "type": "url",
                "required": False,
                "help_text": "Official state/district education website",
                "config": {},
                "order_index": 11,
            },
            {
                "name": "active",
                "label": "Active",
                "type": "boolean",
                "required": False,
                "help_text": "Whether this district is currently active",
                "config": {"default": True},
                "order_index": 12,
            },
            {
                "name": "display_order",
                "label": "Display Order",
                "type": "number",
                "required": False,
                "help_text": "Order for sorting in UI (lower numbers first)",
                "config": {"min": 0, "max": 1000, "step": 1},
                "order_index": 13,
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
    print(f"✅ Created State/District content type: {ct_id}")

    return ct_id


def create_content_instance(token: str, content_type_id: str, district_code: str, state_instances: Dict[str, str]) -> Optional[str]:
    """Create a content instance for a state/district"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Get metadata for this district
    metadata = STATE_DISTRICT_METADATA.get(district_code)
    if not metadata:
        print(f"⚠️  No metadata found for district: {district_code}")
        return None

    # Build instance data
    instance_data = {
        "district_code": district_code,
        "name": metadata["name"],
        "abbreviation": metadata["abbreviation"],
        "district_type": metadata["type"],
        "region": metadata["region"],
        "population": metadata["population"],
        "knowledge_base_path": f"/districts/{district_code}",
        "standards_framework": metadata["standards_framework"],
        "language_standards": metadata.get("language_standards"),
        "website": metadata.get("website"),
        "active": True,
        "display_order": metadata["display_order"],
    }

    # Add parent_state reference if this is a district
    if "parent_state" in metadata:
        parent_state_code = metadata["parent_state"]
        if parent_state_code in state_instances:
            instance_data["parent_state"] = state_instances[parent_state_code]
        else:
            print(f"⚠️  Parent state '{parent_state_code}' not found for {district_code}, will be set later")

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
        print(f"❌ Failed to create instance for {district_code}: {response.status_code}")
        print(response.text)
        return None

    instance = response.json()
    return instance["id"]


def import_states_districts(token: str):
    """Main import process"""
    # 1. Get or create State/District content type
    content_type_id = get_or_create_state_district_content_type(token)

    # 2. Find all district directories
    print(f"\n📁 Searching for districts in {DISTRICTS_PATH}...")
    if not DISTRICTS_PATH.exists():
        print(f"❌ Districts path does not exist: {DISTRICTS_PATH}")
        sys.exit(1)

    districts = []
    for item in DISTRICTS_PATH.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            districts.append(item.name)

    districts = sorted(districts)
    print(f"✅ Found {len(districts)} states/districts")

    # 3. Import states first (so districts can reference them)
    print(f"\n📝 Importing states first...")
    state_instances = {}  # Map of state_code → instance_id
    imported_states = []

    states = [d for d in districts if STATE_DISTRICT_METADATA.get(d, {}).get("type") == "state"]
    for i, district_code in enumerate(states, 1):
        print(f"   [{i}/{len(states)}] {district_code}")

        try:
            instance_id = create_content_instance(token, content_type_id, district_code, {})

            if instance_id:
                state_instances[district_code] = instance_id
                imported_states.append({
                    "district_code": district_code,
                    "name": STATE_DISTRICT_METADATA[district_code]["name"],
                    "instance_id": instance_id,
                })
                print(f"      ✓ Imported as {instance_id}")
            else:
                print(f"      ✗ Failed to import")

        except Exception as e:
            print(f"      ✗ Error: {e}")

    # 4. Import urban districts (now that states exist)
    print(f"\n📝 Importing urban districts...")
    imported_districts = []

    urban_districts = [d for d in districts if STATE_DISTRICT_METADATA.get(d, {}).get("type") != "state"]
    for i, district_code in enumerate(urban_districts, 1):
        print(f"   [{i}/{len(urban_districts)}] {district_code}")

        try:
            instance_id = create_content_instance(token, content_type_id, district_code, state_instances)

            if instance_id:
                imported_districts.append({
                    "district_code": district_code,
                    "name": STATE_DISTRICT_METADATA[district_code]["name"],
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
    print(f"✅ States Imported: {len(imported_states)}/{len(states)}")
    print(f"✅ Districts Imported: {len(imported_districts)}/{len(urban_districts)}")
    print(f"✅ Total: {len(imported_states) + len(imported_districts)}/{len(districts)}")
    print()

    if imported_states:
        print(f"Imported States ({len(imported_states)}):")
        for item in imported_states[:10]:  # Show first 10
            print(f"  ✓ {item['district_code']} → {item['name']}")
        if len(imported_states) > 10:
            print(f"  ... and {len(imported_states) - 10} more")
        print()

    if imported_districts:
        print(f"Imported Districts ({len(imported_districts)}):")
        for item in imported_districts:
            print(f"  ✓ {item['district_code']} → {item['name']}")
        print()


def main():
    """Main entry point"""
    print("=" * 70)
    print("States/Districts Import to Content Type System")
    print("=" * 70)
    print()

    # Login
    token = login()

    # Import
    import_states_districts(token)


if __name__ == "__main__":
    main()
