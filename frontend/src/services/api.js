/**
 * API client for HMH CMS Backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

// Create axios instance
const apiClient = axios.create({
  baseURL: API_V1,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_V1}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await apiClient.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },

  register: async (userData) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  logout: async () => {
    await apiClient.post('/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

// User API
export const userAPI = {
  getCurrentUser: async () => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  updateCurrentUser: async (userData) => {
    const response = await apiClient.put('/users/me', userData);
    return response.data;
  },

  listUsers: async () => {
    const response = await apiClient.get('/users/');
    return response.data;
  },
};

// Knowledge Base API
export const knowledgeAPI = {
  getStats: async () => {
    const response = await apiClient.get('/knowledge/stats');
    return response.data;
  },

  browse: async (path = '') => {
    const response = await apiClient.get('/knowledge/browse', {
      params: { path },
    });
    return response.data;
  },

  getFile: async (path) => {
    const response = await apiClient.get('/knowledge/file', {
      params: { path },
    });
    return response.data;
  },

  getCategories: async () => {
    const response = await apiClient.get('/knowledge/categories');
    return response.data;
  },

  getSubjects: async () => {
    const response = await apiClient.get('/knowledge/subjects');
    return response.data;
  },

  getStates: async () => {
    const response = await apiClient.get('/knowledge/states');
    return response.data;
  },
};

// Curriculum Config API
export const configAPI = {
  list: async (filters = {}) => {
    const response = await apiClient.get('/curriculum-configs/', {
      params: filters,
    });
    return response.data;
  },

  get: async (configId) => {
    const response = await apiClient.get(`/curriculum-configs/${configId}`);
    return response.data;
  },

  create: async (configData) => {
    const response = await apiClient.post('/curriculum-configs/', configData);
    return response.data;
  },

  update: async (configId, configData) => {
    const response = await apiClient.put(
      `/curriculum-configs/${configId}`,
      configData
    );
    return response.data;
  },

  delete: async (configId) => {
    await apiClient.delete(`/curriculum-configs/${configId}`);
  },
};

// Content API
export const contentAPI = {
  list: async (filters = {}) => {
    const response = await apiClient.get('/content/', {
      params: filters,
    });
    return response.data;
  },

  get: async (contentId) => {
    const response = await apiClient.get(`/content/${contentId}`);
    return response.data;
  },

  create: async (contentData) => {
    const response = await apiClient.post('/content/', contentData);
    return response.data;
  },

  update: async (contentId, contentData) => {
    const response = await apiClient.put(`/content/${contentId}`, contentData);
    return response.data;
  },

  delete: async (contentId) => {
    await apiClient.delete(`/content/${contentId}`);
  },

  submit: async (contentId) => {
    const response = await apiClient.post(`/content/${contentId}/submit`);
    return response.data;
  },
};

// Review API
export const reviewAPI = {
  getPending: async () => {
    const response = await apiClient.get('/reviews/pending');
    return response.data;
  },

  create: async (reviewData) => {
    const response = await apiClient.post('/reviews/', reviewData);
    return response.data;
  },

  getForContent: async (contentId) => {
    const response = await apiClient.get(`/reviews/content/${contentId}`);
    return response.data;
  },

  approve: async (contentId) => {
    const response = await apiClient.post(
      `/reviews/content/${contentId}/approve`
    );
    return response.data;
  },

  getMyReviews: async () => {
    const response = await apiClient.get('/reviews/my-reviews');
    return response.data;
  },
};

// Search API
export const searchAPI = {
  search: async (query, filters = {}) => {
    const response = await apiClient.get('/search/', {
      params: { q: query, ...filters },
    });
    return response.data;
  },

  suggest: async (query) => {
    const response = await apiClient.get('/search/suggest', {
      params: { q: query },
    });
    return response.data;
  },
};

// Agent API
export const agentsAPI = {
  // List available agents
  list: async () => {
    const response = await apiClient.get('/agents/');
    return response.data;
  },

  // Invoke an agent
  invoke: async (agentType, taskDescription, parameters = {}) => {
    const response = await apiClient.post('/agents/invoke', {
      agent_type: agentType,
      task_description: taskDescription,
      parameters,
    });
    return response.data;
  },

  // List user's jobs
  listJobs: async (status = null, limit = 20) => {
    const response = await apiClient.get('/agents/jobs', {
      params: { status, limit },
    });
    return response.data;
  },

  // Get job status
  getJobStatus: async (jobId) => {
    const response = await apiClient.get(`/agents/jobs/${jobId}`);
    return response.data;
  },

  // Get job result
  getJobResult: async (jobId) => {
    const response = await apiClient.get(`/agents/jobs/${jobId}/result`);
    return response.data;
  },

  // Cancel a job
  cancelJob: async (jobId) => {
    const response = await apiClient.post(`/agents/jobs/${jobId}/cancel`);
    return response.data;
  },
};

// Standards API
export const standardsAPI = {
  // List all standards with filters
  list: async (params = {}) => {
    const response = await apiClient.get('/standards/', { params });
    return response.data;
  },

  // Get standard by ID
  getById: async (standardId) => {
    const response = await apiClient.get(`/standards/${standardId}`);
    return response.data;
  },

  // Create a new standard
  create: async (standardData) => {
    const response = await apiClient.post('/standards/', standardData);
    return response.data;
  },

  // Update an existing standard
  update: async (standardId, updateData) => {
    const response = await apiClient.patch(`/standards/${standardId}`, updateData);
    return response.data;
  },

  // Search within a standard
  search: async (standardId, query) => {
    const response = await apiClient.get(`/standards/${standardId}/search`, {
      params: { query },
    });
    return response.data;
  },

  // Create import job
  createImportJob: async (importData) => {
    const response = await apiClient.post('/standards/import', importData);
    return response.data;
  },

  // Get import job status
  getImportJob: async (jobId) => {
    const response = await apiClient.get(`/standards/import/${jobId}`);
    return response.data;
  },

  // Delete standard
  delete: async (standardId) => {
    const response = await apiClient.delete(`/standards/${standardId}`);
    return response.data;
  },

  // List import jobs
  listImportJobs: async (params = {}) => {
    const response = await apiClient.get('/standards/import', { params });
    return response.data;
  },
};

export default apiClient;
