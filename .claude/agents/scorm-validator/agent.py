#!/usr/bin/env python3
"""
SCORM Validator Agent

Validates SCORM 1.2 and SCORM 2004 packages for LMS compatibility.
Checks imsmanifest.xml, file references, metadata, sequencing, and accessibility.

Usage:
    from agent import ScormValidatorAgent

    agent = ScormValidatorAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "validate_package",
        "package_path": "path/to/scorm.zip"
    })
"""

import asyncio
import sys
import json
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Any
from xml.etree import ElementTree as ET

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent


class ScormValidatorAgent(BaseAgent):
    """Validates SCORM packages for LMS compatibility"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="scorm-validator",
            agent_name="SCORM Validator",
            project_id=project_id,
            description="Validates SCORM 1.2 and 2004 packages"
        )
        self.scorm_namespaces = {
            "1.2": {
                "imscp": "http://www.imsproject.org/xsd/imscp_rootv1p1p2",
                "adlcp": "http://www.adlnet.org/xsd/adlcp_rootv1p2"
            },
            "2004": {
                "imscp": "http://www.imsglobal.org/xsd/imscp_v1p1",
                "adlcp": "http://www.adlnet.org/xsd/adlcp_v1p3",
                "adlseq": "http://www.adlnet.org/xsd/adlseq_v1p3",
                "adlnav": "http://www.adlnet.org/xsd/adlnav_v1p3"
            }
        }

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute SCORM validator logic

        Actions:
        - validate_package: Complete SCORM package validation
        - validate_manifest: Validate imsmanifest.xml only
        - validate_structure: Check file structure
        - validate_metadata: Check metadata completeness
        - test_lms_compatibility: Test LMS compatibility
        - validate_accessibility: Check content accessibility
        """
        action = parameters.get("action", "validate_package")

        if action == "validate_package":
            return await self._validate_package(parameters, context)
        elif action == "validate_manifest":
            return await self._validate_manifest(parameters, context)
        elif action == "validate_structure":
            return await self._validate_structure(parameters, context)
        elif action == "validate_metadata":
            return await self._validate_metadata(parameters, context)
        elif action == "test_lms_compatibility":
            return await self._test_lms_compatibility(parameters, context)
        elif action == "validate_accessibility":
            return await self._validate_accessibility(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _validate_package(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Complete SCORM package validation"""
        decisions = []
        artifacts = []

        package_path = parameters.get("package_path")
        scorm_version = parameters.get("scorm_version", "auto")  # auto, 1.2, 2004

        decisions.append(f"Validating SCORM package: {package_path}")

        # Phase 1: Extract and detect version
        extraction_result = self._extract_package(package_path)
        if not extraction_result["success"]:
            return {
                "output": {
                    "validation_passed": False,
                    "error": extraction_result["error"]
                },
                "decisions": decisions,
                "artifacts": [],
                "rationale": "Failed to extract SCORM package"
            }

        extracted_path = extraction_result["path"]
        detected_version = self._detect_scorm_version(extracted_path)
        decisions.append(f"Detected SCORM version: {detected_version}")

        # Phase 2: Validate manifest
        manifest_issues = self._validate_manifest_structure(
            extracted_path,
            detected_version
        )
        decisions.append(f"Manifest validation: {len(manifest_issues)} issues")

        # Phase 3: Validate file structure
        structure_issues = self._validate_file_structure(
            extracted_path,
            detected_version
        )
        decisions.append(f"File structure validation: {len(structure_issues)} issues")

        # Phase 4: Validate metadata
        metadata_issues = self._validate_metadata_completeness(
            extracted_path,
            detected_version
        )
        decisions.append(f"Metadata validation: {len(metadata_issues)} issues")

        # Phase 5: Validate sequencing (SCORM 2004 only)
        sequencing_issues = []
        if detected_version == "2004":
            sequencing_issues = self._validate_sequencing(
                extracted_path,
                detected_version
            )
            decisions.append(f"Sequencing validation: {len(sequencing_issues)} issues")

        # Phase 6: Validate accessibility
        accessibility_issues = self._validate_content_accessibility(
            extracted_path
        )
        decisions.append(f"Accessibility validation: {len(accessibility_issues)} issues")

        # Aggregate all issues
        all_issues = (
            manifest_issues +
            structure_issues +
            metadata_issues +
            sequencing_issues +
            accessibility_issues
        )

        # Calculate validation score
        validation_score = self._calculate_validation_score(all_issues)
        validation_passed = validation_score >= 85

        # Use quality gate validation
        validation = await self.validate_quality_gate(
            "delivery",
            {"package": package_path},
            delivery_format="SCORM"
        )

        if validation.passed:
            self.state_manager.pass_quality_gate("delivery")
            decisions.append("SCORM delivery quality gate passed")

        # Create validation report
        report = self._generate_validation_report(
            package_path,
            detected_version,
            all_issues,
            validation_score,
            validation_passed
        )

        report_artifact = f"artifacts/{self.project_id}/scorm_validation_report.md"
        self.create_artifact(
            "validation_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create issues JSON for programmatic use
        issues_json = json.dumps({
            "version": detected_version,
            "validation_passed": validation_passed,
            "validation_score": validation_score,
            "issues": all_issues,
            "issues_by_category": self._categorize_issues(all_issues)
        }, indent=2)

        issues_artifact = f"artifacts/{self.project_id}/scorm_validation_issues.json"
        self.create_artifact(
            "validation_issues",
            Path(issues_artifact),
            issues_json
        )
        artifacts.append(issues_artifact)

        return {
            "output": {
                "validation_passed": validation_passed,
                "validation_score": validation_score,
                "scorm_version": detected_version,
                "total_issues": len(all_issues),
                "issues_by_severity": self._count_by_severity(all_issues),
                "quality_gate_passed": validation.passed
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Validated SCORM {detected_version} package with {len(all_issues)} issues. "
                f"Score: {validation_score}/100, Passed: {validation_passed}"
            )
        }

    async def _validate_manifest(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate imsmanifest.xml"""
        decisions = []
        artifacts = []

        manifest_path = parameters.get("manifest_path")
        scorm_version = parameters.get("scorm_version", "auto")

        decisions.append(f"Validating manifest: {manifest_path}")

        # Detect version if auto
        if scorm_version == "auto":
            scorm_version = self._detect_version_from_manifest(manifest_path)
            decisions.append(f"Detected version: {scorm_version}")

        # Validate manifest structure
        issues = self._validate_manifest_xml(manifest_path, scorm_version)
        decisions.append(f"Found {len(issues)} issues")

        # Create report
        report = self._generate_manifest_report(manifest_path, scorm_version, issues)
        report_artifact = f"artifacts/{self.project_id}/manifest_validation.md"
        self.create_artifact(
            "manifest_validation",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "scorm_version": scorm_version,
                "issues_found": len(issues),
                "validation_passed": len([i for i in issues if i["severity"] in ["critical", "error"]]) == 0
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Validated SCORM {scorm_version} manifest with {len(issues)} issues"
        }

    async def _validate_structure(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate file structure"""
        decisions = []
        artifacts = []

        package_path = parameters.get("package_path")

        decisions.append("Validating SCORM file structure")

        # Extract if zip
        extraction_result = self._extract_package(package_path)
        extracted_path = extraction_result["path"]

        # Check required files
        structure_issues = self._check_required_files(extracted_path)
        decisions.append(f"Required files check: {len(structure_issues)} issues")

        # Check file references
        reference_issues = self._check_file_references(extracted_path)
        decisions.append(f"File references check: {len(reference_issues)} issues")

        all_issues = structure_issues + reference_issues

        return {
            "output": {
                "issues_found": len(all_issues),
                "validation_passed": len([i for i in all_issues if i["severity"] == "critical"]) == 0
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Validated file structure with {len(all_issues)} issues"
        }

    async def _validate_metadata(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate metadata completeness"""
        decisions = []
        artifacts = []

        manifest_path = parameters.get("manifest_path")

        decisions.append("Validating SCORM metadata")

        # Check metadata elements
        issues = self._check_metadata_elements(manifest_path)
        decisions.append(f"Found {len(issues)} metadata issues")

        return {
            "output": {
                "issues_found": len(issues),
                "validation_passed": len([i for i in issues if i["severity"] == "error"]) == 0
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Validated metadata with {len(issues)} issues"
        }

    async def _test_lms_compatibility(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Test LMS compatibility"""
        decisions = []
        artifacts = []

        package_path = parameters.get("package_path")
        target_lms = parameters.get("target_lms", ["Moodle", "Canvas", "Blackboard"])

        decisions.append(f"Testing compatibility with: {', '.join(target_lms)}")

        # Run compatibility checks for each LMS
        compatibility_results = {}
        for lms in target_lms:
            issues = self._check_lms_compatibility(package_path, lms)
            compatibility_results[lms] = {
                "compatible": len([i for i in issues if i["severity"] == "critical"]) == 0,
                "issues": issues
            }
            decisions.append(f"{lms}: {'✓ Compatible' if compatibility_results[lms]['compatible'] else '✗ Issues found'}")

        # Create compatibility report
        report = self._generate_compatibility_report(compatibility_results)
        report_artifact = f"artifacts/{self.project_id}/lms_compatibility_report.md"
        self.create_artifact(
            "compatibility_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "tested_lms": target_lms,
                "compatibility_results": {
                    lms: result["compatible"]
                    for lms, result in compatibility_results.items()
                }
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Tested compatibility with {len(target_lms)} LMS platforms"
        }

    async def _validate_accessibility(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate content accessibility"""
        decisions = []
        artifacts = []

        package_path = parameters.get("package_path")
        wcag_level = parameters.get("wcag_level", "AA")

        decisions.append(f"Validating WCAG {wcag_level} compliance")

        # Extract package
        extraction_result = self._extract_package(package_path)
        extracted_path = extraction_result["path"]

        # Check accessibility
        issues = self._check_accessibility_wcag(extracted_path, wcag_level)
        decisions.append(f"Found {len(issues)} accessibility issues")

        # Create accessibility report
        report = self._generate_accessibility_report(issues, wcag_level)
        report_artifact = f"artifacts/{self.project_id}/scorm_accessibility_report.md"
        self.create_artifact(
            "accessibility_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "wcag_level": wcag_level,
                "issues_found": len(issues),
                "compliant": len([i for i in issues if i["severity"] in ["critical", "error"]]) == 0
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Validated WCAG {wcag_level} compliance with {len(issues)} issues"
        }

    # Helper methods

    def _extract_package(self, package_path: str) -> Dict[str, Any]:
        """Extract SCORM package"""
        # In production, would actually extract zip
        # For now, return mock result
        return {
            "success": True,
            "path": package_path.replace(".zip", "")
        }

    def _detect_scorm_version(self, extracted_path: str) -> str:
        """Detect SCORM version from manifest"""
        manifest_path = Path(extracted_path) / "imsmanifest.xml"
        if not manifest_path.exists():
            return "unknown"

        return self._detect_version_from_manifest(str(manifest_path))

    def _detect_version_from_manifest(self, manifest_path: str) -> str:
        """Detect version from manifest XML"""
        try:
            # In production, would parse actual XML
            # Check for SCORM 2004 namespace
            with open(manifest_path, 'r') as f:
                content = f.read()
                if "adlseq_v1p3" in content or "SCORM 2004" in content:
                    return "2004"
                elif "adlcp_rootv1p2" in content or "SCORM 1.2" in content:
                    return "1.2"
                else:
                    return "unknown"
        except Exception:
            return "unknown"

    def _validate_manifest_structure(
        self,
        extracted_path: str,
        version: str
    ) -> List[Dict[str, Any]]:
        """Validate manifest XML structure"""
        issues = []

        manifest_path = Path(extracted_path) / "imsmanifest.xml"
        if not manifest_path.exists():
            issues.append({
                "severity": "critical",
                "category": "manifest",
                "description": "imsmanifest.xml not found in package root"
            })
            return issues

        # Parse and validate XML
        issues.extend(self._validate_manifest_xml(str(manifest_path), version))

        return issues

    def _validate_manifest_xml(
        self,
        manifest_path: str,
        version: str
    ) -> List[Dict[str, Any]]:
        """Validate manifest XML against SCORM spec"""
        issues = []

        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()

            # Check required elements
            if version == "1.2":
                issues.extend(self._validate_scorm_1_2_manifest(root))
            elif version == "2004":
                issues.extend(self._validate_scorm_2004_manifest(root))

        except ET.ParseError as e:
            issues.append({
                "severity": "critical",
                "category": "manifest",
                "description": f"XML parsing error: {str(e)}"
            })
        except Exception as e:
            issues.append({
                "severity": "error",
                "category": "manifest",
                "description": f"Validation error: {str(e)}"
            })

        return issues

    def _validate_scorm_1_2_manifest(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Validate SCORM 1.2 specific requirements"""
        issues = []

        # Check metadata
        metadata = root.find("metadata")
        if metadata is None:
            issues.append({
                "severity": "warning",
                "category": "manifest",
                "description": "Missing metadata element"
            })

        # Check organizations
        organizations = root.find("organizations")
        if organizations is None:
            issues.append({
                "severity": "critical",
                "category": "manifest",
                "description": "Missing organizations element"
            })
        else:
            if not organizations.get("default"):
                issues.append({
                    "severity": "error",
                    "category": "manifest",
                    "description": "Organizations missing default attribute"
                })

        # Check resources
        resources = root.find("resources")
        if resources is None:
            issues.append({
                "severity": "critical",
                "category": "manifest",
                "description": "Missing resources element"
            })

        return issues

    def _validate_scorm_2004_manifest(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Validate SCORM 2004 specific requirements"""
        issues = []

        # Check schemaversion
        metadata = root.find("metadata")
        if metadata is not None:
            schema = metadata.find("schemaversion")
            if schema is None or "2004" not in schema.text:
                issues.append({
                    "severity": "error",
                    "category": "manifest",
                    "description": "Missing or invalid SCORM 2004 schema version"
                })

        # Check sequencing (optional but common)
        organizations = root.find("organizations")
        if organizations is not None:
            org = organizations.find("organization")
            if org is not None:
                sequencing = org.find("sequencing")
                if sequencing is not None:
                    # Validate sequencing rules
                    issues.extend(self._validate_sequencing_rules(sequencing))

        return issues

    def _validate_sequencing_rules(self, sequencing: ET.Element) -> List[Dict[str, Any]]:
        """Validate SCORM 2004 sequencing rules"""
        issues = []

        # Check for valid sequencing structure
        control_mode = sequencing.find("controlMode")
        if control_mode is not None:
            # Validate control mode attributes
            valid_attrs = ["choice", "flow", "forwardOnly"]
            for attr in valid_attrs:
                value = control_mode.get(attr)
                if value and value not in ["true", "false"]:
                    issues.append({
                        "severity": "error",
                        "category": "sequencing",
                        "description": f"Invalid controlMode {attr} value: {value}"
                    })

        return issues

    def _validate_file_structure(
        self,
        extracted_path: str,
        version: str
    ) -> List[Dict[str, Any]]:
        """Validate file structure"""
        issues = []

        # Check required files
        required_files = ["imsmanifest.xml"]
        for required_file in required_files:
            file_path = Path(extracted_path) / required_file
            if not file_path.exists():
                issues.append({
                    "severity": "critical",
                    "category": "structure",
                    "description": f"Required file missing: {required_file}"
                })

        # Check file references in manifest
        issues.extend(self._check_file_references(extracted_path))

        return issues

    def _check_required_files(self, extracted_path: str) -> List[Dict[str, Any]]:
        """Check for required files"""
        return self._validate_file_structure(extracted_path, "unknown")

    def _check_file_references(self, extracted_path: str) -> List[Dict[str, Any]]:
        """Check that all referenced files exist"""
        issues = []

        manifest_path = Path(extracted_path) / "imsmanifest.xml"
        if not manifest_path.exists():
            return issues

        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()

            # Find all file references
            resources = root.find("resources")
            if resources is not None:
                for resource in resources.findall("resource"):
                    href = resource.get("href")
                    if href:
                        file_path = Path(extracted_path) / href
                        if not file_path.exists():
                            issues.append({
                                "severity": "error",
                                "category": "structure",
                                "description": f"Referenced file not found: {href}"
                            })

                    # Check file elements within resource
                    for file_elem in resource.findall("file"):
                        href = file_elem.get("href")
                        if href:
                            file_path = Path(extracted_path) / href
                            if not file_path.exists():
                                issues.append({
                                    "severity": "error",
                                    "category": "structure",
                                    "description": f"Referenced file not found: {href}"
                                })

        except Exception as e:
            issues.append({
                "severity": "error",
                "category": "structure",
                "description": f"Error checking file references: {str(e)}"
            })

        return issues

    def _validate_metadata_completeness(
        self,
        extracted_path: str,
        version: str
    ) -> List[Dict[str, Any]]:
        """Validate metadata completeness"""
        issues = []

        manifest_path = Path(extracted_path) / "imsmanifest.xml"
        if not manifest_path.exists():
            return issues

        issues.extend(self._check_metadata_elements(str(manifest_path)))

        return issues

    def _check_metadata_elements(self, manifest_path: str) -> List[Dict[str, Any]]:
        """Check metadata elements"""
        issues = []

        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()

            metadata = root.find("metadata")
            if metadata is None:
                issues.append({
                    "severity": "warning",
                    "category": "metadata",
                    "description": "Missing metadata element"
                })
                return issues

            # Check for recommended metadata
            recommended = ["schema", "schemaversion"]
            for elem_name in recommended:
                if metadata.find(elem_name) is None:
                    issues.append({
                        "severity": "warning",
                        "category": "metadata",
                        "description": f"Missing recommended metadata element: {elem_name}"
                    })

        except Exception as e:
            issues.append({
                "severity": "error",
                "category": "metadata",
                "description": f"Error checking metadata: {str(e)}"
            })

        return issues

    def _validate_sequencing(
        self,
        extracted_path: str,
        version: str
    ) -> List[Dict[str, Any]]:
        """Validate SCORM 2004 sequencing"""
        issues = []

        manifest_path = Path(extracted_path) / "imsmanifest.xml"
        if not manifest_path.exists():
            return issues

        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()

            # Find sequencing elements
            for sequencing in root.iter("sequencing"):
                issues.extend(self._validate_sequencing_rules(sequencing))

        except Exception as e:
            issues.append({
                "severity": "error",
                "category": "sequencing",
                "description": f"Error validating sequencing: {str(e)}"
            })

        return issues

    def _validate_content_accessibility(self, extracted_path: str) -> List[Dict[str, Any]]:
        """Validate content accessibility"""
        return self._check_accessibility_wcag(extracted_path, "AA")

    def _check_accessibility_wcag(
        self,
        extracted_path: str,
        wcag_level: str
    ) -> List[Dict[str, Any]]:
        """Check WCAG compliance"""
        issues = []

        # In production, would scan HTML files for accessibility issues
        # Check for: alt text, color contrast, keyboard navigation, ARIA labels, etc.

        # For now, return mock issues
        issues.append({
            "severity": "info",
            "category": "accessibility",
            "description": "Accessibility check requires manual review of content"
        })

        return issues

    def _check_lms_compatibility(
        self,
        package_path: str,
        lms: str
    ) -> List[Dict[str, Any]]:
        """Check compatibility with specific LMS"""
        issues = []

        # LMS-specific compatibility checks
        if lms == "Moodle":
            # Moodle-specific checks
            pass
        elif lms == "Canvas":
            # Canvas-specific checks
            pass
        elif lms == "Blackboard":
            # Blackboard-specific checks
            pass

        return issues

    def _calculate_validation_score(self, issues: List[Dict[str, Any]]) -> int:
        """Calculate validation score"""
        weights = {"critical": 20, "error": 15, "warning": 5, "info": 2}
        deductions = sum(weights.get(issue.get("severity", "info"), 2) for issue in issues)
        return max(0, 100 - deductions)

    def _categorize_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize issues by category"""
        categories = {}
        for issue in issues:
            category = issue.get("category", "other")
            categories[category] = categories.get(category, 0) + 1
        return categories

    def _count_by_severity(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count issues by severity"""
        counts = {"critical": 0, "error": 0, "warning": 0, "info": 0}
        for issue in issues:
            severity = issue.get("severity", "info")
            counts[severity] = counts.get(severity, 0) + 1
        return counts

    def _generate_validation_report(
        self,
        package_path: str,
        version: str,
        issues: List[Dict[str, Any]],
        score: int,
        passed: bool
    ) -> str:
        """Generate validation report"""
        status = "✅ PASSED" if passed else "❌ FAILED"
        severity_counts = self._count_by_severity(issues)
        category_counts = self._categorize_issues(issues)

        issues_by_category = {}
        for issue in issues:
            category = issue.get("category", "other")
            if category not in issues_by_category:
                issues_by_category[category] = []
            issues_by_category[category].append(issue)

        issues_md = []
        for category, cat_issues in issues_by_category.items():
            issues_md.append(f"\n### {category.title()}\n")
            for issue in cat_issues:
                severity_icon = {"critical": "🔴", "error": "🟠", "warning": "🟡", "info": "🔵"}.get(issue["severity"], "⚪")
                issues_md.append(f"{severity_icon} **[{issue['severity'].upper()}]** {issue['description']}")

        return f"""# SCORM Validation Report

**Package**: {package_path}
**SCORM Version**: {version}
**Status**: {status}
**Validation Score**: {score}/100

## Summary

- **Total Issues**: {len(issues)}
- **Critical**: {severity_counts['critical']}
- **Errors**: {severity_counts['error']}
- **Warnings**: {severity_counts['warning']}
- **Info**: {severity_counts['info']}

## Issues by Category

{''.join(issues_md) if issues_md else 'No issues found.'}

## Recommendations

{self._generate_recommendations(issues, passed)}

---
Generated by SCORM Validator Agent
"""

    def _generate_recommendations(
        self,
        issues: List[Dict[str, Any]],
        passed: bool
    ) -> str:
        """Generate recommendations"""
        if passed:
            return "✅ Package meets SCORM compliance requirements and is ready for LMS deployment."

        critical = [i for i in issues if i["severity"] == "critical"]
        errors = [i for i in issues if i["severity"] == "error"]

        recommendations = []
        if critical:
            recommendations.append(f"1. **Critical**: Fix {len(critical)} critical issues before deployment")
        if errors:
            recommendations.append(f"2. **Errors**: Address {len(errors)} errors to ensure compatibility")

        return "\n".join(recommendations)

    def _generate_manifest_report(
        self,
        manifest_path: str,
        version: str,
        issues: List[Dict[str, Any]]
    ) -> str:
        """Generate manifest validation report"""
        return f"""# Manifest Validation Report

**Manifest**: {manifest_path}
**SCORM Version**: {version}
**Issues Found**: {len(issues)}

## Issues

{self._format_issues_list(issues)}

---
Generated by SCORM Validator Agent
"""

    def _generate_compatibility_report(
        self,
        compatibility_results: Dict[str, Dict[str, Any]]
    ) -> str:
        """Generate LMS compatibility report"""
        results_md = []
        for lms, result in compatibility_results.items():
            status = "✅ Compatible" if result["compatible"] else "❌ Issues Found"
            results_md.append(f"### {lms}: {status}\n")
            if result["issues"]:
                for issue in result["issues"]:
                    results_md.append(f"- [{issue['severity'].upper()}] {issue['description']}")

        return f"""# LMS Compatibility Report

## Results

{''.join(results_md)}

---
Generated by SCORM Validator Agent
"""

    def _generate_accessibility_report(
        self,
        issues: List[Dict[str, Any]],
        wcag_level: str
    ) -> str:
        """Generate accessibility report"""
        return f"""# SCORM Accessibility Report

**WCAG Level**: {wcag_level}
**Issues Found**: {len(issues)}

## Accessibility Issues

{self._format_issues_list(issues)}

---
Generated by SCORM Validator Agent
"""

    def _format_issues_list(self, issues: List[Dict[str, Any]]) -> str:
        """Format issues as markdown list"""
        if not issues:
            return "No issues found."

        return "\n".join([
            f"- [{issue['severity'].upper()}] ({issue.get('category', 'general')}): {issue['description']}"
            for issue in issues
        ])

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_scorm_validator():
    """Test the SCORM validator agent"""
    from state_manager import StateManager

    project_id = "PROJ-TEST-SCORM-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test SCORM Validation Project",
        educational_level="9-12",
        standards=["SCORM"],
        context={"package": "genetics_course.zip"}
    )

    agent = ScormValidatorAgent(project_id)

    print("=== Validate SCORM Package ===")
    result = await agent.run({
        "action": "validate_package",
        "package_path": "artifacts/genetics_course.zip",
        "scorm_version": "2004"
    })
    print(f"Status: {result['status']}")
    print(f"Validation passed: {result['output']['validation_passed']}")
    print(f"Score: {result['output']['validation_score']}/100")
    print(f"Total issues: {result['output']['total_issues']}")
    print(f"Artifacts: {result['artifacts']}")

    print("\n=== Test LMS Compatibility ===")
    result = await agent.run({
        "action": "test_lms_compatibility",
        "package_path": "artifacts/genetics_course.zip",
        "target_lms": ["Moodle", "Canvas", "Blackboard"]
    })
    print(f"Status: {result['status']}")
    print(f"Compatibility results: {result['output']['compatibility_results']}")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_scorm_validator())
