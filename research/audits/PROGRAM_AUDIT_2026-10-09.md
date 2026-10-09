# SPIDER Research 2.0 — Program Audit

Date: 2026-10-09
Scope: accepted canonical evidence through the main Codex at 417 canonical experiments, plus frozen pre-2.0 evidence where explicitly identified.
Quarantine: 2 historical packets are excluded from canonical evidence and are not used to raise any claim ceiling.

## Executive conclusion

SPIDER has not discovered a universal physics of the Web and has not yet demonstrated the product-defining claim that a real external LLM agent can use inherited SPIDER mechanisms to reduce end-to-end cost on partially novel real-Web tasks.

It has, however, accumulated a coherent set of bounded discoveries that justify continuing the project:

1. Mechanism inheritance is real in controlled settings. A later executor can reuse learned structure rather than repeat full discovery. This is stronger than literal replay: parameter binding, verification and abstention materially change correctness.
2. Correct parameterization is the central mechanism-level bottleneck. On a controlled resource-A/resource-B transfer experiment, single-collection induction pinned a structural field and failed 0/126, while the same pipeline with the collection represented as a variable identity slot succeeded 126/126. The failure and success differ in the learned representation, not in the target identifiers.
3. A real cold-discovery comparator now exists with dynamic range. In EXP-PRODUCT-36293260887, executed cold discovery cost 4.0794 HTTP requests/task versus 1.0159 for the successful diagnostic identity-slot mechanism. The diagnostic amortized ratio was about 0.5447 with break-even at 50 transfer tasks. This is not Product economics and must not be cited as such.
4. Safety abstention is load-bearing. In that same packet, the shuffled-intent null abstained 126/126 with the confidence gate active; bypassing the gate caused wrong verbs on 84/126 tasks and only 0.3333 task success despite superficially valid HTTP responses.
5. Cross-episode persistence is not required for correctness on at least one controlled plan family. EXP-FRONTIER-36287182510 showed a zero-cross-episode within-episode scratchpad closing 600/600 observation-absent spans and reaching 1.0 span correctness. Its cost exceeded the frozen bar, so persistence survives only as a possible amortization mechanism, not as a correctness requirement.
6. Naive persistent replay can be structurally unsound. The cross-episode cache in the same Frontier experiment keyed on an episode-scoped handle value and achieved 0/600 class-(iii) closures from its own mechanism; all apparent correctness came from oracle fallback.
7. Semantic selection contains signal, but applicability/abstention remains unsolved. Graph experiments observed an embedding selector at 45/52 applicable goals versus 36/52 for lexical overlap, including 19/20 versus 15/20 on paraphrases, but the calibrated gate was inert and confidently executed on 11/20 no-applicable/OOD goals. The relevant packets were measurement-invalid and do not advance C-SEMANTIC-RESOLVE.
8. Freshness has bounded synthetic evidence, not real-Web validation. Two bounded positive packets survive, but the later distributed substrate transaction failed its health gate before the science could run. Frontier additionally observed some server-minted handles rotating within a single episode, demonstrating a structural danger for handle replay.
9. There is predictive Web structure, but not yet a useful universal dynamics law. Pre-2.0 WP-002B showed a rule predictor around 0.624 versus shuffle around 0.571 (+0.053, confidence interval positive). Later Physics work repeatedly found measurement/identifiability failures and mechanism-free explanations competitive with or better than mechanism-conditioned ones. C-WEB-DYNAMICS remains HYPOTHESIS.
10. The product-defining real-agent experiment is still unmeasured. C-LLM-INHERIT has accumulated many events but zero admissible real external-agent arm comparisons at matched model/tools/budget.

The correct current framing is therefore:

> SPIDER has credible bounded evidence that learned, parameterized and verified mechanisms can compress repeated Web work, and strong evidence that literal replay and naive persistent state are insufficient. It has not yet shown that this becomes a cross-site, real-agent, economically superior system.

## Claim-by-claim audit

### C-PARAM-INHERIT — EXPERIMENTAL

Strongest surviving result: EXP-PRODUCT-36293260887 plus later variability-learning diagnostics.

Established:
- parameter induction can reach EXECUTABLE and succeed on held-out identifiers in controlled substrates;
- single-collection training can incorrectly pin a structural field;
- declaring/learning that field as variable changes the same transfer problem from 0/126 to 126/126 in the diagnostic arm;
- a later variability-learning experiment inferred a closed collection vocabulary from multi-collection observations, transferred in-support, abstained out-of-support, and separated itself from lexical/regex/frequency nulls at mechanism level.

Not established:
- durable shipped parameterized induction in current main;
- transfer on real Web APIs/browser tasks;
- transfer to a genuinely different site;
- superiority over strong successful retrieval/replay baselines at matched end-to-end success.

Current main is still deliberately minimal: SpiderKernel.distill() emits literal mechanisms at confidence 0.5; resolve() defaults to 0.8; no distill_parameterized() exists. Thus the current shipped kernel cannot express the strongest experimental capability.

### C-RESIDUAL-NOVELTY — EXPERIMENTAL

Strongest surviving result: EXP-FRONTIER-36287182510.

On one controlled plan family:
- residual decomposition replicated at roughly sigma2=0.2228, sigma3=0.1000, headroom=0.3228;
- a within-episode scratchpad with zero cross-episode persistence closed 600/600 observation-absent spans and reached 1.0 span correctness;
- a value-keyed cross-episode cache served 0/600 such spans itself because the key contained an episode-scoped value;
- the scratchpad was too expensive under the frozen abstract ledger, so correctness closure did not establish economic closure.

Not established:
- later-agent cost scaling with residual novelty rather than full task length on real agents/tasks;
- persistent-state amortization in real token/browser/dollar units;
- generalization across sites or task families.

### C-MEAS-VALID — EXPERIMENTAL

Runtime produced the strongest bounded positive: a WAL/logical-projection/response-fingerprint intervention oracle was validated on a planted controlled surface.

Established:
- the measurement instrument can discriminate planted interventions in a bounded single-author/single-transport setting;
- Chromium/DOM/AX capability has been demonstrated in at least one Runtime transaction;
- fail-closed controls and independent auditing repeatedly catch producer overstatement.

Remaining:
- generalization across author/measurer separation and browser transport simultaneously;
- stable writable/auth/session real-task substrate;
- closure of recurring preregistration defects.

Program-level discovery: measurement validity is not bookkeeping. A large fraction of Research 2.0's apparent scientific negatives were actually failures of substrate reachability, impossible gates, baseline construction or frozen-rule semantics.

### C-FRESHNESS — HYPOTHESIS

Surviving evidence:
- two bounded synthetic/single-resource positives with strong TN/FA figures;
- later real-ish distributed attempt correctly failed closed when all HTTP health probes hit a 404 route-binding defect;
- Frontier observed handles that rotated inside an episode, showing freshness cannot be reduced to long-horizon TTL alone.

Missing:
- valid distributed/real-site false-accept measurement;
- calibrated product freshness guard;
- evidence that a response-derived guard dominates re-derivation economically on real tasks.

### C-DELTA-REPAIR — latest distributed event MEASUREMENT_INVALID; bounded prior evidence remains

A single-node controlled result exists, but the distributed-transfer experiment never reached a valid substrate and executed zero scientific trajectories.

Do not convert the distributed failure into a negative about local repair. Distributed generalization remains untested.

### C-SEMANTIC-RESOLVE — HYPOTHESIS

Bounded observations indicate semantic selection signal:
- uncalibrated embedding argmax 45/52 applicable goals versus lexical overlap 36/52 in one fixture;
- paraphrase subset 19/20 versus 15/20.

But:
- the fitted applicability gate was inert;
- slot filling, not the calibrated gate, caused abstention;
- 11/20 no-applicable/OOD goals were confidently executed;
- several packets were invalidated by an impossible code-freeze validity condition and other instrument defects;
- joint authorship of intents/goals remains a contamination threat.

The next valid test must independently author goals/intents and treat applicability, execution, deferral, coverage and false accepts as separate measurable objects.

### C-WEB-DYNAMICS — HYPOTHESIS

Positive bounded evidence:
- pre-2.0 predictor performance above shuffled null on WebWorldData;
- real HTTP probing confirms some response signatures change with query parameters and HTTP revalidation behavior exists.

Negative/limiting evidence:
- exact routes are highly unstable in Mind2Web-like data, so trajectory replay is the wrong abstraction;
- several proposed dynamics metrics were measurement-invalid or estimator-sensitive;
- in the latest real-public-HTML effect-factorization packet, a mechanism-free constant recovered most of the treatment gain and beat the treatment on the real pool;
- rank-ordered semantic effect magnitude was not identifiable from the chosen HTTP signature.

No universal or product-useful Web physics law has been demonstrated.

### C-CROSSSITE — HYPOTHESIS

No true website-holdout demonstration of a learned SPIDER mechanism transferring to an unseen site at matched baselines.

This remains one of the project-defining missing proofs.

### C-LLM-INHERIT — BLOCKED / UNMEASURED

This is the most important missing product proof.

Repeated attempts did not execute the required cold/instructions/retrieval/SPIDER real-agent arms. The latest readiness packet correctly aborted before spending the full experiment.

Current internal blockers:
- main kernel has no executable parameterized distillation path;
- no committed suitable >=30-task real/credential-free bank with mechanical verifiers for the frozen design;
- no implemented accounting counters for model/browser/retrieval/verification/repair in the current kernel;
- prior designs incorrectly equated absent OpenAI/Anthropic keys with absence of every usable model substrate;
- earlier runners lacked common playwright/httpx imports.

A measured real-agent comparison requires a stable model invocation, but not a particular vendor key. A pinned, preflighted OpenCode model is scientifically acceptable if the same model is held fixed across arms, every invocation is receipted, and provider/model fallback is disabled inside the measured comparison.

### C-PRODUCT-ECON — HYPOTHESIS

Not measured on real agents.

Request-count economics on self-authored substrates are useful engineering evidence but are not total cost per successful task. There is no accepted token, latency, verification, repair, maintenance and model-call accounting result on real tasks.

## Strong pre-2.0 bounded evidence that still matters

The retained pre-2.0 program contains a particularly important clean-room capture/replay demonstration: direct cached HTTP replay matched scripted browser-flow acceptance on 48/48 interleaved valid pairs across four host-tasks and three hosts with zero browser actions. Warm-amortized UI/direct-HTTP median ratios were approximately 9.40x, 5.67x, 18.20x and 37.46x, with Holm-adjusted one-sided sign p=0.000977 in all four tasks and stable leave-one-host-out comparisons.

Ceiling: proof of concept on sandbox/scripted host policies. It is evidence that bypassing repeated browser traversal can create large savings when a reusable mechanism is already known. It is not evidence for real LLM-agent transfer, product economics, or universal Web structure.

Mind2Web falsification remains equally important: high operation-level similarity coexists with very low exact-route and strict causal-chain reuse. This argues for transformation/mechanism inheritance rather than route replay.

## Major discoveries about the research process itself

Research 2.0 uncovered recurring failure classes that can manufacture false confidence:
- frozen decision regions that are empty or algebraically unable to fire;
- positive/null controls that are tautological or cannot fail;
- baselines that are cheaper only because they silently fail the task;
- metrics whose denominator changes between arms;
- apparent mechanism correctness produced entirely by oracle fallback;
- substrate hashes proving byte identity but not that the substrate implements the preregistered surface;
- outcome-bearing code created only after freeze while preregistration simultaneously demands that code be frozen;
- repeated attempts at the same blocked real-agent benchmark without first constructing the missing capability.

These are not reasons to distrust the whole program. They are reasons the audit/Codex machinery is valuable: many superficially positive producer results were prevented from becoming canonical claims.

## Operational audit as of 2026-10-09

The scientific factory stopped generating new experiments after 2026-10-05/06 even though cron jobs continued.

Root causes:
1. Scout became a single point of failure. Free OpenCode providers returned repeated server errors; the surviving model frequently spent the whole allowance synthesizing a brief and timed out.
2. Factory Recovery counted every historical Factory failure on the same main SHA, so a long-lived main commit accumulated 17 failures and permanently tripped a threshold of 3 despite intervening successful runs.
3. The snapshot still inspected the obsolete portfolio_allocation request field rather than director_mandate, misreporting active experiment governance.
4. Factory's strategic job stopped before dispatch when Scout/Director failed, preventing already-frozen scientific transactions from resuming even though policy explicitly allows those retries without a fresh direction decision.
5. Several experiments required outcome-bearing code to be bound at freeze although the old transaction gave DESIGN no code scope and only allowed code changes after freeze. The requirement was impossible by construction.
6. Common Product/Runtime client dependencies (httpx, playwright) were not standardized.
7. Product readiness logic treated absence of specific vendor API keys as absence of any model substrate, despite the factory already possessing an OpenCode invocation path.
8. The shipping kernel on main does not yet implement the strongest experimental parameterization capability and cannot execute its own literal distill() output at default thresholds.

## Repairs in the accompanying change set

- Scout becomes advisory. A deterministic degraded Scout brief is used when model reconnaissance fails and contains no invented external information.
- Strategic cycles use the machine snapshot as their complete directional map and open only targeted canonical packets.
- Scout has a shorter runtime and all configured fallback models are reachable.
- Frozen transactions can resume even when the Global Director is temporarily unavailable; new/pre-freeze work remains fail-closed without a valid mandate.
- Factory Recovery uses the current consecutive failure streak rather than lifetime failures on a main SHA.
- Snapshot governance detection is corrected to director_mandate.
- A real DESIGN -> BUILD -> FREEZE transaction is introduced. BUILD may construct preregistered code/fixtures before outcomes; FREEZE binds exact artifact bytes.
- Product promotion/rejection uses the pre-BUILD baseline for new packets, so audited BUILD code is either promoted completely or reverted completely.
- httpx and playwright Python clients are provisioned as common research dependencies when available.
- Model substrate policy becomes provider-neutral: a pinned healthy OpenCode model may be used for measured agent arms if model identity is fixed and fallback is disabled inside the experiment.

## Immediate research priority after restart

The Global Research Director should reassess rather than blindly resume every local handoff.

1. Runtime / measurement readiness: finish a reusable, frozen, independently-authored browser/HTTP measurement substrate.
2. Product / executable inheritance capability: build and audit a parameterized distillation/resolution path that can actually reach EXECUTABLE, with accounting counters and treatment-liveness controls. Do not call this product evidence until it survives audit/promotion.
3. Product + Graph / real agent inheritance: only after (1) and (2), run the matched same-model/tools/budget cold vs instructions vs retrieval vs SPIDER experiment.
4. Cross-site / residual novelty: make novelty and website holdout explicit variables after real-agent inheritance has a live treatment arm.
5. Physics: PARK broad dynamics work unless a materially new observable/dataset becomes available; do not spend another sequence refining estimators around the same weakly identifiable HTTP signature.
6. Intel: focus on external baselines/prior art that alter the above decisions, especially measured amortization, persistent-agent economics and strong memory/workflow baselines, not internal DOM metrology.

## Bottom line

The project has enough evidence to reject several naive architectures and enough bounded positive mechanism evidence to justify a serious real-agent test.

It has not crossed the threshold that matters commercially or scientifically:

> A real later agent, on partially novel tasks/sites, demonstrably performs the same successful work with materially less total exploration/reasoning/browser cost because it inherited SPIDER mechanisms.

Everything before that is enabling evidence. The next phase should be organized to reach or falsify that statement as directly as the substrate permits.
