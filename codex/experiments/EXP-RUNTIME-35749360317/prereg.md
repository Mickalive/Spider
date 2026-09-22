# EXP-RUNTIME-35749360317 — Preregistration

**Experiment ID:** EXP-RUNTIME-35749360317  
**Lane:** Runtime  
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)  
**Director Mandate:** CONTINUE — Does the HTTP fingerprint substrate discriminate same-status body-only drift where response status is identical (200 vs 200) but response bodies differ via server-side permission/content variation (Content-Length varies, body semantics differ), isolating body-only signal with status confound removed and yielding the complementary non-vacuous full>status test to the header-only success (full 1.0 > body/status 0.0, Content-Length isolation holds), plus writable permission-level and session-invalidation controls that produce discriminating positive (discrimination >=0.7) and valid null (FP<0.05) on localhost Flask HS256?  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35741906498/handoff.json (sha256:6e8a1eaa717dc59bfcdf4c0d464072ef1db429dffabe7bc2eef0d01ca56f6039)  
**Date:** 2026-09-22  

---

## 1. Question

Does the HTTP fingerprint substrate discriminate same-status body-only drift where response status is identical (200 vs 200) but response bodies differ via server-side permission/content variation (Content-Length varies, body semantics differ), isolating body-only signal with status confound removed and yielding the complementary non-vacuous full>status test to the header-only success (full 1.0 > body/status 0.0, Content-Length isolation holds), plus writable permission-level and session-invalidation controls that produce discriminating positive (discrimination ≥0.7) and valid null (FP<0.05) on localhost Flask HS256?

This is the binding Director question for this CONTINUE experiment (tunnel flag true but next result directly changes trust in substrate interpretation). The parent handoff's `next_question` is advisory continuity evidence consistent with this mandate and is preserved, but the Director's target claim, dependencies, and comparative reasoning govern design. Cognitive reset applied — design evaluated from portfolio breadth, not merely local header-only replication.

---

## 2. Hypothesis

The HTTP fingerprint substrate — `hash(status_code || body_bytes || sorted_filtered_standard_headers)` with `EXCLUDED_HEADERS = [Date, Server, X-Request-Id]` identical to parent EXP-RUNTIME-35741906498 and grandparent EXP-RUNTIME-35697043449 (`research/experiments/EXP-RUNTIME-35697043449/run_experiment.py:compute_fingerprint`) — will on localhost Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL (Werkzeug 3.1.8, Python 3.12.14, 127.0.0.1, SEED 44, jitter 50-150ms):

- **Discriminate same-status body-only drift:** `H1: discrimination_full(A vs C) > 0.5` (expected 1.0 deterministic) where A and C both return `200` but byte-different JSON bodies via a writable server-side `body_config/content_variant` change; `H2: discrimination_body_only(A vs C) > 0.5` and on at least one per-body isolation (A vs B).
- **Prove status confound removed:** `H3: discrimination_status_only = 0.0` on all same-status body-only comparisons (200 vs 200). Status-only must not carry signal when status is held constant.
- **Demonstrate complementary non-vacuous full>status:** `H4: discrimination_full > discrimination_status_only` strictly (e.g., 1.0 > 0.0), the body-only complement to header-only's `full 1.0 > max(body 0.0, status 0.0)`. Prior body+status conditions were vacuous `1.0 >= 1.0`; this is the other non-vacuous branch where body is the sole varying modality.
- **Maintain null validity:** `H5: discrimination_full(null) = 0.0`, bootstrap 95% CI contains 0.0, point estimate ≤0.05 (FP<0.05) when resampling the same body state.
- **Body semantics manifest correctly:** `H6: Content-Length varies` (31 ≠ 52 ≠ 95) and body SHA-256 distinct across A/B/C, while non-Content-Length filtered headers (`Cache-Control, ETag, Vary, Set-Cookie`) remain identical across A/B/C — proving body-only not independent-header drift (complement to header-only's Content-Length identity). `B-HEADERS-NO-CLEN` (filtered headers minus Content-Length) must be 0.0; `B-HEADERS-ONLY` may be 1.0 solely via body-correlated Content-Length (documented, not a failure).
- **Writable matrix completion:** `H7/H8: discrimination_full ≥0.7` on writable permission-level (reader body 200 vs admin body 200, same as H1) and on classic writable controls — permission escalation `403 vs 200` via `UPDATE users SET role` and session invalidation `401 vs 200` via `DELETE sessions` — each with valid null FP<0.05. This satisfies the registry next_gate's writable/auth/session drift requirement and the Director's explicit `>=0.7 / <0.05` thresholds.

If all hold, same-status body-only drift is measurable and the localhost C-MEAS-VALID discrimination matrix is complete (header-only + body-only + maximally-distinct + null). If any fails, body-only drift is not discriminated by this fingerprint in this setting.

---

## 3. Inherited State — What is Established, Rejected, Unknown

From `handoff.json` of EXP-RUNTIME-35741906498 (preserved four-way distinction, parent_handoff_disposition USE):

**Established (bounded, audit PASS, narrowed ceiling):**
- HTTP fingerprint `SHA256(status || body_bytes || sorted_filtered_headers)` with `EXCLUDED_HEADERS={Date,Server,X-Request-Id}` deterministically discriminates header-only server-state changes with Jaccard 1.0 when status is 200 vs 200 and bodies are byte-identical (JSON `{"data":"hello","version":1}` 31 bytes SHA `d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34`, Content-Length 31 identical) on localhost Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL + Werkzeug 3.1.8 Python 3.12.14 at 127.0.0.1:19848 single sequential client SEED 44 jitter 50-150ms nominal N=20 per state effective distinct N=1 per state per source degenerate CI [1.0,1.0]/[0.0,0.0] (audit PASS, recomputed 0 mismatches, 180 lines all 200, 15 batch_state_log verified). Claim ceiling audit-certified, still EXPERIMENTAL, not VALIDATED/PRODUCT_CORE.
- Header-only discrimination is not body- or Content-Length-correlated: `B-STATUS-ONLY 0.0` and `B-BODY-ONLY 0.0` on all comparisons (A vs E combined 4 headers, A vs B Cache-Control only, A vs C ETag only, A vs D Set-Cookie only) while `B-HEADERS-ONLY 1.0`; C6 Content-Length identity holds. First non-vacuous C4: `full 1.0 > max(status 0.0, body 0.0)` strictly.
- Per-header isolations each alone sufficient: Cache-Control alone 1.0, ETag alone 1.0, Set-Cookie alone 1.0 on full and headers-only; null controls stable: `null_A1 vs null_A2` 0.0 CI [0.0,0.0] and exploratory `null_E1 vs null_E2` 0.0 on all four sources. Date varies 20 unique values and Server constant correctly excluded with 0 leakage.
- Parent established remains: maximally-distinct writable controls permission escalation (403 vs 200+body) and session invalidation (200 vs 401) Jaccard 1.0 deterministic with null 0.0 on localhost Flask (EXP-RUNTIME-35697043449). Combined with header-only plus nginx HIT/SWR/SIE 960/960 byte-identical decompression validation (EXP-RUNTIME-35611612543), substrate covers body-identical header-different and header-identical body-different branches at localhost synthetic level — but the body-only same-status half (200 vs 200 with different body) was not tested with isolated status.

**Rejected (bounded):**
- Header-only server-state drift is undetectable when bodies and status identical, or detectable only via body-correlated Content-Length — falsified: `full 1.0` and `headers_only 1.0` with Content-Length 31 constant and body SHA identical rejects this (C1-C6 PASS, audit PASS). Bounded to localhost Flask dev server with writable `header_config` and filtered headers {Cache-Control, ETag, Set-Cookie, Vary} included.
- Full-vector adds no marginal information beyond body/status baselines (prior vacuous C4) — falsified for header-only condition where `full 1.0` strictly exceeds `body 0.0` and `status 0.0`; remains vacuous for prior maximally-distinct body+status conditions where body alone already 1.0.

**Unknown (this experiment targets the first):**
- Does substrate discriminate same-status body-only drift (200 vs 200 with different body content via permission/content variation) with status isolated (`status-only 0.0`, `body-only >0.5`, `full > status` strictly) — parent `unresolved[3]` still open, targeted by this `next_question`
- Does header-only discrimination hold on production middleware (Django/Express/FastAPI, gunicorn/nginx, CDN, load balancer) with realistic header handling — out of scope for this localhost complement
- Does discrimination hold under concurrency, HTTP/2, TLS, multi-client, or non-deterministic header emission where bootstrap CI becomes non-degenerate and sensitivity ordering emerges
- Does Vary header alone discriminate when isolated — tested only as combined E state in parent, not single-header isolation
- Does header discrimination generalize to other header values/magnitudes, header ordering, whitespace/case folding beyond 5 tested filtered header JSONs
- Does distributed or CDN-cached header handling preserve header-only discrimination for C-FRESHNESS/C-DELTA-REPAIR beyond localhost
- Per-header signal strength gradient when headers vary with smaller/multiple concurrent changes (ceiling 1.0 masks sensitivity differences)

**Do not assume (explicitly unsafe):**
- C-MEAS-VALID is VALIDATED or PRODUCT_CORE — audit PASS supports EXPERIMENTAL only; degenerate CI effective N=1, localhost bound
- Localhost Flask dev server results generalize to production WSGI (gunicorn), nginx, CDN, or distributed SQLite replication
- Bootstrap CI [1.0,1.0] or [0.0,0.0] reflects high sampling precision — degenerate because all 20 fingerprints per state byte-identical (effective N=1); jitter 50-150ms had no effect
- Full-vector always adds marginal value beyond single-field baselines — true only for header-only and (if this experiment passes) body-only where status 0.0; prior maximally-distinct conditions remain vacuous where body alone already 1.0
- B-HEADERS-ONLY 1.0 proves header signal non-trivial in all deployments — architecturally forced that any included-header change changes hash; test value was isolating from Content-Length/body correlation and proving status/body 0.0
- Header ordering, whitespace, case folding, or multiple Set-Cookie handling is robust — tested only single Set-Cookie value and fixed sort_keys
- C-FRESHNESS and C-DELTA-REPAIR unblocked for distributed/production testing — unblocked only for localhost synthetic header-only drift; production freshness/delta-repair remains blocked pending this body-only complement and production middleware tests
- Vary header delta and per-header signal gradient characterized — Vary only tested inside combined E, all three isolations hit ceiling 1.0 so no ordering measured

This experiment directly tests the first unknown while explicitly not assuming the `do_not_assume` items. Distributed/production generalization remains out of scope and is disclosed as not tested.

---

## 4. Server Design

### 4.1 Testbed Architecture

```
Flask 3.1.3 + PyJWT 2.14.0 (HS256) + SQLite WAL (or in-memory dict with same commit semantics) + Werkzeug 3.1.8 Py 3.12.14
  ├── POST /admin/set_body_variant   — privileged, writes body_config/content_variant (requires admin JWT; commits before 200)
  ├── POST /admin/set_headers        — retained from parent, used once to fix header_config constant across body-only batches
  ├── POST /admin/set_role           — UPDATE users SET role (for classic 403 vs 200 permission escalation control)
  ├── POST /admin/invalidate_session — DELETE sessions (for classic 401 vs 200 session control)
  ├── GET  /resource                 — authenticated GET, returns 200 + JSON body per body_config/role, headers per header_config
  └── GET  /protected                — smoke check retained (not primary measurement)
```

`body_config` table (or dict) schema: `variant TEXT PRIMARY KEY, body_json TEXT` — initialized to `variant='A'` body `{"data":"hello","version":1}`. `POST /admin/set_body_variant` updates the row and commits (SQLite WAL COMMIT) before returning 200; subsequent `GET /resource` reads the committed value. This is a writable server-side state change parallel to parent's `POST /admin/set_headers` but with headers held constant and bodies varying — the exact complement.

Authentication: JWT with `sub` claim only, role looked up from SQLite (same as parent). For body-only comparisons, all `GET /resource` use the same valid JWT (role irrelevant); body variation is driven by `body_config`, not by token, so status stays 200. For permission-filtered variant (P1), two tokens (reader vs admin) may be used with `body_config` fixed to test role-filtered body while still 200 vs 200.

`header_config` fixed once before body-only batches: `Cache-Control: max-age=3600`, `ETag: W/"fixed-aaa-111"`, `Vary: Accept-Encoding`, no `Set-Cookie`, `Content-Type: application/json`. This constant is verified by SELECT before each body batch and logged in `batch_state_log.jsonl`.

### 4.2 Body States

| State | Body JSON (canonical, sort_keys=True) | body_len | Body SHA-256 (expected distinct) | Status | Non-CLEN Headers |
|-------|----------------------------------------|----------|-----------------------------------|--------|-------------------|
| **A baseline** | `{"data":"hello","version":1}` | 31 | `d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34` | 200 | `Cache-Control:max-age=3600, ETag:W/\"fixed-aaa-111\", Vary:Accept-Encoding, Content-Type:application/json` (constant) |
| **B reader** | `{"data":"hello","items":["a","b"],"role":"reader","version":1}` | ~52 (exact logged) | distinct from A/C | 200 | identical to A |
| **C admin** | `{"admin_note":"sensitive:42","count":42,"data":"hello","items":["a","b","c"],"role":"admin","version":1}` | ~95 (exact logged) | distinct from A/B | 200 | identical to A |

**Classic writable controls (same server lifecycle, separate comparisons):**
- **P_403** permission escalation: `UPDATE users SET role='viewer'` then `GET /resource` as viewer returns `403` with body `{"error":"forbidden"}` vs viewer upgraded to `admin` returns `200` with body C — discrimination ≥0.7 expected, status 403 vs 200.
- **S_401** session invalidation: valid session `GET /resource` 200 body A vs `DELETE sessions` then same token returns `401` body `{"error":"unauthorized"}` — discrimination ≥0.7 expected, status 401 vs 200.

**Verification for each state:** after `POST /admin/set_body_variant` (or set_role/invalidate), a `SELECT body_config, header_config` confirms commit; then each of N=20 `GET /resource` observations captures status, body_bytes, body_sha256, body_len, Content-Length header, raw headers; body SHA inequality across A vs C and equality within null verified before discrimination computed. Non-CLEN header identity across A/B/C verified (all values equal); Content-Length must equal body_len and differ across states.

Bodies are intentionally not byte-identical; holders are chosen so that B and C contain strictly more fields and semantic content (permission-filtered vs admin) with measurably different lengths, ensuring `B-BODY-ONLY` must be 1.0 if bodies differ.

### 4.3 Why This Comparand Set

- **Primary comparison A vs C** maximizes body distance (31 vs ~95 bytes, 1 field vs 6 fields, reader vs admin semantics) — most likely to be detected if substrate has any body sensitivity, and Content-Length delta is largest.
- **Per-body isolation A vs B** tests whether a smaller body perturbation (31→52, single extra role field) already suffices; requiring at least one per-body isolation prevents a combined-only artifact and mirrors parent's ≥2/3 per-header rule minimalistically (2 states, need 1 of 1 isolation for this smaller matrix).
- **Content-Length varies by design** (31 vs 52 vs 95) — deliberately the opposite of header-only's C6 identity — so `B-HEADERS-ONLY` will be 1.0 solely via body-correlated Content-Length, and `B-HEADERS-NO-CLEN` must be 0.0 to prove no independent header drift. This demonstrates body semantics manifest in the transport header that prior work worried confounded header detection.
- **Classic controls P_403 and S_401** retained to verify substrate stability at the ≥0.7 threshold the Director explicitly requires for writable/auth/session drift on HS256 localhost; they are measured in the same run to ensure a single server lifecycle covers the full matrix without cross-run environmental drift.

---

## 5. Measurement

### 5.1 Observation Vector

Per request:
- HTTP status code (int)
- Response body exact bytes + SHA-256 + length (int)
- Raw standard headers dict (all headers) + filtered headers dict (minus EXCLUDED_HEADERS) + headers_no_clen dict (filtered minus Content-Length)
- `Content-Length` header value (string, must equal body_len when present)
- Response time (informational)
- Fingerprint variants: `full = hash(status || body_bytes || sorted_filtered_headers)`, `status_only = hash(status)`, `body_only = hash(body_SHA256)`, `headers_only = hash(sorted_filtered_headers)`, `headers_no_clen = hash(sorted_filtered_headers_without_ContentLength)` — same functions as parent `run_experiment.py:compute_fingerprint`, `compute_fingerprint_status_only`, etc.

### 5.2 Discrimination Metric

Jaccard distance between fingerprint sets:

```
discrimination = 1.0 - |set_A ∩ set_B| / |set_A ∪ set_B|
```

Sets built from N=20 fingerprints per state. With deterministic responses expected set size = 1 per state, discrimination is 1.0 if any fingerprint bit differs, 0.0 if identical. Bootstrap 95% CI (B=1000) computed by resampling fingerprint sets with replacement, but reported as degenerate when set size =1 (expected). Effective distinct N reported. Thresholds: `>0.5` for body-only positive, `=0.0` for status null, `≥0.7` for classic writable controls per Director, `≤0.05` for null FP.

### 5.3 Baselines

| ID | Fingerprint source | Expected on A vs C (200 vs 200, bodies differ) | Expected on P_403/S_401 (403/401 vs 200) | Purpose |
|----|--------------------|-----------------------------------------------|------------------------------------------|---------|
| B-STATUS-ONLY | status code alone | 0.0 (status identical) | 1.0 (status differs) | Strong null for body-only: proves status not the signal when held constant |
| B-BODY-ONLY | body SHA-256 alone | >0.5 (expected 1.0) | 1.0 (bodies differ) | Positive: body carries signal when status constant |
| B-HEADERS-ONLY | filtered headers only (incl. Content-Length) | >0 (expected 1.0) via Content-Length only | 0.0 or 1.0 depending on header diff | Body-correlated header: shows Content-Length tracks body |
| B-HEADERS-NO-CLEN | filtered headers minus Content-Length | 0.0 (no independent header drift) | — | Isolation: proves non-CLEN headers constant, so header-only signal not independent |

### 5.4 Sample Size

- Body-only: A×20, B×20, C×20 = 60
- Body nulls: N1 A1×20 + A2×20 =40 (primary), exploratory N2 C1×20+C2×20 reported separately if run (+40 optional)
- Classic controls: P_403 (403×20 + 200×20) =40, S_401 (401×20 + 200×20)=40
- Total raw lines nominal 140 (A/B/C + N1 + P_403 + S_401) = 140; with optional N2 =180. Matches parent's 140-180 range. Jitter 50-150 ms uniform, SEED=44.
- Effective distinct fingerprints expected 3 (A,B,C) +1 per null set (1 each) =6 nominal, degenerate CI disclosure required.

Power: deterministic Jaccard 1.0 needs N=1 to detect; N=20 provides operational replication and audit recomputation without inferential power concerns; threshold `>0.5` is 0.5 away from null 0.0, so even with degenerate CI discrimination is unambiguously above threshold when fingerprints differ.

---

## 6. Decision Rule (Frozen)

**SUPPORTS** iff ALL hold (no post-hoc weakening):

1. **C1_FULL_BODY_DRIFT:** `discrimination_full(A vs C) > 0.5` (expected 1.0 deterministic) with status=200 verified on all 40 observations in A and C, body SHA-256 distinct across A vs C, Content-Length differs (31 ≠ ~95), non-CLEN filtered headers identical.
2. **C2_BODY_ONLY_SIGNAL:** `discrimination_body_only(A vs C) > 0.5` (expected 1.0) AND `>0.5` on A vs B per-body isolation; `discrimination_headers_no_clen(A vs C) = 0.0` (no independent header drift). `discrimination_headers_only` may be 1.0 solely via Content-Length — documented, not a failure — but must be 0.0 when Content-Length excluded.
3. **C3_STATUS_ISOLATED:** `discrimination_status_only = 0.0` on A vs C and on A vs B (and on each body-only isolation). Any >0.0 fails isolation (not same-status).
4. **C4_FULL_EXCEEDS_STATUS_NONVACUOUS:** `discrimination_full(A vs C) > discrimination_status_only(A vs C)` strictly greater (e.g., 1.0 > 0.0). Equality at ceiling (1.0 ≥1.0) as in prior vacuous body+status conditions is defined as failure for this complement test.
5. **C5_NULL_NO_FALSE_POSITIVE:** Null N1 (STATE_A resampled, two independent N=20 batches, no write between) `discrimination_full = 0.0` with 95% bootstrap CI containing 0.0 and point estimate ≤0.05 (FP<0.05); additionally `discrimination_status_only =0.0` and `discrimination_body_only =0.0` on N1. Exploratory N2 (STATE_C resampled) also expected 0.0 but not gating unless N1 fails.
6. **C6_CONTENT_LENGTH_VARIES_AND_HEADERS_CONSTANT:** `Content-Length` header values differ across A/B/C proportional to body_len (31 ≠52 ≠95) and `body_len` differs and body SHA-256 distinct, while non-Content-Length filtered headers (`Cache-Control, ETag, Vary, Set-Cookie`) identical across A/B/C and `Content-Length == body_len` on each observation. Confirms body semantics differ and signal not via independent header drift.
7. **C7_WRITABLE_PERMISSION_LEVEL:** Writable permission-level controls achieve `discrimination_full ≥0.7` — (a) body-filtered permission `reader 200 vs admin 200` (A vs C, same as C1, ≥0.7 automatically if C1 passes at 1.0) and (b) classic permission escalation `403 vs 200` via `UPDATE users SET role` with committed SQLite write, `discrimination_full ≥0.7`, body SHA distinct, status 403 vs 200 verified; same-state 403 null `=0.0` CI contains 0.0 ≤0.05.
8. **C8_WRITABLE_SESSION_INVALIDATION:** Writable session-invalidation control `401 vs 200` via `DELETE sessions` achieves `discrimination_full ≥0.7` with status 401 vs 200 verified, body SHA distinct; same-state 401 null `=0.0` CI contains 0.0 ≤0.05.

If any of C1–C8 fails → **FALSIFIED-IN-SETTING** with specific failing condition documented (which body signal missing, which isolation violated, which threshold, or which null false positive).

If infrastructure prevents verification of status/body/header identity or writable commits (server crash, SQLite commit not verified by SELECT, non-200 where 200 required for body-only, body write not committed, fingerprint computation error, header_config drift) → **MEASUREMENT_INVALID** with category (e.g., `SERVER_CRASH`, `COMMIT_NOT_VERIFIED`, `STATUS_MISMATCH`, `BODY_NOT_DISTINCT`, `HEADER_DRIFT`), retryability, and diagnostic logged. Degenerate bootstrap CI [1.0,1.0]/[0.0,0.0] is EXPECTED deterministic behavior and is not measurement invalidity when set sizes are 1 and validity checks pass.

---

## 7. Controls Summary

| Control | ID | Type | Pass threshold | Evidence required |
|---------|----|------|----------------|-------------------|
| Full body drift | C1 | positive | >0.5, expect 1.0 | A vs C full Jaccard=1.0, 200 vs 200, body SHA ≠, CLEN ≠ |
| Body-only signal | C2 | positive + isolation | body_only >0.5 on A vs C + A vs B; headers_no_clen =0.0 | body_only Jaccard, headers_no_clen Jaccard |
| Status isolated | C3 | strong null | =0.0 on A vs C and A vs B | status_only Jaccard 0 |
| Full > status | C4 | non-vacuous superiority | strictly > (1.0 >0.0) | full vs status_only on A vs C |
| Null stability | C5 | null | =0.0, CI contains 0, ≤0.05 | N1 full Jaccard 0, CI [0.0,0.0] |
| CLEN varies, headers constant | C6 | validity | CLEN ≠, SHA ≠, non-CLEN = | header values, body_len, SHA |
| Permission writable | C7 | positive ≥0.7 + null | full ≥0.7 on 200vs200 +403vs200; nulls 0.0 | P controls Jaccard, SELECT commit |
| Session writable | C8 | positive ≥0.7 + null | full ≥0.7 on 401vs200; null 0.0 | S control Jaccard, SELECT commit |

---

## 8. Validity Threats and Mitigations

1. **Body not committed / stale read:** `POST /admin/set_body_variant` not visible to next `GET` → mitigate by SQLite `SELECT body_config` verification + `COMMIT` before 200; log `body_config` and `header_config` before each batch in `batch_state_log.jsonl`.
2. **Body serialization variance (key order, whitespace):** mitigated by fixing `json.dumps(sort_keys=True, separators=(',',':'))` server-side and verifying SHA-256 inequality before discrimination; Content-Length must equal `len(body_bytes)`.
3. **Content-Length not varying or header-confounded:** bodies deliberately different lengths (31/52/95) so Content-Length must vary; C6 enforces `CLEN ≠` and `body_len` equality; `headers_no_clen` must be 0.0 to prove no independent header drift.
4. **Status not 200:** any 500/401/403 during body-only batches fails validity for that comparison; mitigated by using same valid JWT for A/B/C and verifying status 200 on all 60 observations before computing discrimination.
5. **Excluded headers drift:** `Date` varies per request but is excluded; include only filtered headers in fingerprint; verify `EXCLUDED_HEADERS` constant and log raw headers.
6. **Header_config drift during body batches:** `Cache-Control/ETag/Vary` could be mutated by leftover state → set `header_config` once before body batches and verify identical SELECT before each body batch; any non-CLEN difference fails C6.
7. **Degenerate CI misread as precision:** disclose effective distinct N=1, treat CI as deterministic, do not claim narrow inferential precision; same mitigation as parent.
8. **Set-Cookie or Vary leakage:** ensure `Set-Cookie` absent and `Vary` constant; log raw header list and hashed sorted representation.
9. **Port collision / stale server:** discover free port, start fresh server per run, record port in provenance, kill on exit; SQLite file fresh per run.
10. **Threshold confusion (≥0.7 vs >0.5):** C1/C2 use >0.5 (sensitive body-only), C7/C8 use ≥0.7 per Director for writable/auth drift (slightly stricter for classic controls); document exact value and CI.
11. **Workload conflation:** body-only and classic 403/401 controls run sequentially in one lifecycle to avoid cross-run port/version drift; order fixed (body-only A/B/C → N1 → P_403 → S_401) and logged.

---

## 9. Consequences

**Positive (all C1–C8 pass):** C-MEAS-VALID ceiling expands to include same-status body-only drift — the complementary half of the localhost discrimination matrix to header-only (EXP-RUNTIME-35741906498). This proves the HTTP fingerprint substrate detects both independent header mutations (bodies identical, 31 bytes constant) and independent body mutations (status 200 constant, non-CLEN headers constant, Content-Length varies) with deterministic Jaccard 1.0, null 0.0, and complementary non-vacuous `full > status` (1.0 > 0.0). Together with classic writable permission `403 vs 200` ≥0.7 and session `401 vs 200` ≥0.7 and nginx 960/960 byte-identical decompression, the full localhost matrix (header-only, body-only same-status, status-varying maximally-distinct, null stability) is complete for Flask dev server HS256. Unblocks C-FRESHNESS (graph can trust detection of content-only drift without status change) and C-DELTA-REPAIR (local body perturbation measurement) for localhost synthetic testing with both branches validated. Still bounded: does NOT promote to VALIDATED or PRODUCT_CORE; localhost Flask dev server only, no production WSGI/nginx/CDN, no concurrency/HTTP2/TLS, no distributed SQLite replication, degenerate CI, body/header value magnitudes limited to 3 variants. Director's `CONTINUE` completes with matrix closure, enabling a `PIVOT` to distributed C-FRESHNESS or BrowserGym adapter next.

**Negative (any C1–C8 fails):** Same-status body-only drift not discriminated (or isolation violated, or null false positive, or Content-Length not varying, or permission/session below 0.7). The substrate is then bounded to header-only + status-varying conditions; body semantics that preserve 200 status but change JSON content (permission-filtered fields, `Content-Length` varying) are unmeasurable with current `status+body+filtered_headers` hashing. C-FRESHNESS cases where response bodies vary due to permission filtering or content variation without status change, and C-DELTA-REPAIR cases where local content perturbation keeps status 200, remain unmeasurable with this substrate and require alternative (explicit body diff, augmented hashing, production body handling) or larger body magnitudes. Negative result is equally high-information: it bounds the substrate to metadata-only drift and prevents false trust in body-only freshness guards, directly changing the product decision to require a different body-observation substrate before scaling to distributed or production experiments. It also keeps C-MEAS-VALID at EXPERIMENTAL with narrower ceiling (header-only only), consistent with the portfolio assessment that Graph's freshness tuning was `LOCAL` only.

Both outcomes are high-information and will be consumed by the Codex as the second non-vacuous branch needed before any production or distributed generalization claim.

---

## 10. What is NOT Tested (Scope Boundaries)

- Production WSGI (gunicorn), nginx, CDN, load balancer, concurrent multi-client, HTTP/2, TLS, browser DOM / AgentLab / BrowserGym observation — explicitly out of scope; localhost Flask dev server only.
- Distributed SQLite replication / Redis shared session for C-FRESHNESS `C1 TN=0.667` fix — not tested here; localhost single-node WAL only.
- Header-only value variations beyond fixed `Cache-Control:max-age=3600 / ETag:W/"fixed-aaa-111" / Vary:Accept-Encoding` and header ordering/whitespace/casing sensitivity — held constant, not tested.
- Vary isolation, per-header gradient, or other body JSON magnitudes beyond 31/52/95 — kept minimal to isolate body-only signal, not to profile sensitivity.
- End-to-end cost, latency, tokens, LLM inheritance, cross-site holdout — not measured.
- Freshness correlation `r` or delta-repair amortization — graph-level claims, not runtime substrate.

---

## 11. Execution Checklist for EXECUTE

- Must implement `run_experiment.py` with fingerprint functions byte-identical to `research/experiments/EXP-RUNTIME-35741906498/run_experiment.py:compute_fingerprint` (and `compute_fingerprint_status_only`, `compute_fingerprint_body_only`, `compute_fingerprint_headers_only`), plus `compute_fingerprint_headers_no_clen`, for audit recomputation.
- Must log `raw_observations.jsonl` (140 lines nominal: 7 batches ×20 = A/B/C 60 + N1 40 + P_403 20+20? adjust to 140: A/B/C 60 + N1 40 + P_403 20 + S_401 20 =140; if splitting P_403/S_401 as paired comparisons total raw lines = A 20 + B 20 + C 20 + N1_A1 20 + N1_A2 20 + P_403_200 20 + P_403_403 20? Actually P and S each need two states: counting carefully, total is 180 if both classics included as two-state pairs; disclose nominal vs effective and keep batch_state_log consistent) with fields: `state, status, body_sha256, body_len, content_length_header, headers_filtered_json, headers_raw_json, headers_no_clen_json, fingerprint_full, fingerprint_status, fingerprint_body, fingerprint_headers, fingerprint_headers_no_clen, timestamp`.
- Must produce `experiment_result.json` (derived) and `result.json` (canonical per `research/EXPERIMENT_PACKET.md` §4) with metrics: `body_drift_full_AvsC`, `body_drift_body_only_AvsC`, `body_drift_status_only_AvsC`, `body_drift_headers_only_AvsC`, `body_drift_headers_no_clen_AvsC`, `body_drift_full_AvsB`, `cache_headers?` etc., plus `null_control_full_N1`, `null_control_body_N1`, `null_control_status_N1`, `classic_perm_full`, `classic_sess_full`, and controls C1–C8 pass/fail with bootstrap CI and effective N.
- Must record `provenance.json` with env (Flask 3.1.3 / PyJWT 2.14.0 / SQLite 3.45.0 WAL / Werkzeug 3.1.8 / Python 3.12.14), port, SEED 44, EXCLUDED_HEADERS, body_config variant bodies and lengths and SHAs, header_config constant values per batch, artifact SHA-256, git commit, run id.
- Must produce `batch_state_log.jsonl` with per-batch `SELECT body_config, header_config` commit verification (15+ entries).
- Must not inspect outcomes before freeze; frozen `spec.json`/`prereg.md`/`freeze.json` are immutable after freeze; any deviation after seeing data is exploratory and must be labeled as such.
- Must preserve stable control IDs `C1`–`C8` and metric IDs `body_drift_full_AvsC`, `B-STATUS-ONLY`, `B-BODY-ONLY`, `B-HEADERS-ONLY` for AUDIT/DIRECTOR transmission per `research/EXPERIMENT_PACKET.md` §1.

