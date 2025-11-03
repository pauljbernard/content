# QTI (Question and Test Interoperability) Export Skill

**Skill**: `/curriculum.export-qti`
**Category**: Curriculum Delivery
**Addresses**: GAP-6 (HIGH)
**Purpose**: Export assessments to QTI 2.1/2.2 format for LMS integration (Canvas, Moodle, Blackboard)

## Description

Converts Professor-generated assessments into QTI (Question and Test Interoperability) 2.1 and 2.2 format for seamless integration with major Learning Management Systems. Includes item metadata, response processing, scoring, and feedback rules.

## Usage

```bash
/curriculum.export-qti \
  --input "assessments/unit-1-test.json" \
  --qti-version "2.1|2.2" \
  --package-format "content-package|item-bank" \
  --lms-target "canvas|moodle|blackboard|generic" \
  --include-metadata true \
  --output "unit-1-test-qti.zip"
```

## QTI Versions

### QTI 2.1 (IMS Question & Test Interoperability 2.1)

**Support**: Canvas, Moodle, Blackboard (older versions)

**Features**:
- Basic item types (multiple choice, true/false, short answer, essay)
- Simple response processing
- Basic feedback
- Item metadata
- Assessment metadata

**Use When**: Maximum LMS compatibility needed

### QTI 2.2 (IMS Question & Test Interoperability 2.2)

**Support**: Modern LMS versions (Canvas, Moodle 3.5+, Blackboard Learn)

**Features**:
- All QTI 2.1 features
- Advanced item types (inline choice, hotspot, drag-drop)
- Composite items (multiple parts)
- Adaptive item selection
- Complex scoring rules
- Conditional feedback
- Accessibility features (APIP)

**Use When**: Modern LMS with advanced assessment features

## Supported Item Types

### Basic Item Types (QTI 2.1 & 2.2)

**1. Multiple Choice (Single Select)**
```xml
<assessmentItem>
  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
    <correctResponse>
      <value>ChoiceA</value>
    </correctResponse>
  </responseDeclaration>
  <itemBody>
    <p>What is the capital of France?</p>
    <choiceInteraction responseIdentifier="RESPONSE" shuffle="true">
      <simpleChoice identifier="ChoiceA">Paris</simpleChoice>
      <simpleChoice identifier="ChoiceB">London</simpleChoice>
      <simpleChoice identifier="ChoiceC">Berlin</simpleChoice>
      <simpleChoice identifier="ChoiceD">Madrid</simpleChoice>
    </choiceInteraction>
  </itemBody>
</assessmentItem>
```

**2. Multiple Choice (Multiple Select)**
- Select all correct answers
- Partial credit supported
- Cardinality: "multiple"

**3. True/False**
- Boolean response
- Single correct answer
- Special case of multiple choice

**4. Fill-in-the-Blank (Text Entry)**
```xml
<textEntryInteraction responseIdentifier="RESPONSE" expectedLength="20"/>
```
- String matching (exact, case-insensitive, pattern)
- Multiple acceptable answers

**5. Numeric Response**
- Integer or float input
- Range matching (e.g., 3.14 ± 0.01)
- Significant figures validation

**6. Essay/Extended Response**
- Long text input
- Manual grading required
- Rubric association

**7. Matching**
- Match items from two lists
- One-to-one or many-to-one
- Partial credit by pair

### Advanced Item Types (QTI 2.2)

**8. Inline Choice**
- Dropdown menus within text
- Multiple dropdowns per item
- Each dropdown scored independently

**9. Hotspot**
- Click on image regions
- Defined polygons/rectangles as correct areas
- Multiple hotspots allowed

**10. Drag and Drop**
- Drag items to drop zones
- Reordering, categorizing, or labeling
- Complex scoring rules

**11. Graphic Gap Match**
- Drag images to image locations
- Visual matching tasks
- STEM diagram labeling

**12. Order Interaction**
- Put items in correct sequence
- All-or-nothing or partial credit
- Commonly used for procedure steps

## Metadata Inclusion

### Item Metadata

**Standards Alignment**:
```xml
<qti-metadata-extension>
  <lom:general>
    <lom:identifier>CCSS.Math.7.EE.A.1</lom:identifier>
    <lom:title>Apply properties of operations</lom:title>
  </lom:general>
  <lom:educational>
    <lom:learningResourceType>assessment item</lom:learningResourceType>
    <lom:difficulty>medium</lom:difficulty>
    <lom:typicalAgeRange>12-13</lom:typicalAgeRange>
  </lom:educational>
</qti-metadata-extension>
```

**Psychometric Metadata** (if available):
- Item difficulty (p-value)
- Discrimination index
- Point-biserial correlation
- Distractor analysis

**Instructional Metadata**:
- Bloom's taxonomy level
- Depth of Knowledge (DOK)
- Cognitive complexity
- Estimated time to complete
- Calculator allowed/required
- Prerequisites

### Assessment Metadata

**Test Structure**:
- Total points
- Time limit
- Number of items
- Section organization
- Navigation rules (linear, non-linear)
- Item presentation (one-at-a-time, all-at-once)

**Scoring Rules**:
- Total score calculation
- Cut scores for proficiency levels
- Weight by item or section
- Partial credit rules

## Package Formats

### 1. Content Package (for assessments)

**Structure**:
```
unit-1-test-qti.zip
├── imsmanifest.xml          # Package manifest (IMS Content Packaging)
├── items/
│   ├── item-001.xml
│   ├── item-002.xml
│   └── ...
├── assessments/
│   └── test-001.xml          # Test definition
├── media/
│   ├── image-001.png
│   └── audio-001.mp3
└── metadata/
    └── qti-metadata.xml
```

**imsmanifest.xml** (excerpt):
```xml
<manifest identifier="MANIFEST-001"
          xmlns="http://www.imsglobal.org/xsd/imscp_v1p1">
  <metadata>
    <schema>IMS Content</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations/>
  <resources>
    <resource identifier="RES-001" type="imsqti_item_xmlv2p1" href="items/item-001.xml">
      <file href="items/item-001.xml"/>
      <file href="media/image-001.png"/>
    </resource>
    <resource identifier="TEST-001" type="imsqti_assessment_xmlv2p1" href="assessments/test-001.xml">
      <file href="assessments/test-001.xml"/>
      <dependency identifierref="RES-001"/>
    </resource>
  </resources>
</manifest>
```

### 2. Item Bank Package

**Structure**:
```
item-bank-qti.zip
├── imsmanifest.xml
├── items/
│   ├── item-001.xml         # 5,000 items
│   ├── item-002.xml
│   └── ...
├── media/
│   └── ...
└── metadata/
    ├── taxonomy.xml          # Standards taxonomy
    └── psychometrics.csv     # Item statistics
```

**Use Case**: Assessment companies exporting entire item banks for integration with client LMS.

## Response Processing

### Simple Response Processing (QTI 2.1)

**Template-based scoring**:
```xml
<responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"/>
```

**Templates**:
- `match_correct`: All-or-nothing scoring
- `map_response`: Weighted scoring
- `map_response_point`: Partial credit

### Custom Response Processing (QTI 2.2)

**Complex rules**:
```xml
<responseProcessing>
  <setOutcomeValue identifier="SCORE">
    <sum>
      <mapResponse identifier="RESPONSE1"/>
      <mapResponse identifier="RESPONSE2"/>
      <baseValue baseType="float">5.0</baseValue> <!-- Bonus points -->
    </sum>
  </setOutcomeValue>
</responseProcessing>
```

**Use Cases**:
- Partial credit with custom weights
- Bonus points for speed
- Penalty for incorrect (negative scoring)
- Multi-part items with dependencies

## Feedback Rules

### Item-Level Feedback

**Correct/Incorrect Feedback**:
```xml
<modalFeedback outcomeIdentifier="FEEDBACK" identifier="correct" showHide="show">
  <p>Excellent! You correctly identified Paris as the capital of France.</p>
</modalFeedback>
<modalFeedback outcomeIdentifier="FEEDBACK" identifier="incorrect" showHide="show">
  <p>Not quite. Review the geography of Western Europe and try again.</p>
</modalFeedback>
```

**Distractor-Specific Feedback**:
```xml
<modalFeedback outcomeIdentifier="FEEDBACK" identifier="distractor-london" showHide="show">
  <p>London is the capital of the United Kingdom, not France.</p>
</modalFeedback>
```

### Test-Level Feedback

**Proficiency Level Feedback**:
- Score < 60%: "Needs Improvement - Review the material and retake."
- Score 60-79%: "Proficient - Good understanding with minor gaps."
- Score 80-100%: "Advanced - Excellent mastery of the content!"

## LMS-Specific Optimization

### Canvas

**Optimizations**:
- Use Canvas-specific metadata extensions
- Optimize for New Quizzes (Quizzes.Next)
- Include Canvas quiz settings JSON
- Test with Canvas QTI validator

**Canvas Extensions**:
```xml
<canvas:assessment>
  <canvas:points_possible>100</canvas:points_possible>
  <canvas:time_limit>60</canvas:time_limit>
  <canvas:allowed_attempts>3</canvas:allowed_attempts>
</canvas:assessment>
```

### Moodle

**Optimizations**:
- Use Moodle XML format alongside QTI (dual export)
- Include Moodle question bank categories
- Tag items with Moodle-specific metadata
- Test with Moodle QTI import

### Blackboard

**Optimizations**:
- Use Blackboard-specific item types (journal, file upload)
- Include Blackboard assessment settings
- Export to Blackboard Content Package format
- Test with Blackboard import validator

## Validation

### QTI Schema Validation

Validates XML against IMS QTI XSD schemas:
```bash
/curriculum.export-qti \
  --action "validate" \
  --input "unit-1-test-qti.zip" \
  --qti-version "2.2" \
  --strict-mode true
```

**Validation Checks**:
- ✅ XML well-formed
- ✅ Schema-compliant (QTI 2.1 or 2.2 XSD)
- ✅ All referenced files present
- ✅ Media files accessible
- ✅ Response processing valid
- ✅ Metadata complete
- ✅ Package structure correct

### LMS Import Testing

Automated testing of QTI import into target LMS:
```bash
/curriculum.export-qti \
  --action "test-import" \
  --input "unit-1-test-qti.zip" \
  --lms-target "canvas" \
  --lms-instance "https://canvas.instructure.com/api/v1" \
  --api-token "..."
```

**Test Results**:
- Import success/failure
- Item rendering screenshots
- Scoring accuracy verification
- Feedback display validation
- Metadata preservation check

## Use Cases

### Use Case 1: Export Unit Test to Canvas

**Scenario**: Export 7th Grade Math Unit 1 test (25 items) to Canvas.

```bash
/curriculum.export-qti \
  --input "assessments/7th-math-unit-1-test.json" \
  --qti-version "2.2" \
  --package-format "content-package" \
  --lms-target "canvas" \
  --include-metadata true \
  --standards-alignment "CCSS-Math" \
  --output "unit-1-test-canvas-qti.zip"
```

**Output**:
- `unit-1-test-canvas-qti.zip` (2.3 MB)
- 25 items with images and math notation (MathML)
- Standards alignment for each item
- Estimated time: 45 minutes
- Total points: 100
- Canvas-optimized settings

**Import to Canvas**:
1. Navigate to Quizzes → Import Quiz
2. Select "QTI .zip file"
3. Upload `unit-1-test-canvas-qti.zip`
4. Review and publish

### Use Case 2: Export 5,000-Item Assessment Bank

**Scenario**: TestCraft Pro exports entire item bank to Moodle for client.

```bash
/curriculum.export-qti \
  --input "item-bank/all-items.json" \
  --qti-version "2.1" \
  --package-format "item-bank" \
  --lms-target "moodle" \
  --include-metadata true \
  --include-psychometrics true \
  --output "testcraft-item-bank-moodle.zip"
```

**Output**:
- `testcraft-item-bank-moodle.zip` (487 MB)
- 5,000 items organized by subject and grade
- Psychometric data (difficulty, discrimination)
- Standards alignment (all 50 states)
- Moodle question bank categories

**Import to Moodle**:
1. Navigate to Question Bank → Import
2. Select "QTI 2.0 format"
3. Upload ZIP file
4. Map to Moodle categories
5. Items ready for test assembly

### Use Case 3: Multi-LMS Export

**Scenario**: Export same assessment to Canvas, Moodle, and Blackboard.

```bash
# Canvas
/curriculum.export-qti --input "test.json" --lms-target "canvas" --output "test-canvas.zip"

# Moodle
/curriculum.export-qti --input "test.json" --lms-target "moodle" --output "test-moodle.zip"

# Blackboard
/curriculum.export-qti --input "test.json" --lms-target "blackboard" --output "test-blackboard.zip"
```

**Result**: 3 LMS-optimized packages from single source.

### Use Case 4: Validate QTI Package

**Scenario**: Validate exported QTI before delivering to client.

```bash
/curriculum.export-qti \
  --action "validate" \
  --input "unit-1-test-qti.zip" \
  --qti-version "2.2" \
  --strict-mode true \
  --test-import true \
  --lms-target "canvas"
```

**Validation Report**:
- ✅ Schema validation: PASSED
- ✅ Package structure: PASSED
- ✅ Media files: PASSED (23/23 present)
- ✅ Canvas import: PASSED (test instance)
- ✅ Rendering: PASSED (screenshots captured)
- ⚠️ Warning: 2 items missing Bloom's taxonomy metadata
- Overall: PASSED with warnings

## Implementation

### Technology Stack

**QTI Generation**:
- **Python**: `lxml` (XML generation), `jinja2` (XML templates)
- **Validation**: `xmlschema` (XSD validation)
- **Packaging**: `zipfile` (content package creation)

**LMS Integration**:
- **Canvas API**: `canvasapi` Python library
- **Moodle API**: `requests` with Moodle web services
- **Blackboard API**: Blackboard REST API

### QTI Template Engine

```python
from jinja2 import Environment, FileSystemLoader
from lxml import etree

env = Environment(loader=FileSystemLoader('qti-templates/'))

# Multiple choice template
template = env.get_template('multiple-choice-qti2.2.xml.j2')

item_data = {
    'identifier': 'item-001',
    'title': 'Capital of France',
    'question': 'What is the capital of France?',
    'choices': [
        {'id': 'A', 'text': 'Paris', 'correct': True},
        {'id': 'B', 'text': 'London', 'correct': False},
        {'id': 'C', 'text': 'Berlin', 'correct': False},
        {'id': 'D', 'text': 'Madrid', 'correct': False}
    ],
    'points': 1,
    'metadata': {
        'standard': 'CCSS.ELA.7.G.1',
        'difficulty': 'easy',
        'bloom': 'remember'
    }
}

xml_output = template.render(item_data)
```

### Validation Pipeline

```python
def validate_qti_package(zip_path, qti_version='2.2'):
    """Validate QTI package against schema and conventions"""

    # Extract package
    extract_dir = extract_zip(zip_path)

    # Check manifest
    manifest = parse_manifest(f"{extract_dir}/imsmanifest.xml")
    assert manifest is not None, "Missing imsmanifest.xml"

    # Validate each item against XSD
    schema = load_qti_schema(qti_version)
    items = manifest.get_items()

    for item in items:
        item_xml = etree.parse(f"{extract_dir}/{item.href}")
        schema.assertValid(item_xml)

    # Check media files
    media_files = manifest.get_media_files()
    for media in media_files:
        assert os.path.exists(f"{extract_dir}/{media}"), f"Missing {media}"

    return ValidationReport(passed=True, warnings=[], errors=[])
```

## Integration with Agents

- **Assessment Designer Agent**: Uses QTI export for item bank delivery
- **Quality Assurance Agent**: Validates QTI packages before client delivery
- **Content Developer Agent**: Exports formative assessments to LMS

## Performance Metrics

- **Export time**: <5 seconds per 100 items
- **Package size**: 30-50 KB per item (with images)
- **LMS compatibility**: 95%+ import success rate
- **Validation accuracy**: 99%+ detection of schema violations

## Success Criteria

- ✅ QTI 2.1 and 2.2 packages validate against IMS schemas
- ✅ 95%+ import success in Canvas, Moodle, Blackboard
- ✅ Metadata preservation (standards, difficulty, Bloom's)
- ✅ Complex item types render correctly (drag-drop, hotspot)
- ✅ Assessment companies eliminate manual QTI conversion

---

**Status**: Ready for implementation
**Dependencies**: QTI XSD schemas (IMS Global), LMS APIs for testing
**Testing**: Requires test imports to Canvas, Moodle, Blackboard instances
**Standards**: IMS QTI 2.1/2.2 specifications (www.imsglobal.org)
