# EXP-RUNTIME-35330741639 — Execution Report

## 1. Experiment Summary

**Question**: Does iterative decompression survive CDN-like proxy behaviors — specifically Accept-Encoding negotiation, response caching, and Transfer-Encoding: chunked — that real CDN infrastructure applies between origin and client?

**Outcome**: FALSIFIES — The frozen decision rule triggers FALSIFIED-IN-SETTING because the CACHED proxy behavior has decompressed body-only discrimination = 0.0 across all 9 content-type × size conditions (threshold ≥ 0.3). However, the falsification is NOT about iterative decompression failing — it is about CDN caching behavior destroying auth-dependent response variation.

## 2. Key Findings

### 2.1 PASSTHROUGH: SURVIVES (discrimination = 0.5)

All 9 PASSTHROUGH cells achieve decompressed body-only discrimination = 0.5, matching the parent (EXP-RUNTIME-35290615081) exactly. No regression. Iterative decompression introduces no artifacts when a proxy is present but does not modify responses.

- All decompressed hashes all_same=True within each state
- All decompressed hashes match parent's direct-server hashes (determinism across paths)
- B-RANDOM = 0.0 for all cells
- 0 decompression errors

### 2.2 RECOMPRESS: SURVIVES (discrimination = 0.5)

All 9 RECOMPRESS cells achieve decompressed body-only discrimination = 0.5. The proxy decompresses the origin's brotli response and re-compresses with its own brotli quality 8 (adding one compression layer). Iterative decompression (max_depth=5) handles this correctly — the additional layer is well within the depth budget.

- All decompressed hashes all_same=True within each state
- 0 decompression errors
- This confirms that re-compression at a different quality does not break decompression-normalization

### 2.3 CACHED: FALSIFIES (discrimination = 0.0)

All 9 CACHED cells have decompressed body-only discrimination = 0.0 — **every auth state receives the same decompressed body**. This is NOT a measurement failure or infrastructure artifact. It is a **real and expected CDN behavior**.

**Root cause**: The cache key is `(URL, Accept-Encoding)`, which does NOT include the `Authorization` header. The first request's response (for whichever auth state happens to go first in the shuffled plan) gets cached. All subsequent requests receive the same cached response, regardless of their auth token. This destroys the auth-dependent response variation that discrimination measures.

**CDN realism**: This is exactly how most CDN caches work by default. Cloudflare, Fastly, and Akamai all cache by URL + Accept-Encoding unless specifically configured with `Cache-Control: private` or `Vary: Authorization`.

**Implication**: A CDN with default caching configuration will serve stale/wrong auth-state responses to all clients after the first cache fill. This is a real deployment hazard for auth-dependent content.

### 2.4 Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_NULL_CONTROL | B-RANDOM ~ 0.0 | All 0.0 | YES |
| C_PROXY_PASSTHROUGH_EQUIVALENCE | Passthrough disc = 0.5 | Mean 0.5 | YES |
| C_DECOMPRESSED_DISCRIMINATION | All cells ≥ 0.3 | Min 0.0 (CACHED) | **NO** |
| C_DECOMPRESSED_DETERMINISM | all_same=true | All true | YES |
| C_DETERMINISM_ACROSS_PATHS | Hashes match parent | All match | YES |
| C_NO_ERROR_INFLATION | 0 errors | 0 errors | YES |
| C_SINGLE_LAYER_NO_REGRESSION | Passthrough ≥ 0.3 | All 0.5 | YES |
| C_COMPRESSED_BASELINE | ~0.2781 ref | 0.5 mean (passthrough) | YES (info) |

## 3. Decision Rule Evaluation

Frozen decision rule: **SURVIVES_CURRENT_TEST** if ALL of:
1. decompressed body-only discrimination ≥ 0.3 for ALL (auth_state, proxy_behavior) — **FAIL** (CACHED = 0.0)
2. decompressed hash matches parent's direct hash — PASS
3. B-RANDOM = 0.0 — PASS
4. C_PROXY_PASSTHROUGH_EQUIVALENCE — PASS
5. No decompression crashes/hangs — PASS
6. Regression: all 4 states ≥ 0.3 under passthrough — PASS

**Result**: FALSIFIED-IN-SETTING — condition 1 fails because CACHED has discrimination = 0.0.

## 4. Scientific Interpretation

The falsification is bounded and actionable:

1. **Iterative decompression itself survives all three proxy behaviors** — no errors, no crashes, correct decompression in PASSTHROUGH and RECOMPRESS modes.

2. **CDN caching with (URL, Accept-Encoding) cache key destroys auth-dependent content differentiation** — this is a real CDN behavior, not an artifact. The cache doesn't include the Authorization header in its key.

3. **Product implication**: For auth-dependent content served through a CDN, the origin MUST set `Cache-Control: private` or `Vary: Authorization` to prevent the CDN from caching one auth state's response and serving it to all clients. This is a specific, testable CDN configuration constraint.

4. **The parent's localhost direct-server discrimination of 0.5 is preserved through passthrough and re-compression proxies** — confirming that the decompression-normalization mechanism is format-invariant to proxy-added compression layers.

## 5. Limitations

- This experiment tests locally-simulated CDN behaviors only. Real CDN infrastructure (Cloudflare/Fastly/Akamai) remains untested.
- The cache key (URL, Accept-Encoding) represents a specific CDN configuration — production CDNs may use different default cache keys.
- The RECOMPRESS mode adds exactly one brotli layer — real CDNs may vary compression quality per edge node.
- Transfer-Encoding: chunked is always applied as a constant background condition — chunked TE does not vary across conditions.
- N=5 reps per cell is sufficient for discrimination measurement but low for latency statistics.
