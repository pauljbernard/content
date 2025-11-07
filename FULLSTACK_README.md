# HMH Content Management System - Full Stack Application

Comprehensive full-stack web application for the HMH Multi-Curriculum Knowledge Base with FastAPI backend and React frontend.

## Overview

This system provides a complete content management solution for educational curriculum development, featuring:

- **303 Knowledge Base Files** covering Pre-K through Grade 12
- **Role-Based Access Control** for teachers, authors, editors, and knowledge engineers
- **Content Authoring Workflow** with editorial review and approval
- **REST API** with comprehensive endpoints
- **Modern React UI** with responsive design

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  React Frontend                      │
│  (Vite + React 18 + TailwindCSS + React Query)      │
│  Port 3000                                           │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST
                   │ JSON
┌──────────────────▼──────────────────────────────────┐
│              FastAPI Backend                         │
│  (Python 3.10+ + SQLAlchemy + JWT Auth)             │
│  Port 8000                                           │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┬──────────────┐
        │                     │              │
┌───────▼─────────┐  ┌────────▼─────┐  ┌────▼──────┐
│   SQLite/       │  │  Knowledge    │  │  Config   │
│   PostgreSQL    │  │  Base Files   │  │  Files    │
│   (Content DB)  │  │  (303 .md)    │  │  (.json)  │
└─────────────────┘  └──────────────┘  └───────────┘
```

## Features

### Backend (FastAPI)

✅ **Authentication & Authorization**
- JWT token-based authentication
- Role-based access control (4 roles)
- Automatic token refresh
- Password hashing with bcrypt

✅ **Knowledge Base API**
- Browse 303 markdown files
- Hierarchical directory navigation
- Statistics by category/subject/state
- File content retrieval with metadata

✅ **Curriculum Configuration API**
- CRUD operations for curriculum configs
- JSON-based configuration management
- Knowledge resolution order definition

✅ **Content Authoring API**
- Create lessons, assessments, activities
- Draft, review, approval workflow
- Submit for editorial review

✅ **Review Workflow API**
- Pending review queue
- Editorial feedback and ratings
- Approval and publishing

✅ **Search API**
- Full-text search across knowledge base
- Filter by type, subject, state
- Search suggestions

✅ **Database Models**
- Users (authentication, roles)
- Content (lessons, assessments)
- Reviews (editorial workflow)

### Frontend (React)

✅ **User Interface**
- Responsive design (mobile-friendly)
- TailwindCSS styling
- Headless UI components
- Dark mode support (planned)

✅ **Role-Based Dashboards**
- Teacher: Browse and view published content
- Author: Create and submit content
- Editor: Review and approve content
- Knowledge Engineer: Manage system configuration

✅ **Knowledge Base Browser**
- Directory tree navigation
- Markdown file viewer with syntax highlighting
- Category, subject, state filters
- Breadcrumb navigation

✅ **Content Management**
- Create/edit lessons and assessments
- Submit for review
- View submission history
- Track approval status

✅ **State Management**
- Zustand for client state
- TanStack Query for server state
- Automatic cache invalidation
- Optimistic UI updates

## Quick Start

### Prerequisites

- **Backend**: Python 3.10+, pip
- **Frontend**: Node.js 18+, npm
- **Optional**: PostgreSQL for production database

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your settings
# At minimum, change SECRET_KEY

# Run the server
python main.py
```

Backend will start on http://localhost:8000

**API Documentation**: http://localhost:8000/api/v1/docs

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Frontend will start on http://localhost:3000

### 3. Initial Login

**Default admin credentials**:
- Email: `admin@hmhco.com`
- Password: `changeme`

**⚠️ Change these credentials immediately in production!**

## Project Structure

```
content/
├── backend/                 # FastAPI backend
│   ├── api/
│   │   └── v1/             # API v1 endpoints
│   │       ├── auth.py     # Authentication
│   │       ├── users.py    # User management
│   │       ├── knowledge_base.py  # Knowledge API
│   │       ├── curriculum_configs.py  # Config API
│   │       ├── content.py  # Content API
│   │       ├── reviews.py  # Review API
│   │       └── search.py   # Search API
│   ├── core/
│   │   ├── config.py       # App configuration
│   │   └── security.py     # Auth & security
│   ├── database/
│   │   └── session.py      # DB session
│   ├── models/
│   │   ├── user.py         # User models
│   │   └── content.py      # Content models
│   ├── services/
│   │   └── user_service.py # Business logic
│   ├── main.py             # FastAPI app
│   ├── requirements.txt    # Python deps
│   └── README.md           # Backend docs
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   │   └── Layout.jsx
│   │   ├── pages/         # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── KnowledgeBase.jsx
│   │   ├── services/
│   │   │   └── api.js     # API client
│   │   ├── store/
│   │   │   └── authStore.js  # Auth state
│   │   ├── App.jsx        # Main app
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Node deps
│   └── README.md          # Frontend docs
│
├── reference/
│   └── hmh-knowledge/     # 303 knowledge files
│
├── config/
│   └── curriculum/        # Curriculum configs
│
└── FULLSTACK_README.md    # This file
```

## API Documentation

### Authentication Endpoints

**POST /api/v1/auth/register**
- Register new user
- Body: `{email, password, full_name, role}`

**POST /api/v1/auth/login**
- Login with email/password
- Returns: JWT access & refresh tokens

**POST /api/v1/auth/refresh**
- Refresh expired access token

### Knowledge Base Endpoints

**GET /api/v1/knowledge/stats**
- Get knowledge base statistics

**GET /api/v1/knowledge/browse?path={path}**
- Browse directory at path

**GET /api/v1/knowledge/file?path={path}**
- Get file content and metadata

**GET /api/v1/knowledge/subjects**
- List all subjects

**GET /api/v1/knowledge/states**
- List all states/districts

### Content Endpoints

**GET /api/v1/content/**
- List content (filtered by role)

**POST /api/v1/content/**
- Create new content

**GET /api/v1/content/{id}**
- Get content by ID

**PUT /api/v1/content/{id}**
- Update content

**POST /api/v1/content/{id}/submit**
- Submit for review

### Review Endpoints

**GET /api/v1/reviews/pending**
- Get pending reviews (editors)

**POST /api/v1/reviews/**
- Create review

**POST /api/v1/reviews/content/{id}/approve**
- Approve and publish

See full API documentation at http://localhost:8000/api/v1/docs

## User Roles

| Role | Permissions |
|------|-------------|
| **teacher** | View published content, browse knowledge base |
| **author** | Create content, submit for review, all teacher permissions |
| **editor** | Review content, approve/reject, all author permissions |
| **knowledge_engineer** | Manage configs, admin access, all editor permissions |

## Development

### Running Both Services

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Making Changes

**Backend Changes:**
1. Edit Python files in `backend/`
2. FastAPI will auto-reload
3. Test API at http://localhost:8000/api/v1/docs

**Frontend Changes:**
1. Edit JSX files in `frontend/src/`
2. Vite will hot-reload
3. See changes immediately at http://localhost:3000

### Adding New Features

**New API Endpoint:**
1. Create/edit router in `backend/api/v1/`
2. Add Pydantic models
3. Include router in `main.py`
4. Update frontend API client in `frontend/src/services/api.js`

**New Page:**
1. Create page component in `frontend/src/pages/`
2. Add route in `frontend/src/App.jsx`
3. Add navigation link in `frontend/src/components/Layout.jsx`

## Production Deployment

### Backend

1. **Use PostgreSQL instead of SQLite**

```env
DATABASE_URL="postgresql://user:pass@host:5432/db"
```

2. **Generate secure secret key**

```bash
openssl rand -hex 32
```

Update `SECRET_KEY` in `.env`

3. **Run with production server**

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend

1. **Build production bundle**

```bash
cd frontend
npm run build
```

2. **Deploy `dist/` folder** to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- Or serve from backend static files

3. **Set environment variables**

```env
VITE_API_URL=https://api.yourdomain.com
```

### Security Checklist

- [ ] Change default admin password
- [ ] Generate new SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Enable CORS only for your domain
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set up backup strategy
- [ ] Enable rate limiting
- [ ] Review user permissions

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Troubleshooting

### Backend won't start

1. Check Python version: `python --version` (need 3.10+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check if port 8000 is in use

### Frontend can't connect to API

1. Verify backend is running on port 8000
2. Check `.env.local` has correct `VITE_API_URL`
3. Look for CORS errors in browser console
4. Update backend `.env`: `BACKEND_CORS_ORIGINS=["http://localhost:3000"]`

### Database errors

1. Delete `content.db` (development only!)
2. Restart backend to recreate tables
3. Or use Alembic migrations for production

## Performance

### Backend

- SQLite: Good for dev, < 1000 users
- PostgreSQL: Production, scales to millions
- Add Redis for caching (future enhancement)

### Frontend

- Code splitting with React.lazy()
- Image optimization
- TanStack Query caching (5 min default)
- Lazy load heavy components

## Future Enhancements

- [ ] Real-time collaboration (WebSockets)
- [ ] Advanced search (Elasticsearch)
- [ ] Export to PDF/DOCX
- [ ] Version control for content
- [ ] Comments and annotations
- [ ] Analytics dashboard
- [ ] Professor Framework integration
- [ ] Git integration for version control
- [ ] Automated testing suite
- [ ] CI/CD pipeline

## Support

- **API Docs**: http://localhost:8000/api/v1/docs
- **Backend README**: [backend/README.md](backend/README.md)
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **Knowledge Base Docs**: [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)

## License

Internal HMH project. All rights reserved.

---

**Version:** 1.0.0
**Last Updated:** 2025-11-06
**Tech Stack:** FastAPI + React + SQLAlchemy + TailwindCSS
**Knowledge Base Files:** 303 (Pre-K-12)
**Student Coverage:** 90M+ (US Pre-K-12 + International)
