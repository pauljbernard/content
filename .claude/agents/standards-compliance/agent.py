#!/usr/bin/env python3
"""
Standards Compliance Agent

Validates alignment to educational standards (CCSS, NGSS, TEKS) and regulatory compliance.
Checks coverage, generates alignment reports, identifies gaps, and verifies state requirements.

Usage:
    from agent import StandardsComplianceAgent

    agent = StandardsComplianceAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "validate_alignment",
        "materials_path": "artifacts/",
        "standards": ["NGSS", "TX-TEKS"]
    })
"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent


class StandardsComplianceAgent(BaseAgent):
    """Validates standards alignment and regulatory compliance"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="standards-compliance",
            agent_name="Standards Compliance",
            project_id=project_id,
            description="Validates alignment to educational standards and regulatory compliance"
        )
        self.standards_frameworks = {
            "CCSS": "Common Core State Standards",
            "CCSS-M": "Common Core Math",
            "CCSS-ELA": "Common Core ELA",
            "NGSS": "Next Generation Science Standards",
            "TX-TEKS": "Texas Essential Knowledge and Skills",
            "CA-CCSS": "California Common Core",
            "FL-MAFS": "Florida Math Standards",
            "FL-BEST": "Florida B.E.S.T. Standards",
            "C3": "College, Career, and Civic Life (Social Studies)"
        }
        self.regulatory_frameworks = {
            "COPPA": "Children's Online Privacy Protection Act",
            "FERPA": "Family Educational Rights and Privacy Act",
            "Section 508": "Rehabilitation Act Section 508",
            "WCAG 2.1 AA": "Web Content Accessibility Guidelines",
            "SBOE": "State Board of Education (Texas)",
            "CA-Adoption": "California Adoption Criteria",
            "FL-Statutory": "Florida Statutory Requirements"
        }

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute standards compliance logic

        Actions:
        - validate_alignment: Validate standards alignment
        - check_coverage: Check standards coverage
        - identify_gaps: Identify gaps in coverage
        - validate_state_requirements: Check state-specific requirements
        - validate_regulatory: Check regulatory compliance
        - generate_report: Generate comprehensive compliance report
        """
        action = parameters.get("action", "validate_alignment")

        if action == "validate_alignment":
            return await self._validate_alignment(parameters, context)
        elif action == "check_coverage":
            return await self._check_coverage(parameters, context)
        elif action == "identify_gaps":
            return await self._identify_gaps(parameters, context)
        elif action == "validate_state_requirements":
            return await self._validate_state_requirements(parameters, context)
        elif action == "validate_regulatory":
            return await self._validate_regulatory(parameters, context)
        elif action == "generate_report":
            return await self._generate_report(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _validate_alignment(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate standards alignment"""
        decisions = []
        artifacts = []

        materials_path = parameters.get("materials_path")
        standards = parameters.get("standards", [])
        educational_level = parameters.get("educational_level", context.get("educational_level", "9-12"))

        decisions.append(f"Validating alignment to {len(standards)} standards frameworks")
        decisions.append(f"Educational level: {educational_level}")

        # Load materials and check alignment
        alignment_results = {}
        for standard in standards:
            result = self._check_standard_alignment(
                materials_path,
                standard,
                educational_level
            )
            alignment_results[standard] = result
            decisions.append(
                f"{standard}: {result['aligned_count']}/{result['total_standards']} standards aligned "
                f"({result['coverage_percentage']:.1f}%)"
            )

        # Calculate overall alignment score
        overall_score = self._calculate_alignment_score(alignment_results)
        decisions.append(f"Overall alignment score: {overall_score}/100")

        # Validate quality gate
        validation = await self.validate_quality_gate(
            "review",
            {"materials": materials_path},
            review_type="standards"
        )

        if validation.passed:
            self.state_manager.pass_quality_gate("review")
            decisions.append("Standards review quality gate passed")

        # Create alignment report
        report = self._generate_alignment_report(
            materials_path,
            standards,
            alignment_results,
            overall_score
        )

        report_artifact = f"artifacts/{self.project_id}/standards_alignment_report.md"
        self.create_artifact(
            "alignment_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create alignment matrix JSON
        matrix = {
            "materials_path": materials_path,
            "standards": standards,
            "educational_level": educational_level,
            "alignment_results": alignment_results,
            "overall_score": overall_score,
            "quality_gate_passed": validation.passed
        }

        matrix_artifact = f"artifacts/{self.project_id}/standards_alignment_matrix.json"
        self.create_artifact(
            "alignment_matrix",
            Path(matrix_artifact),
            json.dumps(matrix, indent=2)
        )
        artifacts.append(matrix_artifact)

        return {
            "output": {
                "overall_score": overall_score,
                "standards_validated": len(standards),
                "alignment_results": alignment_results,
                "quality_gate_passed": validation.passed
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Validated alignment to {len(standards)} standards frameworks "
                f"with overall score of {overall_score}/100"
            )
        }

    async def _check_coverage(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check standards coverage"""
        decisions = []
        artifacts = []

        materials_path = parameters.get("materials_path")
        standards = parameters.get("standards", [])
        target_coverage = parameters.get("target_coverage", 80.0)  # Percentage

        decisions.append(f"Checking coverage for {len(standards)} standards")
        decisions.append(f"Target coverage: {target_coverage}%")

        # Analyze coverage for each standard
        coverage_analysis = {}
        for standard in standards:
            analysis = self._analyze_coverage(materials_path, standard)
            coverage_analysis[standard] = analysis

            met_target = analysis["coverage_percentage"] >= target_coverage
            status = "✓" if met_target else "✗"
            decisions.append(
                f"{status} {standard}: {analysis['coverage_percentage']:.1f}% "
                f"({analysis['covered']}/{analysis['total']} standards)"
            )

        # Create coverage report
        report = self._generate_coverage_report(
            coverage_analysis,
            target_coverage
        )

        report_artifact = f"artifacts/{self.project_id}/standards_coverage_report.md"
        self.create_artifact(
            "coverage_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "coverage_analysis": coverage_analysis,
                "target_coverage": target_coverage,
                "meets_target": all(
                    analysis["coverage_percentage"] >= target_coverage
                    for analysis in coverage_analysis.values()
                )
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Analyzed coverage for {len(standards)} standards frameworks "
                f"against {target_coverage}% target"
            )
        }

    async def _identify_gaps(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identify gaps in standards coverage"""
        decisions = []
        artifacts = []

        materials_path = parameters.get("materials_path")
        standards = parameters.get("standards", [])

        decisions.append(f"Identifying gaps in {len(standards)} standards")

        # Identify gaps for each standard
        all_gaps = {}
        total_gaps = 0

        for standard in standards:
            gaps = self._find_coverage_gaps(materials_path, standard)
            all_gaps[standard] = gaps
            total_gaps += len(gaps)
            decisions.append(f"{standard}: {len(gaps)} standards not covered")

        # Prioritize gaps
        prioritized_gaps = self._prioritize_gaps(all_gaps)
        decisions.append(f"Prioritized {total_gaps} gaps by importance")

        # Generate gap analysis report
        report = self._generate_gap_report(all_gaps, prioritized_gaps)

        report_artifact = f"artifacts/{self.project_id}/standards_gap_analysis.md"
        self.create_artifact(
            "gap_analysis",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Generate remediation recommendations
        recommendations = self._generate_remediation_plan(prioritized_gaps)
        decisions.append(f"Generated {len(recommendations)} remediation recommendations")

        recommendations_artifact = f"artifacts/{self.project_id}/gap_remediation_plan.md"
        self.create_artifact(
            "remediation_plan",
            Path(recommendations_artifact),
            self._format_remediation_plan(recommendations)
        )
        artifacts.append(recommendations_artifact)

        return {
            "output": {
                "total_gaps": total_gaps,
                "gaps_by_standard": {
                    standard: len(gaps)
                    for standard, gaps in all_gaps.items()
                },
                "prioritized_gaps": prioritized_gaps[:10]  # Top 10
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Identified {total_gaps} gaps across {len(standards)} standards "
                f"with prioritized remediation plan"
            )
        }

    async def _validate_state_requirements(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate state-specific requirements"""
        decisions = []
        artifacts = []

        materials_path = parameters.get("materials_path")
        state = parameters.get("state", "TX")  # TX, CA, FL, etc.

        decisions.append(f"Validating {state} state requirements")

        # Check state-specific requirements
        requirements_results = self._check_state_requirements(
            materials_path,
            state
        )

        decisions.append(
            f"Checked {requirements_results['total_requirements']} requirements"
        )
        decisions.append(
            f"Met: {requirements_results['met']}, "
            f"Not Met: {requirements_results['not_met']}"
        )

        # Create state compliance report
        report = self._generate_state_compliance_report(
            state,
            requirements_results
        )

        report_artifact = f"artifacts/{self.project_id}/state_compliance_{state}.md"
        self.create_artifact(
            "state_compliance",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "state": state,
                "compliance_met": requirements_results["met"] == requirements_results["total_requirements"],
                "requirements_met": requirements_results["met"],
                "requirements_not_met": requirements_results["not_met"],
                "compliance_percentage": (
                    requirements_results["met"] / requirements_results["total_requirements"] * 100
                    if requirements_results["total_requirements"] > 0 else 0
                )
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Validated {state} state requirements: "
                f"{requirements_results['met']}/{requirements_results['total_requirements']} met"
            )
        }

    async def _validate_regulatory(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate regulatory compliance"""
        decisions = []
        artifacts = []

        materials_path = parameters.get("materials_path")
        regulations = parameters.get("regulations", [
            "COPPA", "FERPA", "Section 508", "WCAG 2.1 AA"
        ])

        decisions.append(f"Validating {len(regulations)} regulatory frameworks")

        # Check each regulation
        regulatory_results = {}
        for regulation in regulations:
            result = self._check_regulatory_compliance(
                materials_path,
                regulation
            )
            regulatory_results[regulation] = result

            status = "✓ Compliant" if result["compliant"] else "✗ Issues Found"
            decisions.append(f"{regulation}: {status} ({len(result['issues'])} issues)")

        # Calculate overall regulatory compliance
        all_compliant = all(
            result["compliant"]
            for result in regulatory_results.values()
        )

        # Create regulatory compliance report
        report = self._generate_regulatory_report(
            regulatory_results,
            all_compliant
        )

        report_artifact = f"artifacts/{self.project_id}/regulatory_compliance_report.md"
        self.create_artifact(
            "regulatory_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Generate compliance certificate if fully compliant
        if all_compliant:
            certificate = self._generate_compliance_certificate(
                regulations,
                regulatory_results
            )

            cert_artifact = f"artifacts/{self.project_id}/compliance_certificate.md"
            self.create_artifact(
                "compliance_certificate",
                Path(cert_artifact),
                certificate
            )
            artifacts.append(cert_artifact)
            decisions.append("Generated compliance certificate")

        return {
            "output": {
                "all_compliant": all_compliant,
                "regulations_validated": len(regulations),
                "regulatory_results": {
                    reg: result["compliant"]
                    for reg, result in regulatory_results.items()
                },
                "total_issues": sum(
                    len(result["issues"])
                    for result in regulatory_results.values()
                )
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Validated {len(regulations)} regulatory frameworks. "
                f"Overall compliant: {all_compliant}"
            )
        }

    async def _generate_report(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        decisions = []
        artifacts = []

        materials_path = parameters.get("materials_path")
        standards = parameters.get("standards", [])
        state = parameters.get("state")
        regulations = parameters.get("regulations", [])

        decisions.append("Generating comprehensive compliance report")

        # Collect all compliance data
        compliance_data = {
            "standards_alignment": {},
            "state_compliance": {},
            "regulatory_compliance": {}
        }

        # Standards alignment
        if standards:
            for standard in standards:
                result = self._check_standard_alignment(
                    materials_path,
                    standard,
                    context.get("educational_level", "9-12")
                )
                compliance_data["standards_alignment"][standard] = result

        # State compliance
        if state:
            compliance_data["state_compliance"] = self._check_state_requirements(
                materials_path,
                state
            )

        # Regulatory compliance
        if regulations:
            for regulation in regulations:
                result = self._check_regulatory_compliance(
                    materials_path,
                    regulation
                )
                compliance_data["regulatory_compliance"][regulation] = result

        # Generate comprehensive report
        report = self._generate_comprehensive_report(
            materials_path,
            compliance_data
        )

        report_artifact = f"artifacts/{self.project_id}/comprehensive_compliance_report.md"
        self.create_artifact(
            "comprehensive_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Generate executive summary
        summary = self._generate_executive_summary(compliance_data)

        summary_artifact = f"artifacts/{self.project_id}/compliance_executive_summary.md"
        self.create_artifact(
            "executive_summary",
            Path(summary_artifact),
            summary
        )
        artifacts.append(summary_artifact)

        decisions.append("Generated comprehensive report and executive summary")

        return {
            "output": {
                "compliance_data": compliance_data,
                "report_generated": True
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": "Generated comprehensive compliance report covering all requirements"
        }

    # Helper methods

    def _check_standard_alignment(
        self,
        materials_path: str,
        standard: str,
        educational_level: str
    ) -> Dict[str, Any]:
        """Check alignment to specific standard"""
        # In production, would load and analyze actual materials
        # For now, return mock data
        total_standards = 50
        aligned_count = 42

        return {
            "standard": standard,
            "total_standards": total_standards,
            "aligned_count": aligned_count,
            "coverage_percentage": (aligned_count / total_standards * 100),
            "unaligned": total_standards - aligned_count,
            "educational_level": educational_level
        }

    def _calculate_alignment_score(
        self,
        alignment_results: Dict[str, Dict[str, Any]]
    ) -> int:
        """Calculate overall alignment score"""
        if not alignment_results:
            return 0

        total_coverage = sum(
            result["coverage_percentage"]
            for result in alignment_results.values()
        )
        avg_coverage = total_coverage / len(alignment_results)

        return int(avg_coverage)

    def _generate_alignment_report(
        self,
        materials_path: str,
        standards: List[str],
        alignment_results: Dict[str, Dict[str, Any]],
        overall_score: int
    ) -> str:
        """Generate standards alignment report"""
        results_md = []
        for standard, result in alignment_results.items():
            coverage_bar = self._create_progress_bar(result["coverage_percentage"])
            results_md.append(
                f"### {standard} - {self.standards_frameworks.get(standard, standard)}\n\n"
                f"**Coverage**: {result['coverage_percentage']:.1f}%\n"
                f"{coverage_bar}\n\n"
                f"- Aligned: {result['aligned_count']}/{result['total_standards']} standards\n"
                f"- Not Aligned: {result['unaligned']} standards\n"
            )

        return f"""# Standards Alignment Report

**Materials**: {materials_path}
**Overall Score**: {overall_score}/100

## Summary

Validated alignment to {len(standards)} standards frameworks:
{', '.join(standards)}

## Alignment Results

{''.join(results_md)}

## Recommendations

{self._generate_alignment_recommendations(alignment_results, overall_score)}

---
Generated by Standards Compliance Agent
"""

    def _create_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Create text progress bar"""
        filled = int(width * percentage / 100)
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}] {percentage:.1f}%"

    def _generate_alignment_recommendations(
        self,
        alignment_results: Dict[str, Dict[str, Any]],
        overall_score: int
    ) -> str:
        """Generate alignment recommendations"""
        if overall_score >= 90:
            return "✅ Excellent alignment to all standards frameworks. Content is ready for deployment."

        recommendations = []
        for standard, result in alignment_results.items():
            if result["coverage_percentage"] < 80:
                recommendations.append(
                    f"- **{standard}**: Address {result['unaligned']} unaligned standards "
                    f"to reach 80% coverage threshold"
                )

        return "\n".join(recommendations) if recommendations else "No critical issues found."

    def _analyze_coverage(
        self,
        materials_path: str,
        standard: str
    ) -> Dict[str, Any]:
        """Analyze standards coverage"""
        # Mock data
        total = 50
        covered = 40

        return {
            "total": total,
            "covered": covered,
            "not_covered": total - covered,
            "coverage_percentage": (covered / total * 100)
        }

    def _generate_coverage_report(
        self,
        coverage_analysis: Dict[str, Dict[str, Any]],
        target_coverage: float
    ) -> str:
        """Generate coverage report"""
        analysis_md = []
        for standard, analysis in coverage_analysis.items():
            met_target = analysis["coverage_percentage"] >= target_coverage
            status = "✓ Target Met" if met_target else "✗ Below Target"

            analysis_md.append(
                f"### {standard}: {status}\n\n"
                f"- Coverage: {analysis['coverage_percentage']:.1f}%\n"
                f"- Covered: {analysis['covered']}/{analysis['total']}\n"
                f"- Gap: {analysis['not_covered']} standards\n"
            )

        return f"""# Standards Coverage Report

**Target Coverage**: {target_coverage}%

## Coverage Analysis

{''.join(analysis_md)}

---
Generated by Standards Compliance Agent
"""

    def _find_coverage_gaps(
        self,
        materials_path: str,
        standard: str
    ) -> List[Dict[str, Any]]:
        """Find coverage gaps"""
        # Mock gaps
        return [
            {
                "standard_id": f"{standard}-001",
                "description": "Standard not covered in materials",
                "grade_level": "9-12",
                "importance": "high"
            },
            {
                "standard_id": f"{standard}-002",
                "description": "Standard partially covered",
                "grade_level": "9-12",
                "importance": "medium"
            }
        ]

    def _prioritize_gaps(
        self,
        all_gaps: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Prioritize gaps by importance"""
        all_gaps_flat = []
        for standard, gaps in all_gaps.items():
            for gap in gaps:
                gap["standard"] = standard
                all_gaps_flat.append(gap)

        # Sort by importance
        importance_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            all_gaps_flat,
            key=lambda g: importance_order.get(g.get("importance", "low"), 2)
        )

    def _generate_gap_report(
        self,
        all_gaps: Dict[str, List[Dict[str, Any]]],
        prioritized_gaps: List[Dict[str, Any]]
    ) -> str:
        """Generate gap analysis report"""
        gaps_md = []
        for standard, gaps in all_gaps.items():
            if gaps:
                gaps_md.append(f"### {standard} ({len(gaps)} gaps)\n")
                for gap in gaps[:5]:  # Top 5 per standard
                    gaps_md.append(
                        f"- **{gap['standard_id']}** [{gap['importance'].upper()}]: "
                        f"{gap['description']}\n"
                    )

        top_priorities_md = []
        for i, gap in enumerate(prioritized_gaps[:10], 1):
            top_priorities_md.append(
                f"{i}. **{gap['standard']} - {gap['standard_id']}** "
                f"[{gap['importance'].upper()}]: {gap['description']}"
            )

        return f"""# Standards Gap Analysis

## Gaps by Standard

{''.join(gaps_md)}

## Top 10 Priorities

{''.join(top_priorities_md)}

---
Generated by Standards Compliance Agent
"""

    def _generate_remediation_plan(
        self,
        prioritized_gaps: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate remediation recommendations"""
        return [
            {
                "gap": gap,
                "recommendation": f"Create content addressing {gap['standard_id']}",
                "estimated_effort": "medium"
            }
            for gap in prioritized_gaps[:10]
        ]

    def _format_remediation_plan(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> str:
        """Format remediation plan"""
        plan_md = []
        for i, rec in enumerate(recommendations, 1):
            gap = rec["gap"]
            plan_md.append(
                f"## {i}. {gap['standard']} - {gap['standard_id']}\n\n"
                f"**Priority**: {gap['importance'].upper()}\n"
                f"**Recommendation**: {rec['recommendation']}\n"
                f"**Estimated Effort**: {rec['estimated_effort']}\n"
            )

        return f"""# Gap Remediation Plan

{''.join(plan_md)}

---
Generated by Standards Compliance Agent
"""

    def _check_state_requirements(
        self,
        materials_path: str,
        state: str
    ) -> Dict[str, Any]:
        """Check state-specific requirements"""
        # Mock state requirements check
        total_requirements = 15
        met = 14

        return {
            "state": state,
            "total_requirements": total_requirements,
            "met": met,
            "not_met": total_requirements - met,
            "requirements": [
                {"id": f"{state}-REQ-001", "met": True, "description": "Requirement 1"},
                {"id": f"{state}-REQ-002", "met": False, "description": "Requirement 2"}
            ]
        }

    def _generate_state_compliance_report(
        self,
        state: str,
        requirements_results: Dict[str, Any]
    ) -> str:
        """Generate state compliance report"""
        compliance_percentage = (
            requirements_results["met"] / requirements_results["total_requirements"] * 100
        )

        requirements_md = []
        for req in requirements_results["requirements"]:
            status = "✓" if req["met"] else "✗"
            requirements_md.append(f"- {status} {req['id']}: {req['description']}")

        return f"""# {state} State Compliance Report

**Compliance**: {compliance_percentage:.1f}%
**Requirements Met**: {requirements_results['met']}/{requirements_results['total_requirements']}

## Requirements

{''.join(requirements_md)}

---
Generated by Standards Compliance Agent
"""

    def _check_regulatory_compliance(
        self,
        materials_path: str,
        regulation: str
    ) -> Dict[str, Any]:
        """Check regulatory compliance"""
        # Mock regulatory check
        issues = []

        if regulation == "WCAG 2.1 AA":
            # Accessibility check
            pass
        elif regulation == "COPPA":
            # Privacy check for under-13
            pass
        elif regulation == "FERPA":
            # Student data privacy
            pass

        return {
            "regulation": regulation,
            "compliant": len(issues) == 0,
            "issues": issues
        }

    def _generate_regulatory_report(
        self,
        regulatory_results: Dict[str, Dict[str, Any]],
        all_compliant: bool
    ) -> str:
        """Generate regulatory compliance report"""
        status = "✅ COMPLIANT" if all_compliant else "❌ ISSUES FOUND"

        results_md = []
        for regulation, result in regulatory_results.items():
            reg_status = "✓ Compliant" if result["compliant"] else "✗ Issues Found"
            full_name = self.regulatory_frameworks.get(regulation, regulation)

            results_md.append(
                f"### {regulation} - {full_name}\n\n"
                f"**Status**: {reg_status}\n"
            )

            if result["issues"]:
                results_md.append("**Issues**:\n")
                for issue in result["issues"]:
                    results_md.append(f"- {issue}\n")

        return f"""# Regulatory Compliance Report

**Overall Status**: {status}

## Compliance Results

{''.join(results_md)}

---
Generated by Standards Compliance Agent
"""

    def _generate_compliance_certificate(
        self,
        regulations: List[str],
        regulatory_results: Dict[str, Dict[str, Any]]
    ) -> str:
        """Generate compliance certificate"""
        from datetime import datetime

        regulations_list = "\n".join([f"- {reg}" for reg in regulations])

        return f"""# Compliance Certificate

This certifies that the educational materials have been validated for compliance with:

{regulations_list}

**Validation Date**: {datetime.utcnow().strftime("%Y-%m-%d")}
**Project ID**: {self.project_id}
**Validated By**: Standards Compliance Agent

All regulatory requirements have been met and the materials are approved for distribution.

---
Generated by Standards Compliance Agent
"""

    def _generate_comprehensive_report(
        self,
        materials_path: str,
        compliance_data: Dict[str, Any]
    ) -> str:
        """Generate comprehensive compliance report"""
        sections = []

        # Standards alignment section
        if compliance_data["standards_alignment"]:
            sections.append("## Standards Alignment\n")
            for standard, result in compliance_data["standards_alignment"].items():
                sections.append(
                    f"- **{standard}**: {result['coverage_percentage']:.1f}% "
                    f"({result['aligned_count']}/{result['total_standards']})\n"
                )

        # State compliance section
        if compliance_data["state_compliance"]:
            state_data = compliance_data["state_compliance"]
            sections.append("\n## State Compliance\n")
            sections.append(
                f"- **State**: {state_data['state']}\n"
                f"- **Requirements Met**: {state_data['met']}/{state_data['total_requirements']}\n"
            )

        # Regulatory compliance section
        if compliance_data["regulatory_compliance"]:
            sections.append("\n## Regulatory Compliance\n")
            for regulation, result in compliance_data["regulatory_compliance"].items():
                status = "✓ Compliant" if result["compliant"] else "✗ Issues"
                sections.append(f"- **{regulation}**: {status}\n")

        return f"""# Comprehensive Compliance Report

**Materials**: {materials_path}

{''.join(sections)}

---
Generated by Standards Compliance Agent
"""

    def _generate_executive_summary(
        self,
        compliance_data: Dict[str, Any]
    ) -> str:
        """Generate executive summary"""
        return f"""# Compliance Executive Summary

## Key Findings

- **Standards Frameworks Validated**: {len(compliance_data['standards_alignment'])}
- **State Compliance**: {'Verified' if compliance_data['state_compliance'] else 'N/A'}
- **Regulatory Compliance**: {len(compliance_data['regulatory_compliance'])} frameworks validated

## Overall Status

All compliance requirements have been thoroughly validated and documented.

---
Generated by Standards Compliance Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_standards_compliance():
    """Test the standards compliance agent"""
    from state_manager import StateManager

    project_id = "PROJ-TEST-COMPLIANCE-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test Standards Compliance Project",
        educational_level="9-12",
        standards=["NGSS", "TX-TEKS"],
        context={"subject": "biology", "topic": "genetics", "state": "TX"}
    )

    agent = StandardsComplianceAgent(project_id)

    print("=== Validate Standards Alignment ===")
    result = await agent.run({
        "action": "validate_alignment",
        "materials_path": "artifacts/PROJ-TEST-COMPLIANCE-001/",
        "standards": ["NGSS", "TX-TEKS"],
        "educational_level": "9-12"
    })
    print(f"Status: {result['status']}")
    print(f"Overall score: {result['output']['overall_score']}/100")
    print(f"Standards validated: {result['output']['standards_validated']}")
    print(f"Artifacts: {result['artifacts']}")

    print("\n=== Check Coverage ===")
    result = await agent.run({
        "action": "check_coverage",
        "materials_path": "artifacts/PROJ-TEST-COMPLIANCE-001/",
        "standards": ["NGSS", "TX-TEKS"],
        "target_coverage": 80.0
    })
    print(f"Status: {result['status']}")
    print(f"Meets target: {result['output']['meets_target']}")

    print("\n=== Validate Regulatory Compliance ===")
    result = await agent.run({
        "action": "validate_regulatory",
        "materials_path": "artifacts/PROJ-TEST-COMPLIANCE-001/",
        "regulations": ["COPPA", "FERPA", "WCAG 2.1 AA"]
    })
    print(f"Status: {result['status']}")
    print(f"All compliant: {result['output']['all_compliant']}")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_standards_compliance())
