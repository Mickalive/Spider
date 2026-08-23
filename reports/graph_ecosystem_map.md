# SPIDER — Graph Ecosystem Map (Team Graph, §11 deliverable)

Date: 2026-08-23. Sources inspected: Stagehand/Browserbase engineering blog +
`ActCache.ts`/`AgentCache.ts` source & DeepWiki, AWM paper (arXiv:2409.07429,
ICML'25) + repo, Healenium repos/docs (proxy architecture, scoring config),
Skyvern docs/blog/PRs. Items marked [unverified] rely on general knowledge
without primary-source inspection this run.

## 1. What exists, technically

### 1.1 Selector/action caching with self-healing locators
**Stagehand (Browserbase)** — the most explicit production design:
- *Stored*: resolved Playwright/XPath selectors + metadata per atomic
  `act()` instruction; cache key = SHA256(normalized URL + trimmed
  instruction + variable keys); entries versioned (`version: 1`);
  server-side entries TTL 48h, project-scoped.
- *Reuse*: on matching key, passive page-fingerprint comparison must clear
  a safety threshold before executing cached selector with **zero LLM
  calls**; reported up to ~80% speedup run1→run2.
- *Healing*: if cached selector fails during replay, fresh LLM inference
  re-resolves the action and the cache entry is rewritten ("self-heal");
  a 2025 fix (PR #1472) specifically addressed healed selectors not being
  persisted — evidence that healing-persistence is a live engineering issue.
- *Granularity*: single action or whole agent step sequence
  (AgentCache: goto/scroll/wait/fillForm/keys steps).
- *Known failure modes* (their own words): pages that don't repeat cleanly,
  randomized URLs defeating normalization, semantic change without obvious
  DOM change — "the harder class of problems for any passive equivalence check".

**Healenium** (test automation): stores *etalon* selectors + DOM subtrees in
PostgreSQL; on locator failure parses current page into tree, scores
candidates vs etalon (key attributes + tree diff), score-cap ≈0.5–0.6,
persists successful healings for cross-session reuse via central service.
Granularity: element locator only. No task/goal semantics.

### 1.2 Procedural memory / induced workflows
**AWM** (Wang et al., ICML 2025): LLM-induced reusable sub-routines from
successful trajectories (offline from annotated data, online from judged
successes); workflows = abstracted text/code snippets injected into prompt
memory. Results: WebArena +12.0 abs / +51.1% rel success; Mind2Web +24.6%
rel step SR; cross-website/domain gaps widen advantage (+8.9–14.0 abs).
Snowball composition: induced workflows serve as subgoals for further
induced workflows. *Not persisted as executable artifacts; no confidence/
freshness metadata; retrieval = all-in-context.*

**Synapse** [unverified details]: trajectory-as-exemplars retrieval — full
successful trajectories selected by similarity as few-shot exemplars.
AWM's own ablation argues abstract sub-routines transfer better than whole
trajectories (element accuracy +5.0–9.0 over Synapse-style baselines).

**ExpeL / AutoGuide** [unverified]: insight/rule extraction from experience
pools; natural-language guidelines rather than executable skills.

### 1.3 Workflow mining / RPA-style replay
**Skyvern**: visual-first agent; workflow builder chains parametrized blocks
(login/nav/download/validation/loops); every run produces full trace used as
diagnostic instrument ("3 consecutive auth failures on same portal = portal
changed, not noise"); credentials vaulted, never sent to LLM. Explicitly
anti-selector: reads live state each run — i.e., deliberately does NOT cache
interaction mechanics; caches *workflow definitions* only.
**Selenium IDE / classic RPA**: literal command replay; zero adaptation;
brittleness is the motivating cautionary tale across all newer systems.

### 1.4 Session continuity
Playwright `storageState`, Skyvern `browser_profile_id` (authenticated state
carried forward between runs), user-data dirs. Session persistence is
orthogonal operational knowledge that all systems treat as infrastructure,
not as addressable knowledge.

### 1.5 Semantic retrieval over operational memory
MemGPT/Letta, Zep/**Graphiti** temporal knowledge graphs [unverified]:
episodic+semantic stores with time-aware edges; used for conversation
memory more than web-action memory. Embedding retrieval over past tasks is
standard practice but no inspected system couples embeddings to
*executable interaction fragments with empirical confidence*.

### 1.6 Browser→API distillation
No mature public system found that automatically distills discovered network
endpoints into preferred API routes replacing UI replay [unverified —
closest: Stagehand network-level security hooks, Skyvern structured output;
opportunity gap].

## 2. Cross-cutting synthesis

| Question | Field consensus |
|---|---|
| What is cached | selectors (Stagehand), etalon locators (Healenium), workflow text (AWM), workflow definitions (Skyvern) |
| Granularity | element → action → workflow; nothing below action, rarely above site |
| Retrieval | exact key match (Stagehand), all-in-context (AWM), none (Skyvern re-reads) |
| Confidence | binary hit/miss; Healenium score-cap closest to graded |
| Freshness | fixed TTL (48h) or none; no measured half-life anywhere |
| Risk classes | handled ad hoc (credential vaulting) not represented per-fragment |
| Transfer | AWM shows cross-task/site transfer of ABSTRACT workflows (+8.9–14 abs); selector caches are strictly site-local by construction |

## 3. The gap (what still gets rediscovered)

1. Every system rediscovers *how to interact* (selectors) OR re-reads the
   page entirely; none accumulate **validated transition fragments with
   empirical success statistics**.
2. No system represents **fragments below the task level keyed by
   subgoal**, retrievable when a NEW task passes through the same subgoal
   (our Run-1 composite result shows this yields ~70% action reuse).
3. No system carries **confidence/freshness/risk/provenance metadata** on
   mechanical knowledge; staleness is either TTL-guessed (48h) or
   discovered by failure.
4. No shared, model-agnostic, externally queryable layer: memories are
   product-internal (Browserbase project scope, prompt context, vendor DB).
5. Failure/recovery knowledge: traces are archived (Skyvern) but recovery
   procedures are not first-class reusable objects.

## 4. What SPIDER adds (differentiators consistent with §7-10,13)

- Subgoal-keyed fragment graph with entry-state anchors + reset-retry glue
  (validated in Run 1: entry-state mismatch was the dominant naive-replay
  failure; glue conversion recovered it at 3 novel actions).
- Empirical confidence = Laplace rate × recency weight (parameterized to be
  MEASURED, G8/G9, not asserted).
- Risk/destructive-class flags per fragment (design present, untested).
- Model/policy-independent consumption demonstrated: store built by one
  policy, consumed successfully by another.
- API-route nodes as peers of browser fragments (G7; unbuilt).

## 5. Honest positioning

SPIDER Run-1 speedups (8.5× wall on exact replay) are consistent in KIND
with Stagehand's reported ~80% two-run speedups; our contribution beyond
the field is the fragment/composition/metadata layer, not the caching idea.
The strongest published evidence that procedural abstraction pays remains
AWM; SPIDER's differentiator is making that abstraction mechanical,
addressable, and statistically maintained OUTSIDE any single model.
