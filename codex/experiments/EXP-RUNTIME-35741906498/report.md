# EXP-RUNTIME-35741906498 — REPORT (EXECUTE)

**Experiment ID:** EXP-RUNTIME-35741906498
**Lane:** runtime
**Claim:** C-MEAS-VALID (measurement substrate is intervention-valid)
**Status:** COMPLETE
**Outcome:** SUPPORTS (all six frozen decision-rule conditions C1–C6 pass)

---

## 1. Summary

This experiment tested the first **non-vacuous C4** for the HTTP fingerprint
substrate: does the fingerprint — `SHA256(status || body_bytes ||
sorted_filtered_headers)` with `EXCLUDED_HEADERS={Date, Server, X-Request-Id}`
— discriminate server-side state changes when response **bodies are
byte-identical** and **status codes are identical (200 vs 200)**, and the only
differences are independent header fields (Cache-Control, ETag, Set-Cookie,
Vary)?

**Answer, bounded to this setting: YES.** On the localhost Flask + SQLite
writable `header_config` testbed, the full-vector fingerprint discriminated
header-only drift at exactly 1.0 (Jaccard distance, deterministic), the
headers-only baseline carried the full signal (1.0), the status-only and
body-only baselines were exactly 0.0, the full vector strictly exceeded its
baselines (1.0 > 0.0 — the first non-vacuous C4 for this substrate), and the
null control (same header state resampled) was exactly 0.0.

This closes parent audit gaps V2 (ceiling effect) and V3 (header correlation
via Content-Length): header discrimination here is **not** body- or
Content-Length-correlated (Content-Length = "31" on all 180 observations, body
SHA-256 identical across all states).

---

## 2. Design as executed (frozen, unchanged)

Per frozen `spec.json` / `prereg.md`:

| Element | Frozen specification | Executed |
|---|---|---|
| Server | Flask 3.1.3 + PyJWT 2.14.0 (HS256) + SQLite WAL | same (127.0.0.1:19848) |
| Body | `{"data":"hello","version":1}` with `sort_keys=True`, byte-identical | 31 bytes, SHA-256 `d0ca83…72e34` on all 180 observations |
| States | A baseline, B Cache-Control-only, C ETag-only, D Set-Cookie-only, E combined (+Vary) | exact per frozen table |
| Sampling | N=20 per state, jitter 50–150 ms, SEED=44 | exact; 9 batches × 20 = 180 raw lines |
| Fingerprint | identical algorithm to parent EXP-RUNTIME-35697043449 (copied verbatim) | independently recomputed: 0 mismatches |
| Metric | `1 − |A∩B| / |A∪B|` over fingerprint sets; bootstrap B=1000, α=0.05 | exact |
| Primary comparison | A vs E (4 header fields changed) | — |
| Isolations | A vs B, A vs C, A vs D (single-header changes) | — |
| Null | A1 vs A2 (same committed STATE_A, no write between; two independent N=20 batches) | exact; plus exploratory E1 vs E2 per frozen null_control clause |

Batch order executed: write A → batch A → write B → batch B → write C → batch
C → write D → batch D → write E → batch E → batch null_E1 → batch null_E2 →
write A → batch null_A1 → batch null_A2. Every write was verified by SQLite
SELECT before the next observation batch (`batch_state_log.jsonl`, 15 lines).

The frozen prereg §5.4 projected 140 primary raw lines; the frozen
`spec.json` null_control clause additionally requires an exploratory STATE_E
resampled null (+40 lines). Total raw lines = 180. The E-null is exploratory
and is not part of decision condition C5.

---

## 3. Raw evidence (direct observations)

Raw evidence lives in `raw_observations.jsonl` (180 lines) and
`batch_state_log.jsonl` (15 lines). Key direct observations:

1. **Status identity:** all 180 observations returned HTTP 200.
2. **Body identity:** body SHA-256 `d0ca83…72e34` in all 9 batches; 31 bytes.
3. **Content-Length identity:** header value `"31"` on all 180 observations.
4. **Header deltas:** filtered header dicts differ only in Cache-Control,
   ETag, Set-Cookie, Vary; `Connection: close`, `Content-Type:
   application/json`, `Content-Length: 31` are constant.
5. **Set-Cookie presence:** exactly 80/180 observations (batches D, E,
   null_E1, null_E2); absent from A, B, C, null_A1, null_A2.
6. **Date varies (20 unique values), Server constant; both excluded with 0
   leakage into filtered dicts.**
7. **Determinism:** exactly 1 unique fingerprint per state per source
   (effective distinct N = 1; nominal N = 20). Bootstrap CIs are degenerate
   — expected per frozen design, not inferential precision.
8. **Null:** null_A1 vs null_A2 identical on all four sources; exploratory
   null_E1 vs null_E2 identical on all four sources.

---

## 4. Derived measurements

Jaccard-distance discrimination (1.0 = fully disjoint fingerprints; 0.0 =
identical). All CIs degenerate per above.

| Comparison | full | status-only | body-only | headers-only |
|---|---|---|---|---|
| **header_drift (A vs E)** | **1.0** | 0.0 | 0.0 | **1.0** |
| cache_only (A vs B) | 1.0 | 0.0 | 0.0 | 1.0 |
| etag_only (A vs C) | 1.0 | 0.0 | 0.0 | 1.0 |
| cookie_only (A vs D) | 1.0 | 0.0 | 0.0 | 1.0 |
| **null_control (A1 vs A2)** | **0.0** | 0.0 | 0.0 | 0.0 |
| null_e_exploratory (E1 vs E2) | 0.0 | 0.0 | 0.0 | 0.0 |

Every single isolated header (Cache-Control, ETag, Set-Cookie) alone produced
full discrimination — the substrate's header sensitivity is not dependent on
a combined multi-header signature.

---

## 5. Controls (frozen decision rule)

| ID | Type | Threshold | Observed | Pass |
|---|---|---|---|---|
| C1_FULL_HEADER_DRIFT | positive | full(A,E) > 0.5, 200-200, body SHA equal, CL identical | 1.0; all verified | PASS |
| C2_HEADERS_ONLY_SIGNAL | positive | headers(A,E) > 0.5 and ≥2/3 isolations | 1.0; 3/3 isolations | PASS |
| C3_BODY_STATUS_ISOLATED | isolation | status=0.0 and body=0.0 on A/E + isolations | 0.0 on all 8 pairs | PASS |
| C4_FULL_EXCEEDS_BASELINES_NONVACUOUS | non-vacuous | full > max(status, body) strictly | 1.0 > 0.0 | PASS |
| C5_NULL_NO_FALSE_POSITIVE | null | full=0.0, CI contains 0.0, ≤0.05, status/body=0.0 | 0.0, CI [0.0,0.0], status/body 0.0 | PASS |
| C6_CONTENT_LENGTH_IDENTITY | validity | CL identical across A–E, body_len equal | "31" everywhere, 31 bytes | PASS |
| B-STATUS-ONLY | baseline null | 0.0 on header-only comparisons | 0.0 (5 comparisons) | PASS |
| B-BODY-ONLY | baseline null | 0.0 on header-only comparisons | 0.0 (5 comparisons) | PASS |
| B-HEADERS-ONLY | baseline positive | >0.5 on A/E + ≥2/3 isolations | 1.0; 3/3 | PASS |

---

## 6. Interpretation (bounded)

The frozen decision rule is satisfied: **SUPPORTS** for the claim
**"the HTTP fingerprint substrate discriminates header-only server-state
drift (Cache-Control/ETag/Set-Cookie/Vary) when bodies and status codes are
identical, on the localhost Flask dev-server setting, with deterministic
responses and effective N=1 per state."**

What this means for the program:

- The parent audit's V2 (ceiling: full == body == status == 1.0) and V3
  (header signal correlated with Content-Length) gaps are closed: header
  discrimination occurs with zero body/Content-Length correlation.
- The first non-vacuous C4 for C-MEAS-VALID: 1.0 > 0.0 on A vs E. The full
  vector adds information over both single-field baselines when bodies and
  statuses are constant.
- C-FRESHNESS / C-DELTA-REPAIR cases where **content is unchanged but
  metadata varies** (cache headers, ETag, cookies) are measurable on this
  substrate at the localhost synthetic level — subject to the strong
  bounds below.
- This complements the already-verified nginx HIT/SWR/SIE body-identical
  oracle-free decompression work (EXP-RUNTIME-35611612543): the substrate
  now covers "header-identical body-different" (decompression studies) and
  "body-identical header-different" (this study).

**Bounding (do not over-read):** the substrate here is a Flask development
server on localhost with a hand-written `header_config` SQLite state; single
sequential client; no production WSGI/nginx middleware; no CDN; no
concurrency; no HTTP/2/TLS; no non-deterministic header emission. All
discrimination is deterministic (effective N=1), and CIs are degenerate —
this is an existence/discrimination ceiling result, not an estimate of
sensitivity under noise. **C-MEAS-VALID remains EXPERIMENTAL**, per the
frozen `product_consequence_positive`; nothing here promotes the claim to
VALIDATED or PRODUCT_CORE, and distributed/production testing remains
blocked pending production middleware/CDN work.

---

## 7. Validity threats and mitigations (how they panned out)

| Threat (prereg §8) | Mitigation | Outcome |
|---|---|---|
| Header not committed before observation | POST /admin/set_headers + SQLite SELECT per batch | All 15 log lines matched expected config |
| Body not byte-identical | fixed serialization; SHA-256 per observation | Single SHA across all 180 |
| Content-Length leaks body correlation | C6 enforcement | Identical "31" everywhere |
| Excluded headers drift | Date/Server/X-Request-Id excluded; per-line check | 0 leakage; Date varied 20× and was excluded |
| Degenerate CI misread as precision | effective N=1 disclosed; CI flagged degenerate | Disclosed in §3 and validity_notes |
| Werkzeug header injection | raw + filtered dicts logged per line | Only `Connection: close` added; constant — no effect |
| Set-Cookie folding | presence/absence is the signal | Exact presence in 80/180 lines |
| Port collision / stale server | free-port discovery (19848), fresh DB per run | Clean single run |

Independent verification performed by the producer after the run: all 180×4
fingerprints recomputed from raw fields with the parent algorithm — 0
mismatches; discrimination recomputed — matches derived metrics exactly.

---

## 8. Unresolved (carried forward)

- Same-status body-only permission change (200 vs 200, different body) —
  the other half of audit V2 — remains untested.
- Production middleware (Django/Express/FastAPI, gunicorn, nginx) header
  behavior; CDN; concurrency; HTTP/2/TLS.
- Non-degenerate CI and sensitivity ordering: all three isolated headers hit
  1.0, so no signal-strength gradient to inform header-freshness policies.
- Distributed/production freshness and delta-repair testing (blocked;
  localhost synthetic now unblocked).

---

## 9. Artifacts

| Path | Role |
|---|---|
| `run_experiment.py` | code (frozen-design executor) |
| `raw_observations.jsonl` | raw evidence (180 lines) |
| `batch_state_log.jsonl` | raw evidence (15 lines) |
| `experiment_result.json` | derived measurements |
| `build_packet.py` | code (packet emission) |
| `result.json` / `provenance.json` | canonical packet (this stage) |

Hashes in `result.json.artifacts` and `provenance.json`. No git mutation was
performed by EXECUTE.