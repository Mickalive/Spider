# EXP-RUNTIME-35542474231 — Encoding-Agnostic CDN Decompression

## Preregistration

**experiment_id**: EXP-RUNTIME-35542474231
**lane**: runtime
**claim_ids**: C-MEAS-VALID
**status**: DESIGN — not yet frozen

---

## 1. Question

Does encoding-agnostic iterative decompression (sniff delivered bytes, try brotli→gzip→identity until SHA256 matches ground truth) restore byte-identical correctness through Cloudflare CDN for all 48 payload×order×chunk×Accept-Encoding conditions — and does it generalize to depths 3-5 and payloads >100KB?

## 2. Inherited State (from EXP-RUNTIME-35538865067 handoff)

### Established
- CDN byte-identity hypothesis FALSIFIED for fixed-origin-order iterative decompression: 60/240 correct (25%)
- Positive control B-LOCALHOST-DIRECT: 240/240, environment valid
- CDN cache stability: 6/6 triplets byte-stable, cf-cache-status DYNAMIC (no HIT observed)
- Encoding-agnostic iterative full-body decode recovers ground truth on 24/24 JSON/HTML forensic CDN deliveries (exploratory, not a frozen condition)
- CDN does not corrupt bytes; failure is in fixed-origin-order framing assumption
- No chunk-size effect: 8192 vs 32 agree on all 48 cells
- High-entropy payload generators validated: JSON 5.57, HTML 4.66, BINARY 7.69 bits/byte

### Rejected
- CDN preserves origin Content-Encoding byte-identical
- Fixed-origin-order iterative decompression through CDN
- Gzip/brotli chunk boundary corruption at chunk_size=32
- Streaming chunked forwarding corruption
- Degenerate synthetic payloads as adequate test material

### Unknown (this experiment targets these)
- Does encoding-agnostic decode restore 240/240 correctness through Cloudflare CDN?
- Does it generalize to depths 3-5, payloads >100KB?
- Does it work for BINARY payloads (parent forensic only fully tested JSON/HTML)?
- Does CDN cache HIT staleness (if observed) cause different behavior?

### Do Not Assume
- C-MEAS-VALID is ready for Product Core promotion (CDN gate still open)
- Encoding-agnostic decode works on all CDN conditions (24/24 was exploratory)
- Localhost correctness implies CDN correctness
- CDN re-encoding is always benign at all quality levels

## 3. Hypothesis

An encoding-agnostic decoder that sniffs delivered bytes and iteratively attempts brotli→gzip→identity decompression until SHA256 matches ground truth restores byte-identical correctness through Cloudflare CDN for all tested conditions.

**Mechanism**: CDN re-encoding is lossless (parent forensic confirmed iterative decode == ground truth). The failure in the parent was the fixed-origin-order assumption (replaying the origin's layer stack against wire bytes after CDN has transformed them). Encoding-agnostic decode removes this assumption by treating the delivered bytes as an opaque blob and trying all decompression paths.

## 4. Falsifier

The hypothesis is falsified if any of the following occur:

1. **C1 failure**: Any of the 48 primary CDN cells produces decompressed SHA256 ≠ ground truth under encoding-agnostic decode
2. **C2 failure**: BINARY CDN cells fail (parent forensic gap)
3. **C5 failure**: Depth 3-5 CDN observations fail at >20% rate
4. **C6 failure**: >100KB CDN observations fail at >20% rate
5. **Identity corruption**: CDN corrupts (not merely compresses) uncompressed data

## 5. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-ENCODING-AGNOSTIC-REGRESSION | Parent fixed-origin-order on same 48-cell matrix | 60/240 correct (parent result) |
| B-LOCALHOST-DIRECT | Same payloads, localhost, no CDN | 240/240 (parent re-validation) |
| B-CDN-IDENTITY | Uncompressed payloads through CDN | Encoding-agnostic decode recovers ground truth for all 15 |
| B-DEPTH-GENERALIZATION | Depths 3-5 stacked encodings through CDN | ≥80% correct under encoding-agnostic decode |
| B-LARGE-PAYLOAD | >100KB payloads through CDN | ≥80% correct under encoding-agnostic decode |

## 6. Controls

### Positive control
**B-LOCALHOST-DIRECT**: encoding-agnostic decode on localhost matches ground truth. Validates the decoder implementation. If this fails, no CDN inference is possible.

### Null control
**B-CDN-IDENTITY**: encoding-agnostic decode on uncompressed CDN payloads recovers ground truth. If CDN corrupts uncompressed data, compressed data cannot be trusted.

## 7. Measurement Protocol

### Primary matrix (48 conditions × N=5 = 240 CDN observations)
- 3 payload types: JSON (5.57 bits/byte), HTML (4.66 bits/byte), BINARY (7.69 bits/byte)
- 2 compression orders: GZIP-OUTER (inner brotli q4, outer gzip L1), BROTLI-OUTER (inner gzip L1, outer brotli q4)
- 2 chunk sizes: 8192, 32 bytes (decompressor feed granularity)
- 4 Accept-Encoding variants: none, gzip, br, both (gzip, br)
- N=5 per cell, unique URLs, Cache-Control: max-age=0, jitter 200-500ms

### Cache stability (6 triplets × 3 reps = 18 CDN observations)
- Fixed URLs, 1s spacing, same as parent

### Identity (15 observations)
- 3 payloads × 5 reps through CDN with no pre-compression

### Depth generalization (exploratory, ≥60 CDN observations)
- Depths 3-5 with alternating brotli(q4)/gzip(L1) stacking
- 3 payload types × 2 depth ranges (3, 4-5) × 5 reps minimum
- Same CDN protocol (unique URLs, jitter)

### Large payload (exploratory, ≥30 CDN observations)
- >100KB high-entropy payloads (JSON, HTML, BINARY)
- 2-layer stacking (GZIP-OUTER and BROTLI-OUTER)
- 5 reps per condition

### Decoding algorithm
```
def encoding_agnostic_decode(raw_bytes, ground_truth_sha256):
    """Try brotli → gzip → identity until SHA256 matches."""
    for decoder in [brotli_decompress, gzip_decompress, identity]:
        try:
            decoded = decoder(raw_bytes)
            if sha256(decoded) == ground_truth_sha256:
                return decoded
        except Exception:
            continue
    return None  # all decoders failed
```

### Ground truth
Same as parent: full-body iterative decode of origin-served payloads (decompress all layers in known order), SHA256 of final decompressed output. For identity payloads, ground truth is the raw uncompressed bytes.

## 8. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- C1: 48/48 primary CDN cells correct under encoding-agnostic decode
- C2: BINARY CDN cells correct (closing parent forensic gap)
- C3: 6/6 cache stability groups byte-stable
- C4: 15/15 identity observations recover ground truth
- C5: ≥80% depth 3-5 observations correct
- C6: ≥80% >100KB observations correct
- Positive control passes (240/240 localhost)
- Null control passes (identity)

**FALSIFIES** if:
- C1 fails (any primary cell incorrect)
- C2 fails (BINARY incorrect)

**MIXED** if:
- C1 passes but C5 or C6 fails (<80% on generalization conditions)

## 9. Product Consequences

### If SURVIVES
CDN decompression gate closes. C-MEAS-VALID is ready for Product Core promotion. Only kernel integration of the encoding-agnostic decoder remains. The full decompression chain is validated across localhost AND real CDN.

### If FALSIFIES
C-MEAS-VALID remains blocked. Diagnosis of failing cells identifies the specific fix needed (encoding detection order, depth handling, payload size, BINARY ground truth).

### If MIXED
Primary gate passes (depth-2 works), but generalization is bounded. C-MEAS-VALID promotion would carry a ceiling annotation: "validated for depth-2, 10KB payloads through Cloudflare CDN; deeper/larger conditions untested."

## 10. Estimated Cost

- Infrastructure: cloudflared binary, Python HTTP server, brotli library (same as parent)
- Additional: payload generation for depths 3-5 and >100KB (~5 min)
- Wall time: ~15-20 minutes total
- Compute: no GPU, no browser automation, no paid services

## 11. Expected Information Gain

Very high. This is the sole remaining blocker for C-MEAS-VALID Product Core promotion per the parent handoff. A positive result closes the CDN gate. A negative result identifies the remaining fix. Both outcomes directly change a product decision. The experiment is the smallest possible test that can resolve the inherited unknown.
