/**
 * Queues - View and manage content instances by workflow status
 * Generic queue system for all content types and statuses
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import {
  QueueListIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  ArchiveBoxIcon,
  DocumentTextIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

// Status configurations
const STATUS_CONFIGS = {
  draft: {
    label: 'Draft',
    icon: DocumentTextIcon,
    color: 'gray',
    description: 'Content being authored or revised',
    actions: ['submit_for_review', 'archive', 'delete'],
  },
  in_review: {
    label: 'In Review',
    icon: ClockIcon,
    color: 'yellow',
    description: 'Content awaiting editorial review',
    actions: ['approve', 'send_back', 'archive'],
  },
  published: {
    label: 'Published',
    icon: CheckCircleIcon,
    color: 'green',
    description: 'Live content available to users',
    actions: ['unpublish', 'archive'],
  },
  archived: {
    label: 'Archived',
    icon: ArchiveBoxIcon,
    color: 'red',
    description: 'Archived or deprecated content',
    actions: ['restore', 'delete'],
  },
};

export default function Queues() {
  const queryClient = useQueryClient();
  const [selectedStatus, setSelectedStatus] = useState('in_review');
  const [selectedContentType, setSelectedContentType] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  // Fetch content types for filtering
  const { data: contentTypesData } = useQuery({
    queryKey: ['content-types'],
    queryFn: () => contentTypesAPI.list(),
  });

  const contentTypes = contentTypesData?.items || contentTypesData || [];

  // Fetch content instances for selected status
  const { data: queueData, isLoading } = useQuery({
    queryKey: ['queue', selectedStatus, selectedContentType, searchQuery],
    queryFn: () => {
      const params = { status: selectedStatus };
      if (selectedContentType !== 'all') {
        params.content_type_id = selectedContentType;
      }
      if (searchQuery) {
        params.search = searchQuery;
      }
      return contentTypesAPI.listAllInstances(params);
    },
  });

  const queueItems = queueData?.items || queueData || [];

  // Update instance status mutation
  const updateStatusMutation = useMutation({
    mutationFn: ({ instanceId, status }) =>
      contentTypesAPI.updateInstance(instanceId, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries(['queue']);
      queryClient.invalidateQueries(['all-content-instances']);
      toast.success('Status updated successfully');
    },
    onError: (error) => {
      toast.error(
        `Failed to update status: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  const handleStatusChange = (instanceId, newStatus) => {
    if (window.confirm(`Change status to "${STATUS_CONFIGS[newStatus]?.label}"?`)) {
      updateStatusMutation.mutate({ instanceId, status: newStatus });
    }
  };

  const getStatusBadge = (status) => {
    const config = STATUS_CONFIGS[status] || STATUS_CONFIGS.draft;
    const colorClasses = {
      gray: 'bg-gray-100 text-gray-800',
      yellow: 'bg-yellow-100 text-yellow-800',
      green: 'bg-green-100 text-green-800',
      red: 'bg-red-100 text-red-800',
    };

    return (
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          colorClasses[config.color]
        }`}
      >
        {config.label}
      </span>
    );
  };

  const currentConfig = STATUS_CONFIGS[selectedStatus];
  const IconComponent = currentConfig?.icon || QueueListIcon;

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <QueueListIcon className="h-8 w-8 mr-3 text-primary-600" />
            Content Queues
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage content instances organized by workflow status
          </p>
        </div>

        {/* Status Tabs */}
        <div className="bg-white shadow rounded-lg">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6" aria-label="Tabs">
              {Object.entries(STATUS_CONFIGS).map(([status, config]) => {
                const StatusIcon = config.icon;
                const isActive = selectedStatus === status;

                return (
                  <button
                    key={status}
                    onClick={() => setSelectedStatus(status)}
                    className={`${
                      isActive
                        ? 'border-primary-500 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
                  >
                    <StatusIcon className="h-5 w-5 mr-2" />
                    {config.label}
                    {queueItems && selectedStatus === status && (
                      <span className="ml-2 py-0.5 px-2 rounded-full text-xs bg-gray-100 text-gray-900">
                        {queueItems.length}
                      </span>
                    )}
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Status Description */}
          <div className="px-6 py-3 bg-gray-50 border-b border-gray-200">
            <div className="flex items-center text-sm text-gray-600">
              <IconComponent className="h-4 w-4 mr-2" />
              {currentConfig?.description}
            </div>
          </div>

          {/* Filters */}
          <div className="px-6 py-4 border-b border-gray-200">
            {/* Search */}
            <div className="mb-3">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="Search by title, description, or content type..."
                />
              </div>
            </div>

            {/* Filter Toggle */}
            <div className="flex items-center justify-between">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="inline-flex items-center text-sm text-gray-700 hover:text-gray-900"
              >
                <FunnelIcon className="h-4 w-4 mr-2" />
                {showFilters ? 'Hide Filters' : 'Show Filters'}
              </button>

              {selectedContentType !== 'all' && (
                <button
                  onClick={() => setSelectedContentType('all')}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  Clear Filters
                </button>
              )}
            </div>

            {/* Filters Panel */}
            {showFilters && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Content Type
                </label>
                <select
                  value={selectedContentType}
                  onChange={(e) => setSelectedContentType(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  <option value="all">All Content Types</option>
                  {contentTypes?.map((ct) => (
                    <option key={ct.id} value={ct.id}>
                      {ct.name}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {/* Queue Items List */}
          <div className="divide-y divide-gray-200">
            {isLoading ? (
              <div className="p-12 text-center text-gray-500">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
                Loading...
              </div>
            ) : queueItems && queueItems.length > 0 ? (
              queueItems.map((item) => {
                const title =
                  item.data?.title ||
                  item.data?.name ||
                  item.data?.human_coding_scheme ||
                  `Content ${item.id.substring(0, 8)}`;

                return (
                  <div
                    key={item.id}
                    className="p-6 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      {/* Content Info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-3 mb-2">
                          <Link
                            to={`/content-types/${item.content_type_id}/instances/${item.id}`}
                            className="text-lg font-medium text-gray-900 hover:text-primary-600"
                          >
                            {title}
                          </Link>
                          {getStatusBadge(item.status)}
                        </div>

                        <div className="flex items-center space-x-4 text-sm text-gray-500 mb-2">
                          <span className="inline-flex items-center">
                            <DocumentTextIcon className="h-4 w-4 mr-1" />
                            {item.content_type?.name || 'Unknown Type'}
                          </span>
                          {item.data?.subject && (
                            <span className="capitalize">{item.data.subject}</span>
                          )}
                          {item.data?.grade_level && (
                            <span>Grade {item.data.grade_level}</span>
                          )}
                        </div>

                        {/* Preview */}
                        {(item.data?.description ||
                          item.data?.full_statement ||
                          item.data?.learning_objectives) && (
                          <p className="text-sm text-gray-600 line-clamp-2">
                            {item.data?.description ||
                              item.data?.full_statement ||
                              (typeof item.data?.learning_objectives === 'string'
                                ? item.data.learning_objectives.substring(0, 150)
                                : '')}
                          </p>
                        )}

                        {/* Metadata */}
                        <div className="mt-2 text-xs text-gray-400">
                          Updated {new Date(item.updated_at).toLocaleDateString()} at{' '}
                          {new Date(item.updated_at).toLocaleTimeString()}
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="ml-4 flex-shrink-0 flex flex-col space-y-2">
                        <Link
                          to={`/content-types/${item.content_type_id}/instances/${item.id}`}
                          className="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                        >
                          View
                        </Link>

                        {/* Quick Actions based on current status */}
                        {selectedStatus === 'in_review' && (
                          <>
                            <button
                              onClick={() => handleStatusChange(item.id, 'published')}
                              className="inline-flex items-center px-3 py-1.5 border border-transparent shadow-sm text-xs font-medium rounded text-white bg-green-600 hover:bg-green-700"
                            >
                              <CheckCircleIcon className="h-4 w-4 mr-1" />
                              Approve
                            </button>
                            <button
                              onClick={() => handleStatusChange(item.id, 'draft')}
                              className="inline-flex items-center px-3 py-1.5 border border-transparent shadow-sm text-xs font-medium rounded text-white bg-yellow-600 hover:bg-yellow-700"
                            >
                              Send Back
                            </button>
                          </>
                        )}

                        {selectedStatus === 'draft' && (
                          <button
                            onClick={() => handleStatusChange(item.id, 'in_review')}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent shadow-sm text-xs font-medium rounded text-white bg-primary-600 hover:bg-primary-700"
                          >
                            Submit for Review
                          </button>
                        )}

                        {selectedStatus === 'published' && (
                          <button
                            onClick={() => handleStatusChange(item.id, 'draft')}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent shadow-sm text-xs font-medium rounded text-white bg-yellow-600 hover:bg-yellow-700"
                          >
                            Unpublish
                          </button>
                        )}

                        {selectedStatus === 'archived' && (
                          <button
                            onClick={() => handleStatusChange(item.id, 'draft')}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent shadow-sm text-xs font-medium rounded text-white bg-primary-600 hover:bg-primary-700"
                          >
                            Restore
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="p-12 text-center">
                <IconComponent className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">
                  No {currentConfig?.label.toLowerCase()} items
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  {currentConfig?.description}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Info Panel */}
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <QueueListIcon className="h-5 w-5 text-blue-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">
                Using Content Queues
              </h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>
                  Content queues organize your work by workflow status. Use tabs to
                  switch between Draft, In Review, Published, and Archived content
                  across all content types.
                </p>
                <p className="mt-2">
                  <strong>Quick actions:</strong> Approve content directly from the In
                  Review queue, submit drafts for review, or restore archived content.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
