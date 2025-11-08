/**
 * Review Queue page - for editors to review content
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import {
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';
import Layout from '../components/Layout';

export default function ReviewQueue() {
  const queryClient = useQueryClient();
  const [selectedInstance, setSelectedInstance] = useState(null);
  const [reviewDecision, setReviewDecision] = useState('published');
  const [reviewComments, setReviewComments] = useState('');

  // Fetch all content instances with "in_review" status
  const { data: pendingContent, isLoading } = useQuery({
    queryKey: ['pending-reviews'],
    queryFn: () => contentTypesAPI.listAllInstances({ status: 'in_review' }),
  });

  // Fetch selected content instance details
  const { data: contentDetails } = useQuery({
    queryKey: ['content-instance', selectedInstance],
    queryFn: () => contentTypesAPI.getInstance(selectedInstance),
    enabled: !!selectedInstance,
  });

  // Update content instance status mutation
  const updateStatusMutation = useMutation({
    mutationFn: ({ instanceId, status }) =>
      contentTypesAPI.updateInstance(instanceId, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries(['pending-reviews']);
      queryClient.invalidateQueries(['all-content-instances']);
      queryClient.invalidateQueries(['content-instance', selectedInstance]);

      toast.success(
        reviewDecision === 'published'
          ? 'Content approved and published!'
          : reviewDecision === 'draft'
          ? 'Content sent back for revision'
          : 'Content archived'
      );

      setSelectedInstance(null);
      setReviewDecision('published');
      setReviewComments('');
    },
    onError: (error) => {
      toast.error(
        `Failed to update content: ${
          error.response?.data?.detail || error.message
        }`
      );
    },
  });

  const handleReview = (e) => {
    e.preventDefault();

    if (!selectedInstance) return;

    updateStatusMutation.mutate({
      instanceId: selectedInstance,
      status: reviewDecision,
    });
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Review Queue</h1>
          <p className="mt-1 text-sm text-gray-500">
            Review and approve content submissions
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Pending List */}
          <div className="lg:col-span-1">
            <div className="bg-white shadow rounded-lg overflow-hidden">
              <div className="p-4 border-b bg-gray-50">
                <h2 className="font-medium text-gray-900">
                  Pending Review ({pendingContent?.length || 0})
                </h2>
              </div>

              <div className="divide-y divide-gray-200 max-h-[600px] overflow-y-auto">
                {isLoading ? (
                  <div className="p-8 text-center text-gray-500">Loading...</div>
                ) : pendingContent && pendingContent.length > 0 ? (
                  pendingContent.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => setSelectedInstance(item.id)}
                      className={`w-full text-left p-4 hover:bg-gray-50 transition-colors ${
                        selectedInstance === item.id ? 'bg-blue-50' : ''
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-gray-900 truncate">
                            {item.data?.title || item.data?.name || `Content ${item.id.substring(0, 8)}`}
                          </p>
                          <p className="text-sm text-gray-500 mt-1">
                            {item.content_type.name}
                            {item.data?.subject && ` • ${item.data.subject}`}
                          </p>
                          <p className="text-xs text-gray-400 mt-1">
                            Updated{' '}
                            {new Date(item.updated_at).toLocaleDateString()}
                          </p>
                        </div>
                        <ClockIcon className="h-5 w-5 text-yellow-500 ml-2" />
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="p-8 text-center text-gray-500">
                    <CheckCircleIcon className="h-12 w-12 mx-auto mb-2 text-green-400" />
                    <p>No pending reviews!</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Review Panel */}
          <div className="lg:col-span-2">
            {selectedInstance && contentDetails ? (
              <div className="bg-white shadow rounded-lg">
                {/* Content Preview */}
                <div className="p-6 border-b">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h2 className="text-xl font-bold text-gray-900">
                        {contentDetails.data?.title || contentDetails.data?.name || `Content ${contentDetails.id.substring(0, 8)}`}
                      </h2>
                      <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                        <span>{contentDetails.content_type.name}</span>
                        {contentDetails.data?.subject && (
                          <>
                            <span>•</span>
                            <span className="capitalize">{contentDetails.data.subject}</span>
                          </>
                        )}
                        {contentDetails.data?.grade_level && (
                          <>
                            <span>•</span>
                            <span>Grade {contentDetails.data.grade_level}</span>
                          </>
                        )}
                      </div>
                    </div>
                    <Link
                      to={`/content-types/${contentDetails.content_type_id}/instances/${selectedInstance}`}
                      className="text-sm text-primary-600 hover:text-primary-700"
                    >
                      View Full Content →
                    </Link>
                  </div>

                  {/* Learning Objectives */}
                  {contentDetails.data?.learning_objectives && (
                    <div className="mt-4">
                      <h3 className="text-sm font-medium text-gray-700 mb-2">
                        Learning Objectives:
                      </h3>
                      <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                        <pre className="whitespace-pre-wrap font-sans">
                          {typeof contentDetails.data.learning_objectives === 'string'
                            ? contentDetails.data.learning_objectives.substring(0, 300)
                            : JSON.stringify(contentDetails.data.learning_objectives, null, 2).substring(0, 300)}
                          ...
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* Content Preview */}
                  {contentDetails.data?.lesson_content && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-md">
                      <h3 className="text-sm font-medium text-gray-700 mb-2">
                        Content Preview:
                      </h3>
                      <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans overflow-auto max-h-64">
                        {contentDetails.data.lesson_content.substring(0, 500)}...
                      </pre>
                    </div>
                  )}
                </div>

                {/* Review Form */}
                <form onSubmit={handleReview} className="p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Review Decision
                  </h3>

                  <div className="space-y-4">
                    {/* Decision */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Action *
                      </label>
                      <div className="space-y-2">
                        <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                          <input
                            type="radio"
                            name="decision"
                            value="published"
                            checked={reviewDecision === 'published'}
                            onChange={(e) => setReviewDecision(e.target.value)}
                            className="mr-3"
                          />
                          <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                          <div>
                            <span className="text-sm font-medium">Approve & Publish</span>
                            <p className="text-xs text-gray-500">Make this content live</p>
                          </div>
                        </label>
                        <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                          <input
                            type="radio"
                            name="decision"
                            value="draft"
                            checked={reviewDecision === 'draft'}
                            onChange={(e) => setReviewDecision(e.target.value)}
                            className="mr-3"
                          />
                          <ClockIcon className="h-5 w-5 text-yellow-500 mr-2" />
                          <div>
                            <span className="text-sm font-medium">Send Back for Revision</span>
                            <p className="text-xs text-gray-500">Author can make changes</p>
                          </div>
                        </label>
                        <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                          <input
                            type="radio"
                            name="decision"
                            value="archived"
                            checked={reviewDecision === 'archived'}
                            onChange={(e) => setReviewDecision(e.target.value)}
                            className="mr-3"
                          />
                          <XCircleIcon className="h-5 w-5 text-red-500 mr-2" />
                          <div>
                            <span className="text-sm font-medium">Archive</span>
                            <p className="text-xs text-gray-500">Remove from active content</p>
                          </div>
                        </label>
                      </div>
                    </div>

                    {/* Comments */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Comments & Feedback (Optional)
                      </label>
                      <textarea
                        value={reviewComments}
                        onChange={(e) => setReviewComments(e.target.value)}
                        rows={4}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="Provide feedback to the author..."
                      />
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="mt-6 flex justify-end space-x-3">
                    <button
                      type="button"
                      onClick={() => setSelectedInstance(null)}
                      className="px-4 py-2 text-gray-700 hover:text-gray-900"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={updateStatusMutation.isPending}
                      className={`px-4 py-2 text-white rounded-lg hover:opacity-90 disabled:opacity-50 ${
                        reviewDecision === 'published'
                          ? 'bg-green-600 hover:bg-green-700'
                          : reviewDecision === 'draft'
                          ? 'bg-yellow-600 hover:bg-yellow-700'
                          : 'bg-red-600 hover:bg-red-700'
                      }`}
                    >
                      {updateStatusMutation.isPending
                        ? 'Updating...'
                        : reviewDecision === 'published'
                        ? 'Approve & Publish'
                        : reviewDecision === 'draft'
                        ? 'Send Back for Revision'
                        : 'Archive Content'}
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              <div className="bg-white shadow rounded-lg p-12">
                <div className="text-center text-gray-500">
                  <ClockIcon className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                  <p className="text-lg font-medium">Select an item to review</p>
                  <p className="text-sm mt-2">
                    Choose content from the pending list to start your review
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}
