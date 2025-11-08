/**
 * Content Types page - List and manage flexible content type definitions
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  CubeIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

export default function ContentTypes() {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [showImportModal, setShowImportModal] = useState(false);
  const [importFile, setImportFile] = useState(null);

  // Fetch content types
  const { data: contentTypes, isLoading } = useQuery({
    queryKey: ['content-types'],
    queryFn: contentTypesAPI.list,
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: contentTypesAPI.delete,
    onSuccess: () => {
      queryClient.invalidateQueries(['content-types']);
      toast.success('Content type deleted successfully');
    },
    onError: (error) => {
      toast.error(
        `Failed to delete content type: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  // Import mutation
  const importMutation = useMutation({
    mutationFn: contentTypesAPI.importContentType,
    onSuccess: () => {
      queryClient.invalidateQueries(['content-types']);
      toast.success('Content type imported successfully');
      setShowImportModal(false);
      setImportFile(null);
    },
    onError: (error) => {
      toast.error(
        `Failed to import content type: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  const handleDelete = (contentTypeId, contentTypeName) => {
    if (
      window.confirm(
        `Are you sure you want to delete "${contentTypeName}"? This action cannot be undone.`
      )
    ) {
      deleteMutation.mutate(contentTypeId);
    }
  };

  const handleExport = async (contentType) => {
    try {
      const exportData = await contentTypesAPI.exportContentType(contentType.id);

      // Create and download JSON file
      const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: 'application/json',
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${contentType.name.toLowerCase().replace(/\s+/g, '-')}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      toast.success(`Content type "${contentType.name}" exported successfully`);
    } catch (error) {
      toast.error(`Failed to export: ${error.message}`);
    }
  };

  const handleImportSubmit = async () => {
    if (!importFile) {
      toast.error('Please select a file to import');
      return;
    }

    try {
      const text = await importFile.text();
      const importData = JSON.parse(text);
      importMutation.mutate(importData);
    } catch (error) {
      toast.error(`Invalid JSON file: ${error.message}`);
    }
  };

  // Filter content types by search term
  const filteredContentTypes = contentTypes?.filter((ct) =>
    ct.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Content Types</h1>
            <p className="mt-1 text-sm text-gray-500">
              Define flexible content schemas for any type of educational content
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setShowImportModal(true)}
              className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <ArrowUpTrayIcon className="h-5 w-5 mr-2" />
              Import
            </button>
            <Link
              to="/content-types/new"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              New Content Type
            </Link>
          </div>
        </div>

        {/* Search */}
        <div className="bg-white shadow rounded-lg p-4">
          <input
            type="text"
            placeholder="Search content types..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        {/* Content Types Grid */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p className="mt-2 text-sm text-gray-500">Loading content types...</p>
          </div>
        ) : filteredContentTypes && filteredContentTypes.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filteredContentTypes.map((contentType) => (
              <div
                key={contentType.id}
                className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
              >
                <div className="p-6">
                  {/* Icon and Title */}
                  <div className="flex items-center mb-4">
                    <div className="flex-shrink-0">
                      {contentType.icon ? (
                        <div className="h-12 w-12 rounded-md bg-primary-50 flex items-center justify-center">
                          <CubeIcon className="h-6 w-6 text-primary-600" />
                        </div>
                      ) : (
                        <div className="h-12 w-12 rounded-md bg-gray-100 flex items-center justify-center">
                          <CubeIcon className="h-6 w-6 text-gray-400" />
                        </div>
                      )}
                    </div>
                    <div className="ml-4 flex-1">
                      <h3 className="text-lg font-medium text-gray-900">
                        {contentType.name}
                      </h3>
                      {contentType.is_system && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                          System
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Description */}
                  {contentType.description && (
                    <p className="text-sm text-gray-500 mb-4 line-clamp-2">
                      {contentType.description}
                    </p>
                  )}

                  {/* Metadata */}
                  <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                    <span>{contentType.attributes.length} attributes</span>
                    <span>{contentType.instance_count || 0} instances</span>
                  </div>

                  {/* Actions */}
                  <div className="grid grid-cols-2 gap-2">
                    <Link
                      to={`/content-types/${contentType.id}/instances`}
                      className="col-span-2 inline-flex justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      Instances
                    </Link>
                    <button
                      onClick={() => handleExport(contentType)}
                      className="inline-flex justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                      title="Export as JSON"
                    >
                      <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
                      Export
                    </button>
                    {!contentType.is_system ? (
                      <>
                        <Link
                          to={`/content-types/${contentType.id}/edit`}
                          className="inline-flex justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                          title="Edit"
                        >
                          <PencilIcon className="h-4 w-4 mr-1" />
                          Edit
                        </Link>
                        <button
                          onClick={() =>
                            handleDelete(contentType.id, contentType.name)
                          }
                          disabled={contentType.instance_count > 0}
                          className="col-span-2 inline-flex justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                          title={
                            contentType.instance_count > 0
                              ? 'Cannot delete content type with instances'
                              : 'Delete'
                          }
                        >
                          <TrashIcon className="h-4 w-4 mr-1" />
                          Delete
                        </button>
                      </>
                    ) : (
                      <div className="col-span-1"></div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-white shadow rounded-lg">
            <CubeIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              No content types found
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by creating a new content type.
            </p>
            <div className="mt-6">
              <Link
                to="/content-types/new"
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                New Content Type
              </Link>
            </div>
          </div>
        )}

        {/* Info Panel */}
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <CubeIcon className="h-5 w-5 text-blue-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">
                Flexible Content Modeling
              </h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>
                  Content types define the structure of your content. Each content type has attributes that determine what
                  fields instances of that type will have. This is similar to Contentful or Strapi.
                </p>
                <p className="mt-2">
                  <strong>Available attribute types:</strong> Text, Long Text, Rich Text, Number, Boolean, Date,
                  Choice, Reference, Media, JSON, URL, Email
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Import Modal */}
        {showImportModal && (
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Import Content Type
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select JSON File
                  </label>
                  <input
                    type="file"
                    accept=".json"
                    onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Upload a JSON file exported from another content type
                  </p>
                </div>
                <div className="flex items-center justify-end space-x-3">
                  <button
                    onClick={() => {
                      setShowImportModal(false);
                      setImportFile(null);
                    }}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleImportSubmit}
                    disabled={!importFile || importMutation.isPending}
                    className="px-4 py-2 bg-primary-600 text-white rounded-md text-sm font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {importMutation.isPending ? 'Importing...' : 'Import'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
