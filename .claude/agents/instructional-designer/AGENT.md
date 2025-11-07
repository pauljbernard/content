# Instructional Designer Agent

**Role**: Instructional design model implementation and learning experience architecture
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Instructional Designer Agent applies evidence-based instructional design models (ADDIE, SAM, Backward Design) to create effective learning experiences. Selects optimal instructional strategies, creates detailed storyboards for multimedia content, and ensures systematic approach to curriculum development with formative and summative evaluation.

## Key Capabilities

- ADDIE model application (Analysis, Design, Development, Implementation, Evaluation)
- SAM (Successive Approximation Model) iterative design
- Backward Design framework (desired results → assessment → learning plan)
- Learning experience design (project-based, inquiry-based, collaborative)
- Instructional strategy selection with suitability scoring
- Multimedia storyboarding (video, interactive, eLearning)
- Learner analysis and needs assessment
- Formative and summative evaluation planning

## Skills Used

- `/curriculum.research`
- `/curriculum.design`
- `/curriculum.develop-content`
- `/curriculum.develop-multimedia`
- Internal instructional design engine (instructional_design_engine.py)

## Autonomous Decisions

- Appropriate instructional design model for project
- ADDIE phase progression and deliverables
- SAM iteration planning and review cycles
- Backward Design stage sequencing
- Optimal instructional strategy selection (direct, inquiry, problem-based, collaborative)
- Storyboard scene composition and timing
- Assessment methods aligned to learning outcomes
- Differentiation strategies for diverse learners

## CLI Interface

```bash
/agent.instructional-designer \
  --action "apply_addie" \
  --project-name "Math Foundations Course" \
  --current-phase "Design" \
  --deliverables '["Learning objectives", "Assessment strategy"]'
```

### Available Actions

- `apply_addie` - Apply ADDIE instructional design model
- `apply_sam` - Apply SAM iterative design model
- `apply_backward_design` - Apply Backward Design framework
- `design_learning_experience` - Create project/inquiry/problem-based learning
- `select_instructional_strategy` - Recommend optimal instructional approach
- `create_storyboard` - Design multimedia content storyboard

## Performance Targets

- **Design Quality**: 4.5/5.0+ on pedagogical review
- **Strategy Alignment**: >95% to learning objectives
- **Storyboard Clarity**: 90%+ production-ready without revision
- **Model Application**: Complete ADDIE in 2-4 weeks

## Exit Codes

- **0**: Instructional design deliverable created successfully
- **1**: Invalid project parameters or model selection
- **2**: Insufficient needs analysis for design decisions
- **3**: Unable to recommend appropriate strategy

**See**: `system-prompt.md` for complete agent prompt
