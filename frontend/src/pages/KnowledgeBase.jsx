/**
 * Knowledge Base browser page
 */
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  FolderIcon,
  DocumentTextIcon,
  ArrowLeftIcon,
  HomeIcon,
} from '@heroicons/react/24/outline';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { knowledgeAPI } from '../services/api';
import Layout from '../components/Layout';

export default function KnowledgeBase() {
  const [currentPath, setCurrentPath] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const { data: items, isLoading } = useQuery({
    queryKey: ['knowledge-browse', currentPath],
    queryFn: () => knowledgeAPI.browse(currentPath),
  });

  const { data: fileContent } = useQuery({
    queryKey: ['knowledge-file', selectedFile],
    queryFn: () => knowledgeAPI.getFile(selectedFile),
    enabled: !!selectedFile,
  });

  const handleItemClick = (item) => {
    if (item.type === 'directory') {
      setCurrentPath(item.path);
      setSelectedFile(null);
    } else {
      setSelectedFile(item.path);
    }
  };

  const handleBack = () => {
    if (selectedFile) {
      setSelectedFile(null);
    } else {
      const parentPath = currentPath.split('/').slice(0, -1).join('/');
      setCurrentPath(parentPath);
    }
  };

  const handleHome = () => {
    setCurrentPath('');
    setSelectedFile(null);
  };

  const breadcrumbs = currentPath
    ? currentPath.split('/').filter((p) => p)
    : [];

  return (
    <Layout>
      <div className="space-y-4">
        {/* Header */}
        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900">Knowledge Base</h1>
          <p className="mt-1 text-sm text-gray-500">
            Browse 303 knowledge files across Pre-K-12 curriculum
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Browser Panel */}
          <div className="lg:col-span-1 bg-white shadow rounded-lg">
            {/* Breadcrumb */}
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleHome}
                  className="p-1 hover:bg-gray-100 rounded"
                  title="Home"
                >
                  <HomeIcon className="h-5 w-5 text-gray-500" />
                </button>
                {(currentPath || selectedFile) && (
                  <button
                    onClick={handleBack}
                    className="p-1 hover:bg-gray-100 rounded"
                    title="Back"
                  >
                    <ArrowLeftIcon className="h-5 w-5 text-gray-500" />
                  </button>
                )}
              </div>
              <div className="mt-2 flex items-center flex-wrap text-sm text-gray-600">
                <span>/</span>
                {breadcrumbs.map((crumb, index) => (
                  <div key={index} className="flex items-center">
                    <button
                      onClick={() =>
                        setCurrentPath(
                          breadcrumbs.slice(0, index + 1).join('/')
                        )
                      }
                      className="hover:text-primary-600 mx-1"
                    >
                      {crumb}
                    </button>
                    <span>/</span>
                  </div>
                ))}
                {selectedFile && (
                  <span className="text-primary-600 mx-1">
                    {selectedFile.split('/').pop()}
                  </span>
                )}
              </div>
            </div>

            {/* File/Directory List */}
            <div className="divide-y divide-gray-200 max-h-[600px] overflow-y-auto">
              {isLoading ? (
                <div className="p-8 text-center text-gray-500">Loading...</div>
              ) : items && items.length > 0 ? (
                items.map((item) => (
                  <button
                    key={item.path}
                    onClick={() => handleItemClick(item)}
                    className="w-full text-left p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center">
                      {item.type === 'directory' ? (
                        <FolderIcon className="h-5 w-5 text-yellow-500 mr-3" />
                      ) : (
                        <DocumentTextIcon className="h-5 w-5 text-blue-500 mr-3" />
                      )}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {item.name}
                        </p>
                        {item.category && (
                          <p className="text-xs text-gray-500">
                            {item.category}
                            {item.subject && ` • ${item.subject}`}
                            {item.state && ` • ${item.state}`}
                          </p>
                        )}
                      </div>
                      {item.size && (
                        <span className="text-xs text-gray-400 ml-2">
                          {(item.size / 1024).toFixed(1)} KB
                        </span>
                      )}
                    </div>
                  </button>
                ))
              ) : (
                <div className="p-8 text-center text-gray-500">
                  No files in this directory
                </div>
              )}
            </div>
          </div>

          {/* Content Panel */}
          <div className="lg:col-span-2 bg-white shadow rounded-lg">
            {fileContent ? (
              <div className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-2">
                  {fileContent.name}
                </h2>
                <div className="flex items-center space-x-4 text-sm text-gray-500 mb-6 pb-4 border-b">
                  <span>Category: {fileContent.metadata.category}</span>
                  {fileContent.metadata.subject && (
                    <span>Subject: {fileContent.metadata.subject}</span>
                  )}
                  {fileContent.metadata.state && (
                    <span>State: {fileContent.metadata.state}</span>
                  )}
                  <span>
                    Size: {(fileContent.metadata.size / 1024).toFixed(1)} KB
                  </span>
                </div>
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {fileContent.content}
                  </ReactMarkdown>
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center p-8">
                <div className="text-center text-gray-500">
                  <DocumentTextIcon className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                  <p className="text-lg font-medium">
                    Select a file to view its contents
                  </p>
                  <p className="text-sm mt-2">
                    Browse through directories or search for specific knowledge
                    files
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
