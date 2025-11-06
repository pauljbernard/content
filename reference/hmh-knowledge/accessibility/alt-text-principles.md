# Alt Text Principles for Mathematical Content
**Accessibility Standard for Images**
**Source:** WCAG 2.1 Level AA + Mathematical Accessibility Best Practices
**Audience:** Curriculum developers writing alt text for mathematical images

---

## Overview

**Alternative text (alt text) provides text descriptions of images for students using screen readers or when images fail to load.** In mathematical content, alt text must convey both the visual appearance and the mathematical meaning.

**Core Principle:** Alt text should provide equivalent access to the information an image conveys, enabling blind and low-vision students to understand the mathematics.

---

## Legal and Quality Requirements

### WCAG 2.1 Level AA (Federal Standard):
**Success Criterion 1.1.1 (Non-text Content):**
All non-text content must have a text alternative that serves the equivalent purpose.

### HMH Standard:
- All images must have descriptive alt text
- Alt text must convey mathematical meaning
- Complex images may require long descriptions
- Decorative images must be marked as such

### Texas Accessibility:
- Required for SBOE adoption
- Part of IPACC compliance
- Checked during vendor review

---

## Types of Mathematical Images

### Type 1: Diagrams and Models
**Examples:** Geometric figures, area models, tape diagrams, number lines, bar models

**Alt Text Goal:** Describe structure, labels, and mathematical relationships

---

### Type 2: Graphs and Charts
**Examples:** Bar graphs, line graphs, pie charts, coordinate planes, scatter plots

**Alt Text Goal:** Convey data, trends, axes, labels, and key points

---

### Type 3: Real-World Photos
**Examples:** Arrays of objects, measurement scenarios, photographs illustrating contexts

**Alt Text Goal:** Describe relevant mathematical features, not every visual detail

---

### Type 4: Symbolic/Notational Images
**Examples:** Fraction bars, equation models, mathematical notation rendered as images

**Alt Text Goal:** Translate visual notation into spoken/written equivalent

---

### Type 5: Decorative Images
**Examples:** Background patterns, borders, purely aesthetic elements

**Alt Text Goal:** Mark as decorative (alt="") so screen readers skip

---

## Core Alt Text Principles

### Principle 1: Be Concise Yet Complete

**Target:** 1-2 sentences (15-25 words) for simple images

**Why:** Screen reader users listen to alt text; long descriptions are fatiguing

**When to Exceed:** Complex diagrams may need longer descriptions or separate long description

**Example:**
- ❌ Too Long: "This is a rectangle. It has four sides. Two sides are long and two sides are short. The long sides are parallel to each other. The short sides are also parallel to each other..."
- ✅ Concise: "Rectangle with length 8 units and width 5 units."

---

### Principle 2: Describe Mathematical Meaning, Not Just Appearance

**Focus:** What does the image teach or illustrate mathematically?

**Avoid:** Purely visual descriptions without math context

**Example:**
- ❌ Appearance Only: "A blue rectangle divided by a line"
- ✅ Mathematical Meaning: "Rectangle partitioned into two equal parts, showing halves"

---

### Principle 3: Include Relevant Labels and Values

**Always Include:**
- Numerical values shown
- Labels on axes, parts, or objects
- Units of measurement
- Key mathematical vocabulary

**Example:**
- ❌ Missing Information: "A number line"
- ✅ Complete: "Number line from 0 to 10, with intervals of 1"

---

### Principle 4: Use Mathematical Vocabulary Appropriately

**Match Grade Level:** Use vocabulary students know or are learning

**Be Precise:** Use correct mathematical terms

**Example:**
- ❌ Informal: "Box with numbers inside"
- ✅ Mathematical: "Array with 3 rows and 4 columns"

---

### Principle 5: Describe Orientation and Position When Relevant

**Include When:**
- Position affects meaning (e.g., coordinate plane)
- Orientation matters (e.g., transformations)
- Relationships between elements are key

**Example:**
- "Point A located at (3, 5) in Quadrant I"
- "Triangle ABC with right angle at vertex B"

---

### Principle 6: Mark Decorative Images as Decorative

**Use alt=""** for purely decorative images

**Screen readers skip** images with empty alt text

**Example:**
- Decorative border: alt=""
- Background pattern: alt=""
- Purely aesthetic clipart: alt=""

**When in Doubt:** If image removal wouldn't change mathematical understanding, it's decorative.

---

## Alt Text Writing Process

### Step 1: Identify Image Purpose

Ask:
- Why is this image here?
- What mathematical concept does it illustrate?
- What information must a student gain from it?

---

### Step 2: Extract Key Information

Note:
- Numerical values
- Labels
- Relationships
- Structures
- Patterns

---

### Step 3: Write Draft Alt Text

Start with:
- Image type (e.g., "Bar graph showing...")
- Key mathematical information
- Labels and values

---

### Step 4: Review for Completeness

Check:
- [ ] Can someone "see" the math without the image?
- [ ] Are all critical labels included?
- [ ] Is mathematical meaning clear?
- [ ] Is it concise?

---

### Step 5: Test with Screen Reader (if possible)

Listen to alt text read aloud:
- Does it make sense when spoken?
- Is pronunciation correct?
- Is length appropriate?

---

## Alt Text by Image Type: Detailed Guidance

### Type 1: Geometric Diagrams

**What to Include:**
- Shape name
- Dimensions or measurements
- Labels on vertices, sides, or angles
- Special properties (right angle, parallel sides, etc.)

**Example 1 - Simple:**
**Image:** Rectangle
**Alt Text:** "Rectangle with length 12 cm and width 7 cm."

**Example 2 - Labeled:**
**Image:** Triangle with vertices labeled A, B, C
**Alt Text:** "Triangle ABC with right angle at vertex B."

**Example 3 - Complex:**
**Image:** Composite figure (rectangle + triangle)
**Alt Text:** "Composite figure composed of a rectangle with dimensions 8 by 4 attached to a triangle with base 8 and height 3."

---

### Type 2: Number Lines

**What to Include:**
- Range (start and end values)
- Interval size
- Points or segments marked
- Labels

**Example 1 - Basic:**
**Image:** Number line 0 to 10
**Alt Text:** "Number line from 0 to 10 with intervals of 1."

**Example 2 - With Point:**
**Image:** Number line with point at 3.5
**Alt Text:** "Number line from 0 to 5 with a point marked at 3.5."

**Example 3 - Comparison:**
**Image:** Two number lines showing fractions
**Alt Text:** "Two number lines from 0 to 1. Top line shows 1/2 marked; bottom line shows 2/4 marked at the same position."

---

### Type 3: Area Models and Arrays

**What to Include:**
- Structure (rows and columns)
- Dimensions
- What's being represented (multiplication, area, fractions)
- Partitions or divisions

**Example 1 - Array:**
**Image:** Array of circles
**Alt Text:** "Array with 3 rows and 5 columns of circles, representing 3 times 5."

**Example 2 - Area Model:**
**Image:** Rectangle divided into sections for multiplication
**Alt Text:** "Area model for 14 times 23, partitioned into four sections: 10 times 20, 10 times 3, 4 times 20, and 4 times 3."

**Example 3 - Fraction Model:**
**Image:** Rectangle divided into 8 parts, 3 shaded
**Alt Text:** "Rectangle partitioned into 8 equal parts with 3 parts shaded, representing 3/8."

---

### Type 4: Bar Models and Tape Diagrams

**What to Include:**
- Number of bars/sections
- Labels for each section
- Total or comparison being shown
- Values if present

**Example 1 - Comparison:**
**Image:** Two bars showing quantities
**Alt Text:** "Bar model showing two bars. Top bar labeled 'Maria' is 12 units long. Bottom bar labeled 'James' is 8 units long."

**Example 2 - Part-Whole:**
**Image:** Tape diagram with sections
**Alt Text:** "Tape diagram with total of 36 divided into 3 equal sections, each labeled with a question mark."

---

### Type 5: Coordinate Planes and Graphs

**What to Include:**
- Axes labels and scale
- Points plotted (with coordinates)
- Lines or curves (with key features)
- Quadrants (if relevant)

**Example 1 - Single Point:**
**Image:** Coordinate plane with one point
**Alt Text:** "Coordinate plane with x-axis and y-axis from -5 to 5. Point A is plotted at (3, 4)."

**Example 2 - Line:**
**Image:** Coordinate plane with line
**Alt Text:** "Coordinate plane showing a line passing through points (0, 2) and (3, 5)."

**Example 3 - Multiple Points:**
**Image:** Scatter plot
**Alt Text:** "Scatter plot with x-axis labeled 'Hours Studied' (0 to 10) and y-axis labeled 'Test Score' (0 to 100). Points show positive correlation, ranging from (1, 55) to (9, 95)."

---

### Type 6: Data Displays (Bar Graphs, Line Graphs, Pie Charts)

**What to Include:**
- Graph type
- Title (if present)
- Axes labels and scale
- Key data points or trends
- Legend (if present)

**Example 1 - Bar Graph:**
**Image:** Bar graph showing favorite fruits
**Alt Text:** "Bar graph titled 'Favorite Fruits.' X-axis shows Apple, Banana, Orange, Grape. Y-axis shows number of students from 0 to 20. Bars show: Apple 15, Banana 12, Orange 8, Grape 10."

**Example 2 - Line Graph:**
**Image:** Line graph showing temperature over time
**Alt Text:** "Line graph titled 'Temperature Throughout the Day.' X-axis shows time from 6 AM to 6 PM. Y-axis shows temperature from 50°F to 90°F. Line shows temperature rising from 60°F at 6 AM to peak of 85°F at 2 PM, then declining to 70°F at 6 PM."

**Example 3 - Pie Chart:**
**Image:** Pie chart showing survey results
**Alt Text:** "Pie chart showing survey results: 40% Yes (largest section), 35% No, 25% Maybe."

---

### Type 7: Real-World Photographs

**What to Include:**
- Relevant mathematical features only
- Quantities visible
- Arrangements or patterns
- Context for problem

**Example 1 - Counting:**
**Image:** Photo of apples in baskets
**Alt Text:** "Three baskets, each containing 5 apples."

**Example 2 - Measurement:**
**Image:** Ruler measuring object
**Alt Text:** "Ruler showing a pencil measuring 15 centimeters long."

**Example 3 - Context:**
**Image:** Parking lot with cars
**Alt Text:** "Parking lot with 4 rows of cars, 6 cars in each row."

**Avoid:** Describing irrelevant details (color of cars, background buildings, etc.)

---

### Type 8: Tables and Organized Data

**What to Include:**
- Table structure (rows and columns)
- Headers
- Key data points (for simple tables) or summary (for complex tables)

**Example 1 - Simple Table:**
**Image:** 2x3 table
**Alt Text:** "Table with 2 rows and 3 columns showing multiplication facts for 5: 5 times 1 equals 5, 5 times 2 equals 10, 5 times 3 equals 15."

**Example 2 - Complex Table:**
**Image:** Large data table
**Alt Text:** "Table showing monthly temperatures for the year. Columns: Month, High Temp, Low Temp. Data ranges from January (High 45°F, Low 30°F) to December (High 50°F, Low 35°F)."

**Note:** For very complex tables, provide long description separately.

---

## Special Cases and Challenges

### Challenge 1: Multi-Part Diagrams

**Problem:** Image contains multiple related elements

**Solution:** Describe each part in sequence, noting relationships

**Example:**
**Image:** Problem showing step-by-step solution with 3 diagrams
**Alt Text:** "Three-step solution. Step 1: Rectangle with dimensions 10 by 6. Step 2: Rectangle partitioned into 10 columns of width 1. Step 3: Six rows highlighted, showing 6 groups of 10."

---

### Challenge 2: Color-Coded Information

**Problem:** Information is conveyed by color alone

**Solution:** Describe the information, not just the color. Fix the image if possible (add patterns, labels).

**Example:**
- ❌ Color-Dependent: "Red section shows boys, blue section shows girls"
- ✅ Accessible: "Left section shows boys (15 students), right section shows girls (18 students)"

**Best Practice:** Use labels or patterns IN the image, not just color.

---

### Challenge 3: Complex Visual Relationships

**Problem:** Spatial relationships are critical but hard to describe concisely

**Solution:** Use directional language (above, below, left, right) or provide long description

**Example:**
**Image:** Venn diagram with overlapping circles
**Alt Text:** "Venn diagram with two overlapping circles. Left circle labeled 'Multiples of 2' contains 2, 4, 6, 8, 10. Right circle labeled 'Multiples of 3' contains 3, 6, 9, 12. Overlapping region contains 6."

**If More Complex:** "See long description below"

---

### Challenge 4: Graphs with Many Data Points

**Problem:** Too many points to describe individually

**Solution:** Describe trend and key points

**Example:**
**Image:** Line graph with 50 data points
**Alt Text:** "Line graph showing steady increase in population from 1970 to 2020. Population starts at 10,000 in 1970, reaches 25,000 by 1990, and ends at 50,000 in 2020."

---

### Challenge 5: Images of Text or Equations

**Problem:** Text or equations rendered as images

**Solution:** Provide text equivalent. Better: use actual text or MathML, not images.

**Example:**
**Image:** Equation "3x + 5 = 20" as image
**Alt Text:** "Equation: 3x + 5 = 20"

**Best Practice:** Don't use images for text or simple equations. Use actual text or MathML.

---

## Long Descriptions for Complex Images

### When to Use Long Descriptions:

- Image requires more than 3-4 sentences to describe
- Multiple elements with complex relationships
- Data tables with many values
- Step-by-step visual processes

### How to Provide Long Descriptions:

**Option 1: Visually-hidden text below image**
```html
<img src="complex-diagram.png" alt="Geometric proof (see long description below)">
<div class="sr-only">
  Long description: [Detailed description here...]
</div>
```

**Option 2: Link to separate description**
```html
<img src="complex-diagram.png" alt="Geometric proof">
<a href="#longdesc1">View detailed description</a>
```

**Option 3: Expandable description**
```html
<img src="complex-diagram.png" alt="Geometric proof">
<button>Show detailed description</button>
<div hidden>...</div>
```

---

### Long Description Example:

**Image:** Complex geometric proof with multiple steps

**Short Alt Text:** "Geometric proof that base angles of an isosceles triangle are congruent (see long description below)."

**Long Description:**
"Detailed description: Isosceles triangle ABC with AB = AC.
Step 1: Draw altitude from A to BC, intersecting BC at point D.
Step 2: Triangle ABD and triangle ACD are formed.
Step 3: In triangles ABD and ACD: AB = AC (given), AD = AD (common side), BD = DC (altitude bisects base).
Step 4: By SSS congruence, triangle ABD ≅ triangle ACD.
Step 5: Therefore, angle ABC = angle ACB (corresponding parts of congruent triangles)."

---

## Alt Text Validation Checklist

### Before Finalizing:

**Content:**
- [ ] Mathematical meaning conveyed
- [ ] All labels and values included
- [ ] Units specified if present
- [ ] Mathematical vocabulary used correctly

**Clarity:**
- [ ] Concise (1-3 sentences for simple images)
- [ ] Unambiguous
- [ ] Grade-appropriate language
- [ ] Correct pronunciation when read aloud

**Completeness:**
- [ ] Student could understand math without seeing image
- [ ] Key relationships described
- [ ] Orientation/position noted if relevant

**Accessibility:**
- [ ] Screen reader friendly
- [ ] No color-only information
- [ ] Decorative images marked (alt="")
- [ ] Complex images have long descriptions

**Technical:**
- [ ] Alt attribute present in HTML
- [ ] No punctuation issues (screen reader problems)
- [ ] Tested with screen reader if possible

---

## Common Alt Text Mistakes

### ❌ Mistake 1: Missing Alt Text
**Problem:** `<img src="diagram.png">` (no alt attribute)
**Impact:** Screen reader says "image" with no context
**Fix:** Always include alt attribute, even if alt=""

### ❌ Mistake 2: Meaningless Alt Text
**Problem:** alt="image" or alt="diagram"
**Impact:** No useful information conveyed
**Fix:** Describe the actual content

### ❌ Mistake 3: Too Verbose
**Problem:** alt="This diagram shows a beautiful rectangle with a length that measures exactly 12 centimeters and a width that is much shorter, measuring exactly 7 centimeters..."
**Impact:** Listener fatigue
**Fix:** "Rectangle with length 12 cm and width 7 cm."

### ❌ Mistake 4: Repeating Nearby Text
**Problem:** Image of rectangle next to text "Rectangle with dimensions 10 by 5", alt text repeats same
**Impact:** Redundancy
**Fix:** Use alt="" or alt="[Diagram]" if text already provides info

### ❌ Mistake 5: Saying "Image of" or "Picture of"
**Problem:** alt="Picture of a number line"
**Impact:** Redundant (screen reader already says "image")
**Fix:** alt="Number line from 0 to 10"

### ❌ Mistake 6: Describing Decorative Elements
**Problem:** Decorative border has alt="blue wavy border"
**Impact:** Distracts from content
**Fix:** alt="" (marks as decorative)

### ❌ Mistake 7: Color-Only Information
**Problem:** alt="Blue section is 30%, red section is 70%"
**Impact:** What do blue and red represent?
**Fix:** alt="Pie chart: Yes 30%, No 70%"

### ❌ Mistake 8: Missing Critical Values
**Problem:** alt="Bar graph showing favorite colors"
**Impact:** No data conveyed
**Fix:** alt="Bar graph: Red 12 students, Blue 15 students, Green 8 students"

---

## Alt Text Quality Rubric

### Excellent Alt Text:
- ✅ Conveys complete mathematical meaning
- ✅ Includes all labels and values
- ✅ Concise yet comprehensive
- ✅ Uses appropriate mathematical vocabulary
- ✅ Would allow student to understand without image

### Adequate Alt Text:
- ⚠️ Conveys most mathematical meaning
- ⚠️ Includes most labels and values
- ⚠️ Somewhat verbose or slightly unclear
- ⚠️ Student could probably understand without image

### Poor Alt Text:
- ❌ Vague or generic ("diagram", "image")
- ❌ Missing critical information
- ❌ Too long or too short
- ❌ Student could not understand without image

---

## Grade-Specific Considerations

### K-2 Alt Text:

**Characteristics:**
- Simple, concrete language
- Focus on countable objects
- Describe visual arrangements

**Example:**
- "Picture showing 5 apples in one group and 3 apples in another group."
- "Number line from 0 to 10 with the number 7 circled."

---

### 3-5 Alt Text:

**Characteristics:**
- Grade-level vocabulary (product, quotient, perimeter)
- Include measurements and units
- Describe models and representations

**Example:**
- "Area model for 14 times 23, showing partial products 200, 60, 40, and 12."
- "Bar graph showing monthly rainfall in centimeters for January through June."

---

### 6-8 Alt Text:

**Characteristics:**
- Advanced mathematical vocabulary
- Coordinate plane notation
- Variables and algebraic expressions
- Statistical representations

**Example:**
- "Coordinate plane showing linear function y = 2x + 3, passing through points (0, 3) and (1, 5)."
- "Scatter plot showing negative correlation between hours of TV watched and test scores."

---

## Tools and Testing

### Screen Readers for Testing:
- **NVDA** (Windows, free)
- **JAWS** (Windows, paid)
- **VoiceOver** (Mac/iOS, built-in)
- **TalkBack** (Android, built-in)

### Browser Extensions:
- **WAVE** (Web Accessibility Evaluation Tool)
- **aXe** (accessibility testing)
- **Screen Reader** Chrome extension

### Testing Process:
1. Turn on screen reader
2. Navigate to image
3. Listen to alt text
4. Ask: Does this convey the math?

---

## Quick Reference Card

### Alt Text Checklist (30-Second Check):

- [ ] **Present?** Alt attribute exists
- [ ] **Meaningful?** Describes math, not just "image"
- [ ] **Complete?** Labels and values included
- [ ] **Concise?** 1-3 sentences for simple images
- [ ] **Decorative?** Decorative images use alt=""

### Formula for Good Alt Text:

**[Image Type] + [Key Mathematical Information] + [Labels/Values]**

**Examples:**
- "Rectangle with length 12 cm and width 7 cm"
- "Bar graph showing test scores: Math 85, Science 90, English 88"
- "Number line from 0 to 20 with point at 15"

---

## Resources

**Related Guides:**
- UDL Principles: `/udl/udl-principles-guide.md`
- WCAG Compliance: (pending)
- Screen Reader Testing Guide: (pending)

**External Resources:**
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- WebAIM Alt Text Guide: https://webaim.org/techniques/alttext/
- Diagram Center Image Description Guidelines: http://diagramcenter.org/

**Tools:**
- WAVE: https://wave.webaim.org/
- aXe DevTools: https://www.deque.com/axe/

---

**Remember:** Alt text is not optional—it's a legal requirement and a matter of equity. Blind and low-vision students deserve equivalent access to mathematical content. Well-written alt text makes that possible.
