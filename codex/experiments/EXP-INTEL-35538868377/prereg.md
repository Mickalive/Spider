# EXP-INTEL-35538868377 Preregistration

## Status: DESIGN NOT YET FROZEN

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35538868377
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID, C-PRODUCT-ECON
- **Parent Handoff**: EXP-INTEL-35530590171 (MEASUREMENT_INVALID, C1 FAIL at n=20, residual 17.8pp)

## Question

Can a sign-magnitude-separated noise decomposition (Phi(median(|M|)/std)) or a direct sign-fraction power law (proportion(margin_i>0) modeled as saturating function of n) pass C1-equivalent validation at n=15 and n=20, providing a validated extrapolation path to full-DOM n=50/82?

## Background and Rationale

The parent experiment (EXP-INTEL-35530590171) tested a corrected SNR decomposition Phi(mean(M_i)/std(M_i)) that replaced within-iteration SE with across-iteration margin_std as the noise scale. This improved residuals by 7.7x at n=15 (50.0pp → 6.5pp) and 2.5x at n=20 (44.1pp → 17.8pp), but failed C1 at n=20 (17.8pp > 10pp threshold).

Root cause analysis revealed that Phi(mean/std) conflates two independent sources:
1. **Sign** of the margin (determines which element ranks higher)
2. **Magnitude** of the margin (determines how much noise affects ranking)

At n=20, std grows faster (exponent 1.64) than |mean| (exponent 0.88), inflating the SNR and over-predicting agreement. The diagnostic statistic proportion(margin_i>0) achieved near-exact prediction (residuals 0.02pp and 0.59pp), confirming that **sign fraction, not mean/std ratio, determines agreement under template invariance**.

This suggests two orthogonal correction paths:

**Model A (Median-based)**: Replace mean with median(|M_i|) to separate sign from magnitude. The median of absolute margins is sign-invariant and captures the typical magnitude; std captures total variation. This directly addresses the conflation problem.

**Model B (Sign-fraction power law)**: Abandon the Phi function entirely. Model proportion(margin_i>0) directly as a saturating function of n: f(n) = a * n^b / (1 + a * n^b). The diagnostic already shows this proportion matches observed agreement within 1pp; the question is whether this proportion extrapolates reliably.

## Hypotheses

**H1 (Model A)**: Phi(median(|M_i|)/std(M_i)) predicts observed ranking agreement at n=15 and n=20 within 10 percentage points.

**H2 (Model B)**: The sign-fraction saturating power law fitted on n=5/10/15/20 predicts proportion(margin>0) at n=15 and n=20 within 2pp, and achieves R² ≥ 0.90 on the training data.

**H3 (Extrapolation)**: The validated model(s) extrapolate agreement at n=50 below 80%, confirming the plateau is structural.

## Falsification Criteria

**F1**: Model A predicted agreement at n=15 or n=20 differs from observed by >10pp.

**F2**: Model B fitted proportion(margin>0) at n=15 or n=20 has residual >2pp, OR R² < 0.90 on the 4-point training data.

**F3**: Both models pass C1 but sign-fraction extrapolation to n=50 predicts proportion(margin>0) > 0.80.

**F4**: Model B saturating power law fit has R² < 0.90 on n=5/10/15/20 data.

## Data Sources

- `research/experiments/EXP-INTEL-35476271877/snr_per_iteration_tag_entropy.json.gz` (sha256: ce3dda6e021137ef0c911c19d8897c24f26342e8bd6da77242e1a026e08c1b7a) — per-iteration margin data
- `research/experiments/EXP-INTEL-35476271877/analysis_output_snr.json` (sha256: f7f6986753774125966be2654a30744de386e2ab93790b02ec84d035ff1358b2) — per-n margin_std, margin_mean, baseline values
- `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json` (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050) — truncated-first-20 raw density data

## Analysis Protocol

### Model A: Median-based decomposition

For each n ∈ {5, 10, 15, 20}:
1. Extract per-iteration margins M_i from snr_per_iteration_tag_entropy.json.gz (canonical recipe, tag_entropy × DEF-FULL-MAP)
2. Compute median_abs_margin = median(|M_i|)
3. Compute margin_std = std(M_i) (across-iteration, same as parent)
4. Compute SNR_A = median_abs_margin / margin_std
5. Compute predicted_agreement = Phi(SNR_A) = 0.5 * (1 + erf(SNR_A / sqrt(2)))
6. Compare against observed ranking agreement at each n

### Model B: Sign-fraction saturating power law

1. For each n ∈ {5, 10, 15, 20}, compute proportion(margin_i > 0) from per-iteration margins
2. Fit saturating power law: proportion(n) = a * n^b / (1 + a * n^b) using scipy.optimize.curve_fit
3. Compute R² on the 4-point training data
4. Validate fitted proportions at n=15 and n=20 against observed (within 2pp)
5. Extrapolate to n=50 and n=82
6. Report predicted proportion(margin>0) with 90% prediction interval via bootstrap (B=2000, seed=999)

### Comparison

- Model A C1: predicted agreement within 10pp of observed at BOTH n=15 and n=20
- Model B C1: fitted proportion within 2pp of observed at BOTH n=15 and n=20 (stricter because Model B has the advantage of the near-exact diagnostic)
- Model B C2: R² ≥ 0.90 on 4-point training data
- Model B C3: extrapolated proportion at n=50 < 0.80

## Decision Rule

Conjunctive:

**C1_EITHER_MODEL_VALID**: At least one of Model A or Model B passes its respective C1 criterion. PASS if either model passes at BOTH n=15 and n=20; FAIL if both models fail.

**C2_SIGN_FRACTION_FIT_QUALITY**: Model B achieves R² ≥ 0.90 on 4-point training data. PASS if R² ≥ 0.90; FAIL if R² < 0.90.

**C3_SIGN_FRACTION_EXTRAPOLATION_BELOW_80**: Model B extrapolation predicts proportion(margin>0) at n=50 < 0.80. PASS if < 0.80; FAIL if ≥ 0.80.

**Verdict**:
- NOT C1 → MEASUREMENT_INVALID
- C1 AND NOT C2 → MIXED
- C1 AND C2 AND C3 → SIGN_FRACTION_VALIDATED
- C1 AND C2 AND NOT C3 → SIGN_FRACTION_PREDICTS_CROSSING

## Controls

### Positive Control: PC1_SIGN_FRACTION_REPRODUCES_OBSERVED
The diagnostic proportion(margin_i>0) reproduces observed ranking agreement at n=15 and n=20 within 1pp, confirming the parent's near-exact diagnostic finding. Expected: proportion at n=15 within 1pp of 49.96%; at n=20 within 1pp of 56.54%.

### Null Control: NC1_RANDOM_NOISE_BASELINE
Random noise model (densities ~ N(0,1)) predicts agreement ~50% at all n. Best validated model must outperform this null at n=20 (error < 0.060).

### Baselines
- B1/B2: Parent frozen SNR model (residuals 0.5002/0.4405)
- B3: Previous corrected Phi(mean/std) model (residual 17.8pp at n=20)
- B4: Diagnostic indicator (residuals 0.02pp/0.59pp)
- B5: Null noise baseline (0.499208)
- B6: Parent extrapolation (1.0 at n=50, gated)

## Validity Threats

1. **Template invariance**: Under template invariance, ranking agreement = proportion(margin>0) exactly. Model B's near-exact fit is expected, not a surprise. The critical test is extrapolation, not in-sample fit.
2. **Small training set**: 4 points (n=5/10/15/20) with sign crossing in |margin| between n=10 and n=15. Power law fit may be unstable.
3. **Single Magento site, 7 tasks**: Results may not generalize to other sites or task types.
4. **Truncated-first-20 sampling**: Full DOM may have different margin structure.
5. **PYTHONHASHSEED=0**: Set-iteration order may affect role-subset composition; delta ~0.006 at n=20 (from parent).
6. **Cart n=1 degeneracy**: Excluded from margin computations per parent protocol.

## Product Consequences

- If C1 AND C3 (validated, predicts <80%): Product lane adopts non-recipe density; Docker re-collection NOT justified.
- If C1 AND NOT C3 (predicts ≥80%): Docker re-collection justified; recipe density remains viable.
- If NOT C1: No model-based extrapolation justified; Docker re-collection is the only path to answer the full-DOM question.

## Estimated Cost

VERY LOW — offline computation on existing data. <1000 LLM tokens for analysis code, <30 seconds compute. No browser/network/model calls.

## Expected Information Gain

HIGH — directly resolves the critical ambiguity from the parent's MEASUREMENT_INVALID result. Either positive (validated extrapolation path) or negative (both decompositions fail) outcome changes a concrete product decision about Docker re-collection investment and recipe density viability.
