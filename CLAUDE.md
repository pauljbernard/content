# Content Repository - Claude Code Configuration

## Project Overview

This repository provides **two integrated systems** for educational content development:

1. **HMH Multi-Curriculum Knowledge Base** - A hierarchical, reusable knowledge system (282 files) for creating standards-aligned instructional materials across any state, any subject, any grade level (K-12) with 85-95% knowledge reuse
2. **Professor Framework Integration** - AI-powered content development with 92 specialized skills and 22 autonomous agents

**Purpose**: Create, manage, and publish high-quality educational content across all educational levels (K-12, undergraduate, graduate, post-graduate, and professional learning).

**Repository**: https://github.com/pauljbernard/content
**Professor Framework**: https://github.com/pauljbernard/professor (private)

---

## HMH Multi-Curriculum Knowledge Base (100% US Coverage Complete)

### What It Is

A **hierarchical knowledge resolution system** that enables creating standards-aligned, state-compliant instructional materials with **85-97% knowledge reuse** across curricula.

**Location**: `/reference/hmh-knowledge/`
**Status**: Complete (282 files, 100% K-12 US coverage)
**Documentation**: See complete documentation suite:
- **[USER_GUIDE.md](USER_GUIDE.md)** - Overview and navigation for all roles
- **[AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)** - Complete authoring workflows (850 lines)
- **[EDITOR_GUIDE.md](EDITOR_GUIDE.md)** - Editorial review processes (450 lines)
- **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** - Multi-format production (450 lines)
- **[ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)** - System architecture and extension (1700 lines)

### Current Coverage

**States**: All 51 US states/districts (100% coverage)
**Subjects**: Mathematics (K-12), ELA (K-12), Science (K-12), Social Studies (K-12), Computer Science (K-12)
**State/Subject Combinations**: 510 (51 states × 5 subjects × 2 grade bands: K-8, 9-12)
**Students Covered**: 66.5M (100% of US K-12 enrollment: 38M K-8 + 28.5M HS)
**Curricula**: 4+ HMH programs (Into Math TX/CA/FL K-8, Into Reading TX K-8, Algebra I, AP Calculus, AP English, etc.)

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

**High School (24 files) - Grade 9-12 subject-specific:**
- Universal HS (3 files): College/Career Readiness Framework, HS Instructional Strategies, HS Assessment Guide
- Math HS (6 files): Algebra I, Algebra II, Geometry, Pre-Calculus, Calculus (AP AB/BC), Statistics (AP)
- ELA HS (4 files): HS Literature, HS Composition, AP English Language, AP English Literature
- Science HS (3 files): Biology, Chemistry, Physics (including AP courses)
- Social Studies HS (4 files): US History, World History, Government, Economics (including AP courses)
- Computer Science HS (1 file): AP CS Principles and AP CS A
- State Graduation Requirements (3 files): Texas, California, Florida (graduation requirements, EOC exams, college prep)

### How Claude Code Should Use This

**When generating state/subject-specific content:**

1. **Check for curriculum config** in `/config/curriculum/`
   - K-8: `hmh-math-tx.json`, `hmh-math-ca.json`, `hmh-math-fl.json`, `hmh-ela-tx.json`
   - HS: `hmh-algebra1-tx.json`, `hmh-biology-tx.json`, `hmh-ap-calc-ab.json`, `hmh-ap-english-lit.json`

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

**Example Query (High School)**: "Create a Florida AP Biology lesson on genetics"

**Resolution Process**:
1. Load `hmh-biology-fl.json` config
2. Gather knowledge from:
   - `/subjects/science/high-school/biology-guide.md` (genetics content, AP Biology standards)
   - `/subjects/science/common/ngss-alignment.md` (HS-LS3 Heredity standards)
   - `/subjects/science/common/science-practices-framework.md` (8 SEPs)
   - `/districts/florida/high-school/florida-graduation-requirements.md` (Biology EOC prep, B.E.S.T. standards)
   - `/districts/florida/language/florida-esol-wida.md` (ESOL scaffolding)
   - `/districts/florida/compliance/florida-adoption-criteria.md` (state compliance)
   - `/universal/high-school/college-career-readiness-framework.md` (AP course preparation)
   - `/universal/high-school/hs-instructional-strategies.md` (HS pedagogy)
   - `/universal/frameworks/udl-principles-guide.md`
   - `/universal/assessment/item-types-reference.md`
3. Combine guidance to create lesson aligned to B.E.S.T. standards, Florida Biology EOC, AP Biology exam, NGSS, and college readiness

### Adding New States/Subjects

**For Engineers**: See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) for complete step-by-step instructions, templates, and examples.

**Quick Summary**:
- **CCSS/NGSS State**: 2-3 files (90-95% reuse) - See ENGINEER_GUIDE.md Section 3
- **State-Specific Standards**: 5-6 files (85-90% reuse) - See ENGINEER_GUIDE.md Section 3
- **New Subject**: 8-10 subject-common files + 1-2 per state - See ENGINEER_GUIDE.md Section 4

### Known Gaps

**See**: [`US_COMPLETE.md`](US_COMPLETE.md) for complete milestone documentation.

**Current Status:**
- ✅ All 51 US states/districts covered (100%)
- ✅ K-12 coverage complete (grades K-8 and 9-12)
- ✅ 5 core subjects complete (Math, ELA, Science, Social Studies, CS)
- ✅ 282 knowledge files production-ready
- ✅ High school expansion complete - 24 files added (2025-11-06)
- ✅ Missing TEKS Math alignment file - FIXED (created 2025-11-06)

**Minor Gaps:**
- Program-specific directories referenced but not yet created (Into Math TX variations)
- Config paths are correct (`/reference/hmh-knowledge/`)

**Future expansion:**
- Additional K-12 subjects (World Languages, Fine Arts, PE/Health) - ~70 hours each
- Large urban districts (NYC, LA, Chicago, etc.) - ~5 hours each
- Pre-K expansion - ~60 hours
- International curricula (IB, Cambridge, UK, Canada, Australia) - ~200 hours

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

**For Content Authors** - See [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md) Section 4 for complete workflows:

**Lesson Authoring Workflow** (3-5 days):
1. Planning - Identify curriculum config, gather knowledge files
2. Drafting - Use knowledge base guidance, apply instructional routines
3. Self-Review - Check against 7 Quality Pillars
4. Submit for Review - Create pull request

**Assessment Authoring Workflow** (2-4 days):
1. Design Assessment Blueprint
2. Write Items (MC, CR, performance tasks)
3. Create Answer Key and Rubrics
4. Self-Review and Submit

**AI-Assisted Workflow** - See [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md) Section 5:
- Method 1: GitHub Issues (@claude mentions)
- Method 2: Command Line (Professor skills)
- Method 3: Workflow Dispatch (GitHub Actions)

**For Content Editors** - See [EDITOR_GUIDE.md](EDITOR_GUIDE.md) Section 2:
1. Receive Assignment
2. Preliminary Review (15-30 minutes)
3. Detailed Review using 8-section checklist (1-3 hours)
4. Provide Feedback using templates
5. Re-Review after author revisions
6. Approval and Merge

**For Production Staff** - See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) Sections 2-3:
1. Receive approved content
2. Choose format(s): PDF, HTML, SCORM, accessible
3. Manage and optimize assets
4. Run QA checks
5. Package and deliver

**For Engineers** - See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) Sections 3-6:
- Adding States: Follow state type decision tree
- Adding Subjects: Create subject-common + subject-district files
- Creating Configs: Use template, define resolution order
- Extending Universal: Add frameworks that apply to all curricula

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

### **When Creating Content** - See [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md) Section 6:
- Always start with clear, measurable learning objectives (Bloom's Taxonomy)
- Align to educational standards (TEKS, CCSS, NGSS, etc.)
- Use knowledge base guidance for instructional routines (MLRs, literacy routines)
- Consider diverse learner needs (UDL principles)
- Include scaffolds for emergent bilinguals (ELPS/ELD/ESOL)
- Apply 7 Quality Pillars before submission
- Include formative and summative assessment opportunities

### **When Reviewing Content** - See [EDITOR_GUIDE.md](EDITOR_GUIDE.md) Section 3:
- Use the comprehensive 8-section review checklist
- Check pedagogical soundness (constructive alignment)
- Verify accessibility (WCAG 2.1 AA compliance)
- Detect and eliminate bias (CEID framework - 11 categories)
- Validate standards alignment with knowledge base files
- Ensure age-appropriate complexity and scaffolding
- Provide specific, actionable feedback with templates

### **When Packaging Content** - See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) Sections 3-5:
- Generate multiple formats (PDF via Pandoc, HTML responsive, SCORM 1.2/2004)
- Optimize assets (images to 1200x800, videos compressed, audio normalized)
- Include all necessary metadata and assets
- Test in target LMS environment
- Validate SCORM compliance with imsmanifest.xml
- Run complete QA checklist before delivery
- Create accessible versions (large print, screen reader, braille-ready)

### **When Extending the System** - See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) Sections 7-9:
- Follow file naming conventions (kebab-case)
- Use templates and patterns for consistency
- Maintain DRY principle (no duplicate content)
- Test knowledge resolution after adding files
- Validate all cross-references
- Apply pre-publication checklist
- Document knowledge reuse percentage

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

**Content Repository**: v3.0.0 (Complete Documentation Suite)
**Documentation**: 3,785 lines covering complete content lifecycle
- AUTHOR_GUIDE.md: 850 lines
- EDITOR_GUIDE.md: 450 lines
- PRODUCTION_GUIDE.md: 450 lines
- ENGINEER_GUIDE.md: 1,700 lines
- USER_GUIDE.md: 335 lines

**HMH Knowledge Base**: 282 files, 85-95% reuse, 5-level hierarchy, 100% K-12 US coverage
**Professor Framework**: 2.0.0 (92 skills, 22 agents)
**Claude Code**: Latest
**Last Updated**: 2025-11-06

---

## Support

**Documentation by Role:**
- **Content Authors**: See [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md) - Complete authoring workflows, AI assistance, quality standards
- **Content Editors**: See [EDITOR_GUIDE.md](EDITOR_GUIDE.md) - Editorial workflow, review checklists, feedback templates
- **Production/Publishers**: See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) - Multi-format production, asset management, delivery
- **Knowledge Base Engineers**: See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) - System architecture, adding states/subjects, configs
- **Overview/Navigation**: See [USER_GUIDE.md](USER_GUIDE.md) - Complete content lifecycle diagram

**Additional Resources:**
- **Professor Framework**: https://github.com/pauljbernard/professor
- **Known Issues**: See [INCOMPLETE_ANALYSIS.md](INCOMPLETE_ANALYSIS.md)
- **Content Repository Issues**: Create an issue in this repository
- **Claude Code Documentation**: https://docs.claude.com/en/docs/claude-code

---

## Quick Navigation by Task

| I want to... | See this guide | Section |
|-------------|----------------|---------|
| Write a lesson | [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md) | Section 4 (Lesson Workflow) |
| Create an assessment | [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md) | Section 4 (Assessment Workflow) |
| Use AI assistance | [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md) | Section 5 (Professor Framework) |
| Review content quality | [EDITOR_GUIDE.md](EDITOR_GUIDE.md) | Section 3 (Review Checklist) |
| Provide feedback | [EDITOR_GUIDE.md](EDITOR_GUIDE.md) | Section 4 (Effective Feedback) |
| Create a PDF | [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) | Section 3 (PDF Production) |
| Build SCORM package | [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) | Section 3 (SCORM Production) |
| Optimize assets | [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) | Section 4 (Asset Management) |
| Add a new state | [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) | Section 3 (Add State/District) |
| Add a new subject | [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) | Section 4 (Add Subject) |
| Create curriculum config | [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) | Section 5 (Create Config) |

---

**Remember**: You have access to a complete world-class learning engineering platform with comprehensive documentation for every role in the content lifecycle. Use Professor's skills and agents confidently to create exceptional educational content.
