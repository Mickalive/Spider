# EXP-GRAPH-35538864957 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-35538864957
- **Lane**: graph
- **Claim IDs**: C-FRESHNESS
- **Parent**: EXP-GRAPH-35530590140 (CONFIRMED at delta=0.15 on LOCAL testbed)

## 2. Question

Does C-FRESHNESS orthogonality at delta=0.15 survive on distributed production-like infrastructure with multi-node independent caches, concurrent client load (N>=5 parallel sessions), and independent cache invalidation across nodes — and does the correlation remain below the LOCAL testbed ceiling (r=0.041)?

## 3. Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED on distributed multi-node infrastructure. The LOCAL testbed result (stratified pooled r=0.041, CI upper 0.116, TOST p=0.002, n_non304=684) will generalize because:

1. Behavioral signals (token validation, session state) are independent of structural signals (ETag, Cache-Control, request_id entropy) regardless of cache topology.
2. Multi-node independent caches increase structural variance without introducing behavioral correlation.
3. Concurrent load adds timing jitter that does not couple the two signal domains.

The distributed correlation is expected to be |r| < 0.15, consistent with LOCAL.

## 4. Falsifier

C-FRESHNESS orthogonality is falsified at delta=0.15 if ANY of:

- **(C1)** Behavioral detection TP < 0.85 on distributed infrastructure (expired tokens not detected).
- **(C2)** Fewer than 2/3 endpoints have non-304 behavioral signal std > 0 AND fewer than 2/3 have non-304 structural signal std > 0.
- **(C3)** 95% CI upper bound of endpoint-stratified pooled Pearson r (non-304, stratified by endpoint) >= 0.15 on distributed testbed.
- **(C4)** TOST equivalence test p_upper >= 0.05 at delta=0.15 (one-sided, endpoint-stratified non-304).
- **(C5)** Endpoint-stratified cache-mode heterogeneity: |r_stratified_enabled - r_stratified_disabled| >= 2 * SE_pooled.
- **(C6)** B-LOCAL-ONLY baseline (single-node, no concurrency) shows |r| >= 0.15 (regression from LOCAL parent).
- **(C7)** B-CONFOUND-DISTRIBUTED negative control shows endpoint-stratified weighted |r| < 0.15 (confound fails to reproduce).

C-FRESHNESS orthogonality is REJECTED if ANY condition fails. MEASUREMENT_INVALID if infrastructure failure prevents data collection.

## 5. Experimental Conditions

### 5.1 Testbed Architecture

**Distributed testbed** (`testbed_server_v3.py`):
- 2 independent Flask processes on ports 18971 and 18972
- Each node has independent SQLite database (`/tmp/testbed_distributed_nodeA.db`, `/tmp/testbed_distributed_nodeB.db`)
- Each node has independent in-memory CDN cache
- Each node independently generates ETag-SHA256 and Cache-Control headers
- Cache invalidation on node A does NOT propagate to node B
- Round-robin request routing across nodes
- Same endpoints, JWT validation, and signal extraction as parent

**Concurrent load client** (`run_concurrent.py`):
- 5 concurrent client threads making simultaneous requests to B-CONCURRENT condition
- Each thread generates independent request tokens and measures response times
- Thread-safe signal extraction with per-thread state isolation

### 5.2 Conditions (4 conditions, 3 endpoints, 8 co-occurring patterns each)

| Condition | Description | Ports | Concurrency |
|-----------|-------------|-------|-------------|
| B-LOCAL-ONLY | Single-node Flask, no concurrency (parent replication) | 18970 | 1 (serial) |
| B-DISTRIBUTED | 2-node Flask, independent caches, round-robin | 18971, 18972 | 1 (serial per node) |
| B-CONCURRENT | Single-node Flask, 5 concurrent clients | 18970 | 5 (parallel) |
| B-CONFOUND-DISTRIBUTED | 2-node with V2 confound (fixed 'expired' request_id) | 18973, 18974 | 1 (serial per node) |

### 5.3 Co-occurring Patterns (8 per endpoint, per condition)

```
token_state x cache_mode x permission_level
= (valid|expired) x (cache_enabled|cache_disabled) x (read|write)
```

### 5.4 Endpoints (3)

```
/api/user/profile
/api/data/list
/api/session/status
```

## 6. Sample Size

- **Per condition per endpoint per pattern**: 34 non-304 samples
- **Per condition per endpoint**: 34 × 8 = 272 non-304 samples
- **Per condition total**: 272 × 3 endpoints = 816 non-304 samples
- **Total across 4 conditions**: 816 × 4 = 3,264 non-304 samples
- **304 samples**: excluded from correlation analysis (estimated 15-25% of total)
- **Minimum valid**: n >= 400 non-304 per condition (MEASUREMENT_INVALID threshold)

## 7. Signal Extraction

### 7.1 Behavioral Signals (inherited from parent, unchanged)

```python
behavioral_delta = token_validation_failure * 2.0 + session_state_change * 3.0 + auth_boundary_shift * 1.0 + status_weight * 2.0
```

Where:
- `token_validation_failure` = 1 if status_code == 401, else 0
- `session_state_change` = 1 if status_code == 401 OR (status_code == 200 AND body.valid == False), else 0
- `auth_boundary_shift` = 1 if status_code == 403, else 0
- `status_weight` = {200: 0.0, 401: 1.0, 403: 0.5, 500: 0.75}

### 7.2 Structural Signals (headers-only, inherited from parent)

```python
structural_composite = etag_var * 0.3 + cache_control_var * 0.3 + norm_entropy * 0.2 + dyn_hash_int * 0.2
```

Where:
- `etag_var` = 1 if ETag changed from previous sample, else 0
- `cache_control_var` = 1 if Cache-Control changed from previous sample, else 0
- `norm_entropy` = min(shannon_entropy(request_id) / 4.0, 1.0)
- `dyn_hash_int` = SHA256(request_id)[:16] as int % 10000 / 10000.0

### 7.3 Critical Validity Constraint

Request IDs use `uuid.uuid4()` for ALL status codes in primary testbed (V1 fix). B-CONFOUND-DISTRIBUTED uses fixed "expired" string for expired responses and uuid4 for valid responses.

## 8. Analysis Plan

### 8.1 Primary Metric

Endpoint-stratified pooled Pearson r between behavioral_delta and structural_composite on non-304 samples.

**Stratified pooling**: For each endpoint e, compute r_e from n_e paired samples. Pooled r = weighted average of r_e weighted by n_e.

**Fisher z-transform**: z = arctanh(r), SE = 1/sqrt(n-3), 95% CI on z, back-transform to r.

### 8.2 Decision Criteria

| ID | Criterion | Threshold | Test |
|----|-----------|-----------|------|
| C1 | Behavioral TP | mean_tp >= 0.85 AND mean_tn >= 0.85 | Wilson CI lower > 0.75 |
| C2 | Variance | >= 2/3 endpoints with std > 0 for both signals | Count endpoints |
| C3 | Equivalence | CI upper of stratified pooled r < 0.15 | One-sided 95% CI |
| C4 | TOST | TOST p_upper < 0.05 at delta=0.15 | One-sided equivalence |
| C5 | Cache heterogeneity | |r_enabled - r_disabled| < 2 * SE_pooled | Stratified difference |
| C6 | Local baseline | |r_B-LOCAL-ONLY| < 0.15 | Simple comparison |
| C7 | Confound control | |r_B-CONFOUND-DISTRIBUTED| >= 0.15 (stratified weighted) | Negative control |

**Conjunctive rule**: ALL C1-C7 must pass for CONFIRMED. ANY fail → REJECTED. Infrastructure failure → MEASUREMENT_INVALID.

### 8.3 TOST Equivalence Test

```
H0: |r| >= 0.15 (non-equivalent)
H1: |r| < 0.15 (equivalent)
Test statistic: z_upper = (0.15 - z_r) / SE
p_upper = 1 - Phi(z_upper)
Reject H0 if p_upper < 0.05
```

### 8.4 Per-Endpoint Analysis

For each endpoint, compute:
- Pearson r and p-value (non-304 samples only)
- Behavioral and structural signal std
- Whether endpoint has variance (both std > 0)

### 8.5 Power Analysis

For n=816 (per condition):
- SE = 1/sqrt(816-3) ≈ 0.035
- Min detectable |r| at alpha=0.05: tanh(1.96 × 0.035) ≈ 0.069
- At observed |r|=0.041: TOST p_upper ≈ 0.001 (well powered)

### 8.6 Secondary Analyses

1. **Distributed vs Local comparison**: Test whether stratified r differs significantly between B-DISTRIBUTED and B-LOCAL-ONLY (Fisher z-difference test).
2. **Concurrent vs Local comparison**: Test whether stratified r differs between B-CONCURRENT and B-LOCAL-ONLY.
3. **Per-node analysis**: For B-DISTRIBUTED, compute per-node r to detect node-level heterogeneity.
4. **Delta sweep**: Report TOST results at delta = 0.10, 0.12, 0.15, 0.20.

## 9. Controls

### 9.1 Positive Control

Token validation failure detection: behavioral signal must correctly identify expired vs valid tokens with TP >= 0.85 across all distributed nodes. If TP < 0.85, behavioral signal extraction is broken in multi-node setting.

### 9.2 Null Control

Structural signal std > 0 across all non-304 conditions: independent ETag generation per node, Cache-Control headers, and UUID-based dynamic content should produce non-zero structural variation.

### 9.3 Negative Control (B-CONFOUND-DISTRIBUTED)

Multi-node infrastructure with V2 confound (fixed "expired" request_id for expired responses, uuid4 for valid). Expected to show |r| >= 0.15, confirming the confound is genuine in distributed setting.

### 9.4 Regression Control (B-LOCAL-ONLY)

Re-run parent LOCAL testbed on same infrastructure to confirm no regression. Expected: |r| ~0.04, consistent with parent.

## 10. Measurement Validity

1. **V_ETAG_PERMISSION_LEAKAGE**: Expired tokens decoded WITHOUT verification to extract permission_level for ETag generation (inherited from parent).
2. **V3 ENDPOINT-STRATIFICATION**: Pooled r uses endpoint-stratified weighting, not simple concatenation (inherited from parent).
3. **V1 UUID FOR ALL STATUS CODES**: All request_ids use uuid.uuid4() for all status codes in primary testbed (inherited from parent).
4. **304 EXCLUSION**: 304 responses excluded from ALL correlations (pooled, per-endpoint, per-cache).
5. **DISTRIBUTED INDEPENDENCE**: Each Flask node has independent SQLite database, independent in-memory cache, independent ETag generation. No shared state between nodes.
6. **CACHE INDEPENDENCE**: Cache invalidation on node A does NOT propagate to node B.
7. **CONCURRENT ISOLATION**: B-CONCURRENT uses thread-safe request generation with per-thread state isolation.
8. **SIGNAL INDEPENDENCE**: No shared variables between behavioral and structural signal domains.

## 11. Product Consequences

### 11.1 If CONFIRMED (all C1-C7 PASS)

- C-FRESHNESS advances toward VALIDATED on distributed infrastructure.
- Parallel-channel architecture justified for multi-node deployment.
- Product may proceed with dual-signal freshness detection across distributed cache topologies.
- Claim ceiling: distributed Flask 3.1.3 + PyJWT RS256 + SQLite WAL-mode + independent per-node CDN simulation + round-robin routing.

### 11.2 If REJECTED (any C1-C7 FAIL)

- C-FRESHNESS orthogonality NOT confirmed on distributed infrastructure.
- Parallel-channel architecture NOT justified for multi-node deployment.
- Product must investigate cache-coupling as correlation source.
- Fused classifiers may be required instead of independent parallel channels.

### 11.3 If MEASUREMENT_INVALID

- No scientific conclusion warranted.
- Infrastructure failure, not scientific falsification.
- Identify blocking issue and design minimal re-run.

## 12. Estimated Cost

- **Development**: testbed_server_v3.py (~100 lines), run_distributed.py (~200 lines), run_experiment_distributed.py (~150 lines) — ~2 hours
- **Execution**: 4 conditions × ~1 hour each — ~4 hours
- **Analysis**: ~1 hour
- **Total**: ~7 compute-hours

## 13. Expected Information Gain

Very high: this is the minimum cost experiment that directly resolves the primary unknown from parent EXP-GRAPH-35530590140 — whether LOCAL orthogonality generalizes to distributed infrastructure with independent caches. Either outcome changes a product decision: CONFIRMED justifies multi-node parallel-channel deployment; REJECTED identifies cache coupling as a blocking issue.
