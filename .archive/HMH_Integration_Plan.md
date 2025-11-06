# HMH Reference Materials Integration Plan for Professor Framework
**Date:** November 5, 2025
**Purpose:** Integrate HMH "Into Math" design guidelines and patterns into the Professor Framework (92 skills, 22 agents)

---

## Executive Summary

The baseline reference directory contains comprehensive HMH-specific guidelines for mathematics curriculum development. This plan outlines how to integrate these materials into the existing Professor framework through:
1. **Enhanced skill configurations** - Adding HMH-specific knowledge to existing skills
2. **New HMH-specific skills** - Creating specialized skills for unique HMH patterns
3. **Agent behavior modifications** - Updating agents to apply HMH standards automatically
4. **Reference knowledge base** - Structured knowledge files for LLM retrieval

---

## Document Analysis Summary

### Analyzed Materials (10 Document Types)

#### **Tier 1: Core Content Development Guidelines**
1. **Mathematical Language Routines (MLR) Guidelines**
   - 8 structured teaching routines (MLR1-MLR8)
   - Specific placement rules (SYL, Tasks, Module Planning)
   - Templated boilerplate text for each routine
   - Tracking requirements via MegaTrackers

2. **Alt Text Guidelines**
   - 40+ mathematical image types with specifications
   - Guiding principles: Brevity, Clarity, Drill-Down Organization, Validity
   - Visual bias detection rules
   - Embedded math notation standards

3. **Emergent Bilinguals (EB) Support Guidelines**
   - Asset-based language support approach
   - 3 proficiency levels (Pre-Production/Beginning, Intermediate, High Intermediate/Advanced)
   - Language objectives tied to 4 domains (speaking, writing, representing, listening)
   - Scaffolded support tables with sentence frames

4. **Universal Design for Learning (UDL) Guidelines**
   - 3 principles: Engagement, Representation, Action & Expression
   - Minimum 2 UDL supports per lesson, no repeated principles
   - Task-specific, not generalized support

5. **Vocabulary Guidelines**
   - New vocab: highlighted yellow + bold
   - Review vocab: no formatting
   - 3 placement approaches (in box, running text, within task)
   - High-utility "Tier 2" word selection
   - Vocabulary Tracker integration

#### **Tier 2: Structural & Pattern Guidelines**
6. **LXDV EMM SE and TE Content Guidelines** (file too large - 328KB)
   - Content structure for Student Edition and Teacher Edition
   - EMM (Educational Materials Management) patterns

7. **Pattern Guide for SYL and Tasks EMM Development** (file not found - need alternative name)
   - Workflow patterns for Spark Your Learning
   - Task development patterns

#### **Tier 3: Reference & Quality Assurance**
8. **Lesson Tools Icons** (InDesign + PDF files for K, 1-2, 3-5, 6-A1)
   - Visual design standards
   - Icon libraries for different grade bands

9. **Sample Lesson PDFs** (multiple files: k_mtxese, 1-2_mtxese, 3-5_mtxese, 6-A1_mtxese)
   - Real implementations showing guidelines in practice

10. **Vendor Guidelines** (subdirectory with checklists and playbooks)
    - Quality assurance checklists
    - Vendor specifications

---

## Integration Strategy

### Approach 1: Enhance Existing Professor Skills

Many Professor skills already handle curriculum development tasks. We'll enhance them with HMH-specific knowledge:

#### **Skills to Enhance:**

| Existing Skill | HMH Enhancement | Implementation Method |
|---|---|---|
| `curriculum.develop-content` | Add MLR placement logic, EB support patterns, UDL principles | Skill knowledge file |
| `curriculum.review-accessibility` | Integrate HMH Alt Text specifications | Skill knowledge file |
| `curriculum.review-bias` | Apply EB asset-based approach, cultural responsiveness checks | Skill knowledge file |
| `curriculum.develop-items` | Add HMH-specific item patterns, visual bias checks | Skill knowledge file |
| `curriculum.design` | Include Language Objective creation, High-Utility word selection | Skill knowledge file |

**Implementation:**
Create `/curriculum.develop-content.knowledge.md` files alongside skill definitions containing:
- MLR selection criteria and boilerplate templates
- EB scaffolding examples by proficiency level
- UDL principle application guidelines
- Vocabulary highlighting and tracking rules

---

### Approach 2: Create New HMH-Specific Skills

Some HMH patterns are unique enough to warrant new specialized skills:

#### **New Skills to Create:**

1. **`/hmh.mlr-embed`** - Embed Mathematical Language Routines
   - **Purpose:** Select and embed appropriate MLRs in lessons
   - **Inputs:** Lesson content, task type (SYL, Task, Module Planning)
   - **Outputs:** MLR selection + boilerplate text + MegaTracker entry
   - **Knowledge:** Full MLR guidelines with decision trees

2. **`/hmh.eb-scaffold`** - Create Emergent Bilingual Scaffolds
   - **Purpose:** Generate differentiated language support by proficiency level
   - **Inputs:** Task content, language objective, domain
   - **Outputs:** 3-level support table with sentence frames/starters
   - **Knowledge:** EB Resource document patterns, domain-specific strategies

3. **`/hmh.alt-text-generate`** - Generate HMH-Compliant Alt Text
   - **Purpose:** Create pedagogically sound alt text for math images
   - **Inputs:** Image type, grade level, item construct
   - **Outputs:** Alt text following HMH specifications
   - **Knowledge:** All 40+ image type specifications, visual bias rules

4. **`/hmh.vocab-track`** - Track and Format Vocabulary
   - **Purpose:** Manage vocabulary highlighting, placement, and tracking
   - **Inputs:** Lesson content, grade, module
   - **Outputs:** Formatted vocabulary, tracker updates, placement decisions
   - **Knowledge:** Vocabulary guidelines, High-Utility word lists

5. **`/hmh.udl-suggest`** - Suggest UDL Supports
   - **Purpose:** Recommend task-specific UDL supports
   - **Inputs:** Task content, already-used principles in lesson
   - **Outputs:** 2+ UDL support suggestions from unused principles
   - **Knowledge:** UDL framework with HMH-specific examples

6. **`/hmh.lesson-validate`** - Validate HMH Lesson Compliance
   - **Purpose:** Check lessons against all HMH quality standards
   - **Inputs:** Complete lesson content
   - **Outputs:** Compliance report with specific violations and fixes
   - **Knowledge:** All HMH guidelines, Vendor Checklist criteria

---

### Approach 3: Modify Agent Behaviors

The Professor framework's autonomous agents should automatically apply HMH standards:

#### **Agents to Modify:**

1. **`content-developer`** Agent
   - **Modification:** When creating Into Math content, automatically:
     - Invoke `/hmh.mlr-embed` for appropriate task types
     - Invoke `/hmh.eb-scaffold` for Turn and Talk sections
     - Invoke `/hmh.vocab-track` for vocabulary management
     - Invoke `/hmh.udl-suggest` for accessibility supports

2. **`assessment-designer`** Agent
   - **Modification:** When designing assessments:
     - Apply visual bias checks from Alt Text guidelines
     - Ensure construct validity (don't cue answers in alt text)
     - Follow HMH item specification patterns

3. **`quality-assurance`** Agent
   - **Modification:** Add HMH-specific validation steps:
     - Run `/hmh.lesson-validate` on all lessons
     - Check MLR tracking in MegaTrackers
     - Verify vocabulary highlighting and tracking
     - Confirm EB scaffolding at required locations
     - Validate UDL minimum requirements (2 per lesson, no repeats)

4. **`pedagogical-reviewer`** Agent
   - **Modification:** Evaluate against HMH pedagogical standards:
     - Asset-based approach for EB support
     - Mathematical language routine effectiveness
     - UDL principle application quality

---

### Approach 4: Create Structured Knowledge Base

Build a retrievable knowledge base for LLM access during content development:

#### **Knowledge Base Structure:**

```
/content/reference/hmh-knowledge/
├── mlr/
│   ├── mlr-overview.md
│   ├── mlr1-stronger-clearer.md
│   ├── mlr2-collect-display.md
│   ├── mlr3-critique-correct-clarify.md
│   ├── mlr6-three-reads.md
│   ├── mlr7-compare-connect.md
│   ├── mlr8-discussion-supports.md
│   └── mlr-placement-rules.md
├── accessibility/
│   ├── alt-text-principles.md
│   ├── visual-bias-detection.md
│   ├── image-types/
│   │   ├── 2d-shapes.md
│   │   ├── 3d-shapes.md
│   │   ├── bar-graphs.md
│   │   ├── coordinate-planes.md
│   │   ├── fraction-models.md
│   │   └── [... 35+ more types]
│   └── embedded-math-notation.md
├── language-support/
│   ├── eb-overview.md
│   ├── language-objectives.md
│   ├── proficiency-levels.md
│   ├── scaffolding-strategies/
│   │   ├── speaking.md
│   │   ├── writing.md
│   │   ├── representing.md
│   │   └── listening.md
│   └── eb-resource-examples.md
├── udl/
│   ├── udl-overview.md
│   ├── engagement-principle.md
│   ├── representation-principle.md
│   ├── action-expression-principle.md
│   └── math-specific-examples.md
├── vocabulary/
│   ├── vocab-guidelines.md
│   ├── high-utility-words.md
│   ├── placement-approaches.md
│   └── vocabulary-tracker-process.md
├── patterns/
│   ├── syl-patterns.md (Spark Your Learning)
│   ├── task-patterns.md
│   ├── turn-and-talk-patterns.md
│   ├── module-planning-patterns.md
│   └── lesson-structure-patterns.md
└── quality/
    ├── vendor-checklist.md
    ├── construct-validity.md
    └── compliance-validation.md
```

**Implementation:**
1. Extract knowledge from baseline PDFs/DOCXs into markdown files
2. Structure for easy retrieval (semantic search, embeddings, RAG)
3. Link knowledge files to relevant skills and agents
4. Version control knowledge base alongside curriculum content

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Extract and structure core knowledge

**Tasks:**
1. ☐ Extract all baseline documents to markdown format
2. ☐ Create knowledge base directory structure
3. ☐ Populate core knowledge files:
   - MLR guidelines (8 routines)
   - Alt Text specifications (40+ types)
   - EB scaffolding strategies
   - UDL principles
   - Vocabulary rules
4. ☐ Create knowledge embeddings for retrieval

**Deliverables:**
- Complete `/content/reference/hmh-knowledge/` directory
- Indexed knowledge base ready for LLM retrieval

---

### Phase 2: Skill Enhancement (Weeks 3-4)
**Goal:** Enhance existing Professor skills with HMH knowledge

**Tasks:**
1. ☐ Create knowledge files for existing skills:
   - `curriculum.develop-content.knowledge.md`
   - `curriculum.review-accessibility.knowledge.md`
   - `curriculum.review-bias.knowledge.md`
   - `curriculum.develop-items.knowledge.md`
   - `curriculum.design.knowledge.md`
2. ☐ Update skill prompts to reference HMH knowledge
3. ☐ Test enhanced skills with sample Into Math content
4. ☐ Iterate based on output quality

**Deliverables:**
- 5+ enhanced skills with HMH-specific knowledge
- Test results demonstrating HMH compliance

---

### Phase 3: New Skill Creation (Weeks 5-7)
**Goal:** Build specialized HMH skills

**Priority 1 (Critical):**
1. ☐ `/hmh.mlr-embed` - MLR embedding skill
2. ☐ `/hmh.alt-text-generate` - Alt text generation skill
3. ☐ `/hmh.eb-scaffold` - EB scaffolding skill

**Priority 2 (Important):**
4. ☐ `/hmh.vocab-track` - Vocabulary tracking skill
5. ☐ `/hmh.udl-suggest` - UDL suggestion skill

**Priority 3 (Quality Assurance):**
6. ☐ `/hmh.lesson-validate` - Lesson validation skill

**For Each Skill:**
- Write skill specification
- Create skill prompt with examples
- Build decision logic/templates
- Test with real content
- Document usage

**Deliverables:**
- 6 new operational HMH-specific skills
- Skill documentation and usage guides

---

### Phase 4: Agent Integration (Weeks 8-9)
**Goal:** Modify agents to use HMH skills automatically

**Tasks:**
1. ☐ Modify `content-developer` agent:
   - Auto-invoke HMH skills during lesson development
   - Follow Into Math content patterns
2. ☐ Modify `assessment-designer` agent:
   - Apply HMH item specifications
   - Validate construct integrity
3. ☐ Modify `quality-assurance` agent:
   - Run HMH validation checks
   - Generate compliance reports
4. ☐ Modify `pedagogical-reviewer` agent:
   - Evaluate HMH pedagogical standards
5. ☐ Test agent workflows end-to-end

**Deliverables:**
- 4 modified agents with HMH capabilities
- End-to-end workflow demonstrations

---

### Phase 5: Validation & Refinement (Weeks 10-12)
**Goal:** Validate outputs against HMH standards

**Tasks:**
1. ☐ Create test corpus of Into Math lessons
2. ☐ Generate content using Professor + HMH integration
3. ☐ Validate outputs against:
   - Vendor Checklists
   - HMH guidelines
   - Sample lesson PDFs
4. ☐ Collect feedback from HMH subject matter experts
5. ☐ Refine skills, agents, and knowledge base
6. ☐ Create usage documentation and training materials

**Deliverables:**
- Validation report with quality metrics
- Refined system ready for production use
- Complete documentation

---

## Prioritized Component List

### Must-Have (Production Ready)
1. **MLR Embedding** - Core to HMH lesson design
2. **Alt Text Generation** - Accessibility requirement
3. **EB Scaffolding** - Differentiates HMH content
4. **Vocabulary Tracking** - Content consistency requirement
5. **Enhanced Content Development** - Foundation for all content

### Should-Have (Enhanced Quality)
6. **UDL Support Suggestions** - Improves accessibility
7. **Lesson Validation** - Ensures compliance
8. **Modified Quality Assurance Agent** - Catches issues early

### Nice-to-Have (Optimization)
9. **Pattern Templates** - Speeds development
10. **Integration with MegaTrackers** - Automates tracking
11. **Sample Lesson Comparison** - Quality benchmarking

---

## Technical Considerations

### Knowledge Retrieval Strategy
**Recommendation:** Hybrid approach
- **Structured templates** for MLRs, EB scaffolds (exact boilerplate needed)
- **Semantic search** for Alt Text specs, UDL examples (context-dependent)
- **Rule-based** for Vocabulary formatting (deterministic)

### Integration Points with Professor Framework
1. **Skill System:** Add HMH skills to existing 92 skills
2. **Agent System:** Modify agent prompts to include HMH awareness
3. **Knowledge System:** Link HMH knowledge base to retrieval system
4. **Workflow System:** Create "Into Math" workflow templates

### Configuration Management
Create HMH-specific configuration:

```json
{
  "curriculum": "Into Math",
  "publisher": "HMH",
  "version": "v2",
  "standards": ["CCSS", "TEKS", "NGSS"],
  "guidelines": {
    "mlr": {
      "enabled": true,
      "tracking": "megatracker",
      "placement": ["syl", "tasks", "module-planning"]
    },
    "eb_support": {
      "enabled": true,
      "proficiency_levels": ["pre-production", "intermediate", "advanced"],
      "domains": ["speaking", "writing", "representing", "listening"]
    },
    "udl": {
      "enabled": true,
      "minimum_per_lesson": 2,
      "allow_repeat_principles": false
    },
    "vocabulary": {
      "new_format": "bold+highlight",
      "review_format": "plain",
      "tracker_integration": true
    },
    "alt_text": {
      "approach": "pedagogical",
      "visual_bias_check": true
    }
  }
}
```

---

## Success Metrics

### Quality Metrics
- **HMH Compliance Rate:** % of generated content meeting all HMH guidelines
- **Alt Text Quality:** % passing visual bias and pedagogy checks
- **MLR Accuracy:** % correct MLR placement and boilerplate usage
- **EB Scaffolding Completeness:** % lessons with proper 3-level support
- **Vocabulary Consistency:** % vocabulary properly highlighted and tracked

### Efficiency Metrics
- **Content Development Speed:** Time to create HMH-compliant lesson
- **Revision Cycles:** Number of iterations needed for compliance
- **Manual Intervention Rate:** % of content requiring human adjustment

### Adoption Metrics
- **Skill Usage:** Number of invocations per HMH skill
- **Agent Workflow Completion:** % of lessons developed fully by agents
- **User Satisfaction:** Feedback scores from content developers

---

## Risk Mitigation

### Risks & Mitigation Strategies

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| HMH guidelines change | High | Medium | Version knowledge base, easy updates |
| Knowledge base too large for context | Medium | High | Use hybrid retrieval (embeddings + rules) |
| Agent decisions conflict with HMH rules | High | Medium | Validation layer, human-in-loop for edge cases |
| Skill complexity overwhelming | Medium | Medium | Progressive disclosure, workflow templates |
| Output quality doesn't meet HMH standards | High | Low | Extensive validation phase, SME review |

---

## Next Steps

### Immediate Actions (This Week)
1. **Get stakeholder approval** on this integration plan
2. **Set up project structure** for knowledge base
3. **Begin Phase 1:** Extract baseline documents to markdown
4. **Identify SMEs** for validation during Phase 5

### Questions to Resolve
1. Do we have access to the MegaTrackers for MLR and Vocab tracking integration?
2. Are there additional HMH guidelines beyond the baseline directory?
3. What's the priority: speed (automate everything) vs. quality (human oversight)?
4. Should HMH integration be a configuration option or a separate deployment?

---

## Conclusion

This plan provides a structured approach to integrating HMH's "Into Math" design knowledge into the Professor framework through:
- **Enhanced existing skills** with HMH-specific knowledge
- **New specialized skills** for unique HMH patterns (MLR, EB, Alt Text, UDL, Vocab)
- **Modified agent behaviors** for automatic HMH compliance
- **Structured knowledge base** for LLM retrieval

The phased approach allows for incremental validation and refinement, with clear success metrics at each stage. The result will be a world-class system capable of generating HMH-compliant "Into Math" curriculum content with minimal human intervention while maintaining the pedagogical quality HMH requires.

**Estimated Timeline:** 12 weeks to production-ready system
**Estimated Effort:** 1-2 developers full-time
**Estimated Impact:** 10x faster HMH content development with higher consistency

