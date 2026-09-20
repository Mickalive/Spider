# EXP-INTEL-35476271877 — SNR decomposition of canonical-vs-per-task ranking instability

## Experiment identity

- experiment_id: `EXP-INTEL-35476271877`
- lane: `intel`
- claim_ids: `C-MEAS-VALID`, `C-PRODUCT-ECON`
- Frozen inputs: `request.json` (0403e9ee…), `spec.json` (c0f2730d…), `prereg.md` (150d1c8b…) — sha256 verified against `freeze.json` (12a1b945…)
- Raw evidence substrate: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json` (sha256 da30bd05…)
- Parent analysis framework: `research/experiments/EXP-INTEL-35445596324/analyze.py` (sha256 5acc3731…), whose per-iteration density machinery this run re-implements with SNR/margin/SE/margin-variance logging.

## Question and frozen decision rule

**Question:** What mechanism drives the paradoxical dissociation between the canonical recipe's high discrimination (eta2=0.9205) and low ranking agreement (55.95%) versus the per-task recipe's low discrimination (eta2=0.3664) and higher ranking agreement (78.65%) at truncated-first-20 — and does an SNR-model decomposition predict whether full-DOM element counts (n=21-82) would cross the 80% ranking-agreement threshold?

**Frozen decision rule (conjunctive):**
- C1_SNR_MODEL_VALID: SNR model predicts observed agreement at n=15 and n=20 within 10pp.
- C2_MECHANISM_IDENTIFIED: at least one of (a) margin/SE < 3, (b) CV > 0.1, (c) rho > 0.3.
- C3_EXTRAPOLATION_FALSIFIES_FULL_DOM: model predicts agreement at n=50 < 80%.
- If NOT C1 → **MEASUREMENT_INVALID regardless of C2/C3**.

## How it was measured

The frozen design is purely computational on the existing EXP-INTEL-34782350557 reconstructed per-task DOM data (7 tasks: 3 listing, 3 detail, 1 cart; truncated-first-20 locatable sample; cart excluded from margin/SNR computations due to its n=1 degeneracy). `analyze_snr.py` (stdlib-only, pure Python 3.12.14, `PYTHONHASHSEED=0` for reproducible set-iteration) re-runs the parent's recipe sampling with per-iteration density logging:

- canonical recipe: random role subset shared across tasks per iteration (parent semantics), per-iteration within-type densities;
- per-task recipe: per-task role subsets sampled independently (parent semantics);
- effective_n ∈ {5, 10, 15, 20}; 10 seeds × 1000 iterations × 2 recipes = 20,000 iterations per n (80,000 total); 10,000 observable iterations per (n, recipe) after seed/attempt bookkeeping;
- definitions: `tag_entropy x DEF-FULL-MAP` (primary) and `tag_entropy x DEF-FORM-ONLY` (comparison).

Per iteration i and page type p (listing, detail): density `d_p,i` = matched-element tag_entropy mean over the type's 3 tasks. For each recipe and n we record the per-iteration margin `M_i = mu_listing_i - mu_detail_i`, per-iteration SE `SE_i = sqrt(SE_l_i^2 + SE_d_i^2)` (within-iteration within-type SE of the mean, ddof=1), per-iteration SNR `SNR_i = M_i / SE_i`, ranking agreement (fraction of iterations with M_i > 0), eta2 for the type-rank ordering, CV of within-type densities, and pairwise correlation rho of the density time series across same-type tasks.

Raw per-iteration records are preserved in `snr_per_iteration_tag_entropy.json.gz` (all n, both definitions, both recipes) and `hybrid_per_iteration_densities_n20.json.gz` (alpha-blend exploratory at n=20).

## RAW EVIDENCE → OBSERVATION

Observations (from the preserved raw per-iteration records; see `result.json` ⇒ `observations` for the full list):

1. **SNR model (frozen form `agreement ≈ Phi(mean(SNR_i))`)** gives `0.9999999999999991` at n=15 and `1.0` at n=20, versus observed agreement `0.4996`/`0.5654` this run (frozen targets 0.4998/0.5595). Residuals: 0.5002 and 0.4405.
2. **Noise-scale mismatch.** Within-iteration within-type SE (`se_tot_mean`) is 3.8e-6 (n=5) → 1.3e-5 (n=20). The iteration-to-iteration margin variation (`margin_std`) is 5.0e-5 (n=5) → 6.2e-4 (n=20), i.e., **10–50× larger** than the SE the frozen model uses as its noise term.
3. **Margin sign crosses zero** between n=10 and n=15: -4.90e-05 (n=5), -1.35e-04 (n=10), +2.66e-05 (n=15), +3.97e-04 (n=20). Agreement follows the sign: 0%, 0%, 49.96%, 56.54%.
4. **Mechanism statistics at n=20 (canonical)**: margin/SE = 29.96; CV_listing = 0.0046, CV_detail = 0.0335; rho_listing = 1.0, rho_detail = 1.0. Per-task recipe: CV_listing = 0.78, CV_detail = 0.55; rho ≈ 0.0005–0.005.
5. **Degenerate iterations** (se_tot == 0, no matched elements): 5070/10000 at n=5, 2464 at n=10, 1230 at n=15, 599 at n=20. All contribute agreement = 0 (margin not > 0).
6. **Template invariance confirmed** on the first-20 subsample for all three page types; direct mean tag_entropy listing (2.646) > detail (2.484) confirms the direct (non-recipe) ordering direction.
7. **Baseline reproduction** (parent vs this run): canonical eta2 n20 0.9205 → 0.91945; per-task eta2 n20 0.3664 → 0.3670; canonical agreement n20 0.5595 → 0.5654; per-task agreement n20 0.7865 → 0.78; monotonic Spearman=1.0 reproduced.

## DERIVED MEASUREMENT

- **C1_SNR_MODEL_VALID = false.** Both target residuals (0.5002 @ n15, 0.4405 @ n20) exceed the 10pp threshold by ~40–50pp.
- **C2_MECHANISM_IDENTIFIED = true** — but only through the correlated-noise branch (rho = 1.0 > 0.3). margin_deficit and task_variance are false (margin/SE = 29.96; CV < 0.1).
- **C3_EXTRAPOLATION_FALSIFIES_FULL_DOM = false.** |margin| and SE power-law fits (b ≈ 0.876 and 0.878) give SNR = 10.47 at n=50 and 10.46 at n=82 → predicted agreement 1.0 (PI90 lo = 0.845 at n50, 0.693 at n82), i.e., ≥ 80% at the full-DOM midpoint.
- **Controls:** PC1 FAIL; NC1 random-noise null behaves as expected (0.499208 ≈ 50%) but the SNR model's error is an order of magnitude larger than the null's — the decomposition performs worse than random noise at the decision points; baselines B1–B4, B6 reproduce; B5 inherited (not recomputed — not needed for C1/C2/C3).
- **Alternative statistic (diagnostic):** `mean(Phi(SNR_i))` = 0.4986 (n15) and 0.5649 (n20), matching observed agreement almost exactly. This is near-tautological: with SE_i ≈ 1e-5 ≈ 0, `Phi(SNR_i)` collapses to `indicator(M_i > 0)`, so the mean of Phi is essentially the observed agreement by construction, not by mechanism.
- **Hybrid exploratory (n=20, alpha blend canonical→per-task):** max agreement 0.8406 at alpha=0.4 with eta2 0.464; max eta2 0.919 at alpha=1.0 with agreement 0.5654. No alpha in the tested grid achieves eta2 ≥ 0.80 AND agreement ≥ 0.80.

## INTERPRETATION — why the model failed and what is/is not established

**Why C1 failed (mechanism-level diagnosis, bounded to this experiment):** The frozen SNR model's noise term is the *within-iteration, within-type SE of the mean*. Under template invariance — which was verified and which the frozen design itself flagged in `measurement_validity` — tasks of the same page type are near-duplicates in truncated-first-20: identical element tags/roles/inForm/w/h; canonical densities differ only by the `elements_with_bbox` denominators (1550/1560/1564; 1215/1149/1143). The within-type density variation is therefore tiny (CV ≈ 0.005–0.034) and the SE ≈ 1e-5. The actual flipper is the *iteration-to-iteration variation of the margin itself* (margin_std up to 6.2e-4), produced by role-subset and element-subset resampling between iterations. The frozen model uses the wrong noise scale: it treats ~0 within-iteration noise as the whole noise, saturating `Phi(mean(SNR))` at 1 while the real flips come from across-iteration margin variation. This is a measurement-validity failure of the frozen decomposition, evaluated mechanically by the frozen rule.

**What the frozen rule therefore decides:** NOT C1 → **MEASUREMENT_INVALID regardless of C2/C3**. The decomposition is unreliable, so:
- the C2 correlated-noise branch (rho=1.0) cannot be read as identification of an independent instability mechanism — rho=1.0 is the mathematical consequence of template invariance plus the canonical recipe's shared role subset (same-type densities are scalar multiples);
- the C3 extrapolation (predicted ≥80% at n=50) **must not** be used to justify Docker re-collection or the full-DOM experiment; it inherits the failed model.

**Consequences for the frozen product decision (necessarily protocol-limited):**
- *Positive consequence branch (NOT C3 → SUPPORTS-FULL-DOM, justify Docker):* **not reached** — the extrapolation is gated behind C1, which failed. Docker re-collection investment is **not** justified by this run.
- *Negative consequence branch (C3 → FALSIFIES-FULL-DOM, adopt non-recipe density immediately; predict EXP-INTEL-35462974425 C6 failure):* **not reached either** — the experiment is MEASUREMENT_INVALID, not FALSIFIES. No recommendation to switch the product lane to non-recipe density can be emitted from this run.
- The correct protocol status is INCONCLUSIVE: for the decision-relevant question (does the 56% plateau persist at full DOM?) this run produces **no supported answer** — it produces a demonstrated failure of the frozen model that was supposed to answer it.

## Validity notes (summary)

- status=MEASUREMENT_INVALID / outcome=INCONCLUSIVE: a validly-completed measurement transaction whose frozen model failed its own validity gate. This is not an infrastructure failure (the run executed fully; prior transient failures in `model_execute.json` are unrelated) and not falsification (no claim is settled either way).
- Small run-to-run quantitative deviations from the parent (e.g., canonical agreement n20 0.5654 vs 0.5595) are hash-seed set-iteration effects and do not affect the verdict (residuals ~0.44–0.50 are ~2 orders of magnitude above the 10pp threshold).
- Cart n=1 degeneracy excluded by construction; non-finite per-iteration SNRs (se_tot==0) retained with explicit +inf/-inf semantics.

## Unresolved (for DIRECTOR / next DESIGN)

1. Full-DOM ranking-agreement question (n=21–82) remains **OPEN** — the frozen model-based extrapolation is unreliable and cannot substitute for the measurement.
2. H1 vs H2 vs H3 discrimination remains **OPEN** — the decomposition that would discriminate them failed its validity gate.
3. Specific smallest next step that could unblock: a **corrected SNR model using across-iteration margin_std as the noise scale** (a valid, preregistrable successor experiment) could pass a C1-equivalent validation and re-open the extrapolation question; alternatively the full-DOM measurement itself can be run if Docker re-collection becomes available.
4. Hybrid alpha-grid sweet spot at finer resolution: untested (exploratory only; not part of the frozen rule).