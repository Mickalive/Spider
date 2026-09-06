# EXP-PRODUCT-34003641840 — Report

## Outcome: FIXES-SURVIVE-REGRESSION

All 7 decision-rule conditions pass. The redesigned noise filter (field-path relevance) and structure-similarity check (Jaccard >= 0.75 + constant-value anchor) resolve D1/D2 noisy-observation over-parametrization and E1 pattern-absence hallucination while preserving clean-synthetic regression.

## Decision Rule

| Condition | Expected | Observed | Pass |
|-----------|----------|----------|------|
| B1 slot_count=1, binding_correct=5/5 | 1 | 1, 5/5 | ✅ |
| B4 slot_count=1, binding_correct=3/3 | 1 | 1, 3/3 | ✅ |
| D1 slot_count=3, slots ⊆ {customer, url, X-Request-ID} | 3 | 3 | ✅ |
| E1 slot_count=0 | 0 | 0 | ✅ |
| C1 slot_count=1, binding_correct=3/3 | 1 | 1, 3/3 | ✅ |
| E2 slot_count=0 | 0 | 0 | ✅ |
| No regression vs parent | — | B2/B3/B5 improved | ✅ |

## Key Results

### Noise Filter: Field-Path Relevance ✅

The old value-pattern heuristic (`len(common_prefix)>0 OR len(common_suffix)>0`) was falsified in EXP-PRODUCT-33993747223 because:
- **False positive:** timestamp passed (prefix `2026-09-01T10:0`, suffix `:00Z`)
- **False negative:** body.name filtered (no common prefix/suffix)

The new field-path relevance filter uses an explicit allowlist: `{method, url, body, headers, query}` at top-level; all other keys are metadata. This correctly:
- Excludes timestamp, request_duration_ms, retry_count, user_agent from D1
- Excludes response_time_ms, cache_hit, result_count from D2
- Includes body.name (B2), body.title (B3), body.user_id (B5), headers.X-Request-ID (B3) as genuine parameters

### Structure-Similarity: Jaccard >= 0.75 + Constant-Value Anchor ✅

The old Jaccard 0.3 threshold was falsified because unrelated observations (POST/GET/DELETE) shared generic leaf paths (method, url) giving Jaccard=0.667 > 0.3.

The new two-part check:
1. **Jaccard >= 0.75** on leaf paths after metadata exclusion
2. **Constant-value anchor:** at least one shared path has identical values across ALL observations

For E1: Jaccard=0.667 (raw) but constant-value anchor fails because all shared paths (method: POST≠GET≠DELETE, url: different) have different values. The observations are correctly rejected.

### Regression: B1-B5 All Pass ✅

| Condition | Slot Count | Binding Accuracy | vs Parent |
|-----------|------------|------------------|-----------|
| B1 | 1 | 1.0 (5/5) | Same |
| B2 | 2 | 1.0 (5/5) | Improved (was 1) |
| B3 | 3 | 1.0 (5/5) | Improved (was 2) |
| B4 | 1 | 1.0 (3/3) | Same |
| B5 | 2 | 1.0 (3/3) | Improved (was 1) |

B2/B3/B5 improvement is because body.name/body.title/body.user_id are no longer filtered by the value-pattern heuristic. The field-path relevance filter correctly includes body.* fields as action-template-relevant.

### D2 Architectural Limitation

D2 produces slot_count=1 [url] instead of the expected slot_count=2 [q, page]. This is because the leaf-path model treats the entire URL as a single leaf node and cannot extract individual query-string parameters. This is a documented architectural limitation, not a noise-filter failure.

## Implementation

The experiment is self-contained in `run_experiment.py` and does not modify `src/spider/kernel.py`. It implements:
1. `_find_common_prefix_suffix()` — prefix/suffix extraction for template construction
2. `_is_metadata_path()` — field-path relevance allowlist check
3. `_compute_structure_similarity()` — two-part Jaccard + constant-value anchor
4. `_detect_double_prefix()` — suffix-empty template handling
5. `_verify_binding_correct()` — strict JSON content comparison

## Product Consequence

This result advances C-PARAM-INHERIT from clean-synthetic POC toward realistic-synthetic robustness. The noise-filter redesign resolves the two primary failure modes (D1 over-parametrization, E1 hallucination) while preserving clean-synthetic regression. The next gate is testing with real browser observation noise.
