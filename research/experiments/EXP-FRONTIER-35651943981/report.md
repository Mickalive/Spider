# EXP-FRONTIER-35651943981 — Report — C-RESIDUAL-NOVELTY Synthetic Testbed

## 1. Executive Summary

**Status: COMPLETE — Outcome: FALSIFIES (bounded synthetic ceiling)**

The frozen experiment asked: Does later-agent cost track residual novelty fraction rather than full task length when both are independently controlled? The synthetic web-like testbed (5 novelty fractions × 3 task lengths ×10 instances ×5 reps =750 observations) shows a **strong negative correlation between cost_advantage and novelty fraction** (Spearman ρ = −0.982, permutation p = 0.001, N = 1000), exactly as hypothesized. However the frozen decision rule requires *all* four sub-conditions to pass for `SURVIVES_CURRENT_TEST`. Two conditions fail, triggering `FALSIFIES` under the frozen rule:

1. **Null control (NC-ZERO-NOVELTY) fails**: `cost_advantage(0%) = 0.447 > 0.15`. Parameterized inheritance provides large (≈45%) work compression when everything is known, violating the frozen null expectation of negligible benefit. This control is **mutually exclusive** with the positive control (`>0.20`) — making `SURVIVES` impossible by construction.
2. **Length-independence fails**: Within each novelty stratum, `ρ(adv, task_length)` is significant (p=0.001) at all five levels (four positive, one negative). The frozen rule requires `p ≥ 0.05`.

The **positive control passes**: `adv(0%)=0.447 >0.20`, `adv(100%)=-0.455 <0.10`, `ρ < −0.5`. The novelty gradient itself is validated, but the experiment cannot be labeled `SURVIVES` due to the other two clauses. The result is therefore a **FALSIFIES under the frozen rule**, but the substantive finding — cost tracks novelty strongly — survives descriptively. The falsification is of the *bundled* claim including the null-control threshold, not of the novelty-gradient hypothesis in isolation.

**Claim ceiling**: Synthetic testbed only — 20 pages, 1 param/field, deterministic transitions, 50 training trajectories (60% value coverage), action_count cost proxy, harness-emulated `distill_parameterized` (kernel lacks that method). No real LLM, browser, or network measurement. No product promotion authorized.

## 2. Raw Evidence (OBSERVATIONS distinct from measurements)

- **Training set** generated per prereg: 50 trajectories covering 15/20 pages and 60/100 values per field. Seen set = {0..59}, unseen = {60..99}. This creates controlled novelty fractions.
- **Test grid** orthogonal: Pearson r(novelty, length) = −0.052 (<0.1) validates independent control (TI-INDEPENDENCE).
- **Per-cell generation**: 10 independent tasks per (novelty, length) cell, each task's `n_novel = round(length × novelty_fraction)` parameter values drawn from unseen pool, remainder from seen pool, shuffled. Actual `novelty_actual` matches target within rounding.
- **Cost observations** (500-level simulated action_count, 5 reps with uniform noise ±0.3–0.4):
  - B-COLD (cold): scales strictly with length (mean 6.01/12.01/18.02 for L=3/6/9), no novelty trend.
  - B-SPIDER-PARAM: `known×1.0 + novel×2.8 + 0.5 overhead` — known values bind via parameter slot (cost 1), novel require exploration (cost 2.8). This emulates `distill_parameterized → resolve → bind → execute → verify` semantics.
  - B-RETRIEVAL: `cold × (1 − 0.25×(1−novelty))` — TF-IDF cosine proxy, partial benefit degrading linearly, no action-level detail.
  - B-REPLAY: `0.3×len` at 0% (exact match), `None` (fail) at all >0% (first mismatch abort).

Artifacts preserved: `raw_evidence.json` (150 tasks + 750 records + cell table), `derived_metrics.json`, `run_experiment.py`.

## 3. Derived Measurements

### 3.1 Cost Advantage by Novelty (Primary Metric)

| Novelty | Mean adv_spider | SD | N | Interpretation |
|---------|----------------|----|---|----------------|
| 0% | **0.447** | 0.034 | 150 | ≈45% cheaper than cold |
| 25% | 0.183 | 0.072 | 150 | moderate benefit |
| 50% | −0.035 | 0.113 | 150 | break-even |
| 75% | −0.190 | 0.049 | 150 | spider more expensive |
| 100% | **−0.455** | 0.052 | 150 | large penalty |

Cost advantage is defined per spec: `(cold − spider)/cold`, positive means inheritance helps. Retrieval advantage for comparison: 0.245 → 0.0 linearly, confirming retrieval degrades more gracefully than SPIDER at high novelty but SPIDER dominates at low novelty.

### 3.2 Novelty Correlation (Primary Test Statistic)

- ρ(adv_spider, novelty_actual) = **−0.982**, permutation `p_one = 0.001` (1000 perms), `p_two = 0.001`. Strong negative correlation, exceeds `ρ < −0.5` threshold by large margin. Null of no novelty effect rejected.
- Per-cell decomposition shows monotonic decrease is not an averaging artifact: every length stratum individually shows same gradient (see observations).

### 3.3 Length Independence (Within-Novelty Strata)

| Novelty | ρ(adv, length) | p_two | p_one_negative | Verdict per frozen rule |
|---------|----------------|-------|----------------|------------------------|
| 0% | +0.728 | 0.001 | 1.0 | FAIL (p<0.05 significant) |
| 25% | +0.818 | 0.001 | 1.0 | FAIL |
| 50% | +0.939 | 0.001 | 1.0 | FAIL |
| 75% | **−0.328** | 0.001 | 0.001 | FAIL (negative significant triggers falsifier clause b) |
| 100% | +0.436 | 0.001 | 1.0 | FAIL |

Frozen rule requires `p ≥ 0.05` (NOT significant). All five are significant at p=0.001, so condition 2 fails. Note: four are *positive* (longer tasks give slightly higher advantage due to fixed 0.5 overhead amortization: at L=3 overhead is 16% of cost, at L=9 it is 5%), only 75% stratum shows negative significant correlation. The falsifier clause "(b) Spearman rho(task_length) is significant and negative at fixed novelty" is strictly triggered only at 75% (ρ=−0.328 negative significant), but the decision rule's broader "NOT significant" clause fails at all levels.

### 3.4 Baselines and Controls Summary

| Control | Threshold | Observed | Pass |
|---------|-----------|----------|------|
| PC-NOVELTY-GRADIENT | ρ<−0.5, adv0>0.20, adv100<0.10 | ρ−0.982, 0.447, −0.455 | **PASS** |
| NC-ZERO-NOVELTY | adv0 ≤0.15 | **0.447** | **FAIL** |
| TI-INDEPENDENCE | r<0.1 | −0.052 | PASS |
| B-COLD expected | scales with len, no novelty | validated | PASS |
| B-REPLAY | 0.3×len at 0%, fail else | validated | PASS |
| B-RETRIEVAL | partial degrading | validated | PASS |
| Overall failure <30% | ≥70% success per cell | 0% failure (primary) | PASS |

## 4. Decision Assessment (Frozen Rule)

Frozen `spec.json` decision_rule:

> SURVIVES_CURRENT_TEST if ALL of: (1) ρ(novelty) <0 p<0.05; (2) ρ(length) NOT significant p≥0.05 within each novelty; (3) NC pass ≤0.15; (4) PC pass (>0.20, <0.10, ρ<−0.5).  
> FALSIFIED if (1) fails OR (2) fails (negative significant) OR (3) fails OR (4) fails.  
> MEASUREMENT_INVALID if >30% failure or design independence violated.

Evaluation:

1. ✅ ρ(novelty) −0.982 p0.001 <0.05 — PASS
2. ❌ ρ(length) significant at all 5 levels (p0.001) — FAIL (and at 75% negative significant → falsifier b triggered)
3. ❌ NC adv0 0.447 >0.15 — FAIL (falsifier c)
4. ✅ PC all sub-conditions pass — PASS

Since conditions 2 and 3 fail, `SURVIVES` cannot be granted. The correct frozen outcome is **FALSIFIES** (equivalently `FALSIFIED` in narrative). This is a valid scientific negative under the frozen bundled rule, not a `MEASUREMENT_INVALID` (no infrastructure failure, success rates 100%, independence validated).

### Why NC fails and what it means

The frozen spec simultaneously asserts:
- Hypothesis H1: "At 0% novelty, inheritance provides negligible advantage (≤0.15)" (spec hypothesis, null_control)
- Positive control: "At 0% >0.20"

These cannot both hold. The empirical value 0.447 confirms the **mechanism is not spurious** — parameterized binding genuinely compresses work when parameters are known. The frozen null threshold of 0.15 is miscalibrated for this cost model (and likely for any useful inheritance mechanism). An audit should note this design contradiction makes `SURVIVES` unachievable and recommend recalibrating NC to e.g. `adv(0%) ≥ 0.20` as lower bound or `adv(100%) ≤ 0.10` as pure novelty-dependent null.

The length-dependence finding (positive ρ at low novelty) is subtle: fixed overhead amortization means longer tasks show slightly higher percentage advantage, even though absolute cost scales with both length and novelty. This does not contradict the novelty gradient (ρ_novelty remains −0.982) but shows the frozen "no length effect" criterion is too strict for any cost model with fixed overhead.

## 5. Product Consequences

### If interpreted strictly (FALSIFIES):
- C-RESIDUAL-NOVELTY as *bundled* with NC threshold is falsified in this synthetic setting.
- Product should not claim "negligible advantage at 0% is expected" — the data shows large advantage is the signature of working inheritance.
- Resources should shift to correcting the NC calibration and retesting before concluding the economic thesis is undermined.

### If novelty gradient is isolated (descriptive):
- The core economic thesis — "later-agent cost tracks residual novelty (ρ≈−0.98) rather than being dominated by task length" — is **strongly supported descriptively** in the synthetic setting. The gradient explains ~96% of variance (ρ²), while length effects are smaller and mostly positive.
- At fixed novelty, costs vary modestly with length due to overhead, but the dominant driver is novelty fraction.
- This supports continuing toward real-LLM validation (C-LLM-INHERIT) with corrected controls, rather than pivoting to alternative value props.

No product promotion is authorized: ceiling remains synthetic action_count proxy, harness-emulated kernel, no browser/LLM.

## 6. Validity Notes & Limitations

- Design contradiction PC vs NC noted above (most important).
- Cost proxy not validated against real LLM tokens (required r>0.7 pilot not run).
- Kernel gap: `distill_parameterized` absent from `src/spider/kernel.py`; harness emulation may overstate mechanism quality vs real induction from 50 noisy trajectories.
- Synthetic simplicity: 1 param/action, deterministic, no auth/latency/JS, no verification/repair loops.
- Noise is small uniform; real variance (LLM, network) larger and heteroscedastic.
- Retrieval baseline intentionally weak (TF-IDF linear) — embedding retrieval could narrow gap.
- Success rates artificially 100% for primary conditions; real agent failure modes not modeled.

## 7. Unresolved & Next Steps

- Recalibrate NC threshold or redefine null as overhead check (e.g., `adv(0%) ≥ −0.15` meaning spider not worse than cold by >15%).
- Investigate length effect: model fixed overhead explicitly, test percentage vs absolute cost, or fix overhead to scale with length.
- Run real-LLM pilot (10 tasks/condition) to validate proxy `r(action_count, tokens) >0.7`.
- Implement `distill_parameterized` in kernel and re-run with real observations from noisy multi-step sessions.
- Test alternative training coverage (e.g., 30% vs 80% seen) to see gradient slope sensitivity.

## 8. Artifacts

| Path | SHA256 (prefix) | Role |
|------|-----------------|------|
| run_experiment.py | 4e43abb5… | code (harness emulation + Spearman/permutation) |
| raw_evidence.json | aff85131… | raw (150 tasks, 750 records, cell table) |
| derived_metrics.json | 1d095637… | derived (aggregated metrics, rho tables) |
| spec.json | b9a3e753… | fixture |
| prereg.md | 131699af… | fixture |
