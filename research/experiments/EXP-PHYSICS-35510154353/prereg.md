# EXP-PHYSICS-35510154353 — Preregistration

## Status

DESIGN ONLY. Not yet frozen.

---

## 1. Background and motivation

Parent experiment EXP-PHYSICS-35482477045 established:

1. **True CMI is 1.52 bits** on the stochastic 12-state SPA (audit-corrected from producer's 0.004 bits via exact enumeration and N=50000 empirical plug-in).
2. **KSG CMI (k=5) is insensitive**: K3=0.000560 bits (893x below 0.5 threshold against 1.52-bit signal). Null centering works (|null|=0.012, C1 passes).
3. **LR (chi2-per-state) history collapse**: K3=K2=0.103695 exactly (identical to deterministic SPA degenerate baseline). Null centering works (|null|=0.005, C1 passes).
4. **Both estimators pass C1 but fail C3** on the same stochastic SPA with a strong 1.52-bit signal.

The frozen verdict was FALSIFIED-IN-SETTING. The audit (REVISE) identified this as genuine estimator insensitivity, not weak design. The next question is: **is the insensitivity specific to KSG k=5 and LR chi2-per-state, or fundamental?**

The parent handoff recommended testing:
- A plug-in transition-matrix KL divergence estimator (bypasses CMI estimation entirely)
- KSG CMI with k=10 or k=20 (tests neighborhood resolution)
- Permutation test conditioned on (state, action) strata (non-parametric)

---

## 2. Research question

Can alternative CMI estimators — a plug-in KL divergence estimator and KSG CMI k=10 — detect the demonstrated 1.52-bit CMI signal while preserving |shuffled-action null_mean| < 0.1 bits at N=5000?

---

## 3. Hypotheses

- **H0 (null)**: Neither plug-in KL nor KSG k=10 achieves BOTH |shuffled-action null_mean| < 0.1 bits AND positive_control_k3 >= 0.5 bits on the stochastic SPA at N=5000.
- **H1 (alternative)**: At least one of plug-in KL or KSG k=10 achieves BOTH.
- **H2 (beyond-Markov, conditional on H1)**: K3 CMI - K2 CMI > 0.1 bits with bootstrap 95% CI lower > 0.0 at N=5000.

---

## 4. State representation

Same as parent EXP-PHYSICS-35482477045:

- **Z (context)**: For K2: Z = (current_state, history_state_K). For K3: Z = (current_state, history_action_K).
- **Y (target)**: next_state (url_after mapped to state index 0-11).
- **A (action)**: action label (form_submit, button_click, js_navigate, menu_select).
- **Action representation**: Action labels (not action targets/hrefs). No target_href leakage.

---

## 5. Action representation

Action labels: `form_submit`, `button_click`, `js_navigate`, `menu_select`. These are the same 4 actions as parent. No action targets, no hrefs, no DOM features.

---

## 6. Environment

Stochastic 12-state SPA (same as parent):

- 12 states with hash-routed URLs (localhost:18973)
- 4 actions per state
- 4 candidate next-states per (state, action) pair
- **Stochastic mixing**: 50% deterministic hash routing + 50% uniform random over CANDIDATES
- True I(Y;A|Z) ≈ 1.52 bits (audit-confirmed)

**Deterministic SPA control**: Same 12-state design with deterministic hash routing only (I(Y;A|Z)=0 by construction).

---

## 7. Estimators

### 7.1 Primary estimators

**A. Plug-in transition-matrix KL divergence** (preferred, materially orthogonal to KSG)

- Definition: D_KL(P(Y|Z,A) || P(Y|Z)) = sum_{z,a,y} P(z,a,y) * log2[P(y|z,a)/P(y|z)]
- This equals I(Y;A;Z) = CMI by the chain rule.
- Implementation: empirical transition counts with Laplace smoothing (alpha=1.0).
- For K2: condition on (current_state, history_state_K).
- For K3: condition on (current_state, history_action_K).
- Bypasses CMI estimation entirely; works directly on the transition matrix.
- Expected to easily detect 1.52-bit signal if the SPA structure is accessible.

**B. KSG CMI k=10** (tests neighborhood resolution hypothesis)

- sklearn.feature_selection.mutual_info_classif with k=10, alpha=1.0, discrete_features=True.
- Parent used k=5; k=10 doubles the neighborhood to test whether resolution was the binding constraint.
- If k=5 was too coarse for 12-state discrete data, k=10 should improve.

### 7.2 Exploratory estimators

**C. KSG CMI k=20** (further neighborhood expansion)

- Same as B but k=20. Tests whether even larger neighborhoods help.
- Exploratory; not required for the frozen decision rule.

**D. Permutation test** (non-parametric, conditionally stratified)

- For each (state, action) stratum with >=5 records:
  - Compute observed PMI for the stratum.
  - Compute null PMI for 500 within-session action-label permutations.
  - One-sided p-value: fraction of null PMI >= observed PMI.
- Bonferroni correction across strata.
- Does not rely on CMI estimation; tests action-label informativeness directly.
- Exploratory; not required for the frozen decision rule.

### 7.3 Replication baseline

**E. KSG CMI k=5** (parent replication)

- Same as parent. Verifies reproducibility.
- Expected: k3 within 10% of parent 0.000560.

---

## 8. Sampling plan

- **N=5000** transitions (50 sessions x 100 steps), seed=42.
- **N=50000** for convergence test (Phase 2, C4).
- Strata with < 5 records are skipped (MIN_STRATUM_SIZE=5).
- Same session generation procedure as parent.

---

## 9. Controls

### 9.1 Null control (C1)

- **Method**: Shuffled-action null.
- **Procedure**: For each of 500 permutations, shuffle action labels **within each session** (preserving session structure and state sequence), recompute the estimator, take the mean across permutations.
- **Correction from parent**: Within-session shuffle (parent used global shuffle, identified as deviation in audit V5).
- **Threshold**: |shuffled-action null_mean| < 0.1 bits for at least 1 estimator.

### 9.2 Positive control (C3)

- **Method**: Stochastic SPA with known I(Y;A|Z) ≈ 1.52 bits.
- **Threshold**: positive_control_k3 >= 0.5 bits (3x below true signal), permutation p <= 0.001.

### 9.3 Degenerate control

- **Method**: Deterministic SPA (I(Y;A|Z)=0 by construction).
- **Expected**: Both plug-in KL and KSG k=10 return ~0.

### 9.4 Design verification (C6)

- All 48/48 (state, action) pairs have 4 distinct candidates.

### 9.5 Stratum coverage (C7)

- >= 2 non-empty stratum size buckets.

---

## 10. Analysis plan

### Phase 1: Sensitivity screening (N=5000)

1. Collect N=5000 transitions on stochastic SPA (seed=42).
2. For each estimator (plug-in KL, KSG k=10, KSG k=5 replication):
   a. Compute K2 (history=state) and K3 (history=action).
   b. Compute shuffled-action null (500 within-session permutations).
   c. Compute |null_mean| and check C1.
   d. If C1 passes, compute positive_control_k3 and permutation p.
   e. Check C3.
3. Run deterministic SPA degenerate control.
4. Check C6 and C7.
5. Apply frozen decision rule.

### Phase 2: Beyond-Markov (only if Phase 1 SURVIVES)

6. Compute K3 - K2 with bootstrap 95% CI (200 trajectory-block resamples).
7. Check C2: K3 - K2 > 0.1 bits AND CI lower > 0.0.
8. Compute K2 at N=50000 for convergence (C4).

### Phase 3: Exploratory (not frozen, report only)

9. KSG k=20 results.
10. Permutation test results.
11. Stratum-level decomposition.
12. Within-session vs global shuffle comparison.

---

## 11. Decision rules (frozen)

**Verdict priority**: FALSIFIED-IN-SETTING > MEASUREMENT_INVALID > SURVIVES_CURRENT_TEST.

**FALSIFIED-IN-SETTING** if ANY of:
- (1) C1: All estimators have |shuffled-action null_mean| >= 0.1 bits
- (2) C3: For any estimator passing C1, positive_control_k3 < 0.5 bits OR p > 0.001
- (3) C6: Fewer than 48/48 (state,action) pairs with 4 distinct candidates

**MEASUREMENT_INVALID** if:
- (4) Fewer than 30% of strata have >= 5 records
- (5) < 2 non-empty size buckets
- (6) Any estimator implementation fails

**SURVIVES_CURRENT_TEST** requires ALL of:
- (C1) >= 1 estimator with |null_mean| < 0.1 bits
- (C3) positive_control_k3 >= 0.5 bits, p <= 0.001 for that estimator
- (C6) Design check passes
- (C7) >= 2 non-empty size buckets

---

## 12. Sample size justification

N=5000 is inherited from parent as the frozen measurement unit. The parent demonstrated that N=5000 provides:
- Sufficient strata for KSG k=5 (1438 K2 strata, 841 K3 strata)
- Null std of 0.000187 (KSG) and 0.000596 (LR) — well-resolved null
- Positive control p=0.001 for both estimators (rank-based significance)

For the plug-in KL estimator, N=5000 provides ~417 records per (state, action) pair on average, sufficient for transition matrix estimation with 12x4=48 pairs. Laplace smoothing handles sparse strata.

---

## 13. Known deviations from parent

1. **Within-session shuffle**: Parent used global shuffle; this experiment uses within-session shuffle (correcting parent audit V5).
2. **Estimator set**: Parent tested KSG k=5 and LR chi2-per-state; this experiment tests plug-in KL and KSG k=10.
3. **C3 threshold**: Inherited at 0.5 bits from parent (unchanged).

---

## 14. Consequences of outcomes

**If H1 passes** (at least one alternative estimator detects the signal):
- The insensitivity is estimator-specific (KSG k=5 and LR chi2-per-state are insensitive, but alternatives work).
- The CMI research program is unblocked for beyond-Markov testing.
- The plug-in KL estimator becomes the preferred tool for discrete Web state spaces.
- Next question: test I(S_next; A | S_current, history) > 0 on stochastic SPA (H2).

**If H0 confirmed** (all alternative estimators also fail):
- The insensitivity may be fundamental to discrete CMI estimation on 12-state SPAs with the shuffled-action null framework.
- The Physics lane must pivot to fundamentally different detection paradigms or production Web data.
- The CMI estimation pathway is exhausted for this SPA class.

---

## 15. Threats to validity

1. **Synthetic-to-real gap**: All evidence is on a 12-state SPA with hash routing. Production SPAs have different state spaces, action vocabularies, and stochastic dynamics.
2. **Discrete representation**: The SPA uses discrete state/action labels. Continuous state representations may behave differently.
3. **Laplace smoothing**: Both the plug-in KL and the null use Laplace alpha=1.0. Smoothing choice may affect sparse strata.
4. **Within-session shuffle**: Corrects parent deviation but may introduce different bias if sessions have strong autocorrelation.
5. **C3 threshold**: 0.5 bits is conservative but may be too high or too low for alternative estimators.

---

## 16. Reproducibility

- **Code**: run_experiment.py (to be written, based on parent infrastructure)
- **Data**: In-memory SPA simulation, seed=42, N=5000
- **Environment**: Python 3, numpy, sklearn, scipy
- **Hashes**: Will be recorded in provenance.json after execution
