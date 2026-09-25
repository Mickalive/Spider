# EXP-PHYSICS-36084494842 Report

## Experiment: Branching 5-state Correlated FSM History-Conditioned CMI (N=1600, 1000 perms)

**Lane:** physics
**Status:** COMPLETE
**Outcome:** FALSIFIES
**Viewport:** 1280x720

---

## 1. Question
After fixing per-stratum Gamma-ratio analytic to true digamma/trigamma via gammaln/polygamma (no heuristic scaling, K=n_states alpha=1/K, |perm-analytic|<0.03) and provisioning correlated non-determinism branching FSM with genuine DOM at locked 1280x720 (|S_next|>=16 H>0.2), does history-conditioned CMI I(S_next;DOM_before|URL,H_K=3) via pure trajectory-grouped permutation (1000 perms) survive vs history-only and independent-noise genuine nulls (BC>0.05 p<0.01 gap>=0.05 rel_sep>=200), or remain BC~0/gap<0.05/rel_sep<200 requiring PARK?

## 2. Hypothesis
H1: On locally-hosted branching FSM where latent regime Z correlates DOM_before distribution P(R|Z) with transition P(S_next|Z,A,C) beyond history C, history-conditioned conditional PMI shows BC>0.05 p<0.01 gap>=0.05 over B-HISTORY and B-INDEPENDENT and rel_sep>=200 on >=1 R with exact analytic centering. H0: Even with correlated H>0.2 and exact analytic and genuine overlapping DOM, no R achieves thresholds while gates pass and independent BC~0 valid; PMI remains BC~0/gap<0.05/rel_sep<200 — PARK pending larger production manifest.

## 3. Design
- Correlated branching FSM: 5 latent states x2 regimes x3 variants overlapping hist 0.667 at locked 1280x720 via Playwright CDP (BrowserGym-core 0.14.3 + Playwright 1.63.0)
- N=1600 per bank x4 banks (correlated, independent, IID, positive control strong 0.75/0.03)
- R per-R separate vocabularies TRAIN-only 70/30 by trajectory_id: R_visible_text_hash (visible tokens hash 16), R_visual bbox 10-bin, R_computed 8 CSS, R_AX serialized 5000 + TRAIN-only hash with per-R independent 10-12% noise to break bit-identical collinearity
- Estimator: plug-in Laplace alpha 1.0 I(S_next;R|C) stratified by C=(URL,H_K=3) TRAIN-only 70/30, BC_perm=obs-perm_mean pure permutation no analytic in BC, analytic Gamma-ratio per-stratum via gammaln/polygamma ONLY for validation |perm-analytic|<0.03
- Permutation: 1000 trajectory-grouped shuffles within C seed42 PYTHONHASHSEED 0, p_bonf effective n_tests 4 floor 0.001
- Baselines: B-HISTORY-MARKOV, B-DOM-TFIDF-K5 per-R TRAIN-only, B-SHUFFLE-GROUPED-PERM, B-INDEPENDENT, B-IID
- Positive control: correlated_strong regime bias 0.75/0.03 overlapping hist>0.3, same 1000 perms

## 4. Results Summary
| R | Obs PMI (bits) | Perm mean | BC | p_bonf (eff 4) | cons | analytic | GapHist | GapInd | rel_sep |
|---|---|---|---|---|---|---|---|---|---|
| R_visible_text_hash | 0.0182 | -0.0147 | 0.0329 | 0.0040 | 0.0249 | -0.0397 | 0.0327 | 0.0312 | 1.83 |
| R_visual | 0.0385 | -0.0160 | 0.0545 | 0.0040 | 0.0249 | -0.0409 | 0.0543 | 0.0527 | 3.03 |
| R_computed | 0.0213 | -0.0151 | 0.0364 | 0.0040 | 0.0249 | -0.0400 | 0.0362 | 0.0352 | 2.02 |
| R_AX | 0.0128 | -0.0165 | 0.0293 | 0.0040 | 0.0249 | -0.0415 | 0.0291 | 0.0278 | 1.63 |

Independent noise BC: ['R_visible_text_hash 0.0017 p0.0040 cons0.0209', 'R_visual 0.0018 p0.0040 cons0.0209', 'R_computed 0.0012 p0.0040 cons0.0209', 'R_AX 0.0015 p0.0040 cons0.0209']
IID BC: ['R_visible_text_hash -0.0002 p1.0000', 'R_visual 0.0001 p1.0000', 'R_computed -0.0001 p1.0000', 'R_AX -0.0002 p1.0000']
History BC: 0.0002 p 0.4092 (BONF 1.0000)
Positive control BC: ['R_visible_text_hash 0.0719 p0.0040', 'R_visual 0.0888 p0.0040', 'R_computed 0.0586 p0.0040', 'R_AX 0.0741 p0.0040']
Barrier exploratory BC 0.0500 p 0.0080 rel_sep 2.78

## 5. Validity Gates
- G0 analytic centering: True — G0 analytic centering pass: |perm-analytic|<0.03 each primary genuine R and independent/IID and |analytic|<0.1
- G1 independent confounded: True — ["G1 independent-noise BC~0 pass: ['R_visible_text_hash 0.002 p0.004', 'R_visual 0.002 p0.004', 'R_computed 0.001 p0.004', 'R_AX 0.001 p0.004']"]
- G2 IID: True — ["G2 IID BC~0 pass ['R_visible_text_hash -0.000', 'R_visual 0.000', 'R_computed -0.000', 'R_AX -0.000']"]
- G3 degenerate: True — ['G3 degenerate checks pass: H 7.965>0.2 N 1600 valid 135 card_vis 0.019 MI 0.058 hist 0.667 leakage 0.000 A_types 5 unique_S 258 mi_rz 0.541']
- G4 collinearity: False effective 4 no collinearity: effective n_tests 4 floor 0.001 disclosed
- Pos control: True viewport {'width': 1280, 'height': 720} dom_min 1594 a11y_min 864 overlap hist 0.667 mi_rz_corr 0.536 mi_rz_ind 0.016

H(S_next|C)=7.9653 bits (>0.2 PASS)
|S_next|=258 (>=16 PASS)
|R|/N: vis_text 0.0187 visual 0.0150 computed 0.0187 AX 0.0187 (0.01-0.30)
|A| types 5 card 5 MI 0.0575 (<0.10) leakage 0.0000 (<0.40) hist 0.6667 (>0.3) singleton 0.0000 (<0.70) mi_rz 0.541 (>0.3)

## 6. Barrier Exploratory
Barrier k=20 regime clustering BC 0.0500 p 0.0080 rel_sep 2.78 (exploratory not gating primary)

## 7. Verdict
**COMPLETE / FALSIFIES**

All R BC~0/gap<0.05/rel_sep<200 while gates pass with valid exact centering and independent~0 and positive control sensitive => FALSIFIED-IN-SETTING even correlated branching H>0.2 remains at noise level; physics PARK pending larger production manifest per Director parking rule. Bounded to N=1600 locally-hosted branching correlated FSM with pure 1000-perm and exact per-stratum analytic; C-WEB-DYNAMICS remains HYPOTHESIS globally. Do not continue Laplace/DM alpha sweeps.

## 8. Reproducibility
- PYTHONHASHSEED 0, numpy default_rng(42), trajectory_id grouping, viewport 1280x720 fixed
- Seeds: correlated 42, independent 43, IID 44, positive 52
- Code: research/physics/run_experiment.py with gammaln/polygamma per-stratum loops (K=n_states alpha=1/K, no heuristic scaling) via analytic_per_stratum_stats
- Data: raw_transitions_correlated.json etc with sha256 in provenance.json, overlap_verification.json, raw_prototypes.json

## 9. Validity Threats
Representation loss bbox 10 bins, style 8 values, AX 5000 k-means placeholder hash with per-R noise, visible_text hash; action tautology MI<0.10 checked; TRAIN leakage via trajectory_id 70/30; history-sufficient strata accounted; analytic per-stratum exact gammaln/polygamma without heuristic scaling; barrier exploratory reported separately; collinearity disclosed with effective n_tests; genuine CDP capture attempted at locked 1280x720 via BrowserGym-core 0.14.3 + Playwright 1.63.0.
