#!/usr/bin/env python3
"""
Curriculum Develop Content Skill

Create detailed lesson plans, instructional materials, learning activities,
and differentiation strategies aligned to learning objectives.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from skill_base import Skill, SkillParameter, register_skill


class CurriculumDevelopContentSkill(Skill):
    """Develop instructional content and lesson plans"""

    def __init__(self):
        super().__init__(
            skill_id="curriculum.develop-content",
            skill_name="Curriculum Content Development",
            category="curriculum",
            description="Create lesson plans, materials, and activities aligned to objectives"
        )

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(
                name="objectives",
                param_type=list,
                description="Learning objectives for content",
                required=True
            ),
            SkillParameter(
                name="lesson_title",
                param_type=str,
                description="Lesson title",
                required=True
            ),
            SkillParameter(
                name="duration_minutes",
                param_type=int,
                description="Lesson duration",
                required=False,
                default=45
            ),
            SkillParameter(
                name="educational_level",
                param_type=str,
                description="Educational level",
                required=True
            )
        ]

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute content development"""
        objectives = parameters["objectives"]
        title = parameters["lesson_title"]
        duration = parameters.get("duration_minutes", 45)
        level = parameters["educational_level"]

        # Create lesson plan
        lesson_plan = self._create_lesson_plan(title, objectives, duration, level)

        # Develop activities
        activities = self._develop_learning_activities(objectives, duration, level)

        # Create differentiation strategies
        differentiation = self._create_differentiation_strategies(objectives, level)

        # Design instructional materials
        materials = self._design_instructional_materials(objectives, level)

        return {
            "data": {
                "lesson_plan": lesson_plan,
                "activities": activities,
                "differentiation_strategies": differentiation,
                "instructional_materials": materials,
                "lesson_title": title,
                "duration_minutes": duration
            },
            "artifacts": [
                f"{title.replace(' ', '_')}_lesson_plan.md",
                f"{title.replace(' ', '_')}_activities.md",
                f"{title.replace(' ', '_')}_materials_list.md"
            ]
        }

    def _create_lesson_plan(
        self,
        title: str,
        objectives: List[str],
        duration: int,
        level: str
    ) -> Dict[str, Any]:
        """Create detailed lesson plan using 5E model"""
        # Allocate time across 5E phases
        engage_time = int(duration * 0.15)
        explore_time = int(duration * 0.25)
        explain_time = int(duration * 0.25)
        elaborate_time = int(duration * 0.20)
        evaluate_time = int(duration * 0.15)

        return {
            "title": title,
            "objectives": objectives,
            "duration": duration,
            "educational_level": level,
            "instructional_model": "5E Model",
            "phases": {
                "engage": {
                    "duration_minutes": engage_time,
                    "purpose": "Hook students and activate prior knowledge",
                    "activities": [
                        "Present real-world scenario or intriguing question",
                        "Elicit predictions or initial thinking",
                        "Connect to prior learning"
                    ],
                    "teacher_actions": [
                        "Pose engaging question",
                        "Facilitate brief discussion",
                        "Listen for prior knowledge"
                    ],
                    "student_actions": [
                        "Respond to hook",
                        "Share initial ideas",
                        "Make connections to experience"
                    ]
                },
                "explore": {
                    "duration_minutes": explore_time,
                    "purpose": "Hands-on investigation and discovery",
                    "activities": [
                        "Guided inquiry activity",
                        "Manipulative exploration or simulation",
                        "Data collection and observation"
                    ],
                    "teacher_actions": [
                        "Set up exploration",
                        "Circulate and observe",
                        "Ask probing questions"
                    ],
                    "student_actions": [
                        "Investigate actively",
                        "Collaborate with peers",
                        "Record observations"
                    ]
                },
                "explain": {
                    "duration_minutes": explain_time,
                    "purpose": "Formalize understanding and introduce terminology",
                    "activities": [
                        "Direct instruction on key concepts",
                        "Worked examples and modeling",
                        "Vocabulary introduction",
                        "Concept mapping or graphic organizers"
                    ],
                    "teacher_actions": [
                        "Provide clear explanations",
                        "Model problem-solving process",
                        "Check for understanding"
                    ],
                    "student_actions": [
                        "Take notes",
                        "Ask clarifying questions",
                        "Practice with guidance"
                    ]
                },
                "elaborate": {
                    "duration_minutes": elaborate_time,
                    "purpose": "Apply learning to new contexts",
                    "activities": [
                        "Independent practice problems",
                        "Application to novel situations",
                        "Extension challenges"
                    ],
                    "teacher_actions": [
                        "Provide varied practice",
                        "Offer differentiated tasks",
                        "Give targeted feedback"
                    ],
                    "student_actions": [
                        "Apply concepts independently",
                        "Solve varied problems",
                        "Extend thinking"
                    ]
                },
                "evaluate": {
                    "duration_minutes": evaluate_time,
                    "purpose": "Assess learning and provide feedback",
                    "activities": [
                        "Exit ticket or formative assessment",
                        "Self-assessment against objectives",
                        "Preview next lesson"
                    ],
                    "teacher_actions": [
                        "Administer assessment",
                        "Provide feedback",
                        "Plan differentiation for next lesson"
                    ],
                    "student_actions": [
                        "Demonstrate learning",
                        "Reflect on progress",
                        "Identify questions"
                    ]
                }
            },
            "materials_needed": [
                "Presentation slides or anchor charts",
                "Student handouts and worksheets",
                "Manipulatives or digital tools",
                "Assessment materials"
            ],
            "preparation": [
                "Review objectives and standards alignment",
                "Prepare all materials in advance",
                "Set up technology and test functionality",
                "Review differentiation strategies"
            ]
        }

    def _develop_learning_activities(
        self,
        objectives: List[str],
        duration: int,
        level: str
    ) -> List[Dict[str, Any]]:
        """Develop varied learning activities"""
        activities = []

        # Activity types based on level
        activity_types = {
            "K-5": [
                ("Hands-on Exploration", "Manipulatives and concrete materials"),
                ("Interactive Game", "Learning through play and engagement"),
                ("Think-Pair-Share", "Collaborative discussion"),
                ("Graphic Organizer", "Visual representation of concepts")
            ],
            "6-8": [
                ("Problem-Based Learning", "Solve authentic problems"),
                ("Jigsaw Activity", "Collaborative expert groups"),
                ("Data Analysis", "Interpret graphs and tables"),
                ("Simulation", "Model real-world scenarios")
            ],
            "9-12": [
                ("Case Study Analysis", "Apply concepts to real cases"),
                ("Debate", "Argue multiple perspectives"),
                ("Research Project", "Independent investigation"),
                ("Presentation", "Communicate findings")
            ]
        }

        # Select appropriate activities
        level_activities = activity_types.get(level, activity_types["6-8"])

        for i, (activity_type, description) in enumerate(level_activities[:3], 1):
            activity = {
                "activity_id": f"ACT-{i:02d}",
                "type": activity_type,
                "description": description,
                "objectives_addressed": objectives[:2] if i == 1 else objectives[2:],
                "duration_minutes": duration // 3,
                "grouping": "Pairs" if "Pair" in activity_type else "Individual",
                "materials": ["Activity handout", "Supporting resources"],
                "instructions": [
                    f"1. Introduce {activity_type} purpose and process",
                    "2. Model expectations and provide examples",
                    "3. Monitor and support during activity",
                    "4. Debrief and connect to learning objectives"
                ],
                "differentiation": [
                    "Scaffold: Provide sentence frames or step-by-step guide",
                    "Challenge: Add complexity or extension questions",
                    "Support: Pair with peer buddy or provide one-on-one assistance"
                ]
            }
            activities.append(activity)

        return activities

    def _create_differentiation_strategies(
        self,
        objectives: List[str],
        level: str
    ) -> Dict[str, Any]:
        """Create differentiation strategies for diverse learners"""
        return {
            "by_readiness": {
                "approaching_grade_level": {
                    "strategies": [
                        "Pre-teach vocabulary and key concepts",
                        "Provide graphic organizers and visual aids",
                        "Chunk content into smaller segments",
                        "Offer extended time and reduced complexity",
                        "Use concrete examples before abstract"
                    ],
                    "supports": [
                        "Sentence frames and word banks",
                        "Step-by-step instructions with visuals",
                        "Partner with on-grade-level peer",
                        "Frequent check-ins and feedback"
                    ]
                },
                "on_grade_level": {
                    "strategies": [
                        "Standard instruction with varied practice",
                        "Mix of collaborative and independent work",
                        "Formative assessment to guide instruction",
                        "Balance of support and challenge"
                    ]
                },
                "above_grade_level": {
                    "strategies": [
                        "Open-ended extension questions",
                        "Independent research opportunities",
                        "Leadership roles in group work",
                        "Abstract and complex applications",
                        "Mentoring other students"
                    ],
                    "enrichment": [
                        "Explore related advanced topics",
                        "Create original products or presentations",
                        "Connect to real-world professions",
                        "Pursue passion projects"
                    ]
                }
            },
            "by_learning_profile": {
                "visual_learners": [
                    "Diagrams, charts, and graphic organizers",
                    "Color coding and highlighting",
                    "Videos and image-rich resources",
                    "Mind mapping and sketch-noting"
                ],
                "auditory_learners": [
                    "Think-pair-share discussions",
                    "Podcasts and audio resources",
                    "Read-aloud and verbal explanations",
                    "Mnemonic devices and rhymes"
                ],
                "kinesthetic_learners": [
                    "Hands-on manipulatives",
                    "Movement breaks and activity-based learning",
                    "Role-playing and simulations",
                    "Building and creating physical models"
                ]
            },
            "by_interest": {
                "choice_boards": "Multiple pathways to demonstrate learning",
                "interest_surveys": "Connect content to student interests",
                "real_world_connections": "Career and application focus",
                "student_selected_topics": "Voice and choice in assignments"
            },
            "language_support": {
                "english_learners": [
                    "Visual vocabulary with images",
                    "Sentence frames and language scaffolds",
                    "Preview/review in native language",
                    "Extended time for language processing",
                    "Gestures and non-verbal communication"
                ],
                "native_language_support": [
                    "Bilingual glossaries",
                    "Peer translation support",
                    "Dual-language resources when available"
                ]
            },
            "accessibility": {
                "accommodations": [
                    "Text-to-speech for reading materials",
                    "Speech-to-text for writing tasks",
                    "Enlarged print or digital zoom",
                    "Extended time on assessments",
                    "Preferential seating"
                ],
                "modifications": [
                    "Reduced number of problems (same complexity)",
                    "Alternate response formats",
                    "Modified assessment criteria"
                ]
            }
        }

    def _design_instructional_materials(
        self,
        objectives: List[str],
        level: str
    ) -> Dict[str, Any]:
        """Design instructional materials list"""
        return {
            "core_materials": [
                {
                    "type": "Presentation",
                    "description": "Slide deck with key concepts and examples",
                    "components": ["Learning objectives", "Hook/Engage", "Direct instruction", "Worked examples", "Practice problems"]
                },
                {
                    "type": "Student Handout",
                    "description": "Guided notes and practice worksheet",
                    "components": ["Key vocabulary", "Note-taking scaffolds", "Practice problems", "Exit ticket"]
                },
                {
                    "type": "Teacher Guide",
                    "description": "Facilitation notes and answer key",
                    "components": ["Timing guide", "Discussion prompts", "Common misconceptions", "Answer key with explanations"]
                }
            ],
            "manipulatives_tools": [
                "Physical manipulatives (if applicable)",
                "Digital tools or simulations",
                "Graphic organizers",
                "Reference sheets"
            ],
            "assessment_materials": [
                "Formative assessment questions",
                "Exit ticket template",
                "Self-assessment checklist",
                "Rubric for performance tasks"
            ],
            "differentiation_materials": [
                "Scaffolded worksheet for approaching",
                "Extension activities for advanced",
                "Language support resources",
                "Alternative representations"
            ],
            "technology_integration": [
                "Interactive digital activities",
                "Online practice platforms",
                "Collaborative tools (shared docs, discussion boards)",
                "Assessment technology"
            ]
        }


# Register skill
skill_instance = CurriculumDevelopContentSkill()
register_skill(skill_instance)


if __name__ == "__main__":
    import asyncio
    import json

    async def test():
        skill = CurriculumDevelopContentSkill()

        result = await skill.run({
            "objectives": ["OBJ-001", "OBJ-002", "OBJ-003"],
            "lesson_title": "Introduction to Quadratic Equations",
            "duration_minutes": 50,
            "educational_level": "9-12"
        })

        print("=== Curriculum Develop Content Skill Test ===")
        print(f"Status: {result.status}")
        print(f"\nLesson Plan Structure:")
        for phase, details in result.output["data"]["lesson_plan"]["phases"].items():
            print(f"  {phase.capitalize()}: {details['duration_minutes']} min - {details['purpose']}")

        print(f"\nActivities: {len(result.output['data']['activities'])}")
        print(f"Differentiation Strategies: {len(result.output['data']['differentiation_strategies'])} categories")

    asyncio.run(test())
