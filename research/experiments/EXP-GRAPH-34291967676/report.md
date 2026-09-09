# EXP-GRAPH-34291967676 Report

## Summary

Experiment **BLOCKED** — fix prerequisite not met. No scientific measurement performed.

## Fix Verification

- **File**: `src/spider/kernel.py`
- **Line 112**: `candidates.sort(key=lambda m: m.confidence, reverse=True)`
- **Expected fix**: `candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)`
- **Fix present**: **NO**
- **Kernel SHA256**: `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`

## Decision Rule Application

Per frozen spec decision rule **9.3 BLOCKED**: "If fix is NOT present in committed HEAD (L112 sort key does not include len(parameter_slots))". This condition is satisfied. The experiment is BLOCKED, not FALSIFIED or SUPPORTS.

## Baseline and Core Hazard Conditions

All 14 conditions (6 baselines, 6 core hazard, 1 null control, 1 upsert compatibility) were skipped per spec: "If fix is not present in committed HEAD, status=BLOCKED, skip all conditions." No measurements were taken.

## Observations

1. Fix verification confirms the one-line fix has not been committed to production HEAD.
2. Parent handoff (EXP-GRAPH-34244445713) also reported fix absent and hazard persists on unfixed HEAD.
3. No monkey-patching was applied during this experiment.
4. No network or infrastructure failures.

## Validity Notes

- BLOCKED status is correct per frozen decision rule.
- No scientific measurement invalidity; prerequisite unmet.
- Claim C-PARAM-INHERIT remains EXPERIMENTAL; no SURVIVES_POST_COMMIT or FALSIFIED_POST_COMMIT possible.
- No new evidence for fix effectiveness obtained.

## Unresolved Questions

1. Whether the fix survives commitment to production HEAD.
2. Whether the fix resolves the hazard for all unseen ids 2-7 without monkey-patching.
3. Whether baselines regress after fix commit.
4. Whether B_CONFIDENCE_LITERAL_HIGHER remains literal-winning after fix commit.
5. Whether fix interacts correctly with registry upsert sorting.
6. Whether fix generalizes to real-web endpoints.

## Recommended Action

Commit the one-line fix to `src/spider/kernel.py` L112 with Director approval, then re-run this exact experiment against committed HEAD without monkey-patching.