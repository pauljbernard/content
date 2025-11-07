/**
 * Content Editor page - create and edit content
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  CheckIcon,
  SparklesIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { contentAPI, agentsAPI } from '../services/api';
import useAuthStore from '../store/authStore';
import Layout from '../components/Layout';

export default function ContentEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const queryClient = useQueryClient();
  const { user } = useAuthStore();

  const isEditing = !!id;

  const [formData, setFormData] = useState({
    title: '',
    content_type: 'lesson',
    subject: 'mathematics',
    grade_level: '',
    state: '',
    file_content: '',
    learning_objectives: [],
    duration_minutes: '',
  });

  const [objectiveInput, setObjectiveInput] = useState('');
  const [showAIAssist, setShowAIAssist] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [agentTaskDescription, setAgentTaskDescription] = useState('');
  const [activeJobId, setActiveJobId] = useState(null);

  // Handle pre-filled content from agent results
  useEffect(() => {
    if (location.state?.generatedContent) {
      const { content } = location.state.generatedContent;
      setFormData((prev) => ({
        ...prev,
        file_content: content,
      }));
      // Clear the location state
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state, location.pathname, navigate]);

  // Load existing content if editing
  const { data: existingContent } = useQuery({
    queryKey: ['content', id],
    queryFn: () => contentAPI.get(id),
    enabled: isEditing,
  });

  useEffect(() => {
    if (existingContent) {
      setFormData({
        title: existingContent.title || '',
        content_type: existingContent.content_type || 'lesson',
        subject: existingContent.subject || 'mathematics',
        grade_level: existingContent.grade_level || '',
        state: existingContent.state || '',
        file_content: existingContent.file_content || '',
        learning_objectives: existingContent.learning_objectives || [],
        duration_minutes: existingContent.duration_minutes || '',
      });
    }
  }, [existingContent]);

  // Create mutation
  const createMutation = useMutation({
    mutationFn: contentAPI.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['content'] });
      navigate(`/content/${data.id}`);
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => contentAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['content'] });
      navigate(`/content/${id}`);
    },
  });

  // Submit mutation
  const submitMutation = useMutation({
    mutationFn: contentAPI.submit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['content'] });
      navigate('/content');
    },
  });

  // Available agents query
  const { data: availableAgents } = useQuery({
    queryKey: ['agents'],
    queryFn: agentsAPI.list,
  });

  // Invoke agent mutation
  const invokeAgentMutation = useMutation({
    mutationFn: ({ agentType, taskDescription, parameters }) =>
      agentsAPI.invoke(agentType, taskDescription, parameters),
    onSuccess: (data) => {
      setActiveJobId(data.id);
    },
  });

  // Poll for job status
  const { data: jobStatus } = useQuery({
    queryKey: ['agent-job-status', activeJobId],
    queryFn: () => agentsAPI.getJobStatus(activeJobId),
    enabled: !!activeJobId,
    refetchInterval: (data) => {
      if (data?.status === 'running' || data?.status === 'queued') {
        return 2000; // Poll every 2 seconds
      }
      return false;
    },
  });

  // Get suggested agents based on content type
  const getSuggestedAgents = () => {
    if (!availableAgents) return [];

    const suggestions = {
      lesson: ['content-developer', 'curriculum-architect'],
      assessment: ['assessment-designer', 'content-developer'],
      activity: ['content-developer'],
      guide: ['content-developer'],
    };

    const suggestedIds = suggestions[formData.content_type] || [];
    return availableAgents.filter((agent) => suggestedIds.includes(agent.id));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddObjective = () => {
    if (objectiveInput.trim()) {
      setFormData((prev) => ({
        ...prev,
        learning_objectives: [...prev.learning_objectives, objectiveInput.trim()],
      }));
      setObjectiveInput('');
    }
  };

  const handleRemoveObjective = (index) => {
    setFormData((prev) => ({
      ...prev,
      learning_objectives: prev.learning_objectives.filter((_, i) => i !== index),
    }));
  };

  const handleSave = (e) => {
    e.preventDefault();

    const data = {
      ...formData,
      duration_minutes: formData.duration_minutes
        ? parseInt(formData.duration_minutes)
        : null,
    };

    if (isEditing) {
      updateMutation.mutate({ id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const handleSubmitForReview = () => {
    if (isEditing) {
      submitMutation.mutate(id);
    }
  };

  const handleInvokeAgent = () => {
    if (!selectedAgent || !agentTaskDescription.trim()) return;

    const parameters = {
      subject: formData.subject,
      grade_level: formData.grade_level,
      state: formData.state,
      content_type: formData.content_type,
    };

    invokeAgentMutation.mutate({
      agentType: selectedAgent.id,
      taskDescription: agentTaskDescription,
      parameters,
    });
  };

  const handleInsertGeneratedContent = () => {
    if (jobStatus?.output_content) {
      setFormData((prev) => ({
        ...prev,
        file_content: jobStatus.output_content,
      }));
      setShowAIAssist(false);
      setActiveJobId(null);
      setSelectedAgent(null);
      setAgentTaskDescription('');
    }
  };

  const handleAppendGeneratedContent = () => {
    if (jobStatus?.output_content) {
      setFormData((prev) => ({
        ...prev,
        file_content: prev.file_content + '\n\n' + jobStatus.output_content,
      }));
      setShowAIAssist(false);
      setActiveJobId(null);
      setSelectedAgent(null);
      setAgentTaskDescription('');
    }
  };

  const canSubmit =
    isEditing &&
    existingContent?.status === 'draft' &&
    existingContent?.author_id === user?.id;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <button
              onClick={() => navigate('/content')}
              className="mr-4 p-2 text-gray-400 hover:text-gray-600"
            >
              <ArrowLeftIcon className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {isEditing ? 'Edit Content' : 'New Content'}
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                Create lessons, assessments, and activities
              </p>
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSave} className="space-y-6">
          {/* Basic Information */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Basic Information
            </h2>

            <div className="space-y-4">
              {/* Title */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Title *
                </label>
                <input
                  type="text"
                  name="title"
                  required
                  value={formData.title}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="e.g., Introduction to Fractions"
                />
              </div>

              {/* Content Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Content Type *
                </label>
                <select
                  name="content_type"
                  required
                  value={formData.content_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="lesson">Lesson</option>
                  <option value="assessment">Assessment</option>
                  <option value="activity">Activity</option>
                  <option value="guide">Guide</option>
                </select>
              </div>

              {/* Subject & Grade Level */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Subject *
                  </label>
                  <select
                    name="subject"
                    required
                    value={formData.subject}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="mathematics">Mathematics</option>
                    <option value="ela">ELA</option>
                    <option value="science">Science</option>
                    <option value="social-studies">Social Studies</option>
                    <option value="world-languages">World Languages</option>
                    <option value="fine-arts">Fine Arts</option>
                    <option value="physical-education">Physical Education</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Grade Level
                  </label>
                  <input
                    type="text"
                    name="grade_level"
                    value={formData.grade_level}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="e.g., 5 or 9-12"
                  />
                </div>
              </div>

              {/* State & Duration */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    State/District
                  </label>
                  <input
                    type="text"
                    name="state"
                    value={formData.state}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="e.g., texas, california (optional)"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Duration (minutes)
                  </label>
                  <input
                    type="number"
                    name="duration_minutes"
                    value={formData.duration_minutes}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="e.g., 45"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Learning Objectives */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Learning Objectives
            </h2>

            <div className="space-y-3">
              {formData.learning_objectives.map((objective, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                >
                  <span className="text-sm text-gray-700">{objective}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveObjective(index)}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}

              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={objectiveInput}
                  onChange={(e) => setObjectiveInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      handleAddObjective();
                    }
                  }}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="Add a learning objective..."
                />
                <button
                  type="button"
                  onClick={handleAddObjective}
                  className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
                >
                  Add
                </button>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-medium text-gray-900">Content *</h2>
              <button
                type="button"
                onClick={() => setShowAIAssist(true)}
                className="inline-flex items-center px-3 py-1.5 border border-purple-300 text-sm font-medium rounded-md text-purple-700 bg-purple-50 hover:bg-purple-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              >
                <SparklesIcon className="h-4 w-4 mr-1.5" />
                AI Assist
              </button>
            </div>

            <textarea
              name="file_content"
              required
              value={formData.file_content}
              onChange={handleChange}
              rows={20}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 font-mono text-sm"
              placeholder="Write your content in Markdown format..."
            />
            <p className="mt-2 text-sm text-gray-500">
              Supports Markdown formatting (headings, lists, bold, italic, code,
              etc.)
            </p>
          </div>

          {/* Actions */}
          <div className="flex justify-between items-center">
            <button
              type="button"
              onClick={() => navigate('/content')}
              className="px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              Cancel
            </button>

            <div className="flex space-x-3">
              {canSubmit && (
                <button
                  type="button"
                  onClick={handleSubmitForReview}
                  disabled={submitMutation.isLoading}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                >
                  {submitMutation.isLoading ? 'Submitting...' : 'Submit for Review'}
                </button>
              )}

              <button
                type="submit"
                disabled={createMutation.isLoading || updateMutation.isLoading}
                className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
              >
                <CheckIcon className="h-5 w-5 mr-2" />
                {createMutation.isLoading || updateMutation.isLoading
                  ? 'Saving...'
                  : isEditing
                  ? 'Save Changes'
                  : 'Create Content'}
              </button>
            </div>
          </div>
        </form>

        {/* AI Assist Panel */}
        {showAIAssist && (
          <div className="fixed inset-0 z-50 overflow-hidden">
            <div className="absolute inset-0 bg-gray-500 bg-opacity-75" onClick={() => setShowAIAssist(false)} />

            <div className="fixed inset-y-0 right-0 max-w-xl w-full bg-white shadow-xl flex flex-col">
              {/* Header */}
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <SparklesIcon className="h-6 w-6 text-purple-600 mr-2" />
                    <h2 className="text-xl font-semibold text-gray-900">AI Assist</h2>
                  </div>
                  <button
                    onClick={() => setShowAIAssist(false)}
                    className="text-gray-400 hover:text-gray-500"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Use AI agents to help generate content faster
                </p>
              </div>

              {/* Content */}
              <div className="flex-1 overflow-y-auto px-6 py-4">
                {!activeJobId ? (
                  <>
                    {/* Suggested Agents */}
                    <div className="mb-6">
                      <h3 className="text-sm font-medium text-gray-700 mb-3">
                        Suggested for {formData.content_type}
                      </h3>
                      <div className="space-y-2">
                        {getSuggestedAgents().map((agent) => (
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
                            <p className="font-medium text-gray-900">{agent.name}</p>
                            <p className="text-xs text-gray-500 mt-1">{agent.description}</p>
                            <p className="text-xs text-purple-600 mt-1">
                              {agent.productivity_gain} faster • {agent.estimated_time}
                            </p>
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Task Description */}
                    {selectedAgent && (
                      <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          What do you want the agent to create?
                        </label>
                        <textarea
                          value={agentTaskDescription}
                          onChange={(e) => setAgentTaskDescription(e.target.value)}
                          rows={4}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder={`Example: Create a ${formData.content_type} about ${formData.subject} for grade ${formData.grade_level || 'K-12'}...`}
                        />
                        <p className="mt-1 text-xs text-gray-500">
                          Be specific about what you want. The agent will use your subject,
                          grade level, and state automatically.
                        </p>
                      </div>
                    )}

                    {/* Invoke Button */}
                    {selectedAgent && (
                      <button
                        type="button"
                        onClick={handleInvokeAgent}
                        disabled={
                          !agentTaskDescription.trim() || invokeAgentMutation.isLoading
                        }
                        className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {invokeAgentMutation.isLoading ? 'Starting...' : 'Generate Content'}
                      </button>
                    )}
                  </>
                ) : (
                  <>
                    {/* Job Progress */}
                    <div className="mb-6">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-sm font-medium text-gray-700">
                          {jobStatus?.status === 'running' ? 'Generating...' :
                           jobStatus?.status === 'queued' ? 'Queued...' :
                           jobStatus?.status === 'completed' ? 'Complete!' :
                           'Failed'}
                        </h3>
                        <span className="text-sm text-gray-500">
                          {jobStatus?.progress_percentage || 0}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${jobStatus?.progress_percentage || 0}%` }}
                        />
                      </div>
                      {jobStatus?.progress_message && (
                        <p className="mt-2 text-sm text-gray-600">
                          {jobStatus.progress_message}
                        </p>
                      )}
                    </div>

                    {/* Generated Content Preview */}
                    {jobStatus?.status === 'completed' && jobStatus?.output_content && (
                      <>
                        <div className="mb-4">
                          <h3 className="text-sm font-medium text-gray-700 mb-2">
                            Generated Content
                          </h3>
                          <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 max-h-96 overflow-y-auto">
                            <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono">
                              {jobStatus.output_content}
                            </pre>
                          </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="space-y-2">
                          <button
                            type="button"
                            onClick={handleInsertGeneratedContent}
                            className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                          >
                            Replace Content
                          </button>
                          <button
                            type="button"
                            onClick={handleAppendGeneratedContent}
                            className="w-full px-4 py-2 bg-white text-purple-600 border border-purple-600 rounded-lg hover:bg-purple-50"
                          >
                            Append to Content
                          </button>
                          <button
                            type="button"
                            onClick={() => {
                              setActiveJobId(null);
                              setSelectedAgent(null);
                              setAgentTaskDescription('');
                            }}
                            className="w-full px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                          >
                            Start Over
                          </button>
                        </div>
                      </>
                    )}

                    {/* Error Message */}
                    {jobStatus?.status === 'failed' && (
                      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-sm text-red-800">
                          {jobStatus.error_message || 'Failed to generate content'}
                        </p>
                        <button
                          type="button"
                          onClick={() => {
                            setActiveJobId(null);
                            setSelectedAgent(null);
                            setAgentTaskDescription('');
                          }}
                          className="mt-3 text-sm text-red-600 hover:text-red-700 font-medium"
                        >
                          Try Again
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
