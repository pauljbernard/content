#!/usr/bin/env python3
"""
Client Portal & Handoff System - Secure Content Delivery and Feedback Collection

Implements GAP-14: Client Portal & Handoff Enhancement
Provides secure material delivery, client feedback collection, and approval workflows

Usage:
    from client_portal import ClientPortal, DeliveryPackage, FeedbackManager

    # Create client portal
    portal = ClientPortal()

    # Create delivery package
    package = portal.create_delivery_package(
        project_id="PROJ-2025-001",
        client_id="CLIENT-ABC",
        content_items=["LESSON-001", "LESSON-002", "ASSESSMENT-001"]
    )

    # Generate secure download link
    link = portal.generate_download_link(package.package_id, expiration_hours=72)

    # Collect client feedback
    feedback_mgr = FeedbackManager()
    feedback = feedback_mgr.collect_feedback(
        package_id=package.package_id,
        reviewer_name="Jane Smith",
        feedback_items=[...]
    )
"""

import json
import secrets
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


class PackageStatus(Enum):
    """Delivery package status"""
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    DOWNLOADED = "downloaded"
    APPROVED = "approved"
    REVISIONS_REQUESTED = "revisions_requested"
    REJECTED = "rejected"


class FeedbackPriority(Enum):
    """Feedback priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NICE_TO_HAVE = "nice_to_have"


class ContentFormat(Enum):
    """Content delivery formats"""
    PDF = "pdf"
    SCORM_12 = "scorm_1_2"
    SCORM_2004 = "scorm_2004"
    HTML = "html"
    DOCX = "docx"
    QTI_21 = "qti_2_1"
    SOURCE_FILES = "source_files"


@dataclass
class DeliveryPackage:
    """Content delivery package"""
    package_id: str
    project_id: str
    client_id: str
    content_items: List[str]
    formats: List[str]
    status: str
    created_at: str
    download_url: Optional[str] = None
    download_expires_at: Optional[str] = None
    download_count: int = 0
    approved_at: Optional[str] = None
    package_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FeedbackItem:
    """Individual feedback item"""
    feedback_id: str
    content_id: str
    content_section: str  # Location in content
    priority: str
    category: str  # content, pedagogy, technical, accessibility, other
    description: str
    suggested_fix: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    status: str = "open"  # open, in_progress, resolved, wont_fix
    created_at: str = ""
    resolved_at: Optional[str] = None


@dataclass
class ClientFeedback:
    """Client feedback collection"""
    feedback_collection_id: str
    package_id: str
    reviewer_name: str
    reviewer_email: str
    overall_rating: int  # 1-5 scale
    overall_comments: str
    feedback_items: List[FeedbackItem]
    approval_decision: str  # approved, revisions_required, rejected
    submitted_at: str = ""


@dataclass
class DownloadLog:
    """Download activity log"""
    log_id: str
    package_id: str
    download_token: str
    ip_address: str
    user_agent: str
    downloaded_at: str
    file_size_bytes: int


class ClientPortal:
    """Client portal for content delivery and feedback"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize Client Portal

        Args:
            data_dir: Directory for portal data
        """
        self.data_dir = data_dir or Path.home() / ".claude" / "agents" / "client_portal"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.packages: List[DeliveryPackage] = []
        self.download_tokens: Dict[str, Dict[str, Any]] = {}  # token -> metadata

    def create_delivery_package(
        self,
        project_id: str,
        client_id: str,
        content_items: List[str],
        formats: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DeliveryPackage:
        """
        Create content delivery package

        Args:
            project_id: Project identifier
            client_id: Client identifier
            content_items: List of content item IDs
            formats: Optional list of delivery formats
            metadata: Optional package metadata

        Returns:
            DeliveryPackage object
        """
        package_id = f"PKG-{project_id}-{int(datetime.utcnow().timestamp())}"

        if formats is None:
            formats = ["pdf", "scorm_2004", "html"]

        package = DeliveryPackage(
            package_id=package_id,
            project_id=project_id,
            client_id=client_id,
            content_items=content_items,
            formats=formats,
            status=PackageStatus.PREPARING.value,
            created_at=datetime.utcnow().isoformat() + "Z",
            package_metadata=metadata or {}
        )

        self.packages.append(package)

        # Start package preparation
        self._prepare_package(package)

        return package

    def _prepare_package(self, package: DeliveryPackage):
        """Prepare delivery package (async in production)"""
        # In production:
        # 1. Export content in all requested formats
        # 2. Create ZIP archive
        # 3. Calculate checksums
        # 4. Upload to secure storage (S3, Azure Blob, etc.)
        # 5. Generate manifest

        # For now, mark as ready
        package.status = PackageStatus.READY.value

    def generate_download_link(
        self,
        package_id: str,
        expiration_hours: int = 72,
        max_downloads: int = 10
    ) -> str:
        """
        Generate secure download link

        Args:
            package_id: Package identifier
            expiration_hours: Link expiration in hours
            max_downloads: Maximum number of downloads allowed

        Returns:
            Secure download URL
        """
        package = self._get_package(package_id)

        if not package:
            raise ValueError(f"Package not found: {package_id}")

        if package.status != PackageStatus.READY.value:
            raise ValueError(f"Package not ready for download: {package.status}")

        # Generate cryptographically secure token
        download_token = secrets.token_urlsafe(32)

        # Calculate expiration
        expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)

        # Store token metadata
        self.download_tokens[download_token] = {
            "package_id": package_id,
            "expires_at": expires_at.isoformat() + "Z",
            "max_downloads": max_downloads,
            "download_count": 0,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        # Generate download URL
        base_url = "https://portal.professor.ai"  # In production, use actual domain
        download_url = f"{base_url}/download/{download_token}"

        # Update package
        package.download_url = download_url
        package.download_expires_at = expires_at.isoformat() + "Z"

        return download_url

    def validate_download_token(
        self,
        token: str,
        ip_address: str,
        user_agent: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate download token

        Args:
            token: Download token
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            (is_valid, error_message) tuple
        """
        if token not in self.download_tokens:
            return False, "Invalid download token"

        token_data = self.download_tokens[token]

        # Check expiration
        expires_at = datetime.fromisoformat(token_data["expires_at"].replace("Z", ""))
        if datetime.utcnow() > expires_at:
            return False, "Download link expired"

        # Check download limit
        if token_data["download_count"] >= token_data["max_downloads"]:
            return False, "Download limit exceeded"

        return True, None

    def log_download(
        self,
        token: str,
        ip_address: str,
        user_agent: str,
        file_size_bytes: int
    ) -> DownloadLog:
        """
        Log download activity

        Args:
            token: Download token
            ip_address: Client IP address
            user_agent: Client user agent
            file_size_bytes: Downloaded file size

        Returns:
            DownloadLog object
        """
        token_data = self.download_tokens[token]
        package_id = token_data["package_id"]

        # Increment download count
        token_data["download_count"] += 1

        # Update package
        package = self._get_package(package_id)
        if package:
            package.download_count += 1
            if package.status == PackageStatus.READY.value:
                package.status = PackageStatus.DOWNLOADED.value

        # Create download log
        log = DownloadLog(
            log_id=f"DL-{int(datetime.utcnow().timestamp())}",
            package_id=package_id,
            download_token=token[:16] + "...",  # Truncate for security
            ip_address=ip_address,
            user_agent=user_agent,
            downloaded_at=datetime.utcnow().isoformat() + "Z",
            file_size_bytes=file_size_bytes
        )

        return log

    def get_package_manifest(self, package_id: str) -> Dict[str, Any]:
        """
        Get package manifest

        Args:
            package_id: Package identifier

        Returns:
            Package manifest with file listing
        """
        package = self._get_package(package_id)

        if not package:
            raise ValueError(f"Package not found: {package_id}")

        # Generate manifest
        manifest = {
            "package_id": package.package_id,
            "project_id": package.project_id,
            "created_at": package.created_at,
            "content_items": len(package.content_items),
            "formats": package.formats,
            "files": []
        }

        # List files for each format
        for item_id in package.content_items:
            for format_type in package.formats:
                manifest["files"].append({
                    "content_id": item_id,
                    "format": format_type,
                    "filename": f"{item_id}.{format_type}",
                    "size_bytes": 1024000,  # Mock size
                    "checksum": hashlib.sha256(f"{item_id}{format_type}".encode()).hexdigest()
                })

        # Add metadata files
        manifest["files"].extend([
            {
                "filename": "README.txt",
                "description": "Package information and usage instructions",
                "size_bytes": 2048
            },
            {
                "filename": "MANIFEST.json",
                "description": "Complete package manifest",
                "size_bytes": 4096
            },
            {
                "filename": "LICENSE.txt",
                "description": "Content license and usage terms",
                "size_bytes": 8192
            }
        ])

        return manifest

    def _get_package(self, package_id: str) -> Optional[DeliveryPackage]:
        """Get package by ID"""
        for package in self.packages:
            if package.package_id == package_id:
                return package
        return None


class FeedbackManager:
    """Client feedback collection and management"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize Feedback Manager

        Args:
            data_dir: Directory for feedback data
        """
        self.data_dir = data_dir or Path.home() / ".claude" / "agents" / "client_feedback"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_collections: List[ClientFeedback] = []

    def collect_feedback(
        self,
        package_id: str,
        reviewer_name: str,
        reviewer_email: str,
        overall_rating: int,
        overall_comments: str,
        feedback_items: List[Dict[str, Any]],
        approval_decision: str
    ) -> ClientFeedback:
        """
        Collect client feedback

        Args:
            package_id: Package identifier
            reviewer_name: Reviewer name
            reviewer_email: Reviewer email
            overall_rating: Overall rating (1-5)
            overall_comments: Overall comments
            feedback_items: List of feedback items
            approval_decision: Approval decision

        Returns:
            ClientFeedback object
        """
        feedback_id = f"FB-{package_id}-{int(datetime.utcnow().timestamp())}"

        # Parse feedback items
        items = []
        for i, item_data in enumerate(feedback_items):
            item = FeedbackItem(
                feedback_id=f"{feedback_id}-ITEM-{i+1:03d}",
                content_id=item_data.get("content_id", ""),
                content_section=item_data.get("content_section", ""),
                priority=item_data.get("priority", "medium"),
                category=item_data.get("category", "other"),
                description=item_data.get("description", ""),
                suggested_fix=item_data.get("suggested_fix"),
                attachments=item_data.get("attachments", []),
                created_at=datetime.utcnow().isoformat() + "Z"
            )
            items.append(item)

        feedback = ClientFeedback(
            feedback_collection_id=feedback_id,
            package_id=package_id,
            reviewer_name=reviewer_name,
            reviewer_email=reviewer_email,
            overall_rating=overall_rating,
            overall_comments=overall_comments,
            feedback_items=items,
            approval_decision=approval_decision,
            submitted_at=datetime.utcnow().isoformat() + "Z"
        )

        self.feedback_collections.append(feedback)
        return feedback

    def generate_feedback_report(self, feedback_id: str) -> str:
        """
        Generate feedback report

        Args:
            feedback_id: Feedback collection ID

        Returns:
            Markdown feedback report
        """
        feedback = self._get_feedback(feedback_id)

        if not feedback:
            raise ValueError(f"Feedback not found: {feedback_id}")

        # Group feedback by category
        by_category = {}
        for item in feedback.feedback_items:
            category = item.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(item)

        # Group feedback by priority
        by_priority = {}
        for item in feedback.feedback_items:
            priority = item.priority
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(item)

        # Generate category sections
        category_sections = []
        for category, items in by_category.items():
            items_md = []
            for item in items:
                items_md.append(
                    f"**{item.content_id} - {item.content_section}** ({item.priority.upper()})\n"
                    f"{item.description}\n"
                    f"{f'*Suggested Fix*: {item.suggested_fix}' if item.suggested_fix else ''}\n"
                )
            category_sections.append(
                f"### {category.replace('_', ' ').title()}\n\n" +
                "\n".join(items_md)
            )

        # Stars for rating
        rating_stars = "★" * feedback.overall_rating + "☆" * (5 - feedback.overall_rating)

        report = f"""# Client Feedback Report

**Feedback ID**: {feedback.feedback_collection_id}
**Package ID**: {feedback.package_id}
**Reviewer**: {feedback.reviewer_name} ({feedback.reviewer_email})
**Submitted**: {feedback.submitted_at}
**Decision**: {feedback.approval_decision.replace('_', ' ').upper()}

---

## Overall Assessment

**Rating**: {rating_stars} ({feedback.overall_rating}/5)

**Comments**:
{feedback.overall_comments}

---

## Feedback Summary

**Total Items**: {len(feedback.feedback_items)}

**By Priority**:
- Critical: {len(by_priority.get('critical', []))}
- High: {len(by_priority.get('high', []))}
- Medium: {len(by_priority.get('medium', []))}
- Low: {len(by_priority.get('low', []))}
- Nice-to-Have: {len(by_priority.get('nice_to_have', []))}

**By Category**:
- Content: {len(by_category.get('content', []))}
- Pedagogy: {len(by_category.get('pedagogy', []))}
- Technical: {len(by_category.get('technical', []))}
- Accessibility: {len(by_category.get('accessibility', []))}
- Other: {len(by_category.get('other', []))}

---

## Detailed Feedback

{chr(10).join(category_sections)}

---

**Next Steps**:
{'- Address critical and high-priority items immediately' if len(by_priority.get('critical', [])) + len(by_priority.get('high', [])) > 0 else '- Review all feedback items and prioritize'}
- Create revision tasks for each feedback item
- Schedule follow-up review after revisions
{'- Deliver final version after approval' if feedback.approval_decision == 'approved' else '- Submit revised version for re-review'}

---

**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
"""

        return report

    def track_feedback_resolution(
        self,
        feedback_id: str
    ) -> Dict[str, Any]:
        """
        Track feedback resolution progress

        Args:
            feedback_id: Feedback collection ID

        Returns:
            Resolution progress metrics
        """
        feedback = self._get_feedback(feedback_id)

        if not feedback:
            raise ValueError(f"Feedback not found: {feedback_id}")

        total_items = len(feedback.feedback_items)
        resolved_items = sum(1 for item in feedback.feedback_items if item.status == "resolved")
        in_progress_items = sum(1 for item in feedback.feedback_items if item.status == "in_progress")
        open_items = sum(1 for item in feedback.feedback_items if item.status == "open")

        progress = {
            "feedback_id": feedback_id,
            "total_items": total_items,
            "resolved": resolved_items,
            "in_progress": in_progress_items,
            "open": open_items,
            "completion_percentage": round((resolved_items / total_items * 100), 1) if total_items > 0 else 0,
            "by_priority": {
                priority: {
                    "total": len([i for i in feedback.feedback_items if i.priority == priority]),
                    "resolved": len([i for i in feedback.feedback_items if i.priority == priority and i.status == "resolved"])
                }
                for priority in ["critical", "high", "medium", "low", "nice_to_have"]
            }
        }

        return progress

    def _get_feedback(self, feedback_id: str) -> Optional[ClientFeedback]:
        """Get feedback by ID"""
        for feedback in self.feedback_collections:
            if feedback.feedback_collection_id == feedback_id:
                return feedback
        return None


class ApprovalWorkflow:
    """Client approval workflow management"""

    def __init__(self):
        """Initialize Approval Workflow"""
        self.approvals: List[Dict[str, Any]] = []

    def request_approval(
        self,
        package_id: str,
        approvers: List[Dict[str, str]],
        deadline: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Request client approval

        Args:
            package_id: Package identifier
            approvers: List of approver details
            deadline: Optional approval deadline

        Returns:
            Approval request metadata
        """
        approval_id = f"APPR-{package_id}-{int(datetime.utcnow().timestamp())}"

        if deadline is None:
            # Default: 5 business days
            deadline = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"

        approval = {
            "approval_id": approval_id,
            "package_id": package_id,
            "approvers": approvers,
            "deadline": deadline,
            "status": "pending",
            "requested_at": datetime.utcnow().isoformat() + "Z",
            "approvals": [],
            "rejections": []
        }

        self.approvals.append(approval)

        # Send approval requests (in production, send emails)
        for approver in approvers:
            print(f"Approval request sent to {approver['name']} ({approver['email']})")

        return approval

    def submit_approval(
        self,
        approval_id: str,
        approver_email: str,
        decision: str,
        comments: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit approval decision

        Args:
            approval_id: Approval ID
            approver_email: Approver email
            decision: Decision (approve, reject)
            comments: Optional comments

        Returns:
            Updated approval record
        """
        approval = next((a for a in self.approvals if a["approval_id"] == approval_id), None)

        if not approval:
            raise ValueError(f"Approval not found: {approval_id}")

        decision_record = {
            "approver_email": approver_email,
            "decision": decision,
            "comments": comments,
            "decided_at": datetime.utcnow().isoformat() + "Z"
        }

        if decision == "approve":
            approval["approvals"].append(decision_record)
        else:
            approval["rejections"].append(decision_record)

        # Check if all approvers have responded
        total_responses = len(approval["approvals"]) + len(approval["rejections"])
        if total_responses >= len(approval["approvers"]):
            if len(approval["rejections"]) == 0:
                approval["status"] = "approved"
            else:
                approval["status"] = "rejected"

        return approval


if __name__ == "__main__":
    # Example usage
    print("=== Client Portal ===")
    portal = ClientPortal()

    # Create delivery package
    package = portal.create_delivery_package(
        project_id="PROJ-2025-001",
        client_id="CLIENT-ABC-CORP",
        content_items=["LESSON-001", "LESSON-002", "LESSON-003", "ASSESSMENT-001"],
        formats=["pdf", "scorm_2004", "html"]
    )
    print(f"Package created: {package.package_id}")
    print(f"Status: {package.status}")
    print(f"Content items: {len(package.content_items)}")

    # Generate download link
    download_url = portal.generate_download_link(package.package_id, expiration_hours=72)
    print(f"\nDownload URL: {download_url}")
    print(f"Expires: {package.download_expires_at}")

    # Get package manifest
    manifest = portal.get_package_manifest(package.package_id)
    print(f"\nPackage manifest: {len(manifest['files'])} files")

    # Validate download token
    token = download_url.split("/")[-1]
    valid, error = portal.validate_download_token(token, "192.168.1.100", "Mozilla/5.0")
    print(f"\nToken valid: {valid}")

    # Log download
    if valid:
        log = portal.log_download(token, "192.168.1.100", "Mozilla/5.0", 50000000)
        print(f"Download logged: {log.log_id}")

    # Feedback collection
    print("\n=== Feedback Manager ===")
    feedback_mgr = FeedbackManager()

    feedback = feedback_mgr.collect_feedback(
        package_id=package.package_id,
        reviewer_name="Jane Smith",
        reviewer_email="jane.smith@client.com",
        overall_rating=4,
        overall_comments="Great content overall. A few minor suggestions for improvement.",
        feedback_items=[
            {
                "content_id": "LESSON-001",
                "content_section": "Section 2.3",
                "priority": "high",
                "category": "content",
                "description": "Add more examples for this concept",
                "suggested_fix": "Include 2-3 real-world examples"
            },
            {
                "content_id": "LESSON-002",
                "content_section": "Activity 1",
                "priority": "medium",
                "category": "accessibility",
                "description": "Image needs alt text",
                "suggested_fix": "Add descriptive alt text for diagram"
            }
        ],
        approval_decision="revisions_required"
    )

    print(f"Feedback collected: {feedback.feedback_collection_id}")
    print(f"Rating: {feedback.overall_rating}/5")
    print(f"Feedback items: {len(feedback.feedback_items)}")
    print(f"Decision: {feedback.approval_decision}")

    # Generate feedback report
    report = feedback_mgr.generate_feedback_report(feedback.feedback_collection_id)
    print(f"\n{report[:500]}...")

    # Track resolution
    progress = feedback_mgr.track_feedback_resolution(feedback.feedback_collection_id)
    print(f"\nResolution progress: {progress['completion_percentage']}%")

    # Approval workflow
    print("\n=== Approval Workflow ===")
    approval_workflow = ApprovalWorkflow()

    approval_request = approval_workflow.request_approval(
        package_id=package.package_id,
        approvers=[
            {"name": "John Doe", "email": "john.doe@client.com"},
            {"name": "Jane Smith", "email": "jane.smith@client.com"}
        ]
    )
    print(f"Approval requested: {approval_request['approval_id']}")
    print(f"Deadline: {approval_request['deadline']}")
