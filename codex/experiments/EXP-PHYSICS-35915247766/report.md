# EXP-PHYSICS-35915247766 Report — C-MEAS-VALID Bayesian K12 exact Gamma-ratio on genuine DOM at 1280x720

**Status: COMPLETE Outcome: FALSIFIES**

## Summary
Exact Bayesian Dirichlet-Multinomial K=12 (alpha 1/K) via scipy.special.gammaln/polygamma (digamma/trigamma) with 1999 trajectory-grouped permutation null (grouped by trajectory_id seed42) on genuine overlapping DOM at locked 1280x720.

Genuine prototypes: 36 at 1280x720 dom_min 443 a11y_min 3971 hist_color 0.667 mean_overlap 0.399 verified >0.3.

WebShop primary 50x38 N=1900 H 2.316 valid strata 30 uniqueS 6; TodoMVC secondary N=1900 H 2.337; Synthetic positive N=5000 12-state hash-routed; Independent N=1900 regime-independent; IID N=1900.

## Gate Table
- G0 synthetic positive BF rel_sep>=200 p<0.01 |analytic|<0.1 cons<0.03: True synth visual BF_obs 609.8 perm_median -414.1 rel_sep 1023.9 p_bonf 0.0040 analytic 0.013 cons 0.019 valid_std True calibrated 0.105 threshold rel_sep>=200
- G1 independent BC~0: True
- G2 IID BC~0: True
- G3 degenerate H>0.05 N>=100 >=5 strata |R|/N 0.01-0.30 |A|>1 MI<0.10: True 
- G4 consistency |perm-analytic|<0.03: True
- G5 substrate genuine 1280x720 overlapping: True
- G6 TRAIN leakage: True

All gates must pass for COMPLETE. Any fail => MEASUREMENT_INVALID.

## Per-R WebShop K12
- R_visual: bf_obs -135.4 perm_median -452.5 rel_sep 317.1 bc 0.158 p_bonf_bf 0.0040 analytic 0.015 cons 0.020 gap_dom 0.016
- R_computed_style: bf_obs -135.4 perm_median -452.5 rel_sep 317.1 bc 0.158 p_bonf_bf 0.0040 analytic 0.015 cons 0.020 gap_dom 0.016
- R_AX: bf_obs -135.4 perm_median -452.5 rel_sep 317.1 bc 0.158 p_bonf_bf 0.0040 analytic 0.015 cons 0.020 gap_dom 0.016
- R_event: bf_obs 0.0 perm_median 0.0 rel_sep 0.0 bc -0.000 p_bonf_bf 1.0000 analytic 0.000 cons 0.000 gap_dom -0.142

## Per-R TodoMVC K12
- R_visual: bf_obs -163.1 rel_sep 286.9 bc 0.150 p 0.0040
- R_computed_style: bf_obs -163.1 rel_sep 286.9 bc 0.150 p 0.0040
- R_AX: bf_obs -163.1 rel_sep 286.9 bc 0.150 p 0.0040
- R_event: bf_obs 0.0 rel_sep 0.0 bc -0.000 p 1.0000

## Synthetic Positive
- R_visual: bf_obs 609.8 perm_median -414.1 rel_sep 1023.9 bc 0.275 p 0.0040 cons 0.019
- R_computed_style: bf_obs 609.8 perm_median -414.1 rel_sep 1023.9 bc 0.275 p 0.0040 cons 0.019
- R_AX: bf_obs 887.5 perm_median -136.8 rel_sep 1024.3 bc 0.276 p 0.0040 cons 0.007
- R_event: bf_obs 0.0 perm_median 0.0 rel_sep 0.0 bc -0.000 p 1.0000 cons 0.000

## Baselines
- TF-IDF k5 R_visual: BC_sim 0.142 analytic 0.014 cons 0.019 acc 0.247
- TF-IDF k5 R_computed_style: BC_sim 0.142 analytic 0.014 cons 0.019 acc 0.247
- TF-IDF k5 R_AX: BC_sim 0.142 analytic 0.014 cons 0.019 acc 0.247
- TF-IDF k5 R_event: BC_sim 0.142 analytic 0.014 cons 0.019 acc 0.247

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
- Code: execute_35915247766.py uses scipy.special.gammaln/polygamma exactly.
