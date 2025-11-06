# Content Author Guide
**HMH Multi-Curriculum Knowledge Base - For Content Authors**
**Version:** 1.0
**Last Updated:** November 6, 2025

---

## Welcome to Content Authoring

As a content author, you create educational materials (lessons, assessments, activities) that are:
- **Standards-aligned** to state requirements (TEKS, CCSS, NGSS, etc.)
- **Pedagogically sound** based on learning science research
- **Accessible** to all learners (WCAG 2.1 AA, UDL principles)
- **Culturally responsive** and bias-free
- **Compliant** with state adoption criteria

This guide provides everything you need to create high-quality content using the HMH Multi-Curriculum Knowledge Base system.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Understanding Your Content Brief](#2-understanding-your-content-brief)
3. [Using the Knowledge Base](#3-using-the-knowledge-base)
4. [Authoring Workflows](#4-authoring-workflows)
5. [Working with AI Assistance](#5-working-with-ai-assistance)
6. [Quality Standards](#6-quality-standards)
7. [Collaboration and Version Control](#7-collaboration-and-version-control)

---

## 1. Getting Started

### Your Authoring Environment

**Tools You'll Use:**
- **Content Management System** - Where you draft and submit content
- **Knowledge Base** - Reference library (50+ files at `/reference/hmh-knowledge-v2/`)
- **Professor AI Assistant** - AI-powered content generation (optional)
- **GitHub** - Version control and collaboration
- **Style Guides** - HMH editorial standards

**Directory Structure:**
```
content/
├── drafts/                    # Your working area
│   ├── lessons/
│   ├── assessments/
│   └── activities/
├── reviews/                   # Editor feedback location
├── published/                 # Final approved content
└── reference/hmh-knowledge-v2/  # Knowledge base (read-only)
```

### First Steps

**Step 1: Understand Your Assignment**
- Review content brief (specifications document)
- Identify state, subject, grade level
- Note standards to address
- Check compliance requirements

**Step 2: Set Up Your Configuration**
Determine which curriculum config applies:
- `config/curriculum/hmh-math-tx.json` - Texas Math (K-8)
- `config/curriculum/hmh-math-ca.json` - California Math (K-8)
- `config/curriculum/hmh-math-fl.json` - Florida Math (K-8)
- `config/curriculum/hmh-ela-tx.json` - Texas ELA (K-8)

**Step 3: Gather Resources**
- Load relevant knowledge base files (see [Section 3](#3-using-the-knowledge-base))
- Review standards documents
- Collect assets (images, diagrams, etc.)

**Step 4: Draft Content**
- Work in `/drafts/` directory
- Follow templates (see [Section 4](#4-authoring-workflows))
- Apply knowledge base guidance
- Use AI assistance if needed (see [Section 5](#5-working-with-ai-assistance))

**Step 5: Self-Review**
- Check quality standards (see [Section 6](#6-quality-standards))
- Run accessibility checks
- Verify standards alignment

**Step 6: Submit for Editorial Review**
- Create pull request in GitHub
- Tag editor for feedback
- Address feedback and iterate

---

## 2. Understanding Your Content Brief

### What is a Content Brief?

A **content brief** is your specification document. It defines what you need to create and all requirements.

### Required Elements

**1. Product Information**
- Program name (e.g., "HMH Into Math Texas Edition")
- Subject and grade level
- Content type (lesson, assessment, activity)

**2. Standards Alignment**
- Specific standards to address (e.g., TEKS.5.NF.1.1)
- Learning objectives (measurable)
- DOK (Depth of Knowledge) levels

**3. Scope and Specifications**
- Length/duration
- Format requirements
- Required components

**4. Compliance Requirements**
- State-specific (SBOE, IPACC, adoption criteria)
- Accessibility standards (WCAG 2.1 AA)
- Language support (ELPS, ELD, ESOL)

**5. Pedagogical Requirements**
- Instructional routines (MLRs, literacy routines, science practices)
- UDL principles
- Scaffolding for emergent bilinguals

**6. Assets and Resources**
- Images, diagrams, manipulatives needed
- External resources
- Prior knowledge to build on

### Example Content Brief

```yaml
project: HMH Into Math Texas Edition - Grade 5
content_type: Lesson
curriculum_config: hmh-math-tx.json

standards:
  primary: TEKS.5.NF.1.1 (Add and subtract fractions with unlike denominators)
  supporting:
    - TEKS.5.NF.1.2 (Fraction operations fluency)
    - ELPS.3.E (Share information in cooperative learning)

learning_objectives:
  - Students will add fractions with unlike denominators using visual models
  - Students will explain their reasoning using academic language
  - Students will identify common denominators in real-world contexts

dok_level: 2 (Skills & Concepts) with DOK 3 extensions

lesson_structure:
  duration: 60 minutes
  components:
    - Warm-up (10 min) - MLR8: Discussion Supports
    - Instruction (20 min) - CRA progression
    - Guided Practice (15 min) - MLR1: Stronger and Clearer Each Time
    - Independent Practice (10 min) - Differentiated
    - Closure (5 min) - MLR2: Collect and Display

scaffolding:
  emergent_bilinguals:
    - Visual fraction models required
    - Sentence frames for reasoning
    - Bilingual glossary (English/Spanish)
    - Strategic partner pairing
  special_needs:
    - Simplified language option
    - Extended time scaffolds
    - Manipulatives (fraction tiles)

accessibility:
  - All images require alt text
  - Color contrast minimum 4.5:1
  - Text must be selectable/scalable

compliance:
  - SBOE Quality Rubric criteria 1-5
  - IPACC suitability requirements
  - Texas content restrictions

deliverables:
  - Teacher guide (PDF and HTML)
  - Student pages (PDF and interactive HTML)
  - Digital slides
  - Assessment items (3-5 formative checks)

timeline:
  draft_due: 2025-11-15
  review_cycle: 2025-11-18 to 2025-11-22
  final_due: 2025-11-29
```

### Interpreting Your Brief

**Step 1: Identify Curriculum Config**
- Brief says "HMH Into Math Texas Edition" → Use `hmh-math-tx.json`

**Step 2: Map Standards to Knowledge Base**
- TEKS.5.NF.1.1 → `/subjects/mathematics/districts/texas/teks-math-alignment.md`
- ELPS.3.E → `/districts/texas/language/elps-alignment.md`

**Step 3: Identify Required Routines**
- MLR1, MLR2, MLR8 → `/subjects/mathematics/common/mlr/mlr1-stronger-clearer.md`, etc.

**Step 4: Note Compliance**
- SBOE, IPACC → `/districts/texas/compliance/sboe-quality-rubric.md`

**Step 5: Check Universal Requirements**
- UDL, WCAG, EB scaffolding → `/universal/frameworks/` files

---

## 3. Using the Knowledge Base

### How the Knowledge Base Helps You

The knowledge base is your comprehensive reference library. It provides unified, hierarchical guidance that combines automatically for your specific content.

### Step-by-Step Process

#### Step 1: Identify Your Config

Your brief specifies which config: `hmh-math-tx.json`, `hmh-math-ca.json`, etc.

#### Step 2: Understand Resolution Order

Open your config file (e.g., `/config/curriculum/hmh-math-tx.json`):

```json
{
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
}
```

System searches **most specific → most general**.

#### Step 3: Gather Relevant Files

**For Texas 5th Grade Math Lesson on Fractions:**

**Universal (applies to everything):**
- `universal/frameworks/udl-principles-guide.md`
- `universal/frameworks/dok-framework.md`
- `universal/frameworks/eb-scaffolding-guide.md`
- `universal/frameworks/sentence-frames-library.md`
- `universal/accessibility/wcag-compliance-guide.md`
- `universal/assessment/item-types-reference.md`

**District-Wide (Texas, all subjects):**
- `districts/texas/language/elps-alignment.md`
- `districts/texas/compliance/sboe-quality-rubric.md`
- `districts/texas/compliance/ipacc-suitability-requirements.md`

**Subject-Common (Math, all states):**
- `subjects/mathematics/common/mlr/mlr-overview.md`
- `subjects/mathematics/common/mlr/mlr1-stronger-clearer.md`
- `subjects/mathematics/common/mlr/mlr2-collect-display.md`
- `subjects/mathematics/common/mlr/mlr8-discussion-supports.md`
- `subjects/mathematics/common/vocab-guidelines.md`
- `subjects/mathematics/common/problem-solving-framework.md`

**Subject-District (Texas Math):**
- `subjects/mathematics/districts/texas/teks-math-alignment.md`
- `subjects/mathematics/districts/texas/gap-mitigation-strategies.md`

**Total:** ~18 files providing comprehensive guidance

#### Step 4: Apply Knowledge Base Guidance

**Example: Writing Warm-Up (10 min)**

**Consult:**
1. MLR8 file for protocol
2. ELPS file for language scaffolding
3. EB Scaffolding Guide for sentence frames
4. UDL Guide for engagement strategies

**Apply:**
```markdown
### Warm-Up (10 minutes) - MLR8: Discussion Supports

**Objective:** Activate prior knowledge of fractions.

**Problem:** "Sarah ate 1/3 of a pizza. Marcus ate 1/4 of the same pizza.
Who ate more? How much did they eat together?"

**MLR8 Protocol** (from mlr8-discussion-supports.md):
1. **Revoicing:** "I heard you say... Is that correct?"
2. **Prompting:** "Can you say more about...?"
3. **Wait Time:** 30 seconds think time

**ELPS 3.E Support** (from elps-alignment.md):
- **Beginning:** "I think ___ ate more because ___."
- **Intermediate:** "To solve this, I need to ___."
- **Advanced:** "First I will ___, then I will ___."

**UDL Engagement** (from udl-principles-guide.md):
- Visual: Project pizza images
- Kinesthetic: Provide fraction circles
- Choice: Explain verbally, write, or draw

**Accessibility** (from wcag-compliance-guide.md):
- Alt text: "Two pizzas, one divided into thirds with 1 shaded,
  one divided into fourths with 1 shaded."
```

---

## 4. Authoring Workflows

### Content Types

1. **Lessons** - Full instructional sequences (45-90 minutes)
2. **Assessments** - Formative and summative evaluations
3. **Activities** - Standalone practice tasks
4. **Scaffolding Materials** - Graphic organizers, sentence frames
5. **Teacher Resources** - Answer keys, facilitation guides

---

### Workflow: Lessons

**Timeline:** 3-5 days from brief to final draft

#### Phase 1: Planning (Day 1)

**Tasks:**
- [ ] Read content brief thoroughly
- [ ] Review standards documents
- [ ] Gather knowledge base files
- [ ] Define learning objectives and success criteria
- [ ] Sketch lesson arc (warm-up → instruction → practice → closure)
- [ ] Plan instructional routines
- [ ] Note differentiation needs

**Deliverable:** Lesson outline (1-2 pages)

#### Phase 2: Drafting (Days 2-3)

**Use This Template:**

```markdown
# [Lesson Title]
**Grade:** X | **Subject:** [Math/ELA/Science] | **Duration:** XX minutes
**Standards:** [List all standards]
**Learning Objectives:**
- Students will [measurable action verb] ...
- Students will [measurable action verb] ...
- Students will [measurable action verb] ...

## Lesson Overview
[2-3 sentence summary of what students will learn and do]

## Materials
**Teacher Materials:**
- [List items]

**Student Materials:**
- [List items]

**Technology/Manipulatives:**
- [List items]

## Preparation
- [Setup task 1]
- [Setup task 2]
- [Key vocabulary to pre-teach]

## Lesson Sequence

### Warm-Up (X minutes)
**Objective:** [What this section accomplishes]
**Instructional Routine:** [MLR/Literacy Routine name]

[Step-by-step instructions for teacher]

**Scaffolds for Emergent Bilinguals:**
- **Beginning:** [Specific scaffold]
- **Intermediate:** [Specific scaffold]
- **Advanced:** [Specific scaffold]

**Accessibility Notes:**
- [Any modifications needed]

**Formative Check:**
- [How to check understanding]

---

### Instruction (X minutes)
**Objective:** [What this section accomplishes]

[Detailed teaching steps with:]
- Modeling and think-alouds
- Examples and non-examples
- Checking for understanding
- Visual supports

**Common Misconceptions:**
- [Misconception 1]: [How to address]

**Scaffolds for Emergent Bilinguals:**
- **Beginning:** [Specific scaffold]
- **Intermediate:** [Specific scaffold]
- **Advanced:** [Specific scaffold]

---

### Guided Practice (X minutes)
**Objective:** [Scaffolded application]

[Partner or small group work structure]
[Teacher circulation and monitoring]
[Questions to ask while circulating]

**Formative Check:**
- [Observation checklist or quick assessment]

---

### Independent Practice (X minutes)
**Objective:** [Individual application]

[Individual work task]

**Differentiation:**
- **Below Grade Level:** [Scaffold]
- **On Grade Level:** [Core task]
- **Above Grade Level:** [Extension]

---

### Closure (X minutes)
**Objective:** [Summarize and assess learning]

[Exit ticket or formative assessment]
[Reflection prompt]

---

## Differentiation

### Emergent Bilinguals
**Beginning:**
- [Specific supports]

**Intermediate:**
- [Specific supports]

**Advanced:**
- [Specific supports]

### By Readiness Level
**Below Grade Level:**
- [Scaffolds and supports]

**On Grade Level:**
- [Core expectations]

**Above Grade Level:**
- [Extensions and challenges]

### Special Needs
- [Modifications as appropriate]

## Assessment

### Formative Checks Throughout Lesson
- Warm-up: [What to observe]
- Instruction: [What to observe]
- Guided Practice: [What to observe]
- Independent Practice: [What to assess]
- Closure: [Exit ticket or check]

### Success Criteria
Students demonstrate success when they can:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

## Answer Key
[Complete solutions with explanations for all practice problems]

---

## Assets Needed
- [Image 1]: [Description for designer]
- [Image 2]: [Description for designer]
- [Video 1]: [Description]
```

**Deliverable:** Complete draft lesson (10-20 pages)

#### Phase 3: Self-Review (Day 4)

**Use Pre-Submission Checklist (see [Section 6](#6-quality-standards))**

#### Phase 4: Submit for Review (Day 5)

1. Move files to `/drafts/lessons/[curriculum-name]/`
2. Create folder:
   ```
   lesson-title/
   ├── teacher-guide.md
   ├── student-pages.md
   ├── assets/
   └── metadata.json
   ```
3. Fill metadata:
   ```json
   {
     "title": "Adding Fractions with Unlike Denominators",
     "curriculum": "hmh-math-tx",
     "grade": "5",
     "subject": "mathematics",
     "standards": ["TEKS.5.NF.1.1"],
     "duration_minutes": 60,
     "author": "Your Name",
     "date_created": "2025-11-15",
     "review_status": "pending"
   }
   ```
4. Create pull request
5. Tag editor

---

### Workflow: Assessments

**Timeline:** 2-4 days

#### Phase 1: Design Blueprint (Day 1)

**Create Assessment Blueprint:**
```
Assessment: Grade 5 Unit 3 - Fractions Operations

Standards Coverage:
- TEKS.5.NF.1.1 (Add/subtract unlike denominators) - 40%
- TEKS.5.NF.1.2 (Fluency) - 30%
- TEKS.5.NF.2.1 (Multiply fractions) - 30%

DOK Distribution:
- DOK 1 (Recall): 20%
- DOK 2 (Skills): 50%
- DOK 3 (Strategic): 25%
- DOK 4 (Extended): 5%

Item Types:
- Multiple Choice: 60%
- Short Constructed Response: 30%
- Extended Constructed Response: 10%
```

**Deliverable:** Blueprint approved by curriculum lead

#### Phase 2: Write Items (Days 2-3)

**Multiple Choice Template:**
```markdown
## Item 7

**Standard:** TEKS.5.NF.1.1
**DOK:** 2
**Correct Answer:** C

**Stimulus:**
Maria has 2/3 of a yard of ribbon. She buys 3/4 of a yard more.
How much ribbon does Maria have in all?

**Options:**
A. 5/7 yard
B. 5/12 yard
C. 1 5/12 yards ← CORRECT
D. 17/12 yards

**Rationale:**
- Option A: Added numerators and denominators incorrectly
- Option B: Found common denominator but didn't add correctly
- Option C: CORRECT - 2/3 = 8/12, 3/4 = 9/12, sum = 17/12 = 1 5/12
- Option D: Didn't convert improper fraction

**Alt Text:** "Text problem about adding fractions of ribbon."

**EB Scaffolds:**
- Beginning: Provide visual ribbon models
- Intermediate: "First I need to find ___."
```

**Constructed Response Template:**
```markdown
## Item 18

**Standard:** TEKS.5.NF.1.1
**DOK:** 3
**Points:** 4

**Prompt:**
Tyler says 1/2 + 1/3 = 2/5 because "you just add across."

Part A: Explain Tyler's error.
Part B: Show the correct solution.
Part C: Give Tyler advice to avoid this mistake.

**Rubric:**
4 points:
- Clearly explains error (added numerators and denominators)
- Shows correct solution (5/6)
- Provides helpful advice about common denominators
- Work is organized

3 points:
- Explains error adequately
- Correct solution
- Advice somewhat helpful

2 points:
- Partially explains error
- Minor errors in solution

1 point:
- Minimal explanation
- Significant errors

0 points:
- No response or completely incorrect

**Sample Response:** [Include exemplar]

**EB Scaffolds:**
- Beginning: Sentence frames for each part
- Intermediate: Partially completed visual model
```

#### Phase 3: Create Answer Key (Day 3)

Include:
- Correct answers marked
- Rationales for MC distractors
- Complete solutions for CR items
- Point values and rubrics

#### Phase 4: Submit (Day 4)

Submit to `/drafts/assessments/[curriculum]/unit-X/`

---

### Workflow: Activities

Activities are standalone tasks (10-30 minutes).

**Types:**
- Practice (skill reinforcement)
- Exploration (discovery learning)
- Games (engaging practice)
- Challenges (extension)

**Template:**
```markdown
# [Activity Title]

**Grade:** X | **Duration:** XX min | **Standards:** [Aligned]
**Objective:** [What students practice/explore]

## Overview
[1-2 sentence description]

## Materials
[What students need]

## Instructions

### Step 1: [Action]
[Clear instructions with visual support]

### Step 2: [Action]
[Clear instructions]

### Step 3: [Action]
[Clear instructions]

## Differentiation
- **Below:** [Scaffolds]
- **On Level:** [Core]
- **Above:** [Extensions]

## Success Criteria
- [Criterion 1]
- [Criterion 2]

## Teacher Notes
[Facilitation tips, common challenges]

## EB Scaffolds
[Language supports]
```

**Timeline:** 1-2 days

---

## 5. Working with AI Assistance

### Overview

The **Professor Framework** provides AI assistance with access to all knowledge base files and 92 curriculum development skills.

### When to Use AI

**Use AI for:**
- Generating first drafts from outlines
- Creating item variations
- Suggesting differentiation strategies
- Drafting sentence frames
- Formatting content
- Checking standards alignment
- Generating alt text

**Don't Rely on AI for:**
- Final pedagogical decisions
- Cultural responsiveness nuances
- Complex assessment validation
- Creative problem-solving

### How to Use AI

#### Method 1: GitHub Issues (@claude)

Create issue:
```markdown
Title: Generate Grade 5 Texas Math Lesson on Fractions

@claude Create 60-min lesson for Grade 5 Texas Math on adding fractions
with unlike denominators.

Config: hmh-math-tx.json

Standards: TEKS.5.NF.1.1, ELPS.3.E

Requirements:
- Include MLR1, MLR2, MLR8
- ELPS scaffolds (Beginning/Intermediate/Advanced)
- UDL principles
- Formative checks
- Differentiation
```

AI generates complete lesson and creates pull request.

#### Method 2: Command Line

```bash
claude-code --skill curriculum.develop-content \
  --config hmh-math-tx.json \
  --grade 5 \
  --standard "TEKS.5.NF.1.1" \
  --output drafts/lessons/
```

#### Method 3: GitHub Actions

1. Go to **Actions** tab
2. Select **"Automated Content Development"**
3. Fill form with specifications
4. System generates content and creates PR

### Reviewing AI Output

**Always check:**
- [ ] Accuracy (content correct)
- [ ] Standards alignment
- [ ] Pedagogical soundness
- [ ] Cultural responsiveness
- [ ] Accessibility
- [ ] Language quality
- [ ] Coherence and flow

**AI is a starting point.** Apply your professional judgment.

---

## 6. Quality Standards

### The 7 Quality Pillars

All content must meet these standards:

#### 1. Standards Alignment

**Requirements:**
- Every objective maps to a standard
- Content depth matches standard expectations
- Assessments measure the standard
- Vertical alignment (builds on prior, prepares for next)

**Check:**
- [ ] List every standard addressed
- [ ] Map each objective to standard
- [ ] Review standards file for expectations
- [ ] Verify rigor matches intent

**Reference:** `/subjects/[subject]/districts/[state]/[standards-file].md`

#### 2. Pedagogical Soundness

**Requirements:**
- Research-based practices
- Gradual release (I do, We do, You do)
- Formative assessment throughout
- Addresses misconceptions
- Sufficient practice

**Check:**
- [ ] Includes modeling, guided practice, independent practice
- [ ] Routines applied correctly (check MLR/literacy files)
- [ ] Multiple representations (concrete, representational, abstract)
- [ ] Formative checks every 10-15 min
- [ ] Misconceptions anticipated

**Reference:**
- `/subjects/mathematics/common/mlr/*.md`
- `/subjects/ela/common/literacy-routines/*.md`
- `/subjects/science/common/science-practices-framework.md`
- `/universal/frameworks/udl-principles-guide.md`

#### 3. Language Support

**Requirements:**
- Scaffolds for Beginning, Intermediate, Advanced ELLs
- Sentence frames for academic discourse
- Vocabulary explicitly taught
- Visuals support language
- Strategic grouping

**Check:**
- [ ] ELPS/ELD/ESOL standards addressed
- [ ] Scaffolds for 3 proficiency levels
- [ ] Sentence frames provided
- [ ] Visual supports for key concepts
- [ ] Language routines embedded

**Reference:**
- `/districts/texas/language/elps-alignment.md`
- `/districts/california/language/eld-alignment.md`
- `/districts/florida/language/esol-alignment.md`
- `/universal/frameworks/eb-scaffolding-guide.md`
- `/universal/frameworks/sentence-frames-library.md`

#### 4. Universal Design for Learning (UDL)

**Requirements:**
- Multiple means of representation
- Multiple means of action/expression
- Multiple means of engagement

**Check:**
- [ ] At least 2 representations per concept
- [ ] Student choice in demonstrating learning
- [ ] Content connects to students' lives
- [ ] Options for different challenge levels

**Reference:** `/universal/frameworks/udl-principles-guide.md`

#### 5. Accessibility (WCAG 2.1 AA)

**Requirements:**
- All images have alt text
- Color contrast ≥ 4.5:1 (normal text), ≥ 3:1 (large text)
- Keyboard navigable
- Text selectable and scalable
- No flashing content

**Check:**
- [ ] Every image has descriptive alt text
- [ ] Color contrast checked
- [ ] Interactive elements keyboard-accessible
- [ ] No color-only information
- [ ] Headings properly nested

**Reference:** `/universal/accessibility/wcag-compliance-guide.md`

#### 6. Cultural Responsiveness

**Requirements:**
- Diverse representation
- No stereotypes
- Culturally inclusive contexts
- Respectful of all identities
- Age-appropriate

**Check:**
- [ ] Diverse names and contexts
- [ ] Images show diverse people
- [ ] No stereotypes (gender, race, ability, family, etc.)
- [ ] Reviewed using CEID framework

**Reference:** `/universal/content-equity/ceid-guidelines.md`

#### 7. State Compliance

**Requirements:**
- Meets state adoption criteria
- Addresses quality rubrics
- Complies with content restrictions

**Check (Texas):**
- [ ] SBOE Quality Rubric criteria met
- [ ] IPACC suitability requirements met
- [ ] No prohibited content

**Reference:**
- `/districts/texas/compliance/sboe-quality-rubric.md`
- `/districts/texas/compliance/ipacc-suitability-requirements.md`
- `/districts/california/compliance/california-adoption-criteria.md`
- `/districts/florida/compliance/florida-adoption-criteria.md`

### Pre-Submission Checklist

**Before submitting, verify:**

- [ ] All standards from brief addressed
- [ ] Learning objectives measurable and clear
- [ ] DOK levels appropriate
- [ ] Instructional routines applied correctly
- [ ] Gradual release followed
- [ ] Formative assessment embedded
- [ ] Differentiation provided
- [ ] ELPS/ELD/ESOL standards addressed
- [ ] Scaffolds for 3 EB proficiency levels
- [ ] Sentence frames provided
- [ ] UDL: multiple representations
- [ ] UDL: multiple means of action/expression
- [ ] UDL: multiple means of engagement
- [ ] All images have alt text
- [ ] Color contrast sufficient
- [ ] Keyboard navigable
- [ ] Diverse representation
- [ ] No stereotypes or bias
- [ ] State compliance met
- [ ] Spelling/grammar correct
- [ ] Formatting consistent
- [ ] Assets specified
- [ ] Answer key complete
- [ ] Metadata complete

---

## 7. Collaboration and Version Control

### Using Git and GitHub

**Basic Workflow:**

**1. Start Work**
```bash
git checkout -b lesson-grade5-fractions
mkdir -p drafts/lessons/math-grade5-fractions
# ... create files ...
git add .
git commit -m "Draft: Grade 5 fractions lesson"
git push origin lesson-grade5-fractions
```

**2. Submit for Review**
```bash
git push origin lesson-grade5-fractions
# In GitHub: Create Pull Request
# Add description, tag reviewers
```

**3. Respond to Feedback**
```bash
# Editor leaves comments
# Make revisions
git add .
git commit -m "Address feedback: add EB scaffolds"
git push origin lesson-grade5-fractions
# PR updates automatically
```

**4. Approval**
```bash
# Editor approves and merges
# Content moves to /published/
```

### Best Practices

**Communicating with Editors:**
- Respond to all feedback
- Ask clarifying questions
- Explain design choices
- Be open to suggestions

**File Organization:**
```
drafts/lessons/hmh-math-tx/grade-5/unit-3-fractions/
└── lesson-1-add-unlike-denominators/
    ├── teacher-guide.md
    ├── student-pages.md
    ├── assets/
    └── metadata.json
```

**Naming:**
- Branches: `content-type-brief-description`
- Files: `lowercase-with-hyphens.md`
- Folders: `descriptive-purpose/`

**Commit Messages:**
```bash
# Good
git commit -m "Draft: Complete Grade 5 fractions lesson"
git commit -m "Fix: Correct answer key for problem 7"

# Bad
git commit -m "updates"
git commit -m "fixed stuff"
```

---

## Quick Reference

### Knowledge Base File Locations

**Universal (all curricula):**
- `/universal/frameworks/` - UDL, DOK, EB scaffolding, sentence frames
- `/universal/assessment/` - Item types, rubrics, answer keys
- `/universal/accessibility/` - WCAG compliance
- `/universal/content-equity/` - CEID guidelines

**Subject-Common (all states):**
- `/subjects/mathematics/common/mlr/` - 8 Math Language Routines
- `/subjects/ela/common/literacy-routines/` - Close Reading, Think-Pair-Share, etc.
- `/subjects/science/common/` - NGSS, Science Practices

**District-Wide (all subjects in state):**
- `/districts/texas/` - ELPS, SBOE, IPACC
- `/districts/california/` - ELD, adoption criteria
- `/districts/florida/` - ESOL, adoption criteria

**Subject-District (state + subject):**
- `/subjects/[subject]/districts/[state]/` - Standards alignment files

### Curriculum Configs

- `config/curriculum/hmh-math-tx.json` - Texas Math
- `config/curriculum/hmh-math-ca.json` - California Math
- `config/curriculum/hmh-math-fl.json` - Florida Math
- `config/curriculum/hmh-ela-tx.json` - Texas ELA

### Support

- **Editorial Questions:** Tag editor in PR comments
- **Technical Issues:** Create issue in GitHub
- **Knowledge Base Questions:** See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)
- **Style Guide:** See HMH editorial standards

---

## Glossary

**CER:** Claim-Evidence-Reasoning framework (science)
**CEID:** Content Equity, Inclusion & Diversity guidelines
**DOK:** Depth of Knowledge (4 levels)
**EB:** Emergent Bilingual
**ELD:** English Language Development (California)
**ELPS:** English Language Proficiency Standards (Texas)
**ESOL:** English for Speakers of Other Languages (Florida)
**MLR:** Mathematical Language Routine (8 routines)
**NGSS:** Next Generation Science Standards
**SBOE:** State Board of Education (Texas)
**TEKS:** Texas Essential Knowledge and Skills
**UDL:** Universal Design for Learning
**WCAG:** Web Content Accessibility Guidelines

---

**Version:** 1.0 | **Last Updated:** November 6, 2025
**For more information:** See [README.md](README.md) | [USER_GUIDE.md](USER_GUIDE.md)
