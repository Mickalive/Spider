# EXP-RUNTIME-35237982464 — Report

## Experiment Summary

**Experiment**: EXP-RUNTIME-35237982464
**Lane**: runtime
**Claim**: C-MEAS-VALID
**Status**: COMPLETE
**Outcome**: SUPPORTS

## Question

Does decompression-normalization (SHA256 on decompressed body + status) maintain body-only discrimination >= 0.3 when brotli quality level varies non-deterministically per request — simulating CDN edge-selection non-determinism?

## Hypothesis

Decompression-normalization preserves body-only discrimination under non-deterministic brotli quality because the mechanism operates on decompressed logical bodies, which are quality-invariant. Random quality selection per request produces different compressed bytes but identical decompressed bodies, so decompressed SHA256 hashes remain stable within each auth state. Discrimination should equal the deterministic baseline (0.5).

## Architecture

The experiment uses a two-layer architecture:

1. **Mock OAuth2 Server** (uncompressed): Returns deterministic bodies per auth state without any compression. This isolates the CDN quality variation as the sole source of non-determinism.

2. **CDN Quality Proxy**: Intercepts each request, forwards to the mock server, then re-compresses the response with a randomly selected brotli quality from {4,5,6,7,8} per request. Quality is selected independently per request using a separate RNG (seed=SEED+7919).

## Results

### Primary Metrics (DECOMPRESSED-VARYING-BROTLI, /userinfo endpoint)

| Content Type | Size | Decompressed Discrimination | Compressed Discrimination | B-RANDOM |
|-------------|------|---------------------------|--------------------------|----------|
| JSON | 1KB | **0.5000** | 0.3474 | 0.0000 |
| JSON | 10KB | **0.5000** | 0.3474 | 0.0000 |
| JSON | 100KB | **0.5000** | 0.3474 | 0.0000 |
| HTML | 1KB | **0.5000** | 0.1596 | 0.0000 |
| HTML | 10KB | **0.5000** | 0.1596 | 0.0000 |
| HTML | 100KB | **0.5000** | 0.1596 | 0.0000 |
| XML | 1KB | **0.5000** | 0.3474 | 0.0000 |
| XML | 10KB | **0.5000** | 0.3474 | 0.0000 |
| XML | 100KB | **0.5000** | 0.3474 | 0.0000 |

### Decision Rule Evaluation

All 6 frozen decision-rule conditions PASS:

1. **C1** (JSON decompressed discrimination >= 0.3 at all sizes): **PASS** — 0.5000 >= 0.3 at 1KB, 10KB, 100KB
2. **C2** (HTML decompressed discrimination >= 0.3 at all sizes): **PASS** — 0.5000 >= 0.3 at 1KB, 10KB, 100KB
3. **C3** (XML decompressed discrimination >= 0.3 at all sizes): **PASS** — 0.5000 >= 0.3 at 1KB, 10KB, 100KB
4. **C4** (Decompressed hash variation all_same=true for all state x type x size): **PASS** — 1 unique decompressed hash per state across all 20 repetitions for all 36 conditions
5. **C5** (B-RANDOM = 0.0 for all conditions): **PASS** — 0.0000 across all conditions
6. **C6** (C_QUALITY_VARIATION_EXISTS: >= 2 distinct compressed hashes per type x size): **PASS** — all 5 quality levels {4,5,6,7,8} observed across all conditions

### Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_QUALITY_VARIATION_EXISTS | >= 2 distinct quality levels | 5 quality levels per condition | **PASS** |
| C_NULL_CONTROL | B-RANDOM ~ 0.0 | 0.0000 across all conditions | **PASS** |
| C_DECOMPRESSION_DETERMINISM | all_same=true | all_same=true for all 144 state x type x size cells | **PASS** |
| C_COMPRESSION_ACTIVE | Content-Encoding = br | br on all observations | **PASS** |
| C_NO_PIPELINE_ERRORS | 0 errors | 0 errors | **PASS** |

### Quality Variation Evidence

The CDN proxy successfully varied brotli quality across all conditions:
- All 5 quality levels {4, 5, 6, 7, 8} observed per content type x size
- Quality values distributed uniformly across 20 requests per state
- Compressed hashes vary (2-3 unique per state) due to quality variation
- Decompressed hashes remain identical (1 unique per state) despite quality variation

### Algorithm Comparison (Compressed vs Decompressed)

Compressed-only discrimination is consistently lower than decompressed:
- JSON: 0.347 vs 0.500 (compressed 30% lower)
- HTML: 0.160 vs 0.500 (compressed 68% lower)
- XML: 0.347 vs 0.500 (compressed 30% lower)

This confirms that decompression is necessary for quality-invariance: different quality levels produce different compressed bytes, but the decompressed content is identical.

### Decompression Latency

| Size | Mean | Min | Max |
|------|------|-----|-----|
| 1KB | ~0.02ms | ~0.01ms | ~0.05ms |
| 10KB | ~0.04ms | ~0.02ms | ~0.08ms |
| 100KB | ~0.25ms | ~0.15ms | ~0.45ms |

Latency scales linearly with payload size and remains sub-millisecond for sizes up to 100KB.

## Interpretation

### What This Experiment Shows

1. **Decompression-normalization survives non-deterministic brotli quality variation.** The mechanism operates on decompressed logical bodies, which are quality-invariant. Different quality levels produce different compressed bytes but identical decompressed content, so the SHA256 decompressed hash remains stable.

2. **The discrimination ceiling (0.5) is unchanged from the deterministic baseline.** Non-deterministic quality does not degrade discrimination below the structural ceiling imposed by 3-way error collapse (no_auth/expired/invalid share identical error bodies).

3. **Compressed-only discrimination degrades under quality variation** (0.16-0.35 vs 0.50 decompressed), confirming that decompression is necessary for quality-invariance.

4. **Quality variation is real and observable.** All 5 quality levels appear across all conditions, and compressed hashes show 2-3 unique values per state (vs 1 unique decompressed hash per state).

### Claim Ceiling

This experiment advances the claim ceiling from:
- **Before**: Decompression-normalization survives deterministic localhost compression (parent EXP-RUNTIME-35209111193)
- **After**: Decompression-normalization survives non-deterministic brotli quality variation on localhost

The ceiling is bounded to:
- CDN proxy with uniform random quality selection from {4,5,6,7,8}
- Synthetic padded content (JSON/HTML/XML) at 1KB/10KB/100KB
- 4 auth states with 3-way error collapse
- No Accept-Encoding negotiation (client always requests brotli)
- No chunked transfer-encoding
- No real CDN infrastructure (Cloudflare/Fastly/Akamai)
- N=20 per state per type per size, seed 44

### What This Experiment Does NOT Show

1. **Real CDN survival** — Cloudflare/Fastly/Akamai may introduce additional non-determinism (caching, edge selection, chunked encoding, Accept-Encoding negotiation) not tested here.
2. **Natural content at scale** — Padded content may compress differently than natural content.
3. **Binary content types** — Only JSON/HTML/XML tested.
4. **Production economics** — Latency/CPU measured on localhost, not production infrastructure.

## Consequences

### Positive Outcome (OBSERVED)

Product team can proceed with real-CDN deployment planning knowing that:
- Quality variation alone does not break the mechanism
- The decompressed-body invariant holds regardless of which quality level the CDN edge selects
- The next critical test is real CDN infrastructure survival

### Negative Outcome (NOT OBSERVED)

If the experiment had shown discrimination < 0.3 under quality variation, the product team would need to:
- Force deterministic quality at the CDN edge (increasing infrastructure complexity)
- Investigate quality-specific decompression artifacts
- Consider alternative fingerprinting that handles quality non-determinism

## Validity Threats

1. **Quality proxy not representative**: Uniform random quality selection differs from real CDN edge selection algorithms. Real CDNs may select quality based on content characteristics, client hints, or edge load.
2. **No Accept-Encoding negotiation**: Client always requests brotli. Real CDN behavior depends on client Accept-Encoding.
3. **No chunked transfer-encoding**: Responses use Content-Length. Real CDNs may use chunked encoding.
4. **Synthetic content**: Padded content compresses differently than natural content.
5. **3-way error collapse**: Structural discrimination ceiling of 0.5 is a property of the test environment.
6. **Localhost only**: No network latency, no CDN edge selection, no cache behavior.
