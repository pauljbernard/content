# Content Repository

**World-class educational content development powered by the Professor framework**

This repository provides automated, AI-powered content development capabilities using Claude Code integrated with the [Professor framework](https://github.com/pauljbernard/professor) - a comprehensive learning engineering platform with **92 specialized skills** and **22 autonomous agents**.

## Quick Start

### 1. Use @claude in Issues or PRs

Simply mention `@claude` in any issue or pull request comment:

```
@claude Create a lesson plan on photosynthesis for 6th grade aligned with NGSS standards
```

Claude will automatically respond using the full Professor framework.

### 2. Run Automated Workflows

Go to **Actions** → **Automated Content Development with Professor** and provide:
- Task description
- Educational level
- Standards alignment
- Output location

### 3. Scheduled Reviews

Every Monday, the system automatically reviews published content for quality, accessibility, and bias.

## What Can This Repository Do?

### 📚 Content Creation
- **Curriculum Development**: Complete courses, units, and lesson plans
- **Assessment Design**: Quizzes, tests, rubrics, and performance tasks
- **Multimedia Content**: Scripts, storyboards, interactive activities
- **Supporting Materials**: Handouts, worksheets, study guides

### 🔍 Quality Assurance
- **Pedagogical Review**: Validate learning design and instructional strategies
- **Accessibility Check**: Ensure WCAG 2.1 AA compliance
- **Bias Detection**: Identify and eliminate bias and cultural insensitivity
- **Standards Alignment**: Verify alignment to educational standards

### 📦 Publishing & Delivery
- **LMS Packages**: Generate SCORM 1.2/2004 packages
- **PDF Generation**: Create print-ready materials
- **Web Content**: Build responsive HTML/CSS content
- **Multi-format Export**: QTI, Canvas, Moodle formats

### 📊 Analytics & Improvement
- **Outcome Analysis**: Analyze student performance data
- **Impact Measurement**: Kirkpatrick evaluation
- **Iterative Improvement**: Data-driven content refinement

## Repository Structure

```
content/
├── CLAUDE.md                    # Claude Code configuration
├── .claude/                     # Claude Code local configs
│   └── commands/                # Spec-kit commands (tracked)
├── .github/
│   ├── actions/
│   │   └── setup-professor/     # Composite action for Professor setup
│   └── workflows/
│       ├── claude-professor.yml           # @claude mention integration
│       ├── content-development-automated.yml  # Manual content creation
│       └── scheduled-content-review.yml   # Automated quality reviews
├── drafts/                      # Work-in-progress content
├── published/                   # Finalized, approved content
├── assessments/                 # Quizzes, tests, rubrics
├── multimedia/                  # Scripts, storyboards
├── specs/                       # Specifications and requirements
├── analytics/                   # Outcome data and reports
└── reviews/                     # Quality review reports
```

## Professor Framework

This repository integrates the complete Professor framework:

### 92 Skills
Organized into 19 categories:
- Curriculum Research & Design
- Content Development
- Assessment Design & Development
- Review & Quality Assurance
- Packaging & Delivery
- Analytics & Measurement
- Personalization & Adaptation
- Learning Support
- And more...

### 22 Agents
Autonomous agents that orchestrate skills:
- `curriculum-architect` - Designs curriculum structures
- `content-developer` - Creates learning materials
- `assessment-designer` - Designs assessments
- `pedagogical-reviewer` - Reviews quality
- `quality-assurance` - Ensures standards
- `learning-analytics` - Analyzes outcomes
- And 16 more specialized agents...

### Framework Components
- **Spec-Kit**: Specification-driven development
- **API Integration**: Connect to external platforms
- **Agent Coordination**: Multi-agent orchestration

## Workflows

### Interactive Mode: @claude Mentions

**In Issues:**
```
@claude Create a complete unit on the American Revolution for 8th grade

Please include:
- 5 lesson plans
- Formative assessments for each lesson
- A summative unit test
- All aligned to C3 Framework standards
```

**In Pull Requests:**
```
@claude Review this lesson plan for pedagogical soundness and accessibility
```

### Automated Mode: Workflow Dispatch

1. Go to **Actions** tab
2. Select **"Automated Content Development with Professor"**
3. Click **"Run workflow"**
4. Fill in the form:
   - **Task**: "Create a diagnostic assessment for algebra readiness"
   - **Level**: "9-12 (High School)"
   - **Standards**: "CCSS Math"
   - **Output**: "assessments/"
   - **Create PR**: ✅ Yes
5. Click **"Run workflow"**

The system will:
- Configure Claude Code with Professor framework
- Execute the task using appropriate skills and agents
- Generate high-quality content
- Create a pull request for review

### Scheduled Mode: Automatic Reviews

Every Monday at 9 AM UTC, the system automatically:
- Reviews all published content
- Checks pedagogical quality
- Validates accessibility compliance
- Detects bias or issues
- Creates an issue with findings and recommendations

## Educational Levels Supported

- **K-5**: Elementary (ages 5-10)
- **6-8**: Middle School (ages 11-13)
- **9-12**: High School (ages 14-18)
- **Undergraduate**: 4-year college/university
- **Graduate**: Master's level
- **Post-graduate**: PhD/Doctoral level
- **Professional Learning**: Corporate training, continuing education

## Standards Frameworks

- **NGSS**: Next Generation Science Standards
- **CCSS**: Common Core State Standards
- **C3 Framework**: College, Career, and Civic Life
- **State Standards**: All US states
- **International**: IB, Cambridge, etc.
- **Professional**: Industry certifications

## Quality Standards

All content created in this repository adheres to:

### Pedagogical Standards
- Evidence-based learning science
- Bloom's Taxonomy for objectives
- Universal Design for Learning (UDL)
- Backwards design methodology
- Constructive alignment

### Accessibility Standards
- WCAG 2.1 Level AA minimum
- Section 508 compliance
- Screen reader compatibility
- Keyboard navigation
- Alternative text for images

### Technical Standards
- SCORM 1.2 and 2004
- LTI 1.3
- QTI 2.1/3.0
- xAPI (Tin Can)

## Setup & Configuration

### Prerequisites

1. **Anthropic API Key**: Add `ANTHROPIC_API_KEY` to repository secrets
2. **Professor Access**: Ensure you have access to the private Professor repository
3. **GitHub Permissions**: Workflows need `contents: write` and `pull-requests: write`

### Installation

The Professor framework is automatically configured when workflows run. No manual setup required!

The `setup-professor` composite action:
1. Clones the Professor repository
2. Configures all 92 skills
3. Configures all 22 agents
4. Sets up spec-kit commands
5. Merges with local configurations
6. Validates the setup

## Examples

### Example 1: Create a Complete Course

```
@claude Create a complete 10-week course on Data Science for undergraduates

Include:
- Weekly learning objectives
- Lecture materials and slides
- Programming exercises (Python)
- Datasets for practice
- Weekly quizzes
- Midterm and final projects
- Rubrics for all assessments

Align to ACM Computer Science guidelines
```

### Example 2: Develop Adaptive Assessment

```
@claude Design an adaptive diagnostic assessment for algebra readiness

Requirements:
- 20-30 items spanning Algebra 1 prerequisites
- Adaptive branching based on performance
- Detailed remediation recommendations
- Teacher dashboard for results
- Export to Canvas format
```

### Example 3: Review and Improve Content

```
@claude Review the content in drafts/chemistry-unit/ for:

1. Pedagogical soundness
2. WCAG 2.1 AA accessibility
3. Cultural responsiveness and bias
4. NGSS standards alignment

Provide specific recommendations for improvement
```

## Contributing

### Adding Local Skills or Agents

1. Create skill/agent in `.claude/skills/` or `.claude/agents/`
2. Follow Professor naming conventions
3. Document usage in skill SKILL.md or agent AGENT.md
4. Skills will be automatically merged with Professor framework

### Improving Content

1. Make changes to content files
2. Run accessibility and quality checks
3. Update metadata and documentation
4. Create a pull request

## Support

- **Professor Framework**: https://github.com/pauljbernard/professor
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code
- **Issues**: Create an issue in this repository

## License

MIT License - See Professor framework for details

---

**Powered by:**
- [Claude Code](https://claude.com/claude-code) - AI-powered coding assistant
- [Professor Framework](https://github.com/pauljbernard/professor) - Learning engineering platform
- [Spec-Kit](https://github.com/github/spec-kit) - Specification-driven development

**Version**: 1.0.0
**Last Updated**: 2025-11-03
