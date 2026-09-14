# EXP-RUNTIME-34902094115 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34902094115
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-14
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does body-only HTTP fingerprint discrimination survive deterministic CDN compression when response body sizes increase from 0-729 bytes to KB-scale JSON (1KB, 10KB, 100KB), where higher entropy may cause non-deterministic compression output or hash instability?

## 3. Motivation

Prior work established:
- EXP-RUNTIME-34741873198: Body-only discrimination at 0.5 under deterministic CDN simulation with small bodies (0-729 bytes)
- Within-state compressed body hash variation 0/10 across all cells, confirming code-level determinism of gzip (mtime=0 level 9) and brotli (quality 6)
- Cross-client pooled discrimination drops to 0.2237 from 0.5 single-client, confirming different Accept-Encoding produces different compressed bytes
- Parent handoff question: "Does body-only discrimination survive at larger body sizes (KB-scale JSON) where compression entropy increases and may cause non-deterministic output or hash instability beyond the 0-729 byte Keycloak responses tested here?"

The critical gap: all prior experiments used tiny Keycloak responses (0-729 bytes). Compression behavior changes with body size:
1. Larger JSON responses have higher entropy
2. Higher entropy may trigger different compression levels or chunking
3. Non-deterministic output may emerge at KB-scale under real CDN conditions

This experiment tests exactly this scenario. If body-only discrimination survives KB-scale JSON, the substrate ceiling extends to realistic API response sizes. If it fails at larger sizes, architecture change is forced.

## 4. Hypotheses

### H1: Deterministic Compression Preserves Discrimination at KB-Scale
When a client with stable Accept-Encoding sees deterministic brotli or gzip compression from the CDN, body-only discrimination on /userinfo must be within 0.15 of identity (uncompressed) discrimination for all three body sizes (1KB, 10KB, 100KB). This confirms deterministic compression produces deterministic compressed output for the same logical body regardless of size.

### H2: Within-State Hash Stability at KB-Scale
Under deterministic brotli and deterministic gzip, within-state body hash variation must be 0 across 10 repetitions for all three body sizes. This confirms the compression library produces identical compressed bytes for the same logical body and Accept-Encoding regardless of entropy.

### H3: Cross-Client Hash Divergence at KB-Scale
When two different clients with different Accept-Encoding headers (e.g., "br, gzip" vs "identity") see different compression algorithms from the CDN, body-only discrimination must be degraded compared to identity for all body sizes. This confirms that body hash divergence across clients is a real phenomenon at KB-scale.

### H4: Status-Only Invariance at KB-Scale
Status-only discrimination must be 0.5 on /userinfo invariant across all client profiles and all body sizes. This confirms status codes are unaffected by compression and body size.

## 5. Experimental Setup

### 5.1 Infrastructure

- Mock OAuth2 server on localhost:5000 returning JSON responses with field "data" containing random bytes of length size
- Python HTTPServer proxy on localhost:5001 forwarding to mock server
- No real IdP required; mock server simulates auth states via query parameter

### 5.2 Body Sizes

Three body sizes representing realistic API response sizes:
- **1KB**: Small API response (e.g., user profile)
- **10KB**: Medium API response (e.g., search results)
- **100KB**: Large API response (e.g., bulk data export)

Each body size uses different random seeds per auth state to ensure distinct bodies.

### 5.3 Client Profiles

Three client profiles simulating different Accept-Encoding configurations:

- **Client A**: `Accept-Encoding: br, gzip` → CDN selects brotli (highest priority)
- **Client B**: `Accept-Encoding: gzip` → CDN selects gzip (only option)
- **Client C**: `Accept-Encoding: identity` → CDN selects identity (no compression)

For B-MIXED-CLIENT: Client A and Client C alternate requests to test cross-client hash divergence.

### 5.4 CDN Negotiation Logic

Proxy reads the client's Accept-Encoding header and selects the first supported algorithm in order: br > gzip > identity. The selection is deterministic — same Accept-Encoding always produces the same algorithm. This simulates real CDN behavior where the CDN picks one algorithm per client.

### 5.5 Endpoints

- `/userinfo` (GET) — resource server endpoint
- `/introspect` (POST) — token introspection endpoint

### 5.6 Auth States

- `no_auth`: No Authorization header → 401 login_required (empty body)
- `valid_token`: Valid access token → 200 JSON body with random data
- `expired_token`: Expired token → 401 JSON error body
- `invalid_token`: Invalid token → 401 JSON error body (identical to expired_token)

### 5.7 Sample Size

- 4 auth states × 10 reps × 3 client profiles × 2 endpoints × 3 body sizes = 720 total requests
- 20 requests per client profile per endpoint per body size (4 states × 10 reps)
- 10 per state per cell

### 5.8 Randomization

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
- **M_DETERMINISTIC_DISCRIMINATION**: Body-only discrimination under deterministic brotli and deterministic gzip on /userinfo for each body size

### 6.4 Secondary Metrics
- Within-state body hash variation (unique hashes per state per client profile per body size)
- Body sizes per state per client profile (to verify compression produces different sizes)
- Cross-client body hash divergence (same state, different clients, different hashes?) per body size
- Status-only discrimination across all conditions
- Compression ratio per body size per algorithm

## 7. Controls

### 7.1 Positive Control (Identity)
- Body-only discrimination >= 0.35 on /userinfo with no compression for all body sizes
- Verifies baseline measurement pipeline works at KB-scale

### 7.2 Positive Control (Deterministic Compression)
- Body-only discrimination >= identity - 0.15 on /userinfo with deterministic brotli and gzip for all body sizes
- Verifies deterministic compression preserves body hash stability at KB-scale

### 7.3 Null Control (Random)
- B-RANDOM discrimination ~ 0.0 at all client profiles and body sizes
- Verifies no spurious structure from compression artifacts

### 7.4 Cross-Client Control
- Body-only discrimination with mixed clients (A and C alternating) must be < identity for all body sizes
- Verifies different Accept-Encoding → different compressed bytes → hash divergence at KB-scale

### 7.5 Status-Only Control
- Status-only discrimination = 0.5 on /userinfo invariant across all client profiles and body sizes
- Verifies status codes are compression-immune and size-immune

## 8. Decision Rules

### 8.1 SURVIVES_CURRENT_TEST
If ALL of:
1. B-IDENTITY-BODY-ONLY >= 0.35 on /userinfo for all body sizes (positive control)
2. B-RANDOM ~ 0.0 at all client profiles and body sizes (null control)
3. B-DETERMINISTIC-BR-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo for all body sizes
4. B-DETERMINISTIC-GZIP-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo for all body sizes
5. Within-state body hash variation = 0 for deterministic brotli and gzip at all body sizes
6. B-MIXED-CLIENT-BODY-ONLY < B-IDENTITY-BODY-ONLY on /userinfo for all body sizes
7. B-STATUS-ONLY >= 0.5 on /userinfo invariant across all conditions
8. No pipeline errors

### 8.2 FALSIFIED-IN-SETTING
If (3) or (4) fails (deterministic compression degrades body-only at KB-scale).

### 8.3 MEASUREMENT_INVALID
If (5) fails (deterministic compression produces non-deterministic output at KB-scale), or (1), (2), or (8) fails.

## 9. Validity Threats

### 9.1 Mock Server vs Real IdP
The mock server simulates auth states but does not run real Keycloak. Real Keycloak responses may have different structure, headers, or compression behavior. This experiment tests the compression substrate, not IdP-specific behavior. Findings apply to deterministic compression of JSON responses, not necessarily to all Keycloak endpoints.

### 9.2 Synthetic CDN Simulation
The proxy simulates CDN behavior but is not a real CDN. Real CDNs may have additional non-determinism (load-balancing, caching layers, server-side variation). This experiment tests the minimum viable CDN model (deterministic algorithm selection per Accept-Encoding). Findings apply to this model, not necessarily to all real CDN implementations.

### 9.3 Brotli Availability
If brotli Python module is unavailable, fallback to gzip-only. Document this limitation. The brotli test is the strongest test of deterministic compression; gzip-only weakens the experiment.

### 9.4 Sample Size
10 reps per state per cell may be insufficient for detecting small non-determinism. Report within-state variation explicitly.

### 9.5 Body Size Range
Only three body sizes tested (1KB, 10KB, 100KB). Results may not generalize to larger sizes (MB-scale) or different content types (binary, XML, etc.).

### 9.6 Expired Token Construction
expired_token is identical to invalid_token by construction (both return same error JSON). This limits discrimination ceiling to 0.5 regardless of body size. This is intentional: the experiment tests compression determinism, not auth state discrimination.

## 10. Analysis Plan

1. **Collect observations**: 720 HTTP requests across 3 body sizes × 3 client profiles × 2 endpoints × 4 states × 10 reps
2. **Compute fingerprints**: Body-only (status + compressed body hash) for each request
3. **Compute discrimination**: Intra-match rate minus inter-match rate for each body size × client profile × endpoint
4. **Compute within-state variation**: Unique body hashes per state per client profile per body size
5. **Compute cross-client divergence**: For each state and body size, check if Client A and Client C produce different body hashes
6. **Apply decision rules**: Check all 8 conditions for SURVIVES_CURRENT_TEST
7. **Report**: All outcomes with equal prominence, including negative and invalid results

## 11. Pre-registered Expectations

From prior work:
- Body-only discrimination at 0.5 for small bodies (0-729 bytes) under deterministic compression
- Within-state variation 0/10 confirming determinism
- Cross-client discrimination degraded due to different compression algorithms

Expectations for KB-scale:
- Within-state variation should remain 0 (deterministic compression)
- Discrimination should remain 0.5 (distinct bodies produce distinct fingerprints)
- Cross-client discrimination should remain degraded (different algorithms produce different bytes)

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 13. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.