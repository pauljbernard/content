/**
 * Standard Detail page - View full hierarchical structure of a standard
 */
import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  ArrowLeftIcon,
  ClipboardDocumentListIcon,
  MagnifyingGlassIcon,
  ChevronDownIcon,
  ChevronRightIcon,
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { standardsAPI } from '../services/api';

export default function StandardDetail() {
  const { standardId } = useParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [expandedDomains, setExpandedDomains] = useState({});
  const [expandedStrands, setExpandedStrands] = useState({});

  // Query standard details
  const { data: standard, isLoading, error } = useQuery({
    queryKey: ['standard', standardId],
    queryFn: () => standardsAPI.getById(standardId),
  });

  // Search within standard
  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setSearchResults(null);
      return;
    }

    try {
      const results = await standardsAPI.search(standardId, searchQuery);
      setSearchResults(results);
    } catch (err) {
      console.error('Search failed:', err);
    }
  };

  const toggleDomain = (domainId) => {
    setExpandedDomains(prev => ({
      ...prev,
      [domainId]: !prev[domainId]
    }));
  };

  const toggleStrand = (strandId) => {
    setExpandedStrands(prev => ({
      ...prev,
      [strandId]: !prev[strandId]
    }));
  };

  const getTypeBadgeColor = (type) => {
    const colors = {
      state: 'bg-blue-100 text-blue-800',
      national: 'bg-purple-100 text-purple-800',
      international: 'bg-green-100 text-green-800',
      district: 'bg-yellow-100 text-yellow-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  const getStatusBadgeColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      importing: 'bg-yellow-100 text-yellow-800',
      imported: 'bg-blue-100 text-blue-800',
      published: 'bg-green-100 text-green-800',
      archived: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  if (error || !standard) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <p className="text-sm text-red-800">Failed to load standard details</p>
          </div>
          <Link
            to="/standards"
            className="mt-4 inline-flex items-center text-primary-600 hover:text-primary-700"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Standards
          </Link>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link
            to="/standards"
            className="inline-flex items-center text-sm text-primary-600 hover:text-primary-700 mb-4"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-1" />
            Back to Standards
          </Link>

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center mb-2">
                <ClipboardDocumentListIcon className="h-8 w-8 text-primary-600 mr-3" />
                <h1 className="text-3xl font-bold text-gray-900">{standard.name}</h1>
              </div>
              {standard.description && (
                <p className="text-gray-600 mt-2">{standard.description}</p>
              )}
            </div>
          </div>
        </div>

        {/* Metadata */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <dt className="text-sm font-medium text-gray-500">Code</dt>
              <dd className="mt-1 text-sm font-semibold text-primary-600">{standard.code}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Type</dt>
              <dd className="mt-1">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${getTypeBadgeColor(standard.type)}`}>
                  {standard.type}
                </span>
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Status</dt>
              <dd className="mt-1">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeColor(standard.status)}`}>
                  {standard.status}
                </span>
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Subject</dt>
              <dd className="mt-1 text-sm text-gray-900 capitalize">{standard.subject.replace('_', ' ')}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Source Organization</dt>
              <dd className="mt-1 text-sm text-gray-900">{standard.source_organization}</dd>
            </div>
            {standard.state && (
              <div>
                <dt className="text-sm font-medium text-gray-500">State</dt>
                <dd className="mt-1 text-sm text-gray-900 capitalize">{standard.state}</dd>
              </div>
            )}
            {standard.version && (
              <div>
                <dt className="text-sm font-medium text-gray-500">Version</dt>
                <dd className="mt-1 text-sm text-gray-900">{standard.version}</dd>
              </div>
            )}
            {standard.year && (
              <div>
                <dt className="text-sm font-medium text-gray-500">Year</dt>
                <dd className="mt-1 text-sm text-gray-900">{standard.year}</dd>
              </div>
            )}
            <div>
              <dt className="text-sm font-medium text-gray-500">Total Standards</dt>
              <dd className="mt-1 text-sm font-semibold text-gray-900">{standard.total_standards_count}</dd>
            </div>
            {standard.grade_levels && standard.grade_levels.length > 0 && (
              <div>
                <dt className="text-sm font-medium text-gray-500">Grade Levels</dt>
                <dd className="mt-1 text-sm text-gray-900">{standard.grade_levels.join(', ')}</dd>
              </div>
            )}
          </div>

          {standard.source_url && (
            <div className="mt-4">
              <dt className="text-sm font-medium text-gray-500">Source URL</dt>
              <dd className="mt-1">
                <a
                  href={standard.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-primary-600 hover:text-primary-700 underline"
                >
                  {standard.source_url}
                </a>
              </dd>
            </div>
          )}
        </div>

        {/* Search */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex items-center space-x-2">
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-primary-500 sm:text-sm"
                placeholder="Search within this standard..."
              />
            </div>
            <button
              onClick={handleSearch}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 text-sm font-medium"
            >
              Search
            </button>
            {searchResults && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  setSearchResults(null);
                }}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 text-sm font-medium"
              >
                Clear
              </button>
            )}
          </div>

          {searchResults && (
            <div className="mt-4 border-t border-gray-200 pt-4">
              <p className="text-sm text-gray-600 mb-2">
                Found {searchResults.total_matches} matching standard{searchResults.total_matches !== 1 ? 's' : ''}
              </p>
              {searchResults.matches.length > 0 && (
                <ul className="space-y-2">
                  {searchResults.matches.map((match, idx) => (
                    <li key={idx} className="bg-gray-50 p-3 rounded">
                      <div className="flex items-baseline justify-between">
                        <span className="font-mono text-sm font-semibold text-primary-600">{match.code}</span>
                        {match.grade_level && (
                          <span className="text-xs text-gray-500">Grade {match.grade_level}</span>
                        )}
                      </div>
                      <p className="text-sm text-gray-700 mt-1">{match.text}</p>
                      {(match.domain || match.strand) && (
                        <p className="text-xs text-gray-500 mt-1">
                          {match.domain && <span>{match.domain}</span>}
                          {match.domain && match.strand && <span> → </span>}
                          {match.strand && <span>{match.strand}</span>}
                        </p>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>

        {/* Hierarchical Structure */}
        {!searchResults && standard.structure && standard.structure.domains && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Standard Structure</h2>
            </div>
            <div className="p-6">
              {standard.structure.domains.map((domain, domainIdx) => (
                <div key={domainIdx} className="mb-4 border-l-4 border-primary-500 pl-4">
                  {/* Domain */}
                  <button
                    onClick={() => toggleDomain(domain.id)}
                    className="w-full flex items-center justify-between text-left py-2 hover:bg-gray-50 rounded"
                  >
                    <div className="flex items-center space-x-2">
                      {expandedDomains[domain.id] ? (
                        <ChevronDownIcon className="h-5 w-5 text-gray-400" />
                      ) : (
                        <ChevronRightIcon className="h-5 w-5 text-gray-400" />
                      )}
                      <span className="font-semibold text-gray-900">{domain.name}</span>
                      {domain.id && (
                        <span className="text-sm text-gray-500">({domain.id})</span>
                      )}
                    </div>
                  </button>

                  {/* Strands */}
                  {expandedDomains[domain.id] && domain.strands && (
                    <div className="ml-6 mt-2 space-y-2">
                      {domain.strands.map((strand, strandIdx) => (
                        <div key={strandIdx} className="border-l-2 border-blue-300 pl-4">
                          <button
                            onClick={() => toggleStrand(strand.id)}
                            className="w-full flex items-center justify-between text-left py-2 hover:bg-gray-50 rounded"
                          >
                            <div className="flex items-center space-x-2">
                              {expandedStrands[strand.id] ? (
                                <ChevronDownIcon className="h-4 w-4 text-gray-400" />
                              ) : (
                                <ChevronRightIcon className="h-4 w-4 text-gray-400" />
                              )}
                              <span className="font-medium text-gray-800">{strand.name}</span>
                              {strand.id && (
                                <span className="text-sm text-gray-500">({strand.id})</span>
                              )}
                            </div>
                          </button>

                          {/* Standards */}
                          {expandedStrands[strand.id] && strand.standards && (
                            <div className="ml-6 mt-2 space-y-2">
                              {strand.standards.map((std, stdIdx) => (
                                <div key={stdIdx} className="bg-gray-50 p-3 rounded">
                                  <div className="flex items-baseline justify-between mb-1">
                                    <span className="font-mono text-sm font-semibold text-primary-600">
                                      {std.code}
                                    </span>
                                    {std.grade_level && (
                                      <span className="text-xs text-gray-500">Grade {std.grade_level}</span>
                                    )}
                                  </div>
                                  <p className="text-sm text-gray-700">{std.text}</p>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Flat List Fallback */}
        {!searchResults && (!standard.structure || !standard.structure.domains || standard.structure.domains.length === 0) && standard.standards_list && standard.standards_list.length > 0 && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">All Standards</h2>
            </div>
            <div className="p-6 space-y-3">
              {standard.standards_list.map((std, idx) => (
                <div key={idx} className="bg-gray-50 p-3 rounded">
                  <div className="flex items-baseline justify-between mb-1">
                    <span className="font-mono text-sm font-semibold text-primary-600">{std.code}</span>
                    {std.grade_level && (
                      <span className="text-xs text-gray-500">Grade {std.grade_level}</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-700">{std.text}</p>
                  {(std.domain || std.strand) && (
                    <p className="text-xs text-gray-500 mt-1">
                      {std.domain && <span>{std.domain}</span>}
                      {std.domain && std.strand && <span> → </span>}
                      {std.strand && <span>{std.strand}</span>}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
