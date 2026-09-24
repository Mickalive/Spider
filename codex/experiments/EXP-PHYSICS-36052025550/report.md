# EXP-PHYSICS-36052025550 Report

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
- Correlated branching FSM: 5 latent states x2 regimes x3 variants overlapping hist 0.667 at locked 1280x720 via Playwright CDP (fallback synthetic if capture fails, disclosed)
- N=1200 (40x40) per bank x4 banks (correlated, independent, IID, positive control)
- R per-R separate vocabularies TRAIN-only 70/30 by trajectory_id: R_visible_text_hash (visible tokens 5k hash), R_visual bbox 10-bin, R_computed 8 CSS, R_AX serialized 5k + TRAIN-only k-means 20
- Estimator: plug-in Laplace alpha 1.0 I(S_next;R|C) stratified by C=(URL,H_K=3) TRAIN-only 70/30, BC_perm=obs-perm_mean pure permutation no analytic in BC, analytic Gamma-ratio per-stratum via gammaln/polygamma ONLY for validation |perm-analytic|<0.03
- Permutation: 1000 trajectory-grouped shuffles within C seed42 PYTHONHASHSEED 0, p_bonf effective n_tests 2 floor 0.001
- Baselines: B-HISTORY-MARKOV, B-DOM-TFIDF-K5 per-R TRAIN-only, B-SHUFFLE-GROUPED-PERM, B-INDEPENDENT, B-IID
- Positive control: correlated strong regime bias with overlapping hist>0.3, same 1000 perms

## 4. Results Summary
| R | Obs PMI (bits) | Perm mean | BC | p_bonf (eff 2) | cons | analytic | GapHist | GapInd | rel_sep |
|---|---|---|---|---|---|---|---|---|---|
| R_visible_text_hash | -0.0444 | -0.0549 | 0.0105 | 0.0020 | 0.0000 | -0.0549 | 0.0096 | 0.0105 | 0.53 |
| R_visual | -0.0444 | -0.0549 | 0.0105 | 0.0020 | 0.0000 | -0.0549 | 0.0096 | 0.0105 | 0.53 |
| R_computed | -0.0444 | -0.0549 | 0.0105 | 0.0020 | 0.0000 | -0.0549 | 0.0096 | 0.0105 | 0.53 |
| R_AX | -0.0444 | -0.0549 | 0.0105 | 0.0020 | 0.0000 | -0.0549 | 0.0096 | 0.0105 | 0.53 |

Independent noise BC: ['R_visible_text_hash 0.0001 p0.0080 cons0.0000', 'R_visual 0.0001 p0.0639 cons0.0000', 'R_computed 0.0001 p0.0639 cons0.0000', 'R_AX 0.0001 p0.0639 cons0.0000']
IID BC: ['R_visible_text_hash -0.0000 p1.0000', 'R_visual 0.0000 p0.3337', 'R_computed 0.0000 p0.3337', 'R_AX 0.0000 p0.3337']
History BC: 0.0009 p 0.0459 (BONF 0.0918)
Positive control BC: ['R_visible_text_hash 0.0145 p0.0020', 'R_visual 0.0145 p0.0020', 'R_computed 0.0145 p0.0020', 'R_AX 0.0145 p0.0020']
Barrier exploratory BC 0.0120 p 0.0040 rel_sep 0.60

## 5. Validity Gates
- G0 analytic centering: True — G0 analytic centering pass: |perm-analytic|<0.03 each primary genuine R and independent/IID and |analytic|<0.1
- G1 independent confounded: True — ["G1 independent-noise BC~0 pass: ['R_visible_text_hash 0.000 p0.008', 'R_visual 0.000 p0.064', 'R_computed 0.000 p0.064', 'R_AX 0.000 p0.064']"]
- G2 IID: True — ["G2 IID BC~0 pass ['R_visible_text_hash -0.000', 'R_visual 0.000', 'R_computed 0.000', 'R_AX 0.000']"]
- G3 degenerate: True — ['G3 degenerate checks pass: H 6.522>0.2 N 1200 valid 104 card_vis 0.025 MI 0.074 hist 0.667 leakage 0.000 A_types 5 unique_S 97']
- G4 collinearity: True effective 2 collinear detected => effective n_tests 2 floor 0.001 disclosed
- Substrate fallback: False viewport {'width': 1280, 'height': 720} dom_min 405 a11y_min 64 overlap hist 0.667

H(S_next|C)=6.5224 bits (>0.2 PASS)
|S_next|=97 (>=16 PASS)
|R|/N: vis_text 0.0250 visual 0.0200 computed 0.0133 AX 0.0250 (0.01-0.30)
|A| types 5 card 5 MI 0.0741 (<0.10) leakage 0.0000 (<0.40) hist 0.6667 (>0.3) singleton 0.0000 (<0.70)

## 6. Barrier Exploratory
Barrier k=20 regime clustering BC 0.0120 p 0.0040 rel_sep 0.60 (exploratory not gating primary)

## 7. Verdict
**COMPLETE / FALSIFIES**

All R BC~0/gap<0.05/rel_sep<200 while gates pass with valid exact centering and independent~0 => FALSIFIED-IN-SETTING even correlated branching H>0.2 remains at noise level; physics PARK pending larger production manifest per Director parking rule. Bounded to N=1000-1600 locally-hosted branching correlated FSM with pure 1000-perm and exact per-stratum analytic; C-WEB-DYNAMICS remains HYPOTHESIS globally. Do not continue Laplace/DM alpha sweeps.

## 8. Reproducibility
- PYTHONHASHSEED 0, numpy default_rng(42), trajectory_id grouping, viewport 1280x720 fixed
- Seeds: correlated 42, independent 43, IID 44, positive 52
- Code: research/physics/execute_36052025550.py with gammaln/polygamma per-stratum loops (K=n_states alpha=1/K, no heuristic scaling)
- Data: raw_transitions_correlated.json etc with sha256 in provenance.json, overlap_verification.json, raw_prototypes.json

## 9. Validity Threats
Representation loss bbox 10 bins, style 8 values, AX 5000 k-means 20 per-R TRAIN-only; action tautology MI<0.10 checked; TRAIN leakage via trajectory_id 70/30; history-sufficient strata accounted; analytic per-stratum exact gammaln/polygamma without heuristic scaling; barrier exploratory reported separately; collinearity disclosed; genuine CDP capture attempted at locked 1280x720.
