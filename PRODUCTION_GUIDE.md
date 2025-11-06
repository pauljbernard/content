# Production Guide
**HMH Multi-Curriculum Knowledge Base - For Publishers and Production Staff**
**Version:** 1.0
**Last Updated:** November 6, 2025

---

## Welcome to Production

As part of the production team, you transform approved content into polished, multi-format deliverables ready for distribution to teachers and students.

You ensure content is professionally formatted, accessible, and delivered in all required formats across multiple platforms.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Publishing Workflow](#2-publishing-workflow)
3. [Multi-Format Production](#3-multi-format-production)
4. [Asset Management](#4-asset-management)
5. [Quality Assurance](#5-quality-assurance)
6. [Delivery and Distribution](#6-delivery-and-distribution)

---

## 1. Getting Started

### Your Responsibilities

**Content Formatting:**
- Apply consistent styling
- Ensure brand compliance
- Prepare for various outputs

**Multi-Format Production:**
- PDF for print
- Interactive HTML for digital
- SCORM packages for LMS
- Accessible formats

**Asset Management:**
- Organize images, videos, audio
- Optimize for web and print
- Ensure licensing compliance

**Quality Assurance:**
- Final technical review
- Cross-format consistency
- Accessibility validation

**Distribution:**
- Package for delivery
- Upload to platforms
- Coordinate with stakeholders

### Your Tools

- **Pandoc** - Markdown to PDF/HTML conversion
- **LaTeX** - PDF typesetting
- **HTML/CSS/JS** - Interactive content
- **SCORM Tools** - LMS packaging
- **Git/GitHub** - Version control
- **Asset Optimization** - ImageMagick, FFmpeg

### Directory Structure

```
content/
├── published/              # Approved content (input)
│   ├── lessons/
│   ├── assessments/
│   └── activities/
├── production/             # Work area
│   ├── pdf/
│   ├── html/
│   ├── scorm/
│   └── accessible/
├── dist/                   # Final deliverables (output)
│   ├── pdf/
│   ├── html/
│   ├── scorm/
│   └── accessible/
└── assets/                 # Media library
    ├── images/
    ├── videos/
    └── audio/
```

---

## 2. Publishing Workflow

### End-to-End Process

```
1. Content Approved → Moved to /published/
   ↓
2. Production receives notification
   ↓
3. Review technical specifications
   ↓
4. Format and style content
   ↓
5. Produce multi-format outputs
   ↓
6. Assemble and optimize assets
   ↓
7. Quality assurance checks
   ↓
8. Package for distribution
   ↓
9. Upload/deliver to platforms
   ↓
10. Confirm successful delivery
```

**Timeline:** 2-5 days depending on complexity

### Step-by-Step

**Step 1: Receive Approved Content**
- GitHub notification of merge to `/published/`
- Review content brief and metadata
- Identify required formats
- Note timeline and platform requirements

**Step 2: Technical Specifications Review**
- Check file completeness
- Verify asset specifications
- Note special requirements
- Identify potential issues

**Step 3: Format Content**
- Apply templates and styles
- Prepare for each output format
- Ensure brand compliance

**Step 4: Produce Outputs**
- Generate PDF
- Create interactive HTML
- Build SCORM package
- Create accessible formats

**Step 5: QA and Package**
- Run QA checklist
- Package for delivery
- Create documentation

**Step 6: Deliver**
- Upload to platforms
- Notify stakeholders
- Confirm receipt

---

## 3. Multi-Format Production

### Format 1: PDF Production

**Use Cases:**
- Teacher guides (print/digital)
- Student workbooks (print)
- Assessments (print)
- Handouts

**Workflow:**

**Step 1: Prepare Content**
```bash
cd /published/lessons/hmh-math-tx/grade-5/fractions-lesson/

# Files:
# - teacher-guide.md
# - student-pages.md
# - assets/
```

**Step 2: Convert to PDF**
```bash
pandoc teacher-guide.md \
  --template=templates/hmh-teacher-guide.latex \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize:11pt \
  -V colorlinks:true \
  -o production/pdf/teacher-guide.pdf
```

**Step 3: Apply Brand Styles**
- HMH colors, fonts, logos
- Consistent headers/footers
- Page numbering

**Step 4: Quality Check**
- [ ] All pages render correctly
- [ ] No broken image links
- [ ] TOC accurate
- [ ] Page numbers sequential
- [ ] Headers/footers consistent
- [ ] No widows/orphans

**Deliverable:** `teacher-guide.pdf`, `student-pages.pdf`

---

### Format 2: Interactive HTML

**Use Cases:**
- Digital lessons
- Interactive activities
- Online assessments
- Teacher resource websites

**Workflow:**

**Step 1: Convert to HTML**
```bash
pandoc teacher-guide.md \
  --template=templates/hmh-interactive.html \
  --css=css/hmh-styles.css \
  --mathjax \
  --self-contained \
  -o production/html/teacher-guide.html
```

**Step 2: Add Interactive Elements**
```html
<!-- Interactive fraction model -->
<div class="interactive-fraction-model"
     data-numerator="2"
     data-denominator="3">
  <script src="https://cdn.hmhco.com/components/fraction-model.js"></script>
</div>
```

**Step 3: Ensure Responsive Design**
```css
@media (max-width: 768px) {
  .lesson-content {
    font-size: 1.1em;
    padding: 10px;
  }
}
```

**Step 4: Accessibility Enhancements**
- Semantic HTML5
- ARIA labels
- Keyboard navigation
- Skip links

**Step 5: Quality Check**
- [ ] Renders on desktop (Chrome, Firefox, Safari, Edge)
- [ ] Renders on tablet (iPad, Android)
- [ ] Renders on phone
- [ ] Interactive elements function
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

**Deliverable:** `teacher-guide.html`, `student-pages.html` + assets

---

### Format 3: SCORM Packages

**Use Cases:**
- LMS integration (Canvas, Moodle, Blackboard)
- Track student progress
- Grade passback

**Structure:**
```
scorm-package/
├── imsmanifest.xml
├── index.html
├── content/
│   ├── lesson-1.html
│   └── assessment.html
├── assets/
│   ├── images/
│   ├── css/
│   └── js/
└── scorm-api.js
```

**Workflow:**

**Step 1: Create Manifest**
```xml
<?xml version="1.0"?>
<manifest identifier="hmh-math-grade5-fractions">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>2004 4th Edition</schemaversion>
    <lom:lom>
      <lom:general>
        <lom:title>Grade 5 Math - Fractions</lom:title>
      </lom:general>
    </lom:lom>
  </metadata>
  <organizations default="org-1">
    <organization identifier="org-1">
      <title>Grade 5 Fractions Unit</title>
      <item identifier="item-1" identifierref="resource-1">
        <title>Lesson 1: Adding Fractions</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="resource-1" type="webcontent"
              href="content/lesson-1.html">
      <file href="content/lesson-1.html"/>
      <file href="assets/css/styles.css"/>
    </resource>
  </resources>
</manifest>
```

**Step 2: Implement SCORM API**
- Initialize SCORM connection
- Track completion status
- Report scores to LMS
- Track time spent

**Step 3: Package as ZIP**
```bash
cd scorm-package/
zip -r ../hmh-math-grade5-fractions-scorm.zip *
```

**Step 4: Test in LMS**
- Upload to Canvas test environment
- Verify launch
- Complete as student
- Check grade passback
- Test on multiple devices

**Quality Checks:**
- [ ] Uploads successfully
- [ ] Launches without errors
- [ ] Navigation works
- [ ] Completion tracking works
- [ ] Scores report correctly
- [ ] Works on all target LMS

**Deliverable:** `hmh-math-grade5-fractions-scorm.zip`

---

### Format 4: Accessible Formats

**Types:**
1. **Large Print PDF** (18pt, high contrast)
2. **Screen Reader HTML**
3. **Braille-Ready Text**

**Large Print PDF:**
```bash
pandoc student-pages.md \
  --template=templates/large-print.latex \
  -V fontsize:18pt \
  -V geometry:margin=1.5in \
  -V linestretch:2 \
  -o production/accessible/student-pages-large-print.pdf
```

**Screen Reader HTML:**
- All images have detailed alt text
- Math as MathML (not images)
- Semantic HTML structure
- ARIA landmarks

**Test with:**
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (Mac/iOS)
- TalkBack (Android)

**Deliverables:**
- `student-pages-large-print.pdf`
- `student-pages-screenreader.html`

---

## 4. Asset Management

### Asset Types

1. **Images** - Photos, illustrations, diagrams
2. **Videos** - Instructional, demonstrations
3. **Audio** - Pronunciations, descriptions
4. **Interactive** - Simulations, games

### Organization

```
assets/
├── images/
│   ├── curriculum/hmh-math-tx/grade-5/fractions/
│   │   ├── fraction-bars-thirds.png
│   │   └── fraction-circles-fourths.png
│   └── universal/icons/
├── videos/
│   └── hmh-math-tx/grade-5/fractions-intro.mp4
├── audio/
│   └── pronunciations/
└── interactive/
    └── fraction-models/
```

### Specifications

**Images:**
- **Format:** PNG (transparency) or JPG (photos)
- **Resolution:**
  - Print: 300 DPI minimum
  - Web: 72-96 DPI
- **Color Space:**
  - Print: CMYK
  - Web: RGB (sRGB)
- **Max File Size:**
  - Web: 500KB (optimized)

**Videos:**
- **Format:** MP4 (H.264)
- **Resolution:** 1920x1080 or 1280x720
- **Frame Rate:** 30 fps
- **Bitrate:** 5-8 Mbps
- **Audio:** AAC, 128 kbps, stereo
- **Captions:** WebVTT format required

**Audio:**
- **Format:** MP3
- **Bitrate:** 128-192 kbps
- **Sample Rate:** 44.1 kHz

### Workflow

**Step 1: Receive Specifications**
- Author provides descriptions
- Review for clarity

**Step 2: Source or Create**
- Search existing library
- Commission from designers
- Purchase stock (with licensing)

**Step 3: Optimize**

**Images:**
```bash
# Resize for web
convert fraction-bars.png \
  -resize 1200x800 \
  -quality 85 \
  fraction-bars-web.png

# Compress
pngquant fraction-bars-web.png \
  --output fraction-bars-optimized.png
```

**Videos:**
```bash
# Compress
ffmpeg -i fractions-intro.mp4 \
  -c:v libx264 -crf 23 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  fractions-intro-optimized.mp4
```

**Step 4: Add Metadata**
```json
{
  "asset_id": "img-frac-bars-001",
  "filename": "fraction-bars-thirds.png",
  "curriculum": "hmh-math-tx",
  "grade": "5",
  "description": "Three fraction bars showing 1/3, 2/3, 3/3",
  "alt_text": "Three horizontal fraction bars. Each divided into thirds. Top has 1/3 shaded, middle 2/3 shaded, bottom 3/3 shaded.",
  "dimensions": "1200x800",
  "file_size": "245KB",
  "license": "HMH proprietary"
}
```

**Step 5: Store in Library**
- Upload to CMS
- Tag with metadata
- Link to content

---

## 5. Quality Assurance

### Final Production QA Checklist

**Format Checks:**
- [ ] PDF renders correctly
- [ ] HTML displays on all browsers
- [ ] SCORM uploads and functions in LMS
- [ ] Accessible formats meet specs

**Visual Quality:**
- [ ] Images sharp (not pixelated)
- [ ] Text readable (size, contrast)
- [ ] Colors match brand
- [ ] Layout professional

**Technical Quality:**
- [ ] All links work
- [ ] All images load
- [ ] Videos play
- [ ] Interactive elements function
- [ ] Downloads work

**Accessibility:**
- [ ] WCAG 2.1 AA verified
- [ ] Screen reader tested
- [ ] Keyboard navigation works
- [ ] Color contrast sufficient
- [ ] Alt text present

**Cross-Format Consistency:**
- [ ] Content identical across formats
- [ ] Formatting consistent
- [ ] References accurate

**Branding:**
- [ ] HMH logo present
- [ ] Brand colors used
- [ ] Fonts match standards
- [ ] Copyright notice included

**Legal:**
- [ ] Copyright notices present
- [ ] Licenses verified
- [ ] Privacy compliance (COPPA, FERPA)
- [ ] Accessibility statement included

### Testing Tools

**Browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Devices:**
- Desktop (Windows, Mac)
- Tablet (iPad, Android)
- Phone (iOS, Android)

**Accessibility:**
- [WAVE Tool](https://wave.webaim.org/)
- [axe DevTools](https://www.deque.com/axe/)
- Screen readers (NVDA, JAWS, VoiceOver)

**LMS:**
- Canvas
- Moodle 3.9+
- Blackboard Learn

---

## 6. Delivery and Distribution

### Distribution Channels

1. **Direct Download** - Zip files
2. **LMS Upload** - SCORM packages
3. **Physical** - Printed materials
4. **Streaming** - Videos on platform
5. **App Stores** - Mobile apps

### Packaging

**Delivery Package Structure:**
```
delivery-package/
├── README.txt
├── teacher-guide.pdf
├── student-pages.pdf
├── teacher-guide.html
├── student-pages.html
├── hmh-math-grade5-fractions-scorm.zip
├── assets/
│   ├── images/
│   └── videos/
└── license.txt
```

### Delivery Manifest

```yaml
package: HMH Into Math Texas - Grade 5 Fractions
version: 1.0.0
release_date: 2025-11-20
curriculum: hmh-math-tx
grade: 5

contents:
  - file: teacher-guide.pdf
    format: PDF
    pages: 24
  - file: hmh-math-grade5-fractions-scorm.zip
    format: SCORM 2004 4th Edition

system_requirements:
  pdf_reader: Adobe Reader 10+
  web_browser: Chrome 90+, Firefox 88+
  lms: Canvas, Moodle 3.9+

accessibility:
  - WCAG 2.1 AA compliant
  - Screen reader compatible
  - Keyboard navigable
  - Closed captions on videos

contact: support@hmhco.com
```

### Upload to CDN

```bash
# Upload to content delivery network
aws s3 cp delivery-package/ \
  s3://hmh-content/math/tx/grade-5/fractions-unit/ \
  --recursive

# Set permissions
aws s3api put-bucket-acl \
  --bucket hmh-content \
  --acl authenticated-read
```

### Stakeholder Notification

**Email Template:**
```
Subject: Ready for Distribution: HMH Math TX Grade 5 Fractions

The Grade 5 Fractions Unit is now ready for distribution.

**Package Details:**
- Curriculum: HMH Into Math Texas Edition
- Grade: 5
- Version: 1.0.0
- Release Date: November 20, 2025

**Included Formats:**
✓ Teacher Guide (PDF, 24 pages)
✓ Student Pages (PDF, 12 pages)
✓ Interactive HTML versions
✓ SCORM package for LMS
✓ All assets

**Accessibility:**
✓ WCAG 2.1 AA compliant
✓ Screen reader compatible
✓ Closed captions

**Download:**
https://content.hmhco.com/math/tx/grade-5/fractions-unit/

**Questions?**
Contact production@hmhco.com
```

### Confirmation

**Delivery Checklist:**
- [ ] Download link works
- [ ] All files accessible
- [ ] Stakeholders notified
- [ ] Usage tracking enabled
- [ ] Support team briefed
- [ ] Documentation complete

---

## Quick Reference

### Common Commands

**PDF Generation:**
```bash
pandoc input.md -o output.pdf --template=hmh-template.latex
```

**HTML Generation:**
```bash
pandoc input.md -o output.html --css=styles.css --self-contained
```

**Image Optimization:**
```bash
convert input.png -resize 1200x800 -quality 85 output.png
```

**Video Compression:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
```

**SCORM Packaging:**
```bash
zip -r package-scorm.zip manifest.xml content/ assets/
```

### File Specifications Summary

| Asset Type | Format | Print | Web | Notes |
|------------|--------|-------|-----|-------|
| Images | PNG/JPG | 300 DPI | 72-96 DPI | Max 500KB web |
| Videos | MP4 (H.264) | N/A | 1080p/720p | Captions required |
| Audio | MP3 | N/A | 128-192 kbps | Mono for speech |
| Documents | PDF | CMYK | RGB | Accessible PDF/A |

### Quality Checklist Quick View

- [ ] All formats render correctly
- [ ] Assets optimized
- [ ] Accessibility validated (WCAG 2.1 AA)
- [ ] Brand compliance
- [ ] Cross-platform tested
- [ ] SCORM tested in LMS
- [ ] Documentation complete
- [ ] Delivery confirmed

---

## Support

- **Author Questions:** See [AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)
- **Editor Questions:** See [EDITOR_GUIDE.md](EDITOR_GUIDE.md)
- **Engineer Questions:** See [ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)
- **Technical Issues:** Create issue in GitHub
- **Production Standards:** HMH production handbook

---

**Version:** 1.0 | **Last Updated:** November 6, 2025
**For more information:** See [README.md](README.md) | [USER_GUIDE.md](USER_GUIDE.md)
