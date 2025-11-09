/**
 * API client for HMH CMS Backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

console.log('[API CONFIG] API_BASE_URL:', API_BASE_URL);
console.log('[API CONFIG] API_V1:', API_V1);

// Create axios instance
const apiClient = axios.create({
  baseURL: API_V1,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const fullUrl = config.baseURL + config.url;
    console.log('[INTERCEPTOR] Request:', config.method.toUpperCase(), fullUrl);
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('[INTERCEPTOR] Added auth token');
    }
    return config;
  },
  (error) => {
    console.error('[INTERCEPTOR] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => {
    console.log('[INTERCEPTOR] Response:', response.status, response.config.url);
    return response;
  },
  async (error) => {
    console.error('[INTERCEPTOR] Response error:', error.response?.status, error.config?.url);
    const originalRequest = error.config;

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      console.log('[INTERCEPTOR] 401 error, attempting token refresh...');
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          console.log('[INTERCEPTOR] Refreshing token...');
          const response = await axios.post(`${API_V1}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);
          console.log('[INTERCEPTOR] Token refreshed successfully');

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        console.error('[INTERCEPTOR] Token refresh failed:', refreshError);
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
    console.log('[API] login called with:', { email, password: '***' });
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    console.log('[API] formData created:', formData.toString());

    console.log('[API] Making POST request to /auth/login...');
    const response = await apiClient.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    console.log('[API] Got response:', response);
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

  // Get available CASE Network frameworks
  getCASENetworkFrameworks: async () => {
    const response = await apiClient.get('/standards/case-network/frameworks');
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

// Content Types API (Flexible CMS)
export const contentTypesAPI = {
  // Get content statistics
  getStats: async () => {
    const response = await apiClient.get('/content-types/stats');
    return response.data;
  },

  // List all content instances across all types
  listAllInstances: async (params = {}) => {
    const response = await apiClient.get('/content-types/instances/all', { params });
    // Return full paginated response {items, total, limit, offset, has_more}
    // For backwards compatibility, if it's an array, wrap it
    if (Array.isArray(response.data)) {
      return { items: response.data, total: response.data.length, limit: response.data.length, offset: 0, has_more: false };
    }
    return response.data;
  },

  // List all content types
  list: async (params = {}) => {
    const response = await apiClient.get('/content-types/', { params });
    // Return full paginated response {items, total, limit, offset, has_more}
    // For backwards compatibility, if it's an array, wrap it
    if (Array.isArray(response.data)) {
      return { items: response.data, total: response.data.length, limit: response.data.length, offset: 0, has_more: false };
    }
    return response.data;
  },

  // Get a specific content type
  get: async (contentTypeId) => {
    const response = await apiClient.get(`/content-types/${contentTypeId}`);
    return response.data;
  },

  // Create a new content type
  create: async (contentTypeData) => {
    const response = await apiClient.post('/content-types/', contentTypeData);
    return response.data;
  },

  // Update a content type
  update: async (contentTypeId, contentTypeData) => {
    const response = await apiClient.put(`/content-types/${contentTypeId}`, contentTypeData);
    return response.data;
  },

  // Delete a content type
  delete: async (contentTypeId) => {
    const response = await apiClient.delete(`/content-types/${contentTypeId}`);
    return response.data;
  },

  // List instances of a specific content type
  listInstances: async (contentTypeId, params = {}) => {
    const response = await apiClient.get(`/content-types/${contentTypeId}/instances`, { params });
    // Handle paginated response format {items, total, ...} or legacy array format
    return response.data.items || response.data;
  },

  // List instances in tree/hierarchical structure (for hierarchical content types)
  listInstancesTree: async (contentTypeId, params = {}) => {
    const response = await apiClient.get(`/content-types/${contentTypeId}/instances/tree`, { params });
    return response.data;
  },

  // Create an instance of a content type
  createInstance: async (contentTypeId, instanceData) => {
    const response = await apiClient.post(`/content-types/${contentTypeId}/instances`, instanceData);
    return response.data;
  },

  // Get a specific content instance
  getInstance: async (instanceId) => {
    const response = await apiClient.get(`/content-types/instances/${instanceId}`);
    return response.data;
  },

  // Update a content instance
  updateInstance: async (instanceId, instanceData) => {
    const response = await apiClient.put(`/content-types/instances/${instanceId}`, instanceData);
    return response.data;
  },

  // Delete a content instance
  deleteInstance: async (instanceId) => {
    const response = await apiClient.delete(`/content-types/instances/${instanceId}`);
    return response.data;
  },

  // Export content type as JSON
  exportContentType: async (contentTypeId) => {
    const response = await apiClient.get(`/content-types/${contentTypeId}/export`);
    return response.data;
  },

  // Import content type from JSON
  importContentType: async (importData) => {
    const response = await apiClient.post('/content-types/import', importData);
    return response.data;
  },

  // Export all instances of a content type
  exportInstances: async (contentTypeId, includeContentType = true) => {
    const response = await apiClient.get(
      `/content-types/${contentTypeId}/instances/export`,
      { params: { include_content_type: includeContentType } }
    );
    return response.data;
  },

  // Import instances from JSON
  importInstances: async (contentTypeId, importData) => {
    const response = await apiClient.post(
      `/content-types/${contentTypeId}/instances/import`,
      importData
    );
    return response.data;
  },

  // Generate field value using AI agent (non-streaming)
  generateField: async (instanceId, fieldName, agentConfigId = null) => {
    const params = { field_name: fieldName, stream: false };
    if (agentConfigId) {
      params.agent_config_id = agentConfigId;
    }

    const response = await apiClient.post(
      `/content-types/instances/${instanceId}/generate-field`,
      null,
      { params }
    );
    return response.data;
  },

  // Generate field value with streaming (Server-Sent Events)
  generateFieldStream: async (instanceId, fieldName, agentConfigId = null, callbacks = {}) => {
    const params = new URLSearchParams({ field_name: fieldName, stream: true });
    if (agentConfigId) {
      params.append('agent_config_id', agentConfigId);
    }

    const token = localStorage.getItem('access_token');
    const url = `${API_V1}/content-types/instances/${instanceId}/generate-field?${params}`;

    console.log('[STREAM] Starting SSE connection to:', url);

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'text/event-stream',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              console.log('[STREAM] Received:', data.type || 'unknown', data);

              if (data.error) {
                // Handle error in data
                console.error('[STREAM] Error in data:', data.error);
                if (callbacks.onError) {
                  callbacks.onError(data.error);
                }
              } else if (data.type === 'start' && callbacks.onStart) {
                callbacks.onStart(data);
              } else if (data.type === 'info' && callbacks.onInfo) {
                callbacks.onInfo(data.message);
              } else if (data.type === 'content' && callbacks.onContent) {
                callbacks.onContent(data.text);
              } else if (data.type === 'done' && callbacks.onDone) {
                callbacks.onDone(data);
              } else if (data.type === 'error' && callbacks.onError) {
                callbacks.onError(data.error);
              }
            } catch (parseError) {
              console.error('[STREAM] Failed to parse line:', line, parseError);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  },

  // Get available agents for a content instance
  getAvailableAgents: async (instanceId, fieldName = null) => {
    const params = fieldName ? { field_name: fieldName } : {};
    const response = await apiClient.get(
      `/content-types/instances/${instanceId}/available-agents`,
      { params }
    );
    return response.data;
  },
};

// Migrations API
export const migrationsAPI = {
  // Setup legacy content type
  setupLegacyContentType: async () => {
    const response = await apiClient.post('/migrations/setup-legacy-content-type');
    return response.data;
  },

  // Migrate legacy content
  migrateLegacyContent: async (limit = 10, offset = 0) => {
    const response = await apiClient.post('/migrations/migrate-legacy-content', null, {
      params: { limit, offset },
    });
    return response.data;
  },

  // Get migration status
  getMigrationStatus: async () => {
    const response = await apiClient.get('/migrations/migration-status');
    return response.data;
  },
};

// Database Configuration API
export const databaseAPI = {
  // List all database configurations
  listConfigs: async () => {
    const response = await apiClient.get('/database-configs');
    return response.data;
  },

  // Get database configuration by ID
  getConfig: async (configId) => {
    const response = await apiClient.get(`/database-configs/${configId}`);
    return response.data;
  },

  // Create database configuration
  createConfig: async (configData) => {
    const response = await apiClient.post('/database-configs', configData);
    return response.data;
  },

  // Update database configuration
  updateConfig: async (configId, configData) => {
    const response = await apiClient.put(`/database-configs/${configId}`, configData);
    return response.data;
  },

  // Delete database configuration
  deleteConfig: async (configId) => {
    const response = await apiClient.delete(`/database-configs/${configId}`);
    return response.data;
  },

  // Test database connection
  testConnection: async (configId) => {
    const response = await apiClient.post(`/database-configs/${configId}/test`);
    return response.data;
  },

  // Initialize database schema
  initializeSchema: async (configId, enablePgvector = true) => {
    const response = await apiClient.post(
      `/database-configs/${configId}/initialize`,
      null,
      { params: { enable_pgvector: enablePgvector } }
    );
    return response.data;
  },

  // Activate database configuration
  activateConfig: async (configId) => {
    const response = await apiClient.post(`/database-configs/${configId}/activate`);
    return response.data;
  },

  // Get database statistics
  getStatistics: async (configId) => {
    const response = await apiClient.get(`/database-configs/${configId}/statistics`);
    return response.data;
  },

  // List migration jobs
  listMigrations: async () => {
    const response = await apiClient.get('/migrations');
    return response.data;
  },

  // Get migration job by ID
  getMigration: async (jobId) => {
    const response = await apiClient.get(`/migrations/${jobId}`);
    return response.data;
  },

  // Start migration
  startMigration: async (migrationData) => {
    const response = await apiClient.post('/migrations', migrationData);
    return response.data;
  },

  // Generate vector embeddings
  generateEmbeddings: async () => {
    const response = await apiClient.post('/vector-search/generate-embeddings');
    return response.data;
  },

  // Vector semantic search
  vectorSearch: async (query, contentTypeIds = null, limit = 5) => {
    const response = await apiClient.post('/vector-search/search', null, {
      params: {
        query,
        content_type_ids: contentTypeIds,
        limit,
      },
    });
    return response.data;
  },
};

// LLM Configuration API
export const llmAPI = {
  // Provider management
  listProviders: async () => {
    const response = await apiClient.get('/llm-providers');
    return response.data;
  },

  getProvider: async (providerId) => {
    const response = await apiClient.get(`/llm-providers/${providerId}`);
    return response.data;
  },

  createProvider: async (providerData) => {
    const response = await apiClient.post('/llm-providers', providerData);
    return response.data;
  },

  updateProvider: async (providerId, providerData) => {
    const response = await apiClient.put(`/llm-providers/${providerId}`, providerData);
    return response.data;
  },

  deleteProvider: async (providerId) => {
    const response = await apiClient.delete(`/llm-providers/${providerId}`);
    return response.data;
  },

  testProvider: async (providerId) => {
    const response = await apiClient.post(`/llm-providers/${providerId}/test`);
    return response.data;
  },

  // Model management
  listModels: async (params = {}) => {
    const response = await apiClient.get('/llm-models', { params });
    return response.data;
  },

  getModel: async (modelId) => {
    const response = await apiClient.get(`/llm-models/${modelId}`);
    return response.data;
  },

  createModel: async (modelData) => {
    const response = await apiClient.post('/llm-models', modelData);
    return response.data;
  },

  updateModel: async (modelId, modelData) => {
    const response = await apiClient.put(`/llm-models/${modelId}`, modelData);
    return response.data;
  },

  deleteModel: async (modelId) => {
    const response = await apiClient.delete(`/llm-models/${modelId}`);
    return response.data;
  },

  // Defaults
  getDefaults: async () => {
    const response = await apiClient.get('/llm-defaults');
    return response.data;
  },
};

export default apiClient;
