# Algebraic Proof Variant - Sample Lesson Plan

## Lesson 1: Introduction to Congruent Triangles (Algebraic Approach)

**Duration**: 45 minutes
**Grade Level**: 9-10 (Geometry)
**Variant**: Algebraic Proof Approach

---

## Learning Objectives

Students will be able to:
1. State the definition of congruent triangles using symbolic notation
2. Identify and apply triangle congruence postulates (SSS, SAS, ASA)
3. Construct a formal two-column proof of triangle congruence
4. Justify each statement in a proof using definitions, postulates, or theorems

---

## Materials

- Two-column proof templates (printed)
- Theorem reference cards
- Ruler and protractor
- Whiteboard markers
- Student notebooks
- Geometry textbook

---

## Lesson Sequence

### Opening (5 minutes): Definition and Notation

**Formal Definition** (project on board):

```
DEFINITION: Congruent Triangles
Two triangles are congruent if and only if all corresponding sides are congruent
and all corresponding angles are congruent.

Symbolic Notation: △ABC ≅ △DEF

This notation means:
Corresponding Sides:     Corresponding Angles:
AB ≅ DE                  ∠A ≅ ∠D
BC ≅ EF                  ∠B ≅ ∠E
CA ≅ FD                  ∠C ≅ ∠F
```

**Guiding Questions**:
- "How many pairs of congruent parts must we verify? (six total: 3 sides + 3 angles)"
- "Is there a more efficient way to prove triangles congruent?"
- "Can we prove all six congruencies by establishing fewer conditions?"

**Key Concept Introduction**: "Today, we will learn three postulates that allow us to prove triangle congruence using only three strategic pieces of information. These postulates are the foundation for formal geometric proof."

---

### Direct Instruction (15 minutes): Triangle Congruence Postulates

#### Part 1: Side-Side-Side (SSS) Postulate

**Formal Statement** (students copy into notebooks):

```
POSTULATE 4-1: Side-Side-Side (SSS) Congruence Postulate

If three sides of one triangle are congruent to three sides of another triangle,
then the triangles are congruent.

Symbolic Form:
If AB ≅ DE, BC ≅ EF, and CA ≅ FD, then △ABC ≅ △DEF.
```

**Example Proof**:

```
Given: AB = 5 cm, BC = 7 cm, CA = 6 cm
       DE = 5 cm, EF = 7 cm, FD = 6 cm

Prove: △ABC ≅ △DEF

TWO-COLUMN PROOF:

Statements                          | Reasons
------------------------------------|----------------------------------------
1. AB = 5 cm, DE = 5 cm             | 1. Given
2. BC = 7 cm, EF = 7 cm             | 2. Given
3. CA = 6 cm, FD = 6 cm             | 3. Given
4. AB ≅ DE                          | 4. Definition of congruent segments
5. BC ≅ EF                          | 5. Definition of congruent segments
6. CA ≅ FD                          | 6. Definition of congruent segments
7. △ABC ≅ △DEF                      | 7. SSS Postulate (steps 4, 5, 6)
```

**Key Points to Emphasize**:
- The logical flow from given information to conclusion
- Each statement must be justified by a reason
- The reason cites a definition, postulate, or previously proven statement
- The order of vertices in congruence notation matters (correspondence)

**Check for Understanding**: "What three pieces of information do we need for SSS?" (Three pairs of congruent sides)

#### Part 2: Side-Angle-Side (SAS) Postulate

**Formal Statement**:

```
POSTULATE 4-2: Side-Angle-Side (SAS) Congruence Postulate

If two sides and the included angle of one triangle are congruent to two sides
and the included angle of another triangle, then the triangles are congruent.

Symbolic Form:
If AB ≅ DE, ∠B ≅ ∠E, and BC ≅ EF, then △ABC ≅ △DEF.

Critical Note: The angle must be INCLUDED (between the two sides).
```

**Example Proof**:

```
Given: GH = 4 cm, JK = 4 cm
       ∠H = 60°, ∠K = 60°
       HI = 5 cm, KL = 5 cm
       ∠H is included between GH and HI
       ∠K is included between JK and KL

Prove: △GHI ≅ △JKL

TWO-COLUMN PROOF:

Statements                          | Reasons
------------------------------------|----------------------------------------
1. GH = 4 cm, JK = 4 cm             | 1. Given
2. GH ≅ JK                          | 2. Definition of congruent segments
3. ∠H = 60°, ∠K = 60°               | 3. Given
4. ∠H ≅ ∠K                          | 4. Definition of congruent angles
5. HI = 5 cm, KL = 5 cm             | 5. Given
6. HI ≅ KL                          | 6. Definition of congruent segments
7. △GHI ≅ △JKL                      | 7. SAS Postulate (steps 2, 4, 6)
```

**Critical Distinction**: Non-Example of SAS

```
INCORRECT APPLICATION:

Given: PQ ≅ ST, ∠R ≅ ∠U, QR ≅ TU

Can we prove △PQR ≅ △STU by SAS?

NO. ∠R is NOT included between PQ and QR (∠Q would be included).
This is an example of SSA (Side-Side-Angle), which is NOT a valid postulate.
```

**Check for Understanding**: "How do you identify the included angle?" (It's the angle formed by the two sides)

#### Part 3: Angle-Side-Angle (ASA) Postulate

**Formal Statement**:

```
POSTULATE 4-3: Angle-Side-Angle (ASA) Congruence Postulate

If two angles and the included side of one triangle are congruent to two angles
and the included side of another triangle, then the triangles are congruent.

Symbolic Form:
If ∠M ≅ ∠P, MN ≅ PQ, and ∠N ≅ ∠Q, then △MNO ≅ △PQR.

Critical Note: The side must be INCLUDED (between the two angles).
```

**Example Proof**:

```
Given: ∠M = 50°, ∠P = 50°
       MN = 6 cm, PQ = 6 cm
       ∠N = 70°, ∠Q = 70°
       MN is included between ∠M and ∠N
       PQ is included between ∠P and ∠Q

Prove: △MNO ≅ △PQR

TWO-COLUMN PROOF:

Statements                          | Reasons
------------------------------------|----------------------------------------
1. ∠M = 50°, ∠P = 50°               | 1. Given
2. ∠M ≅ ∠P                          | 2. Definition of congruent angles
3. MN = 6 cm, PQ = 6 cm             | 3. Given
4. MN ≅ PQ                          | 4. Definition of congruent segments
5. ∠N = 70°, ∠Q = 70°               | 5. Given
6. ∠N ≅ ∠Q                          | 6. Definition of congruent angles
7. △MNO ≅ △PQR                      | 7. ASA Postulate (steps 2, 4, 6)
```

**Check for Understanding**: "Why can't we use AAS (Angle-Angle-Side) the same way?" (We will learn AAS is valid, but it's a theorem derived from ASA, not a postulate)

---

### Guided Practice (15 minutes): Constructing Two-Column Proofs

**Activity**: "Build the Proof Step-by-Step"

Distribute two-column proof templates with three problems (one SSS, one SAS, one ASA).

#### Problem 1: SSS Proof (Scaffolded)

```
Given: AB ≅ XY, BC ≅ YZ, CA ≅ ZX

Prove: △ABC ≅ △XYZ

TWO-COLUMN PROOF TEMPLATE:

Statements                          | Reasons
------------------------------------|----------------------------------------
1. AB ≅ XY                          | 1. _______________________
2. BC ≅ YZ                          | 2. _______________________
3. CA ≅ ZX                          | 3. _______________________
4. △ABC ≅ △XYZ                      | 4. _______________________
```

**Teacher Guidance** (think-aloud):
- "Statement 1 comes from our given information, so the reason is 'Given.'"
- "We repeat this process for all given conditions."
- "Statement 4 is our conclusion. What postulate allows us to conclude this?" (SSS)
- "We cite the postulate and reference the statements we used (steps 1, 2, 3)."

**Students Complete**: Fill in all reasons.

#### Problem 2: SAS Proof (Partially Scaffolded)

```
Given: PQ ≅ ST, ∠Q ≅ ∠T, QR ≅ TU

Prove: △PQR ≅ △STU

TWO-COLUMN PROOF TEMPLATE:

Statements                          | Reasons
------------------------------------|----------------------------------------
1. ____________________             | 1. Given
2. ____________________             | 2. Given
3. ____________________             | 3. Given
4. △PQR ≅ △STU                      | 4. _______________________
```

**Teacher Guidance**:
- "First, write all given information as statements."
- "Then, identify which postulate applies. Is this SSS, SAS, or ASA?"
- "Check: Is the angle included between the two sides? Yes, ∠Q is between PQ and QR."
- "Complete the proof by citing the SAS Postulate."

**Students Complete**: Fill in statements 1-3 and reason 4.

#### Problem 3: ASA Proof (Minimal Scaffolding)

```
Given: ∠J ≅ ∠M, JK ≅ MN, ∠K ≅ ∠N

Prove: △JKL ≅ △MNO

TWO-COLUMN PROOF TEMPLATE:

Statements                          | Reasons
------------------------------------|----------------------------------------
1.                                  | 1.
2.                                  | 2.
3.                                  | 3.
4.                                  | 4.
```

**Teacher Guidance**:
- "This proof is similar in structure to the previous two."
- "Identify which postulate applies first, then construct the proof."
- "Remember: All given information goes in statements, all with the reason 'Given.'"

**Students Complete**: Entire proof independently.

**Differentiation**:
- **Support**: Provide word bank of reasons (Given, SSS Postulate, SAS Postulate, ASA Postulate)
- **Extension**: Challenge students to write a proof where they must use the Definition of Congruent Segments/Angles before applying the postulate (convert numerical measures to congruence statements)

**Circulate and Monitor**: Check for:
- All given information stated explicitly
- Correct identification of postulate
- Proper citation format (postulate name + step numbers)
- Logical flow from statements to conclusion

---

### Independent Practice (8 minutes): Proof Construction

**Activity**: "Complete Proofs Independently"

Provide three new triangle congruence problems (one for each postulate: SSS, SAS, ASA).

#### Problem 1: SSS

```
Given: Diagram shows △ABC and △DEF with markings:
       AB ≅ DE (single tick mark)
       BC ≅ EF (double tick mark)
       CA ≅ FD (triple tick mark)

Prove: △ABC ≅ △DEF

Construct a two-column proof.
```

#### Problem 2: SAS

```
Given: Diagram shows △GHI and △JKL with markings:
       GH ≅ JK (single tick mark)
       ∠H ≅ ∠K (arc marking)
       HI ≅ KL (double tick mark)

Prove: △GHI ≅ △JKL

Construct a two-column proof.
```

#### Problem 3: ASA

```
Given: Diagram shows △MNO and △PQR with markings:
       ∠M ≅ ∠P (single arc)
       MN ≅ PQ (single tick mark)
       ∠N ≅ ∠Q (double arc)

Prove: △MNO ≅ △PQR

Construct a two-column proof.
```

**Success Criteria** (displayed on board):
- [ ] All given information stated as separate statements
- [ ] All statements have corresponding reasons
- [ ] Reasons cite appropriate source (Given, postulate, definition)
- [ ] Correct postulate identified (SSS, SAS, or ASA)
- [ ] Conclusion states triangle congruence with proper notation
- [ ] Final reason cites postulate and relevant statement numbers

**Example Student Work** (SSS proof):

```
Statements                          | Reasons
------------------------------------|----------------------------------------
1. AB ≅ DE                          | 1. Given
2. BC ≅ EF                          | 2. Given
3. CA ≅ FD                          | 3. Given
4. △ABC ≅ △DEF                      | 4. SSS Postulate (statements 1, 2, 3)
```

---

### Closure (2 minutes): Formal Summary

**Quick Review**:
- "What are the three triangle congruence postulates we learned today?" (SSS, SAS, ASA)
- "What does 'included' mean?" (Between two other elements)
- "Why do we need reasons in a proof?" (To justify each statement logically)

**Formal Summary** (project on board, students copy):

```
TRIANGLE CONGRUENCE POSTULATES

SSS (Side-Side-Side)
Three pairs of congruent sides → triangles congruent

SAS (Side-Angle-Side)
Two pairs of congruent sides + included angle → triangles congruent
*Angle must be BETWEEN the two sides*

ASA (Angle-Side-Angle)
Two pairs of congruent angles + included side → triangles congruent
*Side must be BETWEEN the two angles*

TWO-COLUMN PROOF FORMAT:
Statements | Reasons
All statements justified by: Given, Definition, Postulate, or Theorem
```

**Exit Ticket**: "Write the formal statement of the SAS Postulate in your own words. Include the symbolic form."

---

## Assessment

### Formative Assessment (During Lesson)

**Observation Checklist**:
- [ ] Correctly states definitions using precise mathematical language
- [ ] Identifies which postulate applies (SSS, SAS, ASA)
- [ ] Recognizes included angles and sides
- [ ] Writes statements in logical order
- [ ] Cites appropriate reasons for each statement
- [ ] Uses proper congruence notation (≅ symbol, correct vertex order)

### Exit Ticket (End of Lesson)

**Prompt**: Write the formal statement of the SAS Postulate. Include:
1. Hypothesis (If...)
2. Conclusion (Then...)
3. Symbolic form with variables
4. Note about "included angle"

**Scoring Rubric**:
- **4 points**: Complete formal statement, correct symbolic form, included angle clarified
- **3 points**: Mostly correct, minor notation or language errors
- **2 points**: Incomplete or partially incorrect statement
- **1 point**: Minimal understanding demonstrated
- **0 points**: No attempt or entirely incorrect

**Expected Response**:
```
SAS Postulate: If two sides and the included angle of one triangle are congruent to
two sides and the included angle of another triangle, then the triangles are congruent.

Symbolic: If AB ≅ DE, ∠B ≅ ∠E, and BC ≅ EF, then △ABC ≅ △DEF.

The angle ∠B is included between sides AB and BC (similarly for ∠E).
```

---

## Differentiation Strategies

### For English Learners:
- Provide vocabulary list with definitions (congruent, postulate, included, hypothesis, conclusion)
- Use sentence frames for proof statements: "_____ is congruent to _____ because _____."
- Allow use of symbols (≅) instead of writing "is congruent to"
- Pair with native English speaker for collaborative proof construction

### For Students with IEPs:
- Provide partially completed proofs (fill-in-the-blank format)
- Use color-coding: Given statements in blue, conclusion in green, postulates in red
- Allow verbal explanation of proof logic before writing formal proof
- Provide reference sheet with all three postulates and examples

### For Advanced Learners:
- Challenge: "Prove the triangles are congruent using a different postulate if possible."
- Extension: "Why is SSA (Side-Side-Angle) not a valid postulate? Construct a counterexample."
- Investigate: "Can you develop a proof that uses multiple steps (more than just given → postulate → conclusion)?"

---

## Teacher Notes

### Common Misconceptions (Algebraic Approach):

1. **Misconception**: "Any three pieces of information prove triangle congruence."
   - **Address**: Show counterexample with AAA (three angles) → triangles are similar but not congruent
   - **Address**: Show counterexample with SSA → ambiguous case, two different triangles possible

2. **Misconception**: "The order of vertices doesn't matter in congruence notation."
   - **Address**: Emphasize that △ABC ≅ △DEF means A↔D, B↔E, C↔F (correspondence matters)
   - **Address**: Show that △ABC ≅ △EDF would imply different correspondences

3. **Misconception**: "Reasons can be anything that sounds logical."
   - **Address**: Emphasize that reasons must cite specific sources: Given, Definition, Postulate, Theorem (or previously proven statement)
   - **Address**: "Because it looks right" or "It's obvious" are not valid reasons in formal proof

4. **Misconception**: "SAS and SSA are the same thing."
   - **Address**: Use diagram showing included vs. non-included angle
   - **Address**: Construct counterexample where SSA does not guarantee congruence

### Proof Writing Tips:

- **Start with Given**: Always begin by stating all given information
- **Identify the Goal**: Write the "Prove" statement; this is your final statement
- **Choose the Postulate**: Determine which postulate applies based on given info
- **Logical Flow**: Each statement should follow logically from previous statements
- **Cite Steps**: When using a postulate, reference the statement numbers that provide the required information

### Time Management:

- If running short: Reduce independent practice to 2 problems (skip one postulate)
- If extra time: Add "Error Analysis" activity where students find mistakes in flawed proofs

### Vocabulary Emphasis:

Critical terms to reinforce:
- **Congruent** (≅): Same size and shape
- **Postulate**: A statement accepted as true without proof
- **Included angle**: The angle formed by two sides
- **Included side**: The side connecting two angles
- **Hypothesis**: The "if" part of a conditional statement
- **Conclusion**: The "then" part of a conditional statement
- **Correspondence**: The matching of vertices (e.g., A↔D, B↔E, C↔F)

---

## Home Practice (Optional)

**Assignment**: "Formal Proof Practice"

Complete three two-column proofs (provided on worksheet):
1. SSS proof with all statements given (fill in reasons only)
2. SAS proof with some statements and reasons missing
3. ASA proof constructed from scratch

**Purpose**: Build fluency with two-column proof format and postulate application

**Optional Extension**:
Research the difference between a postulate and a theorem. Write 2-3 sentences explaining why SSS, SAS, and ASA are postulates rather than theorems.

---

## Alignment to Standards

**CCSS.MATH.CONTENT.HSG.CO.B.7**: Use the definition of congruence in terms of rigid motions to show that two triangles are congruent if and only if corresponding pairs of sides and corresponding pairs of angles are congruent.

**CCSS.MATH.CONTENT.HSG.CO.B.8**: Explain how the criteria for triangle congruence (ASA, SAS, and SSS) follow from the definition of congruence in terms of rigid motions.

**CCSS.MATH.PRACTICE.MP3**: Construct viable arguments and critique the reasoning of others. (Two-column proof construction develops logical argumentation skills.)

---

## Connection to Formal Logic

**Optional Enrichment** (if time allows):

Triangle congruence proofs exemplify deductive reasoning:

```
LOGICAL STRUCTURE:

Premise 1: All triangles with three pairs of congruent sides are congruent (SSS Postulate)
Premise 2: △ABC and △DEF have three pairs of congruent sides (Given)
Conclusion: △ABC and △DEF are congruent (Deductive reasoning)

This follows the form:
If P, then Q.  (Postulate)
P is true.      (Given)
Therefore, Q.   (Conclusion)
```

This logical structure (modus ponens) underlies all geometric proofs.

---

**Lesson Version**: 1.0 (Algebraic Variant)
**Last Updated**: 2025-11-04
**Fidelity Checklist**: See Appendix C in main experiment document
