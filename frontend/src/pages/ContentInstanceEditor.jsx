/**
 * Dynamic Content Instance Editor with AI Assist
 * Renders a form that adapts to the content type schema
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  ArrowLeftIcon,
  CheckIcon,
  XMarkIcon,
  SparklesIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI, agentsAPI } from '../services/api';
import Layout from '../components/Layout';
import DynamicFormField from '../components/DynamicFormField';
import AgentAssist from '../components/AgentAssist';

export default function ContentInstanceEditor() {
  const { contentTypeId, instanceId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({});
  const [status, setStatus] = useState('draft');
  const [validationErrors, setValidationErrors] = useState({});

  // AI Assist state
  const [showAIAssist, setShowAIAssist] = useState(false);
  const [targetField, setTargetField] = useState(null);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [agentTaskDescription, setAgentTaskDescription] = useState('');
  const [isInvoking, setIsInvoking] = useState(false);
  const [streamingText, setStreamingText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamError, setStreamError] = useState(null);

  // Fetch content type definition
  const { data: contentType, isLoading: loadingContentType } = useQuery({
    queryKey: ['content-type', contentTypeId],
    queryFn: () => contentTypesAPI.get(contentTypeId),
    enabled: !!contentTypeId,
  });

  // Fetch existing instance if editing
  const { data: instance, isLoading: loadingInstance } = useQuery({
    queryKey: ['content-instance', instanceId],
    queryFn: () => contentTypesAPI.getInstance(instanceId),
    enabled: !!instanceId,
  });

  // Initialize form data from existing instance
  useEffect(() => {
    if (instance) {
      setFormData(instance.data || {});
      setStatus(instance.status || 'draft');
    }
  }, [instance]);

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (data) => contentTypesAPI.createInstance(contentTypeId, data),
    onSuccess: (newInstance) => {
      queryClient.invalidateQueries(['content-instances', contentTypeId]);
      toast.success('Content instance created successfully');
      navigate(`/content-types/${contentTypeId}/instances/${newInstance.id}`);
    },
    onError: (error) => {
      console.error('[CREATE ERROR]', error);
      console.error('[CREATE ERROR] Response:', error.response);
      console.error('[CREATE ERROR] Response data:', error.response?.data);

      const errorData = error.response?.data;

      // Handle validation errors object
      if (errorData?.detail && typeof errorData.detail === 'object' && errorData.detail.validation_errors) {
        const errors = {};
        errorData.detail.validation_errors.forEach((err) => {
          const match = err.match(/attribute '(.+?)'/);
          if (match) {
            errors[match[1]] = err;
          }
        });
        setValidationErrors(errors);
        toast.error(`Validation errors: ${errorData.detail.validation_errors.join(', ')}`);
      } else if (errorData?.validation_errors) {
        // Legacy format
        const errors = {};
        errorData.validation_errors.forEach((err) => {
          const match = err.match(/attribute '(.+?)'/);
          if (match) {
            errors[match[1]] = err;
          }
        });
        setValidationErrors(errors);
        toast.error(`Validation errors: ${errorData.validation_errors.join(', ')}`);
      } else {
        // Handle other errors
        const errorMessage = typeof errorData?.detail === 'string'
          ? errorData.detail
          : JSON.stringify(errorData?.detail || errorData || error.message);
        toast.error(`Failed to create instance: ${errorMessage}`);
      }
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: (data) => contentTypesAPI.updateInstance(instanceId, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['content-instance', instanceId]);
      queryClient.invalidateQueries(['content-instances', contentTypeId]);
      toast.success('Content instance updated successfully');
      navigate(`/content-types/${contentTypeId}/instances/${instanceId}`);
    },
    onError: (error) => {
      console.error('[UPDATE ERROR]', error);
      console.error('[UPDATE ERROR] Response:', error.response);
      console.error('[UPDATE ERROR] Response data:', error.response?.data);

      const errorData = error.response?.data;

      // Handle validation errors object
      if (errorData?.detail && typeof errorData.detail === 'object' && errorData.detail.validation_errors) {
        const errors = {};
        errorData.detail.validation_errors.forEach((err) => {
          const match = err.match(/attribute '(.+?)'/);
          if (match) {
            errors[match[1]] = err;
          }
        });
        setValidationErrors(errors);
        toast.error(`Validation errors: ${errorData.detail.validation_errors.join(', ')}`);
      } else if (errorData?.validation_errors) {
        // Legacy format
        const errors = {};
        errorData.validation_errors.forEach((err) => {
          const match = err.match(/attribute '(.+?)'/);
          if (match) {
            errors[match[1]] = err;
          }
        });
        setValidationErrors(errors);
        toast.error(`Validation errors: ${errorData.validation_errors.join(', ')}`);
      } else {
        // Handle other errors
        const errorMessage = typeof errorData?.detail === 'string'
          ? errorData.detail
          : JSON.stringify(errorData?.detail || errorData || error.message);
        toast.error(`Failed to update instance: ${errorMessage}`);
      }
    },
  });

  // Fetch available agents
  const { data: availableAgents } = useQuery({
    queryKey: ['agents'],
    queryFn: agentsAPI.list,
  });

  const handleFieldChange = (attributeName, value) => {
    setFormData((prev) => ({
      ...prev,
      [attributeName]: value,
    }));
    // Clear validation error for this field
    if (validationErrors[attributeName]) {
      setValidationErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[attributeName];
        return newErrors;
      });
    }
  };

  // Handle AI Assist button click for a field
  const handleAIAssist = (attribute) => {
    setTargetField(attribute);
    setShowAIAssist(true);
    setAgentTaskDescription(`Generate ${attribute.label || attribute.name} for this ${contentType.name}`);
  };

  // Invoke AI agent with streaming
  const handleInvokeAgent = () => {
    if (!selectedAgent || !agentTaskDescription.trim()) return;

    setStreamingText('');
    setStreamError(null);
    setIsStreaming(true);
    setIsInvoking(true);

    const parameters = {
      content_type: contentType.name,
      content_type_id: contentTypeId,
      target_field: targetField?.name,
      field_label: targetField?.label,
      field_type: targetField?.type,
      current_data: formData,
    };

    // Add JSON schema if this is a JSON field with a schema defined
    if (targetField?.type === 'json' && targetField?.ai_output_schema) {
      parameters.output_schema = targetField.ai_output_schema;
    }

    const requestBody = {
      agent_type: selectedAgent.id,
      task_description: agentTaskDescription,
      parameters,
    };

    const token = localStorage.getItem('access_token');

    fetch('http://localhost:8000/api/v1/agents/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        const readStream = () => {
          reader.read().then(({ done, value }) => {
            if (done) {
              setIsStreaming(false);
              setIsInvoking(false);
              return;
            }

            buffer += decoder.decode(value, { stream: true });
            const events = buffer.split('\n\n');
            buffer = events.pop() || '';

            events.forEach((event) => {
              const lines = event.split('\n');
              lines.forEach((line) => {
                if (line.startsWith('data: ')) {
                  try {
                    const jsonData = line.substring(6).trim();
                    if (jsonData) {
                      const data = JSON.parse(jsonData);

                      if (data.type === 'text') {
                        setStreamingText((prev) => prev + data.content);
                      } else if (data.type === 'done') {
                        setIsStreaming(false);
                        setIsInvoking(false);
                      } else if (data.type === 'error') {
                        setStreamError(data.message);
                        setIsStreaming(false);
                        setIsInvoking(false);
                      }
                    }
                  } catch (e) {
                    console.error('Error parsing SSE data:', e);
                  }
                }
              });
            });

            readStream();
          }).catch((error) => {
            console.error('Stream reading error:', error);
            setStreamError(error.message);
            setIsStreaming(false);
            setIsInvoking(false);
          });
        };

        readStream();
      })
      .catch((error) => {
        console.error('Streaming error:', error);
        setStreamError(error.message);
        setIsStreaming(false);
        setIsInvoking(false);
      });
  };

  // Extract JSON from potentially wrapped text
  const extractJSON = (text) => {
    // If field is JSON type, try to extract pure JSON
    if (targetField?.type !== 'json') {
      return text;
    }

    try {
      // First, try to parse as-is
      JSON.parse(text);
      return text; // Already valid JSON
    } catch (e) {
      // Try to extract JSON from markdown code fences
      const codeBlockMatch = text.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/);
      if (codeBlockMatch) {
        try {
          JSON.parse(codeBlockMatch[1]);
          return codeBlockMatch[1].trim();
        } catch (e2) {
          // Continue to next extraction method
        }
      }

      // Try to find JSON object/array by looking for { or [ at start
      const jsonMatch = text.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
      if (jsonMatch) {
        try {
          JSON.parse(jsonMatch[1]);
          return jsonMatch[1].trim();
        } catch (e3) {
          // Continue
        }
      }

      // If all extraction fails, return original text and show warning
      toast.error('Generated text is not valid JSON. Please check the output.');
      return text;
    }
  };

  // Insert generated content into target field
  const handleInsertGeneratedContent = () => {
    if (streamingText && targetField) {
      const contentToInsert = extractJSON(streamingText);

      setFormData((prev) => ({
        ...prev,
        [targetField.name]: contentToInsert,
      }));
      setShowAIAssist(false);
      setTargetField(null);
      setSelectedAgent(null);
      setAgentTaskDescription('');
      setStreamingText('');
      setIsStreaming(false);
      toast.success('Content inserted into field');
    }
  };

  // Append generated content to target field
  const handleAppendGeneratedContent = () => {
    if (streamingText && targetField) {
      const contentToAppend = extractJSON(streamingText);
      const currentValue = formData[targetField.name] || '';

      setFormData((prev) => ({
        ...prev,
        [targetField.name]: currentValue + '\n\n' + contentToAppend,
      }));
      setShowAIAssist(false);
      setTargetField(null);
      setSelectedAgent(null);
      setAgentTaskDescription('');
      setStreamingText('');
      setIsStreaming(false);
      toast.success('Content appended to field');
    }
  };

  const validateForm = () => {
    const errors = {};

    if (!contentType?.attributes) return true;

    // Check required fields
    contentType.attributes.forEach((attr) => {
      if (attr.required && !formData[attr.name]) {
        errors[attr.name] = `${attr.label || attr.name} is required`;
      }
    });

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      toast.error('Please fix validation errors');
      return;
    }

    const payload = {
      data: formData,
      status,
    };

    if (instanceId) {
      updateMutation.mutate(payload);
    } else {
      createMutation.mutate(payload);
    }
  };

  const handleCancel = () => {
    navigate(`/content-types/${contentTypeId}`);
  };

  if (loadingContentType || (instanceId && loadingInstance)) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p className="mt-2 text-sm text-gray-500">Loading...</p>
        </div>
      </Layout>
    );
  }

  if (!contentType) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-red-600">Content type not found</p>
        </div>
      </Layout>
    );
  }

  // Sort attributes by order_index
  const sortedAttributes = [...(contentType.attributes || [])].sort(
    (a, b) => (a.order_index || 0) - (b.order_index || 0)
  );

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={handleCancel}
              className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700"
            >
              <ArrowLeftIcon className="h-5 w-5 mr-1" />
              Back to {contentType.name}
            </button>
          </div>
        </div>

        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {instanceId ? 'Edit' : 'Create'} {contentType.name}
          </h1>
          {contentType.description && (
            <p className="mt-1 text-sm text-gray-500">
              {contentType.description}
            </p>
          )}
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
            <div className="space-y-6">
              {sortedAttributes.map((attribute) => (
                <DynamicFormField
                  key={attribute.name}
                  attribute={attribute}
                  value={formData[attribute.name]}
                  onChange={(value) => handleFieldChange(attribute.name, value)}
                  error={validationErrors[attribute.name]}
                  contentTypeId={contentTypeId}
                  instanceId={instanceId}
                  onAIAssist={handleAIAssist}
                />
              ))}

              {sortedAttributes.length === 0 && (
                <p className="text-sm text-gray-500 text-center py-8">
                  This content type has no attributes defined.
                </p>
              )}
            </div>
          </div>

          {/* Status and Actions */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="draft">Draft</option>
                  <option value="in_review">In Review</option>
                  <option value="published">Published</option>
                  <option value="archived">Archived</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-3">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  <XMarkIcon className="h-5 w-5 mr-2" />
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isPending || updateMutation.isPending}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <CheckIcon className="h-5 w-5 mr-2" />
                  {createMutation.isPending || updateMutation.isPending
                    ? 'Saving...'
                    : instanceId
                    ? 'Update'
                    : 'Create'}
                </button>
              </div>
            </div>
          </div>
        </form>

        {/* AI Assist Panel */}
        {showAIAssist && (
          <div className="fixed inset-0 z-50 overflow-hidden">
            <div
              className="absolute inset-0 bg-gray-500 bg-opacity-75"
              onClick={() => setShowAIAssist(false)}
            />

            <div className="fixed inset-y-0 right-0 max-w-xl w-full bg-white shadow-xl flex flex-col">
              {/* Header */}
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <SparklesIcon className="h-6 w-6 text-purple-600 mr-2" />
                    <h2 className="text-xl font-semibold text-gray-900">
                      AI Assist
                    </h2>
                  </div>
                  <button
                    onClick={() => setShowAIAssist(false)}
                    className="text-gray-400 hover:text-gray-500"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Generate content for: {targetField?.label || targetField?.name}
                </p>
              </div>

              {/* Content */}
              <div className="flex-1 overflow-y-auto px-6 py-4">
                {!isStreaming && !streamingText ? (
                  <>
                    {/* Agent Selection */}
                    <div className="mb-6">
                      <h3 className="text-sm font-medium text-gray-700 mb-3">
                        Select an AI Agent
                      </h3>
                      <div className="space-y-2">
                        {(() => {
                          // Filter agents based on field's ai_agents configuration
                          const fieldAgents = targetField?.ai_agents || [];
                          const filteredAgents = availableAgents?.filter(agent =>
                            fieldAgents.includes(agent.id)
                          ) || [];

                          if (filteredAgents.length === 0) {
                            return (
                              <p className="text-sm text-gray-500 text-center py-4">
                                No AI agents configured for this field
                              </p>
                            );
                          }

                          return filteredAgents.map((agent) => (
                            <button
                              key={agent.id}
                              type="button"
                              onClick={() => setSelectedAgent(agent)}
                              className={`w-full text-left p-3 rounded-lg border-2 transition-colors ${
                                selectedAgent?.id === agent.id
                                  ? 'border-purple-500 bg-purple-50'
                                  : 'border-gray-200 hover:border-gray-300'
                              }`}
                            >
                              <p className="font-medium text-gray-900">
                                {agent.name}
                              </p>
                              <p className="text-xs text-gray-500 mt-1">
                                {agent.description}
                              </p>
                            </button>
                          ));
                        })()}
                      </div>
                    </div>

                    {/* Task Description */}
                    {selectedAgent && (
                      <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          What should the agent create?
                        </label>
                        <textarea
                          value={agentTaskDescription}
                          onChange={(e) => setAgentTaskDescription(e.target.value)}
                          rows={4}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder={`Describe what you want for ${targetField?.label || targetField?.name}...`}
                        />
                        <p className="mt-1 text-xs text-gray-500">
                          Be specific about what you want. The agent will use
                          your content type context automatically.
                        </p>

                        {/* Context Info */}
                        <div className="mt-4 bg-gray-50 border border-gray-200 rounded-lg p-4">
                          <h4 className="text-sm font-semibold text-gray-900 mb-2">
                            Context
                          </h4>
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div className="bg-white rounded px-2 py-1 border border-gray-200">
                              <span className="font-medium text-gray-700">
                                Content Type:
                              </span>
                              <span className="ml-1 text-gray-600">
                                {contentType.name}
                              </span>
                            </div>
                            <div className="bg-white rounded px-2 py-1 border border-gray-200">
                              <span className="font-medium text-gray-700">
                                Field:
                              </span>
                              <span className="ml-1 text-gray-600">
                                {targetField?.label || targetField?.name}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Invoke Button */}
                    {selectedAgent && (
                      <button
                        type="button"
                        onClick={handleInvokeAgent}
                        disabled={!agentTaskDescription.trim() || isInvoking}
                        className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                      >
                        {isInvoking && (
                          <ArrowPathIcon className="h-5 w-5 mr-2 animate-spin" />
                        )}
                        {isInvoking ? 'Starting...' : 'Generate Content'}
                      </button>
                    )}
                  </>
                ) : (
                  <>
                    {/* Streaming Content Display */}
                    <div className="mb-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          {isStreaming && (
                            <ArrowPathIcon className="h-5 w-5 text-purple-600 mr-2 animate-spin" />
                          )}
                          <h3 className="text-sm font-medium text-gray-700">
                            {isStreaming ? 'Generating...' : 'Complete!'}
                          </h3>
                        </div>
                        {!isStreaming && streamingText && (
                          <CheckIcon className="h-5 w-5 text-green-600" />
                        )}
                      </div>

                      {/* Streaming text display */}
                      <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 max-h-96 overflow-y-auto">
                        <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono">
                          {streamingText}
                          {isStreaming && (
                            <span className="animate-pulse">▊</span>
                          )}
                        </pre>
                      </div>

                      {/* Error display */}
                      {streamError && (
                        <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                          <p className="text-sm text-red-800">{streamError}</p>
                        </div>
                      )}
                    </div>

                    {/* Action Buttons */}
                    {!isStreaming && streamingText && (
                      <div className="space-y-2">
                        <button
                          type="button"
                          onClick={handleInsertGeneratedContent}
                          className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                        >
                          Replace Field Content
                        </button>
                        <button
                          type="button"
                          onClick={handleAppendGeneratedContent}
                          className="w-full px-4 py-2 bg-white text-purple-600 border border-purple-600 rounded-lg hover:bg-purple-50"
                        >
                          Append to Field
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setStreamingText('');
                            setSelectedAgent(null);
                            setAgentTaskDescription('');
                            setStreamError(null);
                          }}
                          className="w-full px-4 py-2 bg-white text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
                        >
                          Start Over
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
