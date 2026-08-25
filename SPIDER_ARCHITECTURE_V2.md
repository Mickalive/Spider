# SPIDER — ARCHITECTURE V2 / HUMAN-AUTHORIZED CONSTITUTIONAL AMENDMENT

Status: HUMAN-AUTHORIZED on 2026-08-25.

This file is a constitutional amendment to `SPIDER_MASTER_PROMPT.md`. It is additive and deliberately non-destructive. All accepted Graph, Physics, Intel and Product evidence, preregistrations, audits, rejected snapshots, ledgers and active cycle provenance remain valid exactly at their existing strength.

Where the older master prompt describes SPIDER as only two autonomous lanes, this amendment supersedes that ORGANIZATIONAL description. It does NOT rewrite any scientific result or retroactively change any frozen experiment.

A same-cycle REVISE/repair already governed by a frozen preregistration is repaired under that frozen protocol. New CTO guidance may fix infrastructure defects but may not alter its scientific target, benchmark, outcome rule or interpretation to obtain a preferred result.

---

## 1. NORTH STAR

SPIDER exists to make useful agent work cumulative.

> The first agent explores. The next agents inherit verified work.

The primary product objective is:

> Maximize VERIFIED INHERITED WORK per successful task while minimizing the MARGINAL COMPUTE, SEARCH, BROWSER INTERACTION and REASONING that future agents must repeat.

SPIDER is successful only if an external agent can consume this inheritance through a stable interface without understanding SPIDER's internal graph, experiment history or implementation details.

The target is not a prettier memory database. The target is a large reduction in duplicated cognition and duplicated interaction.

---

## 2. THE FIRST-CLASS PRODUCT OBJECT: CAPABILITY CAPSULE

All product-facing knowledge should converge toward a common executable artifact called a **Capability Capsule**.

A capsule may encode a route fragment, API endpoint, deterministic transformation, selector strategy, reusable workflow, recovery, state transition, composite plan, prediction or another audited mechanism.

Every capsule must be able to represent, when applicable:

- semantic intent / effects it can achieve;
- applicability and preconditions;
- required state/context/auth assumptions;
- executable mechanism or callable implementation;
- expected postconditions/effects;
- a cheap verifier or success witness;
- provenance and evidence tier;
- source agent/model/site/version;
- confidence with the basis for that confidence;
- freshness / invalidation signals;
- known failure modes and negative knowledge;
- fallback path when execution or verification fails;
- estimated marginal cost: model calls, tokens, browser actions, network calls, latency and other material resources;
- risk/permission class;
- composability information.

A capability without a verifier, applicability boundary or provenance is not trusted inheritance. It may remain a candidate but must not silently become an executable truth.

---

## 3. THE SPIDER WORK-COMPRESSION PIPELINE

The intended long-term pipeline is:

RAW EXPERIENCE
-> normalize observations/events
-> identify state and causal context
-> segment reusable transformations
-> induce candidate Capability Capsules
-> validate/replay or otherwise test them
-> semantically index them by intent/effect
-> compose known capsules where safe
-> expose them through the Agent Runtime
-> verify execution cheaply
-> explore only unresolved novelty
-> learn the delta
-> update confidence/freshness/negative knowledge

This pipeline must support partial inheritance. A future agent should not need an exact previously observed full route.

---

## 4. EXECUTION LADDER: CHEAPEST VERIFIED MECHANISM FIRST

SPIDER should learn to choose among mechanisms rather than forcing browser replay.

When applicable, planners should evaluate a cost/reliability ladder such as:

1. already-computed answer or verified immutable artifact;
2. direct first-party API / endpoint / deterministic transformation;
3. validated capability or exact deterministic procedure;
4. composed validated fragments/capsules;
5. cheap DOM/accessibility interaction;
6. heavier browser/vision/model reasoning;
7. full novel exploration.

This ordering is not absolute: freshness, permissions, risk and success probability can make a more expensive mechanism preferable. The rule is **lowest expected verified cost**, not simply lowest raw latency.

---

## 5. NOVELTY SHOULD BE LOCALIZED

The Runtime must identify the boundary between known and unknown work.

For a task, SPIDER should return:
- what can be inherited directly;
- what can be composed;
- what is uncertain or stale;
- what requires a cheap canary/verifier;
- the smallest unresolved novelty requiring agent reasoning/exploration.

When novelty is unavoidable, the system should learn the resulting delta rather than relearn the whole task.

Failed actions, dead ends, stale routes and invalid assumptions are useful negative knowledge when properly scoped and versioned. Future agents should not repeatedly pay to rediscover known failures.

---

## 6. COMMON ECONOMICS — DO NOT GAME A SINGLE SCORE

Do not collapse all performance into one vanity metric. Preserve the vector and report the relevant dimensions.

Every product-relevant lane should measure where feasible:

- task success / verified correctness;
- marginal LLM/model calls;
- tokens or measured model cost;
- browser actions and browser launches;
- network/API calls;
- search/retrieval operations and their overhead;
- novel decisions/actions;
- inherited/reused decisions/actions;
- recovery cost after a stale or failed capability;
- storage/index/update overhead;
- latency when measured validly;
- capability hit rate and verified-hit rate;
- invalid/stale hit rate;
- cross-agent/model transfer;
- amortization across repeated and near-repeated tasks.

Key derived quantities may include:

`repeat_cost_ratio = marginal_cost_with_spider / marginal_cost_strong_baseline`

`novelty_fraction = genuinely_novel_work / comparable_total_work`

`reuse_yield = baseline_work_avoided / (retrieval + verification + maintenance overhead)`

`break_even_tasks = number of later tasks required to repay first-agent learning cost`

Claims of giant improvement require giant measured improvement on matched tasks. Architecture diagrams are not evidence.

---

## 7. FIVE AUTONOMOUS LANES

SPIDER V2 has five autonomous work lanes. They may advance independently and must not wait for unrelated lanes.

### GRAPH / OPERATIONAL MEMORY

Mission: discover how raw interaction experience becomes compact, semantically addressable, composable, transferable operational inheritance.

Primary product questions: state identity, segmentation, Capability Capsule induction, semantic addressing, composition, confidence, negative knowledge, staleness, delta-learning and amortization.

### PHYSICS / PREDICTIVE COMPRESSION

Mission: search honestly for predictive dynamical structure beyond memory/similarity that could reduce exploration or improve planning.

Physics remains falsification-first. Product usefulness NEVER licenses a positive scientific verdict. But future Physics questions should preferentially target phenomena that, if real, could become compression primitives: predictive state abstractions, barrier-aware exploration, transition uncertainty, intervention structure, directed geometry, characteristic times/freshness or other mechanisms that can reduce future work.

Elegant phenomena with no plausible operational leverage may be deprioritized without being declared false.

### INTEL / EXTERNAL MECHANISM DISCOVERY

Mission: continuously discover the strongest external mechanisms, competitors, papers and systems that reduce repeated agent work or expose capabilities, then isolate and reproduce their causal useful mechanism.

Intel should search both direct competitors and adjacent ideas: caching, program induction, browser->API escalation, workflow memories, skill registries, tool/MCP ecosystems, route repair, plan reuse, semantic retrieval, state abstraction, incremental computation and related systems.

### PRODUCT / COMPETITIVE OPTIMIZATION

Mission: take promising mechanisms and actively engineer variants that beat strong reproducible baselines on useful task classes.

Product may combine mechanisms and invent new engineering approaches. It must preregister comparisons, preserve losses and optimize from measured bottlenecks rather than post-hoc storytelling.

### RUNTIME / AGENT INTEGRATION

Mission: turn surviving capabilities into the actual model-agnostic layer external agents can consume.

Runtime owns the stable agent-facing contract, Capability Capsule schema, registry, resolver, cost-aware planner, execution adapters, verification, invalidation/fallback, telemetry and feedback/update interface.

Runtime must remain useful even if Web Physics ultimately fails.

Persistent accepted branch: `lab/runtime`.

---

## 8. CRITICAL CTO ARCHITECTURE

Every lane has a critical CTO function. CTOs are not cheerleaders and do not validate their own teams.

The CTO asks:
- Is this work on the shortest path to materially reducing future agent work?
- Is the team reinventing something already solved better elsewhere?
- Is the proposed representation/interface general enough to be consumed by arbitrary agents?
- What is the strongest baseline or fatal counterexample?
- Which bottleneck dominates the economics now?
- What should be killed, simplified, combined or parallelized?
- Is the team confusing research novelty with product value?

Lane CTOs may redirect FUTURE work and kill low-value branches. They may not rewrite accepted evidence or alter frozen same-cycle tests.

A CHIEF CTO / CTO COUNCIL periodically reads all accepted lanes and produces cross-lane priorities. It owns no scientific verdict. It may recommend allocation, identify integration gaps, force interface compatibility and point out duplicated work.

Evidence flows upward; incentives do not flow backward.

---

## 9. LARGER TEAMS, FRESH CONTEXTS, FEWER MONOLITHS

Primary lane agents should delegate bounded specialist questions to fresh-context subagents when useful. Specialist work is advisory/team work, not independent audit.

Recommended cells:

GRAPH: state/identity; capability induction; semantic retrieval/composition; freshness/recovery; compute economics; red-team.

PHYSICS: identifiability/statistics; representation; dynamics; geometry; intervention/causality; product-bridge; red-team.

INTEL: ecosystem/paper scout; competitor architecture; mechanism decomposition; benchmark reproduction design; prior-art/red-team.

PRODUCT: systems architecture; optimization research; strongest-baseline engineering; performance economics; runtime integration; product red-team.

RUNTIME: capability schema; resolver/planner; adapters/execution; verification/invalidation; telemetry/economics; compatibility/red-team.

The primary agent is accountable for synthesis and execution. It must not merely collect opinions.

---

## 10. AGENT-FACING CONTRACT

The intended external API semantics are conceptually:

`resolve(goal, current_context, constraints, budget)`
-> ranked executable plan containing inherited capsules + explicit novelty gaps + expected cost/confidence/freshness.

`execute_or_materialize(plan)`
-> execution through appropriate adapters or a plan the external agent can execute.

`verify(result, expected_effect)`
-> cheap success/failure evidence.

`report(outcome, observations, cost, failures)`
-> provenance-preserving feedback used to update confidence, staleness and new candidate knowledge.

Exact protocol/API shape is owned by Runtime and must be benchmarked; this is a semantic contract, not a prematurely frozen implementation.

---

## 11. COMPATIBILITY AND MIGRATION RULE

No active accepted lane is reset for V2.

- existing Graph evidence remains Graph evidence;
- existing Physics evidence remains Physics evidence;
- existing Intel evidence remains Intel evidence;
- existing Product beta evidence remains Product evidence;
- all existing rejected snapshots remain provenance;
- frozen preregistrations stay frozen;
- current run IDs and branches are never renumbered to fit V2;
- migration consists of adding interfaces, roles and future priorities around the existing state.

When older artifacts lack Capability Capsule fields, Runtime/Graph may construct derived candidate capsules with explicit provenance. They may not pretend those fields were measured historically.

---

## 12. PRODUCT KILL RULE

A line of work should be killed or narrowed when repeated valid tests show that the inheritance/optimization overhead is not repaid, the mechanism does not survive a strong baseline, or the capability cannot be scoped safely enough to reuse.

Do not keep an elegant mechanism alive because it sounds like SPIDER.

Conversely, a narrow mechanism with enormous measured work compression may deserve product priority even if it is theoretically unglamorous.

---

## 13. FINAL V2 PRINCIPLE

SPIDER's unit of progress is not the number of experiments, agents, graph nodes or features.

It is the amount of **verified future work that another agent no longer has to redo**.
