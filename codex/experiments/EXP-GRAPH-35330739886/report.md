# EXP-GRAPH-35330739886 — Execution Report

## Executive Summary

This experiment replaces the frozen permutation p<0.05 decision rule for C-FRESHNESS orthogonality with a TOST equivalence test and confidence-interval upper bound, applied to the parent's n=480 paired samples. The outcome is **MIXED**: the 95% CI upper bound on |r| is **0.123**, which passes equivalence margins delta >= 0.15 but fails for delta <= 0.12.

**Key Finding**: The CI upper bound (0.123) falls in the 0.10-0.15 range that the preregistration identified as the product-decision boundary. At delta=0.15 (shared variance < 2.25%), orthogonality is confirmed and parallel channels are justified. At delta=0.10 (shared variance < 1%), the current sample is insufficient (minimum n=873 required for CI bound).

---

## 1. Parent Metrics Verification (C1, C2, C4)

All inherited controls verified from parent `raw_evidence/experiment_data.json`:

| Control | Threshold | Observed | Pass |
|---------|-----------|----------|------|
| C1_drift_tp | mean_tp >= 0.85, all Wilson lower > 0.75 | mean=1.0, Wilson lower=0.940 | **PASS** |
| C2_variance | >= 6/8 conditions with std > 0 | 8/8 conditions | **PASS** |
| C4_null_control | FP = 0.0 on noise-only | FP = 0.0 (240 samples) | **PASS** |

No new HTTP requests were made. These are inherited measurements verified against parent raw evidence.

---

## 2. Equivalence Test Results (C3)

### 2.1 Core Statistics

| Metric | Value |
|--------|-------|
| n (paired samples) | 480 |
| Pearson r | 0.0335 |
| \|r\| | 0.0335 |
| r^2 | 0.001 |
| Pearson p | 0.463 |
| Fisher z | 0.0336 |
| SE(z) | 0.0458 |

### 2.2 Confidence Interval

| CI Type | Bound | Value |
|---------|-------|-------|
| 95% two-sided | Lower | -0.056 |
| 95% two-sided | Upper | **0.123** |
| One-sided 95% | Upper | 0.108 |

The 95% CI is [-0.056, 0.123]. The upper bound **0.123** is the binding constraint for the decision rule.

### 2.3 TOST Equivalence Test

| Delta | r+delta | p_lower | r-delta | p_upper | TOST | CI bound |
|-------|---------|---------|---------|---------|------|----------|
| 0.10 | 0.134 | 0.002 | -0.066 | 0.073 | FAIL | FAIL |
| 0.12 | 0.154 | <0.001 | -0.086 | 0.030 | **PASS** | FAIL |
| 0.15 | 0.184 | <0.001 | -0.116 | 0.005 | **PASS** | **PASS** |
| 0.20 | 0.234 | <0.001 | -0.166 | <0.001 | **PASS** | **PASS** |

**Critical discrepancy at delta=0.12**: TOST passes (both one-sided p < 0.05) but the CI bound fails (0.123 > 0.12). This occurs because TOST uses a one-sided critical value (z=1.645) while the CI-based decision rule uses a two-sided 95% CI (z=1.96). The frozen decision rule specifies the CI bound test, so delta=0.12 is a **fail** under the preregistered criterion.

### 2.4 Decision Rule Application

- C3 passes for delta >= 0.15 (CI upper bound 0.123 < 0.15)
- C3 fails for delta <= 0.12 (CI upper bound 0.123 > 0.12)
- Per frozen decision rule: **MIXED** when C1-C2-C4 PASS and C3 passes only for delta >= 0.15

---

## 3. Sample Size Trade-off Surface

| Delta | Min n (TOST) | Min n (CI bound) | Current n=480 |
|-------|-------------|-------------------|---------------|
| 0.10 | 155 | **873** | Insufficient for CI |
| 0.12 | 118 | **518** | Insufficient for CI |
| 0.15 | 84 | 287 | **Sufficient** |
| 0.20 | 53 | 142 | **Sufficient** |

At n=480, the minimum detectable |r| for the CI bound to be < delta:
- delta=0.10: requires n >= 873 (need ~1.8x current sample)
- delta=0.12: requires n >= 518 (need ~1.1x current sample, only 38 more)
- delta=0.15: requires n >= 287 (current n=480 is sufficient with 67% margin)
- delta=0.20: requires n >= 142 (current n=480 is 3.4x sufficient)

---

## 4. Per-condition Correlation Analysis

| Condition | r | p | n | Notes |
|-----------|---|---|---|-------|
| PB+optional_field | 0.000 | 1.000 | 60 | Constant behavioral (b_std=0) |
| PB+description | 0.000 | 1.000 | 60 | Constant behavioral (b_std=0) |
| PB+response_time | 0.000 | 1.000 | 60 | Constant behavioral (b_std=0) |
| PB+field_type | 0.000 | 1.000 | 60 | Constant behavioral (b_std=0) |
| SI+optional_field | **-0.314** | **0.014** | 60 | Only significant condition |
| SI+description | -0.044 | 0.738 | 60 | |
| SI+response_time | 0.158 | 0.228 | 60 | |
| SI+field_type | 0.153 | 0.243 | 60 | |

The pooled r=0.034 is entirely determined by the 4 session_invalidation conditions (240 samples). Permission_boundary conditions contribute zero behavioral variance (constant b=0.333) and thus zero correlation.

The single significant per-condition r=-0.314 (SI+optional_field_addition) is 1 of 8 tests significant at alpha=0.05, which is expected under the global null (expected count: 0.4). The binomial probability of exactly 1 significant test is p=0.031, which is suggestive but not confirmatory.

---

## 5. Product Consequences

### If delta=0.15 is acceptable (MIXED outcome, current state):

- CI upper bound 0.123 < 0.15 confirms orthogonality at <2.25% shared variance
- Product pipeline may integrate behavioral + structural as independent parallel channels
- The 95% CI guarantees with 95% confidence that |r| < 0.123, well below the 0.15 margin

### If delta=0.10 is required:

- CI upper bound 0.123 > 0.10 fails the equivalence test
- Options: (a) increase n to ~873 for CI bound confirmation, (b) accept delta=0.15, or (c) pivot to fused classifiers
- The gap is small: one-sided 95% CI upper = 0.108, very close to 0.10

### Recommendation:

The delta=0.15 margin (shared variance < 2.25%) is likely sufficient for parallel-channel architecture, as it means >97.75% of detection variance is independent. The product should document this equivalence margin as a bounded assumption pending larger-sample confirmation at delta=0.10.

---

## 6. Comparison with Parent

| Metric | Parent (permutation) | This experiment (TOST/CI) |
|--------|---------------------|--------------------------|
| r | 0.0335 | 0.0335 (confirmed) |
| Primary test | Permutation p=0.465 | Fisher z CI upper=0.123 |
| C3 gate | FAIL (p > 0.05) | MIXED (CI < 0.15 but > 0.12) |
| Root cause | Underpowered (n=480 < 1538) | Appropriate test for small |r| |
| Product answer | Unknown | Bounded at delta=0.15 |

The parent's permutation p=0.465 was correctly identified as underpowered for the very-low-magnitude correlation. The TOST/CI approach resolves the scientifically meaningful question: "is |r| small enough?" rather than "is |r| exactly zero?" The answer is: yes, for equivalence margins >= 0.15.
