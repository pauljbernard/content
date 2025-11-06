# Professor Framework Issue Templates

These issue templates provide structured ways to request content development using the complete Professor framework (92 skills, 22 agents) integrated with the HMH Multi-Curriculum Knowledge Base through GitHub Actions automation.

**Need guidance?** See the complete documentation suite:
- **[AUTHOR_GUIDE.md](../../AUTHOR_GUIDE.md)** - Content authoring workflows and AI assistance
- **[EDITOR_GUIDE.md](../../EDITOR_GUIDE.md)** - Editorial review and quality checks
- **[PRODUCTION_GUIDE.md](../../PRODUCTION_GUIDE.md)** - Multi-format production and delivery
- **[ENGINEER_GUIDE.md](../../ENGINEER_GUIDE.md)** - System architecture and extension
- **[USER_GUIDE.md](../../USER_GUIDE.md)** - Overview and navigation

## How It Works

1. **Create an Issue** using one of the templates below
2. **Fill in the form** with your requirements
3. **Submit** - GitHub Actions automatically triggers
4. **Professor framework** processes your request using appropriate skills/agents
5. **Results** are committed and reported back to the issue

All templates trigger the `professor-automation.yml` workflow which uses the official `anthropics/claude-code-action`.

## Available Templates

### Core Content Development

#### 📚 Curriculum Development
**File:** `01-curriculum-development.yml`
**Label:** `curriculum-development`

Create complete curriculum materials through autonomous workflow:
- Research topics and standards
- Design measurable learning objectives
- Develop comprehensive content
- Review for quality

**Skills:** curriculum.research, curriculum.design, curriculum.develop-content
**Agent:** curriculum-architect

---

#### 📝 Assessment Creation
**File:** `02-assessment-creation.yml`
**Label:** `assessment-creation`

Design and create comprehensive assessments:
- Assessment blueprints
- Items with rubrics
- Diagnostic, formative, summative assessments
- Adaptive assessments

**Skills:** curriculum.assess-design, curriculum.develop-items, learning.diagnostic-assessment
**Agent:** assessment-designer

---

#### 🎬 Multimedia & Interactive Activities
**File:** `03-multimedia-activities.yml`
**Label:** `multimedia-activities`

Create engaging multimedia and interactive experiences:
- Video/audio scripts
- Educational games
- Simulations and virtual labs
- Collaborative projects

**Skills:** curriculum.develop-multimedia, learning.game-designer, learning.simulation-designer
**Agent:** content-developer

---

### Quality & Compliance

#### ✅ Quality Review
**File:** `06-quality-review.yml`
**Label:** `quality-review`

Comprehensive quality validation:
- Pedagogical soundness review
- WCAG 2.1 accessibility check
- Bias and cultural responsiveness
- Standards alignment validation

**Skills:** curriculum.review-pedagogy, curriculum.review-accessibility, curriculum.review-bias
**Agents:** pedagogical-reviewer, quality-assurance

---

### Packaging & Delivery

#### 📦 LMS Packaging
**File:** `09-lms-packaging.yml`
**Label:** `lms-packaging`

Package content for learning management systems:
- SCORM 1.2/2004 packages
- Canvas course packages
- Moodle backups
- QTI assessment exports

**Skills:** curriculum.package-lms, curriculum.export-qti
**Agent:** scorm-validator

---

### Analytics & Improvement

#### 📊 Learning Analytics
**File:** `12-learning-analytics.yml`
**Label:** `learning-analytics`

Analyze learning data and generate insights:
- Outcome analysis (mastery rates, gaps)
- Impact measurement
- Kirkpatrick evaluation
- Predictive analytics

**Skills:** curriculum.analyze-outcomes, learning.impact-measurement, learning.kirkpatrick-evaluation
**Agent:** learning-analytics

---

#### 📋 Grading Assistance
**File:** `13-grading-assistance.yml`
**Label:** `grading-assistance`

Apply rubrics and grade student work:
- Consistent rubric application
- Detailed feedback generation
- Pattern identification
- Summary statistics

**Skills:** curriculum.grade-assist, learning.formative-assessment

---

### Autonomous Workflows

#### 🎓 Complete Course Development
**File:** `19-complete-course-development.yml`
**Label:** `autonomous-development`

**Full autonomous course development from start to finish:**

The curriculum-architect agent works autonomously through:
1. Needs analysis and research
2. Objective design
3. Content development
4. Assessment creation
5. Quality review
6. Packaging and delivery

This is the **most comprehensive** template - creates complete, publication-ready courses.

**Agent:** curriculum-architect (autonomous mode) coordinates all agents
**Expected Duration:** Several hours for complex courses

---

## Usage Examples

### Example 1: Create a Biology Lesson

1. Click **"New Issue"**
2. Select **"📚 Curriculum Development"**
3. Fill in:
   - Topic: "Photosynthesis"
   - Level: "9-12 (High School)"
   - Duration: "2 weeks"
   - Standards: "NGSS"
   - Deliverables: Lesson plans, activities, assessments
4. Submit
5. Wait for Professor to create materials
6. Review pull request with generated content

### Example 2: Quality Review

1. Click **"New Issue"**
2. Select **"✅ Quality Review"**
3. Fill in:
   - Content Path: `drafts/biology-unit/`
   - Review Types: Pedagogical, Accessibility, Bias
   - Strictness: Commercial-grade
4. Submit
5. Receive detailed review report in issue comments

### Example 3: Build a Complete Course (Autonomous)

1. Click **"New Issue"**
2. Select **"🎓 Complete Course Development"**
3. Fill in comprehensive course details
4. Enable autonomous mode
5. Submit
6. curriculum-architect agent works through all phases
7. Receive complete course in pull request(s)

## Template Structure

All templates follow this structure:

```yaml
name: Template Name
description: Brief description
title: "[Label] "
labels: ["specific-label", "professor-auto"]  # professor-auto triggers workflow

body:
  - type: markdown    # Description
  - type: input       # Text inputs
  - type: textarea    # Long text
  - type: dropdown    # Single/multiple choice
  - type: checkboxes  # Options
```

The `professor-auto` label is **required** for automation to trigger.

## Workflow Processing

When an issue is created with `professor-auto` label:

1. **professor-automation.yml** workflow triggers
2. Issue is parsed to extract form data
3. Professor framework is configured (97 skills, 18 agents)
4. Request type is determined from labels
5. Appropriate prompt is constructed
6. **anthropics/claude-code-action** is invoked
7. Claude Code uses Professor skills/agents to complete request
8. Results are committed to repository
9. Issue is updated with completion status

## Creating Custom Templates

To create a custom template:

1. Create `.github/ISSUE_TEMPLATE/your-template.yml`
2. Include `professor-auto` label
3. Add a specific label for your template type
4. Design form fields for your use case
5. Update `professor-automation.yml` to handle the new label
6. Add prompt logic for your template type

See existing templates for structure examples.

## Labels

### Automation Labels
- `professor-auto` - **Required** - Triggers automation
- `professor-completed` - Auto-applied on success
- `professor-failed` - Auto-applied on failure

### Request Type Labels
- `curriculum-development` - Curriculum creation
- `assessment-creation` - Assessment design
- `quality-review` - Quality validation
- `lms-packaging` - LMS package creation
- `learning-analytics` - Data analysis
- `grading-assistance` - Grading support
- `multimedia-activities` - Multimedia creation
- `autonomous-development` - Full course development

## Configuration

### Required Secrets
- `ANTHROPIC_API_KEY` - Your Anthropic API key for Claude Code

### Workflow Files
- `.github/workflows/professor-automation.yml` - Main automation workflow
- `.github/actions/setup-professor/` - Professor framework setup action

## Troubleshooting

### Issue not processing
- Verify `professor-auto` label is present
- Check workflow run logs in Actions tab
- Ensure API key secret is configured

### Wrong skills/agents used
- Check the request type label is correct
- Review prompt logic in `professor-automation.yml`
- May need to update prompt for your specific use case

### Quality issues with output
- Be more specific in issue form fields
- Add constraints and requirements
- Request higher quality level
- Use autonomous mode for more thorough processing

## Support

**Documentation by Role:**
- **Content Authors**: See [AUTHOR_GUIDE.md](../../AUTHOR_GUIDE.md) - AI assistance covered in Section 5
- **Content Editors**: See [EDITOR_GUIDE.md](../../EDITOR_GUIDE.md) - Review workflows and checklists
- **Production Staff**: See [PRODUCTION_GUIDE.md](../../PRODUCTION_GUIDE.md) - Packaging and delivery
- **Engineers**: See [ENGINEER_GUIDE.md](../../ENGINEER_GUIDE.md) - System extension and configs

**Technical Resources:**
- **Workflow Issues**: Check `.github/workflows/professor-automation.yml`
- **Template Issues**: Check individual template files
- **Professor Skills**: See `.claude/skills/README.md` (if available)
- **Professor Agents**: See `.claude/agents/README.md` (if available)
- **HMH Knowledge Base**: See [ENGINEER_GUIDE.md](../../ENGINEER_GUIDE.md) for architecture

## Version

**Templates Version:** 1.1.0
**Professor Version:** 2.0.0 (92 skills, 22 agents)
**HMH Knowledge Base:** 50 files, 85-97% reuse
**Documentation Suite:** v3.0.0 (3,785 lines)
**Last Updated:** 2025-11-06
