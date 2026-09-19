# EXP-INTEL-35445596324 — Preregistration

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35445596324
- **Lane**: intel
- **Parent**: EXP-INTEL-35434771791 (MIXED verdict, C4 FAIL)
- **Claims**: C-MEAS-VALID (indirectly, through measurement substrate quality)

## Question

Is the OECD/COINr pipeline's ranking instability under recipe sampling a sample-size artifact of the truncated-first-20 locatable_sample, or is the instability structural?

## Background

The parent experiment (EXP-INTEL-35434771791) established that the OECD/COINr pipeline preserves between-type discrimination (eta2 0.964-0.999) but ranking preservation fails under recipe sampling: canonical recipe iterations show only 58%/48% agreement for tag_entropy. The audit (VF1) identified this as the critical unresolved issue.

The raw data contains `locatable_sample` truncated to 20 elements per task, but the full locatable count ranges from 21-82 per task. The hypothesis is that with only 20 elements and 5-8 matching a given definition, recipe sampling (which subsets roles with p=0.5) has too few matching elements to稳定ly capture the discriminative signal.

## Design

### Effective Sample Size Analysis

For each effective sample size n ∈ {5, 10, 15, 20}:
1. Use the first n elements from each task's locatable_sample (ordered by DOM position)
2. Compute feature-weighted density for 3 features × 2 non-degenerate definitions
3. Compute eta2 on page_type
4. Compute ranking agreement (listing > detail for tag_entropy; detail > listing for form_fraction/total_area)

### Recipe Sampling at Each Effective_n

For each effective_n:
- **Canonical recipe**: shared subset p=0.5, 10 seeds × 1000 iterations
- **Per-task recipe**: independent p=0.5 per task, 10 seeds × 1000 iterations
- This replicates parent protocol at each sample size

### Bootstrap Resampling

At each effective_n:
- B=1000 bootstrap resamples of tasks within each page_type (with replacement)
- Compute ranking agreement per bootstrap
- Report mean ± std of ranking agreement

### Definitions (same as parent)

- **DEF-FULL-MAP**: interactive_roles = {button, link, textbox, checkbox, radio, combobox, listbox, menuitem, tab, slider, spinbutton, searchbox, switch}; role_map = {a: link, input: textbox}
- **DEF-FORM-ONLY**: interactive_roles = {button, textbox, checkbox, radio, combobox, listbox, slider, spinbutton, searchbox, switch}; role_map = {}
- **ISOLATED-A-LINK**: interactive_roles = {link}; role_map = {} — expected degenerate zero, excluded from primary analysis

### Features (same as parent)

- **tag_entropy**: Shannon entropy of tag distribution at each element position
- **form_fraction**: Binary inForm flag (1.0 if in form, 0.0 otherwise)
- **total_area**: Bounding box area (w × h) at each element position

### Baselines

| ID | Description | Source |
|----|-------------|--------|
| B1 | Canonical recipe agreement: tag_entropy × DEF-FULL-MAP 58%, × DEF-FORM-ONLY 48% | Parent audit VF1 |
| B2 | Non-recipe ranking: tag_entropy preserves for both definitions (100%) | Parent M7 |
| B3 | Pipeline eta2: 0.964-0.999 for DEF-FULL-MAP and DEF-FORM-ONLY | Parent M1 |

### Controls

| ID | Type | Expected |
|----|------|----------|
| PC1 | Positive | Raw feature eta2=1.0 on page_type |
| NC1 | Null | Normalized hierarchy eta2 < 0.01 |

## Decision Rules (frozen before execution)

### C1: Raw Features Reproduce
- **Condition**: All three direct features achieve eta2 ≥ 0.99 on page_type, within-type std < 0.001
- **PASS**: All three pass
- **FAIL**: Any eta2 < 0.99
- **Consequence of FAIL**: MEASUREMENT_INVALID

### C2: Hierarchy Normalized Reproduces
- **Condition**: Normalized hierarchy density eta2 < 0.01 on page_type
- **PASS**: eta2 < 0.01
- **FAIL**: eta2 ≥ 0.01
- **Consequence of FAIL**: MEASUREMENT_INVALID

### C3: Feature Pipeline Eta2 Nonzero
- **Condition**: At least one feature-weighted density through pipeline at effective_n=20 achieves eta2 ≥ 0.05
- **PASS**: max(eta2) ≥ 0.05
- **FAIL**: All eta2 < 0.05
- **Consequence of FAIL**: FALSIFIES — pipeline collapses all discrimination

### C4: Natural Ranking Preserved
- **Condition**: At effective_n=20, non-recipe pipeline preserves listing > detail for tag_entropy (both definitions)
- **PASS**: ≥ 1 feature preserves ranking for both definitions
- **FAIL**: All features have at least one definition that reverses listing-vs-detail
- **Consequence of FAIL**: MIXED — pipeline discriminates but doesn't preserve natural ranking

### C5: Sample Size Effect
- **Condition**: (a) Spearman correlation between effective_n ∈ {5,10,15,20} and ranking agreement ≥ 0.6; AND (b) agreement at n=20 ≥ agreement at n=5 + 0.10
- **PASS**: Both (a) and (b) hold
- **FAIL**: Either fails
- **Consequence of FAIL**: MIXED — instability is structural, not sample-size-dependent

### C6: Ranking Stability at Full Effective_n
- **Condition**: At effective_n=20, canonical recipe ranking agreement for tag_entropy × DEF-FULL-MAP ≥ 80%
- **PASS**: agreement ≥ 0.80
- **FAIL**: agreement < 0.80
- **Consequence of FAIL**: MIXED — partial improvement, full-DOM testing still needed

### Verdict Matrix

| C1 | C2 | C3 | C4 | C5 | C6 | Verdict |
|----|----|----|----|----|----|---------| 
| FAIL | — | — | — | — | — | MEASUREMENT_INVALID |
| — | FAIL | — | — | — | — | MEASUREMENT_INVALID |
| PASS | PASS | FAIL | — | — | — | FALSIFIES |
| PASS | PASS | PASS | FAIL | — | — | MIXED (ranking not preserved) |
| PASS | PASS | PASS | PASS | FAIL | — | MIXED (structural instability) |
| PASS | PASS | PASS | PASS | PASS | FAIL | MIXED (partial improvement) |
| PASS | PASS | PASS | PASS | PASS | PASS | SURVIVES |

## Product Consequences

### If SURVIVES (C5 AND C6 PASS)
- Ranking instability was a sample-size artifact
- MIXED program unblocked with feature-weighted density
- Product lane can use tag_entropy-weighted density with canonical recipe
- The 31x recipe material gap becomes actionable

### If MIXED (C5 FAIL or C6 FAIL)
- Ranking instability is structural or incompletely resolved
- Product lane must use non-recipe density (100% ranking agreement, but eta2 0.92-0.74)
- Full DOM testing (n=21-82) still warranted as final check
- Do not promote recipe-based density to Product Core

### If FALSIFIES (C3 FAIL)
- Pipeline collapses all feature-based discrimination at full effective_n
- Density-based MIXED handling abandoned for this sample/site
- Product lane pivots to non-density-based approaches

## Validity Threats

1. **Truncation ceiling**: Raw data contains only truncated-first-20 locatable elements (20 of 21-82 available). This experiment tests within the 20-element range. Full DOM testing (n=21-82) is still needed for definitive answer if n=20 result is borderline.

2. **Within-type template invariance**: Tasks of the same page type share identical element tags/roles/inForm/w/h in the truncated-first-20 sample. High eta2 is trivially achievable; the test is ranking preservation.

3. **Cart n=1 degeneracy**: Cart page_type has n=1 (deduplicated), making within-type variance degenerate. Comparison focuses on listing vs detail (n=3 each).

4. **ISOLATED-A-LINK degenerate**: Zero matching elements on this sample. Analysis limited to DEF-FULL-MAP and DEF-FORM-ONLY (2/3 definitions).

5. **Single Magento site**: Cross-site generalization not tested. Claim ceiling bounded to single site.

6. **Y-proxy hierarchy**: NC1 uses y-coordinate as DOM depth proxy with underflow degeneracy. True DOM depth effect not tested.

## Analysis Code

Based on parent analyze.py (sha256: 5edc1bddc960cc7f8ef5048bdb39551244d912619c166b30bb12a7fc4bfc2490), modified to:
1. Add effective_n subsampling loop (n ∈ {5, 10, 15, 20})
2. Add bootstrap resampling (B=1000) at each effective_n
3. Add per-task recipe execution (independent p=0.5 per task)
4. Add Spearman correlation test for sample-size effect (C5)
5. Add ranking agreement extrapolation to effective_n=20

## Raw Evidence

- Source: EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json
- SHA256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050
- 7 successful tasks (3 listing, 3 detail, 1 cart), truncated-first-20 locatable_sample
