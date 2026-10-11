# SPIDER — Two operating loops, one cumulative Codex (11 October 2026)

This is a decision proposal and prototype branch, **not** an audited scientific result, an automatic promotion, or a declaration that the proposed product is validated. Do not edit the historical Codex to fit this strategy.

## Preserve the founding intuition

- **The first agent explores; the next ones inherit.** SPIDER is an independent, model-agnostic operational memory, not a new browser engine.
- **Pay for novelty, not the full task.** Measure saved model tokens, model calls, Web work and total dollars **per verified successful task** including all memory and repair overhead.
- **Graph**: intention -> state -> evidence -> action -> result -> failure/recovery; retrieve mechanisms with their provenance, scope, confidence and freshness.
- **Fractal/multiscale**: site -> section -> page -> component -> action; decomposable task macros. This is a representation/retrieval/compression hypothesis; it is **not** evidence for universal laws of Web dynamics. Compare it explicitly against flat caches and nearest-neighbour retrieval.
- **Selective refresh**: preserve stable how-to; reobserve volatile what-is, sessions and tokens. Subtree repair rather than total replay is a hypothesis to test, not a shipped promise.
- **Inter-agent inheritance**: a safe mechanism may be consumed by an unrelated agent, subject to authorization, user/session scope and replay guardrails. No cross-tenant sharing of secret-bearing traces or token reuse.

The 2 August and 23 August founding discussions already separated pragmatic graph inheritance from speculative physics. The current proposal restores this separation at the **operating-loop** level.

## Factory A — independent scientific exploration (existing Research 2.0)

Keep the six scientific lanes, independent audit, frozen preregistration and ONE cumulative Codex (1,401 historical artifacts and 436 later packets as of last audited snapshot). Its goal is to maximize **decision-changing evidence per experiment dollar**, not packets, PASS verdicts, or speculative features.

Before choosing costly new work, ask:
1. Which concrete uncertainty is this experiment reducing, and what decision would *each* possible result change?
2. What is the strongest competing null/benchmark? Is the experiment identifiable and non-ceiling?
3. Has the same question already failed in either historical or current evidence? If so, what material validity improvement justifies replication?
4. Which prerequisite is missing, and could one reusable substrate repair unblock multiple lanes?
5. What is the stop/pivot condition and maximum compute, time, and failed-attempt budget?

The Director can PARK an unproductive thread, especially repeatedly invalid work, without rejecting its subject forever. Preserve deliberate orthogonal Frontier exploration with a constrained budget and independent falsifiability. Record retrospective invalid/revise rate **by design family** and improvement after review-v2, not just aggregate counts. Repeatedly invalid experimental families should be fixed once or parked, not repeated across lanes.

## Factory B — product delivery and measured value (independent cadence)

**Do not wait for Physics.** Use an existing competent agent (Browser Use/Stagehand/Playwright-based tool) as executor. SPIDER is an optional interception layer before the agent:
1. resolve an already vetted mechanism;
2. check scope, freshness, preconditions, permission and replay safety;
3. execute through an externally authorized callback;
4. verify the postcondition;
5. if unavailable, let the existing agent run; if an attempted execution is ambiguous, return UNKNOWN instead of blind re-execution.

The prototype in `src/spider/agent_bridge.py` is explicitly limited: no autonomous browser, no training, no parameter induction, no automatic side-effect retries, and no claim of savings. `distill_parameterized()` is still missing from the shipped kernel and must enter only through the independent Product promotion gate. Never manually merge an unreviewed research result.

### Build gates and product decisions

- **P0**: working external agent on a nontrivial real multi-step task; same model/tool budget for all arms, realistic oracle, positive/negative test.
- **P1**: an audited parameterized extraction/reuse mechanism in the shipped kernel, with scope control, verify/UNKNOWN, and observable fallback.
- **P2**: benchmark `COLD | INSTRUCTIONS | RETRIEVAL | SPIDER`, plus **Stagehand caching or comparable strongest available compiled-workflow baseline**; deterministic Playwright/HTTP cost floor where feasible.
- **P3**: repeated tasks, changed pages, fresh identifiers and at least two task families; randomized/matched trials, no leakage across arms, preregistered sample size, truly independent success/safety oracle.
- **P4**: commercial validation only if Spider delivers reproducibly >=20% less **fully loaded cost per verified safe success** versus the strongest relevant non-Spider baseline, with non-inferior success/safety and a second-family effect. This threshold is a decision proposal, **not an observed result**.

Account separately for exploration/write, graph storage and lookup, read, model tokens, browser/network work, verification, repair, fallback, retries, and maintaining or invalidating knowledge; show amortization over repeated tasks. A cheaper failed agent is not a success.

The scorer `scripts/score_product_benchmark.py` only checks paired input and publishes descriptive numbers; it executes no tasks, invents no results and awards no scientific verdict. The fourth Stagehand comparison requires extension of the scorer before a flagship claim: four arms are the historic internal gate, not the whole competitive market.

**Delivery rhythm**: one narrowly functioning end-to-end integration and one discriminating task bank before expanding architecture. Publish an actual external-agent example, not merely a synthetic harness. Stop product expansion if the advantage cannot be reproduced. Scientific exploration may continue independently.

## Separation / integration

Factory A owns hypotheses, independent audits, negative evidence and the living Codex. Factory B owns user-facing integration, benchmark execution, deployment and cost-per-success. Factory B may consume audited scientific discoveries but is not required to implement speculative ones. Conversely, product failures generate *questions* for A, not silently accepted Codex evidence. Separate delivery cadences and work budgets, shared provenance and semantic claim ledger.

Current baseline: last global audit found 255 REVISE/MEASUREMENT_INVALID out of 436 packets and no proven real-agent economic advantage. Those figures motivate smarter allocation, **not** a statement that all invalid experiments were wasted or that the product is already viable.
