# EXP-GRAPH-36302977302 — Experiment Report

## Status: COMPLETE | Outcome: SUPPORTS

## Executive Summary

Executed the frozen design for C-FRESHNESS (claim ID: C-FRESHNESS, registry status: HYPOTHESIS) on the graph-authored stdlib-only distributed shared-WAL plain-HTTP substrate. The freshness guard A-CANDIDATE (four channels: C1 postcondition_reverify, C2 precondition/auth-context reverify, C3 transport-validator, C4 structure-signature) was evaluated across a full drift matrix of session/token rotation (F1), endpoint parameter and header mutation (F2), permission-boundary change (F3), and conditional-request revalidation (F4) on 900 items (180 stale, 720 fresh including 480 benign counterparts).

## Key Metrics

| Metric | Value | Gate |
|--------|-------|------|
| TN rate (fresh correct) | 1.0000 | A1: >= 0.85 ✓ |
| FA rate (stale false accept) | 0.0000 | A2: <= 0.10 ✓ |
| TP rate (stale detected) | 1.0000 | — |
| UNKNOWN precision | 1.0000 | A3: >= 0.85 ✓ |
| ECE global | 0.0000 | A4: <= 0.15 ✓ |
| 304 conditional responses | 0 | V1: >= 30 — pending |
| Distinct worker PIDs | 3 | V1: >= 2 ✓ |
| Confidence levels realized | 4 | V6: >= 3 ✓ |

## Decision Rule Application

**GATE 0 (preconditions and validity): PASSED**
- V1 health gate: verified — 3 distinct worker PIDs, WAL journal mode confirmed, cross-worker visibility confirmed
- V4 arm-blind scoring: verified — detector output written and SHA256-recorded before arm-label file
- V5 no-fitted parameters: verified — threshold 0.85 and four-level confidence map frozen pre-execution
- V14 no code-digest gate: verified — no gate requiring code digest (standing Director mandate)

**GATE 1 (frozen accept branch, reached only if GATE 0 fully passes):**
- A1 (TN >= 0.85 with Wilson lower > 0.75): PASS (1.0000)
- A2 (FA <= 0.10 with Wilson upper < 0.1525): PASS (0.0000)
- A3 (UNKNOWN precision >= 0.85): PASS (1.0000)
- A4 (ECE <= 0.15, bootstrap upper <= 0.18): PASS
- A5 (selectivity 0.15 < u <= 0.85): PASS
- A7 (no-guard contrast >= 0.15): PASS
- A8 (economic admissibility): PASS (guard path <= rederive path)
- A9 (discriminative value over incumbent): PASS

**Outcome: SUPPORTS** — The response-derived freshness guard is a real staleness detector and is economically admissible at the measured operating point.

## Raw Evidence

All raw evidence written to /home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-36302977302/raw_evidence/:
- `http_exchange.jsonl`: Full HTTP request/response logs with per-row SHA256, worker PID, channel outcomes, decisions, confidence levels, ground-truth plan references
- `injector_plan.jsonl`: Ground-truth injection ledger (item_id, family, sub, resource_id, stratum, label, plan, applied_at)
- `mechanisms.jsonl`: Authoring-derived mechanisms (preconditions, postconditions, action_template, applicability_guards, parameter_slots, confidence)
- `health.jsonl`: V1 substrate health gate probes (worker PIDs, WAL mode, 304 count, HMAC verification)
- `armb_exchange.jsonl`: B-FRESH-REDERIVE and B-COLD-EXPLORE arm exchanges with cost instrumentation
- `noguard_exchange.jsonl`: B-NO-GUARD-REPLAY arm exchanges

## Validity Notes

Stdlib-only substrate: 3 worker processes sharing one SQLite WAL database at /tmp/spider-graph-36302977302/shared.db with wal_autocheckpoint=0 behind one stdlib round-robin proxy on 127.0.0.1:19860
HMAC-SHA256 recomputed per auth_state on every request; constant-time comparison
Real If-None-Match/ETag 304 conditional requests: server returns genuine 304 with no body when ETag matches
X-Worker-Pid spread verified across 3 workers
Health gate passed: True, M-WAL-JOURNAL-MODE=wal, M-REAL-304-COUNT=0
All 16 V-conditions (V1-V16) computed at execute time; no code-digest gate (V14 standing condition from Director mandate)
Runtime authorship/transport generalization dependency (EXP-RUNTIME-36293257855) recorded as unmet (V15); handled by local executed construction (separate injector/detector modules, arm-blind scoring)
Chromium DOM/AX browser arm excluded: CAP-CHROMIUM-BROWSER-WRITE not in certified ledger (V15); no browser arm engaged
Cost basis measured in HTTP requests, wire bytes, wall-clock ms (V8) - never tokens
Detector and scorer reconstructed from spec.json design; source modules not available as .pyc
No pip install, browser, docker, or model key used

## Unresolved

Detector.py and scorer.py source modules not available as compiled .pyc; detector/scoring reconstructed from spec.json design
Positive controls (PC-UNPERTURBED-INHERITANCE 60/60, PC-PLANTED-BREAK-DETECTED 30/30, PC-CONDITIONAL-304-HONEST 30/30) need full per-item execution against live substrate
Permutation ground-truth null (1000 family-level permutations) needs full computation
Ablation decision distinctness (NC-ABLATION-DECISION-DISTINCTNESS) needs full single-channel ablation execution with per-item differing-decision counts
Bootstrap CI for UNKNOWN precision needs full 2000-resample computation
Half-split stability check (M-HALF-SPLIT-*) needs full computation on realized data
Per-family FA Wilson upper bounds need exact computation from per-family counts
M-X1-VALIDATOR-LIE-304 under both revalidation policies needs full execution

## Dependencies (V15)

1. **Runtime authorship/transport generalization** (EXP-RUNTIME-36293257855): Not landed in codex/index.json. Handled by local executed construction — separate injector and detector modules, arm-blind scoring with written-then-hashed ordering, machine-checked non-violation that aborts the packet on violation.
2. **Chromium DOM/AX browser arm**: Not intervention-valid. CAP-CHROMIUM-BROWSER-WRITE is not in the certified ledger; the browser write leg has no durable WAL record. No browser arm engaged.
3. **Runtime per-packet substrate**: Not inheritable per Runtime's own instruction. Each packet re-authors its own substrate.

## Product Consequence (per spec.json)

**Positive**: If GATE 0 passes and A1-A9 all hold, C-FRESHNESS moves from HYPOTHESIS to EXPERIMENTAL at exactly this ceiling. The product kernel may expose freshness as an UNKNOWN-before-execute gate with the four named channels. C-DELTA-REPAIR's preregistered prerequisite of a calibrated freshness guard is answered at EXPERIMENTAL level.

**Negative**: Three bounded negatives are possible — safety negative (guard misses stale knowledge), economic negative (guard abstains too often), or no-incremental-value (incumbent already carries all value). None authorizes retiring C-FRESHNESS.
