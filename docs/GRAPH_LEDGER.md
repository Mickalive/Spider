# GRAPH LEDGER

## G-H1 (Run 1, 2026-08-23) — Cumulative inheritance proof of concept

- **Operational hypothesis**: storing validated state-action fragments with
  provenance/confidence lets later agents pay only novelty cost.
- **Implementation**: SQLite store + fragment replay + entry-state reset,
  live-site corpus across 4 sites, two scripted heuristic policies.

### Audited results

- Exact replay on the three tasks actually matched between cold and replay:
  **0 novel actions** on replay.
- Matched wall time: ~2.822 s cold vs ~2.816 s replay = **~1.002×**, therefore
  the original **8.5× wall-speedup claim is withdrawn**.
- Three selected composite tasks used 16 reused / 23 total actions = **69.6%
  reuse**. This is a composition proof of concept, not a general autonomous
  decomposition result.
- Run-1 confidence values are not valid evidence: audit found a positional
  INSERT bug placing a timestamp in `success_count` and `1` in `created`.
  Code is now corrected with invariants.

### What survives

- fragment replay can eliminate new decisions for known routes;
- fragment composition is operationally possible in the scripted setup;
- entry-state reset is a useful recovery mechanism;
- operational memory does not solve semantic search on huge unstructured pages.

### What remains unproved

- automatic decomposition of unseen natural-language tasks;
- model-to-model transfer;
- cross-site universal skills;
- calibrated confidence/half-life;
- a material wall-clock or monetary cost reduction with a real LLM in loop;
- superiority over strong trajectory-memory / nearest-route / graph baselines.

## G-R2 (Cycle 32670239235, 2026-08-24) — Blind inheritance with content-derived addressing

- **Operational hypothesis**: fragments acquired on independent tasks can be
  found and composed by a consumer that receives only task keywords (no
  hand-selected fragment IDs, no goal_sig lookup), reducing novelty cost on
  held-out composite routes.
- **Implementation**: `graph/addressing.py` (IDF-weighted content channel +
  low-weight producer-provenance channel; gates frozen pre-recording:
  τ=0.25, ≥1 content hit), `graph/consumer.py` (single consumer shell,
  four memory representations), `graph/baselines.py` (nearest-trajectory,
  graph-BFS), route distillation at acquisition (`graph/explorer.py`),
  matched store isolation + seed-randomized method order
  (`graph/run_cycle2.py`).

### Replicated results (primary artifact `results/graph/run2c_*.json`; replication across three recorded variants)

1. **Blind composition POC**: login→checkboxes succeeds at 7 actions
   (5 reused) with fully independent production-acquired fragment provenance;
   login→tag-love→page2 succeeds at 9 actions (7 reused) but its third subgoal
   reused a fragment created earlier **within the same composite run**
   (audit F-G2 → partial self-inheritance; independence holds for the first two
   subgoals). In run2c trajectory (78) and graph-BFS (89) also succeed on the
   checkbox composite — fragment is cheapest by far but not uniquely
   successful. Cold baseline on that composite: 191 total actions, partial
   (run2c value; earlier text citing 275 was a run2b figure — corrected at
   integration per audit F-G1).
2. **Novel-action reduction vs all baselines** (run2c, n=5 composites):
   fragment 98.8 novel/task vs cold 222.0, graph 160.2, trajectory 142.4;
   paired CIs exclude 0 vs cold and graph; vs trajectory CI [−74.0, −13.2]
   with success-rate parity → NEEDS_REPLICATION before a stronger claim.
3. **Addressing layer**: 87.5% route-found, 12.5% honest UNKNOWN, 0.41 ms/
   lookup; top-choice agreement 16/16 across variants with different stores;
   boilerplate tokens blocked by IDF (unit-tested); UNKNOWN never filled
   from ground truth.
4. **Replay validation**: stored production routes replay with zero novel
   actions, 5/5 tasks in each of the three recorded variants.
5. **≥20 sequential execution ledger**: 35 ordered executions over three
   generations with store growth 21→32 fragments.

### Negative / boundary results (accepted as evidence)

- Fantasy composite unsolved by ALL methods under the DOM-order consumer:
  inheritance cannot compensate novelty the consumer cannot reach within
  budget.
- Numeric specificity invisible to content channel ("Example 1" vs
  "Example 2" confusion, score 1.0 wrong-example retrieval).
- Inheritance outcomes are sensitive to glue-recovery mechanism (status-500
  flipped success→partial when history-back was replaced by deterministic
  hub-return).
- Confidence calibration: DATA_INSUFFICIENT (all prospective rounds in one
  score bucket, empirical rate 0.95, n=40). Scores remain uncalibrated gates.
- Two earlier variants (run2, run2b) partially invalidated by substring
  acceptance evaluators; preserved as provenance with defects documented in
  `reports/graph/run2_blind_inheritance.md`.

### What remains unproved

- LLM-in-the-loop cost savings; natural-language decomposition;
  cross-model/cross-policy transfer (consumer policy fixed);
  superiority over trajectory memory on success-rate (parity observed);
  calibrated confidence/staleness; cross-site skill transfer.

## G-R2 AUDIT STATUS (LAB DIRECTOR, cycle 32670239235)

Independent audit (`reports/audit/CYCLE_32670239235.md`) + director
recomputation from raw artifacts:

- ACCEPTED: aggregates (novel/task, success, wall), paired task-grouped
  bootstrap deltas, addressing-quality diagnostics, replay validation ×3
  variants, ≥20-execution ledger, calibration honesty (DATA_INSUFFICIENT),
  baseline matching/store isolation. All recomputed exactly.
- CORRECTED AT INTEGRATION: composite-outcomes narrative table (stale run2b
  cells, F-G1); ledger cold figure 275→191; quotes-composite independence
  caveat added (F-G2); settle_ms instrumentation change disclosed (F-G3).
- SCOPE: blind fragment composition is a PROOF OF CONCEPT whose cleanest,
  fully-independent evidence is the checkbox composite plus the cross-task
  retrievals (dyn_ex2/status_500/fantasy pager) with verified production
  provenance. Fragment-vs-trajectory superiority remains NEEDS_REPLICATION.
- Instrumentation note: snapshot settle_ms 350→120 vs run 1 — wall_s is not
  comparable across cycles; within-cycle comparisons unaffected.

## Open questions carried forward

- G4' blind composition at depth ≥3 and with a *different consumer policy*
  (keyword-ranker) to decouple memory value from policy weakness;
- G5/G6 semantic identification of known vs novel task portions (addressing
  is keyword-level; embedding/LLM routing untested);
- digit-aware tokenization for fragment content (ex1/ex2 class of failures);
- glue-recovery policy as a first-class, separately measured mechanism;
- confidence calibration needs score-spread (currently compressed);
- G10 true cross-model consumption; G12 cost curve with per-generation
  policies held fixed.

Active instructions are controlled by `directives/GRAPH.md` and may be updated
by the LAB DIRECTOR after each audited cycle.
