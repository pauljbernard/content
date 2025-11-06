# Claude Code Skills Directory

This directory contains Claude Code skills for the content repository. Skills are specialized capabilities that Claude Code can use to perform specific tasks.

## What Are Skills?

Skills are reusable, composable capabilities that extend Claude Code's functionality. Each skill:
- Performs a specific, well-defined function
- Can be invoked via command-line or automatically
- Outputs structured data that can feed into other skills
- Follows learning engineering best practices

## Professor Framework Skills

When GitHub Actions workflows run, the **Professor framework** provides **92 specialized skills** including:

### Curriculum Development (15 skills)
- `curriculum.research` - Research topics and align to standards
- `curriculum.design` - Design learning objectives using Bloom's Taxonomy
- `curriculum.develop-content` - Create lesson plans and materials
- `curriculum.develop-items` - Generate assessment items
- `curriculum.develop-multimedia` - Create multimedia scripts
- And more...

### Review & Quality (5 skills)
- `curriculum.review-pedagogy` - Review pedagogical soundness
- `curriculum.review-accessibility` - Check WCAG 2.1 compliance
- `curriculum.review-bias` - Detect bias and cultural issues
- And more...

### Packaging & Delivery (6 skills)
- `curriculum.package-lms` - Generate SCORM packages
- `curriculum.package-pdf` - Create PDF materials
- `curriculum.package-web` - Build web content
- And more...

### Analytics & Assessment (8 skills)
- `curriculum.analyze-outcomes` - Analyze learning outcomes
- `curriculum.grade-assist` - Assist with grading
- `curriculum.iterate-feedback` - Incorporate feedback
- And more...

### 58 Additional Skills
Including: needs analysis, market research, personalization, diagnostics, adaptive learning, tutoring systems, impact measurement, and more.

## Local Skills

You can add custom skills to this directory that are specific to this repository. Local skills will be **merged with Professor skills** when workflows run.

### Creating a Local Skill

1. Create a new file: `your-skill-name.md`
2. Follow the skill template format:

```markdown
# Skill: Your Skill Name

**Category**: Content Development
**Version**: 1.0.0

## Description

Brief description of what this skill does.

## Usage

How to invoke this skill:
- Command: `/your-skill-name [arguments]`
- Arguments: List of arguments and their purpose

## Inputs

What data this skill expects as input.

## Outputs

What data this skill produces as output.

## Examples

### Example 1
[Input and expected output]

## Dependencies

- Other skills this depends on
- Required tools or libraries

## Notes

Any additional information or best practices.
```

3. Test locally with Claude Code
4. Commit to the repository

## Skill Organization

Skills in this directory should:
- Be focused on a single, specific task
- Have clear inputs and outputs
- Be well-documented
- Follow naming conventions: `category.skill-name`
- Use kebab-case for file names

## Integration with Workflows

When GitHub Actions workflows run:
1. Professor framework is cloned
2. All 92 Professor skills are configured
3. Local skills from this directory are merged (local skills take precedence)
4. Claude Code can use any skill from either source

## Examples of Custom Skills

You might create local skills for:
- **content.style-guide** - Apply organization-specific style rules
- **content.brand-check** - Verify brand guidelines
- **content.terminology** - Enforce terminology consistency
- **assessment.custom-format** - Export to proprietary format
- **workflow.approval** - Custom approval workflow

## Resources

- **Professor Framework**: https://github.com/pauljbernard/professor
- **Claude Code Skills**: https://docs.claude.com/en/docs/claude-code/skills
- **Skill Development Guide**: See Professor repository documentation

---

**Note**: This directory is tracked in version control. Add skills that should be shared across the team. The `setup-professor` composite action merges these with Professor skills automatically.
