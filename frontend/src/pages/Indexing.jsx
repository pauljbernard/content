/**
 * Indexing Management Page
 *
 * Provides UI for managing vector indexes and embeddings:
 * - Content instance embeddings (per content type)
 * - Knowledge base embeddings
 */
import { useState, useEffect } from 'react';
import { ServerIcon, ArrowPathIcon, CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import api from '../services/api';

export default function Indexing() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);
  const [progress, setProgress] = useState(null);

  // Fetch indexing status
  const fetchStatus = async () => {
    try {
      setLoading(true);
      const response = await api.get('/indexing/status');
      setStatus(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load indexing status: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  // SSE streaming handler for progress updates
  const handleStreamingAction = async (url, actionName) => {
    setActionLoading(actionName);
    setProgress({ percent: 0, message: 'Starting...' });

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${import.meta.env.VITE_API_URL}${url}`, {
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

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.substring(6));

            if (data.type === 'progress') {
              setProgress({
                percent: data.progress,
                message: `Processing ${data.processed}/${data.total}...`,
                stats: data
              });
            } else if (data.type === 'complete') {
              setActionLoading(null);
              setProgress(null);
              await fetchStatus();
              alert(`${actionName} completed successfully!`);
            } else if (data.type === 'error') {
              setActionLoading(null);
              setProgress(null);
              alert(`${actionName} failed: ${data.message}`);
            } else if (data.type === 'info') {
              setProgress((prev) => ({ ...prev, message: data.message }));
            }
          }
        }
      }

    } catch (err) {
      console.error('Streaming error:', err);
      setActionLoading(null);
      setProgress(null);
      alert(`${actionName} failed: ${err.message}`);
    }
  };

  // Non-streaming action handler (for init operations)
  const handleAction = async (actionFn, actionName) => {
    setActionLoading(actionName);
    try {
      await actionFn();
      await fetchStatus(); // Refresh status after action
      alert(`${actionName} completed successfully!`);
    } catch (err) {
      alert(`${actionName} failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setActionLoading(null);
    }
  };

  const initializeContentIndexes = () =>
    handleAction(
      () => api.post('/indexing/content/initialize'),
      'Initialize Content Indexes'
    );

  const generateContentEmbeddings = (forceReindex = false) =>
    handleStreamingAction(
      `/api/v1/indexing/content/generate-embeddings?force_reindex=${forceReindex}&stream=true`,
      forceReindex ? 'Force Reindex Content Embeddings' : 'Generate Missing Content Embeddings'
    );

  const initializeKBIndex = () =>
    handleAction(
      () => api.post('/indexing/knowledge-base/initialize'),
      'Initialize Knowledge Base Index'
    );

  const indexKBFiles = (forceReindex = false) =>
    handleStreamingAction(
      `/api/v1/indexing/knowledge-base/index-files?force_reindex=${forceReindex}&stream=true`,
      forceReindex ? 'Force Reindex Knowledge Base' : 'Index New/Changed Knowledge Base Files'
    );

  const contentStats = status?.content_instances || {};
  const kbStats = status?.knowledge_base || {};

  return (
    <Layout>
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : error ? (
        <div className="p-4">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      ) : (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <ServerIcon className="h-8 w-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">Vector Indexing</h1>
        </div>
        <p className="text-gray-600">
          Manage vector indexes and embeddings for semantic search across content instances and knowledge base files.
        </p>
      </div>

      {/* Refresh Button */}
      <div className="mb-6">
        <button
          onClick={fetchStatus}
          className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          <ArrowPathIcon className="h-4 w-4 mr-2" />
          Refresh Status
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Content Instance Indexing */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-5 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Content Instance Embeddings</h2>
            <p className="mt-1 text-sm text-gray-500">Vector search on content instances (lessons, assessments, etc.)</p>
          </div>

          <div className="px-6 py-5 space-y-6">
            {/* Status */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-3">Current Status</h3>

              {!contentStats.column_exists ? (
                <div className="flex items-center gap-2 text-yellow-700 bg-yellow-50 p-3 rounded-md">
                  <ExclamationCircleIcon className="h-5 w-5" />
                  <span className="text-sm">Embedding column not initialized</span>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Total Instances:</span>
                    <span className="font-semibold">{contentStats.total_instances || 0}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">With Embeddings:</span>
                    <span className="font-semibold text-green-600">
                      {contentStats.with_embeddings || 0} ({(contentStats.coverage_percent || 0).toFixed(1)}%)
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Missing Embeddings:</span>
                    <span className="font-semibold text-orange-600">{contentStats.without_embeddings || 0}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Vector Indexes:</span>
                    <span className="font-semibold">{contentStats.vector_indexes?.count || 0}</span>
                  </div>

                  {/* Progress bar */}
                  <div className="mt-4">
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                      <span>Coverage</span>
                      <span>{(contentStats.coverage_percent || 0).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-600 h-2 rounded-full transition-all"
                        style={{ width: `${contentStats.coverage_percent || 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="space-y-3 pt-4 border-t border-gray-200">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Actions</h3>

              <button
                onClick={initializeContentIndexes}
                disabled={actionLoading}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {actionLoading === 'Initialize Content Indexes' ? (
                  <>
                    <ArrowPathIcon className="animate-spin h-4 w-4 mr-2" />
                    Initializing...
                  </>
                ) : (
                  <>
                    <CheckCircleIcon className="h-4 w-4 mr-2" />
                    Initialize Indexes (Create Missing)
                  </>
                )}
              </button>

              <button
                onClick={() => generateContentEmbeddings(false)}
                disabled={actionLoading || !contentStats.column_exists}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {actionLoading === 'Generate Missing Content Embeddings' ? (
                  <>
                    <ArrowPathIcon className="animate-spin h-4 w-4 mr-2" />
                    {progress ? `${progress.percent}% - ${progress.message}` : 'Generating...'}
                  </>
                ) : (
                  <>
                    <ServerIcon className="h-4 w-4 mr-2" />
                    Generate Missing Embeddings
                  </>
                )}
              </button>

              <button
                onClick={() => {
                  if (confirm('This will regenerate ALL embeddings. This is expensive and may take a long time. Continue?')) {
                    generateContentEmbeddings(true);
                  }
                }}
                disabled={actionLoading || !contentStats.column_exists}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {actionLoading === 'Force Reindex Content Embeddings' ? (
                  <>
                    <ArrowPathIcon className="animate-spin h-4 w-4 mr-2" />
                    {progress ? `${progress.percent}% - ${progress.message}` : 'Force Reindexing...'}
                  </>
                ) : (
                  <>
                    <ArrowPathIcon className="h-4 w-4 mr-2" />
                    Force Reindex All (Expensive!)
                  </>
                )}
              </button>
            </div>

            {/* Per-Content-Type Breakdown */}
            {contentStats.by_content_type && contentStats.by_content_type.length > 0 && (
              <div className="pt-4 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-700 mb-3">By Content Type</h3>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {contentStats.by_content_type.map((ct) => (
                    <div key={ct.content_type_id} className="flex justify-between items-center text-sm">
                      <span className="text-gray-600 truncate flex-1">{ct.content_type_name}</span>
                      <span className="ml-2 text-gray-900 font-medium">
                        {ct.with_embeddings}/{ct.total_instances}
                        {ct.total_instances > 0 && (
                          <span className="ml-1 text-xs text-gray-500">
                            ({ct.coverage_percent.toFixed(0)}%)
                          </span>
                        )}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Knowledge Base Indexing */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-5 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Knowledge Base Embeddings</h2>
            <p className="mt-1 text-sm text-gray-500">Vector search on knowledge base markdown files</p>
          </div>

          <div className="px-6 py-5 space-y-6">
            {/* Status */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-3">Current Status</h3>

              {!kbStats.table_exists ? (
                <div className="flex items-center gap-2 text-yellow-700 bg-yellow-50 p-3 rounded-md">
                  <ExclamationCircleIcon className="h-5 w-5" />
                  <span className="text-sm">Knowledge base table not initialized</span>
                </div>
              ) : !kbStats.column_exists ? (
                <div className="flex items-center gap-2 text-yellow-700 bg-yellow-50 p-3 rounded-md">
                  <ExclamationCircleIcon className="h-5 w-5" />
                  <span className="text-sm">Embedding column not initialized</span>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Total Files:</span>
                    <span className="font-semibold">{kbStats.total_files || 0}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">With Embeddings:</span>
                    <span className="font-semibold text-green-600">
                      {kbStats.with_embeddings || 0} ({(kbStats.coverage_percent || 0).toFixed(1)}%)
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Missing Embeddings:</span>
                    <span className="font-semibold text-orange-600">{kbStats.without_embeddings || 0}</span>
                  </div>

                  {/* Progress bar */}
                  <div className="mt-4">
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                      <span>Coverage</span>
                      <span>{(kbStats.coverage_percent || 0).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-600 h-2 rounded-full transition-all"
                        style={{ width: `${kbStats.coverage_percent || 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="space-y-3 pt-4 border-t border-gray-200">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Actions</h3>

              <button
                onClick={initializeKBIndex}
                disabled={actionLoading}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {actionLoading === 'Initialize Knowledge Base Index' ? (
                  <>
                    <ArrowPathIcon className="animate-spin h-4 w-4 mr-2" />
                    Initializing...
                  </>
                ) : (
                  <>
                    <CheckCircleIcon className="h-4 w-4 mr-2" />
                    Initialize KB Index
                  </>
                )}
              </button>

              <button
                onClick={() => indexKBFiles(false)}
                disabled={actionLoading || !kbStats.table_exists || !kbStats.column_exists}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {actionLoading === 'Index New/Changed Knowledge Base Files' ? (
                  <>
                    <ArrowPathIcon className="animate-spin h-4 w-4 mr-2" />
                    {progress ? `${progress.percent}% - ${progress.message}` : 'Indexing...'}
                  </>
                ) : (
                  <>
                    <ServerIcon className="h-4 w-4 mr-2" />
                    Index New/Changed Files
                  </>
                )}
              </button>

              <button
                onClick={() => {
                  if (confirm('This will reindex ALL knowledge base files. This is expensive and may take a long time. Continue?')) {
                    indexKBFiles(true);
                  }
                }}
                disabled={actionLoading || !kbStats.table_exists || !kbStats.column_exists}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {actionLoading === 'Force Reindex Knowledge Base' ? (
                  <>
                    <ArrowPathIcon className="animate-spin h-4 w-4 mr-2" />
                    {progress ? `${progress.percent}% - ${progress.message}` : 'Force Reindexing...'}
                  </>
                ) : (
                  <>
                    <ArrowPathIcon className="h-4 w-4 mr-2" />
                    Force Reindex All (Expensive!)
                  </>
                )}
              </button>
            </div>

            {/* Category Breakdown */}
            {kbStats.by_category && kbStats.by_category.length > 0 && (
              <div className="pt-4 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-700 mb-3">By Category</h3>
                <div className="space-y-2">
                  {kbStats.by_category.map((cat) => (
                    <div key={cat.category} className="flex justify-between items-center text-sm">
                      <span className="text-gray-600">{cat.category}</span>
                      <span className="text-gray-900 font-medium">{cat.count}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Info Section */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-sm font-medium text-blue-900 mb-2">About Vector Indexing</h3>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            Vector indexing enables semantic search across your content using AI embeddings.
            The system automatically creates indexes when content types are created and generates
            embeddings when instances are created/updated.
          </p>
          <p>
            <strong>Use these tools when:</strong>
          </p>
          <ul className="list-disc list-inside ml-4 space-y-1">
            <li>Setting up the system for the first time</li>
            <li>Backfilling embeddings for existing content</li>
            <li>Adding new content types that need indexes</li>
            <li>Knowledge base files have been added or modified</li>
            <li>Switching to a different embedding model</li>
          </ul>
          <p className="mt-3">
            <strong>Performance Note:</strong> Force reindexing regenerates all embeddings which calls
            the OpenAI API for every instance/file. This can be expensive and time-consuming.
          </p>
        </div>
      </div>
        </div>
      )}
    </Layout>
  );
}
