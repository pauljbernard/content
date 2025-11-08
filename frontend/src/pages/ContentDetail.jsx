/**
 * Content Detail page - read-only view of content
 */
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  PencilIcon,
  DocumentCheckIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  StarIcon,
} from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';
import Layout from '../components/Layout';
import { contentAPI, reviewAPI } from '../services/api';
import useAuthStore from '../store/authStore';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ContentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { user } = useAuthStore();

  // Fetch content
  const { data: content, isLoading, error } = useQuery({
    queryKey: ['content', id],
    queryFn: () => contentAPI.get(id),
  });

  // Fetch reviews
  const { data: reviews } = useQuery({
    queryKey: ['reviews', id],
    queryFn: () => reviewAPI.getForContent(id),
    enabled: !!content && content.status !== 'draft',
  });

  // Submit for review mutation
  const submitMutation = useMutation({
    mutationFn: contentAPI.submit,
    onSuccess: () => {
      queryClient.invalidateQueries(['content', id]);
      alert('Content submitted for review successfully!');
    },
    onError: (error) => {
      alert('Failed to submit: ' + (error.response?.data?.detail || error.message));
    },
  });

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="text-center py-12">
          <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-red-500" />
          <h3 className="mt-2 text-lg font-medium text-gray-900">Error loading content</h3>
          <p className="mt-1 text-sm text-gray-500">{error.message}</p>
          <Link
            to="/content"
            className="mt-4 inline-flex items-center text-primary-600 hover:text-primary-700"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Content List
          </Link>
        </div>
      </Layout>
    );
  }

  const getStatusColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      in_review: 'bg-yellow-100 text-yellow-800',
      needs_revision: 'bg-orange-100 text-orange-800',
      approved: 'bg-green-100 text-green-800',
      published: 'bg-blue-100 text-blue-800',
      archived: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const canEdit = user && (
    user.id === content.author_id ||
    user.role === 'editor' ||
    user.role === 'knowledge_engineer'
  );

  const canSubmit = user && (
    user.id === content.author_id &&
    (content.status === 'draft' || content.status === 'needs_revision')
  );

  console.log('ContentDetail - canSubmit:', canSubmit, {
    user,
    content,
    userId: user?.id,
    authorId: content?.author_id,
    status: content?.status,
  });

  const handleSubmit = () => {
    console.log('handleSubmit called, id:', id);
    console.log('Calling submitMutation.mutate with id:', id);
    submitMutation.mutate(id);
  };

  const renderStars = (rating) => {
    return (
      <div className="flex items-center">
        {[1, 2, 3, 4, 5].map((star) => (
          star <= rating ? (
            <StarIconSolid key={star} className="h-5 w-5 text-yellow-400" />
          ) : (
            <StarIcon key={star} className="h-5 w-5 text-gray-300" />
          )
        ))}
      </div>
    );
  };

  return (
    <Layout>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link
            to="/content"
            className="inline-flex items-center text-sm text-primary-600 hover:text-primary-700 mb-4"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Content List
          </Link>

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900">{content.title}</h1>
              <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                <span className="capitalize">{content.content_type}</span>
                <span>•</span>
                <span>{content.subject}</span>
                {content.grade_level && (
                  <>
                    <span>•</span>
                    <span>Grade {content.grade_level}</span>
                  </>
                )}
                {content.state && (
                  <>
                    <span>•</span>
                    <span className="uppercase">{content.state}</span>
                  </>
                )}
              </div>
              <div className="mt-2 text-sm text-gray-500">
                Created {new Date(content.created_at).toLocaleDateString()} •
                Updated {new Date(content.updated_at).toLocaleDateString()}
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <span
                className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                  content.status
                )}`}
              >
                {content.status.replace('_', ' ')}
              </span>

              {canSubmit && (
                <button
                  onClick={handleSubmit}
                  disabled={submitMutation.isPending}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
                >
                  <DocumentCheckIcon className="h-4 w-4 mr-2" />
                  {submitMutation.isPending ? 'Submitting...' : (content.status === 'needs_revision' ? 'Resubmit for Review' : 'Submit for Review')}
                </button>
              )}

              {canEdit && (
                <Link
                  to={`/content/${id}/edit`}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  <PencilIcon className="h-4 w-4 mr-2" />
                  Edit
                </Link>
              )}
            </div>
          </div>
        </div>

        {/* Metadata Card */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Details</h2>
          <dl className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
            <div>
              <dt className="text-sm font-medium text-gray-500">Content Type</dt>
              <dd className="mt-1 text-sm text-gray-900 capitalize">{content.content_type}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Status</dt>
              <dd className="mt-1 text-sm text-gray-900 capitalize">
                {content.status.replace('_', ' ')}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Subject</dt>
              <dd className="mt-1 text-sm text-gray-900">{content.subject}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Grade Level</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {content.grade_level ? `Grade ${content.grade_level}` : 'Not specified'}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">State/District</dt>
              <dd className="mt-1 text-sm text-gray-900 uppercase">
                {content.state || 'Not specified'}
              </dd>
            </div>
            {content.curriculum_config_id && (
              <div>
                <dt className="text-sm font-medium text-gray-500">Curriculum Config</dt>
                <dd className="mt-1 text-sm text-gray-900">{content.curriculum_config_id}</dd>
              </div>
            )}
          </dl>

          {/* Standards */}
          {content.standards_aligned && content.standards_aligned.length > 0 && (
            <div className="mt-6">
              <dt className="text-sm font-medium text-gray-500 mb-2">Standards Aligned</dt>
              <dd className="flex flex-wrap gap-2">
                {content.standards_aligned.map((standard, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    {standard}
                  </span>
                ))}
              </dd>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Content</h2>
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {content.file_content || '*No content available*'}
            </ReactMarkdown>
          </div>
        </div>

        {/* Reviews */}
        {reviews && reviews.length > 0 && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Reviews ({reviews.length})
            </h2>
            <div className="space-y-6">
              {reviews.map((review) => (
                <div key={review.id} className="border-b border-gray-200 pb-6 last:border-b-0 last:pb-0">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {review.reviewer?.full_name || 'Reviewer'}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(review.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex items-center space-x-3">
                      {renderStars(review.rating)}
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          review.status === 'approved'
                            ? 'bg-green-100 text-green-800'
                            : review.status === 'needs_revision'
                            ? 'bg-orange-100 text-orange-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {review.status.replace('_', ' ')}
                      </span>
                    </div>
                  </div>

                  {review.comments && (
                    <div className="mt-2 text-sm text-gray-700 bg-gray-50 rounded-md p-3">
                      {review.comments}
                    </div>
                  )}

                  {review.checklist_results && Object.keys(review.checklist_results).length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs font-medium text-gray-700 mb-2">Checklist:</p>
                      <ul className="space-y-1">
                        {Object.entries(review.checklist_results).map(([key, value]) => (
                          <li key={key} className="flex items-center text-xs text-gray-600">
                            {value ? (
                              <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2" />
                            ) : (
                              <ExclamationTriangleIcon className="h-4 w-4 text-orange-500 mr-2" />
                            )}
                            <span className="capitalize">{key.replace('_', ' ')}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Needs Revision Notice */}
        {content.status === 'needs_revision' && reviews && reviews.length > 0 && (
          <div className="mt-6 bg-orange-50 border-l-4 border-orange-400 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <ExclamationTriangleIcon className="h-5 w-5 text-orange-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-orange-800">Revision Needed</h3>
                <div className="mt-2 text-sm text-orange-700">
                  <p>This content requires revisions before it can be approved. Please review the feedback above and make necessary changes.</p>
                </div>
                {canEdit && (
                  <div className="mt-4">
                    <Link
                      to={`/content/${id}/edit`}
                      className="inline-flex items-center text-sm font-medium text-orange-800 hover:text-orange-900"
                    >
                      Edit content
                      <span className="ml-2">→</span>
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
