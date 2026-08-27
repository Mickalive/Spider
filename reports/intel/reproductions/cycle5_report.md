# INTEL REPRODUCTION REPORT — CYCLE 5, REPAIR ROUND 1

- Mechanism: `unbrowse-route-capture-replay-ladder` — Unbrowse-style three-tier execution ladder (capture → filter → extract/parameterize into pointer-only route records → local-cache replay → structured-code escalation; no-silent-substitution core).
- Scout source run: **cycle 5, GITHUB_RUN_ID 32861355080** (Scout workspace `state/intel_candidate.json`, byte-copied into this tree per audit RF-3; Scout report `reports/intel/scout/cycle5_scout_report.md`).
- External source: Unbrowse (github.com/unbrowse-ai/unbrowse; client boundary MIT; backend PRIVATE); vendor paper arXiv:2604.00694 (CC BY 4.0). Clean-room: vendor repository, paper full text and the secondary-corroboration projects were NOT fetched or viewed by the Reproducer.
- Preregistration: `intel/prereg/cycle5_unbrowse_ladder_prereg.md` — design FROZEN before any condition-level observation; frozen implementation hash table matches committed code **11/11**. Unchanged by this repair round.
- Object of repair: audit gate `results/intel/audit/CYCLE_32861355080_INTEL_GATE.json` (INTEL_AUDITOR run 32861355080, repair round 0): **REVISE / mechanism_status VALIDATED_USEFUL**, required fixes RF-1..RF-4, all documentary. This report is RF-1. The measurement was not re-run, re-tuned or altered; frozen code, data and results under `intel/experiments/unbrowse_ladder_repro/` and `results/intel/reproductions/cycle5/` are byte-identical to the audited round-0 snapshot (proof in §11).
- Verdict proposed: **REPRODUCED_USEFUL** (per the preregistered decision rule, evaluated exactly once in round 0). Claim tier ceiling: **PROOF OF CONCEPT**.

---

## 1. Mechanism identity and claim under test

The mechanism replaces repeated browser work with direct first-party-API calls via a three-tier ladder:

1. CAPTURE network traffic during real task completion;
2. FILTER responses to first-party JSON/XML candidates (content-type + origin heuristics; POST/PUT/PATCH as strong API signals);
3. EXTRACT + PARAMETERIZE endpoints into pointer-like route records (URL templates with `{param}` slots, method, required headers/auth-material association, response-shape sketch) — an index of pointers, never content;
4. RESOLVE at query time: local cache (24 h TTL) → live capture → structured HTML extraction (shared-graph vector-search tier omitted here — see §2);
5. INVALIDATE: freshness decay/TTL, lifecycle state;
6. FALLBACK RULE (safety core): stale/failed replay escalates transparently to the next tier with explicit structured codes (`REPLAY_OK / STALE_TTL / AUTH_FAIL / HTTP_ERROR / SCHEMA_MISMATCH / NO_ROUTE / PARAM_UNRESOLVED / ESCALATED_BROWSER / ESCALATED_HTML_TIER`); replay never silently substitutes for required live traversal.

Scoped claim tested here (NOT the vendor's 94-domain headline — §7):

> In SPIDER-relevant sandbox settings, a clean-room capture→extract→parameterize→replay ladder (a) discovers replayable first-party-JSON routes passively from genuine browser task completion; (b) completes repeat tasks by direct HTTP replay at materially lower wall-clock and browser-action cost than full scripted browser traversal at output equivalence; (c) honors the no-silent-substitution rule under forced staleness, authentication failure and real server-side mutation; and (d) honestly classifies server-rendered no-API targets where no qualifying route exists, falling back without silent substitution.

## 2. Faithful reproduction vs labeled SPIDER adaptations

Disposition table from prereg §2 (frozen), reproduced here for Director consumption:

| Element | Status | Detail |
|---|---|---|
| Capture traffic during task completion | FAITHFUL | Playwright Chromium response recording during scripted task passes |
| Filter heuristics | FAITHFUL (paper §2 level) | first-party origin check; content-type JSON/XML; static-asset exclusion; POST/PUT/PATCH strong signals |
| Extract + parameterize into pointer-like route records | FAITHFUL | URL-template induction, query-param capture, form-body templating, auth-header association (values kept local), top-level response-shape sketch |
| Local cache with TTL, disk-persisted | FAITHFUL | 24 h freshness honored at resolve time |
| Ladder tiers | ADAPTATION (disclosed) | shared-route-graph vector-search tier omitted (private backend); local ladder is cache → live capture → HTML extraction; ranking weights therefore untested |
| Replay as direct HTTP with parameter substitution | FAITHFUL | urllib-based; captured cookie/session material applied |
| No-silent-substitution + structured codes | FAITHFUL (code vocabulary ours) | nine-code vocabulary listed in §1 |
| Validate-before-replay precondition | ADAPTATION (design donor disclosed) | Stagehand ActCache-style freshness + parameter-resolvability check incorporated conceptually; no Stagehand source viewed |
| Scripted policies instead of LLM agents | ADAPTATION (disclosed) | no LLM exists in this environment; token cost structurally zero in ALL conditions; cost axes are wall-clock + browser actions + HTTP transactions |
| Role-3 discovery input | ADAPTATION (forced by verified environment change, prereg §8) | restful-booker's booking UI was removed from the live deployment before the cycle; its API remains public. Probe-substrate capture therefore runs over scripted direct-HTTP agent work (a sanctioned SPIDER execution mode), exercising filter/extract/auth/template mechanics but not passive-UI capture (which Role 1 covers). No A-vs-B latency claim on this substrate |
| HTML-extraction recipes for no-API targets | ADAPTATION (disclosed) | hand-authored recipes ARE the mechanism's declared final fallback tier for sites with no qualifying API route |

Clean-room statement: implemented only from the Scout mechanism description plus public sandbox-site documentation (httpbin.org's own docs; restful-booker's bundled `/apidoc`). Licensing permits this path (client MIT, paper CC BY 4.0); nothing was copied.

## 3. Frozen design snapshot

- Targets/roles (prereg §3): ROLE 1 API-tier matched-pass slice = T_BIN_FORM and T_BIN_COOKIE on httpbin.org; ROLE 2 no-API classification slice = quotes.toscrape login+extract and books.toscrape category extract; ROLE 3 restful-booker probe substrate (no latency claim).
- Conditions (Role 1 only): **A** full scripted browser traversal (`goto(load)` + `networkidle` capped at 6 s; targeted-selector extraction both arms); **B** route replay from the store built during ONE discovery pass identical to A with traffic recording; **C** bare-HTTP null using publicly documented endpoints only (knowledge-privileged by construction).
- Protocol: 1 unmeasured warmup per arm per task, then K=5 measured passes per arm interleaved A,B,…; C block afterward; ≥2 s pacing between passes OUTSIDE all timed regions; single clock `time.perf_counter()` around full task execution for all arms; server timings never enter headline numbers.
- Validity gates V1–V8 (prereg §6) incl.: no artificial waits inside timed regions (V1); matched passes/exclusions arm-blind (V3); B must demonstrably work from CAPTURED traffic alone with no doc-derived hints (V4); hashlib-only hashing (V5); no tuning after first condition-level observation (V6); independent event-log checker for fallback compliance (V7); compact manifests, ≤512-byte body samples only, pointer-only store (V8).

## 4. Results and per-clause decision-rule evaluation

Raw evidence: `passes_raw.json` (34 rows = 30 measured + 4 warmups correctly excluded per protocol; 0 other exclusions), summarized in `latency_summary.json`; discovery outcomes in `discovery_checks.json`. The auditor independently recomputed every number below from raw rows this cycle (`results/intel/audit/CYCLE_32861355080_recompute_cycle5.py`) with zero mismatches.

Clause (i) — discovery success 2/2 Role-1 tasks: **PASS.**
- T_BIN_FORM: learned `POST https://httpbin.org/post` (discovery wall 1257.5 ms); replay check REPLAY_OK, output equivalent at discovery time.
- T_BIN_COOKIE: learned `GET https://httpbin.org/cookies` (563.1 ms) with captured session-material requirement (`headers_required.cookie ← auth_material`); replay check REPLAY_OK, equivalent.

Clause (ii) — materiality on BOTH tasks: **PASS.**

| Metric | T_BIN_FORM | T_BIN_COOKIE |
|---|---|---|
| median A (browser) ms | 1218.8 | 559.7 |
| median B (replay) ms | 32.9 | 64.6 |
| speedup median (headline) | **37.05×** | **8.66×** |
| speedup mean | 17.17× | 9.66× |
| paired wins B vs A (of 5) | 5/5 | 5/5 |
| A browser actions per pass | 6,6,6,6,6 | 1,1,1,1,1 |
| B browser actions per pass | 0×5 | 0×5 |
| B payload equivalence | 5/5 | 5/5 |
| B codes | REPLAY_OK ×5 | REPLAY_OK ×5 |

All B passes ran as direct HTTP replay with zero browser launches; all 10 measured B payloads passed the acceptance predicates.

B−C gap (report-only per prereg interpretation rule): C medians 30.3 ms / 47.0 ms → C/B ratios **0.92 / 0.73**. C is knowledge-privileged by construction (public-doc recipes). Allowed reading is qualitative only: B reached parity WITHOUT privileged endpoint knowledge, and P1 shows induced templates execute correctly on unseen parameter values. NO latency advantage of replay over raw HTTP may be claimed — C is faster or equal here.

Clause (iii) — zero violation-taxonomy violations across P1–P4: **PASS** (details §6).

Clause (iv) — failure-mode taxonomy completed including Role-2 behavior, 0 exclusions vs the 20% INCONCLUSIVE threshold: **PASS** (§5).

Decision rule evaluated exactly once (round 0, `decision_rule.json`): all four clauses pass → **REPRODUCED_USEFUL**, ceiling PROOF OF CONCEPT.

## 5. Role-2 no-API tier: classification and fallback correctness (reliability datum)

This is the "report section 5" referenced by `decision_rule.json` clause 4. Both server-rendered targets produced ZERO qualifying routes (the filter correctly rejected HTML-only traffic, including the quotes login POST redirect) and the ladder escalated to the hand-authored HTML-extraction tier with provenance tagged:

- **T_BOO_CATEGORY_EXTRACT (books.toscrape)**: escalation succeeded — final code REPLAY_OK, provenance `escalated_html_tier:NO_ROUTE`, payload correct (≥1 title extracted). Browser arm completed with 2 actions; report-only html-tier wall 131.5 ms (no latency claim on this slice).
- **T_QUO_LOGIN_EXTRACT (quotes.toscrape)**: **the fallback itself FAILED in-run** — after correct `NO_ROUTE` detection and html-tier escalation (provenance `escalated_html_tier:NO_ROUTE`), the login+extract recipe ended in **SCHEMA_MISMATCH**; nothing was presented as success (`b_payload_ok: false`). Browser arm completed with 4 actions and a valid payload, so the failure is confined to the fallback recipe. This is recorded as an explicit **reliability datum**: the HTML tier can fail on schema drift/mismatch, and when it does, the system surfaces a structured code rather than substituting silently. Per the round-0 decision-rule record, the same html-tier code path succeeds in isolation outside the measured run — i.e., the in-run failure reflects recipe fragility on that flow, not a broken escalation mechanism. No code changes were made post-outcomes (V6); the fragility stands as an honest limitation.

Classification honesty: the mechanism correctly did NOT fabricate routes where none qualify — the expected-zero-routes prediction held 2/2.

## 6. Lifecycle probes P1–P4 and the structural no-substitution check

From `probe_events.json` (+ `role3_routestore.json`, `role3_traffic_manifest.json`), each verified by the independent event-stream checker:

- **P1 parameterization**: the induced `GET /booking/{id}` template replayed two NEW bookings created post-discovery (ids 3081, 3084) field-equal to direct-API ground truth — template slots are induced, not memorized.
- **P2 auth staleness**: replay with corrupted Basic credential returned structured **AUTH_FAIL** (HTTP 403) with nothing presented; positive control round-tripped a sentinel set→restore via valid credentials (REPLAY_OK, confirmed).
- **P3 TTL expiry**: rewinding freshness −48 h made resolve refuse with **STALE_TTL** (age 172800.5 s > 24 h TTL) and escalate rather than replay. Implementation-behavior probe of OUR compliance with the mechanism's own TTL rule.
- **P4 mutation consistency**: scratch booking (id 3080) deleted via direct API (201) → replay surfaced **HTTP_ERROR** → escalation confirmed absence (404) → final output carried provenance `escalated_html_tier:HTTP_ERROR`.
- **Pointer-only store**: mechanical structural check — no response bodies anywhere in the store (`routestore_snapshot.json`, `role3_routestore.json`); silent cached substitution is impossible BY DESIGN and verified.

Checker caveat (disclosed, non-blocking): the checker's `taxonomy_violations` counters are initialized to zero rather than derived by aggregation; they are cosmetic bookkeeping. Functionally the taxonomy is covered because each executed probe's check flips on its corresponding violation class (stale_silent ⇒ P3 would read REPLAY_OK; wrong_data_presented_live ⇒ success code without confirmation; missing_code ⇒ escalation without a code; unreported_substitution ⇒ fallback output without provenance tag). Disclosed in prose per RF-4/V6; no post-outcome code edits.

## 7. External vendor headline status (kept separate by design)

The vendor headline (warmed-cache 950 ms vs 3404 ms Playwright; 3.6× mean / 5.4× median across 94 domains; sub-100 ms well-cached routes) was re-verified verbatim against the arXiv:2604.00694 abstract during the round-0 audit. It remains **OFFICIAL_CLAIM**: vendor-run, untested here, carrying the Scout's prior forensic qualifications (vendor baseline included an unconditional +2 s sleep, raw-dump extraction, server-reported timing asymmetry, 1+1 passes while claiming three) and zero independently confirmable citations at audit time (Semantic Scholar returned HTTP 429; status unconfirmable, immaterial to the verdict). The sandbox numbers in §4 were obtained under the corrected forensic constraints and must NOT be cited alongside, or as support for, the vendor's breadth claims.

## 8. Disclosed non-design findings from round 0 (documentary only)

Per RF-4 none of these were fixed in code post-outcomes; they travel with the record:

1. **Role-3 intent-inheritance labeling artifact.** Only `/auth` and `/booking` had exact intent mappings at capture (`rsb.authenticate`, `rsb.list_bookings`); prefix-based inheritance then labeled ALL other learned routes — including create (`POST /booking`) and update (`PUT /booking/{id}`) — with intent `rsb.list_bookings` (visible in `role3_routestore.json`). No metric impact: P1–P4 select routes by method + template slots and Role-1 resolution uses exact intents; but it is honest evidence that naive intent assignment degrades beyond the exact-match regime — relevant to any future semantic-addressing integration.
2. **Vestigial config: `C_RECIPES["T_BIN_COOKIE"]`.** The dict entry (pointing at the cookie-SET URL) is dead configuration; the measured C path for that task is the prereg §4 recipe (GET `https://httpbin.org/cookies` over the bootstrapped jar), which is what `run_C_pass` actually executes. Behavior conforms to the frozen design; only the leftover entry misdescribes it.
3. **Cosmetic checker taxonomy counts** — see §6 caveat.

## 9. Honest caveats and limitations

- **Single-host API tier**: restful-booker's UI removal (live-verified during calibration AND re-verified by the auditor) shrank the matched-latency slice to one host (httpbin.org, two flows). This limitation travels in ALL wording.
- **Attestation-based freeze timing**: the round-0 snapshot is a single commit; git alone cannot prove prereg-before-outcome ordering. Mitigations: frozen hash table matches committed code 11/11; internal event timestamps cohere physically (~93 s across discovery → checks → 30 measured passes → probes, consistent with ≥2 s pacing); pre-collection Revisions 1–2 logged with environment-fact reasons the auditor re-verified live.
- **Scripted policies, no LLM agents**: tokens structurally zero everywhere; operational-value axes are wall-clock, browser actions, HTTP transactions. n=5 measured passes per arm per task.
- **Browser-process amortization**: launched once per arm-block per task with fresh contexts per pass (identically for discovery and A passes) — disclosed; page-level costs remain inside timers; context creation sits OUTSIDE A's timer, which if anything favors A (conservative direction).
- **C knowledge privilege** (§4): parity-without-privileged-knowledge is the only abstraction value claimable on latency; template reuse on unseen records (P1) is the second demonstrated value axis.
- **Untested mechanism components**: shared-graph ranking/drift detection, marketplace semantics, x402 economics, production/anti-bot-walled behavior, schema-drift detection under real drift-inducing mutations.
- **Quotes html-tier fragility** (§5): the fallback can fail; it failed once in-run, honestly.
- Claim ceiling **PROOF OF CONCEPT** regardless of outcome (prereg §5).

## 10. Verdict proposed and maximum defensible wording

Verdict proposed: **REPRODUCED_USEFUL** — every clause of the preregistered rule evaluated exactly once passed; measurement survived full adversarial recomputation and confounder attack in the round-0 audit (gate: VALIDATED_USEFUL).

Strongest defensible wording (verbatim equal to the binding gate text, `CYCLE_32861355080_INTEL_GATE.json.maximum_defensible_wording`):

In a preregistered clean-room reproduction on public sandbox targets (scripted policies, no LLM agents), a three-tier capture->extract->parameterize->replay route ladder learned replayable first-party-JSON routes passively during genuine scripted browser task completion on both API-tier tasks (httpbin.org form submission and cookie-state read; discovery 2/2 with output equivalence at discovery time) and completed repeat tasks by direct HTTP replay with zero browser actions at 100% output equivalence, at median wall-clock speedups of 37.05x and 8.66x vs full scripted browser traversal under a realistic network-idle load policy (10/10 interleaved paired wins, 5 measured passes per arm per task, warmups excluded, 0 exclusions). Bare HTTP with perfect public-doc knowledge ran at parity or slightly faster than replay (median C/B ratios 0.92 and 0.73), so NO latency advantage over raw HTTP may be claimed; the demonstrated value of the route abstraction is reaching parity without privileged endpoint knowledge plus parameter-template generalization to unseen records (P1: induced {id} template replayed two newly created bookings field-equal to direct-API ground truth). The no-silent-substitution core held under forced stress: corrupted-auth replay returned structured AUTH_FAIL with no output presented (positive control round-tripped), past-TTL replay refused with STALE_TTL, deleted-record replay surfaced HTTP_ERROR with escalated provenance confirming absence, and the store is structurally pointer-only (no cached response bodies). On server-rendered no-API targets the ladder correctly found zero qualifying routes and escalated to a hand-authored HTML-extraction tier (books.toscrape payload correct; on quotes.toscrape the fallback itself failed in-run with SCHEMA_MISMATCH surfaced honestly - a reliability datum, no substitution occurred). Evidence tier: PROOF OF CONCEPT. Not established: the vendor's 94-domain 950ms-vs-3404ms headline (untested here; remains OFFICIAL_CLAIM with prior forensic qualifications and zero independently confirmable citations as of audit time), any multi-host API-tier result (single-host httpbin slice after a live-verified environment change removed the planned second host's UI), shared-route-graph ranking, schema-drift detection, LLM-agent operation, token costs, or production/anti-bot-walled behavior.

Forbidden wordings (binding, from the same gate):
- GENERALIZATION language of any kind;
- citing sandbox speedups (37×/8.7×) alongside or as support for the vendor's 94-domain 3.6×/5.4× or 100× marketing claims;
- any claim that route replay beats raw HTTP calls on latency (C is faster or equal here);
- any claim that the quotes.toscrape fallback succeeded;
- "first independent evaluation" stated as fact rather than as unconfirmable-at-audit-time citation-graph status.

## 11. Repair-round provenance and integrity verification

- Scope of this round: RF-1 (this report), RF-2 (`state/intel_reproduction.json` rewritten for cycle 5 with the complete cycle-1 record preserved untouched in `historical_cycle1_record`), RF-3 (`state/intel_candidate.json` byte-replaced by the Scout cycle-5 candidate, workflow_run_id 32861355080). **RF-4 honored: zero modifications** under `intel/experiments/unbrowse_ladder_repro/` (11 files), `intel/prereg/cycle5_unbrowse_ladder_prereg.md`, and `results/intel/reproductions/cycle5*` (12 files) — all sha256-verified byte-identical to the audited round-0 snapshot `/tmp/spider_intel_old_repro`.
- Evidence manifest re-verified in this tree: `sha256sum -c results/intel/reproductions/cycle5_SHA256SUMS.txt` → 11/11 OK.
- Prereg FROZEN IMPLEMENTATION hashes recomputed vs committed code → 11/11 exact match.
- Offline selftest rerun in this tree: `python3 -m unbrowse_ladder_repro.selftest` → 25/25 PASS (no network needed).
- No Graph/Physics/Product/workflow/constitution files touched; accepted ledgers untouched; nothing integrated into `VALIDATED_MECHANISMS.json` (Director-gated).

— Intel Reproducer, repair round 1, 2026-08-25
