# Plagiarism Detection & Originality Verification Skill

**Skill**: `/curriculum.plagiarism-check`
**Category**: Quality Assurance
**Addresses**: GAP-8 (CRITICAL)
**Purpose**: Detect plagiarism, verify content originality, and ensure copyright compliance for curriculum materials

## Description

Checks curriculum content against internet sources, academic databases, and internal content library to detect potential plagiarism, copyright infringement, or unintentional duplication. Generates originality scores and detailed similarity reports for legal compliance.

## Usage

```bash
/curriculum.plagiarism-check \
  --input "curriculum-content/" \
  --check-against "web|academic|internal|all" \
  --sensitivity "standard|high|strict" \
  --report-format "summary|detailed|legal" \
  --threshold 15
```

## Check Modes

### 1. Web Search Similarity

Checks content against publicly available internet sources.

**Method**:
- Extract text passages (sentences, paragraphs)
- Search via web search APIs (Bing, Google Custom Search)
- Calculate similarity scores using fuzzy matching
- Identify matching URLs and publication dates
- Check Creative Commons vs. copyrighted sources

**Parameters**:
- `--web-search-engine`: "bing|google|duckduckgo"
- `--min-passage-length`: Minimum words to check (default: 8)
- `--similarity-threshold`: % similarity to flag (default: 85%)

**Output**:
- List of matching web sources with URLs
- Similarity percentage per source
- License status (CC, public domain, copyrighted)
- Risk assessment (low/medium/high)

### 2. Academic Database Check

Checks against academic publications, textbooks, and educational materials.

**Databases** (via APIs where available):
- Google Scholar
- JSTOR (if institutional access)
- ERIC (Education Resources Information Center)
- Open textbook libraries (OpenStax, CK-12)
- ArXiv (for STEM content)

**Parameters**:
- `--databases`: Comma-separated list of databases
- `--field-of-study`: "math|science|english|history|all"
- `--publication-years`: Range (e.g., "2015-2025")

**Output**:
- Academic source matches
- Publication details (author, year, title, DOI)
- Exact quotes vs. paraphrased content
- Citation recommendations

### 3. Internal Content Library Check

Checks against previously created Professor curriculum content.

**Method**:
- Maintain database of all generated content
- Index by project, subject, grade level
- Compare new content against existing
- Identify self-plagiarism or unintended reuse

**Parameters**:
- `--exclude-project`: Don't check against specific projects
- `--cross-project-check`: Check across all projects
- `--same-author-ok`: Flag same-author reuse or not

**Output**:
- Internal matches with project references
- Reuse percentage
- Recommendations for attribution or revision

### 4. Citation Verification

Verifies that cited sources are accurate and properly attributed.

**Checks**:
- Citation format correctness (APA, MLA, Chicago)
- URL accessibility (links not broken)
- Quote accuracy (matches original source)
- Page numbers correct
- Publication year accurate

**Output**:
- Citation accuracy report
- Broken links list
- Misquoted passages
- Missing attributions

## Similarity Detection Algorithms

### Text Fingerprinting

- Break content into n-grams (5-10 word sequences)
- Hash each n-gram
- Compare hash sets for similarity
- Jaccard similarity coefficient
- Ignore common phrases ("according to the theorem")

### Semantic Similarity

- Use embedding models (BERT, Sentence Transformers)
- Compare semantic meaning, not just exact words
- Detects paraphrased plagiarism
- Threshold for semantic similarity: 0.85-0.95

### Quote Detection

- Identify quoted passages (in quotation marks)
- Verify against cited sources
- Flag uncited quotes
- Suggest proper attribution

## Originality Scoring

### Overall Originality Score (0-100%)

```
Originality = 100% - (Web Similarity × 0.4 + Academic Similarity × 0.4 + Internal Similarity × 0.2)
```

**Interpretation**:
- **90-100%**: Highly original, no concerns
- **75-89%**: Mostly original, minor similarities acceptable
- **50-74%**: Moderate similarity, requires review
- **25-49%**: High similarity, significant revision needed
- **0-24%**: Potential plagiarism, DO NOT PUBLISH

### Risk Assessment

**Low Risk**:
- Originality > 85%
- Matches are properly cited
- Common knowledge passages
- Creative Commons sources with attribution

**Medium Risk**:
- Originality 60-85%
- Some uncited matches
- Paraphrased content without attribution
- Requires citation additions

**High Risk**:
- Originality < 60%
- Substantial uncited matches
- Copyrighted sources without permission
- DO NOT PUBLISH without legal review

## Detailed Similarity Report

### Report Sections

**1. Executive Summary**
- Overall originality score
- Risk level (low/medium/high)
- Number of flagged passages
- Recommended actions

**2. Passage-Level Findings**
```
Passage: "The Pythagorean theorem states that in a right triangle..."
Location: Unit 3, Lesson 5, Page 47
Similarity: 92% match
Source: [Wikipedia - Pythagorean Theorem](https://en.wikipedia.org/wiki/...)
License: Creative Commons BY-SA
Risk: LOW (properly attributed, CC license)
Recommendation: Add citation or rephrase
```

**3. Source Breakdown**
- Web sources (with URLs and licenses)
- Academic sources (with DOIs and citation info)
- Internal sources (with project references)

**4. Citation Audit**
- Total citations: 47
- Accurate citations: 45 (96%)
- Inaccurate citations: 2 (4%)
- Missing citations: 8 flagged passages

**5. Action Items**
- [ ] Revise 3 passages with high similarity (>90%)
- [ ] Add citations for 8 uncited passages
- [ ] Verify 2 inaccurate citations
- [ ] Request permission for 1 copyrighted image

## Legal Compliance Features

### Copyright Status Tracking

For each flagged source:
- **Public Domain**: Safe to use
- **Creative Commons**: Check license terms (BY, SA, NC, ND)
- **Fair Use**: Assess factors (purpose, amount, effect on market)
- **Copyrighted**: Requires permission or removal

### Fair Use Assessment

Evaluates four factors:
1. **Purpose**: Educational use (favors fair use)
2. **Nature**: Published factual content (favors fair use)
3. **Amount**: Percentage of original work used
4. **Market Effect**: Does it harm commercial value?

**Output**: Fair use likelihood (likely/possible/unlikely)

### Permission Request Workflow

For copyrighted content requiring permission:
1. Identify copyright holder
2. Generate permission request letter
3. Track request status
4. Document granted permissions
5. Schedule license expiration reviews

## Use Cases

### Use Case 1: Pre-Publication Check

**Scenario**: TestCraft Pro verifies 5,000 assessment items before release.

```bash
/curriculum.plagiarism-check \
  --input "assessment-bank/items/" \
  --check-against "all" \
  --sensitivity "strict" \
  --report-format "legal" \
  --threshold 10
```

**Output**:
- Legal compliance report for counsel review
- 47 items flagged for high similarity (0.94%)
- 12 require revision (0.24%)
- 35 need citations added (0.70%)
- Overall originality: 94.2% (acceptable)

### Use Case 2: AI-Generated Content Verification

**Scenario**: Verify AI-generated curriculum doesn't contain copyrighted material.

```bash
/curriculum.plagiarism-check \
  --input "ai-generated/7th-grade-math/" \
  --check-against "web,academic" \
  --sensitivity "high" \
  --report-format "detailed" \
  --ai-generated true
```

**Special AI-Generated Checks**:
- Compare against training data sources (if known)
- Flag verbatim passages (AI shouldn't produce these)
- Check for memorized content (famous quotes, textbook passages)
- Verify factual claims against authoritative sources

### Use Case 3: Competitive Content Analysis

**Scenario**: Ensure new curriculum doesn't infringe competitor copyrights.

```bash
/curriculum.plagiarism-check \
  --input "new-curriculum/" \
  --check-against "web,academic" \
  --competitor-urls "competitor1.com,competitor2.com" \
  --sensitivity "strict" \
  --threshold 5
```

**Output**:
- Flag any similarity to competitor content >5%
- Identify structural similarities (scope/sequence)
- Recommend differentiation strategies

### Use Case 4: Citation Audit

**Scenario**: Review existing curriculum for proper attribution.

```bash
/curriculum.plagiarism-check \
  --action "audit-citations" \
  --input "existing-curriculum/" \
  --citation-style "APA" \
  --check-links
```

**Output**:
- Citation accuracy: 89%
- Broken links: 12 (need updating)
- Misformatted citations: 23
- Missing citations: 8 passages

## Implementation

### Architecture

```
Plagiarism Checker
  ├─ Text Extractor (PDFs, DOCX, HTML, Markdown)
  ├─ N-gram Generator
  ├─ Hash Database (content fingerprints)
  ├─ Web Search Module
  │   ├─ Bing Search API
  │   ├─ Google Custom Search API
  │   └─ DuckDuckGo API
  ├─ Academic Database Module
  │   ├─ Google Scholar scraper
  │   ├─ ERIC API
  │   └─ ArXiv API
  ├─ Internal Content Database
  │   └─ SQLite/PostgreSQL with full-text search
  ├─ Similarity Scorer
  │   ├─ Jaccard similarity
  │   ├─ Cosine similarity (embeddings)
  │   └─ Levenshtein distance (fuzzy matching)
  ├─ Citation Validator
  │   ├─ Citation parser (APA, MLA, Chicago)
  │   ├─ URL checker (HTTP requests)
  │   └─ DOI resolver
  └─ Report Generator
      ├─ HTML report
      ├─ PDF report
      └─ JSON (machine-readable)
```

### Key Technologies

**Text Similarity**:
- `sentence-transformers` (semantic embeddings)
- `nltk` or `spacy` (tokenization)
- `fuzzywuzzy` (fuzzy string matching)
- `datasketch` (MinHash for large-scale deduplication)

**Web Search**:
- Bing Web Search API (Microsoft Azure)
- Google Custom Search JSON API
- DuckDuckGo API (free, no authentication)

**Academic Databases**:
- `scholarly` Python library (Google Scholar)
- ERIC API (free, U.S. Department of Education)
- ArXiv API (free, open-access preprints)

**Citation Parsing**:
- `anystyle` (citation parser)
- `crossref` API (DOI lookup)
- `requests` (URL validation)

### Performance Optimization

- **Chunking**: Process large documents in 1,000-word chunks
- **Caching**: Cache web search results (avoid re-checking)
- **Parallel Processing**: Check multiple passages simultaneously
- **Rate Limiting**: Respect API limits (Bing: 1,000 queries/month free tier)
- **Sampling**: For large item banks, sample 20% for quick check

## Integration with Agents

- **Quality Assurance Agent**: Runs plagiarism check during review phase
- **Content Developer Agent**: Pre-check during content generation
- **Assessment Designer Agent**: Verify item originality before bank addition

## Performance Metrics

- **Check time**: 30 seconds per 1,000 words
- **Accuracy**: >95% detection of substantial similarity (>50%)
- **False positive rate**: <5% (common phrases incorrectly flagged)
- **API costs**: $0.001 per passage checked (web search)

## Success Criteria

- ✅ Detects 95%+ of copyrighted content matches
- ✅ Zero copyright infringement lawsuits
- ✅ 100% of high-risk content reviewed before publication
- ✅ Citation accuracy improves from 70% to 95%
- ✅ Legal teams approve reports for compliance

---

**Status**: Ready for implementation
**Dependencies**: Web search APIs, text similarity libraries
**Testing**: Requires known plagiarized vs. original content samples
**Legal Note**: This tool aids detection but requires human legal review for final decisions
