/**
 * Content Type Setup Page
 * Allows knowledge engineers to import core content types to replace the hardcoded Content model
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  AcademicCapIcon,
  ClipboardDocumentListIcon,
  PuzzlePieceIcon,
  BookOpenIcon,
  CheckCircleIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import { contentTypeTemplates } from '../data/contentTypeTemplates';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

const TEMPLATE_ICONS = {
  'academic-cap': AcademicCapIcon,
  'clipboard': ClipboardDocumentListIcon,
  'puzzle': PuzzlePieceIcon,
  'book-open': BookOpenIcon,
};

export default function ContentTypeSetup() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [importingAll, setImportingAll] = useState(false);
  const [importedTypes, setImportedTypes] = useState(new Set());

  // Fetch existing content types
  const { data: existingTypes, isLoading } = useQuery({
    queryKey: ['content-types'],
    queryFn: () => contentTypesAPI.list(),
  });

  // Import template mutation
  const importMutation = useMutation({
    mutationFn: (template) => {
      const contentTypeData = {
        name: template.name,
        description: template.description,
        icon: template.icon,
        is_system: false,
        attributes: template.attributes,
      };
      return contentTypesAPI.create(contentTypeData);
    },
    onSuccess: (newContentType, template) => {
      queryClient.invalidateQueries(['content-types']);
      setImportedTypes(prev => new Set([...prev, template.name]));
      toast.success(`${template.name} content type created successfully`);
    },
    onError: (error, template) => {
      toast.error(
        `Failed to create ${template.name}: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  // Check if a content type already exists
  const contentTypeExists = (templateName) => {
    if (!existingTypes) return false;
    return existingTypes.some(ct => ct.name === templateName);
  };

  // Import all four core content types
  const handleImportAll = async () => {
    console.log('[SETUP] handleImportAll called');
    console.log('[SETUP] contentTypeTemplates:', contentTypeTemplates);

    // Temporarily bypass confirmation for testing
    // if (!window.confirm(
    //   'This will create all four core content types (Lesson, Assessment, Activity, Guide) to replace the hardcoded Content model. Continue?'
    // )) {
    //   console.log('[SETUP] User cancelled import');
    //   return;
    // }

    console.log('[SETUP] Starting import...');
    setImportingAll(true);

    for (const template of contentTypeTemplates) {
      console.log(`[SETUP] Processing template: ${template.name}`);

      // Skip if already exists
      if (contentTypeExists(template.name)) {
        console.log(`[SETUP] ${template.name} already exists, skipping...`);
        continue;
      }

      try {
        console.log(`[SETUP] Importing ${template.name}...`);
        await importMutation.mutateAsync(template);
        console.log(`[SETUP] Successfully imported ${template.name}`);
        // Small delay between imports to avoid overwhelming the server
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error) {
        console.error(`[SETUP] Failed to import ${template.name}:`, error);
        // Continue with other imports even if one fails
      }
    }

    console.log('[SETUP] All imports complete');
    setImportingAll(false);
    toast.success('Core content types setup complete!');
  };

  // Import a single template
  const handleImportSingle = (template) => {
    if (contentTypeExists(template.name)) {
      toast.error(`${template.name} content type already exists`);
      return;
    }

    if (window.confirm(
      `Create ${template.name} content type with ${template.attributes.length} attributes?`
    )) {
      importMutation.mutate(template);
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  const allImported = contentTypeTemplates.every(t => contentTypeExists(t.name));

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Core Content Type Setup
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Import the four core content types to replace the hardcoded Content model
          </p>
        </div>

        {/* Status Banner */}
        {allImported ? (
          <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded-r-lg">
            <div className="flex">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-5 w-5 text-green-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">
                  All Core Content Types Imported
                </h3>
                <p className="mt-2 text-sm text-green-700">
                  All four core content types have been created. You can now start creating content instances.
                  The old hardcoded Content model can be migrated or phased out.
                </p>
                <div className="mt-3">
                  <button
                    onClick={() => navigate('/content-types')}
                    className="text-sm font-medium text-green-800 hover:text-green-900 underline"
                  >
                    View Content Types
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
            <div className="flex">
              <div className="flex-shrink-0">
                <ArrowPathIcon className="h-5 w-5 text-blue-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  Ready to Import Core Content Types
                </h3>
                <p className="mt-2 text-sm text-blue-700">
                  Click "Import All" to create all four content types at once, or import them individually below.
                </p>
                <div className="mt-3">
                  <button
                    onClick={handleImportAll}
                    disabled={importingAll || importMutation.isPending}
                    className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {importingAll ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Importing...
                      </>
                    ) : (
                      <>Import All Core Content Types</>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Templates Grid */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {contentTypeTemplates.map((template) => {
            const IconComponent = TEMPLATE_ICONS[template.icon] || BookOpenIcon;
            const exists = contentTypeExists(template.name);

            return (
              <div
                key={template.id}
                className={`bg-white overflow-hidden shadow rounded-lg ${
                  exists ? 'ring-2 ring-green-500' : ''
                }`}
              >
                <div className="p-6">
                  {/* Status Badge */}
                  {exists && (
                    <div className="mb-3">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                        <CheckCircleIcon className="h-3 w-3 mr-1" />
                        Imported
                      </span>
                    </div>
                  )}

                  {/* Icon and Title */}
                  <div className="flex items-center mb-4">
                    <div className="flex-shrink-0">
                      <div className={`h-12 w-12 rounded-md flex items-center justify-center ${
                        exists ? 'bg-green-50' : 'bg-primary-50'
                      }`}>
                        <IconComponent className={`h-6 w-6 ${
                          exists ? 'text-green-600' : 'text-primary-600'
                        }`} />
                      </div>
                    </div>
                    <div className="ml-4 flex-1">
                      <h3 className="text-lg font-medium text-gray-900">
                        {template.name}
                      </h3>
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                        {template.category}
                      </span>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-gray-500 mb-4 line-clamp-3">
                    {template.description}
                  </p>

                  {/* Attributes Count */}
                  <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                    <span>{template.attributes.length} attributes</span>
                  </div>

                  {/* Action Button */}
                  <button
                    onClick={() => handleImportSingle(template)}
                    disabled={exists || importMutation.isPending || importingAll}
                    className={`w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed ${
                      exists
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-primary-600 hover:bg-primary-700 focus:ring-primary-500'
                    }`}
                  >
                    {exists ? 'Already Imported' : 'Import'}
                  </button>

                  {/* Expandable Details */}
                  <details className="mt-4">
                    <summary className="text-xs font-medium text-gray-700 cursor-pointer hover:text-primary-600">
                      View Attributes ({template.attributes.length})
                    </summary>
                    <div className="mt-2 space-y-2 max-h-48 overflow-y-auto">
                      {template.attributes.map((attr) => (
                        <div
                          key={attr.name}
                          className="text-xs p-2 bg-gray-50 rounded"
                        >
                          <div className="font-medium text-gray-900">
                            {attr.label || attr.name}
                            {attr.required && (
                              <span className="text-red-500 ml-1">*</span>
                            )}
                          </div>
                          <div className="text-gray-600">
                            Type: {attr.type}
                          </div>
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              </div>
            );
          })}
        </div>

        {/* Next Steps */}
        {allImported && (
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Next Steps
            </h3>
            <div className="space-y-3">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-6 w-6 rounded-full bg-primary-100 text-primary-600 text-sm font-medium">
                    1
                  </div>
                </div>
                <p className="ml-3 text-sm text-gray-700">
                  <strong>Create content instances:</strong> Go to the Content Types page and start creating lessons, assessments, activities, and guides
                </p>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-6 w-6 rounded-full bg-primary-100 text-primary-600 text-sm font-medium">
                    2
                  </div>
                </div>
                <p className="ml-3 text-sm text-gray-700">
                  <strong>Migrate existing content (optional):</strong> If you have content in the old Content model, use the migration tools to convert them to instances
                </p>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-6 w-6 rounded-full bg-primary-100 text-primary-600 text-sm font-medium">
                    3
                  </div>
                </div>
                <p className="ml-3 text-sm text-gray-700">
                  <strong>Customize content types:</strong> You can edit these content types to add custom fields or modify existing ones to fit your needs
                </p>
              </div>
            </div>
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => navigate('/content-types')}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Go to Content Types
              </button>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
