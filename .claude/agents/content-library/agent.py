#!/usr/bin/env python3
"""
Content Library Agent

Manages content repository, search, metadata, versioning, and asset management.
Provides content discovery, organization, and reuse capabilities.

Usage:
    from agent import ContentLibraryAgent

    agent = ContentLibraryAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "search_content",
        "query": "genetics",
        "filters": {"subject": "biology", "grade": "9-12"}
    })
"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent


class ContentLibraryAgent(BaseAgent):
    """Manages content repository and asset library"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="content-library",
            agent_name="Content Library",
            project_id=project_id,
            description="Manages content repository, search, and asset management"
        )

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute content library logic

        Actions:
        - search_content: Search content library
        - index_content: Index new content
        - manage_metadata: Update content metadata
        - version_control: Manage content versions
        - manage_assets: Organize and optimize assets
        - track_usage: Track content usage analytics
        """
        action = parameters.get("action", "search_content")

        if action == "search_content":
            return await self._search_content(parameters, context)
        elif action == "index_content":
            return await self._index_content(parameters, context)
        elif action == "manage_metadata":
            return await self._manage_metadata(parameters, context)
        elif action == "version_control":
            return await self._version_control(parameters, context)
        elif action == "manage_assets":
            return await self._manage_assets(parameters, context)
        elif action == "track_usage":
            return await self._track_usage(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _search_content(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Search content library"""
        decisions = []
        artifacts = []

        query = parameters.get("query", "")
        filters = parameters.get("filters", {})
        limit = parameters.get("limit", 50)

        decisions.append(f"Searching for '{query}' with {len(filters)} filters")

        # Perform search
        search_results = self._perform_search(query, filters, limit)
        decisions.append(f"Found {len(search_results)} results")

        # Rank results by relevance
        ranked_results = self._rank_results(search_results, query)
        decisions.append(f"Ranked results by relevance")

        # Generate search report
        report = self._generate_search_report(
            query,
            filters,
            ranked_results
        )

        report_artifact = f"artifacts/{self.project_id}/search_results.md"
        self.create_artifact(
            "search_results",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create results JSON
        results_json = json.dumps({
            "query": query,
            "filters": filters,
            "total_results": len(search_results),
            "results": ranked_results[:20]  # Top 20
        }, indent=2)

        results_artifact = f"artifacts/{self.project_id}/search_results.json"
        self.create_artifact(
            "search_results_json",
            Path(results_artifact),
            results_json
        )
        artifacts.append(results_artifact)

        return {
            "output": {
                "total_results": len(search_results),
                "top_results": ranked_results[:10],
                "filters_applied": filters
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Searched content library for '{query}' and found "
                f"{len(search_results)} results"
            )
        }

    async def _index_content(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Index new content"""
        decisions = []
        artifacts = []

        content_path = parameters.get("content_path")
        content_type = parameters.get("content_type", "lesson")
        auto_metadata = parameters.get("auto_metadata", True)

        decisions.append(f"Indexing {content_type} content: {content_path}")

        # Extract metadata
        if auto_metadata:
            metadata = self._extract_metadata(content_path, content_type)
            decisions.append(f"Extracted {len(metadata)} metadata fields")
        else:
            metadata = parameters.get("metadata", {})

        # Generate content fingerprint
        fingerprint = self._generate_fingerprint(content_path)
        decisions.append(f"Generated content fingerprint: {fingerprint[:8]}...")

        # Index content
        index_result = self._add_to_index(
            content_path,
            content_type,
            metadata,
            fingerprint
        )
        decisions.append(f"Added to index: {index_result['index_id']}")

        # Create index record
        index_record = {
            "index_id": index_result["index_id"],
            "content_path": content_path,
            "content_type": content_type,
            "metadata": metadata,
            "fingerprint": fingerprint,
            "indexed_at": datetime.utcnow().isoformat() + "Z"
        }

        record_artifact = f"artifacts/{self.project_id}/index_record_{index_result['index_id']}.json"
        self.create_artifact(
            "index_record",
            Path(record_artifact),
            json.dumps(index_record, indent=2)
        )
        artifacts.append(record_artifact)

        return {
            "output": {
                "index_id": index_result["index_id"],
                "metadata_fields": len(metadata),
                "fingerprint": fingerprint
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Indexed {content_type} content with {len(metadata)} metadata fields"
            )
        }

    async def _manage_metadata(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Manage content metadata"""
        decisions = []
        artifacts = []

        content_id = parameters.get("content_id")
        metadata_updates = parameters.get("metadata_updates", {})
        validate_schema = parameters.get("validate_schema", True)

        decisions.append(f"Updating metadata for content: {content_id}")

        # Validate metadata schema
        if validate_schema:
            validation_result = self._validate_metadata_schema(metadata_updates)
            if not validation_result["valid"]:
                decisions.append(f"Metadata validation failed: {len(validation_result['errors'])} errors")
                return {
                    "output": {
                        "success": False,
                        "validation_errors": validation_result["errors"]
                    },
                    "decisions": decisions,
                    "artifacts": [],
                    "rationale": "Metadata validation failed"
                }
            decisions.append("Metadata schema validated")

        # Update metadata
        update_result = self._update_metadata(content_id, metadata_updates)
        decisions.append(f"Updated {len(metadata_updates)} metadata fields")

        # Create metadata record
        metadata_record = {
            "content_id": content_id,
            "updates": metadata_updates,
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }

        record_artifact = f"artifacts/{self.project_id}/metadata_update_{content_id}.json"
        self.create_artifact(
            "metadata_record",
            Path(record_artifact),
            json.dumps(metadata_record, indent=2)
        )
        artifacts.append(record_artifact)

        return {
            "output": {
                "content_id": content_id,
                "fields_updated": len(metadata_updates),
                "success": True
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Updated {len(metadata_updates)} metadata fields for content {content_id}"
        }

    async def _version_control(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Manage content versions"""
        decisions = []
        artifacts = []

        content_id = parameters.get("content_id")
        operation = parameters.get("operation", "create_version")  # create_version, list_versions, restore_version

        decisions.append(f"Version control operation: {operation} for {content_id}")

        if operation == "create_version":
            version_id = self._create_version(content_id)
            decisions.append(f"Created version: {version_id}")

            output = {
                "operation": "create_version",
                "version_id": version_id,
                "content_id": content_id
            }

        elif operation == "list_versions":
            versions = self._list_versions(content_id)
            decisions.append(f"Found {len(versions)} versions")

            output = {
                "operation": "list_versions",
                "content_id": content_id,
                "version_count": len(versions),
                "versions": versions
            }

        elif operation == "restore_version":
            version_id = parameters.get("version_id")
            restore_result = self._restore_version(content_id, version_id)
            decisions.append(f"Restored version: {version_id}")

            output = {
                "operation": "restore_version",
                "content_id": content_id,
                "version_id": version_id,
                "restored": True
            }

        else:
            output = {"error": f"Unknown operation: {operation}"}

        # Create version report
        report = self._generate_version_report(content_id, operation, output)

        report_artifact = f"artifacts/{self.project_id}/version_report_{content_id}.md"
        self.create_artifact(
            "version_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": output,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Executed {operation} for content {content_id}"
        }

    async def _manage_assets(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Manage and optimize assets"""
        decisions = []
        artifacts = []

        assets_path = parameters.get("assets_path")
        operation = parameters.get("operation", "audit")  # audit, optimize, organize

        decisions.append(f"Asset management operation: {operation}")

        if operation == "audit":
            audit_result = self._audit_assets(assets_path)
            decisions.append(f"Audited {audit_result['total_assets']} assets")

            output = audit_result

        elif operation == "optimize":
            optimization_result = self._optimize_assets(assets_path)
            decisions.append(f"Optimized {optimization_result['optimized_count']} assets")

            output = optimization_result

        elif operation == "organize":
            organization_result = self._organize_assets(assets_path)
            decisions.append(f"Organized {organization_result['moved_count']} assets")

            output = organization_result

        else:
            output = {"error": f"Unknown operation: {operation}"}

        # Create asset management report
        report = self._generate_asset_report(operation, output)

        report_artifact = f"artifacts/{self.project_id}/asset_management_report.md"
        self.create_artifact(
            "asset_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": output,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Executed {operation} on assets at {assets_path}"
        }

    async def _track_usage(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track content usage analytics"""
        decisions = []
        artifacts = []

        time_period = parameters.get("time_period", "30d")
        content_types = parameters.get("content_types", ["all"])

        decisions.append(f"Tracking usage for {time_period} period")

        # Collect usage data
        usage_data = self._collect_usage_data(time_period, content_types)
        decisions.append(f"Collected usage data for {usage_data['content_count']} items")

        # Analyze usage patterns
        patterns = self._analyze_usage_patterns(usage_data)
        decisions.append(f"Identified {len(patterns)} usage patterns")

        # Generate recommendations
        recommendations = self._generate_usage_recommendations(usage_data, patterns)
        decisions.append(f"Generated {len(recommendations)} recommendations")

        # Create usage report
        report = self._generate_usage_report(
            time_period,
            usage_data,
            patterns,
            recommendations
        )

        report_artifact = f"artifacts/{self.project_id}/content_usage_report.md"
        self.create_artifact(
            "usage_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create usage analytics JSON
        analytics_json = json.dumps({
            "time_period": time_period,
            "usage_data": usage_data,
            "patterns": patterns,
            "recommendations": recommendations
        }, indent=2)

        analytics_artifact = f"artifacts/{self.project_id}/usage_analytics.json"
        self.create_artifact(
            "usage_analytics",
            Path(analytics_artifact),
            analytics_json
        )
        artifacts.append(analytics_artifact)

        return {
            "output": {
                "time_period": time_period,
                "content_count": usage_data["content_count"],
                "patterns_identified": len(patterns),
                "recommendations": len(recommendations)
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Tracked usage for {time_period} with {len(patterns)} patterns "
                f"and {len(recommendations)} recommendations"
            )
        }

    # Helper methods

    def _perform_search(
        self,
        query: str,
        filters: Dict[str, Any],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Perform content search"""
        # Mock search results
        return [
            {
                "content_id": "CONTENT-001",
                "title": "Introduction to Genetics",
                "content_type": "lesson",
                "subject": "biology",
                "grade": "9-12",
                "relevance_score": 0.95
            },
            {
                "content_id": "CONTENT-002",
                "title": "DNA Structure and Function",
                "content_type": "lesson",
                "subject": "biology",
                "grade": "9-12",
                "relevance_score": 0.87
            }
        ]

    def _rank_results(
        self,
        results: List[Dict[str, Any]],
        query: str
    ) -> List[Dict[str, Any]]:
        """Rank search results by relevance"""
        return sorted(results, key=lambda x: x.get("relevance_score", 0), reverse=True)

    def _generate_search_report(
        self,
        query: str,
        filters: Dict[str, Any],
        results: List[Dict[str, Any]]
    ) -> str:
        """Generate search report"""
        filters_md = "\n".join([f"- **{k}**: {v}" for k, v in filters.items()]) if filters else "None"
        results_md = "\n".join([
            f"### {i+1}. {r['title']} (Score: {r['relevance_score']:.2f})\n"
            f"- **ID**: {r['content_id']}\n"
            f"- **Type**: {r['content_type']}\n"
            f"- **Subject**: {r.get('subject', 'N/A')}\n"
            for i, r in enumerate(results[:10])
        ])

        return f"""# Content Search Results

**Query**: {query}
**Total Results**: {len(results)}

## Filters Applied

{filters_md}

## Top Results

{results_md}

---
Generated by Content Library Agent
"""

    def _extract_metadata(
        self,
        content_path: str,
        content_type: str
    ) -> Dict[str, Any]:
        """Extract metadata from content"""
        return {
            "title": "Extracted Title",
            "subject": "biology",
            "grade": "9-12",
            "content_type": content_type,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

    def _generate_fingerprint(self, content_path: str) -> str:
        """Generate content fingerprint"""
        import hashlib
        return hashlib.md5(content_path.encode()).hexdigest()

    def _add_to_index(
        self,
        content_path: str,
        content_type: str,
        metadata: Dict[str, Any],
        fingerprint: str
    ) -> Dict[str, Any]:
        """Add content to index"""
        return {
            "index_id": f"IDX-{fingerprint[:8]}",
            "indexed_at": datetime.utcnow().isoformat() + "Z"
        }

    def _validate_metadata_schema(
        self,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate metadata against schema"""
        # Mock validation
        return {"valid": True, "errors": []}

    def _update_metadata(
        self,
        content_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update content metadata"""
        return {"success": True, "fields_updated": len(updates)}

    def _create_version(self, content_id: str) -> str:
        """Create new version"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"v{timestamp}"

    def _list_versions(self, content_id: str) -> List[Dict[str, Any]]:
        """List content versions"""
        return [
            {"version_id": "v20250106120000", "created_at": "2025-01-06T12:00:00Z"},
            {"version_id": "v20250106100000", "created_at": "2025-01-06T10:00:00Z"}
        ]

    def _restore_version(self, content_id: str, version_id: str) -> Dict[str, Any]:
        """Restore content version"""
        return {"restored": True, "version_id": version_id}

    def _generate_version_report(
        self,
        content_id: str,
        operation: str,
        output: Dict[str, Any]
    ) -> str:
        """Generate version control report"""
        return f"""# Version Control Report

**Content ID**: {content_id}
**Operation**: {operation}

## Results

{json.dumps(output, indent=2)}

---
Generated by Content Library Agent
"""

    def _audit_assets(self, assets_path: str) -> Dict[str, Any]:
        """Audit assets"""
        return {
            "total_assets": 150,
            "images": 80,
            "videos": 30,
            "audio": 20,
            "documents": 20,
            "total_size_mb": 2500
        }

    def _optimize_assets(self, assets_path: str) -> Dict[str, Any]:
        """Optimize assets"""
        return {
            "optimized_count": 80,
            "size_reduction_mb": 500,
            "size_reduction_percentage": 20.0
        }

    def _organize_assets(self, assets_path: str) -> Dict[str, Any]:
        """Organize assets"""
        return {
            "moved_count": 150,
            "folders_created": 10,
            "duplicates_removed": 5
        }

    def _generate_asset_report(
        self,
        operation: str,
        output: Dict[str, Any]
    ) -> str:
        """Generate asset management report"""
        output_md = "\n".join([f"- **{k.replace('_', ' ').title()}**: {v}" for k, v in output.items()])

        return f"""# Asset Management Report

**Operation**: {operation}

## Results

{output_md}

---
Generated by Content Library Agent
"""

    def _collect_usage_data(
        self,
        time_period: str,
        content_types: List[str]
    ) -> Dict[str, Any]:
        """Collect usage data"""
        return {
            "content_count": 250,
            "total_views": 15000,
            "unique_users": 500,
            "average_views_per_content": 60
        }

    def _analyze_usage_patterns(
        self,
        usage_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze usage patterns"""
        return [
            {"pattern": "Peak usage on weekdays", "confidence": 0.95},
            {"pattern": "Biology content most viewed", "confidence": 0.87}
        ]

    def _generate_usage_recommendations(
        self,
        usage_data: Dict[str, Any],
        patterns: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate usage recommendations"""
        return [
            "Create more biology content to meet demand",
            "Schedule content releases for weekday mornings"
        ]

    def _generate_usage_report(
        self,
        time_period: str,
        usage_data: Dict[str, Any],
        patterns: List[Dict[str, Any]],
        recommendations: List[str]
    ) -> str:
        """Generate usage report"""
        usage_md = "\n".join([f"- **{k.replace('_', ' ').title()}**: {v}" for k, v in usage_data.items()])
        patterns_md = "\n".join([f"- {p['pattern']} (Confidence: {p['confidence']:.0%})" for p in patterns])
        recommendations_md = "\n".join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])

        return f"""# Content Usage Report

**Time Period**: {time_period}

## Usage Statistics

{usage_md}

## Patterns Identified

{patterns_md}

## Recommendations

{recommendations_md}

---
Generated by Content Library Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_content_library():
    """Test the content library agent"""
    from state_manager import StateManager

    project_id = "PROJ-TEST-LIBRARY-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test Content Library Project",
        educational_level="9-12",
        standards=["NGSS"],
        context={"subject": "biology"}
    )

    agent = ContentLibraryAgent(project_id)

    print("=== Search Content ===")
    result = await agent.run({
        "action": "search_content",
        "query": "genetics",
        "filters": {"subject": "biology", "grade": "9-12"},
        "limit": 50
    })
    print(f"Status: {result['status']}")
    print(f"Total results: {result['output']['total_results']}")

    print("\n=== Index Content ===")
    result = await agent.run({
        "action": "index_content",
        "content_path": "content/lessons/genetics_intro.md",
        "content_type": "lesson",
        "auto_metadata": True
    })
    print(f"Status: {result['status']}")
    print(f"Index ID: {result['output']['index_id']}")

    print("\n=== Track Usage ===")
    result = await agent.run({
        "action": "track_usage",
        "time_period": "30d",
        "content_types": ["lesson", "assessment"]
    })
    print(f"Status: {result['status']}")
    print(f"Content count: {result['output']['content_count']}")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_content_library())
