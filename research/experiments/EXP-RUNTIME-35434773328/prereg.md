# EXP-RUNTIME-35434773328 Preregistration

## Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35434773328
- **Lane**: runtime
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-RUNTIME-35401995092 (upstream chunked TE gap)
- **Grandparent**: EXP-RUNTIME-35389142338 (auth-aware caching)

## 1. Question

Does iterative decompression survive Transfer-Encoding: chunked on the upstream origin->proxy leg (origin actually serving chunked without Content-Length, proxy reassembling) — fixing the two implementation gaps (origin use_chunked=False, double-header) that bounded the parent's claim ceiling to proxy->client only?

## 2. Hypothesis

The parent (EXP-RUNTIME-35401995092) established that iterative decompression preserves decompressed body-only discrimination at 0.5 through chunked TE on the proxy->client leg (downstream). However, the origin was always started with `use_chunked=False`, so the upstream origin->proxy chunked reassembly path was never tested. The parent's audit identified this as a measurement validity gap (V1, severity medium).

If chunked TE on the upstream leg is transparent to the proxy's reassembly pipeline (proxy reassembles chunked stream into coherent byte stream before forwarding/decompressing), discrimination should remain at 0.5 matching the parent's downstream result. If origin-served chunked causes the proxy to fail reassembly (partial chunks forwarded, chunk boundaries corrupt brotli multi-byte symbols, or proxy fails to strip chunked framing before cache storage), discrimination will drop below 0.3 or decompression errors will appear.

## 3. Falsifier

Decompressed body-only discrimination < 0.3 for any (auth_state, content_type x size) combination under chunked TE in either PASSTHROUGH or AUTH-AWARE CACHED mode when origin serves chunked, OR decompression errors > 0 for any chunked TE condition, OR decompressed hash for any auth state through chunked proxy with origin-served chunked differs from direct-server hash (determinism failure), OR regression: Content-Length PASSTHROUGH discrimination drops below 0.5 (proxy infrastructure change breaks baseline), OR chunked AUTH-AWARE CACHED discrimination < 0.3 for any cell, OR origin verification fails (origin response contains Content-Length header for CHUNKED conditions — confirming chunked is NOT actually served).

## 4. Design

### 4.1 Infrastructure

Same as parent: localhost Flask/stdlib mock OAuth2 origin + Python reverse proxy on separate port.

### 4.2 Configurations

Three proxy configurations tested:

| Config | Origin Framing | Proxy Mode | Cache Key |
|--------|---------------|------------|-----------|
| CL-PASSTHROUGH | Content-Length | PASSTHROUGH | N/A |
| CHUNKED-PASSTHROUGH | Transfer-Encoding: chunked | PASSTHROUGH | N/A |
| CHUNKED-CACHED | Transfer-Encoding: chunked | AUTH-AWARE CACHED | URL+Accept-Encoding+Authorization |

### 4.3 Fixes from Parent

1. **V1 — Origin chunked**: `start_mock_server()` called with `use_chunked=True` for CHUNKED-PASSTHROUGH and CHUNKED-CACHED cells. Origin serves `Transfer-Encoding: chunked` (no `Content-Length` header).

2. **V2 — Double-header**: Proxy cache HIT path for chunked configs sends ONLY `Transfer-Encoding: chunked` (no `Content-Length`), fixing the HTTP/1.1 violation.

3. **V3 — PARENT_REF_HASHES**: Dead code resolved — either removed or asserted byte-for-byte equal to frozen artifact.

### 4.4 Test Matrix

- **Auth states**: no_auth, valid_token, expired_token, invalid_token (4)
- **Content types**: JSON, HTML, XML (3)
- **Sizes**: 1KB, 10KB, 100KB (3)
- **Configs**: CL-PASSTHROUGH, CHUNKED-PASSTHROUGH, CHUNKED-CACHED (3)
- **Reps**: 5 per cell
- **Total**: 4 × 9 × 3 × 5 = 540 requests

### 4.5 Controls

| Control | Expected | Purpose |
|---------|----------|---------|
| B-RANDOM | 0.0 | Null: random SHA256 fingerprints |
| B-PARENT-CL-0.5 | 0.5 | Regression: CL-PASSTHROUGH must match parent |
| B-PARENT-DOWNSTREAM-0.5 | 0.5 | Regression: upstream chunked should not degrade below downstream |
| C_CONTENT_LENGTH_REGRESSION | 0.5 for all CL cells | Positive control: proxy infrastructure unchanged |
| C_NULL_CONTROL | B-RANDOM ~ 0.0 | Null: no spurious structure |
| C_CHUNKED_CACHED_PRIMARY | >= 0.3 for all CACHED cells | Primary: upstream chunked + caching interaction |
| C_ORIGIN_VERIFICATION | Origin serves chunked (no CL header) | Verification: origin actually sends chunked |
| C_DETERMINISM_ACROSS_PATHS | Hash(proxy) == Hash(direct) | Determinism: chunked reassembly preserves content |
| C_NO_ERROR_INFLATION | 0 errors | Stability: no decompression failures |

### 4.6 Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:

1. Decompressed body-only discrimination >= 0.3 for ALL (auth_state, config) combinations under chunked TE
2. Decompressed hash for each (auth_state, content_type, size) through chunked proxy matches direct-server hash
3. B-RANDOM = 0.0 for all conditions
4. C_CONTENT_LENGTH_REGRESSION passes (CL-PASSTHROUGH = 0.5 for all cells)
5. 0 decompression errors across all chunked TE conditions
6. CHUNKED-CACHED discrimination >= 0.3 for all cells
7. ORIGIN_VERIFICATION passes (origin serves chunked, no Content-Length for CHUNKED conditions)

**FALSIFIED-IN-SETTING** if any of:
- Chunked discrimination < 0.3 for any cell
- Hash mismatch (determinism failure)
- Decompression errors > 0 on chunked
- CL-PASSTHROUGH drops below 0.5
- Origin verification fails

**MEASUREMENT_INVALID** if proxy fails to start, origin unreachable, or chunked not applied on both legs.

## 5. Metrics

### Primary
- `decompressed_body_only_discrimination` per cell
- `decompression_errors` per cell
- `determinism_across_paths` (hash match proxy vs direct)

### Secondary
- `compressed_body_only_discrimination` per cell
- `decompression_latency_ms` per cell
- `proxy_overhead_ms` per cell
- `body_sizes` per auth state per cell
- `decompressed_hash_variation` per state per cell

## 6. Product Consequences

### Positive
Iterative decompression survives end-to-end chunked TE (origin->proxy->client) in both passthrough and cached modes. This closes the parent's explicit upstream scope gap and completes the chunked TE story on localhost. Product team can proceed with chunked TE as a supported transport mode. Remaining blocker for C-MEAS-VALID shifts to real CDN infrastructure only.

### Negative
End-to-end chunked TE breaks iterative decompression when origin serves chunked. This identifies a specific upstream reassembly constraint that must be resolved before CDN deployment.

## 7. Expected Information Gain

HIGH. This is the minimum-cost experiment that closes the parent's explicit upstream scope gap before real CDN investment. The parent identified origin chunked as the sole remaining localhost blocker and explicitly excluded it from its claim ceiling. Either outcome is strictly more informative than repeating the parent or jumping to real CDN with an untested upstream path.

## 8. Claim Updates

If SURVIVES_CURRENT_TEST:
- C-MEAS-VALID: advance to EXPERIMENTAL with expanded claim ceiling to include end-to-end chunked TE (origin->proxy->client) on localhost mock infrastructure

If FALSIFIED-IN-SETTING:
- C-MEAS-VALID: remain EXPERIMENTAL with narrowed ceiling to proxy->client chunked downstream only

## 9. Validity Threats

1. **Mock-only**: localhost Python reverse proxy does not replicate real CDN behavior (Accept-Encoding negotiation, edge-specific header manipulation, geographic latency)
2. **Deterministic brotli**: quality 6 deterministic compression means 0.5 discrimination is a mock ceiling, not a production ceiling
3. **3-way error collapse**: no_auth/expired/invalid share identical bodies, limiting discrimination expressiveness
4. **N=5 per cell**: sufficient for deterministic system but no uncertainty quantification for stochastic environments
