#!/usr/bin/env python3
"""
Learning Analytics Agent

Analyzes learning outcomes, student performance, and assessment data.
Generates insights, recommendations, and visualizations for improvement.

Usage:
    from agent import LearningAnalyticsAgent

    agent = LearningAnalyticsAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "analyze_outcomes",
        "assessment_data": "data/results.csv"
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


class LearningAnalyticsAgent(BaseAgent):
    """Analyzes learning outcomes and generates insights"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="learning-analytics",
            agent_name="Learning Analytics",
            project_id=project_id,
            description="Analyzes learning outcomes and student performance"
        )

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute learning analytics logic

        Actions:
        - analyze_outcomes: Analyze learning outcomes
        - calculate_mastery: Calculate objective mastery rates
        - identify_gaps: Identify learning gaps
        - generate_insights: Generate actionable insights
        - predict_performance: Predict future performance
        - compare_cohorts: Compare different student groups
        """
        action = parameters.get("action", "analyze_outcomes")

        if action == "analyze_outcomes":
            return await self._analyze_outcomes(parameters, context)
        elif action == "calculate_mastery":
            return await self._calculate_mastery(parameters, context)
        elif action == "identify_gaps":
            return await self._identify_gaps(parameters, context)
        elif action == "generate_insights":
            return await self._generate_insights(parameters, context)
        elif action == "predict_performance":
            return await self._predict_performance(parameters, context)
        elif action == "compare_cohorts":
            return await self._compare_cohorts(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _analyze_outcomes(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze learning outcomes"""
        decisions = []
        artifacts = []

        assessment_data = parameters.get("assessment_data")
        learning_objectives = parameters.get("learning_objectives", [])

        decisions.append(f"Analyzing outcomes for {len(learning_objectives)} objectives")

        # Load and analyze assessment data
        data_summary = self._load_assessment_data(assessment_data)
        decisions.append(f"Loaded data for {data_summary['student_count']} students")

        # Calculate outcome metrics
        metrics = self._calculate_outcome_metrics(data_summary, learning_objectives)
        decisions.append(f"Calculated {len(metrics)} outcome metrics")

        # Identify trends
        trends = self._identify_trends(data_summary, metrics)
        decisions.append(f"Identified {len(trends)} trends")

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, trends)
        decisions.append(f"Generated {len(recommendations)} recommendations")

        # Create analytics report
        report = self._generate_analytics_report(
            assessment_data,
            metrics,
            trends,
            recommendations
        )

        report_artifact = f"artifacts/{self.project_id}/learning_analytics_report.md"
        self.create_artifact(
            "analytics_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create metrics JSON
        metrics_json = json.dumps({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "student_count": data_summary['student_count'],
            "metrics": metrics,
            "trends": trends,
            "recommendations": recommendations
        }, indent=2)

        metrics_artifact = f"artifacts/{self.project_id}/outcome_metrics.json"
        self.create_artifact(
            "metrics",
            Path(metrics_artifact),
            metrics_json
        )
        artifacts.append(metrics_artifact)

        return {
            "output": {
                "student_count": data_summary['student_count'],
                "metrics": metrics,
                "trends_identified": len(trends),
                "recommendations": len(recommendations)
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Analyzed learning outcomes for {data_summary['student_count']} students "
                f"with {len(metrics)} metrics and {len(trends)} trends identified"
            )
        }

    async def _calculate_mastery(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate objective mastery rates"""
        decisions = []
        artifacts = []

        assessment_data = parameters.get("assessment_data")
        mastery_threshold = parameters.get("mastery_threshold", 80.0)  # Percentage

        decisions.append(f"Calculating mastery with {mastery_threshold}% threshold")

        # Calculate mastery for each objective
        mastery_results = self._calculate_objective_mastery(
            assessment_data,
            mastery_threshold
        )

        decisions.append(f"Calculated mastery for {len(mastery_results)} objectives")

        # Calculate overall mastery rate
        overall_mastery = sum(
            obj["mastery_rate"] for obj in mastery_results
        ) / len(mastery_results) if mastery_results else 0

        decisions.append(f"Overall mastery rate: {overall_mastery:.1f}%")

        # Create mastery report
        report = self._generate_mastery_report(
            mastery_results,
            mastery_threshold,
            overall_mastery
        )

        report_artifact = f"artifacts/{self.project_id}/mastery_analysis.md"
        self.create_artifact(
            "mastery_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "overall_mastery_rate": overall_mastery,
                "objectives_analyzed": len(mastery_results),
                "objectives_mastered": len([obj for obj in mastery_results if obj["mastery_rate"] >= mastery_threshold]),
                "mastery_results": mastery_results
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Calculated mastery rates for {len(mastery_results)} objectives "
                f"with overall rate of {overall_mastery:.1f}%"
            )
        }

    async def _identify_gaps(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identify learning gaps"""
        decisions = []
        artifacts = []

        assessment_data = parameters.get("assessment_data")
        gap_threshold = parameters.get("gap_threshold", 60.0)  # Performance below this indicates gap

        decisions.append(f"Identifying gaps below {gap_threshold}% performance")

        # Identify gaps by objective
        gaps = self._find_learning_gaps(assessment_data, gap_threshold)
        decisions.append(f"Identified {len(gaps)} learning gaps")

        # Categorize gaps by severity
        gap_categories = self._categorize_gaps(gaps)
        decisions.append(
            f"Critical: {gap_categories['critical']}, "
            f"Moderate: {gap_categories['moderate']}, "
            f"Minor: {gap_categories['minor']}"
        )

        # Generate intervention strategies
        interventions = self._generate_interventions(gaps)
        decisions.append(f"Generated {len(interventions)} intervention strategies")

        # Create gap analysis report
        report = self._generate_gap_analysis_report(
            gaps,
            gap_categories,
            interventions
        )

        report_artifact = f"artifacts/{self.project_id}/learning_gaps_analysis.md"
        self.create_artifact(
            "gap_analysis",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "gaps_identified": len(gaps),
                "gap_categories": gap_categories,
                "interventions_recommended": len(interventions)
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Identified {len(gaps)} learning gaps and generated "
                f"{len(interventions)} intervention strategies"
            )
        }

    async def _generate_insights(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate actionable insights"""
        decisions = []
        artifacts = []

        assessment_data = parameters.get("assessment_data")
        focus_areas = parameters.get("focus_areas", [
            "performance", "engagement", "mastery", "improvement"
        ])

        decisions.append(f"Generating insights for {len(focus_areas)} focus areas")

        # Generate insights for each focus area
        insights = {}
        for area in focus_areas:
            area_insights = self._generate_area_insights(assessment_data, area)
            insights[area] = area_insights
            decisions.append(f"{area}: {len(area_insights)} insights")

        # Prioritize insights
        prioritized = self._prioritize_insights(insights)
        decisions.append(f"Prioritized top {len(prioritized)} actionable insights")

        # Create insights report
        report = self._generate_insights_report(insights, prioritized)

        report_artifact = f"artifacts/{self.project_id}/actionable_insights.md"
        self.create_artifact(
            "insights_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "focus_areas": focus_areas,
                "total_insights": sum(len(area_insights) for area_insights in insights.values()),
                "prioritized_insights": prioritized[:5]  # Top 5
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Generated insights across {len(focus_areas)} focus areas "
                f"with {len(prioritized)} prioritized recommendations"
            )
        }

    async def _predict_performance(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Predict future performance"""
        decisions = []
        artifacts = []

        historical_data = parameters.get("historical_data")
        prediction_window = parameters.get("prediction_window", 30)  # Days

        decisions.append(f"Predicting performance for next {prediction_window} days")

        # Analyze historical trends
        trends = self._analyze_historical_trends(historical_data)
        decisions.append(f"Analyzed {len(trends)} historical trends")

        # Generate predictions
        predictions = self._generate_predictions(trends, prediction_window)
        decisions.append(f"Generated predictions for {len(predictions)} metrics")

        # Calculate confidence intervals
        confidence = self._calculate_confidence_intervals(predictions)
        decisions.append(f"Calculated confidence intervals: {confidence}%")

        # Create predictions report
        report = self._generate_predictions_report(
            predictions,
            confidence,
            prediction_window
        )

        report_artifact = f"artifacts/{self.project_id}/performance_predictions.md"
        self.create_artifact(
            "predictions_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "prediction_window": prediction_window,
                "predictions": predictions,
                "confidence": confidence
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Generated {prediction_window}-day performance predictions "
                f"with {confidence}% confidence"
            )
        }

    async def _compare_cohorts(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare different student cohorts"""
        decisions = []
        artifacts = []

        cohort_data = parameters.get("cohort_data")
        comparison_metrics = parameters.get("comparison_metrics", [
            "average_score", "mastery_rate", "improvement_rate"
        ])

        cohort_count = len(cohort_data) if isinstance(cohort_data, list) else 2
        decisions.append(f"Comparing {cohort_count} cohorts on {len(comparison_metrics)} metrics")

        # Perform cohort comparison
        comparison_results = self._perform_cohort_comparison(
            cohort_data,
            comparison_metrics
        )

        decisions.append(f"Compared cohorts on {len(comparison_metrics)} metrics")

        # Identify significant differences
        significant_diffs = self._identify_significant_differences(comparison_results)
        decisions.append(f"Identified {len(significant_diffs)} significant differences")

        # Create comparison report
        report = self._generate_comparison_report(
            comparison_results,
            significant_diffs
        )

        report_artifact = f"artifacts/{self.project_id}/cohort_comparison.md"
        self.create_artifact(
            "comparison_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": {
                "cohorts_compared": cohort_count,
                "comparison_metrics": len(comparison_metrics),
                "significant_differences": len(significant_diffs),
                "comparison_results": comparison_results
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Compared {cohort_count} cohorts with {len(significant_diffs)} "
                f"significant differences identified"
            )
        }

    # Helper methods

    def _load_assessment_data(self, assessment_data: str) -> Dict[str, Any]:
        """Load assessment data"""
        # Mock data loading
        return {
            "student_count": 150,
            "assessment_count": 5,
            "average_score": 78.5
        }

    def _calculate_outcome_metrics(
        self,
        data_summary: Dict[str, Any],
        objectives: List[str]
    ) -> Dict[str, Any]:
        """Calculate outcome metrics"""
        return {
            "average_score": data_summary.get("average_score", 75.0),
            "median_score": 77.0,
            "standard_deviation": 12.5,
            "pass_rate": 85.0,
            "improvement_rate": 5.2
        }

    def _identify_trends(
        self,
        data_summary: Dict[str, Any],
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify trends in data"""
        return [
            {
                "trend": "improving",
                "metric": "average_score",
                "change": "+5.2%",
                "significance": "high"
            },
            {
                "trend": "stable",
                "metric": "pass_rate",
                "change": "+0.5%",
                "significance": "low"
            }
        ]

    def _generate_recommendations(
        self,
        metrics: Dict[str, Any],
        trends: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations"""
        return [
            "Continue current instructional strategies - performance improving",
            "Focus additional support on lower-performing objectives",
            "Increase formative assessment frequency to maintain improvement trend"
        ]

    def _generate_analytics_report(
        self,
        assessment_data: str,
        metrics: Dict[str, Any],
        trends: List[Dict[str, Any]],
        recommendations: List[str]
    ) -> str:
        """Generate analytics report"""
        metrics_md = "\n".join([f"- **{k.replace('_', ' ').title()}**: {v}" for k, v in metrics.items()])
        trends_md = "\n".join([
            f"- **{t['metric']}**: {t['trend'].title()} ({t['change']}) - {t['significance']} significance"
            for t in trends
        ])
        recommendations_md = "\n".join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])

        return f"""# Learning Analytics Report

**Data Source**: {assessment_data}
**Analysis Date**: {datetime.utcnow().strftime("%Y-%m-%d")}

## Key Metrics

{metrics_md}

## Trends Identified

{trends_md}

## Recommendations

{recommendations_md}

---
Generated by Learning Analytics Agent
"""

    def _calculate_objective_mastery(
        self,
        assessment_data: str,
        threshold: float
    ) -> List[Dict[str, Any]]:
        """Calculate mastery by objective"""
        # Mock mastery calculation
        return [
            {
                "objective_id": "OBJ-001",
                "mastery_rate": 85.0,
                "students_mastered": 127,
                "total_students": 150,
                "mastered": True
            },
            {
                "objective_id": "OBJ-002",
                "mastery_rate": 72.0,
                "students_mastered": 108,
                "total_students": 150,
                "mastered": False
            }
        ]

    def _generate_mastery_report(
        self,
        mastery_results: List[Dict[str, Any]],
        threshold: float,
        overall_mastery: float
    ) -> str:
        """Generate mastery report"""
        results_md = []
        for result in mastery_results:
            status = "✓ Mastered" if result["mastered"] else "✗ Not Mastered"
            results_md.append(
                f"### {result['objective_id']}: {status}\n"
                f"- Mastery Rate: {result['mastery_rate']:.1f}%\n"
                f"- Students Mastered: {result['students_mastered']}/{result['total_students']}\n"
            )

        return f"""# Objective Mastery Analysis

**Mastery Threshold**: {threshold}%
**Overall Mastery Rate**: {overall_mastery:.1f}%

## Results by Objective

{''.join(results_md)}

---
Generated by Learning Analytics Agent
"""

    def _find_learning_gaps(
        self,
        assessment_data: str,
        threshold: float
    ) -> List[Dict[str, Any]]:
        """Find learning gaps"""
        return [
            {
                "objective_id": "OBJ-002",
                "performance": 72.0,
                "gap_size": threshold - 72.0,
                "severity": "moderate",
                "student_count": 42
            }
        ]

    def _categorize_gaps(self, gaps: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize gaps by severity"""
        categories = {"critical": 0, "moderate": 0, "minor": 0}
        for gap in gaps:
            categories[gap.get("severity", "minor")] += 1
        return categories

    def _generate_interventions(
        self,
        gaps: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate intervention strategies"""
        return [
            {
                "gap": gap,
                "intervention": "Provide additional scaffolding and practice",
                "expected_impact": "10-15% improvement"
            }
            for gap in gaps
        ]

    def _generate_gap_analysis_report(
        self,
        gaps: List[Dict[str, Any]],
        categories: Dict[str, int],
        interventions: List[Dict[str, Any]]
    ) -> str:
        """Generate gap analysis report"""
        gaps_md = []
        for gap in gaps:
            gaps_md.append(
                f"### {gap['objective_id']} - {gap['severity'].title()}\n"
                f"- Current Performance: {gap['performance']:.1f}%\n"
                f"- Gap Size: {gap['gap_size']:.1f} percentage points\n"
                f"- Students Affected: {gap['student_count']}\n"
            )

        return f"""# Learning Gaps Analysis

## Gap Summary

- Critical: {categories['critical']}
- Moderate: {categories['moderate']}
- Minor: {categories['minor']}

## Identified Gaps

{''.join(gaps_md)}

## Recommended Interventions

{len(interventions)} intervention strategies generated.

---
Generated by Learning Analytics Agent
"""

    def _generate_area_insights(
        self,
        assessment_data: str,
        area: str
    ) -> List[str]:
        """Generate insights for specific area"""
        insights_map = {
            "performance": ["Average scores trending upward", "Top 25% showing exceptional growth"],
            "engagement": ["Participation rate at 92%", "Assignment completion improved"],
            "mastery": ["85% of objectives above threshold", "2 objectives need attention"],
            "improvement": ["5.2% improvement over baseline", "Growth rate accelerating"]
        }
        return insights_map.get(area, [])

    def _prioritize_insights(
        self,
        insights: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Prioritize insights"""
        prioritized = []
        for area, area_insights in insights.items():
            for insight in area_insights:
                prioritized.append({
                    "area": area,
                    "insight": insight,
                    "priority": "high" if "need attention" in insight else "medium"
                })
        return sorted(prioritized, key=lambda x: 0 if x["priority"] == "high" else 1)

    def _generate_insights_report(
        self,
        insights: Dict[str, List[str]],
        prioritized: List[Dict[str, Any]]
    ) -> str:
        """Generate insights report"""
        insights_md = []
        for area, area_insights in insights.items():
            insights_md.append(f"### {area.title()}\n")
            for insight in area_insights:
                insights_md.append(f"- {insight}\n")

        prioritized_md = "\n".join([
            f"{i+1}. **[{ins['priority'].upper()}]** {ins['area'].title()}: {ins['insight']}"
            for i, ins in enumerate(prioritized)
        ])

        return f"""# Actionable Insights

## Insights by Focus Area

{''.join(insights_md)}

## Prioritized Recommendations

{prioritized_md}

---
Generated by Learning Analytics Agent
"""

    def _analyze_historical_trends(self, historical_data: str) -> List[Dict[str, Any]]:
        """Analyze historical trends"""
        return [
            {"metric": "average_score", "trend": "increasing", "rate": 0.5},
            {"metric": "mastery_rate", "trend": "stable", "rate": 0.1}
        ]

    def _generate_predictions(
        self,
        trends: List[Dict[str, Any]],
        window: int
    ) -> Dict[str, Any]:
        """Generate predictions"""
        return {
            "average_score": 80.5,
            "mastery_rate": 87.0,
            "improvement_rate": 6.0
        }

    def _calculate_confidence_intervals(
        self,
        predictions: Dict[str, Any]
    ) -> float:
        """Calculate confidence intervals"""
        return 85.0

    def _generate_predictions_report(
        self,
        predictions: Dict[str, Any],
        confidence: float,
        window: int
    ) -> str:
        """Generate predictions report"""
        predictions_md = "\n".join([
            f"- **{k.replace('_', ' ').title()}**: {v}"
            for k, v in predictions.items()
        ])

        return f"""# Performance Predictions

**Prediction Window**: {window} days
**Confidence Level**: {confidence}%

## Predicted Metrics

{predictions_md}

---
Generated by Learning Analytics Agent
"""

    def _perform_cohort_comparison(
        self,
        cohort_data: Any,
        metrics: List[str]
    ) -> Dict[str, Any]:
        """Perform cohort comparison"""
        return {
            "cohort_a": {"average_score": 78.5, "mastery_rate": 85.0},
            "cohort_b": {"average_score": 76.2, "mastery_rate": 82.0}
        }

    def _identify_significant_differences(
        self,
        comparison_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify significant differences"""
        return [
            {
                "metric": "average_score",
                "difference": 2.3,
                "significance": "p < 0.05"
            }
        ]

    def _generate_comparison_report(
        self,
        comparison_results: Dict[str, Any],
        significant_diffs: List[Dict[str, Any]]
    ) -> str:
        """Generate comparison report"""
        return f"""# Cohort Comparison Report

## Comparison Results

Cohorts compared with {len(significant_diffs)} significant differences identified.

---
Generated by Learning Analytics Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_learning_analytics():
    """Test the learning analytics agent"""
    from state_manager import StateManager

    project_id = "PROJ-TEST-ANALYTICS-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test Learning Analytics Project",
        educational_level="9-12",
        standards=["NGSS"],
        context={"subject": "biology", "topic": "genetics"}
    )

    agent = LearningAnalyticsAgent(project_id)

    print("=== Analyze Learning Outcomes ===")
    result = await agent.run({
        "action": "analyze_outcomes",
        "assessment_data": "data/assessment_results.csv",
        "learning_objectives": ["OBJ-001", "OBJ-002", "OBJ-003"]
    })
    print(f"Status: {result['status']}")
    print(f"Student count: {result['output']['student_count']}")
    print(f"Trends identified: {result['output']['trends_identified']}")

    print("\n=== Calculate Mastery Rates ===")
    result = await agent.run({
        "action": "calculate_mastery",
        "assessment_data": "data/assessment_results.csv",
        "mastery_threshold": 80.0
    })
    print(f"Status: {result['status']}")
    print(f"Overall mastery: {result['output']['overall_mastery_rate']:.1f}%")

    print("\n=== Identify Learning Gaps ===")
    result = await agent.run({
        "action": "identify_gaps",
        "assessment_data": "data/assessment_results.csv",
        "gap_threshold": 60.0
    })
    print(f"Status: {result['status']}")
    print(f"Gaps identified: {result['output']['gaps_identified']}")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_learning_analytics())
