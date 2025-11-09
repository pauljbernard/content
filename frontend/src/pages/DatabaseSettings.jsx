/**
 * Database Settings Page - Configure databases, test connections, migrate data
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ServerIcon,
  CircleStackIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  PlayIcon,
  ChartBarIcon,
  CogIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import Layout from '../components/Layout';
import { databaseAPI } from '../services/api';

export default function DatabaseSettings() {
  const queryClient = useQueryClient();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedConfig, setSelectedConfig] = useState(null);
  const [showMigrationForm, setShowMigrationForm] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    db_type: 'postgresql',
    host: 'localhost',
    port: 5432,
    database_name: '',
    schema_name: 'public',
    username: '',
    password: '',
    ssl_mode: 'prefer',
    sqlite_path: './content.db',
    pool_size: 5,
    max_overflow: 10,
  });

  // Fetch database configs
  const { data: configs, isLoading } = useQuery({
    queryKey: ['database-configs'],
    queryFn: databaseAPI.listConfigs,
  });

  // Fetch active migrations
  const { data: migrations } = useQuery({
    queryKey: ['migration-jobs'],
    queryFn: databaseAPI.listMigrations,
    refetchInterval: 5000, // Poll every 5 seconds
  });

  // Create config mutation
  const createMutation = useMutation({
    mutationFn: databaseAPI.createConfig,
    onSuccess: () => {
      toast.success('Database configuration created');
      queryClient.invalidateQueries(['database-configs']);
      setShowCreateForm(false);
      resetForm();
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create configuration');
    },
  });

  // Test connection mutation
  const testMutation = useMutation({
    mutationFn: databaseAPI.testConnection,
    onSuccess: (data) => {
      toast.success(data.message);
      if (data.warning) {
        toast(data.warning, { icon: '⚠️' });
      }
      queryClient.invalidateQueries(['database-configs']);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Connection failed');
    },
  });

  // Initialize schema mutation
  const initializeMutation = useMutation({
    mutationFn: ({ configId, enablePgvector }) =>
      databaseAPI.initializeSchema(configId, enablePgvector),
    onSuccess: (data) => {
      toast.success(data.message);
      queryClient.invalidateQueries(['database-configs']);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Schema initialization failed');
    },
  });

  // Activate database mutation
  const activateMutation = useMutation({
    mutationFn: databaseAPI.activateConfig,
    onSuccess: (data) => {
      toast.success(data.message);
      queryClient.invalidateQueries(['database-configs']);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Activation failed');
    },
  });

  // Start migration mutation
  const migrateMutation = useMutation({
    mutationFn: databaseAPI.startMigration,
    onSuccess: () => {
      toast.success('Migration started');
      queryClient.invalidateQueries(['migration-jobs']);
      setShowMigrationForm(false);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Migration failed to start');
    },
  });

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      db_type: 'postgresql',
      host: 'localhost',
      port: 5432,
      database_name: '',
      schema_name: 'public',
      username: '',
      password: '',
      ssl_mode: 'prefer',
      sqlite_path: './content.db',
      pool_size: 5,
      max_overflow: 10,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  const getStatusColor = (status) => {
    const colors = {
      configured: 'gray',
      tested: 'blue',
      active: 'green',
      migrating: 'yellow',
      error: 'red',
    };
    return colors[status] || 'gray';
  };

  const getStatusIcon = (status) => {
    if (status === 'active') return CheckCircleIcon;
    if (status === 'error') return XCircleIcon;
    if (status === 'migrating') return ArrowPathIcon;
    return CircleStackIcon;
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Database Settings</h1>
            <p className="mt-2 text-sm text-gray-600">
              Configure PostgreSQL with pgvector for semantic search and vector embeddings
            </p>
          </div>
          <button
            onClick={() => setShowCreateForm(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
          >
            <ServerIcon className="h-5 w-5 mr-2" />
            Add Database
          </button>
        </div>

        {/* Create Form */}
        {showCreateForm && (
          <div className="mb-8 bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">New Database Configuration</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Database Type</label>
                  <select
                    value={formData.db_type}
                    onChange={(e) => setFormData({ ...formData, db_type: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  >
                    <option value="postgresql">PostgreSQL</option>
                    <option value="sqlite">SQLite</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <input
                  type="text"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>

              {formData.db_type === 'postgresql' ? (
                <>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Host</label>
                      <input
                        type="text"
                        value={formData.host}
                        onChange={(e) => setFormData({ ...formData, host: e.target.value })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Port</label>
                      <input
                        type="number"
                        value={formData.port}
                        onChange={(e) => setFormData({ ...formData, port: parseInt(e.target.value) })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        required
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Database Name</label>
                      <input
                        type="text"
                        value={formData.database_name}
                        onChange={(e) => setFormData({ ...formData, database_name: e.target.value })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Schema</label>
                      <input
                        type="text"
                        value={formData.schema_name}
                        onChange={(e) => setFormData({ ...formData, schema_name: e.target.value })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Username</label>
                      <input
                        type="text"
                        value={formData.username}
                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Password</label>
                      <input
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        required
                      />
                    </div>
                  </div>
                </>
              ) : (
                <div>
                  <label className="block text-sm font-medium text-gray-700">SQLite Path</label>
                  <input
                    type="text"
                    value={formData.sqlite_path}
                    onChange={(e) => setFormData({ ...formData, sqlite_path: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    required
                  />
                </div>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false);
                    resetForm();
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isPending}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                >
                  {createMutation.isPending ? 'Creating...' : 'Create Configuration'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Migration Form Modal */}
        {showMigrationForm && selectedConfig && (
          <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen px-4">
              <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setShowMigrationForm(false)}></div>

              <div className="relative bg-white rounded-lg shadow-xl max-w-lg w-full p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Migrate Data to {selectedConfig.name}
                </h3>

                <div className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-blue-900 mb-2">Migration Details</h4>
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li>• Source: SQLite (current active database)</li>
                      <li>• Target: {selectedConfig.name} ({selectedConfig.host}:{selectedConfig.port})</li>
                      <li>• All tables and relationships will be copied</li>
                      <li>• Estimated time: 30-60 seconds</li>
                    </ul>
                  </div>

                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-yellow-900 mb-2">⚠️ Important</h4>
                    <ul className="text-sm text-yellow-800 space-y-1">
                      <li>• This will copy all data to PostgreSQL</li>
                      <li>• The migration runs in the background</li>
                      <li>• After completion, activate PostgreSQL to switch</li>
                      <li>• Your SQLite data will remain untouched</li>
                    </ul>
                  </div>

                  <div className="flex justify-end space-x-3">
                    <button
                      type="button"
                      onClick={() => {
                        setShowMigrationForm(false);
                        setSelectedConfig(null);
                      }}
                      className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        // Find the active SQLite config
                        const sqliteConfig = configs.find(c => c.is_active);
                        if (sqliteConfig) {
                          migrateMutation.mutate({
                            source_config_id: sqliteConfig.id,
                            target_config_id: selectedConfig.id,
                            tables: [], // Empty array = migrate all tables
                            generate_embeddings: true
                          });
                        } else {
                          toast.error('No active source database found');
                        }
                      }}
                      disabled={migrateMutation.isPending}
                      className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                    >
                      {migrateMutation.isPending ? 'Starting Migration...' : 'Start Migration'}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Database Configurations List */}
        <div className="bg-white shadow rounded-lg divide-y divide-gray-200">
          {configs && configs.length > 0 ? (
            configs.map((config) => {
              const StatusIcon = getStatusIcon(config.status);
              const statusColor = getStatusColor(config.status);

              return (
                <div key={config.id} className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className={`p-3 rounded-lg bg-${statusColor}-100`}>
                        <StatusIcon className={`h-6 w-6 text-${statusColor}-600`} />
                      </div>
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">{config.name}</h3>
                        <p className="text-sm text-gray-500">{config.description}</p>
                        <div className="mt-1 flex items-center space-x-4 text-xs text-gray-500">
                          <span className="uppercase">{config.db_type}</span>
                          {config.db_type === 'postgresql' && (
                            <span>{config.host}:{config.port}/{config.database_name}</span>
                          )}
                          {config.pgvector_enabled && (
                            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800">
                              pgvector
                            </span>
                          )}
                          {config.is_active && (
                            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                              Active
                            </span>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => testMutation.mutate(config.id)}
                        disabled={testMutation.isPending}
                        className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                        title="Test Connection"
                      >
                        <PlayIcon className="h-4 w-4 mr-1" />
                        Test
                      </button>

                      {config.status === 'tested' && config.db_type === 'postgresql' && !config.pgvector_enabled && (
                        <button
                          onClick={() => initializeMutation.mutate({ configId: config.id, enablePgvector: true })}
                          disabled={initializeMutation.isPending}
                          className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                          title="Initialize Schema"
                        >
                          <CogIcon className="h-4 w-4 mr-1" />
                          Initialize
                        </button>
                      )}

                      {!config.is_active && (config.status === 'tested' || config.pgvector_enabled) && config.db_type === 'postgresql' && (
                        <button
                          onClick={() => {
                            setSelectedConfig(config);
                            setShowMigrationForm(true);
                          }}
                          disabled={migrateMutation.isPending}
                          className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                          title="Migrate Data"
                        >
                          <ArrowPathIcon className="h-4 w-4 mr-1" />
                          Migrate Data
                        </button>
                      )}

                      {!config.is_active && (config.status === 'tested' || config.pgvector_enabled) && (
                        <button
                          onClick={() => activateMutation.mutate(config.id)}
                          disabled={activateMutation.isPending}
                          className="inline-flex items-center px-3 py-1.5 border border-transparent rounded text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
                          title="Set as Active"
                        >
                          <CheckCircleIcon className="h-4 w-4 mr-1" />
                          Activate
                        </button>
                      )}
                    </div>
                  </div>

                  {config.last_error && (
                    <div className="mt-3 p-3 bg-red-50 rounded text-sm text-red-700">
                      {config.last_error}
                    </div>
                  )}
                </div>
              );
            })
          ) : (
            <div className="p-12 text-center">
              <ServerIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No database configurations</h3>
              <p className="mt-1 text-sm text-gray-500">
                Get started by creating a new database configuration.
              </p>
              <div className="mt-6">
                <button
                  onClick={() => setShowCreateForm(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
                >
                  <ServerIcon className="h-5 w-5 mr-2" />
                  Add Database
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Active Migrations */}
        {migrations && migrations.length > 0 && (
          <div className="mt-8 bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Migrations</h2>
            <div className="space-y-4">
              {migrations.slice(0, 5).map((job) => (
                <div key={job.id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-900">
                      Migration {job.id.substring(0, 8)}
                    </span>
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                      job.status === 'completed' ? 'bg-green-100 text-green-800' :
                      job.status === 'running' ? 'bg-yellow-100 text-yellow-800' :
                      job.status === 'failed' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {job.status}
                    </span>
                  </div>
                  {job.status === 'running' && (
                    <div className="mt-2">
                      <div className="flex justify-between text-xs text-gray-600 mb-1">
                        <span>{job.current_table}</span>
                        <span>{job.progress_pct}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${job.progress_pct}%` }}
                        ></div>
                      </div>
                      <div className="mt-1 text-xs text-gray-500">
                        {job.migrated_records} / {job.total_records} records
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
