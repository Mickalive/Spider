# EXP-PRODUCT-34685457833 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34685457833
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can the empty-prefix guard be frozen as part of the Fix2 specification, the B_UNFIXED baseline be properly reimplemented as a true unfixed heuristic (without Fix1/Fix2 applied), and the full Fix1+Fix2+empty-prefix guard be committed to src/spider/kernel.py and src/spider/models.py — with production _bind semantics validated against all 9 conditions including slot_prefixes representation and prefix-stripping for VALUE CONTRACT — thereby advancing from monkey-patch validation to committed-code validation?

## 3. Motivation

Prior product work established:
- EXP-PRODUCT-34662221249: Fix1+Fix2 validated on imported kernel module via monkey-patching, all 9 conditions pass.
- Audit identified 5 required_fixes bounding claim ceiling: (1) empty-prefix guard EXPLORATORY, (2) B_UNFIXED invalid, (3) slot_prefixes empty for P1/G3/G5, (4) monkey-patch not committed code, (5) N1_CORRECTED valid only at tested synthetic config.

The next step is to commit patches to kernel.py/models.py, freeze the empty-prefix guard, reimplement B_UNFIXED as true unfixed heuristic, and validate production _bind semantics — moving from monkey-patch validation to committed-code validation.

## 4. Hypotheses

### H1: Committed-code validation
All 9 frozen conditions pass when run against committed kernel.py/models.py (same as monkey-patch results).

### H2: Empty-prefix guard frozen
The empty-prefix guard (reject parameterization when common prefix is empty) is frozen as part of specification, not EXPLORATORY.

### H3: B_UNFIXED true unfixed heuristic
B_UNFIXED reimplemented as rfind('/') without Fix1/Fix2 yields slot_count=1 for P1-like training but fails G1 (suffix corruption) and N1_ORIGINAL (over-parameterization), demonstrating delta attributable to fixes.

## 5. Data Generation

### 5.1 Conditions
Reuse identical conditions from EXP-PRODUCT-34662221249 (9 conditions: P1, G1, G2, G3, G5, N1_ORIGINAL, N1_CORRECTED, B_LITERAL, B_UNFIXED). Each condition: 3 training observations, 3 unseen values.

### 5.2 Training/Unseen Values
Identical to parent spec.json sections 5.2/5.3 (P1 path-prefix, G1 query-string, G2 multi-param, G3 deep-path, G5 path+query hybrid, N1_ORIGINAL cross-host, N1_CORRECTED disjoint, B_LITERAL, B_UNFIXED).

### 5.3 Code Changes
Commit patches to src/spider/kernel.py:
- `_find_common_prefix_suffix` with Fix1 suffix guard
- `_validate_prefix_boundary` with Fix2 last-char delimiter check
- `distill_parameterized` combining leaf-path extraction, Fix1, Fix2, empty-prefix guard
- Empty-prefix guard: if full_prefix empty, skip parameterization (lines 260-266 of parent run_experiment.py)

Commit patch to src/spider/models.py:
- Add `slot_prefixes: dict[str, str]` field to Mechanism dataclass (default empty)

## 6. Measures

### 6.1 Per-Condition Metrics
- slot_count: number of parameter slots induced
- binding_accuracy: fraction of unseen values bound correctly
- slot_prefixes: dict mapping slot name to prefix (observed vs expected)
- distill_success: boolean
- confidence: mechanism confidence

### 6.2 Aggregate Metrics
- condition_pass_rate: fraction of 9 conditions passing decision rule
- structural_generalization_rate: fraction of G-conditions passing
- overall_binding_accuracy: average binding accuracy across parameterized conditions

## 7. Null Models

### 7.1 B_LITERAL
No parameterization. Confidence 0.5 < min_confidence 0.8. Expected fail_rate=1.0.

### 7.2 B_UNFIXED
True unfixed heuristic (rfind('/') without Fix1/Fix2). Expected: slot_count=1 for P1, binding_accuracy=1.0 for P1 unseen, but binding_accuracy=0.0 for G1 (suffix corruption) and slot_count>0 for N1_ORIGINAL (over-parameterization).

## 8. Statistical Tests

No inferential statistics required. All conditions deterministic synthetic, n=3 per condition. Decision based on exact pass/fail per frozen decision rule.

## 9. Controls

### 9.1 Positive Control (P1)
slot_count=1, binding_accuracy=1.0. Verifies pipeline works after commit.

### 9.2 Null Controls (N1_ORIGINAL, N1_CORRECTED)
slot_count=0. Verifies Fix2 rejects over-parameterization and empty-prefix guard rejects disjoint URLs.

### 9.3 Baseline (B_LITERAL)
fail_rate=1.0. Confirms parameterized induction necessary.

### 9.4 Paired Comparison (B_UNFIXED)
slot_count=1 for P1, binding_accuracy=0.0 for G1, slot_count>0 for N1_ORIGINAL. Quantifies delta attributable to fixes.

## 10. Validity Threats

### 10.1 Commit Divergence
Monkey-patch may behave differently from committed code (import order, module state). Mitigation: run identical conditions, compare results.

### 10.2 slot_prefixes Representation Loss
slot_prefixes empty for P1/G3/G5 (observed '' vs expected 'users/'/'repos/main/issues/'). This is a ceiling bound, not a failure condition. Future _bind may rely on slot_prefixes for VALUE CONTRACT prefix-stripping.

### 10.3 External Validity
All conditions deterministic synthetic, zero model/network/browser calls. External validity unproven.

### 10.4 B_UNFIXED Implementation
True unfixed heuristic must be isolated from fixes. Mitigation: implement separate function without Fix1/Fix2.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. P1 slot_count=1 AND binding_accuracy=1.0
2. G1 slot_count=1 AND binding_accuracy=1.0
3. G2 slot_count=1 AND binding_accuracy=1.0
4. G3 slot_count=1 AND binding_accuracy=1.0
5. G5 slot_count=1 AND binding_accuracy=1.0
6. N1_ORIGINAL slot_count=0
7. N1_CORRECTED slot_count=0
8. B_LITERAL fail_rate=1.0
9. no import/syntax errors

### 11.2 FALSIFIED-IN-SETTING
If any established condition (P1/G2/G3/G5) drops below binding_accuracy=1.0.

### 11.3 MIXED
If G1 or N1_ORIGINAL fails but no regressions.

### 11.4 MEASUREMENT_INVALID
If sample sizes insufficient or pipeline errors prevent computation.

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- C-PARAM-INHERIT claim ceiling advances from 'monkey-patched synthetic' to 'committed-code synthetic'
- Clears path for C-PRODUCT-ECON measurement
- Empty-prefix guard frozen as specification
- B_UNFIXED demonstrates delta attributable to fixes

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Commit introduces divergence from monkey-patch
- C-PARAM-INHERIT remains EXPERIMENTAL at monkey-patch level
- Need to identify commit-specific divergence

### 12.3 Mixed Result (MIXED)
- Partial fixes work in committed code, some gaps remain
- Investigate specific failure modes

## 13. Analysis Plan

1. Commit patches to kernel.py/models.py
2. Run experiment script that imports committed kernel module
3. Execute 9 conditions with identical training/unseen values
4. Collect per-condition metrics
5. Apply frozen decision rule
6. Report B_UNFIXED paired comparison
7. Write raw_evidence.json, result.json, report.md, provenance.json

## 14. Analysis Code

Analysis will be implemented in Python using:
- `importlib` for fresh module imports
- `json` for strict comparison
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-PRODUCT-34685457833/` before execution.

## 15. Pre-registered Expectations

From parent experiment:
- All 9 conditions passed with monkey-patching
- Committed code should produce identical results
- If divergence occurs, likely due to import order or module state

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
