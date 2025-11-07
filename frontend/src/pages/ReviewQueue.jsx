/**
 * Review Queue page - for editors to review content
 */
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';
import { reviewAPI, contentAPI } from '../services/api';
import Layout from '../components/Layout';

export default function ReviewQueue() {
  const queryClient = useQueryClient();
  const [selectedContent, setSelectedContent] = useState(null);
  const [reviewForm, setReviewForm] = useState({
    status: 'approved',
    comments: '',
    rating: 5,
  });

  const { data: pendingContent, isLoading } = useQuery({
    queryKey: ['pending-reviews'],
    queryFn: reviewAPI.getPending,
  });

  const { data: contentDetails } = useQuery({
    queryKey: ['content', selectedContent],
    queryFn: () => contentAPI.get(selectedContent),
    enabled: !!selectedContent,
  });

  const createReviewMutation = useMutation({
    mutationFn: reviewAPI.create,
    onSuccess: async (data) => {
      // If review status is "approved", automatically publish the content
      if (reviewForm.status === 'approved') {
        try {
          await reviewAPI.approve(selectedContent);
          alert('Review submitted and content published successfully!');
        } catch (error) {
          alert('Review submitted, but publishing failed: ' + (error.response?.data?.detail || error.message));
        }
      } else {
        alert('Review submitted successfully!');
      }

      queryClient.invalidateQueries({ queryKey: ['pending-reviews'] });
      setSelectedContent(null);
      setReviewForm({
        status: 'approved',
        comments: '',
        rating: 5,
      });
    },
    onError: (error) => {
      alert('Failed to submit review: ' + (error.response?.data?.detail || error.message));
    },
  });

  const handleReview = (e) => {
    e.preventDefault();

    createReviewMutation.mutate({
      content_id: selectedContent,
      ...reviewForm,
      rating: parseInt(reviewForm.rating),
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
                      key={item.content_id}
                      onClick={() => setSelectedContent(item.content_id)}
                      className={`w-full text-left p-4 hover:bg-gray-50 transition-colors ${
                        selectedContent === item.content_id ? 'bg-blue-50' : ''
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-gray-900 truncate">
                            {item.title}
                          </p>
                          <p className="text-sm text-gray-500 mt-1 capitalize">
                            {item.content_type} • {item.subject}
                          </p>
                          <p className="text-xs text-gray-400 mt-1">
                            Submitted{' '}
                            {new Date(item.submitted_at).toLocaleDateString()}
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
            {selectedContent && contentDetails ? (
              <div className="bg-white shadow rounded-lg">
                {/* Content Preview */}
                <div className="p-6 border-b">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h2 className="text-xl font-bold text-gray-900">
                        {contentDetails.title}
                      </h2>
                      <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                        <span className="capitalize">
                          {contentDetails.content_type}
                        </span>
                        <span>•</span>
                        <span>{contentDetails.subject}</span>
                        {contentDetails.grade_level && (
                          <>
                            <span>•</span>
                            <span>Grade {contentDetails.grade_level}</span>
                          </>
                        )}
                      </div>
                    </div>
                    <Link
                      to={`/content/${selectedContent}`}
                      className="text-sm text-primary-600 hover:text-primary-700"
                    >
                      View Full Content →
                    </Link>
                  </div>

                  {/* Learning Objectives */}
                  {contentDetails.learning_objectives &&
                    contentDetails.learning_objectives.length > 0 && (
                      <div className="mt-4">
                        <h3 className="text-sm font-medium text-gray-700 mb-2">
                          Learning Objectives:
                        </h3>
                        <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                          {contentDetails.learning_objectives.map((obj, idx) => (
                            <li key={idx}>{obj}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                  {/* Content Preview */}
                  <div className="mt-4 p-4 bg-gray-50 rounded-md">
                    <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans overflow-auto max-h-64">
                      {contentDetails.file_content?.substring(0, 500)}...
                    </pre>
                  </div>
                </div>

                {/* Review Form */}
                <form onSubmit={handleReview} className="p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Your Review
                  </h3>

                  <div className="space-y-4">
                    {/* Decision */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Decision *
                      </label>
                      <div className="space-y-2">
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="status"
                            value="approved"
                            checked={reviewForm.status === 'approved'}
                            onChange={(e) =>
                              setReviewForm({
                                ...reviewForm,
                                status: e.target.value,
                              })
                            }
                            className="mr-2"
                          />
                          <CheckCircleIcon className="h-5 w-5 text-green-500 mr-1" />
                          <span className="text-sm">Approve</span>
                        </label>
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="status"
                            value="needs_revision"
                            checked={reviewForm.status === 'needs_revision'}
                            onChange={(e) =>
                              setReviewForm({
                                ...reviewForm,
                                status: e.target.value,
                              })
                            }
                            className="mr-2"
                          />
                          <ClockIcon className="h-5 w-5 text-yellow-500 mr-1" />
                          <span className="text-sm">Needs Revision</span>
                        </label>
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="status"
                            value="rejected"
                            checked={reviewForm.status === 'rejected'}
                            onChange={(e) =>
                              setReviewForm({
                                ...reviewForm,
                                status: e.target.value,
                              })
                            }
                            className="mr-2"
                          />
                          <XCircleIcon className="h-5 w-5 text-red-500 mr-1" />
                          <span className="text-sm">Reject</span>
                        </label>
                      </div>
                    </div>

                    {/* Rating */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Quality Rating (1-5)
                      </label>
                      <div className="flex items-center space-x-2">
                        {[1, 2, 3, 4, 5].map((star) => (
                          <button
                            key={star}
                            type="button"
                            onClick={() =>
                              setReviewForm({ ...reviewForm, rating: star })
                            }
                            className={`text-2xl ${
                              star <= reviewForm.rating
                                ? 'text-yellow-400'
                                : 'text-gray-300'
                            }`}
                          >
                            ★
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Comments */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Comments & Feedback
                      </label>
                      <textarea
                        value={reviewForm.comments}
                        onChange={(e) =>
                          setReviewForm({
                            ...reviewForm,
                            comments: e.target.value,
                          })
                        }
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
                      onClick={() => setSelectedContent(null)}
                      className="px-4 py-2 text-gray-700 hover:text-gray-900"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={createReviewMutation.isPending}
                      className={`px-4 py-2 text-white rounded-lg hover:opacity-90 disabled:opacity-50 ${
                        reviewForm.status === 'approved'
                          ? 'bg-green-600 hover:bg-green-700'
                          : reviewForm.status === 'needs_revision'
                          ? 'bg-yellow-600 hover:bg-yellow-700'
                          : 'bg-red-600 hover:bg-red-700'
                      }`}
                    >
                      {createReviewMutation.isPending
                        ? reviewForm.status === 'approved'
                          ? 'Approving & Publishing...'
                          : 'Submitting...'
                        : reviewForm.status === 'approved'
                        ? 'Approve & Publish'
                        : reviewForm.status === 'needs_revision'
                        ? 'Request Revision'
                        : 'Reject Content'}
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
