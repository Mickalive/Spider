# TEAM GRAPH — program `graph-inheritance-generalization`, cycle 1 (repair round 1)
# GitHub run 32883457025 · Date: 2026-08-25

Realized decision-rule branch (frozen rule applied verbatim to raw rows):
**SITE-BOUND** — a bounded negative that completes the program's decision
horizon. The depth-≥4 memory-led composition advantage demonstrated by
G-H5 does NOT replicate on the BOOKS inventory under equalized conditions,
even after the documented books-side instrument defect was repaired through
legitimate producer-phase knowledge acquisition. The quotes-side stability
controls replicated G-H5 exactly. Nothing here rescues or weakens G-H5;
nothing here falsifies Physics; this bounds the product thesis "pay the
cost of novelty, not the cost of the whole task" to inventories whose
stored-knowledge descriptions actually address the consumer's subgoals.

Provenance chain (all preserved, none rewritten): rejected round-0 EMPTY
snapshot `3e36b4c` (= accepted base; branches `cycle/graph/32880179571/
team[-attempt-1]` untouched) · audit `CYCLE_32880179571_GRAPH` REVISE
RF-1..RF-5 · this repair's freeze commit `1a83311` (prereg BEFORE any
outcome; decision rule machine-diffed verbatim against
`directives/GRAPH.md`) · Amendment A1 commit `9cb851c` · Amendment A2
commit `96ec691` · P1 canonical execution + gates PASS + dry (this cycle)
· P2 raw rows `results/graph/generalization_live_runs.json` (84 rows,
batch attempt 1 canonical, zero retries).

## Repair round 2 (this snapshot; GitHub run 32900187567)

Independent audit CYCLE_32883457025_GRAPH returned REVISE
(documentation-only). Repaired here, text/metadata only: RF-D1 books
novel-cost range corrected with explicit population/unit (§3); RF-D2
suite totals replaced by recountable per-suite pytest counts (§4);
RF-D3 `prereg.freeze_commit` filled in
`results/graph/generalization_MANIFEST.json` (manifest-only commit);
RF-D4 the revalidation deviation now names the exact KB row (§4);
RF-D5 analyzer errata line added (§4). NO phase was rerun (forbidden by
the audit constraints); committed raw rows remain canonical; the
rejected round-1 snapshot is preserved verbatim at commit `a8fc785`
(`origin/cycle/graph/32883457025/team`).

## 1. What was measured (frozen design, executed exactly)

7 composites × 6 arms × 2 passes = **84 rows** (denominator unit: rows;
each cell = arm×composite×pass, n=2 passes):
- Carried VERBATIM (stability controls): D2Q [AUTH,PAGER], D3B
  [CAT-B,PAGER,OPENBOOK-B], D4B [CAT-B,PAGER,OPENBOOK-B,HOME-B],
  D4Q [AUTH,TAG,PAGER,HOME-Q], D5Q [AUTH,TAG,PAGER,HOME-Q,LOGOUT].
- NEW (books/historical-fiction region): D4H nominal depth 4
  [HF-CAT,PAGER,OPENBOOK-B,HOME-B]; D5B nominal depth 5
  [CAT-B,HF-CAT,PAGER,OPENBOOK-B,HOME-B]. Achieved-memory-depth classes
  are reported beside every nominal depth below.
- Arms (closed, G-H5-equalized: agentB, desc_only, allow_hints=False,
  oracle access after every action/application, MAX_APPLICATIONS=6,
  MAX_RESETS=2, seed=goalsig.SEED, byte-restored KB before EVERY run):
  frag_v31, frag_legacy, giter_v31, giter_legacy (inheritance);
  cold, traj (references).
- KB for every eval run: `generalization_growth_kb_dump.json.gz`
  (19 states / 29 transitions / 15 actions / 16 fragments = committed
  G-H5 grown base + producer acquisition), distinct store_before == 1
  across all runs, store_after == store_before everywhere, evaluation
  wrote NOTHING (final store == eval-start).

## 2. Decision-rule output (from `results/graph/generalization_analysis.json`)

- **No inheritance arm reached memory-led success on ANY books depth-≥4
  composite** (0 memory-led rows / 2 passes each on D4B, D4H, D5B —
  row convention; cells 0/1).
- All three books depth-≥4 composites are solvable-evidenced via the
  frozen attribution clause (reference success absent everywhere; recorded
  events carry reset/entry-mismatch chains: recoveries>0 with loads>=3 on
  inheritance rows).
- ⇒ **SITE-BOUND**, per the directive rule quoted verbatim in prereg §9.

### Quotes stability controls (equal prominence: these REPLICATED)

| composite | frag_v31 | frag_legacy | giter_v31 | giter_legacy | cold novel | traj novel |
|---|---|---|---|---|---|---|
| D4Q (nominal 4) | 2/2 rows memory-led (novel 1) | 2/2 (novel 1) | 0/2 | 2/2 (novel 3) | 57 | 49 |
| D5Q (nominal 5) | 2/2 rows memory-led (novel 4) | 2/2 (novel 4) | 0/2 | 2/2 (novel 3) | 76 | 65 |

All reference contrasts hold on every qualifying cell; quotes_stability_
holds=true; qualify_counts 2/2/0/2 — **identical pattern and identical
novel-cost ranges to G-H5** ("1–4 vs 49–76 / 49–65"). The stability
control therefore supports: the SITE-BOUND verdict is not an artifact of a
degraded harness — the same code, budgets and instruments reproduce the
accepted quotes result bit-stably (pass1==pass2 in 42/42 cells across the
whole batch, zero violations).

D2Q control: memory-led ONLY under frag_v31 (2/2; others partial) —
replicates the G-H5 D2Q caveat exactly.

## 3. Books side: where and why it fails (attribution, unit: row×subgoal-event)

- **ADDRESSING-MISS persists**: b.cat and b.home produce EMPTY candidate
  lists under desc_only retrieval for every frag arm (df-pruning strips
  the boilerplate tokens that auto-derived descriptions share; surviving
  tokens never reach MIN_MATCH=2 against the frozen confirm-instrument
  queries). Dry diagnostics (`generalization_dry_scores.json`, non-gating,
  committed pre-live) predicted precisely this shape: class@1 correct on
  only b.page2 among books positions.
- **Wrong-class binding persists at b.book/b.hfcat**: pager fragments rank
  above open-book/category candidates (cov 0.333–0.5 vs filtered-out),
  so replay binds the pagination skill onto open-book goals. This is the
  SAME mechanism signature recorded in G-H5.
- **The P1 application constraint changed the failure MODE, not the
  outcome**: `reset_target:"entry_state"` fired 20 times across the batch
  (e.g., D4B frag_v31 b.book: candidates=[generic.paginate.next,
  books.paginate.next], abort ["unresolved","a|||||next"], applications 5,
  re-entered the candidate's OWN recorded entry state). The destructive
  G-H5 drift into the ROOT catalogue (task-start rebinding) no longer
  occurs — but the candidate still ends retired, and the exploration
  fallback still cannot reach a product link within its DOM-order/wall
  budget (~52 sidebar elements precede main content; measured cold-row
  costs 132–147 novel actions). Equalized economics: references fail too
  (cold 0 memory-led anywhere on books; traj at most page-2).
- **giter arms get FURTHER by class count but never end-to-end**: e.g.
  D4H giter arms achieve 3 DISTINCT memory-solved classes
   [HF-CAT, OPENBOOK-B, HOME-B] yet stay partial — one position always
   falls to budget-exhausted exploration, so reused>novel end-to-end never
   materializes (RF-D1 corrected range; population = inheritance-arm rows
   on the four BOOKS composites D3B/D4B/D4H/D5B, row unit, both passes:
   giter rows reused 10–16 vs novel 60–120 — n=16 rows; all-inheritance
   books rows reused 3–16, novel 60–120 — n=32 rows. Recomputed from
   `generalization_live_runs.json`; no batch row has novel=136).

## 4. Mandated disclosures (audit RF-4; equal prominence)

- **giter_v31 equipment-transfer failure REPLICATES**: qualify_count=0
  again, on BOTH inventories' depth chains. Two independent cycles now
  agree the V31 edge-equipment transfer underperforms legacy edges.
- **Achieved pure-memory depth lags nominal EVERYWHERE**: quotes arms
  achieve ≤4 distinct classes vs nominal 5 (home/logout positions fall to
  exploration); books arms achieve ≤3 classes on nominal-4/5 composites.
  No new depth claim is licensed; G-H5's "≤4 classes" limit STANDS.
- **traj baseline representation loss** (applies to EVERY traj number
  above): the rebuilt KB carries raw page snapshots only for states touched
  by growth; base-dump states degrade to slug tokens, weakening site
  scoping. Books-side traj rows ran almost entirely on degraded
  representations; quotes-side traj rows likewise. No strong-RAG comparison
  exists.
- **Instrument roles beside every retrieval-related number**: the scaling
  confirm/dev instruments were used ONLY as frozen consumer-facing task
  text for carried composites (existing definitions, per the directive) —
  they are SPENT for quantitative claims and support none here; the ONE
  new key (b.hfcat) used a fresh isolated-authorship instrument
  (`paraphrases_generalization_{confirm,dev}.json`, prompts verbatim-
  committed; same-lab model-family authorship disclosed). NO quantitative
  retrieval/V31 claim is made anywhere in this cycle; dry diagnostics are
  prediction evidence only.
- **Denominators**: memory-led counts are rows/2 per arm×composite
  (row convention) and /1 cells (cell convention, n=2 deterministic passes
  = replication, NOT sampling uncertainty); attribution events are counted
  per row×subgoal-event; nothing is silently conditioned on success.
- **Latency/cost hygiene**: retrieval_us (perf_counter) fields recorded;
  NO latency/cost/wall-clock claim is made anywhere.
- **P1 amendment history** (full detail in prereg Amendments A1/A2;
  artifacts preserved under `results/graph/provenance/`): attempt 1
  aborted (producer tasks missing standard priors — stop rule DECLINED as
  false verdict with rationale); attempt 2 completed but its own binding
  gates FAILED (5-step multi-region category fragment; rehearsal
  contamination of evaluated chain positions) → A2 redesigned acquisition
  onto NON-EVALUATED instance regions (romance_8); canonical attempt 3:
  both tasks succeeded, **G1 zero violations, G2 zero adjacent-pair hits,
  G3 pass 16/16 fragments, whole-task absence over action records AND
  subgoal-end vectors, vacuity guard satisfied (wired non-empty telemetry)**.
- **Known deviations, disclosed** (RF-D4 exact-row wording): GB3r solved
  via memory replay of an existing pager candidate → the expected new sig
  `books.romance.paginate.next` was NOT created (manifest records
  expect-vs-got); the KB gained one new fragment
  (`books.romance.open.first.book`, dump id 16) and EXACTLY ONE stored
  fragment row changed: `goal_sig=generic.paginate.next`, `site=quotes`,
  dump id 10 — `success_count` 1→2 AND its auto-derived description
  token list refreshed by the same replay event — resolved during the
  BOOKS-region producer task GB3r_books_romance_page2 via legacy
  non-blind lookup (recorded memory event: candidates=
  [generic.paginate.next], solved_candidate=generic.paginate.next;
  producer context allow_hints=True, evaluation=False). Prereg §2's
  sentence "Quotes-side stored content is UNCHANGED by growth" therefore
  holds only up to the already-disclosed confidence/recency tie-break
  class at the letter level; quotes evaluation outcomes were nonetheless
  bit-identical to G-H5 (empirically inert for evaluation).
- **Suite status** (RF-D2 recountable per-suite pytest collection,
  verified in this sandbox at repair round 2): trap suite
  `tests/test_graph_generalization.py` **23**; scaling
  `tests/test_graph_scaling.py` **27**; cycle2 **15**; cycle3 **15**;
  robustness **10** — all green locally (67 legacy graph + 23 = 90
  green; playwright import surface stubbed offline, browser never
  launched). Integrity suite executed locally: 3 pass / 1 pre-existing
  Physics fixture failure (`tests/test_integrity.py::
  PhysicsLeakageGuardTests::test_true_previous_action_sequence_passes`)
  untouched provenance, reproduced identically on the accepted base
  tree.
- **Errata (RF-D5; analyzer frozen as-run)**: in
  `graph/analyze_generalization.py`'s attribution-event classifier the
  first disjunct clause is functionally redundant — Python operator
  precedence reduces the whole condition to `candidates == []` — so
  ADDRESSING-MISS classification and every committed analysis artifact
  are unaffected. No code change was made or permitted; the analyzer is
  byte-identical to snapshot `a8fc785` as-run.

## 5. Maximum-defensible wording (constitution ladder)

> Under the frozen preregistered rule (program
> `graph-inheritance-generalization`, one confirmatory cycle, 84 raw rows,
> batch discipline clean), the depth-≥4 memory-led composition advantage is
> **site-bound at the tested basis**: no inheritance arm achieved
> memory-led success on any preregistered BOOKS depth-≥4 composite in
> either pass, while the quotes stability family replicated the accepted
> G-H5 result exactly (qualify 2/2/0/2; contrasts 24/24-equivalent; novel
> 1–4 vs references 49–76). The books-side wall is attributable, from
> recorded events, to description-vocabulary addressing misses plus
> wrong-class candidate binding compounded by budget-bounded exploration —
> an inventory property of stored-knowledge descriptions, not a harness
> defect. This is a bounded negative at REPLICATION tier for the negative
> direction and REPLICATION tier for the quotes control; it licenses no
> cross-site skill claim, no addressing-solved claim, and no claim beyond
> two scripted demo sites, one grown KB, scripted deterministic consumers,
> and n=2 deterministic passes.

## 6. PENDING ledger wording (proposed; Director integrates — team never edits accepted history)

```
## G-H6 (Run 32883457025 repair round 1, executed 2026-08-25) — Inventory generalization: SITE-BOUND — PENDING Director integration

Status: PROPOSED (audit CYCLE_32880179571 REVISE RF-1..RF-5 repaired;
independent re-audit PENDING). Program graph-inheritance-generalization
completed at its decision horizon via the SITE-BOUND branch: after
legitimate producer-phase repair of the documented books instrument defect
(growth rerun with gate-driven contamination redesign, Amendments A1/A2,
all binding contamination gates passing pre-evaluation; unit-tested
entry-state application constraint replacing task-start rebinding), NO
inheritance arm (frag_v31, frag_legacy, giter_v31, giter_legacy) reached
memory-led success on ANY preregistered BOOKS depth->=4 composite (D4B,
D4H, D5B) in either pass, while the frozen quotes stability family
replicated G-H5 exactly (frag_v31/frag_legacy/giter_legacy qualify 2/2 on
D4Q/D5Q, giter_v31=0 again; arm novel 1-4 vs cold 57-76 / traj 49-65;
pass1==pass2 42/42 cells; distinct store_before=1; evaluation wrote
nothing). Attribution (recorded events): ADDRESSING-MISS empty candidate
lists (b.cat/b.home), wrong-class pager binding (b.book/b.hfcat), and
budget-bounded exploration fallback dominate; the entry-state constraint
eliminated the destructive root-drift failure mode (reset_target=
entry_state x20) without changing outcomes. Binding limits: two scripted
demo sites; ONE grown KB; achieved pure-memory depth <=4 classes vs
nominal 5 (quotes) and <=3 (books); traj baseline on degraded
representations; same-lab model-family third authorship for the one new
instrument key; n=2 deterministic passes; spent-instrument discipline
upheld (no quantitative retrieval/V31 claim); amendments A1/A2 were
pre-evaluation and fully provenanced. Provenance forever: round-0 EMPTY
snapshot 3e36b4c preserved (never a null); P1 attempts 1-2 artifacts
preserved including the gate-detected rehearsal-contamination lesson:
acquiring a skill BY WALKING an evaluated chain position contaminates
every composite containing that position (adjacent-pair rehearsal).
```

## 7. Evidence index

Prereg + amendments `graph/prereg_generalization.md` · tasks
`graph/tasks_generalization.py` · instruments/prompts
`graph/paraphrase_prompt_generalization_*.md`,
`graph/paraphrases_generalization_{confirm,dev}.json` · characterization
`results/graph/generalization_affordance_inventory.json` · growth driver
`graph/run_growth_generalization.py`; manifest/dump
`results/graph/generalization_growth_{manifest.json,kb_dump.json.gz}` ·
gates `graph/check_generalization_gates.py`;
`results/graph/generalization_gates.json` · dry
`graph/score_generalization_dry.py`; scores
`results/graph/generalization_dry_scores.json` · live driver
`graph/run_generalization_live.py`; raw rows
`results/graph/generalization_live_runs.json` · rebuild
`graph/rebuild_generalization.py` · analyzer
`graph/analyze_generalization.py`; analysis
`results/graph/generalization_analysis.json` · manifest
`results/graph/generalization_MANIFEST.json` · provenance
`results/graph/provenance/generalization_*{ABORTED_underpowered_tasks,
ATTEMPT2_hf_rehearsal_taint,ATTEMPT2_FAIL,p1_attempt1,p1_attempt2}*`.
