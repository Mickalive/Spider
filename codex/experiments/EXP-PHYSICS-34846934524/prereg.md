# EXP-PHYSICS-34846934524 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34846934524
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Parent**: EXP-PHYSICS-34764605162 (independent per-step DOM observation noise, FALSIFIED-IN-SETTING)
- **Date**: 2026-09-14
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On locally-hosted Express SPAs with correlated non-determinism (persistent session_id that determines DOM variant at each FSM state), does DOM structural features exhibit conditional PMI I(S_next; DOM_before | URL, H_K=3) > 0 with Bonferroni-corrected permutation p < 0.00417?

## 3. Motivation

Three prior Physics experiments now bound the DOM-hash representation path:

1. **Deterministic Express SPAs** (EXP-PHYSICS-34724244876): PMI=0 at K=3, 100% action-history accuracy, DOM fully redundant.
2. **Independent per-step observation noise** (EXP-PHYSICS-34764605162): PMI 0.004-0.025 bits at K=3, Bonferroni p=1.0. E[I]=0 by construction because DOM variants are drawn independently per step (audit V1).
3. The audit ceiling for EXP-PHYSICS-34764605162 explicitly carves out **correlated non-determinism** as the one remaining locally-hosted setting where DOM_before could predict DOM_after.

The key gap: independent per-step noise means DOM_before and DOM_after are independent by construction (E[I]=0). Correlated non-determinism — where a persistent latent variable (session_id) determines DOM variants — creates a genuine dependency between DOM_before and DOM_after through the shared session variable.

If correlated non-determinism also yields PMI ≤ 0, the DOM-hash path is closed across all locally-hosted regimes and the lane should move to network-response information theory (API payload structure, response headers, timing signatures).

If correlated non-determinism yields PMI > 0, it identifies the specific condition (persistent session state) under which DOM encodes predictive dynamics.

## 4. Hypotheses

### H1: Session-Correlated PMI
Conditional PMI I(S_next; DOM_before | URL, H_K=3) > 0.0 bits on session-SPA with Bonferroni-corrected permutation p < 0.00417 (12 comparisons: 4 representations x 3 K values).

**Theoretical basis**: With 10 sessions mapping deterministically to 5 variants (2 sessions per variant), variant_before reveals session identity (reducing 10 sessions to 2 candidates), which determines variant_after. Expected PMI ≈ 1.32 bits (see Appendix A). This is large enough to survive Bonferroni correction even with finite-sample noise.

### H2: Deterministic Baseline
Deterministic SPA (Level 0) has conditional PMI = 0.0 at all K values, replicating parent findings. This confirms the pipeline returns 0 when no variants are present.

### H3: Independent Noise Baseline
Independent per-step noise SPA (Level 1) has conditional PMI ≈ 0.0 at K=3 with Bonferroni p ≥ 0.00417, replicating parent EXP-PHYSICS-34764605162. This confirms the pipeline distinguishes correlated from independent non-determinism.

### H4: Representation Isomorphism
visible_text_hash, accessibility_tree_hash, and multi_feature_hash produce identical or near-identical PMI values (parent audit V4 found them 1-1 in this FSM design where variant encoding is in text content). numeric_structural PMI = 0.0 (element counts invariant per FSM state).

### H5: K-Value Gradient
PMI decreases with increasing K: PMI(K=1) > PMI(K=2) > PMI(K=3). At K=1, action history is less sufficient, so DOM_before provides both session information and弥补 action-history deficiency. At K=3, action-history is sufficient for FSM state, so DOM_before only provides session information for variant prediction.

## 5. Data Generation

### 5.1 Session-SPA Design

Same 5-state linear FSM as parent:
- States: landing → form_s1 → form_s2 → review → complete → landing
- One deterministic action per state (begin, advance, finalize, submit, restart)

**Key modification**: Persistent session_id determines DOM variant at each state.

### 5.2 Session Configuration

- **N_SESSIONS = 10**: 10 persistent sessions, each randomly assigned to a trajectory
- **N_VARIANTS = 5**: 5 DOM variants per FSM state
- **Mapping**: Session s maps to variant s % 5 (deterministic, round-robin)
  - Sessions 0,5 → variant 0
  - Sessions 1,6 → variant 1
  - Sessions 2,7 → variant 2
  - Sessions 3,8 → variant 3
  - Sessions 4,9 → variant 4

### 5.3 Variant Encoding

Each variant at each FSM state includes session-correlated content:
- **notification_count**: variant_id * 33 (deterministic per variant)
- **items**: list of variant_id items (deterministic per variant)
- **session_token**: SHA-256 of session_id (deterministic per session)

This ensures:
1. DOM_before encodes variant → reveals session → determines variant_after
2. The mapping is deterministic within each session (no within-session noise)
3. Different sessions with same variant produce identical DOM (testable)

### 5.4 Trajectory Generation

- **N_TRAJECTORIES = 500** (increased from parent's 200 for power)
- **STEPS_PER_TRAJECTORY = 10**
- **Total transitions**: 5000
- **Session assignment**: random.Random(seed).choice(range(N_SESSIONS)) per trajectory
- **Session is constant within trajectory**: all 10 steps use the same session

### 5.5 Deterministic SPA (Level 0)

Same as parent: 1 DOM per state, no variants. 500 trajectories x 10 steps = 5000 transitions.

### 5.6 Independent Per-Step Noise SPA (Level 1)

Same as parent: DOM variants drawn independently per step using rng.randint(0, variant_count-1) for each DOM generation call. No session persistence. 500 trajectories x 10 steps = 5000 transitions.

## 6. DOM Representations

### 6.1 visible_text_hash
SHA-256 of visible text content (title, subtitle, form fields, buttons, navigation, variant encoding). Primary representation.

### 6.2 accessibility_tree_hash
SHA-256 of accessibility tree structure. Expected to be isomorphic to visible_text_hash in this FSM design (parent audit V4).

### 6.3 numeric_structural
Element count, tree depth, interactive density, form count. Expected PMI = 0.0 (invariant per FSM state regardless of variant, parent finding).

### 6.4 multi_feature_hash
SHA-256(visible_text_hash + numeric_structural elements). Expected to be isomorphic to visible_text_hash (numeric elements are invariant).

## 7. Measures

### 7.1 Primary Metric
- **conditional_pmi_K3**: I(S_next; DOM_before | URL, H_K=3) computed as weighted average across (URL, H_K) strata
- **permutation_test_bonferroni_p**: Bonferroni-corrected p-value from 1000-permutation test

### 7.2 Secondary Metrics
- conditional_pmi at K=1, K=2 for gradient analysis
- Action-history prediction accuracy P(S_next | URL, H_K) for K=1,2,3
- Determinism accuracy P(DOM_hash_next | DOM_hash_current, Action)
- Session-to-variant mapping verification (fraction of transitions with deterministic mapping)
- Representation isomorphism check (unique hash counts, 1-1 mapping verification)

### 7.3 Control Metrics
- **positive_control_random_labels**: PMI with random DOM labels on session-SPA non-deterministic strata
- **null_control_shuffled_labels**: PMI with shuffled DOM labels within strata on session-SPA non-deterministic strata
- **determinism_control**: accuracy on deterministic SPA (= 1.0 expected) and session-SPA (< 1.0 expected)
- **data_quality**: min_transitions >= 500
- **session_mapping_verification**: fraction of transitions with deterministic session→variant mapping (> 0.95)

## 8. Null Models

### 8.1 Shuffle Null (Permutation Test)
Within each (URL, ActionHistory_K) stratum, permute DOM_before labels 1000 times. Compute PMI for each permutation. The permutation distribution gives the null distribution of PMI under the hypothesis that DOM_before is independent of DOM_after given (URL, H_K).

### 8.2 Frequency Null
Predict next state from marginal distribution P(S_next). Expected accuracy: 1/5 = 20% for 5 FSM states.

### 8.3 Random Label Null
Replace DOM_before labels with random hashes independent of all variables. PMI should be ≈ 0.

## 9. Statistical Tests

### 9.1 Primary Test
- Conditional PMI at K=3 for each representation
- One-sided test: PMI > 0
- 1000 permutations per (representation, K) stratum
- Bonferroni correction: alpha = 0.05 / 12 = 0.00417 (4 representations x 3 K values)

### 9.2 Deterministic Baseline
- PMI at K=3 for deterministic SPA
- Expected: PMI = 0.0 (within noise)
- Verification: |PMI| < 0.05

### 9.3 K-Value Gradient
- Paired comparison: PMI(K=1) vs PMI(K=2) vs PMI(K=3)
- Expected: PMI(K=1) >= PMI(K=2) >= PMI(K=3)

### 9.4 Representation Isomorphism
- Compare PMI across visible_text_hash, accessibility_tree_hash, multi_feature_hash
- Expected: coefficient of variation < 0.1 across hash representations

## 10. Controls

### 10.1 Positive Control (Random Labels on Non-Deterministic Strata)
- Compute on session-SPA non-deterministic strata (NOT deterministic strata, per parent audit V3)
- Random labels: SHA-256(random_counter) independent of session/state/action
- Expected PMI ≈ 0.0
- Pass: |PMI| < 3 * std(permuted PMI)

### 10.2 Null Control (Shuffled Labels on Non-Deterministic Strata)
- Compute on session-SPA non-deterministic strata
- Shuffle DOM_before labels within (URL, H_K) strata
- Expected PMI ≈ 0.0
- Pass: |mean shuffled PMI| < 3 * std(shuffled PMI)

### 10.3 Determinism Control
- Deterministic SPA: P(DOM_hash_next | DOM_hash_current, Action) accuracy = 1.0
- Session-SPA: accuracy < 1.0 (variants create observation non-determinism)

### 10.4 Session Mapping Verification
- For each (session, FSM_state) pair, verify DOM variant is deterministic
- Report fraction of transitions violating deterministic mapping
- Pass: > 95% deterministic

### 10.5 Independent Noise Baseline
- Independent per-step noise SPA: PMI ≈ 0.0 at K=3, Bonferroni p ≥ 0.00417
- Confirms pipeline distinguishes correlated from independent non-determinism

## 11. Validity Threats

### 11.1 Session-Variant Aliasing
With 10 sessions and 5 variants (2 sessions per variant), DOM_before reveals session only to the level of 2 candidate sessions. If both sessions with same variant produce identical DOM, variant_before does not distinguish them. However, variant_before still determines variant_after (both map to same variant), so PMI should be positive. Mitigation: report unique variant counts per session.

### 11.2 Finite-Sample PMI Estimation
With 5000 transitions across ~20 strata (5 URLs x 4 H_K patterns), average ~250 transitions per stratum. PMI estimation is reliable at this scale. Mitigation: report confidence intervals.

### 11.3 Action-History Sufficiency
At K=3, action history fully predicts FSM state (linear FSM). DOM_before cannot add information about FSM state. However, DOM_before adds information about variant (which session), which is not predicted by action history. This is the discriminating test.

### 11.4 Synthetic-to-Real Gap
Locally-hosted Express SPAs with deterministic session-to-variant mapping may not reflect production SPAs with complex session management (OAuth, database-backed sessions, concurrent users). This is a conservative controlled test.

### 11.5 Representation Isomorphism
Hash-based representations (visible_text_hash, accessibility_tree_hash, multi_feature_hash) may be 1-1 in this FSM design (parent audit V4). Richer representations (computed CSS, visual layout, ARIA roles) are not tested. Claim ceiling bounded to hash-based representations.

### 11.6 Multiple Comparisons
12 comparisons (4 reps x 3 K values) with Bonferroni correction is conservative. The primary test is K=3 with visible_text_hash; other comparisons are secondary. Report both corrected and uncorrected p-values.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST
If ALL of:
1. conditional_pmi_K3 > 0.0 with Bonferroni-corrected permutation p < 0.00417 on visible_text_hash (primary) AND mean PMI across representations at K=3 > 0.05 bits
2. positive_control_random_labels passes on session-SPA non-deterministic strata
3. determinism_control: deterministic SPA accuracy = 1.0 AND session-SPA accuracy < 1.0
4. data_quality: >= 500 valid transitions
5. session_mapping_verification: > 95% deterministic

### 12.2 FALSIFIED-IN-SETTING
If ANY of:
1. conditional_pmi_K3 <= 0.0 OR Bonferroni p >= 0.00417 on ALL 4 representations
2. Mean PMI across representations at K=3 <= 0.05 bits
3. Positive control fails on non-deterministic strata
4. Determinism check fails (session-SPA accuracy = 1.0)

### 12.3 MEASUREMENT_INVALID
If:
1. < 500 valid transitions
2. Session-to-variant mapping verification < 95% deterministic
3. Pipeline errors prevent computation

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)
- DOM_before predicts DOM_after through persistent session state
- The parent's falsification of independent per-step noise does NOT generalize to correlated non-determinism
- Specific condition identified: persistent server-side session state creates DOM-encodable dynamics
- SPIDER should capture DOM features when session-like state is present
- Physics lane should investigate session-dependent DOM as a validated observation substrate

### 13.2 Negative Result (FALSIFIED-IN-SETTING)
- DOM hash features have no predictive value even with persistent session state
- DOM-hash path closed across ALL locally-hosted non-deterministic regimes
- Physics lane should move to network-response information theory (API payload structure, response headers, timing signatures)
- Product lane should not invest in DOM hash-based state tracking

### 13.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Generation**: Generate 3 SPA types (deterministic, independent-noise, session-correlated) with 5000 transitions each
2. **Session Mapping Verification**: Verify deterministic session→variant mapping for session-SPA
3. **Strata Construction**: Build (URL, ActionHistory_K) strata for K=1,2,3
4. **PMI Computation**: Compute conditional PMI for each (representation, K, SPA_type) combination
5. **Permutation Tests**: 1000 permutations per (representation, K) stratum on session-SPA non-deterministic data
6. **Bonferroni Correction**: Correct across 12 comparisons (4 reps x 3 K values)
7. **Controls**: Run positive control (random labels), null control (shuffled labels), determinism check, data quality check
8. **Deterministic Baseline**: Verify PMI=0 on deterministic SPA
9. **Independent Noise Baseline**: Verify PMI≈0 on independent per-step noise SPA
10. **Representation Isomorphism**: Check hash representation equivalence
11. **K-Value Gradient**: Compare PMI across K=1,2,3
12. **Decision**: Apply frozen decision rule

## 15. Analysis Code

Analysis will be implemented in Python using:
- `hashlib` for SHA-256 hashing
- `json` for data I/O
- `random` for session assignment and permutation tests
- `collections.Counter` for frequency counting
- `math` for log2 in PMI computation
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-PHYSICS-34846934524/` before execution.

## 16. Stable Identifiers for Downstream

### Metric IDs
- `conditional_pmi_K3`: primary metric, I(S_next; DOM_before | URL, H_K=3) at K=3
- `permutation_test_bonferroni_p`: Bonferroni-corrected permutation p-value
- `action_history_prediction_accuracy_K3`: P(S_next | URL, H_K=3) accuracy
- `determinism_accuracy`: P(DOM_hash_next | DOM_hash_current, Action)
- `session_mapping_verification_fraction`: fraction of transitions with deterministic session→variant

### Control IDs
- `positive_control_random_labels`: random DOM labels on non-deterministic strata
- `null_control_shuffled_labels`: shuffled DOM labels within strata
- `determinism_control`: deterministic SPA vs session-SPA accuracy comparison
- `data_quality`: min transitions per SPA type
- `session_mapping_verification`: session→variant determinism check
- `deterministic_baseline`: PMI on deterministic SPA
- `independent_noise_baseline`: PMI on independent per-step noise SPA

### Artifact IDs
- `raw_session_spa_data.json`: generated session-SPA transition data
- `raw_independent_noise_data.json`: generated independent per-step noise data
- `raw_deterministic_data.json`: generated deterministic SPA data
- `raw_analysis_results.json`: computed PMI, permutation tests, controls
- `generate_data.py`: data generation script
- `analyze.py`: analysis script

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.

## Appendix A: Expected PMI Calculation

With 10 sessions uniformly distributed, 5 variants (2 sessions per variant):

- H(variant_after | URL, H_K) = log2(5) = 2.32 bits (5 variants equally likely)
- H(variant_after | variant_before, URL, H_K) = 1.0 bit (variant_before narrows to 2 sessions, each producing one variant)
- I(variant_before; variant_after | URL, H_K) = 2.32 - 1.0 = 1.32 bits

This is a lower bound. If session distribution within strata is non-uniform, PMI could be higher. If some strata are dominated by a single session, PMI within those strata is 0, but the weighted average across strata should still be positive.

With 5000 transitions and ~250 per stratum, PMI estimation standard error ≈ 1/sqrt(250) ≈ 0.06 bits. The expected PMI (1.32 bits) is well above this noise floor.
