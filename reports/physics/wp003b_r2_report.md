# WP-003B-R2 REPORT — Action-Conditioned Next-State Structure Under Website Holdout

**Verdict: `FALSIFIED`** (primary hypothesis H-R2, exactly as frozen in
`reports/physics/wp003b_r2_preregistration.md`).

Cycle: Physics lane cycle 1, GitHub run 32676578274. Dataset:
`wp003b_r2_v1` (681 collected / 564 confirmed transitions, 7 live sites).
Results: `results/physics/wp003b_r2_results.json`; independent verification:
`results/physics/wp003b_r2_verification.json`; compact data committed at
`data/physics/wp003b_r2_transitions.jsonl.gz`.

## 1. What was tested

Primary object per constitution §16 and the post-WP-003 directive:

    P(class(s_{t+1}) | Z(s_t), a_t)

H-R2: a multinomial logistic predictor of the coarse structural class of the
next state, trained on K-1 sites from mechanics-only state features plus the
executed action chain, predicts held-out-site next-state structure better
than strong nulls. True website holdout (leave-one-site-out). Uncertainty:
trajectory-grouped nonparametric bootstrap (1000 reps), prereg §7.

## 2. Result

| fold | n_scored | coverage | M_SA | N_PERSIST | best null | D_f |
|------|----------|----------|------|-----------|-----------|-----|
| books | 120 | 1.00 | 0.200 | 0.470 | PERSIST 0.470 | **-0.270** |
| internet | 51 | 0.98 | 0.159 | 0.577 | PERSIST 0.577 | **-0.418** |
| openlibrary | 38 | 1.00 | 0.000 | 0.913 | PERSIST 0.913 | **-0.913** |
| quotes | 71 | 0.59 | 0.121 | 0.131 | PERSIST 0.131 | **-0.011** |
| wikipedia | 101 | 1.00 | 0.000 | 0.897 | PERSIST 0.897 | **-0.897** |

- mean D = **-0.5016**; trajectory-grouped bootstrap 95% CI
  **[-0.6467, -0.3153]** — entirely below zero.
- Fold wins: **0/5** (needed >=3). Frozen rule => **FALSIFIED**.
- The structural persistence null was the best null on ALL five adequate
  folds; on wikipedia/openlibrary, page structure simply persists under most
  actions and the learned cross-site model scores 0.000 macro balanced
  accuracy.

Falsification is robust well beyond the CI: every adequate fold is
independently negative; a maximally conservative site-level sign test gives
0/5 with no ties large enough to matter; and an internal metric-definition
correction (below) moved mean D by only +0.0033.

## 3. Exploratory localization (frozen secondary, cannot rescue primary)

In-site trajectory-split diagnostic (`exploratory_in_site_diagnostic`):
predictability EXISTS within a site but is dominated by persistence plus
nearest-neighbour memorization:

- gutenberg in-site: N_NN_ZA 0.946 vs M_SA 0.964 (+0.018);
- quotes in-site: M_SA 0.296 vs best null 0.248 (+0.048);
- books/internet/wikipedia/openlibrary in-site: M_SA <= persistence/NN.

Action-conditioning adds essentially nothing for the logistic model even
in-distribution (M_SA == M_S on 4/6 sites).

## 4. Interpretation (bounded)

At this representation granularity, environment response on these sites
decomposes into:

1. structural persistence (the dominant "dynamics"),
2. site-local retrievable regularity (NN works where you stay on-site),
3. NO transferable cross-site mapping from (Z(s), a) to coarse next-state
   structure.

This extends the WP-002B lesson ("retrieval performs at least as well as
rules") into a true website-holdout setting, and it kills the specific claim
that coarse structural response transfers across websites. It does NOT prove
web dynamics have no useful structure in general: richer state variables,
finer targets (e.g., URL-shape or DOM-diff level), and within-site regimes
remain untested here. Any such next claim needs its own preregistration.

## 5. Descriptive findings worth keeping

- **Gutenberg is structurally isolated**: all 118 confirmed transitions land
  in target classes occurring nowhere else in the corpus (coverage 0 under
  the frozen train-only vocabulary rule; fold correctly skipped, not scored).
  Cross-site "next-state class" prediction there is undefined by
  construction, not merely hard.
- Hackernews trajectories are naturally short under uniform policy because
  logged-out vote links terminate in element-free pages (~15 rows). Real
  environment response; recorded as such.
- Class support is heavily imbalanced (13 classes; largest 103, smallest 1)
  — reported per prereg §5/S3 instead of raw accuracy alone.

## 6. Identifiability-gate diagnostics for WP-004 (descriptive ONLY)

Revisited-state counts exist but are small: e.g., revisited
(url_shape, action) pairs with >=2 distinct outcome classes: books 6,
quotes 5, gutenberg 5, internet 2, hackernews 1, openlibrary 2, wikipedia 3.
At structural-class level the counts are similar (max 8 on quotes). These
numbers do NOT demonstrate identifiability of a committor; WP-004 remains
**BLOCKED** per directive. A future gate attempt would need deliberate
restart designs targeting comparable states, not passive walks.

## 7. Measurement integrity record

- All prereg gates passed on the final dataset (G1 identity/alignment,
  G2 execution filter 564/681 with 117 not-ok exclusions, G3 site
  disjointness asserted per fold, G4 integer/sha256 seeds only, G5 grouped
  bootstrap, G6 train-only vocabularies with coverage reported, G7
  arithmetic recheck).
- Independent verification script (`physics/verify_r2.py`, separate code
  path): D_f recomputation matches on all folds; verdict arithmetic
  reproduces FALSIFIED; train-label shuffling collapses M_SA to 0 (model
  genuinely learns inputs); randomized features degrade it; seed-formula
  integrity PASS; softmax sanity PASS.

### Defect found and corrected during self-audit (disclosed)

The first analysis pass passed `np.arange(len(vocab))` where the frozen spec
requires the ACTUAL class-value set to `balanced_acc`, silently dropping some
present classes from the macro average and producing NaNs in the in-site
diagnostic. Because global class indices are not contiguous integers, this
was a genuine metric bug in BOTH the analysis and the first version of the
verifier (which is why they agreed). Corrected to `np.array(sorted(vocab))`
in both before acceptance; the correction implements the preregistration as
written rather than changing it. Effect on the headline: mean D changed from
-0.4983 to -0.5016; verdict unchanged. Both runs' artifacts were overwritten;
only corrected outputs are stored.

### Instrument repair before confirmatory data existed (disclosed)

A v1 collection instrument lacked navigation/snapshot retries; partial v1
data (578 rows) showed sites dying silently (gutenberg lost 7/8 trajectories;
hackernews truncated). The instrument was hardened (bounded goto retries, one
longer-settle resnapshot before declaring absorbing empty states) and the
ENTIRE corpus was recollected with identical seeds and policy. No model
outcome had been computed when this decision was made; dry-runs used reduced
bootstraps solely to debug pipeline code on partial data and are superseded.
v1 data were kept only ephemerally under /tmp.

## 8. Limitations

- Coarse 13-bucket state representation; negative result is bounded to this
  family (prereg §8 wording) and cannot be generalized to finer states.
- Raw DOM snapshots are ephemeral (/tmp policy); compact derived rows are
  committed so every number above is recomputable, but raw-page content is
  not preserved.
- Snapshot settle times differ by action type (80 ms fill/check vs 350 ms
  default) — uniform across sites/folds, part of the instrument.
- 5 adequate folds of 7 attempted meets the frozen adequacy minimum
  (>=5); hackernews (n=15) inadequate; gutenberg coverage-0.
- Live-site walks are seed-reproducible in policy but not bitwise
  reproducible in environment content; disclosed by design.

## 9. Recommended next question (for Lane Director)

The highest-information next step is NOT another predictor family at this
granularity (persistence + memory already saturate it). Either (a) move the
target one level finer — predict URL-shape/DOM-diff response given (s,a)
with the same holdout discipline, where persistence is NOT automatically
near-perfect — or (b) design a deliberate restart/revisit collection protocol
aimed at the WP-004 identifiability gate, since passive walks yield too few
comparable-state branches. Option (a) directly tests whether transferable
response signal exists anywhere below the structural-class abstraction;
option (b) unblocks (or definitively fails) the committor program.
