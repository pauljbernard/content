# Testing Claude Code + Professor Integration

## Prerequisites Checklist

- [x] `ANTHROPIC_API_KEY` added as repository secret
- [x] Access to private Professor repository (https://github.com/pauljbernard/professor.git)
- [x] Workflows committed to repository
- [x] Issue template available

## Test 1: Setup Workflow via Issue

1. **Create a setup issue:**
   - Go to https://github.com/pauljbernard/content/issues/new/choose
   - Select "Setup/Update Claude Code CLI with Professor"
   - Fill in the form:
     - Action Type: `Install Claude Code CLI (fresh installation)`
     - Professor Branch: `main` (or your preferred branch)
     - Check the acknowledgment boxes
   - Click "Submit new issue"

2. **Monitor the workflow:**
   - The workflow should trigger automatically
   - Check https://github.com/pauljbernard/content/actions
   - You should see "Claude Code CLI Setup with Professor" running

3. **Expected results:**
   - Workflow installs Claude Code CLI
   - Clones Professor repository
   - Configures Claude Code with Professor components
   - Posts results back to the issue
   - Issue is automatically closed with "completed" label
   - Configuration artifact is available for download

4. **Verify success:**
   - Check the issue comments for success message
   - Download the configuration artifact from the workflow run
   - Review `configuration-summary.md` for installed components

## Test 2: Manual Workflow Dispatch

1. **Run the setup workflow manually:**
   - Go to https://github.com/pauljbernard/content/actions/workflows/claude-code-setup.yml
   - Click "Run workflow"
   - Select:
     - Action: `install`
     - Professor branch: `main`
   - Click "Run workflow"

2. **Expected results:**
   - Same as Test 1, but without issue updates
   - Check workflow logs for detailed output
   - Download configuration artifact

## Test 3: Content Development Workflow (Example)

1. **Run the example workflow:**
   - Go to https://github.com/pauljbernard/content/actions/workflows/example-content-workflow.yml
   - Click "Run workflow"
   - Fill in:
     - Task type: `Create new article`
     - Task details: `Write a brief article about GitHub Actions best practices`
     - Target path: `content` (or leave default)
   - Click "Run workflow"

2. **Expected results:**
   - Workflow sets up Claude Code with Professor
   - Creates a task file
   - Executes the content development task
   - Creates a pull request with changes
   - PR is labeled with `automated`, `content`, `professor`

3. **Review the PR:**
   - Check the PR title: `[Professor] Create new article: ...`
   - Review the changes made
   - Verify content quality
   - Merge or provide feedback

## Troubleshooting

### Workflow fails with "API key not set"
- Verify the secret name is exactly `ANTHROPIC_API_KEY`
- Check that the secret is set at the repository level (not environment level)
- Ensure the workflow has permission to access secrets

### Workflow fails with "Professor repository access denied"
- Verify you have read access to the Professor repository
- Check that the repository URL is correct: `https://github.com/pauljbernard/professor.git`
- Ensure the branch exists in the Professor repository

### No skills/commands found
- Check the Professor repository structure
- Verify it contains `.claude/skills`, `.claude/commands`, or root-level `skills/`, `commands/` directories
- Check the workflow logs for details about what was copied

### Claude Code command not found
- The workflow installs it automatically using npm
- Check the "Install/Update Claude Code CLI" step in workflow logs
- Verify Node.js setup step completed successfully

## Success Indicators

✅ **Setup workflow completes successfully**
- Exit code 0
- Issue is closed with "completed" label
- Configuration artifact contains files
- Summary shows installed components count > 0

✅ **Content development workflow completes successfully**
- Pull request is created
- Changes are committed
- Task file is generated
- No errors in logs

## Next Steps After Successful Testing

1. **Customize workflows for your needs:**
   - Create specific content development workflows
   - Add scheduled runs for regular content updates
   - Integrate with other CI/CD pipelines

2. **Configure Professor framework:**
   - Add/update skills in the Professor repository
   - Create custom slash commands
   - Define specialized sub-agents

3. **Set up branch protection:**
   - Require reviews for Professor-generated PRs
   - Add status checks
   - Configure auto-merge rules

4. **Monitor usage:**
   - Track API usage in Anthropic Console
   - Review generated content quality
   - Adjust prompts and configurations as needed

## Getting Help

If you encounter issues:

1. Check the workflow run logs for detailed error messages
2. Review the troubleshooting section above
3. Verify all prerequisites are met
4. Check the `.github/README.md` for additional documentation
5. Create an issue in the repository with:
   - Workflow run URL
   - Error messages
   - Steps to reproduce
