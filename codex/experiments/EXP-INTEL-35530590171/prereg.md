# EXP-INTEL-35530590171 — Preregistration

## Experiment identity

- experiment_id: `EXP-INTEL-35530590171`
- lane: intel
- parent: `EXP-INTEL-35476271877` (handoff sha256: 94f853d160ebbabcd115e28dd1d6ad50f738afd289c8bfb2665537a1c78db36a)
- claim_ids: `C-MEAS-VALID`, `C-PRODUCT-ECON`
- created_at: 2026-09-20T18:55:20+00:00

## Background and motivation

The parent experiment (EXP-INTEL-35476271877) attempted to decompose the ranking instability mechanism for canonical recipe densities using an SNR model: agreement ~ Phi(mean(SNR_i)) where SNR_i = M_i / sqrt(SE_l_i^2 + SE_d_i^2). This model failed C1 validation by 40-50pp (residuals 0.5002 at n=15, 0.4405 at n=20) because it used the wrong noise scale: within-iteration within-type SE (~1e-5) instead of across-iteration margin variation (margin_std ~1e-4 to 6e-4, 10-50x larger).

The parent's audit (VF1) identified the root cause and recommended: "Replace frozen SNR noise term: use across-iteration margin_std (or full distribution of M_i) instead of within-iteration within-type SE (~1e-5) as noise scale."

This experiment implements that correction using the existing per-iteration margin data.

## Scientific question

Does a corrected SNR decomposition using across-iteration margin_std as the noise scale pass C1-equivalent validation, and if so, does the corrected extrapolation predict ranking agreement crosses 80% at full-DOM element counts (n=50)?

## Hypothesis

The corrected model Phi(mean(M_i) / std(M_i)) captures the actual ranking-instability mechanism because margin_std is the empirically relevant noise scale for ranking flips.

- H1: Predicted agreement at n=15 and n=20 will be within 10pp of observed (49.98% and 55.95%).
- H2: Corrected SNR at n=20 < 3.0 (margin-deficit regime).
- H3: Extrapolated agreement at n=50 < 80% (plateau is structural).

## Falsifier

- F1: Predicted agreement at n=15 or n=20 differs from observed by >10pp.
- F2: Extrapolated agreement at n=50 >= 80%.
- F3: Corrected SNR at n=20 >= 3.0.

## Data sources

All from parent EXP-INTEL-35476271877:
- `snr_per_iteration_tag_entropy.json.gz` (sha256: ce3dda6e021137ef0c911c19d8897c24f26342e8bd6da77242e1a026e08c1b7a) — per-iteration margin M_i for canonical recipe at n=5/10/15/20
- `analysis_output_snr.json` (sha256: f7f6986753774125966be2654a30744de386e2ab93790b02ec84d035ff1358b2) — pre-computed per_n margin_mean, margin_std, observed agreement
- `EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json` (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050) — raw reconstruction data

## Analysis plan

### Step 1: Load per-iteration margins

Load `snr_per_iteration_tag_entropy.json.gz`. For canonical recipe, extract per-iteration margins M_i at each effective_n (5, 10, 15, 20). Each M_i = mean(tag_entropy_listing) - mean(tag_entropy_detail) for that iteration's sampled elements.

### Step 2: Compute corrected model predictions

For each effective_n:
1. Compute mean_M = mean(M_i) across iterations
2. Compute std_M = std(M_i) across iterations (ddof=1)
3. Compute corrected_SNR = mean_M / std_M
4. Compute predicted_agreement = Phi(corrected_SNR) = 0.5 * (1 + erf(corrected_SNR / sqrt(2)))

Key values from parent analysis_output_snr.json (verification):
- n=5: margin_mean = -4.90e-05, margin_std = 4.97e-05
- n=10: margin_mean = -1.35e-04, margin_std = 1.06e-04
- n=15: margin_mean = 2.66e-05, margin_std = 1.63e-04
- n=20: margin_mean = 3.97e-04, margin_std = 6.23e-04

### Step 3: Validate against observed agreement

- Observed n=15: 0.4998 (frozen target)
- Observed n=20: 0.5595 (frozen target)
- C1 passes if |predicted - observed| <= 0.10 at both n=15 and n=20

### Step 4: Mechanism classification

At n=20:
- corrected_SNR = margin_mean / margin_std
- CV_listing = std(tag_entropy_listing) / mean(tag_entropy_listing)
- CV_detail = std(tag_entropy_detail) / mean(tag_entropy_detail)
- Classification: margin_deficit if SNR < 3; task_variance if CV > 0.1

### Step 5: Extrapolation to n=50

Fit power laws on the 4 data points (n=5,10,15,20):
- |margin(n)| = a * n^b (log-linear regression on |margin| vs n)
- margin_std(n) = c * n^d (log-linear regression on margin_std vs n)

Predict at n=50:
- margin_hat = a * 50^b (with sign from nearest observed: positive at n>=15)
- std_hat = c * 50^d
- corrected_SNR_50 = margin_hat / std_hat
- predicted_agreement_50 = Phi(corrected_SNR_50)

Compute 90% prediction interval using bootstrap on regression residuals (n_boot=2000, seed=999).

### Step 6: Null control

Random noise model: simulate 500,000 iterations of 3 listing + 3 detail densities ~ N(0,1), compute agreement = P(mean_l > mean_d). Verify agreement ~ 50% +/- 5%. Corrected model prediction error must be less than null model prediction error.

## Decision rule

Conjunctive:

1. **C1_CORRECTED_MODEL_VALID**: Predicted agreement at n=15 and n=20 within 10pp of observed. PASS if both within 10pp; FAIL if either off by >10pp.

2. **C2_MECHANISM_CORRECTED**: Corrected SNR at n=20 < 3.0 (margin-deficit) OR CV_listing or CV_detail > 0.1 (task-variance). PASS if any; FAIL if SNR >= 3.0 AND both CVs < 0.1.

3. **C3_EXTRAPOLATION_FALSIFIES_FULL_DOM**: Extrapolated agreement at n=50 < 80%. PASS if < 80%; FAIL if >= 80%.

Verdict:
- NOT C1 → MEASUREMENT_INVALID
- C1 AND NOT C2 → MIXED
- C1 AND C2 AND C3 → FALSIFIES-FULL-DOM
- C1 AND C2 AND NOT C3 → SUPPORTS-FULL-DOM

## Controls

| Control | Expected | Decision role |
|---------|----------|---------------|
| PC1: Corrected model reproduces observed | Within 10pp at n=15 and n=20 | C1 gating |
| NC1: Random noise baseline | Agreement ~50% +/- 5% at all n; model error < null error | Validates model captures structure |
| B1: Parent failed SNR n=15 | Residual 0.5002 (C1 FAIL) | Baseline: corrected model must do better |
| B2: Parent failed SNR n=20 | Residual 0.4405 (C1 FAIL) | Baseline: corrected model must do better |
| B4: Observed agreement n=15 | 0.4998 | Target for C1 |
| B5: Observed agreement n=20 | 0.5595 | Target for C1 |
| B6: Parent extrapolation n=50 | 1.0 (PI90 lo 0.845) | Baseline: corrected extrapolation is the new measurement |

## Validity threats

1. **Power-law extrapolation from n=4 points**: The margin sign crosses zero between n=10 and n=15, making power-law fitting on |margin| potentially unreliable. Mitigation: report PI width and note sign-crossing in validity_notes.

2. **Template invariance at truncated-first-20**: Same-type tasks share identical templates, making canonical densities scalar multiples. This does not affect margin_std-based SNR but means correlation structure (rho=1.0) is tautological. Mitigation: mechanism classification uses SNR and CV, not rho.

3. **Single site (Magento), small type sample (n=3 per type)**: Generalization beyond this specific setup is untested. Mitigation: claim ceiling explicitly bounded to 7 tasks truncated-first-20 single site.

4. **Cart n=1 degeneracy**: Cart page_type has n=1, excluded from margin computations. Mitigation: listing vs detail used throughout per parent protocol.

5. **PYTHONHASHSEED=0 variation**: Small quantitative differences from parent run due to set-iteration order. Mitigation: reproduced within hash-seed variation (delta < 0.01 in agreement).

## Consequences

**If C1 passes and C3 predicts <80%**: The 56% plateau is structural. Product lane adopts non-recipe density immediately. Docker re-collection (EXP-INTEL-35462974425) is NOT justified for ranking stability. This resolves the MIXED program's central ambiguity.

**If C1 passes and C3 predicts >=80%**: The plateau is an artifact of the narrow n-range. Docker re-collection IS justified. The full-DOM experiment becomes the single highest-information next step.

**If C1 fails**: margin_std is also not the right noise scale. The search for the correct decomposition continues. The 56% plateau remains unexplained and the Docker question remains OPEN.

## Expected cost

< 500 LLM tokens for analysis code, < 30 seconds compute. No browser/network/model calls. Pure offline reanalysis of existing data.
