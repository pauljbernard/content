/**
 * Workflows page - Multi-agent workflow orchestration
 *
 * Create, manage, and execute workflows that chain multiple agents together.
 */
import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  PlusIcon,
  PlayIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  QueueListIcon,
  SparklesIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import EmptyState from '../components/EmptyState';
import { SkeletonWorkflow, SkeletonList } from '../components/LoadingSkeleton';
import { showSuccess, showError, showPromise } from '../utils/toast';

export default function Workflows() {
  const [activeTab, setActiveTab] = useState('my-workflows'); // 'my-workflows' | 'templates' | 'executions'
  const [searchQuery, setSearchQuery] = useState('');
  const queryClient = useQueryClient();

  // Fetch workflows
  const { data: workflows, isLoading: workflowsLoading } = useQuery({
    queryKey: ['workflows', activeTab === 'templates'],
    queryFn: async () => {
      const params = activeTab === 'templates' ? { is_template: true } : {};
      const response = await api.get('/workflows/', { params });
      return response.data;
    },
  });

  // Fetch workflow executions
  const { data: executions, isLoading: executionsLoading } = useQuery({
    queryKey: ['workflow-executions'],
    queryFn: async () => {
      const response = await api.get('/workflows/executions', { params: { limit: 20 } });
      return response.data;
    },
    enabled: activeTab === 'executions',
  });

  // Delete workflow mutation
  const deleteMutation = useMutation({
    mutationFn: (workflowId) => api.delete(`/workflows/${workflowId}`),
    onSuccess: () => {
      queryClient.invalidateQueries(['workflows']);
      showSuccess('Workflow deleted successfully');
    },
    onError: (error) => {
      showError('Failed to delete workflow', error);
    },
  });

  // Execute workflow mutation
  const executeMutation = useMutation({
    mutationFn: ({ workflowId, parameters }) =>
      api.post(`/workflows/${workflowId}/execute`, {
        workflow_id: workflowId,
        input_parameters: parameters || {},
      }),
    onSuccess: () => {
      queryClient.invalidateQueries(['workflow-executions']);
      setActiveTab('executions');
      showSuccess('Workflow execution started successfully');
    },
    onError: (error) => {
      showError('Failed to execute workflow', error);
    },
  });

  // Filter workflows by search
  const filteredWorkflows = workflows?.filter((workflow) => {
    if (!searchQuery) return true;
    return (
      workflow.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      workflow.description?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  // Tabs
  const tabs = [
    { id: 'my-workflows', name: 'My Workflows', icon: QueueListIcon },
    { id: 'templates', name: 'Templates', icon: SparklesIcon },
    { id: 'executions', name: 'Executions', icon: ClockIcon },
  ];

  // Status badge colors
  const statusColors = {
    draft: 'bg-gray-100 text-gray-800',
    active: 'bg-green-100 text-green-800',
    archived: 'bg-yellow-100 text-yellow-800',
    queued: 'bg-blue-100 text-blue-800',
    running: 'bg-purple-100 text-purple-800 animate-pulse',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    cancelled: 'bg-gray-100 text-gray-800',
    partially_completed: 'bg-orange-100 text-orange-800',
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="w-4 h-4" />;
      case 'failed':
        return <XCircleIcon className="w-4 h-4" />;
      case 'running':
        return <ArrowPathIcon className="w-4 h-4 animate-spin" />;
      default:
        return <ClockIcon className="w-4 h-4" />;
    }
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AI Workflows</h1>
              <p className="mt-2 text-sm text-gray-600">
                Orchestrate multiple Professor Framework agents into powerful content development pipelines.
                Create custom workflows or use pre-built templates.
              </p>
            </div>
            <Link
              to="/workflows/new"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
            >
              <PlusIcon className="-ml-1 mr-2 h-5 w-5" />
              Create Workflow
            </Link>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`
                      group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm
                      ${
                        activeTab === tab.id
                          ? 'border-primary-500 text-primary-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }
                    `}
                  >
                    <Icon
                      className={`
                        -ml-0.5 mr-2 h-5 w-5
                        ${activeTab === tab.id ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'}
                      `}
                    />
                    {tab.name}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Search */}
        {activeTab !== 'executions' && (
          <div className="mb-6">
            <input
              type="text"
              placeholder="Search workflows..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="block w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        )}

        {/* Content based on active tab */}
        {activeTab === 'executions' ? (
          // Executions List
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            {executionsLoading ? (
              <div className="p-6">
                <SkeletonList items={5} />
              </div>
            ) : executions && executions.length > 0 ? (
              <ul className="divide-y divide-gray-200">
                {executions.map((execution) => (
                  <li key={execution.id}>
                    <Link
                      to={`/workflows/executions/${execution.id}`}
                      className="block hover:bg-gray-50 transition"
                    >
                      <div className="px-4 py-4 sm:px-6">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            {getStatusIcon(execution.status)}
                            <p className="ml-2 text-sm font-medium text-primary-600 truncate">
                              Execution #{execution.id}
                            </p>
                          </div>
                          <div className="ml-2 flex-shrink-0 flex">
                            <span
                              className={`
                                inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                                ${statusColors[execution.status]}
                              `}
                            >
                              {execution.status}
                            </span>
                          </div>
                        </div>
                        <div className="mt-2 sm:flex sm:justify-between">
                          <div className="sm:flex">
                            <p className="flex items-center text-sm text-gray-500">
                              <ClockIcon className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                              {new Date(execution.created_at).toLocaleString()}
                            </p>
                          </div>
                          {execution.error_message && (
                            <p className="mt-2 text-sm text-red-600 sm:mt-0">
                              Error: {execution.error_message}
                            </p>
                          )}
                        </div>
                      </div>
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyState
                icon="⏱️"
                title="No workflow executions yet"
                message="Execute a workflow to see its execution history here"
              />
            )}
          </div>
        ) : (
          // Workflows Grid
          <div>
            {workflowsLoading ? (
              <SkeletonWorkflow steps={3} />
            ) : filteredWorkflows && filteredWorkflows.length > 0 ? (
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {filteredWorkflows.map((workflow) => (
                  <div
                    key={workflow.id}
                    className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition"
                  >
                    <div className="p-6">
                      {/* Header */}
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <h3 className="text-lg font-medium text-gray-900 truncate">
                            {workflow.name}
                          </h3>
                          <span
                            className={`
                              mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                              ${statusColors[workflow.status]}
                            `}
                          >
                            {workflow.status}
                          </span>
                        </div>
                      </div>

                      {/* Description */}
                      {workflow.description && (
                        <p className="mt-3 text-sm text-gray-600 line-clamp-2">
                          {workflow.description}
                        </p>
                      )}

                      {/* Steps */}
                      <div className="mt-4">
                        <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">
                          {workflow.steps.length} Steps
                        </p>
                        <div className="mt-2 flex flex-wrap gap-1">
                          {workflow.steps.slice(0, 3).map((step, index) => (
                            <span
                              key={index}
                              className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800"
                            >
                              {step.name}
                            </span>
                          ))}
                          {workflow.steps.length > 3 && (
                            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600">
                              +{workflow.steps.length - 3} more
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Tags */}
                      {workflow.tags && workflow.tags.length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-1">
                          {workflow.tags.map((tag) => (
                            <span
                              key={tag}
                              className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Actions */}
                      <div className="mt-6 flex space-x-2">
                        <Link
                          to={`/workflows/${workflow.id}`}
                          className="flex-1 inline-flex justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                        >
                          <EyeIcon className="h-4 w-4 mr-1" />
                          View
                        </Link>

                        {workflow.status === 'active' && (
                          <button
                            onClick={() => executeMutation.mutate({ workflowId: workflow.id })}
                            disabled={executeMutation.isLoading}
                            className="flex-1 inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                          >
                            <PlayIcon className="h-4 w-4 mr-1" />
                            Execute
                          </button>
                        )}

                        {activeTab === 'my-workflows' && !workflow.is_template && (
                          <>
                            <Link
                              to={`/workflows/${workflow.id}/edit`}
                              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                            >
                              <PencilIcon className="h-4 w-4" />
                            </Link>
                            <button
                              onClick={() => {
                                if (confirm('Are you sure you want to delete this workflow?')) {
                                  deleteMutation.mutate(workflow.id);
                                }
                              }}
                              disabled={deleteMutation.isLoading}
                              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 disabled:opacity-50"
                            >
                              <TrashIcon className="h-4 w-4" />
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow">
                <EmptyState
                  icon="📋"
                  title={activeTab === 'templates' ? 'No templates available' : 'No workflows yet'}
                  message={
                    activeTab === 'templates'
                      ? 'Check back later for pre-built workflow templates'
                      : 'Get started by creating a new workflow to orchestrate multiple AI agents'
                  }
                  action={
                    activeTab !== 'templates'
                      ? {
                          label: 'Create Workflow',
                          onClick: () => window.location.href = '/workflows/new',
                          icon: <PlusIcon className="h-5 w-5" />,
                        }
                      : undefined
                  }
                />
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
}
