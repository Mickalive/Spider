# EXP-PRODUCT-35130681515 Report

## 1. Summary

**Status:** COMPLETE | **Outcome:** SUPPORTS | **Verdict:** SURVIVES_CURRENT_TEST

Fix3 (`_is_protocol_only_prefix`) successfully resolves the Fix2 protocol-only gap identified in the parent handoff (EXP-PRODUCT-35124662913). All 10 frozen decision-rule conditions pass. The PROTOCOL_ONLY condition (Fix3 primary target) now produces `slot_count=0`, whereas the unfixed heuristic produces `slot_count=1` (over-parameterized `https://${url}`).

## 2. Decision Rule Evaluation

All 10 conditions pass:

| Condition | Expected | Observed | Pass |
|-----------|----------|----------|------|
| P1_PATH_PREFIX | slot=1, binding=1.0 | slot=1, binding=1.0 | YES |
| G1_QUERY_STRING_SIMPLE | slot=1, binding=1.0 | slot=1, binding=1.0 | YES |
| G2_QUERY_STRING_MULTIPARAM | slot=1, binding=1.0 | slot=1, binding=1.0 | YES |
| G3_DEEP_PATH | slot=1, binding=1.0 | slot=1, binding=1.0 | YES |
| G5_PATH_QUERY_HYBRID | slot=1, binding=1.0 | slot=1, binding=1.0 | YES |
| N1_ORIGINAL | slot=0 | slot=0 | YES |
| N1_CORRECTED | slot=0 | slot=0 | YES |
| PROTOCOL_ONLY | slot=0 (Fix3 target) | slot=0 | YES |
| B_LITERAL | fail_rate=1.0 | fail_rate=1.0 | YES |
| Pipeline errors | none | none | YES |

## 3. Fix3 Mechanism

Fix3 is implemented as `_is_protocol_only_prefix(prefix: str) -> bool` in `src/spider/kernel.py`. It checks whether a common prefix is purely scheme+authority without a path delimiter:

- `https://` → True (protocol-only, rejected)
- `http://` → True (protocol-only, rejected)
- `https://a.com` → True (protocol-only, rejected)
- `https://a.com/` → False (has path delimiter `/`, allowed)
- `https://api.example.com/users/` → False (has path content, allowed)

The function is called at the beginning of `distill_parameterized()` after common prefix computation. When it returns True, the function returns `None` (no parameterization induced), preventing over-parameterized templates like `https://${url}`.

## 4. Fix3 Necessity

- **Without Fix3** (unfixed heuristic): PROTOCOL_ONLY produces `slot_count=1`, template `https://${url}`, `binding_accuracy=1.0` (but semantically wrong — parameterizes the entire domain)
- **With Fix3**: PROTOCOL_ONLY produces `slot_count=0` (no parameterization)
- **Delta:** 1 (fix eliminates one over-parameterized condition)

## 5. Regression Assessment

All 5 parent established conditions survive with identical results to EXP-PRODUCT-35124662913:
- P1: slot=1, binding=1.0, slot_prefixes={"url": "users/"}
- G1: slot=1, binding=1.0, slot_prefixes={"url": "search?q="}
- G2: slot=1, binding=1.0, slot_prefixes={"url": "items?category=books&page="}
- G3: slot=1, binding=1.0, slot_prefixes={"url": "orgs/acme/repos/main/issues/"}
- G5: slot=1, binding=1.0, slot_prefixes={"url": "users/"}

Template invariance preserved: slot_prefixes extraction is metadata-only.

## 6. Realistic Corpus

4/6 conditions parameterize correctly:
- **R1_REST_API** (REST path-versioned): slot=1, binding=1.0 ✓
- **R3_PROTOCOL_ONLY_DEEP** (CDN with path): slot=1, binding=1.0 ✓
- **R5_MINIMAL_PREFIX** (short domain with path): slot=1, binding=1.0 ✓
- **R2_QUERY_HEAVY**: slot=1, binding=0.0 — template varies only `q` param, unseen values lack `&page=` part (test design issue)
- **R4_CROSS_PROTOCOL**: slot=0 — Fix2 rejects prefix ending at non-delimiter character (version segment)
- **R6_PROTOCOL_ONLY_SHALLOW**: slot=1 — `https://a.com/` has path delimiter, correctly parameterized

Prevalence of Fix3-rejected protocol-only patterns: 0/6 in realistic corpus (none are purely scheme+authority without path delimiter). The protocol-only gap is limited to cases where different domains share only the scheme (e.g., `https://a.com/x`, `https://b.com/y`).

## 7. Known Limitations

1. **Fix2 limitation:** Path-embedded version parameters (e.g., `/v1/data` vs `/v2/data`) fail Fix2 boundary check because the prefix ends at a non-delimiter character. Requires segment-aware prefix validation.
2. **Single-slot induction:** Multi-parameter URL templates (R2: `q` + `page`) require multi-slot induction or composite unseen values.
3. **Synthetic only:** Zero model/network/browser calls. C-PRODUCT-ECON measurement remains the next gate.
4. **Realistic corpus is synthetic:** Prevalence measurement is illustrative, not ground truth.

## 8. Consequences

**Positive:** C-PARAM-INHERIT protocol-only gap resolved. Claim ceiling advances to include Fix3. Path for C-PRODUCT-ECON measurement opens: protocol-only over-parameterization concern is addressed for URLs with path delimiters. Product lane can proceed to real-browser cost measurement.

**Negative:** None from this experiment. All decision-rule conditions pass. Known limitations (Fix2 boundary, single-slot) are inherited from parent, not introduced by Fix3.

## 9. What This Does NOT Establish

- Real-browser external validity
- C-PRODUCT-ECON cost savings
- Multi-slot induction
- Fix2 path-embedded parameter handling
- Real-world URL pattern prevalence (synthetic approximation only)
- Cross-site transfer
