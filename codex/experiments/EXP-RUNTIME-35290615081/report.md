# EXP-RUNTIME-35290615081 — Execution Report

## Experiment Summary

**Question**: Does iterative decompression restore decompressed body-only discrimination >= 0.3 and decompressed hash determinism (all_same=true) under triple-brotli encoding for the valid_token success body when triple-br is guaranteed to be observed via stratified scenario assignment?

**Outcome**: **SUPPORTS** — All 7 frozen decision-rule conditions pass. Valid_token triple-br is now observed and passes.

**Status**: COMPLETE

## What This Experiment Does

This is a minimal targeted fix for the measurement defect identified by audit V1 in the parent experiment (EXP-RUNTIME-35280364816). The parent established that iterative decompression (brotli→gzip→identity loop, max_depth=5) handles double-brotli for all auth states and triple-brotli for error states, but never observed triple-br for valid_token (0/180 reps across all 9 conditions) due to a systematic RNG shift from the shared proxy connectivity test.

**The fix**: Replace random scenario assignment with deterministic round-robin (`scenario = ENCODING_SCENARIOS[request_index % 6]`), passed to the CDN proxy via `X-Requested-Scenario` header. The proxy connectivity test uses a separate RNG that does not consume from the measured-request sequence.

## Key Results

### Stratified Coverage (NEW — Fixes Audit V1)

| Condition | State | Scenarios Observed | Triple-BR? |
|-----------|-------|-------------------|------------|
| JSON 1KB | valid_token | 6/6 | ✅ |
| JSON 10KB | valid_token | 6/6 | ✅ |
| JSON 100KB | valid_token | 6/6 | ✅ |
| HTML 1KB | valid_token | 6/6 | ✅ |
| HTML 10KB | valid_token | 6/6 | ✅ |
| HTML 100KB | valid_token | 6/6 | ✅ |
| XML 1KB | valid_token | 6/6 | ✅ |
| XML 10KB | valid_token | 6/6 | ✅ |
| XML 100KB | valid_token | 6/6 | ✅ |

All 4 auth states observe all 6 encoding scenarios in every condition (9/9 conditions × 4 states = 36/36 pass).

### Decompressed Discrimination

All 9 conditions achieve `decompressed_body_only_discrimination = 0.5` (threshold: ≥ 0.3). This includes valid_token under triple-br.

### Decompressed Hash Determinism

All 4 auth states across all 9 conditions: `unique_count = 1`, `all_same = true`. Triple-br decompressed hashes match single-layer hashes for valid_token.

### Controls

| Control | Status |
|---------|--------|
| C_STRATIFIED_COVERAGE | ✅ PASS |
| C_NULL_CONTROL (B-RANDOM = 0.0) | ✅ PASS |
| C_DECOMPRESSION_DETERMINISM | ✅ PASS |
| C_GRACEFUL_DEGRADATION (0 errors) | ✅ PASS |
| C_NO_PIPELINE_ERRORS | ✅ PASS |
| C_TRIPLE_BR_DECOMPRESSIBLE | ✅ PASS |
| C_ENCODING_VARIATION_EXISTS | ✅ PASS |

### Baselines

| Baseline | Expected | Observed | Status |
|----------|----------|----------|--------|
| B-RANDOM | ~0.0 | 0.0 | ✅ PASS |
| B-COMPRESSED-BYTE-ONLY | <0.5 | 0.278 | ✅ PASS |
| B-SINGLE-PASS-0.2911 | exceeded | 0.5 | ✅ EXCEEDS |
| B-NO-DOUBLE-BR-0.4486 | exceeded | 0.5 | ✅ EXCEEDS |

### Decompression Latency

| Condition | Mean | Min | Max |
|-----------|------|-----|-----|
| JSON 1KB | 0.010ms | 0.007ms | 0.030ms |
| JSON 10KB | 0.022ms | 0.019ms | 0.091ms |
| JSON 100KB | 0.149ms | 0.135ms | 0.213ms |
| HTML 1KB | 0.009ms | 0.007ms | 0.026ms |
| HTML 10KB | 0.017ms | 0.012ms | 0.104ms |
| HTML 100KB | 0.073ms | 0.065ms | 0.113ms |
| XML 1KB | 0.010ms | 0.007ms | 0.029ms |
| XML 10KB | 0.014ms | 0.012ms | 0.022ms |
| XML 100KB | 0.072ms | 0.065ms | 0.113ms |

Zero decompression errors across all 720 requests.

## Interpretation

### The Fix Works

The stratified round-robin assignment resolves the parent's measurement defect: valid_token now observes triple_br in all 9 conditions (was 0/180 in parent, now 36/36 conditions × state = guaranteed). The round-robin `index % 6` ensures each scenario appears 13-14 times per 80-request condition, with no RNG dependency on the proxy connectivity test.

### Triple-Brotli for Success Body Confirmed

With valid_token now experiencing triple-br, we observe:
- **Discrimination = 0.5** (same as all other passing state/scenario combinations)
- **Determinism = all_same = true** (decompressed hash for valid_token triple-br matches single-layer hash)
- **Zero decompression errors** (iterative depth-5 handles triple wrapping for the success body)

This confirms the parent's mechanistic prediction: iterative decompression is state-agnostic — it iterates brotli→gzip→identity regardless of body content. If it works for error bodies (which are structurally similar), it works for the success body too.

### Claim Ceiling Advancement

The parent's claim ceiling was bounded to "double-brotli for all states + triple-brotli for error states only." This experiment closes that gap.

**New claim ceiling**: Iterative decompression (brotli→gzip→identity looping to max_depth=5) restores decompression-normalization under multi-layer encoding including triple-brotli for ALL auth states (no_auth, valid_token, expired_token, invalid_token) on localhost mock server with deterministic brotli quality 6. Discrimination 0.5 ≥ 0.3, hash determinism all_same=true, for JSON/HTML/XML × 1KB/10KB/100KB.

**Bounded to**: localhost CDNEncodingProxy, synthetic padded bodies, 4 states with 3-way error collapse (structural ceiling 0.5), N=20 per state per condition (720 total), brotli 1.2.0, iterative depth 5, stratified round-robin scenario assignment.

**NOT validated**: real CDN infrastructure (Cloudflare/Fastly/Akamai), caching/chunked/HTTP2/Accept-Encoding negotiation, natural content, binary types, production latency at scale, decompression bombs, maximum practical depth beyond 5.

### Product Consequence

**Positive**: Product team can deploy iterative decompression with confidence that triple-encoded CDN responses (up to 3 brotli layers) do not break any auth state, including the distinct success response that separates authenticated from error responses.

**Negative**: Triple-brotli for success body now confirmed — no negative outcome observed. Product should still restrict CDN configurations defensively if the maximum real-world encoding depth could exceed 3 layers.

## Decision Rule Evaluation

Per frozen `spec.json` decision rule, ALL conditions pass:

1. ✅ valid_token × triple_br has ≥1 observation per condition (stratified coverage passes — 13-14 per condition)
2. ✅ decompressed body-only discrimination ≥ 0.3 for valid_token × triple_br at all content types × sizes (= 0.5)
3. ✅ decompressed hash variation all_same=true for valid_token × triple_br
4. ✅ decompressed body-only discrimination ≥ 0.3 for ALL (state, scenario) combinations (= 0.5 everywhere)
5. ✅ all_same=true for all conditions
6. ✅ B-RANDOM = 0.0 for all conditions
7. ✅ C_STRATIFIED_COVERAGE passes

**Result**: SURVIVES_CURRENT_TEST

## Validity Threats

1. **Localhost ceiling**: Same as parent — bounded to localhost mock server, not real CDN infrastructure.
2. **Synthetic content**: Bodies are padded to target size; natural content (HTML with JS, CSS, images) may have different compression characteristics.
3. **Structural ceiling 0.5**: The 3-way error collapse means discrimination cannot exceed 0.5 on this testbed regardless of decompression quality.
4. **Stratified round-robin is deterministic**: While this fixes the coverage defect, it removes randomization of scenario ordering. This is acceptable because the purpose is scenario coverage, not random sampling.
5. **N=20 per state per condition**: Adequate for the binary pass/fail question but not for effect-size estimation.

## Unresolved Questions

- Does iterative decompression survive real CDN infrastructure?
- What is production-scale latency at N>1000 with MB-scale natural content?
- What is the maximum practical decompression depth for real-world multi-layer encoding?
- Does iterative decompression introduce false positives on genuinely non-compressed data?
- How does iterative decompression interact with decompression bombs?
