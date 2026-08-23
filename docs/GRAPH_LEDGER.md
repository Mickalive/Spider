# GRAPH LEDGER

## G-H1 (Run 1, 2026-08-23) — Cumulative inheritance reduces exploration cost
- **Operational hypothesis**: storing validated state-action fragments with
  provenance/confidence lets later agents pay only novelty cost.
- **Implementation**: SQLite store + fragment replay + entry-state reset
  (`graph/`), live-site corpus, 4 sites.
- **Measured**: replay 0.00 novel actions/task (cold: 12.33); 8.5× wall
  speedup; cross-task composition 70% reuse under a different consuming
  policy; success rates maintained (0.9→1.0).
- **Reusable structures found**: subgoal-keyed fragments; generic skill
  classes (form.login, paginate.next); entry-state reset glue; internal/
  external boundary flag; structural fingerprints w/ text tokens.
- **Failures recorded**: naive replay breaks on entry-context mismatch;
  heuristic agents fail on >400-element unstructured pages regardless of
  memory.
- **Staleness**: not yet measured (no site drift observed in-run).
- **Next engineering question**: confidence decay vs induced DOM drift (G8/G9),
  ≥3-fragment composition chains, LLM-in-loop cost validation.

## Open questions carried forward
- G4 composition at depth ≥3 and across sites — PARTIALLY answered (depth 2 ✓)
- G7 known-API replacement of browser routes — untouched
- G8 staleness detection — untouched (design exists: last_validated +
  recency-weighted confidence)
- G10 model transfer — proxy answered via policy transfer; LLM test pending
- G12 exploration-cost-vs-knowledge curve — data collected for n=6 growth
  steps; needs longer sequences
