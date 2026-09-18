# EXP-GRAPH-35375596525 Report: Behavioral-Structural Signal Orthogonality Under HTTP Caching

## Executive Summary

**Orthogonality NOT confirmed: CI upper bound 0.2372 >= 0.15 under HTTP caching semantics.**

Behavioral and structural signals may share hidden common causes under HTTP caching conditions.

**Decision criteria (frozen from prereg):**
- **C1 (mean TP >= 0.85, all Wilson lower > 0.75)**: mean TP = 1.0000 -> PASS
- **C2 (variance >= 4/4 conditions)**: 4/4 conditions -> PASS
- **C3 (95% CI upper < 0.15)**: CI upper = 0.2372 -> FAIL
- **C4 (null FP = 0.0)**: FP = 0.0000 -> PASS

**Overall: FAIL**

**Outcome: MIXED**

**HTTP caching semantics tested:**
- Cache-Control: max-age=5 (enabled) / no-store (disabled)
- ETag: SHA-256 hash of response body (content-only)
- If-None-Match: conditional GET returning 304 Not Modified
- Vary: Accept, Authorization

## Design: HTTP Caching vs Parent

| Element | Parent (Stochastic, No HTTP Caching) | This Experiment (HTTP Caching) |
|---------|--------------------------------------|--------------------------------|
| Session state | SQLite DB + WAL-mode | SQLite DB + WAL-mode |
| Cache | In-memory TTL=0.5s | In-memory TTL=0.5s |
| Timing | Real I/O jitter 10-100ms | Real I/O jitter 10-100ms |
| JWT algorithm | HS256 + RS256 | HS256 + RS256 |
| HTTP caching | None | Cache-Control, ETag, If-None-Match, 304 |
| Co-occurring conditions | 2 drift x 4 noise = 8 | 2 drift x 2 caching = 4 |

## Primary Analysis

### Pooled Pearson Correlation

- **r = 0.1140** (|r| = 0.1140)
- **n = 240** paired samples (4 conditions x 60 samples)
- **95% CI (Fisher z)**: [-0.0128, 0.2372]
- **CI upper bound = 0.2372** >= **0.15 (frozen threshold)**
- **Shared variance ceiling**: 5.63% (at CI upper bound)

### TOST Equivalence Test

| Delta | Pass | p_upper | p_lower |
|-------|------|---------|---------|
| 0.1 | FAIL | 0.5862 | 0.0005 |
| 0.12 | FAIL | 0.4626 | 0.0001 |
| 0.15 | FAIL | 0.2863 | 0.0000 |
| 0.2 | FAIL | 0.0872 | 0.0000 |

### Signal Observability (Within-Condition Variance)

- **Conditions with variance**: 4/4
- **cooccur_permission_boundary+cache_enabled**: b_std=0.1633, s_std=1.5671 -> OK
- **cooccur_permission_boundary+cache_disabled**: b_std=0.1502, s_std=1.8050 -> OK
- **cooccur_session_invalidation+cache_enabled**: b_std=0.4180, s_std=1.5451 -> OK
- **cooccur_session_invalidation+cache_disabled**: b_std=0.4282, s_std=1.8150 -> OK

### Per-Condition Pearson r (Exploratory)

| Condition | r | p | n |
|-----------|---|---|---|
| cooccur_permission_boundary+cache_enabled | -0.1997 | 0.1260 | 60 |
| cooccur_permission_boundary+cache_disabled | 0.0557 | 0.6727 | 60 |
| cooccur_session_invalidation+cache_enabled | -0.0275 | 0.8346 | 60 |
| cooccur_session_invalidation+cache_disabled | 0.0804 | 0.5413 | 60 |

### Per-Drift-Pattern Pearson r (Exploratory)

| Drift Pattern | Samples | r |
|---------------|---------|---|
| permission_boundary | 120 | -0.0662 |
| session_invalidation | 120 | 0.0265 |

### Per-Caching-Mode Pearson r (Exploratory — NEW)

| Caching Mode | Samples | r |
|--------------|---------|---|
| cache_enabled | 120 | -0.0055 |
| cache_disabled | 120 | 0.2170 |

### Session Status Code Distribution (Session Invalidation Conditions)

| Condition | 401 | 403 | 500 | Total |
|-----------|-----|-----|-----|-------|
| cooccur_session_invalidation+cache_enabled | 22 | 20 | 18 | 60 |
| cooccur_session_invalidation+cache_disabled | 22 | 22 | 16 | 60 |

## Power Analysis

- **Minimum detectable |r| at n=240**: 0.1266
- **Minimum n for |r|=0.05**: 1538
- **Observed |r|=0.1140**: does not reach minimum detectable

## Product Consequence

**Negative/mixed outcome**: CI upper bound 0.2372 >= 0.15 under HTTP caching semantics.

HTTP caching introduces coupling between behavioral and structural signals. The product architecture decision depends on the CI upper bound:

- If CI upper >= 0.20: Signals are non-orthogonal under HTTP caching. Product must pivot to fused classifiers.
- If CI upper is 0.15-0.20: Decision depends on product risk tolerance. delta=0.15 acceptable -> parallel channels with monitoring; delta=0.10 required -> fused classifiers or larger n.

## Controls

### C1 (Drift TP >= 0.85, all Wilson lower > 0.75)
- Observed mean TP: 1.0000
- All Wilson lower > 0.75: True
- **Pass: YES**

### C2 (Variance >= 4/4 conditions)
- Conditions with variance: 4/4
- **Pass: YES**

### C3 (95% CI upper < 0.15)
- CI upper bound: 0.2372
- **Pass: NO**

### C4 (Null FP = 0.0)
- FP count: 0/120
- **Pass: YES**

### Positive Control (Permission Boundary Detection)
- Detection rate: 1.0000
- **Pass: YES**

## Validity Threats

1. **ETag determinism**: ETags computed from content-only hash (excluding timing headers) to avoid timing-induced structural signal artifacts.
2. **304 response content**: 304 Not Modified responses carry no body. Structural signal computation handles empty-body responses gracefully by using cached schema.
3. **Cache-Control interaction with in-memory TTL**: Parent's in-memory cache (TTL=0.5s) and HTTP Cache-Control (max-age=5) operate at different layers. Both present in "enabled" condition — intentional simulation of real production.
4. **Sample size**: n=240 (vs parent's n=480) reduces power. Minimum detectable |r| = 0.129 vs parent's 0.090. Acceptable for delta=0.15 equivalence.
5. **Localhost network**: All requests are localhost. No CDN, no distributed cache, no network latency. Claim ceiling bounded to "HTTP caching semantics on localhost".

## Artifacts

- `raw_evidence/experiment_data.json` (sha256: 1a2d719102576dcb7cbb340f2fd7782eb30b164ef477db2c6ab61a488c3f5efa, role: raw)
- `mock_server.py` (sha256: 7d1064a9d5a2d630a45cd9b9e5c1d39c6813092b4eda7f4c6a373fa0d132dd86, role: code)
- `run_experiment.py` (sha256: 5598277cc730b2bb1608f15cc46bc16e5af88b4d1a3350a0c3b9f72b793997dd, role: code)
