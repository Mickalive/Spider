# EXP-GRAPH-35611618323 preregistration

## 1. Question

After fixing the DistributedManager RSA key sharing bug by switching to HS256 symmetric JWT with shared TESTBED_SECRET, AND fixing numpy.bool_ JSON serialization, does C-FRESHNESS orthogonality at delta=0.15 achieve CONFIRMED status on distributed infrastructure with n_non304>=800?

## 2. Hypothesis

C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED on distributed multi-node infrastructure after fixing two bugs:

1. **RSA key sharing (PRIMARY)**: Switch testbed_server.py from RS256 (per-process RSA keypair via `generate_rsa_keys()`) to HS256 (shared `TESTBED_SECRET` env var). This eliminates token cross-node invalidation that caused all distributed valid-token samples to return 401 (behavioral_delta=7.0 constant, std=0, r=NaN).
2. **JSON serialization**: Cast `numpy.bool_` to `bool()` and handle NaN via None before `json.dump` at line 696. This ensures result.json persists raw metrics instead of falling back to empty metrics/controls.

The parent's MEASUREMENT_INVALID was caused entirely by these two infrastructure bugs. The grandparent's primary orthogonality metric independently confirms orthogonality on distributed infrastructure (stratified r=-0.0585, CI upper 0.0163 < 0.15, TOST p=2.03e-08, n_non304=688, audit PASS). LOCAL orthogonality is CONFIRMED across multiple experiments (r=0.023-0.047, n=684-844). With the RSA fix restoring valid-token 200 responses on distributed nodes and the JSON fix enabling proper metrics persistence, all C1-C7 conditions are expected to pass at n_non304>=800.

## 3. Falsifier

C-FRESHNESS orthogonality at delta=0.15 on distributed infrastructure is **REJECTED** if ANY of the following occurs after the two fixes:

- (C1) behavioral detection mean TP < 0.85 OR mean TN < 0.85 on distributed infrastructure (after 304 exclusion)
- (C2) fewer than 2/3 endpoints have non-304 behavioral signal std > 0 OR fewer than 2/3 have non-304 structural signal std > 0
- (C3) 95% CI upper bound of endpoint-stratified pooled Pearson r (non-304 only) >= 0.15 on distributed testbed
- (C4) TOST equivalence test p_upper >= 0.05 at delta=0.15 (one-sided, non-304 only)
- (C5) endpoint-stratified cache-mode heterogeneity: |r_stratified_enabled - r_stratified_disabled| >= 2 * SE_pooled
- (C6) B-LOCAL-ONLY baseline shows |r| >= 0.15 (regression from LOCAL parent)
- (C7) B-CONFOUND-DISTRIBUTED shows endpoint-stratified weighted |r| < 0.15 (confound fails to reproduce)

C-FRESHNESS orthogonality is **MEASUREMENT_INVALID** if infrastructure failure prevents data collection or if n_non304 < 400.

## 4. Parent chain and inherited state

### Established (from carry_forward)
- C-FRESHNESS orthogonality at delta=0.15 CONFIRMED on LOCAL testbed (EXP-GRAPH-35530590140: stratified r=0.0410, CI [-0.034,0.116], TOST p=0.002, n_non304=684, C1-C7 all PASS, audit PASS). Reconfirmed in parent (r=0.0233, n=844, CI upper 0.0907, TOST p=0.000105).
- C-FRESHNESS orthogonality at delta=0.15 SUPPORTED by primary metric on distributed 2-node Flask testbed (EXP-GRAPH-35538864957: stratified pooled r=-0.0585, CI [-0.1327,0.0163], CI upper 0.0163<0.15, TOST p=2.03e-08, n_non304=688, audit PASS on primary metric). NOT CONFIRMED on distributed due to C1 measurement validity issue (TN=0.686 with 304s, TN=1.0 without 304s).
- C-FRESHNESS behavioral signals achieve TP=1.0, FP=0.0, AUC=1.0 on deterministic Flask+JWT localhost (EXP-GRAPH-35262258744/35353011131). Orthogonality confirmed across 6+ independent mock experiments at delta=0.15 (r=0.002-0.058, CI upper 0.08-0.135).
- C-FRESHNESS freshness guard calibrated threshold 0.20 with continuous severity gradient, TP=1.0, FP=0.0, TOST PASS at delta=0.15 (EXP-PRODUCT-35538865048: r=-0.0065, CI upper 0.0831, n=480). 4/4 effective noise types.
- B-CONCURRENT reconfirmed in parent (r=0.0233, n=860, CI upper 0.090, TOST PASS) — concurrent load N=5 does not introduce coupling.
- B-CONFOUND-DISTRIBUTED negative control passes: |r|=0.8855>=0.15 (EXP-GRAPH-35538864957), confirming V2 confound is genuine in distributed setting.
- Six structural signal families falsified for C-FRESHNESS frozen gate in deterministic mock: Jaccard, TF-IDF, response-time KS, linear Fisher LDA, field-usage profiling, schema comparison.

### Rejected
- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE — not warranted; claim ceiling bounded to LOCAL production-like regime at delta=0.15 and localhost stochastic mock. No product promotion.
- Simple-pooled pooled r as measure of orthogonality — biased by endpoint heterogeneity; stratified pooling correct.
- HTTP caching as common cause raising |r| above 0.15 — seven+ experiments show orthogonality under caching (r=0.002-0.058).
- Body-inclusive structural signals as orthogonal to behavioral — V1 error body confound fixed (headers-only extraction).
- Six structural signal families for C-FRESHNESS frozen gate: all falsified under structural noise in deterministic mock.

### Unknown
- Whether C-FRESHNESS orthogonality at delta=0.15 achieves CONFIRMED status on distributed infrastructure after RSA key sharing fix (the frozen question from parent, still unanswered after 3 consecutive MEASUREMENT_INVALID runs).
- Whether orthogonality holds on actual distributed production infrastructure with real CDN hierarchies.
- Whether concurrent client load (N>=50 parallel sessions) changes correlation structure (tested at N=5 only).
- Whether the result generalizes to non-Flask frameworks (Django, FastAPI, Express).
- Whether delta=0.10 is achievable at n_non304>=1200 (CI half-width<=0.05).

### Do not assume
- C-FRESHNESS reaches VALIDATED or PRODUCT_CORE — it remains EXPERIMENTAL; orthogonality confirmed at delta=0.15 under LOCAL and stochastic mock only.
- This MEASUREMENT_INVALID run constitutes evidence for or against orthogonality — it is an infrastructure failure with zero valid distributed samples.
- n_non304>=800 requirement satisfied — achieved 688 in grandparent, 0 in parent. Distributed CONFIRMED status requires successful re-run.
- Orthogonality holds on real distributed production infrastructure — tested only on 2-node Flask in-memory CDN simulation.
- The HS256 fix trivially resolves the RSA problem — the grandparent used RS256 with apparently different behavior; root cause of the grandparent's success is not fully understood.

## 5. Implementation changes

### Change 1: HS256 symmetric JWT (PRIMARY FIX)

**File**: `testbed_server.py` (parent experiment's server script)

**Current behavior**: `generate_rsa_keys()` creates per-process RSA keypair; `validate_token()` uses RS256 algorithm; each Flask worker has independent keys.

**Fix**: Replace RSA with HS256 using shared `TESTBED_SECRET`:
```python
# Remove: generate_rsa_keys() function and RSA key variables
# Add: 
import os
SECRET_KEY = os.environ.get("TESTBED_SECRET", "default-secret-for-testing")

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def create_token(user_id, permission_level, expires_in=3600):
    payload = {
        "user_id": user_id,
        "permission_level": permission_level,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Rationale**: The `TESTBED_SECRET` is already generated and passed to child processes by `DistributedManager` (line 109: `env["TESTBED_SECRET"]=secrets.token_hex(32)`). This ensures all nodes share the same signing key. HS256 is simpler than RSA and eliminates key distribution entirely.

### Change 2: JSON serialization fix

**File**: `run_experiment_distributed.py` line 696

**Current behavior**: `json.dump(result)` fails on `numpy.bool_` and NaN values.

**Fix**:
```python
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# At line 696:
with open(result_path, 'w') as f:
    json.dump(result, f, cls=NumpyEncoder, indent=2)
```

### Change 3: Stratified pooled r handling of degenerate inputs

**File**: `run_experiment_distributed.py` (stratified_pooled_r function)

**Current behavior**: When behavioral signal is constant (std=0), `pearsonr` returns NaN and stratified pooling yields NaN/n=0.

**Fix**: Detect constant-input case, flag C2 failure immediately, and report with explicit reason rather than propagating NaN to CI/TOST.

## 6. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-LOCAL-ONLY | Single-node Flask testbed, no concurrency, no distribution | \|r\| < 0.15 |
| B-DISTRIBUTED | 2-node independent Flask processes, round-robin, HS256 shared secret | \|r\| < 0.15 |
| B-CONCURRENT | Single-node with 5 concurrent client sessions | \|r\| < 0.15 |
| B-CONFOUND-DISTRIBUTED | Distributed with V2 confound (fixed 'expired' request_id) | \|r\| >= 0.15 |

## 7. Controls

### Positive control
Token validation failure detection on distributed infrastructure with HS256 shared secret: behavioral signal must correctly identify expired vs valid tokens with TP >= 0.85 across all distributed nodes.

### Null control
Structural signal std > 0 across all non-304 conditions on distributed infrastructure: independent ETag generation, Cache-Control headers, and UUID-based dynamic content should produce non-zero structural variation.

## 8. Decision rule

### CONFIRMED if ALL:
- (C1) behavioral detection mean TP >= 0.85 AND mean TN >= 0.85 (AFTER 304 EXCLUSION)
- (C2) >= 2/3 endpoints with non-304 behavioral signal std > 0 AND >= 2/3 with non-304 structural signal std > 0
- (C3) 95% CI upper bound of endpoint-stratified pooled Pearson r (non-304) < 0.15
- (C4) TOST p_upper < 0.05 at delta=0.15 (one-sided, non-304)
- (C5) |r_stratified_enabled - r_stratified_disabled| < 2 * SE_pooled
- (C6) B-LOCAL-ONLY |r| < 0.15
- (C7) B-CONFOUND-DISTRIBUTED endpoint-stratified weighted |r| >= 0.15

### REJECTED if ANY condition fails

### MEASUREMENT_INVALID if infrastructure failure or n_non304 < 400

## 9. Conditions

4 baselines × 42 samples/condition/endpoint × 3 endpoints = 504 total per baseline
Target n_non304 >= 800 (estimated ~84% non-304 rate = ~423 non-304 per baseline)

| Baseline | Conditions | Samples | Non-304 target |
|----------|-----------|---------|----------------|
| B-LOCAL-ONLY | 4 (cache×read/write) × 3 endpoints | 504 | ~423 |
| B-DISTRIBUTED | 4 × 3 endpoints | 504 | ~504 (0% 304 expected) |
| B-CONCURRENT | 4 × 3 endpoints × 5 threads | 504 | ~423 |
| B-CONFOUND-DISTRIBUTED | 4 × 3 endpoints | 504 | ~504 |

## 10. Measurement validity threats

1. **HS256 migration may change cache behavior**: Switching from RS256 to HS256 changes the JWT token format. If the testbed server's token validation logic has RSA-specific paths (e.g., key ID headers), these must be updated. Mitigation: verify B-LOCAL-ONLY passes before distributed run.

2. **Grandparent's RS256 success is unexplained**: The grandparent used identical RS256 code but apparently had working distributed tokens. Root cause of the grandparent's success is not fully understood. The HS256 fix avoids this mystery entirely by using a different mechanism.

3. **Distributed 304 rate**: With independent caches and round-robin routing, 304 cache hits require the same ETag from the same node. With HS256 tokens valid across nodes, the 304 rate may differ from the grandparent's ~16%. This does not affect the primary orthogonality metric (which excludes 304s) but may affect C1 sample composition.

4. **JSON serialization fix may reveal additional NaN/inf values**: The parent's raw_evidence showed NaN in distributed metrics (r NaN, ci NaN). After the fix, these will be persisted as null. This is the correct behavior — null means "not computable due to degenerate input", not "missing".

## 11. Expected outcomes and consequences

| Outcome | Meaning | Product consequence |
|---------|---------|-------------------|
| CONFIRMED (all C1-C7 PASS) | Orthogonality holds on distributed infrastructure | Parallel-channel architecture justified for multi-node deployment |
| REJECTED (any C1-C7 FAIL) | Orthogonality fails on distributed infrastructure | Must investigate cache-coupling; fused classifiers may be needed |
| MEASUREMENT_INVALID | Infrastructure bugs persist or n<400 | Continue debugging; no scientific inference |

## 12. Sample size and power

- **Target**: n_non304 >= 800 per baseline
- **Achieved in grandparent**: n_non304 = 688 (distributed), 684 (local)
- **Achieved in parent**: n_non304 = 844 (local), 860 (concurrent), 1008 (distributed, but degenerate)
- **Power for delta=0.15**: At n=800, CI half-width ~0.067 (from parent local). At n=1200, CI half-width ~0.054. delta=0.10 inference marginal at n=800.
- **Sample composition**: 42 samples/condition/endpoint × 8 conditions × 3 endpoints = 1008 total, estimated ~84% non-304 = ~847 non-304.

## 13. Analysis plan

1. Verify B-LOCAL-ONLY passes (regression check against parent r=0.0233)
2. Verify B-DISTRIBUTED has valid-token 200 responses (RSA fix working)
3. Compute C1 behavioral detection TP/TN with 304 exclusion
4. Compute C2 per-endpoint signal variance
5. Compute C3 endpoint-stratified pooled r with 95% CI
6. Compute C4 TOST equivalence test at delta=0.15
7. Compute C5 cache-mode heterogeneity
8. Compute C6 B-LOCAL-ONLY |r|
9. Compute C7 B-CONFOUND-DISTRIBUTED |r|
10. All C1-C7 PASS → CONFIRMED; any FAIL → REJECTED
