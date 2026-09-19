# EXP-GRAPH-35389145821 — Preregistration

## Behavioral-Structural Signal Orthogonality Under HTTP Caching (Fixed Manipulation, Parent Power)

**Experiment ID**: EXP-GRAPH-35389145821  
**Lane**: graph  
**Claim**: C-FRESHNESS  
**Created**: 2026-09-18  

---

## 1. Question

Does behavioral-structural signal orthogonality (|r| < 0.15) hold when HTTP conditional caching is operationally exercised (client sends If-None-Match, server returns 304 Not Modified) at parent-matching power (n >= 480), and is the observed per-caching-mode heterogeneity (cache_enabled r~-0.006 vs cache_disabled r~0.217) replicable or attributable to sampling noise?

## 2. Hypothesis

The parent EXP-GRAPH-35353011131 established near-zero pooled correlation (|r|=0.0463, CI upper 0.135 < delta=0.15) on stochastic Flask+SQLite+cache+jitter+mixed JWT without HTTP caching. EXP-GRAPH-35375596525 tested HTTP caching but was measurement-confounded by three defects: (1) client never sent If-None-Match headers so the 304/ETag code path was untested; (2) n=240 is half parent power; (3) per-caching-mode heterogeneity opposite to hypothesis. This experiment fixes all three defects.

**H1 (primary)**: |r| < 0.15 at n >= 480 with proper 304 manipulation.  
**H0**: |r| >= 0.15 — HTTP caching creates coupling between behavioral and structural signals.

## 3. Three Defects Being Fixed

### Defect 1: 304 Never Exercised
- **Parent**: `run_experiment.py` never sends `If-None-Match` headers; the `mock_server.py` has 304 support but it was never triggered.
- **Fix**: Client stores ETag from prior `/schema` response and sends `If-None-Match: <etag>` on subsequent `/schema` requests. 304 response rate logged as manipulation check.

### Defect 2: Underpowered (n=240)
- **Parent**: n=240, SE=0.065, CI width ~0.25. At observed r=0.114, CI upper=0.237.
- **Fix**: n=120 per condition (480 total), SE~0.046, CI width ~0.18 at r~0.05. Matches parent EXP-GRAPH-35353011131 power.

### Defect 3: Per-Caching-Mode Heterogeneity
- **Parent**: cache_enabled r=-0.006 (PASS), cache_disabled r=0.217 (FAIL). Opposite to hypothesis.
- **Hypothesis for this experiment**: Heterogeneity was sampling noise at n=120 per mode. Replication at n=120 per mode will show whether the pattern persists.

### Bug: Decision-Rule Logic
- **Parent**: `run_experiment.py` maps `ci_upper >= 0.20` to `MIXED` (line 1074-1075), but spec.json says CI upper >= 0.20 maps to `FAIL`.
- **Fix**: CI upper >= 0.20 triggers FALSIFIES outcome, consistent with spec.json.

## 4. State Representation

### Behavioral Signal (Composite)
- `token_val_rate` = token_validation_failures / 3.0 (weight: 2)
- `session_change` = 0 or 1 (weight: 3) — always 1 for session_invalidation
- `auth_boundary` = auth_boundary_shifts / 3.0 (weight: 1)
- `session_status_check` = graded: 401->1.0, 403->0.5, 500->0.75 (weight: 2)

### Structural Signal (Composite)
- `jaccard_similarity` = Jaccard index of (field_name, field_type) pairs
- `schema_diff_magnitude` = weighted diff (field add/remove: 1.0, type change: 0.5, desc change: 0.3)
- `structural = max(schema_diff_magnitude, 1.0 - jaccard_similarity)`

## 5. Sampling Policy

- **N_SAMPLES**: 120 per co-occurring condition (480 total)
- **SEED**: 42
- **Co-occurring conditions**: 2 drift (permission_boundary, session_invalidation) x 2 caching (enabled, disabled) = 4
- **Noise-only conditions**: 2 caching modes x 120 samples = 240 null control
- **Positive control**: permission_boundary detection rate across both caching modes
- **Per-condition RNG**: `random.Random(SEED + condition_idx * 1000)` for within-condition sampling
- **Per-sample RNG**: `random.Random(condition_rng.randint(0, 2**31 - 1))` for per-sample variation

## 6. Unit of Analysis

Each paired sample: one behavioral composite score + one structural composite score from the same server state, drift pattern, noise pattern, and caching mode. No temporal grouping. Independence assumption: each sample resets server state and applies fresh drift + noise.

## 7. Holdout

No holdout. This is a fixed-design equivalence test. All samples contribute to the pooled correlation.

## 8. Nulls and Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-PARENT-STOCHASTIC-N480 | Parent stochastic mock without HTTP caching | CI upper < 0.15 |
| B-NO-CACHE-HEADERS | Within-experiment: no-store caching mode | CI upper < 0.15 |
| B-PARENT-HTTP-CACHING-N240 | Prior experiment with 3 defects | Indeterminate |
| NC-FP-CACHE | Noise-only samples, FP = 0.0 | FP = 0.0 |

## 9. Primary Metric

Pooled Pearson correlation r between behavioral composite and structural composite across all 480 paired samples, with 95% CI via Fisher z-transform. **Decision criterion**: CI upper bound < 0.15.

## 10. Expected Direction

Orthogonality: |r| near zero, CI upper bound < 0.15. If HTTP caching introduces coupling, |r| increases and CI upper bound exceeds 0.15.

## 11. Uncertainty Method

- Fisher z-transform for 95% CI: `r +/- 1.96 / sqrt(n-3)` in z-space
- TOST equivalence test at delta=0.15: reject H0: |r| >= 0.15 if both one-sided p < 0.05
- Wilson score interval for TP rate CIs

## 12. Adequacy Rule

- **Power**: n=480, SE~0.046. At observed r=0.114 (parent HTTP caching), CI width ~0.18. CI upper bound ~0.114 + 1.96*0.046 = 0.204 — MARGINAL. At parent r=0.046, CI upper 0.135 — SUFFICIENT. The experiment is powered to confirm parent-level orthogonality; it is NOT powered to detect |r| = 0.08 with CI upper < 0.15.
- **Sample size**: 480 total, 120 per condition. Matches parent EXP-GRAPH-35353011131.

## 13. Falsification / Survival Rule

**PASS** if ALL of C1-C5 pass.  
**FAIL** if any fails.  
**MIXED** if C1-C2-C4-C5 pass and C3 fails with CI upper in [0.15, 0.20).  
**FALSIFIES** if C1-C2-C4-C5 pass and C3 fails with CI upper >= 0.20.

### Decision Criteria

| ID | Criterion | Threshold | Source |
|----|-----------|-----------|--------|
| C1 | Drift detection TP rate | mean TP >= 0.85 AND all Wilson lower CI > 0.75 | Frozen |
| C2 | Within-condition variance | >= 4/4 conditions with std > 0 for both signals | Frozen |
| C3 | Orthogonality | 95% CI upper bound on |r| < 0.15 | Frozen |
| C4 | Null control | FP = 0.0 on noise-only samples | Frozen |
| C5 | 304 manipulation check | 304 response rate >= 10% in cache_enabled condition | NEW |

## 14. Exploratory Analyses (Not Confirmatory)

- Per-condition Pearson r (4 conditions)
- Per-drift-pattern r (permission_boundary vs session_invalidation)
- Per-caching-mode r (cache_enabled vs cache_disabled) — tests heterogeneity replication
- TOST at multiple deltas (0.10, 0.12, 0.15, 0.20)
- Cache hit rate, ETag match rate, 304 rate as manipulation checks
- I/O latency distribution (cache_hit vs cache_miss)
- Power analysis for observed r

## 15. Server Infrastructure

- **Flask 3.1.3** with threaded mode
- **SQLite WAL-mode** for session/permission state
- **In-memory cache** with TTL=0.5s for /schema responses
- **Jitter**: 10-100ms uniform on DB reads, cache lookups, JWT signing
- **JWT algorithms**: HS256 (read/write), RS256 (admin)
- **HTTP caching** (enabled mode): Cache-Control: max-age=5, ETag from body SHA-256, If-None-Match conditional GET, 304 Not Modified
- **HTTP caching** (disabled mode): Cache-Control: no-store, no ETag generation, no conditional requests

## 16. Manipulation Checks (NEW)

- **304 response rate**: fraction of /schema requests in cache_enabled condition that return 304
- **ETag match rate**: fraction of If-None-Match headers that match current ETag
- **Cache hit rate**: fraction of /schema requests served from in-memory TTL cache
- **I/O latency**: time per /schema request, broken down by cache_hit/cache_miss and 304/200

## 17. Validity Threats

1. **ETag generation from response body creates body-structural correlation**: ETag is SHA-256 of body bytes; if body changes with noise, ETag changes too. This could create coupling through the structural channel. Mitigation: ETag computed from content-only hash excluding timing headers; this is the same as the parent.

2. **In-memory TTL cache (0.5s) vs HTTP Cache-Control (max-age=5)**: Two caching layers coexist. The TTL cache causes stale/fresh alternation independent of HTTP caching. This is intentional: it preserves the parent's stochastic alternation while adding HTTP caching on top.

3. **If-None-Match rate depends on timing**: If requests are faster than TTL, the client receives cached 200 responses with the same ETag and sends matching If-None-Match. If requests are slower, new ETags are generated. The 10-100ms jitter with ~1s request interval creates approximately 50% cache hit rate.

4. **Per-caching-mode heterogeneity**: The parent observed cache_enabled r=-0.006 vs cache_disabled r=0.217. This experiment replicates at n=120 per mode to test whether the pattern is systematic or noise.

5. **localhost scope**: All measurements on localhost with Flask mock server. Not validated for production databases, distributed caches, CDN, or network latency.

## 18. Code Changes from Parent

### mock_server.py changes:
- Add `If-None-Match` handling in `/schema` route: compare `request.headers.get("If-None-Match")` with computed ETag
- Return 304 when match (already present in parent server code, but never triggered)
- Log 304 vs 200 response type per request

### run_experiment.py changes:
- **Defect 1 fix**: Store ETag from prior `/schema` response; send `If-None-Match: <etag>` on subsequent requests
- **Defect 2 fix**: N_SAMPLES = 120 (was 60), total = 480 (was 240)
- **Defect 3 fix**: No code change — replication at higher n will test heterogeneity
- **Decision-rule bug fix**: `ci_upper >= 0.20` maps to FALSIFIES (was MIXED)
- **New artifacts**: Log 304 rate, ETag match rate, cache hit rate, I/O latency distribution
- **New control C5**: 304 response rate >= 10% in cache_enabled condition

## 19. Consequences

### If PASS (CI upper < 0.15 at n >= 480 with 304 exercised):
- C-FRESHNESS orthogonality confirmed under operational HTTP caching
- Parallel-channel architecture justified for production APIs with caching
- Product can deploy behavioral + structural as independent channels

### If FALSIFIES (CI upper >= 0.20 at n >= 480 with 304 exercised):
- HTTP caching creates coupling between behavioral and structural signals
- Product must consider fused classifiers or cache-independent structural signals
- Structural signals should be computed from pre-cache API contract, not cached response body

### If MIXED (CI upper 0.15-0.20):
- Indeterminate: orthogonality not confirmed but not decisively falsified
- Product decision depends on risk tolerance at delta=0.15
- Consider larger n or delta=0.10 equivalence margin

### If C5 fails (304 rate < 10%):
- Manipulation failed: If-None-Match was not effectively sent
- Infrastructure issue, not scientific result
- Must fix client implementation and re-run
