# HMH Multi-Curriculum Knowledge Base: Engineer's Guide
**For Knowledge Base Engineers and System Architects**
**Version:** 1.0
**Last Updated:** November 6, 2025

---

## Overview

This guide is for **knowledge base engineers** who extend and maintain the HMH Multi-Curriculum Knowledge Base system.

**Quick Navigation:**
- New to the system? Start with [Architecture Quick Start](#architecture-quick-start)
- Adding content? See [How to Use Existing Knowledge](#how-to-use-existing-knowledge)
- Expanding coverage? See [How to Add a New State/District](#how-to-add-a-new-statedistrict) or [How to Add a New Subject](#how-to-add-a-new-subject)
- Creating curricula? See [How to Create a New Curriculum Config](#how-to-create-a-new-curriculum-config)
- Adding frameworks? See [How to Extend Universal Knowledge](#how-to-extend-universal-knowledge)

**Related Guides:**
- Content Authors: See `AUTHOR_GUIDE.md`
- Content Editors: See `EDITOR_GUIDE.md`
- Publishers/Production: See `PRODUCTION_GUIDE.md`

---

## Table of Contents

1. [Architecture Quick Start](#architecture-quick-start)
2. [How to Use Existing Knowledge](#how-to-use-existing-knowledge)
3. [How to Add a New State/District](#how-to-add-a-new-statedistrict)
4. [How to Add a New Subject](#how-to-add-a-new-subject)
5. [How to Create a New Curriculum Config](#how-to-create-a-new-curriculum-config)
6. [How to Extend Universal Knowledge](#how-to-extend-universal-knowledge)
7. [File Creation Best Practices](#file-creation-best-practices)
8. [Templates and Patterns](#templates-and-patterns)
9. [Knowledge Base Quality Assurance](#knowledge-base-quality-assurance)
10. [Maintenance and Updates](#maintenance-and-updates)
11. [Troubleshooting](#troubleshooting)
12. [Quick Reference](#quick-reference)

---

## Your First Week as a Knowledge Base Engineer

### Welcome

You've joined as a Knowledge Base Engineer! Your role is critical: you design, build, and maintain the hierarchical knowledge system that enables 85-97% content reuse across all curricula.

**This section walks you through your first week, day by day.**

---

### Day 1: Understanding the System (6-8 hours)

**Morning: Architecture Deep Dive (3-4 hours)**

**Hour 1-2: Read Core Documentation**
- [ ] Read this entire guide (sections 1-2 minimum)
- [ ] Review `USER_GUIDE.md` for system overview
- [ ] Skim `AUTHOR_GUIDE.md` to understand user perspective
- [ ] Note: You'll reference these constantly

**Hour 3: Explore the Knowledge Base**
```bash
cd /reference/hmh-knowledge-v2

# See the 5-level hierarchy
ls -la

# Count files at each level
find universal -name "*.md" | wc -l
find subjects -name "*.md" | wc -l
find districts -name "*.md" | wc -l

# Read a universal file
cat universal/frameworks/dok-framework.md

# Read a subject-common file
cat subjects/mathematics/common/mlr/mlr1-stronger-clearer.md

# Read a district-wide file
cat districts/texas/language/elps-alignment.md
```

**Hour 4: Explore Curriculum Configs**
```bash
cd /config/curriculum

# Read all 4 existing configs
cat hmh-math-tx.json | python -m json.tool
cat hmh-math-ca.json | python -m json.tool
cat hmh-ela-tx.json | python -m json.tool
cat hmh-math-fl.json | python -m json.tool

# Note the resolution order patterns
```

**Afternoon: Trace Knowledge Resolution (3-4 hours)**

**Exercise 1: Trace Texas Math Resolution**

```bash
# Open config
cat /config/curriculum/hmh-math-tx.json

# Note resolution order (write down on paper):
# 1. /subjects/mathematics/districts/texas/into-math/
# 2. /subjects/mathematics/districts/texas/
# 3. /subjects/mathematics/common/
# 4. /districts/texas/
# 5. /publishers/hmh/
# 6. /universal/

# For each level, list what files exist
ls subjects/mathematics/districts/texas/into-math/  # (currently empty)
ls subjects/mathematics/districts/texas/           # TEKS alignment, gap mitigation
ls subjects/mathematics/common/                    # MLRs, vocab, problem-solving
ls districts/texas/                                # ELPS, IPACC, SBOE
ls publishers/hmh/                                 # Content block schema
ls universal/                                      # DOK, UDL, assessment, accessibility
```

**Exercise 2: Answer These Questions**
1. If I need MLR guidance for Texas Math, which file resolves? (Answer: `/subjects/mathematics/common/mlr/`)
2. If I need ELPS guidance for Texas Math, which file? (Answer: `/districts/texas/language/elps-alignment.md`)
3. If I need DOK guidance for Texas Math, which file? (Answer: `/universal/frameworks/dok-framework.md`)
4. Why does Texas Math reuse California's MLRs? (Answer: MLRs are subject-common, apply to all states)

**Day 1 Goals:**
- [ ] Understand 5-level hierarchy
- [ ] Can navigate knowledge base directory structure
- [ ] Understand resolution order (specific → general)
- [ ] Know where to find existing files

---

### Day 2: Hands-On Exploration (6-8 hours)

**Morning: Content Analysis (3-4 hours)**

**Exercise: Analyze Knowledge Reuse**

Pick a curriculum (e.g., HMH Math Texas) and calculate reuse:

```bash
# Count files available to TX Math
find subjects/mathematics/common -name "*.md" | wc -l        # Subject-common
find subjects/mathematics/districts/texas -name "*.md" | wc -l  # Subject-district
find districts/texas -name "*.md" | wc -l                    # District-wide
find universal -name "*.md" | wc -l                          # Universal

# Total available files = sum of above
# Texas-specific files = subject-district + district-wide
# Reused files = subject-common + universal
# Reuse % = (reused / total) * 100
```

**Exercise: Compare Across States**

```bash
# Compare TX Math vs CA Math
# TX Math uses:
- subjects/mathematics/districts/texas/teks-math-alignment.md  (NEW)
- districts/texas/language/elps-alignment.md                   (NEW)
- subjects/mathematics/common/*                                 (REUSED)
- universal/*                                                   (REUSED)

# CA Math uses:
- subjects/mathematics/districts/california/ccss-m-alignment.md (NEW)
- districts/california/language/eld-alignment.md                (NEW)
- subjects/mathematics/common/*                                 (REUSED)
- universal/*                                                   (REUSED)

# Both states reuse the SAME math-common and universal files!
```

**Afternoon: Shadow a Senior Engineer (3-4 hours)**

**If available, watch them:**
- Review a pull request adding a new knowledge file
- Make a small update to an existing file
- Test knowledge resolution after a change
- Explain their decision-making process

**If not available:**
- Review recent git commits: `git log --oneline -20`
- Read commit messages to understand changes
- Look at PR history in GitHub (if applicable)

**Day 2 Goals:**
- [ ] Can calculate knowledge reuse percentage
- [ ] Understand what makes content universal vs. subject-specific
- [ ] Observed or studied real KB engineering work
- [ ] Comfortable with git commands for KB repository

---

### Day 3: Small Enhancement (6-8 hours)

**Your First Task: Add a Missing Cross-Reference**

**Morning: Find Opportunities (2-3 hours)**

```bash
# Find files mentioning "DOK" but not linking to DOK framework
grep -r "DOK" /reference/hmh-knowledge-v2 --include="*.md" | grep -v "dok-framework"

# Pick one file that should reference DOK but doesn't
# Example: assessment file mentions DOK but doesn't link
```

**Task:**
1. Read the file
2. Identify where DOK framework reference should be added
3. Add reference: `See: /universal/frameworks/dok-framework.md`
4. Test: Verify linked file exists
5. Commit change

```bash
# Make change
nano [file-with-missing-reference].md

# Add in appropriate section:
# **See Also:** `/universal/frameworks/dok-framework.md`

# Test link
ls /reference/hmh-knowledge-v2/universal/frameworks/dok-framework.md

# Commit
git add [file]
git commit -m "Add cross-reference to DOK framework

- File: [filename]
- Added reference to DOK framework for clarity
- Improves navigation between related files"

git push origin master
```

**Afternoon: Reflect and Learn (3-4 hours)**

**Exercise: File Analysis**

Pick 3 files (one from each level: universal, subject-common, district-wide) and analyze:

1. **Structure:** Does it follow the template pattern?
2. **Examples:** Are examples clear and grade-appropriate?
3. **Cross-references:** Are related files linked?
4. **Completeness:** Any missing sections?

**Document findings** in notes (for yourself).

**Day 3 Goals:**
- [ ] Made first contribution to knowledge base
- [ ] Used git workflow (add, commit, push)
- [ ] Understand file structure expectations
- [ ] Can identify good vs. weak KB files

---

### Day 4: Plan a Small Addition (6-8 hours)

**Scenario: Your supervisor asks you to add support for a CCSS state (e.g., New York)**

**Morning: Research and Planning (3-4 hours)**

**Step 1: Determine State Type**
- [ ] Research: Does NY use CCSS-M for math? (Yes)
- [ ] Research: Does NY use NGSS for science? (Yes)
- [ ] Conclusion: Type A state (2-3 files needed)

**Step 2: Identify What Files to Create**
- [ ] `/districts/new-york/compliance/new-york-adoption-criteria.md`
- [ ] `/districts/new-york/language/nyseslat-alignment.md`
- [ ] `/subjects/mathematics/districts/new-york/ccss-m-ny-notes.md` (reference to CA file)

**Step 3: Find Templates/Examples**
- [ ] Review California compliance file (similar structure)
- [ ] Review California language file (adapt to NY framework)
- [ ] Note what to reuse vs. what's NY-specific

**Step 4: Document Plan**

Create a planning document:
```markdown
# Plan: Add New York State Support

## Files to Create:
1. NY Compliance: [path] - ~18KB - Template: CA compliance file
2. NY Language Standards: [path] - ~15KB - Template: ELPS structure
3. NY Math Notes: [path] - ~8KB - Template: Reference file

## Reuse Strategy:
- CCSS-M alignment: Reuse CA file, add NY notes
- Universal: Reuse all 15 files (100%)
- Math-common: Reuse all 12 files (100%)

## Knowledge Reuse Rate: ~94%

## Timeline:
- Day 4: Research and planning (today)
- Day 5: Create files, test, commit

## Questions/Blockers:
- Need NY ESOL framework specifics (reach out to SME)
```

**Afternoon: Draft First File (3-4 hours)**

**Task: Draft NY Compliance File**

```bash
# Create directory
mkdir -p /reference/hmh-knowledge-v2/districts/new-york/compliance

# Copy template
cp districts/california/compliance/california-adoption-criteria.md \
   districts/new-york/compliance/new-york-adoption-criteria.md

# Edit file - replace CA specifics with NY
nano districts/new-york/compliance/new-york-adoption-criteria.md
```

**Changes to make:**
- Update title: "New York Adoption Criteria"
- Update state-specific sections
- Keep structure from CA file
- Note what NY reuses from universal/subject-common

**Don't commit yet** - Day 5 for final review and commit

**Day 4 Goals:**
- [ ] Can research state requirements independently
- [ ] Can plan multi-file addition systematically
- [ ] Drafted first substantial file
- [ ] Comfortable adapting templates

---

### Day 5: Complete and Test Addition (6-8 hours)

**Morning: Finish Files (3-4 hours)**

**Task 1: Complete NY Compliance File**
- Review draft from Day 4
- Fill in any [TBD] sections
- Verify all cross-references exist
- Check for typos and formatting

**Task 2: Create NY Language Standards File**
```bash
nano districts/new-york/language/nyseslat-alignment.md
```

Use ELPS file as template, adapt to NYSESLAT framework.

**Task 3: Create NY Math Notes File**
```bash
nano subjects/mathematics/districts/new-york/ccss-m-ny-notes.md
```

Brief file noting NY uses CCSS-M, reference to CA file.

**Afternoon: Test and Commit (3-4 hours)**

**Testing Checklist:**
- [ ] All files in correct directory structure?
- [ ] File naming follows kebab-case?
- [ ] All internal links use relative paths?
- [ ] All linked files exist?
- [ ] Markdown syntax valid?
- [ ] No spelling errors?
- [ ] Examples are NY-appropriate?

```bash
# Test links
grep -o '\`/[^`]*\.md\`' [new-file] | tr -d '`' | while read file; do
  if [ ! -f "$file" ]; then
    echo "Broken link: $file"
  fi
done

# Validate structure
ls -la districts/new-york/compliance/
ls -la districts/new-york/language/
ls -la subjects/mathematics/districts/new-york/

# Final review
cat districts/new-york/compliance/new-york-adoption-criteria.md | head -50
```

**Commit:**
```bash
git add districts/new-york
git add subjects/mathematics/districts/new-york

git commit -m "Add New York state support (CCSS/NGSS state)

New Files:
- districts/new-york/compliance/new-york-adoption-criteria.md
- districts/new-york/language/nyseslat-alignment.md
- subjects/mathematics/districts/new-york/ccss-m-ny-notes.md

Knowledge Reuse: ~94%
- Reuses all 15 universal files
- Reuses all 12 math-common files
- Adds 3 NY-specific files

NY Math now has 30 total files available with 94% reuse."

git push origin master
```

**Day 5 Goals:**
- [ ] Completed multi-file addition
- [ ] Tested all links and references
- [ ] Successfully committed and pushed
- [ ] Documented knowledge reuse rate

---

### Week 1 Reflection

**End of Week: Self-Assessment**

**Skills Acquired:**
- ✅ Navigate knowledge base hierarchy
- ✅ Understand resolution order
- ✅ Calculate knowledge reuse percentage
- ✅ Adapt templates for new states
- ✅ Test links and validate files
- ✅ Use git workflow

**Next Steps (Weeks 2-4):**
- **Week 2:** Add a more complex state (state-specific standards)
- **Week 3:** Add a new subject (requires subject-common files)
- **Week 4:** Create a curriculum config and test end-to-end

**Resources for Continued Learning:**
- Section 3: Adding States/Districts (detailed guidance)
- Section 4: Adding Subjects (subject-common files)
- Section 7: Best Practices (writing standards)
- Section 9: QA (quality checklist)

---

## Architecture Quick Start

### What is This System?

The **HMH Multi-Curriculum Knowledge Base** is a hierarchical content development system that enables creating standards-aligned, state-compliant, accessible instructional materials for **any state, any subject, any grade level** with **85-97% knowledge reuse**.

### Key Benefits:

- **DRY Principle:** Write once, reuse everywhere (98% reduction in duplicate files)
- **Scalability:** Add new states/subjects with minimal effort (2-6 files per state)
- **Consistency:** Single source of truth ensures quality across all products
- **Maintainability:** Update once, applies to all curricula
- **Flexibility:** Supports unlimited curriculum combinations

### Current Coverage (Week 3):

- **States:** Texas, California, Florida
- **Subjects:** Mathematics, ELA, Science
- **Grade Levels:** K-8
- **Files:** 50 knowledge files + 4 curriculum configs
- **Proven Reuse:** 85-97% across new curricula

---

## Architecture Quick Start

### Hierarchical Knowledge Resolution

The system uses a **5-level hierarchy** from most specific to most general:

```
1. Program-Specific        (e.g., Into Math TX specific features)
   └─ 2. Subject-District  (e.g., Texas Math TEKS alignment)
       └─ 3. Subject-Common (e.g., Math MLRs - all states)
           └─ 4. District-Wide (e.g., Texas ELPS - all subjects)
               └─ 5. Universal (e.g., DOK Framework - everything)
```

**Resolution Rule:** Search from specific to general, **first match wins**.

### Directory Structure

```
/reference/hmh-knowledge-v2/
├── universal/                  # Level 5: Cross-everything
│   ├── frameworks/             # DOK, UDL, EB Scaffolding, Sentence Frames
│   ├── assessment/             # Item types, rubrics, answer keys, validation
│   ├── accessibility/          # WCAG compliance
│   ├── content-equity/         # CEID guidelines
│   └── vendor/                 # HMH QA checklist
│
├── subjects/                   # Level 3: Subject-Common
│   ├── mathematics/
│   │   ├── common/             # MLRs, vocab, problem-solving (all states)
│   │   └── districts/          # Level 2: Subject-District
│   │       ├── texas/          # TEKS Math, gap mitigation
│   │       ├── california/     # CCSS-M alignment
│   │       └── florida/        # MAFS alignment
│   │
│   ├── ela/
│   │   ├── common/             # Literacy routines (all states)
│   │   └── districts/
│   │       └── texas/          # TEKS ELA
│   │
│   └── science/
│       └── common/             # NGSS alignment, practices (all states)
│
├── districts/                  # Level 4: District-Wide
│   ├── texas/
│   │   ├── compliance/         # IPACC, SBOE, checklist
│   │   └── language/           # ELPS (all subjects)
│   │
│   ├── california/
│   │   ├── compliance/         # Adoption criteria
│   │   └── language/           # ELD (all subjects)
│   │
│   └── florida/
│       ├── compliance/         # Florida statutory compliance
│       └── language/           # ESOL/WIDA (all subjects)
│
└── publishers/                 # Level 1: Program-Specific (optional)
    └── hmh/
        └── content-block-schema.json

/config/curriculum/             # Curriculum configurations
├── hmh-math-tx.json
├── hmh-math-ca.json
├── hmh-ela-tx.json
└── hmh-math-fl.json
```

---

## How to Use Existing Knowledge

### Step 1: Identify Your Curriculum

Determine:
- **State/District:** Texas, California, Florida, etc.
- **Subject:** Mathematics, ELA, Science, Social Studies, etc.
- **Grade Level:** K-2, 3-5, 6-8, 9-12
- **Program:** Into Math, Into Reading, Into Science, etc.

**Example:** HMH Into Math Grade 5 for Texas

### Step 2: Check if Config Exists

Look in `/config/curriculum/` for a matching JSON file.

**Existing configs:**
- K-8 Programs:
  - `hmh-math-tx.json` - HMH Into Math Texas (K-8)
  - `hmh-math-ca.json` - HMH Into Math California (K-8)
  - `hmh-ela-tx.json` - HMH Into Reading Texas (K-8)
  - `hmh-math-fl.json` - HMH Into Math Florida (K-8)
- High School Courses:
  - `hmh-algebra1-tx.json` - HMH Algebra I Texas Edition (grades 8-9)
  - `hmh-biology-tx.json` - HMH Biology Texas Edition (grades 9-10)
  - `hmh-ap-calc-ab.json` - HMH AP Calculus AB (grades 11-12)
  - `hmh-ap-english-lit.json` - HMH AP English Literature and Composition (grades 11-12)

If your curriculum exists, proceed to Step 3.
If not, see [How to Create a New Curriculum Config](#how-to-create-a-new-curriculum-config).

### Step 3: Review Resolution Order

Open the config file and note the `knowledge_resolution.order` array.

**Example from `hmh-math-tx.json`:**
```json
"knowledge_resolution": {
  "order": [
    "/reference/hmh-knowledge-v2/subjects/mathematics/districts/texas/into-math/",
    "/reference/hmh-knowledge-v2/subjects/mathematics/districts/texas/",
    "/reference/hmh-knowledge-v2/subjects/mathematics/common/",
    "/reference/hmh-knowledge-v2/districts/texas/",
    "/reference/hmh-knowledge-v2/publishers/hmh/",
    "/reference/hmh-knowledge-v2/universal/"
  ]
}
```

**This means:**
1. First, look in Texas Math Into Math program-specific folder
2. If not found, look in Texas Math general folder (TEKS alignment)
3. If not found, look in Math common (MLRs, vocabulary)
4. If not found, look in Texas district-wide (ELPS, IPACC)
5. If not found, look in HMH publisher folder
6. Finally, look in universal (DOK, UDL, assessment)

### Step 4: Find Knowledge You Need

**Common Scenarios:**

**Scenario 1: I need scaffolding strategies for emergent bilinguals**
- **Resolves to:** Universal → `/universal/frameworks/eb-scaffolding-guide.md`
- **Why:** EB scaffolding applies to all states, subjects, grades

**Scenario 2: I need Texas Math standards alignment**
- **Resolves to:** Subject-District → `/subjects/mathematics/districts/texas/teks-math-alignment.md`
- **Why:** TEKS Math specific to Texas Math

**Scenario 3: I need Math Language Routines**
- **Resolves to:** Subject-Common → `/subjects/mathematics/common/mlr/mlr1-stronger-clearer.md` (etc.)
- **Why:** MLRs apply to all states' math programs

**Scenario 4: I need Texas language standards**
- **Resolves to:** District-Wide → `/districts/texas/language/elps-alignment.md`
- **Why:** ELPS applies to all subjects in Texas (Math, ELA, Science, etc.)

### Step 5: Navigate to File

Use the resolution order to find the file:

```bash
# Example: Finding ELPS alignment for Texas Math
cd /reference/hmh-knowledge-v2
cat districts/texas/language/elps-alignment.md
```

### Step 6: Apply Knowledge

Read the file and apply guidance to your lesson/assessment/content development.

**Files include:**
- Standards alignment requirements
- Instructional routines (MLRs, literacy routines, science practices)
- Scaffolding strategies by proficiency level
- Assessment guidance
- Compliance requirements
- Examples and templates

---

## How to Add a New State/District

**Use Case:** You need to support a new state (e.g., New York, Illinois, Ohio)

### Determine State Type

**Type A: CCSS/NGSS State (Easy)**
- Uses Common Core State Standards (CCSS-M) for math
- Uses Next Generation Science Standards (NGSS) for science
- **Effort:** 2-3 files
- **Examples:** New York, Illinois, Pennsylvania, Washington, Oregon

**Type B: State-Specific Standards (Moderate)**
- Has unique state standards
- **Effort:** 4-6 files
- **Examples:** Virginia (SOL), Indiana, Georgia

**Type C: Already Covered (No Work)**
- Texas, California, Florida already exist
- **Effort:** 0 files

### Step-by-Step: Adding a CCSS/NGSS State

**Example: Adding New York**

#### 1. Create District Folder

```bash
mkdir -p /reference/hmh-knowledge-v2/districts/new-york/compliance
mkdir -p /reference/hmh-knowledge-v2/districts/new-york/language
```

#### 2. Create Compliance File

**File:** `/districts/new-york/compliance/new-york-adoption-criteria.md`

**Template:** Copy from California or Texas, adapt to NY requirements

**Key sections:**
- NY-specific adoption process
- Content restrictions (if any unique to NY)
- Comparison to other states
- Reuse documentation (what NY reuses from universal/subject-common)

**Estimated size:** 15-20KB

#### 3. Create Language Standards File

**File:** `/districts/new-york/language/nyseslat-alignment.md`

(NYSESLAT = New York State English as a Second Language Achievement Test)

**Template:** Copy from ELPS (Texas) or ELD (California), adapt to NY

**Key sections:**
- NY language proficiency levels
- Scaffolding by level
- Integration with content instruction
- Comparison to ELPS/ELD

**Estimated size:** 12-18KB

#### 4. Create Subject-Specific Notes (if needed)

**For Math:**
**File:** `/subjects/mathematics/districts/new-york/ccss-m-ny-notes.md`

**Content:**
- Note that NY uses CCSS-M (can reuse California's CCSS-M file)
- Any NY-specific variations or emphases
- NY math assessment (NYSAA/Regents exams)
- Link to California CCSS-M file for full alignment

**Estimated size:** 5-10KB (mostly references)

**For ELA:** Similar file for NY ELA notes

**For Science:** Note that NY uses NGSS (reuse existing NGSS file)

#### 5. Total Files for NY

- `/districts/new-york/compliance/new-york-adoption-criteria.md` (18KB)
- `/districts/new-york/language/nyseslat-alignment.md` (15KB)
- `/subjects/mathematics/districts/new-york/ccss-m-ny-notes.md` (8KB)
- **Total: 3 files, ~41KB**

**Reuse:** NY Math now reuses 47 existing files (94% reuse rate)

---

### Step-by-Step: Adding a State-Specific Standards State

**Example: Adding Virginia (Virginia SOL standards)**

#### 1. Create District Folder

```bash
mkdir -p /reference/hmh-knowledge-v2/districts/virginia/compliance
mkdir -p /reference/hmh-knowledge-v2/districts/virginia/language
```

#### 2. Create Compliance File

Same as CCSS state (Step 2 above)

#### 3. Create Language Standards File

Same as CCSS state (Step 3 above)

#### 4. Create Full Subject Standards Files

**Unlike CCSS states, Virginia needs full standards alignment files.**

**File:** `/subjects/mathematics/districts/virginia/sol-math-alignment.md`

**Template:** Copy from Texas TEKS Math alignment, adapt to Virginia SOL

**Key sections:**
- SOL Math standard format
- Sample standards by grade (3, 5, 8)
- Integration with Mathematical Process Goals (Virginia's version of practices)
- Comparison to TEKS and CCSS-M
- Vertical alignment
- Assessment (Virginia SOL tests)

**Estimated size:** 15-20KB

**Repeat for ELA, Science, Social Studies**

#### 5. Total Files for Virginia

- `/districts/virginia/compliance/virginia-adoption-criteria.md` (18KB)
- `/districts/virginia/language/wida-virginia.md` (15KB) - if using WIDA
- `/subjects/mathematics/districts/virginia/sol-math-alignment.md` (18KB)
- `/subjects/ela/districts/virginia/sol-ela-alignment.md` (18KB)
- `/subjects/science/districts/virginia/sol-science-alignment.md` (18KB)
- `/subjects/social-studies/districts/virginia/sol-social-studies-alignment.md` (18KB)
- **Total: 6 files, ~105KB**

**Reuse:** Virginia Math still reuses 44 existing files (88% reuse rate)

---

### Quick Reference: State Type Decision Tree

```
Is the state already covered (TX, CA, FL)?
├─ YES → Use existing files (0 new files needed)
└─ NO → Does state use CCSS-M and/or NGSS?
    ├─ YES (CCSS/NGSS state)
    │   └─ Create: 2-3 files (compliance, language, notes)
    │       → 90-95% reuse from existing files
    │
    └─ NO (State-specific standards)
        └─ Create: 4-6 files (compliance, language, + standards per subject)
            → 85-90% reuse from existing files
```

---

## How to Add a New Subject

**Use Case:** You need to support a new subject (e.g., Social Studies, Computer Science, Arts)

### Determine Subject Type

**Type A: Standards-Based Core Subject**
- Has national framework (C3, CSTA, National Core Arts Standards, etc.)
- Multiple grade levels
- **Examples:** Social Studies, Computer Science, Arts, PE
- **Effort:** 8-15 subject-common files

**Type B: Specialized/Support Subject**
- Cross-cutting (Special Education, Gifted & Talented)
- Or niche (CTE programs)
- **Effort:** 5-10 files

### Step-by-Step: Adding Social Studies

#### 1. Research the Standards Framework

**Social Studies uses:**
- **C3 Framework** (College, Career, and Civic Life Framework)
- **State-specific standards** (Texas TEKS Social Studies, CA History-Social Science, etc.)

#### 2. Create Subject-Common Folder

```bash
mkdir -p /reference/hmh-knowledge-v2/subjects/social-studies/common
mkdir -p /reference/hmh-knowledge-v2/subjects/social-studies/common/c3-practices
```

#### 3. Create Core Subject-Common Files

**File 1:** `/subjects/social-studies/common/c3-framework-alignment.md`

**Content:**
- C3 Framework overview (Inquiry Arc)
- Four dimensions: Developing Questions, Applying Disciplinary Concepts, Evaluating Sources/Using Evidence, Communicating Conclusions
- Integration with state standards
- Performance expectations by grade band

**Size:** 20-25KB
**Template:** Copy structure from NGSS alignment guide

---

**File 2:** `/subjects/social-studies/common/inquiry-arc-practices.md`

**Content:**
- Instructional routines for each dimension of Inquiry Arc
- Practice 1: Developing Compelling Questions
- Practice 2: Applying Disciplinary Concepts (Civics, Economics, Geography, History)
- Practice 3: Evaluating Sources and Using Evidence
- Practice 4: Communicating Conclusions and Taking Informed Action
- Examples by grade level

**Size:** 18-22KB
**Template:** Copy structure from Science Practices Framework

---

**File 3:** `/subjects/social-studies/common/historical-thinking-skills.md`

**Content:**
- Chronological reasoning
- Causation and argumentation
- Contextualization
- Comparison
- Historical interpretation
- Primary source analysis

**Size:** 12-15KB

---

**File 4:** `/subjects/social-studies/common/primary-source-analysis-protocol.md`

**Content:**
- Protocol for analyzing primary sources (documents, images, artifacts)
- Sourcing, contextualization, corroboration, close reading
- Integration with literacy routines
- Scaffolds for emergent bilinguals

**Size:** 15-18KB
**Template:** Adapt from Close Reading Protocol (ELA)

---

**File 5:** `/subjects/social-studies/common/geography-reasoning-framework.md`

**Content:**
- Five Themes of Geography
- Spatial thinking skills
- Map reading and analysis
- Geographic inquiry

**Size:** 10-12KB

---

**File 6-8:** Additional subject-common files as needed
- Civic engagement practices
- Economic reasoning
- Social studies vocabulary guidelines
- etc.

**Total for Social Studies Subject-Common:** 8-10 files, ~120-150KB

#### 4. Create State-Specific Subject-District Files

**For Texas:**
**File:** `/subjects/social-studies/districts/texas/teks-social-studies-alignment.md`

**Content:**
- TEKS Social Studies standard format
- Sample standards by grade
- Integration with C3 Framework
- Texas-specific emphases (Texas history, government)

**Size:** 15-18KB
**Template:** Copy from TEKS Math or TEKS ELA alignment

**Repeat for California, Florida, and other states as needed.**

#### 5. Total Files for Social Studies

**Subject-Common:** 8-10 files (reused by all states)
**Per State:** 1 standards alignment file

**Example for 3 states:**
- 10 subject-common files
- 3 state-specific files (TX, CA, FL)
- **Total: 13 files**

**Reuse:** Each new state adds only 1 file, reuses all 10 subject-common + all universal

---

### Quick Reference: Subject Addition Checklist

- [ ] Research national/state standards framework
- [ ] Create subject-common folder
- [ ] Create framework alignment file (like NGSS, C3, CSTA)
- [ ] Create instructional practices file (like MLRs, Science Practices)
- [ ] Create 3-5 additional subject-common files (vocabulary, protocols, etc.)
- [ ] For each state: Create subject-district standards alignment file
- [ ] Test knowledge resolution with sample lesson
- [ ] Document knowledge reuse rate

---

## How to Create a New Curriculum Config

**Use Case:** You need to create a new curriculum combination (e.g., HMH Into Reading California, HMH Into Science Florida)

### Step-by-Step: Creating a Config

**Example: HMH Into Reading California Edition**

#### 1. Copy Existing Similar Config

```bash
cd /config/curriculum
cp hmh-ela-tx.json hmh-ela-ca.json
```

#### 2. Edit Basic Metadata

Open `hmh-ela-ca.json` and update:

```json
{
  "id": "hmh-into-reading-ca",
  "name": "HMH Into Reading California Edition",
  "publisher": "hmh",
  "program": "into-reading",
  "subject": "ela",
  "district": "california",
  "grades": ["K", "1", "2", "3", "4", "5", "6", "7", "8"],
  "version": "2024",
```

#### 3. Update Knowledge Resolution Order

Replace Texas paths with California paths:

```json
  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge-v2/subjects/ela/districts/california/into-reading/",
      "/reference/hmh-knowledge-v2/subjects/ela/districts/california/",
      "/reference/hmh-knowledge-v2/subjects/ela/common/",
      "/reference/hmh-knowledge-v2/districts/california/",
      "/reference/hmh-knowledge-v2/publishers/hmh/",
      "/reference/hmh-knowledge-v2/universal/"
    ],
    "description": "Resolution order searches from most specific (Into Reading California) to most general (universal)."
  },
```

#### 4. Update Standards

```json
  "standards": {
    "content": "CCSS ELA",
    "language": "ELD (California)",
    "accessibility": "WCAG 2.1 AA"
  },
```

#### 5. Update Compliance Requirements

```json
  "compliance": {
    "required": [
      "CCSS ELA alignment",
      "ELD support (3 proficiency levels)",
      "California adoption criteria",
      "CEID diversity standards",
      "Accessibility (WCAG 2.1 AA)"
    ]
  },
```

#### 6. Add ELD Framework Info

```json
  "eld_framework": {
    "name": "California English Language Development Standards",
    "proficiency_levels": 3,
    "levels": [
      "Emerging",
      "Expanding",
      "Bridging"
    ],
    "parts": [
      "Part I: Interacting in Meaningful Ways",
      "Part II: Learning About How English Works",
      "Part III: Using Foundational Literacy Skills"
    ]
  },
```

#### 7. Document Knowledge Reuse

```json
  "knowledge_reuse": {
    "universal_files_reused": 15,
    "ela_common_files_reused": 4,
    "california_district_files_reused": 2,
    "california_ela_specific_files": 1,
    "total_files_available": 22,
    "new_files_needed": 1,
    "reuse_percentage": 95,
    "note": "California ELA achieves ~95% knowledge reuse."
  },
```

#### 8. Add Validation Status

```json
  "validation_status": {
    "architecture_validated": true,
    "knowledge_resolution_tested": true,
    "demonstrates": "California ELA scalability",
    "curriculum_number": 5,
    "states_supported": ["Texas", "California", "Florida"]
  }
}
```

#### 9. Save and Test

```bash
# Validate JSON syntax
cat hmh-ela-ca.json | python -m json.tool

# Test resolution by checking if files exist
# (manually or with a script)
```

---

### Example 2: Creating a High School Config

**Use Case:** Creating HMH AP Calculus AB (national course, not state-specific)

#### Differences for High School Configs

High school configs differ from K-8 in several ways:
- **Course-specific** (e.g., "Algebra I", "Biology") rather than grade-band programs
- **Specific grade levels** (e.g., [" 11", "12"]) not full K-8 range
- **AP courses** are national (district: null) with College Board standards
- **Knowledge resolution** includes high school-specific paths
- **Standards** reference state graduation requirements, EOC exams, AP frameworks
- **College/career readiness** focus with credit articulation

#### 1. Create New Config File

```bash
cd /config/curriculum
# Copy from similar HS course or create new
touch hmh-ap-calc-ab.json
```

#### 2. Add HS-Specific Metadata

```json
{
  "id": "hmh-ap-calculus-ab",
  "name": "HMH AP Calculus AB",
  "publisher": "hmh",
  "program": "ap-calculus",
  "subject": "mathematics",
  "district": null,  // AP courses are national, not state-specific
  "grades": ["11", "12"],  // Typical HS grades for AP Calc
  "course": "AP Calculus AB",
  "ap_course": true,  // Flag for AP courses
  "version": "2024",
```

#### 3. Update Knowledge Resolution for HS

```json
  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge/subjects/mathematics/high-school/",  // HS math content
      "/reference/hmh-knowledge/subjects/mathematics/common/",       // MLRs, vocab
      "/reference/hmh-knowledge/universal/high-school/",             // HS pedagogy, college/career
      "/reference/hmh-knowledge/universal/"                          // UDL, DOK, assessment
    ],
    "description": "Resolution for AP course: subject HS → common → universal HS → universal"
  },
```

**Key Difference:** HS configs include `/subjects/[subject]/high-school/` and `/universal/high-school/` in resolution order.

#### 4. Add College Board Standards

```json
  "standards": {
    "primary": "College Board AP Calculus AB",
    "secondary": "Common Core State Standards - Mathematics (HS)",
    "frameworks": ["College/Career Readiness"]
  },
```

#### 5. Add AP-Specific Assessment Info

```json
  "assessments": {
    "ap_exam": {
      "format": "AP Calculus AB Exam",
      "sections": ["Multiple Choice", "Free Response"],
      "calculator_policy": "Graphing calculator required"
    }
  },
```

#### 6. Add College Credit Articulation

```json
  "college_credit": {
    "eligible": true,
    "typical_credit": "3-5 credits",
    "score_requirement": "3 or higher (varies by institution)"
  }
}
```

#### 7. For State-Specific HS Courses (e.g., Algebra I Texas)

If creating a state-specific HS course, include state paths:

```json
{
  "id": "hmh-algebra1-tx",
  "name": "HMH Algebra I Texas Edition",
  "district": "texas",
  "grades": ["8", "9"],  // Algebra I can be 8th or 9th grade
  "course": "Algebra I",

  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge/subjects/mathematics/districts/texas/",  // TEKS
      "/reference/hmh-knowledge/subjects/mathematics/high-school/",      // Algebra I content
      "/reference/hmh-knowledge/subjects/mathematics/common/",           // MLRs
      "/reference/hmh-knowledge/districts/texas/high-school/",           // TX graduation requirements
      "/reference/hmh-knowledge/districts/texas/",                       // ELPS
      "/reference/hmh-knowledge/universal/high-school/",                 // HS pedagogy
      "/reference/hmh-knowledge/universal/"                              // UDL, DOK
    ]
  },

  "standards": {
    "primary": "TEKS Mathematics - Algebra I",
    "language": "ELPS",
    "assessments": ["STAAR Algebra I EOC"]
  },

  "compliance": {
    "state_adoption": true,
    "sboe_aligned": true,
    "eoc_preparation": "STAAR Algebra I"
  }
}
```

**Key Additions for State HS:**
- State district paths come BEFORE high school content paths
- Graduation requirement files referenced
- EOC exam preparation noted
- State compliance requirements included

---

### Config File Template

**Location:** `/config/curriculum/TEMPLATE.json`

```json
{
  "id": "[publisher]-[program]-[district-code]",
  "name": "[Publisher] [Program Name] [District/State] Edition",
  "publisher": "[hmh|other]",
  "program": "[into-math|into-reading|into-science|etc]",
  "subject": "[mathematics|ela|science|social-studies|etc]",
  "district": "[texas|california|florida|new-york|etc]",
  "grades": ["K", "1", "2", "3", "4", "5", "6", "7", "8"],
  "version": "2024",

  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge-v2/subjects/[subject]/districts/[district]/[program]/",
      "/reference/hmh-knowledge-v2/subjects/[subject]/districts/[district]/",
      "/reference/hmh-knowledge-v2/subjects/[subject]/common/",
      "/reference/hmh-knowledge-v2/districts/[district]/",
      "/reference/hmh-knowledge-v2/publishers/[publisher]/",
      "/reference/hmh-knowledge-v2/universal/"
    ],
    "description": "Resolution order from specific to general."
  },

  "standards": {
    "content": "[TEKS|CCSS|MAFS|B.E.S.T.|SOL|etc]",
    "language": "[ELPS|ELD|ESOL|WIDA|etc]",
    "accessibility": "WCAG 2.1 AA"
  },

  "compliance": {
    "required": [
      "[State] standards alignment",
      "[Language] support",
      "[State]-specific compliance",
      "CEID diversity standards",
      "Accessibility requirements"
    ]
  },

  "language_framework": {
    "name": "[Framework Name]",
    "proficiency_levels": "[3|4|6]",
    "levels": ["[Level 1]", "[Level 2]", "..."]
  },

  "knowledge_reuse": {
    "universal_files_reused": 15,
    "[subject]_common_files_reused": 0,
    "[district]_district_files_reused": 0,
    "[subject_district]_specific_files": 0,
    "total_files_available": 0,
    "new_files_needed": 0,
    "reuse_percentage": 0
  },

  "validation_status": {
    "architecture_validated": false,
    "knowledge_resolution_tested": false,
    "notes": ""
  }
}
```

---

## How to Extend Universal Knowledge

**Use Case:** You want to add a new universal framework that applies to all subjects, states, and grades.

### When to Add Universal Files

Add to universal when:
- ✅ Applies to **ALL subjects** (Math, ELA, Science, Social Studies, etc.)
- ✅ Applies to **ALL states/districts**
- ✅ Applies to **ALL grade levels** (K-12)
- ✅ No customization needed per state/subject

**Examples of Universal Knowledge:**
- DOK Framework (cognitive demand levels)
- UDL Principles (universal design for learning)
- CEID Guidelines (equity and inclusion)
- WCAG Compliance (web accessibility)
- Assessment best practices (item writing, rubrics)
- Sentence Frames Library
- EB Scaffolding strategies

**Counter-examples (NOT universal):**
- Standards alignment (varies by state) → Subject-District level
- Language proficiency standards (varies by state) → District-Wide level
- MLRs (math-specific) → Subject-Common level

### Step-by-Step: Adding Bloom's Taxonomy

**Example:** Adding Bloom's Taxonomy as a complement to DOK

#### 1. Determine Category

Bloom's Taxonomy is universal:
- Applies to all subjects
- Applies to all states
- Applies to all grades

**Category:** Universal Framework

#### 2. Create File

**Location:** `/reference/hmh-knowledge-v2/universal/frameworks/blooms-taxonomy-guide.md`

#### 3. Structure the File

**Template:**
```markdown
# Bloom's Taxonomy Guide
**Cognitive Levels for Learning Objectives**
**Scope:** Universal (all subjects, all districts, all grades)
**Audience:** Curriculum developers writing learning objectives

---

## Overview

[Explanation of Bloom's Taxonomy]

**Core Principle:** [State the key principle]

---

## Six Levels of Bloom's Taxonomy

### Level 1: Remember
[Description, examples, verbs]

### Level 2: Understand
[Description, examples, verbs]

### Level 3: Apply
[Description, examples, verbs]

### Level 4: Analyze
[Description, examples, verbs]

### Level 5: Evaluate
[Description, examples, verbs]

### Level 6: Create
[Description, examples, verbs]

---

## Integration with DOK

[Comparison table: Bloom's vs. DOK]

---

## Application by Subject

### Mathematics
[Examples]

### ELA
[Examples]

### Science
[Examples]

---

## Writing Learning Objectives with Bloom's

[Guidance and examples]

---

## Resources

**Related Guides:**
- DOK Framework: `/universal/frameworks/dok-framework.md`
- Assessment: `/universal/assessment/item-writing-best-practices.md`

---

**Remember:** [Key takeaway]
```

#### 4. Cross-Reference from Related Files

Update DOK Framework to mention Bloom's:

**In `/universal/frameworks/dok-framework.md`:**

Add section:
```markdown
## DOK vs. Bloom's Taxonomy

DOK and Bloom's are complementary frameworks:

| Aspect | DOK | Bloom's |
|--------|-----|---------|
| Focus | Complexity of thinking | Type of thinking |
| Levels | 4 (Recall to Extended Thinking) | 6 (Remember to Create) |
| Use | Depth of knowledge required | Cognitive process |

**See Also:** `/universal/frameworks/blooms-taxonomy-guide.md`
```

#### 5. Test Reuse

After adding Bloom's Taxonomy:
- It's immediately available to ALL curricula
- All 4 existing curricula now have access
- All future curricula automatically include it
- **Reuse: 100% across all present and future curricula**

---

### Universal File Categories

**Current Universal Categories:**
- **frameworks/** - DOK, UDL, EB Scaffolding, Sentence Frames, Bloom's (new)
- **assessment/** - Item types, rubrics, answer keys, validation, item writing
- **accessibility/** - WCAG compliance
- **content-equity/** - CEID guidelines
- **vendor/** - HMH QA checklist

**Potential New Categories:**
- **pedagogy/** - Instructional models (PBL, SIOP, etc.)
- **technology/** - EdTech integration, LMS guidance
- **data/** - Learning analytics, formative assessment
- **sel/** - Social-emotional learning frameworks

---

## File Creation Best Practices

### Markdown Formatting Standards

**Use consistent structure:**

```markdown
# File Title
**Descriptive Subtitle**
**Scope:** [Universal|Subject-Common|District-Wide|Subject-District|Program-Specific]
**Audience:** [Target users]

---

## Overview

[2-3 paragraphs introducing the topic]

**Core Principle:** [One-sentence key principle]

---

## Main Content Section 1

### Subsection 1.1

[Content]

**Examples:**
✅ Good example
❌ Bad example (with explanation)

---

## Main Content Section 2

[Content with tables, lists, code blocks as needed]

---

## Resources

**Related Guides:**
- [Title]: `[relative/path/to/file.md]`

**External Resources:**
- [Name]: [URL]

---

**Remember:** [Key takeaway in 1-2 sentences]
```

### Writing Style Guidelines

**Tone:**
- Professional but accessible
- Direct and actionable
- Avoid jargon unless necessary (then define it)
- Use examples liberally

**Structure:**
- Start with "why" (purpose and benefits)
- Then "what" (concepts and frameworks)
- Then "how" (step-by-step procedures)
- End with "resources" (related files, external links)

**Length:**
- Aim for 12-20KB for comprehensive guides
- Use examples to illustrate concepts
- Include comparison tables for clarity

**Examples:**
- Provide grade-level examples
- Show both good and bad examples (✅/❌)
- Include edge cases and common mistakes

**Cross-References:**
- Always link to related files with relative paths
- Group references by hierarchy level (universal, subject-common, district-wide)
- Use "See Also" sections consistently

### File Naming Conventions

**Use kebab-case (lowercase with hyphens):**
✅ `dok-framework.md`
✅ `mlr1-stronger-clearer.md`
✅ `texas-compliance-checklist.md`

❌ `DOK_Framework.md`
❌ `MLR1 Stronger and Clearer.md`
❌ `TexasComplianceChecklist.md`

**Be descriptive but concise:**
✅ `elps-alignment.md` (clear)
❌ `elps.md` (too short)
❌ `english-language-proficiency-standards-alignment-guide-for-texas.md` (too long)

**Subject-specific prefixes when needed:**
✅ `teks-math-alignment.md`
✅ `teks-ela-alignment.md`

### Content Quality Standards

**Accuracy:**
- [ ] Standards codes are correct
- [ ] Examples are grade-appropriate
- [ ] External links are valid
- [ ] Cross-references point to existing files

**Completeness:**
- [ ] All major concepts covered
- [ ] Examples for multiple grade levels
- [ ] Scaffolds for emergent bilinguals included
- [ ] Connections to related files documented

**Clarity:**
- [ ] No ambiguous language
- [ ] Technical terms defined
- [ ] Step-by-step procedures clear
- [ ] Visual aids (tables, lists) used effectively

**Utility:**
- [ ] Actionable guidance (not just theory)
- [ ] Templates/examples provided
- [ ] Common mistakes addressed
- [ ] Quick reference sections included

---

## Templates and Patterns

### Template: Standards Alignment File

**Location:** `[subject]/districts/[state]/[standard-system]-alignment.md`

**Structure:**
```markdown
# [Standard System] Alignment Guide
**[Full Name of Standards] for K-[12] [Subject]**
**Source:** [State Department of Education]
**Applies To:** K-[12] [Subject] ([State] only)

---

## Overview

[2-3 paragraphs about the standards]

**Core Principle:** [Key principle]

---

## [Standards] vs. [Other Standards Systems]

[Comparison table]

---

## Standard Format

### Structure:

**Format:** `[example code format]`

**Example:** `[real example]`

**Breakdown:**
- `[part 1]` = [meaning]
- `[part 2]` = [meaning]

---

## Sample Standards by Grade

### Grade 3 (Sample):

**[Code]:** [Full standard text]

### Grade 5 (Sample):

**[Code]:** [Full standard text]

### Grade 8 (Sample):

**[Code]:** [Full standard text]

---

## Alignment Documentation Requirements

[What to include in lessons]

---

## Example Alignment (Grade X):

**Standard:**
[Code and text]

**Lesson Alignment:**
[How lesson addresses standard]

**[Language Standard] Support:**
[Scaffolds by proficiency level]

**Assessment:**
[How to assess]

---

## Knowledge Reuse for [State] [Subject]

### What [State] [Subject] Reuses:

**Universal (100% reused):**
[List with checkmarks]

**[Subject]-Common (100% reused):**
[List with checkmarks]

**[State] District (reused across subjects):**
[List with checkmarks]

**[State] [Subject] Specific (new):**
[List with tool emoji]

**Knowledge Reuse Rate:** ~[XX]%

---

## Resources

[Related files and external links]

---

**Remember:** [Key takeaway]
```

---

### Template: Instructional Routine File

**Location:** Varies by subject
- Math: `/subjects/mathematics/common/mlr/[routine-name].md`
- ELA: `/subjects/ela/common/literacy-routines/[routine-name].md`
- Science: `/subjects/science/common/science-practices-framework.md`

**Structure:**
```markdown
# [Routine Name]
**[Routine Type] for [Purpose]**
**Scope:** Subject-Common (all [subject] programs, all districts)
**Audience:** Curriculum developers creating [type] lessons

---

## Overview

[Purpose and description]

**Core Principle:** [Key principle]

---

## Purpose and Benefits

### Why Use [Routine Name]?

**For All Students:**
[Benefits]

**For Emergent Bilinguals:**
[Benefits]

---

## [Routine Name] Structure

[Step-by-step protocol]

---

## Integration with Standards

[How routine supports standards]

---

## Scaffolding for Emergent Bilinguals

[Scaffolds by proficiency level]

---

## Examples by Grade Level

### Grade 3 Example:

[Complete example]

### Grade 5 Example:

[Complete example]

### Grade 8 Example:

[Complete example]

---

## Common Mistakes and Fixes

### ❌ Mistake 1: [Description]

**Problem:** [Explanation]

**Fix:** [Solution]

---

## Resources

[Related files]

---

**Remember:** [Key takeaway]
```

---

## Knowledge Base Quality Assurance

### Pre-Publication Checklist

Before adding any file to the knowledge base:

**Content Review:**
- [ ] Scope clearly stated (Universal/Subject-Common/District-Wide/Subject-District)
- [ ] Target audience identified
- [ ] Standards codes accurate (if applicable)
- [ ] Grade-level examples appropriate
- [ ] Scaffolds for emergent bilinguals included
- [ ] No bias or stereotypes (CEID compliant)

**Technical Review:**
- [ ] Markdown syntax correct
- [ ] File naming convention followed (kebab-case)
- [ ] File in correct directory (hierarchy level)
- [ ] All internal links use relative paths
- [ ] All internal links point to existing files
- [ ] External links are valid (test them)

**Cross-Reference Review:**
- [ ] Related files identified and linked
- [ ] This file added to related files' "See Also" sections
- [ ] No circular references or broken links
- [ ] Hierarchy relationships clear (what reuses what)

**Examples Review:**
- [ ] At least 2-3 examples per major concept
- [ ] Examples span multiple grade levels
- [ ] Both good (✅) and bad (❌) examples shown
- [ ] Examples use diverse names (CEID)

**Peer Review:**
- [ ] Subject matter expert reviewed content
- [ ] Instructional designer reviewed pedagogy
- [ ] Accessibility expert reviewed scaffolds
- [ ] Compliance expert reviewed standards (if applicable)

---

### Testing Knowledge Resolution

**After adding new files, test resolution:**

**Test 1: Does the file resolve correctly?**

```bash
# Check file exists in expected location
ls [path-to-new-file]

# Verify content is readable
head -20 [path-to-new-file]
```

**Test 2: Is it referenced in configs?**

```bash
# For subject-common file, check if subject's curricula can find it
grep -r "[filename]" /config/curriculum/

# Should appear in resolution order for relevant curricula
```

**Test 3: Are cross-references valid?**

```bash
# Extract all internal links from file
grep -o '\`/[^`]*\.md\`' [path-to-new-file]

# Verify each linked file exists
```

**Test 4: Does it integrate with existing files?**

- Open related files
- Confirm they reference the new file
- Ensure no duplicate content (DRY principle)

---

### Validation Scripts (Future Enhancement)

**Potential automation:**

```python
# Pseudocode for validation script

def validate_knowledge_file(file_path):
    # Check file naming convention
    assert is_kebab_case(file_path.name)

    # Check markdown syntax
    assert valid_markdown(file_path)

    # Check required sections exist
    assert has_overview_section(file_path)
    assert has_resources_section(file_path)

    # Check cross-references
    for link in extract_internal_links(file_path):
        assert file_exists(link)

    # Check scope declaration
    assert has_scope_declaration(file_path)

    return True
```

---

## Maintenance and Updates

### When to Update Files

**Update triggers:**
1. **Standards Change:** State adopts new standards (e.g., Texas TEKS revision)
2. **Compliance Update:** New state laws affect content restrictions
3. **Instructional Research:** New evidence-based practices emerge
4. **Technology Change:** New assessment platform, accessibility standards
5. **Error Discovery:** Inaccuracy or outdated information found

### Update Process

**Step 1: Identify Impact Scope**

Determine what files are affected:
- Single file (minor update)
- Multiple files in one hierarchy level
- Cross-hierarchy update (e.g., affects universal + multiple subjects)

**Step 2: Update Files**

Follow the same quality standards as new file creation:
- Update content
- Update "Last Updated" date if file has one
- Maintain consistent formatting
- Update examples if needed

**Step 3: Update Cross-References**

If file name changes or content significantly changes:
- Update all files that reference it
- Update curriculum configs if resolution paths change

**Step 4: Version Control**

```bash
git add [updated-files]
git commit -m "Update: [description of change]

- [File 1]: [What changed]
- [File 2]: [What changed]
- Reason: [Why update was needed]
"
git push origin master
```

**Step 5: Communicate Changes**

If update affects existing curricula:
- Document breaking changes
- Notify users/developers
- Provide migration guidance if needed

---

### Deprecation Process

**If a file becomes obsolete:**

**Step 1: Add Deprecation Notice**

At top of file:
```markdown
> **⚠️ DEPRECATED:** This file is deprecated as of [date]. Use [replacement-file.md] instead.
> **Reason:** [Why deprecated]
> **Migration:** [How to transition]
```

**Step 2: Update Cross-References**

Change references from deprecated file to replacement:
```markdown
- ~~Old File~~ (deprecated): `[old-path]`
- New File: `[new-path]`
```

**Step 3: Wait Period**

Keep deprecated file for 3-6 months to allow transition

**Step 4: Archive**

Move to `/reference/hmh-knowledge-v2/_deprecated/` folder

**Step 5: Remove**

After sufficient time, remove from repository

---

### Bulk Updates

**Example: Updating all files for new assessment platform**

```bash
# Find all files mentioning old platform
grep -r "Learnosity v2023" /reference/hmh-knowledge-v2/

# Update to new version
find /reference/hmh-knowledge-v2/ -name "*.md" -exec \
  sed -i '' 's/Learnosity v2023/Learnosity v2024/g' {} \;

# Commit
git add -u
git commit -m "Update: Learnosity platform version to v2024"
git push origin master
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: File Not Found During Resolution

**Symptom:** Curriculum config references a file that doesn't exist

**Diagnosis:**
```bash
# Check if file exists
ls [path-from-resolution-order]
```

**Solutions:**
- **Create the missing file** if it should exist
- **Update config** to remove non-existent path from resolution order
- **Check path typo** (common: subject vs. subjects, district vs. districts)

---

#### Issue 2: Circular References

**Symptom:** File A references File B, which references File A

**Diagnosis:**
```bash
# Check cross-references in both files
grep "\`/.*\.md\`" file-a.md
grep "\`/.*\.md\`" file-b.md
```

**Solution:**
- Restructure references to be hierarchical (general → specific only)
- Or use "See Also" sections instead of inline references

---

#### Issue 3: Duplicate Content

**Symptom:** Same information in multiple files (violates DRY)

**Diagnosis:**
- Review files at different hierarchy levels
- Check for overlapping content

**Solution:**
1. Identify the appropriate level for content
2. Keep content in ONE file at that level
3. Other files reference it, don't duplicate

**Example:**
- EB scaffolding strategies → Universal (not repeated in each state file)
- State files say "See: `/universal/frameworks/eb-scaffolding-guide.md`"

---

#### Issue 4: Broken Cross-References

**Symptom:** Links to files that don't exist or moved

**Diagnosis:**
```bash
# Extract all links from a file
grep -o '\`/[^`]*\.md\`' file.md

# Check if each exists
for file in $(grep -o '\`/[^`]*\.md\`' file.md | tr -d '`'); do
  if [ ! -f "$file" ]; then
    echo "Broken: $file"
  fi
done
```

**Solution:**
- Update links to correct paths
- Create missing files if they should exist
- Remove obsolete references

---

#### Issue 5: Inconsistent Naming

**Symptom:** Files in same category use different naming conventions

**Diagnosis:**
- List files in a directory
- Check for patterns

**Solution:**
- Rename files to follow conventions
- Update all cross-references
- Update curriculum configs if needed

```bash
# Rename file
git mv old-name.md new-name.md

# Update references (example with sed)
find . -name "*.md" -exec sed -i '' 's|old-name\.md|new-name.md|g' {} \;

# Commit
git commit -m "Rename: old-name.md → new-name.md for consistency"
```

---

#### Issue 6: Config Not Recognized

**Symptom:** Curriculum config doesn't work as expected

**Diagnosis:**
```bash
# Validate JSON syntax
cat [config-file].json | python -m json.tool

# Check required fields exist
jq '.id, .subject, .district' [config-file].json
```

**Solution:**
- Fix JSON syntax errors
- Ensure all required fields present
- Verify resolution paths exist

---

## Quick Reference

### File Hierarchy Cheat Sheet

```
Universal (15 files)
└─ Applied by: ALL curricula (100% reuse)
   └─ Examples: DOK, UDL, WCAG, Assessment, CEID

Subject-Common (16 files)
└─ Applied by: All states for that subject
   └─ Math: MLRs (12 files) → Used by TX, CA, FL, NY, IL, etc.
   └─ ELA: Literacy Routines (4 files) → Used by all states
   └─ Science: NGSS, Practices (2 files) → Used by 20+ states

District-Wide (9 files)
└─ Applied by: All subjects in that state/district
   └─ Texas: ELPS, IPACC (4 files) → TX Math, TX ELA, TX Science
   └─ California: ELD, Adoption (2 files) → CA Math, CA ELA, CA Science
   └─ Florida: ESOL, Compliance (3 files) → FL Math, FL ELA, FL Science

Subject-District (7 files)
└─ Applied by: One subject in one state
   └─ Texas Math: TEKS Math alignment
   └─ California Math: CCSS-M alignment
   └─ Florida Math: MAFS alignment
   └─ Texas ELA: TEKS ELA alignment

Program-Specific (1 file)
└─ Applied by: Specific program features
   └─ Into Math program-specific guidance
```

### Common Commands

```bash
# Create new state directory structure
mkdir -p /reference/hmh-knowledge-v2/districts/[state]/compliance
mkdir -p /reference/hmh-knowledge-v2/districts/[state]/language

# Create new subject directory structure
mkdir -p /reference/hmh-knowledge-v2/subjects/[subject]/common
mkdir -p /reference/hmh-knowledge-v2/subjects/[subject]/districts/[state]

# Find all files mentioning a topic
grep -r "[topic]" /reference/hmh-knowledge-v2/

# Count total files
find /reference/hmh-knowledge-v2 -name "*.md" | wc -l

# List files by hierarchy level
ls /reference/hmh-knowledge-v2/universal/**/*.md
ls /reference/hmh-knowledge-v2/subjects/*/common/*.md
ls /reference/hmh-knowledge-v2/districts/*/**/*.md

# Validate JSON config
cat /config/curriculum/[config].json | python -m json.tool

# Check file size
du -h [file-path]

# Check git status
git status

# Commit and push changes
git add .
git commit -m "[description]"
git push origin master
```

---

## Frequently Asked Questions

### Architecture and Design Questions

**Q1: When should I add a file to universal vs. subject-common?**

**A:** Use this decision tree:

```
Does it apply to ALL subjects (Math, ELA, Science, Social Studies, etc.)?
├─ YES → Does it apply to ALL states?
│   ├─ YES → Does it apply to ALL grade levels?
│   │   ├─ YES → Universal (/universal/)
│   │   └─ NO → Subject-Common (needs grade-specific versions)
│   └─ NO → District-Wide (/districts/[state]/)
└─ NO → Subject-Common (/subjects/[subject]/common/)
```

**Examples:**
- DOK Framework → Universal (all subjects, all states, all grades)
- MLRs → Subject-Common (math only, but all states)
- ELPS → District-Wide (all subjects in Texas only)
- TEKS Math → Subject-District (math in Texas only)

---

**Q2: What if content is 90% universal but has 10% state variation?**

**A:** Two approaches:

**Approach 1: Universal with State Notes (Preferred)**
- Put main content in universal file
- Add state-specific sections: "Texas-Specific Guidance," "California-Specific Guidance"
- Example: Assessment item types are mostly universal, with minor state variations

**Approach 2: Universal + State Override**
- Universal file has default guidance
- State file overrides specific sections
- Resolution order ensures state file is checked first
- Use sparingly (adds complexity)

**Rule of Thumb:** If >85% universal, use Approach 1.

---

**Q3: How do I handle contradictory requirements between states?**

**A:** Document both clearly:

```markdown
## State-Specific Variations

### Texas Requirement:
[TX-specific requirement]
**Source:** SBOE Quality Rubric Criterion X

### California Requirement:
[CA-specific requirement (may contradict TX)]
**Source:** California Adoption Criteria Section Y

### Implementation Guidance:
For TX content: [specific guidance]
For CA content: [specific guidance]
For multi-state content: [compromise approach or separate versions]
```

**Escalate** if requirements are incompatible and no compromise exists.

---

### File Creation Questions

**Q4: How detailed should examples be in KB files?**

**A:** Include at least:
- **Minimum:** 1 example per major concept
- **Better:** 2-3 examples at different grade levels (e.g., Grade 3, 5, 8)
- **Best:** Examples + non-examples (✅ Good / ❌ Bad)

**Example Depth:**
- Show the complete implementation, not just the concept
- Include scaffolds for emergent bilinguals in examples
- Demonstrate how to integrate with other KB guidance

**Length:** Examples should be 1/4 to 1/3 of file length.

---

**Q5: Should I create one large file or multiple smaller files?**

**A:** Follow the single responsibility principle:

**Create Multiple Files When:**
- Topic is complex with distinct subtopics (e.g., 8 separate MLR files, not 1 giant MLR file)
- Different audiences need different parts
- Easier to maintain smaller, focused files

**Create One File When:**
- Content is tightly interconnected
- Splitting would create confusion
- File is still <30KB

**Current Pattern:**
- Universal frameworks: Individual files (dok-framework.md, udl-principles-guide.md)
- MLRs: Individual files per routine (mlr1-stronger-clearer.md, mlr2-collect-display.md)
- Assessment: Individual files per topic (item-types-reference.md, scoring-rubrics-guide.md)

---

**Q6: How do I name files consistently?**

**A:** Follow these conventions:

**Format:** `topic-descriptor.md` (kebab-case)

**Good Examples:**
- ✅ `dok-framework.md` (clear, concise)
- ✅ `teks-math-alignment.md` (includes subject)
- ✅ `mlr1-stronger-clearer.md` (includes number + descriptor)

**Bad Examples:**
- ❌ `DOK_Framework.md` (not kebab-case)
- ❌ `framework.md` (too vague)
- ❌ `teks-mathematics-state-standards-comprehensive-alignment-guide.md` (too long)

**Patterns:**
- Standards: `[standard-system]-[subject]-alignment.md`
- Routines: `[routine-id]-[short-name].md`
- Frameworks: `[framework-name]-[type].md` (e.g., udl-principles-guide.md)

---

### Knowledge Reuse Questions

**Q7: How do I calculate knowledge reuse percentage?**

**A:** Use this formula:

```
Total Files Available = Universal + Subject-Common + District-Wide + Subject-District + Program-Specific

New Files Created = Subject-District + District-Wide (if new state)

Reused Files = Universal + Subject-Common + (District-Wide if existing state)

Reuse % = (Reused Files / Total Files Available) × 100
```

**Example: Florida Math**
- Universal: 15 files (reused)
- Math-Common: 12 files (reused)
- Florida District: 3 files (reused from existing FL)
- Florida Math: 1 file (NEW)
- **Total: 31 files, Reuse: 30/31 = 97%**

---

**Q8: What's considered "good" knowledge reuse?**

**A:** Targets by state type:

- **CCSS/NGSS State (Type A):** 90-95% reuse
  - Example: New York adds 2-3 files, reuses 28-30

- **State-Specific Standards (Type B):** 85-90% reuse
  - Example: Virginia adds 5-6 files, reuses 25-28

- **First Subject in New State:** 80-90% reuse
  - Building district-wide infrastructure

- **Additional Subject in Existing State:** 90-95% reuse
  - Reuses district-wide files already created

**Red Flag:** <80% reuse suggests over-customization or missing opportunities for abstraction.

---

**Q9: What if two states both use CCSS but implement differently?**

**A:** Use reference files at subject-district level:

**File Structure:**
- `/subjects/mathematics/common/ccss-m-alignment.md` (full CCSS-M content - core file)
- `/subjects/mathematics/districts/california/ccss-m-notes.md` (CA-specific notes, references core)
- `/subjects/mathematics/districts/new-york/ccss-m-notes.md` (NY-specific notes, references core)

**NY Notes File:**
```markdown
# CCSS-M Alignment for New York

**Full Alignment:** See `/subjects/mathematics/common/ccss-m-alignment.md`

## New York-Specific Implementation

### NY State Assessment Alignment
[NY-specific assessment notes]

### NY Emphasis Areas
[Where NY emphasizes differently than other CCSS states]

### Vertical Alignment with NY Regents
[How CCSS prepares for Regents exams]
```

**Result:** Core CCSS content written once, state variations documented separately.

---

### Quality and Maintenance Questions

**Q10: How often should KB files be updated?**

**A:** Update triggers:

**Immediate (Within 1 Week):**
- Standards change (e.g., state adopts new standards)
- Compliance requirement changes (new state law)
- Critical error discovered (wrong standard codes, broken links)

**Quarterly Review:**
- Instructional research updates (new evidence-based practices)
- Technology changes (new assessment platforms)
- Cross-reference validation (ensure no broken links)

**Annual Review:**
- Comprehensive review of all universal files
- Update examples to current best practices
- Remove deprecated content

**Don't Update:**
- Just for rewording (unless improving clarity significantly)
- Personal style preferences
- Minor formatting changes

**Version in commit message** if substantive change.

---

**Q11: What if I find duplicate content across files?**

**A:** Eliminate duplication (DRY principle):

**Steps:**
1. **Identify which level should own the content:**
   - Universal? Subject-Common? District-Wide?
2. **Keep content in ONE file at appropriate level**
3. **Replace duplicates with references:**

```markdown
## [Topic]

**See:** `/path/to/authoritative/file.md`

### [State/Subject]-Specific Notes:
[Only the unique content for this state/subject]
```

**Example:**
- EB scaffolding strategies → Universal file
- Texas ELA file says: "For EB scaffolding strategies, see `/universal/frameworks/eb-scaffolding-guide.md`. Texas-specific: ELPS standards require..."

**Result:** Content maintained in one place, referenced everywhere else.

---

**Q12: How do I deprecate an old file?**

**A:** Follow deprecation process (Section 10):

1. **Add deprecation notice** at top of file
2. **Update cross-references** to point to new file
3. **Wait 3-6 months** (transition period)
4. **Move to `/_deprecated/`** folder
5. **After 6-12 months:** Remove entirely

**Never:** Delete immediately (breaks existing curricula)

---

### Collaboration Questions

**Q13: How do I work with Subject Matter Experts (SMEs)?**

**A:** SMEs provide content expertise, you provide KB architecture expertise:

**Your Role:**
- Explain hierarchy and resolution order
- Guide SME on what level to target (universal vs. subject-common)
- Ensure content follows templates and patterns
- Handle cross-references and technical structure

**SME Role:**
- Provide accurate content (standards, instructional practices)
- Review examples for grade-appropriateness
- Validate pedagogical soundness

**Workflow:**
1. Meet with SME to understand content need
2. Determine appropriate KB level
3. Provide template to SME
4. SME drafts content
5. You review for structure, cross-references, hierarchy fit
6. SME reviews final version
7. You commit to KB

**Communication:** Use shared docs for drafting, clear role boundaries.

---

**Q14: How do I handle requests that don't fit the hierarchy?**

**A:** Challenge the request, propose alternatives:

**Example Request:** "Add Texas-specific UDL guidance"

**Your Response:**
"UDL principles are universal by design. Let me understand what's Texas-specific:
- Is it compliance requirement? → Add to Texas compliance file
- Is it ELPS integration with UDL? → Add section to ELPS file referencing UDL
- Is it Texas assessment format? → Add to Texas assessment guidance

UDL file itself should remain universal."

**Principle:** Maintain hierarchy integrity. State-specific content goes in state files, which reference universal content.

**Escalate** if stakeholder insists on breaking hierarchy after explanation.

---

**Q15: What if an author says "the KB guidance doesn't work for my lesson"?**

**A:** Investigate:

**Possible Causes:**
1. **Author misunderstanding:** Explain KB guidance more clearly
2. **Edge case:** KB guidance works 95% of time, this is 5% exception
3. **KB guidance is wrong/outdated:** Fix the KB file
4. **Lesson is non-standard:** Coach author to align with KB

**Process:**
1. Ask author for specific example
2. Review KB file yourself
3. Consult with SME or instructional designer
4. Either: Update KB file OR explain to author why guidance applies

**Don't:** Let KB guidance be ignored without investigation.

---

### Technical Questions

**Q16: Can I use relative vs. absolute paths for cross-references?**

**A:** **Always use absolute paths from repository root:**

✅ **Correct:**
```markdown
See: `/universal/frameworks/dok-framework.md`
```

❌ **Incorrect:**
```markdown
See: `../../universal/frameworks/dok-framework.md`
```

**Reason:** Absolute paths work regardless of file location, making refactoring easier.

---

**Q17: What if I need to reorganize the hierarchy?**

**A:** Major reorganization requires careful planning:

**Steps:**
1. **Document current structure** (file inventory, cross-references)
2. **Propose new structure** with rationale
3. **Map migration:** Old path → New path for each file
4. **Update all cross-references** (use find/replace scripts)
5. **Update curriculum configs** (resolution order paths)
6. **Test resolution** for all curricula
7. **Communicate change** to users
8. **Commit in atomic transaction** (all changes together)

**Avoid:** Incremental moves that break references temporarily.

**Pro Tip:** Use git mv to preserve history: `git mv old-path new-path`

---

**Q18: How do I handle binary files (images, PDFs) in KB?**

**A:** Minimize binary files in KB:

**Preferred:** Markdown text descriptions
**When Binary Needed:**
- Diagrams explaining complex concepts
- Examples of student work
- Assessment item exemplars

**Storage:**
- Small images (<100KB): In KB repository
- Large files: External storage, link in KB file

**Format:**
- Images: PNG or SVG (accessible)
- Documents: Link to external, don't embed PDFs

**Maintenance:** Binary files are harder to version control and diff.

---

### Scaling Questions

**Q19: How many files is too many?**

**A:** No hard limit, but watch for:

**Warning Signs:**
- Difficulty navigating (too many files in one directory)
- Duplicate content (files overlap)
- Orphaned files (nothing references them)

**Current Scale:**
- 50 files for 3 states × 3 subjects = manageable
- 300 files for national coverage = still manageable with good organization
- 1000+ files = may need subdirectory restructuring

**Organization Strategies:**
- Subdirectories by category (e.g., `/mlr/`, `/literacy-routines/`)
- Clear naming conventions
- Index files (e.g., `mlr-overview.md` lists all 8 MLRs)

---

**Q20: What if knowledge base becomes too large to maintain?**

**A:** Strategies for scale:

**1. Automation:**
- Scripts to validate links
- Scripts to check file naming
- Automated cross-reference generation

**2. Team Structure:**
- Subject leads (own math, ELA, science KB files)
- State leads (own TX, CA, FL KB files)
- Universal lead (own universal files)

**3. Documentation:**
- Clear ownership (README per directory)
- Change logs
- Deprecation tracking

**4. Modularization:**
- Consider splitting very large subjects
- Example: Secondary math (9-12) as separate from elementary (K-8)

**Current Status:** 50 files, single team member can maintain. Plan for scale at 200+ files.

---

### Career Development Questions

**Q21: How do I grow from junior to senior KB engineer?**

**A:** Progression path:

**Junior Engineer (0-6 months):**
- Add states (CCSS states, Type A)
- Update existing files (minor fixes, cross-references)
- Follow templates closely

**Mid-Level Engineer (6-18 months):**
- Add states with unique standards (Type B)
- Add new subjects (create subject-common files)
- Propose template improvements
- Review junior engineer work

**Senior Engineer (18+ months):**
- Design new KB patterns
- Make architectural decisions
- Handle complex cross-state requirements
- Mentor junior engineers
- Optimize for scale

**Skills to Develop:**
- Deep knowledge of standards frameworks (CCSS, NGSS, TEKS, etc.)
- Instructional design expertise
- System design and architecture
- Technical writing
- Stakeholder management

---

**Q22: What skills from KB engineering transfer to other roles?**

**A:** Highly transferable skills:

**Information Architecture:**
- Hierarchical system design
- Taxonomy and classification
- DRY principles

**Technical Writing:**
- Clear documentation
- Template design
- Style consistency

**System Thinking:**
- Abstraction and reuse
- Modularity
- Scalability

**Domain Expertise:**
- Educational standards (TEKS, CCSS, NGSS)
- Instructional design
- Compliance requirements

**Career Paths:**
- Curriculum Architect
- Instructional Designer
- Content Operations Manager
- Learning Engineer
- Product Manager (EdTech)

---

**Q23: How do I stay current with educational standards changes?**

**A:** Monitoring strategies:

**Official Sources:**
- State Department of Education websites
- Sign up for standards update notifications
- Follow CCSSO, NGSS, state education Twitter/news

**Professional Organizations:**
- NCTM (math), NCTE (ELA), NSTA (science)
- State-specific education associations

**Internal Communication:**
- Work with curriculum leads who attend conferences
- Connect with SMEs who track standards
- Review RFPs (Request for Proposals) from districts

**Quarterly Review:**
- Check for standards revisions (most states review every 5-10 years)
- Update KB files proactively, not reactively

**Document Sources:** In KB files, cite official source documents with dates.

---

**Q24: What's the most common mistake new KB engineers make?**

**A:** Top 3 mistakes:

**1. Over-Customization (Most Common)**
- Adding state-specific versions when universal would work
- Creating duplicate content instead of referencing
- Result: Maintenance nightmare

**Prevention:** Always ask "Can this be universal?" before state-specific.

**2. Inadequate Testing**
- Not validating cross-references
- Not testing resolution order
- Committing broken links
- Result: Users hit dead ends

**Prevention:** Use testing checklist (Section 9) every time.

**3. Poor Commit Messages**
- "Update file"
- "Fix"
- Result: No history of why changes made

**Prevention:** Descriptive commits: "Add NY state support: 3 files, 94% reuse"

---

**Q25: How do I handle urgent requests during planned work?**

**A:** Prioritization framework:

**P0 - Drop Everything (Rare):**
- KB file has critical error breaking production
- State compliance deadline tomorrow
- Security issue

**P1 - Same Day:**
- New curriculum launch blocked on KB file
- Author can't proceed without KB addition

**P2 - This Week:**
- New state/subject request with timeline
- Non-critical bug fixes

**P3 - Next Sprint:**
- Enhancements and optimizations
- Nice-to-have additions

**Communication:**
- If urgent request conflicts with planned work: escalate to supervisor
- Explain trade-offs (doing X means delaying Y)
- Get explicit prioritization decision
- Document priority decisions

**Don't:** Silently drop planned work without communication.

---

## Complete Worked Examples

This section provides full end-to-end walkthroughs of common knowledge base engineering tasks.

### Example 1: Adding New York State (CCSS/NGSS State - Type A)

**Task:** Add support for New York, which uses CCSS (math/ELA) and NGSS (science).

**Estimated Time:** 2-3 hours
**Expected Reuse:** 90-95% (2-3 new files)

#### Step 1: Research New York Requirements (30 minutes)

**1.1 Identify Standards**

```bash
# Research standards used
# Math: CCSS-M (same as California)
# ELA: CCSS-ELA (same as California)
# Science: NGSS (same as California)
# Language: NYS Bilingual Common Core Initiative
```

**1.2 Identify State-Specific Requirements**

New York requires:
- P-12 Common Core Learning Standards (same content as CCSS)
- NYS Bilingual Common Core Initiative (ELL support)
- Culturally Responsive-Sustaining Education Framework (CR-SE)
- NYS Commissioner's Regulations (adoption criteria)

**1.3 Calculate Expected Knowledge Reuse**

```
Universal files: 15 (all reused)
Math Common: 12 (all reused)
ELA Common: 5 (all reused)
Science Common: 2 (all reused)
Subject-District Math: 1 (reuse CA CCSS-M file)
Subject-District ELA: 1 (reuse CA CCSS-ELA file)
Subject-District Science: 1 (reuse CA NGSS file)
District-Wide: 3 NEW files needed
Program-Specific: 0 (none yet)

Total available: 15 + 12 + 5 + 2 = 34 common files
New files needed: 3
Reuse rate: 34/(34+3) = 91.9%
```

#### Step 2: Create District-Wide Files (1 hour)

**2.1 Create Language Support File**

```bash
cd /reference/hmh-knowledge-v2/districts/
mkdir -p newyork/language
nano newyork/language/nysbe-alignment.md
```

**File:** `/reference/hmh-knowledge-v2/districts/newyork/language/nysbe-alignment.md`

```markdown
# NYS Bilingual Education (NYSBE) Alignment Guide

## Overview

New York requires support for English Language Learners under the NYS Bilingual Common Core Initiative (NYSBE), aligned to the Home Language Arts (HLA) and English as a New Language (ENL) framework.

## Proficiency Levels

NYSBE uses 5 levels:
- **Entering** (Level 1) - Minimal English proficiency
- **Emerging** (Level 2) - Limited English proficiency
- **Transitioning** (Level 3) - Developing English proficiency
- **Expanding** (Level 4) - Good English proficiency
- **Commanding** (Level 5) - Fluent/near-native English proficiency

## Integration with Content

[...detailed scaffolding guidance by level...]

## Cross-Reference

For general emergent bilingual scaffolding strategies, see:
- `/universal/frameworks/eb-scaffolding-guide.md` (universal strategies)
- `/universal/vocabulary/sentence-frames-guide.md` (sentence stems)
```

**2.2 Create Adoption Criteria File**

```bash
nano newyork/compliance/adoption-criteria.md
```

**File:** `/reference/hmh-knowledge-v2/districts/newyork/compliance/adoption-criteria.md`

```markdown
# New York State Adoption Criteria

## Commissioner's Regulations

NYS Commissioner's Regulations Part 100 requires:

### Content Requirements
- Alignment to NYS P-12 Common Core Learning Standards
- Culturally Responsive-Sustaining Education (CR-SE) Framework
- Representation of diverse perspectives and cultures

### Technical Requirements
- Accessibility (WCAG 2.1 AA minimum)
- Digital formats compatible with NYS LMS platforms
- Assessment alignment to NYS testing frameworks

[...detailed requirements...]

## Cross-References

- `/universal/compliance/wcag-2.1-aa-guide.md` (accessibility)
- `/universal/dei/ceid-guidelines.md` (cultural responsiveness)
```

**2.3 Create Compliance Checklist**

```bash
nano newyork/compliance/nys-compliance-checklist.md
```

**File:** `/reference/hmh-knowledge-v2/districts/newyork/compliance/nys-compliance-checklist.md`

```markdown
# NYS Compliance Checklist

Use this checklist before submitting content for New York review.

## Standards Alignment
- [ ] Content explicitly aligned to P-12 Common Core Learning Standards
- [ ] Standards codes visible in lesson materials
- [ ] Assessment alignment documented

## Language Support
- [ ] NYSBE scaffolds provided for all 5 proficiency levels
- [ ] Home Language Arts (HLA) connections where appropriate
- [ ] ENL support strategies integrated

## Cultural Responsiveness
- [ ] CR-SE Framework applied (see adoption criteria)
- [ ] Diverse perspectives represented
- [ ] Bias-free language verified

[...complete checklist...]
```

#### Step 3: Create Curriculum Configuration (15 minutes)

```bash
cd /config/curriculum/
nano hmh-math-ny.json
```

**File:** `/config/curriculum/hmh-math-ny.json`

```json
{
  "id": "hmh-math-ny",
  "name": "HMH Into Math - New York",
  "version": "1.0.0",
  "subject": "mathematics",
  "district": "newyork",
  "grades": ["K", "1", "2", "3", "4", "5", "6", "7", "8"],
  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge-v2/subjects/mathematics/districts/newyork/into-math/",
      "/reference/hmh-knowledge-v2/subjects/mathematics/districts/newyork/",
      "/reference/hmh-knowledge-v2/subjects/mathematics/districts/california/",
      "/reference/hmh-knowledge-v2/subjects/mathematics/common/",
      "/reference/hmh-knowledge-v2/districts/newyork/",
      "/reference/hmh-knowledge-v2/publishers/hmh/",
      "/reference/hmh-knowledge-v2/universal/"
    ]
  },
  "standards": {
    "content": "P-12 CCLS (Common Core Learning Standards)",
    "language": "NYSBE (NYS Bilingual Education)",
    "accessibility": "WCAG 2.1 AA",
    "cultural": "CR-SE Framework"
  },
  "state_code": "NY",
  "adoption_cycle": "2024-2030"
}
```

**Note:** Resolution order includes `/districts/california/` for CCSS-M standards (file reuse).

#### Step 4: Test Knowledge Resolution (30 minutes)

**4.1 Create Test Script**

```bash
cd /scripts/
nano test-ny-resolution.sh
```

```bash
#!/bin/bash
# Test New York knowledge resolution

echo "Testing NY Math Grade 5 Fractions Lesson..."
echo ""

CONFIG="config/curriculum/hmh-math-ny.json"

# Extract resolution order
RESOLUTION_ORDER=$(jq -r '.knowledge_resolution.order[]' $CONFIG)

echo "Resolution Order:"
echo "$RESOLUTION_ORDER"
echo ""

# Test files that should resolve
TEST_FILES=(
  "mlr/mlr1-lighter-heavier.md"
  "teks-math-alignment.md"  # Should NOT resolve (wrong state)
  "ccss-math-alignment.md"  # Should resolve (from CA subject-district)
  "nysbe-alignment.md"      # Should resolve (NY district-wide)
  "udl-principles-guide.md" # Should resolve (universal)
)

echo "Testing file resolution:"
for FILE in "${TEST_FILES[@]}"; do
  echo -n "  $FILE: "
  FOUND=false
  for DIR in $RESOLUTION_ORDER; do
    if [ -f "$DIR/$FILE" ] || [ -f "$DIR"*"/$FILE" ]; then
      echo "✓ Found in $DIR"
      FOUND=true
      break
    fi
  done
  if [ "$FOUND" = false ]; then
    echo "✗ NOT FOUND"
  fi
done
```

```bash
chmod +x test-ny-resolution.sh
./test-ny-resolution.sh
```

**Expected Output:**

```
Testing NY Math Grade 5 Fractions Lesson...

Resolution Order:
/reference/hmh-knowledge-v2/subjects/mathematics/districts/newyork/into-math/
/reference/hmh-knowledge-v2/subjects/mathematics/districts/newyork/
/reference/hmh-knowledge-v2/subjects/mathematics/districts/california/
/reference/hmh-knowledge-v2/subjects/mathematics/common/
/reference/hmh-knowledge-v2/districts/newyork/
/reference/hmh-knowledge-v2/publishers/hmh/
/reference/hmh-knowledge-v2/universal/

Testing file resolution:
  mlr/mlr1-lighter-heavier.md: ✓ Found in /subjects/mathematics/common/
  teks-math-alignment.md: ✗ NOT FOUND (expected - wrong state)
  ccss-math-alignment.md: ✓ Found in /subjects/mathematics/districts/california/
  nysbe-alignment.md: ✓ Found in /districts/newyork/
  udl-principles-guide.md: ✓ Found in /universal/
```

**4.2 Validate Reuse Percentage**

```bash
# Count all available knowledge files for NY Math
find /reference/hmh-knowledge-v2/subjects/mathematics/common -name "*.md" | wc -l  # 12
find /reference/hmh-knowledge-v2/universal -name "*.md" | wc -l  # 15
find /reference/hmh-knowledge-v2/districts/newyork -name "*.md" | wc -l  # 3 (new)
find /reference/hmh-knowledge-v2/subjects/mathematics/districts/california -name "ccss*.md" | wc -l  # 1 (reused)

# Total: 12 + 15 + 3 + 1 = 31 files
# New: 3 files
# Reuse: 28 files
# Reuse %: 28/31 = 90.3% ✓
```

#### Step 5: Document and Commit (30 minutes)

**5.1 Update Knowledge Base Documentation**

```bash
nano /reference/hmh-knowledge-v2/README.md
```

Add NY to coverage list:
```markdown
**States Covered:** Texas (TX), California (CA), Florida (FL), New York (NY)
```

**5.2 Update System Specification**

```bash
nano /specs/content-repository-specification.md
```

Update metrics section to reflect NY addition.

**5.3 Commit Changes**

```bash
cd /Users/colossus/development/content

# Add all NY files
git add reference/hmh-knowledge-v2/districts/newyork/
git add config/curriculum/hmh-math-ny.json
git add scripts/test-ny-resolution.sh

# Commit with detailed message
git commit -m "Add New York state support (CCSS/NGSS - Type A)

Added NY state with 90.3% knowledge reuse:
- 3 new district-wide files (language, adoption, compliance)
- 1 curriculum config (hmh-math-ny.json)
- Reuses 28 existing files (CA CCSS-M standards, all math common, all universal)
- Tested with resolution script

New files:
- /districts/newyork/language/nysbe-alignment.md
- /districts/newyork/compliance/adoption-criteria.md
- /districts/newyork/compliance/nys-compliance-checklist.md
- /config/curriculum/hmh-math-ny.json

Knowledge reuse: 28 reused / 31 total = 90.3%

Tested: Resolution order validates correctly, all expected files resolve."

git push origin master
```

#### Step 6: Verify with Real Content (30 minutes)

**6.1 Create Test Lesson**

Ask a content author to create a NY Grade 5 math lesson using the new config:

```bash
# Author uses hmh-math-ny.json config
# System should correctly resolve:
# - MLR guidance from /subjects/mathematics/common/
# - CCSS-M standards from /subjects/mathematics/districts/california/
# - NYSBE scaffolding from /districts/newyork/language/
# - UDL principles from /universal/
```

**6.2 Review Output**

Check that lesson includes:
- ✓ CCSS-M standards (e.g., "5.NF.A.1")
- ✓ MLR strategies (e.g., "MLR2: Collect and Display")
- ✓ NYSBE scaffolds for all 5 levels
- ✓ UDL multiple means of representation
- ✓ CR-SE Framework elements
- ✓ NY-specific compliance requirements

#### Summary: NY State Addition

**Time Spent:** 2.5 hours
**Files Created:** 4 (3 knowledge + 1 config)
**Knowledge Reuse:** 90.3%
**Testing:** Automated + manual validation
**Result:** NY state fully supported with minimal duplication

---

### Example 2: Adding Social Studies Subject

**Task:** Add Social Studies as a new subject with support for existing 3 states (TX, CA, FL).

**Estimated Time:** 6-8 hours
**Expected Files:** 13-15 files (8-10 subject-common, 1-2 per state)

#### Step 1: Research Social Studies Requirements (1 hour)

**1.1 Identify Standards Frameworks**

```
National: C3 Framework (College, Career, and Civic Life)
Texas: TEKS Social Studies
California: CA History-Social Science Standards
Florida: NGSSS Social Studies
```

**1.2 Identify Common Instructional Practices**

Common to all social studies:
- Primary source analysis
- Historical thinking skills (sourcing, contextualization, corroboration)
- Geographic reasoning
- Civic engagement practices
- Economic reasoning
- Document-Based Questions (DBQs)

**1.3 Plan File Structure**

```
/reference/hmh-knowledge-v2/subjects/social-studies/
├── common/                          # All social studies programs
│   ├── c3-framework-guide.md        # National C3 Framework
│   ├── historical-thinking-skills.md
│   ├── primary-source-analysis.md
│   ├── dbq-guidelines.md
│   ├── geographic-reasoning.md
│   ├── civic-engagement-practices.md
│   ├── economic-reasoning-framework.md
│   ├── inquiry-design-model.md      # C3 IDM
│   ├── vocabulary-guidelines.md
│   └── assessment-frameworks.md
└── districts/
    ├── texas/
    │   └── teks-social-studies-alignment.md
    ├── california/
    │   └── hss-standards-alignment.md
    └── florida/
        └── ngsss-social-studies-alignment.md
```

**Expected File Count:** 10 common + 3 state = 13 files

#### Step 2: Create Subject-Common Files (3 hours)

**2.1 Create C3 Framework Guide**

```bash
mkdir -p /reference/hmh-knowledge-v2/subjects/social-studies/common
cd /reference/hmh-knowledge-v2/subjects/social-studies/common
nano c3-framework-guide.md
```

**File:** `/subjects/social-studies/common/c3-framework-guide.md`

```markdown
# C3 Framework (College, Career, and Civic Life) Guide

## Overview

The C3 Framework organizes social studies around four dimensions:

**Dimension 1: Developing Questions and Planning Inquiries**
- Formulate compelling and supporting questions
- Identify disciplinary concepts and ideas
- Develop claims and use evidence

**Dimension 2: Applying Disciplinary Concepts**
- **Civics:** Civic and political institutions, participation, processes
- **Economics:** Economic decision-making, markets, national economy
- **Geography:** Human-environment interaction, location, movement
- **History:** Change/continuity, perspectives, causation

**Dimension 3: Evaluating Sources and Using Evidence**
- Gather and evaluate sources
- Develop claims and use evidence
- Communicate and critique conclusions

**Dimension 4: Communicating Conclusions and Taking Informed Action**
- Communicate conclusions
- Critique arguments
- Take informed action

## Inquiry Design Model (IDM)

[...detailed IDM structure with templates...]

## Integration with Lessons

Every social studies lesson should:
1. Begin with a compelling question (Dimension 1)
2. Apply disciplinary concepts (Dimension 2)
3. Analyze sources and evidence (Dimension 3)
4. Communicate findings (Dimension 4)

## Cross-References

- `/subjects/social-studies/common/inquiry-design-model.md` (detailed IDM)
- `/subjects/social-studies/common/primary-source-analysis.md` (Dimension 3)
- `/universal/frameworks/dok-framework.md` (depth of knowledge)
```

**2.2 Create Historical Thinking Skills**

```bash
nano historical-thinking-skills.md
```

**File:** `/subjects/social-studies/common/historical-thinking-skills.md`

```markdown
# Historical Thinking Skills Framework

## The Big Six Historical Thinking Concepts

### 1. Historical Significance
**What:** Identifying events, people, developments that had lasting importance
**Teaching:** Compare short-term vs. long-term effects

### 2. Evidence and Interpretation
**What:** Analyzing primary and secondary sources
**Teaching:** Sourcing, contextualization, corroboration (see Primary Source Analysis)

### 3. Continuity and Change
**What:** Recognizing patterns and transformations over time
**Teaching:** Timeline analysis, periodization

### 4. Cause and Consequence
**What:** Identifying multiple causes and intended/unintended consequences
**Teaching:** Cause-effect chains, historical contingency

### 5. Historical Perspective
**What:** Understanding beliefs, values, motivations of historical actors
**Teaching:** "Historical empathy" vs. presentism

### 6. Ethical Dimension
**What:** Judging actions within their historical context
**Teaching:** Informed moral judgments with evidence

## Application by Grade Band

**Elementary (K-5):**
- Focus on sequencing, change over time
- Simple cause-effect relationships
- Identifying perspectives

**Middle School (6-8):**
- Multiple causes and consequences
- Comparing different perspectives
- Contextualizing primary sources

**High School (9-12):**
- Complex causation, unintended consequences
- Historiography (how interpretations change)
- Sophisticated source analysis

[...detailed examples for each skill...]

## Cross-References

- `/subjects/social-studies/common/primary-source-analysis.md`
- `/subjects/social-studies/common/dbq-guidelines.md`
- `/universal/frameworks/dok-framework.md` (DOK 2-4 applications)
```

**2.3 Create Primary Source Analysis Guide**

```bash
nano primary-source-analysis.md
```

**File:** `/subjects/social-studies/common/primary-source-analysis.md`

```markdown
# Primary Source Analysis Framework

## The Three Heuristics

### 1. Sourcing
**What:** Who created this source? When? Why?
**Questions to Ask:**
- Who is the author/creator?
- When was it created?
- What is the author's perspective?
- What was the purpose/audience?

### 2. Contextualization
**What:** Understanding the historical context
**Questions to Ask:**
- What was happening at this time?
- What came before this?
- How did context influence this source?

### 3. Corroboration
**What:** Comparing sources to establish facts
**Questions to Ask:**
- Do other sources agree or disagree?
- What accounts for differences?
- Which sources are most reliable?

## Scaffolding by Proficiency Level

[...ELPS/ELD/ESOL scaffolds for source analysis...]

## Lesson Integration

**Activity Template:**
1. Preview source (5 min) - observe, wonder, infer
2. Source (10 min) - answer sourcing questions
3. Contextualize (10 min) - connect to prior knowledge
4. Close read (15 min) - analyze content
5. Corroborate (10 min) - compare with other sources
6. Synthesize (10 min) - answer inquiry question

[...detailed templates...]

## Cross-References

- `/subjects/social-studies/common/historical-thinking-skills.md`
- `/subjects/social-studies/common/dbq-guidelines.md`
- `/universal/vocabulary/sentence-frames-guide.md` (analysis sentence frames)
```

**2.4 Create Remaining Common Files**

Continue creating:
- `dbq-guidelines.md` - Document-Based Question structure
- `geographic-reasoning.md` - Five themes of geography
- `civic-engagement-practices.md` - C3 civic practices
- `economic-reasoning-framework.md` - Economic concepts
- `inquiry-design-model.md` - Complete IDM blueprint
- `vocabulary-guidelines.md` - Social studies academic language
- `assessment-frameworks.md` - Assessment types for social studies

*[For brevity, not showing all 10 files, but same level of detail]*

#### Step 3: Create Subject-District Files (2 hours)

**3.1 Create Texas TEKS Social Studies Alignment**

```bash
mkdir -p /reference/hmh-knowledge-v2/subjects/social-studies/districts/texas
cd /reference/hmh-knowledge-v2/subjects/social-studies/districts/texas
nano teks-social-studies-alignment.md
```

**File:** `/subjects/social-studies/districts/texas/teks-social-studies-alignment.md`

```markdown
# TEKS Social Studies Alignment Guide

## Overview

Texas Essential Knowledge and Skills (TEKS) for Social Studies emphasizes:
- Texas history and heritage
- Citizenship responsibilities
- Primary source analysis
- Geographic literacy

## Grade-Level Standards

### Kindergarten: Self, Home, Family, Classroom
**Standards:**
- K.1 History - Chronology, family history
- K.2 History - Historical figures (family, community)
- K.3 Geography - Location of self, classroom, school
- K.4 Economics - Basic wants/needs
- K.5 Government - Purpose of rules
- K.6 Citizenship - Characteristics of good citizenship
- K.7 Culture - Family customs, traditions
- K.8 Science, Technology, Society

[...continues through grade 12...]

### Grade 8: Texas History
**Standards:**
- 8.1 History - Texas from Spanish colonial through present
- 8.2 History - Native Texan groups
- 8.3 History - Spanish colonial/Mexican period
- 8.4 History - Revolution and Republic
- 8.5 History - Statehood and Civil War
[...]

## Cross-References

- `/subjects/social-studies/common/c3-framework-guide.md` (national framework)
- `/districts/texas/compliance/sboe-quality-rubric.md` (state compliance)
- `/districts/texas/language/elps-alignment.md` (language support)
```

**3.2 Create California HSS Standards Alignment**

```bash
mkdir -p /reference/hmh-knowledge-v2/subjects/social-studies/districts/california
cd /reference/hmh-knowledge-v2/subjects/social-studies/districts/california
nano hss-standards-alignment.md
```

*[Similar structure for CA History-Social Science Standards]*

**3.3 Create Florida NGSSS Social Studies Alignment**

```bash
mkdir -p /reference/hmh-knowledge-v2/subjects/social-studies/districts/florida
cd /reference/hmh-knowledge-v2/subjects/social-studies/districts/florida
nano ngsss-social-studies-alignment.md
```

*[Similar structure for FL NGSSS Social Studies]*

#### Step 4: Create Curriculum Configurations (1 hour)

**4.1 Create Texas Social Studies Config**

```bash
cd /config/curriculum/
nano hmh-social-studies-tx.json
```

**File:** `/config/curriculum/hmh-social-studies-tx.json`

```json
{
  "id": "hmh-social-studies-tx",
  "name": "HMH Social Studies - Texas",
  "version": "1.0.0",
  "subject": "social-studies",
  "district": "texas",
  "grades": ["K", "1", "2", "3", "4", "5", "6", "7", "8"],
  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge-v2/subjects/social-studies/districts/texas/",
      "/reference/hmh-knowledge-v2/subjects/social-studies/common/",
      "/reference/hmh-knowledge-v2/districts/texas/",
      "/reference/hmh-knowledge-v2/publishers/hmh/",
      "/reference/hmh-knowledge-v2/universal/"
    ]
  },
  "standards": {
    "content": "TEKS Social Studies",
    "language": "ELPS",
    "accessibility": "WCAG 2.1 AA",
    "cultural": "CEID Framework"
  },
  "state_code": "TX",
  "adoption_cycle": "2024-2030"
}
```

**4.2 Create CA and FL Configs**

*[Similar configs for hmh-social-studies-ca.json and hmh-social-studies-fl.json]*

#### Step 5: Test and Validate (1.5 hours)

**5.1 Test File Resolution**

```bash
cd /scripts/
nano test-social-studies.sh
```

```bash
#!/bin/bash
# Test Social Studies knowledge resolution for all 3 states

STATES=("tx" "ca" "fl")
for STATE in "${STATES[@]}"; do
  echo "Testing Social Studies - $STATE..."
  CONFIG="config/curriculum/hmh-social-studies-$STATE.json"

  # Test expected files resolve
  # - State standards file (subject-district)
  # - C3 Framework (subject-common)
  # - Primary source analysis (subject-common)
  # - State language file (district-wide)
  # - UDL (universal)

  # [Resolution testing code]
done
```

**5.2 Calculate Knowledge Reuse**

```
Subject-Common: 10 files (reused across all 3 states)
Subject-District: 3 files (1 per state, new)
District-Wide: 0 new (reuse existing TX/CA/FL files)
Universal: 15 files (reused)

For Texas Social Studies:
Total: 10 + 1 + 5 (TX district) + 15 = 31 files
New: 10 (common) + 1 (TX standards) = 11 files
Reuse from existing: 5 (TX district) + 15 (universal) = 20 files
Reuse %: 20/31 = 64.5%

But across all 3 states:
Total unique files: 10 (common) + 3 (state standards) = 13 new
Total files used: 31 per state × 3 = 93 total file usages
New: 13, Reused from pre-existing: 20 × 3 = 60
Reuse from pre-existing: 60/93 = 64.5%
Reuse including subject-common: (60 + 30)/93 = 96.8%

Key insight: First subject appears to be 64.5% reuse,
but 10 common files are reused 3 times (across states),
demonstrating 96.8% efficiency for the subject as a whole.
```

#### Step 6: Document and Commit (30 minutes)

```bash
git add reference/hmh-knowledge-v2/subjects/social-studies/
git add config/curriculum/hmh-social-studies-*.json
git add scripts/test-social-studies.sh

git commit -m "Add Social Studies subject with 3-state support

Added Social Studies with strong knowledge reuse:
- 10 subject-common files (C3, historical thinking, primary sources, DBQ, inquiry, etc.)
- 3 subject-district files (TEKS, HSS, NGSSS alignments for TX/CA/FL)
- 3 curriculum configs
- Reuses all existing district-wide and universal files

New files:
Subject-Common (10):
- c3-framework-guide.md
- historical-thinking-skills.md
- primary-source-analysis.md
- dbq-guidelines.md
- geographic-reasoning.md
- civic-engagement-practices.md
- economic-reasoning-framework.md
- inquiry-design-model.md
- vocabulary-guidelines.md
- assessment-frameworks.md

Subject-District (3):
- TX: teks-social-studies-alignment.md
- CA: hss-standards-alignment.md
- FL: ngsss-social-studies-alignment.md

Configs (3):
- hmh-social-studies-tx.json
- hmh-social-studies-ca.json
- hmh-social-studies-fl.json

Knowledge reuse: 64.5% from pre-existing files, 96.8% when including subject-common files shared across all 3 states.

Tested: All 3 state configs resolve correctly."

git push origin master
```

#### Summary: Social Studies Addition

**Time Spent:** 7 hours
**Files Created:** 16 (10 common + 3 state + 3 configs)
**Knowledge Reuse:** 96.8% across all 3 states (64.5% pre-existing + 32.3% new common files reused 3×)
**Impact:** Social Studies now available for TX, CA, FL with minimal duplication
**Extensibility:** Adding 4th state (e.g., NY) would only require 1 new file + 1 config (98% reuse)

---

## Key Takeaways from Worked Examples

**From Example 1 (Adding NY State):**
- Type A states (CCSS/NGSS) achieve 90-95% reuse
- Only 2-3 new files needed (district-wide level)
- Can reuse subject-district files from other CCSS/NGSS states
- Total time: 2-3 hours

**From Example 2 (Adding Social Studies):**
- New subjects require 8-10 subject-common files
- First state in new subject: ~65% reuse from existing
- Each additional state in that subject: ~97% reuse
- Total time for subject + 3 states: 6-8 hours

**Universal Lessons:**
1. **Plan for reuse from the start** - Think about what's common before creating files
2. **Test resolution thoroughly** - Automated scripts catch configuration errors early
3. **Document reuse metrics** - Shows value of hierarchical architecture
4. **Cross-reference extensively** - Helps users navigate knowledge base
5. **Commit with detailed messages** - Future engineers understand your decisions

---

## Comprehensive Testing and Validation Procedures

Testing the knowledge base ensures correct resolution, catches configuration errors, and validates content quality before release.

### Testing Strategy Overview

**4 Testing Levels:**
1. **Unit Testing** - Individual file validation (structure, links, cross-references)
2. **Resolution Testing** - Knowledge resolution order validation
3. **Integration Testing** - End-to-end content generation
4. **Regression Testing** - Verify changes don't break existing functionality

### Level 1: Unit Testing Individual Files

**Goal:** Validate individual knowledge base files for structure, links, and content quality.

#### 1.1 File Structure Validation

**Script:** `scripts/validate-file-structure.sh`

```bash
#!/bin/bash
# Validate knowledge base file structure

FILE=$1

if [ -z "$FILE" ]; then
  echo "Usage: $0 <path-to-md-file>"
  exit 1
fi

echo "Validating: $FILE"
echo ""

# Check 1: File has proper markdown headers
echo "Check 1: Markdown structure"
if grep -q "^# " "$FILE"; then
  echo "✓ Has H1 header"
else
  echo "✗ Missing H1 header"
fi

if grep -q "^## " "$FILE"; then
  echo "✓ Has H2 sections"
else
  echo "✗ Missing H2 sections"
fi

# Check 2: Has Cross-References section
echo ""
echo "Check 2: Cross-references"
if grep -q "## Cross-References" "$FILE"; then
  echo "✓ Has Cross-References section"

  # Extract and validate cross-reference paths
  REFS=$(sed -n '/## Cross-References/,/^##/p' "$FILE" | grep -o '/[a-z-]*/[a-z-]*/.*\.md')
  for REF in $REFS; do
    if [ -f "/reference/hmh-knowledge-v2$REF" ]; then
      echo "  ✓ $REF exists"
    else
      echo "  ✗ $REF MISSING"
    fi
  done
else
  echo "✗ Missing Cross-References section"
fi

# Check 3: Has Overview section
echo ""
echo "Check 3: Content structure"
if grep -q "## Overview" "$FILE"; then
  echo "✓ Has Overview section"
else
  echo "⚠ No Overview section (optional but recommended)"
fi

# Check 4: Word count (minimum threshold)
echo ""
echo "Check 4: Content depth"
WORDS=$(wc -w < "$FILE")
if [ "$WORDS" -gt 500 ]; then
  echo "✓ Sufficient content depth ($WORDS words)"
elif [ "$WORDS" -gt 200 ]; then
  echo "⚠ Minimal content ($WORDS words, consider expanding)"
else
  echo "✗ Insufficient content ($WORDS words, needs expansion)"
fi

echo ""
echo "Validation complete."
```

**Usage:**
```bash
chmod +x scripts/validate-file-structure.sh
./scripts/validate-file-structure.sh /reference/hmh-knowledge-v2/universal/frameworks/udl-principles-guide.md
```

#### 1.2 Cross-Reference Link Validation

**Script:** `scripts/validate-cross-refs.sh`

```bash
#!/bin/bash
# Validate all cross-references in knowledge base

KB_ROOT="/reference/hmh-knowledge-v2"
ERROR_COUNT=0

echo "Validating cross-references in knowledge base..."
echo ""

# Find all markdown files
for FILE in $(find "$KB_ROOT" -name "*.md"); do
  # Extract cross-reference paths (lines with markdown links to .md files)
  REFS=$(grep -o '\[.*\](.*\.md)' "$FILE" | sed 's/.*(\(.*\))/\1/')

  if [ -n "$REFS" ]; then
    echo "Checking: $FILE"
    for REF in $REFS; do
      # Handle relative paths
      if [[ "$REF" == /* ]]; then
        FULL_PATH="$REF"
      else
        FILE_DIR=$(dirname "$FILE")
        FULL_PATH="$FILE_DIR/$REF"
      fi

      if [ -f "$FULL_PATH" ]; then
        echo "  ✓ $REF"
      else
        echo "  ✗ $REF BROKEN"
        ((ERROR_COUNT++))
      fi
    done
  fi
done

echo ""
if [ $ERROR_COUNT -eq 0 ]; then
  echo "✓ All cross-references valid"
  exit 0
else
  echo "✗ Found $ERROR_COUNT broken cross-references"
  exit 1
fi
```

**Usage:**
```bash
chmod +x scripts/validate-cross-refs.sh
./scripts/validate-cross-refs.sh
```

#### 1.3 Content Quality Checklist

For each new knowledge base file, manually verify:

- [ ] **Clear purpose** - Title and overview explain what this file provides
- [ ] **Actionable guidance** - Concrete examples, not just concepts
- [ ] **Grade-appropriate** (if applicable) - Examples match target grade band
- [ ] **Cross-referenced** - Links to related files at all relevant levels
- [ ] **DRY compliance** - No duplication of content from other files
- [ ] **Consistent formatting** - Follows KB style guide (headers, lists, code blocks)
- [ ] **Accessibility** - Tables have headers, images would have alt text
- [ ] **Complete examples** - Code/templates are runnable, not pseudocode

### Level 2: Resolution Testing

**Goal:** Verify knowledge resolution order works correctly for curriculum configs.

#### 2.1 Automated Resolution Testing Script

**Script:** `scripts/test-resolution.sh`

```bash
#!/bin/bash
# Test knowledge resolution for a curriculum config

CONFIG=$1

if [ -z "$CONFIG" ]; then
  echo "Usage: $0 <config-file.json>"
  echo "Example: $0 config/curriculum/hmh-math-tx.json"
  exit 1
fi

if [ ! -f "$CONFIG" ]; then
  echo "Error: Config file not found: $CONFIG"
  exit 1
fi

echo "Testing resolution for: $CONFIG"
echo ""

# Extract resolution order
RESOLUTION_ORDER=$(jq -r '.knowledge_resolution.order[]' "$CONFIG")

if [ -z "$RESOLUTION_ORDER" ]; then
  echo "Error: No resolution order found in config"
  exit 1
fi

echo "Resolution Order:"
echo "$RESOLUTION_ORDER"
echo ""

# Count files at each level
echo "Files available at each level:"
for DIR in $RESOLUTION_ORDER; do
  if [ -d "$DIR" ]; then
    COUNT=$(find "$DIR" -name "*.md" 2>/dev/null | wc -l)
    echo "  $DIR: $COUNT files"
  else
    echo "  $DIR: [MISSING DIRECTORY]"
  fi
done

echo ""

# Test sample file resolution
echo "Testing sample file resolution:"

# Define test files based on subject
SUBJECT=$(jq -r '.subject' "$CONFIG")
case "$SUBJECT" in
  mathematics)
    TEST_FILES=(
      "mlr/mlr1-lighter-heavier.md"
      "udl-principles-guide.md"
      "dok-framework.md"
    )
    ;;
  ela)
    TEST_FILES=(
      "close-reading-routine.md"
      "udl-principles-guide.md"
      "sentence-frames-guide.md"
    )
    ;;
  science)
    TEST_FILES=(
      "ngss-alignment.md"
      "udl-principles-guide.md"
      "science-practices-framework.md"
    )
    ;;
  *)
    echo "Unknown subject: $SUBJECT"
    exit 1
    ;;
esac

# Test each file
for TEST_FILE in "${TEST_FILES[@]}"; do
  echo -n "  $TEST_FILE: "
  FOUND=false

  for DIR in $RESOLUTION_ORDER; do
    # Search for file in directory and subdirectories
    MATCH=$(find "$DIR" -name "$TEST_FILE" 2>/dev/null | head -1)
    if [ -n "$MATCH" ]; then
      RESOLVED_DIR=$(dirname "$MATCH")
      echo "✓ Resolved in $RESOLVED_DIR"
      FOUND=true
      break
    fi
  done

  if [ "$FOUND" = false ]; then
    echo "✗ NOT FOUND (expected failure if file doesn't exist)"
  fi
done

echo ""
echo "Resolution test complete."
```

**Usage:**
```bash
chmod +x scripts/test-resolution.sh

# Test all configs
for config in config/curriculum/*.json; do
  ./scripts/test-resolution.sh "$config"
  echo "---"
done
```

#### 2.2 Manual Resolution Testing

For new curriculum configs, manually verify resolution:

**Test Matrix:**

| File Type | Expected Resolution Level | Test File | Expected to Resolve? |
|-----------|---------------------------|-----------|---------------------|
| Universal | `/universal/` | `udl-principles-guide.md` | ✓ Yes |
| Subject-Common | `/subjects/[subject]/common/` | Math: MLR files | ✓ Yes |
| Subject-District | `/subjects/[subject]/districts/[state]/` | State standards | ✓ Yes |
| District-Wide | `/districts/[state]/` | State language file | ✓ Yes |
| Wrong State | N/A | Different state's standards | ✗ No (should not resolve) |

**Example Test for TX Math:**

```bash
# Should resolve:
✓ MLR guidance from /subjects/mathematics/common/
✓ TEKS standards from /subjects/mathematics/districts/texas/
✓ ELPS guidance from /districts/texas/language/
✓ UDL from /universal/frameworks/

# Should NOT resolve:
✗ CCSS-M from /subjects/mathematics/districts/california/ (wrong state)
✗ CA ELD from /districts/california/ (wrong state)
```

### Level 3: Integration Testing

**Goal:** Test end-to-end content generation using knowledge base with real content authors.

#### 3.1 Integration Test Plan

**Test Scenario:** Create a complete lesson using a curriculum config.

**Steps:**
1. Select test config (e.g., `hmh-math-tx.json`)
2. Select test objective (e.g., "Grade 5: Add fractions with unlike denominators")
3. Have content author create lesson using KB guidance
4. Validate output includes guidance from all resolution levels

**Validation Checklist:**

- [ ] **Standards alignment** - Uses correct state standards from subject-district level
- [ ] **Instructional routines** - Applies subject-common routines (e.g., MLRs for math)
- [ ] **Language support** - Includes district-wide language scaffolds (ELPS/ELD/ESOL)
- [ ] **UDL principles** - Applies universal UDL guidance
- [ ] **Assessment guidance** - Uses universal assessment frameworks
- [ ] **State compliance** - Meets district-wide compliance requirements
- [ ] **No duplication** - Doesn't repeat guidance from KB (author referenced, didn't copy)

#### 3.2 Test Case Template

**File:** `tests/integration/test-case-template.md`

```markdown
# Integration Test Case: [Subject] [State] [Grade] [Topic]

## Test Metadata
- **Date:** [YYYY-MM-DD]
- **Config:** [hmh-subject-state.json]
- **Tester:** [Name]
- **Status:** [Pass/Fail/Blocked]

## Test Objective
Create a [lesson/assessment/activity] for [Grade] [Subject] on [Topic] using [Config].

## Expected Knowledge Base Usage

| KB Level | Expected Files Used | Guidance Applied |
|----------|---------------------|------------------|
| Universal | udl-principles-guide.md | Multiple means of representation |
| Subject-Common | mlr/mlr2-collect-display.md | Collect and Display routine |
| Subject-District | teks-math-alignment.md | 5.NF.A.1 standard |
| District-Wide | elps-alignment.md | ELPS scaffolds for Beginning/Intermediate |

## Test Procedure
1. Provide author with config and topic
2. Author reviews KB files (18 files for typical lesson)
3. Author creates lesson applying KB guidance
4. Reviewer validates output against checklist

## Validation Results

### Standards Alignment
- [ ] State standards explicitly referenced (e.g., "5.NF.A.1")
- [ ] DOK level appropriate
- [ ] Learning objective measurable

### Instructional Quality
- [ ] Subject-specific routines applied (e.g., MLR2)
- [ ] UDL principles evident (3+ means of representation)
- [ ] Formative assessment integrated

### Language Support
- [ ] State language framework applied (ELPS/ELD/ESOL)
- [ ] Sentence frames provided for emergent bilinguals
- [ ] Vocabulary support included

### State Compliance
- [ ] State-specific requirements met
- [ ] Compliance checklist followed

## Issues Found
[List any issues, broken links, missing guidance]

## Recommendations
[Suggestions for KB improvements based on this test]

## Outcome
- **Pass Criteria:** All checklist items complete, no critical issues
- **Result:** [PASS/FAIL]
- **Tester Signature:** [Name, Date]
```

#### 3.3 Smoke Testing New Additions

After adding a new state/subject:

1. **Create 3 test lessons** (one per grade band: elementary, middle, high)
2. **Validate resolution** - All expected files resolve correctly
3. **Check reuse metric** - Actual reuse matches projected (±5%)
4. **Author feedback** - Ask author: "Was any guidance missing? Duplicated?"

### Level 4: Regression Testing

**Goal:** Ensure changes to KB don't break existing content or configs.

#### 4.1 Regression Test Suite

**After Any KB Change, Run:**

1. **Link validation** - All cross-references still valid
2. **Config validation** - All curriculum configs still resolve correctly
3. **Sample content test** - Previously created content still meets quality standards

**Script:** `scripts/regression-test.sh`

```bash
#!/bin/bash
# Regression test suite

echo "Running KB Regression Tests..."
echo ""

# Test 1: Validate all cross-references
echo "Test 1: Cross-Reference Validation"
./scripts/validate-cross-refs.sh
TEST1_RESULT=$?

# Test 2: Test all curriculum configs
echo ""
echo "Test 2: Resolution Testing"
TEST2_RESULT=0
for CONFIG in config/curriculum/*.json; do
  ./scripts/test-resolution.sh "$CONFIG" > /dev/null
  if [ $? -ne 0 ]; then
    echo "✗ Config failed: $CONFIG"
    TEST2_RESULT=1
  else
    echo "✓ Config passed: $CONFIG"
  fi
done

# Test 3: File structure validation for all KB files
echo ""
echo "Test 3: File Structure Validation"
TEST3_RESULT=0
for FILE in $(find /reference/hmh-knowledge-v2 -name "*.md"); do
  ./scripts/validate-file-structure.sh "$FILE" > /dev/null
  if [ $? -ne 0 ]; then
    echo "✗ Structure issue: $FILE"
    TEST3_RESULT=1
  fi
done

if [ $TEST3_RESULT -eq 0 ]; then
  echo "✓ All files have valid structure"
fi

# Summary
echo ""
echo "========================================"
echo "Regression Test Summary"
echo "========================================"
if [ $TEST1_RESULT -eq 0 ] && [ $TEST2_RESULT -eq 0 ] && [ $TEST3_RESULT -eq 0 ]; then
  echo "✓ ALL TESTS PASSED"
  exit 0
else
  echo "✗ SOME TESTS FAILED"
  [ $TEST1_RESULT -ne 0 ] && echo "  - Cross-reference validation failed"
  [ $TEST2_RESULT -ne 0 ] && echo "  - Resolution testing failed"
  [ $TEST3_RESULT -ne 0 ] && echo "  - File structure validation failed"
  exit 1
fi
```

**Usage:**
```bash
chmod +x scripts/regression-test.sh

# Run before committing KB changes
./scripts/regression-test.sh

# Only commit if all tests pass
if [ $? -eq 0 ]; then
  git commit -m "Your change message"
else
  echo "Fix issues before committing"
fi
```

#### 4.2 Impact Analysis Checklist

Before committing changes to knowledge base files, assess impact:

**Changed Universal File?**
- Affects: **ALL** curricula, **ALL** states, **ALL** subjects
- Test: All curriculum configs, sample content from multiple states/subjects
- Risk: **HIGH** - Broad impact

**Changed Subject-Common File?**
- Affects: **ALL** states in that subject
- Test: All configs for that subject (e.g., all math configs)
- Risk: **MEDIUM** - Subject-wide impact

**Changed Subject-District File?**
- Affects: **ONE** state in that subject
- Test: Configs for that state + subject
- Risk: **LOW** - Narrow impact

**Changed District-Wide File?**
- Affects: **ALL** subjects in that state
- Test: All configs for that state
- Risk: **MEDIUM** - State-wide impact

**Changed Program-Specific File?**
- Affects: **ONE** program only
- Test: That program's config only
- Risk: **VERY LOW** - Minimal impact

### Testing Workflow Summary

**For New State Addition:**
```bash
# 1. Unit test new files
for file in districts/newstate/*.md; do
  ./scripts/validate-file-structure.sh "$file"
done

# 2. Test new config resolution
./scripts/test-resolution.sh config/curriculum/hmh-math-newstate.json

# 3. Integration test (create test lesson)
# [Manual: Author creates lesson, validate output]

# 4. Regression test
./scripts/regression-test.sh

# 5. Commit if all pass
git add districts/newstate/
git commit -m "Add New State support"
```

**For New Subject Addition:**
```bash
# 1. Unit test all subject-common files
for file in subjects/new-subject/common/*.md; do
  ./scripts/validate-file-structure.sh "$file"
done

# 2. Test all new state configs
for config in config/curriculum/hmh-new-subject-*.json; do
  ./scripts/test-resolution.sh "$config"
done

# 3. Integration test for each state
# [Manual: Create test lessons for TX, CA, FL]

# 4. Regression test
./scripts/regression-test.sh

# 5. Commit if all pass
git add subjects/new-subject/
git add config/curriculum/hmh-new-subject-*.json
git commit -m "Add New Subject with 3-state support"
```

### Continuous Integration (CI) Setup

**For GitHub Actions:**

**File:** `.github/workflows/kb-validation.yml`

```yaml
name: Knowledge Base Validation

on:
  pull_request:
    paths:
      - 'reference/hmh-knowledge-v2/**'
      - 'config/curriculum/**'
  push:
    branches: [ master ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Validate cross-references
        run: |
          chmod +x scripts/validate-cross-refs.sh
          ./scripts/validate-cross-refs.sh

      - name: Test all curriculum configs
        run: |
          chmod +x scripts/test-resolution.sh
          for config in config/curriculum/*.json; do
            ./scripts/test-resolution.sh "$config"
          done

      - name: Validate file structures
        run: |
          chmod +x scripts/validate-file-structure.sh
          EXIT_CODE=0
          for file in $(find reference/hmh-knowledge-v2 -name "*.md"); do
            ./scripts/validate-file-structure.sh "$file" || EXIT_CODE=1
          done
          exit $EXIT_CODE
```

**Benefits:**
- Automatic validation on every PR
- Catches broken links before merge
- Ensures config resolution works
- Prevents regressions

### Testing Best Practices

1. **Test Early, Test Often** - Run unit tests as you create files, not just at the end
2. **Automate What You Can** - Scripts catch errors faster than manual review
3. **Manual Integration Tests Are Critical** - Real author usage reveals gaps automated tests miss
4. **Document Test Results** - Keep test cases for future regression testing
5. **Fix Forward** - When tests reveal issues, fix them before adding more content
6. **Version Test Scripts** - Keep test scripts in git alongside KB files

### Common Testing Issues and Fixes

**Issue 1: Cross-Reference Link Broken**
- **Symptom:** `validate-cross-refs.sh` reports broken link
- **Cause:** File moved, renamed, or typo in cross-reference
- **Fix:** Update cross-reference path or restore missing file

**Issue 2: Resolution Returns Wrong File**
- **Symptom:** More specific file expected, but general file resolved
- **Cause:** Resolution order incorrect in config, or more specific file doesn't exist
- **Fix:** Check config resolution order, verify file exists at expected level

**Issue 3: Duplicate Guidance Applied**
- **Symptom:** Author applies guidance from multiple levels that say same thing
- **Cause:** DRY violation - content duplicated across hierarchy
- **Fix:** Consolidate to most general applicable level, reference from specific levels

**Issue 4: Missing Guidance**
- **Symptom:** Author can't find guidance for state-specific requirement
- **Cause:** Gap in KB coverage
- **Fix:** Add new file at appropriate level (likely district-wide or subject-district)

**Issue 5: Config Doesn't Resolve Expected Files**
- **Symptom:** Resolution test shows files missing
- **Cause:** Config resolution order missing a level, or file path incorrect
- **Fix:** Update config resolution order, verify paths

---

## Advanced Patterns and Architecture

This section covers sophisticated patterns for handling complex knowledge base scenarios, edge cases, and architectural decisions.

### Pattern 1: Handling Conflicting State Requirements

**Scenario:** Two states have similar but incompatible requirements for the same concept.

**Example:** Texas requires "ELPS" language support, California requires "ELD," but the underlying concepts differ:
- ELPS: 4 proficiency levels (Beginning, Intermediate, Advanced, Advanced High)
- ELD: 3 levels (Emerging, Expanding, Bridging)

**Anti-Pattern (Don't Do This):**
```
/universal/language/ell-support.md   ← Tries to merge ELPS and ELD (confusing!)
```

**Correct Pattern:**
```
/districts/texas/language/elps-alignment.md      ← ELPS-specific guidance
/districts/california/language/eld-alignment.md  ← ELD-specific guidance
/universal/frameworks/eb-scaffolding-guide.md    ← Universal scaffolding strategies (no state-specific frameworks)
```

**Cross-Reference Strategy:**
- Universal file provides general scaffolding types (sentence frames, vocabulary support, visual aids)
- District files map state frameworks to universal strategies
- Example in `elps-alignment.md`:
  ```markdown
  ## ELPS Beginning Level
  Use universal scaffolding strategies (see `/universal/frameworks/eb-scaffolding-guide.md`):
  - Sentence frames (Level 1: Fill-in-the-blank)
  - Visual supports (images, graphic organizers)
  [...]
  ```

**Key Principle:** Keep state-specific frameworks at district level, universal strategies at universal level.

---

### Pattern 2: Multi-Version Support (Managing Standard Updates)

**Scenario:** Standards frameworks are updated (e.g., NGSS 2013 vs. NGSS 2020 updates), need to support both.

**Versioning Strategy:**

**Option A: Inline Versioning (Minor Differences)**
```markdown
# NGSS Alignment Guide

## Version Notes
- **NGSS 2013** - Original framework (most states)
- **NGSS 2020 Update** - Clarifications and additions (some states)

## Science and Engineering Practices

### Practice 1: Asking Questions (NGSS 2013 and 2020)
[Common guidance...]

### Practice 8A: Communicating Information (NGSS 2013)
[Original guidance...]

### Practice 8B: Obtaining, Evaluating, and Communicating Information (NGSS 2020)
[Updated guidance...]
```

**When to use:** Minor updates, 80%+ content shared, both versions in use.

**Option B: Separate Files (Major Differences)**
```
/subjects/science/common/ngss-2013-alignment.md
/subjects/science/common/ngss-2020-alignment.md
```

**When to use:** Major revisions, <80% content shared, clear adoption split.

**Curriculum Config Strategy:**
```json
{
  "standards": {
    "content": "NGSS 2020",
    "version": "2020"
  },
  "knowledge_resolution": {
    "order": [
      "/subjects/science/common/ngss-2020-alignment.md",
      "/subjects/science/common/",
      [...]
    ]
  }
}
```

**Deprecation Plan:**
1. Support both versions for 2-3 years
2. Add deprecation notice to old version
3. Track usage (which states use which version)
4. Archive old version when adoption drops below 10%

---

### Pattern 3: Cross-Subject Knowledge Sharing

**Scenario:** Some instructional practices apply across multiple subjects (e.g., "Think-Pair-Share" works in Math, ELA, Science, Social Studies).

**Anti-Pattern (Duplication):**
```
/subjects/mathematics/common/think-pair-share.md
/subjects/ela/common/think-pair-share.md
/subjects/science/common/think-pair-share.md
/subjects/social-studies/common/think-pair-share.md
```

**Correct Pattern (Universal with Subject Adaptations):**
```
/universal/instructional-practices/think-pair-share.md   ← Core strategy (all subjects)
/subjects/mathematics/common/think-pair-share-math.md    ← Math-specific examples ONLY
/subjects/social-studies/common/think-pair-share-ss.md  ← SS-specific examples ONLY
```

**Universal File Structure:**
```markdown
# Think-Pair-Share Instructional Practice

## Overview
Think-Pair-Share is a cooperative learning strategy applicable across all subjects.

## Core Steps (All Subjects)
1. **Think** - Individual reflection (1-2 min)
2. **Pair** - Partner discussion (2-3 min)
3. **Share** - Whole-class sharing (5-10 min)

## Universal Benefits
- Increases engagement
- Provides processing time
- Supports emergent bilinguals (practice before public sharing)

## Subject-Specific Adaptations
For subject-specific examples and prompts, see:
- Math: `/subjects/mathematics/common/think-pair-share-math.md`
- ELA: `/subjects/ela/common/think-pair-share-ela.md`
- Science: `/subjects/science/common/think-pair-share-science.md`
- Social Studies: `/subjects/social-studies/common/think-pair-share-ss.md`
```

**Subject-Specific File (Math):**
```markdown
# Think-Pair-Share for Mathematics

## Overview
See `/universal/instructional-practices/think-pair-share.md` for core strategy.

This file provides **math-specific prompts and examples only**.

## Math-Specific Prompts

### Elementary (K-5)
**Think:** "How could you solve 24 + 37?"
**Pair:** "Explain your strategy to your partner."
**Share:** [Partners share different strategies]

### Middle School (6-8)
**Think:** "What pattern do you notice in this sequence?"
**Pair:** "Do you and your partner see the same pattern?"
**Share:** [Compare multiple patterns]

[...more examples, NO repetition of core strategy...]
```

**Key Principle:** Universal file = core strategy, subject files = examples only.

---

### Pattern 4: Modular Knowledge Architecture

**Scenario:** Large knowledge files become unwieldy (>1000 lines). Need to break into smaller, composable modules.

**Before (Monolithic):**
```
/universal/assessment/assessment-guide.md   (2500 lines - too large!)
```

**After (Modular):**
```
/universal/assessment/
├── overview.md                    (200 lines - quick reference)
├── item-types-reference.md        (400 lines - MC, CR, performance tasks)
├── writing-mc-items.md            (300 lines - detailed MC guidance)
├── writing-cr-items.md            (350 lines - detailed CR guidance)
├── rubric-design.md               (400 lines - rubric frameworks)
├── answer-key-guidelines.md       (250 lines - answer key best practices)
├── blueprint-templates.md         (300 lines - assessment blueprints)
└── validation-checklist.md        (300 lines - quality checks)
```

**Navigation File (`overview.md`):**
```markdown
# Assessment Framework Overview

## Quick Navigation

- **Creating Assessments:** See `blueprint-templates.md`
- **Writing Items:**
  - Multiple Choice: `writing-mc-items.md`
  - Constructed Response: `writing-cr-items.md`
- **Creating Rubrics:** See `rubric-design.md`
- **Answer Keys:** See `answer-key-guidelines.md`
- **Quality Checks:** See `validation-checklist.md`

## Complete Item Type Reference
See `item-types-reference.md` for comprehensive catalog of:
- Multiple Choice (MC)
- Constructed Response (CR)
- Performance Tasks
- Technology-Enhanced Items (TEI)
[...]
```

**Benefits:**
- Faster loading (authors open only what they need)
- Easier maintenance (edit one module without affecting others)
- Better git diffs (changes isolated to specific modules)
- Clearer responsibilities (one engineer owns writing-mc-items.md, another owns rubrics)

**When to Modularize:**
- File exceeds 1000 lines
- File covers 3+ distinct topics
- Different authors/experts contribute to different sections
- Frequent updates to some sections but not others

---

### Pattern 5: Progressive Enhancement Strategy

**Scenario:** Building knowledge base incrementally while supporting production content creation.

**Phased Approach:**

**Phase 1: Minimum Viable KB (Week 1)**
```
Goal: Support one state, one subject, one grade band
Coverage: 15 files (universal basics only)
Quality: Good enough for pilot content
```

**Phase 2: Horizontal Expansion (Week 2-3)**
```
Goal: Add more states for same subject
Coverage: 35 files (add district-wide + subject-district for 2-3 states)
Quality: Production-ready for one subject
```

**Phase 3: Vertical Expansion (Week 4-6)**
```
Goal: Add more subjects for existing states
Coverage: 70 files (add subject-common for 2-3 new subjects)
Quality: Production-ready for multiple subjects
```

**Phase 4: Deep Enhancement (Month 2-3)**
```
Goal: Add advanced guidance, examples, edge cases
Coverage: 100+ files (specialized files, program-specific customizations)
Quality: Comprehensive, mature KB
```

**Content Author Communication During Phases:**
- **Phase 1:** "Pilot only - expect gaps, provide feedback"
- **Phase 2:** "Production-ready for math, other subjects coming soon"
- **Phase 3:** "All subjects available, advanced guidance being added"
- **Phase 4:** "Mature KB, focus on refinement based on usage"

---

### Pattern 6: Handling Publisher-Specific Customizations

**Scenario:** HMH "Into Math" has specific features not in other HMH math programs.

**Hierarchy Decision:**

**Option A: Program-Specific Level** (Recommended)
```
/subjects/mathematics/districts/texas/into-math/into-math-features.md
```

**Use when:** Feature unique to that program, not applicable to other programs.

**Option B: Publisher Level**
```
/publishers/hmh/hmh-branding-guidelines.md
```

**Use when:** Guidance applies to ALL HMH programs (branding, legal, corporate style).

**Example: "Into Math" Student Workspace Feature**

**File:** `/subjects/mathematics/districts/texas/into-math/student-workspace-integration.md`

```markdown
# Into Math Student Workspace Integration

## Overview
Into Math includes a digital Student Workspace not found in other programs.

## Lesson Integration
When authoring Into Math lessons:
- [ ] Reference Student Workspace activities (e.g., "Complete Practice Set 3.2 in Student Workspace")
- [ ] Include screenshots showing where students find activities
- [ ] Provide teacher guidance on reviewing student work in Workspace

## Cross-References
- For general digital tool integration: `/universal/technology/digital-tool-integration.md`
- For Into Math program overview: `/subjects/mathematics/districts/texas/into-math/program-overview.md`
```

**Key Decision:** Put it at the most specific level where it applies. If only Into Math uses it, it's program-specific.

---

### Pattern 7: Managing Knowledge Base at Scale

**Scenario:** Knowledge base grows to 300+ files across 50 states and 10 subjects.

**Scalability Strategies:**

**1. Directory Naming Conventions**
```
/subjects/
  /mathematics/
    /common/
      /number-sense/           ← Group related files
      /operations/
      /geometry/
      /data-statistics/
  /ela/
    /common/
      /reading/
      /writing/
      /speaking-listening/
```

**2. File Naming with Prefixes**
```
mlr-1-stronger-and-clearer.md
mlr-2-collect-and-display.md
mlr-3-clarify-critique-correct.md
[...ensures alphabetical sort is logical...]
```

**3. Master Index Files**
```
/reference/hmh-knowledge-v2/INDEX.md   ← Complete file catalog
/subjects/mathematics/common/INDEX.md  ← Math-specific catalog
```

**4. Tagging/Metadata System**

Add YAML frontmatter to each file:
```markdown
---
title: "MLR1: Stronger and Clearer Each Time"
category: "Instructional Routine"
subject: "mathematics"
grade_levels: [K, 1, 2, 3, 4, 5, 6, 7, 8]
frameworks: ["UDL", "ELPS", "ELD", "ESOL"]
related_files:
  - "/universal/vocabulary/sentence-frames-guide.md"
  - "/subjects/mathematics/common/mlr/mlr2-collect-display.md"
last_updated: "2025-11-01"
version: "2.0"
---

# MLR1: Stronger and Clearer Each Time
[Content...]
```

**5. Search and Discovery Tools**

**Script:** `scripts/kb-search.sh`
```bash
#!/bin/bash
# Search knowledge base by keyword

KEYWORD=$1
KB_ROOT="/reference/hmh-knowledge-v2"

if [ -z "$KEYWORD" ]; then
  echo "Usage: $0 <keyword>"
  exit 1
fi

echo "Searching for: $KEYWORD"
echo ""

# Search in filenames
echo "=== Matching Files ==="
find "$KB_ROOT" -name "*$KEYWORD*.md"

# Search in content
echo ""
echo "=== Content Matches ==="
grep -rl "$KEYWORD" "$KB_ROOT" --include="*.md" | head -10
```

---

### Pattern 8: Optimization for Performance

**Scenario:** Content authors report slow file loading or difficulty finding files.

**Performance Optimizations:**

**1. File Size Limits**
- Maximum 1000 lines per file
- Break larger files into modules (see Pattern 4)

**2. Cross-Reference Optimization**
- Limit to 10-15 cross-references per file
- Too many links = cognitive overload

**3. Caching Strategy (for web-based KB)**
```
- Universal files: Cache aggressively (change rarely)
- Subject-common: Cache moderately (change occasionally)
- Subject-district: Cache lightly (updated for standards changes)
- Program-specific: No cache (change frequently)
```

**4. Lazy Loading**
```
Overview file loads immediately (200 lines)
Detailed modules load on-demand (click to expand)
```

**5. Search Indexing**
Pre-build search index for fast keyword search:
```bash
# Build search index
scripts/build-search-index.sh

# Creates /reference/hmh-knowledge-v2/search-index.json
# Fast client-side search without loading all files
```

---

### Pattern 9: Knowledge Base Versioning and Rollback

**Scenario:** Need to support multiple KB versions for different products/years.

**Versioning Strategy:**

**Directory Structure:**
```
/reference/
  /hmh-knowledge-v1/    ← Legacy (2023-2024 school year)
  /hmh-knowledge-v2/    ← Current (2024-2025 school year)
  /hmh-knowledge-v3/    ← Next (2025-2026 school year, in development)
```

**Curriculum Config Versioning:**
```json
{
  "id": "hmh-math-tx",
  "version": "2.0.0",
  "kb_version": "v2",
  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge-v2/subjects/mathematics/districts/texas/",
      ...
    ]
  }
}
```

**Migration Path:**
1. **Parallel Development:** Build v3 while v2 is in production
2. **Pilot Testing:** Test v3 with select authors (Q3)
3. **Gradual Migration:** New content uses v3, existing content stays on v2 (Q4)
4. **Full Cutover:** All content uses v3 (start of next school year)
5. **Archive v1:** Move v1 to `/reference/.archived/hmh-knowledge-v1/`

**Rollback Capability:**
```bash
# If critical issue found in v3
git revert <commit-hash-for-v3-cutover>

# Configs automatically fall back to v2 paths
# Authors continue working without interruption
```

---

### Pattern 10: Collaborative Knowledge Authoring

**Scenario:** Multiple engineers work on KB simultaneously, need to avoid conflicts.

**Collaboration Patterns:**

**1. Module Ownership**
```
Engineer A: Owns /universal/assessment/
Engineer B: Owns /subjects/mathematics/common/
Engineer C: Owns /districts/texas/
```

**Reduces merge conflicts** - Each engineer works in their domain.

**2. Feature Branches for Large Additions**
```bash
# Engineer adding New York state
git checkout -b feature/add-newyork

# Make all NY changes
[...add files, test, document...]

# Create PR when ready
git push origin feature/add-newyork
```

**3. Lock Files During Major Edits**
```bash
# Create .lock file to signal "I'm editing this"
touch /subjects/mathematics/common/mlr/.EDITING_LOCK_Engineer_A
git add /subjects/mathematics/common/mlr/.EDITING_LOCK_Engineer_A
git commit -m "Lock MLR directory for major refactor"

# Other engineers see lock and coordinate before editing
```

**4. Sync Meetings for Cross-Cutting Changes**
```
Weekly KB Sync Meeting:
- Review upcoming changes
- Identify conflicts
- Assign ownership
- Plan testing
```

**5. Shared Change Log**
```
/reference/hmh-knowledge-v2/CHANGELOG.md

## 2025-11-06
- Engineer A: Added NY state support (3 files)
- Engineer B: Updated MLR files with grade-band examples (8 files)
- Engineer C: Fixed broken cross-references (12 files)

## 2025-11-05
[...]
```

---

## Advanced Patterns Summary

| Pattern | Use When | Key Benefit |
|---------|----------|-------------|
| **1. Conflicting State Requirements** | States have incompatible frameworks | Maintains clarity, avoids confusion |
| **2. Multi-Version Support** | Standards updated, need both versions | Supports transition period |
| **3. Cross-Subject Knowledge** | Same strategy works across subjects | Maximizes reuse, minimizes duplication |
| **4. Modular Architecture** | Files exceed 1000 lines | Easier maintenance, faster loading |
| **5. Progressive Enhancement** | Building KB while supporting production | Balances speed and quality |
| **6. Publisher-Specific** | Feature unique to one program | Right level of specificity |
| **7. Scale Management** | 300+ files across states/subjects | Organized, discoverable, maintainable |
| **8. Performance Optimization** | Authors report slow access | Fast, responsive user experience |
| **9. KB Versioning** | Major KB changes needed | Safe migration, rollback capability |
| **10. Collaborative Authoring** | Multiple engineers working simultaneously | Reduces conflicts, clear ownership |

---

## Collaboration and Communication

Knowledge base engineers work with multiple stakeholders. Clear communication prevents duplicated effort and ensures KB meets real needs.

### Working with Subject Matter Experts (SMEs)

**SME Role:** Provide content expertise, validate pedagogical accuracy
**Your Role:** Structure knowledge, maintain hierarchy, ensure reusability

**Collaboration Workflow:**

**Step 1: Discovery Meeting (30-60 min)**
- **Ask SME:** "What guidance do authors need for [topic]?"
- **Ask SME:** "Does this apply to all states, or specific ones?"
- **Ask SME:** "What grade levels need this?"
- **You explain:** Hierarchy levels and where guidance belongs

**Step 2: Determine KB Level**
```
SME says "All subjects"     → Universal
SME says "All math programs" → /subjects/mathematics/common/
SME says "Texas only"        → /districts/texas/ or /subjects/[subject]/districts/texas/
SME says "Into Math only"    → /subjects/mathematics/districts/texas/into-math/
```

**Step 3: Provide Template**
Send SME a structured template:
```markdown
# [Title]

## Overview
[What this guidance provides]

## When to Use
[Situations where authors apply this]

## How to Apply
[Step-by-step guidance with examples]

## Examples

### Elementary (K-5)
[Grade-appropriate example]

### Middle School (6-8)
[Grade-appropriate example]

### High School (9-12)
[Grade-appropriate example]

## Common Mistakes to Avoid
[What not to do]

## Cross-References
[Related KB files]
```

**Step 4: Review SME Draft**
- **Check:** Does it duplicate existing KB files? → Consolidate or cross-reference
- **Check:** Is it at the right hierarchy level? → Move if needed
- **Check:** Are examples grade-appropriate? → SME validates
- **Check:** Does it follow KB style? → You format

**Step 5: Integrate into KB**
- Add cross-references from related files
- Update curriculum configs if needed
- Add to appropriate index/catalog
- Notify authors of new guidance

**Communication Tips:**
- **Do:** Use SME's language, then translate to KB structure
- **Do:** Show examples of similar KB files for reference
- **Do:** Explain *why* hierarchy matters (reuse, maintainability)
- **Don't:** Assume SME understands KB architecture
- **Don't:** Ask SME to write cross-references (you handle technical structure)

---

### Working with Content Authors

**Author Needs:** Quick access to relevant guidance, clear examples, no duplicates

**Communication Channels:**
1. **Office Hours:** Weekly drop-in for KB questions
2. **Slack/Email:** Async questions and clarifications
3. **KB Changelog:** Notify authors of new/updated files
4. **Feedback Sessions:** Monthly "What's missing?" discussions

**Common Author Questions:**

**Q: "I can't find guidance on [X]"**
- **Investigate:** Search KB for related topics
- **If exists:** Show author where to find it (improve discoverability)
- **If missing:** Assess if it's a real gap or edge case
- **Action:** Add to KB or clarify in next office hours

**Q: "Which file should I use for Texas emergent bilingual support?"**
- **Answer:** Walk through resolution order from their config
- **Show:** `/districts/texas/language/elps-alignment.md` resolves first
- **Explain:** State-specific trumps universal (hierarchy)

**Q: "These two files contradict each other"**
- **Investigate:** Likely DRY violation or unclear hierarchy
- **Action:** Consolidate to appropriate level, add cross-reference
- **Prevent:** Run regular consistency checks

**Creating Author Resources:**
- **Quick Start Guides:** "5 Essential KB Files for TX Math Authors"
- **Video Tutorials:** "How to Navigate the Knowledge Base"
- **Cheat Sheets:** "Which Hierarchy Level for My Question?"
- **Search Tool:** `kb-search.sh` for keyword lookup

---

### Working with Content Editors

**Editor Needs:** KB files to validate author compliance, editorial checklists

**Collaboration Points:**

**1. Editorial Checklists Reference KB**
```markdown
# Editorial Checklist - Math Lesson (TX)

## Standards Alignment
- [ ] Uses TEKS standards (see /subjects/mathematics/districts/texas/teks-math-alignment.md)
- [ ] Appropriate DOK level (see /universal/frameworks/dok-framework.md)

## Instructional Routines
- [ ] Includes 2+ MLRs (see /subjects/mathematics/common/mlr/)
- [ ] MLRs applied correctly (see individual MLR files for guidance)
[...]
```

**2. Editors Report KB Gaps**
Editors reviewing content notice missing guidance:
- **Example:** "Authors consistently misapply MLR5. Need clearer examples."
- **Action:** Enhance `/subjects/mathematics/common/mlr/mlr5-co-craft-questions.md` with more examples

**3. Consistency Enforcement**
Editors use KB as "single source of truth":
- Author's work contradicts KB → Editor refers author back to KB file
- KB is ambiguous → Editor reports to you, you clarify KB

**Communication:** Monthly sync with editorial team to:
- Identify recurring author mistakes (KB needs more clarity)
- Share editor feedback on KB usability
- Plan KB enhancements based on real usage

---

### Cross-Team Communication Best Practices

**1. Document Decisions**
```
/reference/hmh-knowledge-v2/DECISIONS.md

## Why is ELPS at district-wide level, not universal?
ELPS is Texas-specific. Other states use ELD (CA), WIDA/ESOL (FL), etc.
Universal level contains general emergent bilingual strategies applicable across all state frameworks.
Decision: State-specific language frameworks at /districts/[state]/language/
```

**2. Shared Roadmap**
```
/reference/hmh-knowledge-v2/ROADMAP.md

## Q1 2026
- [ ] Add high school (9-12) grade level guidance (all subjects)
- [ ] Expand math common files with Algebra/Geometry specifics
- [ ] Add 5 CCSS states (NY, IL, PA, OH, NC)

## Q2 2026
- [ ] Add Social Studies subject (10 common files, 3 state alignments)
[...]
```

**3. Regular Updates**
- **Weekly:** KB changelog (new files, updates, deprecations)
- **Monthly:** Office hours with authors and editors
- **Quarterly:** Review roadmap, gather feedback, adjust priorities

**4. Celebrate Wins**
```
KB Impact Report - Q3 2025
- 42 lessons created using TX Math KB (100% standards-aligned on first draft)
- Author time to create lesson: Down from 12 hours to 6 hours (50% reduction)
- Editor revision requests: Down from 8.5 to 3.2 per lesson (62% reduction)
- Knowledge reuse: 95% across new curricula
```

---

## Knowledge Base Metrics and Analytics

Measure KB effectiveness, identify gaps, and demonstrate value.

### Key Metrics to Track

**1. Coverage Metrics**
```bash
# States covered
STATES=$(find /reference/hmh-knowledge-v2/districts -mindepth 1 -maxdepth 1 -type d | wc -l)
echo "States: $STATES / 51 ($(($STATES * 100 / 51))%)"

# Subjects covered
SUBJECTS=$(find /reference/hmh-knowledge-v2/subjects -mindepth 1 -maxdepth 1 -type d | wc -l)
echo "Subjects: $SUBJECTS"

# Total KB files
FILES=$(find /reference/hmh-knowledge-v2 -name "*.md" | wc -l)
echo "Total files: $FILES"
```

**Example Output:**
```
States: 3 / 51 (6%)
Subjects: 3
Total files: 50
```

**2. Knowledge Reuse Metrics**
```bash
# Calculate reuse for specific curriculum
# Example: HMH Math Florida
CONFIG="config/curriculum/hmh-math-fl.json"

UNIVERSAL=$(find /reference/hmh-knowledge-v2/universal -name "*.md" | wc -l)
MATH_COMMON=$(find /reference/hmh-knowledge-v2/subjects/mathematics/common -name "*.md" | wc -l)
FL_DISTRICT=$(find /reference/hmh-knowledge-v2/districts/florida -name "*.md" | wc -l)
FL_MATH=$(find /reference/hmh-knowledge-v2/subjects/mathematics/districts/florida -name "*.md" | wc -l)

TOTAL=$(($UNIVERSAL + $MATH_COMMON + $FL_DISTRICT + $FL_MATH))
NEW=$(($FL_DISTRICT + $FL_MATH))  # Assumes FL was added after universal/math common
REUSED=$(($UNIVERSAL + $MATH_COMMON))

REUSE_PCT=$((REUSED * 100 / TOTAL))
echo "FL Math Reuse: $REUSED / $TOTAL = $REUSE_PCT%"
```

**3. Usage Metrics** (if KB tracked)
- Most-accessed files (top 20)
- Least-accessed files (candidates for deprecation)
- Search queries (what are authors looking for?)
- Broken link reports

**4. Content Quality Metrics**
- Lessons created per week using KB
- Standards alignment success rate (first draft)
- Editor revision requests per lesson (lower = KB working well)
- Author time to create lesson (track reduction over time)

### Impact Reporting Template

**Quarterly KB Impact Report**

```markdown
# Knowledge Base Impact Report - Q4 2025

## Coverage Expansion
- **States:** 3 → 4 (added New York)
- **Subjects:** 3 → 4 (added Social Studies)
- **Total Files:** 50 → 63 (+26%)
- **Knowledge Reuse:** 92% average across all curricula

## Author Productivity
- **Lessons Created:** 127 (TX: 68, CA: 37, FL: 22)
- **Avg. Time per Lesson:** 6.5 hours (down from 8.2 hours in Q3)
- **Standards Alignment (1st draft):** 98% (up from 89% in Q3)

## Editorial Efficiency
- **Avg. Revision Requests:** 3.1 per lesson (down from 4.7 in Q3)
- **Editor Review Time:** 1.8 hours (down from 2.4 hours in Q3)

## KB Health
- **Cross-References Validated:** 100% (0 broken links)
- **Files Updated:** 12 (based on author/editor feedback)
- **New Files Added:** 13

## Top 5 Most-Used Files
1. `/universal/frameworks/udl-principles-guide.md` (89% of lessons)
2. `/universal/frameworks/dok-framework.md` (76% of lessons)
3. `/subjects/mathematics/common/mlr/mlr2-collect-display.md` (71% of math lessons)
4. `/districts/texas/language/elps-alignment.md` (94% of TX lessons)
5. `/universal/vocabulary/sentence-frames-guide.md` (68% of lessons)

## Author Feedback Highlights
- "KB guidance saved me hours of searching for MLR examples"
- "ELPS file made language scaffolding so much clearer"
- Request: More worked examples for high school math

## Roadmap for Q1 2026
- Add high school guidance (grades 9-12)
- Expand 5 CCSS states (NY, IL, PA, OH, NC)
- Enhance advanced math topics (Algebra II, Pre-Calc)
```

### Analytics Automation

**Script:** `scripts/kb-analytics.sh`
```bash
#!/bin/bash
# Generate KB analytics report

KB_ROOT="/reference/hmh-knowledge-v2"

echo "KB Analytics Report - $(date +%Y-%m-%d)"
echo "=========================================="
echo ""

echo "Coverage:"
echo "  States: $(find $KB_ROOT/districts -mindepth 1 -maxdepth 1 -type d | wc -l)"
echo "  Subjects: $(find $KB_ROOT/subjects -mindepth 1 -maxdepth 1 -type d | wc -l)"
echo "  Total Files: $(find $KB_ROOT -name "*.md" | wc -l)"
echo ""

echo "File Distribution:"
echo "  Universal: $(find $KB_ROOT/universal -name "*.md" | wc -l)"
echo "  Subject-Common: $(find $KB_ROOT/subjects/*/common -name "*.md" | wc -l)"
echo "  Subject-District: $(find $KB_ROOT/subjects/*/districts -name "*.md" | wc -l)"
echo "  District-Wide: $(find $KB_ROOT/districts -name "*.md" | wc -l)"
echo ""

echo "Largest Files (top 5):"
find $KB_ROOT -name "*.md" -exec wc -l {} \; | sort -rn | head -5
echo ""

echo "Cross-Reference Health:"
./scripts/validate-cross-refs.sh > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "  ✓ All cross-references valid"
else
  echo "  ✗ Some broken cross-references found (run validate-cross-refs.sh for details)"
fi
```

**Usage:**
```bash
chmod +x scripts/kb-analytics.sh
./scripts/kb-analytics.sh > reports/kb-analytics-2025-11-06.txt
```

### Continuous Improvement Cycle

**Monthly Review:**
1. **Analyze metrics** - What's working? What's not?
2. **Gather feedback** - Authors, editors, SMEs
3. **Identify top 3 improvements** - Prioritize high-impact changes
4. **Implement & test** - Make changes, validate
5. **Measure impact** - Did metrics improve?
6. **Repeat**

**Example Improvement Cycle:**
```
Month 1: Authors report MLR guidance unclear
→ Action: Add more grade-specific examples to MLR files
→ Result: Author MLR application errors drop 40%

Month 2: Editors report inconsistent ELPS scaffolding
→ Action: Enhance ELPS file with sentence frame templates
→ Result: Editor revision requests for language support drop 35%

Month 3: Authors request high school physics guidance
→ Action: Add /subjects/science/common/physics-specific-practices.md
→ Result: 18 high school physics lessons created (previously blocked)
```

---

## Getting Help

### Documentation Resources

- **This Guide:** Complete engineering documentation (you are here)
- **Content Authors:** See `AUTHOR_GUIDE.md`
- **Content Editors:** See `EDITOR_GUIDE.md`
- **Publishers:** See `PRODUCTION_GUIDE.md`
- **System Overview:** See `USER_GUIDE.md`
- **Architecture Summary:** See archived HMH documentation in `.archive/`

### Support Contacts

**For Questions About:**
- **Architecture/System Design:** Contact lead architect
- **Curriculum Content:** Contact subject matter experts
- **Standards Alignment:** Contact state compliance experts
- **Technical Issues:** Contact development team

### Contributing

**To Propose New Files:**
1. Create issue describing need
2. Identify hierarchy level
3. Draft content following templates
4. Submit for review
5. Incorporate feedback
6. Add to repository

**To Report Issues:**
1. Check if issue already known
2. Document what's wrong
3. Provide examples/evidence
4. Suggest solution if possible
5. Submit issue

---

## Appendix: File Inventory

### Current Files (Week 3 - 50 files)

**Universal (15 files):**
- frameworks/dok-framework.md
- frameworks/udl-principles-guide.md
- frameworks/udl-implementation-examples.md
- frameworks/eb-scaffolding-guide.md
- frameworks/sentence-frames-library.md
- assessment/alt-text-principles.md
- assessment/parity-guidelines.md
- assessment/item-types-reference.md
- assessment/item-writing-best-practices.md
- assessment/scoring-rubrics-guide.md
- assessment/validation-methods.md
- assessment/learnosity-configuration-guide.md
- assessment/answer-key-standards.md
- accessibility/wcag-compliance-guide.md
- content-equity/ceid-guidelines.md
- vendor/vendor-checklist-complete.md

**Mathematics Subject-Common (12 files):**
- common/mlr/mlr-overview.md
- common/mlr/mlr-placement-rules.md
- common/mlr/mlr1-stronger-clearer.md
- common/mlr/mlr2-collect-display.md
- common/mlr/mlr3-critique-correct-clarify.md
- common/mlr/mlr4-information-gap.md
- common/mlr/mlr5-co-craft-questions.md
- common/mlr/mlr6-three-reads.md
- common/mlr/mlr7-compare-connect.md
- common/mlr/mlr8-discussion-supports.md
- common/vocab-guidelines.md
- common/problem-solving-framework.md

**ELA Subject-Common (4 files):**
- common/literacy-routines-overview.md
- common/literacy-routines/close-reading-protocol.md
- common/literacy-routines/think-pair-share.md
- common/literacy-routines/annotation-protocol.md
- common/literacy-routines/turn-and-talk.md

**Science Subject-Common (2 files):**
- common/ngss-alignment-guide.md
- common/science-practices-framework.md

**Texas District-Wide (4 files):**
- compliance/ipacc-suitability-requirements.md
- compliance/sboe-quality-rubric.md
- compliance/texas-compliance-checklist.md
- language/elps-alignment.md

**California District-Wide (2 files):**
- compliance/california-adoption-criteria.md
- language/eld-alignment.md

**Florida District-Wide (3 files):**
- compliance/florida-adoption-criteria.md
- language/esol-alignment.md

**Texas Math Subject-District (2 files):**
- districts/texas/teks-math-alignment.md
- districts/texas/gap-mitigation-strategies.md

**California Math Subject-District (1 file):**
- districts/california/ccss-m-alignment.md

**Florida Math Subject-District (1 file):**
- districts/florida/mafs-alignment.md

**Texas ELA Subject-District (1 file):**
- districts/texas/teks-ela-alignment.md

**Publishers/HMH (1 file):**
- content-block-schema.json

**Total: 50 files**

---

**End of Engineer's Guide**

**Version:** 1.0
**Last Updated:** November 6, 2025
**Maintained By:** HMH Curriculum Development Team
**Repository:** https://github.com/pauljbernard/content.git
