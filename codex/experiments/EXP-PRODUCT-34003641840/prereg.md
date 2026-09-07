# EXP-PRODUCT-34003641840 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34003641840
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PRODUCT-33993747223 (FIXES-FALSIFIED)
- **Request Reason**: continuation (inherited next_question from parent handoff)

## 2. Scientific Question

Can a redesigned noise filter using field-path relevance and a higher structure-similarity threshold be implemented without breaking the B1/B4 clean-synthetic regression, and does this redesign resolve D1 noisy-observation over-parametrization and E1 pattern-absence hallucination?

## 3. Motivation

### What the parent experiment established (EXP-PRODUCT-33993747223)

The parent experiment tested three targeted algorithmic fixes to parameterized induction:

**Fix A (double-prefix detection in _bind):** PARTIALLY validated — succeeds when both prefix and suffix are non-empty (C1 passes), fails when suffix is empty (C2 produces `user-user-4` double prefix).

**Fix B (noise filter: len(common_prefix)>0 OR len(common_suffix)>0):** FALSIFIED — both false-positive (timestamp passes with prefix `2026-09-01T10:0` and suffix `:00Z`) and false-negative (body.name Alice/Bob/Charlie filtered out because empty prefix and suffix). Causes regression: B2 slot_count 1 vs 2, B3 2 vs 3, B5 1 vs 2.

**Fix C (structure-similarity Jaccard 0.3):** FALSIFIED — threshold too low. E1 unrelated POST/GET/DELETE share generic leaf paths (method, url) giving Jaccard=0.667 > 0.3, so check does not trigger and 1 slot is hallucinated.

**Established (carried forward):**
- B1 (single-path url) and B4 (non-identifier URLs) pass identically to parent EXP-PRODUCT-33974562602 — base algorithm is sound for simple cases
- Literal mechanism replay fails on all unseen multi-param combinations — parameterization remains necessary
- Single-observation null control (E2) correctly produces slot_count=0

**Rejected (carried forward):**
- Noise-filter heuristic len(prefix)>0 OR len(suffix)>0 — provably insufficient
- Structure-similarity Jaccard 0.3 — too low for unrelated observations sharing generic paths
- Double-prefix detection when suffix is empty — fails (C2 user-user-4)
- Producer binding_accuracy claims — inflated by harness bug (status==EXECUTABLE without content check)

**Unknown (carried forward):**
- Can field-path-relevance noise filtering distinguish signal from noise?
- What structure-similarity threshold correctly separates related from unrelated observations?
- How should suffix-empty double-prefix templates be handled?
- D2 query-string parameters (q, page) — leaf-path model cannot split URL query parameters

**Do Not Assume (carried forward):**
- Fix A works universally — fails when suffix is empty
- Noise-filter heuristic is salvageable without fundamental redesign
- B1/B4 passing means algorithm is generally correct — B2/B3/B5 regress
- Jaccard over leaf paths is the right structure-similarity metric
- Producer binding_accuracy metrics are reliable — harness bug inflates values

### Why this experiment is different

The parent experiment added three fixes on top of the existing code and tested them together. All three failed. This experiment takes a different approach:

1. **Replaces the noise-filter heuristic entirely** rather than patching it. The new approach uses field-path relevance: only consider fields within action-template-relevant paths (body.*, headers.*, url), excluding top-level metadata. This is a fundamentally different criterion than value-pattern prefix/suffix matching.

2. **Raises the structure-similarity threshold** from 0.3 to a two-part check: Jaccard >= 0.75 on leaf paths AND at least one shared path with constant values across observations. The constant-value anchor prevents unrelated observations from passing just because they share generic paths.

3. **Fixes the binding_correct harness bug** from EXP-PRODUCT-33993747223: verifies bound_action content against expected unseen values, not merely status==EXECUTABLE.

4. **Tests on identical observation data** as the parent experiment, enabling direct before/after comparison.

## 4. Hypotheses

### H1: Regression Preserved
B1 slot_count=1 and B4 slot_count=1, with all binding_correct=true under strict content verification. The noise-filter redesign does not break clean-synthetic parameterized induction.

### H2: D1 Noise Resolved
D1 slot_count=3 (customer, url, x_request_id) — metadata fields (timestamp, request_duration_ms, retry_count, user_agent) are excluded by field-path relevance filtering. Previously slot_count=4 (included timestamp).

### H3: E1 Hallucination Resolved
E1 slot_count=0 — unrelated observations (POST /api/payments, GET /api/users/42, DELETE /api/sessions/abc-123) are correctly identified as having no common parameterizable structure. Previously slot_count=1.

### H4: No Regression on Other Conditions
C1 (full-value URLs) slot_count=1 with all binding_correct=true. E2 (single observation) slot_count=0. No condition regresses vs parent experiment.

## 5. Test Conditions

All conditions use identical observation data as parent experiment EXP-PRODUCT-33993747223 (raw_evidence.json).

### 5.1 Regression Conditions (B1-B5)

**B1 (single-path url parameter):**
- Training: GET /api/items/{A,B,C} (3 observations)
- Expected: slot_count=1 [url], all 5 unseen bindings correct

**B2 (path and body):**
- Training: POST /api/users/{D,E,F} with body.name={Alice,Bob,Charlie} (3 observations)
- Expected: slot_count=2 [url, name], all 5 unseen bindings correct
- Note: name field has varying values with no common prefix/suffix — was incorrectly filtered by parent

**B3 (path, body, headers):**
- Training: POST /api/posts/{D,E,F} with body.title={First,Second,Third} and X-Request-ID=req-{4,5,6} (3 observations)
- Expected: slot_count=3 [url, title, x_request_id], all 5 unseen bindings correct

**B4 (non-identifier URL values):**
- Training: POST /api/webhooks with body.callback_url=https://site-{d,e,f}.com/hook (3 observations)
- Expected: slot_count=1 [callback_url], all 3 unseen bindings correct

**B5 (shared slot name):**
- Training: PUT /api/items/{D,E,F} with body.user_id={A,A,A} (3 observations)
- Expected: slot_count=1 [url] — user_id is static (same value A), correctly excluded

### 5.2 Full-Value Conditions (C1-C2)

**C1 (full-value URL binding):**
- Training: POST /api/webhooks with body.callback_url=https://site-{d,e,f}.com/hook (3 observations, full unseen values)
- Expected: slot_count=1 [callback_url], all 3 bindings correct

**C2 (full-value IDs with double-prefix):**
- Training: GET /api/users/user-{4,5,6} (3 observations)
- Expected: slot_count=1 [url], all 3 bindings correct — double-prefix detection handles prefix-only template

### 5.3 Noisy Observation Conditions (D1-D3)

**D1 (noisy POST with metadata):**
- Training: POST /api/orders/order-{4,5,6} with body.customer=cust-{D,E,F}, headers.X-Request-ID=req-10{4,5,6}, plus metadata: timestamp, request_duration_ms, retry_count, user_agent (3 observations)
- Expected: slot_count=3 [customer, url, x_request_id] — metadata excluded by field-path relevance
- Previous: slot_count=4 (included timestamp)

**D2 (noisy GET with query string):**
- Training: GET /api/search?q={delta,epsilon,zeta}&page={4,5,6} with metadata: response_time_ms, cache_hit, result_count (3 observations)
- Expected: slot_count=2 [q, page] — metadata excluded, query parameters extracted
- Previous: slot_count=2 [cache_hit, url] — wrong slots (metadata included, query params missed)
- Note: This condition tests URL query-string parsing, which is a new capability beyond the current leaf-path model. If the leaf-path model cannot extract query parameters, this condition documents the architectural limitation.

**D3 (varying preconditions):**
- Training: POST /api/orders/item-{4,5,6} with body.quantity={1,1,1} and varying session_id/auth_token (3 observations)
- Expected: slot_count=1 [url] — preconditions excluded from induction

### 5.4 Null Control Conditions (E1-E2)

**E1 (pattern-absence / unrelated observations):**
- Training: POST /api/payments, GET /api/users/42, DELETE /api/sessions/abc-123 (3 unrelated observations)
- Expected: slot_count=0 — no common parameterizable structure
- Previous: slot_count=1 (hallucinated from shared generic leaf paths method, url)
- Structure-similarity check: Jaccard on leaf paths after metadata exclusion = 1.0 (all share method, url), but constant-value anchor test fails (all values differ at every shared path)

**E2 (single observation null control):**
- Training: 1 observation only
- Expected: slot_count=0 — function requires >=2 observations

## 6. Noise Filter Design

### 6.1 Field-Path Relevance (replaces value-pattern heuristic)

A field is considered for parameter induction ONLY if its leaf path originates from an action-template-relevant top-level key:

**Included paths:** method, url, body.*, headers.*, query.*
**Excluded paths (metadata):** timestamp, request_duration_ms, retry_count, user_agent, response_time_ms, cache_hit, result_count, and any other top-level key not in the include list

**Rationale:** The value-pattern heuristic (prefix/suffix) conflates "has any common string overlap" with "is a signal field." Field-path relevance uses structural position: fields that are part of the HTTP action template (body, headers, url) are candidates for parameterization; fields that are observational metadata (timing, caching, user agent) are not.

### 6.2 Structure-Similarity Check (replaces Jaccard 0.3)

Two-part check:

**(a) Path-set Jaccard:** Compute Jaccard similarity of leaf-path sets across training observations. Threshold: >= 0.75.

**(b) Constant-value anchor:** At least one shared leaf path must have identical values across ALL training observations. This prevents unrelated observations from passing just because they share generic paths (method, url).

**Rationale for (b):** E1 observations all have leaf paths {method, url} with Jaccard=1.0, but at every shared path the values differ (POST vs GET vs DELETE, different URLs). The constant-value anchor detects this: no path has identical values, so the observations are unrelated.

### 6.3 Double-Prefix Detection (extends Fix A)

When template has prefix but no suffix (e.g., `user-${url}`), the detection checks:
- If param starts with prefix: strip prefix, use remainder as parameter value
- If param does NOT start with prefix: proceed with normal substitution

This handles the C2 case where `user-${url}` with param `user-4` produces `user-user-4` (double prefix). The fix detects that `user-4` starts with `user-` and strips it, yielding `user-${url}` with `url=4`.

## 7. Binding Correctness Verification

### 7.1 Strict Content Check (fixes harness bug)

For each unseen test case:
1. Resolve the mechanism with the test params
2. Compare bound_action content recursively against expected_action
3. binding_correct = (resolution.status == EXECUTABLE) AND (bound_action == expected_action)
4. NOT merely: binding_correct = (resolution.status == EXECUTABLE)

**Impact:** The parent experiment's binding_accuracy=1.0 for B2 was inflated — bound_action had body.name="Alice" (static from first training obs) instead of expected "Diana". Strict recompute gives regression_binding_accuracy=0.381.

## 8. Measures

### 8.1 Primary Metrics
- **slot_count** per condition: number of parameter slots induced
- **binding_correct_count** per condition: number of unseen test cases with correct bound_action (strict)
- **binding_accuracy** per condition: binding_correct_count / unseen_count

### 8.2 Secondary Metrics
- **parameter_slots** per condition: list of slot names induced
- **metadata_excluded** for D1: boolean — are metadata fields (timestamp, etc.) excluded?
- **jaccard_similarity** for E1: Jaccard on leaf paths after metadata exclusion
- **constant_anchor_pass** for E1: boolean — does any shared path have constant values?

### 8.3 Control Metrics
- **B1/B4_regression_pass**: boolean — slot_count and binding unchanged vs parent
- **E2_null_pass**: boolean — slot_count=0 for single observation
- **C1/C2_pass**: boolean — full-value binding correct

## 9. Decision Rules

### 9.1 FIXES-SURVIVE-REGRESSION
If ALL of:
1. B1 slot_count=1 AND all 5 binding_correct=true (strict)
2. B4 slot_count=1 AND all 3 binding_correct=true (strict)
3. D1 slot_count=3 AND slots ⊆ {customer, url, x_request_id}
4. E1 slot_count=0
5. C1 slot_count=1 AND all 3 binding_correct=true (strict)
6. E2 slot_count=0
7. No condition regresses vs parent EXP-PRODUCT-33993747223

### 9.2 FIXES-FALSIFIED
If ANY of conditions (1)-(7) fail.

### 9.3 MEASUREMENT_INVALID
If harness errors prevent execution, or binding_correct verification cannot be performed.

## 10. Validity Threats

### 10.1 D2 Query-String Architecture
The current leaf-path model treats the entire URL as a single leaf node. D2 requires extracting individual query parameters (q, page) from the URL. If the model cannot parse query strings, D2 will fail for architectural reasons unrelated to the noise-filter redesign. **Mitigation:** D2 is included as a diagnostic condition; its failure documents a known limitation rather than falsifying the noise-filter hypothesis.

### 10.2 Structure-Similarity Threshold Sensitivity
The two-part check (Jaccard >= 0.75 + constant-value anchor) is a first design. If it over-filters (rejects related observations) or under-fails (still allows E1), the threshold or anchor criterion may need adjustment. **Mitigation:** Report the exact Jaccard values and constant-anchor pass/fail for each condition to enable diagnosis.

### 10.3 Binding Correctness Definition
Strict content verification requires knowing the expected bound_action for each unseen test case. If the expected action is ambiguous (e.g., partial binding where url is correct but body is static), the verification may be overly strict or overly lenient. **Mitigation:** Define expected actions explicitly for each condition (as in parent raw_evidence.json) and verify recursively.

### 10.4 Synthetic-to-Real Gap
All test conditions use synthetic observations with known ground truth. Real browser observations have more complex noise patterns (network timing, auth state, DOM changes). **Mitigation:** This is a synthetic POC. Real-browser testing is a later gate.

## 11. Expected Outcomes

### 11.1 All Conditions Pass (FIXES-SURVIVE-REGRESSION)
- Field-path relevance filtering resolves D1 (metadata excluded) and E1 (constant-anchor detects unrelated observations)
- B1/B4 regression preserved — base algorithm intact
- C-PARAM-INHERIT advances from clean-synthetic to realistic-synthetic level
- Next gate: test with real browser observation noise
- Product consequence: parameterized induction becomes a credible product capability

### 11.2 B1/B4 Breaks (regression failure)
- Noise-filter redesign is too aggressive — excludes fields that are genuine parameters
- Diagnosis: which B-condition fails and which field is incorrectly excluded?
- Adjustment: weaken the filter (e.g., include body.* paths even if they have no prefix/suffix)
- Product consequence: parameterized induction remains at clean-synthetic POC level

### 11.3 D1 Still Fails (metadata not excluded)
- Field-path relevance filter is not correctly implemented or metadata allowlist is incomplete
- Diagnosis: which metadata field is still included?
- Adjustment: expand the metadata exclusion list or fix the path traversal logic
- Product consequence: noisy-observation robustness not achieved

### 11.4 E1 Still Fails (hallucination persists)
- Constant-value anchor check is insufficient or Jaccard threshold is wrong
- Diagnosis: what is the Jaccard value and constant-anchor result for E1?
- Adjustment: raise threshold, add value-diversity weighting, or use a different metric
- Product consequence: parameterized induction hallucinates on unrelated observations

## 12. Analysis Plan

1. **Implement noise filter:** Field-path relevance (allowlist: method, url, body, headers)
2. **Implement structure-similarity:** Two-part check (Jaccard >= 0.75 + constant-value anchor)
3. **Implement double-prefix fix:** Handle suffix-empty templates
4. **Implement strict binding verification:** Compare bound_action content, not just status
5. **Run all 10 conditions:** B1-B5, C1-C2, D1-D3, E1-E2
6. **Record slot_count, parameter_slots, binding_correct for each condition**
7. **Compare with parent raw_evidence.json:** Direct before/after comparison
8. **Apply decision rule:** FIXES-SURVIVE-REGRESSION / FIXES-FALSIFIED / MEASUREMENT_INVALID
9. **Report all outcomes with equal prominence**

## 13. Analysis Code

Analysis will be implemented in Python using:
- Standard library only (no external dependencies required)
- Recursive dict comparison for binding_correct verification
- Set operations for Jaccard similarity
- Path traversal for field-path relevance filtering

Code will be committed to `research/experiments/EXP-PRODUCT-34003641840/` before execution.

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
