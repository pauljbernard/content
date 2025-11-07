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

  const { data: content, isLoading } = useQuery({
    queryKey: ['content', filters],
    queryFn: () => contentAPI.list(filters),
  });

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const filteredContent = content?.filter(
    (item) =>
      search === '' ||
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.subject.toLowerCase().includes(search.toLowerCase())
  );

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
                  onChange={(e) => setSearch(e.target.value)}
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
          ) : filteredContent && filteredContent.length > 0 ? (
            <div className="divide-y divide-gray-200">
              {filteredContent.map((item) => (
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
      </div>
    </Layout>
  );
}
