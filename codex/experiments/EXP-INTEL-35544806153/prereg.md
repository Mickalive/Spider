# EXP-INTEL-35544806153 Preregistration

## Status: DESIGN NOT YET FROZEN

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35544806153
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID, C-PRODUCT-ECON
- **Parent Handoff**: EXP-INTEL-35538868377 (MEASUREMENT_INVALID, C1 FAIL, both decompositions REJECTED)

## Question

Can a non-parametric empirical CDF mapping of the margin distribution predict ranking agreement at n=15 and n=20 within 10pp, providing a validated extrapolation path to full-DOM n=50/82 — or should the Intel lane pivot to prioritize Docker-based direct full-DOM measurement to bypass modeling entirely?

## Background and Rationale

The parent experiment (EXP-INTEL-35538868377) tested two corrected decompositions:
1. **ModelA**: Phi(median(|M|)/std) — REJECTED at C1 (34.59pp at n15, 18.96pp at n20)
2. **ModelB**: Saturating sign-fraction power law — REJECTED at C1 (12.39pp at n15, R2=0.8797)

This follows three consecutive MEASUREMENT_INVALID results in the SNR model chain:
- EXP-INTEL-35476271877: Phi(mean(SNR_i)) with within-iteration SE — REJECTED (40-50pp at C1)
- EXP-INTEL-35530590171: Phi(mean/std) with margin_std — REJECTED (17.8pp at n20)
- EXP-INTEL-35538868377: Phi(median/std) and sign-fraction power law — REJECTED

The step-function structure of proportion(margin>0) — (0, 0, 0.50, 0.57) at n=5/10/15/20 — suggests a threshold/phase-transition mechanism rather than smooth parametric form. All three parametric families (Phi function, power law, saturating form) have failed to capture this structure.

**Key insight**: The diagnostic proportion(margin>0) already matches observed agreement within 0.02pp and 0.59pp at n=15 and n=20. Under template invariance, this is the true data-generating process. The question is whether this proportion can be extrapolated reliably.

**Non-parametric approach**: An empirical CDF mapping F_empirical: n -> proportion(margin>0) uses the observed data directly without functional form assumptions, capturing the step-function structure that parametric models miss.

## Hypotheses

**H1 (Reproduction)**: The empirical CDF mapping reproduces observed ranking agreement at training points n=15 and n=20 within 1pp (trivially true by construction).

**H2 (Structure)**: The step-function structure (0, 0, 0.50, 0.57) is monotonic from n=10 to n=20, indicating a threshold/phase-transition rather than non-monotonic behavior.

**H3 (Extrapolation)**: Linear extrapolation from n=15 and n=20 predicts agreement at n=50 below 80%, confirming the plateau is structural.

## Falsification Criteria

**F1**: The empirical CDF mapping fails to reproduce observed agreement at training points n=15 and n=20 within 1pp (indicating data corruption or computation error).

**F2**: The step-function structure is non-monotonic (proportion(20) < proportion(15) or proportion(15) < proportion(10)), indicating the margin distribution has non-monotonic behavior that invalidates interpolation.

**F3**: The extrapolated proportion at n=50 exceeds 0.80, indicating the plateau breaks at full DOM.

**F4**: Linear interpolation between n=10 and n=15 produces a slope that implies agreement crosses 80% before n=50.

## Data Sources

- `research/experiments/EXP-INTEL-35476271877/snr_per_iteration_tag_entropy.json.gz` (sha256: ce3dda6e021137ef0c911c19d8897c24f26342e8bd6da77242e1a026e08c1b7a) — per-iteration margin data
- `research/experiments/EXP-INTEL-35476271877/analysis_output_snr.json` (sha256: f7f6986753774125966be2654a30744de386e2ab93790b02ec84d035ff1358b2) — per-n margin_std, margin_mean, baseline values
- `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json` (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050) — truncated-first-20 raw density data

## Analysis Protocol

### Step 1: Compute Empirical CDF

For each n ∈ {5, 10, 15, 20}:
1. Extract per-iteration margins M_i from snr_per_iteration_tag_entropy.json.gz (canonical recipe, tag_entropy × DEF-FULL-MAP)
2. Compute proportion(margin_i > 0) at each n
3. Store as empirical CDF: F(n) = proportion(margin_i > 0)

### Step 2: Validate at Training Points

Compare empirical CDF values against observed ranking agreement:
- F(5) should be within 1pp of 0.0
- F(10) should be within 1pp of 0.0
- F(15) should be within 1pp of 0.4996
- F(20) should be within 1pp of 0.5654

### Step 3: Check Monotonicity

Verify: F(20) > F(15) > F(10) > F(5). If non-monotonic, the interpolation approach is invalid.

### Step 4: Linear Extrapolation

Using the slope between n=15 and n=20:
- slope = (F(20) - F(15)) / (20 - 15)
- F_extrapolated(50) = F(20) + slope * (50 - 20)
- F_extrapolated(82) = F(20) + slope * (82 - 20)

### Step 5: Compare Against Linear Null

Linear extrapolation from n=20 alone (assuming F(20) = 0.5654 and slope = 0):
- F_null(50) = 0.5654
- F_null(82) = 0.5654

If |F_extrapolated(50) - F_null(50)| < 5pp, the non-parametric approach adds no information beyond simple constant trend.

### Step 6: Step-Function Analysis

Analyze the step-function structure:
- Proportion of total increase occurring between n=10 and n=15 (the "jump")
- Proportion of total increase occurring between n=15 and n=20 (the "plateau")
- Ratio of jump to plateau rates

## Decision Rule

Conjointive:

**C1_EMPIRICAL_CDF_REPRODUCES_TRAINING**: The empirical CDF mapping reproduces observed ranking agreement at n=15 and n=20 within 1pp. PASS if residuals <1pp at both points; FAIL otherwise.

**C2_STEP_FUNCTION_STRUCTURE**: The step-function structure (0, 0, 0.50, 0.57) is monotonic from n=10 to n=20. PASS if proportion(20) > proportion(15) > proportion(10) > proportion(5); FAIL if non-monotonic.

**C3_EXTRAPOLATION_BELOW_80**: The empirical CDF extrapolation to n=50 predicts agreement < 0.80. PASS if predicted proportion at n=50 < 0.80; FAIL if >= 0.80.

**Verdict**:
- NOT C1 → MEASUREMENT_INVALID
- C1 AND NOT C2 → MEASUREMENT_INVALID
- C1 AND C2 AND C3 → EMPIRICAL_CDF_VALIDATED
- C1 AND C2 AND NOT C3 → EMPIRICAL_CDF_PREDICTS_CROSSING

## Controls

### Positive Control: PC1_EMPIRICAL_CDF_REPRODUCES_TRAINING
The empirical CDF mapping reproduces observed ranking agreement at all training points (n=5, 10, 15, 20) within 1pp. This is trivially true by construction but serves as a data integrity check.

### Null Control: NC1_LINEAR_INTERPOLATION_NULL
Linear extrapolation from n=20 alone (constant trend) provides a null model. If the empirical CDF extrapolation is indistinguishable from this null (<5pp difference), the non-parametric approach adds no information.

### Baselines
- B1: Parent ModelA residual 34.59pp at n15 (REJECTED)
- B2: Parent ModelB residual 12.39pp at n15 (REJECTED)
- B3: Corrected Phi(mean/std) residual 17.8pp at n20 (REJECTED)
- B4: Diagnostic indicator residuals 0.00pp/0.00pp (near-exact)
- B5: Null noise baseline 0.499208

## Validity Threats

1. **Template invariance**: Under template invariance, ranking agreement = proportion(margin>0) exactly. The empirical CDF mapping is the true data-generating process at training points. The critical test is extrapolation.
2. **Small training set**: 4 points (n=5/10/15/20) with step-function structure. Linear extrapolation may be unreliable.
3. **Single Magento site, 7 tasks**: Results may not generalize to other sites or task types.
4. **Truncated-first-20 sampling**: Full DOM may have different margin structure.
5. **PYTHONHASHSEED=0**: Set-iteration order may affect role-subset composition; delta ~0.006 at n=20 (from parent).
6. **Cart n=1 degeneracy**: Excluded from margin computations per parent protocol.
7. **Linear extrapolation assumption**: The step-function structure may not be linear between n=20 and n=50. Piecewise linear interpolation assumes the trend continues, which may not hold.

## Product Consequences

- If C1 AND C2 AND C3 (empirical CDF validated, predicts <80%): Product lane adopts non-recipe density; Docker re-collection NOT justified.
- If C1 AND C2 AND NOT C3 (predicts >=80%): Docker re-collection justified; recipe density remains viable.
- If NOT C1 OR NOT C2: No non-parametric extrapolation justified; Docker re-collection is the only path to answer the full-DOM question. Intel lane should pivot to Docker-based direct measurement.

## Estimated Cost

VERY LOW — offline computation on existing data. <500 LLM tokens for analysis code, <10 seconds compute. No browser/network/model calls.

## Expected Information Gain

HIGH — directly tests whether the non-parametric empirical CDF approach can succeed where three parametric decompositions failed. The step-function structure (0, 0, 0.50, 0.57) suggests threshold behavior that parametric models cannot capture. Either positive (validated non-parametric extrapolation) or negative (step-function structure invalidates interpolation) outcome changes a concrete product decision about Docker re-collection investment and recipe density viability. If both parametric and non-parametric modeling fail, the Intel lane should pivot to Docker-based direct measurement as the only remaining path to an empirical answer.
