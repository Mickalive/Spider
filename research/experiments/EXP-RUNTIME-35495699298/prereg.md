# EXP-RUNTIME-35495699298 — preregistration

**DESIGN FROZEN: NOT YET** (DESIGN stage only)

---

## 1. Background and motivation

The C-MEAS-VALID decompression correctness claim has accumulated 720+480=1200 correctness passes across the parent chain (EXP-RUNTIME-35470447407 → EXP-RUNTIME-35456070671 → EXP-RUNTIME-35481773400). However, all tested payloads are highly-redundant synthetic bodies generated via `'x'*pad` patterns that compress to 70-1059 bytes (max 34 chunks at chunk_size=32). The parent audit (EXP-RUNTIME-35481773400/audit.json, V1_DEGENERATE_PAYLOAD_REDUNDANCY) identified this as the critical limitation: the intended chunk-boundary stress (60-1500+ chunks) was never expressed because the payloads are degenerate.

The parent handoff (EXP-RUNTIME-35481773400/handoff.json) carry_forward unknown list includes: "Does decompression correctness hold for high-entropy non-redundant payloads where 10KB compresses to 2-10KB and 100KB to 20-50KB (60-1500+ chunks at chunk_size=32)?" This is the mandatory remaining gate before CDN infrastructure testing.

## 2. Research question

Does iterative decompression correctness (byte-identical output to ground-truth uncompressed body) hold for high-entropy non-redundant payloads where compressed sizes actually scale to the 2-50KB range and span 60-1500+ chunks at chunk_size=32?

## 3. Hypothesis

Iterative decompression (brotli->gzip->identity, max_depth=5) produces byte-identical output to ground-truth high-entropy generate_*_body(state, target_size) for all 4 auth states, 3 content types, 2 payload sizes, and 4 compression configurations with multi-chunk framing (chunk_size=32), where high-entropy payloads produce compressed sizes in the 2-50KB range and 60-1500+ chunks.

## 4. Test matrix

### 4.1 Independent variables

| Variable | Levels | Count |
|----------|--------|-------|
| Payload size | 10KB (10240), 100KB (102400) | 2 |
| Content type | JSON-high-entropy, HTML-real, Binary-structured | 3 |
| Compression | gzip level 1, gzip level 9, brotli quality 4, brotli quality 8 | 4 |
| Auth state | valid_token, expired_token, invalid_token, no_auth | 4 |
| Repetitions | 5 per cell | 5 |

**Main test observations**: 2 × 3 × 4 × 4 × 5 = **960 observations**

### 4.2 Baselines and controls

| ID | Description | Observations |
|----|-------------|-------------|
| B-GZIP-MC-1KB-REGRESSION | Gzip 1KB synthetic regression (3 content types × 4 states × 5 reps × 1 compression) | 60 |
| B-BROTLI-MC-1KB-REGRESSION | Brotli 1KB synthetic regression (same matrix) | 60 |
| B-IDENTITY-HE-10KB | Identity (no compression) at 10KB high-entropy (3 types × 4 states × 5 reps) | 60 |
| B-IDENTITY-HE-100KB | Identity (no compression) at 100KB high-entropy (3 types × 4 states × 5 reps) | 60 |
| B-COMPRESSED-TARGET-RANGE | Compressed size validation (measured per cell, not separate requests) | — |
| B-RANDOM | Within-state hash determinism check (measured per cell) | — |

**Total observations**: 960 + 240 = **1200**

## 5. High-entropy payload generators

All generators are deterministic given (state, content_type, target_size). Seeds derived from SHA256(f"{state}:{content_type}:{target_size}:he_seed").

### 5.1 JSON-high-entropy (`generate_json_he_body`)

- Top-level object with `state`, `timestamp`, `entries` array
- Each entry contains: `id` (UUID v4 derived from index+seed), `name` (random alphanumeric 8-32 chars), `value` (random float), `description` (random sentence 20-100 chars from seeded word list), `tags` (array of 1-5 random tags)
- Entries added until total body size ≈ target_size
- Byte entropy: expected >4.0 bits/byte due to UUIDs, random floats, varied string lengths

### 5.2 HTML-real (`generate_html_he_body`)

- Fetch a real Wikipedia article HTML (seeded selection from list of 10 articles) once at experiment start, cache in memory
- Wrap in minimal HTML structure with auth-state-dependent content sections
- Each auth state gets unique visible content (state name embedded in heading, paragraph content varies)
- Pad with additional real-sourced content (paragraphs from cached article) to reach target_size
- Byte entropy: expected >3.5 bits/byte from real HTML with diverse tags, attributes, and text content

### 5.3 Binary-structured (`generate_binary_he_body`)

- Custom binary format: 16-byte magic header, 4-byte version, 4-byte state marker, 4-byte entry count
- Each entry: 8-byte key (random), 4-byte length, N bytes random payload (seeded)
- Random payload sections use `os.urandom` with fixed seed override for determinism
- Checksum block at end (CRC32 of all preceding bytes)
- Byte entropy: expected >5.0 bits/byte from random payload sections

### 5.4 Entropy validation

Shannon entropy computed on each generated body: H = -Σ p(b) log2(p(b)) for byte values 0-255. Minimum acceptable: 3.5 bits/byte. Bodies below threshold trigger MEASUREMENT_INVALID.

## 6. Server architecture

Reuse parent's `run_experiment.py` architecture (EXP-RUNTIME-35481773400) with these changes:

1. **MockOAuthHandler**: Replace `generate_*_body` calls with `generate_*_he_body` (high-entropy variants)
2. **ReverseProxyHandler**: No changes (buffered proxy with chunked transfer-encoding)
3. **New endpoint**: `/health` for payload entropy validation pre-flight check
4. **Same ports**: mock on 8700, proxy on 8800 (or next available)

## 7. Correctness oracle

For each request:
1. Compute `expected_hash = SHA256(generate_*_he_body(state, target_size))`
2. Compute `actual_hash = SHA256(decompress_body(raw_response))`
3. `correctness_pass = (expected_hash == actual_hash)`
4. `silent_fallback = (SHA256(decompressed) == SHA256(raw_compressed))` — classified as failure

## 8. Decision rule (frozen)

**SURVIVES_CURRENT_TEST** requires ALL of:
- **C1**: `correctness_match_rate == 1.0` for ALL high-entropy cells (960 observations)
- **C2**: `silent_fallback_count == 0` for ALL high-entropy cells
- **C3**: B-GZIP-MC-1KB-REGRESSION and B-BROTLI-MC-1KB-REGRESSION pass 100% (no pipeline regression)
- **C4**: null_control passes (all_same=true for all states in all high-entropy cells)
- **C5**: B-COMPRESSED-TARGET-RANGE passes (at least 2/3 content types achieve mean compressed_size_bytes ≥ 2000 at 10KB AND ≥ 5000 at 100KB)

**FALSIFIED** if any correctness failure OR any silent fallback in any high-entropy cell.

**MEASUREMENT_INVALID** if:
- Infrastructure prevents data collection
- Correctness oracle baseline (B-IDENTITY-HE) fails
- B-COMPRESSED-TARGET-RANGE fails (payloads remain degenerate, chunk-boundary stress not expressed)
- Shannon entropy of any content type falls below 3.5 bits/byte

## 9. Metrics (stable identities for downstream transmission)

| Metric ID | Description | Unit |
|-----------|-------------|------|
| M-CORRECTNESS-RATE | Fraction of correctness_pass across all observations | ratio [0,1] |
| M-CORRECTNESS-PER-CELL | Per-cell correctness_match_rate | ratio [0,1] |
| M-SILENT-FALLBACK-COUNT | Total silent fallbacks across all compressed observations | count |
| M-COMPRESSED-SIZE-MEAN | Per-cell mean compressed_size_bytes | bytes |
| M-COMPRESSED-SIZE-MIN | Per-cell min compressed_size_bytes | bytes |
| M-COMPRESSED-SIZE-MAX | Per-cell max compressed_size_bytes | bytes |
| M-CHUNK-COUNT-MEAN | Per-cell mean compressed_size_bytes / chunk_size (32) | count |
| M-CHUNK-COUNT-MAX | Per-cell max chunk count | count |
| M-DECOMPRESSION-LATENCY-MEAN | Per-cell mean decompression latency | ms |
| M-DECOMPRESSION-LATENCY-P99 | Per-cell 99th percentile decompression latency | ms |
| M-ENTROPY-SHANNON | Per-content-type Shannon entropy of generated body | bits/byte |
| M-TARGET-RANGE-PASS | B-COMPRESSED-TARGET-RANGE pass/fail | boolean |
| M-REGRESSION-PASS | Combined regression control pass/fail | boolean |

## 10. Validity threats

| ID | Threat | Mitigation |
|----|--------|------------|
| T1 | High-entropy payloads may not reach target compressed size range | B-COMPRESSED-TARGET-RANGE control with explicit threshold; MEASUREMENT_INVALID if failed |
| T2 | Wikipedia HTML fetch may be unavailable or rate-limited | Cache at startup; fall back to alternative source (BBC News, sample HTML); MEASUREMENT_INVALID if all sources fail |
| T3 | Buffered proxy still masks streaming chunk-boundary failures | Acknowledged; this experiment tests chunk-boundary behavior at transport level, not incremental parsing (parent V2) |
| T4 | Single-layer encoding only (max_depth 1) | Acknowledged; multi-layer is separate unknown from parent V3 |
| T5 | Decompression correctness is near-tautological with stdlib | Acknowledged; discriminative power comes from chunk-boundary stress at scale, not library correctness |
| T6 | chunk_size=32 is small; real CDNs may use 8KB chunks | chunk_size=32 is the established test configuration; real CDN chunking is part of the next gate |

## 11. Scope NOT tested (explicit)

- Multi-layer stacked Content-Encoding (gzip->br, br->gzip) — separate experiment
- Streaming incremental decompression across chunk boundaries without full reassembly — requires architecture change
- Real CDN infrastructure (Cloudflare/Fastly/Akamai) with Accept-Encoding negotiation, cache/Vary, production concurrency — next gate after this
- gzip levels 2-8 and brotli qualities 5-7 — extremes chosen for maximum structural difference
- Binary content types beyond the custom structured format
- Production OAuth/OIDC with real token validation
- Decompression latency at 20-50KB compressed sizes on real network (localhost latency is negligible)

## 12. Expected information gain

A positive result (SURVIVES_CURRENT_TEST) validates the decompression pipeline at realistic compressed sizes (2-50KB, 60-1500+ chunks) and advances C-MEAS-VALID claim ceiling to high-entropy payloads on localhost. The remaining gate narrows to real CDN infrastructure.

A negative result (FALSIFIED or MEASUREMENT_INVALID) reveals a critical failure mode masked by the parent's degenerate payloads. If correctness fails, the specific failure mode (chunk-boundary corruption, buffer overflow, dictionary reference spanning) requires diagnosis before product scope can be defined. If payloads remain degenerate (MEASUREMENT_INVALID on B-COMPRESSED-TARGET-RANGE), the payload generation strategy requires redesign before the chunk-boundary hypothesis can be tested.

Either outcome is highly decision-relevant: it either advances the claim ceiling or reveals a blocking failure mode. No neutral outcome exists.

## 13. Consequences

**If positive**: C-MEAS-VALID advances toward Product Core. The next experiment can target real CDN infrastructure with confidence that the localhost decompression pipeline handles realistic payload sizes. Estimated 1-2 experiments from Product Core readiness.

**If negative**: C-MEAS-VALID claim ceiling remains bounded to synthetic payloads. Product cannot handle realistic web content without diagnosis. The decompression implementation requires investigation, potentially involving architecture changes (streaming decompression, chunk-boundary-aware parsing). Estimated 2-4 experiments to diagnose and fix.
