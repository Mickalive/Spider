# EXP-RUNTIME-35542474231 — Encoding-Agnostic CDN Decompression

## Executive Summary

**Outcome: SUPPORTS** — Encoding-agnostic iterative decompression restores byte-identical correctness through Cloudflare CDN for ALL tested conditions. The CDN decompression gate closes.

### Key Results
- **C1 (Primary gate):** 240/240 encoding-agnostic correct across all 48 CDN cells (3 payload × 2 orders × 2 chunk sizes × 4 Accept-Encoding variants)
- **C2 (BINARY):** 80/80 encoding-agnostic correct on BINARY CDN cells (parent forensic gap closed)
- **C3 (Cache stability):** 6/6 groups have identical decompressed output across consecutive requests
- **C4 (Identity):** 15/15 encoding-agnostic correct on uncompressed CDN payloads
- **C5 (Depth generalization):** 45/45 (100%) encoding-agnostic correct on depths 3-5 (threshold ≥80%)
- **C6 (Large payload):** 30/30 (100%) encoding-agnostic correct on >100KB payloads (threshold ≥80%)
- **Positive control:** 240/240 localhost correct
- **Null control:** 15/15 identity correct

## 1. Question

Does encoding-agnostic iterative decompression (sniff delivered bytes, iteratively try brotli→gzip→identity until SHA256 matches ground truth) restore byte-identical correctness through Cloudflare CDN for all 48 payload×order×chunk×Accept-Encoding conditions — and does it generalize to depths 3-5 and payloads >100KB?

## 2. Hypothesis

An encoding-agnostic decoder that sniffs delivered bytes and iteratively attempts brotli→gzip→identity decompression until SHA256 matches ground truth restores byte-identical correctness through Cloudflare CDN for all tested conditions.

**Mechanism:** CDN re-encoding is lossless (parent forensic confirmed). The failure in the parent was the fixed-origin-order assumption (replaying the origin's layer stack against wire bytes after CDN has transformed them). Encoding-agnostic decode removes this assumption by treating delivered bytes as opaque and iteratively trying all decompression paths until SHA256 matches.

## 3. Results

### 3.1 Primary Matrix (C1): 240/240 ✓

All 48 cells pass 5/5 under encoding-agnostic decode:

| Payload | Order | Chunk | AE=none | AE=gzip | AE=br | AE=both |
|---------|-------|-------|---------|---------|-------|---------|
| JSON | GZIP-OUTER | 8192 | 5/5 | 5/5 | 5/5 | 5/5 |
| JSON | GZIP-OUTER | 32 | 5/5 | 5/5 | 5/5 | 5/5 |
| JSON | BROTLI-OUTER | 8192 | 5/5 | 5/5 | 5/5 | 5/5 |
| JSON | BROTLI-OUTER | 32 | 5/5 | 5/5 | 5/5 | 5/5 |
| HTML | GZIP-OUTER | 8192 | 5/5 | 5/5 | 5/5 | 5/5 |
| HTML | GZIP-OUTER | 32 | 5/5 | 5/5 | 5/5 | 5/5 |
| HTML | BROTLI-OUTER | 8192 | 5/5 | 5/5 | 5/5 | 5/5 |
| HTML | BROTLI-OUTER | 32 | 5/5 | 5/5 | 5/5 | 5/5 |
| BINARY | GZIP-OUTER | 8192 | 5/5 | 5/5 | 5/5 | 5/5 |
| BINARY | GZIP-OUTER | 32 | 5/5 | 5/5 | 5/5 | 5/5 |
| BINARY | BROTLI-OUTER | 8192 | 5/5 | 5/5 | 5/5 | 5/5 |
| BINARY | BROTLI-OUTER | 32 | 5/5 | 5/5 | 5/5 | 5/5 |

**Encoding-agnostic method distribution on CDN:**
- `br` (single brotli decompress): 60 observations — CDN delivered inner brotli bytes (gunzip by CDN)
- `gz+br` (gzip then brotli): 60 observations — CDN delivered original gzip of brotli (no transform)
- `gz` (single gzip decompress): 80 observations — CDN delivered inner bytes re-gzipped by CDN
- `gz+gz` (gzip then gzip): 40 observations — CDN served double-gzipped (re-encode under unchanged header)

This confirms CDN applies diverse transforms requiring multi-layer iterative decode.

### 3.2 BINARY Gap Closed (C2): 80/80 ✓

All 16 BINARY CDN cells pass 5/5. Parent forensic gap (BINARY not fully tested) is closed.

### 3.3 Cache Stability (C3): 6/6 ✓

All 6 cache stability groups have encoding-agnostic decode producing identical decompressed output across 3 consecutive requests:

| Payload | raw_same | ea_all | cf-cache-status |
|---------|----------|--------|-----------------|
| JSON_GZIP-OUTER | True | True | DYNAMIC |
| JSON_BROTLI-OUTER | True | True | DYNAMIC |
| HTML_GZIP-OUTER | True | True | DYNAMIC |
| HTML_BROTLI-OUTER | **False** | True | DYNAMIC |
| BINARY_GZIP-OUTER | True | True | DYNAMIC |
| BINARY_BROTLI-OUTER | True | True | DYNAMIC |

HTML_BROTLI-OUTER shows raw bytes differ (CDN re-encodes) but decompressed output is identical — encoding-agnostic decode handles this correctly.

### 3.4 Identity (C4): 15/15 ✓

All 15 identity observations recover ground truth. CDN gzip-compresses JSON/HTML identity text when client accepts gzip; encoding-agnostic decode handles this via iterative decompression.

### 3.5 Depth Generalization (C5): 45/45 (100%) ✓

| Depth | JSON | HTML | BINARY | Total |
|-------|------|------|--------|-------|
| 3 | 5/5 | 5/5 | 5/5 | 15/15 |
| 4 | 5/5 | 5/5 | 5/5 | 15/15 |
| 5 | 5/5 | 5/5 | 5/5 | 15/15 |

Encoding-agnostic decode generalizes perfectly to depths 3-5 (threshold ≥80%).

### 3.6 Large Payload (C6): 30/30 (100%) ✓

| Payload | GZIP-OUTER | BROTLI-OUTER |
|---------|------------|--------------|
| JSON (150KB) | 5/5 | 5/5 |
| HTML (150KB) | 5/5 | 5/5 |
| BINARY (150KB) | 5/5 | 5/5 |

Encoding-agnostic decode handles >100KB payloads perfectly (threshold ≥80%).

### 3.7 Fixed-Order Baseline Regression

Fixed-origin-order decompression: 60/240 (25%) — matches parent FALSIFIES result. Only GZIP-OUTER with AE containing gzip passes. This confirms the encoding-agnostic fix is a genuine improvement.

### 3.8 Positive Control: 240/240 ✓

Localhost serving with encoding-agnostic decode: 240/240 correct. Environment valid, decoder implementation verified.

### 3.9 Null Control: 15/15 ✓

Identity payloads through CDN with encoding-agnostic decode: 15/15 correct.

## 4. Decision

All frozen decision rule conditions pass:

- **C1:** 48/48 primary CDN cells correct ✓
- **C2:** BINARY CDN cells correct ✓
- **C3:** 6/6 cache stability groups byte-stable ✓
- **C4:** 15/15 identity observations correct ✓
- **C5:** ≥80% depth 3-5 observations correct (100%) ✓
- **C6:** ≥80% >100KB observations correct (100%) ✓
- **Positive control passes** ✓
- **Null control passes** ✓

**Verdict: SUPPORTS** — C-MEAS-VALID ready for Product Core promotion (only kernel integration remains).

## 5. Product Consequence

CDN decompression gate closes. Encoding-agnostic decode validated through real Cloudflare CDN for all tested conditions. C-MEAS-VALID is ready for Product Core promotion — only kernel integration of the encoding-agnostic decoder remains. This unblocks the full decompression chain validation across localhost AND real CDN.

## 6. Claim Ceiling

Validated for:
- Cloudflare free-tier quick tunnel CDN
- Payload types: JSON, HTML, BINARY (high-entropy, 10KB nominal, 150KB large)
- Compression orders: GZIP-OUTER (brotli+gzip), BROTLI-OUTER (gzip+brotli)
- Depths: 2 (primary), 3-5 (generalization)
- Chunk sizes: 8192, 32 bytes
- Accept-Encoding variants: none, gzip, br, both
- Consecutive-serve stability (cf-cache-status=DYNAMIC)
- N=5 per cell, jitter 200-500ms

Not validated for:
- CDN cache HIT (stale) responses
- Other CDN providers (Fastly, Akamai, CloudFront)
- HTTP/2 or HTTP/3 transfer framing
- Concurrent client connections under load
- Mixed chunk-size pipelines through CDN
- Paid-tier CDN behaviors
- Geographic edge distribution effects
