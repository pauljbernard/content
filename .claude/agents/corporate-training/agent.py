#!/usr/bin/env python3
"""Corporate Training Agent - Creates corporate training and professional development content"""
import asyncio, sys, json
from pathlib import Path
from typing import Dict, List, Any
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))
from base_agent import BaseAgent

class CorporateTrainingAgent(BaseAgent):
    def __init__(self, project_id: str):
        super().__init__(agent_id="corporate-training", agent_name="Corporate Training", project_id=project_id, description="Creates corporate training and professional development content")

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        action = parameters.get("action", "create_training_program")
        if action == "create_training_program": return await self._create_training_program(parameters, context)
        elif action == "design_compliance_training": return await self._design_compliance_training(parameters, context)
        elif action == "create_skills_assessment": return await self._create_skills_assessment(parameters, context)
        elif action == "develop_onboarding": return await self._develop_onboarding(parameters, context)
        elif action == "create_leadership_program": return await self._create_leadership_program(parameters, context)
        elif action == "track_completion": return await self._track_completion(parameters, context)
        return {"output": {"error": f"Unknown action: {action}"}, "decisions": [], "artifacts": [], "rationale": ""}

    async def _create_training_program(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        topic = parameters.get("topic")
        audience = parameters.get("audience", "All employees")
        decisions.append(f"Creating training program on {topic} for {audience}")
        program = {"topic": topic, "audience": audience, "duration_hours": 16, "delivery": "Blended (online + in-person)", "modules": [{"title": "Foundations", "duration_hours": 4, "format": "Self-paced online"}, {"title": "Application", "duration_hours": 6, "format": "Instructor-led workshop"}, {"title": "Practice & Feedback", "duration_hours": 4, "format": "Group activities"}, {"title": "Evaluation", "duration_hours": 2, "format": "Skills assessment"}], "learning_objectives": ["Understand core concepts", "Apply skills in workplace", "Demonstrate proficiency"], "assessment_methods": ["Pre-test", "Module quizzes", "Final project", "Manager evaluation"]}
        program_artifact = f"artifacts/{self.project_id}/training_program_{topic.replace(' ', '_')}.json"
        self.create_artifact("training_program", Path(program_artifact), json.dumps(program, indent=2))
        artifacts.append(program_artifact)
        return {"output": program, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created {program['duration_hours']}-hour {program['delivery']} training program"}

    async def _design_compliance_training(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        regulation = parameters.get("regulation", "Data Privacy")
        decisions.append(f"Designing compliance training for {regulation}")
        training = {"regulation": regulation, "mandatory": True, "duration_minutes": 45, "frequency": "Annual", "content": [{"section": "Regulatory Overview", "duration_minutes": 10}, {"section": "Company Policies", "duration_minutes": 15}, {"section": "Scenarios & Best Practices", "duration_minutes": 15}, {"section": "Assessment", "duration_minutes": 5}], "pass_threshold": 80, "certificate": "Issued upon completion", "tracking": "LMS records with manager notification"}
        compliance_artifact = f"artifacts/{self.project_id}/compliance_{regulation.replace(' ', '_')}.json"
        self.create_artifact("compliance_training", Path(compliance_artifact), json.dumps(training, indent=2))
        artifacts.append(compliance_artifact)
        return {"output": training, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created {training['duration_minutes']}-minute mandatory {regulation} compliance training"}

    async def _create_skills_assessment(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        skill = parameters.get("skill")
        assessment = {"skill": skill, "type": "Performance-based", "duration_minutes": 60, "components": [{"component": "Knowledge Check", "weight": 0.3, "items": 15}, {"component": "Practical Exercise", "weight": 0.5, "tasks": 3}, {"component": "Peer Review", "weight": 0.2, "criteria": 5}], "proficiency_levels": ["Novice (0-59)", "Competent (60-79)", "Proficient (80-89)", "Expert (90-100)"], "scoring": "Automated + manager review"}
        return {"output": assessment, "decisions": [f"Created skills assessment for {skill}"], "artifacts": [], "rationale": f"Created {assessment['duration_minutes']}-minute {assessment['type']} assessment"}

    async def _develop_onboarding(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        role = parameters.get("role", "New Employee")
        decisions.append(f"Developing onboarding program for {role}")
        onboarding = {"role": role, "duration_days": 30, "phases": [{"phase": "Week 1: Orientation", "activities": ["Company overview", "Systems access", "Meet the team", "Workspace setup"]}, {"phase": "Week 2-3: Role Training", "activities": ["Job-specific training", "Shadow experienced employee", "Initial projects"]}, {"phase": "Week 4: Integration", "activities": ["Independent work", "30-day review", "Goal setting"]}], "checkpoints": [{"day": 7, "checkpoint": "First week review"}, {"day": 14, "checkpoint": "Mid-point check-in"}, {"day": 30, "checkpoint": "End of onboarding evaluation"}], "resources": ["Employee handbook", "Training videos", "Mentorship program"]}
        onboard_artifact = f"artifacts/{self.project_id}/onboarding_{role.replace(' ', '_')}.json"
        self.create_artifact("onboarding", Path(onboard_artifact), json.dumps(onboarding, indent=2))
        artifacts.append(onboard_artifact)
        return {"output": onboarding, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created {onboarding['duration_days']}-day onboarding program with {len(onboarding['checkpoints'])} checkpoints"}

    async def _create_leadership_program(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        level = parameters.get("level", "Emerging Leaders")
        program = {"level": level, "duration_months": 6, "format": "Cohort-based", "curriculum": [{"module": "Self-Awareness", "duration_hours": 8, "topics": ["Leadership styles", "Emotional intelligence", "360 feedback"]}, {"module": "Team Leadership", "duration_hours": 12, "topics": ["Communication", "Delegation", "Conflict resolution"]}, {"module": "Strategic Thinking", "duration_hours": 10, "topics": ["Decision making", "Change management", "Innovation"]}, {"module": "Executive Presence", "duration_hours": 6, "topics": ["Influencing", "Presentations", "Networking"]}], "experiential_learning": ["Action learning projects", "Executive coaching", "Job shadowing"], "total_hours": 36}
        return {"output": program, "decisions": [f"Created leadership program for {level}"], "artifacts": [], "rationale": f"Created {program['duration_months']}-month program with {program['total_hours']} hours"}

    async def _track_completion(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        training_id = parameters.get("training_id")
        tracking = {"training_id": training_id, "total_enrolled": 500, "completed": 425, "in_progress": 60, "not_started": 15, "completion_rate": 0.85, "average_score": 87, "average_time_hours": 14.5, "satisfaction_rating": 4.3}
        return {"output": tracking, "decisions": [f"Tracked completion for {training_id}"], "artifacts": [], "rationale": f"Completion rate: {tracking['completion_rate']:.0%}, avg score: {tracking['average_score']}"}

    def get_required_parameters(self) -> List[str]: return ["action"]

async def test_corporate_training():
    from state_manager import StateManager
    project_id = "PROJ-TEST-CORP-001"
    sm = StateManager(project_id)
    sm.initialize_project(name="Test Corporate Training", educational_level="Professional", standards=[], context={})
    agent = CorporateTrainingAgent(project_id)
    result = await agent.run({"action": "create_training_program", "topic": "Data Analytics", "audience": "Analysts"})
    print(f"Created {result['output']['duration_hours']}-hour training program")

if __name__ == "__main__": asyncio.run(test_corporate_training())
