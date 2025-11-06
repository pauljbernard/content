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

## Your First Week in Production

Welcome! This section walks you through your first week, building skills progressively from Day 1 observation to Day 5 independent production.

### Day 1: Orientation and Environment Setup (6-8 hours)

**Morning: System Access and Tools (3-4 hours)**

**Hour 1: Get Access**
```bash
# Verify GitHub access
git clone https://github.com/pauljbernard/content.git
cd content

# Verify you can see published content
ls published/

# Verify production directories exist
ls production/ dist/
```

**Hour 2: Install Production Tools**
```bash
# Install Pandoc (for PDF generation)
brew install pandoc  # macOS
# or: sudo apt install pandoc  # Linux

# Install LaTeX (for PDF typesetting)
brew install basictex  # macOS
# or: sudo apt install texlive-latex-base texlive-fonts-recommended  # Linux

# Install ImageMagick (for image optimization)
brew install imagemagick

# Install FFmpeg (for video/audio processing)
brew install ffmpeg

# Verify installations
pandoc --version
pdflatex --version
convert --version  # ImageMagick
ffmpeg -version
```

**Hour 3: Explore Templates**
```bash
cd templates/

# PDF templates (LaTeX)
ls *.latex
# - hmh-teacher-guide.latex
# - hmh-student-workbook.latex
# - hmh-assessment.latex

# HTML templates
ls *.html
# - interactive-lesson.html
# - assessment-player.html

# SCORM templates
ls scorm-templates/
```

**Hour 4: Review Brand Guidelines**
```bash
# HMH brand assets
ls assets/brand/
# - hmh-logo.svg
# - color-palette.json
# - typography-guide.md
# - style-guide.pdf

# Read brand guidelines
open assets/brand/style-guide.pdf
```

**Afternoon: Shadow a Production Run (3-4 hours)**

**Find a recently completed production run:**
```bash
# Look for recent deliveries
ls -lt dist/ | head -10

# Pick one to study
cd dist/pdf/hmh-math-tx-grade5-lesson-3.2/

# Files you'll see:
# - teacher-guide.pdf
# - student-pages.pdf
# - answer-key.pdf
# - production-manifest.json
# - qa-report.txt
```

**Review the source:**
```bash
# Find the original source content
cd /published/lessons/hmh-math-tx/grade-5/lesson-3.2/

# Compare source markdown to final PDF
open teacher-guide.md
open ../../dist/pdf/hmh-math-tx-grade5-lesson-3.2/teacher-guide.pdf
```

**Questions to answer:**
- How did markdown become this polished PDF?
- What brand elements were added (logo, colors, fonts)?
- How are images positioned and sized?
- How is the table of contents generated?

**Day 1 Reflection:**
- [ ] Can access all repositories and tools
- [ ] Tools installed and working (pandoc, LaTeX, ImageMagick, FFmpeg)
- [ ] Understand directory structure (published → production → dist)
- [ ] Reviewed one complete production run end-to-end

---

### Day 2: Hands-On Practice - PDF Production (6-8 hours)

**Morning: Produce Your First PDF (3-4 hours)**

**Step 1: Find Practice Content**
```bash
cd /published/lessons/practice/simple-lesson/

# This is a simplified lesson for practice
ls
# - teacher-guide.md (simple, 2 pages)
# - assets/diagram1.png
```

**Step 2: Generate PDF with Pandoc**
```bash
# Basic conversion (no template)
pandoc teacher-guide.md -o test1.pdf

# Open and review
open test1.pdf

# Note: Looks plain, no branding, basic formatting
```

**Step 3: Apply HMH Template**
```bash
pandoc teacher-guide.md \
  --template=../../templates/hmh-teacher-guide.latex \
  --pdf-engine=xelatex \
  --toc \
  -V geometry:margin=1in \
  -V fontsize:11pt \
  -o test2.pdf

open test2.pdf

# Note: Now has HMH branding, proper fonts, TOC
```

**Step 4: Fix Common Issues**

**Issue 1: Image not found**
```bash
# Error: "! LaTeX Error: File `diagram1.png' not found"

# Solution: Specify resource path
pandoc teacher-guide.md \
  --template=../../templates/hmh-teacher-guide.latex \
  --pdf-engine=xelatex \
  --resource-path=assets \
  -o test3.pdf
```

**Issue 2: Image too large**
```bash
# Solution: Resize with ImageMagick before PDF generation
cd assets/
convert diagram1.png -resize 600x diagram1-resized.png

# Or: Add width specification in markdown
# ![Diagram](assets/diagram1.png){width=400px}
```

**Afternoon: Practice Different PDF Types (3-4 hours)**

**Practice 1: Student Workbook**
```bash
cd /published/assessments/practice/simple-quiz/

pandoc student-quiz.md \
  --template=../../templates/hmh-student-workbook.latex \
  --pdf-engine=xelatex \
  -o student-quiz.pdf

open student-quiz.pdf
```

**Practice 2: Assessment with Answer Key**
```bash
# Generate student version (no answers)
pandoc assessment.md \
  --template=../../templates/hmh-assessment.latex \
  -V show-answers:false \
  -o assessment-student.pdf

# Generate teacher version (with answers)
pandoc assessment.md \
  --template=../../templates/hmh-assessment.latex \
  -V show-answers:true \
  -o assessment-teacher.pdf
```

**Day 2 Reflection:**
- [ ] Generated PDFs using Pandoc
- [ ] Applied HMH templates successfully
- [ ] Resolved image path issues
- [ ] Created both student and teacher versions
- [ ] Understand difference between basic and templated output

---

### Day 3: HTML and Interactive Content (6-8 hours)

**Morning: Basic HTML Production (3-4 hours)**

**Step 1: Convert Markdown to HTML**
```bash
cd /published/lessons/practice/simple-lesson/

# Basic HTML conversion
pandoc teacher-guide.md -o test1.html

# With CSS styling
pandoc teacher-guide.md \
  --css=../../templates/styles/hmh-lesson.css \
  --standalone \
  -o test2.html

open test2.html
```

**Step 2: Add Interactive Elements**

**Create index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Fraction Addition Lesson</title>
  <link rel="stylesheet" href="styles/lesson.css">
</head>
<body>
  <header>
    <img src="assets/hmh-logo.svg" alt="HMH Logo">
    <h1>Lesson 3.2: Adding Fractions</h1>
  </header>

  <nav>
    <button onclick="showSection('teacher')">Teacher Guide</button>
    <button onclick="showSection('student')">Student Pages</button>
    <button onclick="showSection('practice')">Practice</button>
  </nav>

  <div id="teacher" class="section">
    <!-- Teacher content here -->
  </div>

  <div id="student" class="section" style="display:none;">
    <!-- Student content here -->
  </div>

  <div id="practice" class="section" style="display:none;">
    <!-- Practice activities here -->
  </div>

  <script src="scripts/lesson.js"></script>
</body>
</html>
```

**Afternoon: Practice Interactive Features (3-4 hours)**

**Add Interactive Quiz:**
```html
<div class="interactive-quiz">
  <p>What is 1/4 + 1/4?</p>
  <button onclick="checkAnswer('A')">A) 1/8</button>
  <button onclick="checkAnswer('B')">B) 2/4</button>
  <button onclick="checkAnswer('C')">C) 1/2</button>
  <div id="feedback"></div>
</div>

<script>
function checkAnswer(choice) {
  const feedback = document.getElementById('feedback');
  if (choice === 'B' || choice === 'C') {
    feedback.innerHTML = '<p class="correct">✓ Correct!</p>';
  } else {
    feedback.innerHTML = '<p class="incorrect">Try again.</p>';
  }
}
</script>
```

**Test Responsive Design:**
```bash
# Open in browser
open test.html

# Resize browser window - does it adapt?
# Test on mobile viewport
```

**Day 3 Reflection:**
- [ ] Generated HTML from Markdown
- [ ] Applied CSS styling
- [ ] Added interactive navigation
- [ ] Created simple interactive quiz
- [ ] Tested responsive design

---

### Day 4: SCORM Packaging (6-8 hours)

**Morning: Understand SCORM Structure (3-4 hours)**

**SCORM Package Anatomy:**
```
lesson-3.2-scorm.zip
├── imsmanifest.xml       # SCORM manifest (required)
├── index.html            # Launch file
├── assets/
│   ├── images/
│   └── videos/
├── scripts/
│   ├── scorm-api.js      # SCORM API wrapper
│   └── lesson.js         # Content logic
└── styles/
    └── lesson.css
```

**Step 1: Create imsmanifest.xml**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="hmh-math-tx-lesson-3.2" version="1.0">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="hmh-math-tx-lesson-3.2-org">
    <organization identifier="hmh-math-tx-lesson-3.2-org">
      <title>Lesson 3.2: Adding Fractions</title>
      <item identifier="item1" identifierref="resource1">
        <title>Adding Fractions with Unlike Denominators</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="resource1" type="webcontent" href="index.html">
      <file href="index.html"/>
      <file href="scripts/scorm-api.js"/>
      <file href="styles/lesson.css"/>
      <file href="assets/diagram1.png"/>
    </resource>
  </resources>
</manifest>
```

**Step 2: Add SCORM API Communication**
```javascript
// scripts/scorm-api.js
let scormAPI = null;

function initSCORM() {
  scormAPI = window.parent.API || window.top.API;
  if (scormAPI) {
    scormAPI.LMSInitialize("");
    scormAPI.LMSSetValue("cmi.core.lesson_status", "incomplete");
  }
}

function completeSCORM() {
  if (scormAPI) {
    scormAPI.LMSSetValue("cmi.core.lesson_status", "completed");
    scormAPI.LMSSetValue("cmi.core.score.raw", "100");
    scormAPI.LMSCommit("");
    scormAPI.LMSFinish("");
  }
}

window.onload = initSCORM;
window.onbeforeunload = completeSCORM;
```

**Afternoon: Package and Test (3-4 hours)**

**Step 3: Create SCORM Package**
```bash
cd production/scorm/lesson-3.2/

# Package as ZIP
zip -r lesson-3.2-scorm.zip *

# Move to dist
mv lesson-3.2-scorm.zip ../../../dist/scorm/
```

**Step 4: Test in LMS**
```
1. Log into test LMS (Canvas/Moodle)
2. Upload SCORM package
3. Launch and verify:
   - Content loads
   - Navigation works
   - Completion tracked
   - Score recorded
```

**Day 4 Reflection:**
- [ ] Understand SCORM package structure
- [ ] Created imsmanifest.xml
- [ ] Added SCORM API communication
- [ ] Packaged as ZIP
- [ ] Tested in LMS environment

---

### Day 4 Alternative: Common Cartridge Packaging (6-8 hours)

**When to Choose Common Cartridge over SCORM:**
- Need portable assessments (QTI format)
- Want to include LTI tools (external apps)
- Need gradebook categories and weights
- Want discussion forums in package
- Target modern LMS (Canvas, Moodle 3+, Blackboard Ultra)
- Need maximum interoperability

**Morning: Understand Common Cartridge Structure (3-4 hours)**

**Common Cartridge vs SCORM:**

| Feature | SCORM | Common Cartridge |
|---------|-------|------------------|
| **Assessments** | Embedded in content | QTI 2.1 (portable) |
| **External Tools** | No | LTI 1.1/1.3 support |
| **Gradebook** | Basic scoring | Full categories & weights |
| **Discussions** | No | Native support |
| **Interoperability** | LMS-specific | Platform-agnostic |
| **File Extension** | .zip | .imscc |

**Common Cartridge Package Anatomy:**
```
course-bio-101.imscc
├── imsmanifest.xml           # CC manifest (required)
├── course-settings.xml       # Gradebook config (optional)
├── lessons/
│   ├── lesson-1.html
│   └── lesson-2.html
├── assessments/
│   └── quiz-1/
│       ├── assessment_meta.xml
│       └── assessment.xml    # QTI 2.1
├── discussions/
│   └── forum-1.xml
├── lti-tools/
│   └── virtual-lab.xml
├── resources/
│   ├── images/
│   └── videos/
└── web-links/
    └── khan-academy.xml
```

**Step 1: Create imsmanifest.xml (CC 1.3)**

Use the template from `/templates/common-cartridge/v1.3/imsmanifest.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="bio-101-module-1"
          xmlns="http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1"
          xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p3/LOM/resource"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1
                              http://www.imsglobal.org/profile/cc/ccv1p3/ccv1p3_imscp_v1p2_v1p0.xsd">

  <!-- Metadata Section -->
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.3.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>Module 1: Cell Biology</lomimscc:string>
        </lomimscc:title>
        <lomimscc:description>
          <lomimscc:string>Introduction to cell structure and function</lomimscc:string>
        </lomimscc:description>
      </lomimscc:general>
    </lomimscc:lom>
  </metadata>

  <!-- Organizations Section - Course Structure -->
  <organizations>
    <organization identifier="org-bio-101" structure="rooted-hierarchy">
      <item identifier="root">
        <title>Module 1: Cell Biology</title>

        <!-- Lesson 1 -->
        <item identifier="lesson-1" identifierref="res-lesson-1">
          <title>Lesson 1: Cell Membranes</title>
        </item>

        <!-- Assessment -->
        <item identifier="quiz-1" identifierref="res-quiz-1">
          <title>Module 1 Quiz</title>
        </item>

        <!-- Discussion -->
        <item identifier="discuss-1" identifierref="res-discuss-1">
          <title>Discussion: Cell Theory</title>
        </item>

      </item>
    </organization>
  </organizations>

  <!-- Resources Section -->
  <resources>
    <!-- Lesson Resource -->
    <resource identifier="res-lesson-1" type="webcontent" href="lessons/lesson-1.html">
      <file href="lessons/lesson-1.html"/>
      <file href="resources/images/cell-diagram.png"/>
    </resource>

    <!-- QTI Assessment Resource -->
    <resource identifier="res-quiz-1"
              type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"
              href="assessments/quiz-1/assessment_meta.xml">
      <file href="assessments/quiz-1/assessment_meta.xml"/>
      <dependency identifierref="res-quiz-1-qti"/>
    </resource>

    <resource identifier="res-quiz-1-qti"
              type="associatedcontent/imscc_xmlv1p3/learning-application-resource">
      <file href="assessments/quiz-1/assessment.xml"/>
    </resource>

    <!-- Discussion Resource -->
    <resource identifier="res-discuss-1" type="imsdt_xmlv1p3">
      <file href="discussions/forum-1.xml"/>
    </resource>
  </resources>

</manifest>
```

**Step 2: Create Gradebook Configuration**

Use `/templates/common-cartridge/v1.3/course-settings.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<course identifier="bio-101">
  <title>Introduction to Biology</title>

  <!-- Assignment Groups (Gradebook Categories) -->
  <assignment_groups>
    <assignment_group identifier="grp-quizzes">
      <title>Module Quizzes</title>
      <group_weight>40</group_weight>
      <position>1</position>
    </assignment_group>

    <assignment_group identifier="grp-discussions">
      <title>Discussions</title>
      <group_weight>20</group_weight>
      <position>2</position>
    </assignment_group>

    <assignment_group identifier="grp-labs">
      <title>Labs</title>
      <group_weight>40</group_weight>
      <position>3</position>
    </assignment_group>
  </assignment_groups>

  <!-- Assignments (Linked to Gradebook) -->
  <assignments>
    <assignment identifier="quiz-1-assignment">
      <title>Module 1 Quiz</title>
      <assignment_group_identifierref>grp-quizzes</assignment_group_identifierref>
      <points_possible>100</points_possible>
      <grading_type>points</grading_type>
      <quiz_identifierref>res-quiz-1</quiz_identifierref>
    </assignment>

    <assignment identifier="discuss-1-assignment">
      <title>Cell Theory Discussion</title>
      <assignment_group_identifierref>grp-discussions</assignment_group_identifierref>
      <points_possible>10</points_possible>
      <grading_type>points</grading_type>
      <discussion_topic_identifierref>res-discuss-1</discussion_topic_identifierref>
    </assignment>
  </assignments>
</course>
```

**Step 3: Add QTI Assessment**

Use curriculum.export-qti skill to generate QTI 2.1 assessments:

```bash
# Export quiz to QTI 2.1
/curriculum.export-qti \
  --assessment "module-1-quiz.json" \
  --output "assessments/quiz-1/" \
  --version "2.1"

# This creates:
# assessments/quiz-1/
# ├── assessment_meta.xml
# └── assessment.xml (QTI 2.1)
```

**Step 4: Add Discussion Forum (Optional)**

Create `discussions/forum-1.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<topic xmlns="http://www.imsglobal.org/xsd/imsccv1p3/imsdt_v1p3">
  <title>Cell Theory Historical Debate</title>
  <text texttype="text/html">
    <![CDATA[
      <p>Read about the development of cell theory. Then discuss:</p>
      <ul>
        <li>Why was cell theory controversial in the 1800s?</li>
        <li>How did microscopy advances enable this discovery?</li>
      </ul>
    ]]>
  </text>
  <discussion_type>threaded</discussion_type>
  <require_initial_post>true</require_initial_post>
  <assignment identifier="discuss-1-assignment">
    <points_possible>10</points_possible>
  </assignment>
</topic>
```

**Afternoon: Package and Test (3-4 hours)**

**Step 5: Organize Package Directory**

```bash
cd production/common-cartridge/bio-101-module-1/

# Verify structure
tree
# .
# ├── imsmanifest.xml
# ├── course-settings.xml
# ├── lessons/
# │   └── lesson-1.html
# ├── assessments/
# │   └── quiz-1/
# │       ├── assessment_meta.xml
# │       └── assessment.xml
# ├── discussions/
# │   └── forum-1.xml
# └── resources/
#     └── images/
#         └── cell-diagram.png
```

**Step 6: Validate Package**

```bash
# Validate before packaging
/curriculum.validate-cc \
  --materials "production/common-cartridge/bio-101-module-1/" \
  --level thorough

# Expected output:
# ✓ Structure valid (12 checks passed)
# ✓ Schema valid (25 checks passed)
# ✓ QTI valid (18 checks passed)
# ✓ Ready for packaging
```

**Step 7: Create .imscc Package**

```bash
cd production/common-cartridge/bio-101-module-1/

# Package as .imscc (ZIP with .imscc extension)
zip -r bio-101-module-1.imscc *

# Or use skill
/curriculum.package-common-cartridge \
  --materials "." \
  --output "../../../dist/common-cartridge/bio-101-module-1.imscc"

# Move to distribution
mv bio-101-module-1.imscc ../../../dist/common-cartridge/
```

**Step 8: Test Import in LMS**

**Canvas Import:**
```
1. Go to Course Settings → Import Course Content
2. Select "Common Cartridge 1.x Package"
3. Choose file: bio-101-module-1.imscc
4. Click "Import"
5. Wait for import to complete (1-2 minutes)
6. Verify imported content:
   ✓ Module structure appears
   ✓ Lessons display correctly
   ✓ Quiz shows in Quizzes section
   ✓ Discussion appears in Discussions
   ✓ Gradebook categories configured
```

**Moodle Import:**
```
1. Course Administration → Restore
2. Upload bio-101-module-1.imscc
3. Select "Restore"
4. Choose import options
5. Verify content structure
```

**Blackboard Import:**
```
1. Control Panel → Packages and Utilities → Import Package
2. Browse to bio-101-module-1.imscc
3. Select import options
4. Submit
5. Verify content in course
```

**Step 9: Verification Checklist**

After import, verify:
- [ ] Course structure matches organization
- [ ] Lessons display with correct formatting
- [ ] Images and assets load correctly
- [ ] Quiz appears in assessments
- [ ] Quiz questions display properly
- [ ] Discussion forum created
- [ ] Gradebook categories configured correctly
- [ ] Assignment weights sum to 100%
- [ ] All links work (internal and external)

**Common Import Issues:**

**Issue 1: Package won't import**
```bash
# Validate manifest
xmllint --noout imsmanifest.xml

# Check for common errors:
# - Missing namespace declarations
# - Incorrect file references
# - Invalid resource types
```

**Issue 2: Assessments don't display**
```bash
# Validate QTI
xmllint --noout assessments/quiz-1/assessment.xml

# Ensure resource type is correct:
# type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"
```

**Issue 3: Gradebook not configured**
```bash
# Ensure course-settings.xml is included
# Verify assignment group weights sum to 100%
# Check assignment references match resource IDs
```

**Day 4 Alternative Reflection:**
- [ ] Understand Common Cartridge structure
- [ ] Created IMS CC 1.3 manifest
- [ ] Configured gradebook categories
- [ ] Added QTI 2.1 assessment
- [ ] Included discussion forum
- [ ] Validated package
- [ ] Packaged as .imscc
- [ ] Tested import in Canvas/Moodle
- [ ] Verified all content displays correctly

**CC vs SCORM Decision Guide:**

**Choose Common Cartridge when:**
- ✅ You need portable assessments (QTI)
- ✅ You want LTI tool integration
- ✅ You need complex gradebook setup
- ✅ You want discussion forums
- ✅ Target LMS is Canvas, Moodle 3+, Blackboard Ultra
- ✅ Maximum interoperability required

**Choose SCORM when:**
- ✅ Simple completion tracking needed
- ✅ Legacy LMS requires it
- ✅ Standalone module (not full course)
- ✅ No assessments or simple embedded quizzes
- ✅ No external tool integration needed

**Pro Tip:** For full courses, use Common Cartridge. For single lessons with completion tracking, use SCORM.

---

### Day 5: Complete End-to-End Production (6-8 hours)

**Your First Independent Production Run**

**Assignment: Produce Lesson 4.1 in all formats**

**Step 1: Review Source (30 min)**
```bash
cd /published/lessons/hmh-math-tx/grade-5/lesson-4.1/

ls
# - teacher-guide.md
# - student-pages.md
# - practice-problems.md
# - assets/ (5 images, 1 video)
```

**Step 2: PDF Production (1.5 hours)**
```bash
# Teacher guide
pandoc teacher-guide.md \
  --template=../../templates/hmh-teacher-guide.latex \
  --pdf-engine=xelatex \
  --toc \
  --resource-path=assets \
  -o ../../../production/pdf/lesson-4.1-teacher.pdf

# Student pages
pandoc student-pages.md \
  --template=../../templates/hmh-student-workbook.latex \
  --pdf-engine=xelatex \
  --resource-path=assets \
  -o ../../../production/pdf/lesson-4.1-student.pdf

# QA check both PDFs
```

**Step 3: HTML Production (2 hours)**
```bash
# Create interactive HTML
cd ../../../production/html/lesson-4.1/

# Convert markdown sections
pandoc ../../../published/lessons/hmh-math-tx/grade-5/lesson-4.1/teacher-guide.md \
  --css=styles/lesson.css \
  --standalone \
  -o teacher-section.html

# Build interactive index.html (use Day 3 template)
# Add navigation, interactive elements
# Test responsive design
```

**Step 4: SCORM Package (2 hours)**
```bash
cd ../../../production/scorm/lesson-4.1/

# Copy HTML content
cp -r ../html/lesson-4.1/* .

# Create imsmanifest.xml (use Day 4 template)
# Add SCORM API wrapper
# Package as ZIP
zip -r lesson-4.1-scorm.zip *

# Test in LMS
```

**Step 5: QA and Delivery (1 hour)**
```bash
# Run QA checklist
# - All PDFs render correctly
# - HTML responsive on mobile
# - SCORM launches in LMS
# - All assets display correctly

# Move to dist/
mv production/pdf/lesson-4.1-*.pdf dist/pdf/
mv production/html/lesson-4.1/ dist/html/
mv production/scorm/lesson-4.1-scorm.zip dist/scorm/

# Create delivery manifest (JSON)
# Notify stakeholders
```

**Day 5 Reflection:**
- [ ] Completed full production run independently
- [ ] Generated all 3 formats (PDF, HTML, SCORM)
- [ ] Ran QA checklist
- [ ] Delivered to dist/ directory
- [ ] Ready for Week 2 advanced topics

---

### Week 1 Summary

**Skills Acquired:**
- PDF production with Pandoc and LaTeX templates
- HTML production with CSS styling and interactivity
- SCORM packaging with manifest and API
- Asset optimization (images, videos)
- QA processes
- Directory structure and git workflow

**Next Steps (Week 2):**
- Accessible format production (large print, screen reader, braille)
- Advanced asset optimization and CDN delivery
- Automation scripts for batch production
- Performance optimization
- Working with production metrics

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

### Format 3B: Common Cartridge Packages

**Use Cases:**
- Full course packaging (not just single lessons)
- Portable assessments (QTI format)
- LTI tool integration (external apps)
- Gradebook configuration
- Discussion forums
- Maximum LMS interoperability

**When to Choose CC over SCORM:**
- ✅ Need QTI assessments (portable format)
- ✅ Want LTI tool links (simulations, labs, etc.)
- ✅ Need gradebook categories and weights
- ✅ Want discussion forums included
- ✅ Target modern LMS (Canvas, Moodle 3+, Blackboard Ultra)
- ✅ Packaging complete courses (not just modules)

**Structure:**
```
common-cartridge-package/
├── imsmanifest.xml           # CC manifest (required)
├── course-settings.xml       # Gradebook config
├── lessons/
│   ├── lesson-1.html
│   ├── lesson-2.html
│   └── lesson-3.html
├── assessments/
│   ├── quiz-1/
│   │   ├── assessment_meta.xml
│   │   └── assessment.xml    # QTI 2.1
│   └── exam-1/
│       ├── assessment_meta.xml
│       └── assessment.xml
├── discussions/
│   ├── forum-1.xml
│   └── forum-2.xml
├── lti-tools/               # Optional
│   └── virtual-lab.xml
├── resources/
│   ├── images/
│   ├── videos/
│   └── documents/
└── web-links/               # Optional
    └── external-resources.xml
```

**Workflow:**

**Step 1: Create imsmanifest.xml**

Use template: `/templates/common-cartridge/v1.3/imsmanifest.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="hmh-math-grade5-fractions"
          xmlns="http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1"
          xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p3/LOM/manifest"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.3.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>Grade 5 Math - Fractions Unit</lomimscc:string>
        </lomimscc:title>
        <lomimscc:description>
          <lomimscc:string>Complete unit on fraction operations</lomimscc:string>
        </lomimscc:description>
      </lomimscc:general>
    </lomimscc:lom>
  </metadata>

  <organizations>
    <organization identifier="org-1" structure="rooted-hierarchy">
      <item identifier="root">
        <title>Fractions Unit</title>

        <!-- Lesson 1 -->
        <item identifier="lesson-1" identifierref="res-lesson-1">
          <title>Lesson 1: Adding Fractions</title>
        </item>

        <!-- Assessment -->
        <item identifier="quiz-1" identifierref="res-quiz-1">
          <title>Lesson 1 Quiz</title>
        </item>

        <!-- Discussion -->
        <item identifier="discuss-1" identifierref="res-discuss-1">
          <title>Discussion: Fraction Strategies</title>
        </item>

      </item>
    </organization>
  </organizations>

  <resources>
    <!-- Lesson -->
    <resource identifier="res-lesson-1" type="webcontent" href="lessons/lesson-1.html">
      <file href="lessons/lesson-1.html"/>
      <file href="resources/images/fraction-diagram.png"/>
    </resource>

    <!-- QTI Assessment -->
    <resource identifier="res-quiz-1"
              type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"
              href="assessments/quiz-1/assessment_meta.xml">
      <file href="assessments/quiz-1/assessment_meta.xml"/>
      <dependency identifierref="res-quiz-1-qti"/>
    </resource>

    <resource identifier="res-quiz-1-qti"
              type="associatedcontent/imscc_xmlv1p3/learning-application-resource">
      <file href="assessments/quiz-1/assessment.xml"/>
    </resource>

    <!-- Discussion -->
    <resource identifier="res-discuss-1" type="imsdt_xmlv1p3">
      <file href="discussions/forum-1.xml"/>
    </resource>
  </resources>

</manifest>
```

**Step 2: Configure Gradebook**

Create `course-settings.xml` using template:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<course identifier="hmh-math-grade5-fractions">
  <title>Grade 5 Math - Fractions</title>

  <assignment_groups>
    <assignment_group identifier="grp-quizzes">
      <title>Lesson Quizzes</title>
      <group_weight>30</group_weight>
    </assignment_group>
    <assignment_group identifier="grp-discussions">
      <title>Discussions</title>
      <group_weight>20</group_weight>
    </assignment_group>
    <assignment_group identifier="grp-exams">
      <title>Unit Exam</title>
      <group_weight>50</group_weight>
    </assignment_group>
  </assignment_groups>

  <assignments>
    <assignment identifier="quiz-1-assignment">
      <title>Lesson 1 Quiz</title>
      <assignment_group_identifierref>grp-quizzes</assignment_group_identifierref>
      <points_possible>20</points_possible>
      <quiz_identifierref>res-quiz-1</quiz_identifierref>
    </assignment>
  </assignments>
</course>
```

**Step 3: Add QTI Assessments**

```bash
# Export each assessment to QTI 2.1
/curriculum.export-qti \
  --assessment "lesson-1-quiz.json" \
  --output "assessments/quiz-1/" \
  --version "2.1"

# Repeat for each assessment
```

**Step 4: Add Discussions (Optional)**

Create discussion XML files using template:

```xml
<!-- discussions/forum-1.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<topic xmlns="http://www.imsglobal.org/xsd/imsccv1p3/imsdt_v1p3">
  <title>Fraction Strategies Discussion</title>
  <text texttype="text/html">
    <![CDATA[
      <p>Share your strategies for adding fractions with unlike denominators.</p>
    ]]>
  </text>
  <discussion_type>threaded</discussion_type>
  <require_initial_post>true</require_initial_post>
  <assignment identifier="discuss-1-assignment">
    <points_possible>10</points_possible>
  </assignment>
</topic>
```

**Step 5: Validate Package**

```bash
# Validate before packaging
/curriculum.validate-cc \
  --materials "production/common-cartridge/hmh-math-grade5-fractions/" \
  --level thorough

# Expected output:
# ✓ Structure valid (12 checks)
# ✓ Schema valid (25 checks)
# ✓ QTI valid (18 checks)
# ✓ Accessibility (15 checks)
# Overall: PASS - Ready for packaging
```

**Step 6: Package as .imscc**

```bash
cd production/common-cartridge/hmh-math-grade5-fractions/

# Method 1: Manual ZIP
zip -r ../../../dist/common-cartridge/hmh-math-grade5-fractions.imscc *

# Method 2: Use skill
/curriculum.package-common-cartridge \
  --materials "." \
  --output "../../../dist/common-cartridge/hmh-math-grade5-fractions.imscc" \
  --cc-version "1.3" \
  --qti-version "2.1"
```

**Step 7: Test Import in Target LMS**

**Canvas:**
```bash
1. Course Settings → Import Course Content
2. Select "Common Cartridge 1.x Package"
3. Choose file: hmh-math-grade5-fractions.imscc
4. Click "Import"
5. Wait for completion (usually 1-3 minutes)
6. Verify:
   ✓ Modules appear with correct structure
   ✓ Lessons display correctly
   ✓ Quizzes appear in Quizzes section
   ✓ Discussions created
   ✓ Gradebook categories configured
   ✓ All assets load (images, videos)
```

**Moodle:**
```bash
1. Course Administration → Restore
2. Upload .imscc file
3. Select import options
4. Click "Restore"
5. Verify content structure
```

**Blackboard:**
```bash
1. Control Panel → Packages and Utilities → Import Package
2. Browse to .imscc file
3. Select options
4. Submit
5. Verify import
```

**Quality Checks:**
- [ ] Package validates (no errors)
- [ ] Imports successfully to Canvas
- [ ] Imports successfully to Moodle
- [ ] Imports successfully to Blackboard
- [ ] Course structure matches manifest
- [ ] Lessons display with correct formatting
- [ ] Images and assets load
- [ ] QTI assessments appear correctly
- [ ] Quiz questions display and function
- [ ] Discussions created (if included)
- [ ] Gradebook categories configured
- [ ] Assignment weights correct (sum to 100%)
- [ ] LTI tools launch (if included)
- [ ] All links work
- [ ] Accessibility compliant (WCAG 2.1 AA)

**Common Issues and Fixes:**

**Issue 1: Import Fails**
```bash
# Check manifest validity
xmllint --noout imsmanifest.xml

# Validate against schema
/curriculum.validate-cc --package package.imscc --level thorough
```

**Issue 2: Assessments Don't Display**
```bash
# Validate QTI
xmllint --noout assessments/quiz-1/assessment.xml

# Ensure resource type correct:
# type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"
```

**Issue 3: Gradebook Not Configured**
```bash
# Verify course-settings.xml included
# Check weights sum to 100%
# Ensure assignment references match resource IDs
```

**Issue 4: Assets Don't Load**
```bash
# Check file references in manifest
# Verify all files exist
# Use relative paths (not absolute)
# Check case sensitivity
```

**Pro Tips:**

1. **Version Selection:**
   - Use CC 1.3 + QTI 2.1 for maximum compatibility
   - Use CC 1.2 if CC 1.3 fails
   - QTI 2.1 works with all modern LMS

2. **Testing Strategy:**
   - Always validate before packaging
   - Test in Canvas first (most common)
   - Test in Moodle second
   - Test in Blackboard/D2L if required

3. **Gradebook Setup:**
   - Keep categories simple (3-5 max)
   - Make weights sum to 100%
   - Link all assessments to gradebook

4. **Performance:**
   - Keep images optimized (<500KB each)
   - Compress videos or use external links
   - Package size should be <100MB for fast uploads

**Deliverable:** `hmh-math-grade5-fractions.imscc` (Common Cartridge 1.3 package)

**Documentation Reference:**
- `/templates/common-cartridge/README.md` - Template usage
- `/templates/common-cartridge/VERSION_SUPPORT.md` - Version selection
- `.claude/skills/curriculum-package-common-cartridge/SKILL.md` - Packaging skill
- `.claude/skills/curriculum-validate-cc/SKILL.md` - Validation skill

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

## Frequently Asked Questions

### PDF Production

**Q1: Pandoc fails with "! LaTeX Error: File not found". How do I fix image paths?**

**A:** Use `--resource-path` to specify where Pandoc should look for assets:
```bash
pandoc teacher-guide.md \
  --resource-path=assets:../assets:../../shared-assets \
  --pdf-engine=xelatex \
  -o output.pdf
```

Multiple paths separated by `:` (Unix) or `;` (Windows). Pandoc searches in order.

**Q2: PDFs have inconsistent fonts. How do I ensure brand fonts are used?**

**A:** Specify fonts in LaTeX template and install system-wide:
```latex
% In template .latex file
\setmainfont{Helvetica Neue}
\setmonofont{Courier New}
```

Install fonts:
```bash
# macOS
cp fonts/*.ttf /Library/Fonts/

# Linux
cp fonts/*.ttf ~/.fonts/
fc-cache -f -v
```

**Q3: How do I generate both print and digital PDFs with different specifications?**

**A:** Use Pandoc variables to control output:
```bash
# Print version (CMYK, high res, bleed)
pandoc content.md \
  --template=templates/print.latex \
  -V print-mode:true \
  -V dpi:300 \
  -o print.pdf

# Digital version (RGB, screen res, hyperlinks)
pandoc content.md \
  --template=templates/digital.latex \
  -V digital-mode:true \
  -V colorlinks:true \
  -o digital.pdf
```

**Q4: PDF generation is slow (5+ minutes). How can I speed it up?**

**A:** Several optimizations:
```bash
# 1. Optimize images BEFORE Pandoc (resize to needed size)
find assets/ -name "*.png" -exec convert {} -resize 1200x {}.opt.png \;

# 2. Use faster PDF engine (if acceptable quality)
--pdf-engine=pdflatex  # Faster than xelatex

# 3. Disable TOC if not needed
# Remove --toc flag

# 4. Parallel processing for multiple files
ls *.md | xargs -P 4 -I {} pandoc {} -o {}.pdf
```

**Q5: How do I add page numbers, headers, and footers?**

**A:** Configure in LaTeX template:
```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{HMH Into Math - Grade 5}
\fancyhead[R]{Lesson 3.2}
\fancyfoot[C]{\thepage}
```

---

### HTML Production

**Q6: HTML doesn't look right on mobile. How do I make it responsive?**

**A:** Use responsive CSS:
```css
/* Mobile-first approach */
body {
  font-size: 16px;
  padding: 10px;
}

/* Tablet */
@media (min-width: 768px) {
  body {
    font-size: 18px;
    padding: 20px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .content {
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Images scale */
img {
  max-width: 100%;
  height: auto;
}
```

Test with browser dev tools mobile emulation.

**Q7: Videos don't play in HTML. What formats should I use?**

**A:** Provide multiple formats for compatibility:
```html
<video controls width="640">
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  <p>Your browser doesn't support HTML5 video. <a href="video.mp4">Download video</a>.</p>
</video>
```

Convert with FFmpeg:
```bash
# MP4 (H.264)
ffmpeg -i source.mov -c:v libx264 -crf 23 -c:a aac -b:a 128k video.mp4

# WebM (VP9)
ffmpeg -i source.mov -c:v libvpx-vp9 -crf 30 -c:a libopus video.webm
```

**Q8: How do I implement navigation between sections without page reload?**

**A:** Use JavaScript to show/hide sections:
```javascript
function showSection(sectionId) {
  // Hide all sections
  document.querySelectorAll('.section').forEach(section => {
    section.style.display = 'none';
  });

  // Show requested section
  document.getElementById(sectionId).style.display = 'block';

  // Update navigation active state
  document.querySelectorAll('.nav-button').forEach(btn => {
    btn.classList.remove('active');
  });
  event.target.classList.add('active');

  // Update URL without reload (for bookmarking)
  history.pushState({section: sectionId}, '', `#${sectionId}`);
}

// Handle back/forward buttons
window.addEventListener('popstate', (event) => {
  if (event.state && event.state.section) {
    showSection(event.state.section);
  }
});
```

---

### SCORM Packaging

**Q9: SCORM package uploads but doesn't launch in LMS. What's wrong?**

**A:** Check common issues:
```bash
# 1. Verify imsmanifest.xml is at package root
unzip -l package.zip | head -5
# Should show: imsmanifest.xml as first file

# 2. Validate XML syntax
xmllint --noout imsmanifest.xml
# No output = valid

# 3. Check href paths match actual files
# In manifest: <resource ... href="index.html">
ls index.html  # Must exist

# 4. Verify no spaces in filenames
find . -name "* *"
# Rename any files with spaces

# 5. Test with SCORM validator
# Upload to: https://scorm.com/scorm-solved/scorm-cloud-features/scorm-content-player/
```

**Q10: LMS shows "incomplete" even after completing content. How do I fix completion tracking?**

**A:** Ensure proper SCORM API calls:
```javascript
// SCORM 1.2
function completeCourse() {
  var scormAPI = findAPI();
  if (scormAPI) {
    // Set status
    scormAPI.LMSSetValue("cmi.core.lesson_status", "completed");

    // Set score (0-100)
    scormAPI.LMSSetValue("cmi.core.score.raw", "100");
    scormAPI.LMSSetValue("cmi.core.score.min", "0");
    scormAPI.LMSSetValue("cmi.core.score.max", "100");

    // Commit data
    scormAPI.LMSCommit("");

    // Finish session
    scormAPI.LMSFinish("");
  }
}

// Call on quiz completion or lesson end
document.getElementById('finish-button').addEventListener('click', completeCourse);
```

**Q11: Different LMS platforms (Canvas, Moodle, Blackboard) behave differently. How do I ensure compatibility?**

**A:** Stick to SCORM 1.2 (not 2004) for widest compatibility:
```xml
<!-- Use SCORM 1.2 in manifest -->
<schemaversion>1.2</schemaversion>
```

Test in target LMS:
- Canvas: Use SCORM 1.2, test with Canvas Cloud
- Moodle: Works with 1.2 and 2004, test locally
- Blackboard: Prefers SCORM 1.2, test in sandbox

Common compatibility fixes:
```javascript
// Find API across different LMS implementations
function findAPI(win) {
  let attempts = 0;
  const maxAttempts = 500;

  while (!win.API && !win.API_1484_11 && win.parent && win.parent != win && attempts < maxAttempts) {
    attempts++;
    win = win.parent;
  }

  return win.API || win.API_1484_11 || null;
}
```

---

### Asset Management

**Q12: What are the optimal image specifications for web vs. print?**

**A:**

**Web (HTML/SCORM):**
```bash
# JPG for photos
convert photo.jpg -resize 1200x -quality 85 photo-web.jpg

# PNG for diagrams/text
convert diagram.png -resize 800x diagram-web.png

# SVG for logos/icons (no conversion needed, already optimal)
```

**Print (PDF):**
```bash
# High resolution (300 DPI)
convert photo.jpg -density 300 -units PixelsPerInch photo-print.jpg

# CMYK color space for professional printing
convert photo.jpg -colorspace CMYK photo-print-cmyk.jpg
```

**Q13: How do I batch-optimize hundreds of images?**

**A:** Use shell loops with ImageMagick:
```bash
# Optimize all JPGs in assets/
for file in assets/**/*.jpg; do
  convert "$file" -resize 1200x -quality 85 "${file%.jpg}-opt.jpg"
done

# Optimize all PNGs (lossless compression)
for file in assets/**/*.png; do
  optipng -o5 "$file"  # or: pngquant --quality=80-95 "$file"
done

# Or use parallel processing for speed
find assets/ -name "*.jpg" | parallel -j 8 convert {} -resize 1200x -quality 85 {}.opt.jpg
```

**Q14: Videos are too large (100+ MB). How do I compress without losing quality?**

**A:** Use FFmpeg with optimized settings:
```bash
# H.264 compression (good quality, widely supported)
ffmpeg -i input.mov \
  -c:v libx264 \
  -crf 23 \
  -preset slow \
  -c:a aac -b:a 128k \
  output.mp4

# For web (smaller file size)
ffmpeg -i input.mov \
  -c:v libx264 \
  -crf 28 \
  -preset faster \
  -c:a aac -b:a 96k \
  output-web.mp4

# Check file size reduction
ls -lh input.mov output.mp4
```

CRF values: 18 (high quality, large file) to 28 (lower quality, small file). 23 is balanced.

---

### Quality Assurance

**Q15: How do I validate WCAG 2.1 AA compliance for HTML?**

**A:** Use automated tools + manual checks:

**Automated:**
```bash
# Install Pa11y
npm install -g pa11y

# Test HTML file
pa11y --standard WCAG2AA output.html

# Test entire site
pa11y-ci --sitemap https://example.com/sitemap.xml
```

**Manual Checklist:**
- [ ] All images have alt text
- [ ] Color contrast ≥ 4.5:1 for text
- [ ] Keyboard navigation works (no mouse needed)
- [ ] Screen reader announces all content properly
- [ ] Form inputs have labels
- [ ] Videos have captions

**Q16: PDF renders differently on Mac vs. Windows. How do I ensure consistency?**

**A:** Use embedded fonts and consistent settings:
```bash
pandoc content.md \
  --pdf-engine=xelatex \
  --variable fontenc=T1 \
  --variable geometry:margin=1in \
  -o output.pdf

# Verify fonts are embedded
pdffonts output.pdf
# "emb" column should show "yes" for all fonts

# If fonts not embedded, force it in LaTeX template:
\usepackage{fontspec}
\setmainfont[Path=fonts/,Extension=.ttf,UprightFont=*-Regular,BoldFont=*-Bold]{HelveticaNeue}
```

Test on both platforms or use PDF viewer that renders consistently (Adobe Acrobat).

---

### Automation and Workflow

**Q17: Can I automate production for batch processing 50+ lessons?**

**A:** Yes, use bash scripts:
```bash
#!/bin/bash
# batch-produce.sh

LESSONS_DIR="/published/lessons/hmh-math-tx/grade-5"
OUTPUT_DIR="/dist/pdf"

for lesson in "$LESSONS_DIR"/*/; do
  lesson_name=$(basename "$lesson")
  echo "Processing: $lesson_name"

  # PDF
  pandoc "$lesson/teacher-guide.md" \
    --template=templates/hmh-teacher-guide.latex \
    --pdf-engine=xelatex \
    --resource-path="$lesson/assets" \
    -o "$OUTPUT_DIR/$lesson_name-teacher.pdf"

  # HTML
  pandoc "$lesson/student-pages.md" \
    --css=styles/lesson.css \
    --standalone \
    -o "/dist/html/$lesson_name.html"
done

echo "Batch processing complete"
```

Run: `./batch-produce.sh`

**Q18: How do I set up a CI/CD pipeline for automated production on content updates?**

**A:** Use GitHub Actions:
```yaml
# .github/workflows/production.yml
name: Auto Production

on:
  push:
    paths:
      - 'published/**'

jobs:
  produce:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install tools
        run: |
          sudo apt-get install -y pandoc texlive-xelatex

      - name: Generate PDFs
        run: |
          for file in published/**/*.md; do
            pandoc "$file" -o "dist/$(basename $file .md).pdf"
          done

      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: production-output
          path: dist/
```

---

### Troubleshooting

**Q19: Pandoc hangs/crashes on large files (1000+ pages). How do I handle this?**

**A:** Split into smaller chunks:
```bash
# Split markdown file into chapters
csplit content.md '/^# Chapter/' '{*}'

# Process each chapter
for chapter in xx*; do
  pandoc "$chapter" -o "chapter-$(basename $chapter).pdf"
done

# Merge PDFs
pdfunite chapter-*.pdf complete-book.pdf
```

**Q20: Build fails with cryptic LaTeX errors. How do I debug?**

**A:** Check LaTeX log:
```bash
# Run pandoc with --verbose
pandoc content.md --pdf-engine=xelatex --verbose -o output.pdf 2>&1 | tee build.log

# Look for actual error (often near end)
grep -i "error" build.log

# Common fixes:
# 1. Special characters - escape: \$ \% \& \# \_ \{ \}
# 2. Image paths - use --resource-path
# 3. Missing packages - install with tlmgr:
sudo tlmgr install <package-name>
```

**Q21: Common Cartridge vs. SCORM - When should I use which format?**

**A:** Use this decision matrix:

**Choose Common Cartridge when:**
- ✅ Creating full courses (not just single lessons)
- ✅ Need portable QTI assessments
- ✅ Want LTI tool integration (simulations, external labs)
- ✅ Need gradebook categories and weights
- ✅ Want discussion forums in package
- ✅ Target modern LMS (Canvas, Moodle 3+, Blackboard Ultra)
- ✅ Maximum interoperability required

**Choose SCORM when:**
- ✅ Single standalone lesson/module
- ✅ Simple completion tracking sufficient
- ✅ No assessments or simple embedded quizzes
- ✅ Legacy LMS requires it
- ✅ Quick turnaround needed

**Summary:** Full courses → Common Cartridge. Single lessons → SCORM.

**Q22: How do I convert QTI assessments for Common Cartridge packages?**

**A:** Use the curriculum.export-qti skill:

```bash
# Export single assessment to QTI 2.1
/curriculum.export-qti \
  --assessment "module-1-quiz.json" \
  --output "assessments/quiz-1/" \
  --version "2.1"

# This creates:
# assessments/quiz-1/
# ├── assessment_meta.xml  (Canvas-specific metadata)
# └── assessment.xml        (QTI 2.1 standard)

# For multiple assessments, batch process:
for quiz in quizzes/*.json; do
  name=$(basename "$quiz" .json)
  /curriculum.export-qti \
    --assessment "$quiz" \
    --output "assessments/$name/" \
    --version "2.1"
done
```

**Key Points:**
- Always use QTI 2.1 for maximum compatibility
- QTI 3.0 works only with Canvas 2020+ / Moodle 4.x
- Include assessment_meta.xml for gradebook integration
- Validate QTI with: `xmllint --noout assessment.xml`

**Q23: How do I add LTI tools (external apps) to Common Cartridge packages?**

**A:** Create LTI tool XML files:

```bash
# Step 1: Create LTI tool configuration
cat > lti-tools/virtual-microscope.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<cartridge_basiclti_link xmlns="http://www.imsglobal.org/xsd/imslticc_v1p0">
  <blti:title>Virtual Microscope Lab</blti:title>
  <blti:description>Interactive virtual microscope</blti:description>
  <blti:launch_url>https://virtualmicroscope.edu/launch</blti:launch_url>
  <blti:secure_launch_url>https://virtualmicroscope.edu/launch</blti:secure_launch_url>

  <blti:custom>
    <lticm:property name="lab_id">cell-structure</lticm:property>
  </blti:custom>

  <blti:extensions platform="canvas.instructure.com">
    <lticm:property name="privacy_level">public</lticm:property>
  </blti:extensions>
</cartridge_basiclti_link>
EOF

# Step 2: Reference in imsmanifest.xml
# Add to <resources> section:
<resource identifier="res-lti-lab" type="imsbasiclti_xmlv1p0">
  <file href="lti-tools/virtual-microscope.xml"/>
</resource>

# Add to <organizations> section:
<item identifier="lti-lab-item" identifierref="res-lti-lab">
  <title>Virtual Microscope Lab</title>
</item>
```

**Pro Tip:** Use template from `/templates/common-cartridge/v1.3/lti-tool.xml`

**Q24: Common Cartridge package won't import into Canvas/Moodle. How do I troubleshoot?**

**A:** Follow this systematic debugging process:

```bash
# Step 1: Validate package structure
unzip -l package.imscc | head -20

# Ensure imsmanifest.xml at root (not in subdirectory)
# Common mistake: package.imscc/subfolder/imsmanifest.xml ❌
# Correct: package.imscc/imsmanifest.xml ✅

# Step 2: Validate manifest XML
xmllint --noout imsmanifest.xml

# If errors, check:
# - Namespace declarations complete
# - Closing tags match
# - Special characters escaped in CDATA

# Step 3: Validate against IMS CC 1.3 schema
/curriculum.validate-cc --package package.imscc --level thorough

# Step 4: Check file references
# All files in manifest must exist
/curriculum.validate-cc --package package.imscc | grep "Missing file"

# Step 5: Test with minimal package
# Remove optional elements (discussions, LTI tools)
# Try importing just lessons + one assessment

# Step 6: Check LMS-specific logs
# Canvas: Course Settings → Import → View logs
# Moodle: Site Administration → Reports → Logs
```

**Common Issues:**
1. **Wrong resource type** - Ensure assessments use `type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"`
2. **Missing files** - All href references must exist
3. **Invalid XML** - Run xmllint on all XML files
4. **Encoding issues** - Use UTF-8 encoding

**Q25: Canvas imports Common Cartridge but assessments don't display. Why?**

**A:** Check QTI configuration:

```bash
# Step 1: Verify assessment resource type
grep -A5 "type=.*assessment" imsmanifest.xml

# Should be:
# type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"

# Step 2: Check for dependency
<resource identifier="res-quiz-1"
          type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment">
  <file href="assessments/quiz-1/assessment_meta.xml"/>
  <dependency identifierref="res-quiz-1-qti"/>  <!-- REQUIRED -->
</resource>

<resource identifier="res-quiz-1-qti"
          type="associatedcontent/imscc_xmlv1p3/learning-application-resource">
  <file href="assessments/quiz-1/assessment.xml"/>  <!-- QTI file -->
</resource>

# Step 3: Validate QTI XML
xmllint --noout assessments/quiz-1/assessment.xml

# Step 4: Check assessment_meta.xml
# Ensure quiz_identifierref matches resource ID:
<quiz_identifierref>res-quiz-1</quiz_identifierref>

# Step 5: Verify QTI version
# Canvas supports QTI 2.1 and 2.2 best
# Use QTI 2.1 for maximum compatibility

# Step 6: Test individual QTI file
# Upload just the assessment.xml as QTI import
# If this works, issue is in CC manifest
# If this fails, issue is in QTI itself
```

**Q26: Gradebook categories don't transfer when importing Common Cartridge. How do I fix it?**

**A:** Ensure course-settings.xml is properly configured:

```bash
# Step 1: Verify course-settings.xml exists
ls -la course-settings.xml

# Step 2: Check assignment group weights sum to 100%
cat course-settings.xml | grep "group_weight"
# Should total 100%

# Example correct configuration:
<assignment_groups>
  <assignment_group identifier="grp-quizzes">
    <title>Quizzes</title>
    <group_weight>40</group_weight>  <!-- 40% -->
  </assignment_group>
  <assignment_group identifier="grp-discussions">
    <title>Discussions</title>
    <group_weight>20</group_weight>  <!-- 20% -->
  </assignment_group>
  <assignment_group identifier="grp-exams">
    <title>Exams</title>
    <group_weight>40</group_weight>  <!-- 40% -->
  </assignment_group>
</assignment_groups>
<!-- Total: 40 + 20 + 40 = 100% ✓ -->

# Step 3: Link assignments to groups
<assignments>
  <assignment identifier="quiz-1-assignment">
    <title>Module 1 Quiz</title>
    <assignment_group_identifierref>grp-quizzes</assignment_group_identifierref>
    <points_possible>20</points_possible>
    <quiz_identifierref>res-quiz-1</quiz_identifierref>  <!-- Links to quiz -->
  </assignment>
</assignments>

# Step 4: Reference in imsmanifest.xml
# Add course-settings.xml as resource:
<resource identifier="res-course-settings" type="associatedcontent/imscc_xmlv1p3/learning-application-resource">
  <file href="course-settings.xml"/>
</resource>

# Step 5: Validate
/curriculum.validate-cc --package package.imscc | grep -i "gradebook"
```

**Note:** Some LMS platforms (Moodle, Blackboard) have limited gradebook import support. Canvas has the best support for CC gradebook configuration.

---

## Common Issues and Troubleshooting

### Issue 1: "Permission Denied" when writing to dist/

**Symptom:**
```
bash: dist/output.pdf: Permission denied
```

**Cause:** Directory permissions or file locked by another process

**Solution:**
```bash
# Check permissions
ls -la dist/

# Fix permissions
chmod 755 dist/
chmod 644 dist/*.pdf

# Check if file is open in another application
lsof | grep output.pdf  # macOS/Linux

# Close file and retry
```

---

### Issue 2: Broken Images in PDF

**Symptom:** PDF shows empty boxes or [IMAGE] placeholders

**Cause:** Pandoc can't find image files

**Solution:**
```bash
# Method 1: Use --resource-path
pandoc content.md --resource-path=assets:../assets -o output.pdf

# Method 2: Use absolute paths in markdown
# Change: ![](image.png)
# To: ![](/full/path/to/image.png)

# Method 3: Copy images to same directory
cp assets/*.png .
pandoc content.md -o output.pdf
```

---

### Issue 3: SCORM Package Works in One LMS But Not Another

**Symptom:** Package launches in Canvas but fails in Moodle (or vice versa)

**Cause:** LMS-specific SCORM implementation differences

**Solution:**
```javascript
// Robust API finder that works across LMS platforms
function findAPI(win) {
  let API = null;
  let findAttempts = 0;
  const maxAttempts = 500;

  while (!API && win.parent && win != win.parent && findAttempts < maxAttempts) {
    findAttempts++;

    // Check for SCORM 1.2
    if (win.parent.API) {
      API = win.parent.API;
      break;
    }

    // Check for SCORM 2004
    if (win.parent.API_1484_11) {
      API = win.parent.API_1484_11;
      break;
    }

    win = win.parent;
  }

  return API;
}
```

Test in multiple LMS platforms before final delivery.

---

### Issue 4: HTML Looks Different in Different Browsers

**Symptom:** Chrome looks great, Firefox has layout issues, Safari has font problems

**Cause:** Browser-specific CSS rendering differences

**Solution:**
```css
/* Use CSS reset to normalize across browsers */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Use standard web-safe fonts as fallbacks */
body {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

/* Test with vendor prefixes for newer CSS */
.element {
  display: -webkit-flex;
  display: flex;
}

/* Use feature detection, not browser detection */
@supports (display: grid) {
  .container {
    display: grid;
  }
}
```

Test in: Chrome, Firefox, Safari, Edge

---

### Issue 5: PDF File Size Too Large (50+ MB)

**Symptom:** PDF is slow to open, too large to email

**Cause:** Unoptimized images

**Solution:**
```bash
# Optimize images BEFORE Pandoc
find assets/ -name "*.jpg" -exec convert {} -resize 1200x -quality 85 {} \;
find assets/ -name "*.png" -exec optipng -o5 {} \;

# Or compress existing PDF
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output-compressed.pdf input.pdf

# Check size reduction
ls -lh input.pdf output-compressed.pdf
```

---

### Issue 6: Video Won't Play in SCORM Package

**Symptom:** Video shows but doesn't play when clicked

**Cause:** Incorrect MIME type or codec

**Solution:**
```html
<!-- Use multiple formats -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  Your browser doesn't support video.
</video>

<!-- Ensure server sends correct MIME types -->
<!-- .mp4 → video/mp4 -->
<!-- .webm → video/webm -->

<!-- Convert to web-friendly codecs -->
ffmpeg -i input.mov -c:v libx264 -profile:v baseline -level 3.0 -c:a aac video.mp4
```

---

### Issue 7: LaTeX Template Changes Don't Apply

**Symptom:** Modified template, but PDF looks the same

**Cause:** Pandoc caching or using wrong template

**Solution:**
```bash
# Specify template explicitly
pandoc content.md --template=/full/path/to/template.latex -o output.pdf

# Clear Pandoc cache (if exists)
rm -rf ~/.pandoc/

# Verify template is being used
pandoc content.md --template=template.latex --verbose 2>&1 | grep template
```

---

### Issue 8: Accessibility Checker Fails on PDF

**Symptom:** PDF accessibility validation fails

**Cause:** Missing alt text, improper structure, no tags

**Solution:**
```latex
% In LaTeX template, enable PDF/UA tagging
\usepackage[pdfa]{hyperref}
\usepackage{pdfcomment}

% In markdown, always provide alt text
![Alt text describing image](image.png)

% Generate tagged PDF
pandoc content.md --pdf-engine=xelatex -o output.pdf

% Validate with Adobe Acrobat:
% Tools → Accessibility → Full Check
```

### Issue 9: Common Cartridge Imports But Content Missing

**Symptom:** CC package imports successfully but lessons/assessments don't appear in course

**Cause:**
- Missing or incorrect resource references in manifest
- Files not packaged correctly
- Resource type mismatch

**Solution:**
```bash
# Step 1: Verify package contents
unzip -l package.imscc | grep -E "(lessons|assessments)"

# Check all referenced files exist
/curriculum.validate-cc --package package.imscc | grep "Missing file"

# Step 2: Validate manifest structure
xmllint --noout imsmanifest.xml

# Check that items reference resources correctly:
<item identifier="lesson-1" identifierref="res-lesson-1">  <!-- Must match -->
  <title>Lesson 1</title>
</item>

<resource identifier="res-lesson-1" type="webcontent" href="lessons/lesson-1.html">
  <file href="lessons/lesson-1.html"/>
</resource>

# Step 3: Verify resource types
# Lessons: type="webcontent"
# Assessments: type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"
# Discussions: type="imsdt_xmlv1p3"
# LTI tools: type="imsbasiclti_xmlv1p0"

grep "type=" imsmanifest.xml | sort | uniq

# Step 4: Check organizations section
# All items must have identifierref pointing to valid resource

# Step 5: Re-package ensuring correct structure
cd package-source/
zip -r ../fixed-package.imscc *
# Note: imsmanifest.xml must be at root, not in subfolder

# Step 6: Test import again
# If still failing, check LMS import logs:
# Canvas: Course Settings → Import → View logs
# Moodle: Site Administration → Reports → Logs
```

**Prevention:**
- Always validate before packaging: `/curriculum.validate-cc --level thorough`
- Use curriculum.package-common-cartridge skill (handles structure automatically)
- Test in development LMS before delivering to customer

### Issue 10: QTI Assessments Import with Errors

**Symptom:**
- Canvas shows "Some questions could not be imported"
- Moodle shows "Invalid QTI format"
- Questions display incorrectly or are blank

**Cause:**
- Invalid QTI XML structure
- QTI version mismatch
- Missing response processing
- Unsupported item types

**Solution:**
```bash
# Step 1: Validate QTI XML structure
xmllint --noout assessments/quiz-1/assessment.xml

# If errors, check:
# - All opening tags have closing tags
# - Namespace declarations correct
# - CDATA sections properly formatted

# Step 2: Verify QTI version
grep "xmlns=" assessments/quiz-1/assessment.xml

# Should be QTI 2.1 for maximum compatibility:
# xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"

# Step 3: Check item structure
# Each assessment item must have:
# 1. responseDeclaration (correct answer)
# 2. outcomeDeclaration (scoring)
# 3. itemBody (question content)
# 4. responseProcessing (how to score)

<assessmentItem identifier="item-1">
  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
    <correctResponse>
      <value>choice-c</value>  <!-- REQUIRED -->
    </correctResponse>
  </responseDeclaration>

  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
    <defaultValue>
      <value>0</value>
    </defaultValue>
  </outcomeDeclaration>

  <itemBody>
    <!-- Question content -->
    <choiceInteraction responseIdentifier="RESPONSE" maxChoices="1">
      <prompt>Question text here</prompt>
      <simpleChoice identifier="choice-a">Answer A</simpleChoice>
      <simpleChoice identifier="choice-b">Answer B</simpleChoice>
      <simpleChoice identifier="choice-c">Answer C (correct)</simpleChoice>
    </choiceInteraction>
  </itemBody>

  <!-- REQUIRED: Response processing -->
  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"/>
</assessmentItem>

# Step 4: Validate with IMS QTI validator
# Use online validator: http://www.imsglobal.org/developers/qti/validate

# Step 5: Check for unsupported item types
# Stick to these for maximum compatibility:
# - choiceInteraction (MC, TF)
# - textEntryInteraction (fill-in-blank)
# - extendedTextInteraction (essay)
# - matchInteraction (matching)

# Avoid complex interactions in QTI 2.1:
# - Custom interactions
# - Drawing interactions
# - Advanced hotspots

# Step 6: Test QTI file separately
# Import just the QTI assessment (without CC package)
# If it works alone, issue is in CC manifest
# If it fails alone, issue is in QTI XML

# Step 7: Regenerate QTI if needed
/curriculum.export-qti \
  --assessment "quiz-source.json" \
  --output "assessments/quiz-1/" \
  --version "2.1" \
  --validate

# Step 8: Verify in CC manifest
# Check resource declaration correct:
<resource identifier="res-quiz-1"
          type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment"
          href="assessments/quiz-1/assessment_meta.xml">
  <file href="assessments/quiz-1/assessment_meta.xml"/>
  <dependency identifierref="res-quiz-1-qti"/>
</resource>

<resource identifier="res-quiz-1-qti"
          type="associatedcontent/imscc_xmlv1p3/learning-application-resource">
  <file href="assessments/quiz-1/assessment.xml"/>
</resource>
```

**Common QTI Errors:**
1. **Missing correctResponse** - Assessment won't score
2. **Wrong responseIdentifier** - Answers won't record
3. **No responseProcessing** - Can't determine correct/incorrect
4. **Invalid choice identifiers** - Must match in correctResponse
5. **Missing CDATA sections** - Special characters break XML

**Prevention:**
- Use curriculum.export-qti skill (generates valid QTI)
- Always validate: `xmllint --noout assessment.xml`
- Test in target LMS before delivery
- Stick to QTI 2.1 for compatibility
- Use standard item types (avoid custom interactions)

---

## Production Metrics and Analytics

### Key Metrics to Track

**1. Production Time**
```bash
# Track time per content type
echo "Lesson 3.2 PDF: 1.5 hours" >> production-log.txt
echo "Lesson 3.2 HTML: 2 hours" >> production-log.txt
echo "Lesson 3.2 SCORM: 1 hour" >> production-log.txt

# Calculate averages
awk -F: '{sum+=$2; count++} END {print "Average:", sum/count, "hours"}' production-log.txt
```

**2. File Sizes**
```bash
# Track output sizes
ls -lh dist/pdf/*.pdf | awk '{print $5, $9}' > size-report.txt

# Calculate total size per format
du -sh dist/pdf dist/html dist/scorm
```

**3. Quality Metrics**
- PDF rendering issues: 0 per file (target)
- WCAG violations: 0 per HTML file (target)
- SCORM launch failures: <1% (target)
- Asset optimization: >70% size reduction (target)

**4. Throughput**
```bash
# Lessons produced per week
find dist/ -name "*.pdf" -mtime -7 | wc -l

# Formats produced per lesson
find dist/ -type d -mindepth 2 | cut -d/ -f2 | sort | uniq -c
```

### Weekly Production Report Template

```markdown
# Production Report - Week of [DATE]

## Output Summary
- Lessons produced: 12
- Assessments produced: 5
- Total deliverables: 34 (PDF: 15, HTML: 10, SCORM: 9)

## Time Metrics
- Average time per lesson: 4.2 hours (down from 5.1 last week)
- Total production time: 68 hours
- Fastest production: 2.5 hours (Lesson 4.3)
- Slowest production: 7 hours (Lesson 5.1 - complex interactive)

## Quality Metrics
- PDFs with rendering issues: 0
- WCAG violations found: 2 (both fixed)
- SCORM packages tested: 9 (100% launch success)
- Average file size: PDF 4.2 MB, HTML 1.8 MB

## Issues Encountered
- LaTeX compilation error on Lesson 4.8 (resolved: missing image)
- SCORM API timeout in Moodle (resolved: increased timeout)

## Process Improvements
- Implemented batch image optimization script (saved 3 hours/week)
- Created SCORM template with robust API finder (reduced LMS issues)

## Next Week Goals
- Produce 15 lessons
- Reduce average production time to <4 hours
- Implement automated QA checks
```

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
