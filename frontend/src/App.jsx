/**
 * Main App component with routing
 */
import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { ErrorBoundary } from 'react-error-boundary';
import useAuthStore from './store/authStore';
import ErrorFallback from './components/ErrorFallback';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Search from './pages/Search';
import KnowledgeBase from './pages/KnowledgeBase';
import ContentList from './pages/ContentList';
import ContentDetail from './pages/ContentDetail';
import ContentEditor from './pages/ContentEditor';
import ReviewQueue from './pages/ReviewQueue';
import ConfigManager from './pages/ConfigManager';
import Profile from './pages/Profile';
import Agents from './pages/Agents';
import AgentDetails from './pages/AgentDetails';
import AgentTask from './pages/AgentTask';
import Workflows from './pages/Workflows';
import WorkflowDetail from './pages/WorkflowDetail';
import WorkflowEditor from './pages/WorkflowEditor';
import Skills from './pages/Skills';

// Create QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Protected Route component
function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuthStore();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

// Role-based Route
function RoleRoute({ children, allowedRoles }) {
  const { user } = useAuthStore();

  if (!allowedRoles.includes(user?.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}

function App() {
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <QueryClientProvider client={queryClient}>
      <Toaster />
      <BrowserRouter>
        <ErrorBoundary
          FallbackComponent={ErrorFallback}
          onReset={() => window.location.href = '/'}
        >
          <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/search"
            element={
              <ProtectedRoute>
                <Search />
              </ProtectedRoute>
            }
          />

          <Route
            path="/knowledge"
            element={
              <ProtectedRoute>
                <KnowledgeBase />
              </ProtectedRoute>
            }
          />

          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />

          {/* Content Routes (Authors, Editors, Engineers) */}
          <Route
            path="/content"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <ContentList />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          <Route
            path="/content/new"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <ContentEditor />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          <Route
            path="/content/:id"
            element={
              <ProtectedRoute>
                <ContentDetail />
              </ProtectedRoute>
            }
          />

          <Route
            path="/content/:id/edit"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <ContentEditor />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          {/* Agents Routes (Authors+) */}
          <Route
            path="/agents"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <Agents />
                </RoleRoute>
              </ProtectedRoute>
            }
          />
          <Route
            path="/agents/:agentId/details"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <AgentDetails />
                </RoleRoute>
              </ProtectedRoute>
            }
          />
          <Route
            path="/agents/:agentId/task"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <AgentTask />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          {/* Workflows Routes (Authors+) */}
          <Route
            path="/workflows"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <Workflows />
                </RoleRoute>
              </ProtectedRoute>
            }
          />
          <Route
            path="/workflows/new"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <WorkflowEditor />
                </RoleRoute>
              </ProtectedRoute>
            }
          />
          <Route
            path="/workflows/:id"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <WorkflowDetail />
                </RoleRoute>
              </ProtectedRoute>
            }
          />
          <Route
            path="/workflows/:id/edit"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <WorkflowEditor />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          {/* Skills Routes (Authors+) */}
          <Route
            path="/skills"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <Skills />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          {/* Review Routes (Editors, Engineers) */}
          <Route
            path="/reviews"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['editor', 'knowledge_engineer']}>
                  <ReviewQueue />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          {/* Config Routes (Engineers only) */}
          <Route
            path="/configs"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={['knowledge_engineer']}>
                  <ConfigManager />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        </ErrorBoundary>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
