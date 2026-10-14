# EXP-GRAPH-38530149021 preregistration — Graph sensitivity packet: screen re-inclusion + cross-surface lexicon (DESIGN, design_contract_version 2)

## 0. Mandate, inherited state, and legacy position

- Binding direction: `request.json#director_mandate` (cycle `38529778944`, Graph `REOPEN` with cognitive_reset `true`, claim `C-SEMANTIC-RESOLVE`, parent_handoff_disposition `USE`). The Director's strategic question is converted here into the smallest rigorous falsifiable experiment; no drift to a nearby objective.
- Director question (binding): does the DECIDE_REQUIRE_RETRIEVAL_B bound survive a pre-registered sensitivity packet that (a) re-includes the frozen-screen-dropped TEST rows and (b) removes the gold-lexicon asymmetry via a blind or cross-surface lexicon arm, isolating whether the G2 one-row margin and the TFRAME_DOMINATES_G3 fork are robust or artifacts of screening and information asymmetry? Honest out-of-sample retrieval fit required (FIT-TRAIN>=78, disjoint FIT-SELECT, mu>0, resubstitution forbidden); exclusive unknown_precision denominator fixed pre-freeze.
- Smallest batch per mandate: single sensitivity packet on the already-constructed frozen banks. No new anchor/surface collection, no clause refit (mandate stop trigger: any refit of the deterministic clause set converts this from a no-refit structural-bound test into a new architecture experiment and is out of scope → BLOCKED, never silent redesign). Fit-pool construction is identical to the parent by code identity (DESIGN-quoted 102/34/60).
- This is a sensitivity transaction, not a rerun and not a repeat of an invalid design: the screened gold leg is a disclosed validity-transaction reproduction (parent RQF-04 continuity); NEW evidence comes from (a) the reincluded-superset gate vector, (b) the cross-surface lexicon arm, and (c) the reincluded retrieval fork. It varies exactly the screening/asymmetry factors the parent verdict flagged as confounds.
- Parent handoff preserved (`research/experiments/EXP-GRAPH-38446557638/handoff.json`, sha `ca722b25a86be1e898f52aa7b3d7b3ea61b5410c9b62a98c426c5652756ce9f3`): `established` (4 items: byte-identical runner validity repair with audit PASS; bounded screened outcome G3-met/G2-false-solely-on-UP-10/12/G1-met with selection_preserved; honest-retrieval leg SELECT-feasible yet failing every TEST gate with fork TFRAME_DOMINATES_G3; no product promotion), `rejected` (3 items: BROAD/SCOPED ship branches on this gate vector; honest-retrieval viability for the specific pooled TF-IDF comparator at the frozen gates; nothing broader), `unknown` (6 items: G2-margin stability under perturbation; pooled-dilution vs intrinsic weakness; other SELECT-feasible gates under a different selection rule; survival without surface gold lexicons; G1 duplication bias; screen re-inclusion gate values), and `do_not_assume` (7 guards, incl. no elevation from COMPLETE/MIXED, no inclusive-denominator gating, no general retrieval reading of the fork, no new-evidence reading of the Arm A reproduction, no generalization beyond frozen banks/splits/screen, correct gate-vector parent identity EXP-GRAPH-38291080992, no product re-run of this design) are carried forward unchanged. This packet directly resolves parent `unknown` items 1, 4, 6 and the FIX-1 lexicon-asymmetry binding by measurement rather than by carried prose.
- Grandparent context (continuity only): `EXP-GRAPH-38291080992` gate-vector parent (audit FIX-2 continuity); direct parent `EXP-GRAPH-38385040804` is BLOCKED with metrics={} and is never cited as a measurement source.
- Legacy position (`LEGACY: DISTINCT_EXTENSION`): DESIGN searched `codex/legacy_artifact_index.json` (1401 artifacts) for `cross-surface|blind lexicon|reinclu|unknown_precision|abstention`: **0 hits** — no pre-2.0 screen-reinclusion or blind-lexicon experiment exists. Targeted primary-source check of the mounted `.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md` (21,974,490 chars) for `unknown_precision|cross-surface lexicon|blind lexicon|screen-dropped|re-inclu`: **0 hits** in all five patterns. Nearest neighbors (Director-concurred): `P2-BLIND-COMPOSITION` (pre2 product summary artifact 4.697, sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`: 3/3 unseen compositions vs 0/3 weak baselines, keyword/oracle confounds) and `P2-MIND2WEB` (archived Codex §1: 6/176 exact matches, 47/176 retrieval). Neither fixes an abstention-precision denominator, re-includes screen-dropped rows, nor tests a cross-surface lexicon; this packet adds all three. Independent extension with materially improved validity; not a duplicate. Absence of an index hit is not claimed as proof of absence from the full archive (brief guard).

## 1. Hypotheses (single frozen texts)

- H1 (screen-robustness of the published no-refit bound): on the frozen banks with the frozen zero-tunable-parameter clause set, the gold-lexicon gate vector is invariant when the frozen-screen-dropped TEST rows are re-included: `AXIS-G3-NEW` gate-met, `AXIS-G1-PRIMARY` gate-met, `AXIS-G1-ALTLEX` gate-met, `selection_preserved=true` (selective_acc>=0.80 all axes, reincluded), and `AXIS-G2-RETEST` gate-false SOLELY on `unknown_precision_exclusive<0.85` (FA and coverage passing). The G2 margin carries analytically: parent-published flagged rows on G2 are zero, runtime-verified as `g2_reincl_identical`.
- H2 (fork robustness): `B-RETRIEVAL-OOS` — centroids+IDF fit on pooled calibration FIT-TRAIN (n=102), gate `(tau,mu)` selected on disjoint pooled FIT-SELECT under hard `mu>0`, applied frozen to screened and reincluded tests — yields the same `AXIS-G3-NEW` fork on both supersets (parent-published `TFRAME_DOMINATES_G3`, reproduced first as a validity tripwire).
- H3 (lexicon asymmetry, graded co-finding): `XSURF-CROSS` — identical frozen clause code, each axis scored under a fixed foreign-surface lexicon (derangement `G3->LEXICON-G1, G2->LEXICON-G3, G1-PRIMARY/G1-ALTLEX->LEXICON-G2-HELDOUT`, no self-match) — collapses at the coverage floor while gold passes (`gold_dependent=true`), confirming the published fork is gold-lexicon-conditional (parent audit FIX-1 measured, not carried). Any preserved cross gate strengthens lexicon-generality without promoting.
- Expectation from parent-published evidence and DESIGN CAL probes (NOT results): screened reproduction holds deterministically (bound persists on screened sets); screen flips are genuinely open on G3-UP/G1-FA; `fork_reincl` is genuinely open; cross collapse is expected (DESIGN CAL probe, §8.1: cross resolved 0/60 G3, 1/60 G2, 11/80 G1) and is pre-declared VALID collapse, never invalidity.
- Falsifier (frozen): H1 SUPPORTED (BOUND_ROBUST side) iff `screen_stable` (gold-reincluded gates equal gold-screened gates on all four axes AND `selection_reincl == selection_preserved`) AND `fork_stable` (`fork_reincl == fork_screened`). H1/H2 FALSIFIED as artifacts (BOUND_ARTIFACT) if any gold gate or selection flips screened->reincluded (`screen_artifact=true`) or the fork flips (`fork_artifact=true`). Gating any decision on `unknown_precision_inclusive` is pre-declared invalid (parent RQF-02 continuity); inclusive is sensitivity-only (§6).

## 2. Treatment: T-FRAME+ gold (frozen, disclosed reproduction) + XSURF-CROSS variant (no refit)

- Arm A-gold = `B-LEX-STRONG` shared deterministic selector + structural abstention clauses `C1-SUBOP/C3-NO-REFERENCE/C4-COMPLEMENT/C5-SET-QUANT/C6-SOURCE` + `C7-CREATE-OBLIQUE`, all zero tunable parameters. Analysis functions (`comp/frame/clause_c7/is_executed/metrics`) are byte-identical to the audited parent `CANONICAL-RUNNER-SHA256 4c412aec6ba21c9d1733ccb1d5e1105ea62bf116395a142ce72ddb9651f9a7b8` lineage; only EXP_ID/SEED constants and the pre-declared sensitivity additions of this section differ (reincluded-set construction, cross-surface rescoring, reincluded fork, reproduction tripwires, `fork_of`/`arm_gate` helpers). AUDIT can diff raw_evidence runners directly.
- Arm A-cross (XSURF-CROSS) = identical clause code, foreign lexicon only. Fixed derangement (frozen `XSURF` map, §13): G3 rows under `LEXICON-G1`, G2 rows under `LEXICON-G3`, G1 rows (both PRIMARY and ALTLEX axes, which share identical texts) under `LEXICON-G2-HELDOUT`. No surface is scored with its own lexicon; PRIMARY/ALTLEX share the same foreign lexicon so their text-identity comparison stays clean. The screen is lexicon-independent (text similarity vs frozen priors), so cross flagged-gid sets must equal gold flagged-gid sets; divergence is a runner-enforced invalidity tripwire (`screen-lexicon-divergence`, impossible by construction, guards implementation bugs).
- No-refit stop rule (mandate): the runner contains no clause-refit path. Any refit of the deterministic clause set observed at any stage converts scope to BLOCKED (new architecture experiment), never a silent redesign.
- Liveness (gold-screened scope, unchanged from parent): `LIVE = (0<executed_total_test<n_total_test) AND (executed_app_test>=1) AND (abstained_resolved_test>=1)` on gold-screened `AXIS-G3-NEW` TEST only. Cross degeneracy (zero executes, zero resolved abstentions, UP-undefined) is pre-declared VALID collapse: `gate_met` already returns false via the coverage bar, so no undefined-gate branch exists.

## 3. Comparator: Arm B-OOS (honest, unchanged construction, applied to both supersets)

- Mechanism (stdlib only): word unigram + adjacent-bigram features; IDF from FIT-TRAIN app rows only; per-class L2-normalised centroids; prediction = nearest centroid; confidence = top cosine; margin = top minus second. Distinct implementation from Arm A; shares no fitted state; never the cost denominator of Arm A.
- FIT pool (frozen construction, identical to parent by code identity): pool = `AXIS-G1-PRIMARY` cal + `AXIS-G2-RETEST` cal + `AXIS-G3-NEW` cal (one G1 axis only, avoiding duplicate texts with ALTLEX). Nested split: every 4th pooled-app row (global order G1,G2,G3; `idx%4==3`) to FIT-SELECT (34 app rows); remainder to FIT-TRAIN (102 app rows); ALL pooled cal-OOS to FIT-SELECT (60 rows). Gate `(tau,mu)` searched on FIT-SELECT only (lexicographic maximise-feasibility-then-coverage, same rule as parent), hard constraint `mu>0` (candidate `round(margin,4)>0` only). Frozen gate applied unchanged to screened tests AND reincluded tests. Parent-published SELECT gate (tau=0.4156, mu=0.0005, mu_active) is quoted as expectation, never inherited: EXECUTE re-fits and re-emits every value.
- Fairness disclosure (pre-registered, for AUDIT): pooled TRAIN contains same-surface classes for every test axis plus cross-domain distractors (~1.7 train rows/class over ~60 classes); dilution biases AGAINST retrieval (parent continuity). Information asymmetry is now MEASURED rather than carried: gold arms hold surface lexicons while retrieval is lexicon-free (FIX-1), and the XSURF arm quantifies exactly how much of the deterministic performance is lexicon-carried.
- Forbidden fallbacks (violation = BLOCKED, never silent reuse): refitting deterministic clauses; gate search touching TRAIN rows as select rows or any screened-or-reincluded TEST row; `mu==0` gate; ancestor resubstitution values substituted for the OOS leg.
- Infeasibility is informative, not invalid: if no `(tau,mu>0)` is feasible on SELECT, both forks emit `RETRIEVAL_INFEASIBLE_OOS` and the sensitivity verdict still emits.

## 4. Banks, lexicons, priors, screen (reuse by reference; no new collection)

- G3: `LEXICON-G3`, `GOAL-BANK-G3`, `OOS-BANK-G3` read at runtime from frozen `research/experiments/EXP-GRAPH-38291080992/prereg.md` §13.1–13.3 (byte-identical to `38205284279` per parent audit: 3834/6357/3672 chars). Blind-authorship property inherited by identity.
- G1/G2: `GOAL-BANK-G1/OOS-BANK-G1/LEXICON-G1/LEXICON-G1-ALT/GOAL-BANK-G2/OOS-BANK-G2/LEXICON-G2-HELDOUT` from frozen `research/experiments/EXP-GRAPH-38180711589/prereg.md`.
- Priors: `PRIOR-PARENT-BANK-TEXTS` from frozen `research/experiments/EXP-GRAPH-38175554380/prereg.md` + `research/harness/goal_generator.py` vocabularies.
- Contamination screen (frozen, unchanged): token Jaccard>=0.60 OR trigram Jaccard>=0.75 vs frozen priors+banks drops rows from binding (recorded in `flagged`, not counted). Reincluded TEST gids quoted from parent-published `run_output.json#flagged` (no new TEST scoring in DESIGN): G3 test-app `app_026/app_030/app_036/app_076` (+1 cal-app `app_009`, not re-included); G1 per axis test `app_004/app_052/app_076/app_100/oos_024/oos_026` (+3 cal rows, not re-included); G2 zero flagged rows (margin analytic-invariant).

## 5. Axes, splits, reincluded sets, and the frozen fit-pool contract

- Split rule (frozen, deterministic, unchanged): row `i` is test iff `(i%splitmod) in (1,3,5)`; `splitmod` 4 (G3, G2-HELDOUT) / 6 (G1, ALT). Same four axes and roles as parent. Screened bound counts (parent-published): G3 115 (cal 39+20 / test 36+20); G2 120 (cal 40+20 / test 40+20); G1/ALT 151 each (cal 57+20 each).
- Reincluded TEST (frozen): `test_reincl = test + flagged_test` per axis (gold and cross alike). Counts: G3 40 app + 20 OOS; G1/ALT 60 app + 20 OOS; G2 40 + 20 (identical to screened; `g2_reincl_identical` runtime-verified). Reincluded rows are scored post hoc through identical arms; they never enter the screened validity leg and never enter fit/select.
- Fit-pool validity bars (frozen; failure = MEASUREMENT_INVALID/BLOCKED, §7): exact `N_TRAIN==102`, `SELECT_APP==34`, `SELECT_OOS==60` (deterministic; mismatch is bank drift, not tolerance), `TRAIN∩SELECT=∅`, `(TRAIN∪SELECT)∩(screened TEST ∪ reincluded TEST)=∅` (exact text-sha, covering the reincluded union). No TEST row is ever read by Arm A, any clause, the screen, or the retrieval fit/select.

## 6. Metrics, gates, controls (stable identifiers; RQF-02/03/05 continuity)

- Frozen constants: `FA_TARGET=0.10, COV_TARGET=0.50, PREC_TARGET=0.85, SEL_TARGET=0.80, TOK_BAND=0.60, TRI_BAND=0.75, SEED=38530149021%(2**32)=4170410653`.
- Per (axis, set, mode): `coverage, pooled_false_accept, unknown_precision_exclusive (=OOS among resolved-then-abstained / resolved-abstained; null if none → invalidity trigger on gold-screened only), unknown_precision_inclusive (=OOS among all non-executed / all non-executed; SENSITIVITY ONLY, never gated), selective_acc, executed, executed_oos, executed_app, abstained_resolved, unresolved_applicable`.
- PRIMARY gate (sole decision gate, pre-fixed, exclusive only): `pooled_false_accept<=0.10 AND coverage>=0.50 AND unknown_precision_EXCLUSIVE>=0.85`. `selection_preserved = selective_acc>=0.80` on all four axes (screened); `selection_reincl` analogously on reincluded sets. Cross-arm harmonization (parent RQF-05 continuity): Arm B-OOS gates on the same exclusive-formula precision (for retrieval every scored row is decision-conditional, so exclusive==inclusive by construction; both reported).
- Controls (stable ids, parent-continuous, all executed):
  - `PC-AXIS-G1-ALTLEX`: gold-screened gate-met; failure is runner-enforced MEASUREMENT_INVALID (RQF-06 continuity), never a science negative. Reincluded ALTLEX is sensitivity evidence, never the control.
  - `NC-EXEC-ALL` (`gatefree`): must pool materially more FA than Arm A on screened sets (parent TEST 0.2778–0.50 vs 0.0–0.10; DESIGN calibration 0.30–0.60 vs 0.0); re-reported on reincluded and cross sets as sensitivity headroom.
  - `NC-ABSTAIN-ALL`: EXECUTED on screened AND reincluded sets (RQF-03 continuity; no placeholders): executes nothing → `coverage=0.0`, `pooled_false_accept=null`, `unknown_precision_exclusive=OOS_resolved/all_resolved` (informative, not 1.0 by construction).
  - `CTRL-SHUFFLED-SELECTION`, `CTRL-RANDOM-ROLE`: near chance (screened and reincluded gold sets).
  - `CTRL-RANDOM-GATE`: volume-matched random abstention (parent FA 0.65–0.75).
  - `CTRL-B-LEX-ONLY` (gatefree selective_acc), `CTRL-INCUMBENT` (shipped lexical gate FA/selective_acc) on screened and reincluded sets.

## 7. Decision rule and product consequences (frozen sensitivity cascade)

- `MEASUREMENT_INVALID` (`decision=null`) if ANY of §7(a)–(f) in spec.json: liveness fails; gold-screened exclusive UP undefined on any axis; `PC-AXIS-G1-ALTLEX` gold-screened fails (runner-enforced); fit-pool exact counts/disjointness fail (covering the TEST union); any forbidden fallback (resubstitution/mu==0/screened-or-reincluded test-touch/clause refit); screened reproduction fails (gold-screened gate vector != {G3 met, G1 met, ALTLEX met, G2 false-solely-on-UP with FA<=0.10 and coverage>=0.50}, or screened fork != TFRAME_DOMINATES_G3, or screened retrieval fails to fail all four TEST gates, or cross flagged-gid sets diverge from gold). Cross degeneracy is pre-declared VALID collapse. Retrieval-OOS infeasibility is NOT invalid → both forks emit `RETRIEVAL_INFEASIBLE_OOS`, verdict still emits.
- Else: `screen_stable = (gates_reincl==gates on all four axes) AND (selection_reincl==selection_preserved)`; `fork_stable = (fork_reincl==fork_screened)`; `BOUND_ROBUST` iff both, else `BOUND_ARTIFACT` with `artifact_subtype={screen_artifact, fork_artifact}`. Lexicon co-finding (`xgates` vector, per-axis cross coverage/resolved-abstention/UP, `gold_dependent` flag) is mandatory co-evidence shaping `reason` and product consequence.
- Positive (BOUND_ROBUST): keeps the conservative shipped abstention boundary; fork stays resolved toward REQUIRE_RETRIEVAL_B (retrieval-B requirement remains vacated as specified); G2 margin verified screen-invariant. Ceiling stays gold-lexicon-conditional under expected `gold_dependent=true`, reopening blind/cross-surface resolver work without promotion; unexpected cross preservation strengthens lexicon-generality, still without promotion. This packet promotes nothing itself.
- Negative (BOUND_ARTIFACT): the published margin and/or fork are artifacts of screening and/or fork-choice as subtyped. Ship/no-ship branch and retrieval-B requirement return to the Director; Graph reopens the resolver architecture question. HYPOTHESIS retained with narrowed ceiling. INVALID/BLOCKED retires or parks the family per the mandate stop rule. This packet promotes nothing itself.

## 8. Design satisfiability probes (calibration/construction/synthetic evidence only; NO TEST gate/fork/decision outcome of THIS experiment computed in DESIGN)

All probes touch calibration rows, frozen bank construction, published parent values, or synthetic inputs only. The new runner's `--mechanics-only` entry point never calls `metrics()` on any TEST set and never runs `arm_b_oos` with tests (verified in probe output). No confirmatory measurement was run.

**8.1 Treatment liveness + asymmetry-arm discrimination (PASS, by actual execution).** (a) The NEW runner's `--mechanics-only` entry point (extracted §13 block + one trailing newline) was EXECUTED twice pre-freeze: both exit 0, byte-identical stdout (sha256 `9251f48e0212196b2d0f4a51d54bb0a7ae5f3e59c6fc0b8b384f78457393dfc2`), `status=DESIGN-MECHANICS-ONLY`, `test_not_scored=true`, empty stderr — the sensitivity additions (reincluded-set construction, cross-surface rescoring of CAL rows, reincluded-count enumeration) execute cleanly. Measured new-runner construction: N_TRAIN=102/SELECT_APP=34/SELECT_OOS=60 exact, both disjointness checks true (TEST union covers screened+reincluded), xdiv empty, g2_reincl_identical true, flagged_test gids identical to parent-published lists (G3 4 app, G1 6 per axis, G2 0; cross sets equal); new-runner xcal tframeplus: G3 0 executes/0 resolved abstentions (floor collapse, UP null pre-handled as gate-false), G2 0/1, G1 8/3 at coverage 0.1404 (ALTLEX identical); retrieval_select feasible tau=0.4156 mu=0.0005 mu_active=true. (b) Gold liveness predicate semantics verified against parent-published G3-test counts (38 executed of 56; 36 applicable; 7 resolved abstentions → True) while execute-all (`abstained_resolved=0`), abstain-all (`executed_total=0`), and selector-degenerate analogues evaluate False. (c) Gold calibration non-degeneracy DESIGN-measured (parent probe continuity): G3 38/39 app, G2 35 executed coverage 0.875, G1 0.8596, ALTLEX 0.9123. (d) XSURF discrimination probe on CAL rows only (stdin probe, no TEST rows read): G3-cross resolved 0/60 (coverage 0.0, abstR 0, UP null → pre-handled gate-false); G2-cross resolved 1/60, executed 0, abstR 1; G1-cross resolved 11/80, executed 8, coverage 0.1333, abstR 3, UP 1.0 — the asymmetry arm is implemented and discriminating (collapses directionally, parses partially where shared vocabulary permits), not dead code; its TEST collapse is a live informative outcome, and any TEST preservation is genuinely open. (e) Retrieval SELECT-gate feasibility quoted from parent (tau=0.4156, mu=0.0005>0 active) with identical fit code; EXECUTE re-fits and re-emits.

**8.2 C7 non-vacuity and zero applicable cost (PASS, parent continuity).** C7 fires on 0 applicable rows on every axis; on OOS rows: 2 G3 / 4 G2 / 2 G1 / 1 ALT (parent bound totals). Zero tunable parameters. Parent TEST structural facts quoted for the falsifier baseline only: C7 strictly reduced G3 TEST FA 0.20→0.10 and G2 TEST FA 0.10→0.00.

**8.3 Decision-rule reachability (PASS, synthetic enumeration).** Frozen rule enumerated over all boolean input combinations without touching frozen data: BOUND_ROBUST, BOUND_ARTIFACT (screen-only, fork-only, both subtypes), and null-invalid via any of the six invalidity triggers are all reachable; no subsumed guard (`screen_stable` and `fork_stable` are independent conjuncts over disjoint inputs: reincluded gold gates vs reincluded fork). Reproduction tripwires (screened vector, screened fork, exact fit counts, flagged-gid equality) are expected-pass drift detectors, not science branches. The G2 margin is analytically screen-invariant (zero G2 flagged TEST rows, runtime-verified `g2_reincl_identical`); its lexicon exposure is live via `xgates[G2]`.

**8.4 Arithmetic attainability (PASS).** Reinclusion exposures quantified from parent-published counts: G3 +4 app (FA denominator unchanged at 20; UP flip 7/7→7/9 needs ≥2 new resolved abstentions — open); G1 +4 app/+2 OOS per axis (FA 1/18→{1,2,3}/20: flip needs 2/2 new OOS executes — open; UP 4/4 dilution live; coverage 53/56→needs ≥30/60 — headroom); G2 +0 (identical). Fork_reincl open (retrieval lexicon-free on both supersets). Fit-pool bars exact and attainable (102/34/60 by code identity). Gatefree headroom on screened sets (0.30–0.60 FA vs 0.0) extends to reincluded/cross sets as reported controls.

**8.5 Baseline / comparator identity (PASS).** Six baselines/identities plus one treatment variant are distinct implementations (deterministic structure ± C7; foreign-lexicon rescoring with identical clause code but disjoint lexical state; lexical incumbent; execute-all; pooled-centroid retrieval with disjoint fit/select/screened-test/reincluded-test); ancestors resub/embedding are non-decision identities. Arm A reads no calibration pool and no TEST row in fit; Arm B reads no clause state; cross arm shares clause code with gold but disjoint lexicons and is never a cost denominator. Reproduction tripwires verify identity at runtime (screened vector, screened fork, exact fit counts).

**8.6 Control sensitivity (PASS, parent values quoted as baselines + new sensitivity controls).** NC-EXEC-ALL gap (DESIGN calibration 0.30–0.60 vs 0.0; parent TEST 0.2222–0.50) re-measured on reincluded and cross sets; random-gate parent FA 0.65–0.75; shuffled/random near chance on screened and reincluded gold sets; abstain-all executed on both supersets (coverage 0.0 floor, UP informative) so both degeneracy directions are live twice; PC runner-enforced as invalidity. Cross floor collapse is the pre-registered treatment-variant outcome (§8.1d), not a control. No insensitive control.

**8.7 Measurement prerequisites (PASS, probed without outcome measurement).** Python 3.12.15; new runner imports stdlib-only (`argparse/hashlib/json/math/os/re/random/sys/pathlib/__future__`) + one repo-local `goal_generator` import inside `main()`; numpy/sklearn/sentence_transformers absent (import probes raise ModuleNotFoundError); `goal_generator` exposes INTENTS(20)/PARAPHRASES(20)/NO_APPLICABLE_TEMPLATES(20)/OOD_PARAPHRASES(8); every runtime-read block verified present in its exact file (G1/G2/lexicons in `38180711589/prereg.md`; `PRIOR-PARENT-BANK-TEXTS` in `38175554380/prereg.md`; G3 blocks in `38291080992/prereg.md`); reincluded TEST gids quoted from parent-published `run_output.json#flagged` (G3 4 test-app; G1 4 test-app + 2 test-OOS per axis; G2 0); fit-pool construction identical to parent by code identity (136 pooled cal-app → 102/34/60); no network/model/browser/credential; the mandate stop trigger (clause refit) has no code path.

**8.8 Freeze artifacts bounded (PASS).** Exactly the four mutable local interpretation dependencies in `spec.json#freeze_artifacts` (§12); DESIGN-verified sha256 all match parent `freeze.json#artifact_hashes` (files unchanged); runner, banks, lexicons, XSURF map and constants otherwise bound via this prereg's hash (§13) + runtime self-hash.

**8.9 Self-attack (declared threats, not failures).** C7 triggers could over-abstain on unseen benign idioms (0 applicable rows in frozen banks; would surface as reduced coverage, not FA). G3 applicable bank structurally simple by construction — fairness test of abstention, not hard parsing; OOS half is discriminating (gatefree FA 0.30 cal / 0.45 TEST). Reincluded rows are similarity-flagged by construction (near-duplicates of priors): gold handling of near-duplicates is exactly the stress under test; retrieval faces the same superset symmetrically. Pooled-retrieval dilution biases against retrieval (disclosed §3; audit to adjudicate collapse readings). SELECT selective_acc=0/32 co-reported (parent): the SELECT gate is feasible on FA/COV/UP but retrieval classification is weak — the frozen forks judge gate-level viability only. G1-PRIMARY/ALTLEX text-identity persists (three independent surfaces, not four; both share the same foreign lexicon under XSURF). Cross collapse at zero-resolved (G3) yields UP-null → gate-false via coverage bar (pre-handled, reported as floor collapse, never undefined).

**8.10 Empty-branch / identity / ceiling audit (PASS — active disproof attempt recorded).** Attacked and cleared: (i) no empty decision branch — synthetic enumeration reaches BOUND_ROBUST/BOUND_ARTIFACT(all subtypes)/null-invalid; BOUND_ROBUST requires screen+fork stability (both empirically live per §8.4), BOUND_ARTIFACT requires either flip (both live); screened reproduction legs are expected-pass validity tripwires, and the live sensitivity/fork/lexicon measurements change the product state on every branch; the lexicon co-finding is graded (COLLAPSED/PARTIAL/PRESERVED per axis, §8.1d shows PARTIAL live on G1-cal) and modulates consequence text rather than gating a label, so no label depends on the near-certain COLLAPSED leg alone. (ii) no treatment/comparator identity — disjoint code paths, disjoint fitted/test data, runtime tripwires, §8.5. (iii) no ceiling baseline — gatefree headroom on all three set families. (iv) no insensitive control — §8.6. (v) no missing prerequisite — §8.7. (vi) no unbound mutable artifact — §8.8 (four files, hashes verified). Gating on inclusive would manufacture BROAD without evidence — forbidden by the falsifier. Refitting clauses or resubstitution would repeat confounded/out-of-scope designs — forbidden (BLOCKED). Repeating the parent's exact frozen design without the sensitivity factors would be a DUPLICATE — this packet varies exactly the two Director-mandated factors.

## 9. Cost and expected information gain

- Cost: no model calls/network/browser/packages/authorship; one deterministic run over ~500 bound rows + 14 reincluded TEST rows + cross-surface rescoring + pooled fit (199 cal rows) + nested gate search; seconds of CPU.
- Gain: one batch decides the Director's sensitivity question. Predicted VALID BOUND_ROBUST with `gold_dependent=true` keeps the conservative boundary, keeps the fork resolved toward REQUIRE_RETRIEVAL_B (vacated as specified), and authorizes blind-resolver work without promotion. BOUND_ARTIFACT (screen and/or fork flip) retires the published vector/fork reading and returns ship/no-ship plus retrieval-B to the Director with the subtype localizing the artifact. A second INVALID/BLOCKED retires or parks the family. Screened reproduction is disclosed non-evidence; every sensitivity branch changes the claim or product state.

## 10. Environment and EXECUTE command

- Python 3.12.15, stdlib only. EXECUTE extracts `FROZEN-RUNNER` (§13) to `raw_evidence/runner_tframe_sensitivity.py` (block bytes + exactly one trailing newline; sha256 must equal `CANONICAL-RUNNER-SHA256 = 89baf53026da8b33d80bf891a7c116b69b5bec8f60c9ae55a3ef8c484984ce29`), then:
  `python3 research/experiments/EXP-GRAPH-38530149021/raw_evidence/runner_tframe_sensitivity.py --mechanics-only` (twice; byte-identical required; TEST gates/forks/decisions never computed — DESIGN probe already demonstrates rc=0 byte-identical) →
  `python3 research/experiments/EXP-GRAPH-38530149021/raw_evidence/runner_tframe_sensitivity.py > research/experiments/EXP-GRAPH-38530149021/raw_evidence/run_output.json`
- Determinism: fixed `SEED=4170410653`; no wall-clock/RNG-dependent state beyond `random.Random(SEED)`. EXECUTE writes `result.json/report.md/provenance.json` from `run_output.json` only, preserving stable metric/control identifiers from §6.

## 11. Runner identity and environment notes

- `CANONICAL-RUNNER-SHA256 = 89baf53026da8b33d80bf891a7c116b69b5bec8f60c9ae55a3ef8c484984ce29` is the sha256 of the extracted runner file (FROZEN-RUNNER block + one trailing newline), computed at DESIGN end from the frozen block bytes after the §8.1 execution gate; the DESIGN probe's `runner_self_sha` equals it. EXECUTE verifies it (`runner_self_sha`) and AUDIT re-verifies with byte-identical reruns plus a diff against the parent runner scoping the pre-declared deltas (§2).
- `SPIDER_PREREG` env override (default: this experiment's `prereg.md`) is reserved for byte-identity checks only; the scored run uses the default.

## 12. Freeze artifacts (v2)

`spec.json#freeze_artifacts` lists the exact repository-relative mutable files whose identity can change the interpretation; each MUST be hashed into `freeze.json.artifact_hashes` and is immutable for the EXECUTE transaction:
- `research/experiments/EXP-GRAPH-38180711589/prereg.md` (G1/G2 banks + lexicons; DESIGN sha `5a64e90da4d1c13b4a290b988cc6096838119d09869abd69512d095cd9318cb0`)
- `research/experiments/EXP-GRAPH-38175554380/prereg.md` (prior-bank texts; DESIGN sha `dc90bf71ed03a2329b641d46c1f4f70a53dbeef95ebd6d688645f697868aff9b`)
- `research/experiments/EXP-GRAPH-38291080992/prereg.md` (G3 banks + lexicon, reuse by reference; DESIGN sha `5a9cc1190674ffa5a8e6d604f6735ae6a9e2e27ffc9358c82d263f51b43d5735`)
- `research/harness/goal_generator.py` (contamination priors; DESIGN sha `cb5218de6a992cf29e26eee8fd5be4b4d7a50084ac3b885587a8ee1da20ace5f`)
All other inputs (runner, constants, XSURF map, rules) are embedded in §13 and hashed via this prereg.

## 13. FROZEN-RUNNER (the exact frozen treatment + sensitivity legs + honest comparator; hashed at freeze)

<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38530149021 (design_contract_version 2).
# Sensitivity packet: (a) screen re-inclusion (test_reincl = screened test + flagged TEST rows),
# (b) cross-surface lexicon arm XSURF (identical clause code, fixed foreign lexicon, no self-match).
# Arm A-gold = T-FRAME+ : shared deterministic lexical selection (B-LEX-STRONG, frozen)
#   + structural frame-completeness abstention clauses C1/C3/C4/C5/C6 (frozen)
#   + C7-CREATE-OBLIQUE (zero tunable parameters). Analysis functions byte-identical to the
#   audited EXP-GRAPH-38446557638 runner lineage; constants re-frozen below; pre-declared
#   sensitivity additions only (reincluded sets, XSURF rescoring, reincluded fork,
#   reproduction tripwires, fork_of/arm_gate helpers). NO clause-refit path exists.
# Arm B-OOS = B-RETRIEVAL-OOS : stdlib TF-IDF nearest-class-centroid retrieval with
#   IDF+centroids fit on pooled calibration FIT-TRAIN, gate (tau,mu) selected on
#   disjoint pooled FIT-SELECT under hard mu>0, applied frozen to screened AND reincluded tests.
#   Resubstitution (train==select), mu==0 gates, and any screened-or-reincluded TEST-row use
#   in fit/select are FORBIDDEN and force BLOCKED/measurement-invalid (never silent reuse).
# Stdlib only. Usage: python runner_tframe_sensitivity.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, os, re, random, sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38530149021"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
G1G2SRC = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
G3SRC = ROOT / "research/experiments" / "EXP-GRAPH-38291080992"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

SEED = 38530149021 % (2 ** 32)
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
SEL_TARGET = 0.80
TOK_BAND = 0.60
TRI_BAND = 0.75
N_TRAIN_FROZEN = 102
N_SELECT_APP_FROZEN = 34
N_SELECT_OOS_FROZEN = 60

# XSURF derangement: axis -> foreign lexicon key (resolved in build_axes). No self-match.
# G1-PRIMARY and G1-ALTLEX share identical texts, hence the same foreign lexicon.
XSURF = {"AXIS-G3-NEW": "LEXICON-G1", "AXIS-G2-RETEST": "LEXICON-G3",
         "AXIS-G1-PRIMARY": "LEXICON-G2-HELDOUT", "AXIS-G1-ALTLEX": "LEXICON-G2-HELDOUT"}

DET = {"a", "an", "the", "this", "that", "these", "those", "one", "two", "my", "your", "his", "her",
       "its", "our", "their", "each", "every", "any", "some", "all", "no", "another", "other"}
REF = {"id", "identifier", "identified", "number", "numbered", "named", "called", "titled", "referred",
       "labelled", "labeled", "code", "badge"}
QUANT = {"all", "every", "each", "any", "some", "several", "many", "both", "whole", "entire",
         "multiple", "batch", "bulk"}
POLITE = {"please", "kindly", "can", "could", "would", "will", "i", "want", "need", "help", "lets", "let"}
SOURCE = {"from", "into", "onto"}
OBLIQUE = {"to", "on", "onto", "into", "in", "at", "from", "by", "upon", "toward", "towards", "with"}
REL = {"whose", "which", "who", "that", "where", "matching", "containing"}
SUBORD = {"to", "that", "which", "who", "so", "then"}
PREP = {"of", "with", "by", "using", "for", "about", "from", "in", "to", "on", "at", "into", "onto",
        "under", "over", "across", "via", "through", "as", "per", "within", "without", "against",
        "between", "among", "upon", "toward", "towards", "near", "around", "behind", "before",
        "after", "during", "inside", "outside"}


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def self_sha() -> str:
    try:
        return sha_file(Path(__file__))
    except Exception:
        return "UNKNOWN"


def extract_block(text: str, name: str) -> str:
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise SystemExit(f"missing block {name}")
    return m.group(1)


def jlines(block: str):
    return [json.loads(l) for l in block.splitlines() if l.strip()]


def tokens(s: str):
    return re.findall(r"[a-z]+", s.lower())


def _spans(t, phrase, plural=False):
    pt = phrase.split(); L = len(pt); res = []
    for i in range(len(t) - L + 1):
        ok = True
        for k, p in enumerate(pt):
            x = t[i + k]
            if x == p:
                continue
            if plural and (x == p + "s" or x + "s" == p):
                continue
            ok = False; break
        if ok:
            res.append((i, i + L, L))
    return res


def jaccard(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0


def trigrams(s):
    x = " " + " ".join(tokens(s)) + " "
    return {x[i:i + 3] for i in range(len(x) - 2)}


def comp(text: str, lex: dict):
    """Shared deterministic selector (B-LEX-STRONG): longest key-set + homograph guard. FROZEN."""
    t = tokens(text)
    fam_first = {p.split()[0] for ph in lex["family_nouns"].values() for p in ph}
    fsp = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(t, p, plural=True)]
    osp = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(t, p)
           if not (t[s] in fam_first and s > 0 and t[s - 1] in DET)]
    fmax = max([L for _, _, _, L in fsp], default=0); omax = max([L for _, _, _, L in osp], default=0)
    fkm = {f for f, _, _, L in fsp if L == fmax}; okm = {o for o, _, _, L in osp if L == omax}
    fst = "NONE" if not fsp else ("UNIQUE" if len(fkm) == 1 else "TIE")
    ost = "NONE" if not osp else ("UNIQUE" if len(okm) == 1 else "TIE")
    fam = list(fkm)[0] if fst == "UNIQUE" else None
    op = list(okm)[0] if ost == "UNIQUE" else None
    r1 = None
    if fam:
        s0 = min(s for f, s, _, _ in fsp if f == fam); e0 = max(e for f, _, e, _ in fsp if f == fam)
        rem = t[:s0] + t[e0:]
        ors = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(rem, p)
               if not (rem[s] in fam_first and s > 0 and rem[s - 1] in DET)]
        om = max([L for _, _, _, L in ors], default=0); okm2 = {o for o, _, _, L in ors if L == om}
        if len(okm2) == 1:
            r1 = (fam, list(okm2)[0])
    r2 = None
    if op:
        s0 = min(s for o, s, _, _ in osp if o == op); e0 = max(e for o, _, e, _ in osp if o == op)
        rem = t[:s0] + t[e0:]
        frs = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(rem, p, plural=True)]
        fm = max([L for _, _, _, L in frs], default=0); fkm2 = {f for f, _, _, L in frs if L == fm}
        if len(fkm2) == 1:
            r2 = (list(fkm2)[0], op)
    res = (r1 if r1 == r2 else None) if (r1 and r2) else (r1 or r2)
    hasref = any(w in REF for w in t)
    return dict(t=t, fsp=fsp, osp=osp, hasref=hasref,
                mech=None if res is None else f"mech_{res[0]}_{res[1].lower()}",
                fam=None if res is None else res[0], op=None if res is None else res[1],
                famNONE=int(fst == "NONE"), famTIE=int(fst == "TIE"),
                opNONE=int(ost == "NONE"), opTIE=int(ost == "TIE"),
                noslot=1 if (res is not None and res[1] in ("READ", "UPDATE", "DELETE") and not hasref) else 0,
                quant=1 if any(w in QUANT for w in t) else 0)


def frame(r: dict):
    """Frozen structural frame-completeness clauses (FROZEN, fires => ABSTAIN)."""
    t = r["t"]; cl = {}
    h = 0
    while h < len(t) and t[h] in POLITE:
        h += 1
    head = t[h] if h < len(t) else None
    fire = False
    if r["op"]:
        spans = [(s, e) for o, s, e, L in r["osp"] if o == r["op"]]
        if spans:
            osx = min(s for s, _ in spans)
            if head is not None and head != t[osx] and any(i < osx and t[i] in SUBORD for i in range(len(t))):
                fire = True
    cl["C1-SUBOP"] = fire
    cl["C3-NO-REFERENCE"] = bool(r["op"] in ("READ", "UPDATE", "DELETE") and not r["hasref"])
    cl["C4-COMPLEMENT"] = False
    cl["C6-SOURCE"] = False
    if r["fam"]:
        spans = [(s, e) for f, s, e, L in r["fsp"] if f == r["fam"]]
        if spans:
            after = t[max(e for _, e in spans):]
            idx = 0
            while idx < len(after) and after[idx] in DET:
                idx += 1
            if idx < len(after) and after[idx] not in PREP and after[idx] not in REF and after[idx] not in REL:
                cl["C4-COMPLEMENT"] = True
            if r["op"] == "CREATE" and any(w in SOURCE for w in after):
                cl["C6-SOURCE"] = True
    cl["C5-SET-QUANT"] = any(w in QUANT for w in t)
    return cl


def clause_c7(r: dict) -> bool:
    """C7-CREATE-OBLIQUE. Zero tunable parameters. FROZEN (identical to parent)."""
    if r["op"] != "CREATE":
        return False
    t = r["t"]
    if any(w in SOURCE for w in t):
        return True
    osp = [(s, e) for o, s, e, L in r["osp"] if o == "CREATE"]
    if not osp:
        return False
    osx = min(e for _, e in osp)
    fs = [s for f, s, e, L in r["fsp"] if f == r["fam"] and s >= osx] if r["fam"] else []
    if fs and any(t[i] in OBLIQUE for i in range(osx, min(fs))):
        return True
    return False


def analyze(text: str, lex: dict):
    r = comp(text, lex)
    cl = frame(r)
    cl["C7-CREATE-OBLIQUE"] = clause_c7(r)
    r["clauses"] = cl
    r["S"] = r["famNONE"] + r["opNONE"] + r["opTIE"] + r["noslot"] + r["quant"]
    return r


def is_executed(r: dict, mode: str) -> bool:
    if mode == "gatefree":
        return r["mech"] is not None
    if mode == "incumbent":
        return r["mech"] is not None and r["S"] <= 0
    if mode == "tframe_frozen":
        return r["mech"] is not None and not any(v for k, v in r["clauses"].items() if k != "C7-CREATE-OBLIQUE")
    return r["mech"] is not None and not any(r["clauses"].values())


def target_of(goal):
    return f"mech_{goal['family']}_{goal['op'].lower()}"


def build_axis(app, oos, lex, splitmod, prior_texts):
    rows = []
    for i, g in enumerate(app):
        rows.append(dict(gid=f"app_{i+1:03d}", text=g["text"], app=1, target=target_of(g), split=(i % splitmod) in (1, 3, 5)))
    for i, g in enumerate(oos):
        rows.append(dict(gid=f"oos_{i+1:03d}", text=g["text"], app=0, target=None, split=(i % splitmod) in (1, 3, 5)))
    flagged = []
    for r in rows:
        r.update(analyze(r["text"], lex))
        if max(jaccard(tokens(r["text"]), tokens(p)) for p in prior_texts) >= TOK_BAND or \
           max(jaccard(trigrams(r["text"]), trigrams(p)) for p in prior_texts) >= TRI_BAND:
            flagged.append(r["gid"])
    flaggedset = set(flagged)
    bound = [r for r in rows if r["gid"] not in flaggedset]
    flagged_test = [r for r in rows if r["gid"] in flaggedset and r["split"]]
    return bound, flagged, flagged_test


def metrics(rows, mode):
    ex = [r for r in rows if is_executed(r, mode)]
    exo = sum(1 for r in ex if not r["app"]); exa = sum(1 for r in ex if r["app"])
    co = sum(1 for r in rows if not r["app"]); ca = sum(1 for r in rows if r["app"])
    abR = [r for r in rows if r["mech"] is not None and not is_executed(r, mode)]
    abRo = sum(1 for r in abR if not r["app"])
    ab_all = [r for r in rows if not is_executed(r, mode)]
    sel = sum(1 for r in ex if r["app"] and r["mech"] == r["target"])
    return dict(coverage=exa / ca if ca else None, pooled_false_accept=exo / co if co else None,
                unknown_precision_exclusive=abRo / len(abR) if abR else None,
                unknown_precision_inclusive=(sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None,
                unknown_precision=abRo / len(abR) if abR else None,
                executed=len(ex), executed_oos=exo, executed_app=exa, abstained_resolved=len(abR),
                selective_acc=sel / exa if exa else None,
                unresolved_applicable=sum(1 for r in rows if r["app"] and r["mech"] is None))


def gate_met(m):
    return bool(m["pooled_false_accept"] is not None and m["pooled_false_accept"] <= FA_TARGET
                and m["coverage"] is not None and m["coverage"] >= COV_TARGET
                and m["unknown_precision_exclusive"] is not None and m["unknown_precision_exclusive"] >= PREC_TARGET)


def arm_gate(g):
    """Gate check for retrieval test_gate entries (screened or reincluded)."""
    return bool(g is not None
                and g["pooled_false_accept"] is not None and g["pooled_false_accept"] <= FA_TARGET
                and g["coverage"] is not None and g["coverage"] >= COV_TARGET
                and g["unknown_precision_exclusive"] is not None and g["unknown_precision_exclusive"] >= PREC_TARGET)


def fork_of(g3_gate, armb_g3_met, feasible):
    if not feasible:
        return "RETRIEVAL_INFEASIBLE_OOS"
    if armb_g3_met and not g3_gate:
        return "RETRIEVAL_DOMINATES_G3"
    if g3_gate and not armb_g3_met:
        return "TFRAME_DOMINATES_G3"
    if g3_gate and armb_g3_met:
        return "BOTH_PASS_G3"
    return "NEITHER_PASSES_G3"


def abstain_all_metrics(rows):
    """NC-ABSTAIN-ALL, EXECUTED (no placeholders): abstain on everything resolved."""
    res = [r for r in rows if r["mech"] is not None]
    abRo = sum(1 for r in res if not r["app"])
    ab_all = list(rows)
    return dict(coverage=0.0, pooled_false_accept=None,
                unknown_precision_exclusive=abRo / len(res) if res else None,
                unknown_precision_inclusive=(sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None,
                unknown_precision=abRo / len(res) if res else None,
                executed=0, executed_oos=0, executed_app=0, abstained_resolved=len(res),
                selective_acc=None,
                unresolved_applicable=sum(1 for r in rows if r["app"] and r["mech"] is None))


# ---------------- Arm B-OOS : honest pooled retrieval (non-resubstitution, mu>0) ----------------
def _feats(text):
    t = tokens(text)
    bg = [t[i] + "_" + t[i + 1] for i in range(len(t) - 1)]
    return t + bg


def _vec(fs, idf):
    v = {}
    for f in fs:
        v[f] = v.get(f, 0.0) + 1.0
    for f in list(v):
        v[f] = (1.0 + math.log(v[f])) * idf.get(f, 0.0)
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {f: x / n for f, x in v.items()}


def _cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(f, 0.0) for f, x in a.items())


def build_fit_pool(axes):
    """Pool calibration rows across G1-PRIMARY/G2-RETEST/G3-NEW (one G1 axis only:
    ALTLEX shares G1 texts and would duplicate them). Deterministic global order."""
    pool_app, pool_oos = [], []
    for nm in ("AXIS-G1-PRIMARY", "AXIS-G2-RETEST", "AXIS-G3-NEW"):
        for r in axes[nm]["cal"]:
            (pool_app if r["app"] else pool_oos).append((nm, r))
    train, sel_app = [], []
    for i, item in enumerate(pool_app):
        (sel_app if (i % 4 == 3) else train).append(item)
    return train, sel_app, pool_oos


def text_sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def arm_b_oos(train, sel_app, sel_oos, tests, tests_reincl):
    """IDF+centroids on TRAIN app rows; gate (tau,mu>0) on SELECT; frozen apply to
    screened tests AND reincluded tests. Returns (result_dict, construction_flags).
    Any forbidden fallback -> feasible False with reason; caller maps persistent
    infeasibility to RETRIEVAL_INFEASIBLE_OOS on both forks."""
    fit = [r for _, r in train]
    N = len(fit)
    df = {}
    docs = []
    for r in fit:
        fs = _feats(r["text"])
        docs.append((r["target"], fs))
        for f in set(fs):
            df[f] = df.get(f, 0) + 1
    idf = {f: math.log((1 + N) / (1 + d)) + 1.0 for f, d in df.items()}
    cent = {}
    for cls, fs in docs:
        v = _vec(fs, idf)
        c = cent.setdefault(cls, {})
        for f, x in v.items():
            c[f] = c.get(f, 0.0) + x
    cent = {cls: {f: x / (math.sqrt(sum(y * y for y in v.values())) or 1.0) for f, x in v.items()} for cls, v in cent.items()}

    def score(rows):
        out = []
        for r in rows:
            v = _vec(_feats(r["text"]), idf)
            sims = sorted(((_cos(v, c), cls) for cls, c in cent.items()), reverse=True)
            top = sims[0][0] if sims else 0.0
            margin = (sims[0][0] - sims[1][0]) if len(sims) > 1 else 1.0
            out.append((r, sims[0][1] if sims else None, top, margin))
        return out

    def gate_metrics(scored, tau, mu):
        ex = [(r, cls) for r, cls, s, m in scored if s >= tau and m >= mu]
        ab = [(r, cls, s, m) for r, cls, s, m in scored if not (s >= tau and m >= mu)]
        exo = sum(1 for r, c in ex if not r["app"]); exa = sum(1 for r, c in ex if r["app"])
        co = sum(1 for r in scored if not r[0]["app"]); ca = sum(1 for r in scored if r[0]["app"])
        abRo = sum(1 for r, c, s, m in ab if not r["app"])
        sel = sum(1 for r, c in ex if r["app"] and c == r["target"])
        up = abRo / len(ab) if ab else None
        return dict(coverage=exa / ca if ca else 0.0, pooled_false_accept=exo / co if co else None,
                    unknown_precision_exclusive=up, unknown_precision_inclusive=up, unknown_precision=up,
                    selective_acc=sel / exa if exa else None,
                    executed=len(ex), executed_app=exa, executed_oos=exo, abstained=len(ab))

    sel_rows = [r for _, r in sel_app] + [r for _, r in sel_oos]
    sel_scored = score(sel_rows)
    taus = sorted({round(s, 4) for _, _, s, _ in sel_scored})
    mus = sorted({round(m, 4) for _, _, _, m in sel_scored if round(m, 4) > 0.0})
    if not mus:
        empty = {a: None for a in tests}
        return dict(feasible=False, reason="no-positive-margin-candidate-on-SELECT",
                    tau=None, mu=None, select_gate=None, n_fit_train=N,
                    n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                    classes=sorted(cent.keys()), test_gate=empty, test_gate_reincl=dict(empty)), True
    best = None
    for tau in taus:
        for mu in mus:
            gm = gate_metrics(sel_scored, tau, mu)
            feasible = (gm["pooled_false_accept"] is not None and gm["pooled_false_accept"] <= FA_TARGET
                        and gm["coverage"] >= COV_TARGET
                        and gm["unknown_precision_exclusive"] is not None and gm["unknown_precision_exclusive"] >= PREC_TARGET)
            key = (1 if feasible else 0, gm["coverage"] if gm["coverage"] else 0.0)
            if best is None or key > best[0]:
                best = (key, (tau, mu), gm)
    tau, mu = best[1]
    select_gate = best[2]
    fit_feasible = bool(best[0][0])
    out_tests = {}
    for a, trows in tests.items():
        out_tests[a] = gate_metrics(score(trows), tau, mu) if fit_feasible else None
    out_reincl = {}
    for a, trows in tests_reincl.items():
        out_reincl[a] = gate_metrics(score(trows), tau, mu) if fit_feasible else None
    return dict(feasible=fit_feasible, reason=None if fit_feasible else "no-feasible-mu-positive-gate-on-SELECT",
                tau=tau, mu=mu, select_gate=select_gate, n_fit_train=N,
                n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                classes=sorted(cent.keys()), test_gate=out_tests, test_gate_reincl=out_reincl), True


def shuffled_selection(rows, mode, seed):
    rng = random.Random(seed)
    ex = [r for r in rows if is_executed(r, mode) and r["app"]]
    if not ex:
        return None
    targets = [r["target"] for r in ex]
    rng.shuffle(targets)
    return sum(1 for r, t in zip(ex, targets) if r["mech"] == t) / len(ex)


def random_role_selection(rows, mode, seed):
    rng = random.Random(seed)
    mechs = sorted({r["target"] for r in rows if r["app"]})
    ex = [r for r in rows if is_executed(r, mode) and r["app"]]
    if not ex or not mechs:
        return None
    return sum(1 for r in ex if r["mech"] == rng.choice(mechs)) / len(ex)


def matched_random_gate(rows, mode, seed):
    rng = random.Random(seed)
    ab_n = sum(1 for r in rows if not is_executed(r, mode))
    idx = list(range(len(rows))); rng.shuffle(idx)
    ab = set(idx[:ab_n])
    ex = [r for i, r in enumerate(rows) if i not in ab]
    co = [r for r in rows if not r["app"]]
    abr = [r for i, r in enumerate(rows) if i in ab]
    return dict(pooled_false_accept=(sum(1 for r in ex if not r["app"]) / len(co)) if co else None,
                unknown_precision=(sum(1 for r in abr if not r["app"]) / len(abr)) if abr else None,
                matched_abstention_count=ab_n)


def load_banks():
    g3_text = (G3SRC / "prereg.md").read_text(encoding="utf-8")
    g3_app = jlines(extract_block(g3_text, "GOAL-BANK-G3"))
    g3_oos = jlines(extract_block(g3_text, "OOS-BANK-G3"))
    lex_g3 = json.loads(extract_block(g3_text, "LEXICON-G3"))
    g1g2_text = (G1G2SRC / "prereg.md").read_text(encoding="utf-8")
    g1_app = jlines(extract_block(g1g2_text, "GOAL-BANK-G1"))
    g1_oos = jlines(extract_block(g1g2_text, "OOS-BANK-G1"))
    lex_g1 = json.loads(extract_block(g1g2_text, "LEXICON-G1"))
    lex_alt = json.loads(extract_block(g1g2_text, "LEXICON-G1-ALT"))
    g2_app = jlines(extract_block(g1g2_text, "GOAL-BANK-G2"))
    g2_oos = jlines(extract_block(g1g2_text, "OOS-BANK-G2"))
    lex_ho = json.loads(extract_block(g1g2_text, "LEXICON-G2-HELDOUT"))
    grand = (GRANDPARENT / "prereg.md").read_text(encoding="utf-8")
    prior_parent = json.loads(extract_block(grand, "PRIOR-PARENT-BANK-TEXTS"))
    sys.path.insert(0, str(ROOT / "research/harness"))
    from goal_generator import INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES
    gg_only = list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs] + \
        list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES)
    prior_full = gg_only + list(prior_parent)
    priors_g3 = gg_only + list(prior_parent) + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos] + \
        [g["text"] for g in g2_app] + [g["text"] for g in g2_oos]
    priors_g2 = gg_only + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos]
    return dict(g3_app=g3_app, g3_oos=g3_oos, lex_g3=lex_g3, g1_app=g1_app, g1_oos=g1_oos,
                lex_g1=lex_g1, lex_alt=lex_alt, g2_app=g2_app, g2_oos=g2_oos, lex_ho=lex_ho,
                prior_full=prior_full, priors_g3=priors_g3, priors_g2=priors_g2)


def build_axes(banks):
    axes = {}
    spec = {
        "AXIS-G3-NEW": (banks["g3_app"], banks["g3_oos"], banks["lex_g3"], 4, banks["priors_g3"]),
        "AXIS-G2-RETEST": (banks["g2_app"], banks["g2_oos"], banks["lex_ho"], 4, banks["priors_g2"]),
        "AXIS-G1-PRIMARY": (banks["g1_app"], banks["g1_oos"], banks["lex_g1"], 6, banks["prior_full"]),
        "AXIS-G1-ALTLEX": (banks["g1_app"], banks["g1_oos"], banks["lex_alt"], 6, banks["prior_full"]),
    }
    xlex = {"AXIS-G3-NEW": banks["lex_g1"], "AXIS-G2-RETEST": banks["lex_g3"],
            "AXIS-G1-PRIMARY": banks["lex_ho"], "AXIS-G1-ALTLEX": banks["lex_ho"]}
    assert set(xlex) == set(spec) and all(xlex[a] is not spec[a][2] for a in spec), "XSURF derangement broken"
    xdiv = []
    for nm, (app, oos, lex, sm, priors) in spec.items():
        bound, flagged, flagged_test = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        xbound, xflagged, xflagged_test = build_axis(app, oos, xlex[nm], sm, priors)
        if set(xflagged) != set(flagged):
            xdiv.append(nm)
        xcal = [r for r in xbound if not r["split"]]; xtest = [r for r in xbound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, flagged_test=flagged_test, cal=cal, test=test,
                        test_reincl=test + flagged_test,
                        xbound=xbound, xflagged=xflagged, xflagged_test=xflagged_test, xcal=xcal, xtest=xtest,
                        xtest_reincl=xtest + xflagged_test,
                        cal_metrics={m: metrics(cal, m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")},
                        xcal_metrics={m: metrics(xcal, m) for m in ("tframeplus", "gatefree")})
    return axes, xdiv


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    banks = load_banks()
    axes, xdiv = build_axes(banks)
    train, sel_app, sel_oos = build_fit_pool(axes)
    train_shas = {text_sha(r["text"]) for _, r in train}
    sel_shas = {text_sha(r["text"]) for _, r in sel_app} | {text_sha(r["text"]) for _, r in sel_oos}
    test_shas = {text_sha(r["text"]) for a, v in axes.items() for r in v["test"] + v["flagged_test"]}
    construction_ok = (len(train) == N_TRAIN_FROZEN and len(sel_app) == N_SELECT_APP_FROZEN
                       and len(sel_oos) == N_SELECT_OOS_FROZEN
                       and not (train_shas & sel_shas) and not ((train_shas | sel_shas) & test_shas))
    construction = dict(n_fit_train=len(train), n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                        train_select_disjoint=not (train_shas & sel_shas),
                        fit_test_disjoint=not ((train_shas | sel_shas) & test_shas),
                        bars_met=construction_ok,
                        train_gids=[f"{a}:{r['gid']}" for a, r in train],
                        select_gids=[f"{a}:{r['gid']}" for a, r in sel_app] + [f"{a}:{r['gid']}" for a, r in sel_oos])

    if args.mechanics_only:
        fit_res, _ = arm_b_oos(train, sel_app, sel_oos, {}, {})
        out = dict(status="DESIGN-MECHANICS-ONLY", experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
                   axes={k: dict(bound=len(v["bound"]), flagged=v["flagged"],
                                 flagged_test_gids=[r["gid"] for r in v["flagged_test"]],
                                 xflagged_test_gids=[r["gid"] for r in v["xflagged_test"]],
                                 cal_n=[sum(1 for r in v["cal"] if r["app"]), sum(1 for r in v["cal"] if not r["app"])],
                                 cal_metrics=v["cal_metrics"],
                                 xcal_metrics=v["xcal_metrics"],
                                 cal_feasible_tframeplus=gate_met(v["cal_metrics"]["tframeplus"])) for k, v in axes.items()},
                   c7_firing={k: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                      oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                              for k, v in axes.items()},
                   fit_pool=construction,
                   xdiv=xdiv,
                   g2_reincl_identical=(len(axes["AXIS-G2-RETEST"]["flagged_test"]) == 0),
                   retrieval_select=dict(feasible=fit_res["feasible"], reason=fit_res["reason"],
                                         tau=fit_res["tau"], mu=fit_res["mu"],
                                         mu_active=bool(fit_res["mu"] is not None and fit_res["mu"] > 0),
                                         select_gate=fit_res["select_gate"]),
                   liveness=dict(g3_cal_executed=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["executed"],
                                 g3_cal_unresolved=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["unresolved_applicable"]),
                   test_not_scored=True)
        print(json.dumps(out, indent=2))
        return

    for a, v in axes.items():
        v["test_metrics"] = {m: metrics(v["test"], m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
        v["reincl_metrics"] = {m: metrics(v["test_reincl"], m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
        v["xtest_metrics"] = {m: metrics(v["xtest"], m) for m in ("tframeplus", "gatefree")}
        v["xtest_reincl_metrics"] = {"tframeplus": metrics(v["xtest_reincl"], "tframeplus")}
        v["abstain_all"] = abstain_all_metrics(v["test"])
        v["abstain_all_reincl"] = abstain_all_metrics(v["test_reincl"])
        v["shuffled_selection"] = shuffled_selection(v["test"], "tframeplus", SEED)
        v["random_role_selection"] = random_role_selection(v["test"], "tframeplus", SEED)
        v["ctrl_random_gate"] = matched_random_gate(v["test"], "tframeplus", SEED)
        v["shuffled_selection_reincl"] = shuffled_selection(v["test_reincl"], "tframeplus", SEED)
        v["random_role_selection_reincl"] = random_role_selection(v["test_reincl"], "tframeplus", SEED)
        v["ctrl_random_gate_reincl"] = matched_random_gate(v["test_reincl"], "tframeplus", SEED)
    tests = {a: v["test"] for a, v in axes.items()}
    tests_reincl = {a: v["test_reincl"] for a, v in axes.items()}
    fit_res, _ = arm_b_oos(train, sel_app, sel_oos, tests, tests_reincl)

    prim = axes["AXIS-G3-NEW"]["test_metrics"]["tframeplus"]
    gates = {a: gate_met(v["test_metrics"]["tframeplus"]) for a, v in axes.items()}
    gates_reincl = {a: gate_met(v["reincl_metrics"]["tframeplus"]) for a, v in axes.items()}
    xgates = {a: gate_met(v["xtest_metrics"]["tframeplus"]) for a, v in axes.items()}
    xgates_reincl = {a: gate_met(v["xtest_reincl_metrics"]["tframeplus"]) for a, v in axes.items()}
    sels = {a: v["test_metrics"]["tframeplus"]["selective_acc"] for a, v in axes.items()}
    sels_reincl = {a: v["reincl_metrics"]["tframeplus"]["selective_acc"] for a, v in axes.items()}
    selection_preserved = all(s is not None and s >= SEL_TARGET for s in sels.values())
    selection_reincl = all(s is not None and s >= SEL_TARGET for s in sels_reincl.values())
    g3t = axes["AXIS-G3-NEW"]["test"]
    g3t_total = len(g3t)
    g3t_abstained_resolved = sum(1 for r in g3t if r["mech"] is not None and not is_executed(r, "tframeplus"))
    live = ((0 < prim["executed"] < g3t_total)
            and (prim["executed_app"] >= 1)
            and (g3t_abstained_resolved >= 1))
    arm_g3 = (fit_res["test_gate"] or {}).get("AXIS-G3-NEW")
    arm_g2 = (fit_res["test_gate"] or {}).get("AXIS-G2-RETEST")
    armb_g3_met = arm_gate(arm_g3)
    armb_g2_met = arm_gate(arm_g2)
    armr_g3 = (fit_res["test_gate_reincl"] or {}).get("AXIS-G3-NEW")
    armr_g2 = (fit_res["test_gate_reincl"] or {}).get("AXIS-G2-RETEST")
    armr_g3_met = arm_gate(armr_g3)
    armr_g2_met = arm_gate(armr_g2)
    retrieval_fork = fork_of(gates.get("AXIS-G3-NEW"), armb_g3_met, fit_res["feasible"])
    retrieval_fork_reincl = fork_of(gates_reincl.get("AXIS-G3-NEW"), armr_g3_met, fit_res["feasible"])
    invalid_reasons = []
    if not construction_ok:
        invalid_reasons.append("fit-pool-construction-failed: N_TRAIN==102 AND SELECT_APP==34 AND SELECT_OOS==60 AND train/select/test-union disjointness required; resubstitution fallback forbidden")
    if not live:
        invalid_reasons.append("treatment-not-live: AXIS-G3-NEW gold-screened test non-degenerate execution failed (need 0 < executed_total < n_total_test AND executed_app >= 1 AND abstained_resolved >= 1)")
    for a, v in axes.items():
        if v["test_metrics"]["tframeplus"]["unknown_precision_exclusive"] is None:
            invalid_reasons.append(f"{a}: unknown_precision_exclusive undefined on gold-screened test (no resolved abstention)")
    if not gates.get("AXIS-G1-ALTLEX"):
        invalid_reasons.append("positive-control-failed: PC-AXIS-G1-ALTLEX gold-screened gate-met false (runner-enforced invalidity)")
    if xdiv:
        invalid_reasons.append(f"screen-lexicon-divergence: cross flagged-gid sets differ from gold on {sorted(xdiv)} (runner bug guard; screen must be lexicon-independent)")
    g2m = axes["AXIS-G2-RETEST"]["test_metrics"]["tframeplus"]
    expected_vector = {"AXIS-G3-NEW": True, "AXIS-G2-RETEST": False, "AXIS-G1-PRIMARY": True, "AXIS-G1-ALTLEX": True}
    if gates != expected_vector or not (g2m["pooled_false_accept"] is not None and g2m["pooled_false_accept"] <= FA_TARGET
                                        and g2m["coverage"] is not None and g2m["coverage"] >= COV_TARGET):
        invalid_reasons.append("screened-reproduction-failed: gold-screened gate vector != parent {G3 met, G1 met, ALTLEX met, G2 false-solely-on-UP with FA<=0.10 and coverage>=0.50}")
    if retrieval_fork != "TFRAME_DOMINATES_G3":
        invalid_reasons.append("screened-fork-reproduction-failed: screened fork != TFRAME_DOMINATES_G3")
    if any(arm_gate((fit_res["test_gate"] or {}).get(a)) for a in axes):
        invalid_reasons.append("screened-retrieval-reproduction-failed: screened retrieval meets a TEST gate (parent: all four fail)")
    screen_stable = all(gates_reincl[a] == gates[a] for a in gates) and (selection_reincl == selection_preserved)
    fork_stable = (retrieval_fork_reincl == retrieval_fork)
    gold_dependent = all(not xgates[a] for a in gates if gates[a])
    g2_reincl_identical = (len(axes["AXIS-G2-RETEST"]["flagged_test"]) == 0
                           and len(axes["AXIS-G2-RETEST"]["xflagged_test"]) == 0)
    status = "MEASUREMENT_INVALID" if invalid_reasons else "COMPLETE"
    if invalid_reasons:
        decision = None
    elif screen_stable and fork_stable:
        decision = "BOUND_ROBUST"
    else:
        decision = "BOUND_ARTIFACT"
    artifact_subtype = dict(screen_artifact=bool(not screen_stable), fork_artifact=bool(not fork_stable))
    out = dict(status=status, experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
               invalid_reasons=invalid_reasons, decision=decision, artifact_subtype=artifact_subtype,
               screen_stable=screen_stable, fork_stable=fork_stable, gold_dependent=gold_dependent,
               g2_reincl_identical=g2_reincl_identical,
               gates=gates, gates_reincl=gates_reincl, xgates=xgates, xgates_reincl=xgates_reincl,
               selection={a: sels[a] for a in sels}, selection_preserved=selection_preserved,
               selection_reincl={a: sels_reincl[a] for a in sels_reincl}, selection_reincl_preserved=selection_reincl,
               selection_rule="B-LEX-STRONG + C7-CREATE-OBLIQUE",
               retrieval_fork=retrieval_fork, retrieval_fork_reincl=retrieval_fork_reincl,
               retrieval_oos_feasible=fit_res["feasible"], retrieval_oos_reason=fit_res["reason"],
               arm_b_oos_gate_met={"g3": armb_g3_met, "g2": armb_g2_met,
                                   "g3_reincl": armr_g3_met, "g2_reincl": armr_g2_met},
               arm_b_oos=dict(tau=fit_res["tau"], mu=fit_res["mu"],
                              mu_active=bool(fit_res["mu"] is not None and fit_res["mu"] > 0),
                              n_fit_train=fit_res["n_fit_train"], n_select_app=fit_res["n_select_app"],
                              n_select_oos=fit_res["n_select_oos"], classes=fit_res["classes"],
                              select_gate=fit_res["select_gate"], test_gate=fit_res["test_gate"],
                              test_gate_reincl=fit_res["test_gate_reincl"]),
               fit_pool=construction,
               test_metrics={a: v["test_metrics"] for a, v in axes.items()},
               test_reincl_metrics={a: v["reincl_metrics"] for a, v in axes.items()},
               xtest_metrics={a: v["xtest_metrics"] for a, v in axes.items()},
               xtest_reincl_metrics={a: v["xtest_reincl_metrics"] for a, v in axes.items()},
               test_n={a: [sum(1 for r in v["test"] if r["app"]), sum(1 for r in v["test"] if not r["app"])] for a, v in axes.items()},
               test_n_reincl={a: [sum(1 for r in v["test_reincl"] if r["app"]), sum(1 for r in v["test_reincl"] if not r["app"])] for a, v in axes.items()},
               reincluded_gids={a: [r["gid"] for r in v["flagged_test"]] for a, v in axes.items()},
               cal_metrics={a: v["cal_metrics"] for a, v in axes.items()},
               c7_firing={a: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                  oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                          for a, v in axes.items()},
               execution_vectors={a: {r["gid"]: {"split": "test" if r["split"] else "cal",
                                                 "app": r["app"], "mech": r["mech"], "target": r["target"],
                                                 "text_sha256": hashlib.sha256(r["text"].encode()).hexdigest(),
                                                 "clauses": r["clauses"], "S": r["S"],
                                                 "executed": is_executed(r, "tframeplus")} for r in v["bound"]}
                                 for a, v in axes.items()},
               reincl_vectors={a: {r["gid"]: {"split": "test-reincluded",
                                               "app": r["app"], "mech": r["mech"], "target": r["target"],
                                               "text_sha256": hashlib.sha256(r["text"].encode()).hexdigest(),
                                               "clauses": r["clauses"], "S": r["S"],
                                               "executed": is_executed(r, "tframeplus")} for r in v["flagged_test"]}
                               for a, v in axes.items()},
               xvectors={a: {r["gid"]: {"split": ("xtest-reincluded" if r in v["xflagged_test"] else "xtest"),
                                         "app": r["app"], "mech": r["mech"], "target": r["target"],
                                         "text_sha256": hashlib.sha256(r["text"].encode()).hexdigest(),
                                         "clauses": r["clauses"], "S": r["S"],
                                         "executed": is_executed(r, "tframeplus")}
                                       for r in v["xtest"] + v["xflagged_test"]}
                         for a, v in axes.items()},
               controls={a: dict(shuffled_selection=v["shuffled_selection"], random_role_selection=v["random_role_selection"],
                                 ctrl_random_gate=v["ctrl_random_gate"],
                                 shuffled_selection_reincl=v["shuffled_selection_reincl"],
                                 random_role_selection_reincl=v["random_role_selection_reincl"],
                                 ctrl_random_gate_reincl=v["ctrl_random_gate_reincl"],
                                 b_lex_strong=v["test_metrics"]["tframeplus"]["selective_acc"],
                                 b_lex_strong_reincl=v["reincl_metrics"]["tframeplus"]["selective_acc"],
                                 b_lex_only=v["test_metrics"]["gatefree"]["selective_acc"],
                                 b_lex_only_reincl=v["reincl_metrics"]["gatefree"]["selective_acc"],
                                 b_incumbent_kernel=v["test_metrics"]["incumbent"]["selective_acc"],
                                 b_incumbent_kernel_reincl=v["reincl_metrics"]["incumbent"]["selective_acc"],
                                 incumbent_fa=v["test_metrics"]["incumbent"]["pooled_false_accept"],
                                 incumbent_fa_reincl=v["reincl_metrics"]["incumbent"]["pooled_false_accept"],
                                 ctrl_exec_all_fa=v["test_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_exec_all_fa_reincl=v["reincl_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_exec_all_fa_x=v["xtest_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_abstain_all_cov=v["abstain_all"]["coverage"],
                                 ctrl_abstain_all_up=v["abstain_all"]["unknown_precision_exclusive"],
                                 ctrl_abstain_all_up_inclusive=v["abstain_all"]["unknown_precision_inclusive"],
                                 ctrl_abstain_all_reincl_cov=v["abstain_all_reincl"]["coverage"],
                                 ctrl_abstain_all_reincl_up=v["abstain_all_reincl"]["unknown_precision_exclusive"],
                                 ctrl_abstain_all_reincl_up_inclusive=v["abstain_all_reincl"]["unknown_precision_inclusive"],
                                 xcoverage=v["xtest_metrics"]["tframeplus"]["coverage"],
                                 xresolved_abstentions=v["xtest_metrics"]["tframeplus"]["abstained_resolved"],
                                 xunknown_precision=v["xtest_metrics"]["tframeplus"]["unknown_precision_exclusive"]) for a, v in axes.items()},
               flagged={a: v["flagged"] for a, v in axes.items()})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER -->
