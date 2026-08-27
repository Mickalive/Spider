# TEAM GRAPH — program `graph-addressing-fused-retrieval`, cycle 1 report

Run 32905175867 · branch `cycle/graph/32905175867/team` · freeze commit
`05c049d` (prereg + instruments + code, BEFORE any live observation) ·
KB = accepted generalization dump, byte-restored per run, NO growth.

## 0. Verdict (frozen decision rule applied verbatim)

**MEASUREMENT_INVALID** — retrieval-stack-void branch of prereg s8/s9.
This is an INSTRUMENT-LEVEL status, not a claim that fused scoring fails,
and NOT environment instability (health gates never fired on canonical
runs; two earlier whole-pass calibration attempts died to runner shell
timeouts before any completed probe pass — INFRA_INTERRUPTED provenance).
The lane is therefore NOT BLOCKED under the directive's rule (that trigger
requires two consecutive MEASUREMENT_INVALID *from environment
instability*).

The decisive clause: the frozen global validity precondition "B_mmr must
exceed D_random on the hard slice overall" FAILS under the literal output
semantics on the HARD SLICE, n=64 instances (tau-gated B: 0/64 hard-slice
hits; tau-less random by frozen construction: ungated top-1, 16/64) and
would PASS only by +2 hard-slice hits under an alternative all-ungated
ranking reading (18/64 vs 16/64). The all-instance aggregates — gated B
0/75 vs random 17/75 — are aggregates over all 75 query instances and are
NOT hard-slice counts. The ambiguity was
created by the freeze itself (s8 assigned taus "one identical procedure per
arm, B and C_final" and none to random); it is DISCLOSED and was NOT
resolved post hoc. Every number needed to re-read either way is committed.

## 1. What ran (all rows carry instrument_role/instrument_id)

- CALIBRATION (`results/graph/fused_calibration.json.gz`,
  truth sets hashed in `fused_truth_sets.json`): 30 frozen qids → 25 valid
  (3 already-satisfied listed; 2 health-floor exclusions on the genuinely
  small /login page listed), 203 probe rows, writes nothing. Truth
  structure highlights: b.hfcat solved ONLY by books.cat.fiction's prefix
  chain; open-book trio co-solves (|G|=3); q.tagp2@Q_ROOT expected-UNKNOWN;
  login positions |G|=2 (duplicate pair). Chunked idempotent protocol after
  process-group kills; per-candidate fresh browser contexts after a
  within-probe session-carry-over defect was caught in a discarded partial
  (login replay authenticated later unrelated probes — fixed pre-outcome,
  provenance preserved).
- DEV SCREENING (`fused_dev_selection.json`, confirm untouched at this
  point): alpha* = 0.7 (22 vs 21 informative-hard hits — fragile margin in
  the variant-attempt ledger); original tau procedure produced
  MEASUREMENT_INVALID exactly as its floors were written (zero-FA taus
  exist but known-row coverage 0.125–0.167 < my 0.60 floor); **Amendment
  A2 (pre-confirm)** removed ONLY that added floor, keeping zero-dev-FA,
  smallest-tau tie-break and both curves → τ*_B = τ*_C = 0.2. Substrate
  gate passed (61 informative-hard instances ≥ 15; every cluster ≥ 4:
  CATEGORY 16, HOME 13, PAGER 12, AUTH 10, OPENBOOK 5, TAG 5).
- CONFIRM RETRIEVAL (`fused_retrieval_confirm.json`; 75 query instances =
  25 qids × 3 forms, instrument fused-confirm-4a): cross-phase summary-key
  mismatch 0; summary cost 14 misses (=would-be LLM calls) + 14 hits.
- CONFIRM EXECUTION (`fused_live_runs.json`; 48 rows = 6 composites ×
  {A_strict, A_std, B, C} × 2 passes; agentB / desc_only / evaluation
  writes nothing / budgets MAX_APPLICATIONS=6 MAX_RESETS=2 identical to
  G-H5/G-H6 grids / KB digest equal before-after every row): pass identity
  24/24 (determinism check only).

## 2. Retrieval level (clusters NEVER pooled)

GATED primary (NL-consumer × hard × informative, C_final(α=0.7, τ=0.2) vs
B_mmr(τ=0.2)): **0 wins – 0 reversals over 61 paired rows** — universal
abstention tie (B coverage 7/72 known rows, C 5/72; zero false accepts for
both on all 3 UNKNOWN-row outputs, trivially so since the constraint is set
by one UNKNOWN qid family — disclosed in A2.3-ii in advance).

UNGATED secondary (report-all family, predeclared A2.3-iii), hard slice:

| arm | hard@1 | note |
|---|---|---|
| A_sig | 53/64 | signature regime dominates |
| A_ft | 0/64 | free-text incumbent cannot resolve paraphrases |
| B_mmr | 18/64 | barely above chance |
| C_final | 20/64 | paired vs B: 3 wins / 1 reversal (n=61) |
| D_random | 16/64 | chance floor |

Battery (attribution-only), BOTH output conventions labeled (61
informative-hard rows each):

- UNGATED hard-info pairs vs B_mmr (report-all view): C_bat_dummy 5W/6L,
  C_bat_perm 2W/3L, C_bat_sonly 6W/13L.
- GATED pairs at τ*_B = τ*_C = 0.2 (the convention the FROZEN specificity
  determination consumed: `fused_analysis.json` computes `battery_specific`
  from the committed gated `battery_paired` block): C_bat_dummy 2W/0R,
  C_bat_perm 0W/0R, C_bat_sonly 0W/0R — it is the gated dummy pair that
  drives `battery_specific = false`.

No variant separates positively under EITHER convention and dummy matches
or exceeds C's margin under both ⇒ **state-channel specificity NOT
demonstrated** (conclusion INVARIANT under both conventions; summarizer
survival UNRESOLVED even before the verdict gate). Token-provenance
prestate rescore: 28/61 hard-info ungated — most margin survives without
post-state URL/title tokens, i.e., what little signal exists is affordance-
side rather than arrival-vocabulary echo. id10 sensitivity: excluding
id10-touching rows leaves the 0–0 gated tie unchanged (42 kept rows).
At-goal stratum n=12, both arms 0 (no post-state leak effect measurable).

## 3. Execution level (store/policy loop, real browser)

End-to-end memory-led rows (all subgoals solved with reused>novel):
A_strict 8/12, A_std 8/12 (novel 0–14 per composite) vs **B 0/12, C 0/12**
(novel 64–103). Per-subgoal signed medians on commonly-solved cells
(n=16 cells solved by both arms in BOTH passes): C−B = 0.0 (no conversion
advantage); A_std−C = −2.0 and A_strict−C = −2.0 (the incumbent pays TWO
fewer novel actions than C where both solve — no regression of the
signature regime; the direction favors A). Books-side pattern replicates
the G-H6 attribution: embedding arms memory-solve cat/pager/hfcat positions
but burn their application budget on the open-book position ('a|||||'
first-match binding) and fall to budget-bounded exploration. Quotes-side:
A arms perfect replay; B/C diverge mid-chain (tag/tagp2/home positions),
C strictly worse than B on D4Q (98 vs 81 novel) — the state term added
noise here rather than grounding.

Cluster-level honesty per Intel caveats: no advantage anywhere; the one
place fusion COULD have helped (region binding, CATEGORY/HF-CAT) was
already served by task-text ranking because the stored descriptions
themselves carry region tokens.

## 4. Economics (reported WITH the mechanism, hygiene rules respected)

Median retrieval_us per lookup/run (perf_counter; NO wall-clock or latency
claim licensed): A_strict 315, A_std 329, B 1490, C 2949 µs — the fused
layer costs ~2× the plain embedding stack and ~9× legacy sig lookup per
lookup, while saving ZERO novel actions at matched success (median Δ=0.0)
and reducing memory-led success from 8/12 to 0/12 relative to the
incumbent. Summary generation costs would-be LLM calls per C run of
3 (D3B, D4Q), 4 (D4B, D4H) and 5 (D5B, D5Q) — true range 3–5 per run,
max 5, matching `fused_analysis.json`
`economics.would_be_llm_calls_per_run_max.C = 5`; cache hits (0–1 per
run) are recorded beside every row and counted separately. Break-even statement: S=0 saved
actions/subgoal ⇒ repayment undefined — overhead unrepaid at any horizon
in this setting. Storage: bank embeddings + summary cache ≈ tens of KB.

## 5. Deviations & amendments (all labeled, none post-confirm)

1. Amendment A1 (pre-outcome): D2Q excluded (instrument has no honest
   page-3 pager description); SIG_MAP translation for incumbent arms
   (straw-A prevention); additive per-subgoal cost deltas in explorer.
2. Amendment A2 (pre-confirm): tau coverage-floor removal (see §1); both
   procedures' curves committed.
3. Post-analysis disclosure (NO amendment): the s8 B-vs-random
   precondition is ambiguous w.r.t. gating symmetry; verdict follows the
   literal reading; both readings' numbers committed (§0).
4. INFRA_INTERRUPTED ×2 (calibration whole-pass attempts killed by runner
   shell timeout before completion) → chunked protocol; exporter-defect
   first grid preserved under `results/graph/provenance/` (never cited);
   within-probe session-carry-over defect caught and fixed pre-outcome via
   per-candidate fresh browser contexts (additive opt-in
   `Session.new_context()`; shared-infra divergence flagged for
   Meta-Director reconciliation per constitution §5).
5. PROVENANCE ERRATA (repair round 1; no outcome artifact touched): the
   confirm/selection drivers read `self_sha256_input` from the calibration
   gzip (`FE.load_calibration()` → `fused_calibration.json.gz`, which does
   not carry that field) instead of from
   `results/graph/fused_truth_sets.json`, leaving
   `calibration_self_sha256 = null` in BOTH `fused_dev_selection.json` and
   `fused_retrieval_confirm.json`. The true cross-phase
   calibration/truth-set self-pin is
   `235834e82810c36f0f97a63504d8cb60c3da4ef72f092df3406aa721c0c81e77`,
   recorded in `fused_truth_sets.json` field `self_sha256_input`
   (sha256 over canonical sort-keys JSON of the calibration metadata;
   independently recomputed during repair). Until any successor
   regenerates artifacts, cross-phase binding rests on this errata plus
   the manifest pin `489631af…` for `fused_truth_sets.json`; the same
   errata is recorded in `results/graph/fused_MANIFEST.json` notes[].
6. UNEXERCISED EARLY-STOP CLAUSE (labeled deviation): prereg s9's
   economy clause would have restricted execution to A-regression cells
   once retrieval-level separation failed at confirm. It was NOT
   exercised: the full 4-arm × 6-composite × 2-pass execution grid ran
   anyway. Direction CONSERVATIVE — the extra rows are additional
   evidence AGAINST the candidate (the adopt path was already unreachable
   when execution started), so no outcome or verdict depends on the
   deviation.

## 6. Maximum defensible wording (proposed ledger entry G-H7)

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
> under an
> alternative all-ungated reading — an ambiguity created by the freeze,
> disclosed verbatim, not resolved post hoc. Substantively: with honest
> abstention thresholds the lexical-hash embedding stack (with or without
> state-summary fusion) retrieves almost nothing above absolute-score
> noise under paraphrase+entry-shift (ungated hard@1 B 18/64, C 20/64,
> random 16/64); fused scoring separates from task-text-only by at most
> 3 wins/1 reversal ungated and 0–0 gated; converts to ZERO median novel-
> action savings at matched subgoal success (16 common cells) against
> ~2× retrieval overhead per lookup; fails the state-specificity battery
> (constant-summary control matches its margin); and the exact goal_sig
> incumbent remains dominant wherever mapped signatures exist (memory-led
> end-to-end 8/12 composites at 0–14 novel actions vs 0/12 for text arms
> at 64–103). Fused task+state-summary addressing is NOT adopted into the
> Graph product path in this setting; exact addressing stays standard for
> signature consumers; no NL-consumer option is licensed by this evidence.

Binding limits traveling with any citation: two scripted demo sites; ONE
16-fragment KB (small-library regime; pool M=20 ≥ N makes MMR diversity
inert); lexical-hash embedder and deterministic summarizer regimes only
(neural/LLM survival OPEN); single UNKNOWN qid family sets the FA gate;
same-lab model-family instrument authorship; n=2 passes = determinism only;
no latency/wall-clock claims (µs fields hygiene-only); MEASUREMENT_INVALID
is instrument-level and does not falsify the mechanism outside this setting.

## 7. Next high-information action (for the Director)

The discriminating residual is NOT fusion-vs-task-text (decided null here)
but DESCRIPTION QUALITY and LIBRARY SCALE: every observed failure is an
instance of (i) auto-derived descriptions too weak as keys (open-book
'a|||||', category vocabulary) or (ii) N≤M pool saturation. The queued
R-2 addressing arm and any successor should preregister against a
description-induction or scale intervention BEFORE another scorer
comparison; rerunning scorer variants on this KB cannot change the answer.

## 8. Repair-round provenance (round 1, post-audit CYCLE_32905175867_REVISE)

The rejected round-0 team snapshot (`4426f40`, run 32905175867) is preserved
verbatim in git history as provenance; this repair starts from it and changes
NO code, NO outcome-bearing artifact, and NO verdict-bearing number. Applied
required fixes: RF-1 (§4 summary-call sentence corrected to the true 3–5
range, max 5), RF-2 (§0 and §6 G-H7 wording restated with unit-correct hard-
slice denominators n=64: gated-B 0/64 vs random-by-construction 16/64;
all-instance aggregates 0/75 vs 17/75 only as labeled aggregates), RF-3 (§2
battery pairs labeled by convention — gated pairs drive the frozen
`battery_specific=false`; conclusion invariant under both), RF-4 (manifest
notes[] errata + §5 item 5 recording the `calibration_self_sha256=null`
wiring cause and true pin `235834e8…`), RF-5 (§5 item 6 labeled deviation:
s9 early-stop economy clause not exercised; conservative direction).
Every corrected number was independently recounted from raw rows with fresh
(non-analyzer) code before editing; recounts and method are committed as
`results/graph/fused_REPAIR_ROUND1_recount.json`. The verdict
MEASUREMENT_INVALID (instrument-level retrieval-stack-void) and every
substantive number are unchanged.
