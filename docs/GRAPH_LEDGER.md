# GRAPH LEDGER

## G-H1 (Run 1, 2026-08-23) — Cumulative inheritance proof of concept

- **Operational hypothesis**: storing validated state-action fragments with
  provenance/confidence lets later agents pay only novelty cost.
- **Implementation**: SQLite store + fragment replay + entry-state reset,
  live-site corpus across 4 sites, two scripted heuristic policies.

### Audited results

- Exact replay on the three tasks actually matched between cold and replay:
  **0 novel actions** on replay.
- Matched wall time: ~2.822 s cold vs ~2.816 s replay = **~1.002×**, therefore
  the original **8.5× wall-speedup claim is withdrawn**.
- Three selected composite tasks used 16 reused / 23 total actions = **69.6%
  reuse**. This is a composition proof of concept, not a general autonomous
  decomposition result.
- Run-1 confidence values are not valid evidence: audit found a positional
  INSERT bug placing a timestamp in `success_count` and `1` in `created`.
  Code is now corrected with invariants.

### What survives

- fragment replay can eliminate new decisions for known routes;
- fragment composition is operationally possible in the scripted setup;
- entry-state reset is a useful recovery mechanism;
- operational memory does not solve semantic search on huge unstructured pages.

### What remains unproved

- automatic decomposition of unseen natural-language tasks;
- model-to-model transfer;
- cross-site universal skills;
- calibrated confidence/half-life;
- a material wall-clock or monetary cost reduction with a real LLM in loop;
- superiority over strong trajectory-memory / nearest-route / graph baselines.

## G-H2 (Cycle 1 / Run 32676576613, 2026-08-24) — Blind composition on unseen tasks

- **Operational hypothesis**: content-derived fragment addressing lets
  later agents compose unseen tasks from accumulated knowledge WITHOUT
  hand-selected fragment identity — and beats strong memory baselines on
  matched tasks.
- **Evidence**: `results/graph/cycle2_20260824_021114.json` (+ exact
  replication `cycle2_20260824_021804.json`), analysis in
  `reports/graph/cycle2_blind_composition.md` (with post-audit Director
  relabeling section appended).
- **Audit**: `reports/audit/CYCLE_32676576613_GRAPH.md`,
  `results/audit/CYCLE_32676576613_GRAPH_FINDINGS.json`.
  Verdict: SAFE_TO_INTEGRATE_WITH_MANDATORY_RELABELING; grade
  ACCEPT_AS_POC / SURVIVES_AUDIT_WITH_LIMITS. The version below is the
  audited relabeling; the team's pre-audit wording remains in git history.

### Audited results (post-audit wording)

- Route absence verified programmatically before evaluation: no training
  attempt satisfies even two ADJACENT composite subgoals; composites absent
  as whole tasks; max fragment span 4 steps < any composite requirement.
  (audit C4: VALIDATED_FOR_CURRENT_TEST.)
- Consumers received NO goal_sig values, NO hints, NO ground-truth fill;
  evaluation mode wrote nothing; KB restored byte-identically before every
  eval run (1 distinct `store_before` across all 12 eval runs).
  (audit C6: VALIDATED_FOR_CURRENT_TEST.)
- **C2 (quotes login→page3): success, 6/6 reused actions, 0 novel,
  0 decision points** under desc+keyword retrieval.
- **C3 (quotes login→page5): success, 8/8 reused, 0 novel, 0 decision
  points** (iterated single-step pager fragment ×4). Stopping of the
  iterate-until-accept loop is ORACLE-guided by the benchmark acceptance
  predicate, not memory-driven.
- C1 partial: category UNKNOWN→exploration solved it; pager matched memory;
  named-book tail correctly stayed UNKNOWN and unsolved.
- Implemented baselines (single-shot graph-BFS without state revisits or
  self-loops and depth-capped at 6; verbatim nearest-trajectory replay;
  cold) solved 0/3 on identical KBs. Replication: statuses/solved_by/action
  counts identical across both runs AND across v4/v5 for all baseline rows.

### Mandatory claim limits from audit

- **Keyword channel**: eval queries were description + benchmark keywords
  (`explorer.py::_query_text`). Desc-only counterfactual scoring (auditor,
  independently reproduced by Director on the committed store dump)
  retrieves login fragments but returns NO candidates for every pager
  subgoal — df-pruning leaves {2,next,page} on quotes fragments, so
  desc-only pager queries match 1 pair < MIN_MATCH=2. The composed depth
  of C2/C3 currently DEPENDS on the keyword channel. Claims are limited to
  "desc+keyword retrieval" until a preregistered desc-only rerun.
- **Not "strong" baselines**: no-loop/single-shot variants only. Say
  "beat the implemented single-shot/no-loop baselines".
- **No fragment-layer-vs-graph attribution**: the decisive difference vs
  graphbfs is content addressing PLUS iterate-until-accept application,
  which BFS is denied by implementation. Requires loop-permitting
  iterative graph baseline with equalized accept-oracle before any
  representation-value claim.
- **Design freeze was NOT fully pre-registered**: v5 iterative-application
  semantics were adopted AFTER v4 outcomes (blind rows changed v4→v5:
  C2 7/8→6/6; C3 partial 8/27→success 8/8); mitigations verified
  (only fragment-replay mechanics changed; environment/baselines
  bit-identical). Status: REPLICATED_UNDER_FINAL_CONFIG, not preregistered.
- **X1 transfer row MEASUREMENT_INVALID**: acceptance predicate
  `url_frag="fiction"` substring-matched historical-fiction (committed
  store contains `historical-fiction_4/page-2.html` states from X1).
  X1 counts in no inheritance narrative. Substring predicates must be
  path-anchored before any future transfer run.
- **"auth-gated" withdrawn**: quotes listing pages are anonymously
  accessible (HTTP 200 probe by auditor and Director). These tasks involve
  form-auth composition plus iterated pagination on NON-gated pages.

### What survives

- blind content-addressed retrieval + oracle-guided iterative replay
  composes multi-step navigation on unseen routes without hand-selected
  fragment identity (REPLICATED x2 live runs, scripted scope);
- UNKNOWN stays UNKNOWN: unmatchable subgoals fall back to exploration and
  are reported as such; consumers never fabricate from ground truth;
- login-procedure reuse survives the desc-only counterfactual (the one
  genuinely descriptions-addressed piece);
- route absence, matched-KB discipline, write-suppression and provenance
  hygiene (validity map for invalid earlier versions) all audit-clean.

### What remains unproved / new limitations found

- descriptions-only addressing of pagination depth (keyword channel open);
- fragment-layer value over an equalized loop-permitting graph policy;
- robustness to paraphrase (eval descs are near-duplicates of training
  descs; scorer does not understand digits);
- ordinal goals unaddressable from post-state content (F2);
- category-level addressing brittle under df-pruning (F3);
- scripted policies only; no LLM consumer (G10 open);
- two small structured sites; no cross-site skill claim;
- confidence now has real failure counts but is still UNCALIBRATED (G8/G9);
- live-site health must be gated (the-internet skeleton-DOM incident, F4).

## G-H3 (Run 32689296167, executed 2026-08-24; repaired and re-audited via Run 32776369696) — E1–E4 preregistered batch — **INTEGRATED BY GRAPH LANE DIRECTOR (Run 32776369696)**

Status: INTEGRATED. Audit history: round-0 audit `CYCLE_32689296167_GRAPH`
(gate REVISE) found exactly one material defect — unreproducible denominators
in the E2 residual-value sentence (a success-conditioned login count mixed
with a cell-convention denominator; books-pager count covered only the
inherit arm; exact defective strings preserved in the audit reports).
Repair round 1 (team head
`2c585c1`, run 32776369696) applied RF-1..RF-3 as textual-only corrections;
the rejected snapshot `d467e02` is preserved provenance. Re-audit
`CYCLE_32776369696_GRAPH`: gate **PASS**, `safe_to_integrate=true`; every
corrected number independently recomputes from raw rows (Director recount on
the merged accepted tree confirms: fragment arms 16/16 rows = 8/8
condition×task cells; graphiter 0/8 rows = 0/4 cells; books pager 4/4 vs 0/2).
Nothing above this section is modified.

- **Design**: fully pre-registered (`graph/prereg_cycle3.md`, committed
  before ANY Phase-B outcome existed — first on prior run 32684818422
  which died pre-outcome with zero composite observations; adopted
  verbatim and executed under it on run 32689296167). Machine-enforced
  route absence; byte-restored identical KB for all 66 eval rows;
  evaluation consumers wrote nothing (transitions stayed 19); anchored
  predicates + health gate throughout; pass1↔pass2 bit-identical.
- **E1**: desc-only retrieval FAILS quotes pager subgoals (0/2 candidates,
  composites unsolved) → "keyword-assisted retrieval" remains the honest
  wording for composed depth; desc-only IS demonstrated for login
  procedures and books pagination. No tuning performed.
- **E2**: loop-permitting edge-multiset baseline (`graphiter`, equalized
  oracle/caps) MATCHES the fragment condition end-to-end on C2/C3 in all
  mode×pass cells (and beats it under desc_only) → cycle-1 advantage over
  graph baselines was the ITERATION POLICY, not fragment representation;
  stored transition edges alone suffice at this depth. Fragment residual
  value (row/cell convention, all eval rows regardless of end-to-end
  status): multi-step login packaging — fragment arms 16/16 rows = 8/8
  cells memory-solved vs graphiter 0/8 rows = 0/4 cells via edges — and
  books-pager lexical robustness under desc_only: inherit 2/2 + fragntr
  2/2 = 4/4 fragment-arm rows vs graphiter 0/2. `fragntr` shows iteration
  itself buys depth (C3 fails at depth 4 with single applications).
- **E3**: first semantic-addressing number: held-out paraphrase
  retrieval@1 = 2/8 positive goals (near-dup: 4/8 desc_only, 6/8
  desc_kw); expected-UNKNOWN discipline perfect (no false matches);
  live verdict-changing paraphrase probes reused 0 memory actions in 0/8
  rows. Addressing = near-verbatim matching + keyword channel.
- **X1 (valid rerun)**: anchored predicates clean; bounded transfer:
  fiction cat by exploration, page-2 by memory both modes, named tail
  correctly UNKNOWN/unsolved in 4/4 rows.
- Evidence: `results/graph/cycle3_20260824_043334_FINAL.json` (+ analysis,
  store dump), report `reports/graph/cycle3_e1_e4.md` (includes full
  provenance/incident disclosure: post-B-outcome driver crash repaired
  before any E3P observation; dry table recomputed bit-exactly from
  preserved DB). Audits: `reports/audit/CYCLE_32689296167_GRAPH.md` (REVISE,
  RF-1..RF-3), `reports/audit/CYCLE_32776369696_GRAPH.md` (PASS),
  gates in `results/audit/CYCLE_{32689296167,32776369696}_GRAPH_GATE.json`,
  repair recount `results/graph/cycle3_REPAIR_ROUND1_recount.json`.

### Mandatory claim limits carried from audits (binding wording constraints)

- **Scope**: single site pair (books/quotes toscrape); scripted
  deterministic policies, no LLM consumer; n=2 deterministic passes are
  replication against transient flakiness, NOT sampling uncertainty.
- **Attribution depth**: "iteration policy carries composed depth" holds at
  THIS composed depth with equalized accept-oracle and iteration/reset
  budgets only; no deeper or cross-site generalization is licensed.
- **Addressing**: keyword-assisted for quotes pagination depth; held-out
  paraphrase NOT survived (retrieval@1 2/8 both modes; live reuse 0/8);
  paraphrase authorship is same-lab model-family — addressing claims are
  bounded to this authorship class until independently re-tested.
- **Provenance limits (disclosed, accepted on disclosure)**: prior-run
  32684818422 zero-outcome status was not independently checkable by the
  auditor (immaterial: this run retrained its own KB and its own pre-outcome
  commit chain is verified); batch-time HTTP probes were lost in a crash and
  replaced by post-batch probes (`merge_note.probes_preflight_source`);
  per-row health gate fired clean in all 72 rows.
- **Denominator conventions (RF lesson)**: residual-value counts cover ALL
  evaluation rows of an arm regardless of end-to-end status, reported as
  rows and as condition×task cells (2 identical passes each); the
  "~150–151 decision points" for graphiter login fallback are WHOLE-ROW
  counts that also contain cheap edge-solved pager work — attribution to
  the exploration fallback is approximate ("~") and must not be quoted as a
  pure login cost.

## G-H4 (Run 32783797303, executed 2026-08-24) — Robust addressing family 1: SUCCESS at scope — **INTEGRATED BY GRAPH LANE DIRECTOR (Run 32783797303)**

Status: INTEGRATED. Program `graph-addressing-robustness`, repair round 1.
Audit history: round-0 audit `CYCLE_32782331702_GRAPH` (gate REVISE) found an
EMPTY production snapshot (no execution — explicitly NOT a null result); the
repair executed the predeclared R1/R2/R3 program in full; re-audit
`CYCLE_32783797303_GRAPH`: gate **PASS**, `safe_to_integrate=true`,
`required_fixes=[]`. Auditor recomputation reproduced every headline number
byte-exactly or row-exactly from committed raw artifacts; the Director's own
recount on the merged accepted tree confirms them (analyzer replay is
byte-identical; raw-row recount: R2LIVE 6/6 rows solved_by=memory with
reused==actions; R3 login memory frag 4/4 rows = 2/2 cells vs graphiter 0/4
and edgeseq 0/4 both exploration-only; edgeseq ~69 actions/row vs 6–13).
Nothing above this section is modified.

Accepted wording (maximum defensible, per team report §9 as validated by the
PASS audit):

> Under preregistered family 1 of descriptor/query constructions
> (program `graph-addressing-robustness`), arm V31 — a page-anchor pagination
> descriptor token (`page`+depth-digit ⇒ LIST) plus symmetric closed synonym
> canonicalization (GO/NEXT/CAT/LIST/AUTH/HOME), all cycle-3 thresholds
> unchanged — improves held-out paraphrase retrieval@1 from 2/8 to **6/8**
> positives-only with **zero** expected-UNKNOWN false accepts on a fresh,
> independently authored instrument, and all three mechanically selected
> verdict-changing probes were solved entirely from restored memory in both
> live passes on the audited frozen cycle-3 KB (6/6 probe×pass rows,
> reused==actions). R3: login packaging residual = validated procedural
> ordering (frag 4/4 login-memory rows; graphiter 0/4 exploration-solved;
> static ordered edge-unit replay 0/4 with bounce pathology).

### Mandatory integration limits (binding wording constraints, from PASS audit §5 / gate JSON)

- **SELECTION BIAS / SPENT INSTRUMENT (most important)**: V31's fresh-set 6/8
  is the predeclared DECISION OUTCOME for family 1 (BEST arm selected ON the
  fresh instrument among 13 eligible arms), NOT an unbiased estimate of V31's
  transferable retrieval@1. The fresh confirmatory set is SPENT: any future
  QUANTITATIVE claim about V31 or any successor descriptor/query construction
  requires a THIRD independently authored instrument under a new
  preregistration. Adoption of V31 as standard equipment for deeper-chain work
  is a licensed program decision, not established generalization.
- **Scope walls**: two scripted demo sites, one frozen KB, scripted
  deterministic consumers, same-lab model-family paraphrase authorship
  (instructional isolation only — not human-independent), n=2 deterministic
  passes = replication not sampling uncertainty, category addressing unsolved
  (df-pruning removes the CAT anchor site-wide on books; mechanically
  recomputed by auditor AND team), oracle-verified scripted replay semantics
  for "memory-solved"; no LLM-consumer/cross-model/cross-site/calibration/
  wall-clock claims.
- **R3 interpretation bound**: "validated procedural ordering" is a single-KB,
  single-rank-instantiation grid-line inference; no general packaging-quality
  claim beyond this scope without more sites/ranks.
- **Provenance forever**: run 32782331702 remains an EMPTY production snapshot
  (never cite it as a null result; its attempt branches stay untouched at
  `f42c14d`). The pilot live batch
  (`results/graph/provenance/*PILOT_driverbug*`) had an r3_frag non-blind
  driver defect, is EXPLORATORY provenance supporting no claim, and its
  bit-identical R2LIVE phase is recorded as an unplanned replication only.
- **Negative/null material carries equal prominence**: 10–11 of 11
  non-reference arms are marginal-or-null relative to V31/V33 on the dev set
  (descriptor-only enrichments alone move nothing); the effect is the
  CONJUNCTION of one content-derived descriptor rule with symmetric closed
  synonym canonicalization. The commit-message figure "9/11" in `4b4aa53`
  matches no consistent recount (correct: 10/11 counting V33, 10/10
  excluding it) — recorded by the audit as provenance noise; history not
  rewritten.
- **G4 unlocked but NOT executed** in this run; it requires its own
  preregistration (see successor program `graph-inheritance-scaling`,
  `directives/GRAPH.md`).
- **Hygiene for any future cost/latency claim**: `retrieval_ms` floors at
  integer ms in these runs; switch to `perf_counter` granularity before any
  latency claim (none is made anywhere in G-H4 evidence).

Evidence: `graph/prereg_robustness.md` (+ Amendment A1),
`graph/{score_variants.py,select_probes.py,analyze_robustness.py,
rebuild_store.py,run_robustness_live.py}`, `graph/dev_ledger_robustness.json`,
fresh instrument `graph/paraphrases_confirm_cycle4.json` (+ verbatim prompt),
raw scores/results `results/graph/robustness_{dev,confirm}_scores.json`,
`robustness_probe_selection.json`, `robustness_live_runs{,_store_dump}.json.gz`,
recount `robustness_analysis.json`, manifest `robustness_MANIFEST.json`;
report `reports/graph/robustness_repair_round1.md`; audits
`reports/audit/CYCLE_{32782331702,32783797303}_GRAPH.md` + gates
`results/audit/CYCLE_{32782331702,32783797303}_GRAPH_GATE.json`.
Freeze chain verified by commit timestamps: prereg `63768c9` → fresh
instrument `f8da2f9` → scorer/artifacts `2adbd52` → live code `dfb15ab` →
live outcomes; post-first-live-row code change limited to the disclosed
driver arm-config fix + guard assertion.

## G-H5 (Run 32861557668, executed 2026-08-25) — Depth scaling of memory-led composition: SCALING-HOLDS at a narrow basis — **INTEGRATED BY GRAPH LANE DIRECTOR (Run 32861557668)**

Status: INTEGRATED. Program `graph-inheritance-scaling`, cycle 1, same-cycle
recovery: round-0 team snapshot (run 32793580374, head `c952569`) was audited
REVISE (`CYCLE_32793580374_GRAPH`: decisive phase P2 never executed; vacuous
binding gate G1; crashing grown-KB rebuild path; missing dry-before-live,
analysis/report/manifest; provenance/suite discipline) with required_fixes
RF-1..RF-6; the repair round executed the previously-missing P2 exactly per
the frozen prereg; re-audit `CYCLE_32861557668_GRAPH`: gate **PASS**,
`safe_to_integrate=true`, `required_fixes=[]`, every RF verified by auditor
execution (rebuild round-trip clean; hook wired; G1 recomputed non-vacuously
with matching independent derivation; boundary clause rerun 15/15; freeze
chain intact; frozen artifacts empty-diff). The Director's own verification
on the merged accepted tree: fast-forward preserved every team commit hash
(`d41fe9b..db73549`); `analyze_scaling.py` replay regenerates
`scaling_analysis.json` byte-identically (sha256 match); rebuild round-trip
into a temp DB yields stats {16,27,15,15} with 2/2 raw blobs byte-identical
and the NULL-row contract holding. Nothing above this section is modified.

- **Design**: preregistered (`graph/prereg_scaling.md`, `a1d52fc`, committed
  before ANY growth outcome), closed 6-arm grid (frag/giter × V31/legacy +
  cold/traj references) fully equalized (oracle access after every action,
  MAX_APPLICATIONS=6, MAX_RESETS=2, identical fallback/seed/desc_only/
  agentB), third-authorship confirm instrument = THE evaluation descriptions
  (frozen `cbd0495` before growth), byte-restored grown KB before every run,
  60 rows (5 composites × 6 arms × 2 passes), zero unhealthy/error rows, no
  retries, pass1==pass2 in 30/30 cells, distinct store_before==1 across all
  eval runs, evaluation wrote nothing.
- Accepted wording (maximum defensible, per PASS audit §5 C4/C5):

> Under the frozen preregistered rule (prereg s9.1 applied verbatim to raw
> rows), program output is SCALING-HOLDS at a materially narrow basis: on
> the QUOTES depth chains D4Q and D5Q (nominal 4 and 5 DISTINCT stored
> fragment classes), three inheritance arms — blind fragment iteration with
> V31 standard equipment (`frag_v31`), legacy fragment iteration
> (`frag_legacy`), and loop-permitting edge iteration with legacy ranking
> (`giter_legacy`) — reached memory-led success (end-to-end success with
> reused>novel actions) in BOTH deterministic passes, paying 1–4 novel
> actions vs 49–76 for cold exploration and 49–65 for nearest-trajectory
> references on matched tasks (all 24 arm×task×pass reference contrasts
> hold; qualify_counts frag_v31=2, frag_legacy=2, giter_legacy=2,
> giter_v31=0).

### Mandatory integration limits (binding wording constraints, from PASS audit C4–C8 + report §9)

- **QUOTES-SIDE ONLY**: one composite family carries the entire positive
  result; BOOKS-side depth chains (D3B/D4B) were unsolved end-to-end by
  EVERY arm INCLUDING both references (`b.book` EXECUTION-FAIL: pager
  candidate present, its `a|||||next` step unresolvable on product pages),
  so books-side scaling is UNMEASURED — not falsified, not demonstrated.
- **Achieved pure-memory depth ≤4 classes vs nominal 5**: frag arms solve
  home/logout positions by EXPLORATION after empty candidate lists
  (ADDRESSING-MISSes predicted by the committed dry diagnostics);
  "nominal depth 5 was never covered end-to-end FROM MEMORY alone anywhere
  in this cycle."
- **Equipment-transfer negative**: `giter_v31` qualifies on NOTHING
  (frozen V31 edge-equipment transfer underperforms legacy edges);
  D2Q control is memory-led ONLY under `frag_v31`. No quantitative V31 or
  addressing claim licensed anywhere (G-H4 spent-instrument discipline;
  dry diagnostics are prediction evidence only, non-gating).
- **Baseline limits**: traj reference ran on a DEGRADED representation
  (14/16 grown-KB states carry no stored raw snapshot → slug tokens,
  weakened site-scoping); disclosed beside every traj number; the HOLDS
  status contrasts do not depend on the degradation, but no strong-RAG
  comparison exists at full fidelity.
- **Scope walls**: two scripted demo sites, ONE grown KB (16 states /
  15 fragments including the PRE-EXISTING duplicate name
  `generic.paginate.next` from the audited cycle-3 base — ≠15 distinct
  behaviors), scripted deterministic consumers, n=2 deterministic passes =
  replication NOT sampling uncertainty; oracle-verified scripted replay
  semantics for "memory-solved"; same-lab model-family third authorship
  (instructional isolation only); no LLM-consumer/cross-model/cross-site/
  calibration/wall-clock/latency/cost claims (`retrieval_ms` integer
  flooring supports none; `retrieval_us` hygiene-only).
- **Provenance forever**: rejected round-0 snapshot `c952569`
  (+ `origin/cycle/graph/32793580374/team[-attempt-*]`); growth sequence
  run1-crash / run2-prehostfix / canonical rerun preserved under
  `results/graph/provenance/`; post-prereg host-binding predicate amendment
  disclosed with zero-outcome-change evidence; first live launch killed by
  runner shell timeout at row 12 (INFRA_INTERRUPTED artifact preserved; its
  12 rows outcome-identical to canonical rows); residual limitation F-C:
  the live driver was committed together with its outputs, so execution-time
  driver identity is corroborated behaviorally (fixed ordering visible,
  exact cross-launch outcome identity), not provable from git alone.
- **Suite counts (C8)**: CI-reported 70 pass + 1 KNOWN pre-existing Physics
  fixture failure untouched since base `f42c14d`; not independently
  reproducible in the audit sandbox (no playwright/numpy) nor in the
  Director sandbox (same missing deps) — treat as UNVERIFIED-but-plausible
  until the next CI run on this branch.

Evidence: `graph/prereg_scaling.md`; instruments
`graph/paraphrases_scaling_{confirm,dev}.json` (+ verbatim prompts);
affordance inventory `results/graph/scaling_affordance_inventory.json`;
growth dump/manifest `results/graph/scaling_growth_{kb_dump.json.gz,manifest.json}`;
gates `results/graph/scaling_gates.json` (+ reconstruction
`scaling_subgoal_ends_reconstructed.json`); dry diagnostics
`results/graph/scaling_dry_scores.json` (committed pre-live); canonical raw
rows `results/graph/scaling_live_runs.json`; analysis
`results/graph/scaling_analysis.json`; manifest `results/graph/scaling_MANIFEST.json`;
report `reports/graph/inheritance_scaling_cycle1.md`; audits
`reports/audit/CYCLE_{32793580374,32861557668}_GRAPH.md` + gates
`results/audit/CYCLE_{32793580374,32861557668}_GRAPH_GATE.json`.

## G-H6 (Run 32900187567 integration; data executed 2026-08-25) — Inventory generalization: SITE-BOUND — **INTEGRATED BY GRAPH LANE DIRECTOR (Run 32900187567)**

Status: INTEGRATED. Program `graph-inheritance-generalization`, cycle 1,
completed at its decision horizon via the SITE-BOUND branch. Audit history:
round 0 of run 32880179571 was an EMPTY production snapshot (audit REVISE
RF-1..RF-5; explicitly NOT a null result; branches untouched at accepted base
`3e36b4c`); repair round 1 (run 32883457025, head `a8fc785`) executed the
full frozen program — prereg `1a83311` committed BEFORE any outcome,
pre-evaluation amendments A1/A2 with preserved attempt provenance, P1 growth
under gate-driven contamination redesign, P2 = 84 canonical raw rows — and
was audited REVISE for documentation-only defects RF-D1..RF-D5; repair round
2 (`87fbb06`→`7d1d350`→`9e6de6e`, run 32900187567) fixed exactly those five
with zero code/data/outcome changes (exhaustive diff verified by auditor);
re-audit `CYCLE_32900187567_GRAPH`: gate **PASS**,
`safe_to_integrate=true`, `required_fixes=[]`. The Director's own
verification on the merged accepted tree: raw-row recount reproduces every
load-bearing number (84 rows / 84 unique cells / batch attempt 1 canonical /
zero unhealthy; distinct store_before=1; store_after==store_before all;
final store {19,29,15,16}; memory-led 0/2 on D4B/D4H/D5B for ALL FOUR
inheritance arms; solvable-evidenced attribution rows present on all three
composites; quotes cells bit-identical to `scaling_live_runs.json` on all
36 compared cells; reference contrasts hold; giter books n=16 reused[10,16]
novel[60,120], all-inheritance books n=32 reused[3,16] novel[60,120]; batch
max novel=147 = a cold row; reset_target=entry_state ×20 with the exact
per-composite distribution); analyzer replay regenerates
`generalization_analysis.json` byte-identically (sha256 match); KB dump
delta vs the scaling-era dump is exactly one changed fragment row (id 10
`generic.paginate.next`@quotes success_count 1→2 + auto-derived description
refresh) plus one added romance fragment; suite counts verified locally:
trap 23 + scaling 27 + cycle2 15 + cycle3 15 + robustness 10 = 90 green,
integrity 3 pass + 1 pre-existing Physics fixture failure reproduced
identically on base `3e36b4c`.

Accepted wording (maximum defensible, per PASS audit §2/§4):

> Under the frozen preregistered rule (program
> `graph-inheritance-generalization`, one confirmatory cycle, 84 raw rows,
> batch discipline clean), the depth-≥4 memory-led composition advantage is
> **site-bound at the tested basis**: no inheritance arm achieved
> memory-led success on any preregistered BOOKS depth-≥4 composite in
> either pass, while the quotes stability family replicated the accepted
> G-H5 result exactly (qualify 2/2/0/2; contrasts holding; arm novel 1–4 vs
> cold 57–76 / traj 49–65; pass1==pass2 in 42/42 cells). The books-side
> wall is attributable, from recorded events, to description-vocabulary
> addressing misses plus wrong-class candidate binding compounded by
> budget-bounded exploration — an inventory property of stored-knowledge
> descriptions, not a harness defect. This is a bounded negative at
> REPLICATION tier for the negative direction and REPLICATION tier for the
> quotes control.

### Mandatory integration limits (binding wording constraints, from PASS audit §2 C2/C4/C5 + §4)

- **WEAK SOLVABILITY CLAUSE**: the attribution route is weak solvability
  evidence — NO policy INCLUDING references ever solved a books depth≥4
  composite end-to-end here or in G-H5. SITE-BOUND therefore bounds the
  *inheritance advantage* under the frozen equalized budgets
  (MAX_APPLICATIONS=6 / MAX_RESETS=2), NOT books-chain solvability itself.
- **Budget-scoped negative; scope walls travel with every citation**: two
  scripted demo sites; ONE grown KB; scripted deterministic consumers; n=2
  deterministic passes = replication NOT sampling uncertainty; oracle-
  guidance caveat travels with replicated quotes numbers; traj baseline ran
  on degraded representations (no strong-RAG comparison exists);
  same-lab model-family third authorship for the one new instrument key.
- **Achieved pure-memory depth ≤4 classes (quotes) / ≤3 (books)**: "no new
  depth claim; G-H5 ≤4 STANDS".
- **Equipment-transfer negative REPLICATED across both inventories**:
  `giter_v31` qualify_count=0 again. No quantitative V31/addressing claim
  licensed anywhere (spent-instrument discipline; dry diagnostics are
  prediction evidence only).
- **P1 amendment history is part of the record**: attempt-1 aborted
  (producer task-design slip, stop rule declined as false with rationale);
  attempt-2 binding gates FAILED on their own artifacts → Amendment A2
  redesigned acquisition onto non-evaluated instance region romance_8.
  Design lesson preserved forever: acquiring a skill BY WALKING an
  evaluated chain position contaminates every composite containing that
  position (adjacent-pair rehearsal). Attempt-2 contaminated artifacts
  remain under `results/graph/provenance/`.
- **Revalidation deviation disclosed**: GB3r solved via memory replay of an
  existing pager candidate — expected new sig `books.romance.paginate.next`
  was NOT created; KB gained one new fragment and EXACTLY ONE stored
  fragment row changed (id 10, quotes pager, success_count 1→2 +
  description-token refresh), empirically inert for evaluation (quotes
  outcomes bit-identical to G-H5). Prereg §2's "unchanged" sentence holds
  only at tie-break-class level.
- **Analyzer errata (frozen as-run)**: the attribution classifier's first
  disjunct is functionally redundant (condition reduces to
  `candidates == []`); ADDRESSING-MISS classification and committed
  artifacts unaffected; analyzer byte-identical to snapshot `a8fc785`.
- **Cross-attempt concatenation advisory (future preregistrations only)**:
  auditor's artificial concatenation of the two producer sessions' subgoal
  ends shows page2→book adjacencies for four composites — ruled
  NON-contamination under the frozen per-attempt rule (independent fresh
  sessions, fragments do not chain, risk direction pointed at the positive
  that did not occur); future preregistrations using multi-attempt growth
  must state explicitly whether cross-attempt concatenation is tested
  (now codified as `directives/AUDITOR_GRAPH.md` item 28).
- **Provenance forever**: rejected round-0 EMPTY snapshot `3e36b4c` (never
  cite run 32880179571 as a null result); rejected round-1 snapshot
  `a8fc785` preserved verbatim at
  `origin/cycle/graph/32883457025/team`; control-plane baggage commits
  (`e6c0798`, `87fbb06`) flagged for Meta-Director reconciliation per prior
  precedent.

Evidence: `graph/prereg_generalization.md` (+ Amendments A1/A2);
tasks/instruments `graph/tasks_generalization.py`,
`graph/paraphrases_generalization_{confirm,dev}.json` (+ verbatim prompts);
characterization `results/graph/generalization_affordance_inventory.json`;
growth driver/dump/manifest
`graph/run_growth_generalization.py`,
`results/graph/generalization_growth_{kb_dump.json.gz,manifest.json}`;
gates `graph/check_generalization_gates.py`;
`results/graph/generalization_gates.json`; dry diagnostics
`results/graph/generalization_dry_scores.json` (committed pre-live,
non-gating); canonical raw rows
`results/graph/generalization_live_runs.json`; analyzer/analysis
`graph/analyze_generalization.py`,
`results/graph/generalization_analysis.json`; manifest
`results/graph/generalization_MANIFEST.json`; report
`reports/graph/generalization_cycle1.md`; provenance artifacts under
`results/graph/provenance/generalization_*`; audits
`reports/audit/CYCLE_{32880179571,32883457025,32900187567}_GRAPH.md`
(first two via persisted audit branches) + gates
`results/audit/CYCLE_32900187567_GRAPH_GATE.json`.


## G-H7 (Run 32919200264 integration; data executed 2026-08-25/26) — Fused task+state-summary addressing: MEASUREMENT_INVALID (instrument-level retrieval-stack-void) + substantive nulls — **INTEGRATED BY GRAPH LANE DIRECTOR (Run 32919200264)**

Status: INTEGRATED. Program `graph-addressing-fused-retrieval`, cycle 1,
completed at its predeclared decision horizon (ONE confirmatory cycle;
horizon reached in EVERY branch). Audit history: round 0 of run
32905175867 (head `4426f40`, preserved verbatim at
`origin/cycle/graph/32905175867/team`) was audited REVISE RF-1..RF-5
(documentation/provenance-only defects); repair round 1 (`db17659`, run
32919200264) applied all five fixes with ZERO code/data/outcome changes
(exhaustive diff verified by auditor; recount artifact
`fused_REPAIR_ROUND1_recount.json` committed); re-audit
`CYCLE_32919200264_GRAPH`: gate **PASS**, `safe_to_integrate=true`,
`required_fixes=[]`. Freeze discipline verified by auditor git archaeology:
prereg + instruments + ALL mechanism/driver/analyzer code committed at
`05c049d` BEFORE any probe/screening/dry/confirm/live artifact; Amendment A1
pre-outcome; Amendment A2 pre-confirm (tau coverage-floor removal, both
procedures' full curves committed); selection on DEV only (alpha*=0.7,
fragile 22-vs-21 margin ledgered); exporter-defect first execution grid
preserved under `results/graph/provenance/`, never cited. The Director's own
verification on the merged accepted tree: fresh non-analyzer recount
reproduces every load-bearing number — gated primary C-vs-B informative-hard
0W/0R n=61; ungated hard@1 A_sig 53/64 / A_ft 0/64 / B_mmr 18/64 /
C_final 20/64 / D_random 16/64; paired ungated C-vs-B 3W/1R n=61; paired
ungated B-vs-random hard 14W/12L; coverage B 7/72, C 5/72 known rows with
zero false accepts on the single UNKNOWN qid family; validity precondition
under all four readings (literal gated HARD 0/64 vs 16/64 FAIL; literal ALL
0/75 vs 17/75 FAIL; all-ungated HARD 18 vs 16 PASS +2; all-ungated ALL 21 vs
17 PASS +4) with verdict invariant; battery gated dummy 2W/0R (drives
`battery_specific=false`) / ungated dummy 5W/6L perm 2W/3L sonly 6W/13L,
conclusion invariant under both conventions; execution grid 48 rows, pass
identity 24/24, memory-led A_strict 8/12 / A_std 8/12 / B 0/12 / C 0/12,
novel ranges A [0,14] vs text arms [64,103], signed medians over the 16
common cells C−B 0.0 / A_std−C −2.0 / A_strict−C −2.0, store digests equal
before/after on all rows with a single stats tuple {19,29,15,16}; economics
medians 314.5 / 329.0 / 1490.0 / 2949.5 µs with would-be LLM calls per C run
{3,4,5} max 5 counted separately from cache hits; analyzer replay regenerates
`fused_analysis.json` byte-identically (sha256 `0922b06d…`); manifest pins
20/20 match; tests locally verified fused suite 27/27 + full discovery 120
pass + the documented PRE-EXISTING Physics fixture failure reproduced
identically to the audited baseline.

Accepted wording (maximum defensible, per PASS audit §3, endorsing team §6):

> Under preregistered program `graph-addressing-fused-retrieval`
> (freeze commit 05c049d before any observation; fourth-authorship dev/
> confirm instruments, isolated same-lab authorship; accepted generalization
> KB byte-restored, no growth; 25 valid calibrated contexts; 75 retrieval
> query instances; 48 execution rows across 6 composites × 4 arms × 2
> deterministic passes, pass-identical 24/24), the cycle resolves
> MEASUREMENT_INVALID at the instrument level: the frozen validity
> precondition "embedding baseline exceeds the random null on the hard
> slice" fails under the literal output semantics on the hard slice
> (tau-gated B_mmr 0/64 vs ungated-by-construction random 16/64, n=64 hard
> instances; the all-instance aggregates 0/75 vs 17/75 are labeled
> aggregates, not hard-slice counts) and passes only by +2 hard-slice hits
> under an alternative all-ungated reading — an ambiguity created by the
> freeze, disclosed verbatim, not resolved post hoc. Substantively: with
> honest abstention thresholds the lexical-hash embedding stack (with or
> without state-summary fusion) retrieves almost nothing above absolute-
> score noise under paraphrase+entry-shift (ungated hard@1 B 18/64, C 20/64,
> random 16/64); fused scoring separates from task-text-only by at most
> 3 wins/1 reversal ungated and 0–0 gated; converts to ZERO median novel-
> action savings at matched subgoal success (16 common cells) against ~2×
> retrieval overhead per lookup; fails the state-specificity battery
> (constant-summary control matches its margin); and the exact goal_sig
> incumbent remains dominant wherever mapped signatures exist (memory-led
> end-to-end 8/12 composites at 0–14 novel actions vs 0/12 for text arms at
> 64–103). Fused task+state-summary addressing is NOT adopted into the
> Graph product path in this setting; exact addressing stays standard for
> signature consumers; no NL-consumer option is licensed by this evidence.

### Mandatory integration limits (binding wording constraints, from PASS audit §2/§4)

- **ANALYZER DENOMINATOR CLARIFYING CLAUSE (carried at integration per audit
  §2 residual observation 1)**: the verdict-driving
  `validity_B_clears_random_hard.passes` in `analyze_fused.py` consumed
  ALL-instance aggregates while prereg s8 role(iii) named the HARD slice.
  This is OUTCOME-INVARIANT — the auditor's four-way recount proves the
  literal reading fails under BOTH denominators (0/64-vs-16/64 AND 0/75-vs-
  17/75) and passes only under all-ungated readings (+2 hard / +4 all). The
  citable report layer is denominator-correct after repair round 1; the
  analysis JSON discloses both readings. Frozen post-outcome code was NOT
  touched for zero information gain. Successor analyzers must compute
  frozen statistics exactly as written and label denominators inside
  analysis blocks too (codified as `directives/AUDITOR_GRAPH.md` item 29).
- **Instrument-level status travels**: MEASUREMENT_INVALID is instrument-
  level (retrieval-stack-void) and does NOT falsify the mechanism outside
  this setting; it is NOT environment instability (health gates never fired
  on canonical runs; two earlier whole-pass calibration attempts died to
  runner shell timeouts before any completed probe pass = INFRA_INTERRUPTED
  provenance), so the lane was correctly NOT BLOCKED.
- **Scope walls travel with every citation**: two scripted demo sites; ONE
  16-fragment KB (small-library regime; pool M=20 ≥ N makes MMR diversity
  inert); lexical-hash embedder and deterministic summarizer regimes only
  (neural/LLM survival OPEN but untestable via another scorer comparison on
  this KB — the design lesson frozen below); single UNKNOWN qid family sets
  the FA gate; same-lab model-family instrument authorship (NOT human-
  independent); n=2 deterministic passes = determinism only; µs fields are
  perf_counter hygiene-only — NO latency/wall-clock claim licensed anywhere
  (integer-truncated report prints 315/2949 vs stored 314.5/2949.5 noted as
  cosmetic).
- **Adoption decision is final for this program**: fused addressing NOT
  adopted; exact goal_sig stays standard for signature consumers; NO
  NL-consumer option licensed by this evidence. Summarizer survival
  UNRESOLVED (battery non-separating under both output conventions);
  embedder survival untested.
- **Design lesson frozen (drives successor program)**: the discriminating
  residual is NOT scorer choice — on weak keys in a saturated pool every
  scorer variant lands near chance and near each other. Observed failures
  are instances of (i) auto-derived descriptions too weak as keys
  (open-book `'a|||||'` first-match binding; category vocabulary) or (ii)
  N≤M pool saturation. Rerunning scorer variants on this KB cannot change
  the answer. Any description-induction/scale successor needs its OWN
  preregistration and FRESH instruments (opened as program
  `graph-addressing-key-induction`; see `directives/GRAPH.md`).
- **Provenance errata carried**: cross-phase calibration/truth-set self-pin
  is `235834e82810c36f0f97a63504d8cb60c3da4ef72f092df3406aa721c0c81e77`
  (sha256 over canonical sort-keys JSON of the calibration metadata,
  recorded in `fused_truth_sets.json` field `self_sha256_input` and
  independently recomputed during repair round 1;
  `calibration_self_sha256=null` in BOTH selection and confirm artifacts due
  to a gzip-wiring defect — drivers read from the calibration gzip which
  lacks the field; errata recorded in `fused_MANIFEST.json` notes[] and
  report §5 item 5; until a successor regenerates artifacts, cross-phase
  binding rests on this errata plus the manifest pin `489631af…`).
- **Unexercised early-stop clause (labeled deviation)**: prereg s9's economy
  clause (restrict execution to A-regression cells once retrieval
  separation failed) was NOT exercised; the full 48-row grid ran anyway —
  CONSERVATIVE direction, extra rows are additional evidence AGAINST the
  candidate; no outcome or verdict depends on it.
- **Provenance forever**: rejected round-0 snapshot `4426f40` preserved
  verbatim at `origin/cycle/graph/32905175867/team` (REVISE RF-1..RF-5;
  never cite its numbers outside labeled provenance); exporter-defect first
  execution grid preserved under `results/graph/provenance/` (never cited);
  INFRA_INTERRUPTED ×2 calibration attempts documented; shared-infra
  divergence `shared/browser.py` additive opt-in `Session.new_context()`
  flagged lane-local pending Meta-Director reconciliation per constitution s5.

Evidence: `graph/prereg_fused_retrieval.md` (+ Amendments A1/A2); instruments
`graph/paraphrases_fused_{dev,confirm}.json` + verbatim prompts
`graph/paraphrase_prompt_fused_{dev,confirm}.md`; mechanism
`graph/fused_retrieval.py` + eval engine `graph/fused_eval.py`; tasks
`graph/tasks_fused.py`; drivers `graph/run_fused_calibration.py`,
`graph/screen_fused_dev.py`, `graph/run_fused_retrieval_confirm.py`,
`graph/run_fused_live.py`; canonical artifacts
`results/graph/fused_{calibration.json.gz,truth_sets.json,dev_selection.json,retrieval_confirm.json,live_runs.json}`;
analyzer/analysis `graph/analyze_fused.py`,
`results/graph/fused_analysis.json`; manifest
`results/graph/fused_MANIFEST.json`; repair recount
`results/graph/fused_REPAIR_ROUND1_recount.json`; report
`reports/graph/fused_retrieval_cycle1.md`; provenance artifacts under
`results/graph/provenance/fused_*`; audit
`reports/audit/CYCLE_32919200264_GRAPH.md` + gate
`results/audit/CYCLE_32919200264_GRAPH_GATE.json`.


## G-H8 (Run 32936040591 integration; data executed 2026-08-26) — Key-layer induction (keys-vs-scorer contrast): INDETERMINATE_BELOW_FLOOR at frozen power + report-all negatives — **INTEGRATED BY GRAPH LANE DIRECTOR (Run 32936040591)**

Status: INTEGRATED. Program `graph-addressing-key-induction`, cycle 1,
completed at its predeclared decision horizon (ONE confirmatory cycle;
horizon reached in EVERY branch). Audit history: round 0 of run
32925866227 (head `4fb87c0`, preserved verbatim at
`origin/cycle/graph/32925866227/team`) was audited REVISE RF-1..RF-5
(invalid sign-test p-values from a smaller-side tail inversion; four-way
recount population mislabeling; an undisclosed post-freeze metadata-only
driver fix; an undisclosed reference-arm scope divergence; recount parity
blind to p-values) — NONE verdict-driving, and the buggy statistic
participated in NO selection decision. Repair round 1 (`7fb8ecc`, run
32936040591) applied all five fixes against BYTE-IDENTICAL raw evidence
(raw sha256 pins unchanged); re-audit `CYCLE_32936040591_GRAPH`: gate
**PASS**, `safe_to_integrate=true`, `required_fixes=[]`. Freeze discipline:
prereg + fifth-authorship instruments + ALL code committed at `9108ba3`
BEFORE any calibration/screening/confirm/live artifact; truth sets
BIT-IDENTICAL to accepted G-H7 on all 25 qids (zero site drift);
selection-once enforced; item-29 analyzer parity correction disclosed
pre-report in the conservative direction only. The Director's own
verification on the merged accepted tree with fresh non-analyzer code:
slices 75 total / 64 hard / 61 informative-hard; PRIMARY tau-gated paired
B_keys-vs-A_keys informative-hard **10W/0R decisive=10 < pre-declared floor
15 → INDETERMINATE_BELOW_FLOOR** (declared-direction exact tail p=0.000977;
separates predicate d≥15 ∧ p≤0.05 ∧ wins>rev = False; prereg s8 routes
below-floor to INDETERMINATE, never falsified); SECONDARY all-ungated ih
10W/9R d=19 declared p=0.500000 EXACTLY chance (opposite tail 0.676197);
four-way LITERAL grids gated_hard W10/R0 d10 · gated_all W12/R0 d12
p=0.000244 · ungated_hard W10/R9 d19 · ungated_all W13/R10 d23 p=0.338820;
arm ungated hard@1 A_sig 51 / A_ft 0 / A_keys 30 / B_keys 31 / D_random 16
(of 64); validity precondition A_keys 30 > random 16 PASS; zero
expected-UNKNOWN false accepts both text arms at tau*=0.25 (single
q.tagp2@Q_ROOT family, n=3); recall@pool == library 61/61 all three arms
(pool saturation makes candidate recall non-discriminating); projections
AFF 25 / ENTRY 15 / EFF 26 of 61; per-cluster cells reproduced exactly on
informative-hard populations (gated CATEGORY/PAGER 5W/0R d5 p=0.03125 each;
ungated PAGER 8W/0R p=0.003906 offset by AUTH/CATEGORY 0W/2R — no cluster
pooled into any claim); execution grid 48 rows zero errors, pass identity
24/24, kb {19,29,15,16} equal pre/post ×48, would-be LLM calls ≡ 0 BY
CONSTRUCTION; conversion B−A median −0.0 over 19 commonly solved cells
(ZERO), regression medians A_std−B and A_strict−B = −1.0 (incumbents pay
FEWER novel actions), memory-led end-to-end A_strict 8/12 / A_std 8/12 /
A_keys 0/12 / B_keys 0/12; economics retrieval_us medians 332.5 / 320.0 /
1650.0 / 1509.5 µs hygiene-only; manifest pins 29/29 verified incl.
rejected-round-0 provenance pins; rules_hash b76e3726… recomputed
byte-equal; instrument pins match files and prereg s5 verbatim; DEV screen
K_aff 26/61 K_reg 28/61 K_full 31/61 vs baseline 35/61 (argmax→K_full,
selection-once), oracle diagnostic 41/61 (~6-row stack ceiling above
baseline), duplicate-key geometry collapse real (median top1–top2 margin →
0.0 for K_reg/K_full; pairwise cos>0.9 tail 2→6); keys suite 23/23 PASS +
full suite 143 passed + the documented PRE-EXISTING Physics fixture failure
identical to the audited baseline.

Verdict wording (maximum defensible): under the frozen lexical-hash+MMR
machinery held IDENTICAL to the G-H7 baseline arm, mechanically induced
richer keys (rules v1, DEV-selected K_full) did NOT demonstrate separation
from auto-derived descriptions — primary below its pre-declared decisive-
pair floor (INDETERMINATE, never falsified; directionally positive at
undecidable power), secondary ordering EXACTLY chance, ZERO execution
conversion at matched subgoal success, exact goal_sig incumbent dominant.
**Induced keys rules v1 are NOT adopted; keys stay auto-derived; no
NL-consumer option is licensed; exact addressing stays standard for
signature consumers.** Mandated attribution: candidate generation EXCLUDED
(recall@pool full), bad-ordering dominant ungated, embedder/stack ceiling
~6 informative-hard rows above baseline even under task-aligned oracle
keys, duplicate-key geometry collapse real. Design lesson frozen: at this
16-fragment library scale the discriminating residual lives BELOW the key
layer (embedder/representation ceiling), not in scorer choice (G-H7) nor
key construction (G-H8); any re-ask requires a larger-library substrate,
fresh instruments and its own preregistration.

Binding limits traveling with any citation: two scripted demo sites; ONE
16-fragment KB (N ≤ pool M makes recall@pool trivially saturated);
lexical-hash embedder regime ONLY; scripted deterministic consumers;
same-lab model-family fifth-authorship instruments (process-attested
isolation); n=2 deterministic passes = determinism only; µs fields
hygiene-only, NO latency claim; single expected-UNKNOWN qid family sets the
FA gate; INDETERMINATE is statistic-level AT THIS SETTING and does not
falsify key induction elsewhere; reference arms A_sig/A_ft ranked unscoped
(site-scoped-equivalent A_sig hard@1 = 53/64 via faithfulness-gated offline
recount; flipped rows exactly q.rootpager@Q_ROOT_AUTH p1/p2) and are
non-comparable to G-H7 numbers without that label; DEV screening numbers
are decision-procedure outputs, not unbiased estimates.

Provenance forever: rejected round-0 snapshot `4fb87c0` preserved at
`origin/cycle/graph/32925866227/team`; rejected derived artifacts pinned
under `results/graph/provenance/*REJECTED_ROUND0*`; INFRA_INTERRUPTED ×2
chunk events (zero row loss) disclosed; post-freeze pool_ids driver fix
(b80394d) disclosed report+manifest.

Evidence: `graph/prereg_key_induction.md`; instruments
`graph/paraphrases_keys_{dev,confirm}.json` + verbatim prompts; mechanism
`graph/induced_keys.py` + eval engine `graph/keys_eval.py` + tasks
`graph/tasks_keys.py`; drivers `graph/run_keys_calibration.py`,
`graph/screen_keys_dev.py`, `graph/run_keys_retrieval_confirm.py`,
`graph/run_keys_live.py`, `graph/keys_tiesensitivity.py`; analyzer/recount/
claims `graph/{analyze_keys,recount_keys,make_claim_tables,
make_keys_manifest}.py`; canonical artifacts `results/graph/keys_*`;
rejected-round-0 provenance under `results/graph/provenance/keys_*`; report
`reports/graph/key_induction_cycle1.md`; audit
`reports/audit/CYCLE_32936040591_GRAPH.md` + gate
`results/audit/CYCLE_32936040591_GRAPH_GATE.json`.


## Open questions carried forward

- ADDRESSING ROBUSTNESS (decided AT SCOPE by G-H4): closed-class lexical
  descriptor/query construction survives held-out paraphrase at the tested
  bar. Still OPEN inside addressing: category-level goals (CAT anchor killed
  by df-pruning — candidate Family-2 mechanism must go through new
  preregistration); generalization beyond the same-lab model-family
  authorship class (requires third independent instrument); any quantitative
  re-measurement of V31 (fresh set spent).
- G4 DEEPER CHAINS (DECIDED AT SCOPE by G-H5, then G-H6): memory-led
  composition survives nominal depth 4–5 on the quotes inventory with 1–4
  novel actions vs references (G-H5); the depth-≥4 advantage is SITE-BOUND
  at the tested basis — it did NOT replicate on the BOOKS inventory after
  legitimate instrument repair (G-H6), with attribution to
  description-vocabulary addressing misses, wrong-class pager binding and
  budget-bounded exploration. Residual scope limits: weak solvability
  clause (no policy ever solved a books chain end-to-end); budget-scoped;
  two demo sites; achieved pure-memory depth ≤4 classes.
- ADDRESSING MECHANISM (DECIDED IN-SETTING by G-H7, program
  `graph-addressing-fused-retrieval` COMPLETE): the audited Intel R-1 fused
  task+state-summary recommendation did NOT survive store-integrated
  adoption testing — MEASUREMENT_INVALID instrument-level plus substantive
  nulls; NOT adopted; exact goal_sig stays standard; no NL-consumer option
  licensed (see G-H7 above for binding limits). Intel's isolated-harness PoC
  remains evidence for the Intel lane only.
- KEY/DESCRIPTION LAYER (DECIDED AT FROZEN POWER by G-H8, program
  `graph-addressing-key-induction` COMPLETE): mechanically induced richer
  keys did NOT demonstrate separation from auto-derived descriptions under
  the identical frozen machinery — primary below its pre-declared decisive-
  pair floor (INDETERMINATE, never falsified, directionally positive at
  undecidable power p=0.000977 with only 10 decisive pairs), secondary
  ordering exactly chance (p=0.5), zero execution conversion, exact goal_sig
  incumbent dominant. Rules v1 NOT adopted. Attribution localizes the
  residual BELOW the key layer: stack ceiling ~6 informative-hard rows above
  baseline even under oracle keys; duplicate-key geometry collapse real.
  Any re-ask of the key-layer/scorer question requires a larger-library
  substrate plus fresh instruments under its own preregistration (audit
  residual observation carried).
- KNOWLEDGE-FORM LAYER (LAUNCHED by Director Run 32936040591 as successor
  program `graph-procedure-compilation`, `directives/GRAPH.md`; CTO-6
  authorization): the untested lever after two retrieval-stack programs —
  compile committed transition dumps into ordered browser-primitive-level
  procedures consumed directly, attacking the G-H6 books site-bound failure
  (budget-bounded exploration attribution) and the login procedural-ordering
  residual (4/4 vs edge-replay 0/4). Offline P0 grid with contamination
  tests OVER COMPILED PROCEDURES + cross-attempt clause; cheap
  FALSIFIED-IN-SETTING completion branch if no rule compiles valid,
  contamination-clean procedures for any currently-failing composite class;
  conditional single live confirmatory cycle behind NUMERIC power/supply
  arithmetic verified pre-freeze (G-H8 floor lesson made mandatory);
  no-silent-substitution pass/fail gate; shuffled-order + edge-replay strong
  nulls for the ordering claim; fresh proc-dev/confirm-6a instruments.
  Intel R-2 route records stay QUEUED behind this program's reconciliation
  clause (browser-primitive procedures ≠ HTTP route records; zero artifact
  overlap).
- EXTERNAL RECOMMENDATION QUEUED (Intel lane, audited): R-2 "route records
  as APIs/direct-routes execution layer behind a store flag" (Intel audit
  run 32873081963, VALIDATED_USEFUL, PROOF-OF-CONCEPT ceiling; cycles 6–7
  add audited observation-tier design constraints: equivalence policy is a
  design decision, content-type filter blind spots, mechanical
  instrumentation preconditions, restful-booker persistent write refusal,
  POWER ARITHMETIC MUST APPEAR IN PREREG). Its previously suggested fused-
  scoring addressing arm is DEAD-IN-SETTING after G-H7 unless revived by its
  own successor preregistration; the exact-intent vs prefix-inheritance
  contrast remains testable and carries Intel's curl-null boundary. It may
  become a Graph program ONLY under its own preregistration with Intel's
  binding caveats traveling with any claim; it is NOT evidence in this lane
  until tested here.
- G5/G6 semantic identification of known vs novel task portions (LLM pilot
  against the scripted scorer);
- G7 known-API replacement of browser routes;
- G8/G9 prospective confidence/staleness calibration using recorded
  failure events;
- G10 true cross-model consumption;
- G12 exploration-cost-vs-knowledge curve over >=20 sequential agents/tasks
  under natural-growth conditions with valid predicates.

Active instructions are controlled by `directives/GRAPH.md` and may be updated
by the GRAPH LANE DIRECTOR after each audited cycle.
