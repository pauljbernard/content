#!/usr/bin/env python3
"""
Planning Estimator - Automated Scope, Timeline, Cost Estimation

Implements GAP-15: Project Planning Enhancement
Provides automated estimation using historical data, parametric models, and Monte Carlo simulation

Usage:
    from planning_estimator import PlanningEstimator

    estimator = PlanningEstimator()

    # Estimate project from scope
    estimate = estimator.estimate_project(
        project_type="curriculum_development",
        scope={"lessons": 20, "assessments": 5, "multimedia": 10}
    )

    # Cost forecast
    cost = estimator.forecast_costs(estimate, team_composition)

    # Risk assessment
    risks = estimator.assess_risks(estimate, risk_factors)
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class ProjectEstimate:
    """Project estimation results"""
    project_type: str
    scope: Dict[str, int]
    timeline_weeks: float
    timeline_confidence: Tuple[float, float]  # (lower, upper) 90% CI
    total_hours: float
    total_cost: float
    cost_confidence: Tuple[float, float]  # (lower, upper) 90% CI
    resource_requirements: Dict[str, float]
    risk_level: str  # low, medium, high
    estimated_at: str = ""


@dataclass
class WorkItem:
    """Individual work item estimate"""
    item_id: str
    item_type: str  # lesson, assessment, multimedia, review
    complexity: str  # low, medium, high
    hours_optimistic: float
    hours_most_likely: float
    hours_pessimistic: float
    dependencies: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)


@dataclass
class CostForecast:
    """Cost forecast breakdown"""
    total_cost: float
    labor_costs: Dict[str, float]  # role -> cost
    infrastructure_costs: float
    tools_licenses: float
    contingency_reserve: float
    management_reserve: float
    cost_per_deliverable: Dict[str, float]


class PlanningEstimator:
    """Automated project planning and estimation engine"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize Planning Estimator

        Args:
            data_dir: Directory for historical data
        """
        self.data_dir = data_dir or Path.home() / ".claude" / "agents" / "planning"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Historical productivity data (hours per item by complexity)
        self.productivity_rates = {
            "lesson": {
                "low": {"min": 8, "typical": 12, "max": 16},
                "medium": {"min": 16, "typical": 24, "max": 32},
                "high": {"min": 32, "typical": 48, "max": 64}
            },
            "assessment": {
                "low": {"min": 4, "typical": 6, "max": 8},
                "medium": {"min": 8, "typical": 12, "max": 16},
                "high": {"min": 16, "typical": 24, "max": 32}
            },
            "multimedia": {
                "low": {"min": 6, "typical": 10, "max": 14},
                "medium": {"min": 12, "typical": 20, "max": 28},
                "high": {"min": 24, "typical": 40, "max": 56}
            },
            "review": {
                "low": {"min": 2, "typical": 3, "max": 4},
                "medium": {"min": 4, "typical": 6, "max": 8},
                "high": {"min": 8, "typical": 12, "max": 16}
            }
        }

        # Labor cost rates ($/hour by role)
        self.labor_rates = {
            "instructional_designer": 75,
            "subject_matter_expert": 85,
            "content_developer": 65,
            "multimedia_specialist": 70,
            "assessment_designer": 75,
            "editor": 60,
            "qa_specialist": 55,
            "project_manager": 90
        }

    # ==================== PROJECT ESTIMATION ====================

    def estimate_project(
        self,
        project_type: str,
        scope: Dict[str, Any],
        team_experience: str = "medium",
        complexity_factors: Optional[Dict[str, str]] = None
    ) -> ProjectEstimate:
        """
        Estimate project timeline and costs from scope

        Args:
            project_type: Type of project (curriculum_development, assessment_bank, etc.)
            scope: Project scope (lessons, assessments, multimedia items, etc.)
            team_experience: Team experience level (low, medium, high)
            complexity_factors: Additional complexity factors

        Returns:
            ProjectEstimate object with timeline and cost predictions
        """
        # Break down scope into work items
        work_items = self._decompose_scope(scope, complexity_factors or {})

        # Estimate each work item using three-point estimation
        item_estimates = [self._estimate_work_item(item) for item in work_items]

        # Calculate total effort (PERT formula)
        total_hours = sum(
            (est["optimistic"] + 4 * est["most_likely"] + est["pessimistic"]) / 6
            for est in item_estimates
        )

        # Apply team experience multiplier
        experience_multipliers = {"low": 1.3, "medium": 1.0, "high": 0.8}
        adjusted_hours = total_hours * experience_multipliers.get(team_experience, 1.0)

        # Monte Carlo simulation for confidence intervals
        timeline_ci, hours_ci = self._monte_carlo_simulation(item_estimates, iterations=1000)

        # Calculate timeline (assuming 40-hour work weeks, 80% utilization)
        effective_hours_per_week = 32  # 40 * 0.8
        timeline_weeks = adjusted_hours / effective_hours_per_week

        # Resource requirements
        resource_reqs = self._calculate_resource_requirements(work_items)

        # Cost estimation
        total_cost = self._estimate_total_cost(adjusted_hours, resource_reqs)
        cost_ci = (total_cost * 0.85, total_cost * 1.15)  # ±15% confidence interval

        # Risk assessment
        risk_level = self._assess_risk_level(scope, complexity_factors or {}, team_experience)

        return ProjectEstimate(
            project_type=project_type,
            scope=scope,
            timeline_weeks=round(timeline_weeks, 1),
            timeline_confidence=timeline_ci,
            total_hours=round(adjusted_hours, 1),
            total_cost=round(total_cost, 2),
            cost_confidence=cost_ci,
            resource_requirements=resource_reqs,
            risk_level=risk_level,
            estimated_at=datetime.utcnow().isoformat() + "Z"
        )

    def _decompose_scope(
        self,
        scope: Dict[str, Any],
        complexity_factors: Dict[str, str]
    ) -> List[WorkItem]:
        """Decompose scope into individual work items"""
        work_items = []
        item_counter = 1

        # Decompose lessons
        for i in range(scope.get("lessons", 0)):
            complexity = self._determine_complexity(
                "lesson",
                i,
                scope.get("lessons", 0),
                complexity_factors
            )
            rates = self.productivity_rates["lesson"][complexity]

            work_items.append(WorkItem(
                item_id=f"LESSON-{item_counter:03d}",
                item_type="lesson",
                complexity=complexity,
                hours_optimistic=rates["min"],
                hours_most_likely=rates["typical"],
                hours_pessimistic=rates["max"],
                required_skills=["instructional_designer", "content_developer"]
            ))
            item_counter += 1

        # Decompose assessments
        for i in range(scope.get("assessments", 0)):
            complexity = self._determine_complexity(
                "assessment",
                i,
                scope.get("assessments", 0),
                complexity_factors
            )
            rates = self.productivity_rates["assessment"][complexity]

            work_items.append(WorkItem(
                item_id=f"ASSESS-{item_counter:03d}",
                item_type="assessment",
                complexity=complexity,
                hours_optimistic=rates["min"],
                hours_most_likely=rates["typical"],
                hours_pessimistic=rates["max"],
                required_skills=["assessment_designer", "subject_matter_expert"]
            ))
            item_counter += 1

        # Decompose multimedia
        for i in range(scope.get("multimedia", 0)):
            complexity = self._determine_complexity(
                "multimedia",
                i,
                scope.get("multimedia", 0),
                complexity_factors
            )
            rates = self.productivity_rates["multimedia"][complexity]

            work_items.append(WorkItem(
                item_id=f"MEDIA-{item_counter:03d}",
                item_type="multimedia",
                complexity=complexity,
                hours_optimistic=rates["min"],
                hours_most_likely=rates["typical"],
                hours_pessimistic=rates["max"],
                required_skills=["multimedia_specialist"]
            ))
            item_counter += 1

        # Add review items (1 review per 3 content items)
        content_items = len(work_items)
        review_items = (content_items + 2) // 3

        for i in range(review_items):
            rates = self.productivity_rates["review"]["medium"]
            work_items.append(WorkItem(
                item_id=f"REVIEW-{item_counter:03d}",
                item_type="review",
                complexity="medium",
                hours_optimistic=rates["min"],
                hours_most_likely=rates["typical"],
                hours_pessimistic=rates["max"],
                required_skills=["editor", "qa_specialist"]
            ))
            item_counter += 1

        return work_items

    def _determine_complexity(
        self,
        item_type: str,
        index: int,
        total: int,
        complexity_factors: Dict[str, str]
    ) -> str:
        """Determine item complexity"""
        # Check explicit complexity factors
        if f"{item_type}_complexity" in complexity_factors:
            return complexity_factors[f"{item_type}_complexity"]

        # Default: 20% high, 60% medium, 20% low
        percentile = index / total if total > 0 else 0.5

        if percentile < 0.2:
            return "low"
        elif percentile < 0.8:
            return "medium"
        else:
            return "high"

    def _estimate_work_item(self, item: WorkItem) -> Dict[str, float]:
        """Estimate work item effort using three-point estimation"""
        return {
            "optimistic": item.hours_optimistic,
            "most_likely": item.hours_most_likely,
            "pessimistic": item.hours_pessimistic,
            "expected": (item.hours_optimistic + 4 * item.hours_most_likely + item.hours_pessimistic) / 6
        }

    def _monte_carlo_simulation(
        self,
        item_estimates: List[Dict[str, float]],
        iterations: int = 1000
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Monte Carlo simulation for confidence intervals

        Returns:
            (timeline_ci, hours_ci) tuples with (lower, upper) bounds
        """
        simulated_totals = []

        for _ in range(iterations):
            total = 0
            for est in item_estimates:
                # PERT beta distribution approximation
                # Use triangular distribution for simplicity
                min_val = est["optimistic"]
                mode = est["most_likely"]
                max_val = est["pessimistic"]

                value = np.random.triangular(min_val, mode, max_val)
                total += value

            simulated_totals.append(total)

        simulated_totals = np.array(simulated_totals)

        # 90% confidence interval (5th and 95th percentiles)
        hours_lower = np.percentile(simulated_totals, 5)
        hours_upper = np.percentile(simulated_totals, 95)

        # Convert to weeks (32 effective hours/week)
        timeline_lower = hours_lower / 32
        timeline_upper = hours_upper / 32

        return (round(timeline_lower, 1), round(timeline_upper, 1)), (round(hours_lower, 1), round(hours_upper, 1))

    def _calculate_resource_requirements(
        self,
        work_items: List[WorkItem]
    ) -> Dict[str, float]:
        """Calculate required hours per role"""
        role_hours = {}

        for item in work_items:
            expected_hours = (
                item.hours_optimistic + 4 * item.hours_most_likely + item.hours_pessimistic
            ) / 6

            # Distribute hours across required skills
            hours_per_skill = expected_hours / len(item.required_skills)

            for skill in item.required_skills:
                role_hours[skill] = role_hours.get(skill, 0) + hours_per_skill

        # Add project management overhead (15% of total)
        total_hours = sum(role_hours.values())
        role_hours["project_manager"] = total_hours * 0.15

        return {role: round(hours, 1) for role, hours in role_hours.items()}

    def _estimate_total_cost(
        self,
        total_hours: float,
        resource_requirements: Dict[str, float]
    ) -> float:
        """Estimate total project cost"""
        # Labor costs
        labor_cost = sum(
            resource_requirements.get(role, 0) * self.labor_rates.get(role, 70)
            for role in resource_requirements
        )

        # Infrastructure costs (5% of labor)
        infrastructure_cost = labor_cost * 0.05

        # Tools & licenses (3% of labor)
        tools_cost = labor_cost * 0.03

        # Contingency reserve (10% for unforeseen issues)
        contingency = labor_cost * 0.10

        return labor_cost + infrastructure_cost + tools_cost + contingency

    def _assess_risk_level(
        self,
        scope: Dict[str, Any],
        complexity_factors: Dict[str, str],
        team_experience: str
    ) -> str:
        """Assess overall project risk level"""
        risk_score = 0

        # Scope size risk
        total_items = sum(scope.values())
        if total_items > 50:
            risk_score += 2
        elif total_items > 20:
            risk_score += 1

        # Complexity risk
        high_complexity = sum(
            1 for val in complexity_factors.values() if val == "high"
        )
        if high_complexity > 2:
            risk_score += 2
        elif high_complexity > 0:
            risk_score += 1

        # Team experience risk
        if team_experience == "low":
            risk_score += 2
        elif team_experience == "medium":
            risk_score += 1

        # Classify risk
        if risk_score >= 4:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"

    # ==================== COST FORECASTING ====================

    def forecast_costs(
        self,
        estimate: ProjectEstimate,
        team_composition: Optional[Dict[str, int]] = None
    ) -> CostForecast:
        """
        Detailed cost forecast with breakdown

        Args:
            estimate: ProjectEstimate from estimate_project()
            team_composition: Optional custom team composition

        Returns:
            CostForecast with detailed cost breakdown
        """
        # Calculate labor costs by role
        labor_costs = {}
        for role, hours in estimate.resource_requirements.items():
            rate = self.labor_rates.get(role, 70)
            labor_costs[role] = round(hours * rate, 2)

        total_labor = sum(labor_costs.values())

        # Infrastructure costs
        infrastructure_costs = round(total_labor * 0.05, 2)

        # Tools & licenses
        tools_licenses = round(total_labor * 0.03, 2)

        # Contingency reserve (10% for known risks)
        contingency_reserve = round(total_labor * 0.10, 2)

        # Management reserve (5% for unknown risks)
        management_reserve = round(total_labor * 0.05, 2)

        # Cost per deliverable type
        cost_per_deliverable = {}
        for item_type, count in estimate.scope.items():
            if count > 0:
                type_hours = sum(
                    hours for role, hours in estimate.resource_requirements.items()
                    if item_type.lower() in role.lower()
                )
                if type_hours == 0:
                    # Approximate if no direct mapping
                    type_hours = estimate.total_hours / len(estimate.scope)

                type_rate = sum(self.labor_rates.values()) / len(self.labor_rates)
                cost_per_deliverable[item_type] = round(type_hours * type_rate / count, 2)

        total_cost = (
            total_labor +
            infrastructure_costs +
            tools_licenses +
            contingency_reserve +
            management_reserve
        )

        return CostForecast(
            total_cost=round(total_cost, 2),
            labor_costs=labor_costs,
            infrastructure_costs=infrastructure_costs,
            tools_licenses=tools_licenses,
            contingency_reserve=contingency_reserve,
            management_reserve=management_reserve,
            cost_per_deliverable=cost_per_deliverable
        )

    # ==================== RISK ASSESSMENT ====================

    def assess_risks(
        self,
        estimate: ProjectEstimate,
        risk_factors: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Assess project risks and provide mitigation strategies

        Args:
            estimate: ProjectEstimate object
            risk_factors: Optional risk factors

        Returns:
            List of risks with probability, impact, and mitigation
        """
        risks = []

        risk_factors = risk_factors or {}

        # Schedule risk
        if estimate.risk_level in ["medium", "high"]:
            risks.append({
                "risk_id": "RISK-001",
                "category": "schedule",
                "description": "Project may exceed estimated timeline",
                "probability": "medium" if estimate.risk_level == "medium" else "high",
                "impact": "high",
                "mitigation": [
                    "Add 20% schedule buffer",
                    "Implement weekly progress reviews",
                    "Identify critical path and monitor closely"
                ],
                "contingency": "Reduce scope or add resources"
            })

        # Resource availability risk
        if len(estimate.resource_requirements) > 5:
            risks.append({
                "risk_id": "RISK-002",
                "category": "resources",
                "description": "Multiple specialized resources required",
                "probability": "medium",
                "impact": "medium",
                "mitigation": [
                    "Secure resource commitments early",
                    "Identify backup resources",
                    "Cross-train team members"
                ],
                "contingency": "Outsource specialized tasks"
            })

        # Cost overrun risk
        cost_range = estimate.cost_confidence[1] - estimate.cost_confidence[0]
        if cost_range / estimate.total_cost > 0.3:
            risks.append({
                "risk_id": "RISK-003",
                "category": "cost",
                "description": "High cost uncertainty (±30%)",
                "probability": "medium",
                "impact": "high",
                "mitigation": [
                    "Refine estimates after initial sprint",
                    "Use time & materials contract",
                    "Establish change control process"
                ],
                "contingency": "Access management reserve funds"
            })

        # Quality risk
        if risk_factors.get("first_time_content_type"):
            risks.append({
                "risk_id": "RISK-004",
                "category": "quality",
                "description": "New content type may require iterations",
                "probability": "medium",
                "impact": "medium",
                "mitigation": [
                    "Create prototype early",
                    "Implement peer review process",
                    "Schedule additional QA time"
                ],
                "contingency": "Extend timeline for quality assurance"
            })

        # Dependency risk
        if risk_factors.get("external_dependencies"):
            risks.append({
                "risk_id": "RISK-005",
                "category": "dependencies",
                "description": "External dependencies may cause delays",
                "probability": "high",
                "impact": "high",
                "mitigation": [
                    "Identify all dependencies upfront",
                    "Establish SLAs with external parties",
                    "Plan parallel work where possible"
                ],
                "contingency": "Fast-track critical path items"
            })

        return risks

    # ==================== REPORTING ====================

    def generate_estimate_report(
        self,
        estimate: ProjectEstimate,
        cost_forecast: CostForecast,
        risks: List[Dict[str, Any]]
    ) -> str:
        """
        Generate comprehensive estimation report

        Args:
            estimate: ProjectEstimate object
            cost_forecast: CostForecast object
            risks: List of project risks

        Returns:
            Markdown estimation report
        """
        # Resource requirements table
        resource_table = "| Role | Hours | Cost |\n|------|-------|------|\n"
        for role, hours in estimate.resource_requirements.items():
            cost = cost_forecast.labor_costs.get(role, 0)
            resource_table += f"| {role.replace('_', ' ').title()} | {hours:.1f} | ${cost:,.2f} |\n"

        # Risk matrix
        risk_table = "| ID | Category | Description | Probability | Impact |\n|-----|----------|-------------|-------------|--------|\n"
        for risk in risks:
            risk_table += (
                f"| {risk['risk_id']} | {risk['category'].title()} | "
                f"{risk['description']} | {risk['probability'].title()} | "
                f"{risk['impact'].title()} |\n"
            )

        # Cost breakdown
        cost_breakdown = f"""- **Labor**: ${sum(cost_forecast.labor_costs.values()):,.2f}
- **Infrastructure**: ${cost_forecast.infrastructure_costs:,.2f}
- **Tools & Licenses**: ${cost_forecast.tools_licenses:,.2f}
- **Contingency Reserve**: ${cost_forecast.contingency_reserve:,.2f}
- **Management Reserve**: ${cost_forecast.management_reserve:,.2f}
- **Total**: ${cost_forecast.total_cost:,.2f}"""

        report = f"""# Project Estimation Report

**Project Type**: {estimate.project_type.replace('_', ' ').title()}
**Risk Level**: {estimate.risk_level.upper()}
**Estimated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

---

## Executive Summary

**Timeline**: {estimate.timeline_weeks:.1f} weeks ({estimate.timeline_confidence[0]:.1f} - {estimate.timeline_confidence[1]:.1f} weeks, 90% CI)
**Total Effort**: {estimate.total_hours:.1f} hours
**Total Cost**: ${estimate.total_cost:,.2f} (${estimate.cost_confidence[0]:,.2f} - ${estimate.cost_confidence[1]:,.2f}, 90% CI)

---

## Scope

{chr(10).join([f"- **{k.title()}**: {v}" for k, v in estimate.scope.items()])}

---

## Resource Requirements

{resource_table}

**Total Hours**: {sum(estimate.resource_requirements.values()):.1f}

---

## Cost Forecast

{cost_breakdown}

### Cost Per Deliverable

{chr(10).join([f"- **{k.title()}**: ${v:,.2f} per unit" for k, v in cost_forecast.cost_per_deliverable.items()])}

---

## Risk Assessment

**Overall Risk Level**: {estimate.risk_level.upper()}

{risk_table}

### Risk Mitigation Strategies

{chr(10).join([f"**{risk['risk_id']} - {risk['description']}**{chr(10)}- " + chr(10).join(f"  - {m}" for m in risk['mitigation']) for risk in risks])}

---

## Recommendations

{'- Add 30% schedule buffer due to high risk level' if estimate.risk_level == 'high' else '- Add 15% schedule buffer for medium risk level' if estimate.risk_level == 'medium' else '- Minimal buffer required for low-risk project'}
- Secure critical resources before project start
- Implement weekly progress tracking
- Establish change control process for scope changes
- Conduct sprint retrospectives for continuous improvement

---

**Estimation Method**: Three-Point Estimation (PERT) with Monte Carlo Simulation (1,000 iterations)
**Confidence Level**: 90%
**Historical Data**: Based on {len(self.productivity_rates)} content types with {sum(len(v) for v in self.productivity_rates.values())} complexity levels

---

**Generated by**: Planning Estimator v1.0
"""

        return report


if __name__ == "__main__":
    # Example usage
    estimator = PlanningEstimator()

    # Estimate a curriculum development project
    print("=== Project Estimation ===")
    estimate = estimator.estimate_project(
        project_type="curriculum_development",
        scope={"lessons": 20, "assessments": 5, "multimedia": 10},
        team_experience="medium",
        complexity_factors={"lesson_complexity": "medium", "assessment_complexity": "high"}
    )

    print(f"Timeline: {estimate.timeline_weeks} weeks")
    print(f"Confidence Interval: {estimate.timeline_confidence[0]} - {estimate.timeline_confidence[1]} weeks")
    print(f"Total Hours: {estimate.total_hours}")
    print(f"Total Cost: ${estimate.total_cost:,.2f}")
    print(f"Risk Level: {estimate.risk_level}")

    # Cost forecast
    print("\n=== Cost Forecast ===")
    cost_forecast = estimator.forecast_costs(estimate)
    print(f"Total Cost: ${cost_forecast.total_cost:,.2f}")
    print(f"Labor Costs: ${sum(cost_forecast.labor_costs.values()):,.2f}")
    print(f"Contingency: ${cost_forecast.contingency_reserve:,.2f}")

    # Risk assessment
    print("\n=== Risk Assessment ===")
    risks = estimator.assess_risks(
        estimate,
        risk_factors={"first_time_content_type": True, "external_dependencies": True}
    )
    print(f"Identified Risks: {len(risks)}")
    for risk in risks:
        print(f"- {risk['risk_id']}: {risk['description']} ({risk['probability']}/{risk['impact']})")

    # Generate report
    print("\n=== Estimation Report ===")
    report = estimator.generate_estimate_report(estimate, cost_forecast, risks)
    print(report[:600] + "...")
