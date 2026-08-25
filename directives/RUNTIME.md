# SPIDER — RUNTIME DIRECTIVE

## Current mission

Build the smallest honest SPIDER Runtime that proves or falsifies the core agent-facing loop:

> Given a goal + current context, can SPIDER retrieve or compose verified inherited work, expose only the unresolved novelty to the external agent, execute/materialize the known portion, verify cheaply, and fall back safely when inheritance is stale or wrong?

Do not optimize a large platform before this loop is measurable.

## Program R0 — Capability Runtime Skeleton

### Required primitives

1. **Capability Capsule schema** compatible with `directives/CAPABILITY_CAPSULE.md`.
2. **Registry** with versioned capsule storage and provenance.
3. **Resolver** accepting semantic goal/context rather than internal IDs.
4. **Applicability check** that can return UNKNOWN instead of forcing a hit.
5. **Plan representation** with inherited segments + explicit novelty gaps.
6. **Execution/materialization adapter** for at least two mechanism kinds when accepted evidence permits it.
7. **Verifier** separated from the primary success claim where possible.
8. **Fallback** to ordinary agent/browser execution when confidence/applicability/verification fails.
9. **Report/update path** storing observed outcome, cost and scoped negative knowledge.
10. **Accounting** for total Runtime overhead.

### Bootstrap without rewriting history

Runtime may derive candidate capsules from accepted Graph/Intel/Product evidence. Any field that historical evidence did not measure stays null/unknown. Candidate construction does not upgrade the original evidence tier.

### Initial benchmark family

Prefer tasks for which accepted SPIDER evidence already supplies reusable fragments/mechanisms and a reproducible ordinary baseline exists.

Benchmark at minimum:
- exact repeat;
- near-repeat with one localized novelty;
- stale/inapplicable capsule case;
- composition case when supported by accepted evidence.

Compare on matched tasks:
- success;
- model calls/tokens when measurable;
- browser actions/launches;
- novel decisions/actions;
- retrieval/applicability/verification overhead;
- recovery cost;
- repeat cost ratio;
- novelty fraction;
- reuse yield.

### Non-negotiable safety/validity gates

- no hidden use of the answer/task route in semantic addressing;
- no internal fragment ID required from the external caller;
- no silent execution after failed applicability check;
- stale/failed capsule must have observable fallback behavior;
- Runtime overhead included in comparison;
- no promotion of candidate capsules beyond their evidence;
- no claim of broad model independence from one caller implementation.

### Priority architecture hypotheses

Runtime should actively test, not merely implement:

- effect-addressing versus trajectory similarity;
- cost-aware mechanism selection (API/procedure/browser/full exploration);
- cheap canary verification before expensive replay;
- delta-repair after localized environment change;
- scoped negative knowledge to avoid known dead ends;
- confidence decay/invalidation by measured volatility rather than arbitrary TTL;
- capability dominance/Pareto pruning;
- output plans that expose novelty gaps so an external model reasons only where necessary.

## Stop / succession

R0 completes when the end-to-end contract is independently audited on real matched tasks in at least repeat + near-repeat + stale/fallback conditions, regardless of whether the measured advantage is positive.

If the Runtime overhead erases the inheritance gain, complete R0 as a valid negative and open a successor only when the bottleneck is measured and a materially different architecture can address it.
