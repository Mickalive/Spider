# EXP-RUNTIME-35237982464 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35237982464
- **Lane**: runtime
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-RUNTIME-35209111193 (SURVIVES_CURRENT_TEST — decompression-normalization generalizes to multi-format multi-size under localhost brotli/gzip compression)
- **Created**: 2026-09-17

## 2. Research Question

Does decompression-normalization (SHA256 on decompressed body + status) maintain body-only discrimination >= 0.3 when brotli quality level varies non-deterministically per request — simulating CDN edge-selection non-determinism where the same logical body is served through different quality levels across requests?

## 3. Hypothesis

**H1 (Primary)**: Decompression-normalization preserves body-only discrimination under non-deterministic brotli quality because the mechanism operates on decompressed logical bodies, which are quality-invariant. Random quality selection per request produces different compressed bytes but identical decompressed bodies, so decompressed SHA256 hashes remain stable within each auth state. Discrimination should equal the deterministic baseline (0.5).

**H2 (Mechanism)**: Compressed-byte-only discrimination (without decompression) degrades under non-deterministic quality because compressed bytes vary with quality level. This proves decompression is necessary for quality-invariance.

**H3 (Regression)**: Decompression-normalization discrimination under non-deterministic quality equals deterministic-quality discrimination (diff < 0.05) for all content types x sizes.

## 4. Inherited State from Parent

### Established (do not re-test)
- Decompression-normalization preserves body-only discrimination >= 0.3 for JSON, HTML, XML at 1KB/10KB/100KB under localhost brotli (quality 4-8) and gzip compression without CDN noise.
- Algorithm equivalence confirmed: |brotli_decompressed - gzip_decompressed| = 0.0 for all 18 type×size pairs.
- Determinism confirmed: decompressed hash variation all_same=true for all 288 state×type×size×baseline cells.
- Compressed-only brotli discrimination is lower (0.15-0.34) proving decompression is necessary for format-invariance.
- Structural discrimination ceiling is 0.5 due to 3-way error collapse in mock server design.

### Rejected
- Brotli quality diversity does not increase from 1KB to 100KB for repetitive padded content (artifact of padding, not mechanism limitation).
- Decompression-normalization was NOT tested on real CDN infrastructure.

### Unknown (this experiment addresses)
- Does decompression-normalization survive non-deterministic brotli quality variation?
- Does brotli quality diversity increase with natural content at larger sizes?

### Do NOT assume
- Do NOT assume decompression-normalization is production-ready — real CDN infrastructure is untested.
- Do NOT assume the structural discrimination ceiling of 0.5 applies to production environments.
- Do NOT assume non-deterministic quality is equivalent to real CDN behavior — real CDNs also vary caching, chunked encoding, and Accept-Encoding.

## 5. Experimental Design

### 5.1 Infrastructure

- **Mock OAuth2 server**: Same as parent EXP-RUNTIME-35209111193 — 4 auth states (no_auth, valid_token, expired_token, invalid_token), 3-way error collapse.
- **CDN quality proxy**: New layer between client and server that intercepts responses and re-compresses with randomly selected brotli quality {4,5,6,7,8} per request. Quality is selected independently per request (uniform random). The proxy decompresses the server's response and re-compresses with the selected quality.
- **Client**: Python requests library, same as parent. Applies SHA256 decompression-normalization to response body after decoding.

### 5.2 Content Types

Same 3 as parent:
- JSON: application/json (key-value pairs)
- HTML: text/html (paragraphs, lists, links)
- XML: application/xml (nested elements with attributes)

### 5.3 Payload Sizes

Same 3 as parent:
- 1KB (1024 bytes)
- 10KB (10240 bytes)
- 100KB (102400 bytes)

### 5.4 Auth States

Same 4 as parent:
- no_auth (no Authorization header)
- valid_token (valid Bearer JWT)
- expired_token (expired Bearer JWT)
- invalid_token (random string Bearer)

### 5.5 Quality Variation

- CDN proxy selects brotli quality uniformly at random from {4,5,6,7,8} per request.
- Quality is independent of auth state, content type, and payload size.
- N=20 requests per state per content type per size = 720 total requests.
- Seed=44 for request ordering. Quality selection uses a separate RNG seed to ensure independence from request ordering.

### 5.6 Fingerprinting

**Decompressed body-only** (primary):
```
SHA256(status_code || decompressed_body)
```

**Compressed byte-only** (exploratory):
```
SHA256(status_code || compressed_body)
```

### 5.7 Metrics

- **M_DISCRIMINATION**: Jaccard distance between {hash(state_i)} and {hash(state_j)} for all state pairs, per content type x size.
- **M_DETERMINISM**: Within-state decompressed hash uniqueness (all_same=true/false).
- **M_QUALITY_VARIATION**: Number of distinct compressed hashes per state (should be >= 2 if quality varies).
- **M_DECOMPRESSED_STABILITY**: Decompressed hash identical across quality levels for same state (boolean per state).
- **M_COMPRESSED_DISCRIMINATION**: Discrimination using compressed bytes (exploratory).

## 6. Decision Rules

### 6.1 Primary

SURVIVES_CURRENT_TEST if ALL of:
1. Decompressed body-only discrimination >= 0.3 for JSON at all sizes
2. Decompressed body-only discrimination >= 0.3 for HTML at all sizes
3. Decompressed body-only discrimination >= 0.3 for XML at all sizes
4. Decompressed hash variation all_same=true for all content types x sizes x states
5. B-RANDOM = 0.0 for all conditions
6. C_QUALITY_VARIATION_EXISTS passes (at least 2 distinct compressed hashes per content type x size)

### 6.2 Falsification

FALSIFIED-IN-SETTING if:
- Any content type has decompressed discrimination < 0.3 at any size
- Decompressed hashes differ by brotli quality level for any state
- Decompressed hash variation > 1 unique per state

### 6.3 Measurement Invalid

MEASUREMENT_INVALID if:
- Infrastructure failure prevents valid measurements (server doesn't compress, proxy doesn't vary quality, decompression path not exercised)
- Quality variation is degenerate (all requests get same quality despite random selection)

## 7. Controls

| Control | ID | Expected | Purpose |
|---------|-----|----------|---------|
| Positive | C_QUALITY_VARIATION_EXISTS | >= 2 distinct compressed hashes per type x size | Verifies quality proxy actually varies |
| Null | C_NULL_CONTROL | B-RANDOM ~ 0.0 | Random fingerprints produce no structure |
| Regression | B-DETERMINISTIC-QUALITY-6 | 0.5 | Parent's deterministic baseline |
| Mechanism | B-COMPRESSED-BYTE-ONLY | < 0.5 | Proves decompression is necessary |

## 8. Validity Threats

1. **Quality proxy not representative**: The proxy randomly selects quality, but real CDNs may select quality based on content characteristics, client hints, or edge load. This experiment tests quality non-determinism generally, not specific CDN selection algorithms.
2. **No Accept-Encoding negotiation**: The client always advertises 'br'. Real CDN behavior depends on client Accept-Encoding. This is excluded to isolate quality effects.
3. **No chunked transfer-encoding**: Responses use Content-Length. Real CDNs may use chunked encoding. This is excluded to isolate quality effects.
4. **Synthetic content**: Content is padded, not natural. Quality-dependent compression differences may be larger for natural content. This is bounded to padded content.
5. **3-way error collapse**: The mock server has no_auth/expired/invalid sharing similar bodies, capping discrimination at 0.5. This is a property of the test environment, not the mechanism.
6. **Localhost only**: No network latency, no CDN edge selection, no cache behavior. Results are bounded to localhost with quality randomization.

## 9. Scope Boundaries

This experiment tests ONE specific CDN non-determinism: brotli quality level variation. It does NOT test:
- Real CDN infrastructure (Cloudflare/Fastly/Akamai)
- Accept-Encoding negotiation (algorithm selection)
- Chunked transfer-encoding
- Cache-Control / ETag / conditional requests
- Content-Encoding header corruption or absence
- Binary content types
- Natural (non-padded) content at scale
- Concurrent clients
- MB-scale payloads

The claim ceiling is bounded to: localhost mock OAuth2 server with CDN-proxy brotli quality randomization from {4,5,6,7,8}, synthetic padded content (JSON/HTML/XML), 4 auth states with 3-way error collapse, N=20 per state per type per size, seed 44, Python 3.12.14, brotli 1.2.0.
