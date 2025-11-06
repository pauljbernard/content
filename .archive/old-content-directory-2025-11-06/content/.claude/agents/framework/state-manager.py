#!/usr/bin/env python3
"""
Professor Agent State Manager

Manages project state, context, and artifacts for autonomous agents.
Provides persistence, versioning, and context retrieval for agent coordination.

Usage:
    from state_manager import StateManager

    sm = StateManager(project_id="PROJ-2025-001")
    sm.initialize_project(name="High School Biology", level="9-12")
    sm.update_phase("content_development")
    sm.add_agent_decision("curriculum-architect", "Selected ADDIE model")
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ProjectPhase(Enum):
    """Curriculum development phases"""
    INITIATION = "initiation"
    RESEARCH = "research"
    DESIGN = "design"
    CONTENT_DEVELOPMENT = "content_development"
    ASSESSMENT_DEVELOPMENT = "assessment_development"
    REVIEW = "review"
    REVISION = "revision"
    DELIVERY = "delivery"
    DEPLOYED = "deployed"


class QualityGate(Enum):
    """Quality gates that must be passed"""
    RESEARCH = "research"
    DESIGN = "design"
    CONTENT_DEVELOPMENT = "content_development"
    ASSESSMENT_DEVELOPMENT = "assessment_development"
    REVIEW = "review"
    DELIVERY = "delivery"


@dataclass
class AgentDecision:
    """Record of an agent decision"""
    agent: str
    phase: str
    timestamp: str
    decisions: List[str]
    artifacts_created: List[str]
    rationale: Optional[str] = None


@dataclass
class ProjectContext:
    """Project context information"""
    subject: str
    topic: str
    duration: str
    constraints: Dict[str, Any]


@dataclass
class ProjectState:
    """Complete project state"""
    project_id: str
    name: str
    educational_level: str
    standards: List[str]
    current_phase: str
    context: Dict[str, Any]
    artifacts: Dict[str, str]
    agent_history: List[Dict[str, Any]]
    quality_gates_passed: List[str]
    quality_gates_pending: List[str]
    learner_data: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str


class StateManager:
    """Manages project state for Professor agents"""

    def __init__(self, project_id: str, state_dir: Optional[Path] = None):
        """
        Initialize state manager

        Args:
            project_id: Unique project identifier
            state_dir: Directory for state files (default: ~/.claude/agents/state)
        """
        self.project_id = project_id
        self.state_dir = state_dir or Path.home() / ".claude" / "agents" / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / f"{project_id}.json"
        self.state: Optional[ProjectState] = None

    def initialize_project(
        self,
        name: str,
        educational_level: str,
        standards: List[str],
        context: Dict[str, Any]
    ) -> ProjectState:
        """
        Initialize a new project

        Args:
            name: Project name
            educational_level: K-5, 6-8, 9-12, undergraduate, graduate, post-graduate, professional
            standards: List of standards frameworks (e.g., ["NGSS", "Common Core"])
            context: Project context (subject, topic, duration, constraints)

        Returns:
            ProjectState object
        """
        now = datetime.utcnow().isoformat() + "Z"

        self.state = ProjectState(
            project_id=self.project_id,
            name=name,
            educational_level=educational_level,
            standards=standards,
            current_phase=ProjectPhase.INITIATION.value,
            context=context,
            artifacts={},
            agent_history=[],
            quality_gates_passed=[],
            quality_gates_pending=[gate.value for gate in QualityGate],
            learner_data=None,
            created_at=now,
            updated_at=now
        )

        self._save()
        return self.state

    def load_project(self) -> Optional[ProjectState]:
        """
        Load existing project state

        Returns:
            ProjectState object or None if not found
        """
        if not self.state_file.exists():
            return None

        with open(self.state_file, 'r') as f:
            data = json.load(f)
            self.state = ProjectState(**data)
            return self.state

    def update_phase(self, phase: str) -> None:
        """Update current project phase"""
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        self.state.current_phase = phase
        self.state.updated_at = datetime.utcnow().isoformat() + "Z"
        self._save()

    def add_artifact(self, artifact_name: str, artifact_path: str) -> None:
        """
        Add artifact to project

        Args:
            artifact_name: Logical name (e.g., "research_report", "learning_objectives")
            artifact_path: File system path to artifact
        """
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        self.state.artifacts[artifact_name] = artifact_path
        self.state.updated_at = datetime.utcnow().isoformat() + "Z"
        self._save()

    def add_agent_decision(
        self,
        agent: str,
        phase: str,
        decisions: List[str],
        artifacts_created: List[str],
        rationale: Optional[str] = None
    ) -> None:
        """
        Record an agent decision

        Args:
            agent: Agent name (e.g., "curriculum-architect")
            phase: Project phase when decision made
            decisions: List of decisions made
            artifacts_created: List of artifacts created
            rationale: Optional explanation of decision rationale
        """
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        decision = AgentDecision(
            agent=agent,
            phase=phase,
            timestamp=datetime.utcnow().isoformat() + "Z",
            decisions=decisions,
            artifacts_created=artifacts_created,
            rationale=rationale
        )

        self.state.agent_history.append(asdict(decision))
        self.state.updated_at = datetime.utcnow().isoformat() + "Z"
        self._save()

    def pass_quality_gate(self, gate: str) -> None:
        """Mark a quality gate as passed"""
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        if gate in self.state.quality_gates_pending:
            self.state.quality_gates_pending.remove(gate)
            self.state.quality_gates_passed.append(gate)
            self.state.updated_at = datetime.utcnow().isoformat() + "Z"
            self._save()

    def get_context(self) -> Dict[str, Any]:
        """Get full project context for agent decision-making"""
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        return {
            "project_id": self.state.project_id,
            "name": self.state.name,
            "educational_level": self.state.educational_level,
            "standards": self.state.standards,
            "current_phase": self.state.current_phase,
            "context": self.state.context,
            "artifacts": self.state.artifacts,
            "quality_gates_passed": self.state.quality_gates_passed,
            "quality_gates_pending": self.state.quality_gates_pending,
            "agent_history": self.state.agent_history
        }

    def get_latest_decisions(self, agent: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent agent decisions

        Args:
            agent: Filter by specific agent (optional)
            limit: Maximum number of decisions to return

        Returns:
            List of agent decisions
        """
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        decisions = self.state.agent_history

        if agent:
            decisions = [d for d in decisions if d["agent"] == agent]

        return decisions[-limit:]

    def export_state(self) -> Dict[str, Any]:
        """Export complete state as dictionary"""
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        return asdict(self.state)

    def _save(self) -> None:
        """Save state to disk"""
        if not self.state:
            raise ValueError("Project not initialized or loaded")

        with open(self.state_file, 'w') as f:
            json.dump(asdict(self.state), f, indent=2)


def list_projects(state_dir: Optional[Path] = None) -> List[str]:
    """
    List all project IDs

    Args:
        state_dir: Directory for state files

    Returns:
        List of project IDs
    """
    state_dir = state_dir or Path.home() / ".claude" / "agents" / "state"

    if not state_dir.exists():
        return []

    return [f.stem for f in state_dir.glob("*.json")]


def get_project_summary(project_id: str, state_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Get project summary without loading full state

    Args:
        project_id: Project identifier
        state_dir: Directory for state files

    Returns:
        Project summary dictionary
    """
    state_dir = state_dir or Path.home() / ".claude" / "agents" / "state"
    state_file = state_dir / f"{project_id}.json"

    if not state_file.exists():
        raise ValueError(f"Project {project_id} not found")

    with open(state_file, 'r') as f:
        data = json.load(f)
        return {
            "project_id": data["project_id"],
            "name": data["name"],
            "educational_level": data["educational_level"],
            "current_phase": data["current_phase"],
            "quality_gates_passed": len(data["quality_gates_passed"]),
            "quality_gates_total": len(data["quality_gates_passed"]) + len(data["quality_gates_pending"]),
            "created_at": data["created_at"],
            "updated_at": data["updated_at"]
        }


if __name__ == "__main__":
    # Example usage
    sm = StateManager("PROJ-2025-001")

    # Initialize new project
    state = sm.initialize_project(
        name="High School Biology - Genetics Unit",
        educational_level="9-12",
        standards=["NGSS", "TX-TEKS"],
        context={
            "subject": "Biology",
            "topic": "Genetics and Heredity",
            "duration": "6 weeks",
            "constraints": {
                "accessibility": "WCAG-2.1-AA",
                "budget": "medium",
                "timeline": "8 weeks"
            }
        }
    )

    print(f"Created project: {state.name}")
    print(f"Phase: {state.current_phase}")

    # Add agent decision
    sm.add_agent_decision(
        agent="curriculum-architect",
        phase="initiation",
        decisions=["Selected ADDIE model", "Prioritized NGSS over state standards"],
        artifacts_created=["project-plan.md"],
        rationale="ADDIE provides structured approach suitable for 6-week timeline"
    )

    # Update phase
    sm.update_phase(ProjectPhase.RESEARCH.value)

    # Add artifact
    sm.add_artifact("research_report", "artifacts/001-research.md")

    # Pass quality gate
    sm.pass_quality_gate(QualityGate.RESEARCH.value)

    # Get context
    context = sm.get_context()
    print(f"\nProject context: {json.dumps(context, indent=2)}")
