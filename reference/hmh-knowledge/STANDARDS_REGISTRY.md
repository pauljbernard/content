# Standards Registry
**Reference System for Imported Educational Standards**
**Last Updated:** 2025-11-07

---

## Overview

This registry documents the relationship between knowledge base files, curriculum configs, and imported standards stored in the database. Instead of referencing external URLs, the system now uses imported standards as first-class data entities.

**Benefits:**
- **Offline access**: Standards available without internet connection
- **Consistent structure**: All standards in uniform hierarchical format
- **Search capability**: Fast search across all standards
- **Version control**: Track standards changes over time
- **Reference integrity**: Direct links between content and standards

---

## Standard Reference System

### 1. **Database Standards** (Primary Source)

Standards are imported into the database via `/standards/import` and assigned unique IDs.

**Standard Model Fields:**
- `id`: Database primary key
- `code`: Unique code (e.g., "TEKS-MATH-TX", "CCSS-M", "NGSS")
- `name`: Full name
- `type`: state, national, international, district
- `subject`: mathematics, ela, science, etc.
- `state`: State abbreviation (for state standards)
- `structure`: Hierarchical organization
- `standards_list`: Flat list of all standards

### 2. **Curriculum Config References**

Curriculum configs reference imported standards by code in the `standards.content_standard_code` field.

**Example:**
```json
{
  "id": "hmh-into-math-tx",
  "standards": {
    "content": "TEKS",
    "content_standard_code": "TEKS-MATH-TX",
    "language": "ELPS",
    "language_standard_code": "ELPS-TX",
    "accessibility": "WCAG 2.1 AA"
  }
}
```

### 3. **Knowledge Base File References**

Knowledge base files can include a "Standard Reference" section linking to imported standards:

**Example:**
```markdown
## Standard Reference

**Standard:** TEKS Mathematics (Texas)
**Code:** TEKS-MATH-TX
**Database ID:** Reference via code lookup
**Alternative URL:** https://tea.texas.gov/teks (legacy reference)
```

---

## Priority Standards to Import

### National Standards (5 standards)

| Code | Name | Format | Source URL | Status |
|------|------|--------|------------|--------|
| **CCSS-M** | Common Core State Standards - Mathematics | CASE | http://www.corestandards.org/Math/ | ⏳ Pending |
| **CCSS-ELA** | Common Core State Standards - English Language Arts | CASE | http://www.corestandards.org/ELA-Literacy/ | ⏳ Pending |
| **NGSS** | Next Generation Science Standards | CASE | https://www.nextgenscience.org/ | ⏳ Pending |
| **CSTA-CS** | CSTA K-12 Computer Science Standards | HTML | https://csteachers.org/k12standards/ | ⏳ Pending |
| **C3-SS** | C3 Framework for Social Studies | PDF | https://www.socialstudies.org/c3 | ⏳ Pending |

### State Standards - Texas (5 standards)

| Code | Name | Format | Source URL | Status |
|------|------|--------|------------|--------|
| **TEKS-MATH-TX** | TEKS Mathematics K-12 | CASE | https://tea.texas.gov/teks/mathematics | ⏳ Pending |
| **TEKS-ELA-TX** | TEKS English Language Arts K-12 | CASE | https://tea.texas.gov/teks/ela | ⏳ Pending |
| **TEKS-SCI-TX** | TEKS Science K-12 | CASE | https://tea.texas.gov/teks/science | ⏳ Pending |
| **TEKS-SS-TX** | TEKS Social Studies K-12 | CASE | https://tea.texas.gov/teks/social-studies | ⏳ Pending |
| **ELPS-TX** | English Language Proficiency Standards | PDF | https://tea.texas.gov/elps | ⏳ Pending |

### State Standards - California (5 standards)

| Code | Name | Format | Source URL | Status |
|------|------|--------|------------|--------|
| **CCSS-M-CA** | CCSS Mathematics (California Adoption) | CASE | https://www.cde.ca.gov/be/st/ss/mathstandards.asp | ⏳ Pending |
| **CCSS-ELA-CA** | CCSS ELA/Literacy (California Adoption) | CASE | https://www.cde.ca.gov/be/st/ss/enggrade.asp | ⏳ Pending |
| **NGSS-CA** | NGSS (California Adoption) | CASE | https://www.cde.ca.gov/pd/ca/sc/ngssstandards.asp | ⏳ Pending |
| **HSS-CA** | History-Social Science Framework | PDF | https://www.cde.ca.gov/ci/hs/cf/hssframeworkwhole.asp | ⏳ Pending |
| **ELD-CA** | English Language Development Standards | PDF | https://www.cde.ca.gov/sp/el/er/eldstandards.asp | ⏳ Pending |

### State Standards - Florida (5 standards)

| Code | Name | Format | Source URL | Status |
|------|------|--------|------------|--------|
| **MAFS-FL** | Mathematics Florida Standards | CASE | https://www.fldoe.org/academics/standards/subject-areas/math-science/mathematics.stml | ⏳ Pending |
| **BEST-ELA-FL** | B.E.S.T. English Language Arts | CASE | https://www.fldoe.org/academics/standards/subject-areas/lang-arts/fl-benchmarks-ela.stml | ⏳ Pending |
| **NGSSS-FL** | Next Generation Sunshine State Standards (Science) | CASE | https://www.fldoe.org/academics/standards/subject-areas/math-science/science.stml | ⏳ Pending |
| **SS-FL** | Social Studies Standards | PDF | https://www.fldoe.org/academics/standards/subject-areas/social-studies/ | ⏳ Pending |
| **WIDA-ELD-FL** | WIDA English Language Development (Florida) | PDF | https://wida.wisc.edu/teach/standards | ⏳ Pending |

### Additional State CS Standards (51 standards)

All 51 US states/districts have computer science standards that should be imported.
See `/subjects/computer-science/districts/{state}/{state}-cs-standards.md` for details.

**Priority States:**
- New York, Illinois, Massachusetts, Washington, Virginia, Georgia, North Carolina

---

## Import Instructions

### Using the Standards Import UI

1. **Navigate to Standards Page**
   - Go to `/standards` in the web UI
   - Click "Import Standard" button

2. **Fill Import Form**
   - **Source Type**: URL (for most standards)
   - **Source Location**: Enter CASE URL or document URL
   - **Format**: Select format (CASE, PDF, HTML, etc.)
   - **Metadata**: Enter name, code, type, subject, organization

3. **Monitor Import**
   - View progress on job status page
   - Check for completion (usually 5-15 minutes)

4. **Verify Import**
   - View imported standard
   - Check hierarchical structure
   - Validate standard codes

### Using the API

```bash
# Create import job
curl -X POST https://api.example.com/api/v1/standards/import \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "url",
    "source_location": "https://tea.texas.gov/api/case/teks-math",
    "format": "case",
    "name": "TEKS Mathematics K-12",
    "short_name": "TEKS Math",
    "code": "TEKS-MATH-TX",
    "type": "state",
    "subject": "mathematics",
    "source_organization": "Texas Education Agency",
    "state": "texas"
  }'

# Check job status
curl https://api.example.com/api/v1/standards/import/{job_id} \
  -H "Authorization: Bearer $TOKEN"

# View imported standard
curl https://api.example.com/api/v1/standards/{standard_id} \
  -H "Authorization: Bearer $TOKEN"
```

---

## Migration Guide

### For Curriculum Configs

**Before (External References):**
```json
{
  "standards": {
    "content": "TEKS",
    "language": "ELPS"
  }
}
```

**After (Database References):**
```json
{
  "standards": {
    "content": "TEKS",
    "content_standard_code": "TEKS-MATH-TX",
    "language": "ELPS",
    "language_standard_code": "ELPS-TX"
  }
}
```

### For Knowledge Base Files

**Before (External URL):**
```markdown
## Resources
**CSTA Standards:** https://csteachers.org/k12standards/
```

**After (Database Reference):**
```markdown
## Standard Reference
**Standard:** CSTA K-12 Computer Science Standards
**Code:** CSTA-CS
**View in System:** `/standards` page → Search "CSTA"

## Resources (Legacy)
**External URL:** https://csteachers.org/k12standards/
```

---

## Standard Code Conventions

**Format**: `{STANDARD-NAME}-{SUBJECT}-{STATE}`

**Examples:**
- `TEKS-MATH-TX` - Texas Essential Knowledge and Skills, Mathematics, Texas
- `CCSS-M` - Common Core State Standards, Mathematics (no state = national)
- `NGSS` - Next Generation Science Standards (no subject = multi-subject)
- `CSTA-CS` - CSTA Computer Science Standards
- `MAFS-FL` - Mathematics Florida Standards
- `BEST-ELA-FL` - B.E.S.T. ELA, Florida

**State Codes**: Use lowercase state name or abbreviation
- `TX` or `texas` - Texas
- `CA` or `california` - California
- `FL` or `florida` - Florida
- `NY` or `new-york` - New York

---

## Benefits of Imported Standards

### 1. **Offline Access**
All standards available without internet connection.

### 2. **Consistent Structure**
Uniform hierarchical format across all standards:
- Domains → Strands → Individual Standards
- Searchable metadata
- Grade level mapping

### 3. **Content Alignment**
Direct alignment between content and specific standards:
- Link lessons to standard IDs
- Track coverage across curriculum
- Generate alignment reports

### 4. **Version Control**
Track standards updates over time:
- Version numbers
- Change history
- Adoption year tracking

### 5. **Advanced Search**
Search across all imported standards:
- Full-text search
- Filter by subject, grade, state
- Cross-reference capabilities

---

## Next Steps

1. **Import Priority Standards**: Start with CCSS, NGSS, TEKS (TX), CCSS (CA), MAFS (FL)
2. **Update Curriculum Configs**: Add `content_standard_code` fields
3. **Update Knowledge Base**: Add "Standard Reference" sections
4. **Generate Alignment Reports**: Use imported standards for coverage analysis
5. **Train Users**: Document how to use imported standards

---

## Support

**Questions?**
- See documentation: `/docs/standards-management/`
- API docs: `/api/v1/docs#/Standards`
- Contact: knowledge-engineering@example.com

---

**Remember**: Imported standards are the authoritative source. External URLs are kept for reference only.
