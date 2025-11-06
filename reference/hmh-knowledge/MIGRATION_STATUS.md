# Knowledge Base Migration Status
**From:** `/reference/hmh-knowledge/` (v1 - single curriculum)
**To:** `/reference/hmh-knowledge-v2/` (v2 - multi-curriculum)
**Date Started:** 2025-11-06
**Total Files to Migrate:** 27

---

## Migration Plan

### Phase 1: Universal Files (Highest Priority)
**Target:** `/universal/` directory
**Files:** 10 files

| # | Source File | Destination | Status |
|---|-------------|-------------|--------|
| 1 | `assessment/dok-framework.md` | `/universal/frameworks/` | ⏳ Pending |
| 2 | `udl/udl-principles-guide.md` | `/universal/frameworks/` | ⏳ Pending |
| 3 | `accessibility/alt-text-principles.md` | `/universal/assessment/` | ⏳ Pending |
| 4 | `assessment/parity-guidelines.md` | `/universal/assessment/` | ⏳ Pending |
| 5 | `assessment/item-types-reference.md` | `/universal/assessment/` | ⏳ Pending |
| 6 | `assessment/scoring-rubrics-guide.md` | `/universal/assessment/` | ⏳ Pending |
| 7 | `assessment/validation-methods.md` | `/universal/assessment/` | ⏳ Pending |
| 8 | `assessment/learnosity-configuration-guide.md` | `/universal/assessment/` | ⏳ Pending |
| 9 | `vendor-qa/vendor-checklist-complete.md` | `/universal/vendor/` | ⏳ Pending |
| 10 | `language-support/eb-scaffolding-guide.md` | `/universal/frameworks/` | ⏳ Pending |

---

### Phase 2: Mathematics Common Files
**Target:** `/subjects/mathematics/common/` directory
**Files:** 11 files (all MLR + vocab)

| # | Source File | Destination | Status |
|---|-------------|-------------|--------|
| 11 | `mlr/mlr-overview.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 12 | `mlr/mlr1-stronger-clearer.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 13 | `mlr/mlr2-collect-display.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 14 | `mlr/mlr3-critique-correct-clarify.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 15 | `mlr/mlr4-information-gap.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 16 | `mlr/mlr5-co-craft-questions.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 17 | `mlr/mlr6-three-reads.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 18 | `mlr/mlr7-compare-connect.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 19 | `mlr/mlr8-discussion-supports.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 20 | `mlr/mlr-placement-rules.md` | `/subjects/mathematics/common/mlr/` | ⏳ Pending |
| 21 | `vocabulary/vocab-guidelines.md` | `/subjects/mathematics/common/` | ⏳ Pending |

---

### Phase 3: Texas District-Wide Files
**Target:** `/districts/texas/` directory
**Files:** 5 files

| # | Source File | Destination | Status |
|---|-------------|-------------|--------|
| 22 | `texas-compliance/ipacc-suitability-requirements.md` | `/districts/texas/compliance/` | ⏳ Pending |
| 23 | `texas-compliance/sboe-quality-rubric.md` | `/districts/texas/compliance/` | ⏳ Pending |
| 24 | `texas-compliance/texas-compliance-checklist.md` | `/districts/texas/compliance/` | ⏳ Pending |
| 25 | `language-support/elps-alignment.md` | `/districts/texas/language/` | ⏳ Pending |
| 26 | `structure/content-block-schema.json` | `/publishers/hmh/` | ⏳ Pending |

---

### Phase 4: Texas Mathematics Files
**Target:** `/subjects/mathematics/districts/texas/` directory
**Files:** 1 file

| # | Source File | Destination | Status |
|---|-------------|-------------|--------|
| 27 | `texas-compliance/gap-mitigation-strategies.md` | `/subjects/mathematics/districts/texas/` | ⏳ Pending |

---

## Migration Progress

**Total:** 0 / 27 files migrated (0%)

**By Phase:**
- Phase 1 (Universal): 0 / 10 (0%)
- Phase 2 (Math Common): 0 / 11 (0%)
- Phase 3 (Texas Wide): 0 / 5 (0%)
- Phase 4 (Texas Math): 0 / 1 (0%)

---

## Post-Migration Tasks

### Validation:
- [ ] All 27 files successfully copied
- [ ] Directory structure correct
- [ ] No broken internal links
- [ ] Resolution order tested

### Documentation:
- [ ] Update references in configuration files
- [ ] Create index files for each directory
- [ ] Document migration decisions

### Testing:
- [ ] Test Math TX resolution
- [ ] Test Math CA resolution (with placeholders)
- [ ] Test ELA TX resolution (with placeholders)
- [ ] Validate fallback behavior

---

## Notes

### File Modifications During Migration:
- Some files may need path updates in cross-references
- Internal links should be updated if they reference other files
- Relative paths may need adjustment

### Deferred:
- Old `/reference/hmh-knowledge/` directory will remain until validation complete
- Once validated, old directory can be archived or removed

---

**Last Updated:** 2025-11-06
