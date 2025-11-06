#!/usr/bin/env python3
"""
Professor Base Agent Class

Base class for all Professor autonomous agents. Provides common functionality
for state management, coordination, decision-making, and quality validation.

Usage:
    from base_agent import BaseAgent

    class MyAgent(BaseAgent):
        def __init__(self, project_id: str):
            super().__init__(
                agent_id="my-agent",
                agent_name="My Agent",
                project_id=project_id
            )

        async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
            # Agent implementation
            return {"output": "result"}
"""

import asyncio
import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from state_manager import StateManager, ProjectPhase
from decision_framework import DecisionFramework
from quality_gates import QualityValidator, ValidationResult


@dataclass
class AgentConfig:
    """Configuration for an agent"""
    agent_id: str
    agent_name: str
    description: str
    capabilities: List[str]
    quality_gates: List[str]  # Which gates this agent is responsible for


class BaseAgent(ABC):
    """Base class for all Professor agents"""

    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        project_id: str,
        description: Optional[str] = None,
        state_manager: Optional[StateManager] = None
    ):
        """
        Initialize base agent

        Args:
            agent_id: Unique agent identifier (e.g., "curriculum-architect")
            agent_name: Human-readable agent name
            project_id: Project identifier
            description: Agent description
            state_manager: StateManager instance (creates one if not provided)
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.project_id = project_id
        self.description = description or f"{agent_name} agent"

        # Initialize framework components
        self.state_manager = state_manager or StateManager(project_id)
        self.decision_framework: Optional[DecisionFramework] = None
        self.quality_validator = QualityValidator()

        # Agent state
        self.execution_history: List[Dict[str, Any]] = []
        self.artifacts_created: List[str] = []
        self.decisions_made: List[str] = []

    async def run(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for agent execution

        Args:
            parameters: Agent-specific parameters
            context: Additional context

        Returns:
            Dict with output, decisions, artifacts, and rationale
        """
        start_time = datetime.utcnow()

        # Load project state
        project_state = self.state_manager.load_project()
        if not project_state:
            raise ValueError(f"Project {self.project_id} not found. Initialize project first.")

        # Merge context
        project_context = self.state_manager.get_context()
        merged_context = {**project_context, **(context or {})}

        # Initialize decision framework with project context
        self.decision_framework = DecisionFramework(
            educational_level=project_context["educational_level"],
            subject=project_context["context"].get("subject", "general")
        )

        # Execute pre-checks
        pre_check_result = await self.pre_execution_check(parameters, merged_context)
        if not pre_check_result["can_proceed"]:
            return {
                "status": "blocked",
                "message": pre_check_result["message"],
                "decisions": [],
                "artifacts": [],
                "rationale": pre_check_result["message"]
            }

        # Execute agent logic
        try:
            result = await self.execute(parameters, merged_context)

            # Execute post-checks
            post_check_result = await self.post_execution_check(result, merged_context)
            if not post_check_result["passed"]:
                result["warnings"] = post_check_result.get("warnings", [])

            # Record execution
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()

            self._record_execution(
                parameters=parameters,
                result=result,
                execution_time_seconds=execution_time
            )

            # Update state manager
            self.state_manager.add_agent_decision(
                agent=self.agent_id,
                phase=project_context["current_phase"],
                decisions=result.get("decisions", []),
                artifacts_created=result.get("artifacts", []),
                rationale=result.get("rationale")
            )

            return {
                **result,
                "status": "success",
                "execution_time_seconds": execution_time
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "decisions": [],
                "artifacts": [],
                "rationale": f"Agent execution failed: {str(e)}"
            }

    async def pre_execution_check(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Pre-execution checks (can be overridden by subclasses)

        Returns:
            Dict with can_proceed (bool) and message (str)
        """
        # Default: Check if required parameters present
        required_params = self.get_required_parameters()
        missing = [p for p in required_params if p not in parameters]

        if missing:
            return {
                "can_proceed": False,
                "message": f"Missing required parameters: {', '.join(missing)}"
            }

        return {"can_proceed": True, "message": "Pre-checks passed"}

    async def post_execution_check(
        self,
        result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Post-execution validation (can be overridden by subclasses)

        Returns:
            Dict with passed (bool) and warnings (list)
        """
        warnings = []

        # Check if artifacts were created
        if not result.get("artifacts"):
            warnings.append("No artifacts created")

        # Check if decisions were documented
        if not result.get("decisions"):
            warnings.append("No decisions documented")

        return {
            "passed": True,  # Warnings don't block
            "warnings": warnings
        }

    @abstractmethod
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main agent logic (must be implemented by subclasses)

        Args:
            parameters: Agent-specific parameters
            context: Project context

        Returns:
            Dict with:
            - output: Main result
            - decisions: List of decisions made
            - artifacts: List of artifacts created (paths)
            - rationale: Explanation of key decisions
        """
        pass

    def get_required_parameters(self) -> List[str]:
        """Get list of required parameters (can be overridden by subclasses)"""
        return []

    def make_decision(
        self,
        decision_type: str,
        options: List[Any],
        criteria: Dict[str, Any]
    ) -> Any:
        """
        Make a pedagogical decision using decision framework

        Args:
            decision_type: Type of decision (e.g., "instructional_model")
            options: Available options
            criteria: Decision criteria

        Returns:
            Selected option
        """
        # This would use the decision framework in a real implementation
        # For now, simple selection
        self.decisions_made.append(f"{decision_type}: {options[0] if options else 'none'}")
        return options[0] if options else None

    async def validate_quality_gate(
        self,
        gate_name: str,
        artifacts: Dict[str, str],
        **kwargs
    ) -> ValidationResult:
        """
        Validate a quality gate

        Args:
            gate_name: Name of quality gate
            artifacts: Artifacts to validate
            **kwargs: Additional gate-specific parameters

        Returns:
            ValidationResult
        """
        validator_methods = {
            "research": self.quality_validator.validate_research,
            "design": self.quality_validator.validate_design,
            "content_development": self.quality_validator.validate_content_development,
            "assessment_development": self.quality_validator.validate_assessment_development,
            "review": self.quality_validator.validate_review,
            "delivery": self.quality_validator.validate_delivery
        }

        if gate_name not in validator_methods:
            raise ValueError(f"Unknown quality gate: {gate_name}")

        validator = validator_methods[gate_name]
        return validator(artifacts=artifacts, **kwargs)

    async def call_skill(
        self,
        skill_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a Professor skill

        Args:
            skill_id: Skill identifier (e.g., "curriculum.research")
            parameters: Skill parameters

        Returns:
            Skill result
        """
        # This would integrate with the skill execution framework
        # For now, placeholder
        return {
            "skill_id": skill_id,
            "status": "placeholder",
            "output": f"Skill {skill_id} would be executed here"
        }

    async def coordinate_with_agent(
        self,
        agent_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Coordinate with another agent

        Args:
            agent_id: Target agent identifier
            parameters: Parameters for target agent

        Returns:
            Result from target agent
        """
        # This would use the coordination framework
        # For now, placeholder
        return {
            "agent_id": agent_id,
            "status": "placeholder",
            "output": f"Agent {agent_id} would be coordinated here"
        }

    def create_artifact(
        self,
        artifact_name: str,
        artifact_path: Path,
        content: str
    ) -> str:
        """
        Create an artifact and register it

        Args:
            artifact_name: Logical name
            artifact_path: File path
            content: Artifact content

        Returns:
            Artifact path as string
        """
        # Ensure parent directory exists
        artifact_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        with open(artifact_path, 'w') as f:
            f.write(content)

        # Register with state manager
        self.state_manager.add_artifact(artifact_name, str(artifact_path))
        self.artifacts_created.append(str(artifact_path))

        return str(artifact_path)

    def _record_execution(
        self,
        parameters: Dict[str, Any],
        result: Dict[str, Any],
        execution_time_seconds: float
    ) -> None:
        """Record execution in agent history"""
        self.execution_history.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_id": self.agent_id,
            "parameters": parameters,
            "result_status": result.get("status", "unknown"),
            "decisions": result.get("decisions", []),
            "artifacts": result.get("artifacts", []),
            "execution_time_seconds": execution_time_seconds
        })

    def get_agent_summary(self) -> Dict[str, Any]:
        """Get summary of agent's work"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "project_id": self.project_id,
            "total_executions": len(self.execution_history),
            "artifacts_created": len(self.artifacts_created),
            "decisions_made": len(self.decisions_made),
            "latest_execution": self.execution_history[-1] if self.execution_history else None
        }

    def export_agent_log(self, output_path: Path) -> None:
        """Export agent execution log"""
        log_data = {
            "agent": {
                "id": self.agent_id,
                "name": self.agent_name,
                "description": self.description
            },
            "project_id": self.project_id,
            "execution_history": self.execution_history,
            "summary": self.get_agent_summary()
        }

        with open(output_path, 'w') as f:
            json.dump(log_data, f, indent=2)


class AgentExample(BaseAgent):
    """Example agent implementation"""

    def __init__(self, project_id: str):
        super().__init__(
            agent_id="example-agent",
            agent_name="Example Agent",
            project_id=project_id,
            description="Example agent for testing"
        )

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Example execution logic"""
        await asyncio.sleep(0.1)  # Simulate work

        return {
            "output": {"message": "Example agent executed successfully"},
            "decisions": ["Used example strategy"],
            "artifacts": ["example-output.md"],
            "rationale": "This is an example agent for testing the framework"
        }

    def get_required_parameters(self) -> List[str]:
        """Required parameters for this agent"""
        return ["action"]


async def test_base_agent():
    """Test the base agent framework"""
    # Initialize project first
    sm = StateManager("PROJ-TEST-001")
    sm.initialize_project(
        name="Test Project",
        educational_level="9-12",
        standards=["NGSS"],
        context={"subject": "biology", "topic": "genetics", "duration": "6 weeks", "constraints": {}}
    )

    # Create and run example agent
    agent = AgentExample("PROJ-TEST-001")
    result = await agent.run(parameters={"action": "test"})

    print("=== Agent Execution Result ===")
    print(json.dumps(result, indent=2))

    print("\n=== Agent Summary ===")
    print(json.dumps(agent.get_agent_summary(), indent=2))


if __name__ == "__main__":
    asyncio.run(test_base_agent())
