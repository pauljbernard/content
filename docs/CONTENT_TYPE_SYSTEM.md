# Flexible Content Type System - Design Document

## Overview

A flexible, composable content modeling system that allows users to define custom content types composed of reusable attribute types. This creates a schema-flexible CMS similar to Contentful, Strapi, or Drupal's field system.

## Core Concepts

### 1. Attribute Types (Primitives)

Basic building blocks that define the type of data an attribute can hold:

- **Text**: Short text (single line), Long text (multiline), Rich text (HTML/Markdown)
- **Number**: Integer, Decimal
- **Boolean**: True/False toggle
- **Date**: Date only, DateTime, Time only
- **Choice**: Single select, Multi select
- **Reference**: Link to other content (single, multiple)
- **Media**: File upload, Image, Video, Audio, Document
- **JSON**: Structured data object
- **URL**: Valid URL
- **Email**: Valid email address
- **Location**: Geographic coordinates

### 2. Content Types

User-defined schemas that define a type of content:

```json
{
  "id": "uuid",
  "name": "Lesson Plan",
  "description": "A structured lesson plan for K-12 education",
  "icon": "BookOpenIcon",
  "attributes": [
    {
      "name": "title",
      "label": "Lesson Title",
      "type": "text",
      "required": true,
      "config": {
        "maxLength": 200
      }
    },
    {
      "name": "grade_levels",
      "label": "Grade Levels",
      "type": "choice",
      "required": true,
      "config": {
        "multiple": true,
        "choices": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
      }
    },
    {
      "name": "duration",
      "label": "Duration (minutes)",
      "type": "number",
      "required": true,
      "config": {
        "min": 1,
        "max": 180
      }
    },
    {
      "name": "learning_objectives",
      "label": "Learning Objectives",
      "type": "long_text",
      "required": true
    },
    {
      "name": "standards",
      "label": "Aligned Standards",
      "type": "reference",
      "config": {
        "contentType": "standard",
        "multiple": true
      }
    },
    {
      "name": "materials",
      "label": "Materials Needed",
      "type": "json",
      "config": {
        "schema": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "quantity": {"type": "number"}
            }
          }
        }
      }
    }
  ],
  "created_by": "user_id",
  "created_at": "2025-11-07T12:00:00Z",
  "updated_at": "2025-11-07T12:00:00Z"
}
```

### 3. Content Instances

Actual content created based on a content type:

```json
{
  "id": "uuid",
  "content_type_id": "lesson-plan-type-id",
  "data": {
    "title": "Introduction to Fractions",
    "grade_levels": ["3", "4"],
    "duration": 45,
    "learning_objectives": "Students will understand the concept of fractions...",
    "standards": ["standard-id-1", "standard-id-2"],
    "materials": [
      {"name": "Fraction circles", "quantity": 30},
      {"name": "Whiteboard", "quantity": 1}
    ]
  },
  "status": "draft",
  "created_by": "user_id",
  "created_at": "2025-11-07T12:00:00Z",
  "updated_at": "2025-11-07T12:00:00Z"
}
```

## Database Schema

### content_types
```sql
CREATE TABLE content_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    is_system BOOLEAN DEFAULT FALSE,  -- true for built-in types
    attributes JSONB NOT NULL,  -- array of attribute definitions
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### content_instances
```sql
CREATE TABLE content_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_type_id UUID REFERENCES content_types(id) ON DELETE RESTRICT,
    data JSONB NOT NULL,  -- all attribute values
    status VARCHAR(50) DEFAULT 'draft',

    -- Workflow fields
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,

    -- Indexing for search
    search_vector tsvector
);

-- Index for fast queries
CREATE INDEX idx_content_instances_type ON content_instances(content_type_id);
CREATE INDEX idx_content_instances_status ON content_instances(status);
CREATE INDEX idx_content_instances_created_by ON content_instances(created_by);
CREATE INDEX idx_content_instances_search ON content_instances USING GIN(search_vector);
CREATE INDEX idx_content_instances_data ON content_instances USING GIN(data);
```

### content_relationships (for reference fields)
```sql
CREATE TABLE content_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_instance_id UUID REFERENCES content_instances(id) ON DELETE CASCADE,
    source_attribute VARCHAR(100) NOT NULL,
    target_instance_id UUID REFERENCES content_instances(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_content_relationships_source ON content_relationships(source_instance_id);
CREATE INDEX idx_content_relationships_target ON content_relationships(target_instance_id);
```

## API Design

### Content Types

#### List all content types
```
GET /api/v1/content-types
Response: [
  {
    "id": "uuid",
    "name": "Lesson Plan",
    "description": "...",
    "icon": "BookOpenIcon",
    "attributes": [...],
    "instance_count": 42,
    "created_at": "..."
  }
]
```

#### Create content type
```
POST /api/v1/content-types
Body: {
  "name": "Assessment",
  "description": "...",
  "icon": "ClipboardDocumentListIcon",
  "attributes": [...]
}
```

#### Get content type
```
GET /api/v1/content-types/{id}
```

#### Update content type
```
PUT /api/v1/content-types/{id}
```

#### Delete content type
```
DELETE /api/v1/content-types/{id}
```

### Content Instances

#### List instances of a type
```
GET /api/v1/content-types/{type_id}/instances
Query params: status, created_by, search, page, limit
```

#### Create instance
```
POST /api/v1/content-types/{type_id}/instances
Body: {
  "data": {
    "title": "...",
    "grade_levels": [...]
  }
}
```

#### Get instance
```
GET /api/v1/content-instances/{id}
```

#### Update instance
```
PUT /api/v1/content-instances/{id}
Body: {
  "data": {
    "title": "Updated title",
    ...
  }
}
```

#### Delete instance
```
DELETE /api/v1/content-instances/{id}
```

## Validation

Each attribute type has its own validation rules:

### Text
- `required`: boolean
- `minLength`: number
- `maxLength`: number
- `pattern`: regex string

### Number
- `required`: boolean
- `min`: number
- `max`: number
- `step`: number (for decimals)

### Choice
- `required`: boolean
- `choices`: array of strings
- `multiple`: boolean

### Reference
- `required`: boolean
- `contentType`: string (id of referenced content type)
- `multiple`: boolean

### Media
- `required`: boolean
- `allowedTypes`: array of MIME types
- `maxSize`: number (in bytes)

### JSON
- `required`: boolean
- `schema`: JSON Schema object

## Frontend Components

### 1. Content Type Builder
Location: `/content-types`

Features:
- List all content types with instance counts
- Create new content type wizard
- Edit content type (add/remove/reorder attributes)
- Delete content type (with confirmation)
- Preview content type form

### 2. Content Instance Manager
Location: `/content-types/{type_id}/instances`

Features:
- List all instances (table view)
- Filter by status, author, date
- Search instances
- Create new instance
- Bulk actions (delete, publish, archive)

### 3. Content Instance Editor
Location: `/content-instances/{id}`

Features:
- Dynamic form based on content type definition
- Field-specific input components:
  - Text: `<input>` or `<textarea>`
  - Number: `<input type="number">`
  - Boolean: `<Toggle>`
  - Date: `<DatePicker>`
  - Choice: `<Select>` or `<MultiSelect>`
  - Reference: `<ContentPicker>`
  - Media: `<FileUpload>`
  - Rich Text: `<RichTextEditor>`
  - JSON: `<CodeEditor>`
- Real-time validation
- Save draft / Publish
- Version history

### 4. Attribute Type Registry

Built-in attribute types with their input components:

```javascript
const ATTRIBUTE_TYPES = {
  text: {
    label: 'Short Text',
    icon: 'TextIcon',
    component: TextInput,
    defaultConfig: { maxLength: 255 }
  },
  long_text: {
    label: 'Long Text',
    icon: 'DocumentTextIcon',
    component: TextArea,
    defaultConfig: { maxLength: 10000 }
  },
  rich_text: {
    label: 'Rich Text',
    icon: 'PencilIcon',
    component: RichTextEditor,
    defaultConfig: {}
  },
  number: {
    label: 'Number',
    icon: 'NumberIcon',
    component: NumberInput,
    defaultConfig: { step: 1 }
  },
  boolean: {
    label: 'Boolean',
    icon: 'CheckIcon',
    component: Toggle,
    defaultConfig: { defaultValue: false }
  },
  date: {
    label: 'Date',
    icon: 'CalendarIcon',
    component: DatePicker,
    defaultConfig: {}
  },
  choice: {
    label: 'Choice',
    icon: 'ListBulletIcon',
    component: SelectInput,
    defaultConfig: { choices: [], multiple: false }
  },
  reference: {
    label: 'Reference',
    icon: 'LinkIcon',
    component: ContentPicker,
    defaultConfig: { multiple: false }
  },
  media: {
    label: 'Media',
    icon: 'PhotoIcon',
    component: FileUpload,
    defaultConfig: { allowedTypes: ['image/*'] }
  },
  json: {
    label: 'JSON',
    icon: 'CodeBracketIcon',
    component: CodeEditor,
    defaultConfig: { language: 'json' }
  }
};
```

## Migration Strategy

### Phase 1: Foundation (Backend)
1. Create database models
2. Create API endpoints for content types
3. Create API endpoints for content instances
4. Add validation logic
5. Add search functionality

### Phase 2: UI (Frontend)
1. Create Content Type Builder UI
2. Create Content Instance Manager UI
3. Create dynamic Content Instance Editor
4. Add search and filtering

### Phase 3: Integration
1. Migrate existing content types (lessons, assessments) to new system
2. Create system content types for backward compatibility
3. Add workflow integration (reviews, approvals)
4. Add versioning

### Phase 4: Advanced Features
1. Content type templates/starters
2. Import/export content types
3. Content type inheritance
4. Custom validation rules
5. Webhooks on content changes

## Example Use Cases

### Use Case 1: Lesson Plan
Content type with title, objectives, standards, activities, assessments, materials

### Use Case 2: Assessment
Content type with title, type, questions (JSON), rubric, answer key

### Use Case 3: Professional Development Module
Content type with title, duration, audience, learning outcomes, activities, resources

### Use Case 4: Curriculum Unit
Content type with title, grade, subject, lessons (references), assessments (references), pacing guide

## Security Considerations

1. **Permission checks**: Users can only create/edit content types if they have appropriate role
2. **Content ownership**: Instances track creator and can only be edited by creator or editors
3. **Validation**: All data is validated against content type definition
4. **SQL injection**: All JSONB queries use parameterized queries
5. **XSS prevention**: Rich text fields are sanitized

## Performance Considerations

1. **Indexing**: JSONB fields are indexed with GIN indexes
2. **Caching**: Content type definitions are cached (rarely change)
3. **Pagination**: All list endpoints support pagination
4. **Lazy loading**: References are loaded on-demand
5. **Search optimization**: Full-text search using PostgreSQL tsvector

## Next Steps

1. Review and approve this design
2. Create database migration scripts
3. Implement backend models and API
4. Build frontend UI components
5. Test and iterate
