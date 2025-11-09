# Pagination and Bulk Actions Implementation Plan

## Overview

This document outlines the requirements and implementation plan for:
1. **Pagination** - All list endpoints must have proper pagination to avoid open-ended queries
2. **Bulk Actions** - UI tables need checkboxes and bulk delete functionality

## Current Status

### Endpoints with Pagination ✅

| Endpoint | Pagination | Metadata | Max Limit |
|----------|-----------|----------|-----------|
| `GET /api/v1/standards/` | ✅ Yes (skip/limit) | ⚠️ Partial (no metadata wrapper) | 50 |
| `GET /api/v1/standards/import` | ✅ Yes (skip/limit) | ⚠️ Partial | 20 |
| `GET /api/v1/secrets/` | ✅ Yes (skip/limit) | ❌ No metadata | 1000 |
| `GET /api/v1/standards/case-network/frameworks` | ✅ Yes (limit/offset) | ✅ Full metadata | 500 |

### Endpoints Needing Review

| Endpoint | Current Status | Risk Level |
|----------|---------------|------------|
| `GET /api/v1/content-types/` | Unknown | Medium |
| `GET /api/v1/content-instances/` | Unknown | **HIGH** |
| `GET /api/v1/knowledge/` | Unknown | Medium |
| `GET /api/v1/users/` | Unknown | Low |

## Implementation Requirements

### 1. Backend - Pagination Standard

All list endpoints MUST:

1. **Accept pagination parameters:**
   ```python
   limit: int = Query(100, ge=1, le=500)
   offset: int = Query(0, ge=0)
   ```

2. **Return paginated response with metadata:**
   ```json
   {
     "items": [...],
     "total": 1234,
     "limit": 100,
     "offset": 0,
     "has_more": true
   }
   ```

3. **Apply database limits:**
   ```python
   query = query.offset(offset).limit(limit)
   ```

4. **Never allow unbounded queries** - Always have a maximum limit (recommended 500)

### 2. Frontend - Pagination UI

All list pages MUST implement:

1. **Pagination controls:**
   - Previous/Next buttons
   - Page number display
   - Items per page selector (25, 50, 100)
   - Total count display: "Showing 1-50 of 1,234"

2. **Loading states:**
   - Show loading spinner when fetching
   - Disable pagination controls during load

3. **Query parameters:**
   - Sync pagination state with URL (`?page=2&limit=50`)
   - Preserve filters when paginating

### 3. Bulk Actions Requirements

All list pages MUST implement:

#### Backend:

1. **Bulk delete endpoint:**
   ```python
   @router.delete("/bulk")
   async def bulk_delete(
       ids: List[int],
       current_user: User = Depends(get_author)
   )
   ```

2. **Permissions check:**
   - Verify user has delete permission for ALL selected items
   - Return 403 if any item cannot be deleted
   - Use database transactions (all-or-nothing)

3. **Validation:**
   - Maximum 100 items per bulk operation
   - Return clear error if limit exceeded

#### Frontend:

1. **Checkbox column (leftmost):**
   - Header checkbox (select/deselect all on current page)
   - Row checkbox for each item
   - Visual indication of selected state

2. **Bulk actions bar (above table):**
   - Appears when 1+ items selected
   - Shows count: "3 items selected"
   - Delete button with confirmation modal
   - Clear selection button

3. **Confirmation modal:**
   ```
   Delete X items?

   This action cannot be undone.

   [Cancel] [Delete]
   ```

4. **State management:**
   - Track selected IDs in React state
   - Clear selection after successful delete
   - Handle pagination (selected items may be on different pages)

## Implementation Priority

### Phase 1: Critical (High Risk) ✅ IN PROGRESS

- [x] Add pagination to CASE Network frameworks endpoint
- [ ] Review content-instances endpoint (likely has thousands of records)
- [ ] Add pagination metadata wrapper to all endpoints

### Phase 2: Bulk Delete (Most Requested)

- [ ] Add bulk delete endpoint for Standards
- [ ] Implement checkbox UI for Standards list
- [ ] Add bulk delete endpoint for Secrets
- [ ] Implement checkbox UI for Secrets list

### Phase 3: Content Types

- [ ] Review and add pagination to content-types endpoints
- [ ] Review and add pagination to content-instances endpoints
- [ ] Add bulk delete for content instances

### Phase 4: Polish

- [ ] Add pagination to all remaining list endpoints
- [ ] Standardize pagination UI component
- [ ] Add bulk actions to all list pages
- [ ] Performance testing with large datasets

## Code Examples

### Backend Pagination Pattern

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int
    has_more: bool

@router.get("/items", response_model=PaginatedResponse[ItemPublic])
async def list_items(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Item)
    total = query.count()
    items = query.offset(offset).limit(limit).all()

    return PaginatedResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + len(items)) < total
    )
```

### Backend Bulk Delete Pattern

```python
from pydantic import BaseModel

class BulkDeleteRequest(BaseModel):
    ids: List[int]

@router.delete("/bulk")
async def bulk_delete(
    request: BulkDeleteRequest,
    current_user: User = Depends(get_author),
    db: Session = Depends(get_db)
):
    if len(request.ids) > 100:
        raise HTTPException(400, "Maximum 100 items per bulk operation")

    if not request.ids:
        raise HTTPException(400, "No IDs provided")

    try:
        # Check permissions for all items first
        items = db.query(Item).filter(Item.id.in_(request.ids)).all()

        if len(items) != len(request.ids):
            raise HTTPException(404, "Some items not found")

        # Verify user can delete all items
        for item in items:
            if item.created_by_id != current_user.id and current_user.role != "admin":
                raise HTTPException(403, f"Cannot delete item {item.id}")

        # Delete all (transaction)
        db.query(Item).filter(Item.id.in_(request.ids)).delete(synchronize_session=False)
        db.commit()

        return {"success": True, "deleted": len(items)}

    except Exception as e:
        db.rollback()
        raise
```

### Frontend Pagination Hook

```javascript
const usePagination = (fetchFn, limit = 50) => {
  const [page, setPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(limit);

  const offset = (page - 1) * itemsPerPage;

  const { data, isLoading } = useQuery({
    queryKey: ['items', page, itemsPerPage],
    queryFn: () => fetchFn({ limit: itemsPerPage, offset }),
  });

  const totalPages = Math.ceil((data?.total || 0) / itemsPerPage);

  return {
    items: data?.items || [],
    total: data?.total || 0,
    page,
    totalPages,
    itemsPerPage,
    setPage,
    setItemsPerPage,
    hasMore: data?.has_more || false,
    isLoading,
  };
};
```

### Frontend Bulk Selection Hook

```javascript
const useBulkSelection = () => {
  const [selectedIds, setSelectedIds] = useState(new Set());

  const toggleItem = (id) => {
    setSelectedIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const toggleAll = (items) => {
    const allSelected = items.every(item => selectedIds.has(item.id));
    if (allSelected) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(items.map(item => item.id)));
    }
  };

  const clearSelection = () => setSelectedIds(new Set());

  return {
    selectedIds,
    selectedCount: selectedIds.size,
    isSelected: (id) => selectedIds.has(id),
    toggleItem,
    toggleAll,
    clearSelection,
  };
};
```

## Testing Requirements

### Pagination Tests

- [ ] Verify offset/limit parameters work correctly
- [ ] Test with 0 results
- [ ] Test with exactly limit results
- [ ] Test with more than limit results
- [ ] Verify total count is accurate
- [ ] Test navigation to last page

### Bulk Delete Tests

- [ ] Delete single item
- [ ] Delete multiple items (2-10)
- [ ] Try to delete more than 100 items (should fail)
- [ ] Try to delete non-existent items (should fail)
- [ ] Try to delete items user doesn't own (should fail for non-admins)
- [ ] Verify transaction rollback on error
- [ ] Verify all items deleted or none deleted

## Security Considerations

1. **Pagination Limits:**
   - Always enforce maximum limits (500 recommended)
   - Prevent DoS through large limit values

2. **Bulk Operations:**
   - Rate limit bulk delete operations
   - Log all bulk deletes for audit
   - Verify permissions for EVERY item
   - Use database transactions

3. **SQL Injection:**
   - Always use parameterized queries
   - Never concatenate user input into SQL

## Performance Considerations

1. **Database Indexes:**
   - Ensure indexed columns for pagination (created_at, updated_at, id)
   - Add composite indexes for common filter combinations

2. **Count Queries:**
   - Consider caching total counts for large tables
   - Use approximate counts for very large tables (>1M rows)

3. **Bulk Operations:**
   - Use batch operations instead of loops
   - Delete in chunks for very large selections (>1000)

---

**Last Updated:** 2025-11-08
**Status:** Phase 1 In Progress
