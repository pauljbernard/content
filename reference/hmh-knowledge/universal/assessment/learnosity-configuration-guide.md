# Learnosity Configuration Guide
**Technical Reference for Assessment Item Authoring**
**Platform:** Learnosity v2023.3.LTS
**Audience:** Curriculum developers and assessment authors
**Approved Item Types:** 24 (see Item Types Reference)

---

## Overview

**Learnosity** is HMH's digital assessment platform for creating, delivering, and scoring interactive assessment items. This guide covers technical configuration, JSON structure, scoring logic, and best practices.

**Core Principle:** Correct technical configuration ensures items function properly, score accurately, and provide consistent student experience.

---

## Platform Basics

### Learnosity Author API:
- Web-based authoring interface
- WYSIWYG editor for item creation
- JSON-based item structure
- Real-time preview

### Key Components:
- **Items:** Individual assessment questions
- **Activities:** Collections of items
- **Item Banks:** Organized storage of items
- **Scoring:** Automatic or manual scoring rules
- **Metadata:** TEKS, DOK, item type, tags

---

## The 24 Approved Item Types

### Quick Reference:

| Category | Item Types | Learnosity Type Code |
|----------|-----------|---------------------|
| **Multiple Choice** | MCQ Standard, MCQ Multiple Response, Choice Matrix | `mcq`, `mcqmulti`, `choicematrix` |
| **Fill in Blank** | Cloze Drag&Drop, Cloze Dropdown, Label Image DND, Label Image Dropdown | `clozeassociation`, `clozedropdown`, `imageclozeassociation`, `imageclozedropdown` |
| **Math** | Simple Formula, Formula Essay | `formulaV2`, `formulaessay` |
| **Essay** | Essay Plain Text, Essay Rich Text | `plaintext`, `longtextV2` |
| **Drawing** | Drawing Response | `drawing` |
| **Graphing** | Number Line Plot, Graphing | `numberlineplot`, `graphplotting` |
| **Charts** | Chart, Bar Model | `chart`, `customchart` |
| **Classification** | Classification, Sort List, Match List | `classification`, `sortlist`, `association` |
| **Ordering** | Order List | `orderlist` |
| **Hotspot** | Hotspot, Image Hotspot | `hotspot`, `imagehotspot` |
| **Audio** | Audio | `audio` |

**Full Details:** See `/assessment/item-types-reference.md`

---

## JSON Structure Fundamentals

### Basic Item JSON Structure:

```json
{
  "type": "mcq",
  "stimulus": "<p>Question stem text</p>",
  "stimulus_review": "<p>Optional different text for review mode</p>",
  "options": [
    {"label": "A", "value": "0"},
    {"label": "B", "value": "1"},
    {"label": "C", "value": "2"},
    {"label": "D", "value": "3"}
  ],
  "valid_response": {
    "score": 1,
    "value": "1"
  },
  "metadata": {
    "distractor_rationale_response_level": [
      {"key": "0", "distractor_rationale": "Explanation for A"},
      {"key": "1", "distractor_rationale": "Correct! Explanation"},
      {"key": "2", "distractor_rationale": "Explanation for C"},
      {"key": "3", "distractor_rationale": "Explanation for D"}
    ]
  }
}
```

### Key Fields:

**`type`** (required)
- Learnosity item type code
- Example: `"mcq"`, `"formulaV2"`, `"plaintext"`

**`stimulus`** (required)
- Question stem or prompt
- HTML formatted
- Can include images, MathML

**`valid_response`** (required for auto-scored)
- Defines correct answer(s)
- Scoring configuration

**`options`** (for choice-based items)
- Answer choices
- Labels and values

**`metadata`** (recommended)
- Feedback, rationale, tags
- TEKS, DOK codes
- Item bank organization

---

## Configuration by Item Type Category

### 1. Multiple Choice Configuration

#### Standard MCQ (Single Select):

```json
{
  "type": "mcq",
  "stimulus": "<p>What is 7 × 8?</p>",
  "options": [
    {"label": "A", "value": "54"},
    {"label": "B", "value": "56"},
    {"label": "C", "value": "64"},
    {"label": "D", "value": "15"}
  ],
  "valid_response": {
    "score": 1,
    "value": "56"
  },
  "ui_style": {
    "type": "horizontal",
    "choice_label": "upper-alpha"
  }
}
```

**Key Configurations:**
- `ui_style.type`: `"horizontal"` or `"vertical"` (layout)
- `ui_style.choice_label`: `"upper-alpha"` (A, B, C) or `"number"` (1, 2, 3)
- `shuffle_options`: `true` to randomize order

---

#### MCQ Multiple Response (Select All):

```json
{
  "type": "mcqmulti",
  "stimulus": "<p>Select all even numbers:</p>",
  "options": [
    {"label": "A", "value": "2"},
    {"label": "B", "value": "3"},
    {"label": "C", "value": "4"},
    {"label": "D", "value": "5"},
    {"label": "E", "value": "6"}
  ],
  "valid_response": {
    "score": 1,
    "value": ["2", "4", "6"]
  },
  "multiple_responses": true
}
```

**Key Configurations:**
- `multiple_responses`: `true` (enables checkboxes)
- `valid_response.value`: Array of correct values
- Partial credit: Use `alt_responses` for partial scoring

---

### 2. Math Response Configuration

#### Simple Formula (Numerical Answer):

```json
{
  "type": "formulaV2",
  "stimulus": "<p>Calculate: 45 + 37</p>",
  "template": "{{response}}",
  "valid_response": {
    "score": 1,
    "value": [
      {"method": "equivLiteral", "value": "82", "options": {}}
    ]
  },
  "ui_style": {
    "type": "floating-keyboard"
  }
}
```

**Key Configurations:**
- `template`: Defines input area (usually `"{{response}}"`)
- `valid_response.value[0].method`: Scoring method
  - `"equivLiteral"`: Exact match
  - `"equivSymbolic"`: Mathematically equivalent
  - `"equivValue"`: Numerically equivalent
- `ui_style.type`: `"floating-keyboard"` for numeric keypad

**Validation Methods:**

| Method | Use Case | Example |
|--------|----------|---------|
| `equivLiteral` | Exact string match | "3/4" matches only "3/4" |
| `equivSymbolic` | Symbolic equivalence | "3/4" matches "6/8", "0.75" |
| `equivValue` | Numerical value | "0.75" matches "3/4" within tolerance |

---

#### Formula Essay (Show Work + Answer):

```json
{
  "type": "formulaessay",
  "stimulus": "<p>Solve: 3x + 7 = 22. Show your work.</p>",
  "template": "{{response}}",
  "is_math": true,
  "ui_style": {
    "type": "block-on-focus-keyboard",
    "min_height": "200px"
  },
  "validation": {
    "scoring_type": "manual"
  }
}
```

**Key Configurations:**
- `is_math`: `true` enables math keyboard
- `ui_style.min_height`: Defines work area size
- `validation.scoring_type`: `"manual"` (requires human scoring)

---

### 3. Essay/Text Response Configuration

#### Plain Text Essay:

```json
{
  "type": "plaintext",
  "stimulus": "<p>Explain your reasoning.</p>",
  "max_length": 500,
  "show_word_count": true,
  "spellcheck": true,
  "validation": {
    "scoring_type": "manual",
    "max_score": 2
  }
}
```

**Key Configurations:**
- `max_length`: Character limit
- `show_word_count`: Display word counter
- `spellcheck`: Enable spell check
- `validation.max_score`: Points possible (for rubric)

---

### 4. Cloze (Fill-in-Blank) Configuration

#### Cloze Dropdown:

```json
{
  "type": "clozedropdown",
  "stimulus": "<p>The area of a rectangle is found by multiplying {{response}} times {{response}}.</p>",
  "possible_responses": [
    ["length", "width", "perimeter", "height"],
    ["length", "width", "perimeter", "height"]
  ],
  "valid_response": {
    "score": 1,
    "value": ["length", "width"]
  }
}
```

**Key Configurations:**
- `possible_responses`: Array of options for each blank
- `{{response}}`: Placeholder in stimulus for each blank
- Order of `possible_responses` matches order of `{{response}}`

---

#### Cloze Drag & Drop:

```json
{
  "type": "clozeassociation",
  "stimulus": "<p>Complete: 2 + 3 = {{response}}</p>",
  "possible_responses": ["4", "5", "6", "7"],
  "valid_response": {
    "score": 1,
    "value": ["5"]
  },
  "duplicate_responses": false
}
```

**Key Configurations:**
- `duplicate_responses`: `false` prevents reusing choices
- `possible_responses`: Draggable choices (can include distractors)

---

### 5. Graphing Configuration

#### Number Line Plot:

```json
{
  "type": "numberlineplot",
  "stimulus": "<p>Plot 3.5 on the number line.</p>",
  "is_math": true,
  "points": [3.5],
  "line": {
    "min": 0,
    "max": 5,
    "step": 0.5,
    "show_min": true,
    "show_max": true
  },
  "valid_response": {
    "score": 1,
    "value": {
      "points": [3.5]
    }
  }
}
```

**Key Configurations:**
- `line.min`, `line.max`: Number line range
- `line.step`: Interval size
- `points`: Expected point values

---

#### Graphing (Coordinate Plane):

```json
{
  "type": "graphplotting",
  "stimulus": "<p>Plot points (2, 3) and (4, 5). Draw a line through them.</p>",
  "canvas": {
    "x_min": 0,
    "x_max": 10,
    "y_min": 0,
    "y_max": 10
  },
  "toolbar": {
    "tools": ["point", "line", "move", "delete"]
  },
  "valid_response": {
    "score": 1,
    "value": {
      "points": [[2, 3], [4, 5]],
      "line": [[2, 3], [4, 5]]
    }
  },
  "validation": {
    "scoring_type": "manual"
  }
}
```

**Key Configurations:**
- `canvas`: Defines graphing grid
- `toolbar.tools`: Which tools students can use
- Often scored manually for complex graphs

---

### 6. Drawing Configuration

#### Drawing Response:

```json
{
  "type": "drawing",
  "stimulus": "<p>Draw an array showing 3 × 4.</p>",
  "toolbar": {
    "tools": ["circle", "rectangle", "line", "pen", "eraser"]
  },
  "canvas": {
    "width": 600,
    "height": 400
  },
  "validation": {
    "scoring_type": "manual",
    "max_score": 2
  }
}
```

**Key Configurations:**
- `toolbar.tools`: Available drawing tools
- `canvas`: Drawing area dimensions
- Always manual scoring

---

### 7. Classification Configuration

#### Classification (Drag into Categories):

```json
{
  "type": "classification",
  "stimulus": "<p>Sort shapes by number of sides:</p>",
  "possible_responses": ["triangle", "square", "pentagon", "hexagon"],
  "categories": ["3 sides", "4 sides", "5+ sides"],
  "valid_response": {
    "score": 1,
    "value": {
      "3 sides": ["triangle"],
      "4 sides": ["square"],
      "5+ sides": ["pentagon", "hexagon"]
    }
  }
}
```

**Key Configurations:**
- `possible_responses`: Items to classify
- `categories`: Classification bins
- `valid_response.value`: Object mapping categories to items

---

## Scoring Configuration

### Automatic Scoring:

**Exact Match:**
```json
"valid_response": {
  "score": 1,
  "value": "42"
}
```

**Multiple Correct Answers:**
```json
"valid_response": {
  "score": 1,
  "value": ["0.5", "1/2", "50%"]
}
```

**Partial Credit:**
```json
"valid_response": {
  "score": 2,
  "value": ["A", "B", "C"]
},
"alt_responses": [
  {"score": 1, "value": ["A", "B"]},
  {"score": 1, "value": ["A", "C"]}
]
```

---

### Manual Scoring:

**For Constructed Response:**
```json
"validation": {
  "scoring_type": "manual",
  "max_score": 2
}
```

**Rubric Stored in Metadata:**
```json
"metadata": {
  "rubric": "2 points: Complete and accurate...\n1 point: Partially correct...\n0 points: Incorrect..."
}
```

---

## Metadata Configuration

### Required Metadata Fields:

```json
"metadata": {
  "teks": "5.3A",
  "dok": "2",
  "item_type": "mcq",
  "grade": "5",
  "subject": "mathematics",
  "question_type": "multiple-choice"
}
```

---

### Optional Metadata Fields:

```json
"metadata": {
  "distractor_rationale_response_level": [
    {"key": "A", "distractor_rationale": "Explanation for A"},
    {"key": "B", "distractor_rationale": "Correct! Explanation for B"}
  ],
  "rubric": "Scoring rubric text...",
  "difficulty": "medium",
  "time_estimate": 60,
  "tags": ["multiplication", "word-problem", "measurement"]
}
```

**Key Uses:**
- `distractor_rationale`: Feedback for each answer choice
- `rubric`: Scoring guidance for manual items
- `tags`: Organization and searchability

---

## Validation Rules

### Answer Validation:

**For Math Items, Specify Equivalence:**

```json
"valid_response": {
  "score": 1,
  "value": [
    {
      "method": "equivSymbolic",
      "value": "3/4",
      "options": {}
    }
  ]
}
```

**For Rounding:**
```json
"valid_response": {
  "score": 1,
  "value": [
    {
      "method": "equivValue",
      "value": "12.57",
      "options": {
        "tolerance": 0.01
      }
    }
  ]
}
```

---

### Input Validation:

**Restrict Input Type:**

```json
"ui_style": {
  "type": "floating-keyboard",
  "keyboard_below": true
},
"text_blocks": [
  {
    "validation": {
      "allow_decimal": true,
      "allow_negative": false
    }
  }
]
```

**Character Limits:**
```json
"max_length": 500
```

---

## Accessibility Configuration

### Alt Text:

```json
"stimulus": "<p>What is the area?</p><img src='rectangle.png' alt='Rectangle with length 12 cm and width 7 cm' />"
```

**Rule:** All `<img>` tags must have `alt` attribute.

---

### Screen Reader Support:

**Use Semantic HTML:**
```json
"stimulus": "<p><strong>Question 1:</strong> Calculate the perimeter.</p>"
```

**MathML for Math Content:**
```json
"stimulus": "<p>Solve: <math><mrow><mn>3</mn><mi>x</mi><mo>+</mo><mn>5</mn></mrow></math></p>"
```

---

### Keyboard Navigation:

**Ensure Keyboard Access:**
- All interactive elements must be keyboard-navigable
- Tested with Tab key navigation
- Focus indicators visible

---

## Preview and Testing

### Preview Modes:

**1. Author Preview:**
- View as student would see
- Test all interactions
- Check scoring logic

**2. Print Preview:**
- Verify print layout
- Check parity with digital

**3. Accessibility Preview:**
- Test with screen reader
- Verify keyboard navigation
- Check color contrast

---

### Testing Checklist:

**Functionality:**
- [ ] Item renders correctly
- [ ] All interactions work (buttons, dropdowns, drag-drop)
- [ ] Scoring logic tested with sample responses
- [ ] Correct answers award full points
- [ ] Incorrect answers award 0 points
- [ ] Partial credit works (if applicable)

**Content:**
- [ ] Stem is clear and unambiguous
- [ ] All images display
- [ ] Alt text provided
- [ ] MathML renders correctly
- [ ] No typos or errors

**Accessibility:**
- [ ] Alt text for all images
- [ ] Keyboard navigable
- [ ] Screen reader compatible
- [ ] Color not sole means of conveying info

**Metadata:**
- [ ] TEKS code correct
- [ ] DOK level accurate
- [ ] Item type tagged
- [ ] Tags applied

---

## Common Configuration Errors

### ❌ Error 1: Incorrect Scoring Method

**Problem:**
```json
"valid_response": {
  "value": "3/4"
}
```
Student enters "6/8" → marked incorrect (because equivLiteral is default)

**Fix:**
```json
"valid_response": {
  "value": [
    {"method": "equivSymbolic", "value": "3/4"}
  ]
}
```

---

### ❌ Error 2: Missing Alt Text

**Problem:**
```json
"stimulus": "<img src='diagram.png'>"
```

**Fix:**
```json
"stimulus": "<img src='diagram.png' alt='Rectangle partitioned into 8 equal parts with 3 shaded'>"
```

---

### ❌ Error 3: Broken Image Links

**Problem:** Relative path in JSON: `"src='images/fig1.png'"`

**Fix:** Use full asset path or CDN URL

---

### ❌ Error 4: Overly Strict Validation

**Problem:** Won't accept valid equivalent forms

**Fix:** Add all acceptable forms to `valid_response` array or use symbolic equivalence

---

### ❌ Error 5: No Manual Scoring Flag

**Problem:** Essay item without `"scoring_type": "manual"`

**Fix:**
```json
"validation": {
  "scoring_type": "manual",
  "max_score": 2
}
```

---

## JSON Best Practices

### 1. Use Consistent Formatting

**Good:**
```json
{
  "type": "mcq",
  "stimulus": "<p>Question text</p>",
  "options": [
    {"label": "A", "value": "1"},
    {"label": "B", "value": "2"}
  ]
}
```

**Poor:**
```json
{"type":"mcq","stimulus":"<p>Question text</p>","options":[{"label":"A","value":"1"},{"label":"B","value":"2"}]}
```

---

### 2. Validate JSON Syntax

**Use Validator:**
- JSON Lint: https://jsonlint.com/
- Learnosity Author API validator
- Text editor with JSON validation

---

### 3. Use Descriptive Metadata

**Good:**
```json
"metadata": {
  "teks": "6.3C",
  "dok": "2",
  "description": "Multiply fractions using area model"
}
```

**Poor:**
```json
"metadata": {}
```

---

### 4. Test Thoroughly

- Test correct answer → should score full points
- Test incorrect answer → should score 0 points
- Test partial answer → should score partial points (if applicable)
- Test edge cases (e.g., entering text in number field)

---

## Learnosity API Integration

### Activity Structure:

```json
{
  "activity_id": "math_grade5_unit3_lesson5",
  "title": "Lesson 5 Quick Check",
  "items": [
    {"reference": "item_12345"},
    {"reference": "item_12346"},
    {"reference": "item_12347"}
  ],
  "config": {
    "navigation": {
      "show_next": true,
      "show_prev": true,
      "show_submit": true
    },
    "time": {
      "max_time": 600
    }
  }
}
```

---

## Quick Reference: Configuration Checklist

### Before Publishing:

**JSON Structure:**
- [ ] Valid JSON syntax (no errors)
- [ ] All required fields present (`type`, `stimulus`, `valid_response`)
- [ ] Scoring configuration correct

**Content:**
- [ ] Question stem clear
- [ ] All images display
- [ ] Math rendered correctly (MathML)
- [ ] No typos

**Scoring:**
- [ ] Correct answers tested
- [ ] Incorrect answers tested
- [ ] Partial credit configured (if applicable)
- [ ] Manual scoring flagged (if applicable)

**Accessibility:**
- [ ] Alt text for all images
- [ ] Keyboard navigable
- [ ] Screen reader compatible

**Metadata:**
- [ ] TEKS code
- [ ] DOK level
- [ ] Item type
- [ ] Tags

**Parity:**
- [ ] Print version matches digital
- [ ] 3-question parity test passed

---

## Resources

**Related Guides:**
- Item Types Reference: `/assessment/item-types-reference.md`
- Parity Guidelines: `/assessment/parity-guidelines.md`
- Validation Methods: `/assessment/validation-methods.md`
- Scoring Rubrics: `/assessment/scoring-rubrics-guide.md`

**External:**
- Learnosity Author API Docs: https://authorapi.learnosity.com/
- Learnosity Question Types: https://help.learnosity.com/hc/en-us/articles/360000754858

**Tools:**
- JSON Validator: https://jsonlint.com/
- Learnosity Sandbox: Author API test environment

---

**Remember:** Correct Learnosity configuration ensures items function properly, score accurately, and provide accessible, consistent student experiences. Always test items thoroughly in preview mode before publishing. When in doubt, consult Learnosity documentation or HMH technical support.
