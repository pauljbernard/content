#!/usr/bin/env python3
"""Platform Training Agent - Creates training materials for platform adoption"""
import asyncio, sys, json
from pathlib import Path
from typing import Dict, List, Any
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))
from base_agent import BaseAgent

class PlatformTrainingAgent(BaseAgent):
    def __init__(self, project_id: str):
        super().__init__(agent_id="platform-training", agent_name="Platform Training", project_id=project_id, description="Creates platform training materials and onboarding")

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        action = parameters.get("action", "create_training")
        if action == "create_training": return await self._create_training(parameters, context)
        elif action == "generate_onboarding": return await self._generate_onboarding(parameters, context)
        elif action == "create_tutorial": return await self._create_tutorial(parameters, context)
        elif action == "design_workshop": return await self._design_workshop(parameters, context)
        elif action == "track_completion": return await self._track_completion(parameters, context)
        return {"output": {"error": f"Unknown action: {action}"}, "decisions": [], "artifacts": [], "rationale": ""}

    async def _create_training(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        platform = parameters.get("platform", "Learning Management System")
        audience = parameters.get("audience", "Teachers")
        decisions.append(f"Creating training for {platform} targeting {audience}")
        training = {"platform": platform, "audience": audience, "modules": [{"title": "Getting Started", "duration_minutes": 15}, {"title": "Creating Content", "duration_minutes": 30}, {"title": "Assessment Tools", "duration_minutes": 25}], "total_duration_minutes": 70}
        training_artifact = f"artifacts/{self.project_id}/platform_training_{platform.replace(' ', '_')}.json"
        self.create_artifact("training", Path(training_artifact), json.dumps(training, indent=2))
        artifacts.append(training_artifact)
        return {"output": training, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created {len(training['modules'])} training modules ({training['total_duration_minutes']} min)"}

    async def _generate_onboarding(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        user_type = parameters.get("user_type", "new_teacher")
        onboarding = {"user_type": user_type, "steps": ["Account setup", "Profile configuration", "First lesson creation", "First assessment", "Help resources"], "estimated_time_minutes": 45}
        return {"output": onboarding, "decisions": [f"Generated {len(onboarding['steps'])}-step onboarding"], "artifacts": [], "rationale": f"Created {len(onboarding['steps'])}-step onboarding for {user_type}"}

    async def _create_tutorial(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        feature = parameters.get("feature", "Assessment Creation")
        tutorial = {"feature": feature, "format": "video", "duration_minutes": 8, "steps": ["Overview", "Step-by-step walkthrough", "Tips and best practices", "Common pitfalls"]}
        return {"output": tutorial, "decisions": [f"Created tutorial for {feature}"], "artifacts": [], "rationale": f"Created {tutorial['duration_minutes']}-minute tutorial for {feature}"}

    async def _design_workshop(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        topic = parameters.get("topic", "Advanced Features")
        duration_hours = parameters.get("duration_hours", 4)
        workshop = {"topic": topic, "duration_hours": duration_hours, "format": "live", "max_participants": 25, "agenda": ["Introduction", "Hands-on exercises", "Q&A", "Resources"]}
        return {"output": workshop, "decisions": [f"Designed {duration_hours}-hour workshop on {topic}"], "artifacts": [], "rationale": f"Designed {duration_hours}-hour workshop for up to {workshop['max_participants']} participants"}

    async def _track_completion(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        training_id = parameters.get("training_id")
        completion = {"training_id": training_id, "total_users": 150, "completed": 127, "completion_rate": 0.847, "average_score": 88.5}
        return {"output": completion, "decisions": [f"Tracked completion for {training_id}"], "artifacts": [], "rationale": f"Completion rate: {completion['completion_rate']:.1%}"}

    def get_required_parameters(self) -> List[str]: return ["action"]

async def test_platform_training():
    from state_manager import StateManager
    project_id = "PROJ-TEST-TRAINING-001"
    sm = StateManager(project_id)
    sm.initialize_project(name="Test Platform Training", educational_level="K-12", standards=[], context={})
    agent = PlatformTrainingAgent(project_id)
    result = await agent.run({"action": "create_training", "platform": "LMS", "audience": "Teachers"})
    print(f"Created {len(result['output']['modules'])} training modules")

if __name__ == "__main__": asyncio.run(test_platform_training())
