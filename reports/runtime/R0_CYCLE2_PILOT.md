# R0 CYCLE 2 — PILOT REPORT (near-repeat kill experiment)

Lane: RUNTIME. Cycle: R0-2, GitHub run 32908002333. Date: 2026-08-26.
Prereg: `reports/runtime/R0_CYCLE2_PREREG.md`, sha256
`9d07d391d9f177e6d8d5be7c727853c2a8223bec8fc3d5446313c8043b524e3e`
(recorded in `pilot_results.json` at run start; recomputation matches).
Git-orderable freeze (W4): code commit `8ed968d` → frozen instrument
(prereg + probe evidence) `42eb66d` → outcomes commit follows this report.
Evidence root: `results/runtime/pilot2/` (+ addendum), probes under
`results/runtime/probes/`.

## Headline (maximum defensible wording per prereg §10)

> On a single near-repeat task whose goal text never names the route
> anchor, evaluated at two different offset entries with two passes, the
> SPIDER arm finished with strictly fewer browser actions than the
> memory-free baseline on EVERY pass (4 vs 11 actions, both entries),
> with zero novel decisions and full inherited replay — a work-compression
> OBSERVATION at pilot scale. Magnitude is not quoted as a speedup;
> ratios (0.36/0.36) are reported as numbers only; wall-clock stays
> advisory (n=2); multi-task replication and >=3-sample statistics remain
> owed.

This is the program's first gate-passing compression observation, obtained
exactly where R0-1 predicted it must be sought: where ROUTE-FINDING
dominates. It coexists with honest parity elsewhere (C1 below).

## Cells and raw outcomes (stream-counted actions)

| cell | pass | BASE | SPIDER | note |
|---|---|---|---|---|
| C1 exact-repeat | p1 | 4 acts / 3 loads / success | 4 / 3 / success, reused 4, novel 0 | PARITY replicated (R0-1 continuity) |
| C1 | p2 | 4 / 3 / success | 4 / 3 / success | identical |
| C2 stale wrong-host (A0 hint) | p1 | 60 acts / 51 loads / FAIL (budget exhausted, truthfully recorded) | 5 / 4 / success, reused 4, novel 1 (caller repair) | failure-avoidance replicated |
| C2 | p2 | 60 / 51 / FAIL | 5 / 4 / success | identical |
| T3 near-repeat `/tag/love/` | p1 | **11 acts / 7 loads / success** | **4 / 3 / success, reused 4, novel 0** | margin 7 ≥ M=2 |
| T3 near-repeat `/page/10/` | p2 | **11 / 7 / success** | **4 / 3 / success** | margin 7; NOT discordant |
| ABL A1 stripped-hint | p1 | — | UNACTIONABLE, **zero actions**, blinding scan clean | hint CAUSAL (frozen gate) |

BASE's T3 trajectory (event stream): brand-link wander, tag-page drift
(`tag/be-yourself`), return wander — 8 exploratory clicks before the Login
anchor, then form. The goal text ("access your quotes toscrape account…")
contains no anchor substring; retrieval resolved via {quot, toscrape,
form} = 3 pairs, coverage 0.50. Digests matched within every same-entry
pair; the two T3 entries carry different digests by design
(`b66af808…` vs `96d2c4a5…`) — offset robustness, not single-context luck.

## Gates (mechanical, W1) and the labeled repair

All ten gates TRUE with zero derivation errors after the labeled
gate-repair addendum:
`results/runtime/pilot2/POST_HOC_GATE_REPAIR_ADDENDUM.json`.
At run time the driver printed G-C1a/G-C2b/G-T3a=false: `_harness_verdict`
compared ONE predicate_ref string while the two arms legitimately name the
same vendored clause body differently (task id vs capsule witness ref).
Outcomes were untouched; the repair accepts an ACCEPTED REF SET for the
SPIDER row only (BASE still exact-matches). Original run-time analysis
preserved in `pilot_results.json`; recomputation confined to the addendum.
Per-segment APPLICABILITY_PASS trail verified mechanically (P1–P5);
verify rows now carry native verifier compute (max 0.082 ms) and NEVER
wall ms; resolve() overhead max 0.57 ms; applicability re-evaluation max
0.063 ms. Advisory walls: T3 BASE ≈5010 ms vs SPIDER ≈1723 ms; C2 BASE
≈29.5 s (budget exhaustion) vs SPIDER ≈2.37 s — reported as numbers only.

## Hint causality (frozen gate)

A0 succeeded with exactly 1 novel caller action; A1 (pure five-channel
strip; validate_plan green; blinding scan found zero target tokens) ended
UNACTIONABLE with ZERO actions. Gate: causal=true — within THIS caller
implementation; sufficiency-vs-necessity beyond it stays unclaimed.

## Write-back primitive (priority 3)

7 content-hashed observation records (6 VERIFIED_OUTCOME + 1 HANDOFF)
persisted under `results/runtime/observations/` (value=null pinned; ts
copied from source events). One successor candidate derived into a
SEPARATE registry (`results/runtime/capsules-wb/`; audited R0-1 registry
untouched): `runtime/form-login-procedure-wb@v1`, CANDIDATE, mechanism
copied verbatim via manifest join, freshness.last_verified_at + measured
action counts populated, semantic_keys from observed goal-text stems with
credential values excluded by the pinned hygiene rule. Dominance notes:
none fired — demand-vocabulary keys differ from parent step-vocabulary
keys, so the feared null-by-design duplicate did NOT materialize; equally,
NO value claim is made for the successor (no ranking claims; tie-break
disclosure stands).

## Disclosures and negative knowledge

- Registry-level resolution only: every cell executed
  `runtime/form-login-procedure@v1` by lexical capsule_id tie-break
  (byte-identical key sets). "Retrieval identified the right capsule" is
  unsupported and not claimed.
- C1 exact-repeat remains PARITY — inheritance does not beat exploration
  on lexically transparent repeats; consistent with R0-1.
- FROZEN-SCHEMA defect discovered: capsule.v0's additive-default-null
  checker rejects any populated free-object array (negative_knowledge),
  so dominance notes ride manifest+description. Flagged to Director as a
  /v1 schema candidate.
- Baseline competence on T3 is partly DOM-order luck; declared pre-outcome;
  BASE was not retuned post-hoc.
- Loads are read from summary notes and cross-checked (P5); gates depend
  only on stream-counted actions.
- Model independence remains UNFALSIFIABLE (single scripted caller; zero
  provider calls anywhere).

## Refusals honored

No second caller; no MCP/SDK/wire freeze; no TTL/confidence machinery; no
delta-repair executor; no new cost_event fields or enum values (all cycle-2
telemetry rides note discriminators inside the frozen D8 envelope);
derive.py untouched (golden sha test); no inter-capsule ranking claims.

## Status

CYCLE_COMPLETE_PENDING_INDEPENDENT_AUDIT. Handoff to runtime_auditor with
exact evidence paths in `state/runtime_loop.json`. R0 completion state now
hinges on audit of this cycle (near-repeat cell + ablation + replication
all executed; independent audit is the remaining requirement).
