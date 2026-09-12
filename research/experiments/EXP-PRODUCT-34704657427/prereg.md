# EXP-PRODUCT-34704657427 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34704657427
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-PRODUCT-34685457833 (SURVIVES_CURRENT_TEST, 9/9 conditions pass, committed-code synthetic)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Should slot_prefixes be computed non-empty (extracting the path segment before the varying part) or accepted as empty (template-only binding)?

## 3. Motivation

The parent experiment validated Fix1+Fix2 on committed code with 9/9 conditions passing. However, slot_prefixes remained empty for P1/G3/G5 despite the design intent of non-empty values (parent run_experiment.py expected `{"url": "users/"}` for P1, `{"url": "repos/main/issues/"}` for G3).

The parent implementation computed slot_prefixes as the common prefix of full URLs, which equaled the template prefix for path-prefix patterns, yielding empty slot_prefixes. The fix: extract only the path segment immediately before the varying part, not the full URL prefix.

The parent handoff identified this as the primary blocker for C-PRODUCT-ECON.

## 4. Hypotheses

### H1: Non-Empty slot_prefixes for Path-Prefix Patterns
Computing slot_prefixes as the path segment before the varying part produces:
- P1: slot_prefixes = {'url': 'users/'}
- G3: slot_prefixes = {'url': 'repos/main/issues/'}
- G5: slot_prefixes = {'url': 'users/'}

### H2: No Regression
All 5 established conditions maintain binding_accuracy=1.0. slot_prefixes is metadata-only and does not affect _bind behavior or action_template.

### H3: Query-String Patterns Unchanged
G1 and G2 slot_prefixes remain as parent (non-empty for query-string patterns, already correct).

## 5. Data

### 5.1 Established Conditions

Same training values as parent EXP-PRODUCT-34685457833 (from run_experiment.py):

| Condition | Training URLs | Expected slot_count | Expected binding_accuracy | Expected slot_prefixes |
|-----------|---------------|--------------------|-------------------------|----------------------|
| P1_PATH_PREFIX | https://api.example.com/users/{A,B,C} | 1 | 1.0 | {'url': 'users/'} |
| G1_QUERY_STRING | https://api.example.com/search?q={alpha,beta,delta} | 1 | 1.0 | {'url': 'search?q='} |
| G2_QUERY_MULTIPARAM | https://api.example.com/items?category=books&page={1,2,3} | 1 | 1.0 | {'url': 'items?category=books&page='} |
| G3_DEEP_PATH | https://api.example.com/orgs/acme/repos/main/issues/{1,2,3} | 1 | 1.0 | {'url': 'repos/main/issues/'} |
| G5_PATH_QUERY_HYBRID | https://api.example.com/users/{alice,bob,charlie}/items?page=1 | 1 | 1.0 | {'url': 'users/'} |

### 5.2 Null Controls

| Condition | Training URLs | Expected slot_count |
|-----------|---------------|---------------------|
| N1_ORIGINAL | https://api.example.com/a, https://api.other.com/b, https://api.third.com/c | 0 |
| N1_CORRECTED | http://a.com/x, ftp://b.org/y, custom://c.net/z | 0 |

### 5.3 Sample Size

- 3 training observations per condition
- 3 unseen values per condition for binding test
- Total: 7 conditions x 6 = 42 binding tests

## 6. Measures

### 6.1 Primary Metrics
- **slot_prefixes**: Dict mapping slot name to prefix string. Must be non-empty for P1/G3/G5.
- **binding_accuracy**: Fraction of unseen values correctly bound (strict JSON). Must be 1.0 for all established conditions.
- **slot_count**: Number of parameter slots. Must be 1 for established, 0 for nulls.
- **action_template**: Must be identical to parent for all conditions (slot_prefixes is metadata-only).

### 6.2 Derived Metrics
- **slot_prefixes_non_empty_for_path_prefix**: Boolean — P1/G3/G5 slot_prefixes != {'url': ''}
- **binding_regression**: Boolean — any established condition binding_accuracy < 1.0

## 7. Algorithm: slot_prefixes Computation

For each URL value, locate the slot position (${slot_name}) in the template. Extract the path segment immediately before the slot:

1. Find the position of ${slot_name} in the template
2. Find the last '/' before the slot position
3. Find the next '/' after the domain (after '://' and authority)
4. slot_prefix = template[next_slash_after_domain:last_slash_before_slot]

For query-string patterns (slot after '?'):
1. Find the position of ${slot_name} in the template
2. Find the '?' before the slot position
3. slot_prefix = template[question_mark_position + 1:slot_position]

This produces:
- P1: template `https://api.example.com/users/${url}` → last '/' before slot is at `users/`, next '/' after domain is at `users/` → prefix = `users/`
- G1: template `https://api.example.com/search?q=${url}` → '?' at `search?q=` → prefix = `search?q=`
- G3: template `https://api.example.com/orgs/acme/repos/main/issues/${url}` → last '/' before slot is at `issues/`, next '/' after domain is at `repos/` → prefix = `repos/main/issues/`
- G5: template `https://api.example.com/users/${url}/items?page=1` → last '/' before slot is at `users/` → prefix = `users/`

## 8. Controls

### 8.1 Positive Control (P1_PATH_PREFIX)
slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}. Verifies slot_prefixes computation and binding preservation.

### 8.2 Null Controls (N1_ORIGINAL, N1_CORRECTED)
slot_count=0 for both. Verifies Fix2 and empty-prefix guard still work.

### 8.3 Baseline (B_EMPTY_SLOT_PREFIXES)
Parent results: all conditions pass, slot_prefixes empty for P1/G3/G5. Regression check.

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. slot_prefixes computation does not introduce errors
2. P1: slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}
3. G1: slot_count=1, binding_accuracy=1.0
4. G2: slot_count=1, binding_accuracy=1.0
5. G3: slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'repos/main/issues/'}
6. G5: slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}
7. N1_ORIGINAL: slot_count=0
8. N1_CORRECTED: slot_count=0

### 9.2 FALSIFIED-IN-SETTING
If any established condition drops below binding_accuracy=1.0, or slot_prefixes computation introduces errors.

### 9.3 MIXED
If slot_prefixes computation works but produces empty for P1/G3/G5 (same as parent — design intent not achieved).

### 9.4 MEASUREMENT_INVALID
If distill_parameterized cannot be re-committed or pipeline errors prevent computation.

### 9.5 G4 (Reported Separately)
G4_MULTI_SLOT: slot_count=1, binding_accuracy=0.0. Architectural limitation. Not part of decision rule.

## 10. Validity Threats

### 10.1 Re-Commit Risk
The parent execution branch (fb7dd83) committed distill_parameterized, but the verdict commit (359a164) reverted it. Re-committing may introduce divergence. Mitigation: use exact code from fb7dd83, verify hash matches.

### 10.2 Algorithm Risk
The new slot_prefixes extraction algorithm may not match the design intent for all URL patterns. Mitigation: test on 5 conditions covering path-prefix, query-string, deep-path, and hybrid patterns.

### 10.3 Synthetic-to-Real Gap
All conditions deterministic synthetic, n=3, zero model/network/browser calls. External validity unproven. Mitigation: this is a design decision, not economics measurement. C-PRODUCT-ECON tests external validity.

### 10.4 Template不变性 Violation
If slot_prefixes computation accidentally changes action_template, the experiment is invalid. Mitigation: explicit check that action_template matches parent for all conditions.

## 11. Analysis Plan

1. Re-commit distill_parameterized from fb7dd83 to kernel.py
2. Add slot_prefixes extraction algorithm (Section 7)
3. Run all 7 conditions with fresh kernel imports
4. For each condition: record slot_prefixes, binding_accuracy, slot_count, action_template
5. Compare slot_prefixes with expected values (Section 5.1)
6. Verify binding_accuracy=1.0 for all established conditions
7. Verify slot_count=0 for null controls
8. Verify action_template matches parent for all conditions
9. Report all outcomes

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims.

## 13. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected.
