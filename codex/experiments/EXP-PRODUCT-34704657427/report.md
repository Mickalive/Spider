# EXP-PRODUCT-34704657427 Report

## Experiment Summary

**Experiment ID**: EXP-PRODUCT-34704657427  
**Lane**: Product  
**Claim**: C-PARAM-INHERIT  
**Outcome**: SUPPORTS  
**Status**: COMPLETE  
**Verdict**: SURVIVES_CURRENT_TEST

## Scientific Question

Should `slot_prefixes` be computed non-empty (extracting the path segment before the varying part) or accepted as empty (template-only binding)?

## Result

The frozen decision rule requires ALL 8 conditions to pass:

| Condition | slot_count | binding_accuracy | slot_prefixes | Pass |
|-----------|-----------|-----------------|---------------|------|
| P1 (positive control) | 1 | 1.0 | `{'url': 'users/'}` | ✓ |
| G1 (fix1 target) | 1 | 1.0 | `{'url': 'search?q='}` | ✓ |
| G2 (regression) | 1 | 1.0 | `{'url': 'items?category=books&page='}` | ✓ |
| G3 (deep path) | 1 | 1.0 | `{'url': 'orgs/acme/repos/main/issues/'}` | ✓ |
| G5 (path+query hybrid) | 1 | 1.0 | `{'url': 'users/'}` | ✓ |
| N1_ORIGINAL (null) | 0 | — | — | ✓ |
| N1_CORRECTED (null) | 0 | — | — | ✓ |
| B_LITERAL (baseline) | 0 | — | — | ✓ |

**All 8 conditions pass.** path_prefix_non_empty = True. Template invariant holds. Pipeline no errors.

### slot_prefixes Verification

- P1: `{'url': 'users/'}` — non-empty ✓
- G3: `{'url': 'orgs/acme/repos/main/issues/'}` — non-empty ✓
- G5: `{'url': 'users/'}` — non-empty ✓

**Key finding**: slot_prefixes computation produces non-empty values for all path-prefix patterns. The design intent is achieved: non-empty slot_prefixes enable VALUE CONTRACT prefix-stripping.

### G3 slot_prefixes discrepancy

The preregistration expected G3 slot_prefixes = `{'url': 'repos/main/issues/'}`. The observed value is `{'url': 'orgs/acme/repos/main/issues/'}`. This is because the algorithm extracts the full path segment from the first `/` after the domain authority to the slot position, not just the segment before the last `/`. Both are non-empty and functionally correct. The full path segment is more complete for VALUE CONTRACT stripping: given a concrete URL, stripping `orgs/acme/repos/main/issues/` extracts the parameter value; stripping `repos/main/issues/` would leave `orgs/acme/` in the value. The observed behavior is semantically preferable.

### Reported separately (not part of decision rule)

- **G4** (architectural): slot_count=1, binding_accuracy=0.0. Leaf-path model produces 1 slot, multi-char suffix '00' not caught by Fix1. Architectural limitation, not fix failure.
- **B_UNFIXED** (true unfixed heuristic): On P1 training data, slot_count=1, binding_accuracy=1.0. The unfixed `rfind('/')` heuristic works for P1 because the slot is at the end of the URL path. P1 is not a discriminating test for Fix1; the discriminating test is G1 (query-string suffix corruption), which B_UNFIXED does not exercise in this run.

## Interpretation

**The hypothesis is supported**: Computing non-empty `slot_prefixes` by extracting the path segment between domain authority and slot position produces the expected non-empty values for P1/G3/G5 without breaking binding_accuracy=1.0 for any established condition.

**Product consequence**: Non-empty `slot_prefixes` enable VALUE CONTRACT prefix-stripping. Given a concrete URL, the mechanism can extract the parameter value by stripping the known prefix. This clears the primary design blocker for C-PRODUCT-ECON.

**C-PARAM-INHERIT claim ceiling advances** to: committed-code synthetic single-slot with prefix metadata.

**Next steps** (from parent handoff):
1. Proceed to C-PRODUCT-ECON measurement (end-to-end amortized economics on real agents)
2. Run B_UNFIXED against G1 query-string and N1_ORIGINAL cross-host training data to quantify fix delta
3. Consider adding minimum prefix length threshold to Fix2 to reject protocol-only `https://` over-parameterization

## Controls and Baselines

| Control | Type | Result |
|---------|------|--------|
| P1_PATH_PREFIX | positive_control | PASS |
| N1_ORIGINAL | null_control_fix2 | PASS |
| N1_CORRECTED | null_control_corrected | PASS |
| B_LITERAL | baseline_literal | PASS |
| G2_QUERY_STRING_MULTIPARAM | regression | PASS |
| G3_DEEP_PATH | regression_slot_prefixes | PASS |
| G5_PATH_QUERY_HYBRID | regression_slot_prefixes | PASS |

## Validity Threats

1. **Synthetic-to-real gap**: All conditions deterministic synthetic, n=3, zero model/network/browser calls. External validity unproven.
2. **G3 slot_prefixes full path vs shorter path**: Algorithm extracts full path segment from authority end, not the shorter path before last `/`. Both are non-empty; downstream agents should decide preference.
3. **B_UNFIXED not exercised on discriminating conditions**: P1 is not a test for Fix1; G1 (query-string) would discriminate. Not measured.
4. **Template invariance**: Verified by explicit check — action_template matches parent for P1, G3, G5.
