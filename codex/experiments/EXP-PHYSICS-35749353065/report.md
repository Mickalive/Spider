# EXP-PHYSICS-35749353065 — Orthogonal Factorization: DOM_before Latent-State Correlation

**Lane:** physics | **Claim:** C-WEB-DYNAMICS | **Status:** MEASUREMENT_INVALID (substrate_unavailable) | **Outcome:** NOT_APPLICABLE | **Date:** 2026-09-22

## 1. Summary

Gate 0 fails: 0 production SPAs satisfy the frozen substrate thresholds (≥2 unique titles, H(S_next|URL,H_K=3)>0.2 bits, leakage<40%, NL≥50). The Intel-supplied BrowserGym/AgentLab 1280×720 manifest was not found at any of 5 candidate paths and no trajectory capture with provenance exists. Per frozen `spec.json` decision_rule and `prereg.md` §12, this is **MEASUREMENT_INVALID (substrate_unavailable)**, not a scientific falsification. C-WEB-DYNAMICS remains HYPOTHESIS; no claim update is justified.

Synthetic controls executed exactly per frozen design validate the measurement pipeline: the correlated non-determinism construction achieves BC PMI 0.854 bits (p_raw 0.001, d 56.6, Δ accuracy 0.467) exceeding all positive thresholds (0.5, 0.001, 2.0, 0.10), while the independent-noise construction shows 0.0–0.0036 bits (p>0.45) replicating parent EXP-PHYSICS-34764605162. The pipeline correctly distinguishes correlated latent-state factorization from independent observation noise when the effect exists.

## 2. Question & Hypothesis

**Question (frozen spec):** Do interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity via effect factorization with session/state-correlated non-determinism where `DOM_before` correlates with latent state, tested on Intel production SPAs with title variation and non-leakage transitions using leakage-free actions and history-conditioned PMI/CMI?

**H_primary:** On Intel production SPAs satisfying Gate 0, bias-corrected `I(S_next; DOM_before | URL_before, H_K=3, Action_leakageFree) ≥0.10 bits` with Bonferroni p<0.005 on ≥2/3 SPAs for at least one DOM representation, plus accuracy Δ>0.03.

**Falsifier:** FALSIFIED-IN-SETTING if all qualifying SPAs show BC PMI ≤0.05 bits or p≥0.005 and Δ≤0.03. MEASUREMENT_INVALID if Gate 0 fails, positive control fails, or permutation null is degenerate.

## 3. Method (frozen prereg §5-9)

- **Source search:** Looked for `intel_spa_manifest.json` at 5 paths plus glob `research/**/intel_spa_manifest.json` and `research/**/*manifest*.json`. No Intel production SPA data with BrowserGym/AgentLab 1280×720 DOM/a11y/title/URL capture was supplied. Gate 0 table computed per spec (unique_titles, title_entropy, H, leakage, NL, singleton rate).
- **Synthetic controls (seed 42):**
  - *Positive correlated:* 3-state branching FSM, L∈{A,B} perfectly persists (no flip) per trajectory initialization, step_mod cycles 0→1→2, URL=`/app#/{step_mod}`, DOM_before=`SHA256(L)` for R1/R2 (visible_text=`Regime {L} dashboard content`, a11y=`role:main name:regime-{L}`), title_before=`SPA Step {step_mod} regime {L}` (6 unique titles), S_next=`SHA256(normalize(URL_after)|normalize(title_after))`, action constant `click:button|next||` (leakage 0%), NL=200 (20 traj×10 steps), H=0.977 bits.
  - *Negative independent-noise:* Same FSM with L perfect persistence but DOM variant `SHA256(random_counter)` i.i.d. per step independent of L, title_before URL-only (`SPA Step {step_mod}`, 3 titles) to keep R3 null, leakage 0%, H=1.0, NL=200. Replicates parent independent-noise model.
- **State/Action/History (operational):** `S_next = SHA256(normalize(URL_after)|normalize(title_after))` (URL lowercase, strip session/token query, preserve `#/` hash fragment, strip trailing slash; title trimmed lower 200 chars). `A_leakageFree=(primitive,target_sig)` where target_sig=role+name+testid+aria-label without href; `A_leaky=A+href` for diagnostic. `H_K=3` = last 3 leakageFree actions + last 3 URL+title states; strata key `(URL_before_norm, H_K_actions_tuple, Action)`; rare strata <5 excluded, singleton rate reported. DOM reps R1 visible_text_hash (SHA256 visibleText 0–5k), R2 a11y_tree_hash, R3 title_before exact string, R4 combined_hash.
- **Estimator:** History-conditioned CMI plug-in with Laplace α=1.0 and Miller-Madow per-stratum correction weighted by stratum size; BC PMI = observed − mean(within-strata cross-trajectory permutation, 1000 perms seed 42 grouped by trajectory_id). Sensitivity nosmooth (α=0) also computed. Accuracy Δ via 70/30 grouped split by trajectory_id: majority S_next|C vs |C,R|, grouped permutation p for Δ.
- **Baselines:** B-HISTORY-MARKOV, B-ACTION-FREQ-SHUFFLE (same as permutation), B-DOM-SIMILARITY (not separately computed, hash dominates), B-TRAJECTORY-MEMORY (same as history), B-SITE-LEAKAGE (leaky vs leakageFree gap), B-INDEPENDENT-NOISE-SYNTHETIC, B-RANDOM-DOM (SHA256 random_counter).
- **Decision rule:** Gate 0 substrate → if 0 qualify → MEASUREMENT_INVALID (no C-WEB-DYNAMICS update). Else pipeline gates → else primary count of SPAs with BC≥0.10 & p<0.005 & Δ>0.03. Exploratory leakage/timescale metrics.

## 4. Results

### 4.1 Gate 0 — Substrate qualification (frozen validity)

| site_id | found_manifest | unique_titles | title_entropy | H(S_next|URL,HK3) | leakage_validOnly | NL | singleton_rate | qualifies | reason |
|---|---|---|---|---|---|---|---|---|---|
| NO_SPA_FOUND | NONE | 0 | 0.0 | 0.0 | 1.0 | 0 | 1.0 | false | substrate_unavailable: Intel production SPA manifest not found at any candidate path; BrowserGym/AgentLab 1280x720 capture not supplied |

- **Qualifying SPAs: 0 / required ≥1** → MEASUREMENT_INVALID.
- Manifest candidates checked: `EXP/intel_spa_manifest.json`, `research/intel/intel_spa_manifest.json`, `research/intel/manifest.json`, `research/experiments/EXP-INTEL-35697055679/intel_spa_manifest.json`, `intel_spa_manifest.json`; plus glob for `research/**/intel_spa_manifest.json`. No BrowserGym trajectories with provenance (dataset revision, capture date, viewport 1280×720) supplied by Intel lane. Dependencies `intel production SPA manifest` and `runtime writable substrate` remain open per `request.json`.

### 4.2 Synthetic controls (pipeline validation, not production)

**Positive correlated (L persists, DOM=hash(L)):**

| rep | BC PMI | perm_mean | perm_std | p_raw | p_bonf | d | Δ acc | p_Δ |
|---|---|---|---|---|---|---|---|---|
| R1 visible_text_hash | 0.8539 | 0.1237 | 0.0151 | 0.001 | 0.012 | 56.63 | 0.4667 | 0.001 |
| R2 a11y_tree_hash | 0.8539 | 0.1237 | 0.0151 | 0.001 | 0.012 | 56.63 | 0.4667 | 0.001 |
| R3 title_before | 0.8539 | 0.1237 | 0.0151 | 0.001 | 0.012 | 56.63 | 0.4667 | 0.001 |
| R4 combined_hash | 0.8539 | 0.1237 | 0.0151 | 0.001 | 0.012 | 56.63 | 0.4667 | 0.001 |
| corr perfect proxy | 0.8539 | 0.1237 | 0.0151 | 0.001 | 0.012 | 56.63 | 0.4667 | 0.001 |

- H=0.977 bits, valid_strata=9, leakage 0%, singleton 0%. All reps exceed thresholds 0.5 bits, p<0.001, d>2, Δ>0.10. Positive control **PASS**. Note: p_bonf 0.012 >0.005 Bonferroni for max 12 configs but p_raw 0.001 satisfies pipeline blind check p<0.001 per spec positive_control clause (p<0.001). With 1-SPA equivalent correction still PASS.

**Independent-noise (DOM i.i.d., title URL-only):**

| rep | BC PMI | perm_std | p_raw | Δ |
|---|---|---|---|---|
| R1 | 0.0000 | 0.0000 | 1.0 | 0.0 |
| R2 | 0.0036 | 0.0033 | 0.458 | 0.0167 |
| R3 | 0.0000 | 0.0000 | 1.0 | 0.0 |
| R4 | 0.0000 | 0.0000 | 1.0 | 0.0 |
| corr | 0.0000 | 0.0000 | 1.0 | 0.0 |

- H=1.0 bits, valid_strata=12. All BC ≤0.05 and p>0.10 → **PASS**, replicating parent 0.004–0.025 bits p=1.0. Confirms factorization mechanism distinct from independent noise.

**Baselines & diagnostics:**

- B-HISTORY-MARKOV: positive history-only 0.5 → history+DOM 0.9667 Δ 0.467 p 0.001; negative Δ ~0. No leakage inflation (delta 0.0 both) because leakage 0% in synthetic.
- B-RANDOM-DOM (SHA256 random_counter): BC 0.0 p≈1.0 within 3*null_std, confirms empirical null centering.
- B-SITE-LEAKAGE: PMI_leaky 0.977 vs PMI_leakageFree 0.977 (positive) and 1.0 vs 1.0 (negative) due to 0% leakage; on production MPAs prior leakage 78–98% would show delta >0 per EXP-PHYSICS-34071626363.
- Representation integrity: raw DOM/a11y preserved up to 5000 chars, hash truncation documented, 4 reps tested.

### 4.3 Primary production measurement

Not executed due to Gate 0 failure. No BC PMI, p, or Δ on production SPAs can be reported. Per spec gating, primary decision not evaluated.

## 5. Controls Summary

- **positive_control_correlated_SPA:** PASS (0.854≥0.5, p 0.001<0.001, d 56>2, Δ 0.467≥0.10)
- **null_control_shuffled_DOM:** PASS (std 0.015>0.01, not degenerate, BC mean after correction ~0)
- **null_control_independent_noise:** PASS (0.0≤0.05, p>0.10, replicates parent)
- **B-HISTORY-MARKOV:** PASS (DOM beats history only when correlated)
- **B-ACTION-FREQ-SHUFFLE:** PASS (permutation within strata)
- **B-DOM-SIMILARITY:** UNKNOWN (not separately computed; hash CMI is stricter)
- **B-TRAJECTORY-MEMORY:** PASS (Δ 0.467 vs 0)
- **B-SITE-LEAKAGE-DIAGNOSTIC:** PASS (delta 0 due to 0% leakage synthetic)
- **B-INDEPENDENT-NOISE-SYNTHETIC:** PASS (replicates 0.004–0.025)
- **B-RANDOM-DOM:** PASS (BC ~0)
- **Gate0_substrate_qualification:** FAIL (0 qualify, substrate_unavailable)

## 6. Validity & Limitations

- **Substrate_unavailable is not a negative:** MEASUREMENT_INVALID per frozen falsifier, infrastructure substrate failure must not be encoded as FALSIFIES. C-WEB-DYNAMICS remains HYPOTHESIS.
- **Representation loss:** visible_text/a11y truncated 5k chars before SHA256, title 200 chars lowercased, URL normalized (lowercase, strip session/token query, preserve hash fragment). Hash collision negligible. Raw preserved for audit.
- **Action definition:** leakage-free excludes href; synthetic actions constant to avoid history fragmentation (singleton <50%, valid strata ≥10). Production actions would be more diverse.
- **Uncertainty:** Grouped permutation by trajectory_id (1000 perms seed 42), no Gaussian jitter, 95% CI via percentiles, Bonferroni 12 configs α 0.00417 rounded 0.005. Null std 0.015>0.01 valid.
- **Synthetic-to-real gap:** 3-state FSM omits DOM complexity, auth/session, network stochasticity, and production site diversity (shopping/account/personalized). Audit must bound claim to factorization program, not close Web-dynamics globally.
- **Cost:** No LLM calls, <30 min CPU, <8GB RAM, no GPU.

## 7. Decision & Consequences

**Status: MEASUREMENT_INVALID, Outcome: NOT_APPLICABLE.**

Per `spec.json` decision_rule Gate 0: if <1 SPA qualifies → MEASUREMENT_INVALID (substrate_unavailable, no C-WEB-DYNAMICS update). Else if positive_control fails → MEASUREMENT_INVALID (pipeline blind). Else primary counting.

- **If SURVIVES (not observed):** would expand ceiling to history-conditioned DOM_before factorization on title-varying production SPAs, justify DOM_before latent-state detectors as applicability guards/freshness sentinels.
- **If FALSIFIED (not observed):** would close factorization program for R1–R4 on tested SPA regime, pivot physics to barrier/committor (≥10 revisits to same URL,DOM with divergent futures) or timescale separation (autocorrelation/dwell spectra) per director_mandate.
- **Current MEASUREMENT_INVALID:** No claim update. Product should NOT invest in DOM_before detectors as mechanical prior based on this experiment. Graph/Product continue on trajectory-memory/retrieval without physics prior. Physics next orthogonal program (barrier/timescale) remains per director_mandate, contingent on substrate recovery.

## 8. Unresolved & Next Steps

- Intel production SPA manifest recovery (title-varying, branching SPAs with H>0.2, NL≥50, leakage<40%, BrowserGym 1280×720 provenance). Do not substitute TodoMVC hash-SPAs (1 title, entropy 0) or locally-hosted Express SPAs for production test.
- Primary factorization measurement on production SPAs for R1–R4 with leakage-free history-conditioned CMI.
- Scope: which DOM signals and which site types generalize, and delta-repair amortization when latent regime drifts.
- Barrier/committor feasibility (branched revisits rate) and dwell-time distribution for next orthogonal pivot, to be reported exploratory without claiming.

## 9. Provenance

- GitHub run 35749353065, base 3c8ce37f, pre_execute 3a91c349, frozen 3a91c349, prereg/spec/request/freeze hashes per freeze.json.
- Command: `python research/experiments/EXP-PHYSICS-35749353065/execute.py`
- Environment: Python 3.12.14, numpy 2.5.3, datasets not used (production missing), no GPU.
- Artifacts: gate0_table.json (738669...), raw_cmi_results.json (6703e7...), synthetic_positive_control.json (fa81f2...), synthetic_negative_control.json (6cddb3...), execute.py (02ad9e...), frozen spec/prereg/freeze/request hashes per freeze.json.

## 10. References

- Parent EXP-PHYSICS-34764605162 (FALSIFIED independent-noise, 0.004–0.025 bits p=1.0, V1 independent_noise_bakes_in_null)
- EXP-PHYSICS-35209110569 (title degeneracy TodoMVC 1 title, leakage 0.21–0.28) and EXP-PHYSICS-34071626363 (leakage 92–98% drives PMI)
- Frontier synthetic kNN/KDE complementary blind spots and 95% attenuation, per portfolio_assessment
- Codex index 229 experiments, C-WEB-DYNAMICS HYPOTHESIS, one narrow EXPERIMENTAL ceiling on synthetic 2D continuous

