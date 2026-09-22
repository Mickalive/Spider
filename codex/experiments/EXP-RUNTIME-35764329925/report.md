# EXP-RUNTIME-35764329925 — Production WSGI (gunicorn) + nginx Generalization of the HTTP Fingerprint Substrate

## 1. Executive Summary

The frozen Director PIVOT question asked whether the C-MEAS-VALID HTTP fingerprint
substrate — `SHA256(status || body_bytes || sorted_filtered_headers)` with
`EXCLUDED_HEADERS={Date, Server, X-Request-Id}` — retains its discriminating same-status
body-only and header-only behavior, null stability, and writable permission/session
controls when moved from the localhost Flask dev server (Werkzeug) to a production-like
stack (Flask 3.1.3 + PyJWT 2.14.0 + SQLite WAL served by gunicorn 23.0.0, 2 sync workers,
behind an nginx 1.24.0 reverse proxy), under 4-client concurrency and cross-worker
commit visibility.

**Result: SUPPORTS (status=COMPLETE).** All ten mandatory conditions C1–C10 pass with
1.0/0.0 ceiling values on the production WSGI+nginx stack, all four baselines pass, and
the two non-vacuous branches (body-only and header-only drift, both 200 vs 200) are
discriminated deterministically exactly as on localhost. This removes the primary
portfolio blocker: 42 localhost-only experiments left C-MEAS-VALID at EXPERIMENTAL with
`tunnel_flag=true` and no production-middleware evidence.

## 2. Scientific Question

Canonical claim **C-MEAS-VALID**: the HTTP fingerprint substrate discriminates content
and header changes with null stability and writable controls in an operational serving
environment. Frozen question (Director PIVOT): does the *identical* localhost fingerprint
algorithm generalize to gunicorn + nginx reverse proxy — including header
folding/ordering/whitespace normalization, proxy buffering, gunicorn worker isolation,
SQLite WAL cross-worker visibility, and concurrency — without losing discrimination,
isolation, or null stability?

## 3. Measurement Topologies

| Topology | Stack | Port | Role |
|---|---|---|---|
| L (sanity control) | Werkzeug 3.1.8 dev server (threaded), single process | 19870 (free-discovered) | Replicate localhost A-vs-C and A-vs-E discrimination; control for stack change |
| P (primary) | gunicorn 23.0.0, 2 sync workers, 127.0.0.1:19860; nginx 1.24.0 reverse proxy listen 127.0.0.1:19851 (`proxy_pass` to gunicorn upstream, `proxy_http_version 1.1`, `proxy_set_header Connection ""`, `proxy_buffering off`) | 19860 / 19851 | All C1–C10, E1–E4 |

Server: Flask app with `/auth/token`, `/admin/set_body_variant`, `/admin/set_headers`,
`/admin/set_mode`, `/admin/set_role`, `/admin/invalidate_session` (all writes commit to
SQLite WAL before responding 200; verified by post-SELECT), `/resource` (instrumented
with `X-Worker-Pid`), `/protected`.

Fingerprint bodies (frozen pins): A = 31 B (`d0ca833f...`), B = 70 B (`67c186f2...`),
C = 117 B (`b46c461c...`); 403 body 22 B (`387fe7...`), 401 body 25 B (`9df36...`);
non-CLEN headers held constant (Cache-Control `max-age=3600`, ETag `W/"fixed-aaa-111"`,
Vary `Accept-Encoding`, no Set-Cookie) for body-only branches.

## 4. Primary Results

All N=20 batches returned exactly the frozen expected status; body SHA, Content-Length,
header-config, and session/role checks passed on every observation (600/600).

### 4.1 Same-status body-only discrimination (200 vs 200, bodies differ)

| Comparison | full | body | status | headers-no-CLEN | CI (full) |
|---|---|---|---|---|---|
| A vs C (31 B vs 117 B) | **1.0** | 1.0 | 0.0 | 0.0 | [1.0, 1.0] degenerate |
| A vs B (31 B vs 70 B) | **1.0** | 1.0 | 0.0 | 0.0 | [1.0, 1.0] degenerate |
| seq A vs C (sequential baseline) | 1.0 | 1.0 | 0.0 | 0.0 | degenerate |

Content-Length observed 31/70/117, each equal to body_len; non-CLEN filtered headers
byte-identical across A/B/C (verified over all 60 observations per branch). `full > status`
strictly (1.0 > 0.0) — non-vacuous. **C1, C2, C3, C4, C6 pass.**

### 4.2 Header-only discrimination (bodies identical, headers differ)

| Comparison | full | headers | status | body | CI (full) |
|---|---|---|---|---|---|
| A vs E (combined) | **1.0** | 1.0 | 0.0 | 0.0 | [1.0, 1.0] degenerate |
| Iso Cache-Control only | 1.0 | 1.0 | 0.0 | 0.0 | degenerate |
| Iso ETag only | 1.0 | 1.0 | 0.0 | 0.0 | degenerate |
| Iso Set-Cookie only | 1.0 | 1.0 | 0.0 | 0.0 | degenerate |
| seq A vs E (sequential baseline) | 1.0 | — | — | — | degenerate |

Bodies identical 31 B (`d0ca833f...`) and Content-Length 31 == 31 across all header-only
states — no body confound. **C9, C10 pass.**

### 4.3 Null stability (concurrent, 4 clients)

| Null | full | CI | body | status | headers-no-CLEN |
|---|---|---|---|---|---|
| body-A resampled (A1 vs A2) | 0.0 | [0.0, 0.0] | 0.0 | 0.0 | 0.0 |
| header-A resampled (A1 vs A2) | 0.0 | [0.0, 0.0] | 0.0 | 0.0 | 0.0 |
| 403 resampled (null-1 vs null-2) | 0.0 | [0.0, 0.0] | 0.0 | 0.0 | 0.0 |
| 401 resampled (null-1 vs null-2) | 0.0 | [0.0, 0.0] | 0.0 | 0.0 | 0.0 |

**C5 passes**: no false positive under concurrency, FP ≤ 0.05 required, observed 0.0.

### 4.4 Writable controls (cross-worker, SQLite WAL)

| Control | full | statuses | body SHA | null | worker distribution |
|---|---|---|---|---|---|
| Permission escalation 403 vs 200 (`UPDATE users SET role`) | **1.0** (≥0.7) | 403/200 verified | distinct | 0.0 CI [0,0] | {46041:21, 46042:19} ≥10 each |
| Session invalidation 401 vs 200 (`DELETE sessions`) | **1.0** (≥0.7) | 401/200 verified | distinct | 0.0 CI [0,0] | {46041:20, 46042:20} ≥10 each |

Write-to-visible latency measured client-side: role viewer ~7.5 ms, role admin ~7.6 ms,
invalidate session ~7.8 ms (includes HTTP round-trips; commit verified by post-SELECT).
**C7, C8 pass** — commit on worker A visible to worker B within batch time.

### 4.5 Sanity control (Topology L, Werkzeug)

`l_body_AvsC_full=1.0, l_body_AvsC_status=0.0, l_hdr_AvsE_full=1.0, l_hdr_AvsE_body=0.0`
(60 lines) — the localhost behavior replicates exactly before production measurement
proceeds, confirming the stack change is the only independent variable.

## 5. Baselines

- **B-STATUS-ONLY**: 0.0 on all same-status (200 vs 200) comparisons; 1.0 on 403/401
  classic controls — status is inert when held constant. Pass.
- **B-BODY-ONLY**: 1.0 on A vs C and A vs B; 0.0 on nulls and header-only A vs E — body
  carries the full signal in body-only drift. Pass.
- **B-HEADERS-ONLY**: 1.0 on body-only A vs C solely via body-correlated Content-Length
  (31 vs 117) as documented, 1.0 on header-only A vs E via Cache-Control/ETag/Set-Cookie,
  0.0 on nulls. Pass.
- **B-HEADERS-NO-CLEN**: 0.0 on body-only comparisons (no independent header drift) and
  nulls; 1.0 on header-only — independent header signal isolated from Content-Length. Pass.

## 6. Exploratory conditions

- **E1 CI non-degeneracy**: all bootstrap CIs degenerate ([1.0,1.0] / [0.0,0.0]); every
  state has fingerprint set size 1. Declared deterministic (effective distinct N = 1),
  not a precision estimate. No nginx-introduced variance detected: `Connection` was
  constant `keep-alive` on all 380 prod/seq observations (config `proxy_set_header
  Connection ""` + `proxy_http_version 1.1`), so prereg Validity Threat #4 did not
  materialize.
- **E2 header folding**: fold_keys (lowercase keys, shuffled order) vs canonical E →
  full 0.0 (normalization holds); fold_pad (value whitespace padding) vs canonical E →
  full 0.0 (nginx normalizes value padding; value-as-is semantics reported). Sorted/
  lowercased aggregation is robust on this stack. Non-gating (reported).
- **E3 distributed visibility**: two distinct workers seen (`46041`, `46042`), ≥10
  requests per worker on classic pairs, commit visible to both workers ~8 ms.
- **E4 BrowserGym/AgentLab**: NOT_TESTED — docker images unavailable (`IMAGE_UNAVAILABLE`);
  does not gate C1–C10.

## 7. Interpretation

The identical localhost fingerprint algorithm generalizes losslessly to gunicorn + nginx
reverse proxy on loopback: body-only and header-only discrimination remain at ceiling
1.0/0.0, null stability holds under 4-client concurrency, and writable permission/session
controls are visible across both gunicorn workers with no confounding header variance
(introduced `Connection`/`X-Worker-Pid` either held constant or excluded with disclosure).
The production-like stack preserved both the deterministic 1.0/0.0 floor and the
isolation structure (status 0.0, body 0.0, headers-no-CLEN 0.0 where expected).

Per the frozen positive consequence, this expands the C-MEAS-VALID ceiling from
localhost Flask-dev EXPERIMENTAL to production-like gunicorn+nginx EXPERIMENTAL and
unblocks Graph C-DELTA-REPAIR / C-FRESHNESS distributed work and Physics beyond-memory
tests to use this substrate with trustworthy production-middleware evidence. It does NOT
promote C-MEAS-VALID to VALIDATED or PRODUCT_CORE (see §9 unresolved boundaries).

## 8. Validity Notes

1. Fingerprint algorithm byte-identical to parent EXP-RUNTIME-35749360317 (and its
   ancestors); independent recomputation from raw fields (recompute_audit.py) reproduces
   all 600 fingerprints and all 85 comparison metrics with 0 mismatches.
2. Frozen spec mandates client-side lowercasing of filtered header keys before hashing;
   parent stored original-case keys. Cross-experiment fingerprint *strings* therefore are
   not directly comparable, but intra-experiment determinism and audit recomputation are
   unaffected.
3. Frozen-mandated instrumentation header `X-Worker-Pid` is excluded client-side from
   the fingerprint input set (would otherwise inject round-robin pid variance);
   `headers_raw_json` retains the full header set for audit.
4. Raw line count is 600 (60 sanity + 540 production) vs the prereg nominal estimate
   ≈420; the executed frozen itemization (30 states × 20) is authoritative.
5. All bootstrap CIs are degenerate; effective distinct N per state = 1 (deterministic).
6. First execution attempt of this phase completed all batches but crashed in derivation
   code (metrics key alias bug); the run was fixed and re-executed cleanly; only the
   canonical run's artifacts are in this packet.
7. Scope: loopback only (127.0.0.1), no TLS, no HTTP/2, no real CDN, no multi-host Redis,
   no BrowserGym.

## 9. Unresolved

- Real paid-tier CDN (HIT/SWR/SIE/304), TLS/HTTP2, multi-host load balancing untested.
- BrowserGym/AgentLab substrate untested (E4 NOT_TESTED).
- Multi-host Redis shared-state replication untested (single-host SQLite WAL used).
- Value-magnitude gradient beyond 31/70/117 B and 3 header variants (still at ceiling).
- Vary-only isolation not measured independently.

## 10. Decision

`status=COMPLETE`, `outcome=SUPPORTS`. All mandatory C1–C10 pass; all baselines pass;
E1 deterministic, E2 folding robust, E3 cross-worker visible, E4 NOT_TESTED.
C-MEAS-VALID ceiling expands to production-like WSGI+nginx (EXPERIMENTAL, not
VALIDATED/PRODUCT_CORE). Next: CDN HIT/SWR/SIE analogue or BrowserGym WebArena hold-out
to lift the claim further.