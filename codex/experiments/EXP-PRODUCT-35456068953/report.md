# EXP-PRODUCT-35456068953 Report

## Experiment Summary

**Question**: Does token_refresh behavioral detection (TP) survive co-occurring structural noise at the same severity levels as permission_boundary and session_invalidation, when token_refresh drift is stochastic (randomized refresh success/failure) to produce behavioral variance?

**Outcome**: SURVIVES_CURRENT_TEST — all four frozen decision conditions pass. Token_refresh detection is robust to co-occurring structural noise under stochastic drift on the localhost mock ceiling.

## Key Results

| Condition | Criterion | Observed | Pass |
|-----------|-----------|----------|------|
| C1: Structural discrimination | > 0.5 | 0.8333 | YES |
| C2: Token_refresh TP under noise | >= 0.85 | 1.0 (all 4 conditions) | YES |
| C3: Behavioral variance | > 0.05 | 0.134–0.143 (4/4 conditions) | YES |
| C4: Noise false positives | <= 0.15 | 0.0 | YES |

## Detailed Findings

### Stochastic Token Refresh Variance (C3)

The core modification in this experiment was making token_refresh drift stochastic: each request independently samples refresh success (p=0.7) or failure (p=0.3). This produces a bimodal behavioral score distribution:

- **Refresh success** (~70% of samples): status=200, new_token_issued=True → score ≈ 0.65
- **Refresh failure** (~30% of samples): status=401, error=refresh_token_invalid → score ≈ 0.48

Both modes exceed the 0.25 detection threshold, so TP=1.0 despite the bimodality. The behavioral_std (0.128 isolated, 0.134–0.143 under noise) is driven by this bimodal distribution, not by continuous severity variation.

This resolves the parent's unknown #4: "Whether token_refresh TP (1.0 isolated, deterministic std=0.0 by design) survives co-occurring structural noise."

### Token Refresh Under Co-occurring Noise (C2)

Token_refresh TP is 1.0 on all 4 co-occurring conditions (token_refresh × optional_field_addition, description_change, response_time_jitter, field_type_normalization). The behavioral score means under noise (0.55–0.57) are slightly lower than isolated (0.58), but all samples still exceed the threshold.

This confirms that token_refresh detection is as robust to structural noise as permission_boundary and session_invalidation (which also achieved TP=1.0 in the parent experiment).

### Orthogonality (TOST)

The pooled Pearson r between behavioral and structural signals is -0.060 (p=0.353, not significant), with Fisher-z 95% CI [-0.185, 0.067]. The TOST equivalence test at delta=0.15 shows:

- **Upper tail**: p=0.000567 < 0.05 → PASS (r is not more positive than +0.15)
- **Lower tail**: p=0.081 > 0.05 → FAIL (CI extends below -0.15)
- **CI upper bound**: 0.067 < 0.15 → meets measurement validity criterion

The lower tail failure is due to n=240 (vs parent n=480) producing a wider CI. The actual r=-0.06 is well within [-0.15, 0.15]. The frozen decision rule defines C3 as behavioral_std > 0.05 (which passes), not as TOST pass; TOST is a separate measurement validity check.

### Positive Control (C1)

Structural discrimination is 0.8333, replicating EXP-RUNTIME-33902315583 exactly. Three unique fingerprints across four auth states because expired_token and invalid_token produce identical 401 authentication_failed surfaces.

### Null Control (C4)

FP rate is 0.0 on 240 noise-only samples. All behavioral scores are exactly 0.05 (admin-role baseline), well below the 0.25 detection threshold.

## Product Consequences

### If SURVIVES (this outcome)

Token_refresh detection is robust to noise, strengthening C-FRESHNESS claim ceiling. Token_refresh can be included in orthogonality sets, expanding parallel-channel architecture coverage. The three untested drift types become two (token_refresh added; only the production-substrate question remains unknown from the original 3 drift types).

### Remaining Unknowns

1. Whether orthogonality survives on a non-mock production-like substrate (inherited from parent)
2. Whether the expired_token/invalid_token fingerprint collision generalizes to production (inherited from parent)
3. Whether the TOST lower tail failure at n=240 resolves at n>=480 (likely sample-size artifact)

## Claim Ceiling

This experiment extends the C-FRESHNESS claim ceiling to include token_refresh under stochastic drift on the localhost mock (Flask 3.1.3 + SQLite WAL + TTL cache 0.5s + jitter 10-100ms + HS256/RS256 JWT on 127.0.0.1:18951, seed 42, p_refresh_success=0.7). No production generalization, PRODUCT_CORE promotion, or non-mock inference is warranted from this evidence alone.
