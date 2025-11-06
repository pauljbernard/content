# Content Editor Guide
**HMH Multi-Curriculum Knowledge Base - For Content Editors**
**Version:** 1.0
**Last Updated:** November 6, 2025

---

## Welcome to the Editorial Team

As a content editor, you ensure authored content meets quality standards before publication. You are the **quality gate** between draft content and published materials.

Your reviews maintain consistency, pedagogical soundness, and compliance across all HMH educational products.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Editorial Workflow](#2-editorial-workflow)
3. [Content Review Checklist](#3-content-review-checklist)
4. [Providing Effective Feedback](#4-providing-effective-feedback)
5. [Approval Process](#5-approval-process)
6. [Common Issues and Fixes](#6-common-issues-and-fixes)

---

## 1. Getting Started

### Your Responsibilities

**Content Review:**
- Verify standards alignment
- Check pedagogical soundness
- Ensure accessibility compliance
- Validate cultural responsiveness
- Confirm state compliance

**Feedback and Communication:**
- Provide clear, actionable feedback
- Explain rationale for changes
- Collaborate to improve quality
- Approve when standards met

**Process Management:**
- Track content through review cycles
- Enforce deadlines
- Escalate issues when needed
- Maintain consistency

### Your Tools

1. **Editorial Checklist** - Standardized review criteria (Section 3)
2. **Knowledge Base** - Reference for standards (`/reference/hmh-knowledge-v2/`)
3. **GitHub** - Review, comments, approval workflow
4. **Style Guides** - HMH editorial standards

### Workflow Overview

```
1. Author submits (Pull Request)
   ↓
2. Editor receives notification
   ↓
3. Editor reviews using checklist
   ↓
4. Editor provides feedback
   ↓
5. Author revises
   ↓
6. Editor re-reviews
   ↓
7. Approve and merge OR return to step 4
```

---

## 2. Editorial Workflow

### Step 1: Receive Assignment

**Notification Methods:**
- Author tags you in pull request
- Content team assigns review
- GitHub notification

**Initial Actions:**
- [ ] Review PR description
- [ ] Check content brief
- [ ] Identify curriculum config
- [ ] Note timeline/deadline
- [ ] Acknowledge receipt

### Step 2: Preliminary Review (15-30 min)

**Quick Scan:**
- [ ] All required files present?
- [ ] Follows template structure?
- [ ] Length appropriate?
- [ ] Obvious errors?

**If Major Issues:**
- Return to author immediately
- Provide high-level feedback
- Example: "Missing answer key" or "Wrong grade level"

**If Passes:**
- Proceed to detailed review

### Step 3: Detailed Review (1-3 hours)

**Use Editorial Checklist** (Section 3)

Review across 7 quality pillars:
1. Standards Alignment
2. Pedagogical Soundness
3. Language Support
4. UDL
5. Accessibility
6. Cultural Responsiveness
7. State Compliance

**Document Findings:**
- Leave specific comments in GitHub
- Use line-by-line comments for specific issues
- Use general comments for big-picture feedback
- Mark status: "Requires Changes" or "Approved"

### Step 4: Provide Feedback (30-60 min)

**Effective Feedback:**
- **Specific:** "Add alt text to Figure 3" not "Fix images"
- **Actionable:** "Change sentence frame to ___" not "Needs work"
- **Constructive:** Explain why
- **Prioritized:** Critical vs. optional

**Template:**
```markdown
## Review Summary

**Status:** Requires Revisions / Approved with Minor Changes / Approved

**Strengths:**
- [Positive aspect 1]
- [Positive aspect 2]

**Required Changes:**
1. [Critical issue with explanation]
2. [Critical issue with explanation]

**Suggested Changes:**
1. [Optional improvement]
2. [Optional improvement]

**Questions:**
- [Clarification needed]
```

### Step 5: Author Revises

- Author receives feedback
- Author makes revisions
- Author responds to comments
- Author pushes updated version

**Your Role:**
- Answer questions promptly
- Clarify feedback if unclear
- Be available for consultation

### Step 6: Re-Review (30-60 min)

**Focus:**
- Did author address required changes?
- Are revisions acceptable?
- Any new issues introduced?

**Outcomes:**
- **Approved:** Merge PR
- **More Revisions:** Focused feedback, return to Step 5
- **Escalate:** If issues persist after 2-3 cycles

### Step 7: Approval and Merge

**When standards met:**
- [ ] Leave approval comment
- [ ] Change PR status to "Approved"
- [ ] Merge pull request
- [ ] Content moves to `/published/`
- [ ] Thank author

---

## 3. Content Review Checklist

### Section 1: Standards Alignment

**Standards Addressed:**
- [ ] All standards from brief addressed
- [ ] No extraneous standards
- [ ] Standards correctly interpreted (check KB alignment file)
- [ ] Depth appropriate

**Learning Objectives:**
- [ ] Measurable (Bloom's Taxonomy verbs)
- [ ] Map directly to standards
- [ ] Student-facing ("Students will...")
- [ ] Grade-appropriate

**Assessment Alignment:**
- [ ] Assessments measure objectives/standards
- [ ] Doesn't test unrelated skills
- [ ] DOK level matches standard

**Reference:**
- `/subjects/[subject]/districts/[state]/[standards-file].md`
- `/universal/frameworks/dok-framework.md`

---

### Section 2: Pedagogical Soundness

**Instructional Sequence:**
- [ ] Gradual release (I do, We do, You do)
- [ ] Warm-up activates prior knowledge
- [ ] Direct instruction includes modeling
- [ ] Guided practice scaffolded
- [ ] Independent practice individual
- [ ] Closure summarizes and checks understanding

**Instructional Routines:**
- [ ] Routine applied correctly (check KB file)
- [ ] All steps present
- [ ] Timing appropriate
- [ ] Facilitation notes clear

**Example Checks for MLRs:**
- [ ] MLR1: 3 rounds of "Stronger and Clearer Each Time"
- [ ] MLR2: Clear protocol for collecting/displaying language
- [ ] MLR8: Discussion supports explicitly taught

**Example Checks for Literacy Routines:**
- [ ] Close Reading: 3 reads present (literal, craft, inference)
- [ ] Think-Pair-Share: All 3 phases structured
- [ ] Annotation: Symbol system introduced

**Formative Assessment:**
- [ ] Checks every 10-15 minutes
- [ ] Multiple check types
- [ ] Clear success criteria
- [ ] Notes on responding to errors

**Misconceptions:**
- [ ] Common misconceptions anticipated
- [ ] Strategies to address provided
- [ ] Examples and non-examples clarify

**Differentiation:**
- [ ] Three levels: Below, On, Above
- [ ] Scaffolds specific and appropriate
- [ ] Extensions provide genuine challenge

**Reference:**
- `/subjects/mathematics/common/mlr/*.md`
- `/subjects/ela/common/literacy-routines/*.md`
- `/subjects/science/common/science-practices-framework.md`

---

### Section 3: Language Support

**Standards Addressed:**
- [ ] ELPS/ELD/ESOL standards addressed
- [ ] All 4 domains if applicable (Listening, Speaking, Reading, Writing)

**Scaffolds for Emergent Bilinguals:**
- [ ] Differentiated for Beginning, Intermediate, Advanced
- [ ] Beginning: Heavy visual, sentence frames, simplified language
- [ ] Intermediate: Sentence frames, visual support, vocabulary
- [ ] Advanced: Academic discourse frames, vocabulary

**Sentence Frames:**
- [ ] Provided for academic discourse
- [ ] From sentence frames library (or equivalent)
- [ ] Match language function (explaining, justifying, comparing)

**Vocabulary:**
- [ ] Key academic vocabulary identified
- [ ] Explicitly taught (not assumed)
- [ ] Visual supports provided
- [ ] Glossary or word wall included

**Language Routines:**
- [ ] MLRs used (math)
- [ ] Partner/group structures support language
- [ ] Strategic grouping for practice

**Reference:**
- `/districts/texas/language/elps-alignment.md`
- `/districts/california/language/eld-alignment.md`
- `/districts/florida/language/esol-alignment.md`
- `/universal/frameworks/eb-scaffolding-guide.md`
- `/universal/frameworks/sentence-frames-library.md`

---

### Section 4: UDL

**Multiple Means of Representation:**
- [ ] Concepts in ≥ 2 modalities (visual + verbal, etc.)
- [ ] Visual supports for key concepts
- [ ] Options for perception

**Multiple Means of Action/Expression:**
- [ ] Student choices in demonstrating learning
- [ ] Options: verbal, written, drawn, modeled
- [ ] Tools/supports accessible

**Multiple Means of Engagement:**
- [ ] Connects to students' lives
- [ ] Options for different challenge levels
- [ ] Choice embedded where appropriate

**Reference:** `/universal/frameworks/udl-principles-guide.md`

---

### Section 5: Accessibility

**Images:**
- [ ] Every image has descriptive alt text
- [ ] Alt text describes content and function
- [ ] Complex images have extended descriptions
- [ ] Decorative images marked

**Color and Contrast:**
- [ ] Contrast ratio ≥ 4.5:1 (normal text)
- [ ] Contrast ratio ≥ 3:1 (large text)
- [ ] Information not conveyed by color alone

**Structure:**
- [ ] Headings properly nested (H1 → H2 → H3)
- [ ] Lists use proper markup
- [ ] Tables have headers
- [ ] Links descriptive

**Interactivity:**
- [ ] Keyboard-accessible
- [ ] Forms have labels
- [ ] No flashing content

**Text:**
- [ ] Selectable and scalable
- [ ] Font size ≥ 12pt
- [ ] Line spacing ≥ 1.5x

**Tools:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [WAVE Tool](https://wave.webaim.org/)

**Reference:** `/universal/accessibility/wcag-compliance-guide.md`

---

### Section 6: Cultural Responsiveness

**Representation:**
- [ ] Diverse names (multiple cultures)
- [ ] Varied family structures
- [ ] Diverse economic contexts
- [ ] Images show diverse people

**Stereotypes:**
- [ ] No gender stereotypes
- [ ] No racial/ethnic stereotypes
- [ ] No ability stereotypes
- [ ] No family structure stereotypes
- [ ] No socioeconomic stereotypes

**Contexts:**
- [ ] Culturally inclusive
- [ ] Relevant to diverse experiences
- [ ] No assumptions about backgrounds

**CEID 11 Categories:**
1. Ageism - [ ] Age-appropriate
2. Classism - [ ] Economic diversity
3. Gender Bias - [ ] Gender balance
4. Regional Bias - [ ] No geography assumptions
5. Language Bias - [ ] Respectful of multilingualism
6. Religious Bias - [ ] Inclusive, secular
7. Racial/Ethnic Bias - [ ] Diverse, no stereotypes
8. Sexual Orientation Bias - [ ] Inclusive families
9. Exceptionality Bias - [ ] Positive disability representation
10. Body Type Bias - [ ] Diverse body types
11. Situational Bias - [ ] Diverse life situations

**Reference:** `/universal/content-equity/ceid-guidelines.md`

---

### Section 7: State Compliance

**Texas:**
- [ ] SBOE Quality Rubric criteria 1-5
- [ ] IPACC suitability requirements
- [ ] Content restrictions complied with
- [ ] ELPS standards addressed

**California:**
- [ ] Adoption criteria met
- [ ] ELD Standards addressed
- [ ] Content suitable

**Florida:**
- [ ] Statutory compliance (F.S. 1006.31-1006.40)
- [ ] B.E.S.T./MAFS standards addressed
- [ ] ESOL/WIDA supports present

**Reference:**
- `/districts/texas/compliance/sboe-quality-rubric.md`
- `/districts/texas/compliance/ipacc-suitability-requirements.md`
- `/districts/california/compliance/california-adoption-criteria.md`
- `/districts/florida/compliance/florida-adoption-criteria.md`

---

### Section 8: Technical Quality

**Writing:**
- [ ] Spelling correct
- [ ] Grammar correct
- [ ] Punctuation correct
- [ ] Style consistent with HMH standards

**Formatting:**
- [ ] Headings used correctly
- [ ] Lists formatted consistently
- [ ] Tables formatted properly
- [ ] Indentation consistent

**Completeness:**
- [ ] All template sections present
- [ ] No "[TBD]" or placeholders
- [ ] Answer key complete
- [ ] Metadata complete

**Assets:**
- [ ] All images specified or included
- [ ] Descriptions clear for designers
- [ ] Materials clearly listed

---

## 4. Providing Effective Feedback

### Principles

**1. Be Specific**
❌ "This section needs work."
✅ "Guided practice needs scaffolding. Add sentence frames for Beginning ELLs and graphic organizer for Intermediate ELLs."

**2. Be Actionable**
❌ "Language support is weak."
✅ "Add ELPS 3.E scaffolds: Beginning needs visual models and frame 'I see ___ because ___.'"

**3. Explain Why**
❌ "Change this problem."
✅ "Change this problem. Context assumes amusement park visit (CEID: classism). Use school playground instead."

**4. Balance Critical and Positive**
Always start with strengths.

**5. Prioritize**
Separate "must fix" from "nice to have."

### Feedback Template: Lessons

```markdown
## Editorial Review: [Lesson Title]

**Reviewer:** [Name]
**Date:** [Date]
**Status:** ❌ Requires Revisions / ⚠️ Minor Changes / ✅ Approved

---

### Strengths
- Strong MLR2 use in guided practice - clear protocol
- Excellent differentiation with graphic organizer
- Formative checks embedded throughout
- Complete answer key

---

### Required Changes (Must Fix)

#### 1. Standards Alignment
**Issue:** Objective 2 doesn't map to TEKS.5.NF.1.1.
**Fix:** Revise to: "Students will add fractions with unlike denominators using visual models."
**Reference:** `/subjects/mathematics/districts/texas/teks-math-alignment.md` line 487

#### 2. ELPS Scaffolding
**Issue:** Missing Beginning level scaffolds in warm-up.
**Fix:** Add frame: "I think ___ because ___." Provide visual model.
**Reference:** ELPS 3.E requires Beginning sentence frames.

#### 3. Accessibility
**Issue:** Figure 2 has no alt text.
**Fix:** Add: "Two fraction bars showing 1/3 shaded blue and 1/4 shaded red with twelfths grid."
**Reference:** WCAG 2.1 SC 1.1.1

---

### Suggested Changes (Optional)

#### 1. UDL Enhancement
**Suggestion:** In independent practice, offer choice: visual models, number lines, OR algorithms. Currently only algorithm.
**Benefit:** Multiple means of action/expression.

#### 2. Misconception Addressing
**Suggestion:** Add teacher note about "adding across" error. Ask "Does 1/2 + 1/3 = 2/5?" to surface misconception.
**Benefit:** Proactively addresses predictable error.

---

### Questions
1. Exit ticket mentioned (line 287) - provided separately or included?
2. Warm-up references "yesterday's lesson" - correct sequencing?

---

### Next Steps
Address 3 required changes and answer questions. Suggested changes optional but recommended. Tag me when revised.

Time estimate: 30-45 min

Great work on instructional routines!
```

### Feedback Template: Assessments

```markdown
## Editorial Review: [Assessment Title]

**Status:** ❌ Requires Revisions / ✅ Approved

---

### Strengths
- Blueprint alignment excellent
- Rubrics detailed and clear
- Distractors address real misconceptions

---

### Required Changes

#### Item 7
**Issue:** Distractor C not plausible.
**Fix:** Change to "1 1/7 yards" (common error).
**Rationale:** Addresses treating fractions like whole numbers.

#### Item 12
**Issue:** Assumes students have pets (CEID: situational bias).
**Fix:** Use school supplies or classroom materials.

#### Item 18
**Issue:** Rubric doesn't specify scoring if correct answer without work.
**Fix:** Add: "Correct answer without explanation: maximum 2 points."

---

### Accessibility

#### Item 3
**Issue:** Graph has no alt text.
**Fix:** Add: "Bar graph showing Amy 85, Juan 90, Chen 78."

#### Item 15
**Issue:** Color-coded choices (green/red) convey information.
**Fix:** Add text labels OR remove color.

---

Great rubrics - very clear for scoring!
```

### Common Scenarios

**Scenario 1: Missing KB Application**

**Feedback:**
"MLR1 in guided practice is missing Round 3. Per `/subjects/mathematics/common/mlr/mlr1-stronger-clearer.md`, MLR1 requires:
1. Individual think
2. Partner A shares, B responds
3. **Partners switch and refine**

Please add Round 3 for students to refine explanations."

**Scenario 2: Standards Misalignment**

**Feedback:**
"This lesson addresses TEKS.5.NF.1.1 but practice uses only denominators 2, 3, 6 (all factor to 6).

Per `/subjects/mathematics/districts/texas/teks-math-alignment.md` (line 492), 5th grade includes denominators requiring LCM like 4 and 6 (LCM 12) or 3 and 5 (LCM 15).

Revise 30% of problems to include complex denominators."

**Scenario 3: Accessibility Gap**

**Feedback:**
"Figure 3 color codes answers (green = correct, red = incorrect). This creates barrier for colorblind users (8% of males).

Per `/universal/accessibility/wcag-compliance-guide.md` (WCAG 1.4.1), information cannot be by color alone.

**Fix:** Add text labels: ✓ Correct and ✗ Incorrect OR use shape + color."

**Scenario 4: Missing ELL Scaffolds**

**Feedback:**
"Lesson addresses ELPS 4.G but no scaffolds for Beginning/Intermediate ELLs during read-aloud (lines 145-178).

Per `/districts/texas/language/elps-alignment.md`:
- **Beginning:** Provide visual cards, allow pointing/single words
- **Intermediate:** Frame: 'The character feels ___ because ___.'"

---

## 5. Approval Process

### When to Approve

**Ready for approval when:**
- [ ] All required changes addressed
- [ ] Meets all 7 quality pillars
- [ ] Author responded to questions
- [ ] No outstanding concerns

**"Almost there":**
- Use **"Approved with Minor Changes"**
- List minor changes
- Trust author to make them
- No re-review needed

**Fundamental issues:**
- Do NOT approve
- Provide clear feedback
- Set expectations

### Approval Steps

**Step 1: Final Review**
- Re-read with fresh eyes
- Verify all changes made
- Check for new issues

**Step 2: Approval Comment**
```markdown
## ✅ APPROVED

Meets all quality standards. Ready for publication.

### Revisions Completed
- Added ELPS scaffolds ✓
- Revised Learning Objective 2 ✓
- Added alt text to images ✓
- Addressed misconception ✓

### Final Notes
- Excellent MLR2 use - model for others
- Strong differentiation
- Clear teacher notes

Merging to /published/. Great work!
```

**Step 3: Merge PR**
- Click "Approve"
- Merge pull request
- Content moves to `/published/`
- Notify author

**Step 4: Document (if applicable)**
- Note exemplary features for training
- Document creative solutions

---

## 6. Common Issues and Fixes

### Issue 1: Weak Learning Objectives

**Problem:**
❌ "Students will understand fractions."

**Fix:**
✅ "Students will compare fractions with unlike denominators using visual models and explain their reasoning."

Use Bloom's Taxonomy action verbs.

**Reference:** `/universal/frameworks/dok-framework.md`

---

### Issue 2: Missing Misconceptions

**Problem:** Doesn't anticipate errors.

**Fix:** For fractions, "adding across" (1/2 + 1/3 = 2/5) is most common.

Add note: "Watch for adding across. Ask: 'Does 1/2 + 1/3 = 2/5? Test with pizza.' Cognitive conflict helps."

---

### Issue 3: Generic Sentence Frames

**Problem:**
❌ "I think ___."

**Fix:**
✅ "To find the common denominator, I need to ___."
✅ "I know my answer is reasonable because ___."

Make frames task-specific.

**Reference:** `/universal/frameworks/sentence-frames-library.md`

---

### Issue 4: Poor Alt Text

**Problem:**
❌ "Image of fractions"

**Fix:**
✅ "Two fraction bars aligned vertically. Top shows 2/3 shaded blue. Bottom shows 3/4 shaded red. Both have twelfths grid."

Describe content and function.

**Reference:** `/universal/accessibility/wcag-compliance-guide.md`

---

### Issue 5: Token Diversity

**Problem:** Limited diversity - all English names, affluent contexts.

**Fix:**
- Use diverse names (African, Asian, Latinx, European)
- Vary contexts: public parks not country clubs, public library not home office

**Reference:** `/universal/content-equity/ceid-guidelines.md`

---

### Issue 6: Incorrect Routine

**Problem:** Says MLR1 but protocol doesn't match.

**Fix:** Consult MLR file. **MLR1 requires:**
1. Individual think
2. Partner A shares (1 min)
3. Partner B responds (30 sec)
4. Switch roles
5. Individual revision

If missing steps, revise OR choose different routine.

**Reference:** `/subjects/mathematics/common/mlr/mlr1-stronger-clearer.md`

---

### Issue 7: Answer Key Errors

**Problem:** Incorrect answer or incomplete solution.

**Fix:**
- Solve every problem yourself
- Check author's key
- Provide correct solution with explanation

**Critical:** Never approve with answer key errors. Undermines teacher trust.

---

## Quick Reference

### Knowledge Base Locations

**Universal:**
- `/universal/frameworks/` - UDL, DOK, EB, sentence frames
- `/universal/assessment/` - Item types, rubrics, keys
- `/universal/accessibility/` - WCAG
- `/universal/content-equity/` - CEID

**Subject-Common:**
- `/subjects/mathematics/common/mlr/` - MLRs
- `/subjects/ela/common/literacy-routines/` - Literacy routines
- `/subjects/science/common/` - NGSS, practices

**District-Wide:**
- `/districts/texas/` - ELPS, SBOE, IPACC
- `/districts/california/` - ELD, adoption criteria
- `/districts/florida/` - ESOL, adoption criteria

**Subject-District:**
- `/subjects/[subject]/districts/[state]/` - Standards alignment

### Review Times

- **Preliminary Review:** 15-30 min
- **Detailed Review:** 1-3 hours (lessons), 1-2 hours (assessments)
- **Feedback Writing:** 30-60 min
- **Re-Review:** 30-60 min

### Common Actions

**Approve:**
```bash
# In GitHub PR
1. Click "Review changes"
2. Select "Approve"
3. Click "Submit review"
4. Click "Merge pull request"
```

**Request Changes:**
```bash
# In GitHub PR
1. Add line comments on specific issues
2. Add general comment with summary
3. Click "Review changes"
4. Select "Request changes"
5. Click "Submit review"
```

---

## Support

- **Knowledge Base Questions:** See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)
- **Author Questions:** See [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)
- **Production Questions:** See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
- **Style Guide:** HMH editorial standards
- **Technical Issues:** Create issue in GitHub

---

**Version:** 1.0 | **Last Updated:** November 6, 2025
**For more information:** See [README.md](README.md) | [USER_GUIDE.md](USER_GUIDE.md)
