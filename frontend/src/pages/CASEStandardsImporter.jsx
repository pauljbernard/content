/**
 * CASE Standards Importer - Import educational standards from CASE API endpoints
 * Part of the extensible importers system
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  CloudArrowUpIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { standardsAPI } from '../services/api';
import { showSuccess, showError } from '../utils/toast';

export default function CASEStandardsImporter() {
  const navigate = useNavigate();

  // Form state
  const [formData, setFormData] = useState({
    source_type: 'url',
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
  const { data: jobStatus } = useQuery({
    queryKey: ['import-job', importJobId],
    queryFn: () => standardsAPI.getImportJob(importJobId),
    enabled: !!importJobId,
    refetchInterval: (data) => {
      if (data?.status === 'running' || data?.status === 'queued') {
        return 2000; // Poll every 2 seconds
      }
      return false;
    },
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    createJobMutation.mutate(formData);
  };

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
              {jobStatus.status === 'completed' && jobStatus.standard_id && (
                <button
                  onClick={() => navigate(`/standards/${jobStatus.standard_id}`)}
                  className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                >
                  View Standard
                </button>
              )}
              <button
                onClick={() => navigate('/standards')}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
              >
                Back to Standards
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
            Import educational standards from CASE, PDF, XML, or other formats
          </p>
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
                  <option value="url">URL</option>
                  <option value="file">File Upload</option>
                  <option value="api">API Endpoint</option>
                  <option value="manual">Manual Entry</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Source Location *
                </label>
                <input
                  type="text"
                  name="source_location"
                  value={formData.source_location}
                  onChange={handleChange}
                  required
                  placeholder="https://case.georgiastandards.org/api/v1/CFPackages/123abc"
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
                <p className="mt-1 text-xs text-gray-500">
                  URL, file path, or API endpoint for the standard source
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
