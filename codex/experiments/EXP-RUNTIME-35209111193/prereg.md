# EXP-RUNTIME-35209111193 — Preregistration

**Experiment:** Decompression-normalization on non-JSON content types at multiple payload sizes (re-run with server compression fix)
**Lane:** runtime
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)
**Created:** 2026-09-17
**Parent:** EXP-RUNTIME-35154720995 (MEASUREMENT_INVALID — server never applied compression)

---

## 1. Motivation and inherited state

### 1.1 Why this is a re-run

EXP-RUNTIME-35154720995 was MEASUREMENT_INVALID due to a pure infrastructure failure: the MockOAuthHandler never applied brotli/gzip compression. All 2880 observations had `Content-Encoding='none'`. The decompression-normalization mechanism (SHA256 on decompressed body via `brotli.decompress`/`gzip.decompress`) was never exercised — it was dead code. All reported discrimination metrics (0.5) reflected identity-path body hashing, not decompression-normalization.

The frozen question, hypothesis, falsifier, baselines, controls, and decision rule from the parent are scientifically sound and remain untested. This re-run applies the minimal server fix: modify MockOAuthHandler to actually compress response bodies with brotli (quality 4-8) and gzip, and set Content-Encoding headers.

### 1.2 What the parent established (unchanged, not advanced)

Parent EXP-RUNTIME-35137033384 (the grandparent) established:
- Decompressed discrimination: /userinfo 0.5, /introspect 0.8333 (structural ceiling from 3-way error collapse)
- Compressed-only discrimination: /userinfo 0.2789 (< 0.35, confirming H3)
- Algorithm equivalence: |gzip - brotli| = 0.0 < 0.1
- Decompression determinism: all_same=true for all 4 states across both endpoints
- B-RANDOM null: 0.0

All of these were under CDN-noise proxy at 1KB JSON only.

### 1.3 What remains unknown (inherited from parent handoff)

1. **Non-JSON content types:** Does decompression-normalization work on HTML, XML?
2. **MB-scale payloads:** Does 5-level brotli quality selection produce distinct outputs for larger payloads?
3. **Real CDN infrastructure:** Does it survive Cloudflare/Fastly/Akamai? (BLOCKED — requires external infrastructure)
4. **Production latency:** What is the cost of per-response decompression at scale?

### 1.4 Why this experiment

Same as parent: directly answers items 1 and 2 from the handoff unknowns. The parent's design was frozen but never executed due to server failure. The fix is mechanical: modify the server handler to actually compress. The scientific question is identical.

---

## 2. Experimental design

### 2.1 Content types

Three content types, all returning OAuth2-like auth-state responses:

| Content Type | Body Structure | Auth-State Mapping |
|---|---|---|
| JSON | `{"error":"...", "message":"..."}` / `{"user":"...", "scope":"..."}` | Same 4 states as grandparent |
| HTML | `<html><body><div class="error">...</div></body></html>` / `<html><body><div class="user">...</div></body></html>` | Same 4 states, HTML-wrapped |
| XML | `<response><error>...</error></response>` / `<response><user>...</user></response>` | Same 4 states, XML-wrapped |

### 2.2 Payload sizes

Three sizes per content type, controlled by padding:

| Size | Padding Method |
|---|---|
| 1KB | Minimal body (auth-state specific content only) |
| 10KB | Repeated paragraph/list/element blocks |
| 100KB | Large repeated blocks |

### 2.3 Auth states

Same 4 states as grandparent:
- `no_auth`: No Authorization header → 401 with error body
- `expired_token`: Expired Bearer token → 401 with error body (shares body with no_auth/invalid)
- `invalid_token`: Malformed Bearer token → 401 with error body (shares body with no_auth/expired)
- `valid_token`: Valid Bearer token → 200 with user info body

3-way error collapse: no_auth, expired_token, and invalid_token return identical/similar error bodies. This caps /userinfo discrimination at 0.5 (status 401 vs 200 splits 2 vs 2).

### 2.4 Compression

- **Brotli quality levels:** 4, 5, 6, 7, 8 (5 levels)
- **Gzip:** Default compression level (1 algorithm variant)
- **Total baselines per condition:** DECOMPRESSED-VARYING-BROTLI (quality 4-8), DECOMPRESSED-VARYING-GZIP, COMPRESSED-VARYING-BROTLI, COMPRESSED-VARYING-GZIP

### 2.5 Sample size

N = 20 requests per state per content type per size per baseline.
Total states x types x sizes = 4 x 3 x 3 = 36 conditions.
Total requests per baseline = 36 x 20 = 720.
Total requests across all baselines ~ 720 x 4 = 2880 (feasible on localhost).

### 2.6 No CDN noise

This experiment does NOT apply the CDN-noise proxy. The grandparent already validated CDN-noise effects. This experiment isolates content-type and size effects. CDN noise can be added in a follow-up if content-type results are positive.

### 2.7 Server compression fix (NEW vs parent)

The MockOAuthHandler is modified to actually apply brotli/gzip compression:
1. In `do_GET`/`do_POST`, inspect `Accept-Encoding` or force per-baseline encoding
2. Compress body via `brotli.compress(data, quality=q)` for q in [4,5,6,7,8] and `gzip.compress`
3. Set `Content-Encoding` header to `'br'`/`'gzip'`
4. Set `Content-Length` to compressed length

This is the ONLY change from the parent. All content generation, auth-state logic, endpoint routing, and analysis logic remain identical.

---

## 3. Measurement plan

### 3.1 Primary metric: decompressed body-only discrimination

For each (content_type, size, endpoint) combination:

```
discrimination = 1 - (mean_within_state_hash_variation / total_hash_variation)
```

More precisely: compute SHA256 of `(status, decompressed_body_sha256, '')` for each request. Group by auth state. Compute pairwise Jaccard distance between hash sets. Discrimination = 1 - mean Jaccard distance.

Simplified: discrimination = fraction of pairwise state comparisons where hash sets are disjoint.

### 3.2 Secondary metrics

1. **Compressed body-only discrimination:** Same as above but using compressed wire bytes. Expected to be lower than decompressed (grandparent showed 0.2789 vs 0.5 on /userinfo).

2. **Status-only discrimination:** Fraction of state pairs distinguishable by HTTP status alone. Structural ceiling = 0.5 for /userinfo (2 states return 200, 2 return 401).

3. **Decompressed hash variation per state:** unique_count, total, all_same per state. Determinism requires all_same=true for all states.

4. **Brotli quality diversity:** Number of unique compressed hashes per state across quality levels 4-8. Expected: 2 at 1KB (grandparent), potentially more at 10KB/100KB.

5. **Decompression latency:** Time per decompression operation, measured at each size. Critical for production cost assessment.

6. **Algorithm equivalence:** |brotli_discrimination - gzip_discrimination| per content type x size.

7. **Compression verification:** Content-Encoding header value for each response. MUST NOT be 'none' — if any observation has Content-Encoding='none', the server fix failed and the experiment is MEASUREMENT_INVALID.

### 3.3 Baselines

| Baseline ID | Description | Expected |
|---|---|---|
| B-RANDOM | SHA256 on random 32-byte fingerprints | 0.0 |
| B-PARENT-JSON-1KB | Grandparent JSON discrimination at 1KB | 0.5 / 0.8333 |
| B-ALGORITHM-EQUIVALENCE | |brotli - gzip| per condition | < 0.1 |

### 3.4 Controls

| Control ID | Condition | Expected | Failure Meaning |
|---|---|---|---|
| C_COMPRESSION_ACTIVE | Content-Encoding != 'none' for all compressed responses | true | Server fix failed — re-run MEASUREMENT_INVALID |
| C_DECOMPRESSION_DETERMINISM | all_same=true for all states x types x sizes | true | Decompression is non-deterministic → mechanism broken |
| C_NULL_CONTROL | B-RANDOM ~ 0.0 for all conditions | 0.0 | Spurious structure from artifacts |
| C_BROTLI_QUALITY_SCALING | Unique compressed hashes at 100KB > unique at 1KB for HTML | true | Quality diversity is size-dependent (resolves grandparent limitation) |
| C_NO_PIPELINE_ERRORS | 0 errors across all requests | 0 | Infrastructure failure |
| C_REGRESSION_JSON | JSON discrimination at 1KB >= 0.3 | >= 0.3 | Regression from grandparent |

---

## 4. Decision rule (frozen)

### SURVIVES_CURRENT_TEST if ALL of:

1. Content-Encoding != 'none' for all compressed observations (C_COMPRESSION_ACTIVE)
2. JSON decompressed body-only discrimination >= 0.3 at all 3 sizes (regression)
3. HTML decompressed body-only discrimination >= 0.3 at all 3 sizes
4. XML decompressed body-only discrimination >= 0.3 at all 3 sizes
5. decompressed_hash_variation all_same=true for all content types x sizes x states
6. B-RANDOM = 0.0 for all conditions
7. |brotli - gzip| < 0.1 for all content types x sizes (algorithm equivalence)

### FALSIFIED-IN-SETTING if:

- Any non-JSON content type has decompressed discrimination < 0.3 at any size

### MEASUREMENT_INVALID if:

- Infrastructure failure prevents valid measurements (server won't start, compression library unavailable, etc.)
- C_COMPRESSION_ACTIVE fails (any observation has Content-Encoding='none')

---

## 5. Consequences

### Positive outcome (SURVIVES)

- Claim ceiling advances: "1KB JSON under synthetic CDN-noise proxy" → "multi-format (JSON/HTML/XML) multi-size (1KB-100KB) under localhost compression"
- Real-CDN testing becomes the sole remaining blocker for C-MEAS-VALID
- Product team can invest in CDN infrastructure knowing mechanism is format-robust
- Brotli quality diversity at 100KB may resolve the "effective diversity is 2 variants" limitation

### Negative outcome (FALSIFIED)

- Decompression-normalization is format-dependent, not format-invariant
- Product team must either restrict to JSON-only or investigate format-specific issues
- Real-CDN testing investment is premature
- Next experiment: investigate why HTML/XML fail (broader error body overlap? different brotli behavior? decompression pipeline issue?)

---

## 6. Validity threats

1. **Synthetic content types:** HTML and XML are structurally realistic but hand-authored. Real web pages have scripts, styles, dynamic content. However, the mechanism operates on decompressed bytes, not parsed structure, so structural realism is less critical than byte-level diversity.

2. **3-way error collapse is preserved:** All content types use the same auth-state pattern. This caps discrimination at 0.5 for /userinfo-equivalent. This is a property of the mock server, not the mechanism.

3. **No CDN noise:** This experiment isolates content-type effects. If content-type results are positive, a follow-up with CDN noise + non-JSON would be the natural next step.

4. **Brotli library version:** The system brotli library (Python brotli) may behave differently from CDN brotli implementations. This is a known limitation accepted across all runtime experiments.

5. **Payload size control via padding:** Repeated blocks may have different compressibility characteristics than natural content. However, the mechanism tests decompressed-body discrimination, not compression efficiency.

6. **Re-run validity:** This is a re-run of a MEASUREMENT_INVALID experiment with a server fix. The frozen scientific design is unchanged. The only modification is infrastructure-level (server actually compresses). This is methodologically legitimate: the parent's design was never executed, so no outcome data exists to bias this run.

---

## 7. Analysis script requirements

The execution script must:

1. Start a mock OAuth2 server returning JSON/HTML/XML responses for 4 auth states
2. **FIX: The server MUST actually compress response bodies using brotli (quality 4-8) and gzip, and set Content-Encoding headers accordingly**
3. For each content type x size x state x baseline:
   - Make N=20 requests
   - Record: status, headers, raw compressed bytes, decompressed bytes, Content-Encoding
   - Apply decompression-normalization: SHA256(status, decompressed_body)
   - Compute discrimination metric
4. Compute all controls and baselines
5. Output raw_observations.json, result.json, and analysis summary
6. Measure decompression latency per response
7. Use seed=44 for request ordering
8. No CDN-noise proxy
9. **Verify: no observation may have Content-Encoding='none' (would indicate server fix failure)**

---

## 8. Open questions this experiment does NOT answer

- Does decompression-normalization survive real CDN infrastructure? (requires external infrastructure)
- What is production-scale latency? (requires N>1000, real network)
- Does it work on binary content types? (requires binary payload design)
- What happens with incorrect/missing Content-Encoding? (requires error injection)
- Does it work when Content-Encoding is double-encoded? (requires attack scenario)
