# INTEL SCOUT REPORT — CYCLE 8 (2026-08-26)

Role: Intel Scout (`docs/roles/INTEL_SCOUT.md` binding). Mission source: `state/intel_loop.json` priority 1 — **powered single-shot confirmation ROUND 4 (FINAL, once-extended CAP)** of `unbrowse-route-capture-replay-ladder`, with hard closure of the multi-host live line whatever the verdict.

Scope of this report: fresh landscape sweep (papers, code, registries, vendor surfaces, incidents), all eight revisit triggers, three independent pre-selection consultations, round-4 handoff constraints, and the exactly-one mechanism selection. Scout writes nothing outside `reports/intel/scout/`, `results/intel/scout/`, `state/intel_candidate.json`.

---

## 1. Method

1. Read binding role + constitution + V2 amendment + capsule contract + Intel directive + seed + ledgers + loop state.
2. Launched three deliberately independent consultations and invited disagreement: `cto_intel`, `ecosystem_scout`, `intel_benchmark_critic`.
3. Independently verified the highest-stakes claims first-party (WALT arXiv page; WALT GitHub API metadata; Unbrowse citation count via OpenAlex after Semantic Scholar 429 rate-limits).
4. Recomputed the mission's power arithmetic from first principles (exact binomial sign tests under both tail conventions × Holm step-down) because the critic flagged a convention mismatch.
5. Assessed the stop-condition fallback; it did NOT fire.

---

## 2. Pre-selection consultation verdicts

| Context | Verdict | Key content |
|---|---|---|
| cto_intel | **CONFIRM_SELECTION** | n=10 minimum with oversample to 12 ("n≥8" rejected: zero loss tolerance); pair-validity semantics frozen (losses ≠ exclusions); full-shape rehearsal at production volumes; five-verdict evaluator fixtures; market-grade D-acceptance via ideas-only clean-room; WALT upgraded WATCH→ACTIVE comparator; successor = merged candidates (a)+(b). |
| ecosystem_scout | **NO outranking actor** | WALT now fully public but cannot answer SPIDER's open questions; commoditization count up (~13–14); trust/aliveness facts unchanged in kind; five additive design deltas proposed (§5). |
| intel_benchmark_critic | **PROCEED_WITH_FIXES (F1–F7)** | Tail-convention mismatch found inside the mission's own arithmetic; Holm uniform-threshold misreading risk; loss-tolerance table computed; demands byte-replay arm for the causal decomposition; mechanical anti-stopping apparatus specified. |

**Disagreement check:** no consultation flipped the selection; every objection is process/statistics-level and foldable into the stop-condition's mandatory pre-freeze gates. One substantive intra-consultation disagreement (keep mission-named sign-Holm at scheduled n=12 vs switch family clause to an exact task-stratified permutation test at n=10) is recorded as a decision point: deviating from the named statistic would need Director sanction; EITHER way the numeric power proof must appear in-prereg before freeze.

---

## 3. Revisit triggers — all checked fresh this cycle

| Trigger | Status | Evidence |
|---|---|---|
| SkillMigrator code release | NOT FIRED (c5–8) | GitHub search total_count=0; unrelated namesakes only; OpenAlex cited_by_count=0 [CODE_VERIFIED-absence] |
| NeoCognition disclosure | NOT FIRED (c6–8) | research page live-fetched: bare stub; press ends at April seed; Aug 12 talk abstract only [OFFICIAL_CLAIM-absence] |
| APISensor code | NOT FIRED (c6–8) | S2 citationCount=0; unrelated repos only [CODE_VERIFIED-absence] |
| MorphNet maturity | NOT FIRED (worse) | 0★/0 forks/0 issues; last push 2026-05-24; 0 releases [CODE_VERIFIED] |
| QCR follow-ups | NOT FIRED (14d old) | S2/OpenAlex 0 citations; no code [PAPER_EVIDENCE] |
| WebNavigator third-party use | PARTIALLY FIRED (unchanged) | HF graphs/embeddings live; low adoption; dormant repo [CODE_VERIFIED] |
| Unbrowse corpus-bench third-party eval | NOT FIRED through c8 | citationCount=0 FOURTH consecutive verification — Scout re-verified first-party via OpenAlex (W7148370311, cited_by_count=0) + independent S2 fetch by ecosystem_scout after backoff [CODE_VERIFIED-absence] |
| **WALT code/paper release** | **FIRED THIS CYCLE** | See §4.1 — resolved as comparator, not outranker |

---

## 4. New evidence this cycle

### 4.1 WALT is now fully public — FIRES the cycle-7 trigger

- Paper: **arXiv:2510.01524**, "WALT: Web Agents that Learn Tools", Salesforce AI Research (submitted 2025-10-01; cited as ICLR 2026 in WebXSkill's bibliography). Scout independently fetched the abstract page.
- Code: **github.com/SalesforceAIResearch/WALT** — created 2025-10-14, MIT license, 77★ / 12 forks, pushed 2026-06-02; contains `src/walt/tools/`, pre-discovered tools, benchmark harnesses (GitHub API verified; surface-level CODE_VERIFIED).
- Mechanism: demonstrate → tool/schema induction with URL-manipulation promotion **via API reverse-engineering** → test-agent validation; deterministic URL/DOM executors with targeted agentic fallbacks; reported 52.9% VWA / 50.1% WA success, 1.3–1.4× step reduction.
- Why it does NOT outrank round 4: synthetic benchmark sites only; no shared registry; no TTL/aliveness semantics; no auth-lifecycle story; no no-silent-substitution guarantee; its baselines are induced procedures, not spec-driven clients — so it validates the deterministic-tool mechanism class and anchors related work without answering multi-host live economics or capture-vs-declaration under matched tolerance policies.
- Ledger action for Director: move WALT from "WATCH, no code located" to ACTIVE comparator (COMPETITOR_INDEX update belongs to Director integration, not Scout).

### 4.2 Commoditization grows again (~13–14 implementations)

New since cycle 7's ≥9 count:
- **snapspecter/mitmproxy-mcp** (MIT, 104★): mitmproxy-wrapping MCP with auth-pattern detection (Bearer/JWT/API-key/session-cookie/CSRF/OAuth), **session variables that lift tokens from one response and reinject them into replays**, endpoint clustering → `export_openapi_spec()`, curl-cffi TLS impersonation replay. First shipping implementation found outside Unbrowse with concrete auth-session reuse semantics.
- **Arkptz/mitm2openapi** (Rust; pushed 2026-08-24): smart parameterization — UUID/hex detection, cross-request variability, redaction.
- **protostatis/unbrowser** (distinct vendor; pushed 2026-08-23): Chrome-free discovery with explicit escalation ladder to browser-grade execution — a second independent escalation-ladder design.
- None ships TTL-with-escalation + no-silent-substitution + auth-lifecycle together. The D-split answer therefore prices SPIDER's residual value more precisely each cycle this waits.

### 4.3 Freshness/invalidation lane strengthens

- **SEP-2549 landed in the MCP spec** (2026-07-28 RC): native `ttlMs` + `cacheScope`; missing ttlMs ⇒ default 0; notification invalidates mid-TTL; TS SDK v2 caps client TTL at **24h MAX_CACHE_TTL_MS** — joining Unbrowse's ">24h stale ⇒ re-verify" policy to double-anchor the 24h route-TTL prior.
- **hermes-agent #67781 tombstone incident** (OPEN P2, 2026-07-18/20): a daily-reset-finaled session was RESURRECTED by stale-route recovery because durable end_reason promotion failed inside a swallowed try/except while the in-memory flag succeeded → 23h extra runtime, ~$12.10, 206 calls. Lesson: recovery must refuse when ANY terminal marker is present/incomplete (tombstone atomicity). Cheap guard for any replay store.
- Related hermes trail: #45966 cache split-brain; #57836 stale OAuth blocks startup; #35838 stale-while-revalidate proposal.

### 4.4 Steam-like/shared-capability layer

- New registries/marketplaces: SkillsMP (800k+ scraped skills, zero curation — INDEPENDENT_REPORT), Agensi (security-scanned SKILL.md marketplace + creator payouts + $9/mo MCP-delivery catalog tier — OFFICIAL_CLAIM), JFrog Agent Skills Registry (enterprise governance positioning — OFFICIAL_CLAIM).
- Trust facts extended: Trail of Bits bypassed ClawHub/Cisco/skills.sh static scanners in <1h (obfuscation + prompt injection; INDEPENDENT_REPORT) — static scanning is not a control; joins P-7/P-8 measured prevalence/aliveness facts.
- Credential-lifecycle cohort populating (all early-stage): vzt-browser (OS keychain vault), Leaflyst (credential graph + tamper-evident replay), agent-identity-mcp, agent-control-plane. Harpist remains the mature incumbent for queued candidate (b).

### 4.5 Procedural-memory papers indexed (not vetted)

Mem^p (arXiv:2508.06333-family, ACL 2026 Findings, code zjunlp/MemP); SkillRL/SkillBank (arXiv:2602.08234); Skill-as-Pseudocode typed contracts (arXiv:2605.27955; names SkillOps/GraSP/SkillRet/SkillsBench); prompt-cache economics prior (arXiv:2601.06007: 41–80% agentic cost reduction). QCR numbers recorded as external priors (stale-binding error 46.9%→10.9%; rebinding correctness 31.7%→77.8%; large-shift utility retention 8.2% vs 67.9%).

---

## 5. Round-4 handoff constraints (binding on the Reproducer's fresh prereg)

These fold into the stop-condition's mandatory pre-freeze gates. They are constraints and recommended additives, NOT permission to alter the frozen-rule structure beyond what the mission already authorizes.

1. **PIN THE TAIL CONVENTION (required).** The mission text mixes conventions: floor derivation "raw p ≤ 0.0125 ⇒ n ≥ 8 all-wins" holds only TWO-SIDED (n=7 two-sided = 0.015625 > 0.0125; n=8 two-sided = 0.0078125 ≤ 0.0125), while "n ≥ 10 ⇒ adjusted p = 0.0039" equals 4×2⁻¹⁰, i.e. ONE-SIDED (two-sided n=10 adjusted = 0.0078). Freeze one convention and derive n from it.
2. **HOLM IS ORDERED STEP-DOWN (required).** Uniform per-task .0125 is stricter than Holm (.0125/.016667/.025/.05) and wastes power: two-sided n=10 {10,10,9,9} passes ordered Holm but fails a uniform misreading. Spell out ordered rejection-with-stopping.
3. **LOSS-TOLERANCE TABLE IN-PREREG (required).** Two-sided exact binomial, Scout-recomputed: n=8 zero tolerance ({8,8,8,8} only); n=9 one loss ({9,9,9,8}); n=10 ≤2 losses with no task below 9/10 ({10,10,9,9}/{10,10,10,9} pass; {10,9,9,9} fails); n=11 one loss PER TASK ({10,10,10,10} passes at raw .01172); n=12 all ≥11/12 or one at 10/12. Recommended commitment: schedule 12, require ≥10 valid, print the table for the achievable valid-n range. (Permutation-test alternative requires Director sanction; mission names sign tests.)
4. **PAIR-VALIDITY SEMANTICS VERBATIM (required).** Completed-but-lost pairs (B slower OR inequivalent) are LOSSES in the sign test; only harness/host-error pairs are INVALID exclusions covered by oversampling. No post-hoc relabeling.
5. **EVALUATOR FIXTURES (required).** Five-verdict synthetic fixtures (c7 mapped three), regression-lock against archived c7 rows, producer→consumer filename-wiring audit for THIS generation (E2-class kill), frozen evaluator hash.
6. **ANTI-STOPPING MECHANICS (required).** Exact n as a NUMBER pre-committed; seeded interleaved schedule hash committed IN-TREE (fixes cycle-6 `/tmp/opencode/c6_schedule` provenance hole); append-only hash-chained execution log; predeclared invalidity taxonomy with detector code; replacement caps; pool exhausted ⇒ INCONCLUSIVE not USEFUL; optional pseudonym-salt blinding committed pre-run.
7. **D-DECOMPOSITION (required + one recommended additive).** Freeze B's tolerance policy FIRST, then define D-acceptance as matched (else circular). D-strict replicates c7 conditions; both D variants from independent dedicated captures (D-independence protocol retained). RECOMMENDED ADDITIVE (pre-freeze adoption only): naive HAR byte-replay arm completing {byte-replay, parameterized} × {strict-body, acceptance}; retain privileged bare-HTTP C as unscored reference line. Build D-acceptance MARKET-GRADE via ideas-only clean-room of strongest public methods (mitm2openapi UUID/hex detection; Browserbase browser-to-api templating), disclosed verbatim.
8. **TIMING FAIRNESS (required).** Warm-amortized timing as gated metric (both reported); identical retry/cache policies across arms; fixed repetitions-per-pair with median-of-k (closest task has only 33% headroom over the 2.0 gate).
9. **ATTRITION MATRIX (required).** Eligibility matrix + ≥2 spares screened through discovery BEFORE freeze; environment-death ≠ instrument-defect ≠ pair-loss classifiers; m=3-survivor Holm arithmetic printed in-prereg (a host death does not automatically kill the round).
10. **CONTAMINATION & DRIFT CONTROLS (required).** Per-pair unique namespaces keyed by committed seed; schema-normalized oracle (never ID/count equality); A/B interleaved minutes apart within pairs; ownership-scoped cleanup checkpoints; capture-time asset-hash fingerprints; fingerprint-diff classifier (with diff ⇒ environment-invalid excluded-and-documented; without diff ⇒ true loss); quiescence constants hashed; NTP/UTC bookkeeping.
11. **VERDICT TEMPLATE CAVEATS (required).** M4 enum-meaning-flip blindness caveat travels with any USEFUL wording even though C4 is out of the verdict; claims scoped to economics + parameterization dimensions; framed against honest external baselines (Playwright `routeFromHAR` canned-response substitution, JMeter/VuGen recorder-replay lineage, VCR/WireMock cassette-expiry analog) — never the vendor 100x headline (OFFICIAL_CLAIM forever).
12. **CHEAP ADDITIVE GUARDS (recommended).** Tombstone-atomicity refusal guard (hermes #67781 lesson); HTTP-client fingerprint logged per replay (TLS-identity confounder); optional QCR-style binding-shift covariate; optional outcome-code taxonomy alignment with vendor PASS/ANTIBOT_BLOCK/PRODUCT_FAIL/AUTH_GATED categories for external comparability (vendor figures remain OFFICIAL_CLAIM, never citable alongside SPIDER results).

**Clock gate status:** at Scout time (~2026-08-26T01:45Z) neither natural-TTL window is eligible yet (cycle-6 anchors ≥2026-08-26T22:05:30Z; cycle-7 anchors ≥2026-08-27T00:30:08Z) → split-session sequencing remains forced under either anchoring; window-2 stays deliverable-only.

---

## 6. Selection

**SELECTED (exactly one):** `unbrowse-route-capture-replay-ladder` — powered single-shot confirmation round 4 under the once-extended CAP, per `state/intel_candidate.json`. All three consultations confirmed; stop-condition fallback did NOT fire; no outranking actor exists anywhere in today's sweep. Successor pipeline after closure (whichever verdict): merged candidates (a)+(b) — lifecycle ledger driving content-binding freshness control (donor panel arXiv:2608.00997 + SEP-2549 ttlMs/cacheScope + Harpist comparators + replica-mutation harness), with candidate (c) trust-engine evaluation runnable in parallel as non-live work.

## 7. Honest limits / absences

- Semantic Scholar rate-limited Scout's direct checks (429); Unbrowse citationCount=0 verified first-party via OpenAlex instead, plus independent S2 fetch by ecosystem_scout. Fourth consecutive cycle at zero.
- arXiv listing API returned "Rate exceeded." here; late-August paper sweep ran websearch-mediated — small residual chance of a ≤2-day-old posting not yet indexed.
- WALT repo contents verified at metadata/README level (CODE_VERIFIED surface); no deep code audit performed (not needed for selection).
- Nothing new found in the last ~48h on registry-trust incidents; absence-of-evidence over 48h is weak evidence of absence.

## 8. Artifacts

- `reports/intel/scout/cycle8_scout_report.md` (this file)
- `results/intel/scout/cycle8_findings.json`
- `state/intel_candidate.json`

Scout authority limits honored: no Graph/Physics/Product/Runtime edits; no VALIDATED_MECHANISMS/ledger/index updates (Director integrates after audit); no product-validation claims.
