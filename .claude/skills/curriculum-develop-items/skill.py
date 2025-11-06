#!/usr/bin/env python3
"""
Curriculum Develop Items Skill

Author high-quality assessment items (questions, prompts, tasks) aligned
to learning objectives with answer keys and rubrics.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from skill_base import Skill, SkillParameter, register_skill


class CurriculumDevelopItemsSkill(Skill):
    """Develop assessment items and rubrics"""

    def __init__(self):
        super().__init__(
            skill_id="curriculum.develop-items",
            skill_name="Assessment Item Development",
            category="curriculum",
            description="Create assessment items with answer keys and rubrics"
        )

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(
                name="objectives",
                param_type=list,
                description="Learning objectives to assess",
                required=True
            ),
            SkillParameter(
                name="item_types",
                param_type=list,
                description="Types of items to create",
                required=False,
                default=["multiple_choice", "short_answer", "essay"]
            ),
            SkillParameter(
                name="bloom_levels",
                param_type=list,
                description="Bloom's taxonomy levels to assess",
                required=False,
                default=["Remember", "Understand", "Apply"]
            ),
            SkillParameter(
                name="item_count",
                param_type=int,
                description="Total number of items to generate",
                required=False,
                default=20
            )
        ]

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute item development"""
        objectives = parameters["objectives"]
        item_types = parameters.get("item_types", ["multiple_choice", "short_answer"])
        bloom_levels = parameters.get("bloom_levels", ["Remember", "Understand", "Apply"])
        item_count = parameters.get("item_count", 20)

        # Generate items
        items = self._generate_assessment_items(objectives, item_types, bloom_levels, item_count)

        # Create answer key
        answer_key = self._create_answer_key(items)

        # Generate rubrics for constructed response items
        rubrics = self._generate_rubrics([item for item in items if item["type"] in ["short_answer", "essay", "performance"]])

        return {
            "data": {
                "items": items,
                "answer_key": answer_key,
                "rubrics": rubrics,
                "item_statistics": {
                    "total_items": len(items),
                    "by_type": self._count_by_type(items),
                    "by_bloom": self._count_by_bloom(items)
                }
            },
            "artifacts": [
                "assessment_items.json",
                "answer_key.md",
                "rubrics.md"
            ]
        }

    def _generate_assessment_items(
        self,
        objectives: List[str],
        item_types: List[str],
        bloom_levels: List[str],
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate assessment items"""
        items = []
        items_per_objective = count // len(objectives)

        for obj_idx, objective in enumerate(objectives):
            for i in range(items_per_objective):
                item_num = obj_idx * items_per_objective + i + 1
                item_type = item_types[i % len(item_types)]
                bloom_level = bloom_levels[i % len(bloom_levels)]

                if item_type == "multiple_choice":
                    item = self._create_mc_item(item_num, objective, bloom_level)
                elif item_type == "short_answer":
                    item = self._create_short_answer_item(item_num, objective, bloom_level)
                elif item_type == "essay":
                    item = self._create_essay_item(item_num, objective, bloom_level)
                else:
                    item = self._create_performance_task(item_num, objective, bloom_level)

                items.append(item)

        return items[:count]

    def _create_mc_item(self, num: int, objective: str, bloom: str) -> Dict[str, Any]:
        """Create multiple choice item"""
        return {
            "item_id": f"MC-{num:03d}",
            "type": "multiple_choice",
            "objective": objective,
            "bloom_level": bloom,
            "stem": f"Which of the following best describes [concept from {objective}]?",
            "options": [
                {"key": "A", "text": "Correct answer demonstrating understanding", "correct": True},
                {"key": "B", "text": "Common misconception #1", "correct": False},
                {"key": "C", "text": "Common misconception #2", "correct": False},
                {"key": "D", "text": "Plausible distractor", "correct": False}
            ],
            "correct_answer": "A",
            "rationale": "Option A correctly identifies the key concept",
            "points": 1,
            "estimated_time_seconds": 60
        }

    def _create_short_answer_item(self, num: int, objective: str, bloom: str) -> Dict[str, Any]:
        """Create short answer item"""
        return {
            "item_id": f"SA-{num:03d}",
            "type": "short_answer",
            "objective": objective,
            "bloom_level": bloom,
            "prompt": f"Explain how [concept from {objective}] applies to the given scenario. Provide specific examples.",
            "expected_elements": [
                "Identifies key concept correctly",
                "Explains application with clarity",
                "Provides at least one specific example",
                "Uses appropriate terminology"
            ],
            "sample_response": "A complete response that includes all expected elements...",
            "points": 4,
            "estimated_time_seconds": 180
        }

    def _create_essay_item(self, num: int, objective: str, bloom: str) -> Dict[str, Any]:
        """Create essay item"""
        return {
            "item_id": f"ES-{num:03d}",
            "type": "essay",
            "objective": objective,
            "bloom_level": bloom,
            "prompt": f"Analyze [topic related to {objective}] and evaluate its implications. Support your argument with evidence and reasoning.",
            "criteria": [
                "Clear thesis statement",
                "Well-organized structure",
                "Evidence-based reasoning",
                "Analysis and evaluation",
                "Conclusion with synthesis"
            ],
            "length_requirement": "3-5 paragraphs (400-600 words)",
            "points": 10,
            "estimated_time_seconds": 900
        }

    def _create_performance_task(self, num: int, objective: str, bloom: str) -> Dict[str, Any]:
        """Create performance task"""
        return {
            "item_id": f"PT-{num:03d}",
            "type": "performance",
            "objective": objective,
            "bloom_level": bloom,
            "task_description": f"Complete an authentic task that demonstrates mastery of {objective}",
            "deliverables": [
                "Written plan or proposal",
                "Implementation or product",
                "Reflection on process"
            ],
            "criteria": [
                "Task completion and accuracy",
                "Quality of work product",
                "Application of concepts",
                "Creativity and originality"
            ],
            "points": 20,
            "estimated_time_seconds": 1800
        }

    def _create_answer_key(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create answer key"""
        key = {
            "instructions": "Use this key to score student responses",
            "items": []
        }

        for item in items:
            if item["type"] == "multiple_choice":
                key_entry = {
                    "item_id": item["item_id"],
                    "correct_answer": item["correct_answer"],
                    "points": item["points"],
                    "rationale": item["rationale"]
                }
            else:
                key_entry = {
                    "item_id": item["item_id"],
                    "points": item["points"],
                    "scoring_guide": "See rubric for detailed scoring criteria"
                }

            key["items"].append(key_entry)

        return key

    def _generate_rubrics(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate rubrics for constructed response items"""
        rubrics = []

        for item in items:
            if item["type"] == "short_answer":
                rubric = self._create_short_answer_rubric(item)
            elif item["type"] == "essay":
                rubric = self._create_essay_rubric(item)
            elif item["type"] == "performance":
                rubric = self._create_performance_rubric(item)
            else:
                continue

            rubrics.append(rubric)

        return rubrics

    def _create_short_answer_rubric(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create rubric for short answer"""
        return {
            "item_id": item["item_id"],
            "total_points": item["points"],
            "criteria": [
                {
                    "criterion": "Accuracy",
                    "levels": {
                        "4": "Fully accurate with no errors",
                        "3": "Mostly accurate with minor errors",
                        "2": "Partially accurate with some errors",
                        "1": "Largely inaccurate",
                        "0": "No response or completely incorrect"
                    }
                },
                {
                    "criterion": "Completeness",
                    "levels": {
                        "4": "Addresses all parts thoroughly",
                        "3": "Addresses most parts adequately",
                        "2": "Addresses some parts",
                        "1": "Addresses minimal parts",
                        "0": "Does not address prompt"
                    }
                }
            ]
        }

    def _create_essay_rubric(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create rubric for essay"""
        return {
            "item_id": item["item_id"],
            "total_points": item["points"],
            "criteria": [
                {"criterion": "Thesis/Argument", "weight": 0.25, "max_points": item["points"] * 0.25},
                {"criterion": "Evidence & Support", "weight": 0.30, "max_points": item["points"] * 0.30},
                {"criterion": "Analysis & Reasoning", "weight": 0.25, "max_points": item["points"] * 0.25},
                {"criterion": "Organization & Clarity", "weight": 0.20, "max_points": item["points"] * 0.20}
            ],
            "performance_levels": {
                "4": "Exemplary - Exceeds expectations",
                "3": "Proficient - Meets expectations",
                "2": "Developing - Approaching expectations",
                "1": "Beginning - Below expectations"
            }
        }

    def _create_performance_rubric(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create rubric for performance task"""
        return {
            "item_id": item["item_id"],
            "total_points": item["points"],
            "criteria": [
                {"criterion": "Task Completion", "max_points": item["points"] * 0.30},
                {"criterion": "Quality of Work", "max_points": item["points"] * 0.30},
                {"criterion": "Concept Application", "max_points": item["points"] * 0.25},
                {"criterion": "Creativity & Originality", "max_points": item["points"] * 0.15}
            ]
        }

    def _count_by_type(self, items: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count items by type"""
        counts = {}
        for item in items:
            item_type = item["type"]
            counts[item_type] = counts.get(item_type, 0) + 1
        return counts

    def _count_by_bloom(self, items: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count items by Bloom level"""
        counts = {}
        for item in items:
            bloom = item["bloom_level"]
            counts[bloom] = counts.get(bloom, 0) + 1
        return counts


# Register skill
skill_instance = CurriculumDevelopItemsSkill()
register_skill(skill_instance)


if __name__ == "__main__":
    import asyncio
    import json

    async def test():
        skill = CurriculumDevelopItemsSkill()

        result = await skill.run({
            "objectives": ["OBJ-001", "OBJ-002"],
            "item_types": ["multiple_choice", "short_answer", "essay"],
            "bloom_levels": ["Remember", "Understand", "Apply", "Analyze"],
            "item_count": 12
        })

        print("=== Curriculum Develop Items Skill Test ===")
        print(f"Status: {result.status}")
        print(f"\nGenerated {len(result.output['data']['items'])} items")
        print(f"Item types: {result.output['data']['item_statistics']['by_type']}")
        print(f"Bloom levels: {result.output['data']['item_statistics']['by_bloom']}")
        print(f"Rubrics: {len(result.output['data']['rubrics'])}")

    asyncio.run(test())
