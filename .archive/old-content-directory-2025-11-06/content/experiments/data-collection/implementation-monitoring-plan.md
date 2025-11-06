# Implementation & Monitoring Plan
## Geometry Proofs A/B Test

**Experiment**: geometry-proofs-approach
**Duration**: 30 days
**Sample Size**: 500 learners

---

## Pre-Implementation Phase (Weeks -2 to 0)

### Week -2: Recruitment & Baseline Assessment

#### Day -14 to -10: Participant Recruitment

**Activities**:
1. **School/Teacher Recruitment**:
   - Contact geometry teachers at participating schools
   - Present study overview and obtain teacher consent
   - Schedule information sessions for students/parents

2. **Student/Parent Information Sessions**:
   - Distribute study information packets
   - Explain voluntary participation, random assignment, and data privacy
   - Distribute consent forms (parental consent + student assent for minors)
   - Answer questions about time commitment, incentives, and data use

3. **Consent Collection**:
   - Collect signed consent/assent forms
   - Track consent rate (target: ≥70% of eligible students)
   - Follow up with non-responders (reminder emails, phone calls)

**Deliverables**:
- [ ] Information packet distributed to all eligible students
- [ ] Consent forms collected from ≥500 students
- [ ] Participant database created with coded IDs

**Responsible Party**: Research Coordinator
**Status Check**: Day -10 (verify enrollment target met)

---

#### Day -9 to -7: Baseline Data Collection

**Activities**:
1. **Demographic & Background Data**:
   - Collect from school records (with permission):
     - Prior math achievement (previous course grade or standardized test score)
     - Grade level (9th or 10th)
     - English learner status
     - IEP/504 status
     - Gender, race/ethnicity (optional, for equity analysis)
   - Store securely with coded IDs (no PII in analysis dataset)

2. **Baseline Assessment Administration**:
   - Administer pre-test measuring:
     - Geometry prerequisite knowledge (angles, triangles, basic properties)
     - Spatial reasoning skills
     - Logical reasoning ability
   - Duration: 30 minutes
   - Administer during regular class time
   - Provide accommodations per IEP/504 plans

3. **Baseline Surveys**:
   - Mathematics self-efficacy scale (10 items, 5-point Likert)
   - Interest in geometry (5 items)
   - Prior experience with proofs (3 items)
   - Duration: 10 minutes

**Deliverables**:
- [ ] Demographic data collected for all participants
- [ ] Pre-test completed by ≥95% of participants
- [ ] Baseline surveys completed by ≥95% of participants
- [ ] Data entered and validated in database

**Responsible Party**: Classroom Teachers (assessment administration); Research Assistant (data entry)
**Status Check**: Day -7 (verify completion rate)

---

### Week -1: Randomization & Preparation

#### Day -6 to -4: Stratification & Randomization

**Activities**:
1. **Stratification**:
   - Group participants by:
     - Prior math achievement (low: <70%, medium: 70-84%, high: ≥85%)
     - Grade level (9th, 10th)
     - English learner status (yes/no)
     - IEP/504 status (yes/no)
   - Create stratification cells (e.g., 9th grade, medium achievement, non-EL, no IEP)

2. **Random Assignment**:
   - Within each stratum, randomly assign 50% to Visual Variant, 50% to Algebraic Variant
   - Use random number generator (seed documented for reproducibility)
   - Generate assignment list: Participant ID → Variant (Visual or Algebraic)

3. **Balance Check**:
   - Compare groups on baseline measures:
     - Pre-test scores (t-test for difference)
     - Demographics (chi-square for categorical variables)
     - Self-efficacy and interest (t-tests)
   - Target: No significant differences (p > .05)
   - If imbalance detected: Re-randomize or plan to adjust statistically

4. **Class Assignment**:
   - Assign participants to class sections based on variant (if possible)
   - If mixed classes necessary: Ensure instructors can deliver both variants
   - Document any deviations from ideal randomization

**Deliverables**:
- [ ] Stratification cells created
- [ ] Random assignment completed
- [ ] Balance check report generated
- [ ] Class/section assignments finalized
- [ ] Assignment list distributed to teachers (secure, confidential)

**Responsible Party**: Principal Investigator + Statistician
**Status Check**: Day -4 (verify balance; approve randomization)

---

#### Day -3 to -1: Instructor Training & Materials Prep

**Activities**:
1. **Instructor Training Workshop** (4 hours):
   - **Session 1 (90 min)**: Study Overview & Ethics
     - Research design and rationale
     - Ethical guidelines (confidentiality, equipoise, voluntary participation)
     - Role of instructors (deliver treatment, not advocate for one variant)
     - Treatment fidelity expectations

   - **Break (15 min)**

   - **Session 2 (90 min)**: Variant-Specific Pedagogy
     - Split into two groups: Visual Variant instructors, Algebraic Variant instructors
     - Review sample lesson plans
     - Practice key instructional moves
     - Discuss common student misconceptions and how to address them

   - **Session 3 (45 min)**: Assessment & Data Collection
     - Assessment administration protocols
     - Fidelity checklist training
     - Learning platform orientation
     - Q&A

2. **Materials Distribution**:
   - Provide each instructor with:
     - Variant-specific lesson plans (all 12 lessons for 30-day unit)
     - Student workbooks (printed or digital)
     - Assessment materials
     - Fidelity checklists (one per lesson)
     - Learning platform login credentials
     - Consent forms and study information
   - Ensure all materials are organized and ready for Day 1

3. **Technology Setup**:
   - Provision learning platform accounts for all participants
   - Pre-load variant-specific materials (visual: GeoGebra files; algebraic: proof templates)
   - Test platform functionality (login, content access, data tracking)
   - Troubleshoot any technical issues

4. **Communication Plan**:
   - Establish weekly check-in meetings (virtual or in-person)
   - Create instructor support channel (email, chat, or discussion forum)
   - Distribute study calendar with key dates (assessments, data submission deadlines)

**Deliverables**:
- [ ] All instructors complete training workshop
- [ ] Training evaluation survey completed (assess instructor confidence)
- [ ] All materials distributed and organized
- [ ] Learning platform fully operational
- [ ] Communication channels established

**Responsible Party**: Principal Investigator + Research Assistant + Instructional Technology Specialist
**Status Check**: Day -1 (verify all systems ready; conduct dry run if possible)

---

## Implementation Phase (Days 1-30)

### Week 1 (Days 1-7): Foundations

#### Daily Activities (All Instructors)

**Day 1**:
- Welcome students; review study participation (voluntary, confidential)
- Administer brief "Getting to Know You" activity
- Introduce unit topic: Triangle Congruence and Geometric Proof
- **Visual Variant**: Lesson 1 - Introduction to Congruent Triangles (Visual Approach)
- **Algebraic Variant**: Lesson 1 - Introduction to Congruent Triangles (Algebraic Approach)
- Students complete post-lesson reflection (2 min)
- **Instructor**: Complete fidelity checklist (5 min)

**Day 2**:
- Brief review of Day 1 concepts
- **Visual Variant**: Lesson 2 - SSS Congruence with Transformations
- **Algebraic Variant**: Lesson 2 - SSS Postulate and Two-Column Proofs
- Practice problem set (10 problems, 15 min)
- **Instructor**: Complete fidelity checklist

**Day 3**:
- Brief review; address common errors from Day 2 practice
- **Visual Variant**: Lesson 3 - SAS Congruence with Angle Locking
- **Algebraic Variant**: Lesson 3 - SAS Postulate and Included Angles
- Practice problem set (10 problems, 15 min)
- **Instructor**: Complete fidelity checklist

**Day 4**:
- Brief review
- **Visual Variant**: Lesson 4 - ASA Congruence with Ray Intersection
- **Algebraic Variant**: Lesson 4 - ASA Postulate and Included Sides
- Practice problem set (10 problems, 15 min)
- **Instructor**: Complete fidelity checklist

**Day 5**:
- Synthesis activity: Compare and contrast SSS, SAS, ASA
- Mixed practice problems (all three postulates)
- Peer collaboration: Students explain proofs to each other
- **Instructor**: Complete fidelity checklist

**Day 6**:
- Review session: Address misconceptions from Week 1
- Guided practice: Instructor works through 2-3 complex examples
- Independent practice: Students complete 5 proofs
- **Instructor**: Complete fidelity checklist

**Day 7**:
- **Formative Assessment #0** (Week 1 progress check, low-stakes)
- Students complete 5 short proof problems (20 min)
- Self-reflection: "What do I understand well? What is still confusing?"
- **Instructor**: Complete fidelity checklist

#### Monitoring & Support (Week 1)

**Research Team Activities**:
- **Day 2**: Check-in with all instructors (brief email or call)
  - How did Day 1 go?
  - Any issues with materials or technology?
  - Students engaged and on track?

- **Day 4**: Review fidelity checklists for Days 1-3 (random sample of 3 instructors)
  - Verify core elements are being implemented
  - Provide feedback if deviations noted

- **Day 7**: Collect Week 1 data
  - Fidelity checklists (all instructors)
  - Formative assessment scores
  - Learning platform analytics (logins, time on task, problem completion)
  - Attrition tracking (any dropouts?)

**Red Flags to Monitor**:
- Low treatment fidelity (<70% adherence to checklist)
- High student attrition (>10% dropouts in Week 1)
- Technology issues preventing access
- Instructor confusion or deviation from protocol

**Intervention if Red Flags Detected**:
- Schedule immediate consultation with instructor
- Provide additional support or materials
- Document issue and resolution

**Deliverables** (End of Week 1):
- [ ] Fidelity checklists completed for all 7 days by all instructors
- [ ] Formative assessment scores collected and entered
- [ ] Platform analytics downloaded
- [ ] Week 1 data quality check completed
- [ ] Any issues documented and addressed

---

### Week 2 (Days 8-14): Skill Building

#### Daily Activities

**Day 8**:
- Debrief Week 1 formative assessment (return scores, discuss common errors)
- **Visual Variant**: Lesson 5 - Multi-Step Proofs with Transformations (Vertical Angles)
- **Algebraic Variant**: Lesson 5 - Multi-Step Proofs (Vertical Angles Theorem)
- Practice problem set
- **Instructor**: Complete fidelity checklist

**Day 9**:
- **Visual Variant**: Lesson 6 - Shared Elements and Reflexive Property (Visual Overlay)
- **Algebraic Variant**: Lesson 6 - Reflexive Property in Two-Column Proofs
- Practice problem set
- **Instructor**: Complete fidelity checklist

**Day 10**:
- **Formative Assessment #1** (Primary data point)
- Duration: 30 minutes
- 5 proof problems (mix of SSS, SAS, ASA, multi-step)
- Scores recorded in database
- **Instructor**: Complete fidelity checklist (assessment administration)

**Day 11**:
- Debrief Formative Assessment #1
- **Visual Variant**: Lesson 7 - Isosceles Triangle Proofs (Visual Symmetry)
- **Algebraic Variant**: Lesson 7 - Isosceles Triangle Proofs (Definitions and Properties)
- Practice problem set
- **Instructor**: Complete fidelity checklist

**Day 12**:
- **Visual Variant**: Lesson 8 - Parallel Lines and Transversals (Visual Angle Patterns)
- **Algebraic Variant**: Lesson 8 - Parallel Lines and Alternate Interior Angles Theorem
- Practice problem set
- **Instructor**: Complete fidelity checklist

**Day 13**:
- Collaborative problem-solving session
- Students work in pairs to construct proofs (3-4 problems)
- Instructor circulates, provides scaffolding
- Gallery walk: Pairs present one proof to class
- **Instructor**: Complete fidelity checklist

**Day 14**:
- Review and consolidation: Key concepts from Weeks 1-2
- Mixed practice (10 problems, various difficulty levels)
- Students complete mid-unit self-reflection survey (10 min)
- **Instructor**: Complete fidelity checklist

#### Monitoring & Support (Week 2)

**Research Team Activities**:
- **Day 8**: Weekly check-in meeting with instructors (virtual, 30 min)
  - Share Week 1 insights
  - Discuss any challenges
  - Preview Week 2 lessons

- **Day 10**: Data collection priority (Formative Assessment #1)
  - Ensure all assessments administered
  - Collect and enter scores immediately
  - Flag any missing data

- **Day 12**: Fidelity observation (optional but recommended)
  - Observe 2-3 classes (one Visual, one Algebraic) via video recording
  - Code fidelity using checklist
  - Provide feedback to instructors

- **Day 14**: Collect Week 2 data
  - Fidelity checklists (all days)
  - Formative Assessment #1 scores
  - Mid-unit surveys
  - Platform analytics
  - Attrition tracking

**Deliverables** (End of Week 2):
- [ ] Fidelity checklists for Days 8-14 collected
- [ ] Formative Assessment #1 scores entered (100% completion target)
- [ ] Mid-unit surveys collected
- [ ] Week 2 data quality check completed
- [ ] Fidelity observations coded (if conducted)

---

### Week 3 (Days 15-21): Application

#### Daily Activities

**Day 15**: **Interim Analysis & Adjustment**
- **Research Team**: Conduct interim analysis
  - Review mastery rates for both variants (preliminary)
  - Assess engagement metrics
  - Check for adverse outcomes (excessive frustration, attrition)
  - Decide: Continue as planned, make minor adjustments, or (rarely) early termination
- **Instructors**: Regular lesson (no change from student perspective)
  - **Visual Variant**: Lesson 9 - Overlapping Triangles (Visual Parsing)
  - **Algebraic Variant**: Lesson 9 - Overlapping Triangles (Correspondence Identification)
- **Instructor**: Complete fidelity checklist

**Day 16**:
- **Visual Variant**: Lesson 10 - Right Triangles and HL Theorem (Hypotenuse Highlighting)
- **Algebraic Variant**: Lesson 10 - HL Theorem in Two-Column Format
- Practice problem set
- **Instructor**: Complete fidelity checklist

**Day 17**:
- **Visual Variant**: Lesson 11 - AAS Theorem (Derived from ASA, Visual Demonstration)
- **Algebraic Variant**: Lesson 11 - AAS Theorem (Formal Derivation from ASA)
- Practice problem set
- **Instructor**: Complete fidelity checklist

**Day 18**:
- Complex problem-solving session
- Students tackle challenging multi-step proofs (3 problems, 20 min each)
- Instructor provides minimal scaffolding (promote independence)
- **Instructor**: Complete fidelity checklist

**Day 19**:
- Error analysis activity
- Students review flawed proofs, identify errors, correct them
- Discussion: Common mistakes and how to avoid them
- **Instructor**: Complete fidelity checklist

**Day 20**:
- **Formative Assessment #2** (Primary data point)
- Duration: 30 minutes
- 5 proof problems (includes complex, multi-step, and HL/AAS items)
- Scores recorded in database
- **Instructor**: Complete fidelity checklist

**Day 21**:
- Debrief Formative Assessment #2
- Review session: Address errors from assessment
- Students set personal goals for Week 4 (mastery focus)
- **Instructor**: Complete fidelity checklist

#### Monitoring & Support (Week 3)

**Research Team Activities**:
- **Day 15**: Interim analysis and decision meeting
  - Analyze data from Weeks 1-2
  - Present findings to research team
  - Document decision (continue, adjust, or terminate)
  - If adjustments: Communicate to instructors immediately

- **Day 17**: Weekly check-in with instructors

- **Day 20**: Data collection priority (Formative Assessment #2)
  - Immediate collection and entry

- **Day 21**: Collect Week 3 data
  - Fidelity checklists
  - Formative Assessment #2 scores
  - Platform analytics
  - Attrition tracking

**Deliverables** (End of Week 3):
- [ ] Interim analysis report completed
- [ ] Decision documented (continue/adjust/terminate)
- [ ] Fidelity checklists for Days 15-21 collected
- [ ] Formative Assessment #2 scores entered
- [ ] Week 3 data quality check completed

---

### Week 4 (Days 22-30): Mastery & Assessment

#### Daily Activities

**Day 22**:
- **Visual Variant**: Lesson 12 - Transfer and Application (Real-World Proof Problems)
- **Algebraic Variant**: Lesson 12 - Transfer and Application (Formal Proofs in Novel Contexts)
- Practice problem set
- **Instructor**: Complete fidelity checklist

**Day 23**:
- Proof construction workshop
- Students create their own proof problems (given diagram, write proof)
- Peer exchange: Students solve each other's problems
- **Instructor**: Complete fidelity checklist

**Day 24**:
- Review session: Comprehensive review of all concepts (SSS, SAS, ASA, AAS, HL, multi-step)
- Instructor leads review; students contribute examples
- Practice problem marathon (20 problems, mix of all types)
- **Instructor**: Complete fidelity checklist

**Day 25**:
- Review session (continued)
- Focus on areas of weakness identified in formative assessments
- Small group work: Differentiated support based on need
- **Instructor**: Complete fidelity checklist

**Day 26**:
- Practice test (optional, low-stakes)
- Simulates summative assessment format and length
- Students self-score using rubric
- Identify final areas for review
- **Instructor**: Complete fidelity checklist

**Day 27**:
- Final review and consolidation
- Q&A session: Students ask questions
- Proof strategy discussion: Tips for success on assessment
- Relaxation and confidence-building (assessment is tomorrow!)
- **Instructor**: Complete fidelity checklist

**Day 28-29**:
- **SUMMATIVE ASSESSMENT: Geometry Proof Mastery Assessment (GPMA)** - PRIMARY OUTCOME
- Duration: 60 minutes (90-120 min for students with extended time accommodations)
- 10 proof construction problems
- Administered in standardized conditions (quiet, individual, no collaboration)
- All materials collected immediately after session
- **Instructors**: Administer assessment; complete administration fidelity checklist

**Day 30**:
- **Post-Intervention Surveys**
  - Mathematics self-efficacy scale (post-test, same as baseline)
  - Interest in geometry (post-test)
  - Perceived difficulty of unit (new)
  - Cognitive load scale (NASA-TLX adapted)
  - Open-ended feedback: "What helped you learn? What was challenging?"
  - User experience feedback (variant-specific)
- Duration: 20 minutes
- Debrief session: Thank students for participation; explain next steps (results shared in 2-3 weeks)
- Distribute incentives ($10 gift cards)
- **Instructor**: Complete fidelity checklist

#### Monitoring & Support (Week 4)

**Research Team Activities**:
- **Day 24**: Weekly check-in with instructors
  - Prepare for summative assessment
  - Review administration protocols
  - Address any last-minute concerns

- **Day 28-29**: Assessment administration monitoring
  - Research team members present at assessment sites (if possible)
  - Verify standardized conditions
  - Collect assessment materials immediately
  - Secure storage (locked cabinet)

- **Day 30**: Final data collection
  - Post-intervention surveys collected
  - Distribute incentives (verify receipt)
  - Final attrition count

**Deliverables** (End of Week 4):
- [ ] Fidelity checklists for Days 22-30 collected
- [ ] GPMA completed by all participants (target: ≥90%)
- [ ] Post-intervention surveys completed (target: ≥95%)
- [ ] Incentives distributed to all completers
- [ ] All materials secured
- [ ] Final attrition report

---

## Post-Implementation Phase (Days 31-45)

### Week 5 (Days 31-35): Data Processing & Scoring

#### Activities

**Day 31-32**: GPMA Scoring
- Research team scores all GPMA assessments using rubric
- 20% of assessments scored independently by two raters (inter-rater reliability)
- Calculate Cohen's kappa (target: ≥0.80)
- Resolve discrepancies through discussion and consensus
- Enter scores into database

**Day 33**: Data Cleaning & Validation
- Check for missing data (identify and document)
- Verify data entry accuracy (10% random sample double-checked)
- Flag outliers or anomalies for review
- Resolve any data quality issues

**Day 34**: Fidelity Data Analysis
- Calculate treatment fidelity scores for each instructor (% adherence to checklist)
- Identify any systematic deviations from protocol
- Classify participants as "protocol adherent" vs. "protocol deviant" (for per-protocol analysis)
- Generate fidelity report

**Day 35**: Data Preparation for Analysis
- Merge all data sources (demographics, baseline, intervention, outcome)
- Create analysis-ready dataset (de-identified)
- Generate descriptive statistics
- Verify randomization balance (compare groups on baseline measures)

**Deliverables**:
- [ ] All GPMA assessments scored
- [ ] Inter-rater reliability calculated (κ ≥ 0.80)
- [ ] Data cleaned and validated
- [ ] Fidelity scores calculated
- [ ] Analysis-ready dataset created

---

### Week 6 (Days 36-40): Analysis & Reporting

#### Activities

**Day 36-37**: Primary Analysis
- Calculate mastery rates for each variant (Visual, Algebraic)
- Conduct chi-square test of independence (primary analysis)
- Calculate effect size measures (relative risk, odds ratio, risk difference, NNT)
- Run logistic regression with covariates (baseline achievement, grade, EL status, IEP status)
- Generate tables and figures

**Day 38**: Secondary Analyses
- Compare proof quality scores (t-test or Mann-Whitney U)
- Analyze subscale scores (Basic, Strategic, Transfer)
- Examine engagement metrics (time on task, completion rates)
- Analyze affective outcomes (self-efficacy, interest, cognitive load)
- Conduct subgroup analyses (treatment × subgroup interactions)

**Day 39**: Report Writing
- Draft results section (text, tables, figures)
- Write interpretation and discussion
- Draft recommendations (deploy winner, conduct follow-up, etc.)

**Day 40**: Internal Report Finalized
- Review by research team
- Incorporate feedback
- Finalize report (Executive Summary, Methods, Results, Discussion, Recommendations)

**Deliverables**:
- [ ] Primary analysis completed
- [ ] Secondary analyses completed
- [ ] Internal report finalized (ready for stakeholder distribution)

---

### Week 7 (Days 41-45): Dissemination & Deployment Decision

#### Activities

**Day 41**: Stakeholder Presentation Preparation
- Create slide deck (30-minute presentation)
- Highlight key findings, practical implications, recommendations
- Prepare for Q&A

**Day 42**: Stakeholder Presentation
- Present findings to school administrators, teachers, instructional coaches
- Facilitate discussion
- Gather feedback on deployment decision

**Day 43-44**: Deployment Decision
- Review findings against deployment criteria (statistical + practical)
- Make recommendation: Deploy winner, hybrid approach, learner choice, or further study
- Document decision and rationale

**Day 45**: Communication to Participants
- Send email to all participants (students, parents, teachers)
- Share aggregate results (no individual identification)
- Explain deployment decision
- Thank participants for contribution to research

**Deliverables**:
- [ ] Stakeholder presentation delivered
- [ ] Deployment decision documented
- [ ] Participant communication sent

---

## Monitoring Dashboard (Weekly Metrics)

The research team will track these metrics weekly throughout the implementation phase:

### Participation & Attrition
- Enrolled: [#] / 500
- Active (still participating): [#] / 500
- Attrition rate: [%]% (target: <20%)
- Reason for attrition: [List]

### Treatment Fidelity
- Average fidelity score (all instructors): [%]% (target: ≥80%)
- Instructors meeting fidelity threshold: [#] / [#] (target: 100%)
- Common deviations: [List]

### Engagement
- Average logins per student per week: [#]
- Average time on platform per week: [minutes]
- Practice problem completion rate: [%]% (target: ≥70%)
- Help requests per student per week: [#]

### Assessment Completion
- Formative Assessment #1 (Day 10): [#] / 500 ([%]%)
- Formative Assessment #2 (Day 20): [#] / 500 ([%]%)
- Summative GPMA (Day 28-29): [#] / 500 (target: ≥90%)
- Post-surveys (Day 30): [#] / 500 (target: ≥95%)

### Preliminary Outcomes (Formative Assessments)
- Visual Variant - Avg Score: [X]/20 ([%]%)
- Algebraic Variant - Avg Score: [X]/20 ([%]%)
- Difference: [X] points ([%]%)
- Statistical significance: [p-value] (Note: Interim, not conclusive)

### Data Quality
- Missing data rate: [%]% (target: <5%)
- Data validation errors: [#] (target: 0 after correction)
- Survey completion rate: [%]%

### Issues & Resolutions
- Technical issues: [#] reported, [#] resolved
- Instructor concerns: [#] reported, [#] resolved
- Student accommodations: [#] students, [#] types
- Protocol deviations: [#] reported, [#] reviewed

---

## Communication Protocol

### Instructor Support Channels

**Tier 1: Daily Issues** (technology, materials, minor questions)
- **Channel**: Email to research-support@[domain].edu or Slack channel
- **Response Time**: Within 4 hours (during business hours)
- **Responsible Party**: Research Assistant

**Tier 2: Pedagogical Questions** (instruction, assessment, student support)
- **Channel**: Weekly check-in meetings or email to PI
- **Response Time**: Within 24 hours
- **Responsible Party**: Principal Investigator

**Tier 3: Urgent Issues** (safety, ethics, major protocol deviations)
- **Channel**: Phone call to PI (urgent line)
- **Response Time**: Immediate
- **Responsible Party**: Principal Investigator

### Participant Communication

**To Students**:
- **Week 0 (Day -3)**: Welcome email with study overview, platform login, consent reminder
- **Week 1 (Day 1)**: In-class introduction and orientation
- **Week 2 (Day 10)**: Encouragement message ("You're doing great! Keep practicing.")
- **Week 3 (Day 20)**: Motivation message ("Halfway there! You've learned so much.")
- **Week 4 (Day 27)**: Assessment prep tips and confidence booster
- **Week 4 (Day 30)**: Thank you and next steps (results in 2-3 weeks)
- **Week 7 (Day 45)**: Results summary and deployment decision

**To Parents** (if participants are minors):
- **Week 0 (Day -7)**: Study overview and consent request
- **Week 1 (Day 1)**: Confirmation that study has begun
- **Week 3 (Day 15)**: Progress update (general, no individual scores)
- **Week 4 (Day 30)**: Thank you for supporting participation
- **Week 7 (Day 45)**: Results summary

---

## Contingency Plans

### Scenario 1: High Attrition (>20% by Week 2)

**Action**:
1. Conduct exit interviews with students who withdrew (identify reasons)
2. Increase engagement strategies (incentives, encouragement, reduce workload if excessive)
3. Extend recruitment to additional classes (if possible)
4. Adjust sample size for power calculation (may reduce statistical power)
5. Document attrition as limitation in final report

---

### Scenario 2: Low Treatment Fidelity (<70% for any instructor)

**Action**:
1. Schedule immediate consultation with instructor
2. Observe class session (in-person or video)
3. Provide targeted coaching and support
4. If fidelity remains low: Consider excluding that instructor's students from per-protocol analysis (but retain in intent-to-treat analysis)
5. Document fidelity issues and impact on results

---

### Scenario 3: Technology Failure (platform downtime >1 day)

**Action**:
1. Switch to offline materials (printed workbooks)
2. Extend intervention timeline by # of days lost
3. Distribute catch-up assignments
4. Document technology issues and impact

---

### Scenario 4: Interim Analysis Shows Extreme Outcome (Effect Size >0.8 or <-0.8)

**Action**:
1. Convene research team for emergency review
2. Verify data quality (check for errors)
3. Consider early termination (if one variant clearly superior)
4. If continuing: Offer non-mastery students in weaker variant additional support
5. Document decision and rationale

---

### Scenario 5: Unexpected External Event (school closure, natural disaster, pandemic)

**Action**:
1. Pause study immediately
2. Secure all data collected to date
3. Assess feasibility of resuming or pivoting (e.g., to online delivery)
4. Communicate with all stakeholders (participants, IRB, funders)
5. Document event and impact; revise protocol if necessary

---

## Ethical Monitoring

### IRB Reporting

**Scheduled Reports**:
- **Day 15**: Interim report (enrollment, attrition, adverse events)
- **Day 45**: Final report (completion, outcomes, adverse events, protocol deviations)

**Unscheduled Reports** (within 24 hours of occurrence):
- Serious adverse events (e.g., student distress requiring intervention)
- Major protocol deviations
- Unanticipated problems
- Changes to consent or study procedures

### Data Safety Monitoring Board (Optional, for larger studies)

**Composition**: 3 independent experts (1 statistician, 1 education researcher, 1 ethicist)
**Meetings**: Day 15 (interim), Day 45 (final)
**Role**: Review data for safety, efficacy, and ethical conduct; recommend continue/modify/terminate

---

## Summary Checklist: Critical Milestones

| Milestone | Target Date | Status | Responsible Party |
|-----------|-------------|--------|-------------------|
| Recruitment complete (≥500 enrolled) | Day -10 | [ ] | Research Coordinator |
| Baseline data collected (≥95% complete) | Day -7 | [ ] | Teachers + RA |
| Randomization complete & balanced | Day -4 | [ ] | PI + Statistician |
| Instructor training complete | Day -1 | [ ] | PI + RA |
| Week 1 fidelity data collected | Day 7 | [ ] | Instructors + RA |
| Formative Assessment #1 complete | Day 10 | [ ] | Teachers + RA |
| Interim analysis complete | Day 15 | [ ] | Statistician + PI |
| Formative Assessment #2 complete | Day 20 | [ ] | Teachers + RA |
| Summative GPMA complete (≥90%) | Day 29 | [ ] | Teachers + RA |
| Post-surveys complete (≥95%) | Day 30 | [ ] | Teachers + RA |
| Incentives distributed | Day 30 | [ ] | Research Coordinator |
| GPMA scored (100% scored, IRR verified) | Day 32 | [ ] | Research Team |
| Data cleaned and analysis-ready | Day 35 | [ ] | RA + Statistician |
| Primary analysis complete | Day 37 | [ ] | Statistician |
| Internal report finalized | Day 40 | [ ] | PI + Team |
| Stakeholder presentation delivered | Day 42 | [ ] | PI |
| Deployment decision documented | Day 44 | [ ] | PI + Stakeholders |
| Participant communication sent | Day 45 | [ ] | Research Coordinator |

---

**Plan Version**: 1.0
**Last Updated**: 2025-11-04
**Approval**: [Pending IRB, School District, Research Team]
