# Common Cartridge and QTI Version Support

This system supports multiple versions of IMS Common Cartridge and IMS QTI specifications for maximum interoperability across LMS platforms.

## Supported Versions

### Common Cartridge Versions

| Version | Year | Status | Support Level | LMS Compatibility |
|---------|------|--------|---------------|-------------------|
| **CC 1.0** | 2008 | Legacy | Full | Older LMS systems |
| **CC 1.1** | 2011 | Legacy | Full | Most LMS systems |
| **CC 1.2** | 2013 | Active | Full | All modern LMS |
| **CC 1.3** | 2016 | **Recommended** | **Full** | All modern LMS, preferred format |

### QTI (Question & Test Interoperability) Versions

| Version | Year | Status | Support Level | Use Case |
|---------|------|--------|---------------|----------|
| **QTI 2.0** | 2005 | Legacy | Full | Basic assessments, older systems |
| **QTI 2.1** | 2012 | Active | **Full** | **Recommended for CC 1.1-1.3** |
| **QTI 2.2** | 2015 | Active | Full | Advanced item types, modern LMS |
| **QTI 3.0** | 2019 | Current | Full | Latest features, Canvas/Moodle 4.x |

---

## Version Selection Guide

### When to Use Each Common Cartridge Version

#### CC 1.3 (Recommended)

**Use for:**
- New course development (2016+)
- Canvas, Moodle 3.x+, Blackboard Ultra
- Full LTI 1.3 support needed
- Modern gradebook features
- Best interoperability

**Features:**
- LTI 1.1/1.3 tool integration
- QTI 2.1/2.2 assessments
- Rich metadata (Dublin Core + LOM)
- Module prerequisites
- Gradebook categories and weights
- Discussion forums
- Web links

**Schema Namespace:**
```xml
xmlns="http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1"
<schemaversion>1.3.0</schemaversion>
```

#### CC 1.2

**Use for:**
- LMS systems from 2013-2016
- When CC 1.3 import fails
- Moodle 2.x, Blackboard 9.x

**Features:**
- Similar to CC 1.3 but fewer LTI options
- QTI 2.1 assessments
- Basic gradebook integration

**Schema Namespace:**
```xml
xmlns="http://www.imsglobal.org/xsd/imsccv1p2/imscp_v1p1"
<schemaversion>1.2.0</schemaversion>
```

#### CC 1.1

**Use for:**
- Legacy LMS systems (2011-2013)
- Compatibility with older Canvas, Moodle 1.x
- When newer versions unsupported

**Features:**
- Basic LTI 1.0 support
- QTI 2.0/2.1 assessments
- Simple gradebook

**Schema Namespace:**
```xml
xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1"
<schemaversion>1.1.0</schemaversion>
```

#### CC 1.0

**Use for:**
- Very old LMS systems (2008-2011)
- Last resort for compatibility
- Rarely used today

**Features:**
- Minimal LTI support
- QTI 2.0 assessments only
- Basic content packaging

**Schema Namespace:**
```xml
xmlns="http://www.imsglobal.org/xsd/imsccv1p0/imscp_v1p1"
<schemaversion>1.0.0</schemaversion>
```

---

### When to Use Each QTI Version

#### QTI 3.0 (Latest)

**Use for:**
- Canvas (2020+)
- Moodle 4.x
- Latest assessment features
- Accessible assessments (WCAG 2.1)
- Adaptive testing

**Features:**
- Improved accessibility
- New item types (composite, audio/video response)
- Better mobile support
- Enhanced feedback mechanisms
- Portable Custom Interactions (PCI)

**Item Types:**
- Choice (MC, TF, multiple response)
- Text entry (fill-in-blank, essay)
- Inline choice (dropdown)
- Match (matching, ordering)
- Hotspot (image-based)
- Media interaction (audio/video)
- Composite items (multi-part)

**Schema:**
```xml
xmlns="http://www.imsglobal.org/xsd/qti/qtiv3p0/imsqtiasi_v3p0"
```

#### QTI 2.2 (Modern)

**Use for:**
- Modern LMS (2015+)
- Advanced assessment features
- When QTI 3.0 unsupported

**Features:**
- Rich media support
- Custom interactions
- Advanced scoring
- Accessibility improvements
- Better feedback

**Item Types:**
- All QTI 2.1 types
- Custom interactions
- Enhanced hotspot
- Drawing response

**Schema:**
```xml
xmlns="http://www.imsglobal.org/xsd/qti/qtiv2p2/imsqti_v2p2"
```

#### QTI 2.1 (Recommended for CC 1.1-1.3)

**Use for:**
- Maximum compatibility (2012+)
- **Recommended for Common Cartridge packages**
- Works with all modern LMS
- Best balance of features and compatibility

**Features:**
- Comprehensive item types
- Response processing
- Feedback mechanisms
- Scoring
- Outcomes

**Item Types:**
- Choice Interaction (Multiple Choice, True/False)
- Text Entry (Fill-in-the-Blank, Essay)
- Match Interaction (Matching, Ordering)
- Associate Interaction (Grouping)
- Inline Choice (Dropdown)
- Hotspot Interaction (Image maps)
- Slider Interaction (Numeric)

**Schema:**
```xml
xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
```

#### QTI 2.0 (Legacy)

**Use for:**
- Legacy systems only (2005-2012)
- CC 1.0/1.1 packages
- When QTI 2.1+ unsupported

**Features:**
- Basic item types
- Simple scoring
- Limited feedback

**Item Types:**
- Choice (MC, TF)
- Text entry (basic)
- Match (simple)

**Schema:**
```xml
xmlns="http://www.imsglobal.org/xsd/imsqti_v2p0"
```

---

## Version Compatibility Matrix

### Common Cartridge + QTI Compatibility

| CC Version | Recommended QTI | Supported QTI | Min QTI | Max QTI |
|------------|-----------------|---------------|---------|---------|
| **CC 1.3** | **QTI 2.1** | 2.0, 2.1, 2.2, 3.0 | 2.0 | 3.0 |
| **CC 1.2** | **QTI 2.1** | 2.0, 2.1, 2.2 | 2.0 | 2.2 |
| **CC 1.1** | **QTI 2.1** | 2.0, 2.1 | 2.0 | 2.1 |
| **CC 1.0** | **QTI 2.0** | 2.0 | 2.0 | 2.0 |

### LMS Platform Support

| Platform | CC Versions | QTI Versions | Recommended Combo |
|----------|-------------|--------------|-------------------|
| **Canvas (2020+)** | 1.1, 1.2, 1.3 | 2.1, 2.2, 3.0 | **CC 1.3 + QTI 2.1** |
| **Moodle 4.x** | 1.1, 1.2, 1.3 | 2.0, 2.1, 2.2, 3.0 | **CC 1.3 + QTI 2.1** |
| **Moodle 3.x** | 1.1, 1.2, 1.3 | 2.0, 2.1, 2.2 | **CC 1.2 + QTI 2.1** |
| **Moodle 2.x** | 1.1, 1.2 | 2.0, 2.1 | **CC 1.2 + QTI 2.1** |
| **Blackboard Ultra** | 1.1, 1.2, 1.3 | 2.1, 2.2 | **CC 1.3 + QTI 2.1** |
| **Blackboard 9.x** | 1.1, 1.2 | 2.0, 2.1 | **CC 1.2 + QTI 2.1** |
| **D2L Brightspace** | 1.1, 1.2, 1.3 | 2.1, 2.2 | **CC 1.3 + QTI 2.1** |
| **Schoology** | 1.1, 1.2, 1.3 | 2.1 | **CC 1.3 + QTI 2.1** |

---

## Template Organization

Templates are organized by version:

```
templates/common-cartridge/
├── README.md                    # Usage instructions
├── VERSION_SUPPORT.md           # This file
├── v1.0/                        # CC 1.0 templates
│   ├── imsmanifest-cc1.0.xml
│   └── qti2.0/                  # QTI 2.0 for CC 1.0
├── v1.1/                        # CC 1.1 templates
│   ├── imsmanifest-cc1.1.xml
│   ├── qti2.0/
│   └── qti2.1/
├── v1.2/                        # CC 1.2 templates
│   ├── imsmanifest-cc1.2.xml
│   ├── course-settings-cc1.2.xml
│   ├── qti2.0/
│   ├── qti2.1/
│   └── qti2.2/
└── v1.3/                        # CC 1.3 templates (current)
    ├── imsmanifest.xml
    ├── course-settings.xml
    ├── lti-tool.xml
    ├── discussion-topic.xml
    ├── web-link.xml
    ├── assessment-meta.xml
    ├── qti2.0/
    ├── qti2.1/                  # Recommended
    ├── qti2.2/
    └── qti3.0/
```

---

## CLI Version Selection

### Specify CC Version

```bash
# Default: CC 1.3
/curriculum.package-common-cartridge --materials "course/" --output "course.imscc"

# Specify CC 1.2 for compatibility
/curriculum.package-common-cartridge --materials "course/" --output "course.imscc" --cc-version "1.2"

# Specify CC 1.1 for legacy LMS
/curriculum.package-common-cartridge --materials "course/" --output "course.imscc" --cc-version "1.1"

# Specify CC 1.0 (rarely needed)
/curriculum.package-common-cartridge --materials "course/" --output "course.imscc" --cc-version "1.0"
```

### Specify QTI Version

```bash
# Default: QTI 2.1 (recommended)
/curriculum.export-qti --assessment "quiz.json" --output "quiz/" --version "2.1"

# QTI 3.0 for latest features
/curriculum.export-qti --assessment "quiz.json" --output "quiz/" --version "3.0"

# QTI 2.2 for advanced features
/curriculum.export-qti --assessment "quiz.json" --output "quiz/" --version "2.2"

# QTI 2.0 for legacy compatibility
/curriculum.export-qti --assessment "quiz.json" --output "quiz/" --version "2.0"
```

### Combined Version Selection

```bash
# CC 1.3 + QTI 2.1 (recommended)
/curriculum.package-common-cartridge \
  --materials "course/" \
  --output "course.imscc" \
  --cc-version "1.3" \
  --qti-version "2.1"

# CC 1.2 + QTI 2.1 (compatible)
/curriculum.package-common-cartridge \
  --materials "course/" \
  --output "course.imscc" \
  --cc-version "1.2" \
  --qti-version "2.1"

# CC 1.1 + QTI 2.0 (maximum legacy support)
/curriculum.package-common-cartridge \
  --materials "course/" \
  --output "course.imscc" \
  --cc-version "1.1" \
  --qti-version "2.0"
```

### Auto-Detection

```bash
# Detect versions from target LMS
/curriculum.package-common-cartridge \
  --materials "course/" \
  --output "course.imscc" \
  --target-lms "canvas-2020"
  # Auto-selects: CC 1.3 + QTI 2.1

/curriculum.package-common-cartridge \
  --materials "course/" \
  --output "course.imscc" \
  --target-lms "moodle-2.9"
  # Auto-selects: CC 1.2 + QTI 2.1

/curriculum.package-common-cartridge \
  --materials "course/" \
  --output "course.imscc" \
  --target-lms "blackboard-9.1"
  # Auto-selects: CC 1.1 + QTI 2.0
```

---

## Version Migration

### Upgrading Packages

```bash
# Upgrade CC 1.2 package to CC 1.3
/curriculum.migrate-cc --input "course-cc1.2.imscc" --output "course-cc1.3.imscc" --to-version "1.3"

# Upgrade QTI 2.0 to QTI 2.1
/curriculum.migrate-qti --input "assessment-qti2.0/" --output "assessment-qti2.1/" --to-version "2.1"

# Upgrade both CC and QTI
/curriculum.migrate-cc --input "course-old.imscc" --output "course-new.imscc" --cc-version "1.3" --qti-version "2.1"
```

### Downgrading for Compatibility

```bash
# Downgrade CC 1.3 to CC 1.2 for legacy LMS
/curriculum.migrate-cc --input "course-cc1.3.imscc" --output "course-cc1.2.imscc" --to-version "1.2"

# Note: Some features may be lost during downgrade
# - LTI 1.3 → LTI 1.1
# - Advanced gradebook → Basic gradebook
# - QTI 3.0 → QTI 2.1 (item types may be simplified)
```

---

## Best Practices

### Version Selection Recommendations

1. **Default Choice: CC 1.3 + QTI 2.1**
   - Works with all modern LMS platforms
   - Best balance of features and compatibility
   - Recommended for 95% of use cases

2. **Legacy Compatibility: CC 1.2 + QTI 2.1**
   - Use when CC 1.3 import fails
   - Works with older LMS versions
   - Minimal feature loss

3. **Maximum Compatibility: CC 1.1 + QTI 2.0**
   - Use only for very old systems
   - Significant feature limitations

4. **Latest Features: CC 1.3 + QTI 3.0**
   - Use only if target LMS supports QTI 3.0
   - Test thoroughly before delivery
   - Fallback to QTI 2.1 if issues

### Testing Strategy

**Test in this order:**
1. Create with **CC 1.3 + QTI 2.1** (recommended)
2. Test import in target LMS
3. If import fails, try **CC 1.2 + QTI 2.1**
4. If still fails, try **CC 1.1 + QTI 2.0**

### Validation

```bash
# Validate any version
/curriculum.validate-cc --package course.imscc --detect-version

# Specify expected version
/curriculum.validate-cc --package course.imscc --cc-version "1.3" --qti-version "2.1"

# Validate for specific LMS
/curriculum.validate-cc --package course.imscc --target-lms "canvas-2022"
```

---

## References

### IMS Global Specifications

**Common Cartridge:**
- [CC 1.3 (2016)](https://www.imsglobal.org/cc/ccv1p3/imscc_profilev1p3-html/)
- [CC 1.2 (2013)](https://www.imsglobal.org/cc/ccv1p2/imscc_profilev1p2-html/)
- [CC 1.1 (2011)](https://www.imsglobal.org/cc/ccv1p1/imscc_profilev1p1-html/)
- [CC 1.0 (2008)](https://www.imsglobal.org/cc/ccv1p0/imscc_profilev1p0-html/)

**QTI:**
- [QTI 3.0 (2019)](https://www.imsglobal.org/spec/qti/v3p0/impl)
- [QTI 2.2 (2015)](https://www.imsglobal.org/question/qtiv2p2/imsqti_infov2p2.html)
- [QTI 2.1 (2012)](https://www.imsglobal.org/question/qtiv2p1/imsqti_infov2p1.html)
- [QTI 2.0 (2005)](https://www.imsglobal.org/question/qtiv2p0/imsqti_infov2p0.html)

---

## See Also

- [README.md](README.md) - Template usage instructions
- [PRODUCTION_GUIDE.md](../../PRODUCTION_GUIDE.md) - Complete CC workflows
- curriculum.package-common-cartridge skill
- curriculum.export-qti skill
- curriculum.validate-cc skill
- curriculum.migrate-cc skill (version migration)
