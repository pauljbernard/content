# Content Repository - Claude Code Configuration

## Project Overview

This repository provides **two integrated systems** for educational content development:

1. **HMH Multi-Curriculum Knowledge Base** - A hierarchical, reusable knowledge system (50 files) for creating standards-aligned instructional materials across any state, any subject, any grade level with 85-97% knowledge reuse
2. **Professor Framework Integration** - AI-powered content development with 92 specialized skills and 22 autonomous agents

**Purpose**: Create, manage, and publish high-quality educational content across all educational levels (K-12, undergraduate, graduate, post-graduate, and professional learning).

**Repository**: https://github.com/pauljbernard/content
**Professor Framework**: https://github.com/pauljbernard/professor (private)

---

## HMH Multi-Curriculum Knowledge Base (NEW - Week 3 Complete)

### What It Is

A **hierarchical knowledge resolution system** that enables creating standards-aligned, state-compliant instructional materials with **85-97% knowledge reuse** across curricula.

**Location**: `/reference/hmh-knowledge-v2/`
**Status**: Week 3 Complete (50 files, 94%)
**Documentation**: See [`USER_GUIDE.md`](USER_GUIDE.md) for complete engineering guide

### Current Coverage

**States**: Texas (TEKS), California (CCSS/NGSS), Florida (MAFS/B.E.S.T./NGSSS)
**Subjects**: Mathematics (K-8), ELA (K-8), Science (K-8)
**Curricula**: 4 HMH programs (Into Math TX/CA/FL, Into Reading TX)

### 5-Level Hierarchical Architecture

Knowledge resolution order (specific → general, first match wins):

```
1. Program-Specific    → /subjects/mathematics/districts/texas/into-math/
2. Subject-District    → /subjects/mathematics/districts/texas/
3. Subject-Common      → /subjects/mathematics/common/
4. District-Wide       → /districts/texas/
5. Universal           → /universal/
```

### Key Knowledge Files

**Universal (15 files) - ALL curricula use:**
- UDL Principles, DOK Framework, EB Scaffolding, Sentence Frames
- WCAG 2.1 AA Compliance, CEID Guidelines
- 8 Assessment files (item types, rubrics, answer keys, validation, etc.)

**Math Common (12 files) - ALL math programs use:**
- 8 Math Language Routines (MLR1-MLR8)
- Math vocabulary guidelines, problem-solving framework

**ELA Common (5 files) - ALL ELA programs use:**
- Close Reading, Think-Pair-Share, Annotation, Turn-and-Talk

**Science Common (2 files) - ALL NGSS states use:**
- NGSS alignment, Science Practices Framework (8 SEPs)

**District-Wide (9 files) - ALL subjects in that state use:**
- Texas: IPACC, SBOE, ELPS, compliance checklist
- California: Adoption criteria, ELD Standards
- Florida: Adoption criteria, ESOL/WIDA, statutory compliance

**Subject-District (7 files) - State + subject specific:**
- TEKS Math/ELA, CCSS-M, MAFS alignments

### How Claude Code Should Use This

**When generating state/subject-specific content:**

1. **Check for curriculum config** in `/config/curriculum/`
   - `hmh-math-tx.json`, `hmh-math-ca.json`, `hmh-math-fl.json`, `hmh-ela-tx.json`

2. **Follow resolution order** defined in config to find relevant knowledge files
   - Start with most specific (program-specific)
   - Fall back to more general levels as needed
   - Combine knowledge from multiple levels

3. **Apply combined knowledge** when creating content
   - Universal frameworks (UDL, DOK, WCAG) + Subject routines (MLRs) + State standards (TEKS) + State compliance (SBOE)

4. **Leverage knowledge reuse**
   - 85-97% of content guidance comes from reusable files
   - Only 3-15% needs to be state/program-specific

**Example Query**: "Create a 5th grade Texas Math lesson on fractions"

**Resolution Process**:
1. Load `hmh-math-tx.json` config
2. Gather knowledge from:
   - `/subjects/mathematics/common/mlr/` (all 8 MLRs)
   - `/subjects/mathematics/common/vocab-guidelines.md`
   - `/subjects/mathematics/districts/texas/teks-math-alignment.md` (5th grade fractions standards)
   - `/districts/texas/language/elps-alignment.md` (language scaffolding)
   - `/districts/texas/compliance/sboe-quality-rubric.md`
   - `/universal/frameworks/udl-principles-guide.md`
   - `/universal/frameworks/eb-scaffolding-guide.md`
   - `/universal/assessment/item-types-reference.md`
3. Combine guidance to create lesson aligned to TEKS, ELPS, SBOE standards with MLRs and UDL

### Adding New States/Subjects

**For Engineers**: See [`USER_GUIDE.md`](USER_GUIDE.md) for step-by-step instructions, templates, and examples.

**Quick Summary**:
- **CCSS/NGSS State**: 2-3 files (90-95% reuse)
- **State-Specific Standards**: 5-6 files (85-90% reuse)
- **New Subject**: 8-10 subject-common files + 1-2 per state

### Known Gaps

**See**: [`INCOMPLETE_ANALYSIS.md`](INCOMPLETE_ANALYSIS.md) for complete analysis.

**Critical (easy fixes):**
- 3 configs still use old `/reference/hmh-knowledge/` paths (should be `hmh-knowledge-v2`)
- Program-specific directories referenced but don't exist yet

**Moderate (small gaps):**
- ELA California/Florida subject-district files missing
- Science state-specific files missing (TX/CA/FL)

**Future expansion:**
- High school (9-12)
- 7+ additional subjects (Social Studies, CS, Arts, PE, World Languages, etc.)
- 48 additional states/districts
- Estimated 245-310 total files for complete national coverage

---

## Professor Framework Integration

This repository integrates the complete Professor framework, which provides:

### **92 Composable Skills**
Organized into 19 categories covering the complete educational development lifecycle:
- Research & Design (standards alignment, needs analysis, learning objectives)
- Content Development (lessons, assessments, multimedia, activities)
- Review & Quality (pedagogy, bias detection, accessibility)
- Packaging & Delivery (SCORM, PDF, web, LMS integration)
- Assessment & Analytics (grading, outcome analysis, impact measurement)
- Personalization (adaptive learning, diagnostics, recommendations)
- Support & Infrastructure (tutoring, help systems, version control)

### **22 Autonomous Agents**
Intelligent agents that orchestrate skills and make pedagogical decisions:
- **curriculum-architect**: Designs complete curriculum structures
- **content-developer**: Creates learning materials and content
- **assessment-designer**: Designs assessments and rubrics
- **pedagogical-reviewer**: Reviews pedagogical soundness
- **quality-assurance**: Ensures quality standards
- **standards-compliance**: Validates standards alignment
- **scorm-validator**: Validates SCORM packages
- **learning-analytics**: Analyzes learning outcomes
- **project-planning**: Plans educational projects
- **review-workflow**: Manages review processes
- **content-library**: Manages content repositories
- **rights-management**: Handles content rights and licensing
- **performance-optimization**: Optimizes content delivery
- **platform-training**: Provides platform training
- **ab-testing**: Conducts A/B testing on content
- **market-intelligence**: Analyzes market and trends
- **sales-enablement**: Supports sales with content
- And more...

### **Framework Components**
- **Spec-Kit Integration**: Specification-driven development workflows
- **API Integration**: Connect to external educational platforms
- **Client Portal**: Content delivery and management
- **Agent Coordination**: Multi-agent orchestration system

---

## How Claude Code Should Work in This Repository

### **Access to Professor Components**

When working in this repository, Claude Code has access to:

1. **All Professor Skills** (92 skills via `/` commands)
   - Example: `/curriculum.research "topic" --level "9-12" --standards "NGSS"`
   - Example: `/curriculum.develop-content --objectives objectives.json`
   - Example: `/learning.diagnostic-assessment --format "adaptive"`

2. **All Professor Agents** (22 agents for autonomous workflows)
   - Agents are invoked automatically based on task context
   - Can be explicitly requested: "Use the curriculum-architect agent to design..."

3. **Spec-Kit Commands** (8 commands for specification-driven development)
   - `/speckit.constitution` - Establish project principles
   - `/speckit.specify` - Create baseline specification
   - `/speckit.plan` - Create implementation plan
   - `/speckit.tasks` - Generate actionable tasks
   - `/speckit.implement` - Execute implementation
   - `/speckit.clarify` - Ask structured questions
   - `/speckit.analyze` - Cross-artifact consistency
   - `/speckit.checklist` - Generate quality checklists

4. **Framework Tools** (API integration, client portal components)

### **Content Development Standards**

**Quality Requirements:**
- All content must be pedagogically sound (evidence-based learning science)
- Accessibility: WCAG 2.1 AA compliance minimum
- Standards alignment: Explicitly map to relevant educational standards
- Universal Design for Learning (UDL): Multiple means of representation, action, and engagement
- Bias-free and culturally responsive
- Age-appropriate language and complexity
- Clear learning objectives using measurable action verbs (Bloom's Taxonomy)

**Output Formats:**
- Markdown for documentation and content drafts
- JSON for structured data (objectives, assessments, metadata)
- HTML/CSS for web deliverables
- SCORM packages for LMS integration
- PDF for print materials

**File Organization:**
```
content/
├── drafts/              # Work in progress content
├── published/           # Finalized, approved content
├── assessments/         # Quizzes, tests, rubrics
├── multimedia/          # Scripts, storyboards
├── specs/               # Specifications and requirements
└── analytics/           # Outcome data and reports
```

### **Workflows to Follow**

**For New Content Creation:**
1. Use `/speckit.constitution` to establish principles
2. Use `/speckit.specify` to create detailed specifications
3. Use `/curriculum.research` to research the topic and standards
4. Use `/curriculum.design` to create learning objectives
5. Use `/curriculum.develop-content` to create materials
6. Use `/curriculum.review-pedagogy` and `/curriculum.review-accessibility` for quality checks
7. Use `/speckit.implement` to finalize and deliver

**For Content Updates:**
1. Use `/speckit.clarify` to understand requirements
2. Make edits maintaining consistency with Professor standards
3. Use `/curriculum.review-bias` and `/curriculum.review-pedagogy` to validate changes
4. Use `/curriculum.iterate-feedback` to incorporate feedback

**For Assessment Development:**
1. Use `/curriculum.assess-design` to create assessment blueprints
2. Use `/curriculum.develop-items` to generate questions/tasks
3. Use `/curriculum.review-pedagogy` to validate quality
4. Use `/curriculum.package-lms` to prepare for delivery

### **Autonomous Operation**

When given high-level requests like:
- "Create a course on [topic] for [level]"
- "Develop an assessment for [objectives]"
- "Review this content for quality"

Claude Code should:
1. **Automatically select appropriate agents** based on the task
2. **Invoke relevant skills in sequence** following Professor's workflow patterns
3. **Apply quality standards** from this configuration
4. **Generate deliverables** in appropriate formats
5. **Document the process** and decisions made

### **GitHub Actions Integration**

This repository uses GitHub Actions workflows that:
- Automatically configure Claude Code with Professor framework
- Execute content development tasks via `@claude` mentions or workflow triggers
- Create pull requests with generated content
- Run quality checks and validations
- Deploy approved content

**Workflow Triggers:**
- `@claude` mentions in issues/PRs
- Manual workflow dispatch with task descriptions
- Scheduled content updates and reviews

---

## Best Practices

### **When Creating Content:**
- Always start with clear, measurable learning objectives
- Align to educational standards (NGSS, CCSS, etc.)
- Consider diverse learner needs (UDL principles)
- Include formative and summative assessment opportunities
- Provide multiple pathways to demonstrate understanding

### **When Reviewing Content:**
- Check pedagogical soundness (constructive alignment)
- Verify accessibility (WCAG 2.1 compliance)
- Detect and eliminate bias (cultural responsiveness)
- Validate standards alignment
- Ensure age-appropriate complexity

### **When Packaging Content:**
- Generate multiple formats (web, PDF, SCORM)
- Include all necessary assets (images, videos, resources)
- Test in target LMS environment
- Validate SCORM compliance
- Include metadata and documentation

### **When Analyzing Outcomes:**
- Use data-driven approaches
- Calculate objective mastery rates
- Identify achievement gaps
- Generate actionable recommendations
- Measure impact (Kirkpatrick levels)

---

## Communication Style

- **Tone**: Professional, educational, supportive
- **Language**: Clear, precise, jargon-free (unless technical terms are necessary)
- **Documentation**: Comprehensive, well-structured, scannable
- **Code**: Well-commented, following educational technology best practices
- **Commit Messages**: Descriptive, including rationale and impact

---

## Technical Configuration

**Educational Levels Supported:**
- K-5 (Elementary)
- 6-8 (Middle School)
- 9-12 (High School)
- Undergraduate (4-year college)
- Graduate (Master's level)
- Post-graduate (PhD/Doctoral level)
- Professional Learning (corporate training, continuing education)

**Standards Frameworks:**
- NGSS (Next Generation Science Standards)
- CCSS (Common Core State Standards)
- State-specific standards (adaptable)
- International frameworks (IB, Cambridge, etc.)
- Professional certifications

**Accessibility Standards:**
- WCAG 2.1 Level AA (minimum)
- Section 508 compliance
- Universal Design for Learning (UDL)

**LMS Compatibility:**
- SCORM 1.2 and 2004
- Canvas
- Moodle
- Blackboard
- Google Classroom

---

## Quick Reference: Common Tasks

| Task | Command |
|------|---------|
| Research a topic | `/curriculum.research "topic" --level "9-12" --standards "NGSS"` |
| Design learning objectives | `/curriculum.design --level "9-12" --input research.md` |
| Create lesson plans | `/curriculum.develop-content --objectives objectives.json` |
| Generate assessment items | `/curriculum.develop-items --blueprint blueprint.json` |
| Review for quality | `/curriculum.review-pedagogy --materials drafts/` |
| Check accessibility | `/curriculum.review-accessibility --materials drafts/ --standard "WCAG-2.1"` |
| Package for LMS | `/curriculum.package-lms SCORM --materials final/` |
| Analyze learning outcomes | `/curriculum.analyze-outcomes --assessment-data results.csv` |
| Grade student work | `/curriculum.grade-assist --rubric rubric.json --submissions work/` |

---

## Version

**Content Repository**: 1.0.0
**Professor Framework**: 2.0.0 (92 skills, 22 agents)
**Claude Code**: Latest
**Last Updated**: 2025-11-03

---

## Support

For questions about:
- **Professor Framework**: See https://github.com/pauljbernard/professor
- **Content Repository**: Create an issue in this repository
- **Claude Code**: See https://docs.claude.com/en/docs/claude-code

---

**Remember**: You have access to a complete world-class learning engineering platform. Use Professor's skills and agents confidently to create exceptional educational content.
