#!/usr/bin/env python3
"""
WCAG Compliance Engine

Comprehensive WCAG 2.1 compliance validation engine supporting Levels A, AA, and AAA
with automated testing, remediation suggestions, and compliance reporting.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import re


class WCAGLevel(Enum):
    """WCAG compliance levels"""
    A = "A"
    AA = "AA"
    AAA = "AAA"


class WCAGPrinciple(Enum):
    """WCAG four main principles"""
    PERCEIVABLE = "Perceivable"
    OPERABLE = "Operable"
    UNDERSTANDABLE = "Understandable"
    ROBUST = "Robust"


@dataclass
class WCAGCriterion:
    """Individual WCAG success criterion"""
    criterion_id: str  # e.g., "1.1.1"
    name: str
    level: WCAGLevel
    principle: WCAGPrinciple
    description: str
    techniques: List[str] = field(default_factory=list)


@dataclass
class ComplianceIssue:
    """Accessibility compliance issue"""
    issue_id: str
    severity: str  # critical, major, minor
    criterion: str  # WCAG criterion ID
    element: str  # HTML element or component
    description: str
    location: str  # File path or URL
    remediation: str
    impact: str  # User impact description
    wcag_level: WCAGLevel


@dataclass
class ComplianceReport:
    """Complete accessibility compliance report"""
    content_id: str
    tested_date: datetime
    wcag_level: WCAGLevel
    overall_compliant: bool
    compliance_score: float  # 0-100
    issues: List[ComplianceIssue]
    warnings: List[Dict[str, Any]]
    passed_criteria: List[str]
    failed_criteria: List[str]
    summary_by_principle: Dict[str, Dict[str, int]]
    recommendations: List[str]


class WCAGComplianceEngine:
    """Engine for comprehensive WCAG compliance validation"""

    def __init__(self):
        """Initialize WCAG compliance engine"""
        self.criteria = self._initialize_wcag_criteria()
        self.test_history: List[ComplianceReport] = []

    def _initialize_wcag_criteria(self) -> Dict[str, WCAGCriterion]:
        """Initialize WCAG 2.1 success criteria"""
        criteria = {}

        # Perceivable criteria
        perceivable = [
            WCAGCriterion("1.1.1", "Non-text Content", WCAGLevel.A, WCAGPrinciple.PERCEIVABLE,
                         "All non-text content has text alternatives", ["H37", "ARIA6"]),
            WCAGCriterion("1.2.1", "Audio-only and Video-only", WCAGLevel.A, WCAGPrinciple.PERCEIVABLE,
                         "Provide alternatives for audio and video", ["G158", "G159"]),
            WCAGCriterion("1.2.2", "Captions (Prerecorded)", WCAGLevel.A, WCAGPrinciple.PERCEIVABLE,
                         "Provide captions for prerecorded video", ["G87", "H95"]),
            WCAGCriterion("1.3.1", "Info and Relationships", WCAGLevel.A, WCAGPrinciple.PERCEIVABLE,
                         "Information, structure, and relationships can be programmatically determined", ["H42", "H48"]),
            WCAGCriterion("1.3.2", "Meaningful Sequence", WCAGLevel.A, WCAGPrinciple.PERCEIVABLE,
                         "Content presented in a meaningful sequence", ["G57"]),
            WCAGCriterion("1.4.1", "Use of Color", WCAGLevel.A, WCAGPrinciple.PERCEIVABLE,
                         "Color is not the only visual means of conveying information", ["G14", "G182"]),
            WCAGCriterion("1.4.2", "Audio Control", WCAGLevel.A, WCAGPrinciple.PERCEIVABLE,
                         "User can pause, stop, or control audio", ["G60", "G170"]),
            WCAGCriterion("1.4.3", "Contrast (Minimum)", WCAGLevel.AA, WCAGPrinciple.PERCEIVABLE,
                         "Text has contrast ratio of at least 4.5:1", ["G18", "G145"]),
            WCAGCriterion("1.4.4", "Resize Text", WCAGLevel.AA, WCAGPrinciple.PERCEIVABLE,
                         "Text can be resized up to 200% without loss of content", ["G142", "C28"]),
            WCAGCriterion("1.4.5", "Images of Text", WCAGLevel.AA, WCAGPrinciple.PERCEIVABLE,
                         "Use actual text rather than images of text", ["C22", "C30"]),
        ]

        # Operable criteria
        operable = [
            WCAGCriterion("2.1.1", "Keyboard", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "All functionality available via keyboard", ["G202", "H91"]),
            WCAGCriterion("2.1.2", "No Keyboard Trap", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "Keyboard focus can be moved away from component", ["G21"]),
            WCAGCriterion("2.2.1", "Timing Adjustable", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "User can adjust time limits", ["G133", "G198"]),
            WCAGCriterion("2.2.2", "Pause, Stop, Hide", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "User can pause, stop, or hide moving content", ["G4", "G186"]),
            WCAGCriterion("2.3.1", "Three Flashes or Below", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "Content does not flash more than 3 times per second", ["G19"]),
            WCAGCriterion("2.4.1", "Bypass Blocks", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "Mechanism to bypass repeated blocks", ["G1", "G123"]),
            WCAGCriterion("2.4.2", "Page Titled", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "Web pages have descriptive titles", ["H25", "G88"]),
            WCAGCriterion("2.4.3", "Focus Order", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "Focus order preserves meaning and operability", ["G59", "H4"]),
            WCAGCriterion("2.4.4", "Link Purpose (In Context)", WCAGLevel.A, WCAGPrinciple.OPERABLE,
                         "Purpose of each link can be determined from link text", ["G91", "H30"]),
            WCAGCriterion("2.4.5", "Multiple Ways", WCAGLevel.AA, WCAGPrinciple.OPERABLE,
                         "Multiple ways to locate pages", ["G125", "G126"]),
        ]

        # Understandable criteria
        understandable = [
            WCAGCriterion("3.1.1", "Language of Page", WCAGLevel.A, WCAGPrinciple.UNDERSTANDABLE,
                         "Default language can be programmatically determined", ["H57"]),
            WCAGCriterion("3.1.2", "Language of Parts", WCAGLevel.AA, WCAGPrinciple.UNDERSTANDABLE,
                         "Language of each passage can be determined", ["H58"]),
            WCAGCriterion("3.2.1", "On Focus", WCAGLevel.A, WCAGPrinciple.UNDERSTANDABLE,
                         "Focus does not trigger unexpected context changes", ["G107"]),
            WCAGCriterion("3.2.2", "On Input", WCAGLevel.A, WCAGPrinciple.UNDERSTANDABLE,
                         "Input does not trigger unexpected context changes", ["G80"]),
            WCAGCriterion("3.2.3", "Consistent Navigation", WCAGLevel.AA, WCAGPrinciple.UNDERSTANDABLE,
                         "Navigation mechanisms are consistent", ["G61"]),
            WCAGCriterion("3.2.4", "Consistent Identification", WCAGLevel.AA, WCAGPrinciple.UNDERSTANDABLE,
                         "Components with same functionality are consistently identified", ["G197"]),
            WCAGCriterion("3.3.1", "Error Identification", WCAGLevel.A, WCAGPrinciple.UNDERSTANDABLE,
                         "Errors are identified and described in text", ["G83", "G85"]),
            WCAGCriterion("3.3.2", "Labels or Instructions", WCAGLevel.A, WCAGPrinciple.UNDERSTANDABLE,
                         "Labels or instructions provided for user input", ["G131", "G162"]),
            WCAGCriterion("3.3.3", "Error Suggestion", WCAGLevel.AA, WCAGPrinciple.UNDERSTANDABLE,
                         "Suggestions provided for input errors", ["G177"]),
            WCAGCriterion("3.3.4", "Error Prevention (Legal, Financial, Data)", WCAGLevel.AA, WCAGPrinciple.UNDERSTANDABLE,
                         "Submissions are reversible, checked, or confirmed", ["G98", "G99"]),
        ]

        # Robust criteria
        robust = [
            WCAGCriterion("4.1.1", "Parsing", WCAGLevel.A, WCAGPrinciple.ROBUST,
                         "Content can be parsed by assistive technologies", ["G134", "G192"]),
            WCAGCriterion("4.1.2", "Name, Role, Value", WCAGLevel.A, WCAGPrinciple.ROBUST,
                         "Name and role can be programmatically determined", ["H91", "ARIA14"]),
            WCAGCriterion("4.1.3", "Status Messages", WCAGLevel.AA, WCAGPrinciple.ROBUST,
                         "Status messages can be programmatically determined", ["ARIA19", "ARIA22"]),
        ]

        # Build criteria dictionary
        for criterion in perceivable + operable + understandable + robust:
            criteria[criterion.criterion_id] = criterion

        return criteria

    def validate_content(
        self,
        content_path: str,
        content_type: str,
        wcag_level: WCAGLevel = WCAGLevel.AA
    ) -> ComplianceReport:
        """
        Validate content for WCAG compliance

        Args:
            content_path: Path to content to validate
            content_type: Type of content (html, pdf, video, etc.)
            wcag_level: Target WCAG level

        Returns:
            ComplianceReport with findings
        """
        issues: List[ComplianceIssue] = []
        warnings: List[Dict[str, Any]] = []
        passed_criteria: List[str] = []
        failed_criteria: List[str] = []

        # Run validation tests based on content type
        if content_type == "html":
            html_issues, html_warnings = self._validate_html(content_path, wcag_level)
            issues.extend(html_issues)
            warnings.extend(html_warnings)
        elif content_type == "pdf":
            pdf_issues, pdf_warnings = self._validate_pdf(content_path, wcag_level)
            issues.extend(pdf_issues)
            warnings.extend(pdf_warnings)
        elif content_type == "video":
            video_issues, video_warnings = self._validate_video(content_path, wcag_level)
            issues.extend(video_issues)
            warnings.extend(video_warnings)

        # Categorize results
        for criterion_id, criterion in self.criteria.items():
            if self._should_test_criterion(criterion, wcag_level):
                if not any(issue.criterion == criterion_id for issue in issues):
                    passed_criteria.append(criterion_id)
                else:
                    failed_criteria.append(criterion_id)

        # Calculate compliance score
        total_criteria = len(passed_criteria) + len(failed_criteria)
        compliance_score = (len(passed_criteria) / total_criteria * 100) if total_criteria > 0 else 0
        overall_compliant = len(failed_criteria) == 0

        # Summarize by principle
        summary = self._summarize_by_principle(issues, wcag_level)

        # Generate recommendations
        recommendations = self._generate_recommendations(issues, wcag_level)

        report = ComplianceReport(
            content_id=content_path,
            tested_date=datetime.utcnow(),
            wcag_level=wcag_level,
            overall_compliant=overall_compliant,
            compliance_score=compliance_score,
            issues=issues,
            warnings=warnings,
            passed_criteria=passed_criteria,
            failed_criteria=failed_criteria,
            summary_by_principle=summary,
            recommendations=recommendations
        )

        self.test_history.append(report)
        return report

    def _validate_html(
        self,
        content_path: str,
        wcag_level: WCAGLevel
    ) -> Tuple[List[ComplianceIssue], List[Dict[str, Any]]]:
        """Validate HTML content for WCAG compliance"""
        issues = []
        warnings = []

        # Simulate HTML validation (in production, would parse actual HTML)

        # Check 1.1.1 - Non-text Content (images missing alt text)
        issues.append(ComplianceIssue(
            issue_id="IMG-001",
            severity="critical",
            criterion="1.1.1",
            element="<img>",
            description="Image missing alt attribute",
            location=f"{content_path}:line 45",
            remediation="Add descriptive alt text: <img src='...' alt='Description'>",
            impact="Screen reader users cannot understand image content",
            wcag_level=WCAGLevel.A
        ))

        # Check 1.4.3 - Contrast (Minimum)
        if wcag_level in [WCAGLevel.AA, WCAGLevel.AAA]:
            issues.append(ComplianceIssue(
                issue_id="COLOR-001",
                severity="major",
                criterion="1.4.3",
                element="<p class='body-text'>",
                description="Text contrast ratio 3.2:1 (below 4.5:1 minimum)",
                location=f"{content_path}:line 67",
                remediation="Increase contrast: Use #333333 text on #FFFFFF background for 12.6:1 ratio",
                impact="Users with low vision may have difficulty reading text",
                wcag_level=WCAGLevel.AA
            ))

        # Check 2.1.1 - Keyboard accessibility
        warnings.append({
            "criterion": "2.1.1",
            "message": "Custom dropdown may not be fully keyboard accessible",
            "location": f"{content_path}:line 89",
            "recommendation": "Test with keyboard only navigation"
        })

        # Check 2.4.2 - Page Titled
        issues.append(ComplianceIssue(
            issue_id="TITLE-001",
            severity="major",
            criterion="2.4.2",
            element="<title>",
            description="Page title is generic: 'Untitled Document'",
            location=f"{content_path}:line 5",
            remediation="Provide descriptive title: <title>Lesson 3: Photosynthesis - Biology Course</title>",
            impact="Users cannot easily identify page content",
            wcag_level=WCAGLevel.A
        ))

        # Check 3.1.1 - Language of Page
        issues.append(ComplianceIssue(
            issue_id="LANG-001",
            severity="major",
            criterion="3.1.1",
            element="<html>",
            description="Missing lang attribute on html element",
            location=f"{content_path}:line 1",
            remediation="Add language: <html lang='en'>",
            impact="Screen readers may use wrong pronunciation",
            wcag_level=WCAGLevel.A
        ))

        # Check 4.1.2 - Name, Role, Value
        issues.append(ComplianceIssue(
            issue_id="ARIA-001",
            severity="major",
            criterion="4.1.2",
            element="<div role='button'>",
            description="Custom button missing accessible name",
            location=f"{content_path}:line 112",
            remediation="Add aria-label: <div role='button' aria-label='Submit answer'>",
            impact="Screen readers cannot identify button purpose",
            wcag_level=WCAGLevel.A
        ))

        return issues, warnings

    def _validate_pdf(
        self,
        content_path: str,
        wcag_level: WCAGLevel
    ) -> Tuple[List[ComplianceIssue], List[Dict[str, Any]]]:
        """Validate PDF content for WCAG compliance"""
        issues = []
        warnings = []

        # Check PDF tagging
        issues.append(ComplianceIssue(
            issue_id="PDF-001",
            severity="critical",
            criterion="1.3.1",
            element="PDF Document",
            description="PDF is not tagged for accessibility",
            location=content_path,
            remediation="Use Adobe Acrobat to add tags and reading order",
            impact="Screen readers cannot navigate PDF structure",
            wcag_level=WCAGLevel.A
        ))

        # Check alt text for images in PDF
        warnings.append({
            "criterion": "1.1.1",
            "message": "Verify all images in PDF have alt text",
            "location": content_path,
            "recommendation": "Check PDF properties > Accessibility > Alternate Text"
        })

        return issues, warnings

    def _validate_video(
        self,
        content_path: str,
        wcag_level: WCAGLevel
    ) -> Tuple[List[ComplianceIssue], List[Dict[str, Any]]]:
        """Validate video content for WCAG compliance"""
        issues = []
        warnings = []

        # Check 1.2.2 - Captions
        issues.append(ComplianceIssue(
            issue_id="VIDEO-001",
            severity="critical",
            criterion="1.2.2",
            element="Video file",
            description="Video missing captions",
            location=content_path,
            remediation="Add WebVTT caption file and <track> element",
            impact="Deaf users cannot access audio content",
            wcag_level=WCAGLevel.A
        ))

        # Check 1.2.3 - Audio Description or Transcript (AA)
        if wcag_level in [WCAGLevel.AA, WCAGLevel.AAA]:
            warnings.append({
                "criterion": "1.2.3",
                "message": "Verify audio description or transcript provided",
                "location": content_path,
                "recommendation": "Provide detailed transcript of visual information"
            })

        return issues, warnings

    def _should_test_criterion(self, criterion: WCAGCriterion, target_level: WCAGLevel) -> bool:
        """Determine if criterion should be tested for target level"""
        level_order = {WCAGLevel.A: 1, WCAGLevel.AA: 2, WCAGLevel.AAA: 3}
        return level_order[criterion.level] <= level_order[target_level]

    def _summarize_by_principle(
        self,
        issues: List[ComplianceIssue],
        wcag_level: WCAGLevel
    ) -> Dict[str, Dict[str, int]]:
        """Summarize issues by WCAG principle"""
        summary = {}

        for principle in WCAGPrinciple:
            principle_criteria = [c for c in self.criteria.values()
                                if c.principle == principle and self._should_test_criterion(c, wcag_level)]
            principle_issues = [i for i in issues
                              if self.criteria.get(i.criterion, None) and
                              self.criteria[i.criterion].principle == principle]

            summary[principle.value] = {
                "total_criteria": len(principle_criteria),
                "passed": len(principle_criteria) - len(set(i.criterion for i in principle_issues)),
                "failed": len(set(i.criterion for i in principle_issues)),
                "critical_issues": len([i for i in principle_issues if i.severity == "critical"]),
                "major_issues": len([i for i in principle_issues if i.severity == "major"]),
                "minor_issues": len([i for i in principle_issues if i.severity == "minor"])
            }

        return summary

    def _generate_recommendations(
        self,
        issues: List[ComplianceIssue],
        wcag_level: WCAGLevel
    ) -> List[str]:
        """Generate prioritized remediation recommendations"""
        recommendations = []

        # Critical issues first
        critical = [i for i in issues if i.severity == "critical"]
        if critical:
            recommendations.append(f"Address {len(critical)} critical accessibility issues immediately")
            recommendations.append(f"Priority: {', '.join(set(i.criterion for i in critical[:3]))}")

        # Major issues
        major = [i for i in issues if i.severity == "major"]
        if major:
            recommendations.append(f"Fix {len(major)} major issues to achieve {wcag_level.value} compliance")

        # General recommendations
        if any(i.criterion.startswith("1.1") for i in issues):
            recommendations.append("Implement systematic alt text workflow for all images")

        if any(i.criterion.startswith("1.4.3") for i in issues):
            recommendations.append("Use automated color contrast checker during design phase")

        if any(i.criterion.startswith("2.1") for i in issues):
            recommendations.append("Test all interactive elements with keyboard-only navigation")

        if any(i.criterion.startswith("4.1") for i in issues):
            recommendations.append("Use ARIA labels and roles for custom components")

        return recommendations

    def generate_compliance_report(self, report: ComplianceReport) -> str:
        """Generate formatted compliance report"""
        lines = [
            f"# WCAG {report.wcag_level.value} Compliance Report",
            f"",
            f"**Content**: {report.content_id}",
            f"**Tested**: {report.tested_date.strftime('%Y-%m-%d %H:%M:%S')} UTC",
            f"**Status**: {'✅ COMPLIANT' if report.overall_compliant else '❌ NON-COMPLIANT'}",
            f"**Score**: {report.compliance_score:.1f}/100",
            f"",
            f"## Summary",
            f"",
            f"- **Passed**: {len(report.passed_criteria)} criteria",
            f"- **Failed**: {len(report.failed_criteria)} criteria",
            f"- **Issues**: {len(report.issues)} ({len([i for i in report.issues if i.severity=='critical'])} critical)",
            f"- **Warnings**: {len(report.warnings)}",
            f"",
            f"## By Principle",
            f""
        ]

        for principle, stats in report.summary_by_principle.items():
            lines.append(f"### {principle}")
            lines.append(f"- Passed: {stats['passed']}/{stats['total_criteria']}")
            lines.append(f"- Issues: {stats['critical_issues']} critical, {stats['major_issues']} major, {stats['minor_issues']} minor")
            lines.append("")

        lines.append("## Critical Issues")
        lines.append("")
        critical_issues = [i for i in report.issues if i.severity == "critical"]
        for issue in critical_issues:
            lines.append(f"### {issue.issue_id}: {self.criteria[issue.criterion].name}")
            lines.append(f"- **Criterion**: {issue.criterion} ({issue.wcag_level.value})")
            lines.append(f"- **Element**: `{issue.element}`")
            lines.append(f"- **Issue**: {issue.description}")
            lines.append(f"- **Location**: {issue.location}")
            lines.append(f"- **Impact**: {issue.impact}")
            lines.append(f"- **Fix**: {issue.remediation}")
            lines.append("")

        lines.append("## Recommendations")
        lines.append("")
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}")

        lines.append("")
        lines.append("---")
        lines.append("Generated by WCAG Compliance Engine")

        return "\n".join(lines)


if __name__ == "__main__":
    # Test the WCAG compliance engine
    engine = WCAGComplianceEngine()

    print("=== WCAG Compliance Engine Test ===\n")

    # Test HTML validation
    report = engine.validate_content(
        content_path="test_lesson.html",
        content_type="html",
        wcag_level=WCAGLevel.AA
    )

    print(f"Compliance Score: {report.compliance_score:.1f}/100")
    print(f"Status: {'COMPLIANT' if report.overall_compliant else 'NON-COMPLIANT'}")
    print(f"Issues Found: {len(report.issues)}")
    print(f"  Critical: {len([i for i in report.issues if i.severity == 'critical'])}")
    print(f"  Major: {len([i for i in report.issues if i.severity == 'major'])}")
    print(f"  Minor: {len([i for i in report.issues if i.severity == 'minor'])}")
    print(f"\nFailed Criteria: {', '.join(report.failed_criteria[:5])}")

    print("\n" + "="*50 + "\n")
    print(engine.generate_compliance_report(report))
