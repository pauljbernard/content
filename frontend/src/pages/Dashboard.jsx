/**
 * Dashboard page - role-specific home page
 */
import { useQuery } from '@tanstack/react-query';
import {
  BookOpenIcon,
  DocumentTextIcon,
  UsersIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';
import useAuthStore from '../store/authStore';
import { knowledgeAPI, contentAPI } from '../services/api';
import Layout from '../components/Layout';

export default function Dashboard() {
  const { user } = useAuthStore();

  const { data: kbStats } = useQuery({
    queryKey: ['knowledge-stats'],
    queryFn: knowledgeAPI.getStats,
  });

  const { data: myContent } = useQuery({
    queryKey: ['my-content'],
    queryFn: () => contentAPI.list({ author_id: user?.id }),
    enabled: ['author', 'editor'].includes(user?.role),
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
      name: 'Subjects',
      value: Object.keys(kbStats?.files_by_subject || {}).length,
      icon: UsersIcon,
      color: 'bg-purple-500',
    },
    {
      name: 'States',
      value: Object.keys(kbStats?.files_by_state || {}).length,
      icon: DocumentTextIcon,
      color: 'bg-orange-500',
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

        {/* Stats Grid */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
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
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
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

            <a
              href="/search"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <ChartBarIcon className="h-6 w-6 text-purple-600 mr-3" />
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
