# SPIDER — COMPETITIVE / PRIOR-ART INTELLIGENCE DIRECTIVE

## Mission

This lane exists to discover mechanisms used by competitors, adjacent systems and research projects that could materially improve SPIDER.

It is NOT a marketing-news feed and NOT a generic competitor spreadsheet.

Primary question:

> What publicly evidenced mechanism, architecture, representation, retrieval strategy, learning loop, browser/runtime trick, route/skill abstraction, marketplace/distribution primitive, evaluation method or failure-recovery technique appears to work elsewhere, and what is the strongest honest way to test or integrate it into SPIDER?

The lane must continuously search beyond `intel/competitor_seed.json`. The seed is not exhaustive.

## Scope

Track anything plausibly adjacent to any SPIDER layer, including:

- cumulative operational knowledge of the Web;
- trajectory/workflow/skill induction and reuse;
- procedural memory and sub-procedure extraction;
- semantic, structural or state-grounded retrieval;
- interaction graphs / global navigation maps;
- route/API/shadow-API discovery and replay;
- browser-to-direct-API escalation or hybrid execution;
- model-agnostic skills and cross-agent transfer;
- continual/self-learning agents and specialization/world models;
- shared route/skill/tool registries and marketplaces (the Steam-like infrastructure question);
- browser infrastructure that materially improves reliability, persistence, auth/session continuity, latency, cost or observability;
- web search/extraction layers if their mechanism can reduce repeated exploration;
- evaluation, verification, confidence, freshness, decay, recovery or safety mechanisms relevant to accumulated knowledge.

Do not exclude an actor because it calls itself a browser, memory system, agent framework, MCP registry, data platform, world-model lab or marketplace rather than a SPIDER competitor.

## Research method

Use current public evidence. Prefer, in order:

1. papers / arXiv / OpenReview / PMLR / ACL / conference material;
2. public source code and commit history;
3. official architecture docs, API docs, changelogs and benchmarks;
4. technical blogs / talks by the builders;
5. company pages / press releases;
6. independent reporting only as corroboration or discovery pointers.

The runner may use public internet access, `curl`, Python HTTP clients, GitHub Search/API (`gh`), arXiv, OpenAlex/Crossref/Semantic Scholar when reachable, and links/citations discovered in papers/repos. Do not require paid APIs or personal keys.

Always capture source URLs, dates, version/commit when available and an evidence tier.

## Evidence labels — mandatory

Every substantive claim must be labeled one of:

- `CODE_VERIFIED`: mechanism directly visible in public source code;
- `PAPER_EVIDENCE`: described/tested in a paper with enough detail to reconstruct;
- `OFFICIAL_CLAIM`: vendor/builder claim not independently reproduced here;
- `INDEPENDENT_REPORT`: third-party reporting;
- `INFERENCE_HIGH`: strong inference from multiple public signals;
- `INFERENCE_LOW`: plausible but speculative;
- `UNKNOWN`.

Never silently convert a benchmark or marketing number into fact.

## Mechanism extraction — mandatory

Do not stop at "X has memory" or "Y is faster". For every material actor/paper extract, where evidence permits:

- problem attacked;
- exact retained object: raw trajectory, edge, workflow, function/API, structural sketch, route, state abstraction, semantic memory, etc.;
- induction/acquisition mechanism;
- retrieval/addressing mechanism;
- execution/replay mechanism;
- verification/success oracle;
- freshness/invalidations/versioning;
- fallback on miss/failure;
- cross-task/site/model transfer claim;
- measured success, action count, token/cost/latency or reliability delta;
- evaluation design and strongest baseline;
- known failure modes / hidden assumptions;
- licensing/IP constraints if code is public;
- what SPIDER currently does differently.

## Scout handoff — exactly one mechanism per fresh cycle

The Scout may research broadly, but before ending a fresh cycle it must select exactly ONE highest-information mechanism for reproduction and write `state/intel_candidate.json`.

Required schema:

```json
{
  "mechanism_id": "stable-id",
  "actor_or_paper": "...",
  "mechanism_name": "...",
  "source_urls": ["..."],
  "evidence_labels": ["CODE_VERIFIED|PAPER_EVIDENCE|OFFICIAL_CLAIM|INDEPENDENT_REPORT|INFERENCE_HIGH|INFERENCE_LOW|UNKNOWN"],
  "exact_claim": "...",
  "mechanism_summary": "...",
  "retained_object": "...",
  "retrieval_or_trigger": "...",
  "execution_or_use": "...",
  "verification_or_success_oracle": "...",
  "current_spider_weakness_addressed": "...",
  "minimal_reproduction": "...",
  "strongest_baseline": "...",
  "success_rule": "...",
  "license_or_ip_notes": "...",
  "priority_reason": "..."
}
```

If no mechanism is specified enough to reproduce honestly, the Scout must say so and write `state/intel_candidate.json` with `mechanism_id=null` and the missing evidence. The Reproducer must not invent the missing mechanism.

## SPIDER transfer analysis — mandatory

For every promising mechanism create a recommendation record with:

- `mechanism_id`;
- source actor/paper;
- evidence strength;
- relevant SPIDER lane: `GRAPH`, `PHYSICS`, `SHARED`, or `PRODUCT_INFRA`;
- current SPIDER weakness it could address;
- minimal faithful reproduction or ablation;
- expected upside if real;
- strongest null/baseline;
- measurement required;
- integration cost and dependencies;
- contamination/IP/licensing risk;
- provisional verdict: `EXPERIMENT`, `WATCH`, `REJECT`.

No mechanism is `ADOPT` at Scout stage. Positive integration status requires reproduction + independent audit.

## Anti-copy / anti-hype rule

The goal is to learn from effective mechanisms, not clone competitors.

- Do not copy non-public/proprietary implementation details.
- Respect licenses and note incompatible licenses.
- Reimplement ideas cleanly when needed.
- A competitor result does not override SPIDER's falsification gates.
- Negative evidence about a mechanism is as valuable as positive evidence.
- If a mechanism works only because of benchmark leakage, hand-authored structure, privileged APIs, site-specific assumptions or a stronger model, record that explicitly.

## Scout-cycle outputs

Write Scout findings only to Intel-scoped cycle outputs, including:
- `reports/intel/scout/`
- `results/intel/scout/`
- `state/intel_candidate.json`

The accepted cumulative ledgers and `VALIDATED_MECHANISMS` are updated only later by the Intel Research Director after audit PASS.

## Accepted durable outputs

Maintain on the accepted Intel lane through the Intel Research Director:
- `docs/INTEL_LEDGER.md`;
- `docs/INTEL_TO_GRAPH.md`;
- `docs/INTEL_TO_PHYSICS.md`;
- `docs/INTEL_PRODUCT_INFRA.md`;
- `results/intel/COMPETITOR_INDEX.json`;
- `results/intel/MECHANISM_CANDIDATES.json`;
- `results/intel/VALIDATED_MECHANISMS.json`;
- `state/intel_loop.json`.

Do not edit Graph/Physics accepted results, code or directives directly.

## Priority order for the first program

1. Reconstruct the strongest closest systems from papers/code: Unbrowse, WebNavigator, SkillWeaver, AWM, PolySkill, SkillMigrator, SGDR, NeoCognition public research lineage.
2. Reconstruct the Steam-like/shared-capability infrastructure landscape: route registries, agent skill marketplaces, MCP/skill distribution, contribution/incentive/freshness/trust mechanisms.
3. Browser/runtime systems: Browserbase/Stagehand, Browser Use, Steel, Hyperbrowser, Skyvern, AgentQL and newly discovered equivalents.
4. Memory/world-model adjacencies and current agentic browsers.
5. Discover additional actors via citations, GitHub, papers, changelogs and related-work sections.

Highest priority is not fame; it is mechanism relevance to a currently observed SPIDER weakness.

Current particularly valuable questions include:
- How do strong systems retrieve reusable procedures under paraphrase or state change?
- How do they represent multi-action procedures without losing composability?
- How do they equalize iteration/retry/fallback against graph baselines?
- How do route systems capture first-party APIs and invalidate stale routes?
- How do skill systems transfer across sites/models?
- How do shared registries handle discovery, trust, versioning, scoring and incentives?
- What mechanisms reduce exploration/actions/tokens on repeated work?
- What self-learning/world-model systems retain about environment dynamics rather than merely action sequences?
