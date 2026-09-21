# EXP-GRAPH-35611618323 Report: Distributed C-FRESHNESS Orthogonality (HS256 Fix + JSON Fix + Re-Run)

## Question
After fixing the DistributedManager RSA key sharing bug by switching to HS256 symmetric JWT with shared TESTBED_SECRET, AND fixing numpy.bool_ JSON serialization, does C-FRESHNESS orthogonality at delta=0.15 achieve CONFIRMED status on distributed infrastructure with n_non304>=800?

## Hypothesis
C-FRESHNESS orthogonality at delta=0.15 will be CONFIRMED on distributed multi-node infrastructure after fixing two bugs:
1. HS256 symmetric JWT: eliminates token cross-node invalidation
2. JSON serialization: casts numpy types and handles NaN before json.dump

The parent's MEASUREMENT_INVALID was caused entirely by these two infrastructure bugs.

## Results
- **B-LOCAL-ONLY** (single-node serial): stratified r=0.0584 n=844 CI [-0.0091,0.1254] TOST p_upper=0.0036
- **B-DISTRIBUTED** (2-node round-robin, HS256 shared secret): stratified r=-0.0381 n=844 CI [-0.1053,0.0294] TOST p_upper=2.02e-08
- **B-CONCURRENT** (5 threads): stratified r=-0.0324 n=860 CI [-0.0990,0.0346] TOST p_upper=3.88e-08
- **B-CONFOUND-DISTRIBUTED** (negative control): stratified r=-0.9120 |r|=0.9120 n=844

## Decision Criteria
| Criterion | Threshold | Observed | Pass? |
|-----------|-----------|----------|-------|
| C1 behavioral detection | TP>=0.85 AND TN>=0.85 | TP=1.0000 TN=0.6667 | **FAIL** |
| C2 variance | >=2/3 endpoints std>0 | 3/3 endpoints | PASS |
| C3 CI upper | <0.15 | 0.0294 | PASS |
| C4 TOST p_upper | <0.05 | 2.02e-08 | PASS |
| C5 heterogeneity | |r_en-r_dis|<2*SE | 0.1052<0.1409 | PASS |
| C6 baseline local | |r|<0.15 | 0.0584 | PASS |
| C7 confound | |r|>=0.15 | 0.9120 | PASS |

**Overall: FALSIFIES (all_pass=False) status=COMPLETE**

## C1 Failure Analysis
C1 fails because TN=0.6667 < 0.85, specifically at the `/api/session/status` endpoint where TN=0.0.

**Root cause**: HS256 fix resolved JWT token cross-node validation (tokens created on node A validate on node B), BUT the per-node SQLite session store does NOT replicate sessions across nodes. Round-robin routing sends valid-token requests to node B which lacks the session_id from node A, causing `validate_session()` to return False. This adds behavioral_delta>0 for valid tokens on `/api/session/status`, breaking TN.

This is a genuine distributed infrastructure limitation: session state is per-node while tokens are shared. The behavioral signal for session status reflects session validation state, not just token validity.

The other endpoints (`/api/user/profile`, `/api/data/list`) have TN=1.0 because they don't call `validate_session()` in the response path.

## Interpretation
C-FRESHNESS orthogonality at delta=0.15 is **FALSIFIED** on distributed infrastructure per the frozen decision rule. The primary orthogonality metric (C3, C4) confirms orthogonality (stratified r=-0.0381, CI upper 0.0294<0.15, TOST p_upper=2.02e-08), and the negative control confirms the V2 confound is detectable (C7: r=-0.9120). However, C1 behavioral detection fails because session validation is per-node and doesn't replicate across the distributed testbed.

This is a valid scientific negative result, not an infrastructure failure. The HS256 fix successfully resolved the RSA key sharing bug (tokens valid across nodes), but revealed a secondary distributed infrastructure issue: session state non-replication.

## Product Consequence
C-FRESHNESS orthogonality FAILS on distributed infrastructure even with HS256 shared secret and JSON fix. Parallel-channel architecture is NOT justified for multi-node deployment in its current form. Product must address session state replication or accept that behavioral detection for session status endpoint requires sticky session affinity.

## Validity Notes
- HS256 SYMMETRIC JWT FIX: testbed_server.py and testbed_server_v2.py converted from RS256 per-process RSA keypairs to HS256 with one shared TESTBED_SECRET passed to all child nodes
- JSON SERIALIZATION FIX: NumpyEncoder + recursive sanitize (numpy.bool_ -> bool, numpy integer/float -> native, NaN/inf -> None) applied to all json.dump calls
- STRATIFIED DEGENERATE HANDLING: per-endpoint constant behavioral/structural signals excluded from stratified pooling and flagged, no NaN propagation
- V_ETAG_PERMISSION_LEAKAGE FIX: expired tokens decoded WITHOUT verification to extract permission_level for ETag
- V3 ENDPOINT-STRATIFICATION: pooled Pearson r uses endpoint-stratified weighting
- V1 UUID FOR ALL STATUS CODES: primary testbed uses uuid.uuid4() for all; confound uses fixed 'expired'
- 304 EXCLUSION: 304 responses excluded from pooled, per-endpoint, per-cache correlations
- DISTRIBUTED INDEPENDENCE: Each Flask node has independent SQLite DB, independent in-memory cache, independent ETag generation
- CACHE INDEPENDENCE: Cache invalidation on node A does NOT propagate to node B
- ROUND-ROBIN ROUTING: Distributed testbed routes requests round-robin across nodes
- n per condition: local 844, distributed 844, concurrent 860, confounder 844 (all >=800, target met)
- Structural signal headers-only: ETag change, Cache-Control change, normalized Shannon entropy, dyn_hash_int
- Behavioral signal: token_validation_failure*2 + session_state_change*3 + auth_boundary_shift*1 + status_weight*2

## Raw Evidence
- `raw_evidence/experiment_data.json`
- `raw_evidence/metrics.json`
