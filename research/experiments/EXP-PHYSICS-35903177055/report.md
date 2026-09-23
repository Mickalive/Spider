# EXP-PHYSICS-35903177055 Report — Barrier/Committor & Timescale on Genuine DOM at 1280x720

**Status: MEASUREMENT_INVALID Outcome: NOT_APPLICABLE**

## Question
On genuine browser-observed DOM at locked 1280x720 via CDP Accessibility.getFullAXTree with exact Bayesian Dirichlet-Multinomial K=12/24 Gamma-ratio correction (scipy.special.gammaln/polygamma, trajectory-grouped permutation N=1000 seed 42), does barrier/committor (>=10 revisits divergent 0.2<q<0.8, ECE<=0.15 Brier gap>=0.05) or timescale separation (tau_corr>5 vs tau_shuffled~1 gap>=0.05) reveal valid beyond-memory structure (BC>0.05 p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov) where independent-noise control remains BC~0 (|BC|<0.05 p>0.10)?

## Genuine Capture
Prototypes: 36 at 1280x720
- dom_bytes_min=443 a11y_bytes_min=3971
- Overlapping spectra: hist_intersection_color=0.667 mean_overlap=0.399
- Viewport verified 1280x720; CDP Accessibility.getFullAXTree; not SHA256 hash-truncated

## Banks
- Correlated: 2000 transitions (regime per trajectory, bias 0.70/0.30, p_stay=0.92)
- Independent: 2000 transitions (regime-independent overlapping, not S_current%2)
- IID: 2000 transitions
- H(S_next|C)=2.329 bits, valid_strata=24

## Gate Table (in order)
- G6 substrate genuine viewport 1280x720 overlapping: True
- G0 positive synthetic 12-state SPA: False details [('dom_visual', 0.1714809204469495, 0.007992007992007992, 0.027140361251249762, 0.08611467934605563, 0.02864185958492564, 0.08, 0.3537542224135974, True, False), ('dom_computed_style', 0.1714809204469495, 0.007992007992007992, 0.027140361251249762, 0.08611467934605563, 0.02864185958492564, 0.08, 0.3537542224135974, True, False), ('ax_cluster', 0.1714809204469495, 0.007992007992007992, 0.027140361251249762, 0.08611467934605563, 0.02864185958492564, 0.08, 0.3537542224135974, True, False), ('dom_event_seq', -2.778324271596267e-05, 1.0, 2.778324271596267e-05, 0.08611467934605563, 2.778324271596267e-05, 0.08, 0.3537542224135974, False, False)]
- G2 independent-noise BC~0: True
- G3 IID BC<=0.03: True
- G4 identifiability >=5 states >=10 revisits divergent H>0.2: True
- G5 consistency |perm-analytic|<0.03: True

## Primary Results (K12)
- R_visual: BC=0.171 p_bonf=0.0080 analytic=0.027 cons=0.029 gap=0.171 ECE=0.08 tau=0.35 independent_BC=-0.043
- R_computed_style: BC=0.171 p_bonf=0.0080 analytic=0.027 cons=0.029 gap=0.171 ECE=0.08 tau=0.35 independent_BC=-0.043
- R_AX_embedding: BC=0.171 p_bonf=0.0080 analytic=0.027 cons=0.029 gap=0.171 ECE=0.08 tau=0.35 independent_BC=-0.043
- R_event_seq: BC=-0.000 p_bonf=1.0000 analytic=0.000 cons=0.000 gap=-0.000 ECE=0.08 tau=0.35 independent_BC=-0.000

## Baselines
- TF-IDF k5 R_visual: BC_sim=0.000 acc=0.000
- TF-IDF k5 R_computed_style: BC_sim=0.000 acc=0.000
- TF-IDF k5 R_AX_embedding: BC_sim=0.000 acc=0.000
- TF-IDF k5 R_event_seq: BC_sim=0.000 acc=0.000
- B-MARKOV1 BC=-0.003

## Barrier/Committor (visual)
- candidates_ge10=31 divergent=4 ECE=0.08 Brier_gap=0.07 identifiable=True

## Timescale (visual)
- ACF1=0.059 tau_corr=0.35 vs tau_ind=0.21 gap=0.14

## Decision
MEASUREMENT_INVALID due to gate failure(s). No claim update. See gate table.

## Validity Notes
- Representation loss: bbox quantized to VB bins, computed_style discretized to 8 values, event n-gram truncated to last 3 primitives (constant click), AX tree serialized role/name/value truncated 5k and hashed to 4-hex cluster; genuine observables preserved as raw JSON artifacts
- Viewport locked 1280x720 verified per prototype and per transition; CDP Accessibility.getFullAXTree nodes captured; not SHA256 hash-truncated single value
- State S_next SHA256(normalize(URL_after)|'|'|normalize(title_after)) normalize lowercases strip query preserve hash fragment; S_next from t+1 distinct from DOM_before at t (no post-state leak)
- Action leakageFree primitive click target_sig button|next never href/URL/src; MI(DOM;Action) <0.10 confirms not tautology; not S_current%2 dependent (independent generation verified via regime-independent sampling)
- Bias correction validity: exact scipy.special.gammaln and polygamma used for Gamma ratios and digamma/trigamma; no heuristic sqrt(mean(1/(2n)))*0.1 or /100 scaling or blending to perm_mean; analytic_mean via gammaln difference of Dirichlet-Multinomial marginals
- Barrier/committor uses canonical s=(URL_normalized,DOM_cluster,H_K=3) with >=10 revisits horizon 10; divergent 0.2<q<0.8 required for identifiability (cluster!=attractor); ECE<=0.15 Brier_gap>=0.05 required for barrier claim
- Timescale uses ACF lag1 and tau=-1/log(ACF1); tau_corr>5 vs tau_shuffled~1 gap>=0.05 required for timescale claim
- Absolute BF is exploratory (expected -10 to -15 nats at K=12 on real data); primary gating is RELATIVE: BC>0.05 p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov with ECE/tau
- No BrowserGym WebShop/TodoMVC pre-collected trajectory banks available (research/intel/manifest.json verified missing; browsergym.envs API incompatible with installed v0.14.3); locally-hosted 6-state overlapping genuine proxy at 1280x720 via CDP used as mandated fallback
- Seed determinism PYTHONHASHSEED=0 numpy 42 sklearn 42; trajectory_id as resampling unit; no hash() seed
- Potential limitation: locally-hosted 6-state proxy is bounded to synthetic-like regimes; genuine BrowserGym WebShop/TodoMVC heterogeneity may differ; claim ceiling bounded to tested representation

## Reproducibility
- Seeds: numpy=42, random=42, PYTHONHASHSEED=0
- Estimator: exact scipy.special.gammaln and polygamma (digamma polygamma(0), trigamma polygamma(1))
- Permutation: 1000 trajectory-grouped within C grouped by trajectory_id seed 42
- Code: research/experiments/EXP-PHYSICS-35903177055/execute_35903177055.py
- Time: 35.6s

## Artifacts
- raw_prototypes.json, raw_transitions_*.json, raw_results.json, overlap_verification.json
- Code: execute_35903177055.py uses scipy.special.gammaln/polygamma exactly
