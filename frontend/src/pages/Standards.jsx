/**
 * Standards page - Browse and manage educational standards
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ClipboardDocumentListIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  EyeIcon,
  FunnelIcon,
  TrashIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { standardsAPI } from '../services/api';
import EmptyState from '../components/EmptyState';
import { SkeletonList } from '../components/LoadingSkeleton';
import useAuthStore from '../store/authStore';

export default function Standards() {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // State
  const [typeFilter, setTypeFilter] = useState('');
  const [subjectFilter, setSubjectFilter] = useState('');
  const [stateFilter, setStateFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  // Build query params
  const queryParams = {};
  if (typeFilter) queryParams.type = typeFilter;
  if (subjectFilter) queryParams.subject = subjectFilter;
  if (stateFilter) queryParams.state = stateFilter;
  if (statusFilter) queryParams.status = statusFilter;
  if (searchQuery) queryParams.search = searchQuery;

  // Query
  const { data: standards, isLoading, error } = useQuery({
    queryKey: ['standards', queryParams],
    queryFn: () => standardsAPI.list(queryParams),
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: standardsAPI.delete,
    onSuccess: () => {
      queryClient.invalidateQueries(['standards']);
      toast.success('Standard deleted successfully');
    },
    onError: (error) => {
      toast.error(`Failed to delete standard: ${error.response?.data?.detail || error.message}`);
    },
  });

  const canImport = ['author', 'editor', 'knowledge_engineer'].includes(user?.role);
  const canDelete = ['editor', 'knowledge_engineer'].includes(user?.role);

  const handleDelete = async (standardId, standardName) => {
    // Direct delete without confirmation for now
    deleteMutation.mutate(standardId);
  };

  const getTypeBadgeColor = (type) => {
    const colors = {
      state: 'bg-blue-100 text-blue-800',
      national: 'bg-purple-100 text-purple-800',
      international: 'bg-green-100 text-green-800',
      district: 'bg-yellow-100 text-yellow-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  const getStatusBadgeColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      importing: 'bg-yellow-100 text-yellow-800',
      imported: 'bg-blue-100 text-blue-800',
      published: 'bg-green-100 text-green-800',
      archived: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center">
              <ClipboardDocumentListIcon className="h-8 w-8 text-primary-600 mr-3" />
              <h1 className="text-3xl font-bold text-gray-900">Educational Standards</h1>
            </div>
            {canImport && (
              <Link
                to="/standards/import"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Import Standard
              </Link>
            )}
          </div>
          <p className="text-sm text-gray-600">
            Browse and manage educational standards from various sources (TEKS, CCSS, NGSS, etc.)
          </p>
        </div>

        {/* Search and Filters */}
        <div className="mb-6 bg-white rounded-lg shadow p-4">
          {/* Search Bar */}
          <div className="mb-4">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Search standards by name, code, or description..."
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
            {(typeFilter || subjectFilter || stateFilter || statusFilter) && (
              <button
                onClick={() => {
                  setTypeFilter('');
                  setSubjectFilter('');
                  setStateFilter('');
                  setStatusFilter('');
                }}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                Clear Filters
              </button>
            )}
          </div>

          {/* Filters */}
          {showFilters && (
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                <select
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="">All Types</option>
                  <option value="state">State</option>
                  <option value="national">National</option>
                  <option value="international">International</option>
                  <option value="district">District</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
                <select
                  value={subjectFilter}
                  onChange={(e) => setSubjectFilter(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="">All Subjects</option>
                  <option value="mathematics">Mathematics</option>
                  <option value="ela">English Language Arts</option>
                  <option value="science">Science</option>
                  <option value="social_studies">Social Studies</option>
                  <option value="computer_science">Computer Science</option>
                  <option value="world_languages">World Languages</option>
                  <option value="fine_arts">Fine Arts</option>
                  <option value="physical_education">Physical Education</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
                <input
                  type="text"
                  value={stateFilter}
                  onChange={(e) => setStateFilter(e.target.value)}
                  placeholder="e.g., Texas, California"
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="">All Statuses</option>
                  <option value="draft">Draft</option>
                  <option value="importing">Importing</option>
                  <option value="imported">Imported</option>
                  <option value="published">Published</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Standards List */}
        {isLoading ? (
          <SkeletonList items={5} />
        ) : error ? (
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <p className="text-sm text-red-800">Failed to load standards: {error.message}</p>
          </div>
        ) : !standards || standards.length === 0 ? (
          <EmptyState
            icon="📚"
            title="No standards found"
            message="No standards match your current filters. Try adjusting your search or import a new standard."
            action={
              canImport ? {
                label: 'Import Standard',
                href: '/standards/import'
              } : null
            }
          />
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <ul className="divide-y divide-gray-200">
              {standards.map((standard) => (
                <li key={standard.id} className="hover:bg-gray-50">
                  <div className="px-6 py-4 flex items-center justify-between">
                    <Link to={`/standards/${standard.id}`} className="flex-1 min-w-0">
                      <div className="flex items-center mb-2">
                        <h3 className="text-lg font-semibold text-gray-900 truncate">
                          {standard.name}
                        </h3>
                        <span className={`ml-3 px-2.5 py-0.5 rounded-full text-xs font-medium ${getTypeBadgeColor(standard.type)}`}>
                          {standard.type}
                        </span>
                        <span className={`ml-2 px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeColor(standard.status)}`}>
                          {standard.status}
                        </span>
                      </div>
                      <div className="flex items-center text-sm text-gray-500 space-x-4">
                        <span className="font-medium text-primary-600">{standard.code}</span>
                        <span>•</span>
                        <span>{standard.subject.replace('_', ' ')}</span>
                        <span>•</span>
                        <span>{standard.source_organization}</span>
                        {standard.state && (
                          <>
                            <span>•</span>
                            <span className="capitalize">{standard.state}</span>
                          </>
                        )}
                        {standard.version && (
                          <>
                            <span>•</span>
                            <span>v{standard.version}</span>
                          </>
                        )}
                      </div>
                      <div className="mt-2 flex items-center text-sm text-gray-500">
                        <span>{standard.total_standards_count} standards</span>
                        {standard.grade_levels && standard.grade_levels.length > 0 && (
                          <>
                            <span className="mx-2">•</span>
                            <span>Grades: {standard.grade_levels.join(', ')}</span>
                          </>
                        )}
                      </div>
                    </Link>
                    <div className="ml-4 flex-shrink-0 flex items-center space-x-3">
                      <Link to={`/standards/${standard.id}`}>
                        <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                      </Link>
                      {canDelete && (
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            handleDelete(standard.id, standard.name);
                          }}
                          className="text-red-600 hover:text-red-800"
                          title="Delete standard"
                        >
                          <TrashIcon className="h-5 w-5" />
                        </button>
                      )}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Results Count */}
        {standards && standards.length > 0 && (
          <div className="mt-4 text-sm text-gray-500 text-center">
            Showing {standards.length} standard{standards.length !== 1 ? 's' : ''}
          </div>
        )}
      </div>
    </Layout>
  );
}
