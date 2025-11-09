/**
 * TreeView Component
 *
 * Displays hierarchical content in an expandable tree structure.
 * Supports lazy-loading of children on-demand.
 */
import { useState } from 'react';
import { ChevronRightIcon, ChevronDownIcon, TrashIcon } from '@heroicons/react/24/outline';

export default function TreeView({
  contentTypeId,
  hierarchyConfig,
  onNodeClick,
  onDelete,
  selectedNodeId,
  fetchChildren,
  initialNodes = []
}) {
  const [expandedNodes, setExpandedNodes] = useState(new Set());
  const [nodeChildren, setNodeChildren] = useState({}); // Map of nodeId -> children array
  const [loadingNodes, setLoadingNodes] = useState(new Set());

  const displayField = hierarchyConfig?.display_field || 'name';
  const secondaryField = hierarchyConfig?.secondary_display_field;

  const toggleNode = async (node) => {
    const nodeId = node.identifier;
    const newExpandedNodes = new Set(expandedNodes);

    if (expandedNodes.has(nodeId)) {
      // Collapse
      newExpandedNodes.delete(nodeId);
      setExpandedNodes(newExpandedNodes);
    } else {
      // Expand - load children if not already loaded
      newExpandedNodes.add(nodeId);
      setExpandedNodes(newExpandedNodes);

      if (!nodeChildren[nodeId] && node.has_children) {
        // Load children
        setLoadingNodes(new Set([...loadingNodes, nodeId]));
        try {
          const children = await fetchChildren(nodeId);
          setNodeChildren({
            ...nodeChildren,
            [nodeId]: children
          });
        } catch (error) {
          console.error('Failed to load children:', error);
        } finally {
          const newLoadingNodes = new Set(loadingNodes);
          newLoadingNodes.delete(nodeId);
          setLoadingNodes(newLoadingNodes);
        }
      }
    }
  };

  const TreeNode = ({ node, level = 0 }) => {
    const nodeId = node.identifier;
    const isExpanded = expandedNodes.has(nodeId);
    const isLoading = loadingNodes.has(nodeId);
    const isSelected = selectedNodeId === node.id;
    const children = nodeChildren[nodeId] || [];

    return (
      <div className="tree-node">
        {/* Node Row */}
        <div
          className={`flex items-center py-2 px-2 hover:bg-gray-50 cursor-pointer ${
            isSelected ? 'bg-blue-50 border-l-4 border-blue-500' : ''
          }`}
          style={{ paddingLeft: `${level * 1.5 + 0.5}rem` }}
        >
          {/* Expand/Collapse Icon */}
          <div className="flex-shrink-0 w-6 h-6 mr-1">
            {node.has_children ? (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  toggleNode(node);
                }}
                className="w-full h-full flex items-center justify-center hover:bg-gray-200 rounded"
              >
                {isLoading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                ) : isExpanded ? (
                  <ChevronDownIcon className="h-4 w-4 text-gray-600" />
                ) : (
                  <ChevronRightIcon className="h-4 w-4 text-gray-600" />
                )}
              </button>
            ) : (
              <span className="block w-4 h-4 ml-1"></span>
            )}
          </div>

          {/* Node Content */}
          <div
            className="flex-1 flex items-center min-w-0 group"
            onClick={() => onNodeClick && onNodeClick(node)}
          >
            <div className="flex-1 min-w-0">
              {/* Primary Display Text */}
              <div className="text-sm text-gray-900 truncate">
                {node.display_text || 'Untitled'}
              </div>

              {/* Secondary Display Text (e.g., code) */}
              {secondaryField && node.data[secondaryField] && (
                <div className="text-xs text-gray-500 truncate">
                  {node.data[secondaryField]}
                </div>
              )}
            </div>

            {/* Children Count Badge */}
            {node.has_children && (
              <span className="ml-2 flex-shrink-0 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                {node.children_count}
              </span>
            )}

            {/* Delete Button - shows on hover */}
            {onDelete && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(node.id, node.display_text || 'Untitled');
                }}
                className="ml-2 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity inline-flex items-center p-1 border border-gray-300 shadow-sm text-xs font-medium rounded text-red-700 bg-white hover:bg-red-50"
                title="Delete"
              >
                <TrashIcon className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        </div>

        {/* Render Children if Expanded */}
        {isExpanded && children.length > 0 && (
          <div className="tree-children">
            {children.map((child) => (
              <TreeNode key={child.id} node={child} level={level + 1} />
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="tree-view border rounded-lg bg-white">
      {initialNodes.length === 0 ? (
        <div className="p-8 text-center text-gray-500">
          No items to display
        </div>
      ) : (
        <div className="divide-y divide-gray-100">
          {initialNodes.map((node) => (
            <TreeNode key={node.id} node={node} level={0} />
          ))}
        </div>
      )}
    </div>
  );
}
