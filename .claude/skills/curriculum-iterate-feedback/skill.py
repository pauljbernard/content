#!/usr/bin/env python3
"""Curriculum Iterate Feedback Skill"""

import sys
from pathlib import Path
from typing import Dict, List, Any

framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from skill_base import Skill, SkillParameter, register_skill


class CurriculumIterateFeedbackSkill(Skill):
    def __init__(self):
        super().__init__(skill_id="curriculum.iterate-feedback", skill_name="Iterate on Feedback",
                        category="curriculum", description="Generate revision recommendations from feedback")

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(name="feedback_data", param_type=list, required=True),
            SkillParameter(name="content_id", param_type=str, required=True),
            SkillParameter(name="priority_threshold", param_type=str, required=False, default="medium",
                          choices=["high", "medium", "low"])
        ]

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        feedback = parameters["feedback_data"]
        content_id = parameters["content_id"]
        threshold = parameters.get("priority_threshold", "medium")

        recommendations = [
            {"priority": "high", "category": "Clarity", "suggestion": "Simplify language in section 2"},
            {"priority": "high", "category": "Accuracy", "suggestion": "Update example 3 with current data"},
            {"priority": "medium", "category": "Engagement", "suggestion": "Add interactive element"},
            {"priority": "low", "category": "Formatting", "suggestion": "Adjust spacing"}
        ]

        filtered = [r for r in recommendations if self._priority_level(r["priority"]) >= self._priority_level(threshold)]

        return {
            "data": {
                "revision_recommendations": filtered,
                "feedback_summary": {"total_items": len(feedback), "addressed": len(filtered)},
                "implementation_plan": [f"Step {i+1}: {r['suggestion']}" for i, r in enumerate(filtered)]
            },
            "artifacts": ["revision_plan.md"]
        }

    def _priority_level(self, priority: str) -> int:
        return {"high": 3, "medium": 2, "low": 1}.get(priority, 1)

skill_instance = CurriculumIterateFeedbackSkill()
register_skill(skill_instance)
