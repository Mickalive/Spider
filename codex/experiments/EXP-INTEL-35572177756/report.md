# Report: EXP-INTEL-35572177756 — Full-DOM Ranking Stability Test

## Experiment Summary

**Question:** Is the ranking instability under recipe sampling (canonical agreement 55.95% at truncated-first-20) a truncation artifact, or does it persist on full DOM elements (n=21-82 per task)?

**Hypothesis:** The ranking instability is a truncation artifact. Full DOM samples contain richer element diversity with more discriminative elements per definition, enabling canonical recipe sampling to capture a more representative subset.

**Falsifier:** The hypothesis is falsified if canonical recipe ranking agreement for tag_entropy × DEF-FULL-MAP on full DOM is < 75% (F1) OR does NOT exceed truncated-first-20 agreement by ≥5 percentage points (F2).

## Execution

1. **Docker availability:** Image `am1n3e/webarena-verified-shopping:latest` pulled successfully (sha256: 3e8cb9b9...). Container started on port 8080, health check HTTP 200.
2. **Full-DOM data collection:** Playwright automation collected ALL elements with bbox for 7 tasks (3 listing, 3 detail, 1 cart). Locatable_sample lengths match locatable_elements (82,82,82,32,32,32,21). C3 gate passes (7/7 tasks >20).
3. **Analysis:** Applied frozen decision rule C1-C7 from EXP-INTEL-35462974425 on full DOM data.

## Key Results

| Metric | Truncated-first-20 | Full DOM | Delta |
|--------|-------------------|----------|-------|
| Canonical recipe agreement (tag_entropy × DEF-FULL-MAP) | 55.95% | **37.26%** | -18.69pp |
| Per-task recipe agreement | 78.65% | **11.41%** | -67.24pp |
| Pipeline eta2 (max) | 0.9996 | 0.99996 | +0.00036 |

## Decision Rule Evaluation

- **C1 (PC1):** PASS — all three raw features achieve eta2 = 1.0 on page_type with full DOM.
- **C2 (NC1):** PASS — normalized hierarchy density eta2 = 0.0.
- **C3 (full DOM available):** PASS — 7/7 tasks have locatable_sample >20.
- **C4 (pipeline eta2 ≥ 0.05):** PASS — max eta2 = 0.99996.
- **C5 (full DOM > truncated+5pp):** **FAIL** — full DOM agreement 37.26% < 60.95% threshold.
- **C6 (canonical ≥ 75%):** **FAIL** — 37.26% < 75%.
- **C7 (per-task ≥ 85%):** **FAIL** — 11.41% < 85%.

**Overall verdict:** FALSIFIES — the ranking instability is NOT a truncation artifact; it worsens with full DOM elements.

## Interpretation

The hypothesis is decisively falsified. Full DOM elements do NOT improve ranking stability; they degrade it. The canonical recipe agreement drops from 55.95% to 37.26% (−18.69pp), and per-task recipe agreement collapses from 78.65% to 11.41% (−67.24pp). The ranking instability is structural, not truncation-dependent.

**Mechanism:** Additional DOM elements likely introduce noise that disrupts recipe sampling stability. The extra elements are not discriminative for page-type ranking; instead, they dilute the signal from the original 20 most informative elements. This suggests the original truncated-first-20 subsample accidentally captured a relatively stable subset.

**Product consequence:** Recipe density is NOT viable for MIXED handling. The product lane must use non-recipe density only (which preserves ranking at 100% per B3) and accept the eta2 reduction from recipe sampling. The 31× recipe material gap (EXP-INTEL-35264637598) remains actionable only with non-recipe density.

## Validity

- Docker container verified healthy (HTTP 200).
- Full-DOM collection confirmed via Playwright automation.
- Frozen decision rule applied without modification.
- Bootstrap CI degenerate [0.0, 1.0] due to binary ranking agreement across bootstraps (only 7 tasks).
- Cross-site generalization unknown (single Magento site).
- Definition sensitivity: DEF-FORM-ONLY canonical agreement 49.37% (still below truncated baseline 49.34%).

## Artifacts

- Raw full-DOM data: `raw_evidence/exp355_fulldom_raw_results.json` (sha256: e81f4c4e...)
- Analysis output: `analysis_output.json` (sha256: 5f1ad2ff...)
- Collection script: `collect_fulldom.py` (sha256: f8e86315...)
- Analysis script: `analyze_fulldom.py` (sha256: ed81d9ff...)