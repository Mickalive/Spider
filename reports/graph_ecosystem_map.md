# SPIDER — Graph Ecosystem Map

Date: 2026-08-23. Run-1 survey, subsequently audit-qualified.

Sources inspected during the run included Stagehand/Browserbase engineering
material and source, AWM paper/repository, Healenium material, and Skyvern
material. Items not inspected from primary sources remain explicitly
unverified.

## 1. What the inspected systems appear to cover

### Selector/action caching

**Stagehand / Browserbase**: caches resolved interaction mechanics and can reuse
known actions without repeating the same model inference. This establishes that
selector/action caching itself is not a SPIDER novelty.

**Healenium**: stores locator/DOM information and attempts self-healing after
locator drift. This is relevant to SPIDER's staleness/revalidation problem.

### Procedural memory / workflows

**AWM**: induces reusable abstract workflows from successful trajectories and
reports transfer benefits. This is directly relevant prior art for reusable
procedural abstraction and means SPIDER must beat strong workflow-memory
baselines rather than compare only with raw replay.

**Skyvern / RPA-style workflows**: preserve workflow definitions and execution
traces; useful comparison for replay, state re-reading and recovery behavior.

### Session continuity / semantic memory

Browser storage/session persistence and semantic retrieval over prior
experience are established neighboring mechanisms. They must be treated as
baselines/components rather than rediscovered under new names.

## 2. Audit-qualified gap statement

The original report said, in effect, that nobody else had the exact SPIDER
combination. That was too strong for the survey actually performed.

The defensible statement is:

> **Among the systems inspected in Run 1, the team did not identify the exact
> combination of subgoal-addressable executable fragments, empirical
> validation statistics, freshness/provenance metadata, and consumption by an
> external model-agnostic layer.**

This is a research hypothesis about differentiation, **not** a novelty claim.
A broader paper/repository/product search is required before using language such
as "nobody else" or claiming technical novelty.

## 3. What still appears worth testing

1. Whether fragments below the whole-task level can be retrieved for genuinely
   unseen tasks without hand-selecting them.
2. Whether empirical success/failure and freshness signals improve reuse over
   simple TTL or retry-on-failure strategies.
3. Whether operational knowledge can be consumed across different foundation
   models, not merely across two scripted policies.
4. Whether recovery procedures should be first-class reusable objects.
5. Whether discovered stable APIs can become alternative execution edges to UI
   routes.
6. Whether the external cumulative layer provides value beyond AWM-like
   workflow memory, nearest-route retrieval and existing browser caches.

## 4. Run-1 SPIDER evidence, after audit

- Exact known-route replay eliminated novel decisions on the matched tasks.
- The originally reported **8.5× wall-clock speedup is withdrawn**. Matched
  cold/replay wall time was ~1.002× because this scripted experiment had no
  costly LLM decision loop.
- Three selected composite tasks used 16 reused actions out of 23 total
  actions (**69.6% reuse**). This is a proof that the implemented fragment
  mechanism can compose in the prepared setup; it does not yet demonstrate
  automatic decomposition of arbitrary unseen tasks.
- `agentG` knowledge was consumed by `agentB`, which is a useful policy-format
  proxy but **not yet cross-model transfer**.
- The initial confidence implementation had a counter/timestamp initialization
  bug and therefore provides no calibrated run-1 confidence evidence.

## 5. Positioning rule going forward

Treat the ecosystem map as a living falsifiable document. For every claimed
SPIDER differentiator, record the strongest known competing mechanism and test
against it. Do not infer novelty from failure to find a competitor in a small
survey.
