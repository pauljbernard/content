# A/B Test: Geometry Proofs Instructional Approaches

## Experiment Overview

**Experiment Name**: geometry-proofs-approach
**Duration**: 30 days
**Sample Size**: 500 learners (250 per variant)
**Primary Success Metric**: Mastery attainment
**Status**: Design Phase

---

## Research Question

**Primary Question**: Does a visual proof approach or an algebraic proof approach lead to higher mastery rates in geometry proof construction for high school students?

**Hypothesis**: Visual proof instruction will result in higher mastery rates due to increased accessibility for learners with different cognitive preferences and reduced cognitive load during initial concept formation.

---

## Variants

### Variant A: Visual Proof Approach
**Treatment ID**: `visual-proof`

**Instructional Design**:
- Emphasis on geometric diagrams, interactive visualizations, and spatial reasoning
- Proof construction using visual transformation sequences
- Color-coded relationships and congruent elements
- Animated proof steps showing geometric transformations
- Pattern recognition through visual examples
- Minimal symbolic notation in initial instruction

**Key Pedagogical Elements**:
- Van Hiele geometric thinking level progression
- Multiple representations (concrete → pictorial → abstract)
- Visual scaffolding with gradual removal
- Spatial reasoning development exercises
- Geometric software tools (GeoGebra, dynamic geometry)

### Variant B: Algebraic Proof Approach
**Treatment ID**: `algebraic-proof`

**Instructional Design**:
- Emphasis on formal logical structure, symbolic representation, and algebraic reasoning
- Proof construction using two-column format (statements and reasons)
- Algebraic notation for angles, segments, and relationships
- Deductive reasoning chains with explicit logical connectors
- Theorem application in symbolic form
- Formal proof writing conventions

**Key Pedagogical Elements**:
- Deductive reasoning scaffolding
- Logical structure templates
- Theorem bank with formal statements
- Symbolic manipulation practice
- Formal mathematical writing conventions

---

## Experimental Design

### Design Type
**Randomized Controlled Trial (RCT)** with:
- Random assignment to treatment groups
- Stratified sampling by prior mathematics achievement
- Balanced assignment within classrooms/cohorts
- Control for instructor effects (cross-assignment)

### Sample Specifications

**Total Sample**: 500 learners
- **Variant A (Visual)**: 250 learners
- **Variant B (Algebraic)**: 250 learners

**Inclusion Criteria**:
- Currently enrolled in Geometry (Grade 9-10)
- Completed algebra prerequisite
- No prior formal proof instruction
- Active participation commitment

**Exclusion Criteria**:
- Previous geometry course completion
- Currently receiving intensive intervention
- Missing baseline assessment data

**Stratification Variables**:
- Prior math achievement (low, medium, high)
- Grade level (9th, 10th)
- English learner status
- IEP status

### Randomization Protocol

1. **Baseline Data Collection**: Achievement, demographics, pre-test
2. **Stratification**: Group students by key variables
3. **Random Assignment**: Within strata, randomly assign to variant
4. **Verification**: Check balance across groups on baseline measures
5. **Blinding**: Learners unaware of experiment (both methods presented as standard instruction)

---

## Measurement & Success Metrics

### Primary Outcome: Mastery Attainment

**Definition**: Achievement of ≥80% on validated proof construction assessment

**Assessment Instrument**: Geometry Proof Mastery Assessment (GPMA)
- 10 proof construction tasks
- Range of difficulty (simple → complex)
- Scoring rubric: 0-4 points per item (max 40 points)
- Mastery threshold: 32/40 points (80%)

**Assessment Schedule**:
- **Baseline (Day 0)**: Pre-test (geometry concepts, reasoning skills)
- **Formative (Days 10, 20)**: Progress checks (not included in primary analysis)
- **Summative (Day 30)**: Post-test (GPMA - primary outcome)
- **Retention (Day 60)**: Follow-up assessment (optional)

### Secondary Outcomes

1. **Proof Quality Score** (0-40 scale)
   - Logical correctness (0-15 points)
   - Completeness (0-10 points)
   - Clarity and communication (0-10 points)
   - Efficiency (0-5 points)

2. **Transfer Performance**
   - Novel proof construction tasks
   - Cross-domain reasoning problems
   - Real-world application scenarios

3. **Engagement Metrics**
   - Time on task (learning platform analytics)
   - Completion rates for practice problems
   - Voluntary practice attempts
   - Help-seeking behavior

4. **Affective Outcomes**
   - Mathematics self-efficacy (pre/post survey)
   - Perceived difficulty (post-treatment survey)
   - Interest in geometry (pre/post survey)
   - Cognitive load (NASA-TLX adapted scale)

5. **Equity Metrics**
   - Achievement gap analysis by subgroup
   - Differential treatment effects
   - Accessibility feedback from EL and IEP students

---

## Statistical Analysis Plan

### Power Analysis

**Target Effect Size**: Cohen's h = 0.30 (medium effect on proportions)
- Visual mastery rate: 70%
- Algebraic mastery rate: 55%
- Difference: 15 percentage points

**Statistical Power**: 0.80
**Alpha Level**: 0.05 (two-tailed)
**Required Sample Size**: 220 per group (440 total)
**Planned Sample Size**: 250 per group (500 total)
**Justification**: 10% buffer for attrition

### Primary Analysis

**Research Question**: Does the visual proof variant increase mastery rates compared to the algebraic proof variant?

**Statistical Test**: Chi-square test of independence (2x2 contingency table)
- Rows: Treatment variant (Visual, Algebraic)
- Columns: Mastery status (Mastery, Non-mastery)

**Alternative Analysis**: Logistic regression
- Outcome: Mastery (binary)
- Primary predictor: Treatment variant
- Covariates: Baseline achievement, grade level, EL status, IEP status

**Effect Size Measures**:
- Relative risk (RR)
- Odds ratio (OR)
- Risk difference (absolute difference in mastery rates)
- Number needed to treat (NNT)

### Secondary Analyses

1. **Proof Quality Score**: Independent samples t-test (or Mann-Whitney U if non-normal)
2. **Transfer Performance**: ANCOVA with baseline score covariate
3. **Engagement Metrics**: Mixed-effects models with repeated measures
4. **Affective Outcomes**: Paired t-tests (pre/post) and between-group comparisons
5. **Subgroup Analyses**: Interaction tests for treatment × subgroup effects

### Interim Analysis

**Schedule**: Day 15 (midpoint)
**Purpose**: Monitor for extreme outcomes, safety, or unexpected issues
**Criteria for Early Termination**:
- Clear superiority of one variant (effect size > 0.8)
- Null findings with high certainty (futility analysis)
- Adverse outcomes (extreme frustration, attrition)

**Statistical Adjustment**: Lan-DeMets alpha spending function to control Type I error

---

## Implementation Plan

### Timeline (30-Day Intervention)

**Week 1 (Days 1-7): Foundations**
- Introduction to proof concepts
- Baseline assessment completion
- Initial exposure to assigned variant approach
- 3 instructional sessions (45 min each)
- Practice problem sets aligned to variant

**Week 2 (Days 8-14): Skill Building**
- Guided proof construction practice
- Scaffolded problem sets
- Formative assessment #1 (Day 10)
- 4 instructional sessions (45 min each)
- Peer collaboration activities

**Week 3 (Days 15-21): Application**
- Independent proof construction
- Complex multi-step proofs
- Formative assessment #2 (Day 20)
- 4 instructional sessions (45 min each)
- Interim data review and adjustment

**Week 4 (Days 22-30): Mastery & Assessment**
- Review and consolidation
- Transfer tasks and novel problems
- Summative assessment (Day 30 - GPMA)
- Post-treatment surveys
- 3 instructional sessions + assessment session

### Instructional Materials

**Common Elements** (both variants):
- Same learning objectives
- Same proof theorems and postulates covered
- Same number of practice problems (complexity matched)
- Same assessment instruments
- Same instructor training on general pedagogy

**Variant-Specific Materials**:
- **Visual Variant**: Interactive geometry software, visual proof templates, animated demonstrations, color-coded worksheets
- **Algebraic Variant**: Two-column proof templates, theorem reference cards, formal logic flowcharts, symbolic notation guides

### Instructor Training

**Pre-Implementation Workshop** (4 hours):
- Experimental design and ethics overview
- Treatment fidelity requirements
- Variant-specific pedagogical approaches
- Assessment administration protocols
- Data collection procedures

**Ongoing Support**:
- Weekly check-ins with research team
- Treatment fidelity checklists (completed after each session)
- Troubleshooting support channel
- Mid-experiment debrief session (Day 15)

### Treatment Fidelity Monitoring

**Observation Protocol**:
- Video recording of 20% of sessions (randomly selected)
- Independent coding by trained observers
- Fidelity checklist (variant-specific elements present/absent)
- Target fidelity: ≥80% adherence to variant protocols

**Self-Report**:
- Instructor daily logs
- Session-by-session checklists
- Departure from protocol documentation

---

## Data Collection & Management

### Data Sources

1. **Assessment Data**:
   - Pre-test scores (baseline)
   - Formative assessment scores (Days 10, 20)
   - Summative GPMA scores (Day 30)
   - Transfer task scores

2. **Learning Platform Analytics**:
   - Login frequency and duration
   - Problem completion rates
   - Time per problem
   - Hint/help requests
   - Accuracy on practice problems

3. **Survey Data**:
   - Pre-intervention surveys (self-efficacy, interest)
   - Post-intervention surveys (self-efficacy, interest, perceived difficulty, cognitive load)
   - User experience feedback

4. **Fidelity Data**:
   - Observation protocols
   - Instructor logs
   - Session checklists

5. **Demographic & Background Data**:
   - Prior math achievement
   - Grade level
   - English learner status
   - IEP status
   - Gender, race/ethnicity (optional, for equity analysis)

### Data Management

**Storage**:
- Secure database with role-based access control
- Encrypted at rest and in transit
- De-identified participant data (coded IDs)
- Separate key file (linking codes to PII)

**Quality Control**:
- Data validation rules (range checks, logic checks)
- Double-entry verification for critical variables
- Missing data documentation
- Regular data audits

**Anonymization**:
- All reporting uses aggregate or de-identified data
- No individual student identification in publications
- Secure destruction of PII linkage after study completion

---

## Ethical Considerations

### IRB Approval
- Expedited review application (educational research, minimal risk)
- Informed consent from participants (or parental consent for minors)
- Assent from minor participants
- Right to withdraw at any time

### Equipoise
- Both instructional approaches are evidence-based
- No expectation of harm from either variant
- All participants receive high-quality geometry instruction
- Non-mastery students receive additional support regardless of variant

### Data Privacy
- FERPA compliance (educational records protection)
- Minimal collection of personally identifiable information
- Secure data storage and transmission
- Limited access to identifiable data

### Equity & Access
- Accommodations provided as per IEP/504 plans
- Materials available in accessible formats
- Language support for English learners
- No cost to participants or schools

---

## Deployment Decision Criteria

### Statistical Criteria

**Primary Decision Rule**: Deploy winner if:
1. Statistically significant difference in mastery rate (p < 0.05)
2. Effect size ≥ 0.25 (small to medium)
3. Absolute difference in mastery rate ≥ 10 percentage points

**Confidence Threshold**: 95% confidence interval for difference excludes zero

### Practical Criteria

**Consider deploying winner if**:
- Significantly higher mastery rate
- No significant negative effects on secondary outcomes
- Positive user experience feedback
- Feasible implementation at scale
- No disproportionate burden on subgroups

**Do not deploy if**:
- No statistically significant difference (null result)
- Winner has significant drawbacks on secondary outcomes
- Implementation barriers are substantial
- Equity concerns arise (treatment benefits only some subgroups)

### Mixed Results Decision Tree

**Scenario 1**: Visual approach has higher mastery but lower engagement
- **Decision**: Deploy visual approach with engagement enhancements
- **Rationale**: Primary outcome takes precedence; engagement can be improved

**Scenario 2**: Algebraic approach has higher mastery but lower accessibility for EL/IEP students
- **Decision**: Do not deploy widely; develop hybrid or differentiated approach
- **Rationale**: Equity concerns override statistical superiority

**Scenario 3**: No significant difference in mastery; visual approach has higher self-efficacy
- **Decision**: Deploy visual approach with notation about equivalent mastery
- **Rationale**: Affective benefits support long-term learning trajectory

**Scenario 4**: Null results (no differences on any measure)
- **Decision**: Instructor choice or learner choice model
- **Rationale**: No evidence to prefer one approach; personalization may be optimal

---

## Reporting & Dissemination

### Internal Report (Day 35)

**Contents**:
- Executive summary (1 page)
- Full methodology
- Results (primary and secondary outcomes)
- Statistical analyses
- Deployment recommendation
- Appendices (data tables, charts, sample materials)

**Audience**: School administrators, curriculum directors, instructional team

### Stakeholder Presentation (Day 40)

**Format**: 30-minute presentation + Q&A
**Attendees**: Teachers, administrators, instructional coaches
**Focus**: Practical implications and implementation guidance

### Academic Publication (Month 6)

**Target Journals**:
- *Journal for Research in Mathematics Education*
- *Educational Studies in Mathematics*
- *Journal of Educational Psychology*

**Paper Outline**:
1. Introduction (literature review on proof instruction)
2. Methods (experimental design, measures, analysis)
3. Results (primary and secondary outcomes, subgroup analyses)
4. Discussion (interpretation, limitations, implications)
5. Conclusion (recommendations for practice and research)

---

## Budget & Resources

### Personnel

- **Principal Investigator**: 20 hours (design, oversight, analysis)
- **Research Assistant**: 60 hours (data collection, analysis support)
- **Instructors**: 4 teachers × 30 hours each = 120 hours
- **Observer/Coder**: 20 hours (fidelity monitoring)

**Total Personnel Hours**: 220 hours

### Materials & Technology

- Assessment development and validation: $2,000
- Learning platform subscription (500 users × 30 days): $1,500
- Geometry software licenses (GeoGebra Pro): $500
- Video recording equipment rental: $300
- Printing and materials: $200

**Total Materials**: $4,500

### Participant Incentives

- Student incentives ($10 gift card per participant): $5,000
- Instructor stipends ($200 per teacher): $800

**Total Incentives**: $5,800

### Data Analysis & Reporting

- Statistical consultation: $1,000
- Data management system: $500
- Report production: $200

**Total Analysis/Reporting**: $1,700

**Grand Total Budget**: $12,000

---

## Risk Mitigation

### Identified Risks & Mitigation Strategies

**Risk 1**: High attrition (>20%)
- **Mitigation**: Participant incentives, engaging materials, regular communication, make-up sessions
- **Contingency**: Increase initial sample size, conduct attrition analysis

**Risk 2**: Low treatment fidelity
- **Mitigation**: Comprehensive instructor training, ongoing support, fidelity checklists, monitoring
- **Contingency**: Per-protocol analysis in addition to intent-to-treat

**Risk 3**: Baseline imbalance between groups
- **Mitigation**: Stratified randomization, verification of balance before intervention
- **Contingency**: Statistical adjustment using baseline covariates

**Risk 4**: Technology failures (platform downtime)
- **Mitigation**: Backup offline materials, platform reliability testing, technical support
- **Contingency**: Extend intervention timeline if necessary

**Risk 5**: Measurement issues (assessment validity)
- **Mitigation**: Pilot-tested instruments, multiple outcome measures, inter-rater reliability checks
- **Contingency**: Triangulate findings across multiple measures

**Risk 6**: External validity threats (sample not representative)
- **Mitigation**: Recruit from multiple schools/classrooms, document sample characteristics
- **Contingency**: Acknowledge limitations, conduct follow-up studies

---

## Success Indicators (Process Metrics)

Throughout the 30-day experiment, monitor these indicators:

### Recruitment & Retention
- Target: 500 participants enrolled by Day 0 ✓
- Target: <20% attrition by Day 30 ✓
- Target: >90% summative assessment completion ✓

### Treatment Fidelity
- Target: ≥80% adherence to variant protocols ✓
- Target: All instructors complete training workshop ✓
- Target: <10% protocol deviations ✓

### Data Quality
- Target: <5% missing data on primary outcome ✓
- Target: 100% completion of baseline assessments ✓
- Target: All data validation checks passed ✓

### Engagement
- Target: ≥70% practice problem completion rate ✓
- Target: Average ≥60 minutes per week on platform ✓
- Target: <10% passive disengagement (no logins for >5 days) ✓

---

## Next Steps

### Phase 1: Design Completion (Current)
- ✓ Finalize experimental protocol
- Develop assessment instruments (GPMA, surveys)
- Create instructional materials for both variants
- Prepare data collection systems

### Phase 2: Validation & Piloting (2 weeks)
- Pilot test assessment instruments (n=30)
- Conduct instructor training workshops
- Test learning platform and data collection
- Finalize randomization protocol

### Phase 3: Implementation (30 days)
- Recruit and enroll participants
- Randomize to treatment groups
- Deliver interventions with fidelity monitoring
- Collect all data sources

### Phase 4: Analysis & Reporting (2-3 weeks)
- Clean and validate data
- Conduct statistical analyses
- Prepare internal report and presentation
- Make deployment recommendation

### Phase 5: Deployment or Iteration (Ongoing)
- If winner identified: Develop scaling plan
- If null/mixed: Design follow-up study or hybrid approach
- Disseminate findings to stakeholders
- Submit for publication

---

## Contact & Documentation

**Project Lead**: [Name, Email]
**IRB Protocol Number**: [TBD]
**Trial Registration**: ClinicalTrials.gov (if applicable)
**Data Repository**: [TBD - OSF, ICPSR, or institutional repository]

**Version History**:
- v1.0 (2025-11-04): Initial design document

---

## Appendices

### Appendix A: Learning Objectives (Common to Both Variants)

Students will be able to:
1. Identify given information and what needs to be proven in a geometric proof
2. Select appropriate definitions, postulates, and theorems to justify statements
3. Construct a logical sequence of statements leading from givens to conclusion
4. Communicate geometric relationships using appropriate notation and terminology
5. Verify the validity of a geometric proof
6. Construct proofs involving congruent triangles, parallel lines, and quadrilaterals
7. Apply proof techniques to novel geometric situations

### Appendix B: Assessment Specifications (GPMA)

**Item Distribution**:
- 3 items: Congruent triangle proofs (SSS, SAS, ASA criteria)
- 2 items: Parallel lines and transversals (angle relationships)
- 2 items: Quadrilateral properties (parallelograms, rectangles)
- 2 items: Isosceles triangle proofs
- 1 item: Novel application (transfer task)

**Cognitive Demand** (Webb's DOK):
- Level 1 (Recall): 0 items
- Level 2 (Skill/Concept): 3 items (30%)
- Level 3 (Strategic Thinking): 5 items (50%)
- Level 4 (Extended Thinking): 2 items (20%)

### Appendix C: Treatment Fidelity Checklist

Completed after each instructional session:

**Core Elements** (required for both variants):
- [ ] Stated learning objectives at start
- [ ] Connected to prior knowledge
- [ ] Provided multiple examples
- [ ] Included guided practice
- [ ] Included independent practice
- [ ] Assessed understanding (formative)
- [ ] Summarized key concepts

**Visual Variant Elements**:
- [ ] Used dynamic geometry software
- [ ] Emphasized visual patterns and relationships
- [ ] Color-coded congruent elements
- [ ] Showed animated transformations
- [ ] Minimal symbolic notation in examples

**Algebraic Variant Elements**:
- [ ] Used two-column proof format
- [ ] Emphasized formal logical structure
- [ ] Applied symbolic notation consistently
- [ ] Referenced theorems by formal name
- [ ] Practiced formal proof writing conventions

### Appendix D: Sample Size Sensitivity Analysis

**Scenario 1: Lower Effect Size (h = 0.20)**
- Required n per group: 394
- With 250 per group: Power = 0.60 (underpowered)

**Scenario 2: Target Effect Size (h = 0.30)**
- Required n per group: 175
- With 250 per group: Power = 0.88 (well-powered)

**Scenario 3: Higher Effect Size (h = 0.40)**
- Required n per group: 98
- With 250 per group: Power = 0.98 (overpowered)

**Conclusion**: Sample size of 250 per group provides adequate power for small-to-medium effects.

---

**Document Status**: DRAFT - Ready for Review
**Next Review Date**: [Date before pilot testing]
**Approval Required From**: IRB, School District, Research Team
