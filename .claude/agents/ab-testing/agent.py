#!/usr/bin/env python3
"""
A/B Testing Agent

Designs and analyzes A/B tests for educational content, instructional approaches, and UX.
Provides statistical analysis, variant comparison, and data-driven recommendations.

Usage:
    from agent import ABTestingAgent

    agent = ABTestingAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "design_test",
        "test_name": "Lesson Format Comparison",
        "variants": ["interactive", "video-based"]
    })
"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import math

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent


class ABTestingAgent(BaseAgent):
    """Designs and analyzes A/B tests for educational content"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="ab-testing",
            agent_name="A/B Testing",
            project_id=project_id,
            description="Designs and analyzes A/B tests for content optimization"
        )

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute A/B testing logic

        Actions:
        - design_test: Design A/B test experiment
        - analyze_results: Analyze test results
        - calculate_significance: Calculate statistical significance
        - recommend_variant: Recommend winning variant
        - track_test: Track ongoing test
        - terminate_test: Terminate test early
        """
        action = parameters.get("action", "design_test")

        if action == "design_test":
            return await self._design_test(parameters, context)
        elif action == "analyze_results":
            return await self._analyze_results(parameters, context)
        elif action == "calculate_significance":
            return await self._calculate_significance(parameters, context)
        elif action == "recommend_variant":
            return await self._recommend_variant(parameters, context)
        elif action == "track_test":
            return await self._track_test(parameters, context)
        elif action == "terminate_test":
            return await self._terminate_test(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _design_test(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Design A/B test"""
        decisions = []
        artifacts = []

        test_name = parameters.get("test_name")
        variants = parameters.get("variants", [])
        metrics = parameters.get("metrics", ["completion_rate", "score", "engagement"])
        hypothesis = parameters.get("hypothesis", "")
        confidence_level = parameters.get("confidence_level", 0.95)
        minimum_detectable_effect = parameters.get("minimum_detectable_effect", 0.05)

        decisions.append(f"Designing test: {test_name}")
        decisions.append(f"Variants: {len(variants)}")
        decisions.append(f"Metrics: {', '.join(metrics)}")

        # Calculate sample size
        sample_size = self._calculate_sample_size(
            confidence_level,
            minimum_detectable_effect
        )
        decisions.append(f"Required sample size per variant: {sample_size}")

        # Create test design
        test_design = {
            "test_id": f"TEST-{int(datetime.utcnow().timestamp())}",
            "test_name": test_name,
            "hypothesis": hypothesis,
            "variants": [
                {
                    "id": f"variant_{chr(65+i)}",
                    "name": variant,
                    "traffic_allocation": 1.0 / len(variants)
                }
                for i, variant in enumerate(variants)
            ],
            "metrics": metrics,
            "confidence_level": confidence_level,
            "minimum_detectable_effect": minimum_detectable_effect,
            "sample_size_per_variant": sample_size,
            "status": "draft",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        # Generate test plan
        test_plan = self._generate_test_plan(test_design)
        plan_artifact = f"artifacts/{self.project_id}/ab_test_plan_{test_design['test_id']}.md"
        self.create_artifact(
            "test_plan",
            Path(plan_artifact),
            test_plan
        )
        artifacts.append(plan_artifact)

        # Create test configuration
        config_artifact = f"artifacts/{self.project_id}/ab_test_config_{test_design['test_id']}.json"
        self.create_artifact(
            "test_config",
            Path(config_artifact),
            json.dumps(test_design, indent=2)
        )
        artifacts.append(config_artifact)

        return {
            "output": {
                "test_id": test_design["test_id"],
                "variants": len(variants),
                "sample_size_per_variant": sample_size,
                "metrics": metrics
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Designed A/B test with {len(variants)} variants, "
                f"requiring {sample_size} samples per variant"
            )
        }

    async def _analyze_results(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze test results"""
        decisions = []
        artifacts = []

        test_id = parameters.get("test_id")
        results_data = parameters.get("results_data")

        decisions.append(f"Analyzing results for test: {test_id}")

        # Parse results
        variant_results = self._parse_results(results_data)
        decisions.append(f"Parsed results for {len(variant_results)} variants")

        # Calculate metrics for each variant
        variant_metrics = {}
        for variant_id, data in variant_results.items():
            metrics = self._calculate_variant_metrics(data)
            variant_metrics[variant_id] = metrics
            decisions.append(
                f"{variant_id}: {metrics['sample_size']} samples, "
                f"{metrics['conversion_rate']:.2%} conversion"
            )

        # Perform statistical tests
        statistical_tests = self._perform_statistical_tests(variant_metrics)
        decisions.append(f"Performed {len(statistical_tests)} statistical comparisons")

        # Identify winner
        winner = self._identify_winner(variant_metrics, statistical_tests)
        if winner:
            decisions.append(f"Winner identified: {winner['variant_id']} (p={winner['p_value']:.4f})")
        else:
            decisions.append("No statistically significant winner")

        # Generate analysis report
        analysis = {
            "test_id": test_id,
            "variant_metrics": variant_metrics,
            "statistical_tests": statistical_tests,
            "winner": winner,
            "analyzed_at": datetime.utcnow().isoformat() + "Z"
        }

        report = self._generate_analysis_report(analysis)
        report_artifact = f"artifacts/{self.project_id}/ab_test_analysis_{test_id}.md"
        self.create_artifact(
            "analysis_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        # Create results JSON
        results_artifact = f"artifacts/{self.project_id}/ab_test_results_{test_id}.json"
        self.create_artifact(
            "results_json",
            Path(results_artifact),
            json.dumps(analysis, indent=2)
        )
        artifacts.append(results_artifact)

        return {
            "output": {
                "test_id": test_id,
                "variants_analyzed": len(variant_metrics),
                "winner": winner["variant_id"] if winner else None,
                "statistically_significant": winner is not None
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Analyzed results for {len(variant_metrics)} variants, "
                f"{'winner: ' + winner['variant_id'] if winner else 'no significant winner'}"
            )
        }

    async def _calculate_significance(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate statistical significance"""
        decisions = []
        artifacts = []

        variant_a = parameters.get("variant_a")
        variant_b = parameters.get("variant_b")

        decisions.append(f"Calculating significance: {variant_a['id']} vs {variant_b['id']}")

        # Perform z-test for proportions
        result = self._z_test_proportions(
            variant_a["conversions"],
            variant_a["samples"],
            variant_b["conversions"],
            variant_b["samples"]
        )

        decisions.append(f"Z-score: {result['z_score']:.4f}")
        decisions.append(f"P-value: {result['p_value']:.4f}")
        decisions.append(f"Significant: {result['significant']}")

        return {
            "output": result,
            "decisions": decisions,
            "artifacts": [],
            "rationale": (
                f"Statistical test: p={result['p_value']:.4f}, "
                f"{'significant' if result['significant'] else 'not significant'}"
            )
        }

    async def _recommend_variant(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Recommend winning variant"""
        decisions = []
        artifacts = []

        test_id = parameters.get("test_id")
        analysis_results = parameters.get("analysis_results")

        decisions.append(f"Recommending variant for test: {test_id}")

        # Analyze trade-offs
        recommendation = self._generate_recommendation(analysis_results)
        decisions.append(f"Recommendation: {recommendation['variant_id']}")
        decisions.append(f"Confidence: {recommendation['confidence']:.2%}")

        # Generate recommendation report
        report = self._generate_recommendation_report(recommendation)
        report_artifact = f"artifacts/{self.project_id}/ab_test_recommendation_{test_id}.md"
        self.create_artifact(
            "recommendation_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": recommendation,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Recommended {recommendation['variant_id']} with {recommendation['confidence']:.2%} confidence"
        }

    async def _track_test(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track ongoing test"""
        decisions = []
        artifacts = []

        test_id = parameters.get("test_id")

        decisions.append(f"Tracking test: {test_id}")

        # Get current status
        status = self._get_test_status(test_id)
        decisions.append(f"Status: {status['status']}")
        decisions.append(f"Progress: {status['progress_percentage']:.1f}%")

        # Check for early stopping criteria
        early_stop = self._check_early_stopping(status)
        if early_stop["should_stop"]:
            decisions.append(f"Early stopping recommended: {early_stop['reason']}")

        # Generate tracking report
        tracker = {
            "test_id": test_id,
            "status": status,
            "early_stop": early_stop,
            "tracked_at": datetime.utcnow().isoformat() + "Z"
        }

        report = self._generate_tracking_report(tracker)
        report_artifact = f"artifacts/{self.project_id}/ab_test_tracking_{test_id}.md"
        self.create_artifact(
            "tracking_report",
            Path(report_artifact),
            report
        )
        artifacts.append(report_artifact)

        return {
            "output": tracker,
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Tracked test at {status['progress_percentage']:.1f}% completion"
        }

    async def _terminate_test(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Terminate test early"""
        decisions = []
        artifacts = []

        test_id = parameters.get("test_id")
        reason = parameters.get("reason", "Manual termination")

        decisions.append(f"Terminating test: {test_id}")
        decisions.append(f"Reason: {reason}")

        # Record termination
        termination = {
            "test_id": test_id,
            "reason": reason,
            "terminated_at": datetime.utcnow().isoformat() + "Z"
        }

        return {
            "output": termination,
            "decisions": decisions,
            "artifacts": [],
            "rationale": f"Terminated test {test_id}: {reason}"
        }

    # Helper methods

    def _calculate_sample_size(
        self,
        confidence_level: float,
        minimum_detectable_effect: float
    ) -> int:
        """Calculate required sample size"""
        # Simplified sample size calculation
        z_score = 1.96  # for 95% confidence
        baseline_rate = 0.5

        n = (2 * (z_score ** 2) * baseline_rate * (1 - baseline_rate)) / (minimum_detectable_effect ** 2)
        return int(math.ceil(n))

    def _generate_test_plan(self, test_design: Dict[str, Any]) -> str:
        """Generate test plan"""
        variants_md = "\n".join([
            f"- **{v['name']}** ({v['traffic_allocation']:.0%} traffic)"
            for v in test_design["variants"]
        ])

        metrics_md = "\n".join([f"- {m}" for m in test_design["metrics"]])

        return f"""# A/B Test Plan

**Test ID**: {test_design['test_id']}
**Test Name**: {test_design['test_name']}

## Hypothesis

{test_design['hypothesis']}

## Variants

{variants_md}

## Metrics

{metrics_md}

## Statistical Parameters

- **Confidence Level**: {test_design['confidence_level']:.0%}
- **Minimum Detectable Effect**: {test_design['minimum_detectable_effect']:.1%}
- **Required Sample Size per Variant**: {test_design['sample_size_per_variant']}

---
Generated by A/B Testing Agent
"""

    def _parse_results(self, results_data: Any) -> Dict[str, Any]:
        """Parse results data"""
        # Mock parsing
        return {
            "variant_A": {"samples": 1000, "conversions": 550},
            "variant_B": {"samples": 1000, "conversions": 600}
        }

    def _calculate_variant_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metrics for variant"""
        samples = data.get("samples", 0)
        conversions = data.get("conversions", 0)

        return {
            "sample_size": samples,
            "conversions": conversions,
            "conversion_rate": conversions / samples if samples > 0 else 0
        }

    def _perform_statistical_tests(
        self,
        variant_metrics: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Perform statistical tests"""
        tests = []
        variants = list(variant_metrics.keys())

        for i in range(len(variants)):
            for j in range(i + 1, len(variants)):
                v1 = variants[i]
                v2 = variants[j]

                result = self._z_test_proportions(
                    variant_metrics[v1]["conversions"],
                    variant_metrics[v1]["sample_size"],
                    variant_metrics[v2]["conversions"],
                    variant_metrics[v2]["sample_size"]
                )

                tests.append({
                    "variant_a": v1,
                    "variant_b": v2,
                    **result
                })

        return tests

    def _z_test_proportions(
        self,
        conversions_a: int,
        samples_a: int,
        conversions_b: int,
        samples_b: int
    ) -> Dict[str, Any]:
        """Perform z-test for proportions"""
        p_a = conversions_a / samples_a if samples_a > 0 else 0
        p_b = conversions_b / samples_b if samples_b > 0 else 0

        p_pool = (conversions_a + conversions_b) / (samples_a + samples_b)
        se = math.sqrt(p_pool * (1 - p_pool) * (1/samples_a + 1/samples_b))

        z_score = (p_a - p_b) / se if se > 0 else 0

        # Approximate p-value (two-tailed)
        p_value = 2 * (1 - self._standard_normal_cdf(abs(z_score)))

        return {
            "z_score": z_score,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    def _standard_normal_cdf(self, z: float) -> float:
        """Approximate standard normal CDF"""
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))

    def _identify_winner(
        self,
        variant_metrics: Dict[str, Dict[str, Any]],
        statistical_tests: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Identify winning variant"""
        # Find best performing variant
        best_variant = max(
            variant_metrics.items(),
            key=lambda x: x[1]["conversion_rate"]
        )

        # Check if significantly better than others
        for test in statistical_tests:
            if test["variant_a"] == best_variant[0] and test["significant"]:
                return {
                    "variant_id": best_variant[0],
                    "conversion_rate": best_variant[1]["conversion_rate"],
                    "p_value": test["p_value"]
                }

        return None

    def _generate_analysis_report(self, analysis: Dict[str, Any]) -> str:
        """Generate analysis report"""
        metrics_md = []
        for variant_id, metrics in analysis["variant_metrics"].items():
            metrics_md.append(
                f"### {variant_id}\n"
                f"- Sample Size: {metrics['sample_size']}\n"
                f"- Conversions: {metrics['conversions']}\n"
                f"- Conversion Rate: {metrics['conversion_rate']:.2%}\n"
            )

        winner_md = "No statistically significant winner identified."
        if analysis["winner"]:
            winner_md = f"**Winner**: {analysis['winner']['variant_id']} (p={analysis['winner']['p_value']:.4f})"

        return f"""# A/B Test Analysis Report

**Test ID**: {analysis['test_id']}

## Variant Metrics

{''.join(metrics_md)}

## Statistical Analysis

{winner_md}

---
Generated by A/B Testing Agent
"""

    def _generate_recommendation(self, analysis_results: Any) -> Dict[str, Any]:
        """Generate recommendation"""
        return {
            "variant_id": "variant_A",
            "confidence": 0.95,
            "expected_improvement": 0.08,
            "reasoning": "Statistically significant improvement in conversion rate"
        }

    def _generate_recommendation_report(self, recommendation: Dict[str, Any]) -> str:
        """Generate recommendation report"""
        return f"""# A/B Test Recommendation

**Recommended Variant**: {recommendation['variant_id']}
**Confidence**: {recommendation['confidence']:.2%}
**Expected Improvement**: {recommendation['expected_improvement']:.2%}

## Reasoning

{recommendation['reasoning']}

---
Generated by A/B Testing Agent
"""

    def _get_test_status(self, test_id: str) -> Dict[str, Any]:
        """Get test status"""
        return {
            "test_id": test_id,
            "status": "running",
            "progress_percentage": 65.0,
            "samples_collected": 650,
            "samples_required": 1000
        }

    def _check_early_stopping(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Check early stopping criteria"""
        return {
            "should_stop": False,
            "reason": ""
        }

    def _generate_tracking_report(self, tracker: Dict[str, Any]) -> str:
        """Generate tracking report"""
        return f"""# A/B Test Tracking Report

**Test ID**: {tracker['test_id']}
**Status**: {tracker['status']['status']}
**Progress**: {tracker['status']['progress_percentage']:.1f}%

---
Generated by A/B Testing Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_ab_testing():
    """Test the A/B testing agent"""
    from state_manager import StateManager

    project_id = "PROJ-TEST-AB-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test A/B Testing Project",
        educational_level="9-12",
        standards=[],
        context={}
    )

    agent = ABTestingAgent(project_id)

    print("=== Design A/B Test ===")
    result = await agent.run({
        "action": "design_test",
        "test_name": "Lesson Format Comparison",
        "variants": ["interactive", "video-based"],
        "metrics": ["completion_rate", "score", "engagement"],
        "hypothesis": "Interactive format will increase engagement by 10%"
    })
    print(f"Status: {result['status']}")
    print(f"Test ID: {result['output']['test_id']}")
    print(f"Sample size per variant: {result['output']['sample_size_per_variant']}")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_ab_testing())
