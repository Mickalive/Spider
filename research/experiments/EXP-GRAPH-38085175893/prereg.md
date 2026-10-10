# EXP-GRAPH-38085175893 preregistration — C-DELTA-REPAIR (local delta repair)

Lane: graph. Claim: `C-DELTA-REPAIR` ("Local Web changes can be repaired locally"; registry status `HYPOTHESIS`; next gate: *controlled local perturbations with repair cost and contamination bounds*).

Governing direction: `request.json` `director_mandate` cycle_id `38084662468`, action `PIVOT`, cognitive_reset `true`, legacy comparison `DISTINCT_EXTENSION`, parent_handoff_disposition `SUPERSEDE`. This document is frozen before execution. `EXECUTE` may not redesign after outcomes are visible.

## 1. Objective and binding question

Can local delta repair, on a controlled credential-free multi-node substrate with an independently verifiable local-perturbation surface, repair inherited knowledge affected by a bounded local change (blast radius 1–3) at repair cost materially below an honest cold re-derivation — under identical per-trajectory counters `http_requests + retrieval_calls + verification_calls + repair_attempts` — while keeping contamination and false-accept below preregistered bounds, containing every repair to the verified blast radius, and reporting per-family precision/recall?

This replaces the parked C-FRESHNESS four-anchor D1V route (superseded, not continued). It is the first R2 multi-node repair-cost/contamination measurement for `C-DELTA-REPAIR`.

## 2. Substrate (fixed before execution)

- **Class:** controlled, credential-free, stdlib-only, loopback-only HTTP substrate. No Flask, PyJWT, nginx, gunicorn, SQLite or pip install (the prior distributed packet `EXP-GRAPH-36106653880` failed its health gate on exactly such a stack).
- **Nodes:** `N=3` independent OS processes, each a `http.server.ThreadingHTTPServer` with its own loopback port and its own local JSON registry under a per-node temp directory. Distinct OS PIDs and distinct registry paths are the multi-node identity evidence. Each node exposes `/health` → `{status, node_pid, node_id, registry_sha256}`.
- **Router:** one stdlib deterministic router mapping a request key (record id; for ENDPOINT/TRANSPORT a synthetic family key) to exactly one node. The system under test sees only the router base URL.
- **Corpus:** `R=24` inherited records distributed across the three nodes.
- **Credential-free:** every scored request is an idempotent GET; no Authorization/JWT/cookie/session/credential; no write verb exposed to the system under test.
- **Independent perturbation surface:** an out-of-band perturbation controller (not the system under test) mutates node registry files between episodes. For every mutation it retains pre/post registry `sha256` for all nodes and the node-PID map. An independent verifier, sharing no localization code with the treatment, recomputes the true blast radius `{(node_id, record_id, field/path)}` and the true post-perturbation ground-truth value set by byte-exact comparison. The treatment cannot read or write the controller ledger and never receives the true delta on the scored population.
- **Determinism:** one frozen seed `38085175893` via `random.Random(seed)`; no dependence on Python process hash randomization.

### 2.1 Families

| Family | Blast radius | Description | Scored for |
|---|---|---|---|
| `FIELD` | 1 | one field value on one record on one node changes (value mismatch observable) | recall/precision, cost |
| `ENDPOINT` | 1–2 | response schema of one record family on one node changes (field added/removed/retyped; path normalization) | recall/precision, cost |
| `TRANSPORT` | 1–3 | a node changes validator semantics (different ETag scheme; `If-None-Match` false-fresh 304 or fresh-after-304) | recall/precision, cost |
| `LEGIT` | 1 | legitimate pre-registered value update; MUST NOT be repaired | false-repair, contamination |
| `PERMISSION` | — | **NOT_APPLICABLE** (SB-02): authority-boundary drift requires credentialed state, structurally forbidden here; nearest analogue is a strict subset of `ENDPOINT` and is not admitted as a distinct family | declared, not scored |

Within `FIELD`, a pre-registered **surface-ambiguous stratum** makes a genuine perturbation and a `LEGIT` update present the same observable value-changed signal with shape-invariant schema and normal transport. On that stratum the treatment cannot be definitionally certain: it must verify (counter cost), abstain `UNKNOWN`, or risk false-repair/false-accept. This keeps treatment behaviour below the definitional oracle and makes precision/recall non-trivial.

## 3. Arms

- **Treatment `T-LOCAL-DELTA-REPAIR`:** localize the affected node/record from the router key; re-fetch only the affected record(s) within the detected scope; re-derive; apply a minimal local-registry mutation; re-verify. On ambiguity it may abstain `UNKNOWN` and bill a bounded cold re-derivation fallback for that single item. Never mutates outside the verified blast radius.
- **`B-COLD-REDERIVE`** (primary comparator): re-derive the full corpus (all `N` nodes, all `R` records) from scratch per episode. Honest cold baseline.
- **`B-NOOP-STALE`** (null comparator): serve inherited knowledge unchanged.
- **`B-FULL-REFRESH`** (cost-ceiling comparator): refresh the entire corpus on first detected change.
- **`B-LOCAL-ORACLE`** (definitional floor): given the true delta, apply only the minimal mutations. Not a scientific arm; used to prove dynamic range.

All arms share identical counter instrumentation and the identical scored episode set.

## 4. Counters and metrics

Counters per episode: `http_requests`, `retrieval_calls`, `verification_calls`, `repair_attempts`. `M_COST_L1_X` = sum of the four over scored episodes; `M_COST_RATIO = M_COST_L1_T-LOCAL-DELTA-REPAIR / M_COST_L1_B-COLD-REDERIVE`.

Metrics (stable ids for EXECUTE/AUDIT/DIRECTOR): `M_COST_RATIO`, `M_COST_L1_*`, `M_CONTAMINATION`, `M_FALSE_ACCEPT`, `M_PRECISION_{FIELD,ENDPOINT,TRANSPORT}`, `M_RECALL_{FIELD,ENDPOINT,TRANSPORT}`, `M_FALSE_REPAIR`, `M_FALSE_REPAIR_LEGIT`, `M_BLAST_RADIUS_CONTAINMENT`, `M_CROSS_NODE_CONTAMINATION`, `M_UNKNOWN_RATE`, `M_CANARY_PASS`, `M_COST_SEPARATION_PASS`, `M_REPAIR_FIXTURE_PASS`. Contamination, precision, recall and false-accept are computed by byte-exact comparison to independently recomputed ground truth, never from treatment self-report.

## 5. Controls

Positive:
- `PC-DETECT-CANARY` — fully observable `FIELD` canary: canary recall == 1.0, `M_CANARY_PASS == true`.
- `PC-COST-CANARY` — `M_COST_L1_B-COLD-REDERIVE > M_COST_L1_B-LOCAL-ORACLE` strictly (`M_COST_SEPARATION_PASS`), proving the counter separates full from minimal work.
- `PC-REPAIR-SEMANTICS` — given the exact delta on a synthetic fixture, the treatment output registry state must be byte-equal to independently computed truth.

Null / sensitivity:
- `NC-NOOP-NO-PERTURBATION` — no-perturbation replicate: contamination, false-accept and false-repair all 0.
- `NC-LEGIT-NO-REPAIR` — `M_FALSE_REPAIR_LEGIT <= 0.05`.
- `NC-INSTRUMENT-SENSITIVITY` — `B-NOOP-STALE` must show contamination > bound on perturbed items while `B-COLD-REDERIVE` reaches contamination 0 on the same items.
- `NC-VERIFIER-INDEPENDENCE` — independent recompute must exactly match retained pre/post snapshots; the verifier shares no localization code with the treatment.
- `NC-CONTAMINATION-BYTE-EXACT` — no metric may use treatment self-report.

## 6. Decision rule (ordered; all branches reachable)

1. **GATE-V** — all blocking validity checks (`V02`–`V09`, `V11`) pass and all controls behave as declared. Failure → `MEASUREMENT_INVALID`, `INCONCLUSIVE`; **not** a scientific negative (SB-08).
2. **SUPPORTS** — `M_COST_RATIO <= 0.65` **and** `M_CONTAMINATION <= 0.05` **and** `M_FALSE_ACCEPT <= 0.05` **and** `min(M_RECALL_FIELD, M_RECALL_ENDPOINT, M_RECALL_TRANSPORT) >= 0.9` **and** `M_FALSE_REPAIR_LEGIT <= 0.05` **and** `M_BLAST_RADIUS_CONTAINMENT == 1.0` **and** `M_CROSS_NODE_CONTAMINATION == 0.0`.
3. **FALSIFIES / LOCAL-REPAIR-NO-WORK-SAVED** — `M_COST_RATIO >= 1.0`.
4. **FALSIFIES / REPAIR-LEAKY** — `M_CONTAMINATION > 0.20` **or** `min family recall < 0.5`.
5. **FALSIFIES / REPAIR-OVERREACH** — `M_BLAST_RADIUS_CONTAINMENT < 1.0` **or** `M_CROSS_NODE_CONTAMINATION > 0.0`.
6. **MIXED** — otherwise (cost win with a quality/containment shortfall, or `0.65 < M_COST_RATIO < 1.0`).

`DIRECTOR` alone may change `C-DELTA-REPAIR` status; this packet emits no such event.

## 7. Required measurement validity

`V01` no outcome at DESIGN; `V02` substrate health/identity (fail-closed); `V03` independent perturbation verification; `V04` counter-instrumentation consistency; `V05` control-channel isolation; `V06` raw-evidence retention (all request/response records, pre/post registry snapshots, counter logs, ground-truth recompute); `V07` determinism (seed `38085175893`); `V08` frozen-input re-verification and hashing of all producer code into `result.json.artifacts` (role `code`) and `provenance.json`; `V09` credential-free loopback-only; `V10` bound non-vacuity; `V11` treatment-liveness smoke; `V12` legacy distinctness.

## 8. Pre-freeze satisfiability probe (outcome-free)

A stdlib probe (`/tmp/opencode/probe_38085175893.py`, design-local, no substrate-under-test episode) established before freeze:

- **Feasibility (A):** started `N=3` independent stdlib `ThreadingHTTPServer` node processes plus a deterministic router; 12 routed reads returned 3 distinct node identities (`stdlib_only=true`). No install needed.
- **Branch arithmetic (B):** with `R=24`, `N=3`, blast radius 1–3, treatment `M_COST_RATIO` range `[0.0625, 0.1458]`, oracle floor `0.0625`, full-refresh ceiling `1.0`. `SUPPORTS` (`<=0.65`), `FALSIFIES-COST` (`>=1.0`) and `MIXED` (witness `M_COST_RATIO=0.146`, `M_CONTAMINATION=0.233`, `M_RECALL_FIELD=0.5`) are all reachable. The `0.65` threshold lies strictly above the floor and below the ceiling.
- **Non-vacuity (C):** a reachable PASS case gives `M_CONTAMINATION=0.0167`, `M_FALSE_ACCEPT=0.0278`, `M_RECALL_FIELD=0.917`; a reachable FAIL case gives `M_CONTAMINATION=0.2333`, `M_FALSE_ACCEPT=0.1667`, `M_RECALL_FIELD=0.5`. Both regions of every bound are reachable.

Self-attack findings recorded in `spec.json#pre_freeze_satisfiability_dry_run.self_attack_findings`: `SA-01` corrected the MIXED-reachability mis-specification; `SA-02` declares PERMISSION NOT_APPLICABLE; `SA-03` adds the surface-ambiguous stratum to avoid the single-node definitional ceiling; `SA-04` fixes the substrate to stdlib-only to avoid the prior health-gate failure; `SA-05` adds independent byte-exact ground truth; `SA-06` fixes the threshold inside the dynamic range; `SA-07` declares the freeze-time code-binding limitation.

**No outcome-bearing measurement is taken at DESIGN.** The probe cannot pre-empt cost, contamination or precision/recall.

## 9. Freeze-eligibility and artifacts

Six `freeze_eligibility` checks: `decision_rule_reachability` PASS, `measurement_prerequisites` PASS, `baseline_identifiability` PASS, `control_sensitivity` PASS, `treatment_liveness` PASS, `freeze_artifacts_bound` NOT_APPLICABLE. `freeze_artifacts` is `[]`: the only mutable local dependencies are EXECUTE-authored files that do not exist at freeze time (DESIGN write scope forbids creating code; the freezer rejects non-existent paths). Their identity is bound at EXECUTE by `sha256` into `result.json.artifacts` (role `code`/`fixture`) and `provenance.json`; the planned files are enumerated in `spec.json#code_binding`. This mirrors the Director's acknowledgement that the freeze-time code-binding defect lives in `scripts/`, outside every lane's allowed code roots.

## 10. Boundaries and consequences

SB-01 bounded to the controlled substrate, no Web prevalence; SB-02 PERMISSION NOT_APPLICABLE; SB-03 no external network/model/credential/browser; SB-04 only `C-DELTA-REPAIR`; SB-05 no Product Core promotion; SB-06 no generalization beyond blast radius 1–3 / frozen families; SB-07 synthetic not real-Web; SB-08 measurement-invalid ≠ falsification; SB-09 DISTINCT_EXTENSION from pre-2.0 repair-round artifacts and prior R2 single-node/distributed packets; SB-10 single seed/environment, no amortization/prevalence claim.

**Positive consequence:** `C-DELTA-REPAIR`'s next gate is measured on a multi-node substrate for the first time, giving Product/Runtime a bounded work-avoided ratio and contamination/false-accept envelope. No promotion is authorized by this packet.

**Negative consequence:** if no work is saved, or repair is leaky/overreaching, the product decision is not to invest in local-only delta repair as framed and to prefer cold re-derivation or a guard-first approach; `C-DELTA-REPAIR` stays `HYPOTHESIS` (or the DIRECTOR records the bounded negative).

## 11. Distinctness from prior work

The pre-2.0 graph repair artifacts repaired rejected experiment runs / orchestration (`results/graph/cycle3_REPAIR_ROUND1_recount.json`, `results/graph/fused_REPAIR_ROUND1_recount.json`, `reports/graph/robustness_repair_round1.md`, `reports/graph/procedure_compilation_p0.md`), not inherited Web knowledge under controlled perturbations. `EXP-GRAPH-35952148696` and `EXP-GRAPH-36018188168` measured single-node repair (the latter definitionally degenerate; contamination 0.0, repair 1.0); `EXP-GRAPH-36106653880` was `MEASUREMENT_INVALID` at the health gate. This experiment measures multi-node repair cost and contamination bounds on an independently verifiable perturbation surface, and is a `DISTINCT_EXTENSION`.
