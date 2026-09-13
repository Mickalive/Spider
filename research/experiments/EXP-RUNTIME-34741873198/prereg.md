# EXP-RUNTIME-34741873198 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34741873198
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-13
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does body-only HTTP fingerprint discrimination survive realistic CDN negotiation where Content-Encoding is selected deterministically from the client's advertised Accept-Encoding (not per-request random), and would a client with stable Accept-Encoding see deterministic compressed hashes?

## 3. Motivation

Prior work established:
- EXP-RUNTIME-34509593940: Body-only discrimination invariant under synthetic header noise (tautological by construction — proxy preserved bodies)
- EXP-RUNTIME-34654566605: Body-only discrimination degrades under synthetic per-request random compression (Spearman rho -0.948, p=0.051, n=4)
- EXP-RUNTIME-34654566605 audit V5: Ceiling bounded to synthetic random model — real CDN compression is negotiated deterministically via client Accept-Encoding, not per-request random

The critical gap: the parent tested worst-case non-determinism (random algorithm per request) that is NOT observed in real CDN behavior. In production:
1. Client sends `Accept-Encoding: br, gzip` (stable across requests)
2. CDN selects one algorithm (usually the most efficient one the client supports) and applies it consistently
3. The same client with the same Accept-Encoding sees the same compressed bytes for the same logical body

This experiment tests exactly this scenario. If body-only discrimination survives deterministic CDN negotiation, the body-only architecture is viable for production CDN. If it fails even with deterministic negotiation, CDN compression is a fundamental threat regardless of negotiation model.

## 4. Hypotheses

### H1: Deterministic Compression Preserves Discrimination
When a client with stable Accept-Encoding sees deterministic brotli or gzip compression from the CDN, body-only discrimination on /userinfo must be within 0.15 of identity (uncompressed) discrimination. This confirms deterministic compression produces deterministic compressed output for the same logical body.

### H2: Within-State Hash Stability
Under deterministic brotli and deterministic gzip, within-state body hash variation must be 0 across 10 repetitions. This confirms the CDN simulation produces identical compressed bytes for the same logical body and Accept-Encoding.

### H3: Cross-Client Hash Divergence
When two different clients with different Accept-Encoding headers (e.g., "br, gzip" vs "identity") see different compression algorithms from the CDN, body-only discrimination must be degraded compared to identity. This confirms that body hash divergence across clients is a real phenomenon.

### H4: Status-Only Invariance
Status-only discrimination must be 0.5 on /userinfo invariant across all client profiles. This confirms status codes are unaffected by compression negotiation.

## 5. Experimental Setup

### 5.1 Infrastructure

- Keycloak 25.0 start-dev via Docker on localhost:18080
- Python HTTPServer proxy on localhost:18081 forwarding to Keycloak
- Same Docker image and configuration as parent experiments

### 5.2 Client Profiles

Three client profiles simulating different Accept-Encoding configurations:

- **Client A**: `Accept-Encoding: br, gzip` → CDN selects brotli (highest priority)
- **Client B**: `Accept-Encoding: gzip` → CDN selects gzip (only option)
- **Client C**: `Accept-Encoding: identity` → CDN selects identity (no compression)

For B-MIXED-CLIENT: Client A and Client C alternate requests to test cross-client hash divergence.

### 5.3 CDN Negotiation Logic

Proxy reads the client's Accept-Encoding header and selects the first supported algorithm in order: br > gzip > identity. The selection is deterministic — same Accept-Encoding always produces the same algorithm. This simulates real CDN behavior where the CDN picks one algorithm per client.

### 5.4 Endpoints

- `/userinfo` (GET) — resource server endpoint
- `/introspect` (POST) — token introspection endpoint

### 5.5 Auth States

- `no_auth`: No Authorization header → 401 login_required
- `valid_token`: Valid access token → 200 alice_profile
- `expired_token`: Expired token → 401 auth_failed
- `invalid_token`: Invalid token → 401 auth_failed

### 5.6 Sample Size

- 4 auth states × 10 reps × 3 client profiles × 2 endpoints = 240 total requests
- 20 requests per client profile per endpoint (4 states × 10 reps)
- 10 per state per cell

### 5.7 Randomization

- Seed=44 for request ordering (deterministic across runs)
- Jitter: 50-150ms uniform between requests

## 6. Measures

### 6.1 Body-Only Fingerprint
```
fingerprint = SHA-256(repr((status, body_sha256, '')))
```
Where `body_sha256` is computed on compressed wire bytes (not decompressed bytes).

### 6.2 Discrimination Score
```
discrimination = intra_match_rate - inter_match_rate
```
Where:
- intra_match_rate = fraction of same-state pairs with identical fingerprints
- inter_match_rate = fraction of different-state pairs with identical fingerprints

### 6.3 Primary Metric
- **M_DETERMINISTIC_DISCRIMINATION**: Body-only discrimination under deterministic brotli and deterministic gzip on /userinfo

### 6.4 Secondary Metrics
- Within-state body hash variation (unique hashes per state per client profile)
- Body sizes per state per client profile (to verify compression produces different sizes)
- Cross-client body hash divergence (same state, different clients, different hashes?)
- Status-only discrimination across all conditions

## 7. Controls

### 7.1 Positive Control (Identity)
- Body-only discrimination >= 0.35 on /userinfo with no compression
- Verifies baseline measurement pipeline works

### 7.2 Positive Control (Deterministic Compression)
- Body-only discrimination >= identity - 0.15 on /userinfo with deterministic brotli and gzip
- Verifies deterministic compression preserves body hash stability

### 7.3 Null Control (Random)
- B-RANDOM discrimination ~ 0.0 at all client profiles
- Verifies no spurious structure from compression artifacts

### 7.4 Cross-Client Control
- Body-only discrimination with mixed clients (A and C alternating) must be < identity
- Verifies different Accept-Encoding → different compressed bytes → hash divergence

### 7.5 Status-Only Control
- Status-only discrimination = 0.5 on /userinfo invariant across all client profiles
- Verifies status codes are compression-immune

## 8. Decision Rules

### 8.1 SURVIVES_CURRENT_TEST
If ALL of:
1. B-IDENTITY-BODY-ONLY >= 0.35 on /userinfo (positive control)
2. B-RANDOM ~ 0.0 at all client profiles (null control)
3. B-DETERMINISTIC-BR-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo
4. B-DETERMINISTIC-GZIP-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo
5. Within-state body hash variation = 0 for deterministic brotli and gzip
6. B-MIXED-CLIENT-BODY-ONLY < B-IDENTITY-BODY-ONLY on /userinfo
7. B-STATUS-ONLY >= 0.5 on /userinfo invariant
8. No pipeline errors

### 8.2 FALSIFIED-IN-SETTING
If (3) or (4) fails (deterministic compression degrades body-only).

### 8.3 MEASUREMENT_INVALID
If (5) fails (deterministic compression produces non-deterministic output), or (1), (2), or (8) fails.

## 9. Validity Threats

### 9.1 Synthetic CDN Simulation
The proxy simulates CDN behavior but is not a real CDN. Real CDNs may have additional non-determinism (load-balancing, caching layers, server-side variation). This experiment tests the minimum viable CDN model (deterministic algorithm selection per Accept-Encoding). Findings apply to this model, not necessarily to all real CDN implementations.

### 9.2 Small Body Sizes
Keycloak /userinfo returns 0-189 bytes, /introspect returns 16-729 bytes. Gzip/brotli compression effects are larger for larger bodies. Results may not generalize to endpoints returning kilobytes of JSON.

### 9.3 Single IdP
Only Keycloak 25.0 start-dev is tested. Production Keycloak with real CDN, load-balancer, or rate-limiting may behave differently.

### 9.4 Expired Token Construction
expired_token is locally-signed HS256, not Keycloak-issued. This is orthogonal to the compression question (body for expired vs invalid is identical) but limits claim ceiling.

### 9.5 Sample Size
10 reps per state per cell may be insufficient for detecting small non-determinism. Report within-state variation explicitly.

### 9.6 Brotli Availability
If brotli Python module is unavailable, fallback to gzip-only. Document this limitation. The brotli test is the strongest test of deterministic compression; gzip-only weakens the experiment.

## 10. Analysis Plan

1. **Collect observations**: 240 HTTP requests across 3 client profiles × 2 endpoints × 4 states × 10 reps
2. **Compute fingerprints**: Body-only (status + compressed body hash) for each request
3. **Compute discrimination**: Intra-match rate minus inter-match rate for each client profile × endpoint
4. **Compute within-state variation**: Unique body hashes per state per client profile
5. **Compute cross-client divergence**: For each state, check if Client A and Client C produce different body hashes
6. **Apply decision rules**: Check all 8 conditions for SURVIVES_CURRENT_TEST
7. **Report**: All outcomes with equal prominence, including negative and invalid results
