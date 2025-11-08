/**
 * Agents page - Browse and invoke individual Professor Framework agents
 *
 * Provides UI for:
 * - Browsing all 22 available AI agents
 * - Filtering agents by category
 * - Configuring and invoking individual agents
 * - Monitoring agent execution progress
 * - Viewing and using agent results
 *
 * Note: For orchestrating multiple agents in sequence, see the Workflows page.
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import {
  SparklesIcon,
  BeakerIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
  ArrowPathIcon,
  AcademicCapIcon,
  ClipboardDocumentCheckIcon,
  ShieldCheckIcon,
  ChartBarIcon,
  EyeIcon,
  LightBulbIcon,
  UserGroupIcon,
  GlobeAltIcon,
  RocketLaunchIcon,
  BriefcaseIcon,
  CurrencyDollarIcon,
  CogIcon,
  KeyIcon,
  SquaresPlusIcon,
  FolderIcon,
  ClipboardIcon,
  CodeBracketSquareIcon,
  PresentationChartLineIcon,
  InformationCircleIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { agentsAPI, contentAPI } from '../services/api';
import useAuthStore from '../store/authStore';
import EmptyState from '../components/EmptyState';
import { SkeletonList } from '../components/LoadingSkeleton';
import { showSuccess, showError, showWarning } from '../utils/toast';

// Agent icon mapping (22 agents)
const AGENT_ICONS = {
  // Curriculum Design
  'curriculum-architect': BeakerIcon,
  'instructional-designer': LightBulbIcon,

  // Content Creation
  'content-developer': DocumentTextIcon,
  'assessment-designer': ClipboardDocumentCheckIcon,
  'adaptive-learning': ChartBarIcon,
  'platform-training': AcademicCapIcon,
  'corporate-training': BriefcaseIcon,

  // Quality Assurance
  'pedagogical-reviewer': AcademicCapIcon,
  'quality-assurance': CheckCircleIcon,
  'accessibility-validator': EyeIcon,
  'standards-compliance': ShieldCheckIcon,

  // Packaging & Validation
  'scorm-validator': CodeBracketSquareIcon,

  // Analytics
  'learning-analytics': PresentationChartLineIcon,
  'ab-testing': ChartBarIcon,

  // Project & Workflow Management
  'project-planning': ClipboardIcon,
  'review-workflow': ArrowPathIcon,
  'content-library': FolderIcon,

  // Technical & Operations
  'performance-optimization': RocketLaunchIcon,
  'rights-management': KeyIcon,

  // Business & Strategy
  'market-intelligence': CurrencyDollarIcon,
  'sales-enablement': CurrencyDollarIcon,

  // Internationalization
  'localization': GlobeAltIcon,
};

// Agent color mapping (22 agents)
const AGENT_COLORS = {
  // Curriculum Design
  'curriculum-architect': 'purple',
  'instructional-designer': 'yellow',

  // Content Creation
  'content-developer': 'blue',
  'assessment-designer': 'green',
  'adaptive-learning': 'cyan',
  'platform-training': 'teal',
  'corporate-training': 'slate',

  // Quality Assurance
  'pedagogical-reviewer': 'orange',
  'quality-assurance': 'emerald',
  'accessibility-validator': 'pink',
  'standards-compliance': 'indigo',

  // Packaging & Validation
  'scorm-validator': 'violet',

  // Analytics
  'learning-analytics': 'blue',
  'ab-testing': 'sky',

  // Project & Workflow Management
  'project-planning': 'gray',
  'review-workflow': 'amber',
  'content-library': 'lime',

  // Technical & Operations
  'performance-optimization': 'red',
  'rights-management': 'fuchsia',

  // Business & Strategy
  'market-intelligence': 'green',
  'sales-enablement': 'emerald',

  // Internationalization
  'localization': 'blue',
};

// Category definitions
const AGENT_CATEGORIES = [
  { id: 'all', name: 'All Agents', color: 'gray' },
  { id: 'curriculum-design', name: 'Curriculum Design', color: 'purple' },
  { id: 'content-creation', name: 'Content Creation', color: 'blue' },
  { id: 'quality-assurance', name: 'Quality Assurance', color: 'green' },
  { id: 'packaging', name: 'Packaging', color: 'violet' },
  { id: 'analytics', name: 'Analytics', color: 'cyan' },
  { id: 'project-management', name: 'Project Management', color: 'amber' },
  { id: 'technical', name: 'Technical', color: 'red' },
  { id: 'business', name: 'Business', color: 'emerald' },
  { id: 'internationalization', name: 'Internationalization', color: 'sky' },
];

export default function Agents() {
  const { user } = useAuthStore();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  // State
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Queries
  const { data: agents, isLoading: agentsLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: agentsAPI.list,
  });

  const { data: recentJobs } = useQuery({
    queryKey: ['agent-jobs'],
    queryFn: () => agentsAPI.listJobs(null, 10),
  });

  const getStatusColor = (status) => {
    const colors = {
      queued: 'bg-gray-100 text-gray-800',
      running: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      cancelled: 'bg-orange-100 text-orange-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return CheckCircleIcon;
      case 'running':
        return ArrowPathIcon;
      case 'failed':
        return XCircleIcon;
      case 'queued':
        return ClockIcon;
      default:
        return ClockIcon;
    }
  };

  // Filter agents by category
  const filteredAgents = agents?.filter((agent) => {
    if (selectedCategory === 'all') return true;
    return agent.category === selectedCategory;
  }) || [];

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center mb-2">
            <SparklesIcon className="h-8 w-8 text-primary-600 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">AI Agents</h1>
          </div>
          <p className="text-sm text-gray-600">
            Browse and invoke individual Professor Framework agents for 5-10x productivity gains. For multi-agent orchestration, see the Workflows page.
          </p>
        </div>

        {/* Main Content */}
        <>
            {/* Category Tabs */}
            <div className="mb-6">
              <div className="border-b border-gray-200">
                <nav className="-mb-px flex space-x-6 overflow-x-auto" aria-label="Agent Categories">
                  {AGENT_CATEGORIES.map((category) => (
                    <button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id)}
                      className={`
                        whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors
                        ${
                          selectedCategory === category.id
                            ? `border-${category.color}-500 text-${category.color}-600`
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }
                      `}
                    >
                      {category.name}
                      {category.id === 'all' && agents && (
                        <span className="ml-2 text-gray-400">({agents.length})</span>
                      )}
                    </button>
                  ))}
                </nav>
              </div>
            </div>

            {/* Agent Selection Grid */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                {selectedCategory === 'all'
                  ? 'All Agents'
                  : AGENT_CATEGORIES.find(c => c.id === selectedCategory)?.name
                }
                <span className="ml-2 text-sm text-gray-500 font-normal">
                  ({filteredAgents.length} {filteredAgents.length === 1 ? 'agent' : 'agents'})
                </span>
              </h2>
              {agentsLoading ? (
                <SkeletonList items={6} />
              ) : filteredAgents.length === 0 ? (
                <div className="bg-gray-50 rounded-lg">
                  <EmptyState
                    icon="🤖"
                    title="No agents found"
                    message="No agents found in this category. Try selecting a different category."
                  />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredAgents.map((agent) => {
                    const Icon = AGENT_ICONS[agent.id] || DocumentTextIcon;
                    const color = AGENT_COLORS[agent.id] || 'blue';

                    return (
                      <div
                        key={agent.id}
                        className="p-6 bg-white rounded-lg border-2 border-gray-200 hover:border-gray-300 hover:shadow-md transition-all"
                      >
                        <div className="flex items-start mb-3">
                          <div className={`p-3 bg-${color}-100 rounded-lg mr-4`}>
                            <Icon className={`h-6 w-6 text-${color}-600`} />
                          </div>
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 mb-1">
                              {agent.name}
                            </h3>
                            <p className="text-xs text-gray-500">
                              {agent.productivity_gain} faster • {agent.estimated_time}
                            </p>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                          {agent.description}
                        </p>
                        <div className="flex flex-wrap gap-1 mb-4">
                          {agent.capabilities.slice(0, 3).map((cap, idx) => (
                            <span
                              key={idx}
                              className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded"
                            >
                              {cap}
                            </span>
                          ))}
                          {agent.capabilities.length > 3 && (
                            <span className="text-xs px-2 py-1 bg-gray-100 text-gray-500 rounded">
                              +{agent.capabilities.length - 3} more
                            </span>
                          )}
                        </div>

                        {/* Action Buttons */}
                        <div className="flex space-x-2">
                          <Link
                            to={`/agents/${agent.id}/details`}
                            className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                          >
                            <InformationCircleIcon className="h-4 w-4 mr-1.5" />
                            Details
                          </Link>
                          <Link
                            to={`/agents/${agent.id}/task`}
                            className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                          >
                            <SparklesIcon className="h-4 w-4 mr-1.5" />
                            Task
                          </Link>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Recent Jobs */}
            {recentJobs && recentJobs.length > 0 && (
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Recent Jobs
                </h2>
                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          Agent
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          Task
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          Created
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {recentJobs.map((job) => {
                        const StatusIcon = getStatusIcon(job.status);
                        return (
                          <tr key={job.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                              {job.agent_type}
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                              {job.task_description}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(job.status)}`}>
                                <StatusIcon className="h-4 w-4 mr-1" />
                                {job.status}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {new Date(job.created_at).toLocaleDateString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                              <Link
                                to={`/agents/jobs/${job.id}`}
                                className="text-primary-600 hover:text-primary-900"
                              >
                                View
                              </Link>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
      </div>
    </Layout>
  );
}
