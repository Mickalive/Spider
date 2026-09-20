# EXP-PRODUCT-35481773764 Report

## Experiment Summary

**Question**: Does token_refresh behavioral drift detection remain robust (TP >= 0.85, behavioral_std > 0.05) when co-occurring structural noise includes production-like complexity patterns (pagination metadata, variable-length response bodies, error format variation, CDN cache headers) rather than only the 4 simplistic field-level noise types tested in the parent?

**Outcome**: SUPPORTS — all five frozen decision conditions (C1–C5) pass. Token_refresh detection is robust to production-like structural complexity under stochastic drift on the localhost mock ceiling. Orthogonality confirmed at delta=0.15 at n=480.

## Key Results

| Condition | Criterion | Observed | Pass |
|-----------|-----------|----------|------|
| C1: Structural discrimination | > 0.5 | 0.8333 | YES |
| C2: Token_refresh TP under noise | >= 0.85 | 1.0 (all 4 conditions, n=480) | YES |
| C3: Behavioral variance + TOST | std > 0.05 + TOST pass at delta=0.15 | std 0.1345–0.1465, TOST pass=true, CI [-0.0735, 0.1055] | YES |
| C4: Noise false positives | <= 0.15 | 0.0 | YES |
| C5: TOST orthogonality | TOST pass at n=480, delta=0.15 | Both tails pass (p_lower=0.00013, p_upper=0.0016) | YES |

## Detailed Findings

### Production-like Structural Noise Robustness (C2)

Token_refresh TP is 1.0 on all 4 co-occurring conditions (n=120 per condition, n=480 total). Per-condition Wilson lower bounds are 0.969, providing strong evidence that TP ≥ 0.85 even under the most conservative single-condition estimate.

The production-like noise types increase structural variance beyond parent simplistic types:
- **pagination_metadata**: structural_std = 0.898 (body key count varies 2-6 per request)
- **variable_length_data**: structural_std = 0.4017 (data_list length varies 0-8 items)
- **error_format_variation**: structural_std = 0.4017 (error body format varies by status code)
- **cdn_cache_headers**: structural_std = 0.4078 (3-4 CDN-specific headers added)

Despite this increased structural complexity, the behavioral signal remains independent (orthogonality confirmed).

### Orthogonality at n=480 (C5)

- **Pearson r** = 0.0161 (p=0.725, not significant)
- **Fisher-z 95% CI** = [-0.0735, 0.1055] (width 0.179)
- **TOST upper tail**: p=0.0016 < 0.05 → PASS
- **TOST lower tail**: p=0.00013 < 0.05 → PASS
- **CI upper bound**: 0.1055 < 0.15 → within equivalence interval

Both tails pass at n=480. The behavioral-structural correlation is negligible (r=0.016), confirming that production-like structural noise does not introduce coupling with the behavioral signal.

### Stochastic Token Refresh Behavioral Variance (C3)

The bimodal behavioral score distribution persists under production-like noise:
- **Refresh success** (~70%): status=200, new_token_issued=True → score ≈ 0.65
- **Refresh failure** (~30%): status=401, error=refresh_token_invalid → score ≈ 0.48

Behavioral std ranges from 0.1345 to 0.1465 across co-occurring conditions (n=120 each). All 4 conditions exceed the 0.05 variance gate. The behavioral means under noise (0.535–0.5675) are slightly lower than isolated (0.565), but all samples still exceed the 0.25 detection threshold.

### Positive Control (C1)

Structural discrimination is 0.8333, replicating parent experiments. Three unique fingerprints across four auth states because expired_token and invalid_token produce identical 401 authentication_failed surfaces.

### Null Control (C4)

FP rate is 0.0 on 240 noise-only samples. All behavioral scores are exactly 0.05 (admin-role baseline), well below the 0.25 detection threshold. The production-like noise types do not generate false positives.

## Product Consequences

### If SUPPORTS (this outcome)

Token_refresh detection is robust to production-like structural complexity, strengthening the C-FRESHNESS claim ceiling. The behavioral signal generalizes beyond simplistic noise patterns to realistic API response variation (pagination, variable-length data, error format variation, CDN headers). This expands the parallel-channel architecture coverage and moves C-FRESHNESS toward PRODUCT_CORE eligibility (pending production-substrate validation).

### Remaining Unknowns

1. Whether orthogonality survives on a non-mock production-like substrate with real OAuth/OIDC middleware, CDN caching, network RTT, and database-backed sessions (primary bottleneck for PRODUCT_CORE, inherited from parent)
2. Whether the expired_token/invalid_token fingerprint collision generalizes to production endpoints with differentiated error details (inherited from parent)
3. Whether within-condition behavioral variance and structural variance maintain on real network RTT and cache-freshness distributions beyond localhost jitter/TTL (inherited from parent)
4. Whether token_refresh behavioral_score generalizes to production token refresh endpoints where refresh failure may produce different error surfaces or graded severity (inherited from parent)
5. Whether 4 production-like structural noise types are sufficient coverage for production schema drift (inherited from parent)

## Claim Ceiling

This experiment validates C-FRESHNESS under production-like structural complexity at n=480 with TOST equivalence at delta=0.15 on the localhost mock ceiling (Flask 3.1.3 + SQLite WAL + in-memory TTL cache 0.5s + jitter 10–100ms + HS256/RS256 JWT on 127.0.0.1:18951, seed 42, p_refresh_success=0.7). The production-like noise types (pagination_metadata, variable_length_data, error_format_variation, cdn_cache_headers) are included in the claim ceiling. No production generalization, PRODUCT_CORE promotion, or non-mock inference is warranted from this evidence alone.

## Raw Evidence

- Raw experiment data: `raw_evidence/experiment_data.json` (sha256: b9ec764fb2d512930b97743e9dc6506f4f30dcdba17d3b8d0f7cc7cf04b1fca0)
- Runtime: ~96 seconds, single-threaded Werkzeug server on 127.0.0.1:18951
- Total HTTP request cycles: ~780 (40 phase-A + 480 phase-B + 240 phase-C + 60 phase-D)
- No LLM calls; no network beyond localhost.
