/**
 * Agent Job Detail page - view status and generated output for a specific run
 */
import { useMemo } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  DocumentDuplicateIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { agentsAPI } from '../services/api';
import { showSuccess, showWarning, showError } from '../utils/toast';

export default function AgentJobDetail() {
  const { jobId } = useParams();
  const queryClient = useQueryClient();

  const {
    data: job,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['agent-job', jobId],
    queryFn: () => agentsAPI.getJobStatus(jobId),
    enabled: !!jobId,
    refetchInterval: (data) => {
      if (!data) return 2000;
      return ['running', 'queued'].includes(data.status) ? 2000 : false;
    },
  });

  const { data: jobResult } = useQuery({
    queryKey: ['agent-job-result', jobId],
    queryFn: () => agentsAPI.getJobResult(jobId),
    enabled: !!job && job.status === 'completed',
  });

  const cancelMutation = useMutation({
    mutationFn: () => agentsAPI.cancelJob(jobId),
    onSuccess: () => {
      queryClient.invalidateQueries(['agent-job', jobId]);
      queryClient.invalidateQueries(['agent-jobs']);
      showWarning('Agent job cancelled');
    },
    onError: (err) => {
      showError('Failed to cancel job', err);
    },
  });

  const jobMetadata = useMemo(() => {
    if (jobResult?.metadata && Object.keys(jobResult.metadata).length > 0) {
      return jobResult.metadata;
    }
    if (job?.output_metadata && Object.keys(job.output_metadata).length > 0) {
      return job.output_metadata;
    }
    return null;
  }, [jobResult, job]);

  const generatedContent = jobResult?.generated_content || job?.output_content;

  const suggestions = jobResult?.suggestions || [];

  const statusStyles = {
    queued: 'text-yellow-700 bg-yellow-100',
    running: 'text-blue-700 bg-blue-100',
    completed: 'text-green-700 bg-green-100',
    failed: 'text-red-700 bg-red-100',
    cancelled: 'text-gray-700 bg-gray-100',
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading job...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (isError || !job) {
    return (
      <Layout>
        <div className="max-w-3xl mx-auto py-12 text-center">
          <XCircleIcon className="h-12 w-12 text-red-500 mx-auto" />
          <h2 className="mt-4 text-xl font-semibold text-gray-900">Unable to load job</h2>
          <p className="mt-2 text-gray-600">
            {error?.response?.data?.detail || 'This job may not exist or you may not have access.'}
          </p>
          <div className="mt-6">
            <Link
              to="/agents"
              className="inline-flex items-center text-primary-600 hover:text-primary-700"
            >
              <ArrowLeftIcon className="h-4 w-4 mr-2" />
              Back to Agents
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <Link
              to="/agents"
              className="inline-flex items-center text-sm text-primary-600 hover:text-primary-700"
            >
              <ArrowLeftIcon className="h-4 w-4 mr-2" />
              Back to Agents
            </Link>
            <h1 className="mt-3 text-3xl font-bold text-gray-900">Agent Job #{job.id}</h1>
            <p className="text-sm text-gray-500 mt-1">
              {job.agent_type.replace('-', ' ')}
            </p>
          </div>
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
              statusStyles[job.status] || 'text-gray-700 bg-gray-100'
            }`}
          >
            {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white shadow rounded-lg p-6 lg:col-span-2">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Task Details</h2>
            <dl className="space-y-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Task Description</dt>
                <dd className="mt-1 text-sm text-gray-900 whitespace-pre-line">
                  {job.task_description}
                </dd>
              </div>
              {job.parameters && Object.keys(job.parameters).length > 0 && (
                <div>
                  <dt className="text-sm font-medium text-gray-500">Parameters</dt>
                  <dd className="mt-2">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {Object.entries(job.parameters).map(([key, value]) => (
                        <div key={key} className="text-sm text-gray-700">
                          <span className="text-gray-500 capitalize">{key.replace('_', ' ')}:</span>{' '}
                          <span className="font-medium">
                            {Array.isArray(value) ? value.join(', ') : value}
                          </span>
                        </div>
                      ))}
                    </div>
                  </dd>
                </div>
              )}
            </dl>
          </div>
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Execution</h2>
            <dl className="space-y-3 text-sm text-gray-700">
              <div className="flex items-start">
                <ClockIcon className="h-5 w-5 text-gray-400 mr-2 mt-0.5" />
                <div>
                  <dt className="text-gray-500">Created</dt>
                  <dd className="font-medium">
                    {new Date(job.created_at).toLocaleString()}
                  </dd>
                </div>
              </div>
              {job.started_at && (
                <div className="flex items-start">
                  <SparklesIcon className="h-5 w-5 text-gray-400 mr-2 mt-0.5" />
                  <div>
                    <dt className="text-gray-500">Started</dt>
                    <dd className="font-medium">
                      {new Date(job.started_at).toLocaleString()}
                    </dd>
                  </div>
                </div>
              )}
              {job.completed_at && (
                <div className="flex items-start">
                  <CheckCircleIcon className="h-5 w-5 text-gray-400 mr-2 mt-0.5" />
                  <div>
                    <dt className="text-gray-500">Completed</dt>
                    <dd className="font-medium">
                      {new Date(job.completed_at).toLocaleString()}
                    </dd>
                  </div>
                </div>
              )}
              {job.status === 'failed' && job.error_message && (
                <div className="bg-red-50 border border-red-100 rounded-md p-3">
                  <p className="text-sm text-red-700">
                    {job.error_message}
                  </p>
                </div>
              )}
              {job.status === 'running' && (
                <button
                  onClick={() => cancelMutation.mutate()}
                  disabled={cancelMutation.isPending}
                  className="mt-4 w-full inline-flex justify-center px-3 py-2 border border-red-300 rounded-md text-sm font-medium text-red-600 hover:bg-red-50 disabled:opacity-50"
                >
                  Cancel Job
                </button>
              )}
            </dl>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Generated Output</h2>
            {generatedContent && (
              <button
                onClick={() => {
                  navigator.clipboard.writeText(generatedContent);
                  showSuccess('Content copied to clipboard');
                }}
                className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
              >
                <DocumentDuplicateIcon className="h-4 w-4 mr-1.5" />
                Copy
              </button>
            )}
          </div>

          {generatedContent ? (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 max-h-[32rem] overflow-y-auto">
              <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">
                {generatedContent}
              </pre>
            </div>
          ) : (
            <div className="text-sm text-gray-500">
              {job.status === 'completed'
                ? 'This job did not return any content.'
                : 'Content will appear here once the agent completes the task.'}
            </div>
          )}
        </div>

        {jobMetadata && (
          <div className="bg-white shadow rounded-lg p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Metadata</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(jobMetadata).map(([key, value]) => (
                <div key={key} className="text-sm">
                  <span className="text-gray-500 capitalize block">{key.replace('_', ' ')}</span>
                  <span className="font-medium text-gray-900">
                    {Array.isArray(value) ? value.join(', ') : value?.toString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {suggestions.length > 0 && (
          <div className="bg-white shadow rounded-lg p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Suggested Next Steps</h2>
            <ul className="space-y-3">
              {suggestions.map((suggestion, idx) => (
                <li key={idx} className="flex items-start text-sm text-gray-700">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
                  {suggestion}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Layout>
  );
}
