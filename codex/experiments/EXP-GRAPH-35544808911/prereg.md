# EXP-GRAPH-35544808911 Preregistration

## Experiment

C-FRESHNESS Orthogonality on Distributed Infrastructure -- C1 Fix and Re-Run

## Claim IDs

C-FRESHNESS

## Question

After fixing C1 behavioral detection control to exclude 304 responses (consistent with primary metric's 304 exclusion), does C-FRESHNESS orthogonality at delta=0.15 achieve CONFIRMED status on distributed infrastructure with n_non304>=800 -- and does the C1 fix also resolve the parent audit's reporting inconsistency (C2/C7 including 304s)?

## 1. Background and Motivation

Parent experiment EXP-GRAPH-35538864957 tested C-FRESHNESS orthogonality at delta=0.15 on distributed 2-node Flask infrastructure. The frozen decision_rule triggered FALSIFIES because C1 behavioral detection control failed (mean TN=0.686 < 0.85 threshold). The root cause is a measurement validity issue: 304 cache-hit responses are included in behavioral TP/TN calculation. When valid tokens with cache enabled produce 304 status codes, the behavioral signal extraction maps status_code=304 to behavioral_delta=1.0 (via default status_weight=0.5), causing false negative TN failures.

However, the primary orthogonality metric is valid and independently confirms orthogonality: endpoint-stratified pooled r=-0.0585, 95% CI [-0.1327, 0.0163], CI upper 0.0163 < 0.15, TOST p_upper=2.03e-08 < 0.05, n_non304=688. Audit V1 confirms C1 passes when 304s are excluded (TN=1.0). C2-C7 all PASS.

The parent handoff recommends: fix C1 to exclude 304s (consistent with primary metric's 304 exclusion) and re-run with n_non304>=800 to achieve CONFIRMED status.

## 2. Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED on distributed multi-node infrastructure after fixing the C1 measurement validity issue. The parent's FALSIFIES outcome was driven entirely by 304 cache-hit responses being included in behavioral TP/TN calculation (TN=0.686 with 304s, TN=1.0 without 304s). The primary orthogonality metric independently confirms orthogonality.

## 3. The Fix

C1 behavioral detection control now excludes 304 responses from TP/TN calculation. This is consistent with the primary orthogonality metric which already excludes 304s. The fix filters 304 rows before computing C1 TP/TN. This is a targeted code change (~5 lines) in run_experiment_distributed.py.

## 4. Conditions

### 4.1 Primary Condition: B-DISTRIBUTED

Multi-node distributed testbed with C1 304-exclusion fix applied. Same infrastructure as parent: 2 independent Flask processes on separate ports, each with independent SQLite database and in-memory CDN cache. Round-robin request routing. Each node independently generates ETag/Cache-Control headers. Cache invalidation on one node does NOT propagate to the other.

### 4.2 Baseline: B-LOCAL-ONLY

Single-node Flask testbed WITHOUT concurrent load or multi-node distribution -- identical to parent EXP-GRAPH-35530590140 LOCAL testbed.

### 4.3 Baseline: B-CONCURRENT

Single-node Flask testbed with 5 concurrent client sessions making simultaneous requests.

### 4.4 Negative Control: B-CONFOUND-DISTRIBUTED

Distributed negative control with V2 confound (fixed 'expired' request_id for expired responses, uuid4 for valid).

## 5. Controls

### 5.1 Positive Control (C1)

Token validation failure detection on distributed infrastructure. Behavioral signal must correctly identify expired vs valid tokens with TP >= 0.85 across all distributed nodes. After 304 exclusion, all cache-enabled valid-token conditions that previously produced TN=0.0588 will now correctly exclude 304 responses, yielding TN=1.0.

### 5.2 Null Control (C2)

Structural signal std > 0 across all non-304 conditions on distributed infrastructure. Independent ETag generation per node, Cache-Control headers, and UUID-based dynamic content should produce non-zero structural variation.

### 5.3 Negative Control (C7)

B-CONFOUND-DISTRIBUTED shows endpoint-stratified weighted |r| >= 0.15. V2 confound (fixed 'expired' request_id) reproduces the confound across distributed nodes.

## 6. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-LOCAL-ONLY | Single-node, no concurrency | \|r\| < 0.15 (parent r=0.041) |
| B-DISTRIBUTED | 2-node distributed | \|r\| < 0.15 (parent r=-0.0585) |
| B-CONCURRENT | Single-node + 5 concurrent sessions | \|r\| < 0.15 |
| B-CONFOUND-DISTRIBUTED | Distributed V2 confound negative control | \|r\| >= 0.15 |

## 7. Decision Rules

### 7.1 C-FRESHNESS orthogonality CONFIRMED if ALL:

- C1: behavioral detection TP >= 0.85 across all endpoints (AFTER 304 EXCLUSION)
- C2: at least 2/3 endpoints have non-304 behavioral signal std > 0 AND at least 2/3 have non-304 structural signal std > 0
- C3: 95% CI upper bound of endpoint-stratified pooled Pearson r (non-304 samples only) < 0.15
- C4: TOST equivalence test p_upper < 0.05 at delta=0.15 (one-sided, non-304 samples only)
- C5: endpoint-stratified cache-mode heterogeneity check (non-304 samples): |r_stratified_enabled - r_stratified_disabled| < 2 * SE_pooled
- C6: B-LOCAL-ONLY baseline shows |r| < 0.15 (no regression from parent)
- C7: B-CONFOUND-DISTRIBUTED shows endpoint-stratified weighted |r| >= 0.15 (negative control passes)

### 7.2 C-FRESHNESS orthogonality REJECTED if ANY condition fails.

### 7.3 MEASUREMENT_INVALID if infrastructure failure prevents data collection or n_non304 < 400.

## 8. Measurement Validity

1. **304 EXCLUSION FROM C1 (THE FIX)**: C1 behavioral detection control excludes 304 responses from TP/TN calculation. 304 cache-hit responses are HTTP caching artifacts, not behavioral signal changes.
2. **V_ETAG_PERMISSION_LEAKAGE FIX** (inherited): testbed_server_v3.py decodes expired JWT tokens WITHOUT verification to extract permission_level for ETag generation.
3. **V3 ENDPOINT-STRATIFICATION** (inherited): Pooled Pearson r uses endpoint-stratified weighting, not simple concatenation.
4. **V1 UUID FOR ALL STATUS CODES** (inherited): All request_ids use uuid.uuid4() for all status codes.
5. **304 EXCLUSION**: 304 responses excluded from pooled correlation, per-endpoint correlations, per-cache correlations, AND C1 behavioral detection control.
6. **DISTRIBUTED INDEPENDENCE**: Each Flask node has independent SQLite database, independent in-memory cache, independent ETag generation.
7. **NON-304 POWER**: n >= 800 non-304 samples.
8. **TOST ONE-SIDED**: C3 tests CI upper < 0.15 only; C4 tests TOST p_upper < 0.05 only.
9. **Structural signal extraction** uses ONLY: (a) ETag change, (b) Cache-Control change, (c) normalized Shannon entropy of UUID-based request_id, (d) SHA256(request_id)[:16] as int % 10000 / 10000.
10. **Each endpoint** has independent behavioral and structural signal extraction -- no shared variables.

## 9. Sample Size and Power

Target: n_non304 >= 800. Parent achieved 688. With 3 endpoints x 8 conditions x 34 samples = 816 target, additional sampling should meet or exceed 800. At n=800, min detectable |r| is approximately 0.070; observed |r|=0.0585 well within equivalence bounds.

## 10. Expected Outcomes

### Positive outcome (CONFIRMED)

All C1-C7 PASS. C-FRESHNESS orthogonality at delta=0.15 confirmed on distributed infrastructure. Product may proceed with parallel-channel architecture for multi-node deployment.

### Negative outcome (REJECTED)

Any C1-C7 fails after 304-exclusion fix. Identifies a genuine distributed infrastructure barrier beyond the 304 measurement artifact.

### Mixed outcome

C3 passes for delta=0.15 but not delta=0.10. Bounded confirmation at delta=0.15 only.

## 11. Product Consequences

- **CONFIRMED**: Parallel-channel architecture (separate behavioral and structural signal processing) justified for multi-node deployment. Product may proceed with dual-signal freshness detection across distributed cache topologies.
- **REJECTED**: Parallel-channel architecture NOT justified for multi-node deployment. Product must investigate cache-coupling as a correlation source and potentially use fused classifiers.

## 12. Carry Forward from Parent

### Established

- C-FRESHNESS orthogonality at delta=0.15 SUPPORTED by primary metric on distributed 2-node Flask testbed: stratified pooled r=-0.0585, 95% CI [-0.1327, 0.0163], CI upper 0.0163 < 0.15, TOST p_upper=2.03e-08, n_non304=688 (audit PASS on primary metric recomputation).
- C-FRESHNESS orthogonality CONFIRMED on LOCAL testbed (parent EXP-GRAPH-35530590140: r=0.0410, CI upper 0.116, TOST p_upper=0.002, n_non304=684, C1-C7 all PASS).
- Distributed infrastructure does not introduce behavioral-structural coupling: distributed r=-0.0585 directionally consistent with LOCAL r=0.041 (delta=0.107, within noise).
- B-CONCURRENT (N=5 concurrent client sessions): stratified r=-0.0319, n=816 -- concurrent load does not introduce coupling.
- B-CONFOUND-DISTRIBUTED negative control passes: |r|=0.8855 >= 0.15.
- B-LOCAL-ONLY baseline (C6): |r|=0.0471 < 0.15, no regression from parent.
- Distributed testbed architecture verified: 2 independent Flask nodes with independent SQLite DBs, independent in-memory CDN caches, independent ETag generation, round-robin routing.
- V1 UUID fix and V_ETAG permission leakage fix applied and verified.
- 6 prior localhost mock experiments (r=0.002-0.046) consistent with LOCAL r=0.041 and DISTRIBUTED r=-0.0585.

### Rejected

- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE -- not warranted; claim ceiling bounded to LOCAL production-like regime at delta=0.15 only.
- Simple-pooled pooled r as measure of orthogonality -- biased by endpoint heterogeneity.
- HTTP caching as common cause raising |r| above 0.15 -- seven experiments show orthogonality under caching.
- Body-inclusive structural signals as orthogonal to behavioral -- V1 error body confound fixed.

### Unknown

- Whether C-FRESHNESS orthogonality at delta=0.15 achieves CONFIRMED status after C1 304-exclusion fix.
- Whether orthogonality holds on actual distributed production infrastructure with real CDN hierarchies.
- Whether concurrent client load (N>=50 parallel sessions) changes correlation structure (tested at N=5 only).
- Whether the result generalizes to non-Flask frameworks (Django, FastAPI, Express).
- Whether headers-only structural signal captures sufficient variation for production use.
- Whether delta=0.10 is achievable at n_non304>=1200 (CI half-width <=0.05).

### Do Not Assume

- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE -- status remains EXPERIMENTAL with bounded LOCAL confirmation and distributed primary-metric support.
- The frozen FALSIFIES outcome constitutes scientific falsification of orthogonality -- the C1 failure is measurement-confounded.
- n_non304>=800 requirement satisfied -- achieved 688, 112 short in parent.
- Orthogonality holds on real distributed production infrastructure -- tested only on 2-node Flask in-memory CDN simulation.
- Headers-only structural signal is sufficient for production -- validated only on testbeds.
- Non-Flask frameworks preserve orthogonality -- untested.
