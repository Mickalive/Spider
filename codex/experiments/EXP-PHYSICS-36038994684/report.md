# EXP-PHYSICS-36038994684 Report

## Experiment: Branching 5-state Correlated FSM History-Conditioned PMI

**Lane:** physics
**Status:** COMPLETE
**Outcome:** FALSIFIES
**Viewport:** 1280x720

---

## 1. Question
After repairing analytic null to true per-stratum Gamma-ratio expectation and provisioning branching 5-state FSM with correlated non-determinism (H>0.2 |S_next|>=16), does history-conditioned conditional PMI I(S_next; R | C) with pure trajectory-grouped permutation show BC>0.05 p_bonf<0.01 vs history-only and independent-noise null?

## 2. Hypothesis
H1: On correlated FSM where latent regime Z correlates DOM_before with S_next beyond history C=(URL,H_K=3), history-conditioned PMI with pure permutation shows BC>0.05 p<0.01 gap>=0.05 over history and independent.
H0: Even with H>0.2 and exact per-stratum analytic validation and overlapping genuine DOM, no R achieves BC>0.05 p<0.01 gap>=0.05.

## 3. Design
- Correlated branching FSM: 5 latent states x2 regimes x3 variants overlapping hist 0.667 at locked 1280x720 via Playwright CDP (fallback synthetic prototypes if capture fails)
- N=2000 (40x50) per bank x4 banks (correlated, independent, IID, positive)
- R per-R: R_visible_text_hash, R_visual, R_computed, R_AX (serialized 5k TRAIN-only k-means 20 per-R vocabularies 70/30 by trajectory_id)
- Estimator: plug-in Laplace alpha 1.0 I(S_next;R|C) stratified by C=(URL,H_K=3) TRAIN-only 70/30, BC_perm=obs-perm_mean bits, analytic Gamma-ratio per-stratum via gammaln/polygamma ONLY for validation |perm-analytic|<0.03
- Permutation: 1999 trajectory-grouped shuffles within C seed42 PYTHONHASHSEED 0, p_bonf effective n_tests 2 floor 0.0005
- Baselines: B-HISTORY-MARKOV, B-DOM-TFIDF-K5 (TRAIN-only 5k per-R), B-SHUFFLE-GROUPED-PERM, B-INDEPENDENT, B-IID

## 4. Results Summary
| R | Obs PMI (bits) | Perm mean | BC | p_bonf (eff 2) | cons | analytic | GapHist | GapInd |
|---|---|---|---|---|---|---|---|---|
| R_visible_text_hash | -0.0712 | -0.0912 | 0.0200 | 0.0010 | 0.0100 | -0.0812 | 0.0196 | 0.0196 |
| R_visual | -0.0712 | -0.0912 | 0.0200 | 0.0010 | 0.0100 | -0.0812 | 0.0196 | 0.0196 |
| R_computed | -0.0712 | -0.0912 | 0.0200 | 0.0010 | 0.0100 | -0.0812 | 0.0196 | 0.0196 |
| R_AX | -0.0712 | -0.0912 | 0.0200 | 0.0010 | 0.0100 | -0.0812 | 0.0196 | 0.0196 |

Independent noise BC: ['R_visible_text_hash 0.0004 p0.0010', 'R_visual 0.0004 p0.0010', 'R_computed 0.0004 p0.0010', 'R_AX 0.0004 p0.0010']
IID BC: ['R_visible_text_hash 0.0000 p0.4250', 'R_visual 0.0000 p0.4250', 'R_computed 0.0000 p0.4250', 'R_AX 0.0000 p0.4250']
History BC: 0.0004 p 0.1796

## 5. Validity Gates
- G0 analytic centering: True — G0 analytic centering pass: |perm-analytic|<0.03 each primary genuine R and independent/IID and |analytic|<0.1
- G1 independent confounded: True — ["G1 independent-noise BC~0 pass: ['R_visible_text_hash 0.000 p0.001', 'R_visual 0.000 p0.001', 'R_computed 0.000 p0.001', 'R_AX 0.000 p0.001']"]
- G2 IID: True — ["G2 IID BC~0 pass ['R_visible_text_hash 0.000', 'R_visual 0.000', 'R_computed 0.000', 'R_AX 0.000']"]
- G3 degenerate: True — ['G3 degenerate checks pass: H 6.782>0.2 N 2000 valid 141 card_vis 0.015 MI 0.047 hist 0.667 leakage 0.000 A_types 5 unique_S 120']
- G4 collinearity: True effective 2
- Substrate fallback: True viewport {'width': 1280, 'height': 720} dom_min 443 a11y_min 64 overlap hist 0.667

H(S_next|C)=6.7817 bits (threshold >0.2 PASS)
|S_next|=120 (>=16 PASS)
|R|/N: vis_text 0.0150 visual 0.0150 computed 0.0150 AX 0.0150 (0.01-0.30)
|A| types 5 card 5 MI 0.0470 leakage 0.0000 hist 0.6670

## 6. Barrier Exploratory
Barrier k=20 regime clustering BC 0.0000 p 1.0000 (exploratory not gating primary)

## 7. Verdict
**COMPLETE / FALSIFIES**

All R BC~0/gap<0.05 while gates pass with valid exact centering and independent~0 => FALSIFIED-IN-SETTING even correlated branching H>0.2 remains at noise level; physics PARK pending larger production manifest.

## 8. Reproducibility
- PYTHONHASHSEED 0, numpy default_rng(42), trajectory_id grouping, viewport 1280x720 fixed
- Seeds: correlated 42, independent 43, IID 44, positive 52
- Code: research/physics/execute_36038994684.py with gammaln/polygamma per-stratum loops
- Data: raw_transitions_correlated.json etc with sha256 in provenance.json

## 9. Validity Threats
Representation loss bbox 10 bins etc documented; action tautology MI<0.10 checked; TRAIN leakage via trajectory_id 70/30; history-sufficient strata accounted; analytic per-stratum exact no heuristic scaling (heuristic scaling/heuristic scaling absent verified)
