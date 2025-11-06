#!/usr/bin/env python3
"""
Professor Skill Base Class

Base class for all 92 Professor skills. Provides common functionality for
skill execution, validation, and integration with the agent framework.

Usage:
    from skill_base import Skill, SkillParameter

    class MySkill(Skill):
        def __init__(self):
            super().__init__(
                skill_id="curriculum.research",
                skill_name="Curriculum Research",
                category="curriculum"
            )

        def get_parameters(self) -> List[SkillParameter]:
            return [
                SkillParameter("topic", str, required=True),
                SkillParameter("level", str, required=True)
            ]

        async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
            # Implementation
            return {"output": "research results"}
"""

import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Type


class SkillCategory(Enum):
    """Skill categories"""
    CURRICULUM = "curriculum"
    LEARNING = "learning"
    ASSESSMENT = "assessment"
    CONTENT = "content"
    REVIEW = "review"
    PACKAGING = "packaging"
    ANALYTICS = "analytics"
    SUPPORT = "support"


@dataclass
class SkillParameter:
    """Definition of a skill parameter"""
    name: str
    param_type: Type
    description: str = ""
    required: bool = True
    default: Optional[Any] = None
    choices: Optional[List[Any]] = None

    def validate(self, value: Any) -> bool:
        """Validate parameter value"""
        # Check required
        if self.required and value is None:
            return False

        # Check type
        if value is not None and not isinstance(value, self.param_type):
            try:
                # Try to convert
                self.param_type(value)
            except (ValueError, TypeError):
                return False

        # Check choices
        if self.choices and value not in self.choices:
            return False

        return True


@dataclass
class SkillResult:
    """Result from skill execution"""
    skill_id: str
    status: str  # success, failed, partial
    output: Dict[str, Any]
    artifacts: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    execution_time_seconds: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class Skill(ABC):
    """Base class for all Professor skills"""

    def __init__(
        self,
        skill_id: str,
        skill_name: str,
        category: str,
        description: str = "",
        version: str = "1.0.0"
    ):
        """
        Initialize skill

        Args:
            skill_id: Unique skill identifier (e.g., "curriculum.research")
            skill_name: Human-readable name
            category: Skill category
            description: Skill description
            version: Skill version
        """
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.category = category
        self.description = description
        self.version = version
        self.execution_count = 0

    async def run(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> SkillResult:
        """
        Execute the skill with validation

        Args:
            parameters: Skill parameters
            context: Additional context

        Returns:
            SkillResult
        """
        start_time = datetime.utcnow()

        # Validate parameters
        validation_errors = self._validate_parameters(parameters)
        if validation_errors:
            return SkillResult(
                skill_id=self.skill_id,
                status="failed",
                output={},
                errors=validation_errors
            )

        # Execute skill
        try:
            output = await self.execute(parameters, context or {})

            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()

            self.execution_count += 1

            return SkillResult(
                skill_id=self.skill_id,
                status="success",
                output=output,
                artifacts=output.get("artifacts", []),
                warnings=output.get("warnings", []),
                execution_time_seconds=execution_time,
                metadata={
                    "execution_count": self.execution_count,
                    "version": self.version
                }
            )

        except Exception as e:
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()

            return SkillResult(
                skill_id=self.skill_id,
                status="failed",
                output={},
                errors=[f"Execution error: {str(e)}"],
                execution_time_seconds=execution_time
            )

    @abstractmethod
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute skill logic (must be implemented by subclasses)

        Args:
            parameters: Validated parameters
            context: Execution context

        Returns:
            Dict with:
            - data: Primary output data
            - artifacts: List of created artifacts (optional)
            - warnings: List of warnings (optional)
        """
        pass

    @abstractmethod
    def get_parameters(self) -> List[SkillParameter]:
        """
        Get skill parameter definitions (must be implemented by subclasses)

        Returns:
            List of SkillParameter definitions
        """
        pass

    def _validate_parameters(self, parameters: Dict[str, Any]) -> List[str]:
        """Validate parameters against schema"""
        errors = []
        param_defs = {p.name: p for p in self.get_parameters()}

        # Check required parameters
        for param_name, param_def in param_defs.items():
            if param_def.required and param_name not in parameters:
                errors.append(f"Missing required parameter: {param_name}")
                continue

            # Validate parameter if provided
            value = parameters.get(param_name)
            if value is not None and not param_def.validate(value):
                if param_def.choices:
                    errors.append(
                        f"Invalid value for {param_name}. "
                        f"Must be one of: {', '.join(map(str, param_def.choices))}"
                    )
                else:
                    errors.append(
                        f"Invalid value for {param_name}. "
                        f"Expected type: {param_def.param_type.__name__}"
                    )

        # Check for unknown parameters
        unknown = set(parameters.keys()) - set(param_defs.keys())
        if unknown:
            errors.append(f"Unknown parameters: {', '.join(unknown)}")

        return errors

    def get_schema(self) -> Dict[str, Any]:
        """Get skill schema for documentation"""
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "category": self.category,
            "description": self.description,
            "version": self.version,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.param_type.__name__,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                    "choices": p.choices
                }
                for p in self.get_parameters()
            ]
        }


class SkillRegistry:
    """Registry of all available skills"""

    def __init__(self):
        """Initialize skill registry"""
        self.skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """
        Register a skill

        Args:
            skill: Skill instance
        """
        self.skills[skill.skill_id] = skill

    def get(self, skill_id: str) -> Optional[Skill]:
        """
        Get skill by ID

        Args:
            skill_id: Skill identifier

        Returns:
            Skill instance or None
        """
        return self.skills.get(skill_id)

    def list_skills(
        self,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all skills

        Args:
            category: Filter by category (optional)

        Returns:
            List of skill schemas
        """
        skills = self.skills.values()

        if category:
            skills = [s for s in skills if s.category == category]

        return [s.get_schema() for s in skills]

    def list_categories(self) -> List[str]:
        """Get all skill categories"""
        return list(set(s.category for s in self.skills.values()))


# Global skill registry
_global_registry = SkillRegistry()


def register_skill(skill: Skill) -> None:
    """Register a skill in global registry"""
    _global_registry.register(skill)


def get_skill(skill_id: str) -> Optional[Skill]:
    """Get skill from global registry"""
    return _global_registry.get(skill_id)


def list_skills(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List skills from global registry"""
    return _global_registry.list_skills(category)


class ExampleSkill(Skill):
    """Example skill implementation"""

    def __init__(self):
        super().__init__(
            skill_id="example.hello",
            skill_name="Hello World Skill",
            category="example",
            description="Example skill that returns a greeting"
        )

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(
                name="name",
                param_type=str,
                description="Name to greet",
                required=True
            ),
            SkillParameter(
                name="language",
                param_type=str,
                description="Language for greeting",
                required=False,
                default="english",
                choices=["english", "spanish", "french"]
            )
        ]

    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute example skill"""
        name = parameters["name"]
        language = parameters.get("language", "english")

        greetings = {
            "english": f"Hello, {name}!",
            "spanish": f"¡Hola, {name}!",
            "french": f"Bonjour, {name}!"
        }

        return {
            "data": {
                "greeting": greetings[language],
                "language": language
            }
        }


async def test_skill_framework():
    """Test the skill framework"""
    # Create and register example skill
    skill = ExampleSkill()
    register_skill(skill)

    # Test successful execution
    result = await skill.run({"name": "World", "language": "spanish"})
    print("=== Successful Execution ===")
    print(f"Status: {result.status}")
    print(f"Output: {json.dumps(result.output, indent=2)}")

    # Test validation error
    result = await skill.run({"language": "german"})
    print("\n=== Validation Error ===")
    print(f"Status: {result.status}")
    print(f"Errors: {result.errors}")

    # Test schema
    print("\n=== Skill Schema ===")
    print(json.dumps(skill.get_schema(), indent=2))

    # Test registry
    print("\n=== Registry ===")
    print(f"Registered skills: {len(list_skills())}")
    retrieved = get_skill("example.hello")
    print(f"Retrieved skill: {retrieved.skill_name if retrieved else 'Not found'}")


if __name__ == "__main__":
    asyncio.run(test_skill_framework())
