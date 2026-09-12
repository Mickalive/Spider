# EXP-PRODUCT-34704657427 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34704657427
- **Lane**: Product
- **Claims**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers), C-PRODUCT-ECON (SPIDER saves total cost per successful task)
- **Parent**: EXP-PRODUCT-34685457833 (SURVIVES_CURRENT_TEST, 9/9 conditions pass, committed-code synthetic)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Should slot_prefixes be computed non-empty (extracting the common prefix before the slot for VALUE CONTRACT prefix-stripping) or accepted as empty (template-only binding), and what is the delta attributable to Fix1+Fix2 when B_UNFIXED is run against G1 query-string and N1_ORIGINAL cross-host training data?

## 3. Motivation

### 3.1 slot_prefixes Decision (Primary Blocker)

The parent experiment (EXP-PRODUCT-34685457833) validated FIX1+Fix2 on committed code with 9/9 conditions passing. However, slot_prefixes remains empty for P1/G3/G5 (observed `{'url': ''}` vs expected `'users/'`/`'repos/main/issues/'`). Binding succeeds via template prefix embedded in action_template, not via slot_prefixes.

This is a design decision blocking C-PRODUCT-ECON:
- **Option A**: Accept empty slot_prefixes as design (binding works via template prefix, slot_prefixes not used for VALUE CONTRACT stripping)
- **Option B**: Modify distill_parameterized to compute non-empty slot_prefixes (extract portion after last '/' before slot)

The parent handoff explicitly identified this as the highest-priority next step before real-browser measurement.

### 3.2 B_UNFIXED Delta Quantification (Secondary)

The parent experiment reimplemented B_UNFIXED as true unfixed heuristic (rfind('/') without Fix1/Fix2) but only tested it on P1-like training data. G1/N1_ORIGINAL were not tested with B_UNFIXED to quantify the delta attributable to fixes. The parent handoff recommended running B_UNFIXED against G1 and N1_ORIGINAL training data.

### 3.3 Protocol-Only Gap (Tertiary)

The parent audit (V6) identified that Fix2 does not reject protocol-only 'https://' over-parameterization (`'https://${url}'`). `_validate_prefix_boundary('https://')` returns True (last_char '/'). This gap persists and should be documented.

## 4. Hypotheses

### H1: slot_prefixes Computation
Computing non-empty slot_prefixes by extracting the portion of the template path after the last '/' delimiter before the slot produces:
- P1: slot_prefixes = {'url': 'users/'}
- G3: slot_prefixes = {'url': 'repos/main/issues/'}
- G5: slot_prefixes = {'url': 'repos/main/issues/'}

without breaking any established condition (binding_accuracy remains 1.0 for all P1/G1/G2/G3/G5).

### H2: B_UNFIXED Delta
B_UNFIXED (true unfixed heuristic rfind('/') without Fix1/Fix2) applied to:
- G1 query-string training data: produces suffix-corrupted template, binding_accuracy=0.0 for unseen values
- N1_ORIGINAL cross-host training data: produces over-parameterized template, slot_count>0

demonstrating that Fix1 and Fix2 are necessary for these conditions.

### H3: Protocol-Only Gap
Fix2 does not reject protocol-only 'https://' over-parameterization (`'https://${url}'` with slot_prefixes={'url': 'https://'}), confirming the protocol-only gap persists.

## 5. Data

### 5.1 Established Conditions (Parent Replication)

Same 5 conditions as parent EXP-PRODUCT-34685457833, same training values:

| Condition | Training URLs | Slot | Expected slot_count | Expected binding_accuracy |
|-----------|---------------|------|--------------------|--------------------------|
| P1_PATH_PREFIX | https://api.example.com/users/{A,B,C} | url | 1 | 1.0 |
| G1_QUERY_STRING | https://api.example.com/posts?param={A,B,C} | url | 1 | 1.0 |
| G2_QUERY_MULTIPARAM | https://api.example.com/items?key={A,B,C}&sort=name | key | 1 | 1.0 |
| G3_DEEP_PATH | https://api.example.com/repos/main/issues/{A,B,C} | url | 1 | 1.0 |
| G5_PATH_QUERY_HYBRID | https://api.example.com/repos/main/issues/{A,B,C}?state=open | url | 1 | 1.0 |

### 5.2 Null Controls

| Condition | Training URLs | Expected slot_count |
|-----------|---------------|---------------------|
| N1_ORIGINAL | https://api.example.com/a, https://api.other.com/b, https://api.third.com/c | 0 |
| N1_CORRECTED | http://a.com/x, ftp://b.org/y, custom://c.net/z | 0 |

### 5.3 B_UNFIXED Conditions

| Condition | Training URLs | Expected Behavior |
|-----------|---------------|-------------------|
| B_UNFIXED_G1 | https://api.example.com/posts?param={A,B,C} | Suffix-corrupted template, binding_accuracy=0.0 |
| B_UNFIXED_N1 | https://api.example.com/a, https://api.other.com/b, https://api.third.com/c | Over-parameterized template, slot_count>0 |

### 5.4 Protocol-Only Condition

| Condition | Template | Expected Fix2 Behavior |
|-----------|----------|----------------------|
| PROTOCOL_ONLY | https://${url} | NOT rejected (gap persists) |

### 5.5 Sample Size

- 3 training observations per condition
- 3 unseen values per condition for binding test
- Total: ~11 conditions x 3 training + 3 unseen = ~66 binding tests

## 6. Measures

### 6.1 Primary Metrics
- **slot_prefixes_computed**: For each condition, the slot_prefixes dict after computing non-empty prefixes
- **binding_accuracy**: Fraction of unseen values correctly bound (strict JSON comparison)
- **slot_count**: Number of parameter slots induced
- **template**: The action_template string produced by distill_parameterized

### 6.2 B_UNFIXED Metrics
- **b_unfixed_template_g1**: Template produced by unfixed heuristic on G1 training data
- **b_unfixed_binding_accuracy_g1**: Binding accuracy on unseen values
- **b_unfixed_slot_count_n1**: Slot count on N1_ORIGINAL training data
- **b_unfixed_template_n1**: Template produced by unfixed heuristic on N1 training data

### 6.3 Protocol-Only Metrics
- **protocol_only_rejected**: Whether Fix2 rejects 'https://${url}'
- **protocol_only_slot_prefixes**: slot_prefixes when protocol-only template is parameterized

## 7. Null Models

### 7.1 B_EMPTY_SLOT_PREFIXES (Baseline)
Current behavior — slot_prefixes empty. All conditions pass with binding_accuracy=1.0. This is the baseline for comparison with computed non-empty slot_prefixes.

### 7.2 B_UNFIXED (Fix Necessity)
True unfixed heuristic without Fix1/Fix2. Expected to fail on G1 (suffix corruption) and N1_ORIGINAL (over-parameterization). If it does not fail, fixes are unnecessary for those conditions.

## 8. Statistical Tests

### 8.1 Primary
- Exact comparison: binding_accuracy == 1.0 for all established conditions
- Exact comparison: slot_count == 0 for N1_ORIGINAL/N1_CORRECTED
- Exact comparison: slot_prefixes == {'url': 'users/'} for P1, {'url': 'repos/main/issues/'} for G3/G5

### 8.2 B_UNFIXED
- Exact comparison: binding_accuracy == 0.0 for B_UNFIXED_G1
- Exact comparison: slot_count > 0 for B_UNFIXED_N1

### 8.3 Effect Size
- Not applicable: all metrics are deterministic binary (pass/fail) or exact values

## 9. Controls

### 9.1 Positive Control (P1_PATH_PREFIX)
- slot_count=1, binding_accuracy=1.0, slot_prefixes={'url': 'users/'}
- Verifies pipeline works after slot_prefixes computation change

### 9.2 Null Controls (N1_ORIGINAL, N1_CORRECTED)
- slot_count=0 for both
- Verifies empty-prefix guard and Fix2 still work

### 9.3 B_EMPTY_SLOT_PREFIXES (Baseline Comparison)
- All conditions pass with binding_accuracy=1.0 under empty slot_prefixes
- Identical to parent results — regression check

### 9.4 B_UNFIXED (Fix Necessity)
- B_UNFIXED_G1: binding_accuracy=0.0 (fix necessary)
- B_UNFIXED_N1: slot_count>0 (fix necessary)

### 9.5 Protocol-Only (Gap Documentation)
- Fix2 does NOT reject 'https://${url}'
- Gap persists, documented for future Fix2 enhancement

## 10. Validity Threats

### 10.1 slot_prefixes Computation Risk
Computing non-empty slot_prefixes could break distill_parameterized if the extraction logic is incorrect. Mitigation: fresh import per condition, regression check against parent results.

### 10.2 B_UNFIXED Implementation Risk
B_UNFIXED must be truly unfixed (no Fix1/Fix2 applied). If fixes leak into B_UNFIXED, delta is overestimated. Mitigation: isolated implementation, separate function without Fix1/Fix2 calls.

### 10.3 Synthetic-to-Real Gap
All conditions deterministic synthetic with n=3, zero model/network/browser calls. External validity unproven. Mitigation: this is a design decision experiment, not an economics measurement. C-PRODUCT-ECON will test external validity.

### 10.4 Protocol-Only Gap Scope
The protocol-only gap is documented but not fixed. Future Fix2 enhancement may add minimum prefix length or domain-aware threshold. Mitigation: gap is explicitly recorded in unresolved, not silently ignored.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Computing non-empty slot_prefixes does not introduce errors
2. P1 slot_count=1 AND binding_accuracy=1.0 AND slot_prefixes={'url': 'users/'}
3. G1 slot_count=1 AND binding_accuracy=1.0
4. G2 slot_count=1 AND binding_accuracy=1.0
5. G3 slot_count=1 AND binding_accuracy=1.0 AND slot_prefixes={'url': 'repos/main/issues/'}
6. G5 slot_count=1 AND binding_accuracy=1.0 AND slot_prefixes={'url': 'repos/main/issues/'}
7. N1_ORIGINAL slot_count=0
8. N1_CORRECTED slot_count=0
9. B_UNFIXED_G1 produces suffix-corrupted template (binding_accuracy=0.0)
10. B_UNFIXED_N1 produces over-parameterization (slot_count>0)
11. Protocol-only 'https://${url}' is NOT rejected by Fix2

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
- Any established condition (P1/G1/G2/G3/G5) drops below binding_accuracy=1.0 when slot_prefixes are computed non-empty
- Computing non-empty slot_prefixes introduces import/syntax errors

### 11.3 MIXED
If:
- B_UNFIXED does not show expected failures (binding_accuracy>0.0 on G1 or slot_count=0 on N1)
- Some conditions pass, some fail — partial fix necessity

### 11.4 MEASUREMENT_INVALID
If:
- Pipeline errors prevent computation
- B_UNFIXED implementation is not truly unfixed (fixes leak)

### 11.5 G4 (Reported Separately)
G4_MULTI_SLOT: slot_count=1 (not 2), binding_accuracy=0.0. Architectural limitation. Not part of decision rule.

## 12. Expected Outcomes

### 12.1 SURVIVES_CURRENT_TEST (Primary Expected)
- slot_prefixes computed non-empty for P1/G3/G5 without breaking conditions
- B_UNFIXED confirms Fix1+Fix2 necessary for G1/N1
- Protocol-only gap documented
- **Consequence**: slot_prefixes decision resolved (compute non-empty). C-PRODUCT-ECON can proceed with non-empty slot_prefixes. B_UNFIXED delta quantified. Product lane unblocked.

### 12.2 FALSIFIED-IN-SETTING
- slot_prefixes computation breaks established conditions
- **Consequence**: slot_prefixes must remain empty (template-only binding). C-PRODUCT-ECON proceeds with empty slot_prefixes. Design decision: Option A (accept empty).

### 12.3 MIXED
- B_UNFIXED does not show expected failures
- **Consequence**: Fix1+Fix2 may be unnecessary for G1/N1. Need to re-evaluate fix necessity. C-PRODUCT-ECON may proceed but with weaker fix justification.

## 13. Analysis Plan

1. **Implementation**: Add slot_prefixes computation to distill_parameterized (~20 lines). Compute non-empty prefixes by extracting portion after last '/' before slot.
2. **Established Conditions**: Re-run P1/G1/G2/G3/G5 with slot_prefixes computation. Verify binding_accuracy=1.0, slot_count=1, slot_prefixes non-empty for P1/G3/G5.
3. **Null Controls**: Re-run N1_ORIGINAL/N1_CORRECTED. Verify slot_count=0.
4. **B_UNFIXED**: Run unfixed heuristic on G1 and N1_ORIGINAL training data. Verify expected failures.
5. **Protocol-Only**: Test Fix2 on 'https://${url}'. Verify NOT rejected.
6. **Comparison**: Compare slot_prefixes values with expected values. Compare B_UNFIXED templates with fixed templates.
7. **Reporting**: Report all outcomes with equal prominence.

## 14. Analysis Code

Analysis will be implemented in Python using:
- `src/spider/kernel.py` (distill_parameterized with slot_prefixes computation)
- `src/spider/models.py` (Mechanism.slot_prefixes field)
- Custom test harness for binding accuracy and template comparison
- Standard library only (json, re, hashlib)

Code will be committed to `research/experiments/EXP-PRODUCT-34704657427/` before execution.

## 15. Pre-registered Expectations

From parent experiment EXP-PRODUCT-34685457833:
- slot_prefixes empty for P1/G3/G5 (observed '' vs expected 'users/'/'repos/main/issues/')
- Binding succeeds via template prefix, not slot_prefixes
- B_UNFIXED on P1-like training produces identical template to fixed version (rfind('/') correctly handles path-prefix)
- B_UNFIXED on G1/N1 not tested — delta unknown

From this experiment:
- slot_prefixes computation should produce non-empty values for P1/G3/G5
- B_UNFIXED should fail on G1 (suffix corruption) and N1 (over-parameterization)
- Protocol-only gap should persist

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
