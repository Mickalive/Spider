# GRAPH CYCLE 1 — PROGRAM `graph-inheritance-scaling` (repair round 1)

- GitHub runs: team snapshot run **32793580374** (round 0, REJECTED, preserved
  at `c952569` / `origin/cycle/graph/32793580374/team[-attempt-*]`); repair
  round executed on top of it. Independent audit:
  `reports/audit/CYCLE_32793580374_GRAPH.md` +
  `results/audit/CYCLE_32793580374_GRAPH_GATE.json` (REVISE, RF-1..RF-6).
- Prereg: `graph/prereg_scaling.md` (`a1d52fc`, frozen BEFORE any growth or
  evaluation outcome). Instruments frozen at `cbd0495` BEFORE any growth run.
- This report covers the SAME scientific cycle after repairing the audited
  defects and executing the previously-missing decisive phase P2.

## 0. Headline

**Decision-rule output (prereg s9.1, applied verbatim to raw rows):
SCALING-HOLDS — with a materially narrower basis than the headline word
suggests.** On the two QUOTES depth chains, three inheritance arms
(`frag_v31`, `frag_legacy`, `giter_legacy`) reached memory-led success
(end-to-end success with reused>novel) on BOTH passes of D4Q (depth 4) and
D5Q (depth 5), and all 24 cold/traj reference contrasts hold (cold novel
57/76; traj novel 49/65 vs arm novel 1–4). **Equal-prominence negatives:**
the BOOKS depth chain did not collapse gracefully — it was unsolved
end-to-end by EVERY arm including both references (D3B/D4B all partial;
`b.book` fails everywhere), `giter_v31` qualifies on NOTHING (equipment
transfer map underperforms legacy edges), achieved MEMORY depth is only
3 of 4–5 nominal classes (frag arms solve home/logout subgoals by
exploration because retrieval returns EMPTY candidate lists), and the D2Q
control is memory-led ONLY under `frag_v31`. One composite family
(quotes-side) carries the entire positive result.

Unit conventions below follow audit item 22 strictly.

## 1. Repair-round provenance (what changed since the rejected snapshot)

| Audit item | Fix | Evidence |
|---|---|---|
| RF-1 rebuild crash | `graph/rebuild_scaling.py` states INSERT binds decoded raw blob (7 placeholders/7 values); round-trip test asserts stats {16,27,15,15} + byte-identical blobs for the 2 growth states | commit fc94e5a; `RebuildRoundTripTests` |
| latent `Store.state_raw` NULL crash | found during first-ever traj-arm execution over a rebuilt KB ((None,) truthiness); fixed to return None; unit-tested | same commit |
| RF-2 vacuous G1 | hook wired into Explorer in `run_growth_task`; produced-attempt invariant `len(subgoal_ends)==subgoal_rows` tested (incl. carryover); deterministic reconstruction from committed marker matrix (`graph/reconstruct_subgoal_ends.py`) feeds G1 marked `recomputed:true`; zero violations (matches auditor's independent recount); growth NOT re-executed | commit fc94e5a; `SubgoalHookWiringTests`, `ReconstructionTests` |
| RF-3 missing boundary clause | implemented pre-eval-row: all 15 fragments replayed over recorded transition multigraph; node regions from RECORDED growth vectors else URL+auth-trace surrogate; crossings = phase transitions of non-empty region sets; binding max<=1 → PASS 15/15 (logout fragment exactly 1 boundary via recorded evidence) | `scaling_gates.json` regenerated; `BoundaryReplaySyntheticTests` |
| RF-4 dry-then-live | s7 dry diagnostics committed (`2b66cd5`) BEFORE any live row; then full frozen grid executed (`d98f040`) | `results/graph/scaling_dry_scores.json`, `scaling_live_runs.json` |
| RF-5 analysis/report/manifest | this report + `graph/analyze_scaling.py` + `results/graph/scaling_MANIFEST.json` | this cycle |
| RF-6 suite/provenance | scaling suite 27 green; full suite 70 pass + 1 KNOWN pre-existing Physics fixture failure (`tests/test_integrity.py::PhysicsLeakageGuardTests::test_true_previous_action_sequence_passes`, untouched since base f42c14d — verified by empty diff f42c14d..HEAD on physics/) | CI log |

Frozen artifacts (prereg, instruments, growth dump, growth manifest)
received NO edits — additive new files only; `scaling_gates.json` is
regenerated output explicitly marked with `repair_round_note`.

## 2. Execution provenance (disclosure duty)

- Growth sequence (unchanged from round 0): run1 dump-serialization crash →
  run2 completed under pre-hostfix predicates → canonical rerun byte-identical
  KB outcomes. Artifacts preserved under `results/graph/provenance/`
  (`scaling_growth_run1_crash_dumpdb.db`,
  `scaling_growth_run2_prehostfix_*`). The host-binding predicate amendment
  was post-prereg but ZERO-outcome-change (run2-vs-canonical diff: identical
  statuses/actions/stats; only 5 cross-site false-positive D4B|eval.b.home
  marker cells flipped true→false).
- Pre-existing duplicate fragment name `generic.paginate.next` (ids 3 books /
  10 quotes) comes from the AUDITED cycle-3 base, not from growth; "15
  fragments" ≠ 15 distinct behaviors.
- THIS repair round: first live-batch launch was killed mid-D2Q by the runner
  shell timeout (browser-driver EPIPE; infrastructure, not experiment
  outcome). Its 12 rows are preserved as
  `provenance/scaling_live_runs_INFRA_INTERRUPTED_20260825_infra_interrupted.json`;
  no mechanism code changed between launches; the canonical batch is one
  complete clean 60-row execution.
- Freeze-timing: prereg (a1d52fc) → instruments (cbd0495) → pre-outcome code
  (6105fcc) → growth outcomes → repair fixes+tests (fc94e5a) → dry scores
  (2b66cd5) → FIRST canonical live row → analyzer written while later batch
  rows accumulated (analysis-only code, implements the FROZEN s9 text; no
  mechanism file touched post-first-row).

## 3. Discipline proofs (raw-row recomputation)

- 60/60 rows, each cell exactly once per pass, no retries.
- unhealthy/error fraction 0/60 (batch-validity threshold 20% not approached);
  HTTP probes all 200; browser preflight true for both hosts.
- distinct store_before across the 60 eval runs == 1 (byte-restored grown KB
  via the FIXED rebuild path); store_after == store_before for every run;
  final store {states:16, transitions:27, actions:15, fragments:15} ==
  kb_at_eval_start ⇒ evaluation wrote nothing.
- pass1 == pass2 on status/action counts/reused/novel/subgoals_ok/solved_by
  in ALL 30 cells (deterministic replication, n=2 passes = replication NOT
  sampling uncertainty).

## 4. Depth ladder (unit: ROWS of 2 per task×arm; CELL = both passes)

| task (depth) | frag_v31 | frag_legacy | giter_v31 | giter_legacy | cold | traj |
|---|---|---|---|---|---|---|
| D2Q (2, control) | **2/2** (cell 1/1) | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| D3B (3, control) | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| D4B (4) | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| D4Q (4) | **2/2** (cell 1/1) | **2/2** (cell 1/1) | 0/2 | **2/2** (cell 1/1) | 0/2 | 0/2 |
| D5Q (5) | **2/2** (cell 1/1) | **2/2** (cell 1/1) | 0/2 | **2/2** (cell 1/1) | 0/2 | 0/2 |

Memory-led := status=="success" AND reused>novel (whole-row counts; resets
counted inside both by the explorer).

ACHIEVED memory-depth (distinct position classes among memory-solved
subgoals; prereg s4.6): D4Q/D5Q frag arms = {AUTH,TAG,PAGER} (3 classes —
HOME-Q and LOGOUT positions were solved by EXPLORATION); giter_legacy D5Q =
{TAG,PAGER,HOME-Q,LOGOUT} (4 classes; AUTH position by exploration).
**Nominal depth 5 was never covered end-to-end FROM MEMORY alone anywhere in
this cycle.**

## 5. Novel-action cost per task (matched tasks; both passes identical)

| task | frag_v31 | frag_legacy | giter_v31 | giter_legacy | cold | traj* |
|---|---|---|---|---|---|---|
| D2Q | **0** | 16 | 18 | 18 | 21 | 19 |
| D3B | 73 | 73 | 120 | 120 | 132 | 131 |
| D4B | 74 | 74 | 120 | 120 | 133 | 132 |
| D4Q | **1** | **1** | 38 | 3 | 57 | 49 |
| D5Q | **4** | **4** | 54 | 3 | 76 | 65 |

\* TRAJ REPRESENTATION LOSS (stated here wherever traj numbers appear):
14/16 grown-KB states carry no stored raw snapshot (cycle-3 dump convention),
so nearest-trajectory tokens degrade to step-slug tokens for those states and
site-scoping weakens (`sites=[]` for slug-only trajectories). Traj numbers
quantify THIS degraded representation, not a strong RAG baseline at full
fidelity.

## 6. Attribution (unit: row × subgoal; mechanism separation per prereg s1)

- (a) ADDRESSING-MISS (empty candidate lists): 26 subgoal rows —
  concentrated exactly where the committed dry diagnostics predicted:
  `eval.q.home`, `eval.q.logout` (+ `eval.b.cat`, `eval.b.home` on books;
  legacy also `eval.c2.page3`). The DISCLOSED broken-CAT expectation
  (prereg s4.2) reproduced: cat fell to exploration in every books memory
  arm.
- (b) EXECUTION-FAIL (candidates present, replay aborted): 8 rows — ALL
  books `b.book`: pager candidate present but its `a|||||next` step is
  unresolvable on product pages (abort_step "unresolved").
- (c) reset/entry-cascade pattern rows: 8 (books chains).
- (d) oracle/budget exhaustion rows (applications hit MAX_APPLICATIONS=6): 8
  (books graphiter rows).
- (e) exploration-fallback-dominant rows (novel>reused): 46 of 60.
- Reset counts are NOT instrumented at subgoal granularity (limitation);
  re-entry evidence reported at row level (loads/recoveries fields in raw
  rows).

## 7. Dry diagnostics (s7; REPORTED ONLY — non-gating)

Instrument roles beside these retrieval numbers: CONFIRM strings = THE
evaluation descriptions (third-authorship, frozen cbd0495); DEV strings =
alternates for offline sensitivity only (can never confirm); the cycle-4
fresh set remains SPENT and was not consulted; D2Q uses verbatim cycle-3 C2
descriptions (near-duplicate control). Offline rankings against the grown
dump, confidence filter disabled: frag_v31 nonempty 13/19 confirm queries
(class@1 11/19), frag_legacy 12/19 (10/19); giter arms rank all edges by
design (no threshold) with class@1 5/19. Empty frag candidates at b.cat /
b.home / q.home / q.logout (+c2.page3/q.tag legacy) — the exact ADDRESSING-
MISS set observed live. NO quantitative V31 claim is licensed from this
artifact (G4/spent-instrument discipline; V31 adoption is a program
decision).

## 8. Decision rule application (verbatim mechanics)

qualify_count(A) = #{D∈{D4B,D4Q,D5Q}: memory_led(A,D,pass) BOTH passes}:
frag_v31=2 (D4Q,D5Q), frag_legacy=2 (D4Q,D5Q), giter_legacy=2 (D4Q,D5Q),
giter_v31=0. Reference contrast (status(ref)!=\"success\" OR
novel(ref)>novel(A)) holds for cold AND traj on every qualifying pair and
pass (24/24). ≥1 arm with qualify_count≥2 + contrasts ⇒ **SCALING-HOLDS**
under the frozen rule. SCALING-COLLAPSE was not reached (its antecedent
fails). The rule does NOT weight WHICH composites qualify — the books side
contributes zero qualifying composites and zero reference successes; see §9
limits.

## 9. Mandatory limits (binding on any reuse of this result)

1. Scope: TWO scripted demo sites, ONE grown KB (16 states/15 fragments incl.
   duplicates), scripted deterministic consumers (agentB), desc_only,
   n=2 deterministic passes = replication not sampling uncertainty.
2. The positive result is QUOTES-SIDE ONLY (D4Q/D5Q share the login/tag/pager
   fragment inventory and the authenticated-root region). Books-side depth
   chains were unsolved by EVERY arm INCLUDING references — inheritance did
   not merely lose there, the TASKS were not solvable end-to-end by anything
   in this grid (b.book execution-fail mechanism), so books-side scaling is
   UNMEASURED, not falsified.
3. Achieved memory-depth ≤4 classes vs nominal depth 5: memory carried most
   but never all positions; exploration paid the remainder (novel 1–4 per
   successful deep row).
4. giter_v31 (frozen edge-equipment transfer) UNDERPERFORMED legacy edges —
   equipment transfer to the edge layer failed in this instantiation; no V31
   quantitative claim licensed anywhere (spent instruments; selection-on-
   instrument caveat inherited from G-H4).
5. Same-lab model-family third-authorship instruments (instructional
   isolation only, disclosed); oracle-verified scripted replay semantics for
   "memory-solved".
6. No LLM-consumer, cross-model, cross-site, calibration, wall-clock/latency
   or cost claims. retrieval_ms integer flooring supports NO latency claim;
   retrieval_us recorded hygiene-only.
7. Traj baseline ran on a DEGRADED representation (§5 note).
8. Program decision horizon reached: per directive, this preregistered
   confirmation completes `graph-inheritance-scaling` in EVERY branch of the
   decision rule.

## 10. PENDING ledger wording (PROPOSAL — Director integrates; team never
edits accepted history)

- G-H5 (PENDING, program `graph-inheritance-scaling`, cycle 1 run
  32793580374+repair): On the quotes demo site, composed routes requiring 4
  and 5 DISTINCT stored fragment classes were solved memory-led (end-to-end
  success, reused>novel) in 2/2 deterministic passes by blind fragment
  iteration with V31 standard equipment AND by legacy fragment iteration
  AND by loop-permitting edge iteration (legacy ranking), paying 1–4 novel
  actions vs 49–76 for cold/traj references on matched tasks; acceptance via
  anchored predicates + health gates; contamination gates (adjacent-pair
  recomputed non-vacuously, whole-task absence, NEW boundary-traversal check
  ≤1 crossing for all 15 fragments) passed before evaluation. BINDING
  CAVEATS: quotes-side only; books-side depth chains unsolved by ALL arms
  including references (execution-fail on b.book) so books scaling is
  UNMEASURED; achieved pure-memory depth ≤4 classes (home/logout positions
  exploration-filled after addressing misses predicted by committed dry
  diagnostics); giter edge-equipment transfer FAILED (qualify_count=0);
  D2Q control memory-led only under frag_v31; traj reference degraded to
  slug tokens on 14/16 raw-less states; two sites/one KB/scripted
  consumers/n=2 replication/no wall-clock claims; V31 adoption remains a
  program decision with spent instruments — no quantitative addressing claim.

## 11. Artifact map

- Raw rows: `results/graph/scaling_live_runs.json` (canonical, 60 rows)
- Interrupted first launch: `results/graph/provenance/
  scaling_live_runs_INFRA_INTERRUPTED_20260825_infra_interrupted.json`
- Analysis: `results/graph/scaling_analysis.json` (from raw rows only;
  `graph/analyze_scaling.py`)
- Gates: `results/graph/scaling_gates.json` (regenerated, marked;
  `graph/check_scaling_gates.py`; ends reconstruction
  `results/graph/scaling_subgoal_ends_reconstructed.json`)
- Dry: `results/graph/scaling_dry_scores.json` (`graph/score_scaling_dry.py`,
  committed BEFORE live rows)
- Drivers: `graph/run_scaling_live.py` (P2), `graph/run_growth_scaling.py`
  (growth, hook-wired for future producer runs)
- Manifest: `results/graph/scaling_MANIFEST.json`
