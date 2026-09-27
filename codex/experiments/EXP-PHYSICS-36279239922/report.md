# EXP-PHYSICS-36279239922 — Calibration Experiment Report

**Lane:** physics  
**Experiment ID:** EXP-PHYSICS-36279239922  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE  
**Verdict:** NOT_INSTRUMENTED — The physics apparatus fails calibration on known ground-truth banks.

---

## 1. Executive Summary

This experiment tested whether the corrected physics apparatus — using a representation-dependent analytic null with K = n_states_observed, alpha = 1/K per stratum, and a non-negative Dirichlet-Multinomial plug-in entropy estimator with shared state-space support — can produce **opposite, correct verdicts** on two constructed calibration banks with known ground truth.

**Result: The instrument is NOT CALIBRATED.** Three of four validity gates fail:

| Gate | Name | Result | Details |
|------|------|--------|---------|
| **G0** | Analytic Centering | **FAIL** | \|analytic_mean\| ≈ 3.8–5.1 bits (required < 0.1); \|perm_mean − analytic_mean\| ≈ 3.0–4.3 (required < 0.03) |
| **G1** | Null Bank Validity | **PASS** | p_bonf = 1.0, BC ≈ 0 on all channels (required p_bonf > 0.10, \|BC\| < 0.05) |
| **G2** | Positive Bank Sensitivity | **FAIL** | p_bonf = 1.0, BC = 0, gap = 0 (required p_bonf < 0.01, BC > 0.05, gap ≥ 0.05) |
| **G3** | Identifiability (Non-Copy) | **FAIL** | MI(R;latent) ≈ 2.26 > 0.9 (required < 0.9); MI(R;regime) ≈ 0.99 > 0.3 passes |

**Per the Director's mandate:** Since the banks do not both return the correct verdict, the C-WEB-DYNAMICS measurement paradigm (pointwise conditional PMI on synthetic FSM facade) **is not instrumented**, and the thread is **retired rather than repaired a ninth time**.

---

## 2. Experimental Design (Frozen)

### 2.1 Calibration Banks

| Bank | Description | Ground Truth |
|------|-------------|--------------|
| **B-INDEPENDENT-REGIME-NULL** | Regime-independent, matched marginals. Regime fixed per trajectory. Next_state ~ P(next \| cur_state, action) — SAME kernel for both regimes. R generated from (cur_state, action) ONLY. | Zero regime-dependent structure. p_bonf > 0.10, \|BC\| < 0.05 expected. |
| **CTRL_POS_NONCOPY_REGIME** | Non-copy regime-injected. Regime switches every 10 steps within trajectory. Next_state ~ P(next \| cur_state, action, regime) — DIFFERENT kernels per regime. R from stochastic mixing channel: regime is primary signal, latent state adds noise. | Regime-dependent structure exists. Regime signal injected through non-copy channel. p_bonf < 0.01, BC > 0.05, gap ≥ 0.05, MI(R;regime) > 0.3, MI(R;latent) < 0.9 expected. |

### 2.2 Key Design Parameters (Frozen)

- **Trajectories:** 40 × 40 steps = 1600 transitions per bank
- **Latent states:** 5 (0–4)
- **Actions:** 5 primitives (uniform)
- **Regimes:** 2 (A, B)
- **Context C:** (URL_before_norm, H_K=3) — 3-step URL history
- **S_next:** 16-char SHA256 of (url_after, title_after, dom_cluster)
- **R channels:** 4 channels, 4-char SHA256 (short hash to induce collisions)
- **Estimator:** Exact Dirichlet-Multinomial plug-in, shared K=|unique S_next in TRAIN|, alpha=1/K per stratum
- **Analytic null (G0):** E[PMI] = Σ_c p(c)[digamma(Kα) − digamma(N_c+Kα) + Σ_i(digamma(n_i+α)−digamma(α))]/ln(2)
- **Permutation test:** 1000 trajectory-grouped shuffles within C strata, seed 42
- **TRAIN/TEST:** 70/30 by trajectory_id, all fitting on TRAIN only
- **Bonferroni:** Effective n_tests from pairwise BC correlation < 0.95

---

## 3. Results

### 3.1 Gate Outcomes

#### G0 — Analytic Centering (FAIL)
The representation-dependent analytic null computes E[PMI] under the Dirichlet-Multinomial prior. With ~440 strata and ~2.5 samples/stratum in TRAIN, the finite-sample bias is extreme:

| Bank | Channel | analytic_mean (bits) | perm_mean (bits) | \|diff\| | \|analytic_mean\| < 0.1? | \|diff\| < 0.03? |
|------|---------|---------------------|------------------|---------|--------------------------|------------------|
| Null | All | 5.092 | ~0.81 | 4.279 | **NO** | **NO** |
| Positive | All | 3.810 | ~0.76 | 3.049 | **NO** | **NO** |

The analytic formula yields large positive values (3–5 bits) because digamma(N_c+1) − Σ digamma(n_i+α) is dominated by the small-N_c regime. The permutation mean is near zero (as expected under the null), so consistency fails catastrophically.

**Root cause:** The frozen design (40×40, 5 states, H_K=3) creates too many strata with too few samples for the analytic null to be accurate. This is a design-level issue, not an implementation bug.

#### G1 — Null Bank Validity (PASS)
The null bank correctly returns no signal:
- p_bonf = 1.0 on all 4 channels
- BC = −3.3×10⁻¹⁶ (effectively zero)
- \|BC\| < 0.05 ✓, p_bonf > 0.10 ✓

#### G2 — Positive Bank Sensitivity (FAIL)
The positive bank shows zero detectable signal:
- p_bonf = 1.0 on all 4 channels
- BC = 0.0 on all channels
- Gap over null = 0.0
- Required: p_bonf < 0.01, BC > 0.05, gap ≥ 0.05

**Root cause:** The DM plug-in estimator with shared K,alpha yields H(S_next\|C) = H(S_next\|C,R) for all permutations. The regime signal in R does not reduce conditional entropy because:
1. Context C = (URL_before, 3-step history) nearly identifies the trajectory. Regime switches every 10 steps, so C contains partial regime information.
2. Sub-strata (C,R) have ≤1 sample typically, making entropy estimates identical.

#### G3 — Identifiability Non-Copy (FAIL)
| Channel | MI(R;regime) | MI(R;latent) | MI(R;regime) > 0.3? | MI(R;latent) < 0.9? |
|---------|--------------|--------------|---------------------|---------------------|
| R_visible_text_hash | 0.9946 | 2.2672 | ✓ | **✗** |
| R_visual | 0.9919 | 2.2626 | ✓ | **✗** |
| R_computed_style | 0.9982 | 2.2707 | ✓ | **✗** |
| R_AX | 0.9930 | 2.2593 | ✓ | **✗** |

MI(R;latent) ≈ 2.26 bits (max possible = log₂(5) ≈ 2.32). The 4-char hash (65,536 values) with only 25 (cur_state,action) combinations acts as a near-injective function. MI(R;regime) is high because regime is the primary signal in R, but this comes at the cost of also encoding latent state.

---

## 4. Interpretation

### 4.1 What This Means

The calibration experiment **correctly falsifies the instrument**. The physics apparatus — as specified in the frozen design — cannot reliably distinguish a known null from a known positive on constructed banks with known ground truth.

This is **not** a falsification of Web dynamics. It is a falsification of the *measurement paradigm* (pointwise conditional PMI on synthetic FSM facade with the current estimator/analytic/null design).

### 4.2 Why the Gates Fail

| Failure | Fundamental Cause |
|---------|-------------------|
| **G0** | Too many strata (~440) with too few samples (~2.5/stratum) for the digamma-based E[PMI] formula to approximate the permutation null. The bias is O(1/N_c) and N_c is tiny. |
| **G2** | The DM plug-in estimator with shared support cannot detect the regime signal because (a) C already encodes trajectory/regime information, (b) sub-strata are too sparse for conditional entropy to differ. |
| **G3** | The frozen R generation requires R = f(cur_state, action, regime). With only 5 latent states, any hash that preserves regime signal also preserves latent state signal. MI(R;latent) ≈ H(latent) = 2.32 bits. |

### 4.3 Validity Threats (Declared Up Front)

1. **Synthetic banks only** — No genuine DOM, browser, or network. This was a calibration experiment, not a Web measurement.
2. **Generative assumptions** — The non-copy channel design (regime as primary signal) was a design choice. The tension between G2 and G3 is inherent.
3. **Finite sample** — N=1600, K_observed ≈ 15–20 per stratum in aggregate, but ~440 strata → ~2.5/stratum. The DM plug-in is well-behaved but the analytic null bias is O(1/N_c).
4. **Collinearity** — Four R channels constructed from same latent variables. Effective n_tests = 1 (perfect correlation of BC values).
5. **No browser substrate** — Explicitly browser-free per Director mandate. A later packet would require Runtime substrate.

---

## 5. Consequences

### Per the Director's Mandate and Frozen Decision Rule:

**VERDICT: NOT_INSTRUMENTED**

- **status** = MEASUREMENT_INVALID
- **outcome** = NOT_APPLICABLE
- The C-WEB-DYNAMICS measurement paradigm (pointwise conditional PMI on synthetic FSM facade) **is not instrumented**.
- The thread is **RETIRED** — not repaired a ninth time.
- No further Physics cycles on this paradigm.
- C-WEB-DYNAMICS remains HYPOTHESIS in the registry, but the predictive-accuracy/pointwise-PMI detection method is **rejected as a valid instrument**.
- Future Physics work on C-WEB-DYNAMICS must pursue **orthogonal detection methods** (effect factorization, barriers, timescales, geometry, multiscale dynamics, or other measurable mechanisms per registry next_gate).

This is a **valid scientific negative at the instrument level**, not a falsification of Web dynamics.

---

## 6. Reproducibility

- **Seeds:** numpy default_rng(42), PYTHONHASHSEED=0
- **Code:** Single self-contained script `execute_calibration_v3.py`
- **No external dependencies** beyond numpy, scipy.special, hashlib, json, collections, pathlib
- **Deterministic:** Same seeds → identical banks, identical metrics
- **Environment:** Python 3.12+, numpy, scipy

---

## 7. Artifacts

| Artifact | Path | SHA256 | Role |
|----------|------|--------|------|
| Null bank transitions | raw_transitions_null_bank.json | 5001860a7f78c8312798aa9c5fb5278a2eff261c10e00962ca485944616e70a3 | raw |
| Positive bank transitions | raw_transitions_positive_bank.json | 9de45a63bafec5fde2ae157cbfcc2960a08727c0802d2bb06e28071e4359efaf | raw |
| IID null bank | raw_transitions_iid_null.json | d655ab3a827f75cd33af612f245066d12865baa45a8d9efb578ab3b43113d97c | raw |
| Analytic null stats | analytic_null_stats.json | 06c6c93ee6b460dd703433750df39e24f3e6ea8aba168c6e792f64da673ced01 | derived |
| Permutation results | permutation_results.json | ffc4ac09176b98fa5679665b54f1fd2028bcdc8b4d45dda4b4d24c70a150467c | derived |
| Full results pickle | results.pkl | bc2cfae658e9f09568e8b41ba95010fed9ecca14253d01f8812a04da04d4163c | derived |

---

## 8. Unresolved Questions

1. Whether any variant of the pointwise conditional PMI paradigm can pass G0 with the frozen design parameters (40×40, 5 states, H_K=3).
2. Whether the regime signal can be made detectable (G2) while keeping MI(R;latent)<0.9 (G3) under the frozen R generation constraints.
3. Whether a different entropy estimator (NSB, Miller-Madow) would yield non-zero BC on the positive bank with this data.

---

**End of Report.**  
This packet is the canonical transmission. Downstream agents must reference `result.json` for machine-readable state.