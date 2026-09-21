# EXP-INTEL-35530590171 — Execution Report

## Experiment Identity

- **experiment_id**: `EXP-INTEL-35530590171`
- **lane**: intel
- **parent**: `EXP-INTEL-35476271877` (handoff sha256: 94f853d160ebbabcd115e28dd1d6ad50f738afd289c8bfb2665537a1c78db36a)
- **claim_ids**: `C-MEAS-VALID`, `C-PRODUCT-ECON`
- **frozen_at**: 2026-09-20T18:57:02+00:00

## Question

Does a corrected SNR decomposition using across-iteration margin_std (not within-iteration within-type SE) as the noise scale pass C1-equivalent validation, enabling a reliable extrapolation to full-DOM element counts?

## Frozen Decision Rule

Conjunctive:
1. **C1_CORRECTED_MODEL_VALID**: Both predicted agreement at n=15 and n=20 within 10pp of observed
2. **C2_MECHANISM_CORRECTED**: Corrected SNR at n=20 < 3.0 (margin-deficit) OR CV_listing or CV_detail > 0.1
3. **C3_EXTRAPOLATION_FALSIFIES_FULL_DOM**: Extrapolated agreement at n=50 < 80%

Verdict: NOT C1 → MEASUREMENT_INVALID

## Results

### Corrected Model Predictions

| n | mean(M_i) | std(M_i) | Corrected SNR | Φ(SNR) | Observed | Residual | C1 |
|---|-----------|----------|---------------|--------|----------|----------|-----|
| 5 | −4.90e-05 | 4.97e-05 | −0.986 | 0.162 | — | — | — |
| 10 | −1.35e-04 | 1.06e-04 | −1.275 | 0.101 | — | — | — |
| 15 | 2.66e-05 | 1.63e-04 | 0.163 | 0.5648 | 0.4998 | 0.065 | PASS |
| 20 | 3.97e-04 | 6.23e-04 | 0.637 | 0.7379 | 0.5595 | 0.178 | **FAIL** |

**C1_CORRECTED_MODEL_VALID: FAIL** — n=15 passes (6.5pp residual) but n=20 fails (17.8pp residual, 7.8pp above threshold).

### Comparison with Parent Model

| n | Parent Φ(SNR_SE) | Parent residual | Corrected Φ(SNR_std) | Corrected residual | Improvement |
|---|-------------------|-----------------|----------------------|--------------------|----|
| 15 | 1.0000 | 0.5002 | 0.5648 | 0.065 | 7.7× |
| 20 | 1.0000 | 0.4405 | 0.7379 | 0.178 | 2.5× |

The corrected model dramatically improves over the parent (which used within-iteration SE ~1e-5 as noise). margin_std (~1e-4 to 6e-4) is the empirically relevant noise scale. However, the corrected model still fails at n=20.

### Root Cause of n=20 Failure

The corrected model over-predicts because `std(M_i)` grows faster than `mean(M_i)` as n increases:

- At n=15: mean = 2.66e-05, std = 1.63e-04 → SNR = 0.163
- At n=20: mean = 3.97e-04, std = 6.23e-04 → SNR = 0.637

The 14.9× increase in mean is offset by the 3.8× increase in std, inflating the SNR ratio at n=20. The model predicts 73.8% agreement when the observed is 56.0%.

### Mechanism Classification (gated behind failed C1)

- Corrected SNR at n=20: 0.637 < 3.0 → **margin_deficit** regime
- CV_listing: 0.0046 (< 0.1, no task variance)
- CV_detail: 0.0335 (< 0.1, no task variance)
- Classification: **margin_deficit** (C2 PASS, but unusable due to C1 FAIL)

### Extrapolation to n=50 (gated behind failed C1)

Power-law fits on the 4 data points (n=5,10,15,20):
- |margin(n)| = 1.11e-05 × n^0.876 (R² = 0.197, poor — sign crossing)
- margin_std(n) = 2.93e-06 × n^1.643 (R² = 0.867, reasonable)

At n=50: predicted agreement = 0.575 (PI90 [0.511, 0.774])

**C3_EXTRAPOLATION_FALSIFIES_FULL_DOM: PASS** (predicted < 80%) — but gated behind failed C1. Cannot be used to justify product decisions.

### Diagnostic: Direct Indicator Statistic

Under template invariance, ranking agreement equals `proportion(margin_i > 0)`:

| n | prop(margin>0) | Observed | Residual |
|---|----------------|----------|----------|
| 15 | 0.4996 | 0.4998 | 0.02pp |
| 20 | 0.5654 | 0.5595 | 0.59pp |

This near-exact match confirms the mechanism: agreement is determined by the fraction of iterations where the margin is positive. The corrected model (Φ(mean/std)) fails to capture this because it conflates the sign-determining mean with the magnitude-determining std.

### Null Control

Random noise model: 500,000 simulations → agreement 0.499208 (expected ~50%).

Corrected model does NOT outperform the null:
- n=15: model error 0.065 vs null error 0.0006
- n=20: model error 0.178 vs null error 0.060

### Baseline Reproduction

All parent values reproduced within hash-seed variation:
- Canonical agreement n=20: 0.5654 vs 0.5595 (delta +0.0059)
- Canonical eta2 n=20: 0.9195 vs 0.9205 (delta −0.0010)
- Per-task agreement n=20: 0.78 vs 0.7865 (delta −0.0065)

## Frozen Verdict

**MEASUREMENT_INVALID** — C1 fails at n=20 (residual 17.8pp > 10pp threshold). Per frozen conjunctive rule, NOT C1 → MEASUREMENT_INVALID regardless of C2/C3.

The corrected model is a substantial improvement over the parent (7.7× and 2.5× residual reduction) and confirms margin_std is the right noise scale direction. However, it does not pass the frozen validation gate because the SNR ratio over-predicts at n=20, where std grows faster than mean.

## Scientific Interpretation

1. **margin_std is better than within-iteration SE**: The corrected model improves residuals by 2.5–7.7× over the parent. This is strong evidence that across-iteration margin variation is the relevant noise scale.

2. **The model still fails because mean and std scale differently**: The power-law exponents differ (b=0.876 for |margin|, d=1.643 for std), causing the SNR to increase with n. This means the model predicts improving agreement faster than observed.

3. **The 56% plateau is real but unexplained**: The direct indicator statistic confirms agreement equals the fraction of positive-margin iterations. The corrected model cannot explain why this fraction is ~56% at n=20 rather than the model-predicted ~74%.

4. **Full-DOM question remains OPEN**: The C3 extrapolation (predicted 57.5% at n=50) suggests the plateau persists, but it is gated behind failed C1 and built on a power law with poor fit (R²=0.197 for |margin|).

## Product Consequence

**No usable prediction**: C1 fails, so the experiment provides no justified basis for either Docker re-collection investment or non-recipe density adoption. The MIXED program's central question (is the 56% plateau structural?) remains unresolved.

## Validity Threats

1. **Power-law extrapolation from n=4 points with sign crossing**: The margin sign crosses zero between n=10 and n=15, making |margin| power-law fitting unreliable (R²=0.197). PI90 width 26.3pp reflects this uncertainty.

2. **Template invariance tautology**: Under template invariance, same-type canonical densities are scalar multiples, making rho=1.0 a mathematical consequence. The corrected model does not address this structural issue.

3. **Single site (Magento), small type sample (n=3 per type)**: Generalization beyond this specific setup is untested.

4. **PYTHONHASHSEED=0 variation**: Small quantitative differences from parent runs due to set-iteration order. These do not affect the C1 verdict.
