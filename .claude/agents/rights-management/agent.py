#!/usr/bin/env python3
"""
Rights Management Agent

Manages content licenses, permissions, attribution, and copyright compliance.
Tracks usage rights, generates license documentation, and ensures legal compliance.

Usage:
    from agent import RightsManagementAgent

    agent = RightsManagementAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "assign_license",
        "content_id": "CONTENT-001",
        "license_type": "CC-BY-4.0"
    })
"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent


class RightsManagementAgent(BaseAgent):
    """Manages content rights, licenses, and permissions"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="rights-management",
            agent_name="Rights Management",
            project_id=project_id,
            description="Manages content licenses, permissions, and copyright"
        )
        self.license_types = {
            "CC-BY-4.0": "Creative Commons Attribution 4.0",
            "CC-BY-SA-4.0": "Creative Commons Attribution-ShareAlike 4.0",
            "CC-BY-NC-4.0": "Creative Commons Attribution-NonCommercial 4.0",
            "CC-BY-NC-SA-4.0": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0",
            "CC0-1.0": "Creative Commons Zero (Public Domain)",
            "MIT": "MIT License",
            "Apache-2.0": "Apache License 2.0",
            "Proprietary": "All Rights Reserved"
        }

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute rights management logic

        Actions:
        - assign_license: Assign license to content
        - check_permissions: Check usage permissions
        - generate_attribution: Generate attribution text
        - audit_compliance: Audit copyright compliance
        - track_usage_rights: Track content usage rights
        - manage_agreements: Manage licensing agreements
        """
        action = parameters.get("action", "assign_license")

        if action == "assign_license":
            return await self._assign_license(parameters, context)
        elif action == "check_permissions":
            return await self._check_permissions(parameters, context)
        elif action == "generate_attribution":
            return await self._generate_attribution(parameters, context)
        elif action == "audit_compliance":
            return await self._audit_compliance(parameters, context)
        elif action == "track_usage_rights":
            return await self._track_usage_rights(parameters, context)
        elif action == "manage_agreements":
            return await self._manage_agreements(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _assign_license(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assign license to content"""
        decisions = []
        artifacts = []

        content_id = parameters.get("content_id")
        license_type = parameters.get("license_type")
        copyright_holder = parameters.get("copyright_holder", "Content Creator")
        effective_date = parameters.get("effective_date", datetime.utcnow().isoformat() + "Z")

        if license_type not in self.license_types:
            return {
                "output": {"error": f"Invalid license type: {license_type}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"License type {license_type} not recognized"
            }

        decisions.append(f"Assigning {license_type} license to {content_id}")
        decisions.append(f"Copyright holder: {copyright_holder}")

        # Create license record
        license_record = {
            "content_id": content_id,
            "license_type": license_type,
            "license_full_name": self.license_types[license_type],
            "copyright_holder": copyright_holder,
            "effective_date": effective_date,
            "permissions": self._get_license_permissions(license_type)
        }

        # Generate license file
        license_text = self._generate_license_text(license_record)

        license_artifact = f"artifacts/{self.project_id}/LICENSE_{content_id}.md"
        self.create_artifact(
            "license",
            Path(license_artifact),
            license_text
        )
        artifacts.append(license_artifact)

        # Create license metadata JSON
        metadata_artifact = f"artifacts/{self.project_id}/license_metadata_{content_id}.json"
        self.create_artifact(
            "license_metadata",
            Path(metadata_artifact),
            json.dumps(license_record, indent=2)
        )
        artifacts.append(metadata_artifact)

        decisions.append(f"Generated license documentation")

        return {
            "output": {
                "content_id": content_id,
                "license_type": license_type,
                "copyright_holder": copyright_holder,
                "permissions": license_record["permissions"]
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Assigned {license_type} license to {content_id} "
                f"with holder {copyright_holder}"
            )
        }

    async def _check_permissions(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check usage permissions"""
        decisions = []
        artifacts = []

        content_id = parameters.get("content_id")
        intended_use = parameters.get("intended_use")  # commercial, educational, derivative, etc.
        user_type = parameters.get("user_type", "general")  # general, educational, commercial

        decisions.append(f"Checking permissions for {intended_use} use of {content_id}")

        # Get content license
        license_info = self._get_content_license(content_id)
        decisions.append(f"Content license: {license_info['license_type']}")

        # Check if use is permitted
        permission_check = self._verify_permission(
            license_info,
            intended_use,
            user_type
        )

        decisions.append(
            f"Permission {'granted' if permission_check['permitted'] else 'denied'}"
        )

        # Generate permission report
        report = self._generate_permission_report(
            content_id,
            intended_use,
            user_type,
            license_info,
            permission_check
        )

        report_artifact = f"artifacts/{self.project_id}/permission_check_{content_id}.md"
        self.create_artifact(
            "permission_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "content_id": content_id,
                "intended_use": intended_use,
                "permitted": permission_check["permitted"],
                "conditions": permission_check.get("conditions", []),
                "restrictions": permission_check.get("restrictions", [])
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Checked {intended_use} permissions for {content_id}: "
                f"{'permitted' if permission_check['permitted'] else 'denied'}"
            )
        }

    async def _generate_attribution(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate attribution text"""
        decisions = []
        artifacts = []

        content_id = parameters.get("content_id")
        format_type = parameters.get("format", "text")  # text, html, markdown

        decisions.append(f"Generating {format_type} attribution for {content_id}")

        # Get content metadata
        metadata = self._get_content_metadata(content_id)
        decisions.append(f"Loaded content metadata")

        # Generate attribution
        attribution = self._create_attribution(metadata, format_type)
        decisions.append(f"Generated attribution in {format_type} format")

        # Create attribution file
        file_extension = {"text": "txt", "html": "html", "markdown": "md"}[format_type]
        attribution_artifact = f"artifacts/{self.project_id}/ATTRIBUTION_{content_id}.{file_extension}"
        self.create_artifact(
            "attribution",
            Path(attribution_artifact),
            attribution
        )
        artifacts.append(attribution_artifact)

        return {
            "output": {
                "content_id": content_id,
                "format": format_type,
                "attribution_text": attribution
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Generated {format_type} attribution for {content_id}"
        }

    async def _audit_compliance(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Audit copyright compliance"""
        decisions = []
        artifacts = []

        content_path = parameters.get("content_path")
        check_types = parameters.get("check_types", [
            "licenses", "attributions", "permissions", "third_party"
        ])

        decisions.append(f"Auditing compliance for content at {content_path}")
        decisions.append(f"Checking: {', '.join(check_types)}")

        # Perform compliance checks
        compliance_results = {}
        total_issues = 0

        for check_type in check_types:
            result = self._perform_compliance_check(content_path, check_type)
            compliance_results[check_type] = result
            total_issues += len(result["issues"])
            decisions.append(
                f"{check_type}: {len(result['issues'])} issues found"
            )

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(compliance_results)
        decisions.append(f"Compliance score: {compliance_score}/100")

        # Generate compliance report
        report = self._generate_compliance_report(
            content_path,
            compliance_results,
            compliance_score
        )

        report_artifact = f"artifacts/{self.project_id}/copyright_compliance_audit.md"
        self.create_artifact(
            "compliance_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Generate remediation plan if needed
        if total_issues > 0:
            remediation = self._generate_remediation_plan(compliance_results)
            remediation_artifact = f"artifacts/{self.project_id}/compliance_remediation.md"
            self.create_artifact(
                "remediation_plan",
                Path(remediation_artifact),
                remediation
            )
            artifacts.append(remediation_artifact)
            decisions.append("Generated remediation plan")

        return {
            "output": {
                "compliance_score": compliance_score,
                "total_issues": total_issues,
                "checks_performed": len(check_types),
                "compliant": total_issues == 0
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Audited copyright compliance with score {compliance_score}/100 "
                f"and {total_issues} issues found"
            )
        }

    async def _track_usage_rights(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track content usage rights"""
        decisions = []
        artifacts = []

        content_id = parameters.get("content_id")
        usage_event = parameters.get("usage_event")  # distributed, modified, embedded, etc.
        user_id = parameters.get("user_id")

        decisions.append(f"Tracking {usage_event} usage of {content_id} by {user_id}")

        # Record usage
        usage_record = {
            "content_id": content_id,
            "usage_event": usage_event,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Check if usage complies with license
        compliance_check = self._check_usage_compliance(
            content_id,
            usage_event,
            user_id
        )

        decisions.append(
            f"Usage compliance: {'compliant' if compliance_check['compliant'] else 'violation'}"
        )

        if not compliance_check["compliant"]:
            decisions.append(f"Violation reason: {compliance_check['reason']}")

        # Create usage record
        record_artifact = f"artifacts/{self.project_id}/usage_record_{content_id}_{int(datetime.utcnow().timestamp())}.json"
        self.create_artifact(
            "usage_record",
            Path(record_artifact),
            json.dumps({
                **usage_record,
                "compliance_check": compliance_check
            }, indent=2)
        )
        artifacts.append(record_artifact)

        return {
            "output": {
                "content_id": content_id,
                "usage_event": usage_event,
                "compliant": compliance_check["compliant"],
                "tracked": True
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Tracked {usage_event} usage of {content_id}, "
                f"compliance: {compliance_check['compliant']}"
            )
        }

    async def _manage_agreements(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Manage licensing agreements"""
        decisions = []
        artifacts = []

        operation = parameters.get("operation", "create")  # create, list, update, expire
        agreement_type = parameters.get("agreement_type", "content_license")

        decisions.append(f"Managing agreements: {operation}")

        if operation == "create":
            agreement_id = self._create_agreement(parameters)
            decisions.append(f"Created agreement: {agreement_id}")

            output = {
                "operation": "create",
                "agreement_id": agreement_id,
                "agreement_type": agreement_type
            }

        elif operation == "list":
            agreements = self._list_agreements()
            decisions.append(f"Listed {len(agreements)} agreements")

            output = {
                "operation": "list",
                "agreement_count": len(agreements),
                "agreements": agreements
            }

        elif operation == "update":
            agreement_id = parameters.get("agreement_id")
            updates = parameters.get("updates", {})
            self._update_agreement(agreement_id, updates)
            decisions.append(f"Updated agreement: {agreement_id}")

            output = {
                "operation": "update",
                "agreement_id": agreement_id,
                "updates_applied": len(updates)
            }

        elif operation == "expire":
            agreement_id = parameters.get("agreement_id")
            self._expire_agreement(agreement_id)
            decisions.append(f"Expired agreement: {agreement_id}")

            output = {
                "operation": "expire",
                "agreement_id": agreement_id,
                "expired": True
            }

        else:
            output = {"error": f"Unknown operation: {operation}"}

        # Create agreement management report
        report = self._generate_agreement_report(operation, output)

        report_artifact = f"artifacts/{self.project_id}/agreement_management.md"
        self.create_artifact(
            "agreement_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": output,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Executed {operation} operation for agreements"
        }

    # Helper methods

    def _get_license_permissions(self, license_type: str) -> Dict[str, bool]:
        """Get permissions for license type"""
        permissions = {
            "CC-BY-4.0": {
                "commercial_use": True,
                "modifications": True,
                "distribution": True,
                "attribution_required": True
            },
            "CC-BY-SA-4.0": {
                "commercial_use": True,
                "modifications": True,
                "distribution": True,
                "attribution_required": True,
                "share_alike": True
            },
            "CC-BY-NC-4.0": {
                "commercial_use": False,
                "modifications": True,
                "distribution": True,
                "attribution_required": True
            },
            "Proprietary": {
                "commercial_use": False,
                "modifications": False,
                "distribution": False,
                "attribution_required": True
            }
        }
        return permissions.get(license_type, {})

    def _generate_license_text(self, license_record: Dict[str, Any]) -> str:
        """Generate license text"""
        permissions_md = "\n".join([
            f"- **{k.replace('_', ' ').title()}**: {'✓ Yes' if v else '✗ No'}"
            for k, v in license_record["permissions"].items()
        ])

        return f"""# License

**License Type**: {license_record['license_full_name']}
**Content ID**: {license_record['content_id']}
**Copyright Holder**: {license_record['copyright_holder']}
**Effective Date**: {license_record['effective_date']}

## Permissions

{permissions_md}

## Full License Text

See: https://creativecommons.org/licenses/ for full license details.

---
Generated by Rights Management Agent
"""

    def _get_content_license(self, content_id: str) -> Dict[str, Any]:
        """Get content license info"""
        # Mock license retrieval
        return {
            "content_id": content_id,
            "license_type": "CC-BY-4.0",
            "copyright_holder": "Content Creator",
            "permissions": self._get_license_permissions("CC-BY-4.0")
        }

    def _verify_permission(
        self,
        license_info: Dict[str, Any],
        intended_use: str,
        user_type: str
    ) -> Dict[str, Any]:
        """Verify if use is permitted"""
        permissions = license_info["permissions"]

        # Check commercial use
        if intended_use == "commercial":
            permitted = permissions.get("commercial_use", False)
            return {
                "permitted": permitted,
                "conditions": ["Attribution required"] if permitted else [],
                "restrictions": ["Commercial use not permitted"] if not permitted else []
            }

        # Check modifications
        if intended_use == "derivative":
            permitted = permissions.get("modifications", False)
            conditions = ["Attribution required"]
            if permissions.get("share_alike"):
                conditions.append("Share-Alike: derivatives must use same license")
            return {
                "permitted": permitted,
                "conditions": conditions if permitted else [],
                "restrictions": ["Modifications not permitted"] if not permitted else []
            }

        # Default: educational use usually permitted
        return {
            "permitted": True,
            "conditions": ["Attribution required"],
            "restrictions": []
        }

    def _generate_permission_report(
        self,
        content_id: str,
        intended_use: str,
        user_type: str,
        license_info: Dict[str, Any],
        permission_check: Dict[str, Any]
    ) -> str:
        """Generate permission report"""
        status = "✅ PERMITTED" if permission_check["permitted"] else "❌ DENIED"

        conditions_md = "\n".join([f"- {c}" for c in permission_check.get("conditions", [])]) or "None"
        restrictions_md = "\n".join([f"- {r}" for r in permission_check.get("restrictions", [])]) or "None"

        return f"""# Permission Check Report

**Status**: {status}

**Content ID**: {content_id}
**Intended Use**: {intended_use}
**User Type**: {user_type}
**License**: {license_info['license_type']}

## Conditions

{conditions_md}

## Restrictions

{restrictions_md}

---
Generated by Rights Management Agent
"""

    def _get_content_metadata(self, content_id: str) -> Dict[str, Any]:
        """Get content metadata"""
        return {
            "content_id": content_id,
            "title": "Content Title",
            "author": "Content Author",
            "year": "2025",
            "license": "CC-BY-4.0",
            "url": f"https://example.com/content/{content_id}"
        }

    def _create_attribution(
        self,
        metadata: Dict[str, Any],
        format_type: str
    ) -> str:
        """Create attribution text"""
        if format_type == "text":
            return (
                f"{metadata['title']} by {metadata['author']} ({metadata['year']}) "
                f"is licensed under {metadata['license']}. "
                f"Available at: {metadata['url']}"
            )
        elif format_type == "markdown":
            return (
                f"[{metadata['title']}]({metadata['url']}) by {metadata['author']} "
                f"({metadata['year']}) is licensed under [{metadata['license']}]"
                f"(https://creativecommons.org/licenses/)."
            )
        elif format_type == "html":
            return (
                f'<p><a href="{metadata["url"]}">{metadata["title"]}</a> '
                f'by {metadata["author"]} ({metadata["year"]}) is licensed under '
                f'<a href="https://creativecommons.org/licenses/">{metadata["license"]}</a>.</p>'
            )
        return ""

    def _perform_compliance_check(
        self,
        content_path: str,
        check_type: str
    ) -> Dict[str, Any]:
        """Perform compliance check"""
        # Mock compliance check
        issues = []
        if check_type == "attributions":
            issues.append("Missing attribution for third-party image")

        return {
            "check_type": check_type,
            "passed": len(issues) == 0,
            "issues": issues
        }

    def _calculate_compliance_score(
        self,
        compliance_results: Dict[str, Dict[str, Any]]
    ) -> int:
        """Calculate compliance score"""
        total_checks = len(compliance_results)
        passed_checks = sum(1 for result in compliance_results.values() if result["passed"])
        return int((passed_checks / total_checks * 100)) if total_checks > 0 else 100

    def _generate_compliance_report(
        self,
        content_path: str,
        compliance_results: Dict[str, Dict[str, Any]],
        compliance_score: int
    ) -> str:
        """Generate compliance report"""
        results_md = []
        for check_type, result in compliance_results.items():
            status = "✓ Passed" if result["passed"] else "✗ Failed"
            results_md.append(f"### {check_type.title()}: {status}\n")
            if result["issues"]:
                results_md.append("**Issues**:\n")
                for issue in result["issues"]:
                    results_md.append(f"- {issue}\n")

        return f"""# Copyright Compliance Audit

**Content Path**: {content_path}
**Compliance Score**: {compliance_score}/100

## Results

{''.join(results_md)}

---
Generated by Rights Management Agent
"""

    def _generate_remediation_plan(
        self,
        compliance_results: Dict[str, Dict[str, Any]]
    ) -> str:
        """Generate remediation plan"""
        remediation_md = []
        issue_num = 1
        for check_type, result in compliance_results.items():
            if result["issues"]:
                for issue in result["issues"]:
                    remediation_md.append(
                        f"{issue_num}. **{check_type.title()}**: {issue}\n"
                        f"   - **Action**: Review and add proper attribution\n"
                    )
                    issue_num += 1

        return f"""# Compliance Remediation Plan

{''.join(remediation_md)}

---
Generated by Rights Management Agent
"""

    def _check_usage_compliance(
        self,
        content_id: str,
        usage_event: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Check if usage complies with license"""
        # Mock compliance check
        return {
            "compliant": True,
            "reason": "Usage permitted under current license"
        }

    def _create_agreement(self, parameters: Dict[str, Any]) -> str:
        """Create licensing agreement"""
        timestamp = int(datetime.utcnow().timestamp())
        return f"AGR-{timestamp}"

    def _list_agreements(self) -> List[Dict[str, Any]]:
        """List agreements"""
        return [
            {"agreement_id": "AGR-001", "type": "content_license", "status": "active"},
            {"agreement_id": "AGR-002", "type": "content_license", "status": "active"}
        ]

    def _update_agreement(self, agreement_id: str, updates: Dict[str, Any]) -> None:
        """Update agreement"""
        pass

    def _expire_agreement(self, agreement_id: str) -> None:
        """Expire agreement"""
        pass

    def _generate_agreement_report(
        self,
        operation: str,
        output: Dict[str, Any]
    ) -> str:
        """Generate agreement report"""
        output_md = json.dumps(output, indent=2)

        return f"""# Agreement Management Report

**Operation**: {operation}

## Results

```json
{output_md}
```

---
Generated by Rights Management Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_rights_management():
    """Test the rights management agent"""
    from state_manager import StateManager

    project_id = "PROJ-TEST-RIGHTS-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test Rights Management Project",
        educational_level="9-12",
        standards=[],
        context={}
    )

    agent = RightsManagementAgent(project_id)

    print("=== Assign License ===")
    result = await agent.run({
        "action": "assign_license",
        "content_id": "CONTENT-001",
        "license_type": "CC-BY-4.0",
        "copyright_holder": "Educational Publisher"
    })
    print(f"Status: {result['status']}")
    print(f"License: {result['output']['license_type']}")

    print("\n=== Check Permissions ===")
    result = await agent.run({
        "action": "check_permissions",
        "content_id": "CONTENT-001",
        "intended_use": "commercial",
        "user_type": "commercial"
    })
    print(f"Status: {result['status']}")
    print(f"Permitted: {result['output']['permitted']}")

    print("\n=== Generate Attribution ===")
    result = await agent.run({
        "action": "generate_attribution",
        "content_id": "CONTENT-001",
        "format": "markdown"
    })
    print(f"Status: {result['status']}")
    print(f"Attribution: {result['output']['attribution_text'][:100]}...")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_rights_management())
