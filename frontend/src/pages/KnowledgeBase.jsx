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
import rehypeHighlight from 'rehype-highlight';
import rehypeRaw from 'rehype-raw';
import { knowledgeAPI } from '../services/api';
import Layout from '../components/Layout';
import 'highlight.js/styles/github.css';

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
                <div className="markdown-body prose prose-lg max-w-none">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeHighlight, rehypeRaw]}
                    components={{
                      h1: ({node, ...props}) => <h1 className="text-3xl font-bold mt-8 mb-4 pb-2 border-b border-gray-200" {...props} />,
                      h2: ({node, ...props}) => <h2 className="text-2xl font-bold mt-6 mb-3 pb-2 border-b border-gray-200" {...props} />,
                      h3: ({node, ...props}) => <h3 className="text-xl font-bold mt-5 mb-2" {...props} />,
                      h4: ({node, ...props}) => <h4 className="text-lg font-semibold mt-4 mb-2" {...props} />,
                      h5: ({node, ...props}) => <h5 className="text-base font-semibold mt-3 mb-2" {...props} />,
                      h6: ({node, ...props}) => <h6 className="text-sm font-semibold mt-3 mb-2 text-gray-600" {...props} />,
                      p: ({node, ...props}) => <p className="mb-4 leading-7 text-gray-800" {...props} />,
                      ul: ({node, ...props}) => <ul className="list-disc list-inside mb-4 space-y-2 ml-4" {...props} />,
                      ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-4 space-y-2 ml-4" {...props} />,
                      li: ({node, ...props}) => <li className="leading-7 text-gray-800" {...props} />,
                      blockquote: ({node, ...props}) => (
                        <blockquote className="border-l-4 border-gray-300 pl-4 my-4 italic text-gray-700 bg-gray-50 py-2" {...props} />
                      ),
                      code: ({node, inline, className, children, ...props}) => {
                        if (inline) {
                          return (
                            <code className="bg-gray-100 text-red-600 px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
                              {children}
                            </code>
                          );
                        }
                        return (
                          <code className={`${className} block bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm`} {...props}>
                            {children}
                          </code>
                        );
                      },
                      pre: ({node, ...props}) => (
                        <pre className="bg-gray-900 rounded-lg mb-4 overflow-x-auto" {...props} />
                      ),
                      a: ({node, ...props}) => (
                        <a className="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer" {...props} />
                      ),
                      table: ({node, ...props}) => (
                        <div className="overflow-x-auto mb-4">
                          <table className="min-w-full divide-y divide-gray-200 border border-gray-200" {...props} />
                        </div>
                      ),
                      thead: ({node, ...props}) => <thead className="bg-gray-50" {...props} />,
                      tbody: ({node, ...props}) => <tbody className="bg-white divide-y divide-gray-200" {...props} />,
                      tr: ({node, ...props}) => <tr className="hover:bg-gray-50" {...props} />,
                      th: ({node, ...props}) => (
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" {...props} />
                      ),
                      td: ({node, ...props}) => (
                        <td className="px-4 py-3 text-sm text-gray-800" {...props} />
                      ),
                      hr: ({node, ...props}) => <hr className="my-6 border-t border-gray-300" {...props} />,
                      img: ({node, ...props}) => (
                        <img className="max-w-full h-auto rounded-lg shadow-md my-4" {...props} />
                      ),
                      strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                      em: ({node, ...props}) => <em className="italic" {...props} />,
                    }}
                  >
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
