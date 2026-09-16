# EXP-PRODUCT-35124662913 — Execution Report

## 1. Summary

**Experiment:** EXP-PRODUCT-35124662913  
**Lane:** product  
**Claim:** C-PARAM-INHERIT  
**Status:** COMPLETE  
**Outcome:** SUPPORTS  

The re-committed parameterized distillation kernel with Fix1 (suffix guard), Fix2 (delimiter-bound prefix validation), and slot_prefixes extraction passes all 8 decision-rule conditions from the amended frozen spec. The G3 slot_prefixes expected value amended to `'orgs/acme/repos/main/issues/'` is validated. Fix1 and Fix2 necessity are quantified on discriminating baselines for the first time.

## 2. Decision Rule Evaluation

All 8 frozen decision-rule conditions pass:

| Condition | Expected | Observed | Pass |
|-----------|----------|----------|------|
| P1_PATH_PREFIX | slot_count=1, binding=1.0, slot_prefixes={'url':'users/'} | slot_count=1, binding=1.0, slot_prefixes={'url':'users/'} | YES |
| G1_QUERY_STRING_SIMPLE | slot_count=1, binding=1.0 | slot_count=1, binding=1.0 | YES |
| G2_QUERY_STRING_MULTIPARAM | slot_count=1, binding=1.0 | slot_count=1, binding=1.0 | YES |
| G3_DEEP_PATH | slot_count=1, binding=1.0, slot_prefixes={'url':'orgs/acme/repos/main/issues/'} | slot_count=1, binding=1.0, slot_prefixes={'url':'orgs/acme/repos/main/issues/'} | YES |
| G5_PATH_QUERY_HYBRID | slot_count=1, binding=1.0, slot_prefixes={'url':'users/'} | slot_count=1, binding=1.0, slot_prefixes={'url':'users/'} | YES |
| N1_ORIGINAL | slot_count=0 | slot_count=0 | YES |
| N1_CORRECTED | slot_count=0 | slot_count=0 | YES |
| B_LITERAL | fail_rate=1.0 | fail_rate=1.0 | YES |

**Verdict: SURVIVES_CURRENT_TEST**

## 3. Fix1 Necessity Delta

B_UNFIXED_G1 runs the true unfixed heuristic (rfind('/') without Fix1/Fix2) against G1 query-string training data:

- **Fixed G1:** binding_accuracy=1.0, template `search?q=${url}`
- **Unfixed G1:** binding_accuracy=0.0, template `search?q=${url}a` (suffix-corrupted)
- **Delta:** 1.0 (maximum discriminating power)

This confirms Fix1 (suffix guard) is necessary. Without Fix1, the single-char suffix `'a'` from `'alpha/beta/delta'` is appended to the template, breaking all bindings.

## 4. Fix2 Necessity

B_UNFIXED_N1 runs the true unfixed heuristic against N1_ORIGINAL cross-host training data:

- **Fixed N1_ORIGINAL:** slot_count=0 (Fix2 rejects cross-host prefix ending at `.`)
- **Unfixed N1_ORIGINAL:** slot_count=1, template `https://${url}` (over-parameterized)

This confirms Fix2 (delimiter-bound prefix validation) is necessary. Without Fix2, cross-host URLs produce a template that parameterizes the entire domain+path.

## 5. Protocol-Only Boundary

PROTOCOL_ONLY condition: `['https://a.com/x', 'https://b.com/y', 'https://c.com/z']`

- Observed: slot_count=1, template `https://${url}`, binding_accuracy=1.0
- Fix2 allows `'https://'` prefix because last_char `'/'` passes delimiter check

This is a documented boundary condition, not a failure. The protocol-only gap means Fix2 does not reject prefixes shorter than the path segment. This needs a design decision before C-PRODUCT-ECON.

## 6. G3 Slot Prefixes Amendment

The G3 expected slot_prefixes amended from `'repos/main/issues/'` to `'orgs/acme/repos/main/issues/'` is validated:

- Observed: `{'url': 'orgs/acme/repos/main/issues/'}`
- Expected: `{'url': 'orgs/acme/repos/main/issues/'}`
- Match: YES

The full path segment from authority end to slot position is semantically correct for VALUE CONTRACT prefix-stripping: stripping `'orgs/acme/repos/main/issues/'` from a concrete URL extracts the bare parameter value (e.g., `'4'` from `'https://api.example.com/orgs/acme/repos/main/issues/4'`).

## 7. Template Invariance

slot_prefixes computation is metadata-only: action_template matches parent for all distill_success conditions. The template substitution logic (`_bind`) and template construction are unchanged.

## 8. G4 Architectural Bound

B_UNFIXED_G4: multi-char suffix `'00'` not caught by Fix1 (which addresses single-char suffixes only).

- Template: `users/${url}00`
- binding_accuracy: 0.0
- Architectural limitation, not fix regression

## 9. What This Experiment Establishes

- Fix1 (suffix guard) necessity quantified: delta=1.0 on G1 discriminating condition
- Fix2 (delimiter-bound prefix validation) necessity confirmed: unfixed N1 produces over-parameterization
- G3 slot_prefixes spec amendment validated: full path segment is correct
- All 5 established conditions pass with binding_accuracy=1.0
- Both null controls correctly reject (slot_count=0)
- slot_prefixes is non-empty for all path-prefix conditions
- Template invariance preserved

## 10. What This Experiment Does NOT Establish

- Real-browser external validity (all synthetic, zero model/browser/network calls)
- C-PRODUCT-ECON cost savings (requires real-browser testing)
- Multi-slot induction (G4 architectural bound persists)
- Protocol-only gap resolution (PROTOCOL_ONLY documents boundary, does not fix it)
- Cross-site transfer (C-CROSSSITE not tested)
