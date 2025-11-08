/**
 * Content Instances List Page
 * Shows all instances of a specific content type
 */
import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  ArrowLeftIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

export default function ContentInstances() {
  const { contentTypeId } = useParams();
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  // Fetch content type
  const { data: contentType, isLoading: loadingContentType } = useQuery({
    queryKey: ['content-type', contentTypeId],
    queryFn: () => contentTypesAPI.get(contentTypeId),
  });

  // Fetch instances
  const { data: instances, isLoading: loadingInstances } = useQuery({
    queryKey: ['content-instances', contentTypeId],
    queryFn: () => contentTypesAPI.listInstances(contentTypeId),
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: contentTypesAPI.deleteInstance,
    onSuccess: () => {
      queryClient.invalidateQueries(['content-instances', contentTypeId]);
      toast.success('Instance deleted successfully');
    },
    onError: (error) => {
      toast.error(
        `Failed to delete instance: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  const handleDelete = (instanceId, instanceTitle) => {
    if (
      window.confirm(
        `Are you sure you want to delete "${instanceTitle}"? This action cannot be undone.`
      )
    ) {
      deleteMutation.mutate(instanceId);
    }
  };

  // Filter instances
  const filteredInstances = instances?.filter((instance) => {
    // Status filter
    if (statusFilter !== 'all' && instance.status !== statusFilter) {
      return false;
    }

    // Search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const instanceData = JSON.stringify(instance.data).toLowerCase();
      return instanceData.includes(searchLower);
    }

    return true;
  });

  // Get display title for an instance
  const getInstanceTitle = (instance) => {
    return (
      instance.data?.title ||
      instance.data?.name ||
      instance.data?.label ||
      `Instance ${instance.id.substring(0, 8)}`
    );
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800';
      case 'draft':
        return 'bg-yellow-100 text-yellow-800';
      case 'archived':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  if (loadingContentType || loadingInstances) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p className="mt-2 text-sm text-gray-500">Loading...</p>
        </div>
      </Layout>
    );
  }

  if (!contentType) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-red-600">Content type not found</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link
              to="/content-types"
              className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700"
            >
              <ArrowLeftIcon className="h-5 w-5 mr-1" />
              Back to Content Types
            </Link>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {contentType.name} Instances
            </h1>
            {contentType.description && (
              <p className="mt-1 text-sm text-gray-500">
                {contentType.description}
              </p>
            )}
          </div>
          <Link
            to={`/content-types/${contentTypeId}/instances/new`}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            New Instance
          </Link>
        </div>

        {/* Filters */}
        <div className="bg-white shadow rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search
              </label>
              <input
                type="text"
                placeholder="Search instances..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="all">All Statuses</option>
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="archived">Archived</option>
              </select>
            </div>
          </div>
        </div>

        {/* Instances Table */}
        {filteredInstances && filteredInstances.length > 0 ? (
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Updated
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredInstances.map((instance) => (
                  <tr key={instance.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {getInstanceTitle(instance)}
                      </div>
                      <div className="text-xs text-gray-500">
                        ID: {instance.id.substring(0, 8)}...
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                          instance.status
                        )}`}
                      >
                        {instance.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(instance.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(instance.updated_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end space-x-2">
                        <Link
                          to={`/content-types/${contentTypeId}/instances/${instance.id}`}
                          className="inline-flex items-center p-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
                          title="View"
                        >
                          <EyeIcon className="h-4 w-4" />
                        </Link>
                        <Link
                          to={`/content-types/${contentTypeId}/instances/${instance.id}/edit`}
                          className="inline-flex items-center p-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
                          title="Edit"
                        >
                          <PencilIcon className="h-4 w-4" />
                        </Link>
                        <button
                          onClick={() =>
                            handleDelete(instance.id, getInstanceTitle(instance))
                          }
                          className="inline-flex items-center p-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-red-700 bg-white hover:bg-red-50"
                          title="Delete"
                        >
                          <TrashIcon className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12 bg-white shadow rounded-lg">
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              No instances found
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by creating a new instance.
            </p>
            <div className="mt-6">
              <Link
                to={`/content-types/${contentTypeId}/instances/new`}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                New Instance
              </Link>
            </div>
          </div>
        )}

        {/* Summary */}
        {instances && instances.length > 0 && (
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
            <p className="text-sm text-blue-700">
              Showing {filteredInstances?.length || 0} of {instances.length}{' '}
              instances
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
}
