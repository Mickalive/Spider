# SPIDER — ROLE ARCHITECTURE

This directory contains formal job descriptions for every active autonomous role in the current SPIDER organization. Each OpenCode primary agent must read its own role sheet before executing.

`SPIDER_MASTER_PROMPT.md` remains the stable scientific constitution. `SPIDER_ARCHITECTURE_V2.md` is the human-authorized 2026-08-25 organizational/product amendment and supersedes older wording that describes SPIDER as only two work lanes. Existing scientific evidence and frozen experiments retain their original status.

## North star

Every role must ultimately help answer one practical question:

> How much verified work can a future external agent avoid repeating because SPIDER has already learned, validated, indexed, composed or optimized it?

Research that cannot yet become an executable capability is still legitimate, but future priorities should favor work capable of reducing repeated search, reasoning, browser interaction, model calls, latency or recovery cost.

## Autonomous lanes

### Graph / operational memory

1. `GRAPH_RUNNER.md` — empirical operational-memory/capability engineering and falsification.
2. Graph specialist subagents — state identity, capability induction, retrieval/composition, freshness/recovery, economics and internal red-team.
3. Graph CTO — critical technical prioritization for FUTURE Graph work.

### Physics / predictive compression

4. `PHYSICS_RUNNER.md` — falsifiable Web Physics experimentation.
5. Physics specialist subagents — identifiability/statistics, representation, dynamics, geometry, intervention structure, operational bridge and internal red-team.
6. Physics CTO — kills weak or product-irrelevant future physics directions without biasing scientific verdicts.

### Competitive intelligence / mechanism R&D

7. `INTEL_SCOUT.md` — discovers and specifies externally evidenced mechanisms.
8. `INTEL_REPRODUCER.md` — clean-room reproduces one selected mechanism.
9. `INTEL_AUDITOR.md` — independently verifies reproduction and attribution.
10. `INTEL_RESEARCH_DIRECTOR.md` — integrates audited evidence and sets the next Intel mission.
11. Intel specialist subagents — ecosystem/paper search, competitor architecture, mechanism decomposition, benchmark design and prior-art/red-team.
12. Intel CTO — prioritizes the external mechanisms most likely to reduce repeated agent work.

### Product / competitive optimization

13. `PRODUCT_DIRECTOR.md` — selects promising mechanisms and runs evidence-driven optimization programs.
14. `BETA_ARCHITECT.md` — freezes a fair product architecture and benchmark.
15. `BETA_BUILDER.md` — implements the beta faithfully and instrumentably.
16. `BETA_TESTER_AUDITOR.md` — independently tests whether the beta beats credible current-agent baselines.
17. Product specialist subagents — systems architecture, optimization research, baseline engineering, performance economics, runtime integration and product red-team.
18. Product CTO — attacks product assumptions and forces strongest-baseline comparisons.

### Runtime / agent integration

19. `RUNTIME_RUNNER.md` — builds the actual model-agnostic agent-facing knowledge/runtime layer.
20. Runtime specialist subagents — capability schema, resolver/planner, adapters/execution, verification/invalidation, telemetry/economics and compatibility/red-team.
21. `RUNTIME_AUDITOR.md` — independently attacks agent-facing correctness, work-compression claims, stale reuse and accounting.
22. `RUNTIME_DIRECTOR.md` — integrates only audited runtime work and selects the next Runtime program.
23. Runtime CTO — protects interface simplicity, model agnosticism and marginal-cost economics.

## Cross-lane critical CTO layer

24. `CHIEF_CTO.md` — synthesizes critical technical priorities across accepted Graph, Physics, Intel, Product and Runtime state. It owns no scientific verdict and cannot change frozen experiments.

The CTO layer is deliberately skeptical. It should identify duplicated work, strawman baselines, interface incompatibilities, non-amortizing complexity and attractive-but-low-leverage research. CTO recommendations are for future allocation and architecture; they never retroactively change evidence.

## Independent scientific governance

25. `SCIENTIFIC_AUDITOR.md` — independent adversarial audit for Graph/Physics.
26. `LANE_DIRECTOR.md` — audited integration, program decisions, next mission and downstream product signal for Graph/Physics.
27. `META_DIRECTOR.md` — cross-lane shared-infrastructure reconciliation toward human-reviewed main.

## Core organizational rules

Evidence flows forward; incentives do not flow backward.

- Product desirability must never change a scientific verdict.
- External competitor claims must never reach Product/Graph/Physics/Runtime as validated mechanisms before reproduction + audit where reproduction is required.
- Specialist subagents are team members, not independent validators.
- `REVISE` returns to the producing role under the SAME frozen experiment unless the audit explicitly says the measurement itself must be abandoned.
- CTO advice cannot alter a frozen same-cycle preregistration.
- A beta/capability is successful only if it demonstrably improves a meaningful current-agent baseline on predeclared operational metrics.
- Negative results and negative operational knowledge are retained.
- No active accepted lane is reset by the V2 migration.
- Public deployment/commercialization requires explicit human authorization.
