# HMH Multi-Curriculum Knowledge Base: User Guide Overview
**Complete Documentation Suite for All Roles**
**Version:** 3.0
**Last Updated:** November 6, 2025

---

## Welcome

This documentation suite provides comprehensive guidance for everyone involved in the HMH content development lifecycle:

- **Content Authors** - Writing lessons, assessments, and activities
- **Content Editors** - Reviewing and approving content
- **Publishers/Production** - Formatting and delivering final products
- **Knowledge Base Engineers** - Extending and maintaining the system

**Each role has a dedicated guide with complete workflows, templates, examples, and best practices.**

---

## Quick Navigation: Choose Your Guide

### Are you creating content?
→ **[AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)** - Complete guide for content authors

**You'll learn:**
- How to use the knowledge base to generate lessons and assessments
- Complete authoring workflows for lessons (3-5 days), assessments (2-4 days), and activities (1-2 days)
- How to work with AI assistance (Professor Framework)
- Quality standards and pre-submission checklists
- Git workflow and collaboration practices

**Start here if you're:** Writing lessons, creating assessments, developing activities, or authoring any instructional content.

---

### Are you reviewing content?
→ **[EDITOR_GUIDE.md](EDITOR_GUIDE.md)** - Complete guide for content editors

**You'll learn:**
- Editorial workflow from assignment to approval
- Comprehensive review checklist (8 sections covering all 7 quality pillars)
- How to provide effective, actionable feedback
- When and how to approve content
- Common content issues and how to fix them

**Start here if you're:** Reviewing content for quality, providing feedback to authors, or approving content for publication.

---

### Are you producing deliverables?
→ **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** - Complete guide for publishers and production staff

**You'll learn:**
- Multi-format production workflows (PDF, HTML, SCORM, Common Cartridge, accessible formats)
- Asset management and optimization (images, videos, audio)
- Quality assurance checklists for production
- Delivery and distribution processes
- Technical specifications and tools

**Start here if you're:** Formatting content, creating PDFs, building SCORM/Common Cartridge packages, managing assets, or delivering final products.

---

### Are you extending the system?
→ **[ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)** - Complete guide for knowledge base engineers

**You'll learn:**
- System architecture and hierarchical knowledge resolution
- How to add new states/districts (2-6 files, 85-97% reuse)
- How to add new subjects (8-15 files)
- How to create curriculum configs
- How to extend universal knowledge
- File creation best practices and templates

**Start here if you're:** Adding new states, creating subject frameworks, maintaining the knowledge base, or architecting the system.

---

## What is the HMH Multi-Curriculum Knowledge Base?

A **hierarchical knowledge resolution system** that enables creating standards-aligned, state-compliant instructional materials with **85-97% knowledge reuse** across curricula.

### Key Innovation: Write Once, Reuse Everywhere

Instead of creating separate content for each state and subject, the system uses a 5-level hierarchy:

```
1. Program-Specific      → HMH Into Math TX specific features
2. Subject-District      → Texas Math TEKS alignment
3. Subject-Common        → Math Language Routines (all states)
4. District-Wide         → Texas ELPS language standards (all subjects)
5. Universal             → UDL, DOK, WCAG (everything)
```

**Resolution Rule:** Search from specific to general, first match wins.

### Current Coverage (Week 3 - 50 Files)

**States:**
- Texas (TEKS standards)
- California (CCSS/NGSS standards)
- Florida (MAFS/B.E.S.T./NGSSS standards)

**Subjects:**
- Mathematics (K-8) - 8 Math Language Routines
- ELA (K-8) - 4 Literacy Routines
- Science (K-8) - NGSS 3-dimensional learning

**Programs:**
- HMH Into Math (TX, CA, FL editions)
- HMH Into Reading (TX edition)

### Knowledge Reuse Demonstrated

- **Florida Math:** 97% reuse (only 1 new file, 30 existing files reused)
- **California Math:** 93% reuse (2 new files, 28 existing files reused)
- **Texas ELA:** 90% reuse (3 new files, 27 existing files reused)

---

## Getting Started

### For Content Authors

1. Read **[AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)** Section 1: Getting Started
2. Understand your content brief (Section 2)
3. Learn to use the knowledge base (Section 3)
4. Follow the appropriate workflow (Section 4: Lessons, Assessments, or Activities)
5. Run through the quality checklist before submitting (Section 6)

**Typical timeline:** 1-5 days depending on content type

---

### For Content Editors

1. Read **[EDITOR_GUIDE.md](EDITOR_GUIDE.md)** Section 1: Getting Started
2. Review the editorial workflow (Section 2)
3. Use the comprehensive review checklist (Section 3)
4. Provide feedback using templates (Section 4)
5. Approve when ready (Section 5)

**Typical review:** 2-4 hours per lesson/assessment

---

### For Production Staff

1. Read **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** Section 1: Getting Started
2. Understand the publishing workflow (Section 2)
3. Choose appropriate format(s) (Section 3: PDF, HTML, SCORM, Common Cartridge, accessible)
4. Manage and optimize assets (Section 4)
5. Run QA checks before delivery (Section 5)

**Typical production:** 2-5 days depending on complexity

---

### For Engineers

1. Read **[ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)** Section 1: Architecture Quick Start
2. Learn knowledge resolution (Section 2)
3. Follow step-by-step guides for adding states/subjects (Sections 3-4)
4. Use templates and patterns (Section 8)
5. Apply quality assurance (Section 9)

**Typical implementation:** 2-6 hours per state, 1-2 days per subject

---

## The Complete Content Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE BASE                            │
│  (50 files: Universal, Subject-Common, District-Wide, etc.) │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    ┌──────────────┐
                    │   AUTHORING  │  ← AUTHOR_GUIDE.md
                    │  (3-5 days)  │
                    └──────────────┘
                           ↓
                    ┌──────────────┐
                    │   EDITORIAL  │  ← EDITOR_GUIDE.md
                    │  (2-4 hours) │
                    └──────────────┘
                           ↓
                    ┌──────────────┐
                    │  PRODUCTION  │  ← PRODUCTION_GUIDE.md
                    │  (2-5 days)  │
                    └──────────────┘
                           ↓
                    ┌──────────────┐
                    │   DELIVERY   │
                    │ (PDF, SCORM, │
                    │ HTML, Print) │
                    └──────────────┘

       SYSTEM EXTENSION: ENGINEER_GUIDE.md
```

---

## Quality Standards (All Roles)

All content must meet these standards:

### The 7 Quality Pillars

1. **Standards Alignment** - Explicitly aligned to state content standards
2. **Pedagogical Soundness** - Evidence-based instructional practices
3. **Language Support** - ELPS/ELD/ESOL scaffolds by proficiency level
4. **Universal Design for Learning** - Multiple means of representation, action, engagement
5. **Accessibility** - WCAG 2.1 AA compliance (minimum)
6. **Cultural Responsiveness** - CEID framework, bias-free, diverse representation
7. **State Compliance** - State-specific adoption criteria and statutory requirements

**Each guide provides detailed checklists and guidance for your role's responsibilities.**

---

## The Professor Framework Integration

All guides integrate with the **Professor Framework** - an AI-powered content development system with:

- **92 Composable Skills** - Research, design, development, review, packaging, analytics
- **22 Autonomous Agents** - Intelligent agents that orchestrate workflows
- **GitHub Integration** - @claude mentions, workflow triggers, automated reviews

**Authors:** Section 5 of AUTHOR_GUIDE.md covers AI assistance
**Engineers:** See CLAUDE.md for complete Professor configuration

---

## Documentation Roadmap

### Current Documentation (Week 3 Complete)

✅ **AUTHOR_GUIDE.md** - 850 lines, comprehensive authoring workflows
✅ **EDITOR_GUIDE.md** - 450 lines, complete editorial process
✅ **PRODUCTION_GUIDE.md** - 450 lines, multi-format production
✅ **ENGINEER_GUIDE.md** - 1700 lines, system architecture and extension
✅ **USER_GUIDE.md** - This overview (you are here)

### Supporting Documentation

- **README.md** - Project overview and quick start
- **CLAUDE.md** - Claude Code configuration and Professor integration
- **INCOMPLETE_ANALYSIS.md** - Known gaps and future work
- **.archive/** - Historical HMH planning documents (Week 1-3 summaries)

---

## Support and Resources

### Documentation

- **All Guides:** Available in repository root directory
- **Knowledge Base Files:** `/reference/hmh-knowledge-v2/`
- **Curriculum Configs:** `/config/curriculum/`
- **Professor Framework:** https://github.com/pauljbernard/professor

### Getting Help

**For Questions About:**
- **Authoring:** See AUTHOR_GUIDE.md Section 7 (Collaboration) and Quick Reference
- **Editorial:** See EDITOR_GUIDE.md Section 6 (Support)
- **Production:** See PRODUCTION_GUIDE.md Section 6 (Support)
- **Engineering:** See ENGINEER_GUIDE.md Section 11 (Getting Help)

**For System Issues:**
- Create issue in repository: https://github.com/pauljbernard/content/issues
- Contact development team
- Check INCOMPLETE_ANALYSIS.md for known issues

---

## Quick Reference: Common Tasks

| I want to... | See this guide | Section |
|-------------|----------------|---------|
| Write a lesson | AUTHOR_GUIDE.md | Section 4 (Lesson Workflow) |
| Create an assessment | AUTHOR_GUIDE.md | Section 4 (Assessment Workflow) |
| Use AI assistance | AUTHOR_GUIDE.md | Section 5 (Professor Framework) |
| Review content quality | EDITOR_GUIDE.md | Section 3 (Review Checklist) |
| Provide feedback | EDITOR_GUIDE.md | Section 4 (Effective Feedback) |
| Create a PDF | PRODUCTION_GUIDE.md | Section 3 (PDF Production) |
| Build SCORM package | PRODUCTION_GUIDE.md | Section 3 (SCORM Production) |
| Build Common Cartridge package | PRODUCTION_GUIDE.md | Section 3 (Format 3B: Common Cartridge) |
| Optimize images/videos | PRODUCTION_GUIDE.md | Section 4 (Asset Management) |
| Add a new state | ENGINEER_GUIDE.md | Section 3 (Add State/District) |
| Add a new subject | ENGINEER_GUIDE.md | Section 4 (Add Subject) |
| Create curriculum config | ENGINEER_GUIDE.md | Section 5 (Create Config) |
| Add universal framework | ENGINEER_GUIDE.md | Section 6 (Extend Universal) |

---

## Version History

**Version 3.0** (November 6, 2025)
- Restructured as overview document
- Created 4 specialized role-based guides
- Complete content lifecycle coverage
- 850+ pages of comprehensive documentation

**Version 2.0** (November 4, 2025)
- Added Parts A, B, C structure (authoring, editorial, production)
- Expanded from engineering-only to full lifecycle

**Version 1.0** (October 2025)
- Initial engineering documentation (Part D)
- Architecture and knowledge base extension

---

## What's Next?

**Choose your guide and get started:**

- **[AUTHOR_GUIDE.md](AUTHOR_GUIDE.md)** - If you create content
- **[EDITOR_GUIDE.md](EDITOR_GUIDE.md)** - If you review content
- **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** - If you produce deliverables
- **[ENGINEER_GUIDE.md](ENGINEER_GUIDE.md)** - If you extend the system

**Each guide is comprehensive, with step-by-step workflows, templates, examples, checklists, and quick references.**

---

**Welcome to the HMH Multi-Curriculum Knowledge Base!**

**Maintained By:** HMH Curriculum Development Team
**Repository:** https://github.com/pauljbernard/content.git
**Last Updated:** November 6, 2025
