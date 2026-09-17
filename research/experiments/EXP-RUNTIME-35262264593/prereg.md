# Preregistration: EXP-RUNTIME-35262264593

## Inherited state (from EXP-RUNTIME-35237982464 handoff)

### Established
- Decompression-normalization (SHA256 on decompressed body + status) preserves body-only discrimination at 0.5 under uniform random brotli quality variation {4,5,6,7,8} on localhost.
- Algorithm equivalence (brotli vs gzip) confirmed: |brotli_decompressed - gzip_decompressed| = 0.0 for all 18 type x size pairs.
- Determinism under quality variation confirmed: decompressed hash variation all_same=true for all 36 content-type x size x state cells.
- Compressed-only brotli discrimination is lower than decompressed (0.16-0.35 vs 0.50), confirming decompression is necessary.
- Structural discrimination ceiling is 0.5 due to 3-way error collapse in mock server design.

### Rejected
- Brotli quality diversity does not increase from 1KB to 100KB for repetitive padded content (artifact of padding).
- Decompression-normalization was NOT tested on real CDN infrastructure.
- The experiment's information gain is bounded by construction (lossless compression guarantees).

### Unknown
- Does decompression-normalization survive real CDN infrastructure (Cloudflare/Fastly/Akamai)?
- Does decompression-normalization handle incorrect, missing, or double-encoded Content-Encoding headers gracefully?

### Do Not Assume
- Do NOT assume decompression-normalization is production-ready — real CDN infrastructure is untested.
- Do NOT assume the structural discrimination ceiling of 0.5 applies to production environments.
- Do NOT assume non-deterministic quality is equivalent to real CDN behavior.

## Design

### Question
Does decompression-normalization (SHA256 on decompressed body + status) maintain body-only discrimination >= 0.3 under CDN-like encoding-layer non-determinism — incorrect, missing, double-encoded, and garbled Content-Encoding headers — in addition to the previously established brotli quality variation?

### Hypothesis
Decompression-normalization preserves body-only discrimination under encoding-layer non-determinism because the mechanism operates on decompressed logical bodies. CDN-like header corruption (incorrect algorithm label, missing Content-Encoding, double encoding, garbled value) is a header-layer artifact that does not alter the decompressed logical body when the client attempts standard decompression or falls back to identity. Discrimination should equal the quality-only baseline (0.5) because encoding non-determinism affects only the header/compressed representation, not the decompressed content, provided at least one decompression path succeeds. When ALL decompression paths fail (garbled/empty headers), the mechanism gracefully degrades to the raw body hash, which may still carry auth-state discrimination.

### Falsifier
Decompressed body-only discrimination < 0.3 for any content type at any size, OR decompressed hash variation > 1 unique per state for any condition (determinism failure under encoding non-determinism), OR decompressed hashes for double-encoded responses differ from single-encoded hashes for the same auth state and content type (decomposition-order sensitivity), OR a garbled Content-Encoding header causes a client crash/hang rather than a decompression error (missing graceful degradation).

### Baselines
| ID | Description | Expected |
|----|-------------|----------|
| B-QUALITY-ONLY-0.5 | Parent quality-only baseline | 0.5 |
| B-RANDOM | SHA256 on random 32-byte fingerprints | ~0.0 |
| B-COMPRESSED-BYTE-ONLY | Discrimination using compressed bytes directly (no decompression) | < 0.5 |
| B-IDENTITY-FALLBACK | When decompression fails, use raw (compressed) body hash | >= 0.3 |

### Positive control
C_ENCODING_VARIATION_EXISTS: For each content type x size, at least 3 distinct Content-Encoding scenarios must produce distinct response headers. Verifies encoding variation is present.

### Null control
C_NULL_CONTROL: B-RANDOM ~ 0.0 for all conditions.

### Content types and sizes
- Types: JSON (key-value), HTML (paragraphs/lists/links), XML (nested elements)
- Sizes: 1KB, 10KB, 100KB (controlled by padding)
- Auth states: 4 (valid_token, no_auth, expired_token, invalid_token) with 3-way error collapse

### Encoding scenarios (5)
1. **Correct 'br'** — standard brotli, quality 6
2. **Missing Content-Encoding** — no header, identity transfer
3. **Incorrect 'gzip' label** — brotli-compressed bytes served with `Content-Encoding: gzip`
4. **Double-encoded 'br, br'** — brotli-compressed bytes wrapped in another brotli layer
5. **Garbled 'br; quality=invalid'** — malformed Content-Encoding value

### Execution
- Mock server generates brotli-compressed responses at quality 6 (deterministic baseline quality).
- CDN proxy layer applies random encoding scenario per request.
- Client attempts: (a) standard brotli decompression, (b) gzip decompression fallback, (c) identity (no decompression) on error.
- SHA256 decompression-normalization applied to decompressed body.
- Seed=44, N=20 per state per type per size.

### Decision rule
SURVIVES_CURRENT_TEST if ALL of:
1. Decompressed body-only discrimination >= 0.3 for JSON at all sizes
2. Decompressed body-only discrimination >= 0.3 for HTML at all sizes
3. Decompressed body-only discrimination >= 0.3 for XML at all sizes
4. Decompressed hash variation all_same=true for all content types x sizes x states
5. B-RANDOM = 0.0 for all conditions
6. C_ENCODING_VARIATION_EXISTS passes

FALSIFIED-IN-SETTING if any non-JSON type has discrimination < 0.3 at any size, OR decompressed hashes differ by encoding scenario for any condition, OR double-encoded produces different decompressed hashes than single-encoded.

MEASUREMENT_INVALID if infrastructure failure prevents valid measurements.

### Product consequences
- **Positive**: Claim ceiling advances to "quality + encoding-layer non-determinism". Real-CDN deployment proceeds for encoding corruption scenarios.
- **Negative**: Mechanism depends on correct Content-Encoding headers. Real-CDN deployment blocked until failure mode understood.

### Validity threats
1. **Lossy decompression**: Some encoding combinations (e.g., double br) may produce partial/garbled output rather than clean fallback. The graceful degradation path is tested explicitly.
2. **Repetitive padding**: Content padding compresses identically across sizes (known artifact from parent). Quality diversity may be lower than with natural content.
3. **No real CDN**: Results bounded to localhost mock server. Real CDN introduces caching, chunked transfer-encoding, HTTP/2 framing, and edge selection not tested here.
4. **Error body collapse**: no_auth/expired/invalid share identical error bodies, limiting discrimination to 0.5 maximum. This is a property of the test environment, not the mechanism.
5. **Client library behavior**: brotli/gzip library may handle garbled headers differently than production HTTP clients. Results bounded to Python brotli 1.2.0 library behavior.

### Scope boundaries
- This experiment tests encoding-layer non-determinism only. It does not test real CDN infrastructure (Cloudflare/Fastly/Akamai).
- This experiment does not test chunked transfer-encoding, HTTP/2 framing, response caching, or edge selection.
- This experiment does not test natural (non-padded) content at production scale.
- This experiment does not test binary content types.
