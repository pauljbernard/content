/**
 * Importers Gallery
 * Central hub for all data import capabilities
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ClipboardDocumentListIcon,
  ArrowDownTrayIcon,
  CheckCircleIcon,
  DocumentArrowUpIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';

// Importer Registry
// Each importer defines what it imports, from where, and to which content type
const IMPORTERS = [
  {
    id: 'case-standards',
    name: 'CASE Standards Importer',
    icon: ClipboardDocumentListIcon,
    category: 'Standards & Frameworks',
    description: 'Import educational standards from IMS Global CASE (Competencies and Academic Standards Exchange) API endpoints. Supports hierarchical standards frameworks with full CASE-compliant metadata.',
    sourceType: 'CASE API',
    sourceDescription: 'IMS Global CASE v1.0 API endpoints',
    targetContentType: 'CASE Standard',
    features: [
      'Hierarchical parent-child relationships',
      'Full CASE metadata preservation',
      'Automatic education level mapping',
      'CFItem type normalization',
      'Supports all major standards frameworks (TEKS, CCSS, NGSS, etc.)',
    ],
    exampleSources: [
      'Georgia Standards of Excellence (case.georgiastandards.org)',
      'OpenSalt repositories',
      'State CASE API endpoints',
    ],
    status: 'active',
    lastUpdated: '2025-11-08',
  },
  // Future importers can be added here:
  // {
  //   id: 'csv-generic',
  //   name: 'CSV Data Importer',
  //   icon: DocumentArrowUpIcon,
  //   category: 'File Upload',
  //   description: 'Import structured data from CSV files with column mapping',
  //   sourceType: 'CSV Upload',
  //   targetContentType: 'Any',
  //   status: 'coming_soon',
  // },
];

export default function Importers() {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Extract unique categories
  const categories = ['all', ...new Set(IMPORTERS.map(i => i.category))];

  // Filter importers by category
  const filteredImporters = selectedCategory === 'all'
    ? IMPORTERS
    : IMPORTERS.filter(i => i.category === selectedCategory);

  const getStatusBadge = (status) => {
    const statusConfig = {
      active: { bg: 'bg-green-100', text: 'text-green-800', label: 'Active' },
      beta: { bg: 'bg-yellow-100', text: 'text-yellow-800', label: 'Beta' },
      coming_soon: { bg: 'bg-gray-100', text: 'text-gray-800', label: 'Coming Soon' },
    };

    const config = statusConfig[status] || statusConfig.active;

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
        {config.label}
      </span>
    );
  };

  const handleConfigureImporter = (importer) => {
    // Navigate to the specific importer's configuration page
    if (importer.id === 'case-standards') {
      navigate('/importers/case-standards');
    }
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <ArrowDownTrayIcon className="h-8 w-8 mr-3 text-primary-600" />
            Data Importers
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Import content and data from external sources into your knowledge base.
            Each importer handles a specific data format or API.
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
                {category === 'all' ? 'All Importers' : category}
                {category !== 'all' &&
                  ` (${IMPORTERS.filter(i => i.category === category).length})`}
              </button>
            ))}
          </div>
        </div>

        {/* Importers Grid */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {filteredImporters.map((importer) => {
            const IconComponent = importer.icon;
            const isActive = importer.status === 'active';

            return (
              <div
                key={importer.id}
                className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
              >
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-12 w-12 rounded-md bg-primary-50 flex items-center justify-center">
                          <IconComponent className="h-6 w-6 text-primary-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <h3 className="text-lg font-medium text-gray-900">
                          {importer.name}
                        </h3>
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 mt-1">
                          {importer.category}
                        </span>
                      </div>
                    </div>
                    {getStatusBadge(importer.status)}
                  </div>

                  {/* Description */}
                  <p className="text-sm text-gray-600 mb-4">
                    {importer.description}
                  </p>

                  {/* Source & Target Info */}
                  <div className="space-y-2 mb-4 text-sm">
                    <div className="flex items-start">
                      <span className="font-medium text-gray-700 w-24 flex-shrink-0">Source:</span>
                      <div>
                        <span className="text-gray-900">{importer.sourceType}</span>
                        {importer.sourceDescription && (
                          <p className="text-gray-500 text-xs mt-1">{importer.sourceDescription}</p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-start">
                      <span className="font-medium text-gray-700 w-24 flex-shrink-0">Target:</span>
                      <span className="text-gray-900">{importer.targetContentType}</span>
                    </div>
                  </div>

                  {/* Features */}
                  {importer.features && (
                    <div className="mb-4">
                      <h4 className="text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2">
                        Features
                      </h4>
                      <ul className="space-y-1">
                        {importer.features.slice(0, 3).map((feature, idx) => (
                          <li key={idx} className="flex items-start text-xs text-gray-600">
                            <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                            <span>{feature}</span>
                          </li>
                        ))}
                        {importer.features.length > 3 && (
                          <li className="text-xs text-gray-500 ml-6">
                            +{importer.features.length - 3} more...
                          </li>
                        )}
                      </ul>
                    </div>
                  )}

                  {/* Example Sources */}
                  {importer.exampleSources && (
                    <details className="mb-4">
                      <summary className="text-xs font-medium text-gray-700 cursor-pointer hover:text-primary-600">
                        Example Sources ({importer.exampleSources.length})
                      </summary>
                      <ul className="mt-2 space-y-1 ml-4">
                        {importer.exampleSources.map((source, idx) => (
                          <li key={idx} className="text-xs text-gray-600">
                            • {source}
                          </li>
                        ))}
                      </ul>
                    </details>
                  )}

                  {/* Action Button */}
                  <button
                    onClick={() => handleConfigureImporter(importer)}
                    disabled={!isActive}
                    className={`w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium ${
                      isActive
                        ? 'text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
                        : 'text-gray-400 bg-gray-100 cursor-not-allowed'
                    }`}
                  >
                    <ArrowDownTrayIcon className="h-5 w-5 mr-2" />
                    {isActive ? 'Configure & Import' : 'Coming Soon'}
                  </button>

                  {/* Last Updated */}
                  {importer.lastUpdated && isActive && (
                    <p className="text-xs text-gray-400 mt-2 text-center">
                      Last updated: {importer.lastUpdated}
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {filteredImporters.length === 0 && (
          <div className="text-center py-12 bg-white shadow rounded-lg">
            <ArrowDownTrayIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              No importers found
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
              <ArrowDownTrayIcon className="h-5 w-5 text-blue-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">
                About Data Importers
              </h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>
                  Data importers allow you to bring in content from external sources into
                  the Nova knowledge base. Each importer is specialized for a specific data
                  format or API protocol.
                </p>
                <p className="mt-2">
                  <strong>Need a custom importer?</strong> Importers are extensible and new
                  ones can be added for CSV files, JSON data, Google Sheets, or any other
                  data source your team needs.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
