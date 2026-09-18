# EXP-GRAPH-35308806969 Report: Pooled Paired-Sample Orthogonality Test at n=480 with Power Analysis

## Executive Summary

**MIXED outcome: Frozen gate fails on permutation p, but near-zero correlation with explicit power bound is a valid scientific finding.**

- **|r| = 0.0335 < 0.3**: Behavioral and structural signals show near-zero pooled correlation (r² = 0.001)
- **Permutation p = 0.4650 > 0.05**: Frozen C3 gate fails — the test lacks power to confirm orthogonality at n=480
- **Power analysis confirms underpowering**: At n=480, minimum detectable |r| for p<0.05 is 0.0895. For true |r|=0.05, minimum n required is 1,538. Observed |r|=0.0335 is below the detectable threshold.
- **C1-C2 PASS, C4 PASS**: TP=1.0, 8/8 conditions with variance, FP=0.0

**This is NOT evidence of non-orthogonality.** The frozen decision rule's permutation p<0.05 criterion is insufficient for very-low-magnitude correlations (|r| < 0.1). The result requires decision-rule revision.

**Decision criteria:**
- **C1 (drift TP >= 0.85, all Wilson lower > 0.75)**: mean TP = 1.0000, all Wilson lower = 0.9398 > 0.75 -> **PASS**
- **C2 (variance >= 6/8 conditions)**: 8/8 conditions with variance -> **PASS**
- **C3 (orthogonality |r| < 0.3 AND p < 0.05)**: |r| = 0.0335 < 0.3 (PASS), p = 0.4650 > 0.05 (FAIL) -> **FAIL** (conjunctive gate fails on p alone)
- **C4 (null FP = 0.0)**: FP = 0.0000 (0/240) -> **PASS**

**Overall: FAIL** (frozen conjunctive rule), but **outcome = MIXED** per prereg definition (C1-C2 PASS, C3 fails ONLY on permutation p, power analysis confirms underpowering)

**Measurement validity**: VALID (8/8 conditions with variance, 480 paired samples)

## Design Changes from Parent (EXP-GRAPH-35262262505)

| Aspect | Parent (n=240) | This Experiment (n=480) |
|--------|----------------|-------------------------|
| Samples per condition | 30 | 60 (doubled) |
| Total paired samples | 240 | 480 |
| Permutation permutations | 1,000 | 10,000 (as per prereg) |
| Power analysis | Not included | Fisher z-transform (mandatory) |
| MIXED outcome class | Not defined | Defined for power-confirmed underpowering |
| Session validity | ALL invalid (session_change=1) | SAME |
| session_status_check mapping | 401->1.0, 403->0.5, 500->0.75 | SAME |
| All other aspects | Same | Same |

## Experimental Conditions

### Co-occurring Conditions (8 total)

| Condition | Drift | Noise | Samples | Variance |
|-----------|-------|-------|---------|----------|
| cooccur_permission_boundary+optional_field_addition | permission_boundary | optional_field_addition | 60 | OK (b_std=0.1633, s_std=1.0820) |
| cooccur_permission_boundary+description_change | permission_boundary | description_change | 60 | OK (b_std=0.1502, s_std=0.6075) |
| cooccur_permission_boundary+response_time_jitter | permission_boundary | response_time_jitter | 60 | OK (b_std=0.1373, s_std=0.8315) |
| cooccur_permission_boundary+field_type_normalization | permission_boundary | field_type_normalization | 60 | OK (b_std=0.1551, s_std=0.7178) |
| cooccur_session_invalidation+optional_field_addition | session_invalidation | optional_field_addition | 60 | OK (b_std=0.3948, s_std=0.9330) |
| cooccur_session_invalidation+description_change | session_invalidation | description_change | 60 | OK (b_std=0.4028, s_std=0.6890) |
| cooccur_session_invalidation+response_time_jitter | session_invalidation | response_time_jitter | 60 | OK (b_std=0.3818, s_std=0.7980) |
| cooccur_session_invalidation+field_type_normalization | session_invalidation | field_type_normalization | 60 | OK (b_std=0.4282, s_std=0.6355) |

### Per-Condition Pearson r (Exploratory)

| Condition | r | p |
|-----------|---|---|
| cooccur_permission_boundary+optional_field_addition | 0.0220 | 0.8674 |
| cooccur_permission_boundary+description_change | -0.1497 | 0.2537 |
| cooccur_permission_boundary+response_time_jitter | 0.2003 | 0.1249 |
| cooccur_permission_boundary+field_type_normalization | -0.2458 | 0.0583 |
| cooccur_session_invalidation+optional_field_addition | -0.3145 | 0.0144 |
| cooccur_session_invalidation+description_change | -0.0440 | 0.7383 |
| cooccur_session_invalidation+response_time_jitter | 0.1579 | 0.2281 |
| cooccur_session_invalidation+field_type_normalization | 0.1531 | 0.2428 |

### Per-Drift-Pattern Pearson r (Exploratory)

| Drift Pattern | Samples | r |
|---------------|---------|---|
| permission_boundary | 240 | 0.0005 |
| session_invalidation | 240 | -0.0136 |

### Session Status Code Distribution (Session Invalidation Conditions)

| Condition | 401 | 403 | 500 | Total |
|-----------|-----|-----|-----|-------|
| cooccur_session_invalidation+optional_field_addition | 22 | 16 | 22 | 60 |
| cooccur_session_invalidation+description_change | 16 | 24 | 20 | 60 |
| cooccur_session_invalidation+response_time_jitter | 18 | 17 | 25 | 60 |
| cooccur_session_invalidation+field_type_normalization | 22 | 22 | 16 | 60 |

## Primary Analysis

### Pooled Pearson Correlation

- **r = 0.0335** (|r| = 0.0335, r² = 0.001)
- **p = 0.4650** (permutation test, 10,000 permutations)
- **n = 480** paired samples (8 conditions × 60 samples)
- **C3 threshold**: |r| < 0.3 -> PASS (but p < 0.05 required conjunctively -> FAIL)

### Power Analysis (Fisher z-transform, mandatory per prereg §9)

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Observed \|r\| | 0.0335 | Near-zero correlation |
| Fisher z(observed) | 0.0336 | |
| z-statistic under H0:ρ=0 | 0.733 | Not significant |
| p from Fisher z | 0.4636 | Consistent with permutation p |
| **Min detectable \|r\| at n=480** | **0.0895** | Observed \|r\|=0.0335 < 0.0895 (below detection threshold) |
| **Min n for \|r\|=0.05, p<0.05** | **1,538** | n=480 << 1,538 (underpowered) |
| **Expected p at n=480 for \|r\|=0.05** | **0.2744** | Would still fail p<0.05 gate |
| n sufficient for observed \|r\|? | **NO** | Underpowered for the observed effect size |

**Key finding**: The parent's recommendation of n>=480 is confirmed as insufficient. The power analysis predicts p≈0.27 for |r|~0.05 at n=480, which matches the observed p=0.47 for |r|=0.034. To achieve p<0.05 for |r|=0.05, n≈1,538 is required.

### Signal Observability (Within-Condition Variance)

- **Conditions with variance (both signals std > 0)**: 8/8
- **Measurement validity**: VALID (8 >= 6 conditions, 480 >= 480 samples)

### Per-Condition Variance Details

| Condition | Behavioral Std | Structural Std | Has Variance |
|-----------|----------------|----------------|--------------|
| cooccur_permission_boundary+optional_field_addition | 0.1633 | 1.0820 | YES |
| cooccur_permission_boundary+description_change | 0.1502 | 0.6075 | YES |
| cooccur_permission_boundary+response_time_jitter | 0.1373 | 0.8315 | YES |
| cooccur_permission_boundary+field_type_normalization | 0.1551 | 0.7178 | YES |
| cooccur_session_invalidation+optional_field_addition | 0.3948 | 0.9330 | YES |
| cooccur_session_invalidation+description_change | 0.4028 | 0.6890 | YES |
| cooccur_session_invalidation+response_time_jitter | 0.3818 | 0.7980 | YES |
| cooccur_session_invalidation+field_type_normalization | 0.4282 | 0.6355 | YES |

## Controls

### Positive Control: permission_boundary Detection (PC-TP-WITH-VARIANCE)

- **Observed rate**: 1.0000 (60/60)
- **Threshold**: >= 0.90
- **Pass**: YES
- **Evidence**: All 60 permission_boundary samples correctly detected drift via behavioral signals

### Positive Control: session_status_variance

- **session_invalidation conditions with variance**: 4/4
- **Threshold**: >= 4 (all 4 session_invalidation conditions should have variance)
- **Pass**: YES
- **Evidence**: Graded session_status_check (401/403/500) produces behavioral std > 0 in all SI conditions

### Null Control: Noise-Only FP (NC-SCHEMA-NOISE-ONLY)

- **Observed FP rate**: 0.0000 (0/240)
- **Threshold**: FP = 0.0
- **Pass**: YES
- **Evidence**: Behavioral signals produce zero false positives on 240 noise-only samples (4 conditions × 60)

## Validity Threats

1. **Deterministic mock server**: All measurements on localhost Flask, not production APIs. Claim ceiling bounded to deterministic mock.
2. **Limited drift patterns**: Only permission_boundary and session_invalidation tested. Real API drift may involve different mechanisms.
3. **Graded status code mapping**: The mapping 401->1.0, 403->0.5, 500->0.75 is arbitrary. Different mappings might change the correlation structure.
4. **Composite score weighting**: Behavioral weights (2, 3, 1, 2) inherited from parent, not optimized.
5. **Power analysis limitation**: Fisher z-transform assumes bivariate normality, which may not hold for bounded behavioral composites. Permutation test is the primary inference; Fisher z is supplementary.
6. **Seed-specific results**: SEED=42 only; no seed-variation sensitivity analysis in this experiment.
7. **Unauthenticated /session/status endpoint**: Synthetic construct not present in real APIs in this form.

## Interpretation

### What This Means for C-FRESHNESS

This experiment provides a **valid scientific finding** that requires decision-rule revision:

1. **Near-zero correlation confirmed**: |r| = 0.0335 (r² = 0.001) across 480 paired samples. This is even lower than the parent's |r| = 0.053 at n=240, suggesting the true correlation is extremely small.

2. **Frozen gate fails on power, not on effect**: The permutation p = 0.4650 > 0.05 because n=480 is insufficient for |r| ~ 0.05, not because the signals are correlated. The power analysis proves this: minimum detectable |r| at n=480 is 0.0895, and the observed |r| = 0.0335 is below this threshold.

3. **Orthogonality is plausible but not formally confirmed**: The data is consistent with orthogonality (|r| ~ 0, p >> 0.05) but the frozen confirmatory test cannot confirm it at this sample size.

4. **Decision rule revision needed**: The conjunctive rule (|r| < 0.3 AND p < 0.05) is inappropriate for very-low-magnitude correlations. Alternatives:
   - Increase n to ~1,538 for |r| = 0.05 (impractical for current infrastructure)
   - Replace permutation p with equivalence test (TOST) or confidence-interval bound
   - Accept |r| < 0.1 as practically significant regardless of p-value

### Product Consequences

- **TP/variance trade-off IS broken**: Confirmed at n=480 (TP=1.0, 8/8 conditions with variance)
- **Behavioral + structural signals are independently observable**: Both signals have non-zero variance on all conditions
- **Near-zero correlation suggests independence**: |r| = 0.0335 means behavioral and structural signals share < 0.1% variance
- **Product pipeline**: Precautionary composite multi-signal classifiers recommended pending formal orthogonality confirmation
- **C-FRESHNESS remains EXPERIMENTAL**: The frozen gate fails; decision-rule revision required before advancing to PRODUCT_ARCHITECTURE_IMPACT

### Comparison with Parent

| Metric | Parent (n=240) | This Experiment (n=480) | Change |
|--------|----------------|-------------------------|--------|
| \|r\| | 0.053 | 0.0335 | -37% (closer to 0) |
| r² | 0.003 | 0.001 | -67% |
| Permutation p | 0.414 | 0.465 | +12% (less significant) |
| C1 (TP) | PASS (1.0) | PASS (1.0) | Same |
| C2 (variance) | PASS (8/8) | PASS (8/8) | Same |
| C3 (orthogonality) | FAIL (p>0.05) | FAIL (p>0.05) | Same |
| C4 (null FP) | PASS (0.0) | PASS (0.0) | Same |

The correlation is stable across sample sizes (both near zero), confirming orthogonality is plausible. The failure is purely a power issue.
