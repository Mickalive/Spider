# EXP-PHYSICS-35578258358 — Preregistration

## 1. Question

Can a corrected Bayesian model comparison with K=n_states=12 (as per frozen spec) and N_SHUFFLE>=1000 within-session shuffled-action permutations replicate the audit-corrected SURVIVES_CURRENT_TEST result on the stochastic 12-state SPA, thereby establishing the Bayesian paradigm as the first estimator to pass both C1 (null median < 0) and C3 (p < 0.001) and unblocking Phase 2 beyond-Markov K3-K2 testing?

## 2. Background and Motivation

### 2.1 What has been established
- True I(Y;A|Z) = 1.52 bits on stochastic 12-state SPA (audit-confirmed via exact enumeration and N=50000 empirical plug-in). (EXP-PHYSICS-35530591329)
- Per-stratum PMI 1.46-1.69 bits across 48/48 strata confirms signal is strong and detectable by non-parametric permutation tests.
- K3 PMI = 1.22-1.69 bits, K2 PMI = 0.93-1.51 bits (established reference scale for information-theoretic detection).
- KSG CMI (sklearn k=5) achieves |shuffled-action null_mean|=0.0155 bits — first estimator to center null near zero. (EXP-PHYSICS-35476270440)
- Likelihood-ratio achieves |null|=0.0045 bits — also centers null near zero.

### 2.2 What has failed
- **Plug-in KL with Laplace smoothing** (alpha in {0, 0.01, 0.1, 0.5, 1.0}): All alphas fail simultaneous C1+C3. Alpha=1.0 passes C1 (|null|=0.064) but fails C3 (K3=0.099). Alpha=0 passes C3 (K3=1.377) but fails C1 (|null|=0.924). No crossover. (EXP-PHYSICS-35530591329)
- **Entropy-rate CMI** (alpha in {0.1, 0.5, 1.0}): ALL alphas fail C1 (|null|>=0.200). At alpha>=0.5, CMI becomes NEGATIVE (artifacts). Bias is intrinsic to Laplace smoothing on discrete spaces with many cells. (EXP-PHYSICS-35538866166)
- **KSG CMI k=5**: Passes C1 but fails C3 (positive_control_k3=0.018 on deterministic SPA). Sensitivity tradeoff: near-zero for all inputs. (EXP-PHYSICS-35476270440)
- **LR chi2**: Passes C1 but K2=K3 exactly (history collapse). Cannot test beyond-Markov. (EXP-PHYSICS-35476270440)
- **Bayesian Dirichlet-Multinomial** (as-executed with K bug): null_median +3700 to +4000 nats positive, C1 fails. (EXP-PHYSICS-35572180485)

### 2.3 Root cause of all failures
Laplace smoothing inflates H(Y|Z,A) more than H(Y|Z) because the (z,a) conditioning space has n_a times more cells. Pseudo-counts add artificial uncertainty proportional to cell count. This is intrinsic to histogram-based estimation on discrete spaces with many cells and varying stratum sizes.

### 2.4 Why Bayesian model comparison is different
The Bayesian approach computes marginal likelihoods over model parameters, completely bypassing histogram smoothing. It does NOT estimate CMI — it compares two nested transition models. The log Bayes factor operates on a DIFFERENT scale than CMI (nats vs bits), so prior CMI-scale decision criteria (|null_mean| < 0.1 bits) do not apply.

### 2.5 Parent implementation bug and audit correction
The parent experiment EXP-PHYSICS-35572180485 used K=len(counts) (observed distinct next-states, typically 1-4) instead of the frozen spec-mandated K=n_states=12. This systematically under-penalized M1 over M0, producing a +3621 to +4048 nat upward null bias that triggered the producer's C1 failure. Audit recomputation with corrected K=12 on the identical data shows null median flips to -78 to -131 nats (all alphas PASS C1), observed log BF 168-643 nats exceeds max null by 200-500 nats (all alphas PASS C3). The corrected verdict under K=12 is SURVIVES_CURRENT_TEST, but this is hypothesis-generating only. A new frozen experiment with corrected K=12 and N>=1000 permutations is required for confirmatory claim.

## 3. Hypotheses

**H1 (alternative):** The log Bayes factor (full model P(S_next|S_current,A) vs reduced model P(S_next|S_current)) is significantly > 0 nats on the stochastic SPA, with the shuffled-action null distribution centered at log BF < 0 nats (Occam's razor penalizes the larger model under the null). At least one tested prior specification achieves (a) null median < 0 and (b) observed log BF on stochastic SPA exceeding the 99.9th percentile of the null distribution (permutation p < 0.001).

**H0 (null):** No tested specification achieves both null centering (median < 0) and significant detection (p < 0.001) on the stochastic SPA.

## 4. Model Specification

### 4.1 Full model M1 (action-dependent)
For each state s and action a, the next state s' follows a categorical distribution with parameters theta_{s,a} (12 possible next states). The likelihood is:
P(data | M1) = prod_{i=1}^N theta_{s_i, a_i, s'_i}
with symmetric Dirichlet prior alpha_prior for each theta_{s,a}.

### 4.2 Reduced model M0 (action-independent)
For each state s, the next state s' follows a categorical distribution with parameters phi_s (same for all actions). The likelihood is:
P(data | M0) = prod_{i=1}^N phi_{s_i, s'_i}
with symmetric Dirichlet prior alpha_prior for each phi_s.

### 4.3 Exact marginal likelihoods
Both models have closed-form marginal likelihoods under Dirichlet-Multinomial:
P(data | M) = prod_{cells} [Gamma(K*alpha) / Gamma(N_cell + K*alpha) * prod_i Gamma(n_i + alpha) / Gamma(alpha)]
where K = 12 categories (NOT K=len(counts)), N_cell = total count per cell, n_i = category counts.

### 4.4 Log Bayes factor
log BF = log ML(M1) - log ML(M0) in nats (natural logarithm, NOT log2).

### 4.5 Prior sensitivity
Test three Dirichlet prior concentrations: alpha_prior in {0.5, 1.0, 2.0}.
- alpha=0.5: moderately informative (favors sparse distributions)
- alpha=1.0: uniform (non-informative)
- alpha=2.0: concentrated (favors uniform distributions)

### 4.6 History conditioning
- **K2:** State + last 2 actions (a_{t-1}, a_t). Full model: separate multinomial per (state, a_{t-1}, a_t). Reduced model: separate multinomial per (state, a_{t-1}).
- **K3:** State + last 3 actions (a_{t-2}, a_{t-1}, a_t). Full model: separate multinomial per (state, a_{t-2}, a_{t-1}, a_t). Reduced model: separate multinomial per (state, a_{t-2}, a_{t-1}).

## 5. Analysis Plan

### 5.1 Data collection
- Stochastic 12-state SPA: 12 states, 4 candidates per (state,action), 50% hash routing + 50% uniform random.
- N=5000 transitions (50 sessions x 100 steps), seed=42.
- Same collection procedure as parent EXP-PHYSICS-35530591329.

### 5.2 Primary metric
Log Bayes factor (nats) comparing M1 vs M0.

### 5.3 Null control
Shuffled-action within-session null: N_SHUFFLE >= 1000 permutations, shuffle action labels within each session, recompute log BF, report null distribution (mean, median, std, 99.9th percentile). Permutation p = (count_ge + 1) / (N_SHUFFLE + 1).

### 5.4 Positive control
**Deterministic SPA:** Same 12-state design with deterministic hash routing only. Action determines next state deterministically. Expected: log BF >> 0 nats (strongly favors M1). This validates the Bayesian implementation.

**Stochastic SPA:** The primary test target with true I(Y;A|Z) = 1.52 bits. Expected: log BF >> 0 nats, permutation p < 0.001.

### 5.5 Design verification
- 48/48 (state,action) pairs with 4 distinct candidates (C6).
- >= 2 non-empty stratum size buckets (C7).

## 6. Decision Criteria

### C1 (null validity)
At least 1 prior specification has shuffled-action null MEDIAN < 0 nats (Occam's razor penalizes the larger model under the null).

**Rationale:** Under the null hypothesis (action provides no information), the larger model M1 should have lower marginal likelihood than M0 due to the parameter complexity penalty. This manifests as log BF < 0 on average. If the null median >= 0, the Bayesian approach has systematic upward bias and is invalid for detection.

### C3 (sensitivity)
For any specification passing C1, the observed log BF on the stochastic SPA exceeds the 99.9th percentile of the null distribution (permutation p < 0.001).

**Rationale:** The Bayesian approach should detect the known 1.52-bit action-conditioned structure. If the observed BF is not significantly above the null, the approach lacks sensitivity for this SPA class.

### C6 (design)
48/48 (state,action) pairs with 4 distinct candidates.

### C7 (stratum coverage)
>= 2 non-empty stratum size buckets.

### Phase 2 (beyond-Markov)
If C1 passes, compute K3 log BF - K2 log BF. If > 0 nats with permutation p < 0.01, evidence for beyond-Markov structure.

## 7. Falsification Rules

**FALSIFIED-IN-SETTING** triggers if ANY of:
1. C1 fails for ALL tested prior specifications (null median >= 0)
2. C3 fails for any specification passing C1 (p >= 0.001)
3. C6 fails (< 48/48 pairs)

**MEASUREMENT_INVALID** triggers if:
4. < 30% of strata have >= 5 records
5. < 2 non-empty stratum buckets
6. Any implementation fails

**SURVIVES_CURRENT_TEST** requires ALL of:
- C1 passes (at least 1 specification with null median < 0)
- C3 passes (p < 0.001 for that specification)
- C6 passes
- C7 passes

## 8. Expected Outcomes

### 8.1 If corrected K=12 replicates audit-corrected SURVIVES_CURRENT_TEST
The Laplace smoothing bias is definitively bypassed. The 5th estimator family (after plug-in KL, entropy-rate, KSG, LR) detects the action-conditioned structure. Opens path to:
- Beyond-Markov K3-K2 testing with Bayes factors
- Production Web data with richer state representations
- Potential product integration of Bayesian transition models

### 8.2 If corrected K=12 fails C1 (null median >= 0)
The Bayesian approach has systematic upward bias under the null. The 5th estimator family fails. The Physics lane must pivot to:
- Continuous-state estimators (KDE/kNN on embeddings)
- Production Web data with fundamentally different dynamics
- Abandoning discrete transition estimation entirely

### 8.3 If corrected K=12 fails C3 (p >= 0.001)
The Bayesian approach cannot detect the known 1.52-bit signal. Same pivot as 8.2.

## 9. Consequences

This is the **corrected re-execution of the fifth estimator family** tested on this SPA class:
1. Plug-in KL with Laplace smoothing (FALSIFIED)
2. Entropy-rate CMI (FALSIFIED)
3. KSG CMI k=5 (sensitivity too low)
4. LR chi2 (history collapse)
5. **Bayesian Dirichlet-Multinomial (as-executed FALSIFIED due to K bug; corrected audit shows SURVIVES_CURRENT_TEST)**

If corrected K=12 fails, the cumulative evidence across 5 families will strongly suggest that discrete transition estimation on this SPA class is fundamentally limited by cell-count inflation and stratum size heterogeneity, regardless of estimator paradigm. The Physics lane should then pivot decisively to alternative approaches.

## 10. Parent Handoff Carry-Forward

### Established
- True I(Y;A|Z) = 1.52 bits on stochastic 12-state SPA (audit-confirmed)
- Plug-in KL alpha sweep tradeoff monotonic and irreconcilable
- Entropy-rate CMI does NOT bypass per-stratum KL bias
- Laplace smoothing inflates H(Y|Z,A) more than H(Y|Z) due to cell-count inflation
- KSG CMI k=5 is insensitive (K3=0.000560) but achieves null centering
- LR chi2 collapses history (K2=K3 exactly)
- Design verification: 48/48 (state,action) pairs with 4 distinct candidates
- Bayesian model comparison with corrected K=12: null median -78 to -131 nats (PASS C1), observed log BF 168-643 nats exceeds max null (PASS C3 via percentile, p=0.001996 > 0.001 due to N=500 cap) — AUDIT CORRECTED RECOMPUTATION, hypothesis-generating only
- As-executed K bug (K=len(counts) instead of K=12) explains entire +3700-4000 nat upward null bias — single-bug root cause confirmed by audit recomputation

### Rejected
- Plug-in KL estimator class with Laplace smoothing alpha in {0, 0.01, 0.1, 0.5, 1.0}
- Entropy-rate CMI with alpha in {0.1, 0.5, 1.0}
- Hypothesis that per-stratum KL bias is estimator-specific (entropy-rate bypasses it)
- KSG CMI k=5 for simultaneous C1+C3
- LR chi2 for beyond-Markov detection
- Hyperparameter tuning (reduced smoothing) as remedy
- Deterministic/stochastic strata mixing as cause of bias
- Bias-corrected estimators (equal-weight, median, KNN)

### Unknown
- Whether corrected K=12 result replicates with N>=1000 perms in a new frozen experiment (required for confirmation)
- Whether N=50000 resolves the p-threshold cap (audit notes p=0.001996 with N=500 perms, would be <0.001 with N>=1000)
- Whether Phase 2 beyond-Markov K3-K2 testing passes under corrected K=12 (audit-corrected K3-K2 = 79-235 nats positive, untested at N>=1000)
- Whether the parent EXP-PHYSICS-35476270440 null_mean -213.7 nats discrepancy is due to K handling or shuffle framework differences
- Whether alternative Bayesian methods (WAIC, LOO-CV, fractional Bayes factors) achieve valid null centering on this SPA class

### Do Not Assume
- This FALSIFIED verdict closes C-WEB-DYNAMICS or the Physics lane
- CMI estimation is fundamentally impossible on discrete SPAs
- The 1.52-bit true CMI is undetectable
- Production Web transitions generalize from this synthetic SPA
- The consistent K3-K2 differences are evidence for or against beyond-Markov dynamics

## 11. Code Reuse

- SPA generation and data collection: reuse from EXP-PHYSICS-35538866166 (run_experiment.py)
- Bayesian model comparison: exact Dirichlet-Multinomial marginal likelihood (from EXP-PHYSICS-35476270440 _dirichlet_multinomial_log_marginal function, lines 364-376)
- Shuffled-action null: reuse within-session shuffle framework from parent
- **Critical fix:** Replace K=len(counts) with K=n_states=12 in _dirichlet_multinomial_log_marginal (line 234-235 of EXP-PHYSICS-35572180485/run_experiment.py)

## 12. Risks

1. **Numerical underflow/overflow:** With N=5000 and K=12, Gamma functions may overflow. Mitigate by computing in log-space (already implemented in _dirichlet_multinomial_log_marginal).
2. **Prior sensitivity:** Different alpha_prior values may produce different results. Test alpha in {0.5, 1.0, 2.0}.
3. **Bayes factor scale:** The log BF operates on nats scale, not bits. Decision criteria must be adapted (done: median < 0 and permutation p < 0.001).
4. **Positive control confusion:** Unlike CMI estimators, the Bayesian approach DOES detect structure on the stochastic SPA. The "positive control" IS the primary test target.
5. **Permutation resolution:** With N_SHUFFLE=1000, minimum p = 0.000999 < 0.001 threshold achievable. With N_SHUFFLE=5000, minimum p = 0.0001998.
