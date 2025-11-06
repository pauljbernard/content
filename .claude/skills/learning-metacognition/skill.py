#!/usr/bin/env python3
"""LearningMetacognitionSkill"""
import sys
from pathlib import Path
from typing import Dict, List, Any
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))
from skill_base import Skill, SkillParameter, register_skill

class LearningMetacognitionSkill(Skill):
    def __init__(self):
        super().__init__(skill_id="learning.metacognition", skill_name="learning-metacognition", category="learning",
                        description="learning.metacognition skill for learning experience design")

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(name="topic", param_type=str, required=True),
            SkillParameter(name="educational_level", param_type=str, required=True),
            SkillParameter(name="options", param_type=dict, required=False, default={})
        ]

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        topic = parameters["topic"]
        level = parameters["educational_level"]
        options = parameters.get("options", {})
        result = {
            "skill": "learning.metacognition",
            "topic": topic,
            "level": level,
            "deliverable": f"{topic} learning experience created",
            "status": "success"
        }
        return {"data": result, "artifacts": [f"{topic.replace(' ', '_')}_{skill_dir}.json"]}

skill_instance = LearningMetacognitionSkill()
register_skill(skill_instance)
