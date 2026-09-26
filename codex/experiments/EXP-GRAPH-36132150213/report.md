# EXP-GRAPH-36132150213 — EXECUTE Report

**Lane:** graph  
**Claim:** C-FRESHNESS  
**Status:** `MEASUREMENT_INVALID`  
**Outcome:** `NOT_APPLICABLE`  
**Run:** `36132150213`  
**Preflight:** 2026-09-25T12:34:59+00:00

## Executive Summary

The frozen experiment was not allowed to enter outcome-bearing execution. Its mandatory Runtime dependency — a machine-readable capability ledger and one-command bring-up contract for the required 4-worker distributed substrate — was not present in the expected Runtime experiment path, the searched repository scope, or `/tmp/spider-runtime`.

The read-only preflight therefore stopped before starting nginx, gunicorn, the shared-WAL application, HTTP requests, browser observation, or any freshness classification. The producer result is `MEASUREMENT_INVALID` with scientific outcome `NOT_APPLICABLE`. This is an infrastructure/precondition result, **not** a falsification of C-FRESHNESS.

The durable raw diagnostic is [`raw_evidence/preflight.json`](raw_evidence/preflight.json), SHA-256 `f4c75b7c143ecdaf8371c531cd2dffb0e74a64372f95ed063d0a8a009122d20b`.

## 1. Frozen Design and Scope

The immutable packet remains unchanged:

- `request.json` — SHA-256 `c3f698891f43bcb43a97c8cdd989dcef7d3ae69103778485e73263e92e8c5913`
- `spec.json` — SHA-256 `4e406c0b524075f55bac2554b739048f58ce1ac80060c911113ffdccf3759fe9`
- `prereg.md` — SHA-256 `1c56eb558605bf36b1a3e3f2f193b811ef17ad7cbfde1328df175bf60618fccf`
- `freeze.json` — SHA-256 `b0a151030023838c061673403bb168b1685661bd8f52045da0867dbd6f051ce7`

The required design is the deterministic four-signal guard (Jaccard over required DOM fields, endpoint-template drift, CSRF drift, and ETag plus `Cache-Control: max-age=0`) on nginx 1.24.0 with `$request_uri` sticky routing, 4x gunicorn/Flask 3.1.3 with PyJWT HS256, shared SQLite WAL, real 304 revalidation, and verified worker-PID spread. The required D1–D9 thresholds, baselines, controls, prevalence, trajectory-grouped uncertainty, and conditional browser gate were not altered.

## 2. Read-Only Preflight

| Check | Observation | Result |
|---|---|---|
| Frozen input hashes | All three frozen input hashes match `freeze.json` | PASS |
| Runtime capability ledger | `research/experiments/EXP-RUNTIME-36129163700` absent; searched capability-ledger paths returned no artifact | **BLOCKING FAILURE** |
| One-command bring-up contract | No contract found in the expected Runtime path or checked temporary path | **BLOCKING FAILURE** |
| 4-worker substrate | Not started or measured because the certified contract was unavailable | NOT RUN |
| Health gate | Not started or measured | NOT RUN |
| Browser channel | Chromium 153.0.8010.0 is installed, but no Runtime certification for 1280x720 plus CDP `Accessibility.getFullAXTree` was found | UNKNOWN, not a primary HTTP blocker |

The environment did expose nginx 1.24.0, gunicorn 23.0.0, Flask 3.1.3, PyJWT 2.15.0, SQLite 3.45.1, and a Chromium executable. Those version observations do not substitute for the required machine-readable contract or health-gate certification.

No bring-up command, HTTP workload, conditional request, 304 probe, worker-PID spread check, or browser observation was executed. Accordingly, `raw_evidence/raw_evidence_distributed.jsonl`, `health_gate.json`, and `decision.json` do not exist for this run; no substitute measurements were created.

## 3. Measurements

All frozen scientific metrics are explicitly `null` in `result.json` because the measurement transaction did not begin:

- `M-TN-POOLED-WILSON-LOWER`
- `M-FALSE-ACCEPT-POOLED-WILSON-UPPER`
- `M-UNKNOWN-PRECISION-POOLED`
- `M-ECE-GLOBAL`
- `M-ECE-GLOBAL-BOOTSTRAP-97.5`
- `M-ECE-PER-CLASS-MAX`
- `M-MAX-ABS-RHO`
- `M-PC-FRESH-SUCCESS-RATE`
- `M-NC-NOISE-FA-WILSON-UPPER`

Per-family and per-class objects are empty rather than zero-filled. `substrate_started`, `health_gate_pass`, `n_non304`, and `n_distinct_workers` are also `null`: they were not observed, rather than observed as zero.

## 4. Controls and Baselines

The following frozen identities are preserved as `NOT_RUN` with `pass: null`:

| Identifier | Frozen role | Observed |
|---|---|---|
| `PC-FRESH-EXECUTION` | Fresh execution and postcondition positive control | NOT RUN; no substrate |
| `NC-NOISE-IMMUNITY` | Benign-noise null control | NOT RUN; no substrate |
| `B-NO-GUARD` | No-guard matched-log baseline | NOT RUN; no raw workload |
| `B-JACCARD-ONLY` | Jaccard-only matched-log baseline | NOT RUN; no raw workload |
| `B-HEADER-ONLY` | Header-only matched-log baseline | NOT RUN; no raw workload |
| `B-COLD` | Cold full-re-discovery baseline | NOT RUN; no substrate |

No control is marked failed as a scientific result. The unavailable substrate is the reason the controls were not executed.

## 5. Evidence and Interpretation Boundary

**Raw evidence:** the preflight path/version/hash diagnostic in [`raw_evidence/preflight.json`](raw_evidence/preflight.json).  
**Observations:** the ledger and bring-up contract were absent; binaries were present; no workload was started.  
**Derived measurements:** none; all frozen metrics are null.  
**Interpretation:** the mandatory measurement preconditions were unavailable, so the result is measurement-invalid.

Accepted Runtime evidence in `codex/experiments/EXP-RUNTIME-36100549580/` and `codex/experiments/EXP-RUNTIME-36094450333/` documents a bounded 2x plain-HTTP setup. It does not certify the current 4x/ledger contract and was not substituted. The prior distributed Graph result `codex/experiments/EXP-GRAPH-36106653880/` is also not reused as a scientific observation.

## 6. Consequence and Smallest Next Action

C-FRESHNESS receives no update from this packet. No claim promotion, downstream freshness unblocking, or product consequence is authorized.

The smallest unblocking action is for Runtime to publish and certify:

1. a machine-readable capability ledger; and
2. a one-command bring-up contract for nginx 1.24.0, 4x gunicorn/Flask 3.1.3, shared SQLite WAL, real 304 revalidation, and worker-PID health checks.

After that dependency is available, retry the exact frozen request/spec/preregistration without changing thresholds or substituting synthetic fixtures. A valid run must generate the required raw observations before any D1–D9 decision can be made.

## 7. Provenance and Scope

The producer wrote only the target experiment's `raw_evidence/preflight.json`, `result.json`, `report.md`, `provenance.json`, and `failure.json`. It did not edit `SPIDER_CODEX.md`, `codex/claim_state.json`, `codex/index.json`, Runtime artifacts, frozen inputs, or product code. Existing unrelated repository modifications were observed before output and left untouched.

The execution checkpoint records GitHub run `36132150213`; the prior `model_execute.json` records a transient automation failure (`exit_code: 75`, attempt 4), which is not a scientific result. Full commands, environment observations, hashes, and external evidence references are in [`provenance.json`](provenance.json).
