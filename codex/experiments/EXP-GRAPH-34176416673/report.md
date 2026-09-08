# EXP-GRAPH-34176416673 Report

## Executive Summary

**Status**: BLOCKED  
**Outcome**: NOT_APPLICABLE  

The parameter-slot-count fix is **not committed** to production HEAD. The prerequisite for this experiment (fix committed) is not met. The experiment cannot proceed to its primary goal: testing whether the fix survives commitment and eliminates the false-accept hazard in committed code.

However, we successfully executed **baseline preservation checks** and **null control** (hazard existence verification) using the unfixed HEAD. All baselines pass, confirming no regression. The null control confirms the hazard persists without the fix: literal wins at equal confidence due to insertion-order tie-break.

## 1. Fix Verification

- **Kernel sha256**: `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`
- **Expected unfixed sha256**: `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`
- **Fix committed**: `False`
- **Line 112 content**: `candidates.sort(key=lambda m: m.confidence, reverse=True)`
- **Fix line present**: `False`

The fix (`candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`) is **not present** in the current HEAD. All measurements are therefore on unfixed code.

## 2. Baseline Preservation

All 6 baseline conditions pass with no regression:

| Baseline | Expected | Observed | Pass |
|----------|----------|----------|------|
| B_COLD | UNKNOWN | UNKNOWN | ✅ |
| B_LITERAL_ONLY_ORIG | EXECUTABLE, /posts/1, id=1 | EXECUTABLE, /posts/1, id=1 | ✅ |
| B_LITERAL_ONLY_UNSEEN | EXECUTABLE, /posts/1 (literal universal), id=1 | EXECUTABLE, /posts/1, id=1 | ✅ |
| B_PARAM_ONLY_ORIG | EXECUTABLE, /posts/1, id=1 | EXECUTABLE, /posts/1, id=1 | ✅ |
| B_PARAM_ONLY_UNSEEN | EXECUTABLE, /posts/7 (param generalizes), id=7 | EXECUTABLE, /posts/7, id=7 | ✅ |
| B_CONFIDENCE_PARAM_HIGHER | EXECUTABLE, param (0.98) wins, id=7 | EXECUTABLE, param-fetch-posts-high, id=7 | ✅ |

**Baseline pass rate**: 6/6 (100%)

## 3. Null Control (Hazard Existence)

**C_COMPETE_EQUAL_HEAD**: Without fix, compete-equal (literal 0.95 vs param 0.95, literal registered before param) resolves to **literal-fetch-posts-1** for unseen id=7.

- **Expected**: literal wins (false accept)
- **Observed**: literal wins, bound URL `/posts/1`, HTTP response id=1
- **Pass**: ✅

This confirms the hazard exists in unfixed HEAD: at equal confidence, literal beats param due to insertion-order tie-break, causing a false accept (id=7 resolves to id=1 endpoint).

## 4. Additional Exploratory Tests

We tested compete-equal without fix for unseen ids 2-6. All resolve to literal (false accept):

- id=2: literal-fetch-posts-1, /posts/1, id=1
- id=3: literal-fetch-posts-1, /posts/1, id=1
- id=4: literal-fetch-posts-1, /posts/1, id=1
- id=5: literal-fetch-posts-1, /posts/1, id=1
- id=6: literal-fetch-posts-1, /posts/1, id=1

The hazard is consistent across all unseen ids tested.

## 5. Network and Execution

- **Network failures**: 0
- **Exceptions**: 0
- **Total conditions**: 12 (6 baselines + 1 null control + 5 exploratory)
- **Conditions with correct status**: 12/12

All HTTP requests succeeded with status 200. jsonplaceholder.typicode.com is reachable and endpoints exist for ids 1-7.

## 6. Decision Rule Assessment

Per frozen spec.json decision rules:

- **SURVIVES_POST_COMMIT**: NOT APPLICABLE (fix not committed)
- **FALSIFIED_POST_COMMIT**: NOT APPLICABLE (fix not committed)
- **MEASUREMENT_INVALID**: NO (all measurements valid)
- **BLOCKED**: YES (fix not committed to production HEAD)

**Verdict**: BLOCKED. The prerequisite (fix committed) is not met. The experiment cannot answer its primary question.

## 7. Implications

### For Next Steps

1. **Commit fix to production HEAD**: The one-line fix (`candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`) must be committed to `src/spider/kernel.py` L112 with Director approval.
2. **Re-validate in committed HEAD**: After commit, re-run this experiment (without monkey-patching) to confirm:
   - Fix survives commitment
   - Core hazard eliminated for unseen ids 2-7
   - All baselines preserve
   - No regression
3. **Advance to real-web testing**: After post-commit validation, test generalization to real-web endpoints with DOM, auth, session state, drift.

### For Product Promotion

Product promotion remains **blocked** until the fix is committed and re-validated. The current unfixed HEAD does not meet the safety requirement for production use.

## 8. Limitations

1. **Fix not committed**: Primary experiment cannot proceed.
2. **Simple REST endpoint**: jsonplaceholder is not complex Web; claim ceiling is narrow.
3. **No model calls**: LLM distillation half of C-PARAM-INHERIT not tested.
4. **Empty preconditions**: All mechanisms tested with preconditions={}; non-empty preconditions untested.
5. **Single template shape**: Only URL-embedded `${id}` substitution tested.

## 9. Conclusion

The experiment is BLOCKED due to prerequisite not met. However, the baseline and null control measurements provide valuable diagnostic information:

- **No regression**: All baselines pass on unfixed HEAD.
- **Hazard confirmed**: Literal beats param at equal confidence without fix, for all unseen ids tested.
- **Network stable**: jsonplaceholder reachable, no failures.

The next action is to commit the fix to production HEAD and re-run this experiment to answer the primary question: does the fix survive commitment and eliminate the hazard?

---

**Experiment ID**: EXP-GRAPH-34176416673  
**Lane**: Graph  
**Date**: 2026-09-08  
**Status**: BLOCKED  
**Outcome**: NOT_APPLICABLE