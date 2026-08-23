# NEXT RUN — READ THIS FIRST

## CURRENT STATE

Run 1 produced useful engineering work but post-run audit changed the scientific
status materially.

### TEAM GRAPH

Status: **PROOF OF CONCEPT**.

- exact replay eliminated novel decisions on matched known routes;
- original 8.5× wall-clock claim was an unmatched-average artifact and is
  withdrawn; matched wall time was ~1.002×;
- selected composite tasks achieved 69.6% action reuse, but decomposition and
  success predicates were hand-specified;
- run-1 confidence values were compromised by a fragment counter/timestamp
  insertion bug, now fixed with invariants.

### TEAM PHYSICS

Status of historical WP-003: **MEASUREMENT_INVALID**.

- Markov baseline leaked the current target through `prev_action_label`;
- reported bootstrap CI was Gaussian jitter, not a real bootstrap;
- Python `hash(site)` made the seed non-reproducible across processes.

Corrected collection/analysis code now requires deterministic trajectory IDs,
true previous-transition actions, anti-leak assertions, trajectory-grouped
uncertainty and action-conditioned next-state prediction.

## NEW LAB ARCHITECTURE

The next cycle uses genuinely separate primary OpenCode contexts/runners:

1. `TEAM GRAPH` — independent runner/branch.
2. `TEAM PHYSICS` — independent runner/branch.
3. `INDEPENDENT AUDITOR` — starts only after both teams finish; reads both.
4. `LAB DIRECTOR` — starts only after the audit; integrates accepted work,
   rejects/quarantines invalid claims, and rewrites the operational directives
   for the next cycle.

The stable scientific/product constitution remains `SPIDER_MASTER_PROMPT.md`.
The Director controls the cycle through:

- `directives/GRAPH.md`
- `directives/PHYSICS.md`
- `directives/AUDITOR.md`
- `directives/LAB_DIRECTOR.md`

The Director may rewrite the first three after each cycle. It must not silently
rewrite the master prompt.

## EXACT NEXT ACTIONS

### Graph
Read `directives/GRAPH.md`. Priorities are blind fragment composition,
stronger baselines, state identity vs dynamic variables, >=20-agent/task cost
curve, and prospective confidence calibration.

### Physics
Read `directives/PHYSICS.md`. First produce a clean corrected transition corpus
and rerun the action-conditioned next-state target. WP-004 committor/barrier is
blocked until an identifiability gate passes.

### Auditor
Read both team branches after completion and execute `directives/AUDITOR.md`.
Attempt to falsify every headline claim from code/raw results rather than
accepting team summaries.

### Lab Director
Read all three branches and execute `directives/LAB_DIRECTOR.md`. Integrate only
accepted work, record disagreements, update directives for the next cycle and
open one final PR toward `main`. Never auto-merge.

## HISTORICAL ARTIFACT POLICY

Do not overwrite run-1 JSON to make old results look corrected. Preserve them
as provenance and add audit status/reporting around them. New corrected runs
must use new filenames.
