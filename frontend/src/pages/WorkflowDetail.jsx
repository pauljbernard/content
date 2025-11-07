/**
 * Workflow Detail Page - Graphical visualization of workflow
 */
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  PlayIcon,
  PencilIcon,
  ClockIcon,
  UserIcon,
  TagIcon,
  ChevronRightIcon,
  CheckCircleIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import api from '../services/api';

export default function WorkflowDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Fetch workflow details
  const { data: workflow, isLoading } = useQuery({
    queryKey: ['workflow', id],
    queryFn: async () => {
      const response = await api.get(`/workflows/${id}`);
      return response.data;
    },
  });

  // Execute workflow mutation
  const executeMutation = useMutation({
    mutationFn: (parameters) =>
      api.post(`/workflows/${id}/execute`, {
        workflow_id: parseInt(id),
        input_parameters: parameters || {},
      }),
    onSuccess: (data) => {
      queryClient.invalidateQueries(['workflow-executions']);
      // Navigate to executions tab or show success message
      navigate('/workflows', { state: { tab: 'executions' } });
    },
  });

  const handleExecute = () => {
    if (confirm(`Execute workflow "${workflow.name}"?`)) {
      executeMutation.mutate({});
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading workflow...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (!workflow) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900">Workflow not found</h3>
          <Link to="/workflows" className="mt-4 text-primary-600 hover:text-primary-700">
            Back to Workflows
          </Link>
        </div>
      </Layout>
    );
  }

  const statusColors = {
    draft: 'bg-gray-100 text-gray-800',
    active: 'bg-green-100 text-green-800',
    archived: 'bg-yellow-100 text-yellow-800',
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link
            to="/workflows"
            className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Workflows
          </Link>

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900">{workflow.name}</h1>
              {workflow.description && (
                <p className="mt-2 text-gray-600">{workflow.description}</p>
              )}
              <div className="mt-3 flex items-center space-x-4">
                <span
                  className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    statusColors[workflow.status]
                  }`}
                >
                  {workflow.status}
                </span>
                {workflow.is_template && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                    Template
                  </span>
                )}
                {workflow.is_public && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    Public
                  </span>
                )}
              </div>
            </div>

            <div className="flex space-x-3">
              {workflow.status === 'active' && (
                <button
                  onClick={handleExecute}
                  disabled={executeMutation.isLoading}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                >
                  <PlayIcon className="h-5 w-5 mr-2" />
                  {executeMutation.isLoading ? 'Executing...' : 'Execute Workflow'}
                </button>
              )}
              {!workflow.is_template && (
                <Link
                  to={`/workflows/${id}/edit`}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  <PencilIcon className="h-5 w-5 mr-2" />
                  Edit
                </Link>
              )}
            </div>
          </div>
        </div>

        {/* Metadata */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="flex items-center text-sm text-gray-500 mb-1">
                <ClockIcon className="h-4 w-4 mr-2" />
                Created
              </div>
              <div className="text-sm font-medium text-gray-900">
                {new Date(workflow.created_at).toLocaleDateString()}
              </div>
            </div>
            <div>
              <div className="flex items-center text-sm text-gray-500 mb-1">
                <UserIcon className="h-4 w-4 mr-2" />
                Steps
              </div>
              <div className="text-sm font-medium text-gray-900">
                {workflow.steps.length} agent{workflow.steps.length !== 1 ? 's' : ''}
              </div>
            </div>
            {workflow.estimated_duration && (
              <div>
                <div className="flex items-center text-sm text-gray-500 mb-1">
                  <ClockIcon className="h-4 w-4 mr-2" />
                  Estimated Duration
                </div>
                <div className="text-sm font-medium text-gray-900">
                  {workflow.estimated_duration}
                </div>
              </div>
            )}
          </div>

          {/* Tags */}
          {workflow.tags && workflow.tags.length > 0 && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <TagIcon className="h-4 w-4 mr-2" />
                Tags
              </div>
              <div className="flex flex-wrap gap-2">
                {workflow.tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Workflow Visualization */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Workflow Steps</h2>

          {/* Flow Diagram */}
          <div className="space-y-0">
            {workflow.steps.map((step, index) => (
              <div key={index}>
                {/* Step Card */}
                <div className="relative">
                  {/* Step Number Badge */}
                  <div className="absolute -left-4 top-8 flex items-center justify-center w-8 h-8 rounded-full bg-primary-600 text-white font-bold text-sm z-10">
                    {index + 1}
                  </div>

                  {/* Step Content */}
                  <div className="ml-6 border-l-4 border-primary-300 pl-8 pb-8">
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 hover:shadow-md transition">
                      {/* Step Header */}
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <div className="flex items-center">
                            <SparklesIcon className="h-5 w-5 text-primary-600 mr-2" />
                            <h3 className="text-lg font-semibold text-gray-900">
                              {step.name}
                            </h3>
                          </div>
                          <p className="mt-1 text-sm text-gray-600 font-mono">
                            {step.agent_type}
                          </p>
                        </div>
                        {step.required && (
                          <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800">
                            Required
                          </span>
                        )}
                      </div>

                      {/* Step Description */}
                      {step.description && (
                        <p className="text-sm text-gray-700 mb-4">{step.description}</p>
                      )}

                      {/* Task Template */}
                      {step.task_template && (
                        <div className="bg-white border border-gray-200 rounded p-3 mb-4">
                          <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">
                            Task Template
                          </div>
                          <p className="text-sm text-gray-800 font-mono">
                            {step.task_template}
                          </p>
                        </div>
                      )}

                      {/* Parameters */}
                      {step.parameters && Object.keys(step.parameters).length > 0 && (
                        <div className="mb-4">
                          <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
                            Parameters
                          </div>
                          <div className="space-y-1">
                            {Object.entries(step.parameters).map(([key, value]) => (
                              <div
                                key={key}
                                className="flex items-center text-sm text-gray-700"
                              >
                                <code className="bg-gray-200 px-2 py-0.5 rounded text-xs font-mono">
                                  {key}
                                </code>
                                <span className="mx-2">→</span>
                                <span className="text-gray-600">{String(value)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Use Previous Output */}
                      {step.use_previous_output && (
                        <div className="flex items-center text-sm text-blue-600">
                          <CheckCircleIcon className="h-4 w-4 mr-2" />
                          Uses output from previous step
                        </div>
                      )}
                    </div>

                    {/* Arrow to next step */}
                    {index < workflow.steps.length - 1 && (
                      <div className="flex justify-center my-2">
                        <ChevronRightIcon className="h-6 w-6 text-primary-400 transform rotate-90" />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {/* Final Output */}
            <div className="relative">
              <div className="absolute -left-4 top-4 flex items-center justify-center w-8 h-8 rounded-full bg-green-600 text-white z-10">
                <CheckCircleIcon className="h-5 w-5" />
              </div>
              <div className="ml-6 pl-8">
                <div className="bg-green-50 border-2 border-green-300 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-green-900">Final Output</h3>
                  <p className="mt-2 text-sm text-green-700">
                    Workflow completes with the output from all {workflow.steps.length} steps
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
