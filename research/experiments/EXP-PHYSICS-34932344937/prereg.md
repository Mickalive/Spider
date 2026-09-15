# EXP-PHYSICS-34932344937 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-34932344937
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-15
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-PHYSICS-34846934524 (MEASUREMENT_INVALID, DOM-hash cardinality degeneracy)

## 2. Scientific Question

On locally-hosted Express SPAs with correlated non-determinism, does network-response payload structure (API response bodies, headers, timing signatures) exhibit conditional PMI I(S_next; Response_before | URL, H_K=3) > 0 with Bonferroni-corrected permutation p < 0.00556?

This is an orthogonal observation level that avoids DOM hash cardinality degeneracy (parent audit V1) and session-token identity leakage (parent audit V8).

## 3. Motivation

### 3.1 Parent Failure Summary

EXP-PHYSICS-34846934524 tested DOM structural features for conditional PMI on session-correlated SPAs. The experiment was MEASUREMENT_INVALID due to:

- **V1 (Estimator cardinality degeneracy)**: Plug-in PMI estimator degenerated when |R| ≈ N per stratum. PMI = 3.319 bits equaled H(S_next|URL,H_K) = log2(10) = 3.3219 for 10 session-specific DOM hashes. Random DOM_before labels gave identical PMI (3.317 bits), proving any unique-valued R gives I=H(S) regardless of dependence.
- **V8 (Identity leakage)**: Session token SHA256(session_id)[:16] embedded in DOM made DOM_before a perfect session identifier. PMI measured identity function DOM_before(session_id) → DOM_after(session_id), not predictive Web dynamics.
- **V2 (Control failure)**: Positive and null controls failed because they were designed for independent-noise SPAs, not session-correlated SPAs.
- **V4 (Target misoperationalization)**: Target was DOM hash (observation), not FSM state. Action-history predicting DOM hash is different from predicting FSM state.

### 3.2 Why Network-Response Is Different

Network-response payload structure is an orthogonal observation level that may avoid the parent's problems:

1. **Lower cardinality**: API response bodies are structured JSON with fixed schemas. Distinct responses ≈ N_sessions (10-20), not N_sessions × N_states (50) as with DOM hashes. This reduces |R| relative to N, mitigating cardinality degeneracy.
2. **No session token embedding**: Response bodies contain structured data (item counts, greetings, data arrays) that varies by session but does NOT encode session identity. This avoids the trivial identity function.
3. **Genuine predictive structure**: Response content predicts DOM_after through the shared session variable, not through identity leakage. The prediction is: response content → session → DOM_after, which is a genuine information channel.
4. **Bias-corrected estimator**: Using observed - perm_mean instead of plug-in PMI avoids the cardinality degeneracy.

### 3.3 What This Experiment Tests

The experiment asks: does API response body content predict the next DOM observation through the shared latent session variable, after bias correction?

If yes → network-response payload structure is a valid observation level for C-WEB-DYNAMICS.
If no → both DOM-hash AND network-response paths are closed locally, forcing a lane pivot.

## 4. Hypotheses

### H1: Bias-Corrected PMI > 0
The bias-corrected conditional PMI I(Response_body; DOM_after | URL, H_K=3) > 0.0 with Bonferroni-corrected permutation p < 0.00556 on >= 1/3 response representations at K=3. Mean bias-corrected PMI across representations at K=3 > 0.01 bits.

### H2: Positive Control
Session-randomized PMI < 0.5 × observed PMI (randomizing sessions reduces PMI by >50%).

### H3: Determinism Check
Deterministic SPA: determinism accuracy = 1.0. Session-SPA: accuracy < 1.0. Independent noise: accuracy < 1.0.

### H4: Response Representation Distinctness
Response representations (body_hash, body_structure, headers_hash) are NOT isomorphic (unlike DOM hash representations which were 1-1 per parent audit V4). Different representations capture different aspects of response variation.

## 5. Data Generation

### 5.1 SPA Infrastructure

Locally-hosted Express server returning JSON API responses. Same 5-state linear FSM as parent:
- landing → form_s1 (action: begin)
- form_s1 → form_s2 (action: advance)
- form_s2 → review (action: finalize)
- review → complete (action: submit)
- complete → landing (action: restart)

### 5.2 API Response Structure

Each state has a base JSON response template. Session-dependent fields vary by session_id:

```json
{
  "state": "<fsm_state>",
  "items": ["item_<variant>_<i>" for i in range(variant)],
  "total": <variant * 33>,
  "greeting": "Welcome session_<session_id>",
  "timestamp": <step_number>,
  "metadata": {"variant": <variant>, "step": <step_number>}
}
```

**CRITICAL**: The response body does NOT contain session token (SHA-256 of session_id or similar hex string > 16 chars). The `greeting` field contains `session_<session_id>` as a human-readable label, NOT a cryptographic hash. This avoids the parent's identity leakage (audit V8).

### 5.3 Three SPA Types

1. **Deterministic (Level 0)**: Same response for each state across all sessions. variant=0 for all sessions. No session-dependent fields.
2. **Independent noise (Level 1)**: Response variant drawn independently per step (no session persistence). 3 variants per state.
3. **Session-correlated (Level 2)**: Persistent session_id determines response variant at each state. variant = session_id % N_VARIANTS. 10 sessions, 5 variants (2 sessions per variant).

### 5.4 Session Configuration

- N_SESSIONS = 10 (session_id ∈ {0, 1, ..., 9})
- N_VARIANTS = 5 (variant = session_id % 5)
- Session-to-variant mapping: deterministic (same session always gets same variant at same state)
- Session assignment: random per trajectory (uniform over 10 sessions)

### 5.5 Sample Size

- 500 trajectories × 10 steps = 5000 transitions per SPA type
- 3 SPA types × 5000 = 15000 total transitions
- 80/20 train/test split: 4000 train, 1000 test per SPA type

### 5.6 Random Seeds

- Base seed: 42 (for trajectory generation)
- Per-trajectory seed: 42 + traj_id (deterministic across processes)
- Permutation test seed: 42 (for reproducibility)

## 6. Response Representations

### 6.1 Response Body Hash (response_body_hash)
SHA-256 of the full JSON response body (serialized with sorted keys). This captures all variation in response content.

### 6.2 Response Body Structure (response_body_structure)
SHA-256 of the JSON schema: sorted keys, value types, nesting depth. This captures structural variation without content variation (e.g., same schema with different values).

### 6.3 Response Headers Hash (response_headers_hash)
SHA-256 of response headers (Content-Type, Cache-Control, X-Session-Variant). Excludes session-specific headers that might encode session identity.

### 6.4 Target: DOM Observation (S_next)
visible_text_hash of DOM_after (next DOM observation), consistent with parent framework. This is the "next state" that the response is supposed to predict.

## 7. Measures

### 7.1 Bias-Corrected Conditional PMI

For each (representation, K) stratum:
1. Compute raw PMI using plug-in estimator within each (URL, ActionHistory_K) stratum
2. Weight by stratum size: weighted_PMI = Σ (n_h / N) × stratum_PMI
3. Compute permutation null: shuffle entire transitions within strata, recompute PMI
4. Bias-corrected PMI = raw_PMI - perm_mean_PMI

### 7.2 Permutation Test
1000 permutations per (representation, K) stratum. Shuffle entire transitions within (URL, ActionHistory_K) strata. This correctly breaks the R→S pairing while preserving stratum structure (parent audit methodology).

### 7.3 Action-History Prediction
Accuracy of predicting S_next from ActionHistory alone: P(S_next | URL, H_K). For each stratum, predict the most frequent next DOM hash. If action-history alone achieves high accuracy, response cannot add predictive value.

### 7.4 Determinism Check
P(Response_hash | DOM_hash_current, Action). For each (DOM_before, Action) pair, check if response hash is deterministic. Deterministic SPA: accuracy = 1.0. Session-SPA: accuracy < 1.0 (response varies by session). Independent noise: accuracy < 1.0.

## 8. Null Models

### 8.1 Shuffle Null
Permute entire transitions within (URL, ActionHistory_K) strata. Expected bias-corrected PMI ≈ 0.

### 8.2 Frequency Null
Predict next DOM hash from marginal distribution P(S_next). Expected accuracy: 1/|S| where |S| is the number of distinct DOM hashes.

### 8.3 Session-Randomized Null
Randomize session_id assignment across trajectories (break session→response mapping). Expected bias-corrected PMI < 0.5 × observed PMI.

## 9. Controls

### 9.1 Positive Control (Session-Randomized)
Randomize session_id assignment (break session→response mapping). Compute bias-corrected PMI on randomized data.
PASS criterion: session-randomized PMI < 0.5 × observed PMI (randomizing sessions reduces PMI by >50%).
This tests whether the PMI is driven by session→response correlation rather than estimator bias.

### 9.2 Null Control (Shuffled Responses)
Shuffle response_body labels within (URL, ActionHistory_K) strata. Compute bias-corrected PMI.
PASS criterion: |shuffled PMI| < 3 × std(shuffled PMI) (shuffled PMI is within noise of zero).

### 9.3 Determinism Control
Deterministic SPA: determinism accuracy = 1.0. Session-SPA: accuracy < 1.0. Independent noise: accuracy < 1.0.
PASS criterion: all three conditions hold.

### 9.4 Data Quality Control
>= 500 valid transitions per SPA type.
PASS criterion: min_transitions >= 500.

### 9.5 Session Mapping Verification
For each session, verify that API response body at each FSM state is deterministic (same response every time).
PASS criterion: > 95% of (session, state) pairs are deterministic.

### 9.6 Response Body No-Token Verification
Verify that no response body field matches pattern 'session_*' or contains hex strings > 16 chars.
PASS criterion: 0 violations.

## 10. Validity Threats

### 10.1 Cardinality Degeneracy (Addressing Parent V1)
Network-response payloads have lower cardinality than DOM hashes:
- DOM hashes: N_sessions × N_states = 10 × 5 = 50 distinct hashes
- Response bodies: N_variants = 5 distinct responses per state (10 sessions → 5 variants via %5)
- |R| = 5 per stratum vs N ≈ 714 per stratum (K=3)
- Bias: (|R|-1)(|S|-1)/(2N ln2) ≈ 4×9/(2×714×0.693) ≈ 0.036 (much smaller than parent's 0.085)

The bias-corrected estimator (observed - perm_mean) further reduces this bias.

### 10.2 Session Token Leakage (Addressing Parent V8)
Response bodies do NOT contain session tokens (SHA-256 of session_id or similar). The `greeting` field contains `session_<session_id>` as a human-readable label, not a cryptographic hash. This avoids the trivial identity function.

However: if the greeting field uniquely identifies the session (10 sessions → 10 distinct greetings), the response body might still carry session identity information through the greeting. The bias-corrected PMI should still be > 0 if the greeting is the only session-identifying field, but the interpretation would be: "response body predicts DOM_after through session identity in the greeting field."

Mitigation: The response body also contains structured data (items, total, metadata) that varies by session. The body_structure representation captures structural variation without content, reducing the impact of greeting identity.

### 10.3 Synthetic-to-Real Gap
Locally-hosted Express SPAs with deterministic session-to-variant mapping may not reflect production SPAs with complex session management. Claim ceiling bounded to this synthetic setting.

### 10.4 Deterministic FSM
The FSM is linear and deterministic. S_next is fully determined by S_current and action. Response content cannot add predictive value for FSM state prediction beyond action history.

However: the target is DOM_after (observation), not FSM state (abstract). DOM_after varies by session (via session-dependent content), so response content may predict DOM_after through the session variable even though FSM transitions are deterministic.

### 10.5 Response Body Greeting Identity
The greeting field "Welcome session_<session_id>" uniquely identifies the session (10 sessions → 10 distinct greetings). This means response_body_hash has |R| = 10 per state, not 5. The body_structure representation (SHA-256 of JSON schema) has |R| = 1 (same schema for all sessions), which should have PMI ≈ 0.

### 10.6 Multiple Comparisons
9 comparisons (3 reps × 3 K values). Bonferroni alpha = 0.05/9 ≈ 0.00556.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Bias-corrected PMI > 0.0 with Bonferroni-corrected permutation p < 0.00556 on >= 1/3 response representations at K=3 AND mean bias-corrected PMI across representations at K=3 > 0.01 bits
2. Positive control passes (session-randomized PMI < 0.5 × observed PMI)
3. Determinism check passes (det SPA = 1.0, session SPA < 1.0, independent < 1.0)
4. >= 500 valid transitions per SPA type
5. Session mapping > 95% deterministic
6. No pipeline errors

### 11.2 FALSIFIED-IN-SETTING
If ANY of:
1. Bias-corrected PMI ≤ 0.0 or non-significant on ALL representations at K=3 (after Bonferroni correction)
2. Mean bias-corrected PMI across representations at K=3 ≤ 0.01 bits

### 11.3 MEASUREMENT_INVALID
If:
1. Controls fail (positive, determinism, data quality, session mapping)
2. Pipeline errors prevent computation
3. Response body contains session tokens (violating no-token verification)

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Network-response payload structure carries predictive information about DOM observation
- The parent's DOM-hash falsification does NOT generalize to network-response observations
- SPIDER should capture API response bodies when predicting state transitions
- Physics lane has a new valid observation level for C-WEB-DYNAMICS
- Next step: test on production SPAs with genuine transition non-determinism

### 12.2 Negative Result (FALSIFIED-IN-SETTING)
- Network-response payload structure has no conditional PMI beyond action-history memory
- Both DOM-hash AND network-response paths are closed locally
- Physics lane should pivot to: production SPAs, multi-scale dynamics, causal structure, information geometry
- The locally-hosted SPA setting is exhausted for information-theoretic approaches

### 12.3 Invalid Result (MEASUREMENT_INVALID)
- Pipeline needs debugging before this question can be answered
- Not scientific evidence for or against

## 13. Analysis Plan

1. **Data Generation**: Generate 15000 transitions (500 trajectories × 10 steps × 3 SPA types) with API response bodies
2. **Response Body Verification**: Verify no session tokens in response bodies
3. **Session Mapping Verification**: Verify deterministic session→response mapping
4. **Train/Test Split**: 80/20 stratified split by SPA type
5. **Strata Construction**: Group transitions by (URL, ActionHistory_K) for K=1,2,3
6. **PMI Computation**: Compute raw PMI within each stratum, weight by stratum size
7. **Bias Correction**: Compute permutation null (1000 perms), subtract perm_mean from raw PMI
8. **Statistical Tests**: Permutation p-value with Bonferroni correction across 9 comparisons
9. **Controls**: Positive (session-randomized), null (shuffled), determinism, data quality, session mapping
10. **Decision Rule**: Apply frozen decision rule to determine verdict
11. **Reporting**: Report all outcomes with equal prominence

## 14. Analysis Code

Analysis will be implemented in Python using:
- `json` for API response parsing
- `hashlib` for SHA-256 hashing
- `collections.Counter` for frequency counting
- `random` for permutation tests (seed=42)
- Standard library only (no custom estimators required)

Code will be committed to `research/experiments/EXP-PHYSICS-34932344937/` before execution.

## 15. Pre-registered Expectations

From parent experiment and theory:
- Deterministic SPA: PMI = 0.0 at all K (no response variation)
- Independent noise SPA: PMI ≈ 0.0 (E[I]=0 by construction)
- Session-correlated SPA: PMI > 0.0 (response predicts DOM_after through session)
- Bias-corrected PMI should be smaller than raw PMI (bias correction reduces overestimate)
- Body_structure representation may have PMI ≈ 0 (same schema for all sessions)
- Body_hash representation should have highest PMI (most variation)
- Headers_hash representation may have intermediate PMI

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
