/**
 * Content List page - view and manage content
 */
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  PlusIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from '@heroicons/react/24/outline';
import { contentAPI } from '../services/api';
import useAuthStore from '../store/authStore';
import Layout from '../components/Layout';
import EmptyState from '../components/EmptyState';
import { SkeletonList } from '../components/LoadingSkeleton';

export default function ContentList() {
  const { user } = useAuthStore();
  const [filters, setFilters] = useState({
    status: '',
    content_type: '',
    subject: '',
    grade_level: '',
  });
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  const { data: response, isLoading } = useQuery({
    queryKey: ['content', filters, page, pageSize],
    queryFn: () => {
      const params = {
        ...filters,
        skip: (page - 1) * pageSize,
        limit: pageSize,
      };
      console.log('Fetching content with params:', params);
      return contentAPI.list(params);
    },
    keepPreviousData: false,
    staleTime: 0,
    cacheTime: 0,
    refetchOnMount: 'always',
  });

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
    setPage(1); // Reset to first page when filters change
  };

  const handlePageSizeChange = (newSize) => {
    const numSize = Number(newSize);
    console.log('Page size changing from', pageSize, 'to', numSize);
    setPageSize(numSize);
    setPage(1); // Reset to first page when page size changes
  };

  const handleSearchChange = (value) => {
    setSearch(value);
    setPage(1); // Reset to first page when search changes
  };

  // Get data from response - backend now provides all pagination metadata
  const content = response?.items || [];
  const total = response?.total || 0;
  const totalPages = response?.total_pages || 1;
  const currentPage = response?.page || page;
  const hasPrevious = response?.has_previous || false;
  const hasNext = response?.has_next || false;
  const currentPageSize = response?.page_size || pageSize;

  // Calculate display range
  const startItem = total === 0 ? 0 : (currentPage - 1) * currentPageSize + 1;
  const endItem = Math.min(currentPage * currentPageSize, total);

  // Debug logging
  console.log('Response data:', {
    itemsCount: content.length,
    total,
    page: currentPage,
    totalPages,
    pageSize: currentPageSize,
    hasPrevious,
    hasNext,
  });

  const getStatusColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      in_review: 'bg-yellow-100 text-yellow-800',
      needs_revision: 'bg-orange-100 text-orange-800',
      approved: 'bg-green-100 text-green-800',
      published: 'bg-blue-100 text-blue-800',
      archived: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Content</h1>
            <p className="mt-1 text-sm text-gray-500">
              Manage lessons, assessments, and activities
            </p>
          </div>
          {['author', 'editor', 'knowledge_engineer'].includes(user?.role) && (
            <Link
              to="/content/new"
              className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              New Content
            </Link>
          )}
        </div>

        {/* Filters */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center mb-4">
            <FunnelIcon className="h-5 w-5 text-gray-400 mr-2" />
            <h2 className="text-lg font-medium text-gray-900">Filters</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="md:col-span-4">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by title or subject..."
                  value={search}
                  onChange={(e) => handleSearchChange(e.target.value)}
                  className="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">All Statuses</option>
                <option value="draft">Draft</option>
                <option value="in_review">In Review</option>
                <option value="needs_revision">Needs Revision</option>
                <option value="approved">Approved</option>
                <option value="published">Published</option>
                <option value="archived">Archived</option>
              </select>
            </div>

            {/* Type Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                value={filters.content_type}
                onChange={(e) =>
                  handleFilterChange('content_type', e.target.value)
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">All Types</option>
                <option value="lesson">Lesson</option>
                <option value="assessment">Assessment</option>
                <option value="activity">Activity</option>
                <option value="guide">Guide</option>
              </select>
            </div>

            {/* Subject Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Subject
              </label>
              <select
                value={filters.subject}
                onChange={(e) => handleFilterChange('subject', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">All Subjects</option>
                <option value="mathematics">Mathematics</option>
                <option value="ela">ELA</option>
                <option value="science">Science</option>
                <option value="social-studies">Social Studies</option>
                <option value="world-languages">World Languages</option>
                <option value="fine-arts">Fine Arts</option>
                <option value="physical-education">Physical Education</option>
              </select>
            </div>

            {/* Grade Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Grade Level
              </label>
              <select
                value={filters.grade_level}
                onChange={(e) =>
                  handleFilterChange('grade_level', e.target.value)
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">All Grades</option>
                <option value="K">Kindergarten</option>
                <option value="1">Grade 1</option>
                <option value="2">Grade 2</option>
                <option value="3">Grade 3</option>
                <option value="4">Grade 4</option>
                <option value="5">Grade 5</option>
                <option value="6">Grade 6</option>
                <option value="7">Grade 7</option>
                <option value="8">Grade 8</option>
                <option value="9">Grade 9</option>
                <option value="10">Grade 10</option>
                <option value="11">Grade 11</option>
                <option value="12">Grade 12</option>
              </select>
            </div>
          </div>
        </div>

        {/* Content List */}
        <div className="bg-white shadow rounded-lg overflow-hidden">
          {isLoading ? (
            <div className="p-6">
              <SkeletonList items={5} />
            </div>
          ) : content && content.length > 0 ? (
            <div className="divide-y divide-gray-200">
              {content.map((item) => (
                <Link
                  key={item.id}
                  to={`/content/${item.id}`}
                  className="block hover:bg-gray-50 transition-colors"
                >
                  <div className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-medium text-gray-900 truncate">
                          {item.title}
                        </h3>
                        <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                          <span className="capitalize">{item.content_type}</span>
                          <span>•</span>
                          <span>{item.subject}</span>
                          {item.grade_level && (
                            <>
                              <span>•</span>
                              <span>Grade {item.grade_level}</span>
                            </>
                          )}
                          {item.state && (
                            <>
                              <span>•</span>
                              <span className="uppercase">{item.state}</span>
                            </>
                          )}
                        </div>
                        <div className="mt-2 text-sm text-gray-500">
                          Updated {new Date(item.updated_at).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="ml-4 flex-shrink-0">
                        <span
                          className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                            item.status
                          )}`}
                        >
                          {item.status.replace('_', ' ')}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <EmptyState
              icon="📝"
              title="No content found"
              message={
                search || Object.values(filters).some((f) => f !== '')
                  ? 'No content matches your search or filter criteria. Try adjusting your filters.'
                  : 'Get started by creating your first piece of content'
              }
              action={
                ['author', 'editor', 'knowledge_engineer'].includes(user?.role)
                  ? {
                      label: 'Create Content',
                      onClick: () => (window.location.href = '/content/new'),
                      icon: <PlusIcon className="h-5 w-5" />,
                    }
                  : undefined
              }
            />
          )}
        </div>

        {/* Pagination Controls */}
        {!isLoading && total > 0 && (
          <div className="bg-white shadow rounded-lg px-6 py-4">
            <div className="flex items-center justify-between">
              {/* Page Info and Size Selector */}
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-700">
                  Showing <span className="font-medium">{startItem}</span> to{' '}
                  <span className="font-medium">{endItem}</span> of{' '}
                  <span className="font-medium">{total}</span> results
                </div>
                <div className="flex items-center space-x-2">
                  <label className="text-sm text-gray-700">Items per page:</label>
                  <select
                    value={pageSize}
                    onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                    className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
                  >
                    <option value={5}>5</option>
                    <option value={10}>10</option>
                    <option value={20}>20</option>
                    <option value={50}>50</option>
                    <option value={100}>100</option>
                  </select>
                </div>
              </div>

              {/* Page Navigation */}
              <div className="flex items-center space-x-2">
                {/* Previous Button */}
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={!hasPrevious}
                  className={`inline-flex items-center px-3 py-2 border rounded-md text-sm font-medium ${
                    !hasPrevious
                      ? 'border-gray-200 text-gray-400 cursor-not-allowed'
                      : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <ChevronLeftIcon className="h-5 w-5" />
                  Previous
                </button>

                {/* Page Numbers */}
                <div className="hidden md:flex items-center space-x-1">
                  {[...Array(Math.min(totalPages, 7))].map((_, idx) => {
                    let pageNum;
                    if (totalPages <= 7) {
                      pageNum = idx + 1;
                    } else if (currentPage <= 4) {
                      pageNum = idx + 1;
                    } else if (currentPage >= totalPages - 3) {
                      pageNum = totalPages - 6 + idx;
                    } else {
                      pageNum = currentPage - 3 + idx;
                    }

                    return (
                      <button
                        key={pageNum}
                        onClick={() => setPage(pageNum)}
                        className={`px-3 py-2 border rounded-md text-sm font-medium ${
                          currentPage === pageNum
                            ? 'bg-primary-600 text-white border-primary-600'
                            : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                </div>

                {/* Current Page (Mobile) */}
                <div className="md:hidden text-sm text-gray-700">
                  Page {currentPage} of {totalPages}
                </div>

                {/* Next Button */}
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={!hasNext}
                  className={`inline-flex items-center px-3 py-2 border rounded-md text-sm font-medium ${
                    !hasNext
                      ? 'border-gray-200 text-gray-400 cursor-not-allowed'
                      : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Next
                  <ChevronRightIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
