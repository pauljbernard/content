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

**Quick Start:**
- [Your First Week](#your-first-week-quick-start)

**Core Content:**
1. [Getting Started](#1-getting-started)
2. [Understanding Your Content Brief](#2-understanding-your-content-brief)
3. [Using the Knowledge Base](#3-using-the-knowledge-base)
   - [How to Read Knowledge Base Files](#35-how-to-read-and-apply-knowledge-base-files)
   - [Cross-Subject Example: California ELA](#36-cross-subject-example-california-ela)
4. [Authoring Workflows](#4-authoring-workflows)
   - [Complete Example Works](#45-complete-example-works)
5. [Working with AI Assistance](#5-working-with-ai-assistance)
6. [Quality Standards](#6-quality-standards)
7. [Collaboration and Version Control](#7-collaboration-and-version-control)

**Support:**
8. [Frequently Asked Questions](#8-frequently-asked-questions)
9. [Troubleshooting Common Issues](#9-troubleshooting-common-issues)
10. [Process Information and Support](#10-process-information-and-support)

---

## Your First Week Quick Start

**New to content authoring?** This quickstart gets you productive in 5 days.

### Day 1: Environment Setup and Orientation (2-3 hours)

**Morning:**
1. **Access your authoring environment**
   - Log into content management system
   - Verify GitHub access
   - Clone content repository: `git clone https://github.com/pauljbernard/content.git`

2. **Read your first content brief**
   - Check your email/dashboard for assignment
   - Download or bookmark content brief
   - Note: State, subject, grade, standards, deadline

3. **Quick tour of knowledge base**
   - Navigate to `/reference/hmh-knowledge-v2/`
   - Browse universal files (everyone uses these)
   - Find your state folder (TX, CA, or FL)
   - Find your subject folder (mathematics, ela, or science)

**Afternoon:**
4. **Read Section 1-2 of this guide**
   - Understand the 6-step process
   - Learn how to interpret your brief

5. **Find your curriculum config**
   - Locate in `/config/curriculum/`
   - Open and review resolution order
   - Bookmark the 5-8 folders you'll use most

**End of Day 1:** You should know what you're creating, which config to use, and where to find help.

---

### Day 2: Deep Dive on Knowledge Base (3-4 hours)

**Morning:**
1. **Read Section 3 of this guide carefully**
2. **Gather your knowledge files** (~18 files)
   - Universal: UDL, DOK, EB Scaffolding, WCAG
   - District: ELPS/ELD/ESOL, compliance files
   - Subject-Common: MLRs or literacy routines
   - Subject-District: Standards alignment

3. **Practice reading knowledge base files** (see [Section 3.5](#35-how-to-read-and-apply-knowledge-base-files))
   - Open one MLR file (if Math) or literacy routine (if ELA)
   - Read the protocol section
   - Note the examples

**Afternoon:**
4. **Study a complete example** (see [Section 4.5](#45-complete-example-works))
   - Read the complete lesson example
   - Notice how knowledge base guidance is applied
   - See how the 7 Quality Pillars show up

5. **Sketch a rough outline** for your assignment
   - Warm-up activity idea
   - Main instruction approach
   - Practice activities
   - Assessment ideas

**End of Day 2:** You can read knowledge base files and see how they apply to real content.

---

### Day 3-4: Drafting Content (6-8 hours total)

**Day 3 - Structure and First Draft:**
1. **Use templates from Section 4**
   - Copy template appropriate to your content type
   - Fill in header information
   - Draft lesson sequence or assessment items
   - Don't worry about perfection

2. **Apply knowledge base guidance as you go**
   - Reference MLR/literacy routine files
   - Include ELPS/ELD scaffolds
   - Add UDL supports
   - Note accessibility requirements

3. **Focus on substance over polish**
   - Complete all sections
   - Include placeholders for assets ("IMAGE: fraction circles")
   - Write answer keys

**Day 4 - Refine and Enhance:**
4. **Review and improve**
   - Read through with fresh eyes
   - Add missing scaffolds
   - Enhance differentiation
   - Complete all formative checks

5. **Check special requirements**
   - Review compliance files (SBOE, IPACC, etc.)
   - Verify standards alignment
   - Add alt text notes for images

**End of Day 4:** You have a complete first draft.

---

### Day 5: Self-Review and Submit (2-3 hours)

**Morning:**
1. **Run the Essential Checklist** (see Section 6)
   - Standards addressed
   - Learning objectives clear
   - Scaffolds for 3 EB levels
   - Alt text specified
   - Answer key complete

2. **Quick quality check**
   - Read aloud to check flow
   - Verify formulas/solutions correct
   - Check spelling and grammar
   - Format consistently

**Afternoon:**
3. **Prepare for submission**
   - Organize files in proper directory
   - Create metadata.json
   - Write clear commit message

4. **Submit for review** (see Section 7)
   - Create Git branch
   - Push to GitHub
   - Create pull request
   - Tag editor

5. **Take a break!** You've completed your first content piece.

**End of Week 1:** You've created and submitted your first piece of content. Now wait for editorial feedback (typically 3-5 business days).

---

### Week 1 Checklist

- [ ] Environment set up and working
- [ ] Content brief understood
- [ ] Curriculum config identified
- [ ] Knowledge base files gathered
- [ ] At least one KB file read and understood
- [ ] Example complete work reviewed
- [ ] Draft content created using templates
- [ ] All required components included
- [ ] Essential checklist completed
- [ ] Content submitted via pull request

### What to Expect Next

**Editorial Review (3-5 business days):**
- Editor will review against 8-section checklist
- Expect detailed feedback in PR comments
- Some revisions are normal (everyone gets feedback!)

**Your Response (1-2 days):**
- Address all feedback points
- Ask questions if unclear
- Make revisions
- Push updates to same branch

**Final Approval:**
- Editor approves and merges
- Content moves to /published/
- You receive next assignment!

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

## 3.5. How to Read and Apply Knowledge Base Files

### Overview

Knowledge base files contain specific guidance for your content. This section shows you **how to read** these files and **how to apply** what you learn.

### Anatomy of a Knowledge Base File

Most KB files follow this structure:

```
# [Title]
**[Subtitle]**
**Scope:** [Who uses this]
**Audience:** [Target users]

## Overview
[Purpose and benefits]

## Main Content Sections
[Detailed guidance]

## Examples
[Concrete examples]

## Resources
**Related Guides:** [Links]
```

### Step-by-Step: Reading an MLR File

**Example:** Let's read `/subjects/mathematics/common/mlr/mlr1-stronger-clearer.md`

**Step 1: Check the Header**
```markdown
# MLR1: Stronger and Clearer Each Time
**Math Language Routine for Refining Mathematical Communication**
**Scope:** Subject-Common (all math programs, all districts)
```

**What this tells you:**
- **Name:** MLR1 - I can reference this in my lesson
- **Purpose:** Helps students refine math communication
- **Scope:** Use this for any math lesson, any state

**Step 2: Read the Overview**
```markdown
## Overview

MLR1 provides a structured protocol for students to:
1. Articulate mathematical thinking verbally
2. Receive feedback from peers
3. Revise and clarify their explanations
4. Strengthen both language and mathematical understanding
```

**What this tells you:**
- This is a **verbal protocol** (students talk)
- It's **iterative** (students revise)
- It serves **dual purposes** (language + math)

**Step 3: Find the Protocol Section**
```markdown
## MLR1 Protocol (5-8 minutes per round)

**Round 1:** Student explains thinking to Partner A
**Round 2:** Partner A asks clarifying questions
**Round 3:** Student revises explanation for Partner B
**Round 4:** Partner B provides feedback
**Final:** Student produces written explanation
```

**What this tells you:**
- **Duration:** 5-8 minutes per round (plan ~20-30 min total)
- **Structure:** Specific steps to follow
- **Outcome:** Written explanation at end

**Step 4: Review Examples Section**
```markdown
## Grade 5 Example: Comparing Fractions

**Prompt:** "Explain why 3/4 is greater than 2/3"

**Round 1 (Student to Partner A):**
"3/4 is bigger because... um... 3 is closer to 4 than 2 is to 3."

**Round 2 (Partner A questions):**
"What do you mean by closer? Can you explain with a model?"

**Round 3 (Student revises for Partner B):**
"3/4 is greater because if I make both fractions have the same denominator,
3/4 becomes 9/12 and 2/3 becomes 8/12. 9/12 is greater."
```

**What this tells you:**
- Shows realistic student language (imperfect at first)
- Demonstrates how questioning improves explanations
- Gives you language you can use in your lesson

**Step 5: Check Scaffolds Section**
```markdown
## Scaffolds for Emergent Bilinguals

**Beginning:**
- Sentence frame: "_____ is greater/less than _____ because _____."
- Provide visual models to point to
- Allow use of L1 (first language) with partner

**Intermediate:**
- Sentence stems: "First I... Then I..."
- Encourage math vocabulary: numerator, denominator, equivalent
```

**What this tells you:**
- Specific sentence frames to include
- Visual supports needed
- How to differentiate by proficiency level

### Step-by-Step: Applying the Guidance

**Now write your lesson using what you learned:**

```markdown
### Guided Practice (20 minutes) - MLR1: Stronger and Clearer Each Time

**Objective:** Students will explain their comparison strategy for fractions.

**Prompt:** "Explain why 5/6 is greater than 3/4. Use a model or strategy."

**MLR1 Protocol:**

**Round 1 (3 minutes):** Partner A listens as student explains.
- Provide fraction bars as visual support
- Circulate and listen to explanations

**Round 2 (2 minutes):** Partner A asks:
- "Can you show me with the model?"
- "What strategy did you use?"
- "How do you know for certain?"

**Round 3 (3 minutes):** Student explains to Partner B with revisions.
- Listen for improved precision
- Note use of vocabulary (common denominator, equivalent fractions)

**Round 4 (2 minutes):** Partner B gives feedback:
- "I understood when you said..."
- "Can you clarify...?"

**Final (5 minutes):** Students write their explanation independently.

**EB Scaffolds:**
- **Beginning:** Sentence frame: "_____ is greater than _____ because _____."
                  Visual: Fraction bars available
- **Intermediate:** Sentence starter: "First I found... Then I compared..."
- **Advanced:** Encourage: "My strategy was... This works because..."

**Formative Check:** Collect written explanations. Look for:
- Correct comparison
- Clear strategy explained
- Math vocabulary used appropriately
```

**Notice how you applied the KB file:**
- ✅ Used MLR1 protocol structure
- ✅ Included timing from KB file
- ✅ Added scaffolds from KB file
- ✅ Adapted example to your specific content

### Common KB File Types and How to Use Them

#### Type 1: Standards Alignment Files
**Example:** `teks-math-alignment.md`

**Read for:**
- Standard code format
- Expected student performance
- Sample problems at grade level
- Vertical alignment (prior/next grades)

**Apply by:**
- Quoting standard codes in your lesson
- Matching rigor to exemplars
- Building on prerequisite knowledge

#### Type 2: Language Support Files
**Example:** `elps-alignment.md`

**Read for:**
- Proficiency level definitions
- Required scaffolds per level
- Sentence frames by domain
- Language functions

**Apply by:**
- Adding 3 levels of scaffolds to every activity
- Using provided sentence frames
- Noting which ELPS standards you address

#### Type 3: Framework Files
**Example:** `udl-principles-guide.md`

**Read for:**
- Principles (Representation, Action/Expression, Engagement)
- Specific strategies per principle
- Examples of implementation

**Apply by:**
- Ensuring at least 2 representations per concept
- Offering choice in how students demonstrate learning
- Connecting to students' interests

#### Type 4: Compliance Files
**Example:** `sboe-quality-rubric.md`

**Read for:**
- Specific requirements (e.g., "must include 5 formative checks")
- Forbidden content
- Quality indicators

**Apply by:**
- Checking your draft against requirements
- Documenting compliance in metadata

### When Files Seem to Conflict

**Scenario:** MLR file says "5-8 minutes" but your lesson is only 45 minutes total, and you need to use 3 MLRs.

**Resolution:**
1. **Prioritize the core activity** - Maybe use full MLR1 (20 min) in guided practice
2. **Adapt others** - Use abbreviated versions of MLR2 and MLR8 (5 min each)
3. **Document your choice** - Note in lesson: "Abbreviated MLR2 due to time constraints"
4. **Ask if unsure** - Tag curriculum lead in PR: "Please review my MLR timing"

**General Rule:** Apply the spirit of the guidance. Adapt thoughtfully when needed.

### Quick Reference: Where to Find What

| Need | File Location | What to Read |
|------|---------------|--------------|
| Math instruction routine | `/subjects/mathematics/common/mlr/*.md` | Protocol + Examples |
| ELA instruction routine | `/subjects/ela/common/literacy-routines/*.md` | Protocol + Examples |
| Language scaffolds | `/districts/[state]/language/*.md` | Proficiency levels + Frames |
| Accessibility | `/universal/accessibility/*.md` | Requirements + Checklist |
| Cultural responsiveness | `/universal/content-equity/ceid-guidelines.md` | 11 categories + Examples |
| Standards | `/subjects/[subject]/districts/[state]/*.md` | Code format + Exemplars |
| Compliance | `/districts/[state]/compliance/*.md` | Requirements + Checklist |
| UDL | `/universal/frameworks/udl-*.md` | Principles + Strategies |

---

## 3.6. Cross-Subject Example: California ELA

Let's walk through a California ELA example to show how the process differs from Math.

### The Assignment

**Content Brief (abbreviated):**
```yaml
project: HMH Into Reading California Edition - Grade 3
content_type: Lesson
curriculum_config: hmh-ela-ca.json

standards:
  primary: CCSS.ELA-LITERACY.RL.3.2 (Recount stories, determine central message)
  supporting: CA ELD.PI.3.6 (Connecting ideas)

learning_objectives:
  - Students will recount the key events of a story in sequence
  - Students will determine the central message using text evidence
  - Students will connect ideas using transition words

duration: 60 minutes
routine: Close Reading Protocol
```

### Step 1: Identify Config

Brief says "Into Reading California Edition" → **Config:** `hmh-ela-ca.json`

### Step 2: Review Resolution Order

Open `/config/curriculum/hmh-ela-ca.json`:

```json
{
  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge-v2/subjects/ela/districts/california/into-reading/",
      "/reference/hmh-knowledge-v2/subjects/ela/districts/california/",
      "/reference/hmh-knowledge-v2/subjects/ela/common/",
      "/reference/hmh-knowledge-v2/districts/california/",
      "/reference/hmh-knowledge-v2/publishers/hmh/",
      "/reference/hmh-knowledge-v2/universal/"
    ]
  }
}
```

### Step 3: Gather Knowledge Files

**For California Grade 3 ELA Lesson on Central Message:**

**Universal (7 files):**
- `universal/frameworks/udl-principles-guide.md`
- `universal/frameworks/dok-framework.md`
- `universal/frameworks/eb-scaffolding-guide.md`
- `universal/frameworks/sentence-frames-library.md`
- `universal/accessibility/wcag-compliance-guide.md`
- `universal/content-equity/ceid-guidelines.md`
- `universal/assessment/item-types-reference.md`

**District-Wide California (2 files):**
- `districts/california/language/eld-alignment.md`
- `districts/california/compliance/california-adoption-criteria.md`

**Subject-Common ELA (5 files):**
- `subjects/ela/common/literacy-routines-overview.md`
- `subjects/ela/common/literacy-routines/close-reading-protocol.md`
- `subjects/ela/common/literacy-routines/think-pair-share.md`
- `subjects/ela/common/literacy-routines/turn-and-talk.md`
- `subjects/ela/common/literacy-routines/annotation-protocol.md`

**Subject-District California ELA (would need - currently missing per INCOMPLETE_ANALYSIS.md):**
- `subjects/ela/districts/california/ccss-ela-alignment.md` (to be created)

**Total:** ~14 files (note: 1 fewer than Math because CA ELA subject-district file is missing)

### Step 4: Read and Apply ELA-Specific Files

**Reading Close Reading Protocol File:**

Key sections:
- **Protocol Structure:** 3 reads with different purposes
- **Text Selection Criteria:** Complex enough for multiple reads
- **Questioning Strategies:** Text-dependent questions
- **Annotation Strategies:** Mark key details, connections

**Reading ELD Alignment File:**

Key sections:
- **ELD Standards:** Part I (Interacting), Part II (How English Works), Part III (Foundational Literacy)
- **Proficiency Levels:** Emerging, Expanding, Bridging
- **Scaffolds:** Sentence frames for literary analysis

### Step 5: Apply to Your Lesson

**Abbreviated Lesson Excerpt:**

```markdown
# Determining Central Message in Folk Tales
**Grade:** 3 | **Subject:** ELA | **Duration:** 60 minutes
**Standards:** CCSS.ELA-LITERACY.RL.3.2, CA ELD.PI.3.6
**Text:** "The Lion and the Mouse" (Aesop's Fable)

## Lesson Sequence

### First Read (15 minutes) - Close Reading Protocol: Read for Gist

**Purpose:** Understand the basic story

**Teacher reads aloud:** (students follow along)

**After reading, Think-Pair-Share:**
- "What happened in this story? Turn and tell your partner."

**CA ELD Scaffolds** (from eld-alignment.md):
- **Emerging:** Sentence frame: "First, the ___. Then, the ___."
                  Provide story sequence cards to arrange
- **Expanding:** Sentence frame: "The story is about a ___ who ___."
- **Bridging:** Encourage: "The main events were..."

**Formative Check:** Students share key events in sequence.

---

### Second Read (15 minutes) - Close Reading Protocol: Read for Key Details

**Purpose:** Identify important details about characters' actions

**Students read independently** with annotation:
- Underline: What the lion does
- Circle: What the mouse does
- Star: How each character helps the other

**After reading, Turn-and-Talk:**
- "What did you notice about how the characters treated each other?"

**CA ELD Scaffolds:**
- **Emerging:** Provide sentence frames + visual storyboard
- **Expanding:** "I noticed that the mouse ___. This shows ___."
- **Bridging:** "The author shows that..."

---

### Third Read (15 minutes) - Close Reading Protocol: Read for Central Message

**Purpose:** Determine what the author wants us to learn

**Guided discussion:**
Teacher: "Why do you think the author wrote this story?
What lesson or message can we learn?"

**Think-Pair-Share → Whole Class Discussion**

**CA ELD Scaffolds:**
- **Emerging:** Choose from 2-3 pre-written messages (with pictures)
- **Expanding:** "The central message is ___. I know this because ___."
- **Bridging:** "The author's message is... This is important because..."

**Anchor Chart:** Class co-constructs central message

---

### Independent Application (10 minutes)

**Task:** Write 3-4 sentences explaining the central message with evidence.

**Success Criteria:**
- State the message clearly
- Use at least 2 examples from text
- Use transition words (First, Also, This shows)

**Differentiation:**
- **Emerging:** Sentence frames + word bank + story pictures
- **Expanding:** Sentence starters provided
- **Bridging:** Open response with vocabulary suggestions
```

### Key Differences from Math Example

| Aspect | Math (TX) | ELA (CA) |
|--------|-----------|----------|
| **Routines** | MLRs (8 total) | Literacy Routines (4 total) |
| **Language Standards** | ELPS (TX) | ELD (CA) |
| **Focus** | Precision in explanation | Text evidence, interpretation |
| **Materials** | Manipulatives, visuals | Texts, annotation tools |
| **Scaffolds** | Visual models, sentence frames | Frames, word banks, text supports |

### Similarities Across Subjects

- **Same Universal Files:** UDL, DOK, WCAG, CEID all apply
- **Same Structure:** Warm-up → Instruction → Practice → Closure
- **Same 7 Quality Pillars:** Every subject must meet all 7
- **Same Process:** Read KB files → Apply guidance → Self-review → Submit

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

## 4.5. Complete Example Works

**New to authoring?** This section shows you what **finished, approved** content looks like.

### Example 1: Complete Approved Lesson

**Grade 5 Texas Math: Comparing Fractions**

```markdown
# Comparing Fractions Using Benchmarks
**Grade:** 5 | **Subject:** Mathematics | **Duration:** 60 minutes
**Standards:** TEKS.5.3.H (Represent and compare fractions), ELPS.3.E (Share information)
**Learning Objectives:**
- Students will compare fractions with unlike denominators using benchmark fractions (0, 1/2, 1)
- Students will justify comparisons using visual models and mathematical reasoning
- Students will explain comparison strategies using precise mathematical language

## Lesson Overview
Students learn to compare fractions by reasoning about their relationship to benchmark
fractions (0, 1/2, 1), then use this strategy to solve comparison problems with
visual models and mathematical justification.

## Materials
**Teacher Materials:**
- Chart paper for anchor chart
- Document camera
- Fraction strips (wholes, halves, thirds, fourths, fifths, sixths, eighths, tenths, twelfths)

**Student Materials:**
- Fraction strips (1 set per student)
- Comparison recording sheet
- Number lines (0 to 1, marked in halves)

**Technology/Manipulatives:**
- Digital fraction tool (optional, for visual support)

## Preparation
- Pre-cut fraction strips or prepare digital version
- Create anchor chart template "Benchmark Comparison Strategies"
- Pre-select 3 student strategies to share during summary
- Review common misconceptions (see below)

## Lesson Sequence

### Warm-Up (10 minutes) - MLR8: Discussion Supports
**Objective:** Activate prior knowledge of benchmark fractions

**Prompt (display):** "Is 3/8 closer to 0, 1/2, or 1? How do you know?"

**Think Time:** 1 minute (silent think time)
**Turn-and-Talk:** 2 minutes (students share with partner)

**Whole Class Share:** Call on 3-4 students to share reasoning

**MLR8 Discussion Supports:**
- Display sentence frame: "I think ___ is closer to ___ because ___."
- Revoice: "So you're saying that..."
- Press for details: "Can you show that with the fraction strips?"

**✓ Pillar 2 - Pedagogical Soundness:** Gradual release begins with activating prior knowledge
**✓ Pillar 3 - Language Support:** MLR8 provides structured discussion support

**Scaffolds for Emergent Bilinguals:**
- **Beginning:** Provide 3 fraction strips (3/8, 0, 1/2, 1) to physically compare
                  Sentence frame: "3/8 is close to ___."
- **Intermediate:** Sentence frame: "I think ___ because when I look at ___."
- **Advanced:** Encourage: "I can prove this by..."

**Accessibility Notes:**
- Enlarged number line for students with visual needs
- Tactile fraction strips available
- Audio description: "Three-eighths on a number line marked with 0, one-half, and 1"

**Formative Check:**
- Listen for: students identify 3/8 is closer to 1/2 than 0 or 1
- Note misconceptions for addressing in instruction

---

### Instruction (20 minutes) - MLR7: Compare and Connect
**Objective:** Learn systematic strategy for comparing fractions using benchmarks

**Teacher Models:** "Let's compare 2/5 and 5/8. I'll show you my strategy."

**Think-Aloud:**
"First, I'll think about 2/5. Is it close to 0, 1/2, or 1?
Well, 2 out of 5 pieces... half of 5 would be 2.5, so 2/5 is less than half.
Let me mark it on my number line. [Marks just left of 1/2]

Now 5/8. Is it close to 0, 1/2, or 1?
5 out of 8 pieces... half of 8 is 4, so 5/8 is more than half.
Let me mark it. [Marks just right of 1/2]

Now I can see that 2/5 < 1/2 < 5/8, so 2/5 < 5/8."

**Visual Support:** Display fraction strips and number line simultaneously

**✓ Pillar 1 - Standards Alignment:** Directly teaches TEKS.5.3.H using benchmark reasoning
**✓ Pillar 4 - UDL:** Multiple representations (verbal, visual models, number line)

**Check for Understanding:**
"Thumbs up if you followed my reasoning. Thumbs sideways if you're a little confused."

**Model Second Example:** 7/10 and 2/3 (students guide teacher)
"Talk me through the steps. What should I think about first?"

**Anchor Chart:** Co-construct with students:
```
Comparing Fractions with Benchmarks
1. Look at first fraction - Is it close to 0, 1/2, or 1?
2. Look at second fraction - Is it close to 0, 1/2, or 1?
3. Compare their positions
4. Write comparison with symbol (<, >, =)
5. Explain your reasoning
```

**Common Misconceptions:**
- **"Bigger denominator = bigger fraction"**: Address by showing 1/8 < 1/3
  "Denominators tell us the SIZE of pieces, not the AMOUNT"

- **"Just use common denominator every time"**: Validate as strategy, but show
  benchmarks are faster: "Both strategies work! Benchmarks save time."

**✓ Pillar 2 - Pedagogical Soundness:** Addresses misconceptions proactively

**Scaffolds for Emergent Bilinguals:**
- **Beginning:** Provide partially completed anchor chart with visuals
                  Use manipulatives alongside every example
- **Intermediate:** Sentence frames: "First I look at ___. This fraction is close to ___."
- **Advanced:** Encourage comparison language: "whereas," "however," "on the other hand"

---

### Guided Practice (20 minutes) - MLR1: Stronger and Clearer Each Time
**Objective:** Students apply benchmark strategy with feedback

**Task (display):**
"Compare these fraction pairs using benchmarks. Explain your reasoning.
1. 4/9 and 5/6
2. 1/8 and 2/5
3. 7/12 and 3/5"

**Round 1 (5 minutes):** Students work individually, record thinking

**Round 2 (8 minutes):** MLR1 Protocol
- Partner A shares solution for #1
- Partner B asks: "How did you decide where each fraction was?"
                  "Can you show me with the fraction strips?"
- Partner A revises explanation
- Switch roles for #2

**✓ Pillar 2 - Pedagogical Soundness:** MLR1 supports mathematical communication refinement
**✓ Pillar 3 - Language Support:** Structured language protocol with sentence frames

**Circulate and Monitor:**
Listen for:
- Correct benchmark identification
- Logical reasoning
- Use of academic vocabulary
- Peer questioning

**Questions to ask:**
- "How did you decide that fraction was close to 1/2?"
- "Could you use a different strategy? Would it work?"
- "What if the numerator was one more? Would your answer change?"

**Round 3 (7 minutes):** Share-out and discussion
Select 3 students with different representations:
- Student 1: Used fraction strips
- Student 2: Used number line
- Student 3: Used reasoning about half without model

**MLR7: Compare and Connect:** "What's the same about these strategies? What's different?"

**✓ Pillar 4 - UDL:** Multiple means of action/expression (students choose representations)

**Formative Check:** Review student recording sheets
- 80%+ should correctly compare all 3 pairs
- If < 80%, address whole-class before independent practice

---

### Independent Practice (10 minutes)
**Objective:** Individual application and assessment

**Task (handout):**
1. Compare 5 fraction pairs using benchmarks
2. Choose 2 pairs: draw models to justify
3. Write 2-3 sentences explaining your strategy

**Differentiation:**
- **Below Grade Level:**
  - Provide number lines with benchmarks pre-marked
  - Only 3 fraction pairs
  - Sentence frames provided

- **On Grade Level:**
  - All 5 pairs
  - Choice of models

- **Above Grade Level:**
  - Include three-fraction comparisons (e.g., order 3/5, 7/8, 2/9)
  - Challenge: "Find 3 fractions between 1/2 and 1"

**✓ Pillar 4 - UDL:** Multiple means of engagement through differentiation

**Scaffolds for Emergent Bilinguals:**
- **Beginning:** Pre-drawn models to label, word bank, sentence frames
- **Intermediate:** Partially completed sentences, word bank
- **Advanced:** Open response with vocabulary reference

---

### Closure (5 minutes) - Exit Ticket
**Objective:** Assess individual understanding

**Exit Ticket (individual, written):**
1. Compare 3/10 and 4/5 using benchmarks. Show your thinking.
2. Explain why benchmark fractions are helpful for comparing.

**Collection:** Students submit as they leave

**Success Criteria Display:**
"Today I can:
✓ Compare fractions using 0, 1/2, 1 as benchmarks
✓ Explain my reasoning with models
✓ Use math language to justify comparisons"

**Reflection Prompt:** "What benchmark strategy will you remember?"

---

## Differentiation

### Emergent Bilinguals
**Beginning:**
- Visual fraction models for every problem
- Sentence frames for all responses
- Word bank with academic vocabulary + visuals
- Partner with intermediate/advanced speaker
- Extended time

**Intermediate:**
- Sentence starters
- Partially completed anchor chart as reference
- Access to digital fraction tools
- Encourage elaboration: "Say more about that"

**Advanced:**
- Comparison language structures
- Academic vocabulary extensions (equivalent, magnitude, proximity)
- Leadership roles in group discussions

**✓ Pillar 3 - Language Support:** Scaffolds for all 3 proficiency levels per ELPS

### By Readiness Level
**Below Grade Level:**
- Pre-marked number lines
- Fewer problems (focus on mastery)
- Fraction strips available throughout
- Check-in after guided practice

**On Grade Level:**
- Choice of tools
- All core problems
- Standard expectations

**Above Grade Level:**
- Three-fraction comparisons
- Challenge problems (find fractions between benchmarks)
- Explore fractions close to 1/3 and 2/3 as additional benchmarks

### Special Needs
- Enlarged manipulatives and number lines
- Graph paper for organizing work
- Assistive technology as per IEP
- Alternative response formats (oral explanation, video)

**✓ Pillar 4 - UDL:** Multiple means of representation, action/expression, engagement

## Assessment

### Formative Checks Throughout Lesson
- **Warm-up:** Can students place fraction relative to benchmarks? (observation)
- **Instruction:** Thumbs up/sideways check, call on non-volunteers
- **Guided Practice:** Circulate, review recording sheets (80%+ accuracy target)
- **Independent Practice:** Review work, note students needing intervention
- **Closure:** Exit tickets (will score to plan tomorrow's lesson)

### Success Criteria
Students demonstrate success when they can:
- Identify whether a fraction is close to 0, 1/2, or 1
- Compare two fractions by reasoning about their relationship to benchmarks
- Justify comparisons using visual models (strips, number lines, or area models)
- Explain reasoning using mathematical language

**✓ Pillar 2 - Pedagogical Soundness:** Formative assessment throughout, aligned to objectives

## Answer Key

**Guided Practice:**
1. 4/9 and 5/6:  4/9 is less than 1/2 (half would be 4.5/9), 5/6 is close to 1 (one more piece)
   So 4/9 < 5/6

2. 1/8 and 2/5:  1/8 is close to 0, 2/5 is close to 1/2
   So 1/8 < 2/5

3. 7/12 and 3/5:  7/12 is greater than 1/2 (half is 6/12), 3/5 is greater than 1/2 (half is 2.5/5)
   Both greater than 1/2; 7/12 is barely over, 3/5 is a bit over
   Need closer look: 7/12 vs 3/5... could use common denominator (35/60 vs 36/60)
   Or: 7/12 is 1 piece away from 8/12 (which = 2/3), 3/5 is 2 pieces away from 5/5
   So 7/12 < 3/5

**Independent Practice:** [Full solutions with visual models]

**Exit Ticket Exemplar:**
"3/10 is less than 1/2 because half of 10 is 5, and I only have 3 pieces.
4/5 is close to 1 because I only need 1 more piece.
So 3/10 < 4/5.
Benchmarks help because I don't have to find a common denominator every time."

**✓ Pillar 1 - Standards Alignment:** All problems and solutions align to TEKS.5.3.H

---

## Assets Needed
- **Image 1**: Fraction strips set (wholes through twelfths) - 1200x800px, alt text provided
- **Image 2**: Number line 0 to 1 with benchmarks marked - 1200x400px, alt text provided
- **Image 3**: Visual of 3/8 on number line with benchmarks - 800x400px, alt text provided

**✓ Pillar 5 - Accessibility:** Alt text specified for all images per WCAG 2.1 AA

---

## Metadata
**Curriculum:** hmh-math-tx
**KB Files Used:** 18 files
- Universal: UDL, DOK, EB Scaffolding, Sentence Frames, WCAG, CEID
- Math Common: MLR1, MLR7, MLR8, Vocab Guidelines
- District-Wide TX: ELPS Alignment, SBOE Rubric, IPACC
- Subject-District: TEKS Math Alignment (Grade 5)
- Subject-Common Math: Problem-Solving Framework, Misconceptions

**Review Notes:**
"Strong alignment to TEKS.5.3.H and ELPS.3.E. MLR protocols correctly applied.
Three-tiered EB scaffolds comprehensive. Misconceptions addressed. UDL evident
throughout. All 7 quality pillars met. APPROVED." - Editor, 2025-11-04

**✓ Pillar 6 - Cultural Responsiveness:** Neutral context, diverse names, no stereotypes
**✓ Pillar 7 - State Compliance:** Meets Texas SBOE standards for math instructional materials
```

---

### Example 2: Complete Approved Assessment

**Grade 5 Texas Math: Unit Assessment - Fractions Operations**

```markdown
# Unit 4 Assessment: Fraction Operations
**Grade:** 5 | **Subject:** Mathematics | **Duration:** 45 minutes
**Standards:** TEKS.5.3.H, TEKS.5.3.K, TEKS.5.3.I
**Total Points:** 24
**Item Count:** 12 items (8 MC, 3 SCR, 1 ECR)

## Blueprint

| Standard | Items | Points | DOK Distribution |
|----------|-------|--------|------------------|
| TEKS.5.3.H (Compare) | 4 | 8 | DOK 1: 1, DOK 2: 2, DOK 3: 1 |
| TEKS.5.3.K (Add/Sub) | 5 | 10 | DOK 1: 1, DOK 2: 3, DOK 3: 1 |
| TEKS.5.3.I (Represent) | 3 | 6 | DOK 2: 2, DOK 3: 1 |

**✓ Pillar 1 - Standards Alignment:** Blueprint maps items to standards with DOK levels

---

## Multiple Choice Items

### Item 1
**Standard:** TEKS.5.3.H | **DOK:** 1 | **Points:** 2 | **Correct:** C

**Stimulus:**
Which symbol makes the comparison true?

3/5 ___ 2/3

**Options:**
A. <
B. =
C. > ← CORRECT
D. Cannot be determined

**Rationale:**
- Option A: Incorrect - Students may have compared numerators only (3 > 2, but didn't consider denominators)
- Option B: Incorrect - Not equivalent fractions
- Option C: CORRECT - Using benchmarks: 3/5 is greater than 1/2 (half = 2.5/5), 2/3 is greater than 1/2 (half = 1/3), but 3/5 is 2 pieces away from whole, 2/3 is 1 piece away. OR common denominator: 9/15 < 10/15
- Option D: Incorrect - All fractions can be compared

**Alt Text:** "Mathematical comparison with two fractions and four answer choices."

**EB Scaffolds:**
- Beginning: Provide fraction strips to physically compare
- Intermediate: "First, I compare each to ___."

**✓ Pillar 3 - Language Support:** EB scaffolds for Beginning and Intermediate
**✓ Pillar 5 - Accessibility:** Alt text provided

---

### Item 2
**Standard:** TEKS.5.3.K | **DOK:** 2 | **Points:** 2 | **Correct:** B

**Stimulus:**
Keisha has 3/4 of a pizza. She eats 1/3 of what she has.
How much of the whole pizza did Keisha eat?

**Options:**
A. 2/7 of the pizza
B. 1/4 of the pizza ← CORRECT
C. 4/7 of the pizza
D. 1/3 of the pizza

**Rationale:**
- Option A: Incorrect - Subtracted 3/4 - 1/3 (incorrect operation and execution)
- Option B: CORRECT - 1/3 of 3/4 means multiply: 1/3 × 3/4 = 3/12 = 1/4
- Option C: Incorrect - Added 3/4 + 1/3 (incorrect operation)
- Option D: Incorrect - Misunderstood "of what she has" vs "of the whole"

**Alt Text:** "Word problem about fractions of pizza."

**EB Scaffolds:**
- Beginning: Provide visual of pizza divided into fourths, with 3 pieces shaded. Show "1/3 of the shaded part"
- Intermediate: "I need to find 1/3 of ___."

**✓ Pillar 2 - Pedagogical Soundness:** Tests conceptual understanding, not just computation

---

[Items 3-8: Additional MC items following same format]

---

## Short Constructed Response Items

### Item 9
**Standard:** TEKS.5.3.K | **DOK:** 3 | **Points:** 3

**Prompt:**
Marcus says that 2/3 + 3/4 = 5/7 because "you just add the tops and add the bottoms."

Explain why Marcus's method doesn't work. Then show the correct solution.

**Rubric:**
**3 points:**
- Clearly explains why adding numerators and denominators is incorrect (need same-size pieces)
- Shows correct solution using common denominator (8/12 + 9/12 = 17/12 or 1 5/12)
- Work is organized and complete

**2 points:**
- Adequately explains error
- Correct answer with minor work errors OR incomplete explanation

**1 point:**
- Partially explains error
- Significant errors in solution

**0 points:**
- No response or completely incorrect

**Sample Student Response (3 points):**
"Marcus's method doesn't work because fractions have to have the same denominator
before you can add them. The denominator tells you the size of the pieces, and you
can't add different-size pieces. You need to find a common denominator first.

The correct way:
2/3 = 8/12 (multiply by 4/4)
3/4 = 9/12 (multiply by 3/3)
8/12 + 9/12 = 17/12 = 1 5/12

The correct answer is 1 5/12, not 5/7."

**✓ Pillar 1 - Standards Alignment:** DOK 3 item requires explaining and correcting misconception
**✓ Pillar 2 - Pedagogical Soundness:** Addresses common error in meaningful way

**EB Scaffolds:**
- Beginning: Sentence frames: "Marcus is wrong because ___. The right way is ___."
              Provide partially completed visual models
- Intermediate: Sentence starters: "First, I need to... Next, I... The answer is..."
- Advanced: Encourage mathematical language: "whereas," "in contrast," "the error occurs when"

---

### Item 10
**Standard:** TEKS.5.3.I | **DOK:** 2 | **Points:** 2

**Prompt:**
Draw a visual model to represent 2/3 + 1/6. Then write the sum.

**Rubric:**
**2 points:**
- Accurate visual model (area model, number line, or fraction strips)
- Correct sum (5/6 or equivalent)
- Model clearly shows combining

**1 point:**
- Model attempted but has minor errors OR
- Correct sum but model unclear

**0 points:**
- No model or completely incorrect

**Exemplar:** [Visual showing two area models: 2/3 shaded in one bar, 1/6 in another,
             combined into single bar showing 5/6]

**✓ Pillar 4 - UDL:** Students choose representation type

---

### Item 11
**Standard:** TEKS.5.3.H | **DOK:** 3 | **Points:** 2

[Additional SCR item]

---

## Extended Constructed Response

### Item 12
**Standard:** TEKS.5.3.K, TEKS.5.3.H | **DOK:** 3 | **Points:** 4

**Prompt:**
The Martinez family is painting their fence. On Monday, they painted 3/8 of the fence.
On Tuesday, they painted 1/4 more.

Part A: What fraction of the fence have they painted after Tuesday? Show your work.

Part B: How much more of the fence do they still need to paint? Show your work.

Part C: If they want to finish the fence on Wednesday, is it reasonable to paint the
        rest in one day? Explain why or why not using your answers from Parts A and B.

**Rubric:**
**4 points:**
- Part A: Correct sum (5/8) with clear work showing common denominator
- Part B: Correct difference (3/8) with clear work
- Part C: Reasonable conclusion with mathematical justification
  (e.g., "Yes, because 3/8 is less than half, which is less than they painted on Monday")
- All work organized, complete, and mathematically accurate

**3 points:**
- Parts A and B correct
- Part C lacks complete justification OR minor calculation error in one part

**2 points:**
- One part completely correct
- Other parts attempted with some correct reasoning

**1 point:**
- Minimal correct work
- Some understanding of concepts shown

**0 points:**
- No response or no correct work

**Sample Student Response (4 points):**
"Part A:
3/8 + 1/4
= 3/8 + 2/8  (1/4 = 2/8)
= 5/8
They painted 5/8 of the fence.

Part B:
1 whole - 5/8
= 8/8 - 5/8
= 3/8
They still need to paint 3/8.

Part C:
Yes, it's reasonable to finish on Wednesday. They need to paint 3/8, which is
less than 1/2. On Monday they painted 3/8 in one day, so they can definitely
do it again. Also, 3/8 is less than what they painted on Monday (3/8) and way
less than they did in two days (5/8)."

**✓ Pillar 1 - Standards Alignment:** Multi-part item integrates multiple standards
**✓ Pillar 2 - Pedagogical Soundness:** Real-world context, multi-step reasoning

**EB Scaffolds:**
- Beginning: Provide visual fence diagram with sections marked
              Sentence frames for each part
              Word bank: sum, difference, whole, reasonable, less than, more than
- Intermediate: Partially completed visual
                 Sentence starters for Part C
- Advanced: Encourage comparison and justification language

**✓ Pillar 6 - Cultural Responsiveness:** Neutral family context, common household task

---

## Answer Key

**Multiple Choice:**
1. C | 2. B | 3. [C] | 4. [A] | 5. [D] | 6. [B] | 7. [A] | 8. [C]

**Constructed Response:**
9. See rubric and exemplar above - 3 points
10. See rubric and exemplar above - 2 points
11. [Answer] - 2 points
12. See rubric and exemplar above - 4 points

**Total Possible:** 24 points

**Grading Scale:**
- 22-24 points: Mastery (A)
- 19-21 points: Proficient (B)
- 16-18 points: Developing (C)
- 13-15 points: Beginning (D)
- 0-12 points: Insufficient Evidence (F)

**Scoring Notes:**
- Use rubrics consistently
- Award partial credit per rubric guidance
- If student shows correct reasoning but calculation error, award partial credit
- For CR items, focus on mathematical thinking, not just answer

**✓ Pillar 2 - Pedagogical Soundness:** Clear scoring criteria, partial credit for reasoning

---

## Administration Guidelines

**Timing:** 45 minutes standard, extended time per IEP/504

**Materials Permitted:**
- Scratch paper
- Fraction manipulatives (optional for items 1-8)
- Bilingual dictionary (for ELL students)

**Accommodations:**
- Read-aloud (items may be read to students per IEP)
- Extended time (time and a half)
- Separate setting
- Responses may be scribed or dictated

**✓ Pillar 5 - Accessibility:** Accommodations specified per WCAG and IEP requirements

---

## Metadata
**Curriculum:** hmh-math-tx
**Unit:** 4 - Fraction Operations
**Item Count:** 12 (8 MC, 3 SCR, 1 ECR)
**Points:** 24
**Duration:** 45 minutes

**KB Files Referenced:** 8 files
- Universal: Assessment Item Types, Rubric Design, Answer Key Formatting
- Math Common: Common Misconceptions, Problem-Solving Framework
- District TX: TEKS Math Grade 5, ELPS, SBOE Item Requirements

**Review Notes:**
"Blueprint aligns to TEKS with appropriate DOK distribution. Items test conceptual
understanding and procedural fluency. Rubrics clear and scorable. EB scaffolds present.
All accessibility requirements met. APPROVED." - Assessment Specialist, 2025-11-05

**✓ Pillar 7 - State Compliance:** Meets Texas assessment item format and rigor requirements
```

---

### What Makes These Examples "Approved"?

Both examples demonstrate all 7 Quality Pillars:

**✓ Pillar 1 - Standards Alignment:** Every objective and item explicitly maps to standards (TEKS, ELPS)
**✓ Pillar 2 - Pedagogical Soundness:** Evidence-based routines (MLRs), gradual release, formative assessment, misconceptions addressed
**✓ Pillar 3 - Language Support:** Three-tiered EB scaffolds (Beginning/Intermediate/Advanced) throughout
**✓ Pillar 4 - UDL:** Multiple representations, student choice, differentiation by readiness
**✓ Pillar 5 - Accessibility:** Alt text for images, accommodations specified, WCAG compliant
**✓ Pillar 6 - Cultural Responsiveness:** Neutral contexts, diverse names, no stereotypes
**✓ Pillar 7 - State Compliance:** Meets Texas SBOE/ELPS requirements

---

### Use These Examples When:

- **Starting your first lesson**: Reference structure, section headings, level of detail
- **Applying an MLR**: See how MLR1, MLR7, MLR8 are implemented in context
- **Writing EB scaffolds**: Note the specificity for each proficiency level
- **Creating assessments**: Study item format, rubrics, rationales
- **Self-reviewing**: Compare your draft to these approved examples against 7 Pillars
- **Uncertain about detail level**: These show the expected depth and completeness

**Remember:** Your content doesn't need to be identical in structure, but should meet the same quality standards demonstrated here.

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

**How to Check:**
1. **List all standards explicitly** at the top of your document
2. **Open the standards KB file** (e.g., `/subjects/mathematics/districts/texas/teks-math-alignment.md`)
3. **Find your standard** and read the full description and expectations
4. **Compare your objective verbs** to the standard's verb (e.g., if standard says "justify," your objective should say "justify," not "explain")
5. **Check vertical alignment**: Read the grade-level-before and grade-level-after standards to ensure your content bridges appropriately
6. **Verify assessment alignment**: Each assessment item should test the standard, not just related content

**Checklist:**
- [ ] All standards from brief listed at top of document
- [ ] Each learning objective explicitly maps to a standard
- [ ] Reviewed standards KB file for depth and rigor expectations
- [ ] Verified rigor matches standard intent (DOK level appropriate)
- [ ] Checked vertical alignment (builds on prior grade, prepares for next)

**Reference:** `/subjects/[subject]/districts/[state]/[standards-file].md`

#### 2. Pedagogical Soundness

**Requirements:**
- Research-based practices
- Gradual release (I do, We do, You do)
- Formative assessment throughout
- Addresses misconceptions
- Sufficient practice

**How to Check:**
1. **Check lesson structure**: Does it follow Warm-up → Instruction (I do) → Guided Practice (We do) → Independent Practice (You do) → Closure?
2. **Verify instructional routine application**: Open the MLR/literacy routine KB file you're using. Does your lesson match the protocol steps? Are you using the routine correctly or just mentioning it?
3. **Count formative checks**: Are there check-ins every 10-15 minutes? (45-min lesson = 3+ checks, 60-min = 4+ checks)
4. **Look for misconceptions**: Did you include at least one common misconception and how to address it? Check subject-common KB files for typical misconceptions.
5. **Check representations**: Count how many different representations you use (visual models, verbal, symbolic, physical). Minimum 2 per key concept.
6. **Compare to approved example**: Does your lesson have similar depth and structure to Section 4.5 examples?

**Checklist:**
- [ ] Includes modeling, guided practice, independent practice
- [ ] Instructional routine applied correctly (checked against KB file protocol)
- [ ] Multiple representations (concrete, representational, abstract)
- [ ] Formative checks every 10-15 min
- [ ] At least one common misconception identified and addressed

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

**How to Check:**
1. **Search your document for "Beginning," "Intermediate," "Advanced"** - Do you have all three levels? Are they in multiple sections (not just one place)?
2. **Check scaffold specificity**: Are your scaffolds specific enough? Compare to Section 4.5 examples. Generic = "Provide scaffolds." Specific = "Sentence frame: 'I think ___ because ___.'"
3. **Count sentence frames**: Do you have at least 3-5 actual sentence frames written out (not just "provide sentence frames")?
4. **Open the language KB file** (ELPS/ELD/ESOL) and verify you've referenced the appropriate standards from your brief
5. **Check visuals**: For each key vocabulary word or concept, is there a visual support? (model, diagram, graphic, real object, gesture)
6. **Test with this question**: Could a teacher who's never worked with emergent bilinguals use your scaffolds successfully, or would they need to guess?

**Checklist:**
- [ ] ELPS/ELD/ESOL standards explicitly referenced
- [ ] Scaffolds for all 3 proficiency levels (Beginning/Intermediate/Advanced)
- [ ] At least 3 specific sentence frames written out
- [ ] Visual supports identified for key concepts
- [ ] Scaffolds are specific enough (not generic "provide support")

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

**How to Check:**
1. **Check representations (Principle 1)**: For each key concept, count representations. Minimum 2. Examples: visual model + verbal explanation, manipulative + diagram, text + video
2. **Check action/expression options (Principle 2)**: Do students have choice in how they show learning? Examples: "Draw OR write," "Use fraction strips OR number line," "Explain verbally OR in writing"
3. **Check engagement (Principle 3)**: Is there variety in activity types? Examples: Individual → Partner → Whole class. Different problem types (real-world, abstract, puzzles)
4. **Look for differentiation**: Do you offer Below/On/Above grade level options? Are there multiple entry points?
5. **Ask**: If you removed one representation or activity, could all students still access the content? If no, you don't have enough options.

**Checklist:**
- [ ] At least 2 representations for each key concept
- [ ] Student choice in at least one section (action/expression)
- [ ] Variety in activity types and groupings (engagement)
- [ ] Differentiation by readiness level provided
- [ ] Compared to UDL principles in KB file

**Reference:** `/universal/frameworks/udl-principles-guide.md`

#### 5. Accessibility (WCAG 2.1 AA)

**Requirements:**
- All images have alt text
- Color contrast ≥ 4.5:1 (normal text), ≥ 3:1 (large text)
- Keyboard navigable
- Text selectable and scalable
- No flashing content

**How to Check:**
1. **Count images, count alt text**: Every image placeholder must have alt text specified. Format: `Alt text: "Description of what the image shows"`
2. **Check for color-only information**: Search your document for color references. If you say "green correct, red incorrect," also include shapes or labels (checkmark/X, "Correct"/"Incorrect")
3. **Check headings**: Are sections properly nested? (## Section, ### Subsection, #### Sub-subsection) No skipping levels
4. **Interactive elements**: If you have interactive activities (clicks, drags, etc.), note "Keyboard accessible" and specify Tab/Enter interactions
5. **Use this test**: Could a blind student using a screen reader understand your content from alt text and structure alone?
6. **Check tables**: Do tables have row/column headers? Is the structure clear?

**Checklist:**
- [ ] Every image has descriptive alt text specified
- [ ] No color-only information (always pair with shapes/labels/text)
- [ ] Interactive elements are keyboard-accessible (noted if applicable)
- [ ] Headings properly nested (no level skipping)
- [ ] Tables have clear headers

**Reference:** `/universal/accessibility/wcag-compliance-guide.md`

#### 6. Cultural Responsiveness

**Requirements:**
- Diverse representation
- No stereotypes
- Culturally inclusive contexts
- Respectful of all identities
- Age-appropriate

**How to Check:**
1. **List all names in your content**: Are they diverse? (not all European/English names) Include names from various cultural backgrounds (Latinx, Asian, African, Middle Eastern, etc.)
2. **Check for stereotypes**: Open `/universal/content-equity/ceid-guidelines.md` and review the 11 categories. Ask for each:
   - Gender: Any stereotypes? (boys = sports, girls = shopping)
   - Race/ethnicity: Any stereotypes? (particular jobs, behaviors)
   - Family structure: Assuming two-parent families only?
   - Socioeconomic: Assuming all students have resources?
   - Ability: Are people with disabilities shown with agency?
3. **Check contexts**: Are examples universally relatable or culturally specific? (If specific, is it explained?)
4. **Review images**: Will images show diverse people in non-stereotypical roles?
5. **Use this test**: Would students from all backgrounds see themselves and their communities represented respectfully?

**Checklist:**
- [ ] Diverse names throughout (not all one culture)
- [ ] No gender stereotypes
- [ ] No racial/ethnic stereotypes
- [ ] Multiple family structures respected
- [ ] No assumptions about resources/socioeconomic status
- [ ] People with disabilities shown positively (if included)
- [ ] Contexts culturally inclusive or explained
- [ ] Reviewed against CEID 11 categories

**Reference:** `/universal/content-equity/ceid-guidelines.md`

#### 7. State Compliance

**Requirements:**
- Meets state adoption criteria
- Addresses quality rubrics
- Complies with content restrictions

**How to Check:**
1. **Identify your state**: Texas = SBOE/IPACC, California = Adoption Criteria, Florida = Adoption Criteria
2. **Open the compliance KB file** for your state:
   - Texas: `/districts/texas/compliance/sboe-quality-rubric.md` AND `/districts/texas/compliance/ipacc-suitability-requirements.md`
   - California: `/districts/california/compliance/california-adoption-criteria.md`
   - Florida: `/districts/florida/compliance/florida-adoption-criteria.md`
3. **Review checklist in KB file**: Most compliance files have a checklist. Go through it item by item
4. **Check for prohibited content**: Does your state prohibit certain topics or approaches? (Texas: no social/emotional learning in math/science. California: comprehensive history standards. Florida: specific literacy approaches)
5. **Verify citation requirements**: Some states require specific citation formats or source attributions
6. **When unsure**: Flag for editor review with specific question: "@editor Does this meet [state requirement X]?"

**Checklist:**
- [ ] Reviewed state-specific compliance KB file
- [ ] State quality rubric criteria addressed (if applicable)
- [ ] No content violates state restrictions
- [ ] Required elements included (varies by state)
- [ ] When uncertain, flagged for editor review

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

## 8. Frequently Asked Questions

### Getting Started

**Q: Where do content briefs come from? Who creates them?**
A: Content briefs are created by curriculum leads based on scope and sequence documents, state adoption requirements, and product roadmaps. They typically arrive via:
- Email assignment from your supervisor
- Task management system (Asana, Jira, etc.)
- Project dashboard notification
You'll be notified 1-2 weeks before your deadline.

**Q: What if I don't understand my content brief?**
A: Ask questions EARLY! Options:
1. Tag curriculum lead in your draft PR with specific questions
2. Email curriculum lead within 24 hours of receiving brief
3. Attend office hours (if your team has them)
4. Ask a peer author who's worked on similar content
Don't wait until the deadline to clarify.

**Q: How long does authoring usually take?**
A: Typical timelines:
- **Lesson:** 3-5 days (planning, drafting, self-review, submission)
- **Assessment:** 2-4 days (blueprint, items, answer key, self-review)
- **Activity:** 1-2 days (design, draft, self-review)
- **First assignment:** Add 1-2 extra days as you learn the process
Block out uninterrupted time for complex tasks like lesson sequences.

**Q: I'm overwhelmed. Where do I start?**
A: Follow the "Your First Week Quick Start" in this guide:
1. Day 1: Read brief, identify curriculum config, gather ~10 most important KB files
2. Day 2: Read KB files, review one complete example
3. Day 3-4: Draft using templates
4. Day 5: Self-review and submit
Don't try to read all 18 KB files cover-to-cover. Skim for what you need.

---

### Knowledge Base

**Q: How do I know which knowledge base files apply to my content?**
A: Check your curriculum config (e.g., `hmh-math-tx.json`). It lists resolution order. Then:
1. **Always use:** Universal files (UDL, DOK, WCAG, CEID, EB Scaffolding)
2. **Subject-specific:** Math = MLRs, ELA = Literacy Routines, Science = SEPs
3. **State-specific:** Texas = ELPS + SBOE, California = ELD, Florida = ESOL
See Section 3.2 for complete walkthrough.

**Q: Do I need to read all 18 knowledge base files for every lesson?**
A: No. Skim headers and overviews first. Prioritize:
- **MUST READ (5-7 files):** Standards alignment, language support (ELPS/ELD/ESOL), 1-2 instructional routines, UDL
- **SHOULD REFERENCE (3-5 files):** DOK framework, EB scaffolding, accessibility, vocab guidelines
- **AS NEEDED (remaining):** Assessment files (if writing assessments), CEID (check for bias), state compliance checklists

**Q: What if two knowledge base files give conflicting guidance?**
A: Use the resolution order (specific → general):
1. Program-specific guidance wins
2. Then subject-district
3. Then subject-common
4. Then district-wide
5. Finally universal
If truly contradictory (rare), note it in your PR and ask curriculum lead.

**Q: Can I create content without using the knowledge base?**
A: No. Knowledge base files ensure consistency, compliance, and quality. Editors will check that you've applied KB guidance. If you skip it, your content will be returned for revision. The KB is required, not optional.

**Q: The knowledge base file is 200 lines long. Do I need to apply ALL of it?**
A: No. Apply what's relevant to your specific content. For example:
- MLR file describes 8 routines → Use 2-3 that fit your lesson goals
- ELPS file lists 100+ standards → Focus on the 3-5 that align with your content
- Sentence frames library has 50+ frames → Choose 3-4 appropriate for your context

---

### AI Assistance

**Q: Should I use AI to generate my content?**
A: AI is a tool, not a replacement. Use it for:
- First drafts from outlines (then revise heavily)
- Generating item variations (then validate)
- Brainstorming differentiation ideas (then refine)
- Formatting and organizing (then check accuracy)
You're still responsible for quality, accuracy, cultural responsiveness, and pedagogical decisions.

**Q: How do I invoke AI assistance via GitHub?**
A: Create an issue, @ mention `@claude`, provide specifications:
```markdown
@claude Create Grade 5 Texas Math lesson on adding fractions.

Config: hmh-math-tx.json
Standards: TEKS.5.3.K, ELPS.3.E
Duration: 60 minutes
Include: MLR1, MLR2, three-tiered EB scaffolds, UDL
```
AI will generate draft and create PR. You review, revise, and finalize.

**Q: Can AI-generated content be submitted as-is?**
A: **NO.** You must:
1. Review for accuracy (AI makes mistakes)
2. Check cultural responsiveness (AI can perpetuate bias)
3. Verify standards alignment
4. Validate pedagogical soundness
5. Ensure all 7 Quality Pillars are met
6. Add your professional judgment
Editors can tell when content is unrevised AI output. It will be rejected.

---

### Review Process

**Q: How long does editorial review take?**
A: Typical timelines:
- **Initial review:** 3-5 business days after submission
- **Re-review after revisions:** 1-2 business days
- **Rush requests:** 24-48 hours (if pre-approved by supervisor)
Don't submit Friday afternoon expecting Monday feedback. Plan accordingly.

**Q: What if I disagree with editor feedback?**
A: It's okay to discuss! Options:
1. **Ask for clarification:** "Can you explain why this scaffold isn't sufficient?"
2. **Propose alternative:** "What if I do X instead of Y? Would that address your concern?"
3. **Provide rationale:** "I chose this approach because [pedagogical reason]. Is there a compliance issue?"
Editors are partners, not adversaries. Most "disagreements" are miscommunications.

**Q: My content was returned with 15 comments. Is that bad?**
A: **No, it's normal**, especially for your first 2-3 assignments. Average for new authors:
- First assignment: 15-25 comments
- Second assignment: 10-15 comments
- Third+ assignment: 5-10 comments
Feedback means the editor is helping you improve. No feedback would be concerning.

**Q: What happens if my content is rejected?**
A: "Rejected" is rare. More common: "returned for major revision."
- **Minor revisions:** Small fixes, 1-2 days of work, re-submit
- **Major revisions:** Significant changes needed, 2-3 days of work, may need new review cycle
- **Rejection (very rare):** Content doesn't meet basic standards, may need to start over
Your supervisor will work with you if you're struggling.

**Q: Can I see examples of approved content before I start?**
A: Yes! See Section 4.5 "Complete Example Works" for:
- Full approved lesson (Grade 5 Texas Math)
- Full approved assessment (Grade 5 Texas Math)
Both demonstrate all 7 Quality Pillars. Use these as models.

---

### Quality Standards

**Q: What are the 7 Quality Pillars, and do I really need to meet ALL of them?**
A: Yes, all 7 are required for approval:
1. **Standards Alignment** - Map to state standards
2. **Pedagogical Soundness** - Evidence-based practices
3. **Language Support** - ELPS/ELD/ESOL scaffolds
4. **UDL** - Multiple means of representation, action, engagement
5. **Accessibility** - WCAG 2.1 AA compliance
6. **Cultural Responsiveness** - CEID framework, bias-free
7. **State Compliance** - Meets state adoption criteria
Missing even one pillar = returned for revision.

**Q: How do I check if my content is culturally responsive?**
A: Use the CEID framework (11 categories). Ask yourself:
- Do examples include diverse names and contexts?
- Are there stereotypes (even subtle ones)?
- Is language gender-neutral where appropriate?
- Do images show diverse representation?
- Are contexts relevant across cultures?
When in doubt, consult CEID guidelines file or ask editor.

**Q: What's the difference between "accessibility" and "UDL"?**
A:
- **Accessibility (Pillar 5):** Technical compliance (alt text, color contrast, keyboard navigation, WCAG 2.1 AA)
- **UDL (Pillar 4):** Instructional design (multiple representations, student choice, flexible paths)
Both are required. Example: Alt text = accessibility. Offering audio AND text = UDL.

**Q: I don't have time to make it perfect. What's the minimum to pass review?**
A: "Minimum" is still high quality. Use the Essential Checklist (see Section 6.5):
- Standards explicitly listed and addressed
- Learning objectives with measurable verbs
- At least one instructional routine correctly applied
- Three-tiered EB scaffolds (Beginning/Intermediate/Advanced)
- At least 2 forms of representation (visual + verbal, or manipulative + visual)
- Alt text for all images
- Answer key with complete solutions
- No obvious bias or stereotypes
Rushing leads to more revision cycles. Better to ask for deadline extension.

---

### State-Specific Questions

**Q: I'm writing for Texas. What's different from other states?**
A: Texas specifics:
- **Standards:** TEKS (not CCSS)
- **Language:** ELPS (English Language Proficiency Standards)
- **Compliance:** SBOE quality rubric, IPACC (Instructional Planning and Assessment Correlation Chart)
- **Unique requirements:** Proclamation alignment (changes every 6-8 years)
Use `/districts/texas/` and `/subjects/[subject]/districts/texas/` KB files.

**Q: I'm writing for California. What's different?**
A: California specifics:
- **Standards:** CCSS (Common Core) for Math/ELA, NGSS for Science, CA History-Social Science Framework
- **Language:** ELD (English Language Development Standards)
- **Compliance:** California adoption criteria, Content Review Standards
- **Unique requirements:** Grade-level span materials (K-5, 6-8, 9-12)
Use `/districts/california/` and `/subjects/[subject]/districts/california/` KB files.

**Q: Can I reuse content across states?**
A: Partially. You can reuse:
- Instructional sequences and activities (if standards align)
- Visual models and manipulatives
- Assessment item stems (if adjusted for state standards)
You MUST change:
- Standards references (TEKS → CCSS, etc.)
- Language scaffolds (ELPS → ELD → ESOL)
- State-specific compliance elements
Don't just find-and-replace. Review for alignment.

---

### Collaboration

**Q: Can I collaborate with other authors?**
A: Yes, encouraged! Ways to collaborate:
- Peer review drafts before submitting to editors
- Share strategies in team meetings
- Co-author large projects (with supervisor approval)
- Ask experienced authors for advice
Just don't copy someone else's content without attribution.

**Q: What if I find an error in the knowledge base?**
A: Report it immediately:
1. Note the error in your PR comments
2. Create an issue: "KB Error: [file name] line [X] - [description]"
3. Tag curriculum lead or knowledge base engineer
In the meantime, document your workaround in your PR.

**Q: Can I suggest improvements to the knowledge base?**
A: Absolutely! Create an issue:
```markdown
Title: KB Enhancement: Add sentence frames for science explanations

The current sentence frames library doesn't include frames for
scientific explanations (CER). Suggest adding:
- "I claim that ___ because ___."
- "The evidence for this is ___."
- "This reasoning connects to ___ because ___."
```

---

### Technical and Process

**Q: I'm not comfortable with Git. Can I submit content another way?**
A: Git/GitHub is required for version control and editorial workflow. But there are easier tools:
- **GitHub Desktop:** GUI alternative to command-line Git
- **VS Code with GitHub extension:** Integrated GUI
- **Web interface:** Create/edit files directly on GitHub.com
Ask your supervisor for training if needed. Section 9 has troubleshooting tips.

**Q: What if I miss a deadline?**
A: Communicate ASAP (ideally 2-3 days before deadline):
1. Notify supervisor and editor
2. Explain situation (illness, complex content, etc.)
3. Propose new deadline
4. Ask if partial submission is possible
Occasional deadline issues are understood. Chronic lateness without communication is a problem.

**Q: How do I handle content that needs sensitive topic warnings?**
A: Some content may address sensitive topics (violence, trauma, etc.). If your brief includes such content:
1. Follow trauma-informed practices (don't gratuitously detail harm)
2. Add content warnings where appropriate
3. Consult CEID guidelines for age-appropriateness
4. Flag for editorial review if you're unsure
When in doubt, ask your curriculum lead.

**Q: What if the knowledge base doesn't cover my topic?**
A: Rare, but possible for new subjects or emerging standards. Steps:
1. Use the closest analogous KB files
2. Research best practices externally (cite sources)
3. Document your approach in PR comments
4. Ask curriculum lead for guidance
5. Propose new KB file creation (may become your contribution!)

**Q: Can I work ahead and create content not in my brief?**
A: Check with supervisor first. Unsolicited content may:
- Not fit the scope and sequence
- Duplicate work in progress
- Not align with upcoming adoption cycles
If you have ideas, propose them through proper channels.

---

### Career Development

**Q: How do I become a better author?**
A: Strategies:
1. **Study approved examples** (Section 4.5)
2. **Read editor feedback carefully** - it's free professional development
3. **Compare your drafts to approved content** - what's different?
4. **Learn from peer authors** - attend working sessions
5. **Deepen knowledge base understanding** - read KB files for professional learning
6. **Request targeted feedback** - "I'm working on improving my EB scaffolds. Please focus on that."

**Q: Can I become an editor or curriculum lead?**
A: Typically after 1-2 years of successful authoring. Demonstrate:
- Consistent quality (most content approved on first submission)
- Deep knowledge base understanding
- Strong peer collaboration
- Mentoring newer authors
- Contributions to knowledge base improvement
Express interest to your supervisor during performance reviews.

**Q: I love this work. How do I do more of it?**
A: Options:
1. **Take on more assignments** (if capacity allows)
2. **Expand to new subjects** (requires learning new KB files)
3. **Become a subject matter expert** (go deep in one area)
4. **Mentor new authors** (formal or informal)
5. **Contribute to knowledge base** (propose new files, improve existing)
6. **Present at team meetings** (share strategies, best practices)

---

### If You're Still Stuck

**Q: I've read the guide, but I'm still confused. What now?**
A: Reach out for human help:
1. **Your supervisor** - Primary point of contact
2. **Experienced peer author** - Day-to-day questions
3. **Editor assigned to your project** - Content-specific guidance
4. **Curriculum lead** - Brief interpretation, standards questions
5. **Knowledge base engineer** - KB file questions, technical issues

**Office hours**, **team meetings**, and **Slack channels** (if your organization uses them) are also great resources.

**You're not expected to know everything on Day 1.** Asking questions shows you care about quality.

---

**Still have questions?** See Section 9 (Troubleshooting) or Section 10 (Process Information and Support).

---

## 9. Troubleshooting Common Issues

This section provides solutions to problems you'll likely encounter. Try these fixes before asking for help.

---

### Problem: "I can't find the right knowledge base file"

**Symptoms:**
- Unsure which KB files apply to your content
- Can't locate a file referenced in another guide
- Don't know where to start

**Solutions:**

**Step 1: Check your curriculum config**
```bash
# Example: Find config for Texas Math
cat config/curriculum/hmh-math-tx.json
```
This shows the resolution order with full paths.

**Step 2: Use the Quick Reference table in Section 7**
- Universal files: Always `/universal/[category]/`
- Math routines: `/subjects/mathematics/common/mlr/`
- ELA routines: `/subjects/ela/common/literacy-routines/`
- Texas language: `/districts/texas/language/elps-alignment.md`
- California language: `/districts/california/language/eld-alignment.md`

**Step 3: Browse the directory**
```bash
# See all math common files
ls reference/hmh-knowledge-v2/subjects/mathematics/common/

# See all Texas district files
ls reference/hmh-knowledge-v2/districts/texas/
```

**Still stuck?** See ENGINEER_GUIDE.md Section 2 for complete KB architecture.

---

### Problem: "My MLR/Literacy Routine doesn't fit my lesson"

**Symptoms:**
- The routine takes too long (MLR says 15 min, but your lesson is only 45 min)
- The routine doesn't match your content
- You're not sure which routine to use

**Solutions:**

**If it doesn't fit timewise:**
- **Abbreviate:** Use 2 rounds of MLR1 instead of 3 (8 min instead of 15 min)
- **Focus:** Apply the routine to just the key activity, not every problem
- **Document:** Note in your lesson: "Abbreviated MLR1 due to time constraints"

**If it doesn't match your content:**
- **Choose a different routine:** MLR8 (Discussion Supports) works for almost anything
- **Adapt the protocol:** Keep the structure, change the prompts to fit your content
- **Combine:** Use part of MLR1 and part of MLR2 if both partially fit

**If you're not sure which to use:**

| When your goal is... | Use this routine |
|----------------------|------------------|
| Refine explanations | MLR1 (Stronger and Clearer) |
| Collect strategies | MLR2 (Collect and Display) |
| Clarify vocabulary | MLR3 (Clarify, Critique, Correct) |
| Make connections | MLR7 (Compare and Connect) |
| Support any discussion | MLR8 (Discussion Supports) |
| Reading with purpose (ELA) | Close Reading Protocol |
| Quick pair check (ELA) | Turn-and-Talk |

---

### Problem: "Editor says my EB scaffolds aren't specific enough"

**Symptoms:**
- Feedback: "Scaffolds too generic"
- Feedback: "Provide actual sentence frames, not just 'provide scaffolds'"
- Feedback: "Differentiate between Beginning/Intermediate/Advanced"

**Solution: Be SPECIFIC**

**❌ Too Generic:**
```
EB Scaffolds:
- Beginning: Provide sentence frames
- Intermediate: Provide some support
- Advanced: Minimal support
```

**✅ Specific:**
```
EB Scaffolds:
- Beginning: Sentence frame: "I think ___ is greater because ___."
              Provide fraction strips to physically compare
              Word bank: greater, less, equal, more, fewer
- Intermediate: Sentence starter: "I can tell that ___ because when I ___."
                 Fraction strips available upon request
- Advanced: Prompt: "Explain your reasoning using precise mathematical language."
            Encourage terms: equivalent, magnitude, compare
```

**Key difference:** Specific scaffolds tell teachers EXACTLY what to say/provide. Generic scaffolds leave teachers guessing.

---

### Problem: "I don't have time to meet all 7 Quality Pillars"

**Symptoms:**
- Deadline approaching, content incomplete
- Tempted to skip a pillar ("Does anyone really check accessibility?")
- Overwhelmed by requirements

**Solution: Use the Essential Checklist**

Editors WILL check all 7 pillars. Missing one = revision required. But you can be efficient:

**Essential Checklist (minimum viable product):**

**Pillar 1 - Standards:**
- [ ] Standards listed at top of document
- [ ] Each learning objective maps to a standard
- [ ] Check standards KB file for expectations

**Pillar 2 - Pedagogy:**
- [ ] Warm-up → Instruction → Practice → Closure structure
- [ ] At least ONE instructional routine applied (MLR or literacy routine)
- [ ] At least one formative check

**Pillar 3 - Language:**
- [ ] Three-tiered EB scaffolds (Beginning/Intermediate/Advanced) in at least 2 sections
- [ ] At least 1 sentence frame provided
- [ ] ELPS/ELD/ESOL standard referenced

**Pillar 4 - UDL:**
- [ ] At least 2 representations (e.g., visual model + verbal explanation)
- [ ] At least 1 student choice (e.g., "choose number line OR fraction strips")

**Pillar 5 - Accessibility:**
- [ ] Alt text for every image
- [ ] No color-only information (if using colors, also use shapes/labels)

**Pillar 6 - Cultural Responsiveness:**
- [ ] Diverse names in examples (not all "Tom, Sue, Bob")
- [ ] No stereotypes (check CEID file if unsure)
- [ ] Neutral or diverse contexts

**Pillar 7 - State Compliance:**
- [ ] Used state-specific KB files (TEKS/CCSS, ELPS/ELD, SBOE/adoption criteria)
- [ ] Checked state compliance checklist

**Time-saving tip:** Template these! Once you have one approved lesson, reuse the structure.

---

### Problem: "Git/GitHub errors"

**Common Git Issues and Fixes:**

#### Error: "fatal: not a git repository"

**Cause:** You're not in the right directory.

**Fix:**
```bash
cd /path/to/content  # Navigate to repo
pwd  # Verify you're in the right place
git status  # Should work now
```

#### Error: "Permission denied (publickey)"

**Cause:** GitHub can't authenticate you.

**Fix:**
```bash
# Check if you have SSH keys
ls -al ~/.ssh

# If no keys, generate them (follow prompts):
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add key to SSH agent:
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key and add to GitHub:
cat ~/.ssh/id_ed25519.pub
# Go to GitHub.com → Settings → SSH Keys → Add New
```

#### Error: "merge conflict"

**Cause:** Someone else edited the same file.

**Fix:**
```bash
# Option 1: Accept their changes (safe if you haven't started yet)
git checkout --theirs path/to/file
git add path/to/file
git commit

# Option 2: Accept your changes (if you're sure yours are correct)
git checkout --ours path/to/file
git add path/to/file
git commit

# Option 3: Manually resolve (open file, look for <<<<<<, ======, >>>>>>)
# Edit file to keep what you want, remove markers
git add path/to/file
git commit
```

#### "I committed to the wrong branch"

**Fix:**
```bash
# Move commit to correct branch
git log  # Copy the commit hash
git checkout correct-branch
git cherry-pick <commit-hash>

# Remove from wrong branch
git checkout wrong-branch
git reset --hard HEAD~1
```

#### "I want to undo my last commit"

**Fix:**
```bash
# Keep changes, undo commit:
git reset --soft HEAD~1

# Discard changes AND commit:
git reset --hard HEAD~1  # WARNING: Deletes your work!
```

#### "GitHub Desktop / VS Code alternatives"

If command-line Git is overwhelming:

**GitHub Desktop (free):**
1. Download: desktop.github.com
2. Clone your repo through the GUI
3. Make changes in your editor
4. Commit and push through the app

**VS Code Git Integration:**
1. Open repo folder in VS Code
2. Make changes
3. Click Source Control icon (left sidebar)
4. Stage changes (+ icon)
5. Enter commit message
6. Click checkmark to commit
7. Click "..." → Push

---

### Problem: "Editor feedback is unclear"

**Symptoms:**
- Comment: "Improve EB scaffolds" (but how?)
- Comment: "Fix standards alignment" (but what's wrong?)
- Not sure what the editor wants

**Solutions:**

**Ask for clarification in the PR:**
```markdown
@editor Thanks for the feedback. I want to make sure I understand:

For your comment on EB scaffolds in the Warm-Up section:
- Do you mean the scaffolds are too generic? Should I provide specific sentence frames?
- Or do you mean they're not differentiated enough between proficiency levels?
- Or something else?

Could you provide an example of what you're looking for?
```

**Request a synchronous meeting:**
If you have 3+ unclear comments, ask for a 15-minute call or video chat to discuss.

**Compare to approved examples:**
Look at Section 4.5 examples. Does your content match that level of detail?

**Tag a peer author:**
"@experienced-author Can you look at this feedback and help me understand what the editor is asking for?"

---

### Problem: "I'm behind deadline"

**Symptoms:**
- Deadline in 1-2 days, content 50% done
- Panicking
- Considering submitting incomplete work

**Solutions:**

**Option 1: Ask for extension (BEST)**
```markdown
@supervisor @editor

I'm working on [content brief name] due [date]. I've encountered
[challenge: complexity/illness/other assignment conflict] and need
an additional [2-3 days] to complete it with quality.

Current status: [Brief summary of what's done]
Remaining work: [What's left]

Can we extend the deadline to [new date]?
```
Most supervisors would rather have quality work late than rushed work on time.

**Option 2: Submit partial for feedback**
```markdown
@editor

I'm behind on [content brief]. I'd like to submit what I have
so far for early feedback while I finish the rest.

Completed: [Sections done]
In progress: [What you're working on]

Can you review what's here and let me know if I'm on the right track?
I'll complete the rest by [date].
```

**Option 3: Focus on essentials**
If extension isn't possible, use the Essential Checklist (see above) to ensure minimum quality standards. Better to have solid essentials than incomplete everything.

**What NOT to do:**
- ❌ Submit without communicating you're behind
- ❌ Skip quality pillars hoping no one notices
- ❌ Submit AI-generated content without review

---

### Problem: "Knowledge base file seems outdated or wrong"

**Symptoms:**
- KB file references standards that don't exist
- Guidance contradicts official state documents
- File seems incomplete

**Solutions:**

**Step 1: Verify you have the latest version**
```bash
git pull origin main  # Get latest updates
```
KB files are updated regularly.

**Step 2: Check if there's a newer file**
```bash
# See all files in that directory
ls reference/hmh-knowledge-v2/subjects/mathematics/districts/texas/

# Check file modification date
ls -l reference/hmh-knowledge-v2/subjects/mathematics/districts/texas/teks-math-alignment.md
```

**Step 3: Report the issue**
Create an issue in GitHub:
```markdown
Title: KB File Error: teks-math-alignment.md Grade 5 standard incorrect

**File:** /reference/hmh-knowledge-v2/subjects/mathematics/districts/texas/teks-math-alignment.md
**Line:** 234
**Issue:** Lists TEKS.5.3.H as "compare fractions with like denominators"
           but current TEKS (2022) says "compare fractions with unlike denominators"

**Source:** https://tea.texas.gov/academics/curriculum-standards

**Impact:** Affects all Grade 5 Texas Math fractions content
```

**Step 4: Document your workaround**
In your PR:
```markdown
**Note:** KB file [name] appears outdated. I used the official TEKS document
(linked above) for standards alignment. Please review.
```

---

### Problem: "I don't understand DOK levels"

**Symptoms:**
- Brief says "DOK 2" but you don't know what that means
- Unsure if your item is DOK 2 or DOK 3
- Editor feedback: "This is DOK 1, not DOK 2"

**Quick DOK Guide:**

**DOK 1 - Recall:**
- What is...? Define... Identify... Label...
- Example: "What is 2/3 + 1/3?"

**DOK 2 - Skill/Concept:**
- How did you...? Explain how... Classify... Compare...
- Example: "Explain how to add 2/3 + 1/3 using a visual model."

**DOK 3 - Strategic Thinking:**
- Why did you...? Justify... Analyze... What if...? Critique...
- Example: "Marcus says 2/3 + 1/3 = 3/6. Explain his error and show the correct solution."

**DOK 4 - Extended Thinking (rare):**
- Design an investigation... Develop a model... Synthesize across disciplines...
- Example: "Design three different problems that all have the answer 5/6. Explain how you created them."

**Rule of thumb:**
- DOK 1 = recall or one step
- DOK 2 = apply or multiple steps
- DOK 3 = justify, analyze, or critique
- DOK 4 = sustained project (rare in K-12)

**Still unsure?** Check `/universal/frameworks/dok-framework.md`

---

### Problem: "My content is too long"

**Symptoms:**
- Brief says "45 minutes" but your lesson is 75 minutes
- Too many activities and not enough time
- Everything feels essential

**Solutions:**

**Step 1: Check your time estimates**
Are they realistic?
- Warm-up: 5-10 min (not 20)
- Instruction: 15-20 min (not 30)
- Practice: 15-20 min (not 30)
- Closure: 5 min (not 15)

**Step 2: Cut or abbreviate**
- Reduce number of practice problems
- Abbreviate routines (2 rounds instead of 3)
- Move some content to homework or next lesson
- Remove "nice to have" vs "need to have"

**Step 3: Consider pacing note**
Add a pacing note:
```markdown
**Pacing Note:** This lesson is designed for 60 minutes. For 45-minute periods:
- Skip problems 4-6 in guided practice OR
- Abbreviate MLR1 to 2 rounds OR
- Assign independent practice as homework
```

**Step 4: Verify with curriculum lead**
Maybe the content IS too much for one lesson. Ask: "This seems like 75 minutes of content. Should I split into two lessons?"

---

### Problem: "I don't have the required assets/images"

**Symptoms:**
- Brief specifies images you don't have
- Need manipulatives you can't create
- Videos or audio files not available

**Solutions:**

**Step 1: Document what you need**
Create assets list in your lesson:
```markdown
## Assets Needed
- Image 1: Fraction strips (wholes, halves, thirds, fourths) - 1200x800px
  Alt text: "Fraction strips showing wholes through fourths"
- Image 2: Number line 0 to 1 with benchmarks - 1200x400px
  Alt text: "Number line from 0 to 1 with 1/2 marked"
```

**Step 2: Use placeholders**
```markdown
[IMAGE: Fraction strips - to be created by design team]
```

**Step 3: Note in PR**
```markdown
@supervisor Asset requests documented in lesson. Please assign to design team.
Timeline needed: 2 weeks before final publication.
```

Production team will create assets based on your specifications.

**Interim solution for draft:** Use text descriptions or ASCII art as placeholders.

---

### Problem: "I'm getting conflicting guidance from different sources"

**Symptoms:**
- KB file says one thing, curriculum lead says another
- AUTHOR_GUIDE says X, but editor marked it wrong
- State document contradicts KB file

**Resolution hierarchy (most to least authoritative):**

1. **Official state documents** (TEKS, CCSS, ELPS, etc.) - These are law
2. **Your supervisor/curriculum lead** - They have final authority on product
3. **Knowledge base files** - Authoritative for this project (unless outdated)
4. **Editor guidance** - Interprets KB files for your content
5. **This guide (AUTHOR_GUIDE.md)** - General guidance, not absolute rules

**When in conflict:**
1. Document all sources in your PR
2. Ask: "@curriculum-lead I'm seeing conflicting guidance. [Explain conflict]. Which should I follow?"
3. Wait for clarification before proceeding

**Never guess** when requirements conflict. Always ask.

---

### When to Escalate

**Escalate to supervisor when:**
- Editor feedback is repeatedly unclear after clarification attempts
- You're consistently behind deadline due to workload
- Knowledge base has errors affecting multiple assignments
- You're unsure if content is appropriate (sensitive topics, etc.)
- Interpersonal issues with editor or team members

**How to escalate professionally:**
```markdown
@supervisor

I need your guidance on [situation]. Here's what I've tried:
1. [Action taken]
2. [Result]
3. [Action taken]
4. [Result]

I'm stuck and need your help to move forward. Can we schedule 15 minutes to discuss?

Priority: [High/Medium/Low]
```

---

**Most issues can be solved by:**
1. Reading this guide thoroughly
2. Checking approved examples (Section 4.5)
3. Asking in PR comments
4. Checking knowledge base files
5. Asking a peer author

**If still stuck:** See Section 10 (Process Information and Support).

---

## 10. Process Information and Support

This section provides organizational context: where content comes from, how it flows through the system, and who to contact for help.

---

### The Content Development Lifecycle

**High-Level Overview:**

```
Product Planning → Curriculum Design → Content Brief Creation → Author Assignment
    ↓
Author Drafts Content (3-5 days)
    ↓
Self-Review Against 7 Quality Pillars
    ↓
Submit via Pull Request → Editorial Review (3-5 days)
    ↓
[If revisions needed] ← Author Revises (1-2 days) → Re-Review (1-2 days)
    ↓
[If approved] → Approval & Merge
    ↓
Production (Multi-Format) (2-5 days)
    ↓
Quality Assurance
    ↓
Delivery to Stakeholders
```

**Your role:** Draft high-quality content that meets the 7 Quality Pillars

---

### Where Content Briefs Come From

**The Planning Process:**

1. **Product Management** defines what products/curricula to develop based on:
   - Market needs
   - State adoption cycles (e.g., Texas adopts math every 6-8 years)
   - Customer requests
   - Strategic priorities

2. **Curriculum Architects** create scope and sequence:
   - What topics in what order?
   - How many lessons per unit?
   - What assessments are needed?
   - Timeline for development

3. **Curriculum Leads** create content briefs:
   - Break scope into assignable chunks
   - Specify standards, learning objectives, duration
   - Identify knowledge base files to use
   - Note any special requirements

4. **Project Managers** assign briefs to authors:
   - Match author expertise to content needs
   - Balance workload across team
   - Set deadlines based on production schedule

**Timeline:** Typically planned 3-6 months ahead for major curricula, 4-8 weeks for updates.

**You receive brief:** 1-2 weeks before your deadline (sometimes less for urgent updates)

---

### Review Timelines and Expectations

**Standard Review Timeline:**

| Stage | Time | What Happens |
|-------|------|--------------|
| **Author Drafts** | 3-5 days | You create content, self-review, submit PR |
| **Editor Receives** | 1 day | Editor triages, schedules review |
| **Initial Review** | 3-5 business days | Editor applies 8-section checklist, leaves feedback |
| **Author Revises** | 1-2 days | You address feedback, push updates |
| **Re-Review** | 1-2 business days | Editor verifies fixes |
| **Approval** | Same day | Editor approves, merges to main |
| **Total** | 8-14 days | From submission to approval |

**Expedited Review (pre-approved only):**
- Initial review: 24-48 hours
- Re-review: Same day or next day
- Total: 3-5 days
- **Note:** Not all content qualifies. Ask supervisor first.

**What affects review time:**
- Editor workload (they review multiple authors)
- Complexity of content
- Quality of initial submission (fewer issues = faster approval)
- Time of year (slower during holidays)
- Urgency of project

**Pro tip:** Submit Tuesday-Wednesday for fastest turnaround. Avoid Friday PM submissions.

---

### Understanding Editor Feedback

**Types of Feedback:**

1. **Required Changes** - Must fix before approval
   - "Missing ELPS scaffolds for Beginning proficiency"
   - "Standards not explicitly listed"
   - "Answer key incorrect for problem 7"

2. **Strongly Recommended** - Should fix, but may discuss
   - "Consider adding a visual model here"
   - "This routine might work better than the one you chose"
   - "Suggest revising this misconception explanation"

3. **Suggestions** - Optional improvements
   - "Nice touch with the anchor chart"
   - "You could extend this for advanced students"
   - "Consider this approach for future lessons"

**How to tell which is which:**
- Required: "Must," "Need to," "Missing," "Incorrect"
- Recommended: "Should," "Consider," "Suggest"
- Suggestions: "Could," "Nice," "Optional," "Idea"

**If unclear:** Ask the editor to clarify priority level.

---

### Escalation Paths

**When you need help, follow this escalation order:**

**Level 1: Self-Service (try first)**
- This guide (AUTHOR_GUIDE.md)
- Approved examples (Section 4.5)
- Knowledge base files
- FAQ (Section 8)
- Troubleshooting (Section 9)

**Level 2: Peer Support (day-to-day questions)**
- Experienced author on your team
- Team Slack/chat channel
- Weekly team meetings
- Informal peer review

**Level 3: Editor (content-specific)**
- Your assigned editor via PR comments
- Questions about their feedback
- Content interpretation questions
- State compliance clarification

**Level 4: Curriculum Lead (brief/standards)**
- Brief interpretation
- Standards alignment questions
- Scope changes
- Knowledge base file questions

**Level 5: Supervisor (workload/process)**
- Deadline extensions
- Workload concerns
- Performance feedback
- Career development
- Interpersonal issues
- Process problems

**Level 6: Project Manager (cross-team issues)**
- Dependencies on other teams (design, production)
- Timeline concerns affecting multiple people
- Resource conflicts

**When to skip levels:**
- **Urgent compliance issue** (e.g., content may violate law) → Supervisor immediately
- **Knowledge base error** affecting multiple authors → Curriculum Lead + create issue
- **Interpersonal conflict** → Supervisor (don't try to resolve yourself)

---

### Support Contacts and Resources

**Role-Specific Contacts:**

**For Authoring Questions:**
- **Primary:** Your assigned editor (via PR comments)
- **Secondary:** Curriculum lead for your subject
- **Backup:** Peer authors on your team

**For Technical Issues (Git, GitHub, system access):**
- **Primary:** IT support (create ticket via [your org's system])
- **GitHub-specific:** See Section 9 Git troubleshooting first
- **Knowledge base technical issues:** Knowledge base engineer (tag in issue)

**For Standards/Compliance:**
- **Primary:** Curriculum lead for your state/subject
- **State adoption questions:** Compliance specialist (if your org has one)
- **Official state documents:**
  - Texas: tea.texas.gov
  - California: cde.ca.gov
  - Florida: fldoe.org

**For Knowledge Base:**
- **Usage questions:** See ENGINEER_GUIDE.md
- **Errors/improvements:** Create GitHub issue, tag KB engineer
- **Missing KB files:** Curriculum lead or KB engineer

**For Process/Workflow:**
- **Your supervisor** - Primary point of contact for all process questions
- **Project manager** - Timeline and dependencies
- **Onboarding mentor** (if assigned) - General questions in first 2 months

---

### Communication Best Practices

**When Asking for Help:**

**❌ Ineffective:**
```
"My content isn't working. Help!"
```

**✅ Effective:**
```markdown
@editor I'm stuck on EB scaffolds for my warm-up section.

**What I'm trying to do:** Provide three-tiered scaffolds for fraction comparison

**What I've tried:**
- Read `/universal/frameworks/eb-scaffolding-guide.md`
- Looked at Section 4.5 example
- Drafted scaffolds (see lines 45-52)

**Specific question:** Are these scaffolds specific enough, or do I need to add more detail?
The guide says "be specific," but I'm not sure if this is specific enough.

Can you advise?
```

**Elements of effective questions:**
1. Context (what you're working on)
2. What you've already tried
3. Specific question or decision point
4. Where to look in your draft (line numbers, sections)

---

### Office Hours and Meetings

**Typical Support Structures (may vary by organization):**

**Weekly Team Meetings:**
- Share progress updates
- Discuss common challenges
- Learn from each other's work
- Announcements about KB updates

**Office Hours (if available):**
- Drop-in time with curriculum lead or experienced author
- Ask questions in real-time
- Get quick feedback on drafts
- Typical: 1 hour/week

**One-on-Ones with Supervisor:**
- Monthly or bi-weekly
- Discuss workload, performance, career development
- Raise concerns
- Request additional training

**Professional Development:**
- Workshops on instructional design
- Training on new standards or frameworks
- Guest speakers (e.g., state education officials)
- Curriculum conferences

**Participate when you can.** These are opportunities to learn, connect, and grow.

---

### Knowledge Base Updates and Announcements

**How you'll know about KB updates:**

1. **GitHub notifications** (if you watch the repo)
2. **Team meeting announcements**
3. **Email from curriculum lead** (for major updates)
4. **Slack/chat notifications** (if your org uses them)

**What to do when KB files update:**
```bash
# Pull latest changes
git pull origin main

# Check what changed
git log reference/hmh-knowledge-v2/

# If it affects your current work, review the updated file
```

**Major updates** (e.g., new state standards adopted) will come with transition guidance.

**Minor updates** (typos, clarifications) don't require action unless they affect your current assignment.

---

### Feedback and Continuous Improvement

**This guide and the knowledge base improve based on YOUR input.**

**How to contribute:**

1. **Report errors:** Create GitHub issue for any mistakes you find
2. **Suggest improvements:** "This section could use an example of X"
3. **Share strategies:** Present at team meetings about what works for you
4. **Propose new KB files:** "We need guidance on [topic]"
5. **Review updates:** When KB files are updated, provide feedback

**Creating an Improvement Issue:**
```markdown
Title: AUTHOR_GUIDE Enhancement: Add example for science lessons

**Current State:** Section 4.5 has math examples, but no science examples.

**Proposed Improvement:** Add Grade 5 NGSS science lesson example showing:
- How to apply Science Practices (SEPs)
- CER (Claim-Evidence-Reasoning) framework
- NGSS 3-dimensional learning

**Why it matters:** Science authors don't have a model to follow.

**Volunteer:** I'm willing to draft this once my current lesson is approved.
```

**Your experience matters.** If something confused you, it will confuse the next new author. Help us improve the system.

---

### Career Path and Growth

**Progression for Content Authors:**

**Year 1: Developing Author**
- Learning knowledge base and workflows
- Requires significant editorial feedback
- Focuses on one subject/state
- Goal: Consistent quality, faster turnaround

**Year 2: Proficient Author**
- Minimal editorial revisions needed
- May expand to new subjects/states
- Starts mentoring newer authors
- May contribute to knowledge base improvements

**Year 3+: Advanced/Senior Author**
- Consistently approved on first submission
- Subject matter expert in one+ areas
- Formal mentorship role
- May transition to editor or curriculum lead

**Other paths:**
- **Editorial track:** Content reviewer, managing editor
- **Curriculum design track:** Curriculum lead, learning architect
- **Production track:** Multi-format production specialist
- **Knowledge engineering:** KB maintenance and expansion
- **Project management:** Content development PM

**How to progress:**
1. Demonstrate consistent quality
2. Expand your expertise (new subjects/states)
3. Mentor others
4. Contribute to knowledge base
5. Express interest during performance reviews

---

### When the Process Isn't Working

**Signs the system needs improvement:**
- Consistently unclear briefs
- Excessive revision cycles (>3 rounds)
- Conflicting guidance from different sources
- Missing knowledge base files for your content
- Unrealistic timelines
- Inadequate training or onboarding

**What to do:**
1. Document specific examples
2. Discuss with supervisor
3. Propose concrete improvements
4. Volunteer to help implement solutions

**Example:**
```markdown
@supervisor

I've noticed that Texas science briefs don't specify which NGSS performance
expectations to address. This has led to confusion in my last 3 assignments,
requiring extra clarification rounds.

Could we update the brief template to include:
- Primary NGSS PE
- Supporting PEs
- Science Practices (SEPs) to emphasize

I'm happy to draft template language if that helps.
```

**The system improves when people speak up constructively.**

---

### Emergency Contacts

**For urgent issues only** (use during business hours when possible):

**Content emergencies:**
- Supervisor (check your org's contact sheet for phone/email)

**Technical emergencies:**
- IT support hotline (check your org's contact sheet)

**What qualifies as "emergency":**
- ✅ Content may violate state law or accessibility requirements (and deadline is imminent)
- ✅ System completely down and blocking all work (and deadline is imminent)
- ✅ Personal safety or well-being concern

**What doesn't qualify:**
- ❌ "I forgot about my deadline" (use regular escalation)
- ❌ "Editor hasn't responded in 2 hours" (editors need time to review)
- ❌ "I don't understand this KB file" (use regular support channels)

**Use emergency contacts sparingly and professionally.**

---

### Final Thoughts on Support

**You're part of a team.** Content development is collaborative:
- Curriculum leads plan
- Authors create
- Editors review
- Production formats
- QA validates
- Everyone improves the system

**Ask questions.** There are no stupid questions, only undocumented answers. If you're confused, others probably are too.

**Be patient with the process.** Review cycles exist to ensure quality. Feedback isn't criticism—it's how we get to great content together.

**Contribute back.** As you learn, help the next person. Update docs, mentor new authors, improve the knowledge base.

**Most important:** Focus on creating excellent educational content that serves students. That's why we're all here.

---

**You've reached the end of the Author Guide!** Return to:
- [Section 1: Getting Started](#1-getting-started) to begin authoring
- [Section 8: FAQ](#8-frequently-asked-questions) for quick answers
- [Section 9: Troubleshooting](#9-troubleshooting-common-issues) when stuck

**Other guides:**
- [USER_GUIDE.md](USER_GUIDE.md) - Overview of complete system
- [EDITOR_GUIDE.md](EDITOR_GUIDE.md) - For content editors
- [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) - For production staff
- [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md) - For knowledge base engineers

---

**Version:** 1.0 | **Last Updated:** November 6, 2025
**For more information:** See [README.md](README.md) | [USER_GUIDE.md](USER_GUIDE.md)
