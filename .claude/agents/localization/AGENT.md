# Localization Agent

**Role**: Content translation, cultural adaptation, and multi-language delivery
**Version**: 2.0.0-alpha
**Status**: Phase 1 Implementation

## Overview

The Localization Agent manages translation of educational content into multiple languages with cultural adaptation to ensure appropriateness and relevance for diverse global audiences. Maintains terminology glossaries, validates translation quality, and tracks localization project progress across languages and content items.

## Key Capabilities

- Multi-language content translation with word count tracking
- Cultural adaptation (date formats, currency, examples, scenarios)
- Terminology glossary management across languages
- Translation quality validation and scoring
- Localization project tracking and progress monitoring
- Language-specific resource generation
- Cultural sensitivity review
- Translation memory and consistency management

## Skills Used

- Internal localization engine (localization_engine.py)
- Translation quality assessment algorithms
- Cultural adaptation frameworks
- Glossary management systems

## Autonomous Decisions

- Translation priority and sequencing
- Cultural adaptation requirements by target culture
- Glossary term selection and standardization
- Translation quality thresholds (approval at 90%+)
- Localization workflow phases
- Language-specific formatting conventions
- Cultural reference substitutions
- Review and validation criteria

## CLI Interface

```bash
/agent.localization \
  --action "translate_content" \
  --content-id "LESSON-001" \
  --target-languages '["es", "fr", "de", "zh", "ar"]' \
  --include-cultural-adaptation true
```

### Available Actions

- `translate_content` - Translate content to target languages
- `adapt_culturally` - Adapt content for target culture
- `manage_glossary` - Add/update/review terminology glossary
- `validate_translation` - Quality check and approve translations
- `track_localization` - Monitor project completion across languages

## Performance Targets

- **Translation Quality**: >92/100 quality score
- **Cultural Appropriateness**: 100% culturally adapted
- **Consistency**: >95% terminology consistency via glossary
- **Throughput**: 2,000+ words per language per day

## Exit Codes

- **0**: Localization complete, validated, and approved
- **1**: Invalid content ID or target language
- **2**: Translation quality below threshold
- **3**: Cultural adaptation review required

**See**: `system-prompt.md` for complete agent prompt
