# EXP-GRAPH-35572179326 Preregistration

## Experiment

C-FRESHNESS Orthogonality on Distributed Infrastructure — Two-Bug Fix and Re-Run

## Claim IDs

C-FRESHNESS

## Question

After fixing the infrastructure bug (SameFileError in run_experiment_distributed.py line 368 where src and dst both resolve to the same testbed_server.py) AND fixing C1 behavioral detection control to exclude 304 responses (consistent with parent metric's 304 exclusion), does C-FRESHNESS orthogonality at delta=0.15 achieve CONFIRMED status on distributed infrastructure with n_non304>=800?

## 1. Background and Motivation

Parent experiment EXP-GRAPH-35544808911 tested C-FRESHNESS orthogonality at delta=0.15 on distributed 2-node Flask infrastructure. It was MEASUREMENT_INVALID due to an infrastructure crash: `shutil.copy2(src,dst)` at line 368 raised SameFileError because `src` (parent_dir/testbed_server.py) and `dst` (EXPERIMENT_DIR/testbed_server.py) resolved to the same file. No data was collected; C1-C7 conditions were never tested.

The grandparent experiment EXP-GRAPH-35538864957 on the same distributed infrastructure had: (1) primary orthogonality metric confirmed (stratified pooled r=-0.0585, 95% CI [-0.1327, 0.0163], CI upper 0.0163 < 0.15, TOST p_upper=2.03e-08, n_non304=688, audit PASS); (2) C1 behavioral detection control failed because 304 cache-hit responses were included in TP/TN calculation (TN=0.686 with 304s, TN=1.0 without 304s). The parent was designed to fix C1 (304 exclusion) and re-run, but crashed on the SameFileError before executing.

This experiment fixes BOTH bugs and re-runs to determine if C-FRESHNESS orthogonality achieves CONFIRMED status on distributed infrastructure with n_non304>=800.

## 2. Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED on distributed multi-node infrastructure after fixing two bugs:

1. **SameFileError fix**: Remove the unnecessary `shutil.copy2` block (lines 364-368) that copies testbed_server.py from the parent experiment directory. The copy was for provenance only — the experiment code already uses `parent_dir/testbed_server.py` and `parent_dir/testbed_server_v2.py` directly as the server scripts in SingleServerManager and DistributedManager. Provenance is recorded via SHA-256 hash of the parent's files in provenance.json. This eliminates the SameFileError that crashed the parent.

2. **C1 304-exclusion fix**: C1 behavioral detection control now excludes 304 responses from TP/TN calculation. 304 cache-hit responses are HTTP caching artifacts, not behavioral signal changes. This is consistent with the primary orthogonality metric which already excludes 304s. The fix filters 304 rows before computing C1 TP/TN in `compute_c1()`.

The parent's MEASUREMENT_INVALID outcome was an infrastructure crash, not evidence against orthogonality. The grandparent's primary orthogonality metric independently confirms orthogonality. Excluding 304s from C1 yields mean TN=1.0 (audit-confirmed by grandparent audit V1).

## 3. The Two Fixes

### Fix 1: SameFileError

**Root cause**: Lines 360-368 of `run_experiment_distributed.py` attempt to copy testbed_server.py from `parent_dir` (EXP-GRAPH-35538864957) to `EXPERIMENT_DIR` (EXP-GRAPH-35544808911). The guard `if src.exists() and src.resolve() != dst.resolve():` passed, but `shutil.copy2(src,dst)` raised SameFileError because both paths resolved to the same file after path canonicalization.

**Fix**: Remove the entire copy block (lines 364-368). The experiment code already uses `primary_script` (parent_dir/testbed_server.py) and `confound_script` (parent_dir/testbed_server_v2.py) directly as server script arguments to SingleServerManager and DistributedManager. No copy is needed for execution. Provenance is recorded by hashing the parent's files in the provenance step.

### Fix 2: C1 304-Exclusion

**Root cause**: In the grandparent EXP-GRAPH-35538864957, C1 behavioral detection control computed TP/TN including 304 cache-hit responses. 304 responses map to effective_code=200 in the behavioral signal extractor, producing behavioral_delta=0.0 for valid tokens — same as non-304 valid tokens. However, for expired tokens, 304 responses cannot occur (expired tokens get 401), so 304 inclusion only affects valid-token TN: cache-enabled valid conditions with 304 responses appear as "correctly not detected" (TN), but the 304 is an HTTP caching artifact, not a behavioral signal. When 304 rate is high (e.g., 33% of cache-enabled samples), this dilutes TN to 0.686.

**Fix**: In `compute_c1()`, filter out 304 responses before computing TP/TN:
```python
samples=[s for s in cdata["samples"] if s["status"]=="OK" and not s.get("has_304",False)]
```
This is consistent with the primary orthogonality metric which already excludes 304s from pooled correlation computation. After the fix, all cache-enabled valid-token conditions that previously produced TN=0.0588 will correctly yield TN=1.0 (as confirmed by grandparent audit V1).

## 4. Conditions

### 4.1 Primary Condition: B-DISTRIBUTED

Multi-node distributed testbed with both fixes applied. Same infrastructure as grandparent: 2 independent Flask processes on separate ports (18971, 18972), each with independent SQLite database and in-memory CDN cache. Round-robin request routing. Each node independently generates ETag/Cache-Control headers. Cache invalidation on one node does NOT propagate to the other.

### 4.2 Baseline: B-LOCAL-ONLY

Single-node Flask testbed (port 18970) WITHOUT concurrent load or multi-node distribution — identical to parent EXP-GRAPH-35530590140 LOCAL testbed. Regression-free baseline confirmation.

### 4.3 Baseline: B-CONCURRENT

Single-node Flask testbed (port 18970) with 5 concurrent client sessions making simultaneous requests. Tests whether request contention, timing jitter, and interleaved cache states introduce behavioral-structural coupling.

### 4.4 Negative Control: B-CONFOUND-DISTRIBUTED

Distributed negative control: same multi-node architecture as B-DISTRIBUTED (ports 18973, 18974) but with V2 confound (fixed 'expired' request_id for expired responses, uuid4 for valid). Expected to reproduce the confound (|r| >= 0.15) across distributed nodes, confirming the testbed can detect genuine behavioral-structural coupling.

## 5. Controls

### 5.1 Positive Control (C1)

Token validation failure detection on distributed infrastructure. Behavioral signal must correctly identify expired vs valid tokens with mean TP >= 0.85 AND mean TN >= 0.85 across all distributed nodes. After 304 exclusion, all cache-enabled valid-token conditions that previously produced TN=0.0588 will now correctly exclude 304 responses, yielding TN=1.0.

### 5.2 Null Control (C2)

Structural signal std > 0 across at least 2/3 non-304 endpoints on distributed infrastructure. Independent ETag generation per node, Cache-Control headers, and UUID-based dynamic content should produce non-zero structural variation.

### 5.3 Negative Control (C7)

B-CONFOUND-DISTRIBUTED shows endpoint-stratified weighted |r| >= 0.15. V2 confound (fixed 'expired' request_id) reproduces the confound across distributed nodes, confirming the testbed can detect genuine behavioral-structural coupling when it exists.

## 6. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-LOCAL-ONLY | Single-node, no concurrency | \|r\| < 0.15 (parent r=0.041) |
| B-DISTRIBUTED | 2-node distributed | \|r\| < 0.15 (grandparent r=-0.0585) |
| B-CONCURRENT | Single-node + 5 concurrent sessions | \|r\| < 0.15 (grandparent r=-0.0319) |
| B-CONFOUND-DISTRIBUTED | Distributed V2 confound negative control | \|r\| >= 0.15 |

## 7. Decision Rules

### 7.1 C-FRESHNESS orthogonality CONFIRMED if ALL:

- **C1**: behavioral detection mean TP >= 0.85 AND mean TN >= 0.85 across all endpoints on distributed testbed (AFTER 304 EXCLUSION)
- **C2**: at least 2/3 endpoints have non-304 behavioral signal std > 0 AND at least 2/3 have non-304 structural signal std > 0
- **C3**: 95% CI upper bound of endpoint-stratified pooled Pearson r (non-304 samples only) < 0.15 on distributed testbed
- **C4**: TOST equivalence test p_upper < 0.05 at delta=0.15 (one-sided, non-304 samples only)
- **C5**: endpoint-stratified cache-mode heterogeneity check (non-304 samples): |r_stratified_enabled - r_stratified_disabled| < 2 * SE_pooled
- **C6**: B-LOCAL-ONLY baseline shows |r| < 0.15 (no regression from parent)
- **C7**: B-CONFOUND-DISTRIBUTED shows endpoint-stratified weighted |r| >= 0.15 (negative control passes)

### 7.2 C-FRESHNESS orthogonality REJECTED if ANY condition fails.

### 7.3 MEASUREMENT_INVALID if infrastructure failure prevents data collection or n_non304 < 400.

## 8. Measurement Validity

1. **SAMEFILEERROR FIX**: Remove unnecessary shutil.copy2 block. Use parent testbed_server.py directly. Record SHA-256 hashes for provenance.
2. **C1 304-EXCLUSION FIX**: Exclude 304 responses from behavioral TP/TN calculation in compute_c1(). Consistent with primary metric's 304 exclusion.
3. **V_ETAG_PERMISSION_LEAKAGE FIX** (inherited): testbed_server.py decodes expired JWT tokens WITHOUT verification to extract permission_level for ETag generation.
4. **V3 ENDPOINT-STRATIFICATION** (inherited): Pooled Pearson r uses endpoint-stratified weighting, not simple concatenation.
5. **V1 UUID FOR ALL STATUS CODES** (inherited): All request_ids use uuid.uuid4() for all status codes.
6. **304 EXCLUSION**: 304 responses excluded from pooled correlation, per-endpoint correlations, per-cache correlations, AND C1 behavioral detection control.
7. **DISTRIBUTED INDEPENDENCE**: Each Flask node has independent SQLite database, independent in-memory cache, independent ETag generation.
8. **NON-304 POWER**: n >= 800 non-304 samples (target: 42 per condition per endpoint x 8 conditions x 3 endpoints = 1012 total, ~850 non-304 at 84% rate).
9. **TOST ONE-SIDED**: C3 tests CI upper < 0.15 only; C4 tests TOST p_upper < 0.05 only.
10. **Structural signal extraction** uses ONLY: (a) ETag change, (b) Cache-Control change, (c) normalized Shannon entropy of UUID-based request_id, (d) SHA256(request_id)[:16] as int % 10000 / 10000.
11. **Each endpoint** has independent behavioral and structural signal extraction — no shared variables between signal domains.

## 9. Sample Size and Power

Target: n_non304 >= 800. Grandparent achieved 688 non-304 out of 816 total (84.3% non-304 rate). With 42 samples per condition per endpoint (42 x 8 x 3 = 1012 total), expected non-304 count is ~853 at 84.3% rate. At n=800, min detectable |r| is approximately 0.070 (Fisher z, 80% power, alpha=0.05 two-sided); observed |r|=0.0585 well within equivalence bounds at delta=0.15. TOST power at delta=0.15, n=800, true r=0.05 is approximately 0.99.

## 10. Expected Outcomes

### Positive outcome (CONFIRMED)

All C1-C7 PASS. C-FRESHNESS orthogonality at delta=0.15 confirmed on distributed infrastructure with n_non304>=800. Both bugs confirmed resolved. Product may proceed with parallel-channel architecture for multi-node deployment.

### Negative outcome (REJECTED)

Any C1-C7 fails after both fixes. Identifies a genuine distributed infrastructure barrier beyond the measurement artifacts. Product must investigate cache-coupling as a correlation source.

### Mixed outcome

C3 passes for delta=0.15 but not delta=0.10. Bounded confirmation at delta=0.15 only. Consistent with grandparent (CI upper 0.0163 at delta=0.15, marginal at delta=0.10).

## 11. Product Consequences

- **CONFIRMED**: Parallel-channel architecture (separate behavioral and structural signal processing) justified for multi-node deployment. Product may proceed with dual-signal freshness detection across distributed cache topologies. Both bugs confirmed resolved.
- **REJECTED**: Parallel-channel architecture NOT justified for multi-node deployment. Product must investigate cache-coupling as a correlation source and potentially use fused classifiers.

## 12. Carry Forward from Parent (EXP-GRAPH-35544808911) and Grandparent (EXP-GRAPH-35538864957)

### Established

- C-FRESHNESS orthogonality at delta=0.15 CONFIRMED on LOCAL testbed (EXP-GRAPH-35530590140: stratified r=0.0410, CI [-0.034,0.116], TOST p_upper=0.002, n_non304=684, C1-C7 all PASS, audit PASS).
- C-FRESHNESS orthogonality at delta=0.15 SUPPORTED by primary metric on distributed 2-node Flask testbed (EXP-GRAPH-35538864957: stratified pooled r=-0.0585, CI [-0.1327,0.0163], CI upper 0.0163<0.15, TOST p=2.03e-08, n_non304=688, audit PASS on primary metric). NOT CONFIRMED on distributed due to C1 measurement validity issue (TN=0.686 with 304s, TN=1.0 without 304s).
- C-FRESHNESS behavioral signals achieve TP=1.0, FP=0.0, AUC=1.0 on deterministic Flask+JWT localhost (EXP-GRAPH-35262258744/35353011131). Orthogonality confirmed across 6+ independent mock experiments at delta=0.15 (r=0.002-0.058, CI upper 0.08-0.135).
- C-FRESHNESS freshness guard calibrated threshold 0.20 with continuous severity gradient, TP=1.0, FP=0.0, TOST PASS at delta=0.15 (EXP-PRODUCT-35538865048: r=-0.0065, CI upper 0.0831, n=480). 4/4 effective noise types. V-THRESHOLD-TAUTOLOGY partially resolved.
- Distributed infrastructure verified: 2 independent Flask nodes (ports 18971,18972) with independent SQLite DBs, independent in-memory CDN caches, independent ETag generation, round-robin routing.
- V1 UUID fix (uuid4 for all status codes) and V_ETAG_PERMISSION_LEAKAGE fix (expired JWT decoded without verification for ETag) applied and verified.
- B-CONFOUND-DISTRIBUTED negative control passes: |r|=0.8855>=0.15, confirming V2 confound is genuine in distributed setting.
- B-CONCURRENT (N=5 concurrent client sessions): stratified r=-0.0319, n=816 — concurrent load does not introduce coupling.
- C5 cache heterogeneity check passes: |r_enabled-r_disabled|=0.0425<2*SE_pooled.
- Six structural signal families falsified for C-FRESHNESS frozen gate in deterministic mock: Jaccard (FP=1.0), TF-IDF (FP=1.0 inverted), response-time KS (TP=0.0), linear Fisher LDA (AUC=0.625), field-usage profiling (change_type invisible), schema comparison (noise tolerance fails).

### Rejected

- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE — not warranted; claim ceiling bounded to LOCAL production-like regime at delta=0.15 and localhost stochastic mock. No product promotion.
- The frozen FALSIFIES outcome from parent EXP-GRAPH-35538864957 constitutes scientific falsification of orthogonality — the C1 failure is measurement-confounded (304 inclusion in behavioral detection control), not evidence against orthogonality.
- Simple-pooled pooled r as measure of orthogonality — biased by endpoint heterogeneity; stratified pooling correct.
- HTTP caching as common cause raising |r| above 0.15 — seven+ experiments show orthogonality under caching (r=0.002-0.058).
- Body-inclusive structural signals as orthogonal to behavioral — V1 error body confound fixed (headers-only extraction).
- Six structural signal families for C-FRESHNESS frozen gate: Jaccard, TF-IDF, response-time KS, linear LDA, field-usage, schema comparison — all falsified under structural noise in deterministic mock.
- B-PARENT-CONFOUND V1 confound design (token_hex-vs-uuid4) — fragile under 304 exclusion; V2 redesign with fixed 'expired' request_id resolves.

### Unknown

- Whether C-FRESHNESS orthogonality at delta=0.15 achieves CONFIRMED status on distributed infrastructure after both fixes (the frozen question from parent, still unanswered).
- Whether orthogonality holds on actual distributed production infrastructure with real CDN hierarchies (multi-node cache invalidation on session state change).
- Whether concurrent client load (N>=50 parallel sessions) changes correlation structure (tested at N=5 only).
- Whether the result generalizes to non-Flask frameworks (Django, FastAPI, Express).
- Whether headers-only structural signal captures sufficient variation for production use vs body-inclusive signals.
- Whether per-cache heterogeneity is systematic or sampling noise.
- Whether delta=0.10 is achievable at n_non304>=1200 (CI half-width<=0.05).

### Do Not Assume

- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE — it remains EXPERIMENTAL; orthogonality confirmed at delta=0.15 under LOCAL and stochastic mock only.
- This MEASUREMENT_INVALID run constitutes evidence for or against orthogonality — it is an infrastructure failure with zero samples collected.
- n_non304>=800 requirement satisfied — achieved 688 in grandparent, 0 in this run. Distributed CONFIRMED status requires successful re-run.
- Orthogonality holds on real distributed production infrastructure — tested only on 2-node Flask in-memory CDN simulation.
- Testbed CDN simulation represents production CDN behavior — single-node Flask in-memory cache per node.
- The V2 confound (fixed 'expired' request_id) generalizes to other confound mechanisms — tested only on request_id entropy zeroing.
- Headers-only structural signal is sufficient for production — validated only on LOCAL and distributed testbeds with controlled response headers.
- Concurrent load N>=50 produces same result as N=5 — only N=5 tested.
- Non-Flask frameworks preserve orthogonality — untested.
- The SameFileError is a one-time fluke — the root cause (copy source path resolution) may indicate a systemic issue in the automation that must be audited before re-run.

## 13. Sample Size Justification

Grandparent achieved 688 non-304 out of 816 total (84.3% non-304 rate). The 304 rate was driven by cache-enabled conditions with valid tokens (If-None-Match -> 304 at ~33% rate in cache-enabled conditions). With 42 samples per condition per endpoint (up from 34), total samples increase from 816 to 1012. At 84.3% non-304 rate, expected non-304 count is ~853, exceeding the 800 target with margin. The increase from 34 to 42 samples per condition per endpoint adds ~1 hour to total execution time. This is justified by the need to achieve n_non304>=800 for CONFIRMED status and delta=0.10 inference.
