# EXP-PHYSICS-35130680344 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35130680344
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-PHYSICS-35040401992 (branching FSM, MEASUREMENT_INVALID)

## 2. Scientific Question

On a branching FSM with session-dependent transitions (H(S_next|URL,H_K=3) > 0.2 bits), does non-trivial response encoding — realistic page-content structure (title, items, status) that varies with state but contains NO explicit state_id, session_token, direction, or step fields — yield conditional PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125?

## 3. Motivation

The previous experiment (EXP-PHYSICS-35040401992) tested network-response PMI on a branching FSM with session-dependent transitions. It established:

- **Ceiling eliminated**: H(S_next|URL,H_K=3) = 1.346 bits (branching FSM works)
- **K=1 PMI robust**: BC PMI = 0.924 bits, Bonferroni p = 0.0 (replicated from parent linear FSM)
- **State-independent baseline correct**: BC PMI = 0.0 at both K=1 and K=3
- **Cardinality bounded**: max |R|/N = 0.782 (below 0.8 threshold)

However, the experiment is MEASUREMENT_INVALID due to:

1. **V1 (critical)**: Determinism check fails by construction — response includes `step` field varying within (state, session), making P(Response|state,session)=1.0 impossible
2. **V2 (critical)**: Positive control degeneracy — min_perm_null_std = 0.0 because deterministic strata (H=0) have perm_std = 0
3. **V10 (critical)**: Physics identifiability — response trivially embeds state_id, session_token, direction in JSON. PMI>0 is constructed, not emergent web dynamics.

**The V10 concern is the dominant open question.** The parent's BC PMI = 0.369 bits at K=3 may be entirely explained by explicit state label injection. The K=1 PMI = 0.924 bits is robust but may also be trivially from state_id leakage.

The correct next step is to test the same hypothesis with **non-trivial response encoding** that:
- Contains realistic web page content (title, items, status text)
- Varies with FSM state (so PMI can be >0)
- Does NOT contain explicit state_id, session_token, direction, or step fields
- Resembles what a real SPA would return (not a state machine debug output)

If PMI persists with non-trivial encoding, this demonstrates that page-content variation — not just state label injection — carries predictive information. If PMI drops to zero, the parent's signal was trivially constructed.

## 4. Hypotheses

### H1: Non-Trivial Encoding PMI
On the non-trivial encoding condition (page content without state labels), bias-corrected PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125.

### H2: Encoding Comparison
Non-trivial encoding BC PMI is within 0.1 bits of trivial encoding BC PMI at K=3 (i.e., removing explicit labels does not eliminate the signal). This is a weaker discrimination test than the parent's H2 — we expect non-trivial to be slightly worse but not zero.

### H3: Positive Control
Session-randomized control on non-trivial encoding yields BC PMI ≈ 0 within permutation noise, AND perm_null_std > 0 (computed on H>0 strata only).

### H4: Cardinality Bounded
Non-trivial encoding has |R| ≈ 3 unique response hashes (one per state) vs trivial's |R| ≈ 60 (20 sessions × 3 states). Max |R|/N per stratum at K=3 < 0.8.

### H5: Determinism Check
Both conditions have P(Response_hash | FSM_state, session, step) = 1.0. Grouping includes step (fixing parent V1).

### H6: Ceiling Elimination
Conditional entropy H(S_next|URL, H_K=3) > 0.2 bits (same branching FSM as parent).

## 5. Experimental Conditions

### 5.1 Branching FSM Design

Identical to parent EXP-PHYSICS-35040401992:

**States**: {S0, S1, S2}
**Actions**: {advance, branch}
**Session parameter**: Each session has a hidden direction ∈ {left, right} (uniform random, independent per session)

**Transition rules** (deterministic given session direction):
- From S0: advance → S1; branch → S2 if direction=='left' else S1
- From S1: advance → S2; branch → S0 if direction=='left' else S2
- From S2: advance → S0; branch → S1 if direction=='left' else S0

**Branching property**: Every state has two outgoing actions. At every state, branch leads to two possible next states depending on session direction. H(S_next|URL,H_K=3) ≈ 0.5 bits for uniform action policy.

### 5.2 Non-Trivial Encoding Condition (PRIMARY)

Response body contains realistic page-content structure that varies with state but contains NO explicit state labels:

```json
{
  "page_title": "<state-specific>",
  "page_description": "<state-specific>",
  "content_items": [<state-specific list>],
  "status_text": "<state-specific>",
  "navigation": {
    "available_actions": ["advance", "branch"]
  }
}
```

**State-specific content** (deterministic per state, same for all sessions):

- **S0 (Home)**:
  - page_title: "Home"
  - page_description: "Welcome to the application"
  - content_items: ["Featured Products", "Popular Categories", "New Arrivals"]
  - status_text: "browsing"

- **S1 (Browse)**:
  - page_title: "Browse"
  - page_description: "Explore available items"
  - content_items: ["Filter Options", "Sort By Price", "View Details"]
  - status_text: "comparing"

- **S2 (Detail)**:
  - page_title: "Details"
  - page_description: "Item specifications and reviews"
  - content_items: ["Customer Reviews", "Technical Specs", "Related Items"]
  - status_text: "reviewing"

**Key properties**:
- Content varies with state (3 unique response hashes, one per state)
- Content is NOT a state label (no "S0", "S1", "S2" in response)
- Content resembles real web page structure (titles, items, status)
- Content is deterministic per state (same for all sessions at same state)
- Navigation available_actions is constant (not state-informative)

**Expected unique response hashes**: ~3 (one per state)

### 5.3 Trivial Encoding Condition (COMPARISON)

Response body contains explicit state labels (parent's state-dependent response):

```json
{
  "state_id": "S0",
  "step": 2,
  "session_token": "a1b2c3d4",
  "direction": "left",
  "items": ["item1", "item2"]
}
```

**Key properties**:
- Explicitly encodes current state, step, session, direction
- Expected BC PMI > 0 (trivially from state label)
- Provides within-experiment comparison for V10 test

**Expected unique response hashes**: ~60 (20 sessions × 3 states)

### 5.4 Why This Comparison Is Decisive

The only difference between conditions is response encoding strategy:
- Same FSM, same sessions, same session assignment, same action sequences
- Non-trivial: page content (no state labels) → PMI reflects content-structure correlation
- Trivial: explicit state labels → PMI reflects label leakage

If non-trivial BC PMI ≈ trivial BC PMI: page-content structure carries predictive information (V10 addressed)
If non-trivial BC PMI ≈ 0 while trivial BC PMI > 0: parent's signal was from state label injection (V10 confirmed)
If both ≈ 0: pipeline issue or environment insufficient

## 6. Data Generation

### 6.1 Trajectory Generation

- 200 trajectories per condition (400 total)
- 10 steps per trajectory
- Actions chosen uniformly at random from available action at each state
- **Session assignment**: Generate session_directions ONCE with seed=42, use IDENTICALLY for both conditions (fixes parent V7 session mismatch)
- Session ID assigned uniformly at random from 20 sessions at trajectory start (independent random draw)
- Session direction fixed per session (left/right, uniform random)

### 6.2 Response Generation

**Non-trivial encoding**: For each (state) pair, generate response containing:
- `page_title`: state-specific title (3 values)
- `page_description`: state-specific description (3 values)
- `content_items`: state-specific item list (3 value sets)
- `status_text`: state-specific status (3 values)
- `navigation.available_actions`: ["advance", "branch"] (constant)

**Trivial encoding**: For each (session, state) pair, generate response containing:
- `state_id`: FSM state name (S0, S1, S2)
- `step`: step number within trajectory (1-10)
- `session_token`: SHA-256(session_id)[:8] (20 values)
- `direction`: session direction (left/right)
- `items`: list of length = step number

### 6.3 Response Hashing

Response hash = SHA-256(json.dumps(response_body, sort_keys=True))[:16]. This is the discretized observation for PMI computation.

## 7. Measures

### 7.1 Primary Metric

**Bias-corrected conditional PMI** on non-trivial encoding at K=3:
- observed_pmi = plug-in PMI I(S_next; Response_before | URL, H_K=3)
- perm_mean = mean PMI across 1000 within-strata permutations of Response_before labels
- bias_corrected_pmi = observed_pmi - perm_mean

### 7.2 Secondary Metrics

- BC PMI at K=1 on non-trivial encoding (parent showed 0.924 bits)
- BC PMI at K=3 on trivial encoding (parent showed 0.369 bits)
- BC PMI at K=1 on trivial encoding (parent showed 0.924 bits)
- |R| per stratum at K=3 (cardinality check)
- Action-history prediction accuracy at K=1,2,3
- Conditional entropy H(S_next|URL, H_K=3)
- Stratum sizes and distribution

## 8. Null Models

### 8.1 Session-Randomized Control (Positive Control) — CORRECTED

Replace each trajectory's session_id with a random session_id from a different trajectory. Response content still varies, but session→state mapping is broken. Expected BC PMI ≈ 0.

**CORRECTION from parent V2**: Exclude strata where H(S_next|stratum)=0 from min_perm_null_std computation. This prevents deterministic strata from making perm_null_std = 0 by construction.

Pass criterion: |session-randomized BC PMI| < 3 * std(permuted PMI) AND perm_null_std > 0 (computed on H>0 strata only).

### 8.2 Shuffled Response Labels (Null Control) — CORRECTED

Within each (URL, H_K, step) stratum, permute Response_before labels. Preserves marginal distributions but breaks R→S pairing. Expected BC PMI ≈ 0.

**CORRECTION**: Compute bias-corrected shuffled PMI (shuffled PMI - perm_mean) to remove finite-sample bias. Pass criterion: |mean shuffled BC PMI| < 3 * std(shuffled BC PMI).

### 8.3 State-Independent Baseline

Same FSM, constant response. Expected PMI = 0.0.

## 9. Statistical Tests

### 9.1 Primary Test

- BC PMI at K=3 on non-trivial encoding
- One-sided: PMI > 0.05 bits
- Within-strata permutation test, 1000 permutations
- Bonferroni correction across 4 comparisons (2 conditions × 2 K values)
- Corrected alpha: 0.05 / 4 = 0.0125

### 9.2 Encoding Comparison Test

- Non-trivial BC PMI - Trivial BC PMI at K=3
- Two-sided equivalence-style: difference > -0.1 bits (non-trivial is not substantially worse)
- Paired permutation test across trajectories (trajectory-level, fixing parent V6)
- 1000 permutations
- Uncorrected alpha: 0.05

### 9.3 Cardinality Check

- Report |R| per stratum at K=3 for both conditions
- Non-trivial expected ~3 unique hashes; trivial expected ~60
- Pass: |R| < 0.8 * N

### 9.4 Conditional Entropy Check

- H(S_next|URL, H_K=3) on generated data
- Pass: H > 0.2 bits

## 10. Controls

### 10.1 Positive Control (Session-Randomized) — CORRECTED

- Randomize session assignment across trajectories
- Response→state mapping broken; PMI should be ≈ 0
- **CORRECTION**: Exclude H=0 strata from min_perm_null_std
- Pass: |session-randomized BC PMI| < 3 * std(permuted PMI) AND perm_null_std > 0

### 10.2 Null Control (Shuffled Labels) — CORRECTED

- Permute response labels within (URL, H_K, step) strata
- Breaks R→S pairing; PMI should be ≈ 0
- **CORRECTION**: Use bias-corrected shuffled PMI
- Pass: |mean shuffled BC PMI| < 3 * std(shuffled BC PMI)

### 10.3 State-Independent Baseline

- Constant response regardless of state
- PMI should be 0.0 exactly
- Pass: BC PMI = 0.0

### 10.4 Determinism Check — CORRECTED

- Both conditions: P(Response_hash | FSM_state, session, step) = 1.0
- **CORRECTION**: Grouping includes step (fixing parent V1)
- Both conditions must pass

## 11. Validity Threats

### 11.1 State Label Removal May Not Remove Signal

Even without explicit state_id, the non-trivial encoding's content uniquely identifies the state (3 unique hashes for 3 states). PMI>0 could still be "trivial" in the sense that content uniquely determines state.

**Mitigation**: This is expected and acceptable. The question is whether realistic web-content variation (not state labels) carries predictive information. Real web pages also have content that varies with state. The improvement over the parent is that the content resembles real page structure, not machine-readable state debug output.

### 11.2 Synthetic-to-Real Gap

Locally-hosted Express SPA may not reflect production SPAs. **Mitigation**: Controlled validation. If pipeline cannot detect known structure in controlled data with realistic content, it cannot be trusted on real data.

### 11.3 Sample Size

200 trajectories × 10 steps = 2000 transitions per condition, ~714 per stratum at K=3. Adequate power for PMI > 0.05 bits.

### 11.4 Parent K=3 Non-Significance

Parent showed BC PMI = 0.369 but Bonferroni p = 0.322 (raw 0.0805). With non-trivial encoding having only 3 unique responses (vs 60), |R|/N drops from 0.78 to 0.004, dramatically reducing finite-sample bias (perm_mean from 0.977 to near 0). This should improve power and reduce p-value. However, if the true effect is small, significance may still fail.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST

If ALL of:
1. H(S_next|URL, H_K=3) > 0.2 bits (ceiling eliminated)
2. BC PMI on non-trivial encoding at K=3 > 0.05 bits, Bonferroni p < 0.0125
3. Non-trivial BC PMI > trivial BC PMI - 0.1 bits (not substantially worse)
4. Positive control passes (|session-randomized BC PMI| < 3 * std(permuted PMI) on H>0 strata AND perm_null_std > 0)
5. Determinism check passes (both conditions accuracy = 1.0 on state,session,step grouping)
6. >= 500 valid transitions per condition
7. Cardinality check: |R| < 0.8 * N per stratum

### 12.2 FALSIFIED-IN-SETTING

If ANY of:
1. BC PMI on non-trivial encoding at K=3 <= 0.05 bits
2. Non-trivial BC PMI < trivial BC PMI - 0.1 bits (removing labels eliminates signal)
3. Both conditions have BC PMI ≈ 0 (no response informativeness)

### 12.3 MEASUREMENT_INVALID

If:
1. Controls fail (positive control perm_null_std = 0, determinism check fails)
2. Data quality insufficient (< 500 transitions per condition)
3. Pipeline errors prevent computation
4. Cardinality degenerate (|R| >= 0.8 * N per stratum)
5. Conditional entropy H <= 0.2 bits (ceiling not eliminated)

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)

- Non-trivial page-content structure carries predictive information about state transitions
- V10 identifiability concern addressed: PMI persists without explicit state labels
- SPIDER should capture page content (titles, items, status) as observation features
- Response-level observation validated as viable substrate for state labeling
- Justifies further exploration with richer content representations and production SPAs

### 13.2 Negative Result (FALSIFIED-IN-SETTING)

- Non-trivial encoding yields no PMI; parent's signal was from state label injection
- Response-level observation does not carry predictive information beyond action-history
- Locally-hosted testable path for C-WEB-DYNAMICS across ALL observation levels is closed
- Physics lane should pivot to production infrastructure or alternative mechanisms

### 13.3 Invalid Result (MEASUREMENT_INVALID)

- Pipeline still needs debugging
- Not scientific evidence for or against
- Re-run with corrected pipeline

## 14. Analysis Plan

1. **Data Generation**: Generate 4000 transitions (200 trajectories × 10 steps × 2 conditions)
2. **Response Hashing**: SHA-256(json.dumps(response_body, sort_keys=True))[:16]
3. **Stratification**: Build strata by (URL, H_K, step) for K=1,2,3
4. **MI Computation**: Plug-in PMI per stratum, weighted average
5. **Bias Correction**: Permutation null (1000 perms per stratum), subtract perm_mean
6. **Permutation Tests**: Within-strata shuffling, Bonferroni correction
7. **Encoding Comparison**: Paired permutation on non-trivial vs trivial PMI difference (trajectory-level)
8. **Controls**: Session-randomized (H>0 strata only), shuffled labels (bias-corrected), state-independent, determinism (state,session,step grouping)
9. **Cardinality Check**: Report |R| per stratum for both conditions
10. **Conditional Entropy**: Compute H(S_next|URL, H_K=3)
11. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for permutation tests
- `hashlib` for response hashing
- `json` for response parsing
- `collections.Counter` for frequency counting
- Standard library only (no custom estimators)

Code will be committed to `research/experiments/EXP-PHYSICS-35130680344/` before execution.

## 16. Pre-registered Expectations

From prior Physics work:
- Network-response PMI at K=1 on branching FSM was 0.924 bits (parent, trivial encoding)
- Network-response PMI at K=3 on branching FSM was 0.369 bits (parent, trivial encoding, MEASUREMENT_INVALID)
- Linear FSM at K>=2 had H=0 (ceiling effect)
- Branching FSM eliminates ceiling (H=1.346 bits)
- Bias-corrected estimator (observed - perm_mean) is valid

**Key unknown**: Does PMI persist when explicit state labels are removed?
- If yes: page-content structure carries predictive information (V10 addressed)
- If no: parent's signal was trivially constructed from state label injection

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
