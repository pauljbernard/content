# SCORM Testing Agent

**Role**: SCORM package validation and LMS compatibility testing
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The SCORM Testing Agent validates SCORM 1.2 and 2004 packages for compliance, tests compatibility across multiple LMS platforms (Canvas, Moodle, Blackboard), and provides automated remediation for common SCORM issues. Ensures educational content packages work reliably in target learning management systems.

## Key Capabilities

- SCORM package structure and manifest validation (1.2 and 2004)
- imsmanifest.xml compliance checking
- API compatibility verification (SCORM RTE)
- Multi-LMS compatibility testing (Canvas, Moodle, Blackboard, Brightspace)
- Automated issue detection and remediation
- Tracking and scoring validation
- Launch and completion testing
- Packaging standards compliance scoring

## Skills Used

- Internal SCORM testing engine (scorm_testing_engine.py)
- SCORM API simulation and validation
- Manifest parsing and validation algorithms
- LMS compatibility test suites

## Autonomous Decisions

- Appropriate SCORM version validation rules (1.2 vs. 2004)
- Issue severity classification (critical, major, minor)
- Remediation strategy selection
- LMS-specific compatibility requirements
- API method validation priorities
- Manifest structure validation criteria
- Test completion thresholds
- Package scoring algorithms

## CLI Interface

```bash
/agent.scorm-testing \
  --action "validate_package" \
  --package-path "dist/biology-unit-1.zip" \
  --scorm-version "2004" \
  --test-lms "canvas,moodle,blackboard"
```

### Available Actions

- `validate_package` - Validate SCORM package structure and manifest
- `test_lms_compatibility` - Test across multiple LMS platforms
- `auto_remediate` - Automatically fix common SCORM issues

## Performance Targets

- **Validation Accuracy**: >99% issue detection rate
- **LMS Coverage**: Test against 4+ major LMS platforms
- **Remediation Success**: >90% auto-fix success rate
- **Validation Speed**: <2 minutes per package

## Exit Codes

- **0**: SCORM package valid and LMS-compatible
- **1**: Invalid package path or version
- **2**: Critical SCORM compliance issues found
- **3**: LMS compatibility failures detected

**See**: `system-prompt.md` for complete agent prompt
