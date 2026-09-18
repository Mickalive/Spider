# EXP-GRAPH-35308806969 — Preregistration

## Title

Pooled Paired-Sample Orthogonality Test at n=480 with Power Analysis: Can Doubled Sample Size Confirm Behavioral-Structural Signal Independence for C-FRESHNESS?

## Parent

EXP-GRAPH-35262262505 (FAIL — C3 permutation p=0.414 > 0.05 despite |r|=0.053)

## Claim

C-FRESHNESS: SPIDER can detect when inherited knowledge is stale. This experiment tests the orthogonality of behavioral and structural detection channels.

## 1. Question

Does doubling paired-sample size from 240 to 480 confirm |r|<0.3 with permutation p<0.05 for behavioral-structural signal orthogonality — and does a formal power analysis reveal whether n=480 is sufficient for the frozen permutation test at |r|~0.05?

## 2. Hypothesis

The parent achieved near-zero pooled correlation (|r|=0.053, r²=0.003, n=240) but failed the frozen C3 gate (p=0.414). The parent handoff recommends n>=480. However, Fisher z-transform power analysis indicates n≈1,568 is needed for |r|=0.05 at α=0.05. At n=480, expected p≈0.26. This experiment tests the parent recommendation and includes formal sensitivity analysis.

## 3. Design

### 3.1 Server

Flask 3.1.3 + PyJWT 2.14.0 HS256 on localhost, identical to parent. Endpoints: /session/status (401/403/500 based on session validity), /schema (unauthenticated structural observability).

### 3.2 Conditions

**8 co-occurring conditions** (2 drift patterns × 4 structural noise patterns):
- Drift: permission_boundary (write=False, admin=False) × session_invalidation (clear session store + graded status)
- Structural: optional_field_addition, description_change, response_time_jitter, field_type_normalization

**4 noise-only conditions** (null control): structural noise without drift.

### 3.3 Sample Size

**60 samples per condition** (doubled from parent's 30):
- 8 co-occurring × 60 = 480 paired (behavioral, structural) samples
- 4 noise-only × 60 = 240 null control samples
- Total: 720 request sequences

### 3.4 Session Invalidation Design

ALL session_invalidation samples have session_change=1 (every session is invalid). Session_status_check varies by randomly choosing HTTP status from {401, 403, 500} with equal probability. Mapping: 401→1.0, 403→0.5, 500→0.75. This preserves the parent's validated TP/variance mechanism.

### 3.5 RNG

SEED=42, per-condition independent RNG, identical to parent. Deterministic and reproducible.

## 4. Measures

### 4.1 C1 — Drift True Positive Rate

- **Definition**: Fraction of drift samples where behavioral composite correctly detects drift.
- **Threshold**: mean TP ≥ 0.85 AND all Wilson score lower CI > 0.75.
- **Method**: Exact Wilson score interval for binomial proportion at each condition, then mean across 8 co-occurring conditions.

### 4.2 C2 — Within-Condition Variance

- **Definition**: Fraction of co-occurring conditions where behavioral_std > 0 AND structural_std > 0.
- **Threshold**: ≥ 6 of 8 conditions have std > 0 for both signals.

### 4.3 C3 — Orthogonality (PRIMARY)

- **Definition**: Pearson correlation on pooled paired (behavioral_i, structural_i) scores from all 8 co-occurring conditions.
- **Threshold**: |r| < 0.3 AND permutation p < 0.05.
- **Permutation test**: 10,000 label-shuffled permutations of the structural scores, two-sided, against the observed |r|.
- **Power analysis (MANDATORY)**: Fisher z-transform computation:
  - (a) Minimum detectable |r| at n=480 for p<0.05 (two-sided α=0.05).
  - (b) Minimum n for |r|=0.05 to achieve p<0.05 (two-sided α=0.05).
  - Report both values in result.json under `metrics.power_analysis`.

### 4.4 C4 — Null False Positive Rate

- **Definition**: FP rate on noise-only conditions (schema noise without drift).
- **Threshold**: FP = 0.0.

### 4.5 Positive Controls

- **PC-TP-WITH-VARIANCE**: session_invalidation conditions produce behavioral std > 0 AND TP = 1.0.
- **PC-PERMISSION-BOUNDARY-DETECTION**: permission_boundary conditions detect drift at rate 1.0.

## 5. Decision Rule

**PASS** if ALL of:
1. C1_drift_tp: mean TP ≥ 0.85 AND all Wilson lower CI > 0.75
2. C2_variance: ≥ 6/8 co-occurring conditions have std > 0 for both signals
3. C3_orthogonality: |r| < 0.3 AND permutation p < 0.05
4. C4_null_control: FP = 0.0

**FAIL** if any criterion fails.

**MIXED** (new outcome class): If C1-C2 PASS and C3 fails ONLY on permutation p (|r| < 0.3 but p ≥ 0.05) AND the power analysis confirms n=480 is underpowered for the observed |r|, the outcome is MIXED — the frozen gate fails but the near-zero correlation with explicit power bound is a valid scientific finding. This MIXED outcome is NOT evidence of non-orthogonality; it requires decision-rule revision in the next cycle.

**MEASUREMENT_INVALID** if < 6/8 conditions have sufficient variance or < 480 paired samples.

## 6. Outcomes and Consequences

### Positive (C1-C4 PASS)
- TP/variance trade-off broken AND orthogonality formally confirmed
- C-FRESHNESS advances to PRODUCT_ARCHITECTURE_IMPACT
- Product pipeline: independent parallel channels (behavioral + structural)

### Mixed (C1-C2 PASS, C3 FAIL with power-confirmed underpowering)
- TP/variance trade-off broken, orthogonality plausible but not confirmed
- Decision rule requires revision: either increase n to ~1,600, or replace permutation p with equivalence test or confidence-interval bound for very-low-magnitude correlations
- Product pipeline: composite multi-signal classifiers (precautionary)
- C-FRESHNESS remains EXPERIMENTAL pending revised confirmatory test

### Negative (C1-C2 PASS, C3 FAIL with |r| >= 0.3)
- Signals are confirmed non-orthogonal
- Product pipeline: fused classifiers (mandatory)
- C-FRESHNESS pivots to composite detection architecture

### C1 FAIL
- session_status_check mechanism exhausted
- Fundamentally different variance mechanism needed
- C-FRESHNESS blocked on detection channel diversity

## 7. Validity Threats

1. **Deterministic mock server**: Flask + PyJWT localhost does not capture real API stochasticity (DB/cache/CDN, OAuth/OIDC). Claim ceiling bounded to deterministic mock.
2. **Arbitrary status mapping**: 401→1.0, 403→0.5, 500→0.75 is not grounded in real API behavior. Any mapping creating variance while keeping session_change=1 tests the core hypothesis.
3. **Unauthenticated /schema endpoint**: Synthetic construct; practical in few real API deployments.
4. **Power analysis limitation**: Fisher z-transform assumes bivariate normality, which may not hold for bounded behavioral composites. Permutation test is the primary inference; Fisher z is supplementary.
5. **Seed-specific results**: SEED=42 only; no seed-variation sensitivity analysis in this experiment.

## 8. Artifacts to Reuse from Parent

- `mock_server.py` from EXP-GRAPH-35262262505 (Flask 3.x + PyJWT, /session/status 401/403/500, /schema unauthenticated)
- `run_experiment.py` from EXP-GRAPH-35262262505 (8 co-occurring conditions, graded session_status_check)
- Modifications: change `n_samples_per_condition` from 30 to 60; add Fisher z power analysis computation; add MIXED outcome class to decision logic.

## 9. Power Analysis (Pre-Registered)

For a two-sided test of H0: ρ=0 using Pearson r:

**Minimum n for |r|=0.05 at α=0.05**:
- Fisher z = 0.5 * ln((1+0.05)/(1-0.05)) = 0.05004
- Required: z > 1.96 * √(1/(n-3))
- n > 3 + (1.96/0.05004)² = 3 + 1533.5 ≈ 1,537
- With continuity correction: n ≈ 1,568

**Expected p at n=480 for |r|=0.05**:
- SE_z = 1/√(477) = 0.04588
- z = 0.05004 / 0.04588 = 1.091
- p ≈ 0.275 (two-sided)

**Minimum detectable |r| at n=480 for p<0.05**:
- |r| > tanh(1.96 / √(477)) = tanh(0.08987) ≈ 0.0897

This pre-registered analysis predicts n=480 will NOT achieve p<0.05 for |r|~0.05. The experiment tests this prediction.
