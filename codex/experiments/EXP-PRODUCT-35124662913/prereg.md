# EXP-PRODUCT-35124662913 preregistration

## 1. Experiment identity

- **Experiment ID:** EXP-PRODUCT-35124662913
- **Lane:** product
- **Claim IDs:** C-PARAM-INHERIT
- **Parent:** EXP-PRODUCT-34704657427 (verdict: REVISE, required_fixes: 3)
- **Mode:** Revision — re-commit validated code, amend spec, rerun on discriminating baselines

## 2. Question

After amending the G3 slot_prefixes expected value to the full path segment and rerunning B_UNFIXED against G1 query-string training data, does the parameterized distillation kernel with Fix1+Fix2+slot_prefixes pass the amended decision rule, and how large is the Fix1 necessity delta on discriminating conditions?

## 3. Hypothesis

Re-committing Fix1 (suffix guard), Fix2 (delimiter-bound prefix validation), and slot_prefixes extraction to `src/spider/kernel.py`, with G3 expected amended to `'orgs/acme/repos/main/issues/'`, produces:

1. All 5 established conditions (P1/G1/G2/G3/G5) maintain `binding_accuracy=1.0` with correct `slot_count=1`
2. B_UNFIXED against G1 yields `binding_accuracy=0.0` (suffix corruption without Fix1)
3. B_UNFIXED against N1_ORIGINAL yields `slot_count=1` (over-parameterization without Fix2)
4. Protocol-only condition yields `slot_count=1` (Fix2 allows `https://`)
5. All null controls (N1_ORIGINAL/N1_CORRECTED) correctly reject (`slot_count=0`)

The Fix1 necessity delta is: `fixed_G1_binding - unfixed_G1_binding = 1.0 - 0.0 = 1.0`.

## 4. Falsifier

Any of:

1. Re-committed code introduces import/syntax errors
2. Any established condition (P1/G1/G2/G3/G5) drops below `binding_accuracy=1.0`
3. `slot_prefixes` computation changes `action_template` or `_bind` behavior (must be metadata-only)
4. B_UNFIXED against G1 does NOT show suffix corruption (`binding_accuracy > 0.0`), indicating Fix1 is unnecessary
5. N1_ORIGINAL `slot_count > 0` under fixed kernel (Fix2 regression)

## 5. Conditions

### 5.1 Established conditions (regression checks)

| ID | Training URLs | Unseen URLs | Expected slot_count | Expected binding_accuracy | Expected slot_prefixes |
|----|---------------|-------------|---------------------|--------------------------|----------------------|
| P1_PATH_PREFIX | `https://api.example.com/users/{A,B,C}` | `{D,E,F}` | 1 | 1.0 | `{"url":"users/"}` |
| G1_QUERY_STRING_SIMPLE | `https://api.example.com/search?q={alpha,beta,delta}` | `{gamma,epsilon,zeta}` | 1 | 1.0 | `{"url":"search?q="}` |
| G2_QUERY_STRING_MULTIPARAM | `https://api.example.com/items?category=books&page={1,2,3}` | `{4,5,6}` | 1 | 1.0 | `{"url":"items?category=books&page="}` |
| G3_DEEP_PATH | `https://api.example.com/orgs/acme/repos/main/issues/{1,2,3}` | `{4,5,6}` | 1 | 1.0 | `{"url":"orgs/acme/repos/main/issues/"}` |
| G5_PATH_QUERY_HYBRID | `https://api.example.com/users/{A,B,C}/items?page=1` | `{D,E,F}` | 1 | 1.0 | `{"url":"users/"}` |

### 5.2 Null controls

| ID | Training URLs | Expected slot_count | Rationale |
|----|---------------|--------------------|----|
| N1_ORIGINAL | `https://api.example.com/a`, `https://api.other.com/b`, `https://api.third.com/c` | 0 | Cross-host: Fix2 rejects prefix ending at `.` |
| N1_CORRECTED | `http://a.com/x`, `ftp://b.org/y`, `custom://c.net/z` | 0 | Truly disjoint: empty-prefix guard rejects |
| PROTOCOL_ONLY | `https://a.com/x`, `https://b.com/y`, `https://c.com/z` | 1 | Protocol-only: Fix2 allows (last_char `/`), documents gap boundary |

### 5.3 Baselines (unfixed behavior)

| ID | Training data | Expected behavior | Purpose |
|----|---------------|-------------------|---------|
| B_UNFIXED_G1 | G1 training (`https://api.example.com/search?q={alpha,beta,delta}`) | `binding_accuracy=0.0` (suffix-corrupted template) | Quantify Fix1 necessity |
| B_UNFIXED_N1 | N1_ORIGINAL training (`https://api.example.com/a`, etc.) | `slot_count=1` (over-parameterized `https://${url}`) | Quantify Fix2 necessity |
| B_LITERAL | Any 3 URLs | `confidence=0.5 < min_confidence=0.8`, `fail_rate=1.0` | Confirm parameterized induction necessary |

### 5.4 B_UNFIXED_G4 (architectural bound, reported separately)

| ID | Training data | Expected behavior | Purpose |
|----|---------------|-------------------|---------|
| B_UNFIXED_G4 | G4 training (`https://api.example.com/items/{11,22,33}`) | `slot_count=1`, `binding_accuracy=0.0` (multi-char suffix `00` not caught by Fix1) | Architectural limitation, not fix failure |

## 6. Decision rule

If ALL of:

1. Re-commit does not introduce errors
2. P1: `slot_count=1 AND binding_accuracy=1.0 AND slot_prefixes={"url":"users/"}`
3. G1: `slot_count=1 AND binding_accuracy=1.0`
4. G2: `slot_count=1 AND binding_accuracy=1.0`
5. G3: `slot_count=1 AND binding_accuracy=1.0 AND slot_prefixes={"url":"orgs/acme/repos/main/issues/"}`
6. G5: `slot_count=1 AND binding_accuracy=1.0 AND slot_prefixes={"url":"users/"}`
7. N1_ORIGINAL: `slot_count=0`
8. N1_CORRECTED: `slot_count=0`

**Verdict = SURVIVES_CURRENT_TEST**

If any established condition (2-8) fails: **Verdict = FALSIFIED-IN-SETTING**

B_UNFIXED_G1, B_UNFIXED_N1, PROTOCOL_ONLY, and B_UNFIXED_G4 are reported for necessity quantification and gap bounding but do not gate the decision rule.

## 7. Algorithm

The experiment re-commits `distill_parameterized` from parent EXP-PRODUCT-34704657427 (kernel.py sha256 `1880ef67`), which includes:

1. **Fix1** (lines 157-186): Suffix guard — reject single-char suffixes not preceded by `?` or `&`
2. **Fix2** (lines 191-199): Delimiter-bound prefix validation — `_validate_prefix_boundary` checks prefix ends at a URL delimiter (`/`, `?`, `=`)
3. **Empty prefix guard** (lines 260-271): Reject parameterization when common prefix is empty
4. **slot_prefixes extraction** (lines 276-314): Extract path segment from domain authority end to slot position for path-prefix patterns; query prefix before slot for query-string patterns

B_UNFIXED uses the original `rfind('/')` heuristic without Fix1/Fix2, applied to the same training data as the fixed kernel.

## 8. Spec amendment rationale

G3 slot_prefixes expected value amended from `'repos/main/issues/'` to `'orgs/acme/repos/main/issues/'` because:

- The algorithm extracts the path segment from the first `/` after the domain authority to the slot position
- This produces `'orgs/acme/repos/main/issues/'` for G3, which is semantically correct for VALUE CONTRACT prefix-stripping (stripping this prefix from a concrete URL extracts the bare parameter value)
- The shorter `'repos/main/issues/'` would leave `'orgs/acme/'` in the stripped value, which is incorrect
- The frozen expected value in EXP-PRODUCT-34704657427 was an approximation; the actual algorithm behavior is correct
- Evidence: EXP-PRODUCT-34704657427 audit.json V1_RECOMPUTED_NON_EMPTY_WITH_G3_VALUE_MISMATCH

## 9. Controls and stability

- Fresh Python import per condition (no cross-contamination)
- Training values identical to parent `run_experiment.py`
- Training/unseen values disjoint (no leakage)
- n=3 training + 3 unseen per condition (42 binding tests total)
- Zero model/network/browser calls (deterministic synthetic)
- Deterministic: same inputs produce same outputs

## 10. Product consequences

**Positive:** C-PARAM-INHERIT claim ceiling advances. Fix1/Fix2 necessity quantified on discriminating conditions. Three audit required_fixes from EXP-PRODUCT-34704657427 cleared. Path for C-PRODUCT-ECON measurement opens.

**Negative:** If re-commit introduces regressions or B_UNFIXED on G1 shows Fix1 unnecessary, C-PARAM-INHERIT remains EXPERIMENTAL with narrowed mechanism scope.

## 11. What this does NOT establish

- Real-browser external validity (all synthetic, zero model/browser/network calls)
- C-PRODUCT-ECON cost savings (requires real-browser testing)
- Multi-slot induction (G4 architectural bound persists)
- Protocol-only gap resolution (PROTOCOL_ONLY documents boundary, does not fix it)
- Cross-site transfer (C-CROSSSITE not tested)
