/**
 * Workflow Editor - Create or edit multi-agent workflows
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  PlusIcon,
  TrashIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  SparklesIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import api from '../services/api';

export default function WorkflowEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEditMode = !!id;

  // Form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('draft');
  const [tags, setTags] = useState('');
  const [estimatedDuration, setEstimatedDuration] = useState('');
  const [steps, setSteps] = useState([]);

  // Fetch available agents
  const { data: agents } = useQuery({
    queryKey: ['agents'],
    queryFn: async () => {
      const response = await api.get('/agents/');
      return response.data;
    },
  });

  // Fetch workflow if editing
  const { data: workflow, isLoading } = useQuery({
    queryKey: ['workflow', id],
    queryFn: async () => {
      const response = await api.get(`/workflows/${id}`);
      return response.data;
    },
    enabled: isEditMode,
  });

  // Populate form when editing
  useEffect(() => {
    if (workflow) {
      setName(workflow.name);
      setDescription(workflow.description || '');
      setStatus(workflow.status);
      setTags(workflow.tags?.join(', ') || '');
      setEstimatedDuration(workflow.estimated_duration || '');
      setSteps(workflow.steps || []);
    }
  }, [workflow]);

  // Save mutation
  const saveMutation = useMutation({
    mutationFn: async (workflowData) => {
      if (isEditMode) {
        return api.put(`/workflows/${id}`, workflowData);
      } else {
        return api.post('/workflows/', workflowData);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['workflows']);
      navigate('/workflows');
    },
  });

  const handleAddStep = () => {
    setSteps([
      ...steps,
      {
        agent_type: agents?.[0]?.agent_type || '',
        name: '',
        description: '',
        task_template: '',
        parameters: {},
        use_previous_output: false,
        required: true,
      },
    ]);
  };

  const handleRemoveStep = (index) => {
    setSteps(steps.filter((_, i) => i !== index));
  };

  const handleMoveStep = (index, direction) => {
    const newSteps = [...steps];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    [newSteps[index], newSteps[newIndex]] = [newSteps[newIndex], newSteps[index]];
    setSteps(newSteps);
  };

  const handleStepChange = (index, field, value) => {
    const newSteps = [...steps];
    newSteps[index] = { ...newSteps[index], [field]: value };
    setSteps(newSteps);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const workflowData = {
      name,
      description,
      status,
      tags: tags.split(',').map((t) => t.trim()).filter(Boolean),
      estimated_duration: estimatedDuration || null,
      steps,
    };

    saveMutation.mutate(workflowData);
  };

  if (isEditMode && isLoading) {
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

  return (
    <Layout>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link
            to="/workflows"
            className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Workflows
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">
            {isEditMode ? 'Edit Workflow' : 'Create New Workflow'}
          </h1>
          <p className="mt-2 text-gray-600">
            Design a multi-agent workflow by chaining Professor Framework agents together.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Workflow Name *
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  placeholder="e.g., Content Review Pipeline"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Describe what this workflow does..."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status
                  </label>
                  <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="draft">Draft</option>
                    <option value="active">Active</option>
                    <option value="archived">Archived</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Estimated Duration
                  </label>
                  <input
                    type="text"
                    value={estimatedDuration}
                    onChange={(e) => setEstimatedDuration(e.target.value)}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., 2-3 hours"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tags (comma-separated)
                  </label>
                  <input
                    type="text"
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., content, review, quality"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Workflow Steps */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Workflow Steps</h2>
              <button
                type="button"
                onClick={handleAddStep}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                <PlusIcon className="h-4 w-4 mr-1" />
                Add Step
              </button>
            </div>

            {steps.length === 0 ? (
              <div className="text-center py-12 border-2 border-dashed border-gray-300 rounded-lg">
                <SparklesIcon className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-500">No steps yet</p>
                <p className="text-sm text-gray-500">Add your first agent step to begin</p>
              </div>
            ) : (
              <div className="space-y-4">
                {steps.map((step, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-lg p-4 bg-gray-50"
                  >
                    {/* Step Header */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-2">
                        <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary-600 text-white font-bold text-sm">
                          {index + 1}
                        </span>
                        <span className="font-medium text-gray-900">
                          Step {index + 1}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        {index > 0 && (
                          <button
                            type="button"
                            onClick={() => handleMoveStep(index, 'up')}
                            className="p-1 text-gray-400 hover:text-gray-600"
                            title="Move up"
                          >
                            <ArrowUpIcon className="h-5 w-5" />
                          </button>
                        )}
                        {index < steps.length - 1 && (
                          <button
                            type="button"
                            onClick={() => handleMoveStep(index, 'down')}
                            className="p-1 text-gray-400 hover:text-gray-600"
                            title="Move down"
                          >
                            <ArrowDownIcon className="h-5 w-5" />
                          </button>
                        )}
                        <button
                          type="button"
                          onClick={() => handleRemoveStep(index)}
                          className="p-1 text-red-400 hover:text-red-600"
                          title="Remove step"
                        >
                          <TrashIcon className="h-5 w-5" />
                        </button>
                      </div>
                    </div>

                    {/* Step Fields */}
                    <div className="space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Agent Type *
                        </label>
                        <select
                          value={step.agent_type}
                          onChange={(e) =>
                            handleStepChange(index, 'agent_type', e.target.value)
                          }
                          required
                          className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                        >
                          <option value="">Select an agent...</option>
                          {agents?.map((agent) => (
                            <option key={agent.agent_type} value={agent.agent_type}>
                              {agent.name} ({agent.agent_type})
                            </option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Step Name *
                        </label>
                        <input
                          type="text"
                          value={step.name}
                          onChange={(e) => handleStepChange(index, 'name', e.target.value)}
                          required
                          className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                          placeholder="e.g., Review Content"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Description
                        </label>
                        <input
                          type="text"
                          value={step.description}
                          onChange={(e) =>
                            handleStepChange(index, 'description', e.target.value)
                          }
                          className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                          placeholder="What does this step do?"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Task Template
                        </label>
                        <textarea
                          value={step.task_template}
                          onChange={(e) =>
                            handleStepChange(index, 'task_template', e.target.value)
                          }
                          rows={2}
                          className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500 font-mono text-sm"
                          placeholder="Use {'{'}variable{'}'} for dynamic parameters"
                        />
                      </div>

                      <div className="flex items-center space-x-6">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={step.use_previous_output}
                            onChange={(e) =>
                              handleStepChange(
                                index,
                                'use_previous_output',
                                e.target.checked
                              )
                            }
                            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">
                            Use output from previous step
                          </span>
                        </label>

                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={step.required}
                            onChange={(e) =>
                              handleStepChange(index, 'required', e.target.checked)
                            }
                            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">Required</span>
                        </label>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-3">
            <Link
              to="/workflows"
              className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={saveMutation.isLoading || steps.length === 0}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
            >
              <CheckCircleIcon className="h-5 w-5 mr-2" />
              {saveMutation.isLoading
                ? 'Saving...'
                : isEditMode
                ? 'Update Workflow'
                : 'Create Workflow'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
