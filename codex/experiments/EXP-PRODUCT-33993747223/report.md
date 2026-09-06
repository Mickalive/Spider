# EXP-PRODUCT-33993747223 Report

## Executive Summary

**Status**: COMPLETE  
**Outcome**: FALSIFIES  
**Decision**: FIXES-FALSIFIED

The three algorithmic fixes applied to `distill_parameterized()` in `src/spider/kernel.py` do NOT survive regression on clean synthetic inputs. Fix A (double-prefix detection) works correctly, but Fix B (noise-filter heuristic) introduces regression by filtering genuine varying fields, and Fix C (structure-similarity check) has an insufficient threshold.

## Key Findings

### Fix A: Double-Prefix Detection — WORKS ✓

The double-prefix detection in `_bind()` correctly handles full-value unseen parameters:

- **C1 (full-value URLs)**: `https://site-d.com/hook` resolves to correct `bound_action` without double-prefix error. `3/3 EXECUTABLE`, `3/3 binding correct`.
- **C2 (full-value IDs)**: `user-4` resolves correctly. `3/3 EXECUTABLE`, `3/3 binding correct`.

The detection logic (`prefix + param_value + suffix == param_value → use param_value directly`) is correct and deterministic.

### Fix B: Noise-Field Filtering — FAILS ✗

The pre-registered noise-filter criterion (`len(common_prefix) > 0 OR len(common_suffix) > 0`) is insufficient:

**Problem 1: False positives (noise passes filter)**
- `timestamp` values (`2026-09-01T10:00:00Z`, `2026-09-01T10:01:00Z`, `2026-09-01T10:02:00Z`) have common prefix `2026-09-01T10:0` and suffix `:00Z`, so they pass the filter.
- D1 produces 4 slots (including `timestamp`) instead of expected 3.

**Problem 2: False negatives (genuine parameters filtered)**
- `body.name` values (`Alice`, `Bob`, `Charlie`) have no common prefix or suffix, so they are filtered out.
- B2 produces 1 slot (only `url`) instead of expected 2 (missing `name`).
- B3 produces 2 slots instead of expected 3 (missing `title`).
- B5 produces 1 slot instead of expected 2 (missing `user_id`).

**Impact**: Regression slot counts are WRONG for B2 (1 vs 2), B3 (2 vs 3), B5 (1 vs 2). Binding accuracy drops to 67% (14/21) vs parent 100% (21/21).

### Fix C: Structure-Similarity Check — FAILS ✗

The pre-registered Jaccard threshold of 0.3 is too low:

- E1 observations (POST /api/payments, GET /api/users/42, DELETE /api/sessions/abc-123) share generic leaf paths (`('method',)`, `('url',)`).
- Pairwise Jaccard: (1,2)=0.5, (1,3)=0.5, (2,3)=1.0 → mean=0.667 > 0.3.
- The structure-similarity check does NOT trigger, and E1 produces 1 slot instead of 0.

## Regression Baseline (B1-B5)

| Condition | Expected Slots | Actual Slots | Executable | Binding Correct | Verdict |
|-----------|---------------|-------------|------------|-----------------|---------|
| B1 (single-path) | 1 | 1 | 5/5 | 5/5 | ✓ PASS |
| B2 (path+body) | 2 | 1 | 5/5 | 0/5 | ✗ FAIL |
| B3 (path+body+headers) | 3 | 2 | 5/5 | 0/5 | ✗ FAIL |
| B4 (non-identifier URLs) | 1 | 1 | 3/3 | 3/3 | ✓ PASS |
| B5 (shared-slot collision) | 2 | 1 | 3/3 | 0/3 | ✗ FAIL |

**Total**: 21/21 executable (100%), 14/21 binding correct (67%) vs parent 21/21 (100%).

## Full-Value Unseen (C1-C2)

| Condition | Slots | Executable | Binding Correct | Double-Prefix Error |
|-----------|-------|------------|-----------------|---------------------|
| C1 (full-value URLs) | 1 | 3/3 | 3/3 | No |
| C2 (full-value IDs) | 1 | 3/3 | 3/3 | No |

## Noisy Browser (D1-D3)

| Condition | Expected Slots | Actual Slots | Noise Fields Included | Signal Fields Filtered |
|-----------|---------------|-------------|----------------------|----------------------|
| D1 (noisy POST) | 3 | 4 | timestamp | body.name |
| D2 (noisy GET) | 2 | 2 | cache_hit | query.page |
| D3 (varying preconditions) | 2 | 1 | — | body.quantity |

## Null Controls (E1-E2)

| Condition | Expected Slots | Actual Slots | Jaccard | Verdict |
|-----------|---------------|-------------|---------|---------|
| E1 (unrelated structures) | 0 | 1 | 0.667 | ✗ FAIL |
| E2 (single observation) | 0 | 0 | N/A | ✓ PASS |

## Decision Rule Application

Per preregistered decision rule:

1. ✓ Kernel integration completes without crashes; existing tests pass
2. ✗ Regression baseline: B2, B3, B5 produce WRONG slot counts and binding accuracy < 100%
3. ✓ Full-value unseen: C1+C2 resolve EXECUTABLE with binding_accuracy = 1.0
4. ✗ Noisy browser: D1 slot_count ≠ expected (4 vs 3); D2 noise filter includes wrong fields
5. ✗ Null control: E1 produces slot_count=1 instead of 0
6. ✓ No crashes or non-deterministic output

**Result**: FIXES-FALSIFIED (condition 2 fails — regression slot counts and binding accuracy don't match parent)

## Root Cause Analysis

The noise-filter heuristic (`len(common_prefix) > 0 OR len(common_suffix) > 0`) is fundamentally flawed because:

1. **Timestamps have structural prefix/suffix**: `2026-09-01T10:0` is a common prefix across timestamp values, so timestamps pass the filter.
2. **Genuine parameters may lack prefix/suffix**: `Alice`, `Bob`, `Charlie` are genuinely varying but share no common prefix/suffix, so they are filtered out.
3. **The heuristic conflates "has pattern" with "is structural"**: A field can have a common prefix/suffix (pattern) without being a meaningful parameter (structural), and vice versa.

## Recommendations

1. **Fix B redesign**: Instead of prefix/suffix heuristic, filter by field path relevance:
   - Only consider fields within action-template-relevant paths (e.g., `body.*`, `headers.*`, `url`)
   - Ignore top-level metadata fields (`timestamp`, `request_duration_ms`, `retry_count`, `user_agent`)
   - This requires understanding the action structure, not just the value patterns

2. **Fix C threshold increase**: Raise Jaccard threshold from 0.3 to >0.7, or use a weighted similarity metric that accounts for:
   - Path depth (deeper paths are more distinctive)
   - Value diversity (fields with diverse values are more indicative of structure)
   - HTTP method differentiation (POST body vs GET query vs DELETE path)

3. **Regression verification**: After fixing B and C, re-run B1-B5 to verify slot counts match parent exactly.

## Consequences

- **C-PARAM-INHERIT** remains blocked on realistic inputs
- The double-prefix fix (Fix A) is validated and can be retained
- Fixes B and C need fundamental redesign before re-testing
- The next experiment should focus on a better noise-filter mechanism and structure-similarity metric
