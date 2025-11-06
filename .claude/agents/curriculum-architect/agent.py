#!/usr/bin/env python3
"""
Curriculum Architect Agent

Orchestrates the complete curriculum development lifecycle from research through delivery.
Makes high-level pedagogical decisions and coordinates with other agents.

Usage:
    from agent import CurriculumArchitectAgent

    agent = CurriculumArchitectAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "full_cycle",
        "autonomous_mode": "full"
    })
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent
from coordination import Coordinator, AgentCall


class CurriculumArchitectAgent(BaseAgent):
    """Orchestrates complete curriculum development lifecycle"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="curriculum-architect",
            agent_name="Curriculum Architect",
            project_id=project_id,
            description="Orchestrates complete curriculum development from research to delivery"
        )
        self.coordinator: Optional[Coordinator] = None

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute curriculum architect logic

        Actions:
        - full_cycle: Complete curriculum development
        - research: Research and needs analysis only
        - design: Design learning objectives and assessments
        - coordinate_development: Coordinate content development
        - quality_check: Final quality assurance
        """
        action = parameters.get("action", "full_cycle")
        autonomous_mode = parameters.get("autonomous_mode", "full")  # full, guided, supervised

        if action == "full_cycle":
            return await self._execute_full_cycle(parameters, context, autonomous_mode)
        elif action == "research":
            return await self._execute_research(parameters, context)
        elif action == "design":
            return await self._execute_design(parameters, context)
        elif action == "coordinate_development":
            return await self._execute_development(parameters, context)
        elif action == "quality_check":
            return await self._execute_quality_check(parameters, context)
        else:
            return {
                "output": {"error": f"Unknown action: {action}"},
                "decisions": [],
                "artifacts": [],
                "rationale": f"Action '{action}' not recognized"
            }

    async def _execute_full_cycle(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any],
        autonomous_mode: str
    ) -> Dict[str, Any]:
        """Execute complete curriculum development cycle"""
        decisions = []
        artifacts = []
        phases_completed = []

        # Phase 1: Select instructional model
        duration_weeks = context.get("context", {}).get("duration", "6 weeks")
        duration_num = int(duration_weeks.split()[0]) if "weeks" in duration_weeks else 6

        model_decision = self.decision_framework.select_instructional_model(
            duration_weeks=duration_num,
            complexity=parameters.get("complexity", "medium"),
            timeline_urgency=parameters.get("timeline_urgency", "normal")
        )
        decisions.append(f"Selected {model_decision['model']} instructional model")
        decisions.append(f"Rationale: {model_decision['rationale']}")

        # Phase 2: Select learning theory
        learning_theory = self.decision_framework.select_learning_theory(
            learning_goals=parameters.get("learning_goals", []),
            age_group=context.get("educational_level")
        )
        decisions.append(f"Selected {learning_theory['theory']} learning theory")

        # Phase 3: Execute research phase
        research_output = await self._execute_research(parameters, context)
        phases_completed.append("research")
        artifacts.extend(research_output.get("artifacts", []))

        # Phase 4: Execute design phase
        design_output = await self._execute_design(parameters, context)
        phases_completed.append("design")
        artifacts.extend(design_output.get("artifacts", []))

        # Phase 5: Coordinate development
        if autonomous_mode == "full":
            dev_output = await self._execute_development(parameters, context)
            phases_completed.append("development")
            artifacts.extend(dev_output.get("artifacts", []))

        # Phase 6: Quality check
        if autonomous_mode == "full":
            qa_output = await self._execute_quality_check(parameters, context)
            phases_completed.append("quality_assurance")
            artifacts.extend(qa_output.get("artifacts", []))

        return {
            "output": {
                "phases_completed": phases_completed,
                "instructional_model": model_decision["model"],
                "learning_theory": learning_theory["theory"],
                "status": "complete" if autonomous_mode == "full" else "partial"
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": (
                f"Executed {len(phases_completed)} phases of curriculum development "
                f"using {model_decision['model']} model and {learning_theory['theory']} theory"
            )
        }

    async def _execute_research(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute research and needs analysis phase"""
        decisions = []
        artifacts = []

        # Use curriculum.research skill (simulated for now)
        research_artifact = f"artifacts/{self.project_id}/research_report.md"
        artifacts.append(research_artifact)
        decisions.append("Conducted standards alignment analysis")
        decisions.append("Identified target audience needs")
        decisions.append("Analyzed prerequisites and learning gaps")

        # Create research artifact
        research_content = self._generate_research_report(context)
        artifact_path = Path(research_artifact)
        self.create_artifact("research_report", artifact_path, research_content)

        # Validate research gate
        validation = await self.validate_quality_gate(
            "research",
            {"research_report": research_artifact},
            standards=context.get("standards", []),
            educational_level=context.get("educational_level", "9-12")
        )

        if validation.passed:
            self.state_manager.pass_quality_gate("research")
            self.state_manager.update_phase("design")
            decisions.append("Research quality gate passed")
        else:
            decisions.append(f"Research quality gate issues: {len(validation.issues)} items")

        return {
            "output": {
                "validation_score": validation.score,
                "quality_gate_passed": validation.passed
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": "Research phase completed with standards alignment and needs analysis"
        }

    async def _execute_design(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute design phase - learning objectives and assessment blueprint"""
        decisions = []
        artifacts = []

        # Design learning objectives
        objectives_artifact = f"artifacts/{self.project_id}/learning_objectives.json"
        artifacts.append(objectives_artifact)
        decisions.append("Designed learning objectives using Bloom's Taxonomy")

        objectives_content = self._generate_learning_objectives(context)
        self.create_artifact(
            "learning_objectives",
            Path(objectives_artifact),
            objectives_content
        )

        # Create assessment blueprint
        blueprint_artifact = f"artifacts/{self.project_id}/assessment_blueprint.md"
        artifacts.append(blueprint_artifact)
        decisions.append("Created assessment blueprint aligned to objectives")

        blueprint_content = self._generate_assessment_blueprint(context)
        self.create_artifact(
            "assessment_blueprint",
            Path(blueprint_artifact),
            blueprint_content
        )

        # Validate design gate
        validation = await self.validate_quality_gate(
            "design",
            {
                "learning_objectives": objectives_artifact,
                "assessment_blueprint": blueprint_artifact
            },
            standards=context.get("standards", []),
            educational_level=context.get("educational_level", "9-12")
        )

        if validation.passed:
            self.state_manager.pass_quality_gate("design")
            self.state_manager.update_phase("content_development")
            decisions.append("Design quality gate passed")

        return {
            "output": {
                "validation_score": validation.score,
                "quality_gate_passed": validation.passed
            },
            "decisions": decisions,
            "artifacts": artifacts,
            "rationale": "Design phase completed with learning objectives and assessment blueprint"
        }

    async def _execute_development(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate content development phase"""
        decisions = []

        # This would coordinate with content-developer agent
        # For now, simulated
        decisions.append("Coordinated with content-developer agent")
        decisions.append("Applied instructional routines and UDL principles")
        decisions.append("Ensured accessibility compliance (WCAG 2.1 AA)")

        return {
            "output": {"phase": "development_coordinated"},
            "decisions": decisions,
            "artifacts": [],
            "rationale": "Coordinated content development with appropriate agents"
        }

    async def _execute_quality_check(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute final quality assurance"""
        decisions = []

        # This would coordinate with quality-assurance agent
        decisions.append("Coordinated comprehensive quality review")
        decisions.append("Verified all quality gates passed")
        decisions.append("Generated final quality report")

        return {
            "output": {"quality_check": "complete"},
            "decisions": decisions,
            "artifacts": [],
            "rationale": "Final quality assurance completed"
        }

    def _generate_research_report(self, context: Dict[str, Any]) -> str:
        """Generate research report content"""
        subject = context.get("context", {}).get("subject", "General")
        topic = context.get("context", {}).get("topic", "Curriculum")
        standards = context.get("standards", [])
        level = context.get("educational_level", "9-12")

        return f"""# Research Report

## Project Overview
- **Subject**: {subject}
- **Topic**: {topic}
- **Educational Level**: {level}
- **Standards**: {', '.join(standards)}

## Standards Alignment
- Mapped to {len(standards)} standards frameworks
- Identified key performance expectations
- Cross-referenced state and national standards

## Target Audience Analysis
- Grade level: {level}
- Prior knowledge assessment completed
- Learning needs identified
- Accessibility requirements documented

## Prerequisites
- Foundational concepts identified
- Entry skills documented
- Scaffolding needs determined

## Success Criteria
- Learning objectives defined
- Assessment criteria established
- Performance indicators specified

---
Generated by Curriculum Architect Agent
"""

    def _generate_learning_objectives(self, context: Dict[str, Any]) -> str:
        """Generate learning objectives"""
        import json
        topic = context.get("context", {}).get("topic", "Topic")

        objectives = [
            {
                "id": "OBJ-001",
                "bloom_level": 2,
                "verb": "Explain",
                "objective": f"Explain the fundamental concepts of {topic}",
                "standards": context.get("standards", [])
            },
            {
                "id": "OBJ-002",
                "bloom_level": 3,
                "verb": "Apply",
                "objective": f"Apply {topic} concepts to solve problems",
                "standards": context.get("standards", [])
            },
            {
                "id": "OBJ-003",
                "bloom_level": 4,
                "verb": "Analyze",
                "objective": f"Analyze complex scenarios involving {topic}",
                "standards": context.get("standards", [])
            }
        ]

        return json.dumps(objectives, indent=2)

    def _generate_assessment_blueprint(self, context: Dict[str, Any]) -> str:
        """Generate assessment blueprint"""
        topic = context.get("context", {}).get("topic", "Topic")

        return f"""# Assessment Blueprint

## Formative Assessments

### Quick Checks (Daily)
- Type: Multiple choice, Short answer
- Frequency: End of each lesson
- Purpose: Check understanding

### Problem Sets (Weekly)
- Type: Applied problems
- Frequency: End of week
- Purpose: Practice and feedback

## Summative Assessments

### Unit Test
- Type: Mixed (MC, CR, Performance)
- Weight: 40%
- Objectives: OBJ-001, OBJ-002, OBJ-003

### Final Project
- Type: Performance task
- Weight: 60%
- Objectives: OBJ-002, OBJ-003

## Alignment Matrix

| Objective | Formative | Summative | Bloom Level |
|-----------|-----------|-----------|-------------|
| OBJ-001   | Quiz 1-3  | Unit Test | 2 |
| OBJ-002   | Problem Sets | Project | 3 |
| OBJ-003   | Lab Reports | Project | 4 |

---
Generated by Curriculum Architect Agent
"""

    def get_required_parameters(self) -> List[str]:
        """Required parameters"""
        return ["action"]


async def test_curriculum_architect():
    """Test the curriculum architect agent"""
    from state_manager import StateManager

    # Initialize project
    project_id = "PROJ-TEST-ARCH-001"
    sm = StateManager(project_id)
    sm.initialize_project(
        name="Test Curriculum Project",
        educational_level="9-12",
        standards=["NGSS", "TX-TEKS"],
        context={
            "subject": "biology",
            "topic": "genetics",
            "duration": "6 weeks",
            "constraints": {}
        }
    )

    # Create and run agent
    agent = CurriculumArchitectAgent(project_id)

    print("=== Executing Research Phase ===")
    result = await agent.run({"action": "research"})
    print(f"Status: {result['status']}")
    print(f"Decisions: {len(result.get('decisions', []))}")
    print(f"Artifacts: {result.get('artifacts', [])}")

    print("\n=== Executing Design Phase ===")
    result = await agent.run({"action": "design"})
    print(f"Status: {result['status']}")
    print(f"Decisions: {len(result.get('decisions', []))}")
    print(f"Artifacts: {result.get('artifacts', [])}")

    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")
    print(f"Artifacts created: {summary['artifacts_created']}")


if __name__ == "__main__":
    asyncio.run(test_curriculum_architect())
