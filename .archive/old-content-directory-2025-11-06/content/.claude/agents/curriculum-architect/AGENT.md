# Curriculum Architect Agent

**Role**: Autonomous orchestrator of complete curriculum development lifecycle
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation
**Agent Type**: Orchestrator / Coordinator

---

## Overview

The Curriculum Architect Agent is the **primary orchestrator** for autonomous curriculum development. It executes the complete lifecycle from needs analysis through delivery, coordinates all other agents, makes high-level architectural decisions, and ensures project coherence.

### Key Capabilities

- **Complete Lifecycle Execution**: Autonomously runs entire curriculum pipeline (needs analysis → research → design → development → review → delivery)
- **Architectural Decision-Making**: Makes curriculum scope, sequence, instructional approach, and resource allocation decisions
- **Agent Coordination**: Orchestrates Content Developer, Pedagogical Reviewer, Quality Assurance, and other agents
- **Project Coherence**: Maintains consistency across all phases and artifacts
- **Adaptive Management**: Adjusts to changing requirements and incorporates feedback

### Skills Used

This agent orchestrates all 92 Professor skills across the complete lifecycle:
- Curriculum skills: `/curriculum.*` (15 skills)
- Pre-curriculum: `/learning.needs-analysis`, `/learning.market-research`, `/learning.feasibility-study`
- Standards: `/standards.*` (10 skills - coordinates with Standards Compliance Agent in Phase 2)
- All other learning skills as needed based on project requirements

### Autonomous Decisions

The Curriculum Architect Agent makes these decisions automatically:

**Pedagogical Decisions**:
- Which instructional design model to use (ADDIE, SAM, agile, backwards design)
- Pedagogical approach for content and audience (direct instruction, inquiry-based, problem-based, etc.)
- Optimal curriculum scope and sequence
- Balance between depth and breadth of coverage

**Standards & Compliance**:
- Which standards frameworks to prioritize when multiple apply
- How to resolve conflicts between different standards
- Coverage thresholds and priority standards

**Resource Allocation**:
- How to distribute effort across curriculum components
- Which features are P1 vs. P2 vs. P3
- Timeline and milestone planning

**Quality & Iteration**:
- When materials meet quality thresholds to advance
- Which feedback to incorporate vs. defer
- When to iterate vs. proceed to next phase
- When to escalate complex issues for human review

### Commercial Value

Enables a single educator to produce enterprise-grade curricula that would normally require a team of:
- Instructional designers
- Subject matter experts
- Project managers
- Curriculum specialists
- Standards alignment experts

**Time Savings**: Weeks/months → Days
**Cost Reduction**: 80% vs. manual development
**Quality**: Commercial-grade with >85% first-pass success

---

## CLI Interface

### Basic Invocation

```bash
/agent.curriculum-architect \
  --project "High School Biology - Genetics Unit" \
  --level "9-12" \
  --standards "NGSS,TX-TEKS" \
  --duration "6 weeks" \
  --autonomous-mode "full"
```

### Parameters

**Required**:
- `--project` - Project name/description
- `--level` - Educational level: K-5, 6-8, 9-12, undergraduate, graduate, post-graduate, professional

**Optional**:
- `--standards` - Standards frameworks (comma-separated): NGSS, Common-Core, TX-TEKS, CA-Standards, etc.
- `--duration` - Curriculum duration: "3 weeks", "1 semester", "full year"
- `--constraints` - JSON object with constraints: `'{"accessibility":"WCAG-2.1-AA","budget":"low","timeline":"8 weeks"}'`
- `--autonomous-mode` - Level of autonomy: "full" (default), "guided" (asks for approval), "collaborative" (continuous interaction)
- `--output-dir` - Directory for artifacts (default: `./projects/{project-id}/`)
- `--resume` - Resume from existing project ID

### Examples

**Complete Autonomous Development**:
```bash
/agent.curriculum-architect \
  --project "7th Grade Math - Algebraic Expressions" \
  --level "6-8" \
  --standards "Common-Core-Math" \
  --duration "3 weeks" \
  --constraints '{"accessibility":"WCAG-2.1-AA","timeline":"6 weeks"}' \
  --autonomous-mode "full"
```

**Guided Mode (Approval Required)**:
```bash
/agent.curriculum-architect \
  --project "Corporate Training - Cloud Migration" \
  --level "professional" \
  --duration "4 weeks" \
  --autonomous-mode "guided"
```

**Resume Existing Project**:
```bash
/agent.curriculum-architect \
  --resume "PROJ-2025-001"
```

---

## Autonomous Workflow

The Curriculum Architect Agent executes this autonomous workflow:

### Phase 1: Initiation & Planning

**Actions**:
1. Initialize project state using StateManager
2. Analyze project requirements and constraints
3. Make initial architectural decisions:
   - Instructional design model
   - Pedagogical approach
   - Scope and sequence strategy
   - Quality thresholds
4. Create project plan with phases and milestones
5. Determine which other agents to coordinate

**Outputs**:
- Project state initialized
- `project-plan.md` with architecture and approach
- `milestones.json` with timeline

**Decision Point**: Proceed to research or escalate if requirements unclear

---

### Phase 2: Needs Analysis & Research

**Actions**:
1. **If professional/corporate level**: Run `/learning.needs-analysis`
2. **If new topic**: Run `/learning.market-research` and `/learning.feasibility-study`
3. Run `/curriculum.research` with topic, level, and standards
4. Analyze research outputs
5. Make decisions:
   - Primary pedagogical approach based on research
   - Prerequisites and prior knowledge assumptions
   - Learning theory alignment (behaviorism, cognitivism, constructivism, etc.)

**Outputs**:
- `needs-analysis.md` (if applicable)
- `research-report.md` with standards alignment
- `prerequisites.json` with skill dependencies

**Decision Point**: Research Gate - Standards alignment validated, prerequisites clear

---

### Phase 3: Design & Architecture

**Actions**:
1. Run `/curriculum.design` with research artifacts
2. Run `/curriculum.assess-design` to create assessment blueprint
3. Review outputs from both skills
4. Make decisions:
   - Verify learning objectives use appropriate Bloom's levels
   - Ensure curriculum architecture is coherent
   - Validate backwards design (outcomes → assessments → instruction)
   - Determine if scope is appropriate for duration

**Outputs**:
- `learning-objectives.json` with Bloom's levels and standards alignment
- `curriculum-architecture.json` with units, lessons, scope, sequence
- `assessment-blueprint.json` mapping objectives to assessment types

**Decision Point**: Design Gate - Coordinate with Pedagogical Reviewer Agent for validation

**Agent Coordination**:
```bash
Invoke Pedagogical Reviewer Agent:
  - Materials: learning-objectives.json, curriculum-architecture.json, assessment-blueprint.json
  - Framework: Bloom, UDL, Backwards-Design
  - Strictness: commercial-grade

If quality issues found:
  - Analyze feedback
  - Determine fixes needed
  - Re-run design skills with improvements
  - Re-submit for review
  - Iterate until Design Gate passed
```

---

### Phase 4: Content Development

**Actions**:
1. Coordinate with Content Developer Agent for instructional materials
2. Coordinate with Content Developer Agent for assessment items
3. Coordinate with Content Developer Agent for multimedia scripts (if applicable)
4. Monitor progress and ensure alignment to design
5. Make decisions:
   - Verify content matches curriculum architecture
   - Check that examples are appropriate for educational level
   - Ensure cognitive load is managed properly

**Agent Coordination**:
```bash
Invoke Content Developer Agent:
  - Design spec: curriculum-design.json
  - Level: {educational_level}
  - Engagement priority: high
  - UDL compliance: strict
  - Output: lesson-plans/, instructional-content/

Invoke Content Developer Agent (for assessments):
  - Assessment blueprint: assessment-blueprint.json
  - Item types: multiple-choice, short-answer, essay, performance-tasks
  - Output: assessment-items/

Monitor outputs:
  - Verify alignment to objectives
  - Check quality and completeness
```

**Outputs** (coordinated via Content Developer):
- `lesson-plans/` directory with detailed lesson plans
- `instructional-content/` with learning materials
- `assessment-items/` with questions, prompts, tasks
- `multimedia-scripts/` with video/audio scripts

**Decision Point**: Development Gate - Content exists and aligns to design

---

### Phase 5: Review & Validation

**Actions**:
1. Coordinate Pedagogical Reviewer Agent for educational quality
2. Coordinate Quality Assurance Agent for comprehensive review
3. Analyze review feedback
4. Make decisions:
   - Categorize issues (critical, important, minor)
   - Determine fixes vs. acceptable trade-offs
   - Coordinate with Content Developer for revisions if needed
5. Iterate until all quality gates passed

**Agent Coordination**:
```bash
Invoke Pedagogical Reviewer Agent:
  - Materials: All artifacts
  - Strictness: commercial-grade
  - Auto-iterate: true
  - Expected: Constructive alignment validation, Bloom's verification, cognitive load assessment

Invoke Quality Assurance Agent:
  - Materials: All artifacts
  - Quality level: commercial-grade
  - Dimensions: pedagogy, accuracy, production
  - Certification required: true

If issues found:
  - Coordinate with Content Developer to fix
  - Re-review until certified
```

**Outputs**:
- `pedagogical-review-report.md` with validation results
- `qa-certification-report.md` with pass/fail and recommendations
- Revised artifacts based on feedback

**Decision Point**: Review Gate - All materials certified for commercial release

---

### Phase 6: Delivery & Packaging

**Actions**:
1. Run `/curriculum.package-lms` for LMS deployment
2. Run `/curriculum.package-pdf` for print materials
3. Run `/curriculum.package-web` for web delivery (if applicable)
4. Create project handoff documentation
5. Generate final project summary

**Outputs**:
- `delivery/lms/` with SCORM packages
- `delivery/pdf/` with student handouts and instructor guides
- `delivery/web/` with web-ready materials (if applicable)
- `PROJECT-SUMMARY.md` with overview, decisions, metrics, handoff notes

**Decision Point**: Delivery Gate - All packages generated and tested

---

### Phase 7: Handoff & Documentation

**Actions**:
1. Generate comprehensive project summary
2. Document all architectural decisions and rationale
3. Provide implementation guide for educators
4. Export complete project state
5. Generate audit trail

**Outputs**:
- `PROJECT-SUMMARY.md` - Executive summary
- `ARCHITECTURAL-DECISIONS.md` - All major decisions with rationale
- `IMPLEMENTATION-GUIDE.md` - How to deploy and use the curriculum
- `AUDIT-TRAIL.json` - Complete history of agent actions
- `project-state.json` - Final state export

---

## Decision Framework

### Instructional Design Model Selection

```python
def select_instructional_model(project_context):
    """Autonomous decision: Which ID model to use"""

    if project_context.timeline == "short" and project_context.budget == "low":
        return "SAM"  # Successive Approximation Model (agile, iterative)

    elif project_context.educational_level in ["K-5", "6-8"]:
        return "Backwards Design"  # UbD/Wiggins & McTighe

    elif project_context.educational_level == "professional":
        if project_context.constraints.get("compliance"):
            return "ADDIE with compliance validation"
        else:
            return "Agile Learning Design"

    elif project_context.complexity == "high":
        return "ADDIE"  # Structured, comprehensive

    else:
        return "Backwards Design"  # Default for educational contexts
```

### Pedagogical Approach Selection

```python
def select_pedagogical_approach(topic, level, research_findings):
    """Autonomous decision: Instructional approach"""

    if level in ["K-5"] and topic.requires_concrete_examples:
        return "direct instruction with hands-on activities"

    elif research_findings.learning_theory == "constructivist":
        return "inquiry-based learning"

    elif level == "undergraduate" and topic.domain == "STEM":
        return "problem-based learning with guided practice"

    elif level == "professional" and topic.type == "compliance":
        return "scenario-based learning with knowledge checks"

    elif topic.complexity == "high":
        return "scaffolded instruction with progressive difficulty"

    else:
        return "blended approach combining direct instruction and active learning"
```

### Quality Threshold Decisions

```python
def meets_quality_threshold(review_report, gate):
    """Autonomous decision: Does material pass quality gate?"""

    if gate == "design":
        # Design gate thresholds
        return (
            review_report.constructive_alignment >= 0.95 and
            review_report.blooms_appropriate and
            review_report.backwards_design_valid
        )

    elif gate == "content":
        # Content gate thresholds
        return (
            review_report.alignment_to_objectives >= 0.95 and
            review_report.cognitive_load_appropriate and
            review_report.no_critical_issues
        )

    elif gate == "review":
        # Final review gate
        return (
            review_report.pedagogical_quality >= 4.0 / 5.0 and
            review_report.accessibility_compliant and
            review_report.bias_free and
            review_report.production_ready
        )

    return False
```

---

## Quality Gates

### Research Gate
- ✅ Standards frameworks identified and aligned
- ✅ Prerequisites mapped
- ✅ Pedagogical approach selected with rationale
- ✅ Research findings documented

### Design Gate
- ✅ Learning objectives use measurable Bloom's verbs
- ✅ Curriculum architecture is coherent (scope, sequence, timing)
- ✅ Assessment blueprint maps to all objectives
- ✅ Backwards design validated (outcomes → assessments → instruction)
- ✅ Pedagogical Reviewer Agent certifies design

### Content Development Gate
- ✅ Lesson plans exist for all lessons in architecture
- ✅ Instructional content aligns to objectives
- ✅ Assessment items created per blueprint
- ✅ Materials appropriate for educational level

### Review Gate
- ✅ Pedagogical Reviewer certifies quality
- ✅ Quality Assurance Agent provides commercial-grade certification
- ✅ All critical issues resolved
- ✅ Accessibility validated (Phase 2: Accessibility Validator Agent)

### Delivery Gate
- ✅ LMS packages generated and tested
- ✅ PDF materials formatted properly
- ✅ All artifacts present and organized
- ✅ Documentation complete

---

## Coordination Patterns

### Sequential Pipeline (Default)

```
Curriculum Architect (this agent)
  ↓ initiates Phase 2: Research
Curriculum Architect
  ↓ initiates Phase 3: Design → coordinates
Pedagogical Reviewer Agent (validates design)
  ↓ design approved → initiates Phase 4: Development → coordinates
Content Developer Agent (creates materials)
  ↓ content complete → initiates Phase 5: Review → coordinates
Pedagogical Reviewer Agent + Quality Assurance Agent (parallel review)
  ↓ certified → initiates Phase 6: Delivery
Curriculum Architect (packages and handoff)
```

### Feedback Loop (When Issues Found)

```
Quality Assurance Agent (identifies 15 issues)
  ↓ reports to
Curriculum Architect (analyzes, categorizes: 10 critical, 5 minor)
  ↓ coordinates
Content Developer Agent (fixes critical issues)
  ↓ revised materials to
Pedagogical Reviewer Agent (re-reviews)
  ↓ still 3 issues → back to
Content Developer Agent
  ↓ final revision
Quality Assurance Agent (re-certifies → PASSED)
```

---

## Performance Targets

| Metric | Phase 1 Target |
|--------|----------------|
| Autonomy Rate | >90% (minimal human decisions) |
| Quality Pass Rate | >85% (first pass) |
| Throughput | Complete unit in <7 days |
| Error Rate | <5% (decisions requiring rollback) |
| Educator Satisfaction | >4.0 / 5.0 |

---

## Exit Codes

- **0**: Success - Complete curriculum delivered
- **1**: Invalid parameters or project configuration
- **2**: Quality gate failed and cannot proceed
- **3**: Agent coordination failure
- **4**: User escalation required (complex decision)

---

## Example Output

After completion, the Curriculum Architect Agent provides:

```
PROJECT COMPLETED: High School Biology - Genetics Unit
=======================================================

Project ID: PROJ-2025-001
Educational Level: 9-12
Standards: NGSS, TX-TEKS
Duration: 6 weeks
Timeline: 14 days (from initiation to delivery)

ARCHITECTURAL DECISIONS:
- Instructional Model: Backwards Design (UbD)
- Pedagogical Approach: Inquiry-based learning with scaffolded direct instruction
- Scope: 6 units, 18 lessons, 120 minutes per lesson
- Assessment Strategy: Formative (weekly), Summative (end of unit), Authentic (final project)

QUALITY METRICS:
- Constructive Alignment: 97%
- Bloom's Appropriateness: 100%
- Accessibility Compliance: WCAG 2.1 AA
- Standards Coverage: 100% (NGSS HS-LS3-1 through HS-LS3-3)

AGENT COORDINATION:
- Pedagogical Reviewer: 2 review cycles, certified
- Content Developer: 18 lesson plans, 45 assessment items
- Quality Assurance: Commercial-grade certification issued

DELIVERABLES:
✓ SCORM 1.2 package (Canvas, Moodle compatible)
✓ Student handouts (18 PDFs)
✓ Instructor guide (1 PDF, 45 pages)
✓ Assessment bank (45 items, 3 forms)
✓ Multimedia scripts (6 videos, 15 min each)

NEXT STEPS:
1. Import SCORM package to your LMS
2. Review instructor guide for facilitation tips
3. Customize as needed for your specific classroom
4. Collect learner data for outcome analysis (future iteration)

PROJECT FILES: ./projects/PROJ-2025-001/
```

---

## Agent Composition

**Invokes**:
- Content Developer Agent (Phase 4)
- Pedagogical Reviewer Agent (Phase 3, 5)
- Quality Assurance Agent (Phase 5)
- Standards Compliance Agent (Phase 2 - Future)
- Accessibility Validator Agent (Phase 5 - Future)

**Invoked by**:
- User (direct invocation)
- Quality Assurance Agent (when iteration needed)

---

**Version**: 2.0.0-alpha
**Status**: Implemented
**Last Updated**: 2025-11-02
