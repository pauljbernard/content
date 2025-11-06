# Knowledge Resolution Guide
**Multi-Curriculum Knowledge Base Architecture**
**Version:** 2.0
**Date:** 2025-11-06

---

## Overview

The HMH Knowledge Base uses a **hierarchical resolution system** that allows curriculum-specific, subject-specific, district-specific, and universal knowledge to coexist without duplication.

**Core Principle:** Knowledge is stored once at the most appropriate level, and retrieved through a resolution order that moves from specific to general.

---

## Architecture Design

### Directory Structure:

```
/reference/hmh-knowledge-v2/
├── universal/                    # Cross-everything knowledge
│   ├── frameworks/               # DOK, Accessibility
│   ├── vendor/                   # HMH QA processes
│   └── assessment/               # General assessment principles
│
├── subjects/                     # Subject-specific knowledge
│   ├── mathematics/
│   │   ├── common/               # All math programs (MLR, problem-solving)
│   │   └── districts/
│   │       ├── texas/            # Texas math specifics
│   │       ├── california/       # California math specifics
│   │       └── florida/          # Florida math specifics
│   │
│   ├── ela/
│   │   ├── common/               # All ELA programs (literacy routines)
│   │   └── districts/
│   │       └── texas/            # Texas ELA specifics
│   │
│   └── science/
│       └── common/               # All science programs
│
├── districts/                    # District/state-specific (cross-subject)
│   ├── texas/                    # IPACC, ELPS, SBOE, CEID
│   ├── california/               # California-specific requirements
│   └── florida/                  # Florida-specific requirements
│
└── publishers/                   # Publisher-specific
    └── hmh/                      # HMH-specific processes
```

---

## Knowledge Resolution Order

### How It Works:

When a skill needs knowledge, the system searches in order from **most specific** to **most general**:

1. **Program-District-Specific** (e.g., `/subjects/mathematics/districts/texas/into-math/`)
2. **Subject-District** (e.g., `/subjects/mathematics/districts/texas/`)
3. **Subject-Common** (e.g., `/subjects/mathematics/common/`)
4. **District-Wide** (e.g., `/districts/texas/`)
5. **Publisher-Wide** (e.g., `/publishers/hmh/`)
6. **Universal** (e.g., `/universal/`)

**First Match Wins:** The system returns the first file found in the resolution order.

---

## Configuration Files

### Curriculum Configuration:

Each curriculum combination has a JSON config file in `/config/curriculum/`:

**Example:** `hmh-math-tx.json`

```json
{
  "id": "hmh-into-math-tx",
  "subject": "mathematics",
  "district": "texas",
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

---

## File Placement Rules

### Rule 1: Universal Files

**Place in `/universal/` if:**
- Applies to ALL subjects AND ALL districts
- No customization needed
- Truly cross-curricular

**Examples:**
- DOK Framework (all subjects use DOK 1-4)
- WCAG Accessibility (same standards everywhere)
- UDL Principles (universal design)
- HMH Vendor QA Checklist (same process for all)

---

### Rule 2: Subject-Common Files

**Place in `/subjects/{subject}/common/` if:**
- Applies to ALL districts within one subject
- Subject-specific, but not district-specific

**Examples:**
- MLR (Mathematical Language Routines) - used in all math programs
- Problem-Solving Framework for Math
- Literacy Routines for ELA
- Science Inquiry Practices

---

### Rule 3: District-Wide Files

**Place in `/districts/{district}/` if:**
- Applies to ALL subjects within one district/state
- State law or policy, not subject-specific

**Examples:**
- Texas IPACC (applies to math, ELA, science, social studies)
- Texas ELPS (applies to all subjects)
- Texas SBOE Quality Rubric (all subjects)
- California ELD Standards (all subjects)

---

### Rule 4: Subject-District Files

**Place in `/subjects/{subject}/districts/{district}/` if:**
- Specific to one subject AND one district
- Customization for that combination

**Examples:**
- Texas TEKS Mathematics Standards
- Texas Math Gap Mitigation (SBOE-specific)
- California CCSS-M alignment
- Texas TEKS ELA Standards

---

### Rule 5: Program-Specific Files

**Place in `/subjects/{subject}/districts/{district}/{program}/` if:**
- Specific to one program within subject-district combination
- Into Math vs. other HMH math programs

**Examples:**
- Into Math TX specific lesson structure
- Into Reading TX specific routines
- Program-specific naming conventions

---

## Knowledge Migration Map

### Where Files Go (From Current to New Structure):

| Current File | New Location | Rationale |
|--------------|--------------|-----------|
| **Universal (Cross-Everything)** |||
| `vendor-qa/vendor-checklist-complete.md` | `/universal/vendor/` | HMH QA for all programs |
| `structure/content-block-schema.json` | `/publishers/hmh/` | HMH-specific structure |
| `assessment/dok-framework.md` | `/universal/frameworks/` | All subjects use DOK |
| `udl/udl-principles-guide.md` | `/universal/frameworks/` | Universal Design |
| `accessibility/alt-text-principles.md` | `/universal/assessment/` | WCAG for all |
| **Mathematics (All Districts)** |||
| `mlr/*.md` (all 9 files + placement) | `/subjects/mathematics/common/` | All math programs |
| `assessment/parity-guidelines.md` | `/universal/assessment/` | All subjects |
| `assessment/item-types-reference.md` | `/universal/assessment/` | All subjects |
| `assessment/scoring-rubrics-guide.md` | `/universal/assessment/` | All subjects |
| `assessment/validation-methods.md` | `/universal/assessment/` | All subjects |
| `assessment/learnosity-configuration-guide.md` | `/universal/assessment/` | Platform for all |
| `vocabulary/vocab-guidelines.md` | `/subjects/mathematics/common/` | Math-specific approach |
| **Texas (All Subjects)** |||
| `texas-compliance/ipacc-suitability-requirements.md` | `/districts/texas/` | All TX subjects |
| `texas-compliance/sboe-quality-rubric.md` | `/districts/texas/` | All TX subjects |
| `texas-compliance/texas-compliance-checklist.md` | `/districts/texas/` | All TX subjects |
| `language-support/elps-alignment.md` | `/districts/texas/` | All TX subjects |
| **Texas Mathematics** |||
| `texas-compliance/gap-mitigation-strategies.md` | `/subjects/mathematics/districts/texas/` | TX math SBOE gaps |
| **Language Support (Partial)** |||
| `language-support/eb-scaffolding-guide.md` | `/universal/frameworks/` | General EB principles |

---

## Resolution Examples

### Example 1: MLR6 (Three Reads)

**Request:** "Get knowledge about MLR6 for HMH Math TX"

**Resolution Order:**
1. `/subjects/mathematics/districts/texas/into-math/mlr6-three-reads.md` ❌ Not found
2. `/subjects/mathematics/districts/texas/mlr6-three-reads.md` ❌ Not found
3. `/subjects/mathematics/common/mlr6-three-reads.md` ✅ **FOUND**

**Result:** Returns math-common version (all math programs use same MLR6)

---

### Example 2: IPACC Requirements

**Request:** "Get IPACC requirements for HMH Math TX"

**Resolution Order:**
1. `/subjects/mathematics/districts/texas/into-math/ipacc-suitability-requirements.md` ❌ Not found
2. `/subjects/mathematics/districts/texas/ipacc-suitability-requirements.md` ❌ Not found
3. `/subjects/mathematics/common/ipacc-suitability-requirements.md` ❌ Not found
4. `/districts/texas/ipacc-suitability-requirements.md` ✅ **FOUND**

**Result:** Returns Texas-wide version (IPACC applies to all TX subjects)

---

### Example 3: DOK Framework

**Request:** "Get DOK framework for HMH ELA TX"

**Resolution Order:**
1. `/subjects/ela/districts/texas/into-reading/dok-framework.md` ❌ Not found
2. `/subjects/ela/districts/texas/dok-framework.md` ❌ Not found
3. `/subjects/ela/common/dok-framework.md` ❌ Not found
4. `/districts/texas/dok-framework.md` ❌ Not found
5. `/publishers/hmh/dok-framework.md` ❌ Not found
6. `/universal/frameworks/dok-framework.md` ✅ **FOUND**

**Result:** Returns universal version (DOK 1-4 same for all subjects/districts)

---

### Example 4: Texas Math Gap Mitigation

**Request:** "Get gap mitigation strategies for HMH Math TX"

**Resolution Order:**
1. `/subjects/mathematics/districts/texas/into-math/gap-mitigation-strategies.md` ❌ Not found
2. `/subjects/mathematics/districts/texas/gap-mitigation-strategies.md` ✅ **FOUND**

**Result:** Returns Texas Math version (specific to TX math SBOE gaps)

---

## Benefits of This Architecture

### 1. DRY (Don't Repeat Yourself)

**Problem Solved:** Without hierarchy, we'd duplicate DOK framework 9 times (TX/CA/FL × Math/ELA/Science)

**With Hierarchy:** DOK framework stored once in `/universal/`, used by all 9 combinations

---

### 2. Easy Maintenance

**Problem Solved:** If DOK framework changes, update 1 file instead of 9

**With Hierarchy:** Single source of truth for each piece of knowledge

---

### 3. Clear Ownership

**File Location = Scope:**
- `/universal/` = Everyone's responsibility
- `/districts/texas/` = Texas team's responsibility
- `/subjects/mathematics/` = Math team's responsibility

---

### 4. Scalable

**Adding New Combinations:**
- New district: Add `/districts/{new_district}/` with state-specific files
- New subject: Add `/subjects/{new_subject}/common/` with subject-specific files
- New combination: Create config file, existing knowledge auto-resolves

**Example:** Adding Florida Math = create config, most knowledge already exists

---

### 5. Override Capability

**If Texas Math needs different DOK examples:**
- Place `/subjects/mathematics/districts/texas/dok-framework.md`
- Resolution finds TX-specific version first
- Other combinations still use universal version

---

## Implementation Guidelines

### For Curriculum Developers:

**Step 1: Identify Scope**
Ask: "Who needs this knowledge?"
- Everyone? → `/universal/`
- All math? → `/subjects/mathematics/common/`
- All Texas? → `/districts/texas/`
- Texas math only? → `/subjects/mathematics/districts/texas/`

**Step 2: Check for Existing Knowledge**
Search resolution order before creating new files

**Step 3: Place File**
Put file at most general applicable level

**Step 4: Create Overrides Only When Needed**
Don't create district-specific version unless truly different

---

### For Skills:

**Skills Auto-Detect Curriculum:**
```python
# Skill reads project config
config = load_curriculum_config("hmh-math-tx")

# Skill queries knowledge system
mlr6_knowledge = resolve_knowledge(
    topic="mlr6-three-reads",
    resolution_order=config.knowledge_resolution.order
)

# System returns first match in resolution order
```

---

## Testing Knowledge Resolution

### Test Cases:

**Test 1: Universal Knowledge**
- Request DOK framework for Math TX → should find `/universal/frameworks/`
- Request DOK framework for ELA CA → should find same file
- ✅ Proves universal knowledge works across all combinations

**Test 2: Subject-Common Knowledge**
- Request MLR6 for Math TX → should find `/subjects/mathematics/common/`
- Request MLR6 for Math CA → should find same file
- Request MLR6 for ELA TX → should NOT find (ELA doesn't use MLR)
- ✅ Proves subject-common works across districts but not subjects

**Test 3: District-Wide Knowledge**
- Request IPACC for Math TX → should find `/districts/texas/`
- Request IPACC for ELA TX → should find same file
- Request IPACC for Math CA → should NOT find (California doesn't have IPACC)
- ✅ Proves district-wide works across subjects but not districts

**Test 4: Specific Knowledge**
- Request TX Math gaps for Math TX → should find `/subjects/mathematics/districts/texas/`
- Request TX Math gaps for Math CA → should NOT find
- Request TX Math gaps for ELA TX → should NOT find
- ✅ Proves subject-district specificity works

---

## Validation Checklist

### Before Adding New File:

- [ ] Determined appropriate scope (universal, subject, district, specific)
- [ ] Checked resolution order for existing file
- [ ] Placed file at most general applicable level
- [ ] Avoided duplication
- [ ] Documented in this guide if new pattern

### Before Migrating Existing File:

- [ ] Identified file's true scope
- [ ] Checked if other combinations need it
- [ ] Placed in appropriate location
- [ ] Updated any references to old path
- [ ] Tested resolution for affected combinations

---

## Quick Reference

### File Placement Decision Tree:

```
START: Where should this file go?

├─ Applies to ALL subjects AND ALL districts?
│  └─ YES → /universal/
│
├─ Applies to ALL districts in ONE subject?
│  └─ YES → /subjects/{subject}/common/
│
├─ Applies to ALL subjects in ONE district?
│  └─ YES → /districts/{district}/
│
├─ Applies to ONE subject in ONE district?
│  └─ YES → /subjects/{subject}/districts/{district}/
│
└─ Applies to ONE program?
   └─ YES → /subjects/{subject}/districts/{district}/{program}/
```

---

## Migration Checklist

### Phase 1: Universal Files (Done First)
- [ ] DOK Framework
- [ ] UDL Principles
- [ ] Alt Text Principles
- [ ] Vendor Checklist
- [ ] Assessment guides (parity, item types, scoring, validation, Learnosity)

### Phase 2: Subject-Common Files
- [ ] All 10 MLR files (math common)
- [ ] Math Vocabulary Guidelines

### Phase 3: District-Wide Files
- [ ] IPACC Requirements (Texas)
- [ ] SBOE Quality Rubric (Texas)
- [ ] Texas Compliance Checklist (Texas)
- [ ] ELPS Alignment (Texas)

### Phase 4: Subject-District Files
- [ ] Texas Math Gap Mitigation

### Phase 5: Test Resolution
- [ ] Test universal knowledge retrieval
- [ ] Test subject-common retrieval
- [ ] Test district-wide retrieval
- [ ] Test subject-district retrieval
- [ ] Document any issues

---

## Future Expansion

### Adding California Mathematics:

**Required:**
1. Create `/subjects/mathematics/districts/california/` directory
2. Add California-specific files:
   - `ccss-m-alignment.md` (California content standards)
   - `ca-adoption-criteria.md` (California-specific requirements)
3. Create curriculum config: `hmh-math-ca.json`

**Reused (no new files needed):**
- All MLR files (subject-common)
- DOK framework (universal)
- Assessment guides (universal)
- UDL, Accessibility (universal)

**Estimated:** 3-5 new files, ~40 files reused

---

### Adding Texas ELA:

**Required:**
1. Create `/subjects/ela/common/` directory
2. Add ELA-specific files:
   - Literacy routines (ELA equivalent of MLR)
   - ELA problem-solving framework
3. Create `/subjects/ela/districts/texas/` directory
4. Add Texas ELA files:
   - `teks-ela-alignment.md`
   - `ela-gap-mitigation.md`
5. Create curriculum config: `hmh-ela-tx.json`

**Reused (no new files needed):**
- IPACC, SBOE, ELPS (district-wide Texas)
- DOK, UDL, Accessibility (universal)
- Assessment guides (universal)

**Estimated:** 8-12 new files, ~35 files reused

---

## Resources

**Configuration Files:**
- HMH Math TX: `/config/curriculum/hmh-math-tx.json`
- HMH Math CA: `/config/curriculum/hmh-math-ca.json`
- HMH ELA TX: `/config/curriculum/hmh-ela-tx.json`

**Knowledge Directories:**
- Universal: `/reference/hmh-knowledge-v2/universal/`
- Subjects: `/reference/hmh-knowledge-v2/subjects/`
- Districts: `/reference/hmh-knowledge-v2/districts/`
- Publishers: `/reference/hmh-knowledge-v2/publishers/`

**Migration Tools:**
- Migration script: (pending)
- Validation script: (pending)
- Resolution test suite: (pending)

---

**Remember:** The goal is to store knowledge once at the most appropriate level, and retrieve it through a clear resolution order. This architecture enables scaling to dozens of curriculum combinations without duplicating content or losing subject/district specificity.
