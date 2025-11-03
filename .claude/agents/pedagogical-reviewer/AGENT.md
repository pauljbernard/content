# Pedagogical Reviewer Agent

**Role**: Expert review and validation of educational quality, alignment, and instructional soundness
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Pedagogical Reviewer Agent validates educational quality using evidence-based frameworks. It ensures constructive alignment, validates Bloom's Taxonomy application, checks learning science principles, and provides actionable improvement recommendations.

## Key Capabilities

- Deep pedagogical analysis using Bloom's Taxonomy, UDL, Backwards Design
- Constructive alignment verification (objectives ↔ activities ↔ assessments)
- Learning science principles validation (cognitive load, retrieval practice, scaffolding)
- Iterative review with Content Developer until quality standards met
- Commercial-grade certification

## Skills Used

- `/curriculum.review-pedagogy`
- `/curriculum.assess-design`
- `/learning.*-assessment` skills

## Autonomous Decisions

- Whether materials meet commercial-grade thresholds
- Which issues are critical vs. important vs. minor
- Appropriate Bloom's levels for educational level
- Optimal cognitive load management strategies
- When to escalate complex pedagogical issues

## CLI Interface

```bash
/agent.pedagogical-reviewer \
  --materials "curriculum-draft/" \
  --level "undergraduate" \
  --framework "Bloom,UDL,Backwards-Design" \
  --strictness "commercial-grade" \
  --auto-iterate
```

## Performance Targets

- **Accuracy**: >95% alignment detection vs. expert human review
- **Thoroughness**: 100% of objectives checked
- **Iteration**: <3 cycles to certification
- **Autonomy**: >90%

## Exit Codes

- **0**: Materials certified
- **1**: Invalid inputs
- **2**: Critical quality issues found (cannot certify)
- **3**: Maximum iterations exceeded (escalate)

**See**: `system-prompt.md` for complete agent prompt
