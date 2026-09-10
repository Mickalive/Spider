# EXP-GRAPH-34320613096 — BLOCKED Execution Report

## Experiment Identity

- **Experiment ID**: EXP-GRAPH-34320613096
- **Lane**: Graph
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-GRAPH-34291967676 (BLOCKED)
- **Status**: BLOCKED (decision rule 9.3)
- **Outcome**: NOT_APPLICABLE (0/14 conditions executed)

## Summary

The parameter-slot-count fix is **not present** in committed HEAD. Line 112 of `src/spider/kernel.py` remains:

```python
candidates.sort(key=lambda m: m.confidence, reverse=True)
```

The expected fix would be:

```python
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
```

Per frozen decision rule 9.3, the experiment is BLOCKED: no conditions executed, no HTTP requests made, no scientific measurement occurred. This is the **third consecutive BLOCKED result** (EXP-GRAPH-34244445713, EXP-GRAPH-34291967676, EXP-GRAPH-34320613096) on the same kernel hash (46929b3a).

## Diagnostic Evidence

### Fix Verification (Gate)
- **L112 content**: `candidates.sort(key=lambda m: m.confidence, reverse=True)`
- **Fix present**: No
- **Kernel sha256**: 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61 (unchanged from parent experiment)
- **Uncommitted changes**: None (clean working tree)

### Git History (kernel.py)
- **Current branch (lab2/graph)**: 2 commits — `r2: bind parameters safely inside action templates` and `r2: add product kernel and experiment transaction tooling` — neither includes the fix
- **All branches**: 14 commits — all are product-lane execute/verdict commits; none include the fix

### Branch Sweep
- **12 branches checked**: lab2/graph, main, lab2/frontier, lab2/intel, lab2/physics, lab2/product, lab2/runtime, research2/bootstrap, research2/codex-unification, research2/hotfix-control-overlay, plus remotes
- **Fix found on**: NONE

### No-Monkey-Patching
- Confirmed: no runtime modification of kernel.py occurred
- Experiment correctly skipped all conditions per BLOCKED decision rule

## Controls

All 14 condition controls correctly show status=`unknown` (skipped). No false negatives or false positives introduced. The BLOCKED gate operated correctly.

| Control | Status | Note |
|---------|--------|------|
| FIX-PRESENCE | **FAIL** | Gate — fix absent |
| B-COLD | unknown | Skipped |
| B-LITERAL-ONLY-ORIG | unknown | Skipped |
| B-LITERAL-ONLY-UNSEEN | unknown | Skipped |
| B-PARAM-ONLY-ORIG | unknown | Skipped |
| B-PARAM-ONLY-UNSEEN | unknown | Skipped |
| B-COMPETE-PARAM-HIGHER | unknown | Skipped |
| C-EQUAL-ID2–ID7 (6) | unknown | Skipped |
| B-CONFIDENCE-LITERAL-HIGHER | unknown | Skipped |
| C-EQUAL-UPSERT-ID7 | unknown | Skipped |
| NO-MONKEY-PATCHING | PASS | No modifications |
| DIAGNOSTIC-GIT-LOG | PASS | Commits captured |
| DIAGNOSTIC-BRANCH-COVERAGE | PASS | All branches checked |

## Interpretation

This experiment produced **no scientific measurement**. The BLOCKED status means the prerequisite (fix committed to production HEAD) remains unmet. The inherited state from the parent handoff is carried forward unchanged:

- **Established**: Core hazard validated on unfixed HEAD (parent), baseline behavior on unfixed HEAD (parent), fix absent across all branches
- **Rejected**: Post-commit hazard elimination claim (cannot test), any scientific falsification of the fix
- **Unknown**: Whether fix survives commitment, whether baselines regress, whether upsert interacts with fix
- **Do Not Assume**: Fix is committed, post-commit behavior matches monkey-patched behavior, production-readiness

### Consecutive BLOCKED Pattern

This is the third consecutive BLOCKED result. The kernel hash has not changed across any of the three runs. The fix has not appeared on any branch. This is an operational delay (fix not committed), not scientific closure (hypothesis not rejected).

## Recommendation to Director

The one-line fix must be committed with Director approval:

```python
# Line 112 of src/spider/kernel.py
# BEFORE (current):
candidates.sort(key=lambda m: m.confidence, reverse=True)
# AFTER (fix):
candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
```

After fix commit, the exact same frozen spec (EXP-GRAPH-34320613096) should be re-executed against committed HEAD without monkey-patching. All 14 conditions are sufficient — no spec changes needed.
