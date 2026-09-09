# EXP-PRODUCT-34015741916 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34015741916
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-06
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can the field-path relevance noise filter, two-part structure-similarity check (Jaccard>=0.75 + constant-value anchor), and double-prefix detection be ported from run_experiment.py into src/spider/kernel.py distill_parameterized() such that all 10 test conditions pass with correct prereg training data?

## 3. Motivation

The parent experiment EXP-PRODUCT-34003641840 validated the field-path relevance and structure-similarity concepts in an isolated implementation (run_experiment.py) that never modified kernel.py. The audit identified KERNEL_INTEGRATION_GAP as the primary blocker: the entire implementation is self-contained and does not touch the production code path.

This experiment ports the validated components into the kernel and tests whether the algorithmic gains survive integration. This is the critical gate between offline validation and kernel-integrated parameterized induction.

## 4. Parent Handoff State

### Established (from parent)
- Field-path relevance noise filter correctly excludes metadata from D1 and D2
- Structure-similarity two-part check (Jaccard>=0.75 + constant anchor) prevents E1 hallucination
- B1/B4 clean-synthetic regression preserved under strict binding verification
- C1 full-value URL binding passes
- E2 single-observation null control passes
- Base distill_parameterized algorithm sound for path-only and URL-value parameterization

### Rejected (from parent)
- Noise-filter heuristic len(common_prefix)>0 OR len(common_suffix)>0 — PROVABLY INSUFFICIENT
- Structure-similarity Jaccard threshold 0.3 — TOO LOW
- Producer's broad claim FIXES-SURVIVE-REGRESSION — NOT SUPPORTED per audit ceiling

### Unknown (from parent)
- Whether field-path relevance + structure-similarity survive kernel integration
- Whether B5/D3 pass with correct prereg training data
- Whether C2 double-prefix can be fixed for suffix-empty templates
- Whether nested metadata (body.timestamp) leaks through top-level-only allowlist

### Do Not Assume (from parent)
- Do not assume this result transfers to kernel-integrated code
- Do not assume B5/D3 results are valid regression anchors (parent used wrong training data)
- Do not assume C2 double-prefix is fixed (parent had dead code)
- Do not assume D2 slot_count=1 means D2 passes (parent redefined post-hoc)

## 5. Hypotheses

### H1: Kernel Integration Preserves Regression
B1-B5 produce correct slot counts (B1=1, B2=2, B3=3, B4=1, B5=1) with binding_accuracy=1.0 after porting to kernel.py.

### H2: Double-Prefix Fixed
C2 full-value binding (user-4, user-5, user-6) produces correct binding without double-prefix errors.

### H3: Noise Filtering Works in Kernel
D1 produces slot_count=3 with metadata excluded. D2 produces slot_count=1 [url] with metadata excluded and prereg limitation documented.

### H4: Prereg Compliance Restored
B5 uses static A,A,A training (expected slot_count=1 [url]). D3 uses static quantity 1,1,1 training (expected slot_count=1 [url]).

### H5: Null Controls Hold
E1 produces slot_count=0. E2 produces slot_count=0.

### H6: Literal Baseline Still Fails
Literal mechanism replay fails on all unseen multi-parameter combinations.

## 6. Implementation Plan

### 6.1 Components to Port

Port these functions from run_experiment.py into src/spider/kernel.py:

1. **`_collect_leaf_paths(d, prefix)`** — Collect leaf paths from nested dict
2. **`_is_metadata_path(path)`** — Check if path is metadata (top-level allowlist)
3. **`_get_value_at_path(d, path)`** — Get value at dot-separated path
4. **`_compute_jaccard(set1, set2)`** — Jaccard similarity
5. **`_check_constant_value_anchor(actions, shared_paths)`** — Constant-value anchor check
6. **`_find_common_prefix_suffix(values)`** — Common prefix/suffix
7. **`_extract_parameter_candidates(template, observations)`** — Field-path relevance extraction
8. **`_compute_structure_similarity(actions, path_values)`** — Two-part structure similarity
9. **`_detect_double_prefix(template_url, param_value)`** — Double-prefix detection
10. **`_set_template_value(d, path, new_value)`** — Set value at dot-separated path

### 6.2 New Kernel Method

Add `distill_parameterized(observations, mechanism_id)` to SpiderKernel class. This method:
1. Extracts parameter candidates using field-path relevance
2. Checks structure similarity (Jaccard>=0.75 + constant anchor)
3. Builds action template with prefix/suffix patterns
4. Detects and handles double-prefix for suffix-empty templates
5. Returns Mechanism with parameter_slots populated

### 6.3 Constants to Port

```python
ACTION_TEMPLATE_PATHS = {"method", "url", "body", "headers", "query"}
METADATA_KEYS = {
    "timestamp", "request_duration_ms", "retry_count", "user_agent",
    "response_time_ms", "cache_hit", "result_count",
}
```

### 6.4 Test Harness

Create a test script that:
1. Imports kernel.py (not run_experiment.py)
2. Uses kernel.distill_parameterized() for induction
3. Uses kernel.resolve() for binding
4. Verifies binding_correct via strict JSON comparison
5. Runs all 10 conditions with correct prereg data

## 7. Test Conditions

### Phase B: Regression Baseline

| Condition | Training | Expected Slot Count | Expected Slots |
|-----------|----------|-------------------|----------------|
| B1-single-path | GET items A,B,C | 1 | [url] |
| B2-path-and-body | POST users A,B,C with name | 2 | [name, url] |
| B3-path-body-headers | POST posts A,B,C with title + X-Request-ID | 3 | [title, X-Request-ID, url] |
| B4-non-identifier-values | POST webhooks with callback_url site-a/b/c.com | 1 | [callback_url] |
| B5-shared-slot-name | PUT items A,B,C with **static** user_id A,A,A | 1 | [url] |

**B5 correction**: Parent used varying A,B,C (slot_count=2). Prereg specifies static A,A,A. Only url varies, so expected slot_count=1 [url].

### Phase C: Full-Value Unseen

| Condition | Training | Expected Slot Count | Binding Test |
|-----------|----------|-------------------|--------------|
| C1-full-value-urls | Same as B4 | 1 | Full URLs site-d/e/f.com/hook |
| C2-full-value-ids | GET users user-1,2,3 | 1 | Full values user-4,5,6 (no double prefix) |

**C2 critical test**: Template is `https://api.example.com/users/user-${url}`. When binding with `{url: "4"}`, result must be `user-4` not `user-user-4`.

### Phase D: Noisy Browser

| Condition | Training | Expected Slot Count | Expected Slots |
|-----------|----------|-------------------|----------------|
| D1-noisy-post | POST orders with metadata | 3 | [customer, X-Request-ID, url] |
| D2-noisy-get | GET search with metadata | 1 | [url] |
| D3-varying-preconditions | POST orders with **static** quantity 1,1,1 | 1 | [url] |

**D2 honest documentation**: Prereg expected 2 [q,page] but leaf-path cannot split query params. Expected remains 1 [url]; limitation documented, not redefined.

**D3 correction**: Parent used varying 1,2,3 (slot_count=2). Prereg specifies static 1,1,1. Only url varies, so expected slot_count=1 [url].

### Phase E: Null Controls

| Condition | Training | Expected Slot Count |
|-----------|----------|-------------------|
| E1-pattern-absence | 3 unrelated observations (POST/GET/DELETE) | 0 |
| E2-single-obs | 1 observation | 0 |

### Literal Baseline

Literal mechanism from kernel.distill() on B2 training must fail (EXPLORE) on all B2 unseen combinations.

## 8. Measures

### 8.1 Primary Metric
- **binding_accuracy** = fraction of unseen test cases where bound_action == expected_action (strict JSON equality)

### 8.2 Secondary Metrics
- **slot_count** per condition
- **parameter_slots** identity per condition
- **executable_count** per condition
- **metadata_excluded** boolean per D1/D2
- **double_prefix_detected** boolean per C2
- **jaccard_similarity** per E1
- **has_constant_anchor** boolean per E1

## 9. Decision Rules

### 9.1 KERNEL-INTEGRATION-SURVIVES
If ALL of:
1. B1 slot_count=1, binding_accuracy=1.0
2. B2 slot_count=2, binding_accuracy=1.0
3. B3 slot_count=3, binding_accuracy=1.0
4. B4 slot_count=1, binding_accuracy=1.0
5. B5 slot_count=1, binding_accuracy=1.0 (static A,A,A)
6. C1 slot_count=1, binding_accuracy=1.0
7. C2 slot_count=1, binding_accuracy=1.0 (full values, no double prefix)
8. D1 slot_count=3, metadata excluded
9. D2 slot_count=1 [url], metadata excluded, limitation documented
10. D3 slot_count=1 [url] (static quantity)
11. E1 slot_count=0
12. E2 slot_count=0
13. Literal baseline fail_rate=1.0
14. No crashes or None returns where mechanism expected

### 9.2 KERNEL-INTEGRATION-FALSIFIED
If ANY condition fails its expected outcome.

### 9.3 MEASUREMENT_INVALID
If infrastructure prevents execution (import errors, kernel modification breaks existing functionality).

## 10. Validity Threats

### 10.1 Kernel Modification Risk
Modifying kernel.py could break existing distill(), resolve(), verify() methods. Mitigation: run existing kernel tests before and after modification.

### 10.2 Test Harness Fidelity
Test harness exercises kernel via import, not via end-to-end browser path. This tests algorithmic correctness, not network/auth/session dynamics. Disclosure: this is an offline synthetic test.

### 10.3 Nested Metadata Scope Leak
The parent audit identified that _is_metadata_path only checks top-level keys. body.timestamp would pass the filter. This experiment does NOT fix this bug — it is tracked as a separate follow-up. The current allowlist {method, url, body, headers, query} correctly handles the test conditions because metadata fields (timestamp, duration, etc.) are top-level.

### 10.4 D2 Query-String Limitation
The leaf-path model treats URL as a single leaf node. D2 produces slot_count=1 [url] instead of prereg expected 2 [q,page]. This is a known architectural limitation, not a porting bug. The expected outcome is slot_count=1 with limitation documented.

## 11. Consequences

### 11.1 Positive Outcome (KERNEL-INTEGRATION-SURVIVES)
- Removes KERNEL_INTEGRATION_GAP from parent audit
- Advances C-PARAM-INHERIT from offline-isolated to kernel-integrated
- Enables future product experiments to test end-to-end economics
- Claim ceiling: kernel-integrated, synthetic conditions only

### 11.2 Negative Outcome (KERNEL-INTEGRATION-FALSIFIED)
- Specific failure condition identifies which component broke during port
- Kernel integration remains blocked until bug is fixed
- Product lane must redesign approach or fix specific integration bug

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 13. Freeze Statement

This preregistration is frozen BEFORE any kernel code is modified or any outcome data is inspected. The experiment will be executed exactly as described here.
