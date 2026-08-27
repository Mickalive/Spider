# SPIDER RUNTIME LEDGER

Status: accepted-state record for `lab/runtime`.
Updated: 2026-08-27 by RUNTIME DIRECTOR after independent audit **PASS**
(repair round 1, three required fixes resolved) of cycle R2-3 (GitHub run
33109369710, audited tip `3506103`). R2-3's D1 substrate-deciding probe
is accepted at its frozen ceiling: **FLOOR_DOMINATES with a FED
discriminator — bare HTTP reached verified success in 1 wire transaction
(≤ B_AUTH=6, steps counted after the entry GET) on all three budgeted
cells (valid credentials → token), AND the wrong-input negative control
verifiably FAILED under the pinned failure witness (HTTP 200 JSON body
{"reason":"Bad credentials"}).** Program R2 CLOSES via branch (b) with TWO
decidable dominating cell classes (pagination R2-2 + auth-lifecycle R2-3).
X31: mechanism-floor killer (ii) DISCHARGED for TWO cell classes; killer
(i) stands UNDISCHARGED — compression phrasing still banned everywhere
else. R1 remains COMPLETE via the kill branch. See sections below in
reverse chronological order; earlier sections preserved unchanged beneath.

## R2 CYCLE 3 — D1 Substrate-Deciding Probe (AUDITED_DURABLE)

**Integration provenance (2026-08-27):**
- Cycle chain: team run (GitHub run 33109369710, audit harness label
  'Runtime cycle 12') over accepted base `548709d` (R2-2 accepted);
  feasibility pre-freeze (6 live requests, all receipts persisted) →
  blinding preflight clean → 3 budgeted cells + 3 negative controls →
  gate analysis → FLOOR_DOMINATES. Repair round 1 resolved RF1 (run-id
  reconciliation), RF2 (verifier-cost bundle reword), RF3 (failure-witness
  class wording); no new required fixes. Audit tip `3506103` (team-attempt-1).
- Team work is additive: new files only (floor_auth.py, gates_r23.py,
  r2_cycle3.py, test_floor_auth.py, R2_CYCLE3_PREREG.md, R2_CYCLE3_REPORT.md
  + results artifacts). No accepted file modified.
- Independent audit committed verbatim by Director:
  `results/audit/CYCLE_33111123019_RUNTIME_GATE.json` (sha256
  `b8b85d80…` — verify against file) +
  `reports/audit/CYCLE_33111123019_RUNTIME.md`.
- Tests re-run at integration: **264/264 pass** (pytest, Python 3.12.3) —
  240 existing + 24 new auth tests. Auditor did not independently rerun
  tests (mount-mutation avoidance); team report taken as reported; test
  substance inspected by auditor (non-vacuous).
- Outcome artifacts byte-untouched after generation.
- CTO-9 handoff committed for W-7 verifiability:
  `reports/runtime/provenance/CTO_TO_RUNTIME_CTO9.snapshot.md`.

**Inputs consumed (evidence tiers preserved):**
- R2-2 accepted lane state (lab/runtime at `548709d`)
- CTO-9 handoff (supersedes CTO-8) — RP1 identified as highest-leverage
  post-R2 program; /v1 negotiation opens jointly on three primitives
- Intel restful-booker environment facts (UI removed, API public, 418
  write-path protection, published demo credentials)
- R2-3 frozen prereg (`reports/runtime/R2_CYCLE3_PREREG.md`, sha256
  `64e705a4…` — auditor-recomputed and matched)

**Accepted results (exact prereg/audit ceilings — never strengthen):**

| # | Result | Audit status |
|---|---|---|
| D1 | D1 AUTH-LIFECYCLE FLOOR EXECUTED LIVE (stdlib only, zero browser launches, zero provider calls): budgeted cells AUTH-V1/AUTH-V2/AUTH-V3 each judge_success in 1 wire transaction after the entry GET (≤ B_AUTH=6 anatomy-derived; true marginal wire cost per cell = 2 transactions incl. entry — qualifier BINDS on every external quotation); wrong-input control AUTH-NEG-WP (wrong password) judged **fail** via pinned failure witness (HTTP 200 JSON body {"reason":"Bad credentials"}; well-formed-fail=true); two additional wrong-input arms (wrong username, empty body) also judge fail — all three negative-control bodies byte-identical (corroboration at request-arm level only, not distinct witness classes) → gate **FLOOR_DOMINATES**, discriminator **FED not voided**. | SURVIVES_AUDIT |
| SUB-D1 | Substrate decision: **FLOOR_DOMINATES on D1 auth-lifecycle cell class**. Witnessed-effect addressing POC **NOT_TRIGGERED** (gated on FLOOR_FAILS cells; none occurred). Program R2 CLOSES via branch (b) with TWO decidable dominating cell classes (pagination + auth-lifecycle). Login-class coverage of any branch-(b) wording stays VOID-CAVEATED (R2-1). | SURVIVES_AUDIT |
| FLIP | Route-tier HTTP-executor flip-condition evidence collected as BYPRODUCT of scored cells: POST /auth with different credentials produces token vs rejection (parameterization-to-new-ids under lifecycle shift). Measurement only; executor still refused. Never grounds for extending R2 per CTO-9. | SURVIVES_AUDIT |
| VB | Verifier-cost measurement bundle: DEFINED for this cycle but NOT executed (no microbench artifact produced; no capsule cost_class or latency_ms field populated). Native perf_counter timing + offline microbench (≥1k invocations) carried to next cycle. Instrument tier; no schema change. | SURVIVES_AUDIT_WITH_LIMITS |

**Negative knowledge (scoped, first-class):**
- restful-booker's auth endpoint IS credential-discriminating (opposite
  of the quotes-login void): the environment CAN distinguish valid from
  invalid credentials on this surface
- Discriminability is a server-behavior property (R2-1 lesson confirmed)
- Published demo credentials required; arbitrary discovery NOT tested
- Write-path 418 protection persists but irrelevant to auth endpoint
- Auth endpoint is stateless (no session bleed between cells)

**Program R2 closure:**
R2 CLOSES via branch (b) with TWO decidable cell classes. Succession
requires explicit CTO decision per GO-matrix SUNSET clause. Full
carried-obligation register in state/runtime_loop.json next_program block.

**Audit warnings W-AUD-1…W-AUD-7 — Director disposition:**
- **W-AUD-1** Run-id provenance mismatch (assignment 33111123019 vs artifact
  33109369710) → NOTED; RF1 reconciled. Integration labels team run as
  33109369710; both ids recorded.
- **W-AUD-2** Negative-control redundancy: all three wrong-input arms
  return identical 28-byte body (sha256 `16961a62…`) → ACCEPTED; RF3
  corrected wording to request-arm level only; must not be elevated to
  distinct-witness-class strength.
- **W-AUD-3** Verifier-cost bundle DEFINED but NOT executed (no microbench,
  no cost_class, no latency_ms) → ACCEPTED; verification compute unmeasured
  (C4 lineage); must be closed before any capsule is trusted for reuse
  economics. Carried as standing obligation.
- **W-AUD-4** No intent-addressable Capability Capsule or resolver contract
  produced this cycle (substrate probe by charter) → ACCEPTED; the
  consumer-facing contract is a CTO-succession deliverable (RP1).
- **W-AUD-5** "1 wire transaction" excludes entry GET (true marginal 2/cell
  incl. entry) → ACCEPTED; qualifier BINDS on every external quotation
  (mirrors W-B5).
- **W-AUD-6** Positive evidence base is ONE distinct valid-input case
  replicated across 3 transport-repeat passes → ACCEPTED; confirmation
  passes never count toward REPLICATION/GENERALIZATION tiers (mirrors W-B4).
- **W-AUD-7** Live external API with no freshness/TTL/invalidation signal
  measured → ACCEPTED; floor verdict can silently degrade to
  CYCLE_INCONCLUSIVE on site drift. Maintenance/invalidation overhead
  disclosed as limitation.

Pre-cycle state: scaffolding only (`7669dcd`, one workflow YAML commit, zero
runtime artifacts). Lineage note: runs 32864270667 / 32875577618 /
32877702179 resubmitted an unexecuted instrument tree and were BLOCKED; run
32887030457 was a legitimate restart with a fresh frozen prereg (audit-confirmed;
no outcomes ever existed under the abandoned line — supersession record below).

## R0 CYCLE 1 — Capability Runtime Skeleton (AUDITED_DURABLE)

**Integration provenance:**
- Team snapshot `f2178e4` integrated byte-identically (`git diff` vs audited
  tree empty) in commit `88d7139` on `lab/runtime`; 42 files: runtime code,
  schemas, tests, capsules, pilot evidence, attempt provenance.
- Independent audit committed verbatim by Director:
  `results/runtime/AUDIT/CYCLE_32887030457_RUNTIME_GATE.json` +
  `reports/runtime/AUDIT/CYCLE_32887030457_RUNTIME.md`.
- CTO-4 charter committed verbatim for W7 verifiability:
  `reports/runtime/provenance/CTO_TO_RUNTIME_CTO4.snapshot.md`
  (sha256 `ac5944def50b541d439159a72cfd687babbba7ddfe7243255842a61ee7648662`,
  source origin/lab/cto via `/tmp/spider_cto/docs/CTO_TO_RUNTIME.md`).
- Tests re-run at integration: 23/23 pass (pytest, Python 3.12.3), matching
  auditor sandbox result C7.

**Inputs consumed (evidence tiers preserved):**
- Graph cycle-3 post-training store dump (AUDITED_DURABLE lineage, lab/graph
  audit-gated), committed copy sha256
  `ec5af9e146ea629fac642ec4a7b14c49b685e5c193cff345a92191b7e05e7073`.
- Product PB-001 frozen D8 cost-event envelope + predicate dialect semantics
  (consumed as contract, not forked; dual-name identity map).
- CTO-4 handoff: first-commit order, corrections (ONE executor,
  HANDOFF-TO-CALLER fallback, two-cell pilot), refuse list.

**Accepted artifacts:** cost-event pack (`directives/COST_EVENT.md` +
`spider.cost_event/v0` schema); capsule.v0/plan.v0 schemas with validators and
negative fixtures; pure-stdlib `resolve/verify/report` over a content-hashed
registry with pinned `retrieval_version` and explicit ABSTAIN; ONE executor
refusing silent execution of non-inherited segments; two CANDIDATE capsules
derived byte-reproducibly from Graph evidence
(`runtime/quotes-login-route@v1` ROUTE_FRAGMENT,
`runtime/form-login-procedure@v1` PROCEDURE); zero-provider scripted baseline;
two-cell pilot driver + frozen prereg; 176 schema-valid dual-name cost-event
rows (88 twin pairs, identity errors 0).

## Audited results (maximum defensible wording — do not strengthen)

| # | Result | Audit status |
|---|---|---|
| C1 | Exact-repeat cell: action/load PARITY (4v4, ratio 1.0), novel decisions 0v4, retrieval 0.54 ms included. NO work compression demonstrated and none may be claimed (lexically transparent task; greedy baseline already optimal). Producer withdrew its own prereg compression phrasing against producer interest. | SURVIVES_AUDIT |
| C2 | Stale/wrong-host cell: deterministic applicability FAIL with per-clause attribution → ABSTAIN before ANY browser action → valid spider.plan/v0 handoff → caller repair with ONE novel action → predicate-verified success; baseline truthfully exhausted its 60-action budget. Illustrative failure avoidance only — never a speedup ratio, never a hint-causality claim. | SURVIVES_AUDIT_WITH_LIMITS |
| C3 | All six frozen gates true under auditor recomputation; G-C1c verified manually from trail (hardcoded in driver), G-C2c degenerates to isinstance check. | TRUE_UNDER_AUDITOR_RECOMPUTATION |
| C4 | Total-overhead accounting incl. retrieval/applicability/recovery; additive null-not-zero telemetry; verification compute remains UNMEASURED and verify-stage latency_ms mislabeled → no verification-cost or absolute-latency claim permitted. | SURVIVES_WITH_LIMITS |
| C5 | Agent-facing contract without internal-ID dependence (need-sense), goal_sig/store-path/credential leakage absent; leak-freedom scoped to query-time scoring only. | VALIDATED_FOR_CURRENT_TEST_WITH_NOTES |
| C6 | Evidence-tier discipline: CANDIDATE capsules, validator-enforced VALIDATED_POC ceiling, unmeasured fields null, derivation byte-identical, model independence declared UNFALSIFIABLE. | VALIDATED_FOR_CURRENT_TEST |
| C7 | 23/23 tests green and hermetic in auditor sandbox; running tests mutates nothing committed. | SURVIVES_AUDIT |
| C8 | Attempt history preserved (attempt-1 discarded AGAINST producer interest: baseline-only defect rcr=0.0046; attempt-2 valid but telemetry-incomplete); post-hoc recomputation confined to labeled addendum; freeze ordering self-attested only (W4). | SURVIVES_AUDIT_WITH_WARNING |

Cross-model inheritance: UNFALSIFIABLE this cycle by design (one caller
implementation, zero provider calls) and stated as such everywhere.

## Negative knowledge (scoped, first-class)

- Inheritance value does NOT appear on short lexically-transparent exact
  repeats against greedy scripted baselines: replay ≈ exploration there.
  Compression must be sought where ROUTE-FINDING dominates (near-repeat,
  drift, composition).
- A deep-link `/login` entry does NOT falsify the login capsule's entry
  precondition on quotes.toscrape.com (header Login anchor persists);
  wrong-HOST arrival is the deterministic stale trigger on this site pair.
- Baseline fill-retirement key-shape mismatch causes infinite refill loops —
  never mix key shapes in action-retirement sets (attempt-1 preserved).
- Legacy 2000-byte health floor misfires on real recorded pages (/login ≈
  1855–1880 B); floor lowered to 1200 with disclosure.
- Both current capsules carry byte-identical semantic_keys AND step sequences:
  no scoring function can discriminate them; pairwise ranking at n=2 is vacuous.

## Audit limitations W1–W9 — Director disposition

- **W1 (binding)** gates hardcoded/isinstance-level → ACCEPTED. Cycle-2 gates
  must be mechanically derived from the event stream; per-action applicability
  events added at segment granularity. Encoded in `directives/RUNTIME.md`.
- **W2 (binding)** caller default target makes hint causality undemonstrated →
  ACCEPTED. Caller blinded (absent hint ⇒ UNACTIONABLE, no navigation) + A0/A1
  hint-strip ablation arm with pre-frozen causality gate. Encoded.
- **W3** verification compute unmeasured; verify latency mislabels → ACCEPTED;
  relabel + native verifier timing required before any verification/wall
  overhead wording. Encoded.
- **W4** freeze ordering not git-auditable (single commit) → ACCEPTED for
  cycle 2 (prereg committed before outcomes exist). Not retroactively fixable
  for R0-1; disclosed, stays a limitation of R0-1 wording strength.
- **W5** semantic_keys derive from step vocabulary; leak-freedom query-time
  only; ranking power untested → ACCEPTED. Wording scoped in ledger; offline
  TP/TN/near-miss probe suite with tau sweep replaces vacuous pairwise test;
  derive-time duplicate-key rule adopted.
- **W6** plans expose capsule_id + content sha256 → ACCEPTED as legitimate
  provenance; "no internal IDs" phrasing permanently scoped to need-sense.
- **W7** abandoned six-W instrument lacked supersession record; CTO-4 charter
  uncommitted → RESOLVED NOW: supersession recorded above (instrument never
  executed, zero outcomes existed under it); charter committed verbatim at
  `reports/runtime/provenance/CTO_TO_RUNTIME_CTO4.snapshot.md` (sha256
  `ac5944de…`).
- **W8** n=1/cell advisory wall-clock; BASE entry_digest unserialized →
  ACCEPTED; digest serialization required in cycle-2 harness; wall-clock stays
  advisory until replication (≥3-sample question open).
- **W9** crash-on-expectation asserts → ACCEPTED; HEALTH_TRIP-style recorded
  failed rows required wherever ABSTAIN/skip is non-deterministic.

## Known limitations / portability debts (carried)

Element-text-signature coupling to site DOM (cross-site execution claim absent
revalidation — to be made explicit + mutation-tested in cycle 2); exact-netloc
precondition matching; steps[0]-derived precondition is a marked heuristic
boundary, not a measured one; warm-process registry assumption; single-sample
wall-clock; single-effect assumption in resolve().

## Refusals honored this cycle

No registry infra beyond hashed dir; no MCP transport; no SDKs; no wire
freeze; no Pareto engine (manual dominance note only); no TTL/confidence
machinery; no delta-repair executor; no composite mechanisms; ONE executor;
ONE vendored predicate dialect; no internal fallback agent; no new cost_event
fields beyond additive-default-null; near-repeat deferred to cycle 2.

Provenance discipline: attempts 1–2 preserved (`results/runtime/pilot/attempt*/`);
post-hoc recomputations confined to labeled addendum files; no frozen document
edited after outcomes; rejected/BLOCKED lineage preserved on origin branches.

## R0 CYCLE 2 — Near-repeat kill experiment (AUDITED_DURABLE)

**Integration provenance (2026-08-26):**
- Team branch `origin/cycle/runtime/32908002333/team` == team-attempt-1 ==
  tip `613fbd4b786627214b11f6fde37c88d5ca55e94b`; mounted snapshot verified
  byte-identical by the auditor and re-verified at integration (`diff -rq`
  clean on all tracked files).
- Integrated as a **fast-forward** `9dc50ba..613fbd4` so the audited
  git-orderable freeze chain remains bit-for-bit in lane history:
  `8ed968d` harness v2 → `42eb66d` FROZEN prereg + pre-outcome probe
  evidence → `e172e16` outcomes → `613fbd4b` commit-scope disclosure.
  Recommitting would have destroyed the W4 closure the audit verified.
- Independent audit committed verbatim by Director in `9b56d25`:
  `results/audit/CYCLE_32908002333_RUNTIME_GATE.json` (sha256
  `495de4e3dc3ab7a905261268adff647909927b13defb07db2fd37e3299df2963`) +
  `reports/audit/CYCLE_32908002333_RUNTIME.md` (sha256
  `b136f7e1b94f1b9a157e42f507b505d6115724b99f610d080d1c40e977c6dc6e`).
- Tests re-run at integration: **58/58 pass** (pytest, Python 3.12) —
  matches auditor sandbox. Pre-existing shared
  `tests/test_integrity.py::PhysicsLeakageGuardTests` failure confirmed by
  the auditor as identical on untouched base; Physics-lane owner's issue,
  outside Runtime scope.
- Commit-scope disclosure honored: the environment-staged V3 control-plane
  overlay rode team commit `8ed968d` with receipt
  `reports/runtime/provenance/R0_CYCLE2_COMMIT_SCOPE_DISCLOSURE.md`
  (audit warning W-C2-4); Director commits are path-scoped.

**Inputs consumed:** R0-1 accepted lane state (registry, schemas, capsules);
Graph-lineage memory-free greedy explorer baseline (policy untouched this
cycle — diff verified additive telemetry only); frozen prereg sha256
`9d07d391…24e3e`; input store dump unchanged (sha256 `ec5af9e1…05e7073`).

**Accepted results (exact prereg/audit ceilings — never strengthen):**

| # | Result | Audit status |
|---|---|---|
| T3 | NEAR-REPEAT KILL CELL: first gate-passing work-compression OBSERVATION — SPIDER 4 actions vs BASE 11 on BOTH offset entries (/tag/love/, /page/10/), margins 7 ≥ M=2 per pass, zero novel decisions, reused == pinned steps_len == 4, entry digests distinct across entries and equal within arms. Single task, single site family, two passes; magnitude unquoted; ratios reported as numbers only; multi-task replication + ≥3-sample statistics owed. | SURVIVES_AUDIT |
| C1 | Exact-repeat PARITY replicated ×2 (4v4 actions / 3v3 loads), reused 4 novel 0 — inheritance does not beat exploration on lexically transparent repeats. | SURVIVES_AUDIT |
| C2 | Stale wrong-host replicated ×2: clause-attributed ABSTAIN → zero pre-handoff actions → valid spider.plan/v0 handoff → single-novel-action caller repair via hint.params.expected_host → RESOLVED → verified success vs truthfully recorded BASE budget exhaustion. Failure-avoidance illustration only — never a speedup. | SURVIVES_AUDIT |
| ABL | A1 five-channel hint strip → blinded caller UNACTIONABLE with ZERO actions → hint CAUSAL within THIS caller implementation (sufficiency-vs-necessity beyond it unclaimed). Closes R0-1 W2. | SURVIVES_AUDIT |
| GATES | All ten mechanical gates TRUE after the labeled POST-HOC GATE-REPAIR ADDENDUM (`results/runtime/pilot2/POST_HOC_GATE_REPAIR_ADDENDUM.json`). Auditor reproduced both wirings from the same committed stream; defect direction was against producer interest; original live analysis preserved verbatim. See W-C2-3. | SURVIVES_WITH_DISCLOSURE |
| WB | Write-back primitive: 7 content-hashed observation records (6 VERIFIED_OUTCOME + 1 HANDOFF) + 1 CANDIDATE successor (`runtime/form-login-procedure-wb@v1`) in quarantined `-wb` registry; parent registry byte-untouched; dominance rule correctly NOT fired. Candidate derivation substrate only — no ranking/confidence/applicability-boundary claim. Maintenance cost disclosed-but-unmeasured (W-C2-1). | SURVIVES_WITH_LIMITS |

Binding requirements from R0-1 (W1–W9): ALL dispositioned DONE and verified
by independent recomputation (W6/W7 carried/resolved from R0-1).

Model independence: still UNFALSIFIABLE (single scripted caller, zero
provider calls anywhere — auditor-confirmed).

## R0 COMPLETION DECLARATION

R0 "Capability Runtime Skeleton" is **COMPLETE (positive)** per its frozen
completion condition: end-to-end contract independently audited across
exact-repeat + near-repeat + stale/fallback cells, each replicated ×2, with
this PASS audit. The negative-completion branch (overhead erases gain
everywhere) did NOT occur: one compression OBSERVATION exists where
route-finding dominates. Succession to program R1 is chartered in
`directives/RUNTIME.md` and `state/runtime_loop.json`.

## Cycle-2 audit warnings W-C2-1…W-C2-6 — Director disposition

- **W-C2-1 (binding next cycle)** write-back maintenance/update cost
  promised but never measured → ACCEPTED. R1 economics work must measure
  storage/persistence/derive overhead before write-back is default-path;
  reuse_yield may not be quoted while its numerator is structurally zero
  (no wb capsule has ever been consumed by any cell).
- **W-C2-2 (binding next cycle)** wb precondition uses ENTRY-url hosts while
  effect was witnessed only on quotes host → ACCEPTED with semantics pinned
  NOW by Director: **capsule preconditions carry effect-WITNESSED hosts;
  entry-host context belongs in context_signature.** Fix must be a
  re-derived wb-v2 in the quarantined registry with provenance pointing at
  v1 — never an in-place edit of a CANDIDATE artifact.
- **W-C2-3 (binding next cycle)** repaired gate code existed only inside the
  outcomes commit → ACCEPTED. Future cycles: gate code derives witness refs
  from registry artifacts and is frozen BEFORE outcomes (team prevention
  note adopted as binding).
- **W-C2-4 (process)** V3 control-plane overlay flushed into lane branch →
  NOTED; disclosure receipt verified against git reality; Director
  integration commits are path-scoped (this integration demonstrates it).
- **W-C2-5 (binding next cycle)** brittle string-keyed `analyze()` indexing
  → ACCEPTED; regression test pin required with next harness change.
- **W-C2-6 (wording)** compression margin conditional on baseline's lexical
  inability → ACCEPTED as THE design driver of successor program R1:
  strongest-baseline resolution precedes any multi-task replication.

## Additional negative knowledge (scoped, first-class)

- Baseline competence on T3 is partly DOM-order luck (declared pre-outcome);
  the offline rank probe already showed the scorer reaches Login second on
  /page/10/ — the margin is more fragile than "4 vs 11" reads.
- Registry-level resolution only: every cell executed
  `runtime/form-login-procedure@v1` by lexical capsule_id tie-break among
  byte-twin key sets; "retrieval identified the right capsule" unsupported.
- FROZEN-SCHEMA defect: capsule.v0 additive-default-null checker rejects
  populated free-object arrays (negative_knowledge), so dominance notes ride
  manifest+description. **Director disposition:** recorded as a formal /v1
  schema candidate requiring identity-or-mapper evidence + both lanes'
  sign-off per the compatibility rule; no silent v0 change until then.
- Gate predicate_ref single-string wiring was a legitimate duality blind
  spot (task-id vs witness-ref naming of identical clause bodies) — repaired
  under the labeled addendum; ref-set semantics now tested.

Provenance discipline: freeze ordering git-auditable; prereg hash pins
recomputed by auditor; parent registry untouched; post-hoc recomputation
confined to the labeled addendum; original run-time analysis preserved.

Next high-information action: `docs/NEXT_RUNTIME.md`.

## R1 CYCLE 1 — Compression Validation & Honest Economics (AUDITED_DURABLE)

**Integration provenance (2026-08-26):**
- Cycle chain: run 32916020607 REVISE (RF-1..RF-3) → repair r1 (run
  32921019845) REVISE (RF-4..RF-5) → repair r2 (run 32924286888) **PASS**.
  Team tip `e0c6eb8` == `origin/cycle/runtime/32924286888/team` == mounted
  snapshot (clean detached HEAD; auditor full-tree diff empty).
- Integrated as a **fast-forward** `162468f..e0c6eb8` so the audited
  git-orderable freeze chain remains bit-for-bit in lane history:
  `e95e4a9` harness v3 → `1b5ae4d` FROZEN prereg (01:35:05Z, before any
  outcome existed) → `20f285e` disclosed pre-outcome blinding-fixture fix
  (01:39:50Z, zero outcomes existed) → `9ddd723` outcomes → `66468f4`
  disclosed post-persist test fix → repair r1 `93f374a`,`9e1875d` →
  repair r2 `ae9c0d1`,`e0c6eb8`.
- Independent audit committed verbatim by Director in `eed8dc3`:
  `results/audit/CYCLE_32924286888_RUNTIME_GATE.json` (sha256
  `27213f4098514624a22d71a491987ef150a0ce60ef41565cb4f8198cfc05e807`) +
  `reports/audit/CYCLE_32924286888_RUNTIME.md` (sha256
  `e974b441a454eafa2f092fd60cef7c1e3a53104139e2f8bf19b154d1da6ab06c`).
- Tests re-run at integration: **129/129 pass** (`pytest tests/runtime`,
  Python 3.12.3) — matches auditor sandbox and the state-JSON count lineage
  109→120→129.
- Outcome artifacts byte-untouched across BOTH repairs (auditor git-diff
  verified on every protected path; all seven headline artifact sha256 pins
  identical between repair rounds AND equal to current files; events-stream
  sha256 `fdefc608…26609c` matches its round-1 pin). Audited modules
  `baseline.py`/`derive.py`/`gates.py`/`pilot2.py` byte-untouched.
  No live re-run occurred during repairs (none authorized).

**Inputs consumed:** R0-2 accepted lane state (registries, capsules,
pilot2 stream read-only for golden pin + wb-v2 evidence join); frozen prereg
`reports/runtime/R1_CYCLE1_PREREG.md` @ `1b5ae4d`; Graph-lineage greedy
explorer untouched this cycle and now SUPERSEDED as standard comparator by
the surviving sweep winner `goal_href|root0`.

**Accepted results (exact audit ceilings — never strengthen):**

| # | Result | Audit status |
|---|---|---|
| K1 | B-KILLED — near-repeat compression OBSERVATION does not survive strongest frozen scripted comparator: STRONG 4 vs SPIDER 4 stream-counted browser actions on ALL FOUR counterbalanced paired passes (margin 0 < M=2), both arms harness-judged successful, zero novel SPIDER decisions, no censoring, no digest drift; single task/site family, two committed offset entries. Observation-strength scoped negative; never generalized. | SURVIVES_AUDIT |
| K2 | Offline necessary-condition bound: raw goal-token scoring places the anchor rank 3–4 on BOTH entries (never stably top-1); six variants with lexicon/href features survive permutation-stable top-1; winner `goal_href|root0` by frozen tie-break. Auditor reproduced every rank from scratch — outcome is spec-determined. Bound over TWO snapshots of ONE site family; never an offline performance claim. | SURVIVES_AUDIT_SPEC_REPRODUCED |
| K3 | W-C2-6 confirmed causally: the R0-2 "4 vs 11" margin was comparator lexical inability; root bonus actively hurts on deep entries (rank 4 vs 3). Intervention-backed diagnosis on these entries only. Inherited Graph-lineage defect recorded. | SURVIVES_AUDIT |
| E1 | Write-side overhead ≈1.8032 ms/cycle construct-once fresh-write flow (≈1.9018 incl idempotent branch); containment relations mechanically pinned after RF-1/RF-4 double-count repairs; residual hygiene⊂derive overlap 0.0776% ≤ disclosed 0.08% (conservative). Denominator-only point measurement; never a payoff claim. | SURVIVES_AUDIT_WITH_LIMITS |
| E2 | Recurring consumer tax ≈0.3839 ms/resolve (`resolve_e2e` alone); warm-index workload binding disclosed. Same limits as E1. | SURVIVES_AUDIT_WITH_LIMITS |
| E3 | reuse_yield UNDEFINED — consuming-task population structurally empty; not pending, not zero; no yield quotation anywhere. | SURVIVES_AUDIT |
| WB2 | wb-v2 derived candidate `runtime/form-login-procedure-wb@v2`: preconditions carry ONLY effect-witnessed host via preregistered evidence join + execution-witnessed step-1 affordance; entry hosts demoted to NON-GATING context_signature (mechanically pinned); v1 byte-identical; append-only index; status stays CANDIDATE. Already-authenticated-caller ABSTAIN gap disclosed open (scoped out). | SURVIVES_AUDIT_JOIN_RECOMPUTED |
| N1 | Retrieval negative controls clean: 0/7 must-ABSTAIN leakage goals × 3 registries; 0 near-miss cross-matches at n=4 capsules (tau=0.30/min_match=2 pinned). n=4 point measurement, not a scaling claim. | SURVIVES_AUDIT_RERUN_DEEP_IDENTICAL |
| F1 | plan.v0 message-code conformance fixture live: expected_host sole actionable param; unknown codes UNACTIONABLE/ERROR; blinding rule encoded; enables alternate-caller conformance, does NOT prove portability. | SURVIVES_AUDIT_LIVE_EMISSIONS_CONFORM |

Binding requirements from R0-2 (W-C2-1..W-C2-6): ALL dispositioned DONE and
verified (W-C2-1 economics denominator measured; W-C2-2 wb-v2 join;
W-C2-3 witness refs derived from registry artifacts frozen pre-outcome;
W-C2-5 analyze() golden pin; W-C2-4 path-scoped commits; W-C2-6 resolved
by K3).

Model independence: still UNFALSIFIABLE (single scripted caller, zero
provider calls anywhere — auditor-confirmed).

## R1 COMPLETION DECLARATION

R1 "Compression Validation & Honest Economics" is **COMPLETE via branch
(a)** of its directive stop rule: the compression observation was killed by
the strongest baseline and is reported as an honest scoped negative with
the offline bound as durable knowledge. The multi-task replication arm
(R1-2 compression-replication) is REFUSED: replicating a killed observation
is uninformative. The transfer trigger (≥2 tasks margin ≥ M vs STRONGEST
baseline) never fired — best result against STRONG is parity (margin 0).
The lane's current honest ceiling: the agent-facing loop works end-to-end,
but **no work-compression claim survives its strongest scripted comparator
anywhere tested by this lane**.

## Cycle R1-1 audit warnings W-R1-1…W-R1-5 — Director disposition

- **W-R1-1 (binding for future use)** economics per-cycle aggregates are
  decomposition-based point measurements assuming the observed R0-2 cycle
  rate and one construct-once fresh write → ACCEPTED. Figures stay
  denominator-only and non-gating; flow-weighted re-measurement is REQUIRED
  before default-path adoption, break-even consumption or any external
  quoting. Encoded in `directives/RUNTIME.md` refuse list.
- **W-R1-2** residual `hygiene_filter ⊂ derive_successors` overlap left at
  prescribed aggregation → ACCEPTED as conservative residual (≤0.08%,
  inflates denominator against mechanism interest). No action unless a
  future gate consumes these figures.
- **W-R1-3** immutable historical quotations retain superseded economics
  values under no-amend discipline → NOTED; correct behavior. Durable
  artifacts + provenance notes govern interpretation, not commit messages.
- **W-R1-4 (scoping)** kill verdict and offline bound scoped to ONE site
  family/date/two committed entries → ACCEPTED. Cross-site generalization
  remains forbidden in wording until ≥2 site families are actually tested;
  succession decision recorded below (Program R2).
- **W-R1-5 (method note)** stream recounting requires twin deduplication
  of dual-name rows differing only by schema field → RECORDED as standing
  audit note for all future stream analyses in this lane.

## Additional negative knowledge (scoped, first-class)

- The inheritance edge on the near-repeat cell class was comparator
  weakness: ONE generic href prior collapses the entire margin 7→0;
  affordance-lexicon OR href-prior features are individually sufficient
  for stable top-1 anchor placement on these entries; neither requires
  target-site strings.
- Legacy root-bonus self-handicaps route-finding on deep entries — recorded
  for any future reuse of that Graph-lineage explorer.
- Write-back maintenance overhead is measurable and small (~ms/cycle) but
  has NO demonstrated payoff; numerator structurally absent until a consumer
  cell exists.
- URL-construction policy arms were absent from the R1-1 frozen sweep
  (recorded for successor comparator strength). This cannot affect the
  realized kill verdict — the margin was already 0 < M — but a
  URL-construction arm could make STRONG strictly cheaper than SPIDER, so
  it is mandatory in the next comparator generation.

Known limitations carried: verification compute still unmeasured (C4
lineage); single-machine warm-cache point economics; already-authenticated-
caller ABSTAIN gap open; element-text-signature DOM coupling unchanged.

Provenance discipline: freeze ordering git-auditable end-to-end; prereg hash
pins recomputed by auditor; repairs surgically regenerated aggregates from
committed streams with fixed-point verification; superseded figures confined
to labeled provenance/disclosure contexts (grep-swept); parent registry and
v1 capsule byte-untouched.

Next high-information action: `docs/NEXT_RUNTIME.md`.

## R2 CYCLE 1 — Mechanism-Floor Null (AUDITED_DURABLE)

**Integration provenance (2026-08-26):**
- Cycle chain: run 32928419260 (team, tip `8e99234`) audited **REVISE
  round 0** (RF-1/RF-2/RF-3 + W-1..W-5; committed verbatim at `e61b989`) →
  repair r1 (run 32933579869) → **PASS**, audited tip `89ffeba` ==
  `origin/cycle/runtime/32933579869/team` == team-attempt-1 == mounted
  snapshot (clean; auditor full-tree verification).
- Team work integrated as a **fast-forward** `917bbf8..89ffeba`, preserving
  the audited git-orderable freeze chain bit-for-bit: `b4254a6` harness
  (pre-outcome) → `5dd51ab` FROZEN prereg (zero live requests) → `95aa45a`
  disclosed pre-outcome blinding-scope correction (still zero live
  requests) → `c2f0a6d` OUTCOMES (live, zero browser launches) → `8e99234`
  report at frozen ceilings → `e61b989` audit round 0 recorded →
  `09536fd`/`89ffeba` repair r1. Delta vs accepted base is insertion-only
  (18 files, +4436/−0; no accepted file modified — auditor blob-verified).
- Independent repair audit committed verbatim by Director in `d6d5342`:
  `results/audit/CYCLE_32933579869_RUNTIME_GATE.json` (sha256
  `0b62fdf0389ecb6ad6abd06d0ea9611da3971a2e25b7e60cb0a7c02e9e3762cb`) +
  `reports/audit/CYCLE_32933579869_RUNTIME.md` (sha256
  `f4ec53a34b79344f506f2c311127a01eb6b27776c6c40f00c6ac39cdb9bcf37e`).
- Tests re-run at integration: **182/182 pass** (`pytest tests/runtime`,
  pytest 9.1.1 via `/tmp/opencode/pylibs`) — matches the auditor sandbox.
  Lineage independently verified by the auditor: 160 passed on a throwaway
  clone of rejected `8e99234` → 182 at tip (+22 repair pins); base lane
  suite 129. Repo-wide integrity: single pre-existing Physics environmental
  failure, identical on untouched base — not a Runtime regression.
- Frozen outcome artifacts byte-untouched across the repair (auditor git
  blob identity + sha256): prereg `950a4ded…79a199`, URL-arms
  `0df622fb…bbbf6`, events stream `ce719500…884848`, floor results
  `debe7cef…9caba`, substrate decision `db094b05…8ee9e8d`. No live re-run
  occurred during the repair (none authorized).

**Inputs consumed:** R1 accepted state (sweep winner `goal_href|root0` as
standard comparator, byte-untouched); R1-1 prereg §3.3 verbatim design
(preserved by reference for WB); committed entry snapshots (parser-parity
oracle); frozen prereg `reports/runtime/R2_CYCLE1_PREREG.md`.

**Accepted results (exact prereg/audit ceilings — never strengthen):**

| # | Result | Audit status |
|---|---|---|
| FLR | MECHANISM-FLOOR NULL EXECUTED LIVE (stdlib cookie-jar, ZERO browser launches): cells FLR-T3P1 (/tag/love/), FLR-T3P2 (/page/10/), FLR-CONFIRM-P2 all judge_success at 3 wire transactions ≤ B_FLOOR=6 with all guards true — and the WRONG-PASSWORD negative control FLR-NEGCTRL ALSO passed verification ⇒ gate **FLOOR_VOID**: the environment accepts any credentials on this goal class; the direct-HTTP surface cannot discriminate credential validity; no substrate inference licensed in either direction. Observation-tier facts only; void-caveated. The seductive FLOOR_DOMINATES reading was refused by the pre-frozen rule. | SURVIVES_AUDIT |
| SUB | Substrate decision **NO_SUBSTRATE_DECISION_VOID** (repair-first): witnessed-effect addressing POC NOT triggered (gated on surviving cells); stop-rule branch (b) NOT invoked — the discriminator itself was voided, cell-class death did NOT occur. | SURVIVES_AUDIT |
| URLA | URL-construction comparator arm `url_construct_account_route` recorded descriptively over both committed entries (`results/runtime/probes/url_arms_r21.json`); gating NONE; R1 sweep/winner byte-untouched; blinding clean. Mandatory member of any future strongest-comparator canon. | SURVIVES_AUDIT |
| WBC | Priority 3 decided PRE-outcome in frozen prereg §3: write-back stays **QUARANTINED NON-DEFAULT, no consumer evidence owed**; verbatim R1-1 §3.3 design preserved by reference; infrastructure note OPERATIONAL_DIAGNOSTIC (no browser stack in run env). `reuse_yield` stays UNDEFINED; no economics figure quoted anywhere (W-R1-1, X31). | SURVIVES_AUDIT |

Binding notes recorded by the cycle (acted on only via directive):
1. The floor discriminator needs a goal class where wrong inputs verifiably
   FAIL; none demonstrated within the current accepted substrate.
2. Any future strongest-comparator canon must include URL-construction /
   convention arms or margins repeat the K3 lesson.
3. Retroactive scoping: ALL prior browser-side login-cell economics on this
   family measured FORM-COMPLETION, not credential-authenticated sessions
   (shared correct fills spec ⇒ sessions were real; the goal class is
   weaker than its wording assumed).

## Cycle R2-1 required-fixes disposition (round 0 → repaired → PASS)

- **RF-1** alleged zero-affordance fallback dead path → **RESOLVED as a
  FALSE-POSITIVE ROUND-0 AUDIT FINDING**: the team empirically refuted it
  (hermetic mock repro; `discover_login_url` returns convention URLs AS
  candidates on fallback, so probes seeds were non-empty; exhausted sweep =
  FLOOR_FAIL at exactly 5 convention GETs) and the auditor's independent
  reproduction CONFIRMS the refutation against both the audited snapshot
  module and the hardened module (behaviorally identical). The requested
  hardening was applied anyway: source-unified probe construction,
  fallback-seed identity pinned by assertion, full-cell regressions
  `TestZeroAffordanceFallbackCell` + divergence-pin test. Zero outcome
  effect. Round-0 report remains immutable history; this section is its
  correction of record.
- **RF-2** PREFLIGHT note truncated mid-JSON at a 900-char cap →
  **RESOLVED in-harness + provenance**: `_note_json`/`._row` now emit notes
  WHOLE with mechanical json.loads round-trip assertion;
  NOTE_SANITY_MAX=8000 raises rather than truncates; v0 schema types `note`
  as unconstrained string; `TestNoteHygiene` pins. Deterministic
  write-once generator `runtime/repair_cycle3.py` rebuilt the full 924-char
  payload into `results/runtime/r2_floor/preflight_correction_r21.json`
  under an exact-prefix transcription stop rule (byte identity over all 900
  visible chars); the defective row is PRESERVED as evidence, not rewritten.
- **RF-3** impossible hand-written `updated_utc` (05:20:00Z vs actual commit
  05:00:07Z) → **RESOLVED surgically**: disclosed hand-assembly block added
  to `results/runtime/r2_cycle1_state.json`; timestamp restamped
  mechanically at write time; ALL future lane state timestamps mechanical.

## Cycle R2-1 warnings — Director disposition

Round-0 warnings (all resolved inside the repair, auditor-verified):
- **W-1** cross-media arithmetic key annotated at definition site; key name
  unchanged so gate regeneration stays deep-equal; non-gating (single
  occurrence = definition; no consumer).
- **W-2** void_mechanism wording corrected by row-citing suffix tag; original
  preserved verbatim in `repair_round_1.original_void_mechanism_verbatim`;
  substrate_decision artifact left byte-untouched with supersession
  recorded.
- **W-3** static-parser visibility limit already disclosed; carried below.
- **W-4 (binding)** http_floor arm-value registration DEFERRED to the next
  schema-touching change per audit condition; recorded durably so it cannot
  be lost. Director: this deferral must be honored at that change.
- **W-5** audit-environment diagnostic; no repo action.

Repair-audit warnings W-A1..W-A6:
- **W-A1 (standing method lesson)** round-0 RF-1 was a false positive from
  alleging a dead path by code reading without executing it; literal fix
  prescriptions can themselves be harmful (round-0 fix text would have
  double-probed conventions ~10 GETs). ACCEPTED as standing audit-process
  note for this lane: alleged dead paths must be reproduced before being
  alleged; fix prescriptions reviewed for side effects before application.
  Encoded in `directives/RUNTIME.md`.
- **W-A2 (binding)** historical 900-char truncation pattern persists in
  accepted modules `pilot.py`/`economics.py` until their next harness touch;
  deferred-with-record acceptable ONCE, "must not be deferred twice" →
  ACCEPTED_BINDING: the whole-note emission fix is REQUIRED in the next
  harness change touching either module. Encoded in `directives/RUNTIME.md`.
- **W-A3** NOTE_SANITY_MAX raises mid-run rather than emitting corrupt
  evidence — accepted trade-off; harness rule going forward: keep payloads
  small or split rows (an oversized payload burns a live cell without a
  taxonomy verdict).
- **W-A4** freeze-chain ordering provable only up to single-machine timing —
  inherited caveat, carried unchanged.
- **W-A5** OPERATIONAL_DIAGNOSTIC (auditor-installed pytest outside tracked
  scopes) — no repo action.
- **W-A6** `runtime/repair_cycle3.py` embeds absolute pre-repair sha pins;
  `--check` fails BY DESIGN after any legitimate future mutation of the
  five pinned artifacts. Accepted as cycle-scoped tamper evidence — NOT
  living infrastructure; future --check failures after legitimate mutation
  of those artifacts are expected, not defects.

## Additional negative knowledge (scoped, first-class)

- The accepted substrate's quotes-login goal class is CREDENTIAL-NON-
  DISCRIMINATING: unusable for mechanism-floor discrimination AND for any
  future claim of an "authenticated" effect without a stronger witness.
- Discriminability is a server-behavior property, NOT derivable from
  committed DOM snapshots: the login form is maximally discriminating by
  syntax yet accepts anything behaviorally. Offline affordance enumeration
  is possible; offline discriminability classification is not.
- In-canon committed entry snapshots contain zero form-like elements; the
  canon's one POST affordance (login) is now void-proven non-discriminating
  (enumeration receipt basis for the substrate-demand escalation).
- Static HTML parsing cannot reproduce computed-style visibility (mitigated
  by must-not-fire rows + negative control + form guard; residual open).
- Convention list contained the answer route for this family — bias
  direction AGAINST inheritance, disclosed; affordance cascade fired first
  on every cell so no convention probe was ever spent live.

Known limitations carried: single site family/date/scripted implementation,
three passes + one control; verification compute still unmeasured (C4
lineage); already-authenticated-caller ABSTAIN gap open; element-text-
signature DOM coupling unchanged; model independence UNFALSIFIABLE (zero
provider calls — auditor-confirmed).

Provenance discipline: freeze ordering git-orderable end-to-end; prereg
committed before any live request; outcomes byte-preserved across the
repair; corrections confined to labeled provenance artifacts; defective
rows preserved; timestamps mechanical going forward; path-scoped commits.

Next high-information action: `docs/NEXT_RUNTIME.md`.

## R2 CYCLE 2 — Decidable In-Canon Pagination Mechanism Floor (AUDITED_DURABLE)

Status: accepted-state record for `lab/runtime`. Integrated 2026-08-26 by
RUNTIME DIRECTOR after independent audit **PASS** (repair round 0, ZERO
required fixes, warnings W-B1..W-B6 all non-blocking) of cycle R2-2
(GitHub run 32940627441, audited tip `548709d`, linear chain
`fcbeaa2 → ce70080 (demand spec) → a2bbaaa (harness+34 tests) → e0ae931
(FROZEN prereg) → 88c7418 (outcomes) → 548709d (report)`). Audit gate +
report committed verbatim at `3da63d0` (gate JSON sha256
`24f11b42…678101`, report sha256 `cafdcf6b…42b22a`). Integration rerun:
**216/216** lane tests pass (= 182 accepted lineage + 34 new hermetic);
Director independently reproduced the auditor's headline recomputation —
fresh `gate_pagination_cycle()` over the committed stream is DEEP-EQUAL to
the committed analysis block (0 key mismatches), outcome FLOOR_DOMINATES.

**Inputs consumed:** directive priority order R2-2 items 1–2; rulings
R2-2-A/R2-2-B; committed entry snapshots (parser-parity oracle); audited
R2-1 harness shape (`floor_null.py`, `parity_check` reused verbatim);
CTO-7 council handoff (advisory); Product substrate-demand spec classes;
filed escalation package `R2_SUBSTRATE_DEMAND_SPEC.md` (committed BEFORE
any live request, `ce70080`); frozen prereg `R2_CYCLE2_PREREG.md`
(sha256 `6958b7ef…f02c9e`, committed before any live request; witness
receipt written before even the authorized parity fetches).

**Accepted results (exact prereg/audit ceilings — never strengthen):**

| # | Result | Audit status |
|---|---|---|
| PG | DECIDABLE IN-CANON PAGINATION FLOOR EXECUTED LIVE (stdlib only, zero browser launches, zero provider calls): budgeted cells PG-K3F (`/tag/love/`→`/page/3/`), PG-K9B (`/page/10/`→`/page/9/`), confirmation PG-KCONF (=K3F) each judge_success in **1 wire transaction after the entry GET** (≤ B_PG=6 anatomy-derived; true marginal wire cost per cell = 2 transactions incl. entry — qualifier BINDS on every external quotation); out-of-range control PG-NEGCTL-OOR (`/page/1000/`) judged **fail** via pinned failure-witness branch 1 (HTTP 200 soft-200 render, 3051 bytes, ZERO `class="quote"` markers; full-success void-detector evaluated FIRST did not fire) ⇒ gate **FLOOR_DOMINATES**, discriminator **FED not voided**. Every scored body byte-reproduced live from the audit sandbox same-day. Observation tier, ONE site family, ONE date. Never "the pagination goal class", never "all k", never cross-site, never agents, never the Web. | SURVIVES_AUDIT |
| SUB-PG | Substrate decision: **MEASURED_IN_CANON_DOMINATION_ON_PAGINATION_CELL_CLASS**. Witnessed-effect addressing POC **NOT_TRIGGERED** (gated on FLOOR_FAILS cells; none occurred). Branch-(b) recording correctly left `NOT_RECORDED_BY_RUNNER` → recorded by the Director below. Login-class coverage of any branch-(b) wording stays VOID-CAVEATED (R2-1). | SURVIVES_AUDIT |
| SPEC | Priority-1 escalation package **FILED FIRST pre-outcome** (`reports/runtime/R2_SUBSTRATE_DEMAND_SPEC.md`, measurement-invariant by design): canon affordance enumeration receipt (57+44 anchors, zero form-like), K1 comparator parity, mechanism-floor void mechanism; hypothesized-fail candidate Classes A/B/C with exact proposed frozen lists; branch-(b) gating statement §3; loop-only productionization charter as alternative demand §4. Creates no claims; authorizes nothing by itself. Spec §1.4 ("discriminator unfedable in-canon") is **SUPERSEDED for this cell class** by the outcome — consume the package via §3 gating only; §1.4 text stands unmodified as history (no-amend discipline). | SURVIVES_AUDIT |
| X31-KILLER-II | Mechanism-floor killer (ii) status moves VOIDED → **DISCHARGED FOR THIS CELL CLASS ONLY** via the fed-control DOMINATES. Killer (i) UNDISCHARGED (K1 margin 0 stands). X31 phrasing ceiling unchanged everywhere else: no compression phrasing leaves observation tier until BOTH killers discharge on accepted evidence. | SURVIVES_AUDIT |

**Director decision — stop-rule branch (b) RECORDED (scoped):**
Measured backing accepted and recorded for THE PAGINATION CELL CLASS ONLY:
"within the enumerated in-canon pagination cells (both frozen targets plus
one confirmation pass, one site family, one date), bare HTTP reaches
harness-verified success within budget AND discriminates invalid targets
under the hard-pinned witness — so witnessed-effect inheritance has NO
measured headroom on this cell class." NOT recorded: any universal claim
("no positive class exists anywhere"), any login-class coverage (VOID),
any cross-site generalization. Program R2 does NOT close on this alone:
succession requires either a surviving positive cell (never yet measured)
or branch-(b) closure across reachable substrate — which now hinges on the
ONE remaining upstream question (decidable substrate outside the voided
canon), chartered as R2-3 under CTO-7 authority.

**Cycle R2-2 audit warnings W-B1..W-B6 — Director disposition (none
required code changes; obligations encoded where binding):**

- **W-B1 (binding-at-next-touch)** generic arm module hardcodes guard key
  `quotes_content_present` despite "NO site strings" claim; blinding scan
  genuinely clean. ACCEPTED_BINDING: rename/parameterize at the next touch
  of `runtime/floor_pagination.py`; do NOT touch the module solely for
  this. Encoded in `directives/RUNTIME.md`.
- **W-B2** seven advisory pre-freeze unscored GETs unverifiable (no
  receipts); risk contained by exhaustive pinned witness + void-first
  order + fed live control. ACCEPTED process rule: future cycles that let
  advisory probes inform design MUST persist probe receipts.
- **W-B3** demand-spec §1.4 falsified for this cell class; supersession
  tag lives in report/state (history unmodified — correct). ACCEPTED:
  escalation package consumed via spec §3 gating only; §1.4 never quoted
  as current truth. Recorded above and in directive refuse list.
- **W-B4 (binding)** PG-KCONF bodies byte-identical to PG-K3F
  (deterministic static site): the confirmation pass is a transport-repeat
  check ONLY and must NEVER be counted toward REPLICATION/GENERALIZATION
  tiers. Encoded in directive refuse list.
- **W-B5 (binding)** "1 wire transaction" excludes the entry GET (true
  marginal wire cost = 2/cell + amortized preflight); qualifier rides
  every external quotation forever; construction latency remains a 0.0
  placeholder assertable only by anatomy (`probing: none_by_construction`),
  never a quoted number. Encoded in directive refuse list.
- **W-B6** state-file E1/E2 disclosure ("applied PRE-commit while
  untracked") not cryptographically provable post-hoc; load-bearing
  outcome artifacts hash-reproduce live; edit direction honesty-improving.
  ACCEPTED process rule: commit the state file BEFORE corrective patches,
  or emit patch receipts, next time.

Standing obligations confirmed carried, NOT owed this cycle: W-A2
(whole-note emission due at next pilot.py/economics.py touch — neither
touched), W-4 (http_floor arm registration due at next schema-touching
change — none occurred).

**Additional negative knowledge (scoped, first-class):**

- The quotes pagination route at the observed out-of-range cell behaves
  as soft-200 empty render YET is effect-discriminating under the pinned
  witness: route totality ≠ non-discriminability. SAMPLED SCOPE ONLY
  (single observed k; no boundary claim).
- Decidability itself was environment luck bounded to this sample: a
  content-mirroring route would have auto-VOIDed via the success
  void-detector-first order. No decidability inference transfers to other
  routes or hosts.
- Free site-model endowment disclosed (construction templates/pager
  tokens derived offline from prior committed snapshots at zero measured
  cost): bias AGAINST inheritance — legitimate for a floor null, but
  "construction is trivially sufficient" must not generalize off
  static-canon cells whose conventions the snapshots already encode.
- A decidable floor cell CAN be run inside a static canon once the goal
  class exposes an out-of-range failure witness: the R2-1 blocker
  ("discriminator unfedable in-canon") was login-class-specific, not
  canon-wide.

Known limitations carried: single site family/date/scripted
implementation; three budgeted passes + one control; verification compute
globally UNMEASURED (accepted C4 lineage; native verify eval ~0.04–0.05 ms
descriptive on positives only); model independence UNFALSIFIABLE (zero
provider calls — auditor-confirmable from stream); freeze-chain ordering
provable up to single-machine timing (inherited caveat).

Provenance discipline: git-orderable freeze chain end-to-end (spec →
harness+tests → FROZEN prereg → outcomes → report); prereg sha pinned in
three places byte-matching today; blinding clean WITHOUT exemptions;
mechanical timestamps; path-scoped additive commits (12 files, +2865/−0,
audited modules byte-untouched); E1/E2 post-run edits disclosed with
verbatim originals preserved in-file.

Next high-information action: `docs/NEXT_RUNTIME.md` (R2-3 mission).

---

# HISTORY — R0 CYCLE 1 (integrated 2026-08-25; content below preserved as accepted)

Status: accepted-state record for `lab/runtime`.
Updated: 2026-08-25 by RUNTIME DIRECTOR after independent audit **PASS** of
cycle R0-1 (GitHub run 32887030457, audited snapshot `f2178e45`, tree `824325ab`).
