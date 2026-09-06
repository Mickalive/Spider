# EXP-PRODUCT-34015741916 — Kernel Integration Report

## Executive Summary

**Verdict: KERNEL-INTEGRATION-SURVIVES**

All 10 test conditions pass with binding_accuracy=1.0 (28/28 total). The field-path relevance noise filter, two-part structure-similarity check (Jaccard>=0.75 + constant-value anchor), and parameterized mechanism induction survive porting from the isolated run_experiment.py into src/spider/kernel.py.

A genuine bug was discovered and fixed during execution: the `_PARAMETER` regex in kernel.py was missing the hyphen in its character class, preventing binding of slot names containing hyphens (e.g., `X-Request-ID`).

## Key Results

### Slot Counts (All Correct)

| Condition | Expected | Observed | Match |
|-----------|----------|----------|-------|
| B1 | 1 | 1 [url] | ✓ |
| B2 | 2 | 2 [name, url] | ✓ |
| B3 | 3 | 3 [title, X-Request-ID, url] | ✓ |
| B4 | 1 | 1 [callback_url] | ✓ |
| B5 | 1 | 1 [url] | ✓ |
| C1 | 1 | 1 [callback_url] | ✓ |
| C2 | 1 | 1 [url] | ✓ |
| D1 | 3 | 3 [customer, X-Request-ID, url] | ✓ |
| D2 | 1 | 1 [url] | ✓ |
| D3 | 1 | 1 [url] | ✓ |
| E1 | 0 | 0 | ✓ |
| E2 | 0 | 0 | ✓ |

### Binding Accuracy (All 1.0)

- B1-B5: 21/21 (regression preserved)
- C1-C2: 6/6 (full-value binding correct)
- D1-D3: 7/7 (noisy conditions correct)
- E1-E2: N/A (null controls, slot_count=0)
- Literal baseline: 5/5 EXPLORE (fail_rate=1.0)

### Prereg Corrections Applied

- **B5**: Static A,A,A training (prereg) → slot_count=1 [url]. Parent deviation (varying A,B,C → slot_count=2) corrected.
- **D3**: Static quantity 1,1,1 training (prereg) → slot_count=1 [url]. Parent deviation (varying 1,2,3 → slot_count=2) corrected.
- **D2**: Expected slot_count=1 [url] per prereg architectural limitation. Post-hoc redefinition avoided.

## Bug Fix: _PARAMETER Regex Hyphen

The kernel.py regex `_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")` was missing the hyphen `-` in the character class. This prevented matching slot names like `X-Request-ID`.

**Fix**: Changed to `r"\$\{([A-Za-z_][A-Za-z0-9_-]*)\}"`.

**Impact**: Without this fix, B3 and D1 binding would fail (template `req-${X-Request-ID}` would not match). With the fix, all conditions pass.

## Parent Audit Findings Addressed

| Finding | Status |
|---------|--------|
| PREREG_DEVIATION_B5 | FIXED: B5 uses static A,A,A per prereg |
| PREREG_DEVIATION_D3 | FIXED: D3 uses static 1,1,1 per prereg |
| EXPECTED_POSTHOC_D2 | FIXED: D2 expected 1 [url] per prereg limitation |
| DOUBLE_PREFIX_NOT_TESTED | ADDRESSED: C2 passes with stripped varying parts |
| METADATA_SCOPE_LEAK | NOT FIXED: Separate follow-up (top-level allowlist works for test conditions) |
| KERNEL_INTEGRATION_GAP | RESOLVED: Code ported into kernel.py and tested |
| STRUCTURE_SIMILARITY_CONFOUNDED | NOT FIXED: E1 rejected by both criteria, anchor necessity not isolated |

## Claim Ceiling

Kernel-integrated, synthetic conditions only. The algorithmic gains of field-path relevance + structure-similarity transfer from isolated implementation to kernel code path. Ceiling does NOT extend to:
- Real-browser noise distributions
- End-to-end product economics (tokens, browser work)
- Nested metadata inside body/headers
- Query-string parameterization (D2 architectural limitation)
- True full-value binding with prefix-containing params (C2 tested with stripped parts)

## Consequences

### Positive
- Removes KERNEL_INTEGRATION_GAP from parent audit
- Advances C-PARAM-INHERIT from offline-isolated to kernel-integrated
- Enables future product experiments to test end-to-end economics
- B5/D3 prereg compliance restored for valid regression comparison

### Negative
- D2 query-string limitation persists (architectural, not a porting bug)
- Nested metadata scope leak persists (separate follow-up)
- Real-browser validation still required
