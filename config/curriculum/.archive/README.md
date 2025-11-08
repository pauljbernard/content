# Archived Curriculum Configuration Files

**Date Archived:** 2025-11-08
**Reason:** Migrated to dynamic Content Type system

## What Happened

These curriculum configuration JSON files were the original hardcoded curriculum definitions. They have been **successfully migrated** to the dynamic Content Type system and are now managed as content instances.

## Migration Details

- **Content Type:** Curriculum Configuration (ID: `17307f1b-0eb0-46d3-ba81-1731dd2b1750`)
- **Migrated Files:** 11 curriculum configurations
- **Migration Script:** `/backend/scripts/import_curriculum_configs.py`
- **Migration Date:** 2025-11-08

## How to Access Curriculum Data Now

### Via UI
Navigate to: `/content-types/17307f1b-0eb0-46d3-ba81-1731dd2b1750/instances`

Or search for "Curriculum Configuration" content type in the Content Types page.

### Via API
```bash
# List all curriculum configurations
GET /api/v1/content-types/17307f1b-0eb0-46d3-ba81-1731dd2b1750/instances

# Get specific curriculum
GET /api/v1/content-types/instances/{instance_id}
```

### Via Content Page
1. Go to `/content`
2. Filter by Content Type: "Curriculum Configuration"
3. View, edit, or create new curriculum configurations

## Migrated Curricula

All 11 curricula were successfully migrated:

1. hmh-into-math-ca - HMH Into Math California Edition
2. hmh-into-math-fl - HMH Into Math Florida Edition
3. hmh-into-math-tx - HMH Into Math Texas Edition
4. hmh-into-reading-tx - HMH Into Reading Texas Edition
5. hmh-algebra1-tx - HMH Algebra I Texas Edition
6. hmh-biology-tx - HMH Biology Texas Edition
7. hmh-ap-calculus-ab - HMH AP Calculus AB
8. hmh-ap-english-literature - HMH AP English Literature
9. hmh-spanish-i-tx - HMH Spanish I Texas
10. hmh-art-i - HMH Art I
11. hmh-pe-9-12 - HMH Physical Education High School

## Benefits of New System

- ✅ **CRUD through UI** - No file system access needed
- ✅ **Version history** - Automatic timestamps and audit trail
- ✅ **Validation** - Schema-based validation
- ✅ **Searchable** - Full-text search across all metadata
- ✅ **API access** - RESTful API for all operations
- ✅ **Permissions** - Role-based access control
- ✅ **Status workflow** - Draft, Published, Archived states

## These Files Are Safe to Delete

These archived JSON files are **no longer needed** by the application. They are kept here only as a backup reference. The application now reads curriculum data from the database via the Content Type API.

If you need to restore or reference the original data structure, these files are preserved here.

## Related Files Archived

- **Frontend:** `/frontend/src/pages/.archive/ConfigManager.jsx.archived` (legacy curriculum management page)
- **Routes:** Removed `/configs` route from App.jsx
- **Navigation:** Removed "Curriculums" menu item from Layout.jsx
