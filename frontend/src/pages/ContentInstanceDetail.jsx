/**
 * Content Instance Detail Page
 * Shows detailed view of a single content instance
 */
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  ArrowLeftIcon,
  PencilIcon,
  TrashIcon,
  ClockIcon,
  UserIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

export default function ContentInstanceDetail() {
  const { contentTypeId, instanceId } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Fetch content type
  const { data: contentType, isLoading: loadingContentType } = useQuery({
    queryKey: ['content-type', contentTypeId],
    queryFn: () => contentTypesAPI.get(contentTypeId),
  });

  // Fetch instance
  const { data: instance, isLoading: loadingInstance } = useQuery({
    queryKey: ['content-instance', instanceId],
    queryFn: () => contentTypesAPI.getInstance(instanceId),
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: contentTypesAPI.deleteInstance,
    onSuccess: () => {
      queryClient.invalidateQueries(['content-instances', contentTypeId]);
      toast.success('Instance deleted successfully');
      navigate(`/content-types/${contentTypeId}/instances`);
    },
    onError: (error) => {
      toast.error(
        `Failed to delete instance: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  const handleDelete = () => {
    const title =
      instance?.data?.title ||
      instance?.data?.name ||
      `Instance ${instanceId.substring(0, 8)}`;

    if (
      window.confirm(
        `Are you sure you want to delete "${title}"? This action cannot be undone.`
      )
    ) {
      deleteMutation.mutate(instanceId);
    }
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

  const renderValue = (value, attributeType) => {
    if (value === null || value === undefined) {
      return <span className="text-gray-400 italic">Not set</span>;
    }

    switch (attributeType) {
      case 'boolean':
        return value ? (
          <span className="text-green-600">Yes</span>
        ) : (
          <span className="text-gray-500">No</span>
        );

      case 'date':
        return new Date(value).toLocaleDateString();

      case 'choice':
        if (Array.isArray(value)) {
          return value.join(', ');
        }
        return value;

      case 'reference':
        if (Array.isArray(value)) {
          return `${value.length} reference(s)`;
        }
        return value;

      case 'media':
        if (typeof value === 'object') {
          return value.filename || JSON.stringify(value);
        }
        return value;

      case 'json':
        return (
          <pre className="text-xs bg-gray-100 p-2 rounded overflow-x-auto">
            {JSON.stringify(value, null, 2)}
          </pre>
        );

      case 'location':
        if (typeof value === 'object' && value.lat && value.lng) {
          return `${value.lat}, ${value.lng}`;
        }
        return JSON.stringify(value);

      case 'long_text':
      case 'rich_text':
        return (
          <div className="text-sm whitespace-pre-wrap break-words">
            {value.length > 500 ? value.substring(0, 500) + '...' : value}
          </div>
        );

      default:
        if (typeof value === 'object') {
          return JSON.stringify(value);
        }
        return value;
    }
  };

  if (loadingContentType || loadingInstance) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p className="mt-2 text-sm text-gray-500">Loading...</p>
        </div>
      </Layout>
    );
  }

  if (!contentType || !instance) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-red-600">Content not found</p>
        </div>
      </Layout>
    );
  }

  const title =
    instance.data?.title ||
    instance.data?.name ||
    instance.data?.label ||
    `Instance ${instanceId.substring(0, 8)}`;

  // Sort attributes by order_index
  const sortedAttributes = [...(contentType.attributes || [])].sort(
    (a, b) => (a.order_index || 0) - (b.order_index || 0)
  );

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link
              to={`/content-types/${contentTypeId}/instances`}
              className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700"
            >
              <ArrowLeftIcon className="h-5 w-5 mr-1" />
              Back to Instances
            </Link>
          </div>
          <div className="flex items-center space-x-2">
            <Link
              to={`/content-types/${contentTypeId}/instances/${instanceId}/edit`}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              <PencilIcon className="h-5 w-5 mr-2" />
              Edit
            </Link>
            <button
              onClick={handleDelete}
              disabled={deleteMutation.isPending}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 disabled:opacity-50"
            >
              <TrashIcon className="h-5 w-5 mr-2" />
              Delete
            </button>
          </div>
        </div>

        {/* Title and Status */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
              <p className="mt-1 text-sm text-gray-500">{contentType.name}</p>
            </div>
            <span
              className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                instance.status
              )}`}
            >
              {instance.status}
            </span>
          </div>
        </div>

        {/* Metadata */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Metadata</h2>
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <dt className="text-sm font-medium text-gray-500 flex items-center">
                <ClockIcon className="h-4 w-4 mr-1" />
                Created
              </dt>
              <dd className="mt-1 text-sm text-gray-900">
                {new Date(instance.created_at).toLocaleString()}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500 flex items-center">
                <ClockIcon className="h-4 w-4 mr-1" />
                Last Updated
              </dt>
              <dd className="mt-1 text-sm text-gray-900">
                {new Date(instance.updated_at).toLocaleString()}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">ID</dt>
              <dd className="mt-1 text-sm text-gray-900 font-mono">
                {instance.id}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Version</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {instance.version || 1}
              </dd>
            </div>
          </dl>
        </div>

        {/* Content Data */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Content</h2>
          <dl className="space-y-4">
            {sortedAttributes.map((attribute) => (
              <div
                key={attribute.name}
                className="border-b border-gray-200 pb-4 last:border-b-0 last:pb-0"
              >
                <dt className="text-sm font-medium text-gray-900 mb-2">
                  {attribute.label || attribute.name}
                  {attribute.required && (
                    <span className="text-red-500 ml-1">*</span>
                  )}
                </dt>
                <dd className="text-sm text-gray-700">
                  {renderValue(instance.data[attribute.name], attribute.type)}
                </dd>
                {attribute.help_text && (
                  <dd className="mt-1 text-xs text-gray-500">
                    {attribute.help_text}
                  </dd>
                )}
              </div>
            ))}

            {sortedAttributes.length === 0 && (
              <p className="text-sm text-gray-500 text-center py-4">
                No attributes defined for this content type
              </p>
            )}
          </dl>
        </div>

        {/* Raw Data (for debugging) */}
        <details className="bg-gray-50 shadow rounded-lg p-6">
          <summary className="text-sm font-medium text-gray-700 cursor-pointer">
            Raw Data (JSON)
          </summary>
          <pre className="mt-4 text-xs bg-white p-4 rounded border border-gray-200 overflow-x-auto">
            {JSON.stringify(instance, null, 2)}
          </pre>
        </details>
      </div>
    </Layout>
  );
}
