# INTEL SCOUT — CYCLE 1 REPORT

Date: 2026-08-24
Role: Intel Scout (`docs/roles/INTEL_SCOUT.md` — binding)
Mission: `state/intel_loop.json` (priority 1) — identify the publicly evidenced SPIDER-adjacent mechanism that most directly addresses the Graph weakness in **robust procedure addressing** or the product-level need to **reduce repeated exploration**.
Structured findings: `results/intel/scout/cycle1_findings.json`
Selected candidate: `state/intel_candidate.json`

---

## 1. Scope executed

Per `directives/INTEL.md` priority order:

1. **Priority-1 systems reconstructed from papers/code**: SGDR, SkillMigrator/"Beyond Domains", Unbrowse, WebNavigator, AWM, SkillWeaver, PolySkill, NeoCognition.
2. **Steam-like shared-capability infrastructure**: skills.sh/Vercel, LobeHub/agentskills mirrors, Unbrowse registry, marketplace-governance papers.
3. **Discovery beyond seed**: 15+ new actors via Semantic Scholar citation graphs of SkillWeaver, related-work sections of arXiv:2606.04391 and arXiv:2606.17645, and the agent-skills survey (Preprints 202605.1276).

## 2. SPIDER weakness grounding

Accepted state (`SPIDER_MASTER_PROMPT.md` §14, `docs/NEXT_GRAPH.md`, `graph/store.py`):

- Fragment reuse ~69.6% is only a small hand-structured POC; semantic addressing NOT solved; goal signatures are hand-authored.
- `graph/store.py` addresses fragments solely by exact `goal_sig` (`ix_frag_goal`); no paraphrase or state-conditioned retrieval exists.
- Entry-context mismatch is a real measured failure mode.
- Physics WP-002B already showed plain nearest-neighbour retrieval performs at least as well as induced rules — retrieval quality is a live scientific question inside SPIDER, not just engineering.

## 3. Priority-1 mechanism extraction (summary table)

| Actor | Retained object | Addressing/retrieval | Evidence tier | Code | Key numbers (as reported) |
|---|---|---|---|---|---|
| **SGDR** (arXiv:2606.04391) | Dual text-code skill (desc + executable code), sliding-window sub-procedures L∈{2..5} | **Every-step fused score**: α·cos(task,desc)+(1−α)·cos(state-summary,desc); top-M=max(3k,20); greedy MMR λ=0.7; semantic dedup on insert | PAPER_EVIDENCE + **CODE_VERIFIED this cycle** | yes (official, CC BY-SA 4.0) | WebArena avg success 37.5% (GPT-4.1), 24.3% (Qwen3-4B); beats AWM/ASI/CER |
| **SkillMigrator** (arXiv:2606.17645) | TIP = skill + induction-time snapshot structural sketch + slot schema | Layout-similarity + text retrieval from one global library; ground slots to live refs before replay; primitive fallback on weak match | PAPER_EVIDENCE | not found | −8–10% LLM actions at matched success (WebArena+Mind2Web) |
| **Unbrowse** (repo + arXiv:2604.00694) | First-party API routes captured from HAR; route-graph edges | Intent resolve → cached route (<200ms claim) → browser fallback; shared registry w/ publish/score/version/payouts | CODE_VERIFIED (surface) / OFFICIAL_CLAIM (numbers) | yes (MIT) | 3.6× mean / 5.4× median over Playwright, 94 domains (vendor-run) |
| **WebNavigator** (arXiv:2603.20366) | Interaction graph from zero-token heuristic exploration | Retrieve-Reason-Teleport deterministic pathfinding | PAPER_EVIDENCE (+code MIT, graphs/embeddings public) | yes (MIT) | 72.9% WebArena multi-site (not independently reproduced) |
| **AWM** (arXiv:2409.07429, ICML'25) | Induced textual workflows, merged routines | Task-level injection into prompt (static per task) | PAPER_EVIDENCE | yes (Apache-2.0) | +51.1% rel. WebArena; reviewers criticized induction methodology |
| **SkillWeaver** (arXiv:2504.07079) | Synthesized Python APIs per site | Autonomous discovery; reward-model honing; task-level API provision | PAPER_EVIDENCE | yes | +31.8% rel. WebArena; strong→weak transfer up to +54.3% rel.; ≈ human-authored APIs |
| **PolySkill** (arXiv:2510.15863) | Polymorphic skill: abstract goal ≠ concrete implementation | Goal-keyed reuse across implementations, same domain | PAPER_EVIDENCE | yes | 1.7× reuse seen sites; +13.9% unseen; −20% steps |
| **NeoCognition** | undisclosed ("world model per micro-world") | unknown | OFFICIAL_CLAIM only | no | $40M seed; watch |

## 4. Steam-like infrastructure mechanisms (evidence-labeled)

- **Usage-telemetry ranking** — skills.sh ranks by anonymous CLI install counts; open-source CLI (`vercel-labs/skills`). OFFICIAL_CLAIM/CODE_VERIFIED.
- **Packs** — bundle public+private skills into one install command (distribution primitive). OFFICIAL_CLAIM.
- **Trust/audits** — routine security audits page + explicit non-guarantee disclaimer; official curation tier. OFFICIAL_CLAIM.
- **Route marketplaces with incentives** — Unbrowse: publish/score/version sanitized routes; contributor wallet payouts; three-tier execution ladder (skill cache → shared route graph → full browser as source of truth) with an explicit "never silently substitute replay for live traversal" rule. CODE_VERIFIED surface / OFFICIAL_CLAIM economics.
- **Ecosystem versioning is weak** — identical skill artifacts mirrored across registries with divergent versions (observed for unbrowse listings). INFERENCE_HIGH from inspected metadata.
- **Documented threat model** — hidden-comment injection (arXiv:2602.10498) and trivially simple prompt injections via skills (arXiv:2510.26328): any future SPIDER registry design must treat contributed procedures as untrusted input.

## 5. New actors discovered beyond seed

Graph of Skills (dependency-aware structural retrieval, arXiv:2604.05333); ContractSkill (verifiable/repairable contract-based skill artifacts, arXiv:2603.20340); Hierarchical Memory Tree (pre/post-conditioned web memory, arXiv:2603.07024); EchoTrail (critic-guided trajectory filtering); SAGE (RL-trained skill-library use, AppWorld); WMA (web world models, ICLR 2025 — PHYSICS-relevant); CER (experience-replay baseline); WALT (site-tools-over-primitives); the 2026 skill-infrastructure wave (SkillNet, SkillFlow, WebXSkill, SkillClaw, MIND-Skill, MMG2Skill, SkillTracer, SkillLearnBench, CASCADE, ASI); the agent-skills survey with a governance/marketplace layer (Preprints 202605.1276); NeoCognition as radar company entry.

## 6. SPIDER transfer analysis (mandatory records)

Full machine-readable records in `results/intel/scout/cycle1_findings.json`. Provisional verdicts (Scout stage — nothing is ADOPT):

- **sgdr-state-grounded-dynamic-retrieval → GRAPH: EXPERIMENT (selected).**
  - Weakness addressed: robust procedure addressing under paraphrase AND mid-task state drift; entry-context mismatch; repeated exploration cost.
  - Minimal faithful test: replace/augment `fragments.goal_sig` lookup with dual task+state-summary cosine scoring + MMR over fragment descriptions, on SPIDER's existing scripted-route store; conditions: (A) current goal_sig addressing, (B) task-text-only embedding retrieval (strong simple baseline), (C) fused α score + state summary + MMR. Matched execution policy; measure retrieved-correct rate under paraphrased goals and shifted entry contexts, plus downstream reused-action fraction and LLM/state-summary call cost.
  - Strongest nulls/baselines: exact goal_sig (current), task-text-only embedding, random-fragment null; SGDR's own repo retains AWM/ASI/CER baselines for later scale-up.
  - Expected upside if real: fragments become addressable from natural goals without hand-authored signatures; reuse survives entry-state mismatch.
  - Integration cost: low-moderate (embedding dependency; one state-summarizer LLM call per novel state, hash-cached as in reference implementation).
  - Contamination/IP: clean-room reimplementation required (reference code CC BY-SA 4.0 — copyleft; do NOT copy source into SPIDER). Paper formulas are public and sufficient.
- **skillmigrator-tip-layout-retrieval → GRAPH: WATCH.** No public code found; smaller reported effect; harder faithful reproduction; revisit after SGDR-style addressing scaffolding exists.
- **unbrowse-route-cache-marketplace → PRODUCT_INFRA: EXPERIMENT (later cycle).** Closest public precedent for SPIDER's browser→API escalation + shared registry; headline speedups remain vendor-run claims pending independent reproduction.
- **webnavigator-interaction-graph → GRAPH/PHYSICS context: WATCH.** Deterministic pathfinding-over-topology is directly comparable to Graph replay claims; its released graphs/embeddings could serve as external evaluation material.
- **awm / skillweaver / polyskill → GRAPH: WATCH.** Induction-side ideas; their addressing is static/task-level relative to SGDR.
- **neocognition → RADAR: WATCH.** No public mechanism.
- **skills.sh telemetry ranking, packs, audits, Unbrowse payout/versioning, skill-injection threat literature → PRODUCT_INFRA: evidence stored** for Product Director synthesis.

## 7. Selection decision

**Selected exactly ONE mechanism for reproduction this cycle:** `sgdr-state-grounded-dynamic-retrieval`.

Rationale: highest information per unit reproduction risk — it targets the exact measured SPIDER weakness (addressing), is specified to the formula level in both paper and public code (verified this cycle: scoring function, MMR, insert-time dedup, state summarizer with caching/fallback), maps onto the existing Graph schema with no new infrastructure, ships its own strongest baselines, and its license permits clean-room reimplementation. Paper/code discrepancy recorded honestly: paper states α=0.5, code default is α=0.4 — the reproduction must preregister its α choice and may ablate both.

Runner-up (SkillMigrator TIP layout retrieval) deliberately deferred: no public code, smaller claimed effect, higher fidelity risk.

## 8. Honest limits of this cycle

- Headline numbers cited are PAPER_EVIDENCE/OFFICIAL_CLAIM; none were independently reproduced here (that is the Reproducer's job).
- SGDR evaluates same-site online reuse on WebArena; cross-site/cross-domain transfer of the mechanism is UNTESTED by its authors — SPIDER should not assume it transfers.
- Unbrowse ToS/legality of first-party-API replay is unresolved; flagged, not judged.
- NeoCognition remains opaque; no inference beyond official positioning.
