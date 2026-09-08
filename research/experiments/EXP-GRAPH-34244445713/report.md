# EXP-GRAPH-34244445713 — Execution Report

## Status: BLOCKED

**Outcome**: NOT_APPLICABLE — The parameter-slot-count tie-break fix is not present in committed production HEAD. The experiment's primary gate (fix presence verification) failed, making the post-commit question unanswerable from this run.

## Summary

| Metric | Value |
|--------|-------|
| Fix committed | **NO** |
| Baseline pass rate | 6/6 (1.0) |
| Hazard elimination rate | 0/6 (0.0) |
| Null control pass | true |
| Exceptions | 0 |
| Network failures | 0 |
| Total conditions | 13 |

## Fix Verification

The frozen design required verifying that `src/spider/kernel.py` L112 contains the parameter-slot-count fix:

```python
# Expected (fixed):
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)

# Actual (unfixed):
candidates.sort(key=lambda m: m.confidence, reverse=True)
```

**The fix is NOT present.** The kernel file sha256 is `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`, matching the parent experiment's evidence. Git log confirms the last kernel change was commit `1e6f32b` ("r2: bind parameters safely inside action templates"), which is unrelated to the tie-break fix.

Per the frozen decision rule: **BLOCKED** — fix not present in committed HEAD (gate 1 of 6 not met).

## Baseline Results (6/6 Pass)

All 6 baseline conditions pass on unfixed HEAD, confirming no regression from the parent experiment:

| Condition | Status | URL | HTTP | Pass |
|-----------|--------|-----|------|------|
| B-COLD | UNKNOWN | N/A | N/A | ✓ |
| B-LITERAL-ONLY-ORIG | EXECUTABLE | /posts/1 | 200 | ✓ |
| B-LITERAL-ONLY-UNSEEN | EXECUTABLE | /posts/1 | 200 | ✓ |
| B-PARAM-ONLY-ORIG | EXECUTABLE | /posts/1 | 200 | ✓ |
| B-PARAM-ONLY-UNSEEN | EXECUTABLE | /posts/7 | 200 | ✓ |
| B-COMPETE-PARAM-HIGHER | EXECUTABLE | /posts/7 | 200 | ✓ |

Key observations:
- **Literal does not generalize**: B-LITERAL-ONLY-UNSEEN resolves to `/posts/1` for unseen id=7 (literal template, no parameter binding)
- **Param generalizes**: B-PARAM-ONLY-UNSEEN resolves to `/posts/7` for unseen id=7 via `${id}` template binding
- **Confidence ordering works**: B-COMPETE-PARAM-HIGHER resolves to param when param confidence (0.98) exceeds literal (0.95)

## Core Hazard Results (0/6 Param Wins — Hazard Persists)

All 6 equal-confidence conditions (literal 0.95 vs param 0.95, literal registered first) resolve to **literal**, not param. The hazard persists on unfixed HEAD:

| Condition | Expected | Observed | URL | HTTP | Pass |
|-----------|----------|----------|-----|------|------|
| C-EQUAL-ID2 | param | literal | /posts/1 | 200 | ✗ |
| C-EQUAL-ID3 | param | literal | /posts/1 | 200 | ✗ |
| C-EQUAL-ID4 | param | literal | /posts/1 | 200 | ✗ |
| C-EQUAL-ID5 | param | literal | /posts/1 | 200 | ✗ |
| C-EQUAL-ID6 | param | literal | /posts/1 | 200 | ✗ |
| C-EQUAL-ID7 | param | literal | /posts/1 | 200 | ✗ |

**Interpretation**: Without the fix, the sort key is only `m.confidence`. When confidences are equal (0.95 == 0.95), Python's `sorted()` is stable and preserves insertion order. Since literal is registered before param (worst-case), literal wins the tie-break for every unseen id. This is exactly what the parent experiment found.

**This does NOT falsify the fix** — it confirms the hazard persists on unfixed HEAD, which is the expected prerequisite state. The fix must be committed before the hazard test becomes meaningful.

## Null Control (1/1 Pass)

B-CONFIDENCE-LITERAL-HIGHER: literal (0.98) vs param (0.95) for unseen id=7. Literal wins as expected. Strict confidence ordering is preserved. The fix (when committed) would not override this because the primary sort key is confidence, and 0.98 > 0.95 regardless of parameter_slots.

## Interpretation

This experiment is BLOCKED, not FALSIFIED. The distinction matters:

- **BLOCKED** = prerequisite not met (fix not committed). The experiment cannot answer its question. No scientific conclusion about the fix's effectiveness can be drawn.
- **FALSIFIED** = prerequisite met but the fix doesn't work. This would require the fix to be present and the hazard to persist.

The hazard test results (0/6 param wins) are diagnostic evidence that:
1. The hazard is systematic across all tested unseen ids (2-7), not just id=7
2. The hazard mechanism is insertion-order tie-breaking (literal registered first always wins)
3. The baseline behavior is stable between this experiment and the parent experiment

## Next Action

The single blocking action remains: **commit the one-line fix to `src/spider/kernel.py` L112** with Director approval:

```python
# Change L112 from:
candidates.sort(key=lambda m: m.confidence, reverse=True)
# To:
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
```

After commit, re-run this exact experiment (EXP-GRAPH-34244445713 or a successor) to:
1. Confirm fix survives commitment
2. Verify hazard elimination for all unseen ids 2-7
3. Confirm baseline preservation
4. Confirm confidence ordering preservation
5. Advance C-PARAM-INHERIT to real-web testing

## Claim Ceiling

This experiment does not advance C-PARAM-INHERIT beyond its current ceiling (EXPERIMENTAL, BLOCKED). The claim ceiling remains bounded to:
- Single intent (fetch-post)
- Single endpoint (jsonplaceholder /posts/{id})
- Preconditions = {}
- Deterministic n=1
- Simple REST (no DOM, auth, session state, drift)
