# EXP-INTEL-35538868377 — Execution Report

## Experiment Identity

- **experiment_id**: `EXP-INTEL-35538868377`
- **lane**: intel
- **parent**: `EXP-INTEL-35530590171` (handoff sha256: 252702537489bc90a720725382a8387c37652e995ba46b8e0e9eabe638701af1)
- **claim_ids**: `C-MEAS-VALID`, `C-PRODUCT-ECON`
- **frozen_at**: 2026-09-20T21:36:14.546202+00:00

## Question

Can a sign-magnitude-separated noise decomposition (Phi(median(|M|)/std)) or a direct sign-fraction power law (proportion(margin_i>0) modeled as saturating function of n) pass C1-equivalent validation at n=15 and n=20, providing a validated extrapolation path to full-DOM n=50/82?

## Frozen Decision Rule

Conjunctive:

1. **C1_EITHER_MODEL_VALID**: At least one of Model A or Model B predicts observed ranking agreement at n=15 and n=20 within 10 percentage points. PASS if either passes at BOTH n; FAIL if both fail at either n.
2. **C2_SIGN_FRACTION_FIT_QUALITY**: Model B achieves R² >= 0.90 on 4-point training data (n=5/10/15/20). PASS if R²>=0.90; FAIL if R²<0.90.
3. **C3_SIGN_FRACTION_EXTRAPOLATION_BELOW_80**: Model B extrapolation predicts proportion(margin>0) at n=50 < 0.80. PASS if <0.80; FAIL if >=0.80.

Verdict:
- NOT C1 → MEASUREMENT_INVALID
- C1 AND NOT C2 → MIXED
- C1 AND C2 AND C3 → SIGN_FRACTION_VALIDATED
- C1 AND C2 AND NOT C3 → SIGN_FRACTION_PREDICTS_CROSSING

## Results

### Model A: Phi(median(|M_i|)/std(M_i))

| n | median(|M|) | std(M) | SNR_median | Phi(SNR) | Observed | Residual | C1 (10pp) |
|---|-------------|--------|------------|----------|----------|----------|-----------|
| 5 | 0.0 | 4.97e-05 | 0.000 | 0.5000 | 0.0000 | 0.5000 | 50.00pp FAIL |
| 10 | 7.12e-05 | 1.06e-04 | 0.674 | 0.7498 | 0.0000 | 0.7498 | 74.98pp FAIL |
| 15 | 1.66e-04 | 1.63e-04 | 1.017 | 0.8455 | 0.4996 | 0.3459 | 34.59pp **FAIL** |
| 20 | 4.30e-04 | 6.23e-04 | 0.690 | 0.7550 | 0.5654 | 0.1896 | 18.96pp **FAIL** |

**C1_ModelA_valid: FAIL** — Both n15 and n20 exceed 10pp threshold. Falsifier F1 triggered at both points. Median-based decomposition does NOT capture the flip mechanism; it over-predicts by 34.6pp at n15 and 19.0pp at n20. It performs worse than the corrected Phi(mean/std) model (which had 6.5pp at n15, 17.8pp at n20).

For comparison, Phi(mean/std) from parent at same n: 0.5648 at n15 (6.5pp) and 0.7379 at n20 (17.8pp). ModelA is worse at both.

### Model B: Sign-Fraction Saturating Power Law

Fitted: `proportion(n) = a * n^b / (1 + a*n^b)` on n=5/10/15/20, curve_fit, 4 points.

- **Fit params**: a = 2.289e-05 (perr 1.16e-04), b = 3.758 (perr 1.81)
- **R²** = 0.8797 (< 0.90 threshold) → **C2 FAIL** (F4 triggered)
- **Fitted vs observed**:

| n | Observed prop>0 | Fitted prop | Residual | Abs resid |
|---|-----------------|-------------|----------|-----------|
| 5 | 0.0000 | 0.0096 | -0.0096 | 0.96pp |
| 10 | 0.0000 | 0.1159 | -0.1159 | 11.59pp |
| 15 | 0.4996 | 0.3757 | +0.1239 | 12.39pp |
| 20 | 0.5654 | 0.6395 | -0.0741 | 7.41pp |

At C1 thresholds:
- Strict (2pp, per prereg falsifier F2): n15 12.39pp >2pp FAIL, n20 7.41pp >2pp FAIL → **C1_ModelB_valid (2pp): FAIL**
- Loose (10pp, per frozen decision_rule): n15 12.39pp >10pp FAIL → **C1_ModelB_valid (10pp): FAIL**

**C1_EITHER_MODEL_VALID: FAIL** — Neither ModelA nor ModelB passes at both n15 and n20 within 10pp.

### Extrapolation (gated behind failed C1/C2)

ModelB predicts:
- n50: 0.9823 (bootstrap PI90 [0.9806, 0.9838], B=2000 per-iteration bootstrap, seed 999, median 0.9823)
- n82: 0.9972 (PI90 [0.9968, 0.9975])

**C3_below_80: FAIL** — n50 prediction 0.982 > 0.80 would trigger SIGN_FRACTION_PREDICTS_CROSSING if C1/C2 had passed, but is gated. The narrow PI90 reflects fit stability, not validity.

### Comparison with Baselines

| Baseline | Residual | ModelA n15/20 | ModelB n15/20 | Beat? |
|----------|----------|---------------|---------------|-------|
| B1 parent SNR n15 (0.5002) | 50.02pp | 34.59pp (1.4x better) | 12.39pp (4.0x better) | Both improve |
| B2 parent SNR n20 (0.4405) | 44.05pp | 18.96pp (2.3x better) | 7.41pp (5.9x better) | Both improve |
| B3 corrected Phi(mean/std) n20 (0.1784) | 17.84pp | 18.96pp (worse) | 7.41pp (2.4x better) | Only B beats |
| B4 diagnostic (0.02/0.59pp) | 0.02/0.59pp | 34.59/18.96 | 12.39/7.41 | Diagnostic still best |
| B5 null 0.499208 | null err 0.0004/0.0662 | ModelA 0.3459/0.1896 | ModelB 0.1239/0.0741 | Neither beats null |
| B6 parent extrapol n50 1.0 | — | — | 0.982 | — |

### Controls

- **PC1_SIGN_FRACTION_REPRODUCES_OBSERVED**: PASS — Direct proportion(margin>0) = 0.4996 at n15 (0.00pp) and 0.5654 at n20 (0.00pp) within 1pp of observed, reconfirming parent diagnostic.
- **NC1_RANDOM_NOISE_BASELINE**: Random noise 0.499208 within 50% +/-5% (PASS). Best model error at n20 (ModelB 0.0741) > null error 0.0662 (FAIL to beat null).
- **B1/B2**: PASS (improvement direction).
- **B3**: ModelB beats corrected mean/std at n20; ModelA does not.
- **B4**: PASS (reproduced).
- **B5**: verified.
- **B6**: not_gated (extrapolation changed but invalid).

## Frozen Verdict

**MEASUREMENT_INVALID** — NOT C1 triggered. Per frozen conjunctive rule, neither decomposition captures the ranking instability mechanism within the 10pp gate. No model-based extrapolation is justified.

Specifically:
- C1_EITHER_MODEL_VALID: **FAIL** (ModelA 34.59pp/18.96pp, ModelB 12.39pp/7.41pp; best R² model still fails n15 by 2.39pp over 10pp threshold)
- C2_SIGN_FRACTION_FIT_QUALITY: **FAIL** (R² 0.8797 < 0.90, short by 0.0203)
- C3_SIGN_FRACTION_EXTRAPOLATION_BELOW_80: **FAIL** (0.982 > 0.80) but gated.

The two orthogonal corrections both fail for distinct reasons: ModelA because median|M|/std still overestimates agreement (Phi inflates), ModelB because a smooth saturating power law cannot fit step-like data (0,0,0.50,0.57) with only 4 points.

## Scientific Interpretation

1. **Median-based decomposition fails more severely than mean-based**: Phi(median|M|/std) residual 34.59pp at n15 vs 6.5pp for Phi(mean/std). Replacing mean with median|M| does not separate sign from magnitude; it instead inflates the SNR (median|M| > |mean| at n15) and worsens over-prediction. The hypothesis that median is sign-invariant and thus cleaner is falsified.

2. **Saturating power law misspecifies the sign-fraction trajectory**: The observed sign fraction is exactly 0.0 at n=5,10 then jumps to 0.50 at n=15. The form a*n^b/(1+a*n^b) is smooth and monotonic with diminishing returns, but cannot reproduce a flat-zero then step pattern. Best fit leaves 12.39pp error at n15 and underfits n10 by 11.59pp. R² 0.8797 below 0.90 confirms poor shape match.

3. **Diagnostic remains descriptive-only**: proportion(margin>0) equals ranking agreement exactly (0.00pp) under template invariance, but this is a tautology of the template-invariant data structure, not a predictive model. It cannot be extrapolated without modeling how margin distribution changes with n.

4. **Null baseline dominance**: Both corrected models fail to beat random noise (50%) at n20. ModelB's 7.41pp error exceeds null's 6.62pp. This underscores that neither decomposition adds predictive value beyond chance for the small effect size (56% vs 50%).

5. **Extrapolation would predict crossing if taken at face value**: ModelB's gated extrapolation to 98.2% at n50 suggests, if the saturating form were valid, the plateau would break and recipe density would become viable at full DOM. But this extrapolation is invalid precisely because the fit is poor and the form is misspecified.

## Product Consequence

**No validated extrapolation exists.** Per frozen rule, NOT C1 → MEASUREMENT_INVALID. The Docker re-collection question remains open; recipe density viability at full DOM cannot be decided from modeling.

- Non-recipe density remains the only known 100% ranking-preservation method.
- Per-task recipe (78.65% at n20) remains tantalizingly close but unvalidated at full DOM.
- The investment decision to run full-DOM re-collection via Docker image `am1n3e/webarena-verified-shopping:latest` (EXP-INTEL-35462974425) is NOT resolved by this experiment; if anything, the failure of both analytic extrapolations strengthens the case that direct measurement is the only remaining path.

## Validity Threats

1. **4-point training set with step discontinuity**: n=5,10 have exactly zero positive margins due to small-n regime; power-law fitting is ill-conditioned near zero. The saturating form assumes gradual increase, but data has abrupt jump. Alternative 3-parameter forms (e.g., with offset/threshold) were outside frozen spec.

2. **Template invariance may not hold at full DOM**: All n=5-20 data uses truncated-first-20 locatable elements. If template invariance breaks at n>20, margin distributions could change discontinuously, invalidating any extrapolation from n≤20.

3. **Median|M|/std coupling**: Both numerator and denominator grow with n (b≈0.88 for |margin|, d≈1.64 for std), but ratio behavior is non-monotonic (SNR 0.67→1.02→0.69 across n10→15→20), suggesting Phi(median/std) has no stable scaling law.

4. **Single Magento site, 7 tasks, truncated-first-20 sampling**: Generalization to other sites, definitions, or full-DOM element pools untested.

5. **Degrees of freedom**: 2-parameter model on 4 points leaves only 2 df; R² threshold 0.90 is stringent for step data. Bootstrap PI90 narrow due to per-iteration resampling stability, not model validity.

6. **PYTHONHASHSEED=0**: Reproduced observed exactly; not a threat to verdict (margins 10-35pp over threshold).

## Reproduction

```bash
python3 research/intel/exp_35538868377_analysis.py
# inputs: snr_per_iteration_tag_entropy.json.gz (ce3dda6e...), analysis_output_snr.json (f7f69867...)
# outputs: derived_analysis.json, result.json
# No browser/network/model calls, <30s, <1000 tokens
```

Hashes: snr_per_iteration ce3dda6e021137ef0c911c19d8897c24f26342e8bd6da77242e1a026e08c1b7a, analysis_output f7f6986753774125966be2654a30744de386e2ab93790b02ec84d035ff1358b2, exp347_raw da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050.

