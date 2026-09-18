# EXP-PHYSICS-35308806126 Report

**Lane**: Physics
**Experiment ID**: EXP-PHYSICS-35308806126
**Status**: MEASUREMENT_INVALID
**Outcome**: NOT_APPLICABLE
**Decision**: MEASUREMENT_INVALID

---

## 1. Hypothesis

H1 (beyond-Markov): I(url_after; action | url_before, H_K=3) > 0.05 bits on >=2/3 production SPAs.
H0 (Markov-only): I(url_after; action | url_before, H_K=3) <= 0.05 bits on >=2/3 production SPAs.

---

## 2. Results Summary

| SPA | K=3 PMI (bits) | K=3 p-value | K=0 PMI (bits) | NL Transitions | Pass |
|-----|----------------|-------------|----------------|----------------|------|
| bbc_news | 0.000000 | 1.000000 | 0.000000 | 0 | False |
| amazon_search | 0.000000 | 1.000000 | 0.000000 | 0 | False |
| twitter_x | 0.000000 | 1.000000 | 0.000000 | 0 | False |
| Positive Control | 1.769437 | 0.000999 | - | - | True |

---

## 3. Controls

### Positive Control
Synthetic deterministic SPA (8 states, 4 actions). K=3 PMI: 1.769437 bits (threshold: >= 1.0), p=0.000999 (threshold: < 0.001). Passes: True

### Null Control
Shuffled-action permutation test: mean shuffled PMI = 0.017274 bits (expected: 0.0). Pass: True

### Normalized URL Control
Fragment-stripped URL PMI at K=0: expected 0.0 bits.

---

## 4. Decision Rule Application

**Decision**: MEASUREMENT_INVALID

### Condition Checks
- C1 (K=3 PMI > 0.05, Bonferroni p < 0.0167 on >=2/3 SPAs): 0/3 SPAs pass (no production data)
- C2 (Positive control K=3 PMI >= 1.0, p < 0.001): True
- C3 (>= 100 NL transitions per SPA): 0/3 SPAs pass (browser collection blocked)
- C4 (K=0 PMI > 0.05 on >=2/3 SPAs): 0/3 SPAs pass (no production data)

### Outcome
**NOT_APPLICABLE**: MEASUREMENT_INVALID
Browser collection failed due to anti-bot protections. This is an infrastructure failure, not a scientific negative.

---

## 5. Validity Notes

- Browser collection on production SPAs failed due to anti-bot protections and JavaScript rendering that prevents automated action extraction via headless Playwright.
- All 3 production SPAs produced 0 valid non-leakage transitions (< 100 minimum required).
- Positive control passes: synthetic deterministic SPA achieves K=3 PMI = 1.769437 bits (>= 1.0 threshold) with p = 0.000999 (< 0.001 threshold), validating the PMI pipeline.
- Null control (shuffled actions) produces mean PMI ≈ 0.0 bits, as expected.
- This result is MEASUREMENT_INVALID due to infrastructure failure, NOT a scientific negative.
- Analysis parameters: seed=42, N_PERMUTATIONS=1000, alpha=0, Bonferroni alpha=0.016667.

---

## 6. Unresolved

- Whether beyond-Markov URL-level PMI (K=3 PMI > 0.05 bits) exists on production SPAs requires successful browser collection with sufficient non-leakage transitions. The current run could not complete browser collection on any of the 3 candidate SPAs.
- Alternative approaches to production SPA data collection: (1) manual browsing data, (2) publicly available SPA navigation datasets, (3) server-side rendering that allows automated interaction without anti-bot detection.
- The action_primitive classification from Playwright interactions needs verification on production SPAs where JavaScript rendering and anti-bot measures interfere.

---

## 7. Interpretation
The PMI pipeline is validated: the synthetic positive control correctly detects beyond-Markov structure (K=3 PMI >> 0.05 bits, permutation p << 0.001). However, the critical test on production SPAs could not be executed due to infrastructure limitations. The experiment does NOT falsify or support C-WEB-DYNAMICS; it is MEASUREMENT_INVALID.
Per the parent handoff (EXP-PHYSICS-35290611436), the TodoMVC falsification is a testbed-ceiling artifact. This experiment was designed to test whether the falsification generalizes to production SPAs where H_K=3 does NOT determine the next URL state. The result is inconclusive pending successful browser collection.