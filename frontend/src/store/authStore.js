/**
 * Authentication store using Zustand
 */
import { create } from 'zustand';
import { authAPI, userAPI } from '../services/api';

const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  // Login
  login: async (email, password) => {
    try {
      console.log('[AUTH] Starting login...');
      set({ isLoading: true, error: null });

      console.log('[AUTH] Calling authAPI.login...');
      const tokens = await authAPI.login(email, password);
      console.log('[AUTH] Login successful, got tokens:', {
        hasAccessToken: !!tokens.access_token,
        hasRefreshToken: !!tokens.refresh_token
      });

      localStorage.setItem('access_token', tokens.access_token);
      localStorage.setItem('refresh_token', tokens.refresh_token);
      console.log('[AUTH] Tokens saved to localStorage');

      console.log('[AUTH] Fetching current user...');
      const user = await userAPI.getCurrentUser();
      console.log('[AUTH] Got user:', user);

      set({ user, isAuthenticated: true, isLoading: false });
      console.log('[AUTH] Login complete, state updated');

      return true;
    } catch (error) {
      console.error('[AUTH] Login error:', error);
      set({
        error: error.response?.data?.detail || 'Login failed',
        isLoading: false,
      });
      return false;
    }
  },

  // Register
  register: async (userData) => {
    try {
      set({ isLoading: true, error: null });
      await authAPI.register(userData);

      // Auto-login after registration
      return await get().login(userData.email, userData.password);
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Registration failed',
        isLoading: false,
      });
      return false;
    }
  },

  // Logout
  logout: async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({ user: null, isAuthenticated: false });
    }
  },

  // Check authentication status
  checkAuth: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ isLoading: false, isAuthenticated: false });
      return;
    }

    try {
      const user = await userAPI.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({ isAuthenticated: false, isLoading: false });
    }
  },

  // Update user profile
  updateUser: async (userData) => {
    try {
      const updatedUser = await userAPI.updateCurrentUser(userData);
      set({ user: updatedUser });
      return true;
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Update failed' });
      return false;
    }
  },

  // Clear error
  clearError: () => set({ error: null }),
}));

export default useAuthStore;
