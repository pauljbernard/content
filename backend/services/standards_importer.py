"""
Standards Import Service

Processes StandardImportJob records and transforms various format standards
(CASE, PDF, HTML, XML, JSON, CSV) into the standardized hierarchical structure.
"""
import json
import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import aiohttp
from bs4 import BeautifulSoup


class CASEParser:
    """Parser for CASE (Competency and Academic Standards Exchange) format."""

    async def parse(self, source_location: str) -> Dict[str, Any]:
        """
        Parse CASE format from URL.

        CASE is the IMS Global standard format for educational standards.
        Returns hierarchical structure with domains, strands, and standards.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(source_location) as response:
                if response.status != 200:
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
                "id": domain_item.get("humanCodingScheme", ""),
                "name": domain_item.get("fullStatement", ""),
                "strands": []
            }

            # Get strands (level 2)
            strand_ids = children_by_parent.get(domain_id, [])
            for strand_id in strand_ids:
                strand_item = items_by_id.get(strand_id)
                if not strand_item:
                    continue

                strand = {
                    "id": strand_item.get("humanCodingScheme", ""),
                    "name": strand_item.get("fullStatement", ""),
                    "standards": []
                }

                # Get standards (level 3)
                standard_ids = children_by_parent.get(strand_id, [])
                for std_id in standard_ids:
                    std_item = items_by_id.get(std_id)
                    if not std_item:
                        continue

                    standard = {
                        "code": std_item.get("humanCodingScheme", ""),
                        "text": std_item.get("fullStatement", ""),
                        "grade_level": self._extract_single_grade(
                            std_item.get("educationLevel", [])
                        )
                    }
                    strand["standards"].append(standard)

                domain["strands"].append(strand)

            domains.append(domain)

        return {"domains": domains}

    def _extract_standards_list(self, items: List[Dict]) -> List[Dict]:
        """Extract flat list of all standards."""
        standards = []
        for item in items:
            # Only include leaf items (actual standards)
            if item.get("CFItemType") == "Standard":
                standards.append({
                    "code": item.get("humanCodingScheme", ""),
                    "text": item.get("fullStatement", ""),
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
            uri_lower = uri.lower()
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

        Note: PDF parsing requires external tools like pdftotext or PyPDF2.
        This is a simplified implementation that would need enhancement
        for production use.
        """
        # For now, return a placeholder
        # In production, you'd use PyPDF2 or pdfplumber
        return {
            "name": "PDF Standard",
            "description": "PDF parsing requires additional setup",
            "source_url": source_location,
            "structure": {"domains": []},
            "standards_list": [],
            "total_standards_count": 0,
            "error": "PDF parsing not yet implemented. Please use CASE, HTML, XML, JSON, or CSV formats."
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
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a standards import job.

        Args:
            job_id: StandardImportJob ID
            source_type: url, file, api, or manual
            source_location: Location of the source data
            format: case, pdf, html, xml, json, csv, or manual
            metadata: Additional metadata (name, code, type, subject, etc.)

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

            # Parse the source
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
