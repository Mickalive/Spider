# TEAM GRAPH — program `graph-addressing-key-induction`, cycle 1
# (run 32925866227, REPAIR ROUND 1)

Round-0 audit (CYCLE_32925866227): **REVISE** — five concrete same-cycle
defects (invalid sign-test p-values, four-way population mislabeling, an
undisclosed post-freeze driver tweak, undisclosed reference-arm scope
divergence, parity coverage blind to p-values); NONE verdict-driving. This
document is the repaired snapshot: every fix applied against BYTE-IDENTICAL
raw evidence, every affected artifact regenerated and recounted, rejected
round-0 derived artifacts preserved under `results/graph/provenance/
*REJECTED_ROUND0*` and at `origin/cycle/graph/32925866227/team @ 4fb87c0`.

Verdict (mechanical, prereg s9 applied verbatim): **INDETERMINATE** — the
declared primary retrieval statistic finished BELOW its pre-declared
decisive-pair floor (10 decisive pairs < 15), which prereg s8 routes to
"INDETERMINATE, never falsified"; none of the three independent
FALSIFIED-IN-SETTING triggers (separation failure WITH floors met /
incumbent regression / confirm false accepts) fired. The verdict is
INVARIANT under the repaired statistic, both four-way population
conventions and every defensible reading. Substantive report-all
secondaries are integrated honestly below. The decision horizon is reached
in this branch: the keys-vs-baseline contrast is decided at the level the
frozen rule supports, and every follow-up requires its own successor
preregistration with fresh instruments.

Freeze chain: prereg + fifth-authorship instruments + ALL code committed at
`9108ba3` BEFORE any calibration probe / screening / confirm / live row.
Calibration truth sets are BIT-IDENTICAL to the accepted G-H7 sets on all
25 qids (zero site drift; stability delta = NONE).

## 0. Disclosed corrections (both pre-report; nothing hidden)

### 0a. Item-29 parity correction (round 0)

The first analyzer draft emitted `FALSIFIED_IN_SETTING` because its branch
ordering tested `not separates` before the decisive-pair floor. Prereg s8
(frozen pre-outcome) states verbatim: "below 15 decisive pairs the statistic
is INDETERMINATE, never falsified." The analyzer was corrected BEFORE any
report or ledger wording existed, in the only direction the frozen text
permits (toward the weaker label); no raw artifact changed; recount parity
was re-verified after the correction (`keys_RECOUNT.json all_parity_ok=true`).
Recorded as a labeled deviation in `keys_MANIFEST.json notes[]`.

### 0b. REPAIR ROUND 1 (audit CYCLE_32925866227 REVISE, RF-1..RF-5)

The round-0 audit found that the shared sign-test machinery implemented a
DIFFERENT statistic than the frozen text: `paired_sign` fed
`min(wins, reversals)` to the tail function, i.e. the SMALLER-side tail,
which is bounded below by ~0.5 for any B-favorable outcome — so every
round-0 committed p-value was invalid AND `separates` was unreachable in
exactly the adopt direction (latent false-FALSIFIED hazard for any
successor reusing the code). RF-1 repairs the statistic to prereg s8 as
written: direction-labeled exact one-sided binomial tails,
`one_sided_p = P(X >= wins | decisive pairs, .5)` on the declared better
arm, exported beside the opposite-direction tail; `separates` consumes the
declared-direction tail under the unchanged conjunctive floor. ALL derived
artifacts (`keys_analysis.json`, `keys_claim_tables.md`, this report,
the G-H8 proposal) were regenerated from UNCHANGED raw rows; raw-evidence
sha256 pins are identical to round 0; recount parity coverage extended to
every derived-statistic class (RF-5, 23 classes) and is green. Corrected
headline p-values: primary gated informative-hard 10W/0R d=10 → **0.000977**
(floor binding: INDETERMINATE_BELOW_FLOOR unchanged); secondary ungated
10W/9R d=19 → **0.500000** (exactly chance); four-way literal gated_all
12W/0R d=12 → 0.000244; ungated_all 13W/10R d=23 → 0.33882; PAGER cluster
ungated 8W/0R → 0.003906. Nothing separates anywhere; verdict invariant.
The scientific conclusion is UNCHANGED from round 0 and, if anything,
slightly more favorable to B_keys directionally at undecidable power.

## 1. Design executed

- Arms (prereg s3): A_keys = auto-derived descriptions under the UNMODIFIED
  G-H7 arm-B machinery (bank bit-identity gate green);
  B_keys = induced keys rules v1, DEV-selected variant **K_full**
  (R1 affordance verbs + ordered labels; R1b key-side digit<->ordinal;
  R2 site-scoped region-of-entry join, netloc/`index`/`html` excluded;
  R3 effect join), IDENTICAL machinery; D_random ungated-by-construction;
  A_sig/A_ft incumbents as references/regression checks only.
- Instruments: fifth authorship, isolated sessions, `keys-dev-5a`
  (sha256 01c6436f…164c) / `keys-confirm-5a` (e8ce9a26…a200); roles enforced
  by loader; selection-once enforced by artifact-exists guard.
- Calibration: this program's own pass (203 probe rows / 25 valid qids /
  3 already-satisfied listed / 2 health-floor invalid probes — same qid
  family as G-H7); substrate gate PASS (61 informative-hard >= 15; min
  cluster 5 >= 4).
- Execution grid: 6 composites x 4 arms x 2 deterministic passes = 48 rows,
  budgets equalized to audited grids, byte-restored KB {19,29,15,16} before
  every run, evaluation wrote nothing (store stats equal pre/post on all
  rows), pass identity 24/24 (determinism ONLY).

## 2. Retrieval-level outcomes (confirm instrument, n=75 rows)

Hard slice n=64 hard rows; informative-hard n=61 rows (unit = evaluation
rows). UNGATED hard@1: A_sig 51/64 | A_ft 0/64 | **A_keys 30/64** |
**B_keys 31/64** | D_random 16/64. Validity precondition (pinned reading:
A_keys ungated vs random ungated-by-construction) PASSES 30 > 16.

PRIMARY (tau-gated at dev-chosen tau*=0.25 BOTH arms, abstention counted as
miss, paired informative-hard): **10 wins B / 0 reversals / decisive 10 of
61 rows; exact one-sided DECLARED-DIRECTION tail p = 0.000977** — direction
positive but decisive-pair count below the frozen floor of 15 =>
statistic status INDETERMINATE_BELOW_FLOOR (p <= 0.05 AND decisive >= 15
is conjunctive; the floor binds). The 10 decisive pairs are rows where
B_keys output above tau while A_keys abstained; both arms' absolute scores
sit mostly under tau* (A_keys known coverage at tau: 2.8%, B_keys 26.4%),
reproducing G-H7's universal-abstention pathology on the baseline side even
under abstention-as-miss semantics. (Round 0 committed p=1.0 for this cell
under the removed smaller-side tail — see section 0b.)

SECONDARY (all-ungated, same slice): **10 W / 9 R over 19 decisive pairs,
declared-direction p = 0.500000** (opposite-direction tail 0.676197) —
ordering quality statistically EXACTLY at chance; direction-consistent
(wins >= reversals) but maximally far from separation. (Round 0 reported
"p = 0.676", which was the opposite-side tail under the removed inversion.)

Four-way convention recount (auditor item 29 as repaired by RF-2;
denominators and populations INSIDE `keys_analysis.json` blocks; unit =
evaluation rows). LITERAL grid: gated_hard W10/R0 d10 n=64 · gated_all
W12/R0 d12 n=75 · ungated_hard W10/R9 d19 n=64 · ungated_all W13/R10 d23
n=75. INFORMATIVE-CONDITIONED grid (honestly labeled): same counts on
n=61 / n=72 populations. No reading separates under either convention.

Reference-arm scope disclosure (RF-4): this cycle's A_sig/A_ft reference
arms ranked over ALL 16 store fragments, whereas the frozen G-H7 incumbent
site-scopes its candidate list (`bank.site_frags`). Offline deterministic
recount with a faithfulness gate (unscoped recomputation reproduces every
committed top1 exactly): **A_sig hard@1 unscoped 51/64 vs site-scoped-
equivalent 53/64**; flipped rows exactly `q.rootpager@Q_ROOT_AUTH` p1/p2
(unscoped picks fragment 3 books → scoped fragment 10 quotes within truth
[9,10]); A_ft 0/64 under both conventions. These arms are REFERENCE ONLY,
no gate consumes them, and the divergence is anti-self-serving; the
unscoped columns are NOT directly comparable to G-H7's numbers without
this label.

False accepts at chosen taus (expected-UNKNOWN discipline): 0/3 unknown rows
BOTH text arms (single expected-UNKNOWN qid family; n disclosed). Zero FA
gate GREEN for both.

recall@pool == recall@library (N=16 <= M=20; losses are ordering-only):
61/61 hard-informative rows for A_keys, B_keys and D_random alike.

Cluster-level (report-only, NEVER pooled): gated wins concentrate where
B_keys scores clear tau and A_keys does not — CATEGORY 5W/0R d5 (p=0.03125),
PAGER 5W/0R d5 (p=0.03125); AUTH/HOME/OPENBOOK/TAG all d0 gated. Ungated:
PAGER 8W/0R (declared-direction p = 0.003906 — the one genuinely
induced-key-aligned family), offset by AUTH 0W/2R (p=1.0), CATEGORY
0W/2R (p=1.0), HOME 1W/3R (p=0.9375), TAG 1W/2R (p=0.875), OPENBOOK 0/0.
NO cluster satisfies the mechanical separation predicate under any reading:
every direction-positive cell (largest: PAGER ungated d=8) sits far below
the conjunctive 15-decisive floor despite small tails, and clusters are
never pooled into a claim.

## 3. Mandated attribution (FALSIFIED-style decomposition attached to the INDETERMINATE outcome)

- EMPTY-CANDIDATE: excluded — recall@pool 61/61 everywhere.
- BAD-ORDERING: the dominant proximate cause — ungated pairing balanced
  (10W/9R); induced keys did not order truth-first more often than auto
  descs beyond noise.
- EMBEDDER/STACK CEILING: substantial — DEV-only ORACLE_DIAGNOSTIC (keys :=
  union of dev desc texts of truly-solved qids; attribution-only, never a
  mechanism claim) reaches only 41/61 informative-hard vs A_keys 35/61 on
  dev: even maximally task-aligned keys add ~6 rows under the frozen stack.
- REPRESENTATION GEOMETRY: fired exactly as pre-declared — duplicate-step
  fragments collapse to IDENTICAL induced keys (median top1-top2 margin
  0.0055 -> 0.0000 for K_reg/K_full; pairwise cos>0.9 tail 2 -> 6 pairs),
  and K variants churned 58-61/61 top-3 sets vs A_keys on dev.
- DEV variant screen (selection-once, ledgered): ALL induced variants
  scored BELOW the auto-desc baseline on dev informative-hard ungated —
  K_aff 26/61, K_reg 28/61, K_full 31/61 vs A_keys 35/61; argmax selected
  K_full per the frozen procedure.
- Provenance decomposition projections (ungated informative-hard hits):
  AFF-only 25/61 · ENTRY-only 15/61 · EFF-only 26/61 vs pooled B_keys 31 —
  no single token class carries the (small) pooled margin; the wording cap
  machinery was not needed because nothing separated anywhere.

## 4. Execution-level outcomes (48 rows; cells = composite x pos x pass)

- Conversion (ADOPT requirement): median novel_delta difference
  B_keys − A_keys over commonly solved cells = **−0.0** across 19 common
  cells (n_cells>=1, median NOT < 0) => ZERO conversion, same shape as
  G-H7's C−B result.
- Signature-regime regression checks: A_std − B_keys median −1.0 (19 cells);
  A_strict − B_keys median −1.0 (19 cells) — incumbents pay FEWER novel
  actions than B_keys on commonly solved cells; NO incumbent regression.
- Memory-led end-to-end (report-all, unit = arm x composite x pass rows):
  A_strict 8/12 · A_std 8/12 · A_keys 0/12 · B_keys 0/12 — the exact
  goal_sig incumbent remains dominant wherever mapped signatures exist,
  replicating G-H7's execution hierarchy on the new instruments.
- Economics vector (rides WITH results; hygiene only): per-run
  retrieval_us medians A_strict 332.5 / A_std 320.0 / A_keys 1650.0 /
  B_keys 1509.5 — the embedding stack costs ~5x the exact-sig lookup per
  run (perf_counter µs fields; integer flooring upstream; NO latency/
  wall-clock claim licensed anywhere). No summarizer exists in this
  program: would-be LLM calls are 0 BY CONSTRUCTION. Key derivation cost:
  offline deterministic rules, zero live calls.

## 5. Sensitivity recounts (all GREEN; sign-invariance holds)

Duplicate-goal_sig collapse recount sign-invariant TRUE; tie-flip recount
(higher-id-wins re-ranking, driver-side `keys_tiesensitivity.json`)
sign-invariant TRUE; id10 sensitivity kept-row recount recorded beside the
headline (`keys_analysis.json id10_sensitivity`). Truth-set stability vs
G-H7: identical on 25/25 qids.

## 6. Deviations & provenance (labeled; nothing hidden)

1. ITEM-29 ANALYZER PARITY CORRECTION (section 0a) — conservative direction,
   pre-report, disclosed here and in manifest notes[].
2. REPAIR ROUND 1 (section 0b; audit CYCLE_32925866227 REVISE RF-1..RF-5) —
   sign-test statistic repaired to the prereg s8 declared-direction tail;
   four-way recount relabeled to literal populations plus an
   honestly-labeled informative-conditioned block; recount parity coverage
   extended to every derived-statistic class (23 classes, green); report/
   claim tables/G-H8 proposal regenerated from byte-identical raw rows.
   Representation-only: frozen question, task set, instruments, taus,
   verdict rule and all raw artifacts UNCHANGED (raw sha256 pins identical
   to round 0).
3. POST-FREEZE DRIVER CHANGE (RF-3 disclosure): `run_keys_retrieval_confirm.py`
   received a metadata-only `pool_ids` source fix at commit b80394d —
   D_random's per-row pool list is read from `banks["A_keys"]` (the bank
   `FR.random_rank` actually samples) instead of the nonexistent
   `banks["D_random"]` key, which would have raised KeyError in freeze-time
   code. Statistics-neutral by construction (same-site fragment-id list
   under either source); made BEFORE any analysis/report existed; now
   disclosed here and in manifest notes[].
4. REFERENCE-ARM SCOPE DIVERGENCE (RF-4 disclosure): A_sig/A_ft ranked over
   ALL 16 fragments vs the G-H7 site-scoped incumbent; quantified in
   section 2 and `keys_analysis.json reference_arm_scope_recount` with a
   green faithfulness gate. Reference-only arms; no gate consumes them;
   unscoped columns labeled non-comparable-to-G-H7 without this note.
5. Runner shell timeouts killed two chunk invocations mid-pass
   (books_p1/pass1 once; books_p2 once) — INFRA_INTERRUPTED-class events
   with ZERO completed-row loss (idempotent chunks resumed; final grid has
   48/48 rows, zero error fields). One transient Node.js crash inside a
   browser session produced no row and was retried cleanly.
6. First calibration finalize produced the canonical artifacts on the FIRST
   completed pass (no partial-pass discards needed).
7. Spent-instrument discipline: fused-dev/confirm-4a and ALL earlier sets
   untouched; no quantitative claim reuses them.

## 7. What this cycle establishes (maximum defensible wording)

> Under preregistered program `graph-addressing-key-induction` (freeze
> commit 9108ba3 before any observation; fifth-authorship instruments;
> accepted KB byte-restored, no growth; truth sets bit-identical to G-H7's
> on all 25 qids; 75 retrieval query instances; 48 execution rows across 6
> composites x 4 arms x 2 deterministic passes, pass-identical 24/24), the
> keys-vs-baseline contrast resolves **INDETERMINATE at the declared
> primary statistic**: mechanically induced richer keys (rules v1, K_full)
> did NOT separate from the auto-derived-description baseline under the
> frozen lexical-hash+MMR machinery (primary tau-gated paired statistic
> 10W/0R, declared-direction exact tail p=0.000977 but only 10 decisive
> pairs of 61 — below the pre-declared floor of 15, which the freeze maps
> to INDETERMINATE, never falsified; secondary all-ungated 10W/9R,
> declared-direction p=0.500000 — exactly chance). Zero execution
> conversion at matched subgoal success (median novel diff -0.0 over 19
> common cells), zero expected-UNKNOWN false accepts both arms, no
> signature-regime regression, and the exact goal_sig incumbent remains
> dominant (memory-led 8/12 composite x pass rows at fewer novel actions
> vs 0/12 for both text arms). Attribution attaches the mandated
> decomposition: candidate generation was never the binding constraint
> (recall@pool 61/61); ordering is at chance under the corrected statistic,
> the embedder/stack ceiling sits ~6 informative-hard rows above the
> baseline (oracle diagnostic 41/61 vs 35/61), and duplicate-key geometry
> collapse is real (margin -> 0.0). Induced keys rules v1 are NOT adopted
> into the Graph product path; exact addressing stays standard for
> signature consumers; no NL-consumer option is licensed. Whether ANY key
> representation can move this regime is bounded by the ceiling finding:
> at this library scale the stack itself, not key construction alone, is
> near its limit.

### Binding limits traveling with any citation

Two scripted demo sites; ONE 16-fragment KB (pool M=20 >= N makes pool ==
library); lexical-hash embedder regime ONLY (neural survival OPEN and now
ATTRIBUTION-BOUNDED by the oracle diagnostic); scripted deterministic
consumers; same-lab model-family fifth-authorship instruments (NOT human-
independent); n=2 deterministic passes = determinism only; µs fields
hygiene-only, no latency claim; single expected-UNKNOWN qid family sets the
FA gate; INDETERMINATE is statistic-level at THIS setting and does not
falsify key induction elsewhere; DEV screening numbers are decision-
procedure outputs, not unbiased estimates (auditor item 26 discipline).

## 8. Proposed GRAPH_LEDGER entry G-H8 (for Director integration)

Status: PROPOSED wording for Director integration, pending independent
re-audit of repair round 1 (round-0 audit CYCLE_32925866227 returned REVISE
on representation defects only — invalid p-values, mislabeled recount
populations, two undisclosed deviations, parity coverage gap; all repaired;
verdict invariant). Program COMPLETE at its horizon via the INDETERMINATE
branch (statistic-level, floors binding) with substantive report-all
negatives integrated honestly. Corrected statistics travel with the entry:
primary tau-gated informative-hard paired 10W/0R decisive=10 < floor 15 →
INDETERMINATE_BELOW_FLOOR (declared-direction exact tail 0.000977);
secondary ungated 10W/9R declared-direction p=0.500000; four-way literal
gated_all d12 / ungated_all d23 — nothing separates anywhere. Keys stay
auto-derived; induced keys rules v1 NOT adopted; no NL-consumer option
licensed. Design lesson frozen for successors: at 16-fragment library scale
the lexical-hash stack is within ~6 informative-hard rows of its
task-aligned ceiling (oracle diagnostic), duplicate-prone key induction
collapses geometry, and the residual discriminative residual lives BELOW
the key layer — embedder/representation successors need their own
preregistration, fresh instruments and probably a larger-library substrate
before the key-layer question can be re-asked decisively.

## 9. Evidence index

graph/prereg_key_induction.md · graph/paraphrases_keys_{dev,confirm}.json +
verbatim prompts · graph/{induced_keys,tasks_keys,keys_eval}.py · drivers
graph/{run_keys_calibration,screen_keys_dev,run_keys_retrieval_confirm,
run_keys_live,keys_tiesensitivity}.py · graph/{analyze_keys,
make_claim_tables,recount_keys,make_keys_manifest}.py · tests/
test_graph_keys.py (23/23 green incl. RF-1 declared-direction regression
tests; full suite green except the documented pre-existing Physics fixture
failure identical to audited baseline) · results/graph/keys_* (canonical
artifacts, sha256-pinned in results/graph/keys_MANIFEST.json; raw evidence
pins identical to round 0) · claims table results/graph/keys_claim_tables.md
· independent recount results/graph/keys_RECOUNT.json (all_parity_ok=true
over 23 derived-statistic classes) · rejected round-0 provenance preserved
under results/graph/provenance/*REJECTED_ROUND0* and at origin/cycle/graph/
32925866227/team @ 4fb87c0.
