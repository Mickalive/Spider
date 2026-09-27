# EXP-RUNTIME-36129163700 — H1-A-INTERVENTION-VALIDITY (C-MEAS-VALID)

**Status:** COMPLETE  
**Outcome:** SUPPORTS  
**Lane:** runtime  
**Claim:** C-MEAS-VALID (no registry promotion authorized by this packet)  
**Run ID:** 36129163700

## 1. Raw evidence (immutable JSONL/JSON artifacts)

- `artifacts/A-EPISODE-LEDGER.jsonl` — 120 raw episode records (pre/post WAL vectors, logical projections, read fingerprints, statuses, redacted sid refs)
- `artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl` — raw length-framed SHA-256 WAL vectors per episode
- `artifacts/A-RESPONSE-FINGERPRINTS.jsonl` — raw status/body/stable-header fingerprints per episode
- `artifacts/A-DETECTOR-OUTPUT.jsonl` — blind per-episode detector signals (no arm label)
- `artifacts/A-CAPTURE-STABILITY.jsonl` — ten no-action capture pairs
- `artifacts/A-READINESS-CERTIFICATE.json` — raw readiness probe records + derived floors
- `artifacts/A-SEEDED-ORDER.json` — raw seeded episode order archived before scoring
- `artifacts/B-PLAYWRIGHT-CAPABILITY.json`, `artifacts/B-DOM-AX-CAPTURE.json`, `artifacts/B-WAL-EVIDENCE.jsonl` — real browser captures or explicit UNAVAILABLE records
- `artifacts/capability_ledger.json` — same-run machine-readable capability ledger
- `artifacts/D-DURABILITY-CHECK.json` — HEAD/worktree comparison

## 2. Observations (direct, not interpretations)

- Readiness certificate: n_total=None n_non304=None n_304=None per_ep=None distinct_workers=None min_stickiness=None missing_on_200=None
- Capture stability: 10/10 no-action WAL-vector pairs byte-identical over the frozen 250 ms interval
- Part A matrix: 120 episodes executed (20 per arm x 6 arms) in the seeded order archived at artifacts/A-SEEDED-ORDER.json
- Part A verdict: SUPPORTS — P-WRITE: 1.0 [0.8388748419471806, 1.0]; P-DRIFT: 1.0 [0.8388748419471806, 1.0]; N-READ: 1.0 [0.8388748419471806, 1.0]; N-INVALID: 1.0 [0.8388748419471806, 1.0]; N-EXPIRED: 1.0 [0.8388748419471806, 1.0]; N-DELETED: 1.0 [0.8388748419471806, 1.0]
- Part B (non-vetoing): UNAVAILABLE
- Part C contract: AVAILABLE
- Durability: UNSATISFIABLE (REFERENCE_ONLY)

## 3. Derived measurements (computed from raw evidence only)

- Part A verdict: **SUPPORTS**
- P-WRITE: sensitivity k=20/20 point=1.0 Wilson95%=[0.8388748419471806, 1.0] nondegenerate=True
- P-DRIFT: sensitivity k=20/20 point=1.0 Wilson95%=[0.8388748419471806, 1.0] nondegenerate=True
- N-READ: specificity k=20/20 point=1.0 Wilson95%=[0.8388748419471806, 1.0] nondegenerate=True
- N-INVALID: specificity k=20/20 point=1.0 Wilson95%=[0.8388748419471806, 1.0] nondegenerate=True
- N-EXPIRED: specificity k=20/20 point=1.0 Wilson95%=[0.8388748419471806, 1.0] nondegenerate=True
- N-DELETED: specificity k=20/20 point=1.0 Wilson95%=[0.8388748419471806, 1.0] nondegenerate=True
- Pooled descriptive (cannot mask a failed arm): {'pooled_sensitivity_point': 1.0, 'pooled_specificity_point': 1.0, 'note': 'descriptive only; cannot override a failed individual arm'}
- Readiness: n_total=None n_non304=None n_304=None per_ep=None distinct_workers=None min_stickiness=None
- Capture stability: 10/10 pairs byte-identical
- Part B: UNAVAILABLE; Part C: AVAILABLE; Durability: UNSATISFIABLE

## 4. Controls

| control | pass | observed |
|---|---|---|
| V-NGINX-CONFIG-OK | True | nginx: the configuration file /tmp/single.db.nginx.conf syntax is ok
nginx: configuration file /tmp/single.db.nginx.conf test is successful |
| V-SINGLE-HASH | True | count=1 |
| V-CACHE-ENABLED | True | proxy_cache_path+proxy_cache+proxy_cache_valid+proxy_temp_path+bypass present |
| NC-CACHE-DISABLED-REJECTED | True | cache enabled |
| NC-EXCLUSIVE-NGINX | True | 1 master(s): root       49055  0.0  0.0  21452  1720 ?        Ss   03:34   0:00 nginx: master process nginx -c /tmp/single.db.nginx.conf |
| V-FLASK-LISTENING | True | [{'port': 19860, 'listening': True}, {'port': 19861, 'listening': True}] |
| V-HEALTH-GATE | True | nginx:1 attempts missing_on_200=0; origin60_ok=True; origin61_ok=True |
| V-NGINX-NO-PERMISSION-DENIED | True | nginx_error.log clean |
| V-UPSTREAM-2-SERVERS | True | server directives count=2 |
| DIAG-CACHE-MISS-THEN-HIT | True | [{"leg": 1, "status": 200, "x_cache": "MISS"}, {"leg": 2, "status": 200, "x_cache": "HIT"}] |
| V-SUBSTRATE-CERTIFICATE | False | {} |
| V-CAPTURE-STABILITY | True | 10/10 pairs byte-identical |
| V-AUTH-SESSION-BOUNDARY | True | {"P-WRITE": {"statuses": [200], "violations": 0}, "P-DRIFT": {"statuses": [200], "violations": 0}, "N-INVALID": {"statuses": [401], "violations": 0}, "N-EXPIRED": {"statuses": [401 |
| V-A-MATRIX-COMPLETE | True | {"P-WRITE": {"n_complete": 20, "n_scored": 20}, "P-DRIFT": {"n_complete": 20, "n_scored": 20}, "N-READ": {"n_complete": 20, "n_scored": 20}, "N-INVALID": {"n_complete": 20, "n_scor |
| V-RECOMPUTE | True | {} |
| V-B-PUBLIC-API | True | {"status": "AVAILABLE", "executable_path": "/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome", "is_canonical_path": true, "executable_sha256": "8c599d43aec53f2 |
| V-B-REAL-CAPTURE | True | {"status": "AVAILABLE", "page_content_bytes": 2385, "cdp_dom_snapshot_nodes": 28, "ax_tree_nodes": 30, "ax_tree_nodes_with_role": 30} |
| V-C-LEDGER-SCHEMA | True | ledger_written=True schema_complete=True |
| V-DUR-HEAD | False | [{"path": "research/experiments/EXP-RUNTIME-36129163700/run_experiment.py", "head_matches_worktree": false}, {"path": "research/runtime/bringup.py", "head_matches_worktree": false} |
| V-SECRET-REDACTION | True | TESTBED_SECRET appears in no artifact; recorded only as SHA-256+length; tokens recorded as token_class + redacted sid_ref; policy-model capability records env-key presence booleans |
| B-WAL-VECTOR | True | per-episode vector_changed bits in A-WAL-VECTOR-BEFORE-AFTER.jsonl; arm-level: {"P-WRITE": 1.0, "P-DRIFT": 1.0, "N-READ": 1.0, "N-INVALID": 1.0, "N-EXPIRED": 1.0, "N-DELETED": 1.0} |
| B-LOGICAL-STATE | True | pre/post logical projections per episode in A-EPISODE-LEDGER.jsonl |
| B-RESPONSE-FINGERPRINT | True | per-episode fingerprint_changed bits in A-RESPONSE-FINGERPRINTS.jsonl |
| B-STATUS-ONLY | None | status-only separation is a proxy for the assigned condition; primary detector is semantic+side-effect |
| B-STATIC-REPEAT-NULL | True | 10/10 identical |
| B-NO-SYNTHETIC-FALLBACK | True | every unavailable fact is recorded UNAVAILABLE/ERROR with evidence and one smallest unblocking action; no fabricated observation exists in any artifact |
| PC-A-VALID-WRITE | True | k=20/20 |
| PC-A-INDUCED-DRIFT | True | k=20/20 |
| PC-B-REAL-BROWSER | False | UNAVAILABLE |
| PC-C-CONTRACT | True | AVAILABLE |
| NC-A-READ-ONLY | True | specificity=1.0 k=20/20 |
| NC-A-INVALID-AUTH | True | specificity=1.0 k=20/20 |
| NC-A-EXPIRED-AUTH | True | specificity=1.0 k=20/20 |
| NC-A-DELETED-SESSION | True | specificity=1.0 k=20/20 |
| NC-A-STATIC-CAPTURE | True | 10/10 identical |
| NC-B-NO-SYNTHETIC | True | all browser/WAL facts derive from real captures or are explicitly UNAVAILABLE |

## 5. Interpretation

Part A (primary) measured the frozen intervention-validity matrix on the certified distributed shared-WAL plain-HTTP substrate. The verdict is **SUPPORTS** in the exact bounded setting (2x gunicorn 23.0.0 @127.0.0.1:19860/19861 sharing /tmp/single.db WAL with wal_autocheckpoint=0, exclusive nginx 1.24.0 @19851, hash $request_uri consistent, real proxy_cache, plain HTTP localhost). This does not validate browser, TLS, HTTP/2, multi-host or real-site behavior.

Part B is a standalone, non-vetoing capability result: **UNAVAILABLE**. Its outcome never alters Part A raw evidence, derived metrics or validity status.

Part C is a contract result: **AVAILABLE**. Durability is **UNSATISFIABLE** (REFERENCE_ONLY) — a bounded contract result under the lane no-commit rule, not a scientific falsification.

## 6. Validity notes

- sudo available: nginx master started as root with user www-data workers; cache/temp dirs chowned www-data.
- The detector was blind to the arm label; the label was joined only after detector output was written.
- No synthetic fallback exists anywhere; every unavailable fact is recorded UNAVAILABLE/ERROR with evidence and one smallest unblocking action.
- TESTBED_SECRET is recorded only as SHA-256 + length; tokens appear only as token_class + redacted sid_ref.
- The frozen private-helper gate from the voided parent packet is NOT used; Part B uses only the documented public Playwright API.

## 7. Unresolved

