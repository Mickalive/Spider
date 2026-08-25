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
