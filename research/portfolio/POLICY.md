# SPIDER Research 2.0 — Global Research Direction

Status: binding control-plane policy for NEW experiment selection.

## Purpose

Research 2.0 must not confuse a locally sensible continuation with the globally best next problem.

A lane handoff's `next_question` is a proposal. It preserves scientific continuity, but it does not automatically determine the next experiment.

Before any NEW experiment is allocated, a Global Research Director considers the whole SPIDER program and decides what each lane should investigate next.

Already-frozen experiments are completed under their frozen design. Operational retries do not require a new research-direction decision.

The Director is also responsible for research liveness. A lane that has stopped, failed before freeze, exhausted its local thread, or has no active experiment is not silently left dormant. The Director must explicitly decide whether to REOPEN it on the most promising available problem, PARK it for a stated dependency/reason, or TERMINATE a bounded thread.

## Director mandate

The Director reasons across:

- the ONE cumulative Codex and claim state covering original source evidence and subsequently accepted audited experiments, using `effective_event_by_claim` for current epistemic status and raw latest events only for chronology;
- historical evidence within that same Codex via `codex/legacy_brief.json`, `codex/index.json.historical.artifacts`, and targeted original source/audit reads from `codex/sources/0000-historical-evidence.md` (pinned to the frozen archive Git blob) where relevant;
- the missions and capabilities of all six lanes;
- recent and historical experiment trajectories;
- unresolved central claims and current product bottlenecks;
- dependencies between lanes;
- the last handoff proposed by each lane;
- general knowledge about autonomous agents, planning, exploration/exploitation, local optima, path dependence, long-horizon error accumulation, research strategy and measurement design.

Historical verdict-token co-occurrence is NOT an accepted scientific claim and cannot promote a Research 2.0 status. The two generations form one continuous scientific corpus, while retaining distinct provenance and audit semantics; a previous negative, invalid or blocked design is a clue for whether a new experiment is redundant or requires stronger controls.

General knowledge about agents is a PRIOR, not SPIDER evidence. The Director must distinguish it from observations established by the Codex.

A permanent Research Scout supports the Director with broad reconnaissance. The Scout continuously scans the Codex, lane trajectories, external agent approaches, benchmarks, papers and tooling at shallow depth, then produces a staff brief. It does not decide the agenda and its external findings are not SPIDER evidence.

The Director should consume this brief rather than spend its own cycle on broad reconnaissance. Deep verification, reproduction or implementation is delegated to Intel or the appropriate research lane.

The recurring question is:

> Given everything SPIDER currently knows, what is the most promising next problem for each lane?

"Promising" means likely to materially improve understanding, falsify an important hypothesis, unblock a central dependency, change the architecture/product decision, or explore a genuinely high-upside alternative.

Do not reward PASS. A clean negative result may be more valuable than another positive refinement.

## Historical non-duplication check

For every NEW research allocation, compare its **question, substrate, treatment, comparator, statistic, falsifier and control** with relevant pre-2.0 artefacts before allocating expensive EXECUTE work. Use the small source-pinned `legacy_history` snapshot and selective `codex/legacy_artifact_index.json` lookups; do not load 22 MB into the agent context. Record in each lane's existing `comparative_reasoning`: `LEGACY: DUPLICATE | REPLICATION | DISTINCT_EXTENSION | NO_MATCH | UNCERTAIN`, cited artifact SHA(s) or an explicit reason the historical source could not be inspected, and the justification for proceeding. A real replication with materially improved independent validity is allowed. Repeating an already falsified design with the same flaws is not. Never turn absence of a hit in the compact brief into proof of absence from the full archive.

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

## Research-efficiency mandate — choose decision-changing experiments, not activity

The two factories have **different outputs**. Research produces falsifiable, independently audited evidence in the ONE Codex; the product-delivery loop produces a working integration and measured marginal economic value. Do not force the product to wait for a speculative Physics breakthrough. The existing Product scientific lane still obeys audit and guarded promotion; a separate product prototype may consume its results without claiming that an experimental mechanism is shipped.

For every NEW allocation, the Director must use the existing `rationale` and `comparative_reasoning` fields to answer, in concise prose:

- **Decision counterfactual:** what changes if the treatment wins, loses, or is invalid? If no branch of the outcome changes a decision, PARK or redesign.
- **Strongest fair baseline:** which existing cached/compiled/agent solution would make an apparent improvement meaningless? A baseline at ceiling cannot support a success-rate advantage.
- **Validity and dependency:** can the substrate and independent outcome oracle discriminate now? If repeated MEASUREMENT_INVALID / REVISE findings share a cause, assign a single repair instead of another near-duplicate outcome-bearing experiment.
- **Budget and stopping:** state the smallest decisive batch, a bounded attempt/cost ceiling in the rationale, and the explicit stop/pivot trigger. Do not pretend the present allocation schema mechanically enforces budget limits.
- **Multi-scale graph ablation when relevant:** test flat cache / nearest-neighbour / procedural lookup against fractal graph + macro composition with identical context and metrics; do not assume graph structure saves tokens or that Web physics exists.

Use the current dated global audit as a directional prior (436 subsequent packets, 255 REVISE or MEASUREMENT_INVALID as of 11 October 2026), **never** as live counts or as evidence that 255 packets were wasted. Examine marginal yield by experiment family: repeated invalid measurements are an instrumentation problem, repeated nondiscriminating positives are a design problem, and a clean negative may be the most useful result. Preserve an explicitly limited exploratory allowance for Frontier and Physics when the hypothesis is independent and genuinely falsifiable.

Product-adjacent lanes should prioritize the three known blockers until evidence changes them: an audited executable parameterized carrier, a non-ceiling multi-step task bank, and a capable external-agent runtime. Other scientifically valuable research may proceed independently when its decision value justifies the cost. The research Codex remains cumulative and neither loop may rewrite or cherry-pick negative evidence.

## Lane roles

Graph: cumulative operational inheritance — parameterization, semantic resolution, freshness, delta repair, residual novelty and LLM inheritance.

Physics: falsification-first search for Web-dynamical structure beyond memory/similarity. Deep estimator work is justified only insofar as it unlocks meaningful tests.

Runtime: measurement/execution substrate serving central scientific or product questions. It should follow important blockers rather than acquire a permanent micro-specialty by inertia.

Product: coherent external-agent behavior and end-to-end economics. It should integrate audited capabilities rather than duplicate another lane's fundamental micro-research without reason.

Intel: external datasets, competitors, baselines and prior art that can change a live SPIDER claim or experimental design. It is not a generic internal metrology lane.

Frontier: deliberately search outside the current solution basin for orthogonal high-upside mechanisms or levels of description.

## Durable mandate

Every NEW experiment request stores the Director mandate that authorized it.

For liveness, the Director snapshot identifies whether each lane is running, has an unfinished experiment, is stalled before freeze, or is idle. The Director must not leave an idle/stalled lane accidental: PARK/TERMINATE must be explicit; otherwise CONTINUE/PIVOT/REOPEN causes the factory to dispatch or redispatch work.

The Director also records how the Scout brief affected the decision.

The mandate records:

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

New design-contract v2 work must pass an independent pre-freeze satisfiability/identifiability review. Repeated measurement-invalid packets with the same prerequisite failure are evidence that the prerequisite should be repaired or the thread PARKed; they are not a reason to spend more cycles rediscovering the same absence.

## Failure behavior

The Director is a reasoning stage, not a heuristic fallback.

If it is unavailable or produces an invalid mandate, the factory may resume already-existing experiments but MUST NOT allocate new experiments until a valid global decision exists.

This preserves scientific liveness without silently restoring the old handoff-driven behavior.

## Success criterion

The factory must be able both to go deep and to decide when depth has stopped being the best use of intelligence.

The central governance capability is not "stop after N experiments."

It is:

> choose the next problem from the whole world of currently available problems, rather than from the last problem's immediate children.
