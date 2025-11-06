#!/usr/bin/env python3
"""
Professor Agent Coordination Framework

Manages agent-to-agent communication, orchestration patterns, and workflow execution.
Supports sequential pipelines, parallel execution, and feedback loops.

Usage:
    from coordination import Coordinator, AgentCall

    coordinator = Coordinator(project_id="PROJ-2025-001")
    await coordinator.execute_pipeline([
        AgentCall("curriculum-architect", {"action": "research"}),
        AgentCall("content-developer", {"action": "develop"}),
        AgentCall("quality-assurance", {"action": "validate"})
    ])
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from state_manager import StateManager, ProjectPhase


class ExecutionPattern(Enum):
    """Agent execution patterns"""
    SEQUENTIAL = "sequential"  # One after another
    PARALLEL = "parallel"      # All at once
    CONDITIONAL = "conditional" # Based on previous results
    FEEDBACK_LOOP = "feedback_loop"  # Iterative until quality gate passed


class AgentStatus(Enum):
    """Agent execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class AgentCall:
    """Represents a call to an agent"""
    agent_id: str
    parameters: Dict[str, Any]
    dependencies: List[str] = None  # IDs of agents that must complete first
    retry_on_failure: bool = True
    max_retries: int = 3
    timeout_seconds: int = 600

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class AgentResult:
    """Result from agent execution"""
    agent_id: str
    status: str
    execution_time_seconds: float
    output: Dict[str, Any]
    artifacts_created: List[str]
    errors: Optional[List[str]] = None
    retries: int = 0


class Coordinator:
    """Coordinates multi-agent workflows"""

    def __init__(self, project_id: str, state_manager: Optional[StateManager] = None):
        """
        Initialize coordinator

        Args:
            project_id: Project identifier
            state_manager: StateManager instance (creates one if not provided)
        """
        self.project_id = project_id
        self.state_manager = state_manager or StateManager(project_id)
        self.agent_registry: Dict[str, Callable] = {}
        self.execution_log: List[AgentResult] = []

    def register_agent(self, agent_id: str, agent_callable: Callable) -> None:
        """
        Register an agent for execution

        Args:
            agent_id: Unique agent identifier
            agent_callable: Callable that executes the agent
        """
        self.agent_registry[agent_id] = agent_callable

    async def execute_agent(
        self,
        agent_call: AgentCall,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Execute a single agent

        Args:
            agent_call: Agent call specification
            context: Additional context for execution

        Returns:
            AgentResult with execution details
        """
        if agent_call.agent_id not in self.agent_registry:
            raise ValueError(f"Agent {agent_call.agent_id} not registered")

        agent_callable = self.agent_registry[agent_call.agent_id]
        start_time = datetime.utcnow()
        retries = 0
        errors = []

        # Get project context
        project_context = self.state_manager.get_context()
        merged_context = {**project_context, **(context or {})}

        while retries <= agent_call.max_retries:
            try:
                # Execute agent
                output = await asyncio.wait_for(
                    agent_callable(agent_call.parameters, merged_context),
                    timeout=agent_call.timeout_seconds
                )

                # Success
                end_time = datetime.utcnow()
                execution_time = (end_time - start_time).total_seconds()

                result = AgentResult(
                    agent_id=agent_call.agent_id,
                    status=AgentStatus.COMPLETED.value,
                    execution_time_seconds=execution_time,
                    output=output,
                    artifacts_created=output.get("artifacts", []),
                    retries=retries
                )

                # Log to state manager
                self.state_manager.add_agent_decision(
                    agent=agent_call.agent_id,
                    phase=project_context.get("current_phase", "unknown"),
                    decisions=output.get("decisions", []),
                    artifacts_created=result.artifacts_created,
                    rationale=output.get("rationale")
                )

                self.execution_log.append(result)
                return result

            except asyncio.TimeoutError:
                errors.append(f"Timeout after {agent_call.timeout_seconds}s")
                retries += 1

            except Exception as e:
                errors.append(f"Error: {str(e)}")
                retries += 1

            if not agent_call.retry_on_failure:
                break

        # Failed after all retries
        end_time = datetime.utcnow()
        execution_time = (end_time - start_time).total_seconds()

        result = AgentResult(
            agent_id=agent_call.agent_id,
            status=AgentStatus.FAILED.value,
            execution_time_seconds=execution_time,
            output={},
            artifacts_created=[],
            errors=errors,
            retries=retries
        )

        self.execution_log.append(result)
        return result

    async def execute_sequential(
        self,
        agent_calls: List[AgentCall],
        stop_on_failure: bool = True
    ) -> List[AgentResult]:
        """
        Execute agents sequentially (pipeline pattern)

        Args:
            agent_calls: List of agent calls
            stop_on_failure: Stop pipeline if any agent fails

        Returns:
            List of agent results
        """
        results = []
        accumulated_context = {}

        for agent_call in agent_calls:
            result = await self.execute_agent(agent_call, accumulated_context)
            results.append(result)

            if result.status == AgentStatus.FAILED.value and stop_on_failure:
                break

            # Pass output to next agent as context
            accumulated_context[f"{agent_call.agent_id}_output"] = result.output

        return results

    async def execute_parallel(
        self,
        agent_calls: List[AgentCall]
    ) -> List[AgentResult]:
        """
        Execute agents in parallel

        Args:
            agent_calls: List of agent calls

        Returns:
            List of agent results
        """
        tasks = [self.execute_agent(call) for call in agent_calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to failed results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(AgentResult(
                    agent_id=agent_calls[i].agent_id,
                    status=AgentStatus.FAILED.value,
                    execution_time_seconds=0,
                    output={},
                    artifacts_created=[],
                    errors=[str(result)]
                ))
            else:
                processed_results.append(result)

        return processed_results

    async def execute_with_dependencies(
        self,
        agent_calls: List[AgentCall]
    ) -> List[AgentResult]:
        """
        Execute agents respecting dependencies (DAG pattern)

        Args:
            agent_calls: List of agent calls with dependencies

        Returns:
            List of agent results
        """
        # Build dependency graph
        completed = set()
        results_map = {}
        all_results = []

        while len(completed) < len(agent_calls):
            # Find agents ready to execute (dependencies satisfied)
            ready = [
                call for call in agent_calls
                if call.agent_id not in completed
                and all(dep in completed for dep in call.dependencies)
            ]

            if not ready:
                # Circular dependency or missing dependency
                remaining = [call for call in agent_calls if call.agent_id not in completed]
                raise ValueError(f"Cannot resolve dependencies for: {[c.agent_id for c in remaining]}")

            # Execute ready agents in parallel
            batch_results = await self.execute_parallel(ready)

            for result in batch_results:
                completed.add(result.agent_id)
                results_map[result.agent_id] = result
                all_results.append(result)

        return all_results

    async def execute_feedback_loop(
        self,
        agent_call: AgentCall,
        validator_call: AgentCall,
        max_iterations: int = 5
    ) -> List[AgentResult]:
        """
        Execute agent with feedback loop until validation passes

        Args:
            agent_call: Primary agent to execute
            validator_call: Validator agent that checks quality
            max_iterations: Maximum number of iterations

        Returns:
            List of all agent results (including iterations)
        """
        results = []
        iteration = 0

        while iteration < max_iterations:
            # Execute primary agent
            agent_result = await self.execute_agent(agent_call)
            results.append(agent_result)

            if agent_result.status == AgentStatus.FAILED.value:
                break

            # Validate result
            validator_params = {
                **validator_call.parameters,
                "artifacts": agent_result.artifacts_created,
                "iteration": iteration
            }
            validator_result = await self.execute_agent(
                AgentCall(
                    agent_id=validator_call.agent_id,
                    parameters=validator_params
                )
            )
            results.append(validator_result)

            # Check if validation passed
            if validator_result.output.get("validation_passed", False):
                break

            # Provide feedback to next iteration
            agent_call.parameters["feedback"] = validator_result.output.get("feedback", [])
            iteration += 1

        return results

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all agent executions"""
        total_time = sum(r.execution_time_seconds for r in self.execution_log)
        failed = [r for r in self.execution_log if r.status == AgentStatus.FAILED.value]

        return {
            "total_agents_executed": len(self.execution_log),
            "successful": len(self.execution_log) - len(failed),
            "failed": len(failed),
            "total_execution_time_seconds": total_time,
            "failed_agents": [r.agent_id for r in failed],
            "all_artifacts": [
                artifact
                for result in self.execution_log
                for artifact in result.artifacts_created
            ]
        }

    def export_execution_log(self, output_path: Path) -> None:
        """Export execution log to JSON file"""
        log_data = [asdict(result) for result in self.execution_log]

        with open(output_path, 'w') as f:
            json.dump({
                "project_id": self.project_id,
                "execution_log": log_data,
                "summary": self.get_execution_summary()
            }, f, indent=2)


async def example_usage():
    """Example coordination patterns"""
    coordinator = Coordinator("PROJ-2025-EXAMPLE")

    # Register mock agents
    async def mock_agent(params, context):
        await asyncio.sleep(0.1)  # Simulate work
        return {
            "decisions": [f"Decision from {params.get('agent_name')}"],
            "artifacts": [f"{params.get('agent_name')}-output.md"],
            "rationale": "Mock rationale"
        }

    coordinator.register_agent("curriculum-architect", mock_agent)
    coordinator.register_agent("content-developer", mock_agent)
    coordinator.register_agent("pedagogical-reviewer", mock_agent)
    coordinator.register_agent("quality-assurance", mock_agent)

    # Pattern 1: Sequential pipeline
    print("=== Sequential Pipeline ===")
    results = await coordinator.execute_sequential([
        AgentCall("curriculum-architect", {"agent_name": "curriculum-architect"}),
        AgentCall("content-developer", {"agent_name": "content-developer"}),
        AgentCall("quality-assurance", {"agent_name": "quality-assurance"})
    ])

    for r in results:
        print(f"{r.agent_id}: {r.status} ({r.execution_time_seconds:.2f}s)")

    # Pattern 2: Parallel execution
    print("\n=== Parallel Execution ===")
    results = await coordinator.execute_parallel([
        AgentCall("pedagogical-reviewer", {"agent_name": "pedagogical-reviewer"}),
        AgentCall("content-developer", {"agent_name": "content-developer"})
    ])

    for r in results:
        print(f"{r.agent_id}: {r.status} ({r.execution_time_seconds:.2f}s)")

    # Get summary
    print("\n=== Execution Summary ===")
    summary = coordinator.get_execution_summary()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    asyncio.run(example_usage())
