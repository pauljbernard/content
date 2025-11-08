# Content Type System Migration Guide

## Overview

The Nova platform is transitioning from a hardcoded Content model (lessons, assessments, activities, guides) to a flexible content type system similar to Contentful or Strapi. This migration allows for:

- **Flexible Content Modeling**: Define any content structure without code changes
- **Custom Attributes**: Create content types with any combination of 13 attribute types
- **Future-Proof**: No need to modify backend code for new content types
- **Backward Compatibility**: Legacy content continues to work through the migration system

## Architecture

### Old System (Legacy)
- Hardcoded `Content` model with fixed schema
- Content types: lesson, assessment, activity, guide, framework
- Fixed fields: title, subject, grade_level, learning_objectives, etc.
- Located in `/backend/models/content.py`
- Accessed via `/api/v1/content`

### New System (Flexible)
- Dynamic `ContentTypeModel` with JSON attributes
- Custom content types defined by users
- `ContentInstanceModel` with flexible data storage
- Located in `/backend/models/content_type.py`
- Accessed via `/api/v1/content-types`

## Migration Strategy

The migration happens in phases to ensure zero downtime and backward compatibility:

### Phase 1: Parallel Systems ✅ COMPLETE
- [x] New flexible content type system implemented
- [x] Old Content system remains operational
- [x] Both systems coexist

### Phase 2: Legacy Content Type Creation (CURRENT)
- [ ] Knowledge Engineer runs `/api/v1/migrations/setup-legacy-content-type`
- [ ] Creates "Legacy Content" system content type
- [ ] Matches old Content model schema exactly
- [ ] Marked as `is_system=true` (cannot be deleted)

### Phase 3: Data Migration
- [ ] Knowledge Engineer runs `/api/v1/migrations/migrate-legacy-content`
- [ ] Converts existing Content records to ContentInstances
- [ ] Preserves all data and metadata
- [ ] Can be run in batches (limit/offset parameters)
- [ ] Idempotent - safe to re-run

### Phase 4: Dual Read (Future)
- [ ] Update `/content` endpoints to read from both systems
- [ ] Check ContentInstances first, fall back to Content
- [ ] Transparent to users

### Phase 5: Deprecation (Future)
- [ ] Announce deprecation timeline
- [ ] All new content uses flexible system
- [ ] Old Content API marked as deprecated
- [ ] Documentation updated

### Phase 6: Removal (Future, 6-12 months)
- [ ] Remove old Content model and endpoints
- [ ] Remove legacy tables from database
- [ ] Update all references

## Migration API Endpoints

### Setup Legacy Content Type
```bash
POST /api/v1/migrations/setup-legacy-content-type
Authorization: Bearer <knowledge_engineer_token>
```

Creates the "Legacy Content" system content type with attributes matching the old Content schema.

**Response:**
```json
{
  "message": "Legacy Content type created successfully",
  "content_type_id": "abc-123-def",
  "attributes_count": 11,
  "next_steps": [
    "Legacy content can now be migrated to content instances",
    "Future content should be created as instances of flexible content types",
    "The old /content endpoint can eventually be deprecated"
  ]
}
```

### Migrate Legacy Content
```bash
POST /api/v1/migrations/migrate-legacy-content?limit=100&offset=0
Authorization: Bearer <knowledge_engineer_token>
```

Migrates existing Content records to ContentInstances in batches.

**Response:**
```json
{
  "migrated": 95,
  "skipped": 5,
  "errors": [],
  "total_processed": 100,
  "offset": 0,
  "limit": 100,
  "message": "Migrated 95 content items to flexible content type system"
}
```

### Check Migration Status
```bash
GET /api/v1/migrations/migration-status
Authorization: Bearer <knowledge_engineer_token>
```

Shows current migration progress.

**Response:**
```json
{
  "legacy_type_created": true,
  "legacy_type_id": "abc-123-def",
  "total_legacy_content": 500,
  "migrated_instances": 450,
  "remaining_to_migrate": 50,
  "migration_complete": false
}
```

## Step-by-Step Migration Process

### For Knowledge Engineers

1. **Setup Legacy Content Type**
   ```bash
   curl -X POST http://localhost:8000/api/v1/migrations/setup-legacy-content-type \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

2. **Check Initial Status**
   ```bash
   curl http://localhost:8000/api/v1/migrations/migration-status \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **Migrate in Batches** (recommended for large datasets)
   ```bash
   # Batch 1
   curl -X POST "http://localhost:8000/api/v1/migrations/migrate-legacy-content?limit=100&offset=0" \
     -H "Authorization: Bearer YOUR_TOKEN"

   # Batch 2
   curl -X POST "http://localhost:8000/api/v1/migrations/migrate-legacy-content?limit=100&offset=100" \
     -H "Authorization: Bearer YOUR_TOKEN"

   # Continue until all content is migrated
   ```

4. **Verify Migration**
   ```bash
   curl http://localhost:8000/api/v1/migrations/migration-status \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

5. **Test Legacy Content Type**
   - Go to `/content-types` in the UI
   - Find "Legacy Content" (marked as System)
   - Click "Instances" to view migrated content
   - Create a test instance to verify functionality

## Data Mapping

### Content Model → ContentInstance Data

| Old Field | New Location | Notes |
|-----------|--------------|-------|
| `id` | Instance ID prefixed with "legacy-" | Tracks migration source |
| `title` | `data.title` | Direct mapping |
| `content_type` | `data.content_type` | lesson, assessment, etc. |
| `subject` | `data.subject` | Direct mapping |
| `grade_level` | `data.grade_level` | Direct mapping |
| `state` | `data.state` | Direct mapping |
| `curriculum_id` | `data.curriculum_id` | Direct mapping |
| `learning_objectives` | `data.learning_objectives` | JSON array |
| `standards_aligned` | `data.standards_aligned` | JSON array |
| `duration_minutes` | `data.duration_minutes` | Number |
| `file_content` | `data.file_content` | Rich text |
| `knowledge_files_used` | `data.knowledge_files_used` | JSON array |
| `status` | `status` | Mapped to draft/published/archived |
| `author_id` | `created_by` | Direct mapping |
| `created_at` | `created_at` | Preserved |
| `updated_at` | `updated_at` | Preserved |

### Status Mapping

| Old Status | New Status |
|------------|------------|
| draft | draft |
| in_review | draft |
| needs_revision | draft |
| approved | published |
| published | published |
| archived | archived |

## Benefits of Migration

1. **Flexibility**: Create new content types without code changes
2. **Consistency**: All content uses the same storage system
3. **Scalability**: Add new fields and types as needed
4. **Templates**: Pre-built templates for common content types
5. **Future-Proof**: Easy to add new content models

## Future Content Types

After migration, these specialized content types can be created:

- **Lesson Plans** (from template)
- **Assessments** (from template)
- **Learning Activities** (from template)
- **Reading Passages** (from template)
- **Multimedia Resources** (from template)
- **Vocabulary Lists** (from template)
- **Custom Types**: Whatever you need!

## Rollback Plan

If migration issues occur:

1. The old Content system remains untouched
2. Migrated ContentInstances can be deleted
3. The "Legacy Content" type can be removed
4. System returns to pre-migration state
5. No data loss occurs

## Testing Checklist

Before running production migration:

- [ ] Test setup-legacy-content-type in development
- [ ] Migrate a small batch (10 items)
- [ ] Verify all fields mapped correctly
- [ ] Test viewing instances in UI
- [ ] Test editing an instance
- [ ] Test creating a new instance
- [ ] Verify search works with instances
- [ ] Check performance with large batches

## Support

For migration assistance:
- Check `/api/v1/docs` for detailed API documentation
- Run `/api/v1/migrations/migration-status` for current state
- Contact knowledge engineering team for issues

## Timeline

- **Phase 1**: ✅ Complete
- **Phase 2**: Available now (run migration endpoints)
- **Phase 3**: After Phase 2 complete
- **Phase 4**: 2-3 months after Phase 3
- **Phase 5**: 6 months after Phase 4
- **Phase 6**: 12 months after Phase 5

## Next Steps

1. Knowledge Engineer: Run setup-legacy-content-type
2. Knowledge Engineer: Test migration with small batch
3. Knowledge Engineer: Run full migration
4. Team: Begin creating new content using flexible types
5. Team: Stop creating content via old /content endpoint
6. Engineering: Plan Phase 4 implementation
