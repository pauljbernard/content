# Taxonomy Migration to Content Type System

**Date:** 2025-11-08
**Status:** ✅ Complete
**Migration Type:** Hardcoded Taxonomies → Dynamic Content Types

## Overview

This document describes the migration of hardcoded taxonomy data (Subjects and States/Districts) from the knowledge base file system structure to the dynamic Content Type system.

## What Was Migrated

### 1. Subjects (10 total)
Previously: Read dynamically from `/reference/hmh-knowledge/subjects/` directory structure
Now: Managed as **Subject** content type instances

**Migrated Subjects:**
1. Computer Science
2. Early Literacy (Pre-K/K)
3. Early Mathematics (Pre-K/K)
4. English Language Arts (ELA)
5. Fine Arts
6. Mathematics
7. Physical Education & Health
8. Science
9. Social Studies
10. World Languages

### 2. States/Districts (71 total)
Previously: Read dynamically from `/reference/hmh-knowledge/districts/` directory structure
Now: Managed as **State/District** content type instances

**Migrated:**
- 51 US States + DC
- 20 Large Urban Districts (NYC, LA, Chicago, Houston, Dallas, Miami, etc.)

## Migration Details

### Subject Content Type

**Content Type ID:** `a3e3b5f2-1b64-4cae-a927-df9b94ca7966`
**Category:** taxonomy
**Template:** `subject-template`

**Attributes:**
- `subject_code` (text, required) - Unique identifier (e.g., "mathematics")
- `name` (text, required) - Full display name (e.g., "Mathematics")
- `abbreviation` (text) - Short abbreviation (e.g., "Math")
- `description` (long_text) - Detailed description
- `parent_subject` (reference, self) - For hierarchical subjects
- `subject_category` (choice, required) - core, stem, humanities, arts, wellness, language, technical, other
- `grade_levels` (choice, multiple) - Pre-K through Higher Ed
- `knowledge_base_path` (text) - Path to subject directory
- `standards_frameworks` (json) - Array of applicable standards
- `icon` (text) - Icon name for UI
- `color` (text) - Hex color for UI
- `active` (boolean) - Whether currently active
- `display_order` (number) - Sort order

### State/District Content Type

**Content Type ID:** `f99c30e1-872c-44a8-bbb8-c1d6d5d23f08`
**Category:** taxonomy
**Template:** `state-district-template`

**Attributes:**
- `district_code` (text, required) - Unique identifier (e.g., "texas")
- `name` (text, required) - Full display name (e.g., "Texas")
- `abbreviation` (text) - Short abbreviation (e.g., "TX")
- `district_type` (choice, required) - state, large_urban_district, county, region, national
- `parent_state` (reference, self) - Parent state for districts
- `region` (choice) - Northeast, Southeast, Midwest, Southwest, West, Pacific, Non-US
- `population` (number) - Student population
- `knowledge_base_path` (text) - Path to district directory
- `standards_framework` (choice) - TEKS, CCSS, NGSS, State-Specific, Custom
- `compliance_requirements` (json) - Array of requirements
- `language_standards` (text) - ELPS, ELD, WIDA, etc.
- `website` (url) - Official education website
- `active` (boolean) - Whether currently active
- `display_order` (number) - Sort order

## Migration Scripts

### Subjects Import
**Script:** `/backend/scripts/import_subjects.py`

**Results:**
- ✅ 10/10 subjects successfully imported
- All subjects include comprehensive metadata (description, category, grade levels, standards frameworks, icons, colors)
- All subjects set to `published` status

### States/Districts Import
**Script:** `/backend/scripts/import_states_districts.py`

**Results:**
- ✅ 51/51 states successfully imported
- ✅ 20/20 urban districts successfully imported
- All entries include comprehensive metadata (region, population, standards framework, language standards, websites for districts)
- Parent state references correctly established for urban districts
- All entries set to `published` status

## How to Access Taxonomy Data Now

### Via UI

**Subjects:**
- Navigate to: `/content-types/a3e3b5f2-1b64-4cae-a927-df9b94ca7966/instances`
- Or: Content Types → Subject → View Instances

**States/Districts:**
- Navigate to: `/content-types/f99c30e1-872c-44a8-bbb8-c1d6d5d23f08/instances`
- Or: Content Types → State/District → View Instances

### Via API

**List all subjects:**
```bash
GET /api/v1/content-types/a3e3b5f2-1b64-4cae-a927-df9b94ca7966/instances
```

**List all states/districts:**
```bash
GET /api/v1/content-types/f99c30e1-872c-44a8-bbb8-c1d6d5d23f08/instances
```

**Get specific instance:**
```bash
GET /api/v1/content-types/instances/{instance_id}
```

## Benefits of New System

### ✅ Subjects
- **CRUD through UI** - No file system access needed
- **Version history** - Automatic timestamps and audit trail
- **Metadata enrichment** - Icons, colors, categories, descriptions
- **Hierarchical** - Support for parent-child relationships
- **Flexible** - Easy to add new subjects or modify existing ones
- **API access** - RESTful API for all operations
- **Status workflow** - Draft, Published, Archived states

### ✅ States/Districts
- **CRUD through UI** - No file system access needed
- **Version history** - Automatic timestamps and audit trail
- **Rich metadata** - Population, regions, compliance requirements, websites
- **Hierarchical** - Urban districts reference parent states
- **Searchable** - Full-text search across all metadata
- **API access** - RESTful API for all operations
- **Status workflow** - Draft, Published, Archived states

## Knowledge Base Integration

**Important:** The knowledge base file system structure remains unchanged. The `/reference/hmh-knowledge/subjects/` and `/reference/hmh-knowledge/districts/` directories continue to exist and serve as the source of knowledge files.

**What changed:**
- Taxonomy metadata is now managed in the database
- UI components can fetch subjects/states from the API instead of file system
- New subjects/states can be added through the UI
- Metadata can be enriched without touching file system

**What stayed the same:**
- Knowledge base file organization
- Knowledge resolution paths
- Curriculum configurations still reference these directories

## Backend API Updates

The following API endpoints can now optionally use the Content Type system instead of file system enumeration:

**Current (file system):**
```bash
GET /api/v1/knowledge-base/subjects
GET /api/v1/knowledge-base/states
```

**New (content type):**
```bash
GET /api/v1/content-types/a3e3b5f2-1b64-4cae-a927-df9b94ca7966/instances  # Subjects
GET /api/v1/content-types/f99c30e1-872c-44a8-bbb8-c1d6d5d23f08/instances  # States/Districts
```

Both approaches are valid. The Content Type approach provides richer metadata and UI management capabilities.

## Future Considerations

### Optional Enhancement: Reference Fields in Content Templates

Currently, content type templates (Lesson, Assessment, etc.) use free-text fields for subjects and states:

```javascript
{
  name: 'subject',
  type: 'choice',  // Hardcoded choices
  config: {
    choices: ['mathematics', 'ela', 'science', ...],
  }
}
```

**Possible future enhancement:**
```javascript
{
  name: 'subject',
  type: 'reference',  // Reference to Subject content type
  config: {
    targetContentType: 'a3e3b5f2-1b64-4cae-a927-df9b94ca7966',
    multiple: false,
  }
}
```

This would provide:
- Dynamic subject lists that update when new subjects are added
- Referential integrity
- Ability to fetch subject metadata (icons, colors, descriptions)
- Consistent taxonomy across all content

**Trade-offs:**
- Would require updating existing content instances
- More complex form handling in UI
- Increased database queries

**Recommendation:** Evaluate based on usage patterns and UX requirements.

## Migration Summary

| Category | Count | Content Type ID | Status |
|----------|-------|-----------------|--------|
| Subjects | 10 | a3e3b5f2-1b64-4cae-a927-df9b94ca7966 | ✅ Complete |
| States | 51 | f99c30e1-872c-44a8-bbb8-c1d6d5d23f08 | ✅ Complete |
| Districts | 20 | f99c30e1-872c-44a8-bbb8-c1d6d5d23f08 | ✅ Complete |
| **Total** | **81** | **2 content types** | ✅ **100% migrated** |

## Related Migrations

This migration is part of a larger effort to move all hardcoded data structures to the dynamic Content Type system:

1. ✅ **Curriculum Configurations** - Completed 2025-11-08 (11 curricula)
2. ✅ **Subjects** - Completed 2025-11-08 (10 subjects)
3. ✅ **States/Districts** - Completed 2025-11-08 (71 states/districts)

## Files Created/Modified

**Created:**
- `/frontend/src/data/contentTypeTemplates.js` - Added Subject and State/District templates
- `/backend/scripts/import_subjects.py` - Subject migration script
- `/backend/scripts/import_states_districts.py` - States/Districts migration script
- `/docs/TAXONOMY_MIGRATION.md` - This documentation

**Modified:**
- Database: 2 new content types, 81 new content instances

## Support

For questions or issues related to this migration:
- See [USER_GUIDE.md](../USER_GUIDE.md) for content type system overview
- See [ENGINEER_GUIDE.md](../ENGINEER_GUIDE.md) for extending taxonomies
- Create an issue in the repository

---

**Last Updated:** 2025-11-08
**Migration Status:** ✅ Complete
**Total Entities Migrated:** 81 (10 subjects + 71 states/districts)
