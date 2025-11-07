# Statistics Guide (High School)
**Course Level:** Typically Grade 11-12 (alternative to or alongside Calculus)
**Prerequisites:** Algebra II (Algebra I and Geometry minimum)
**Applies To:** All high school Statistics materials, including AP Statistics

---

## Overview

Statistics is the science of collecting, analyzing, interpreting, and presenting data. It develops data literacy, statistical reasoning, and the ability to make data-driven decisions—essential skills in the modern world. AP Statistics is a rigorous college-level course and a popular alternative to AP Calculus for students pursuing non-STEM fields or as a complement to Calculus for STEM students.

**College/Career Readiness:** Statistics is increasingly required or recommended for business, social sciences, healthcare, psychology, economics, and data-driven careers. AP Statistics credit can fulfill quantitative reasoning requirements at many colleges.

**Why Statistics Matters:**
- Data is everywhere (business, politics, healthcare, sports, social media)
- Critical thinking about data and claims
- Essential for informed citizenship (understanding polls, studies, news)
- Foundation for data science, machine learning, and AI

**AP Statistics:** College-level introductory statistics course, equivalent to a one-semester college statistics course.

---

## Core Learning Objectives

Students will be able to:

1. **Exploring Data** - Analyze and display univariate and bivariate data, describe distributions
2. **Sampling and Experimentation** - Design studies, understand sampling methods, identify bias
3. **Probability** - Understand probability rules, random variables, and probability distributions
4. **Statistical Inference** - Estimate population parameters and test hypotheses using sample data
5. **Data Analysis in Context** - Interpret statistical results, communicate findings, identify limitations
6. **Critical Evaluation** - Critique statistical claims, identify misuse of statistics, question conclusions

---

## Key Mathematical Concepts

### 1. Exploring Data: Describing Patterns and Departures from Patterns (20-30% of AP Exam)

#### Univariate Data (One Variable)

**Categorical Data:**
- Frequency tables and relative frequency
- Bar charts and pie charts
- Two-way tables (contingency tables)

**Quantitative Data:**
- Dotplots, stemplots (stem-and-leaf), histograms, boxplots
- Shape (symmetric, skewed left/right, uniform, bimodal)
- Center (mean, median, mode)
- Spread (range, IQR, standard deviation, variance)
- Outliers (1.5 × IQR rule, unusual values)
- **SOCS:** Shape, Outliers, Center, Spread (describe distributions)

**Measures of Center:**
- Mean (x̄): average, sensitive to outliers
- Median: middle value, resistant to outliers
- Mode: most frequent value

**Measures of Spread:**
- Range: max - min
- Interquartile Range (IQR): Q3 - Q1
- Standard Deviation (s): typical distance from mean
- Variance (s²): average squared deviation

**Comparing Distributions:**
- Compare shape, center, and spread
- Use parallel boxplots or back-to-back stemplots
- Always compare in context

---

#### Bivariate Data (Two Variables)

**Scatterplots:**
- Display relationship between two quantitative variables
- Direction (positive, negative, no association)
- Form (linear, curved, clusters)
- Strength (strong, moderate, weak)
- Outliers and influential points

**Correlation (r):**
- Measures strength and direction of LINEAR relationship
- Range: -1 ≤ r ≤ 1
- r near +1: strong positive linear relationship
- r near -1: strong negative linear relationship
- r near 0: weak or no linear relationship
- **Limitations:** Only measures LINEAR association, sensitive to outliers, correlation ≠ causation

**Least-Squares Regression Line (LSRL):**
- ŷ = a + bx (predicted y, y-intercept, slope, x)
- Slope (b): for each 1-unit increase in x, ŷ increases by b units
- Interpret slope and y-intercept IN CONTEXT
- Residual = observed - predicted = y - ŷ
- Residual plot (check linearity assumption)
- Coefficient of determination (r²): proportion of variation in y explained by x

**Outliers and Influential Points:**
- Outlier: unusual y-value given x (large residual)
- Influential point: if removed, changes regression line substantially (usually extreme x-value)

**Transformations:**
- Log, exponential transformations to linearize curved relationships
- Residual plots to assess fit

**Categorical Bivariate Data:**
- Two-way tables
- Marginal and conditional distributions
- Association between categorical variables

---

**Real-World Applications:**
- Economics (relationship between variables)
- Healthcare (risk factors and outcomes)
- Social Sciences (correlations between behaviors)
- Sports Analytics (performance metrics)
- Market Research (consumer behavior)

**Career Connections:**
- Data Science: Exploratory data analysis (EDA)
- Business Analytics: Descriptive statistics, trend identification
- Public Health: Identifying health trends and risk factors
- Social Sciences: Survey data analysis

---

### 2. Sampling and Experimentation: Planning and Conducting a Study (10-15% of AP Exam)

#### Study Design

**Observational Study:**
- Observe and measure without intervention
- Cannot establish causation (only association)
- Examples: Surveys, polls, observational medical studies

**Experiment:**
- Impose treatments and measure responses
- CAN establish causation (with good design)
- Random assignment to treatment groups (key!)
- Control group vs. treatment group
- Examples: Drug trials, A/B testing, agricultural experiments

---

#### Sampling Methods

**Simple Random Sample (SRS):**
- Every individual has equal chance of selection
- Gold standard for sampling

**Stratified Random Sample:**
- Divide population into strata (groups)
- Take SRS from each stratum
- Ensures representation of subgroups

**Cluster Sample:**
- Divide population into clusters (groups)
- Randomly select clusters, include all individuals in selected clusters

**Systematic Sample:**
- Select every kth individual from list

**Convenience Sample:**
- Choose individuals easy to reach
- **BIASED** - not random, not representative

---

#### Sources of Bias

**Sampling Bias:**
- Undercoverage: Some groups not represented in sample
- Voluntary response bias: Only those who feel strongly respond
- Convenience sampling bias: Sample not representative

**Response Bias:**
- Wording of questions (leading, confusing)
- Interviewer effect
- Social desirability bias (respondents answer what sounds good)

**Nonresponse Bias:**
- Individuals selected don't respond
- Respondents may differ from nonrespondents

---

#### Experimental Design Principles

**Control:**
- Control extraneous variables
- Use control group (no treatment or placebo)

**Randomization:**
- Random assignment to treatment groups
- Balances confounding variables

**Replication:**
- Sufficient sample size
- Repeat experiment to verify results

**Blocking:**
- Group similar individuals into blocks
- Randomize within blocks
- Reduces variability

**Blinding:**
- Single-blind: subjects don't know which treatment they receive
- Double-blind: subjects AND evaluators don't know
- Reduces bias

**Placebo Effect:**
- Subjects improve because they THINK they're receiving treatment
- Control with placebo group

---

**Real-World Applications:**
- Clinical trials (medical research)
- A/B testing (web design, marketing)
- Agricultural experiments (crop yields)
- Educational research (teaching methods)
- Quality control (manufacturing)

**Career Connections:**
- Healthcare: Clinical trial design
- Marketing: A/B testing, market research
- Public Policy: Survey design, program evaluation
- Quality Assurance: Experimental design for improvement

---

### 3. Probability (20-30% of AP Exam)

#### Probability Basics

**Definitions:**
- Probability: P(A) = (number of outcomes in A) / (total number of outcomes)
- Range: 0 ≤ P(A) ≤ 1
- Law of Large Numbers: As trials increase, empirical probability → theoretical probability

**Probability Rules:**
- Complement Rule: P(not A) = 1 - P(A)
- Addition Rule (Mutually Exclusive): P(A or B) = P(A) + P(B)
- Addition Rule (General): P(A or B) = P(A) + P(B) - P(A and B)
- Multiplication Rule (Independent): P(A and B) = P(A) × P(B)
- Multiplication Rule (General): P(A and B) = P(A) × P(B|A)

**Conditional Probability:**
- P(A|B) = P(A and B) / P(B)
- Probability of A GIVEN B has occurred

**Independence:**
- A and B are independent if P(A|B) = P(A)
- OR if P(A and B) = P(A) × P(B)

**Two-Way Tables and Tree Diagrams:**
- Organize conditional probabilities
- Visualize probability calculations

---

#### Random Variables

**Discrete Random Variable:**
- Takes on countable values (0, 1, 2, ...)
- Probability distribution: P(X = x) for all possible x
- Mean (Expected Value): μ = E(X) = Σ[x × P(X = x)]
- Variance: σ² = Σ[(x - μ)² × P(X = x)]
- Standard Deviation: σ = √σ²

**Continuous Random Variable:**
- Takes on any value in interval (usually modeled with normal distribution)

---

#### Probability Distributions

**Binomial Distribution:**
- Fixed number of trials (n)
- Two outcomes (success or failure)
- Constant probability of success (p)
- Independent trials
- **BINS:** Binary outcomes, Independent trials, Number of trials fixed, Same probability
- P(X = k) = C(n,k) × p^k × (1-p)^(n-k)
- Mean: μ = np
- Standard Deviation: σ = √[np(1-p)]

**Geometric Distribution:**
- Probability of first success on trial X = k
- P(X = k) = (1-p)^(k-1) × p
- Mean: μ = 1/p

**Normal Distribution:**
- Continuous, bell-shaped, symmetric
- Defined by mean (μ) and standard deviation (σ)
- Notation: N(μ, σ)
- Empirical Rule (68-95-99.7 Rule):
  - 68% within 1 standard deviation
  - 95% within 2 standard deviations
  - 99.7% within 3 standard deviations
- Standard Normal Distribution: N(0, 1) (z-scores)
- z = (x - μ) / σ
- Use z-table or calculator to find probabilities

**Normal Probability Plots:**
- Assess whether data is approximately normal
- If points follow straight line, data is approximately normal

---

**Real-World Applications:**
- Quality Control (binomial: defect rate)
- Insurance (probability of claims)
- Finance (risk assessment)
- Games of chance (lottery, gambling - be skeptical!)

**Career Connections:**
- Actuarial Science: Risk assessment
- Finance: Portfolio risk, option pricing
- Healthcare: Diagnostic testing (sensitivity, specificity)
- Data Science: Probability modeling, Bayesian inference

---

### 4. Statistical Inference: Estimating Population Parameters and Testing Claims (30-40% of AP Exam)

#### Sampling Distributions

**Sampling Distribution of Sample Mean (x̄):**
- Distribution of ALL possible sample means from samples of size n
- Center: μ_x̄ = μ (unbiased)
- Spread: σ_x̄ = σ/√n (standard error)
- **Central Limit Theorem (CLT):** For large n (n ≥ 30), sampling distribution of x̄ is approximately normal, REGARDLESS of population distribution

**Sampling Distribution of Sample Proportion (p̂):**
- Distribution of ALL possible sample proportions from samples of size n
- Center: μ_p̂ = p (unbiased)
- Spread: σ_p̂ = √[p(1-p)/n] (standard error)
- **Normal Approximation:** If np ≥ 10 and n(1-p) ≥ 10, then p̂ is approximately normal

---

#### Confidence Intervals (Estimation)

**Concept:**
- Use sample statistic to estimate population parameter
- Interval estimate with confidence level (90%, 95%, 99%)
- Interpretation: "We are 95% confident that the true population parameter is in this interval"
- **NOT:** "There is a 95% probability the parameter is in this interval" (parameter is fixed, not random!)

**One-Sample z-Interval for Population Mean μ (σ known):**
- x̄ ± z* × (σ/√n)
- Conditions: Random sample, normal population OR large n (CLT)

**One-Sample t-Interval for Population Mean μ (σ unknown):**
- x̄ ± t* × (s/√n)
- Use t-distribution with df = n - 1
- Conditions: Random sample, normal population OR large n

**One-Sample z-Interval for Population Proportion p:**
- p̂ ± z* × √[p̂(1-p̂)/n]
- Conditions: Random sample, np̂ ≥ 10, n(1-p̂) ≥ 10

**Two-Sample t-Interval for Difference in Means (μ₁ - μ₂):**
- (x̄₁ - x̄₂) ± t* × SE
- Conditions: Independent random samples, normal populations OR large n for both

**Two-Sample z-Interval for Difference in Proportions (p₁ - p₂):**
- (p̂₁ - p̂₂) ± z* × SE
- Conditions: Independent random samples, success-failure condition for both

**Paired t-Interval for Mean Difference (μ_diff):**
- x̄_diff ± t* × (s_diff/√n)
- Use when data is paired (before/after, matched pairs)

---

**Factors Affecting Confidence Interval Width:**
- Higher confidence level → wider interval
- Larger sample size → narrower interval
- Greater variability (σ or s) → wider interval

---

#### Hypothesis Testing (Significance Tests)

**Concept:**
- Test a claim about a population parameter
- Null hypothesis (H₀): Claim of no effect, no difference, status quo
- Alternative hypothesis (Hₐ): Claim we're testing (what we suspect is true)

**Steps:**
1. State hypotheses (H₀ and Hₐ)
2. Check conditions (random, normal, independence)
3. Calculate test statistic (z or t)
4. Find p-value (probability of observing this data if H₀ is true)
5. Make decision: If p-value < α, reject H₀; otherwise, fail to reject H₀
6. State conclusion IN CONTEXT

**P-Value:**
- Probability of observing sample result (or more extreme) if H₀ is true
- Small p-value (< α): evidence AGAINST H₀ → reject H₀
- Large p-value (≥ α): insufficient evidence against H₀ → fail to reject H₀

**Significance Level (α):**
- Threshold for decision (commonly α = 0.05)
- P(Type I Error) = α

**Types of Errors:**
- **Type I Error:** Reject H₀ when H₀ is true (false positive)
- **Type II Error:** Fail to reject H₀ when Hₐ is true (false negative)
- Power: P(Reject H₀ | Hₐ is true) = 1 - P(Type II Error)

---

**Significance Tests:**

**One-Sample z-Test for Mean μ (σ known):**
- z = (x̄ - μ₀) / (σ/√n)

**One-Sample t-Test for Mean μ (σ unknown):**
- t = (x̄ - μ₀) / (s/√n)
- df = n - 1

**One-Sample z-Test for Proportion p:**
- z = (p̂ - p₀) / √[p₀(1-p₀)/n]

**Two-Sample t-Test for Difference in Means:**
- Test H₀: μ₁ = μ₂

**Two-Sample z-Test for Difference in Proportions:**
- Test H₀: p₁ = p₂

**Paired t-Test for Mean Difference:**
- Test H₀: μ_diff = 0 (no difference)

**Chi-Square Test for Goodness of Fit:**
- Test if categorical data fits expected distribution
- χ² = Σ[(observed - expected)² / expected]
- df = (number of categories) - 1

**Chi-Square Test for Independence (Homogeneity):**
- Test if two categorical variables are independent
- df = (rows - 1) × (columns - 1)

---

**Real-World Applications:**
- Clinical Trials (is drug effective?)
- A/B Testing (which website design performs better?)
- Quality Control (is defect rate acceptable?)
- Social Science Research (do groups differ?)
- Legal/Forensic (evidence evaluation)

**Career Connections:**
- Data Science: A/B testing, hypothesis testing
- Healthcare: Clinical trials, medical research
- Business: Marketing effectiveness, quality control
- Public Policy: Program evaluation

---

## College and Career Readiness Integration

### College Readiness

**AP Statistics prepares students for:**
- College Statistics (exemption with AP score 3+)
- Social Science majors (psychology, sociology, political science)
- Business and Economics majors
- Health Sciences (public health, nursing, pre-med)
- Data Science and Analytics
- Research methods courses

**AP Statistics is ideal for students pursuing:**
- Non-STEM majors (alternative to Calculus)
- Business, Economics, Psychology, Sociology, Political Science
- Healthcare (nursing, public health, epidemiology)
- Communications, Marketing, Sports Management
- **Also valuable for STEM students** (data analysis, research methods)

---

### Career Readiness

**Data-Driven Careers (Statistics is foundational):**

**Data Science and Analytics:**
- Business analytics, marketing analytics, sports analytics
- Data scientist, data analyst, quantitative analyst
- ALL data careers require statistics

**Business and Finance:**
- Market research analyst, financial analyst, actuary
- Risk assessment, investment analysis, quality control
- Economics, operations research

**Healthcare and Public Health:**
- Epidemiologist, biostatistician, public health analyst
- Clinical trial design, health outcomes research
- Medical research, pharmaceutical development

**Social Sciences:**
- Psychology researcher, survey researcher, political analyst
- Sociology, education research, program evaluation

**Government and Policy:**
- Census Bureau, Bureau of Labor Statistics
- Policy analysis, program evaluation, survey design

**Sports and Entertainment:**
- Sports analytics, Sabermetrics (baseball analytics)
- Market research for entertainment industry

---

## State Standards Alignment

### AP Statistics Curriculum (College Board)

**Primary Alignment:** AP Statistics Course and Exam Description (CED)

**See:** College Board AP Statistics Course and Exam Description

**AP Statistics Units:**
1. Exploring One-Variable Data (15%)
2. Exploring Two-Variable Data (5-7%)
3. Collecting Data (12-15%)
4. Probability, Random Variables, and Probability Distributions (10-20%)
5. Sampling Distributions (7-12%)
6. Inference for Categorical Data: Proportions (12-15%)
7. Inference for Quantitative Data: Means (10-18%)
8. Inference for Categorical Data: Chi-Square (2-5%)
9. Inference for Quantitative Data: Slopes (2-5%)

---

### State Standards (Where Applicable)

**Common Core States:**
- CCSS includes some statistics standards (S-ID, S-IC, S-CP, S-MD)
- AP Statistics extends beyond CCSS

**Texas:**
- Statistics course (optional, follows AP or similar curriculum)

**California:**
- Data Science pathway (alternative to traditional math sequence)
- Includes statistics, probability, data analysis

**All States:**
- High school Statistics typically aligns to AP Statistics
- Some schools offer non-AP Statistics (similar content, no AP exam)

---

## Instructional Strategies (High School Level)

### Integration with Universal HS Frameworks

**See:**
- `/universal/high-school/hs-instructional-strategies.md`
- `/universal/high-school/college-career-readiness-framework.md`

---

### Inquiry-Based Learning and Data Exploration

**Student-Generated Questions:**
- Start with question, collect data, analyze
- Example: "Do students who eat breakfast perform better on tests?"

**Real Data Analysis:**
- Use real data sets (Census, sports, economics)
- Students explore patterns, make discoveries

**Simulation-Based Learning:**
- Simulate probability distributions
- Visualize sampling distributions
- Understand variability through simulation

---

### Technology Integration (Essential in AP Statistics)

**Graphing Calculators (Required for AP Exam):**
- TI-83/84, TI-Nspire (check AP-approved list)
- Compute statistics (mean, SD, correlation)
- Create graphs (histograms, boxplots, scatterplots)
- Perform inference (confidence intervals, significance tests)
- Binomial/normal probability calculations

**Statistical Software (R, Python, Minitab, StatCrunch, Fathom):**
- Professional-level data analysis
- Create publication-quality graphics
- Perform complex analyses
- Programming skills (R, Python - valuable for careers)

**Simulation Tools (Desmos, online simulators):**
- Visualize sampling distributions
- Law of Large Numbers demonstrations
- Probability simulations

**AP Exam Policy:**
- Graphing calculator allowed on entire exam
- Must show work (not just calculator output)

---

### Connecting to Real-World Context (CRITICAL in Statistics)

**Always Analyze in Context:**
- Never just "the mean is 75"
- Always "the mean test score is 75 points"

**Data Stories:**
- Every data set has a story
- Who, what, when, where, why, how?

**Current Events:**
- Polls (elections, approval ratings)
- Studies in the news (health, psychology)
- Sports statistics (game analysis)

---

### Differentiation

**For Struggling Students:**
- Review algebra skills (solving equations, graphing)
- Scaffolded data analysis
- Technology support (calculators, software)
- Focus on interpretation over computation

**For Advanced Students:**
- Advanced inference topics (regression inference)
- Programming in R or Python
- Independent data analysis projects
- Statistical consulting for school/community

**For Emergent Bilinguals:**
- Math Language Routines (MLRs)
- Context-rich language support
- Bilingual glossaries
- Visual representations (graphs, diagrams)

---

## Assessment Approaches

### Formative Assessment

**Ongoing Checks:**
- Daily problem sets (AP-style multiple choice and free response)
- Data analysis activities
- Error analysis (common mistakes)
- Statistical reasoning discussions

**Strategic Questioning:**
- "What does this graph tell us about the distribution?"
- "How would you interpret this confidence interval?"
- "What are the limitations of this study?"
- "Is this correlation or causation?"

---

### Summative Assessment

**Unit Tests:**
- Multiple choice (AP-style)
- Free response (AP-style, show work and reasoning)
- Interpret output from calculator or software
- Always in context

**AP Exam Preparation:**
- Practice AP Exams (full-length, timed)
- Released Free Response Questions (FRQs)
- AP-style quizzes

**End-of-Course:**
- **AP Statistics Exam (May):** THE summative assessment
  - Section I: Multiple Choice (40 questions)
  - Section II: Free Response (6 questions: 5 short, 1 investigative task)
  - Scored 1-5 (3+ typically earns college credit)

---

### Performance-Based Assessment

**Projects:**
- Data Collection and Analysis Project (design study, collect data, analyze, report)
- Survey Design and Implementation
- Real-world data investigation (sports, economics, health)

**Presentations:**
- Present findings from data analysis
- Critique statistical study
- Explain statistical concept with examples

---

## Prerequisites and Course Sequencing

**Prerequisites:**
- Algebra II (recommended) OR Algebra I + Geometry (minimum)
- Strong algebra skills helpful but not required

**Prerequisite Skills:**
- Solving equations
- Graphing on coordinate plane
- Understanding functions
- Basic probability (helpful)

---

**Course Sequencing:**

**Typical:**
- Grade 12: **AP Statistics** ← Alternative to Calculus for non-STEM students

**For STEM Students (may take both):**
- Grade 11: AP Calculus AB
- Grade 12: **AP Statistics**

**For Data Science Pathway:**
- Grade 11: **AP Statistics**
- Grade 12: Data Science / Computer Science

**After AP Statistics:**
- College statistics courses (may be exempt with AP credit)
- Data science courses
- Research methods courses in college major

---

## Knowledge Reuse

### Reused from Universal Frameworks

✅ **UDL Principles** - 100% reuse
✅ **DOK Framework** - Emphasize DOK 2-3 (interpretation, analysis, reasoning)
✅ **EB Scaffolding** - 100% reuse
✅ **WCAG 2.1 AA** - 100% reuse
✅ **Assessment Tools** - 100% reuse

---

### Reused from Math Common

✅ **Math Language Routines (MLR1-MLR8)** - 100% reuse
- MLR2: Collect and Display (statistical vocabulary: distribution, correlation, p-value, etc.)
- MLR3: Clarify, Critique, Correct (interpretation and reasoning)
- MLR6: Three Reads (word problems in context)
- MLR7: Compare and Connect (multiple representations: graphical, numerical, verbal)
- MLR8: Discussion Supports (statistical reasoning sentence frames)

✅ **Math Vocabulary Guidelines** - 100% reuse

---

### Reused from Algebra I/II

✅ **Algebraic Skills** - 60-70% connection
- Solving equations
- Graphing (scatterplots, lines)
- Functions (for regression)

---

### Reused from State/District

✅ **ELL Frameworks** - 90% reuse

---

### Statistics-Specific Content (30-40%)

🔧 **Course-Specific:**
- AP Statistics scope and sequence
- Descriptive statistics (univariate and bivariate data)
- Study design (sampling, experimentation)
- Probability and probability distributions
- Statistical inference (confidence intervals, hypothesis tests)
- Interpretation in context (CRITICAL)
- AP Exam preparation strategies
- Technology use (calculator, statistical software)
- Free response writing and rubrics

---

## Quick Reference: AP Statistics Must-Haves

**Every AP Statistics Material Must:**
- Align to College Board AP Statistics Course and Exam Description (CED)
- Cover all AP units (exploring data, sampling/experimentation, probability, inference)
- Emphasize interpretation IN CONTEXT (never just numbers!)
- Use real data and real-world examples
- Teach proper study design and critique
- Prepare for calculator-active exam (entire exam)
- Include AP-style multiple choice and free response questions
- Use AP scoring rubrics for free response
- Develop statistical reasoning and critical thinking
- Address common misconceptions (correlation ≠ causation, p-value interpretation)
- Use Math Language Routines (MLRs)
- Support emergent bilinguals (ELPS/ELD)
- Support diverse learners (UDL)

**Common AP Statistics Misconceptions to Address:**
- "Correlation implies causation" (NO!)
- "The p-value is the probability H₀ is true" (NO! It's P(data | H₀ is true))
- "We accept the null hypothesis" (NO! Fail to reject ≠ accept)
- Confidence interval misinterpretation ("95% chance parameter is in interval" - NO!)

**Remember:** Statistics is about reasoning with data and uncertainty. Success requires critical thinking, clear communication, and understanding context. Every analysis must tell a data story with integrity, honesty, and appropriate skepticism.
