#!/usr/bin/env python3
"""
Version Control & Revision Management for Professor

Extends StateManager with version control capabilities including:
- Semantic versioning (major.minor.patch)
- Branch management (state-specific versions)
- Revision tracking with diffs
- Changelog generation
- Merge capabilities

Addresses GAP-1: Version Control & Revision Management

Usage:
    from version_control import VersionManager

    vm = VersionManager(project_id="PROJ-2025-001")
    vm.create_version("1.0.0", "Initial release")
    vm.create_branch("texas-edition", from_version="1.0.0")
    vm.switch_branch("texas-edition")
    # Make changes...
    vm.create_version("1.1.0", "Texas-specific enhancements")
    changelog = vm.generate_changelog("1.0.0", "1.1.0")
"""

import json
import os
import hashlib
import difflib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import copy


class VersionType(Enum):
    """Version bump types"""
    MAJOR = "major"  # Breaking changes, incompatible API
    MINOR = "minor"  # New features, backward compatible
    PATCH = "patch"  # Bug fixes, backward compatible


@dataclass
class Version:
    """Version metadata"""
    version: str  # Semantic version (e.g., "1.2.3")
    branch: str
    timestamp: str
    author: str
    message: str
    state_snapshot: Dict[str, Any]
    parent_version: Optional[str]
    changes: List[str]


@dataclass
class Branch:
    """Branch metadata"""
    name: str
    created_from: str  # Parent version
    created_at: str
    description: str
    current_version: str
    merge_parent: Optional[str] = None


class VersionManager:
    """Manages versions and branches for curriculum projects"""

    def __init__(self, project_id: str, version_dir: Optional[Path] = None):
        """
        Initialize version manager

        Args:
            project_id: Unique project identifier
            version_dir: Directory for version files (default: ~/.claude/agents/versions)
        """
        self.project_id = project_id
        self.version_dir = version_dir or Path.home() / ".claude" / "agents" / "versions"
        self.project_dir = self.version_dir / project_id
        self.project_dir.mkdir(parents=True, exist_ok=True)

        self.versions_file = self.project_dir / "versions.json"
        self.branches_file = self.project_dir / "branches.json"
        self.current_file = self.project_dir / "current.json"

        self.versions: Dict[str, Version] = {}
        self.branches: Dict[str, Branch] = {}
        self.current_branch: str = "main"
        self.current_version: Optional[str] = None

        self._load()

    def _load(self) -> None:
        """Load versions and branches from disk"""
        if self.versions_file.exists():
            with open(self.versions_file, 'r') as f:
                data = json.load(f)
                self.versions = {k: Version(**v) for k, v in data.items()}

        if self.branches_file.exists():
            with open(self.branches_file, 'r') as f:
                data = json.load(f)
                self.branches = {k: Branch(**v) for k, v in data.items()}
        else:
            # Create default main branch
            self.branches["main"] = Branch(
                name="main",
                created_from="initial",
                created_at=datetime.utcnow().isoformat() + "Z",
                description="Main development branch",
                current_version="0.0.0"
            )

        if self.current_file.exists():
            with open(self.current_file, 'r') as f:
                data = json.load(f)
                self.current_branch = data.get("branch", "main")
                self.current_version = data.get("version")

    def _save(self) -> None:
        """Save versions and branches to disk"""
        with open(self.versions_file, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.versions.items()}, f, indent=2)

        with open(self.branches_file, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.branches.items()}, f, indent=2)

        with open(self.current_file, 'w') as f:
            json.dump({
                "branch": self.current_branch,
                "version": self.current_version
            }, f, indent=2)

    def create_version(
        self,
        version: str,
        message: str,
        state_snapshot: Dict[str, Any],
        author: str = "Professor Framework",
        changes: Optional[List[str]] = None
    ) -> Version:
        """
        Create a new version

        Args:
            version: Semantic version string (e.g., "1.2.3")
            message: Commit message describing changes
            state_snapshot: Complete project state at this version
            author: Author name
            changes: List of specific changes made

        Returns:
            Version object
        """
        if not self._validate_semver(version):
            raise ValueError(f"Invalid semantic version: {version}")

        version_key = f"{self.current_branch}@{version}"

        if version_key in self.versions:
            raise ValueError(f"Version {version} already exists on branch {self.current_branch}")

        version_obj = Version(
            version=version,
            branch=self.current_branch,
            timestamp=datetime.utcnow().isoformat() + "Z",
            author=author,
            message=message,
            state_snapshot=state_snapshot,
            parent_version=self.current_version,
            changes=changes or []
        )

        self.versions[version_key] = version_obj
        self.branches[self.current_branch].current_version = version
        self.current_version = version_key

        self._save()
        return version_obj

    def bump_version(
        self,
        bump_type: VersionType,
        message: str,
        state_snapshot: Dict[str, Any],
        author: str = "Professor Framework",
        changes: Optional[List[str]] = None
    ) -> Version:
        """
        Automatically bump version number

        Args:
            bump_type: Type of version bump (major, minor, patch)
            message: Commit message
            state_snapshot: Current project state
            author: Author name
            changes: List of changes

        Returns:
            New Version object
        """
        current_ver = self.branches[self.current_branch].current_version
        major, minor, patch = map(int, current_ver.split('.'))

        if bump_type == VersionType.MAJOR:
            new_version = f"{major + 1}.0.0"
        elif bump_type == VersionType.MINOR:
            new_version = f"{major}.{minor + 1}.0"
        else:  # PATCH
            new_version = f"{major}.{minor}.{patch + 1}"

        return self.create_version(new_version, message, state_snapshot, author, changes)

    def create_branch(
        self,
        branch_name: str,
        from_version: Optional[str] = None,
        description: str = ""
    ) -> Branch:
        """
        Create a new branch

        Args:
            branch_name: Name of new branch (e.g., "texas-edition", "california-edition")
            from_version: Version to branch from (defaults to current)
            description: Branch description

        Returns:
            Branch object
        """
        if branch_name in self.branches:
            raise ValueError(f"Branch {branch_name} already exists")

        base_version = from_version or self.current_version
        if not base_version:
            raise ValueError("No version to branch from")

        # Extract version number from version_key (branch@version)
        if '@' in base_version:
            _, version_num = base_version.split('@')
        else:
            version_num = base_version

        branch = Branch(
            name=branch_name,
            created_from=base_version,
            created_at=datetime.utcnow().isoformat() + "Z",
            description=description,
            current_version=version_num
        )

        self.branches[branch_name] = branch
        self._save()

        return branch

    def switch_branch(self, branch_name: str) -> None:
        """Switch to a different branch"""
        if branch_name not in self.branches:
            raise ValueError(f"Branch {branch_name} does not exist")

        self.current_branch = branch_name
        branch = self.branches[branch_name]
        self.current_version = f"{branch_name}@{branch.current_version}"
        self._save()

    def list_branches(self) -> List[Dict[str, Any]]:
        """List all branches"""
        return [
            {
                "name": branch.name,
                "current_version": branch.current_version,
                "created_from": branch.created_from,
                "created_at": branch.created_at,
                "description": branch.description,
                "is_current": branch.name == self.current_branch
            }
            for branch in self.branches.values()
        ]

    def list_versions(self, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all versions

        Args:
            branch: Filter by branch (optional)

        Returns:
            List of version summaries
        """
        branch = branch or self.current_branch

        versions = [
            {
                "version": v.version,
                "branch": v.branch,
                "timestamp": v.timestamp,
                "author": v.author,
                "message": v.message,
                "parent": v.parent_version,
                "changes_count": len(v.changes)
            }
            for k, v in self.versions.items()
            if v.branch == branch
        ]

        # Sort by timestamp
        return sorted(versions, key=lambda x: x["timestamp"])

    def get_version(self, version: str, branch: Optional[str] = None) -> Optional[Version]:
        """
        Get a specific version

        Args:
            version: Version number
            branch: Branch name (defaults to current)

        Returns:
            Version object or None
        """
        branch = branch or self.current_branch
        version_key = f"{branch}@{version}"
        return self.versions.get(version_key)

    def get_state_at_version(self, version: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Get project state at a specific version

        Args:
            version: Version number
            branch: Branch name (defaults to current)

        Returns:
            State snapshot
        """
        version_obj = self.get_version(version, branch)
        if not version_obj:
            raise ValueError(f"Version {version} not found on branch {branch or self.current_branch}")

        return version_obj.state_snapshot

    def diff_versions(
        self,
        version_a: str,
        version_b: str,
        branch: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare two versions

        Args:
            version_a: First version
            version_b: Second version
            branch: Branch name (defaults to current)

        Returns:
            Dictionary with differences
        """
        branch = branch or self.current_branch

        ver_a = self.get_version(version_a, branch)
        ver_b = self.get_version(version_b, branch)

        if not ver_a or not ver_b:
            raise ValueError("One or both versions not found")

        # Compare state snapshots
        state_a = json.dumps(ver_a.state_snapshot, indent=2, sort_keys=True)
        state_b = json.dumps(ver_b.state_snapshot, indent=2, sort_keys=True)

        diff = list(difflib.unified_diff(
            state_a.splitlines(keepends=True),
            state_b.splitlines(keepends=True),
            fromfile=f"version {version_a}",
            tofile=f"version {version_b}",
            lineterm=''
        ))

        return {
            "version_a": version_a,
            "version_b": version_b,
            "branch": branch,
            "diff": ''.join(diff),
            "changes_a": ver_a.changes,
            "changes_b": ver_b.changes
        }

    def generate_changelog(
        self,
        from_version: str,
        to_version: str,
        branch: Optional[str] = None,
        format: str = "markdown"
    ) -> str:
        """
        Generate changelog between two versions

        Args:
            from_version: Starting version
            to_version: Ending version
            branch: Branch name (defaults to current)
            format: Output format (markdown, json, text)

        Returns:
            Formatted changelog
        """
        branch = branch or self.current_branch

        # Get all versions between from_version and to_version
        versions = self.list_versions(branch)

        # Find versions in range
        in_range = False
        changelog_versions = []

        for v in versions:
            if v["version"] == from_version:
                in_range = True
                continue
            if in_range:
                changelog_versions.append(self.get_version(v["version"], branch))
            if v["version"] == to_version:
                break

        if format == "markdown":
            return self._format_changelog_markdown(changelog_versions, from_version, to_version)
        elif format == "json":
            return json.dumps([asdict(v) for v in changelog_versions], indent=2)
        else:  # text
            return self._format_changelog_text(changelog_versions, from_version, to_version)

    def _format_changelog_markdown(
        self,
        versions: List[Version],
        from_version: str,
        to_version: str
    ) -> str:
        """Format changelog as Markdown"""
        lines = [
            f"# Changelog: {from_version} → {to_version}",
            "",
            f"**Project**: {self.project_id}",
            f"**Branch**: {self.current_branch}",
            f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
            "",
            "---",
            ""
        ]

        for version in versions:
            lines.append(f"## Version {version.version}")
            lines.append(f"*Released {version.timestamp[:10]} by {version.author}*")
            lines.append("")
            lines.append(version.message)
            lines.append("")

            if version.changes:
                lines.append("**Changes:**")
                for change in version.changes:
                    lines.append(f"- {change}")
                lines.append("")

        return "\n".join(lines)

    def _format_changelog_text(
        self,
        versions: List[Version],
        from_version: str,
        to_version: str
    ) -> str:
        """Format changelog as plain text"""
        lines = [
            f"CHANGELOG: {from_version} -> {to_version}",
            f"Project: {self.project_id}",
            f"Branch: {self.current_branch}",
            "=" * 60,
            ""
        ]

        for version in versions:
            lines.append(f"Version {version.version} ({version.timestamp[:10]})")
            lines.append(f"Author: {version.author}")
            lines.append(f"Message: {version.message}")
            if version.changes:
                lines.append("Changes:")
                for change in version.changes:
                    lines.append(f"  * {change}")
            lines.append("")

        return "\n".join(lines)

    def merge_branch(
        self,
        source_branch: str,
        target_branch: str,
        strategy: str = "theirs",
        author: str = "Professor Framework"
    ) -> Version:
        """
        Merge source branch into target branch

        Args:
            source_branch: Branch to merge from
            target_branch: Branch to merge into
            strategy: Merge strategy ("ours", "theirs", "manual")
            author: Author of merge commit

        Returns:
            New merge version
        """
        if source_branch not in self.branches or target_branch not in self.branches:
            raise ValueError("Source or target branch does not exist")

        source_ver = self.branches[source_branch].current_version
        target_ver = self.branches[target_branch].current_version

        source_state = self.get_state_at_version(source_ver, source_branch)
        target_state = self.get_state_at_version(target_ver, target_branch)

        # Simple merge strategies
        if strategy == "theirs":
            merged_state = copy.deepcopy(source_state)
        elif strategy == "ours":
            merged_state = copy.deepcopy(target_state)
        else:
            raise ValueError("Manual merge strategy not yet implemented")

        # Switch to target branch and create merge commit
        self.switch_branch(target_branch)

        # Bump minor version for merge
        new_version = self.bump_version(
            VersionType.MINOR,
            f"Merge branch '{source_branch}' into '{target_branch}'",
            merged_state,
            author=author,
            changes=[f"Merged from {source_branch}@{source_ver}"]
        )

        return new_version

    def tag_version(self, version: str, tag: str, description: str = "") -> None:
        """
        Add a tag to a version (e.g., "production", "staging")

        Args:
            version: Version to tag
            tag: Tag name
            description: Tag description
        """
        version_obj = self.get_version(version)
        if not version_obj:
            raise ValueError(f"Version {version} not found")

        # Store tags in version metadata
        if not hasattr(version_obj, 'tags'):
            version_obj.tags = {}

        version_obj.tags[tag] = {
            "description": description,
            "tagged_at": datetime.utcnow().isoformat() + "Z"
        }

        self._save()

    def _validate_semver(self, version: str) -> bool:
        """Validate semantic version format"""
        parts = version.split('.')
        if len(parts) != 3:
            return False

        try:
            major, minor, patch = map(int, parts)
            return major >= 0 and minor >= 0 and patch >= 0
        except ValueError:
            return False

    def get_version_tree(self) -> Dict[str, Any]:
        """
        Get version tree showing branches and versions

        Returns:
            Tree structure
        """
        tree = {
            "branches": {},
            "current_branch": self.current_branch,
            "current_version": self.current_version
        }

        for branch_name, branch in self.branches.items():
            tree["branches"][branch_name] = {
                "description": branch.description,
                "current_version": branch.current_version,
                "created_from": branch.created_from,
                "versions": [
                    v["version"] for v in self.list_versions(branch_name)
                ]
            }

        return tree


if __name__ == "__main__":
    # Example usage
    vm = VersionManager("PROJ-2025-001")

    # Create initial version
    initial_state = {
        "name": "High School Biology",
        "phase": "design",
        "artifacts": {}
    }

    vm.create_version(
        "1.0.0",
        "Initial curriculum release",
        initial_state,
        changes=["Created learning objectives", "Developed lesson plans"]
    )

    # Create state-specific branch
    vm.create_branch(
        "texas-edition",
        from_version="1.0.0",
        description="Texas TEKS-aligned version"
    )

    # Switch to Texas branch
    vm.switch_branch("texas-edition")

    # Make Texas-specific changes
    texas_state = initial_state.copy()
    texas_state["standards"] = ["TX-TEKS"]

    vm.bump_version(
        VersionType.MINOR,
        "Added Texas TEKS alignment",
        texas_state,
        changes=["Aligned to TEKS standards", "Added Texas-specific examples"]
    )

    # Generate changelog
    changelog = vm.generate_changelog("1.0.0", "1.1.0", "texas-edition")
    print(changelog)

    # List all branches
    print("\nBranches:")
    for branch in vm.list_branches():
        print(f"  {branch['name']}: v{branch['current_version']} {'[current]' if branch['is_current'] else ''}")

    # Get version tree
    tree = vm.get_version_tree()
    print(f"\nVersion Tree: {json.dumps(tree, indent=2)}")
