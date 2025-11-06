# Content Repository

**Multi-Curriculum Educational Content Development System**

This repository provides:
1. **HMH Multi-Curriculum Knowledge Base** - A hierarchical, reusable knowledge system for creating standards-aligned instructional materials across any state, any subject, any grade level
2. **Professor Framework Integration** - AI-powered content development with 92 specialized skills and 22 autonomous agents

---

## Table of Contents

- [HMH Multi-Curriculum Knowledge Base](#hmh-multi-curriculum-knowledge-base)
- [Professor Framework Integration](#professor-framework-integration)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Quality Standards](#quality-standards)
- [Support](#support)

---

## HMH Multi-Curriculum Knowledge Base

**Status:** Week 3 Complete (50 files, 94% of Phase 1)

### What It Is

A **hierarchical knowledge resolution system** that enables creating standards-aligned, state-compliant instructional materials with **85-97% knowledge reuse** across curricula.

**Key Innovation:** Write once, reuse everywhere. Universal instructional frameworks, assessment guides, and accessibility standards are shared across all states and subjects. State-specific standards and compliance requirements are layered on top through a 5-level hierarchy.

### Current Coverage

**States:** 3 of 51 (6%)
- Texas (TEKS standards)
- California (CCSS/NGSS standards)
- Florida (MAFS/B.E.S.T./NGSSS standards)

**Subjects:** 3 of 10+ core subjects (30%)
- Mathematics (K-8) - 8 Math Language Routines, TEKS/CCSS-M/MAFS alignment
- ELA (K-8) - 4 Literacy Routines, TEKS ELA/CCSS ELA alignment
- Science (K-8) - NGSS 3-dimensional learning, 8 Science & Engineering Practices

**Grade Levels:** K-8 (elementary and middle school)

**Curricula Supported:**
- HMH Into Math Texas Edition
- HMH Into Math California Edition
- HMH Into Math Florida Edition
- HMH Into Reading Texas Edition

### Knowledge Reuse Demonstrated

- **Florida Math:** 97% reuse (only 1 new file, 30 files reused)
- **California Math:** 93% reuse (2 new files, 28 files reused)
- **Texas ELA:** 90% reuse (3 new files, 27 files reused)

**Comparison to Traditional Approach:**
- Traditional: ~500-750 unique files per curriculum (no reuse)
- This System: 50 shared files support 4 curricula (98% file reduction)

### Architecture

**5-Level Hierarchical Resolution** (specific → general, first match wins):

```
1. Program-Specific       (e.g., Into Math TX specific features)
   ↓ (if not found)
2. Subject-District       (e.g., TEKS Math alignment)
   ↓ (if not found)
3. Subject-Common         (e.g., Math MLRs, universal for all states)
   ↓ (if not found)
4. District-Wide          (e.g., Texas compliance, ELPS)
   ↓ (if not found)
5. Universal              (e.g., UDL, DOK, WCAG, assessment best practices)
```

**Example Resolution** for "How to scaffold vocabulary for emergent bilinguals in Texas Math":
1. Checks `/subjects/mathematics/districts/texas/into-math/` (program-specific)
2. Checks `/subjects/mathematics/districts/texas/` (TEKS math)
3. ✅ **Finds** `/subjects/mathematics/common/mlr/` (Math Language Routines - universal)
4. ✅ **Finds** `/districts/texas/language/elps-alignment.md` (Texas language standards)
5. ✅ **Finds** `/universal/frameworks/eb-scaffolding-guide.md` (universal EB support)

**Result:** Combines universal MLR strategies with Texas-specific ELPS requirements and universal EB scaffolding techniques.

### Directory Structure

```
reference/hmh-knowledge-v2/
├── universal/                    # 15 files - applies to ALL curricula
│   ├── frameworks/               # UDL, DOK, EB scaffolding, sentence frames
│   ├── assessment/               # Item types, rubrics, answer keys (8 files)
│   ├── accessibility/            # WCAG 2.1 AA compliance
│   ├── content-equity/           # CEID bias-free content standards
│   └── vendor/                   # HMH-specific quality checklists
├── subjects/
│   ├── mathematics/
│   │   ├── common/               # 12 files - ALL states use these
│   │   │   ├── mlr/              # 8 Math Language Routines (MLR1-MLR8)
│   │   │   ├── vocab-guidelines.md
│   │   │   └── problem-solving-framework.md
│   │   └── districts/
│   │       ├── texas/            # TEKS Math alignment
│   │       ├── california/       # CCSS-M alignment
│   │       └── florida/          # MAFS alignment
│   ├── ela/
│   │   ├── common/               # 5 files - ALL states use these
│   │   │   └── literacy-routines/  # Close Reading, Think-Pair-Share, etc.
│   │   └── districts/
│   │       └── texas/            # TEKS ELA alignment
│   └── science/
│       └── common/               # 2 files - ALL NGSS states use these
│           ├── ngss-alignment-guide.md
│           └── science-practices-framework.md
├── districts/
│   ├── texas/                    # 4 files - applies to ALL subjects in TX
│   │   ├── compliance/           # SBOE, IPACC requirements
│   │   └── language/             # ELPS (Texas language standards)
│   ├── california/               # 2 files - applies to ALL subjects in CA
│   │   ├── compliance/           # CA adoption criteria
│   │   └── language/             # ELD Standards
│   └── florida/                  # 3 files - applies to ALL subjects in FL
│       ├── compliance/           # FL statutory compliance
│       └── language/             # ESOL/WIDA Standards
└── publishers/
    └── hmh/                      # HMH content schema

config/curriculum/
├── hmh-math-tx.json              # Defines resolution order for TX Math
├── hmh-math-ca.json              # Defines resolution order for CA Math
├── hmh-math-fl.json              # Defines resolution order for FL Math
└── hmh-ela-tx.json               # Defines resolution order for TX ELA
```

### Key Files by Category

**Universal (15 files) - Reused by ALL Curricula:**
- UDL Principles Guide
- DOK (Depth of Knowledge) Framework
- EB Scaffolding Guide (Emergent Bilinguals)
- Sentence Frames Library
- WCAG 2.1 AA Compliance Guide
- 8 Assessment Files (item types, rubrics, answer keys, validation, etc.)
- CEID Guidelines (Content Equity, Inclusion & Diversity)
- Vendor Quality Checklist

**Mathematics Common (12 files) - Reused by ALL Math Programs:**
- 8 Math Language Routines (MLR1-MLR8):
  - MLR1: Stronger and Clearer Each Time
  - MLR2: Collect and Display
  - MLR3: Critique, Correct, and Clarify
  - MLR4: Information Gap
  - MLR5: Co-Craft Questions
  - MLR6: Three Reads
  - MLR7: Compare and Connect
  - MLR8: Discussion Supports
- MLR Overview & Placement Rules
- Math Vocabulary Guidelines
- Problem-Solving Framework

**ELA Common (5 files) - Reused by ALL ELA Programs:**
- Close Reading Protocol
- Think-Pair-Share
- Annotation Protocol
- Turn-and-Talk
- (More literacy routines to be added)

**Science Common (2 files) - Reused by ALL NGSS States:**
- NGSS Alignment Guide (3-dimensional learning)
- Science Practices Framework (8 SEPs with CER framework)

**State-District Files (9 files) - Apply to ALL subjects in that state:**
- Texas: IPACC, SBOE, ELPS, compliance checklist
- California: Adoption criteria, ELD Standards
- Florida: Adoption criteria, ESOL/WIDA, statutory compliance

**Subject-District Files (7 files) - State + Subject specific:**
- TEKS Math alignment (TX)
- TEKS ELA alignment (TX)
- CCSS-M alignment (CA)
- MAFS alignment (FL)
- Gap mitigation strategies (TX Math)
- (ELA CA/FL and Science files - documented gaps)

### Documentation: Complete Guide Suite

The system provides **4 specialized guides** for different roles:

**📝 [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)** - For Content Authors
- Complete authoring workflows (lessons, assessments, activities)
- Using the knowledge base to generate content
- AI assistance with Professor Framework
- Quality standards and checklists
- **850 lines** of comprehensive guidance

**✅ [EDITOR_GUIDE.md](EDITOR_GUIDE.md)** - For Content Editors
- Editorial workflow from assignment to approval
- 8-section comprehensive review checklist
- Effective feedback templates
- Common issues and fixes
- **450 lines** of editorial guidance

**📦 [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** - For Publishers/Production
- Multi-format production (PDF, HTML, SCORM, accessible)
- Asset management and optimization
- QA checklists and delivery workflows
- **450 lines** of production guidance

**⚙️ [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)** - For Knowledge Base Engineers
- System architecture and hierarchical resolution
- Adding new states/districts (2-6 files, 85-97% reuse)
- Adding new subjects (8-15 files)
- Creating curriculum configs
- File creation best practices and templates
- **1700 lines** of engineering documentation

**📋 [USER_GUIDE.md](USER_GUIDE.md)** - Overview and Navigation
- Introduction to the 4 guides
- Quick navigation by role
- Complete content lifecycle
- Documentation roadmap

### For Engineers: How to Use This System

**See:** [`ENGINEER_GUIDE.md`](ENGINEER_GUIDE.md) - Complete guide for knowledge base engineers

**Quick Start:**
1. Choose or create a curriculum config (see `config/curriculum/`)
2. Config defines resolution order (program → subject-district → subject-common → district → universal)
3. System automatically finds and combines relevant knowledge files
4. Generate content using combined knowledge with 85-97% reuse

**Adding New States:**
- CCSS/NGSS state: 2-3 files (compliance, language, notes) → 90-95% reuse
- State-specific standards: 5-6 files (standards per subject + compliance) → 85-90% reuse

**Adding New Subjects:**
- 8-10 subject-common files (instructional routines, standards alignment)
- 1-2 subject-district files per state
- Reuse all 15 universal files and all district-wide files

### Future Expansion Roadmap

**See:** [`.archive/HMH_Scaling_Roadmap_National_All_Subjects.md`](.archive/HMH_Scaling_Roadmap_National_All_Subjects.md)

**Phase 2-7:** Complete national coverage
- Add 48 more states/districts (total: 51)
- Add 7+ core subjects (Social Studies, CS, World Languages, Arts, PE, etc.)
- Add high school (9-12) grade band
- Estimated: 245-310 total files for complete coverage
- Timeline: 8-12 months with focused team

**ROI:** 98% reduction in files compared to traditional approach (5,000+ files vs 250-310)

---

## Professor Framework Integration

**World-class educational content development powered by AI**

This repository integrates the complete [Professor framework](https://github.com/pauljbernard/professor) with **92 specialized skills** and **22 autonomous agents** for AI-powered curriculum and assessment engineering.

### Quick Start

#### 1. Use @claude in Issues or PRs

```
@claude Create a lesson plan on photosynthesis for 6th grade aligned with NGSS standards
```

#### 2. Run Automated Workflows

Go to **Actions** → **Automated Content Development with Professor** and provide:
- Task description
- Educational level
- Standards alignment
- Output location

#### 3. Scheduled Reviews

Every Monday, the system automatically reviews published content for quality, accessibility, and bias.

### What Can Professor Do?

**Content Creation:**
- Curriculum Development (courses, units, lesson plans)
- Assessment Design (quizzes, tests, rubrics, performance tasks)
- Multimedia Content (scripts, storyboards, interactive activities)
- Supporting Materials (handouts, worksheets, study guides)

**Quality Assurance:**
- Pedagogical Review (validate learning design)
- Accessibility Check (WCAG 2.1 AA compliance)
- Bias Detection (identify cultural insensitivity)
- Standards Alignment (verify educational standards)

**Publishing & Delivery:**
- LMS Packages (SCORM 1.2/2004)
- PDF Generation (print-ready materials)
- Web Content (responsive HTML/CSS)
- Multi-format Export (QTI, Canvas, Moodle)

**Analytics & Improvement:**
- Outcome Analysis (student performance data)
- Impact Measurement (Kirkpatrick evaluation)
- Iterative Improvement (data-driven refinement)

### Professor Components

**92 Skills** organized into 19 categories:
- Curriculum Research & Design
- Content Development
- Assessment Design & Development
- Review & Quality Assurance
- Packaging & Delivery
- Analytics & Measurement
- Personalization & Adaptation
- Learning Support
- And more...

**22 Agents** for autonomous workflows:
- `curriculum-architect` - Designs curriculum structures
- `content-developer` - Creates learning materials
- `assessment-designer` - Designs assessments
- `pedagogical-reviewer` - Reviews quality
- `quality-assurance` - Ensures standards
- `learning-analytics` - Analyzes outcomes
- And 16 more specialized agents...

**Framework Components:**
- **Spec-Kit**: Specification-driven development
- **API Integration**: Connect to external platforms
- **Agent Coordination**: Multi-agent orchestration

**See:** [`CLAUDE.md`](CLAUDE.md) for complete Professor configuration

---

## Repository Structure

```
content/
├── README.md                               # This file
├── CLAUDE.md                               # Claude Code configuration (Professor)
├── USER_GUIDE.md                           # Documentation overview and navigation
├── AUTHOR_GUIDE.md                         # Complete guide for content authors
├── EDITOR_GUIDE.md                         # Complete guide for content editors
├── PRODUCTION_GUIDE.md                     # Complete guide for production/publishing
├── ENGINEER_GUIDE.md                       # Complete guide for knowledge base engineers
├── INCOMPLETE_ANALYSIS.md                  # Known gaps and future work
├── .archive/                               # Archived planning documents
│   └── HMH_*.md                            # Week 1-3 summaries, roadmap
├── .claude/                                # Claude Code local configs
│   └── commands/                           # Spec-kit commands (tracked)
├── .github/
│   ├── actions/
│   │   └── setup-professor/                # Composite action for Professor
│   └── workflows/
│       ├── claude-professor.yml            # @claude mention integration
│       ├── content-development-automated.yml  # Manual content creation
│       └── scheduled-content-review.yml    # Automated quality reviews
├── config/
│   └── curriculum/                         # Curriculum configs (4 configs)
│       ├── hmh-math-tx.json
│       ├── hmh-math-ca.json
│       ├── hmh-math-fl.json
│       └── hmh-ela-tx.json
├── reference/
│   ├── hmh-knowledge/                      # OLD v1 structure (to be archived)
│   └── hmh-knowledge-v2/                   # CURRENT multi-curriculum system
│       ├── universal/                      # 15 files
│       ├── subjects/                       # Math, ELA, Science
│       ├── districts/                      # TX, CA, FL
│       └── publishers/                     # HMH
├── drafts/                                 # Work-in-progress content
├── published/                              # Finalized, approved content
├── assessments/                            # Quizzes, tests, rubrics
├── multimedia/                             # Scripts, storyboards
├── specs/                                  # Specifications and requirements
├── analytics/                              # Outcome data and reports
├── reviews/                                # Quality review reports
└── experiments/                            # Experimental content
```

---

## Getting Started

### Choose Your Guide

Start with the guide that matches your role:

**Creating Content?** → [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)
- Learn authoring workflows for lessons (3-5 days), assessments (2-4 days), and activities (1-2 days)
- Use the knowledge base to generate aligned content
- Work with AI assistance and quality checklists

**Reviewing Content?** → [EDITOR_GUIDE.md](EDITOR_GUIDE.md)
- Follow the editorial workflow (2-4 hours per review)
- Use the comprehensive 8-section review checklist
- Provide effective feedback with templates

**Producing Deliverables?** → [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
- Create multi-format outputs (PDF, HTML, SCORM, accessible)
- Manage and optimize assets
- Run QA checks before delivery

**Extending the System?** → [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)
- Understand system architecture
- Add new states (2-6 files, 85-97% reuse)
- Add new subjects (8-15 files)
- Create curriculum configs

### For Content Engineers (Using HMH Knowledge Base)

1. **Read [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)** - Complete engineering guide
2. **Choose a curriculum config** - See `config/curriculum/`
3. **Understand resolution order** - Specific → general (first match wins)
4. **Generate content** - Use Claude Code with appropriate config
5. **Add new states/subjects** - Follow patterns in ENGINEER_GUIDE.md

### For Curriculum Developers (Using Professor Framework)

1. **Mention @claude in an issue** with your content development request
2. **Or run the workflow** via Actions → Automated Content Development
3. **Review the generated content** in the pull request
4. **Iterate and refine** using Professor skills

### Prerequisites

1. **Anthropic API Key**: Add `ANTHROPIC_API_KEY` to repository secrets (for workflows)
2. **Professor Access**: Ensure access to the private Professor repository (for workflows)
3. **Claude Code CLI**: For local development with HMH Knowledge Base
4. **GitHub Permissions**: Workflows need `contents: write` and `pull-requests: write`

---

## Quality Standards

### HMH Knowledge Base Standards

**All knowledge files adhere to:**
- Pedagogical soundness (evidence-based learning science)
- Standards alignment (TEKS, CCSS, NGSS, etc.)
- Emergent Bilingual support (ELPS, ELD, ESOL/WIDA)
- Universal Design for Learning (UDL)
- Accessibility (WCAG 2.1 AA)
- Bias-free content (CEID guidelines)

**File Quality Checklist:**
- Clear structure and formatting
- Cross-references valid
- Grade-level appropriate examples
- Subject-specific accuracy
- Reusability demonstrated

### Professor Framework Standards

**All generated content adheres to:**

**Pedagogical:**
- Evidence-based learning science
- Bloom's Taxonomy for objectives
- Universal Design for Learning (UDL)
- Backwards design methodology
- Constructive alignment

**Accessibility:**
- WCAG 2.1 Level AA minimum
- Section 508 compliance
- Screen reader compatibility
- Keyboard navigation
- Alternative text for images

**Technical:**
- SCORM 1.2 and 2004
- LTI 1.3
- QTI 2.1/3.0
- xAPI (Tin Can)

---

## Educational Levels Supported

- **K-5**: Elementary (ages 5-10)
- **6-8**: Middle School (ages 11-13)
- **9-12**: High School (ages 14-18) - *HMH: Coming in Phase 2*
- **Undergraduate**: 4-year college/university
- **Graduate**: Master's level
- **Post-graduate**: PhD/Doctoral level
- **Professional Learning**: Corporate training, continuing education

---

## Standards Frameworks Supported

**HMH Knowledge Base (Current):**
- **TEKS** (Texas Essential Knowledge and Skills)
- **CCSS-M** / **CCSS ELA** (Common Core State Standards)
- **MAFS** / **B.E.S.T.** (Florida Mathematics Standards)
- **NGSS** (Next Generation Science Standards)
- **ELPS** (English Language Proficiency Standards - Texas)
- **ELD** (English Language Development - California)
- **ESOL/WIDA** (English for Speakers of Other Languages - Florida)

**Professor Framework (All):**
- All state standards (50 states + DC)
- International frameworks (IB, Cambridge)
- Professional certifications

---

## Examples

### Example 1: Generate Texas Math Content (HMH Knowledge Base)

Use curriculum config `hmh-math-tx.json` to automatically pull in:
- Universal assessment frameworks (DOK, rubrics)
- Math MLRs (8 language routines)
- TEKS Math alignment
- Texas compliance (SBOE, IPACC)
- ELPS language scaffolding
- UDL principles

**Result:** 97% of guidance comes from reusable files, 3% from Texas Math specific

### Example 2: Create Complete Course (Professor Framework)

```
@claude Create a complete 10-week course on Data Science for undergraduates

Include:
- Weekly learning objectives
- Lecture materials and slides
- Programming exercises (Python)
- Datasets for practice
- Weekly quizzes
- Midterm and final projects
- Rubrics for all assessments

Align to ACM Computer Science guidelines
```

### Example 3: Expand to New State (HMH Knowledge Base)

**Add New York Math (CCSS-M state):**
1. Create `districts/new-york/compliance/ny-adoption-criteria.md`
2. Create `districts/new-york/language/nyseslat-alignment.md` (if needed)
3. Create config `hmh-math-ny.json` pointing to:
   - Universal (reuse all 15 files)
   - Math common (reuse all 12 files)
   - California CCSS-M file (reuse)
   - New York district files (2 new files)

**Result:** 27 reused, 2 new = 93% reuse

---

## Known Issues and Future Work

**See:** [`INCOMPLETE_ANALYSIS.md`](INCOMPLETE_ANALYSIS.md)

**Critical (1 hour to fix):**
- Config path inconsistencies (3 configs use old paths)
- Program-specific directory references (don't exist yet)
- Outdated migration documentation

**Moderate (6-9 hours to fix):**
- Subject-district gaps (ELA CA/FL, Science TX/CA/FL)
- Old hmh-knowledge directory cleanup

**Future Expansion (110-170 hours):**
- High school (9-12) coverage
- 7+ additional subjects (Social Studies, CS, Arts, etc.)
- 48 additional states/districts
- Complete national coverage (245-310 total files)

---

## Contributing

### Extending the HMH Knowledge Base

1. Follow patterns in `USER_GUIDE.md`
2. Use templates for standards alignment and instructional routines
3. Ensure cross-references are valid
4. Add to appropriate hierarchy level (universal, subject-common, district, etc.)
5. Update curriculum configs as needed
6. Test knowledge resolution

### Improving Professor Framework Content

1. Make changes to content files
2. Run accessibility and quality checks
3. Update metadata and documentation
4. Create a pull request

---

## Support

**Documentation by Role:**
- **Content Authors**: See [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)
- **Content Editors**: See [EDITOR_GUIDE.md](EDITOR_GUIDE.md)
- **Production/Publishing**: See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
- **Knowledge Base Engineers**: See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)
- **Overview/Navigation**: See [USER_GUIDE.md](USER_GUIDE.md)

**Additional Resources:**
- **Known Issues**: See [INCOMPLETE_ANALYSIS.md](INCOMPLETE_ANALYSIS.md)
- **Professor Framework**: https://github.com/pauljbernard/professor
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code
- **Issues**: Create an issue in this repository

---

## License

MIT License

---

## Version History

**v3.0.0** (2025-11-06) - Complete Documentation Suite
- **4 Specialized Role-Based Guides:**
  - AUTHOR_GUIDE.md (850 lines) - Complete authoring workflows
  - EDITOR_GUIDE.md (450 lines) - Editorial process and review
  - PRODUCTION_GUIDE.md (450 lines) - Multi-format production
  - ENGINEER_GUIDE.md (1700 lines) - System architecture and extension
  - USER_GUIDE.md (335 lines) - Overview and navigation
- **Total Documentation:** 3,785 lines covering complete content lifecycle
- HMH Multi-Curriculum Knowledge Base: 50 files, 3 states, 3 subjects, 85-97% reuse
- 4 curriculum configs

**v2.0.0** (2025-11-06) - Week 3 Complete
- HMH Multi-Curriculum Knowledge Base: 50 files, 3 states, 3 subjects
- 4 curriculum configs
- Initial USER_GUIDE.md for engineers
- Scaling roadmap for national coverage

**v1.0.0** (2025-11-03) - Initial Release
- Professor framework integration
- GitHub workflows for @claude mentions
- Automated content development and review

---

**Powered by:**
- [Claude Code](https://claude.com/claude-code) - AI-powered coding assistant
- [Professor Framework](https://github.com/pauljbernard/professor) - Learning engineering platform
- [HMH Multi-Curriculum Knowledge Base](reference/hmh-knowledge-v2/) - Hierarchical knowledge system

**Last Updated**: 2025-11-06 (Week 3 Complete)
