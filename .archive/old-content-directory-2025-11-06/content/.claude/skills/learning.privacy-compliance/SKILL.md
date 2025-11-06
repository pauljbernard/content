# Data Privacy Compliance for Educational Platforms

**Skill**: `/learning.privacy-compliance`
**Category**: Compliance & Legal
**Addresses**: GAP-20 (CRITICAL)
**Purpose**: Ensure curriculum platforms comply with FERPA, COPPA, GDPR, and CCPA for educational data privacy

## Description

Comprehensive data privacy compliance validation for EdTech platforms serving K-12 schools, universities, and international markets. Validates curriculum materials, platform features, and data practices against federal and state privacy regulations.

## Usage

```bash
/learning.privacy-compliance \
  --target "curriculum|platform|data-practices" \
  --regulations "FERPA,COPPA,GDPR,CCPA" \
  --student-age-range "under-13|13-17|18-plus|all" \
  --geographic-scope "US|EU|California|international" \
  --assessment-type "self-assessment|audit|certification"
```

## Regulatory Frameworks

### 1. FERPA (Family Educational Rights and Privacy Act)

**Scope**: U.S. educational institutions receiving federal funding

**Key Requirements**:
- Protect student education records
- Obtain parental consent before disclosing PII
- Allow parents to inspect and request amendments
- Annual notification of FERPA rights

**Curriculum Compliance Checks**:
- ✅ No embedded tracking pixels in digital materials
- ✅ No third-party analytics collecting student data
- ✅ Assessment data stored with proper safeguards
- ✅ Parent consent forms for data collection
- ✅ Directory information clearly designated
- ✅ Data retention policies (max 7 years post-graduation)

**Platform Compliance Checks**:
- ✅ Role-based access control (teachers, parents, students)
- ✅ Audit logs for who accessed student records
- ✅ Encryption at rest and in transit
- ✅ Data processing agreements with vendors
- ✅ Annual security training for staff
- ✅ Breach notification procedures (<72 hours)

### 2. COPPA (Children's Online Privacy Protection Act)

**Scope**: U.S. websites/services directed at children under 13

**Key Requirements**:
- Obtain verifiable parental consent
- Provide clear privacy policy in plain language
- No conditioning service on unnecessary data collection
- Allow parents to review/delete child's information
- Maintain reasonable data security

**Curriculum Compliance Checks**:
- ✅ Age gate before data collection (<13 requires consent)
- ✅ Privacy policy readable by 8-year-olds (Flesch-Kincaid Grade 3-4)
- ✅ No persistent identifiers in cookies/local storage
- ✅ No behavioral advertising to children
- ✅ Parental consent mechanism (credit card, video conference, etc.)
- ✅ "Kid-friendly" privacy policy with illustrations

**Platform Compliance Checks**:
- ✅ Verifiable parental consent (VPC) mechanism
- ✅ Data minimization (collect only what's needed for education)
- ✅ No sale of child data to third parties
- ✅ Teacher exception properly documented (COPPA exemption for school-authorized use)
- ✅ Parental access portal (view/delete child data)
- ✅ FTC-approved safe harbor certification (e.g., iKeepSafe, PRIVO)

### 3. GDPR (General Data Protection Regulation)

**Scope**: European Union residents (data subjects)

**Key Requirements**:
- Lawful basis for processing (consent, contract, legitimate interest)
- Data protection by design and by default
- Right to access, rectification, erasure ("right to be forgotten")
- Right to data portability
- Data Protection Impact Assessment (DPIA) for high-risk processing
- Appoint Data Protection Officer (DPO) if required

**Curriculum Compliance Checks**:
- ✅ Privacy notices in EU languages (23 official languages)
- ✅ Explicit consent for non-essential cookies
- ✅ Data portability format (JSON, CSV)
- ✅ Automated deletion workflows (right to erasure)
- ✅ Purpose limitation (use data only for stated purpose)
- ✅ Cross-border transfer mechanisms (Standard Contractual Clauses)

**Platform Compliance Checks**:
- ✅ Cookie consent banner (granular opt-in)
- ✅ Privacy by design in platform architecture
- ✅ DPIA completed for automated decision-making
- ✅ DPO appointed (if processing at scale)
- ✅ Records of processing activities (Article 30)
- ✅ Data breach notification (72 hours to supervisory authority)
- ✅ EU representative appointed (if no EU establishment)

### 4. CCPA (California Consumer Privacy Act) / CPRA

**Scope**: California residents (expanded to businesses with CA customers)

**Key Requirements**:
- Notice of collection at or before data collection
- Right to know what data is collected
- Right to delete personal information
- Right to opt out of sale/sharing
- Right to correct inaccurate data (CPRA addition)
- No discrimination for exercising rights

**Curriculum Compliance Checks**:
- ✅ "Do Not Sell My Personal Information" link (if selling data)
- ✅ Privacy policy with CCPA-specific disclosures
- ✅ Data category disclosures (12 categories)
- ✅ Retention period justifications
- ✅ Consumer rights request mechanism
- ✅ Authorized agent support

**Platform Compliance Checks**:
- ✅ Consumer rights portal (request access, deletion, opt-out)
- ✅ Request verification process (2-3 piece matching)
- ✅ 45-day response timeline (15-day extension if needed)
- ✅ No retaliation for exercising rights
- ✅ Annual privacy metrics report (requests received, compliance rate)
- ✅ Sensitive personal information notice (CPRA)

## Compliance Assessment

### Self-Assessment Checklist

**FERPA Compliance** (20 checks):
- [ ] PII definition documented (name, SSN, student ID, biometric)
- [ ] Education records inventory maintained
- [ ] Directory information policy published
- [ ] Annual FERPA notice sent to parents
- [ ] Consent forms for non-directory disclosures
- [ ] Legitimate educational interest defined
- [ ] Third-party agreements include FERPA requirements
- [ ] Audit logs capture all record access
- [ ] Parent/eligible student access procedures
- [ ] Amendment request process documented
- [ ] Complaint procedures published
- [ ] Data retention schedule (3-7 years typical)
- [ ] Secure destruction procedures
- [ ] Breach notification plan
- [ ] Staff training on FERPA (annual)
- [ ] Ex-employee access revoked (within 24 hours)
- [ ] Court order/subpoena procedures
- [ ] Health/safety emergency exception documented
- [ ] Redisclosure prohibitions in agreements
- [ ] FERPA compliance officer designated

**COPPA Compliance** (15 checks):
- [ ] Age gate before any data collection
- [ ] Privacy policy link on homepage
- [ ] Privacy policy updated within 12 months
- [ ] Clear notice of data collection practices
- [ ] Parental consent mechanism (verifiable)
- [ ] Parent email notification after consent
- [ ] Parent access to child's data (within 10 days)
- [ ] Parent deletion requests honored (within 30 days)
- [ ] Data security safeguards documented
- [ ] No conditioning on unnecessary data
- [ ] No behavioral advertising to kids
- [ ] Third-party data sharing disclosed
- [ ] Safe harbor certification current
- [ ] Teacher exception properly applied
- [ ] FTC complaint response procedures

**GDPR Compliance** (25 checks):
- [ ] Lawful basis identified for each processing activity
- [ ] Privacy notice provided at data collection
- [ ] Explicit consent obtained (opt-in, not opt-out)
- [ ] Consent withdrawal mechanism available
- [ ] Data subject rights procedures (access, rectification, erasure, etc.)
- [ ] Data portability format defined
- [ ] DPIA completed for high-risk processing
- [ ] DPO appointed (if required)
- [ ] Records of processing activities maintained
- [ ] Data retention periods justified
- [ ] Automated deletion workflows implemented
- [ ] Cross-border transfer mechanisms (SCCs, BCRs)
- [ ] Vendor data processing agreements (Article 28)
- [ ] Breach notification procedures (72 hours)
- [ ] Security measures documented (encryption, access controls)
- [ ] Privacy by design in system architecture
- [ ] Cookie consent (granular, opt-in)
- [ ] Profiling/automated decision-making safeguards
- [ ] Child consent age thresholds (13-16 depending on member state)
- [ ] EU representative appointed (if outside EU)
- [ ] Supervisory authority liaison identified
- [ ] Data protection training for staff
- [ ] Privacy impact reviews for new features
- [ ] User-friendly rights request forms
- [ ] Annual GDPR compliance audit

**CCPA Compliance** (18 checks):
- [ ] Privacy policy updated with CCPA disclosures
- [ ] Notice at collection provided
- [ ] Data categories disclosed (12 categories)
- [ ] Business purposes for collection disclosed
- [ ] Third-party sharing disclosed
- [ ] Sale of personal information disclosed (if applicable)
- [ ] "Do Not Sell" link on homepage (if selling)
- [ ] Consumer rights request mechanism
- [ ] Request verification process (2-3 piece)
- [ ] Access requests fulfilled (within 45 days)
- [ ] Deletion requests fulfilled (within 45 days)
- [ ] Opt-out requests honored (within 15 days)
- [ ] No discrimination for exercising rights
- [ ] Authorized agent process supported
- [ ] Right to correct implemented (CPRA)
- [ ] Sensitive PI notice (CPRA)
- [ ] Annual privacy metrics tracked
- [ ] Service provider agreements include CCPA terms

### Automated Audit

Scans curriculum and platform for privacy issues.

```bash
/learning.privacy-compliance \
  --action "audit" \
  --target "platform" \
  --regulations "FERPA,COPPA,GDPR,CCPA" \
  --output "audit-report-2025-11-02.pdf"
```

**Automated Checks**:
- Web page scanning for privacy policy links
- Cookie/tracker detection (third-party analytics)
- Data flow analysis (where does student data go?)
- Encryption validation (TLS 1.2+, AES-256)
- Access control testing (unauthorized access attempts)
- Data retention policy verification
- Consent form language analysis (readability, clarity)
- Third-party vendor agreements review

**Output**: Compliance scorecard (0-100% per regulation)

### Certification Preparation

Prepares documentation for privacy certifications.

**Certifications**:
- **iKeepSafe COPPA Safe Harbor**
- **iKeepSafe FERPA Certification**
- **Student Privacy Pledge (Future of Privacy Forum)**
- **ISO 27001** (information security)
- **SOC 2 Type II** (security, availability, confidentiality)
- **GDPR Certification** (via approved bodies)

```bash
/learning.privacy-compliance \
  --action "prepare-certification" \
  --certification "iKeepSafe-COPPA" \
  --target "platform" \
  --output "certification-package/"
```

**Output**:
- Evidence bundle (policies, procedures, technical documentation)
- Gap analysis vs. certification requirements
- Remediation roadmap for gaps
- Attestation letters
- Audit logs demonstrating compliance

## Privacy-First Curriculum Design

### Data Minimization

**Principle**: Collect only data necessary for educational purpose.

**Curriculum Guidelines**:
- ✅ Use anonymous IDs instead of names for practice activities
- ✅ Aggregate analytics (class-level, not individual-level)
- ✅ Optional profile fields (don't require birthday if not needed)
- ✅ Temporary session data (delete after logout)
- ✅ No embedded social media widgets (privacy leak)

### Privacy by Design

**Principle**: Build privacy into system architecture from day one.

**Platform Guidelines**:
- ✅ Default settings are most privacy-protective
- ✅ Encryption at rest (AES-256) and in transit (TLS 1.3)
- ✅ Role-based access control (least privilege principle)
- ✅ Separate databases for PII vs. non-PII
- ✅ Pseudonymization where possible
- ✅ Data anonymization for analytics
- ✅ Regular penetration testing (quarterly)
- ✅ Bug bounty program for vulnerability disclosure

### Transparency

**Principle**: Clear communication about data practices.

**Communication Guidelines**:
- ✅ Privacy policy in plain language (Flesch-Kincaid Grade 8)
- ✅ Layered privacy notices (short + long versions)
- ✅ Privacy center with FAQs
- ✅ Privacy icons (visual representations)
- ✅ Annual privacy transparency reports
- ✅ Proactive breach notifications (even when not legally required)

## Use Cases

### Use Case 1: EdTech Startup Launch Compliance

**Scenario**: LearnFlow launching adaptive platform for K-12 (ages 5-18).

```bash
/learning.privacy-compliance \
  --action "self-assessment" \
  --target "platform" \
  --regulations "FERPA,COPPA,CCPA" \
  --student-age-range "all" \
  --geographic-scope "US"
```

**Output**:
- Compliance scorecard: FERPA 78%, COPPA 45%, CCPA 82%
- **Critical gaps**:
  - ❌ No verifiable parental consent for <13 (COPPA blocker)
  - ❌ No data retention policy (FERPA gap)
  - ⚠️ Privacy policy too complex (Grade 12 reading level)
- **Remediation**: 3 months to implement VPC and simplify policy

### Use Case 2: International Expansion (GDPR)

**Scenario**: U.S. publisher expanding to EU market.

```bash
/learning.privacy-compliance \
  --action "gap-analysis" \
  --current-compliance "FERPA,COPPA" \
  --target-compliance "GDPR" \
  --geographic-scope "EU"
```

**Output**:
- GDPR gaps: 18 items
- **Critical**:
  - Must appoint EU representative
  - Must implement right to erasure
  - Must complete DPIA for automated grading
  - Must revise privacy policy (explicit consent, not implied)
- **Timeline**: 6 months for full GDPR compliance
- **Cost estimate**: $50K (legal, technical, organizational changes)

### Use Case 3: COPPA Certification Application

**Scenario**: Assessment company seeking iKeepSafe COPPA Safe Harbor.

```bash
/learning.privacy-compliance \
  --action "prepare-certification" \
  --certification "iKeepSafe-COPPA" \
  --target "platform" \
  --evidence-bundle true
```

**Output**:
- Evidence bundle (28 documents):
  - Privacy policy (kid-friendly version)
  - Parental consent flow diagrams
  - Data retention policy
  - Security safeguards documentation
  - Vendor agreements (with COPPA terms)
  - Penetration test reports
  - Staff training records
- Gap analysis: 2 minor gaps
- Timeline: 2 months to certification

### Use Case 4: Privacy Incident Response

**Scenario**: Unauthorized access to student records (data breach).

```bash
/learning.privacy-compliance \
  --action "breach-response" \
  --incident-type "unauthorized-access" \
  --records-affected 1247 \
  --data-types "name,email,grades" \
  --regulations "FERPA,GDPR"
```

**Output**:
- Breach notification timeline:
  - Hour 0: Contain breach, revoke access
  - Hour 4: Assess scope and severity
  - Hour 12: Notify DPO and legal counsel
  - Hour 72: Notify GDPR supervisory authority (required)
  - Day 7: Notify affected parents (FERPA best practice)
- Notification templates (FERPA, GDPR-compliant)
- Remediation steps
- Post-incident report

## Implementation

### Technology Components

**Privacy Management Platform**:
- Consent management (OneTrust, TrustArc, Cookiebot)
- Data mapping and inventory (BigID, OneTrust)
- Data subject rights automation (Securiti, DataGrail)
- Privacy policy generator (Termly, iubenda)

**Security Tools**:
- Encryption: AES-256 (at rest), TLS 1.3 (in transit)
- Access control: OAuth 2.0, RBAC
- Audit logging: Splunk, ELK Stack
- Vulnerability scanning: Nessus, Qualys
- Penetration testing: HackerOne, Bugcrowd

**Compliance Monitoring**:
- Cookie scanner: OneTrust, Cookiebot
- Data flow mapping: BigID, Egnyte
- Privacy impact assessment: OneTrust, TrustArc
- Vendor risk management: SecurityScorecard, BitSight

### Integration with Agents

- **Quality Assurance Agent**: Runs privacy compliance check before release
- **Curriculum Architect Agent**: Embeds privacy by design principles
- **Content Developer Agent**: Validates no unnecessary data collection in activities

## Performance Metrics

- **Compliance score**: 95%+ across all applicable regulations
- **Incident response time**: <72 hours to notification
- **Data subject request response**: <30 days (GDPR), <45 days (CCPA)
- **Staff training completion**: 100% annually
- **Audit findings**: Zero critical findings in annual audit

## Success Criteria

- ✅ Zero regulatory fines or penalties
- ✅ Privacy certification maintained (iKeepSafe, Student Privacy Pledge)
- ✅ 100% of school districts accept privacy terms
- ✅ Parent satisfaction with data practices >90%
- ✅ Zero data breaches compromising student PII

---

**Status**: Ready for implementation
**Dependencies**: Privacy management platform (OneTrust or equivalent), legal counsel review
**Testing**: Requires test with school district privacy officer review
**Legal Note**: This skill provides technical compliance checks but requires legal counsel for final validation
