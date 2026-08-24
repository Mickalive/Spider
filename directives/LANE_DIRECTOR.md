# LANE DIRECTOR — COMMON CONTRACT

A Lane Director runs immediately after the independent audit of ONE completed research lane.
It does not wait for the other lane.

## Inputs

Read:
1. `SPIDER_MASTER_PROMPT.md`;
2. this contract;
3. the active lane directive;
4. the completed team workspace supplied by the workflow;
5. the completed audit workspace supplied by the workflow;
6. the lane ledger and relevant accepted history.

## Graph scope

May integrate/update:
- Graph implementation/results/reports;
- `docs/GRAPH_LEDGER.md`;
- `docs/NEXT_GRAPH.md`;
- `directives/GRAPH.md`;
- `directives/AUDITOR_GRAPH.md`;
- Graph lane state under `state/`;
- shared code only when needed for Graph, with the change explicitly marked as lane-local pending Meta-Director reconciliation.

Must not change Physics accepted state.

## Physics scope

May integrate/update:
- Physics implementation/results/reports;
- `docs/PHYSICS_LEDGER.md`;
- `docs/NEXT_PHYSICS.md`;
- `directives/PHYSICS.md`;
- `directives/AUDITOR_PHYSICS.md`;
- Physics lane state under `state/`;
- shared code only when needed for Physics, with the change explicitly marked as lane-local pending Meta-Director reconciliation.

Must not change Graph accepted state.

## Audit response

For every material audit objection choose one:
- ACCEPTED_AND_FIXED;
- ACCEPTED_CLAIM_DOWNGRADED;
- REPLICATION_REQUIRED;
- REJECTED_WITH_EVIDENCE.

Never silently ignore an objection.

## Continuation decision

Write exactly one machine-readable state file:

Graph: `state/graph_loop.json`
Physics: `state/physics_loop.json`

Schema:

```json
{
  "continue": true,
  "reason": "why another autonomous cycle is justified",
  "next_question": "single highest-information next question"
}
```

Use `continue: false` if the next step would be busywork, measurement-invalid, data-blocked, repetitive, or requires a genuine human/external decision.

## Output reports

Graph: `reports/director/CYCLE_<run_id>_GRAPH.md`
Physics: `reports/director/CYCLE_<run_id>_PHYSICS.md`

The report must state accepted/rejected evidence, audit response, next directive and continuation rationale.