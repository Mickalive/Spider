# Preregistration: EXP-PHYSICS-35402003775

## Background

The parent experiment (EXP-PHYSICS-35389142077) achieved a major milestone: state-history K=2 conditional PMI = 0.933 bits (p=0.001, d=79.7) on the 12-state hash-routed SPA simulation at N=5000, confirming the beyond-Markov signal is real and reproducible. The parent also demonstrated action-history K=3 at N=5000 = 1.221 bits, showing the prior N=1000 failure was primarily sparsity, not conditioning strategy.

However, the frozen decision rule evaluated FALSIFIED-IN-SETTING due to null control failure (C4): within-stratum conditional permutation yielded null_mean=0.417 bits at K=2 (4.17x the |mean|<0.1 threshold). The convergence of within-stratum (0.417) and action-shuffle (0.406) null means, with block permutation at 0.552, reveals the bias is intrinsic to PMI estimator weighting across deterministic/stochastic strata — not a permutation scheme artifact.

At K=2, 31.5% of strata (407/1292) are deterministic (single url_after, PMI=0 by construction) and dilute the weighted average, while the remaining 68.5% (885/1292) carry signal and bias. The mean observations per stratum is 3.87, with only 30.8% meeting MIN_STRATUM_SIZE=5.

The parent handoff identified the corrective action: test three materially orthogonal null frameworks that address the root cause (estimator bias) rather than the permutation scheme. These are: (a) model-based parametric bootstrap that simulates null samples from the estimated transition distribution; (b) Miller-Madow unbiased PMI estimator that corrects for small-sample bias analytically; (c) conditional entropy H as an alternative to PMI that bypasses PMI weighting entirely.

### Parent carry_forward

- **Established:**
  - Within-stratum conditional permutation FAILS to center null at zero for hash-routed SPA: null_mean=0.417+/-0.006 bits, threshold |mean|<0.1 FAILS by 4.17x. (result.json:metrics.within_stratum_null_mean_k2)
  - Bias floor ~0.41 bits is intrinsic to PMI estimator weighting across deterministic/stochastic strata, not permutation scheme: within-stratum (0.417) and action-shuffle (0.406) converge within 2.6%. (result.json:metrics.null_method_comparison)
  - Deterministic strata 407/1292 (31.5%) contribute PMI=0 by construction; stochastic 885/1292 (68.5%) carry signal and bias. (result.json:metrics.determinism_check_state_k2)
  - State-history K2 PMI=0.933 bits (p=0.001, d=79.7) at N=5000 on 12-state SPA, reproducible across experiments. (result.json:metrics.state_history_pmi_k2)
  - Positive control validates PMI pipeline: 8-state deterministic SPA K3 PMI=1.671 bits (state), 1.806 bits (action), p=0.001. (result.json:controls.POSITIVE_CONTROL_SYNTHETIC_SPA)
  - Fragment-stripping destroys all state information: normalized PMI = 0.0 bits on TodoMVC. (parent carry_forward.established)

- **Rejected:**
  - Within-stratum conditional permutation as null centering method for hash-routed SPAs: null_mean=0.417 bits, 4.17x above threshold.
  - Trajectory-level block permutation as null control: null_mean=0.552 bits, known biased.
  - Action-shuffle as null control: null_mean=0.406 bits, converges with within-stratum, same bias floor.
  - Beyond-Markov URL-level PMI on TodoMVC hash-SPAs: 0/5 variants achieve K3 PMI > 0.05 bits.
  - Title-aware PMI on TodoMVC: 0/5 variants have >=2 unique titles.

- **Unknown:**
  - Whether model-based parametric bootstrap centers null at zero for hash-routed SPAs.
  - Whether Miller-Madow unbiased PMI estimator reduces finite-sample bias below 0.41 bits.
  - Whether conditional entropy H(url_after|action,url_before,history) eliminates deterministic/stochastic mixing bias.
  - Whether the 0.933-bit PMI signal is Markov or beyond-Markov (requires independent validation).
  - Whether null bias generalizes beyond 12-state SPA to other state cardinalities.

- **Do not assume:**
  - C-WEB-DYNAMICS is globally false. The experiment confirms beyond-Markov structure exists and is detectable (K2 PMI 0.933 bits, p=0.001). The FALSIFIED-IN-SETTING verdict is due to null control methodology limitation, not absence of signal.
  - Null bias is evidence against beyond-Markov signal. The permutation bias is intrinsic to PMI estimator weighting; the p-value remains valid.
  - Within-stratum permutation is the best available null method. Other frameworks are untested.
  - The bias floor of ~0.41 bits at N=5000 is irreducible. Alternative estimators may reduce it.
  - Production SPA results generalize from this simulation.

## Hypothesis

**H1 (parametric bootstrap null centering — primary):** A model-based null — estimate P(url_after | url_before, history) from observed data via maximum likelihood with Laplace smoothing, simulate N=5000 null transitions from this estimated distribution for each of 1000 bootstrap samples, compute PMI on each simulated dataset — yields bootstrap null mean PMI within [-0.1, +0.1] bits of zero at K=2 on the 12-state SPA simulation with N=5000.

**H2 (Miller-Madow bias correction):** The Miller-Madow bias-corrected PMI estimator (PMI_MM = PMI + (V_x - 1)/(2*N_x*ln2) + (V_y - 1)/(2*N_y*ln2) - (V_xy - 1)/(2*N_xy*ln2)) reduces the within-stratum permutation null mean to within [-0.1, +0.1] bits of zero.

**H3 (conditional entropy):** DeltaH = H(url_after | action, url_before, history) - H(url_after | url_before, history) yields within-stratum permutation null mean within [-0.1, +0.1] bits of zero, and observed DeltaH > 0.05 bits.

**H0 (all fail):** All three frameworks yield null mean outside [-0.1, +0.1] bits of zero. The null control problem is intrinsic to hash-routed SPA design with deterministic/stochastic mixing at N=5000.

**Rationale for three frameworks:** The inherited bias has three candidate root causes: (1) finite-sample bias in the PMI log-ratio estimator (addressed by Miller-Madow); (2) permutation scheme not respecting the true data-generating process (addressed by parametric bootstrap which simulates from the estimated DGP); (3) PMI weighting itself as a problematic quantity (addressed by conditional entropy which bypasses PMI entirely). These are materially orthogonal — a success in any one validates a different correction pathway.

## Methods

### Testbed

Same 12-state SPA simulation as parent (EXP-PHYSICS-35389142077):
- 12 unique URL states with hash-based routing
- 4 action primitives: form_submit, button_click, js_navigate, menu_select
- Stochastic transitions: choose_next(prev1, prev2, current, action) selects from 4 candidates via SHA256(prev1:prev2:current:action) mod 4
- In-memory simulation

### Data Collection

- N=5000 transitions: 50 sessions x 100 steps, seed=42 (same as parent)
- State-history H_K built from URL states with START_TOKEN padding
- K=2 as primary test (same as parent)

### Framework 1: Parametric Bootstrap

1. From observed data, estimate P_hat(url_after | url_before, history) via maximum likelihood with Laplace smoothing (alpha=1.0 for unseen strata)
2. For each of 1000 bootstrap iterations (seed=42):
   a. For each record in the dataset, draw url_after from P_hat(url_after | url_before=record.url_before, history=record.history)
   b. Keep (url_before, history, action) fixed; only url_after is redrawn
   c. Compute PMI on the simulated dataset using the same pipeline (alpha=0, MIN_STRATUM_SIZE=5)
3. Record bootstrap null mean, std, and 95% CI
4. This preserves the estimated conditional distribution P(url_after|stratum) while breaking action-PMI coupling analytically, not via permutation

### Framework 2: Miller-Madow Corrected PMI

1. For each stratum (url_before, history) with N_s observations:
   a. Compute standard PMI as parent (alpha=0, log2)
   b. Compute Miller-Madow correction: PMI_MM = PMI + (V_a - 1)/(2*N_s*ln2) + (V_y - 1)/(2*N_s*ln2) - (V_ay - 1)/(2*N_s*ln2)
   where V_a = unique actions in stratum, V_y = unique url_after values in stratum, V_ay = unique (action, url_after) pairs in stratum
2. Compute weighted average PMI_MM across strata (same weighting as parent)
3. Apply within-stratum permutation null with corrected estimator: 1000 perms, seed=42
4. Record null mean, std, and corrected PMI_MM at K=2

### Framework 3: Conditional Entropy Difference

1. Compute H(url_after | action, url_before, history) via plug-in estimator with Laplace smoothing
2. Compute H(url_after | url_before, history) (marginal over action)
3. DeltaH_observed = H(url_after | action, url_before, history) - H(url_after | url_before, history)
4. Under within-stratum permutation null: shuffle url_after within each stratum, recompute DeltaH for each of 1000 permutations
5. Expected null: DeltaH_null = 0 because permutation makes action and url_after independent within each stratum
6. Record null mean, std, and observed DeltaH

### Positive Controls (per framework)

- 8-state synthetic deterministic SPA, K=3, N=5000: PMI >= 1.0 bits, p < 0.001
- Conditional entropy positive control: H(S_next|S,H_K=3) > H(S_next|S,H_K=2) on 8-state SPA
- Validates pipeline integrity for each framework

### Comparison Baselines

- Within-stratum conditional permutation null_mean (parent method, expected biased ~0.417)
- Block permutation null_mean (known biased ~0.552)
- Action-shuffle null_mean (expected ~0.406, converges with within-stratum)

## Decision Rule

**Per-framework evaluation:**
Each framework is evaluated independently against the same criterion:
- PASS if |null_mean| < 0.1 bits AND positive control passes AND signal > 0.05 bits
- FAIL if |null_mean| >= 0.1 bits OR positive control fails

**Overall verdict:**
- SURVIVES_CURRENT_TEST if >= 1/3 frameworks passes all conditions (any one valid null enables production testing)
- FALSIFIED-IN-SETTING if 0/3 frameworks pass (all three fail to center null)
- MEASUREMENT_INVALID if positive control fails on any framework (pipeline integrity compromised) or data quality insufficient

**Bonferroni correction:** alpha = 0.0167 for 3 independent framework tests.

## Validity Threats

1. **Parametric bootstrap model misspecification.** The estimated P_hat may not capture the true data-generating process if the 12-state SPA has complex dependencies. Mitigation: Laplace smoothing handles unseen strata; the model is deliberately simple (conditional frequency table) to test whether even a basic DGP model outperforms permutation.

2. **Miller-Madow correction may overcorrect.** The (V-1)/(2Nln2) correction assumes multinomial sampling; the effective V may differ from observed unique counts. Mitigation: report both raw and corrected PMI; the correction is small (O(1/N)) and should not flip sign.

3. **Conditional entropy estimator variance.** Plug-in entropy estimators have known bias for small samples. Mitigation: use Laplace smoothing; compare against permutation null (which shares the same estimator bias).

4. **Deterministic strata dilution.** Same as parent: 31.5% deterministic strata contribute zero to all metrics. This dilutes but does not bias the null (deterministic strata contribute zero to both observed and null).

5. **Framework correlation.** The three frameworks are not fully independent — they all operate on the same dataset and share some estimator components. Bonferroni correction for 3 tests is conservative but appropriate for the primary decision.

6. **No production SPA testing.** This experiment stays in simulation. Production testing requires a validated null first; this experiment provides or denies that prerequisite.

## Expected Outcomes and Consequences

**If any framework survives (>= 1/3 pass):**
- The PMI pipeline becomes measurement-valid for hash-routed SPAs
- The inherited FALSIFIED-IN-SETTING verdict from null methodology is resolved
- The surviving framework becomes the standard null control for subsequent Physics experiments
- C-WEB-DYNAMICS advances from HYPOTHESIS toward EXPERIMENTAL
- Production SPA testing is unblocked

**If all frameworks fail (0/3 pass):**
- The null control problem is intrinsic to hash-routed SPA design with deterministic/stochastic mixing at N=5000
- The Physics lane pivots to the orthogonal question: Is the 0.933-bit K2 PMI signal primarily Markov or beyond-Markov?
  - Compare K2 PMI (0.933 bits) against action-history K3 PMI at same N
  - If K3 > K2: signal is primarily Markov (action determines next state given current state)
  - If K2 > K3 by > 0.1 bits: history adds beyond-Markov information
  - This decomposition does not require null centering (it is a ratio/comparison, not an absolute test)
- C-WEB-DYNAMICS remains HYPOTHESIS; the detection strategy changes but the claim is not closed

**Information gain:**
Either outcome materially changes the Physics lane trajectory — the highest-information experiment available given the inherited state.
