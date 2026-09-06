# EXP-PHYSICS-33788037373 Report

## Experiment: Corrected Action-Conditioned Transition Substrate

**Lane**: Physics
**Experiment ID**: EXP-PHYSICS-33788037373
**Status**: COMPLETE
**Outcome**: SUPPORTS

---

## 1. Hypothesis

After correcting three methodology defects (in-sample evaluation, invalid bootstrap,
non-discriminating positive control) identified in EXP-PHYSICS-33528829431, does the
measurement substrate reveal genuine action-conditioned transition structure on live
Web pages with navigational density?

---

## 2. Results Summary

### Positive Control
- **Transitions**: 600
- **Action-Conditioned Accuracy (held-out)**: 1.0000
- **Action-Frequency Accuracy (held-out)**: 0.6500
- **Memorization Ratio**: 1.00

### Null Control
- **Transitions**: 300
- **Action-Conditioned Accuracy (held-out)**: 0.0111
- **Action-Frequency Accuracy (held-out)**: 0.0000

### Live Tests

**Wikipedia**:
- Transitions: 192
- Action-Conditioned Accuracy (held-out): 0.0000
- SA vs Shuffle Diff: 0.0000

**Python_Docs**:
- Transitions: 184
- Action-Conditioned Accuracy (held-out): 0.0333
- SA vs Shuffle Diff: 0.0333

---

## 3. Permutation Tests

| Condition | Observed Diff | p-value | Significant? |
|-----------|--------------|---------|--------------|
| positive_SA_vs_shuffle | 0.5611 | 0.0000 | YES |
| positive_SA_vs_AF | 0.3500 | 0.0000 | YES |
| null_SA_vs_shuffle | 0.0000 | 0.7040 | NO |
| live_wikipedia_SA_vs_shuffle | 0.0000 | 1.0000 | NO |
| live_python_docs_SA_vs_shuffle | 0.0500 | 0.0000 | YES |

---

## 4. Validity Gates

- REPRESENTATION LOSS: HTTP fetch only, no JavaScript execution
- REPRESENTATION LOSS: No accessibility tree (ARIA roles, states)
- REPRESENTATION LOSS: No visual structure (CSS, layout, images)
- REPRESENTATION LOSS: Link texts may be empty (image links, aria-hidden)
- REPRESENTATION LOSS: Tag counts are aggregate, not hierarchical
- REPRESENTATION LOSS: Query string stripped from URL

---

## 5. Observations

- Positive control: 600 transitions, SA held-out acc=1.0000, AF held-out acc=0.6500
- Null control: 300 transitions, SA held-out acc=0.0111
- Live wikipedia: 192 transitions, 20 trajectories
- Live python_docs: 184 transitions, 20 trajectories

---

## 6. Interpretation

### Memorization Artifact (H1)
The memorization ratio (1.00) is modest. In-sample memorization was not the dominant artifact.

### Positive Control Discrimination (H2)
The positive control discriminates (SA > AF, p=0.0000). The measurement substrate can detect state-dependent structure when it exists.

### Live Action-Conditioned Structure (H3)
- live_wikipedia_SA_vs_shuffle: raw p=1.0000, corrected p=1.0000
- live_python_docs_SA_vs_shuffle: raw p=0.0000, corrected p=0.0000

---

## 7. Verdict

**SUPPORTS**

REPRESENTATION LOSS: HTTP fetch only, no JavaScript execution

---

## 8. Validity Threats

1. **HTTP fetch only**: No JavaScript execution, no accessibility tree. SPA pages
   may appear structurally identical across navigations.
2. **Sample size**: ~200 transitions per live site. Limited power for small effects.
3. **Multiple comparisons**: 6 comparisons (3 null tests x 2 sites), Bonferroni conservative.
4. **Synthetic-to-real gap**: Positive control validates pipeline, not Web dynamics.
5. **Link text representation**: Empty link texts (image links) reduce state information.
