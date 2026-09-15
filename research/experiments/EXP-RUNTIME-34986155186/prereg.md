# EXP-RUNTIME-34986155186 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34986155186
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-15
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does decompression-normalization (hashing the DECOMPRESSED response body after reversing Content-Encoding) preserve body-only discrimination under varying brotli quality levels, and does it provide a universal fallback when compressed-byte hashing fails?

## 3. Motivation

Prior Runtime work established:
- EXP-RUNTIME-34902094115: Body-only discrimination (SHA256 on compressed bytes) = 0.5 under deterministic brotli quality 6 and gzip level 9 mtime=0, for JSON at 1KB, 10KB, 100KB
- EXP-RUNTIME-34654566605: Body-only discrimination degrades under fully non-deterministic compression (random bytes per request)
- Cross-client pooling degrades to 0.2237 (different algorithms produce different compressed bytes)
- Status-only discrimination is compression-immune at 0.5

The parent handoff (EXP-RUNTIME-34902094115) recommends real-CDN validation as the next step, but that requires external infrastructure (Cloudflare/Fastly/Akamai account). The minimum unblocked path toward production deployment is to test decompression-normalization as a universal fallback.

**Key insight**: If we hash the DECOMPRESSED body (normalizing via Content-Encoding), the hash should be invariant to compression quality because different logical bodies decompress to different bytes regardless of how they were compressed. This eliminates the dependency on compression stability.

**What this changes**: If decompression-normalization works, the product recommendation changes from "body-only with stable Accept-Encoding" to "use decompression-normalization as universal fallback", enabling deployment behind real CDNs where quality levels may vary.

## 4. Hypotheses

### H1: Decompression-Normalization Preserves Discrimination
Decompression-normalization achieves discrimination >= 0.5 on /userinfo under fixed brotli quality 6, because different logical bodies decompress to different bytes regardless of compression algorithm.

### H2: Quality Variation Degrades Compressed-Byte Hashing
Body-only discrimination on compressed bytes degrades under brotli quality variation (quality 4-8 per request) but remains above 0.0 because quality variation is bounded (not full random).

### H3: Decompression-Normalization Outperforms Compressed-Byte Hashing Under Quality Variation
Decompression-normalization achieves higher discrimination than compressed-byte hashing under quality variation.

### H4: Within-State Determinism Under Decompression
Decompression-normalization produces deterministic hashes (within-state variation = 0) because brotli.decompress() is a deterministic function for a given compressed input.

## 5. Experimental Design

### 5.1 Server Infrastructure

Same mock OAuth2 server as parent (EXP-RUNTIME-34902094115):
- Mock OAuth2 server on port 5000
- CDN proxy on port 5001
- 4 auth states: no_auth (401), valid_token (200), expired_token (401), invalid_token (401)
- Error bodies identical across no_auth/expired/invalid (capping discrimination ceiling at 0.5)
- Valid_token body: JSON with field "data" = hex(random bytes) at ~1KB uncompressed

### 5.2 Conditions

**5 conditions x 4 states x 20 reps x 2 endpoints = 800 total requests**

| Condition | Compression | Fingerprint | Description |
|-----------|-------------|-------------|-------------|
| COMPRESSED-FIXED | brotli quality=6 (fixed) | SHA256(status, compressed_body_sha256, '') | Replicates parent baseline |
| COMPRESSED-VARYING | brotli quality ∈ {4,5,6,7,8} (random per request) | SHA256(status, compressed_body_sha256, '') | Tests quality variation |
| DECOMPRESSED-FIXED | brotli quality=6 (fixed) | SHA256(status, decompressed_body_sha256, '') | Normalization under fixed quality |
| DECOMPRESSED-VARYING | brotli quality ∈ {4,5,6,7,8} (random per request) | SHA256(status, decompressed_body_sha256, '') | Normalization under quality variation |
| IDENTITY | no compression | SHA256(status, body_sha256, '') | Identity baseline |

### 5.3 Quality Variation Mechanism

For COMPRESSED-VARYING and DECOMPRESSED-VARYING conditions:
- Quality level randomly selected from {4, 5, 6, 7, 8} for each request
- Selection uses `random.randint(4, 8)` with frozen seed=44
- Brotli quality 4 = fast compression (lower ratio), quality 8 = slow compression (higher ratio)
- Range chosen to represent realistic CDN quality variation under load

### 5.4 Decompression Procedure

For DECOMPRESSED-FIXED and DECOMPRESSED-VARYING conditions:
1. Receive compressed response with Content-Encoding: br
2. Remove Content-Encoding header from fingerprint
3. Decompress body via `brotli.decompress(compressed_body)`
4. Compute SHA256 of decompressed body
5. Fingerprint = SHA256(repr((status, decompressed_body_sha256, '')))

### 5.5 Sample Size

- 20 requests per state per condition per endpoint
- 4 states x 5 conditions x 20 reps x 2 endpoints = 800 total
- Seed=44 for reproducibility
- Jitter 50-150ms uniform between requests

## 6. Measures

### 6.1 Primary Metric
- **discrimination**: Fraction of correctly distinguishable state pairs from fingerprint, computed as (number of distinguishable pairs) / (total possible pairs) for each condition on /userinfo and /introspect

### 6.2 Secondary Metrics
- **within_state_variation**: Number of unique fingerprints per state per condition (expected: 1 for deterministic)
- **compressed_body_hash_variation**: Number of unique compressed hashes per state under quality variation
- **decompressed_body_hash_variation**: Number of unique decompressed hashes per state under quality variation
- **cross_condition_divergence**: Whether compressed and decompressed fingerprints diverge for the same request
- **body_sizes**: Min/max/mean decompressed body size per state

### 6.3 Baselines
- **B-COMPRESSED-FIXED**: body-only discrimination at fixed quality 6 (expected 0.5)
- **B-COMPRESSED-VARYING**: body-only discrimination under quality variation (expected < 0.5 but > 0.0)
- **B-DECOMPRESSED-FIXED**: decompression-normalization at fixed quality 6 (expected >= 0.5)
- **B-DECOMPRESSED-VARYING**: decompression-normalization under quality variation (expected >= 0.5)
- **B-STATUS-ONLY**: status code discrimination (expected 0.5 on /userinfo, 0.0 on /introspect)
- **B-RANDOM**: random fingerprint (expected 0.0)

## 7. Controls

### 7.1 Positive Control (B-COMPRESSED-FIXED)
- Body-only discrimination at fixed brotli quality 6 must achieve >= 0.35 on /userinfo
- This replicates parent EXP-RUNTIME-34902094115 and verifies the harness

### 7.2 Null Control (B-RANDOM)
- Random fingerprint discrimination must be ~ 0.0 at all conditions
- This verifies no spurious structure from compression artifacts

### 7.3 Decompression Determinism Control
- Within-state variation for DECOMPRESSED-FIXED must be 0 (all 20 requests produce same hash)
- This verifies brotli.decompress() is deterministic for the same input

### 7.4 Quality Variation Control
- Within-state variation for COMPRESSED-VARYING must be > 0 (quality variation produces different compressed hashes)
- This verifies quality variation is actually occurring

## 8. Validity Threats

### 8.1 Brotli Quality Range
The quality range {4-8} may not represent real CDN behavior. Real CDNs may use quality 0-11 or vary by response size. Mitigation: range chosen to be realistic for production CDN behavior under load.

### 8.2 Decompression Latency
Decompression adds latency (~1ms for 1KB). This is not measured in this experiment but is a product concern. Mitigation: latency measurement is out of scope; this experiment tests discrimination only.

### 8.3 Mock Server Limitations
Mock OAuth2 server returns identical error bodies for no_auth/expired/invalid, capping discrimination at 0.5. This matches parent and is a known ceiling. Mitigation: discrimination ceiling is structural, not a measurement gap.

### 8.4 Sample Size
20 reps per cell may be insufficient for stable discrimination estimation. Mitigation: parent used 10 reps and achieved stable results; 20 reps provides 2x margin.

### 8.5 Seed Dependency
Single seed=44 may produce unrepresentative quality variation patterns. Mitigation: seed is frozen for reproducibility; variation is uniform random across quality levels.

## 9. Decision Rules

### 9.1 SURVIVES_CURRENT_TEST
If ALL of:
1. B-COMPRESSED-FIXED >= 0.35 on /userinfo (positive control passes)
2. B-RANDOM ~ 0.0 at all conditions (null control passes)
3. B-DECOMPRESSED-FIXED >= 0.5 on /userinfo (decompression-normalization preserves discrimination under fixed quality)
4. No pipeline errors

### 9.2 MIXED
If B-DECOMPRESSED-FIXED >= 0.5 BUT B-COMPRESSED-VARYING < 0.35 on /userinfo
(body-only fails under quality variation but normalization works — product recommendation changes to normalization)

### 9.3 FALSIFIED-IN-SETTING
If B-DECOMPRESSED-FIXED < 0.35 on /userinfo
(decompression-normalization fails under fixed quality — normalization is not a viable fallback)

### 9.4 MEASUREMENT_INVALID
If pipeline errors prevent computation, OR sample size < 20 per cell, OR within-state variation > 0 for DECOMPRESSED-FIXED (decompression non-deterministic)

## 10. Expected Outcomes

### 10.1 Positive Result (SURVIVES_CURRENT_TEST)
- Decompression-normalization preserves discrimination at 0.5 under fixed quality
- Product recommendation: "use decompression-normalization as universal fallback"
- Enables deployment behind real CDNs without requiring compression stability
- Next step: test normalization under real CDN conditions

### 10.2 Mixed Result (MIXED)
- Body-only fails under quality variation but normalization works
- Product recommendation: "use decompression-normalization, body-only is not sufficient"
- Stronger case for normalization as mandatory fallback
- Next step: test normalization latency and failure modes

### 10.3 Negative Result (FALSIFIED-IN-SETTING)
- Decompression-normalization fails under fixed quality
- Body-only on compressed bytes remains the only viable approach
- Deployment constrained to deterministic compression environments
- Next step: investigate why normalization fails (decompression non-determinism? hash collision?)

### 10.4 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging
- Not scientific evidence for or against
- Next step: fix pipeline and re-run

## 11. Analysis Plan

1. **Data Collection**: 800 requests across 5 conditions x 4 states x 2 endpoints x 20 reps
2. **Fingerprint Computation**: For each request, compute both compressed and decompressed fingerprints
3. **Discrimination Calculation**: For each condition on each endpoint, compute fraction of distinguishable state pairs
4. **Within-State Variation**: Count unique fingerprints per state per condition
5. **Baseline Comparison**: Compare all baselines against expected values
6. **Control Checks**: Verify positive, null, decompression determinism, and quality variation controls
7. **Decision Rule Application**: Apply frozen decision rules to determine verdict
8. **Reporting**: Report all outcomes with equal prominence

## 12. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 13. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
