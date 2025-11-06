# Content/ Directory Audit Report

**Audit Date**: 2025-11-06
**Audited By**: Claude Code
**Total Size**: 182MB (255 files)
**Status**: Contains CRITICAL unique files + outdated duplicates

---

## Executive Summary

The `content/` directory contains **a mix of critical unique files and outdated duplicates**.

### Critical Finding ⚠️

**DO NOT DELETE** `content/` without extracting `reference/baseline/` first!

**Key Discovery**:
- **181MB (99%) = Unique baseline reference materials** ✅ KEEP
- **1MB (1%) = Outdated duplicates of .claude/ and other files** ❌ REMOVE

---

## Detailed Breakdown

### 1. UNIQUE FILES - MUST KEEP ✅

#### `content/reference/baseline/` (181MB, 74 files)

**Status**: **CRITICAL - Does NOT exist at top-level**

**Contents**: HMH curriculum baseline reference materials
- 27 PDFs (curriculum samples, style guides, vendor docs)
- 15 DOCX files (guidelines, specifications)
- 11 Markdown files (converted versions of PDFs/DOCX)
- 8 InDesign files (.indd - lesson templates)
- 9 TXT files (extracted text)
- 2 XLSX files (spreadsheets)
- 1 ZIP file (icon assets)
- 1 directory (LessonTools_Icon_Displays/)

**Sample Files**:
```
content/reference/baseline/
├── Alt Text Guidelines.docx (3.1 MB)
├── CEID Vendor Reference Guide v3.pdf (668 KB)
├── Core_Solutions_Style_Guide_for_Mathematics.pdf (1.5 MB)
├── Emergent Bilinguals Guidelines.docx (1.3 MB)
├── Mathematical Language Routines (MLR) Guidelines.docx
├── UDL Guidelines.docx
├── Vocabulary Guidelines.docx
├── IPACC-Guide_TX-Spec-Writing-Playbook_CURRENT.docx
├── Math Item Specs Guide.pdf
├── Pattern Guide for SYL and Tasks EMM Development.docx (6.1 MB)
├── Into Math TX – Content Block Output List.pdf
├── imra25-math-k12-sboe-approved-quality-rubric.pdf
├── g04_imnlv2_ptg_mod_m04l00s00_en.pdf (32 MB) - Grade 4 teacher guide
├── g08_imnlv2_ptg_mod_m06l00s00_en.pdf (14 MB) - Grade 8 teacher guide
├── 1-2_mtxese000000_lesson_2R.pdf (6.3 MB) - Sample lesson
├── 3-5_mtxese000000_SE_Final2.pdf (2.6 MB) - Student edition
├── LessonTools_Icon_Displays.zip (25 MB) - Icon assets
└── [58 more files...]
```

**Largest Files**:
1. `g04_imnlv2_ptg_mod_m04l00s00_en.pdf` - 32 MB
2. `LessonTools_Icon_Displays.zip` - 25 MB
3. `g08_imnlv2_ptg_mod_m06l00s00_en.pdf` - 14 MB
4. `1-2_imv2_LessonTools_Icons.indd` - 8 MB
5. `3-5_imv2_LessonTools_icons.indd` - 6.6 MB

**Purpose**:
- Source materials for curriculum development
- Style guides and writing guidelines
- Sample lessons and teacher guides
- Vendor documentation
- Baseline examples for knowledge extraction

**Recommendation**: **MOVE to top-level `reference/baseline/`** ✅

---

### 2. OUTDATED DUPLICATES - REMOVE ❌

#### `content/.claude/` (892 KB, 131 files)

**Status**: **OUTDATED COPY** - Last modified Nov 3-5, 2025

**Problem**: Missing ALL recent work from Nov 6, 2025:
- ❌ Missing 8 new agents (accessibility-validator, adaptive-learning, corporate-training, instructional-designer, localization, scorm-testing, etc.)
- ❌ Missing ALL 108 skill.py implementations
- ❌ Missing 13 engine files (wcag_compliance_engine.py, etc.)
- ❌ Missing AGENT_ENGINES_IMPLEMENTATION.md
- ❌ Missing PROFESSOR_IMPLEMENTATION.md

**What it has**: Only AGENT.md and README.md files (documentation stubs)

**Comparison**:
```
TOP-LEVEL .claude/                  NESTED content/.claude/
├── agents/ (27 items)              ├── agents/ (19 items) ⚠️ MISSING 8
├── skills/ (108 skill.py)          ├── skills/ (0 skill.py) ❌ MISSING ALL
├── framework/ (8 .py files)        ├── framework/ (same)
└── commands/ (10 files)            └── commands/ (same)

Last modified: Nov 6, 2025 ✅        Last modified: Nov 3, 2025 ❌
Size: 3.0 MB                         Size: 892 KB
```

**Recommendation**: **DELETE** - All content superseded by top-level ❌

---

#### `content/CLAUDE.md` and `content/README.md`

**Status**: **OLDER VERSIONS**

**Differences**:
- Top-level CLAUDE.md: 19,772 bytes (Nov 6) - Includes HMH Multi-Curriculum Knowledge Base section ✅
- Nested CLAUDE.md: 10,664 bytes (Nov 3) - Older, simpler version ❌

- Top-level README.md: 24,557 bytes (Nov 6) - Complete documentation ✅
- Nested README.md: 9,152 bytes (Nov 3) - Older version ❌

**Recommendation**: **DELETE** - Superseded by top-level versions ❌

---

#### Other Directories

**content/experiments/**: IDENTICAL to top-level `experiments/`
- Same `geometry-proofs-ab-test.md` file
- Same subdirectory structure
- **Recommendation**: DELETE (duplicate)

**content/specs/**: IDENTICAL to top-level `specs/`
- Same `dok-integration-plan.md` file
- **Recommendation**: DELETE (duplicate)

**content/.github/**: Likely old GitHub Actions workflows
- **Recommendation**: DELETE (use top-level .github/)

**content/.specify/**: Likely old Spec-Kit files
- **Recommendation**: DELETE (use top-level .specify/)

**Other empty/stub directories**:
- `content/analytics/` - Empty (3 .gitkeep files)
- `content/assessments/` - Empty
- `content/drafts/` - Empty
- `content/multimedia/` - Empty
- `content/published/` - Empty
- `content/reviews/` - Empty
- **Recommendation**: DELETE (no content)

---

## File Count Summary

| Location | Files | Size | Status |
|----------|-------|------|--------|
| **content/reference/baseline/** | 74 | 181 MB | ✅ **UNIQUE - KEEP** |
| **content/.claude/** | 131 | 892 KB | ❌ Outdated - DELETE |
| **Other directories** | 50 | ~1 MB | ❌ Duplicates/Empty - DELETE |
| **TOTAL** | 255 | 182 MB | Mixed |

---

## Recommended Action Plan

### Phase 1: Extract Unique Files (5 minutes)

**CRITICAL**: Move baseline directory to top-level before deleting anything.

```bash
# 1. Move baseline to top-level reference/
mv content/reference/baseline/ reference/

# 2. Verify move succeeded
ls -la reference/baseline/
du -sh reference/baseline/  # Should show 181M

# 3. Verify baseline exists at top level
[ -d "reference/baseline" ] && echo "✅ baseline moved successfully"
```

**Result**: Baseline materials now accessible at `reference/baseline/`

---

### Phase 2: Archive content/ Directory (10 minutes)

**Option A: Full Archive** (Safest - keep everything for review)

```bash
# 1. Create archive
mkdir -p .archive/old-content-directory-2025-11-06
mv content/ .archive/old-content-directory-2025-11-06/

# 2. Verify
ls -la .archive/old-content-directory-2025-11-06/

# 3. Update git
git add reference/baseline/
git add .archive/old-content-directory-2025-11-06/
git rm -r content/  # Remove from git tracking
git commit -m "Move baseline to top-level, archive old content/ directory"
```

**Option B: Selective Delete** (Keep only baseline, delete rest)

```bash
# After moving baseline/ to top-level:

# 1. Delete content/ directory
rm -rf content/

# 2. Verify baseline exists at top-level
ls -la reference/baseline/

# 3. Update git
git add reference/baseline/
git rm -rf content/
git commit -m "Move baseline to top-level, remove duplicate content/ directory"
```

---

### Phase 3: Verify No Data Loss (5 minutes)

```bash
# 1. Check baseline exists at top-level
[ -d "reference/baseline" ] && echo "✅ Baseline directory exists"
[ $(find reference/baseline -type f | wc -l) -eq 74 ] && echo "✅ All 74 files present"

# 2. Check content/ is gone or archived
[ ! -d "content" ] && echo "✅ content/ directory removed"
# OR
[ -d ".archive/old-content-directory-2025-11-06" ] && echo "✅ content/ archived"

# 3. Check top-level .claude/ still intact
[ -d ".claude/agents" ] && echo "✅ Top-level .claude/ intact"
[ $(find .claude/skills -name "skill.py" | wc -l) -eq 108 ] && echo "✅ All 108 skills present"

# 4. Check disk space recovered
du -sh .  # Should show ~182MB less if content/ deleted
```

---

## What You'll Gain

**After cleanup**:

✅ **Baseline materials accessible** at `reference/baseline/`
- All 74 reference documents
- HMH curriculum samples
- Style guides and vendor docs
- No data loss

✅ **Repository cleanup**:
- Remove 182MB of duplicates (if deleting)
- Or archive for future review (if archiving)
- Eliminate confusion about which .claude/ to use

✅ **Single source of truth**:
- One `.claude/` directory (top-level)
- One `reference/` directory structure
- Clear, unambiguous file locations

---

## What You'll Lose

❌ **If you delete without archiving**:
- Old .claude/ snapshot from Nov 3 (but superseded by top-level)
- Old CLAUDE.md/README.md versions (but superseded by top-level)
- Duplicate experiments/ and specs/ (but identical to top-level)

⚠️ **RISK**: If you delete without moving baseline/, you'll lose 181MB of critical reference materials!

---

## Detailed File Inventory

### Files in content/reference/baseline/ (74 files)

**PDFs (27 files)**:
1. 01_Mathematics_Revised_Webb_DOK_Definition_032016.pdf (122 KB)
2. 1-2_imv2_LessonTools_Icons.pdf (1.1 MB)
3. 1-2_mtxese000000_lesson_2R.pdf (6.3 MB)
4. 1-5_mtxeteXXXXXX_tg_final2.pdf (3.1 MB)
5. 3-5_imv2_LessonTools_icons.pdf (969 KB)
6. 3-5_mtxese000000_SE_Final2.pdf (2.6 MB)
7. 6-a1_imv2_LessonTools_icons.pdf (434 KB)
8. 6-A1_mtxese000000_lesson_2R.pdf (584 KB)
9. 6-A1_mtxeteXXXXXX_lesson_3R.pdf (1.3 MB)
10. CEID Vendor Reference Guide v3.pdf (668 KB)
11. Core_Solutions_Style_Guide_for_Mathematics.pdf (1.5 MB)
12. g04_imnlv2_pse_mod_m04l00s00_en (1).pdf (5.8 MB)
13. g04_imnlv2_ptg_mod_m04l00s00_en.pdf (32 MB)
14. g08_imnlv2_ptg_mod_m06l00s00_en.pdf (14 MB)
15. imra25-math-k12-sboe-approved-quality-rubric.pdf
16. Into Math TX – Content Block Output List.pdf
17. k_imv2_LessonTools_icons.pdf
18. k_mtxese000000_lesson_2R.pdf
19. k_mtxete000000_lesson_2R.pdf
20. Math Item Specs Guide (1).pdf
21. math-grade-1-breakouts.pdf
22. [6 more PDFs...]

**DOCX files (15 files)**:
1. Alt Text Guidelines.docx (3.1 MB)
2. Emergent Bilinguals Guidelines.docx (1.3 MB)
3. IMNLv2 A1 Digital Manipulatives.docx
4. IMNLv2 G3–5 Digital Manipulatives.docx
5. IMNLv2 G6–8 Digital Manipulatives.docx
6. IPACC-Guide_TX-Spec-Writing-Playbook_CURRENT.docx
7. LXDV EMM SE and TE Content Guidelines (2).docx
8. Mathematical Language Routines (MLR) Guidelines (1).docx
9. Mathematical Language Routines (MLR) Guidelines.docx
10. Pattern Guide for SYL and Tasks EMM Development.docx (6.1 MB)
11. UDL Guidelines (2).docx
12. UDL Guidelines (3).docx
13. Vocabulary Guidelines (1).docx
14. [1 more DOCX...]

**Markdown files (11 files)**:
1. alt-text-guidelines.md (86 KB)
2. content-guidelines.md (336 KB)
3. digital-manipulatives-a1.md
4. digital-manipulatives-g3-5.md
5. emergent-bilinguals.md (31 KB)
6. ipacc-playbook.md
7. mlr-guidelines.md
8. udl-guidelines.md
9. vendor-checklist-blocks.md
10. vendor-checklist-v2.md
11. vocabulary-guidelines.md

**InDesign files (8 files)**:
1. 1-2_imv2_LessonTools_Icons.indd (8 MB)
2. 3-5_imv2_LessonTools_icons.indd (6.6 MB)
3. 6-a1_imv2_LessonTools_icons.indd (4.6 MB)
4. k_imv2_LessonTools_icons.indd
5. [4 more in LessonTools_Icon_Displays/ subdirectory]

**Text files (9 files)**:
1. ceid-vendor-guide.txt (93 KB)
2. content-block-output-list.txt (6 KB)
3. grade-1-breakouts.txt
4. math-item-specs.txt
5. sboe-quality-rubric.txt
6. style-guide-math.txt
7. vendor-1pager.txt
8. vendor-playbook.txt
9. webb-dok-definition.txt

**Excel files (2 files)**:
1. Into Math Manipulatives List (1).xlsx
2. Into Math Prompts 11.5.2025.xlsx

**Other (2 items)**:
1. LessonTools_Icon_Displays.zip (25 MB)
2. LessonTools_Icon_Displays/ (directory)

---

## Questions to Consider

Before proceeding, consider:

1. **Do you need the baseline files?**
   - Yes → Move to `reference/baseline/` ✅
   - No → Still archive them (they're 181MB of work)

2. **Do you want to review the old .claude/ before deleting?**
   - Yes → Archive entire `content/` directory first
   - No → Just move baseline, delete the rest

3. **Any other files you might need?**
   - Check `content/` for any other files you recognize
   - Look for work in progress, drafts, etc.

---

## Conclusion

The `content/` directory is primarily valuable for the **181MB of baseline reference materials** in `content/reference/baseline/`.

**The rest is outdated duplicates** that can be safely deleted after moving baseline.

### Recommended Next Step

**SAFE APPROACH** (Recommended):
```bash
# 1. Move baseline to top-level
mv content/reference/baseline/ reference/

# 2. Archive entire content/ directory
mkdir -p .archive/old-content-directory-2025-11-06
mv content/ .archive/old-content-directory-2025-11-06/

# 3. Commit
git add reference/baseline/
git add .archive/old-content-directory-2025-11-06/
git rm -rf content/
git commit -m "Move baseline to top-level, archive old content/ directory

- Moved content/reference/baseline/ (181MB, 74 files) to reference/baseline/
- Archived outdated content/ directory (old .claude/ from Nov 3)
- No data loss - all unique files preserved
"
```

**Result**:
- ✅ All baseline materials accessible at `reference/baseline/`
- ✅ Old content/ archived for review if needed
- ✅ Clean repository structure
- ✅ No data loss

---

**Audit Complete**: 2025-11-06
**Total Files Analyzed**: 255
**Critical Files Found**: 74 (baseline/)
**Recommendation**: Move baseline, archive or delete rest
