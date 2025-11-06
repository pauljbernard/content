#!/usr/bin/env python3
"""
Professor Skill Executor

Executes skills on behalf of agents. Provides caching, retry logic,
parallel execution, and integration with the agent framework.

Usage:
    from skill_executor import SkillExecutor

    executor = SkillExecutor()
    result = await executor.execute_skill("curriculum.research", {"topic": "genetics"})
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import hashlib

from skill_base import Skill, SkillResult, get_skill, list_skills


@dataclass
class CachedResult:
    """Cached skill result"""
    skill_id: str
    parameters_hash: str
    result: SkillResult
    cached_at: datetime
    ttl_seconds: int


@dataclass
class ExecutionPlan:
    """Plan for executing multiple skills"""
    skills: List[Dict[str, Any]]
    dependencies: Dict[str, List[str]]  # skill_id -> list of dependency skill_ids
    parallel_groups: List[List[str]]  # Groups of skills that can run in parallel


class SkillExecutor:
    """Executes Professor skills"""

    def __init__(
        self,
        cache_enabled: bool = True,
        default_cache_ttl_seconds: int = 3600
    ):
        """
        Initialize skill executor

        Args:
            cache_enabled: Enable result caching
            default_cache_ttl_seconds: Default cache TTL (1 hour)
        """
        self.cache_enabled = cache_enabled
        self.default_cache_ttl = default_cache_ttl_seconds
        self.cache: Dict[str, CachedResult] = {}
        self.execution_log: List[Dict[str, Any]] = []

    async def execute_skill(
        self,
        skill_id: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
        cache_ttl_seconds: Optional[int] = None
    ) -> SkillResult:
        """
        Execute a single skill

        Args:
            skill_id: Skill identifier
            parameters: Skill parameters
            context: Execution context
            use_cache: Use cached result if available
            cache_ttl_seconds: Cache TTL override

        Returns:
            SkillResult
        """
        # Check cache
        if use_cache and self.cache_enabled:
            cached = self._get_cached_result(skill_id, parameters)
            if cached:
                cached.result.metadata["from_cache"] = True
                return cached.result

        # Get skill
        skill = get_skill(skill_id)
        if not skill:
            return SkillResult(
                skill_id=skill_id,
                status="failed",
                output={},
                errors=[f"Skill not found: {skill_id}"]
            )

        # Execute skill
        result = await skill.run(parameters, context)

        # Cache result
        if self.cache_enabled and result.status == "success":
            self._cache_result(
                skill_id,
                parameters,
                result,
                cache_ttl_seconds or self.default_cache_ttl
            )

        # Log execution
        self._log_execution(skill_id, parameters, result)

        return result

    async def execute_skill_with_retry(
        self,
        skill_id: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        retry_delay_seconds: float = 1.0
    ) -> SkillResult:
        """
        Execute skill with retry logic

        Args:
            skill_id: Skill identifier
            parameters: Skill parameters
            context: Execution context
            max_retries: Maximum number of retries
            retry_delay_seconds: Delay between retries

        Returns:
            SkillResult
        """
        retries = 0

        while retries <= max_retries:
            result = await self.execute_skill(
                skill_id,
                parameters,
                context,
                use_cache=(retries == 0)  # Only use cache on first attempt
            )

            if result.status == "success":
                result.metadata["retries"] = retries
                return result

            retries += 1

            if retries <= max_retries:
                await asyncio.sleep(retry_delay_seconds)

        result.metadata["retries"] = retries
        result.errors.append(f"Failed after {retries} retries")
        return result

    async def execute_skills_parallel(
        self,
        skill_calls: List[Dict[str, Any]]
    ) -> List[SkillResult]:
        """
        Execute multiple skills in parallel

        Args:
            skill_calls: List of dicts with skill_id, parameters, context

        Returns:
            List of SkillResults
        """
        tasks = [
            self.execute_skill(
                call["skill_id"],
                call.get("parameters", {}),
                call.get("context")
            )
            for call in skill_calls
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to failed results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(SkillResult(
                    skill_id=skill_calls[i]["skill_id"],
                    status="failed",
                    output={},
                    errors=[f"Exception: {str(result)}"]
                ))
            else:
                processed_results.append(result)

        return processed_results

    async def execute_skills_sequential(
        self,
        skill_calls: List[Dict[str, Any]],
        pass_outputs: bool = True
    ) -> List[SkillResult]:
        """
        Execute multiple skills sequentially

        Args:
            skill_calls: List of dicts with skill_id, parameters, context
            pass_outputs: Pass previous outputs as context to next skills

        Returns:
            List of SkillResults
        """
        results = []
        accumulated_context = {}

        for call in skill_calls:
            context = {**call.get("context", {}), **accumulated_context}

            result = await self.execute_skill(
                call["skill_id"],
                call.get("parameters", {}),
                context
            )

            results.append(result)

            # Accumulate outputs for next skill
            if pass_outputs and result.status == "success":
                accumulated_context[f"{call['skill_id']}_output"] = result.output

        return results

    async def execute_plan(self, plan: ExecutionPlan) -> Dict[str, SkillResult]:
        """
        Execute an execution plan with dependencies

        Args:
            plan: ExecutionPlan

        Returns:
            Dict mapping skill_id to SkillResult
        """
        results = {}
        skills_by_id = {s["skill_id"]: s for s in plan.skills}

        # Execute parallel groups in sequence
        for group in plan.parallel_groups:
            # Build skill calls for this group
            skill_calls = []
            for skill_id in group:
                skill_info = skills_by_id[skill_id]

                # Add dependency outputs to context
                context = skill_info.get("context", {})
                deps = plan.dependencies.get(skill_id, [])
                for dep_id in deps:
                    if dep_id in results:
                        context[f"{dep_id}_output"] = results[dep_id].output

                skill_calls.append({
                    "skill_id": skill_id,
                    "parameters": skill_info.get("parameters", {}),
                    "context": context
                })

            # Execute group in parallel
            group_results = await self.execute_skills_parallel(skill_calls)

            # Store results
            for skill_id, result in zip(group, group_results):
                results[skill_id] = result

        return results

    def create_execution_plan(
        self,
        skill_calls: List[Dict[str, Any]]
    ) -> ExecutionPlan:
        """
        Create execution plan from skill calls with dependencies

        Args:
            skill_calls: List of dicts with skill_id, parameters, dependencies

        Returns:
            ExecutionPlan with parallel groups
        """
        # Build dependency graph
        dependencies = {}
        for call in skill_calls:
            dependencies[call["skill_id"]] = call.get("dependencies", [])

        # Topological sort to find execution order
        parallel_groups = []
        remaining = set(call["skill_id"] for call in skill_calls)
        completed: Set[str] = set()

        while remaining:
            # Find skills with all dependencies satisfied
            ready = [
                skill_id for skill_id in remaining
                if all(dep in completed for dep in dependencies.get(skill_id, []))
            ]

            if not ready:
                # Circular dependency
                raise ValueError(f"Circular dependencies detected in: {remaining}")

            parallel_groups.append(ready)
            completed.update(ready)
            remaining -= set(ready)

        return ExecutionPlan(
            skills=skill_calls,
            dependencies=dependencies,
            parallel_groups=parallel_groups
        )

    def _get_cached_result(
        self,
        skill_id: str,
        parameters: Dict[str, Any]
    ) -> Optional[CachedResult]:
        """Get cached result if available and not expired"""
        cache_key = self._get_cache_key(skill_id, parameters)

        if cache_key in self.cache:
            cached = self.cache[cache_key]

            # Check if expired
            age = (datetime.utcnow() - cached.cached_at).total_seconds()
            if age < cached.ttl_seconds:
                return cached
            else:
                # Remove expired cache
                del self.cache[cache_key]

        return None

    def _cache_result(
        self,
        skill_id: str,
        parameters: Dict[str, Any],
        result: SkillResult,
        ttl_seconds: int
    ) -> None:
        """Cache a skill result"""
        cache_key = self._get_cache_key(skill_id, parameters)
        params_hash = hashlib.md5(
            json.dumps(parameters, sort_keys=True).encode()
        ).hexdigest()

        self.cache[cache_key] = CachedResult(
            skill_id=skill_id,
            parameters_hash=params_hash,
            result=result,
            cached_at=datetime.utcnow(),
            ttl_seconds=ttl_seconds
        )

    def _get_cache_key(self, skill_id: str, parameters: Dict[str, Any]) -> str:
        """Generate cache key"""
        params_json = json.dumps(parameters, sort_keys=True)
        params_hash = hashlib.md5(params_json.encode()).hexdigest()
        return f"{skill_id}:{params_hash}"

    def _log_execution(
        self,
        skill_id: str,
        parameters: Dict[str, Any],
        result: SkillResult
    ) -> None:
        """Log skill execution"""
        self.execution_log.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "skill_id": skill_id,
            "status": result.status,
            "execution_time_seconds": result.execution_time_seconds,
            "from_cache": result.metadata.get("from_cache", False)
        })

    def clear_cache(self, skill_id: Optional[str] = None) -> int:
        """
        Clear cache

        Args:
            skill_id: Clear only this skill's cache (or all if None)

        Returns:
            Number of entries cleared
        """
        if skill_id:
            keys_to_remove = [
                k for k in self.cache.keys()
                if k.startswith(f"{skill_id}:")
            ]
            for key in keys_to_remove:
                del self.cache[key]
            return len(keys_to_remove)
        else:
            count = len(self.cache)
            self.cache.clear()
            return count

    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        total_executions = len(self.execution_log)
        cached_executions = sum(
            1 for log in self.execution_log
            if log.get("from_cache", False)
        )
        successful = sum(
            1 for log in self.execution_log
            if log["status"] == "success"
        )
        total_time = sum(
            log["execution_time_seconds"]
            for log in self.execution_log
        )

        return {
            "total_executions": total_executions,
            "cached_executions": cached_executions,
            "cache_hit_rate": cached_executions / total_executions if total_executions > 0 else 0,
            "success_rate": successful / total_executions if total_executions > 0 else 0,
            "total_execution_time_seconds": total_time,
            "average_execution_time_seconds": total_time / total_executions if total_executions > 0 else 0,
            "cache_size": len(self.cache)
        }

    def export_execution_log(self, output_path: Path) -> None:
        """Export execution log to JSON"""
        log_data = {
            "execution_log": self.execution_log,
            "stats": self.get_execution_stats()
        }

        with open(output_path, 'w') as f:
            json.dump(log_data, f, indent=2)


async def test_skill_executor():
    """Test the skill executor"""
    from skill_base import ExampleSkill, register_skill

    # Register example skill
    skill = ExampleSkill()
    register_skill(skill)

    executor = SkillExecutor()

    # Test 1: Single execution
    print("=== Single Execution ===")
    result = await executor.execute_skill(
        "example.hello",
        {"name": "World", "language": "english"}
    )
    print(f"Status: {result.status}")
    print(f"Output: {json.dumps(result.output, indent=2)}")

    # Test 2: Cached execution
    print("\n=== Cached Execution ===")
    result = await executor.execute_skill(
        "example.hello",
        {"name": "World", "language": "english"}
    )
    print(f"From cache: {result.metadata.get('from_cache', False)}")

    # Test 3: Parallel execution
    print("\n=== Parallel Execution ===")
    results = await executor.execute_skills_parallel([
        {"skill_id": "example.hello", "parameters": {"name": "Alice", "language": "spanish"}},
        {"skill_id": "example.hello", "parameters": {"name": "Bob", "language": "french"}},
        {"skill_id": "example.hello", "parameters": {"name": "Charlie", "language": "english"}}
    ])
    for r in results:
        print(f"{r.skill_id}: {r.output.get('data', {}).get('greeting', 'N/A')}")

    # Test 4: Execution plan with dependencies
    print("\n=== Execution Plan ===")
    plan = executor.create_execution_plan([
        {"skill_id": "example.hello", "parameters": {"name": "Step1", "language": "english"}, "dependencies": []},
        {"skill_id": "example.hello", "parameters": {"name": "Step2", "language": "spanish"}, "dependencies": ["example.hello"]},
        {"skill_id": "example.hello", "parameters": {"name": "Step3", "language": "french"}, "dependencies": ["example.hello"]}
    ])
    print(f"Parallel groups: {plan.parallel_groups}")

    # Test 5: Statistics
    print("\n=== Execution Statistics ===")
    stats = executor.get_execution_stats()
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    asyncio.run(test_skill_executor())
