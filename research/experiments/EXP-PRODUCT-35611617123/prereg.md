# EXP-PRODUCT-35611617123 — Preregistration

## Status

DESIGN ONLY. Not yet frozen.

## Experiment Identity

- **Experiment ID**: EXP-PRODUCT-35611617123
- **Lane**: product
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Parent**: EXP-PRODUCT-35572180893 (Gaussian overlap discrimination, FALSIFIED — orthogonality break at 50% overlap)

## Question

Does increasing sample size from n=480 to n=1000 at 50% Gaussian overlap resolve the marginal orthogonality failure (CI upper 0.168 vs delta 0.15, TOST p_upper=0.061) under Bonferroni correction for 3 overlap conditions — and does this recover the 50% operating point for the freshness guard?

## Hypothesis

The parent's 50% orthogonality failure (r=0.080, CI upper 0.168 at n=480) is a Type I error from underpowering: the true population correlation at 50% Gaussian overlap is below delta=0.15, and increasing n to 1000 will narrow the CI enough to pass TOST equivalence at the Bonferroni-corrected alpha=0.0167. The calibrated threshold at 50% (0.27) will remain valid, recovering the 0-50% usable operating envelope.

## Falsifier

If the 50% orthogonality failure persists at n=1000 (CI upper >= 0.15 after Bonferroni correction), OR if the calibrated threshold becomes None at 50% with larger n, OR if any of the 0%/25% regression controls fail — then the 50% operating point is a real breakdown, not a sampling artifact, and the usable envelope remains bounded to 0-25% overlap.

## Prior Evidence (from parent handoff)

The parent experiment (EXP-PRODUCT-35572180893) tested 5 overlap conditions (0%,25%,50%,75%,100%) using Gaussian noise/refresh distributions with sigma=0.05. Key findings:

- Calibrated threshold increases gradually under genuine overlap: 0.20 (0%) -> 0.25 (25%) -> 0.27 (50%) — confirms threshold is not flat-then-jump (parent's uniform-shift artifact resolved)
- FP at threshold 0.20 increases monotonically: 0.42% (0%) -> 23.75% (25%) -> 44.17% (50%) -> 67.5% (75%) -> 96.25% (100%)
- Orthogonality TOST PASS at 0% (r=-0.023, CI upper 0.066), 25% (r=-0.029, CI upper 0.061), 75% (r=0.046, CI upper 0.135), 100% (r=-0.026, CI upper 0.064)
- **Orthogonality FAILS at 50%**: r=0.080, CI upper 0.168 > delta 0.15, TOST p_upper=0.061
- No valid threshold at 75% and 100% (operating envelope collapses)
- C1 structural discrimination 0.8333 across all conditions
- Continuous injection: 452-460 unique behavioral scores per condition

**Established usable envelope**: 0-25% overlap (valid threshold, orthogonality holds, FP moderate). Marginal at 50% (valid threshold but orthogonality fragile). Unusable at >=75% (no valid threshold).

**The 50% orthogonality failure is the critical uncertainty**: CI upper 0.168 is only 12% above delta 0.15. With n=480, the test may be underpowered for detecting equivalence at this borderline. The non-monotonic pattern (r=0.080 at 50%, r=0.046 at 75%, r=-0.026 at 100%) is suspicious — a real effect would likely be monotonic.

## Design

### Conditions

| Condition | mu_noise | Target overlap | n per condition | Notes |
|-----------|----------|----------------|-----------------|-------|
| 0% | 0.095 | ~0% | 480 | Regression control — must PASS |
| 25% | 0.1663 | ~25% | 480 | Regression control — must PASS |
| 50% | 0.195 | ~50% | 1000 | Primary test condition |

### Rationale for condition selection

- **0% and 25%**: Regression controls. Both passed at n=480 in the parent. Must replicate to confirm infrastructure consistency.
- **50%**: The single failing condition from the parent. n=1000 provides ~2x parent sample size, narrowing the CI width by ~sqrt(480/1000) ≈ 0.69x. If parent CI half-width was 0.088 (0.168 - 0.080), the expected half-width at n=1000 is ~0.061, giving expected CI upper ~0.141 — below delta 0.15 if r is truly ~0.08.
- **75% and 100% excluded**: These are tautological boundary conditions (no valid threshold exists). Not actionable for product deployment. The parent already established they are unusable.

### Sample Size Justification

Parent n=480 produced CI upper 0.168 at 50% overlap (r=0.080). The CI half-width was 0.088. At n=1000:
- Expected SE ≈ sqrt((1-r²)/(n-2)) ≈ sqrt((1-0.0064)/998) ≈ 0.0315
- Expected 95% CI upper ≈ 0.080 + 1.96 * 0.0315 ≈ 0.142
- This is below delta 0.15, so TOST should PASS if r is truly ~0.08

However, if the true r is higher (e.g., 0.10), CI upper would be ~0.162 — still above 0.15. The experiment is designed to discriminate between these scenarios.

### Bonferroni Correction

Three overlap conditions are tested (0%, 25%, 50%). Bonferroni-corrected alpha = 0.05/3 = 0.0167 for each TOST test.

### Overlap Model

Identical to parent (EXP-PRODUCT-35572180893):

- **Failure distribution**: N(mu=0.295, sigma=0.05)
- **Noise distribution**: N(mu_noise, sigma=0.05)
- **FAILURE_THRESHOLD**: 0.20
- **Overlap definition**: P(noise_score > FAILURE_THRESHOLD) — verified empirically
- Noise means computed via inverse CDF: mu_noise = FAILURE_THRESHOLD + sigma * Phi_inv(1 - target_overlap)

### Threshold Sweep

50 points [0.05, 0.06, ..., 0.54] in 0.01 increments — identical to parent for comparability.

### Infrastructure

Same mock server as parent: Flask 3.1.3 + PyJWT HS256 + SQLite WAL-mode on localhost. Same behavioral_score computation (structural composite = hash(body)%10000, behavioral composite = session_validity * (1 + permission_boundary + token_freshness)).

## Controls

### Positive Controls

1. **PC-0%-TOST**: At 0% overlap, TOST must PASS (CI upper < 0.15) at n=480 — replicates parent
2. **PC-25%-TOST**: At 25% overlap, TOST must PASS (CI upper < 0.15) at n=480 — replicates parent
3. **PC-0%-THRESHOLD**: At 0% overlap, calibrated threshold must be 0.20 (not None) — replicates parent
4. **PC-25%-THRESHOLD**: At 25% overlap, calibrated threshold must be not None — replicates parent
5. **PC-50%-FP-BINDING**: At 50% overlap, FP at threshold 0.20 must exceed 0.10 (genuine overlap produces false accepts)

### Null Controls

1. **NC-50%-PARENT-REPLICATION**: At 50% overlap with n=480 (parent sample size), TOST must FAIL — confirms parent result is reproducible and not an artifact
2. **NC-NULL-OVERLAP-0**: At 0% overlap, FP at threshold 0.20 must be <= 0.01 (near-zero)

### Regression Controls

1. **RC-C1-DISCRIMINATION**: C1 structural discrimination must be > 0.5 at all conditions — consistent with 7+ prior experiments
2. **RC-CONTINUOUS-INJECTION**: Unique behavioral scores >= 5 at all conditions — confirms continuous severity gradient

## Decision Tree

```
Step 1: Check regression controls
  - If C1 discrimination <= 0.5 at any condition → MEASUREMENT_INVALID
  - If unique behavioral scores < 5 at any condition → MEASUREMENT_INVALID

Step 2: Check null controls
  - If FP at 0% overlap > 0.01 → MEASUREMENT_INVALID
  - If TOST PASS at 50% overlap with n=480 → MEASUREMENT_INVALID (parent replication failed)

Step 3: Check 0%/25% regression
  - If TOST FAIL at 0% or 25% → MEASUREMENT_INVALID (regression broken)

Step 4: Primary test — 50% overlap at n=1000
  - If TOST PASS at 50% (CI upper < 0.15, alpha=0.0167 Bonferroni) AND calibrated_threshold is not None → RECOVERED
  - If TOST FAIL at 50% (CI upper >= 0.15) OR calibrated_threshold is None → CONFIRMED-BREAKDOWN
  - Otherwise → MIXED
```

## Consequences

**Positive (RECOVERED)**: The 50% orthogonality failure was a sampling artifact. The freshness guard's usable envelope extends to 0-50% Gaussian overlap (threshold 0.20-0.27). This broadens the production deployment window significantly. C-FRESHNESS moves toward PRODUCT_CORE eligibility with wider deployment envelope.

**Negative (CONFIRMED-BREAKDOWN)**: The 50% orthogonality failure is a real effect. The usable envelope remains bounded to 0-25% overlap. Production deployment requires keeping noise/refresh overlap below 25% — a tighter constraint that may be unrealistic for high-stochasticity environments. C-FRESHNESS stays EXPERIMENTAL with narrowed deployment envelope.

## Scope and Limitations

- This experiment tests only Gaussian overlap on localhost mock — not production noise distributions
- The Bonferroni correction is conservative; if only the 50% condition is truly tested (0%/25% are regression), a less conservative correction might be appropriate but Bonferroni is the pre-registered choice
- The experiment does not test whether production-like noise (non-Gaussian, heavy-tailed, multimodal) produces similar orthogonality behavior
- The mock server infrastructure is identical to the parent, so any confounds specific to Flask/PyJWT/SQLite persist
