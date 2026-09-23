# EXP-PHYSICS-35860320716 Report — Exact Gamma-Ratio Genuine Overlapping-DOM Barrier/Committor & Timescale

**Status: MEASUREMENT_INVALID Outcome: NOT_APPLICABLE**

## Summary
With exact closed-form Dirichlet-Multinomial Gamma-ratio bias correction via scipy.special.gammaln/polygamma (exact digamma/trigamma, no heuristic scaling or consistency blending), overlapping genuine DOM spectra not deterministically tied to generating basins (visual bbox, computed style 8 values, AX embedding from locked 1280x720 via CDP Accessibility.getFullAXTree) and trajectory-grouped permutation (N=1000-1999, K=12/24, |perm-analytic|<0.03), does barrier/committor or timescale reveal valid beyond-memory structure where independent-noise remains BC~0?

Genuine prototypes: 36 at 1280x720 dom_bytes_min 443 a11y_bytes_min 3971 hist_intersection_color 0.667 mean_overlap 0.399 verified overlapping >0.3.

Correlated bank 50x40 N=2000 regime per trajectory bias 0.70/0.30 p_stay 0.70. Independent 50x40 N=2000 regime-independent overlapping (not S_current%2). IID N=2000.

H(S_next|C) 2.329 bits valid strata 24/24.

## Gate Table (in order)
- G6 substrate genuine viewport 1280x720 overlapping: True
- G1 positive genuine correlated BC>=0.30 p<0.01 |analytic|<0.1 valid std cons<0.03 ECE<=0.15 or tau>5: False details [('dom_visual', 0.1714809204469495, 0.007992007992007992, 0.027140361251249762, 0.08611467934605563, 0.02864185958492564, 0.08, 1.0, False), ('dom_computed_style', 0.1714809204469495, 0.007992007992007992, 0.027140361251249762, 0.08611467934605563, 0.02864185958492564, 0.08, 1.0, False), ('ax_cluster', 0.1714809204469495, 0.007992007992007992, 0.027140361251249762, 0.08611467934605563, 0.02864185958492564, 0.08, 1.0, False), ('dom_event_seq', -2.778324271596267e-05, 1.0, 2.778324271596267e-05, 0.08611467934605563, 2.778324271596267e-05, 0.08, 1.0, False)]
- G2 independent-noise BC~0: True
- G3 IID BC<=0.03: True
- G4 identifiability >=5 states >=10 revisits divergent and H>0.2: True
- G5 consistency |perm-analytic|<0.03 on at least one R: True

All gates must pass for primary. Any fail => MEASUREMENT_INVALID.

## Primary per-R Results (K12)
- R_visual: observed 0.199 perm -0.002 analytic 0.027 cons 0.029 BC 0.171 p_bonf 0.0080 d 1.99 gap 0.011 ECE 0.08 tau 1.00
- R_computed_style: observed 0.199 perm -0.002 analytic 0.027 cons 0.029 BC 0.171 p_bonf 0.0080 d 1.99 gap 0.011 ECE 0.08 tau 1.00
- R_AX_embedding: observed 0.199 perm -0.002 analytic 0.027 cons 0.029 BC 0.171 p_bonf 0.0080 d 1.99 gap 0.011 ECE 0.08 tau 1.00
- R_event_seq: observed 0.000 perm 0.000 analytic 0.000 cons 0.000 BC -0.000 p_bonf 1.0000 d -0.00 gap -0.161 ECE 0.08 tau 1.00

## Baselines
- TF-IDF k5 R_visual: BC_sim 0.161 analytic 0.026 cons 0.027 acc 0.277
- TF-IDF k5 R_computed_style: BC_sim 0.161 analytic 0.026 cons 0.027 acc 0.277
- TF-IDF k5 R_AX_embedding: BC_sim 0.161 analytic 0.026 cons 0.027 acc 0.277
- TF-IDF k5 R_event_seq: BC_sim 0.161 analytic 0.026 cons 0.027 acc 0.277
- B-MARKOV1 BC -0.0035 gap vs best 0.011

## Independent / IID
- Independent R_visual BC -0.029 p 1.000 analytic 0.033 cons 0.035
- Independent R_computed_style BC -0.029 p 1.000 analytic 0.033 cons 0.035
- Independent R_AX_embedding BC -0.029 p 1.000 analytic 0.033 cons 0.035
- Independent R_event_seq BC -0.000 p 1.000 analytic 0.000 cons 0.000
- IID R_visual BC -0.035 p 1.000
- IID R_computed_style BC -0.035 p 1.000
- IID R_AX_embedding BC -0.035 p 1.000
- IID R_event_seq BC -0.000 p 1.000

## Barrier / Timescale
- R_visual barrier candidates 31 divergent 4 ECE 0.08 Brier_gap 0.07 tau 1.00 ACF1 -0.018
- R_computed_style barrier candidates 31 divergent 4 ECE 0.08 Brier_gap 0.07 tau 1.00 ACF1 -0.018
- R_AX_embedding barrier candidates 31 divergent 4 ECE 0.08 Brier_gap 0.07 tau 1.00 ACF1 -0.018
- R_event_seq barrier candidates 31 divergent 4 ECE 0.08 Brier_gap 0.07 tau 1.00 ACF1 -0.018

## Decision
MEASUREMENT_INVALID due to gate failure(s). No claim update. See gate table.

## Validity Notes
- Representation loss as per validity_notes.
- Exact gammaln/polygamma used, no heuristic scaling/blending.
- Overlapping spectra verified >0.3, not deterministic red/blue per regime.
- Independent-noise regime-independent not S_current%2.
- No BrowserGym WebShop reuse available; primary is locally-hosted overlapping proxy which satisfies mandate's locally-hosted branch.

## Artifacts
- raw_prototypes.json, raw_transitions_*.json, raw_results.json, overlap_verification.json
- Code: execute_35860320716.py uses scipy.special.gammaln/polygamma exactly.

