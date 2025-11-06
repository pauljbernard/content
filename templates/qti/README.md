# QTI (Question & Test Interoperability) Templates

IMS QTI templates for creating portable, interoperable assessments across multiple versions (2.0, 2.1, 2.2, 3.0).

## Supported Versions

| Version | Year | Status | Support Level | Recommended For |
|---------|------|--------|---------------|-----------------|
| QTI 2.0 | 2005 | Legacy | Full | CC 1.0/1.1, legacy systems |
| QTI 2.1 | 2012 | Active | **Full** | **CC 1.1-1.3, maximum compatibility** |
| QTI 2.2 | 2015 | Active | Full | CC 1.2/1.3, advanced features |
| QTI 3.0 | 2019 | Current | Full | CC 1.3, latest features, Canvas/Moodle 4.x |

**Default:** QTI 2.1 (best balance of features and compatibility)

## Template Organization

```
templates/qti/
├── README.md              # This file
├── v2.0/                  # QTI 2.0 templates (legacy)
│   ├── choice-item.xml
│   ├── text-entry-item.xml
│   └── match-item.xml
├── v2.1/                  # QTI 2.1 templates (recommended)
│   ├── choice-item.xml
│   ├── text-entry-item.xml
│   ├── match-item.xml
│   ├── hotspot-item.xml
│   ├── inline-choice-item.xml
│   └── assessment.xml
├── v2.2/                  # QTI 2.2 templates
│   ├── choice-item.xml
│   ├── custom-interaction-item.xml
│   ├── enhanced-hotspot-item.xml
│   └── assessment.xml
└── v3.0/                  # QTI 3.0 templates (latest)
    ├── choice-item.xml
    ├── composite-item.xml
    ├── media-interaction-item.xml
    └── assessment.xml
```

## Item Types by Version

### QTI 2.0 (Basic Item Types)

- **choiceInteraction** - Multiple choice, true/false
- **textEntryInteraction** - Fill-in-the-blank, short answer
- **matchInteraction** - Simple matching, ordering

**Limitations:**
- Basic response processing
- Limited feedback options
- No custom interactions

### QTI 2.1 (Standard Item Types - Recommended)

- **choiceInteraction** - Multiple choice, true/false, multiple response
- **textEntryInteraction** - Fill-in-the-blank, short answer, essay
- **matchInteraction** - Matching, ordering, grouping
- **associateInteraction** - Drag-and-drop grouping
- **inlineChoiceInteraction** - Dropdown selections
- **hotspotInteraction** - Image-based responses (click on image)
- **sliderInteraction** - Numeric slider
- **extendedTextInteraction** - Long-form essay responses

**Features:**
- Comprehensive response processing
- Rich feedback (correct/incorrect, per-choice)
- Scoring with partial credit
- Adaptive items (conditional logic)

### QTI 2.2 (Advanced Item Types)

All QTI 2.1 types plus:
- **customInteraction** - Custom JavaScript interactions
- **Enhanced hotspot** - Multiple hotspot areas, complex shapes
- **drawingInteraction** - Student drawing responses
- **uploadInteraction** - File upload responses

**Features:**
- Custom interactions via JavaScript
- Enhanced multimedia support
- Better accessibility features

### QTI 3.0 (Latest Item Types)

All QTI 2.2 types plus:
- **compositeItem** - Multi-part items (passage + multiple questions)
- **mediaInteraction** - Audio/video recording responses
- **Portable Custom Interactions (PCI)** - Standardized custom types
- **Enhanced accessibility** - WCAG 2.1 AA compliance built-in

**Features:**
- Improved mobile support
- Better accessibility
- Richer media types
- Standardized custom interactions

## Common Item Type Examples

### Multiple Choice (All Versions Compatible)

**QTI 2.1 Example:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
                identifier="mc-001"
                title="Cell Structure Question"
                adaptive="false"
                timeDependent="false">

  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
    <correctResponse>
      <value>choice-c</value>
    </correctResponse>
  </responseDeclaration>

  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
    <defaultValue>
      <value>0</value>
    </defaultValue>
  </outcomeDeclaration>

  <itemBody>
    <p>Which organelle is responsible for cellular respiration?</p>
    <choiceInteraction responseIdentifier="RESPONSE" shuffle="true" maxChoices="1">
      <prompt>Select the correct answer:</prompt>
      <simpleChoice identifier="choice-a">Nucleus</simpleChoice>
      <simpleChoice identifier="choice-b">Ribosome</simpleChoice>
      <simpleChoice identifier="choice-c">Mitochondrion</simpleChoice>
      <simpleChoice identifier="choice-d">Chloroplast</simpleChoice>
    </choiceInteraction>
  </itemBody>

  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"/>

</assessmentItem>
```

### Fill-in-the-Blank (Text Entry)

**QTI 2.1 Example:**
```xml
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
                identifier="fib-001"
                title="Cell Membrane Fill-in">

  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="string">
    <correctResponse>
      <value>phospholipid bilayer</value>
    </correctResponse>
  </responseDeclaration>

  <itemBody>
    <p>The cell membrane is composed of a <textEntryInteraction responseIdentifier="RESPONSE" expectedLength="20"/> structure.</p>
  </itemBody>

  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"/>

</assessmentItem>
```

### Essay Question

**QTI 2.1 Example:**
```xml
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
                identifier="essay-001"
                title="Evolution Essay">

  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="string"/>

  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
    <defaultValue>
      <value>0</value>
    </defaultValue>
  </outcomeDeclaration>

  <itemBody>
    <p>Explain the process of natural selection and provide two examples of how it has shaped modern species. Your response should be 250-500 words.</p>
    <extendedTextInteraction responseIdentifier="RESPONSE" expectedLines="10" expectedLength="500">
      <prompt>Enter your essay here:</prompt>
    </extendedTextInteraction>
  </itemBody>

  <!-- Manual grading required - no response processing -->

</assessmentItem>
```

## Assessment Packaging

### QTI 2.1 Assessment Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<assessmentTest xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
                identifier="assessment-001"
                title="Module 1 Quiz: Cell Biology">

  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float"/>

  <testPart identifier="part-1" navigationMode="linear" submissionMode="individual">
    <assessmentSection identifier="section-1" title="Multiple Choice" visible="true">
      <assessmentItemRef identifier="mc-001" href="items/mc-001.xml"/>
      <assessmentItemRef identifier="mc-002" href="items/mc-002.xml"/>
      <assessmentItemRef identifier="mc-003" href="items/mc-003.xml"/>
    </assessmentSection>

    <assessmentSection identifier="section-2" title="Fill-in-the-Blank" visible="true">
      <assessmentItemRef identifier="fib-001" href="items/fib-001.xml"/>
      <assessmentItemRef identifier="fib-002" href="items/fib-002.xml"/>
    </assessmentSection>

    <assessmentSection identifier="section-3" title="Essay" visible="true">
      <assessmentItemRef identifier="essay-001" href="items/essay-001.xml"/>
    </assessmentSection>
  </testPart>

</assessmentTest>
```

## Version Selection Guide

### Choose QTI 2.1 (Recommended)

**When:**
- Creating new assessments for Common Cartridge packages
- Need maximum LMS compatibility
- Standard item types sufficient

**Works with:**
- Canvas, Moodle 3.x+, Blackboard, D2L, Schoology
- CC 1.1, 1.2, 1.3

### Choose QTI 3.0

**When:**
- Target LMS supports QTI 3.0 (Canvas 2020+, Moodle 4.x)
- Need latest accessibility features
- Composite items or media interactions required

**Works with:**
- Modern Canvas, Moodle 4.x
- CC 1.3 only

### Choose QTI 2.2

**When:**
- Need custom interactions
- QTI 3.0 not yet supported
- Advanced item types required

**Works with:**
- Canvas, Moodle 3.x, Blackboard
- CC 1.2, 1.3

### Choose QTI 2.0

**When:**
- Legacy LMS only (pre-2012)
- CC 1.0/1.1 packages
- Last resort for compatibility

**Works with:**
- Very old LMS systems
- CC 1.0, 1.1

## CLI Usage

```bash
# Default: QTI 2.1
/curriculum.export-qti --assessment "quiz.json" --output "quiz/"

# Specify QTI version
/curriculum.export-qti --assessment "quiz.json" --output "quiz/" --version "2.1"
/curriculum.export-qti --assessment "quiz.json" --output "quiz/" --version "3.0"

# Validate QTI
/curriculum.validate-qti --assessment "quiz/assessment.xml" --version "2.1"

# Convert between versions
/curriculum.migrate-qti --input "quiz-qti2.0/" --output "quiz-qti2.1/" --to-version "2.1"
```

## Integration with Common Cartridge

QTI assessments are embedded in CC packages:

```xml
<!-- In imsmanifest.xml -->
<resource identifier="res-quiz-1" type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment">
  <file href="assessments/quiz-1/assessment_meta.xml"/>
  <dependency identifierref="res-quiz-1-qti"/>
</resource>

<resource identifier="res-quiz-1-qti" type="associatedcontent/imscc_xmlv1p3/learning-application-resource">
  <file href="assessments/quiz-1/assessment.xml"/>
  <file href="assessments/quiz-1/items/item-1.xml"/>
  <file href="assessments/quiz-1/items/item-2.xml"/>
</resource>
```

## Best Practices

### Item Authoring

✅ **Do:**
- Use QTI 2.1 for maximum compatibility
- Provide feedback for all items
- Use partial credit where appropriate
- Randomize choice order (shuffle="true")
- Include clear prompts and instructions

❌ **Don't:**
- Mix QTI versions in one assessment
- Use overly complex custom interactions
- Forget to test in target LMS
- Use non-standard response processing

### Accessibility

✅ **Include:**
- Alt text for all images
- Text alternatives for audio/video
- Keyboard navigation support
- Screen reader friendly markup
- Clear instructions

### Scoring

✅ **Configure:**
- Point values for each item
- Response processing templates
- Partial credit rules
- Feedback timing (immediate, after submission, never)

## References

- [QTI 3.0 Specification](https://www.imsglobal.org/spec/qti/v3p0/impl)
- [QTI 2.2 Specification](https://www.imsglobal.org/question/qtiv2p2/imsqti_infov2p2.html)
- [QTI 2.1 Specification](https://www.imsglobal.org/question/qtiv2p1/imsqti_infov2p1.html)
- [QTI 2.0 Specification](https://www.imsglobal.org/question/qtiv2p0/imsqti_infov2p0.html)

## See Also

- [Common Cartridge Templates](../common-cartridge/README.md)
- [VERSION_SUPPORT.md](../common-cartridge/VERSION_SUPPORT.md) - CC + QTI compatibility
- curriculum.export-qti skill
- curriculum.validate-qti skill
- [PRODUCTION_GUIDE.md](../../PRODUCTION_GUIDE.md) - Assessment workflows
