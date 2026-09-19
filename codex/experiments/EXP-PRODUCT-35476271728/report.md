# EXP-PRODUCT-35476271728 Report

## Experiment Summary

**Question**: Does token_refresh behavioral detection (TP) survive co-occurring structural noise at n=480, with TOST equivalence at delta=0.15 and threshold sensitivity analysis to diagnose the n=240 TOST lower-tail failure?

**Outcome**: SURVIVES — all five frozen decision conditions (C1–C5) pass. Token_refresh detection is robust to co-occurring structural noise under stochastic drift on the localhost mock ceiling. The n=240 TOST lower-tail failure was a sample-size power artifact resolved at n=480.

## Key Results

| Condition | Criterion | Observed | Pass |
|-----------|-----------|----------|------|
| C1: Structural discrimination | > 0.5 | 0.8333 | YES |
| C2: Token_refresh TP under noise | >= 0.85 | 1.0 (all 4 conditions, n=480) | YES |
| C3: Behavioral variance + TOST | std > 0.05 + TOST pass at delta=0.15 | std 0.133–0.141, TOST pass=true, CI [-0.126, 0.053] | YES |
| C4: Noise false positives | <= 0.15 | 0.0 | YES |
| C5: TOST orthogonality | TOST pass at n=480, delta=0.15 | Both tails pass (p_lower=0.0062, p_upper=2.05e-05) | YES |

## Detailed Findings

### TOST Resolution at n=480 (C5)

The primary question of this experiment was whether the n=240 TOST lower-tail failure (parent: p_lower=0.081, CI [-0.185, 0.067]) was a sample-size power artifact. At n=480:

- **Pearson r** = -0.0366 (p=0.423, not significant)
- **Fisher-z 95% CI** = [-0.126, 0.053] (width 0.179, narrowed from parent's 0.252)
- **TOST upper tail**: p=2.05e-05 < 0.05 → PASS
- **TOST lower tail**: p=0.0062 < 0.05 → PASS
- **CI upper bound**: 0.053 < 0.15 → within equivalence interval

Both tails pass at n=480. The lower bound moved from -0.185 (n=240, outside [-0.15, 0.15]) to -0.126 (n=480, inside). This confirms the hypothesis that the parent failure was a power artifact.

### Stochastic Token Refresh Behavioral Variance (C3)

The bimodal behavioral score distribution persists at n=480:

- **Refresh success** (~70%): status=200, new_token_issued=True → score ≈ 0.65
- **Refresh failure** (~30%): status=401, error=refresh_token_invalid → score ≈ 0.48

Behavioral std ranges from 0.133 to 0.141 across co-occurring conditions (n=120 each). All 4 conditions exceed the 0.05 variance gate. The behavioral means under noise (0.55–0.57) are slightly lower than isolated (0.52), but all samples still exceed the 0.25 detection threshold.

### Token Refresh Under Co-occurring Noise (C2)

Token_refresh TP is 1.0 on all 4 co-occurring conditions (n=120 per condition, n=480 total). Per-condition Wilson lower bounds are 0.969, providing strong evidence that TP ≥ 0.85 even under the most conservative single-condition estimate.

### Threshold Sensitivity Analysis (Exploratory)

Threshold sensitivity reveals a sharp TP cliff:

| Threshold | TP Rate | TP Count | Notes |
|-----------|---------|----------|-------|
| 0.15 | 1.0 | 540/540 | Both modes exceed 0.15 |
| 0.20 | 1.0 | 540/540 | Both modes exceed 0.20 |
| 0.25 | 1.0 | 540/540 | Primary threshold; both modes exceed 0.25 |
| 0.30 | 1.0 | 540/540 | Both modes exceed 0.30 |
| 0.35 | 1.0 | 540/540 | Both modes exceed 0.35 |
| 0.40 | 0.694 | 375/540 | Failure-mode samples (~0.48) fall below 0.40 |

FP=0.0 at all thresholds. The bimodal distribution means thresholds 0.15–0.35 all achieve TP=1.0 because both the failure-mode (~0.48) and success-mode (~0.65) scores exceed them. Only threshold 0.40 falls between the two modes and loses detection of failure-mode samples.

This confirms the parent audit V3 finding: the 0.25 threshold is not uniquely optimal — any threshold in [0.15, 0.35] achieves identical TP=1.0 under the current bimodal model. Continuous severity variation would be needed for meaningful threshold calibration.

### Positive Control (C1)

Structural discrimination is 0.8333, replicating EXP-RUNTIME-33902315583. Three unique fingerprints across four auth states because expired_token and invalid_token produce identical 401 authentication_failed surfaces.

### Null Control (C4)

FP rate is 0.0 on 240 noise-only samples. All behavioral scores are exactly 0.05 (admin-role baseline), well below the 0.25 detection threshold.

## Product Consequences

### If SURVIVES (this outcome)

Token_refresh detection is robust to noise, strengthening the C-FRESHNESS claim ceiling. With TOST passing at n=480, orthogonality is formally validated under the frozen decision rule. Token_refresh can be included in orthogonality sets, expanding parallel-channel architecture coverage.

### Remaining Unknowns

1. Whether orthogonality survives on a non-mock production-like substrate with real OAuth/OIDC middleware (inherited from parent)
2. Whether the expired_token/invalid_token fingerprint collision generalizes to production (inherited from parent)
3. Whether within-condition variance maintains on real network RTT and cache-freshness distributions (inherited from parent)
4. Whether continuous severity variation reveals threshold sensitivity beyond the bimodal model (new from this experiment)

## Claim Ceiling

This experiment validates C-FRESHNESS at n=480 with TOST equivalence at delta=0.15 on the localhost mock ceiling (Flask 3.1.3 + SQLite WAL + in-memory TTL cache 0.5s + jitter 10–100ms + HS256/RS256 JWT on 127.0.0.1:18951, seed 42, p_refresh_success=0.7). No production generalization, PRODUCT_CORE promotion, or non-mock inference is warranted from this evidence alone.
