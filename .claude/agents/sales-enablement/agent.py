#!/usr/bin/env python3
"""
Sales Enablement Agent

Creates sales materials, product demonstrations, ROI calculators, and competitive analysis.
Supports sales teams with data-driven content and customer success stories.

Usage:
    from agent import SalesEnablementAgent

    agent = SalesEnablementAgent(project_id="PROJ-2025-001")
    result = await agent.run({
        "action": "create_demo",
        "product": "Biology Curriculum",
        "audience": "District Administrators"
    })
"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from base_agent import BaseAgent


class SalesEnablementAgent(BaseAgent):
    """Creates sales enablement materials and tools"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="sales-enablement",
            agent_name="Sales Enablement",
            project_id=project_id,
            description="Creates sales materials and enablement tools"
        )

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        action = parameters.get("action", "create_demo")

        if action == "create_demo":
            return await self._create_demo(parameters, context)
        elif action == "generate_roi_calculator":
            return await self._generate_roi_calculator(parameters, context)
        elif action == "create_competitive_analysis":
            return await self._create_competitive_analysis(parameters, context)
        elif action == "generate_case_study":
            return await self._generate_case_study(parameters, context)
        elif action == "create_pitch_deck":
            return await self._create_pitch_deck(parameters, context)
        elif action == "generate_battlecard":
            return await self._generate_battlecard(parameters, context)
        else:
            return {"output": {"error": f"Unknown action: {action}"}, "decisions": [], "artifacts": [], "rationale": ""}

    async def _create_demo(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions = []
        artifacts = []
        
        product = parameters.get("product")
        audience = parameters.get("audience")
        
        decisions.append(f"Creating demo for {product} targeting {audience}")
        
        demo = {
            "product": product,
            "audience": audience,
            "key_features": ["Feature 1", "Feature 2", "Feature 3"],
            "demo_script": "Demo walkthrough...",
            "duration_minutes": 30
        }
        
        demo_artifact = f"artifacts/{self.project_id}/demo_{product.replace(' ', '_')}.md"
        self.create_artifact("demo", Path(demo_artifact), json.dumps(demo, indent=2))
        artifacts.append(demo_artifact)
        
        return {"output": demo, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created demo for {product}"}

    async def _generate_roi_calculator(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions = []
        artifacts = []
        
        product = parameters.get("product")
        
        decisions.append(f"Generating ROI calculator for {product}")
        
        calculator = {
            "product": product,
            "cost_inputs": ["license_cost", "implementation_cost", "training_cost"],
            "benefit_inputs": ["time_saved", "improved_outcomes", "reduced_costs"],
            "formula": "ROI = (Total Benefits - Total Costs) / Total Costs * 100"
        }
        
        calc_artifact = f"artifacts/{self.project_id}/roi_calculator.json"
        self.create_artifact("roi_calculator", Path(calc_artifact), json.dumps(calculator, indent=2))
        artifacts.append(calc_artifact)
        
        return {"output": calculator, "decisions": decisions, "artifacts": artifacts, "rationale": "Generated ROI calculator"}

    async def _create_competitive_analysis(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions = []
        artifacts = []
        
        competitors = parameters.get("competitors", [])
        
        decisions.append(f"Analyzing {len(competitors)} competitors")
        
        analysis = {
            "competitors": competitors,
            "comparison_matrix": {},
            "strengths": [],
            "weaknesses": []
        }
        
        analysis_artifact = f"artifacts/{self.project_id}/competitive_analysis.json"
        self.create_artifact("competitive_analysis", Path(analysis_artifact), json.dumps(analysis, indent=2))
        artifacts.append(analysis_artifact)
        
        return {"output": analysis, "decisions": decisions, "artifacts": artifacts, "rationale": f"Analyzed {len(competitors)} competitors"}

    async def _generate_case_study(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions = []
        artifacts = []
        
        customer = parameters.get("customer")
        
        decisions.append(f"Generating case study for {customer}")
        
        case_study = {
            "customer": customer,
            "challenge": "Customer challenge...",
            "solution": "Our solution...",
            "results": "Measurable results...",
            "testimonial": "Customer quote..."
        }
        
        case_artifact = f"artifacts/{self.project_id}/case_study_{customer.replace(' ', '_')}.md"
        self.create_artifact("case_study", Path(case_artifact), json.dumps(case_study, indent=2))
        artifacts.append(case_artifact)
        
        return {"output": case_study, "decisions": decisions, "artifacts": artifacts, "rationale": f"Generated case study for {customer}"}

    async def _create_pitch_deck(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions = []
        artifacts = []
        
        product = parameters.get("product")
        
        decisions.append(f"Creating pitch deck for {product}")
        
        pitch_deck = {
            "product": product,
            "slides": [
                {"title": "Problem", "content": "Problem statement"},
                {"title": "Solution", "content": "Our solution"},
                {"title": "Benefits", "content": "Key benefits"},
                {"title": "Pricing", "content": "Pricing model"},
                {"title": "Call to Action", "content": "Next steps"}
            ]
        }
        
        deck_artifact = f"artifacts/{self.project_id}/pitch_deck.json"
        self.create_artifact("pitch_deck", Path(deck_artifact), json.dumps(pitch_deck, indent=2))
        artifacts.append(deck_artifact)
        
        return {"output": pitch_deck, "decisions": decisions, "artifacts": artifacts, "rationale": f"Created pitch deck with {len(pitch_deck['slides'])} slides"}

    async def _generate_battlecard(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        decisions = []
        artifacts = []
        
        competitor = parameters.get("competitor")
        
        decisions.append(f"Generating battlecard for {competitor}")
        
        battlecard = {
            "competitor": competitor,
            "strengths": ["Strength 1", "Strength 2"],
            "weaknesses": ["Weakness 1", "Weakness 2"],
            "our_advantages": ["Advantage 1", "Advantage 2"],
            "objection_responses": []
        }
        
        battlecard_artifact = f"artifacts/{self.project_id}/battlecard_{competitor.replace(' ', '_')}.json"
        self.create_artifact("battlecard", Path(battlecard_artifact), json.dumps(battlecard, indent=2))
        artifacts.append(battlecard_artifact)
        
        return {"output": battlecard, "decisions": decisions, "artifacts": artifacts, "rationale": f"Generated battlecard for {competitor}"}

    def get_required_parameters(self) -> List[str]:
        return ["action"]


async def test_sales_enablement():
    from state_manager import StateManager
    
    project_id = "PROJ-TEST-SALES-001"
    sm = StateManager(project_id)
    sm.initialize_project(name="Test Sales Enablement", educational_level="9-12", standards=[], context={})
    
    agent = SalesEnablementAgent(project_id)
    
    print("=== Create Demo ===")
    result = await agent.run({"action": "create_demo", "product": "Biology Curriculum", "audience": "Teachers"})
    print(f"Status: {result['status']}")
    
    print("\n=== Agent Summary ===")
    summary = agent.get_agent_summary()
    print(f"Total executions: {summary['total_executions']}")


if __name__ == "__main__":
    asyncio.run(test_sales_enablement())
