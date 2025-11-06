# Agent Coordination Framework

**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

This framework defines how Professor agents coordinate, communicate, and manage workflows autonomously.

## Coordination Patterns

### 1. Sequential Pipeline

Agents execute in sequence, each completing before the next begins.

```
Agent A → Agent B → Agent C → Agent D
```

**Example**: Curriculum Architect → Content Developer → Pedagogical Reviewer → Quality Assurance

**When to Use**: Linear workflows where each phase depends on previous completion

### 2. Parallel Execution

Multiple agents execute simultaneously on the same materials.

```
           ┌─ Agent B
Agent A ──→├─ Agent C  ──→ Agent D (aggregates)
           └─ Agent D
```

**Example**: Materials → [Pedagogical Reviewer + Accessibility Validator + Standards Compliance] → Quality Assurance

**When to Use**: Independent review dimensions that can run concurrently

### 3. Feedback Loop

Agent identifies issues, coordinates fixes, re-validates.

```
QA Agent (finds issues) → Curriculum Architect → Content Developer (fixes) → QA Agent (re-validates)
```

**When to Use**: Iterative improvement until quality gates passed

### 4. Hierarchical Orchestration

One agent (orchestrator) coordinates multiple specialized agents.

```
Curriculum Architect (orchestrator)
  ├─ coordinates → Content Developer
  ├─ coordinates → Pedagogical Reviewer
  ├─ coordinates → Standards Compliance
  └─ coordinates → Quality Assurance
```

**When to Use**: Complex multi-phase projects requiring central coordination

## Communication Protocol

### Agent Invocation

Agents communicate via the Task API with structured inputs/outputs.

**Invocation Format**:
```json
{
  "agent": "content-developer",
  "purpose": "Create instructional materials aligned to design",
  "inputs": {
    "design_spec": "curriculum-design.json",
    "level": "9-12",
    "engagement_priority": "high"
  },
  "expected_outputs": [
    "lesson-plans/",
    "instructional-content/",
    "assessment-items/"
  ],
  "quality_requirements": {
    "alignment": ">= 95%",
    "udl_compliance": "strict"
  }
}
```

**Response Format**:
```json
{
  "status": "success",
  "outputs": {
    "lesson_plans": "lesson-plans/",
    "instructional_content": "instructional-content/",
    "assessment_items": "assessment-items/"
  },
  "metrics": {
    "alignment_score": 0.97,
    "lessons_created": 18,
    "items_created": 45
  },
  "issues": [],
  "recommendations": [
    "Consider adding more visual supports for unit 3"
  ]
}
```

### State Sharing

Agents share state via the StateManager:

```python
from framework.state_manager import StateManager

# Agent A writes
sm = StateManager("PROJ-2025-001")
sm.add_artifact("design_spec", "curriculum-design.json")
sm.add_agent_decision(
    agent="curriculum-architect",
    phase="design",
    decisions=["Selected inquiry-based approach"],
    artifacts_created=["curriculum-design.json"]
)

# Agent B reads
context = sm.get_context()
design_spec_path = context["artifacts"]["design_spec"]
previous_decisions = sm.get_latest_decisions(agent="curriculum-architect")
```

### Quality Gate Coordination

```python
# Curriculum Architect initiates review
invoke_agent(
    agent="pedagogical-reviewer",
    materials="design-artifacts/",
    level="9-12",
    strictness="commercial-grade"
)

# Pedagogical Reviewer validates and returns
if review_result.certified:
    sm.pass_quality_gate("design")
    proceed_to_next_phase()
else:
    iterate_on_issues(review_result.issues)
```

## Agent Responsibilities

| Agent | Phase | Responsibility | Coordinates With |
|-------|-------|----------------|------------------|
| Curriculum Architect | All | Orchestrate complete lifecycle | All agents |
| Pedagogical Reviewer | Design, Review | Validate educational quality | Curriculum Architect, Content Developer |
| Content Developer | Development | Create instructional materials | Curriculum Architect, Pedagogical Reviewer |
| Quality Assurance | Review | Certify commercial-grade quality | All agents |

## Error Handling

### Agent Failure

If an agent fails:
1. Log error to project state
2. Attempt recovery (retry once)
3. If still failing, escalate to Curriculum Architect
4. Curriculum Architect decides: manual intervention or alternative approach

```python
try:
    result = invoke_agent("content-developer", inputs)
except AgentError as e:
    log_error(e)
    if retry_count < 1:
        result = invoke_agent("content-developer", inputs)  # Retry once
    else:
        escalate_to_orchestrator(agent="content-developer", error=e)
```

### Quality Gate Failure

If quality gate fails:
1. Agent categorizes issues (critical, important, minor)
2. Coordinates with Content Developer to fix
3. Re-validates
4. If still failing after 2 iterations, escalates

```python
for iteration in range(3):
    review = pedagogical_reviewer.review(materials)

    if review.certified:
        break

    if iteration < 2:
        fixes = content_developer.fix_issues(review.issues)
        materials = fixes.updated_materials
    else:
        escalate_to_human("Quality gate failed after 3 iterations")
```

## Audit Trail

All agent coordination is logged:

```json
{
  "agent_history": [
    {
      "timestamp": "2025-11-02T10:00:00Z",
      "agent": "curriculum-architect",
      "action": "initiated",
      "phase": "research",
      "decisions": ["Selected ADDIE model"],
      "artifacts_created": ["project-plan.md"]
    },
    {
      "timestamp": "2025-11-02T10:15:00Z",
      "agent": "curriculum-architect",
      "action": "coordinated",
      "invoked_agent": "content-developer",
      "purpose": "Create lesson plans",
      "inputs": {"design_spec": "..."},
      "result": "success"
    },
    {
      "timestamp": "2025-11-02T11:00:00Z",
      "agent": "content-developer",
      "action": "completed",
      "outputs": ["lesson-plans/", "instructional-content/"],
      "metrics": {"lessons": 18, "alignment": 0.97}
    }
  ]
}
```

## Performance Monitoring

Track coordination efficiency:
- **Handoff Time**: Time between agent completions
- **Iteration Cycles**: Number of review/fix cycles
- **Parallel Efficiency**: Speedup from parallel execution
- **Coordination Overhead**: Time spent coordinating vs. executing

---

**Status**: Phase 1 framework complete. Supports 4 agents: Curriculum Architect, Pedagogical Reviewer, Content Developer, Quality Assurance.

**Next**: Phase 2 will add Standards Compliance and Accessibility Validator agents.
