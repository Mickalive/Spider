# EXP-RUNTIME-35130682006 — Preregistration

**Status:** DESIGN NOT YET FROZEN.

## 1. Experiment Identity

- **experiment_id:** EXP-RUNTIME-35130682006
- **lane:** runtime
- **parent:** EXP-RUNTIME-35058619700 (handoff sha256: b9bc44c5...)
- **claim_ids:** C-MEAS-VALID
- **created_at:** 2026-09-16

## 2. Question

After fixing BROTLI_QUALITY_RANGE to (4,5,6,7,8) and re-executing DECOMPRESSED-VARYING-BROTLI with N=20 per state, does |B-DECOMPRESSED-VARYING-GZIP - B-DECOMPRESSED-VARYING-BROTLI| remain <0.1 for the full 5-level brotli range, and does the /introspect compressed variation become >1 for error bodies at larger sizes?

## 3. Hypotheses

### H1: Decompression-normalization preserves discrimination under full brotli quality variation

Decompression-normalization (SHA256 on decompressed body + status via brotli.decompress after Content-Encoding removal) preserves body-only discrimination at 0.5 under brotli quality variation {4,5,6,7,8} because:
- brotli.decompress() is deterministic for fixed input+quality
- Different logical bodies decompress to different bytes regardless of quality level
- The structural ceiling of 0.5 is set by 3-way error collapse (no_auth/expired/invalid share identical body)

### H2: Algorithm-equivalence holds across full 5-level brotli range

|B-DECOMPRESSED-VARYING-GZIP - B-DECOMPRESSED-VARYING-BROTLI-FIXED| < 0.1 because:
- Decompression-normalization is algorithm-agnostic: it removes Content-Encoding and decompresses
- The decompressed body is identical across algorithms for the same logical body
- Parent demonstrated diff=0.0 for binary brotli {4,8} vs gzip {1,3,5,7,9}
- Full 5-level brotli should not change the decompressed output

### H3: Compressed-byte-only hashing degrades under full brotli quality variation

B-COMPRESSED-VARYING-BROTLI-FIXED < 0.35 on /userinfo because:
- Quality levels 4-8 produce different compressed byte sequences for the same logical body
- Binary {4,8} degraded to 0.2286 (parent); full 5-level should produce similar or larger degradation
- More quality levels may produce more unique compressed outputs, increasing degradation

## 4. Baselines

| ID | Description | Expected | Source |
|----|-------------|----------|--------|
| B-DECOMPRESSED-VARYING-GZIP | Decompressed body hash under gzip quality {1,3,5,7,9} | 0.5 | PARENT reference (not re-executed) |
| B-DECOMPRESSED-VARYING-BROTLI-FIXED | Decompressed body hash under brotli quality {4,5,6,7,8} (FIXED) | 0.5 | THIS EXPERIMENT |
| B-COMPRESSED-VARYING-BROTLI-FIXED | Compressed-byte-only hash under brotli quality {4,5,6,7,8} (FIXED) | <0.35 | THIS EXPERIMENT |
| B-STATUS-ONLY | Status code only (compression-immune) | 0.5 /userinfo, 0.0 /introspect | PARENT reference |
| B-RANDOM | Random fingerprint | 0.0 | PARENT reference |

## 5. Controls

### 5.1 Positive Control: Decompression Determinism

Within-state decompressed hash variation = 0 for all 4 states under DECOMPRESSED-VARYING-BROTLI-FIXED.
This verifies brotli.decompress() is deterministic across the full quality range {4,5,6,7,8}.
If any state shows unique_count > 1, decompression is non-deterministic and the experiment is MEASUREMENT_INVALID.

### 5.2 Null Control: B-RANDOM

B-RANDOM ~ 0.0 at all conditions (PARENT reference, not re-executed).

### 5.3 Algorithm-Equivalence Control

|B-DECOMPRESSED-VARYING-GZIP(parent) - B-DECOMPRESSED-VARYING-BROTLI-FIXED| < 0.1.
This is the primary decision criterion. Parent observed diff=0.0 for binary brotli; full 5-level must remain < 0.1.

## 6. Conditions

Only **1 condition** is re-executed:

| Condition | Algorithm | Quality Range | N/state | Endpoints | Total Requests |
|-----------|-----------|---------------|---------|-----------|----------------|
| DECOMPRESSED-VARYING-BROTLI-FIXED | brotli | {4,5,6,7,8} | 20 | 2 (/userinfo, /introspect) | 160 |

Parent conditions (reference only, NOT re-executed):
- COMPRESSED-FIXED-GZIP (gzip level 9, N=20)
- COMPRESSED-VARYING-GZIP (gzip {1,3,5,7,9}, N=20)
- DECOMPRESSED-FIXED-GZIP (gzip level 9, N=20)
- DECOMPRESSED-VARYING-GZIP (gzip {1,3,5,7,9}, N=20)
- DECOMPRESSED-VARYING-BROTLI (brotli {4,8} — the buggy binary version)

## 7. Measurement

### 7.1 Fingerprint Algorithm

Same as parent:
- `fingerprint_compressed = SHA256(repr((status, SHA256(compressed_bytes), '')))`
- `fingerprint_decompressed = SHA256(repr((status, SHA256(decompressed_bytes), '')))`
- Decompressed body: brotli.decompress(compressed_bytes) after removing Content-Encoding header

### 7.2 Discrimination Score

Same as parent:
- `discrimination = intra_match_rate - inter_match_rate`
- Intra-match: fraction of same-state same-condition fingerprint pairs that match
- Inter-match: fraction of different-state same-condition fingerprint pairs that match
- Structural ceiling = 0.5 (3-way error collapse)

### 7.3 Derived Metrics

- `compressed_hash_variation`: unique compressed SHA256 hashes per state (expected: 2-5 distinct for 5 quality levels)
- `decompressed_hash_variation`: unique decompressed SHA256 hashes per state (expected: 1 — deterministic)
- `body_sizes`: min/max/mean compressed body size per state per quality level
- `algorithm_equivalence_diff`: |parent_gzip_decompressed - this_brotli_decompressed|

## 8. Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
1. Within-state decompressed hash variation = 0 for all states (positive control)
2. B-RANDOM ~ 0.0 at all conditions (null control — PARENT reference)
3. DECOMPRESSED-VARYING-BROTLI-FIXED decompressed discrimination >= 0.5 on /userinfo
4. |B-DECOMPRESSED-VARYING-GZIP(parent) - B-DECOMPRESSED-VARYING-BROTLI-FIXED| < 0.1

**ALGORITHM-EQUIVALENT** if condition (4) holds (diff < 0.1).

**ALGORITHM-DEPENDENT** if condition (4) fails (diff >= 0.1).

**FALSIFIED-IN-SETTING** if condition (3) fails (decompression-normalization fails under full brotli quality).

**MEASUREMENT_INVALID** if pipeline errors or sample size insufficient.

**MIXED** if decompressed >= 0.5 BUT compressed-varying < 0.35 (degradation on compressed side but normalization compensates). Note: both SURVIVES and MIXED may fire; SURVIVES takes priority as it addresses the primary algorithm-equivalence question.

## 9. Validity Threats

### 9.1 Synthetic-to-Real Gap (inherited)

Same as parent: local Python proxy on port 5001 with brotli.compress() does not exercise real CDN non-determinism (caching, chunked transfer, load-balancing, Accept-Encoding negotiation). Result bounded to synthetic determinism model.

### 9.2 Brotli Quality-Level Collapse at Larger Bodies

Brotli quality variation may produce more distinct outputs for larger payloads (>1KB). The parent observed 2 unique compressed hashes/20 for 1KB JSON at binary {4,8}; full 5-level may yield 3-5 uniques. This could increase compressed-varying degradation. Mitigation: report compressed_hash_variation unique_count per state explicitly.

### 9.3 Error-Body Insensitivity (inherited)

Brotli error bodies (21B compressed) showed 1 unique hash/20 for 3 of 4 states at binary {4,8}. Full 5-level may still show 1 unique for tiny payloads. Mitigation: report per-state compressed variation; algorithm-equivalence is tested on decompressed side (body-size invariant).

### 9.4 Parent Reference Data Not Re-Executed

Gzip baselines reference parent EXP-RUNTIME-35058619700 data. If parent data has undetected issues, the algorithm-equivalence comparison inherits those issues. Mitigation: parent data was independently audited with max_abs_diff=0.0 recomputation.

### 9.5 Single Seed

Seed=44 for quality variation ordering. Single seed means quality-level mapping is fixed. If brotli quality 5 happens to produce identical output to quality 4 for 1KB JSON, the full range may appear binary. Mitigation: report compressed_hash_variation unique_count; if < 5 for valid_token bodies, note potential collapse.

## 10. Sample Size

- N=20 per state per endpoint for DECOMPRESSED-VARYING-BROTLI-FIXED
- 4 states x 20 reps x 2 endpoints = 160 requests
- Same as parent per-state sample size
- Adequate for discrimination score estimation (parent recomputed exactly, max_abs_diff=0.0)

## 11. Expected Outcomes

| Outcome | Implication |
|---------|-------------|
| SURVIVES + ALGORITHM-EQUIVALENT | Full brotli range does not break algorithm-equivalence. Claim broadens from binary {4,8} to full {4,5,6,7,8}. Product can deploy universal normalization. |
| SURVIVES + ALGORITHM-DEPENDENT | Intermediate brotli levels break equivalence. Claim ceiling restricted to tested conditions. Per-algorithm code paths needed. |
| FALSIFIED-IN-SETTING | Decompression-normalization fails under full brotli quality variation. Fundamental decomposition problem. |
| MEASUREMENT_INVALID | Infrastructure issue (brotli library, proxy, etc.). Not a scientific result. |

## 12. Consequences

### If Positive (SURVIVES + ALGORITHM-EQUIVALENT)

- C-MEAS-VALID claim ceiling broadens: algorithm-equivalence validated for full brotli {4,5,6,7,8}
- Product recommendation: universal decompression-normalization (algorithm-agnostic)
- Next question: real-CDN validation (inherited from parent handoff)
- Do NOT promote to Product Core — still synthetic proxy only

### If Negative (ALGORITHM-DEPENDENT or FALSIFIED)

- C-MEAS-VALID claim ceiling narrows: algorithm-equivalence bounded to tested conditions
- Product requires per-algorithm normalization paths
- Next question: identify which brotli quality levels break equivalence and whether they correspond to common CDN configurations
- Real-CDN question remains blocked

## 13. Artifacts

- `run_experiment.py` — modified experiment script with BROTLI_QUALITY_RANGE fix
- `raw_observations.json` — 160 HTTP observations (4 states x 20 reps x 2 endpoints)
- `result.json` — structured metrics and controls
- `report.md` — interpretation bounded by measurements

## 14. Forks

None. This is a deterministic re-execution of a single condition with a bug fix. No branching decisions anticipated.
