"""
Standards Import Service

Processes StandardImportJob records and transforms various format standards
(CASE, PDF, HTML, XML, JSON, CSV) into the standardized hierarchical structure.
"""
import json
import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import aiohttp
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class CASEParser:
    """Parser for CASE (Competency and Academic Standards Exchange) format."""

    # OAuth2 token cache
    _token_cache = {
        "access_token": None,
        "expires_at": None
    }

    async def _get_oauth2_token(
        self,
        client_id: str,
        client_secret: str,
        token_url: str = "https://casenetwork.1edtech.org/case-oauth2/clienttoken"
    ) -> str:
        """
        Get OAuth2 access token using client credentials grant.

        Args:
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            token_url: OAuth2 token endpoint

        Returns:
            Access token string

        Raises:
            ValueError: If authentication fails
        """
        # Check if we have a cached valid token
        if (self._token_cache["access_token"] and
            self._token_cache["expires_at"] and
            datetime.utcnow() < self._token_cache["expires_at"]):
            logger.info("Using cached OAuth2 token")
            return self._token_cache["access_token"]

        logger.info("Requesting new OAuth2 token from CASE Network")

        # Request new token
        async with aiohttp.ClientSession() as session:
            # OAuth2 client credentials grant
            auth = aiohttp.BasicAuth(client_id, client_secret)
            data = {
                "grant_type": "client_credentials"
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            async with session.post(token_url, auth=auth, data=data, headers=headers) as response:
                # Accept both 200 OK and 201 Created as success
                if response.status not in (200, 201):
                    error_text = await response.text()
                    logger.error(f"OAuth2 token request failed: {response.status} - {error_text}")
                    raise ValueError(
                        f"Failed to get OAuth2 token: HTTP {response.status}. "
                        f"Check your CASE Network credentials in Secrets."
                    )

                # Try to parse JSON, handle different content types
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    token_data = await response.json()
                else:
                    # Response might be JSON but with wrong content-type
                    text = await response.text()
                    try:
                        import json
                        token_data = json.loads(text)
                    except json.JSONDecodeError:
                        logger.error(f"OAuth2 response not JSON. Content-Type: {content_type}, Body: {text[:200]}")
                        raise ValueError(
                            f"OAuth2 endpoint returned non-JSON response (Content-Type: {content_type}). "
                            f"Check your CASE Network credentials."
                        )

        # Extract access token
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("OAuth2 response missing access_token")

        # Cache token (default to 1 hour if no expires_in)
        expires_in = token_data.get("expires_in", 3600)
        self._token_cache["access_token"] = access_token
        self._token_cache["expires_at"] = datetime.utcnow() + timedelta(seconds=expires_in - 60)  # Refresh 1 min early

        logger.info("Successfully obtained OAuth2 token")
        return access_token

    async def get_available_frameworks(
        self,
        base_url: str = "https://casenetwork.1edtech.org",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of available CASE frameworks from CASE Network.

        Args:
            base_url: Base URL for CASE Network API
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret

        Returns:
            List of CFDocuments with metadata:
            [
                {
                    "identifier": "uuid",
                    "uri": "full URI to CFPackage",
                    "title": "Framework title",
                    "description": "Framework description",
                    "subject": "Subject area",
                    "creator": "Organization"
                },
                ...
            ]

        Raises:
            ValueError: If authentication fails or API request fails
        """
        # Get OAuth2 token
        access_token = await self._get_oauth2_token(client_id, client_secret)

        # Prepare headers
        headers = {"Authorization": f"Bearer {access_token}"}

        # Fetch CFDocuments list using CASE v1.0 REST binding path
        documents_url = f"{base_url}/ims/case/v1p0/CFDocuments"
        params = {
            "limit": limit,
            "offset": offset
        }
        logger.info(f"Fetching available CASE frameworks from {documents_url} (limit={limit}, offset={offset})")

        async with aiohttp.ClientSession() as session:
            async with session.get(documents_url, headers=headers, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Failed to fetch CFDocuments: {response.status} - {error_text}")
                    raise ValueError(f"Failed to fetch available frameworks: HTTP {response.status}")

                # Try to parse JSON, handle different content types
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    data = await response.json()
                else:
                    # Response might be JSON but with wrong content-type
                    text = await response.text()
                    try:
                        import json as json_module
                        data = json_module.loads(text)
                    except json_module.JSONDecodeError:
                        logger.error(f"CFDocuments response not JSON. Content-Type: {content_type}, Body: {text[:200]}")
                        raise ValueError(
                            f"CFDocuments endpoint returned non-JSON response (Content-Type: {content_type}). "
                            f"The endpoint might not be available or requires different authentication."
                        )

        # Extract CFDocuments array
        cf_documents = data.get("CFDocuments", [])

        frameworks = []
        for doc in cf_documents:
            # Extract package URI (CFPackageURI is an object with 'title', 'identifier', and 'uri')
            package_uri = doc.get("CFPackageURI", {})
            uri = package_uri.get("uri") if isinstance(package_uri, dict) else None

            # If no URI provided, construct it using CASE v1.0 REST binding format
            doc_identifier = doc.get("identifier", "")
            if not uri and doc_identifier:
                uri = f"{base_url}/ims/case/v1p0/CFPackages/{doc_identifier}"

            # Extract subjects (may be array of URIs)
            subjects = doc.get("subjectURI", [])
            subject = subjects[0] if subjects else "General"

            frameworks.append({
                "identifier": doc_identifier,
                "uri": uri,
                "title": doc.get("title", "Untitled Framework"),
                "description": doc.get("description", ""),
                "subject": self._infer_subject(subjects) if subjects else "general",
                "creator": doc.get("creator", ""),
                "version": doc.get("version", ""),
                "adoptionStatus": doc.get("adoptionStatus", ""),
                "statusStartDate": doc.get("statusStartDate", ""),
                "statusEndDate": doc.get("statusEndDate", ""),
                "officialSourceURL": doc.get("officialSourceURL", ""),
                "lastChangeDateTime": doc.get("lastChangeDateTime", "")
            })

        logger.info(f"Found {len(frameworks)} available frameworks")
        return frameworks

    async def parse(
        self,
        source_location: str,
        use_oauth: bool = False,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Parse CASE format from URL.

        CASE is the IMS Global standard format for educational standards.
        Returns hierarchical structure with domains, strands, and standards.

        Args:
            source_location: URL to CASE API endpoint
            use_oauth: Whether to use OAuth2 authentication (for CASE Network)
            client_id: OAuth2 client ID (required if use_oauth=True)
            client_secret: OAuth2 client secret (required if use_oauth=True)

        Returns:
            Parsed CASE data with hierarchical structure
        """
        # Prepare headers
        headers = {}

        # Get OAuth2 token if needed
        if use_oauth:
            if not client_id or not client_secret:
                raise ValueError("client_id and client_secret required when use_oauth=True")

            access_token = await self._get_oauth2_token(client_id, client_secret)
            headers["Authorization"] = f"Bearer {access_token}"
            logger.info(f"Fetching CASE data from {source_location} with OAuth2")

        # Fetch CASE data
        async with aiohttp.ClientSession() as session:
            async with session.get(source_location, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Failed to fetch CASE data: {response.status} - {error_text}")
                    raise ValueError(f"Failed to fetch CASE data: HTTP {response.status}")

                data = await response.json()

        # CASE format structure
        # CFDocument contains metadata
        # CFItems are the hierarchical standards
        # CFAssociations define relationships

        cf_document = data.get("CFDocument", {})
        cf_items = data.get("CFItems", [])
        cf_associations = data.get("CFAssociations", [])

        # Build hierarchy from associations
        hierarchy = self._build_hierarchy(cf_items, cf_associations)

        # Extract standards into flat list
        standards_list = self._extract_standards_list(cf_items)

        return {
            "name": cf_document.get("title", ""),
            "description": cf_document.get("description", ""),
            "source_url": source_location,
            "version": cf_document.get("version", "1.0"),
            "subject": self._infer_subject(cf_document.get("subjectURI", [])),
            "grade_levels": self._extract_grade_levels(cf_document.get("educationLevel", [])),
            "structure": hierarchy,
            "standards_list": standards_list,
            "total_standards_count": len(standards_list)
        }

    def _build_hierarchy(
        self,
        items: List[Dict],
        associations: List[Dict]
    ) -> Dict[str, Any]:
        """Build hierarchical structure from CASE items and associations."""
        # If no associations, use fallback grade-level hierarchy
        if not associations:
            return self._build_hierarchy_fallback(items)

        # Create lookup maps
        items_by_id = {item["identifier"]: item for item in items}

        # Build parent-child relationships
        children_by_parent = {}
        for assoc in associations:
            if assoc.get("associationType") == "isChildOf":
                parent_id = assoc.get("destinationNodeURI", {}).get("identifier")
                child_id = assoc.get("originNodeURI", {}).get("identifier")

                if parent_id not in children_by_parent:
                    children_by_parent[parent_id] = []
                children_by_parent[parent_id].append(child_id)

        # Find root items (domains)
        root_items = []
        all_child_ids = set()
        for children in children_by_parent.values():
            all_child_ids.update(children)

        for item_id in items_by_id.keys():
            if item_id not in all_child_ids:
                root_items.append(item_id)

        # Build domain structure
        domains = []
        for domain_id in root_items:
            domain_item = items_by_id.get(domain_id)
            if not domain_item:
                continue

            domain = {
                "id": domain_item.get("humanCodingScheme", "") or f"DOMAIN-{domain_id[:8]}",
                "name": domain_item.get("fullStatement", "") or domain_item.get("title", "Unnamed Domain"),
                "strands": []
            }

            # Get strands (level 2)
            strand_ids = children_by_parent.get(domain_id, [])
            for strand_id in strand_ids:
                strand_item = items_by_id.get(strand_id)
                if not strand_item:
                    continue

                strand = {
                    "id": strand_item.get("humanCodingScheme", "") or f"STRAND-{strand_id[:8]}",
                    "name": strand_item.get("fullStatement", "") or strand_item.get("title", "Unnamed Strand"),
                    "standards": []
                }

                # Recursively collect all standards under this strand
                self._collect_standards_recursive(
                    strand_id,
                    children_by_parent,
                    items_by_id,
                    strand["standards"]
                )

                # Only add strand if it has standards
                if strand["standards"]:
                    domain["strands"].append(strand)

            # Only add domain if it has strands with standards
            if domain["strands"]:
                domains.append(domain)

        return {"domains": domains}

    def _collect_standards_recursive(
        self,
        parent_id: str,
        children_by_parent: Dict[str, List[str]],
        items_by_id: Dict[str, Dict],
        standards_list: List[Dict]
    ):
        """
        Recursively collect all standards (leaf nodes with code and text) under a parent node.
        """
        child_ids = children_by_parent.get(parent_id, [])

        for child_id in child_ids:
            child_item = items_by_id.get(child_id)
            if not child_item:
                continue

            # Check if this is a standard (has both code and text)
            code = child_item.get("humanCodingScheme", "")
            text = child_item.get("fullStatement", "")

            if code and text and len(code) > 0:
                # This is a standard - add it
                standards_list.append({
                    "code": code,
                    "text": text,
                    "grade_level": self._extract_single_grade(
                        child_item.get("educationLevel", [])
                    )
                })

            # Recurse into children to find more standards
            self._collect_standards_recursive(
                child_id,
                children_by_parent,
                items_by_id,
                standards_list
            )

    def _build_hierarchy_fallback(self, items: List[Dict]) -> Dict[str, Any]:
        """
        Build hierarchical structure from CASE items without associations.
        Groups standards by grade level when CFAssociations are not available.
        """
        # Extract all standards with both code and text
        standards_by_grade = {}
        for item in items:
            code = item.get("humanCodingScheme", "")
            text = item.get("fullStatement", "")

            # Only include items with both code and text
            if code and text and len(code) > 0:
                grade = self._extract_single_grade(item.get("educationLevel", []))
                grade_key = grade if grade else "General"

                if grade_key not in standards_by_grade:
                    standards_by_grade[grade_key] = []

                standards_by_grade[grade_key].append({
                    "code": code,
                    "text": text,
                    "grade_level": grade
                })

        # Build hierarchical structure organized by grade level
        domains = []

        # Sort grade levels: PK, K, then numeric grades
        def grade_sort_key(grade):
            if grade == "PK":
                return (0, 0)
            elif grade == "K":
                return (0, 1)
            elif grade.isdigit():
                return (1, int(grade))
            else:
                return (2, grade)

        sorted_grades = sorted(standards_by_grade.keys(), key=grade_sort_key)

        for grade in sorted_grades:
            grade_standards = standards_by_grade[grade]

            domain = {
                "id": f"GRADE-{grade}",
                "name": f"Grade {grade}" if grade != "General" else "General Standards",
                "strands": [{
                    "id": f"GRADE-{grade}-ALL",
                    "name": "All Standards",
                    "standards": grade_standards
                }]
            }
            domains.append(domain)

        return {"domains": domains}

    def _extract_standards_list(self, items: List[Dict]) -> List[Dict]:
        """Extract flat list of all standards."""
        standards = []
        for item in items:
            # Extract items that have both a code and a statement
            # This handles various CASE formats (some use CFItemType, some don't)
            code = item.get("humanCodingScheme", "")
            text = item.get("fullStatement", "")

            # Only include items with both code and text
            # Skip items that are just containers (no code or very short codes)
            if code and text and len(code) > 0:
                standards.append({
                    "code": code,
                    "text": text,
                    "grade_level": self._extract_single_grade(
                        item.get("educationLevel", [])
                    )
                })
        return standards

    def _infer_subject(self, subject_uris: List[str]) -> str:
        """Infer subject from CASE subject URIs."""
        subject_map = {
            "mathematics": "mathematics",
            "math": "mathematics",
            "english": "ela",
            "language arts": "ela",
            "ela": "ela",
            "science": "science",
            "social studies": "social_studies",
            "history": "social_studies",
            "computer science": "computer_science",
            "cs": "computer_science"
        }

        for uri in subject_uris:
            # Handle both string URIs and dict objects
            if isinstance(uri, dict):
                # Try to get URI or title from dict
                uri_str = uri.get("uri", "") or uri.get("title", "")
            else:
                uri_str = str(uri)

            if not uri_str:
                continue

            uri_lower = uri_str.lower()
            for key, value in subject_map.items():
                if key in uri_lower:
                    return value

        return "general"

    def _extract_grade_levels(self, education_levels: List[str]) -> List[str]:
        """Extract grade levels from CASE education level strings."""
        grades = set()
        for level in education_levels:
            # Common formats: "Grade 5", "Grades 3-5", "K", "PK"
            level_str = str(level).upper()

            if "PK" in level_str or "PRE-K" in level_str:
                grades.add("PK")
            elif "K" in level_str and "KINDERGARTEN" not in level_str:
                grades.add("K")

            # Extract numeric grades
            matches = re.findall(r'\d+', level_str)
            for match in matches:
                grade_num = int(match)
                if 1 <= grade_num <= 12:
                    grades.add(str(grade_num))

        return sorted(list(grades), key=lambda x: (x != "PK", x != "K", int(x) if x.isdigit() else 0))

    def _extract_single_grade(self, education_levels: List[str]) -> Optional[str]:
        """Extract single grade level for a standard."""
        grades = self._extract_grade_levels(education_levels)
        return grades[0] if grades else None


class HTMLParser:
    """Parser for HTML documents containing standards."""

    async def parse(self, source_location: str) -> Dict[str, Any]:
        """Parse standards from HTML document."""
        async with aiohttp.ClientSession() as session:
            async with session.get(source_location) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch HTML: HTTP {response.status}")

                html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        # Extract title
        title = soup.find('title')
        name = title.get_text() if title else "HTML Standard"

        # Try to find standards in common HTML structures
        standards_list = []

        # Look for standards in lists or tables
        for item in soup.find_all(['li', 'tr']):
            text = item.get_text().strip()
            if text and len(text) > 10:  # Minimum standard text length
                # Try to extract code from text
                code_match = re.match(r'^([\w\.\-]+)\s+', text)
                code = code_match.group(1) if code_match else f"STD-{len(standards_list) + 1}"

                standards_list.append({
                    "code": code,
                    "text": text,
                    "grade_level": None
                })

        return {
            "name": name,
            "description": "Imported from HTML",
            "source_url": source_location,
            "structure": {"domains": []},  # Flat structure for HTML
            "standards_list": standards_list,
            "total_standards_count": len(standards_list)
        }


class XMLParser:
    """Parser for XML documents containing standards."""

    async def parse(self, source_location: str) -> Dict[str, Any]:
        """Parse standards from XML document."""
        import xml.etree.ElementTree as ET

        async with aiohttp.ClientSession() as session:
            async with session.get(source_location) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch XML: HTTP {response.status}")

                xml_text = await response.text()

        root = ET.fromstring(xml_text)

        # Try to extract standards from common XML structures
        standards_list = []

        # Look for standard-like elements
        for elem in root.iter():
            if 'standard' in elem.tag.lower() or 'item' in elem.tag.lower():
                code = elem.get('code') or elem.get('id') or f"STD-{len(standards_list) + 1}"
                text = elem.text or elem.get('description') or ""

                if text.strip():
                    standards_list.append({
                        "code": code,
                        "text": text.strip(),
                        "grade_level": elem.get('grade')
                    })

        return {
            "name": root.get('title') or "XML Standard",
            "description": "Imported from XML",
            "source_url": source_location,
            "structure": {"domains": []},  # Flat structure for XML
            "standards_list": standards_list,
            "total_standards_count": len(standards_list)
        }


class JSONParser:
    """Parser for JSON documents containing standards."""

    async def parse(self, source_location: str) -> Dict[str, Any]:
        """Parse standards from JSON document."""
        async with aiohttp.ClientSession() as session:
            async with session.get(source_location) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch JSON: HTTP {response.status}")

                data = await response.json()

        # Try to extract standards from common JSON structures
        standards_list = []

        # If it's CASE format, delegate to CASE parser
        if "CFDocument" in data or "CFItems" in data:
            case_parser = CASEParser()
            return await case_parser.parse(source_location)

        # Otherwise, try to find array of standards
        standards_array = data.get('standards') or data.get('items') or []

        for idx, item in enumerate(standards_array):
            if isinstance(item, dict):
                code = item.get('code') or item.get('id') or f"STD-{idx + 1}"
                text = item.get('text') or item.get('description') or item.get('statement') or ""

                standards_list.append({
                    "code": code,
                    "text": text,
                    "grade_level": item.get('grade_level') or item.get('grade')
                })

        return {
            "name": data.get('name') or data.get('title') or "JSON Standard",
            "description": data.get('description') or "Imported from JSON",
            "source_url": source_location,
            "structure": {"domains": []},  # Flat structure for JSON
            "standards_list": standards_list,
            "total_standards_count": len(standards_list)
        }


class CSVParser:
    """Parser for CSV documents containing standards."""

    async def parse(self, source_location: str) -> Dict[str, Any]:
        """Parse standards from CSV document."""
        import csv
        import io

        async with aiohttp.ClientSession() as session:
            async with session.get(source_location) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch CSV: HTTP {response.status}")

                csv_text = await response.text()

        # Parse CSV
        reader = csv.DictReader(io.StringIO(csv_text))
        standards_list = []

        for row in reader:
            # Common CSV column names
            code = (
                row.get('code') or
                row.get('Code') or
                row.get('ID') or
                row.get('id') or
                f"STD-{len(standards_list) + 1}"
            )

            text = (
                row.get('text') or
                row.get('Text') or
                row.get('description') or
                row.get('Description') or
                row.get('standard') or
                row.get('Standard') or
                ""
            )

            grade = (
                row.get('grade') or
                row.get('Grade') or
                row.get('grade_level') or
                row.get('Grade Level')
            )

            if text.strip():
                standards_list.append({
                    "code": code,
                    "text": text.strip(),
                    "grade_level": grade
                })

        return {
            "name": "CSV Standard",
            "description": "Imported from CSV",
            "source_url": source_location,
            "structure": {"domains": []},  # Flat structure for CSV
            "standards_list": standards_list,
            "total_standards_count": len(standards_list)
        }


class PDFParser:
    """Parser for PDF documents containing standards."""

    async def parse(self, source_location: str) -> Dict[str, Any]:
        """
        Parse standards from PDF document.

        Uses PyPDF2 to extract text, then applies pattern matching to
        identify standards codes and descriptions.
        """
        try:
            import PyPDF2
            import io
            import tempfile
            import re

            # Download PDF
            async with aiohttp.ClientSession() as session:
                async with session.get(source_location) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to fetch PDF: HTTP {response.status}")

                    pdf_content = await response.read()

            # Parse PDF
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract all text
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text() + "\n"

            # Common Core format: Domain heading followed by numbered standards
            # Example: "Counting and Cardinality  K.CC" then "1. Count to 100..."
            # High School: "N-RN", "A-SSE", "F-IF", "G-CO", "S-ID"
            standards_list = []

            # Pattern for domain headings - captures both K-8 and high school formats
            # K-8: "K.CC", "1.OA", "5.NF"
            # High School: "N-RN", "A-SSE", "F-IF", "G-CO", "S-ID"
            domain_pattern = re.compile(r'\s+((?:(?:K|\d{1,2})\.[A-Z]{2,4})|(?:[A-ZGFNS]-[A-Z]{2,4}))\s*\n', re.MULTILINE)

            # Find all domain codes and their positions
            domain_matches = [(m.group(1), m.start(), m.end()) for m in domain_pattern.finditer(full_text)]

            if domain_matches:
                # Common Core format detected
                for i, (domain_code, start, end) in enumerate(domain_matches):
                    # Get text from this domain to the next (or end of document)
                    next_start = domain_matches[i + 1][1] if i + 1 < len(domain_matches) else len(full_text)
                    domain_text = full_text[end:next_start]

                    # Extract grade level from domain code
                    # K-8: "K" from "K.CC", "5" from "5.NF"
                    # High School: "HS" for all high school standards
                    if '.' in domain_code:
                        grade_level = domain_code.split('.')[0]
                    else:
                        # High school standard (e.g., N-RN, A-SSE)
                        grade_level = "HS"

                    # Find numbered standards in this domain (1., 2., 3., etc.)
                    # Match number at start of line followed by text until next number or section
                    std_pattern = re.compile(r'^\s*(\d+)\.\s+(.+?)(?=^\s*\d+\.|^\s*[A-Z][a-z]+\s+[a-z]+|\Z)', re.MULTILINE | re.DOTALL)

                    for std_num, std_text in std_pattern.findall(domain_text):
                        # Clean up the text
                        cleaned_text = std_text.strip().replace('\n', ' ').replace('\t', ' ')
                        # Remove multiple spaces
                        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

                        # Limit to first 500 characters for display
                        if len(cleaned_text) > 500:
                            cleaned_text = cleaned_text[:497] + "..."

                        standards_list.append({
                            "code": f"{domain_code}.{std_num}",
                            "text": cleaned_text,
                            "grade_level": grade_level,
                            "domain": domain_code
                        })

            # Fallback: Try explicit Grade.Domain.Standard format if no domains found
            if not standards_list:
                explicit_pattern = re.compile(r'((?:K|\d{1,2})\.[A-Z]{2,4}\.\d+)\s+(.+?)(?=\n(?:K|\d{1,2})\.[A-Z]{2,4}\.\d+|\n\n|\Z)', re.DOTALL)
                explicit_matches = explicit_pattern.findall(full_text)
                for code, text in explicit_matches:
                    cleaned_text = text.strip().replace('\n', ' ').replace('\t', ' ')
                    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)[:500]
                    standards_list.append({
                        "code": code,
                        "text": cleaned_text,
                        "grade_level": code.split('.')[0]
                    })

            # Last resort: split into pages
            if not standards_list:
                for idx, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text().strip()
                    if page_text:
                        standards_list.append({
                            "code": f"PAGE-{idx + 1}",
                            "text": page_text[:500],
                            "grade_level": None
                        })

            # Organize standards by grade level into CASE-compatible structure
            standards_by_grade = {}
            for std in standards_list:
                grade = std.get("grade_level") or "General"
                if grade not in standards_by_grade:
                    standards_by_grade[grade] = []
                standards_by_grade[grade].append(std)

            # Build CASE-compatible domain/strand structure
            domains = []
            for grade, grade_standards in sorted(standards_by_grade.items()):
                domain = {
                    "id": f"GRADE-{grade}",
                    "name": f"Grade {grade}" if grade != "General" else "General Standards",
                    "strands": [{
                        "id": f"GRADE-{grade}-ALL",
                        "name": "All Standards",
                        "standards": [
                            {
                                "code": s["code"],
                                "text": s["text"]
                            }
                            for s in grade_standards
                        ]
                    }]
                }
                domains.append(domain)

            structure = {"domains": domains}

            # Build standards_list in CASE format (code, text, grade_level only)
            standards_list_clean = [
                {
                    "code": s["code"],
                    "text": s["text"],
                    "grade_level": s.get("grade_level")
                }
                for s in standards_list
            ]

            # Extract unique grade levels
            grade_levels = sorted(list(set(
                s["grade_level"]
                for s in standards_list
                if s.get("grade_level")
            )))

            return {
                "name": "Standards from PDF",
                "description": f"Extracted {len(standards_list)} items from PDF document using PyPDF2 pattern matching",
                "source_url": source_location,
                "structure": structure,
                "standards_list": standards_list_clean,
                "total_standards_count": len(standards_list_clean),
                "grade_levels": grade_levels
            }

        except ImportError:
            return {
                "name": "PDF Standard",
                "description": "PyPDF2 library not installed",
                "source_url": source_location,
                "structure": {"domains": []},
                "standards_list": [],
                "total_standards_count": 0,
                "error": "PyPDF2 not installed. Run: pip install PyPDF2"
            }
        except Exception as e:
            return {
                "name": "PDF Standard",
                "description": f"Error parsing PDF: {str(e)}",
                "source_url": source_location,
                "structure": {"domains": []},
                "standards_list": [],
                "total_standards_count": 0,
                "error": str(e)
            }


class StandardsImportService:
    """Service for importing educational standards from various formats."""

    def __init__(self):
        self.parsers = {
            "case": CASEParser(),
            "html": HTMLParser(),
            "xml": XMLParser(),
            "json": JSONParser(),
            "csv": CSVParser(),
            "pdf": PDFParser(),
        }

    async def process_import_job(
        self,
        job_id: int,
        source_type: str,
        source_location: str,
        format: str,
        metadata: Dict[str, Any],
        db_session=None
    ) -> Dict[str, Any]:
        """
        Process a standards import job.

        Args:
            job_id: StandardImportJob ID
            source_type: url, file, api, case_network, or manual
            source_location: Location of the source data
            format: case, pdf, html, xml, json, csv, or manual
            metadata: Additional metadata (name, code, type, subject, etc.)
            db_session: Database session (required for case_network to retrieve secrets)

        Returns:
            Dict with:
                - success: bool
                - standard_id: int (if successful)
                - error_message: str (if failed)
                - standards_extracted: int
        """
        try:
            # Get appropriate parser
            parser = self.parsers.get(format)
            if not parser:
                return {
                    "success": False,
                    "error_message": f"Unknown format: {format}. Supported: case, html, xml, json, csv, pdf"
                }

            # Check if this is a CASE Network source (requires OAuth2)
            use_oauth = source_type == "case_network"
            client_id = None
            client_secret = None

            if use_oauth:
                # Retrieve CASE Network credentials from secrets
                if not db_session:
                    return {
                        "success": False,
                        "error_message": "Database session required for CASE Network authentication"
                    }

                from services.secrets_helper import get_secrets_helper
                secrets_helper = get_secrets_helper(db_session)
                credentials = secrets_helper.get_case_network_credentials()

                if not credentials:
                    return {
                        "success": False,
                        "error_message": (
                            "CASE Network credentials not found. "
                            "Please add 'case_network_key' secret with client ID and secret."
                        )
                    }

                client_id = credentials["client_id"]
                client_secret = credentials["client_secret"]
                logger.info("Retrieved CASE Network credentials from secrets")

            # Parse the source
            if format == "case" and isinstance(parser, CASEParser):
                # Pass OAuth2 params to CASE parser if needed
                parsed_data = await parser.parse(
                    source_location,
                    use_oauth=use_oauth,
                    client_id=client_id,
                    client_secret=client_secret
                )
            else:
                # Other parsers don't support OAuth2
                parsed_data = await parser.parse(source_location)

            # Check for parsing errors
            if "error" in parsed_data:
                return {
                    "success": False,
                    "error_message": parsed_data["error"]
                }

            # Merge with provided metadata (metadata takes precedence)
            final_data = {
                "name": metadata.get("name") or parsed_data.get("name", "Untitled Standard"),
                "short_name": metadata.get("short_name") or parsed_data.get("name", "")[:100],
                "code": metadata["code"],  # Required
                "description": metadata.get("description") or parsed_data.get("description"),
                "type": metadata["type"],  # Required
                "subject": metadata.get("subject") or parsed_data.get("subject", "general"),
                "source_organization": metadata["source_organization"],  # Required
                "source_url": source_location,
                "source_type": source_type,
                "source_format": format,
                "version": metadata.get("version") or parsed_data.get("version"),
                "year": metadata.get("year"),
                "state": metadata.get("state"),
                "district": metadata.get("district"),
                "country": metadata.get("country"),
                "grade_levels": metadata.get("grade_levels") or parsed_data.get("grade_levels", []),
                "structure": parsed_data.get("structure", {"domains": []}),
                "standards_list": parsed_data.get("standards_list", []),
                "total_standards_count": parsed_data.get("total_standards_count", 0)
            }

            return {
                "success": True,
                "parsed_data": final_data,
                "standards_extracted": final_data["total_standards_count"]
            }

        except Exception as e:
            return {
                "success": False,
                "error_message": f"Import failed: {str(e)}"
            }


# Singleton instance
_standards_import_service: Optional[StandardsImportService] = None


def get_standards_import_service() -> StandardsImportService:
    """Get or create the standards import service singleton."""
    global _standards_import_service
    if _standards_import_service is None:
        _standards_import_service = StandardsImportService()
    return _standards_import_service
