# EXP-PRODUCT-35954196999 — Executive Report

- **Lane:** product | **Status:** MEASUREMENT_INVALID | **Outcome:** INCONCLUSIVE
- **Claim under exam:** C-PRODUCT-ECON (DIE/SURVIVES per frozen C1–C4 gate suite)
- **Frozen falsifier precedence:** DIE triggers on any PC fail OR single-node substrate absent OR n_non304<800 OR BrowserGym 0.14.3 + gpt-4o-mini unavailable (`rho_proxy_real` unmeasurable ⇒ "Docker replication gates SURVIVES per Director else MEASUREMENT_INVALID irrespective of proxy economics") OR $request_uri sticky violated OR If-None-Match not exercised OR SGDR index missing OR fixtures missing OR kernel dot-regex not patched. **No file-proxy fallback.**

## RAW EVIDENCE (what was observed, not interpreted)

Levels are kept distinct per the packet contract: RAW EVIDENCE → OBSERVATION → DERIVED MEASUREMENT → INTERPRETATION → AUDIT → DECISION. Raw evidence lives in `artifacts/env_audit.json` (13 observations in `result.json`).

1. Frozen inputs byte-identical to freeze.json (request 50088843, spec 5cf9297b, prereg ba516310, freeze 810514ca).
2. HEAD 30c57a10; prior EXECUTE attempts (failure.json code 76; model_execute.json attempt 3 exit 76 output-missing) produced no packet.
3. Kernel at HEAD: pre-patch regex (no dot), sha 46929b3a; parent verdict commit dac04e60 did NOT carry the patched kernel (blob cfec9866). Patch re-applied → sha d926279d (matches frozen `d926279d` prefix).
4. MV2 spot check 5/5 EXECUTABLE with correct dot binding; family gate abstains UNKNOWN; confidence-0.5 → EXPLORE. `tests/test_kernel.py` 3/3 PASS.
5. Scientific stack absent at run start; installed: numpy 2.5.3, scipy 1.18.1, sklearn 1.9.1, pandas 3.0.6, flask 3.1.3, pyjwt 2.15.0, gunicorn 26.2.0, requests 2.34.2 (frozen pins 23.0.0 / 2.14.0 → drift).
6. Docker pull `ghcr.io/servicenow/browsergym:0.14.3` → **denied**; no BrowserGym image locally; browsergym 0.14.3 on PyPI index but not installed.
7. OPENAI_API_KEY unset (only GH_TOKEN) → gpt-4o-mini unavailable.
8. `/tmp/spider-runtime` absent; shared.db absent anywhere; nginx 1.24.0 present but stock config, not running; no listener on 80/8080/8000. n_non304 = null.
9. Fixtures present (prior-run paths only): qcr_bank 8c69804b (36 fam, TAU 0.30, Jaccard<0.30), webmcp 2147/714 (af3c18e5 / 8e106525), cost_config 55fa25af, curated 0219b15f, tasks 192/36 census 391e8f6c. **sgdr_index absent repo-wide.**
10. Dependency lanes: runtime C-MEAS-VALID **MEASUREMENT_INVALID** (EXP-RUNTIME-35949568321, gunicorn wsgi import loop); graph EXP-GRAPH-35952148696 SURVIVES_CURRENT_TEST but **only on synthetic flat-JSON** — health-gated substrate transfer explicitly open.

## OBSERVATION → DERIVED MEASUREMENT

- MV2 kernel sub-gate: **CLEARED** (5/5 EXECUTABLE, tests 3/3, sha d926279d = frozen identity).
- MV5 Docker gate: **FAIL** (image pull denied; no key).
- MV3 substrate gate: **FAIL** (no /tmp/spider-runtime, no shared.db, no sticky $request_uri, no If-None-Match 304).
- PC2 SGDR gate: **FAIL** (index absent).
- MV1 census staging: **NOT STAGED** for this experiment (prior-run fallback 192/36 present only).
- All economics metrics: **null** (explicitly not available, not zero).

## INTERPRETATION

The frozen decision rule fires **multiple independent DIE triggers** → **MEASUREMENT_INVALID / INCONCLUSIVE** is the correct status regardless of economics. This is substrate/infrastructure failure, **not scientific falsification** of C-PRODUCT-ECON. No economics numbers were invented (file-proxy/bijective/random proxies banned by freeze). The Director's REOPEN stacking dependencies (runtime single-node HS256 honesty gate, graph single-node freshness TN≥0.85) were not satisfied this cycle, consistent with the DIE.

**Consumers should carry forward:** `established` = MV2 kernel gate now verified-and-tested (but patch is **not durable** in the committed tree — it must be committed with any verdict); scientific stack is now installable. `rejected`/`unknown` = all economics claims remain unmeasurable; prior file-proxy numbers remain bounded file-proxy evidence only. **do_not_assume** = do not assume substrate/key/index/census exist; do not treat the 192/36 fallback as the Hard-258 census; do not treat synthetic flat-JSON graph results as health-gated validation.

## Controls

| ID | Status | Notes |
|----|--------|-------|
| PC-SINGLE-NODE-PARETO-CORRELATED | UNKNOWN | kernel sub-gate PASS; substrate/SGDR/registry sub-gates FAIL/UNKNOWN |
| NC-SINGLE-NODE-SHUFFLE-PIPELINE | UNKNOWN | not runnable: no pipeline |
| B-COLD, B-RAG-EMBED-TAU030-QCR, B-STAGEHAND-CACHE | UNKNOWN | not measurable without substrate |
| P-STAGEHAND-TTL-CORRELATED, P-DSM-COMPILE-O1, P-SGDR-AWM | UNKNOWN | substrate/SGDR absent |

## Smallest next actions (see `result.json.unresolved`)

1. OPENAI_API_KEY + pullable BrowserGym 0.14.3 image → measure rho_proxy_real.
2. Fix runtime lane wsgi import loop; provision /tmp/spider-runtime shared.db WAL, gunicorn 23.0.0 single-worker, nginx sticky $request_uri, PyJWT 2.14.0, If-None-Match/ETag loop, n_non304≥800.
3. Build sgdr_index (36 state_key TRAIN-only) + stage this experiment's census/fixtures.
4. Commit the MV2 kernel patch (durability fix).
5. Then run PC1–PC5, NC1–NC4, C1–C4 with bootstrap5000/block-permutation5000 before any SURVIVES/FALSIFIED/SUPERSEDE decision.