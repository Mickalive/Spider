# EXP-RUNTIME-35749360317 — REPORT (EXECUTE)

**Experiment ID:** EXP-RUNTIME-35749360317
**Lane:** runtime
**Claim:** C-MEAS-VALID (measurement substrate is intervention-valid)
**Status:** COMPLETE
**Outcome:** SUPPORTS (all eight frozen decision-rule conditions C1–C8 pass; exploratory N2 null also 0.0)

---

## 1. Summary

This experiment tested the second non-vacuous branch for the HTTP fingerprint
substrate: does the fingerprint —
`SHA256(status || body_bytes || sorted_filtered_headers)` with
`EXCLUDED_HEADERS={Date, Server, X-Request-Id}` — discriminate server-side state
changes when **status codes are identical (200 vs 200)**, non-Content-Length
headers are held constant, and the only difference is the response **body**,
changed via a committed SQLite-writeable server state (body variant)?

**Answer, bounded to this setting: YES.** On the localhost Flask + SQLite
writable `body_config` testbed, the full-vector fingerprint discriminated
same-status body-only drift (STATE_A 31-byte baseline vs STATE_C 117-byte admin
body) at exactly 1.0 (Jaccard distance, deterministic), the body-only baseline
carried the full signal (1.0 on A vs C and on the A vs B per-body isolation),
the status-only baseline was exactly 0.0 (200 == 200 on every observation of
the body-only batches), the non-Content-Length header baseline was exactly 0.0
(no independent header drift), the full vector strictly exceeded status-only
(1.0 > 0.0 — the body-branch complement of the parent's V2-fixed C4), and all
nulls were exactly 0.0 (N1 STATE_A resample, exploratory N2 STATE_C resample,
same-state 403, same-state 401).

This is the complementary half of the localhost discrimination matrix to
EXP-RUNTIME-35741906498 (header-only drift, bodies identical, CLEN constant here
CLEN varies with body): together with the classic writable permission-escalation
(403 vs 200) and session-invalidation (401 vs 200) controls at 1.0 ≥ 0.7 with
nulls 0.0, the localhost matrix (header-only, body-only same-status,
status-varying maximally-distinct, null stability) is complete for the Flask
dev-server HS256 setting.

---

## 2. Design as executed (frozen, unchanged)

Per frozen `spec.json` / `prereg.md` (freeze hashes: request
622d624e…, spec eaedd714…, prereg 78a5ec55…):

| Element | Frozen specification | Executed |
|---|---|---|
| Server | Flask 3.1.3 + PyJWT 2.14.0 (HS256) + SQLite WAL + Werkzeug 3.1.8, Python 3.12.14 | same (127.0.0.1:19849) |
| Body A | `{"data":"hello","version":1}`, 31 bytes, SHA-256 `d0ca83…72e34` (pinned) | exact pin; all body_A/null_A observations |
| Body B | `{"data":"hello","items":["a","b"],"role":"reader","version":1}`, `~52 (exact logged)`, SHA distinct | 70 bytes, SHA-256 `67c186…99c`; exact JSON per frozen §4.2 with parent default separators |
| Body C | `{"admin_note":"sensitive:42","count":42,"data":"hello","items":["a","b","c"],"role":"admin","version":1}`, `~95 (exact logged)`, SHA distinct | 117 bytes, SHA-256 `b46c46…dd32`; exact JSON per frozen §4.2 |
| Error bodies | P_403 `{"error":"forbidden"}`; S_401 `{"error":"unauthorized"}` | 22 bytes `387fe7…603b`; 25 bytes `9df366…8f34` (constant on all 403/401 observations) |
| fixed headers | Cache-Control max-age=3600, ETag W/"fixed-aaa-111", Vary Accept-Encoding, no Set-Cookie, Content-Type application/json | SELECT-verified constant before each 200-batch |
| Sampling | N=20 per batch, jitter 50–150 ms, SEED=44 | exact; 15 batches × 20 = 300 raw lines |
| Fingerprint | algorithm identical to parent EXP-RUNTIME-35697043449 (copied verbatim) + `headers_no_clen` | `fingerprint_algorithm_matches_parent` check passed; independent recomputation from raw fields: 0 mismatches |
| Metric | `1 − |A∩B| / |A∪B|` over fingerprint sets; bootstrap B=1000, α=0.05 | exact |
| Primary comparison | A vs C (200 vs 200, bodies byte-different, non-CLEN headers identical) | full 1.0, body-only 1.0, status-only 0.0, headers-no-CLEN 0.0 |
| Isolation | A vs B (smaller perturbation, reader role added) | full 1.0, body-only 1.0, status-only 0.0 |
| Nulls | N1 (STATE_A resampled) gating; N2 (STATE_C resampled) exploratory; N3 same-state 403/401 nulls (per frozen spec null_control) | N1 0.0, N2 0.0, perm-null 0.0, sess-null 0.0 |
| Classic controls | P_403 permission escalation 403 vs 200 ≥0.7; S_401 session invalidation 401 vs 200 ≥0.7 | 1.0 ≥ 0.7 both; nulls 0.0 |

Batch order executed (frozen spec null_control N1/N2/N3 + decision rule C7/C8
null requirements; prereg §8 item 11 relative order body-only → N1 → P_403 →
S_401 preserved, N2 exploratory inserted between N1 and P_403):

```
set_headers → body_A → body_B → body_C → null_A1 → null_A2 → null_C1 → null_C2
→ perm_403 → perm_200 → perm403_null_1 → perm403_null_2
→ sess_200 → sess_401 → sess401_null_1 → sess401_null_2
```

Every one of the 12 admin writes was verified by SQLite SELECT (post-SELECT
matching intended state) before the next observation batch
(`batch_state_log.jsonl`, 27 lines = 12 writes + 15 pre-batch verifies ≥ the
15+ entries the prereg §11 requires).

**Line-count disclosure (nominal vs effective):** prereg §5.4/§11 prose
projected 140–180 raw lines for A/B/C + N1 + P_403 + S_401 (+ N2); the frozen
`spec.json` null_control additionally mandates N3 (same-state 403 resampled and
same-state 401 resampled) and its decision rule C7/C8 require those nulls, so
the full mandatory schedule is 15 batches × 20 = **300 raw lines**. The
batch_state_log is consistent with 300 lines as the prereg §11 requires
(disclose nominal vs effective).

---

## 3. Raw evidence (direct observations)

Raw evidence lives in `raw_observations.jsonl` (300 lines) and
`batch_state_log.jsonl` (27 lines). Key direct observations:

1. **Status identity:** 180× HTTP 200 (body-only A/B/C + all nulls + perm_200 +
   sess_200), 60× HTTP 403 (perm_403 + perm403 nulls), 60× HTTP 401 (sess_401 +
   sess401 nulls). All 20 observations in every body-only and null batch were
   200.
2. **Body identity:** body SHA-256 per state — A `d0ca83…72e34` (31 B), B
   `67c186…99c` (70 B), C `b46c46…dd32` (117 B), each with exactly one value
   across its 20 observations and all resampled null batches; 403 body
   `387fe7…603b` (22 B) constant in all 60×403; 401 body `9df366…8f34` (25 B)
   constant in all 60×401.
3. **Content-Length == body_len** on all 300 observations; CLEN by state: 31 /
   70 / 117 (distinct, strictly increasing, proportional to body_len).
4. **Non-CLEN filtered headers identical across A/B/C** (Cache-Control, ETag,
   Vary, Content-Type, Connection constant; Set-Cookie absent everywhere — 0/300
   observations carry Set-Cookie).
5. **Date varied across observations and is excluded** (0 leakage into filtered
   dicts); Server constant; EXCLUDED_HEADERS unchanged.
6. **Determinism:** exactly 1 unique fingerprint per state per source
   (effective distinct N = 1; nominal N = 20); bootstrap CIs degenerate —
   expected per frozen design, not inferential precision.
7. **Writable commits:** all 12 `write_state::*` entries recorded HTTP 200 +
   `match_expected=true` with post-SELECT state (e.g., body_config
   `{variant, body_sha256}` matched, role matched, reader_valid_sessions → 0 for
   the session control).
8. **Session/role mechanics:** sess_401 batch observed only after
   `invalidate_session` post-SELECT showed `reader_valid_sessions = 0`; perm_403
   batch observed only after `set_role` post-SELECT showed `role = viewer`.

---

## 4. Derived measurements

Jaccard-distance discrimination (1.0 = fully disjoint fingerprint sets; 0.0 =
identical). All CIs degenerate `[1.0,1.0]`/`[0.0,0.0]` (deterministic substrate,
effective N=1), reported in full in `experiment_result.json` / `result.json`.

| Comparison | full | status-only | body-only | headers-only | headers-no-CLEN |
|---|---|---|---|---|---|
| **body_drift A vs C** (primary) | **1.0** | **0.0** | **1.0** | 1.0 | **0.0** |
| body_drift A vs B (isolation) | 1.0 | 0.0 | 1.0 | 1.0 | 0.0 |
| **null N1** (A1 vs A2) | **0.0** | 0.0 | 0.0 | 0.0 | 0.0 |
| **null N2** (C1 vs C2, exploratory) | **0.0** | 0.0 | 0.0 | 0.0 | 0.0 |
| **classic perm** (403 vs 200) | **1.0** | 1.0 | 1.0 | 1.0 | 1.0 |
| **classic sess** (401 vs 200) | **1.0** | 1.0 | 1.0 | 1.0 | 1.0 |
| perm null (403 vs 403) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| sess null (401 vs 401) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Reading of the components on the primary comparison:
- **full = 1.0** and **body-only = 1.0** → the body bytes alone fully separate
  A from C; every one of the 40 fingerprints differs.
- **status-only = 0.0** → status is genuinely 200 vs 200; no status confound.
- **headers-only = 1.0** occurs solely through body-correlated Content-Length
  (documented per frozen C2, not a failure); **headers-no-CLEN = 0.0** proves no
  independent header drift.
- **full 1.0 > status-only 0.0** → non-vacuous complement of the parent's
  header-only `full 1.0 > max(status 0.0, body 0.0)`; the equality-at-ceiling
  vacuous case (full == status == 1.0) does not occur here.

---

## 5. Controls (frozen decision rule)

| ID | Type | Threshold | Observed | Pass |
|---|---|---|---|---|
| C1_FULL_BODY_DRIFT | positive | full(A,C) > 0.5; 200-200; body SHA ≠; CLEN ≠ | 1.0; all verified | PASS |
| C2_BODY_ONLY_SIGNAL | positive + isolation | body(A,C) > 0.5 AND body(A,B) > 0.5; headers-no-CLEN(A,C) = 0.0 | 1.0; 1.0; 0.0 | PASS |
| C3_STATUS_ISOLATED | strong null | status-only = 0.0 on A/C and A/B | 0.0; 0.0 | PASS |
| C4_FULL_EXCEEDS_STATUS_NONVACUOUS | non-vacuous | full(A,C) > status(A,C) strictly | 1.0 > 0.0 | PASS |
| C5_NULL_NO_FALSE_POSITIVE | null | full(N1) = 0.0, CI contains 0.0, ≤0.05; status/body = 0.0 | 0.0; CI [0.0,0.0]; 0.0/0.0 | PASS |
| C6_CONTENT_LENGTH_VARIES_AND_HEADERS_CONSTANT | validity | CLEN 31≠70≠117, SHA distinct, non-CLEN identical, CLEN==body_len, no Set-Cookie | all verified on raw | PASS |
| C7_WRITABLE_PERMISSION_LEVEL | positive ≥0.7 + null | (a) reader-200 vs admin-200 ≥0.7 (realized as A vs C); (b) 403 vs 200 ≥0.7 + 403-null 0.0 | 1.0 (A vs C); 1.0; 0.0 | PASS |
| C8_WRITABLE_SESSION_INVALIDATION | positive ≥0.7 + null | 401 vs 200 ≥0.7; 401-null 0.0 | 1.0; 0.0 | PASS |
| C5B_NULL_N2_EXPLORATORY | null (reported, not gating) | N2 = 0.0 | 0.0 | PASS |
| B-STATUS-ONLY | baseline strong null | 0.0 on same-status body-only; 1.0 on classic | 0.0/0.0/0.0; 1.0/1.0 | PASS |
| B-BODY-ONLY | baseline positive | >0.5 on A/C and A/B; 1.0 on classic; 0.0 on nulls | 1.0/1.0; 1.0/1.0; 0.0 | PASS |
| B-HEADERS-ONLY | baseline (CLEN-correlated) | >0 via Content-Length only; 0.0 on nulls | 1.0/1.0; 0.0 (nulls) | PASS |
| B-HEADERS-NO-CLEN | isolation | 0.0 on body-only comparisons | 0.0/0.0/0.0 | PASS |

Identifiers match the frozen prereg §6/§7/§11 exactly; the C7(a) body-filtered
permission comparison is realized as STATE_A vs STATE_C per the frozen decision
rule ("A vs C, same as C1, ≥0.7 automatically if C1 passes at 1.0").

---

## 6. Interpretation (bounded)

The frozen decision rule is satisfied: **SUPPORTS** for the claim **"the HTTP
fingerprint substrate discriminates same-status body-only server-state drift
(200 vs 200 with byte-different bodies via a committed SQLite-only write) when
non-Content-Length headers and status are held constant, on the localhost Flask
dev-server setting, with deterministic responses and effective N=1 per
state."**

Program consequences (as the frozen `product_consequence_positive` prescribes):

- The parent audit's V2 body half is closed: body-only discrimination occurs
  with status constant (0.0) and no independent header signal (headers-no-CLEN
  0.0); CLEN variation is fully body-correlated and equals body_len.
- C-MEAS-VALID's localhost matrix is now complete for the Flask dev server:
  header-only drift (parent), body-only same-status drift (this experiment),
  status-varying maximally-distinct classics (403/401 vs 200), and null
  stability at 0.0. Substrate detects both independent header mutations and
  independent body mutations, each with non-vacuous `full > status`.
- C-FRESHNESS (graph can trust detection of content-only drift without status
  change) and C-DELTA-REPAIR (local body perturbation measurement) are unblocked
  for **localhost synthetic testing only** — the exact ceiling the frozen
  consequence describes.

**Bounding (do not over-read):** Flask development server on localhost; single
sequential client; no production WSGI (gunicorn), nginx, CDN, load balancer; no
concurrency, HTTP/2, TLS; no distributed SQLite replication; body value
magnitudes limited to 3 variants (31/70/117); all discrimination is
deterministic (effective N=1) and CIs are degenerate — an existence/
discrimination-ceiling result, not a sensitivity estimate under noise.
**C-MEAS-VALID remains EXPERIMENTAL**; nothing here promotes it to VALIDATED or
PRODUCT_CORE. The permission-filtered **role-based** body variant (two tokens,
role-filtered field) is not separately measured — A vs C realized it via
`body_config` per the frozen decision rule; a role-column-driven body filter
remains untested (see §8).

---

## 7. Validity threats and mitigations (how they panned out)

| Threat (prereg §8/§9) | Mitigation | Outcome |
|---|---|---|
| Body not committed / stale read | POST /admin/set_body_variant + SQLite SELECT per batch | 12 writes all post-SELECT-match; 15 pre-batch verifies |
| Body serialization variance | `json.dumps(sort_keys=True, separators=(',',':'))` server-side; per-observation SHA | Single SHA per state; CLEN == body_len all 300 |
| CLEN not varying / header-confounded | bodies 31/70/117; C6; headers-no-CLEN | CLEN 31/70/117; headers-no-CLEN 0.0 |
| Status not 200 during body-only | same valid JWT; per-observation status check | all 60 body-only + 120 null observations 200 |
| Excluded headers drift | Date/Server/X-Request-Id excluded; per-line check | 0 leakage |
| header_config drift | set_headers once; SELECT before each batch | identical non-CLEN headers across A/B/C |
| Degenerate CI misread as precision | effective N=1 disclosed; CI flagged degenerate | disclosed here and in validity_notes |
| Set-Cookie / Vary leakage | absence verified; raw dicts logged | Set-Cookie absent 0/300 |
| Port collision / stale server | free-port discovery 19849–19898; fresh SQLite per run | clean single run on 19849 |
| Threshold confusion (≥0.7 vs >0.5) | per-control thresholds from frozen rule | C1/C2 >0.5; C7/C8 ≥0.7 — applied as frozen |
| Workload conflation | one server lifecycle, fixed order, logged | batch_state_log documents order |

**Execution disclosures (pre-measurement, not weakening):**

1. *Attempt-1 infra failure is not a scientific negative.* The first attempt
   (run 35749360317) exited 75 during pre-execution environment
   checks — an infrastructure/retry-exit condition
   (`failure.json` history[0]; category EXECUTION_FAILURE, retryable=true,
   fingerprint fbf5825e…). This run (35756234169) executed cleanly; the failure
   carries no measurement content. `failure.json` was later rewritten by this
   stage as a resolved-history record (see below; both transient events are
   preserved in its `history`, with `retryable=false` and the COMPLETE outcome).
2. *Server error-body mapping fix.* During the pre-measurement smoke pass,
   GET /resource returned a reason-specific 401 body (`{"error":
   "session_invalid"}`) for invalidated sessions, which contradicts the frozen
   prereg S_401 pin (`401 body {"error":"unauthorized"}`). The server's error
   mapping was corrected to the frozen constant error bodies (P_403 →
   `{"error":"forbidden"}`, S_401 → `{"error":"unauthorized"}`) **before any
   full measurement ran**; smoke re-passed, then the full run executed cleanly.
   No measurement was taken with the non-conforming body.
3. *Body B/C exact lengths.* Frozen prose "~52"/"~95" are explicitly marked
   approximate with "exact logged" in prereg §4.2; effective lengths are 70/117
   for the exact frozen JSON under the parent's default-separator
   serialization. C6 (strict inequality, proportionality via CLEN==body_len,
   SHA distinct) is satisfied; body A pin is exact (31 B, `d0ca83…72e34`).
4. *Line count 300.* See §2 disclosure: the frozen spec's N3 nulls + C7/C8 null
   requirements mandate the full 15-batch schedule.

Independent verification performed by the producer after the run: all 300×5
fingerprints recomputed from raw fields with the parent algorithm — 0
mismatches; Jaccard distances recomputed — match derived metrics exactly.

---

## 8. Unresolved (carried forward)

- Role-column-driven permission-filtered body (two tokens, same `body_config`),
  the P1 spelling, is not separately measured; A vs C (body_config variant)
  realized the 200 vs 200 permission-level comparison per the frozen rule.
- Production WSGI (gunicorn), nginx, CDN, load balancer, Django/Express/FastAPI
  middleware; concurrency; HTTP/2; TLS — untested (localhost Werkzeug only).
- Distributed SQLite replication / Redis shared session for distributed
  C-FRESHNESS / C-DELTA-REPAIR — blocked; localhost synthetic now unblocked for
  both branches.
- Non-degenerate bootstrap CI cannot be obtained on this deterministic
  substrate; a source of nondeterminism (e.g., real CDN) is needed for
  genuine inferential CIs.
- Body magnitude gradient (beyond 31/70/117) and per-field sensitivity ordering
  for body-freshness policy design remain uncharacterized — all present variants
  produced ceiling 1.0.

---

## 9. Artifacts

| Path | Role |
|---|---|
| `run_experiment.py` | code (frozen-design executor) |
| `raw_observations.jsonl` | raw evidence (300 lines) |
| `batch_state_log.jsonl` | raw evidence (27 lines) |
| `experiment_result.json` | derived measurements |
| `build_packet.py` | code (packet emission) |
| `result.json` / `provenance.json` | canonical packet (this stage) |

Hashes in `result.json.artifacts` and `provenance.json`. No git mutation was
performed by EXECUTE.