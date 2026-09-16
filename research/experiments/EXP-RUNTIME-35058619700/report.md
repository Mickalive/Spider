# EXP-RUNTIME-35058619700 — Execution Report

## Experiment Identity

- **Experiment ID**: EXP-RUNTIME-35058619700
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID
- **Status**: COMPLETE
- **Outcome**: MIXED

## Executive Summary

Decompression-normalization is **algorithm-agnostic**: it achieves maximum discrimination (0.5) under both gzip and brotli quality variation. Compressed-byte hashing degrades under both algorithms, with gzip producing worse degradation than brotli. All 7 controls pass.

## Primary Metrics (/userinfo endpoint)

| Condition | Compressed | Decompressed | Status | B-RANDOM |
|---|---|---|---|---|
| COMPRESSED-FIXED-GZIP | 0.5000 | 0.5000 | 0.5000 | 0.0000 |
| COMPRESSED-VARYING-GZIP | 0.1714 | 0.5000 | 0.5000 | 0.0000 |
| DECOMPRESSED-FIXED-GZIP | 0.5000 | 0.5000 | 0.5000 | 0.0000 |
| DECOMPRESSED-VARYING-GZIP | 0.1974 | 0.5000 | 0.5000 | 0.0000 |
| DECOMPRESSED-VARYING-BROTLI | 0.2286 | 0.5000 | 0.5000 | 0.0000 |

## Controls

| Control | Expected | Observed | Pass |
|---|---|---|---|
| C_POSITIVE_CONTROL | B-COMPRESSED-FIXED-GZIP >= 0.35 | 0.5 | YES |
| C_NULL_CONTROL | B-RANDOM ~ 0.0 | [0.0, 0.0, 0.0, 0.0, 0.0] | YES |
| C_DECOMPRESSED_FIXED_PRESERVES | B-DECOMPRESSED-FIXED-GZIP >= 0.5 | 0.5 | YES |
| C_DECOMPRESSION_DETERMINISM | all_same=true for DECOMPRESSED-FIXED-GZIP | all states: true | YES |
| C_QUALITY_VARIATION_ACTIVE | unique_count > 1 for COMPRESSED-VARYING-GZIP | {no_auth:3, invalid:3, expired:3, valid:4} | YES |
| C_NO_PIPELINE_ERRORS | 0 errors | 0 | YES |
| C_ALGORITHM_EQUIVALENT | \|gzip_brotli_diff\| < 0.1 | 0.0 | YES |

## Detailed Findings

### Finding 1: Decompression-Normalization Is Algorithm-Agnostic

**H3 SUPPORTED.** The absolute difference between decompression-normalized discrimination under gzip and brotli quality variation is **0.0** on /userinfo:

- B-DECOMPRESSED-VARYING-GZIP = 0.5000
- B-DECOMPRESSED-VARYING-BROTLI = 0.5000
- |diff| = 0.0 < 0.1 threshold

This is the strongest possible result: decompression-normalization achieves identical discrimination regardless of compression algorithm. The SHA-256 hash of the decompressed body + status produces the same fingerprint whether the wire bytes were compressed with gzip or brotli.

**Product consequence:** Decompression-normalization is not brotli-specific. SPIDER can normalize any Content-Encoding (br, gzip, identity) without algorithm-specific code paths. This broadens deployment options behind CDNs that negotiate different algorithms for different clients.

### Finding 2: Compressed-Byte Hashing Degrades Under Both Algorithms

**H2 SUPPORTED.** Compressed-byte-only hashing degrades under quality variation for both algorithms:

| Algorithm | /userinfo | /introspect |
|---|---|---|
| Gzip {1,3,5,7,9} | 0.1714 | 0.1940 |
| Brotli {4,5,6,7,8} | 0.2286 | 0.3803 |

Gzip degrades **more** than brotli on /userinfo (0.1714 vs 0.2286). This is because gzip with mtime=0 produces 3-4 unique compressed outputs per state for 1KB JSON, while brotli produces only 2 unique outputs. More unique compressed hashes means more cross-state fingerprint collisions, hence lower discrimination.

The degradation is substantial: compressed-varying-gzip drops to ~0.17-0.19, well below the 0.35 threshold that was marginally breached in the parent (0.3475 for brotli). Gzip quality variation is a **stronger** threat to body-only architecture than brotli quality variation.

### Finding 3: Decompression Is Deterministic Under Fixed Gzip

**C_DECOMPRESSION_DETERMINISM PASS.** All 20 requests within each state produce identical decompressed hashes under fixed gzip level 9 (unique_count=1/20, all_same=true for all 4 states). This confirms that Python's `gzip.decompress()` with `mtime=0` is deterministic.

### Finding 4: Quality Variation Is Active

**C_QUALITY_VARIATION_ACTIVE PASS.** Under COMPRESSED-VARYING-GZIP, compressed hash unique_count ranges from 3-4 per state across 20 requests. The 5 quality levels {1,3,5,7,9} collapse to 3-4 distinct compressed outputs for this payload size, confirming that quality variation produces non-determinism on the wire.

## Decision Rule Application

Per frozen spec.json decision_rule:

- **SURVIVES_CURRENT_TEST** requires ALL of: (1) positive control >= 0.35, (2) null control ~ 0.0, (3) decompressed-fixed >= 0.5
  - All three pass: positive=0.5, null=0.0, decompressed-fixed=0.5
- **MIXED** requires: decompressed-fixed >= 0.5 BUT compressed-varying < 0.35
  - decompressed-fixed=0.5 >= 0.5 ✓, compressed-varying-gzip=0.1714 < 0.35 ✓
- **ALGORITHM-EQUIVALENT** requires: |gzip_decomp - brotli_decomp| < 0.1
  - |0.5 - 0.5| = 0.0 < 0.1 ✓

**Applied outcome: MIXED.** The MIXED classification fires because compressed-varying-gzip (0.1714) is below the 0.35 threshold, even though all SURVIVES conditions are met. The script's if/elif chain prioritizes MIXED over SURVIVES when both conditions are true.

**Interpretation:** The MIXED outcome reflects the fact that raw compressed bytes are unreliable under gzip quality variation, while decompression-normalization fully compensates. The practical answer is that decompression-normalization **survives** all tested conditions, but body-only hashing on compressed bytes **fails** under gzip variation.

## Scope Limitations (Validity Threats)

1. **Synthetic-to-real gap.** Mock OAuth2 server + Python proxy. Gzip quality variation via `random.randint` does not exercise real CDN non-determinism (caching, chunked transfer, load-balancing, Accept-Encoding negotiation). Claim ceiling bounded to synthetic proxy.

2. **Body size.** ~1KB JSON (1024 bytes). Compression behavior changes with body size. Generalization to KB-scale and MB-scale not supported.

3. **Gzip level range.** Tested {1,3,5,7,9} (5 levels). Real CDN behavior may use different ranges or adaptive compression.

4. **3-way error collapse.** no_auth, expired_token, invalid_token have identical bodies. Discrimination 0.5 reflects 200 vs 401 plus collapsed triple.

5. **Brotli quality range.** Tested {4,5,6,7,8} (parent range). Does not test extreme qualities (0-3, 9-11).

6. **Determinism by construction.** Python gzip with mtime=0 is deterministic by implementation. Falsification would require proxy bug, not CDN behavior.

## Consequences

### Positive Outcome (Algorithm-Equivalent Normalization)

Decompression-normalization achieves identical discrimination under both gzip and brotli quality variation. Product recommendation changes from "decompression-normalization is brotli-specific" to "decompression-normalization is algorithm-agnostic". This broadens deployment options: SPIDER can normalize any Content-Encoding without algorithm-specific code paths.

### Negative Outcome (Compressed-Byte Degradation Under Gzip)

Compressed-byte hashing degrades more under gzip (0.17) than brotli (0.23) quality variation. Gzip is a stronger threat to body-only architecture than brotli. This reinforces the need for decompression-normalization as a mandatory preprocessing step, not an optional enhancement.

### MIXED Classification nuance

The MIXED classification is technically correct per the frozen decision rule (compressed-varying < 0.35). However, the scientific conclusion is that decompression-normalization **fully compensates** for compressed-byte degradation under both algorithms. The MIXED label reflects the raw compressed-byte degradation, not a failure of normalization.

## Unresolved Questions

1. Does decompression-normalization survive real CDN infrastructure with non-deterministic compression?
2. Does result generalize to non-JSON content types (HTML, XML, binary) and to MB-scale?
3. What is latency cost of per-response gzip/brotli decompression before hashing at production scale?
4. What is behavior when Content-Encoding is missing, incorrect, or double-encoded?
5. Is compressed-varying threshold <0.35 robust across seeds and body sizes?
6. Does 2-unique-hashes (brotli) vs 3-4-unique-hashes (gzip) indicate that gzip quality levels are more semantically distinct for this payload?
