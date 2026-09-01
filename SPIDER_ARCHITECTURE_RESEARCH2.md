# SPIDER — RESEARCH 2.0 / PRODUCT-CONVERGENT FACTORY

Status: active architecture for the post-pre2 factory.

This document changes organization and automation. It does **not** rewrite any frozen pre-2.0 scientific result. `SPIDER_MASTER_PROMPT.md` remains the scientific constitution; where its old organizational mechanics conflict with this file, this file governs Research 2.0 operations.

## 1. Non-negotiable objective

SPIDER must not converge prematurely on a merely functional but mediocre browser-memory product.

The factory has two simultaneous obligations:

- continuously turn surviving evidence into a product that external agents can use;
- continue searching for stronger mechanisms that could materially change the amount and shape of Web exploration itself.

Research is therefore not a pre-product phase and Product is not a post-research phase.

> Product = capabilities that survived gates.
>
> Research = the engine that tries to improve, replace or falsify those capabilities.

A negative result may kill a mechanism. It must not silently kill the broader search domain.

## 2. Product core

The stable external abstraction is:

`observe -> distill -> registry -> resolve -> execute -> verify -> repair/UNKNOWN`

The implementation may change radically behind this surface when evidence warrants it.

The product must prefer `UNKNOWN` over unsafe inheritance.

The unit of reusable knowledge is a **Mechanism**, not an exact human route. A mechanism may encode semantic effect, preconditions, parameter slots, state signatures, postconditions, side-effect contracts, auth scope, freshness, applicability guards, verification and repair boundaries.

## 3. Claim/Capability Registry

Every major product capability is tied to one or more falsifiable claims.

Claim status is one of:

`HYPOTHESIS | EXPERIMENTAL | VALIDATED | PRODUCT_CORE | SHIPPED | REJECTED | BLOCKED | MEASUREMENT_INVALID | SUPERSEDED`

No agent may promote a claim because it sounds plausible.

A claim can enter Product Core only after a frozen gate and independent audit justify that level. A rejected claim remains in the registry and Codex.

## 4. Independent parallel lanes

Research 2.0 has no global research cycle.

Core lanes:

- Graph
- Physics
- Runtime
- Product
- Intel

plus an open Frontier lane whose mandate is to generate and test materially orthogonal, high-upside hypotheses. Frontier is specifically authorized to search beyond what pre-2.0 already knows.

Each lane has its own:

- persistent branch `lab2/<lane>`;
- concurrency group;
- immutable work request;
- experiment id;
- checkpoints;
- state;
- continuation decision.

A lane never waits for another lane merely for synchronization.

Cross-lane evidence is consumed from the Codex or exact immutable commits. Cross-lane dependencies may affect priority but do not become workflow `needs:` barriers unless the scientific design strictly requires it.

## 5. One standard experiment transaction

Every claim-bearing cycle is:

`REQUEST -> DESIGN -> FREEZE -> EXECUTE -> CHECKPOINT -> INDEPENDENT AUDIT -> DIRECTOR VERDICT -> CODEX`

DESIGN is not allowed to inspect outcome data.

FREEZE is performed by deterministic code, not by the research agent. It hashes the request, specification and preregistration before execution begins.

EXECUTE may not mutate frozen inputs.

AUDIT may not help the producer obtain PASS.

DIRECTOR integrates only what survived audit.

Every stage checkpoints to the lane branch. A later-stage crash must never erase an earlier valid stage.

## 6. Standard experiment packet

Every experiment directory is `research/experiments/<experiment_id>/`.

Required canonical files:

- `request.json` — immutable machine work request;
- `spec.json` — scientific/product question, claim ids, baselines, falsifier, controls, validity;
- `prereg.md` — human-readable preregistration;
- `freeze.json` — deterministic hashes proving pre-outcome freeze;
- `result.json` — structured measurements and execution status;
- `report.md` — interpretation bounded by the measurements;
- `provenance.json` — commits, run ids, datasets, code paths and environment;
- `audit.json` — independent audit;
- `verdict.json` — claim and product consequence;
- `handoff.json` — exact unresolved question / next high-information action.

`failure.json` is required when a stage cannot finish.

No scientific result may exist only in Actions logs.

## 7. Codex

Pre-2.0 memory stays frozen and separately addressable.

Research 2.0 maintains `SPIDER_CODEX.md` from standardized experiment packets across all lane branches.

The compiler:

- ingests all finalized outcomes, including negative/blocked/invalid;
- includes the exact preregistration and decision rule, not merely final numbers;
- reports incomplete packet coverage instead of silently omitting it;
- deduplicates by experiment id and content hashes;
- serializes writes to main without blocking research lanes.

The Codex is a scientific memory, not execution exhaust.

## 8. Product promotion

Product experiments are allowed to modify the shipping kernel only inside Product's granted scope.

Rejected Product experiments must leave the Product branch tree with their code changes reverted. Accepted experiments may mark `promotion_ready=true`.

A separate serialized promotion workflow merges Product into `main` only after:

- finalized independent audit;
- promotion verdict;
- repository validation;
- kernel tests;
- conflict-free integration.

Promotion is a main-branch write bottleneck by design; research is not.

## 9. Anti-fragility rules

The factory must survive model failures, GitHub retries and partial runs.

- no `git add -A`;
- no runner writes concurrently to the same branch;
- immutable `request_id` and `request_hash`;
- rerunning the same GitHub run resumes the same experiment id;
- completed stages are skipped on retry;
- network/provider failures rotate models;
- semantic/code failures do not get misclassified as retryable network failures;
- every failed stage writes a durable receipt;
- no old work request may be consumed merely because it is the newest file;
- no global all-or-nothing recovery;
- no workflow depends on push-trigger recursion;
- continuation uses explicit `workflow_dispatch`;
- scheduled pulses repair sleeping transitions;
- chained self-relaunch is bounded; scheduled pulses provide liveness;
- per-lane concurrency prevents duplicate simultaneous work;
- the pulse never dispatches a lane already queued or running.

## 10. Research allocation

The factory should prioritize work roughly by:

`information_gain * claim_centrality * product_leverage * uncertainty_reduction / cost / measurement_risk`

This is guidance, not a magic score.

A proposed experiment is low priority if neither a positive nor a negative result could change a scientific or product decision.

Frontier remains deliberately exploratory. It may investigate attractors, metastability, committors/barriers, directed geometry, characteristic times, entropy/flux, effective dimension, multi-scale dynamics, causal effect factorization, incremental computation, program synthesis, cache invalidation, process mining, verification, uncertainty, or ideas not yet named.

The requirement is not familiarity. The requirement is falsifiability and plausible work-compression leverage.

## 11. Near-term gates, not a permanent roadmap

The current registry seeds high-value gates around:

- valid writable measurement substrates;
- parameterized inheritance to unseen identifiers;
- freshness and invalidation;
- localized delta repair;
- residual-novelty economics;
- true LLM inheritance against strong baselines;
- cross-site transfer;
- stronger Web-Physics mechanisms.

These are starting claims, not a ban on discovering better questions.

## 12. Definition of success

SPIDER succeeds only if future external agents measurably avoid work they would otherwise have to search, reason, browse or rediscover, while remaining correct under drift and uncertainty.

A product that merely replays history faster is insufficient.

The factory is explicitly authorized to change the internal architecture when research discovers a better way to make agent work cumulative.
