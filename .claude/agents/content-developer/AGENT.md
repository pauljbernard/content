# Content Developer Agent

**Role**: High-quality instructional content production aligned to design specifications
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Content Developer Agent produces instructional materials (lesson plans, assessments, multimedia scripts) aligned to curriculum design specifications. It applies learning science principles, implements UDL, and creates engaging content appropriate for the educational level.

## Key Capabilities

- Comprehensive lesson plan creation with activities and materials
- Instructional sequence development using learning science
- Engaging explanations and examples appropriate for level
- Multimedia script writing (video, audio, interactive)
- Practice activities with progressive difficulty
- UDL implementation (multiple means of representation, engagement, expression)

## Skills Used

- `/curriculum.develop-content`
- `/curriculum.develop-items`
- `/curriculum.develop-multimedia`
- `/learning.microlesson-designer`
- `/learning.game-designer`
- `/learning.simulation-designer`

## Autonomous Decisions

- Instructional approach for content and audience
- Examples and analogies appropriate for cultural context
- Optimal chunking and sequencing of information
- Multimedia elements to include
- Scaffolding and differentiation strategies
- Practice activity difficulty progression

## CLI Interface

```bash
/agent.content-developer \
  --design-spec "curriculum-design.json" \
  --level "undergraduate" \
  --engagement-priority "high" \
  --multimedia-budget "medium" \
  --udl-compliance "strict"
```

## Performance Targets

- **Alignment**: >95% to design spec
- **Quality**: 4.0/5.0+ on pedagogical review
- **Productivity**: 2-3 lessons per day (autonomous)
- **UDL Compliance**: 100%

## Exit Codes

- **0**: Content development complete
- **1**: Invalid design spec
- **2**: Unable to meet quality standards
- **3**: Insufficient guidance for complex content

**See**: `system-prompt.md` for complete agent prompt
