# EXP-PRODUCT-34642376433 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34642376433
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN
- **Parent Experiment**: EXP-PRODUCT-34485517221 (FALSIFIED-IN-SETTING, 4/7 pass)
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Scientific Question

Can three bounded kernel fixes — suffix extraction guard, Jaccard similarity threshold, and multi-slot URL decomposition — resolve the 3/7 condition failures from EXP-PRODUCT-34485517221 against actual `src/spider/kernel.py`, while preserving the 4/7 passing conditions?

## 3. Motivation

### What the parent experiment established (EXP-PRODUCT-34485517221)

The parent tested the `rfind('/')` leaf-path URL-as-string parameterization heuristic on 7 structurally different URL conditions. Results:

**Established (4/7 pass):**
- P1 (path-prefix): binding_accuracy=1.0, slot_count=1, template `https://api.example.com/users/${url}`
- G2 (multi-param query): binding_accuracy=1.0, slot_count=1, template `https://api.example.com/items?category=books&page=${url}`
- G3 (deep path): binding_accuracy=1.0, slot_count=1, template `https://api.example.com/orgs/acme/repos/main/issues/${url}`
- G5 (path+query hybrid): binding_accuracy=1.0, slot_count=1, template `https://api.example.com/users/${url}/items?page=1`

**Falsified (3/7 fail):**
- G1 (query-string simple): binding_accuracy=0.0 — suffix extraction captures trailing 'a' from alpha/beta/delta, corrupting template to `search?q=${url}a`
- G4 (multi-slot): slot_count=1 vs expected 2 — leaf-path model treats URL as single leaf, cannot split into >2 parameter slots
- N1 (null control): slot_count=1 vs expected 0 — training URLs share 'https://api.' prefix, heuristic over-parameterizes

**Key audit findings (REVISE, producer_claim_supported=false):**
- V1: slot_prefixes empty for P1/G3/G5 ('' vs expected 'users/'/'repos/main/issues/') — binding via template prefix, not correct slot_prefix semantics
- V2: standalone reimplementation, not actual kernel.py — _bind ignores prefixes dict
- V3: suffix corruption is mechanism failure, not training artifact
- V4: N1 misdesigned — shares 'https://api.' prefix, does not test true disjoint URLs
- V5: G4 contrived — single-leaf model cannot induce >1 slot by design

**Carry-forward from parent handoff:**
- Established: C2 resolved without regressions (path-prefix patterns work)
- Rejected: rfind('/') generalizes to all URL patterns; distill-time prefix stripping; _bind prefix-strip with full template prefix; C-PARAM-INHERIT is product-ready
- Unknown: Whether suffix fix restores G1; whether Jaccard threshold prevents N1; whether leaf-path extends to multi-slot; whether empty slot_prefixes is correctness failure or artifact; end-to-end economics (C-PRODUCT-ECON)
- Do not assume: C-PARAM-INHERIT is product-ready; 4 passing conditions are comprehensive; binding via template prefix equals correct slot_prefix semantics; run_experiment.py transfers to kernel.py; N1 is algorithmic over-parameterization; G4 is suffix bug vs architectural limitation

### Why this experiment is different

This experiment implements three **bounded, targeted fixes** against actual `src/spider/kernel.py` (not standalone reimplementation), resolves all 5 audit findings from the parent, and re-validates against the same 7 conditions plus a corrected N1 null control. The key differences:

1. **Actual kernel.py execution** (resolves V2): distill_parameterized and _bind are tested on the product code, not a standalone copy
2. **Suffix guard** (resolves V3/G1): filter out single-character or short non-structural common suffixes
3. **Jaccard threshold** (resolves V4/N1): gate parameterization when URL structure similarity is low
4. **Multi-slot via URL parsing** (resolves V5/G4): decompose URL path segments and query parameters into multiple slots
5. **Redesigned N1** (resolves V4): truly disjoint URLs with no shared prefix

## 4. Hypotheses

### H1: All 7 conditions pass
After implementing the three fixes, all 7 conditions achieve binding_accuracy=1.0 and correct slot_count when tested against actual kernel.py distill_parameterized and _bind.

### H2: No regressions
The 4 previously passing conditions (P1, G2, G3, G5) maintain binding_accuracy=1.0 with no change in binding behavior.

### H3: G1 suffix fix
The suffix guard prevents template corruption from shared trailing characters. Training values alpha/beta/gamma (no shared suffix beyond '') produce clean template `search?q=${url}` with binding_accuracy=1.0 on unseen gamma/epsilon/zeta.

### H4: G4 multi-slot
URL path-segment parsing detects 2 varying slots (user + order_id) with slot_count=2 and correct bound URLs for unseen values dave/400, eve/500, frank/600.

### H5: N1 null control (redesigned)
With truly disjoint URLs (https://a.com/x, https://b.org/y, https://c.net/z), Jaccard structure_similarity < 0.5 gates parameterization and slot_count=0.

### H6: B_LITERAL baseline
Literal mechanism reuse (confidence 0.5 < min_confidence 0.8) produces ResolutionStatus.UNKNOWN/EXPLORE for all conditions, confirming parameterized induction is necessary.

## 5. Implementation: Three Kernel Fixes

### 5.1 Fix 1: Suffix Extraction Guard

**File**: `src/spider/kernel.py` — `_find_common_prefix_suffix` function (or equivalent in distill_parameterized)

**Current behavior**: `_find_common_prefix_suffix(['alpha', 'beta', 'gamma'])` returns prefix='' suffix='a' (all end with 'a'). This corrupts templates by appending spurious suffixes.

**Fix**: After computing the common suffix, apply a guard:
- If suffix length == 1: discard (single-character suffixes are almost always spurious in URL/query contexts)
- If suffix length <= 2 AND suffix matches a common word boundary (e.g., is a single letter after a digit or special character): discard
- Otherwise: keep the suffix

**Rationale**: Single-character common suffixes (like 'a' from alpha/beta/gamma, '1' from page1/page2/page3) are structural artifacts of the training value vocabulary, not meaningful URL structure. The guard prevents template corruption without requiring URL-specific parsing.

**Expected effect on G1**: Template becomes `search?q=${url}` (no suffix), binding produces `search?q=gamma` correctly.

**Risk**: May discard legitimate short suffixes (e.g., 'v1' from api/v1, api/v2). Mitigated by requiring suffix length >= 2 for retention, and validated by checking P1/G2/G3/G5 are unaffected (their training values share no common suffix).

### 5.2 Fix 2: Jaccard Similarity Threshold

**File**: `src/spider/kernel.py` — after computing common prefix and path sets

**Current behavior**: Any set of observations with a common prefix is parameterized, regardless of how structurally similar the URLs are.

**Fix**: Compute `_compute_structure_similarity(observations)` (Jaccard of leaf paths) and gate parameterization:
- If `mean_jaccard < 0.5`: do NOT parameterize (return None from distill_parameterized)
- If `mean_jaccard >= 0.5`: proceed with parameterization

**Rationale**: URLs from different hosts (https://a.com/x, https://b.org/y, https://c.net/z) have low structural similarity because their leaf paths are disjoint. A threshold of 0.5 allows parameterization when most paths are shared (e.g., P1: all share url path) while blocking when paths are mostly disjoint.

**Expected effect on N1 (redesigned)**: Disjoint URLs have leaf paths {x}, {y}, {z} with Jaccard = 0/3 = 0.0 < 0.5, so parameterization is blocked and slot_count=0.

**Risk**: May reject valid parameterization for URLs with moderate structural overlap. Mitigated by setting threshold conservatively (0.5) and validating P1/G2/G3/G5 have Jaccard >= 0.5.

### 5.3 Fix 3: Multi-Slot URL Decomposition

**File**: `src/spider/kernel.py` — new `_decompose_url_slots` function

**Current behavior**: Leaf-path model treats URL as single string value. Only 1 slot is detected regardless of how many URL segments vary.

**Fix**: Add URL-aware slot detection that:
1. Parse the URL into components: scheme, host, path segments, query parameters
2. For each varying value, identify which path segment(s) or query parameter(s) differ across training observations
3. Create a separate slot for each independently varying segment/parameter
4. Build template with multiple `${slot_name}` placeholders

**Implementation approach**:
- Use `urllib.parse.urlparse` to decompose URLs
- Split path by '/' and query by '&'/'='
- For each path segment position: if values differ across training obs, create a slot
- For each query parameter: if values differ, create a slot
- Constant segments/parameters remain in the template as literals

**Expected effect on G4**: Training URLs `/users/alice/orders/100`, `/users/bob/orders/200`, `/users/charlie/orders/300` decompose into:
- Path segment 2 (user): alice/bob/charlie → slot `user`
- Path segment 4 (order_id): 100/200/300 → slot `order_id`
- Template: `https://api.example.com/users/${user}/orders/${order_id}`
- slot_count=2, binding_accuracy=1.0 on unseen dave/400, eve/500, frank/600

**Risk**: URL parsing may break on non-standard URLs. Mitigated by using stdlib `urllib.parse` and testing only on well-formed API URLs. Single-slot conditions (P1/G2/G3/G5) should be unaffected because only 1 segment varies.

## 6. Test Conditions

### 6.1 Conditions from Parent (EXP-PRODUCT-34485517221)

All 7 conditions are re-used with identical training data and unseen values:

| Condition | Type | Training URLs | Unseen Values | Expected Slots | Expected Binding |
|-----------|------|---------------|---------------|----------------|------------------|
| P1_PATH_PREFIX | Positive control | /users/A, /users/B, /users/C | D, E, F | 1 (url) | /users/D, /users/E, /users/F |
| G1_QUERY_STRING | Fix 1 target | /search?q=alpha, /search?q=beta, /search?q=gamma | gamma, epsilon, zeta | 1 (q) | /search?q=gamma, etc. |
| G2_MULTI_PARAM | Passing | /items?category=books&page=1,2,3 | 4, 5, 6 | 1 (page) | /items?category=books&page=4, etc. |
| G3_DEEP_PATH | Passing | /orgs/acme/repos/main/issues/1,2,3 | 4, 5, 6 | 1 (issue_id) | /orgs/acme/repos/main/issues/4, etc. |
| G4_MULTI_SLOT | Fix 3 target | /users/alice/orders/100, /users/bob/orders/200, /users/charlie/orders/300 | dave/400, eve/500, frank/600 | 2 (user, order_id) | /users/dave/orders/400, etc. |
| G5_PATH_QUERY | Passing | /users/alice/items?page=1, /users/bob/items?page=1, /users/charlie/items?page=1 | dave, eve, frank | 1 (user) | /users/dave/items?page=1, etc. |
| N1_NULL | Fix 2 target (redesigned) | https://a.com/x, https://b.org/y, https://c.net/z | x, y, z | 0 | No parameterization |

### 6.2 G1 Training Value Note

The parent used alpha/beta/delta (all end with 'a'). This prereg uses alpha/beta/gamma (also all end with 'a') to test the suffix guard under the same failure mode. The unseen values are gamma/epsilon/zeta. The suffix guard must discard the trailing 'a' to produce a clean template.

### 6.3 N1 Redesign Note

The parent N1 used https://api.example.com/a, https://api.other.com/b, https://api.third.com/c — these share 'https://api.' prefix (8 chars). The redesigned N1 uses truly disjoint URLs: https://a.com/x, https://b.org/y, https://c.net/z — these share only 'https://' (8 chars) and have Jaccard structure similarity = 0.0 (leaf paths {x}, {y}, {z} are disjoint).

### 6.4 G4 Unseen Values Note

The parent G4 used a workaround: unseen_values=[{'url': 'dave/orders/400'}] as a single string for the single slot. With multi-slot fix, unseen_values should be [{'user': 'dave', 'order_id': '400'}] to test true 2-slot binding. The expected URL is https://api.example.com/users/dave/orders/400.

## 7. Measures

### 7.1 Primary Metric
- **binding_accuracy**: fraction of unseen values that produce correct bound URL (1.0 = all correct)
- **slot_count_correct**: observed slot_count == expected slot_count for each condition
- **slot_prefixes_correct**: slot_prefixes match expected prefixes where structurally meaningful (P1: 'users/', G2: 'items?category=books&page=', G3: 'repos/main/issues/', G5: 'users/', G1: 'search?q=')

### 7.2 Secondary Metrics
- **structure_similarity**: Jaccard of leaf paths across training observations (for threshold validation)
- **template_correct**: action_template matches expected template structure
- **regression_check**: P1/G2/G3/G5 binding_accuracy == 1.0 (no regression)

### 7.3 Aggregate Metrics
- **condition_pass_rate**: fraction of 7 conditions passing (binding_accuracy=1.0 AND slot_count correct)
- **all_conditions_pass**: boolean (7/7 == true)
- **no_regression**: boolean (P1/G2/G3/G5 all pass)

## 8. Baselines

### 8.1 B_LITERAL (regression)
Literal mechanism reuse from kernel.py `distill()` method. Confidence 0.5 < min_confidence 0.8, so resolve() returns UNKNOWN/EXPLORE. Expected: fail_rate=1.0. This confirms parameterized induction is necessary.

### 8.2 B_PREVIOUS (parent reference)
EXP-PRODUCT-34485517221 standalone results: 4/7 pass, G1/G4/N1 fail. Used as regression reference, not as a competitive baseline.

### 8.3 B_NO_FIX_* (ablation baselines)
Run each condition without the corresponding fix to confirm the fix is causally responsible for the improvement:
- B_NO_FIX_SUFFIX: G1 without suffix guard → expected template corruption
- B_NO_FIX_THRESHOLD: N1 redesigned without Jaccard threshold → expected over-parameterization
- B_NO_FIX_MULTI_SLOT: G4 without URL parsing → expected slot_count=1

## 9. Controls

### 9.1 Positive Control (P1_PATH_PREFIX)
P1 has been passing since EXP-PRODUCT-34420092879. It must continue to pass after all three fixes are applied. Regression on P1 would indicate a fix broke established behavior.

### 9.2 Null Control (N1_DISJOINT_URLS)
Redesigned N1 with truly disjoint URLs tests the Jaccard threshold. slot_count must be 0. This replaces the misdesigned parent N1.

### 9.3 Regression Controls (G2, G3, G5)
These conditions have been passing since the parent experiment. They must continue to pass with binding_accuracy=1.0. Any regression indicates a fix introduced a new failure mode.

### 9.4 Fix Validation Controls (G1, G4)
G1 validates the suffix guard. G4 validates multi-slot decomposition. Both must pass with binding_accuracy=1.0 after fixes are applied.

## 10. Validity Threats

### 10.1 Kernel.py Divergence
**Threat**: distill_parameterized may not exist in current kernel.py, or may differ from the parent's standalone reimplementation in ways that affect binding.
**Mitigation**: If distill_parameterized is absent, implement it in kernel.py as part of the experiment (within product lane's granted scope). If present, use the existing implementation with fixes applied. Record exact kernel.py code version in provenance.

### 10.2 models.py slot_prefixes Field
**Threat**: Production Mechanism model may lack slot_prefixes field, causing serialization issues.
**Mitigation**: Add slot_prefixes field to Mechanism model if absent. Record the change in provenance.

### 10.3 Jaccard Threshold Sensitivity
**Threat**: Threshold of 0.5 may be too permissive (allowing N1-type over-parameterization) or too restrictive (rejecting valid parameterization).
**Mitigation**: Measure structure_similarity for all conditions. If P1/G2/G3/G5 have Jaccard < 0.5, the threshold needs adjustment. Report per-condition Jaccard values.

### 10.4 Multi-Slot Parsing Robustness
**Threat**: URL parsing may fail on edge cases (encoded characters, fragments, trailing slashes).
**Mitigation**: Use stdlib `urllib.parse` which handles standard URLs. Test only well-formed API URLs. Record any parsing errors.

### 10.5 Suffix Guard Over-Conservatism
**Threat**: Discarding single-character suffixes may lose legitimate short suffixes (e.g., 'v1' in api/v1).
**Mitigation**: The guard discards suffixes of length 1 only. 'v1' (length 2) is retained. Validate on conditions with short suffixes if needed.

### 10.6 Synthetic-to-Real Gap
**Threat**: All conditions are deterministic synthetic. Real-world URLs may have different structural patterns.
**Mitigation**: This is a kernel correctness experiment, not an economics experiment. C-PRODUCT-ECON will test real-world cost. The goal here is to establish that the kernel can handle the tested URL classes correctly.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. 7/7 conditions pass (binding_accuracy=1.0 AND slot_count correct)
2. No regression: P1/G2/G3/G5 each binding_accuracy=1.0
3. G4 induces slot_count >= 2 with correct bound URLs
4. N1_DISJOINT_URLS produces slot_count=0 (null control passes)
5. B_LITERAL fails as expected (fail_rate=1.0)
6. Execution is against actual kernel.py (not standalone reimplementation)
7. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Any condition fails (binding_accuracy < 1.0 or slot_count incorrect)
2. Any previously passing condition (P1/G2/G3/G5) regresses
3. Jaccard threshold incorrectly rejects a valid parameterization
4. Multi-slot parsing produces incorrect bound URLs

### 11.3 MEASUREMENT_INVALID
If:
1. Execution fails against kernel.py (import errors, missing functions)
2. Pipeline errors prevent measurement
3. models.py slot_prefixes field cannot be added without breaking other code

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- All 3 failure modes resolved on actual kernel.py
- C-PARAM-INHERIT advances toward validated status
- C-PRODUCT-ECON measurement unblocked
- Product lane can proceed to end-to-end economics measurement

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Identifies which fix failed and why
- May indicate deeper architectural limitation (leaf-path model insufficient)
- C-PARAM-INHERIT remains blocked; may require alternative approach (URL parsing as first-class mechanism, different representation)

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Kernel.py integration issue prevents measurement
- Not scientific evidence; indicates infrastructure gap

## 13. Analysis Plan

1. **Implement fixes**: Add suffix guard, Jaccard threshold, multi-slot decomposition to kernel.py
2. **Update models.py**: Add slot_prefixes field to Mechanism if absent
3. **Run all 7 conditions**: Against actual kernel.py distill_parameterized and _bind
4. **Run baselines**: B_LITERAL on all conditions
5. **Run ablations**: B_NO_FIX_SUFFIX, B_NO_FIX_THRESHOLD, B_NO_FIX_MULTI_SLOT
6. **Measure**: binding_accuracy, slot_count, slot_prefixes, structure_similarity per condition
7. **Check controls**: P1 positive, N1 null, G2/G3/G5 regression, G1/G4 fix validation
8. **Apply decision rule**: SURVIVES/FALSIFIED/INVALID
9. **Report**: All outcomes with equal prominence

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
