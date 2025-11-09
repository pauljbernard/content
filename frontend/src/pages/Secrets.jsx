/**
 * Secrets Management Page
 * Secure storage for API keys and sensitive configuration
 */
import { useState, useEffect } from 'react';
import { PlusIcon, KeyIcon, TrashIcon, PencilIcon, EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import api from '../services/api';
import Layout from '../components/Layout';

export default function Secrets() {
  const [secrets, setSecrets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingSecret, setEditingSecret] = useState(null);
  const [formData, setFormData] = useState({
    secret_name: '',
    api_key: '',
    secret_value: '',
    description: '',
    category: 'API_KEY',
    environment: 'PRODUCTION',
    is_active: true,
  });

  useEffect(() => {
    fetchSecrets();
  }, []);

  const fetchSecrets = async () => {
    try {
      setLoading(true);
      const response = await api.get('/secrets');
      setSecrets(response.data);
    } catch (error) {
      console.error('Failed to fetch secrets:', error);
      alert('Failed to load secrets');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editingSecret) {
        await api.put(`/secrets/${editingSecret.id}`, formData);
      } else {
        await api.post('/secrets', formData);
      }

      setShowForm(false);
      setEditingSecret(null);
      setFormData({ secret_name: '', api_key: '', secret_value: '', description: '', category: 'API_KEY', environment: 'PRODUCTION', is_active: true });
      fetchSecrets();
    } catch (error) {
      console.error('Failed to save secret:', error);
      alert(`Failed to save secret: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleEdit = (secret) => {
    setEditingSecret(secret);
    setFormData({
      secret_name: secret.secret_name,
      api_key: '',  // Don't pre-fill encrypted fields
      secret_value: '',  // Don't pre-fill encrypted fields
      description: secret.description || '',
      category: secret.category || 'API_KEY',
      environment: secret.environment || 'PRODUCTION',
      is_active: secret.is_active,
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this secret?')) return;

    try {
      await api.delete(`/secrets/${id}`);
      fetchSecrets();
    } catch (error) {
      console.error('Failed to delete secret:', error);
      alert('Failed to delete secret');
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingSecret(null);
    setFormData({ secret_name: '', api_key: '', secret_value: '', description: '', category: 'API_KEY', environment: 'PRODUCTION', is_active: true });
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Secrets Management</h1>
            <p className="mt-1 text-sm text-gray-500">
              Securely store API keys and sensitive configuration values
            </p>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            <PlusIcon className="-ml-1 mr-2 h-5 w-5" />
            New Secret
          </button>
        </div>

      {showForm && (
        <div className="bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
              {editingSecret ? 'Edit Secret' : 'Create New Secret'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Secret Name
                </label>
                <input
                  type="text"
                  required
                  value={formData.secret_name}
                  onChange={(e) => setFormData({ ...formData, secret_name: e.target.value })}
                  placeholder="CASE API"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                <p className="mt-1 text-xs text-gray-500">Service or category name (e.g., "CASE API", "OpenAI")</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  API Key / Username
                </label>
                <input
                  type="password"
                  required={!editingSecret}
                  value={formData.api_key}
                  onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                  placeholder={editingSecret ? "Leave blank to keep current value" : "Enter API key or username"}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                <p className="mt-1 text-xs text-gray-500">Will be encrypted in database</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Secret Value / Password
                </label>
                <input
                  type="password"
                  required={!editingSecret}
                  value={formData.secret_value}
                  onChange={(e) => setFormData({ ...formData, secret_value: e.target.value })}
                  placeholder={editingSecret ? "Leave blank to keep current value" : "Enter secret value or password"}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                <p className="mt-1 text-xs text-gray-500">Will be encrypted in database</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={2}
                  placeholder="What this secret is used for"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Category
                </label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="API_KEY">API Key</option>
                  <option value="DATABASE">Database</option>
                  <option value="INTEGRATION">Integration</option>
                  <option value="CREDENTIALS">Credentials</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Environment
                </label>
                <select
                  value={formData.environment}
                  onChange={(e) => setFormData({ ...formData, environment: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="PRODUCTION">Production</option>
                  <option value="STAGING">Staging</option>
                  <option value="DEVELOPMENT">Development</option>
                  <option value="TEST">Test</option>
                </select>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <label className="ml-2 block text-sm text-gray-900">
                  Active
                </label>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  {editingSecret ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {secrets.length === 0 ? (
            <li className="px-6 py-12 text-center text-gray-500">
              <KeyIcon className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2">No secrets yet</p>
              <p className="text-sm">Create your first secret to get started</p>
            </li>
          ) : (
            secrets.map((secret) => (
              <li key={secret.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-3">
                      <KeyIcon className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {secret.secret_name}
                        </p>
                        {secret.description && (
                          <p className="text-sm text-gray-500 truncate">
                            {secret.description}
                          </p>
                        )}
                        <div className="mt-1 flex items-center flex-wrap gap-2 text-xs">
                          <span className="font-mono bg-gray-100 px-2 py-1 rounded text-gray-700">
                            Key: {secret.api_key_masked}
                          </span>
                          <span className="font-mono bg-gray-100 px-2 py-1 rounded text-gray-700">
                            Value: {secret.secret_value_masked}
                          </span>
                          {secret.category && (
                            <span className="px-2 py-1 rounded bg-blue-100 text-blue-800">
                              {secret.category}
                            </span>
                          )}
                          {secret.environment && (
                            <span className="px-2 py-1 rounded bg-purple-100 text-purple-800">
                              {secret.environment}
                            </span>
                          )}
                          {secret.is_active ? (
                            <span className="px-2 py-1 rounded bg-green-100 text-green-800">Active</span>
                          ) : (
                            <span className="px-2 py-1 rounded bg-gray-100 text-gray-800">Inactive</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleEdit(secret)}
                      className="p-2 text-indigo-600 hover:text-indigo-900"
                      title="Edit secret"
                    >
                      <PencilIcon className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(secret.id)}
                      className="p-2 text-red-600 hover:text-red-900"
                      title="Delete secret"
                    >
                      <TrashIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </li>
            ))
          )}
        </ul>
      </div>

      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-yellow-700">
              <strong className="font-medium">Security Note:</strong> Secrets are encrypted in the database and only accessible by system administrators. Never share secret values through unsecured channels.
            </p>
          </div>
        </div>
      </div>
      </div>
    </Layout>
  );
}
