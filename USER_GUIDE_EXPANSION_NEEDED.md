# USER_GUIDE.md Expansion Plan

**Status:** Structure complete, content needs to be added for Parts A, B, and C
**Date:** 2025-11-06

---

## Current State

The USER_GUIDE.md has been restructured to serve **four audiences** instead of just one:

1. **Part A: For Content Authors** - *(PLACEHOLDER - Needs content)*
2. **Part B: For Content Editors** - *(PLACEHOLDER - Needs content)*
3. **Part C: For Publishers and Production** - *(PLACEHOLDER - Needs content)*
4. **Part D: For Knowledge Base Engineers** - ✅ **COMPLETE** (original content preserved)

**Table of Contents:** Updated with 33 sections (7 for authors, 6 for editors, 6 for publishers, 11 for engineers)

---

## What Needs to Be Added

### Part A: For Content Authors (Sections 1-7)

**Section 1: Getting Started as a Content Author**
- Welcome and role overview
- Tools and environment setup
- Directory structure explanation
- First steps (understanding assignment, setup config, gather resources, draft, self-review, submit)

**Section 2: Understanding Your Content Brief**
- What a content brief contains
- Required elements (product info, standards, scope, compliance, pedagogy, assets)
- Example content brief (YAML format with complete specifications)
- How to interpret the brief (mapping to knowledge base files)

**Section 3: Using the Knowledge Base to Generate Content**
- Step-by-step guide to using the knowledge base
- How to identify curriculum config
- Understanding resolution order
- Gathering relevant knowledge files (example: 18 files for TX 5th grade math lesson)
- Applying knowledge base guidance with concrete examples
- Using AI assistance (optional)

**Section 4: Content Types and Authoring Workflows**
- Overview of content types (lessons, assessments, activities, scaffolding, teacher resources)
- **Lesson Authoring Workflow** (5 phases over 3-5 days):
  - Phase 1: Planning (Day 1)
  - Phase 2: Drafting (Days 2-3) with complete template
  - Phase 3: Self-Review and Revision (Day 4) with checklist
  - Phase 4: Submit for Review (Day 5)
- **Assessment Authoring Workflow** (4 phases over 2-4 days):
  - Phase 1: Design Assessment Blueprint
  - Phase 2: Write Items (with MC and CR templates)
  - Phase 3: Create Answer Key and Rubrics
  - Phase 4: Self-Review and Submit
- **Activity Authoring Workflow** (1-2 days) with template

**Section 5: Working with AI Assistance (Professor Framework)**
- When to use AI (generation, variation, differentiation, formatting, checking)
- When NOT to rely on AI (final decisions, cultural nuances, complex items)
- Three methods:
  - Method 1: GitHub Issues (@claude mentions)
  - Method 2: Command Line (local development)
  - Method 3: Workflow Dispatch (GitHub Actions)
- Reviewing AI-generated content checklist

**Section 6: Quality Standards for Authored Content**
- The 7 Quality Pillars:
  1. Standards Alignment (requirements, how to check, KB references)
  2. Pedagogical Soundness (requirements, how to check, KB references)
  3. Language Support (ELPS/ELD/ESOL requirements, how to check)
  4. Universal Design for Learning (UDL - requirements, how to check)
  5. Accessibility (WCAG 2.1 AA - requirements, how to check)
  6. Cultural Responsiveness and Bias-Free Content (CEID framework)
  7. State Compliance (state-specific requirements)
- Pre-Submission Quality Checklist (comprehensive checklist before submitting)

**Section 7: Collaboration and Version Control**
- Using Git and GitHub (basic workflow: start work, submit for review, respond to feedback, final approval)
- Collaboration best practices (communicating with editors, file organization, naming conventions)
- Commit message examples (good vs bad)

**Estimated Length:** 150-200 pages (600-800 lines)

---

### Part B: For Content Editors (Sections 8-13)

**Section 8: Getting Started as a Content Editor**
- Welcome and role overview
- Responsibilities (content review, feedback, process management)
- Tools (editorial checklist, knowledge base, GitHub, style guides)
- Editorial workflow overview (7-step process from assignment to approval)

**Section 9: Editorial Workflow Overview**
- Step 1: Receive Assignment
- Step 2: Preliminary Review (15-30 minutes)
- Step 3: Detailed Review (1-3 hours) using checklist
- Step 4: Provide Feedback (30-60 minutes)
- Step 5: Author Revises
- Step 6: Re-Review (30-60 minutes)
- Step 7: Approval and Merge

**Section 10: Content Review Checklist**
- **Comprehensive 8-section checklist:**
  1. Standards Alignment (standards addressed, objectives, assessment alignment)
  2. Pedagogical Soundness (instructional sequence, routines, formative assessment, misconceptions, differentiation)
  3. Language Support (ELPS/ELD/ESOL, scaffolds, sentence frames, vocabulary)
  4. UDL (multiple means of representation, action/expression, engagement)
  5. Accessibility (images, color/contrast, structure, interactivity, text)
  6. Cultural Responsiveness (representation, stereotypes, contexts, CEID 11 categories)
  7. State Compliance (TX/CA/FL specific requirements)
  8. Technical Quality (writing, formatting, completeness, assets)

**Section 11: Providing Effective Feedback**
- Principles (be specific, actionable, explain why, balance critical/positive, prioritize)
- Feedback templates for lessons and assessments
- Common feedback scenarios with examples (missing KB application, standards misalignment, accessibility gaps, missing ELL scaffolds)

**Section 12: Approval Process and Sign-Off**
- When to approve (criteria, "almost there" vs fundamental issues)
- Approval workflow (4 steps: final review, leave approval comment, merge PR, document if needed)

**Section 13: Common Content Issues and Fixes**
- Issue 1: Weak learning objectives (problem/fix)
- Issue 2: Missing common misconceptions (problem/fix)
- Issue 3: Formulaic sentence frames (problem/fix)
- Issue 4: Accessibility afterthought (problem/fix)
- Issue 5: Token diversity (problem/fix)
- Issue 6: Incorrect instructional routine application (problem/fix)
- Issue 7: Answer key errors (problem/fix)

**Estimated Length:** 100-150 pages (400-600 lines)

---

### Part C: For Publishers and Production (Sections 14-19)

**Section 14: Getting Started in Production**
- Welcome and role overview
- Responsibilities (formatting, multi-format production, asset management, QA, distribution)

**Section 15: Publishing Workflow Overview**
- End-to-end 10-step process from approved content to delivery
- Timeline: 2-5 days depending on complexity

**Section 16: Multi-Format Content Production**
- Overview of 4 output formats (PDF, HTML, SCORM, accessible formats)
- **Format 1: PDF Production** (6 steps with code examples, quality checks)
- **Format 2: Interactive HTML Production** (5 steps with code examples, responsive design, accessibility, quality checks)
- **Format 3: SCORM Package Production** (5 steps: structure, manifest, API, package, test in LMS)
- **Format 4: Accessible Formats** (large print, screen reader HTML, braille-ready, audio descriptions)

**Section 17: Asset Management and Organization**
- Asset types (images, videos, audio, interactive, documents)
- Asset organization structure (directory tree)
- Asset specifications (images, videos, audio with technical requirements)
- Asset workflow (4 steps: receive specs, source/create, optimize, add metadata, store)

**Section 18: Quality Assurance in Production**
- Final Production QA Checklist (format checks, visual quality, technical quality, accessibility, cross-format consistency, branding, legal/compliance)

**Section 19: Delivery and Distribution**
- Distribution channels (direct download, LMS, physical, streaming, app stores)
- Distribution workflow (5 steps: package, create manifest, upload, notify stakeholders, confirm delivery)
- Examples of delivery manifests and stakeholder notifications

**Estimated Length:** 80-120 pages (320-480 lines)

---

## Implementation Plan

### Option 1: Fill in USER_GUIDE.md

**Approach:** Replace placeholder text in USER_GUIDE.md with full content for Parts A, B, C

**Pros:**
- All content in one place
- Single source of truth

**Cons:**
- Very large file (~3500-4500 lines total)
- Slower to load and navigate
- Git diffs will be large

**Steps:**
1. Write Part A content (600-800 lines)
2. Insert into USER_GUIDE.md replacing placeholder
3. Write Part B content (400-600 lines)
4. Insert into USER_GUIDE.md replacing placeholder
5. Write Part C content (320-480 lines)
6. Insert into USER_GUIDE.md replacing placeholder
7. Test navigation and links
8. Commit

---

### Option 2: Separate Guides (Recommended)

**Approach:** Create separate guide files for each audience

**Files:**
- `AUTHOR_GUIDE.md` - Complete guide for content authors (Part A)
- `EDITOR_GUIDE.md` - Complete guide for content editors (Part B)
- `PRODUCTION_GUIDE.md` - Complete guide for publishers (Part C)
- `ENGINEER_GUIDE.md` - Knowledge base engineering guide (Part D, extracted from current USER_GUIDE.md)
- `USER_GUIDE.md` - Overview that links to the 4 specialized guides

**Pros:**
- Focused, role-specific documentation
- Easier to navigate and maintain
- Smaller files load faster
- Can be updated independently

**Cons:**
- Multiple files to manage
- Need master overview/index

**Steps:**
1. Create `AUTHOR_GUIDE.md` with Part A content
2. Create `EDITOR_GUIDE.md` with Part B content
3. Create `PRODUCTION_GUIDE.md` with Part C content
4. Extract Part D to `ENGINEER_GUIDE.md`
5. Rewrite `USER_GUIDE.md` as overview with links to 4 guides
6. Update README.md to reference the guide suite
7. Commit all files

---

### Option 3: Modular Documentation System

**Approach:** Break content into smaller, focused modules

**Structure:**
```
docs/
├── README.md                       # Documentation index
├── authors/
│   ├── getting-started.md
│   ├── content-briefs.md
│   ├── using-knowledge-base.md
│   ├── workflows-lessons.md
│   ├── workflows-assessments.md
│   ├── workflows-activities.md
│   ├── ai-assistance.md
│   ├── quality-standards.md
│   └── collaboration.md
├── editors/
│   ├── getting-started.md
│   ├── editorial-workflow.md
│   ├── review-checklist.md
│   ├── providing-feedback.md
│   ├── approval-process.md
│   └── common-issues.md
├── production/
│   ├── getting-started.md
│   ├── workflow-overview.md
│   ├── pdf-production.md
│   ├── html-production.md
│   ├── scorm-production.md
│   ├── accessible-formats.md
│   ├── asset-management.md
│   ├── qa-checklist.md
│   └── delivery.md
└── engineers/
    ├── architecture.md
    ├── using-knowledge.md
    ├── adding-states.md
    ├── adding-subjects.md
    ├── creating-configs.md
    ├── extending-universal.md
    ├── best-practices.md
    ├── templates.md
    ├── qa.md
    ├── maintenance.md
    └── troubleshooting.md
```

**Pros:**
- Highly modular and maintainable
- Easy to find specific topics
- Can be reorganized easily
- Good for documentation websites

**Cons:**
- Many files to manage
- Need good navigation/index
- More complex structure

---

## Recommendation

**Option 2: Separate Guides** is recommended because:

1. **Role-specific focus** - Each guide serves one audience
2. **Manageable file sizes** - 600-800 lines per guide vs 3500+ in one file
3. **Independent updates** - Can update author guide without affecting engineers
4. **Better discoverability** - Clear file names match user roles
5. **Scales well** - Easy to add new role-specific guides later

---

## Next Steps

1. **Decide on approach** (Option 1, 2, or 3)
2. **Write comprehensive content** for Parts A, B, C based on outlines above
3. **Test documentation** with representatives from each role
4. **Iterate based on feedback**
5. **Commit final version**

---

**Current Status:** Structural foundation complete, awaiting content development for Parts A, B, C.

**Estimated Effort:** 12-20 hours to write all comprehensive content (Options 1 or 2)

**Priority:** High - Users need comprehensive authoring, editorial, and production guidance to use the system effectively.
