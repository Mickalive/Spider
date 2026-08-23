# NEXT RUN — READ THIS FIRST

## CURRENT STATE

First full autonomous run completed. Both programs executed real
experiments on live websites with committed code and evidence.
Program outcome: **GRAPH SUCCESS (first demonstration) + PHYSICS
FALSIFICATION (informative negative)** — an explicitly acceptable state
per master prompt §45.

## WHAT WAS ACTUALLY COMPLETED

### TEAM GRAPH
1. Working cumulative operational store: `graph/store.py` (SQLite; states
   w/ raw gz snapshots + text-token structural fingerprints, actions,
   transitions w/ outcomes+error classes, subgoal-keyed fragments +
   generic skill classes, Laplace×recency confidence).
2. Two independent explorer policies (`graph/explorer.py`: keyword-ranker
   G, DOM-walker B) + inheritance machinery incl. **entry-state reset
   retry** (the run's key invention: replay failure from wrong context →
   reset to fragment entry region → re-replay; novelty localized to glue).
3. Live-site corpus `graph/tasks.py` (12 tasks / 4 sites incl. login
   flows, pagination, async dynamic content, composition tasks).
4. Run-1 experiment executed end-to-end (`results/graph/run1_*.json`,
   report `reports/graph/run1_inheritance.md`):
   - exact replay: **0 novel actions, 8.5× wall speedup**, success 1.0;
   - cross-task composites under a DIFFERENT consuming policy: ~70%
     action reuse, success maintained;
   - honest negatives recorded (>400-element unstructured pages defeat
     heuristic agents regardless of memory).
5. Ecosystem survey at implementation level
   (`reports/graph_ecosystem_map.md`): Stagehand ActCache/AgentCache,
   AWM, Healenium, Skyvern inspected via sources/docs. Gap identified:
   nobody else has subgoal-keyed fragments + empirical confidence +
   cross-policy consumption.

### TEAM PHYSICS
1. WP-003 preregistered and frozen BEFORE data collection
   (`reports/physics/wp003_preregistration.md`).
2. Random-walk transition corpus collected on 7 live hosts (557 usable
   transitions, all ≥45/site): manifest
   `data/manifests/wp003_dataset_manifest.json`; collector
   `physics/collector.py` + driver `physics/run_collection.py`
   (per-site subprocess isolation, hard caps, dialog dismissal,
   dead-state hops).
3. WP-003 executed per frozen rule: **FALSIFIED**
   (`reports/physics/wp003_report.md`, `results/physics/wp003_results.json`):
   mechanics-only features add ZERO cross-site predictive power vs a global
   first-order Markov null (0/7 folds; mean Δ=−0.348, CI [−0.363,−0.333]).
   Secondary WP-003b: next-page structural class also fails site holdout
   (0/7). Universal shallow regularity found instead: last-action-class →
   next-action-class transfers near-perfectly everywhere.
4. Measurement honesty log in the report: one invalidated dataset caught by
   invariant check (kind-mismatch bug) and recollected; HN degradation
   diagnosed (auth-wall dead ends) and fixed.

### INFRA
- `.opencode/agents/` role definitions (both teams + coordinator).
- Shared instrumented browser driver `shared/browser.py` (raw observable
  capture: elements w/ CSS paths + ext flags, forms, page_text).

## IMPORTANT RESULTS
- GRAPH: inheritance is real on live sites; entry-state anchoring is THE
  failure mode of naive fragment reuse; glue-reset converts failures into
  small novelty payments. Knowledge is policy-transferable.
- PHYSICS: website-holdout universality is falsified for transition-level
  mechanical prediction at this granularity; trivial Markov structure is
  universal but shallow. Any future "physics" claim must beat memory AND
  trivial sequence statistics AND be policy-sensitivity-controlled.

## CURRENT BLOCKERS
- No LLM API available in-run: agents are scripted heuristics; absolute
  cost numbers and semantic-addressing quality remain unvalidated against
  real model-driven agents.
- No long-lived deployment: staleness/half-life (G8) still has no
  longitudinal data (needs repeated runs over days).
- openlibrary/the-internet walks hit hard caps (420s) — collector budget,
  not a scientific blocker.

## EXACT NEXT ACTIONS (priority order)
1. GRAPH G8/G9: DOM-drift experiment — perturb cached selectors/pages
   programmatically, measure how confidence decay + revalidation restores
   performance; calibrate halflife parameter empirically.
2. GRAPH G12: extend run to ≥20 sequential agents on growing store; plot
   exploration-cost-vs-knowledge curve properly (per-agent costs already
   logged in runs table).
3. GRAPH G10-real: rerun identical protocol with an actual LLM agent
   (needs model access) consuming the same store format.
4. PHYSICS WP-004: committor/barrier test on authenticated regimes using
   existing quotes/internet walk infra (Monte-Carlo restarts, q(x)
   estimation, degree-preserving null). Data collection code reusable as-is.
5. PHYSICS policy-control: rerun WP-003 with goal-directed sampler to test
   whether N2 dominance was a sampler artifact (preregister first).
6. Commit /tmp raw snapshot digests→rehydration script if deeper physics
   re-analysis of raw DOM ever needed (currently raw only in /tmp, lost
   after run — acceptable per §40, noted here).
