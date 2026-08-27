# INTEL SCOUT — CYCLE 6 REPORT

Date: 2026-08-25
Role: Intel Scout (`docs/roles/INTEL_SCOUT.md` — binding)
Mission: `state/intel_loop.json` priority 1 — does the validated capture→extract→parameterize→replay route ladder hold beyond a single API host (≥4 heterogeneous first-party-API sandbox hosts), survive NATURALLY elapsed TTL (calendar time, no rewinding), and detect INDUCED response-schema mutations with transparent escalation? Select exactly one mechanism for reproduction.
Structured findings: `results/intel/scout/cycle6_findings.json`
Selected candidate: `state/intel_candidate.json`
Pre-selection consultation: three independent contexts (`cto_intel`, `ecosystem_scout`, benchmark critic) — all three returned CONFIRM_SELECTION / "nothing outranks it" with material design upgrades incorporated below.

---

## 0. Mission framing

Cycle 5 validated `unbrowse-route-capture-replay-ladder` at PROOF OF CONCEPT ceiling on a **single-host API-tier slice** (httpbin.org, two flows). The binding wording lists multi-host scope, real calendar-time staleness and real mutation handling among the explicitly Not-established boundaries. The Director's cycle-6 mission converts exactly those boundaries into the testable question. The Scout's job this cycle: (1) establish whether the stop-condition fallback triggers (<4 qualifying reachable hosts), (2) refresh external evidence and revisit triggers, (3) discover beyond seed, (4) select exactly one mechanism.

## 1. Live feasibility probe — stop-condition NOT triggered

Probed 2026-08-25 from runner egress (curl, status/content-type verified). Qualification = reachable, sandbox-intended or explicitly agent-welcoming, first-party JSON API inducible through some surface:

| Host | Probe result | Browser surface for passive capture | Auth style | Scout qualification note |
|---|---|---|---|---|
| httpbin.org | 200 (/forms/post, /html) | HTML forms submit→JSON; cookie flows | none + cookie state | Incumbent; robots allows all but /deny |
| petstore.swagger.io | 200 UI; 200 swagger.json | Swagger UI issues XHR to same-host API on Try-it-out | none (v2 demo api-key nominal) | Public OpenAPI = template-correctness ground truth, BUT runtime known to diverge from its spec (undocumented statuses, 400-for-404) — validate against spec AND observed traffic |
| www.demoblaze.com → api.demoblaze.com | 200 / 200 | Full JS store SPA over first-party JSON API (signup/login/cart/place-order) | session-token (signup→token in localStorage flows) | **Pivotal host: spec-less SPA regime**, closest sandbox analog to real first-party APIs; no robots.txt exists (404); shared demo DB — write-pollution ethics require scoped, prefixed, cleaned-up records |
| restful-booker.herokuapp.com | 201 /ping; 200 /booking; POST /auth→200 token | **UI removed upstream (cycle-5 fact stands)** | token (POST /auth) | API-tier only — cannot contribute to discovery-during-browser-completion; community-documented ~10-minute data reset means its natural-TTL cell measures reset cron, not decay |
| jsonplaceholder.typicode.com | 200 JSON | none | none | Trivial CRUD; declared-contract class; content-signal boilerplate only, no disallow |
| reqres.in | 200; llms.txt + openapi.json live | docs + explicit Agent Sandbox surfaces (/agent/v1/*) + payments sandbox | tiered (demo none / project token) | Explicitly "welcomes AI assistants, agents, and crawlers" yet robots Disallow:/api/ for crawlers — needs a written interpretation + rate caps before use; notable ecosystem signal (see §5) |
| dummyjson.com | 200; POST /auth/login→JWT accessToken verified | docs UI only | JWT bearer (expiry <24h — interacts with route TTL) | Tier-2 ambiguous: Cloudflare-managed Content-Signal search=yes,ai-train=no,use=reference AND wildcard Disallow /auth/ — include only with disclosure next to any JWT result, or drop |
| gorest.co.in | 200 public reads | none | bearer-token writes | robots Disallow /public-api/; tier-3 backup only |
| fakestoreapi.com | **403 (Cloudflare)** | — | — | EXCLUDED on availability/control |
| demo.owasp-juice.shop / juice-shop.herokuapp.com | **503 both** | — | — | Unavailable this cycle |
| restful-booker.platform.dev | **unreachable** | — | — | Environment churn datum: the alternate URL died while herokuapp revived — lability itself is route-staleness context |

**Conclusion:** even under the strictest access-tier discipline (critic's taxonomy), at least four qualifying cells exist spanning four distinct auth styles (no-auth+cookie, session-token, JWT, auth-token; plus nominal api_key): httpbin.org, demoblaze, restful-booker (API-tier), petstore (spec-ground-truth class), with reqres.in/jsonplaceholder/gorest as labeled declared-contract or restricted extras. **Stop-condition fallback does NOT fire.**

## 2. Fresh Unbrowse evidence

- **Vendor posture shift toward honest negatives (`CODE_VERIFIED`, repo `docs/benchmarks.md` read this cycle):** the vendor deleted script-based benches ("benches should never be scripts", commit 2026-05-26) and now ships `bench-run.ts` (evidence-only executor; verdicts rendered in-thread by an LLM agent per rubric) plus `unbrowse-corpus-bench`: corpus harvested live per run from r/webscraping + curated seeds, difficulty-tagged R/H/A. Self-reported results: **retrieval coverage 0.50 across every difficulty tier (12/24)**, execution axis resolve→execute **1/6 sampled**, security axis credential-redaction **pass 24/24**; misses named by vendor class (cloudflare-js-challenge, datadome); ANTIBOT_BLOCK deliberately counted in denominators ("honest negatives are the product"). Significance: (a) independently corroborates cycle-2 forensics' adversarial-coverage figure; (b) the vendor's own protected-target boundary is where the true mechanism limit lives; (c) SPIDER's audited sandbox result must never be conflated with either the vendor's 94-domain warmed-cache headline or its corpus bench — different populations, all OFFICIAL_CLAIM/self-run.
- Citation status: Semantic Scholar rate-limited (429) throughout this cycle's attempts; cycle-5's same-day check (citationCount=0 as of 2026-08-25) stands uncontradicted. No independent evaluation surfaced in any sweep this cycle.
- No new vendor release signals beyond those recorded in cycle 5 (repo marketing still "100x faster" vs paper's own 3.6× mean — claim-tier gap persists).

## 3. Ecosystem commoditization discovery (the decisive new landscape fact)

At least five independent public implementations now convert captured browser traffic into declarative specs — the ladder's extraction stage is becoming a commodity:

1. **Browserbase `browser-to-api` skill** (`CODE_VERIFIED`, github.com/browserbase/skills): consumes `browser-trace` CDP request/response captures, templatizes URLs, infers JSON schemas, emits **OpenAPI 3.1** + coverage report + `confidence.json`; `x-confidence`/`x-observed-auth` extensions; GraphQL/multiplexed-endpoint decomposition.
2. **TabAPI** (`CODE_VERIFIED`, Lay4U/tabapi): record→analyze→export **OpenAPI 3.0 + TS SDK + MCP server config + replay tests**; `tabapi replay` returns pass/fail/**changed** summaries for CI drift detection.
3. **Vespasian** (`CODE_VERIFIED`, praetorian-inc/vespasian, Apache-2.0, 125★, pushed 2026-08-24): traffic/HAR/Burp import → REST/GraphQL/SOAP/gRPC spec recovery incl. **SPA bundle static extraction recovering routes no click exercises** (Next.js chunk-filename segment mining), 404-decoy filtering, byte-deterministic output.
4. **Harpist** (`CODE_VERIFIED`, kenobi-ai/harpist, MIT, 9★, pushed 2026-08-04): Chrome-recorded workflow traffic → **versioned per-host `contract-profile.json`** → derived contract.ts/openapi.json/docs; additive recordings (later sessions refresh credentials + extend endpoint set); credentialed replay + `auth check --all`; ships as an agent skill so the agent refines its own recordings. Closest uncovered analog to the Unbrowse ladder with an explicit invalidation story.
5. **mitmproxy2swagger / mitm2openapi** (established OSS): HAR→OpenAPI 3.0 conversion — the cheap null-arm generator.

**Implication adopted into the selected reproduction (per cto_intel + critic):** the decision-relevant quantity is no longer only replay-vs-browser (cycle 5 settled its shape) but **capture-value-over-declaration (B−D)**: a GENERATED_SPEC_NULL arm builds a direct-HTTP client purely from a spec auto-generated off the Reproducer's own discovery-pass HAR (or from public machine-readable contracts where they exist) under identical clocks/equivalence gates. Preregistered directional prediction: on spec-public hosts docs-null ≈ replay; on spec-less hosts (demoblaze) replay > spec-null. If spec-null reaches parity everywhere, the honest verdict flips to REPRODUCED_NO_ADVANTAGE for the observation mechanism (packaging, not perception). The mechanism's defensible niche contracts to: spec-less SPA regimes, auth-material association/lifecycle, and drift/fallback handling.

## 4. Adjacent-system staleness-rate priors (new quantitative anchors)

- **PreAct** (arXiv:2606.17929, `PAPER_EVIDENCE`): verify-gated compiled replays for CUAs; blind linear replay showed **50–67% cache-miss rates on WebArena**; verify-before-store gate **rejected ~83% of compiles** there (brittle predicates). First published quantification of how fast naive action-level replay goes stale — the action-granularity counterpart to the route-ladder's TTL question. Also documents that gate-only without miss→fallback loses to blind caching (fallback policy is load-bearing).
- **Weblica** (arXiv:2605.06761, `PAPER_EVIDENCE`): HTTP-level record/replay for training-env construction with **auto-synthesized volatile-parameter normalization rules** (timestamps/tokens stripped from URLs/headers/bodies), rule validation by isolated playback, replay-fidelity-as-admission-criterion (15.6K of 146K tasks retained). Method donor for equivalence-canonicalization and cache-key normalization under drift.
- **Muscle-Mem** (`CODE_VERIFIED`, pig-dot-dev/muscle-mem, Apache-2.0, ~766★): behavior cache keyed by environment Checks (`capture`/`compare`); hit→deterministic trajectory replay with zero model calls; **no TTL concept at all** (pure environment-match validity) — the design gap the route ladder's natural-TTL arm probes.
- **Screen-activity compilation** (arXiv:2608.05784, `PAPER_EVIDENCE`): guarded replay plans fail safe via expected-element/role guards; introduces measured **Routine Overhead Ratio R=60–343×** and delegable recurrence h≈8%, bounding fleet-wide replay savings at h·(1−1/R)≈8% — the emerging honest-accounting frame any "replay saves X%" claim will be judged against; forbids double-counting with caching gains.

## 5. Steam-like shared-capability infrastructure (new entries for the P-line)

- **reqres.in agent-native API surface** (`CODE_VERIFIED`): llms.txt + llm.json + openapi.json + pricing.md machine-readable contracts; explicit Agent Sandbox (`/agent/v1/*`) and payments sandbox with idempotency-key replay semantics, test clocks, signed webhooks. An API provider openly building for agent consumers — supports the "agent-native surfaces reduce repeated exploration" hypothesis and supplies a ToS-explicit target class.
- **x402 Bazaar** (Coinbase/x402 foundation, `OFFICIAL_CLAIM`): payment-gated service listings embedded in HTTP 402 responses, JSON-Schema-validated, catalog keyed by canonical **routeTemplate** (`/users/:userId`) so parameterized calls collapse into one listing; `/discovery/search`; Bazaar MCP server wraps 402→pay→retry. The clearest live instance of routes-as-products economics. Parallel rails: OpenAI/Stripe Agentic Commerce Protocol (date-versioned spec snapshots), Parallel MPP pay-per-call gateway.
- **Official MCP Registry trust stack matured** (`CODE_VERIFIED` mechanics): namespace ownership proof (GitHub OIDC/DNS TXT/HTTP challenge), metadata-not-artifacts hosting, namespaced `_meta` enrichment. On top: **MCPLookup** Trust Index (usage-ranked trailing-30-day downloads; thin-evidence ⇒ unrated) and **Unfragile Census** (~79,858 cross-registry listings machine-verified — package resolution, endpoint liveness, tool-schema extraction — Ed25519-signed passports; **only ~15% verifiable alive**). Registry-aliveness prevalence joins malicious-skill prevalence (~12%) as measured infrastructure facts.
- **Commercial drift-detection incumbents** (`OFFICIAL_CLAIM`): Akto Runtime Analyzer (traffic→inventory→"API Changes" feed with change detection) and APIContext conformance (live-response-vs-spec diffing every synthetic run). They define what production-grade "detection quality under schema mutation" currently means — neither is agent-native nor browser-origin, which is precisely the gap the selected reproduction occupies.
- **@skills protocol** (arXiv:2608.12610, `PAPER_EVIDENCE` + implementation): separates content/persistence/auto-triggering of skills; path-addressed reading instead of prompt-resident install; July-2026 census: **56,804 SKILL.md directories across 1,133 repos**, install locations fragmented across 54 directory conventions; `/.well-known/agent-skills/index.json` self-hosting convention exists but rarely used. Distribution-layer evidence; no demonstrated reduction in repeated work ⇒ WATCH/P-line only.
- **SkillTrace** (arXiv:2608.05204): multi-trace provenance auditing for skill reuse (Expression/Implementation/Operational traces; Skill Operational Graph; AUROC 0.938 vs repo-level baselines 0.841; 36,446-skill wild audit). Directly reusable for contributed-route provenance/duplicate governance when SPIDER capsules ever enter distribution.
- **QCR** (arXiv:2608.12847, `PAPER_EVIDENCE`): post-retrieval reuse formulated and measured separately from retrieval (2,391 instances, WebArena/WorkArena/AppWorld): target-bound support notes (workflow invariant + bindings-to-reobtain + applicability conditions incl. decline + verification guardrail) beat full-trajectory injection by +10.7 pts success at −48.9% online tokens; stale-binding errors 46.9%→10.9% under large shift; raw-trajectory utility retains only 8.2% of no-shift value under large rewrite. **Strongest existing evidence that raw-trace inheritance decays under binding shift and that support-object shape dominates substrate choice** — maps 1:1 onto Capability Capsule required fields (PARAM_UNRESOLVED/SCHEMA_MISMATCH/applicability/verifier). GRAPH/Product-schema relevance; not selected this cycle (LLM-agent harness out of Intel-lane scope; Graph lane owns addressing/reuse experiments).
- **FCPAgent** (arXiv:2607.24167): falsifiable commitment units (confirming+falsifying evidence per plan step) with scope-aware repair, +13.8% rel. success WebArena — verification/negative-knowledge design radar.
- **Skill-library retrieval negative result** (arXiv:2608.06196): typed LLM-generated graph edges add zero retrieval reach over embedding kNN (98.6% edge redundancy; "topology bound"); author-written queries overstate hit@5 by up to 44 points. Cautionary methodology for any Graph addressing evaluation (non-echo queries mandatory).
- **MCP registry drift panel** (arXiv:2608.00997): first longitudinal registry measurement (88.6 days, 19,099 servers): description drift ≈12%/30d concentrated in ~5% of servers; drift-history-ranked re-auditing covers only ~20% of changers at top-5% budget; **content-binding (hash-move revalidation) + sized periodic sweep is the fitting control**. Candidate next-next Intel mechanism (below).
- Flagged-but-cut (radar only): agentrr (BLAKE3-keyed LLM-proxy record/replay + verify), Healenium Pro healing proxy (locator-level repair analog), Zatanna/Kampala (YC W26 app→API interception), arXiv 2608.07911 (replay semantics alone can invert cache-policy rankings — replay-fidelity eval caution).

## 6. Revisit triggers (mandated checks)

| Trigger | Status | Evidence |
|---|---|---|
| SkillMigrator code release | **NOT FIRED** | S2 citationCount=0 (fetched this cycle); emergentmind analysis repeats the paper's own limitation ("clarify release of code/logs/TIP libraries"); GitHub searches negative |
| NeoCognition disclosure | **NOT FIRED** | Site/press re-checked: manifesto + $40M seed coverage only; no paper/code/product spec |
| WebNavigator external-evaluation use | unchanged (material available; no Graph replay claim pending this cycle) |
| APISensor code release | NOT FIRED (no release found) |
| MorphNet maturity | NOT FIRED (still unmeasured/unadopted) |

## 7. Selection — exactly one mechanism

**SELECTED: `unbrowse-route-capture-replay-ladder` — same actor, materially changed question (mission-permitted), upgraded design.**

Why it remains highest-information:
1. Assigned priority-1 mission; stop-condition fallback NOT triggered (≥4 qualifying hosts probed live today, §1).
2. Both genuinely uncertain regimes are now addressable: SCHEMA_MISMATCH detection quality under controlled mutation (vendor admits auto-deprecation unwired; no independent measurement anywhere) and the spec-less session-token SPA regime (demoblaze), which no prior SPIDER cycle touched.
3. The new commoditization landscape makes the experiment *more* discriminating, not less: the generated-spec null turns the cycle into a market-segmentation map (where does traffic-derived capture add value over declaration?) that directly steers Runtime capsule schema and Product positioning.
4. Feasibility de-risked: harness pattern/probes/checkers exist from cycle 5; all consultation contexts independently confirmed nothing outranks it (alternatives are either Product-lane engineering, Graph-lane work, or distribution-layer infra without demonstrated repeated-work reduction).
5. Negative results remain first-mover publishable either way (citation graph still empty; vendor's own bench stops at coverage counts, never lifecycle/drift).

Incorporated design upgrades (from the three independent consultations — these travel with the handoff):
- Two-phase preregistration: mechanical pilot audit window → frozen host roster + exclusion ledger timestamped into prereg BEFORE measured passes; host×arm eligibility matrix (discovery-capable / replay-capable / TTL-informative / mutation-probeable); headline claims restricted to fully qualified cells.
- Access-tier taxonomy with verbatim robots/terms quotes; honest UA, ≤1 rps caps, backoff; dummyjson included only with its Content-Signal/auth-path disallowance disclosed (or dropped); demoblaze write-pollution ethics handled by unique prefixes + cleanup verification.
- Matched-pass definition fixed: per-host calibrated quiescence wait (p99 inter-request gap + margin, hard cap) instead of deprecated `networkidle`; identical retry/timeout budgets; symmetric warm/cold policy; wall-clock decomposed (render/network/tool segments) with absolute seconds reported alongside ratios; scripted-policy scope stated (UI-traversal-vs-direct-HTTP economics, not agent economics).
- Output-equivalence canonicalization frozen in prereg: volatility profiling via double-run of genuine completion; sorted-keys deep compare dropping volatile class; order-insensitive arrays unless semantically ordered; ids via pointer indirection; conservative default strict; adjudication capped (>10% ⇒ MEASUREMENT_INVALID).
- Natural-TTL attribution: STALE_TTL event counts ONLY with positive differential (fresh discovery succeeds while artifact replay fails at T+24h); redeploy fingerprints both windows; infrastructure failure codes separated by header evidence (cf-ray/challenge markers); UNATTRIBUTED_DRIFT excluded from TTL claims; second window mandatory if any fingerprint changed. Restful-booker excluded from TTL claims (reset cron).
- Mutation probing de-circularized: replica schemas sourced independently of own captures where public contracts exist; mutation classes span surface/semantic/behavioral drift seeded from real historical API breaking-change taxonomies; false-positive trials on benign variation (key order, whitespace, added optional fields) with Wilson-CI'd FPR; unknown-field tolerance predeclared ON/OFF; mutation schedule sealed (committed hash withheld until runs complete); wording boundary: "sensitivity to predeclared mutation classes under controlled replicas" — NEVER "detects live-site drift"; opportunistic live-drift anecdotes reported separately.
- Statistics: per-host paired log-ratio BCa bootstrap primary; mixed-effects cross-host (host random intercept, auth-tier interaction); asymmetric n permitted (replay 20–30 vs browser ≥5) with MDE predeclared; randomized block order; leave-one-host-out required (wins-concentration precedent); denominator floor (<2s browser passes reported separately); Holm on secondaries.
- Mechanical verdict rules enumerated (silent substitution anywhere ⇒ MEASUREMENT_INVALID; adjudication>10%; availability<95%; discovery below floor; cross-arm contamination; infra-coded failures>20%). REPRODUCED_USEFUL requires gate-pass ≥90% lower-bound on every qualifying host + zero invariant violations + log-ratio CI>0 with ≥half hosts individually CI>1 + spec-null failing/slower on ≥1 spec-less host (causal separation). REPRODUCED_NO_ADVANTAGE iff gates pass but spec/null parity everywhere or speedup CI includes 1.
- Intent-addressing secondary arm retained: exact-intent vs prefix-inheritance vs (optionally) fused task+state-summary scorer on multi-host route sets — settles the cycle-5 intent-labeling artifact datum.

## 8. Next-next candidates queued (not selected)

1. **Content-binding freshness control for route stores** (from arXiv:2608.00997 policy result + TabAPI/Vespasian CI replay-diff practice): replace naive calendar-TTL decay with schema-hash-move-triggered revalidation + sized periodic sweep; directly populates Capability Capsule freshness/invalidation fields; cheap, falsifiable.
2. **Harpist versioned contract-profiles** as an alternative retained-object schema (additive merge + credential-refresh invalidation) — compare against pointer-only route records when capsule schema work begins.
3. **QCR support-note schema** as required-field donor for capsule composition/decline semantics (Graph-lane routing recommended).

## 9. Honest limits of this cycle

- Semantic Scholar remained rate-limited; Unbrowse citation status carries forward from cycle 5's same-day check rather than a fresh fetch.
- demoblaze qualification rests on its established status as a QA-practice sandbox and absence of prohibitive terms; no formal terms document was found (absence of robots ≠ grant) — the Reproducer must keep writes scoped/cleaned.
- reqres.in's welcome-vs-disallow tension needs the written interpretation promised above before it feeds headline claims.
- Ecosystem-scout product claims (Spectral, x402 Bazaar scale, MCPLookup/Unfragile stats) taken at OFFICIAL_CLAIM tier; not independently reproduced.
- petstore runtime-vs-spec divergence documented by third-party sources, not re-verified here; treat spec-only template scoring as insufficient.
- Playwright's `networkidle` deprecation nuance retroactively qualifies (does not invalidate) cycle-5's "realistic network-idle load policy" wording; absolute seconds were committed then, which limits exposure.
