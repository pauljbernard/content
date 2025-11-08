/**
 * Config Manager page - manage curriculum configurations
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';
import { configAPI } from '../services/api';
import Layout from '../components/Layout';

export default function ConfigManager() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingConfig, setEditingConfig] = useState(null);
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    grades: [],
    subject: '',
    district: '',
    course: '',
    knowledge_resolution: { order: [] },
  });

  const { data: configs, isLoading } = useQuery({
    queryKey: ['curriculum-configs'],
    queryFn: () => configAPI.list(),
  });

  const createMutation = useMutation({
    mutationFn: configAPI.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['curriculum-configs'] });
      setIsModalOpen(false);
      resetForm();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => configAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['curriculum-configs'] });
      setIsModalOpen(false);
      resetForm();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: configAPI.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['curriculum-configs'] });
    },
  });

  const resetForm = () => {
    setFormData({
      id: '',
      name: '',
      grades: [],
      subject: '',
      district: '',
      course: '',
      knowledge_resolution: { order: [] },
    });
    setEditingConfig(null);
  };

  const handleEdit = (config) => {
    setEditingConfig(config.id);
    setFormData(config);
    setIsModalOpen(true);
  };

  const handleDelete = (configId) => {
    if (confirm('Are you sure you want to delete this configuration?')) {
      deleteMutation.mutate(configId);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (editingConfig) {
      updateMutation.mutate({ id: editingConfig, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Curriculum Configurations
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Manage curriculum configurations and knowledge resolution orders
            </p>
          </div>
          <button
            onClick={() => {
              resetForm();
              setIsModalOpen(true);
            }}
            className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            New Configuration
          </button>
        </div>

        {/* Config List */}
        <div className="bg-white shadow rounded-lg overflow-hidden">
          {isLoading ? (
            <div className="p-8 text-center text-gray-500">Loading...</div>
          ) : configs && configs.length > 0 ? (
            <div className="divide-y divide-gray-200">
              {configs.map((config) => (
                <div key={config.id} className="p-6 hover:bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center">
                        <Cog6ToothIcon className="h-6 w-6 text-primary-600 mr-3" />
                        <div>
                          <h3 className="text-lg font-medium text-gray-900">
                            {config.name}
                          </h3>
                          <div className="mt-1 flex items-center space-x-3 text-sm text-gray-500">
                            <span className="font-mono bg-gray-100 px-2 py-1 rounded">
                              {config.id}
                            </span>
                            <span>•</span>
                            <span>{config.subject}</span>
                            {config.district && (
                              <>
                                <span>•</span>
                                <span className="uppercase">{config.district}</span>
                              </>
                            )}
                            {config.grades && config.grades.length > 0 && (
                              <>
                                <span>•</span>
                                <span>Grades {config.grades.join(', ')}</span>
                              </>
                            )}
                          </div>
                          {config.course && (
                            <div className="mt-1 text-sm text-gray-500">
                              Course: {config.course}
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Resolution Order */}
                      {config.knowledge_resolution?.order && (
                        <div className="mt-4 p-3 bg-gray-50 rounded-md">
                          <p className="text-xs font-medium text-gray-700 mb-2">
                            Knowledge Resolution Order:
                          </p>
                          <ol className="list-decimal list-inside space-y-1 text-xs text-gray-600">
                            {config.knowledge_resolution.order.map((path, idx) => (
                              <li key={idx} className="font-mono">
                                {path}
                              </li>
                            ))}
                          </ol>
                        </div>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="ml-4 flex space-x-2">
                      <button
                        onClick={() => handleEdit(config)}
                        className="p-2 text-gray-400 hover:text-primary-600"
                        title="Edit"
                      >
                        <PencilIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => handleDelete(config.id)}
                        className="p-2 text-gray-400 hover:text-red-600"
                        title="Delete"
                      >
                        <TrashIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-8 text-center text-gray-500">
              No configurations yet. Create your first one!
            </div>
          )}
        </div>

        {/* Modal */}
        {isModalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <form onSubmit={handleSubmit}>
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">
                    {editingConfig ? 'Edit Configuration' : 'New Configuration'}
                  </h2>
                </div>

                <div className="p-6 space-y-4">
                  {/* Config ID */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Configuration ID *
                    </label>
                    <input
                      type="text"
                      required
                      disabled={!!editingConfig}
                      value={formData.id}
                      onChange={(e) =>
                        setFormData({ ...formData, id: e.target.value })
                      }
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
                      placeholder="e.g., hmh-math-tx"
                    />
                  </div>

                  {/* Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Display Name *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) =>
                        setFormData({ ...formData, name: e.target.value })
                      }
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., HMH Math - Texas K-8"
                    />
                  </div>

                  {/* Subject & District */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Subject *
                      </label>
                      <input
                        type="text"
                        required
                        value={formData.subject}
                        onChange={(e) =>
                          setFormData({ ...formData, subject: e.target.value })
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="e.g., mathematics"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        District/State
                      </label>
                      <input
                        type="text"
                        value={formData.district}
                        onChange={(e) =>
                          setFormData({ ...formData, district: e.target.value })
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="e.g., texas"
                      />
                    </div>
                  </div>

                  {/* Grades */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Grades (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={formData.grades.join(', ')}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          grades: e.target.value.split(',').map((g) => g.trim()),
                        })
                      }
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., K, 1, 2, 3, 4, 5, 6, 7, 8"
                    />
                  </div>

                  {/* Course */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Course Name
                    </label>
                    <input
                      type="text"
                      value={formData.course}
                      onChange={(e) =>
                        setFormData({ ...formData, course: e.target.value })
                      }
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., Algebra I"
                    />
                  </div>

                  {/* Knowledge Resolution Order */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Knowledge Resolution Order (one path per line)
                    </label>
                    <textarea
                      value={formData.knowledge_resolution.order.join('\n')}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          knowledge_resolution: {
                            order: e.target.value.split('\n').filter((p) => p),
                          },
                        })
                      }
                      rows={6}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 font-mono text-sm"
                      placeholder="/reference/hmh-knowledge/subjects/mathematics/districts/texas/&#10;/reference/hmh-knowledge/subjects/mathematics/common/&#10;/reference/hmh-knowledge/districts/texas/&#10;/reference/hmh-knowledge/universal/"
                    />
                  </div>
                </div>

                <div className="p-6 border-t flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      setIsModalOpen(false);
                      resetForm();
                    }}
                    className="px-4 py-2 text-gray-700 hover:text-gray-900"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={
                      createMutation.isLoading || updateMutation.isLoading
                    }
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                  >
                    {createMutation.isLoading || updateMutation.isLoading
                      ? 'Saving...'
                      : editingConfig
                      ? 'Update Configuration'
                      : 'Create Configuration'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
