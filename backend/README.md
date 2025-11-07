# HMH Content Management System - Backend API

Comprehensive REST API for the HMH Multi-Curriculum Knowledge Base, built with FastAPI.

## Features

- **Knowledge Base API**: Browse and search 303 knowledge files across Pre-K-12
- **Curriculum Configs**: Manage curriculum configurations for different states/subjects
- **Content Authoring**: Create, edit, and manage lessons, assessments, and activities
- **Review Workflow**: Editorial review and approval process
- **User Management**: Role-based access control (authors, editors, engineers, teachers)
- **Full-text Search**: Search across knowledge base and content
- **JWT Authentication**: Secure token-based authentication

## Architecture

```
backend/
├── api/
│   └── v1/              # API v1 endpoints
│       ├── auth.py      # Authentication (login, register, refresh)
│       ├── users.py     # User management
│       ├── knowledge_base.py  # Knowledge base browsing
│       ├── curriculum_configs.py  # Curriculum configs
│       ├── content.py   # Content authoring
│       ├── reviews.py   # Review workflow
│       └── search.py    # Search functionality
├── core/
│   ├── config.py        # Application configuration
│   └── security.py      # Authentication & authorization
├── database/
│   └── session.py       # Database session management
├── models/
│   ├── user.py          # User models
│   └── content.py       # Content models
├── services/
│   └── user_service.py  # User business logic
└── main.py              # FastAPI application
```

## User Roles

- **teacher**: Browse and view published content
- **author**: Create and submit content for review
- **editor**: Review and approve content
- **knowledge_engineer**: Manage knowledge base and configs (superuser)

## Quick Start

### Prerequisites

- Python 3.10+
- pip or uv package manager

### Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Create `.env` file:**

```bash
cp .env.example .env
```

Edit `.env` with your settings (see Configuration section below).

3. **Initialize database:**

The database will be automatically created on first run (SQLite by default).

4. **Run the server:**

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. **Access API documentation:**

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Configuration

Create a `.env` file in the backend directory:

```env
# API Configuration
PROJECT_NAME="HMH Content Management System"
API_V1_STR="/api/v1"
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Database
DATABASE_URL="sqlite:///./content.db"
# For PostgreSQL:
# DATABASE_URL="postgresql://user:password@localhost/content_db"

# Security
SECRET_KEY="your-secret-key-here-use-openssl-rand-hex-32"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Paths (relative to backend directory)
KNOWLEDGE_BASE_PATH="../reference/hmh-knowledge"
CURRICULUM_CONFIG_PATH="../config/curriculum"
CONTENT_PATH="../"

# Admin User
FIRST_SUPERUSER_EMAIL="admin@hmhco.com"
FIRST_SUPERUSER_PASSWORD="changeme"

# Features
PROFESSOR_ENABLED=false
GIT_ENABLED=true
GIT_AUTO_COMMIT=false
```

## API Endpoints

### Authentication

**POST /api/v1/auth/register**
- Register new user
- Body: `{email, password, full_name, role}`
- Returns: User object

**POST /api/v1/auth/login**
- Login with email/password
- Body: `{username (email), password}`
- Returns: `{access_token, refresh_token, token_type}`

**POST /api/v1/auth/refresh**
- Refresh access token
- Body: `{refresh_token}`
- Returns: New tokens

### Knowledge Base

**GET /api/v1/knowledge/stats**
- Get knowledge base statistics
- Returns: File counts by category, subject, state

**GET /api/v1/knowledge/browse?path={path}**
- Browse knowledge base directory
- Returns: List of files and directories

**GET /api/v1/knowledge/file?path={path}**
- Get knowledge file content
- Returns: File content and metadata

**GET /api/v1/knowledge/subjects**
- Get list of subjects

**GET /api/v1/knowledge/states**
- Get list of states/districts

### Curriculum Configs

**GET /api/v1/curriculum-configs/**
- List all curriculum configurations
- Query params: `subject`, `district`

**GET /api/v1/curriculum-configs/{config_id}**
- Get specific config

**POST /api/v1/curriculum-configs/** (Engineers only)
- Create new config

**PUT /api/v1/curriculum-configs/{config_id}** (Engineers only)
- Update config

**DELETE /api/v1/curriculum-configs/{config_id}** (Engineers only)
- Delete config

### Content

**GET /api/v1/content/**
- List content (filtered by role and status)
- Query params: `status`, `content_type`, `subject`, `grade_level`, `state`

**POST /api/v1/content/** (Authors+)
- Create new content

**GET /api/v1/content/{content_id}**
- Get content by ID

**PUT /api/v1/content/{content_id}** (Authors+)
- Update content

**DELETE /api/v1/content/{content_id}** (Authors+)
- Delete content

**POST /api/v1/content/{content_id}/submit** (Authors)
- Submit content for review

### Reviews

**GET /api/v1/reviews/pending** (Editors)
- Get content pending review

**POST /api/v1/reviews/** (Editors)
- Create content review

**GET /api/v1/reviews/content/{content_id}**
- Get all reviews for content

**POST /api/v1/reviews/content/{content_id}/approve** (Editors)
- Approve and publish content

**GET /api/v1/reviews/my-reviews** (Editors)
- Get reviews created by current user

### Search

**GET /api/v1/search/?q={query}**
- Search knowledge base and content
- Query params: `q`, `type`, `subject`, `state`, `limit`

**GET /api/v1/search/suggest?q={prefix}**
- Get search suggestions

### Users

**GET /api/v1/users/me**
- Get current user info

**PUT /api/v1/users/me**
- Update current user

**GET /api/v1/users/** (Superuser)
- List all users

**GET /api/v1/users/{user_id}** (Superuser)
- Get user by ID

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication.

### Using the API

1. **Register or login:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@hmhco.com&password=changeme"
```

2. **Use the access token:**

```bash
curl -X GET "http://localhost:8000/api/v1/knowledge/stats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

3. **Refresh token when expired:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
```

## Database Schema

### Users Table

- id (PK)
- email (unique)
- hashed_password
- full_name
- role (teacher, author, editor, knowledge_engineer)
- is_active
- is_superuser
- created_at, updated_at, last_login

### Content Table

- id (PK)
- title
- content_type (lesson, assessment, activity, guide, framework)
- status (draft, in_review, needs_revision, approved, published, archived)
- subject, grade_level, state
- standards_aligned (JSON)
- file_content (text)
- author_id (FK to users)
- timestamps

### Content Reviews Table

- id (PK)
- content_id (FK)
- reviewer_id (FK to users)
- status (approved, needs_revision, rejected)
- comments
- checklist_results (JSON)
- rating (1-5)
- timestamps

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint
flake8 .

# Type check
mypy .
```

### Adding New Endpoints

1. Create router in `api/v1/`
2. Define Pydantic models for request/response
3. Implement endpoint logic
4. Add router to `main.py`
5. Update this README

## Production Deployment

### Using Docker

```bash
docker build -t hmh-cms-backend .
docker run -p 8000:8000 --env-file .env hmh-cms-backend
```

### Using PostgreSQL

1. Install PostgreSQL
2. Create database: `createdb content_db`
3. Update `.env`: `DATABASE_URL="postgresql://user:password@localhost/content_db"`
4. Run migrations (if using Alembic)

### Environment Variables

Required for production:
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `DATABASE_URL`: Production database URL
- `BACKEND_CORS_ORIGINS`: List of allowed origins for CORS

## Troubleshooting

### Database Issues

- **SQLite locked**: Reduce concurrent requests or switch to PostgreSQL
- **Migration errors**: Delete `content.db` and restart (development only)

### Import Errors

- Ensure all `__init__.py` files exist
- Check Python path: `export PYTHONPATH="${PYTHONPATH}:/path/to/backend"`

### Permission Errors

- Check file permissions on knowledge base path
- Ensure user has read access to `../reference/hmh-knowledge/`

## API Versioning

Current version: v1

Breaking changes will be introduced in v2 while maintaining v1 compatibility.

## Support

- API Documentation: http://localhost:8000/api/v1/docs
- Issues: Create GitHub issue
- Email: support@hmhco.com

---

**Version:** 1.0.0
**Last Updated:** 2025-11-06
