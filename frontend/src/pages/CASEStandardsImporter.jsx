/**
 * CASE Standards Importer - Import educational standards from CASE API endpoints
 * Part of the extensible importers system
 */
import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  CloudArrowUpIcon,
  CheckCircleIcon,
  XCircleIcon,
  MagnifyingGlassIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { standardsAPI } from '../services/api';
import { showSuccess, showError } from '../utils/toast';

export default function CASEStandardsImporter() {
  const navigate = useNavigate();

  // Form state
  const [formData, setFormData] = useState({
    source_type: 'case_network',
    source_location: '',
    format: 'case',
    name: '',
    short_name: '',
    code: '',
    type: 'state',
    subject: 'mathematics',
    source_organization: '',
    state: '',
    district: '',
    country: '',
  });

  const [importJobId, setImportJobId] = useState(null);
  const [selectedFramework, setSelectedFramework] = useState(null);
  const [frameworkSearchQuery, setFrameworkSearchQuery] = useState('');

  // Create import job mutation
  const createJobMutation = useMutation({
    mutationFn: (data) => standardsAPI.createImportJob(data),
    onSuccess: (data) => {
      setImportJobId(data.id);
      showSuccess('Import job created successfully');
    },
    onError: (error) => {
      showError('Failed to create import job', error);
    },
  });

  // Poll import job status
  const { data: jobStatus, refetch: refetchJobStatus } = useQuery({
    queryKey: ['import-job', importJobId],
    queryFn: () => standardsAPI.getImportJob(importJobId),
    enabled: !!importJobId,
    refetchInterval: (data) => {
      // Stop polling if job is completed or failed
      if (!data || data.status === 'completed' || data.status === 'failed') {
        return false;
      }
      // Poll every 2 seconds while running or queued
      return 2000;
    },
  });

  // Fetch CASE Network frameworks - manual trigger only
  const { data: frameworksData, isLoading: frameworksLoading, error: frameworksError, refetch: fetchFrameworks } = useQuery({
    queryKey: ['case-network-frameworks'],
    queryFn: () => standardsAPI.getCASENetworkFrameworks(),
    enabled: false, // Don't auto-fetch - require manual button click
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });

  const handleFetchFrameworks = () => {
    fetchFrameworks();
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFrameworkSelect = (framework) => {
    setSelectedFramework(framework);

    // Auto-populate form fields from selected framework
    setFormData(prev => ({
      ...prev,
      source_location: framework.uri,
      name: framework.title,
      short_name: framework.title.substring(0, 100), // Truncate if needed
      code: framework.identifier.substring(0, 50), // Use identifier as code
      subject: framework.subject,
      source_organization: framework.creator || 'CASE Network',
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Reset previous job status before creating new one
    setImportJobId(null);
    createJobMutation.mutate(formData);
  };

  // Navigate to standards list when import completes successfully
  useEffect(() => {
    if (jobStatus?.status === 'completed' && jobStatus?.standard_id) {
      showSuccess(`Import completed! ${jobStatus.standards_extracted} standards imported.`);
      setTimeout(() => {
        navigate('/standards');
      }, 2000);
    } else if (jobStatus?.status === 'failed') {
      showError(`Import failed: ${jobStatus.error_message || 'Unknown error'}`);
    }
  }, [jobStatus?.status, jobStatus?.standard_id, jobStatus?.standards_extracted, jobStatus?.error_message, navigate]);

  // Filter frameworks based on search query
  const filteredFrameworks = frameworksData?.frameworks?.filter(fw => {
    if (!frameworkSearchQuery) return true;
    const query = frameworkSearchQuery.toLowerCase();
    return (
      fw.title.toLowerCase().includes(query) ||
      fw.description?.toLowerCase().includes(query) ||
      fw.creator?.toLowerCase().includes(query) ||
      fw.subject?.toLowerCase().includes(query)
    );
  }) || [];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-6 w-6 text-green-500" />;
      case 'failed':
        return <XCircleIcon className="h-6 w-6 text-red-500" />;
      default:
        return <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>;
    }
  };

  // If import job is active, show progress
  if (importJobId && jobStatus) {
    return (
      <Layout>
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-6">
              {getStatusIcon(jobStatus.status)}
              <h2 className="ml-3 text-xl font-semibold text-gray-900">
                Import {
                  jobStatus.status === 'completed' ? 'Complete' :
                  jobStatus.status === 'failed' ? 'Failed' :
                  'In Progress'
                }
              </h2>
            </div>

            {/* Only show progress bar if import is still running */}
            {jobStatus.status !== 'completed' && jobStatus.status !== 'failed' && (
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">
                    {jobStatus.progress_message || 'Processing...'}
                  </span>
                  <span className="text-sm text-gray-600">
                    {jobStatus.progress_percentage}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${jobStatus.progress_percentage}%` }}
                  ></div>
                </div>
              </div>
            )}

            {jobStatus.status === 'completed' && (
              <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
                <div className="flex">
                  <CheckCircleIcon className="h-5 w-5 text-green-400" />
                  <div className="ml-3">
                    <p className="text-sm text-green-800">
                      Successfully imported {jobStatus.standards_extracted} standards
                    </p>
                  </div>
                </div>
              </div>
            )}

            {jobStatus.status === 'failed' && (
              <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
                <div className="flex">
                  <XCircleIcon className="h-5 w-5 text-red-400" />
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Import Failed</h3>
                    <p className="mt-2 text-sm text-red-700">
                      {jobStatus.error_message || 'An error occurred during import'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="flex space-x-3">
              {jobStatus.status === 'completed' && (() => {
                // Parse import_log to get content_instance_id
                try {
                  const importLog = typeof jobStatus.import_log === 'string'
                    ? JSON.parse(jobStatus.import_log)
                    : jobStatus.import_log;
                  const contentInstanceId = importLog?.content_instance_id;

                  if (contentInstanceId) {
                    // Get CASE Standard content type ID (hardcoded for now, could be fetched)
                    const caseStandardTypeId = '2c49a0f3-c785-4156-888d-e03119bd8d24';

                    return (
                      <button
                        onClick={() => navigate(`/content-types/${caseStandardTypeId}/instances/${contentInstanceId}`)}
                        className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                      >
                        View Standard
                      </button>
                    );
                  }
                } catch (e) {
                  console.error('Failed to parse import_log:', e);
                }
                return null;
              })()}
              {jobStatus.status === 'failed' && (
                <button
                  onClick={() => {
                    setImportJobId(null);
                    setSelectedFramework(null);
                  }}
                  className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                >
                  Try Again
                </button>
              )}
              <button
                onClick={() => navigate('/content')}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
              >
                Back to All Content
              </button>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  // Show import form
  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link
            to="/importers"
            className="inline-flex items-center text-sm text-primary-600 hover:text-primary-700 mb-4"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Importers
          </Link>

          <div className="flex items-center mb-2">
            <CloudArrowUpIcon className="h-8 w-8 text-primary-600 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">Import Standard</h1>
          </div>
          <p className="text-gray-600">
            Import educational standards from CASE Network, public CASE endpoints, PDF, XML, or other formats
          </p>
          <div className="mt-2 bg-blue-50 border-l-4 border-blue-400 p-3">
            <p className="text-sm text-blue-700">
              <strong>CASE Network:</strong> Connect to the 1EdTech CASE Network with OAuth2 authentication.
              Credentials must be configured in Secrets (secret name: <code className="bg-blue-100 px-1 rounded">case_network_key</code>).
            </p>
          </div>
        </div>

        {/* Import Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-6">
          {/* Source Information */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Source Information</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Source Type *
                </label>
                <select
                  name="source_type"
                  value={formData.source_type}
                  onChange={handleChange}
                  required
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="case_network">CASE Network (OAuth2 authenticated)</option>
                  <option value="url">URL (Public CASE endpoint)</option>
                  <option value="file">File Upload</option>
                  <option value="api">API Endpoint</option>
                  <option value="manual">Manual Entry</option>
                </select>
                <p className="mt-1 text-xs text-gray-500">
                  {formData.source_type === 'case_network'
                    ? 'CASE Network requires credentials stored in Secrets (secret name: case_network_key)'
                    : 'Select the type of source for your standards import'
                  }
                </p>
              </div>

              {/* Framework Selector for CASE Network */}
              {formData.source_type === 'case_network' && (
                <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-gray-900">
                      Select CASE Network Framework
                    </label>
                    <button
                      type="button"
                      onClick={handleFetchFrameworks}
                      disabled={frameworksLoading}
                      className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <ArrowPathIcon className={`h-4 w-4 mr-1 ${frameworksLoading ? 'animate-spin' : ''}`} />
                      {frameworksLoading ? 'Loading...' : 'Fetch Frameworks'}
                    </button>
                  </div>

                  {!frameworksLoading && !frameworksError && !frameworksData && (
                    <div className="bg-blue-50 border-l-4 border-blue-400 p-3">
                      <div className="text-sm text-blue-800">
                        <p className="font-medium">Click "Fetch Frameworks" to load available frameworks</p>
                        <p className="mt-1">
                          This will retrieve the list of available CASE frameworks from the CASE Network using your configured credentials.
                        </p>
                      </div>
                    </div>
                  )}

                  {frameworksLoading && (
                    <div className="flex items-center justify-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                      <span className="ml-3 text-sm text-gray-600">Loading available frameworks...</span>
                    </div>
                  )}

                  {frameworksError && (
                    <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3">
                      <div className="text-sm text-yellow-800">
                        <p className="font-medium">Framework list unavailable</p>
                        {frameworksError.response?.data?.detail && (
                          <p className="mt-2 text-red-700 font-mono text-xs bg-red-50 p-2 rounded">
                            Error: {frameworksError.response.data.detail}
                          </p>
                        )}
                        <p className="mt-1">
                          The CASE Network framework list could not be loaded. This might be because:
                        </p>
                        <ul className="mt-2 ml-4 list-disc space-y-1">
                          <li>Your credentials are incorrect (check Secrets)</li>
                          <li>The CASE Network API structure has changed</li>
                          <li>The CFDocuments endpoint is not available</li>
                        </ul>
                        <p className="mt-2 font-medium">
                          You can still import by entering the CASE Package URL manually in the Source Location field below.
                        </p>
                      </div>
                    </div>
                  )}

                  {!frameworksLoading && !frameworksError && frameworksData && (
                    <div className="space-y-3">
                      {/* Search box */}
                      <div className="relative">
                        <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                        <input
                          type="text"
                          value={frameworkSearchQuery}
                          onChange={(e) => setFrameworkSearchQuery(e.target.value)}
                          placeholder="Search frameworks by title, subject, or organization..."
                          className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>

                      {/* Framework list */}
                      <div className="max-h-96 overflow-y-auto border border-gray-300 rounded-md">
                        {filteredFrameworks.length === 0 ? (
                          <div className="p-4 text-center text-gray-500">
                            {frameworkSearchQuery ? 'No frameworks match your search' : 'No frameworks available'}
                          </div>
                        ) : (
                          <div className="divide-y divide-gray-200">
                            {filteredFrameworks.map((framework) => (
                              <button
                                key={framework.identifier}
                                type="button"
                                onClick={() => handleFrameworkSelect(framework)}
                                className={`w-full text-left p-4 hover:bg-indigo-50 transition-colors ${
                                  selectedFramework?.identifier === framework.identifier
                                    ? 'bg-indigo-50 border-l-4 border-indigo-600'
                                    : ''
                                }`}
                              >
                                <div className="flex items-start justify-between">
                                  <div className="flex-1">
                                    <h4 className="text-sm font-medium text-gray-900">
                                      {framework.title}
                                    </h4>
                                    {framework.description && (
                                      <p className="mt-1 text-xs text-gray-600 line-clamp-2">
                                        {framework.description}
                                      </p>
                                    )}
                                    <div className="mt-2 flex flex-wrap gap-2">
                                      {framework.creator && (
                                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                                          {framework.creator}
                                        </span>
                                      )}
                                      {framework.subject && framework.subject !== 'general' && (
                                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                                          {framework.subject}
                                        </span>
                                      )}
                                      {framework.adoptionStatus && (
                                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                                          {framework.adoptionStatus}
                                        </span>
                                      )}
                                    </div>
                                  </div>
                                  {selectedFramework?.identifier === framework.identifier && (
                                    <CheckCircleIcon className="h-5 w-5 text-indigo-600 flex-shrink-0 ml-2" />
                                  )}
                                </div>
                              </button>
                            ))}
                          </div>
                        )}
                      </div>

                      <p className="text-xs text-gray-500">
                        Showing {filteredFrameworks.length} of {frameworksData?.total || 0} frameworks
                      </p>
                    </div>
                  )}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Source Location {formData.source_type !== 'case_network' && '*'}
                  {formData.source_type === 'case_network' && !selectedFramework && (
                    <span className="text-xs text-gray-500 font-normal ml-1">(optional - select a framework above)</span>
                  )}
                </label>
                <input
                  type="text"
                  name="source_location"
                  value={formData.source_location}
                  onChange={handleChange}
                  required={formData.source_type !== 'case_network'}
                  readOnly={formData.source_type === 'case_network' && selectedFramework}
                  placeholder={
                    formData.source_type === 'case_network'
                      ? selectedFramework
                        ? 'Auto-populated from selected framework'
                        : 'https://casenetwork.1edtech.org/ims/case/v1p0/CFPackages/{id}'
                      : 'https://case.georgiastandards.org/ims/case/v1p0/CFPackages/{id}'
                  }
                  className={`block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500 ${
                    formData.source_type === 'case_network' && selectedFramework
                      ? 'bg-gray-100 cursor-not-allowed'
                      : ''
                  }`}
                />
                <p className="mt-1 text-xs text-gray-500">
                  {formData.source_type === 'case_network'
                    ? selectedFramework
                      ? '✓ Auto-populated from selected framework'
                      : 'Select a framework from the list above, or enter a CASE Network URL manually'
                    : 'URL, file path, or API endpoint for the standard source'
                  }
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Format *
                </label>
                <select
                  name="format"
                  value={formData.format}
                  onChange={handleChange}
                  required
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="case">CASE (IMS Global Standard)</option>
                  <option value="pdf">PDF Document</option>
                  <option value="html">HTML Document</option>
                  <option value="xml">XML Document</option>
                  <option value="json">JSON Format</option>
                  <option value="csv">CSV Spreadsheet</option>
                  <option value="manual">Manual Entry</option>
                </select>
              </div>
            </div>
          </div>

          {/* Standard Metadata */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Standard Metadata</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Full Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  placeholder="Texas Essential Knowledge and Skills - Mathematics"
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Short Name *
                </label>
                <input
                  type="text"
                  name="short_name"
                  value={formData.short_name}
                  onChange={handleChange}
                  required
                  placeholder="TEKS Mathematics"
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Unique Code *
                </label>
                <input
                  type="text"
                  name="code"
                  value={formData.code}
                  onChange={handleChange}
                  required
                  placeholder="TEKS-MATH-TX"
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Must be unique across all standards in the system
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Type *
                  </label>
                  <select
                    name="type"
                    value={formData.type}
                    onChange={handleChange}
                    required
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                  >
                    <option value="state">State</option>
                    <option value="national">National</option>
                    <option value="international">International</option>
                    <option value="district">District</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Subject *
                  </label>
                  <select
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    required
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                  >
                    <option value="mathematics">Mathematics</option>
                    <option value="ela">English Language Arts</option>
                    <option value="science">Science</option>
                    <option value="social_studies">Social Studies</option>
                    <option value="computer_science">Computer Science</option>
                    <option value="world_languages">World Languages</option>
                    <option value="fine_arts">Fine Arts</option>
                    <option value="physical_education">Physical Education</option>
                    <option value="health">Health</option>
                    <option value="career_technical_education">Career & Technical Education</option>
                    <option value="general">General (Cross-Curricular)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Source Organization *
                </label>
                <input
                  type="text"
                  name="source_organization"
                  value={formData.source_organization}
                  onChange={handleChange}
                  required
                  placeholder="Texas Education Agency"
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
              </div>

              {/* Geographic Scope */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    State (if applicable)
                  </label>
                  <input
                    type="text"
                    name="state"
                    value={formData.state}
                    onChange={handleChange}
                    placeholder="texas"
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    District (if applicable)
                  </label>
                  <input
                    type="text"
                    name="district"
                    value={formData.district}
                    onChange={handleChange}
                    placeholder="Austin ISD"
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Country (if applicable)
                  </label>
                  <input
                    type="text"
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                    placeholder="United States"
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-3 pt-6 border-t">
            <Link
              to="/importers"
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={createJobMutation.isPending}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {createJobMutation.isPending ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Creating...
                </>
              ) : (
                <>
                  <CloudArrowUpIcon className="h-5 w-5 mr-2" />
                  Start Import
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
