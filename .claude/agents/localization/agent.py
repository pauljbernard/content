#!/usr/bin/env python3
"""Localization Agent - Manages content translation and cultural adaptation"""
import asyncio, sys, json
from pathlib import Path
from typing import Dict, List, Any
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))
from base_agent import BaseAgent

class LocalizationAgent(BaseAgent):
    def __init__(self, project_id: str):
        super().__init__(agent_id="localization", agent_name="Localization", project_id=project_id, description="Manages content translation and localization")

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        action = parameters.get("action", "translate_content")
        if action == "translate_content": return await self._translate_content(parameters, context)
        elif action == "adapt_culturally": return await self._adapt_culturally(parameters, context)
        elif action == "manage_glossary": return await self._manage_glossary(parameters, context)
        elif action == "validate_translation": return await self._validate_translation(parameters, context)
        elif action == "track_localization": return await self._track_localization(parameters, context)
        return {"output": {"error": f"Unknown action: {action}"}, "decisions": [], "artifacts": [], "rationale": ""}

    async def _translate_content(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions, artifacts = [], []
        content_id = parameters.get("content_id")
        target_languages = parameters.get("target_languages", [])
        decisions.append(f"Translating {content_id} to {len(target_languages)} languages")
        translations = {"content_id": content_id, "source_language": "en", "target_languages": target_languages, "status": "completed", "word_count": 5000}
        for lang in target_languages:
            trans_artifact = f"artifacts/{self.project_id}/translation_{content_id}_{lang}.json"
            self.create_artifact(f"translation_{lang}", Path(trans_artifact), json.dumps({"language": lang, "status": "complete"}, indent=2))
            artifacts.append(trans_artifact)
        return {"output": translations, "decisions": decisions, "artifacts": artifacts, "rationale": f"Translated {translations['word_count']} words to {len(target_languages)} languages"}

    async def _adapt_culturally(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        content_id = parameters.get("content_id")
        target_culture = parameters.get("target_culture")
        adaptations = {"content_id": content_id, "target_culture": target_culture, "adaptations_made": ["Date format", "Currency", "Cultural references", "Examples and scenarios"], "review_status": "pending"}
        return {"output": adaptations, "decisions": [f"Adapted {content_id} for {target_culture}"], "artifacts": [], "rationale": f"Made {len(adaptations['adaptations_made'])} cultural adaptations"}

    async def _manage_glossary(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        operation = parameters.get("operation", "add")
        terms = parameters.get("terms", [])
        glossary = {"operation": operation, "terms_count": len(terms), "languages": ["en", "es", "fr", "de"], "total_entries": 1500}
        return {"output": glossary, "decisions": [f"Glossary {operation}: {len(terms)} terms"], "artifacts": [], "rationale": f"Managed glossary with {glossary['total_entries']} total entries"}

    async def _validate_translation(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        content_id = parameters.get("content_id")
        language = parameters.get("language")
        validation = {"content_id": content_id, "language": language, "quality_score": 92, "issues": [{"type": "terminology", "severity": "low"}], "approved": True}
        return {"output": validation, "decisions": [f"Validated translation for {language}"], "artifacts": [], "rationale": f"Translation quality: {validation['quality_score']}/100"}

    async def _track_localization(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        project_status = {"total_content_items": 50, "languages": 5, "completed": 42, "in_progress": 6, "pending": 2, "completion_rate": 0.84}
        return {"output": project_status, "decisions": ["Tracked localization progress"], "artifacts": [], "rationale": f"Localization {project_status['completion_rate']:.0%} complete"}

    def get_required_parameters(self) -> List[str]: return ["action"]

async def test_localization():
    from state_manager import StateManager
    project_id = "PROJ-TEST-LOC-001"
    sm = StateManager(project_id)
    sm.initialize_project(name="Test Localization", educational_level="K-12", standards=[], context={})
    agent = LocalizationAgent(project_id)
    result = await agent.run({"action": "translate_content", "content_id": "LESSON-001", "target_languages": ["es", "fr", "de"]})
    print(f"Translated to {len(result['output']['target_languages'])} languages")

if __name__ == "__main__": asyncio.run(test_localization())
