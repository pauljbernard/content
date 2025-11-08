/**
 * Dashboard page - role-specific home page
 */
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  BookOpenIcon,
  DocumentTextIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  SparklesIcon,
  QueueListIcon,
  CodeBracketIcon,
  CubeIcon,
} from '@heroicons/react/24/outline';
import useAuthStore from '../store/authStore';
import { knowledgeAPI, contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

export default function Dashboard() {
  const { user } = useAuthStore();

  const { data: kbStats } = useQuery({
    queryKey: ['knowledge-stats'],
    queryFn: knowledgeAPI.getStats,
  });

  const { data: myContent } = useQuery({
    queryKey: ['my-content'],
    queryFn: () => contentTypesAPI.listAllInstances({ author_id: user?.id, limit: 10000 }),
    enabled: ['author', 'editor'].includes(user?.role),
  });

  const { data: needsRevision } = useQuery({
    queryKey: ['needs-revision'],
    queryFn: () => contentTypesAPI.listAllInstances({ status: 'needs_revision', author_id: user?.id, limit: 10000 }),
    enabled: user?.role === 'author',
  });

  // Fetch content stats
  const { data: contentStats } = useQuery({
    queryKey: ['content-stats'],
    queryFn: contentTypesAPI.getStats,
  });

  const statCards = [
    {
      name: 'Knowledge Files',
      value: kbStats?.total_files || '303',
      icon: BookOpenIcon,
      color: 'bg-blue-500',
    },
    {
      name: 'Total Size',
      value: `${kbStats?.total_size_mb || '0'} MB`,
      icon: ChartBarIcon,
      color: 'bg-green-500',
    },
    {
      name: 'Content Types',
      value: contentStats?.total_content_types || '0',
      icon: CubeIcon,
      color: 'bg-purple-500',
    },
    {
      name: 'Content Instances',
      value: contentStats?.total_instances || '0',
      icon: DocumentTextIcon,
      color: 'bg-cyan-500',
    },
    {
      name: 'Agents',
      value: '22',
      icon: SparklesIcon,
      color: 'bg-violet-500',
    },
    {
      name: 'Workflows',
      value: '0',
      icon: QueueListIcon,
      color: 'bg-amber-500',
    },
    {
      name: 'Skills',
      value: '92',
      icon: CodeBracketIcon,
      color: 'bg-rose-500',
    },
  ];

  return (
    <Layout>
      <div className="space-y-6">
        {/* Welcome Header */}
        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900">
            Welcome back, {user?.full_name || user?.email}!
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Role: <span className="font-medium">{user?.role}</span>
          </p>
        </div>

        {/* Needs Revision Alert */}
        {user?.role === 'author' && needsRevision && needsRevision.length > 0 && (
          <div className="bg-orange-50 border-l-4 border-orange-400 p-4 rounded-lg shadow">
            <div className="flex">
              <div className="flex-shrink-0">
                <ExclamationTriangleIcon className="h-5 w-5 text-orange-400" />
              </div>
              <div className="ml-3 flex-1">
                <h3 className="text-sm font-medium text-orange-800">
                  {needsRevision.length} {needsRevision.length === 1 ? 'item' : 'items'} need revision
                </h3>
                <div className="mt-2 text-sm text-orange-700">
                  <p className="mb-3">
                    The following content has received feedback from reviewers. Please review the comments and make necessary changes, then resubmit for review.
                  </p>
                  <ul className="space-y-2">
                    {needsRevision.map((content) => (
                      <li key={content.id} className="flex items-center justify-between bg-white rounded-md p-3">
                        <div className="flex-1">
                          <p className="font-medium text-gray-900">{content.title}</p>
                          <p className="text-xs text-gray-500 mt-1">
                            {content.content_type} • {content.subject}
                          </p>
                        </div>
                        <Link
                          to={`/content/${content.id}`}
                          className="ml-4 inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-orange-700 bg-orange-100 hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
                        >
                          View Feedback & Edit
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {statCards.map((stat) => (
            <div
              key={stat.name}
              className="bg-white overflow-hidden shadow rounded-lg"
            >
              <div className="p-5">
                <div className="flex items-center">
                  <div className={`flex-shrink-0 ${stat.color} rounded-md p-3`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        {stat.name}
                      </dt>
                      <dd className="text-2xl font-semibold text-gray-900">
                        {stat.value}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Role-specific content */}
        {['author', 'editor', 'knowledge_engineer'].includes(user?.role) && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              My Recent Content
            </h2>
            {myContent && myContent.length > 0 ? (
              <div className="space-y-3">
                {myContent.slice(0, 5).map((content) => (
                  <div
                    key={content.id}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-gray-900">
                        {content.title}
                      </p>
                      <p className="text-sm text-gray-500">
                        {content.content_type} • {content.subject}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 text-xs font-medium rounded-full ${
                        content.status === 'published'
                          ? 'bg-green-100 text-green-800'
                          : content.status === 'in_review'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {content.status}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">
                No content yet. Create your first lesson or assessment!
              </p>
            )}
          </div>
        )}

        {/* Quick Actions */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <a
              href="/knowledge"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <BookOpenIcon className="h-6 w-6 text-primary-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">Browse Knowledge</p>
                <p className="text-sm text-gray-500">
                  Explore Pre-K-12 frameworks
                </p>
              </div>
            </a>

            {['author', 'editor', 'knowledge_engineer'].includes(
              user?.role
            ) && (
              <a
                href="/content/new"
                className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <DocumentTextIcon className="h-6 w-6 text-green-600 mr-3" />
                <div>
                  <p className="font-medium text-gray-900">Create Content</p>
                  <p className="text-sm text-gray-500">New lesson or assessment</p>
                </div>
              </a>
            )}

            {['author', 'editor', 'knowledge_engineer'].includes(
              user?.role
            ) && (
              <a
                href="/agents"
                className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <SparklesIcon className="h-6 w-6 text-purple-600 mr-3" />
                <div>
                  <p className="font-medium text-gray-900">AI Agents</p>
                  <p className="text-sm text-gray-500">5-10x faster with AI</p>
                </div>
              </a>
            )}

            <a
              href="/search"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <ChartBarIcon className="h-6 w-6 text-indigo-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">Search</p>
                <p className="text-sm text-gray-500">Find files and content</p>
              </div>
            </a>
          </div>
        </div>

        {/* Knowledge Base Categories */}
        {kbStats?.files_by_category && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Knowledge Base by Category
            </h2>
            <div className="space-y-2">
              {Object.entries(kbStats.files_by_category).map(
                ([category, count]) => (
                  <div
                    key={category}
                    className="flex justify-between items-center"
                  >
                    <span className="text-gray-700 capitalize">
                      {category.replace('-', ' ')}
                    </span>
                    <span className="text-gray-900 font-medium">
                      {count} files
                    </span>
                  </div>
                )
              )}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
