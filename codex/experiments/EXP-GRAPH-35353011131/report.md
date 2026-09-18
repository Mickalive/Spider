# EXP-GRAPH-35353011131 Report: Behavioral-Structural Signal Orthogonality on Stochastic API

## Executive Summary

**Orthogonality CONFIRMED: CI upper bound 0.1353 < 0.15 under stochastic API conditions.**

Behavioral and structural signals are independent parallel channels under stochastic DB/cache/timing/algorithm conditions.

**Decision criteria (frozen from prereg):**
- **C1 (mean TP >= 0.85, all Wilson lower > 0.75)**: mean TP = 1.0000 -> PASS
- **C2 (variance >= 6/8 conditions)**: 8/8 conditions -> PASS
- **C3 (95% CI upper < 0.15)**: CI upper = 0.1353 -> PASS
- **C4 (null FP = 0.0)**: FP = 0.0000 -> PASS

**Overall: PASS**

**Outcome: SUPPORTS**

**Stochastic elements tested:**
- SQLite DB-backed sessions (WAL-mode, real file I/O)
- In-memory cache with TTL=0.5s (stale/fresh alternation)
- Real I/O jitter 10-100ms (DB reads, cache lookups, JWT signing)
- Mixed JWT algorithms: HS256 (read/write), RS256 (admin)

## Design: Stochastic Server vs Parent

| Element | Parent (Deterministic) | This Experiment (Stochastic) |
|---------|----------------------|------------------------------|
| Session state | In-memory dict | SQLite DB with WAL-mode |
| Cache | None | In-memory cache with TTL=0.5s |
| Timing | Simulated jitter | Real I/O jitter (10-100ms) |
| JWT algorithm | HS256 only | HS256 (read/write) + RS256 (admin) |
| Error modes | Deterministic status codes | Stochastic from DB/cache failures |

## Primary Analysis

### Pooled Pearson Correlation

- **r = 0.0463** (|r| = 0.0463)
- **n = 480** paired samples (8 conditions x 60 samples)
- **95% CI (Fisher z)**: [-0.0434, 0.1353]
- **CI upper bound = 0.1353** < **0.15 (frozen threshold)**
- **Shared variance ceiling**: 1.83% (at CI upper bound)

### TOST Equivalence Test

| Delta | Pass | p_upper | p_lower |
|-------|------|---------|---------|
| 0.1 | FAIL | 0.1192 | 0.0007 |
| 0.12 | FAIL | 0.0525 | 0.0001 |
| 0.15 | PASS | 0.0110 | 0.0000 |
| 0.2 | PASS | 0.0003 | 0.0000 |

### Signal Observability (Within-Condition Variance)

- **Conditions with variance**: 8/8
- **cooccur_permission_boundary+optional_field_addition**: b_std=0.1633, s_std=1.0015 -> OK
- **cooccur_permission_boundary+description_change**: b_std=0.1502, s_std=0.7263 -> OK
- **cooccur_permission_boundary+response_time_jitter**: b_std=0.1373, s_std=0.6800 -> OK
- **cooccur_permission_boundary+field_type_normalization**: b_std=0.1551, s_std=0.7151 -> OK
- **cooccur_session_invalidation+optional_field_addition**: b_std=0.4329, s_std=0.8475 -> OK
- **cooccur_session_invalidation+description_change**: b_std=0.3629, s_std=0.7925 -> OK
- **cooccur_session_invalidation+response_time_jitter**: b_std=0.3918, s_std=0.6418 -> OK
- **cooccur_session_invalidation+field_type_normalization**: b_std=0.4069, s_std=0.6731 -> OK

### Per-Condition Pearson r (Exploratory)

| Condition | r | p | n |
|-----------|---|---|---|
| cooccur_permission_boundary+optional_field_addition | 0.1087 | 0.4084 | 60 |
| cooccur_permission_boundary+description_change | 0.0535 | 0.6849 | 60 |
| cooccur_permission_boundary+response_time_jitter | -0.0679 | 0.6061 | 60 |
| cooccur_permission_boundary+field_type_normalization | 0.1395 | 0.2879 | 60 |
| cooccur_session_invalidation+optional_field_addition | 0.1771 | 0.1757 | 60 |
| cooccur_session_invalidation+description_change | -0.1043 | 0.4276 | 60 |
| cooccur_session_invalidation+response_time_jitter | 0.1599 | 0.2223 | 60 |
| cooccur_session_invalidation+field_type_normalization | 0.1481 | 0.2588 | 60 |

### Per-Drift-Pattern Pearson r (Exploratory)

| Drift Pattern | Samples | r |
|---------------|---------|---|
| permission_boundary | 240 | 0.0851 |
| session_invalidation | 240 | 0.0769 |

### Session Status Code Distribution (Session Invalidation Conditions)

| Condition | 401 | 403 | 500 | Total |
|-----------|-----|-----|-----|-------|
| cooccur_session_invalidation+optional_field_addition | 22 | 23 | 15 | 60 |
| cooccur_session_invalidation+description_change | 23 | 11 | 26 | 60 |
| cooccur_session_invalidation+response_time_jitter | 17 | 20 | 23 | 60 |
| cooccur_session_invalidation+field_type_normalization | 22 | 18 | 20 | 60 |

## Power Analysis

- **Minimum detectable |r| at n=480**: 0.0895
- **Minimum n for |r|=0.05**: 1538
- **Observed |r|=0.0463**: does not reach minimum detectable

## Product Consequence

**Positive outcome**: CI upper bound 0.1353 < 0.15 under stochastic DB/cache/timing/algorithm conditions.

C-FRESHNESS orthogonality is confirmed beyond deterministic mocks. Product pipeline can integrate behavioral + structural as independent parallel channels with quantified shared-variance ceiling < 2.25% under realistic API conditions.

**However, claim ceiling is bounded to:**
- Flask 3.1.3 + SQLite WAL-mode + in-memory cache TTL=0.5s + PyJWT HS256/RS256 on localhost
- 8 co-occurring conditions, 480 paired samples, delta=0.15
- NOT validated for: production databases, distributed caches, network latency, OAuth/OIDC, stochastic SPA frontends, or delta=0.10

## Controls

### C1 (Drift TP >= 0.85, all Wilson lower > 0.75)
- Observed mean TP: 1.0000
- All Wilson lower > 0.75: True
- **Pass: YES**

### C2 (Variance >= 6/8 conditions)
- Conditions with variance: 8/8
- **Pass: YES**

### C3 (95% CI upper < 0.15)
- CI upper bound: 0.1353
- **Pass: YES**

### C4 (Null FP = 0.0)
- FP count: 0/240
- **Pass: YES**

### Positive Control (Permission Boundary Detection)
- Detection rate: 1.0000
- **Pass: YES**

## Validity Threats

1. **DB locking contention**: SQLite WAL-mode may serialize concurrent requests, reducing stochastic variation. Mitigated by per-thread connections and busy_timeout=5000ms.
2. **Cache hit rate**: TTL=0.5s with ~1s request interval ensures ~50% stale rate. Verified by cache monitoring.
3. **Single server instance**: All conditions on same machine. Claim ceiling bounded to localhost.
4. **RSA key generation**: Deterministic for fixed seed. Generated once at server start.
5. **Sample size**: n=480 sufficient for delta=0.15 but NOT for delta=0.10 (needs n~865).

## Artifacts

- `raw_evidence/experiment_data.json` (sha256: b9ce34242155ace4..., role: raw)
- `mock_server.py` (sha256: 5b6cf363a4779457..., role: code)
- `run_experiment.py` (sha256: 01c49b98ad829457..., role: code)
