# EXP-RUNTIME-38110505221 preregistration (Research 2.0, design-contract v2)

Status: DESIGN NOT YET FROZEN. This file and the complete instrument definition are pinned BEFORE any outcome-bearing execution. After the freeze commit, no threshold, cell, arm, constant, endpoint or decision rule may be edited; any post-outcome change converts analysis into exploratory work and supports no confirmatory claim. The frozen scientific content is `spec.json`; this file explains and bounds it and must not contradict it silently.

- experiment_id: `EXP-RUNTIME-38110505221`
- lane: `runtime`
- claim_ids (frozen, v2): `["C-MEAS-VALID"]` — the Director target claim, and the only claim this packet may move.
- director mandate cycle: `38109980663` (action CONTINUE, target `C-MEAS-VALID`, parent_handoff_disposition SUPERSEDE, cognitive_reset true)
- design contract: v2 (six freeze-eligibility checks filled; `freeze_artifacts` empty, see §12)

## 1. Mandate and scope

The Global Research Director (request.json `director_mandate.allocation`) directs a cognitive reset away from the parent handoff `EXP-RUNTIME-37973247935` (a `MEASUREMENT_INVALID` out-of-surface oracle-transfer packet whose repairs are explicitly NOT executed here) and toward blocker B2: the task bank for the flagship inheritance benchmark must give cold/retrieval baselines NON-CEILING dynamic range and a genuine treatment/comparator distinction before any expensive benchmark executes.

The binding strategic question is: can a non-degenerate ASYMMETRIC-DISCOVERY task bank be certified ARITHMETICALLY before freeze — cold re-derivation and a retrieval-shaped comparator demonstrably below the success ceiling at high residual novelty (`B-COLD-RE-DERIVE` and `B-RETRIEVAL-SHAPED` success_rate < 0.95 at novelty >= 0.5 on at least one family, all arms matched correctness >= 0.80), with a real treatment/comparator behavioural distinction, honest per-condition counters (`http_requests + retrieval_calls + verification_calls + repair_attempts`) and a preregistered contamination/dynamic-range certificate — and delivered as a reusable substrate unblocking B2; recording a bounded substrate-class negative and delivering no validated bank if the certificate is unsatisfiable on every credential-free family tested.

Claim scope (strict). Only `C-MEAS-VALID` is addressed. `C-RESIDUAL-NOVELTY` and `C-PARAM-INHERIT` are graph/product claims named as Director dependencies; no event may be emitted for them. `C-FRESHNESS`, `C-DELTA-REPAIR`, `C-LLM-INHERIT`, `C-PRODUCT-ECON`, `C-SEMANTIC-RESOLVE`, `C-WEB-DYNAMICS`, `C-CROSSSITE` are out of scope. This packet does not advance any claim by itself; it supplies a recheckable measurement-substrate fact and leaves the status decision to the DIRECTOR. The prior `C-MEAS-VALID` bounded VALIDATED ceiling (authorship-separated real-Chromium fixture, `EXP-RUNTIME-36293257855`) is neither widened nor narrowed.

## 2. Why this is not a repeat of `EXP-PRODUCT-37989728440`

The predecessor proved a bounded substrate-class negative: on its mandatory-discovery deterministic credential-free REST class, `B-COLD-RE-DERIVE` and `B-RETRIEVAL-SHAPED` both reached success_rate = 1.000 at novelty 0.5 and 0.75 in families F1 and F2, so the bank had ZERO headroom (a null instrument). The root cause, recorded in its report §3, is that discovery was MANDATORY AND SYMMETRIC: every arm could read the session token, the valid resource identifier and the schema per task by explicit GETs, so every arm could always act.

This design makes discovery ASYMMETRIC across a multi-task SESSION. Per session exactly one session-scoped binding is revealed exactly once, in a completion receipt, and is NOT re-derivable from any idempotent endpoint; a context-resetting arm cannot obtain it while a context-retaining arm can. This is the materially different construction the mandate names ("multi-task sessions where one-time session/resource/schema discovery is amortized or cached across tasks"). A fourth re-run of the mandatory-discovery deterministic REST certificate is explicitly EXCLUDED and is not performed.

A second, separate defect is also not repeated: the predecessor's hard pre-freeze certificate (C1) was asserted but not enforced, so it froze with certificate=false (governance defect recorded on `C-MEAS-VALID`). Here the certificate is computed at DESIGN from the frozen construction arithmetic, is re-computed by EXECUTE from the realized deterministic run, and has a reachable fail-loud negative branch (§9).

## 3. Substrate and construction (frozen; arbitrary constants are the design)

Credential-free, deterministic stdlib `http.server` on `127.0.0.1`, SEED = `38110505221` (the run id). Real localhost HTTP; no browser, no model, no credentials, no external network; `model_calls = 0`, `model_tokens = 0`.

Two content families: `F1 = CHAIN-BINDING-RECORDS` (records/documents) and `F2 = CHAIN-BINDING-WIDGETS` (widgets/gadgets), with disjoint abstract vocabulary and wire names.

A session has `K = 8` tasks in a fixed frozen order and exposes:

- `GET /s/{sid}/session` → `{schema: {abstract_field -> wire_field}, resource_base, session_epoch}` — idempotent; required at novelty >= 0.25.
- `GET /s/{sid}/task/{i}` → `{intent, abstract_params, resource_id?}` — for a CHAIN task `resource_id` is OMITTED.
- `POST /s/{sid}/task/{i}/commit` (JSON `{resource_id, wire_field, value, session_epoch}`) → on first success `{ok:true, receipt:{next_resource_id?}}`. Commits are stateful and idempotent-rejected after first success.

Exactly `L = 1` task per session is a CHAIN task. Its required binding (`next_resource_id`) is revealed ONLY in the FIRST successful commit receipt of a designated earlier task; a later read or re-issue of that receipt returns 409/redacted. The binding is session-scoped and rotates per session, so it is stale in any other session.

Novelty ladder (frozen): `0.00` no discovery required (direct action works); `0.25` schema required, no chain; `0.50` schema required, chain task index 5, binding revealed in task 4's receipt; `0.75` schema required, chain task index 7, binding revealed in task 5's receipt (deeper carry, so a one-step-only arm fails while a true context-retaining arm passes).

## 4. Arms (frozen identities, reused verbatim by EXECUTE/AUDIT/DIRECTOR)

- `T-AMORTIZED-DISCOVERY` (treatment): fetch `/session` once; retain a session context; record `next_resource_id` when present; apply it to the chain task; never re-fetch `/session`.
- `B-COLD-RE-DERIVE` (mandated baseline): clear context after every task; re-fetch `/session` before every task; never consult a prior receipt. Solves the K−L non-chain tasks; the chain task fails and execution continues.
- `B-RETRIEVAL-SHAPED` (mandated comparator): like cold, plus one cross-session retrieval (surface similarity on abstract intent + family, top-K=1) reusing the retrieved wire mapping and `next_resource_id`; the retrieved binding is stale. Counts `retrieval_calls = 1` per task.
- `B-EMPTIED-CONTEXT` (null/ablation): identical to the treatment but with context force-cleared after every task; predicts `== B-COLD-RE-DERIVE`.

Honest counters per trajectory: `http_requests`, `retrieval_calls`, `verification_calls` (1 per commit attempt), `repair_attempts` (1 per failed commit re-attempt, capped at 1), `model_calls` (0), `model_tokens` (0), `latency_ms` (advisory only). Predicted high-novelty per-session `http_requests`: T = `1+8+8 = 17`; `B-COLD-RE-DERIVE` = `8+8+8 = 24`; `B-RETRIEVAL-SHAPED` = `8+8+8+8 = 32` plus 8 `retrieval_calls`.

## 5. Cells, seeds, scoring

`2 families × 4 novelty levels × 4 arms × N_SESSIONS = 20`, plus the control cells below. Seeds: `random.Random(SEED + stable_int_hash(family, novelty, session_index))`; the process-randomized `hash()` is never used as a seed or key. Given determinism, each cell's success fraction is an exact multiple of `1/K`. The correct action is recomputed by the scorer from the server's frozen ground truth; the scorer never reads an arm label (arm-blind), and the label is joined only after scoring. Arms are interleaved by a frozen seeded order.

## 6. Pre-freeze arithmetic dynamic-range certificate (the mandate's hard object)

Computed at DESIGN from the frozen construction only — no run, no outcome data — and re-computed by EXECUTE from the realized run.

| novelty | T-AMORTIZED | B-COLD-RE-DERIVE | B-RETRIEVAL-SHAPED | B-EMPTIED-CONTEXT |
|---|---|---|---|---|
| 0.00 | 1.000 | 1.000 | 1.000 | 1.000 |
| 0.25 | 1.000 | 1.000 | 1.000 | 1.000 |
| 0.50 | 1.000 | 0.875 | 0.875 | 0.875 |
| 0.75 | 1.000 | 0.875 | 0.875 | 0.875 |

- `CERT-A`: on >= 1 family, both baselines < 0.95 at 0.50 and 0.75. `0.875 < 0.95` → HOLDS.
- `CERT-B`: every arm >= 0.80 at every level. minimum `0.875 >= 0.80` → HOLDS.
- `CERT-C`: treatment margin at novelty >= 0.5 is >= `1/K = 0.125`. `1.000 − 0.875 = 0.125` → HOLDS.

The certificate is SATISFIABLE by construction on both families. Because the substrate is deterministic, EXECUTE must reproduce these exact fractions (0 or 8 of 8 tasks per cell). A realized mismatch is itself the falsification (`F-CEILING` / `F-FLOOR` / `F-LEAK`), never silently accepted. `latency_ms` is excluded from the certificate and all gates.

## 7. Positive and null controls (frozen)

- `PC-EXACT-REPLAY`: oracle given the full session discovery up front (schema + all `resource_id` including the chain binding). Must be `1.000` at EVERY cell. Proves the bank is solvable; `< 1.0` → `F-SUBSTRATE` (MEASUREMENT_INVALID).
- `NC-SHUFFLED-BINDING`: treatment with the chain binding replaced by a seeded binding from a DIFFERENT session. Must equal the baseline `0.875` at novelty >= 0.5. Proves the binding is causally necessary (permutation null).
- `NC-EMPTIED-CONTEXT`: must equal `B-COLD-RE-DERIVE`. Proves context retention is the carrier.
- `NC-NO-DISCOVERY-DIRECT`: skip all discovery; must be `1.000` at 0.00 and `<= 0.875` at >= 0.50. Proves the action is genuinely not determined by the task spec and that novelty is real.
- `NC-NO-LEAK`: mechanical scan of every idempotent response a re-deriving arm consumes (`/session`, `/task/{i}`) for the chain binding (or any value sufficient to reconstruct it); the designated receipt must be returned exactly once (re-read 409/redacted). Failure → `F-LEAK` and the bounded class-negative, never a SUPPORT.
- `NC-FAMILY-ISOLATION`: F1 bindings invalid in F2 and vice versa.
- `NC-EQUAL-BUDGET`: identical task schedule, seeds, endpoint access and request ceiling for all arms; only the oracle receives the binding.
- `NC-NO-SYNTHETIC`: every scored trajectory is real localhost HTTP; a synthetic fallback is terminal MEASUREMENT_INVALID (inherited discipline).
- `NC-ARM-BLIND-SCORING`, `NC-COUNTER-INTEGRITY`: as in §5 and §4.

## 8. Measurement validity (extended list in spec.json `measurement_validity`)

Pre-registration with no design-time outcome measurement (V01); the certificate is a prediction, not a measurement (V02); seeded determinism (V03); credential-free, model counters forced zero (V04); full raw-evidence retention and re-computability (V05); frozen-input re-verification (V06); binding causality required (V07); no-leak required (V08); equal budget/tooling (V09); no synthetic fallback (V10); latency excluded from gates (V11); independent recompute zero mismatches (V12).

## 9. Decision rule, ordered and fail-closed (full table in spec.json `decision_rule`)

Substrate and controls are read FIRST. The certificate and success comparison are read only if the substrate (`PC-EXACT-REPLAY == 1.000`) and all controls are valid.

| branch | frozen condition | consequence |
|---|---|---|
| SUPPORTS | C1–C8 pass: certificate holds arithmetically and the realized deterministic run reproduces T=1.000, baselines=0.875, margin 0.125, controls and recompute pass | Deliver the reusable bank; B2 unblocked for this construction; DIRECTOR decides any `C-MEAS-VALID` status move. |
| FALSIFIES (bounded substrate-class negative) | on EVERY family the realized certificate is unsatisfiable: baseline high-novelty success >= 0.95 (`F-CEILING`/`F-LEAK`, asymmetry not enforced) OR any arm < 0.80 (`F-FLOOR`) | Record the bounded class-negative; deliver NO validated bank; redirect to procedure caching / external-agent benchmarking; do not re-run the excluded mandatory-discovery certificate. |
| MIXED | C1 and C4 pass on >= 1 family but C5–C8 partially fail without a control/substrate fault | Report the partial result; no bank promotion; DIRECTOR decides. |
| INCONCLUSIVE | certificate holds and substrate/controls valid but a cell is not evaluable without invalidating the measurement | Report; no claim move. |
| MEASUREMENT_INVALID | `F-SUBSTRATE` (PC < 1.0), `F-CONTROL` (shuffled/emptied/null-discovery mismatch), or `F-RECOMPUTE` (nonzero mismatches), or infrastructure failure | No conclusion about the construction class; preserve raw evidence; retry only from a valid checkpoint. |

`status` describes measurement validity/completion; a valid scientific negative is `status=COMPLETE` with a negative `outcome`, never an infrastructure failure.

## 10. Contamination / dynamic-range certificate (preregistered)

The certificate is preregistered as the §6 table plus the §7 causal controls. Contamination is controlled by: `NC-NO-DISCOVERY-DIRECT` (task spec alone cannot solve high-novelty tasks), `NC-SHUFFLED-BINDING` (binding causal necessity), `NC-FAMILY-ISOLATION` (no cross-family leakage), `NC-NO-LEAK` (non-re-derivability), and arm-blind scoring. Dynamic range is certified by `CERT-A/B/C` at DESIGN and re-checked by C4/C5 at EXECUTE.

## 11. Self-attack (DESIGN) and why no branch is empty

Seven blocking/major findings were raised and resolved pre-freeze (full list in spec.json `pre_freeze_satisfiability_dry_run.self_attack_findings`): (SA-01) circularity of a definitional certificate — resolved by making it a falsifiable prediction about a realized deterministic run with concrete failure modes; (SA-02) a chain task needed for all K tasks would break the 0.80 floor — resolved by fixing exactly L=1 chain task with explicit `resource_id` elsewhere; (SA-03) a one-time schema would break the floor — resolved by keeping `/session` idempotent and making only the single binding one-time; (SA-04) a shallow one-step arm vs real context retention — resolved by the deeper-carry novelty 0.75 cell; (SA-05) cost vs correctness — resolved by making the certificate about success_rate; (SA-06) latency noise — resolved by excluding `latency_ms` from all gates; (SA-07) single-family artifact — resolved by two disjoint content families. Every branch in §9 is reachable: the ceiling branch via a re-derivable/leaked binding, the floor branch via a mis-sized schedule, and the SUPPORT branch via the designed construction.

## 12. Freeze eligibility and artifacts

All six v2 checks are `PASS`, except `freeze_artifacts_bound`, which is `NOT_APPLICABLE` with reason: no pre-existing mutable local fixture, task bank, dataset or code file is an interpretation dependency. Every interpretation-determining constant (endpoints, K=8, L=1, novelty ladder, chain indices, arm policies, counter definitions, seeds, certificate arithmetic, thresholds 0.95/0.80/0.125 and branch logic) is embedded verbatim in `spec.json` and this file, which the deterministic freezer hashes directly. The bank, server, arms and scorer are authored at EXECUTE strictly as a literal realization of those literals, may not introduce or retune any decision-relevant constant, and their hashes must be recorded in `result.json.artifacts` (role `code`) and `provenance.json`. Remote-like behaviour is not used (the substrate is local and deterministic). Therefore `freeze_artifacts` is empty.

## 13. Required artifacts at EXECUTE

1. The realized bank/server, arms, scorer and runner, each hashed into `result.json.artifacts` (role `code`) and `provenance.json`.
2. Raw trajectories per (family, novelty, arm, session, task) with counters; redacted binding + sha256; the `NC-NO-LEAK` scan record.
3. Derived per-arm/per-novelty success and counters; the recomputed certificate; the control lattice.
4. `result.json`, `report.md`, `provenance.json` with the exact packet-contract top-level shapes, preserving the frozen control/metric identifiers.

## 14. Stop condition

Exactly one audited experiment on this frozen design. No threshold, arm, cell, endpoint or certificate change after outcomes exist. The bounded-negative branch is a first-class terminal outcome, not a reason to re-run or to weaken the certificate.
