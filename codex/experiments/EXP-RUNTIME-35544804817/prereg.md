# EXP-RUNTIME-35544804817 — Oracle-Free Greedy CDN Decompression + Cache HIT Test

## Preregistration

**experiment_id**: EXP-RUNTIME-35544804817
**lane**: runtime
**claim_ids**: C-MEAS-VALID
**status**: DESIGN — not yet frozen

---

## 1. Question

Does oracle-free greedy iterative decompression (try brotli then gzip until neither succeeds, return final bytes — no SHA256 oracle) produce byte-identical output to ground truth on the same 48-cell Cloudflare CDN matrix, and does CDN cache HIT (stale) serving alter the decompressed output?

## 2. Inherited State (from EXP-RUNTIME-35542474231 handoff)

### Established
- Encoding-agnostic ORACLE-GUIDED iterative decompression (try brotli->gzip->identity until SHA256 matches ground truth) losslessly recovers ground truth for ALL tested Cloudflare free-tier CDN transformations on DYNAMIC responses: 240/240 primary cells, 80/80 BINARY, 15/15 identity, 45/45 depth 3-5, 30/30 large payloads. (EXP-RUNTIME-35542474231, audit REVISE with ceiling bounded)
- CDN does not corrupt bytes — the parent fixed-origin-order failure was in the framing assumption. CDN Accept-Encoding negotiation transforms are lossless. (EXP-RUNTIME-35538865067 + EXP-RUNTIME-35542474231)
- Encoding-agnostic method distribution: br=60, gz+br=60, gz=80, gz+gz=40 — each cell requires a deterministic path. (EXP-RUNTIME-35542474231)
- No chunk-size effect: 8192 vs 32 agree on all 48 cells. (EXP-RUNTIME-35542474231)
- Depth generalization: 45/45 at depths 3-5. Large payloads: 30/30 at >100KB. (EXP-RUNTIME-35542474231)

### Rejected
- Fixed-origin-order iterative decompression through Cloudflare CDN (180/240 failures)
- CDN preserves origin Content-Encoding byte-identical
- Gzip/brotli chunk boundary corruption at chunk_size=32
- Streaming chunked forwarding corruption
- Chunk size (8192 vs 32) affects CDN decompression correctness

### Unknown (this experiment targets these)
- Does oracle-free greedy iterative decompression (no SHA256 check) achieve 240/240 byte-identical correctness on the same 48-cell Cloudflare CDN matrix? Highly likely (format headers are distinct) but unmeasured. Audit V4 confirms the question.
- Does encoding-agnostic decode recover correctness for CDN cache HIT (stale) responses? All 423 CDN responses in the parent were cf-cache-status=DYNAMIC; zero HIT observed.
- Do CDN re-encodings at deeper depths (3-5) with different quality/level settings ever produce ambiguous bytes where both brotli and gzip decompress successfully (oracle tie-break needed)?

### Do Not Assume
- C-MEAS-VALID is ready for Product Core promotion — audit REVISE with producer_claim_supported=false; oracle-free decode validation and CDN HIT test required first
- Oracle-guided decode = deployable decoder — ground_truth_sha256 as stop condition is circular (audit V1, severity major)
- Encoding-agnostic decode works on all CDN conditions globally — validated only for Cloudflare free-tier quick tunnel edge iad05, DYNAMIC only
- CDN cache HIT behavior is safe — zero HIT observed; stale-cache serving not exercised
- The 87 duplicate rows in raw_cell_results.jsonl affect metrics — producer correctly reports deduped counts

## 3. Hypothesis

A greedy oracle-free iterative decoder that attempts brotli decompression, then gzip decompression, looping until neither succeeds and returning the final bytes WITHOUT checking SHA256 against ground truth produces byte-identical output to ground truth for all 48 primary Cloudflare CDN cells.

**Mechanism**: The parent method distribution (br=60, gz+br=60, gz=80, gz+gz=40) demonstrates that each cell requires a deterministic decompression path where only one format is valid at each layer. Brotli (magic 0xCEB2CF81) and gzip (magic 0x1F8B) have distinct format signatures, so the greedy try-brotli-then-gzip order is unambiguous. The parent's 240/240 oracle-guided result confirms all CDN transforms are losslessly recoverable by iterative decode. Without the oracle, the greedy algorithm naturally terminates when neither decompressor succeeds, returning the final bytes.

**CDN cache HIT hypothesis**: Cached responses are byte-identical to DYNAMIC responses because the CDN stores the compressed bytes and serves them unchanged. The Content-Encoding and body are the same regardless of cache status.

## 4. Falsifier

The hypothesis is falsified if any of the following occur:

1. **C1 failure**: Any of the 48 primary CDN cells produces decompressed SHA256 != ground truth under oracle-free greedy decode
2. **C2 failure**: CDN cache HIT responses diverge from ground truth or from DYNAMIC responses
3. **C5 failure**: Depth 3-5 CDN observations fail at >20% rate under oracle-free decode
4. **C6 failure**: >100KB CDN observations fail at >20% rate under oracle-free decode
5. **Ambiguity failure**: Both brotli and gzip decompress successfully at the same layer and produce divergent final SHA256 outputs

## 5. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-ORACLE-GUIDED-REGRESSION | Oracle-guided decode on same 48-cell CDN matrix | 240/240 (parent re-validation) |
| B-LOCALHOST-DIRECT | Same payloads served directly from localhost | 240/240 oracle-free decode |
| B-CDN-IDENTITY | Uncompressed payloads through CDN | 15/15 oracle-free decode |
| B-DEPTH-GENERALIZATION | Depths 3-5 stacked encodings through CDN | >=80% oracle-free decode |
| B-LARGE-PAYLOAD | >100KB payloads through CDN | >=80% oracle-free decode |
| B-FIXED-ORDER-CDN | Parent fixed-origin-order on same 48-cell matrix | 60/240 (parent result) |

## 6. Controls

### Positive control
**B-LOCALHOST-DIRECT**: oracle-free greedy decode on localhost matches ground truth. Validates the decoder implementation. If this fails, no CDN inference is possible.

### Null control
**B-CDN-IDENTITY**: oracle-free greedy decode on uncompressed CDN payloads recovers ground truth. If CDN corrupts uncompressed data, compressed data cannot be trusted.

## 7. Measurement Protocol

### Primary matrix (48 conditions x N=5 = 240 CDN observations)
- 3 payload types: JSON (5.57 bits/byte), HTML (4.66 bits/byte), BINARY (7.69 bits/byte)
- 2 compression orders: GZIP-OUTER, BROTLI-OUTER
- 2 chunk sizes: 8192, 32 bytes
- 4 Accept-Encoding variants: none, gzip, br, both (gzip, br)
- N=5 per cell, unique URLs, Cache-Control: max-age=0, jitter 200-500ms

### CDN cache HIT test (48 conditions x N=5 = 240 HIT observations)
- Same 48-cell matrix as primary
- Fixed URLs per cell (no cache-busting token)
- Cache-Control: public, max-age=300
- Two-phase: (1) initial request to populate cache; (2) second request 2-5s later to trigger HIT
- Record cf-cache-status for each observation; require >=90% HIT rate for validity
- Apply oracle-free greedy decode to HIT responses

### Cache stability (6 triplets x 3 reps = 18 CDN observations)
- Fixed URLs, 1s spacing, same as parent
- Verify oracle-free decode produces identical decompressed output across reps

### Identity (15 observations)
- 3 payloads x 5 reps through CDN with no pre-compression

### Depth generalization (>=60 CDN observations)
- Depths 3-5 with alternating brotli(q4)/gzip(L1) stacking
- 3 payload types x 2 depth ranges (3, 4-5) x 5 reps minimum

### Large payload (>=30 CDN observations)
- >100KB high-entropy payloads (JSON, HTML, BINARY)
- 2-layer stacking, 5 reps per condition

### Oracle-free greedy decode algorithm
```python
def oracle_free_greedy_decode(raw_bytes):
    """Try brotli -> gzip until neither succeeds, return final bytes.
    NO SHA256 oracle check at any point."""
    current = raw_bytes
    path = []
    ambiguous = False
    for depth in range(MAX_DEPTH):
        br_result = None
        gz_result = None
        # Try brotli
        try:
            br_result = brotli.decompress(current)
        except Exception:
            pass
        # Try gzip
        try:
            gz_result = gzip.decompress(current)
        except Exception:
            pass
        # Determine which succeeded
        if br_result is not None and gz_result is not None:
            # Ambiguous: both succeed. Record and try both.
            ambiguous = True
            # Default to brotli (try-brotli-first order)
            path.append("br")
            current = br_result
            # Store alternative for later comparison
            alt_path = path.copy()
            alt_path[-1] = "gz"
            alt_current = gz_result
        elif br_result is not None:
            path.append("br")
            current = br_result
        elif gz_result is not None:
            path.append("gz")
            current = gz_result
        else:
            # Neither succeeded: return current (identity or already decompressed)
            break
    method = "+".join(path) if path else "identity"
    return current, method, ambiguous
```

### Ground truth
Same as parent: full-body iterative decode of origin-served payloads (decompress all layers in known order), SHA256 of final decompressed output. For identity payloads, ground truth is the raw uncompressed bytes.

## 8. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- C1: 48/48 primary CDN cells correct under oracle-free greedy decode
- C2: >=90% of CDN HIT observations correct under oracle-free greedy decode
- C3: 6/6 cache stability groups byte-stable under oracle-free decode
- C4: 15/15 identity observations recover ground truth under oracle-free decode
- C5: >=80% depth 3-5 observations correct under oracle-free decode
- C6: >=80% >100KB observations correct under oracle-free decode
- C7: Zero ambiguous tie-breaks with divergent final SHA256 (if ambiguous but paths agree, that is acceptable)
- Positive control passes (240/240 localhost)
- Null control passes (identity)

**FALSIFIES** if:
- C1 fails (any primary cell incorrect under oracle-free decode)
- C7 fails (ambiguous tie-break produces different final outputs)

**MIXED** if:
- C1 passes but C2 fails (HIT staleness divergence)
- C1 passes but C5 or C6 fails (<80% on generalization conditions)

## 9. Product Consequences

### If SURVIVES
Oracle-free CDN decompression gate closes. C-MEAS-VALID advances to VALIDATED. The deployable decoder (no SHA oracle) is validated through real CDN for all tested conditions. Kernel integration is authorized. This is the final blocker for Product Core promotion of the decompression-normalization mechanism.

### If FALSIFIES
C-MEAS-VALID remains EXPERIMENTAL. Diagnosis of failing cells identifies the specific oracle-free failure mode (ambiguous format detection, greedy ordering, depth handling, or payload size). The product cannot use the decompression fix without SHA oracle.

### If MIXED
Primary gate passes (DYNAMIC works) but HIT staleness or generalization is bounded. C-MEAS-VALID carries a ceiling annotation: "oracle-free decode validated for Cloudflare CDN DYNAMIC responses; HIT/stale-cache and depth>2/large untested."

## 10. Estimated Cost

- Infrastructure: cloudflared binary, Python HTTP server, brotli library (same as parent)
- Reuse: parent payload manifest, ground truth computation, test harness
- Additional: cache HIT test phase (~5 min), oracle-free decode implementation (~30 min coding)
- Wall time: ~20-25 minutes total
- Compute: no GPU, no browser automation, no paid services

## 11. Expected Information Gain

Very high. This is the single highest-information experiment remaining for the decompression-normalization sub-thread per parent handoff. A positive result converts the lossless-recovery observation into a deployable mechanism and closes C-MEAS-VALID for Product Core. A negative result identifies the specific oracle-free failure mode. Both outcomes directly change a product decision. The experiment resolves the two inherited blocking gaps (oracle circularity V1 and HIT absence V3) in a single frozen design.
