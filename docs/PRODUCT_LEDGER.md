# SPIDER PRODUCT LEDGER

Evidence-gated synthesis of possible products/architectures from accepted
Intel, Graph and Physics findings. Only AUDITED findings enter here.

No product construction beyond an authorized internal Product Beta is
authorized by this file. Public deployment/commercialization requires
explicit human authorization.

---

## Intake 2026-08-25 (Product session on mounted snapshots)

Sources consumed (mounted accepted snapshots):

| Lane | Item | Audit status | Product reading |
|---|---|---|---|
| Graph | G-H1 (Run 1, 2026-08-23) cumulative store, replay, entry-reset | Audited (RUN1_AUDIT_STATUS) | Validated: fragment replay eliminates novel decisions on matched routes; entry-state reset converts context mismatch into localized novelty. NOT validated: any wall-clock/cost speedup (8.5x withdrawn). |
| Graph | G-H2 (Cycle 32676576613) blind composition | Audit SAFE_TO_INTEGRATE_WITH_MANDATORY_RELABELING | Blind content-addressed retrieval + iterative replay solves unseen composed routes; cold / verbatim-nearest-replay / single-shot BFS solved 0/3. Limits: keyword channel dependency; oracle-guided stopping; baselines not "strong". |
| Graph | G-H3 (Runs 32689296167→32776369696, re-audit PASS) E1–E4 preregistered batch | Gate PASS, safe_to_integrate=true | Composed depth carried by ITERATION POLICY, not fragment representation, at tested depth. Fragment residual value = multi-step login packaging (frag 16/16 rows vs graphiter 0/8) + books-pager desc-only lexical robustness (4/4 vs 0/2). Held-out paraphrase retrieval@1 = 2/8 (weak). Expected-UNKNOWN discipline perfect. |
| Graph | G-H4 (Run 32783797303, audit PASS, required_fixes=[]) robust addressing family 1 | Gate PASS, safe_to_integrate=true | V31 (page-anchor pagination descriptor token + symmetric closed synonym canonicalization) raises held-out paraphrase retrieval@1 2/8→6/8 positives-only, 0 false accepts; 3 mechanically selected verdict-changing probes memory-solved live in both passes (6/6 rows, reused==actions); R3: login fragment residual = validated procedural ordering (frag 4/4 vs graphiter 0/4 exploration vs static edge replay 0/4, bounce pathology ~69 actions/row). BINDING LIMITS: 6/8 is a selection-on-instrument decision outcome (fresh set SPENT; third instrument required for any quantitative V31 claim); category goals UNSOLVED; two scripted demo sites, one frozen KB, scripted deterministic consumers; NO LLM-consumer/cross-model/cross-site/calibration/wall-clock claims; retrieval_ms floored at integer ms. |
| Physics | WP-003B-R2 (Cycle 32676578274, audit VALIDATED_FOR_CURRENT_TEST) | FALSIFIED | Coarse next-state structure does not transfer across sites beyond persistence + site-local 1-NN memorization. |
| Physics | WP-005 (Cycle 32689298051, audit PASS) fine-grained response transfer | FALSIFIED | Same negative at fine granularity (URL-shape T1, DOM-diff T2) under leave-one-site-out; ACTION_ONLY and NN memory are the strongest nulls. |
| Physics | WP-004 gate | BLOCKED | Committor/barrier work lacks identifiability. |
| Intel | Ledger | EMPTY | Zero reproduced+audited external mechanisms. No marketplace/sharing/trust feature may be claimed as validated. |
| Context | reports/graph_ecosystem_map.md (audit-qualified) | Survey, qualified | Nearest competitor classes: selector/action caching (Stagehand), self-healing selectors (Healenium), induced workflow memory (AWM), workflow traces (Skyvern). Differentiation is a bounded hypothesis, not a novelty claim. |

Deliberately EXCLUDED as evidence (unaudited in-flight branches observed on
the remote only): `cycle/graph/32793580374/*`, `cycle/intel/32781482957|32792931901|32796176172/*`,
`cycle/physics/32776372437|32793165981/*`. These may become evidence only
after their own audits and Director integration.

### Cross-lane synthesis constraints

1. Physics double-negative ⇒ no product feature may rely on cross-site
   prediction of environment response. The product story is purely
   cumulative operational memory + retrieval + validated procedures,
   site-local by construction. It also means the strongest honest internal
   comparator is NN/trajectory memory — a product win over a cold agent
   alone would be weak evidence.
2. G-H4 limits ⇒ the beta measures END-TO-END product outcomes (success,
   actions, calls, tokens, latency) with V31 as adopted equipment; it must
   NOT quote any V31 retrieval-transfer rate (instrument spent).
3. G-H2/G-H4 oracle-stopping caveat ⇒ the acceptance/completion signal must
   be part of the task definition given IDENTICALLY to all arms, so no arm
   enjoys an oracle the others lack.
4. Intel emptiness ⇒ the "shared capability line" stays WATCH; nothing
   marketplace-like enters the beta.
5. Cost/latency claims are unclaimed territory ⇒ beta instrumentation must
   switch to `perf_counter` granularity and count model calls/tokens
   (G-H4 hygiene note).

---

## Decisions 2026-08-25

- PH-1 "Inherited operational memory for repeat/near-repeat web tasks"
  promoted WATCH → **PRODUCT_CANDIDATE**; **Product Beta PB-001
  authorized** (`state/product_beta_request.json`). Rationale vs the five
  contract criteria:
  1. Audited important building blocks exist (store+replay+reset G-H1;
     blind retrieval G-H2; procedure packaging + V31 equipment G-H3/G-H4).
  2. Remaining critical assumptions (real LLM consumer inheritance;
     free-form-goal addressing end-to-end; material cost/latency deltas;
     containment of known failure modes) are precisely what the beta tests.
  3. Credible current-agent baselines definable cleanly: same-backbone
     ReAct-style browser agent, cold (B0); same agent + retrieved prior
     trajectories prompt-augmented (B1, AWM-class memory — mandatory per
     constitution §13); exact replay sanity arm (B2, diagnostic).
  4. Fair instrumentation specified: perf_counter timing, token/call
     accounting, byte-restored KB, evaluation write-suppression, equal
     acceptance predicate, site-health gate, seeded determinism.
  5. Falsifiable win rule written before any benchmark outcome.
- PH-2 "Shared capability infrastructure line" kept **WATCH** (Intel
  empty; internal confidence/staleness UNCALIBRATED).
- PH-3 "Predictive Web-dynamics routing" **REJECTED** (Physics
  double-FALSIFIED at both tested granularities; audited).
- PH-4 "Selector self-healing/staleness product" kept **WATCH**
  (adjacent competitor space; no audited SPIDER block yet; staleness
  calibration open G8/G9).

Next upstream dependencies (for future sessions): Graph
`graph-inheritance-scaling` (>3 distinct fragments) would extend the beta
task panel; Intel's first validated mechanism could upgrade PH-2/PH-4;
any Physics restart-design positive would reopen PH-3 narrowly.

A losing beta is an acceptable outcome and will be absorbed per the
feedback rules in the role directive.

---

## Intake 2026-08-25 (second Product session on refreshed mounted snapshots)

Session-start state anomaly, recorded for provenance: the working tree
carried an UNCOMMITTED deletion of `state/product_beta_request.json` and an
uncommitted flip of `state/product_direction.json.beta_launch` to `false`,
while HEAD (`f238e1c`) still contained the committed PB-001 authorization.
No Beta Tester/Auditor result exists anywhere that could justify a rollback.
This session therefore re-evaluated the decision from scratch against the
refreshed accepted snapshots rather than assuming either prior state.

Sources consumed (mounted accepted snapshots; mounts verified byte-identical
to `lab/graph@d41fe9b`, `lab/physics@d3afd9b`, `lab/intel@fca0acb`):

| Lane | Item | Audit status | Product reading |
|---|---|---|---|
| Graph | unchanged since first session | G-H1..G-H4 audits PASS | Addressing-robustness program COMPLETE at scope; successor program `graph-inheritance-scaling` (>3 distinct fragments) launched but NOT decided — depth ≤3 remains the product frontier. No new product signal emitted. |
| Physics | unchanged since first session | WP-003B-R2 + WP-005 FALSIFIED (audited) | PH-3 stays REJECTED. Nothing predictive enters any product arm. |
| Intel | cycle 1 INTEGRATED: `sgdr-state-grounded-dynamic-retrieval` | Gate PASS run 32800296360, VALIDATED_USEFUL, claim-tier ceiling PROOF_OF_CONCEPT, REPRODUCED_USEFUL under frozen rule | FIRST validated external mechanism. Fused task-goal + current-state-summary retrieval (lexical-hash embedder, deterministic contract-faithful summarizer, pool top-M=max(3k,20), MMR λ=0.7) retrieved executable-correct fragments strictly more often than task-text-only retrieval under paraphrased goals + shifted entry contexts (36/74 vs 25/74 hard@1; 11 wins / 0 reversals); wrong-context-summary fusion falls back to baseline level (24/74); converted into fewer novel exploration actions at equal-or-higher subgoal success in the NL-consumer regime (39 vs 42 literal; 36 vs 42 paraphrase). BINDING LIMITS travel verbatim from the gate: PoC tier only; wins only vs task-only retrieval in the NL regime (hand-authored exact signatures remain more action-efficient when they exist: 21 vs 39 novel); no login/pager improvement; lexical-hash embedder + deterministic summarizer regimes; tiny library/sites; WebArena headline numbers NOT reproduced and forbidden in any narrative. |
| Intel | infra entries P-1..P-5 (docs/INTEL_PRODUCT_INFRA.md) | Mixed tiers: P-1 Unbrowse OFFICIAL_CLAIM (vendor-run) + CODE_VERIFIED surface; P-2 OFFICIAL_CLAIM+CODE_VERIFIED; P-3 INFERENCE_HIGH; P-4 PAPER_EVIDENCE threat model | PH-2 stays WATCH but its path is now concrete: Unbrowse browser→API route-capture/replay reproduction is Intel cycle-2's selected mission; registry design constraints already evidenced (content-addressing load-bearing; contributed procedures untrusted by default). None of this may enter a beta until independently reproduced. |
| Product pipeline | Beta Architect output READY (`cycle/product/32799261473/architect`, builder `b05d8f8`) | Internal artifacts; no outcomes exist | Benchmark prereg frozen pre-outcome meets-or-exceeds the Director floor with three tightenings. MATERIAL INTAKE GAP FOUND: the architect's provenance states "Intel ledger empty" — it never saw the integrated SGDR mechanism (integration commits postdate my 02:07 synthesis, which the architect consumed). Builder has produced docs/build-plan only; WP-0 vendoring not begun; no `state/product_beta_build.json`; zero Phase-A/B rows anywhere. |

Deliberately EXCLUDED as evidence (unaudited/un-integrated branches observed
on the remote only): all `cycle/*` attempt branches other than those
integrated into the three lab branches above — including Intel cycle-2 Scout
(Unbrowse selection), Physics WP-006 carry-forward work, and Graph scaling
cycle outputs. They may become evidence only after their own audits and
Director integration.

### Updated cross-lane synthesis constraints

1. Physics double-negative stands ⇒ PH-3 stays REJECTED; no predictive feature anywhere.
2. G-H4 spent-instrument rule stands ⇒ the beta measures END-TO-END outcomes;
   no V31 quantitative retrieval-transfer rates may be quoted from it.
3. NEW — Intel gate wording constraints bind every downstream use of the SGDR
   block: no GENERALIZATION language; no unqualified "beats the incumbent";
   combined novel-action totals only with the regime caveat; no claim that
   login/pager addressing improved; no constant-dummy-text ablation citations.
4. Equal-information principle (G-H2/G-H4 oracle lesson) stands ⇒ acceptance
   predicate disclosed identically to all arms.

---

## Decisions 2026-08-25 (second session)

- **PH-1 stays PRODUCT_CANDIDATE; Product Beta PB-001 RE-AUTHORIZED as the
  single authorized beta — request revision 2**
  (`state/product_beta_request.json`). Re-evaluation against the five
  contract criteria:
  1. Audited important building blocks: YES — now STRONGER than at first
     authorization (store/replay/reset G-H1; blind retrieval G-H2; procedure
     packaging + iteration policy G-H3/G-H4; V31 equipment G-H4; PLUS the
     first audited external mechanism, SGDR fused retrieval, addressing the
     exact assumption A2 that was previously carried entirely unvalidated).
  2. Remaining critical assumptions testable by the beta: YES (LLM consumer,
     end-to-end free-form goal serving, material cost/latency deltas,
     failure-mode containment).
  3. Credible current-agent baselines definable cleanly: YES (B0 cold
     same-backbone ReAct agent; B1 trajectory-prompt memory mandatory per
     constitution §13; B2 replay sanity diagnostic).
  4. Fair instrumentation specified: YES (perf_counter, provider usage-token
     accounting, byte-restored KB, write-suppression assertions, anchored
     predicates disclosed to all arms identically, health gates, seeded
     schedule).
  5. Falsifiable win rule written before outcomes: YES (Director floor in
     the request; architect prereg freezes it verbatim plus tightenings).
- **Directed bounded pre-outcome architecture revision (v2)**: the Beta
  Architect must issue `BENCHMARK_PREREG.md` v2 BEFORE any outcome,
  changing ONE component of the SPIDER arm — candidate fragment scoring for
  free-form goals adopts the audited SGDR-style fused score
  `alpha*cos(task_goal, description) + (1-alpha)*cos(current-state summary, description)`
  (reference alpha=0.4, pool top-M=max(3k,20), greedy MMR λ=0.7, degrade to
  primitives on weak match) over the same auto-derived descriptions, with
  V31 canonicalization retained as query preprocessing/equipment and all
  UNKNOWN thresholds/discipline unchanged. Rationale: the v1 freeze rested
  on a stale premise ("Intel ledger empty") and equipped A2 with the
  known-weaker addressing channel (held-out paraphrase retrieval@1 was 2/8
  pre-V31, and V31's instrument is spent); a fair test of the product must
  give the treatment arm its best AUDITED front door while leaving baselines
  untouched. Panel tasks, anchored predicates, arms B0/B1/B2, budgets,
  metrics, win rule and scope are UNCHANGED. The deterministic
  contract-faithful summarizer (part of the validated PoC configuration) is
  used; no LLM-summarizer or neural-embedder adaptation may be introduced
  mid-beta — those remain explicitly unvalidated adaptations for later
  cycles. Clean-room discipline: vendor from `intel/experiments/sgdr_repro/`
  lineage only; never copy CC BY-SA reference source.
- **PH-2 shared-capability line stays WATCH**, path sharpened (Intel
  cycle-2 Unbrowse reproduction in flight; P-3/P-4 registry constraints
  noted). Still nothing registry-like in any beta.
- **PH-3 stays REJECTED** (no new audited physics evidence).
- **PH-4 stays WATCH** (no new staleness-calibration evidence).
- Next upstream dependencies: Graph `graph-inheritance-scaling` verdict
  would extend/cap the beta task panel for any successor version; Intel
  cycle-2 Unbrowse verdict gates any execution-ladder product feature;
  Beta Tester/Auditor result on PB-001 triggers the feedback decision.

---

## Intake 2026-08-25 (third Product session on mounted accepted snapshots)

Session-start state anomaly, recorded for provenance (same class as the
anomaly that preceded the second session): the working tree carried an
UNCOMMITTED deletion of `state/product_beta_request.json` and an uncommitted
flip of `state/product_direction.json.beta_launch` to `false`, while HEAD
(`1ecb1b8`) still contained the committed PB-001 rev-2 authorization. No
Beta Tester/Auditor result, no BENCHMARK_PREREG v2, no builder WP-0 output
and no Phase-A/B evaluation row exist anywhere in the repository or mounts.
Nothing justifies a rollback; this session re-evaluated the decision from
scratch rather than assuming either prior state.

Sources consumed and verified against the persistent claims:

| Lane | Mounted accepted state | Match to persistent claims | Product reading |
|---|---|---|---|
| Graph | G-H1..G-H4 audits PASS through Run 32783797303 (`results/audit/CYCLE_32783797303_GRAPH_GATE.json`, safe_to_integrate=true); addressing program COMPLETE; successor `graph-inheritance-scaling` preregistered, launched, NOT decided | YES | No new product signal. Depth ≤3 remains the beta frontier; depth>3 stays out of scope whether scaling holds or collapses — the pending verdict neither blocks nor alters PB-001. |
| Physics | WP-003B-R2 + WP-005 FALSIFIED (audits VALIDATED_FOR_CURRENT_TEST / PASS); WP-004 BLOCKED pending identifiability | YES | PH-3 stays REJECTED; no predictive feature enters any arm. |
| Intel | cycle-1 integrated: `sgdr-state-grounded-dynamic-retrieval` VALIDATED_USEFUL, PROOF_OF_CONCEPT ceiling, gate PASS run 32800296360; cycle-2 mission selected (Unbrowse reproduction), not decided | YES | SGDR fused retrieval remains the audited front-door block for A2; binding wording constraints travel verbatim. Unbrowse stays OFFICIAL_CLAIM vendor-run until independently reproduced — nothing registry-like enters the beta. |
| Product pipeline | no outcomes anywhere (`product_beta_audits: 0`) | YES | Re-authorization before any outcome is constitutionally clean (§19). |

Deliberately EXCLUDED as evidence: all unaudited/un-integrated in-flight
branches (Graph scaling cycle outputs, Intel cycle-2 Scout work, Physics
WP-006 carry-forward). They may become evidence only after their own audits
and Director integration.

### Decision 2026-08-25 (third session)

- **PH-1 stays PRODUCT_CANDIDATE; Product Beta PB-001 RE-AUTHORIZED as the
  single authorized beta — request revision 3**
  (`state/product_beta_request.json`). The five contract criteria were
  re-checked and all hold, with zero substantive deltas vs rev 2:
  1. Audited important building blocks: YES (unchanged set: G-H1 store/
     replay/reset; G-H2 blind retrieval + UNKNOWN discipline; G-H3/G-H4
     procedure packaging + iteration policy; V31 equipment-only; Intel
     SGDR fused addressing at PoC ceiling).
  2. Remaining critical assumptions testable by the beta: YES (A1 LLM
     consumer end-to-end; A2 end-to-end free-form-goal serving via the
     audited fused scorer; A3 savings over edge iteration AND trajectory
     memory; A4 material token/call/wall-clock deltas; A5 containment).
  3. Credible current-agent baselines cleanly definable: YES (B0 cold
     same-backbone ReAct agent; B1 AWM-class trajectory memory mandatory
     per constitution §13; B2 exact-replay sanity diagnostic).
  4. Fair instrumentation specified: YES (perf_counter, provider usage
     accounting, byte-restored KB, write-suppression, equalized anchored
     predicates disclosed to all arms, site-health gates, seeded schedule).
  5. Falsifiable win rule written before outcomes: YES (Director floor in
     the request; architect prereg must freeze it verbatim plus tightenings;
     no outcome exists yet).
- **Request bumped to rev 3 for provenance only**: revision_note documents
  the second working-tree reset and this session's independent re-verification;
  every Director-floor clause, assumption A1–A5 and the directed pre-outcome
  revision v2 are carried forward UNCHANGED.
- **PH-2 WATCH** (Intel cycle-2 Unbrowse verdict pending; nothing registry-
  like enters any beta). **PH-3 REJECTED** (no new physics evidence).
  **PH-4 WATCH** (no new staleness-calibration evidence).
- Standing next step unchanged: **BETA_ARCHITECT must commit
  `product-beta/PB-001/BENCHMARK_PREREG.md` v2 (+ amended architecture
  state) BEFORE any outcome**, implementing exactly the directed fused-scoring
  change under the frozen everything-else rule; then BETA_BUILDER proceeds
  under freeze checkpoints F1/F2. Public deployment and commercialization
  remain unauthorized without explicit human decision.

---

## Intake 2026-08-25 (fourth Product session on mounted accepted snapshots)

Session-start state anomaly, recorded for provenance (third occurrence of
the same class): the working tree carried an UNCOMMITTED deletion of
`state/product_beta_request.json` and an uncommitted flip of
`state/product_direction.json.beta_launch` to `false`, while HEAD (`4dc8820`)
still contained the committed PB-001 rev-3 authorization. No Beta
Tester/Auditor result, no BENCHMARK_PREREG v2, no builder WP-0 output and no
Phase-A/B evaluation row exist anywhere in the repository or mounts.
Nothing justifies a rollback; this session re-derived the decision from
scratch rather than assuming either prior state.

Deepened verification this session: instead of relying on persistent
claims, both audit gates were re-read directly from the mounts —
`results/audit/CYCLE_32783797303_GRAPH_GATE.json` (Graph: PASS,
safe_to_integrate=true, required_fixes=[], byte-exact recomputation of all
headline numbers incl. R2LIVE 6/6 and R3 login frag 4/4 vs graphiter 0/4 vs
edgeseq 0/4 bounce) and
`results/intel/audit/CYCLE_32800296360_INTEL_GATE.json` (Intel: PASS,
VALIDATED_USEFUL, claim-tier ceiling PROOF_OF_CONCEPT). Physics loop state
confirms the audited double falsification and program completion; Graph loop
state confirms addressing COMPLETE and `graph-inheritance-scaling` launched/
undecided; Intel loop confirms cycle-2 (Unbrowse reproduction) selected but
not decided. No new product signals exist beyond CYCLE_32783797303
(Graph) and CYCLE_32800296360 (Intel).

| Lane | Mounted accepted state | Match | Product reading |
|---|---|---|---|
| Graph | G-H1..G-H4 audits PASS through Run 32783797303; scaling successor undecided | YES | Unchanged; depth ≤3 beta frontier stands either way |
| Physics | WP-003B-R2 + WP-005 FALSIFIED audited; within-site interventional program launched | YES | PH-3 stays REJECTED |
| Intel | cycle-1 SGDR integrated at PoC ceiling; cycle-2 Unbrowse pending | YES | SGDR remains PH-1's audited front door; Unbrowse stays OFFICIAL_CLAIM only |
| Product pipeline | zero outcomes anywhere | YES | Pre-outcome freeze remains constitutionally clean (§19) |

### Decision 2026-08-25 (fourth session)

- **PH-1 stays PRODUCT_CANDIDATE; Product Beta PB-001 RE-AUTHORIZED as the
  single authorized beta — request revision 4** (provenance-only bump;
  every Director-floor clause, assumption A1–A5 and directed pre-outcome
  revision v2 carried forward UNCHANGED). All five contract criteria
  re-checked and hold on independently re-read gates.
- **`directives/PRODUCT_OPTIMIZATION.md` authored** (was referenced by both
  role file and Director directive but did not exist anywhere): codifies the
  optimization charter — bottleneck/baseline/metrics/win-rule/scope/kill
  admission record per process, freeze discipline (§19-aligned), versioning
  after losses, fairness floors, wording-constraint inheritance, honest
  reporting, internal-only scope ceiling.
- **PH-2 WATCH / PH-3 REJECTED / PH-4 WATCH**: unchanged (no new audited
  evidence this session).
- Standing next step unchanged: **BETA_ARCHITECT commits BENCHMARK_PREREG
  v2 before any outcome; then BETA_BUILDER under F1/F2**. Public deployment
  and commercialization remain unauthorized without explicit human decision.

---

## Intake 2026-08-25 (fifth Product session on mounted accepted snapshots)

Session-start state anomaly, recorded for provenance (fourth occurrence):
the working tree again carried an UNCOMMITTED deletion of
`state/product_beta_request.json` plus a flipped `beta_launch=false`, while
HEAD held the committed rev-4 authorization. This session VERIFIED the root
cause instead of re-recording an anomaly:
`.github/workflows/product-loop.yml` lines 62-65 mechanically delete the
authorization file and flip `beta_launch` before every Director session.
Four director sessions have re-derived an identical decision because of this
one workflow step. **Escalation (outside Product write scope): infra owner /
human must make the product loop non-destructive** — until then,
authorization is read via `git show HEAD:state/product_beta_request.json`
and re-derivation on a hash-verified match is forbidden.

### Material discoveries this session

1. **The rev-4 directive was already executed — but marooned.**
   `BENCHMARK_PREREG.md` v2 + ARCHITECTURE/BUILD_PLAN/INTERFACES +
   `state/product_beta_architecture.json` were committed pre-outcome at
   `1457fd3cf8212f2bbea929b078aa5f1f7df8fdb6`
   (`origin/cycle/product/32861115761/architect`, 15:08Z), implementing
   `.directed_pre_outcome_revision_v2` as sole semantic change. It was never
   integrated into `lab/product`.
2. **The "build" commit is empty.** `aceaea6`
   (`origin/cycle/product/32861115761/builder`) has a byte-identical tree to
   1457fd3: zero vendor code, zero Phase-A/B rows. A full `git log --all`
   search confirms NO beta outcome rows exist on any branch. The persistent
   claims "no prereg v2, no builder output anywhere" in revs 3-4 were wrong
   about the prereg; they were right about outcomes.
3. **Chief CTO council CTO-2 review exists** (`lab/cto` 2d4505f, postdates
   the fourth session): independently verified the marooned freeze and issued
   `docs/CTO_TO_PRODUCT.md` — pointer-file durability protocol, critical path
   (F0 integration → WP-0 vendoring → LLM consumer wiring → arms with B1 from
   Intel AWM-min → cost_event telemetry BEFORE Phase A) and a pre-outcome
   prereg v3 delta pack.

### Fresh-context critic review (run before this decision, per charter)

Four critics returned convergent findings; all are folded into rev 5:

| Critic | Verdict | Adopted as |
|---|---|---|
| cto_product | DO_NOT_LAUNCH_BECAUSE_CONTROL_PLANE_SELF_WIPE | durability protocol + F0-first critical path |
| product_system_architect | CUT_LIST (login-packaging/V31 confound/MMR/alpha/B2 weight) | V31 fixed identically across all arm conditions (never a differing variable); knobs hashed into F1 manifest; alpha=0.4/lambda=0.7 frozen as audited config; B2 demoted to fixture check; local content-hashed fixtures; mechanical form-write allowlist |
| product_optimization_researcher | RETARGET_A1_CONSUMER_INHERITANCE_GATE | staged execution: Phase-A smoke/diagnostic gates A1 before confirmatory panel; fused-vs-incumbent attribution handled inside Phase A rather than blind stacking |
| product_baseline_performance_critic | BASELINE_FIX_REQUIRED | B1 strengthened/sourced from Intel AWM-min lineage with symmetric corpus; paired per-row deltas; CONJUNCTIVE two-pass replication; frozen comparator-selection procedure; R3 overhead reporting bound (+25%); producer≠eval disjointness; paraphrases outside V31 synonym classes; amortization + break-even N* accounting |

Note on disagreements: the architect recommended cutting login packaging and
V31 entirely; overruled with rationale — login packaging is one of the two
strongest audited blocks (G-H3/G-H4) and part of the declared task class
(enters at Phase B), and V31 is Graph-program adopted equipment; both stay,
but V31 is pinned identical across every compared condition so it cannot
confound attribution. The researcher's suggestion to soften the directed
SGDR swap was resolved by CTO alignment: keep the swap, add the Phase-A
stacked-vs-V31-only-vs-primitive diagnostic with frozen fallback ordering so
any A2 result is attributable to mechanism vs assembly error.

### Decision 2026-08-25 (fifth session)

- **PH-1 stays PRODUCT_CANDIDATE; PB-001 RE-AUTHORIZED as the single beta —
  request revision 5** (`state/product_beta_request.json`),
  `beta_launch=true`, durable pointer `state/product_current.json` written
  (phase F0_PENDING_PREREG_INTEGRATION). Win-rule floor carried VERBATIM
  through revisions 1→5; delta pack D1-D8 is additive strictness/diagnostics
  only, disclosed, and legal because zero outcomes exist anywhere (§19).
- **Execution order is binding**: nothing downstream starts before F0 lands
  (`1457fd3` integrated to `product-beta/PB-001/`, tag `pb001-F0`).
- PH-2 WATCH (CTO standing rule: zero hours until reproduced mechanism AND
  resolver exist). PH-3 REJECTED. PH-4 WATCH/deprioritized.
- Re-derivation ceremony is killed by the pointer protocol; future dirty-tree
  sessions log receipts instead of rewriting history.
- Public deployment and commercialization remain unauthorized without
  explicit human decision.

---

## Intake 2026-08-25 (sixth Product session — review of PB-001 BUILD status=BLOCKED)

This session reviewed the first actual Beta Builder execution of PB-001.
**PB-001 remains UNBENCHMARKED: zero Phase-A/B evaluation outcome rows exist
anywhere** (re-verified independently: `cost_events.jsonl` contains only
`phase=diag` harness-side events; no provider_call row, no pilot/smoke/arm
rows; no phase-B artifacts on any branch or mount). Nothing in this session
determines BEATS_BASELINE / PARITY / LOSES_BASELINE.

### What the Builder actually delivered (independently verified)

Builder branch HEAD `61c42d4` (F1 freeze `fc24c86`, v3 addendum `c287f00`
= current lab/product HEAD, F0 tag `pb001-F0` = `86b0102`). Verified this
session by direct inspection, not self-report:

| Item | Verification performed | Result |
|---|---|---|
| Freeze chain | git log both mounts | intact: infra hotfix `8f3980c` → F0 → v3 → F1 → builder state |
| KB integrity | recomputed sha256 of `kb_frozen.sqlite`/`kb_live.sqlite` | both `893486e348210d65f89abd…`, byte-match MANIFEST `kb_dump.sha256` and `diag_retrieval.json.kb_snapshot_sha256` |
| Outcome absence | event-class audit of telemetry + results tree + branches | zero outcome rows anywhere |
| Offline suite | ran all 13 test modules under unittest | 65 tests, 0 failures; 3 errors are `playwright`-missing environment artifacts of live-path integration tests (driver imports `runtime.react` → playwright), consistent with the offline-green claim |
| Producer Phase A | `phase_a_result.json`, maintenance ledger, route-absence records, B2 sanity rows | present, internally consistent (producers 8/8; B2 4/4 replay-clean) |

Two defects found by the Builder, both disclosed rather than repaired
unilaterally:

1. **BF-2 (environment)**: no authenticated LLM backbone endpoint is
   configured (`PB_LLM_API_KEY`/`PB_LLM_MODEL` unset). WP-1 correctly
   recorded BLOCKED instead of fabricating provider accounting. Armed and
   unrunnable-until-credentials: provider telemetry row, B0 pilot smoke,
   Phase-B agent-arm rows, ablation slice, VERDICT.
2. **D2 attribution diagnostic fired its frozen proceed/block rule**
   (addendum D2.5). On the real built KB, retrieval@1 over the 8
   trained-coverage panel tasks: **stacked SGDR⊕V31 front door 3/8;
   V31-canonicalized desc-only ranking 8/8; primitive lexical scorer 7/8**.
   Ground truth = producer-provenance fragment ids (training-side). The one
   sanctioned assembly/plumbing repair round found NO defect (seams S1–S6
   pass; vendored-scorer fixture reproduces Intel numbers exactly);
   failures localize to the mechanism itself — fused α=0.4 state-summary
   term selects context-matching-but-goal-wrong fragments under shifted
   entries. Second consecutive violation ⇒ per frozen rule
   MEASUREMENT_INVALID_BEFORE_OUTCOME, routed to this Director.
   Third finding **BF-1** (measurement-design): panel task 10's anchored
   predicate is satisfied by its own entry state (zero actions for every
   arm) — disclosed, not swapped unilaterally.

Hygiene defect found by this session (not by Builder): 
`state/product_beta_build.json.manifest_hashes.kb_frozen_sha256` records tail
`…c0a0695b…` matching NO committed version of the artifact (git-history
re-hash of every blob touching `kb_frozen.sqlite` yields only
`…f89abd8f…`, which MANIFEST, diag record and my recomputation agree on).
Pure transcription defect; correction WITH disclosure directed at the next
builder commit. MANIFEST remains authoritative and correct.

### Fresh-context critic review (charter duty, run before disposition)

Two fresh critics were consulted on the intended disposition.

Adopted: one-shot front-door freeze (no repeated selection on the D2
instrument — selection set ≈ eval set would otherwise become tuning);
ratification litmus satisfied for A2 (the desc-only V31 configuration IS the
rev-1-ratified front door; SGDR stacking was the later directed experiment);
kill-counter tightening (next MEASUREMENT_INVALID batch OR post-go-live
environment-blocked event auto-kills — closes the "blocked≠invalid" loophole);
stub-backbone dress rehearsal as F2 entry condition (converts Blocker 1 into
ops latency); reserve-swap justification restricted to pre-D2 builder-preflight
evidence; D2@1 numbers barred from predictive quotation (spent-instrument
discipline); descriptive-only shifted-entry probe, explicitly non-binding.
Rejected/overruled: baseline critic's option to keep degenerate task 10 with
"fidget predictions" — rejected because a trivially-satisfied R3 row provides
no novelty-containment signal and silently halves R3 control power; the swap
with full disclosure preserves more measurement honesty. CTO's immediate
hard-park-before-any-artifact — overruled in favor of ONE bounded v4
amendment then hard park, because the v4 items are legal pre-outcome now and
would otherwise rot into a seventh re-derivation session.

### Decision 2026-08-25 (sixth session) — PB-001 continues; narrow component-level rearchitecture via versioned preregistration; beta UNBENCHMARKED

Disposition against the feedback menu: **not reject** (zero outcomes; both
blockers are an external ops gap and a component-level measured defect with
an audited substitute available), **not watch-park** (concrete legal
pre-outcome work exists), but **continue with a directed pre-outcome
revision v4** — the same intervention class as the earlier directed SGDR
swap, now reversing it on measurement. Request bumped to **rev 6**.

1. **D2 disposition**: MEASUREMENT_INVALID_BEFORE_OUTCOME accepted as valid
   pre-outcome attribution evidence. The SPIDER-arm front door reverts to
   the audited V31-canonicalized desc-only coverage ranking (the 8/8
   configuration; the rev-1-ratified family). ONE-SHOT: the front door is
   permanently frozen at v4; no further component amendment is legal this
   beta. The SGDR⊕V31 stacking is recorded as scoped NEGATIVE KNOWLEDGE
   (product composition result, n=8, training-side truth): it does NOT
   alter Intel cycle-1's verdict (fused > task-text-only in its own PoC
   regime) and must be cited only as a boundary condition on composing two
   separately validated mechanisms. The D2 instrument is SPENT for
   selection purposes; its numbers must never be quoted as predictive of
   Phase B.
2. **BF-1 disposition**: invoke §5.4-class reserve swap
   `E_R3_top10_tags → R-res_quotes_authors_nav` via a DISCLOSED F2
   amendment naming the new trigger class (entry-satisfiable anchor /
   zero discriminating power — not covered by v2 §5.4's literal trigger
   list). Justification may cite only builder-preflight fixture evidence
   (quotes_root.snapshot.json; predicate-fixture tests), which is
   independent of D2 ranking data. Symmetric-inflation analysis and the
   restraint-test caveat recorded as negative knowledge.
3. **Kill-condition accounting (tightened, pre-outcome)**: the D2 block
   counts as **1 of 2** consecutive-invalid slots. The second slot is
   consumed automatically by ANY subsequent MEASUREMENT_INVALID batch OR by
   ANY environment-blocked event that prevents executing the frozen
   confirmatory path once credentials exist; either ⇒ beta stops and PH-1
   returns to PROMISING-or-lower. No reinterpretation reserved.
4. **Backbone gap escalated** (external prerequisite, owned outside Product
   scope, same channel as the workflow-wipe fix). New F2 entry condition:
   a committed STUB-BACKBONE DRESS REHEARSAL — all arms × ≥1 synthetic row
   each through driver/judging/telemetry/verdict mechanics, clearly labeled
   SYNTHETIC, excluded from all statistics — before go-live. Go-live then
   equals credentials-configured plus replay.
5. **Assumption A2 rewritten** (only change to the assumption set): names
   the surviving audited configuration, scopes claims to trained-coverage
   repeats, renounces generalization. Win rule, baselines B0/B1/B2/B3,
   budgets, metrics, panel semantics: carried verbatim. Auditor duties
   added: verify B1 corpus/store independence and door-independent
   thresholds at F2.
6. **Hard-park rule**: after the single v4 amendment lands, Product logs
   receipts only — no further artifacts — until `PB_LLM_API_KEY`/
   `PB_LLM_MODEL` exist or the tightened kill condition fires.

PH-1 stays PRODUCT_CANDIDATE. PH-2 WATCH, PH-3 REJECTED, PH-4 WATCH:
unchanged (no new lane evidence). Public deployment/commercialization
remain unauthorized without explicit human decision.

---

## Intake 2026-08-25 (seventh Product session — re-authorization on refreshed mounts; CTO-4 pack dispositioned)

Session-start state anomaly (fifth occurrence of the same class): the
working tree again carried the deletion of `state/product_beta_request.json`
and a flipped `beta_launch=false`. This session VERIFIED the escalation
status instead of re-recording: **the destructive wipe is STILL LIVE at
HEAD `.github/workflows/product-loop.yml` L62–64 AND at the supposedly-
hotfixed commit `8f3980c`** (lines present in that tree too). Escalation to
infra/human is RENEWED; the pointer protocol remains the workaround.

Re-verifications performed before any decision:

| Check | Method | Result |
|---|---|---|
| Outcome absence | telemetry event-class audit + results tree + branch scan | ZERO Phase-A/B rows anywhere |
| Backbone credentials | environment inspection | `PB_LLM_API_KEY`/`PB_LLM_MODEL` ABSENT |
| v4 amendment status | branch/log search | NOT landed (no architect commit postdates `86a59ec`) |
| Authorization | `git show HEAD:state/product_beta_request.json` | rev 6 intact at HEAD |

### New audited signals integrated (all three material)

| Lane | Signal | Audit status | Product reading |
|---|---|---|---|
| Graph | `graph-inheritance-scaling` cycle 1 (run 32861557668) | SCALING-HOLDS at narrow basis; audit PASS after same-cycle repair of round-0 REVISE | Depth economics of inherited memory have PoC support beyond toy depth: quotes-side chains needing 4–5 DISTINCT fragment classes solved memory-led in both deterministic passes with 1–4 novel actions vs 49–76 cold / 49–65 degraded-trajectory reference; 24/24 contrasts. Hard limits travel: quotes-only (books UNMEASURED), achieved ≤4 classes, scripted consumers, single-site inventory carries everything, giter_v31 edge-equipment transfer FAILED (qualify_count=0). Supports PH-1's depth≤3 panel frontier; adds NO feature to PB-001. The equipment-transfer failure independently corroborates rev 6's D2 mechanism-not-assembly reversion reading. |
| Physics | WP-006 identifiability gate (run 32866107906) | FALSIFIED; lane TERMINATED per pre-declared stop rule; final gate PASS safe_to_integrate | PH-3 permanently REJECTED (third audited negative; no reopening instrument exists). Salvage retained: descriptive exports addressed to Graph G8/G9 and maintenance accounting. Audited instrument lesson ADOPTED as cross-lane interface requirement: an action slot may be declared executable only after a recorded classifier×executor integration-test witness (168 deterministic dead-arm failures observed: click_link#0 0/84 wikipedia, 0/84 gutenberg, 0/21 openlibrary vs 217/217 elsewhere); placement chosen by fresh critic review: admission gate at Runtime capsule registration (candidate stays non-executable without witness), not applicability fields (wrong layer) or runtime verifiers (pay the failure first). |
| Intel | cycle 5 Unbrowse clean-room reproduction (runs 32861355080→32873081963, gate PASS after documentary-only repair) | VALIDATED_USEFUL, claim-tier ceiling PROOF_OF_CONCEPT | FIRST reproduced+audited execution-substrate mechanism: three-tier route ladder (passive capture → first-party filtering → pointer-only records → direct cached HTTP replay w/ TTL + nine-code transparent escalation vocabulary; no-silent-substitution core proven under corrupted-auth/expired-TTL/deleted-record stress). Repeat tasks ran with 0 browser launches (vs 6/1 per browser pass), payload equivalence 10/10, sandbox median speedups 37.05x/8.66x — BUT bare HTTP with perfect knowledge is equal-or-faster, so the demonstrated value is parity WITHOUT privileged knowledge plus induced {id} template reuse on unseen records. Limits: single host (httpbin tier), scripted policies, n=5/task, ToS flag unresolved; vendor 94-domain/100x claims remain OFFICIAL_CLAIM never reproduced. |

### CTO-4 council intake and disposition

The CTO-4 execution-audit pass (postdates session six; read accepted
`lab/product@c287f00`) identified HIGH decode-debt defects in PB-001's
verdict machinery, verified real this session by direct inspection:
**X15** — INTERFACES §10 freezes `comparator = higher-success baseline
(tie→B1)` with NO B3 and enum `LOSES`, while addendum D4.2 selects
per-regime from {B0,B1,B3} tie→lowest tokens and BUILD_PLAN_V3_DELTA uses
`LOSES_BASELINE|BLOCKED`: the headline verdict was not auditor-recomputable.
**X16** — B3 cards license direct-URL gotos (`/catalogue/page-N.html`,
page-50 depth, slug_id pattern) while SPIDER-arm `browser_actions` counts
silent-executed click-chain primitives: median action-reduction floors vs
B3 measured navigation-policy asymmetry, not inheritance.

Fresh-context critic review (charter duty; three critics, converged):

| Critic | Key verdicts adopted |
|---|---|
| cto_product | KEEP PB-001 (kill/park fails economics; no fatal decodability case survives the fix pack). Fold into ONE atomic amendment. Order of leverage: verdict reconciliation > action-unit normalization > B3-binding-via-selection > guards > edge_iter > token split > leakage map. REFUSE D2.5 rescoping (moot/spent = threshold shopping). Extra findings folded: swap task has LESS card coverage than retired task (disclose); seam lint belongs inside the dress rehearsal; PH-4 deprioritized below PH-2. |
| product_baseline_performance_critic | Best-of-{B0,B1,B3} everywhere via completed D4.2; NO separate WIN clause for B3 (double-counting); goto-NORMALIZE the metric and do NOT route-minimize producers (KB regeneration breaks pinned hashes behind the spent instrument); floors consume total billed tokens with cache state pinned/disabled identically; pin median convention, division guard, occupancy floor (<6 paired cells ⇒ MEASUREMENT_INVALID), failed-CMP costs-as-incurred, full tie cascade ending deterministic arm-id. |
| product_system_architect | Receipts-only while parked (telemetry slot and PH-2 gates doc both rejected as artificial loops). WP-006 lesson placement: producer-side admission gate at Runtime capsule registration. Post-PB-001 decision tree recorded. Flagged TWO REAL DEFECTS in results/product/PRODUCT_HYPOTHESES.json (stale fused-front-door architecture text contradicting rev 6; stale PH-2 "no independent verdict exists" claim falsified by cycle-5) — corrected this session. |

### Decision 2026-08-25 (seventh session)

- **PH-1 stays PRODUCT_CANDIDATE; PB-001 RE-AUTHORIZED as the single beta —
  request revision 7** (`state/product_beta_request.json`),
  `beta_launch=true`. Win-rule FLOORS carried verbatim since rev 1; rev 7
  adds `.directed_pre_outcome_revision_v5` (items W1–W8) folding the CTO-4
  pack into the SAME single architect amendment commit as the pending v4
  items V1–V6: verdict-contract reconciliation (per-regime best-of-{B0,B1,B3},
  deterministic tie cascade, unified enums, re-pinned verdict script);
  navigation-equivalent action units as the floor metric (raw counts stay
  descriptive; NO producer route-minimization); per-regime scope + B3
  leakage map gating R3 comparator selection; mechanical guard batch (t=0
  exclusion generalized incl. swapped task, division guard, N*=∞ convention,
  ≥2-cycle amortization estimability, frozen compute-projection/abort cap,
  D8 REAL-row definition, per-class producer floor); mandatory edge_iter
  slice as sole licensed A3-attribution instrument; total-billed-token
  accounting with cache state pinned identically + cached-split reporting;
  statistics conventions (median interpolation, <6-paired-cell occupancy
  ⇒ MEASUREMENT_INVALID, failed-CMP costs-as-incurred); dress rehearsal
  extended with the WP-006 seam lint over action-primitive × element-class
  pairs. Two CTO-4 items REFUSED with recorded reasons (X10/D2.5 rescoping;
  separate B3-parity WIN clause). All five beta-opening criteria re-checked
  on independently re-read gates; zero outcomes exist so §19 cleanliness holds.
- **PH-2 WATCH → PROMISING**: Intel cycle-5 clears half the standing gate
  (reproduced + audited mechanism with a proven safety core); the other half
  stands (Runtime has zero artifacts ⇒ no resolver/consumption surface).
  Dual unlock before any candidate/beta status: multi-host + active-staleness
  validation (Intel's next mission) AND a Runtime resolver. Trust landscape
  now MEASURED (~12% malicious-skill prevalence; 9/11 registries shipped a
  benign PoC malicious server) and binds any future trust model. Wording
  constraints travel verbatim from the cycle-5 gate. Zero hours on
  registry/marketplace features. Nothing enters PB-001 or any successor beta
  before the dual unlock.
- **PH-3 REJECTED (permanent)**: WP-006 terminal falsification closes the
  lane; salvage = descriptive exports; seam-lint lesson adopted as interface
  requirement only.
- **PH-4 WATCH, deprioritized below PH-2** on evidence ordering.
- **Next step binding**: ONE combined architect amendment commit (V1–V6 +
  W1–W8), then HARD PARK pending backbone credentials; go-live sequence
  unchanged (credentials → provider telemetry row → dress-rehearsal replay
  incl. seam lint → B0 pilot smoke → Phase B under the frozen win rule).
- Public deployment/commercialization remain unauthorized without explicit
  human decision.

A losing beta — including the council-predeclared modal LOSE-vs-B3-card
outcome — remains an acceptable, informative result and will be absorbed
per the feedback rules in the role directive.

---

## 2026-08-25 — Eighth session: PB-001 BUILD status=BLOCKED formal review

- **Reviewed**: BETA_BUILDER `status=BLOCKED / no_backbone_available` (architect mount
  `/tmp/spider_beta_architect`, builder mount `/tmp/spider_beta_builder`).
- **Verdict**: BLOCKED **UPHELD** as a legitimate ops blocker (PRODUCT_OPTIMIZATION
  taxonomy: "cannot be fairly tested in the current environment"). Credentials
  PB_LLM_API_KEY/PB_LLM_MODEL re-verified ABSENT by the Director. Kill slots remain
  **1 of 2** consumed: v4 V4 consumes slot 2 only for post-credential invalid/blocked
  events; pre-go-live credential absence does not auto-stop.
- **Disposition: WATCH (armed-park)** — beta stays AUTHORIZED + FROZEN + ARMED.
  NOT rejected: zero outcome rows exist, no fairness defect, nothing negative to
  absorb — rejection would be evidence-free abandonment. NOT rearchitected: V1
  permanent front-door freeze stands, no measured bottleneck implicates design,
  CTO-4 decode-debt pack already dispositioned (adopt W1–W8 / refusals recorded).
- **NOT_BENCHMARKED re-verified directly** (not trusted from state): cost_events.jsonl
  = exactly 8 harness-side rows (action/retrieval_event/summary_event/health/
  write_guard/violation); zero provider_call rows; zero Phase-A/B outcome rows.
  No superiority or comparative claim is licensed anywhere.
- **Director independent verification**: kb_frozen.sqlite sha256 byte-match vs
  MANIFEST (...f89abd8f...); compute_verdict.py + panel.json hash-match the v4
  amendment supersession records; dress rehearsal SYNTHETIC-labeled green with W4e
  violation detectors fired and W8 seam-lint dead_pairs empty;
  `python -m harness.run_phase_b` → BLOCKED/no_backbone_available, exit 3; clean-env
  offline suite 84 passed / **0 assertion failures** (7 failures all Playwright
  environment artifacts; Builder env had playwright 1.62.0 → its 91-passing claim
  consistent).
- **Defects found & recorded**: (a) stale direction state on both mounts still said
  ARCHITECT after the amendment landed and WP-8 executed — corrected in
  state/product_direction.json (eighth session); (b) PROVENANCE GAP: combined v4+v5
  amendment + WP-8 artifacts exist ONLY on session mounts while lab/product HEAD
  e84b11c lacks them and the product-loop.yml destructive-wipe defect remains LIVE at
  HEAD — recovery hashes pinned in state/product_current.json.artifact_pins;
  merge/push into durable branches directed as first action at next activation;
  (c) minor: build-state test counts must name the exact offline subset going forward.
- **State**: continue=false (frozen park rule: receipts-only once the amendment lands
  without credentials); next_action=WAIT_FOR_EVIDENCE. Resume = configure backbone →
  `python -m harness.run_phase_b` (gate chain mechanical) → pin model_id before any
  outcome row.

---

## 2026-08-25 — Ninth session: Runtime R0-1 + Graph G-H6 intake; provenance gap RESOLVED; bounded durability activation

- **Trigger**: new ACCEPTED lane evidence since session 8 — Runtime R0-1 (audit gate
  PASS run 32887030457, integrated `origin/lab/runtime` 9dc50ba) and Graph G-H6
  SITE-BOUND (audit PASS run 32900187567). This fires the park rule's own review
  condition ("new audited lane signal legally bearing on PH-1/PH-2 disposition").
- **Credentials re-verified ABSENT live**; wipe defect re-verified STILL LIVE at HEAD
  (`product-loop.yml` L62–68: deletes `state/product_beta_request.json`, forces
  `beta_launch=false`). Working-tree request file restored BYTE-IDENTICAL from HEAD
  under the pointer protocol; sha256 pinned `d8b007a7…d7582`.
- **Session-8 PROVENANCE GAP RESOLVED**: the feared mount-only copies were not lost —
  `/tmp/spider_beta_architect` and `/tmp/spider_beta_builder` are gone, but the v4+v5
  amendment line (`ddce3a3`) and Builder WP-8 line (`7657565`) are durably pushed on
  `origin/cycle/product/32886859788/{architect,builder}`. All five recovery hashes
  re-verified byte-exact, including the **disclosed** dress-rehearsal supersession:
  MANIFEST `v4_builder_wp8.verification.dress_rehearsal_rerun` records record
  `02dddfaa…` superseding `823dedea…` (rerun against WP-8-amended code, green,
  dead_pairs empty). No unexplained hash drift exists anywhere in the frozen set.
- **Runtime R0-1 accepted into Product reasoning** at its audit ceilings, none of
  which license a Product claim: exact-repeat cell action/load PARITY 4v4 with novel
  decisions 0v4 and the producer's own compression wording WITHDRAWN — recorded here
  verbatim so the ledger cannot be quoted as compression evidence later; stale-context
  cell clause-attributed ABSTAIN → valid `spider.plan/v0` handoff → one caller-side
  novel navigation → verified success vs truthfully-reported baseline budget
  exhaustion (illustrative failure avoidance, never a ratio). Cost-event twins vs
  `pb001.cost_event/v0`: 88 pairs / 0 identity errors ⇒ the interim-telemetry 1:1
  field-migration duty contracted at D8 build time is now TRIGGERED.
- **Graph G-H6 accepted**: reuse value is INVENTORY-CONDITIONAL (books depth≥4
  composites: zero qualifying memory-led rows in either pass; quotes family replicated
  bit-identically); attribution taxonomy = description-vocabulary miss / wrong-class
  binding / budget-bounded exploration. Reinforces PH-1's locked scope without touching
  beta text. A NON-BINDING post-loss decode plan using this taxonomy is pre-recorded in
  `state/product_direction.json` so post-outcome attribution cannot be invented ad hoc.
- **Intel cycle-6 EXCLUDED**: multi-host/staleness program exists only as unintegrated
  repair-round branches; unaudited branch work moves nothing.
- **Dispositions unchanged on the merits**: PH-1 PRODUCT_CANDIDATE parked (R0-1's n=1
  scripted zero-provider cells prove nothing about PB-001's real-LLM token-economics
  regime; V1 freeze stands; kill slots 1 of 2). PH-2 PROMISING — unlock (1) unmet;
  unlock (2) now has accepted PRELIMINARY PoC-scale evidence via R0-1, formal
  satisfaction deferred to Runtime route-tier acceptance (not a Product discretionary
  call). PH-3 REJECTED permanent; PH-4 WATCH. `beta_launch=false`; no second beta.
- **Fresh-context critical CTO consulted** (adversarial pass over all six dispositions).
  Adopted: slot-contention rule (mandatory documented review if any other hypothesis
  becomes candidate-eligible while credentials absent — replaces a hard sunset, since
  no alternative claimant exists today); ONE bounded BETA_ARCHITECT durability session
  NOW rather than at credential-time (the live wipe defect makes deferral the risky
  posture); pre-recorded decode taxonomy; escalations sharpened with mechanical
  remedies (exact workflow lines to delete; exact env vars/resume command for keys).
  Rejected with reasons: terminating PB-001 (evidence-free abandonment of a fully
  built, twice-audited-adjacent, armed instrument whose modal LOSE outcome remains
  decodable and useful), Director-authored harness edits (role boundary: Director does
  not implement the beta), informal "partial unlock" precedent for PH-2 (erodes gate
  discipline), treating R0-1 parity cells as economic evidence (n=1 scripted ≠ token
  economics).
- **Directed next role**: BETA_ARCHITECT, bounded and enumerated — (1) merge/push both
  durable lines into a lab branch UNCHANGED + re-verify hashes incl. the supersession
  pair; (2) ONE disclosed pre-outcome measurement-infra commit implementing dual-id
  acceptance/mapping (`spider.cost_event/v0` alongside `pb001.cost_event/v0`) per the
  triggered migration duty — no treatment byte may change; offline suite subset +
  dress-rehearsal replay re-run; hashes re-pinned; (3) return to hard park unless
  credentials appear mid-session ⇒ frozen go-live gate chain directly.
- **State**: continue=true ONLY for that bounded session (next_action=ARCHITECT);
  returns to continue=false / WAIT_FOR_EVIDENCE on completion or inability to execute;
  flips to BUILD only when PB_LLM_API_KEY/PB_LLM_MODEL exist. NOT_BENCHMARKED
  unchanged; no superiority or comparative claim licensed by anything in this entry.

## 2026-08-25 — TENTH DIRECTOR SESSION (bounded durability execution + Intel cycle-6 intake)

**Posture**: hard park maintained; `beta_launch=false`; single authorization PB-001 rev 7
(`d8b007a7…` @ HEAD) intact. Zero outcome rows anywhere; NOT_BENCHMARKED unchanged.

- **Working-tree wipe recurrence handled per pointer protocol**: `state/product_beta_request.json`
  found wiped again by the live control-plane defect (`.github/workflows/product-loop.yml`
  L62–68 re-verified present at HEAD); restored BYTE-IDENTICAL from HEAD; sha256 re-pinned
  `d8b007a7d72f3337ce4d8004bc6b026f4aa746dfdb4af1bce4f6a517b01d7582`. Escalation renewed.
- **Credentials re-verified UNSET live** (`PB_LLM_API_KEY`/`PB_LLM_MODEL` absent) — hard-park
  precondition holds; the frozen go-live gate chain remains correctly un-startable.
- **Bounded BETA_ARCHITECT durability session EXECUTED via Product systems-architect cell**
  (directed by ninth session; previously never landed). Landed on `lab/product`, NOT pushed
  until Director verification:
  - `cf25299` merge 1/2: architect line `ddce3a3` (v4+v5 amendment) byte-identical TAKE-set,
    Director-owned files kept at dc716c5 bytes.
  - `7c2ca71` merge 2/2: builder line `7657565` (WP-8 build incl. kb_frozen/kb_live/phase_a
    artifacts) byte-identical; all add/add conflicts resolved from builder bytes.
  - `2988fa1` measurement-infra delta (pre-outcome, disclosed): CTO-4 §5 dual-id cost-event
    acceptance — additive `normalize_cost_event()` seam in telemetry.py + ingestion seam in
    compute_verdict.py + new twin-equivalence test; MANIFEST `analysis_code_hash` repinned
    `608c2ecb→0cb76809` (corrects the builder line's stale entry; authoritative v4 pin
    `992dc919` held through BOTH merges and changed only via this contracted delta).
  - `770c87c` receipts: `results/product/PB001_durability_receipts.json`.
  - **Director independent verification**: 6/6 pins MATCH post-merge pre-delta; post-delta
    tree matches all session pins with the one CONTRACTED repin; dress-rehearsal replay
    regenerated against amended code in disposable worktree = BYTE-IDENTICAL (`02dddfaa…`);
    offline suite green on Director's own run (41 passed across verdict-mechanics +
    panel-spec + dual-id + integration-local); diff scope additive-only — no arm/prompt/
    threshold/budget/win-rule byte touched; zero outcome rows created; staged control-plane
    agent work snapshotted/restored byte-exactly outside session commits.
- **Intel cycle-6 intake (NEW audited evidence since session 9)**: cycle closed audit PASS
  (run 32897120087) = honest MEASUREMENT_INVALID on multi-host/staleness program; instrument
  defects, nothing established either way; ONE capped instrumentation-restoration attempt
  remains. Dispositions unchanged on the merits; PH-2 unlock (1) epistemic status sharpened
  from "unintegrated" to "audited-closed invalid, final attempt capped".
- **PH-2 unlock(1) terminal-resolution mapping preregistered NOW** (planning discipline;
  non-binding, alters no lane verdict): restoration attempt USEFUL ⇒ audit-gated progress
  toward unlock(1); NO_ADVANTAGE / FAILED_TO_REPRODUCE ⇒ unlock(1) premise falsified at
  measured tier, PH-2 demoted below PROMISING absent new external evidence; second
  MEASUREMENT_INVALID ⇒ live collection ends, unlock(1) dead absent new external evidence.
- **Fresh-context critical CTO consulted (advisory)**: AGREE_WITH_PARK. Adopted: PH-2 decode
  mapping preregistration (above); explicit record that no slot-contention review is due
  (graph-addressing-fused-retrieval is unaudited round-0 Graph-lane work; R0-1 W1–W9 bind
  Runtime's next cycle, not a product hypothesis). Its steelman for killing PB-001
  pre-outcome (B3 card ceiling ~70% modal LOSE; G-H6 inventory-conditionality) examined and
  REJECTED as grounds to kill: A1 (real-LLM consumer, token economics) is a first-order
  unknown nothing has tested; decode machinery exists precisely to make a LOSE attributable;
  killing pre-outcome converts falsifiability into hunch. Run stands.
- **State**: bounded session COMPLETE ⇒ hard park restored: `continue=false`,
  `next_action=WAIT_FOR_EVIDENCE`. Flips to `continue=true/BUILD` only when
  `PB_LLM_API_KEY/PB_LLM_MODEL` are configured (then frozen go-live gate chain, unchanged).
  No superiority, compression or comparative claim is licensed by anything in this entry.

---

## 2026-08-26 — ELEVENTH DIRECTOR SESSION (Intel cycle-7 + Runtime R1-1 intake; CTO-5 adoption; rev 8; park maintained)

**Posture**: armed hard park MAINTAINED after fresh re-evaluation on refreshed mounts.
`beta_launch=false`; single authorization PB-001 now **rev 8** (`725cbfe4…`, superseding
rev 7 `d8b007a7…` byte-identical restore after another live wipe recurrence). Zero outcome
rows anywhere (re-verified); NOT_BENCHMARKED unchanged.

**Live verifications before any decision**: `PB_LLM_API_KEY`/`PB_LLM_MODEL` UNSET;
NO local inference capability exists in this environment (no ollama/vllm/llama servers,
no open ports 11434/8000, no `openai`/`transformers`/`torch` packages) — the CTO-5 S4
"locally served open-weight model" path is assessed INFEASIBLE in-lane today; wipe defect
re-verified STILL LIVE at HEAD L62-68; request file wiped from working tree again and
restored BYTE-IDENTICAL from HEAD under the pointer protocol.

**New audited lane evidence integrated**:

| Lane | Signal | Audit status | Product reading |
|---|---|---|---|
| Intel | cycle-7 route ladder (run 32908028297) | PASS; mechanism status INCONCLUSIVE (VALID measurement, zero-power frozen family gate: min achievable Holm-adjusted p=0.125>0.05 at n=5 — disclosed prereg design defect) | Neither success nor failure; nothing entered VALIDATED_MECHANISMS. Per-session-10 preregistered terminal mapping NONE of its outcomes fired (INCONCLUSIVE ∉ {USEFUL, NO_ADVANTAGE/FAILED_TO_REPRODUCE, second-MEASUREMENT_INVALID}) ⇒ no mechanical PH-2 movement. Unlock(1) REMAINS UNMET. Intel authorized ONE final powered round (n≥8 pref. 10, repair-free, FINAL — line closes permanently whatever it returns). Extended mapping preregistered NOW (below). |
| Runtime | R1-1 (run 32908002333, integrated lab/runtime@613fbd4) | Gate PASS; accepted at prereg ceilings | T3 near-repeat compression OBSERVATION (SPIDER 4 vs BASE 11 actions, both offsets, zero novel decisions; single task/site family, two passes, scripted caller, ZERO provider calls; multi-task replication + ≥3-sample stats OWED); C1 exact-repeat PARITY replicated ×2 (consistent with CTO-5 deprioritization of transparent-repeat optimization); C2 failure-avoidance replicated ×2 with valid plan handoff; ABL-A1 hint causality PoC-scoped; write-back capsule QUARANTINED CANDIDATE (maintenance cost unmeasured W-C2-1 binding). OBSERVATION TIER ONLY: adjacent evidence for PH-1's regime premise; tests none of PB-001's assumptions A1/A4; cited nowhere in product narratives until W-C2-1/W-C2-2 discharge. |
| CTO | CTO-5 council pass (2026-08-26) | Advisory synthesis over accepted mounts | Adopted: X28 endpoint-stability hazard → rev 8 pack; S4 "any compliant backbone incl. local open-weight" → recorded as activation option pending feasibility receipt (INFEASIBLE in-lane today, receipt logged); delivery-integrity debt catalogued (escalations renewed). Not adopted: any allocation change to Product dispositions. |

**Fresh-context critic consultation** (charter duty, pre-decision): all four critics —
`cto_product`, `product_system_architect`, `product_optimization_researcher`,
`product_baseline_performance_critic` — independently returned convergent verdicts:
**MAINTAIN armed park; NO second beta; NO floor/comparator edits pre-outcome.**

- Kill rejected (evidence-free abandonment; A1 real-LLM economics first-order unknown
  untested by anything incl. R1-1's zero-provider cells; decode machinery makes LOSE
  attributable).
- Second beta rejected: a T3-derived instrument would measure a different dependent
  variable (scripted hint-channel action counts) than PB-001 (real-LLM token/call/
  wall-clock economics through the addressing front door), could not flip any PH
  disposition, and fails Runtime's own standing gates (W-C2-6 strongest-baseline
  unresolved; CF-25 curl-null unclosed: bare HTTP ≈ replay C/B 0.92/0.73).
- Smallest architecture that could win NOW: **none exists without a backbone** — B0
  (the credible current agent) is by definition an LLM agent on the identical backbone;
  binding floors consume billed tokens; every credential-free artifact already run is
  correctly SYNTHETIC/non-evidence forever.
- `beta_launch=false` during park confirmed HONEST (flag = execution state; authorization
  lives in the sha-pinned request + this ledger).

**Decision 2026-08-26 (eleventh session)**

1. **PH-1 stays PRODUCT_CANDIDATE (parked); PB-001 remains the single authorized beta —
   request bumped rev 7→8** for exactly ONE semantic addition:
   `.directed_pre_outcome_revision_v6` (X28 go-live-gate classification): credential
   declaration requires one green stability validation (dress-rehearsal replay incl. W8)
   BEFORE kill-accounting "post-credentials" begins; transport-instability failures at
   PRE-PANEL go-live gates are logged gate failures, NOT instant slot-2 death; FROZEN
   numeric persistence rule K=3 consecutive failed full gate-chain attempts across ≥2
   dispatch sessions ⇒ persistent environment-blocked event ⇒ consumes slot 2 per v4 V4;
   CAPABILITY-classified persistent failure (e.g., repeated B0 smoke <2/3 on a stable
   endpoint) explicitly CONSUMES slot 2; everything mid-panel/post-panel untouched
   (W4d/W7/MEASUREMENT_INVALID rules verbatim). Net effect disclosed in the request:
   narrows weather-death at pre-panel gates, strengthens against incapable-backbone retry
   loops; panel-runs-or-beta-stops invariant preserved. Win-rule floors verbatim since
   rev 1.
2. **Free disclosure executed (baseline-critic hole ii)**: "comparable success" in clause
   2 has NO separate numeric constant because it is STRUCTURAL in hash-pinned
   `compute_verdict.py` (0cb76809…): per-regime clause-1 non-inferiority within −0.10
   absolute INCLUDING R3; LOSE-1 fires when SPIDER leaves >25% of per-regime best-baseline-
   solved tasks unsolved; paired-by-task deltas use costs-as-incurred with CMP=0<S_t clip
   at −1.0; occupancy floor <6 valid paired cells ⇒ MEASUREMENT_INVALID. Recorded so no
   post-outcome interpretive dispute can arise.
3. **Binding narrative constraint adopted (CF-25/http_floor)**: any future BEATS_BASELINE
   narrative MUST carry verbatim the http_floor null-parity statement
   (`results/product-beta/PB-001/http_floor.json`: all 10 panel targets reachable by bare
   HTTP at zero LLM tokens, 203–517 ms) or be inadmissible as product evidence. The null
   stays OUTSIDE win-rule arithmetic by design (adding arms now = unjustified freeze
   violation).
4. **Extended PH-2 unlock(1) mapping preregistered BEFORE powered round 4 runs**
   (planning discipline; alters no lane verdict): USEFUL ⇒ audit-gated progress toward
   unlock(1); REPRODUCED_NO_ADVANTAGE / FAILED_TO_REPRODUCE ⇒ unlock(1) premise falsified
   at measured tier ⇒ demote below PROMISING absent new external evidence;
   INCONCLUSIVE-or-MEASUREMENT_INVALID (round 4 is FINAL; line closes permanently) ⇒ live
   collection ends, unlock(1) dead absent new external evidence. Cycle-7 free design
   requirements ADOPTED as binding on any future Product-side evaluation plan:
   response-validation policy declared per source/arm; numeric power proofs inside any
   prereg before freezing multi-arm family gates.
5. **Slot-contention trigger preregistered** (mechanical, replaces ad-hoc judgment): if
   Runtime R-line completes POSITIVE surviving BOTH the strongest scripted baseline AND a
   curl-level HTTP null AND a provider-carrying replication design exists ⇒ a claimant
   becomes candidate-eligible ⇒ contention review fires vs PB-001 monopoly BEFORE
   exclusive credential access. Until then: no eligible claimant exists; review not due.
6. **PARK CHARTER recorded** (converts future park reviews into checklist execution):
   - Flip conditions: credentials present + stability-green ⇒ frozen go-live chain
     mechanically; audited evidence creating a candidate-eligible claimant ⇒ slot-contention
     review first.
   - Admission rule: observation-tier/scripted results and INCONCLUSIVE intel verdicts enter
     as ADJACENT EVIDENCE ONLY — never spawn betas, never reopen dispositions, never cite as
     product evidence.
   - Pre-registered decoders: Intel round-4 mapping (item 4); Runtime R1 outcome mapping —
     killed-by-strongest-baseline/null ⇒ boundary knowledge only; replicated-with-economics
     ⇒ candidate-eligibility evaluation via item 5.
   - Standing citation bans until discharged: T3/quarantined write-back capsules (Runtime
     W-C2-1/2); any cycle-7 figure outside explicit observation-inside-INCONCLUSIVE framing.
7. **Activation checklist directed** (executes AT go-live, not before; avoids artificial
   sessions): (a) endpoint stability validation green; (b) dual-id ingestion seam
   hardening — enum-conformance assertion inside `normalize_cost_event` ingestion path +
   conformance fixture against REAL Runtime-emitted rows + one-writer-per-stream ownership
   rule (disclosed pre-outcome infra delta like 2988fa1); (c) optional pre-approved
   descriptive probe V-C (oracle-entry-context ranking on training-provenance rows,
   STRICTLY_DESCRIPTIVE_NON_BINDING, V5 precedent); (d) then frozen gate chain verbatim.
8. **Terminal fork preregistered** (baseline critic, adopted): at the NEXT Director session
   finding keys absent, the local-endpoint option is formally posed — granted-with-stability-
   gate ⇒ go-live chain; declined/infeasible ⇒ PB-001 closes TERMINAL `BLOCKED_UNRUN`
   (authorized+frozen+armed, never benchmarked, zero outcome rows, closed on external block;
   artifact pack preserved as durable negative knowledge) and PH-1 drops to PROMISING
   (untested at product tier; explicitly NOT falsified) in the SAME session. Indefinite
   park without that fork decision is not an option.

**Dispositions**: PH-1 PRODUCT_CANDIDATE parked (rev 8; kill slots 1 of 2; V1 freeze
stands; G-H6 inventory-conditionality + X27 addressing divergence remain interpretation
guards, not comparator defects). PH-2 PROMISING (dual unlock unmet; extended mapping
preregistered). PH-3 REJECTED permanent. PH-4 WATCH below PH-2. Public deployment and
commercialization remain unauthorized without explicit human decision.

A losing beta — including the council-predeclared modal LOSE-vs-B3-card ceiling — remains
an acceptable, informative result and will be absorbed per the feedback rules in the role
directive.

## 2026-08-26 — TWELFTH DIRECTOR SESSION (preregistered TERMINAL FORK executed: PB-001 closed TERMINAL BLOCKED_UNRUN; PH-1 -> PROMISING)

**Trigger satisfied on live evidence.** The eleventh session bound the fork: at the next
Director session finding keys absent, pose the compliant/local-endpoint option formally —
granted-with-stability-gate => frozen go-live chain; declined/infeasible => PB-001 closes
TERMINAL `BLOCKED_UNRUN` and PH-1 drops to PROMISING in the SAME session; indefinite park
without that decision is not an option. This was that session.

1. **Live verification receipts (all re-run this session):**
   - Credentials ABSENT: `PB_LLM_API_KEY`/`PB_LLM_MODEL`/`PB_LLM_BASE_URL` unset; env scan
     for OPENAI*/ANTHROPIC*/*API_KEY*/*BASE_URL* empty.
   - In-lane provisioning INFEASIBLE, second consecutive session: no ollama/vllm/
     llama-server binaries on PATH; ports 11434/8000/8080/1234 closed; python packages
     openai/vllm/transformers/torch ALL absent. CTO-5 S4 local-open-weight option remains
     infeasible today; feasibility receipt logged.
   - Wipe defect recurrence **#12**: working-tree `state/product_beta_request.json` wiped by
     `.github/workflows/product-loop.yml` L62-68 (still LIVE at HEAD); restored
     BYTE-IDENTICAL from HEAD rev 8 BEFORE any decision action (`sha256 725cbfe4…` match
     verified). Escalation renewed with mechanical remedy attached.
   - Zero outcome rows anywhere re-verified pre-closure (8 harness-side telemetry rows only;
     no provider_call rows; no VERDICT/raw_rows/phase-B artifacts on any branch or mount).
2. **Fork resolution: DECLINED_INFEASIBLE_IN_ENVIRONMENT.** No granting authority present or
   responsive across eleven consecutive escalated sessions; provisioning path verified absent
   twice under live audit; expected information value of another parked cycle is zero at
   nonzero cost. Executed mechanically per preregistration — no fresh critic round convened,
   by design: the four critics' converged eleventh-session output (maintain-park / NO second
   beta / no floor edits) plus their co-authored PARK CHARTER and terminal fork fully
   determine this execution; reconvening them to re-adjudicate a preregistered fork would be
   the exact re-derivation ceremony class killed permanently at CTO-5.
3. **Closure record.** PB-001: authorized 2026-08-25 (rev 1), three-times frozen through
   rev 8, durably merged, independently verified, armed with kill slots 1-of-2 consumed
   (D2 block), never dispatched past harness-side telemetry. Closed TERMINAL
   `BLOCKED_UNRUN` — authorized but never benchmarked, zero outcome rows, closed on external
   block. `beta_request` rev 8 remains at HEAD as CLOSURE PROVENANCE / durable
   negative-knowledge artifact pack; NOT a live authorization; must not be executed or
   amended. Kill accounting retired with closure.
4. **Artifact pack preserved as durable negative knowledge** (inheritable ONLY by a NEW
   successor authorization with floors verbatim; slot-contention rule governs claimants):
   D2 one-shot front-door reversion record (SGDR+V31 stack measured WORSE than
   desc_only/primitive on the built KB — scoped composition negative); http_floor null
   documentation (all 10 panel targets reachable via bare HTTP at zero LLM tokens, 203–517 ms)
   WITH its binding narrative constraint on any future BEATS claim; BF-1 anchor-swap
   rationale; B3 instruction cards + leakage map; panel v4 + paraphrases + dress-rehearsal +
   verdict script (floors VERBATIM since rev 1) — all pins carried in
   `state/product_current.json.artifact_pins`.
5. **PH dispositions after closure:** PH-1 **PROMISING** (dropped from PRODUCT_CANDIDATE per
   fork terms: untested at product tier, explicitly NOT falsified; A1/A4 remain first-order
   unknowns; scripted-tier audited support stands unchanged). PH-2 PROMISING (dual unlock
   unmet; Intel FINAL powered round pending under the preregistered extended mapping).
   PH-3 REJECTED permanent. PH-4 WATCH below PH-2. Public deployment/commercialization
   remain unauthorized without explicit human decision.
6. **No replacement beta — and why that satisfies "exactly one Product Beta" discipline.**
   The minimal product still cannot FAIRLY test SPIDER vs a credible current agent after full
   overhead: its decisive overhead dimensions (real-LLM consumer tokens/calls/latency against
   cold-agent AND instruction-card-ceiling baselines) are unmeasurable in this environment
   today. A scripted-only surrogate would duplicate already-audited Graph/Runtime coverage and
   test no PB-001 assumption (the critics' unanimous position). T3-derived second betas stay
   rejected (observation-tier, single-cell, comparator unresolved, curl-null lesson);
   slot-contention review not due — no eligible claimant exists.
7. **Standing rules carried post-closure** (`state/product_direction.json.
   standing_rules_post_closure`): admission rule (observation-tier/INCONCLUSIVE evidence =
   ADJACENT EVIDENCE ONLY); pre-registered decoders (Intel round-4 extended mapping; Runtime
   R1 outcome mapping); slot-contention trigger; citation bans until discharged (T3 +
   quarantined write-back capsules; cycle-7 figures outside INCONCLUSIVE framing; vendor
   Unbrowse numbers forever OFFICIAL_CLAIM; spent-D2 numbers never predictive).
8. **Flip inputs that resume Product work** (the ONLY paths back to active work):
   (a) compliant endpoint becomes available => PH-1 successor revival review derived from the
   preserved pack, floors inherited verbatim; (b) Intel FINAL round returns USEFUL =>
   PH-2 unlock(1) progress review; (c) Runtime R-line positive surviving strongest-baseline +
   curl-null with provider replication design => slot-contention review; (d) new AUDITED lane
   signal materially bearing on PH-1/PH-2/PH-4 premises. Absent these:
   `continue=false`, `next_action=WAIT_FOR_EVIDENCE`. Product does not spin on unchanged
   evidence.

**Session state writes:** `state/product_direction.json` (twelfth session, closure record,
standing rules, flip inputs), `state/product_current.json` (phase CLOSED_TERMINAL_BLOCKED_
UNRUN; authorization source of truth marked historical provenance), `results/product/
PRODUCT_HYPOTHESES.json` (build/internal-beta authorization flags false; PH-1 status history;
twelfth_session_note), this entry. Working tree `state/product_beta_request.json` = HEAD
rev 8 byte-identical (provenance only).

## 2026-08-26 — THIRTEENTH DIRECTOR SESSION (post-closure intake: flip inputs re-verified UNMET; CTO-6 duties discharged; beta_launch stays false)

New accepted evidence since the twelfth session, all consumed under the standing admission
rule (ADJACENT EVIDENCE ONLY unless a decoder fires):

1. **Intel cycle 8** (signal CYCLE_32931388530, audit PASS run 32931388530): the powered
   single-shot instrument was completed and frozen with numeric power proven in-prereg, but
   collected ZERO condition-level observations — `mechanism_status INCONCLUSIVE` strictly
   pending-measurement, `validated_mechanism=null`. The FINAL confirmatory dispatch is still
   OUT. **Flip input (b) not met.** Carried round-4 decoder remains armed unchanged.
2. **Runtime R2-1 accepted at frozen ceilings** (audit CYCLE_32933579869 PASS after repair r1):
   headline `FLOOR_VOID` — the environment accepts ANY credentials, so the preregistered
   wrong-password negative control passed verification and all floor verdicts are VOID by the
   frozen rule; no substrate inference either direction; witnessed-effect POC never triggered;
   WB quarantine stands; X31 killer (ii) is VOIDED, not discharged. **Flip input (c) not met**
   — no candidate-eligible claimant exists under the slot-contention rule. R2-2 formally
   demands the Product/CTO substrate-demand spec first.
3. **CTO-6 council pass**: closure of PB-001 reviewed adversarially and UPHELD; surrogate
   pre-credential instruments REFUSED; no second beta; no floor edits; route-tier HTTP
   executor REFUSED with three preregistered flip conditions; http_floor null confirmed as
   the PORTFOLIO-WIDE BEATS-narrative ceiling (X31); slot-contention trigger mechanically
   repaired (provider-replication design authorship becomes mandatory if Runtime's success
   branch fires); evidence-bar additions recorded for any future authorization.

**Live re-verifications:** backbone feasibility INFEASIBLE third consecutive session (env,
binaries, ports, packages); wipe defect recurrence #13 — working-tree request wiped again by
product-loop.yml L62-68, restored BYTE-IDENTICAL from HEAD rev 8 (sha256 725cbfe4… verified)
BEFORE any decision action.

**Duties discharged this session (the only Product work performed):**

4. **Closure-hygiene clause-mapping audit => PASS** (`results/product/PB001_closure_hygiene_audit.json`):
   every directed hardening item across the revision chain (v3 D1–D8; v4 V1–V6; rev7 W1–W8;
   rev8 X28) verified present in the frozen addenda and mapped to build WPs WP-0.5..WP-8d;
   WIN/LOSE floors byte-consistent between request rev 8 and compute_verdict.py
   (.50/.40/.30 reductions; .20 LOSE; −0.10 success tolerance; occupancy floor 6; conjunctive
   replication); all load-bearing pins recomputed and MATCHED (compute_verdict 0cb76809…,
   panel.json be006d7b…, telemetry.py 5f9f04a31117…, b3_leakage_map 389de646…,
   kb_frozen.sqlite 893486e348…). Zero vanished items; zero floor edits since rev 1.
   Interpretation note: literal "V3-A..G" lettering from unmounted radar feed
   CF-2026-08-25-27 resolved as the full directed chain (strictly stronger check).
5. **X22 hypotheses-vs-ledger lint folded in**: PH dispositions identical across
   PRODUCT_HYPOTHESES.json / ledger / direction file; flags false everywhere.
6. **Dormant successor-derivation map filed** (`results/product/PB001_SUCCESSOR_DERIVATION_MAP.json`):
   pack→floors→gates routing + revival triggers so any future flip-input revival takes ONE
   session without critic re-convention; explicit non-authorization clause.
7. **Substrate-demand spec FILED AND FROZEN** (`docs/PRODUCT_SUBSTRATE_DEMAND_SPEC.md`,
   Runtime R2-2 priority 1): measurement-invariant demand classes only where plain HTTP
   fails or discriminating failure exists (auth-lifecycle D1; spec-less SPA D2; drift-prone
   D3; parameterized-writable D4), default NO-GO, expansion authorized by nobody here;
   Runtime advised to proceed with the decidable canon pagination-floor cell without waiting.

**Decision on the session question (authorize exactly one Product Beta?):** NO.
A minimal product still cannot fairly test SPIDER vs a credible current agent after full
overhead: the decisive consumer-economics axis requires a compliant LLM endpoint (absent,
third live verification); every zero-provider regime in the audited record shows parity-or-
domination by trivial baselines (exact-repeat PARITY ×2; bare-HTTP floor; Intel C/B≈1);
and the single promising near-repeat compression observation has BOTH orthogonal killers
undischarged and owned by Runtime, whose newest result is a VOID verdict, not a positive.
Authorizing now would either duplicate audited lane coverage or rest on an unmeasurable
comparator. `beta_launch=false`; exactly-one-beta rule satisfied by zero open betas.

**Dispositions unchanged:** PH-1 PROMISING (NOT falsified; A1/A4 unknowns preserved; revival
via derivation map). PH-2 PROMISING (dual unlock unmet; Intel round-4 pending). PH-3 REJECTED
permanent. PH-4 WATCH below PH-2. Public deployment/commercialization unauthorized.

**Session state writes:** `state/product_direction.json` (thirteenth session),
`state/product_current.json`, `results/product/PRODUCT_HYPOTHESES.json`
(thirteenth_session_note), the three duty artifacts above, this entry. Working-tree
`state/product_beta_request.json` = HEAD rev 8 byte-identical (provenance only).

---

## Fourteenth Director session — 2026-08-26 — flip input (b) FIRED and DISCHARGED; four-critic round; NO BETA

**Trigger (changed evidence, first since closure):** Intel cycle-9 ACCEPTED in the mounted
snapshot (`CYCLE_32941504002`: audit gate PASS run 32941504002, `safe_to_integrate=true`,
`mechanism_status=VALIDATED_USEFUL`, `cycle_9_confirmation` appended to
`results/intel/VALIDATED_MECHANISMS.json` with mandatory dual-collection caveat and PoC
ceiling). The FINAL powered route-ladder round returned USEFUL => the eleventh-session
decoder fired mechanically and was **executed this session**.

**Decoder outcome — PH-2 unlock(1) = PARTIAL (no promotion):**
- Component A multi-host economics: **SATISFIED** at PoC ceiling — REPRODUCED_USEFUL on 4
  sandbox host-tasks / 3 hosts / 3 auth styles incl. spec-less session-token SPA
  (api.demoblaze.com); 48/48 interleaved valid pairs with zero browser actions at output
  equivalence; warm-amortized median speedups vs scripted browser traversal
  9.40x / 5.67x / 18.20x / 37.46x; one-sided Holm-adjusted sign p=0.000977 on all four;
  BCa ci_low>0 all four; LOHO direction stable. Capture value over auto-generated
  declarative specs attributed to **PARAMETERIZATION_CREDENTIAL_CONTENT** (spec client
  0.00 strict AND 0.00 when granted the replay arm's tolerance policy vs replay 1.00 on
  the same decision cell). Traveling caveats bind verbatim: single GUARDED EVALUATION,
  dual-collection disclosure, scout-tree figures NON-EVIDENCE forever.
- Component B active staleness/drift: **OPEN** — mutation detection replica-scoped only
  (never live drift per gate wordings); natural calendar TTL behind clock-gated
  deliverables-only window-2 (>=2026-08-27T00:30:08Z); multi-host live line CLOSED
  PERMANENTLY (once-extended CAP consumed).
- Dual unlock requires BOTH unlock(1) fully AND unlock(2). Unlock(2) unmet. =>
  **PH-2 remains PROMISING** with progress recorded. Promotion rules frozen before
  outcomes are not edited after them.

**Route-tier executor refusal re-evaluated mechanically on ACCEPTED evidence:** condition 1
MET (powered round USEFUL); condition 3 MET (C3p attribution on spec-less SPA cell);
condition 2 UNTESTED (= chartered Runtime R2-3 D1 writable-discriminating-substrate probe;
restful-booker write-path HTTP 418 persists). **REFUSE STANDS** (requires all three).

**Other intake:** Runtime R2-2 accepted (run 32940627441, PASS round-0-clean): pagination
cell class **FLOOR_DOMINATES** — bare HTTP within budget WITH a working failure-witness
discriminator => witnessed-effect inheritance has no measured headroom there (branch-b
recorded, that cell class only; K1 strongest-comparator killer still undischarged; no
compression phrasing leaves observation tier). Graph G-H8 accepted: induced keys NOT
adopted; exact goal_sig addressing stays standard; abstention-first resolver pattern
validated in-setting.

**Four fresh-context Product critics convened (changed-evidence rule):** cto_product,
product_system_architect, product_optimization_researcher, product_baseline_performance_critic.
**All four returned NO-BETA**, each via independent argument: candidate-cell partition
emptiness (every runnable comparison = forbidden duplication of audited lane results, void/
dominated oracle, floor-covered cell where BEATS is impossible in principle, unavailable
D1 substrate, or endpoint-blocked consumer economics); serial-conjunctive gate analysis;
break-even arithmetic (K*≈2–110 recurrences/route at 60–343x overhead ratios vs ~8% fleet
recurrence and 50–67% blind-miss drag); ten-item minimum benchmark evidence bar with items
3/6/10 unsatisfiable today. Convergent dominant-bottleneck finding adopted: **substrate
discriminativeness, not algorithms** — cycle-9's residual value monetizes only where plain
documented HTTP fails, and no such host exists in-environment yet.

**Pre-commitments filed (additive, dormant) in
`results/product/PB001_SUCCESSOR_DERIVATION_MAP.json` appendix_fourteenth_session:**
lifetime-economics panel sketch (maintenance+recovery-inclusive lifecycle cells vs
best-of {bare-HTTP null, B3-card policy, fresh traversal}); WritePath-class capsule sketch
(new-ID parameterized writes with verifiable wrong-input rejection vs docs-first thin-client
ablation); H-AUDIT selected-class break-even spec FROZEN; ten-item evidence bar for any
future BEATS claim; warm-amortized accounting warning as binding self-discipline; new flip
inputs (e) R2-3/D1 PASS and (f) window-2 landing routed.

**H-AUDIT honest refusal:** the critic-proposed zero-cost retrospective break-even audit was
artifact-verified BEFORE commissioning: committed PB-001 pack contains NO recurrence-bearing
rows (`runs` table empty; 8 telemetry-class cost events; toy KB 11 fragments / 21
transitions). NOT RUNNABLE without fabricating inputs => ARMED_BEHIND_DATA; commissioning
refused. Recorded as durable knowledge.

**Governance ruling issued (Product-owned):** window-2 deliverables-only TTL executions are
NEVER benchmark outcome rows absent an explicit new authorization meeting the full evidence
bar plus CTO/Meta concurrence. Default NO.

**Dispositions:** PH-1 PROMISING (endpoint absent FOURTH consecutive live verification);
PH-2 PROMISING (unlock(1) partial); PH-3 REJECTED permanent; PH-4 WATCH -> **DORMANT**
(CTO-7 council disposition adopted with critic concurrence).

**Session question (authorize exactly one Product Beta?):** **NO — beta_launch stays false.**
The emptiness of {fair ∧ non-duplicative ∧ winnable-after-full-overhead} comparison cells is
now verified constructively, not asserted. Exactly-one-beta rule satisfied by zero open betas.

**State writes:** `state/product_direction.json` (fourteenth session),
`state/product_current.json` (fourteenth receipts), `results/product/PRODUCT_HYPOTHESES.json`
(fourteenth_session_note; PH-2 progress; PH-4 DORMANT), derivation-map appendix above, this
entry. `state/product_beta_request.json` restored byte-identical from HEAD rev 8 BEFORE any
decision action — WIPE RECURRENCE #14 (defect confirmed still present at HEAD; escalation
renewed). Zero outcome rows anywhere; continue=false WAIT_FOR_EVIDENCE behind updated flip
inputs.

---

## Fifteenth Director session — 2026-08-27 — Authorization of bounded pre-beta engineering package PW-CONSUMPTION-LAYER-001

**Trigger:** UNCHANGED evidence since fourteenth session (no new lane signals). Product Director
evaluating whether to authorize a bounded pre-beta engineering package per the PRODUCT_DIRECTOR
role directive ("When no honest beta is ready, you may and usually should authorize exactly one
bounded pre-beta Product Engineering package if it can concretely reduce integration work or
uncertainty").

**Four fresh-context critics convened (charter duty, pre-decision):**

| Critic | Verdict | Key finding |
|---|---|---|
| cto_product | WAIT | Substrate indeterminate; economics undecidable; every comparison cell fatal. If spending 5%, only STEP-6 paperwork. |
| product_system_architect | PROPOSE | `product/consumption/` thin agent-facing layer. All components buildable NOW. Addresses 4/5 CTO-8 runtime_missing_primitives (RP1, RP3, RP4, RP7). 10 test files + thin-client baseline. |
| product_optimization_researcher | PROPOSE | Docs-first consumption contract feasibility probe. 4 acceptance tests. ~1 day. Subsumed by architect's fuller proposal. |
| product_baseline_performance_critic | Credible evidence impossible today | Strongest baseline = max over {B0, B1, B3, curl-null, scripted-traversal, generated-spec}. Full-cost accounting mandatory. Composability testing is valid pre-credential work. |

**Synthesis:** The architect's consumption layer is the strongest bounded package. It does NOT
claim product superiority, does NOT require LLM backbone, does NOT modify frozen benchmark
artifacts. It answers the prior question "can accepted primitives be made agent-consumable?" and
produces measurable integration-cost evidence via the thin-client baseline. The cto_product's WAIT
verdict is accepted for beta authorization (no beta is authorized) but overruled for this bounded
package: the package has positive integration/information value (addresses RP1/RP3/RP4/RP7, proves
composability before substrate decision).

**Decision:** Authorize exactly one bounded pre-beta engineering package PW-CONSUMPTION-LAYER-001.

1. **Work request written:** `state/product_work_request.json` with work_launch=true, work_id
   PW-CONSUMPTION-LAYER-001, concrete objective (extract resolve→execute→verify→report into
   standalone `product/consumption/`), accepted evidence refs, allowed paths, 10 executable
   acceptance tests, maximum scope (22 files, ~2000 LOC, no changes to existing code), explicit
   dependencies, and 4 kill conditions.
2. **Direction updated:** `state/product_direction.json` — work_launch=true, next_action=ENGINEER,
   continue=true (for duration of work package only), next_role=PRODUCT_ENGINEER.
3. **Scope:** Extract Graph store + V31 equipment + goalsig gate + SpiderExecutor + verification
   + telemetry into a thin, importable consumption layer. Include thin-client baseline (capsule
   JSON without execution) to measure integration-cost delta. Include conformance test suite
   (RP1). Include freshness hook (RP3, conservative UNKNOWN default). Include negative knowledge
   store (RP4, fail-open default). Include derivation manifest (RP7).
4. **Kill conditions:** (a) primitives can't be wrapped without leaking internal knowledge;
   (b) thin-client achieves equivalent composability at lower cost; (c) >2 of 10 tests fail
   after one repair; (d) conformance test imports internal modules.
5. **What this does NOT do:** Does NOT authorize a beta. Does NOT claim product superiority.
   Does NOT modify frozen PB-001 artifacts. Does NOT require LLM backbone. Does NOT resolve
   the endpoint availability escalation. Does NOT change any PH disposition.

**Dispositions unchanged:** PH-1 PROMISING (endpoint absent FIFTH consecutive verification
pending). PH-2 PROMISING (unlock(1) partial). PH-3 REJECTED permanent. PH-4 DORMANT.

**State writes:** `state/product_work_request.json` (new), `state/product_direction.json`
(fifteenth session), `results/product/PRODUCT_HYPOTHESES.json` (fifteenth_session_note), this
entry. continue=true for duration of work package; returns to WAIT_FOR_EVIDENCE on completion
or kill. Zero outcome rows anywhere; no superiority or comparative claim licensed by anything
in this entry.

---

## Sixteenth Director session — 2026-08-27 — Review of PW-CONSUMPTION-LAYER-001 audit gate=REVISE; authorization of bounded repair package

**Trigger:** PW-CONSUMPTION-LAYER-001 completed (Engineer status=READY_FOR_AUDIT, self-reported
86/86 passing). Independent product_work_auditor audit gate=REVISE. Product Director reviewing
before integrating or rejecting.

**Independent audit summary (product_work_auditor):**
- Rerun confirmed: 86/86 tests pass (reproduced independently).
- Package is real: loads genuine frozen KB (sha256=893486e348210d65..., fragments=11); clean
  import boundary (zero spider_mem/runtime/arms/harness/analysis imports); no scientific or
  product-superiority claim leakage; capsule status hardcoded CANDIDATE; confidence labeled
  engineering (laplace_recency) score.
- **4 of 10 acceptance criteria NOT met as written** (tests loosened to match implementation):
  - F1 (high): freshness_decision() never returns UNKNOWN (RP3 hook non-functional);
    test_missing_last_verified_unknown asserts STALE instead of UNKNOWN.
  - F2 (medium): executor step_not_found returns STEP_NOT_FOUND, not precondition_mismatch
    as criterion names.
  - F3 (high): executor max_resets→exhausted unreachable for max_resets>=1 (dead code);
    test uses always-succeeding mock, passes vacuously.
  - F4 (medium): verify({}, snap) without nav_chain returns FAILED; verifier unusable for
    natural call signature without nav_chain.
  - F5 (medium): All PB-001 modules vendored (reimplemented inline) instead of importing
    authorized dependencies_to_import_from; deviation not disclosed; drift risk.
- Kill conditions: 0/4 triggered (no internal knowledge leak; thin-client not equivalent
  composability; <3 test failures; clean import boundary).
- Gate: **REVISE** (not BLOCKED; defects are localized fidelity mismatches, not architectural
  impossibility).

**Decision:** Authorize exactly one bounded repair package PW-CONSUMPTION-LAYER-001-REPAIR.

1. **Original request consumed:** PW-CONSUMPTION-LAYER-001 marked CONSUMED_SUPERSEDED. Candidate
   preserved at /tmp/spider_product_work (NOT integrated). Audit snapshot preserved at
   /tmp/spider_product_work_audit.
2. **Repair work request written:** `state/product_work_request_repair.json` with work_launch=true,
   work_id PW-CONSUMPTION-LAYER-001-REPAIR, 5 required fixes (F1-F5), same acceptance criteria
   as original request, constrained to product/consumption/ directory, no new files, max 500 LOC
   change, no changes to frozen PB-001 artifacts.
3. **Direction updated:** `state/product_direction.json` — work_launch=true, next_action=REPAIR,
   continue=true (for duration of repair package only), next_role=PRODUCT_ENGINEER.
4. **Kill conditions:** regression (new failures); modifying frozen artifacts; requiring
   architectural redesign; >2 test failures after repair.

**Negative evidence preserved (durable):**
- 4 of 10 acceptance criteria unmet as written on original completion.
- Freshness RP3 hook unreachable (always STALE, never UNKNOWN).
- Executor exhaustion path dead code for max_resets>=1.
- Verifier unusable without nav_chain for natural call signature.
- Vendored PB-001 logic drift-prone, hidden kb_frozen.sqlite procurement cost.
- Tests were loosened to match implementation rather than stated requirements (systematic
  fidelity gap between work-request criteria and Engineer test assertions).

**What this does NOT do:** Does NOT authorize a beta. Does NOT claim product superiority.
Does NOT modify frozen PB-001 artifacts. Does NOT require LLM backbone. Does NOT resolve
the endpoint availability escalation. Does NOT change any PH disposition.

**Dispositions unchanged:** PH-1 PROMISING (endpoint absent FIFTH consecutive verification
pending). PH-2 PROMISING (unlock(1) partial). PH-3 REJECTED permanent. PH-4 DORMANT.

**State writes:** `state/product_work_request_repair.json` (new), `state/product_direction.json`
(sixteenth session), this entry. continue=true for duration of repair package; returns to
WAIT_FOR_EVIDENCE on completion or kill. Zero outcome rows anywhere; no superiority or
comparative claim licensed by anything in this entry.

---

## Seventeenth Director session — 2026-08-27 — Review of PW-CONSUMPTION-LAYER-001 audit gate=REVISE; authorization of bounded documentation-fixes package

**Trigger:** User requested review of PW-CONSUMPTION-LAYER-001 after Engineer
status=READY_FOR_AUDIT and audit gate=REVISE. Candidate at
`/tmp/spider_product_work`; audit at `/tmp/spider_product_work_audit`.

**Independent audit summary (product_work_auditor, already issued):**
- 86/86 tests pass (reproduced independently).
- Package is real: genuine frozen KB (sha256 verified), 11 fragments, clean import
  boundary, no claim leakage.
- **4 REQ-FIX items** identified (differ from the 6th-session's 5 F-series findings):
  - REQ-FIX-A (high): conformance test computes violations but discards them —
    import boundary kill condition not verified.
  - REQ-FIX-B (high): execution engine incompatible with real session interface
    (target_sig vs int index). Only tested with mocks. Docstring falsely claims
    Playwright support.
  - REQ-FIX-C (medium): lane mechanisms vendored instead of imported. Faithful
    today but drift-prone.
  - REQ-FIX-D (low): thin-client kill condition #2 not evaluated.
- Gate: **REVISE** (not BLOCKED).

**Fresh-context critic consultation (charter duty, 4 critics):**

| Critic | Verdict | Key finding |
|---|---|---|
| cto_product | WAIT | Execution engine is wrong abstraction for standalone layer. 5-file thin client has equivalent effective capability. Do not repair engine; document ceiling. |
| product_system_architect | All fixes compatible | Proposed TargetSigAdapter for REQ-FIX-B (~120 LOC). Consensus overridden: adapter only consumable internally. |
| product_optimization_researcher | Selective repair | REQ-FIX-A + D HIGH value/LOW cost. REQ-FIX-B LOW value/HIGH cost (blocked by flip conditions). Accept ceiling. |
| product_baseline_performance_critic | Documentation path | ~30-45 LOC, ~2.5-4 hours vs adapter ~85-165 LOC, ~9-17 hours. Adapter has negative marginal value for external agents. |

**Convergent dominant finding adopted:** The execution engine's `target_sig → element
index` resolution requires internal snapshot-schema knowledge (react.py lines 232-264)
that the consumption boundary forbids. Building an adapter to runtime/session.py only
makes the engine consumable by SPIDER-internal agents, not the target external-agent
audibility. The 5-file thin client (registry+resolver+freshness+negative_knowledge+
capsule_schema) provides equivalent effective composability at half the LOC. The
economically rational action is to document the ceiling and repair the 3 cheap fixes.

**Negative knowledge recorded (durable):**
- Execution engine primitive resists agent-facing extraction at this maturity level:
  target_sig→element resolution requires internal snapshot-schema knowledge.
- Building an adapter to runtime/session.py only makes the engine consumable by
  SPIDER-internal agents, not the target external-agent audience.
- Tests were loosened to match implementation rather than stated requirements
  (systematic fidelity gap across both audits).

**Decision:** Authorize exactly one bounded documentation-fixes package
PW-CONSUMPTION-LAYER-001-DOC-FIXES.

1. **Prior requests consumed:** PW-CONSUMPTION-LAYER-001 and
   PW-CONSUMPTION-LAYER-001-REPAIR both marked CONSUMED_SUPERSEDED. Candidates
   preserved at /tmp/spider_product_work (NOT integrated). Audit snapshot preserved
   at /tmp/spider_product_work_audit.
2. **Doc-fixes work request written:** `state/product_work_request_doc_fixes.json`
   with work_launch=true, work_id PW-CONSUMPTION-LAYER-001-DOC-FIXES, 4 fixes
   (REQ-FIX-A: test assertion; REQ-FIX-B: docstring + limitations; REQ-FIX-C:
   deviation disclosure; REQ-FIX-D: measurement-only documentation), ~70 LOC max,
   no new files, no adapter build, no frozen artifact modifications.
3. **Direction updated:** `state/product_direction.json` — work_launch=true (new
   package), next_action=REPAIR, continue=true (for duration of doc-fixes only),
   next_role=PRODUCT_ENGINEER.
4. **Kill conditions:** regression; modifying frozen artifacts; building a
   TargetSigAdapter (violates kill condition #1); >2 test failures after repair.

**What this does NOT do:** Does NOT authorize a beta. Does NOT claim product
superiority. Does NOT modify frozen PB-001 artifacts. Does NOT require LLM backbone.
Does NOT build an execution engine adapter. Does NOT resolve the endpoint availability
escalation. Does NOT change any PH disposition.

**Dispositions unchanged:** PH-1 PROMISING (endpoint absent SIXTH consecutive
verification pending). PH-2 PROMISING (unlock(1) partial). PH-3 REJECTED permanent.
PH-4 DORMANT.

**State writes:** `state/product_work_request_doc_fixes.json` (new),
`state/product_direction.json` (seventeenth session), this entry. continue=true for
duration of doc-fixes package; returns to WAIT_FOR_EVIDENCE on completion or kill.
Zero outcome rows anywhere; no superiority or comparative claim licensed by anything
in this entry.
