/**
 * Search page for knowledge base and content
 */
import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { MagnifyingGlassIcon, FunnelIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import Layout from '../components/Layout';
import { searchAPI, knowledgeAPI } from '../services/api';

export default function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';

  const [query, setQuery] = useState(initialQuery);
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [filters, setFilters] = useState({
    type: searchParams.get('type') || 'all',
    subject: searchParams.get('subject') || '',
    state: searchParams.get('state') || '',
  });
  const [showFilters, setShowFilters] = useState(false);

  // Fetch search results
  const { data: results, isLoading, error } = useQuery({
    queryKey: ['search', searchQuery, filters],
    queryFn: () => {
      if (!searchQuery) return [];
      const filterParams = {};
      if (filters.type !== 'all') filterParams.type = filters.type;
      if (filters.subject) filterParams.subject = filters.subject;
      if (filters.state) filterParams.state = filters.state;
      return searchAPI.search(searchQuery, filterParams);
    },
    enabled: searchQuery.length >= 2,
  });

  // Fetch subjects and states for filters
  const { data: subjects } = useQuery({
    queryKey: ['subjects'],
    queryFn: knowledgeAPI.getSubjects,
  });

  const { data: states } = useQuery({
    queryKey: ['states'],
    queryFn: knowledgeAPI.getStates,
  });

  // Suggestions
  const { data: suggestions } = useQuery({
    queryKey: ['suggestions', query],
    queryFn: () => searchAPI.suggest(query),
    enabled: query.length >= 2 && query !== searchQuery,
  });

  useEffect(() => {
    if (initialQuery) {
      setSearchQuery(initialQuery);
    }
  }, [initialQuery]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.length >= 2) {
      setSearchQuery(query);
      updateSearchParams();
    }
  };

  const updateSearchParams = () => {
    const params = { q: query };
    if (filters.type !== 'all') params.type = filters.type;
    if (filters.subject) params.subject = filters.subject;
    if (filters.state) params.state = filters.state;
    setSearchParams(params);
  };

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setFilters({ type: 'all', subject: '', state: '' });
  };

  const highlightMatch = (text, searchTerm) => {
    if (!searchTerm) return text;
    const parts = text.split(new RegExp(`(${searchTerm})`, 'gi'));
    return parts.map((part, index) =>
      part.toLowerCase() === searchTerm.toLowerCase() ? (
        <mark key={index} className="bg-yellow-200 font-semibold">
          {part}
        </mark>
      ) : (
        part
      )
    );
  };

  const getResultTypeLabel = (type) => {
    const labels = {
      knowledge_file: 'Knowledge Base',
      config: 'Curriculum Config',
      content: 'Content',
    };
    return labels[type] || type;
  };

  const getResultTypeColor = (type) => {
    const colors = {
      knowledge_file: 'bg-blue-100 text-blue-800',
      config: 'bg-purple-100 text-purple-800',
      content: 'bg-green-100 text-green-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  const groupedResults = results?.reduce((acc, result) => {
    if (!acc[result.type]) acc[result.type] = [];
    acc[result.type].push(result);
    return acc;
  }, {}) || {};

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Search</h1>
          <p className="mt-2 text-sm text-gray-600">
            Search across knowledge base files, curriculum configs, and content
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <form onSubmit={handleSearch} className="relative">
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search for topics, standards, or content..."
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />

                {/* Suggestions dropdown */}
                {suggestions && suggestions.length > 0 && query !== searchQuery && (
                  <div className="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    {suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => {
                          setQuery(suggestion);
                          setSearchQuery(suggestion);
                        }}
                        className="w-full text-left px-4 py-2 hover:bg-gray-100"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <button
                type="submit"
                disabled={query.length < 2}
                className="px-6 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Search
              </button>

              <button
                type="button"
                onClick={() => setShowFilters(!showFilters)}
                className="px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <FunnelIcon className="h-5 w-5" />
              </button>
            </div>
          </form>
        </div>

        {/* Filters */}
        {showFilters && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-gray-900">Filters</h3>
              <button
                onClick={clearFilters}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                Clear all
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Type
                </label>
                <select
                  value={filters.type}
                  onChange={(e) => handleFilterChange('type', e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  <option value="all">All Types</option>
                  <option value="knowledge_file">Knowledge Base</option>
                  <option value="config">Curriculum Config</option>
                  <option value="content">Content</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Subject
                </label>
                <select
                  value={filters.subject}
                  onChange={(e) => handleFilterChange('subject', e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  <option value="">All Subjects</option>
                  {subjects?.map((subject) => (
                    <option key={subject} value={subject}>
                      {subject}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  State/District
                </label>
                <select
                  value={filters.state}
                  onChange={(e) => handleFilterChange('state', e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  <option value="">All States</option>
                  {states?.map((state) => (
                    <option key={state} value={state}>
                      {state}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        <div>
          {isLoading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Searching...</p>
            </div>
          )}

          {error && (
            <div className="text-center py-12">
              <p className="text-red-600">Error: {error.message}</p>
            </div>
          )}

          {!isLoading && !error && searchQuery && (
            <>
              {results?.length === 0 ? (
                <div className="text-center py-12">
                  <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No results found</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Try adjusting your search or filters
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-700">
                      Found <span className="font-medium">{results.length}</span> results for{' '}
                      <span className="font-medium">"{searchQuery}"</span>
                    </p>
                  </div>

                  {/* Grouped Results */}
                  {Object.entries(groupedResults).map(([type, typeResults]) => (
                    <div key={type}>
                      <h2 className="text-lg font-medium text-gray-900 mb-3">
                        {getResultTypeLabel(type)} ({typeResults.length})
                      </h2>
                      <div className="space-y-3">
                        {typeResults.map((result, idx) => (
                          <div
                            key={idx}
                            className="bg-white p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2">
                                  <span
                                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getResultTypeColor(
                                      result.type
                                    )}`}
                                  >
                                    {getResultTypeLabel(result.type)}
                                  </span>
                                  {result.type === 'knowledge_file' ? (
                                    <Link
                                      to={`/knowledge?path=${result.path}`}
                                      className="text-base font-medium text-primary-600 hover:text-primary-700"
                                    >
                                      {result.title}
                                    </Link>
                                  ) : (
                                    <span className="text-base font-medium text-gray-900">
                                      {result.title}
                                    </span>
                                  )}
                                </div>
                                <p className="text-sm text-gray-600 mb-2">
                                  {highlightMatch(result.excerpt, searchQuery)}
                                </p>
                                <p className="text-xs text-gray-500">{result.path}</p>
                              </div>
                              <div className="ml-4">
                                {result.type === 'knowledge_file' && (
                                  <Link
                                    to={`/knowledge?path=${result.path}`}
                                    className="text-sm text-primary-600 hover:text-primary-700"
                                  >
                                    View →
                                  </Link>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}

          {!searchQuery && (
            <div className="text-center py-12">
              <MagnifyingGlassIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Start searching</h3>
              <p className="mt-1 text-sm text-gray-500">
                Enter a search term to find knowledge base files, configs, and content
              </p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
