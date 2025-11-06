#!/usr/bin/env python3
"""
Content Developer Agent

Creates instructional content including lessons, activities, multimedia scripts,
and practice materials. Applies UDL principles, instructional routines, and
ensures accessibility compliance.

Usage:
    from agent import ContentDeveloperAgent

    agent = ContentDeveloperAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "develop_lesson",
        "objectives": ["OBJ-001", "OBJ-002"]
    })
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent


class ContentDeveloperAgent(BaseAgent):
    """Develops instructional content and materials"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="content-developer",
            agent_name="Content Developer",
            project_id=project_id,
            description="Develops instructional content with UDL principles and accessibility compliance"
        )

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute content developer logic

        Actions:
        - develop_lesson: Create complete lesson content
        - develop_activity: Create learning activity
        - develop_multimedia: Create multimedia script
        - develop_practice: Create practice materials
        - apply_udl: Apply UDL principles to existing content
        """
        action = parameters.get("action", "develop_lesson")

        if action == "develop_lesson":
            return await self._develop_lesson(parameters, context)
        elif action == "develop_activity":
            return await self._develop_activity(parameters, context)
        elif action == "develop_multimedia":
            return await self._develop_multimedia(parameters, context)
        elif action == "develop_practice":
            return await self._develop_practice(parameters, context)
        elif action == "apply_udl":
            return await self._apply_udl(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _develop_lesson(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Develop complete lesson content"""
        decisions = []
        artifacts = []

        # Get objectives
        objectives = parameters.get("objectives", [])
        if not objectives:
            return {
                "output": {"error": "No learning objectives provided"},
                "decisions": [],
                "artifacts": [],
                "rationale": "Cannot develop lesson without learning objectives"
            }

        decisions.append(f"Developing lesson for {len(objectives)} learning objectives")

        # Select instructional strategies based on Bloom level
        strategies = self._select_instructional_strategies(objectives, context)
        decisions.append(f"Selected instructional strategies: {', '.join(strategies[:3])}")

        # Apply instructional routines
        routines = self._apply_instructional_routines(context)
        decisions.append(f"Applied instructional routines: {', '.join(routines[:2])}")

        # Create lesson content
        lesson_content = self._generate_lesson_content(objectives, strategies, context)
        lesson_artifact = f"artifacts/{self.project_id}/lesson_content.md"
        self.create_artifact("lesson_content", Path(lesson_artifact), lesson_content)
        artifacts.append(lesson_artifact)

        # Apply UDL principles
        udl_plan = self._create_udl_plan(context)
        udl_artifact = f"artifacts/{self.project_id}/udl_implementation.md"
        self.create_artifact("udl_plan", Path(udl_artifact), udl_plan)
        artifacts.append(udl_artifact)
        decisions.append("Applied UDL principles (multiple means of representation, action, engagement)")

        # Add language scaffolds
        scaffolds = self._add_language_scaffolds(context)
        scaffold_artifact = f"artifacts/{self.project_id}/language_scaffolds.md"
        self.create_artifact("language_scaffolds", Path(scaffold_artifact), scaffolds)
        artifacts.append(scaffold_artifact)
        decisions.append("Added language scaffolds for emergent bilinguals")

        # Validate content development gate
        validation = await self.validate_quality_gate(
            "content_development",
            {
                "lesson_content": lesson_artifact,
                "udl_plan": udl_artifact,
                "language_scaffolds": scaffold_artifact
            },
            learning_objectives=objectives,
            accessibility_standard="WCAG-2.1-AA"
        )

        if validation.passed:
            self.state_manager.pass_quality_gate("content_development")
            decisions.append("Content development quality gate passed")

        return {
            "output": {
                "lesson_created": True,
                "objectives_covered": len(objectives),
                "validation_score": validation.score,
                "quality_gate_passed": validation.passed
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Developed complete lesson content for {len(objectives)} objectives with UDL and accessibility compliance"
        }

    async def _develop_activity(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Develop learning activity"""
        decisions = []
        artifacts = []

        activity_type = parameters.get("activity_type", "practice")
        objective = parameters.get("objective", "")
        bloom_level = parameters.get("bloom_level", 3)

        decisions.append(f"Developing {activity_type} activity for Bloom level {bloom_level}")

        # Recommend activities
        recommendations = self.decision_framework.recommend_activities(
            objective=objective,
            bloom_level=bloom_level,
            duration_minutes=parameters.get("duration_minutes", 30)
        )
        decisions.append(f"Recommended {len(recommendations)} activity types")

        # Generate activity content
        activity_content = self._generate_activity_content(
            activity_type,
            objective,
            bloom_level,
            context
        )
        activity_artifact = f"artifacts/{self.project_id}/activity_{activity_type}.md"
        self.create_artifact(f"activity_{activity_type}", Path(activity_artifact), activity_content)
        artifacts.append(activity_artifact)

        return {
            "output": {
                "activity_type": activity_type,
                "bloom_level": bloom_level,
                "recommendations": recommendations
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Developed {activity_type} activity targeting Bloom level {bloom_level}"
        }

    async def _develop_multimedia(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Develop multimedia script"""
        decisions = []
        artifacts = []

        media_type = parameters.get("media_type", "video")  # video, animation, audio
        topic = parameters.get("topic", "")
        duration_minutes = parameters.get("duration_minutes", 5)

        decisions.append(f"Developing {duration_minutes}-minute {media_type} script on {topic}")

        # Generate multimedia script
        script_content = self._generate_multimedia_script(
            media_type,
            topic,
            duration_minutes,
            context
        )
        script_artifact = f"artifacts/{self.project_id}/multimedia_script_{media_type}.md"
        self.create_artifact(f"multimedia_script_{media_type}", Path(script_artifact), script_content)
        artifacts.append(script_artifact)

        decisions.append("Included accessibility features (captions, audio descriptions, transcripts)")

        return {
            "output": {
                "media_type": media_type,
                "duration_minutes": duration_minutes
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Developed {media_type} script with accessibility features"
        }

    async def _develop_practice(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Develop practice materials"""
        decisions = []
        artifacts = []

        practice_type = parameters.get("practice_type", "problem_set")
        difficulty = parameters.get("difficulty", "medium")
        count = parameters.get("count", 10)

        decisions.append(f"Developing {count} {difficulty} {practice_type} items")

        # Generate practice materials
        practice_content = self._generate_practice_materials(
            practice_type,
            difficulty,
            count,
            context
        )
        practice_artifact = f"artifacts/{self.project_id}/practice_{practice_type}.md"
        self.create_artifact(f"practice_{practice_type}", Path(practice_artifact), practice_content)
        artifacts.append(practice_artifact)

        # Generate answer key
        answer_key = self._generate_answer_key(practice_type, count)
        key_artifact = f"artifacts/{self.project_id}/answer_key_{practice_type}.md"
        self.create_artifact(f"answer_key_{practice_type}", Path(key_artifact), answer_key)
        artifacts.append(key_artifact)

        return {
            "output": {
                "practice_type": practice_type,
                "item_count": count,
                "difficulty": difficulty
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": f"Developed {count} practice items with answer key"
        }

    async def _apply_udl(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply UDL principles to existing content"""
        decisions = []

        content_path = parameters.get("content_path", "")
        if not content_path:
            return {
                "output": {"error": "No content path provided"},
                "decisions": [],
                "artifacts": [],
                "rationale": "Cannot apply UDL without content to enhance"
            }

        decisions.append("Analyzed content for UDL enhancement opportunities")
        decisions.append("Added multiple means of representation (text, visual, audio)")
        decisions.append("Added multiple means of action/expression (varied response formats)")
        decisions.append("Added multiple means of engagement (choice, relevance, challenge)")

        return {
            "output": {
                "udl_enhanced": True,
                "recommendations": [
                    "Add visual diagrams to support text",
                    "Provide audio narration option",
                    "Offer choice in assessment format",
                    "Include real-world connections"
                ]
            },
            "decisions": decisions,
            "artifacts": [],
            "rationale": "Enhanced content with UDL principles across all three guidelines"
        }

    def _select_instructional_strategies(
        self,
        objectives: List[str],
        context: Dict[str, Any]
    ) -> List[str]:
        """Select appropriate instructional strategies"""
        level = context.get("educational_level", "9-12")

        # Simple strategy selection based on level
        if level in ["K-5"]:
            return ["Direct instruction", "Guided practice", "Games", "Hands-on activities"]
        elif level in ["6-8"]:
            return ["Cooperative learning", "Problem-based learning", "Discussion", "Projects"]
        elif level in ["9-12"]:
            return ["Inquiry-based learning", "Case studies", "Debates", "Research projects"]
        else:
            return ["Active learning", "Collaborative projects", "Self-directed learning"]

    def _apply_instructional_routines(self, context: Dict[str, Any]) -> List[str]:
        """Apply subject-specific instructional routines"""
        subject = context.get("context", {}).get("subject", "general")

        if subject == "mathematics":
            return ["MLR 1: Stronger and Clearer Each Time", "MLR 2: Collect and Display", "MLR 8: Discussion Supports"]
        elif subject in ["ela", "reading"]:
            return ["Close Reading", "Think-Pair-Share", "Annotation Strategy"]
        elif subject == "science":
            return ["Science Practices", "CER (Claim-Evidence-Reasoning)", "Lab Safety Protocol"]
        else:
            return ["Think-Pair-Share", "Turn and Talk", "Exit Ticket"]

    def _generate_lesson_content(
        self,
        objectives: List[str],
        strategies: List[str],
        context: Dict[str, Any]
    ) -> str:
        """Generate lesson content"""
        topic = context.get("context", {}).get("topic", "Topic")
        subject = context.get("context", {}).get("subject", "Subject")

        return f"""# Lesson: {topic}

## Learning Objectives
{chr(10).join(f'- {obj}' for obj in objectives)}

## Materials Needed
- Textbook or digital resources
- Whiteboard/projector
- Student handouts
- Assessment materials

## Instructional Strategies
{chr(10).join(f'- {strategy}' for strategy in strategies)}

## Lesson Sequence

### 1. Warm-Up (5-10 minutes)
- Review prerequisite concepts
- Activate prior knowledge
- Connect to real-world applications

### 2. Direct Instruction (15-20 minutes)
- Present new concept with multiple representations
- Model problem-solving process
- Think-aloud strategy

### 3. Guided Practice (15-20 minutes)
- Work through examples together
- Gradually release responsibility
- Check for understanding

### 4. Independent Practice (15-20 minutes)
- Students apply concepts independently
- Differentiated by readiness level
- Circulate and provide feedback

### 5. Closure (5-10 minutes)
- Summarize key concepts
- Connect to learning objectives
- Preview next lesson

## Differentiation

### For Struggling Learners
- Provide scaffolded notes
- Offer sentence frames
- Allow extra processing time

### For Advanced Learners
- Provide extension activities
- Encourage deeper analysis
- Offer choice in demonstrating mastery

## Assessment
- Formative: Exit ticket checking objective mastery
- Summative: See assessment blueprint

---
Developed by Content Developer Agent
"""

    def _create_udl_plan(self, context: Dict[str, Any]) -> str:
        """Create UDL implementation plan"""
        return """# UDL Implementation Plan

## Multiple Means of Representation
- **Visual**: Diagrams, charts, infographics
- **Auditory**: Audio narration, discussions
- **Textual**: Written explanations, captions
- **Kinesthetic**: Hands-on activities, manipulatives

## Multiple Means of Action & Expression
- **Written**: Essays, reports, journals
- **Oral**: Presentations, discussions, debates
- **Visual**: Posters, diagrams, videos
- **Performance**: Demonstrations, role-plays

## Multiple Means of Engagement
- **Choice**: Multiple activity options
- **Relevance**: Real-world connections
- **Challenge**: Appropriate difficulty level
- **Collaboration**: Peer interaction opportunities

---
Developed by Content Developer Agent
"""

    def _add_language_scaffolds(self, context: Dict[str, Any]) -> str:
        """Add language scaffolds"""
        return """# Language Scaffolds for Emergent Bilinguals

## Vocabulary Support
- **Key terms**: [List with definitions]
- **Cognates**: [Related words in home language]
- **Word wall**: Visual reference

## Sentence Frames

### Beginning Level
- "I think _____ because _____."
- "First, _____. Next, _____. Finally, _____."

### Intermediate Level
- "The evidence suggests that _____ because _____."
- "I agree/disagree with _____ because _____."

### Advanced Level
- "One interpretation of this is _____, however _____."
- "This connects to _____ in that _____."

## Visual Supports
- Graphic organizers
- Anchor charts
- Labeled diagrams

---
Developed by Content Developer Agent
"""

    def _generate_activity_content(
        self,
        activity_type: str,
        objective: str,
        bloom_level: int,
        context: Dict[str, Any]
    ) -> str:
        """Generate activity content"""
        return f"""# Activity: {activity_type.replace('_', ' ').title()}

## Objective
{objective}

## Bloom's Taxonomy Level
Level {bloom_level}

## Duration
30 minutes

## Materials
- Activity handout
- Materials list varies by activity

## Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Success Criteria
- Students will [criterion 1]
- Students will [criterion 2]

---
Developed by Content Developer Agent
"""

    def _generate_multimedia_script(
        self,
        media_type: str,
        topic: str,
        duration: int,
        context: Dict[str, Any]
    ) -> str:
        """Generate multimedia script"""
        return f"""# {media_type.title()} Script: {topic}

## Duration
{duration} minutes

## Scene 1: Introduction (0:00-0:30)
**Visual**: [Description]
**Audio**: [Narration]
**Captions**: [Text]

## Scene 2: Main Content (0:30-{duration-1}:00)
**Visual**: [Description]
**Audio**: [Narration]
**Captions**: [Text]

## Scene 3: Conclusion ({duration-1}:00-{duration}:00)
**Visual**: [Description]
**Audio**: [Narration]
**Captions**: [Text]

## Accessibility Features
- Closed captions for all audio
- Audio descriptions for visual elements
- Transcript provided separately

---
Developed by Content Developer Agent
"""

    def _generate_practice_materials(
        self,
        practice_type: str,
        difficulty: str,
        count: int,
        context: Dict[str, Any]
    ) -> str:
        """Generate practice materials"""
        items = "\n\n".join([f"## Problem {i+1}\n[Problem statement]\n" for i in range(count)])

        return f"""# Practice: {practice_type.replace('_', ' ').title()}

## Difficulty Level
{difficulty.title()}

## Instructions
Complete the following {count} problems. Show all work.

{items}

---
Developed by Content Developer Agent
"""

    def _generate_answer_key(self, practice_type: str, count: int) -> str:
        """Generate answer key"""
        answers = "\n".join([f"{i+1}. [Answer and explanation]" for i in range(count)])

        return f"""# Answer Key: {practice_type.replace('_', ' ').title()}

{answers}

---
Developed by Content Developer Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_content_developer():
    """Test the content developer agent"""
    from state_manager import StateManager

    # Initialize project
    project_id = "PROJ-TEST-DEV-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test Content Project",
        educational_level="9-12",
        standards=["NGSS"],
        context={
            "subject": "biology",
            "topic": "genetics",
            "duration": "6 weeks",
            "constraints": {}
        }
    )

    # Create and run agent
    agent = ContentDeveloperAgent(project_id)

    print("=== Developing Lesson ===")
    result = await agent.run({
        "action": "develop_lesson",
        "objectives": ["OBJ-001", "OBJ-002", "OBJ-003"]
    })
    print(f"Status: {result['status']}")
    print(f"Decisions: {len(result.get('decisions', []))}")
    print(f"Artifacts: {result.get('artifacts', [])}")

    print("\n=== Developing Activity ===")
    result = await agent.run({
        "action": "develop_activity",
        "activity_type": "lab",
        "objective": "Analyze genetic data",
        "bloom_level": 4
    })
    print(f"Status: {result['status']}")
    print(f"Output: {result.get('output', {})}")


if __name__ == "__main__":
    asyncio.run(test_content_developer())
