# EXP-GRAPH-38816768796 preregistration — Graph tau-rule-sensitivity packet: pre-registered max-slack feasible-tau vs the ascending-tau tie-break (DESIGN, design_contract_version 2)

## 0. Mandate, inherited state, and legacy position

- Binding direction: `request.json#director_mandate` (cycle `38816465757`, Graph `REOPEN` on `C-SEMANTIC-RESOLVE` with `cognitive_reset=true`, `parent_handoff_disposition=USE`). The Director's strategic question is converted here into the smallest rigorous falsifiable experiment; no drift to a nearby objective.
- Director question (binding): under a pre-registered feasible-tau selection rule that is not lowest-tau-wins (e.g. a held-out selection axis or a feasibility-plus-margin rule fixed before any TEST scoring), does the word-unigram Jaccard 1-NN blind resolver survive the frozen AXIS-G3-NEW reincluded G3 gate, or does BLIND_FAILS persist independent of the ascending-tau tie-break?
- Smallest batch per mandate: one tau-rule-sensitivity packet on the already-constructed frozen banks. No new anchor/surface collection, no clause refit (mandate stop trigger: any refit of the deterministic clause set converts this from a bound test into a new architecture experiment and is out of scope → BLOCKED, never silent redesign). No new surface family. Stop trigger: one packet; stop/pivot if the rule is infeasible or degenerate; then park-or-continue per outcome.
- Baseline per mandate: the frozen deterministic resolver (gold T-FRAME+ = B-LEX-STRONG plus ambiguity gate) plus the honest out-of-sample retrieval fit (B-RETRIEVAL-OOS), exclusive unknown-precision denominator fixed pre-freeze.
- Decision counterfactual (mandate): if blind survives under the pre-registered feasible-tau rule, the TFRAME_DOMINATES_G3 fork reopens; if BLIND_FAILS persists, the blind path is retired and Product keeps the conservative abstention boundary. Strongest baseline is the frozen deterministic B-LEX-STRONG plus ambiguity gate.
- Parent handoff preserved (`research/experiments/EXP-GRAPH-38666634300/handoff.json`, sha `da318f26724e528475d3032a8d59e3686b684dac3756a71841282902dd5c81b2`): `established` (audit-PASS v2 transaction with byte-identical runner re-execution and auditor-owned blind reimplementation, zero mismatch; decided AXIS-G3-NEW REINCLUDED TEST blind failure at frozen tau=0.2727: FA 0.20 (4/20 OOS) with COV 1.0/UP 1.0/selective 0.05, blind_inert=false so false-accept-excess not degeneracy; blind fails all four TEST gates both supersets at that tau, fork GOLD_DOMINATES_BLIND_G3; B-RETRIEVAL-OOS fails every TEST gate with fork TFRAME_DOMINATES_G3; gate apparatus sensitive — gold gate-met on decided rows, PC passes, NC headroom/floor live, nulls at chance; treatment-vs-comparator identifiability with blindness contract), `rejected` (frozen blind procedure + ascending-tau calibration fails G3; no tau passes G1/G2 on either superset and no single tau passes all four axes; degeneracy and gate-insensitivity readings; ancestor arms as non-decision identities), `unknown` (TAU-SELECTION-RULE SENSITIVITY as the highest-priority item — this packet resolves exactly it — plus OOS-denominator margin, other blind mechanism classes, pooled-dilution vs intrinsic weakness, blind-operationalization reading gap, G1 text-identity and G3 zero-slack fragility), and `do_not_assume` (10 guards, incl. no mechanism-class reading of BLIND_FAILS given post hoc tau=0.3333 SELECT-feasible AND G3-gate-met; no powered FA-rate reading of the 2-row margin, P=0.133; no general-retrieval reading of the fork; no unsupervised-resolution reading; no resolution-quality reading, SELECT selective 0.0; no claim elevation, HYPOTHESIS retained; no generalization beyond frozen banks/splits/screen/lexicons; screened/retrieval reproduction as tripwires only; no infrastructure-as-evidence; frozen-procedure-level reading of the falsifier) are carried forward unchanged. This packet directly resolves parent `unknown` item 1 (tau-selection-rule sensitivity) by pre-registered measurement.
- Grandparent context (continuity only): gate-vector packet `EXP-GRAPH-38530149021` (BOUND_ROBUST / DECIDE_REQUIRE_RETRIEVAL_B, gold-lexicon-conditional); mandate parent `EXP-GRAPH-38446557638` (handoff resolved); direct parent `EXP-GRAPH-38385040804` is BLOCKED with metrics={} and is never cited as a measurement source.
- Legacy position (`LEGACY: DISTINCT_EXTENSION`): DESIGN searched `codex/legacy_artifact_index.json` for `tie-break|ascending-tau|lowest-tau|feasible-tau|margin-rule|max-slack|select_feasible`: **0 hits** — no pre-2.0 precedent varies, or even names, the abstention-tau tie-break confound. Searched for `jaccard-1nn|1-nn-jaccard|blind-resolv|lexicon-free`: **0 hits**. Parent's 6 `blind` hits (artifacts 97/98 `reports/graph/cycle2_blind_composition.md`, 115/116 `reports/graph/run2_blind_inheritance.md`, 48, 639) were inspected at the primary source (`.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md`): pre-2.0 `blind` means `blind=True desc_only` fragment queries against stored fragment descriptions with embedding/MMR rankers, i.e. blind-query-against-memory with the keyword/oracle confounds recorded in `P2-BLIND-COMPOSITION` (pre2 product summary artifact 4.697, sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`: 3/3 unseen compositions vs 0/3 weak baselines). No pre-2.0 experiment fixes an abstention-precision denominator, calibrates an abstention gate on a disjoint SELECT split, enforces fit/select/test disjointness with forbidden resubstitution, or pits a lexicon-free resolver against an OOS-fit retrieval comparator on frozen banks — and none tests a word-unigram Jaccard 1-NN fully-blind resolver under a non-lowest-tau-wins feasible-tau rule on the frozen AXIS-G3-NEW banks with the DECIDE_REQUIRE_RETRIEVAL_B bound (mandate comparative_reasoning continuity). Nearest-neighbour `P2-MIND2WEB` (archived Codex §1: 6/176 exact matches, 47/176 retrieval) likewise has no abstention gate. This packet rigorously REPLICATES the parent procedure in every byte except the Director-mandated factor (the tau-selection rule), and materially DIFFERS from every pre-2.0 precedent in denominator, calibration, disjointness, comparator honesty, and the pre-registered margin rule. Independent extension with materially improved validity; not a duplicate. Absence of a matching design in the index is not claimed as proof of absence from the full archive (brief guard).

## 1. Hypotheses (single frozen texts)

- H1 (tie-break-independent blind viability on the frozen banks): `BLIND-JAC-1NN` — word-unigram Jaccard 1-nearest TRAIN exemplar resolution over the pooled FIT-TRAIN pool with a single SELECT-fitted Jaccard threshold `tau*` as its calibrated abstention gate, reading no `LEXICON-*` block at any stage, where `tau*` is selected by the pre-registered NON-LOWEST-TAU-WINS rule (§2) — meets the frozen G3 gate on `AXIS-G3-NEW` reincluded TEST (`pooled_false_accept<=0.10 AND coverage>=0.50 AND unknown_precision_exclusive>=0.85`).
- Continuity legs (tripwires, not hypotheses): gold T-FRAME+ screened vector reproduces the parent `{G3 met, G1 met, ALTLEX met, G2 false-solely-on-UP}`; gold reincluded vector reproduces the audited parent vector (G3 met FA 0.10/cov 1.0/UP 1.0, G2 false solely on UP 0.8333, G1/ALTLEX met); B-RETRIEVAL-OOS re-fits to `(tau=0.4156, mu=0.0005)` with fork `TFRAME_DOMINATES_G3` on both supersets and no TEST gate met. Any drift is bank-drift invalidity, not science.
- Expectation from parent-published evidence and DESIGN proofs (NOT results): the SELECT feasible set under the UNCHANGED predicate holds 9 taus (`0.2727/0.3333/0.375/0.4/0.4286/0.5/0.5556/0.5714/0.6`, auditor post hoc sweep) all at SELECT coverage 1.0; `tau*` is provably not the lowest tau (§2, §8.2); published post hoc shows exactly one feasible tau (`0.3333`: SELECT FA 0.0333/COV 1.0/UP 1.0; G3 reincluded FA 0.10/COV 0.925/UP 0.8571/selective 0.0541) passes the G3 reincluded gate while `0.2727` fails (FA 0.20) and NO tau passes G1/G2 on either superset; blind SELECT `selective_acc=0.0` (pooled-dilution continuity with retrieval). TEST genuinely open: `tau*` depends on the unpublished SELECT FA ordering at the remaining feasible taus.
- Falsifier (frozen): H1 SUPPORTED (`BLIND_SURVIVES`) iff `blind_g3_met` at the frozen `tau*` (blind `AXIS-G3-NEW` reincluded gate-met on the exclusive denominator). H1 retired for this mechanism-plus-calibration class (`BLIND_FAILS`) iff the blind G3 reincluded gate is false at `tau*`, including pre-handled `BLIND_INERT` collapse (zero executes or zero resolved abstentions → UP-null → gate-false via the coverage/None bars, §2). Empty feasible set under the unchanged predicate yields `TAU_RULE_INFEASIBLE` (BLOCKED/NOT_APPLICABLE mandate stop, never `BLIND_FAILS`, §7). Gating any decision on `unknown_precision_inclusive` is pre-declared invalid (parent RQF-02 continuity); inclusive is reported sensitivity-only. Survival is graded by `selective_acc` and `CTRL-BLIND-PERMUTED` in `reason`/product text (no extra label): gate-met with `selective_acc>=0.80` reads as viability signal; gate-met with `selective_acc<0.80` reads as abstention-viable but resolution-deficient (selective_acc must enter the gate before any ship discussion, no ship). Any refit of the deterministic clause set or any new surface family is out of scope per the mandate stop trigger (BLOCKED).

## 2. Treatment: BLIND-JAC-1NN with the pre-registered max-slack rule (frozen)

- Blindness contract (auditable): the blind functions (`_blind_token_set`, `blind_jac_predict`, `blind_gate_metrics`, `arm_blind_oos`) accept ONLY `(text, target)` exemplar pairs from the pooled FIT-TRAIN pool. No `LEXICON-*` object is constructed, read, passed, or in scope on the blind path — fit, select, or test. There is no `lex` parameter anywhere in the blind block. AUDIT verifies by diffing the blind block against this contract (byte-identical to parent apart from the rule lines of §13).
- Operational definition of blind: no surface-form dictionary of any kind (same as parent). Mechanism: resolution = 1-nearest TRAIN exemplar by word-unigram Jaccard (raw token sets, no weighting); predicted class = the nearest exemplar's target; confidence = the max Jaccard score. Deterministic: fixed global TRAIN order (G1,G2,G3 pool order), strict-greater replacement, ties resolve to the earliest TRAIN row. Abstention = single threshold `tau` on the 1-NN score: execute iff `score >= tau`. `tau` candidates = sorted unique `round(score,4)` on FIT-SELECT (unchanged candidate set).
- THE RULE (frozen, the single variable of this packet): among SELECT-feasible taus (gate-met on pooled FIT-SELECT under the UNCHANGED predicate `FA<=0.10 AND COV>=0.50 AND UP_excl>=0.85`), select `tau* = argmax (FA_TARGET − SELECT pooled_false_accept)`; tie-break HIGHER `tau` wins (explicitly not lowest-tau-wins). Implementation: fully-ordered key `(feasible_bit, slack_or_-1.0, tau)` with strict-greater comparison over distinct taus, so the unique maximum is picked regardless of iteration order; `select_slack` recorded for audit. Rationale (principled, not ad-hoc): the most conservative feasible gate — maximal false-accept margin consistent with SELECT feasibility — directly tests whether the parent failure was an artifact of picking the loosest feasible gate. The feasibility predicate is byte-identical to the parent, so feasibility itself is not redefined.
- Non-identity proof (from accepted evidence, no new measurement): published SELECT FA is 0.0833 at `tau=0.2727` and 0.0333 at `tau=0.3333`; argmin-FA therefore cannot be the lowest feasible tau whatever the unpublished values are. `tau* != 0.2727` is proven before freeze; the tie-break confound is genuinely varied.
- Totality: the candidate set is always non-empty (94 SELECT rows); the rule always emits a `tau*` when the feasible set is non-empty. Empty feasible set → `TAU_RULE_INFEASIBLE` stop (§7): a drift guard only, provably non-taken on identical banks (same predicate that yielded 9 feasible taus in the accepted packet).
- Held-out-selection-axis alternative (mandate's other example) declined ON RECORD: it would change the calibration distribution (a second variable: which rows calibrate), while the max-slack rule isolates the tie-break confound exactly on the identical SELECT pool. Held-out selection is reserved if the margin-rule outcome is ambiguous.
- Mechanism distance from B-RETRIEVAL-OOS (identifiability, five points, parent continuity): (1) features unigram-only vs uni+bigram; (2) no IDF/term weighting (raw sets) vs sublinear-tf*IDF; (3) 1-NN exemplar vs per-class L2 centroid; (4) Jaccard vs cosine; (5) single-tau gate vs (tau,mu) margin gate. Shared by design: the SAME pooled rows (mechanism-given-data ablation).

## 3. Comparators: gold T-FRAME+ (frozen strongest baseline) + Arm B-OOS (honest, unchanged)

- Arm A-gold = `B-LEX-STRONG` shared deterministic selector + structural frame-completeness clauses `C1-SUBOP/C3-NO-REFERENCE/C4-COMPLEMENT/C5-SET-QUANT/C6-SOURCE` + `C7-CREATE-OBLIQUE`, all zero tunable parameters. Analysis functions (`comp/frame/clause_c7/is_executed/metrics`) are byte-identical to the audited parent `EXP-GRAPH-38666634300` runner lineage; only EXP_ID/SEED constants and the pre-declared blind-rule lines of §2 differ. AUDIT can diff raw_evidence runners directly.
- Arm B-OOS = byte-identical honest pooled retrieval: word unigram + adjacent-bigram features; IDF from FIT-TRAIN app rows only; per-class L2-normalised centroids; prediction = nearest centroid; confidence = top cosine; margin = top minus second. Gate `(tau,mu)` searched on FIT-SELECT only (lexicographic maximise-feasibility-then-coverage), hard constraint `mu>0` (candidate `round(margin,4)>0` only). Frozen gate applied unchanged to screened tests AND reincluded tests. Expected reproduction (never inherited): `tau=0.4156, mu=0.0005, mu_active=true`, SELECT `coverage 0.9412 FA 0.10 UP 0.9643 selective_acc 0.0`, fork `TFRAME_DOMINATES_G3` both supersets, no TEST gate met. EXECUTE re-fits and re-emits every value.
- Fairness disclosure (pre-registered, for AUDIT): pooled TRAIN contains same-surface classes for every test axis plus cross-domain distractors (~1.7 train rows/class over ~60 classes); dilution biases AGAINST both memory arms symmetrically (parent continuity). Gold arms hold surface lexicons while both memory arms are lexicon-free; the XSURF-measured gold-dependence (`gold_dependent=true`, quoted) quantifies exactly how much of the deterministic performance is lexicon-carried.
- Forbidden fallbacks (violation = BLOCKED or MEASUREMENT_INVALID, never silent reuse): refitting deterministic clauses; gate search touching TRAIN rows as select rows or any screened-or-reincluded TEST row; `mu==0` retrieval gate; ancestor resubstitution values substituted for the OOS leg; any `LEXICON-*` read on the blind path; authoring a new surface or lexicon.

## 4. Banks, lexicons, priors, screen (reuse by reference; no new collection)

- G3: `LEXICON-G3`, `GOAL-BANK-G3`, `OOS-BANK-G3` read at runtime from frozen `research/experiments/EXP-GRAPH-38291080992/prereg.md` §13.1–13.3 (byte-identical to `38205284279` per parent audit: 3834/6357/3672 chars). Blind-authorship property inherited by identity. G3 domain is public-transit fleet management (routes/vehicles/drivers/stops/fares), disjoint by construction from `goal_generator.py` vocabulary.
- G1/G2: `GOAL-BANK-G1/OOS-BANK-G1/LEXICON-G1/LEXICON-G1-ALT/GOAL-BANK-G2/OOS-BANK-G2/LEXICON-G2-HELDOUT` from frozen `research/experiments/EXP-GRAPH-38180711589/prereg.md`.
- Priors: `PRIOR-PARENT-BANK-TEXTS` from frozen `research/experiments/EXP-GRAPH-38175554380/prereg.md` + `research/harness/goal_generator.py` vocabularies.
- Contamination screen (frozen, unchanged): token Jaccard>=0.60 OR trigram Jaccard>=0.75 vs frozen priors+banks drops rows from binding (recorded in `flagged`, not counted). Reincluded TEST gids tripwired against parent-published `run_output.json#reincluded_test_gids` (no new TEST scoring in DESIGN): G3 test-app `app_026/app_030/app_036/app_076`; G1 per axis test `app_004/app_052/app_076/app_100/oos_024/oos_026`; G2 zero flagged rows (margin analytic-invariant).

## 5. Axes, splits, reincluded sets, and the frozen fit-pool contract

- Split rule (frozen, deterministic, unchanged): row `i` is test iff `(i%splitmod) in (1,3,5)`; `splitmod` 4 (G3, G2-HELDOUT) / 6 (G1, ALT). Same four axes and roles as parent. Screened bound counts (parent-published): G3 115 (cal 39+20 / test 36+20); G2 120 (cal 40+20 / test 40+20); G1/ALT 151 each.
- Reincluded TEST (frozen): `test_reincl = test + flagged_test` per axis (gold AND blind alike). Counts: G3 40 app + 20 OOS; G1/ALT 60 app + 20 OOS; G2 40 + 20 (identical to screened; `g2_reincl_identical` runtime-verified). Reincluded rows are scored post hoc through identical arms; they never enter fit/select.
- Fit-pool validity bars (frozen; failure = MEASUREMENT_INVALID/BLOCKED, §7): exact `N_TRAIN==102`, `SELECT_APP==34`, `SELECT_OOS==60` (deterministic; mismatch is bank drift, not tolerance), `TRAIN∩SELECT=∅`, `(TRAIN∪SELECT)∩(screened TEST ∪ reincluded TEST)=∅` (exact text-sha, covering the reincluded union). No TEST row is ever read by Arm A, any clause, the screen, or either fit/select leg. Blind TRAIN inputs are `(text,target)` pairs only.
- Decided sets: the PRIMARY decision is scored on the REINCLUDED superset (the audited current ceiling). Screened sets are scored as validity reproduction only. Per-axis blind gates on all four axes are reported; the decision label depends on `AXIS-G3-NEW` (novel-surface generalization axis) alone — pre-declared because G1-blind behavior under generic token overlap is informative but not decisive for the Director's bound question. G1/G2/ALTLEX TEST legs are non-decision characterization plus continuity tripwires.
- On the mandate's "frozen G3-NEW surface only" phrase (ON RECORD): the full four-axis apparatus is retained deliberately. The fit pool is pooled across G1/G2/G3 by construction (calibration is inherently multi-axis), and the gold continuity tripwires on all axes are what make this packet auditable as bank-identical; the marginal cost is nil (seconds). The decision is strictly on G3-NEW reincluded TEST. Single-variable ablation (only the tau rule changes) maximizes comparability with the parent BLIND_FAILS packet.

## 6. Metrics, gates, controls (stable identifiers; RQF-02/03/05/06 continuity)

- Frozen constants: `FA_TARGET=0.10, COV_TARGET=0.50, PREC_TARGET=0.85, SEL_TARGET=0.80, TOK_BAND=0.60, TRI_BAND=0.75, SEED=38816768796%(2**32)=162063132`.
- Per (axis, set, mode/arm): `coverage, pooled_false_accept, unknown_precision_exclusive (=OOS among resolved-then-abstained / resolved-abstained; null if none → blind pre-handled as gate-false, gold-reincluded as invalidity trigger), unknown_precision_inclusive (=OOS among all non-executed / all non-executed; SENSITIVITY ONLY, never gated), selective_acc, executed, executed_oos, executed_app, abstained_resolved (abstained for memory arms), unresolved_applicable`. New metric identities for this packet: `blind_select_rule="max-slack-fa-tiebreak-higher-tau"`, `blind_select_slack=(FA_TARGET − SELECT FA at tau*)`, `blind_select_tau=tau*`.
- PRIMARY gate (sole decision gate, pre-fixed, exclusive only): `pooled_false_accept<=0.10 AND coverage>=0.50 AND unknown_precision_EXCLUSIVE>=0.85`. Memory arms (retrieval, blind) gate on the same exclusive-formula precision (for them every scored row is decision-conditional, so exclusive==inclusive by construction; both reported). `selection_reincl_preserved = selective_acc>=0.80` on all four gold axes (continuity co-finding).
- Blind fork (descriptive, G3 reincluded): `blind_fork_of(gold_met, blind_met)` in `{BLIND_DOMINATES_G3, GOLD_DOMINATES_BLIND_G3, BOTH_PASS_G3, NEITHER_PASSES_G3}`. Retrieval fork continuity: `fork_of` on screened and reincluded (expect `TFRAME_DOMINATES_G3` both).
- Controls (stable ids, parent-continuous, all executed):
  - `PC-AXIS-G1-ALTLEX`: gold-reincluded gate-met; failure is runner-enforced MEASUREMENT_INVALID (RQF-06 continuity on the decided set), never a science negative.
  - `NC-EXEC-ALL` (`gatefree`): must pool materially more FA than gold Arm A on screened AND reincluded sets (parent TEST 0.2778–0.50 vs 0.0–0.10; DESIGN calibration 0.30–0.60 vs 0.0).
  - `NC-ABSTAIN-ALL`: EXECUTED on screened AND reincluded sets (RQF-03 continuity; no placeholders): executes nothing → `coverage=0.0`, `pooled_false_accept=null`, `unknown_precision_exclusive=OOS_resolved/all_resolved` (informative, not 1.0 by construction).
  - `CTRL-SHUFFLED-SELECTION`, `CTRL-RANDOM-ROLE`: near chance (gold screened and reincluded).
  - `CTRL-RANDOM-GATE`: volume-matched random abstention (parent FA 0.65–0.75).
  - `CTRL-B-LEX-ONLY` (gatefree selective_acc), `CTRL-INCUMBENT` (shipped lexical gate FA/selective_acc) on screened and reincluded sets.
  - `CTRL-BLIND-PERMUTED`: blind scorer with TRAIN targets shuffled by `Random(SEED+1)` (deterministic), SAME frozen `tau*` applied, scored on SELECT/screened/reincluded. SCOPED to the selection reading only: the execute/abstain partition is a function of scores, not labels, so permuted FA/COV/UP equal real blind by construction — it can never gate a label. It guards `selective_acc`: permuted selective ~chance is expected; if real blind gate-mets with selective≈permuted selective, the survival is abstention-driven (resolution-deficient grade), never shippable resolution.

## 7. Decision rule and product consequences (frozen cascade)

- `MEASUREMENT_INVALID` (`decision=null`) if ANY of spec.json §(a)–(f): fit-pool exact counts/disjointness fail (covering the TEST union); gold liveness fails on `AXIS-G3-NEW` REINCLUDED TEST; gold-reincluded exclusive UP undefined on any axis; `PC-AXIS-G1-ALTLEX` gold-reincluded fails (runner-enforced); any forbidden fallback (resubstitution/mu==0/screened-or-reincluded test-touch/clause refit/blind lexicon read); continuity tripwires fail (gold-screened vector != {G3 met, G1 met, ALTLEX met, G2 false} or G2 screened FA/COV bars not passing or screened fork != TFRAME_DOMINATES_G3 or screened retrieval meets any TEST gate or gold-reincluded vector != audited parent vector or flagged TEST gid sets != parent-published or reincluded gold-vs-retrieval fork != TFRAME_DOMINATES_G3 or reincluded retrieval meets any TEST gate). Blind degeneracy (`BLIND_INERT`) is pre-declared VALID collapse. Blind SELECT-infeasibility under the unchanged predicate is NOT invalid and NOT a mechanism failure → `TAU_RULE_INFEASIBLE` (`status=BLOCKED`, EXECUTE transcribes `result.json` outcome `NOT_APPLICABLE`): the mandate stop trigger, a drift guard provably non-taken on identical banks.
- Else: `blind_g3_met = arm_gate(blind AXIS-G3-NEW reincluded gate at tau*)`; `BLIND_SURVIVES` iff `blind_g3_met`, else `BLIND_FAILS`. `blind_fork_reincl`, per-axis blind gates, blind selective values, and `CTRL-BLIND-PERMUTED` shape `reason` and product text (graded) without adding labels.
- EXECUTE transcription (pre-declared for packet validity): BLIND_SURVIVES → `result.json{status=COMPLETE, outcome=SUPPORTS}`; BLIND_FAILS → `{status=COMPLETE, outcome=FALSIFIES}` (a valid scientific negative, not an infrastructure failure); TAU_RULE_INFEASIBLE → `{status=BLOCKED, outcome=NOT_APPLICABLE}`; any invalidity → `{status=MEASUREMENT_INVALID, outcome=NOT_APPLICABLE}`.
- Positive (BLIND_SURVIVES at tau*): lexicon-free viability demonstrated on the novel G3 surface under a pre-registered non-lowest-tau-wins rule; re-opens the embedding-vs-deterministic fork against DECIDE_REQUIRE_RETRIEVAL_B; shipped abstention boundary re-examined; Graph continues blind-resolver architecture (surface-local vs pooled memory, selective_acc hardening). Grade: selective>=0.80 → viability signal; selective<0.80 (published-shape expectation) → abstention-viable but resolution-deficient → selective_acc must enter the gate before any ship discussion. This packet promotes nothing itself.
- Negative (BLIND_FAILS at tau*): the word-unigram Jaccard 1-NN blind path fails the frozen G3 gate under BOTH the lowest-tau and the max-slack feasible-tau rules while G1/G2 negatives are tau-robust — the tie-break confound is closed and the mechanism (not the calibration) carries the failure. Park the blind thread at the PRIMARY+ALTLEX gold-lexicon-conditional bound; keep the conservative shipped abstention boundary with the retrieval-B requirement vacated in the gold-conditional sense; no further Jaccard-1NN blind work without a new mechanism class (structural-heuristic blind held as explicit follow-up). HYPOTHESIS retained with hardened ceiling. TAU_RULE_INFEASIBLE/INVALID/BLOCKED parks or retires the family per the mandate stop rule. This packet promotes nothing itself.

## 8. Design satisfiability probes (accepted evidence + read-only checks only; NO execution of any kind in DESIGN — not even SELECT scoring)

DESIGN ran zero outcome-bearing measurements and zero calibration scoring. In particular DESIGN deliberately did NOT run blind SELECT scoring to determine `tau*` in advance: with the auditor post hoc published, any SELECT execution would be outcome-bearing-by-proxy. All proofs below use accepted packet values, read-only file checks, and synthetic arithmetic. The new runner's `--mechanics-only` entry point never scores any TEST set (verified `test_not_scored=true` at EXECUTE).

**8.1 Measurement prerequisites (PASS, probed without outcome measurement).** Python 3.12.15 verified; runner source imports stdlib-only (`argparse/hashlib/json/math/os/re/random/sys/pathlib/__future__`) plus one repo-local `goal_generator` import inside `load_banks` (read-only source check); numpy/sklearn/sentence_transformers absent (import probes raise ModuleNotFoundError); `goal_generator` exposes INTENTS(20)/PARAPHRASES(20)/NO_APPLICABLE_TEMPLATES(20)/OOD_PARAPHRASES(8) (probed by import, no bank scoring); every runtime-read block verified present in its exact file (G3 blocks in `38291080992/prereg.md`; G1/G2/lexicon blocks in `38180711589/prereg.md`; `PRIOR-PARENT-BANK-TEXTS` in `38175554380/prereg.md`); fit-pool construction identical to parent by code identity (same `build_fit_pool`: 136 pooled cal-app → 102/34/60); no network/model/browser/credential; the mandate stop trigger (clause refit / new surface) has no code path (§13 diff audit: only the §2 rule lines, EXP_ID/SEED, and reporting fields differ).

**8.2 Feasibility + rule non-identity (PASS, proof from accepted evidence).** The feasibility predicate is byte-identical to the parent packet, which published 9 SELECT-feasible taus (`0.2727/0.3333/0.375/0.4/0.4286/0.5/0.5556/0.5714/0.6`, audit post hoc sweep) all at SELECT coverage 1.0 — so on identical banks the feasible set is provably non-empty and `tau*` is always emitted (fully-ordered key over distinct taus). Published SELECT FA (0.0833 at `0.2727` vs 0.0333 at `0.3333`) proves argmin-FA is never the lowest feasible tau: `tau* != 0.2727` regardless of the unpublished values. The tie-break confound is therefore genuinely varied by construction, and treatment-vs-parent calibration identity is disproven without any new measurement.

**8.3 Decision-rule reachability (PASS, synthetic enumeration).** Frozen rule enumerated over all boolean input combinations without touching frozen data: BLIND_SURVIVES, BLIND_FAILS, TAU_RULE_INFEASIBLE-stop, and null-invalid via any continuity/forbidden-fallback trigger are all reachable; no subsumed guard (`blind_g3_met` at `tau*` is independent of the continuity conjuncts; graded selection/permuted readings modulate text, never the label). Continuity tripwires (screened vector, screened fork, exact fit counts, flagged-gid equality, gold-reincluded vector, reincluded fork) are expected-pass drift detectors, not science branches.

**8.4 Arithmetic attainability (PASS).** SURVIVES-arith uses the published post hoc feasible-and-passing vector (`tau=0.3333`: G3 reincluded FA 0.10/COV 0.925/UP 0.8571 → gate True); FAILS-arith uses the published failing vector (`tau=0.2727`: FA 0.20 → False; any non-passing `tau*` likewise); INERT-arith (cov 0.0, UP null) → False via pre-handled bars. Gold reincluded liveness arithmetic True from parent counts (42/60 executed, 40 app, 7 resolved abstentions); G2 reinclusion +0 rows so UP 10/12=0.8333 carries analytically. Fit-pool bars exact and attainable (102/34/60 by code identity). Gatefree headroom extends to reincluded sets as reported controls.

**8.5 Baseline / comparator identity (PASS).** Gold deterministic (±C7), lexical incumbent, execute-all, pooled-centroid retrieval (disjoint fit/select/screened-test/reincluded-test, mu>0), and blind 1-NN (same pooled rows, five documented mechanism differences, no lexicon in scope) are distinct implementations; the ONLY change vs parent is the blind SELECT rule (§2); ancestors resub/embedding are non-decision identities. Gold reads no calibration pool; memory arms read no clause state; blind shares clause code with nothing and lexicons with nothing.

**8.6 Control sensitivity (PASS, parent values quoted as baselines + new scoped null).** NC-EXEC-ALL gap (DESIGN calibration 0.30–0.60 vs 0.0; parent TEST 0.2222–0.50) re-measured on reincluded and screened sets; random-gate parent FA 0.65–0.75; shuffled/random near chance on screened and reincluded gold sets; abstain-all executed on both supersets (coverage 0.0 floor, UP informative) so both degeneracy directions are live twice; PC runner-enforced as invalidity on the decided set. CTRL-BLIND-PERMUTED scoped to selection at the new frozen `tau*` (label-invariance proof in §6: partition is a function of scores, hence identical for any fixed tau) so it cannot deaden the gate. Blind INERT collapse is the pre-registered informative treatment outcome, not an insensitive control. No insensitive control.

**8.7 No missing prerequisite (PASS).** §8.1 (environment, imports, blocks, pool identity, no-refit-path) covers every runtime input of §13; §8.2 covers rule inputs (feasible set proven non-empty on identical banks); §6 covers denominator definedness (gold-reincluded UP-undefined → invalidity trigger; blind UP-null → pre-handled gate-false). No frozen computation reads an unbound input.

**8.8 Freeze artifacts bounded (PASS).** Exactly the four mutable local interpretation dependencies in `spec.json#freeze_artifacts` (§12); DESIGN-verified sha256 all match parent `freeze.json#artifact_hashes` (files unchanged — hashes recomputed in DESIGN, §12); runner, banks, lexicons, constants and the max-slack rule otherwise bound via this prereg's hash (§13) + runtime self-hash.

**8.9 Self-attack (declared threats, not failures).** (i) Post-hoc-knowledge contamination (DISCLOSED, mitigated mechanically): DESIGN knows the auditor post hoc (`0.3333` passes, `0.2727` fails, G1/G2 tau-robust). Mitigation: the rule is fixed on SELECT-only inputs, computed once by the frozen runner before any TEST scoring in EXECUTE; DESIGN performed no scoring at all (§8 head); AUDIT re-derives `tau*` from SELECT data and checks TEST-blindness of selection. The residual risk (rule chosen because a feasible-and-passing tau exists post hoc) is inherent to the Director's explicit question and is disclosed, not hidden. (ii) Permuted-label trap (CAUGHT in DESIGN, parent continuity): a naïve `SURVIVES requires permuted-blind gate-false` conjunct would be unsatisfiable — the abstention partition is label-invariant, so permuted FA/COV/UP equal real blind by construction. Scoped to selection instead (§6). (iii) SELECT `selective_acc=0.0` for BOTH memory arms (accepted evidence): blind survival-with-selection≥0.80 is unlikely; the graded consequence (abstention-viable/resolution-deficient → gate redesign, no ship) keeps every branch decision-changing without pretending resolution quality unmeasured. (iv) Pooled-dilution symmetry: both memory arms share the dilution bias; a joint failure bounds lexicon-free MEMORY statistics, not all conceivable blind mechanisms — the ceiling is stated exactly so (retire ambitions/park, not prove impossibility). (v) G1 text-identity persists (three independent surfaces, not four). (vi) G3 FA zero-slack fragility carries (published `0.3333` sits exactly at 0.10; gold likewise C7-carried) — quoted ceiling, not re-litigated; a SURVIVES at zero slack re-opens but does not harden. (vii) Gating on inclusive would manufacture viability without evidence — forbidden. (viii) Refit/resubstitution/new-surface would repeat confounded/out-of-scope designs — forbidden (BLOCKED). (ix) Re-running the exact parent design without the rule change would be a DUPLICATE — this packet varies exactly the Director-mandated factor. (x) Held-out-axis alternative declined on record (§2) to preserve single-variable ablation.

**8.10 Empty-branch / identity / ceiling audit (PASS — active disproof attempt recorded).** Attacked and cleared: (i) no empty decision branch — synthetic enumeration reaches BLIND_SURVIVES/BLIND_FAILS/TAU_RULE_INFEASIBLE/null-invalid; SURVIVES requires blind G3 gate-met at `tau*` (live per §8.4 published vector), FAILS requires gate-false (live per published `0.2727` vector and the non-passing-`tau*` case); TAU_RULE_INFEASIBLE is a declared drift guard proven non-taken on identical banks, same class as invalidity conjuncts; continuity legs are expected-pass validity tripwires and the blind/fork/selection measurements change the product state on every branch; the graded selection reading modulates consequence text rather than gating a label, so no label depends on the unlikely selective≥0.80 leg. (ii) no treatment/comparator identity — disjoint code paths, disjoint fitted statistics, same-rows-by-ablation-design, §8.5, plus proven parent-vs-current calibration non-identity (§8.2). (iii) no ceiling baseline — gatefree headroom on both set families. (iv) no insensitive control — §8.6 (+permuted scoping proof). (v) no missing prerequisite — §8.7. (vi) no unbound mutable artifact — §8.8 (four files, hashes verified). (vii) no treatment/comparator/outcome identity with pre-2.0 — §0 legacy position (0 precedent hits; mechanism, denominator, calibration, and rule all differ).

## 9. Cost and expected information gain

- Cost: no model calls/network/browser/packages/authorship; one deterministic run over ~500 bound rows + 14 reincluded TEST rows + pooled fit (199 cal rows) + nested gate searches + blind 1-NN scoring + permuted null; seconds of CPU.
- Gain: one batch closes the auditor-flagged tie-break confound — the cheapest decision-changing step on the idle Graph lane. Predicted shape (not a result): VALID packet either way; BLIND_FAILS under max-slack is the confound-closing negative that retires the Jaccard-1NN path and parks the thread; BLIND_SURVIVES (gate-met at `tau*`) re-opens the fork and the shipped boundary, graded by selection. TAU_RULE_INFEASIBLE/INVALID/BLOCKED stops or parks the family. Screened/gold/retrieval reproduction is disclosed non-evidence; every blind branch changes the claim or product state.

## 10. Environment and EXECUTE command

- Python 3.12.15, stdlib only. EXECUTE extracts `FROZEN-RUNNER` (§13) to `raw_evidence/runner_blind_resolver.py` (block bytes + exactly one trailing newline; sha256 must equal `CANONICAL-RUNNER-SHA256 = d43563861b55600ebead5d344c0f5eede94e8ea93ff19d9c36a1af24320f536f`), then:
  `python3 research/experiments/EXP-GRAPH-38816768796/raw_evidence/runner_blind_resolver.py --mechanics-only` (twice; byte-identical required; TEST gates/forks/decisions never computed) →
  `python3 research/experiments/EXP-GRAPH-38816768796/raw_evidence/runner_blind_resolver.py > research/experiments/EXP-GRAPH-38816768796/raw_evidence/run_output.json`
- Determinism: fixed `SEED=162063132`; no wall-clock/RNG-dependent state beyond `random.Random(SEED)` (gold shuffles) and `random.Random(SEED+1)` (permuted null). EXECUTE writes `result.json/report.md/provenance.json` from `run_output.json` only, preserving stable metric/control identifiers from §6 and the §7 transcription rule.

## 11. Runner identity and environment notes

- `CANONICAL-RUNNER-SHA256 = d43563861b55600ebead5d344c0f5eede94e8ea93ff19d9c36a1af24320f536f` is the sha256 of the extracted runner file (FROZEN-RUNNER block + one trailing newline), computed at DESIGN end from the frozen block bytes (hash computation only; no execution of any kind was performed in DESIGN). EXECUTE verifies the extracted file hash (`runner_self_sha`) and AUDIT re-verifies with byte-identical reruns plus an independent blind-path reimplementation and a blind-block-vs-contract diff. The §13 diff vs the parent runner is confined to: EXP_ID/SEED constants, the header comment, the `arm_blind_oos` selection key (ascending first-max → max-FA-slack with higher-tau tie-break) plus `select_rule`/`select_slack` reporting, the mechanics-only `blind_select` reporting, and the `TAU_RULE_INFEASIBLE` decision mapping. Every other byte of analysis logic is identical by construction (patched programmatically from the audited parent runner, compiled clean).

## 12. Freeze artifacts (v2)

- `research/experiments/EXP-GRAPH-38180711589/prereg.md` (G1/G2 banks + lexicons; DESIGN sha `5a64e90da4d1c13b4a290b988cc6096838119d09869abd69512d095cd9318cb0`, matches parent freeze hash)
- `research/experiments/EXP-GRAPH-38175554380/prereg.md` (prior-bank texts; DESIGN sha `dc90bf71ed03a2329b641d46c1f4f70a53dbeef95ebd6d688645f697868aff9b`, matches parent freeze hash)
- `research/experiments/EXP-GRAPH-38291080992/prereg.md` (G3 banks + lexicon, reuse by reference; DESIGN sha `5a9cc1190674ffa5a8e6d604f6735ae6a9e2e27ffc9358c82d263f51b43d5735`, matches parent freeze hash)
- `research/harness/goal_generator.py` (contamination priors; DESIGN sha `cb5218de6a992cf29e26eee8fd5be4b4d7a50084ac3b885587a8ee1da20ace5f`, matches parent freeze hash)
All other inputs (runner, constants, max-slack gate rule, tripwire values) are embedded in §13 and hashed via this prereg.

## 13. FROZEN-RUNNER (the exact frozen treatment + honest comparator; hashed at freeze)

<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38816768796 (design_contract_version 2).
# Tau-rule-sensitivity packet: BLIND-JAC-1NN (genuinely blind: no LEXICON-* read
# at any stage) with a PRE-REGISTERED NON-LOWEST-TAU-WINS SELECT rule
# (feasibility-plus-maximum-FA-slack: argmax over SELECT-feasible taus of
# (FA_TARGET - SELECT pooled_false_accept), tie-break HIGHER tau wins),
# on the frozen banks, against gold T-FRAME+ and honest B-RETRIEVAL-OOS.
# Single-variable ablation vs EXP-GRAPH-38666634300: ONLY the blind tau-selection
# rule changes (ascending-tau first-max -> max-FA-slack); every other byte of
# analysis logic is identical apart from EXP_ID/SEED constants.
# Arm A-gold = T-FRAME+ : shared deterministic lexical selection (B-LEX-STRONG, frozen)
#   + structural frame-completeness abstention clauses C1/C3/C4/C5/C6 (frozen)
#   + C7-CREATE-OBLIQUE (zero tunable parameters). Analysis functions byte-identical to the
#   audited EXP-GRAPH-38530149021 runner lineage; constants re-frozen below; pre-declared
#   blind-leg additions only (blind 1-NN block, blind fork helper, reincluded-scope
#   liveness, continuity tripwires, settled-XSURF-leg removal). NO clause-refit path exists.
# Arm B-OOS = B-RETRIEVAL-OOS : stdlib TF-IDF nearest-class-centroid retrieval with
#   IDF+centroids fit on pooled calibration FIT-TRAIN, gate (tau,mu) selected on
#   disjoint pooled FIT-SELECT under hard mu>0, applied frozen to screened AND reincluded tests.
#   Resubstitution (train==select), mu==0 gates, and any screened-or-reincluded TEST-row use
#   in fit/select are FORBIDDEN and force BLOCKED/measurement-invalid (never silent reuse).
# BLIND-JAC-1NN = treatment: word-unigram Jaccard 1-NN over pooled FIT-TRAIN exemplars,
#   single tau on FIT-SELECT, no LEXICON-* in scope at any stage (see blindness contract
#   in code comments below). Same pooled rows by ablation design (mechanism-given-data).
# Stdlib only. Usage: python runner_blind_resolver.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, os, re, random, sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38816768796"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
G1G2SRC = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
G3SRC = ROOT / "research/experiments" / "EXP-GRAPH-38291080992"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

SEED = 38816768796 % (2 ** 32)
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
SEL_TARGET = 0.80
TOK_BAND = 0.60
TRI_BAND = 0.75
N_TRAIN_FROZEN = 102
N_SELECT_APP_FROZEN = 34
N_SELECT_OOS_FROZEN = 60

# Parent-published flagged TEST gids (tripwire values, from EXP-GRAPH-38530149021/result.json#reincluded_test_gids)
EXPECTED_FLAGGED_TEST = {
    "AXIS-G3-NEW": ["app_026", "app_030", "app_036", "app_076"],
    "AXIS-G2-RETEST": [],
    "AXIS-G1-PRIMARY": ["app_004", "app_052", "app_076", "app_100", "oos_024", "oos_026"],
    "AXIS-G1-ALTLEX": ["app_004", "app_052", "app_076", "app_100", "oos_024", "oos_026"],
}
EXPECTED_GOLD_REINCL = {"AXIS-G3-NEW": True, "AXIS-G2-RETEST": False, "AXIS-G1-PRIMARY": True, "AXIS-G1-ALTLEX": True}
EXPECTED_GOLD_SCREENED = {"AXIS-G3-NEW": True, "AXIS-G2-RETEST": False, "AXIS-G1-PRIMARY": True, "AXIS-G1-ALTLEX": True}

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
    """Gate check for retrieval/blind test_gate entries (screened or reincluded)."""
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


def blind_fork_of(gold_g3_met, blind_g3_met):
    if blind_g3_met and not gold_g3_met:
        return "BLIND_DOMINATES_G3"
    if gold_g3_met and not blind_g3_met:
        return "GOLD_DOMINATES_BLIND_G3"
    if gold_g3_met and blind_g3_met:
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


# ---------------- BLIND-JAC-1NN : genuinely blind resolver (NEW treatment) ----------------
# BLINDNESS CONTRACT (auditable): these functions accept ONLY (text, target) exemplar
# pairs from the pooled FIT-TRAIN pool. No LEXICON-* object is in scope here: no lex
# parameter exists, no lexicon block is read, no surface-form dictionary is consulted.
# Resolution = 1-nearest TRAIN exemplar by word-unigram Jaccard; abstention = single
# threshold tau on the 1-NN Jaccard score, fitted on FIT-SELECT only.
# Mechanism distance from B-RETRIEVAL-OOS (identifiability): (1) features unigram-only
# vs uni+bigram; (2) no IDF/term weighting (raw sets) vs sublinear-tf*IDF; (3) 1-NN
# exemplar vs per-class L2 centroid; (4) Jaccard vs cosine; (5) single-tau gate vs
# (tau,mu) margin gate. Shared by design: the SAME pooled FIT-TRAIN/FIT-SELECT rows
# (the separator is mechanism-given-data, the standard ablation shape).
def _blind_token_set(text):
    return set(tokens(text))


def blind_jac_predict(tok_sets_targets, text):
    """1-NN by unigram Jaccard over pooled TRAIN exemplars. Deterministic: fixed TRAIN
    order, strict-greater replacement, so ties resolve to the earliest TRAIN row."""
    q = _blind_token_set(text)
    best_cls, best_s = None, -1.0
    for toks, cls in tok_sets_targets:
        inter = len(q & toks)
        union = len(q | toks)
        s = inter / union if union else 0.0
        if s > best_s:
            best_s, best_cls = s, cls
    return best_cls, best_s


def blind_gate_metrics(scored, tau):
    """Same gate formula as retrieval (every scored row is decision-conditional, so
    exclusive==inclusive by construction). scored = [(row, pred_cls, score)]."""
    ex = [(r, c) for r, c, s in scored if s >= tau]
    ab = [(r, c, s) for r, c, s in scored if not (s >= tau)]
    exo = sum(1 for r, c in ex if not r["app"]); exa = sum(1 for r, c in ex if r["app"])
    co = sum(1 for r in scored if not r[0]["app"]); ca = sum(1 for r in scored if r[0]["app"])
    abRo = sum(1 for r, c, s in ab if not r["app"])
    sel = sum(1 for r, c in ex if r["app"] and c == r["target"])
    up = abRo / len(ab) if ab else None
    return dict(coverage=exa / ca if ca else 0.0, pooled_false_accept=exo / co if co else None,
                unknown_precision_exclusive=up, unknown_precision_inclusive=up, unknown_precision=up,
                selective_acc=sel / exa if exa else None,
                executed=len(ex), executed_app=exa, executed_oos=exo, abstained=len(ab))


def arm_blind_oos(train, sel_app, sel_oos, tests, tests_reincl, permute_seed=None, frozen_tau=None):
    """Blind 1-NN fit on TRAIN exemplar texts; single tau selected on SELECT
    by the frozen max-FA-slack rule (argmax over feasible of FA_TARGET - SELECT FA,
    tie-break higher tau; explicitly NOT lowest-tau-wins);
    frozen tau applied to screened AND reincluded tests. permute_seed is not None only
    for CTRL-BLIND-PERMUTED (TRAIN targets shuffled by Random(permute_seed); the REAL
    frozen tau passed via frozen_tau is applied unchanged, so the execute/abstain
    partition equals the real blind partition by construction and only the predicted
    labels differ). Never reads TEST rows in fit/select; never reads any lexicon."""
    fit_pairs = [(_blind_token_set(r["text"]), r["target"]) for _, r in train]
    if permute_seed is not None:
        rng = random.Random(permute_seed)
        tgts = [c for _, c in fit_pairs]
        rng.shuffle(tgts)
        fit_pairs = [(t, c) for (t, _), c in zip(fit_pairs, tgts)]
        assert frozen_tau is not None, "permuted null requires the real frozen tau"

    def score(rows):
        out = []
        for r in rows:
            cls, s = blind_jac_predict(fit_pairs, r["text"])
            out.append((r, cls, s))
        return out

    sel_rows = [r for _, r in sel_app] + [r for _, r in sel_oos]
    sel_scored = score(sel_rows)
    if frozen_tau is not None:
        tau = frozen_tau
        select_gate = blind_gate_metrics(sel_scored, tau)
        fit_feasible = arm_gate(select_gate)
        select_slack = ((FA_TARGET - select_gate["pooled_false_accept"])
                        if select_gate["pooled_false_accept"] is not None else None)
    else:
        # PRE-REGISTERED NON-LOWEST-TAU-WINS RULE (max-FA-slack):
        # among SELECT-feasible taus maximise (FA_TARGET - SELECT FA);
        # tie-break HIGHER tau wins (explicitly not lowest-tau-wins).
        # Key is fully ordered (taus distinct), so strict-greater picks the
        # unique maximum regardless of iteration order.
        taus = sorted({round(s, 4) for _, _, s in sel_scored})
        best = None
        for tau in taus:
            gm = blind_gate_metrics(sel_scored, tau)
            feasible = (gm["pooled_false_accept"] is not None and gm["pooled_false_accept"] <= FA_TARGET
                        and gm["coverage"] >= COV_TARGET
                        and gm["unknown_precision_exclusive"] is not None and gm["unknown_precision_exclusive"] >= PREC_TARGET)
            slack = (FA_TARGET - gm["pooled_false_accept"]) if feasible else -1.0
            key = (1 if feasible else 0, slack, tau)
            if best is None or key > best[0]:
                best = (key, tau, gm)
        tau = best[1]
        select_gate = best[2]
        fit_feasible = bool(best[0][0])
        select_slack = best[0][1] if fit_feasible else None
    out_tests = {}
    for a, trows in tests.items():
        out_tests[a] = blind_gate_metrics(score(trows), tau)
    out_reincl = {}
    for a, trows in tests_reincl.items():
        out_reincl[a] = blind_gate_metrics(score(trows), tau)
    return dict(feasible=fit_feasible, reason=None if fit_feasible else "no-feasible-tau-gate-on-SELECT",
                tau=tau, select_rule="max-slack-fa-tiebreak-higher-tau", select_slack=select_slack,
                select_gate=select_gate, n_fit_train=len(fit_pairs),
                n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                permuted=bool(permute_seed is not None),
                test_gate=out_tests, test_gate_reincl=out_reincl)


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
    for nm, (app, oos, lex, sm, priors) in spec.items():
        bound, flagged, flagged_test = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, flagged_test=flagged_test, cal=cal, test=test,
                        test_reincl=test + flagged_test,
                        cal_metrics={m: metrics(cal, m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")})
    return axes


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    banks = load_banks()
    axes = build_axes(banks)
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
        blind_res = arm_blind_oos(train, sel_app, sel_oos, {}, {})
        # CAL-only blind probes (no TEST rows read or scored here):
        sel_rows = [r for _, r in sel_app] + [r for _, r in sel_oos]
        cal_rows = [r for a, v in axes.items() for r in v["cal"]]
        fit_pairs = [(_blind_token_set(r["text"]), r["target"]) for _, r in train]
        btau = blind_res["tau"]
        cal_scored = []
        for r in cal_rows:
            cls, s = blind_jac_predict(fit_pairs, r["text"])
            cal_scored.append((r, cls, s))
        cal_gm = blind_gate_metrics(cal_scored, btau)
        out = dict(status="DESIGN-MECHANICS-ONLY", experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
                   seed=SEED,
                   axes={k: dict(bound=len(v["bound"]), flagged=v["flagged"],
                                 flagged_test_gids=[r["gid"] for r in v["flagged_test"]],
                                 flagged_test_match_expected=([r["gid"] for r in v["flagged_test"]] == EXPECTED_FLAGGED_TEST[k]),
                                 cal_n=[sum(1 for r in v["cal"] if r["app"]), sum(1 for r in v["cal"] if not r["app"])],
                                 cal_metrics=v["cal_metrics"],
                                 cal_feasible_tframeplus=gate_met(v["cal_metrics"]["tframeplus"])) for k, v in axes.items()},
                   c7_firing={k: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                      oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                              for k, v in axes.items()},
                   fit_pool=construction,
                   retrieval_select=dict(feasible=fit_res["feasible"], reason=fit_res["reason"],
                                         tau=fit_res["tau"], mu=fit_res["mu"],
                                         mu_active=bool(fit_res["mu"] is not None and fit_res["mu"] > 0),
                                         select_gate=fit_res["select_gate"]),
                   blind_select=dict(feasible=blind_res["feasible"], reason=blind_res["reason"],
                                     tau=blind_res["tau"], select_rule=blind_res["select_rule"],
                                     select_slack=blind_res["select_slack"],
                                     select_gate=blind_res["select_gate"]),
                   blind_cal_probe=dict(select_executed=blind_res["select_gate"]["executed"],
                                        select_abstained=blind_res["select_gate"]["abstained"],
                                        cal_executed=cal_gm["executed"], cal_abstained=cal_gm["abstained"],
                                        cal_coverage=cal_gm["coverage"],
                                        cal_selective=cal_gm["selective_acc"],
                                        cal_up=cal_gm["unknown_precision_exclusive"]),
                   blind_lexicon_guard=dict(
                       lex_params_in_blind_scope=False,
                       note="arm_blind_oos/blind_jac_predict accept only (text,target) pairs; no lexicon object in scope"),
                   test_not_scored=True)
        print(json.dumps(out, indent=2))
        return

    for a, v in axes.items():
        v["test_metrics"] = {m: metrics(v["test"], m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
        v["reincl_metrics"] = {m: metrics(v["test_reincl"], m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
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
    blind_res = arm_blind_oos(train, sel_app, sel_oos, tests, tests_reincl)
    blind_perm = arm_blind_oos(train, sel_app, sel_oos, tests, tests_reincl, permute_seed=SEED + 1,
                              frozen_tau=blind_res["tau"])

    gates = {a: gate_met(v["test_metrics"]["tframeplus"]) for a, v in axes.items()}
    gates_reincl = {a: gate_met(v["reincl_metrics"]["tframeplus"]) for a, v in axes.items()}
    sels_reincl = {a: v["reincl_metrics"]["tframeplus"]["selective_acc"] for a, v in axes.items()}
    selection_reincl = all(s is not None and s >= SEL_TARGET for s in sels_reincl.values())
    # gold liveness on the REINCLUDED G3 TEST (scope-adapted from the parent screened rule)
    g3tr = axes["AXIS-G3-NEW"]["test_reincl"]
    prim_reincl = axes["AXIS-G3-NEW"]["reincl_metrics"]["tframeplus"]
    g3tr_abstained_resolved = sum(1 for r in g3tr if r["mech"] is not None and not is_executed(r, "tframeplus"))
    live = ((0 < prim_reincl["executed"] < len(g3tr))
            and (prim_reincl["executed_app"] >= 1)
            and (g3tr_abstained_resolved >= 1))
    arm_g3 = (fit_res["test_gate"] or {}).get("AXIS-G3-NEW")
    armb_g3_met = arm_gate(arm_g3)
    armr_g3 = (fit_res["test_gate_reincl"] or {}).get("AXIS-G3-NEW")
    armr_g3_met = arm_gate(armr_g3)
    retrieval_fork = fork_of(gates.get("AXIS-G3-NEW"), armb_g3_met, fit_res["feasible"])
    retrieval_fork_reincl = fork_of(gates_reincl.get("AXIS-G3-NEW"), armr_g3_met, fit_res["feasible"])
    blind_g3 = (blind_res["test_gate_reincl"] or {}).get("AXIS-G3-NEW")
    blind_g3_met = arm_gate(blind_g3)
    blind_gates_reincl = {a: arm_gate((blind_res["test_gate_reincl"] or {}).get(a)) for a in axes}
    blind_gates_screened = {a: arm_gate((blind_res["test_gate"] or {}).get(a)) for a in axes}
    blind_perm_g3 = (blind_perm["test_gate_reincl"] or {}).get("AXIS-G3-NEW")
    blind_inert = bool(blind_g3 is not None and (blind_g3["executed"] == 0 or blind_g3["abstained"] == 0))
    bfork = blind_fork_of(gates_reincl.get("AXIS-G3-NEW"), blind_g3_met)
    invalid_reasons = []
    if not construction_ok:
        invalid_reasons.append("fit-pool-construction-failed: N_TRAIN==102 AND SELECT_APP==34 AND SELECT_OOS==60 AND train/select/test-union disjointness required; resubstitution fallback forbidden")
    if not live:
        invalid_reasons.append("treatment-not-live: AXIS-G3-NEW gold-reincluded test non-degenerate execution failed (need 0 < executed_total < n_total_test AND executed_app >= 1 AND abstained_resolved >= 1)")
    for a, v in axes.items():
        if v["reincl_metrics"]["tframeplus"]["unknown_precision_exclusive"] is None:
            invalid_reasons.append(f"{a}: unknown_precision_exclusive undefined on gold-reincluded test (no resolved abstention)")
    if not gates_reincl.get("AXIS-G1-ALTLEX"):
        invalid_reasons.append("positive-control-failed: PC-AXIS-G1-ALTLEX gold-reincluded gate-met false (runner-enforced invalidity)")
    if gates != EXPECTED_GOLD_SCREENED:
        invalid_reasons.append("screened-reproduction-failed: gold-screened gate vector != parent {G3 met, G1 met, ALTLEX met, G2 false}")
    g2m = axes["AXIS-G2-RETEST"]["test_metrics"]["tframeplus"]
    if not (g2m["pooled_false_accept"] is not None and g2m["pooled_false_accept"] <= FA_TARGET
            and g2m["coverage"] is not None and g2m["coverage"] >= COV_TARGET):
        invalid_reasons.append("screened-reproduction-failed: G2 screened FA/COV bars not passing (false-solely-on-UP required)")
    if retrieval_fork != "TFRAME_DOMINATES_G3":
        invalid_reasons.append("screened-fork-reproduction-failed: screened fork != TFRAME_DOMINATES_G3")
    if any(arm_gate((fit_res["test_gate"] or {}).get(a)) for a in axes):
        invalid_reasons.append("screened-retrieval-reproduction-failed: screened retrieval meets a TEST gate (parent: all four fail)")
    if gates_reincl != EXPECTED_GOLD_REINCL:
        invalid_reasons.append("gold-drift: gold-reincluded gate vector != audited parent reincluded vector (bank drift, not science)")
    if any([r["gid"] for r in v["flagged_test"]] != EXPECTED_FLAGGED_TEST[a] for a, v in axes.items()):
        invalid_reasons.append("screen-drift: reincluded TEST gid sets != parent-published flagged sets")
    if retrieval_fork_reincl != "TFRAME_DOMINATES_G3":
        invalid_reasons.append("fork-drift: reincluded gold-vs-retrieval fork != TFRAME_DOMINATES_G3")
    if any(arm_gate((fit_res["test_gate_reincl"] or {}).get(a)) for a in axes):
        invalid_reasons.append("retrieval-drift: reincluded retrieval meets a TEST gate (parent: all four fail)")
    status = "MEASUREMENT_INVALID" if invalid_reasons else "COMPLETE"
    if invalid_reasons:
        decision = None
    elif not blind_res["feasible"]:
        # Pre-registered mandate stop trigger: the feasibility predicate is byte-identical
        # to the parent packet (9 SELECT-feasible taus published), so on identical banks
        # this branch is a drift guard only. Bank drift must never read as mechanism failure.
        status = "BLOCKED"
        decision = "TAU_RULE_INFEASIBLE"
    elif blind_g3_met:
        decision = "BLIND_SURVIVES"
    else:
        decision = "BLIND_FAILS"
    out = dict(status=status, experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
               invalid_reasons=invalid_reasons, decision=decision, blind_fork_reincl=bfork,
               blind_g3_met=blind_g3_met, blind_inert=blind_inert,
               blind_gates_screened=blind_gates_screened, blind_gates_reincl=blind_gates_reincl,
               gates=gates, gates_reincl=gates_reincl,
               selection_reincl={a: sels_reincl[a] for a in sels_reincl}, selection_reincl_preserved=selection_reincl,
               retrieval_fork=retrieval_fork, retrieval_fork_reincl=retrieval_fork_reincl,
               retrieval_oos_feasible=fit_res["feasible"], retrieval_oos_reason=fit_res["reason"],
               arm_b_oos=dict(tau=fit_res["tau"], mu=fit_res["mu"],
                              mu_active=bool(fit_res["mu"] is not None and fit_res["mu"] > 0),
                              n_fit_train=fit_res["n_fit_train"], n_select_app=fit_res["n_select_app"],
                              n_select_oos=fit_res["n_select_oos"], classes=fit_res["classes"],
                              select_gate=fit_res["select_gate"], test_gate=fit_res["test_gate"],
                              test_gate_reincl=fit_res["test_gate_reincl"]),
               arm_blind_oos=dict(tau=blind_res["tau"], select_rule=blind_res["select_rule"],
                                  select_slack=blind_res["select_slack"],
                                  feasible=blind_res["feasible"], reason=blind_res["reason"],
                                  n_fit_train=blind_res["n_fit_train"], n_select_app=blind_res["n_select_app"],
                                  n_select_oos=blind_res["n_select_oos"],
                                  select_gate=blind_res["select_gate"], test_gate=blind_res["test_gate"],
                                  test_gate_reincl=blind_res["test_gate_reincl"],
                                  permuted_selective=(blind_perm["select_gate"] or {}).get("selective_acc"),
                                  permuted_test_gate=blind_perm["test_gate"],
                                  permuted_test_gate_reincl=blind_perm["test_gate_reincl"],
                                  permuted_g3_met=arm_gate(blind_perm_g3)),
               fit_pool=construction,
               test_metrics={a: v["test_metrics"] for a, v in axes.items()},
               test_reincl_metrics={a: v["reincl_metrics"] for a, v in axes.items()},
               test_n={a: [sum(1 for r in v["test"] if r["app"]), sum(1 for r in v["test"] if not r["app"])] for a, v in axes.items()},
               test_n_reincl={a: [sum(1 for r in v["test_reincl"] if r["app"]), sum(1 for r in v["test_reincl"] if not r["app"])] for a, v in axes.items()},
               reincluded_gids={a: [r["gid"] for r in v["flagged_test"]] for a, v in axes.items()},
               cal_metrics={a: v["cal_metrics"] for a, v in axes.items()},
               c7_firing={a: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                  oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
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
                                 ctrl_abstain_all_cov=v["abstain_all"]["coverage"],
                                 ctrl_abstain_all_up=v["abstain_all"]["unknown_precision_exclusive"],
                                 ctrl_abstain_all_up_inclusive=v["abstain_all"]["unknown_precision_inclusive"],
                                 ctrl_abstain_all_reincl_cov=v["abstain_all_reincl"]["coverage"],
                                 ctrl_abstain_all_reincl_up=v["abstain_all_reincl"]["unknown_precision_exclusive"],
                                 ctrl_abstain_all_reincl_up_inclusive=v["abstain_all_reincl"]["unknown_precision_inclusive"]) for a, v in axes.items()},
               flagged={a: v["flagged"] for a, v in axes.items()})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER -->
