#!/usr/bin/env python3
"""
Professor Decision Framework

Provides decision-making utilities for agents to make pedagogical choices based on
educational theory, learning science, and project context.

Usage:
    from decision_framework import DecisionFramework, LearningTheory

    df = DecisionFramework(educational_level="9-12", subject="biology")
    model = df.select_instructional_model(duration_weeks=6, complexity="high")
    activities = df.recommend_activities(objective="analyze", bloom_level=4)
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


class LearningTheory(Enum):
    """Learning theories"""
    BEHAVIORISM = "behaviorism"
    COGNITIVISM = "cognitivism"
    CONSTRUCTIVISM = "constructivism"
    SOCIAL_CONSTRUCTIVISM = "social_constructivism"
    CONNECTIVISM = "connectivism"


class InstructionalModel(Enum):
    """Instructional design models"""
    ADDIE = "addie"  # Analysis, Design, Development, Implementation, Evaluation
    SAM = "sam"  # Successive Approximation Model (iterative)
    BACKWARD_DESIGN = "backward_design"  # Start with outcomes
    AGILE = "agile"  # Sprint-based iterative
    DICK_AND_CAREY = "dick_and_carey"  # Systems approach


class BloomLevel(Enum):
    """Bloom's Taxonomy cognitive levels"""
    REMEMBER = 1
    UNDERSTAND = 2
    APPLY = 3
    ANALYZE = 4
    EVALUATE = 5
    CREATE = 6


@dataclass
class DecisionCriteria:
    """Criteria for making pedagogical decisions"""
    educational_level: str  # K-5, 6-8, 9-12, undergraduate, etc.
    subject: str
    duration_weeks: int
    learner_count: Optional[int] = None
    budget: str = "medium"  # low, medium, high
    timeline_urgency: str = "normal"  # relaxed, normal, urgent
    accessibility_requirements: str = "WCAG-2.1-AA"
    engagement_priority: str = "medium"  # low, medium, high


class DecisionFramework:
    """Makes pedagogical decisions based on context"""

    def __init__(self, educational_level: str, subject: str):
        """
        Initialize decision framework

        Args:
            educational_level: K-5, 6-8, 9-12, undergraduate, graduate, post-graduate, professional
            subject: Subject area (mathematics, science, ela, social-studies, etc.)
        """
        self.educational_level = educational_level
        self.subject = subject

    def select_instructional_model(
        self,
        duration_weeks: int,
        complexity: str = "medium",
        timeline_urgency: str = "normal"
    ) -> Dict[str, Any]:
        """
        Select appropriate instructional design model

        Args:
            duration_weeks: Project duration in weeks
            complexity: Project complexity (low, medium, high)
            timeline_urgency: Timeline urgency (relaxed, normal, urgent)

        Returns:
            Dict with model selection and rationale
        """
        # Decision logic
        if timeline_urgency == "urgent" or duration_weeks < 4:
            model = InstructionalModel.SAM
            rationale = "SAM chosen for rapid iterative development suitable for short timeline"

        elif complexity == "high" and duration_weeks >= 12:
            model = InstructionalModel.ADDIE
            rationale = "ADDIE chosen for systematic approach needed for complex project"

        elif self.educational_level in ["undergraduate", "graduate", "post-graduate"]:
            model = InstructionalModel.BACKWARD_DESIGN
            rationale = "Backward Design chosen for outcome-focused higher education context"

        elif duration_weeks >= 8 and timeline_urgency == "normal":
            model = InstructionalModel.AGILE
            rationale = "Agile chosen for flexible, sprint-based development with regular stakeholder feedback"

        else:
            model = InstructionalModel.BACKWARD_DESIGN
            rationale = "Backward Design chosen as default evidence-based approach"

        return {
            "model": model.value,
            "rationale": rationale,
            "phases": self._get_model_phases(model),
            "recommended_sprint_weeks": 2 if model == InstructionalModel.AGILE else duration_weeks // 4
        }

    def _get_model_phases(self, model: InstructionalModel) -> List[str]:
        """Get phases for each instructional model"""
        phases_map = {
            InstructionalModel.ADDIE: [
                "Analysis", "Design", "Development", "Implementation", "Evaluation"
            ],
            InstructionalModel.SAM: [
                "Preparation", "Iterative Design (3 cycles)", "Iterative Development"
            ],
            InstructionalModel.BACKWARD_DESIGN: [
                "Identify Desired Results", "Determine Assessment Evidence", "Plan Learning Experiences"
            ],
            InstructionalModel.AGILE: [
                "Sprint 1", "Sprint 2", "Sprint 3", "Sprint N", "Release"
            ],
            InstructionalModel.DICK_AND_CAREY: [
                "Identify Goals", "Conduct Analysis", "Identify Entry Behaviors",
                "Write Performance Objectives", "Develop Assessment", "Develop Strategy",
                "Develop Materials", "Formative Evaluation", "Revise", "Summative Evaluation"
            ]
        }
        return phases_map.get(model, [])

    def select_learning_theory(
        self,
        learning_goals: List[str],
        age_group: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Select appropriate learning theory for goals

        Args:
            learning_goals: List of learning goal descriptions
            age_group: Optional age group override

        Returns:
            Dict with theory selection and rationale
        """
        age_group = age_group or self.educational_level

        # K-5: Typically constructivist with social elements
        if age_group == "K-5":
            theory = LearningTheory.CONSTRUCTIVISM
            rationale = "Constructivism supports active learning appropriate for elementary learners"

        # 6-8: Social constructivism for collaborative learning
        elif age_group == "6-8":
            theory = LearningTheory.SOCIAL_CONSTRUCTIVISM
            rationale = "Social constructivism leverages peer interaction critical for middle school"

        # 9-12: Mix of cognitivism and constructivism
        elif age_group == "9-12":
            # Check if goals emphasize problem-solving
            if any(word in " ".join(learning_goals).lower() for word in ["solve", "analyze", "create", "design"]):
                theory = LearningTheory.CONSTRUCTIVISM
                rationale = "Constructivism supports complex problem-solving in high school"
            else:
                theory = LearningTheory.COGNITIVISM
                rationale = "Cognitivism emphasizes information processing suitable for high school"

        # Higher ed: Constructivism or connectivism
        elif age_group in ["undergraduate", "graduate", "post-graduate"]:
            if self.subject in ["computer-science", "data-science", "information-technology"]:
                theory = LearningTheory.CONNECTIVISM
                rationale = "Connectivism emphasizes networked learning ideal for technology fields"
            else:
                theory = LearningTheory.CONSTRUCTIVISM
                rationale = "Constructivism supports self-directed learning in higher education"

        # Professional: Connectivism or social constructivism
        else:
            theory = LearningTheory.SOCIAL_CONSTRUCTIVISM
            rationale = "Social constructivism supports collaborative professional learning"

        return {
            "theory": theory.value,
            "rationale": rationale,
            "instructional_strategies": self._get_theory_strategies(theory)
        }

    def _get_theory_strategies(self, theory: LearningTheory) -> List[str]:
        """Get instructional strategies for each theory"""
        strategies_map = {
            LearningTheory.BEHAVIORISM: [
                "Direct instruction", "Drill and practice", "Reinforcement",
                "Clear objectives", "Immediate feedback"
            ],
            LearningTheory.COGNITIVISM: [
                "Scaffolding", "Worked examples", "Schema activation",
                "Chunking information", "Metacognitive prompts"
            ],
            LearningTheory.CONSTRUCTIVISM: [
                "Problem-based learning", "Inquiry-based learning", "Discovery learning",
                "Authentic tasks", "Reflection activities"
            ],
            LearningTheory.SOCIAL_CONSTRUCTIVISM: [
                "Collaborative projects", "Peer review", "Discussion forums",
                "Think-pair-share", "Jigsaw activities"
            ],
            LearningTheory.CONNECTIVISM: [
                "Network building", "Curating resources", "Community of practice",
                "Social media integration", "Distributed cognition"
            ]
        }
        return strategies_map.get(theory, [])

    def recommend_activities(
        self,
        objective: str,
        bloom_level: int,
        duration_minutes: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Recommend learning activities for an objective

        Args:
            objective: Learning objective description
            bloom_level: Bloom's Taxonomy level (1-6)
            duration_minutes: Optional activity duration

        Returns:
            List of recommended activities with details
        """
        activities = []

        # Lower order thinking (1-3)
        if bloom_level <= 3:
            if bloom_level == 1:  # Remember
                activities.extend([
                    {"type": "Flashcards", "engagement": "low", "complexity": "low"},
                    {"type": "Practice Quiz", "engagement": "medium", "complexity": "low"},
                    {"type": "Matching Exercise", "engagement": "medium", "complexity": "low"}
                ])
            elif bloom_level == 2:  # Understand
                activities.extend([
                    {"type": "Concept Mapping", "engagement": "medium", "complexity": "medium"},
                    {"type": "Summarization", "engagement": "medium", "complexity": "medium"},
                    {"type": "Think-Pair-Share", "engagement": "high", "complexity": "medium"}
                ])
            elif bloom_level == 3:  # Apply
                activities.extend([
                    {"type": "Worked Problems", "engagement": "medium", "complexity": "medium"},
                    {"type": "Simulation", "engagement": "high", "complexity": "medium"},
                    {"type": "Case Study", "engagement": "high", "complexity": "medium"}
                ])

        # Higher order thinking (4-6)
        else:
            if bloom_level == 4:  # Analyze
                activities.extend([
                    {"type": "Compare/Contrast", "engagement": "medium", "complexity": "high"},
                    {"type": "Categorization Task", "engagement": "medium", "complexity": "high"},
                    {"type": "Data Analysis", "engagement": "high", "complexity": "high"}
                ])
            elif bloom_level == 5:  # Evaluate
                activities.extend([
                    {"type": "Peer Review", "engagement": "high", "complexity": "high"},
                    {"type": "Debate", "engagement": "high", "complexity": "high"},
                    {"type": "Critique Task", "engagement": "high", "complexity": "high"}
                ])
            elif bloom_level == 6:  # Create
                activities.extend([
                    {"type": "Project-Based Learning", "engagement": "very-high", "complexity": "very-high"},
                    {"type": "Design Challenge", "engagement": "very-high", "complexity": "very-high"},
                    {"type": "Research Project", "engagement": "very-high", "complexity": "very-high"}
                ])

        # Add recommended durations
        duration_map = {
            "low": 10, "medium": 20, "high": 30, "very-high": 60
        }

        for activity in activities:
            if duration_minutes:
                activity["duration_minutes"] = duration_minutes
            else:
                activity["duration_minutes"] = duration_map.get(activity["complexity"], 20)
            activity["bloom_level"] = bloom_level

        return activities

    def select_assessment_types(
        self,
        bloom_level: int,
        purpose: str = "formative"
    ) -> List[Dict[str, Any]]:
        """
        Recommend assessment types for objectives

        Args:
            bloom_level: Bloom's Taxonomy level (1-6)
            purpose: Assessment purpose (formative, summative, diagnostic)

        Returns:
            List of recommended assessment types
        """
        assessments = []

        if purpose == "diagnostic":
            assessments = [
                {"type": "Pre-test", "when": "Before instruction"},
                {"type": "Concept Inventory", "when": "Before instruction"},
                {"type": "Self-Assessment", "when": "Before instruction"}
            ]

        elif purpose == "formative":
            if bloom_level <= 2:
                assessments = [
                    {"type": "Quick Quiz", "frequency": "After each section"},
                    {"type": "Exit Ticket", "frequency": "End of lesson"},
                    {"type": "Clicker Questions", "frequency": "During lesson"}
                ]
            elif bloom_level <= 4:
                assessments = [
                    {"type": "Problem Set", "frequency": "Weekly"},
                    {"type": "Lab Report Draft", "frequency": "Mid-unit"},
                    {"type": "Peer Feedback", "frequency": "During project"}
                ]
            else:  # 5-6
                assessments = [
                    {"type": "Project Milestone", "frequency": "Bi-weekly"},
                    {"type": "Presentation Draft", "frequency": "Mid-project"},
                    {"type": "Portfolio Review", "frequency": "Monthly"}
                ]

        else:  # summative
            if bloom_level <= 3:
                assessments = [
                    {"type": "Unit Test", "weight": "High"},
                    {"type": "Final Exam", "weight": "Very High"}
                ]
            elif bloom_level <= 4:
                assessments = [
                    {"type": "Research Paper", "weight": "High"},
                    {"type": "Comprehensive Lab", "weight": "High"}
                ]
            else:  # 5-6
                assessments = [
                    {"type": "Capstone Project", "weight": "Very High"},
                    {"type": "Portfolio", "weight": "Very High"},
                    {"type": "Presentation + Defense", "weight": "High"}
                ]

        for assessment in assessments:
            assessment["bloom_level"] = bloom_level
            assessment["purpose"] = purpose

        return assessments

    def calculate_cognitive_load(
        self,
        content_complexity: str,
        prior_knowledge: str,
        multimedia_elements: int
    ) -> Dict[str, Any]:
        """
        Estimate cognitive load and recommend adjustments

        Args:
            content_complexity: low, medium, high
            prior_knowledge: novice, intermediate, advanced
            multimedia_elements: Number of multimedia elements

        Returns:
            Cognitive load analysis and recommendations
        """
        # Simplified cognitive load calculation
        complexity_score = {"low": 1, "medium": 2, "high": 3}.get(content_complexity, 2)
        prior_score = {"novice": 3, "intermediate": 2, "advanced": 1}.get(prior_knowledge, 2)
        multimedia_score = min(multimedia_elements / 3, 2)  # Cap at 2

        total_load = complexity_score + prior_score + multimedia_score

        if total_load <= 3:
            load_level = "low"
            recommendation = "Appropriate cognitive load. Consider adding challenge."
        elif total_load <= 5:
            load_level = "medium"
            recommendation = "Appropriate cognitive load for most learners."
        elif total_load <= 7:
            load_level = "high"
            recommendation = "High cognitive load. Add scaffolding and worked examples."
        else:
            load_level = "very-high"
            recommendation = "Excessive cognitive load. Chunk content and add significant scaffolding."

        return {
            "load_level": load_level,
            "load_score": total_load,
            "recommendation": recommendation,
            "suggested_scaffolds": self._get_scaffolds(load_level)
        }

    def _get_scaffolds(self, load_level: str) -> List[str]:
        """Get recommended scaffolds for cognitive load level"""
        if load_level in ["high", "very-high"]:
            return [
                "Worked examples",
                "Advance organizers",
                "Chunking strategies",
                "Glossary of terms",
                "Step-by-step guides",
                "Visual aids and diagrams"
            ]
        elif load_level == "medium":
            return [
                "Occasional worked examples",
                "Key term definitions",
                "Practice problems"
            ]
        else:
            return ["Optional extension activities"]


if __name__ == "__main__":
    # Example usage
    df = DecisionFramework(educational_level="9-12", subject="biology")

    # Select instructional model
    model_decision = df.select_instructional_model(duration_weeks=6, complexity="medium")
    print("=== Instructional Model ===")
    print(f"Model: {model_decision['model']}")
    print(f"Rationale: {model_decision['rationale']}")
    print(f"Phases: {', '.join(model_decision['phases'])}")

    # Select learning theory
    theory_decision = df.select_learning_theory(
        learning_goals=["Analyze genetic inheritance patterns", "Design experiments"]
    )
    print("\n=== Learning Theory ===")
    print(f"Theory: {theory_decision['theory']}")
    print(f"Rationale: {theory_decision['rationale']}")
    print(f"Strategies: {', '.join(theory_decision['instructional_strategies'][:3])}")

    # Recommend activities
    activities = df.recommend_activities(objective="Analyze data", bloom_level=4, duration_minutes=30)
    print("\n=== Recommended Activities (Analyze Level) ===")
    for activity in activities[:3]:
        print(f"- {activity['type']}: {activity['duration_minutes']} min (engagement: {activity['engagement']})")

    # Cognitive load
    load = df.calculate_cognitive_load(
        content_complexity="high",
        prior_knowledge="novice",
        multimedia_elements=5
    )
    print("\n=== Cognitive Load Analysis ===")
    print(f"Load Level: {load['load_level']} (score: {load['load_score']})")
    print(f"Recommendation: {load['recommendation']}")
