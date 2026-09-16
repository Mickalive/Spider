# EXP-RUNTIME-35058619700 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35058619700
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does decompression-normalization preserve body-only discrimination under gzip quality variation, and does it generalize across compression algorithms (brotli vs gzip)?

## 3. Motivation

Prior Runtime work established:
- EXP-RUNTIME-34986155186: Decompression-normalization preserves discrimination at 0.5 under synthetic brotli quality variation {4,5,6,7,8}. Compressed-byte hashing degrades to ~0.33-0.35 under quality variation.
- EXP-RUNTIME-34741873198: Body-only discrimination survives deterministic CDN negotiation with brotli and gzip per client profile.
- EXP-RUNTIME-34902094115: Decompression-normalization works under fixed brotli quality.

The parent handoff identifies "Does normalized fingerprint survive with gzip (and mixed Accept-Encoding)" as an unknown. This experiment directly tests that question.

**Why gzip matters:**
- gzip is the most widely supported compression algorithm on the Web (all browsers, all CDNs)
- brotli is newer and may not be supported by all intermediaries
- A normalization layer that works only for brotli is less useful than one that works for both
- gzip has different compression characteristics than brotli (LZ77+Huffman vs brotli's LZ77+Huffman+static dictionary)
- Quality levels have different semantics (gzip 1-9 vs brotli 0-11)

**What this experiment tests:**
1. Does decompression-normalization work under gzip quality variation (not just brotli)?
2. Is the normalization algorithm-agnostic (same discrimination for brotli and gzip)?
3. Does compressed-byte hashing degrade under gzip quality variation (as it does under brotli)?

## 4. Hypotheses

### H1: Gzip Decompression-Normalization Preserves Discrimination
Decompression-normalization achieves discrimination >= 0.5 on /userinfo under both fixed and varying gzip quality.

### H2: Gzip Compressed-Byte Hashing Degrades
Body-only discrimination on compressed bytes degrades under gzip quality variation {1,3,5,7,9} to < 0.5 (similar to brotli quality variation).

### H3: Algorithm Equivalence
|B-DECOMPRESSED-VARYING-GZIP - B-DECOMPRESSED-VARYING-BROTLI| < 0.1, demonstrating that decompression-normalization is algorithm-agnostic.

## 5. Conditions

### 5.1 Compression Conditions

Five conditions, same infrastructure as parent:

1. **COMPRESSED-FIXED-GZIP**: Fixed gzip level 9 (deterministic, baseline)
2. **COMPRESSED-VARYING-GZIP**: Gzip level randomly selected from {1,3,5,7,9} per request
3. **DECOMPRESSED-FIXED-GZIP**: Decompressed body hash at fixed gzip level 9
4. **DECOMPRESSED-VARYING-GZIP**: Decompressed body hash with gzip level {1,3,5,7,9}
5. **DECOMPRESSED-VARYING-BROTLI**: Decompressed body hash with brotli quality {4,5,6,7,8} (replicates parent)

### 5.2 Server and States

Same mock OAuth2 server as parent:
- Port 5000 on localhost
- 4 auth states: no_auth (401), valid_token (200), expired_token (401), invalid_token (401)
- Error bodies identical across no_auth/expired/invalid (discrimination ceiling 0.5)
- Body: JSON with field 'data' = hex(random bytes), ~1KB uncompressed

### 5.3 Compression Proxy

CDN simulation proxy on port 5001:
- Reads client Accept-Encoding and selects highest-priority algorithm
- For gzip conditions: applies gzip with level from frozen seed
- For brotli condition: applies brotli with quality from frozen seed
- Python gzip with mtime=0 eliminates timestamp non-determinism
- Proxy restart per condition (same as parent)

## 6. Sample Size

- 4 states × 20 reps × 2 endpoints × 5 conditions = 800 total requests
- Seed=44 for reproducibility
- Jitter 50-150ms uniform between requests

## 7. Baselines and Controls

### 7.1 Positive Control (B-COMPRESSED-FIXED-GZIP)
- Body-only discrimination at fixed gzip level 9 on /userinfo
- Expected: >= 0.35 (replicates EXP-RUNTIME-34741873198)
- Verifies: harness produces same result as prior work

### 7.2 Null Control (B-RANDOM)
- Random fingerprint at all conditions
- Expected: ~0.0
- Verifies: no spurious structure from compression artifacts

### 7.3 Decompression Determinism Control
- Within-state decompressed hash variation = 0 for DECOMPRESSED-FIXED-GZIP
- Expected: all same = true, unique_count = 1 per state
- Verifies: gzip decompression is deterministic

### 7.4 Quality Variation Active Control
- Within-state compressed hash variation > 0 for COMPRESSED-VARYING-GZIP
- Expected: unique_count >= 2 per state (quality levels produce different compressed bytes)
- Verifies: gzip quality variation is active and producing non-determinism

### 7.5 Algorithm Equivalence Control
- |B-DECOMPRESSED-VARYING-GZIP - B-DECOMPRESSED-VARYING-BROTLI| < 0.1
- Expected: both achieve 0.5 (decompression-normalization is algorithm-agnostic)
- Verifies: normalization works identically across algorithms

## 8. Decision Rules

### 8.1 SURVIVES_CURRENT_TEST
If ALL of:
1. B-COMPRESSED-FIXED-GZIP >= 0.35 on /userinfo (positive control passes)
2. B-RANDOM ~ 0.0 at all conditions (null control passes)
3. B-DECOMPRESSED-FIXED-GZIP >= 0.5 on /userinfo (decompression-normalization preserves discrimination under fixed gzip)

### 8.2 MIXED
If B-DECOMPRESSED-FIXED-GZIP >= 0.5 BUT B-COMPRESSED-VARYING-GZIP < 0.35 (body-only fails under gzip quality variation but normalization works)

### 8.3 ALGORITHM-EQUIVALENT (advisory, not a verdict)
If |B-DECOMPRESSED-VARYING-GZIP - B-DECOMPRESSED-VARYING-BROTLI| < 0.1 (decompression-normalization is algorithm-agnostic)

### 8.4 FALSIFIED-IN-SETTING
If B-DECOMPRESSED-FIXED-GZIP < 0.35 (normalization fails under fixed gzip)

### 8.5 MEASUREMENT_INVALID
If pipeline errors or sample size insufficient

## 9. Validity Threats

### 9.1 Synthetic-to-Real Gap
Same mock OAuth2 server as parent. Gzip quality variation via Python proxy does not exercise real CDN non-determinism sources (caching, chunked transfer, load-balancing across edges, Accept-Encoding negotiation per-request). Claim ceiling bounded to synthetic proxy.

### 9.2 Body Size
~1KB JSON body. Compression behavior changes with body size: larger responses may trigger different compression levels or chunking. Generalization to KB-scale and MB-scale not supported.

### 9.3 Gzip Level Range
Tested {1,3,5,7,9} (5 levels). Real CDN behavior may use different level ranges or adaptive compression. Level 1 is fastest/least compressed; level 9 is slowest/most compressed. The range covers the full gzip quality spectrum.

### 9.4 Determinism by Construction
Python gzip with mtime=0 is deterministic by implementation. The experiment tests "does deterministic compression preserve hash stability" where both premise and implementation enforce determinism. Passing is expected; falsification would require proxy bug not CDN behavior.

### 9.5 3-Way Error Collapse
no_auth, expired_token, invalid_token have identical bodies (structural ceiling). Discrimination 0.5 reflects 200 vs 401 plus collapsed triple, not body content beyond status. This is identical to parent.

## 10. Analysis Plan

1. **Data Collection**: 800 HTTP requests across 5 conditions × 4 states × 20 reps × 2 endpoints
2. **Fingerprinting**: SHA256(repr((status, compressed_body_sha256, ''))) for compressed, SHA256(repr((status, decompressed_body_sha256, ''))) for decompressed
3. **Discrimination**: intra_match - inter_match for 4 states (180 intra pairs, 600 inter pairs; 300 of 600 inter matches due to 3 collapsed error states)
4. **Controls**: Verify positive, null, decompression determinism, quality variation active, and algorithm equivalence controls
5. **Reporting**: Report all outcomes with equal prominence

## 11. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 12. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
