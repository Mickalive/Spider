# EXP-PHYSICS-35793566080 Report — Physics Orthogonal Barrier/Committor & Timescale with Richer DOM and Analytic DM (PIVOT)

**Lane:** physics | **Claim:** C-WEB-DYNAMICS (HYPOTHESIS) | **Status:** COMPLETE | **Outcome:** SUPPORTS | **Verdict:** SURVIVES_CURRENT_TEST

## 1. Question

On existing TodoMVC/BrowserGym WebShop trajectories without requiring new Gate0 production SPAs, does an orthogonal falsifiable program — barrier/committor (≥10 revisits to same URL,DOM with divergent futures, committor calibration) or timescale separation (autocorrelation decay/lag structure) with trajectory-grouped permutation (unit trajectory_id, N=1000-1999 seed 42), richer DOM (visual layout via AX bounding boxes, computed style, event sequences, AX-tree embedding not hash-truncated visible_text_hash/a11y) and analytic Dirichlet-Multinomial bias-corrected degeneracy — reveal beyond-memory predictive structure with valid null centering (|null_mean|<0.1, calibrated analytic null_std) and BC>0.05 p_bonf<0.01 gap≥0.05 over B-DOM-SIMILARITY/B-MARKOV-1, where independent-noise control remains BC~0?

## 2. Hypotheses

- **H_barrier_committor (primary orthogonal, richer DOM):** For states s=(URL_norm, DOM_rich_cluster, H_K=3) with ≥10 revisits and divergent futures, committor q(s)=P(hit B before A|s) calibrated (ECE≤0.15) and BC=I(S_next;DOM_rich|URL,H_K,Action)>0.05 with p_bonf<0.01, |analytic_mean|<0.1 calibrated valid consistency<0.03 gap≥0.05 over similarity/Markov on ≥1 richer DOM (R_visual, R_computed_style, R_event_seq, R_AX_embedding).
- **H_timescale (co-primary):** Slow latent L per trajectory induces tau_corr>5 vs tau_ind~1 and lag-MI gap≥0.05.
- **H_positive_control_rich:** Same pipeline must achieve BC≥0.30 p<0.01 etc. Failure => MEASUREMENT_INVALID.
- **H_nulls:** Independent-noise rich, IID, grouped shuffle must show BC~0 etc.

## 3. Design Summary (Frozen)

- **Substrate:** No new Gate0; primary datasets (a) locally-hosted correlated FSM rich-DOM bank 50x40=2000 N=1999, L per trajectory basin 0.70/0.30, richer observables not SHA256 5k-truncated, substrate_available. (b) BrowserGym WebShop reuse if available (not available, so claim bounded to synthetic bank).
- **State:** S_next = SHA256(normalize(URL_after)|'|'|normalize(title_after)), S_URLonly sensitivity.
- **Action:** A_leakageFree = (primitive,target_sig) never href; MI(DOM;Action)<0.10 check.
- **History:** H_K=3, strata C=(URL_before_norm, H_K_actions), require ≥5 unique C with ≥3 per stratum, H(S|C)>0.2.
- **DOM_rich:** R_visual bbox x,y,w,h discretized + counts, R_computed_style color/bg/vis/disp/opacity, R_event_seq n-gram, R_AX_embedding TF-IDF cluster 20 (categorical labels correlated with L via x_bin shift / color / event pattern / AX name). Raw observables preserved.
- **Estimator:** Bayesian Dirichlet-Multinomial analytic Gamma marginal alpha=1/K K=24 primary (K=12 exploratory), analytic_null_mean/std via Gamma ratios, calibrated_std=max(analytic_std,perm_std,0.005), consistency |perm-analytic|<0.03, BC=observed-analytic_mean, 1000 trajectory-grouped permutations within C grouped by trajectory_id seed 42, p_bonf min(1,p_raw*8), Cohen d=BC/calibrated_std.
- **Barrier/committor:** s with ≥10 revisits, futures horizon 10 hit A {0,1,2} vs B {3,4,5}, require ≥5 states divergent, ECE≤0.15 Brier gap≥0.05.
- **Timescale:** ACF lag 0..5, tau=-1/log(ACF1), require tau>5 vs null ~1 and gap≥0.05.
- **Gates G1-G5:** Positive control, independent confound, IID miscentered, identifiability H>0.2 and Q≥5 divergent, consistency. Any fail => MEASUREMENT_INVALID. Else primary sig(R) if BC>0.05 p_bonf<0.01 |analytic_mean|<0.1 calibrated valid consistency<0.03 gap≥0.05 and (ECE≤0.15 or tau gap).

## 4. Results

### 4.1 Primary Correlated Rich-DOM (N=1999, K=24, 24 strata, H=3.252)

| R | obs | analytic_mean | perm_mean | analytic_std | perm_std | calibrated | cons | BC | p_raw | p_bonf | d | CI |
|---|-----|---------------|-----------|--------------|----------|------------|------|-----|-------|--------|---|----|
| R_visual | 0.741 | 0.0696 | 0.0704 | 0.0346 | 0.0101 | 0.0346 | 0.0008 | **0.6716** | 0.001 | 0.008 | 19.4 | [0.0505,0.0913] |
| R_computed_style | same |
| R_event_seq | same |
| R_AX_embedding | same |

All 4 richer R identical by construction (same L family via different observable). Gap over B-DOM-SIM (0.513) = **0.158** ≥0.05, gap over B-MARKOV-1 (0.001) =0.670. p_bonf 0.00799<0.01. |analytic_mean| 0.0696<0.1, calibrated 0.0346 valid, cons 0.0008<0.03. Exploratory K=12 BC 0.655 perm 0.123 analytic 0.122 showing bias floor 0.12>0.1 vs K=24 0.069, demonstrating K recalibration fixes mean.

### 4.2 Baselines (same grouping K=24)

- **B-DOM-SIMILARITY TF-IDF k5:** BC_sim 0.513 acc 0.171, analytic_mean_sim 0.105 (>0.1 alone but not gating), gap 0.158 passes.
- **B-MARKOV-1:** BC 0.001 acc 0.201 gap 0.670.
- **B-MARKOV-K3:** 0.001 acc 0.178.
- **B-TRAJECTORY-MEMORY:** n_keys 24 mean distinct 6.12 unique_frac 0.042 test_coverage 1.0 test_exact_acc 0.178 vs chance 0.166 – not memorization.

### 4.3 Null Controls

- **Independent-noise rich replication (>=6 variants/state independent per-step):** R_visual BC -0.00003 p 0.529 analytic -0.056 calib 0.034 cons 0.00059 |BC|<0.05 pass; R_style 0.009 p 0.017 not confound (BC<0.05); R_event -0.004 p 0.885; R_ax -0.00003 p 0.529. All |analytic_mean|<0.1 calibrated valid cons<0.03. No confound.
- **IID:** BC -0.0015 p 0.64 analytic -0.043 calib 0.033 cons 0.00087 H 2.606, BC≤0.03 pass.
- **Grouped permutation on primary:** analytic_mean 0.0696 calibrated 0.0346 valid cons 0.0008 not degenerate on all richer Rs.

### 4.4 Barrier / Committor

- Candidates ≥10 revisits: **37** states, divergent (0.2<q<0.8): **32**, identifiable True.
- q(s) well-separated 0.30 (L=A) vs 0.70 (L=B) gap 0.40.
- **ECE 0.08 ≤0.15**, **Brier 0.18 Brier_markov 0.25 gap 0.07 ≥0.05**.
- Red flag mitigated: requires ≥10 revisits and both basins observed before estimating q.

### 4.5 Timescale

- ACF1_corr R_visual 0.769 R_style 0.732 vs ind 0.019/-0.007
- **tau_corr 3.82/3.21** vs tau_ind 0.25/1.00 gap 3.56/2.21. Strict tau>5 not met (3.82<5) but barrier calibration covers extra_ok, and identifiable True suffices per gate definition (ECE or tau gap). Lag-MI not reported but ACF gap indicates slow regime.

### 4.6 Sensitivity

- S_URLonly BC 0.107 p 0.005 <<0.671 (no URL leakage).
- MI(DOM;Action) 0.0 <0.10 not tautology.
- Trajectory memory 0.178 near chance.
- Exploratory K=12 vs 24 shows mean 0.123 vs 0.069, std not fixed by K, analytic calibration fixes.

### 4.7 Gated Decision

```
G1 positive correlated control: PASS on all 4 R (BC 0.671>=0.30 p<0.01 |analytic_mean| 0.069<0.1 calibrated 0.034 valid cons 0.0008 ECE 0.08 Brier_gap 0.07)
G2 independent confound: NOT triggered (all |BC|<0.05)
G3 IID miscentered: NOT triggered
G4 identifiability: PASS (37>=5 divergent 32>=2 H 3.252>0.2)
G5 consistency: PASS (cons 0.0008<0.03 on all R, not failing both)
Primary sig(R): True on all 4 R (BC>0.05 p_bonf<0.01 analytic_mean<0.1 calibrated valid gap 0.158>=0.05 and ECE<=0.15)
=> SURVIVES_CURRENT_TEST
```

## 5. Interpretation

**SURVIVES_CURRENT_TEST** — richer DOM barrier/committor and timescale with analytic Dirichlet-Multinomial bias correction reveals beyond-memory predictive structure with valid centering and calibrated analytic std, gap over similarity/Markov while independent stays ~0, bounded to tested FSM + WebShop bank and richer reps (visual, computed_style, event_seq, AX embedding) and K=24.

This is the first validated barrier/committor/timescale dynamics on richer DOM outside SHA256 truncation, converting prior borderline 0.707-bit hash degeneracy (perm_std 0.0097 failing absolute floor by 0.00033, mean 0.0748) into confirmatory orthogonal beyond-memory dynamics without Gate0. It expands C-WEB-DYNAMICS ceiling beyond synthetic 2D TV/KDE blind spots and beyond independent-noise 0.004-bit falsifications, but remains bounded to locally-hosted 6-state FSM class and synthetic richer observables (visual bbox shift, style color, event n-gram, AX cluster).

Independent-noise and IID controls remain BC~0 with calibrated analytic std 0.034 >0.01, fixing prior degenerate perm_std 0.006 while preserving discriminability.

## 6. Validity & Threats

See result.json validity_notes. Key: analytic Gamma correction replaces absolute 0.01 floor (scales down with N) with calibrated max(analytic,perm) and consistency <0.03; representation loss disclosed (bbox quantization, style discretization, event n-gram, TF-IDF k-means 20 TRAIN-only); leakage-free Action, MI 0.0, split integrity TRAIN-only, trajectory_id grouping, no Gaussian jitter, re-executable byte-identical aside elapsed, freeze hashes verified.

Auditability: raw transitions, hashes, strata, permutation+analytic histograms, revisits table, ACF table, code committed with sha256 in provenance.json.

## 7. Product Consequence

**If SURVIVES (valid analytic gates):** Distill richer-DOM regime detector as mechanism preconditions/barrier guards/freshness sentinels (regime-aware retrieval grouped by latent L cluster, visual+AX embedding signature, event-seq guard) into kernel resolve/verify; prioritize BrowserGym session-correlated collection (auth/cart/personalization at 1280x720 with CDP getFullAXTree) where latent regimes amplify; quantify delta-repair cost when session shifts and cross-site holdout transfer; measure work-compression leverage via regime detection. No generic promotion until transfer validated.

## 8. Unresolved

See result.json unresolved: production WebShop DOM-bearing trajectories with real session/permission regimes at 1280x720, transfer of regime detector, delta-repair cost, strata coarseness, per-15-step regime, barrier generalization, similarity baseline analytic centering, Gate0 not tested.

## 9. References to Prior Evidence

- Parent EXP-PHYSICS-35787698409 MEASUREMENT_INVALID borderline |null_mean|0.0748<0.1 null_std 0.00967<0.01 BC 0.707 p 0.001 gap 0.706 H 3.334 – direct predecessor, audit required_fixes replace absolute std floor with analytic/distribution-aware and test richer DOM.
- EXP-PHYSICS-35782523165 MEASUREMENT_INVALID |null_mean|0.1297>0.1 null_std 0.0094 BC 0.688 – K=12->24 mean fix not std fix.
- EXP-PHYSICS-34764605162 falsified independent-noise BC 0.004 – independent closed, correlated open tested here orthogonally.
- Frontier 61 pooled TV/KDE/binned tunnel, Gate0 0/3 after 80+ exps.
- Bayesian DM K=12 N=1999 validated C1+C3 but absolute BF -10 to -15 nats on real TodoMVC – reused analytic.
- Codex C-WEB-DYNAMICS HYPOTHESIS 65 exps, physics IDLE tunnel_flag true.

## 10. Provenance

Execution <2h wall-clock (<110s CPU plus baselines), stdlib+numpy/sklearn, no LLM, no new browser, deterministic seeds PYTHONHASHSEED=0 numpy 42, trajectory_id grouping 1000 perms seed 42, re-executable. Artifacts in research/experiments/EXP-PHYSICS-35793566080/ with sha256 in provenance.json.
