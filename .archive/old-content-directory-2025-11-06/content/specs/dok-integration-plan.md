# Webb's Depth of Knowledge (DOK) Integration Plan
## Implementation Blueprint for Automated Agent Execution

**Version**: 1.0.0
**Date**: 2025-11-05
**Framework**: Professor 2.0.0
**Estimated Effort**: 40-50 hours automated work
**Priority**: High

---

## Executive Summary

This plan details the step-by-step integration of Webb's Depth of Knowledge (DOK) framework into the Professor learning engineering platform. The implementation will add DOK classification, validation, and analysis capabilities across all curriculum and assessment skills.

**Success Criteria**:
- All assessment items can be tagged with DOK levels (1-4)
- Review skills validate DOK alignment between standards, objectives, instruction, and assessment
- Analytics can disaggregate performance by DOK level
- Documentation and examples demonstrate usage

---

## Phase 1: Create DOK Framework Foundation

### 1.1 Create DOK Framework Data Structures

**File**: `professor/framework/dok/schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "DOKLevel": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4,
      "description": "Webb's DOK level: 1=Recall, 2=Skill/Concept, 3=Strategic Thinking, 4=Extended Thinking"
    },
    "Subject": {
      "type": "string",
      "enum": ["mathematics", "ela", "science", "social-studies"],
      "description": "Content area with subject-specific DOK descriptors"
    },
    "DOKClassification": {
      "type": "object",
      "required": ["dok_level", "subject", "rationale"],
      "properties": {
        "dok_level": {"$ref": "#/definitions/DOKLevel"},
        "subject": {"$ref": "#/definitions/Subject"},
        "rationale": {
          "type": "string",
          "description": "Evidence-based justification for DOK level assignment"
        },
        "indicators": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Specific DOK indicators from framework that apply"
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Confidence score for classification (0-1)"
        },
        "classified_by": {
          "type": "string",
          "enum": ["human", "automated", "hybrid"],
          "description": "Source of classification"
        },
        "classified_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "DOKDistribution": {
      "type": "object",
      "required": ["dok1_count", "dok2_count", "dok3_count", "dok4_count"],
      "properties": {
        "dok1_count": {"type": "integer", "minimum": 0},
        "dok2_count": {"type": "integer", "minimum": 0},
        "dok3_count": {"type": "integer", "minimum": 0},
        "dok4_count": {"type": "integer", "minimum": 0},
        "dok1_percent": {"type": "number"},
        "dok2_percent": {"type": "number"},
        "dok3_percent": {"type": "number"},
        "dok4_percent": {"type": "number"},
        "total_items": {"type": "integer"},
        "balance_score": {
          "type": "number",
          "description": "0-100 score for DOK distribution balance"
        }
      }
    }
  }
}
```

**Acceptance Criteria**:
- Schema validates valid DOK classifications
- Schema rejects invalid DOK levels (e.g., 0, 5, non-integers)
- All required fields enforced

---

### 1.2 Create DOK Descriptor Libraries

**File**: `professor/framework/dok/descriptors/mathematics.json`

```json
{
  "subject": "mathematics",
  "version": "Webb 2014",
  "levels": {
    "1": {
      "name": "Recall",
      "description": "Rote recall of information or performance of simple, routine procedures",
      "indicators": [
        "Recall or recognize a fact, term, or property",
        "Perform a one-step computation or well-defined algorithm",
        "Execute a multi-step procedure with clear steps (e.g., long division, finding mean)",
        "Read information directly from graph/table",
        "Apply a memorized formula",
        "Plot points on coordinate system",
        "Use coordinates with distance formula",
        "Draw lines of symmetry",
        "Solve quadratic equation using well-known procedures (factoring, quadratic formula)",
        "Solve system of linear equations using standard methods (substitution, elimination)",
        "Operate on polynomials/radicals using standard procedures",
        "Simplify rational expressions using rote procedures"
      ],
      "keywords": ["recall", "recognize", "identify", "calculate", "compute", "apply formula"],
      "characteristics": [
        "Student either knows answer or does not",
        "No figuring out required",
        "Straightforward context with obvious solution path",
        "Single correct answer",
        "Keywords indicate operation needed"
      ],
      "examples": [
        "What is 7 × 8?",
        "Find the mean of 3, 7, 12, 8",
        "Solve for x: 2x + 5 = 13",
        "What is the formula for area of a circle?",
        "Plot the point (3, -2) on a coordinate plane"
      ]
    },
    "2": {
      "name": "Skill/Concept",
      "description": "Mental processing beyond habitual response; decision-making; conceptual understanding",
      "indicators": [
        "Distinguish among mathematical ideas",
        "Process information about underlying structure",
        "Draw relationships among ideas",
        "Decide among and perform appropriate skills",
        "Apply properties/conventions in relevant context",
        "Transform among different representations",
        "Interpret and solve problems with graphs",
        "Formulate equation/inequality from problem statement",
        "Derive and report solution in context",
        "Classify, organize, estimate with multiple attributes",
        "Construct graph and interpret meaning of critical features",
        "Describe effects of parameter changes on functions",
        "Illustrate computation with different representations",
        "Use measures of central tendency to compare data sets",
        "Explain reasons for action or application of property",
        "Perform visualization tasks (mental rotation, transformations)",
        "Determine sample space or probability of compound event",
        "Detect/describe non-trivial patterns"
      ],
      "keywords": ["explain", "interpret", "classify", "organize", "compare", "represent", "model"],
      "characteristics": [
        "Requires conceptual understanding",
        "Multiple steps with decision-making",
        "Context requires interpretation",
        "May have multiple valid approaches",
        "Requires explaining thinking"
      ],
      "examples": [
        "Explain why multiplying two negative numbers results in a positive number",
        "Compare the growth rates of linear and exponential functions",
        "Model this word problem with an equation: 'Maria has 3 times as many books as Juan. Together they have 24 books.'",
        "Interpret what the y-intercept means in this context",
        "Which measure of central tendency best represents this data set? Explain."
      ]
    },
    "3": {
      "name": "Strategic Thinking",
      "description": "Reasoning and analyzing using mathematical principles; novel solutions; proofs; mathematical arguments",
      "indicators": [
        "Solve non-routine, abstract, complex problems",
        "Conjecture and test hypotheses",
        "Create novel solutions and representations",
        "Devise original proofs",
        "Construct mathematical arguments",
        "Critique mathematical arguments",
        "Build mathematical models considering constraints",
        "Form robust inferences and predictions",
        "Produce sound and valid mathematical arguments",
        "Verify answers through multiple methods",
        "Develop proofs or draw inferences",
        "Apply properties in proving theorems/identities",
        "Make sense of mathematics in situations",
        "Derive new formulas",
        "Design and conduct experiments"
      ],
      "keywords": ["prove", "justify", "critique", "construct model", "analyze", "generalize", "hypothesize"],
      "characteristics": [
        "Solution path not obvious from first reading",
        "Requires demanding reasoning",
        "Can be solved multiple ways",
        "May have multiple correct solutions",
        "Requires mathematical argumentation",
        "Abstract reasoning required",
        "Prior knowledge determines sophistication"
      ],
      "examples": [
        "Prove that the sum of any two odd numbers is always even",
        "Develop a formula for the nth term of this pattern: 3, 7, 11, 15...",
        "Critique this student's solution and identify the error in their reasoning",
        "Design an experiment to determine if your dice is fair",
        "Construct a mathematical model for population growth that accounts for limited resources"
      ]
    },
    "4": {
      "name": "Extended Thinking",
      "description": "Complex reasoning over extended time (days/weeks); research; original work; metacognitive awareness",
      "indicators": [
        "Conduct research project requiring planning and verification",
        "Execute performance activity over time",
        "Design and implement multi-week experiment",
        "Create new theorem and proof",
        "Develop complex mathematical model with multiple variables",
        "Synthesize ideas in novel ways",
        "Create original models or approaches",
        "Critique body of work",
        "Make connections among multiple ideas/content areas",
        "Select appropriate approach among many alternatives"
      ],
      "keywords": ["design project", "conduct research", "synthesize", "create original", "investigate over time"],
      "characteristics": [
        "Requires days/weeks to complete",
        "Allows for creation of original work",
        "Requires metacognitive awareness",
        "Complex reasoning and planning",
        "Research and verification needed",
        "Connects multiple ideas or content areas",
        "Not just repetitive work over time"
      ],
      "examples": [
        "Design and conduct a month-long experiment to model traffic flow at your school and propose improvements",
        "Develop a mathematical model of climate change using multiple variables and data sources",
        "Research the history of a mathematical theorem, recreate the original proof, and extend it to a new domain",
        "Create an original mathematical game that teaches algebraic concepts, playtest it, and refine based on data"
      ]
    }
  },
  "classification_rules": {
    "verb_analysis": {
      "note": "Verbs alone do not determine DOK; must consider what verb acts upon",
      "examples": {
        "identify": {
          "dok1": "Identify attributes of a polygon",
          "dok2": "Identify the rate of change for an exponential function"
        },
        "describe": {
          "dok1": "Describe steps used to solve (show work)",
          "dok2": "Describe mathematical argument/rationale for solution"
        }
      }
    },
    "context_matters": {
      "prior_knowledge": "Classification depends on typical student experience at grade level",
      "grade_level": "Same task may be different DOK at different grades"
    }
  }
}
```

**Additional Files to Create**:
- `professor/framework/dok/descriptors/ela.json` (placeholder for future)
- `professor/framework/dok/descriptors/science.json` (placeholder for future)
- `professor/framework/dok/descriptors/social-studies.json` (placeholder for future)

**Acceptance Criteria**:
- All 4 DOK levels documented with mathematics descriptors
- Minimum 8 indicators per level
- Minimum 5 examples per level
- Classification rules and edge cases documented

---

### 1.3 Create DOK Classification Engine

**File**: `professor/framework/dok/classifier.py`

```python
"""
DOK Classification Engine
Analyzes tasks, items, and objectives to assign Webb's DOK levels
"""

import json
import re
from typing import Dict, List, Tuple
from datetime import datetime

class DOKClassifier:
    """Classifies educational content by Webb's Depth of Knowledge level"""

    def __init__(self, subject: str = "mathematics"):
        """
        Initialize classifier with subject-specific descriptors

        Args:
            subject: Content area (mathematics, ela, science, social-studies)
        """
        self.subject = subject
        self.descriptors = self._load_descriptors(subject)
        self.schema = self._load_schema()

    def _load_descriptors(self, subject: str) -> Dict:
        """Load DOK descriptors for subject"""
        path = f"professor/framework/dok/descriptors/{subject}.json"
        with open(path, 'r') as f:
            return json.load(f)

    def _load_schema(self) -> Dict:
        """Load DOK schema"""
        with open("professor/framework/dok/schema.json", 'r') as f:
            return json.load(f)

    def classify_item(self, item_text: str, context: Dict = None) -> Dict:
        """
        Classify an assessment item or task

        Args:
            item_text: The item/task text to classify
            context: Optional context (grade_level, standard, etc.)

        Returns:
            DOKClassification object with level, rationale, indicators, confidence
        """
        # Extract linguistic features
        features = self._extract_features(item_text)

        # Analyze against each DOK level
        scores = {}
        for level in ["1", "2", "3", "4"]:
            score, indicators = self._score_level(features, level, context)
            scores[level] = {
                "score": score,
                "indicators": indicators
            }

        # Determine best match
        best_level = max(scores, key=lambda k: scores[k]["score"])
        confidence = scores[best_level]["score"]

        # Generate rationale
        rationale = self._generate_rationale(
            best_level,
            scores[best_level]["indicators"],
            features
        )

        return {
            "dok_level": int(best_level),
            "subject": self.subject,
            "rationale": rationale,
            "indicators": scores[best_level]["indicators"],
            "confidence": confidence,
            "classified_by": "automated",
            "classified_at": datetime.utcnow().isoformat()
        }

    def _extract_features(self, text: str) -> Dict:
        """Extract linguistic and structural features from text"""
        features = {
            "text": text,
            "verbs": self._extract_verbs(text),
            "complexity_indicators": [],
            "word_count": len(text.split()),
            "has_multiple_steps": False,
            "requires_explanation": False,
            "requires_proof": False,
            "requires_creation": False,
            "has_context": False,
            "solution_path_obvious": True
        }

        # Detect explanation requirements
        explanation_patterns = [
            r"\bexplain\b", r"\bjustify\b", r"\bshow\s+your\s+(work|reasoning)\b",
            r"\bwhy\b", r"\bhow\s+do\s+you\s+know\b"
        ]
        features["requires_explanation"] = any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in explanation_patterns
        )

        # Detect proof requirements
        proof_patterns = [r"\bprove\b", r"\bshow\s+that\b", r"\bdemonstrate\s+that\b"]
        features["requires_proof"] = any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in proof_patterns
        )

        # Detect creation requirements
        creation_patterns = [
            r"\bcreate\b", r"\bdesign\b", r"\bdevelop\b",
            r"\bconstruct\b", r"\bdevise\b"
        ]
        features["requires_creation"] = any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in creation_patterns
        )

        # Detect context/word problems
        context_indicators = [
            r"\bMaria\b", r"\bJohn\b", r"\bstudent\b",  # names/people
            r"\bstore\b", r"\bschool\b", r"\bhome\b",    # places
            r"\bprice\b", r"\bcost\b", r"\bsell\b"       # real-world
        ]
        features["has_context"] = any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in context_indicators
        )

        return features

    def _extract_verbs(self, text: str) -> List[str]:
        """Extract action verbs from text"""
        # Simple verb extraction (in production, use NLP library)
        common_verbs = [
            "solve", "calculate", "find", "compute", "identify",
            "explain", "justify", "prove", "describe", "compare",
            "analyze", "evaluate", "create", "design", "construct",
            "classify", "organize", "interpret", "model", "represent"
        ]

        found_verbs = []
        text_lower = text.lower()
        for verb in common_verbs:
            if verb in text_lower:
                found_verbs.append(verb)

        return found_verbs

    def _score_level(self, features: Dict, level: str, context: Dict) -> Tuple[float, List[str]]:
        """
        Score how well features match a DOK level

        Returns:
            (score, matched_indicators)
        """
        score = 0.0
        matched_indicators = []

        level_data = self.descriptors["levels"][level]
        indicators = level_data["indicators"]
        keywords = level_data.get("keywords", [])

        # Check verb alignment
        for verb in features["verbs"]:
            if verb in keywords:
                score += 0.2
                matched_indicators.append(f"Verb '{verb}' aligns with DOK {level}")

        # Level-specific scoring
        if level == "1":
            # DOK 1: Simple, routine, obvious solution
            if features["word_count"] < 20:
                score += 0.3
            if not features["requires_explanation"]:
                score += 0.2
            if not features["requires_proof"]:
                score += 0.2
            if features["solution_path_obvious"]:
                score += 0.3
                matched_indicators.append("Solution path is obvious")

        elif level == "2":
            # DOK 2: Conceptual understanding, interpretation
            if features["requires_explanation"]:
                score += 0.4
                matched_indicators.append("Requires explanation of thinking")
            if features["has_context"]:
                score += 0.3
                matched_indicators.append("Involves contextual interpretation")
            if "compare" in features["verbs"] or "interpret" in features["verbs"]:
                score += 0.3

        elif level == "3":
            # DOK 3: Strategic thinking, proofs, novel solutions
            if features["requires_proof"]:
                score += 0.5
                matched_indicators.append("Requires mathematical proof or argument")
            if features["requires_creation"]:
                score += 0.3
                matched_indicators.append("Requires creating novel solution")
            if "prove" in features["verbs"] or "justify" in features["verbs"]:
                score += 0.4

        elif level == "4":
            # DOK 4: Extended thinking over time
            if features["requires_creation"] and features["word_count"] > 50:
                score += 0.4
            extended_keywords = ["project", "research", "over time", "days", "weeks"]
            if any(kw in features["text"].lower() for kw in extended_keywords):
                score += 0.6
                matched_indicators.append("Indicates extended time requirement")

        # Normalize score
        score = min(score, 1.0)

        return score, matched_indicators

    def _generate_rationale(self, level: str, indicators: List[str], features: Dict) -> str:
        """Generate human-readable rationale for classification"""
        level_name = self.descriptors["levels"][level]["name"]
        rationale = f"Classified as DOK {level} ({level_name}) because:\n"

        for indicator in indicators[:3]:  # Top 3 indicators
            rationale += f"- {indicator}\n"

        return rationale.strip()

    def classify_batch(self, items: List[str]) -> List[Dict]:
        """Classify multiple items"""
        return [self.classify_item(item) for item in items]

    def calculate_distribution(self, classifications: List[Dict]) -> Dict:
        """Calculate DOK distribution for a set of items"""
        counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for classification in classifications:
            level = classification["dok_level"]
            counts[level] += 1

        total = len(classifications)

        distribution = {
            "dok1_count": counts[1],
            "dok2_count": counts[2],
            "dok3_count": counts[3],
            "dok4_count": counts[4],
            "total_items": total
        }

        if total > 0:
            distribution["dok1_percent"] = round((counts[1] / total) * 100, 1)
            distribution["dok2_percent"] = round((counts[2] / total) * 100, 1)
            distribution["dok3_percent"] = round((counts[3] / total) * 100, 1)
            distribution["dok4_percent"] = round((counts[4] / total) * 100, 1)

            # Calculate balance score (0-100)
            # Ideal: 20% DOK1, 40% DOK2, 30% DOK3, 10% DOK4
            ideal = [0.20, 0.40, 0.30, 0.10]
            actual = [counts[i]/total for i in range(1, 5)]
            deviation = sum(abs(actual[i] - ideal[i]) for i in range(4))
            distribution["balance_score"] = round(max(0, 100 - (deviation * 100)), 1)

        return distribution
```

**File**: `professor/framework/dok/__init__.py`

```python
"""Webb's Depth of Knowledge Framework"""

from .classifier import DOKClassifier

__all__ = ['DOKClassifier']
```

**Acceptance Criteria**:
- Classifier can analyze text and assign DOK levels
- Returns confidence scores
- Generates evidence-based rationales
- Calculates distributions
- Unit tests pass (see Phase 9)

---

### 1.4 Create DOK Utilities

**File**: `professor/framework/dok/utils.py`

```python
"""DOK Framework Utilities"""

import json
from typing import Dict, List

def validate_dok_classification(classification: Dict) -> bool:
    """Validate a DOK classification object against schema"""
    required_fields = ["dok_level", "subject", "rationale"]

    if not all(field in classification for field in required_fields):
        return False

    if classification["dok_level"] not in [1, 2, 3, 4]:
        return False

    if classification["subject"] not in ["mathematics", "ela", "science", "social-studies"]:
        return False

    return True

def format_dok_display(classification: Dict) -> str:
    """Format DOK classification for display"""
    level = classification["dok_level"]
    level_names = {1: "Recall", 2: "Skill/Concept", 3: "Strategic Thinking", 4: "Extended Thinking"}

    output = f"**DOK Level {level}: {level_names[level]}**\n\n"
    output += f"{classification['rationale']}\n\n"

    if "confidence" in classification:
        confidence_pct = int(classification["confidence"] * 100)
        output += f"Confidence: {confidence_pct}%\n"

    return output

def analyze_dok_alignment(
    standard_dok: int,
    objective_dok: int,
    assessment_dok: int
) -> Dict:
    """
    Analyze DOK alignment between standard, objective, and assessment

    Returns alignment report with issues
    """
    issues = []
    aligned = True

    # Assessment should match or be within 1 level of standard
    if abs(assessment_dok - standard_dok) > 1:
        issues.append(
            f"Assessment DOK ({assessment_dok}) is more than 1 level away from "
            f"standard DOK ({standard_dok}). This indicates misalignment."
        )
        aligned = False

    # Objective should support assessment
    if objective_dok < assessment_dok - 1:
        issues.append(
            f"Objective DOK ({objective_dok}) is too low to support "
            f"assessment DOK ({assessment_dok}). Students may not be prepared."
        )
        aligned = False

    # Assessment shouldn't be easier than objective
    if assessment_dok < objective_dok - 1:
        issues.append(
            f"Assessment DOK ({assessment_dok}) is lower than objective DOK ({objective_dok}). "
            f"Assessment doesn't measure what students are expected to learn."
        )
        aligned = False

    return {
        "aligned": aligned,
        "issues": issues,
        "standard_dok": standard_dok,
        "objective_dok": objective_dok,
        "assessment_dok": assessment_dok
    }

def recommend_dok_distribution(
    num_items: int,
    grade_band: str = "6-12"
) -> Dict:
    """
    Recommend DOK distribution for an assessment

    Args:
        num_items: Total number of items
        grade_band: K-5, 6-8, 9-12, or college

    Returns:
        Recommended counts per DOK level
    """
    # Default distributions by grade band
    distributions = {
        "K-5": {"dok1": 0.30, "dok2": 0.50, "dok3": 0.15, "dok4": 0.05},
        "6-8": {"dok1": 0.25, "dok2": 0.45, "dok3": 0.25, "dok4": 0.05},
        "9-12": {"dok1": 0.20, "dok2": 0.40, "dok3": 0.30, "dok4": 0.10},
        "college": {"dok1": 0.15, "dok2": 0.35, "dok3": 0.35, "dok4": 0.15}
    }

    dist = distributions.get(grade_band, distributions["9-12"])

    return {
        "dok1_recommended": int(num_items * dist["dok1"]),
        "dok2_recommended": int(num_items * dist["dok2"]),
        "dok3_recommended": int(num_items * dist["dok3"]),
        "dok4_recommended": int(num_items * dist["dok4"]),
        "total_items": num_items,
        "distribution_rationale": f"Based on recommended distribution for {grade_band}"
    }
```

**Acceptance Criteria**:
- Validation functions work correctly
- Alignment analysis identifies misalignment
- Recommendations provided for different grade bands

---

## Phase 2: Create New DOK Skills

### 2.1 Create `curriculum-classify-dok` Skill

**File**: `.claude/skills/curriculum-classify-dok.md`

```markdown
# curriculum-classify-dok

Analyzes educational tasks, assessment items, or learning objectives and assigns Webb's Depth of Knowledge (DOK) levels with evidence-based rationales.

## Description

This skill classifies content by cognitive complexity using Webb's DOK framework:
- **DOK 1 (Recall)**: Memorized facts, simple procedures, well-known algorithms
- **DOK 2 (Skill/Concept)**: Conceptual understanding, decision-making, interpretation
- **DOK 3 (Strategic Thinking)**: Reasoning, proofs, novel solutions, mathematical arguments
- **DOK 4 (Extended Thinking)**: Multi-day projects, research, original work

Use this skill when you need to:
- Tag assessment items with DOK levels
- Validate existing DOK classifications
- Understand cognitive complexity of tasks
- Ensure appropriate challenge levels

## Usage

**Basic Classification:**
```bash
/curriculum-classify-dok --item "What is 7 × 8?"
/curriculum-classify-dok --item "Explain why multiplying two negative numbers gives a positive result"
/curriculum-classify-dok --item "Prove that the sum of two even numbers is always even"
```

**Batch Classification:**
```bash
/curriculum-classify-dok --file assessment-items.json
```

**With Context:**
```bash
/curriculum-classify-dok --item "Solve for x: 2x + 5 = 13" --grade "6" --subject "mathematics"
```

## Input Format

**Single Item:**
```json
{
  "item_text": "Compare the growth rates of linear and exponential functions",
  "subject": "mathematics",
  "grade_level": "9-12",
  "context": "Algebra 1 unit on functions"
}
```

**Batch Items (JSON file):**
```json
{
  "items": [
    {"id": "1", "text": "What is the area formula for a circle?"},
    {"id": "2", "text": "Explain how changing the coefficient affects a linear function"},
    {"id": "3", "text": "Prove the Pythagorean theorem using similar triangles"}
  ],
  "subject": "mathematics",
  "grade_level": "8"
}
```

## Output Format

```json
{
  "item_id": "1",
  "item_text": "Prove that the sum of two even numbers is always even",
  "classification": {
    "dok_level": 3,
    "subject": "mathematics",
    "rationale": "Classified as DOK 3 (Strategic Thinking) because:\n- Requires mathematical proof or argument\n- Verb 'prove' aligns with DOK 3\n- Requires reasoning about number properties",
    "indicators": [
      "Requires mathematical proof or argument",
      "Verb 'prove' aligns with DOK 3",
      "Must generalize beyond specific examples"
    ],
    "confidence": 0.95,
    "classified_by": "automated",
    "classified_at": "2025-11-05T10:30:00Z"
  }
}
```

## Implementation

When this skill is invoked:

1. **Load DOK Framework**
   - Import `DOKClassifier` from `professor/framework/dok/classifier.py`
   - Initialize with appropriate subject (default: mathematics)

2. **Parse Input**
   - Extract item text, subject, grade level, context
   - Handle single items or batch files

3. **Classify Each Item**
   ```python
   from professor.framework.dok import DOKClassifier

   classifier = DOKClassifier(subject=subject)
   classification = classifier.classify_item(item_text, context)
   ```

4. **Format Output**
   - Generate human-readable display with DOK level and rationale
   - If batch, include summary statistics
   - Save results to file if requested

5. **Provide Recommendations**
   - If item is DOK 1 and context suggests higher DOK needed, recommend enhancement
   - If confidence is low (<0.6), flag for human review

## Examples

**Example 1: Simple Recall**
```
Input: "What is 15% of 80?"
Output: DOK 1 (Recall) - Direct application of percentage formula; no interpretation needed
```

**Example 2: Conceptual Understanding**
```
Input: "Explain why the median is a better measure than the mean for this skewed data set"
Output: DOK 2 (Skill/Concept) - Requires conceptual understanding of measures of central tendency and interpretation in context
```

**Example 3: Strategic Thinking**
```
Input: "Design a fair game using two dice where each player has equal probability of winning"
Output: DOK 3 (Strategic Thinking) - Requires novel solution, probability analysis, and verification of fairness
```

## Notes

- Classification depends on typical student experience at grade level
- Same task may have different DOK at different grades
- Verbs alone don't determine DOK - must consider what verb acts upon
- Low confidence scores (<0.6) should trigger human review
- Subject-specific descriptors currently available for mathematics only

## Related Skills

- `curriculum-develop-items` - Creates assessment items (now with DOK tagging)
- `curriculum-assess-design` - Designs assessment blueprints (should specify DOK distribution)
- `curriculum-review-pedagogy` - Reviews quality (includes DOK alignment checks)
```

**File**: `.claude/skills/curriculum-classify-dok` (executable wrapper)

```bash
#!/bin/bash
# Wrapper script for curriculum-classify-dok skill
python3 -m professor.skills.curriculum_classify_dok "$@"
```

**File**: `professor/skills/curriculum_classify_dok.py`

```python
#!/usr/bin/env python3
"""
Curriculum Classify DOK Skill
Classifies educational content by Webb's Depth of Knowledge level
"""

import argparse
import json
import sys
from pathlib import Path
from professor.framework.dok import DOKClassifier
from professor.framework.dok.utils import format_dok_display

def main():
    parser = argparse.ArgumentParser(description='Classify content by DOK level')
    parser.add_argument('--item', help='Single item text to classify')
    parser.add_argument('--file', help='JSON file with items to classify')
    parser.add_argument('--subject', default='mathematics',
                       choices=['mathematics', 'ela', 'science', 'social-studies'])
    parser.add_argument('--grade', help='Grade level or grade band (e.g., "8" or "9-12")')
    parser.add_argument('--output', help='Output file for results (JSON)')

    args = parser.parse_args()

    # Initialize classifier
    classifier = DOKClassifier(subject=args.subject)

    # Prepare context
    context = {}
    if args.grade:
        context['grade_level'] = args.grade

    results = []

    if args.item:
        # Single item classification
        classification = classifier.classify_item(args.item, context)
        result = {
            "item_text": args.item,
            "classification": classification
        }
        results.append(result)

        # Display result
        print(f"\nItem: {args.item}\n")
        print(format_dok_display(classification))

    elif args.file:
        # Batch classification
        with open(args.file, 'r') as f:
            data = json.load(f)

        items = data.get('items', [])
        subject = data.get('subject', args.subject)

        classifier = DOKClassifier(subject=subject)

        for item in items:
            item_text = item.get('text') or item.get('item_text')
            item_id = item.get('id', '')

            classification = classifier.classify_item(item_text, context)
            result = {
                "item_id": item_id,
                "item_text": item_text,
                "classification": classification
            }
            results.append(result)

        # Calculate and display distribution
        classifications = [r['classification'] for r in results]
        distribution = classifier.calculate_distribution(classifications)

        print(f"\n📊 DOK Distribution for {len(items)} items:\n")
        print(f"DOK 1 (Recall): {distribution['dok1_count']} ({distribution['dok1_percent']}%)")
        print(f"DOK 2 (Skill/Concept): {distribution['dok2_count']} ({distribution['dok2_percent']}%)")
        print(f"DOK 3 (Strategic Thinking): {distribution['dok3_count']} ({distribution['dok3_percent']}%)")
        print(f"DOK 4 (Extended Thinking): {distribution['dok4_count']} ({distribution['dok4_percent']}%)")
        print(f"\nBalance Score: {distribution['balance_score']}/100")

        if distribution['balance_score'] < 60:
            print("\n⚠️  Warning: DOK distribution may be unbalanced")
            if distribution['dok1_percent'] > 40:
                print("   - Too many DOK 1 (Recall) items")
            if distribution['dok3_percent'] + distribution['dok4_percent'] < 20:
                print("   - Insufficient DOK 3-4 (higher-order thinking) items")

    else:
        print("Error: Must provide --item or --file", file=sys.stderr)
        sys.exit(1)

    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Results saved to {args.output}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
```

**Acceptance Criteria**:
- Skill can be invoked via `/curriculum-classify-dok`
- Classifies single items and batch files
- Displays DOK level, rationale, confidence
- Calculates distributions for batches
- Saves results to JSON

---

### 2.2 Create `curriculum-balance-dok` Skill

**File**: `.claude/skills/curriculum-balance-dok.md`

```markdown
# curriculum-balance-dok

Analyzes curriculum or assessment materials for DOK distribution and recommends adjustments to improve cognitive rigor and balance.

## Description

Reviews educational materials to ensure appropriate distribution of cognitive complexity across Webb's DOK levels. Identifies over-reliance on lower DOK levels and recommends enhancements.

Use this skill when you need to:
- Audit an assessment for DOK balance
- Ensure curriculum provides appropriate challenge
- Identify gaps in cognitive rigor
- Improve alignment with standards

## Usage

```bash
/curriculum-balance-dok --file assessment.json --grade-band "9-12"
/curriculum-balance-dok --directory curriculum/unit-3/ --subject mathematics
```

## Implementation

When invoked:

1. **Analyze Existing Classifications**
   - Load items with DOK classifications
   - Calculate current distribution

2. **Compare to Ideal Distribution**
   - Use grade-band-appropriate targets
   - Identify gaps and excesses

3. **Generate Recommendations**
   - Suggest which items to enhance
   - Provide example enhancements
   - Recommend new items to balance

4. **Output Report**
   - Current vs. ideal distribution
   - Specific action items
   - Enhanced versions of selected items

[Full implementation details omitted for brevity - follow pattern of curriculum-classify-dok]
```

**Acceptance Criteria**:
- Analyzes DOK distributions
- Compares to grade-appropriate targets
- Provides actionable recommendations
- Can enhance items to higher DOK levels

---

### 2.3 Create `curriculum-webb-alignment` Skill

**File**: `.claude/skills/curriculum-webb-alignment.md`

```markdown
# curriculum-webb-alignment

Performs a complete Webb Alignment study analyzing the alignment between standards, curriculum, and assessments across multiple dimensions including DOK.

## Description

Conducts comprehensive alignment analysis using Webb's methodology:
- **Categorical Concurrence**: Do assessments match standard content categories?
- **Depth of Knowledge**: Do assessments match standard DOK levels?
- **Range of Knowledge**: Do assessments cover breadth of standards?
- **Balance of Representation**: Are all standards adequately represented?

Use this skill for:
- Formal alignment studies
- Curriculum audits
- Standards validation
- Quality assurance

## Output

Generates alignment report with:
- Overall alignment score (0-100)
- Dimension-by-dimension analysis
- Identified gaps and misalignments
- Recommendations for improvement

[Full implementation omitted for brevity]
```

**Acceptance Criteria**:
- Performs multi-dimensional alignment analysis
- Generates formal Webb alignment reports
- Identifies specific misalignments
- Provides corrective recommendations

---

## Phase 3: Enhance Existing Assessment Skills

### 3.1 Enhance `curriculum-develop-items`

**Current File**: `.claude/skills/curriculum-develop-items.md`

**Changes Required**:

1. **Update Skill Description** - Add DOK capabilities
2. **Add DOK Parameters** - Allow specifying target DOK levels
3. **Enhance Output Format** - Include DOK classification
4. **Update Implementation** - Integrate DOK classifier

**Modified Sections**:

```markdown
## Usage

**Generate items with specific DOK levels:**
```bash
/curriculum-develop-items --objective "Solve systems of linear equations" --dok-distribution "dok1:2,dok2:5,dok3:3"
/curriculum-develop-items --blueprint blueprint.json --auto-classify-dok
```

## Output Format

```json
{
  "item_id": "Q1",
  "item_type": "constructed-response",
  "item_text": "Prove that any linear combination of solutions to a homogeneous system is also a solution.",
  "answer_key": "...",
  "rubric": {...},
  "dok_classification": {
    "dok_level": 3,
    "subject": "mathematics",
    "rationale": "Requires producing mathematical proof and generalizing beyond specific examples",
    "confidence": 0.92
  },
  "standard": "HSA-REI.C.6",
  "objective": "Solve systems of linear equations"
}
```

## Implementation

When generating items:

1. **Parse DOK Requirements**
   - Extract target DOK distribution from blueprint or parameters
   - Default distribution if not specified

2. **Generate Items**
   - For each required DOK level, craft appropriate items
   - Use DOK descriptors to guide item creation
   - Ensure items truly require the target DOK level

3. **Validate DOK Levels**
   ```python
   from professor.framework.dok import DOKClassifier

   classifier = DOKClassifier(subject="mathematics")
   classification = classifier.classify_item(item_text)

   # Verify it matches target DOK
   if classification['dok_level'] != target_dok:
       # Revise item or flag for review
   ```

4. **Include Classifications in Output**
   - Attach DOK classification to each item
   - Calculate distribution
   - Verify distribution matches blueprint
```

**File**: `professor/skills/curriculum_develop_items.py`

**Code Changes**:

```python
# Add at top of file
from professor.framework.dok import DOKClassifier

# In main generation function
def generate_items(objective, num_items, dok_distribution=None):
    """
    Generate assessment items for a learning objective

    Args:
        objective: Learning objective text
        num_items: Total number of items to generate
        dok_distribution: Dict like {"dok1": 2, "dok2": 5, "dok3": 3}
    """
    items = []
    classifier = DOKClassifier(subject="mathematics")

    # Parse DOK distribution
    if dok_distribution is None:
        # Default distribution
        dok_distribution = distribute_items_by_dok(num_items, "9-12")

    # Generate items for each DOK level
    for dok_level, count in dok_distribution.items():
        level_num = int(dok_level.replace("dok", ""))

        for i in range(count):
            # Generate item targeting this DOK level
            item = generate_item_at_dok_level(objective, level_num)

            # Validate DOK classification
            classification = classifier.classify_item(item['item_text'])
            item['dok_classification'] = classification

            # Verify it matches target
            if classification['dok_level'] != level_num:
                # Log warning or regenerate
                print(f"Warning: Generated item classified as DOK {classification['dok_level']}, "
                      f"but target was DOK {level_num}")

            items.append(item)

    return items

def generate_item_at_dok_level(objective, dok_level):
    """Generate an item targeting a specific DOK level"""
    # Use DOK descriptors to guide item creation
    # This is where LLM generation would occur, guided by DOK framework

    # For DOK 1: Simple, direct application
    if dok_level == 1:
        item_text = f"[Generate straightforward problem for: {objective}]"

    # For DOK 2: Requires explanation or interpretation
    elif dok_level == 2:
        item_text = f"[Generate problem requiring explanation for: {objective}]"

    # For DOK 3: Requires proof, justification, or novel solution
    elif dok_level == 3:
        item_text = f"[Generate problem requiring proof/justification for: {objective}]"

    # For DOK 4: Extended project or research
    elif dok_level == 4:
        item_text = f"[Generate multi-day project for: {objective}]"

    return {
        "item_text": item_text,
        "target_dok": dok_level
        # ... other fields
    }
```

**Acceptance Criteria**:
- Skill accepts DOK distribution parameters
- Generated items tagged with DOK classifications
- Validation ensures items match target DOK
- Output includes DOK metadata

---

### 3.2 Enhance `curriculum-assess-design`

**Current File**: `.claude/skills/curriculum-assess-design.md`

**Changes Required**:

1. **Add DOK to Assessment Blueprints**
2. **Specify DOK Distribution Requirements**
3. **Validate DOK-Standard Alignment**

**Modified Blueprint Format**:

```json
{
  "assessment_title": "Algebra 1 Unit 3: Linear Functions",
  "standards": [
    {
      "standard_id": "HSF-IF.B.4",
      "standard_text": "For a function that models a relationship, interpret key features",
      "dok_level": 2,
      "num_items": 4,
      "item_types": ["multiple-choice", "constructed-response"]
    },
    {
      "standard_id": "HSF-IF.C.7",
      "standard_text": "Graph functions and show key features",
      "dok_level": 2,
      "num_items": 3
    },
    {
      "standard_id": "HSF-LE.A.2",
      "standard_text": "Construct linear and exponential functions",
      "dok_level": 3,
      "num_items": 2
    }
  ],
  "dok_distribution": {
    "dok1_target": 2,
    "dok2_target": 7,
    "dok3_target": 4,
    "dok4_target": 0,
    "total_items": 13,
    "rationale": "Grade 9-12 balanced distribution emphasizing DOK 2-3"
  },
  "grade_level": "9",
  "subject": "mathematics"
}
```

**Acceptance Criteria**:
- Blueprints include DOK specifications
- DOK aligned with standards
- Distribution validated against grade-band norms

---

## Phase 4: Enhance Curriculum Design Skills

### 4.1 Enhance `curriculum-design` (Learning Objectives)

**Changes Required**:

1. **Tag objectives with expected DOK levels**
2. **Ensure progression within units (DOK 1 → 2 → 3 → 4)**
3. **Validate Bloom's-DOK alignment**

**Enhanced Objective Format**:

```json
{
  "objective_id": "LO-3.2",
  "objective_text": "Students will solve systems of two linear equations algebraically and justify which method is most efficient for different equation types",
  "blooms_level": "Analyze",
  "dok_level": 3,
  "dok_rationale": "Requires both solving (DOK 2) and justifying method selection (DOK 3)",
  "standard": "HSA-REI.C.6",
  "prerequisites": ["LO-3.1"],
  "assessment_types": ["constructed-response", "performance-task"]
}
```

**Acceptance Criteria**:
- All objectives tagged with DOK
- DOK progression validated
- Blooms-DOK alignment checked

---

### 4.2 Enhance `curriculum-develop-content`

**Changes Required**:

1. **Tag activities with DOK levels**
2. **Scaffold from lower to higher DOK**
3. **Provide DOK 3-4 extensions**

**Enhanced Lesson Plan Format**:

```markdown
## Lesson 3.2: Solving Systems of Linear Equations

### Learning Objectives
- Solve systems using substitution and elimination (DOK 2)
- Justify method selection based on equation structure (DOK 3)

### Activities

#### Activity 1: Direct Practice (DOK 1)
Time: 15 minutes
Students practice solving systems using provided procedures...

#### Activity 2: Method Comparison (DOK 2)
Time: 20 minutes
Students solve same system using both methods and explain which was easier...

#### Activity 3: Strategic Selection (DOK 3)
Time: 25 minutes
Students analyze 10 different systems, predict most efficient method, solve, and justify...

#### Extension: Create Your Own (DOK 4 - Optional)
Students design a real-world scenario that requires solving a system, create the model, solve, and verify solution makes sense in context...
```

**Acceptance Criteria**:
- Lessons include activities at multiple DOK levels
- Clear DOK progression
- Extensions available for high-DOK work

---

## Phase 5: Enhance Review & Quality Assurance Skills

### 5.1 Enhance `curriculum-review-pedagogy`

**Changes Required**:

1. **Add DOK alignment validation**
2. **Check constructive alignment across DOK levels**
3. **Flag DOK mismatches**

**New Validation Checks**:

```python
def review_pedagogy(materials):
    """Enhanced pedagogical review with DOK validation"""

    issues = []

    # Extract DOK levels
    objective_dok = materials['objective']['dok_level']
    instruction_dok = max(activity['dok_level'] for activity in materials['activities'])
    assessment_dok = max(item['dok_classification']['dok_level']
                         for item in materials['assessment_items'])
    standard_dok = materials['standard']['dok_level']

    # Validate alignment
    from professor.framework.dok.utils import analyze_dok_alignment

    alignment = analyze_dok_alignment(standard_dok, objective_dok, assessment_dok)

    if not alignment['aligned']:
        for issue in alignment['issues']:
            issues.append({
                "severity": "high",
                "category": "dok_alignment",
                "message": issue
            })

    # Check if instruction prepares for assessment DOK
    if instruction_dok < assessment_dok - 1:
        issues.append({
            "severity": "high",
            "category": "dok_alignment",
            "message": f"Instruction activities (max DOK {instruction_dok}) don't prepare "
                      f"students for assessment (DOK {assessment_dok})"
        })

    # Check DOK distribution in assessment
    if len(materials['assessment_items']) > 5:
        from professor.framework.dok import DOKClassifier
        classifier = DOKClassifier()
        classifications = [item['dok_classification'] for item in materials['assessment_items']]
        distribution = classifier.calculate_distribution(classifications)

        if distribution['balance_score'] < 60:
            issues.append({
                "severity": "medium",
                "category": "dok_balance",
                "message": f"DOK distribution unbalanced (score: {distribution['balance_score']}/100). "
                          f"Current: DOK1={distribution['dok1_percent']}%, "
                          f"DOK2={distribution['dok2_percent']}%, "
                          f"DOK3={distribution['dok3_percent']}%"
            })

    return issues
```

**Acceptance Criteria**:
- Reviews check DOK alignment
- Identifies DOK mismatches
- Flags unbalanced distributions
- Provides specific corrective actions

---

### 5.2 Enhance `curriculum-review-accessibility`

**Changes Required**:

1. **Validate DOK levels don't confound with accessibility barriers**
2. **Ensure high DOK available to all learners via UDL**

**Note**: DOK represents cognitive complexity, not difficulty. Ensure high-DOK tasks are accessible through:
- Multiple means of representation
- Multiple means of action/expression
- Appropriate scaffolding

**Acceptance Criteria**:
- Checks that DOK 3-4 tasks have accessibility supports
- UDL strategies don't lower DOK
- Accommodations preserve DOK level

---

## Phase 6: Enhance Analytics & Reporting

### 6.1 Enhance `curriculum-analyze-outcomes`

**Changes Required**:

1. **Disaggregate performance by DOK level**
2. **Identify DOK-specific achievement gaps**
3. **Generate targeted interventions**

**Enhanced Analytics Output**:

```json
{
  "overall_mastery": 0.72,
  "dok_analysis": {
    "dok1": {
      "mastery_rate": 0.85,
      "num_items": 5,
      "avg_score": 0.85,
      "status": "proficient"
    },
    "dok2": {
      "mastery_rate": 0.73,
      "num_items": 12,
      "avg_score": 0.73,
      "status": "approaching_proficient"
    },
    "dok3": {
      "mastery_rate": 0.45,
      "num_items": 8,
      "avg_score": 0.45,
      "status": "needs_improvement"
    },
    "dok4": {
      "mastery_rate": null,
      "num_items": 0,
      "avg_score": null,
      "status": "not_assessed"
    }
  },
  "achievement_gaps": [
    {
      "gap_type": "dok_progression",
      "description": "Students perform well on DOK 1-2 but struggle with DOK 3",
      "magnitude": "large",
      "affected_percentage": 0.68
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Increase instructional time on DOK 3 reasoning and justification tasks",
      "rationale": "Only 45% mastery on DOK 3 compared to 85% on DOK 1",
      "specific_actions": [
        "Model mathematical argumentation",
        "Provide scaffolded proof activities",
        "Use think-alouds for problem-solving strategies"
      ]
    },
    {
      "priority": "medium",
      "recommendation": "Include DOK 4 extended thinking opportunities",
      "rationale": "No DOK 4 items in current assessment; students need practice with sustained reasoning",
      "specific_actions": [
        "Design multi-day project",
        "Assign research investigation",
        "Create performance assessment"
      ]
    }
  ]
}
```

**Implementation**:

```python
def analyze_outcomes_by_dok(assessment_results):
    """Analyze student performance disaggregated by DOK level"""

    dok_performance = {1: [], 2: [], 3: [], 4: []}

    for student in assessment_results['students']:
        for response in student['responses']:
            item = response['item']
            dok_level = item['dok_classification']['dok_level']
            score = response['score'] / item['max_points']  # Normalize to 0-1

            dok_performance[dok_level].append(score)

    # Calculate statistics per DOK level
    analysis = {}
    for dok_level in [1, 2, 3, 4]:
        scores = dok_performance[dok_level]

        if scores:
            avg_score = sum(scores) / len(scores)
            mastery_rate = sum(1 for s in scores if s >= 0.7) / len(scores)

            analysis[f"dok{dok_level}"] = {
                "mastery_rate": round(mastery_rate, 2),
                "num_items": len(set(r['item']['item_id']
                                     for s in assessment_results['students']
                                     for r in s['responses']
                                     if r['item']['dok_classification']['dok_level'] == dok_level)),
                "avg_score": round(avg_score, 2),
                "status": get_status(mastery_rate)
            }
        else:
            analysis[f"dok{dok_level}"] = {
                "mastery_rate": None,
                "num_items": 0,
                "avg_score": None,
                "status": "not_assessed"
            }

    # Identify gaps and generate recommendations
    gaps = identify_dok_gaps(analysis)
    recommendations = generate_dok_recommendations(gaps, analysis)

    return {
        "dok_analysis": analysis,
        "achievement_gaps": gaps,
        "recommendations": recommendations
    }
```

**Acceptance Criteria**:
- Performance disaggregated by DOK
- Gaps identified with magnitude
- Specific recommendations generated
- Reports include visualizations

---

### 6.2 Create DOK Reporting Templates

**File**: `professor/framework/dok/reports/dok-analysis-template.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>DOK Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .dok-level { margin: 20px 0; padding: 15px; border-left: 4px solid #ccc; }
        .dok1 { border-color: #4CAF50; }
        .dok2 { border-color: #2196F3; }
        .dok3 { border-color: #FF9800; }
        .dok4 { border-color: #F44336; }
        .status-proficient { color: #4CAF50; font-weight: bold; }
        .status-approaching { color: #FF9800; font-weight: bold; }
        .status-needs-improvement { color: #F44336; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Depth of Knowledge Analysis Report</h1>
    <p><strong>Assessment:</strong> {{assessment_title}}</p>
    <p><strong>Date:</strong> {{analysis_date}}</p>
    <p><strong>Students:</strong> {{num_students}}</p>

    <h2>Performance by DOK Level</h2>

    <table>
        <tr>
            <th>DOK Level</th>
            <th>Description</th>
            <th>Items</th>
            <th>Mastery Rate</th>
            <th>Avg Score</th>
            <th>Status</th>
        </tr>
        {{#each dok_levels}}
        <tr>
            <td>DOK {{level}}</td>
            <td>{{name}}</td>
            <td>{{num_items}}</td>
            <td>{{mastery_rate}}%</td>
            <td>{{avg_score}}%</td>
            <td class="status-{{status}}">{{status_display}}</td>
        </tr>
        {{/each}}
    </table>

    <h2>Achievement Gaps</h2>
    {{#each gaps}}
    <div class="gap">
        <h3>{{description}}</h3>
        <p><strong>Magnitude:</strong> {{magnitude}}</p>
        <p><strong>Affected Students:</strong> {{affected_percentage}}%</p>
    </div>
    {{/each}}

    <h2>Recommendations</h2>
    {{#each recommendations}}
    <div class="recommendation">
        <h3>[{{priority}}] {{recommendation}}</h3>
        <p>{{rationale}}</p>
        <h4>Specific Actions:</h4>
        <ul>
            {{#each specific_actions}}
            <li>{{this}}</li>
            {{/each}}
        </ul>
    </div>
    {{/each}}
</body>
</html>
```

**Acceptance Criteria**:
- Professional HTML reports generated
- Includes charts/visualizations
- Exportable to PDF
- Shareable with stakeholders

---

## Phase 7: Update Agent Orchestration

### 7.1 Enhance Agent Decision Logic

**File**: `professor/agents/assessment-designer/agent.py`

**Changes**:

```python
class AssessmentDesignerAgent:
    """Agent that orchestrates assessment design with DOK awareness"""

    def design_assessment(self, standards, grade_level, num_items):
        """Design assessment with DOK distribution"""

        # 1. Analyze standards for DOK levels
        standard_doks = []
        for standard in standards:
            if 'dok_level' not in standard:
                # Classify standard if DOK not specified
                classifier = DOKClassifier()
                classification = classifier.classify_item(standard['text'])
                standard['dok_level'] = classification['dok_level']
            standard_doks.append(standard['dok_level'])

        # 2. Determine target DOK distribution
        from professor.framework.dok.utils import recommend_dok_distribution
        recommended_dist = recommend_dok_distribution(num_items, grade_level)

        # But also respect standard DOK levels
        # If standards are mostly DOK 2-3, don't force DOK 1 items
        adjusted_dist = self._adjust_distribution_for_standards(
            recommended_dist,
            standard_doks
        )

        # 3. Create assessment blueprint with DOK specifications
        blueprint = self._create_blueprint(standards, adjusted_dist)

        # 4. Generate items using curriculum-develop-items skill
        items = self._generate_items(blueprint)

        # 5. Validate DOK distribution
        classifier = DOKClassifier()
        actual_dist = classifier.calculate_distribution(
            [item['dok_classification'] for item in items]
        )

        # 6. If distribution doesn't match, regenerate specific items
        if actual_dist['balance_score'] < 70:
            items = self._rebalance_items(items, adjusted_dist)

        return {
            "blueprint": blueprint,
            "items": items,
            "dok_distribution": actual_dist
        }
```

**Acceptance Criteria**:
- Agents automatically consider DOK
- Distributions aligned with standards and grade level
- Validation ensures quality
- Agents can rebalance if needed

---

### 7.2 Update Agent Prompts

**File**: `professor/agents/curriculum-architect/prompt.md`

**Add Section**:

```markdown
## DOK Considerations

When designing curriculum:

1. **Identify Expected DOK Levels**
   - Review standards for specified DOK levels
   - If not specified, classify standards using DOK framework

2. **Plan DOK Progression**
   - Unit should build from lower to higher DOK
   - Early lessons: DOK 1-2 (building foundation)
   - Middle lessons: DOK 2-3 (developing understanding)
   - Culminating tasks: DOK 3-4 (applying and extending)

3. **Ensure DOK Alignment**
   - Learning objectives → Instruction → Assessment must align on DOK
   - If standard is DOK 3, ensure assessment includes DOK 3 items
   - Ensure instruction prepares students for assessment DOK level

4. **Balance Rigor**
   - Don't over-rely on DOK 1 (recall) tasks
   - Provide opportunities for DOK 3-4 (strategic/extended thinking)
   - Ensure all students have access to high-DOK tasks (via UDL)
```

**Acceptance Criteria**:
- All agents have DOK guidance
- Prompts reference DOK framework
- Agents make DOK-aware decisions

---

## Phase 8: Documentation & Examples

### 8.1 Create DOK Integration Guide

**File**: `docs/dok-framework-guide.md`

```markdown
# Webb's Depth of Knowledge (DOK) Framework Integration Guide

## Overview

This guide explains how the Professor framework integrates Webb's Depth of Knowledge (DOK) to ensure appropriate cognitive rigor in curriculum and assessment materials.

## What is DOK?

Webb's Depth of Knowledge is a framework for categorizing educational tasks by the complexity of thinking required:

- **DOK 1 (Recall)**: Memorized facts, well-known procedures
- **DOK 2 (Skill/Concept)**: Conceptual understanding, decision-making
- **DOK 3 (Strategic Thinking)**: Reasoning, proofs, novel solutions
- **DOK 4 (Extended Thinking)**: Multi-day projects, research

**Important**: DOK is about complexity, not difficulty. A DOK 1 calculus problem is difficult but not complex.

## Using DOK in Professor

### Classifying Content

```bash
# Classify a single item
/curriculum-classify-dok --item "Prove that √2 is irrational"

# Classify batch of items
/curriculum-classify-dok --file assessment-items.json --subject mathematics
```

### Generating DOK-Tagged Items

```bash
# Specify DOK distribution
/curriculum-develop-items --objective "Solve quadratic equations" --dok-distribution "dok1:2,dok2:5,dok3:3"
```

### Checking DOK Balance

```bash
# Analyze existing assessment
/curriculum-balance-dok --file unit-test.json --grade-band "9-12"
```

### Reviewing DOK Alignment

```bash
# Check alignment between standards, objectives, and assessment
/curriculum-review-pedagogy --materials unit3/
```

## Best Practices

### 1. Know Your Standards' DOK Levels

Many state standards specify expected DOK levels. Always check.

### 2. Align Across the System

If a standard is DOK 3, ensure:
- Objective targets DOK 3
- Instruction includes DOK 3 activities
- Assessment includes DOK 3 items

### 3. Don't Over-Test DOK 1

Aim for 20-30% DOK 1, 40-50% DOK 2, 20-30% DOK 3, 5-10% DOK 4

### 4. Make High DOK Accessible

Use UDL strategies to ensure all students can access DOK 3-4 tasks

### 5. Consider Grade Level

Same task may be different DOK at different grades based on typical prior knowledge

## Examples by Subject

### Mathematics

| Task | DOK | Rationale |
|------|-----|-----------|
| What is 7 × 8? | 1 | Recall of memorized fact |
| Solve for x: 2x + 5 = 13 | 1 | Well-known procedure |
| Explain why (a+b)² ≠ a² + b² | 2 | Requires conceptual understanding |
| Which measure of central tendency best represents this skewed data? Explain. | 2 | Interpretation in context |
| Prove that the sum of two even numbers is always even | 3 | Requires mathematical proof |
| Design a fair probability game using two dice | 3 | Novel solution, verification required |
| Conduct month-long study of traffic patterns and create mathematical model | 4 | Extended project with research |

[Additional examples for ELA, Science, Social Studies when those descriptors are added]

## Troubleshooting

### "My DOK 3 item was classified as DOK 2"

Check if the item truly requires reasoning or if it can be solved with a learned procedure. If genuinely DOK 3, you can manually override.

### "My assessment has low balance score"

Use `/curriculum-balance-dok` to get specific recommendations for which items to enhance or add.

### "Automated classification confidence is low (<0.6)"

Flag item for human review. Edge cases may need expert judgment.

## References

- Webb, N. L. (2002). Depth-of-Knowledge Levels for Four Content Areas
- Webb Alignment Tool: https://www.wcer.wisc.edu/WAT/
```

**Acceptance Criteria**:
- Comprehensive guide created
- Examples for all DOK levels
- Troubleshooting section
- Best practices documented

---

### 8.2 Create Example Workflows

**File**: `examples/dok-workflows/example-1-classify-assessment.md`

```markdown
# Example Workflow: Classifying an Existing Assessment

## Scenario

You have an existing algebra assessment with 20 items and want to verify appropriate DOK distribution.

## Steps

1. **Prepare Items File**

Create `algebra-test.json`:
```json
{
  "assessment_title": "Algebra 1 Unit 3 Test",
  "subject": "mathematics",
  "grade_level": "9",
  "items": [
    {"id": "Q1", "text": "Simplify: 3x + 5x"},
    {"id": "Q2", "text": "Solve for x: 2x - 7 = 15"},
    {"id": "Q3", "text": "Explain why the slope of a vertical line is undefined"},
    // ... 17 more items
  ]
}
```

2. **Classify All Items**

```bash
/curriculum-classify-dok --file algebra-test.json --output algebra-test-classified.json
```

**Output:**
```
📊 DOK Distribution for 20 items:

DOK 1 (Recall): 8 (40%)
DOK 2 (Skill/Concept): 9 (45%)
DOK 3 (Strategic Thinking): 3 (15%)
DOK 4 (Extended Thinking): 0 (0%)

Balance Score: 72/100
```

3. **Analyze Balance**

```bash
/curriculum-balance-dok --file algebra-test-classified.json --grade-band "9-12"
```

**Output:**
```
⚠️ DOK Distribution Analysis

Current vs. Recommended (Grade 9-12):
- DOK 1: 40% (current) vs 20% (recommended) - TOO HIGH
- DOK 2: 45% (current) vs 40% (recommended) - GOOD
- DOK 3: 15% (current) vs 30% (recommended) - TOO LOW
- DOK 4: 0% (current) vs 10% (recommended) - MISSING

Recommendations:
1. Replace 4 DOK 1 items with DOK 3 items
2. Add 2 DOK 4 items (or replace 2 DOK 1 items)

Suggested Items to Enhance:
- Q1 "Simplify: 3x + 5x" → Enhance to "Explain why 3x + 5x = 8x but 3x + 5y cannot be simplified"
- Q2 "Solve for x: 2x - 7 = 15" → Enhance to "Create a real-world problem that would be modeled by 2x - 7 = 15, then solve and verify"
```

4. **Implement Recommendations**

Revise items based on recommendations and re-classify to verify.

## Expected Outcome

- Balanced DOK distribution appropriate for grade 9-12
- Mix of recall, conceptual understanding, and strategic thinking
- At least one extended thinking opportunity
```

**Additional Example Files**:
- `example-2-design-dok-aligned-assessment.md`
- `example-3-analyze-outcomes-by-dok.md`
- `example-4-webb-alignment-study.md`

**Acceptance Criteria**:
- 4+ complete workflow examples
- Real data files included
- Step-by-step instructions
- Expected outputs shown

---

## Phase 9: Testing & Validation

### 9.1 Unit Tests

**File**: `professor/framework/dok/tests/test_classifier.py`

```python
"""Unit tests for DOK Classifier"""

import unittest
from professor.framework.dok import DOKClassifier

class TestDOKClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = DOKClassifier(subject="mathematics")

    def test_dok1_simple_recall(self):
        """Test DOK 1 classification for simple recall"""
        item = "What is 7 × 8?"
        result = self.classifier.classify_item(item)
        self.assertEqual(result['dok_level'], 1)
        self.assertGreater(result['confidence'], 0.7)

    def test_dok1_formula_application(self):
        """Test DOK 1 for direct formula application"""
        item = "Find the area of a circle with radius 5 cm. Use π ≈ 3.14"
        result = self.classifier.classify_item(item)
        self.assertEqual(result['dok_level'], 1)

    def test_dok2_explanation(self):
        """Test DOK 2 for explanation requirement"""
        item = "Explain why multiplying two negative numbers gives a positive result"
        result = self.classifier.classify_item(item)
        self.assertEqual(result['dok_level'], 2)

    def test_dok2_interpretation(self):
        """Test DOK 2 for interpretation in context"""
        item = "The graph shows temperature over 24 hours. During which period did temperature increase most rapidly? Explain."
        result = self.classifier.classify_item(item)
        self.assertEqual(result['dok_level'], 2)

    def test_dok3_proof(self):
        """Test DOK 3 for proof requirement"""
        item = "Prove that the sum of two even numbers is always even"
        result = self.classifier.classify_item(item)
        self.assertEqual(result['dok_level'], 3)
        self.assertIn("proof", result['rationale'].lower())

    def test_dok3_novel_solution(self):
        """Test DOK 3 for novel solution"""
        item = "Design a fair game using two dice where Player A wins if sum is even, Player B wins if sum is odd"
        result = self.classifier.classify_item(item)
        self.assertIn(result['dok_level'], [2, 3])  # Could be 2 or 3 depending on sophistication

    def test_dok4_extended_project(self):
        """Test DOK 4 for extended thinking"""
        item = "Over the next month, collect data on traffic patterns at your school. Create a mathematical model and propose schedule changes to reduce congestion."
        result = self.classifier.classify_item(item)
        self.assertEqual(result['dok_level'], 4)

    def test_batch_classification(self):
        """Test batch classification"""
        items = [
            "What is 5 + 3?",
            "Explain why 5 + 3 = 3 + 5",
            "Prove that addition is commutative for all real numbers"
        ]
        results = self.classifier.classify_batch(items)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['dok_level'], 1)
        self.assertEqual(results[1]['dok_level'], 2)
        self.assertEqual(results[2]['dok_level'], 3)

    def test_distribution_calculation(self):
        """Test DOK distribution calculation"""
        classifications = [
            {'dok_level': 1}, {'dok_level': 1},
            {'dok_level': 2}, {'dok_level': 2}, {'dok_level': 2},
            {'dok_level': 3}
        ]
        dist = self.classifier.calculate_distribution(classifications)
        self.assertEqual(dist['dok1_count'], 2)
        self.assertEqual(dist['dok2_count'], 3)
        self.assertEqual(dist['dok3_count'], 1)
        self.assertEqual(dist['total_items'], 6)
        self.assertAlmostEqual(dist['dok1_percent'], 33.3, places=1)

if __name__ == '__main__':
    unittest.main()
```

**File**: `professor/framework/dok/tests/test_utils.py`

```python
"""Unit tests for DOK utilities"""

import unittest
from professor.framework.dok.utils import (
    validate_dok_classification,
    analyze_dok_alignment,
    recommend_dok_distribution
)

class TestDOKUtils(unittest.TestCase):

    def test_validate_classification_valid(self):
        """Test validation with valid classification"""
        classification = {
            "dok_level": 2,
            "subject": "mathematics",
            "rationale": "Requires conceptual understanding"
        }
        self.assertTrue(validate_dok_classification(classification))

    def test_validate_classification_invalid_level(self):
        """Test validation rejects invalid DOK level"""
        classification = {
            "dok_level": 5,  # Invalid
            "subject": "mathematics",
            "rationale": "Test"
        }
        self.assertFalse(validate_dok_classification(classification))

    def test_alignment_perfect(self):
        """Test alignment analysis with perfect alignment"""
        result = analyze_dok_alignment(
            standard_dok=2,
            objective_dok=2,
            assessment_dok=2
        )
        self.assertTrue(result['aligned'])
        self.assertEqual(len(result['issues']), 0)

    def test_alignment_assessment_too_easy(self):
        """Test alignment catches assessment easier than objective"""
        result = analyze_dok_alignment(
            standard_dok=3,
            objective_dok=3,
            assessment_dok=1
        )
        self.assertFalse(result['aligned'])
        self.assertGreater(len(result['issues']), 0)

    def test_alignment_objective_too_low(self):
        """Test alignment catches objective not supporting assessment"""
        result = analyze_dok_alignment(
            standard_dok=3,
            objective_dok=1,
            assessment_dok=3
        )
        self.assertFalse(result['aligned'])
        self.assertTrue(any('not prepared' in issue.lower() for issue in result['issues']))

    def test_recommend_distribution_high_school(self):
        """Test DOK distribution recommendations for high school"""
        rec = recommend_dok_distribution(num_items=20, grade_band="9-12")
        self.assertEqual(rec['total_items'], 20)
        # Should recommend ~20% DOK1, 40% DOK2, 30% DOK3, 10% DOK4
        self.assertAlmostEqual(rec['dok1_recommended'], 4, delta=1)
        self.assertAlmostEqual(rec['dok2_recommended'], 8, delta=1)
        self.assertAlmostEqual(rec['dok3_recommended'], 6, delta=1)
        self.assertAlmostEqual(rec['dok4_recommended'], 2, delta=1)

    def test_recommend_distribution_elementary(self):
        """Test DOK distribution for elementary"""
        rec = recommend_dok_distribution(num_items=20, grade_band="K-5")
        # Elementary should have more DOK 1-2, less DOK 3-4
        self.assertGreater(rec['dok1_recommended'], 4)
        self.assertLess(rec['dok4_recommended'], 2)

if __name__ == '__main__':
    unittest.main()
```

**Acceptance Criteria**:
- All unit tests pass
- Coverage > 80%
- Edge cases tested
- Integration tests included

---

### 9.2 Integration Tests

**File**: `professor/tests/integration/test_dok_workflow.py`

```python
"""Integration tests for end-to-end DOK workflows"""

import unittest
import json
from professor.framework.dok import DOKClassifier
from professor.skills.curriculum_develop_items import generate_items
from professor.skills.curriculum_review_pedagogy import review_pedagogy

class TestDOKWorkflow(unittest.TestCase):

    def test_generate_and_classify_items(self):
        """Test generating items with DOK requirements and validating"""

        # Generate items with specific DOK distribution
        objective = "Solve systems of linear equations"
        dok_dist = {"dok1": 2, "dok2": 3, "dok3": 2}

        items = generate_items(objective, sum(dok_dist.values()), dok_dist)

        # Verify all items have DOK classifications
        for item in items:
            self.assertIn('dok_classification', item)
            self.assertIn('dok_level', item['dok_classification'])

        # Verify distribution matches request
        classifier = DOKClassifier()
        actual_dist = classifier.calculate_distribution(
            [item['dok_classification'] for item in items]
        )

        self.assertEqual(actual_dist['dok1_count'], dok_dist['dok1'])
        self.assertEqual(actual_dist['dok2_count'], dok_dist['dok2'])
        self.assertEqual(actual_dist['dok3_count'], dok_dist['dok3'])

    def test_pedagogical_review_detects_misalignment(self):
        """Test that pedagogical review catches DOK misalignment"""

        # Create materials with misaligned DOK
        materials = {
            "standard": {"text": "Construct proofs", "dok_level": 3},
            "objective": {"text": "Students will recall definitions", "dok_level": 1},
            "activities": [{"text": "Memorize definitions", "dok_level": 1}],
            "assessment_items": [
                {"text": "What is the definition of congruent?",
                 "dok_classification": {"dok_level": 1}}
            ]
        }

        issues = review_pedagogy(materials)

        # Should flag that assessment doesn't match standard
        self.assertGreater(len(issues), 0)
        self.assertTrue(any('alignment' in issue['category'].lower() for issue in issues))

    def test_full_curriculum_development_with_dok(self):
        """Test complete curriculum development workflow with DOK"""

        # 1. Design learning objectives with DOK
        # 2. Create lesson plans with DOK-scaffolded activities
        # 3. Generate assessment with appropriate DOK distribution
        # 4. Review for DOK alignment
        # 5. Validate all pieces align

        # [Full workflow test - implementation details omitted for brevity]
        pass

if __name__ == '__main__':
    unittest.main()
```

**Acceptance Criteria**:
- End-to-end workflows tested
- Integration between skills validated
- Real-world scenarios covered

---

### 9.3 Validation with Real Content

**File**: `professor/tests/validation/validate-with-real-assessments.py`

```python
"""
Validate DOK classifier against real assessment items with known DOK levels
Uses items from state assessments, SBAC, PARCC, etc. with published DOK levels
"""

import json
import unittest
from professor.framework.dok import DOKClassifier

class TestDOKValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load real assessment items with known DOK levels"""
        with open('professor/tests/validation/sbac-math-items.json', 'r') as f:
            cls.sbac_items = json.load(f)

        cls.classifier = DOKClassifier(subject="mathematics")

    def test_accuracy_on_known_items(self):
        """Test classifier accuracy on items with known DOK levels"""

        correct = 0
        within_one = 0
        total = len(self.sbac_items)

        for item in self.sbac_items:
            actual_dok = item['published_dok_level']
            classification = self.classifier.classify_item(item['text'])
            predicted_dok = classification['dok_level']

            if predicted_dok == actual_dok:
                correct += 1
                within_one += 1
            elif abs(predicted_dok - actual_dok) == 1:
                within_one += 1

        accuracy = correct / total
        within_one_accuracy = within_one / total

        print(f"\nDOK Classifier Validation Results:")
        print(f"Exact match accuracy: {accuracy*100:.1f}%")
        print(f"Within-one accuracy: {within_one_accuracy*100:.1f}%")

        # Should achieve at least 60% exact match, 85% within one level
        self.assertGreater(accuracy, 0.60,
                          "Classifier should achieve >60% exact match accuracy")
        self.assertGreater(within_one_accuracy, 0.85,
                          "Classifier should achieve >85% within-one accuracy")

if __name__ == '__main__':
    unittest.main()
```

**Data File**: `professor/tests/validation/sbac-math-items.json`

```json
{
  "items": [
    {
      "id": "SBAC-MA-G8-01",
      "text": "What is the slope of the line passing through (2, 3) and (5, 9)?",
      "published_dok_level": 1,
      "source": "SBAC Grade 8 Practice Test",
      "rationale": "Direct application of slope formula"
    },
    {
      "id": "SBAC-MA-G8-02",
      "text": "Compare the rates of change of the two functions shown. Explain which function is growing faster.",
      "published_dok_level": 2,
      "source": "SBAC Grade 8 Practice Test",
      "rationale": "Requires interpretation and comparison"
    },
    {
      "id": "SBAC-MA-HS-01",
      "text": "Prove algebraically that the sum of two consecutive integers is always odd.",
      "published_dok_level": 3,
      "source": "SBAC High School Practice Test",
      "rationale": "Requires proof and generalization"
    }
    // ... more items with known DOK levels from published sources
  ]
}
```

**Acceptance Criteria**:
- Validated against 50+ real items
- Achieves >60% exact match accuracy
- Achieves >85% within-one-level accuracy
- Documents any systematic misclassifications

---

## Phase 10: Deployment & Rollout (Bonus)

### 10.1 Update CLAUDE.md

**File**: `/Users/colossus/development/content/content/CLAUDE.md`

**Add Section**:

```markdown
## Depth of Knowledge (DOK) Integration

The Professor framework includes comprehensive Webb's Depth of Knowledge support for ensuring appropriate cognitive rigor in all educational materials.

### DOK Levels

All content is classified by cognitive complexity:
- **DOK 1 (Recall)**: Memorized facts, simple procedures
- **DOK 2 (Skill/Concept)**: Conceptual understanding, interpretation
- **DOK 3 (Strategic Thinking)**: Reasoning, proofs, novel solutions
- **DOK 4 (Extended Thinking)**: Multi-day projects, research

### DOK-Enhanced Skills

The following skills now include DOK capabilities:

**Assessment Development:**
- `/curriculum-develop-items` - Generate items with specified DOK levels
- `/curriculum-assess-design` - Create blueprints with DOK distributions
- `/curriculum-classify-dok` - Classify existing items by DOK level
- `/curriculum-balance-dok` - Analyze and improve DOK balance

**Quality Assurance:**
- `/curriculum-review-pedagogy` - Validate DOK alignment
- `/curriculum-webb-alignment` - Formal Webb alignment studies

**Analytics:**
- `/curriculum-analyze-outcomes` - Performance data by DOK level

### Automatic DOK Features

When you use Professor skills, DOK is applied automatically:

✅ **Assessment items are auto-tagged with DOK levels**
✅ **Review skills validate DOK alignment**
✅ **Analytics disaggregate by DOK level**
✅ **Agents ensure DOK-appropriate rigor**

### Best Practices

1. **Always specify DOK in blueprints** - Don't rely only on defaults
2. **Validate alignment** - Standard DOK = Objective DOK = Assessment DOK
3. **Balance distributions** - Avoid over-reliance on DOK 1 recall
4. **Make high DOK accessible** - Use UDL for all students to access DOK 3-4

### Quick Reference

| Need | Command |
|------|---------|
| Tag items with DOK | `/curriculum-classify-dok --file items.json` |
| Check DOK balance | `/curriculum-balance-dok --file assessment.json` |
| Generate DOK-specific items | `/curriculum-develop-items --dok-distribution "dok1:2,dok2:5,dok3:3"` |
| Validate alignment | `/curriculum-review-pedagogy --materials unit/` |

See `docs/dok-framework-guide.md` for comprehensive DOK documentation.
```

**Acceptance Criteria**:
- CLAUDE.md updated with DOK information
- Quick reference included
- Best practices documented

---

## Summary Checklist

Use this checklist to verify all phases completed:

### Phase 1: Foundation ✅
- [ ] DOK schema created (`schema.json`)
- [ ] Mathematics descriptors complete (`descriptors/mathematics.json`)
- [ ] Classifier implemented (`classifier.py`)
- [ ] Utilities created (`utils.py`)
- [ ] Unit tests pass

### Phase 2: New Skills ✅
- [ ] `curriculum-classify-dok` skill created and tested
- [ ] `curriculum-balance-dok` skill created and tested
- [ ] `curriculum-webb-alignment` skill created and tested

### Phase 3: Enhanced Assessment Skills ✅
- [ ] `curriculum-develop-items` enhanced with DOK
- [ ] `curriculum-assess-design` enhanced with DOK
- [ ] Output formats include DOK metadata

### Phase 4: Enhanced Curriculum Skills ✅
- [ ] `curriculum-design` tags objectives with DOK
- [ ] `curriculum-develop-content` scaffolds by DOK

### Phase 5: Enhanced Review Skills ✅
- [ ] `curriculum-review-pedagogy` validates DOK alignment
- [ ] `curriculum-review-accessibility` ensures UDL for high DOK

### Phase 6: Enhanced Analytics ✅
- [ ] `curriculum-analyze-outcomes` disaggregates by DOK
- [ ] Reporting templates created
- [ ] Visualization support added

### Phase 7: Agent Orchestration ✅
- [ ] Agent logic updated for DOK awareness
- [ ] Agent prompts include DOK guidance

### Phase 8: Documentation ✅
- [ ] DOK framework guide created
- [ ] Example workflows created (4+)
- [ ] Troubleshooting documentation complete

### Phase 9: Testing ✅
- [ ] Unit tests pass (80%+ coverage)
- [ ] Integration tests pass
- [ ] Validated against real assessments (60%+ accuracy)

### Phase 10: Deployment ✅
- [ ] CLAUDE.md updated
- [ ] Quick reference guides created
- [ ] Framework ready for production use

---

## Estimated Effort

| Phase | Estimated Hours | Complexity |
|-------|----------------|------------|
| Phase 1: Foundation | 8-10 hours | High |
| Phase 2: New Skills | 6-8 hours | Medium |
| Phase 3: Assessment Skills | 4-6 hours | Medium |
| Phase 4: Curriculum Skills | 3-4 hours | Low |
| Phase 5: Review Skills | 4-5 hours | Medium |
| Phase 6: Analytics | 5-6 hours | Medium |
| Phase 7: Agents | 2-3 hours | Low |
| Phase 8: Documentation | 4-5 hours | Low |
| Phase 9: Testing | 6-8 hours | Medium |
| **Total** | **42-55 hours** | **Medium-High** |

For an automated agent working efficiently, this could be completed in 5-7 days of focused work.

---

## Success Metrics

After implementation, validate success with:

1. **Technical Metrics:**
   - All unit tests pass
   - Classifier achieves >60% accuracy on real items
   - No breaking changes to existing skills

2. **Functional Metrics:**
   - Can classify 100 items in <30 seconds
   - Alignment reports generated in <5 minutes
   - DOK distributions calculated correctly

3. **Quality Metrics:**
   - DOK-enhanced assessments have balanced distributions
   - Review skills catch DOK misalignments
   - Analytics provide actionable DOK insights

4. **User Experience Metrics:**
   - Clear documentation for all DOK features
   - Examples demonstrate common use cases
   - Error messages are helpful and actionable

---

**This plan is ready for execution by an automated agent like Claude Code. Each phase includes specific files, code, and acceptance criteria to guide implementation.**
