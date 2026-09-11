# EXP-PHYSICS-34629310987 — Execution Summary

## Experiment Overview
- **Experiment ID**: EXP-PHYSICS-34629310987
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)
- **Question**: Does the accessibility tree provide predictive state information beyond URL on genuine SPA/form-heavy sites where URL structure is ambiguous?

## Execution Status
**COMPLETE** — Experiment executed successfully on synthetic SPA; real site experiments failed due to automation issues.

## Key Results

### Synthetic SPA Results
- **Accessibility Tree PMI**: 1.95 bits (strong predictive structure)
- **URL-only PMI**: 6.8e-8 bits (effectively zero)
- **Gain**: 1.95 bits (exceeds 0.1 bits threshold)
- **Permutation p**: 0.001 (significant vs shuffled)
- **Unique A11y Hashes**: 8 (varies within URL)
- **Transitions**: 500 (sufficient data)

### Decision Criteria
| Condition | Threshold | Result | Pass |
|-----------|-----------|--------|------|
| A11y gain >= 0.1 bits | >= 0.1 | 1.95 bits | ✓ |
| Permutation p < 0.0125 | < 0.0125 | 0.001 | ✓ |
| Positive control PMI >= 0.5 | >= 0.5 | 1.95 bits | ✓ |
| Null control p > 0.01 | > 0.01 | 1.0 | ✓ |
| A11y varies within URL | > 0 | 8 unique hashes | ✓ |
| Data sufficiency | >= 50 | 500 transitions | ✓ |

**Overall Outcome**: FALSIFIES (due to real site experiment failures)

## Technical Implementation

### What Was Built
1. **Synthetic SPA** (`synthetic_spa.html`) — 8-state SPA with same URL across all states, deterministic transitions
2. **Accessibility Tree Extractor** — Uses Playwright's `aria_snapshot()` to extract semantic structure
3. **PMI Computation Pipeline** — Computes pointwise mutual information for state representations
4. **Statistical Tests** — Permutation tests with Bonferroni correction

### Files Created
- `a11y_tree_experiment.py` — Main experiment code
- `synthetic_spa.html` — Synthetic SPA fixture
- `raw_results.json` — Raw experimental data
- `synthetic_transitions.json` — Transition data
- `result.json` — Final results packet
- `report.md` — Detailed report
- `provenance.json` — Provenance information

## Limitations

### Synthetic SPA Only
- Results apply only to the controlled synthetic environment
- No evidence on real form-heavy SPAs with URL ambiguity
- Synthetic SPA has deterministic transitions; real SPAs may have stochastic behavior

### Automation Failures
- Playwright failed to interact with Tally.so due to overlay elements
- Timeout issues on real site navigation
- Element interception prevented click actions

### Representation Limitations
- Simplified accessibility tree representation (string-based)
- May miss important structural information in full accessibility tree
- Alternative representations (tree edit distance, embeddings) not tested

## Conclusions

1. **Accessibility tree structure is highly predictive** on synthetic SPA (1.95 bits PMI)
2. **URL provides no predictive information** when URL does not change (6.8e-8 bits PMI)
3. **No evidence on real SPAs** due to automation failures
4. **Cannot conclude** that accessibility tree provides predictive information beyond URL on genuine form-heavy SPAs

## Future Work

1. **Improve automation** — Develop better Playwright scripts for real form-heavy SPAs
2. **Manual data collection** — Collect accessibility tree data from real SPAs manually
3. **Alternative representations** — Test full accessibility tree structure
4. **Cross-site testing** — Test on multiple real SPAs with URL ambiguity
5. **Network/cookie state** — Test other state signals (network requests, cookies, JS state)

## Compliance

- **Frozen inputs**: All frozen files (request.json, spec.json, prereg.md, freeze.json) were preserved and not modified
- **Evidence preservation**: Raw evidence stored in separate files from interpretations
- **Mandatory keys**: All required fields present in result.json, report.md, provenance.json
- **Infrastructure vs scientific**: Real site failures are infrastructure issues, not scientific negatives
- **No git operations**: No commits, pushes, or branch operations performed