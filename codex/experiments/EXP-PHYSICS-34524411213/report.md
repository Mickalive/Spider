# EXP-PHYSICS-34524411213 — Execution Report

## Experiment Summary

**Experiment ID**: EXP-PHYSICS-34524411213
**Lane**: Physics
**Claim**: C-WEB-DYNAMICS
**Question**: Can DOM structural features (element counts, tree depth, interactive element density) predict next-state transitions on real SPA/form-heavy sites, providing state representation beyond URL and title?
**Outcome**: FALSIFIES (status=COMPLETE)

## Scientific Context

This experiment tests whether DOM structural features provide a state representation that captures predictive dynamical information beyond URL and title. The parent experiment (EXP-PHYSICS-34348438464) found that title-aware PMI was MEASUREMENT_INVALID due to site selection mismatch (MPA vs SPA sites). The current experiment tests a materially orthogonal hypothesis: whether the *physical structure* of the page (element counts, tree depth, interactive density) carries dynamical information that semantic identifiers (URL, title) miss.

## Key Results

### Controls

| Control | Expected | Observed | Result |
|---------|----------|----------|--------|
| Positive control (synthetic SPA) | PMI >= 0.5, p < 0.001 | PMI = 1.271, p = 0.001 | PASS |
| Null control (shuffled synthetic) | p > 0.05 | p = 0.631 | PASS |

Both controls pass, validating the PMI computation pipeline and DOM feature extraction.

### Site Results

| Site | URL PMI | DOM PMI | Improvement | DOM p-value | Data Sufficient |
|------|---------|---------|-------------|-------------|-----------------|
| TodoMVC React | 0.670 | 0.597 | -0.073 bits | 0.001 | Yes (76 transitions) |
| TodoMVC Vue | 0.751 | 0.745 | -0.006 bits | 0.001 | Yes (78 transitions) |

### Decision Rule Evaluation

| Condition | Required | Observed | Pass |
|-----------|----------|----------|------|
| DOM > URL by >= 0.1 bits on >= 2/3 sites | 2/3 sites | 0/2 sites | FAIL |
| DOM PMI sig > 0 on >= 2/3 sites | 2/3 sites | 2/2 sites | PASS |
| Positive control passes | Yes | Yes | PASS |
| Null control passes | Yes | Yes | PASS |
| Data sufficiency on >= 2/3 sites | 2/3 sites | 2/2 sites | PASS |

**Decision**: FALSIFIED-IN-SETTING — Condition 1 fails on 2+ sites (both).

## Interpretation

### 1. DOM features are informative but not superior to URL

DOM-feature PMI is significantly > 0 on both sites (p = 0.001), confirming that DOM structural features do carry predictive dynamical information about next-state transitions. However, DOM-feature PMI is *lower* than URL-only PMI on both sites (React: -0.073 bits, Vue: -0.006 bits). The structural level of description does not provide better predictive state representation than URL path alone for these TodoMVC apps.

### 2. State-space expansion without predictive gain

DOM features create a larger discrete state space (React: 25 vs 13 states; Vue: 16 vs 13 states) with more unique state-action pairs (React: 33 vs 18; Vue: 21 vs 17). However, this expansion does not translate to better predictive PMI. The additional states appear to dilute transition density without capturing action-conditioned structure that URL misses.

### 3. Entropy reduction paradox

DOM features show higher entropy reduction than URL-only (React: 5.74 vs 3.21 bits; Vue: 4.19 vs 3.38 bits), suggesting they capture more conditional uncertainty reduction. However, PMI (which normalizes by marginal probability) shows URL-only is better. This discrepancy suggests that DOM features capture more *unconditional* structure but URL-only provides better *action-conditioned* prediction relative to the state space size.

### 4. Title variance remains a dead end on TodoMVC

URL+title PMI is identical to URL-only on both sites due to zero title variance (unique_titles = 1). This confirms the parent handoff's finding that TodoMVC titles do not vary across client-side routes. Title-aware testing requires sites where titles change with navigation state.

### 5. Alpha sensitivity confirms robustness

DOM PMI is stable across smoothing values (React: 0.578–0.624; Vue: 0.738–0.756), indicating the result is not an artifact of Laplace smoothing.

## Scope and Limitations

This experiment tests a *specific* structural representation (element count, tree depth, interactive density) on *specific* sites (TodoMVC React and Vue). The falsification applies to this setting:

- **Does NOT falsify** C-WEB-DYNAMICS entirely — only this specific structural representation on these specific sites.
- **Does NOT test** more complex production SPAs where DOM structure varies more than URL structure.
- **Does NOT test** more expressive features (accessibility tree, component hierarchy, visual layout).
- **Does NOT test** adaptive discretization or learned state representations.

## Implications

### For C-WEB-DYNAMICS

The hypothesis that DOM structural features provide predictive state representation beyond URL/title is falsified on TodoMVC. However, the finding that DOM features carry significant predictive information (p = 0.001 on both sites) suggests that the structural level of description is not empty — it is just not superior to URL for these simple apps.

### For Product

Product should focus on URL/title/semantic representations for state identity. DOM structural features may be useful as a *complementary* signal (e.g., for sites where URL is ambiguous) but should not replace URL-based state identity.

### For Future Physics Work

The entropy reduction paradox (DOM has higher entropy reduction but lower PMI) warrants investigation. Possible explanations:
1. State-space dilution: more states with sparse transitions reduce PMI estimates.
2. Discretization artifacts: 5-bin quantile discretization may not capture relevant DOM variation.
3. Site complexity: TodoMVC is too simple for DOM features to provide advantage.

Future work should test on production SPAs with richer DOM evolution, use more expressive features, and explore adaptive discretization.
