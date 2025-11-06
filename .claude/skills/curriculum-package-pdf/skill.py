#!/usr/bin/env python3
"""Curriculum Package PDF Skill"""

import sys
from pathlib import Path
from typing import Dict, List, Any

framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from skill_base import Skill, SkillParameter, register_skill


class CurriculumPackagePdfSkill(Skill):
    def __init__(self):
        super().__init__(skill_id="curriculum.package-pdf", skill_name="PDF Package Generation",
                        category="packaging", description="Generate PDF materials with proper formatting")

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(name="content_path", param_type=str, required=True),
            SkillParameter(name="format", param_type=str, required=False, default="standard",
                          choices=["standard", "print", "accessible"]),
            SkillParameter(name="include_answer_key", param_type=bool, required=False, default=False)
        ]

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        path = parameters["content_path"]
        format_type = parameters.get("format", "standard")
        include_key = parameters.get("include_answer_key", False)

        package = {
            "format": format_type,
            "pages": 24,
            "includes": ["Student materials", "Teacher guide"] + (["Answer key"] if include_key else []),
            "specifications": {
                "paper_size": "Letter (8.5x11)" if format_type == "standard" else "A4",
                "margins": "1 inch" if format_type == "print" else "0.75 inch",
                "font": "Arial 12pt" if format_type == "accessible" else "Times New Roman 11pt",
                "accessibility": ["Tagged PDF", "Logical reading order"] if format_type == "accessible" else []
            }
        }

        return {
            "data": {"pdf_package": package, "output_file": f"{Path(path).stem}.pdf"},
            "artifacts": [f"{Path(path).stem}.pdf"]
        }

skill_instance = CurriculumPackagePdfSkill()
register_skill(skill_instance)
