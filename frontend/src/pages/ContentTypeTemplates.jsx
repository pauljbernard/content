/**
 * Content Type Templates Gallery
 * Browse and import pre-built content type templates
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  AcademicCapIcon,
  ClipboardDocumentListIcon,
  BookOpenIcon,
  VideoCameraIcon,
  PuzzlePieceIcon,
  CubeIcon,
  CheckIcon,
} from '@heroicons/react/24/outline';
import {
  contentTypeTemplates,
  getTemplatesByCategory,
} from '../data/contentTypeTemplates';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

const TEMPLATE_ICONS = {
  'academic-cap': AcademicCapIcon,
  clipboard: ClipboardDocumentListIcon,
  book: BookOpenIcon,
  'book-open': BookOpenIcon,
  video: VideoCameraIcon,
  puzzle: PuzzlePieceIcon,
};

export default function ContentTypeTemplates() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedTemplate, setSelectedTemplate] = useState(null);

  // Group templates by category
  const templatesByCategory = getTemplatesByCategory();
  const categories = ['all', ...Object.keys(templatesByCategory).sort()];

  // Import template mutation
  const importMutation = useMutation({
    mutationFn: async (template) => {
      // Transform template to content type format
      const contentTypeData = {
        name: template.name,
        description: template.description,
        icon: template.icon,
        is_system: false,
        attributes: template.attributes,
      };

      // Create the content type first
      const newContentType = await contentTypesAPI.create(contentTypeData);

      // Check if any attributes have __SELF__ placeholder for self-referencing
      const hasSelfReference = template.attributes.some(
        attr => attr.config?.targetContentType === '__SELF__'
      );

      if (hasSelfReference) {
        // Replace __SELF__ with the actual content type ID
        const updatedAttributes = template.attributes.map(attr => {
          if (attr.config?.targetContentType === '__SELF__') {
            return {
              ...attr,
              config: {
                ...attr.config,
                targetContentType: newContentType.id,
              },
            };
          }
          return attr;
        });

        // Update the content type with corrected self-references
        await contentTypesAPI.update(newContentType.id, {
          attributes: updatedAttributes,
        });
      }

      return newContentType;
    },
    onSuccess: (newContentType, template) => {
      queryClient.invalidateQueries(['content-types']);
      toast.success(`"${template.name}" template imported successfully`);
      navigate(`/content-types/${newContentType.id}/edit`);
    },
    onError: (error, template) => {
      toast.error(
        `Failed to import template: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  const handleImportTemplate = (template) => {
    setSelectedTemplate(template);
    if (
      window.confirm(
        `Import "${template.name}" template? This will create a new content type that you can customize.`
      )
    ) {
      importMutation.mutate(template);
    }
  };

  // Filter templates by category
  const filteredTemplates =
    selectedCategory === 'all'
      ? contentTypeTemplates
      : templatesByCategory[selectedCategory] || [];

  const getIconComponent = (iconName) => {
    return TEMPLATE_ICONS[iconName] || CubeIcon;
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Content Type Templates
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Pre-built content type templates ready to use. Import a template and
            customize it to your needs.
          </p>
        </div>

        {/* Category Filter */}
        <div className="bg-white shadow rounded-lg p-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Filter by Category
          </label>
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  selectedCategory === category
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category.charAt(0).toUpperCase() + category.slice(1)}
                {category !== 'all' &&
                  ` (${templatesByCategory[category]?.length || 0})`}
              </button>
            ))}
          </div>
        </div>

        {/* Templates Grid */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filteredTemplates.map((template) => {
            const IconComponent = getIconComponent(template.icon);

            return (
              <div
                key={template.id}
                className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
              >
                <div className="p-6">
                  {/* Icon and Title */}
                  <div className="flex items-center mb-4">
                    <div className="flex-shrink-0">
                      <div className="h-12 w-12 rounded-md bg-primary-50 flex items-center justify-center">
                        <IconComponent className="h-6 w-6 text-primary-600" />
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
                  <p className="text-sm text-gray-500 mb-4 line-clamp-2">
                    {template.description}
                  </p>

                  {/* Attributes Count */}
                  <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                    <span>{template.attributes.length} attributes</span>
                  </div>

                  {/* Action Button */}
                  <button
                    onClick={() => handleImportTemplate(template)}
                    disabled={importMutation.isPending}
                    className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {importMutation.isPending &&
                    selectedTemplate?.id === template.id ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Importing...
                      </>
                    ) : (
                      <>
                        <CheckIcon className="h-5 w-5 mr-2" />
                        Import Template
                      </>
                    )}
                  </button>

                  {/* Expandable Details */}
                  <details className="mt-4">
                    <summary className="text-xs font-medium text-gray-700 cursor-pointer hover:text-primary-600">
                      View Attributes ({template.attributes.length})
                    </summary>
                    <div className="mt-2 space-y-2">
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
                          {attr.help_text && (
                            <div className="text-gray-500 mt-1">
                              {attr.help_text}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              </div>
            );
          })}
        </div>

        {filteredTemplates.length === 0 && (
          <div className="text-center py-12 bg-white shadow rounded-lg">
            <CubeIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              No templates found
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Try selecting a different category.
            </p>
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
                Using Templates
              </h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>
                  Templates provide a quick starting point for common content
                  types. After importing, you can customize the attributes,
                  add validation rules, and adjust to your specific needs.
                </p>
                <p className="mt-2">
                  <strong>Available templates:</strong> Lesson Plans,
                  Assessments, Learning Activities, Multimedia Resources,
                  Reading Passages, and Vocabulary Lists.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
