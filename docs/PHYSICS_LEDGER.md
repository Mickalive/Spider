# PHYSICS LEDGER

## WP-006 (2026-08-25, cycle 3, run 32776372437) — Identifiability-by-restart gate (H-ID)

- **Status: FALSIFIED by the frozen verdict mapping — TEAM RESULT, PENDING
  INDEPENDENT AUDIT** (this entry records the team outcome with exact
  provenance; audit status will be appended by the Lane Director after the
  independent Physics audit, per lane discipline).
- Preregistration frozen before any data: `reports/physics/wp006_preregistration.md`
  in freeze commit `aba6858` (2026-08-24T21:30:49Z), which also contains the
  restart/matched-state collector v4 (`physics/collector_wp006.py`), driver,
  frozen analysis and independent verifier. Disclosure/smoke commit `744cdd3`
  precedes the freeze. All 1075 committed rows postdate the freeze (verifier
  C3 = 0 rows before freeze).
- Dataset `wp006_v1`: 8 sites ATTEMPTED (5 static + 3 stateful), 164
  calibration rows + 910 trial rows (704 valid / 206 invalid, exclusions
  counted by reason); compact rows at `data/physics/wp006_trials.jsonl.gz`
  (sha256 in `data/manifests/wp006_dataset_manifest.json`); resolved-BP
  references/calibration artifact `data/physics/wp006_bp_manifest.json`.
- **Outcome (frozen rule trace): producers 2/4 (books 12, quotes 12);
  total verified matched branch points 38/60 ⇒ FALSIFIED for H-ID at the
  director floors.** No hard validity-gate failure (G2/G4/G5/G7 green);
  execution adequate ⇒ not DATA_INSUFFICIENT; verifier PASS with own
  reference path, verdict agreement true.
- Mandatory decomposition (report §2 — read before interpreting): calibration
  double-reset control passed 62/62 BPs (~0% false-negative rate of the
  state-match tolerance); per-site valid-trial rates books 168/168,
  quotes 168/168, saucedemo 98/98 and parabank 70/70 (both full fresh-context
  logins), internet 28/28, wikipedia & gutenberg 84/168 each, openlibrary
  4/42 (cap-truncated). Of cells with ≥1 valid trial, 101/102 showed
  all-identical T2 outcome distributions (near-deterministic response).
  The floor miss is localized: (i) the frozen ordinal-0 anchor slot selected
  non-actionable accessibility skip-links on wikipedia+gutenberg skins
  (171 action_failed exclusions; one dead arm per BP zeroed 24 otherwise
  reproducible BPs), (ii) openlibrary page-weight timeouts + 13 state_match
  failures, (iii) planned stateful BP counts (≤8) below the ≥10 producer bar
  by design despite saucedemo verifying 7/7 of its plan.
- Pre-outcome instrument repairs (gate G8 compliant, zero outcomes observed
  before the final build): nested sync-playwright crash fix (`a5c5112`,
  pre-fix collector sha256 49d2218b… preserved) and trial-row persistence fix
  (`d8303d2`); partial rows from defective builds discarded both times.
- Per the directive's pre-declared stop condition, H-ID FALSIFIED engages
  lane termination at the next Director step. The Director owns that decision;
  the team adds only the bounded facts above (state reproducibility and
  near-deterministic matched-state response succeeded everywhere execution
  existed; the shortfall is instrument-side action executability and floor
  arithmetic). No committor/barrier estimation was performed (WP-004 stays
  BLOCKED); no cross-site transfer claim was retested.
- **ERRATUM (repair round 1, GitHub run 32793165981) — additive correction
  per independent audit `results/audit/CYCLE_32776372437_PHYSICS_GATE.json`
  (REVISE, RF1–RF5); original bullet above preserved verbatim, pre-fix
  ledger sha256 `9d5da8136b137184a6d0034eebaac07c1a60e3ee71aca7ce8a2f81886d973841`.**
  Original claim: *"calibration double-reset control passed 62/62 BPs (~0%
  false-negative rate of the state-match tolerance)"*. REFUTED AS STATED: D5
  was BP-manifest-fed and openlibrary's per-site manifest was never dumped
  after the 2400 s hard-timeout kill, silently dropping its 12 recorded c1/c2
  calibration pairs (5 PASS / 7 FAIL; `button_bucket` Z-drift,
  |Δn_elements| = 42 > tol 3). Corrected from raw calibration rows without
  consulting the manifest (`results/physics/wp006_fn_control_corrected.json`,
  generator `physics/fn_control_wp006_v2.py`): **corpus 67 pass / 74
  evaluated (90.5%), FN rate ≈ 9.46%; openlibrary 5/12; static core 48/48;
  saucedemo 7/7, parabank 5/5, internet 2/2**. (The audit-gate headline
  "62/74" reconciles to 67/74: its own per-site figures sum to 62+5=67 pass.)
  Related corrections: report §2/§3/§7 decomposition bounded accordingly;
  v1 verifier C2 covered only manifest BPs (868 of 910 trial rows,
  undisclosed) — v2 verifier reconstructs references from raw calibration
  rows and covers 888/910 with 0 mismatches (22 rows without PRE snapshot
  counted as not-recomputable), `results/physics/wp006_verification_v2.json`;
  the promised G5 chosen-descriptor↔pre-menu check is now actually
  implemented (875 rows checked, 0 violations). Primary verdict unchanged:
  **FALSIFIED** for H-ID at the director floors; openlibrary contributes 0
  verified BPs either way.

- **ADDENDUM (TEAM-PROPOSED WORDING, PENDING INDEPENDENT AUDIT AND DIRECTOR
  INTEGRATION — run 32860596387, 2026-08-25).** Additive only; every bullet
  above is preserved verbatim as provenance (the "pending independent
  audit" status line above is superseded by the certification facts below
  ONLY once the Lane Director integrates this snapshot). Certification
  chain since the entry was written: audit round 0 of run 32776372437 =
  REVISE RF1–RF5 (`results/audit/CYCLE_32776372437_PHYSICS_GATE.json`);
  repair round 1 (run 32793165981, `a00dc6a`) closed RF1–RF5 additively →
  audit round 1 = **PASS, safe_to_integrate=true, required_fixes=[]**
  (`results/audit/CYCLE_32793165981_PHYSICS_GATE.json`, measurement
  VALID_FOR_CURRENT_TEST); carryforward + fresh-environment reproduction +
  advisory A1/C10 closure via `results/physics/wp006_verification_v3.json`
  (run 32799587656, snapshot `45fa5db`) → audit round 2 = **PASS,
  safe_to_integrate=true, required_fixes=[]**
  (`reports/audit/CYCLE_32799587656_PHYSICS.md` +
  `results/audit/CYCLE_32799587656_PHYSICS_GATE.json`; dataset
  blob unchanged since `8d84196`). Run 32860596387 (stewardship, NO new
  collection): carried all 23 WP-006 scientific files bit-exact onto the
  accepted base (23/23 blob-identical); an INDEPENDENT stdlib-only team
  recheck importing no team module
  (`physics/team_recheck_wp006_run32860596387.py` →
  `results/physics/wp006_team_recheck_run32860596387.json`) reproduced
  every headline number exactly from raw rows (row accounting 1075=1+164+910;
  704/206 valid/invalid with identical exclusion ledger; verified BPs books
  12, quotes 12, saucedemo 7, parabank 5, internet 2 = 38 <60; producers
  {books,quotes}=2<4; FN control 67/74, openlibrary 5/12; T1/T2 rederivation
  0 mismatches on its explicit denominators; prereg-timing 0 rows pre-freeze;
  applied frozen mapping ⇒ FALSIFIED) and the UNMODIFIED frozen verifier
  rerun in the fresh environment returned PASS=true / own_verdict=FALSIFIED /
  verdict_agreement=true. Descriptive-only post-mortem
  (`results/physics/wp006_floor_postmortem_run32860596387.json`): the 24
  one-arm-zeroed branch points (wikipedia/gutenberg skip-link arms) are
  reproduced from raw rows; ARITHMETIC-ONLY sensitivity: had those arms been
  executable+valid at sibling rates, floor totals would read 62/60 and 4
  producer sites — a quantification of one declared slot rule's influence,
  NOT evidence for H-ID and NOT grounds for re-collection under the stop
  condition. Per the directive's pre-declared stop condition, H-ID
  FALSIFIED engages Physics lane TERMINATION at the Director step; the
  decision is the Lane Director's alone (see
  `reports/physics/wp006_stewardship_run32860596387.md`).

- **ADDENDUM 2 (TEAM-PROPOSED WORDING, PENDING INDEPENDENT AUDIT AND
  DIRECTOR INTEGRATION — run 32866107906, 2026-08-25).** Additive only;
  nothing above edited. Succession/recovery dispatch (same steering note;
  no positive-result demand inferred). Audit chain now FOUR gates: round 3
  on the run 32860596387 stewardship snapshot = **PASS,
  safe_to_integrate=true** (`reports/audit/CYCLE_32860596387_PHYSICS.md` +
  `results/audit/CYCLE_32860596387_PHYSICS_GATE.json`) — still not
  integrated by any Director; accepted base remained `d3afd9b`. This run:
  (i) carried all 26 WP-006 scientific files bit-exact onto the accepted
  lineage (22 core files blob-identical to certified snapshot `45fa5db`;
  4 stewardship files unique to 32860596387/team; ledger +112/−0);
  (ii) fresh-environment verification with ZERO environment interactions —
  dataset sha256 `fafd1cef…31149397` manifest-matched; committed recheck
  script rerun in a scratch tree reproduces BOTH its artifacts byte-identical;
  UNMODIFIED frozen verifier rerun returns PASS=true /
  own_verdict=FALSIFIED / verdict_agreement=true with key-level diffs vs
  stored artifacts exactly the two disclosed artifact-key/provenance-block
  differences; (iii) ONE new descriptive-only exhibit
  (`physics/terminal_bound_wp006_run32866107906.py` →
  `results/physics/wp006_terminal_bound_and_seam_run32866107906.json`,
  deterministic, no RNG): DATA_INSUFFICIENT negation row-cited (8≥6 sites,
  both classes, 38>0 verified BPs); tiered shortfall bounds — tier0
  measured 38 total / 2 producers; **tier1 ADMISSIBLE-imputation bound
  U_tot=50<60 and U_prod=3<4: both floors fail in EVERY admissible world**
  (credit only components with ≥1 committed success); tier2 descriptive
  upper bounds 62/4 and ≤82/≤5 stamped INADMISSIBLE-COMPONENT-INCLUDED,
  never evidence for H-ID; instrument-seam signature checks from raw rows —
  all 171 action_failed exclusions share ONE exception class (click
  actionability timeout; locators resolve then await visibility),
  `click_link#0` is 0-for-{84,84,21} on wikipedia/gutenberg/openlibrary vs
  217/217 successes elsewhere, and at ALL 24 affected BPs slot A runs 7/7
  valid while slot B runs 0/7 with ZERO state-match failures there ⇒
  restart/state reproducibility was perfect on those sites and the miss is
  a classifier×executor composability seam (hidden-anchor slots declared
  executable), i.e., stratum-level scope collapse (wikipedia/gutenberg
  UNKNOWN, not refuted), NOT a verdict flip; per-cell census: 130 cells,
  100 reach ≥6 valid replicates, all 30 sub-floor cells = the 24 dead arms
  plus cap-truncated openlibrary cells; dead-arm failure uniform across
  replicate positions (no ordering transient). Confirmatory extraction set
  of prereg aba6858 EXHAUSTED. Verdict inherited UNCHANGED: FALSIFIED at
  director floors, VALID_FOR_CURRENT_TEST ×4 audits; stop condition
  engaged; termination decision remains the Lane Director's alone (see
  `reports/physics/wp006_termination_package_run32866107906.md`).

- **ADDENDUM 3 (DIRECTOR ADOPTION — Lane Director integration, run
  32866107906 audit gate PASS, 2026-08-25).** Additive only; nothing above
  edited. The Lane Director integrated the audited snapshot
  `cycle/physics/32866107906/team` @ `38e697b` onto `lab/physics` by
  fast-forward (`f64848b` control-plane sync + `91eff06` bit-exact carry +
  `38e697b` verification/exhibit/package), then committed only Director-owned
  artifacts. Fifth independent gate on the WP-006 chain:
  **PASS, safe_to_integrate=true, required_fixes=[]**
  (`results/audit/CYCLE_32866107906_PHYSICS_GATE.json`; report
  `reports/audit/CYCLE_32866107906_PHYSICS.md` — adversarial recomputation
  from raw rows with auditor's own from-prereg implementation; every headline
  number reproduced; FALSIFIED confirmed as the unique frozen-mapping
  outcome). Audit report + gate JSON recorded into lane history per lane
  discipline.
  **DIRECTOR DECISION: the pre-declared program stop condition is ENGAGED —
  WP-006 H-ID FALSIFIED ⇒ the Physics lane TERMINATES;
  `state/physics_loop.json` set to `program_status=TERMINATE_LANE`,
  continue=false, no successor program.** Program
  `within-site-dynamics-interventional` closes COMPLETE-with-FALSIFIED-
  primary; WP-004 committor/barrier lineage closes BLOCKED-never-unlocked.
  Surviving audit objections answered: O1 (hardcoded `spans_both_classes`)
  → ACCEPTED_CLAIM_DOWNGRADED, exhibit remains descriptive and the computed
  adjacent field governs; O2 (tier-1 "admissible" label credits openlibrary
  beyond its demonstrated cells) → ACCEPTED_CLAIM_DOWNGRADED, the stricter
  reading U_tot=38/U_prod=2 is hereby the primary quoted bound (floors fail
  a fortiori; conclusion invariant either way); O3 (evidence-chain commits on
  historical refs, not carry ancestors) → ACCEPTED_AND_NOTED, provenance
  rests on verified blob identity + dataset hash per the previously-audited
  carryforward pattern. C6/C11 SURVIVES_AUDIT_WITH_LIMITS items adopted with
  their disclosed limits verbatim. Intel consultation before the decision
  (`lab/intel` @ `cc49ba3`): `docs/INTEL_TO_PHYSICS.md` routes NO mechanisms;
  the single validated mechanism file rates Physics relevance LOW (retrieval
  mechanics, not environment dynamics) — no audited Intel input addresses an
  accepted weakness falsifiably, and none can override an engaged stop
  condition. Product signal emitted downstream-only:
  `product-signals/physics/CYCLE_32866107906.json` (material=true, seam/
  instrument-lint lesson as validated operational limit; carries no physics
  or product-performance claim).

## WP-007 (2026-08-27, cycle 3, run 33109361290) — Transferable environment response magnitude, website holdout

- **Status: SURVIVES_CURRENT_TEST (technically) — SEVERELY CAVEATED NULL.**
  The literal frozen rule returns SURVIVES (Mean MSE(Full) 0.7347 < Mean MSE(Action-only) 0.7564 < Mean MSE(Persistence) 1.3213). However, the improvement (0.0217 MSE) is statistically insignificant (paired t-test p=0.43, Wilcoxon p=0.50, sign test 5/9 p=0.50), negligible effect size (Cohen's d = 0.07), outlier-driven (removing hackernews and saucedemo yields mean improvement −0.025), and action-semantics dominated (pre-state features add <3% additional variance explanation). Scientific interpretation: a clean, honestly-reported null. Under the 13-dim mechanics Z representation and uniform-random-walk sampling, environment response magnitude is dominated by action semantics; pre-state features add negligible, non-significant information. This is consistent with WP-005 (categorical next-state prediction does not transfer) and does not rescue or contradict WP-006.
- Preregistration frozen before data: `reports/physics/wp007_preregistration.md` (commit `e271ba9` 2026-08-27). Dataset is WP-005's `data/physics/wp005_transitions.jsonl.gz` (sha256 manifest `data/manifests/wp005_dataset_manifest.json`). No new data collection.
- Dataset `wp005_v1`: 875 atomic single-action transitions, 9 live sites; target y = L2 norm of state-change vector Δ = post_Z − pre_Z; 70.5% zero-change transitions.
- Models: Persistence (predict 0), Action-only (action-mean y), Pre-state-only (ridge on pre_Z), Full (action+pre-state ridge). Leave-one-site-out CV (9 folds).
- **Outcome (frozen rule trace)**: Mean MSE Persistence 1.3213, Action-only 0.7564, Pre-state-only 1.0660, Full 0.7347. Mean improvement (Action−Full) 0.0217 ± 0.3139. Paired t-test t=0.195, p=0.425 (one-sided); Wilcoxon W=23.0, p=0.50; Cohen's d=0.069; sign test 5/9 positive p=0.50. Per-fold improvement: 5/9 positive, 4/9 negative. Sensitivity: excluding hackernews+saucedemo yields mean improvement −0.025. Per-action: improvement concentrated in click_link (+0.385) and click_button (+0.362); fill actions have zero L2 norm by construction.
- Independent verification (`physics/verify_wp007.py`): own learner + own metric, bit-exact reproduction of all headline numbers; target recomputation 0 mismatches on 875 rows.
- Validity gates G1–G5 all passed. No measurement invalidity conditions.
- **Bounded lesson accepted**: Pre-state mechanics features contribute negligibly to predicting environment response magnitude beyond action semantics. The action-only model is nearly as good as the full model; the difference is not statistically significant. Future Physics work should use richer state representations, study different phenomena, or use different data.
- **Director integration**: Lane Director accepted the audited snapshot, annotated ledger headline as "literal-rule pass; scientific reading = null." Product signal emitted downstream-only: `product-signals/physics/CYCLE_33109361290.json` (material=false). Program status COMPLETE, lane DORMANT pending calibration-kit certification per CTO-9. No immediate successor core-lane program; CTO-9 defers new Physics families until calibration kit certifies.

## WP-005 (2026-08-24, cycle 2, run 32689298051) — Fine-grained response transfer, website holdout

- **Status: FALSIFIED — INDEPENDENTLY AUDITED (VALID_FOR_CURRENT_TEST),
  integrated into accepted lane state by the Physics Lane Director (cycle 2,
  run 32689298051).** Both co-primary fine-grained targets fail above all
  pre-declared strong nulls under true leave-one-site-out holdout.
  (The team commit `6963545` recorded this entry as "pending independent
  audit"; that pre-audit wording is preserved in team history and was
  upgraded here only after the PASS gate.)
- Preregistration frozen before data:
  `reports/physics/wp005_preregistration.md` in freeze commit `d81aee5`
  (2026-08-24T04:47:56Z), which also contains the collector v3 and the full
  frozen analysis + verifier code (cycle-1 provenance defect C6 not repeated;
  verified against git). Dataset commit `9e19461`; results commit `7c9b395`.
- Dataset `wp005_v1`: 875 collected / 769 confirmed ATOMIC single-action
  transitions, 9 live sites (7 from cycle 1 + NEW saucedemo, parabank),
  compact rows at `data/physics/wp005_transitions.jsonl.gz`
  (sha256 manifest: `data/manifests/wp005_dataset_manifest.json`).
- Targets (frozen pre-data): T1 URL-shape transition class
  (host × depth-delta × query-delta); T2 DOM-diff signature
  (digest-change × element-count delta bucket). Train-fold-only fitting of
  every fitted object; fixed structural Z one-hot; per-fold action vocab.
- **Outcome**: mean D(M_SA − best strong null): T1 −0.0432 (wins 1/9,
  randomization p=0.898); T2 −0.0497 (wins 4/9, p=0.270). ACTION-ONLY is
  best null on 3/9 folds each; NN memory wins most others; persistence-fine
  dominates where pages rarely change. M_SA>M_S paired on 7/9 T2 folds yet
  still not competitive cross-site.
- Methods gate 1 (P3 anomaly) resolved BEFORE this experiment:
  `physics/p3_bootstrap_diagnosis.py` +
  `results/physics/p3_bootstrap_diagnosis.json`. Diagnosis: nonlinear-
  statistic effect (class-composition lottery + recall-ratio re-weighting +
  max-selection at ~8 clusters); cycle-1 numbers reproduced bit-exact;
  bootstrap widths carry no inferential weight at this fold size — primary
  inference here was fold-level sign/randomization (as mandated).
- Independent verification (`results/physics/wp005_verification.json`):
  bit-exact D_f recomputation on all 18 target-folds via separate code path,
  independent target re-derivation PASS on 100% of rows, train-only action
  vocabularies verified, seed-formula integrity PASS, verdict arithmetic PASS.
- Bounded lesson (AUDITED, accepted in exactly this form): NO transferable
  action-conditioned environment regularity was detected at EITHER tested
  granularity (coarse R2, fine WP-005) under uniform random-walk sampling
  with these instruments; apparent predictability decomposes into structural
  persistence/diff inertia, site-local retrieval, and generic action-type
  semantics. This is a failure to detect above strong nulls at n=769 with a
  conservative frozen rule — not proof that web dynamics lack all structure.
- Per the Director's pre-declared horizon (`directives/PHYSICS.md`,
  `docs/NEXT_PHYSICS.md`): two-level negative reached → the lane stops on
  this instrument family unless a genuinely different measurement instrument
  (e.g., deliberate restart/matched-state designs) is proposed by the Lane
  Director.
- Descriptive robustness: excluding degenerate zero-information folds
  (saucedemo/wikipedia T1, all-equal accuracies) leaves wins 1/7 and 4/7 —
  verdict unchanged. Reported descriptively only; frozen rule untouched.

### Independent audit addendum (Physics Lane Director integration, 2026-08-24)

Audit: `reports/audit/CYCLE_32689298051_PHYSICS.md`; machine-readable gate:
`results/audit/CYCLE_32689298051_PHYSICS_GATE.json`. Overall: **PASS,
safe_to_integrate=true**, `required_fixes = []`.

- The auditor reran the UNMODIFIED frozen pipeline on the committed dataset:
  output identical bit-exact to `results/physics/wp005_results.json`
  (verdict FALSIFIED; T1 mean_D −0.0432 wins 1/9 p=0.897605; T2 −0.0497
  wins 4/9 p=0.269537). A fully independent from-scratch recomputation
  (different learner: standardized multinomial LR with bias, own targets,
  own metrics, own seed) reproduced both FALSIFIED verdicts (T1 mean_D
  −0.0312 wins 3/9; T2 −0.0474 wins 2/9): the negative does not depend on
  the team's optimizer or metric implementation.
- Director spot-checks at integration time independently confirmed: gz and
  uncompressed dataset sha256 match the manifest exactly; all 875 row
  timestamps postdate freeze commit `d81aee5` (range [04:52:14, 05:20:11]
  UTC vs freeze 04:47:56Z); stored T1/T2 labels re-derive from raw
  pre/post observables with 0 mismatches on all 875 rows; chain_len==1 +
  primary==target atomicity holds on all 769 confirmed rows; per-site
  confirmed counts recomputed from raw rows match the results JSON;
  frozen-rule trace R1–R4 → FALSIFIED/FALSIFIED reproduces from stored
  per-fold artifacts.
- All nine claim statuses VALIDATED_FOR_CURRENT_TEST (dataset integrity,
  prereg timing/provenance, target construction G9, split/train-only
  integrity, headline arithmetic, uncertainty level + P3 resolution, null
  strength/policy confounding, S10 honesty, stop-rule invocation/bounded
  wording).
- Audit limitations recorded (non-blocking), Director dispositions:
  - **L1** — team verifier re-derives targets independently but imports
    learner/metric helpers from analysis modules. ACCEPTED_AND_FIXED going
    forward: future verifiers must implement their own learner+metric
    reference path (binding in `directives/AUDITOR_PHYSICS.md` and
    `directives/PHYSICS.md` methods gates). This cycle is covered by the
    auditor's fully independent recomputation.
  - **L2** — report §2 prose says "(gutenberg 0.90, others 1.00)" but
    openlibrary T1 coverage is 0.97 in artifacts. ACCEPTED_AND_FIXED via an
    appended erratum note in the report file (artifacts were always
    correct; prose digit corrected without rewriting history).
  - **C2 standing caveat** — "no dataset existed at freeze time" is not
    provable from git alone. REJECTED_WITH_EVIDENCE as a blocking concern:
    git absence + all-row timestamp ordering + disclosed goto-only smoke
    tests/synthetic dry-run is the strongest available provenance; the
    negative verdict does not depend on it. Caveat stands on record.
  - **L3 power bound (ACCEPTED_CLAIM_DOWNGRADED)** — small folds
    (hackernews 25 / internet 27 / openlibrary 36 confirmed) and n=769
    overall limit sensitivity; the accepted wording is therefore "no
    detectable transferable signal above strong nulls at this sample size
    under this instrument", never "absence of structure".

## WP-003B-R2 (2026-08-24, cycle 1, run 32676578274) — Action-conditioned next-state structure, website holdout

- **Status: FALSIFIED — INDEPENDENTLY AUDITED (VALIDATED_FOR_CURRENT_TEST),
  integrated into accepted lane state by the Physics Lane Director
  (cycle 1, run 32676578274).**
- Preregistration frozen before data:
  `reports/physics/wp003b_r2_preregistration.md` (commit `9dc895d`, ahead of
  the collection commits).
- Dataset `wp003b_r2_v1`: 681 collected / 564 confirmed transitions,
  7 live sites, corrected collector v2 (deterministic trajectory_id/step_id,
  true prev-action alignment, sha256 site seed offsets), compact rows
  committed at `data/physics/wp003b_r2_transitions.jsonl.gz`
  (sha256 in `data/manifests/wp003b_r2_dataset_manifest.json`).
- Primary target: coarse structural class of s_{t+1} from (Z(s_t), a_t),
  leave-one-site-out, trajectory-grouped bootstrap.
- **Outcome**: mean D(M_SA − best null) = −0.5016; grouped-bootstrap 95% CI
  [−0.6467, −0.3153]; 0/5 adequate folds positive → **FALSIFIED** for this
  representation family.
- The structural persistence null won every adequate fold (wikipedia 0.897,
  openlibrary 0.913 macro balanced accuracy). In-distribution diagnostic:
  signal exists but is persistence + nearest-neighbour memorization;
  action-conditioning adds ~0 even in-site.
- Descriptive: gutenberg's next-state classes are unique to it in-corpus
  (coverage-0 fold); hackernews walks terminate early on logged-out vote
  pages (real environment response).
- Self-audit disclosures: metric-class-values defect found and corrected
  pre-acceptance (verdict unchanged, Δmean +0.0033); v1 instrument replaced
  by retry-hardened v2 with full recollection before any outcome existed.
- Independent verification artifacts:
  `results/physics/wp003b_r2_verification.json`; report:
  `reports/physics/wp003b_r2_report.md`.
- **Bounded lesson accepted into working knowledge (subject to audit):**
  coarse structural environment response does not transfer across websites;
  it decomposes into structural persistence plus site-local retrieval.
  WP-002B's "memory ≥ rules" now holds under true website holdout.

### Independent audit addendum (Physics Lane Director integration, 2026-08-24)

Audit: `reports/audit/CYCLE_32676578274_PHYSICS.md`; machine-readable
findings: `results/audit/CYCLE_32676578274_PHYSICS_findings.json`.
Overall audit status: **VALIDATED_FOR_CURRENT_TEST**, safe to integrate.

- The auditor performed a full independent recomputation from the committed
  dataset with a from-scratch implementation (no team analysis code):
  mean D = −0.5016, grouped-bootstrap CI [−0.6467, −0.3153], fold wins 0/5,
  verdict FALSIFIED — all reproduced bit-exact. Director spot-checks
  independently confirmed dataset hashes, per-site counts, trajectory
  alignment (0 violations on 681 rows), the prev==target guard rate (0.541),
  and the training-free persistence null on all five adequate folds.
- Accepted into working knowledge, in exactly this bounded form: at the
  frozen 13-dim mechanics representation Z × this action encoding × coarse
  structural target, next-state structure does NOT transfer across these
  seven websites beyond structural persistence plus site-local
  memorization. This says nothing about finer-grained targets or richer
  state variables.
- Process caveats recorded by the auditor (do not affect this negative
  verdict; binding on future cycles):
  1. C5 — post-hoc metric correction implemented the frozen spec and is
     verdict-invariant, but pre-correction artifacts were overwritten.
     Future corrections must preserve pre-fix artifacts or their recomputed
     hashes.
  2. C6 — prereg §11 states analysis code was committed in the freeze
     commit; that sentence is FALSE (analysis code first appeared ~30 min
     later in `4dae86c` together with collector hardening). Design/rules
     verifiably froze before data; confirmatory status stands. Recorded
     here as an annotation, not fixed by silently editing the prereg file.
  3. C7 — team's P3 probe anomaly (grouped CI width < naive row-bootstrap
     width on books fold) remains unresolved; no conclusion from this cycle
     depended on it. Must be settled before any future cycle relies on
     bootstrap CI widths.
  4. C3 note — pooled action-vocabulary encoding was mildly transductive;
     immaterial for a negative result but forbidden for future positive
     claims (train-fold-only fitting mandatory).
  5. C8 note — N_MAJ is degenerate under macro balanced accuracy; keep it
     reported but never describe it as a strong null.

## WP-004 gate

Committor/barrier work remains **BLOCKED pending identifiability**. Passive-walk
revisit diagnostics from WP-003B-R2 (`identifiability_gate_diagnostics_...`
in the results JSON) show only small numbers of revisited comparable states
with branching outcomes (max ~6–8 per site). These do NOT satisfy the gate.
A deliberate restart/revisit collection design would be required.

## WP-003 (2026-08-23) — Website-holdout transition structure

- **Original hypothesis**: mechanics-only state features Z transfer across
  websites for predicting next-action-class beyond strong nulls.
- **Historical dataset**: 557 transitions, 7 live sites.
- **Original reported verdict**: `FALSIFIED`.
- **POST-RUN AUDIT VERDICT: `MEASUREMENT_INVALID`.**

### Fatal defects found

1. `prev_action_label` was assigned from the current transition's final action,
   while `target_action` was the current transition's first action. For the
   dominant one-action transitions the Markov baseline therefore received the
   target itself.
2. The reported confidence interval was not a nonparametric paired bootstrap;
   the code added Gaussian noise to fold-level point estimates.
3. The supposedly frozen random seed used Python `hash(site)`, which is salted
   across fresh processes and therefore not reproducible.

### Consequence

The historical Δ=-0.348, 0/7 fold result and "universal last-action→next-action"
claim are retained only as invalidated provenance. They provide **no evidence
for or against Web Physics**.

### Corrected infrastructure now present

- deterministic site seed offsets;
- independent `trajectory_id` and `step_id`;
- true `prev_action_label = action(t-1)`;
- hard pre-analysis anti-leak assertions;
- trajectory-grouped bootstrap;
- corrected WP-003B family conditioned on `(s_t, a_t)` to predict coarse
  `s_{t+1}` structure.

These corrections require a **new dataset and new result files**. Historical
JSON files are never silently overwritten.

## WP-004 gate

Committor/barrier work is **BLOCKED pending identifiability**. Before estimating
`q(s)=P(reach B before A | s)`, Team Physics must show enough independent
restarts/revisits/branching from comparable states and a null separating a
dynamical barrier from a graph bottleneck. Failure of this gate yields
`DATA_INSUFFICIENT`, not a physics result.

## Prior carried from earlier program

- Mind2Web reconstruction: operation inventory != causal mechanics.
- WP-001: ~+0.05 dimension-accuracy over shuffle, but post-state proxy was not
  a verified next state.
- WP-002B: true `(S,A,S')`; rule ~ NN > shuffle in-distribution; no website
  holdout claim.

WP-003 does not supersede WP-002B because WP-003's historical measurement is
invalid.
