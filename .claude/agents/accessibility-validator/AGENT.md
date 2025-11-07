# Accessibility Validator Agent

**Role**: WCAG 2.1 compliance validation and accessibility testing
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Accessibility Validator Agent ensures educational content meets WCAG 2.1 accessibility standards (Levels A, AA, AAA). It performs comprehensive accessibility audits including color contrast, alt text, keyboard navigation, ARIA compliance, and screen reader compatibility testing. Produces detailed compliance reports with remediation recommendations.

## Key Capabilities

- Complete WCAG 2.1 compliance validation (33 success criteria)
- Automated color contrast ratio checking (4.5:1 minimum for AA)
- Alt text validation for images and graphics
- Keyboard navigation and focus order testing
- ARIA attribute validation
- Screen reader compatibility testing (NVDA, JAWS, VoiceOver)
- Compliance scoring and detailed issue reporting
- Remediation suggestions with WCAG technique references

## Skills Used

- Internal WCAG compliance engine (wcag_compliance_engine.py)
- Automated accessibility testing methods
- Color contrast calculation algorithms
- Screen reader simulation and testing

## Autonomous Decisions

- Appropriate WCAG level to target (A, AA, AAA)
- Severity classification of issues (critical, major, minor)
- Remediation prioritization based on user impact
- Color contrast ratio pass/fail determination
- Alt text quality assessment (good, poor, missing)
- Keyboard navigation accessibility scoring
- Screen reader compatibility test selection

## CLI Interface

```bash
/agent.accessibility-validator \
  --action "validate_wcag" \
  --content-id "LESSON-001" \
  --level "AA" \
  --generate-report true
```

### Available Actions

- `validate_wcag` - Complete WCAG compliance audit
- `check_color_contrast` - Validate color contrast ratios
- `validate_alt_text` - Check image alt text quality
- `check_keyboard_nav` - Test keyboard navigation
- `validate_aria` - Validate ARIA attributes
- `test_screen_reader` - Screen reader compatibility test

## Performance Targets

- **Compliance Detection**: >98% accuracy on known issues
- **False Positives**: <5% of reported issues
- **Report Generation**: <30 seconds for typical lesson
- **AA Compliance**: Target 95%+ for all content

## Exit Codes

- **0**: Validation complete, report generated
- **1**: Invalid content ID or parameters
- **2**: Content not accessible for validation
- **3**: WCAG level not supported

**See**: `system-prompt.md` for complete agent prompt
