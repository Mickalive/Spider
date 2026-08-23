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

## Open questions carried forward

- G4 blind composition at depth >=3 and without hand-selected fragments;
- G5/G6 semantic identification of known vs novel task portions;
- G7 known-API replacement of browser routes;
- G8/G9 staleness and confidence calibration;
- G10 true cross-model consumption;
- G12 exploration-cost-vs-knowledge curve over >=20 sequential agents/tasks.

Active instructions are controlled by `directives/GRAPH.md` and may be updated
by the LAB DIRECTOR after each audited cycle.
