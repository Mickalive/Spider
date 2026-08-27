# INTEL SCOUT — CYCLE 7 REPORT

Date: 2026-08-25 (session started ~22:50Z)
Role: Intel Scout (`docs/roles/INTEL_SCOUT.md` binding)
Mission source: `state/intel_loop.json` priority 1 (set by cycle-6 Director integration, commit 9f9a757)
Outputs: this report + `results/intel/scout/cycle7_findings.json` + `state/intel_candidate.json`

---

## 1. Mission

Assigned priority-1 mission: **clean-instrument confirmation round 3 of `unbrowse-route-capture-replay-ladder`** — the CAPPED final live attempt. With the four audited cycle-6 instrument defects repaired under a fresh preregistration disclosing every cycle-6 observation as prior knowledge, does the multi-host route-ladder measurement produce an interpretable verdict on its five open questions: (a) multi-host discovery fidelity (≥4 qualifying first-party-API sandbox hosts), (b) repeat-task economics vs matched browser traversal at output equivalence, (c) natural calendar-time staleness via the committed window-2 protocol, (d) replica-scoped induced-mutation detection quality, (e) capture-value-over-declaration vs the GENERATED_SPEC_NULL arm.

The Scout's job this cycle was NOT to rerun anything confirmatory. It was to (1) re-select exactly one mechanism for reproduction with fresh external evidence, (2) verify revisit triggers, (3) sweep for new actors/papers beyond the seed including Steam-like/shared-capability infrastructure, (4) consult cto_intel + ecosystem scout + an independent benchmark critic with deliberately independent contexts, and (5) hand the Reproducer a candidate precise enough that any residual invalidity cannot be blamed on underspecification.

## 2. Selection decision (up front)

**SELECTED (reconfirmed): `unbrowse-route-capture-replay-ladder`, measurement-validity restoration round 3**, per assignment.

- All three pre-selection consultations independently returned CONFIRM_SELECTION / "no outranking challenger" (contexts were independent; disagreement was explicitly invited; none flipped).
- Ecosystem sweep across papers, code, registries and vendor surfaces found **no actor or paper that outranks the assigned mission** on information value × feasibility this cycle. The strongest new evidence (donor panel arXiv:2608.00997 data release; MCP SEP-2549 native TTL fields; measured registry-trust incidents) *strengthens* the assigned mission's framing rather than displacing it.
- The queued non-live candidates (content-binding freshness control; Harpist contract-profile schema; trust-engine evaluation) are **downstream consumers** of this result: freshness control populates capsule fields *of a store whose viability round 3 determines*; trust-engine evaluation blocks nothing and can be fed without live collection.
- Stop-condition fallback did not fire in any form: no trigger fired (§7), no environment fact removes ≥4 qualifying hosts from the roster as last probed live ~1 day ago (cycle 6, same calendar day).

Two NEW decision-relevant facts discovered this cycle materially shape HOW the Reproducer must sequence the run (they change scheduling and one design policy, not the target):

### 2.1 NEW FACT — the natural-TTL clock gate forces a split session, not a delay

Committed evidence arithmetic (all from committed files, recomputed fresh):

- `results/intel/reproductions/cycle6/ttl_window1.json` was captured at **ts_ms 1787695530749 = 2026-08-25T22:05:30Z**.
- The committed window-2 protocol requires a **≥24h calendar gap**: earliest eligibility **2026-08-26T22:05:30Z**.
- At Scout time (2026-08-25T23:12Z) only **~1.1h** had elapsed.

Implications:
1. A single-session run executing full P0–P7 **including** window-2 per the committed protocol is **impossible today** under either anchoring option (see 2.2). Cycle 6 disclosed a single-session runner constraint at freeze time; if that constraint persists, the Reproducer MUST split sessions inside the cycle (prereg freeze + non-TTL phases now; window-2 after eligibility opens; frozen evaluator once, at the end) — or start collection only after the boundary. Waiting entirely buys nothing: with a fresh own-study anchor, ANY start time requires an internal ≥24h gap anyway.
2. The verdict itself is NOT blocked by the clock: cycle-6 prereg §13 froze "**Natural-TTL never enters the verdict**" — the mechanical §14 rule consumes only C1–C5. Window-2 execution is a mandated stop-condition deliverable ("full P0–P7 including natural-TTL window 2"), not a verdict input. So the confirmatory measurement can be frozen and executed now with window-2 completing after eligibility opens, provided cross-session continuation rules are frozen pre-outcome.
3. Process hazards introduced by the split (must be gated BEFORE freeze):
   - **Premature evaluator invocation auto-invalidates the cycle**: the frozen evaluator's own first invalidity condition is "required evidence files missing/unparseable". Running it mid-cycle "to sanity-check" burns the exactly-once invocation AND trips the CAP. Mitigation: wrapper refuses invocation until a committed manifest of ALL required evidence files (window-2 outputs included) verifies by hash; prereg states any evaluator invocation IS the invocation; all invocations logged.
   - Cross-session discontinuity: host death overnight (restful-booker free-tier herokuapp; petstore on Jetty 9.2.9/v2015), session-cookie expiry shorter than the 24h gate, state-handoff errors. Mitigations: hash-signed boundary manifests at each session end; per-window availability accounting frozen in advance; identical-across-windows untimed auth bootstrap (cycle-5/6 precedent); host-death handled by the existing host×arm eligibility matrix.
   - Clock discipline: NTP/UTC check; evaluator recomputes eligibility from artifact-stored UTC timestamps, never from wall-clock assertions.

### 2.2 NEW FACT — anchor integrity: cycle-6 window-1 records are audit-proven structurally unsound for 2 of 4 host-tasks

The committed protocol replays WINDOW-1 route records at T+24h. But the audited cycle-6 defect rows mean those records are defective BY CONSTRUCTION for two host-tasks:

- petstore: intent matcher compared method-tagged keys against bare URLs → captures never inherited intents (audit row 3; route records carry unusable addressing);
- demoblaze cart-write: content-type filter silently dropped the learnable write route (audit row 2 / observation-tier fact).

Replaying known-corrupted records inside a positive-differential STALE_TTL test would confound staleness with inherited record corruption — a manufactured-positive hazard an auditor must flag. Meanwhile httpbin FORM/COOKIE records were verified sound (30/30 structural replays OK modulo the row-4 payload instrumentation).

Options the fresh prereg MUST choose between and freeze BEFORE outcomes (this is a disclosed representation/protocol scoping decision informed by audit rows, not threshold/equivalence/exclusion retuning):

- **Option A — carry cycle-6 artifacts forward** (the loop-state assumption "executable next cycle for free"): scope TTL claims honestly to structurally sound host-tasks (effectively httpbin); treat petstore/demoblaze TTL clauses as honest clause-failures/no-events. Cheapest; but weakens clause (c) coverage to one host-family.
- **Option B — fresh own-study window-1 anchor**: capture clean fingerprints + route-store at session 1 (immediately post-freeze), replay them at session 2 (≥24h later); compare against cycle-6's `ttl_window1.json` as mandatory NON-decisional environment-drift observation. Cleanest attribution; costs a split session regardless (which 2.1 shows is forced anyway).
- **Option C — hybrid per-host anchoring**: reuse sound cycle-6 records where they exist (httpbin), re-capture unsound ones (petstore/demoblaze). Preserves committed-protocol continuity where artifacts are valid; requires per-host disclosure at freeze.

Scout recommendation: B or C, with the choice and rationale frozen verbatim in the prereg before any outcome observation. Final call belongs to the Reproducer within the stop-condition's no-retuning constraint; whichever option is chosen, positive-differential attribution must never rest on records proven defective by the cycle-6 audit.

## 3. Pre-selection consultations (independent contexts; disagreement invited)

| Consultation | Verdict | Key deltas incorporated |
|---|---|---|
| ecosystem_scout (fresh context; web/GitHub/S2 verified) | NO outranking actor exists; assigned mission confirmed | Trigger statuses all NOT FIRED (§7); commoditization set grew by ~4 small actors converging on drift-diff-as-CI-gate; donor paper shipped Zenodo panel + production fail-closed >24h freshness gate; Unbrowse citationCount=0 re-verified; vendor blog-vs-paper numeric inconsistency documented |
| cto_intel (fresh context) | CONFIRM_SELECTION; clock gate forces split-not-delay; anchor on clean records | Verified prereg §13 (natural-TTL excluded from verdict) against the frozen file; premature-evaluator-invocation hazard; window-2 rehearsal requirement; Harpist upgraded from schema-donor to strongest underestimated comparator (credential ledger w/ capture-time/expiry/validation status feeding replay validity + automated re-auth recapture — directly answers AUTH_FAIL/staleness attribution); successor-if-stopped recommendation: credential-lifecycle validation loops, then Weblica-class volatile-parameter normalization |
| intel_benchmark_critic (fresh context) | Proceed, but V1–V5 are each individually sufficient to produce a third invalid run or a misleading verdict unless fixed pre-freeze | Fix list + ambiguity flags digested in §6 and handed to Reproducer |

Disagreement check: none of the three argued for pivoting; the critic's objections are process-level (fold into gates), not selection-level. No consultation validated any other mechanism as higher-information AND feasible this cycle.

## 4. Landscape refresh (evidence-labeled)

### 4.1 Unbrowse (selected actor) — status refresh
- Repo active through v11.3.6 (v11.3.4/.5/.6 published same-day cluster 2026-08-04; npm latest 11.3.6; 748 stars / 65 forks). [CODE_VERIFIED]
- Semantic Scholar: **citationCount = 0**, citations list empty (fetched 2026-08-25) — third consecutive independent verification; no independent evaluation of the corpus bench anywhere in the scholarly graph or open web. [CODE_VERIFIED-absence]
- **NEW inconsistency datum**: vendor blog posts cite numbers that do not match the peer paper (blog: 8,240→2,289 ms mean on "M2 MacBook Pro", 67 ms cached median vs paper: 3,404→950 ms on M4 Max, best route 79 ms). Two different runs or sloppy secondary material; recorded as OFFICIAL_CLAIM-tier inconsistency. SPIDER's sandbox results must never be cited alongside either. [OFFICIAL_CLAIM]

### 4.2 Traffic→spec conversion: commoditization set GREW again
New small actors since the cycle-6 five-implementation landscape: **Specwatch** (traffic→OpenAPI 3.1 + versioned snapshots + breaking-change diff + MCP agent-session analyzer measuring wasted-call %), **Specothesis/specint** (HAR→OpenAPI+StepCI+drift.json, v1.5.0 2026-07-30), **MimicAPI** (extension capture→spec→mock server), **traffic2openapi** (multi-source IR→OpenAPI 3.0/3.1/3.2 + spec-diff). Convergence pattern: every actor now ships capture→spec→drift-diff-as-CI-gate; NONE ships auth/session lifecycle or fallback semantics beyond what Unbrowse/SPIDER already model. Reinforces cycle-6 conclusion: differentiation lives in lifecycle/auth/drift/fallback, which is exactly what round 3 measures. All CODE_VERIFIED surfaces, solo-maintained, low adoption.

### 4.3 Freshness/staleness movement (feeds queued candidate (a))
- Donor paper arXiv:2608.00997 shipped its panel + production controls: 120 obs / 88.6 days / 19,099 servers; content-binding (hash-move revalidation) + sized sweep beats drift-ranked re-audit; 51% of stale verdicts were "born stale"; naive compounding overestimates description-change 3×; production fail-closed gate REFUSES snapshots >24h old; Zenodo panel (CC-BY-4.0) + analysis code released. [PAPER_EVIDENCE + CODE_VERIFIED] — independently corroborates BOTH the hash-move+sweep design queued as next-next candidate AND the ≥24h window discipline used here.
- MCP spec SEP-2549 (final 2026-07-28): native `ttlMs` + `cacheScope` on tools/list & resource reads; `Mcp-Method` header caching. Protocol now carries freshness metadata natively. [OFFICIAL_CLAIM]
- Real-world stale-catalog incident: NousResearch hermes-agent #72560 — tool catalog stayed stale because refresh compared tool-name SETS only; fixes converge on byte-stable schemas + full-schema fingerprints. Live proof cached-procedure stores go silently stale without content binding. [INDEPENDENT_REPORT/CODE_VERIFIED]
- TrueFoundry gateway pattern (cached_tool_schema + listChanged events + sweeper fallback; notes servers declare but don't emit listChanged); Official MCP Registry `updated_since`/include_deleted/deprecated PATCH APIs. [OFFICIAL_CLAIM/CODE_VERIFIED]

### 4.4 Shared-capability ("Steam-like") trust: more measured threat data
- Zenity Labs Paperclip campaign (Black Hat 2026-08-06): typosquatted skill family uploaded clean 2026-07-05, weaponized 2026-07-11, trended through July, **1.7M aggregate installs** before takedown; explicit marketplace TOCTOU (reputation accumulated while clean, then mutated; malicious payload in secondary setup-installation.md). [INDEPENDENT_REPORT] → textbook hash-move-revalidation target class.
- Snyk audit (Feb 2026 corpus): 3,984 skills ClawHub+skills.sh; 13.4% critical; **76 confirmed malicious payloads** (labeled corpus); detectors 90–100% recall / 0% FP on curated top-100. [INDEPENDENT_REPORT]
- Unit42 (2026-06-23): persistent evasion on ClawHub post-VirusTotal/ClawScan (paste-site lures, 22MB padding, runtime affiliate injection via remotely-updated referrals.json). Pluto Security (2026-02-04): downstream aggregators (SkillsMP-class, 145K skills) kept serving malicious skills AFTER upstream takedown — cross-registry invalidation unsolved; "removal is not a security control." [INDEPENDENT_REPORT]
- Net: trust-engine evaluation (queued candidate (c)) can now be fed with labeled data (Snyk payloads + Zenodo panel + TOCTOU timeline) WITHOUT live collection.

### 4.5 Web-agent procedural memory successors (60-day cohort)
- **BASM** (arXiv:2608.22339): boundary-aware skill memory — applicability conditions, risk cues, avoidance rules, recovery notes attached per skill; documents a "Skill Imitation Trap" (+47% wrong-tool margin from unbounded skills). Strongest academic echo yet of SPIDER's escalation-vocabulary/no-silent-substitution core. [PAPER_EVIDENCE]
- **HyperSkill** (arXiv:2608.16114): hypergraph skill memory, utility-weighted pruning/merge; code released (github.com/rux001/HyperSkill). [PAPER_EVIDENCE + CODE_VERIFIED]
- **ContraMem** (arXiv:2608.22533): procedural memory from contrasting multi-model trajectories; Function/Skill Cards; >2× success on GAIA2/ARE vs no-memory. [PAPER_EVIDENCE]
- **SkillAlchemy** (arXiv:2608.23417): admission-controlled skill creation from underspecified briefs. [PAPER_EVIDENCE]
- **WebXSkill** (arXiv:2604.13318): executable skills + step-level NL guidance, URL-keyed skill graph; its related work surfaces **WALT** (Prabhu et al., 2026): reverse-engineers built-in website functionality into deterministic tools with validated input schemas — **closest academic cousin to the route ladder found to date**; add to index, watch for code. [PAPER_EVIDENCE]

None of these closes any of the five open questions (see §6.3); all are LLM-agent-harness mechanisms outside Intel-lane reproduction feasibility this cycle; recorded for the Director's index integration.

## 5. Feasibility / stop-condition assessment

NOT TRIGGERED. Host roster qualification was probed live ~1 day ago (cycle 6, same calendar day: httpbin forms/cookies, petstore UI+spec, demoblaze SPA→api.demoblaze.com incl. login endpoint, restful-booker POST /auth; reqres.in/dummyjson remain excluded by frozen robots interpretation; jsonplaceholder auxiliary-only). Nothing observed this cycle removes hosts. Environment facts that BIND the round-3 prereg as prior-knowledge disclosures: httpbin echoes transport headers into JSON bodies; demoblaze cart-write answers 200 text/html; petstore runtime diverges from published spec; restful-booker developed HTTP 418 write-protection under repeated scripted traffic (cooldown check mandated before lifecycle probes; RB excluded from TTL claims by reset cron). Re-probing remains the Reproducer's P0 job under the availability gate.

## 6. Red-team digest handed to the Reproducer (from benchmark critic; full lists in findings JSON)

### 6.1 Validity threats beyond the enumerated repairs (top items; each cheaply mitigable pre-freeze)
1. **V1 mutation smoke floor**: "smoke detects ≥1 seeded class" would pass an instrument blind on 5/6 classes (exactly cycle-6 row 5). Require smoke detection of ALL six classes (naming type-change and pagination-shape) PLUS zero-FP on a seeded benign set.
2. **V2 D-null circularity**: a spec generated from the SAME discovery HAR/pipeline as B inherits its endpoint-selection bias and labeling bugs → "D fails/slower" passes vacuously. Require separate capture session/time (and ideally recorder config) for D-HAR on spec-less hosts; D-public as distinct lane fetched at BOTH windows (tests drift-tracking, not staleness-at-birth); report B↔D endpoint-set disagreement metric as independence check.
3. **V3 STALE_TTL↔AUTH_FAIL conflation**: demo-site sessions typically expire ≪24h; at T+24h replay legitimately dies of auth while re-discovery re-authenticates → "staleness" silently measures session lifetime. Prereg a replay-failure triage tree: auth-refresh-only retry (same template, fresh credentials) succeeds → AUTH_REFRESH_OK (auth-bound); shape still differs → SCHEMA_STALE (route-bound); scope wording to "frozen-auth artifact validity".
4. **V4 proof-pass gaming/perturbation**: smoke cells may not equal scored cells (easy GETs vs demoblaze POST-with-session), same-day smoke validates only the happy path, and proof-pass traffic itself perturbs targets (restful-booker's 418 arose under repeated scripted traffic). Bind smoke matrix to committed scored-manifest IDs; cooldown + per-host probe-volume log after proof-pass; disclose smoke cannot exercise the ≥24h path.
5. **V5 unfrozen statistics levers**: escalation-cell charging (bill escalations at measured same-task A-cost, never censor), estimator choice (median/trimmed, winsorization — means are fragile on shared demo infra), mixed-model formula, blocked-randomization schedule: ALL frozen before evaluator freeze.
6. Also: demoblaze shared-DB contamination controls (unique per-arm identities/markers, shape-only oracle on shared resources, randomized arm order, canary cross-detection); fingerprint canonicalization spec + stability pre-check (two samples hours apart must match — config.json ETags churn benignly); quiescence-wait constants hashed + settle times logged + A-latency reported ± waits; per host×arm×window availability ledger + whole-host drop rule + explicit survivor-set recalculation for the "≥half hosts CI>1" clause; adjudication-cap pre-counting from cycle-6 rates (new echo-envelope/text-html policies concentrate ambiguity exactly where invented); benign-FPR corpus enlarged with joint n/threshold/power commitment (at n≈25 the Wilson bound degenerates to demanding zero FPs); per-call-site manifest-delta assertions → INVALID_CELL on zero delta (recorder-attach regression class); evaluator-invocation logging; NTP/UTC bookkeeping; window-regress cap (one fingerprint-triggered restart per host, further changes → explicit TTL_INCONCLUSIVE host label, not run-invalid).

### 6.2 Baseline fairness
- D as specified is UNSOUND if it shares pipeline/session with B (see V2) — fix is structural, not statistical.
- C stays the right ceiling null but verdict language must amortize its doc-acquisition cost over the same horizon as B's discovery cost (break-even repeat count preregistered).
- A is fair only with wait-constant disclosure (fixed conservative quiescence waits systematically over-cost traversal).
- Cheap additive arms reviewers will demand: naive HAR byte-replay (curl-verbatim, isolates recording vs parameterization value) and B-no-cache (rediscover every run; isolates persistence value). Both nearly free; recommended additions (additive baselines strengthen, they do not retune).
- Stagehand ActCache-style action-granularity cache: minimum treatment = documented exclusion justification (DOM-drift vs schema-drift failure surface), citable from Browserbase's own docs.

### 6.3 Prior art vs the five open questions
No public work closes any of them. Closest encroachments: Q4 partially encroached by PreAct's store-gate ablation, ActionEngine's amortization (95% success / 11.8× cost cut, WebArena Reddit family) and Unbrowse's own speedup claims; Q2 methodology borrowed from the MCP registry panel (89-day decay curves; compounding overestimates 3×; born-stale instrument lag) — description-text surface only, explicitly NOT live API behavior. SPIDER's distinctive contributions remain: the generated-spec null (absent even from the source paper), sealed-schedule mutation FPR science, and write-flow replay — PROVIDED V1–V3 are fixed, otherwise those contributions are manufactured by construction.

## 7. Revisit-trigger board (checked 2026-08-25)

| Trigger | Status | Evidence |
|---|---|---|
| SkillMigrator (arXiv:2606.17645) code release | NOT FIRED (cycles 5,6,7) | GitHub search 0 repos; paper HTML has no code link; author CV files it as non-refereed preprint |
| NeoCognition public paper/code/spec | NOT FIRED (cycles 6,7) | Aug 2026 reporting confirms no product publicly available, approach undisclosed |
| APISensor (arXiv:2603.23852) code | NOT FIRED (cycles 6,7) | No own-repo link in paper HTML; GitHub search returns unrelated projects |
| MorphNet maturity | NOT FIRED (worse) | 0 stars/forks/issues, 1 contributor, last push 2026-05-24, zero releases |
| QCR (arXiv:2608.12847) follow-ups | NOT FIRED (12 days old) | S2 citationCount=0, v1 only, summarizer coverage only |
| WebNavigator third-party use | PARTIALLY FIRED (unchanged) | HF graphs/embeddings released (Apache-2.0) but 27 downloads / 1 like; repo dormant since 2026-04-07 |
| Unbrowse corpus-bench third-party eval | NOT FIRED; numeric-inconsistency datum added | citationCount=0 (3rd verification); no independent bench re-run; blog≠paper numbers documented |
| NEW WALT (via WebXSkill related work) | WATCH (new) | Reverse-engineering websites into deterministic tools w/ validated schemas — watch for code release |

## 8. Handoff summary to the Intel Reproducer

The candidate (`state/intel_candidate.json`) carries the complete constraint set. Non-negotiables from the stop condition, restated with this cycle's additions:

1. Fresh preregistration disclosing EVERY cycle-6 observation as prior knowledge; §14 decision-rule structure identical; no threshold/equivalence-mode/exclusion retuning beyond the disclosed representation-policy repairs (echo-envelope detector policy; non-JSON-labeled successful-writes filter policy).
2. Mechanical instrumentation proof-pass BEFORE freeze, EXTENDED this cycle: recorder manifests non-empty per browser host-task; ≥1 route learned per qualifying host-task; smoke replay REPLAY_OK with payload_ok=true; **mutation smoke detecting all six seeded classes + zero-FP benign set**; selftest green; golden fixtures from cycle-6 corpora (rb_auth type-name sketch, demoblaze text/html body, method-tagged intent key, parsed-body propagation); **mechanical window-2 rehearsal on local replicas** (short-gap capture→replay OK; induced fingerprint mutation fires positive-differential logic; unchanged control produces no false STALE_TTL); fingerprint stability pre-check. All marked NON-EVIDENCE; probe-volume logged; RB cooldown respected.
3. Freeze pre-outcome: anchor policy (Option A/B/C from §2.2, disclosed with rationale); triage tree (AUTH_REFRESH_OK vs SCHEMA_STALE) and its interaction with pass-code definitions in C-clauses; statistics freezing (escalation charging, estimator, model formula, blocked randomization); D-independence protocol; availability ledger + drop rules; evaluator-invocation guard (manifest-gated, logged, exactly-once); NTP/UTC bookkeeping; window-regress cap.
4. Sequencing: session 1 = proof-pass → freeze → P0–P6 (+ own window-1 capture if Option B/C chosen, committed immediately post-P1 to maximize margin above the 24h line) ; clock-wait under fence discipline (zero edits to frozen repro tree); session 2 ≥24h post-anchor = availability re-probe (hash-identical probe code) → window-2 per committed protocol → evaluator exactly once. If the runner cannot span sessions, start collection only after eligibility opens and keep everything else identical.
5. Restful-booker cooldown check before relying on lifecycle probes; RB stays excluded from TTL claims.
6. Verdict integrates normally per §14 mapping; second consecutive instrument-invalid round STOPS live collection on this mechanism (bounded single-host-PoC wording becomes final lane memory; fallback to queued candidates per directives/INTEL.md item 2).

## 9. Queued candidates update (Director-integration inputs, no routing performed)

- **content-binding-freshness-control** (queued EXPERIMENT): strengthened — donor panel data + production fail-closed >24h gate now public (Zenodo, CC-BY-4.0); hermes-agent incident supplies a live negative exemplar; MCP ttlMs/cacheScope gives a protocol-native comparator. Add Paperclip TOCTOU timeline + Snyk labeled corpus to the threat-data set.
- **harpist-versioned-contract-profiles** (WATCH): upgraded relevance — credential ledger (capture-time/expiry/validation status feeding replay validity) + automated re-auth recapture is a shipping answer to the exact AUTH_FAIL/staleness-attribution problem round 3 will fight; candidate successor mechanism if the ladder line stops (per cto_intel), ahead of Weblica-class volatile-parameter normalization.
- **trust-engine evaluation** (queued): now feedable entirely from labeled non-live data (Snyk 76 payloads; 2608.00997 panel; TOCTOU timeline; Unfragile Census aliveness stats).
- New index candidates for Director integration: Specwatch, Specothesis/specint, MimicAPI, traffic2openapi, BASM, HyperSkill (code released), ContraMem, SkillAlchemy, WebXSkill/WALT, Merlonix drift detector, TrueFoundry gateway pattern, hermes-agent incident, Zenity/Snyk/Unit42/Pluto trust reports, MCP SEP-2549.

## 10. Honest limits of this Scout cycle

- Cycle 6 ran earlier the SAME calendar day; the "refresh" therefore spans hours, not weeks — absence of newer events is weak evidence of absence.
- Semantic Scholar was reachable this cycle (citationCount=0 freshly verified for 2604.00694 and 2608.12847); SkillMigrator/APISensor counts remain UNKNOWN (rate-limit class), covered instead by direct GitHub/arXiv absence checks.
- Unbrowse-bench repo contents not inspected (existence inferred from paper reference; unchanged from cycle-6 posture).
- Feasibility probing was NOT repeated this cycle (last live probes <24h old, same-day as cycle 6); P0 re-probing remains the Reproducer's job under the availability gate.
- All design recommendations in §8 are Scout-handoff constraints/recommendations; the Reproducer owns the prereg text and the Director owns integration.

## 11. Primary sources (selection)

- Committed evidence: `state/intel_loop.json`; `docs/INTEL_LEDGER.md` (cycles 1/5/6); `intel/prereg/cycle6_unbrowse_ladder_multihost_prereg.md` §§13–14; `results/intel/reproductions/cycle6/ttl_window1.json` + `ttl_window2_protocol.json`; `results/intel/reproductions/cycle6/discovery/*_routes.json`; `reports/intel/reproductions/cycle6_report.md` (defect rows 3/4/5/7); `results/intel/VALIDATED_MECHANISMS.json`.
- Selected mechanism: https://arxiv.org/abs/2604.00694 ; https://github.com/unbrowse-ai/unbrowse ; npm registry dist-tag latest 11.3.6.
- Freshness donors: https://arxiv.org/abs/2608.00997 (panel + production gate); MCP blog 2026-07-28 (SEP-2549 ttlMs/cacheScope); github.com/nousresearch hermes-agent issue #72560.
- Trust data: Zenity labs.zenity.io Paperclip writeup (2026-08-06); Snyk skill-marketplace audit; Unit42 2026-06-23; Pluto Security 2026-02-04.
- Commoditization growth: github.com/rajeevramani/specwatch ; github.com/Rajat-Dandoti/specothesis ; github.com/Quaser001/mimicapi ; github.com/grokify/traffic2openapi.
- Adjacent memory systems: arXiv:2608.22339 (BASM), 2608.16114 (HyperSkill + code), 2608.22533 (ContraMem), 2608.23417 (SkillAlchemy), 2604.13318 (WebXSkill/WALT pointer).
- Comparators: PreAct arXiv:2606.17929 ; ActionEngine arXiv:2602.20502 ; Activity Frames arXiv:2608.05784 ; TabAPI github.com/Lay4U/tabapi ; Harpist github.com/kenobi-ai/harpist.

— Intel Scout, cycle 7, 2026-08-25
