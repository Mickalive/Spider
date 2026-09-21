# EXP-PRODUCT-35572180893 — Preregistration

## Status

DESIGN ONLY. Not yet frozen.

## Experiment Identity

- **Experiment ID**: EXP-PRODUCT-35572180893
- **Lane**: product
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Parent**: EXP-PRODUCT-35551517868 (overlap-controlled FP-TP tradeoff, MIXED outcome)

## Question

Can the freshness guard discriminating operating point be measured under genuine distributional overlap (25%/50%/75% area) using Gaussian noise/refresh distributions on localhost mock — and does the calibrated threshold increase gradually (not just at 100% overlap) when the overlap is real rather than an artifact of uniform-shift boundary behavior?

## Hypothesis

When noise and failure behavioral-score distributions genuinely overlap (Gaussian, not uniform-shift), the calibrated threshold will increase gradually across overlap conditions (not just a single jump at 100%), and FP > 0 at threshold 0.20 will emerge at moderate (25%-50%) overlap — demonstrating a discriminating operating point under genuine distributional contamination.

## Falsifier

If the calibrated threshold remains at 0.20 even under genuine 25%-75% Gaussian overlap (FP constraint never binding), OR if FP > 0 at threshold 0.20 only emerges at 75%+ overlap despite genuine overlap at 25%-50%, OR if orthogonality (TOST delta=0.15) breaks under any overlap condition — then the discriminating operating point hypothesis is falsified under genuine overlap.

## Prior Evidence (from parent handoff)

The parent experiment (EXP-PRODUCT-35551517868) tested 5 overlap conditions (0%,25%,50%,75%,100%) using uniform-shift overlap design. Key findings:

- Calibrated threshold: 0.20 at 0%-75%, 0.25 at 100% — non-monotonic flat-then-jump
- FP at threshold 0.20: 0.0 at 0%/25%/50%, 0.0958 at 75%, 0.35 at 100%
- Orthogonality: TOST PASS at 0%/25%/50%/100%, marginal failure at 75% (CI upper 0.1549 > 0.15)

**Critical flaw identified**: The uniform-shift design (shift=overlap_pct/100*0.09) produces 0% actual distributional overlap at the 25% and 50% conditions. At 25% overlap, noise max = 0.20 = failure min — boundary contact only, not实质性 overlap. FP=0 at those conditions is an artifact of insufficient shift, not evidence against discrimination. The coarse threshold grid [0.20,0.25,...0.80] cannot locate the true optimum between 0.20 and 0.25.

## Design

### Overlap Model

Use Gaussian distributions instead of uniform-shift:

- **Failure distribution**: N(μ=0.295, σ=0.05) — behavioral scores for token_refresh failure samples
- **Noise distribution**: N(μ_noise, σ=0.05) — behavioral scores for noise-only samples
- **FAILURE_THRESHOLD**: 0.20 (calibrated threshold from 7+ prior experiments)
- **Overlap definition**: P(noise_score > FAILURE_THRESHOLD) — fraction of noise samples in the failure zone; verified empirically

### Overlap Conditions

| Condition | μ_noise | Target overlap | Empirical verification |
|-----------|---------|----------------|----------------------|
| 0% | 0.095 | P(N(0.095,0.05) > 0.20) ≈ 0% | Count noise > 0.20 |
| 25% | 0.1663 | P(N(0.1663,0.05) > 0.20) ≈ 25% | Count noise > 0.20 |
| 50% | 0.195 | P(N(0.195,0.05) > 0.20) ≈ 50% | Count noise > 0.20 |
| 75% | 0.2237 | P(N(0.2237,0.05) > 0.20) ≈ 75% | Count noise > 0.20 |
| 100% | 0.295 | P(N(0.295,0.05) > 0.20) ≈ 100% | Count noise > 0.20 |

Noise means computed via inverse CDF: μ_noise = FAILURE_THRESHOLD + σ * Φ⁻¹(1 - target_overlap).

### Sample Size

- **480 samples per overlap condition** (240 token_refresh + 240 noise-only)
- **Total**: 5 conditions × 480 = 2400 calibration samples
- **480 paired co-occurring samples per condition** (4 drift×noise pairs × 120 each)
- **40 discrimination probes** (4 auth states × 10 each)
- **Total samples**: ~4400 across all phases

### Threshold Grid

50 points: [0.05, 0.06, 0.07, ..., 0.54] (0.01 increments).

This resolves the true optimum between 0.20 and 0.25 that the parent's coarse grid [0.20,0.25,...0.80] could not locate.

### Phases

1. **Phase C — Discrimination**: 40 probes across 4 auth states (no_auth, valid_token, expired_token, invalid_token). Measures C1 structural discrimination. Same as parent.

2. **Phase A — Calibration**: For each overlap condition:
   - Set overlap via POST /api/overlap
   - Collect 240 token_refresh samples (drift=token_refresh, valid token)
   - Collect 240 noise-only samples (4 noise types × 60 each)
   - Measure behavioral_score from /api/session/status, structural_signal from /api/schema

3. **Phase B — Co-occurring**: For each overlap condition:
   - 4 drift×noise pairs × 120 samples = 480 paired samples
   - Same as parent

4. **ROC Analysis**: For each overlap condition:
   - Sweep 50 thresholds on token vs noise calibration scores
   - Compute TPR, FPR, precision, F1, Wilson lower bound at each threshold
   - Find calibrated threshold (highest F1 meeting TPR≥0.85, FPR≤0.10)
   - Compute full AUC

### Metrics (stable identifiers for downstream)

- `overlap_genuine_pct_by_condition` — empirical P(noise > 0.20) at each overlap condition
- `calibrated_threshold_by_overlap` — threshold selected by ROC at each condition
- `fp_at_020_by_overlap` — FPR at baseline threshold 0.20 at each condition
- `tp_at_020_by_overlap` — TPR at baseline threshold 0.20 at each condition
- `threshold_increases_monotonically` — bool: does threshold increase across 0→25→50→75→100?
- `fp_binding_below_75` — bool: is FP > 0 at threshold 0.20 for any condition in {25%, 50%}?
- `orthogonality_by_overlap` — TOST result (r, CI upper, pass) at each condition
- `c1_discrimination` — structural discrimination (same as parent, measured once)
- `roc_auc_by_overlap` — area under ROC curve at each condition
- `unique_behavioral_scores` — count of unique scores (continuous injection check)

### Controls

| Control | Condition | Expected | Metric |
|---------|-----------|----------|--------|
| NC-NULL-OVERLAP-0 | 0% overlap | FP=0.0 at threshold 0.20 | fp_at_020_by_overlap[0] |
| PC-FP-BINDING-100 | 100% overlap | FP > 0.20 at threshold 0.20 | fp_at_020_by_overlap[100] |
| PC-FP-BINDING-25 | 25% overlap | FP > 0 at threshold 0.20 | fp_at_020_by_overlap[25] |
| PC-FP-BINDING-50 | 50% overlap | FP > 0 at threshold 0.20 | fp_at_020_by_overlap[50] |
| C1-STRUCTURAL-DISCRIMINATION | all conditions | discrimination > 0.5 | c1_discrimination |
| C3-ORTHOGONALITY | all conditions | TOST PASS, CI upper < 0.15 | orthogonality_by_overlap |
| CONTINUOUS-INJECTION | all conditions | unique scores ≥ 5 | unique_behavioral_scores |

### Decision Rule

1. If not continuous_injection_ok → MEASUREMENT_INVALID
2. If error_format_inert (structural_std ≤ 0.15) → MEASUREMENT_INVALID
3. If n_cooccur < 480 at any condition → MEASUREMENT_INVALID
4. If calibrated_threshold is None at any condition → FALSIFIED
5. If not c1_pass → FALSIFIED
6. If not c5_pass (orthogonality fails at any condition) → FALSIFIED
7. If threshold_increases_monotonically AND fp_binding_below_75 → SUPPORTS
8. If NOT threshold_increases_monotonically AND NOT fp_binding_below_75 → FALSIFIED
9. Otherwise → MIXED

## Key Improvements Over Parent

1. **Genuine overlap**: Gaussian distributions with controlled P(noise > threshold) instead of uniform-shift boundary behavior. At 25% overlap, ~25% of noise samples genuinely exceed 0.20 (vs parent's 0%).

2. **Finer threshold resolution**: 50-point grid (0.01 increments) vs parent's 8-point grid (0.05 increments). Resolves the true optimum between 0.20 and 0.25.

3. **Empirical overlap verification**: Count actual noise samples > 0.20 to verify the target overlap, rather than assuming it from distribution parameters.

4. **Same sample size**: 480 per condition for direct TOST comparability with 6+ prior experiments.

## Validity Threats

1. **Clamping artifact**: Gaussian samples may fall outside [0,1]; clamping to [0,1] slightly reduces overlap at extreme conditions. Mitigated by verifying empirical overlap from clamped samples.

2. **Gaussian vs production noise**: Production noise may not be Gaussian. The Gaussian design tests the principle of genuine overlap, not production fidelity.

3. **75% overlap power**: Parent flagged marginal orthogonality failure at 75% (CI upper 0.1549 vs delta 0.15). With 480 samples, this condition has reduced power to detect small correlations. A future n≥800 re-run may be needed.

4. **σ choice**: Both distributions use σ=0.05. Different σ values would change the overlap geometry. This is a design choice, not a universal parameter.

## Product Consequence

- **If SUPPORTS**: Freshness guard discriminates under genuine moderate overlap → calibrated production threshold selection enabled → C-FRESHNESS moves toward PRODUCT_CORE
- **If FALSIFIED**: Freshness guard cannot separate noise from failure under genuine overlap → production threshold must trade off false accepts vs missed failures → C-FRESHNESS remains EXPERIMENTAL, production deployment blocked
- **If MIXED**: Partial discrimination exists → threshold calibration may be possible but with bounded operating range
