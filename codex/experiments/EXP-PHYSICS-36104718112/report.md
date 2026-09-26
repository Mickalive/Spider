# EXP-PHYSICS-36104718112 Report

## Experiment: Branching 5-state Correlated FSM History-Conditioned CMI (N=1600, 1000 perms)

**Lane:** physics
**Status:** MEASUREMENT_INVALID
**Outcome:** NOT_APPLICABLE
**Viewport:** 1280x720

---

## 1. Question
After fixing per-stratum Gamma-ratio analytic to true digamma/trigamma via gammaln/polygamma (no heuristic scaling, K=n_states alpha=1/K, |perm-analytic|<0.03) and provisioning correlated non-determinism branching FSM with genuine DOM at locked 1280x720 (|S_next|>=16 H>0.2), does history-conditioned CMI I(S_next;DOM_before|URL,H_K=3) via pure trajectory-grouped permutation (1000 perms) survive vs history-only and independent-noise genuine nulls (BC>0.05 p<0.01 gap>=0.05 rel_sep>=200), or remain BC~0/gap<0.05/rel_sep<200 requiring PARK?

## 2. Hypothesis
H1: On locally-hosted branching FSM where latent regime Z correlates DOM_before distribution P(R|Z) with transition P(S_next|Z,A,C) beyond history C, history-conditioned conditional PMI shows BC>0.05 p<0.01 gap>=0.05 over B-HISTORY and B-INDEPENDENT and rel_sep>=200 on >=1 R with exact analytic centering. H0: Even with correlated H>0.2 and exact analytic and genuine overlapping DOM, no R achieves thresholds while gates pass and independent BC~0 valid; PMI remains BC~0/gap<0.05/rel_sep<200 — PARK pending larger production manifest.

## 3. Design
- Correlated branching FSM: 5 latent states x2 regimes x3 variants overlapping hist 1.000 at locked 1280x720 via Playwright CDP (BrowserGym-core 0.14.3 + Playwright 1.63.0)
- N=1600 per bank x4 banks (correlated, independent, IID, positive control strong 0.75/0.03)
- R per-R separate vocabularies TRAIN-only 70/30 by trajectory_id: R_visible_text_hash (visible tokens hash 16), R_visual bbox 10-bin, R_computed 8 CSS, R_AX serialized 5000 + TRAIN-only hash with per-R independent 10-12% noise to break bit-identical collinearity
- Estimator: plug-in Laplace alpha 1.0 I(S_next;R|C) stratified by C=(URL,H_K=3) TRAIN-only 70/30, BC_perm=obs-perm_mean pure permutation no analytic in BC, analytic Gamma-ratio per-stratum via gammaln/polygamma ONLY for validation |perm-analytic|<0.03
- Permutation: 1000 trajectory-grouped shuffles within C seed42 PYTHONHASHSEED 0, p_bonf effective n_tests 4 floor 0.001
- Baselines: B-HISTORY-MARKOV, B-DOM-TFIDF-K5 per-R TRAIN-only, B-SHUFFLE-GROUPED-PERM, B-INDEPENDENT, B-IID
- Positive control: correlated_strong regime bias 0.75/0.03 overlapping hist>0.3, same 1000 perms

## 4. Results Summary
| R | Obs PMI (bits) | Perm mean | BC | p_bonf (eff 4) | cons | analytic | GapHist | GapInd | rel_sep |
|---|---|---|---|---|---|---|---|---|---|
| R_visible_text_hash | -0.0994 | -0.1307 | 0.0314 | 0.0040 | 2.9048 | -3.0355 | 0.0307 | 0.0291 | 0.03 |
| R_visual | -0.0128 | -0.1004 | 0.0875 | 0.0040 | 2.9351 | -3.0355 | 0.0868 | 0.0822 | 0.07 |
| R_computed | -0.0981 | -0.1318 | 0.0337 | 0.0040 | 2.9037 | -3.0355 | 0.0330 | 0.0316 | 0.03 |
| R_AX | -0.1053 | -0.1348 | 0.0295 | 0.0040 | 2.9008 | -3.0355 | 0.0288 | 0.0273 | 0.02 |

Independent noise BC: ['R_visible_text_hash 0.0023 p0.0040 cons3.1334', 'R_visual 0.0054 p0.0040 cons3.1496', 'R_computed 0.0022 p0.0040 cons3.1327', 'R_AX 0.0022 p0.0040 cons3.1336']
IID BC: ['R_visible_text_hash 0.0004 p0.8911', 'R_visual 0.0006 p0.7512', 'R_computed 0.0003 p1.0000', 'R_AX 0.0002 p1.0000']
History BC: 0.0007 p 0.3493 (BONF 1.0000)
Positive control BC: ['R_visible_text_hash 0.0653 p0.0040', 'R_visual 0.1111 p0.0040', 'R_computed 0.0523 p0.0040', 'R_AX 0.0690 p0.0040']
Barrier exploratory BC 0.0000 p 1.0000 rel_sep 0.00

## 5. Validity Gates
- G0 analytic centering: False — R_visible_text_hash corr cons 2.9048>=0.03; R_visible_text_hash corr |analytic| -3.0355>=0.1; R_visible_text_hash ind cons 3.1334>=0.03; R_visible_text_hash ind |analytic| -3.1826>=0.1; R_visible_text_hash iid cons 3.1227>=0.03; R_visible_text_hash iid |analytic| -3.1711>=0.1; R_visual corr cons 2.9351>=0.03; R_visual corr |analytic| -3.0355>=0.1; R_visual ind cons 3.1496>=0.03; R_visual ind |analytic| -3.1826>=0.1; R_visual iid cons 3.1338>=0.03; R_visual iid |analytic| -3.1711>=0.1; R_computed corr cons 2.9037>=0.03; R_computed corr |analytic| -3.0355>=0.1; R_computed ind cons 3.1327>=0.03; R_computed ind |analytic| -3.1826>=0.1; R_computed iid cons 3.1223>=0.03; R_computed iid |analytic| -3.1711>=0.1; R_AX corr cons 2.9008>=0.03; R_AX corr |analytic| -3.0355>=0.1; R_AX ind cons 3.1336>=0.03; R_AX ind |analytic| -3.1826>=0.1; R_AX iid cons 3.1224>=0.03; R_AX iid |analytic| -3.1711>=0.1
- G1 independent confounded: True — ["G1 independent-noise BC~0 pass: ['R_visible_text_hash 0.002 p0.004', 'R_visual 0.005 p0.004', 'R_computed 0.002 p0.004', 'R_AX 0.002 p0.004']"]
- G2 IID: True — ["G2 IID BC~0 pass ['R_visible_text_hash 0.000', 'R_visual 0.001', 'R_computed 0.000', 'R_AX 0.000']"]
- G3 degenerate: False — ['|R|/N R_visual 0.0019 outside 0.01-0.30', '|S_next| 15<16']
- G4 collinearity: False effective 4 no collinearity: effective n_tests 4 floor 0.001 disclosed
- Pos control: False viewport {'width': 1280, 'height': 720} dom_min 2000 a11y_min 300 overlap hist 1.000 mi_rz_corr 0.536 mi_rz_ind 0.016

H(S_next|C)=2.4929 bits (>0.2 PASS)
|S_next|=15 (>=16 FAIL)
|R|/N: vis_text 0.0187 visual 0.0019 computed 0.0187 AX 0.0187 (0.01-0.30)
|A| types 5 card 5 MI 0.0503 (<0.10) leakage 0.0000 (<0.40) hist 1.0000 (>0.3) singleton 0.0000 (<0.70) mi_rz 0.579 (>0.3)

## 6. Barrier Exploratory
Barrier k=20 regime clustering BC 0.0000 p 1.0000 rel_sep 0.00 (exploratory not gating primary)

## 7. Verdict
**MEASUREMENT_INVALID / NOT_APPLICABLE**

Measurement invalid due to gate failure; no H1/H0 claim licensed. Smallest unblock: fix per-stratum digamma/trigamma analytic, ensure H>0.2, |S_next|>=16, genuine DOM capture at 1280x720, or increase positive control bias.

## 8. Reproducibility
- PYTHONHASHSEED 0, numpy default_rng(42), trajectory_id grouping, viewport 1280x720 fixed
- Seeds: correlated 42, independent 43, IID 44, positive 52
- Code: research/physics/run_experiment.py with gammaln/polygamma per-stratum loops (K=n_states alpha=1/K, no heuristic scaling) via analytic_per_stratum_stats
- Data: raw_transitions_correlated.json etc with sha256 in provenance.json, overlap_verification.json, raw_prototypes.json

## 9. Validity Threats
Representation loss bbox 10 bins, style 8 values, AX 5000 k-means placeholder hash with per-R noise, visible_text hash; action tautology MI<0.10 checked; TRAIN leakage via trajectory_id 70/30; history-sufficient strata accounted; analytic per-stratum exact gammaln/polygamma without heuristic scaling; barrier exploratory reported separately; collinearity disclosed with effective n_tests; genuine CDP capture attempted at locked 1280x720 via BrowserGym-core 0.14.3 + Playwright 1.63.0.
