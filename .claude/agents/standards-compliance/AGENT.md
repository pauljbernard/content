# Standards Compliance Agent

**Role**: Educational standards alignment validation and regulatory compliance verification
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Standards Compliance Agent validates alignment to educational content standards (CCSS, NGSS, TEKS, state-specific) and regulatory requirements (COPPA, FERPA, Section 508, WCAG). Checks coverage comprehensiveness, identifies gaps, generates alignment reports, and verifies state-specific adoption criteria compliance.

## Key Capabilities

- Multi-framework standards validation (CCSS, NGSS, TEKS, state standards)
- Standards coverage analysis and gap identification
- Alignment report generation with evidence documentation
- State-specific requirement validation (TX SBOE, CA Adoption, FL Statutory)
- Regulatory compliance checking (COPPA, FERPA, Section 508, WCAG)
- Cross-reference verification between materials and standards
- Benchmark-by-benchmark alignment documentation
- Adoption criteria scorecard generation

## Skills Used

- Internal standards validation engine
- Knowledge base integration (all 53 standards files)
- Regulatory compliance frameworks
- Alignment mapping algorithms

## Autonomous Decisions

- Appropriate standards framework selection based on state/district
- Coverage threshold determination (typically 95%+ for adoption)
- Gap severity classification (critical, moderate, minor)
- Evidence sufficiency assessment for alignment claims
- State requirement applicability determination
- Regulatory framework selection based on content type
- Compliance scoring algorithm application
- Report format and detail level

## CLI Interface

```bash
/agent.standards-compliance \
  --action "validate_alignment" \
  --materials-path "artifacts/lessons/" \
  --standards '["CCSS-M", "NGSS", "TX-TEKS"]' \
  --state "TX" \
  --generate-report true
```

### Available Actions

- `validate_alignment` - Validate standards alignment comprehensiveness
- `check_coverage` - Analyze standards coverage percentage
- `identify_gaps` - Identify uncovered standards and gaps
- `validate_state_requirements` - Check state-specific compliance (SBOE, adoption)
- `validate_regulatory` - Verify regulatory compliance (COPPA, FERPA, 508)
- `generate_report` - Create comprehensive compliance report

## Performance Targets

- **Validation Accuracy**: >98% correct alignment detection
- **Coverage Analysis**: Complete in <10 seconds per module
- **Gap Detection**: 100% identification of missing standards
- **Report Generation**: <30 seconds for full compliance report

## Exit Codes

- **0**: Validation complete, alignment verified
- **1**: Invalid standards framework or materials path
- **2**: Critical gaps detected, materials non-compliant
- **3**: Insufficient evidence for alignment claims

**See**: `system-prompt.md` for complete agent prompt
