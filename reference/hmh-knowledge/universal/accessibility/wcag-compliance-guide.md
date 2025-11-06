# WCAG 2.1 AA Compliance Guide
**Web Content Accessibility Guidelines for Educational Materials**
**Scope:** Universal (all subjects and districts)
**Audience:** Curriculum developers creating accessible digital content

---

## Overview

**WCAG 2.1 Level AA** is the accessibility standard required for all HMH digital instructional materials. This ensures content is accessible to students with disabilities, including those using assistive technologies.

**Core Principle:** Accessible design benefits all learners, not just those with disabilities.

---

## WCAG Four Principles: POUR

### 1. Perceivable
Information and user interface components must be presentable to users in ways they can perceive.

### 2. Operable
User interface components and navigation must be operable.

### 3. Understandable
Information and the operation of user interface must be understandable.

### 4. Robust
Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

---

## Critical WCAG 2.1 AA Success Criteria

### Perceivable Requirements

#### 1.1.1 Non-Text Content (Level A)
**Requirement:** All non-text content has a text alternative.

**Application:**
- Images: Alt text describing content or function
- Math diagrams: Text description + MathML when possible
- Decorative images: Empty alt attribute (`alt=""`)
- Complex images: Long description via `aria-describedby`

**Examples:**
```html
<!-- Informative image -->
<img src="fraction-diagram.png" alt="Visual model showing 3/4 as three shaded parts out of four equal parts">

<!-- Decorative image -->
<img src="border-decoration.png" alt="">

<!-- Complex diagram -->
<img src="graph.png" alt="Bar graph showing student scores" aria-describedby="graph-desc">
<div id="graph-desc">
  Bar graph with 5 bars. Test 1: 75%, Test 2: 82%, Test 3: 88%,
  Test 4: 90%, Test 5: 95%. Shows increasing trend over time.
</div>
```

**See Also:** `/universal/assessment/alt-text-principles.md`

---

#### 1.3.1 Info and Relationships (Level A)
**Requirement:** Information, structure, and relationships can be programmatically determined.

**Application:**
- Use semantic HTML (headings, lists, tables)
- Proper heading hierarchy (H1 → H2 → H3, no skipping)
- Table headers marked with `<th>` and `scope` attributes
- Form labels associated with inputs

**Examples:**
```html
<!-- Proper heading hierarchy -->
<h1>Lesson 3: Fractions</h1>
<h2>Learning Objectives</h2>
<h3>Students will be able to:</h3>
<ul>
  <li>Identify equivalent fractions</li>
  <li>Compare fractions with unlike denominators</li>
</ul>

<!-- Data table with headers -->
<table>
  <thead>
    <tr>
      <th scope="col">Strategy</th>
      <th scope="col">Example</th>
      <th scope="col">When to Use</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Counting On</td>
      <td>7 + 3 = count "8, 9, 10"</td>
      <td>Adding small numbers</td>
    </tr>
  </tbody>
</table>

<!-- Form with labels -->
<label for="answer1">What is 12 × 5?</label>
<input type="text" id="answer1" name="answer1">
```

---

#### 1.3.2 Meaningful Sequence (Level A)
**Requirement:** Correct reading sequence can be programmatically determined.

**Application:**
- Content order in HTML matches visual order
- CSS doesn't create misleading visual order
- Reading order logical for screen readers

**Common Issue:**
Visual layout (CSS Grid/Flexbox) that changes order but HTML order is different.

**Fix:** Ensure HTML source order is logical, even if visually rearranged.

---

#### 1.4.1 Use of Color (Level A)
**Requirement:** Color is not the only visual means of conveying information.

**Application:**
- Don't use color alone to indicate correct/incorrect
- Add icons, labels, or patterns in addition to color
- Error messages include text, not just red color

**Examples:**
✅ **Good:** "✓ Correct" (green checkmark + word)
❌ **Bad:** Green background only

✅ **Good:** "✗ Incorrect: The area formula is length × width, not length + width"
❌ **Bad:** Red highlighting only

---

#### 1.4.3 Contrast (Minimum) (Level AA)
**Requirement:** Text has contrast ratio of at least 4.5:1 (3:1 for large text).

**Application:**
- Body text: 4.5:1 minimum
- Headings (18pt+ or 14pt+ bold): 3:1 minimum
- Check contrast with tools (WebAIM, browser dev tools)

**HMH Brand Colors with Compliant Combinations:**
- Navy text (#003057) on white background: 13.5:1 ✓
- Orange (#FF6F00) requires dark background or white text
- Gray text must be dark enough (#595959 minimum on white)

**Common Violations:**
❌ Light gray text on white (#CCCCCC on #FFFFFF = 1.6:1)
❌ Yellow text on white
❌ Pastel colors without sufficient contrast

**Fixing:**
- Darken text color
- Lighten background color
- Add background container with sufficient contrast

---

#### 1.4.4 Resize Text (Level AA)
**Requirement:** Text can be resized up to 200% without loss of content or functionality.

**Application:**
- Use relative units (rem, em, %) not fixed pixels
- Test zoom to 200% - content should reflow, not overflow
- No horizontal scrolling at 200% zoom

**Examples:**
```css
/* Good - relative units */
body { font-size: 1rem; }
h1 { font-size: 2.5rem; }
p { font-size: 1rem; line-height: 1.5; }

/* Bad - fixed pixels prevent scaling */
body { font-size: 16px; }
```

---

#### 1.4.10 Reflow (Level AA, WCAG 2.1)
**Requirement:** Content reflows at 320px width without horizontal scrolling (except tables, diagrams, equations).

**Application:**
- Responsive design required
- Test at 320px viewport (equivalent to 400% zoom)
- Mobile-first approach

**Exceptions:**
- Data tables (okay to scroll horizontally)
- Math equations (if complex)
- Diagrams and maps

---

#### 1.4.11 Non-Text Contrast (Level AA, WCAG 2.1)
**Requirement:** UI components and graphics have 3:1 contrast ratio.

**Application:**
- Buttons, form borders, focus indicators: 3:1 minimum
- Interactive elements distinguishable from background
- Icons and meaningful graphics have sufficient contrast

**Examples:**
✅ Button with dark border on light background
✅ Input field with visible border
❌ Very light gray button on white background

---

### Operable Requirements

#### 2.1.1 Keyboard (Level A)
**Requirement:** All functionality available via keyboard.

**Application:**
- No mouse-only interactions
- All interactive elements keyboard accessible
- Custom widgets need keyboard handlers
- Tab order logical

**Testing:** Navigate entire page using only Tab, Enter, Arrow keys, Escape

**Common Issues:**
❌ Drag-and-drop without keyboard alternative
❌ Custom dropdowns not keyboard accessible
❌ Click handlers on non-focusable elements

**Fixes:**
✅ Provide keyboard alternative to drag-and-drop
✅ Use semantic HTML (`<button>`, `<select>`) or add ARIA + keyboard handlers
✅ Ensure interactive elements are focusable (tabindex when needed)

---

#### 2.1.2 No Keyboard Trap (Level A)
**Requirement:** Keyboard focus can be moved away from any component.

**Application:**
- Users can Tab out of all interactive elements
- Modals/dialogs can be closed with Escape
- Focus doesn't get stuck

**Common Issue:** Modal dialogs that trap focus without Escape key handler.

**Fix:** Add Escape key listener, restore focus on close.

---

#### 2.4.1 Bypass Blocks (Level A)
**Requirement:** Skip navigation mechanism available.

**Application:**
- "Skip to main content" link at top of page
- Landmark regions (header, nav, main, footer)
- Heading structure enables navigation

**Example:**
```html
<a href="#main-content" class="skip-link">Skip to main content</a>

<header>
  <nav aria-label="Primary navigation">...</nav>
</header>

<main id="main-content">
  <!-- Lesson content -->
</main>
```

---

#### 2.4.2 Page Titled (Level A)
**Requirement:** Web pages have descriptive titles.

**Application:**
- Every page has unique, descriptive `<title>`
- Title describes topic or purpose
- Format: `{Specific} - {General}` (e.g., "Lesson 3: Fractions - Grade 5 Math")

**Examples:**
✅ `<title>Quiz: Multiplying Fractions - Grade 5 Unit 3</title>`
✅ `<title>MLR2: Collect and Display - Teacher Guide</title>`
❌ `<title>Page</title>`
❌ `<title>Untitled</title>`

---

#### 2.4.3 Focus Order (Level A)
**Requirement:** Focusable components receive focus in logical order.

**Application:**
- Tab order follows reading order
- Don't use positive tabindex values (they mess up order)
- Test by tabbing through page

**Common Issue:** CSS visual order differs from DOM order.

**Fix:** Reorder HTML to match visual flow, or use `tabindex="-1"` to remove from tab order (only when appropriate).

---

#### 2.4.4 Link Purpose (In Context) (Level A)
**Requirement:** Purpose of link can be determined from link text or context.

**Application:**
- Avoid "click here" or "read more" alone
- Link text describes destination
- If generic text needed, provide context

**Examples:**
✅ "Review the TEKS alignment guide"
✅ "Read more about UDL Principle 1: Multiple Means of Engagement"
❌ "Click here" (no context)
❌ "Read more" (which topic?)

**Fix for multiple "Read more" links:**
```html
<a href="udl-guide.html">
  Read more <span class="visually-hidden">about UDL Principles</span>
</a>
```

---

#### 2.4.6 Headings and Labels (Level AA)
**Requirement:** Headings and labels describe topic or purpose.

**Application:**
- Headings clearly describe section
- Form labels clearly describe input
- No ambiguous labels

**Examples:**
✅ `<h2>Multiple Means of Engagement</h2>`
✅ `<label for="q1">Question 1: What is 3/4 + 1/4?</label>`
❌ `<h2>Section 1</h2>` (not descriptive)
❌ `<label>Answer:</label>` (which question?)

---

#### 2.4.7 Focus Visible (Level AA)
**Requirement:** Keyboard focus indicator is visible.

**Application:**
- Don't remove focus outlines with CSS
- If customizing, ensure 3:1 contrast ratio
- Focus indicator must be clearly visible

**Common Violation:**
```css
/* DON'T DO THIS */
*:focus { outline: none; }
```

**Better Approach:**
```css
/* Custom focus with sufficient contrast */
:focus {
  outline: 2px solid #003057; /* HMH Navy */
  outline-offset: 2px;
}

/* Or use browser default (best) */
```

---

#### 2.5.3 Label in Name (Level A, WCAG 2.1)
**Requirement:** For UI components with labels, the accessible name contains the visible text label.

**Application:**
- Button visual text matches accessible name
- If icon + text, accessible name includes text

**Example:**
✅ Visual: "Submit Answer" → Accessible name: "Submit Answer"
❌ Visual: "Submit" → Accessible name: "Send response" (mismatch)

---

### Understandable Requirements

#### 3.1.1 Language of Page (Level A)
**Requirement:** Default human language of page can be programmatically determined.

**Application:**
- Set `lang` attribute on `<html>` element
- Specify language of content

**Example:**
```html
<html lang="en">
```

For Spanish content:
```html
<html lang="es">
```

---

#### 3.1.2 Language of Parts (Level AA)
**Requirement:** Language of passages can be programmatically determined.

**Application:**
- If content switches language, mark with `lang` attribute
- Common in bilingual materials

**Example:**
```html
<p>The Spanish word for "equivalent" is <span lang="es">equivalente</span>.</p>
```

---

#### 3.2.1 On Focus (Level A)
**Requirement:** When component receives focus, it doesn't initiate change of context.

**Application:**
- Focus alone doesn't submit forms
- Focus alone doesn't open new windows
- Focus alone doesn't change content

**Violation Example:**
❌ Dropdown that auto-submits when option receives focus (before Enter pressed)

**Fix:** Require explicit action (Enter key, button click) to submit.

---

#### 3.2.2 On Input (Level A)
**Requirement:** Changing setting of component doesn't automatically cause change of context.

**Application:**
- Typing in field doesn't auto-submit
- Selecting dropdown option doesn't auto-navigate (unless warned)
- Provide explicit submit button

**Acceptable with Warning:**
```html
<label for="unit-select">Jump to unit (will navigate immediately):</label>
<select id="unit-select" onchange="navigateToUnit()">
  <option>Unit 1</option>
  <option>Unit 2</option>
</select>
```

Better: Separate "Go" button.

---

#### 3.2.3 Consistent Navigation (Level AA)
**Requirement:** Navigation mechanisms repeated on multiple pages occur in consistent order.

**Application:**
- Navigation menu in same place on every page
- Same order of links
- Consistent UI patterns

---

#### 3.2.4 Consistent Identification (Level AA)
**Requirement:** Components with same functionality are identified consistently.

**Application:**
- Submit buttons always labeled "Submit" (not "Submit" on one page, "Send" on another)
- Icons mean the same thing across pages
- Consistent terminology

**Examples:**
✅ All "next lesson" buttons have same icon and text
❌ "Next" on page 1, "Continue" on page 2, "Proceed" on page 3 (for same action)

---

#### 3.3.1 Error Identification (Level A)
**Requirement:** If input error detected, error is described in text.

**Application:**
- Form validation errors clearly stated
- Identify which field has error
- Describe the error

**Example:**
✅ "Error: Answer must be a number. You entered 'abc'."
✅ "Required field: Please enter your response."
❌ Red highlighting only (violates color + text requirement)

---

#### 3.3.2 Labels or Instructions (Level A)
**Requirement:** Labels or instructions provided when content requires user input.

**Application:**
- All form fields have labels
- Instructions for complex inputs
- Format requirements stated

**Examples:**
✅ "Enter your answer as a fraction (e.g., 3/4)"
✅ "Round to the nearest tenth"
❌ Unlabeled text box

---

#### 3.3.3 Error Suggestion (Level AA)
**Requirement:** If input error detected and suggestions are known, suggestions provided.

**Application:**
- Offer correction when possible
- Explain how to fix error
- Examples of valid input

**Example:**
✅ "Error: Answer must be in decimal form. You entered '3/4'. Try '0.75' instead."
✅ "Invalid date format. Use MM/DD/YYYY (e.g., 03/15/2024)."

---

#### 3.3.4 Error Prevention (Legal, Financial, Data) (Level AA)
**Requirement:** For pages causing commitments, submissions are reversible, checked, or confirmed.

**Application:**
- High-stakes assessments: confirm before submit
- Allow review before final submission
- Provide "Are you sure?" confirmation

**Example:**
"You are about to submit your test. Once submitted, you cannot change your answers. Are you sure you want to submit?"
[Cancel] [Submit Test]

---

### Robust Requirements

#### 4.1.1 Parsing (Level A)
**Requirement:** Content can be parsed by assistive technologies (valid HTML).

**Application:**
- No duplicate IDs
- Properly nested elements
- Start and end tags correct
- Valid HTML attributes

**Validation:** Use W3C HTML Validator

**Common Issues:**
❌ `<div id="question1">...<div id="question1">...` (duplicate ID)
❌ `<p><div>...</div></p>` (invalid nesting)
❌ Unclosed tags

---

#### 4.1.2 Name, Role, Value (Level A)
**Requirement:** For all UI components, name and role can be programmatically determined.

**Application:**
- Use semantic HTML when possible (`<button>`, not `<div onclick>`)
- When custom widgets needed, use ARIA
- Interactive elements have accessible names

**Examples:**
```html
<!-- Good: semantic button -->
<button>Submit Answer</button>

<!-- Acceptable: div with ARIA (only if semantic HTML can't work) -->
<div role="button" tabindex="0" aria-label="Submit Answer">Submit</div>

<!-- Bad: div without ARIA -->
<div onclick="submit()">Submit</div>
```

---

#### 4.1.3 Status Messages (Level AA, WCAG 2.1)
**Requirement:** Status messages can be programmatically determined through role or properties.

**Application:**
- Screen readers announced status updates
- Use ARIA live regions for dynamic updates
- Success/error messages announced

**Examples:**
```html
<!-- Success message -->
<div role="status" aria-live="polite">
  Answer saved successfully.
</div>

<!-- Error alert -->
<div role="alert" aria-live="assertive">
  Error: Please answer all required questions.
</div>

<!-- Progress update -->
<div aria-live="polite" aria-atomic="true">
  Question 5 of 10 completed
</div>
```

**ARIA Live Region Types:**
- `aria-live="polite"` - Announces when user pauses (most status messages)
- `aria-live="assertive"` - Announces immediately (errors, urgent alerts)
- `role="status"` - Equivalent to `aria-live="polite"`
- `role="alert"` - Equivalent to `aria-live="assertive"`

---

## Educational-Specific Considerations

### Math Content Accessibility

**Challenge:** Mathematical notation is visual.

**Solutions:**
1. **MathML** for equations (when supported)
2. **Alt text** describing equation in words
3. **MathJax/KaTeX** with accessibility features enabled
4. **Text alternatives** for complex expressions

**Example:**
```html
<img src="equation.png" alt="x equals negative b plus or minus the square root of b squared minus 4ac, all divided by 2a">
```

Or with MathML:
```html
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mrow>
    <mi>x</mi>
    <mo>=</mo>
    <mfrac>
      <mrow>
        <mo>−</mo>
        <mi>b</mi>
        <mo>±</mo>
        <msqrt>
          <msup><mi>b</mi><mn>2</mn></msup>
          <mo>−</mo>
          <mn>4</mn><mi>a</mi><mi>c</mi>
        </msqrt>
      </mrow>
      <mrow><mn>2</mn><mi>a</mi></mrow>
    </mfrac>
  </mrow>
</math>
```

**See Also:** `/universal/assessment/alt-text-principles.md` (Math section)

---

### Video and Audio Accessibility

**Requirements:**

**Captions (Required for all video with audio):**
- Synchronized captions
- Include all spoken words
- Include relevant sound effects [applause], [music]
- Speaker identification when needed

**Transcripts (Required):**
- Full text transcript available
- Includes descriptions of visual content
- Downloadable or visible on page

**Audio Descriptions (When needed):**
- Describe important visual content not conveyed in audio
- Required when visual-only content is critical

**Example Caption Format:**
```
[Teacher]: Let's look at this fraction model.
[Points to diagram]
Notice that 3 out of 4 parts are shaded.
This represents three-fourths.
```

---

### Interactive Assessment Accessibility

**Learnosity-Specific:**
- Enable accessibility mode in Learnosity config
- Provide keyboard shortcuts documentation
- Test with screen readers (JAWS, NVDA, VoiceOver)
- Ensure item types are accessible (see item type guide)

**Drag-and-Drop Alternatives:**
- Provide keyboard-based alternative
- Dropdown or radio button equivalent
- Document how to use keyboard version

**Common Accessible Item Types:**
✅ Multiple choice (keyboard navigable)
✅ Text input (with labels)
✅ Multiple response (checkboxes)
✅ Simple drag-drop (with keyboard alternative)

**Challenging Item Types:**
⚠️ Complex drag-drop (needs keyboard alternative)
⚠️ Hotspot images (needs text alternative)
⚠️ Drawing tools (needs alternative response method)

**See Also:** `/universal/assessment/item-types-reference.md`

---

## Testing for WCAG Compliance

### Manual Testing Checklist

**Keyboard Navigation:**
- [ ] Tab through entire page
- [ ] All interactive elements reachable
- [ ] Focus visible on all elements
- [ ] No keyboard traps
- [ ] Logical tab order

**Screen Reader Testing:**
- [ ] Test with NVDA (Windows - free)
- [ ] Test with JAWS (Windows - paid)
- [ ] Test with VoiceOver (Mac - built-in)
- [ ] All content announced correctly
- [ ] Images have alt text read
- [ ] Form labels associated
- [ ] Headings navigable

**Visual Testing:**
- [ ] Zoom to 200% - content reflows
- [ ] Resize to 320px width - no horizontal scroll
- [ ] Color contrast sufficient (use tool)
- [ ] Content understandable without color
- [ ] Text resizable without breaking layout

**Cognitive/Language:**
- [ ] Clear instructions provided
- [ ] Error messages descriptive
- [ ] Consistent navigation and terminology
- [ ] Content organized with headings

---

### Automated Testing Tools

**Browser Extensions:**
- **axe DevTools** (Chrome, Firefox) - catches 57% of issues
- **WAVE** (WebAIM) - visual feedback on errors
- **Lighthouse** (Chrome DevTools) - accessibility audit

**Command Line:**
- **Pa11y** - automated testing
- **axe-core** - headless testing

**Limitations:** Automated tools catch ~30-50% of issues. Manual testing required.

---

### WCAG Testing Workflow

**Step 1: Automated Scan**
Run axe DevTools or Lighthouse
Fix all flagged issues

**Step 2: Manual Keyboard Test**
Navigate with Tab, Enter, Arrow keys only
Verify all functionality accessible

**Step 3: Screen Reader Test**
Test with NVDA or VoiceOver
Verify all content announced correctly

**Step 4: Visual Checks**
Verify color contrast
Test zoom and reflow
Check focus indicators

**Step 5: Content Review**
Check alt text quality
Verify heading structure
Review form labels and error messages

**Step 6: Documentation**
Document testing results
Log issues found
Track remediation

---

## Common WCAG Violations and Fixes

### ❌ Violation 1: Missing Alt Text

**Problem:**
```html
<img src="diagram.png">
```

**Fix:**
```html
<img src="diagram.png" alt="Number line showing -3 to +5 with arrow from -3 to +2">
```

---

### ❌ Violation 2: Insufficient Color Contrast

**Problem:** Gray text on white background (2:1 contrast)

**Fix:** Darken text to meet 4.5:1 ratio
- Use contrast checker tool
- Test: WebAIM Contrast Checker

---

### ❌ Violation 3: Unlabeled Form Inputs

**Problem:**
```html
<input type="text" name="answer">
```

**Fix:**
```html
<label for="answer1">What is 12 × 5?</label>
<input type="text" id="answer1" name="answer">
```

---

### ❌ Violation 4: No Keyboard Access to Custom Widget

**Problem:** Clickable div without keyboard support

**Fix:** Use `<button>` or add keyboard handlers + ARIA
```html
<button type="button">Submit Answer</button>
```

---

### ❌ Violation 5: Missing Focus Indicator

**Problem:**
```css
*:focus { outline: none; }
```

**Fix:** Remove that CSS, or provide custom high-contrast focus style
```css
:focus {
  outline: 2px solid #003057;
  outline-offset: 2px;
}
```

---

### ❌ Violation 6: Ambiguous Link Text

**Problem:**
```html
<a href="guide.html">Click here</a>
```

**Fix:**
```html
<a href="guide.html">Read the UDL implementation guide</a>
```

---

### ❌ Violation 7: Auto-Playing Video

**Problem:** Video with audio plays automatically

**Fix:** Don't autoplay, or provide pause button and mute option
```html
<video controls>
  <source src="lesson.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English">
</video>
```

---

### ❌ Violation 8: Color-Only Error Indication

**Problem:** Red border around field with no text

**Fix:** Add error message text
```html
<label for="answer">Enter your answer:</label>
<input type="text" id="answer" aria-describedby="answer-error" aria-invalid="true">
<span id="answer-error" role="alert">Error: Answer must be a number.</span>
```

---

## WCAG and UDL Alignment

**WCAG and UDL work together:**

**UDL Principle 1 (Engagement)** → WCAG Understandable
- Clear instructions (3.3.2)
- Error prevention (3.3.4)
- Consistent navigation (3.2.3)

**UDL Principle 2 (Representation)** → WCAG Perceivable
- Alt text (1.1.1)
- Multiple formats (1.3.1)
- Captions and transcripts (1.2.1, 1.2.2)

**UDL Principle 3 (Action/Expression)** → WCAG Operable
- Keyboard access (2.1.1)
- Multiple input methods (2.1.1)
- Sufficient time (2.2.1)

**See Also:** `/universal/frameworks/udl-principles-guide.md`

---

## Resources

**Official WCAG Documentation:**
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- Understanding WCAG: https://www.w3.org/WAI/WCAG21/Understanding/

**Testing Tools:**
- axe DevTools: https://www.deque.com/axe/devtools/
- WAVE: https://wave.webaim.org/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

**Screen Readers:**
- NVDA (free): https://www.nvaccess.org/
- JAWS (paid): https://www.freedomscientific.com/products/software/jaws/
- VoiceOver (Mac/iOS): Built-in

**Related Guides:**
- Alt Text Principles: `/universal/assessment/alt-text-principles.md`
- UDL Principles: `/universal/frameworks/udl-principles-guide.md`
- Item Types Accessibility: `/universal/assessment/item-types-reference.md`
- Learnosity Configuration: `/universal/assessment/learnosity-configuration-guide.md`

---

**Remember:** WCAG compliance is not just a legal requirement—it's an educational imperative. Accessible content ensures all students, including those with disabilities, can fully participate in learning. Design with accessibility from the start, not as an afterthought. When you design for accessibility, you improve the experience for everyone.
