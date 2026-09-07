# EXP-PHYSICS-33965269281 Report

## Experiment: Playwright-Based Action-Conditioned Transition Substrate

**Lane**: Physics
**Experiment ID**: EXP-PHYSICS-33965269281
**Status**: MEASUREMENT_INVALID
**Outcome**: NOT_APPLICABLE

---

## 1. Hypothesis

The previous MEASUREMENT_INVALID result (EXP-PHYSICS-33788037373) was caused by
representation degradation: HTTP fetch discarded DOM structure, accessibility tree,
and form signals. With Playwright-based collection extracting full DOM structure,
accessibility tree, link texts, tag counts, and form signals, the corrected substrate
will reveal action-conditioned transition structure on live Web pages.

---

## 2. Results Summary

### Positive Control
- **Transitions**: 600
- **Action-Conditioned Accuracy (held-out)**: 1.0000
- **Action-Frequency Accuracy (held-out)**: 0.6778
- **Shuffle Accuracy**: 0.3500
- **diff_SA_vs_shuffle**: 0.6500
- **diff_SA_vs_AF**: 0.3222
- **Memorization Ratio**: 1.00

### Null Control
- **Transitions**: 300
- **Action-Conditioned Accuracy (held-out)**: 0.0000
- **diff_SA_vs_shuffle**: -0.0333

### Live Tests

**Wikipedia**:
- Transitions: 880
- Trajectories: 110
- Action-Conditioned Accuracy (held-out): 0.0303
- Action-Frequency Accuracy (held-out): 0.1515
- SA vs Shuffle Diff: 0.0227
- Memorization Ratio: 32.95

**Python Docs**:
- Transitions: 880
- Trajectories: 110
- Action-Conditioned Accuracy (held-out): 0.2424
- Action-Frequency Accuracy (held-out): 0.4015
- SA vs Shuffle Diff: 0.0871
- Memorization Ratio: 4.12

---

## 3. Permutation Tests

| Condition | Observed Diff | p-value | Significant? |
|-----------|--------------|---------|--------------|
| positive_SA_vs_shuffle | 0.6000 | 0.0000 | YES |
| positive_SA_vs_AF | 0.3222 | 0.0000 | YES |
| null_SA_vs_shuffle | 0.0111 | 0.2410 | NO |
| live_wikipedia_SA_vs_shuffle | 0.0189 | 0.0000 | YES |
| live_python_docs_SA_vs_shuffle | 0.1023 | 0.0000 | YES |

### Bonferroni Correction (6 comparisons)

| Site | Raw p-value | Corrected p-value | Significant? |
|------|------------|-------------------|--------------|
| live_wikipedia_SA_vs_shuffle | 0.0000 | 0.0000 | YES |
| live_python_docs_SA_vs_shuffle | 0.0000 | 0.0000 | YES |

---

## 4. Validity Gates

- VALIDITY GATE FAILURE: see validity checks above
- Validity gate target_href_encoding FAILED: ['target_href equals source URL: https://en.wikipedia.org/wiki/Samsung_Browser', 'target_href equals source URL: https://en.wikipedia.org/wiki/-shat', 'target_href equals source URL: https://en.wikipedia.org/wiki/-shat', 'target_href equals source URL: https://en.wikipedia.org/wiki/CSS', 'target_href equals source URL: https://en.wikipedia.org/wiki/CSS']
- REPRESENTATION: Playwright-based collection with full DOM, accessibility tree, link texts, tag_counts, form_signals
- REPRESENTATION LOSS: No visual layout or CSS structure
- REPRESENTATION LOSS: No interaction history (hover, scroll, focus)
- REPRESENTATION LOSS: Accessibility tree may be incomplete on some pages
- REPRESENTATION LOSS: Query string stripped from URL
- COLLECTION: Chromium headless, JavaScript enabled, domcontentloaded wait
- FIX APPLIED: target_href = destination URL (not source URL as in EXP-PHYSICS-33788037373)
- FIX APPLIED: Full state representation stored in raw data
- FIX APPLIED: Bonferroni correction for 6 comparisons

---

## 5. Observations

- Positive control: 600 transitions, SA held-out acc=1.0000, AF held-out acc=0.6778, diff_SA_vs_AF=0.3222
- Null control: 300 transitions, SA held-out acc=0.0000, diff_SA_vs_shuffle=-0.0333
- Live wikipedia: 880 transitions, 110 trajectories, SA held-out acc=0.0303, diff_SA_vs_shuffle=0.0227
- Live python_docs: 880 transitions, 110 trajectories, SA held-out acc=0.2424, diff_SA_vs_shuffle=0.0871

---

## 6. Interpretation

### Representation
This experiment uses Playwright-based collection with:
- Full DOM structure (tag counts for 11 categories)
- Accessibility tree (ARIA roles and names, up to 30 per page)
- Link texts (first 30 visible, sorted and deduplicated)
- Form signals (has_form, has_input, has_select, has_textarea)
- target_href = destination URL (FIXED from prior experiment which used source URL)

### Prior Experiment Comparison
EXP-PHYSICS-33788037373 used HTTP fetch with URL-only state representation.
Best result: Python docs diff_SA_vs_shuffle = 0.030, SA==AF, p_corr=0.096 (NOT significant).
State representation was degraded (URL-only, no DOM/accessibility tree).

### Positive Control
The positive control achieves 100.0% held-out accuracy with SA > AF (diff = 0.3222), confirming the pipeline can learn deterministic transitions with overlapping actions.

### Null Control
Null control SA held-out accuracy: 0.0000. diff_SA_vs_shuffle = -0.0333.

### Live Web Structure
- **Wikipedia**: diff_SA_vs_shuffle = 0.0227
- **Python Docs**: diff_SA_vs_shuffle = 0.0871

---

## 7. Verdict

**NOT_APPLICABLE**

Measurement invalid: see validity notes above.

---

## 8. Validity Threats

1. **Synthetic-to-real gap**: Positive control validates pipeline, not Web dynamics.
2. **Multiple comparisons**: 6 comparisons (3 null tests x 2 sites), Bonferroni conservative.
3. **Sample size**: Target 100+ trajectories per site. Actual counts may vary.
4. **Navigation depth**: Limited to 8 steps per trajectory.
5. **Link selection**: Uniform random over available links (no content-aware selection).
