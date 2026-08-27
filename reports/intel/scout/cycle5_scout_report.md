# INTEL SCOUT — CYCLE 5 REPORT

Date: 2026-08-25
Run: workflow dispatch #6 of `intel-loop.yml` (GITHUB_RUN_ID 32861355080)
Role: Intel Scout (`docs/roles/INTEL_SCOUT.md` — binding)
Mission: `state/intel_loop.json` priority 1 — does Unbrowse-style browser-to-first-party-API escalation measurably reduce actions/latency vs full browser traversal on SPIDER-relevant sandbox tasks, and what are its fidelity, staleness and failure modes? Select exactly one mechanism for reproduction.
Structured findings: `results/intel/scout/cycle5_findings.json`
Selected candidate: `state/intel_candidate.json`

---

## 0. Cycle-state reconciliation (performed first)

The accepted Intel lane (`lab/intel`) contains exactly one integrated cycle: SGDR state-grounded retrieval, audit PASS run 32800296360. A later Scout snapshot exists **unintegrated** on `origin/cycle/intel/32809100696/scout` ("Intel cycle 2": Unbrowse selection + benchmark forensics). Branch-wide search found **no committed Intel cycles 3 or 4** anywhere (the only "cycle 3/4" hits are Physics lanes). This session therefore executes the still-open priority-1 mission as a fresh Scout cycle, building ON the cycle-2 snapshot instead of duplicating it: its Unbrowse mechanism extraction and CSV forensics stand as recorded; this cycle adds what cycle-2 could not obtain and covers its declared gaps.

## 1. Scope executed

1. Repo-state reconciliation across all branches.
2. Unbrowse fresh evidence: GitHub API metadata + commit log; marketing surface recheck.
3. Citation-graph follow-up on arXiv:2604.00694 via Semantic Scholar API (rate-limited in cycle 2, reachable now).
4. Binding revisit-trigger checks: SkillMigrator code release; WebNavigator releases; NeoCognition disclosure.
5. Priority-3 runtime actor extraction: Stagehand/Browserbase cache internals (direct source reads), Skyvern session-profile reuse, Browser Use posture check.
6. New-actor discovery beyond seed: peek-api, MorphNet, APISensor, HANSEL, HAR quality-testing methodology, protocol-validity auditing, model-endpoint shadow-API fraud literature.
7. Steam-like registry re-sweep (explicit cycle-2 gap): malicious-skill prevalence audit, registry gullibility experiment, published trust-scoring designs, Official MCP Registry status.
8. Sandbox feasibility re-probe.

## 2. Fresh Unbrowse evidence (evidence-tiered)

**Citation graph — the decisive new fact.** Semantic Scholar now answers: arXiv:2604.00694 has **citationCount = 0** as of 2026-08-25 (`CODE_VERIFIED` via API response). No independent evaluation, reproduction or critique exists in the visible scholarly graph. Combined with cycle 2's finding that no third-party evaluation exists on the web either, **any independent measurement SPIDER produces would be the first**. That maximizes information value in BOTH directions, exactly as the mission anticipated.

**Vendor surface advanced.** Repo last push 2026-08-04; v11.3.3 "sync public surface" + CI/npm fixes + "positioning canon — route/action layer for web agents" docs. The repo description still markets "**100x faster**, 80% cheaper locally" against the paper's own 3.6× mean / 5.4× median warmed-cache numbers — the claim-tier gap flagged in cycle 2 persists into the current product surface (`OFFICIAL_CLAIM`, downgraded per anti-hype rule).

**Ecosystem corroboration (new).** `peek-api` (MIT, 39 stars): a standalone community reimplementation of the core loop (browse → filter XHR/fetch → extract auth → dedupe endpoint catalog by method+path → replay via plain HTTP with saved cookies + CSRF injection). Its README traces lineage to an OpenClaw plugin under the `lekt9` org/name — matching the hardcoded `/Users/lekt9/` path in the vendor's own bench harness (`CODE_VERIFIED` cross-reference). Significance: the capture→catalog→cookie-replay loop is demonstrably implementable without the vendor's private backend, which de-risks the clean-room reproduction.

## 3. Revisit triggers (mandated checks)

| Trigger | Status | Evidence |
|---|---|---|
| SkillMigrator code release | **NOT FIRED** | No public code; independent paper-analysis surfaces list "clarify release of code/logs/TIP libraries" as an openness limitation |
| WebNavigator evaluation material | **PARTIALLY FIRED** | Official repo ships Interaction Graphs + precomputed embeddings for five WebArena domains on HF dataset `Jimzhang324/webNavigator`; trajectory release announced-pending. Usable as external evaluation material when Graph needs it; WATCH unchanged |
| NeoCognition disclosure | **NOT FIRED** | $40M seed coverage (Apr + Aug 2026 press): approach undisclosed beyond "world model" framing; no product. Same-lab public artifact WebDreamer (TMLR'25, Dreamer-7B released) noted as Physics context only |

## 4. Priority-3 runtime actors — mechanism extraction

**Stagehand (Browserbase) — deterministic caching at two granularities.** `CODE_VERIFIED`: the v4 branch contains `packages/core/lib/v3/cache/{ActCache,AgentCache,CacheStorage,serverAgentCache,utils}.ts`; ActCache key construction was read directly in source this cycle: `(sanitized instruction, normalizeUrlForCacheKey(pageUrl), sorted variable keys)`; replay validates page state via `waitForCachedSelector` (default 15s attach timeout) before executing cached actions; misses/self-heal fall back to live LLM resolution; AgentCache records whole multi-step runs for zero-LLM deterministic replay; Browserbase-hosted sessions get managed server-side caching with `cacheStatus` HIT/MISS surfaced from act()/extract(). Performance deltas (cold 15–60+s → cached 1–5s, 0 tokens) remain `OFFICIAL_CLAIM`.
→ Role in this cycle: **baseline-design donor**. State-keyed deterministic replay + explicit staleness validation + self-healing fallback is precisely the action-granularity analogue of the route ladder's no-silent-substitution rule. Not a competing candidate: no route/API discovery, no sharing layer, single-agent scope.

**Skyvern — saved-login archives.** `CODE_VERIFIED` (PR #4833, commit 515f632, PR #7032): durable browser profiles created explicitly from closed sessions or persisted workflow runs (async archive upload with ARCHIVE_NOT_READY polling), reuse via `browser_profile_id`, product guidance to validate logged-in state after reuse and conditionalize login blocks. Indexed as Product Infra auth/session-continuity evidence with honest lifecycle handling.

**Browser Use** (~98k stars; Rust-core rebuild) re-checked via independent comparison reporting: autonomous posture, per-step model-call cost model; no cumulative-memory mechanism outranking the mission surfaced.

## 5. New discoveries beyond seed

- **APISensor** (arXiv:2603.23852, `PAPER_EVIDENCE`): unsupervised black-box API discovery from mixed runtime traffic — noise filtering + path normalization, then two-stage clustering (structural interface-shape templates → graph-based semantic refinement within groups). Reported 95.92% group-accuracy precision / 94.91 F1 across six apps, >10k requests, best robustness among 10 baselines (incl. APICARV, APIDrain3, Mitmproxy2Swagger); discovered undocumented Dify shadow APIs confirmed by developers. Code availability UNKNOWN (quick search negative).
  → **Feeds the reproduction's extraction stage**: gives the Reproducer a public quality bar (and fallback algorithm) for mechanical endpoint parameterization beyond naive heuristics.
- **MorphNet** (MIT, 0 stars, single author; `CODE_VERIFIED` surface): computer-use-as-discovery building deterministic execution graphs that re-invoke the site's own JavaScript via CDP (5-strategy entry-point fallback), keyed preconditions on JS bundle sha256 with canary tests and degraded lifecycle; retrieval = URL-pattern precondition filter then capability-statement embedding rank. An **alternate replay substrate**: in-page invocation sidesteps TLS-fingerprint/signature walls that break external HTTP replay, but keeps a persistent browser alive — the exact cost Unbrowse claims to eliminate. RADAR; immaturity bars candidacy.
- **HANSEL** (arXiv:2606.18671): interactive evidence-breadcrumb extraction from trajectories for human verification (83.7% precision / 88.8% recall; −61.6% log volume). Verification/transparency adjacent; WATCH.
- **HAR capture protocol reference** (arXiv:2602.08242, open artifact): DOMContentLoaded → ≤5s network-idle → scroll-triggered lazy-load settle protocol over 18 production sites; documents pervasive redundant calls/missing cache headers. Methodology input for matched-pass discovery baselines.
- **HackDetect** (arXiv:2607.22368): Exposure→Exploit→Mislead attribution for agent-benchmark validity; aligns with SPIDER auditor doctrine; methodology radar.
- **Deceptive Model Claims in Shadow APIs** (arXiv:2603.01919): terminology collision documented — "shadow APIs" there means unofficial MODEL-endpoint resellers (45.83% misrepresent identity); contributes a four-stage endpoint identity/stability verification protocol reusable for shared-infrastructure trust design. Product Infra evidence.

## 6. Steam-like shared-capability infrastructure (cycle-2 gap closed)

- **Measured prevalence, not just threat model:** Koi Security's live-registry audit found **341 malicious skills out of 2,857 examined ≈ 12%** (ClawHub) — `INDEPENDENT_REPORT`. Upgrades cycle-1 entry P-4 from documented-threat to measured-prevalence.
- **Registry gullibility experiment:** OX Security submitted one benign PoC malicious MCP server to 11 registries; **nine published it without security review** (incl. LobeHub, Cursor Directory); GitHub alone rejected — `INDEPENDENT_REPORT`.
- **Published scoring designs:** MCPSkills.io 15-signal composite trust scoring (2,631 scored; sampled MCP Registry cohort: 83% disqualifier flags, 58% single-author, 21% license-less, mean legitimacy 3.05/10 — `OFFICIAL_CLAIM`, stated-reproducible methodology). skill-swarm-mcp ships a concrete open trust engine: five weighted git-quality dimensions, TRUST≥0.75-auto-install through REJECT<0.25-block verdict tiers, install-time security-scan gate, two-phase high-trust-first registry search, BM25F+7-signal local matching, dead-skill detection — `CODE_VERIFIED` surface.
- **Infrastructure:** Official MCP Registry is live (production/staging/local); Smithery moves to hosted-connect with open-source agent.pw vault. Platform scale figures (8.5k–57.8k servers/skills across directories) remain unnormalized `OFFICIAL_CLAIM`s.
- **Synthesis for Product Director:** contributed-capability trust is now a measured problem with public countermeasure designs; content-addressed versioning (P-3) + operation-time policy enforcement remain load-bearing; static scores are signals, not verdicts (MCPSkills' own disclaimer).

## 7. Transfer analysis and selection

Full machine-readable records: `results/intel/scout/cycle5_findings.json`. Provisional verdicts:

| Mechanism | Lane | Verdict |
|---|---|---|
| unbrowse-route-capture-replay-ladder | PRODUCT_INFRA (+GRAPH execution) | **EXPERIMENT (selected, reconfirmed)** |
| apisensor-traffic-api-discovery | SHARED (extraction-stage donor) | INDEXED — feeds reproduction design |
| stagehand-actcache-agentcache | PRODUCT_INFRA | INDEXED — baseline-design donor |
| skyvern-browser-profiles | PRODUCT_INFRA | INDEXED |
| morphnet-js-invocation-graphs | PRODUCT_INFRA | RADAR |
| peek-api-standalone-capture-replay | PRODUCT_INFRA | WATCH (corroborating actor) |
| hansel-trajectory-evidence | GRAPH (presentation/provenance) | WATCH |
| webnavigator graphs/embeddings | GRAPH (external eval material) | WATCH (trigger partially fired) |

**Selected exactly ONE mechanism:** `unbrowse-route-capture-replay-ladder` (same mechanism the unintegrated cycle-2 snapshot selected; evidence base refreshed and strengthened this cycle).

Why it remains highest-information:
1. Assigned priority-1 mission; feasibility gates pass (all four sandbox targets reachable today: 201/200/200/200); stop-condition fallback NOT triggered.
2. Zero citations + zero independent evaluations anywhere → first-mover measurement value in both directions; vendor marketing still outpaces its own paper (100x vs 3.6×).
3. Ecosystem corroboration de-risks clean-room implementation (peek-api) and supplies baseline designs (Stagehand) plus an extraction-stage quality bar (APISensor).
4. Nothing discovered among priority-3 actors or new papers constitutes a higher-information reproduction candidate under directives priority order.
5. The same reproduction yields shared-registry evidence (ladder semantics, TTL/drift, opt-out/ToS gates) for the Product Infra line, per priority 2.

## 8. Honest limits of this cycle

- If uncommitted Intel Scout sessions between cycles 2 and 5 existed outside git, their findings are unknowable here and treated as non-existent (evidence discipline).
- APISensor code availability checked only via one repository-search query; method taken from paper text.
- peek-api/MorphNet inspected at README/docs + metadata level, not line-audited (unnecessary for their roles).
- Stagehand performance deltas remain vendor-documented; only code presence and key-construction were independently verified.
- Platform scale/trust statistics are platform-reported and not cross-normalized.
- NeoCognition trigger judged unfired on press + company-site surfaces; deep crawl of its research page not performed.
