/**
 * Agent Task page - Configure and invoke an AI agent
 */
import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  SparklesIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { agentsAPI } from '../services/api';
import { showSuccess, showError, showWarning } from '../utils/toast';

export default function AgentTask() {
  const { agentId } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // State
  const [taskDescription, setTaskDescription] = useState('');
  const [parameters, setParameters] = useState({
    grade_levels: [],
    subject: '',
    state: '',
    standards: [],
  });
  const [activeJobId, setActiveJobId] = useState(null);
  const [showResults, setShowResults] = useState(false);

  // Queries
  const { data: agents, isLoading: agentsLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: agentsAPI.list,
  });

  const agent = agents?.find(a => a.id === agentId);

  const { data: jobStatus, refetch: refetchJobStatus } = useQuery({
    queryKey: ['agent-job-status', activeJobId],
    queryFn: () => agentsAPI.getJobStatus(activeJobId),
    enabled: !!activeJobId,
    refetchInterval: (data) => {
      if (data?.status === 'running' || data?.status === 'queued') {
        return 2000;
      }
      return false;
    },
  });

  const { data: jobResult } = useQuery({
    queryKey: ['agent-job-result', activeJobId],
    queryFn: () => agentsAPI.getJobResult(activeJobId),
    enabled: !!activeJobId && jobStatus?.status === 'completed',
  });

  // Mutations
  const invokeMutation = useMutation({
    mutationFn: () => agentsAPI.invoke(agentId, taskDescription, parameters),
    onSuccess: (data) => {
      setActiveJobId(data.id);
      queryClient.invalidateQueries(['agent-jobs']);
      setShowResults(false);
      showSuccess(`${agent.name} started successfully`);
    },
    onError: (error) => {
      showError('Failed to invoke agent', error);
    },
  });

  const cancelMutation = useMutation({
    mutationFn: (jobId) => agentsAPI.cancelJob(jobId),
    onSuccess: () => {
      queryClient.invalidateQueries(['agent-job-status', activeJobId]);
      queryClient.invalidateQueries(['agent-jobs']);
      showWarning('Agent job cancelled');
    },
    onError: (error) => {
      showError('Failed to cancel job', error);
    },
  });

  // Effects
  useEffect(() => {
    if (jobStatus?.status === 'completed') {
      setShowResults(true);
      queryClient.invalidateQueries(['agent-jobs']);
    }
  }, [jobStatus?.status, queryClient]);

  // Handlers
  const handleInvoke = () => {
    if (!taskDescription.trim()) {
      showWarning('Please provide a task description');
      return;
    }
    invokeMutation.mutate();
  };

  const handleUseResult = () => {
    if (!jobResult?.generated_content) return;

    navigate('/content/new', {
      state: {
        generatedContent: jobResult.generated_content,
        metadata: jobResult.metadata,
      },
    });
  };

  const handleStartNew = () => {
    setActiveJobId(null);
    setShowResults(false);
    setTaskDescription('');
    setParameters({
      grade_levels: [],
      subject: '',
      state: '',
      standards: [],
    });
  };

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

  if (agentsLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  if (!agent) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h3 className="mt-2 text-lg font-medium text-gray-900">Agent not found</h3>
          <Link
            to="/agents"
            className="mt-4 inline-flex items-center text-primary-600 hover:text-primary-700"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Agents
          </Link>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link
            to="/agents"
            className="inline-flex items-center text-sm text-primary-600 hover:text-primary-700 mb-4"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Agents
          </Link>

          <div className="flex items-center mb-2">
            <SparklesIcon className="h-8 w-8 text-primary-600 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">{agent.name}</h1>
          </div>
          <p className="text-gray-600">{agent.description}</p>
        </div>

        {/* Agent Configuration (when no job active) */}
        {!activeJobId && (
          <div className="bg-white rounded-lg shadow p-6">
            {/* Task Description */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Task Description *
              </label>
              <textarea
                value={taskDescription}
                onChange={(e) => setTaskDescription(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Describe what you want to create..."
              />
              <p className="mt-1 text-xs text-gray-500">
                Be specific about your requirements, target audience, and desired outcomes
              </p>
            </div>

            {/* Parameters */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Subject
                </label>
                <select
                  value={parameters.subject}
                  onChange={(e) => setParameters({ ...parameters, subject: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Select subject</option>
                  <option value="mathematics">Mathematics</option>
                  <option value="ela">English Language Arts</option>
                  <option value="science">Science</option>
                  <option value="social-studies">Social Studies</option>
                  <option value="computer-science">Computer Science</option>
                  <option value="world-languages">World Languages</option>
                  <option value="fine-arts">Fine Arts</option>
                  <option value="physical-education">Physical Education</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  State/District
                </label>
                <select
                  value={parameters.state}
                  onChange={(e) => setParameters({ ...parameters, state: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Select state</option>
                  <option value="texas">Texas</option>
                  <option value="california">California</option>
                  <option value="florida">Florida</option>
                  <option value="new-york">New York</option>
                  <option value="pennsylvania">Pennsylvania</option>
                </select>
              </div>
            </div>

            {/* Actions */}
            <div className="flex justify-end space-x-3">
              <Link
                to="/agents"
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </Link>
              <button
                onClick={handleInvoke}
                disabled={invokeMutation.isPending || !taskDescription.trim()}
                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {invokeMutation.isPending ? (
                  <>
                    <ArrowPathIcon className="h-4 w-4 mr-2 animate-spin" />
                    Starting...
                  </>
                ) : (
                  <>
                    <SparklesIcon className="h-4 w-4 mr-2" />
                    Start Agent
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Agent Progress/Results (when job active) */}
        {activeJobId && jobStatus && (
          <div className="bg-white rounded-lg shadow p-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">
                  {jobStatus.agent_type.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </h2>
                <p className="text-sm text-gray-600 mt-1">
                  {jobStatus.task_description}
                </p>
              </div>
              <button
                onClick={handleStartNew}
                className="text-sm text-gray-600 hover:text-gray-900"
              >
                ← Start New Task
              </button>
            </div>

            {/* Progress Bar */}
            {(jobStatus.status === 'queued' || jobStatus.status === 'running') && (
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
                {jobStatus.status === 'running' && (
                  <div className="mt-4 flex justify-center">
                    <button
                      onClick={() => cancelMutation.mutate(activeJobId)}
                      disabled={cancelMutation.isPending}
                      className="text-sm text-red-600 hover:text-red-700 disabled:opacity-50"
                    >
                      Cancel Job
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Status Badge */}
            <div className="mb-6">
              {(() => {
                const StatusIcon = getStatusIcon(jobStatus.status);
                return (
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(jobStatus.status)}`}>
                    <StatusIcon className={`h-5 w-5 mr-2 ${jobStatus.status === 'running' ? 'animate-spin' : ''}`} />
                    {jobStatus.status.charAt(0).toUpperCase() + jobStatus.status.slice(1)}
                  </span>
                );
              })()}
            </div>

            {/* Results */}
            {showResults && jobResult && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Generated Content
                </h3>

                {/* Content Preview */}
                <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200 max-h-96 overflow-y-auto">
                  <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                    {jobResult.generated_content}
                  </pre>
                </div>

                {/* Metadata */}
                {jobResult.metadata && Object.keys(jobResult.metadata).length > 0 && (
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Metadata</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {Object.entries(jobResult.metadata).map(([key, value]) => (
                        <div key={key} className="text-sm">
                          <span className="text-gray-500">{key.replace('_', ' ')}:</span>{' '}
                          <span className="font-medium text-gray-900">
                            {Array.isArray(value) ? value.join(', ') : value}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Suggested Next Steps */}
                {jobResult.suggestions && jobResult.suggestions.length > 0 && (
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Suggested Next Steps</h4>
                    <ul className="space-y-2">
                      {jobResult.suggestions.map((suggestion, idx) => (
                        <li key={idx} className="flex items-start text-sm text-gray-600">
                          <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Actions */}
                <div className="flex space-x-3">
                  <button
                    onClick={handleUseResult}
                    className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                  >
                    Use in Content Editor
                  </button>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(jobResult.generated_content);
                      showSuccess('Content copied to clipboard!');
                    }}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Copy to Clipboard
                  </button>
                  {activeJobId && (
                    <button
                      onClick={() => navigate(`/agents/jobs/${activeJobId}`)}
                      className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                    >
                      Open Job Detail
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Error Display */}
            {jobStatus.status === 'failed' && (
              <div className="bg-red-50 border-l-4 border-red-400 p-4">
                <div className="flex">
                  <XCircleIcon className="h-5 w-5 text-red-400" />
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Job Failed</h3>
                    <p className="mt-2 text-sm text-red-700">
                      {jobStatus.error_message || 'An error occurred while processing your request.'}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
}
