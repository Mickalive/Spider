# TEAM GRAPH — Cycle 2 (Run 32689296167): E1–E4 preregistered batch

Date: 2026-08-24 · Live sites (books.toscrape.com, quotes.toscrape.com) ·
Playwright/Chromium · scripted heuristic policies (no LLM in loop)

Primary artifacts:
- Raw batch (Phase A + full Phase-B matrix + X1):
  `results/graph/cycle3_20260824_043334.json`
- E3P completion rows + recomputed dry table + pristine-KB proof:
  `results/graph/cycle3_20260824_045849_e3p.json`
- Merged final dataset + frozen analysis:
  `results/graph/cycle3_20260824_043334_FINAL.json`,
  `results/graph/cycle3_20260824_043334_FINAL_analysis.json`
- Auditor store dump (post-training KB, transitions==19):
  `results/graph/cycle3_20260824_043334_store_dump.json.gz`
- Preserved live DB during this session:
  `/tmp/opencode/spider_graph_cycle3.db` (ephemeral; dump above is the
  durable extract)
- Preregistration: `graph/prereg_cycle3.md`

## AUDIT STATUS

**Status: PREREGISTERED BATCH EXECUTED; decisions below are team-level
conclusions pending independent audit.** All headline numbers recompute
from raw rows via `graph/analyze_cycle3.py` (arithmetic frozen before
Phase B, commit a1be3a0/7087e4a).

**REPAIR ROUND 1 (2026-08-24) applied**: independent audit
`CYCLE_32689296167_GRAPH` (gate REVISE, textual-only, no rerun required)
found one defect — non-reproducible denominators in the E2 residual-value
sentence ("login 6/6 vs 0/4 edges", success-conditioned count mixed with
a cell convention; books-pager "fragments 2/2" counted only inherit).
RF-1..RF-3 applied above: login packaging now reported as 16/16 fragment-arm
evaluation rows = 8/8 condition×task cells vs graphiter 0/8 rows = 0/4
cells; books pager as inherit 2/2 + fragntr 2/2 = 4/4 fragment-arm rows vs
graphiter 0/2; corrected numbers mirrored into F1' and the proposed G-H3
wording (and into the pending ledger entry). Denominators independently
recomputed from `results/graph/cycle3_20260824_043334_FINAL.json`
subgoal_rows; all scientific outcomes, raw data and other findings are
unchanged from the audited snapshot (team head d467e02, preserved as
provenance).

### Provenance chain (freeze-timing, disclosed in full)

1. Prior run 32684818422 committed the frozen prereg (cedf34d, 03:13),
   the anti-strawman E2 amendment (220196d), all mechanism code
   (cb3fa61), independently-authored paraphrases (a93639d) — then died
   BEFORE any evaluation outcome: every artifact it left is
   `stage: post-training-dry`; zero composite outcomes exist anywhere on
   that branch (verified by inspecting all four JSONs).
2. This run adopted that prereg + machinery VERBATIM (commit a987e82),
   then made three pre-outcome driver edits, each committed before any
   outcome existed: mechanical E3P case selection replacing a hard-coded
   draft (a1be3a0); incremental progress flushing (e66ae31); intent-label
   fix for case selection (7087e4a). Unit tests (15) pass.
3. The batch executed at 04:33–04:55 under exactly the committed code.
   Phase B row 1 was observed only AFTER all commits above.
4. POST-OUTCOME INCIDENT: after all 54 Phase-B rows and 4 X1 rows were
   recorded, the driver crashed at E3P probe-task ASSEMBLY (KeyError from
   my pre-outcome driver edits; lookup keyed by composite id instead of
   subgoal sig). No E3P row had been observed. Repair touched only probe-
   task construction; mechanism code is unchanged since 7087e4a. E3P rows
   were then produced by `graph/run_cycle3_e3p.py` on the preserved
   post-training KB (pristineness asserted there: fragments=12,
   states=14, transitions=19, transitions reference training tasks only —
   proving evaluation wrote nothing across all 58 earlier rows).
5. Losses caused by the crash, disclosed: (a) the batch's interim dry/KB/
   probes sections were overwritten by progress flushes; the dry table
   and KB snapshot were RECOMPUTED bit-exactly from the preserved DB
   (deterministic scorer + seed; same fragment order); (b) batch-time
   HTTP probes were lost and replaced by POST-BATCH probes recorded in
   the FINAL json (`merge_note.probes_preflight_source`). Primary per-row
   environment evidence is the prereg §1 health gate, evaluated at EVERY
   run start: no `unhealthy_host` status occurs in any of the 72 rows.

Route absence was verified before evaluation (strict adjacent-pair test,
C1/C2/C3 all True; recomputed from the preserved DB and recorded in the
FINAL json). X1 is transfer-by-design with known shared prefix.

---

# HEADLINE DECISIONS (priority order per steering note)

## E1 — Query-construction ablation: **keyword-assisted retrieval** is still the honest state for composed depth; desc-only addressing is REAL but partial.

Live matched evidence (inherit arm, 2 passes × 3 composites × both modes,
identical restored KBs):

| subgoal | mode | candidates non-empty | memory-solved | end-to-end |
|---|---|---|---|---|
| eval.c2.login / eval.c3.login | desc_only | 4/4 | 4/4 | login always replayed |
| eval.c1.page2 (books pager) | desc_only | 2/2 | 2/2 | memory |
| **eval.c2.page3 (quotes pager)** | **desc_only** | **0/2** | **0/2** | **unsolved** |
| **eval.c3.page5 (quotes pager)** | **desc_only** | **0/2** | **0/2** | **unsolved** |
| same two quotes pager goals | desc_kw | 4/4 | 4/4 | C2+C3 success |

Decision rule applied (directive E1): desc-only does NOT solve the pager
subgoals that define composed quotes depth → the accepted wording stays
**"desc+keyword retrieval"** for that capability. Simultaneously, desc-only
addressing IS demonstrated for (a) form-login procedures and (b) books
listing pagination — so "descriptions never work" would be equally wrong.
No threshold was tuned (constants frozen at TAU=0.30/MIN_MATCH=2/
COV_CAP=6/DF_KEEP=0.6); per directive, any future fix must be validated
on the E3 holdout, not on these composites.

## E2 — Loop-permitting iterative graph baseline: **the cycle-1 advantage over graph-search baselines was the ITERATION POLICY, not the fragment representation.**

`graphiter` (flat edge multiset, no thresholds, same scoring family,
equalized accept-oracle, MAX_APPLICATIONS=6, MAX_RESETS=2, identical
exploration fallback):

| cell (status, x2 passes) | inherit | graphiter | fragntr |
|---|---|---|---|
| C2 desc_kw | success | success | success (chained 2 frags) |
| C3 desc_kw | success | success | **partial** (depth 4 > candidate count) |
| C2 desc_only | partial | **success** | partial |
| C3 desc_only | partial | **success** | partial |
| C1 (all modes) | partial 2/3 | partial 2/3 (desc_kw) / 1/3 (desc_only) | partial 2/3 / 2/3 |

Decision rule applied (directive E2): graphiter MATCHES the fragment
condition end-to-end on every C2/C3 cell (and exceeds it under desc_only,
where edge application has no MIN_MATCH cutoff). Per the frozen rule the
ledger records: **at this composed depth the store's transition edges
alone suffice once iteration + oracle are equalized; the product question
moves from abstraction to addressing.**

Residual fragment-layer value measured (not assumed). Denominator
convention (fixed in repair round 1 per audit CYCLE_32689296167
RF-1/RF-2): counts cover ALL evaluation rows of an arm regardless of
end-to-end status — never conditioned on composite success — reported as
rows and as condition×task cells (2 identical passes each):
- **Login packaging**: fragment arms (inherit+fragntr × desc_kw+desc_only
  × C2+C3) solved the login subgoal by memory in **16/16 evaluation rows
  = 8/8 condition×task cells** (passes identical); graphiter solved it
  via stored edges in **0/8 rows = 0/4 cells** — all eight graphiter
  logins fell back to exploration and burned ~150–151 decision points
  (fill edges rank top but state-setters apply-once; budget burned on
  clicks). Multi-step procedure structure lives in fragments, not in
  flat edges.
- **Books pagination under desc_only**: inherit 2/2 and fragntr 2/2 —
  **4/4 fragment-arm evaluation rows** memory-solved; graphiter 0/2
  (bare anchors too weak lexically without keywords).
- **Cost**: on C2/C3 graphiter reused MORE actions (8–11 vs 6–8) and
  paid exploration fallback for login; fragment rows ran 0 decision
  points. Status parity ≠ cost parity.

`fragntr` isolates iteration itself: removing it costs C3 depth even
with retrieval intact (partial; 2 applications of two DISTINCT pager
fragments cannot reach page-5), while C2 succeeds by chaining distinct
candidates — direct evidence that ITERATION buys depth, candidate count
buys shallow chains.

Also notable AGAINST fragment superiority: the mystery-category subgoal
rejected by the fragment scorer (MIN_MATCH after df-pruning, known F3)
was solved by graphiter in 1 click (`click a|||||mystery`, top-ranked
edge, no cutoff). Flat edges addressed category navigation BETTER than
the fragment layer this cycle.

Baselines replicate cycle 1: graphbfs / traj / cold solve 0/3 composites
end-to-end on identical KBs (statuses bit-stable across passes).

## E3 — Paraphrase holdout: **first semantic-addressing number of this lane is LOW: retrieval@1 = 2/8 positive goals (25%) on held-out wording.**

Offline scoring (frozen scorer, freshly trained KB, both modes;
10 held-out paraphrases authored without access to corpus/scorer —
same-lab model-family authorship, disclosed in
`graph/paraphrase_prompt_cycle3.md`):

| metric | near-dup descs | held-out paraphrases |
|---|---|---|
| positive-goal retrieval@1, desc_only | 4/8 | **2/8** |
| positive-goal retrieval@1, desc_kw | 6/8 | **2/8** |
| expected-UNKNOWN discipline (unseen named books stay unmatched) | 4/4 | 4/4 |

The 25% is a TRUE positive-retrieval rate: only 2 of 8 addressable
paraphrases retrieved anything at all (x1.page2, c2.login). Reporting
4/8 "correct" would silently count trivially-correct empties; both numbers
are given. Expected-UNKNOWN discipline is perfect everywhere — the scorer
never fabricated a match for unseen content.

Live confirmation (mechanically selected verdict-changing cases:
c2.page3, c3.login, c3.page5, c1.page2; 2 passes each, restored KB):
**0/8 rows reused a single memory action.** Paraphrase-worded pager goals
fell back to exploration and stayed unsolved (c1_page2: 60 wasted actions
×2 passes; quotes pagers: 15 actions ×2). The one paraphrase-login probe
was solved by EXPLORATION (5 novel actions), not by memory. Addressing
robustness, not just offline ranking, collapses under rewording.

Interpretation: current "semantic addressing" is near-verbatim lexical
matching plus a keyword channel. It does not yet survive independent
paraphrase. Any claim of solved semantic addressing is falsified for this
mechanism.

## E4 — Anchored predicates + hygiene: **valid; X1 rerun clean.**

- Path-segment-anchored predicates (`graph/accept.py`) passed the trap
  suite BEFORE any live run ('fiction' ⊄ historical-fiction; '/page/3' ⊄
  '/page/30'; segment equality after `_N`/`.html` stripping) — 15/15 unit
  tests green.
- X1 transfer row rerun under anchored predicates, 2 modes × 2 passes:
  identical behavior ['exploration', 'memory', 'unsolved'] — fiction
  category reached by exploration, page-2 memory-solved (books pager
  retrieves under BOTH modes), named tail correctly UNKNOWN and unsolved.
  No historical-fiction false accept occurred anywhere (the fresh KB also
  contains no historical-fiction fragments — df-universe differs from the
  invalid cycle-1 X1 setting). X1 enters the ledger as a VALID bounded
  transfer observation: known-prefix reuse + honest novelty boundary, NOT
  whole-task transfer.
- Hygiene verified from raw rows: distinct `store_before` across ALL 66
  eval runs = 1 (per-run byte restore); evaluation wrote NOTHING
  (transitions stayed 19 through 58 consumer rows — closes audit C6
  self-read channel absolutely, including states/transitions);
  `steps_ok` cleared between candidates; health gate active every entry
  and reset (no unhealthy_host rows).
- Pass1↔pass2 replication: all 27 cells IDENTICAL in status/reused/novel/
  actions/subgoals_ok (deterministic seeds + stable site content; the two
  passes guard against transient flakiness, they do not sample variance).

---

# Findings

- **F1' (E2, replaces audited F1 attribution gap)**: composed-depth
  advantage over single-shot/no-loop baselines is attributable to the
  iterate-until-accept POLICY with equalized oracle; fragment packaging
  adds multi-step procedure value (login memory-solved in 16/16
  fragment-arm rows = 8/8 cells vs 0/8 graphiter rows = 0/4 cells) and
  lexical robustness (books pager under desc_only: inherit 2/2 +
  fragntr 2/2 = 4/4 fragment-arm rows vs graphiter 0/2), not
  compositional power.
- **F2' (E3, hard limit)**: addressing does not survive independent
  paraphrase (2/8 positive retrieval@1; 0/8 live memory reuse). Current
  mechanism = near-verbatim matching + keyword channel + strict UNKNOWN
  discipline (zero false positives measured).
- **F7 (new, E1 nuance)**: desc-only viability is site/description
  dependent: URL-borne tokens give books pager descriptions enough signal
  ({page, 2, book}) while quotes pager descriptions collapse to
  {page, next, 2} after df-pruning, needing the injected keyword 'next'.
- **F8 (new, E2 mechanics)**: single-application fragment mode composes
  depth up to the number of DISTINCT matching candidates (C2: 2 pages via
  generic.paginate.next + quotes.page.2), then fails (C3 page-5) — depth
  beyond TOPK requires iteration, not more fragments.
- **F9 (new, E2)**: threshold-free edge ranking can beat the fragment
  scorer where df-pruning starves fragment descriptions (mystery category,
  1 click) — cutoffs on the query side can be the binding constraint, not
  knowledge missingness.
- **F10 (provenance)**: progress-flush robustness overwrote interim
  sections on crash; dry/KB reconstruction from the preserved DB was
  bit-exact ONLY because evaluation writes nothing and the scorer is
  deterministic. Write-suppression is what made recovery possible.
- **F11 (prior-run reconciliation)**: prior attempt 32684818422 left a
  complete frozen design and zero outcomes; its hard-coded two-case E3P
  draft would have UNDER-selected (mechanical rule yields 4 cases on this
  KB). Adopting its prereg while redoing execution preserved registration
  validity and added an independent training replicate.

# What this cycle does NOT support

- No descriptions-only addressing of quotes pagination depth (E1 failed
  there by the frozen rule).
- No fragment-layer composition-power claim over equalized graph
  iteration (E2 resolved toward policy).
- No semantic-addressing claim of any generality (E3 number is low).
- No cross-site skill, cross-model, wall-clock, or calibration claims
  (untouched, out of scope per directive).
- Scripted policies, two small structured sites; consumer never sees
  IDs/sigs/hints; subgoal decomposition remains benchmark-defined.

# Required next tests

1. Descriptor work for addressing robustness MUST be validated on the E3
   paraphrase holdout (directive rule), e.g. positional/entry-context
   descriptors and anchor-token enrichment — predeclared, no threshold
   tuning on composites.
2. Login-procedure reuse without the fragment layer (edge-sequence
   packaging) to test whether F1'-login is procedural structure or
   merely fill-ordering.
3. Natural-growth inheritance curve (G12) now has valid predicates +
   health gating as prerequisites.
4. If addressing is fixed, revisit G4 deeper chains (>3 fragments) under
   BOTH policies with the E2-equalized baseline as standard equipment.

---

## Team-level ledger proposal (for GRAPH LANE DIRECTOR; not integrated)

Proposed G-H3 wording pending audit (numbers corrected in repair round 1
per audit CYCLE_32689296167 RF-1..RF-3): "Under a fully pre-registered
batch
(replicated x2 passes, machine-enforced route absence, byte-restored KB,
write-suppressed consumers, anchored predicates): (1) composed-depth
capability is carried by oracle-guided iteration over stored transition
edges; the fragment layer contributes procedure packaging (login
memory-solved 16/16 fragment-arm evaluation rows = 8/8 cells vs 0/8
graphiter rows = 0/4 cells) and lexical robustness (books pager under
desc_only: inherit 2/2 + fragntr 2/2 = 4/4 fragment-arm rows vs
graphiter 0/2), not composition power; (2) addressing
remains keyword-assisted for quotes pagination and fails held-out
paraphrases (retrieval@1 2/8; live reuse 0/8) while preserving perfect
expected-UNKNOWN discipline; (3) X1 transfer rerun is measurement-valid
under path-anchored predicates (bounded prefix transfer, named tail
honestly unknown)."
