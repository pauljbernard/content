/**
 * Content Editor page - create and edit content
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeftIcon, CheckIcon } from '@heroicons/react/24/outline';
import { contentAPI } from '../services/api';
import useAuthStore from '../store/authStore';
import Layout from '../components/Layout';

export default function ContentEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
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
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Content *
            </h2>

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
      </div>
    </Layout>
  );
}
