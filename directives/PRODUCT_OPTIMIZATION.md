# SPIDER — PRODUCT OPTIMIZATION CHARTER

This charter governs the Product team whenever it identifies a process, mechanism or workflow that could become a useful product advantage.

## Objective

The Product team does not merely package accepted research. It must actively turn promising processes into implementations that are measurably better than what a credible current baseline can do today.

Examples include route inheritance, state-grounded retrieval, browser-to-first-party-API escalation, fallback ladders, staleness handling, selector recovery, capability registries, semantic addressing, execution planning, caching and reuse.

## Product-owned optimization loop

For each promising process:

1. **Define the current baseline.** Use the strongest reproducible implementation reasonably available in the repository/environment. Vendor claims are context only until reproduced locally.
2. **Specify the bottleneck.** State what is currently inefficient or unreliable: success, actions, exploration, model calls, tokens/cost, latency, recovery, staleness, fidelity, reuse, or another operational metric.
3. **Generate alternatives before outcomes.** The Product Architect may design multiple implementation variants, but must select/freeze the tested variant and benchmark rule before seeing confirmatory outcomes.
4. **Build the smallest optimized implementation.** The Builder may improve algorithms, data structures, caching, routing, fallback, parallelism, state representation or execution strategy so long as the frozen comparison remains fair.
5. **Benchmark against the strongest local baseline.** Equal task set, success oracle, budgets, retries, environment and accounting. Do not use a strawman baseline.
6. **Audit independently.** The Tester/Auditor decides whether the claimed improvement is real and identifies the causal bottleneck when it is not.
7. **Iterate only from evidence.** A failed version may spawn another version only when the audit or measured failure mode gives a concrete optimization hypothesis. Preserve every prior attempt.
8. **Promote only demonstrated improvements.** Product superiority means a preregistered operational win, not architectural elegance or use of SPIDER components.

## Search space

The Product team MAY optimize implementation details even when the underlying mechanism came from Intel/Graph/Physics, provided it does not rewrite the scientific verdict. Product optimization is engineering/product experimentation, not retroactive scientific validation.

The Product team MAY combine multiple audited building blocks and MAY create new product-specific engineering mechanisms whose purpose is to improve operational performance. Such mechanisms remain product hypotheses until independently benchmarked.

## Current-state requirement

Whenever the phrase "better than current" is used, record:
- the exact baseline implementation/version;
- why it is a credible current comparator;
- whether it is locally reproduced or only externally claimed;
- the frozen metric(s) and win rule;
- the date of the comparison.

Externally reported headline numbers must never be treated as achieved baseline measurements unless independently reproduced under the Product benchmark.

## Optimization outcomes

Every beta/version must end in one of:
- `BEATS_BASELINE` — preregistered win rule met;
- `PARITY` — no material advantage;
- `LOSES_BASELINE` — materially worse;
- `MEASUREMENT_INVALID` — comparison cannot support a conclusion;
- `BLOCKED` — implementation cannot be fairly tested in the current environment.

A loss is not repaired by changing the win rule. It is repaired only by a new, explicitly versioned optimization hypothesis.

## Continuity

Product state must include `continue` and `next_action`.

- `continue=true` only when there is concrete unfinished work: an authorized beta, an evidence-backed optimization variant, a repair, or another product hypothesis ready to test.
- `continue=false` when Product has no actionable experiment until new audited evidence arrives.
- `next_action` should be one of `OPTIMIZE`, `ARCHITECT`, `BUILD`, `AUDIT`, `REPAIR`, `REVIEW`, or `WAIT_FOR_EVIDENCE`.

The Product team must not spin on unchanged evidence merely to remain busy.