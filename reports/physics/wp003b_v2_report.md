# WP-003B-v2 REPORT — Action-Conditioned Next-State Structure Under Website Holdout

Cycle 32670239235, TEAM PHYSICS, 2026-08-23.
Preregistration: `reports/physics/wp003b_v2_preregistration.md`, frozen at
commit `81c46a6` **before** any data collection and before any outcome was
observed. Analysis code and measurement-validity tests were committed in the
same freeze.

## Headline verdicts (exactly as preregistered)

| Arm | Status | Result |
|---|---|---|
| **Primary**: additive mechanics model → next-state signature, website holdout | **INCONCLUSIVE** | mean Δ = −0.0368 vs best null; wins 2/6; trajectory-grouped CI95 [−0.0850, +0.0345] |
| Exploratory S-E: interaction-augmented model (A×Z crossings) | SURVIVES_CURRENT_TEST **(exploratory only)** | mean Δ = +0.1683; wins 3/6; CI95 [+0.1117, +0.2272] |
| Representation ablation S-B (alternate thresholds) | FALSIFIED (for the additive family) | mean Δ = −0.1242; wins 1/6; CI95 [−0.1645, −0.0341] |
| Component targets S-A (link / form / inputs / password) | no signal | Δ = −0.106 / −0.101 / −0.137 / 0.000 |
| WP-004 identifiability gate S-C | **FAILED** → WP-004 stays BLOCKED | G1=29 (<50), G2=11 (<20); DATA_INSUFFICIENT for committor feasibility |
| Control E-1 (EXPLORATORY, post-hoc labeled): within-site action permutation on the S-E arm | effect **collapses** | Δ +0.168 → −0.0459; CI95 [−0.0952, +0.0121] |

Per master §20 the primary status is INCONCLUSIVE, not FALSIFIED: the paired
effect is slightly negative but its interval includes zero. What IS cleanly
established:

1. **No additive cross-site mechanical structure**: the preregistered linear
   model never beats strong nulls on any adequate fold consistently
   (best folds: wikipedia +0.204, hackernews +0.025; worst: gutenberg −0.340).
   Component targets agree (all ≤ 0). The representation-ablation arm, which
   changes only bucketing thresholds, flips to a clean negative.
2. **Conjunctive structure is where the signal lives (exploratory)**: adding
   action×state crossing features to the SAME model class, SAME target, SAME
   folds moves the effect from −0.037 to +0.168 with CI strictly above 0,
   driven by hackernews (+0.749), wikipedia (+0.246) and gutenberg (+0.145,
   also beating the NN memory baseline there). Under prereg §9 this cannot
   rescue or overturn the primary verdict; it is a POC-level observation that
   demands a new confirmatory preregistration on fresh data.
   The post-hoc control E-1 (exploratory) strengthens the interpretation:
   permuting the imposed action within each site — preserving state rows,
   action marginals and outcomes, destroying only action→outcome pairing —
   collapses the effect back to −0.046. The exploratory survival therefore
   depends on REAL action-conditioning, not on state marginals wearing an
   action costume; this is consistent with transferable environment-response
   structure of the form P(s′ | s, a) with conjunctive (state×action)
   character, and inconsistent with a pure state-persistence artifact.
3. **WP-004 remains blocked**: only 29 state-groups have ≥3 independent
   visits and 11 of those show ≥2 actions × ≥2 outcomes. A committor is not
   identifiable from random-walk corpora of this kind. Verdict:
   DATA_INSUFFICIENT for committor feasibility.

## Data and integrity

Corpus `wp003b_v2_transitions.jsonl`: 548 raw rows → 504 usable after the
frozen exclusion (operationalized per deviation D2), 80 trajectories, 6 sites
(openlibrary refused connections repeatedly — abandoned per D4). Full
provenance incl. seed batches and sha256 in
`data/manifests/wp003b_v2_dataset_manifest.json`.

Integrity evidence committed during this cycle:

- corpus verification recomputed EVERY row's derived features, raw counts and
  digest names from preserved raw DOM snapshots: 0 mismatches;
  trajectory chaining exact (`results/physics/wp003b_v2_corpus_verification.json`);
- seed mechanism verified process-stable under randomized PYTHONHASHSEED
  (unit test, the exact WP-003 defect);
- protocol sensitivity verified pre-freeze on synthetic corpora: planted
  linear channel detected, pure noise not survived (the first draft's parity
  channel correctly could NOT be fitted by the frozen linear model — episode
  documented in prereg §10);
- determinism: full analysis reruns are byte-identical;
- independent reproduction: an out-of-pipeline reimplementation with different
  optimizer settings reproduced the strongest fold exactly (M=0.8411 vs 0.841);
  NN differs only by tie-breaking on duplicate feature vectors (0.026 vs 0.013);
- internal consistency: macro-recalls and d_effects recompute from stored
  per-class blocks across all result files: no violations;
- uncertainty: real trajectory-grouped bootstrap (2000 replicates, within-site
  resampling of whole trajectories); no jittered point estimates anywhere;
- provenance: all result JSONs record `git_commit_at_analysis = 81c46a6`
  (the freeze commit). Post-freeze code touches, all verifiable in git and
  none affecting model/target/null/verdict definitions: (1) loader reordered
  to run integrity assertions BEFORE exclusions after it crashed on a gap
  created by an excluded failed-action row — no result had been produced;
  (2) ablation-arm target wiring fixed after a KeyError crash — no result had
  been produced; (3) `skip_chaining` flag added solely for counterfactual
  control corpora; (4) S0 calibration and E-1 permutation-control scripts
  added (descriptive/exploratory by construction).

## Limitations

- One live-web sample; sites are heterogeneous in trajectory counts (6–30)
  and two needed second seed batches (D3).
- HN sub-corpus uses many-short-trajectory sampling (D1) — same policy,
  different walk-length distribution.
- Multi-chain rows whose LATER step failed are retained (D2 limitation).
- Balanced accuracy over 6 a-priori signature classes; rare classes (e.g.
  password-bearing pages) have wide recall intervals.
- The exploratory interaction result is one preregistered arm among several;
  multiplicity argues for treating it as hypothesis-generating until
  replicated under a new preregistration with interactions as the primary
  model.

## Recommended next discriminating test (for LAB DIRECTOR)

New preregistration, new collection: primary model = interaction-augmented
linear softmax (the S-E specification), same target family, ≥8 sites with
site holdout, plus a permuted-action control (shuffle a_t labels within site:
if the effect survives, it is state-only structure mislabeled as dynamics).
This directly tests whether "which action was imposed" carries transferable
information about environment response — the sharpest current candidate for
mechanical Web physics beyond memory and similarity.
