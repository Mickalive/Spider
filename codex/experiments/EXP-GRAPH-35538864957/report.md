# EXP-GRAPH-35538864957 Report

## Summary

**Experiment:** C-FRESHNESS Orthogonality on Distributed Infrastructure
**Lane:** graph
**Claim:** C-FRESHNESS
**Status:** COMPLETE
**Outcome:** FALSIFIES

## Question

Does C-FRESHNESS orthogonality at delta=0.15 survive on distributed production-like infrastructure with multi-node independent caches, concurrent client load (N>=5 parallel sessions), and independent cache invalidation across nodes?

## Decision Rule Results (on B-DISTRIBUTED primary condition)

| Criterion | Threshold | Observed | Pass |
|-----------|-----------|----------|------|
| C1 Behavioral TP >= 0.85 | mean expired TP >= 0.85 AND valid TN >= 0.85 | TP=1.0000, TN=0.6863 | False |
| C2 Variance >= 2/3 | >= 2/3 endpoints have std > 0 | 3/3 | True |
| C3 Equivalence | CI upper < 0.15 | upper=0.0163 | True |
| C4 TOST | p_upper < 0.05 at delta=0.15 | p_upper=0.0000 | True |
| C5 Cache heterogeneity | |r_enabled - r_disabled| < 2*SE | diff=0.0425 | True |
| C6 B-LOCAL-ONLY | |r| < 0.15 | |r|=0.0471 | True |
| C7 B-CONFOUND-DISTRIBUTED | |r| >= 0.15 | |r|=0.8855 | True |

## Primary Metric (B-DISTRIBUTED, endpoint-stratified, non-304)

- **Stratified pooled r = -0.0585** (n = 688)
- 95% CI = [-0.1327, 0.0163]
- TOST delta=0.15: p_upper = 0.0000
- Simple pooled r = -0.0661

## Per-Endpoint Non-304 r (B-DISTRIBUTED)

- /api/user/profile: r=-0.0807, n=208
- /api/data/list: r=-0.0188, n=208
- /api/session/status: r=-0.0719, n=272

## B-LOCAL-ONLY Baseline (C6)

- Stratified pooled r = 0.0471, n = 684
- |r| = 0.0471 < 0.15

## B-CONCURRENT

- Stratified pooled r = -0.0319, n = 816

## B-CONFOUND-DISTRIBUTED (C7)

- Stratified pooled r = -0.8855, n = 816
- |r| = 0.8855 >= 0.15

## TOST at Various Deltas

- delta=0.1: p_upper=0.0000, pass=True
- delta=0.12: p_upper=0.0000, pass=True
- delta=0.15: p_upper=0.0000, pass=True
- delta=0.2: p_upper=0.0000, pass=True

## Interpretation

C-FRESHNESS orthogonality result is FALSIFIES at delta=0.15 on distributed infrastructure.

B-LOCAL-ONLY baseline (|r|=0.0471) confirms no regression from parent.

B-CONFOUND-DISTRIBUTED negative control (|r|=0.8855) confirms V2 confound is genuine in distributed setting.

Endpoint-stratified pooled r on distributed (-0.0585) < 0.15, within equivalence bounds.

## Validity Notes

- V3 endpoint-stratified pooling applied (inherited from parent).
- 304 exclusion applied to ALL correlations (pooled, per-endpoint, per-cache).
- B-DISTRIBUTED uses 2 independent Flask processes with round-robin routing.
- Each distributed node has independent SQLite database, in-memory CDN cache, ETag generation.
- Cache invalidation on node A does NOT propagate to node B.
- B-CONCURRENT uses 5 concurrent client threads with independent request generation.
- B-CONFOUND-DISTRIBUTED uses V2 confound (fixed 'expired' request_id for expired responses).
- V_ETAG permission leakage fix from parent: permission_level from JWT payload.
- V1 UUID fix from parent: uuid.uuid4() for ALL status codes in primary testbed.
- Structural signal extraction: headers-only (ETag, Cache-Control, request_id entropy).
- Production-like testbed: Flask 3.1.3, PyJWT RS256, SQLite WAL-mode.
- n_non304 DISTRIBUTED=688 (target >= 400 for MEASUREMENT_INVALID threshold).
- B-LOCAL-ONLY replication: single-node Flask identical to parent testbed.

## Unresolved

- Whether orthogonality holds on actual production CDN hierarchies with real cache invalidation.
- Whether concurrent client load (N>=50) changes correlation structure (tested at N=5).
- Whether the result generalizes to non-Flask frameworks (Django, FastAPI, Express).
- Whether headers-only structural signal is sufficient for production use.
- Whether per-cache heterogeneity is systematic or sampling noise.
- Whether delta=0.10 becomes achievable at n_non304>=1200.
