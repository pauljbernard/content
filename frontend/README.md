# HMH Content Management System - Frontend

React-based frontend for the HMH Multi-Curriculum Knowledge Base.

## Features

- **Role-Based Dashboards**: Customized views for teachers, authors, editors, and knowledge engineers
- **Knowledge Base Browser**: Browse and view 303 knowledge files with markdown rendering
- **Content Authoring**: Create and edit lessons, assessments, and activities
- **Review Workflow**: Submit and review content for approval
- **Search**: Full-text search across knowledge base and content
- **Responsive Design**: TailwindCSS for mobile-friendly UI

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **TanStack Query** - Server state management
- **Zustand** - Client state management
- **Axios** - HTTP client
- **TailwindCSS** - Styling
- **Headless UI** - Accessible components
- **React Markdown** - Markdown rendering

## Project Structure

```
frontend/
├── src/
│   ├── components/         # Reusable components
│   │   └── Layout.jsx     # Main layout with navigation
│   ├── pages/             # Page components
│   │   ├── Login.jsx      # Login page
│   │   ├── Dashboard.jsx  # Home dashboard
│   │   ├── KnowledgeBase.jsx  # Knowledge browser
│   │   ├── ContentList.jsx    # Content list/management
│   │   ├── ContentEditor.jsx  # Content create/edit
│   │   ├── ReviewQueue.jsx    # Review workflow
│   │   ├── ConfigManager.jsx  # Curriculum configs
│   │   └── Profile.jsx        # User profile
│   ├── services/          # API clients
│   │   └── api.js         # Backend API integration
│   ├── store/             # State management
│   │   └── authStore.js   # Authentication state
│   ├── App.jsx            # Main app with routing
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running on http://localhost:8000

### Installation

1. **Install dependencies:**

```bash
npm install
```

2. **Configure environment:**

Create `.env.local` file:

```env
VITE_API_URL=http://localhost:8000
```

3. **Start development server:**

```bash
npm run dev
```

4. **Access the app:**

Open http://localhost:3000

## Available Scripts

- **`npm run dev`** - Start development server with hot reload
- **`npm run build`** - Build for production
- **`npm run preview`** - Preview production build
- **`npm run lint`** - Run ESLint
- **`npm run format`** - Format code with Prettier

## User Roles

### Teacher
- Browse and view published content
- Search knowledge base
- View knowledge files

### Author
- All teacher permissions
- Create lessons, assessments, activities
- Submit content for review
- View own draft content

### Editor
- All author permissions
- Review and approve submitted content
- Publish approved content
- Access review queue

### Knowledge Engineer
- All editor permissions
- Manage curriculum configurations
- Add/edit knowledge base files
- Manage users (superuser)

## Key Components

### Layout Component

Main layout with navigation bar, user menu, and role-based navigation links.

**Location**: `src/components/Layout.jsx`

### Authentication

JWT-based authentication with automatic token refresh.

**Store**: `src/store/authStore.js`
**API**: `src/services/api.js`

**Features**:
- Login/logout
- Token storage in localStorage
- Automatic token refresh on 401
- Protected routes

### Knowledge Base Browser

Browse the hierarchical knowledge base with 303 markdown files.

**Location**: `src/pages/KnowledgeBase.jsx`

**Features**:
- Directory navigation with breadcrumbs
- File preview panel
- Markdown rendering with syntax highlighting
- Category/subject/state metadata display

### Dashboard

Role-specific home page with statistics and quick actions.

**Location**: `src/pages/Dashboard.jsx`

**Features**:
- Knowledge base statistics
- Recent content (for authors/editors)
- Quick action cards
- Category breakdown

### Content List

Browse and manage all content with advanced filtering.

**Location**: `src/pages/ContentList.jsx`

**Features**:
- Search by title or subject
- Filter by status, type, subject, grade level
- View content metadata
- Quick create button
- Status badges (draft, in_review, approved, published)

**Permissions**: Authors, Editors, Knowledge Engineers

### Content Editor

Create and edit lessons, assessments, and activities.

**Location**: `src/pages/ContentEditor.jsx`

**Features**:
- Create new content or edit existing
- Rich form with all metadata fields
- Learning objectives management
- Markdown content editor
- Submit for review workflow
- Save drafts
- Validation and error handling

**Permissions**: Authors, Editors, Knowledge Engineers

### Review Queue

Editorial review and approval workflow for editors.

**Location**: `src/pages/ReviewQueue.jsx`

**Features**:
- Pending review queue
- Content preview panel
- Review form with approve/needs-revision/reject options
- Rating system (1-5 stars)
- Comments and feedback
- Approve and publish action
- Real-time queue updates

**Permissions**: Editors, Knowledge Engineers only

### Config Manager

Manage curriculum configurations and knowledge resolution orders.

**Location**: `src/pages/ConfigManager.jsx`

**Features**:
- List all curriculum configs
- Create new configurations
- Edit existing configs
- Delete configs
- Define knowledge resolution order
- Configure grades, subjects, districts
- JSON export/import

**Permissions**: Knowledge Engineers only

### Profile

User profile and account settings.

**Location**: `src/pages/Profile.jsx`

**Features**:
- Update full name and email
- Change password
- View account role (read-only)
- Account activity stats
- Success notifications

**Permissions**: All authenticated users

## API Integration

All API calls go through `src/services/api.js` which provides:

- Automatic authentication headers
- Token refresh on expiry
- Error handling
- Request/response interceptors

### API Modules

```javascript
import {
  authAPI,       // Login, register, logout
  userAPI,       // User management
  knowledgeAPI,  // Knowledge base
  configAPI,     // Curriculum configs
  contentAPI,    // Content CRUD
  reviewAPI,     // Review workflow
  searchAPI      // Search
} from './services/api';
```

## State Management

### Auth Store (Zustand)

Global authentication state:

```javascript
const {
  user,              // Current user object
  isAuthenticated,   // Boolean
  login,            // Login function
  logout,           // Logout function
  checkAuth,        // Verify session
} = useAuthStore();
```

### Server State (TanStack Query)

Server data caching and synchronization:

```javascript
const { data, isLoading, error } = useQuery({
  queryKey: ['knowledge-stats'],
  queryFn: knowledgeAPI.getStats,
});
```

## Styling

### TailwindCSS

Utility-first CSS framework with custom configuration.

**Config**: `tailwind.config.js`

Custom classes:
- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button
- `.card` - Card container
- `.input` - Form input
- `.label` - Form label

### Responsive Design

Mobile-first responsive design with breakpoints:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

## Development

### Adding New Pages

1. Create page component in `src/pages/`
2. Add route to `src/App.jsx`
3. Add navigation link to `src/components/Layout.jsx` (if needed)

### Adding API Endpoints

1. Add API function to `src/services/api.js`
2. Use in components with TanStack Query:

```javascript
const { data } = useQuery({
  queryKey: ['my-data'],
  queryFn: myAPI.getData,
});
```

### Protected Routes

Wrap routes that require authentication:

```javascript
<Route
  path="/protected"
  element={
    <ProtectedRoute>
      <MyPage />
    </ProtectedRoute>
  }
/>
```

### Role-Based Access

Use `RoleRoute` component for role-specific pages:

```javascript
<Route
  path="/admin"
  element={
    <RoleRoute allowedRoles={['knowledge_engineer']}>
      <AdminPage />
    </RoleRoute>
  }
/>
```

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
```

Output directory: `dist/`

## Deployment

### Static Hosting (Netlify, Vercel, GitHub Pages)

1. Build the project: `npm run build`
2. Deploy the `dist/` directory
3. Configure environment variables:
   - `VITE_API_URL`: Production API URL

### With Backend (Same Server)

1. Build frontend: `npm run build`
2. Copy `dist/` contents to backend `static/` directory
3. Configure FastAPI to serve static files

## Environment Variables

Create `.env.local`:

```env
# Backend API URL
VITE_API_URL=http://localhost:8000

# Optional: Enable debug mode
VITE_DEBUG=true
```

## Troubleshooting

### CORS Errors

Ensure backend has proper CORS configuration in `.env`:

```env
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### API Connection Issues

1. Verify backend is running on port 8000
2. Check `VITE_API_URL` in `.env.local`
3. Look for errors in browser console

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

1. Follow existing code structure
2. Use TailwindCSS for styling
3. Write reusable components
4. Add PropTypes or TypeScript types
5. Test on multiple screen sizes

---

**Version:** 1.0.0
**Last Updated:** 2025-11-06
