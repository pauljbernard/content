# Learning Analytics Agent

**Role**: Learning outcomes analysis and performance insights generation
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Learning Analytics Agent analyzes student performance data, calculates learning outcomes, identifies achievement gaps, and generates actionable insights for curriculum improvement. Provides data-driven recommendations, mastery rate calculations, predictive analytics, and cohort comparisons to support evidence-based instructional decisions.

## Key Capabilities

- Learning outcomes analysis with objective mastery calculations
- Student performance metrics and trend analysis
- Achievement gap identification across demographics
- Actionable insights generation with recommendations
- Predictive performance modeling
- Cohort comparison analysis (class, school, district)
- Visualization generation (charts, dashboards, reports)
- Kirkpatrick Level 1-4 impact measurement

## Skills Used

- `/curriculum.analyze-outcomes`
- Internal analytics algorithms (statistical analysis, predictive modeling)
- Data visualization libraries
- Performance metric calculations

## Autonomous Decisions

- Appropriate mastery threshold determination (typically 80%)
- Statistical significance testing for gap identification
- Insight prioritization based on impact and feasibility
- Visualization type selection for data presentation
- Performance prediction model selection
- Cohort segmentation strategies
- Recommendation generation based on data patterns
- Outlier detection and handling

## CLI Interface

```bash
/agent.learning-analytics \
  --action "analyze_outcomes" \
  --assessment-data "data/results.csv" \
  --learning-objectives '["OBJ-001", "OBJ-002", "OBJ-003"]' \
  --generate-dashboard true
```

### Available Actions

- `analyze_outcomes` - Comprehensive learning outcomes analysis
- `calculate_mastery` - Calculate objective mastery rates
- `identify_gaps` - Identify learning and achievement gaps
- `generate_insights` - Generate actionable recommendations
- `predict_performance` - Predict future student performance
- `compare_cohorts` - Compare different student groups

## Performance Targets

- **Analysis Speed**: <5 seconds for 1,000 student records
- **Insight Accuracy**: >90% actionable recommendations
- **Gap Detection**: >95% accuracy on known achievement gaps
- **Prediction Accuracy**: R² > 0.75 for performance models

## Exit Codes

- **0**: Analysis complete, insights generated
- **1**: Invalid assessment data or parameters
- **2**: Insufficient data for statistical analysis
- **3**: Unable to generate meaningful insights

**See**: `system-prompt.md` for complete agent prompt
