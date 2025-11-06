# GitHub Workflows - Claude Code with Professor Framework

This directory contains GitHub Actions workflows and issue templates for automating content development using Claude Code CLI configured with the Professor framework.

## Overview

The Professor framework integration enables automated content development workflows powered by Claude Code CLI with specialized skills, commands, and sub-agents from the private [professor repository](https://github.com/pauljbernard/professor.git).

## Components

### Issue Templates

#### `ISSUE_TEMPLATE/claude-code-setup.yml`
Issue template for requesting Claude Code CLI installation/updates with Professor framework configuration.

**Usage:**
1. Create a new issue using the "Setup/Update Claude Code CLI with Professor" template
2. Select your desired action (install, update, reconfigure, or reinstall)
3. Choose the Professor repository branch
4. Submit the issue - the workflow will automatically run
5. The issue will be updated with results and closed upon completion

### Workflows

#### `claude-code-setup.yml`
Automated workflow that installs/updates Claude Code CLI and configures it with the Professor framework.

**Triggered by:**
- Issues with the `claude-code` label
- Manual workflow dispatch

**What it does:**
1. Installs or updates Claude Code CLI to the latest version
2. Clones the Professor framework from the private repository
3. Configures Claude Code with:
   - Skills from Professor
   - Commands (slash commands) from Professor
   - Sub-agent configurations
   - Framework-specific settings
4. Validates the configuration
5. Creates a configuration artifact
6. Reports results back to the triggering issue

**Outputs:**
- Configuration summary markdown
- Downloadable artifact with full Claude Code configuration

#### `professor-content-development.yml`
Reusable workflow for content development tasks using Claude Code with Professor.

**Usage:**
```yaml
jobs:
  my-content-task:
    uses: ./.github/workflows/professor-content-development.yml
    with:
      task_description: "Create a technical article about GraphQL best practices"
      content_path: "content/articles/"
      professor_branch: "main"
      create_pr: true
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Inputs:**
- `task_description` (required): Description of the content development task
- `content_path` (optional): Path to content files (default: '.')
- `professor_branch` (optional): Professor framework branch (default: 'main')
- `create_pr` (optional): Create a pull request with changes (default: false)

**Secrets:**
- `ANTHROPIC_API_KEY` (required): Your Anthropic API key for Claude Code

**Outputs:**
- `result_summary`: JSON summary of the task execution

#### `example-content-workflow.yml`
Example workflow demonstrating how to use the Professor content development workflow.

**Usage:**
Run manually via workflow dispatch with:
- Task type selection
- Detailed task description
- Target path for content

## Setup Instructions

### Prerequisites

1. **Access to Professor Repository**
   - Ensure you have read access to `https://github.com/pauljbernard/professor.git`
   - The repository must contain Claude Code configurations (skills, commands, agents)

2. **Anthropic API Key**
   - Obtain an API key from [Anthropic Console](https://console.anthropic.com/)
   - Add it as a repository secret named `ANTHROPIC_API_KEY`:
     - Go to repository Settings → Secrets and variables → Actions
     - Click "New repository secret"
     - Name: `ANTHROPIC_API_KEY`
     - Value: Your Anthropic API key

3. **GitHub Token Permissions**
   - The default `GITHUB_TOKEN` needs access to:
     - Read private repositories (to clone Professor)
     - Write to issues (to update setup issues)
     - Write to pull requests (to create PRs)

### Initial Setup

1. **Create a setup issue:**
   - Navigate to Issues → New Issue
   - Select "Setup/Update Claude Code CLI with Professor"
   - Fill in the form
   - Submit

2. **Wait for completion:**
   - The workflow will run automatically
   - Progress updates will be posted to the issue
   - The issue will be closed when complete

3. **Verify configuration:**
   - Download the configuration artifact from the workflow run
   - Review the configuration summary

## Using Professor in Workflows

### Basic Example

```yaml
name: Create Article

on:
  workflow_dispatch:
    inputs:
      topic:
        description: 'Article topic'
        required: true

jobs:
  create-article:
    uses: ./.github/workflows/professor-content-development.yml
    with:
      task_description: "Write a comprehensive article about ${{ inputs.topic }}"
      content_path: "content/articles/"
      create_pr: true
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Advanced Example with Multiple Tasks

```yaml
name: Content Pipeline

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am

jobs:
  update-readme:
    uses: ./.github/workflows/professor-content-development.yml
    with:
      task_description: "Review and update the README.md file for clarity and completeness"
      content_path: "."
      professor_branch: "main"
      create_pr: true
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

  generate-docs:
    needs: update-readme
    uses: ./.github/workflows/professor-content-development.yml
    with:
      task_description: "Generate API documentation from code comments"
      content_path: "docs/"
      professor_branch: "main"
      create_pr: true
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Professor Framework Structure

The Professor framework should contain the following structure:

```
professor/
├── .claude/
│   ├── skills/           # Claude Code skills
│   ├── commands/         # Slash commands
│   ├── agents/           # Sub-agent configurations
│   ├── CLAUDE.md         # Main configuration file
│   └── config.json       # Additional settings
├── CLAUDE.md             # Alternative config location
└── README.md
```

Or alternatively:

```
professor/
├── skills/               # Root-level skills directory
├── commands/             # Root-level commands directory
├── agents/               # Root-level agents directory
├── CLAUDE.md
└── README.md
```

## Troubleshooting

### Issue: "Professor repository access denied"
- Verify you have read access to the Professor repository
- Check that the `GITHUB_TOKEN` has permission to read private repositories
- Ensure the repository URL is correct

### Issue: "Configuration files not found"
- Verify the Professor repository contains the expected directory structure
- Check that the branch name is correct
- Ensure configuration files exist in one of the expected locations

### Issue: "Claude Code command not found"
- The setup workflow should install Claude Code CLI automatically
- If using in a custom workflow, ensure you call the setup workflow first or install manually

### Issue: "ANTHROPIC_API_KEY not set"
- Verify the secret is created in repository settings
- Ensure the secret name matches exactly: `ANTHROPIC_API_KEY`
- Check that the workflow has access to the secret

## Security Considerations

1. **API Key Protection**
   - Never commit API keys to the repository
   - Always use GitHub Secrets for sensitive data
   - Rotate API keys regularly

2. **Private Repository Access**
   - The Professor repository is private and requires authentication
   - Access is managed through GitHub token permissions
   - Only users with access to both repositories can trigger workflows

3. **Code Review**
   - Always review PRs created by automated workflows
   - Verify generated content before merging
   - Use branch protection rules to enforce reviews

## Maintenance

### Updating Claude Code CLI
Create an issue using the setup template with action type "Update Claude Code CLI"

### Updating Professor Framework
Professor configurations are cloned fresh for each workflow run, so updates to the Professor repository are automatically picked up.

### Re-configuring
If you need to reconfigure without reinstalling:
1. Create an issue with action type "Reconfigure with Professor"
2. This will re-clone Professor and update configurations

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review workflow run logs for detailed error messages
3. Create an issue in this repository
4. Refer to [Claude Code documentation](https://github.com/anthropics/claude-code)

## License

This workflow configuration is part of the content repository and follows its license terms.
