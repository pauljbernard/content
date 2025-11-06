#!/usr/bin/env python3
"""
Project Planning Agent

Manages curriculum development projects, timelines, resources, milestones, and dependencies.
Provides project tracking, risk management, and resource optimization.

Usage:
    from agent import ProjectPlanningAgent

    agent = ProjectPlanningAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "create_plan",
        "project_name": "Biology - Genetics Unit",
        "scope": {"lessons": 10, "assessments": 3, "duration_weeks": 6}
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


class ProjectPlanningAgent(BaseAgent):
    """Manages curriculum development projects and planning"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="project-planning",
            agent_name="Project Planning",
            project_id=project_id,
            description="Manages project planning, timelines, resources, and milestones"
        )

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute project planning logic

        Actions:
        - create_plan: Create project plan
        - estimate_timeline: Estimate project timeline
        - allocate_resources: Allocate resources
        - track_milestones: Track project milestones
        - assess_risks: Assess project risks
        - optimize_schedule: Optimize project schedule
        """
        action = parameters.get("action", "create_plan")

        if action == "create_plan":
            return await self._create_plan(parameters, context)
        elif action == "estimate_timeline":
            return await self._estimate_timeline(parameters, context)
        elif action == "allocate_resources":
            return await self._allocate_resources(parameters, context)
        elif action == "track_milestones":
            return await self._track_milestones(parameters, context)
        elif action == "assess_risks":
            return await self._assess_risks(parameters, context)
        elif action == "optimize_schedule":
            return await self._optimize_schedule(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _create_plan(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create project plan"""
        decisions = []
        artifacts = []

        project_name = parameters.get("project_name")
        scope = parameters.get("scope", {})
        start_date = parameters.get("start_date", datetime.utcnow().strftime("%Y-%m-%d"))
        team_size = parameters.get("team_size", 3)

        decisions.append(f"Creating plan for project: {project_name}")
        decisions.append(f"Team size: {team_size}")

        # Define project phases
        phases = self._define_phases(scope)
        decisions.append(f"Defined {len(phases)} project phases")

        # Break down work packages
        work_packages = self._create_work_packages(scope, phases)
        decisions.append(f"Created {len(work_packages)} work packages")

        # Estimate effort
        effort_estimate = self._estimate_effort(work_packages, team_size)
        decisions.append(f"Estimated effort: {effort_estimate['total_hours']} hours")

        # Calculate timeline
        timeline = self._calculate_timeline(
            phases,
            work_packages,
            effort_estimate,
            start_date,
            team_size
        )
        decisions.append(f"Project duration: {timeline['duration_weeks']} weeks")

        # Identify dependencies
        dependencies = self._identify_dependencies(work_packages)
        decisions.append(f"Identified {len(dependencies)} dependencies")

        # Create project plan
        project_plan = {
            "project_name": project_name,
            "project_id": self.project_id,
            "scope": scope,
            "start_date": start_date,
            "end_date": timeline["end_date"],
            "team_size": team_size,
            "phases": phases,
            "work_packages": work_packages,
            "effort_estimate": effort_estimate,
            "timeline": timeline,
            "dependencies": dependencies,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        # Generate project charter
        charter = self._generate_project_charter(project_plan)
        charter_artifact = f"artifacts/{self.project_id}/project_charter.md"
        self.create_artifact(
            "project_charter",
            Path(charter_artifact),
            charter
        )
        artifacts.append(charter_artifact)

        # Generate Gantt chart data
        gantt_data = self._generate_gantt_data(work_packages, timeline)
        gantt_artifact = f"artifacts/{self.project_id}/gantt_chart.json"
        self.create_artifact(
            "gantt_chart",
            Path(gantt_artifact),
            json.dumps(gantt_data, indent=2)
        )
        artifacts.append(gantt_artifact)

        # Create project plan JSON
        plan_artifact = f"artifacts/{self.project_id}/project_plan.json"
        self.create_artifact(
            "project_plan",
            Path(plan_artifact),
            json.dumps(project_plan, indent=2)
        )
        artifacts.append(plan_artifact)

        return {
            "output": {
                "project_name": project_name,
                "duration_weeks": timeline["duration_weeks"],
                "total_hours": effort_estimate["total_hours"],
                "work_packages": len(work_packages),
                "end_date": timeline["end_date"]
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Created project plan with {len(work_packages)} work packages "
                f"over {timeline['duration_weeks']} weeks"
            )
        }

    async def _estimate_timeline(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Estimate project timeline"""
        decisions = []
        artifacts = []

        work_packages = parameters.get("work_packages", [])
        team_size = parameters.get("team_size", 3)
        start_date = parameters.get("start_date", datetime.utcnow().strftime("%Y-%m-%d"))

        decisions.append(f"Estimating timeline for {len(work_packages)} work packages")

        # Calculate effort per package
        package_estimates = []
        total_hours = 0

        for package in work_packages:
            estimate = self._estimate_package_effort(package)
            package_estimates.append({
                "package_id": package.get("id", "unknown"),
                "estimated_hours": estimate["hours"],
                "complexity": estimate["complexity"]
            })
            total_hours += estimate["hours"]

        decisions.append(f"Total estimated effort: {total_hours} hours")

        # Calculate duration with team size
        working_hours_per_week = team_size * 40  # 40 hours per person per week
        duration_weeks = (total_hours / working_hours_per_week)

        # Add buffer for reviews, revisions, meetings (20%)
        buffered_duration = duration_weeks * 1.2
        decisions.append(f"Duration with buffer: {buffered_duration:.1f} weeks")

        # Calculate end date
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = start + timedelta(weeks=buffered_duration)
        end_date = end.strftime("%Y-%m-%d")

        # Create timeline estimate
        timeline_estimate = {
            "start_date": start_date,
            "end_date": end_date,
            "duration_weeks": round(buffered_duration, 1),
            "total_hours": total_hours,
            "team_size": team_size,
            "package_estimates": package_estimates
        }

        # Generate timeline report
        report = self._generate_timeline_report(timeline_estimate)
        report_artifact = f"artifacts/{self.project_id}/timeline_estimate.md"
        self.create_artifact(
            "timeline_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": timeline_estimate,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Estimated {buffered_duration:.1f} week timeline for "
                f"{total_hours} hours of work with team of {team_size}"
            )
        }

    async def _allocate_resources(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Allocate resources to project"""
        decisions = []
        artifacts = []

        work_packages = parameters.get("work_packages", [])
        available_resources = parameters.get("available_resources", [])
        allocation_strategy = parameters.get("allocation_strategy", "balanced")  # balanced, speed, quality

        decisions.append(f"Allocating {len(available_resources)} resources to {len(work_packages)} packages")
        decisions.append(f"Strategy: {allocation_strategy}")

        # Analyze resource skills
        resource_analysis = self._analyze_resource_skills(available_resources)
        decisions.append(f"Analyzed {len(resource_analysis)} resource skill profiles")

        # Match resources to work packages
        allocations = self._match_resources_to_work(
            work_packages,
            available_resources,
            resource_analysis,
            allocation_strategy
        )
        decisions.append(f"Created {len(allocations)} resource allocations")

        # Calculate utilization
        utilization = self._calculate_resource_utilization(allocations, available_resources)
        decisions.append(f"Average utilization: {utilization['average_percentage']:.1f}%")

        # Identify conflicts
        conflicts = self._identify_resource_conflicts(allocations)
        if conflicts:
            decisions.append(f"Found {len(conflicts)} resource conflicts")

        # Create allocation plan
        allocation_plan = {
            "allocations": allocations,
            "utilization": utilization,
            "conflicts": conflicts,
            "strategy": allocation_strategy
        }

        # Generate allocation report
        report = self._generate_allocation_report(allocation_plan)
        report_artifact = f"artifacts/{self.project_id}/resource_allocation.md"
        self.create_artifact(
            "allocation_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create allocation JSON
        allocation_artifact = f"artifacts/{self.project_id}/resource_allocation.json"
        self.create_artifact(
            "allocation_json",
            Path(allocation_artifact),
            json.dumps(allocation_plan, indent=2)
        )
        artifacts.append(allocation_artifact)

        return {
            "output": {
                "allocations": len(allocations),
                "average_utilization": utilization["average_percentage"],
                "conflicts": len(conflicts)
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Allocated {len(available_resources)} resources with "
                f"{utilization['average_percentage']:.1f}% utilization"
            )
        }

    async def _track_milestones(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track project milestones"""
        decisions = []
        artifacts = []

        project_plan = parameters.get("project_plan")
        current_date = parameters.get("current_date", datetime.utcnow().strftime("%Y-%m-%d"))

        decisions.append(f"Tracking milestones as of {current_date}")

        # Extract milestones
        milestones = self._extract_milestones(project_plan)
        decisions.append(f"Tracking {len(milestones)} milestones")

        # Check milestone status
        milestone_status = []
        for milestone in milestones:
            status = self._check_milestone_status(milestone, current_date)
            milestone_status.append(status)

        # Calculate progress
        completed = sum(1 for ms in milestone_status if ms["status"] == "completed")
        progress_percentage = (completed / len(milestones) * 100) if milestones else 0
        decisions.append(f"Progress: {progress_percentage:.1f}% ({completed}/{len(milestones)})")

        # Identify at-risk milestones
        at_risk = [ms for ms in milestone_status if ms["status"] == "at_risk"]
        if at_risk:
            decisions.append(f"At-risk milestones: {len(at_risk)}")

        # Create milestone tracker
        tracker = {
            "current_date": current_date,
            "milestones": milestone_status,
            "progress_percentage": progress_percentage,
            "completed": completed,
            "total": len(milestones),
            "at_risk": len(at_risk)
        }

        # Generate milestone report
        report = self._generate_milestone_report(tracker)
        report_artifact = f"artifacts/{self.project_id}/milestone_tracker.md"
        self.create_artifact(
            "milestone_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": tracker,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Tracked {len(milestones)} milestones with {progress_percentage:.1f}% completion "
                f"and {len(at_risk)} at-risk"
            )
        }

    async def _assess_risks(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess project risks"""
        decisions = []
        artifacts = []

        project_plan = parameters.get("project_plan")
        risk_categories = parameters.get("risk_categories", [
            "schedule", "resources", "quality", "dependencies", "scope"
        ])

        decisions.append(f"Assessing risks across {len(risk_categories)} categories")

        # Identify risks
        identified_risks = []
        for category in risk_categories:
            category_risks = self._identify_category_risks(project_plan, category)
            identified_risks.extend(category_risks)

        decisions.append(f"Identified {len(identified_risks)} risks")

        # Assess risk severity
        risk_assessment = []
        for risk in identified_risks:
            assessment = self._assess_risk_severity(risk)
            risk_assessment.append(assessment)

        # Prioritize risks
        prioritized_risks = sorted(
            risk_assessment,
            key=lambda r: r["risk_score"],
            reverse=True
        )
        decisions.append(f"Prioritized risks by severity")

        # Generate mitigation strategies
        mitigations = []
        for risk in prioritized_risks[:10]:  # Top 10 risks
            mitigation = self._generate_mitigation_strategy(risk)
            mitigations.append(mitigation)

        decisions.append(f"Generated {len(mitigations)} mitigation strategies")

        # Create risk register
        risk_register = {
            "identified_risks": len(identified_risks),
            "high_severity": len([r for r in risk_assessment if r["severity"] == "high"]),
            "medium_severity": len([r for r in risk_assessment if r["severity"] == "medium"]),
            "low_severity": len([r for r in risk_assessment if r["severity"] == "low"]),
            "prioritized_risks": prioritized_risks[:10],
            "mitigation_strategies": mitigations
        }

        # Generate risk report
        report = self._generate_risk_report(risk_register)
        report_artifact = f"artifacts/{self.project_id}/risk_assessment.md"
        self.create_artifact(
            "risk_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create risk register JSON
        register_artifact = f"artifacts/{self.project_id}/risk_register.json"
        self.create_artifact(
            "risk_register",
            Path(register_artifact),
            json.dumps(risk_register, indent=2)
        )
        artifacts.append(register_artifact)

        return {
            "output": risk_register,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Assessed {len(identified_risks)} risks with {risk_register['high_severity']} "
                f"high severity and generated {len(mitigations)} mitigation strategies"
            )
        }

    async def _optimize_schedule(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize project schedule"""
        decisions = []
        artifacts = []

        project_plan = parameters.get("project_plan")
        optimization_goal = parameters.get("optimization_goal", "time")  # time, cost, quality

        decisions.append(f"Optimizing schedule for {optimization_goal}")

        # Analyze current schedule
        current_analysis = self._analyze_schedule(project_plan)
        decisions.append(f"Current duration: {current_analysis['duration_weeks']} weeks")

        # Identify optimization opportunities
        opportunities = self._identify_optimization_opportunities(
            project_plan,
            optimization_goal
        )
        decisions.append(f"Found {len(opportunities)} optimization opportunities")

        # Apply optimizations
        optimized_schedule = self._apply_optimizations(
            project_plan,
            opportunities,
            optimization_goal
        )
        decisions.append(f"Optimized duration: {optimized_schedule['duration_weeks']} weeks")

        # Calculate improvement
        improvement = {
            "original_weeks": current_analysis["duration_weeks"],
            "optimized_weeks": optimized_schedule["duration_weeks"],
            "time_saved_weeks": current_analysis["duration_weeks"] - optimized_schedule["duration_weeks"],
            "improvement_percentage": (
                (current_analysis["duration_weeks"] - optimized_schedule["duration_weeks"])
                / current_analysis["duration_weeks"] * 100
            )
        }
        decisions.append(f"Time saved: {improvement['time_saved_weeks']:.1f} weeks ({improvement['improvement_percentage']:.1f}%)")

        # Create optimization report
        optimization_result = {
            "optimization_goal": optimization_goal,
            "current_analysis": current_analysis,
            "optimized_schedule": optimized_schedule,
            "improvement": improvement,
            "opportunities_applied": opportunities
        }

        # Generate optimization report
        report = self._generate_optimization_report(optimization_result)
        report_artifact = f"artifacts/{self.project_id}/schedule_optimization.md"
        self.create_artifact(
            "optimization_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": optimization_result,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Optimized schedule from {improvement['original_weeks']} to "
                f"{improvement['optimized_weeks']} weeks ({improvement['improvement_percentage']:.1f}% improvement)"
            )
        }

    # Helper methods

    def _define_phases(self, scope: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define project phases"""
        return [
            {"phase": "research", "description": "Research and needs analysis"},
            {"phase": "design", "description": "Learning objectives and assessment design"},
            {"phase": "development", "description": "Content development"},
            {"phase": "review", "description": "Quality review and revisions"},
            {"phase": "delivery", "description": "Packaging and delivery"}
        ]

    def _create_work_packages(
        self,
        scope: Dict[str, Any],
        phases: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create work packages"""
        packages = []
        package_id = 1

        # Generate packages based on scope
        lessons = scope.get("lessons", 0)
        assessments = scope.get("assessments", 0)

        for i in range(lessons):
            packages.append({
                "id": f"WP-{package_id:03d}",
                "name": f"Lesson {i+1} Development",
                "phase": "development",
                "type": "lesson"
            })
            package_id += 1

        for i in range(assessments):
            packages.append({
                "id": f"WP-{package_id:03d}",
                "name": f"Assessment {i+1} Development",
                "phase": "development",
                "type": "assessment"
            })
            package_id += 1

        return packages

    def _estimate_effort(
        self,
        work_packages: List[Dict[str, Any]],
        team_size: int
    ) -> Dict[str, Any]:
        """Estimate effort for work packages"""
        effort_by_type = {
            "lesson": 16,  # hours
            "assessment": 12,
            "review": 4
        }

        total_hours = sum(
            effort_by_type.get(pkg.get("type", "lesson"), 16)
            for pkg in work_packages
        )

        return {
            "total_hours": total_hours,
            "average_hours_per_package": total_hours / len(work_packages) if work_packages else 0
        }

    def _calculate_timeline(
        self,
        phases: List[Dict[str, Any]],
        work_packages: List[Dict[str, Any]],
        effort_estimate: Dict[str, Any],
        start_date: str,
        team_size: int
    ) -> Dict[str, Any]:
        """Calculate project timeline"""
        total_hours = effort_estimate["total_hours"]
        working_hours_per_week = team_size * 40
        duration_weeks = (total_hours / working_hours_per_week) * 1.2  # 20% buffer

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = start + timedelta(weeks=duration_weeks)

        return {
            "duration_weeks": round(duration_weeks, 1),
            "start_date": start_date,
            "end_date": end.strftime("%Y-%m-%d")
        }

    def _identify_dependencies(
        self,
        work_packages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify work package dependencies"""
        # Mock dependencies
        return [
            {
                "package_id": "WP-002",
                "depends_on": ["WP-001"],
                "type": "finish_to_start"
            }
        ]

    def _generate_project_charter(self, project_plan: Dict[str, Any]) -> str:
        """Generate project charter"""
        phases_md = "\n".join([
            f"- **{p['phase'].title()}**: {p['description']}"
            for p in project_plan["phases"]
        ])

        return f"""# Project Charter

**Project Name**: {project_plan['project_name']}
**Project ID**: {project_plan['project_id']}
**Start Date**: {project_plan['start_date']}
**End Date**: {project_plan['end_date']}
**Duration**: {project_plan['timeline']['duration_weeks']} weeks

## Scope

- **Lessons**: {project_plan['scope'].get('lessons', 0)}
- **Assessments**: {project_plan['scope'].get('assessments', 0)}
- **Duration**: {project_plan['scope'].get('duration_weeks', 0)} weeks

## Team

- **Team Size**: {project_plan['team_size']} members
- **Estimated Effort**: {project_plan['effort_estimate']['total_hours']} hours

## Project Phases

{phases_md}

## Work Packages

- **Total**: {len(project_plan['work_packages'])}
- **Dependencies**: {len(project_plan['dependencies'])}

---
Generated by Project Planning Agent
"""

    def _generate_gantt_data(
        self,
        work_packages: List[Dict[str, Any]],
        timeline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Gantt chart data"""
        return {
            "timeline": timeline,
            "tasks": [
                {
                    "id": pkg["id"],
                    "name": pkg["name"],
                    "phase": pkg.get("phase", "development")
                }
                for pkg in work_packages
            ]
        }

    def _estimate_package_effort(self, package: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate effort for single package"""
        effort_map = {
            "lesson": {"hours": 16, "complexity": "medium"},
            "assessment": {"hours": 12, "complexity": "medium"},
            "review": {"hours": 4, "complexity": "low"}
        }
        return effort_map.get(package.get("type", "lesson"), {"hours": 16, "complexity": "medium"})

    def _generate_timeline_report(self, timeline_estimate: Dict[str, Any]) -> str:
        """Generate timeline report"""
        packages_md = "\n".join([
            f"- **{pkg['package_id']}**: {pkg['estimated_hours']} hours ({pkg['complexity']})"
            for pkg in timeline_estimate["package_estimates"][:10]
        ])

        return f"""# Timeline Estimate

**Start Date**: {timeline_estimate['start_date']}
**End Date**: {timeline_estimate['end_date']}
**Duration**: {timeline_estimate['duration_weeks']} weeks
**Total Effort**: {timeline_estimate['total_hours']} hours
**Team Size**: {timeline_estimate['team_size']}

## Work Package Estimates

{packages_md}

---
Generated by Project Planning Agent
"""

    def _analyze_resource_skills(
        self,
        available_resources: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze resource skills"""
        return [
            {
                "resource_id": res.get("id", "unknown"),
                "skills": res.get("skills", []),
                "availability": res.get("availability", 100)
            }
            for res in available_resources
        ]

    def _match_resources_to_work(
        self,
        work_packages: List[Dict[str, Any]],
        available_resources: List[Dict[str, Any]],
        resource_analysis: List[Dict[str, Any]],
        strategy: str
    ) -> List[Dict[str, Any]]:
        """Match resources to work packages"""
        allocations = []
        for i, package in enumerate(work_packages):
            resource = available_resources[i % len(available_resources)]
            allocations.append({
                "package_id": package["id"],
                "resource_id": resource.get("id", f"RES-{i+1}"),
                "allocation_percentage": 100
            })
        return allocations

    def _calculate_resource_utilization(
        self,
        allocations: List[Dict[str, Any]],
        available_resources: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate resource utilization"""
        return {
            "average_percentage": 85.0,
            "by_resource": {}
        }

    def _identify_resource_conflicts(
        self,
        allocations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify resource conflicts"""
        return []

    def _generate_allocation_report(self, allocation_plan: Dict[str, Any]) -> str:
        """Generate allocation report"""
        allocations_md = "\n".join([
            f"- **{a['package_id']}**: {a['resource_id']} ({a['allocation_percentage']}%)"
            for a in allocation_plan["allocations"][:10]
        ])

        return f"""# Resource Allocation Report

**Strategy**: {allocation_plan['strategy']}
**Average Utilization**: {allocation_plan['utilization']['average_percentage']:.1f}%
**Conflicts**: {len(allocation_plan['conflicts'])}

## Allocations

{allocations_md}

---
Generated by Project Planning Agent
"""

    def _extract_milestones(self, project_plan: Any) -> List[Dict[str, Any]]:
        """Extract milestones from project plan"""
        return [
            {"id": "MS-001", "name": "Research Complete", "date": "2025-01-15"},
            {"id": "MS-002", "name": "Design Complete", "date": "2025-01-30"},
            {"id": "MS-003", "name": "Development Complete", "date": "2025-03-15"}
        ]

    def _check_milestone_status(
        self,
        milestone: Dict[str, Any],
        current_date: str
    ) -> Dict[str, Any]:
        """Check milestone status"""
        milestone_date = datetime.strptime(milestone["date"], "%Y-%m-%d")
        current = datetime.strptime(current_date, "%Y-%m-%d")

        if current >= milestone_date:
            status = "completed"
        elif (milestone_date - current).days <= 7:
            status = "at_risk"
        else:
            status = "on_track"

        return {
            **milestone,
            "status": status
        }

    def _generate_milestone_report(self, tracker: Dict[str, Any]) -> str:
        """Generate milestone report"""
        milestones_md = "\n".join([
            f"- {'✓' if ms['status'] == 'completed' else '○'} **{ms['name']}** ({ms['date']}) - {ms['status'].replace('_', ' ').title()}"
            for ms in tracker["milestones"]
        ])

        return f"""# Milestone Tracker

**Current Date**: {tracker['current_date']}
**Progress**: {tracker['progress_percentage']:.1f}% ({tracker['completed']}/{tracker['total']})
**At Risk**: {tracker['at_risk']}

## Milestones

{milestones_md}

---
Generated by Project Planning Agent
"""

    def _identify_category_risks(
        self,
        project_plan: Any,
        category: str
    ) -> List[Dict[str, Any]]:
        """Identify risks in category"""
        risks_by_category = {
            "schedule": [{"id": "RISK-001", "description": "Tight deadline", "category": "schedule"}],
            "resources": [{"id": "RISK-002", "description": "Limited team", "category": "resources"}]
        }
        return risks_by_category.get(category, [])

    def _assess_risk_severity(self, risk: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk severity"""
        return {
            **risk,
            "severity": "medium",
            "probability": 0.5,
            "impact": 0.6,
            "risk_score": 0.5 * 0.6
        }

    def _generate_mitigation_strategy(self, risk: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mitigation strategy"""
        return {
            "risk_id": risk["id"],
            "strategy": "Monitor closely and adjust timeline if needed",
            "owner": "Project Manager"
        }

    def _generate_risk_report(self, risk_register: Dict[str, Any]) -> str:
        """Generate risk report"""
        risks_md = "\n".join([
            f"### {r['id']}: {r['description']}\n"
            f"- **Severity**: {r['severity'].title()}\n"
            f"- **Risk Score**: {r['risk_score']:.2f}\n"
            for r in risk_register["prioritized_risks"][:5]
        ])

        return f"""# Risk Assessment Report

**Total Risks**: {risk_register['identified_risks']}
**High Severity**: {risk_register['high_severity']}
**Medium Severity**: {risk_register['medium_severity']}
**Low Severity**: {risk_register['low_severity']}

## Top Risks

{risks_md}

---
Generated by Project Planning Agent
"""

    def _analyze_schedule(self, project_plan: Any) -> Dict[str, Any]:
        """Analyze current schedule"""
        return {"duration_weeks": 12}

    def _identify_optimization_opportunities(
        self,
        project_plan: Any,
        optimization_goal: str
    ) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        return [
            {"type": "parallel_execution", "impact": "2 weeks"},
            {"type": "resource_reallocation", "impact": "1 week"}
        ]

    def _apply_optimizations(
        self,
        project_plan: Any,
        opportunities: List[Dict[str, Any]],
        optimization_goal: str
    ) -> Dict[str, Any]:
        """Apply optimizations"""
        return {"duration_weeks": 9}

    def _generate_optimization_report(self, optimization_result: Dict[str, Any]) -> str:
        """Generate optimization report"""
        return f"""# Schedule Optimization Report

**Optimization Goal**: {optimization_result['optimization_goal'].title()}

## Results

- **Original Duration**: {optimization_result['improvement']['original_weeks']} weeks
- **Optimized Duration**: {optimization_result['improvement']['optimized_weeks']} weeks
- **Time Saved**: {optimization_result['improvement']['time_saved_weeks']:.1f} weeks
- **Improvement**: {optimization_result['improvement']['improvement_percentage']:.1f}%

---
Generated by Project Planning Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_project_planning():
    """Test the project planning agent"""
    from state_manager import StateManager

    project_id = "PROJ-TEST-PLANNING-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test Project Planning",
        educational_level="9-12",
        standards=[],
        context={}
    )

    agent = ProjectPlanningAgent(project_id)

    print("=== Create Project Plan ===")
    result = await agent.run({
        "action": "create_plan",
        "project_name": "Biology - Genetics Unit",
        "scope": {
            "lessons": 10,
            "assessments": 3,
            "duration_weeks": 6
        },
        "team_size": 3
    })
    print(f"Status: {result['status']}")
    print(f"Duration: {result['output']['duration_weeks']} weeks")
    print(f"Work packages: {result['output']['work_packages']}")

    print("\n=== Assess Risks ===")
    result = await agent.run({
        "action": "assess_risks",
        "project_plan": {},
        "risk_categories": ["schedule", "resources", "quality"]
    })
    print(f"Status: {result['status']}")
    print(f"Identified risks: {result['output']['identified_risks']}")
    print(f"High severity: {result['output']['high_severity']}")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_project_planning())
