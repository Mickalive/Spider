# TEAM GRAPH — ACTIVE DIRECTIVE

Authority: LAB DIRECTOR. This file is operational and may be rewritten by the
LAB DIRECTOR after each audited cycle. It does not override the scientific and
product constitution in `SPIDER_MASTER_PROMPT.md`.

## Current status

Run 1 is a **proof of concept**, not a general demonstration.

Audited facts:
- exact replay eliminated novel decisions/actions on the three matched known
  routes;
- matched wall-clock speedup was ~1.002×, not 8.5×;
- three chosen composite tasks used 16 reused / 23 total actions (69.6% reuse),
  but task decomposition and success predicates were hand-specified;
- run-1 confidence values are invalid because of a fragment counter/timestamp
  initialization bug, now fixed in `graph/store.py`.

## Next mission

Do not rerun the same demonstration and do not optimize presentation.

1. Add tests/invariants for fragment counters, timestamps and confidence.
2. Separate structural state identity from causally relevant dynamic variables
   (form values, auth/session state, checkboxes, etc.) without losing raw
   observables.
3. Build a blind composition experiment where:
   - the full target trajectory is absent from training;
   - useful fragments, if any, come from independent tasks;
   - the consumer does not receive hand-selected fragment IDs;
   - UNKNOWN remains UNKNOWN rather than being filled from ground truth.
4. Evaluate at minimum: task success, novel actions, reused actions, browser
   interactions, decision points, failures/recoveries and retrieval overhead.
5. Compare against strong baselines: nearest-route/trajectory retrieval,
   concrete graph retrieval, and current browser-memory/skill approaches when
   implementable.
6. Extend sequential inheritance toward >=20 agents/tasks so an actual
   exploration-cost-vs-accumulated-knowledge curve can be estimated.
7. Treat staleness/recency confidence as uncalibrated until prospective
   revalidation outcomes support a mapping.
8. Do not claim cross-model transfer until distinct model policies actually
   consume the same stored knowledge.

## Reporting rule

Every headline claim must point to matched raw rows or a reproducible analysis
script. Never compare unmatched condition averages and label them identical.
