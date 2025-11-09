/**
 * LLM Configuration Settings Page
 *
 * Manage LLM providers (OpenAI, Anthropic, etc.) and their models.
 * Configure API keys, set default models, and test connections.
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  PlusIcon,
  CheckCircleIcon,
  XCircleIcon,
  SparklesIcon,
  Cog6ToothIcon,
  TrashIcon,
  PencilIcon,
  KeyIcon,
  ServerIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { llmAPI } from '../services/api';

export default function LLMSettings() {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState('providers'); // 'providers', 'models', 'defaults'
  const [showProviderForm, setShowProviderForm] = useState(false);
  const [showModelForm, setShowModelForm] = useState(false);
  const [editingProvider, setEditingProvider] = useState(null);
  const [editingModel, setEditingModel] = useState(null);

  // Fetch data
  const { data: providers = [], isLoading: providersLoading } = useQuery({
    queryKey: ['llm-providers'],
    queryFn: llmAPI.listProviders,
  });

  const { data: models = [], isLoading: modelsLoading } = useQuery({
    queryKey: ['llm-models'],
    queryFn: llmAPI.listModels,
  });

  const { data: defaults = {}, isLoading: defaultsLoading } = useQuery({
    queryKey: ['llm-defaults'],
    queryFn: llmAPI.getDefaults,
  });

  // Provider form
  const [providerForm, setProviderForm] = useState({
    name: '',
    display_name: '',
    description: '',
    provider_type: 'openai',
    api_key: '',
    api_base_url: '',
    organization_id: '',
    api_version: '',
    supports_chat: true,
    supports_embeddings: false,
    supports_function_calling: false,
    supports_streaming: false,
    requests_per_minute: null,
    tokens_per_minute: null,
  });

  // Model form
  const [modelForm, setModelForm] = useState({
    provider_id: '',
    model_id: '',
    display_name: '',
    description: '',
    model_type: 'chat',
    context_window: null,
    max_output_tokens: null,
    supports_vision: false,
    supports_json_mode: false,
    supports_tools: false,
    default_temperature: 0.7,
    default_top_p: 1.0,
    default_max_tokens: null,
    input_cost_per_1m: null,
    output_cost_per_1m: null,
    is_default_for_chat: false,
    is_default_for_embeddings: false,
    is_default_for_agents: false,
    custom_params: null,
  });

  // Mutations
  const createProviderMutation = useMutation({
    mutationFn: llmAPI.createProvider,
    onSuccess: () => {
      queryClient.invalidateQueries(['llm-providers']);
      setShowProviderForm(false);
      resetProviderForm();
    },
  });

  const updateProviderMutation = useMutation({
    mutationFn: ({ id, data }) => llmAPI.updateProvider(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['llm-providers']);
      setEditingProvider(null);
      setShowProviderForm(false);
      resetProviderForm();
    },
  });

  const deleteProviderMutation = useMutation({
    mutationFn: llmAPI.deleteProvider,
    onSuccess: () => {
      queryClient.invalidateQueries(['llm-providers']);
      queryClient.invalidateQueries(['llm-models']);
    },
  });

  const testProviderMutation = useMutation({
    mutationFn: llmAPI.testProvider,
  });

  const createModelMutation = useMutation({
    mutationFn: llmAPI.createModel,
    onSuccess: () => {
      queryClient.invalidateQueries(['llm-models']);
      queryClient.invalidateQueries(['llm-defaults']);
      setShowModelForm(false);
      resetModelForm();
    },
  });

  const updateModelMutation = useMutation({
    mutationFn: ({ id, data }) => llmAPI.updateModel(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['llm-models']);
      queryClient.invalidateQueries(['llm-defaults']);
      setEditingModel(null);
      setShowModelForm(false);
      resetModelForm();
    },
  });

  const deleteModelMutation = useMutation({
    mutationFn: llmAPI.deleteModel,
    onSuccess: () => {
      queryClient.invalidateQueries(['llm-models']);
      queryClient.invalidateQueries(['llm-defaults']);
    },
  });

  // Reset forms
  const resetProviderForm = () => {
    setProviderForm({
      name: '',
      display_name: '',
      description: '',
      provider_type: 'openai',
      api_key: '',
      api_base_url: '',
      organization_id: '',
      api_version: '',
      supports_chat: true,
      supports_embeddings: false,
      supports_function_calling: false,
      supports_streaming: false,
      requests_per_minute: null,
      tokens_per_minute: null,
    });
  };

  const resetModelForm = () => {
    setModelForm({
      provider_id: '',
      model_id: '',
      display_name: '',
      description: '',
      model_type: 'chat',
      context_window: null,
      max_output_tokens: null,
      supports_vision: false,
      supports_json_mode: false,
      supports_tools: false,
      default_temperature: 0.7,
      default_top_p: 1.0,
      default_max_tokens: null,
      input_cost_per_1m: null,
      output_cost_per_1m: null,
      is_default_for_chat: false,
      is_default_for_embeddings: false,
      is_default_for_agents: false,
      custom_params: null,
    });
  };

  // Edit handlers
  const handleEditProvider = (provider) => {
    setEditingProvider(provider);
    setProviderForm({
      ...provider,
      api_key: '', // Don't populate API key for security
    });
    setShowProviderForm(true);
  };

  const handleEditModel = (model) => {
    setEditingModel(model);
    setModelForm(model);
    setShowModelForm(true);
  };

  // Submit handlers
  const handleProviderSubmit = (e) => {
    e.preventDefault();

    if (editingProvider) {
      updateProviderMutation.mutate({
        id: editingProvider.id,
        data: providerForm,
      });
    } else {
      createProviderMutation.mutate(providerForm);
    }
  };

  const handleModelSubmit = (e) => {
    e.preventDefault();

    if (editingModel) {
      updateModelMutation.mutate({
        id: editingModel.id,
        data: modelForm,
      });
    } else {
      createModelMutation.mutate(modelForm);
    }
  };

  // Loading state
  if (providersLoading && modelsLoading && defaultsLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading LLM configuration...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <SparklesIcon className="h-8 w-8 text-primary-600 mr-3" />
            LLM Configuration
          </h1>
          <p className="mt-2 text-gray-600">
            Manage AI providers, models, and API keys for Claude Code integration and vector embeddings
          </p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('providers')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'providers'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <ServerIcon className="h-5 w-5 inline mr-2" />
              Providers
            </button>
            <button
              onClick={() => setActiveTab('models')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'models'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Cog6ToothIcon className="h-5 w-5 inline mr-2" />
              Models
            </button>
            <button
              onClick={() => setActiveTab('defaults')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'defaults'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <CheckCircleIcon className="h-5 w-5 inline mr-2" />
              Defaults
            </button>
          </nav>
        </div>

        {/* Providers Tab */}
        {activeTab === 'providers' && (
          <div>
            {/* Add Provider Button */}
            <div className="mb-6 flex justify-end">
              <button
                onClick={() => {
                  resetProviderForm();
                  setEditingProvider(null);
                  setShowProviderForm(true);
                }}
                className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Add Provider
              </button>
            </div>

            {/* Provider Form Modal */}
            {showProviderForm && (
              <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-500 bg-opacity-75 flex items-center justify-center">
                <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                  <div className="p-6">
                    <h2 className="text-2xl font-bold mb-6">
                      {editingProvider ? 'Edit Provider' : 'Add LLM Provider'}
                    </h2>

                    <form onSubmit={handleProviderSubmit} className="space-y-4">
                      {/* Basic Info */}
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Name *
                          </label>
                          <input
                            type="text"
                            required
                            value={providerForm.name}
                            onChange={(e) => setProviderForm({ ...providerForm, name: e.target.value })}
                            className="w-full px-3 py-2 border rounded-lg"
                            placeholder="openai"
                            disabled={!!editingProvider}
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Display Name *
                          </label>
                          <input
                            type="text"
                            required
                            value={providerForm.display_name}
                            onChange={(e) => setProviderForm({ ...providerForm, display_name: e.target.value })}
                            className="w-full px-3 py-2 border rounded-lg"
                            placeholder="OpenAI"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Description
                        </label>
                        <textarea
                          value={providerForm.description}
                          onChange={(e) => setProviderForm({ ...providerForm, description: e.target.value })}
                          className="w-full px-3 py-2 border rounded-lg"
                          rows="2"
                          placeholder="Official OpenAI API"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Provider Type *
                        </label>
                        <select
                          required
                          value={providerForm.provider_type}
                          onChange={(e) => setProviderForm({ ...providerForm, provider_type: e.target.value })}
                          className="w-full px-3 py-2 border rounded-lg"
                          disabled={!!editingProvider}
                        >
                          <option value="openai">OpenAI</option>
                          <option value="anthropic">Anthropic</option>
                          <option value="azure">Azure OpenAI</option>
                          <option value="cohere">Cohere</option>
                          <option value="huggingface">HuggingFace</option>
                          <option value="local">Local Model</option>
                        </select>
                      </div>

                      {/* API Configuration */}
                      <div className="border-t pt-4">
                        <h3 className="font-semibold text-lg mb-3">API Configuration</h3>

                        <div className="space-y-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              API Key
                            </label>
                            <input
                              type="password"
                              value={providerForm.api_key}
                              onChange={(e) => setProviderForm({ ...providerForm, api_key: e.target.value })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="sk-..."
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              API Base URL (optional)
                            </label>
                            <input
                              type="url"
                              value={providerForm.api_base_url}
                              onChange={(e) => setProviderForm({ ...providerForm, api_base_url: e.target.value })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="https://api.openai.com/v1"
                            />
                          </div>

                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">
                                Organization ID (optional)
                              </label>
                              <input
                                type="text"
                                value={providerForm.organization_id}
                                onChange={(e) => setProviderForm({ ...providerForm, organization_id: e.target.value })}
                                className="w-full px-3 py-2 border rounded-lg"
                                placeholder="org-..."
                              />
                            </div>

                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">
                                API Version (Azure only)
                              </label>
                              <input
                                type="text"
                                value={providerForm.api_version}
                                onChange={(e) => setProviderForm({ ...providerForm, api_version: e.target.value })}
                                className="w-full px-3 py-2 border rounded-lg"
                                placeholder="2023-05-15"
                              />
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Capabilities */}
                      <div className="border-t pt-4">
                        <h3 className="font-semibold text-lg mb-3">Capabilities</h3>

                        <div className="grid grid-cols-2 gap-3">
                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={providerForm.supports_chat}
                              onChange={(e) => setProviderForm({ ...providerForm, supports_chat: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Supports Chat</span>
                          </label>

                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={providerForm.supports_embeddings}
                              onChange={(e) => setProviderForm({ ...providerForm, supports_embeddings: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Supports Embeddings</span>
                          </label>

                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={providerForm.supports_function_calling}
                              onChange={(e) => setProviderForm({ ...providerForm, supports_function_calling: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Supports Function Calling</span>
                          </label>

                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={providerForm.supports_streaming}
                              onChange={(e) => setProviderForm({ ...providerForm, supports_streaming: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Supports Streaming</span>
                          </label>
                        </div>
                      </div>

                      {/* Rate Limiting */}
                      <div className="border-t pt-4">
                        <h3 className="font-semibold text-lg mb-3">Rate Limiting (optional)</h3>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Requests per Minute
                            </label>
                            <input
                              type="number"
                              value={providerForm.requests_per_minute || ''}
                              onChange={(e) => setProviderForm({ ...providerForm, requests_per_minute: e.target.value ? parseInt(e.target.value) : null })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="500"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Tokens per Minute
                            </label>
                            <input
                              type="number"
                              value={providerForm.tokens_per_minute || ''}
                              onChange={(e) => setProviderForm({ ...providerForm, tokens_per_minute: e.target.value ? parseInt(e.target.value) : null })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="100000"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Form Actions */}
                      <div className="flex justify-end space-x-3 pt-4 border-t">
                        <button
                          type="button"
                          onClick={() => {
                            setShowProviderForm(false);
                            setEditingProvider(null);
                            resetProviderForm();
                          }}
                          className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                        >
                          Cancel
                        </button>
                        <button
                          type="submit"
                          disabled={createProviderMutation.isPending || updateProviderMutation.isPending}
                          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                        >
                          {editingProvider ? 'Update Provider' : 'Create Provider'}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            )}

            {/* Providers List */}
            <div className="space-y-4">
              {providers.length === 0 ? (
                <div className="text-center py-12 bg-gray-50 rounded-lg">
                  <ServerIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No LLM providers configured</p>
                  <button
                    onClick={() => setShowProviderForm(true)}
                    className="mt-4 text-primary-600 hover:text-primary-700"
                  >
                    Add your first provider
                  </button>
                </div>
              ) : (
                providers.map((provider) => (
                  <div
                    key={provider.id}
                    className="bg-white border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {provider.display_name}
                          </h3>
                          {provider.is_default && (
                            <span className="ml-2 px-2 py-1 bg-green-100 text-green-700 text-xs rounded">
                              Default
                            </span>
                          )}
                          {provider.is_active ? (
                            <CheckCircleIcon className="ml-2 h-5 w-5 text-green-500" />
                          ) : (
                            <XCircleIcon className="ml-2 h-5 w-5 text-gray-400" />
                          )}
                        </div>

                        <div className="mt-1 flex items-center text-sm text-gray-500">
                          <span className="font-mono bg-gray-100 px-2 py-1 rounded">
                            {provider.name}
                          </span>
                          <span className="mx-2">•</span>
                          <span className="capitalize">{provider.provider_type}</span>
                        </div>

                        {provider.description && (
                          <p className="mt-2 text-sm text-gray-600">{provider.description}</p>
                        )}

                        <div className="mt-4 flex flex-wrap gap-2">
                          {provider.api_key_configured && (
                            <span className="inline-flex items-center px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
                              <KeyIcon className="h-3 w-3 mr-1" />
                              API Key: {provider.api_key_masked}
                            </span>
                          )}

                          {provider.supports_chat && (
                            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                              Chat
                            </span>
                          )}

                          {provider.supports_embeddings && (
                            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                              Embeddings
                            </span>
                          )}

                          {provider.supports_function_calling && (
                            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                              Functions
                            </span>
                          )}

                          {provider.supports_streaming && (
                            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                              Streaming
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => testProviderMutation.mutate(provider.id)}
                          disabled={testProviderMutation.isPending}
                          className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                          title="Test Connection"
                        >
                          <CheckCircleIcon className="h-5 w-5" />
                        </button>

                        <button
                          onClick={() => handleEditProvider(provider)}
                          className="p-2 text-gray-600 hover:bg-gray-50 rounded-lg"
                          title="Edit"
                        >
                          <PencilIcon className="h-5 w-5" />
                        </button>

                        <button
                          onClick={() => {
                            if (confirm(`Delete provider "${provider.display_name}"?`)) {
                              deleteProviderMutation.mutate(provider.id);
                            }
                          }}
                          disabled={deleteProviderMutation.isPending}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                          title="Delete"
                        >
                          <TrashIcon className="h-5 w-5" />
                        </button>
                      </div>
                    </div>

                    {provider.last_error && (
                      <div className="mt-4 p-3 bg-red-50 text-red-700 text-sm rounded">
                        Error: {provider.last_error}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* Models Tab */}
        {activeTab === 'models' && (
          <div>
            {/* Add Model Button */}
            <div className="mb-6 flex justify-end">
              <button
                onClick={() => {
                  resetModelForm();
                  setEditingModel(null);
                  setShowModelForm(true);
                }}
                className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Add Model
              </button>
            </div>

            {/* Model Form Modal */}
            {showModelForm && (
              <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-500 bg-opacity-75 flex items-center justify-center">
                <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                  <div className="p-6">
                    <h2 className="text-2xl font-bold mb-6">
                      {editingModel ? 'Edit Model' : 'Add LLM Model'}
                    </h2>

                    <form onSubmit={handleModelSubmit} className="space-y-4">
                      {/* Basic Info */}
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Provider *
                          </label>
                          <select
                            required
                            value={modelForm.provider_id}
                            onChange={(e) => setModelForm({ ...modelForm, provider_id: e.target.value })}
                            className="w-full px-3 py-2 border rounded-lg"
                            disabled={!!editingModel}
                          >
                            <option value="">Select provider...</option>
                            {providers.map((p) => (
                              <option key={p.id} value={p.id}>
                                {p.display_name}
                              </option>
                            ))}
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Model Type *
                          </label>
                          <select
                            required
                            value={modelForm.model_type}
                            onChange={(e) => setModelForm({ ...modelForm, model_type: e.target.value })}
                            className="w-full px-3 py-2 border rounded-lg"
                          >
                            <option value="chat">Chat</option>
                            <option value="embedding">Embedding</option>
                            <option value="completion">Completion</option>
                          </select>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Model ID *
                          </label>
                          <input
                            type="text"
                            required
                            value={modelForm.model_id}
                            onChange={(e) => setModelForm({ ...modelForm, model_id: e.target.value })}
                            className="w-full px-3 py-2 border rounded-lg"
                            placeholder="gpt-4-turbo-preview"
                            disabled={!!editingModel}
                          />
                          <p className="text-xs text-gray-500 mt-1">API identifier (e.g., gpt-4-turbo-preview, claude-3-opus-20240229)</p>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Display Name *
                          </label>
                          <input
                            type="text"
                            required
                            value={modelForm.display_name}
                            onChange={(e) => setModelForm({ ...modelForm, display_name: e.target.value })}
                            className="w-full px-3 py-2 border rounded-lg"
                            placeholder="GPT-4 Turbo"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Description
                        </label>
                        <textarea
                          value={modelForm.description}
                          onChange={(e) => setModelForm({ ...modelForm, description: e.target.value })}
                          className="w-full px-3 py-2 border rounded-lg"
                          rows="2"
                          placeholder="Model description..."
                        />
                      </div>

                      {/* Capabilities */}
                      <div className="border-t pt-4">
                        <h3 className="font-semibold text-lg mb-3">Model Specifications</h3>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Context Window (tokens)
                            </label>
                            <input
                              type="number"
                              value={modelForm.context_window || ''}
                              onChange={(e) => setModelForm({ ...modelForm, context_window: e.target.value ? parseInt(e.target.value) : null })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="128000"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Max Output Tokens
                            </label>
                            <input
                              type="number"
                              value={modelForm.max_output_tokens || ''}
                              onChange={(e) => setModelForm({ ...modelForm, max_output_tokens: e.target.value ? parseInt(e.target.value) : null })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="4096"
                            />
                          </div>
                        </div>

                        <div className="grid grid-cols-3 gap-3 mt-3">
                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={modelForm.supports_vision}
                              onChange={(e) => setModelForm({ ...modelForm, supports_vision: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Vision</span>
                          </label>

                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={modelForm.supports_json_mode}
                              onChange={(e) => setModelForm({ ...modelForm, supports_json_mode: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">JSON Mode</span>
                          </label>

                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={modelForm.supports_tools}
                              onChange={(e) => setModelForm({ ...modelForm, supports_tools: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Tools/Functions</span>
                          </label>
                        </div>
                      </div>

                      {/* Default Parameters */}
                      <div className="border-t pt-4">
                        <h3 className="font-semibold text-lg mb-3">Default Parameters</h3>

                        <div className="grid grid-cols-3 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Temperature
                            </label>
                            <input
                              type="number"
                              step="0.1"
                              min="0"
                              max="2"
                              value={modelForm.default_temperature}
                              onChange={(e) => setModelForm({ ...modelForm, default_temperature: parseFloat(e.target.value) })}
                              className="w-full px-3 py-2 border rounded-lg"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Top P
                            </label>
                            <input
                              type="number"
                              step="0.1"
                              min="0"
                              max="1"
                              value={modelForm.default_top_p}
                              onChange={(e) => setModelForm({ ...modelForm, default_top_p: parseFloat(e.target.value) })}
                              className="w-full px-3 py-2 border rounded-lg"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Max Tokens (default)
                            </label>
                            <input
                              type="number"
                              value={modelForm.default_max_tokens || ''}
                              onChange={(e) => setModelForm({ ...modelForm, default_max_tokens: e.target.value ? parseInt(e.target.value) : null })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="Leave empty for model default"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Pricing */}
                      <div className="border-t pt-4">
                        <h3 className="font-semibold text-lg mb-3">Pricing (USD per 1M tokens)</h3>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Input Cost
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              value={modelForm.input_cost_per_1m || ''}
                              onChange={(e) => setModelForm({ ...modelForm, input_cost_per_1m: e.target.value ? parseFloat(e.target.value) : null })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="10.00"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Output Cost
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              value={modelForm.output_cost_per_1m || ''}
                              onChange={(e) => setModelForm({ ...modelForm, output_cost_per_1m: e.target.value ? parseFloat(e.target.value) : null })}
                              className="w-full px-3 py-2 border rounded-lg"
                              placeholder="30.00"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Default Settings */}
                      <div className="border-t pt-4">
                        <h3 className="font-semibold text-lg mb-3">Default Settings</h3>

                        <div className="space-y-2">
                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={modelForm.is_default_for_chat}
                              onChange={(e) => setModelForm({ ...modelForm, is_default_for_chat: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Set as default for Chat</span>
                          </label>

                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={modelForm.is_default_for_embeddings}
                              onChange={(e) => setModelForm({ ...modelForm, is_default_for_embeddings: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Set as default for Embeddings</span>
                          </label>

                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={modelForm.is_default_for_agents}
                              onChange={(e) => setModelForm({ ...modelForm, is_default_for_agents: e.target.checked })}
                              className="mr-2"
                            />
                            <span className="text-sm">Set as default for AI Agents</span>
                          </label>
                        </div>
                      </div>

                      {/* Form Actions */}
                      <div className="flex justify-end space-x-3 pt-4 border-t">
                        <button
                          type="button"
                          onClick={() => {
                            setShowModelForm(false);
                            setEditingModel(null);
                            resetModelForm();
                          }}
                          className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                        >
                          Cancel
                        </button>
                        <button
                          type="submit"
                          disabled={createModelMutation.isPending || updateModelMutation.isPending}
                          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                        >
                          {editingModel ? 'Update Model' : 'Create Model'}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            )}

            {/* Models List */}
            <div className="space-y-4">
              {models.length === 0 ? (
                <div className="text-center py-12 bg-gray-50 rounded-lg">
                  <Cog6ToothIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No models configured</p>
                  <button
                    onClick={() => setShowModelForm(true)}
                    className="mt-4 text-primary-600 hover:text-primary-700"
                  >
                    Add your first model
                  </button>
                </div>
              ) : (
                <>
                  {/* Group models by provider */}
                  {providers.map((provider) => {
                    const providerModels = models.filter((m) => m.provider_id === provider.id);
                    if (providerModels.length === 0) return null;

                    return (
                      <div key={provider.id} className="bg-white border rounded-lg p-6 shadow-sm">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">
                          {provider.display_name} Models
                        </h3>

                        <div className="space-y-3">
                          {providerModels.map((model) => (
                            <div
                              key={model.id}
                              className="border rounded-lg p-4 hover:bg-gray-50"
                            >
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <div className="flex items-center">
                                    <h4 className="font-semibold text-gray-900">
                                      {model.display_name}
                                    </h4>
                                    <span className={`ml-2 px-2 py-1 text-xs rounded ${
                                      model.model_type === 'chat'
                                        ? 'bg-blue-100 text-blue-700'
                                        : model.model_type === 'embedding'
                                        ? 'bg-purple-100 text-purple-700'
                                        : 'bg-gray-100 text-gray-700'
                                    }`}>
                                      {model.model_type}
                                    </span>

                                    {(model.is_default_for_chat || model.is_default_for_embeddings || model.is_default_for_agents) && (
                                      <span className="ml-2 px-2 py-1 bg-green-100 text-green-700 text-xs rounded">
                                        Default
                                      </span>
                                    )}
                                  </div>

                                  <div className="mt-1 text-sm text-gray-500 font-mono">
                                    {model.model_id}
                                  </div>

                                  {model.description && (
                                    <p className="mt-1 text-sm text-gray-600">{model.description}</p>
                                  )}

                                  <div className="mt-3 flex flex-wrap gap-2 text-xs">
                                    {model.context_window && (
                                      <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded">
                                        Context: {model.context_window.toLocaleString()} tokens
                                      </span>
                                    )}

                                    {model.max_output_tokens && (
                                      <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded">
                                        Output: {model.max_output_tokens.toLocaleString()} tokens
                                      </span>
                                    )}

                                    {model.input_cost_per_1m && (
                                      <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded">
                                        ${model.input_cost_per_1m}/1M in
                                      </span>
                                    )}

                                    {model.output_cost_per_1m && (
                                      <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded">
                                        ${model.output_cost_per_1m}/1M out
                                      </span>
                                    )}

                                    {model.supports_vision && (
                                      <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded">
                                        Vision
                                      </span>
                                    )}

                                    {model.supports_tools && (
                                      <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded">
                                        Tools
                                      </span>
                                    )}
                                  </div>
                                </div>

                                <div className="flex items-center space-x-2 ml-4">
                                  <button
                                    onClick={() => handleEditModel(model)}
                                    className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                                    title="Edit"
                                  >
                                    <PencilIcon className="h-5 w-5" />
                                  </button>

                                  <button
                                    onClick={() => {
                                      if (confirm(`Delete model "${model.display_name}"?`)) {
                                        deleteModelMutation.mutate(model.id);
                                      }
                                    }}
                                    disabled={deleteModelMutation.isPending}
                                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                                    title="Delete"
                                  >
                                    <TrashIcon className="h-5 w-5" />
                                  </button>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </>
              )}
            </div>
          </div>
        )}

        {/* Defaults Tab */}
        {activeTab === 'defaults' && (
          <div>
            <div className="bg-white border rounded-lg p-6 shadow-sm">
              <h2 className="text-xl font-semibold mb-4">Default Model Configuration</h2>
              <p className="text-gray-600 mb-6">
                These models will be used system-wide unless overridden in specific contexts.
              </p>

              <div className="space-y-6">
                {/* Chat Default */}
                <div className="border-b pb-6">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <h3 className="font-semibold text-gray-900">Default Chat Model</h3>
                      <p className="text-sm text-gray-500">Used for general conversational AI tasks</p>
                    </div>
                  </div>

                  {defaults.chat ? (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-semibold text-blue-900">{defaults.chat.display_name}</div>
                          <div className="text-sm text-blue-700 font-mono">{defaults.chat.model_id}</div>
                          {defaults.chat.provider && (
                            <div className="text-sm text-blue-600 mt-1">
                              Provider: {defaults.chat.provider.display_name}
                            </div>
                          )}
                        </div>
                        <CheckCircleIcon className="h-6 w-6 text-blue-600" />
                      </div>
                    </div>
                  ) : (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">
                      <p className="text-sm">No default chat model configured. Add a model and mark it as default for chat.</p>
                    </div>
                  )}
                </div>

                {/* Embeddings Default */}
                <div className="border-b pb-6">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <h3 className="font-semibold text-gray-900">Default Embeddings Model</h3>
                      <p className="text-sm text-gray-500">Used for vector search and semantic similarity</p>
                    </div>
                  </div>

                  {defaults.embeddings ? (
                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-semibold text-purple-900">{defaults.embeddings.display_name}</div>
                          <div className="text-sm text-purple-700 font-mono">{defaults.embeddings.model_id}</div>
                          {defaults.embeddings.provider && (
                            <div className="text-sm text-purple-600 mt-1">
                              Provider: {defaults.embeddings.provider.display_name}
                            </div>
                          )}
                        </div>
                        <CheckCircleIcon className="h-6 w-6 text-purple-600" />
                      </div>
                    </div>
                  ) : (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">
                      <p className="text-sm">No default embeddings model configured. Add a model and mark it as default for embeddings.</p>
                    </div>
                  )}
                </div>

                {/* Agents Default */}
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <h3 className="font-semibold text-gray-900">Default Agent Model</h3>
                      <p className="text-sm text-gray-500">Used for AI agent operations and autonomous tasks</p>
                    </div>
                  </div>

                  {defaults.agents ? (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-semibold text-green-900">{defaults.agents.display_name}</div>
                          <div className="text-sm text-green-700 font-mono">{defaults.agents.model_id}</div>
                          {defaults.agents.provider && (
                            <div className="text-sm text-green-600 mt-1">
                              Provider: {defaults.agents.provider.display_name}
                            </div>
                          )}
                        </div>
                        <CheckCircleIcon className="h-6 w-6 text-green-600" />
                      </div>
                    </div>
                  ) : (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">
                      <p className="text-sm">No default agent model configured. Add a model and mark it as default for agents.</p>
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600">
                  <strong>Note:</strong> To change defaults, edit the corresponding model in the Models tab and check the appropriate "Set as default" options.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
