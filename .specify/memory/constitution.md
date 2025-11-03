<!--
SYNC IMPACT REPORT
==================
Version Change: 1.1.0 → 1.2.0 (MINOR: New principle added for agentic architecture)
Changes:
  - Added Principle VIII: Agentic Autonomy - Autonomous Claude sub-agents for commercial-grade quality at scale
  - Added 12 specialized agents: Curriculum Architect, Pedagogical Reviewer, Standards Compliance, Adaptive Learning, Assessment Designer, Content Developer, Accessibility Validator, Learning Analytics, Instructional Designer, Quality Assurance, Localization, Corporate Training
  - Added agent coordination patterns: sequential pipelines, parallel review, feedback loops, multi-market rollout
  - Added enterprise requirements: multi-tenant, RBAC, audit trails, compliance documentation
  - Added performance targets: >90% autonomy, >85% quality pass rate, 5-10x throughput
  - Expanded scope: Skill-based toolkit → Fully autonomous learning engineering system

Templates Status:
  - ✅ .specify/templates/plan-template.md - UPDATED with all 8 principles + Agentic Gate
  - ✅ .specify/templates/spec-template.md - Compatible (agent requirements added to spec.md)
  - ✅ .specify/templates/tasks-template.md - Compatible (agent implementation phases)

Agent Architecture:
  - ✅ professor/AGENT_ARCHITECTURE.md - Complete agent design specification
  - ✅ specs/001-curriculum-skills-suite/spec.md - FR-062 through FR-098 (37 new functional requirements)
  - ⏳ Agent implementations - Planned for Phase 1-6 roadmap (18 month timeline)

Follow-up TODOs:
  - Implement Phase 1 agents (Curriculum Architect, Pedagogical Reviewer, Content Developer, Quality Assurance)
  - Build agent coordination framework with state management
  - Create agent testing and evaluation harness
  - Develop multi-tenant platform architecture
-->

# Professor Constitution

A comprehensive curriculum and assessment engineering platform enabling single-author creation of educational materials across the complete educational spectrum: kindergarten through 12th grade (K-12), undergraduate (4-year college), graduate (Master's), post-graduate (PhD/Doctoral), and professional learning (corporate training, continuing education), using Claude skills.

## Core Principles

### I. CLI-First Interface

Every feature MUST expose its functionality through a command-line interface. This ensures accessibility, automation, composability, and testability.

**Requirements**:
- All functionality accessible via CLI commands with clear argument structure
- Text-based I/O protocol: stdin/arguments → stdout for results, stderr for errors
- Support both JSON (machine-readable) and human-readable output formats
- Commands MUST be documented with `--help` flags
- Exit codes MUST follow POSIX conventions (0 = success, non-zero = error)

**Rationale**: CLI-first design enables scripting, automation, integration with other tools, and provides a stable interface contract that can be tested programmatically. Educational tools benefit from composability and reproducible workflows.

### II. Educational Clarity

All code, documentation, and interfaces MUST prioritize clarity and learning over clever solutions. The system should teach good practices by example.

**Requirements**:
- Code MUST be self-documenting with clear variable/function names
- Complex logic MUST include explanatory comments describing "why", not "what"
- Error messages MUST be instructive, explaining both the problem and potential solutions
- Documentation MUST include examples for every feature
- Abstractions MUST be justified - avoid premature generalization

**Rationale**: As an educational tool, Professor's codebase itself serves as a teaching resource. Clear, maintainable code that explains its own purpose helps users understand both the tool and good software engineering practices.

### III. Incremental Value Delivery

Features MUST be designed and implemented as independently testable user stories that deliver value incrementally. Each story should function standalone.

**Requirements**:
- Features MUST be broken into prioritized user stories (P1, P2, P3...)
- Each user story MUST be independently implementable and testable
- P1 stories MUST represent a viable MVP (Minimum Viable Product)
- Implementation MUST proceed in priority order unless parallelized
- Each story completion MUST be demonstrable to users independently

**Rationale**: Incremental delivery reduces risk, enables early feedback, and ensures that even partial implementations provide user value. This aligns with modern agile practices and makes development progress visible.

### IV. Skills-First Architecture

All curriculum and assessment engineering capabilities MUST be implemented as Claude skills that extend Claude Code's tooling ecosystem.

**Requirements**:
- Each educational capability (curriculum design, assessment creation, rubric generation, etc.) implemented as a discrete Claude skill
- Skills MUST follow the skill-creator pattern with clear prompts, tools, and workflows
- Skills MUST compose with each other to support complex workflows
- Skills MUST expose CLI interfaces (via Principle I)
- Skill descriptions MUST clearly indicate when to invoke them (trigger patterns)

**Rationale**: Claude skills provide a modular, extensible architecture that leverages Claude Code's existing infrastructure. This approach enables rapid development, easy testing, and natural composition of educational tools. Users interact with familiar Claude Code patterns while gaining domain-specific curriculum engineering capabilities.

### V. Lifecycle Coverage

Professor MUST support the complete curriculum and assessment engineering lifecycle from research through delivery and iteration.

**Required Lifecycle Phases**:
1. **Research** - Subject matter research, standards alignment, prerequisite analysis
2. **Design** - Learning objectives, curriculum architecture, assessment design
3. **Development** - Content creation, assessment item writing, rubric development
4. **Review** - Pedagogical review, bias detection, accessibility validation
5. **Delivery** - Format generation (LMS, PDF, web), distribution packaging
6. **Assessment** - Grading tools, analytics, learning outcome measurement
7. **Iteration** - Feedback collection, revision tracking, continuous improvement

**Requirements**:
- Each phase MUST have dedicated Claude skills
- Artifacts from one phase MUST inform subsequent phases
- Traceability from learning objectives → content → assessments → outcomes
- Version control for curriculum revisions

**Rationale**: Curriculum engineering is not just content creation—it's a rigorous, iterative process. Supporting the full lifecycle ensures quality, alignment, and continuous improvement. Each phase builds on the previous, creating a comprehensive system.

### VI. Educational Spectrum

Professor MUST support creation of educational materials across the complete educational spectrum from kindergarten through post-graduate education and professional learning.

**Required Level Support**:
- **K-5**: Age-appropriate language, visual learning emphasis, foundational skills
- **6-8**: Transitional complexity, skill building, exploratory learning
- **9-12**: Subject depth, college preparation, critical thinking
- **Undergraduate**: Disciplinary foundations (4-year college degrees in any subject), research introduction, professional preparation
- **Graduate**: Advanced theory (Master's level), original research, professional practice
- **Post-Graduate**: Cutting-edge research (PhD/Doctoral level), specialization, thought leadership
- **Professional**: Corporate training, continuing education, professional development, workplace application, ROI focus

**Requirements**:
- Skills MUST adapt output to specified educational level
- Vocabulary, complexity, and cognitive load MUST match target audience
- Assessment types MUST be age/level appropriate
- Standards alignment for K-12 (Common Core, NGSS, etc.)
- Discipline-specific conventions for higher education

**Rationale**: A single person should be able to create materials for any educational level without becoming an expert in developmental psychology or pedagogical theory for each level. Professor embeds this expertise in its skills.

### VII. Pedagogical Rigor

All curriculum and assessment design MUST be grounded in evidence-based instructional design principles and learning science.

**Required Foundations**:
- **Bloom's Taxonomy** - Cognitive skill levels in learning objectives and assessments
- **Backwards Design** - Start with outcomes, design assessments, then instruction
- **Constructive Alignment** - Learning objectives, activities, and assessments aligned
- **Universal Design for Learning (UDL)** - Multiple means of representation, engagement, expression
- **Assessment Validity** - Assessments measure intended learning objectives
- **Bias Awareness** - Cultural responsiveness, accessibility, equity considerations

**Requirements**:
- Learning objectives MUST use measurable action verbs (Bloom's Taxonomy)
- Assessments MUST map explicitly to learning objectives
- Curriculum designs MUST justify pedagogical approach
- Content MUST be reviewed for bias, accessibility, and inclusive language
- Cognitive load MUST be managed appropriately for level
- Rubrics MUST have clear criteria and performance levels

**Rationale**: Educational quality is not subjective. Learning science provides evidence-based principles that improve outcomes. Professor embeds these principles to ensure a single author can create pedagogically sound materials without a PhD in education.

### VIII. Agentic Autonomy

Professor 2.0 introduces autonomous Claude sub-agents that orchestrate skills, make intelligent decisions, and deliver commercial-grade quality at scale.

**Required Agent Capabilities**:
- **Autonomous Orchestration** - Agents execute multi-phase workflows without constant human intervention
- **Intelligent Decision-Making** - Agents make pedagogical, quality, compliance, and architectural decisions based on context and best practices
- **Quality Assurance at Scale** - Automated review and validation ensures consistent quality across thousands of materials
- **Adaptive Personalization** - Real-time learning path adaptation based on learner performance
- **Continuous Improvement** - Agents learn from outcomes and feedback to improve over time
- **Enterprise Reliability** - Graceful error handling, audit trails, rollback capabilities, and reproducible builds

**Requirements**:
- 12 specialized agents MUST cover all phases: Curriculum Architect, Pedagogical Reviewer, Standards Compliance, Adaptive Learning, Assessment Designer, Content Developer, Accessibility Validator, Learning Analytics, Instructional Designer, Quality Assurance, Localization, Corporate Training
- Agents MUST achieve >90% autonomy rate (decisions without human intervention)
- Agents MUST achieve >85% quality pass rate (materials passing all gates first time)
- Agents MUST maintain complete audit trails (decisions, rationales, artifacts, scores)
- Agents MUST support human-in-the-loop escalation for complex issues
- Agents MUST coordinate via sequential pipelines, parallel review, feedback loops, and multi-market patterns
- Agent platform MUST support 100+ concurrent projects with multi-tenant architecture
- Agent platform MUST provide enterprise features (RBAC, SSO, audit, compliance documentation)

**Rationale**: Autonomous agents elevate Professor from a toolkit to a fully autonomous learning engineering system that rivals the output of entire instructional design teams. By combining specialized skills with intelligent orchestration, Professor delivers commercial-grade quality at scale while maintaining pedagogical rigor and accessibility.

## Curriculum Lifecycle

### Workflow Overview

Professor supports a specification-driven curriculum engineering workflow:

```
1. Research Phase
   ↓ /curriculum.research [topic, level, standards]
   → Subject matter synthesis, prerequisite maps, standards alignment

2. Design Phase
   ↓ /curriculum.design [research artifacts]
   → Learning objectives, curriculum architecture, assessment blueprint

3. Development Phase
   ↓ /curriculum.develop [design artifacts]
   → Lesson plans, content, assessment items, rubrics

4. Review Phase
   ↓ /curriculum.review [content artifacts]
   → Pedagogical review, bias detection, accessibility check

5. Delivery Phase
   ↓ /curriculum.package [reviewed artifacts, format]
   → LMS packages, PDFs, web content, distribution ready

6. Assessment Phase
   ↓ /curriculum.assess [student work, rubrics]
   → Grading assistance, analytics, outcome measurement

7. Iteration Phase
   ↓ /curriculum.iterate [outcomes, feedback]
   → Revision recommendations, version tracking
```

### Skill Integration with SpecKit

Professor curriculum skills integrate with the existing SpecKit workflow:

- `/speckit.specify` - Define curriculum feature requirements
- `/speckit.plan` - Design skill architecture for new capabilities
- `/speckit.tasks` - Generate implementation tasks for skills
- `/speckit.implement` - Build and test curriculum skills

SpecKit handles Professor's **development**, while curriculum skills handle **educational content engineering**.

## Development Workflow

### Specification-Driven Development

All features MUST begin with a written specification (`spec.md`) that defines user scenarios, requirements, and success criteria before any implementation planning.

**Process**:
1. User provides feature description → `/speckit.specify` generates `spec.md`
2. Clarify ambiguities → `/speckit.clarify` refines specification
3. Plan implementation → `/speckit.plan` creates technical design
4. Generate tasks → `/speckit.tasks` produces actionable task list
5. Implement → `/speckit.implement` executes task-by-task

### Quality Gates

All features MUST pass these gates before merging:

- **Specification Gate**: Clear user stories with acceptance criteria
- **Design Gate**: Technical plan addresses constitution principles
- **Implementation Gate**: Code matches specification requirements
- **Documentation Gate**: CLI help, examples, and user docs complete
- **Pedagogical Gate** (for curriculum skills): Evidence-based design validated

### Complexity Justification

Any deviation from simplicity MUST be explicitly justified in the implementation plan's "Complexity Tracking" section. Simpler alternatives MUST be documented and explained why they were rejected.

## Governance

### Authority

This constitution supersedes all other development practices. When conflicts arise between convenience and constitutional principles, principles take precedence.

### Amendment Procedure

Amendments to this constitution require:
1. Documented rationale explaining the need for change
2. Version bump following semantic versioning (MAJOR.MINOR.PATCH)
3. Update to all dependent templates (plan, spec, tasks)
4. Sync Impact Report detailing affected artifacts

### Versioning Policy

- **MAJOR**: Backward-incompatible changes (principle removal/redefinition)
- **MINOR**: New principles or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, non-semantic fixes

### Compliance Review

All pull requests and code reviews MUST verify compliance with:
- CLI-first interface requirements
- Educational clarity standards
- Incremental value delivery structure
- Skills-first architecture (modular, composable Claude skills)
- Lifecycle coverage (artifacts support full curriculum workflow)
- Educational spectrum support (appropriate for target level)
- Pedagogical rigor (evidence-based, aligned, accessible)
- Agentic autonomy (autonomous agents, quality at scale, enterprise reliability)
- Specification-driven workflow adherence

**Version**: 1.2.0 | **Ratified**: 2025-11-02 | **Last Amended**: 2025-11-02
