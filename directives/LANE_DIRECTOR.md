# LANE DIRECTOR — COMMON CONTRACT

A Lane Director runs only after the independent audit of ONE completed research lane returns the machine-readable integration gate `PASS`.
It does not wait for the other lane.

A `REVISE` audit does NOT go to the Lane Director. It is routed back to the producing coding/research agent with the exact audit report and `required_fixes`, then independently re-audited inside the same scientific cycle.
A `BLOCKED` audit does not go to the Lane Director either; the rejected snapshot remains provenance and the lane stops until the block is legitimately resolved.

## Research programs versus cycles

A **research program** is a bounded scientific question with an explicit decision horizon. A program may require several cycles, repairs, replications or falsification attempts.

A **cycle** is one Team -> Audit -> Director pass inside that program.

Do not confuse the two. Finishing a cycle does not automatically mean the research program is finished. Conversely, when the current program's decision horizon has been reached, do not keep generating cosmetic extra cycles merely to stay busy.

When a research program is finished, the Lane Director must decide whether a genuinely different, high-information next research program is justified. If yes, it must recommend that program explicitly and prepare the lane directive so that it can start automatically. If no honest next program exists, the lane stops.

A new program must NOT be a disguised attempt to rescue a falsified hypothesis by changing representations, thresholds, targets or datasets until something becomes positive. It must ask a materially different question or use a genuinely different measurement instrument, and its rationale must explain why the accepted evidence makes that next question informative.

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

Even after a `PASS`, the report may contain limits, claim downgrades or replication requirements. For every material surviving audit objection choose one:
- ACCEPTED_AND_FIXED;
- ACCEPTED_CLAIM_DOWNGRADED;
- REPLICATION_REQUIRED;
- REJECTED_WITH_EVIDENCE.

Never silently ignore an objection.

## Program state and continuation decision

Write exactly one machine-readable state file:

Graph: `state/graph_loop.json`
Physics: `state/physics_loop.json`

Required schema:

```json
{
  "continue": true,
  "program_status": "ACTIVE",
  "program_id": "short-stable-id",
  "reason": "why another cycle in the current program is justified",
  "next_question": "single highest-information next question inside this program",
  "program_completed_by_run_id": null,
  "next_program": {
    "launch": false,
    "id": null,
    "title": null,
    "question": null,
    "rationale": null,
    "stop_condition": null
  }
}
```

Allowed `program_status` values:
- `ACTIVE`: current program is not finished. Requires `continue=true` and `next_program.launch=false`.
- `COMPLETE`: current program's decision horizon has been reached. Requires `continue=false`. Set `program_completed_by_run_id` to the current GitHub run ID. A new program may be recommended through `next_program.launch=true`.
- `BLOCKED`: the current program cannot honestly proceed because required data/instrumentation/external dependency is unavailable. Requires `continue=false` and no automatic next program unless the proposed next program is genuinely independent of the block.
- `TERMINATE_LANE`: no further research program is epistemically justified. Requires `continue=false` and `next_program.launch=false`.

For `next_program.launch=true`, ALL fields `id`, `title`, `question`, `rationale`, and `stop_condition` are mandatory. The new program must be materially distinct from the just-completed one, and the Director must rewrite the lane directive (`directives/GRAPH.md` or `directives/PHYSICS.md`) so it already contains the initial mission, validity gates, baselines, decision rule and stopping condition for that next program BEFORE advancing the accepted lane branch.

### Same-program continuation

Use `program_status=ACTIVE` and `continue=true` only when another cycle can materially change the answer to the current program's question.

### Program completion with automatic succession

If the current program is complete and a next program is justified:
- set `program_status=COMPLETE`;
- set `continue=false`;
- set `program_completed_by_run_id` to the current GitHub run ID;
- set `next_program.launch=true` and fully specify the recommendation;
- rewrite the active lane directive for the new program before pushing accepted state.

The external Program Supervisor will launch the first cycle of that new program automatically. It will consume the recommendation only for the exact Director run that completed the prior program, preventing duplicate launches.

### Honest stopping

Use `TERMINATE_LANE` when further work would be busywork, p-hacking-by-representation, repetitive, non-discriminating, or lacks a genuinely different instrument/question.

A negative or falsifying result is a valid program completion. Do not invent another nearby program merely because the result was negative.

## Output reports

Graph: `reports/director/CYCLE_<run_id>_GRAPH.md`
Physics: `reports/director/CYCLE_<run_id>_PHYSICS.md`

The report must state:
- accepted/rejected evidence;
- audit response;
- current research program and whether it remains ACTIVE or is COMPLETE/BLOCKED/TERMINATED;
- if COMPLETE, the exact accepted conclusion of the program;
- if a next program is recommended, why it is scientifically distinct and its stopping condition;
- the next directive and continuation rationale.