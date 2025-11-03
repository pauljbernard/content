# Advanced Psychometric Analysis Enhancement

**Enhancement to**: Assessment Designer Agent (Phase 4)
**Addresses**: GAP-5 (CRITICAL)
**Purpose**: Professional psychometric validation for assessment companies

## Overview

Enhances Assessment Designer Agent with Item Response Theory (IRT), reliability analysis, validity studies, test equating, and DIF analysis. Enables assessment companies to certify products meet psychometric standards competitive with Pearson, ETS, and ACT.

## New Capabilities

### 1. Item Response Theory (IRT)

**Models Supported**:
- **1PL (Rasch)**: Item difficulty only
- **2PL**: Item difficulty + discrimination
- **3PL**: Item difficulty + discrimination + guessing

**Calibration**:
```bash
/agent.assessment-designer \
  --action "irt-calibration" \
  --response-data "item-responses.csv" \
  --model "2PL" \
  --output "item-parameters.json"
```

**Output** (per item):
```json
{
  "item_id": "item-001",
  "difficulty": 0.45,
  "discrimination": 1.23,
  "se_difficulty": 0.08,
  "se_discrimination": 0.12,
  "fit_statistics": {
    "infit": 1.02,
    "outfit": 0.98
  }
}
```

### 2. Classical Test Theory (CTT)

**Metrics**:
- **P-value**: Proportion correct (item difficulty)
- **Point-Biserial**: Item-total correlation (item discrimination)
- **Distractor Analysis**: How often each wrong answer chosen

**Example**:
```
Item 001: "What is 2 + 2?"
P-value: 0.92 (easy)
Point-Biserial: 0.45 (good discrimination)
Distractors:
  A) 3 - chosen by 3% (plausible)
  B) 4 - chosen by 92% (CORRECT)
  C) 5 - chosen by 4% (plausible)
  D) 22 - chosen by 1% (implausible - consider revising)
```

### 3. Reliability Analysis

**Coefficients**:
- **Cronbach's Alpha**: Internal consistency (0.70+ acceptable, 0.80+ good, 0.90+ excellent)
- **Split-Half**: Correlation between test halves
- **Test-Retest**: Stability over time (requires two administrations)
- **Standard Error of Measurement (SEM)**: Precision of scores

**Example**:
```
Assessment: 7th Grade Math Unit 1 Test (25 items)
Cronbach's Alpha: 0.87 (good internal consistency)
SEM: 3.2 points (95% CI: ±6.3 points)
Interpretation: True score within ±6 points of observed score
```

### 4. Validity Studies

**Types**:
- **Content Validity**: Standards alignment (already supported)
- **Construct Validity**: Factor analysis (measures intended construct)
- **Criterion Validity**: Correlation with external measure (e.g., state test)
- **Consequential Validity**: Impact on instruction and students

**Example**:
```
Construct Validity: 7th Grade Math Test
Factor Analysis: 3 factors identified (Algebra, Geometry, Statistics)
Factor loadings: Items load appropriately on intended factors
Conclusion: Test measures 3 distinct mathematical constructs as intended
```

### 5. Test Equating

**Methods**:
- **Linear Equating**: Simple linear transformation
- **Equipercentile Equating**: Match percentile ranks
- **IRT Equating**: Use IRT parameters (most accurate)

**Use Case**: Create equivalent Form B that's statistically parallel to Form A.

**Example**:
```
Form A: Mean = 75, SD = 12
Form B (raw): Mean = 78, SD = 11
Form B (equated to Form A):
  Score 80 on Form B = 77 on Form A (slightly easier)
  Score 90 on Form B = 87 on Form A
```

### 6. Differential Item Functioning (DIF)

**Purpose**: Detect bias (items that function differently for subgroups despite equal ability)

**Subgroup Comparisons**:
- Gender (male vs. female)
- Ethnicity (majority vs. underrepresented)
- Language (native vs. ELL)
- SES (low-income vs. higher-income)

**Example**:
```
Item 045: Word problem about golf
DIF Analysis: Flagged for gender bias
- Males (ability-matched): 72% correct
- Females (ability-matched): 58% correct
- Difference: 14% (moderate DIF, p < 0.001)
Recommendation: Revise or remove (golf context may favor males)
```

### 7. Test Information Functions

**Purpose**: Visualize test precision across ability range

**Output**: Chart showing where test is most/least precise
- Peak at theta = 0.5: Test best measures mid-ability students
- Low at theta = -2.0: Test poor for low-ability students
- Recommendation: Add easier items for better low-end precision

## Implementation

### Technology Stack

**Python Libraries**:
- `mirt` (via rpy2): IRT models (R library, Python wrapper)
- `factor_analyzer`: Factor analysis for construct validity
- `scipy.stats`: Correlations, t-tests
- `numpy`: Matrix operations
- `pandas`: Data manipulation

**Alternative**:
- `catsim`: Python-native IRT library (simpler but less powerful than mirt)

**Data Requirements**:
- Item responses: Student × Item matrix (1 = correct, 0 = incorrect)
- Minimum sample size: 200 students for CTT, 500+ for IRT

## CLI Interface

```bash
/agent.assessment-designer \
  --action "psychometric-analysis" \
  --response-data "responses.csv" \
  --analysis "all" \
  --report-format "technical|non-technical|certification" \
  --output "psychometric-report.pdf"
```

## Use Case Example

**Scenario**: TestCraft Pro validates 5,000-item bank before launch.

**Analysis**:
1. **IRT Calibration** (2PL model, 5,000 items, 10,000 students)
   - Difficulty range: -3.0 to +3.0 (good spread)
   - Discrimination: 0.8 to 2.5 (mostly good items)
   - 47 items flagged for low discrimination (<0.5) → review or remove

2. **Reliability** (100 sample tests, 50 items each)
   - Cronbach's Alpha: 0.88-0.93 (excellent range)
   - SEM: 2.8-3.5 points → Tests are precise

3. **DIF Analysis**
   - 23 items flagged for potential bias (gender, ethnicity, language)
   - 12 reviewed and revised, 11 removed
   - Final item bank: 4,989 items (99.8% pass rate)

4. **Certification**: Item bank certified for commercial use
   - Reliability: ✅ Exceeds 0.85 threshold
   - Validity: ✅ Strong content and construct validity
   - Fairness: ✅ DIF issues resolved
   - Precision: ✅ SEM < 4.0 points

**Result**: **CERTIFIED** - Ready for market

**Business Impact**: Certification enables sales to state departments ($8M contract potential)

## Success Criteria

- ✅ IRT calibration for 10,000+ items in <6 hours
- ✅ Reliability coefficients calculated accurately (match expert validation)
- ✅ DIF detection rate >90% (vs. expert review)
- ✅ Certification reports accepted by state procurement

---

**Status**: Ready for Phase 4 implementation (with Assessment Designer Agent)
**Dependencies**: `mirt` (R), `rpy2` (Python-R interface), large response datasets
**Testing**: Requires 500+ student responses per test for validation
**Standards**: Standards for Educational and Psychological Testing (AERA, APA, NCME)
