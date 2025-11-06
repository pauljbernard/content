#!/usr/bin/env python3
"""
Experiment Engine - Advanced A/B Testing for Educational Content

Provides experimental design, statistical analysis, and automated optimization
for testing content variations and pedagogical approaches

Usage:
    from experiment_engine import ExperimentEngine, ExperimentDesign

    engine = ExperimentEngine()

    # Design experiment
    experiment = engine.create_experiment(
        hypothesis="Multimedia videos improve learning outcomes",
        variants=["control_text_only", "treatment_with_video"],
        metrics=["completion_rate", "assessment_score", "time_on_task"],
        sample_size=500
    )

    # Analyze results
    results = engine.analyze_experiment(
        experiment_id=experiment.experiment_id,
        data=response_data
    )

    # Determine winner
    winner = engine.determine_winner(results, confidence_level=0.95)
"""

import json
import numpy as np
from scipy import stats
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd


class ExperimentStatus(Enum):
    """Experiment status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MetricType(Enum):
    """Metric type for analysis"""
    CONTINUOUS = "continuous"  # e.g., test scores, time
    BINARY = "binary"  # e.g., pass/fail, completion
    COUNT = "count"  # e.g., number of attempts
    ORDINAL = "ordinal"  # e.g., satisfaction rating


@dataclass
class ExperimentDesign:
    """Experiment design specification"""
    experiment_id: str
    name: str
    hypothesis: str
    variants: List[str]
    metrics: List[str]
    metric_types: Dict[str, str]
    sample_size_per_variant: int
    duration_days: int
    confidence_level: float = 0.95
    minimum_detectable_effect: float = 0.10  # 10% relative change
    power: float = 0.80  # 80% statistical power
    randomization_unit: str = "student"  # student, class, school
    stratification_variables: List[str] = field(default_factory=list)
    created_at: str = ""
    status: str = "draft"


@dataclass
class ExperimentResults:
    """Experiment results and analysis"""
    experiment_id: str
    analysis_date: str
    total_participants: int
    participants_by_variant: Dict[str, int]
    metric_results: Dict[str, Dict[str, Any]]
    statistical_tests: Dict[str, Dict[str, Any]]
    winner: Optional[str] = None
    confidence: float = 0.0
    recommendations: List[str] = field(default_factory=list)


class ExperimentEngine:
    """A/B testing and experimental design engine"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize Experiment Engine

        Args:
            data_dir: Directory for experiment data
        """
        self.data_dir = data_dir or Path.home() / ".claude" / "agents" / "experiments"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.experiments: List[ExperimentDesign] = []

    def create_experiment(
        self,
        name: str,
        hypothesis: str,
        variants: List[str],
        metrics: List[str],
        metric_types: Dict[str, str],
        duration_days: int = 14,
        confidence_level: float = 0.95,
        minimum_detectable_effect: float = 0.10,
        stratification_variables: Optional[List[str]] = None
    ) -> ExperimentDesign:
        """
        Create experiment design

        Args:
            name: Experiment name
            hypothesis: Hypothesis being tested
            variants: List of variant names (first is control)
            metrics: List of metrics to measure
            metric_types: Metric types (continuous, binary, count, ordinal)
            duration_days: Experiment duration in days
            confidence_level: Statistical confidence level (typically 0.95)
            minimum_detectable_effect: Minimum effect size to detect (e.g., 0.10 = 10%)
            stratification_variables: Optional stratification variables

        Returns:
            ExperimentDesign object
        """
        experiment_id = f"EXP-{int(datetime.utcnow().timestamp())}"

        # Calculate required sample size per variant
        sample_size = self._calculate_sample_size(
            confidence_level=confidence_level,
            power=0.80,
            effect_size=minimum_detectable_effect,
            num_variants=len(variants)
        )

        experiment = ExperimentDesign(
            experiment_id=experiment_id,
            name=name,
            hypothesis=hypothesis,
            variants=variants,
            metrics=metrics,
            metric_types=metric_types,
            sample_size_per_variant=sample_size,
            duration_days=duration_days,
            confidence_level=confidence_level,
            minimum_detectable_effect=minimum_detectable_effect,
            stratification_variables=stratification_variables or [],
            created_at=datetime.utcnow().isoformat() + "Z",
            status=ExperimentStatus.DRAFT.value
        )

        self.experiments.append(experiment)
        return experiment

    def _calculate_sample_size(
        self,
        confidence_level: float,
        power: float,
        effect_size: float,
        num_variants: int
    ) -> int:
        """
        Calculate required sample size per variant

        Uses power analysis for two-sample t-test

        Args:
            confidence_level: Confidence level (e.g., 0.95)
            power: Statistical power (e.g., 0.80)
            effect_size: Minimum detectable effect (Cohen's d)
            num_variants: Number of variants

        Returns:
            Required sample size per variant
        """
        # Z-scores for confidence level and power
        z_alpha = stats.norm.ppf(1 - (1 - confidence_level) / 2)  # Two-tailed
        z_beta = stats.norm.ppf(power)

        # Cohen's d effect size
        # For relative effect (e.g., 10%), convert to standardized effect size
        # Assume pooled standard deviation = baseline mean (conservative)
        cohen_d = effect_size

        # Sample size formula for two-sample t-test
        n = 2 * ((z_alpha + z_beta) ** 2) / (cohen_d ** 2)

        # Adjust for multiple comparisons (Bonferroni correction)
        if num_variants > 2:
            adjusted_alpha = (1 - confidence_level) / (num_variants - 1)
            z_alpha_adjusted = stats.norm.ppf(1 - adjusted_alpha / 2)
            n = 2 * ((z_alpha_adjusted + z_beta) ** 2) / (cohen_d ** 2)

        # Round up and add 10% buffer
        return int(np.ceil(n * 1.1))

    def analyze_experiment(
        self,
        experiment_id: str,
        data: pd.DataFrame
    ) -> ExperimentResults:
        """
        Analyze experiment results

        Args:
            experiment_id: Experiment identifier
            data: Experimental data (columns: variant, student_id, [metrics])

        Returns:
            ExperimentResults object
        """
        experiment = self._get_experiment(experiment_id)

        if not experiment:
            raise ValueError(f"Experiment not found: {experiment_id}")

        # Calculate participants per variant
        participants_by_variant = data["variant"].value_counts().to_dict()

        # Analyze each metric
        metric_results = {}
        statistical_tests = {}

        for metric in experiment.metrics:
            metric_type = experiment.metric_types.get(metric, "continuous")

            if metric_type == "continuous":
                results, tests = self._analyze_continuous_metric(
                    data, metric, experiment.variants
                )
            elif metric_type == "binary":
                results, tests = self._analyze_binary_metric(
                    data, metric, experiment.variants
                )
            else:
                results, tests = self._analyze_continuous_metric(
                    data, metric, experiment.variants
                )

            metric_results[metric] = results
            statistical_tests[metric] = tests

        # Determine overall winner
        winner, confidence = self._determine_winner(
            experiment, metric_results, statistical_tests
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            experiment, metric_results, statistical_tests, winner
        )

        return ExperimentResults(
            experiment_id=experiment_id,
            analysis_date=datetime.utcnow().isoformat() + "Z",
            total_participants=len(data),
            participants_by_variant=participants_by_variant,
            metric_results=metric_results,
            statistical_tests=statistical_tests,
            winner=winner,
            confidence=confidence,
            recommendations=recommendations
        )

    def _analyze_continuous_metric(
        self,
        data: pd.DataFrame,
        metric: str,
        variants: List[str]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Analyze continuous metric (t-test, ANOVA)"""
        results = {}
        control = variants[0]

        # Calculate descriptive statistics for each variant
        for variant in variants:
            variant_data = data[data["variant"] == variant][metric].dropna()

            results[variant] = {
                "n": len(variant_data),
                "mean": float(variant_data.mean()),
                "std": float(variant_data.std()),
                "median": float(variant_data.median()),
                "min": float(variant_data.min()),
                "max": float(variant_data.max())
            }

        # Statistical tests
        tests = {}

        # Compare each treatment to control
        control_data = data[data["variant"] == control][metric].dropna()

        for variant in variants[1:]:
            treatment_data = data[data["variant"] == variant][metric].dropna()

            # Two-sample t-test
            t_stat, p_value = stats.ttest_ind(treatment_data, control_data)

            # Effect size (Cohen's d)
            pooled_std = np.sqrt(
                ((len(control_data) - 1) * control_data.std() ** 2 +
                 (len(treatment_data) - 1) * treatment_data.std() ** 2) /
                (len(control_data) + len(treatment_data) - 2)
            )
            cohens_d = (treatment_data.mean() - control_data.mean()) / pooled_std if pooled_std > 0 else 0

            # Confidence interval for difference
            se_diff = pooled_std * np.sqrt(1/len(control_data) + 1/len(treatment_data))
            ci_95 = stats.t.interval(
                0.95,
                len(control_data) + len(treatment_data) - 2,
                loc=treatment_data.mean() - control_data.mean(),
                scale=se_diff
            )

            tests[f"{variant}_vs_{control}"] = {
                "test": "two_sample_t_test",
                "t_statistic": float(t_stat),
                "p_value": float(p_value),
                "significant": p_value < 0.05,
                "cohens_d": float(cohens_d),
                "effect_size_interpretation": self._interpret_cohens_d(cohens_d),
                "ci_95_lower": float(ci_95[0]),
                "ci_95_upper": float(ci_95[1]),
                "relative_change": float((treatment_data.mean() - control_data.mean()) / control_data.mean() * 100) if control_data.mean() != 0 else 0
            }

        # ANOVA (if more than 2 variants)
        if len(variants) > 2:
            variant_groups = [
                data[data["variant"] == v][metric].dropna()
                for v in variants
            ]
            f_stat, p_value_anova = stats.f_oneway(*variant_groups)

            tests["anova"] = {
                "test": "one_way_anova",
                "f_statistic": float(f_stat),
                "p_value": float(p_value_anova),
                "significant": p_value_anova < 0.05
            }

        return results, tests

    def _analyze_binary_metric(
        self,
        data: pd.DataFrame,
        metric: str,
        variants: List[str]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Analyze binary metric (chi-square test, proportions test)"""
        results = {}
        control = variants[0]

        # Calculate proportions for each variant
        for variant in variants:
            variant_data = data[data["variant"] == variant][metric].dropna()

            results[variant] = {
                "n": len(variant_data),
                "successes": int(variant_data.sum()),
                "proportion": float(variant_data.mean()),
                "percentage": float(variant_data.mean() * 100)
            }

        # Statistical tests
        tests = {}

        control_data = data[data["variant"] == control][metric].dropna()
        control_successes = int(control_data.sum())
        control_n = len(control_data)
        control_prop = control_successes / control_n if control_n > 0 else 0

        for variant in variants[1:]:
            treatment_data = data[data["variant"] == variant][metric].dropna()
            treatment_successes = int(treatment_data.sum())
            treatment_n = len(treatment_data)
            treatment_prop = treatment_successes / treatment_n if treatment_n > 0 else 0

            # Two-proportion z-test
            pooled_prop = (control_successes + treatment_successes) / (control_n + treatment_n)
            se_pooled = np.sqrt(pooled_prop * (1 - pooled_prop) * (1/control_n + 1/treatment_n))

            if se_pooled > 0:
                z_stat = (treatment_prop - control_prop) / se_pooled
                p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))  # Two-tailed
            else:
                z_stat = 0
                p_value = 1.0

            # Confidence interval for difference in proportions
            se_diff = np.sqrt(
                control_prop * (1 - control_prop) / control_n +
                treatment_prop * (1 - treatment_prop) / treatment_n
            )
            ci_95 = (
                (treatment_prop - control_prop) - 1.96 * se_diff,
                (treatment_prop - control_prop) + 1.96 * se_diff
            )

            tests[f"{variant}_vs_{control}"] = {
                "test": "two_proportion_z_test",
                "z_statistic": float(z_stat),
                "p_value": float(p_value),
                "significant": p_value < 0.05,
                "absolute_difference": float(treatment_prop - control_prop),
                "relative_lift": float((treatment_prop - control_prop) / control_prop * 100) if control_prop > 0 else 0,
                "ci_95_lower": float(ci_95[0]),
                "ci_95_upper": float(ci_95[1])
            }

        return results, tests

    def _interpret_cohens_d(self, cohens_d: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_d = abs(cohens_d)

        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"

    def _determine_winner(
        self,
        experiment: ExperimentDesign,
        metric_results: Dict[str, Dict[str, Any]],
        statistical_tests: Dict[str, Dict[str, Any]]
    ) -> Tuple[Optional[str], float]:
        """Determine experiment winner"""
        control = experiment.variants[0]
        treatments = experiment.variants[1:]

        # Count significant wins for each treatment
        wins = {variant: 0 for variant in treatments}
        total_metrics = len(experiment.metrics)

        for metric in experiment.metrics:
            tests = statistical_tests.get(metric, {})

            for treatment in treatments:
                test_key = f"{treatment}_vs_{control}"
                if test_key in tests:
                    test_result = tests[test_key]

                    if test_result.get("significant", False):
                        # Check if treatment is better (higher mean/proportion)
                        control_value = metric_results[metric][control].get("mean") or metric_results[metric][control].get("proportion")
                        treatment_value = metric_results[metric][treatment].get("mean") or metric_results[metric][treatment].get("proportion")

                        if treatment_value > control_value:
                            wins[treatment] += 1

        # Determine winner (must win on majority of metrics)
        best_treatment = max(wins, key=wins.get)
        win_percentage = wins[best_treatment] / total_metrics if total_metrics > 0 else 0

        if win_percentage >= 0.5:  # Majority of metrics
            return best_treatment, win_percentage
        else:
            return None, 0.0  # No clear winner

    def _generate_recommendations(
        self,
        experiment: ExperimentDesign,
        metric_results: Dict[str, Dict[str, Any]],
        statistical_tests: Dict[str, Dict[str, Any]],
        winner: Optional[str]
    ) -> List[str]:
        """Generate recommendations based on results"""
        recommendations = []

        if winner:
            recommendations.append(f"✅ Deploy '{winner}' variant - showed significant improvement")

            # Quantify impact
            for metric in experiment.metrics:
                tests = statistical_tests.get(metric, {})
                test_key = f"{winner}_vs_{experiment.variants[0]}"

                if test_key in tests and tests[test_key].get("significant"):
                    relative_change = tests[test_key].get("relative_change") or tests[test_key].get("relative_lift", 0)
                    recommendations.append(
                        f"  - {metric.replace('_', ' ').title()}: {relative_change:+.1f}% improvement"
                    )
        else:
            recommendations.append("⚠️ No clear winner - consider running experiment longer or increasing sample size")

        # Check sample size adequacy
        for variant in experiment.variants:
            actual_size = sum(
                metric_results[metric][variant]["n"]
                for metric in experiment.metrics
            ) / len(experiment.metrics)

            if actual_size < experiment.sample_size_per_variant:
                recommendations.append(
                    f"⚠️ '{variant}' underpowered: {int(actual_size)}/{experiment.sample_size_per_variant} participants "
                    f"(need {experiment.sample_size_per_variant - int(actual_size)} more)"
                )

        return recommendations

    def generate_report(self, results: ExperimentResults) -> str:
        """
        Generate experiment report

        Args:
            results: ExperimentResults object

        Returns:
            Markdown experiment report
        """
        experiment = self._get_experiment(results.experiment_id)

        if not experiment:
            raise ValueError(f"Experiment not found: {results.experiment_id}")

        # Winner section
        winner_section = ""
        if results.winner:
            winner_section = f"""
## Winner: {results.winner.replace('_', ' ').title()} ✅

**Confidence**: {results.confidence * 100:.1f}% of metrics showed significant improvement
"""
        else:
            winner_section = """
## Result: No Clear Winner

No variant showed consistent significant improvement across majority of metrics.
"""

        # Metric results sections
        metric_sections = []
        for metric, metric_data in results.metric_results.items():
            metric_type = experiment.metric_types.get(metric, "continuous")

            # Create comparison table
            if metric_type == "continuous":
                rows = []
                for variant, stats in metric_data.items():
                    rows.append(
                        f"| {variant.replace('_', ' ').title()} | {stats['n']} | "
                        f"{stats['mean']:.2f} | {stats['std']:.2f} | "
                        f"{stats['median']:.2f} |"
                    )

                table = "| Variant | N | Mean | Std Dev | Median |\n" + \
                        "|---------|---|------|---------|--------|\n" + \
                        "\n".join(rows)
            else:  # binary
                rows = []
                for variant, stats in metric_data.items():
                    rows.append(
                        f"| {variant.replace('_', ' ').title()} | {stats['n']} | "
                        f"{stats['successes']} | {stats['percentage']:.1f}% |"
                    )

                table = "| Variant | N | Successes | Success Rate |\n" + \
                        "|---------|---|-----------|-------------|\n" + \
                        "\n".join(rows)

            # Statistical tests
            tests_md = []
            tests = results.statistical_tests.get(metric, {})
            for test_name, test_result in tests.items():
                if test_name != "anova":
                    sig_indicator = "✅" if test_result.get("significant") else "❌"
                    p_value = test_result.get("p_value", 1.0)
                    change = test_result.get("relative_change") or test_result.get("relative_lift", 0)

                    tests_md.append(
                        f"**{test_name.replace('_', ' ').title()}**: {sig_indicator}\n"
                        f"- p-value: {p_value:.4f}\n"
                        f"- Change: {change:+.1f}%\n"
                    )

            metric_sections.append(f"""
### {metric.replace('_', ' ').title()}

{table}

#### Statistical Tests

{chr(10).join(tests_md)}
""")

        report = f"""# Experiment Report: {experiment.name}

**Experiment ID**: {results.experiment_id}
**Analysis Date**: {results.analysis_date}
**Hypothesis**: {experiment.hypothesis}

---

## Summary

**Total Participants**: {results.total_participants}
**Variants**: {', '.join(experiment.variants)}
**Metrics Analyzed**: {len(experiment.metrics)}

**Participants by Variant**:
{chr(10).join([f"- {variant}: {count}" for variant, count in results.participants_by_variant.items()])}

{winner_section}

---

## Detailed Results

{chr(10).join(metric_sections)}

---

## Recommendations

{chr(10).join([f"- {rec}" for rec in results.recommendations])}

---

## Methodology

**Statistical Approach**:
- Confidence Level: {experiment.confidence_level * 100}%
- Minimum Detectable Effect: {experiment.minimum_detectable_effect * 100}%
- Sample Size (per variant): {experiment.sample_size_per_variant}
- Tests: Two-sample t-test (continuous), Two-proportion z-test (binary)

**Interpretation**:
- p < 0.05: Statistically significant
- Cohen's d: Effect size (0.2 = small, 0.5 = medium, 0.8 = large)

---

**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
"""

        return report

    def _get_experiment(self, experiment_id: str) -> Optional[ExperimentDesign]:
        """Get experiment by ID"""
        for experiment in self.experiments:
            if experiment.experiment_id == experiment_id:
                return experiment
        return None


if __name__ == "__main__":
    # Example usage
    engine = ExperimentEngine()

    # Create experiment
    print("=== Creating Experiment ===")
    experiment = engine.create_experiment(
        name="Video vs. Text Learning",
        hypothesis="Adding instructional videos improves assessment scores",
        variants=["control_text_only", "treatment_with_video"],
        metrics=["assessment_score", "completion_rate", "time_on_task"],
        metric_types={
            "assessment_score": "continuous",
            "completion_rate": "binary",
            "time_on_task": "continuous"
        },
        duration_days=14,
        minimum_detectable_effect=0.10
    )

    print(f"Experiment ID: {experiment.experiment_id}")
    print(f"Sample size needed (per variant): {experiment.sample_size_per_variant}")

    # Generate mock data
    print("\n=== Generating Mock Data ===")
    np.random.seed(42)
    n_control = 300
    n_treatment = 300

    data = pd.DataFrame({
        "variant": ["control_text_only"] * n_control + ["treatment_with_video"] * n_treatment,
        "student_id": range(n_control + n_treatment),
        "assessment_score": (
            list(np.random.normal(75, 10, n_control)) +  # Control: mean=75
            list(np.random.normal(80, 10, n_treatment))  # Treatment: mean=80 (5-point improvement)
        ),
        "completion_rate": (
            list(np.random.binomial(1, 0.70, n_control)) +  # Control: 70%
            list(np.random.binomial(1, 0.80, n_treatment))  # Treatment: 80%
        ),
        "time_on_task": (
            list(np.random.normal(25, 5, n_control)) +  # Control: 25 min
            list(np.random.normal(23, 5, n_treatment))  # Treatment: 23 min (faster)
        )
    })

    print(f"Generated data: {len(data)} participants")

    # Analyze experiment
    print("\n=== Analyzing Experiment ===")
    results = engine.analyze_experiment(experiment.experiment_id, data)

    print(f"Winner: {results.winner or 'No clear winner'}")
    print(f"Confidence: {results.confidence * 100:.1f}%")
    print(f"Recommendations: {len(results.recommendations)}")

    # Generate report
    print("\n=== Experiment Report ===")
    report = engine.generate_report(results)
    print(report[:1000] + "...")
