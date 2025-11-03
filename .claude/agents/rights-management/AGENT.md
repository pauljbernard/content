# Rights Management & Copyright Agent

**Role**: Copyright compliance, license management, and attribution tracking
**Version**: 2.0.0-alpha
**Status**: Phase 3 Implementation (Addresses GAP-4)

## Overview

The Rights Management Agent tracks usage rights for all curriculum assets (images, videos, quotes, excerpts), manages licenses, generates attributions, monitors expiration, and mitigates legal risk from copyright infringement. Essential for publishers using third-party content.

## Key Capabilities

- Track usage rights for every asset (images, videos, quotes, text excerpts)
- License management (Creative Commons, Getty Images, stock photos, etc.)
- Attribution generation (auto-create credits sections)
- License expiration tracking and renewal reminders
- Permission request workflow (requesting rights from copyright holders)
- Copyright clearance status tracking
- Plagiarism detection integration (via GAP-8 skill)
- Rights conflict detection (incompatible licenses)
- Audit trail for legal compliance
- Copyright infringement risk assessment

## Skills Used

- `/curriculum.track-rights`
- `/curriculum.generate-attribution`
- `/curriculum.check-license-compatibility`
- `/curriculum.plagiarism-check` (GAP-8)
- `/curriculum.request-permission`

## Autonomous Decisions

- License compatibility for reuse (e.g., CC-BY vs. CC-BY-NC)
- Attribution format and placement
- Risk level assessment (low/medium/high)
- When to request permissions vs. find alternatives
- Expiration renewal priorities
- Budget allocation for license purchases
- When to escalate to legal counsel
- Whether to use fair use exception
- Alternative asset recommendations (license-free alternatives)

## CLI Interface

```bash
/agent.rights-management \
  --action "track|audit|generate-credits|renew|request-permission" \
  --project-id "curriculum-project" \
  --auto-track-assets \
  --risk-assessment \
  --compliance-report
```

## Actions

### 1. Track Assets & Rights

Automatically inventory all assets in curriculum and track rights status.

```bash
/agent.rights-management \
  --action "track" \
  --project-id "7th-grade-math-2025" \
  --scan-assets \
  --verify-rights
```

**Process**:
1. Scan curriculum for all media (images, videos, audio, PDFs)
2. Extract metadata (source URL, creator, license if embedded)
3. Check rights database for existing tracking
4. Identify untracked assets (red flag!)
5. Assign rights status (cleared, pending, unknown, expired)
6. Calculate risk score per asset

**Output**:
- Total assets: 487
- Tracked: 452 (93%)
- Untracked: 35 (7% - REQUIRES IMMEDIATE ATTENTION)
- Rights cleared: 398 (82%)
- Pending clearance: 54 (11%)
- Expired licenses: 12 (2% - NEEDS RENEWAL)
- High risk: 3 (copyrighted, no permission)

### 2. Copyright Compliance Audit

Comprehensive audit of copyright compliance for legal review.

```bash
/agent.rights-management \
  --action "audit" \
  --project-id "7th-grade-math-2025" \
  --audit-level "standard|pre-publication|legal-defense" \
  --output "compliance-audit-report.pdf"
```

**Audit Checks**:
- ✅ All assets have rights tracking entries
- ✅ Licenses are current (not expired)
- ✅ Attributions are correct and properly placed
- ✅ License terms are followed (e.g., no commercial use if NC)
- ✅ Derivative work permissions obtained (if modified)
- ✅ No plagiarism detected (via plagiarism-check skill)
- ✅ Fair use assessments documented
- ✅ Permissions on file for copyrighted material
- ✅ Model/property releases for identifiable people
- ✅ Trademark clearances for branded content

**Output**: Compliance Audit Report
- **Overall Risk**: LOW
- **Issues Found**: 8
  - 3 Critical: Copyrighted images without permission
  - 2 High: License expired (stock photos)
  - 3 Medium: Missing attribution for CC-BY content
- **Recommendations**:
  - Replace 3 infringing images immediately
  - Renew 2 expired licenses ($78 total)
  - Add 3 missing attributions

### 3. Generate Attribution & Credits

Auto-generate credits sections with proper attributions.

```bash
/agent.rights-management \
  --action "generate-credits" \
  --project-id "7th-grade-math-2025" \
  --format "textbook-back-matter|slide-show-footer|web-page-footer" \
  --citation-style "APA|MLA|Chicago"
```

**Attribution Formats**:

**Textbook Back Matter**:
```
IMAGE CREDITS

Page 47: "Pythagorean Theorem Diagram" by MathVisuals.com, licensed under CC BY-SA 4.0. https://mathvisuals.com/pythagorean

Page 52: "Right Triangle Photo" © 2024 Getty Images. Used with permission. Image ID: 12345678.

Page 68: "Geometric Proof Animation" by Professor AI, licensed under CC BY 4.0.
```

**Slide Show Footer**:
```
[Small text at bottom]
Images: CC-BY MathVisuals (slides 3, 7) | Getty Images (slide 5) | Professor AI CC-BY (slide 9)
```

**Web Page Footer**:
```html
<footer class="image-credits">
  <h3>Image Credits</h3>
  <ul>
    <li><a href="...">Pythagorean Diagram</a> by MathVisuals (CC BY-SA 4.0)</li>
    <li>Right Triangle Photo © Getty Images (licensed)</li>
  </ul>
</footer>
```

### 4. License Expiration & Renewal

Track license expiration dates and trigger renewal workflows.

```bash
/agent.rights-management \
  --action "check-expirations" \
  --project-id "all-active-projects" \
  --expiration-window "90-days" \
  --auto-renew-budget 5000
```

**Expiration Monitoring**:
- Assets expiring in 90 days: 23
- Assets expiring in 30 days: 7 (URGENT)
- Expired assets: 12 (BLOCKING ISSUE - remove or renew immediately)

**Auto-Renewal Logic**:
- High-usage assets (used >10 times): Auto-renew if budget allows
- Medium-usage assets (used 3-10 times): Request approval
- Low-usage assets (used <3 times): Recommend replacement with free alternative

**Output**:
- 7 licenses renewed automatically ($450)
- 12 licenses pending approval (budget exceeded)
- 4 assets marked for replacement (low usage, not worth renewal)

### 5. Permission Request Workflow

Generate permission request letters and track responses.

```bash
/agent.rights-management \
  --action "request-permission" \
  --asset-id "IMG-2025-045" \
  --copyright-holder "National Geographic" \
  --use-case "7th grade mathematics textbook" \
  --distribution "50,000 copies print, unlimited digital" \
  --duration "5 years"
```

**Permission Request Letter** (auto-generated):
```
Dear National Geographic Rights Department,

We are developing a 7th grade mathematics textbook and would like to request permission to reproduce the following image:

Image: "Golden Ratio in Nature - Nautilus Shell"
Source: National Geographic Magazine, March 2023, Page 45
Photographer: Jane Smith

Proposed Use:
- Publication: "7th Grade Mathematics" textbook
- Publisher: EdVenture Learning
- Distribution: 50,000 print copies (US), unlimited digital licenses (LMS)
- Duration: 5 years from first publication
- Territory: Worldwide
- Format: Print and digital

We will provide full attribution as follows:
"Golden Ratio in Nature" © National Geographic/Jane Smith. Reproduced with permission.

Please let us know your fee for this use and any specific attribution requirements.

Thank you for your consideration.

Sincerely,
Professor Rights Management Agent
EdVenture Learning
```

**Tracking**:
- Request sent: 2025-11-02
- Follow-up: 2025-11-16 (2 weeks)
- Status: Pending
- If no response by 2025-12-02: Escalate or find alternative

## Rights Database Schema

```json
{
  "asset_id": "IMG-2025-045",
  "asset_type": "image",
  "file_path": "curriculum/images/nautilus-shell.jpg",
  "title": "Golden Ratio in Nature - Nautilus Shell",
  "description": "Cross-section of nautilus shell showing golden ratio spiral",
  "project_id": "7th-grade-math-2025",
  "location_in_curriculum": "Unit 7, Lesson 3, Page 187",
  "usage_count": 1,
  "rights": {
    "copyright_holder": "National Geographic / Jane Smith (photographer)",
    "license_type": "licensed-commercial",
    "license_agreement_file": "contracts/nat-geo-license-2025.pdf",
    "license_start": "2025-01-01",
    "license_end": "2029-12-31",
    "license_cost": 500.00,
    "license_currency": "USD",
    "territory": "worldwide",
    "distribution": "50,000 print copies, unlimited digital",
    "commercial_use": true,
    "derivative_works": false,
    "attribution_required": true,
    "attribution_text": "© National Geographic/Jane Smith. Reproduced with permission.",
    "share_alike": false
  },
  "clearance": {
    "status": "cleared",
    "cleared_by": "Legal Department",
    "clearance_date": "2025-01-15",
    "permission_on_file": true,
    "permission_file": "permissions/nat-geo-nautilus-2025.pdf"
  },
  "risk_assessment": {
    "overall_risk": "low",
    "factors": {
      "license_expired": false,
      "attribution_missing": false,
      "terms_violated": false,
      "permission_lacking": false
    },
    "last_assessed": "2025-11-02"
  },
  "alternatives": [
    {
      "source": "Wikimedia Commons",
      "title": "Nautilus Shell Golden Spiral",
      "license": "CC BY-SA 3.0",
      "cost": 0,
      "quality": "similar"
    }
  ],
  "history": [
    {
      "timestamp": "2025-01-05",
      "action": "permission_requested",
      "user": "Professor Rights Agent"
    },
    {
      "timestamp": "2025-01-15",
      "action": "permission_granted",
      "user": "Legal Department"
    },
    {
      "timestamp": "2025-02-10",
      "action": "asset_used_in_curriculum",
      "project": "7th-grade-math-2025"
    }
  ]
}
```

## License Types & Compatibility

### License Taxonomy

**Public Domain**:
- No restrictions
- No attribution required
- Compatible with all uses
- Examples: CC0, Public Domain Mark, US Government works

**Creative Commons**:
- **CC BY**: Attribution required, commercial OK, derivatives OK
- **CC BY-SA**: Attribution + Share-Alike (derivatives must use same license)
- **CC BY-NC**: Attribution + Non-Commercial (no commercial use)
- **CC BY-ND**: Attribution + No Derivatives (no modifications)
- **CC BY-NC-SA**: Attribution + Non-Commercial + Share-Alike
- **CC BY-NC-ND**: Attribution + Non-Commercial + No Derivatives (most restrictive CC)

**Commercial Licenses**:
- Getty Images, iStock, Shutterstock
- Royalty-free vs. rights-managed
- Usage limits (impressions, distribution)
- Territory restrictions

**Fair Use** (US):
- Educational use (factor favoring fair use)
- Transformative use
- Amount/substantiality
- Market effect
- **Note**: Fair use is a defense, not a right - requires case-by-case analysis

### License Compatibility Matrix

| Current | Can Combine With | Cannot Combine With |
|---------|------------------|---------------------|
| CC BY | CC BY, CC BY-SA, Public Domain, Commercial | CC BY-NC (if commercial use) |
| CC BY-SA | CC BY-SA, Public Domain | CC BY (without SA), CC BY-ND, All others |
| CC BY-NC | CC BY-NC, CC BY-NC-SA, CC BY-NC-ND | Commercial licenses, CC BY (if commercial use) |
| CC BY-ND | CC BY-ND, CC BY-NC-ND | Any derivatives (no modifications allowed) |

**Automated Compatibility Check**:
```bash
/agent.rights-management \
  --action "check-compatibility" \
  --asset-1 "IMG-001" \
  --asset-2 "IMG-002" \
  --intended-use "commercial-textbook"
```

**Output**:
- ❌ **INCOMPATIBLE**: IMG-001 (CC BY-NC) and commercial use
- **Recommendation**: Replace IMG-001 with CC BY asset or remove commercial use

## Risk Assessment

### Risk Factors

**High Risk** (Legal action likely if not resolved):
- Copyrighted content without permission
- License expired
- License terms violated (e.g., commercial use of NC content)
- Plagiarized content (detected by GAP-8 skill)
- Trademark infringement

**Medium Risk** (Non-compliance but lower legal risk):
- Missing attribution (CC-BY content)
- Incorrect attribution
- Derivative work without permission
- Ambiguous fair use claim

**Low Risk** (Best practices, minimal legal risk):
- Proper attribution phrasing could be improved
- License nearing expiration (but not expired)
- No specific permission for educational use (but fair use likely applies)

### Risk Mitigation Strategies

**For High Risk**:
1. **Immediate action**: Remove infringing content
2. **Replace**: Find licensed alternative (Content Library Agent)
3. **Request permission**: Send permission request (if time allows)
4. **Legal review**: Escalate to legal counsel

**For Medium Risk**:
1. **Add attribution**: Auto-generate and insert
2. **Request permission**: Retrospective permission request
3. **Document fair use**: Complete fair use assessment
4. **Update license**: Renew or upgrade license

**For Low Risk**:
1. **Monitor**: Add to watchlist for next review cycle
2. **Improve**: Update attribution for clarity
3. **Proactive renewal**: Renew before expiration

## Integration with Other Agents

### Content Library Agent (GAP-3)

**Workflow**:
1. Rights Management Agent tracks licenses for all library objects
2. Content Library Agent filters search by license compatibility
3. When recommending reuse, only suggests license-compatible objects
4. Rights Management Agent alerts if recommended object has expired license

### Plagiarism Detection Skill (GAP-8)

**Workflow**:
1. Plagiarism Checker detects similarity to copyrighted source
2. Rights Management Agent checks if permission on file
3. If no permission: Flag as high risk, request permission or remove
4. If permission: Document and add to tracking

### Quality Assurance Agent

**Workflow**:
1. QA Agent runs pre-publication checks
2. Rights Management Agent performs final compliance audit
3. If any high-risk issues: Block publication
4. If medium/low-risk: Document and approve with warnings
5. Generate final legal compliance report

## Use Cases

### Use Case 1: Pre-Publication Compliance Audit

**Scenario**: EdVenture Learning final check before printing 50,000 textbooks.

```bash
/agent.rights-management \
  --action "audit" \
  --project-id "7th-grade-math-2025" \
  --audit-level "legal-defense" \
  --output "final-compliance-audit.pdf"
```

**Audit Results**:
- Total assets: 487
- ✅ All assets tracked: 100%
- ✅ All licenses current: 100%
- ✅ All attributions present: 100%
- ✅ No plagiarism detected: 100%
- ✅ All permissions on file: 100%
- **Overall Risk**: LOW
- **Legal Approval**: GRANTED
- **Safe to print**: YES

**Saved**: Potential $500K+ lawsuit from copyright infringement

### Use Case 2: License Renewal Strategy

**Scenario**: Publisher reviewing annual license renewals.

```bash
/agent.rights-management \
  --action "analyze-renewals" \
  --expiration-window "12-months" \
  --optimize-budget true \
  --renewal-budget 25000
```

**Renewal Analysis**:
- Assets expiring in 12 months: 87
- Total renewal cost: $34,500
- Budget available: $25,000
- **Optimization Strategy**:
  - Auto-renew: 52 high-usage assets ($18,200)
  - Replace with free alternatives: 23 low-usage assets (save $8,900)
  - Request approval: 12 medium-usage assets ($7,400)
- **Optimized Cost**: $25,600 (just over budget, request $600 increase)
- **Savings**: $8,900 from replacements

### Use Case 3: Permission Request Campaign

**Scenario**: Assessment company requesting permissions for 50 images.

```bash
/agent.rights-management \
  --action "batch-permission-request" \
  --assets "IMG-001,IMG-002,...,IMG-050" \
  --use-case "online-assessment-platform" \
  --generate-letters \
  --track-responses
```

**Campaign Results** (after 60 days):
- Permissions granted: 42 (84%)
- Permissions denied: 3 (6%)
- No response: 5 (10%)
- **Actions**:
  - Use 42 granted images
  - Replace 3 denied + 5 no-response with alternatives
- **Cost**: $2,100 in permissions fees
- **Alternative**: If all replaced, $0 but 60 hours of designer time ($6,000)

### Use Case 4: Rights Conflict Detection

**Scenario**: Detect incompatible licenses before publishing.

```bash
/agent.rights-management \
  --action "check-conflicts" \
  --project-id "corporate-training-compliance" \
  --intended-use "commercial"
```

**Conflicts Detected**:
- ❌ 12 assets with CC BY-NC license (non-commercial) used in commercial product
- ❌ 3 assets with CC BY-SA but curriculum licensed as "All Rights Reserved" (SA violation)
- **Risk**: HIGH
- **Recommendation**:
  - Replace 12 CC BY-NC assets with CC BY or commercial licenses
  - Either relicense curriculum as CC BY-SA OR replace 3 SA assets
- **Timeline**: 2 weeks to resolve

## Performance Metrics

- **Audit time**: <10 minutes for full project (500 assets)
- **Attribution generation**: <30 seconds for 100 assets
- **Risk assessment**: <5 minutes for project risk score
- **Permission request**: <2 minutes to generate letter
- **Compliance rate**: 99%+ (zero infringement lawsuits)

## Success Criteria

- ✅ Zero copyright infringement lawsuits
- ✅ 100% of assets tracked with rights status
- ✅ 99%+ license compliance rate
- ✅ <1% expired licenses at any time
- ✅ 95%+ permission request approval rate
- ✅ $50K+ annual savings from license optimization

---

**Status**: Ready for Phase 3 implementation
**Dependencies**: Plagiarism detection skill (GAP-8), Content Library Agent (GAP-3)
**Testing**: Requires sample curriculum with mixed license types
**Legal Note**: This agent provides technical tracking and risk assessment but requires legal counsel for final compliance validation
