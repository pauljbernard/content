# California Adoption Criteria
**State Board of Education Requirements**
**Source:** California Education Code
**Applies To:** All California instructional materials (all subjects)

---

## Overview

**California has specific adoption criteria** that all instructional materials must meet to be eligible for state adoption. These requirements apply to mathematics, ELA, science, and social studies programs.

**Core Principle:** Materials must align to California content standards, support English Learners, provide accessibility, and demonstrate quality instructional design.

---

## Key Differences from Texas

| Aspect | California | Texas |
|--------|-----------|-------|
| **Content Standards** | CCSS-based (Common Core State Standards) | TEKS (Texas Essential Knowledge and Skills) |
| **Language Standards** | ELD (English Language Development) | ELPS (English Language Proficiency Standards) |
| **Adoption Process** | State Board of Education review | SBOE review + local adoption |
| **Compliance** | CA Content Review Panel | IPACC review |

---

## California-Specific Requirements

### 1. Content Standards Alignment

**California uses:**
- **Mathematics:** CCSS-M (Common Core State Standards for Mathematics)
- **ELA:** CCSS-ELA + California additions
- **Science:** NGSS (Next Generation Science Standards) + California modifications
- **Social Studies:** California History-Social Science Standards

**Key Difference:** California adopted Common Core, Texas did not.

---

### 2. English Language Development (ELD) Standards

**California ELD Framework:**
- Part I: Interacting in Meaningful Ways
- Part II: Learning About How English Works
- Part III: Using Foundational Literacy Skills

**Proficiency Levels:**
- Emerging
- Expanding
- Bridging

**Similar to Texas ELPS but organized differently**

---

### 3. Accessibility Requirements

**California follows:**
- Section 508 compliance
- WCAG 2.1 AA standards
- Universal Design for Learning (UDL)

**Same as Texas in accessibility requirements**

---

### 4. Content Review Panel Criteria

**Mathematics materials evaluated on:**
- Standards alignment (CCSS-M)
- Mathematical practices implementation
- Coherence and progression
- Conceptual understanding emphasis
- Problem-solving opportunities
- Support for English Learners
- Assessment quality
- Digital-print alignment

---

## What Knowledge Reuses vs. What's California-Specific

### ✅ Reused from Universal/Common (No CA version needed):

- **DOK Framework** - Same DOK 1-4 levels (universal)
- **MLR (Mathematical Language Routines)** - Same routines (subject-common)
- **Assessment guidelines** - Parity, item types, scoring (universal)
- **UDL Principles** - Same principles (universal)
- **Accessibility** - Alt text, WCAG (universal)

### 🔧 California-Specific (Requires CA files):

- **CCSS-M Alignment** - Different from TEKS
- **ELD Integration** - California's version of language standards
- **California Content Review** - Different adoption process
- **Sample Items** - May need CA-specific examples

---

## Implementation Notes for Curriculum Developers

### When Creating California Math Lessons:

**Content Standards:**
- Tag with CCSS-M codes (not TEKS)
- Example: CCSS.MATH.CONTENT.5.NF.A.1

**Language Support:**
- Reference ELD standards (not ELPS)
- Use MLRs (same as Texas - math common)
- Provide EL scaffolds (same principles, different numbering)

**Assessment:**
- Same item types as Texas (universal)
- Same quality standards (universal)
- May have CA-specific item bank

**Examples:**
- Can use same mathematical contexts
- May want CA-specific real-world scenarios (CA geography, etc.)

---

## Knowledge Resolution Example

**Scenario:** Creating HMH Math CA Lesson 5.3

**Knowledge Needed:**
1. CCSS-M standards → `/subjects/mathematics/districts/california/ccss-m-alignment.md`
2. MLR6 Three Reads → `/subjects/mathematics/common/mlr/mlr6-three-reads.md` (reused!)
3. DOK Framework → `/universal/frameworks/dok-framework.md` (reused!)
4. ELD Standards → `/districts/california/language/eld-alignment.md`
5. Assessment guidelines → `/universal/assessment/` (all reused!)

**Result:** Only 2 CA-specific files needed; 90% of knowledge reused!

---

## Quick Reference

### California-Specific Files (Required):
- `ccss-m-alignment.md` - Content standards
- `eld-alignment.md` - Language standards
- `california-adoption-criteria.md` - This file

### Reused from Universal/Common:
- All MLR files (10 files)
- All assessment files (6 files)
- DOK, UDL, Accessibility (3 files)
- EB scaffolding principles (1 file)

**Total:** ~3 new files, ~20 files reused

---

## Resources

**California Department of Education:**
- CCSS-M: https://www.cde.ca.gov/be/st/ss/mathstandards.asp
- ELD Standards: https://www.cde.ca.gov/sp/el/er/eldstandards.asp
- Adoption Criteria: https://www.cde.ca.gov/ci/cr/cf/

**Related Guides:**
- ELD Alignment: `/districts/california/language/eld-alignment.md` (pending)
- CCSS-M Alignment: `/subjects/mathematics/districts/california/ccss-m-alignment.md` (pending)

---

**Remember:** California and Texas have different content standards and language frameworks, but share the same pedagogical approaches (MLR, UDL, DOK) and technical requirements (assessment, accessibility). The multi-curriculum architecture allows us to store shared knowledge once and reuse it across states.
