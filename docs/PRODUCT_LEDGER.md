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
