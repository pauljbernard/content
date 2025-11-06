# Professional Print Production Skill

**Skill**: `/curriculum.print-production`
**Category**: Curriculum Delivery
**Addresses**: GAP-2 (CRITICAL)
**Purpose**: Generate commercial-quality print-ready PDFs for textbooks, workbooks, and supplementary materials

## Description

Produces print-ready PDF/X-1a compliant files with professional typography, page layout, bleeds, crop marks, running headers/footers, automatic table of contents, and indexes. Meets commercial printing standards for K-12 textbook publishers.

## Usage

```bash
/curriculum.print-production \
  --input "curriculum-content/" \
  --output-type "textbook|workbook|teacher-guide|test-booklet" \
  --page-size "8.5x11|8x10|6x9" \
  --color-mode "cmyk|grayscale" \
  --binding "perfect-bound|saddle-stitch|spiral" \
  --quality "print-ready|review-draft"
```

## Output Types

### 1. Student Textbook

Professional hardcover/softcover textbook with full features.

**Features**:
- Professional typography (Minion Pro, Myriad Pro, or custom fonts)
- Multi-column layouts where appropriate
- Running headers with chapter/section titles
- Running footers with page numbers
- Automatic table of contents with page numbers
- Automatic index generation
- Glossary with alphabetical organization
- Image placement with captions and credits
- Sidebar boxes for supplementary information
- End-of-chapter review sections
- Standards alignment references

**Specifications**:
- Bleed: 0.125" on all sides
- Trim size: 8.5" x 11" (or custom)
- Margins: 0.75" inside, 0.625" outside, 0.75" top, 0.875" bottom
- Gutter: 0.25" additional for perfect binding
- Color: CMYK (Coated or Uncoated)
- Resolution: 300 DPI minimum for images
- Font embedding: Full
- PDF/X-1a:2001 compliance

### 2. Student Workbook

Consumable workbook with practice activities and writing spaces.

**Features**:
- Open page layout for writing
- Lined/gridded writing spaces
- Answer blanks with proper sizing
- Practice problem sets
- Activity instructions
- Perforated pages (marked with perforation lines)
- 3-hole punch guides (if specified)

**Specifications**:
- Lighter weight paper (marked in print specs)
- Larger margins for binding
- High-contrast for photocopying
- Grayscale option for cost savings

### 3. Teacher Guide

Comprehensive teacher edition with annotations and answer keys.

**Features**:
- Reduced student pages with teacher annotations
- Marginal notes with teaching tips
- Answer keys (inline or separate section)
- Pacing guides
- Differentiation strategies
- Assessment guidance
- Standards correlation charts
- Additional resources references

**Specifications**:
- Larger page size (8.5" x 11" for 6" x 9" student book)
- Teacher annotations in different color (typically red or blue)
- Tabbed sections for quick navigation

### 4. Assessment Test Booklet

Standardized test format with answer sheets.

**Features**:
- Clear, uncluttered layout
- Adequate white space
- Answer bubbles or writing spaces
- Instructions on each section
- Separate answer sheet option
- Secure test marking (sequential numbering)

**Specifications**:
- High contrast for scanning
- Optical mark recognition (OMR) compatible
- Standard test fonts (Arial, Times New Roman)
- Numbered items with clear breaks

## Advanced Features

### Typography

**Professional Font Stack**:
- Body text: Minion Pro, Garamond, or custom
- Headings: Myriad Pro, Frutiger, or custom
- Math: Computer Modern, STIX, or MathTime
- Code: Fira Code, Consolas (if technical content)

**Typography Settings**:
- Leading (line spacing): 120-145% of font size
- Kerning: Optical kerning enabled
- Hyphenation: Smart hyphenation with 2-3 character minimum
- Widow/orphan control: Enabled
- Paragraph spacing: 0.5-1em between paragraphs
- Justification: Full justification for body text, left-aligned for activities

### Page Layout

**Master Pages**:
- Front matter (title, copyright, TOC)
- Chapter opener (full-page with chapter title and objectives)
- Standard text page (two-column or single-column)
- Activity page (single column with generous margins)
- End-of-chapter review
- Glossary/index

**Running Headers/Footers**:
- Left page header: Book title or unit title
- Right page header: Chapter title or section title
- Footer: Page number (centered or outside corner)
- First page of chapter: No header, footer only

### Automatic Front/Back Matter

**Front Matter** (auto-generated):
- Title page with curriculum details
- Copyright page with ISBN, edition, credits
- Table of contents with page numbers (hyperlinked in PDF)
- "How to Use This Book" section
- Standards correlation chart

**Back Matter** (auto-generated):
- Glossary (alphabetically sorted from content)
- Index (auto-generated from keywords and concepts)
- Credits (image attributions, permissions)
- Answer key (optional, or in teacher guide)

### Print Production Specs

**PDF/X-1a Compliance**:
- All fonts embedded (no font substitution)
- All colors CMYK (no RGB or spot colors)
- No transparency (flattened)
- Trim box defined
- Bleed box defined
- Output intent: US Web Coated (SWOP) v2

**Prepress Marks**:
- Crop marks (0.25" outside bleed)
- Registration marks
- Color bars (CMYK)
- Page information (filename, date, plate)
- Fold marks (if applicable)

**Image Requirements**:
- Minimum resolution: 300 DPI at final size
- Maximum resolution: 600 DPI (to avoid file bloat)
- Format: TIFF or high-quality JPEG
- Color space: CMYK (converted from RGB if needed)
- Embedded ICC profiles

### Quality Checks

Before finalizing print-ready PDF:
- ✅ All images at 300+ DPI
- ✅ All fonts embedded
- ✅ No RGB colors (CMYK only)
- ✅ Bleed present on all edge-to-edge content
- ✅ No content in trim area (safe zone)
- ✅ Page numbers sequential
- ✅ TOC page numbers match actual pages
- ✅ Index entries present on referenced pages
- ✅ Running headers match chapter/section
- ✅ Widow/orphan control applied
- ✅ PDF/X-1a validation passes
- ✅ File size optimized (<50MB per 100 pages)

## Use Cases

### Use Case 1: Textbook Publisher

**Scenario**: EdVenture Learning needs print-ready PDFs for 300-page 7th Grade Math textbook.

```bash
/curriculum.print-production \
  --input "7th-grade-math/final-content/" \
  --output-type "textbook" \
  --page-size "8.5x11" \
  --color-mode "cmyk" \
  --binding "perfect-bound" \
  --quality "print-ready" \
  --isbn "978-1-234567-89-0" \
  --edition "2025 Edition" \
  --copyright-year "2025" \
  --include-toc \
  --include-index \
  --include-glossary \
  --running-headers
```

**Output**:
- `7th-grade-math-textbook-PRINT.pdf` (PDF/X-1a compliant)
- `print-specifications.json` (paper stock, binding, page count)
- `prepress-report.html` (quality check results)

### Use Case 2: Workbook with Answer Key

**Scenario**: Create consumable student workbook and separate teacher answer key.

```bash
# Student workbook
/curriculum.print-production \
  --input "7th-grade-math/workbook-activities/" \
  --output-type "workbook" \
  --page-size "8.5x11" \
  --color-mode "grayscale" \
  --binding "saddle-stitch" \
  --quality "print-ready" \
  --perforated-pages \
  --3-hole-punch-guides

# Teacher answer key
/curriculum.print-production \
  --input "7th-grade-math/workbook-activities/" \
  --output-type "teacher-guide" \
  --page-size "8.5x11" \
  --color-mode "grayscale" \
  --binding "saddle-stitch" \
  --quality "print-ready" \
  --include-answers
```

### Use Case 3: Review Draft

**Scenario**: Generate low-cost PDF for internal review before final print production.

```bash
/curriculum.print-production \
  --input "7th-grade-math/draft-content/" \
  --output-type "textbook" \
  --page-size "8.5x11" \
  --color-mode "grayscale" \
  --quality "review-draft" \
  --watermark "DRAFT - NOT FOR DISTRIBUTION"
```

**Output**:
- RGB colors (for screen viewing)
- Lower image resolution (150 DPI)
- No bleed/crop marks
- Watermarked pages
- Faster generation time

## Implementation

### Technology Stack

**PDF Generation**:
- **Python**: ReportLab (advanced page layout) or WeasyPrint (HTML to PDF)
- **LaTeX**: XeLaTeX for professional typography (academic textbooks)
- **Adobe InDesign Scripting**: If InDesign server available (highest quality)

**Recommended Approach**: LaTeX with custom document class
- Reason: Best typography, proven for textbook production
- `xelatex` engine for modern fonts and Unicode support
- Custom `.cls` file for textbook layouts
- `memoir` document class as base

### LaTeX Document Class Structure

```latex
\documentclass[12pt,openright,twoside]{textbook-professor}

% Packages for professional features
\usepackage{fontspec}         % Modern fonts
\usepackage{geometry}         % Page layout
\usepackage{fancyhdr}         % Headers/footers
\usepackage{graphicx}         % Images
\usepackage{tikz}             % Diagrams
\usepackage{tcolorbox}        % Sidebar boxes
\usepackage{imakeidx}         % Index generation
\usepackage[hidelinks]{hyperref} % PDF hyperlinks

% PDF/X-1a settings
\usepackage[x-1a]{pdfx}

% Professional typography
\setmainfont{Minion Pro}
\setsansfont{Myriad Pro}
\setmonofont{Fira Code}

% Page geometry with bleed
\geometry{
  paperwidth=8.75in,  % 8.5" + 0.25" bleed
  paperheight=11.25in, % 11" + 0.25" bleed
  textwidth=6in,
  textheight=8.5in,
  inner=1in,
  outer=0.75in,
  top=1in,
  bottom=1.25in
}
```

### Alternative: HTML to PDF (WeasyPrint)

For simpler layouts or integration with web workflows:

```python
from weasyprint import HTML, CSS

# HTML content with semantic markup
html_content = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>7th Grade Mathematics</title>
  <link rel="stylesheet" href="textbook-styles.css">
</head>
<body>
  <div class="front-matter">
    <h1 class="title">7th Grade Mathematics</h1>
    <p class="edition">2025 Edition</p>
  </div>
  <div class="toc">
    <!-- Auto-generated TOC -->
  </div>
  <chapter id="chapter-1">
    <h1>Chapter 1: Rational Numbers</h1>
    <!-- Content -->
  </chapter>
</body>
</html>
"""

# CSS for print layout
css = CSS(string="""
@page {
  size: 8.5in 11in;
  margin: 0.75in 0.625in 0.875in 0.75in;
  bleed: 0.125in;

  @top-left {
    content: "7th Grade Mathematics";
    font-family: 'Myriad Pro', sans-serif;
    font-size: 10pt;
  }

  @top-right {
    content: string(chapter-title);
    font-family: 'Myriad Pro', sans-serif;
    font-size: 10pt;
  }

  @bottom-center {
    content: counter(page);
  }
}

body {
  font-family: 'Minion Pro', serif;
  font-size: 12pt;
  line-height: 1.4;
  text-align: justify;
  hyphens: auto;
}

h1 {
  font-family: 'Myriad Pro', sans-serif;
  color: cmyk(100%, 60%, 0%, 20%);
  page-break-before: always;
}
""")

# Generate PDF/X-1a
HTML(string=html_content).write_pdf(
  'textbook-output.pdf',
  stylesheets=[css],
  pdf_variant='pdf/x-1a'
)
```

## Integration with Existing Skills

Enhances `/curriculum.package-pdf` with professional print features:

```bash
# Basic PDF packaging (existing)
/curriculum.package-pdf --input "content/" --output "basic.pdf"

# Professional print production (new)
/curriculum.print-production --input "content/" --quality "print-ready"
```

## Performance Metrics

- **Generation time**: 1-2 minutes per 50 pages (with images)
- **File size**: 30-40MB per 100 pages (optimized)
- **Image processing**: 300 DPI conversion from source
- **Quality validation**: Automatic prepress check in <30 seconds

## Success Criteria

- ✅ PDF/X-1a validation passes (Adobe Acrobat Preflight)
- ✅ Commercial printers accept files without errors
- ✅ Typography meets professional publishing standards
- ✅ Automatic TOC and index reduce manual work by 90%
- ✅ 60% of textbook publishers can eliminate InDesign step

---

**Status**: Ready for implementation
**Dependencies**: `/curriculum.package-pdf` (extends), LaTeX (xelatex) or WeasyPrint
**Testing**: Requires sample 50-page curriculum and print validation
