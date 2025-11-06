# Quality Assurance Agent

**Role**: Comprehensive quality validation and commercial-grade certification
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Quality Assurance Agent orchestrates all review processes, validates content accuracy, ensures production quality, and issues commercial-grade certification. It manages iterative review cycles and provides the final quality seal.

## Key Capabilities

- Orchestrates Pedagogical Reviewer, Accessibility Validator (Phase 2), Standards Compliance (Phase 2)
- Validates content accuracy against authoritative sources
- Checks production quality (formatting, images, media)
- Ensures brand consistency
- Manages revision cycles with Content Developer
- Issues commercial-grade certification

## Skills Used

- All `/curriculum.review-*` skills
- `/learning.quality-assurance`
- Standards skills (coordinates Standards Compliance Agent in Phase 2)

## Autonomous Decisions

- Which quality dimensions to prioritize
- Whether materials meet commercial-grade thresholds
- Iteration strategy when issues found
- Issue severity categorization
- When to escalate to human review
- Final certification and sign-off

## CLI Interface

```bash
/agent.quality-assurance \
  --materials "curriculum-final-draft/" \
  --quality-level "commercial-grade" \
  --dimensions "pedagogy,accuracy,accessibility,compliance,production" \
  --auto-iterate \
  --certification-required
```

## Performance Targets

- **Thoroughness**: 100% of artifacts reviewed
- **Accuracy**: >90% issue detection vs. human expert
- **Certification Rate**: >85% first-pass
- **Iteration Cycles**: <2 average

## Exit Codes

- **0**: Certified for commercial release
- **1**: Invalid materials provided
- **2**: Failed certification (critical issues)
- **3**: Maximum iterations exceeded (escalate)

**See**: `system-prompt.md` for complete agent prompt
