# Statistical Analysis Plan (SAP)
## Geometry Proofs A/B Test: Visual vs. Algebraic Approaches

**Study Title**: Comparing Visual and Algebraic Proof Instruction for Geometry Mastery
**Trial Registration**: [TBD - ClinicalTrials.gov or equivalent]
**SAP Version**: 1.0
**Date**: 2025-11-04
**Statistician**: [Name]
**Principal Investigator**: [Name]

---

## 1. Study Design Overview

### 1.1 Design Type
Randomized Controlled Trial (RCT) with two parallel groups

### 1.2 Randomization
- **Method**: Stratified randomization
- **Allocation Ratio**: 1:1 (Visual Variant : Algebraic Variant)
- **Stratification Variables**:
  - Prior math achievement (Low: <70%, Medium: 70-84%, High: ≥85%)
  - Grade level (9th, 10th)
  - English learner status (Yes/No)
  - IEP/504 status (Yes/No)
- **Randomization Tool**: Computer-generated random numbers (seed documented)

### 1.3 Sample Size
- **Target Sample**: 500 participants (250 per group)
- **Power Analysis**:
  - Target effect size: Cohen's h = 0.30 (medium)
  - Expected mastery rates: Visual 70%, Algebraic 55%
  - Alpha: 0.05 (two-tailed)
  - Power: 0.80
  - Required sample: 220 per group (440 total)
  - Buffer for attrition: 10% → 250 per group

### 1.4 Intervention Duration
30 days (approximately 12 instructional sessions)

### 1.5 Primary Outcome
**Mastery Attainment**: Dichotomous variable (Mastery = score ≥32/40 on GPMA; Non-Mastery = score <32/40)

### 1.6 Primary Hypothesis
**H₀** (Null): There is no difference in mastery rates between the Visual and Algebraic variants.
**H₁** (Alternative): There is a difference in mastery rates between the Visual and Algebraic variants.

**Directional Hypothesis** (exploratory): The Visual variant will result in higher mastery rates than the Algebraic variant.

---

## 2. Data Management

### 2.1 Data Sources
1. **Baseline Data**: Demographics, prior achievement, pre-test scores, baseline surveys
2. **Intervention Data**: Fidelity checklists, learning platform analytics, formative assessments
3. **Outcome Data**: GPMA scores, post-intervention surveys
4. **Attrition Data**: Dropout dates, reasons for withdrawal

### 2.2 Data Entry & Quality Control
- **Entry Method**: Double entry for critical variables (treatment assignment, GPMA scores)
- **Validation Rules**: Range checks, logic checks, completeness checks
- **Missing Data**: Documented with reason codes (refused, absent, technical issue, other)
- **Audit**: 10% random sample re-checked for accuracy

### 2.3 Data Storage
- **Format**: De-identified dataset in .csv and SPSS/R formats
- **Variables**: Participant ID (coded), treatment group, baseline covariates, outcomes
- **Security**: Encrypted storage; access restricted to research team

### 2.4 Codebook

| Variable Name | Type | Coding | Description |
|---------------|------|--------|-------------|
| participant_id | Numeric | 1-500 | Unique participant identifier |
| treatment | Categorical | 1=Visual, 2=Algebraic | Treatment variant |
| grade | Categorical | 1=9th, 2=10th | Grade level |
| prior_achievement | Categorical | 1=Low, 2=Med, 3=High | Prior math achievement stratum |
| el_status | Binary | 0=No, 1=Yes | English learner status |
| iep_status | Binary | 0=No, 1=Yes | IEP/504 plan status |
| baseline_pretest | Numeric | 0-30 | Baseline pre-test score |
| baseline_efficacy | Numeric | 10-50 | Baseline self-efficacy (10 items × 5-point scale) |
| baseline_interest | Numeric | 5-25 | Baseline interest in geometry (5 items × 5-point scale) |
| formative1_score | Numeric | 0-20 | Formative Assessment #1 score (Day 10) |
| formative2_score | Numeric | 0-20 | Formative Assessment #2 score (Day 20) |
| gpma_score | Numeric | 0-40 | Geometry Proof Mastery Assessment (GPMA) score |
| mastery | Binary | 0=No, 1=Yes | Mastery attainment (≥32/40 on GPMA) |
| gpma_subscale1 | Numeric | 0-12 | GPMA subscale: Basic Postulate Application |
| gpma_subscale2 | Numeric | 0-20 | GPMA subscale: Strategic Proof Construction |
| gpma_subscale3 | Numeric | 0-8 | GPMA subscale: Specialized & Transfer |
| post_efficacy | Numeric | 10-50 | Post-intervention self-efficacy |
| post_interest | Numeric | 5-25 | Post-intervention interest |
| perceived_difficulty | Numeric | 1-5 | Perceived difficulty (1=Very Easy, 5=Very Hard) |
| cognitive_load | Numeric | 6-120 | NASA-TLX adapted cognitive load (6 items × 20-point scale) |
| time_on_task | Numeric | 0-999 | Total minutes on learning platform |
| problem_completion | Numeric | 0-100 | Percentage of practice problems completed |
| fidelity_score | Numeric | 0-100 | Instructor treatment fidelity (% adherence) |
| attrition | Binary | 0=Completed, 1=Withdrew | Attrition status |
| attrition_reason | Categorical | 1=Time, 2=Disinterest, 3=Other, 9=NA | Reason for withdrawal |

---

## 3. Analysis Populations

### 3.1 Full Analysis Set (Intent-to-Treat)
**Definition**: All randomized participants, analyzed according to assigned treatment group, regardless of:
- Treatment received
- Adherence to protocol
- Withdrawal from study

**Handling of Missing Outcomes**:
- Primary analysis: Complete-case analysis (participants with GPMA scores)
- Sensitivity analysis: Multiple imputation for missing GPMA scores

**Rationale**: Preserves randomization; provides unbiased estimate of treatment effect under realistic conditions

### 3.2 Per-Protocol Set
**Definition**: Participants who:
1. Completed ≥80% of instructional sessions (≥10 of 12 sessions)
2. Received treatment with ≥70% fidelity (instructor adherence ≥70%)
3. Completed GPMA assessment

**Rationale**: Estimates treatment effect under ideal conditions (treatment delivered as intended)

### 3.3 Safety Set
**Definition**: All participants who received at least one instructional session

**Purpose**: Monitor adverse outcomes (extreme frustration, dropout due to intervention)

---

## 4. Primary Analysis

### 4.1 Research Question
Does the Visual proof variant result in a different mastery rate compared to the Algebraic proof variant?

### 4.2 Statistical Test
**Chi-Square Test of Independence** (2×2 contingency table)

**Null Hypothesis**: Mastery rate is independent of treatment variant
**Alternative Hypothesis**: Mastery rate differs by treatment variant

**Significance Level**: α = 0.05 (two-tailed)

**Test Statistic**: χ² with 1 degree of freedom

**Software**: R (chisq.test function) or SPSS (Crosstabs)

### 4.3 Contingency Table Structure

|                | Mastery | Non-Mastery | Total |
|----------------|---------|-------------|-------|
| Visual Variant | a       | b           | n₁    |
| Algebraic Variant | c    | d           | n₂    |
| **Total**      | m₁      | m₂          | N     |

### 4.4 Effect Size Measures

#### 4.4.1 Relative Risk (RR)
```
RR = (a/n₁) / (c/n₂)
```
Interpretation:
- RR = 1: No difference in mastery rates
- RR > 1: Visual variant has higher mastery rate
- RR < 1: Algebraic variant has higher mastery rate

**95% Confidence Interval** (log method):
```
log(RR) ± 1.96 × SE[log(RR)]
where SE[log(RR)] = sqrt(1/a - 1/n₁ + 1/c - 1/n₂)
```

#### 4.4.2 Risk Difference (RD)
```
RD = (a/n₁) - (c/n₂)
```
Interpretation: Absolute difference in mastery rates (expressed as percentage points)

**95% CI**:
```
RD ± 1.96 × SE(RD)
where SE(RD) = sqrt[(p₁(1-p₁)/n₁) + (p₂(1-p₂)/n₂)]
```

#### 4.4.3 Number Needed to Treat (NNT)
```
NNT = 1 / RD
```
Interpretation: Number of students who need to receive Visual variant (vs. Algebraic) for one additional student to achieve mastery

#### 4.4.4 Odds Ratio (OR)
```
OR = (a×d) / (b×c)
```
Interpretation: Odds of mastery in Visual variant compared to Algebraic variant

**95% CI** (log method):
```
log(OR) ± 1.96 × SE[log(OR)]
where SE[log(OR)] = sqrt(1/a + 1/b + 1/c + 1/d)
```

#### 4.4.5 Cohen's h
```
h = 2 × [arcsin(sqrt(p₁)) - arcsin(sqrt(p₂))]
```
Interpretation: Standardized effect size for proportions
- Small: h = 0.20
- Medium: h = 0.50
- Large: h = 0.80

### 4.5 Assumptions & Diagnostics

**Assumptions**:
1. Independent observations (no clustering; if clustering exists, use multilevel model)
2. Expected cell frequencies ≥5 in each cell

**Diagnostic Checks**:
- Check expected frequencies: E(cell) = (row total × column total) / N
- If any E(cell) < 5: Use Fisher's Exact Test instead of chi-square

### 4.6 Reporting

**Results Statement Template**:
```
The mastery rate was [X]% ([a]/[n₁]) in the Visual variant and [Y]% ([c]/[n₂]) in the
Algebraic variant. A chi-square test of independence revealed [a statistically
significant difference / no statistically significant difference], χ²(1) = [value],
p = [p-value]. The relative risk was [RR] (95% CI: [LL, UL]), indicating that students
in the Visual variant were [RR] times as likely to achieve mastery compared to the
Algebraic variant. The absolute difference in mastery rates was [RD]% (95% CI: [LL, UL]),
corresponding to a number needed to treat of [NNT]. The effect size was Cohen's h = [h],
indicating a [small/medium/large] effect.
```

---

## 5. Secondary Analyses

### 5.1 Logistic Regression (Adjusted Analysis)

**Purpose**: Estimate treatment effect while adjusting for baseline covariates

**Model**:
```
logit(P(Mastery = 1)) = β₀ + β₁(Treatment) + β₂(Baseline_Pretest) + β₃(Grade) +
                         β₄(EL_Status) + β₅(IEP_Status)
```

**Variables**:
- **Outcome**: Mastery (0/1)
- **Primary Predictor**: Treatment (Visual=1, Algebraic=0)
- **Covariates**:
  - Baseline pre-test score (continuous)
  - Grade level (9th=0, 10th=1)
  - English learner status (No=0, Yes=1)
  - IEP/504 status (No=0, Yes=1)

**Interpretation**:
- **β₁**: Log-odds of mastery in Visual vs. Algebraic (adjusted for covariates)
- **exp(β₁)**: Adjusted odds ratio (AOR)
- **p-value for β₁**: Test of treatment effect (adjusted)

**Reporting**:
```
After adjusting for baseline pre-test score, grade level, English learner status, and
IEP status, students in the Visual variant had [AOR] times the odds of achieving mastery
compared to the Algebraic variant (95% CI: [LL, UL], p = [p-value]).
```

**Software**: R (glm function with family=binomial) or SPSS (Binary Logistic Regression)

---

### 5.2 Proof Quality Score (Continuous Outcome)

**Research Question**: Does the Visual variant result in higher proof quality scores?

**Outcome**: GPMA total score (0-40, continuous)

**Statistical Test**:
1. **Normality Check**: Shapiro-Wilk test; Q-Q plots
   - If normally distributed: Independent samples t-test
   - If non-normally distributed: Mann-Whitney U test

#### 5.2.1 Independent Samples t-Test (if normal)

**Null Hypothesis**: Mean GPMA score is equal across variants
**Alternative Hypothesis**: Mean GPMA score differs across variants

**Test Statistic**:
```
t = (M₁ - M₂) / sqrt[(s₁²/n₁) + (s₂²/n₂)]
```

**Assumptions**:
- Normality (checked via Shapiro-Wilk)
- Homogeneity of variance (Levene's test; if violated, use Welch's t-test)

**Effect Size**: Cohen's d
```
d = (M₁ - M₂) / pooled_SD
```

**95% CI for Mean Difference**:
```
(M₁ - M₂) ± t_critical × SE(M₁ - M₂)
```

**Reporting**:
```
The Visual variant had a mean GPMA score of M = [M₁] (SD = [s₁]), while the Algebraic
variant had M = [M₂] (SD = [s₂]). An independent samples t-test revealed [a statistically
significant difference / no statistically significant difference], t([df]) = [t-value],
p = [p-value], Cohen's d = [d], indicating a [small/medium/large] effect.
```

#### 5.2.2 Mann-Whitney U Test (if non-normal)

**Null Hypothesis**: Distributions of GPMA scores are identical across variants
**Alternative Hypothesis**: Distributions differ

**Test Statistic**: U (sum of ranks)

**Effect Size**: Rank-biserial correlation or η² (eta-squared)

**Reporting**:
```
Median GPMA scores were [Mdn₁] for the Visual variant and [Mdn₂] for the Algebraic
variant. A Mann-Whitney U test indicated [a statistically significant difference /
no statistically significant difference], U = [U-value], p = [p-value].
```

---

### 5.3 Subscale Analyses

**Purpose**: Identify which aspects of proof construction differ by variant

**Subscales**:
1. **Basic Postulate Application** (Items 1-3, max 12 points)
2. **Strategic Proof Construction** (Items 4-8, max 20 points)
3. **Specialized & Transfer** (Items 9-10, max 8 points)

**Analysis**: Independent t-tests (or Mann-Whitney U) for each subscale

**Multiple Comparisons Adjustment**: Bonferroni correction (α = 0.05 / 3 = 0.0167)

**Reporting**: Report mean (SD), test statistic, p-value, and effect size for each subscale

---

### 5.4 Engagement Metrics

**Research Question**: Does engagement differ by variant?

**Metrics**:
1. **Time on Task**: Total minutes on learning platform
2. **Problem Completion Rate**: Percentage of practice problems completed (0-100%)
3. **Help-Seeking**: Number of help requests or hints used

**Analysis**: Independent t-tests or Mann-Whitney U tests (depending on normality)

**Interpretation**: Assess whether higher mastery is associated with greater engagement or efficiency

---

### 5.5 Affective Outcomes

**Research Question**: Do self-efficacy, interest, perceived difficulty, and cognitive load differ by variant?

**Outcomes**:
1. **Self-Efficacy**: Post-intervention score (controlling for baseline)
2. **Interest**: Post-intervention score (controlling for baseline)
3. **Perceived Difficulty**: Post-intervention rating (1-5 scale)
4. **Cognitive Load**: NASA-TLX adapted score (6-120 scale)

**Analysis**:
- **Self-Efficacy & Interest**: ANCOVA (post-test as outcome, baseline as covariate, treatment as factor)
- **Perceived Difficulty & Cognitive Load**: Independent t-tests or Mann-Whitney U

**Reporting**: Report adjusted means (for ANCOVA) or raw means (for t-tests), test statistics, p-values, effect sizes

---

### 5.6 Subgroup Analyses (Exploratory)

**Purpose**: Identify differential treatment effects by subgroup

**Subgroups**:
1. Prior achievement level (Low vs. Medium vs. High)
2. Grade level (9th vs. 10th)
3. English learner status (Yes vs. No)
4. IEP/504 status (Yes vs. No)

**Analysis**: Logistic regression with treatment × subgroup interaction term

**Model Example** (for prior achievement):
```
logit(P(Mastery)) = β₀ + β₁(Treatment) + β₂(Achievement) + β₃(Treatment × Achievement)
```

**Interpretation**:
- **β₃**: Interaction effect (does treatment effect vary by achievement level?)
- If β₃ is significant (p < .05): Treatment effect differs across achievement levels
- If β₃ is non-significant: Treatment effect is consistent across levels

**Forest Plot**: Display treatment effects (OR or RR) for each subgroup with 95% CIs

**Caution**: Subgroup analyses are exploratory and may be underpowered; interpret with caution

---

## 6. Missing Data Analysis

### 6.1 Patterns of Missingness

**Analysis**:
1. Calculate missingness rate for each variable
2. Compare baseline characteristics of completers vs. non-completers (t-tests, chi-square)
3. Assess whether missingness is related to treatment assignment

**Classification**:
- **MCAR** (Missing Completely At Random): Missingness unrelated to any variables
- **MAR** (Missing At Random): Missingness related to observed variables
- **MNAR** (Missing Not At Random): Missingness related to unobserved variables

### 6.2 Primary Analysis Approach

**Complete-Case Analysis**: Analyze only participants with GPMA scores

**Assumptions**: Assumes data are MCAR or MAR (conditional on covariates in model)

### 6.3 Sensitivity Analyses

#### 6.3.1 Multiple Imputation (MI)

**Purpose**: Account for uncertainty due to missing data

**Procedure**:
1. Generate m=20 imputed datasets using chained equations (MICE algorithm)
2. Impute missing GPMA scores based on:
   - Treatment assignment
   - Baseline pre-test, self-efficacy, interest
   - Formative assessment scores (if available)
   - Demographics (grade, EL status, IEP status)
3. Perform primary analysis on each imputed dataset
4. Pool results using Rubin's rules

**Software**: R (mice package) or SPSS (Multiple Imputation module)

**Reporting**:
```
Multiple imputation was conducted to address missing outcome data (n = [#] missing).
Twenty imputed datasets were generated using predictive mean matching based on treatment
assignment, baseline covariates, and formative assessments. The pooled estimate of the
treatment effect was [OR/RR] (95% CI: [LL, UL], p = [p-value]).
```

#### 6.3.2 Best-Case / Worst-Case Scenarios

**Best-Case** (favoring Visual variant):
- All missing GPMA scores in Visual group → Mastery
- All missing GPMA scores in Algebraic group → Non-Mastery

**Worst-Case** (favoring Algebraic variant):
- All missing GPMA scores in Visual group → Non-Mastery
- All missing GPMA scores in Algebraic group → Mastery

**Purpose**: Assess robustness of findings under extreme assumptions

**Reporting**: If treatment effect remains significant in both scenarios, findings are robust to missing data

---

## 7. Attrition Analysis

### 7.1 Attrition Rate

**Calculation**:
```
Attrition Rate (%) = (Number of Withdrawals / Number Enrolled) × 100
```

**Benchmark**: <20% attrition is acceptable for educational RCTs

### 7.2 Differential Attrition

**Analysis**: Compare attrition rates between treatment groups using chi-square test

**Null Hypothesis**: Attrition rate is independent of treatment variant

**Reporting**:
```
Attrition was [X]% in the Visual variant and [Y]% in the Algebraic variant. A chi-square
test revealed [no significant difference / a significant difference], χ²(1) = [value],
p = [p-value].
```

**Concern**: If differential attrition exists, it may introduce bias (e.g., if struggling students disproportionately drop from one variant)

### 7.3 Attrition Bias Assessment

**Analysis**: Compare baseline characteristics of completers vs. non-completers

**Variables**: Prior achievement, baseline self-efficacy, demographics

**Test**: t-tests (continuous) or chi-square (categorical)

**Interpretation**: If non-completers differ systematically from completers, results may not generalize

---

## 8. Treatment Fidelity Analysis

### 8.1 Fidelity Score Calculation

**Method**: Average percentage of checklist items completed across all sessions for each instructor

**Formula**:
```
Fidelity Score (%) = (Sum of Completed Items / Total Items Across Sessions) × 100
```

**Threshold**: ≥80% considered acceptable fidelity

### 8.2 Fidelity and Outcomes

**Analysis**: Correlation or regression of fidelity score with mastery rate

**Research Question**: Is higher fidelity associated with better outcomes?

**Model**:
```
logit(P(Mastery)) = β₀ + β₁(Fidelity_Score)
```

**Interpretation**: β₁ indicates whether adherence to protocol predicts mastery

### 8.3 Per-Protocol Analysis

**Purpose**: Estimate treatment effect among participants who received high-fidelity intervention

**Inclusion Criteria**:
- Instructor fidelity ≥70%
- Student attendance ≥80% (≥10 of 12 sessions)
- Completed GPMA

**Analysis**: Repeat primary analysis (chi-square, effect sizes) for per-protocol set

**Reporting**: Compare intent-to-treat and per-protocol results

---

## 9. Interim Analysis

### 9.1 Timing
Day 15 (midpoint of intervention)

### 9.2 Purpose
- Monitor for extreme outcomes (futility or clear superiority)
- Assess safety (attrition, adverse events)
- Check assumptions (balance, fidelity)

### 9.3 Alpha Spending

**Method**: Lan-DeMets alpha spending function (O'Brien-Fleming boundary)

**Adjustment**: Controls Type I error rate when conducting interim analysis

**Critical p-value at Interim**: p < 0.005 (more stringent than final p < 0.05)

**Critical p-value at Final**: Adjusted based on alpha spending (approximately p < 0.048)

**Software**: R (gsDesign package) or East software

### 9.4 Decision Rules

**Stop for Efficacy** (early termination, deploy winner):
- Statistically significant difference at p < 0.005 (interim alpha)
- Effect size (h) > 0.80 (very large)
- No safety concerns

**Stop for Futility**:
- Conditional power <10% (probability of detecting effect at final analysis is very low)
- Treatment groups nearly identical (h < 0.10)

**Continue as Planned**:
- p > 0.005 or moderate effect size (0.20 < h < 0.80)
- No safety concerns

**Reporting**: Document interim analysis, decision, and rationale in final report

---

## 10. Reporting & Presentation

### 10.1 CONSORT Diagram

**Flow Chart** (participants through each stage):

```
Assessed for Eligibility (n = [X])
    |
    ├─ Excluded (n = [Y])
    │   ├─ Did not meet criteria (n = [#])
    │   ├─ Declined participation (n = [#])
    │   └─ Other reasons (n = [#])
    |
Randomized (n = 500)
    |
    ├─────────────────────────────┬─────────────────────────────┐
    |                             |                             |
Allocated to Visual (n=250)   Allocated to Algebraic (n=250)
    |                             |
Received Visual (n = [#])     Received Algebraic (n = [#])
Did not receive (n = [#])     Did not receive (n = [#])
    |                             |
Lost to follow-up (n = [#])   Lost to follow-up (n = [#])
Discontinued (n = [#])        Discontinued (n = [#])
    |                             |
Analyzed (n = [#])            Analyzed (n = [#])
Excluded from analysis (n=[#]) Excluded from analysis (n=[#])
```

### 10.2 Baseline Characteristics Table

**Table 1: Baseline Characteristics by Treatment Group**

| Characteristic | Visual (n=250) | Algebraic (n=250) | p-value |
|----------------|----------------|-------------------|---------|
| **Demographics** |              |                   |         |
| Grade 9, n (%) | [#] ([%]%)     | [#] ([%]%)        | [p]     |
| Grade 10, n (%) | [#] ([%]%)    | [#] ([%]%)        | [p]     |
| English Learner, n (%) | [#] ([%]%) | [#] ([%]%)    | [p]     |
| IEP/504, n (%) | [#] ([%]%)     | [#] ([%]%)        | [p]     |
| **Prior Achievement** |          |                   |         |
| Low, n (%)     | [#] ([%]%)     | [#] ([%]%)        | [p]     |
| Medium, n (%)  | [#] ([%]%)     | [#] ([%]%)        | [p]     |
| High, n (%)    | [#] ([%]%)     | [#] ([%]%)        | [p]     |
| **Baseline Measures** |          |                   |         |
| Pre-test, M (SD) | [M] ([SD])   | [M] ([SD])        | [p]     |
| Self-efficacy, M (SD) | [M] ([SD]) | [M] ([SD])      | [p]     |
| Interest, M (SD) | [M] ([SD])   | [M] ([SD])        | [p]     |

*Note: p-values from chi-square tests (categorical) or t-tests (continuous)*

### 10.3 Primary Outcome Table

**Table 2: Primary Outcome (Mastery Attainment)**

| Outcome | Visual (n=250) | Algebraic (n=250) | Effect Size | 95% CI | p-value |
|---------|----------------|-------------------|-------------|--------|---------|
| Mastery, n (%) | [a] ([%]%) | [c] ([%]%)     | RR = [RR]   | [LL, UL] | [p]   |
|                |            |                   | RD = [RD]%  | [LL, UL] |       |
|                |            |                   | OR = [OR]   | [LL, UL] |       |
|                |            |                   | h = [h]     | -        |       |
|                |            |                   | NNT = [NNT] | -        |       |

*Note: RR = Relative Risk, RD = Risk Difference, OR = Odds Ratio, h = Cohen's h, NNT = Number Needed to Treat*

### 10.4 Secondary Outcomes Table

**Table 3: Secondary Outcomes**

| Outcome | Visual M (SD) or % | Algebraic M (SD) or % | Test Statistic | p-value | Effect Size |
|---------|--------------------|-----------------------|----------------|---------|-------------|
| **GPMA Total Score** | [M] ([SD])    | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |
| Basic Postulate    | [M] ([SD])    | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |
| Strategic Proof    | [M] ([SD])    | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |
| Transfer           | [M] ([SD])    | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |
| **Engagement**     |               |                       |                |         |             |
| Time on Task (min) | [M] ([SD])    | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |
| Completion Rate (%)| [M] ([SD])    | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |
| **Affective**      |               |                       |                |         |             |
| Post Self-Efficacy | [M] ([SD])    | [M] ([SD])            | F(1,[df]) = [F]| [p]     | η² = [η²]   |
| Post Interest      | [M] ([SD])    | [M] ([SD])            | F(1,[df]) = [F]| [p]     | η² = [η²]   |
| Perceived Difficulty| [M] ([SD])   | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |
| Cognitive Load     | [M] ([SD])    | [M] ([SD])            | t([df]) = [t]  | [p]     | d = [d]     |

---

## 11. Software & Reproducibility

### 11.1 Statistical Software
- **Primary**: R (version ≥4.0) with packages: base, stats, lme4, mice, ggplot2
- **Alternative**: SPSS (version ≥27) or SAS (version ≥9.4)

### 11.2 Reproducibility
- **Analysis Scripts**: All R code saved in version-controlled repository (GitHub or OSF)
- **Random Seed**: Document seed used for randomization and imputation
- **Data Availability**: De-identified dataset archived in public repository (OSF, ICPSR) upon publication

### 11.3 Code Availability
- R scripts for primary and secondary analyses provided as supplementary materials
- Annotated code with comments explaining each step

---

## 12. Deviations from SAP

**Protocol**: Any deviations from this SAP must be documented with rationale

**Examples of Acceptable Deviations**:
- Change in statistical test due to violated assumptions (e.g., use Mann-Whitney U instead of t-test if non-normal)
- Additional exploratory analyses requested by reviewers

**Documentation**: Maintain deviation log with date, reason, and approval

---

## 13. Summary Checklist

**Before Analysis**:
- [ ] Data cleaning complete (missing data documented, outliers reviewed)
- [ ] Data quality checks passed (10% audit, validation rules)
- [ ] Randomization balance verified (no significant baseline differences)
- [ ] Treatment fidelity calculated (≥80% achieved)
- [ ] Attrition documented (rates and reasons)

**Primary Analysis**:
- [ ] Chi-square test conducted (intent-to-treat)
- [ ] Effect sizes calculated (RR, RD, OR, h, NNT)
- [ ] 95% CIs reported for all effect sizes
- [ ] Assumptions checked (expected cell frequencies ≥5)
- [ ] Results interpreted and summarized

**Secondary Analyses**:
- [ ] Logistic regression (adjusted analysis) conducted
- [ ] Continuous outcomes analyzed (t-tests or Mann-Whitney U)
- [ ] Subscale analyses conducted (with Bonferroni correction)
- [ ] Engagement metrics compared
- [ ] Affective outcomes analyzed (ANCOVA for self-efficacy and interest)
- [ ] Subgroup analyses conducted (with caution regarding power)

**Missing Data & Sensitivity**:
- [ ] Missingness patterns described
- [ ] Complete-case analysis conducted
- [ ] Multiple imputation conducted (20 datasets)
- [ ] Best-case/worst-case scenarios analyzed
- [ ] Results compared across methods

**Reporting**:
- [ ] CONSORT diagram created
- [ ] Baseline characteristics table completed
- [ ] Primary outcome table completed
- [ ] Secondary outcomes table completed
- [ ] Forest plots for subgroup analyses (if applicable)
- [ ] Statistical analysis report drafted

---

**SAP Status**: FINAL (locked before data analysis)
**Approval Date**: [TBD - before interim analysis]
**Approved by**: Principal Investigator, Statistician, IRB (if required)

---

## References

1. Schulz, K. F., Altman, D. G., & Moher, D. (2010). CONSORT 2010 statement: Updated guidelines for reporting parallel group randomised trials. *BMJ*, 340, c332.

2. Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

3. Little, R. J. A., & Rubin, D. B. (2002). *Statistical analysis with missing data* (2nd ed.). Wiley.

4. Van Buuren, S., & Groothuis-Oudshoorn, K. (2011). mice: Multivariate imputation by chained equations in R. *Journal of Statistical Software*, 45(3), 1-67.

5. Lan, K. K. G., & DeMets, D. L. (1983). Discrete sequential boundaries for clinical trials. *Biometrika*, 70(3), 659-663.
