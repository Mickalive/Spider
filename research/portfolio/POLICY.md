# SPIDER Research 2.0 — Global Research Direction

Status: binding control-plane policy for NEW experiment selection.

## Purpose

Research 2.0 must not confuse a locally sensible continuation with the globally best next problem.

A lane handoff's `next_question` is a proposal. It preserves scientific continuity, but it does not automatically determine the next experiment.

Before any NEW experiment is allocated, a Global Research Director considers the whole SPIDER program and decides what each lane should investigate next.

Already-frozen experiments are completed under their frozen design. Operational retries do not require a new research-direction decision.

## Director mandate

The Director reasons across:

- the complete accepted Codex and claim state;
- the missions and capabilities of all six lanes;
- recent and historical experiment trajectories;
- unresolved central claims and current product bottlenecks;
- dependencies between lanes;
- the last handoff proposed by each lane;
- general knowledge about autonomous agents, planning, exploration/exploitation, local optima, path dependence, long-horizon error accumulation, research strategy and measurement design.

General knowledge about agents is a PRIOR, not SPIDER evidence. The Director must distinguish it from observations established by the Codex.

The recurring question is:

> Given everything SPIDER currently knows, what is the most promising next problem for each lane?

"Promising" means likely to materially improve understanding, falsify an important hypothesis, unblock a central dependency, change the architecture/product decision, or explore a genuinely high-upside alternative.

Do not reward PASS. A clean negative result may be more valuable than another positive refinement.

## Decisions

For every lane the Director emits exactly one action:

- `CONTINUE`: the current research thread is still the most promising next direction.
- `PIVOT`: a different claim or materially different problem is more promising.
- `PARK`: preserve the current thread but start no new experiment now.
- `REOPEN`: return to a previously abandoned/parked direction because the global state changed.
- `TERMINATE`: stop a bounded research thread because further work is not currently justified.

These decisions concern research direction, not truth status. PARK or TERMINATE does not falsify a claim.

## Local-attractor warning

The machine may flag a lane when its recent experiments are heavily concentrated on one claim. This is diagnostic context only.

A flag MUST NOT mechanically force a pivot and MUST NOT impose a quota.

It tells the Director to perform a cognitive reset:

1. temporarily ignore the inherited `next_question`;
2. ask what this lane would investigate if it encountered the current Codex for the first time today;
3. compare that answer with the inherited continuation;
4. choose whichever is genuinely more promising and explain why.

The Director may continue a deep thread when that is the right decision.

## Lane roles

Graph: cumulative operational inheritance — parameterization, semantic resolution, freshness, delta repair, residual novelty and LLM inheritance.

Physics: falsification-first search for Web-dynamical structure beyond memory/similarity. Deep estimator work is justified only insofar as it unlocks meaningful tests.

Runtime: measurement/execution substrate serving central scientific or product questions. It should follow important blockers rather than acquire a permanent micro-specialty by inertia.

Product: coherent external-agent behavior and end-to-end economics. It should integrate audited capabilities rather than duplicate another lane's fundamental micro-research without reason.

Intel: external datasets, competitors, baselines and prior art that can change a live SPIDER claim or experimental design. It is not a generic internal metrology lane.

Frontier: deliberately search outside the current solution basin for orthogonal high-upside mechanisms or levels of description.

## Durable mandate

Every NEW experiment request stores the Director mandate that authorized it:

- cycle id;
- lane;
- action;
- target claim;
- exact strategic question;
- rationale;
- comparative reasoning against plausible alternatives;
- treatment of the parent handoff;
- dependencies;
- whether a cognitive reset was performed;
- general agent priors used, separately identified from SPIDER evidence.

DESIGN may convert the strategic question into a rigorous falsifiable experiment, but it must not silently replace the Director's target with a nearby local continuation.

If the mandate is infeasible, fail loudly. Do not invent a substitute research direction.

## Failure behavior

The Director is a reasoning stage, not a heuristic fallback.

If it is unavailable or produces an invalid mandate, the factory may resume already-existing experiments but MUST NOT allocate new experiments until a valid global decision exists.

This preserves scientific liveness without silently restoring the old handoff-driven behavior.

## Success criterion

The factory must be able both to go deep and to decide when depth has stopped being the best use of intelligence.

The central governance capability is not "stop after N experiments."

It is:

> choose the next problem from the whole world of currently available problems, rather than from the last problem's immediate children.
