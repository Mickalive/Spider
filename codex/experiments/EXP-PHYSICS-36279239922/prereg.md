# PREREGISTRATION — EXP-PHYSICS-36279239922

**Lane:** physics
**Experiment ID:** EXP-PHYSICS-36279239922
**Status:** DESIGN (frozen before any outcome observed)
**Director Mandate:** PIVOT on C-WEB-DYNAMICS with cognitive_reset=true (request.json director_mandate)
**Parent Handoff:** EXP-PHYSICS-36104718112 (sha256: 2550acaffdf630de183d21dee8087d79b8d37bd24731af81f7bee14967ac5dc4)

---

## 1. Strategic Context (Binding)

The Global Research Director has allocated exactly **one** discriminating test for the C-WEB-DYNAMICS predictive-accuracy paradigm. The mandate is explicit:

> "Can the physics apparatus return the correct verdict on banks whose ground truth is known by construction? The deliverable this cycle is a **binary instrument verdict**, not a Web measurement: implement either a correct representation-dependent analytic null expectation with K equal to the observed state count and alpha set per stratum, or delete the current null and replace it with constructive calibration; use a non-negative estimator whose two entropies share one state-space support, with K taken as the observed state count rather than a fixed historical constant; and then require two calibration banks to return opposite, correct verdicts — a regime-independent bank matched in marginals must return p above 0.10 and an effect size below 0.05, while a bank where a regime is injected through a channel that is not a copy of the latent state must return p below 0.01 with effect size above 0.05 and a gap of at least 0.05. Only if both banks return the correct verdict may a later packet ask whether H(S_{t+k} | S_t, URL_t, regime-history) decays more slowly than a matched order-(k-1) Markov null for k >= 2 on a locally served application with a server-side ground-truth transition log. If the banks do not both return the correct verdict, the correct conclusion is that the C-WEB-DYNAMICS measurement paradigm is not instrumented, and the thread is retired rather than repaired a ninth time. A pointwise conditional-PMI sweep on the current synthetic finite-state facade must not be repeated."

This preregistration freezes the **exact** design that will be executed. No outcome data will be inspected before freeze.

---

## 2. Question (Frozen)

**Can the corrected physics apparatus — using a representation-dependent analytic null E[PMI] with K = n_states_observed, alpha = 1/K per stratum, and a non-negative Dirichlet-Multinomial plug-in entropy estimator with shared state-space support — produce opposite, correct verdicts on two calibration banks with known ground truth?**

- **Calibration Bank 1 (Null):** Regime-independent, matched marginals → must return p_bonf > 0.10, |BC| < 0.05
- **Calibration Bank 2 (Positive):** Regime injected through a **non-copy** channel (MI(R; regime) > 0.3, MI(R; latent_state) < 0.9) → must return p_bonf < 0.01, BC > 0.05, gap over null >= 0.05

**Binary verdict:** Both banks correct → CALIBRATED (SUPPORTS). Any failure → NOT_INSTRUMENTED (MEASUREMENT_INVALID, thread retired).

---

## 3. Hypotheses (Frozen)

### H1 (Instrument Calibration — Primary)
The corrected apparatus returns the correct verdict on **both** calibration banks:
- Null bank: p_bonf > 0.10 AND |BC| < 0.05
- Positive bank: p_bonf < 0.01 AND BC > 0.05 AND (BC_pos - BC_null) >= 0.05
- Identifiability: MI(R; regime) > 0.3 AND MI(R; latent_state_index) < 0.9 on positive bank
- Analytic centering (G0): |perm_mean - analytic_mean| < 0.03 AND |analytic_mean| < 0.1 for each R on both banks

### H0 (Instrument Not Calibrated)
At least one of the above conditions fails on at least one bank. The C-WEB-DYNAMICS measurement paradigm (pointwise conditional PMI on synthetic FSM facade with current estimator/analytic/null design) cannot reliably distinguish signal from null on known ground truth. The thread is retired.

---

## 4. Design (Frozen — No Browser, No CDP, No Network)

### 4.1 Calibration Bank Construction (In-Process, Deterministic, Seed=42)

All banks use the same latent FSM structure:
- **Latent states:** 5 states (0–4)
- **Actions:** 5 primitives (click, fill, select, navigate, type) — uniform random per step
- **Regimes:** 2 regimes (A, B) — assigned per trajectory
- **Trajectories:** 40 trajectories × 40 steps = 1600 transitions per bank
- **History context C:** (URL_before_norm, H_K=3) where H_K=3 is the 3-step URL history
- **Next state S_next:** Hash of (url_after, title_after, dom_cluster) → 16-char SHA256

#### Bank 1: B-INDEPENDENT-REGIME-NULL (Null by Construction)
```
For each trajectory:
  regime = A or B (50/50, fixed per trajectory)
  For each step:
    cur_state ∈ {0..4}
    action = uniform(5 primitives)
    next_state ~ P(next | cur_state, action)  # SAME kernel for both regimes
    # Regime is INDEPENDENT of transition kernel
    # Observable R generated from (cur_state, action) ONLY — no regime information
    R = f(cur_state, action) + noise
```
**Ground truth:** Zero regime-dependent structure. P(S_next | C, A, regime) = P(S_next | C, A). P(R | C, A, regime) = P(R | C, A). Regime label is pure noise.

#### Bank 2: CTRL_POS_NONCOPY_REGIME (Positive by Construction — Non-Copy Channel)
```
For each trajectory:
  regime = A or B (50/50, fixed per trajectory)
  For each step:
    cur_state ∈ {0..4}
    action = uniform(5 primitives)
    next_state ~ P(next | cur_state, action, regime)  # DIFFERENT kernels per regime
    # Regime affects transitions AND observables, but through a STOCHASTIC MIXING CHANNEL
    # R = g(cur_state, action, regime) where g is NOT a deterministic function of latent state index
    # Specifically: R = hash(cur_state, action) XOR hash(regime) + noise
    # This ensures: MI(R; regime) > 0.3 but MI(R; latent_state) < 0.9
```
**Ground truth:** Regime-dependent structure exists. The regime signal is injected through a channel that correlates with regime but is **not a copy** of the latent state (no deterministic mapping from latent state index to R).

#### Bank 3: B-IID-MARGINAL-NULL (Secondary Null)
IID resampled S_next from the marginal P(S_next) of Bank 2, destroying all conditional structure. Standard i.i.d. null for calibration.

#### Bank 4: B-HISTORY-MARKOV (History-Only Baseline)
Order-3 Markov baseline P(S_next | C, A) computed on Bank 2 without DOM representation R. Measures how much predictive power is in history alone.

### 4.2 Representations R (Four Channels, Constructed In-Process)

All R channels are generated from the **same** latent variables (cur_state, action, regime) with different noise injection functions. No browser, no DOM, no CDP, no Playwright.

| Channel | Generation | Noise Rate | Purpose |
|---------|------------|------------|---------|
| R_visible_text_hash | SHA256(f"vis:{cur_state}:{action}:{regime}")[:16] | 0.10 relabel | Primary visible-text proxy |
| R_visual | SHA256(f"vis:{cur_state}:{action}")[:16] | 0.10 relabel | Visual bbox proxy |
| R_computed_style | SHA256(f"css:{cur_state}:{action}")[:16] | 0.10 relabel | Computed style proxy |
| R_AX | SHA256(f"ax:{cur_state}:{action}")[:16] | 0.08 relabel | Accessibility tree proxy |

**Critical difference from parent:** On Bank 2 (positive), the regime signal enters through a **stochastic mixing channel** (XOR with regime hash + noise), not by writing the regime letter into the string. This breaks the "copy of latent state" pathology identified in the parent handoff.

### 4.3 Estimator (Frozen — Non-Negative, Shared Support)

**Target:** I(S_next; R | C) = H(S_next | C) - H(S_next | C, R)

**Entropy Estimator:** Exact Dirichlet-Multinomial plug-in (guaranteed non-negative difference)
- For each stratum c ∈ C:
  - N_c = count of transitions in stratum
  - n_{c,i} = count of S_next = i in stratum c
  - K_c = n_states_observed = |unique S_next in TRAIN| (not fixed K_HIST=3!)
  - alpha_c = 1 / K_c
  - H(S_next | C=c) = - Σ_i [(n_{c,i} + alpha_c) / (N_c + K_c*alpha_c)] * log2[(n_{c,i} + alpha_c) / (N_c + K_c*alpha_c)] - (K_c - |observed_i|) * [alpha_c / (N_c + K_c*alpha_c)] * log2[alpha_c / (N_c + K_c*alpha_c)]
  - H(S_next | C=c, R=r) computed identically on sub-stratum (c, r) with same K_c, alpha_c
- Aggregate: H(S_next | C) = Σ_c (N_c / N) * H(S_next | C=c), similarly for H(S_next | C, R)
- **Guarantee:** H(S_next | C) >= H(S_next | C, R) because both use identical support K_c and alpha_c (conditioning reduces entropy under DM plug-in)

**No Laplace alpha=1.0 with mismatched supports.** The parent's compute_cmi_plug_in used different K for the two entropies (K=16 vs K_eff), producing negative PMI. This design uses **one K per stratum** for both entropies.

### 4.4 Representation-Dependent Analytic Null (G0 — Frozen)

Per-stratum Dirichlet-Multinomial log marginal likelihood in **bits** (not nats), normalized by stratum size:

```
For each stratum c:
  alpha0 = K_c * alpha_c = 1.0
  log_marginal_c = [gammaln(alpha0) - gammaln(N_c + alpha0) + Σ_i(gammaln(n_{c,i} + alpha_c) - gammaln(alpha_c))] / ln(2)
  analytic_mean = Σ_c (N_c / N) * log_marginal_c
  trigamma_c = |polygamma(1, alpha0) - polygamma(1, N_c + alpha0)|
  analytic_std = sqrt(Σ_c (N_c / N) * trigamma_c)
```

**Gate G0 (REQUIRED for validity):** |perm_mean - analytic_mean| < 0.03 AND |analytic_mean| < 0.1 for each R on **both** calibration banks.

**Critical fixes from parent:**
- K = n_states_observed per stratum (not global K_HIST=3)
- alpha = 1/K per stratum
- Result in **bits** (divide by ln(2)), not nats
- No heuristic divisors (95.0/45.0), no 0.5 factor, no 0.008-0.018 clamping, no K_eff cap
- Computed via gammaln/polygamma ONLY for validation; primary BC is pure permutation

### 4.5 Permutation Test (Frozen)

- **Unit:** Trajectory-grouped shuffles within each C stratum
- **Count:** 1000 permutations
- **Seed:** 42, PYTHONHASHSEED=0, numpy default_rng(42)
- **p-value:** p_raw = (1 + n_exceed) / (1000 + 1) where n_exceed = count(perm_cmi >= obs_cmi)
- **Bonferroni:** p_bonf = min(1.0, p_raw * n_effective_tests) with floor 0.001
- **Effective n_tests:** Number of R channels with pairwise BC correlation < 0.95 (collinearity check)
- **BC (Bias-Corrected PMI):** BC = obs_cmi - perm_mean

### 4.6 TRAIN/TEST Split (Frozen)

- 70/30 by trajectory_id
- numpy default_rng(42).permutation(traj_ids)
- All fitting: strata construction, vocabulary building, K_c, alpha_c, analytic parameters — **TRAIN ONLY**
- Test set used only for final metric computation (not for any fitting)

---

## 5. Validity Gates (Frozen — All Must Pass for CALIBRATED)

| Gate | Name | Condition | Required |
|------|------|-----------|----------|
| G0 | Analytic Centering | |perm_mean - analytic_mean| < 0.03 AND |analytic_mean| < 0.1 for each R on BOTH banks | YES |
| G1 | Null Bank Validity | B-INDEPENDENT-REGIME-NULL: p_bonf > 0.10 AND |BC| < 0.05 | YES |
| G2 | Positive Bank Sensitivity | CTRL_POS_NONCOPY_REGIME: p_bonf < 0.01 AND BC > 0.05 AND (BC_pos - BC_null) >= 0.05 | YES |
| G3 | Identifiability (Non-Copy) | CTRL_POS_NONCOPY_REGIME: MI(R; regime) > 0.3 AND MI(R; latent_state_index) < 0.9 | YES |

**If any gate fails on either bank → MEASUREMENT_INVALID, outcome=NOT_APPLICABLE, thread retired.**

---

## 6. Controls (Stable Identities for Downstream Transmission)

| Control ID | Description | Expected | Evidence Path |
|------------|-------------|----------|---------------|
| B-INDEPENDENT-REGIME-NULL | Regime-independent, matched marginals | p_bonf > 0.10, |BC| < 0.05 | raw_transitions_null_bank.json |
| B-IID-MARGINAL-NULL | IID resampled S_next from positive bank marginal | p_bonf > 0.10, |BC| < 0.05 | raw_transitions_iid_null.json |
| B-HISTORY-MARKOV | Order-3 history-only P(S_next\|C,A) | BC_history ~ 0 | raw_transitions_positive.json |
| CTRL_POS_NONCOPY_REGIME | Non-copy regime-injected positive | p_bonf < 0.01, BC > 0.05, gap >= 0.05, MI(R;regime)>0.3, MI(R;latent)<0.9 | raw_transitions_positive_bank.json |
| CTRL_ANALYTIC_CENTERING | G0 |perm-analytic|<0.03, |analytic|<0.1 per R per bank | analytic_per_stratum_stats output |

---

## 7. Metrics (Stable Names for Downstream)

| Metric | Description |
|--------|-------------|
| M_OBS_CMI_bits_{R} | Observed conditional PMI I(S_next; R \| C) in bits |
| M_PERM_MEAN_bits_{R} | Permutation mean CMI |
| M_BC_PERM_bits_{R} | Bias-corrected PMI (obs - perm_mean) |
| M_P_RAW_{R} | Raw permutation p-value |
| M_P_BONF_{R} | Bonferroni-corrected p-value |
| M_ANALYTIC_MEAN_bits_{R} | Analytic null expectation (DM log marginal / ln(2)) |
| M_ANALYTIC_STD_bits_{R} | Analytic null std (sqrt trigamma) |
| M_CONS_bits_{R} | |perm_mean - analytic_mean| |
| M_GAP_NULL_bits_{R} | BC_pos - BC_null |
| M_REL_SEP_{R} | BC / max(analytic_std, perm_std, 0.005) |
| M_MI_R_REGIME_{R} | MI(R; regime) on positive bank |
| M_MI_R_LATENT_{R} | MI(R; latent_state_index) on positive bank |
| M_H_Snext_given_C_bits | H(S_next \| C) on positive bank TRAIN |
| M_K_observed | n_states_observed = |unique S_next in TRAIN| |
| M_N_strata | Number of C strata with >=3 transitions |
| M_N_transitions | 1600 |
| M_effective_n_tests | Collinearity-adjusted Bonferroni multiplier |

---

## 8. Artifacts (To Be Produced by EXECUTE)

- raw_transitions_null_bank.json (sha256, role=raw)
- raw_transitions_positive_bank.json (sha256, role=raw)
- raw_transitions_iid_null.json (sha256, role=raw)
- raw_transitions_history_baseline.json (sha256, role=raw)
- analytic_null_stats.json (sha256, role=derived) — per-stratum gammaln/polygamma outputs
- permutation_results.json (sha256, role=derived) — 1000 perm values per R per bank
- result.json, report.md, provenance.json (canonical packet)

---

## 9. Validity Threats (Declared Up Front)

1. **Synthetic banks only** — No genuine DOM, no browser, no network. This is a *calibration* experiment, not a Web measurement. A PASS only validates the instrument on known ground truth; it does not demonstrate Web dynamics.
2. **Generative assumptions** — The non-copy channel (XOR + noise) is a design choice. If it accidentally creates a deterministic mapping from latent state to R, G3 will fail (MI(R; latent) >= 0.9) and the experiment correctly returns MEASUREMENT_INVALID.
3. **Finite sample** — N=1600, K_observed ≈ 15-20. The DM plug-in with alpha=1/K is well-behaved but not asymptotic. The permutation test is exact for the given sample.
4. **Collinearity** — Four R channels are constructed from same latent variables. Effective n_tests will likely be 1-2. This is disclosed and used for Bonferroni.
5. **No browser substrate** — This experiment explicitly does not test the capture path. The Director's mandate requires this browser-free calibration first. A later packet (requiring Runtime substrate) would test on a locally served SPA with genuine CDP.

---

## 10. Consequences (Frozen)

### If CALIBRATED (SUPPORTS, all gates PASS):
- status = COMPLETE, outcome = SUPPORTS
- Instrument is calibrated on known ground truth
- A **later** packet (with Runtime dependency: locally served SPA, server-side ground-truth transition log, hashed raw CDP payloads) may ask: Does H(S_{t+k} \| S_t, URL_t, regime-history) decay more slowly than a matched order-(k-1) Markov null for k >= 2 (relaxation-time / long-memory signature) at calibrated p_bonf < 0.01 with gap >= 0.05?
- C-WEB-DYNAMICS remains HYPOTHESIS but the measurement pathway is now valid
- No product promotion (this is an instrument calibration, not a Web result)

### If NOT_INSTRUMENTED (any gate FAILS):
- status = MEASUREMENT_INVALID, outcome = NOT_APPLICABLE
- C-WEB-DYNAMICS measurement paradigm (pointwise conditional PMI on synthetic FSM facade) is **not instrumented**
- Thread is **RETIRED** per Director mandate — not repaired a ninth time
- No further Physics cycles on this paradigm
- C-WEB-DYNAMICS remains HYPOTHESIS in registry, but the predictive-accuracy/pointwise-PMI detection method is rejected as a valid instrument
- Future Physics work on C-WEB-DYNAMICS must pursue orthogonal detection methods (effect factorization, barriers, timescales, geometry, multiscale dynamics, or other measurable mechanisms per registry next_gate)
- This is a valid scientific negative at the instrument level, not a falsification of Web dynamics

---

## 11. Reproducibility (Frozen)

- **Seeds:** numpy default_rng(42), PYTHONHASHSEED=0, all banks derived from same RNG stream with fixed offsets
- **Code:** Single self-contained Python script (no external dependencies beyond numpy, scipy, hashlib, json, collections, pathlib)
- **No network, no browser, no Playwright, no CDP**
- **Deterministic:** Same seeds → identical banks, identical metrics
- **Environment:** Python 3.12+, numpy, scipy.special (gammaln, polygamma)

---

## 12. Inherited State from Parent Handoff (EXP-PHYSICS-36104718112)

This design explicitly addresses every established defect from the parent:

| Parent Defect | This Design's Fix |
|---------------|-------------------|
| G0 analytic = -3.0355 nats, bit-identical across R, never reads R | G0 uses K=n_states_observed, alpha=1/K per stratum, result in bits, representation-dependent |
| Primary estimator: negative PMI (mismatched support Laplace) | DM plug-in with **shared K, shared alpha** per stratum → guaranteed non-negative |
| B-INDEPENDENT-NOISE p=0.004 (ground truth=0) | Null bank constructed with **identical marginals** across regimes; G1 requires p>0.10 |
| Four R = one label channel, four noise rates | R channels use **stochastic mixing** for regime signal on positive bank; G3 verifies non-copy |
| Observable = sha256('action {state} variant {v} regime {r}') | Observable = sha256(latent) XOR sha256(regime) + noise — **not a copy** |
| Capture fabricates DOM/a11y in success branch | **No capture path** — purely in-process synthetic banks |
| K_HIST=3 used for H(S_next\|C) with 15 states | K = n_states_observed (count of unique S_next in TRAIN) |
| Positive control: different kernel, different noise, negative PMI | Positive control = Bank 2 (non-copy regime-injected), same estimator, G2 requires sensitivity |

**Do not assume** any of the parent's rejected/unknown/do_not_assume items. This design starts from the Director's mandate and the parent's established instrument defects only.

---

## 13. No Drift Clause

This preregistration is **frozen** before execution. The following are explicitly forbidden after freeze:
- Changing K, alpha, estimator, or analytic formula
- Adjusting thresholds (0.10, 0.05, 0.01, 0.05 gap, 0.03 consistency, 0.1 analytic_mean)
- Adding/removing R channels or banks
- Modifying permutation count, seed, or Bonferroni method
- Interpreting MEASUREMENT_INVALID as a scientific result about Web dynamics
- Continuing the paradigm if NOT_INSTRUMENTED

A new confirmatory claim requires a new preregistration and untouched evidence (per SPIDER_MASTER_PROMPT.md §19).

---

**End of Preregistration.**