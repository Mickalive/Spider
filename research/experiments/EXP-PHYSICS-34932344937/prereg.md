# EXP-PHYSICS-34932344937 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34932344937
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-15
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

On locally-hosted Express SPAs with session-dependent API responses, does network-response payload structure exhibit conditional PMI I(S_next; Response_before | URL, H_K=3) > 0 with Bonferroni-corrected permutation p < 0.00417?

## 3. Motivation

The DOM-hash observation path for C-WEB-DYNAMICS is now closed across all locally-hosted testable regimes:

1. **Deterministic SPAs**: FALSIFIED (EXP-PHYSICS-34724244876). DOM hash adds no PMI when action-history is sufficient (K=3). PMI = 0.0.

2. **Independent per-step observation noise**: FALSIFIED (EXP-PHYSICS-34764605162). DOM features have no conditional PMI when observation noise is independent across steps. PMI ≈ 0.003, Bonferroni p = 1.0.

3. **Correlated non-determinism (session-dependent)**: MEASUREMENT_INVALID (EXP-PHYSICS-34846934524). PMI = 3.319 bits looked significant but was **artefactual**: it equals H(S|URL,H_K) = log2(10) for 10 session-specific DOM hashes, and random DOM_before labels produce the same PMI (3.318 bits), proving the plug-in MI estimator degenerates when |R| ≈ N per stratum.

The parent audit (V1, V2, V8) identified three specific problems:
- **Cardinality degeneracy**: The plug-in MI estimator saturates at H(S) when the number of unique response values |R| approaches the stratum size N. DOM hashes are high-cardinality (SHA-256 outputs), making this inevitable.
- **Control design flaw**: The positive control randomized DOM_before labels instead of session assignment, so it could not detect the identity function DOM_before(session_id) → DOM_after(session_id).
- **Target misoperationalization**: PMI measured prediction of next DOM hash (which contains session token), not next FSM state.

This experiment tests **network-response payload structure** as an orthogonal observation level that avoids all three problems:

1. **Low-cardinality features**: API response bodies are JSON objects with discrete fields (state_id, step_count, status_code), not SHA-256 hashes. |R| is small by construction.

2. **Session-randomized control**: The positive control randomizes session_id assignment (breaking the session→response mapping), not response labels. This correctly tests whether the response→state channel carries information.

3. **State-targeted MI**: The PMI target is next FSM state (5 values), not next DOM hash (50 values). This measures genuine state-transition prediction, not observation identity.

The within-experiment comparison (state-dependent vs state-independent responses) provides the cleanest causal test: identical FSM, identical sessions, only response content varies.

## 4. Hypotheses

### H1: State-Dependent Response PMI
On the state-dependent response condition, bias-corrected PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125.

### H2: Response-Condition Discrimination
State-dependent bias-corrected PMI > state-independent bias-corrected PMI by >= 0.05 bits, with paired permutation p < 0.05 across trajectories.

### H3: Positive Control
Session-randomized control yields bias-corrected PMI ≈ 0.0 within permutation noise on state-dependent non-deterministic strata.

### H4: Cardinality Bounded
On the state-dependent condition, |R| < 0.8 * N per stratum at K=3, avoiding the parent's |R| ≈ N degeneracy.

### H5: Determinism Check
Both conditions have P(Response_hash | FSM_state, session) accuracy = 1.0 — responses are deterministic. The difference is whether response encodes state information, not whether response is non-deterministic.

## 5. Experimental Conditions

### 5.1 State-Dependent Response Condition

An Express server hosts a 5-state linear FSM with session persistence:

- **FSM**: landing → form_s1 → form_s2 → review → complete → landing (cyclic)
- **Actions**: begin, advance, finalize, submit, restart (one per state)
- **Sessions**: 10 unique session IDs, randomly assigned per trajectory
- **API responses**: Each session gets a distinct response token (SHA-256(session_id)[:8]) embedded in a JSON body:
  ```json
  {"state_id": "form_s1", "step": 2, "session_token": "a1b2c3d4", "items": [...]}
  ```
- **Response features**: state_id (5 values), step (5 values), session_token (10 values), items list (state-dependent length)
- **Total unique response hashes**: ~50 (10 sessions × 5 states)

### 5.2 State-Independent Response Condition (Control)

Identical FSM and sessions, but API returns identical response regardless of state:

```json
{"state_id": "unknown", "step": 0, "session_token": "none", "items": []}
```

- **Response features**: All values constant across states and sessions
- **Total unique response hashes**: 1
- **Expected PMI**: 0.0 (no state information in response)

### 5.3 Why This Comparison Is Decisive

The only difference between conditions is response content. If state-dependent responses yield PMI > state-independent responses, the response structure carries predictive information. This cannot be explained by:
- Session identity (both conditions have sessions)
- Action history (both conditions have identical action sequences)
- FSM structure (both conditions have identical FSMs)
- Estimator bias (bias correction applies to both)

## 6. Data Generation

### 6.1 Trajectory Generation

- 200 trajectories per condition (400 total)
- 10 steps per trajectory
- Actions chosen uniformly at random from the available action at each state
- Session ID assigned uniformly at random from 10 sessions at trajectory start
- Seed = 42 for reproducibility

### 6.2 Response Generation

**State-dependent**: For each (session, state) pair, generate a response containing:
- `state_id`: the FSM state name (5 values)
- `step`: step number within trajectory (1-10)
- `session_token`: SHA-256(session_id)[:8] (10 values)
- `items`: list of length = step number (deterministic per step)

**State-independent**: For all (session, state) pairs, return:
- `state_id`: "unknown"
- `step`: 0
- `session_token`: "none"
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

## 8. Null Models

### 8.1 Session-Randomized Control (Positive Control)

Replace each trajectory's session_id with a random session_id from a different trajectory. Response content still varies (same generation), but the session→response mapping is broken. Expected bias-corrected PMI ≈ 0.

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

## 10. Controls

### 10.1 Positive Control (Session-Randomized)

- Randomize session assignment across trajectories
- Response→state mapping broken; PMI should be ≈ 0
- Pass: |session-randomized PMI| < 3 * std(permuted PMI)

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

### 11.1 Action-History Sufficiency

On the 5-state linear FSM, action-history at K=3 predicts FSM state with near-perfect accuracy. If FSM state is already determined by action-history, response cannot add predictive value for FSM state prediction. **Mitigation**: This is the intended strong null — if response cannot add information beyond action-history, it is not a useful observation substrate. The within-experiment comparison (state-dependent vs state-independent) still discriminates: state-dependent should have higher PMI even if absolute PMI is small.

### 11.2 Cardinality Degeneracy Risk

With 10 sessions × 5 states = 50 unique response hashes and ~714 transitions per stratum at K=3, |R|/N ≈ 50/714 = 0.07, well below the 0.8 threshold. This avoids the parent's degeneracy. **Mitigation**: Cardinality check is a mandatory decision criterion.

### 11.3 Synthetic-to-Real Gap

Locally-hosted Express SPA with deterministic session-to-state mapping may not reflect production SPAs. **Mitigation**: This is a controlled validation experiment. If the pipeline cannot detect known structure in controlled data, it cannot be trusted on real data.

### 11.4 FSM Linearity

The 5-state linear FSM has deterministic transitions: each state has exactly one outgoing action. This means action-history fully determines FSM state. The experiment tests whether response carries information about the next state *given* URL and action-history — if action-history already determines the next state, response information is redundant by definition. **Mitigation**: The within-experiment comparison still discriminates: state-dependent responses yield PMI = H(S_next|URL,H_K) (response reveals current state), while state-independent responses yield PMI ≈ 0 (no state information). The difference measures response informativeness.

### 11.5 Sample Size

With 200 trajectories × 10 steps = 2000 transitions per condition, and ~714 per stratum at K=3, we have adequate power to detect PMI > 0.05 bits (effect size > 0.05 bits with perm_std ≈ 0.005 gives z > 10). Smaller effects may be missed but the 0.05 bits threshold is the minimum practically meaningful effect.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST

If ALL of:
1. Bias-corrected PMI on state-dependent condition at K=3 > 0.05 bits, Bonferroni-corrected p < 0.0125
2. State-dependent PMI > state-independent PMI by >= 0.05 bits, paired permutation p < 0.05
3. Positive control passes (session-randomized PMI ≈ 0)
4. Determinism check passes (both conditions accuracy = 1.0)
5. >= 500 valid transitions per condition
6. Cardinality check: |R| < 0.8 * N per stratum at K=3

### 12.2 FALSIFIED-IN-SETTING

If ANY of:
1. Bias-corrected PMI <= 0.0 on state-dependent condition at K=3
2. State-dependent PMI not > state-independent PMI (difference < 0.05 bits or p >= 0.05)
3. Both conditions have PMI ≈ 0 (no response informativeness in either condition)

### 12.3 MEASUREMENT_INVALID

If:
1. Controls fail (positive control PMI ≈ 0 but raw PMI ≈ H(S), cardinality degeneracy)
2. Data quality insufficient (< 500 transitions per condition)
3. Pipeline errors prevent computation
4. Cardinality check fails (|R| > 0.8 * N per stratum)

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)

- Network-response payload structure carries predictive information about Web state transitions
- SPIDER should capture API response bodies and headers as observation features
- The response-level observation avoids DOM hash cardinality degeneracy
- Opens a new observation layer for C-WEB-DYNAMICS
- Justifies further exploration with richer response features (headers, timing, multi-endpoint)

### 13.2 Negative Result (FALSIFIED-IN-SETTING)

- Network-response structure has no conditional PMI beyond action-history memory
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
10. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for permutation tests
- `hashlib` for response hashing
- `json` for response parsing
- `collections.Counter` for frequency counting
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-PHYSICS-34932344937/` before execution.

## 16. Pre-registered Expectations

From prior Physics work:
- DOM-hash PMI was artefactual (cardinality degeneracy) — network-response should not exhibit this
- Bias-corrected estimator (observed - perm_mean) should give valid effect sizes
- State-dependent > state-independent is the cleanest causal test
- Action-history at K=3 on linear FSM predicts state perfectly — response adds information only if it reveals current state

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
