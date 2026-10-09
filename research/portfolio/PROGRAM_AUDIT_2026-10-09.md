# SPIDER Research 2.0 — Program Audit

Date: 2026-10-09  
Canonical corpus: 417 experiments  
Quarantined packets: 2  
Purpose: strategic synthesis for Scout and Global Research Director. This document is a dated synthesis, not a replacement for canonical packets.

## Executive conclusion

SPIDER has **not** demonstrated a universal "Web Physics", nor has it yet demonstrated the core product claim that a real external LLM agent pays mainly for residual novelty rather than the whole task.

It **has** demonstrated several bounded ingredients:

1. parameterized mechanism inheritance is possible on synthetic/in-kernel task families;
2. some Web/action datasets contain non-random predictive structure beyond shuffle;
3. bounded measurement instruments can discriminate real HTTP/auth state under controlled conditions;
4. response-derived freshness/staleness signals can work on synthetic/local substrates;
5. direct protocol/API replay can dramatically outperform repeated UI traversal in bounded sandbox workflows;
6. the factory's audits have repeatedly falsified naive shortcuts: exact-route replay, TF-IDF staleness semantics, simple DOM-density metrics, several Web-Physics estimators, and token-length-as-economics.

The missing proof is the **integrated causal chain**:

> observation -> parameterized mechanism -> executable binding in the shipped kernel -> applicability/freshness decision -> real external agent action -> lower end-to-end successful-task cost on partially novel or cross-site work.

No canonical packet currently validates that chain end to end.

## Claim audit

### C-PARAM-INHERIT — EXPERIMENTAL

**What survived**

- Synthetic experiments demonstrated parameter-slot induction and correct binding on unseen identifiers.
- Multi-parameter synthetic variants reached perfect binding/resolution within their frozen harnesses.
- Competition-safe retrieval/selection behavior survived bounded Graph tests.

Representative evidence includes:
- EXP-PRODUCT-33528829801
- EXP-PRODUCT-33741671686
- EXP-GRAPH-33816735314

**What did not survive / current ceiling**

- Later Product work repeatedly found that harness-level parameterization did not cleanly transfer into the product/kernel path.
- The latest Product diagnosis (EXP-PRODUCT-37385633334) identifies a decisive implementation gap: the shipped kernel exposes literal `distill()`, not the parameterized induction path expected by the experimental design, and the literal confidence/resolution thresholds can make distill-to-EXECUTABLE impossible by construction.

**Current interpretation**

The *idea* of parameterized inheritance is experimentally supported. The *shipped mechanism path* is not yet demonstrated.

**Highest-value next gate**

Before any expensive LLM benchmark:
1. prove a positive round trip in the actual kernel: observe -> distill parameterized -> resolve EXECUTABLE -> non-null bound_action -> execute;
2. prove a negative round trip: wrong/out-of-support binding is refused for the right reason;
3. hash/pin the actual kernel and task bank into the frozen transaction.

---

### C-MEAS-VALID — EXPERIMENTAL

**What survived**

Runtime established multiple bounded measurement-validity successes:
- real Flask/JWT discrimination;
- bounded Keycloak/auth-state discrimination;
- a later intervention oracle combining WAL-byte, logical projection and response fingerprints passed an independent audit at a narrow instrument scope (EXP-RUNTIME-36129163700).

**What was falsified**

- Header mechanisms often failed to transfer across endpoints.
- Several apparent signals were body-dominated, endpoint-specific or application-engineered.
- Browser/write-path generalization remained incomplete.
- Multiple later packets failed because the substrate or frozen control scheme was invalid before science could be read.

**Current interpretation**

This is the strongest infrastructural claim in the program: SPIDER can construct trustworthy bounded instruments, but they are not yet a general measurement substrate for all downstream claims.

**Highest-value next gate**

Repair and execute the author-separated + real-browser/write-path validation that was already identified, instead of inventing another estimator.

---

### C-FRESHNESS — HYPOTHESIS

**What survived**

- Two bounded Graph positives showed that response-derived freshness guards can separate planted stale/fresh states on synthetic/local HTTP substrates.
- Ablations showed some multi-channel value in those bounded settings.

**What failed**

- Naive TF-IDF semantic staleness was falsified.
- The latest distributed/shared-WAL Graph attempt (EXP-GRAPH-36302977302) was MEASUREMENT_INVALID: the frozen HTTP routes were not actually bound and the health gate correctly failed.
- Therefore no distributed-realistic freshness operating point was measured.

**Additional Frontier observation**

EXP-FRONTIER-37385647440 observed that some server-minted handles rotate *within* a single episode. That creates a structural blind cell for replay-by-handle and reinforces the need for re-derivation/procedure-level reasoning. It is not itself a freshness-accuracy result.

**Highest-value next gate**

Do not retune thresholds. First supply a route-valid, independently health-certified substrate. Then measure false accepts on auth/session/permission/endpoint/validator drift and compare the guard economically with fresh re-derivation.

---

### C-DELTA-REPAIR — latest event MEASUREMENT_INVALID; inherited bounded ceiling EXPERIMENTAL

**What is established**

EXP-GRAPH-36106653880 was measurement-invalid on the distributed-transfer attempt and explicitly preserved the prior single-node EXP-GRAPH-36018188168 as the inherited EXPERIMENTAL ceiling. The distributed run obtained no D1-D7 outcomes and must not be read as a negative. A bounded local-repair mechanism therefore exists, but distributed/general repair with contamination and cost bounds is not established.

**Main dependency**

A useful delta-repair experiment depends on:
- trustworthy freshness/applicability detection;
- a real executable mechanism path;
- a measurement substrate whose perturbations are independently certified.

**Current interpretation**

This claim is downstream, not dead. Repeatedly testing it before fixing those prerequisites mostly measures the substrate.

---

### C-RESIDUAL-NOVELTY — EXPERIMENTAL

**Why it matters**

This is closest to SPIDER's distinctive thesis:

> pay for novelty, not for the whole task.

**Current state**

EXP-FRONTIER-36287182510 kept the claim at EXPERIMENTAL after a PASS audit. It replicated the residual decomposition over 6000 classified span occurrences (sigma2 about 0.2228, sigma3 0.1000, headroom 0.3228). A zero-cross-episode within-episode scratchpad closed 600/600 observation-absent spans at 1.0 span-level correctness, showing that cross-episode persistence is not required for correctness on that plan family. The value-keyed cross-episode cache closed 0/600 such spans itself and fell back to oracle execution 600/600 times. The successful scratchpad cost 48 abstract units, above the frozen 38.6 cost bar.

What remains unproven is the claim's intended scaling law: no canonical experiment has yet shown a real external-agent successful-task cost curve tracking controlled novelty fraction rather than full task length. The cost units are not tokens/latency/dollars and no model call occurred in the transaction.

**Highest-value next gate**

Construct matched task families with controlled novelty and compare:
- cold agent;
- instructions/memory;
- retrieval;
- compiled/replayed workflow where applicable;
- SPIDER executable mechanism inheritance.

Primary outcome must be **cost per successful task**, including verification and repair.

---

### C-LLM-INHERIT — BLOCKED condition; underlying registry hypothesis remains unmeasured

**Current state**

The latest canonical Product event, EXP-PRODUCT-37385633334, emits BLOCKED to describe the present condition while explicitly preserving the underlying registry hypothesis as unmeasured. It executed zero treatment/comparator arms, zero model calls, zero browser actions and zero retrieval/verification/repair calls. This is not negative evidence against the claim.

Intel/Product repeatedly identified the missing external-agent experiment, but the last Product readiness gate (EXP-PRODUCT-37385633334) correctly aborted before spending the full budget.

**Critical discovery**

The treatment arm itself is currently not proven live in the shipped kernel. A benchmark comparing SPIDER with retrieval is meaningless until SPIDER can actually execute an inherited mechanism at a non-zero rate.

**Highest-value next gate**

Treatment-arm liveness first; real LLM benchmark second.

---

### C-CROSSSITE — HYPOTHESIS

**What we know**

- Existing WebWorldData-style evidence contains predictive signal beyond shuffle.
- MIND2WEB strongly falsified naive exact replay: exact route reuse is rare even when operation-level similarity is substantial.
- No canonical experiment yet demonstrates mechanism transfer on a true website holdout without identity leakage.

**Current interpretation**

Cross-site inheritance remains one of the project's defining unanswered questions.

**Highest-value next gate**

After executable kernel liveness exists, train/induce on site A and evaluate homologous mechanisms on unseen site B with strict site holdout and no site identity leakage.

---

### C-WEB-DYNAMICS — HYPOTHESIS

**What survived**

- Non-random predictive structure exists in bounded datasets and synthetic systems.
- Some narrow mechanism-conditioned effects survive specific tests.

**What repeatedly failed**

Across Physics and Frontier, many candidate formulations were falsified or measurement-invalid:
- simple distributional geometry;
- several density/divergence estimators;
- rank/magnitude effects not identifiable in HTTP signatures;
- designs with empty or unattainable accept regions;
- site/template baselines that absorbed purported mechanism signal.

Latest Physics (EXP-PHYSICS-37385620138) remained MEASUREMENT_INVALID and did not move the claim.

**Current interpretation**

There is no justification for a broad "physics of the Web" claim. Physics should remain PARKED unless a materially different observable, dataset or mechanism becomes available.

---

### C-SEMANTIC-RESOLVE — HYPOTHESIS

**What survived**

A bounded semantic-resolution result existed, but later work showed important aliasing and grounding failures.

HTTP status alone failed to identify equivalent/valid templates in realistic aliasing cases; body-based grounding can help but requires an external correctness oracle and can create false positives.

**Current interpretation**

Semantic resolution remains useful but should be downstream of a live executable mechanism path. Do not restart another isolated resolver micro-benchmark without a product use case.

---

### C-PRODUCT-ECON — HYPOTHESIS

**What is established**

Bounded sandbox results show large UI-vs-direct-protocol speed/cost differences. Competitor systems also clearly avoid repeated reasoning using action caches, compiled workflows, semantic selectors, inference caching and browser/API bypass.

**What is not established**

SPIDER has not measured:
- real end-to-end amortized cost per successful task;
- break-even reuse count under its own system;
- recurrence/reuse distribution on the target task population;
- maintenance/freshness/repair overhead at realistic scale.

Intel's later work sharpened an important point: published persistence/memory systems often provide cost equations or component costs without the empirical recurrence/stationarity quantity needed to calculate an operational break-even.

**Highest-value next gate**

SPIDER must measure its own recurrence/novelty distribution and treatment efficacy rather than borrow an external economics number.

## Program-level discoveries

### 1. Local continuation is a real agent failure mode

The factory itself demonstrated a general agent behavior: previous-output injection creates strong path dependence. Agents can rationally refine a local problem indefinitely while losing global utility.

This motivated the Scout -> Global Director -> scientific lanes architecture.

### 2. Measurement design is a first-class scientific object

A large fraction of failures were not null scientific results but invalid instruments:
- empty accept regions;
- controls that could not fire;
- positive controls tautological by construction;
- frozen rules that made one branch unreachable;
- substrate health failures;
- future-stage packet contamination.

The program learned that pre-freeze *attainability* and *control liveness* need explicit machine checks.

### 3. Reuse unit matters

The evidence increasingly disfavors "replay the previous route" as the general abstraction.

The more promising hierarchy is:
- literal action replay for exact repetition;
- compiled workflow for same workflow/new values;
- semantic selector for layout variation;
- parameterized mechanism for homologous transformations;
- procedure/path persistence when handles themselves rotate;
- fresh re-derivation when state is cheap or unstable.

### 4. The economic object should be work avoided, not representation size

Parameterization does not reliably reduce representation tokens. The plausible economic value is avoided exploration, browser traversal, model inference, verification and repair.

### 5. The Web may contain predictive structure without possessing a useful universal low-dimensional physics

Those statements are compatible. Current evidence supports the first in bounded settings and does not establish the second.

## Current strategic bottlenecks

Priority order as of this audit:

1. **Restore factory liveness.**
   Scout must be advisory, not a single point of failure; Factory recovery must use consecutive failures rather than lifetime failures on one SHA.

2. **Repair the actual kernel treatment path.**
   A real distill -> resolve -> execute parameterized round trip is prerequisite to C-LLM-INHERIT and C-RESIDUAL-NOVELTY.

3. **Finish the Runtime generalization gate.**
   Resolve the blocked author-separated/browser-write measurement transaction or supersede it cleanly with a repaired frozen design.

4. **Run the first real external-agent comparison.**
   Only after (2) and (3).

5. **Keep Physics parked unless a new observable/substrate appears.**
   More estimator refinement on the current evidence base has low marginal value.

6. **Use Frontier for orthogonal economics/structure questions.**
   The hop-depth re-acquisition cost scaling question is materially different and can determine whether paths/procedures are worth persisting.

## Things the program must not claim

- "Universal Web Physics discovered."
- "SPIDER beats cold/retrieval agents on real tasks."
- "Cross-site mechanism transfer demonstrated."
- "Freshness solved."
- "Product economics validated."
- "Token savings are the main source of value."
- "A PASS producer result is evidence when the independent audit says MEASUREMENT_INVALID/REVISE."

## Recommended immediate Director posture after liveness restoration

- Runtime: REOPEN or repair the blocked measurement-generalization transaction.
- Product: PIVOT to kernel treatment-arm liveness; no full LLM benchmark before it passes.
- Graph: support the executable parameterized mechanism + freshness prerequisites, not another local threshold refinement.
- Intel: stop internal metrology; provide current competitor/baseline and external-accounting evidence that directly affects Product's benchmark.
- Frontier: pursue hop-depth/re-acquisition cost scaling or another genuinely orthogonal mechanism/economics question.
- Physics: PARK unless Scout/Director identifies a materially new observable or dataset.
