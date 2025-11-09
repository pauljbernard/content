# Vector Indexing System - Complete Architecture

## Overview

The Content Management System implements a **per-content-type vector indexing architecture** that enables efficient semantic search across content instances and knowledge base files.

### Key Design Principles

1. **Filtered Partial Indexes** - Each content type gets its own specialized vector index
2. **Automatic Index Management** - Indexes created automatically when content types are created
3. **Automatic Embedding Generation** - Embeddings generated when instances are created/updated
4. **Multi-Type Search Efficiency** - PostgreSQL uses bitmap index scans across multiple specialized indexes
5. **Non-Blocking Operations** - Embedding generation failures don't block content creation

## Architecture

### Two Independent Vector Index Systems

#### 1. Content Instance Vector Indexes (Per Content Type)

**Purpose**: Enable semantic search on content instances (Subjects, Curricula, Lessons, etc.)

**Index Strategy**: Filtered partial indexes per content type
```sql
-- Example: Index for "Subject" content type
CREATE INDEX content_instances_embedding_ct_{subject_uuid}_idx
ON content_instances
USING ivfflat (embedding vector_cosine_ops)
WHERE content_type_id = '{subject_uuid}'
WITH (lists = 100)
```

**When Created**: Automatically when a new content type is created via `POST /content-types/`

**When Populated**: Automatically when content instances are created or updated

**Search Usage**: When an attribute is configured to search specific content types for RAG context

#### 2. Knowledge Base Vector Index (Single Global)

**Purpose**: Enable semantic search on knowledge base markdown files

**Index Strategy**: Single global index with category/subject/state filters
```sql
CREATE INDEX knowledge_base_embeddings_embedding_idx
ON knowledge_base_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100)
```

**When Created**: Manually via `python scripts/manage_kb_index.py init`

**When Populated**: Manually via `python scripts/manage_kb_index.py index`

**Search Usage**: When retrieval config enables `use_kb_vector_search: true`

## Lifecycle Workflows

### Content Type Creation Flow

```
User creates new content type
    ↓
POST /content-types/
    ↓
1. Validate content type schema
2. Save content type to DB
3. Create filtered vector index for this type ← AUTOMATIC
    ↓
Vector index ready for instances of this type
```

**Code**: `/backend/api/v1/content_types.py` lines 315-323

### Content Instance Creation Flow

```
User creates new content instance
    ↓
POST /content-types/{id}/instances
    ↓
1. Validate instance data
2. Save instance to DB
3. Generate embedding from instance data ← AUTOMATIC
4. Store embedding in vector index
    ↓
Instance is now searchable via semantic search
```

**Code**: `/backend/api/v1/content_types.py` lines 681-693

### Content Instance Update Flow

```
User updates content instance data
    ↓
PUT /instances/{id}
    ↓
1. Validate updated data
2. Merge and save to DB
3. Regenerate embedding ← AUTOMATIC (if data changed)
4. Update embedding in vector index
    ↓
Instance semantic search index is updated
```

**Code**: `/backend/api/v1/content_types.py` lines 975-988

### Knowledge Base Indexing Flow

```
Admin runs: python scripts/manage_kb_index.py init
    ↓
1. Create knowledge_base_embeddings table
2. Add embedding vector column
3. Create global vector index
    ↓
Admin runs: python scripts/manage_kb_index.py index
    ↓
1. Scan /reference/hmh-knowledge/ for .md files
2. For each file:
   - Calculate SHA-256 hash (change detection)
   - Extract category/subject/state from path
   - Generate embedding from file content
   - Store in knowledge_base_embeddings table
3. Skip unchanged files (hash comparison)
    ↓
Knowledge base is searchable via semantic search
```

**Code**: `/backend/scripts/manage_kb_index.py`

## Semantic Search Flow (RAG Context Assembly)

When an AI agent needs to generate content for a field:

```
Agent execution starts
    ↓
1. Extract ALL attributes from content instance
2. Build semantic query: "subject: Mathematics grade: 5 topic: Fractions"
    ↓
3. FOUR INDEPENDENT SEARCHES (in parallel):

   A. RAG Content Type Search (if configured)
      - For each selected content type ID
      - Ensure vector index exists for that type
      - PostgreSQL uses specialized filtered index
      - Returns top N most similar instances

   B. Knowledge Base Vector Search (if enabled)
      - Use same semantic query
      - Filter by category/subject/state
      - Returns top N most similar KB files

   C. Custom Prompt (if configured)
      - Load from attribute.ai_custom_prompt

   D. Agent Skills/Config
      - Load agent capabilities and instructions
    ↓
4. Assemble 4-Section Context:
   {
     "rag_content_instances": { ... },
     "knowledge_files": { ... },
     "custom_prompt": "...",
     "agent_config": { ... }
   }
    ↓
5. Pass to AI agent for generation
```

**Code**: `/backend/services/context_retrieval.py` lines 258-386

## Performance Optimization

### Why Per-Content-Type Indexes?

**Before (Global Index - SLOW)**:
```sql
-- ONE big index for ALL content types
CREATE INDEX content_instances_embedding_idx ...

-- Search must scan entire index, then filter
WHERE embedding IS NOT NULL
  AND content_type_id IN ('uuid1', 'uuid2', 'uuid3')  ← Post-filter
```

**After (Filtered Indexes - FAST)**:
```sql
-- Separate small index per content type
CREATE INDEX content_instances_embedding_ct_uuid1_idx
WHERE content_type_id = 'uuid1'

CREATE INDEX content_instances_embedding_ct_uuid2_idx
WHERE content_type_id = 'uuid2'

-- PostgreSQL uses bitmap index scan across specific indexes
-- Only scans relevant embeddings, not all instances
```

### Performance Benefits

- **Smaller Index Size**: Each filtered index only contains embeddings for one content type
- **Faster Searches**: Index scans are faster on smaller indexes
- **Parallel Index Usage**: PostgreSQL can use multiple indexes in parallel (bitmap scan)
- **Scalability**: Adding new content types doesn't slow down existing searches
- **Efficient Multi-Type Search**: When searching 3 types, only those 3 indexes are scanned

## Management Scripts

### Content Instance Embeddings

**Script**: `/backend/scripts/manage_content_embeddings.py`

```bash
# Initialize embedding column and create indexes for all content types
python scripts/manage_content_embeddings.py init

# Generate embeddings for instances that don't have them
python scripts/manage_content_embeddings.py index

# Force regenerate ALL embeddings (expensive)
python scripts/manage_content_embeddings.py reindex

# Show status: how many instances have embeddings, index coverage
python scripts/manage_content_embeddings.py status
```

**Use Cases**:
- Initial setup after adding embedding system
- Backfill embeddings for existing instances
- Regenerate after changing embedding model
- Check which instances are missing embeddings

### Knowledge Base Embeddings

**Script**: `/backend/scripts/manage_kb_index.py`

```bash
# Initialize knowledge base embeddings table and index
python scripts/manage_kb_index.py init

# Index all .md files in /reference/hmh-knowledge/
python scripts/manage_kb_index.py index

# Force reindex all files (ignores hash check)
python scripts/manage_kb_index.py reindex

# Show status: how many files indexed, category breakdown
python scripts/manage_kb_index.py status
```

**Use Cases**:
- Initial setup of knowledge base search
- Index new knowledge files after adding them
- Update changed files (uses SHA-256 hash to detect changes)
- Re-index after changing embedding model

## Configuration

### Content Type Attribute Configuration

When creating/editing a content type, each attribute can configure AI assist:

```json
{
  "name": "description",
  "type": "textarea",
  "ai_assist_enabled": true,
  "ai_agents": ["curriculum-architect", "content-developer"],
  "ai_rag_content_types": [
    "uuid-of-subject-type",
    "uuid-of-curriculum-type"
  ],
  "ai_custom_prompt": "Generate a grade-appropriate description that aligns with state standards...",
  "ai_output_schema": null
}
```

**When this field is generated**:
1. System searches the 2 selected content types using semantic search
2. System searches knowledge base (if enabled in agent config)
3. System includes custom prompt instructions
4. System loads agent skills/config
5. All 4 sections passed to AI agent

### Agent Configuration (Retrieval Config)

Built-in agents have retrieval configurations:

```python
"curriculum-architect": {
    "retrieval_config": {
        "content_types": [],  # Populated from attribute config
        "knowledge_base_paths": [
            "/universal/frameworks/",
            "/subjects/{subject}/common/"
        ],
        "use_kb_vector_search": True,  # ← Enables KB semantic search
        "filters": {}
    }
}
```

## Database Schema

### content_instances Table

```sql
CREATE TABLE content_instances (
    id VARCHAR(36) PRIMARY KEY,
    content_type_id VARCHAR(36) NOT NULL,
    data JSONB NOT NULL,
    status VARCHAR(20),
    embedding vector(1536),  -- ← OpenAI text-embedding-3-small
    created_by VARCHAR(36),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (content_type_id) REFERENCES content_types(id)
);

-- Filtered indexes created automatically per content type
CREATE INDEX content_instances_embedding_ct_{uuid}_idx
ON content_instances USING ivfflat (embedding vector_cosine_ops)
WHERE content_type_id = '{uuid}';
```

### knowledge_base_embeddings Table

```sql
CREATE TABLE knowledge_base_embeddings (
    id VARCHAR(36) PRIMARY KEY,
    file_path VARCHAR(500) UNIQUE NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,  -- SHA-256 for change detection
    embedding vector(1536),
    category VARCHAR(50) NOT NULL,      -- universal, subject-common, etc.
    subject VARCHAR(50),                -- mathematics, ela, etc.
    state VARCHAR(50),                  -- texas, california, etc.
    file_size_bytes INTEGER,
    last_modified TIMESTAMP,
    last_indexed TIMESTAMP
);

-- Global index with optional filtering
CREATE INDEX knowledge_base_embeddings_embedding_idx
ON knowledge_base_embeddings USING ivfflat (embedding vector_cosine_ops);
```

## API Endpoints

### Embedding-Related Endpoints

All handled automatically - no direct API needed:

- `POST /content-types/` → Creates content type + vector index
- `POST /content-types/{id}/instances` → Creates instance + generates embedding
- `PUT /instances/{id}` → Updates instance + regenerates embedding
- `POST /instances/{id}/generate-field` → Uses semantic search for RAG context

## Vector Search Service API

### VectorSearchService Methods

```python
class VectorSearchService:

    # Embedding generation
    async def generate_embedding(text: str) -> List[float]
    async def generate_content_embedding(content_data: dict) -> List[float]

    # Index management
    async def add_embedding_column(db, table_name, create_global_index=False)
    async def create_content_type_vector_index(db, content_type_id)
    async def ensure_content_type_indexes_exist(db, content_type_ids)

    # Instance embedding updates
    async def update_instance_embedding(db, instance_id, content_data)
    async def batch_generate_embeddings(db, batch_size=10, progress_callback=None)

    # Semantic search
    async def semantic_search(db, query_text, content_type_ids, limit, similarity_threshold)
```

## Troubleshooting

### Embeddings Not Generated

**Symptoms**: Instances exist but semantic search returns no results

**Check**:
```bash
python scripts/manage_content_embeddings.py status
```

**Fix**:
```bash
python scripts/manage_content_embeddings.py index
```

### Vector Index Missing for Content Type

**Symptoms**: Slow searches or errors about missing index

**Check**: Look for warnings in backend logs when content type was created

**Fix**:
```bash
python scripts/manage_content_embeddings.py init
```

### Knowledge Base Not Searchable

**Symptoms**: KB vector search returns no results

**Check**:
```bash
python scripts/manage_kb_index.py status
```

**Fix**:
```bash
python scripts/manage_kb_index.py init
python scripts/manage_kb_index.py index
```

### PostgreSQL pgvector Extension Not Installed

**Symptoms**: Errors about "vector" type not found

**Fix**:
```sql
-- Connect to your database
psql -U postgres -d your_database

-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

### Embedding Generation Failures

**Symptoms**: Warnings in logs about embedding generation failures

**Common Causes**:
1. OpenAI API key not configured
2. Rate limiting from OpenAI API
3. Instance data has no text content to embed
4. Network connectivity issues

**Fix**:
- Check LLM provider configuration has valid API key
- Check instance has text fields (title, description, content, etc.)
- Check backend logs for specific error messages

## Performance Tuning

### Embedding Dimensions

Default: `1536` (OpenAI text-embedding-3-small)

To use different model:
1. Configure in LLM Providers UI
2. Set as default for embeddings
3. Regenerate all embeddings:
   ```bash
   python scripts/manage_content_embeddings.py reindex
   python scripts/manage_kb_index.py reindex
   ```

### Index Lists Parameter

Default: `lists = 100`

**Rule of thumb**: Set to `sqrt(total_rows)` for optimal performance

```sql
-- For content type with 10,000 instances
WITH (lists = 100)  -- sqrt(10000) = 100

-- For content type with 100,000 instances
WITH (lists = 316)  -- sqrt(100000) ≈ 316
```

Modify in `/backend/services/vector_search.py` line 256 (content instances) and line 86 (knowledge base)

### Similarity Threshold

Default: `0.7` (70% similarity required)

**Adjust based on needs**:
- Higher (0.8-0.9): More precise, fewer results
- Lower (0.5-0.7): More recall, more results
- Very low (0.3-0.5): Broad matching, many results

Configured in:
- `/backend/services/context_retrieval.py` line 68 (content instances)
- `/backend/services/context_retrieval.py` line 243 (knowledge base)

## Monitoring

### Metrics to Track

1. **Embedding Coverage**: % of instances with embeddings
2. **Index Count**: Number of content type indexes created
3. **Search Performance**: Average query time for semantic searches
4. **Embedding Generation Rate**: Embeddings/second during batch operations
5. **API Failures**: Embedding generation failures (rate limiting, errors)

### Log Messages

**Success**:
```
✓ Created vector index for content type: Subject
✓ Generated embedding for new instance abc-123
✓ Regenerated embedding for updated instance xyz-789
```

**Warnings** (non-fatal):
```
Could not create vector index for content type {id}: {error}
Could not generate embedding for instance {id}: {error}
```

**Info**:
```
Semantic search returned 5 results (searched 3 content types)
KB semantic search returned 8 files
```

## Future Enhancements

### Planned Improvements

1. **Async Background Processing**: Use Celery/background tasks for embedding generation
2. **Batch Optimization**: Generate embeddings in batches to reduce API calls
3. **Caching Layer**: Cache frequently-searched embeddings in Redis
4. **Hybrid Search**: Combine vector search with keyword search (BM25)
5. **Dimension Reduction**: Support for reduced-dimension embeddings (512, 256)
6. **Multi-Modal Embeddings**: Support for image/video content embeddings
7. **Incremental Indexing**: Real-time index updates via database triggers
8. **Index Statistics**: Track index usage, query performance metrics

### Experimental Features

1. **Semantic Deduplication**: Detect near-duplicate content instances
2. **Content Clustering**: Group similar content automatically
3. **Anomaly Detection**: Identify content that doesn't match patterns
4. **Recommendation Engine**: "Similar content" suggestions

---

## Quick Reference

### Content Instance Embeddings
```bash
# One-time setup
python scripts/manage_content_embeddings.py init

# Generate missing embeddings
python scripts/manage_content_embeddings.py index

# Check coverage
python scripts/manage_content_embeddings.py status
```

### Knowledge Base Embeddings
```bash
# One-time setup
python scripts/manage_kb_index.py init

# Index all KB files
python scripts/manage_kb_index.py index

# Check status
python scripts/manage_kb_index.py status
```

### Automatic (No Action Needed)
- ✅ Vector indexes created when content types are created
- ✅ Embeddings generated when instances are created
- ✅ Embeddings updated when instances are updated
- ✅ Semantic search uses optimal per-type indexes

---

**Last Updated**: 2025-11-09
**Version**: 1.0.0
**Dependencies**: PostgreSQL 12+, pgvector 0.5.0+, OpenAI API
