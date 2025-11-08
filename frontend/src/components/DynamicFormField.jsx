/**
 * Dynamic Form Field Component
 * Renders appropriate input based on attribute type
 */
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { SparklesIcon } from '@heroicons/react/24/outline';
import { contentTypesAPI } from '../services/api';
import AgentAssist from './AgentAssist';

export default function DynamicFormField({
  attribute,
  value,
  onChange,
  error,
  contentTypeId,
  instanceId,
  onAIAssist,
}) {
  const { name, label, type, required, help_text, config = {}, ai_assist_enabled = false, ai_agents = [], ai_rag_content_types = [] } = attribute;

  // Check if AI assist is enabled for this specific field
  // If ai_agents is empty or not specified, will use default Claude Code configuration
  const showAIAssist = ai_assist_enabled && instanceId;

  const renderField = () => {
    switch (type) {
      case 'text':
        return (
          <input
            type="text"
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            maxLength={config.maxLength}
            minLength={config.minLength}
            pattern={config.pattern}
            className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
          />
        );

      case 'long_text':
        return (
          <textarea
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            rows={config.rows || 4}
            maxLength={config.maxLength}
            className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
          />
        );

      case 'rich_text':
        return (
          <div>
            <textarea
              value={value || ''}
              onChange={(e) => onChange(e.target.value)}
              rows={8}
              className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 font-mono text-sm ${
                error ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Enter HTML or Markdown content..."
            />
            <p className="mt-1 text-xs text-gray-500">
              Rich text editor (supports HTML/Markdown)
            </p>
          </div>
        );

      case 'number':
        return (
          <input
            type="number"
            value={value !== undefined && value !== null ? value : ''}
            onChange={(e) => {
              const val = e.target.value === '' ? null : parseFloat(e.target.value);
              onChange(val);
            }}
            min={config.min}
            max={config.max}
            step={config.step || 1}
            className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
          />
        );

      case 'boolean':
        return (
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={!!value}
              onChange={(e) => onChange(e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label className="ml-2 text-sm text-gray-700">
              {config.checkboxLabel || 'Enable'}
            </label>
          </div>
        );

      case 'date':
        return (
          <input
            type={config.includeTime ? 'datetime-local' : 'date'}
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            min={config.min}
            max={config.max}
            className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
          />
        );

      case 'choice':
        if (config.multiple) {
          return (
            <div className="space-y-2">
              {(config.choices || []).map((choice) => (
                <div key={choice} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={Array.isArray(value) && value.includes(choice)}
                    onChange={(e) => {
                      const currentValues = Array.isArray(value) ? value : [];
                      if (e.target.checked) {
                        onChange([...currentValues, choice]);
                      } else {
                        onChange(currentValues.filter((v) => v !== choice));
                      }
                    }}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label className="ml-2 text-sm text-gray-700">{choice}</label>
                </div>
              ))}
            </div>
          );
        } else {
          return (
            <select
              value={value || ''}
              onChange={(e) => onChange(e.target.value)}
              className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
                error ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">-- Select --</option>
              {(config.choices || []).map((choice) => (
                <option key={choice} value={choice}>
                  {choice}
                </option>
              ))}
            </select>
          );
        }

      case 'reference':
        return <ReferenceField value={value} onChange={onChange} config={config} error={error} />;

      case 'media':
        return (
          <div>
            <input
              type="file"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) {
                  // For now, just store filename - in production, upload to server
                  onChange({
                    filename: file.name,
                    size: file.size,
                    type: file.type,
                  });
                }
              }}
              accept={config.allowedTypes?.join(',')}
              className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
                error ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {value && (
              <div className="mt-2 text-sm text-gray-600">
                Current: {value.filename || value}
              </div>
            )}
            {config.allowedTypes && (
              <p className="mt-1 text-xs text-gray-500">
                Allowed types: {config.allowedTypes.join(', ')}
              </p>
            )}
          </div>
        );

      case 'json':
        return (
          <div>
            <textarea
              value={
                typeof value === 'string'
                  ? value
                  : value
                  ? JSON.stringify(value, null, 2)
                  : ''
              }
              onChange={(e) => {
                try {
                  const parsed = JSON.parse(e.target.value);
                  onChange(parsed);
                } catch (err) {
                  // Allow invalid JSON while typing
                  onChange(e.target.value);
                }
              }}
              rows={8}
              className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 font-mono text-sm ${
                error ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder='{"key": "value"}'
            />
            <p className="mt-1 text-xs text-gray-500">
              Enter valid JSON
            </p>
          </div>
        );

      case 'url':
        return (
          <input
            type="url"
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            placeholder="https://example.com"
            className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
          />
        );

      case 'email':
        return (
          <input
            type="email"
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            placeholder="email@example.com"
            className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
          />
        );

      case 'location':
        return (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Latitude
              </label>
              <input
                type="number"
                value={value?.lat || ''}
                onChange={(e) =>
                  onChange({
                    ...value,
                    lat: parseFloat(e.target.value) || 0,
                  })
                }
                step="0.000001"
                min="-90"
                max="90"
                placeholder="40.7128"
                className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
                  error ? 'border-red-500' : 'border-gray-300'
                }`}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Longitude
              </label>
              <input
                type="number"
                value={value?.lng || ''}
                onChange={(e) =>
                  onChange({
                    ...value,
                    lng: parseFloat(e.target.value) || 0,
                  })
                }
                step="0.000001"
                min="-180"
                max="180"
                placeholder="-74.0060"
                className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
                  error ? 'border-red-500' : 'border-gray-300'
                }`}
              />
            </div>
          </div>
        );

      default:
        return (
          <div className="text-sm text-gray-500">
            Unsupported field type: {type}
          </div>
        );
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <label className="block text-sm font-medium text-gray-700">
          {label || name}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
        {showAIAssist && (
          <AgentAssist
            instanceId={instanceId}
            fieldName={name}
            fieldLabel={label || name}
            availableAgents={ai_agents || []}
            ragContentTypes={ai_rag_content_types || []}
            currentValue={value}
            onAccept={(generatedValue) => onChange(generatedValue)}
            onReject={() => {}}
            disabled={!instanceId}
          />
        )}
      </div>
      {renderField()}
      {help_text && (
        <p className="mt-1 text-xs text-gray-500">{help_text}</p>
      )}
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  );
}

/**
 * Reference Field Component
 * Allows selecting references to other content instances
 */
function ReferenceField({ value, onChange, config, error }) {
  const targetContentTypeId = config.targetContentType;

  // Fetch available instances to reference
  const { data: instances, isLoading } = useQuery({
    queryKey: ['content-instances', targetContentTypeId],
    queryFn: () => contentTypesAPI.listInstances(targetContentTypeId),
    enabled: !!targetContentTypeId,
  });

  if (!targetContentTypeId) {
    return (
      <div className="text-sm text-yellow-600">
        Reference target not configured
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="text-sm text-gray-500">Loading options...</div>
    );
  }

  if (config.multiple) {
    // Multiple references - checkboxes
    return (
      <div className="space-y-2 max-h-64 overflow-y-auto border border-gray-200 rounded-md p-3">
        {instances && instances.length > 0 ? (
          instances.map((instance) => (
            <div key={instance.id} className="flex items-center">
              <input
                type="checkbox"
                checked={Array.isArray(value) && value.includes(instance.id)}
                onChange={(e) => {
                  const currentValues = Array.isArray(value) ? value : [];
                  if (e.target.checked) {
                    onChange([...currentValues, instance.id]);
                  } else {
                    onChange(currentValues.filter((v) => v !== instance.id));
                  }
                }}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label className="ml-2 text-sm text-gray-700">
                {instance.data?.title || instance.data?.name || instance.id}
              </label>
            </div>
          ))
        ) : (
          <p className="text-sm text-gray-500">No instances available</p>
        )}
      </div>
    );
  } else {
    // Single reference - dropdown
    return (
      <select
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        className={`w-full px-3 py-2 border rounded-md focus:ring-primary-500 focus:border-primary-500 ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
      >
        <option value="">-- Select --</option>
        {instances?.map((instance) => (
          <option key={instance.id} value={instance.id}>
            {instance.data?.title || instance.data?.name || instance.id}
          </option>
        ))}
      </select>
    );
  }
}
