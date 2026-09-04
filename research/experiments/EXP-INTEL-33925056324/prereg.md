# EXP-INTEL-33925056324 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-33925056324
- **Lane**: Intel
- **Claims**: C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON
- **Date**: 2026-09-04
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does existing accessibility-tree-based web agent research provide reusable element-matching or state-tracking patterns that could reduce the REQUIRES_TRANSFORM overhead for WebArena integration, or is SPIDER's fragment extraction a genuinely novel requirement?

## 3. Motivation

The parent handoff (EXP-INTEL-33842055594) established that:
- WebArena exposes DOM via CDP in accessibility_tree and html modes
- The observation format requires non-trivial transformation (REQUIRES_TRANSFORM / PARTIALLY_COMPATIBLE)
- The critical unknown is whether the transformation cost is recoverable

The parent handoff recommended a graph-lane integration experiment (Docker deployment + fragment extraction). However, SPIDER currently has NO fragment extraction code (research/harness/ does not exist). Before the graph lane builds new code, Intel should determine whether the accessibility-tree web agent literature already provides reusable patterns.

If existing work demonstrates structured element matching from accessibility trees with cross-site transfer, the graph lane can adapt these patterns rather than building from scratch, dramatically reducing integration cost. If no such work exists, the graph lane faces a genuinely novel engineering challenge and the cost-benefit calculus for WebArena changes.

## 4. Scope

### 4.1 What This Survey Covers

Recent (2023-2026) web agent papers that:
1. Use accessibility trees (ARIA structure from browser DevTools) as a primary observation modality
2. Perform some form of element matching, selection, or grounding for interactive tasks
3. Report cross-site, cross-environment, or generalizable element-matching results

### 4.2 What This Survey Excludes

- Papers using only screenshots, HTML, or raw DOM (not accessibility trees)
- Papers using accessibility trees only for page understanding (not element matching)
- Papers before 2023 (pre-dates current accessibility-tree-based web agent methods)
- Papers without published results or peer review

### 4.3 Relevance Criterion

Each paper is assessed for relevance to SPIDER's specific problem: can its element-matching approach be adapted to extract reusable fragments from WebArena's accessibility tree output for cross-site transfer? Papers that use accessibility trees for navigation but not for reusable fragment extraction are included but flagged as partially relevant.

## 5. Search Strategy

### 5.1 Query Strategy

Use 3+ independent search approaches:

1. **Keyword search**: "accessibility tree" + "web agent", "accessibility tree" + "element matching", "accessibility tree" + "cross-site", "ARIA" + "web navigation" + "agent"
2. **Venue/conference search**: ACL, EMNLP, NeurIPS, ICML, ICLR, AAAI, CHI, UIST proceedings (2023-2026)
3. **Citation tracking**: Forward/backward citation from key papers (e.g., Mind2Web, WebArena, SeeAct, AutoWebGLM)
4. **Author search**: Known web agent research groups (Notre Dame Mind2Web team, Microsoft Research, Google DeepMind)

### 5.2 Inclusion Criteria

A paper is included if ALL of:
- Published 2023-2026
- Uses accessibility trees (Accessibility.getFullAXTree or equivalent) as input
- Addresses interactive web tasks (not just static page analysis)
- Reports some quantitative performance metric

### 5.3 Exclusion Criteria

A paper is excluded if ANY of:
- Uses only screenshots, HTML, or raw DOM (no accessibility tree)
- Pre-2023 publication
- No quantitative results
- Accessibility tree is mentioned but not used as primary observation

## 6. Data Extraction

For each included paper, extract:

### 6.1 Paper Metadata
- Title, authors, year, venue
- Task type (navigation, form filling, information extraction, etc.)
- Number of sites/tasks tested
- Whether tasks span multiple sites (cross-site evidence)

### 6.2 Accessibility Tree Usage
- Which accessibility tree API: getFullAXTree, getAccessibilityTree, other
- What properties are extracted: role, name, state, bounding box, relationships
- How the tree is structured/processed (raw, pruned, flattened, hierarchical)
- Whether current_viewport_only filtering is applied

### 6.3 Element Matching Strategy
- Classification: role-based, name-based, embedding-based, LLM-based, hybrid
- Whether matching is structured (algorithmic) or unstructured (LLM reasoning)
- Whether matches are reusable across sites or site-specific
- Whether the approach handles dynamic state changes

### 6.4 Cross-Site Evidence
- Does the paper test across multiple sites?
- What is the element matching accuracy (if reported)?
- Is the accuracy reported per-site or aggregate?
- Does the paper explicitly claim cross-site generalization?

### 6.5 Relevance to SPIDER
- Can the element-matching approach be adapted for fragment extraction?
- What transformation would be required to map from their representation to SPIDER's Observation.state?
- Does the approach preserve enough structure for SPIDER's Mechanism model (preconditions, postconditions, parameter slots)?

## 7. Classification Taxonomy

### 7.1 Element Matching Strategy Types

| Type | Description | Example |
|------|-------------|---------|
| ROLE-NAME | Match by ARIA role + accessible name | "button[name='Submit']" |
| ROLE-STATE | Match by role + state (focused, expanded, etc.) | "textbox[focused=True]" |
| EMBEDDING | Embed element text/properties, match by cosine similarity | Sentence-BERT on element text |
| LLM | Use LLM to identify/select elements | GPT-4 with element descriptions |
| HYBRID | Combine structured + LLM approaches | Role-name with LLM fallback |
| SITE-SPECIFIC | Hardcoded selectors per site | CSS selectors, XPath |

### 7.2 Cross-Site Evidence Levels

| Level | Description |
|-------|-------------|
| NONE | No cross-site testing |
| WITHIN-DOMAIN | Tests across sites of same type (e.g., multiple e-commerce) |
| CROSS-DOMAIN | Tests across different site types |
| PROVEN-TRANSFER | Explicitly demonstrates transfer to unseen sites |

## 8. Controls

### 8.1 Positive Control
At least one paper must use accessibility trees with structured (not pure LLM) element matching and report cross-site or cross-environment results. If no paper meets this, the survey is in the expected failure region.

### 8.2 Null Control
Papers using HTML, DOM, or screenshots (not accessibility trees) must be correctly excluded. The survey must not inflate counts by including non-accessibility-tree work.

### 8.3 Sensitivity Control
The search must use 3+ independent strategies to avoid missing relevant work. If all papers are found via a single strategy, the survey may be biased.

## 9. Measurement Validity

### 9.1 Representation Loss
- Literature surveys are inherently incomplete; we cannot guarantee all relevant papers are found
- Mitigation: multiple search strategies, forward/backward citation, known research groups
- The survey reports what was found, not a claim of exhaustive coverage

### 9.2 Classification Ambiguity
- Some papers may use hybrid approaches that don't fit neatly into one category
- Mitigation: classify by primary approach, note hybrid nature in extraction

### 9.3 Metric Heterogeneity
- Different papers report different metrics (accuracy, success rate, F1, etc.)
- Mitigation: extract the primary metric used, note when metrics are not comparable

### 9.4 Publication Bias
- Published papers may overrepresent successful approaches
- Mitigation: note this limitation; negative results in the survey are valuable

## 10. Validity Threats

### 10.1 Search Coverage
With 3+ search strategies and citation tracking, we expect to find most high-impact papers. However, very recent (2026) or very niche papers may be missed. This is a completeness threat, not a validity threat.

### 10.2 Recency
Papers from 2023-2026 are selected to capture current methods. Earlier work may have relevant findings but uses older accessibility tree APIs or browser versions.

### 10.3 Relevance Assessment
The relevance criterion (can it be adapted for SPIDER?) is subjective. Mitigation: use explicit criteria (structured matching, cross-site evidence, adaptability) and document reasoning for each paper.

### 10.4 Cross-Site Definition
"Cross-site" is defined as testing on sites not used for training/development. Some papers may test on sites from the same domain (e.g., multiple Wikipedia pages) which is not true cross-site transfer. Mitigation: distinguish within-domain vs cross-domain vs proven-transfer in extraction.

## 11. Decision Rules

### 11.1 SUPPORTS
If ALL of:
1. >= 3 papers demonstrate structured element matching from accessibility trees
2. At least 1 paper demonstrates cross-domain transfer (different site types)
3. At least 1 paper reports element matching accuracy > 70% on cross-site tasks
4. The matching approach is algorithmic (not pure LLM reasoning)

### 11.2 PARTIALLY_SUPPORTS
If:
1. 1-2 papers demonstrate structured element matching from accessibility trees with cross-site evidence, OR
2. >= 3 papers demonstrate structured matching but only within-domain, OR
3. >= 3 papers demonstrate cross-site matching but accuracy < 70%

### 11.3 DOES_NOT_SUPPORT
If:
1. 0 papers demonstrate structured element matching from accessibility trees with cross-site evidence, OR
2. All surveyed papers use site-specific selectors or pure LLM matching, OR
3. No paper reports cross-site element matching accuracy > 70%

### 11.4 MEASUREMENT_INVALID
If:
1. Search infrastructure fails (no access to academic databases)
2. Fewer than 5 papers are found meeting inclusion criteria (insufficient evidence base)

## 12. Expected Outcomes

### 12.1 SUPPORTS
If existing work provides reusable patterns, the graph lane should:
- Identify the most promising matching approach for adaptation
- Estimate transformation cost from WebArena's accessibility tree to adapted approach
- Proceed with integration experiment using adapted patterns (lower risk)
- C-CROSSSITE moves toward EXPERIMENTAL

### 12.2 PARTIALLY_SUPPORTS
If partial evidence exists, the graph lane should:
- Combine multiple partial approaches into a hybrid strategy
- Accept higher integration risk but with informed design choices
- Consider whether the available patterns justify the 812-task corpus expansion
- C-CROSSSITE remains HYPOTHESIS with narrowed unknowns

### 12.3 DOES_NOT_SUPPORT
If no reusable patterns exist, the graph lane should:
- Accept that fragment extraction is a genuinely novel requirement
- Decide whether to build from scratch (higher cost) or accept 2-site corpus (lower cost)
- Consider whether VisualWebArena or other benchmarks offer lower transformation cost
- C-CROSSSITE remains HYPOTHESIS with the additional unknown: "Can novel fragment extraction be built?"

## 13. Analysis Plan

1. **Search execution**: Run all 4 search strategies, collect candidate papers
2. **Deduplication**: Remove duplicates across strategies
3. **Screening**: Apply inclusion/exclusion criteria
4. **Data extraction**: For each included paper, extract structured metadata per Section 6
5. **Classification**: Classify element matching strategy and cross-site evidence level
6. **Assessment**: For each paper, assess relevance to SPIDER's problem
7. **Synthesis**: Build evidence matrix, compute summary statistics
8. **Decision**: Apply decision rules from Section 11
9. **Reporting**: Structured report with per-paper findings and overall verdict

## 14. Analysis Artifacts

- `survey_results.json`: Structured extraction per paper
- `evidence_matrix.md`: Cross-tabulation of papers vs capabilities
- `relevance_assessment.md`: Per-paper assessment of SPIDER adaptability
- This preregistration and spec.json

## 15. Deviation Policy

Any deviation from this preregistration (e.g., expanding scope, changing inclusion criteria) will be labeled EXPLORATORY and cannot support confirmatory claims about C-CROSSSITE. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any literature search is conducted or any papers are read. The survey will be executed exactly as described here.
