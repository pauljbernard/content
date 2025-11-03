# Claude Code Framework Directory

This directory contains framework components for the content repository. Framework components provide infrastructure, utilities, and supporting functionality for skills and agents.

## What Are Framework Components?

Framework components are foundational building blocks that:
- Provide shared infrastructure for skills and agents
- Handle cross-cutting concerns (logging, state, coordination)
- Manage integrations with external systems
- Implement common patterns and utilities
- Support the overall architecture

## Professor Framework Components

When GitHub Actions workflows run, the **Professor framework** provides several framework components:

### API Integration
Located in `framework/api-integration/`:
- **Educational platform APIs** - Connect to LMS, assessment platforms
- **Standards repositories** - Fetch educational standards
- **Content delivery** - Publish to content delivery networks
- **Analytics platforms** - Send learning analytics data

### Client Portal
Located in `framework/client-portal/`:
- **User management** - Handle learner and instructor access
- **Content delivery** - Serve educational content
- **Progress tracking** - Monitor learner progress
- **Reporting** - Generate reports for stakeholders

### Agent Coordination
- **State manager** (`agents/framework/state-manager.py`) - Manages agent state
- **Coordination protocols** (`agents/framework/coordination.md`) - Agent communication
- **Event bus** - Publish/subscribe for agent events
- **Workflow orchestration** - Coordinate multi-agent workflows

## Local Framework Components

You can add custom framework components to this directory.

### Creating a Framework Component

1. Create a directory: `component-name/`
2. Add a `README.md` describing the component
3. Add implementation files

```markdown
# Framework Component: Your Component Name

**Version**: 1.0.0
**Purpose**: Brief description

## Overview

What this component provides and why it's needed.

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Architecture

How this component is structured and integrates with the system.

## Usage

### For Skills
How skills can use this component.

### For Agents
How agents can use this component.

## Configuration

Configuration options and environment variables.

## API Reference

Key functions, classes, or interfaces provided.

## Examples

Practical examples of using this component.

## Dependencies

- External dependencies
- System requirements
- Other framework components

## Testing

How to test this component.

## Deployment

How this component is deployed in workflows.
```

## Framework Structure

```
.claude/framework/
├── api-integration/          # External API integrations
│   ├── README.md
│   ├── lms-connector.py
│   ├── standards-api.py
│   └── analytics-client.py
├── client-portal/            # Content delivery portal
│   ├── README.md
│   ├── app.py
│   └── templates/
├── utilities/                # Common utilities
│   ├── README.md
│   ├── logging.py
│   └── validation.py
├── state-management/         # State management
│   ├── README.md
│   └── state-manager.py
└── README.md                 # This file
```

## Common Framework Components

### Utilities
Shared utilities used across skills and agents:
- **Logging** - Structured logging
- **Validation** - Input/output validation
- **Error handling** - Standardized error handling
- **Configuration** - Configuration management
- **Caching** - Result caching

### Data Management
- **Storage adapters** - Connect to various storage systems
- **Data transformers** - Convert between formats
- **Schema validators** - Validate data structures
- **Database connectors** - Database integrations

### Integration Services
- **API clients** - Connect to external services
- **Webhooks** - Handle incoming webhooks
- **Event publishers** - Publish events to external systems
- **Authentication** - Manage authentication/authorization

### Workflow Support
- **Task queues** - Asynchronous task processing
- **State machines** - Workflow state management
- **Schedulers** - Schedule recurring tasks
- **Retry logic** - Resilient operations

## Integration with Workflows

When GitHub Actions workflows run:
1. Professor framework is cloned
2. Professor framework components are configured
3. Local framework components are merged
4. Skills and agents can use any framework component

The `setup-professor` composite action ensures all framework components are properly configured.

## Examples of Custom Framework Components

You might create local framework components for:

### `organization-api/`
Connect to your organization's internal APIs:
- Student information system
- Learning management system
- Content management system
- Authentication provider

### `brand-assets/`
Manage brand and style resources:
- Logo files and guidelines
- Color palettes
- Typography rules
- Template library

### `workflow-automation/`
Custom workflow automation:
- Approval workflows
- Notification systems
- Integration with Slack/Teams
- Custom reporting

### `compliance-checker/`
Organization-specific compliance:
- Privacy regulations (COPPA, FERPA)
- Accessibility standards
- Industry certifications
- Security requirements

## Framework Best Practices

1. **Keep framework code separate from skills/agents**
   - Framework = infrastructure
   - Skills = capabilities
   - Agents = orchestration

2. **Make components reusable**
   - Generic interfaces
   - Configuration-driven
   - Well-documented APIs

3. **Version your components**
   - Semantic versioning
   - Changelog maintenance
   - Backward compatibility

4. **Test thoroughly**
   - Unit tests for utilities
   - Integration tests for connectors
   - End-to-end tests for workflows

5. **Document extensively**
   - Clear README files
   - API documentation
   - Usage examples

## Configuration Files

Framework components often need configuration:

### `config.json`
```json
{
  "api_endpoints": {
    "lms": "https://lms.example.com/api",
    "standards": "https://standards.example.com/api"
  },
  "features": {
    "caching_enabled": true,
    "analytics_enabled": true
  },
  "limits": {
    "max_retries": 3,
    "timeout_seconds": 30
  }
}
```

### `.env` (gitignored)
```bash
API_KEY=your-api-key-here
DATABASE_URL=your-database-url
SECRET_KEY=your-secret-key
```

## Resources

- **Professor Framework**: https://github.com/pauljbernard/professor
- **Professor API Integration**: See `professor/framework/api-integration/`
- **Professor Client Portal**: See `professor/framework/client-portal/`

---

**Note**: This directory is tracked in version control except for sensitive configuration files (use .env for secrets). The `setup-professor` composite action merges these with Professor framework components automatically.
