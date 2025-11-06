#!/usr/bin/env python3
"""Instructional Designer Agent - Implements instructional design models and methodologies"""
import asyncio, sys, json
from pathlib import Path
from typing import Dict, List, Any
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))
from base_agent import BaseAgent

class InstructionalDesignerAgent(BaseAgent):
    def __init__(self, project_id: str):
        super().__init__(agent_id="instructional-designer", agent_name="Instructional Designer", project_id=project_id, description="Implements instructional design models and creates learning experiences")

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        action = parameters.get("action", "apply_addie")
        if action == "apply_addie": return await self._apply_addie(parameters, context)
        elif action == "apply_sam": return await self._apply_sam(parameters, context)
        elif action == "apply_backward_design": return await self._apply_backward_design(parameters, context)
        elif action == "design_learning_experience": return await self._design_learning_experience(parameters, context)
        elif action == "select_instructional_strategy": return await self._select_instructional_strategy(parameters, context)
        elif action == "create_storyboard": return await self._create_storyboard(parameters, context)
        return {"output": {"error": f"Unknown action: {action}"}, "decisions": [], "artifacts": [], "rationale": ""}

    async def _apply_addie(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        project_name = parameters.get("project_name")
        decisions.append(f"Applying ADDIE model to {project_name}")
        addie = {"project": project_name, "phases": [{"phase": "Analysis", "status": "complete", "deliverables": ["Needs analysis", "Learner analysis", "Task analysis"]}, {"phase": "Design", "status": "in_progress", "deliverables": ["Learning objectives", "Assessment strategy", "Instructional strategy"]}, {"phase": "Development", "status": "pending", "deliverables": ["Content creation", "Media development", "Prototype"]}, {"phase": "Implementation", "status": "pending", "deliverables": ["Delivery plan", "Pilot test", "Rollout"]}, {"phase": "Evaluation", "status": "pending", "deliverables": ["Formative evaluation", "Summative evaluation", "Revision plan"]}], "current_phase": "Design"}
        plan_artifact = f"artifacts/{self.project_id}/addie_plan_{project_name.replace(' ', '_')}.json"
        self.create_artifact("addie_plan", Path(plan_artifact), json.dumps(addie, indent=2))
        artifacts.append(plan_artifact)
        return {"output": addie, "decisions": decisions, "artifacts": artifacts, "rationale": f"ADDIE plan created, currently in {addie['current_phase']} phase"}

    async def _apply_sam(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        project_name = parameters.get("project_name")
        sam = {"project": project_name, "model": "SAM (Successive Approximation Model)", "iterations": [{"iteration": 1, "phase": "Preparation", "activities": ["Savvy Start", "Project planning", "Brainstorming"]}, {"iteration": 2, "phase": "Iterative Design", "activities": ["Design proof", "Prototype", "Review cycle"]}, {"iteration": 3, "phase": "Iterative Development", "activities": ["Alpha build", "Review and refine", "Beta build"]}], "current_iteration": 2}
        return {"output": sam, "decisions": [f"Applied SAM model to {project_name}"], "artifacts": [], "rationale": f"SAM iteration {sam['current_iteration']}/3 in progress"}

    async def _apply_backward_design(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        topic = parameters.get("topic")
        backward_design = {"topic": topic, "stage_1_outcomes": {"desired_results": "Students will understand...", "essential_questions": ["What is...?", "How does...?"], "knowledge": ["Students will know..."], "skills": ["Students will be able to..."]}, "stage_2_assessment": {"performance_tasks": ["Design project", "Presentation"], "other_evidence": ["Quiz", "Observation", "Self-assessment"], "criteria": "Rubrics aligned to outcomes"}, "stage_3_plan": {"learning_activities": ["Hook/engagement", "Guided instruction", "Practice", "Application"], "resources": ["Textbook", "Videos", "Manipulatives"], "differentiation": ["Scaffolding for struggling learners", "Extensions for advanced"]}}
        return {"output": backward_design, "decisions": [f"Applied Backward Design to {topic}"], "artifacts": [], "rationale": "Backward design framework created with 3 stages"}

    async def _design_learning_experience(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        experience_type = parameters.get("experience_type", "project_based")
        objective = parameters.get("objective")
        decisions.append(f"Designing {experience_type} learning experience for {objective}")
        experience = {"type": experience_type, "objective": objective, "duration_hours": 6, "components": [{"component": "Introduction", "duration_minutes": 30, "activities": ["Hook", "Context setting"]}, {"component": "Exploration", "duration_minutes": 120, "activities": ["Research", "Investigation"]}, {"component": "Creation", "duration_minutes": 150, "activities": ["Product development", "Iteration"]}, {"component": "Presentation", "duration_minutes": 60, "activities": ["Sharing", "Peer feedback"]}], "assessment": "Rubric-based evaluation of final product", "differentiation": ["Choice in topic", "Flexible grouping", "Scaffolded resources"]}
        exp_artifact = f"artifacts/{self.project_id}/learning_experience_{experience_type}.json"
        self.create_artifact("learning_experience", Path(exp_artifact), json.dumps(experience, indent=2))
        artifacts.append(exp_artifact)
        return {"output": experience, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created {experience['duration_hours']}-hour {experience_type} learning experience"}

    async def _select_instructional_strategy(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        objective = parameters.get("objective")
        learner_level = parameters.get("learner_level", "intermediate")
        strategies = [{"strategy": "Direct Instruction", "suitability": 0.7, "rationale": "Good for foundational knowledge"}, {"strategy": "Inquiry-Based Learning", "suitability": 0.85, "rationale": "Excellent for deep understanding and engagement"}, {"strategy": "Collaborative Learning", "suitability": 0.75, "rationale": "Supports peer learning"}, {"strategy": "Problem-Based Learning", "suitability": 0.9, "rationale": "Best fit for application and real-world context"}]
        recommended = max(strategies, key=lambda s: s['suitability'])
        return {"output": {"objective": objective, "learner_level": learner_level, "strategies": strategies, "recommended": recommended}, "decisions": [f"Selected {recommended['strategy']} as optimal strategy"], "artifacts": [], "rationale": f"Recommended {recommended['strategy']} (suitability: {recommended['suitability']})"}

    async def _create_storyboard(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        content_id = parameters.get("content_id")
        format_type = parameters.get("format", "video")
        decisions.append(f"Creating {format_type} storyboard for {content_id}")
        storyboard = {"content_id": content_id, "format": format_type, "duration_minutes": 8, "scenes": [{"scene": 1, "duration_seconds": 30, "visual": "Title screen with engaging question", "audio": "Narrator introduction", "interaction": None}, {"scene": 2, "duration_seconds": 120, "visual": "Animated diagram showing concept", "audio": "Explanation of key points", "interaction": "Pause points for reflection"}, {"scene": 3, "duration_seconds": 90, "visual": "Real-world example", "audio": "Case study narration", "interaction": None}, {"scene": 4, "duration_seconds": 60, "visual": "Practice problem", "audio": "Guided walkthrough", "interaction": "Interactive quiz"}, {"scene": 5, "duration_seconds": 30, "visual": "Summary and next steps", "audio": "Recap and call-to-action", "interaction": "Link to resources"}], "production_notes": "Use consistent branding, ensure captions for accessibility"}
        story_artifact = f"artifacts/{self.project_id}/storyboard_{content_id}.json"
        self.create_artifact("storyboard", Path(story_artifact), json.dumps(storyboard, indent=2))
        artifacts.append(story_artifact)
        return {"output": storyboard, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created {len(storyboard['scenes'])}-scene storyboard for {storyboard['duration_minutes']}-minute {format_type}"}

    def get_required_parameters(self) -> List[str]: return ["action"]

async def test_instructional_designer():
    from state_manager import StateManager
    project_id = "PROJ-TEST-ID-001"
    sm = StateManager(project_id)
    sm.initialize_project(name="Test Instructional Design", educational_level="K-12", standards=[], context={})
    agent = InstructionalDesignerAgent(project_id)
    result = await agent.run({"action": "apply_addie", "project_name": "Science Curriculum"})
    print(f"Current ADDIE phase: {result['output']['current_phase']}")

if __name__ == "__main__": asyncio.run(test_instructional_designer())
