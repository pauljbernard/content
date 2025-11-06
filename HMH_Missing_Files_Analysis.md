# Missing Files Analysis - HMH Integration Plan
**Date:** November 5, 2025

## Files Analyzed in Original Plan (5 documents)

✅ **Successfully Analyzed:**
1. `Alt Text Guidelines.docx` - 40+ image types with alt text specifications
2. `Emergent Bilinguals Guidelines.docx` - EB scaffolding strategies
3. `Mathematical Language Routines (MLR) Guidelines.docx` - 8 MLR routines
4. `UDL Guidelines (3).docx` - UDL principles and examples
5. `Vocabulary Guidelines (1).docx` - Vocabulary tracking rules

## Critical Files NOT Analyzed (15+ documents)

### **Tier 1: Critical for Complete Integration**

1. **`Pattern Guide for SYL and Tasks EMM Development.docx`** ⚠️ CRITICAL
   - **Purpose:** Defines Spark Your Learning and Task development patterns
   - **Status:** File exists but won't convert (possible corruption or permissions issue)
   - **Impact:** Without this, we're missing core content structure patterns
   - **Recommendation:** Must obtain readable version

2. **`LXDV EMM SE and TE Content Guidelines (2).docx`** ⚠️ CRITICAL
   - **Purpose:** Complete Student Edition and Teacher Edition content guidelines
   - **Status:** File too large (328KB) - couldn't read completely
   - **Impact:** Missing comprehensive EMM (Educational Materials Management) specifications
   - **Recommendation:** Need to extract in sections or get summary

3. **`Into Math Prompts 11.5.2025.xlsx`** ⚠️ HIGH PRIORITY
   - **Purpose:** Contains actual prompt strategies and templates for Into Math
   - **Status:** Python library version issue prevented reading
   - **Impact:** Missing specific prompt engineering guidance for content generation
   - **Recommendation:** Export to CSV or upgrade openpyxl library

4. **`IPACC-Guide_TX-Spec-Writing-Playbook_CURRENT.docx`** ✅ NOW ANALYZED
   - **Purpose:** Texas-specific asset specification writing (Photos, Art, Tech Art)
   - **Status:** Successfully converted and read
   - **Key Content:**
     - Asset type classification (Photo, Illustrative Art, Tech Art, Hybrid)
     - Spec writing principles
     - Texas SBOE Suitability Requirements (strict content guidelines)
     - Accessibility and knockout text rules
   - **Impact:** Critical for Texas adoption compliance

5. **`Math Item Specs Guide (1).pdf`** ⚠️ HIGH PRIORITY
   - **Purpose:** Mathematics assessment item specifications
   - **Status:** PDF - couldn't convert (pandoc doesn't read PDFs)
   - **Impact:** Missing item writing standards and patterns
   - **Recommendation:** Need PDF text extraction tool

6. **`CEID Vendor Reference Guide v3.pdf`** ⚠️ HIGH PRIORITY
   - **Purpose:** Vendor compliance reference (CEID = Cultural/Ethnic/Inclusion/Diversity)
   - **Status:** PDF - couldn't convert
   - **Impact:** Missing DEI validation criteria
   - **Recommendation:** Need PDF extraction

7. **`Core_Solutions_Style_Guide_for_Mathematics.pdf`** ⚠️ MEDIUM PRIORITY
   - **Purpose:** HMH style guide for mathematics content
   - **Status:** PDF - couldn't convert
   - **Impact:** Missing style and formatting standards
   - **Recommendation:** Need PDF extraction

8. **`01_Mathematics_Revised_Webb_DOK_Definition_032016.pdf`** 📊 MEDIUM PRIORITY
   - **Purpose:** Webb's Depth of Knowledge framework definitions
   - **Status:** PDF - couldn't convert
   - **Impact:** Missing DOK level classification guidance
   - **Recommendation:** DOK is critical for item development

### **Tier 2: Important Supporting Documents**

9. **Digital Manipulatives Lists (3 files):**
   - `IMNLv2 A1 Digital Manipulatives.docx` ✅ Read (minimal content: Algebra Tiles, Counters, Probability)
   - `IMNLv2 G3–5 Digital Manipulatives.docx` ✅ Converted
   - `IMNLv2 G6–8 Digital Manipulatives.docx` - Not yet read
   - **Purpose:** Lists of digital tools available by grade band
   - **Impact:** Needed for embedding manipulative references in lessons

10. **`Into Math Manipulatives List (1).xlsx`** 📊 MEDIUM PRIORITY
    - **Purpose:** Complete manipulatives inventory
    - **Status:** Excel file - couldn't read
    - **Impact:** Missing comprehensive manipulative catalog
    - **Recommendation:** Convert to CSV

11. **`imra25-math-k12-sboe-approved-quality-rubric.pdf`** ⚠️ HIGH PRIORITY
    - **Purpose:** Texas SBOE approved quality rubric for math materials
    - **Status:** PDF - couldn't convert
    - **Impact:** Missing official Texas quality standards
    - **Recommendation:** Critical for Texas compliance

12. **`Into Math TX – Content Block Output List.pdf`** 📊 MEDIUM PRIORITY
    - **Purpose:** Defines content block structure and outputs
    - **Status:** PDF - couldn't convert
    - **Impact:** Missing content organization framework

13. **`math-grade-1-breakouts.pdf`** 📊 LOW PRIORITY
    - **Purpose:** Grade 1 content breakdowns
    - **Status:** PDF - couldn't convert
    - **Impact:** Example reference for one grade

### **Tier 3: Reference Examples & Vendor QA**

14. **Sample Lesson PDFs (12 files):** 📚 REFERENCE
    - K: `k_mtxese000000_lesson_2R.pdf`, `k_mtxete000000_lesson_2R.pdf`
    - 1-2: `1-2_mtxese000000_lesson_2R.pdf`, `1-5_mtxeteXXXXXX_tg_final2.pdf`
    - 3-5: `3-5_mtxese000000_SE_Final2.pdf`
    - 6-A1: `6-A1_mtxese000000_lesson_2R.pdf`, `6-A1_mtxeteXXXXXX_lesson_3R.pdf`
    - Grade 4/8: `g04_imnlv2_pse_mod_m04l00s00_en (1).pdf`, `g04_imnlv2_ptg_mod_m04l00s00_en.pdf`, `g08_imnlv2_ptg_mod_m06l00s00_en.pdf`
    - **Purpose:** Real examples of guidelines in practice
    - **Status:** All PDFs - couldn't convert
    - **Impact:** Valuable as exemplars for validation
    - **Recommendation:** Use for visual comparison, not text extraction

15. **Lesson Tools Icons (7 files):** 🎨 DESIGN ASSETS
    - Source: `.indd` files (InDesign)
    - Export: `.pdf` files for K, 1-2, 3-5, 6-A1
    - Plus: `LessonTools_Icon_Displays.zip`
    - **Purpose:** Visual design standards and icon libraries
    - **Status:** Design files - not analyzed
    - **Impact:** Needed for visual consistency, not for text-based content generation
    - **Recommendation:** Reference for visual validation only

16. **Vendor Guidelines (Subdirectory - 4 files):** ✅ IDENTIFIED
    - `Into Math TX Vendor Checklist v2.docx`
    - `Into_Math_TX_Vendor_Checklist_1Pager.pdf`
    - `Into_Math_TX_Vendor_Guidelines_Playbook.pdf`
    - `Vendor Checklists by Content Block v1.docx`
    - **Purpose:** Quality assurance checklists for vendors
    - **Status:** Not yet analyzed
    - **Impact:** Critical for validation workflows
    - **Recommendation:** Convert DOCXs and extract PDF content

17. **Duplicate/Version Files:** 📋 CLARIFY
    - `Mathematical Language Routines (MLR) Guidelines (1).docx` vs `Mathematical Language Routines (MLR) Guidelines.docx`
    - `UDL Guidelines (2).docx` vs `UDL Guidelines (3).docx`
    - **Status:** Need to determine which is current version
    - **Recommendation:** Compare and use latest

---

## Impact Assessment

### Critical Gaps in Current Plan

| Missing Document | Impact on Integration | Workaround Available? |
|---|---|---|
| **Pattern Guide (SYL/Tasks)** | HIGH - Missing core content structure | ❌ No - Must resolve |
| **LXDV EMM Guidelines (complete)** | HIGH - Missing comprehensive EMM specs | ⚠️ Partial - Have other sources |
| **Into Math Prompts spreadsheet** | HIGH - Missing prompt strategies | ⚠️ Partial - Can infer from guidelines |
| **Math Item Specs Guide** | MEDIUM - Missing item standards | ⚠️ Partial - Have some item guidance |
| **CEID Vendor Guide** | MEDIUM - Missing DEI criteria | ✅ Yes - Have IPACC Texas guide |
| **Texas SBOE Quality Rubric** | HIGH - Missing quality standards | ❌ No - Critical for Texas |
| **Webb DOK Definition** | MEDIUM - Missing DOK framework | ✅ Yes - DOK is public knowledge |

### New Information from IPACC Playbook

**CRITICAL ADDITION:** The IPACC Texas Spec Writing Playbook revealed extensive Texas-specific requirements not in original plan:

1. **Texas SBOE Suitability Requirements** - Strict content prohibitions:
   - No Common Core references (TEKS only)
   - Historical accuracy requirements (1776 founding, not 1619)
   - Political neutrality
   - Parental rights respect
   - Specific equity guidelines
   - CIPA compliance for digital content

2. **Asset Type Classification** - 4 types with specific use cases:
   - Photos (realism, authenticity)
   - Illustrative Art (control, labels, idealization)
   - Tech Art (teaching tools, diagrams, manipulatives)
   - Hybrid (embedded assets)

3. **Spec Writing Standards** - Detailed requirements:
   - Objective statement required
   - Must-have vs discretionary elements
   - Reference scrap mandatory
   - DEI/CEID requirements per asset
   - Grade-appropriate age ranges

**This requires a NEW SKILL in the integration plan:**
- `/hmh.asset-spec` - Generate HMH-compliant asset specifications (Photo, Art, Tech Art)
- Should integrate with `/hmh.alt-text-generate` for accessibility

---

## Updated Recommendations

### Immediate Actions

1. **Resolve Pattern Guide access** ⚠️ CRITICAL
   - Try opening on different system
   - Request fresh copy from source
   - Check file permissions
   - This is blocking core pattern integration

2. **Extract LXDV EMM Guidelines** ⚠️ HIGH
   - Read in smaller sections (offset/limit parameters)
   - Or request summary document
   - Contains comprehensive content structure

3. **Convert PDFs to text** 📊 HIGH
   - Use PDF extraction tool (e.g., `pdftotext`, Adobe Acrobat, online converters)
   - Priority order:
     1. Texas SBOE Quality Rubric (critical for compliance)
     2. Math Item Specs Guide (item development)
     3. CEID Vendor Reference Guide (DEI validation)
     4. Core Solutions Style Guide (formatting)
     5. Webb DOK Definition (cognitive complexity)

4. **Read vendor checklist documents** ✅ MEDIUM
   - Convert the 2 DOCX files in Vendor Guidelines subdirectory
   - Extract PDFs if possible
   - These drive quality assurance workflows

5. **Export Excel files to CSV** 📊 MEDIUM
   - Into Math Prompts (HIGH - prompt strategies)
   - Manipulatives List (MEDIUM - tool inventory)

### Integration Plan Updates Required

#### New Skills to Add:
1. `/hmh.asset-spec` - Generate asset specifications (Photo/Art/Tech Art)
2. `/hmh.texas-validate` - Validate against Texas SBOE requirements
3. `/hmh.dok-classify` - Classify items by Webb DOK level

#### Enhanced Skills to Update:
1. `/hmh.alt-text-generate` - Integrate with asset spec workflow
2. `/hmh.lesson-validate` - Add Texas SBOE checks
3. `curriculum.develop-items` - Add DOK classification

#### Knowledge Base Sections to Add:
1. `/hmh-knowledge/texas-compliance/`
   - `sboe-requirements.md` (from IPACC playbook)
   - `quality-rubric.md` (from PDF when extracted)
   - `ceid-standards.md` (from vendor guide)

2. `/hmh-knowledge/assets/`
   - `asset-types.md` (Photo, Art, Tech Art, Hybrid)
   - `spec-writing-standards.md`
   - `texas-restrictions.md`

3. `/hmh-knowledge/assessment/`
   - `item-specifications.md` (from PDF when extracted)
   - `dok-framework.md`

---

## File Extraction Strategy

### For PDFs (10 files):
**Tools to try:**
1. `pdftotext` (command-line) - Available in most systems
2. `pdfminer` (Python) - Better for complex layouts
3. Adobe Acrobat - Export as Word/Text
4. Online converters (e.g., pdf2go.com, ilovepdf.com)
5. OCR if scanned (Tesseract)

**Command to try:**
```bash
# If pdftotext is available
pdftotext "Math Item Specs Guide (1).pdf" math-item-specs.txt

# If pdfminer.six is available
pdf2txt.py "Math Item Specs Guide (1).pdf" > math-item-specs.txt
```

### For Large DOCX:
**Strategy:** Read in chunks
```python
# Read specific sections by offset/limit
# Section 1: Lines 1-2000
# Section 2: Lines 2000-4000
# etc.
```

### For Excel Files:
**Strategy:** Convert to CSV
```bash
# If LibreOffice is available
soffice --headless --convert-to csv:"Text - txt - csv (StarCalc)":"44,34,76" "Into Math Prompts 11.5.2025.xlsx"

# Or use Excel to export as CSV
```

### For Pattern Guide:
**Strategy:** Multiple attempts
1. Copy file to new location
2. Try opening in Word and re-saving
3. Request fresh copy from source
4. Check if file is actually corrupted

---

## Summary Statistics

### Current Coverage:
- **Analyzed:** 5 core guideline documents + 1 Texas playbook = **6/40+ files** (15%)
- **Critical gaps:** 3-4 major documents
- **Blockers:** PDF extraction, Pattern Guide access, Excel library

### To Reach Complete Coverage:
- **High Priority:** 8 additional documents (Pattern Guide, EMM complete, Prompts, Item Specs, Quality Rubric, CEID Guide, Style Guide, DOK)
- **Medium Priority:** 4 documents (Content Block List, Manipulatives, Vendor checklists)
- **Reference:** 12 sample lessons (for validation, not extraction)

### Estimated Additional Effort:
- **PDF Extraction:** 2-4 hours (setup + extraction of 10 PDFs)
- **Pattern Guide Resolution:** 1-2 hours (troubleshooting)
- **Large DOCX Processing:** 1-2 hours (chunked reading)
- **Excel Conversion:** 30 minutes
- **Analysis & Integration:** 4-8 hours (reading + updating plan)
- **Total:** 8-16 additional hours

---

## Revised Integration Plan Impact

### Phases to Update:

**Phase 1 (Foundation)** - Add activities:
- ☐ Resolve Pattern Guide file access
- ☐ Extract all PDF documents to text
- ☐ Convert Excel files to CSV
- ☐ Read LXDV EMM Guidelines in sections
- ☐ Analyze vendor checklists
- ☐ Verify version currency (MLR, UDL duplicates)

**Phase 2 (Skill Enhancement)** - No major changes

**Phase 3 (New Skill Creation)** - Add skills:
- ☐ `/hmh.asset-spec` - Asset specification generation
- ☐ `/hmh.texas-validate` - Texas SBOE compliance
- ☐ `/hmh.dok-classify` - DOK level classification

**Phase 4 (Agent Integration)** - Add checks:
- Modify `quality-assurance` agent to validate Texas requirements
- Modify `assessment-designer` agent to classify DOK levels

**Phase 5 (Validation)** - Expand scope:
- Add Texas SBOE compliance validation
- Add asset specification validation
- Add DOK classification validation

---

## Next Steps (Priority Order)

1. ⚠️ **CRITICAL:** Resolve Pattern Guide file access
2. 📊 **HIGH:** Extract high-priority PDFs (Quality Rubric, Item Specs, CEID Guide)
3. 📊 **HIGH:** Export Into Math Prompts Excel to CSV
4. ✅ **MEDIUM:** Convert vendor checklist DOCXs
5. 📚 **MEDIUM:** Read LXDV EMM Guidelines in sections
6. 📋 **LOW:** Check MLR/UDL file versions
7. 🎨 **LOW:** Catalog lesson icons (reference only)
8. 📚 **REFERENCE:** Review sample lesson PDFs visually

Once critical files are accessible, update the main integration plan with:
- Pattern development guidelines (from Pattern Guide)
- Texas compliance requirements (from SBOE Rubric + IPACC Playbook)
- Assessment specifications (from Item Specs Guide)
- DEI validation criteria (from CEID Vendor Guide)
- Prompt engineering strategies (from Prompts spreadsheet)

