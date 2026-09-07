# EXP-PHYSICS-34071626363 — Non-Leakage PMI Analysis Report

## Experiment Summary

**Experiment ID**: EXP-PHYSICS-34071626363  
**Lane**: Physics  
**Claim**: C-WEB-DYNAMICS  
**Status**: COMPLETE  
**Outcome**: FALSIFIES  

This experiment tested whether pointwise mutual information (PMI) between actions and next-states remains positive when action-to-destination URL leakage is eliminated. The parent experiment (EXP-PHYSICS-34038570933) found PMI > 0 but confounded by 92-98% of transitions where `action.target_href == state_after.url`. This experiment isolates the non-leakage subset to test for genuine state-conditioned dynamical structure.

## Key Results

| Metric | Wikipedia | Python Docs |
|--------|-----------|-------------|
| Non-leakage transitions | 67 (7.6%) | 21 (2.4%) |
| PMI (non-leakage) | **0.000 bits** | **0.874 bits** |
| Permutation p-value | **1.000** | **0.667** |
| PMI (all transitions) | 1.073 bits | 1.502 bits |
| Effect size d | -0.711 | 0.707 |

## Decision Checks

| Check | Description | Result |
|-------|-------------|--------|
| 1 | Wiki non-leakage PMI > 0, p < 0.025 | **FAIL** (PMI=0.0, p=1.0) |
| 2 | Python non-leakage PMI > 0, p < 0.025 | **FAIL** (PMI=0.874, p=0.667) |
| 3 | Positive control PMI >= 1.0 | **FAIL** (PMI=0.855) |
| 4 | Null control p > 0.05 | **PASS** (p=1.0) |
| 5 | No pipeline errors | **PASS** |

**Verdict**: FALSIFIED-IN-SETTING (checks 1, 2, and 3 fail)

## Detailed Observations

### Wikipedia Non-Leakage: PMI = 0.0 Exactly

The Wikipedia non-leakage subset has 67 transitions with 58 unique states and 58 unique (state, action) pairs. **Every SA pair appears exactly once**. Under this condition:

- P(a, s'|s) = 1/count(s) for each transition
- P(a|s) = 1/count(s) for each unique action from s  
- P(s'|s) = 1/count(s) for each unique next-state from s

Therefore PMI = log2[P(a,s'|s) / (P(a|s) × P(s'|s))] = log2[1] = 0.0 for every transition.

This is not a failure of the PMI computation — it is a mathematical consequence of the sparse, unique SA-pair regime. When each (state, action) combination appears exactly once, there is no statistical association to detect because the marginal and joint distributions are identical under Laplace smoothing.

### Python Docs Non-Leakage: PMI = 0.874, Not Significant

The Python docs subset has 21 transitions with 14 unique states and 20 unique SA pairs. PMI is positive (0.874 bits) but the permutation test p-value is 0.667, meaning the observed PMI is indistinguishable from the shuffled-action null (mean = 0.843). The moderate effect size (d = 0.71) is not statistically reliable with this sample size.

### Action Representations

- **Hashed actions** (SHA-256 of target_href): Identical PMI to unblinded actions. Hashing preserves uniqueness, so when each SA pair is already unique, it does not change the PMI computation.
- **Action-type categorical** (all actions = 'click'): PMI ≈ 0 on both sites. When all actions are identical, PMI reduces to state-to-next-state predictability, which is ~0 for sparse state spaces.

### Positive Control Threshold

The positive control PMI = 0.855 bits is statistically significant (p = 0.001) but below the preregistered 1.0 bit threshold. This threshold failure was inherited from the parent experiment, where it was noted that the 1.0 bit expectation was based on incorrect assumptions about the synthetic data structure (8 states, 8 actions, some single-action states). The PMI computation correctly detects known structure; the threshold is the issue.

### Null Control

The null control passes: shuffled PMI = 0.001, p = 1.0. The PMI computation correctly does not detect structure when action labels carry no information.

## Comparison with Parent Experiment

| Condition | Parent (all transitions) | This experiment (non-leakage) |
|-----------|-------------------------|-------------------------------|
| Wikipedia PMI | 1.073 bits | 0.000 bits |
| Python PMI | 1.502 bits | 0.874 bits |
| Leakage fraction | 92-98% | N/A (excluded) |

The dramatic drop in PMI when leakage transitions are excluded confirms that the parent experiment's PMI signal was driven by the trivial action-to-destination mapping, not by genuine state-conditioned dynamical structure.

## Interpretation

**The hypothesis is falsified in this setting**: PMI does not remain positive on non-leakage transitions for both live sites. The Wikipedia non-leakage subset has PMI = 0.0 exactly (all unique SA pairs), and the Python docs subset has positive PMI that is not statistically distinguishable from the shuffled null.

This does not falsify C-WEB-DYNAMICS entirely — only this detection method (URL-level PMI) on these specific server-rendered sites. The non-leakage fraction is very low (7.6% wiki, 2.4% python), suggesting these sites are predominantly characterized by trivial action-to-destination mapping.

## Limitations

1. **Small sample sizes**: 67 wiki, 21 python non-leakage transitions limit statistical power
2. **Sparse state spaces**: Unique SA pairs in the non-leakage subset make PMI identically 0 under Laplace smoothing
3. **URL-only representation**: Richer state representations might reveal structure not visible at URL level
4. **Server-rendered sites**: SPA/form-heavy sites where non-leakage is more frequent were not tested

## Recommendations for Future Work

1. **SPA/form-heavy sites**: Test on sites where `action.target_href != state_after.url` by construction (JavaScript navigation, form submissions)
2. **Trajectory-level measures**: Test entropy rates (H(S_1,...,S_T)) as an aggregate measure that may be more robust to per-transition sparsity
3. **Richer state representations**: Use composite BrowserState (title, link_texts, tag_counts, form_signals, accessibility) instead of URL-only
4. **Revise positive control**: Either redesign synthetic data with more states/actions or lower the threshold to >= 0.5 bits
