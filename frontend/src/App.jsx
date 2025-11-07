/**
 * Main App component with routing
 */
import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import useAuthStore from './store/authStore';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import KnowledgeBase from './pages/KnowledgeBase';
import ContentList from './pages/ContentList';
import ContentEditor from './pages/ContentEditor';
import ReviewQueue from './pages/ReviewQueue';
import ConfigManager from './pages/ConfigManager';
import Profile from './pages/Profile';

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
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />

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
                <RoleRoute allowedRoles={['author', 'editor', 'knowledge_engineer']}>
                  <ContentEditor />
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
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
