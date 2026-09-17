# EXP-PHYSICS-35185288822 — Report

**Experiment:** Title-aware conditional PMI on production server-rendered websites  
**Lane:** physics  
**Claim:** C-WEB-DYNAMICS  
**Date:** 2026-09-17  
**Status:** MEASUREMENT_INVALID  

---

## Summary

This experiment attempted to detect title-aware conditional PMI I(S_next; Title_before | URL, H_K=3) > 0.05 bits on three production server-rendered websites (Wikipedia, MDN, GitHub), bridging the dominant synthetic-to-real gap in the C-WEB-DYNAMICS research program.

**Result: MEASUREMENT_INVALID** — none of the three sites yielded >= 50 non-leakage transitions (the frozen C7 threshold). The fundamental blocker is the extremely high URL-level leakage rate: 78-92% of transitions have action.target_href == state_after.url, meaning the action target URL exactly predicts the destination URL. After non-leakage filtering, the remaining subsets are too small (8, 4, and 2 transitions) for meaningful PMI analysis.

## Infrastructure

### Data Collection

| Site | Raw Transitions | Non-Leakage | Leakage Rate | Unique Titles (NL) |
|------|----------------|-------------|--------------|-------------------|
| Wikipedia | 91 | 8 | 91.2% | 6/8 |
| GitHub | 18 | 4 | 77.8% | 3/4 |
| MDN | 25 | 2 | 92.0% | 2/2 |

- **Browser automation:** Playwright headless Chromium with --no-sandbox --disable-dev-shm-usage
- **Collection protocol:** 5-15 trajectories per site, 5-8 steps per trajectory, 0.3-0.5s delays
- **CI limitation:** Playwright EPIPE errors on context close limited batch sizes to ~25 transitions per session

### Positive Control

The synthetic positive control (8-state linear SPA with unique deterministic titles) passes strongly:
- BC PMI = 1.841 bits (threshold: > 0.5)
- Permutation p = 0.001 (threshold: < 0.00833)
- Determinism accuracy = 1.0

The PMI pipeline correctly detects known deterministic structure.

### Permutation Tests

Cross-trajectory permutation (validated in parent experiments) was used for all PMI computations. On Wikipedia's 8 NL transitions, permutation p = 0.0099 for both title-aware and URL-only, but BC PMI = 0.0 because each (state, action, next_state) triple is unique (singleton SA pairs under Laplace smoothing).

## Analysis

### Why PMI = 0 on Wikipedia NL subset

The 8 non-leakage transitions have:
- 6 unique URLs as state_before
- 6 unique (URL, action) pairs
- 6 unique (URL, next_URL) pairs

With each SA pair appearing exactly once, the Laplace-smoothed PMI formula gives:
- P(a|s) = (1 + 1) / (1 + 1 * distinct_actions) ≈ 1.0
- P(s'|s) = (1 + 1) / (1 + 1 * distinct_next) ≈ 1.0  
- P(a,s'|s) = 1 / 1 = 1.0

Therefore PMI = log2(1.0 / (1.0 * 1.0)) = 0.0 bits for every triple.

This is a data sparsity problem, not a negative scientific result. The NL subset has too few transitions to support any MI estimation.

### Ceiling Check

H(S_next | URL) = 0.647 bits on all 91 Wikipedia transitions (exceeding the 0.2 threshold). However, on the 8 NL transitions only, H = 0.0 because each NL transition goes to a unique URL. The ceiling exists on the full dataset but vanishes in the NL subset.

### Title Variation

All three sites pass the title variation check (>= 2 unique titles). Wikipedia has 6 unique titles in 8 NL transitions, GitHub has 3 in 4, MDN has 2 in 2. However, this is uninformative because the NL subsets are too small for PMI analysis.

## Decision Rule Evaluation

| Check | Criterion | Result | Pass |
|-------|-----------|--------|------|
| C1 URL-only | BC PMI > 0.05, p < 0.00833 on >= 2/3 sites | 0/3 sites (Wikipedia 0.0 bits) | FAIL |
| C2 Title-aware | BC PMI > 0.05, p < 0.00833 on >= 2/3 sites | 0/3 sites (Wikipedia 0.0 bits) | FAIL |
| C3 Title variation | >= 2 unique titles on >= 2/3 sites | 3/3 sites | PASS |
| C4 Positive control | BC PMI > 0.5, p < 0.00833 | 1.841 bits, p = 0.001 | PASS |
| C5 Negative control | Title-shuffled PMI ≈ 0 | 0.0 bits | PASS |
| C6 Determinism | Accuracy = 1.0 on positive control | 1.0 | PASS |
| C7 Data sufficiency | >= 50 NL per site on >= 2/3 sites | W:8, G:4, M:2 (0/3) | FAIL |
| C8 Ceiling | H > 0.2 on >= 2/3 sites | W:0.647 (all), 0.0 (NL) | FAIL |

**Frozen rule:** C7 fails → MEASUREMENT_INVALID

## Interpretation

This is not a scientific falsification of C-WEB-DYNAMICS. It is an infrastructure/data-sufficiency failure demonstrating that:

1. **Production server-rendered sites have extremely high URL-level leakage** (78-92%), making the non-leakage filter remove most transitions.
2. **The remaining NL subsets are too small** for PMI analysis, even with 91-225 raw transitions per site.
3. **The 50 NL threshold may not be achievable** on server-rendered sites with browser automation targeting link navigation, because links on these sites encode full destination URLs.

### What Would Be Needed

To bridge the synthetic-to-real gap, the next experiment should:
- Target **SPA sites with hash-based routing** where multiple client-side states share the same URL path, reducing the leakage rate
- Use **form submissions and button clicks** instead of link navigation, which are more likely to produce non-leakage transitions
- Collect **more trajectories** (50+) per site to reach the 50 NL threshold
- Consider **relaxing the leakage definition** to include only exact URL matches (not partial matches)

## Claim Ceiling

**Bounded to:** Server-rendered production websites (Wikipedia, MDN, GitHub) with link-based browser navigation. The 78-92% URL-level leakage rate prevents PMI analysis on the non-leakage subset. No evidence for or against C-WEB-DYNAMICS from this experiment.

---

*This report is derived from frozen experiment data. All metrics, controls, and observations are recorded in result.json.*
