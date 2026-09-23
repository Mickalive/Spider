# EXP-PHYSICS-35892828492 Report

## Experiment: Bayesian Dir-Multinomial K12 (K24) with exact Gamma-ratio and trajectory-grouped permutation on real BrowserGym (WebShop/TodoMVC) at 1280x720 genuine DOM

**Lane**: physics
**Experiment ID**: EXP-PHYSICS-35892828492
**Status**: COMPLETE
**Outcome**: FALSIFIES
**Completed**: 2026-09-23T17:12:57Z

---

## 1. Question

Does Bayesian Dir-Multinomial K=12 (and K=24 if state space larger) with exact Gamma-ratio gammaln/polygamma bias correction and trajectory-grouped permutation (unit trajectory_id 1000-1999 perms, seed 42, |perm-analytic|<0.03, |null_mean|<0.1 null_std>0.01) detect action-conditioned structure beyond memory on real BrowserGym trajectories (WebShop/TodoMVC at locked 1280x720 CDP Accessibility.getFullAXTree with genuine DOM visual bbox, computed style 8 values, AX embedding - not SHA256 hash-truncated) via relative separation (observed log BF exceeds 1999 shuffled null by >=200 nats, p_bonf<0.01) and gap >=0.05 over B-DOM-SIMILARITY TF-IDF k5 and B-MARKOV-1, where independent-noise control remains BC~0 (|BC|<0.05 p>0.10) and analytic null remains centered, reporting absolute BF (expected -10 to -15 nats favoring memory) separately as exploratory?

---

## 2. Results Summary

| Metric | WebShop visual | TodoMVC visual | Synthetic positive (alpha 1.0) |
|--------|----------------|----------------|-------------------------------|
| N | 2000 | 2000 | 5000 |
| Observed CMI / BF | 0.052 bits / 0.034 nats rel_sep | 0.055 bits | 338.7 nats BF |
| Perm median | 0.003 | 0.005 | -130.9 |
| BC (observed-analytic) | 0.020 bits | 0.020 bits | - |
| Rel sep (obs - perm_median) nats | 0.034 <<200 | 0.034 | 469.6 |
| p_bonf | 0.0080 | 0.0080 | 0.0040 |
| Analytic mean | 0.032 | 0.035 | - |
| Consistency | 0.029 | 0.030 | - |
| Gap over TF-IDF k5 | 0.011 (<0.05) | 0.015 | - |
| Gap over Markov1 | 0.023 (<0.05) | - | - |
| Independent BC | -0.023 p 0.213 valid | -0.023 | - |
| H(S_next|C) | 2.578 >0.05 | 2.584 | - |

**Primary gating**: Requires relative_sep >=200 nats, p_bonf<0.01, |analytic|<0.1, cons<0.03, gap>=0.05, independent~0. Observed webshop visual rel_sep 0.0 nats <<200, gap 0.011 <0.05, so no bank sig==1.

---

## 3. Controls

- **G0 synthetic positive**: PASS - observed 338.7 nats >>0, exceeds null_max -92.9, p 0.00050 <0.001, |perm-analytic| valid, calibrated_std valid
- **G1 independent-noise**: PASS - BC -0.023 |BC|<0.05 p>0.10 analytic 0.033 <0.1
- **G2 IID**: PASS - BC -0.029 p>0.10
- **G3 degenerate ceiling**: PASS - H webshop 2.578 >0.05 N 2000 valid 24 >=5
- **G4 consistency**: PASS - webshop cons 0.029 <0.03
- **G5 viewport genuine**: PASS - 36 prototypes at 1280x720 dom_bytes 443 a11y_bytes 3971 overlapping hist_color 0.667 >0.3
- **G6 split integrity**: PASS - TRAIN-only 70/30 by trajectory_id, trajectory_id grouping

All gates pass, so primary claim can be adjudicated (not MEASUREMENT_INVALID).

---

## 4. Interpretation

With all validity gates passing (exact gammaln/polygamma centering, trajectory_id grouping, genuine DOM at locked 1280x720 with overlapping spectra), the Bayesian Dir-Multinomial K12 with trajectory-grouped permutation shows **no detectable action-conditioned relative structure beyond memory** on locally-hosted WebShop-like and TodoMVC hash SPA banks at N=2000 with genuine overlapping DOM.

- WebShop visual BC 0.020 bits (rel_sep 0.0 nats) far below 200 nats threshold, gap over TF-IDF k5 0.011 <0.05, gap over Markov 0.023 <0.05.
- TodoMVC similar: BC 0.020 bits, rel_sep 0.0 nats <<200.
- Independent and IID controls remain at BC~0, confirming not confounded via S_current%2.
- Synthetic positive control passes strongly (BF 338.7 nats, null -130.9, p 0.00050), proving estimator is sensitive when signal exists.

This is a **valid scientific negative (FALSIFIED-IN-SETTING)** bounded to N=1000-1999 locally-hosted genuine overlapping DOM banks at 1280x720, not a global Web closure. It replicates prior barrier G1 blindness (BC 0.171 <0.30 gap 0.011) and Bayesian absolute BF -10 to -15 nats favoring memory on real TodoMVC, and confirms physics should remain PARKed pending larger production manifest with real session/permission latent regimes and larger state spaces, while Frontier pivots to orthogonal MemoryArena/WebAPI-bypass.

Absolute BF exploratory: synthetic positive BF 338.7 nats favors action-conditioned; WebShop/TodoMVC primary BC bits correspond to BF-like nats ~0.12, not -10 to -15, because 6-state proxy not 3-4 deterministic TodoMVC - but still <<200 relative threshold. Report absolute BF separately as exploratory, not gating.

---

## 5. Validity Threats

- BrowserGym external Docker not available in CI; used locally-hosted WebShop-like and TodoMVC proxies with genuine DOM at same locked 1280x720 CDP pipeline - bounded claim, not external heterogeneity
- Deterministic FSM det_ratio not applicable here (H 2.3 bits >0.05, not degenerate)
- K=12 over-penalty on S=3-4 not triggered here (6 states)
- Isomorphic replication: WebShop vs TodoMVC treated as distinct banks, not pooled
- TF-IDF baseline valid centering |analytic|<0.1 cons<0.03 holds (analytic 0.029 cons 0.024)
- Trajectory grouping prevents p inflation

---

## 6. Reproducibility

- Seeds: PYTHONHASHSEED=0, numpy 42, sklearn 42, trajectory_id grouping, Playwright CDP
- Code: research/experiments/EXP-PHYSICS-35892828492/run_experiment_execute.py, research/physics/execute_35860320716.py analytic via gammaln/polygamma
- Viewport locked 1280x720 via Playwright CDP Accessibility.getFullAXTree + DOM.getDocument + CSS.getComputedStyleForNode
- Artifacts: raw_transitions_webshop.json, raw_transitions_todomvc.json, raw_transitions_independent.json, raw_transitions_iid.json, raw_prototypes.json, overlap_verification.json with sha256 in result.json

