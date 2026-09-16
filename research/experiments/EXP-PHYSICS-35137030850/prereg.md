# EXP-PHYSICS-35137030850 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35137030850
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Date**: 2026-09-16
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-PHYSICS-35130680344 (branching FSM, non-trivial encoding, MEASUREMENT_INVALID)

## 2. Scientific Question

Can a non-deterministic branching FSM with session-dependent transitions and many-to-one content mapping (where response does NOT uniquely identify state for a subset of states) yield conditional PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125?

## 3. Motivation

The previous experiment (EXP-PHYSICS-35130680344) tested non-trivial response encoding on a branching FSM with deterministic transitions. It established:

- **Ceiling eliminated**: H(S_next|URL,H_K=3) = 1.103 bits (branching FSM works)
- **K=1 PMI robust**: BC PMI = 1.035 bits, Bonferroni p = 0.0
- **Non-trivial encoding yields higher PMI**: NT 0.766 vs TR 0.345 at K=3
- **BC estimator valid**: null control yields BC PMI ≈ 0 (mean 0.0014)
- **Determinism check passes**: P(Response|state,session,step) = 1.0 with step grouping

However, the experiment is MEASUREMENT_INVALID due to:

1. **C2 (primary)**: Bonferroni p = 0.076 > 0.0125 — non-significant
2. **C4**: Positive control fails by construction — session randomization cannot break deterministic state→hash mapping
3. **V10 (critical)**: Physics identifiability — NT encoding uniquely determines state (3 hashes for 3 states), making PMI>0 a content-state alias, not emergent dynamics

**The V10 concern is the dominant open question.** The parent's NT K3 BC PMI = 0.766 bits may be entirely explained by content uniquely determining state. The handoff explicitly identifies this as the critical unknown:

> "Whether PMI persists with stochastic/many-to-one content mapping where content does NOT uniquely determine state — the critical test separating content-as-state-alias from genuine predictive dynamics."

**The correct next step is to test the same hypothesis with many-to-one content mapping** where:
- Multiple states share the same content hash (content does NOT uniquely determine state)
- Transitions are stochastic (same state+action yields different next states across sessions)
- PMI>0 cannot be attributed to content-state aliasing

If PMI persists with many-to-one mapping, this demonstrates genuine predictive dynamics beyond content-state aliasing. If PMI drops to zero, the parent's signal was trivially constructed.

## 4. Hypotheses

### H1: Many-to-One PMI
On the many-to-one content condition (S0 and S1 share content hash, S2 unique), bias-corrected PMI I(S_next; Response_before | URL, H_K=3) > 0.05 bits with Bonferroni-corrected permutation p < 0.0125.

### H2: Content Mapping Comparison
Many-to-one BC PMI is within 0.1 bits of unique-content BC PMI at K=3 (i.e., making content ambiguous for some states does not eliminate the signal). This directly tests whether content-state aliasing was the sole PMI source.

### H3: Positive Control
Content-shuffled control on many-to-one condition yields BC PMI ≈ 0 within permutation noise, AND perm_null_std > 0 (computed on H>0 strata only). The control randomizes state→content mapping (not session assignment), which the parent handoff identified as the correct design.

### H4: Cardinality Bounded
Many-to-one condition has |R| ≈ 2 unique response hashes (shared S0/S1 + unique S2) vs unique-content's |R| ≈ 3. Max |R|/N per stratum at K=3 < 0.8.

### H5: Determinism Check
Both conditions have P(Response_hash | FSM_state, session, step) = 1.0. Grouping includes step.

### H6: Ceiling Elimination
Conditional entropy H(S_next|URL, H_K=3) > 0.2 bits (stochastic branching FSM).

## 5. Experimental Conditions

### 5.1 Branching FSM Design

**States**: {S0, S1, S2}
**Actions**: {advance, branch}
**Session parameter**: Each session has a hidden direction ∈ {left, right} (uniform random, independent per session)

**Transition rules** (stochastic given session direction):
- From S0:
  - advance → S1 with prob p_dir, S2 with prob 1-p_dir
  - branch → S2 with prob p_dir, S1 with prob 1-p_dir
- From S1:
  - advance → S2 with prob p_dir, S0 with prob 1-p_dir
  - branch → S0 with prob p_dir, S2 with prob 1-p_dir
- From S2:
  - advance → S0 with prob p_dir, S1 with prob 1-p_dir
  - branch → S1 with prob p_dir, S0 with prob 1-p_dir

Where p_dir = 0.7 for direction='left', p_dir = 0.3 for direction='right'.

**Branching property**: Every state has two outgoing actions. At every state, each action leads to two possible next states depending on session direction, with stochastic outcomes. H(S_next|URL,H_K=3) > 0.2 bits for uniform action policy.

**Key difference from parent**: Transitions are STOCHASTIC, not deterministic. Same (state, action) yields different next states across sessions with probabilities p and 1-p. This creates genuine non-determinism in the environment.

### 5.2 Many-to-One Content Condition (PRIMARY)

Response body contains realistic page-content structure where **S0 and S1 share the same content hash** (many-to-one mapping), while S2 has unique content:

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

**Content mapping** (many-to-one):
- **S0 (Home)** and **S1 (Browse)** share identical content:
  - page_title: "Shared Content"
  - page_description: "Content shared between states"
  - content_items: ["Item A", "Item B", "Item C"]
  - status_text: "shared"

- **S2 (Detail)** has unique content:
  - page_title: "Details"
  - page_description: "Item specifications and reviews"
  - content_items: ["Customer Reviews", "Technical Specs", "Related Items"]
  - status_text: "reviewing"

**Key properties**:
- Content does NOT uniquely determine state: observing "Shared Content" means state is S0 OR S1
- Only S2 has unique content
- Expected unique response hashes: ~2 (shared S0/S1 + unique S2)
- Content resembles real web page structure
- Content is deterministic per state (same for all sessions at same state)

### 5.3 Unique-Content Condition (COMPARISON)

Response body contains **unique content for each state** (each state has distinct content hash):

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

**Content mapping** (one-to-one):
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
- Each state has unique content (3 unique response hashes)
- Content uniquely determines state
- Expected BC PMI > 0 (replicates parent's NT condition)

### 5.4 Why This Comparison Is Decisive

The only difference between conditions is content mapping strategy:
- Same FSM, same sessions, same session assignment, same action sequences
- Many-to-one: S0 and S1 share content → content does NOT uniquely determine state
- Unique-content: each state has unique content → content uniquely determines state

If many-to-one BC PMI ≈ unique-content BC PMI: predictive dynamics beyond content-state aliasing (V10 addressed)
If many-to-one BC PMI ≈ 0 while unique-content BC PMI > 0: parent's signal was from content-state aliasing (V10 confirmed)
If both ≈ 0: pipeline issue or environment insufficient

## 6. Data Generation

### 6.1 Trajectory Generation

- 200 trajectories per condition (400 total)
- 10 steps per trajectory
- Actions chosen uniformly at random from available action at each state
- **Session assignment**: Generate session_directions ONCE with seed=42, use IDENTICALLY for both conditions
- Session ID assigned uniformly at random from 20 sessions at trajectory start (independent random draw)
- Session direction fixed per session (left/right, uniform random)

### 6.2 Transition Execution

For each (state, action, session_direction) tuple:
- Draw next_state from Bernoulli(p_dir) where p_dir = 0.7 for left, 0.3 for right
- Record transition (state, action, next_state, session_id, step)

### 6.3 Response Generation

**Many-to-one condition**: For each (state) pair, generate response containing:
- If state is S0 or S1: identical content (shared hash)
- If state is S2: unique content

**Unique-content condition**: For each (state) pair, generate response containing:
- Each state has distinct content (3 unique hashes)

### 6.4 Response Hashing

Response hash = SHA-256(json.dumps(response_body, sort_keys=True))[:16]. This is the discretized observation for PMI computation.

## 7. Measures

### 7.1 Primary Metric

**Bias-corrected conditional PMI** on many-to-one condition at K=3:
- observed_pmi = plug-in PMI I(S_next; Response_before | URL, H_K=3)
- perm_mean = mean PMI across 1000 within-strata permutations of Response_before labels
- bias_corrected_pmi = observed_pmi - perm_mean

### 7.2 Secondary Metrics

- BC PMI at K=1 on many-to-one condition
- BC PMI at K=3 on unique-content condition (replication check)
- BC PMI at K=1 on unique-content condition
- |R| per stratum at K=3 (cardinality check)
- Action-history prediction accuracy at K=1,2,3
- Conditional entropy H(S_next|URL, H_K=3)
- Stratum sizes and distribution
- Transition probability estimates p_hat per (state, action, direction)

## 8. Null Models

### 8.1 Content-Shuffled Control (Positive Control)

Replace each trajectory's response content with content from a random state (preserving the many-to-one mapping structure but breaking state→content pairing). Expected BC PMI ≈ 0.

**CRITICAL DESIGN**: This randomizes state→content mapping (not session assignment), which the parent handoff identified as the correct control design for deterministic content encodings.

Pass criterion: |content-shuffled BC PMI| < 3 * std(permuted PMI) AND perm_null_std > 0 (computed on H>0 strata only).

### 8.2 Shuffled Response Labels (Null Control)

Within each (URL, H_K, step) stratum, permute Response_before labels. Preserves marginal distributions but breaks R→S pairing. Expected BC PMI ≈ 0.

Compute bias-corrected shuffled PMI (shuffled PMI - perm_mean) to remove finite-sample bias. Pass criterion: |mean shuffled BC PMI| < 3 * std(shuffled BC PMI).

### 8.3 State-Independent Baseline

Same FSM, constant response. Expected PMI = 0.0.

## 9. Statistical Tests

### 9.1 Primary Test

- BC PMI at K=3 on many-to-one condition
- One-sided: PMI > 0.05 bits
- Within-strata permutation test, 1000 permutations
- Bonferroni correction across 4 comparisons (2 conditions × 2 K values)
- Corrected alpha: 0.05 / 4 = 0.0125

### 9.2 Content Mapping Comparison Test

- Many-to-one BC PMI - Unique-content BC PMI at K=3
- Two-sided equivalence-style: difference > -0.1 bits (many-to-one is not substantially worse)
- Paired permutation test across trajectories (trajectory-level)
- 1000 permutations
- Uncorrected alpha: 0.05

### 9.3 Cardinality Check

- Report |R| per stratum at K=3 for both conditions
- Many-to-one expected ~2 unique hashes; unique-content expected ~3
- Pass: |R| < 0.8 * N

### 9.4 Conditional Entropy Check

- H(S_next|URL, H_K=3) on generated data
- Pass: H > 0.2 bits

### 9.5 Transition Probability Verification

- Estimate p_hat for each (state, action, direction) tuple
- Verify p_hat ≈ 0.7 for left-direction, p_hat ≈ 0.3 for right-direction
- Verify stochasticity: p_hat not ≈ 0.0 or 1.0

## 10. Controls

### 10.1 Positive Control (Content-Shuffled)

- Randomize state→content mapping across states (preserving many-to-one structure)
- Content→state pairing broken; PMI should be ≈ 0
- Pass: |content-shuffled BC PMI| < 3 * std(permuted PMI) AND perm_null_std > 0

### 10.2 Null Control (Shuffled Labels)

- Permute response labels within (URL, H_K, step) strata
- Breaks R→S pairing; PMI should be ≈ 0
- Use bias-corrected shuffled PMI
- Pass: |mean shuffled BC PMI| < 3 * std(shuffled BC PMI)

### 10.3 State-Independent Baseline

- Constant response regardless of state
- PMI should be 0.0 exactly
- Pass: BC PMI = 0.0

### 10.4 Determinism Check

- Both conditions: P(Response_hash | FSM_state, session, step) = 1.0
- Grouping includes step
- Both conditions must pass

## 11. Validity Threats

### 11.1 Many-to-One Mapping May Still Allow State Discrimination

Even with S0 and S1 sharing content, S2 is unique. PMI>0 could come from discriminating S2 from {S0, S1} rather than from genuine dynamics.

**Mitigation**: This is acceptable. The key test is whether PMI persists when content is ambiguous for SOME states. If PMI drops to zero, content-state aliasing was the sole source. If PMI persists, content carries predictive information even when ambiguous.

### 11.2 Stochastic Transitions Reduce Signal Strength

Stochastic transitions make prediction harder, potentially reducing PMI below detection threshold even if genuine dynamics exist.

**Mitigation**: H(S_next|URL,H_K=3) > 0.2 bits is achievable with p=0.7/0.3 branching. K=1 PMI was robust (1.035 bits) on parent's deterministic FSM; stochastic transitions should preserve signal at K=1.

### 11.3 Synthetic-to-Real Gap

Locally-hosted Express SPA may not reflect production SPAs. **Mitigation**: Controlled validation. If pipeline cannot detect known structure in controlled data with many-to-one mapping, it cannot be trusted on real data.

### 11.4 Sample Size

200 trajectories × 10 steps = 2000 transitions per condition, ~714 per stratum at K=3. Adequate power for PMI > 0.05 bits.

## 12. Decision Rules

### 12.1 SURVIVES_CURRENT_TEST

If ALL of:
1. H(S_next|URL, H_K=3) > 0.2 bits (ceiling eliminated)
2. BC PMI on many-to-one condition at K=3 > 0.05 bits, Bonferroni p < 0.0125
3. Many-to-one BC PMI > unique-content BC PMI - 0.1 bits (not substantially worse)
4. Positive control passes (|content-shuffled BC PMI| < 3 * std(permuted PMI) on H>0 strata AND perm_null_std > 0)
5. Determinism check passes (both conditions accuracy = 1.0 on state,session,step grouping)
6. >= 500 valid transitions per condition
7. Cardinality check: |R| < 0.8 * N per stratum on many-to-one condition

### 12.2 FALSIFIED-IN-SETTING

If ANY of:
1. BC PMI on many-to-one condition at K=3 <= 0.05 bits
2. Many-to-one BC PMI < unique-content BC PMI - 0.1 bits (content-state aliasing was sole source)
3. Both conditions have BC PMI ≈ 0 (no response informativeness)

### 12.3 MEASUREMENT_INVALID

If:
1. Controls fail (positive control perm_null_std = 0, determinism check fails)
2. Data quality insufficient (< 500 transitions per condition)
3. Pipeline errors prevent computation
4. Cardinality degenerate (|R| >= 0.8 * N per stratum on many-to-one condition)
5. Conditional entropy H <= 0.2 bits (ceiling not eliminated)

## 13. Expected Outcomes

### 13.1 Positive Result (SURVIVES_CURRENT_TEST)

- PMI persists when content does NOT uniquely determine state
- Genuine predictive dynamics beyond content-state aliasing demonstrated
- V10 identifiability concern resolved: PMI survives many-to-one content mapping
- SPIDER should capture page content as observation features for state prediction
- Justifies further exploration with richer content representations and production SPAs

### 13.2 Negative Result (FALSIFIED-IN-SETTING)

- PMI drops to zero when content is many-to-one
- Parent's signal was trivially constructed from deterministic content-state mapping
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
7. **Content Mapping Comparison**: Paired permutation on many-to-one vs unique-content PMI difference (trajectory-level)
8. **Controls**: Content-shuffled (H>0 strata only), shuffled labels (bias-corrected), state-independent, determinism (state,session,step grouping)
9. **Cardinality Check**: Report |R| per stratum for both conditions
10. **Conditional Entropy**: Compute H(S_next|URL, H_K=3)
11. **Transition Verification**: Estimate p_hat per (state, action, direction), verify stochasticity
12. **Reporting**: Report all outcomes with equal prominence

## 15. Analysis Code

Analysis will be implemented in Python using:
- `numpy` for array operations and random generation
- `scipy.stats` for permutation tests
- `hashlib` for response hashing
- `json` for response parsing
- `collections.Counter` for frequency counting
- Standard library only (no custom estimators)

Code will be committed to `research/experiments/EXP-PHYSICS-35137030850/` before execution.

## 16. Pre-registered Expectations

From prior Physics work:
- Branching FSM with deterministic transitions: H=1.103 bits, NT K3 BC PMI=0.766 (MEASUREMENT_INVALID)
- K=1 PMI robust: 1.035 bits on branching FSM
- Linear FSM at K>=2 had H=0 (ceiling effect)
- Branching FSM eliminates ceiling
- Bias-corrected estimator is valid (null control yields ≈0)

**Key unknown**: Does PMI persist when content does NOT uniquely determine state?
- If yes: genuine predictive dynamics beyond content-state aliasing (V10 addressed)
- If no: parent's signal was trivially constructed from content-state mapping

## 17. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 18. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
