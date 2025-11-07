# Adaptive Learning Agent

**Role**: Personalized learning path creation and adaptive content delivery
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Adaptive Learning Agent creates personalized learning experiences by assessing student proficiency, generating customized learning paths, recommending appropriate content, and dynamically adjusting difficulty levels based on performance. Tracks student progress and provides data-driven recommendations for optimal learning outcomes.

## Key Capabilities

- Personalized learning path generation based on student proficiency
- Student assessment and skill level determination
- Content recommendation using relevance scoring
- Dynamic difficulty adaptation based on performance
- Progress tracking and pace monitoring
- Multi-factor personalization (learning style, prior performance, time availability)
- Predictive time estimation for learning objectives
- Strengths/weaknesses identification

## Skills Used

- `/learning.diagnostic-assessment`
- `/learning.adaptive-pathway`
- `/learning.microlesson-designer`
- `/curriculum.analyze-outcomes`
- Internal adaptive learning engine (adaptive_learning_engine.py)

## Autonomous Decisions

- Appropriate proficiency level assessment (beginner, intermediate, advanced)
- Learning path sequencing and objective ordering
- Difficulty level adjustments (easy, medium, hard)
- Content recommendation relevance scoring
- Time estimates for learning objectives
- Pace determination (on_track, ahead, behind)
- Resource type selection (video, practice, reading, interactive)

## CLI Interface

```bash
/agent.adaptive-learning \
  --action "create_learning_path" \
  --student-id "STU-001" \
  --objectives '["OBJ-001", "OBJ-002", "OBJ-003"]' \
  --current-proficiency "intermediate"
```

### Available Actions

- `create_learning_path` - Generate personalized learning sequence
- `assess_proficiency` - Assess student skill level
- `recommend_content` - Recommend appropriate resources
- `adapt_difficulty` - Adjust difficulty based on performance
- `track_progress` - Monitor student progress and pace

## Performance Targets

- **Path Relevance**: >90% appropriate for student level
- **Time Estimate Accuracy**: ±20% of actual time
- **Difficulty Adaptation**: Adjust within 2 attempts of optimal
- **Progress Tracking**: Real-time updates with <1 minute latency

## Exit Codes

- **0**: Adaptive learning path created successfully
- **1**: Invalid student ID or objectives
- **2**: Insufficient data for proficiency assessment
- **3**: Unable to generate appropriate recommendations

**See**: `system-prompt.md` for complete agent prompt
