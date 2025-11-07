# Assessment Designer Agent

**Role**: Assessment blueprint design, item creation, and psychometric validation
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Assessment Designer Agent creates comprehensive assessments aligned to learning objectives including blueprints, test items (multiple-choice, constructed-response, performance tasks), scoring rubrics, and answer keys. Validates assessment quality, ensures bias-free items, and applies psychometric best practices for reliable and valid measurement.

## Key Capabilities

- Assessment blueprint creation with DOK alignment
- Test item generation (multiple-choice, constructed-response, performance tasks)
- Scoring rubric design with clear performance criteria
- Answer key generation with exemplar responses
- Assessment quality validation (validity, reliability, fairness)
- Bias detection and mitigation
- Item difficulty estimation
- Test specification alignment verification
- Psychometric analysis integration

## Skills Used

- `/curriculum.assess-design`
- `/curriculum.develop-items`
- Internal psychometrics engine (psychometrics_engine.py)
- Item writing best practices framework
- Bias detection algorithms

## Autonomous Decisions

- Assessment blueprint structure and item distribution
- Appropriate item types for learning objectives
- DOK level alignment to objectives
- Rubric criteria and performance levels
- Item difficulty targeting
- Bias review criteria and thresholds
- Assessment validity evidence requirements
- Answer key format and exemplar selection

## CLI Interface

```bash
/agent.assessment-designer \
  --action "design_blueprint" \
  --objectives '["OBJ-001", "OBJ-002", "OBJ-003"]' \
  --assessment-type "summative" \
  --dok-distribution "balanced"
```

### Available Actions

- `design_blueprint` - Create assessment blueprint aligned to objectives
- `create_items` - Generate assessment items (MC, CR, performance)
- `create_rubric` - Design detailed scoring rubric
- `create_answer_key` - Generate answer key with exemplars
- `validate_assessment` - Quality check for validity and reliability
- `review_bias` - Detect and mitigate assessment bias

## Performance Targets

- **Objective Alignment**: >95% of items aligned to blueprint
- **DOK Distribution**: ±5% of target distribution
- **Bias-Free Rate**: >98% items pass bias review
- **Rubric Clarity**: 4.5/5.0+ scorer agreement

## Exit Codes

- **0**: Assessment designed successfully, validated
- **1**: Invalid objectives or parameters
- **2**: Unable to meet quality standards
- **3**: Significant bias detected, revision required

**See**: `system-prompt.md` for complete agent prompt
