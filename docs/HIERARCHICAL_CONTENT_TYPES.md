# Hierarchical Content Types

## Overview

The system now supports **hierarchical content types** that can display content in an expandable tree structure instead of a linear table. This is essential for content like CASE Standards, organizational structures, taxonomies, and any other naturally hierarchical data.

## Key Features

### 1. Content Type Level Configuration

Any content type can be marked as hierarchical with configuration:

```json
{
  "is_hierarchical": true,
  "hierarchy_config": {
    "identifier_field": "identifier",           // Unique ID field in data
    "parent_field": "parent",                   // Field pointing to parent's identifier
    "children_field": "children",               // Field with array of child identifiers
    "display_field": "full_statement",          // Primary display text
    "secondary_display_field": "human_coding_scheme",  // Optional secondary text
    "supports_lazy_loading": true               // Load children on-demand
  }
}
```

### 2. Automatic Detection

The frontend automatically detects hierarchical content types and switches between:
- **Tree View**: Expandable hierarchy with lazy-loading children
- **Table View**: Traditional linear list with pagination

### 3. Tree-Based API Endpoint

**`GET /api/v1/content-types/{id}/instances/tree`**

Query Parameters:
- `parent_id`: null for root nodes, or parent identifier for children
- `skip`: Pagination offset
- `limit`: Items per page

Response:
```json
{
  "items": [
    {
      "id": "uuid",
      "identifier": "item-123",
      "display_text": "Primary display text",
      "data": { /* full instance data */ },
      "status": "published",
      "created_at": "2025-11-08T...",
      "children_count": 5,
      "has_children": true,
      "is_leaf": false
    }
  ],
  "total": 42,
  "limit": 100,
  "offset": 0,
  "has_more": false,
  "parent_id": null,
  "level_info": {
    "is_root_level": true,
    "hierarchy_config": { /* config */ }
  }
}
```

## Implementation Details

### Backend Changes

1. **Database Schema** (`models/content_type.py`)
   - Added `is_hierarchical` boolean column
   - Added `hierarchy_config` JSON column
   - Updated Pydantic schemas to include these fields

2. **Migration Script** (`scripts/add_hierarchy_fields.py`)
   - Adds new columns to `content_types` table
   - Configures CASE Standard as hierarchical

3. **Tree API Endpoint** (`api/v1/content_types.py`)
   - New `/instances/tree` endpoint
   - Filters by parent field in JSON data
   - Counts children for each node
   - Returns metadata for tree rendering

### Frontend Changes

1. **TreeView Component** (`components/TreeView.jsx`)
   - Expandable/collapsible nodes
   - Lazy-loads children on expand
   - Shows children count badges
   - Supports node selection
   - Click handler for navigation

2. **API Service** (`services/api.js`)
   - Added `listInstancesTree()` method

3. **AllContent Page** (`pages/AllContent.jsx`)
   - Detects hierarchical content types
   - Conditional rendering: TreeView vs Table
   - Separate queries for tree vs linear data
   - Navigate to instance on node click

## CASE Standards Example

The CASE Standard content type has been configured as hierarchical:

- **identifier_field**: `"identifier"` - Unique CASE item ID
- **parent_field**: `"parent"` - Points to parent item identifier
- **children_field**: `"children"` - Array of child identifiers
- **display_field**: `"full_statement"` - Standard description
- **secondary_display_field**: `"human_coding_scheme"` - Standard code

When you import CASE standards and filter by "CASE Standard" on the All Content page, you'll see:
- Root nodes displayed initially
- Arrow icons for nodes with children
- Click arrow to lazy-load and expand children
- Children count badges
- Full hierarchy navigation

## Usage

### Viewing Hierarchical Content

1. Go to **All Content** page
2. Filter by a hierarchical content type (e.g., "CASE Standard")
3. See tree view with expandable nodes
4. Click arrows to expand/collapse
5. Click node text to view details

### Creating Hierarchical Content Types

When creating or editing a content type:

1. Check the "Hierarchical" checkbox
2. Configure hierarchy fields:
   - Identifier field name in your data
   - Parent field name in your data
   - Children field name in your data
   - Display field for tree labels
   - Optional secondary display field

3. Ensure your content instances have:
   - Unique identifier
   - Parent identifier (or null for root)
   - Children array (can be empty)

## Benefits

1. **Handles Large Datasets**: Paginated at each level, only loads what's visible
2. **Performance**: Lazy-loading prevents overwhelming the browser
3. **Generic**: Works with any hierarchical structure, not just CASE
4. **Backward Compatible**: Non-hierarchical types still use table view
5. **User-Friendly**: Clear visual indication of hierarchy and navigation

## Future Enhancements

Potential improvements:
- Drag-and-drop to reorganize hierarchy
- Bulk operations on tree nodes
- Export hierarchy as nested JSON or CSV
- Search within tree with expand-to-match
- Virtualized rendering for very large trees
- Breadcrumb navigation showing current path

## Related Files

**Backend:**
- `/Users/colossus/development/content/backend/models/content_type.py`
- `/Users/colossus/development/content/backend/api/v1/content_types.py`
- `/Users/colossus/development/content/backend/scripts/add_hierarchy_fields.py`

**Frontend:**
- `/Users/colossus/development/content/frontend/src/components/TreeView.jsx`
- `/Users/colossus/development/content/frontend/src/pages/AllContent.jsx`
- `/Users/colossus/development/content/frontend/src/services/api.js`

## Testing

To test the hierarchical system:

1. Import CASE standards (already configured as hierarchical)
2. Go to All Content page
3. Filter by "CASE Standard"
4. Verify tree view appears with blue info banner
5. Click arrows to expand nodes
6. Verify children load and display
7. Click node text to navigate to detail page
8. Check pagination works at root level

---

**Note**: This system was implemented to solve the challenge of displaying large hierarchical datasets (like CASE standards with 140+ items) in a user-friendly, performant way with lazy-loading and pagination at each tree level.
