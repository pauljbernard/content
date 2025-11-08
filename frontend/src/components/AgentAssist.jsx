/**
 * AgentAssist Component
 *
 * Provides AI-powered assistance for content fields using the RAG-based agent system.
 * This component integrates with Claude Code to generate field values based on:
 * - Retrieved context from content instances
 * - Knowledge base files
 * - User inputs and field dependencies
 */
import { useState } from 'react';
import { SparklesIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';

// All 23 built-in agents available in the system
const BUILTIN_AGENTS = [
  'curriculum-architect',
  'lesson-planner',
  'assessment-designer',
  'content-developer',
  'pedagogical-reviewer',
  'quality-assurance',
  'standards-compliance',
  'accessibility-reviewer',
  'bias-detector',
  'scorm-packager',
  'pdf-generator',
  'web-publisher',
  'learning-analytics',
  'grading-assistant',
  'diagnostic-assessor',
  'adaptive-personalizer',
  'tutoring-assistant',
  'project-planner',
  'review-coordinator',
  'content-librarian',
  'rights-manager',
  'performance-optimizer',
  'platform-trainer',
];

export default function AgentAssist({
  instanceId,
  fieldName,
  fieldLabel,
  availableAgents = [], // Array of agent names from ai_agents attribute config
  currentValue,
  onAccept,
  onReject,
  disabled = false,
}) {
  // Filter to only show agents that are:
  // 1. In the built-in agents list (valid)
  // 2. In the availableAgents array for this field (relevant)
  const agents = availableAgents.length > 0
    ? availableAgents.filter(agent => BUILTIN_AGENTS.includes(agent))
    : BUILTIN_AGENTS.slice(0, 3); // Default to first 3 if none specified

  const [showPanel, setShowPanel] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(agents[0]);
  const [generatedValue, setGeneratedValue] = useState(null);
  const [contextMetadata, setContextMetadata] = useState(null);
  const [editableValue, setEditableValue] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleOpenPanel = () => {
    if (disabled) return;
    setEditableValue(formatValue(currentValue));
    setShowPanel(true);
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    setEditableValue(''); // Clear existing content
    setGeneratedValue(null);

    try {
      await contentTypesAPI.generateFieldStream(
        instanceId,
        fieldName,
        selectedAgent,
        {
          onStart: (data) => {
            console.log('Generation started:', data);
          },
          onInfo: (message) => {
            // Display retry info messages in the textarea
            console.log('[INFO]', message);
            setEditableValue((prev) => prev + `\n\n[INFO: ${message}]\n\n`);
          },
          onContent: (text) => {
            // Append new text to the textarea in real-time
            setEditableValue((prev) => prev + text);
          },
          onDone: (data) => {
            console.log('Generation complete:', data);
            setGeneratedValue(data.generated_value);
            setContextMetadata(data.context_metadata);
            setIsGenerating(false);
          },
          onError: (error) => {
            console.error('Generation error:', error);
            alert(`Failed to generate content: ${error}`);
            setIsGenerating(false);
          },
        }
      );
    } catch (error) {
      console.error('Stream error:', error);
      alert(`Failed to start generation: ${error.message}`);
      setIsGenerating(false);
    }
  };

  const handleAccept = () => {
    // Try to parse the editable value back to original type if it was JSON
    let finalValue = editableValue;
    try {
      // If current value was an object/array, parse the edited text back to JSON
      if (typeof currentValue === 'object' && currentValue !== null) {
        finalValue = JSON.parse(editableValue);
      }
    } catch (e) {
      // If parse fails, use as string
    }
    onAccept(finalValue);
    setShowPanel(false);
    setGeneratedValue(null);
    setEditableValue('');
    setContextMetadata(null);
  };

  const handleClose = () => {
    if (onReject) {
      onReject();
    }
    setShowPanel(false);
    setGeneratedValue(null);
    setContextMetadata(null);
  };

  // Format generated value for display
  const formatValue = (value) => {
    if (typeof value === 'object') {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  return (
    <div className="agent-assist">
      {/* Generate Button */}
      {!showPanel && (
        <button
          type="button"
          onClick={handleOpenPanel}
          disabled={disabled}
          className={`
            inline-flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md
            ${
              disabled
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-purple-50 text-purple-700 hover:bg-purple-100 focus:outline-none focus:ring-2 focus:ring-purple-500'
            }
          `}
          title={disabled ? 'Save the instance first to enable AI assistance' : `Generate ${fieldLabel} using AI`}
        >
          <SparklesIcon className="h-4 w-4" />
          Generate with AI
        </button>
      )}

      {/* AI Assist Panel - Right Side Slide-out */}
      {showPanel && (
        <div className="fixed inset-0 z-50 overflow-hidden">
          {/* Background overlay */}
          <div
            className="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
            onClick={handleClose}
          ></div>

          {/* Right-side panel */}
          <div className="fixed inset-y-0 right-0 max-w-2xl w-full bg-white shadow-xl flex flex-col">
            {/* Header */}
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <SparklesIcon className="h-6 w-6 text-purple-600 mr-2" />
                  <h2 className="text-xl font-semibold text-gray-900">
                    {generatedValue ? 'AI-Generated Content' : 'AI Assist'}
                  </h2>
                </div>
                <button
                  onClick={handleClose}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <XMarkIcon className="h-6 w-6" />
                </button>
              </div>
              <p className="mt-1 text-sm text-gray-500">
                {generatedValue ? 'Review and accept or reject the generated content' : `Generate content for: ${fieldLabel}`}
              </p>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto px-6 py-4">
              {/* Agent Selection */}
              {!generatedValue && (
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Select AI Agent</h3>
                  <div className="space-y-2">
                    {agents.map((agentName) => (
                      <div key={agentName} className="flex items-center">
                        <input
                          type="radio"
                          id={`agent-${agentName}`}
                          name="agent-selection"
                          value={agentName}
                          checked={selectedAgent === agentName}
                          onChange={(e) => setSelectedAgent(e.target.value)}
                          className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300"
                        />
                        <label
                          htmlFor={`agent-${agentName}`}
                          className="ml-3 block text-sm font-medium text-gray-700 capitalize"
                        >
                          {agentName.replace(/-/g, ' ')}
                        </label>
                      </div>
                    ))}
                  </div>
                  <p className="mt-2 text-xs text-gray-500">
                    Different agents have specialized behaviors and knowledge for specific tasks.
                  </p>
                </div>
              )}

              {/* Editable Content Area */}
              <div className="mb-6">
                <h3 className="text-sm font-medium text-gray-700 mb-2">
                  {generatedValue ? 'Generated Content (editable)' : 'Current Field Value (editable)'}
                </h3>
                <textarea
                  value={editableValue || ''}
                  onChange={(e) => setEditableValue(e.target.value)}
                  rows={12}
                  className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-900 font-mono focus:ring-purple-500 focus:border-purple-500"
                  placeholder="No value set yet"
                />
              </div>

              {/* Info Box */}
              {!generatedValue && (
                <div className="mb-6 bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <h4 className="text-sm font-semibold text-blue-900 mb-2">
                    What will happen:
                  </h4>
                  <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                    <li>Retrieve relevant knowledge from the knowledge base</li>
                    <li>Analyze current instance data for context</li>
                    <li>Generate content using {selectedAgent || 'Claude Sonnet 4.5'}</li>
                    <li>Content will appear in the editor above for review</li>
                  </ul>
                </div>
              )}

              {/* Context Metadata */}
              {contextMetadata && (
                <div className="mb-6 bg-green-50 rounded-lg p-3 border border-green-200">
                  <h4 className="text-xs font-semibold text-green-900 uppercase tracking-wide mb-2">
                    ✓ Generation Complete - Context Used
                  </h4>
                  <div className="text-xs text-green-700 space-y-1">
                    <div>
                      <strong>Content Instances:</strong> {contextMetadata.total_instances}
                    </div>
                    <div>
                      <strong>Knowledge Files:</strong> {contextMetadata.total_knowledge_files}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Footer - Action Buttons */}
            <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
              <div className="flex gap-3 justify-end">
                {!generatedValue ? (
                  /* Before Generation - Show Cancel and Generate buttons */
                  <>
                    <button
                      type="button"
                      onClick={handleClose}
                      className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      onClick={handleGenerate}
                      disabled={isGenerating}
                      className="inline-flex items-center gap-2 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <SparklesIcon className={`h-5 w-5 ${isGenerating ? 'animate-pulse' : ''}`} />
                      {isGenerating ? 'Generating...' : 'Generate with AI'}
                    </button>
                  </>
                ) : (
                  /* After Generation - Show Reject and Accept buttons */
                  <>
                    <button
                      type="button"
                      onClick={handleClose}
                      className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                    >
                      <XMarkIcon className="h-5 w-5" />
                      Reject
                    </button>
                    <button
                      type="button"
                      onClick={handleAccept}
                      className="inline-flex items-center gap-2 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                    >
                      <CheckIcon className="h-5 w-5" />
                      Accept & Use
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
