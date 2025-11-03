# Version Control & Revision Management Skill

**Skill**: `/curriculum.version-control`
**Category**: Curriculum Development
**Addresses**: GAP-1 (CRITICAL)
**Purpose**: Manage curriculum versions, revisions, and branching for multi-edition product lines

## Description

Provides semantic versioning, branch management, revision tracking, and changelog generation for curriculum products. Essential for publishers maintaining multiple concurrent versions (state editions, year updates, custom editions).

## Usage

```bash
/curriculum.version-control \
  --action "create-version|create-branch|merge|diff|changelog" \
  --project-id "7th-grade-math" \
  --version "2.0.0" \
  --branch "california-edition" \
  --base-version "1.5.0"
```

## Actions

### 1. Create Version

Creates a new semantic version of the curriculum.

**Parameters**:
- `project-id`: Curriculum project identifier
- `version`: Semantic version (major.minor.patch)
- `description`: Version description
- `changes`: List of changes from previous version

**Output**:
- Version manifest with timestamp, author, changes
- Tagged snapshot of all curriculum artifacts
- Version comparison report

### 2. Create Branch

Creates a branch for variant development (state-specific, custom editions).

**Parameters**:
- `project-id`: Base curriculum identifier
- `branch`: Branch name (e.g., "texas-edition", "2025-update")
- `base-version`: Version to branch from
- `description`: Branch purpose

**Output**:
- Branch manifest
- Copy of all artifacts at base version
- Tracking file for divergence from main

### 3. Merge Branches

Merges changes from one branch into another.

**Parameters**:
- `project-id`: Curriculum identifier
- `source-branch`: Branch to merge from
- `target-branch`: Branch to merge into
- `conflict-resolution`: "auto" | "manual" | "prefer-source" | "prefer-target"

**Output**:
- Merge report (conflicts, auto-merged sections, manual review needed)
- Updated target branch
- Changelog of merged changes

### 4. Generate Diff

Compares two versions or branches.

**Parameters**:
- `project-id`: Curriculum identifier
- `compare-from`: Version or branch name
- `compare-to`: Version or branch name
- `detail-level`: "summary" | "detailed" | "line-by-line"

**Output**:
- Diff report showing:
  - Added/removed/modified lessons
  - Changed learning objectives
  - Modified assessments
  - Updated standards alignment
  - Media changes
- HTML diff visualization

### 5. Generate Changelog

Automatically generates changelog from version history.

**Parameters**:
- `project-id`: Curriculum identifier
- `from-version`: Starting version
- `to-version`: Ending version
- `format`: "markdown" | "html" | "pdf"
- `audience`: "internal" | "client" | "student"

**Output**:
- Formatted changelog with categories:
  - New Features
  - Content Updates
  - Standards Alignment Changes
  - Bug Fixes
  - Removed Content
- Client-friendly language (non-technical)

## Version Manifest Format

```json
{
  "project_id": "7th-grade-math",
  "version": "2.0.0",
  "created": "2025-11-02T10:00:00Z",
  "author": "Professor System",
  "base_version": "1.5.0",
  "type": "major",
  "description": "2025 Edition - Updated to new state standards",
  "changes": [
    {
      "category": "standards",
      "description": "Aligned to California Mathematics Framework 2023",
      "artifacts_affected": ["unit-1", "unit-3", "unit-5"]
    },
    {
      "category": "content",
      "description": "Added 12 new lessons on data science",
      "artifacts_affected": ["unit-7"]
    }
  ],
  "artifacts": {
    "curriculum_design": "curriculum-design-v2.0.0.json",
    "lesson_plans": "lesson-plans-v2.0.0/",
    "assessments": "assessments-v2.0.0/",
    "media": "media-v2.0.0/"
  },
  "statistics": {
    "total_lessons": 145,
    "total_assessments": 58,
    "total_standards": 87,
    "changes_from_previous": {
      "lessons_added": 12,
      "lessons_modified": 23,
      "lessons_removed": 2,
      "assessments_modified": 15
    }
  }
}
```

## Branch Tracking Format

```json
{
  "project_id": "7th-grade-math",
  "branch": "texas-edition",
  "base_version": "2.0.0",
  "created": "2025-11-02T11:00:00Z",
  "purpose": "Texas TEKS alignment for 2025-2026 school year",
  "divergence_tracking": {
    "common_content": ["unit-1", "unit-2", "unit-4", "unit-6"],
    "texas_specific": ["unit-3-texas", "unit-5-texas"],
    "removed_from_base": ["unit-8"],
    "last_synced_from_main": "2025-10-15T09:00:00Z"
  },
  "merge_history": [
    {
      "timestamp": "2025-10-15T09:00:00Z",
      "merged_from": "main",
      "conflicts": 3,
      "auto_resolved": 2,
      "manual_resolved": 1
    }
  ]
}
```

## Use Cases

### Use Case 1: Publisher Annual Update

**Scenario**: EdVenture Learning releases annual updates to their 7th Grade Math curriculum.

```bash
# Create 2025 edition
/curriculum.version-control \
  --action create-version \
  --project-id "7th-grade-math" \
  --version "3.0.0" \
  --base-version "2.5.2" \
  --description "2025 Edition - Updated standards, new data science unit"

# Generate changelog for customers
/curriculum.version-control \
  --action changelog \
  --project-id "7th-grade-math" \
  --from-version "2.5.2" \
  --to-version "3.0.0" \
  --format "pdf" \
  --audience "client"
```

### Use Case 2: State-Specific Editions

**Scenario**: Create Texas and California editions from national curriculum.

```bash
# Create Texas branch
/curriculum.version-control \
  --action create-branch \
  --project-id "7th-grade-math" \
  --branch "texas-edition" \
  --base-version "3.0.0" \
  --description "TEKS alignment for Texas adoption"

# Create California branch
/curriculum.version-control \
  --action create-branch \
  --project-id "7th-grade-math" \
  --branch "california-edition" \
  --base-version "3.0.0" \
  --description "CA Mathematics Framework 2023 alignment"

# Later: merge common updates from main
/curriculum.version-control \
  --action merge \
  --project-id "7th-grade-math" \
  --source-branch "main" \
  --target-branch "texas-edition" \
  --conflict-resolution "prefer-target"
```

### Use Case 3: Revision Tracking

**Scenario**: Compare what changed between versions for client communication.

```bash
/curriculum.version-control \
  --action diff \
  --project-id "7th-grade-math" \
  --compare-from "2.5.2" \
  --compare-to "3.0.0" \
  --detail-level "detailed"
```

## Implementation Notes

### Storage Structure

```
~/.claude/curriculum-versions/
  {project-id}/
    versions/
      v1.0.0/
        manifest.json
        artifacts/
          curriculum-design.json
          lesson-plans/
          assessments/
      v2.0.0/
        manifest.json
        artifacts/
    branches/
      texas-edition/
        branch-manifest.json
        artifacts/
      california-edition/
        branch-manifest.json
        artifacts/
    changelogs/
      v1.0.0-to-v2.0.0.md
      v2.0.0-to-v3.0.0.md
```

### Semantic Versioning Rules

- **Major version** (X.0.0): Breaking changes (standards framework change, scope change)
- **Minor version** (1.X.0): New content (new units, lessons, assessments)
- **Patch version** (1.0.X): Bug fixes (typos, alignment corrections, minor updates)

### Conflict Resolution

When merging branches:
- **Auto-merge**: Non-overlapping changes to different lessons
- **Manual review needed**: Same lesson modified in both branches
- **Metadata conflicts**: Standards alignment, learning objectives
- **Asset conflicts**: Images, videos with same filename but different content

## Integration with Agents

- **Curriculum Architect Agent**: Automatically creates versions at quality gate passages
- **Quality Assurance Agent**: Validates version consistency before tagging
- **Content Developer Agent**: Works within branches for variant development

## Performance Metrics

- **Version creation time**: <2 minutes for full curriculum snapshot
- **Diff generation**: <30 seconds for detailed comparison
- **Merge operation**: <5 minutes for typical branch merge
- **Storage efficiency**: Deduplication of unchanged artifacts

## Success Criteria

- ✅ Publishers can maintain 5+ concurrent product versions
- ✅ State editions can diverge and merge common updates
- ✅ Complete revision history with accountability
- ✅ Client-ready changelogs generated automatically
- ✅ No loss of data during version operations

---

**Status**: Ready for implementation
**Dependencies**: State Manager (framework/state-manager.py)
**Testing**: Requires test with multi-state curriculum project
