# Common Cartridge Templates

IMS Common Cartridge 1.3 templates for creating interoperable LMS packages.

## Templates Available

### Core Templates

1. **imsmanifest.xml** - Main manifest file (required)
   - Defines course structure (organizations)
   - Lists all resources
   - Contains metadata

2. **course-settings.xml** - Course configuration
   - Gradebook setup (assignment groups, weights)
   - Grading standards
   - Module prerequisites and completion requirements
   - Course settings

### Resource Templates

3. **lti-tool.xml** - LTI (Learning Tools Interoperability) tool links
   - Basic LTI 1.0/1.1 configuration
   - Platform-specific extensions (Canvas, Moodle)
   - Custom parameters
   - Privacy settings

4. **discussion-topic.xml** - Discussion forums
   - Forum configuration
   - Grading settings
   - Posting requirements

5. **web-link.xml** - External web links
   - Simple URL links
   - Link descriptions

6. **assessment-meta.xml** - QTI assessment metadata
   - Quiz settings
   - Timing and attempts
   - Security settings
   - Scoring policies

## Template Variable Syntax

All templates use `{{VARIABLE_NAME}}` syntax for placeholders.

**Example:**
```xml
<title>{{COURSE_TITLE}}</title>
```

Replace with actual values:
```xml
<title>Introduction to Biology</title>
```

## Common Variables

### Course-Level Variables

- `{{COURSE_ID}}` - Unique course identifier
- `{{COURSE_TITLE}}` - Course name
- `{{COURSE_CODE}}` - Course code (e.g., BIO-101)
- `{{COURSE_DESCRIPTION}}` - Course description
- `{{KEYWORDS}}` - Comma-separated keywords
- `{{CREATION_DATE}}` - ISO 8601 date (YYYY-MM-DDTHH:MM:SSZ)
- `{{COPYRIGHT_INFO}}` - Copyright notice
- `{{START_DATE}}` - Course start date
- `{{END_DATE}}` - Course end date

### Organization Variables

- `{{ORG_ID}}` - Organization identifier
- `{{ROOT_ITEM_ID}}` - Root item identifier
- `{{MODULE_X_ID}}` - Module identifier
- `{{MODULE_X_TITLE}}` - Module title
- `{{MODULE_X_RESOURCE_ID}}` - Module resource reference

### Resource Variables

- `{{LESSON_X_ID}}` - Lesson item identifier
- `{{LESSON_X_RESOURCE_ID}}` - Lesson resource identifier
- `{{LESSON_X_FILE}}` - Lesson file path
- `{{LESSON_X_TITLE}}` - Lesson title
- `{{LESSON_X_DEPENDENCIES}}` - Additional files (images, CSS, etc.)

### Assessment Variables

- `{{ASSESSMENT_X_ID}}` - Assessment item identifier
- `{{ASSESSMENT_X_RESOURCE_ID}}` - Assessment resource identifier
- `{{ASSESSMENT_X_FILE}}` - Assessment metadata file
- `{{ASSESSMENT_X_TITLE}}` - Assessment title
- `{{QUIZ_X_ID}}` - Quiz identifier
- `{{QUIZ_X_POINTS}}` - Points possible
- `{{QUIZ_X_DUE_DATE}}` - Due date

### Gradebook Variables

- `{{ASSIGNMENTS_WEIGHT}}` - Assignments category weight (0-100)
- `{{QUIZZES_WEIGHT}}` - Quizzes category weight
- `{{DISCUSSIONS_WEIGHT}}` - Discussions category weight
- `{{EXAMS_WEIGHT}}` - Exams category weight
- `{{GRADING_STANDARD_ID}}` - Grading standard identifier

### LTI Tool Variables

- `{{LTI_TOOL_TITLE}}` - Tool name
- `{{LTI_LAUNCH_URL}}` - Tool launch URL
- `{{LTI_SECURE_LAUNCH_URL}}` - HTTPS launch URL
- `{{VENDOR_NAME}}` - Tool vendor name
- `{{VENDOR_CODE}}` - Vendor identifier
- `{{PRIVACY_LEVEL}}` - Privacy level (anonymous, name_only, public)

### Discussion Variables

- `{{DISCUSSION_TITLE}}` - Discussion topic title
- `{{DISCUSSION_TEXT}}` - Discussion prompt (HTML)
- `{{DISCUSSION_TYPE}}` - threaded or side_comment
- `{{REQUIRE_INITIAL_POST}}` - true/false
- `{{POINTS_POSSIBLE}}` - Points for graded discussions

## Repeatable Sections

Some templates include repeatable sections marked with `{{ADDITIONAL_X}}`:

```xml
<!-- Module 1 -->
<item identifier="{{MODULE_1_ID}}">
  <title>{{MODULE_1_TITLE}}</title>
</item>

<!-- Additional modules -->
{{ADDITIONAL_MODULES}}
```

Replace `{{ADDITIONAL_MODULES}}` with additional `<item>` blocks for each module.

## Usage Example

### 1. Create Course Structure

```xml
<!-- imsmanifest.xml -->
<manifest identifier="bio-101-2025">
  <metadata>
    <lomimscc:title>
      <lomimscc:string>Introduction to Biology</lomimscc:string>
    </lomimscc:title>
  </metadata>
  <organizations>
    <organization identifier="org-bio-101">
      <item identifier="root">
        <title>Introduction to Biology</title>

        <!-- Module 1 -->
        <item identifier="mod-1" identifierref="res-mod-1">
          <title>Cell Structure</title>

          <!-- Lesson -->
          <item identifier="lesson-1" identifierref="res-lesson-1">
            <title>Cell Membranes</title>
          </item>

          <!-- Assessment -->
          <item identifier="quiz-1" identifierref="res-quiz-1">
            <title>Cell Structure Quiz</title>
          </item>
        </item>
      </item>
    </organization>
  </organizations>
  <resources>
    <!-- Define resources here -->
  </resources>
</manifest>
```

### 2. Add Gradebook Configuration

```xml
<!-- course-settings.xml -->
<course identifier="bio-101-2025">
  <title>Introduction to Biology</title>
  <assignment_groups>
    <assignment_group identifier="grp-quizzes">
      <title>Quizzes</title>
      <group_weight>30</group_weight>
    </assignment_group>
    <assignment_group identifier="grp-exams">
      <title>Exams</title>
      <group_weight>70</group_weight>
    </assignment_group>
  </assignment_groups>
</course>
```

### 3. Package as .imscc

1. Create directory structure:
   ```
   course_package/
   ├── imsmanifest.xml
   ├── course-settings.xml
   ├── lessons/
   │   └── lesson-1.html
   ├── assessments/
   │   └── quiz-1/
   │       ├── assessment_meta.xml
   │       └── quiz-1.xml (QTI)
   └── resources/
       └── images/
   ```

2. ZIP the entire directory

3. Rename .zip to .imscc

4. Import into Canvas, Moodle, Blackboard, etc.

## Validation

Use the `curriculum.validate-cc` skill to validate packages:

```bash
/curriculum.validate-cc --package course.imscc
```

## References

- [IMS Common Cartridge 1.3 Specification](https://www.imsglobal.org/cc/ccv1p3/imscc_profilev1p3-html/)
- [IMS QTI 2.1 Specification](https://www.imsglobal.org/question/qtiv2p1/imsqti_infov2p1.html)
- [IMS Basic LTI 1.0](https://www.imsglobal.org/specs/ltiv1p0)
- [Canvas Common Cartridge Extensions](https://canvas.instructure.com/doc/api/file.common_cartridge.html)

## See Also

- [PRODUCTION_GUIDE.md](../../PRODUCTION_GUIDE.md) - Section on Common Cartridge packaging
- [AUTHOR_GUIDE.md](../../AUTHOR_GUIDE.md) - Authoring CC-compatible content
- curriculum.package-common-cartridge skill
- curriculum.validate-cc skill
- cc-validator agent
