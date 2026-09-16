# EXP-PHYSICS-35040401992 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35040401992
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On locally-hosted Express SPAs with session-dependent API responses and a BRANCHING FSM (at least one state with >=2 outgoing actions and session-dependent transition probabilities) so that H(S_next|URL,H_K=3) > 0.2 bits, does network-response payload structure exhibit conditional PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125 and a discriminating positive control (non-zero perm_null_std)?

## 3. Motivation

The previous experiment (EXP-PHYSICS-34932344937) tested network-response PMI on a 5-state linear FSM. The linear FSM had a critical limitation: action-history at K=3 fully determines the next state (H=0), creating a ceiling effect where PMI must be zero regardless of response informativeness. However, the experiment revealed a strong positive signal at K=1 (BC PMI=0.386 bits, Bonferroni p=0.004) that network-response DOES carry predictive information when action-history is insufficient.

The correct next step is to test the same hypothesis on a **branching FSM** where:
- At least one state has >=2 outgoing actions
- Session-dependent transition probabilities ensure H(S_next|URL,H_K=3) > 0.2 bits
- This eliminates the ceiling effect while keeping the observation level (network-response) that already shows PMI when H>0

The parent handoff (carry_forward established) confirms:
- Network-response payload structure carries significant conditional PMI when action-history is insufficient (K=1, H=0.4 bits, BC PMI=0.386 bits)
- Linear FSM at K>=2 has H=0 (ceiling effect, not falsification of response informativeness)
- Bias-corrected PMI estimator is valid (observed - perm_mean)

This experiment directly tests the unknown: "Whether network-response PMI remains >0 at K=3 on a branching FSM where H(S_next|URL,H_K=3) > 0.2 bits".

## 4. Hypotheses

### H1: State-Dependent Response PMI on Branching FSM
On the state-dependent response condition, bias-corrected PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125.

### H2: Response-Condition Discrimination
State-dependent bias-corrected PMI > state-independent bias-corrected PMI by >= 0.05 bits, with paired permutation p < 0.05 across trajectories.

### H3: Positive Control
Session-randomized control yields bias-corrected PMI ≈ 0.0 within permutation noise on state-dependent non-deterministic strata, AND perm_null_std > 0 (non-zero null standard deviation).

### H4: Cardinality Bounded
On the state-dependent condition, |R| < 0.8 * N per stratum at K=3, avoiding the parent's |R| ≈ N degeneracy.

### H5: Determinism Check
Both conditions have P(Response_hash | FSM_state, session) accuracy = 1.0 — responses are deterministic. The difference is whether response encodes state information, not whether response is non-deterministic.

### H6: Ceiling Elimination
Conditional entropy H(S_next|URL, H_K=3) > 0.2 bits on the branching FSM, ensuring action-history does not fully determine the next state.

## 5. Experimental Conditions

### 5.1 Branching FSM Design

An Express server hosts a 3-state branching FSM with session-dependent transition probabilities:

**States**: {S0, S1, S2}
**Actions**: {advance, branch}
**Session parameter**: Each session has a hidden direction ∈ {left, right} (uniform random, independent per session)

**Transition rules** (deterministic given session direction):
- From S0:
  - advance → S1
  - branch → S2 if direction == 'left' else S1
- From S1:
  - advance → S2
  - branch → S0 if direction == 'left' else S2
- From S2:
  - advance → S0
  - branch → S1 if direction == 'left' else S0

**Branching property**: Every state has two outgoing actions (advance, branch). At every state, the branch action leads to two possible next states depending on session direction. For example, at S0 with branch: direction='left' → S2, direction='right' → S1. This ensures that even with full action history, the next state is not deterministic (entropy >0) whenever a branch action is taken.

**Conditional entropy analysis**: For a uniform action policy (50/50 advance/branch at each state):
- H(S_next | state, action=advance) = 0 bits (advance is deterministic regardless of direction)
- H(S_next | state, action=branch) = 1 bit (branch leads to 2 equally likely states)
- H(S_next | URL, H_K=3) = 0.5 × 0 + 0.5 × 1 = 0.5 bits

This exceeds the 0.2 bits threshold. The exact value depends on the action distribution in the generated data; the conditional entropy check (mandatory decision criterion) verifies this empirically.

**Why every state branches**: The key design choice is that from each state, the branch action maps left→next_state and right→prev_state (mod 3), ensuring two genuinely different next states. No self-loops exist. This maximizes the branching at every state.

### 5.2 State-Dependent Response Condition

- **Sessions**: 20 unique session IDs, each with a random direction (left/right)
- **API responses**: Each session gets a distinct response token (SHA-256(session_id)[:8]) embedded in a JSON body:
  ```json
  {"state_id": "S0", "step": 2, "session_token": "a1b2c3d4", "direction": "left", "items": [...]}
  ```
- **Response features**: state_id (3 values), step (10 values), session_token (20 values), direction (2 values), items list (state-dependent length)
- **Total unique response hashes**: ~60 (20 sessions × 3 states)

### 5.3 State-Independent Response Condition (Control)

Identical FSM and sessions, but API returns identical response regardless of state:
```json
{"state_id": "unknown", "step": 0, "session_token": "none", "direction": "unknown", "items": []}
```
- **Response features**: All values constant across states and sessions
- **Total unique response hashes**: 1
- **Expected PMI**: 0.0 (no state information in response)

### 5.4 Why This Comparison Is Decisive

The only difference between conditions is response content. If state-dependent responses yield PMI > state-independent responses, the response structure carries predictive information. This cannot be explained by:
- Session identity (both conditions have sessions)
- Action history (both conditions have identical action sequences)
- FSM structure (both conditions have identical FSMs)
- Estimator bias (bias correction applies to both)

## 6. Data Generation

### 6.1 Trajectory Generation

- 200 trajectories per condition (400 total)
- 10 steps per trajectory
- Actions chosen uniformly at random from the available action at each state (advance or branch)
- Session ID assigned uniformly at random from 20 sessions at trajectory start (independent random draw, NOT round-robin)
- Session direction fixed per session (left/right, uniform random)
- Seed = 42 for reproducibility

### 6.2 Response Generation

**State-dependent**: For each (session, state) pair, generate a response containing:
- `state_id`: the FSM state name (S0, S1, S2)
- `step`: step number within trajectory (1-10)
- `session_token`: SHA-256(session_id)[:8] (20 values)
- `direction`: session direction (left/right)
- `items`: list of length = step number (deterministic per step)

**State-independent**: For all (session, state) pairs, return:
- `state_id`: "unknown"
- `step`: 0
- `session_token`: "none"
- `direction`: "unknown"
- `items`: []

### 6.3 Response Hashing

Response hash = SHA-256(json.dumps(response_body, sort_keys=True))[:16]. This is the discretized observation for PMI computation.

## 7. Measures

### 7.1 Primary Metric

**Bias-corrected conditional PMI**:
- observed_pmi = plug-in PMI I(S_next; Response_before | URL, H_K) computed on actual data
- perm_mean = mean PMI across 1000 within-strata permutations of Response_before labels
- bias_corrected_pmi = observed_pmi - perm_mean

This isolates genuine predictive information from finite-sample bias.

### 7.2 Conditional MI Computation

For each (URL, H_K) stratum:
1. Count joint occurrences: n(r, s) = |{t ∈ stratum : R_before=r, S_next=s}|
2. Count marginals: n(r) = |{t ∈ stratum : R_before=r}|, n(s) = |{t ∈ stratum : S_next=s}|
3. Compute plug-in PMI: PMI(r,s) = log2(n(r,s) * N / (n(r) * n(s)))
4. Weighted PMI = Σ_r Σ_s (n(r,s)/N) * PMI(r,s)

### 7.3 Permutation Test

For each stratum:
1. Shuffle Response_before labels within the stratum (1000 times)
2. Recompute PMI for each shuffle
3. p_raw = fraction of shuffled PMIs >= observed PMI
4. p_bonferroni = min(p_raw * n_comparisons, 1.0)

### 7.4 Secondary Metrics

- Plug-in MI (uncorrected) for comparison with parent
- |R| per stratum (cardinality check)
- Action-history prediction accuracy at K=1,2,3
- Per-condition PMI at K=1 and K=3
- Stratum sizes and distribution
- Conditional entropy H(S_next|URL, H_K=3)

## 8. Null Models

### 8.1 Session-Randomized Control (Positive Control)

Replace each trajectory's session_id with a random session_id from a different trajectory. Response content still varies (same generation), but the session→response mapping is broken. Expected bias-corrected PMI ≈ 0. Additionally, perm_null_std must be > 0 (non-zero) to ensure discriminating power.

### 8.2 Shuffled Response Labels (Null Control)

Within each (URL, H_K) stratum, permute Response_before labels. Preserves marginal distributions but breaks R→S pairing. Expected bias-corrected PMI ≈ 0.

### 8.3 State-Independent Baseline

Same FSM and sessions, but response is constant. Expected PMI ≈ 0 (no state information). Provides within-experiment null.

## 9. Statistical Tests

### 9.1 Primary Test

- Bias-corrected PMI at K=3 on state-dependent condition
- One-sided: PMI > 0.05 bits
- Within-strata permutation test, 1000 permutations
- Bonferroni correction across 4 comparisons (2 conditions × 2 K values)
- Corrected alpha: 0.05 / 4 = 0.0125

### 9.2 Discrimination Test

- Paired permutation test: state-dependent PMI - state-independent PMI across trajectories
- One-sided: difference > 0.05 bits
- 1000 permutations of condition labels within matched trajectory pairs
- Uncorrected alpha: 0.05 (single comparison)

### 9.3 Cardinality Check

- Report |R| per stratum at K=3
- Pass criterion: |R| < 0.8 * N (avoiding parent's |R| ≈ N degeneracy)

### 9.4 Conditional Entropy Check

- Compute H(S_next|URL, H_K=3) on the generated data
- Pass criterion: H > 0.2 bits (ceiling eliminated)

## 10. Controls

### 10.1 Positive Control (Session-Randomized)

- Randomize session assignment across trajectories
- Response→state mapping broken; PMI should be ≈ 0
- Pass: |session-randomized PMI| < 3 * std(permuted PMI) AND perm_null_std > 0

### 10.2 Null Control (Shuffled Labels)

- Permute response labels within strata
- Breaks R→S pairing; PMI should be ≈ 0
- Pass: |mean shuffled PMI| < 3 * std(shuffled PMI)

### 10.3 State-Independent Baseline

- Identical FSM, constant responses
- PMI should be 0.0 exactly
- Pass: bias-corrected PMI = 0.0

### 10.4 Determinism Check

- Both conditions: P(Response_hash | FSM_state, session) = 1.0
- Responses are deterministic; difference is state-encoding, not non-determinism

## 11. Validity Threats

### 11.1 Action-History Sufficiency (Ceiling Effect)

The previous linear FSM had H=0 at K=3, making PMI identically zero. The branching FSM ensures H>0.2 bits at K=3 (analytically ~0.5 bits for uniform action policy). **Mitigation**: Conditional entropy check is a mandatory decision criterion. If H ≤ 0.2 bits, experiment is MEASUREMENT_INVALID.

### 11.2 Cardinality Degeneracy Risk

With 20 sessions × 3 states = 60 unique response hashes and ~714 transitions per stratum at K=3, |R|/N ≈ 60/714 = 0.084, well below the 0.8 threshold. **Mitigation**: Cardinality check is a mandatory decision criterion.

### 11.3 Synthetic-to-Real Gap

Locally-hosted Express SPA with deterministic session-to-state mapping may not reflect production SPAs. **Mitigation**: This is a controlled validation experiment. If the pipeline cannot detect known structure in controlled data, it cannot be trusted on real data.

### 11.4 FSM Complexity

The 3-state branching FSM is simple but ensures H>0.2 bits. More complex FSMs could yield different results. **Mitigation**: The branching property (>=2 outgoing actions per state, session-dependent selection) is the key feature, not the specific state count. The design is minimal but sufficient to test the hypothesis.

### 11.5 Sample Size

With 200 trajectories × 10 steps = 2000 transitions per condition, and ~714 per stratum at K=3, we have adequate power to detect PMI > 0.05 bits (effect size > 0.05 bits with perm_std ≈ 0.005 gives z > 10). Smaller effects may be missed but the 0.05 bits threshold is the minimum practically meaningful effect.

### 11.6 Direction Leakage via Session Token

The state-dependent response includes `direction` and `session_token` fields. The session_token is deterministic per session, so a PMI detector could use session_token to infer direction and thus predict transitions, even without genuine state information in the response body. **Mitigation**: This is by design — the response DOES carry state-relevant information (direction determines transitions). The state-independent control removes all session-varying fields, providing the clean comparison. The question is whether response structure carries predictive information, not whether it carries information through a specific mechanism.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST

If ALL of:
1. H(S_next|URL, H_K=3) > 0.2 bits (ceiling eliminated)
2. Bias-corrected PMI on state-dependent condition at K=3 > 0.05 bits, Bonferroni-corrected p < 0.0125
3. State-dependent PMI > state-independent PMI by >= 0.05 bits, paired permutation p < 0.05
4. Positive control passes (session-randomized PMI ≈ 0 AND perm_null_std > 0)
5. Determinism check passes (both conditions accuracy = 1.0)
6. >= 500 valid transitions per condition
7. Cardinality check: |R| < 0.8 * N per stratum at K=3

### 12.2 FALSIFIED-IN-SETTING

If ANY of:
1. Bias-corrected PMI <= 0.05 on state-dependent condition at K=3
2. State-dependent PMI not > state-independent PMI (difference < 0.05 bits or p >= 0.05)
3. Both conditions have PMI ≈ 0 (no response informativeness in either condition)

### 12.3 MEASUREMENT_INVALID

If:
1. Controls fail (positive control PMI ≈ 0 but raw PMI ≈ H(S), cardinality degeneracy, perm_null_std = 0)
2. Data quality insufficient (< 500 transitions per condition)
3. Pipeline errors prevent computation
4. Cardinality check fails (|R| > 0.8 * N per stratum)
5. Conditional entropy H(S_next|URL, H_K=3) ≤ 0.2 bits (ceiling not eliminated)

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)

- Network-response payload structure carries predictive information about Web state transitions even when action-history is insufficient (entropy >0.2 bits)
- SPIDER should capture API response bodies and headers as observation features
- The response-level observation avoids DOM hash cardinality degeneracy and linear FSM ceiling effects
- Opens a new observation layer for C-WEB-DYNAMICS beyond DOM structure
- Justifies further exploration with richer response features (headers, timing, multi-endpoint)

### 13.2 Negative Result (FALSIFIED-IN-SETTING)

- Network-response structure has no conditional PMI beyond action-history memory even when action-history is insufficient
- Locally-hosted testable path for C-WEB-DYNAMICS is closed across ALL observation levels
- Physics lane should either:
  - (a) Move to production infrastructure with genuine non-deterministic state transitions
  - (b) Abandon PMI-based conditional information approach, investigate alternative physics mechanisms

### 13.3 Invalid Result (MEASUREMENT_INVALID)

- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 14. Analysis Plan

1. **Data Generation**: Generate 4000 transitions (200 trajectories × 10 steps × 2 conditions)
2. **Response Hashing**: SHA-256(json.dumps(response_body))[:16] for each response
3. **Stratification**: Build strata by (URL, H_K) for K=1,2,3
4. **MI Computation**: Plug-in PMI per stratum, weighted average
5. **Bias Correction**: Permutation null (1000 perms per stratum), subtract perm_mean from observed
6. **Permutation Tests**: Within-strata shuffling, Bonferroni correction
7. **Discrimination Test**: Paired permutation on state-dependent vs state-independent PMI difference
8. **Controls**: Session-randomized, shuffled labels, state-independent baseline, determinism check
9. **Cardinality Check**: Report |R| per stratum
10. **Conditional Entropy**: Compute H(S_next|URL, H_K=3) to verify ceiling elimination
11. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for permutation tests
- `hashlib` for response hashing
- `json` for response parsing
- `collections.Counter` for frequency counting
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-PHYSICS-35040401992/` before execution.

## 16. Pre-registered Expectations

From prior Physics work:
- Network-response PMI at K=1 on linear FSM was 0.386 bits (bias-corrected)
- Linear FSM at K=3 had H=0 (ceiling effect, not falsification)
- Branching FSM should have H>0.2 bits at K=3 (analytically ~0.5 bits for uniform policy), eliminating ceiling
- State-dependent > state-independent is the cleanest causal test
- Bias-corrected estimator (observed - perm_mean) should give valid effect sizes

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
