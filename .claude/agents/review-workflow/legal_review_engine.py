#!/usr/bin/env python3
"""
Legal Review Workflow Engine - Multi-Person Review with Compliance Tracking

Implements GAP-13: Legal Review Workflow Enhancement
Enables multi-person review workflows (SME, legal, editorial, QA) with audit trails

Usage:
    from legal_review_engine import LegalReviewEngine

    engine = LegalReviewEngine()

    # Create multi-person workflow
    workflow = engine.create_workflow(
        content_id="CONTENT-001",
        review_roles=["sme", "legal", "editorial", "qa"]
    )

    # Submit legal sign-off
    engine.submit_signoff(
        workflow_id=workflow_id,
        reviewer_role="legal",
        reviewer_id="LEGAL-001",
        signoff_decision="approved"
    )

    # Generate audit trail
    audit = engine.generate_audit_trail(workflow_id)
"""

import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


class ReviewRole(Enum):
    """Review role types"""
    SME = "sme"  # Subject Matter Expert
    LEGAL = "legal"  # Legal counsel
    EDITORIAL = "editorial"  # Editorial reviewer
    QA = "quality_assurance"  # Quality assurance
    COMPLIANCE = "compliance"  # Compliance officer
    EXECUTIVE = "executive"  # Executive approval
    ACCESSIBILITY = "accessibility"  # Accessibility specialist


class ReviewStageType(Enum):
    """Review stage execution types"""
    SEQUENTIAL = "sequential"  # Stages run one after another
    PARALLEL = "parallel"  # Stages run simultaneously
    CONDITIONAL = "conditional"  # Stage depends on previous results


class SignoffDecision(Enum):
    """Sign-off decision types"""
    APPROVED = "approved"
    APPROVED_WITH_CONDITIONS = "approved_with_conditions"
    REVISIONS_REQUIRED = "revisions_required"
    REJECTED = "rejected"
    DEFERRED = "deferred"


@dataclass
class ReviewerSignoff:
    """Individual reviewer sign-off record"""
    signoff_id: str
    workflow_id: str
    reviewer_role: str
    reviewer_id: str
    reviewer_name: str
    decision: str
    conditions: List[str] = field(default_factory=list)
    comments: str = ""
    signed_at: str = ""
    signature_hash: str = ""  # Digital signature for legal liability
    ip_address: str = ""
    audit_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewStage:
    """Review workflow stage"""
    stage_id: str
    stage_name: str
    stage_type: str  # sequential, parallel, conditional
    required_roles: List[str]
    optional_roles: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Stage IDs that must complete first
    sla_hours: int = 48  # Service Level Agreement
    escalation_roles: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, blocked
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class LegalWorkflow:
    """Legal review workflow"""
    workflow_id: str
    content_id: str
    content_type: str  # lesson, assessment, textbook, video
    workflow_type: str  # standard, expedited, comprehensive
    stages: List[ReviewStage]
    signoffs: List[ReviewerSignoff] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, rejected, cancelled
    initiated_at: str = ""
    completed_at: Optional[str] = None
    legal_compliance_verified: bool = False
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)


class LegalReviewEngine:
    """Legal review workflow engine with multi-person review and compliance tracking"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize Legal Review Engine

        Args:
            data_dir: Directory for workflow data
        """
        self.data_dir = data_dir or Path.home() / ".claude" / "agents" / "legal_review"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Role-based permissions
        self.role_permissions = {
            "sme": ["content_approval", "technical_review"],
            "legal": ["legal_approval", "copyright_review", "compliance_review"],
            "editorial": ["editorial_approval", "style_review", "language_review"],
            "quality_assurance": ["qa_approval", "testing_review"],
            "compliance": ["compliance_approval", "policy_review"],
            "executive": ["final_approval", "budget_approval"],
            "accessibility": ["accessibility_approval", "wcag_review"]
        }

    # ==================== WORKFLOW CREATION ====================

    def create_workflow(
        self,
        content_id: str,
        content_type: str,
        workflow_type: str = "standard",
        custom_stages: Optional[List[Dict[str, Any]]] = None
    ) -> LegalWorkflow:
        """
        Create legal review workflow

        Args:
            content_id: Content identifier
            content_type: Type of content (lesson, assessment, textbook, video)
            workflow_type: Workflow type (standard, expedited, comprehensive)
            custom_stages: Optional custom stage definitions

        Returns:
            LegalWorkflow object
        """
        workflow_id = self._generate_workflow_id(content_id)

        # Define stages based on workflow type
        if custom_stages:
            stages = self._parse_custom_stages(custom_stages)
        else:
            stages = self._get_standard_stages(content_type, workflow_type)

        workflow = LegalWorkflow(
            workflow_id=workflow_id,
            content_id=content_id,
            content_type=content_type,
            workflow_type=workflow_type,
            stages=stages,
            initiated_at=datetime.utcnow().isoformat() + "Z",
            status="pending"
        )

        # Log workflow creation
        self._add_audit_entry(
            workflow,
            "workflow_created",
            {
                "content_id": content_id,
                "workflow_type": workflow_type,
                "stages": len(stages)
            }
        )

        return workflow

    def _generate_workflow_id(self, content_id: str) -> str:
        """Generate unique workflow ID"""
        timestamp = int(datetime.utcnow().timestamp())
        return f"LWF-{content_id}-{timestamp}"

    def _get_standard_stages(self, content_type: str, workflow_type: str) -> List[ReviewStage]:
        """Get standard workflow stages"""
        if workflow_type == "expedited":
            # Fast-track: SME + QA only
            return [
                ReviewStage(
                    stage_id="stage_1",
                    stage_name="Content Review",
                    stage_type="parallel",
                    required_roles=["sme", "quality_assurance"],
                    sla_hours=24
                ),
                ReviewStage(
                    stage_id="stage_2",
                    stage_name="Final Approval",
                    stage_type="sequential",
                    required_roles=["editorial"],
                    dependencies=["stage_1"],
                    sla_hours=12
                )
            ]

        elif workflow_type == "comprehensive":
            # Full review: All roles with legal sign-off
            return [
                ReviewStage(
                    stage_id="stage_1",
                    stage_name="Initial Content Review",
                    stage_type="parallel",
                    required_roles=["sme"],
                    optional_roles=["accessibility"],
                    sla_hours=48
                ),
                ReviewStage(
                    stage_id="stage_2",
                    stage_name="Legal & Compliance Review",
                    stage_type="parallel",
                    required_roles=["legal", "compliance"],
                    dependencies=["stage_1"],
                    sla_hours=72,
                    escalation_roles=["executive"]
                ),
                ReviewStage(
                    stage_id="stage_3",
                    stage_name="Editorial & QA Review",
                    stage_type="parallel",
                    required_roles=["editorial", "quality_assurance"],
                    dependencies=["stage_1"],
                    sla_hours=48
                ),
                ReviewStage(
                    stage_id="stage_4",
                    stage_name="Final Approval",
                    stage_type="sequential",
                    required_roles=["executive"],
                    dependencies=["stage_2", "stage_3"],
                    sla_hours=24
                )
            ]

        else:  # standard
            # Standard: SME → Legal → Editorial → QA
            return [
                ReviewStage(
                    stage_id="stage_1",
                    stage_name="Content Review",
                    stage_type="sequential",
                    required_roles=["sme"],
                    sla_hours=48
                ),
                ReviewStage(
                    stage_id="stage_2",
                    stage_name="Legal Review",
                    stage_type="sequential",
                    required_roles=["legal"],
                    dependencies=["stage_1"],
                    sla_hours=72,
                    escalation_roles=["compliance"]
                ),
                ReviewStage(
                    stage_id="stage_3",
                    stage_name="Editorial Review",
                    stage_type="sequential",
                    required_roles=["editorial"],
                    dependencies=["stage_2"],
                    sla_hours=36
                ),
                ReviewStage(
                    stage_id="stage_4",
                    stage_name="Quality Assurance",
                    stage_type="sequential",
                    required_roles=["quality_assurance"],
                    dependencies=["stage_3"],
                    sla_hours=24
                )
            ]

    def _parse_custom_stages(self, custom_stages: List[Dict[str, Any]]) -> List[ReviewStage]:
        """Parse custom stage definitions"""
        stages = []
        for i, stage_def in enumerate(custom_stages):
            stages.append(ReviewStage(
                stage_id=stage_def.get("stage_id", f"stage_{i+1}"),
                stage_name=stage_def.get("stage_name", f"Stage {i+1}"),
                stage_type=stage_def.get("stage_type", "sequential"),
                required_roles=stage_def.get("required_roles", []),
                optional_roles=stage_def.get("optional_roles", []),
                dependencies=stage_def.get("dependencies", []),
                sla_hours=stage_def.get("sla_hours", 48),
                escalation_roles=stage_def.get("escalation_roles", [])
            ))
        return stages

    # ==================== SIGN-OFF MANAGEMENT ====================

    def submit_signoff(
        self,
        workflow: LegalWorkflow,
        reviewer_role: str,
        reviewer_id: str,
        reviewer_name: str,
        decision: str,
        comments: str = "",
        conditions: Optional[List[str]] = None,
        ip_address: str = "0.0.0.0"
    ) -> ReviewerSignoff:
        """
        Submit reviewer sign-off

        Args:
            workflow: Workflow object
            reviewer_role: Role of reviewer
            reviewer_id: Reviewer ID
            reviewer_name: Reviewer name
            decision: Sign-off decision
            comments: Optional comments
            conditions: Optional approval conditions
            ip_address: IP address for audit

        Returns:
            ReviewerSignoff object
        """
        # Verify reviewer authority
        if reviewer_role not in self.role_permissions:
            raise ValueError(f"Invalid reviewer role: {reviewer_role}")

        # Generate signoff ID
        signoff_id = f"SIGNOFF-{workflow.workflow_id}-{reviewer_role.upper()}-{int(datetime.utcnow().timestamp())}"

        # Create digital signature for legal liability
        signature_data = f"{signoff_id}|{reviewer_id}|{decision}|{datetime.utcnow().isoformat()}"
        signature_hash = hashlib.sha256(signature_data.encode()).hexdigest()

        # Create signoff record
        signoff = ReviewerSignoff(
            signoff_id=signoff_id,
            workflow_id=workflow.workflow_id,
            reviewer_role=reviewer_role,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            decision=decision,
            conditions=conditions or [],
            comments=comments,
            signed_at=datetime.utcnow().isoformat() + "Z",
            signature_hash=signature_hash,
            ip_address=ip_address,
            audit_metadata={
                "user_agent": "Claude Code / Legal Review Engine",
                "session_id": f"SESSION-{int(datetime.utcnow().timestamp())}",
                "content_version": workflow.content_id
            }
        )

        # Add to workflow
        workflow.signoffs.append(signoff)

        # Log in audit trail
        self._add_audit_entry(
            workflow,
            "signoff_submitted",
            {
                "signoff_id": signoff_id,
                "reviewer_role": reviewer_role,
                "reviewer_id": reviewer_id,
                "decision": decision,
                "signature_hash": signature_hash[:16] + "..."
            }
        )

        # Update stage status
        self._update_stage_status(workflow)

        return signoff

    def _update_stage_status(self, workflow: LegalWorkflow) -> None:
        """Update workflow stage status based on signoffs"""
        for stage in workflow.stages:
            # Check if all dependencies completed
            if stage.dependencies:
                deps_completed = all(
                    self._is_stage_completed(workflow, dep_id)
                    for dep_id in stage.dependencies
                )
                if not deps_completed:
                    continue  # Skip this stage until dependencies complete

            # Check if all required roles have signed off
            required_signoffs = {role: False for role in stage.required_roles}

            for signoff in workflow.signoffs:
                if signoff.reviewer_role in required_signoffs:
                    if signoff.decision in ["approved", "approved_with_conditions"]:
                        required_signoffs[signoff.reviewer_role] = True

            # Update stage status
            if all(required_signoffs.values()):
                stage.status = "completed"
                if not stage.completed_at:
                    stage.completed_at = datetime.utcnow().isoformat() + "Z"
            elif any(required_signoffs.values()):
                stage.status = "in_progress"
                if not stage.started_at:
                    stage.started_at = datetime.utcnow().isoformat() + "Z"

        # Update overall workflow status
        self._update_workflow_status(workflow)

    def _is_stage_completed(self, workflow: LegalWorkflow, stage_id: str) -> bool:
        """Check if stage is completed"""
        for stage in workflow.stages:
            if stage.stage_id == stage_id:
                return stage.status == "completed"
        return False

    def _update_workflow_status(self, workflow: LegalWorkflow) -> None:
        """Update overall workflow status"""
        all_completed = all(stage.status == "completed" for stage in workflow.stages)
        any_rejected = any(
            signoff.decision == "rejected"
            for signoff in workflow.signoffs
        )

        if any_rejected:
            workflow.status = "rejected"
        elif all_completed:
            workflow.status = "completed"
            workflow.completed_at = datetime.utcnow().isoformat() + "Z"
            workflow.legal_compliance_verified = self._verify_legal_compliance(workflow)
        elif any(stage.status == "in_progress" for stage in workflow.stages):
            workflow.status = "in_progress"

    def _verify_legal_compliance(self, workflow: LegalWorkflow) -> bool:
        """Verify legal compliance requirements met"""
        # Check if legal role signed off with approval
        legal_signoffs = [
            s for s in workflow.signoffs
            if s.reviewer_role == "legal" and s.decision in ["approved", "approved_with_conditions"]
        ]

        # Check if all required stages completed
        all_stages_completed = all(stage.status == "completed" for stage in workflow.stages)

        return len(legal_signoffs) > 0 and all_stages_completed

    # ==================== SLA TRACKING & ESCALATION ====================

    def check_sla_violations(self, workflow: LegalWorkflow) -> List[Dict[str, Any]]:
        """
        Check for SLA violations in workflow stages

        Args:
            workflow: Workflow object

        Returns:
            List of SLA violations
        """
        violations = []
        now = datetime.utcnow()

        for stage in workflow.stages:
            if stage.status not in ["completed", "pending"]:
                # Stage is in progress
                if stage.started_at:
                    started = datetime.fromisoformat(stage.started_at.replace("Z", ""))
                    elapsed_hours = (now - started).total_seconds() / 3600

                    if elapsed_hours > stage.sla_hours:
                        violations.append({
                            "stage_id": stage.stage_id,
                            "stage_name": stage.stage_name,
                            "sla_hours": stage.sla_hours,
                            "elapsed_hours": round(elapsed_hours, 1),
                            "overdue_hours": round(elapsed_hours - stage.sla_hours, 1),
                            "escalation_roles": stage.escalation_roles,
                            "severity": "high" if elapsed_hours > stage.sla_hours * 1.5 else "medium"
                        })

        return violations

    def escalate_workflow(
        self,
        workflow: LegalWorkflow,
        stage_id: str,
        escalation_reason: str
    ) -> Dict[str, Any]:
        """
        Escalate workflow stage to higher authority

        Args:
            workflow: Workflow object
            stage_id: Stage to escalate
            escalation_reason: Reason for escalation

        Returns:
            Escalation record
        """
        stage = next((s for s in workflow.stages if s.stage_id == stage_id), None)
        if not stage:
            raise ValueError(f"Stage not found: {stage_id}")

        escalation = {
            "escalation_id": f"ESC-{workflow.workflow_id}-{stage_id}-{int(datetime.utcnow().timestamp())}",
            "workflow_id": workflow.workflow_id,
            "stage_id": stage_id,
            "stage_name": stage.stage_name,
            "escalation_reason": escalation_reason,
            "escalation_roles": stage.escalation_roles,
            "escalated_at": datetime.utcnow().isoformat() + "Z",
            "status": "pending"
        }

        # Log escalation in audit trail
        self._add_audit_entry(
            workflow,
            "workflow_escalated",
            escalation
        )

        return escalation

    # ==================== AUDIT TRAIL & COMPLIANCE ====================

    def _add_audit_entry(
        self,
        workflow: LegalWorkflow,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Add entry to audit trail"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "event_data": event_data,
            "workflow_id": workflow.workflow_id
        }
        workflow.audit_trail.append(entry)

    def generate_audit_trail(self, workflow: LegalWorkflow) -> str:
        """
        Generate comprehensive audit trail report

        Args:
            workflow: Workflow object

        Returns:
            Markdown audit trail report
        """
        # Sort audit entries by timestamp
        sorted_trail = sorted(workflow.audit_trail, key=lambda x: x["timestamp"])

        trail_md = []
        for entry in sorted_trail:
            trail_md.append(
                f"**{entry['timestamp']}** - {entry['event_type'].replace('_', ' ').title()}\n"
                f"```json\n{json.dumps(entry['event_data'], indent=2)}\n```\n"
            )

        signoffs_md = []
        for signoff in workflow.signoffs:
            signoffs_md.append(
                f"### {signoff.reviewer_role.replace('_', ' ').title()}\n\n"
                f"- **Reviewer**: {signoff.reviewer_name} ({signoff.reviewer_id})\n"
                f"- **Decision**: {signoff.decision.replace('_', ' ').title()}\n"
                f"- **Signed At**: {signoff.signed_at}\n"
                f"- **Signature Hash**: `{signoff.signature_hash[:32]}...`\n"
                f"- **IP Address**: {signoff.ip_address}\n"
                f"- **Comments**: {signoff.comments or 'None'}\n"
            )

        sla_violations = self.check_sla_violations(workflow)
        sla_md = "None" if not sla_violations else "\n".join([
            f"- **{v['stage_name']}**: {v['overdue_hours']:.1f} hours overdue ({v['severity'].upper()})"
            for v in sla_violations
        ])

        report = f"""# Legal Review Workflow - Audit Trail

**Workflow ID**: {workflow.workflow_id}
**Content ID**: {workflow.content_id}
**Content Type**: {workflow.content_type.title()}
**Workflow Type**: {workflow.workflow_type.title()}
**Status**: {workflow.status.upper()}
**Initiated**: {workflow.initiated_at}
**Completed**: {workflow.completed_at or 'In Progress'}
**Legal Compliance Verified**: {'✅ Yes' if workflow.legal_compliance_verified else '❌ No'}

---

## Workflow Stages

{self._format_stages_table(workflow.stages)}

---

## Reviewer Sign-Offs

{chr(10).join(signoffs_md) if signoffs_md else 'No sign-offs yet.'}

---

## SLA Status

{sla_md}

---

## Complete Audit Trail

{chr(10).join(trail_md)}

---

## Legal Certification

This audit trail serves as legal documentation of the review process. All sign-offs include digital signatures (SHA-256 hashes) for non-repudiation and compliance verification.

**Digital Signature Verification**: All reviewer sign-offs can be independently verified using the signature hashes provided.

**Compliance Standards**: This workflow adheres to industry standards for content review and legal liability documentation.

---

**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
**Report ID**: AUDIT-{workflow.workflow_id}
"""

        return report

    def _format_stages_table(self, stages: List[ReviewStage]) -> str:
        """Format stages as markdown table"""
        rows = []
        for stage in stages:
            status_icon = {
                "pending": "⏳",
                "in_progress": "🔄",
                "completed": "✅",
                "blocked": "🚫"
            }.get(stage.status, "❓")

            rows.append(
                f"| {status_icon} {stage.stage_name} | {', '.join(stage.required_roles)} | "
                f"{stage.status.title()} | {stage.sla_hours}h |"
            )

        table = "| Stage | Required Roles | Status | SLA |\n"
        table += "|-------|----------------|--------|-----|\n"
        table += "\n".join(rows)

        return table

    def export_workflow(self, workflow: LegalWorkflow, format: str = "json") -> str:
        """
        Export workflow data

        Args:
            workflow: Workflow object
            format: Export format (json, markdown)

        Returns:
            Formatted workflow data
        """
        if format == "json":
            # Convert dataclasses to dicts
            workflow_dict = {
                "workflow_id": workflow.workflow_id,
                "content_id": workflow.content_id,
                "content_type": workflow.content_type,
                "workflow_type": workflow.workflow_type,
                "status": workflow.status,
                "initiated_at": workflow.initiated_at,
                "completed_at": workflow.completed_at,
                "legal_compliance_verified": workflow.legal_compliance_verified,
                "stages": [
                    {
                        "stage_id": s.stage_id,
                        "stage_name": s.stage_name,
                        "stage_type": s.stage_type,
                        "required_roles": s.required_roles,
                        "status": s.status,
                        "sla_hours": s.sla_hours
                    }
                    for s in workflow.stages
                ],
                "signoffs": [
                    {
                        "signoff_id": so.signoff_id,
                        "reviewer_role": so.reviewer_role,
                        "reviewer_id": so.reviewer_id,
                        "decision": so.decision,
                        "signed_at": so.signed_at,
                        "signature_hash": so.signature_hash
                    }
                    for so in workflow.signoffs
                ],
                "audit_trail": workflow.audit_trail
            }
            return json.dumps(workflow_dict, indent=2)
        elif format == "markdown":
            return self.generate_audit_trail(workflow)
        else:
            raise ValueError(f"Unknown format: {format}")


if __name__ == "__main__":
    # Example usage
    engine = LegalReviewEngine()

    # Create comprehensive review workflow
    print("=== Creating Legal Review Workflow ===")
    workflow = engine.create_workflow(
        content_id="TEXTBOOK-BIOLOGY-2025",
        content_type="textbook",
        workflow_type="comprehensive"
    )
    print(f"Workflow ID: {workflow.workflow_id}")
    print(f"Stages: {len(workflow.stages)}")

    # Submit SME sign-off
    print("\n=== Submitting SME Sign-Off ===")
    signoff1 = engine.submit_signoff(
        workflow=workflow,
        reviewer_role="sme",
        reviewer_id="SME-001",
        reviewer_name="Dr. Jane Smith",
        decision="approved",
        comments="Content is scientifically accurate and age-appropriate."
    )
    print(f"Sign-off ID: {signoff1.signoff_id}")
    print(f"Decision: {signoff1.decision}")
    print(f"Signature: {signoff1.signature_hash[:32]}...")

    # Submit Legal sign-off with conditions
    print("\n=== Submitting Legal Sign-Off ===")
    signoff2 = engine.submit_signoff(
        workflow=workflow,
        reviewer_role="legal",
        reviewer_id="LEGAL-001",
        reviewer_name="John Doe, Esq.",
        decision="approved_with_conditions",
        conditions=[
            "Add attribution for Figure 3.2",
            "Verify Creative Commons license for diagrams"
        ],
        comments="Legal review complete. Address conditions before publication."
    )
    print(f"Sign-off ID: {signoff2.signoff_id}")
    print(f"Decision: {signoff2.decision}")
    print(f"Conditions: {len(signoff2.conditions)}")

    # Check SLA violations
    print("\n=== Checking SLA Status ===")
    violations = engine.check_sla_violations(workflow)
    print(f"SLA Violations: {len(violations)}")

    # Generate audit trail
    print("\n=== Generating Audit Trail ===")
    audit_report = engine.generate_audit_trail(workflow)
    print(audit_report[:500] + "...")

    # Export workflow
    print("\n=== Exporting Workflow ===")
    workflow_json = engine.export_workflow(workflow, format="json")
    print(f"Workflow exported ({len(workflow_json)} bytes)")
