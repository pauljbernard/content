#!/usr/bin/env python3
"""Curriculum Package Web Skill"""

import sys
from pathlib import Path
from typing import Dict, List, Any

framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from skill_base import Skill, SkillParameter, register_skill


class CurriculumPackageWebSkill(Skill):
    def __init__(self):
        super().__init__(skill_id="curriculum.package-web", skill_name="Web Package Generation",
                        category="packaging", description="Generate responsive HTML/CSS/JS content")

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(name="content_path", param_type=str, required=True),
            SkillParameter(name="include_interactive", param_type=bool, required=False, default=True),
            SkillParameter(name="responsive", param_type=bool, required=False, default=True)
        ]

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        path = parameters["content_path"]
        interactive = parameters.get("include_interactive", True)
        responsive = parameters.get("responsive", True)

        package = {
            "format": "HTML5",
            "includes": ["index.html", "styles.css", "script.js"] + (["interactive.js"] if interactive else []),
            "features": ["Responsive design" if responsive else "Fixed width", "Accessibility compliant"],
            "navigation": {"type": "sidebar", "sections": 5},
            "technology_stack": {"html": "5", "css": "3", "javascript": "ES6+"}
        }

        return {
            "data": {"web_package": package, "output_directory": f"{Path(path).stem}_web"},
            "artifacts": [f"{Path(path).stem}_web/index.html"]
        }

skill_instance = CurriculumPackageWebSkill()
register_skill(skill_instance)
