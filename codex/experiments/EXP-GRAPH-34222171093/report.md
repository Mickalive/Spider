# EXP-GRAPH-34222171093 Report

## Executive Summary

**Status**: BLOCKED  
**Outcome**: NOT_APPLICABLE  

The parameter-slot-count fix is **NOT committed** to production HEAD. The experiment cannot proceed as designed. However, baselines and null control were executed to verify no regression and confirm the hazard persists without the fix.

## Key Findings

1. **Fix Not Committed**: `src/spider/kernel.py` L112 remains unfixed (`candidates.sort(key=lambda m: m.confidence, reverse=True)`). The sha256 matches the known unfixed version (`46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`).

2. **Baseline Regression**: **PASS** (6/6). All baseline conditions behave identically to the parent experiment on unfixed HEAD.

3. **Cold Baseline**: **PASS**. No mechanisms registered → UNKNOWN resolution.

4. **Null Control (B-LITERAL-HIGHER-CONF)**: **PASS**. Literal (0.98) beats param (0.95) for unseen id=7, confirming confidence ordering is not broken.

5. **Core Hazard Test**: **6/6 literal wins** (hazard persists). Without the fix, literal beats param at equal confidence for ALL unseen ids 2-7. This confirms the hazard is systematic and persists in the current HEAD.

## Detailed Results

### Baseline Conditions (6/6 PASS)

| Condition | Expected | Observed | HTTP ID | Pass |
|-----------|----------|----------|---------|------|
| B-COLD | UNKNOWN | UNKNOWN | N/A | ✓ |
| B-LITERAL-ONLY-ORIG | /posts/1 | /posts/1 | 1 | ✓ |
| B-LITERAL-ONLY-UNSEEN | /posts/1 | /posts/1 | 1 | ✓ |
| B-PARAM-ONLY-ORIG | /posts/1 | /posts/1 | 1 | ✓ |
| B-PARAM-ONLY-UNSEEN | /posts/7 | /posts/7 | 7 | ✓ |
| B-COMPETE-PARAM-HIGHER | /posts/7 | /posts/7 | 7 | ✓ |

### Null Control (B-LITERAL-HIGHER-CONF)

- **Expected**: Literal (0.98) wins over param (0.95) for unseen id=7
- **Observed**: `literal-fetch-posts-high` wins, resolves to `/posts/1`, HTTP returns id=1
- **Result**: **PASS** — confidence ordering preserved

### Core Hazard Test (6/6 literal wins — hazard persists)

| ID | Expected (without fix) | Observed Mechanism | HTTP ID | Pass |
|----|------------------------|-------------------|---------|------|
| 2 | Literal wins | `literal-fetch-posts-1` | 1 | ✓ |
| 3 | Literal wins | `literal-fetch-posts-1` | 1 | ✓ |
| 4 | Literal wins | `literal-fetch-posts-1` | 1 | ✓ |
| 5 | Literal wins | `literal-fetch-posts-1` | 1 | ✓ |
| 6 | Literal wins | `literal-fetch-posts-1` | 1 | ✓ |
| 7 | Literal wins | `literal-fetch-posts-1` | 1 | ✓ |

**Hazard Elimination Rate**: 0.0 (0/6 param wins) — hazard persists without fix.

## Interpretation

This experiment is BLOCKED because the prerequisite fix is not committed to production HEAD. The results confirm:

1. **No regression**: All baselines pass identically to the parent experiment.
2. **Hazard persists**: Without the fix, literal wins at equal confidence for ALL unseen ids 2-7 (systematic hazard).
3. **Confidence ordering intact**: The null control confirms that literal (0.98) correctly beats param (0.95) when confidence differs.

The core hazard test results are **EXPLORATORY** in BLOCKED status. They confirm the hazard persists without fix but cannot support confirmatory claims about fix effectiveness.

## Next Steps

1. **Commit the fix** to `src/spider/kernel.py` L112: `candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`
2. **Re-run this experiment** (no monkey-patching) in committed HEAD to confirm:
   - Fix survives commitment
   - Compete-equal resolves to param for ALL unseen ids 2-7
   - All 6 baselines pass
   - B-LITERAL-HIGHER-CONF remains literal-winning
3. **After post-commit validation**, advance to real-web endpoint testing with DOM, auth, session state, drift.

## Validity Threats

1. **Fix Not Committed**: The primary threat. The experiment cannot proceed without the fix.
2. **Monkey-Patch Contamination**: Not applicable — no monkey-patching used.
3. **HTTP Endpoint Unavailability**: jsonplaceholder was reachable for all conditions.
4. **Insertion-Order Assumption**: Literal registered before param in shared-equal conditions (worst case for param).
5. **Single Endpoint, Single Intent**: jsonplaceholder /posts/{id} with fetch-post intent only.
6. **Deterministic n=1**: Each condition run once; no statistical inference needed.

## Claim Ceiling

- **Scope**: jsonplaceholder API, /posts/{id} endpoint, fetch-post intent, preconditions={}, deterministic n=1
- **Mechanism**: parameter_slots count as tie-breaker at equal confidence (NOT TESTED — fix not committed)
- **Limitation**: no real-web endpoints, no DOM, no auth, no session state, no drift, no LLM distillation, no multi-intent, no non-empty preconditions
- **Claim level**: BLOCKED (prerequisite not met)
- **Not established**: fix effectiveness, generalization, robustness, production-readiness
