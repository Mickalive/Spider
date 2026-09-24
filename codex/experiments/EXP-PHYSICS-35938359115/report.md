# EXP-PHYSICS-35938359115 Report — C-MEAS-VALID Bayesian K12 exact Gamma-ratio on genuine DOM at 1280x720

**Status: COMPLETE Outcome: FALSIFIES**

## Summary
Exact Bayesian Dirichlet-Multinomial K=12 (alpha 1/K) via scipy.special.gammaln/polygamma (digamma/trigamma) with 1999 trajectory-grouped permutation null (grouped by trajectory_id seed42) on genuine overlapping DOM at locked 1280x720.

Genuine prototypes: 36 at 1280x720 dom_min 443 a11y_min 64 hist_color 0.667 mean_overlap 0.399 verified >0.3.

WebShop primary 50x38 N=1900 H 2.316 valid strata 30 uniqueS 6; TodoMVC secondary N=1900 H 2.337; Synthetic positive N=5000 12-state hash-routed; Independent N=1900 regime-independent; IID N=1900.

## Gate Table
- G0 synthetic positive BF rel_sep>=200 p<0.01 |analytic|<0.1 cons<0.03: True synth visual BF_obs 814.6 perm_median -465.3 rel_sep 1280.0 p_bonf 0.0040 analytic 0.015 cons 0.021 valid_std True calibrated 0.356 threshold rel_sep>=200
- G1 independent BC~0: True
- G2 IID BC~0: True
- G3 degenerate H>0.05 N>=100 >=5 strata |R|/N 0.01-0.30 |A|>1 MI<0.10: True 
- G4 consistency |perm-analytic|<0.03: True
- G5 substrate genuine 1280x720 overlapping: True
- G6 TRAIN leakage: True

All gates must pass for COMPLETE. Any fail => MEASUREMENT_INVALID.

## Per-R WebShop K12
- R_visual: bf_obs -135.4 perm_median -452.5 rel_sep 317.1 bc 0.158 p_bonf_bf 0.0040 analytic 0.015 cons 0.020 gap_dom 0.034
- R_computed_style: bf_obs -135.4 perm_median -452.5 rel_sep 317.1 bc 0.158 p_bonf_bf 0.0040 analytic 0.015 cons 0.020 gap_dom 0.034
- R_AX: bf_obs -135.4 perm_median -452.5 rel_sep 317.1 bc 0.158 p_bonf_bf 0.0040 analytic 0.015 cons 0.020 gap_dom 0.034
- R_event: bf_obs 0.0 perm_median 0.0 rel_sep 0.0 bc -0.015 p_bonf_bf 1.0000 analytic 0.015 cons 0.015 gap_dom -0.139

## Per-R TodoMVC K12
- R_visual: bf_obs -163.1 rel_sep 286.9 bc 0.150 p 0.0040
- R_computed_style: bf_obs -163.1 rel_sep 286.9 bc 0.150 p 0.0040
- R_AX: bf_obs -163.1 rel_sep 286.9 bc 0.150 p 0.0040
- R_event: bf_obs 0.0 rel_sep 0.0 bc -0.015 p 1.0000

## Synthetic Positive
- R_visual: bf_obs 814.6 perm_median -465.3 rel_sep 1280.0 bc 0.334 p 0.0040 cons 0.021
- R_computed_style: bf_obs 814.6 perm_median -465.3 rel_sep 1280.0 bc 0.334 p 0.0040 cons 0.021
- R_AX: bf_obs 1067.4 perm_median -162.2 rel_sep 1229.6 bc 0.321 p 0.0040 cons 0.001
- R_event: bf_obs 0.0 perm_median 0.0 rel_sep 0.0 bc -0.015 p 1.0000 cons 0.015

## Baselines
- TF-IDF k5 R_visual: BC_sim 0.124 analytic 0.015 cons 0.019 acc 0.253
- TF-IDF k5 R_computed_style: BC_sim 0.124 analytic 0.015 cons 0.019 acc 0.253
- TF-IDF k5 R_AX: BC_sim 0.124 analytic 0.015 cons 0.019 acc 0.253
- TF-IDF k5 R_event: BC_sim 0.124 analytic 0.015 cons 0.019 acc 0.253

## Decision
FORALL banks sig fails while gates pass => FALSIFIED-IN-SETTING — even correctly centered genuine DOM remains BC~0 / rel_sep<200, estimator not valid on this genuine scale; physics remains PARKED.

## Validity Notes
- Representation loss as per validity_notes.
- Exact gammaln/polygamma used, no heuristic.
- Overlapping spectra verified >0.3.
- Independent regime-independent not S_current%2.
- No BrowserGym reuse available; primary locally-hosted proxy bounded.

## Artifacts
- raw_prototypes.json, raw_transitions_*.json, raw_results.json, overlap_verification.json
- Code: execute_35938359115.py uses scipy.special.gammaln/polygamma exactly.
