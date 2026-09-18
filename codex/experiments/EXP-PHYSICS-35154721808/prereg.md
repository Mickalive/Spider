# EXP-PHYSICS-35154721808 — Preregistration

## Status

DESIGN FROZEN. This document records the experiment plan before execution.

---

## 1. Background and Motivation

### 1.1 Chain of Evidence

The Physics lane has accumulated a series of experiments testing whether response content carries predictive information about state transitions on locally-hosted SPAs. The key sequence:

1. **EXP-PHYSICS-35130680344**: Stochastic branching FSM, unique content mapping (3 hashes). BC PMI = 0.766 bits at K=3, but measurement-invalid (C2 Bonferroni p=0.076, C4 positive control by construction).

2. **EXP-PHYSICS-35137030850**: Many-to-one content mapping (S0/S1 share hash, S2 unique = 2 hashes) vs unique-content (3 hashes). BC PMI: many-to-one = 0.226 bits, unique = 0.493 bits. Difference = -0.268 bits (54% reduction). Verdict: FALSIFIED-IN-SETTING per frozen C3 threshold, but PMI>0 persists with many-to-one mapping.

3. **Audit V4 of EXP-PHYSICS-35137030850**: Identifies critical partial discrimination confound. The many-to-one condition still has 2 unique hashes: observing the unique S2 content eliminates 2 states, and observing the shared S0/S1 content narrows to 2 states. The residual 0.226 bits cannot distinguish genuine predictive dynamics from partial state aliasing.

### 1.2 The Critical Unknown

**Does the residual 0.226 bits from EXP-PHYSICS-35137030850 reflect genuine predictive dynamics beyond aliasing, or is it entirely explained by partial state discrimination?**

This is the single dominant unknown from the parent handoff.

### 1.3 Why This Experiment

A fully-ambiguous (1-hash) content mapping where ALL 3 states share the same content hash eliminates partial discrimination entirely:

- Observing the shared content reveals zero information about which state the system is in
- Any PMI must come from response-context dynamics (session-dependent content variations that correlate with transition direction)
- This is the minimal next experiment to resolve V4

The experiment is low-cost (same FSM, only content mapping changes) and directly resolves the dominant unknown. After this, regardless of outcome, the Physics lane should pivot to production SPA infrastructure.

---

## 2. Hypothesis

### H1 (Primary)

If BC PMI > 0.05 bits with Bonferroni p < 0.0125 on the fully-ambiguous condition (1 hash) at K=3, the hypothesis survives: response content carries predictive information about state transitions even when content does NOT uniquely determine any state. This demonstrates genuine predictive dynamics beyond content-state aliasing.

### H0 (Null)

If BC PMI ≤ 0.05 bits or Bonferroni p ≥ 0.0125 on the fully-ambiguous condition at K=3, the hypothesis is falsified in this setting: the parent's 0.226 bits was entirely explained by partial state discrimination.

---

## 3. State Representation

- **3 states**: S0, S1, S2
- **URL**: constant "/app" (single-page app)
- **Response content**: JSON object with page_title, page_description, content_items, status_text, navigation
- **Content hash**: SHA-256 of JSON response, truncated to 16 hex chars
- **Fully-ambiguous mapping**: ALL 3 states produce identical content → 1 unique hash
- **Stochastic transitions**: p_left=0.7, p_right=0.3 (session-dependent)

### 3.1 Content Definition

```python
CONTENT_FULLY_AMBIGUOUS = {
    "S0": {
        "page_title": "Shared Content",
        "page_description": "Content shared between all states",
        "content_items": ["Item A", "Item B", "Item C"],
        "status_text": "shared",
        "navigation": {"available_actions": ["advance", "branch"]}
    },
    "S1": {
        "page_title": "Shared Content",
        "page_description": "Content shared between all states",
        "content_items": ["Item A", "Item B", "Item C"],
        "status_text": "shared",
        "navigation": {"available_actions": ["advance", "branch"]}
    },
    "S2": {
        "page_title": "Shared Content",
        "page_description": "Content shared between all states",
        "content_items": ["Item A", "Item B", "Item C"],
        "status_text": "shared",
        "navigation": {"available_actions": ["advance", "branch"]}
    }
}
```

All three states produce identical JSON → single SHA-256 hash.

---

## 4. Action Representation

- **2 actions**: "advance", "branch"
- **Action selection**: deterministic per trajectory position (alternating or sequential)
- **Action history**: sequence of K previous actions, padded with "START"

---

## 5. Target

Conditional PMI: I(S_next; Response_before | URL, H_K=3)

- **S_next**: next FSM state (S0, S1, or S2)
- **Response_before**: SHA-256 hash of response content before transition
- **URL**: constant "/app"
- **H_K=3**: last 3 actions in trajectory

---

## 6. Sampling Policy

- **Seed**: 42 (Python random.seed, numpy random seed)
- **Trajectories**: 200 per condition
- **Steps per trajectory**: 10
- **Total transitions**: 2000 per condition
- **Sessions**: 20, directions generated once with seed=42
- **Session assignment**: identical to parent (EXP-PHYSICS-35137030850)

---

## 7. Unit of Analysis

Each transition (state, action, response, next_state) is one observation. Strata are defined by (URL, ActionHistory_K, step). PMI is computed within strata and averaged.

---

## 8. Holdout

No holdout in this experiment. The FSM has known structure; there is no train/test split. All 2000 transitions are used for PMI estimation. The permutation test provides the inferential framework.

---

## 9. Null Models and Baselines

### 9.1 Null Models

1. **Shuffled labels**: Permute Response_before labels within (URL, H_K, step) strata. Expected BC PMI ≈ 0.
2. **Content-shuffled**: Replace each trajectory's response with content from a random state (preserving single-hash structure). Expected BC PMI ≈ 0.

### 9.2 Baselines

1. **Unique-content (parent)**: 3 unique hashes, BC PMI = 0.493 bits (upper bound)
2. **Many-to-one (parent)**: 2 unique hashes, BC PMI = 0.226 bits (intermediate)
3. **State-independent**: constant response, expected BC PMI = 0
4. **Action-history-only**: P(S_next | URL, H_K), K=1,2,3

---

## 10. Primary Metric

Bias-corrected Pointwise Mutual Information (BC PMI):

```
BC_PMI = observed_PMI - permutation_null_mean
```

where observed_PMI is computed within (URL, H_K, step) strata and permutation_null_mean is the mean PMI from 1000 within-strata permutations of Response_before labels.

---

## 11. Expected Direction

If H1 is true: BC PMI > 0 (positive, response context carries transition information).
If H0 is true: BC PMI ≈ 0 (response context carries no transition information).

---

## 12. Uncertainty Method

- **Permutation test**: 1000 permutations per (condition, K) stratum
- **Bonferroni correction**: across 2 comparisons (1 condition × 2 K values: K=1, K=3)
- **Corrected threshold**: p < 0.0125 (α/4, conservative to maintain comparability with parent)
- **Effect size**: BC PMI in bits

---

## 13. Adequacy Rule

The experiment is adequate if:
- H(S_next|URL, H_K=3) > 0.2 bits (ceiling eliminated)
- ≥ 500 valid transitions
- Determinism check passes (accuracy = 1.0)
- Positive control passes
- Null control passes

---

## 14. Falsification/Survival Rule

### SURVIVES_CURRENT_TEST if ALL of:
1. H(S_next|URL, H_K=3) > 0.2 bits
2. BC PMI at K=3 > 0.05 bits with Bonferroni p < 0.0125
3. Positive control passes (|content-shuffled BC PMI| < 3 × std(permuted PMI))
4. Determinism check passes (accuracy = 1.0)
5. ≥ 500 valid transitions

**Note**: Cardinality criterion suspended (|R| = 1 by construction in fully-ambiguous condition).

### FALSIFIED-IN-SETTING if:
- BC PMI ≤ 0.05 bits OR Bonferroni p ≥ 0.0125

### MEASUREMENT_INVALID if:
- Controls fail, ceiling not eliminated, or data quality insufficient

---

## 15. Decision Consequences

### Positive Outcome (SURVIVES)

- V4 audit confound (partial discrimination) is resolved
- PMI persists with fully ambiguous content → genuine predictive dynamics
- Three-condition ordered sequence (3→2→1 hashes) quantifies aliasing contribution
- Physics lane pivots to production SPA infrastructure
- C-WEB-DYNAMICS advances toward EXPERIMENTAL status

### Negative Outcome (FALSIFIED-IN-SETTING)

- Parent's 0.226 bits was entirely from partial state discrimination
- Locally-hosted FSM pathway for C-WEB-DYNAMICS is closed
- Physics lane pivots to production SPA infrastructure
- C-WEB-DYNAMICS remains HYPOTHESIS with narrowed ceiling

### Either Outcome

- Dominant unknown resolved
- Go/no-go decision enabled
- Pivot to production SPA infrastructure warranted

---

## 16. Deviations from Parent

| Aspect | Parent (EXP-PHYSICS-35137030850) | This Experiment |
|--------|----------------------------------|-----------------|
| Content mapping | Many-to-one (2 hashes) + Unique (3 hashes) | Fully-ambiguous (1 hash) |
| Conditions | 2 | 1 |
| Bonferroni comparisons | 4 (2×2) | 2 (1×2) |
| Cardinality criterion | Active | Suspended (|R|=1 by design) |
| FSM | Same | Same |
| Sessions | Same | Same |
| Seed | 42 | 42 |
| Estimator | Same BC PMI | Same BC PMI |

---

## 17. Scope and Limitations

- **Synthetic**: locally-hosted Express SPA with known FSM structure
- **Hash-based observation**: SHA-256 of JSON response, not DOM/accessibility/visual
- **3 states only**: may not generalize to larger state spaces
- **Stochastic but simple**: p=0.7/0.3 session-dependent transitions
- **No production features**: no client-side rendering, auth, external data, DOM evolution
- **Single content representation**: JSON hash only, not multi-modal

The experiment resolves the V4 confound within the tested scope. It does not demonstrate C-WEB-DYNAMICS on production SPAs.
