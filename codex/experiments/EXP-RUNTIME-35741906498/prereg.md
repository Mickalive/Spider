# EXP-RUNTIME-35741906498 — Preregistration

**Experiment ID:** EXP-RUNTIME-35741906498  
**Lane:** Runtime  
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)  
**Director Mandate:** CONTINUE — isolate header-only drift from vacuous body/status confound  
**Parent Handoff:** research/experiments/EXP-RUNTIME-35697043449/handoff.json (sha256:d3144036f4663aabfd22b0fc44386f8d067f3da8cf3ced65b53a400e270d2f43)  
**Date:** 2026-09-22  

---

## 1. Question

Does the HTTP fingerprint substrate discriminate when response bodies and status codes are identical but server-side state changes only independent header fields (Cache-Control, ETag, Set-Cookie, Vary) — isolating header-only drift from the vacuous body/status confound where full==body==status==1.0 and C4 is degenerate?

This is the binding Director question for this CONTINUE experiment. The parent handoff's `next_question` is advisory continuity evidence consistent with this mandate and is preserved, but the Director's target claim and portfolio rationale govern design.

---

## 2. Hypothesis

The HTTP fingerprint substrate — `hash(status_code + body_bytes + sorted_filtered_standard_headers)` with `EXCLUDED_HEADERS = [Date, Server, X-Request-Id]` identical to parent EXP-RUNTIME-35697043449 — will:

- **Discriminate header-only drift:** `H1: discrimination_full(A vs E) > 0.5` (expected 1.0 deterministic) where A and E return identical `200` status and byte-identical JSON bodies but differ only on independent headers via a writable server-side `header_config` change.
- **Show header baseline carries signal:** `H2: discrimination_headers_only(A vs E) > 0.5` and on at least 2/3 per-header isolations.
- **Prove body/status confound isolated:** `H3: discrimination_status_only = 0.0 AND discrimination_body_only = 0.0` on the same A-vs-E comparison (and per-header isolations), with `Content-Length` identical across states (not the driver, fixing parent V3).
- **Demonstrate non-vacuous full > baseline:** `H4: discrimination_full > max(discrimination_status_only, discrimination_body_only)` strictly (e.g., 1.0 > 0.0), the first non-vacuous C4.
- **Maintain null validity:** `H5: discrimination_full(null) = 0.0`, bootstrap 95% CI contains 0.0, point estimate ≤ 0.05 when resampling the same header state.

If all hold, header-only drift is measurable on the localhost substrate. If any fails, header-only drift is not discriminated by this fingerprint.

---

## 3. Inherited State — What is Established, Rejected, Unknown

From `handoff.json` of EXP-RUNTIME-35697043449 (preserved four-way distinction):

**Established (bounded):**
- On localhost Flask 3.1.3 + PyJWT 2.14.0 + SQLite WAL, the fingerprint deterministically discriminates maximally-distinct writable controls: permission escalation (403 vs 200+body, Jaccard 1.0, N=20 but 1 unique fingerprint/state) and session invalidation (200 vs 401, Jaccard 1.0). Null control on token-expiry metadata (fresh vs near-expiry valid JWT, identical responses) is 0.0 with degenerate CI [0.0,0.0]. All five decision-rule conditions C1-C5 pass, but audit status REVISE with `producer_claim_supported=false` narrows ceiling.

**Rejected:** (none — no hypothesis globally closed; parent narrowed ceiling only)

**Unknown (this experiment targets the first):**
- Header-only drift discrimination (bodies identical, only Cache-Control/ETag/Set-Cookie change) — `unresolved[1]`
- Same-status body-only permission change (200 vs 200 with different body) — `unresolved[3]`
- Production middleware (Django/Express/FastAPI, nginx) — `unresolved[2]`
- Partial body overlap, concurrency, HTTP/2/TLS — `unresolved[4]`
- Non-degenerate bootstrap CI — `unresolved[5]`

**Do not assume:**
- C-MEAS-VALID ready for VALIDATED/PRODUCT_CORE; C-FRESHNESS/C-DELTA-REPAIR unblocked for distributed testing; full-vector adds value beyond single-field (C4 was vacuous 1.0≥1.0); Flask dev results generalize to production; bootstrap [1.0,1.0] reflects precision (it is degenerate, effective N=1); B-HEADERS-ONLY 1.0 demonstrated independent signal (it was Content-Length/body-correlated).

This experiment directly tests the first unknown while explicitly not assuming the `do_not_assume` items. Distributed/production generalization remains out of scope and is disclosed as not tested.

---

## 4. Server Design

### 4.1 Testbed Architecture

```
Flask 3.1.3 + PyJWT 2.13.0 (HS256) + SQLite WAL (or in-memory dict with same commit semantics)
  ├── POST /admin/set_headers   — privileged, writes header_config (requires admin JWT; commits before 200 response)
  ├── GET  /resource            — authenticated GET, returns 200 + JSON body {"data":"hello","version":1} with headers per header_config
  └── GET  /protected           — retained from parent for smoke check (not primary measurement)
```

`header_config` table (or dict) schema: `cache_control TEXT, etag TEXT, vary TEXT, set_cookie TEXT` — initialized to STATE_A. `POST /admin/set_headers` updates the row and commits (SQLite WAL COMMIT) before returning 200; subsequent `GET /resource` reads the committed value. This is a writable server-side state change parallel to parent's `UPDATE users SET role` and `DELETE sessions` but with body/status held constant.

Authentication: JWT with `sub` claim only, role looked up from SQLite (same as parent). `/resource` requires valid JWT (200) but returns the same body regardless of `header_config` — only headers vary.

### 4.2 Header States

| State | Cache-Control | ETag | Vary | Set-Cookie | Status | Body |
|-------|---------------|------|------|------------|--------|------|
| **A baseline** | `max-age=3600` | `W/"aaa-111"` | `Accept-Encoding` | *(absent)* | 200 | `{"data":"hello","version":1}` |
| **B cache-only** | `max-age=0, must-revalidate` | `W/"aaa-111"` | `Accept-Encoding` | *(absent)* | 200 | identical to A |
| **C etag-only** | `max-age=3600` | `W/"bbb-222"` | `Accept-Encoding` | *(absent)* | 200 | identical to A |
| **D cookie-only** | `max-age=3600` | `W/"aaa-111"` | `Accept-Encoding` | `session=hdrdrift; Path=/; HttpOnly` | 200 | identical to A |
| **E combined** | `max-age=0, must-revalidate` | `W/"bbb-222"` | `Accept-Encoding, Origin` | `session=hdrdrift; Path=/; HttpOnly` | 200 | identical to A |

**Verification for each state:** after `POST /admin/set_headers`, a `SELECT header_config` confirms commit; then each of the N=20 `GET /resource` observations captures status, body_bytes, raw headers; body SHA-256 across states must be equal and Content-Length header identical (otherwise C6 fails).

Vary in E adds `Origin` to test a second value for the same header field; Set-Cookie tests the `Set-Cookie` vector that prior localhost tests never varied independently.

Bodies are intentionally byte-identical (same JSON serialization, same key order, no dynamic fields) so that B-BODY-ONLY must be 0.0.

### 4.3 Why This Comparand Set

- **Primary comparison A vs E** maximizes header distance (4 independent header changes) — most likely to be detected if the substrate has any header sensitivity.
- **Per-header isolations A vs B/C/D** test whether discrimination requires the combined signal or any single independent header suffices; requiring ≥2/3 prevents a single-header success from being dismissed as anomaly while also preventing combined-only success from masking per-header blindness.
- Content-Length is held constant by construction (bodies identical), so B-HEADERS-ONLY cannot cheat via Content-Length as in parent V3.

---

## 5. Measurement

### 5.1 Observation Vector

Per request:
- HTTP status code (int)
- Response body exact bytes + SHA-256 + length
- Raw standard headers dict (all headers except those in EXCLUDED_HEADERS are sorted and hashed)
- Response time (informational)
- Fingerprint variants: `full = hash(status + body_bytes + sorted_filtered_headers)`, `status_only = hash(status)`, `body_only = hash(body_SHA256)`, `headers_only = hash(sorted_filtered_headers)` — same functions as parent.

### 5.2 Discrimination Metric

Jaccard distance between fingerprint sets:

```
discrimination = 1.0 - |set_A ∩ set_B| / |set_A ∪ set_B|
```

Sets are built from N=20 fingerprints per state. With deterministic responses expected set size = 1 per state, discrimination is 1.0 if fingerprints differ, 0.0 if identical. Bootstrap 95% CI (B=1000) computed by resampling fingerprint sets with replacement, but reported as degenerate when set size =1 (expected). Effective distinct N reported.

### 5.3 Baselines

| ID | Fingerprint source | Expected on A vs E | Purpose |
|----|--------------------|--------------------|---------|
| B-STATUS-ONLY | status code alone | 0.0 | Strong null: proves status not the signal |
| B-BODY-ONLY | body SHA-256 alone | 0.0 | Strong null: proves body not the signal |
| B-HEADERS-ONLY | filtered headers only | >0.5 (expected 1.0) | Positive baseline: header signal alone |

### 5.4 Sample Size

- N=20 per header state: A×20, B×20, C×20, D×20, E×20 = 100
- Null control: A resampled as A1×20 and A2×20 (two independent batches, no write between) = 40
- Total raw lines = 140 (effective distinct fingerprints expected 5 for header states + 1 for null =6, nominal N=20 each disclosed)
- Jitter 50-150 ms uniform, SEED=44, same as parent for reproducibility.

Power: deterministic discrimination (set size 1) needs N=1 to detect; N=20 provides operational replication and matches parent's sampling plan while making degenerate CI explicit.

---

## 6. Decision Rule (Frozen)

**SUPPORTS** iff ALL hold:

1. **C1_FULL_HEADER_DRIFT:** `discrimination_full(A vs E) > 0.5` (expected 1.0) with status=200 verified on all observations in A and E, body SHA-256 identical across A vs E, Content-Length identical.
2. **C2_HEADERS_ONLY_SIGNAL:** `discrimination_headers_only(A vs E) > 0.5` AND `>0.5` on at least 2 of 3 per-header isolations (A vs B, A vs C, A vs D).
3. **C3_BODY_STATUS_ISOLATED:** `discrimination_status_only = 0.0` AND `discrimination_body_only = 0.0` on A vs E and on each per-header isolation (A vs B, A vs C, A vs D). Any >0.0 fails isolation.
4. **C4_FULL_EXCEEDS_BASELINES_NONVACUOUS:** `discrimination_full(A vs E) > max(discrimination_status_only, discrimination_body_only)` strictly greater (e.g., 1.0 > 0.0). Equality at ceiling (1.0 ≥1.0) as in parent is defined as failure for this experiment.
5. **C5_NULL_NO_FALSE_POSITIVE:** Null control A1 vs A2 (same header state, two batches) `discrimination_full = 0.0`, bootstrap 95% CI contains 0.0, point estimate ≤0.05; additionally `discrimination_status_only =0.0` and `discrimination_body_only =0.0` on null.
6. **C6_CONTENT_LENGTH_IDENTITY:** `Content-Length` header value identical across A/B/C/D/E and body lengths equal — confirming header discrimination not via body-correlated Content-Length.

If any of C1–C6 fails → **FALSIFIED-IN-SETTING** with specific failing condition documented (which header signal missing, which isolation violated, or null false positive).

If infrastructure prevents verification of status/body identity or header writes (server crash, commit failure, body mismatch due to server error, non-200 where 200 required) → **MEASUREMENT_INVALID** with category, retryability, and diagnostic logged. Degenerate bootstrap CI [1.0,1.0] / [0.0,0.0] is EXPECTED deterministic behavior and is not a measurement invalidity when set sizes are 1 and validity checks pass.

---

## 7. Controls Summary

| Control | ID | Type | Pass threshold | Evidence required |
|---------|----|------|----------------|-------------------|
| Full header drift | C1 | positive | >0.5, expect 1.0 | A vs E full Jaccard=1.0, status 200, body SHA equal |
| Headers-only signal | C2 | positive | >0.5 on A vs E +2/3 isolations | headers_only Jaccard per comparison |
| Body/status isolated | C3 | strong null | =0.0 | status_only and body_only Jaccard =0 on all header comparisons |
| Full > baselines | C4 | non-vacuous superiority | strictly > | full vs max(status,body) on A vs E |
| Null stability | C5 | null | =0.0, CI contains 0, ≤0.05 | A1 vs A2 full Jaccard 0 |
| Content-Length identity | C6 | validity | identical | header values equal across states |

---

## 8. Validity Threats and Mitigations

1. **Header not committed:** POST /admin/set_headers not visible to next GET → mitigate by SELECT verification + COMMIT before 200; log header_config before each batch.
2. **Body not byte-identical:** JSON serialization variance (key order, whitespace) → mitigate by fixing `json.dumps(sort_keys=True)` server-side and verifying SHA-256 equality before computing discrimination.
3. **Content-Length leaks body-correlation:** bodies identical guarantees Content-Length identical; C6 enforces this; any difference fails the comparison rather than being called a header signal.
4. **Excluded headers drift:** Date varies per request but is excluded; include only filtered headers in fingerprint; verify EXCLUDED_HEADERS constant.
5. **Degenerate CI misread as precision:** disclose effective distinct N=1, treat CI as deterministic, do not claim narrow inferential CI; parent V1 fix applied.
6. **Flask dev server header injection:** Werkzeug may add Connection: close etc. → capture raw headers and include all non-excluded headers; log full header dict for audit recomputation.
7. **Set-Cookie parsing:** multiple Set-Cookie headers may be folded → log raw header list and hashed sorted representation; treat presence/absence as the signal.
8. **Port collision / stale server:** discover free port, start fresh server per run, record port in provenance, kill on exit.

---

## 9. Consequences

**Positive (all C1–C6 pass):** C-MEAS-VALID ceiling expands to include header-only drift on localhost synthetic substrate — the first non-vacuous C4 (full > body/status) and first header signal independent of Content-Length. This directly closes parent audit V2 (ceiling) and V3 (header correlation) and provides the measurement prerequisite for Graph-layer C-FRESHNESS (detect staleness when content unchanged) and C-DELTA-REPAIR (perturbation cost when only metadata varies). Still bounded to localhost Flask dev server; does NOT unlock distributed/production promotion. C-MEAS-VALID remains EXPERIMENTAL.

**Negative (any C1–C6 fails):** Header-only drift not discriminated by current fingerprint (or isolation not achieved, or null false positive). This bounds C-MEAS-VALID to body/status-only discrimination (parent ceiling) and shows header-only cases — the actual freshness/delta-repair use case — are unmeasurable with this substrate. Product consequence: header freshness requires a different substrate (explicit header-aware check, DOM-level observation, or production header handling) and distributed testing of header-sensitive flows is not yet valid. Negative result is equally high-information because it prevents premature scaling of a non-discriminating measurement to Graph/Product lanes.

---

## 10. What is NOT Tested (Scope Boundaries)

- Production WSGI (gunicorn/nginx), CDN, concurrent load, HTTP/2, TLS, browser DOM — explicitly out of scope; localhost Flask only.
- Same-status body-only permission change (200 with reader vs admin body) — listed as unknown, not tested here to keep this experiment minimal and header-isolated.
- Fresh vs near-expiry token null from parent — not repeated as primary (parent already established); exploratory only if needed.
- Cost, latency, token economics — not measured.

---

## 11. Execution Checklist for EXECUTE

- Must implement `run_experiment.py` with fingerprint functions identical to parent for audit recomputation.
- Must log `raw_observations.jsonl` (140 lines: 7 batches ×20) with fields: state, status, body_sha256, body_len, headers_filtered_json, headers_raw_json, fingerprint_full, fingerprint_status, fingerprint_body, fingerprint_headers.
- Must produce `experiment_result.json` (derived) and `result.json` (canonical) with metrics: `header_drift_full`, `cache_only_full`, `etag_only_full`, `cookie_only_full`, `null_control_full` plus baseline variants and controls C1–C6.
- Must record `provenance.json` with env (Flask/PyJWT/SQLite/Python versions, port, seed 44, excluded_headers, header_config values per state, artifact SHA-256).
- Must not inspect outcomes before freeze; frozen spec/prereg/decision_rule are immutable after `freeze.json`.

