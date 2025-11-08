/**
 * Agent Details page - Read-only view of agent configuration and capabilities
 */
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  SparklesIcon,
  ClockIcon,
  RocketLaunchIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { agentsAPI } from '../services/api';

export default function AgentDetails() {
  const { agentId } = useParams();

  const { data: agents, isLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: agentsAPI.list,
  });

  const agent = agents?.find(a => a.id === agentId);

  if (isLoading) {
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
          <p className="mt-1 text-sm text-gray-500">
            The requested agent could not be found.
          </p>
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

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center mb-2">
                <SparklesIcon className="h-8 w-8 text-primary-600 mr-3" />
                <h1 className="text-3xl font-bold text-gray-900">{agent.name}</h1>
              </div>
              <p className="text-lg text-gray-600 mt-2">{agent.description}</p>
            </div>
          </div>
        </div>

        {/* Overview Card */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-start">
              <ClockIcon className="h-6 w-6 text-gray-400 mr-3 mt-1" />
              <div>
                <dt className="text-sm font-medium text-gray-500">Estimated Time</dt>
                <dd className="mt-1 text-lg font-semibold text-gray-900">
                  {agent.estimated_time}
                </dd>
              </div>
            </div>

            <div className="flex items-start">
              <RocketLaunchIcon className="h-6 w-6 text-gray-400 mr-3 mt-1" />
              <div>
                <dt className="text-sm font-medium text-gray-500">Productivity Gain</dt>
                <dd className="mt-1 text-lg font-semibold text-gray-900">
                  {agent.productivity_gain}
                </dd>
              </div>
            </div>

            <div className="flex items-start">
              <CheckCircleIcon className="h-6 w-6 text-gray-400 mr-3 mt-1" />
              <div>
                <dt className="text-sm font-medium text-gray-500">Category</dt>
                <dd className="mt-1 text-lg font-semibold text-gray-900 capitalize">
                  {agent.category.replace('-', ' ')}
                </dd>
              </div>
            </div>
          </div>
        </div>

        {/* Capabilities Card */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Capabilities & Skills</h2>
          <p className="text-sm text-gray-600 mb-4">
            This agent has been trained with the following capabilities:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {agent.capabilities.map((capability, idx) => (
              <div key={idx} className="flex items-start">
                <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-gray-700">{capability}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Requirements Card */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Requirements</h2>
          <dl className="grid grid-cols-1 gap-4">
            <div>
              <dt className="text-sm font-medium text-gray-500">Required Role</dt>
              <dd className="mt-1 text-sm text-gray-900 capitalize">
                {agent.required_role.replace('_', ' ')}
              </dd>
              <dd className="mt-1 text-xs text-gray-500">
                Minimum user role required to invoke this agent
              </dd>
            </div>
          </dl>
        </div>

        {/* Configuration Info Card */}
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <SparklesIcon className="h-5 w-5 text-blue-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">Agent Configuration</h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>
                  This agent uses the Professor Framework's advanced AI capabilities. When invoked,
                  it will leverage all the skills listed above to complete your requested task.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="flex justify-end">
          <Link
            to={`/agents/${agent.id}/task`}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <SparklesIcon className="h-5 w-5 mr-2" />
            Start Task with This Agent
          </Link>
        </div>
      </div>
    </Layout>
  );
}
