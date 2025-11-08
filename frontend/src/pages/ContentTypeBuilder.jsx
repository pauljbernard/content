/**
 * Content Type Builder - Visual editor for creating/editing content type definitions
 */
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  PlusIcon,
  TrashIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  BookOpenIcon,
  DocumentTextIcon,
  HashtagIcon,
  CalendarIcon,
  CheckCircleIcon,
  ListBulletIcon,
  LinkIcon,
  PhotoIcon,
  CodeBracketIcon,
  AtSymbolIcon,
  GlobeAltIcon,
  MapPinIcon,
} from '@heroicons/react/24/outline';
import { contentTypesAPI, agentsAPI } from '../services/api';
import Layout from '../components/Layout';

// Attribute type definitions with icons and configs
const ATTRIBUTE_TYPES = {
  text: {
    label: 'Short Text',
    icon: DocumentTextIcon,
    defaultConfig: { maxLength: 255 },
    configFields: ['maxLength', 'minLength', 'pattern'],
  },
  long_text: {
    label: 'Long Text',
    icon: DocumentTextIcon,
    defaultConfig: { maxLength: 10000 },
    configFields: ['maxLength', 'minLength'],
  },
  rich_text: {
    label: 'Rich Text',
    icon: DocumentTextIcon,
    defaultConfig: {},
    configFields: [],
  },
  number: {
    label: 'Number',
    icon: HashtagIcon,
    defaultConfig: { step: 1 },
    configFields: ['min', 'max', 'step'],
  },
  boolean: {
    label: 'Boolean',
    icon: CheckCircleIcon,
    defaultConfig: { defaultValue: false },
    configFields: ['defaultValue'],
  },
  date: {
    label: 'Date',
    icon: CalendarIcon,
    defaultConfig: {},
    configFields: [],
  },
  choice: {
    label: 'Choice',
    icon: ListBulletIcon,
    defaultConfig: { choices: [], multiple: false },
    configFields: ['choices', 'multiple'],
  },
  reference: {
    label: 'Reference',
    icon: LinkIcon,
    defaultConfig: { targetContentType: '', multiple: false },
    configFields: ['targetContentType', 'multiple'],
  },
  media: {
    label: 'Media',
    icon: PhotoIcon,
    defaultConfig: { allowedTypes: ['image/*'] },
    configFields: ['allowedTypes', 'maxSize'],
  },
  json: {
    label: 'JSON',
    icon: CodeBracketIcon,
    defaultConfig: {},
    configFields: [],
  },
  url: {
    label: 'URL',
    icon: GlobeAltIcon,
    defaultConfig: {},
    configFields: [],
  },
  email: {
    label: 'Email',
    icon: AtSymbolIcon,
    defaultConfig: {},
    configFields: [],
  },
  location: {
    label: 'Location',
    icon: MapPinIcon,
    defaultConfig: {},
    configFields: [],
  },
};

export default function ContentTypeBuilder() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEditMode = Boolean(id);

  // Form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [icon, setIcon] = useState('BookOpenIcon');
  const [attributes, setAttributes] = useState([]);
  const [showAttributeForm, setShowAttributeForm] = useState(false);
  const [editingAttributeIndex, setEditingAttributeIndex] = useState(null);

  // Attribute form state
  const [attrName, setAttrName] = useState('');
  const [attrLabel, setAttrLabel] = useState('');
  const [attrType, setAttrType] = useState('text');
  const [attrRequired, setAttrRequired] = useState(false);
  const [attrHelpText, setAttrHelpText] = useState('');
  const [attrConfig, setAttrConfig] = useState({});
  const [attrAiEnabled, setAttrAiEnabled] = useState(false);
  const [attrAiAgents, setAttrAiAgents] = useState([]);
  const [attrAiRagContentTypes, setAttrAiRagContentTypes] = useState([]);
  const [attrAiOutputSchema, setAttrAiOutputSchema] = useState('');

  // Fetch content type if editing
  const { data: contentType, isLoading } = useQuery({
    queryKey: ['content-type', id],
    queryFn: () => contentTypesAPI.get(id),
    enabled: isEditMode,
  });

  // Fetch available agents for AI configuration
  const { data: availableAgents } = useQuery({
    queryKey: ['agents'],
    queryFn: agentsAPI.list,
  });

  // Fetch available content types for reference fields
  const { data: availableContentTypes } = useQuery({
    queryKey: ['content-types-list'],
    queryFn: contentTypesAPI.list,
  });

  // Load content type data into form
  useEffect(() => {
    if (contentType) {
      setName(contentType.name);
      setDescription(contentType.description || '');
      setIcon(contentType.icon || 'BookOpenIcon');
      setAttributes(contentType.attributes || []);
    }
  }, [contentType]);

  // Create/Update mutations
  const createMutation = useMutation({
    mutationFn: contentTypesAPI.create,
    onSuccess: () => {
      queryClient.invalidateQueries(['content-types']);
      toast.success('Content type created successfully');
      navigate('/content-types');
    },
    onError: (error) => {
      toast.error(`Failed to create: ${error.response?.data?.detail || error.message}`);
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data) => contentTypesAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['content-types']);
      queryClient.invalidateQueries(['content-type', id]);
      toast.success('Content type updated successfully');
      navigate('/content-types');
    },
    onError: (error) => {
      toast.error(`Failed to update: ${error.response?.data?.detail || error.message}`);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    const data = {
      name,
      description,
      icon,
      attributes,
    };

    if (isEditMode) {
      updateMutation.mutate(data);
    } else {
      createMutation.mutate(data);
    }
  };

  const handleAddAttribute = () => {
    setShowAttributeForm(true);
    setEditingAttributeIndex(null);
    resetAttributeForm();
  };

  const handleEditAttribute = (index) => {
    const attr = attributes[index];
    setAttrName(attr.name);
    setAttrLabel(attr.label);
    setAttrType(attr.type);
    setAttrRequired(attr.required);
    setAttrHelpText(attr.help_text || '');
    setAttrConfig(attr.config || {});
    setAttrAiEnabled(attr.ai_assist_enabled || false);
    setAttrAiAgents(attr.ai_agents || []);
    setAttrAiRagContentTypes(attr.ai_rag_content_types || []);
    setAttrAiOutputSchema(attr.ai_output_schema || '');
    setEditingAttributeIndex(index);
    setShowAttributeForm(true);
  };

  const handleSaveAttribute = () => {
    const attribute = {
      name: attrName,
      label: attrLabel,
      type: attrType,
      required: attrRequired,
      help_text: attrHelpText,
      config: attrConfig,
      order_index: editingAttributeIndex !== null ? editingAttributeIndex : attributes.length,
      ai_assist_enabled: attrAiEnabled,
      ai_agents: attrAiAgents,
      ai_rag_content_types: attrAiRagContentTypes,
      ai_output_schema: attrAiOutputSchema || null,
    };

    if (editingAttributeIndex !== null) {
      // Update existing
      const newAttributes = [...attributes];
      newAttributes[editingAttributeIndex] = attribute;
      setAttributes(newAttributes);
    } else {
      // Add new
      setAttributes([...attributes, attribute]);
    }

    setShowAttributeForm(false);
    resetAttributeForm();
  };

  const handleDeleteAttribute = (index) => {
    setAttributes(attributes.filter((_, i) => i !== index));
  };

  const handleMoveAttribute = (index, direction) => {
    const newAttributes = [...attributes];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    [newAttributes[index], newAttributes[newIndex]] = [newAttributes[newIndex], newAttributes[index]];
    setAttributes(newAttributes);
  };

  const resetAttributeForm = () => {
    setAttrName('');
    setAttrLabel('');
    setAttrType('text');
    setAttrRequired(false);
    setAttrHelpText('');
    setAttrConfig(ATTRIBUTE_TYPES.text.defaultConfig);
    setAttrAiEnabled(false);
    setAttrAiAgents([]);
    setAttrAiRagContentTypes([]);
    setAttrAiOutputSchema('');
  };

  if (isEditMode && isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {isEditMode ? 'Edit Content Type' : 'Create Content Type'}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Define the structure of your content by adding attributes
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Basic Information</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name *</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  placeholder="Lesson Plan"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  placeholder="A structured lesson plan for K-12 education"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Icon</label>
                <input
                  type="text"
                  value={icon}
                  onChange={(e) => setIcon(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  placeholder="BookOpenIcon"
                />
                <p className="mt-1 text-xs text-gray-500">Heroicons name (e.g., BookOpenIcon, DocumentTextIcon)</p>
              </div>
            </div>
          </div>

          {/* Attributes */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-medium text-gray-900">Attributes ({attributes.length})</h2>
              <button
                type="button"
                onClick={handleAddAttribute}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                <PlusIcon className="h-4 w-4 mr-1" />
                Add Attribute
              </button>
            </div>

            {/* Attribute List */}
            {attributes.length > 0 ? (
              <div className="space-y-2">
                {attributes.map((attr, index) => {
                  const AttrIcon = ATTRIBUTE_TYPES[attr.type]?.icon || DocumentTextIcon;
                  return (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center flex-1">
                        <AttrIcon className="h-5 w-5 text-gray-400 mr-3" />
                        <div className="flex-1">
                          <div className="flex items-center space-x-2">
                            <span className="font-medium text-gray-900">{attr.label}</span>
                            <span className="text-xs text-gray-500">({attr.name})</span>
                            {attr.required && (
                              <span className="text-xs bg-red-100 text-red-800 px-2 py-0.5 rounded">Required</span>
                            )}
                          </div>
                          <div className="text-sm text-gray-500">
                            {ATTRIBUTE_TYPES[attr.type]?.label || attr.type}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-1">
                        <button
                          type="button"
                          onClick={() => handleMoveAttribute(index, 'up')}
                          disabled={index === 0}
                          className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30"
                        >
                          <ArrowUpIcon className="h-4 w-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => handleMoveAttribute(index, 'down')}
                          disabled={index === attributes.length - 1}
                          className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30"
                        >
                          <ArrowDownIcon className="h-4 w-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => handleEditAttribute(index)}
                          className="p-1 text-blue-600 hover:text-blue-800"
                        >
                          Edit
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDeleteAttribute(index)}
                          className="p-1 text-red-600 hover:text-red-800"
                        >
                          <TrashIcon className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-2">No attributes yet. Add your first attribute to get started.</p>
              </div>
            )}
          </div>

          {/* Attribute Form Modal */}
          {showAttributeForm && (
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  {editingAttributeIndex !== null ? 'Edit Attribute' : 'Add Attribute'}
                </h3>

                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Name (snake_case) *</label>
                      <input
                        type="text"
                        value={attrName}
                        onChange={(e) => setAttrName(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, '_'))}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        placeholder="lesson_title"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Label *</label>
                      <input
                        type="text"
                        value={attrLabel}
                        onChange={(e) => setAttrLabel(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        placeholder="Lesson Title"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">Type *</label>
                    <select
                      value={attrType}
                      onChange={(e) => {
                        setAttrType(e.target.value);
                        setAttrConfig(ATTRIBUTE_TYPES[e.target.value].defaultConfig);
                      }}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    >
                      {Object.entries(ATTRIBUTE_TYPES).map(([key, type]) => (
                        <option key={key} value={key}>
                          {type.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={attrRequired}
                        onChange={(e) => setAttrRequired(e.target.checked)}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">Required field</span>
                    </label>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">Help Text</label>
                    <input
                      type="text"
                      value={attrHelpText}
                      onChange={(e) => setAttrHelpText(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      placeholder="Brief description or hint for users"
                    />
                  </div>

                  {/* Type-specific config fields */}
                  {attrType === 'choice' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Choices (comma-separated)</label>
                      <input
                        type="text"
                        value={(attrConfig.choices || []).join(', ')}
                        onChange={(e) =>
                          setAttrConfig({
                            ...attrConfig,
                            choices: e.target.value.split(',').map((s) => s.trim()).filter(Boolean),
                          })
                        }
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        placeholder="Option 1, Option 2, Option 3"
                      />
                    </div>
                  )}

                  {attrType === 'reference' && (
                    <div className="space-y-4 border-t border-gray-200 pt-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Target Content Type *
                        </label>
                        <select
                          value={attrConfig.targetContentType || ''}
                          onChange={(e) =>
                            setAttrConfig({
                              ...attrConfig,
                              targetContentType: e.target.value,
                            })
                          }
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                        >
                          <option value="">-- Select Content Type --</option>
                          {id && (
                            <option value={id}>
                              ⟲ {contentType?.name || 'This Type'} (Self-Reference)
                            </option>
                          )}
                          {availableContentTypes?.map((ct) => (
                            <option key={ct.id} value={ct.id}>
                              {ct.name}
                            </option>
                          ))}
                        </select>
                        <p className="mt-1 text-xs text-gray-500">
                          Select which content type this field will reference. Choose "This Type" for hierarchical structures.
                        </p>
                      </div>

                      <div>
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={attrConfig.multiple || false}
                            onChange={(e) =>
                              setAttrConfig({
                                ...attrConfig,
                                multiple: e.target.checked,
                              })
                            }
                            className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">Allow multiple references</span>
                        </label>
                        <p className="mt-1 ml-6 text-xs text-gray-500">
                          Enable for parent-children relationships or multiple related items
                        </p>
                      </div>
                    </div>
                  )}

                  {/* AI Assist Configuration */}
                  {['text', 'long_text', 'rich_text', 'json'].includes(attrType) && (
                    <div className="border-t border-gray-200 pt-4">
                      <div className="flex items-center mb-3">
                        <input
                          type="checkbox"
                          id="ai-assist-enabled"
                          checked={attrAiEnabled}
                          onChange={(e) => {
                            setAttrAiEnabled(e.target.checked);
                            if (!e.target.checked) {
                              setAttrAiAgents([]);
                              setAttrAiOutputSchema('');
                            }
                          }}
                          className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                        />
                        <label htmlFor="ai-assist-enabled" className="ml-2 text-sm font-medium text-gray-700">
                          Enable AI Assist for this field
                        </label>
                      </div>

                      {attrAiEnabled && (
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Select Available AI Agents
                          </label>
                          <p className="text-xs text-gray-500 mb-3">
                            Choose which AI agents can assist with generating content for this field
                          </p>
                          <div className="space-y-2 max-h-48 overflow-y-auto border border-gray-200 rounded-md p-3">
                            {availableAgents && availableAgents.length > 0 ? (
                              availableAgents.map((agent) => (
                                <label key={agent.id} className="flex items-start cursor-pointer hover:bg-gray-50 p-2 rounded">
                                  <input
                                    type="checkbox"
                                    checked={attrAiAgents.includes(agent.id)}
                                    onChange={(e) => {
                                      if (e.target.checked) {
                                        setAttrAiAgents([...attrAiAgents, agent.id]);
                                      } else {
                                        setAttrAiAgents(attrAiAgents.filter(id => id !== agent.id));
                                      }
                                    }}
                                    className="mt-0.5 rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                                  />
                                  <div className="ml-3">
                                    <div className="text-sm font-medium text-gray-900">{agent.name}</div>
                                    <div className="text-xs text-gray-500">{agent.description}</div>
                                  </div>
                                </label>
                              ))
                            ) : (
                              <p className="text-sm text-gray-500 text-center py-4">
                                No AI agents available
                              </p>
                            )}
                          </div>
                          {attrAiAgents.length > 0 && (
                            <p className="mt-2 text-xs text-green-600">
                              ✓ {attrAiAgents.length} agent{attrAiAgents.length !== 1 ? 's' : ''} selected
                            </p>
                          )}

                          {/* RAG Content Types Selection */}
                          <div className="mt-6 border-t border-gray-200 pt-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Select Content Types for RAG Context
                            </label>
                            <p className="text-xs text-gray-500 mb-3">
                              Choose which content types to search for relevant context when generating this field. The AI will retrieve similar content from these types to inform its generation.
                            </p>
                            <div className="space-y-2 max-h-48 overflow-y-auto border border-gray-200 rounded-md p-3">
                              {availableContentTypes && availableContentTypes.length > 0 ? (
                                availableContentTypes.map((ct) => (
                                  <label key={ct.id} className="flex items-start cursor-pointer hover:bg-gray-50 p-2 rounded">
                                    <input
                                      type="checkbox"
                                      checked={attrAiRagContentTypes.includes(ct.id)}
                                      onChange={(e) => {
                                        if (e.target.checked) {
                                          setAttrAiRagContentTypes([...attrAiRagContentTypes, ct.id]);
                                        } else {
                                          setAttrAiRagContentTypes(attrAiRagContentTypes.filter(id => id !== ct.id));
                                        }
                                      }}
                                      className="mt-0.5 rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                                    />
                                    <div className="ml-3">
                                      <div className="text-sm font-medium text-gray-900">{ct.name}</div>
                                      {ct.description && (
                                        <div className="text-xs text-gray-500">{ct.description}</div>
                                      )}
                                    </div>
                                  </label>
                                ))
                              ) : (
                                <p className="text-sm text-gray-500 text-center py-4">
                                  No content types available for selection
                                </p>
                              )}
                            </div>
                            {attrAiRagContentTypes.length > 0 && (
                              <p className="mt-2 text-xs text-green-600">
                                ✓ {attrAiRagContentTypes.length} content type{attrAiRagContentTypes.length !== 1 ? 's' : ''} selected for RAG context
                              </p>
                            )}
                            {attrAiRagContentTypes.length === 0 && (
                              <p className="mt-2 text-xs text-amber-600">
                                ⚠ No content types selected - AI will search all content types for context
                              </p>
                            )}
                          </div>

                          {/* JSON Output Schema - only for JSON fields */}
                          {attrType === 'json' && (
                            <div className="mt-4 border-t border-gray-200 pt-4">
                              <label className="block text-sm font-medium text-gray-700 mb-2">
                                JSON Output Schema/Sample
                              </label>
                              <p className="text-xs text-gray-500 mb-2">
                                Provide a sample JSON structure that the AI should produce. This guides the AI to generate properly formatted structured data.
                              </p>
                              <textarea
                                value={attrAiOutputSchema}
                                onChange={(e) => setAttrAiOutputSchema(e.target.value)}
                                rows={8}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500 font-mono text-xs"
                                placeholder={`Example:\n[\n  {\n    "objective": "Students will be able to...",\n    "bloom_level": "analyze",\n    "standard": "TEKS.5.Math.3A",\n    "measurable": true\n  }\n]`}
                              />
                              <p className="mt-1 text-xs text-gray-500">
                                The AI will use this schema to generate structured JSON matching this format
                              </p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <div className="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAttributeForm(false);
                      resetAttributeForm();
                    }}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={handleSaveAttribute}
                    disabled={!attrName || !attrLabel}
                    className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                  >
                    {editingAttributeIndex !== null ? 'Update' : 'Add'} Attribute
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Form Actions */}
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate('/content-types')}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!name || attributes.length === 0 || createMutation.isLoading || updateMutation.isLoading}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
            >
              {isEditMode ? 'Update' : 'Create'} Content Type
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
