/**
 * All Content Instances Page
 * Shows all content instances from all content types in one unified view
 * Supports both linear table view and hierarchical tree view
 */
import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  FunnelIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';
import TreeView from '../components/TreeView';

export default function AllContent() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [contentTypeFilter, setContentTypeFilter] = useState('all');
  const [page, setPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [selectedNodeId, setSelectedNodeId] = useState(null);

  // Fetch all content types for filter dropdown
  const { data: contentTypesData } = useQuery({
    queryKey: ['content-types'],
    queryFn: () => contentTypesAPI.list(),
  });

  const contentTypes = contentTypesData?.items || contentTypesData || [];

  // Find the selected content type to check if it's hierarchical
  const selectedContentType = contentTypes.find(ct => ct.id === contentTypeFilter);
  const isHierarchical = selectedContentType?.is_hierarchical || false;
  const hierarchyConfig = selectedContentType?.hierarchy_config;

  // Debug logging
  console.log('AllContent Debug:', {
    contentTypeFilter,
    selectedContentType: selectedContentType ? {
      id: selectedContentType.id,
      name: selectedContentType.name,
      is_hierarchical: selectedContentType.is_hierarchical,
      hierarchy_config: selectedContentType.hierarchy_config
    } : null,
    isHierarchical,
    totalContentTypes: contentTypes.length
  });

  // Fetch all content instances with pagination (for non-hierarchical types)
  const { data: paginatedData, isLoading } = useQuery({
    queryKey: ['all-content-instances', statusFilter, contentTypeFilter, searchTerm, page, itemsPerPage],
    queryFn: () => {
      const params = {
        skip: (page - 1) * itemsPerPage,
        limit: itemsPerPage,
      };
      if (statusFilter !== 'all') params.status = statusFilter;
      if (contentTypeFilter !== 'all') params.content_type_id = contentTypeFilter;
      if (searchTerm) params.search = searchTerm;
      return contentTypesAPI.listAllInstances(params);
    },
    enabled: !isHierarchical || contentTypeFilter === 'all', // Only fetch when not in hierarchical mode
  });

  // Fetch tree data for hierarchical content types
  const { data: treeData, isLoading: isLoadingTree } = useQuery({
    queryKey: ['content-tree', contentTypeFilter, page, itemsPerPage],
    queryFn: () => {
      return contentTypesAPI.listInstancesTree(contentTypeFilter, {
        parent_id: null, // Get root nodes
        skip: (page - 1) * itemsPerPage,
        limit: itemsPerPage,
      });
    },
    enabled: isHierarchical && contentTypeFilter !== 'all', // Only fetch when hierarchical type is selected
  });

  // Function to fetch children for a node
  const fetchChildren = async (parentIdentifier) => {
    const response = await contentTypesAPI.listInstancesTree(contentTypeFilter, {
      parent_id: parentIdentifier,
      skip: 0,
      limit: 100, // Load up to 100 children at once
    });
    return response.items || [];
  };

  const instances = paginatedData?.items || [];
  const treeNodes = treeData?.items || [];
  const total = isHierarchical ? (treeData?.total || 0) : (paginatedData?.total || 0);
  const totalPages = Math.ceil(total / itemsPerPage);
  const loading = isHierarchical ? isLoadingTree : isLoading;

  // Reset to page 1 when filters change
  useEffect(() => {
    setPage(1);
  }, [statusFilter, contentTypeFilter, searchTerm]);

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: contentTypesAPI.deleteInstance,
    onSuccess: () => {
      queryClient.invalidateQueries(['all-content-instances']);
      queryClient.invalidateQueries(['content-tree']); // Also invalidate tree view
      toast.success('Content deleted successfully');
    },
    onError: (error) => {
      toast.error(
        `Failed to delete content: ${
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

  // Bulk delete mutation
  const bulkDeleteMutation = useMutation({
    mutationFn: async (ids) => {
      // Delete each instance sequentially
      for (const id of ids) {
        await contentTypesAPI.deleteInstance(id);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['all-content-instances']);
      setSelectedIds(new Set());
      toast.success(`Successfully deleted ${selectedIds.size} items`);
    },
    onError: (error) => {
      toast.error(
        `Failed to delete items: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  // Selection handlers
  const toggleSelectAll = () => {
    if (selectedIds.size === instances.length && instances.length > 0) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(instances.map(i => i.id)));
    }
  };

  const toggleSelect = (id) => {
    const newSelected = new Set(selectedIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedIds(newSelected);
  };

  const handleBulkDelete = () => {
    if (selectedIds.size === 0) {
      toast.error('No items selected');
      return;
    }

    if (
      window.confirm(
        `Are you sure you want to delete ${selectedIds.size} items? This action cannot be undone.`
      )
    ) {
      bulkDeleteMutation.mutate(Array.from(selectedIds));
    }
  };

  // Clear selection when filters change
  useEffect(() => {
    setSelectedIds(new Set());
  }, [statusFilter, contentTypeFilter, searchTerm, page]);

  // Get display title for an instance
  const getInstanceTitle = (instance) => {
    return (
      instance.data?.title ||
      instance.data?.name ||
      instance.data?.label ||
      `Content ${instance.id.substring(0, 8)}`
    );
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800';
      case 'draft':
        return 'bg-yellow-100 text-yellow-800';
      case 'in_review':
        return 'bg-blue-100 text-blue-800';
      case 'archived':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-purple-100 text-purple-800';
    }
  };

  // Handle tree node click - navigate to instance detail
  const handleNodeClick = (node) => {
    setSelectedNodeId(node.id);
    navigate(`/content-types/${contentTypeFilter}/instances/${node.id}`);
  };

  if (loading) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p className="mt-2 text-sm text-gray-500">Loading content...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">All Content</h1>
            <p className="mt-1 text-sm text-gray-500">
              Manage all your content instances across all content types
            </p>
          </div>
          <Link
            to="/content-types"
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Create Content
          </Link>
        </div>

        {/* Bulk Actions Bar */}
        {selectedIds.size > 0 && (
          <div className="bg-indigo-50 border-l-4 border-indigo-400 p-4 rounded-r-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <p className="text-sm font-medium text-indigo-800">
                  {selectedIds.size} item{selectedIds.size !== 1 ? 's' : ''} selected
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => setSelectedIds(new Set())}
                  className="inline-flex items-center px-3 py-2 border border-indigo-300 rounded-md shadow-sm text-sm font-medium text-indigo-700 bg-white hover:bg-indigo-50"
                >
                  Clear Selection
                </button>
                <button
                  onClick={handleBulkDelete}
                  disabled={bulkDeleteMutation.isPending}
                  className="inline-flex items-center px-3 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <TrashIcon className="h-4 w-4 mr-2" />
                  {bulkDeleteMutation.isPending ? 'Deleting...' : 'Delete Selected'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white shadow rounded-lg p-4">
          <div className="flex items-center mb-3">
            <FunnelIcon className="h-5 w-5 text-gray-400 mr-2" />
            <h3 className="text-sm font-medium text-gray-900">Filters</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search
              </label>
              <input
                type="text"
                placeholder="Search content..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content Type
              </label>
              <select
                value={contentTypeFilter}
                onChange={(e) => setContentTypeFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="all">All Types</option>
                {contentTypes?.map((type) => (
                  <option key={type.id} value={type.id}>
                    {type.name}
                  </option>
                ))}
              </select>
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
                <option value="in_review">In Review</option>
                <option value="published">Published</option>
                <option value="archived">Archived</option>
              </select>
            </div>
          </div>
        </div>

        {/* Content Display - Tree View for Hierarchical, Table for Linear */}
        {isHierarchical && contentTypeFilter !== 'all' ? (
          /* Tree View for Hierarchical Content Types */
          treeNodes && treeNodes.length > 0 ? (
            <div className="space-y-4">
              <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
                <p className="text-sm text-blue-700">
                  <strong>Tree View:</strong> This content type is hierarchical. Click the arrows to expand/collapse nodes and load children on-demand.
                </p>
              </div>
              <TreeView
                contentTypeId={contentTypeFilter}
                hierarchyConfig={hierarchyConfig}
                initialNodes={treeNodes}
                onNodeClick={handleNodeClick}
                onDelete={handleDelete}
                selectedNodeId={selectedNodeId}
                fetchChildren={fetchChildren}
              />
            </div>
          ) : (
            <div className="bg-white shadow rounded-lg p-12 text-center">
              <p className="text-gray-500">No items found at the root level</p>
            </div>
          )
        ) : (
          /* Table View for Non-Hierarchical Content Types */
          instances && instances.length > 0 ? (
            <div className="bg-white shadow rounded-lg overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 w-12">
                    <input
                      type="checkbox"
                      checked={selectedIds.size === instances.length && instances.length > 0}
                      onChange={toggleSelectAll}
                      className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer"
                    />
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
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
                {instances.map((instance) => (
                  <tr key={instance.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 w-12">
                      <input
                        type="checkbox"
                        checked={selectedIds.has(instance.id)}
                        onChange={() => toggleSelect(instance.id)}
                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer"
                      />
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">
                        {getInstanceTitle(instance)}
                      </div>
                      <div className="text-xs text-gray-500">
                        ID: {instance.id.substring(0, 8)}...
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {instance.content_type.icon && (
                          <span className="mr-2 text-lg">
                            {instance.content_type.icon}
                          </span>
                        )}
                        <span className="text-sm text-gray-900">
                          {instance.content_type.name}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                          instance.status
                        )}`}
                      >
                        {instance.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(instance.updated_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end space-x-2">
                        <Link
                          to={`/content-types/${instance.content_type_id}/instances/${instance.id}`}
                          className="inline-flex items-center p-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
                          title="View"
                        >
                          <EyeIcon className="h-4 w-4" />
                        </Link>
                        <Link
                          to={`/content-types/${instance.content_type_id}/instances/${instance.id}/edit`}
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
                No content found
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Get started by creating a new content type and adding instances.
              </p>
              <div className="mt-6">
                <Link
                  to="/content-types"
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  <PlusIcon className="h-5 w-5 mr-2" />
                  Go to Content Types
                </Link>
              </div>
            </div>
          )
        )}

        {/* Pagination Controls */}
        {total > 0 && (
          <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 rounded-b-lg shadow">
            <div className="flex-1 flex justify-between sm:hidden">
              {/* Mobile pagination */}
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div className="flex items-center gap-4">
                <p className="text-sm text-gray-700">
                  Showing <span className="font-medium">{(page - 1) * itemsPerPage + 1}</span> to{' '}
                  <span className="font-medium">{Math.min(page * itemsPerPage, total)}</span> of{' '}
                  <span className="font-medium">{total}</span> results
                </p>
                <select
                  value={itemsPerPage}
                  onChange={(e) => {
                    setItemsPerPage(Number(e.target.value));
                    setPage(1);
                  }}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                >
                  <option value={25}>25 per page</option>
                  <option value={50}>50 per page</option>
                  <option value={100}>100 per page</option>
                  <option value={200}>200 per page</option>
                </select>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  {/* Previous button */}
                  <button
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span className="sr-only">Previous</span>
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                  {/* Page numbers */}
                  {[...Array(Math.min(totalPages, 5))].map((_, idx) => {
                    let pageNum;
                    if (totalPages <= 5) {
                      pageNum = idx + 1;
                    } else if (page <= 3) {
                      pageNum = idx + 1;
                    } else if (page >= totalPages - 2) {
                      pageNum = totalPages - 4 + idx;
                    } else {
                      pageNum = page - 2 + idx;
                    }
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setPage(pageNum)}
                        className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                          page === pageNum
                            ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                            : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                  {/* Next button */}
                  <button
                    onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                    disabled={page >= totalPages}
                    className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span className="sr-only">Next</span>
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
