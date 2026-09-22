# EXP-PHYSICS-35756224948 Report — Physics Orthogonal Factorization (REOPEN corrected pipeline)

**Status: MEASUREMENT_INVALID substrate_unavailable (Q=0) + pipeline_blind (positive control BC 0.075 <0.5)**

## 1. Question
On Intel-supplied production SPAs satisfying Gate0 (>=2 titles, H>0.2, leakage<40%, NL>=50, strata>=10, singleton<50%) with BrowserGym/AgentLab 1280x720 provenance, does history-conditioned CMI I(S_next;DOM_before|URL,H_K=3,Action_leakageFree) with trajectory-grouped permutation (resampling unit trajectory_id, 1000 perms) and restored positive control (P(L flips)=0.3, DOM=SHA256(L||step_mod)) achieve BC PMI>=0.10 bits, Bonferroni p<0.005 and delta accuracy>0.03 on >=1/2 SPAs?

## 2. Design Summary (frozen)
- **Hypothesis:** DOM_before proxies latent regime L correlated with stochastic branch P(S_next|S_current,A,L) beyond (URL,HK=3,Action). Predicts BC>=0.10 Bonferroni p<0.005 delta>0.03 on >=1/2 SPAs for R1 or R2.
- **Falsifier:** 0/qualifying SPAs achieve thresholds => FALSIFIED-IN-SETTING for hash-DOM factorization on this regime (bounded).
- **Gate0:** Intel manifest intel_spa_manifest.json with provenance, SPA qualifies only if unique_titles>=2, H>0.2 bits (>=5 per stratum), leakage<40%, NL>=50, strata>=10, singleton<50%. If 0 qualify => MEASUREMENT_INVALID.
- **Estimator:** history-conditioned CMI I(S_next;DOM_before|C) C=(URL_before,HK=3,Action), Laplace alpha=1.0 + Miller-Madow per stratum weighted, BC=observed - mean(grouped permuted) 1000 perms seed 42 grouped by trajectory_id.
- **Baselines (all frozen executed):** B-HISTORY-MARKOV, B-ACTION-FREQ-SHUFFLE, B-DOM-SIMILARITY (kNN/TFIDF cosine k=5), B-TRAJECTORY-MEMORY, B-SITE-LEAKAGE-DIAGNOSTIC, B-INDEPENDENT-NOISE-SYNTHETIC, B-RANDOM-DOM.
- **Controls:** Positive correlated synthetic must BC>=0.5 raw p<0.005 d>2.0 delta>=0.10; independent-noise synthetic must BC<=0.05 p>0.10.
- **Parent handoff:** EXP-PHYSICS-35749353065 MEASUREMENT_INVALID substrate_unavailable (0/5 candidates, no manifest), synthetic pipeline qualitative discrimination reproduced but deviations (item-level shuffle, P=0.0 outcome-modified, unreachable Bonferroni, degenerate nulls). This design corrects all six required_fixes.

## 3. Execution (actual)
- **Gate0 survey:** Checked 5 candidate paths: EXP/intel_spa_manifest.json, research/intel/intel_spa_manifest.json, research/intel/manifest.json, EXP-INTEL-35697055679/intel_spa_manifest.json, ./intel_spa_manifest.json. `found_manifest=null`. No research/intel/ dir, no BrowserGym trajectories. Gate rows: NO_SPA_FOUND 0 titles H 0 leakage 1.0 NL 0 singleton 1.0 qualifies false. `qualifying=0`. Published `gate0_table.json`.
- **Synthetic positive correlated:** 20 trajectories x10 steps NL=200, FSM 3-state, L∈{A,B} P(flip)=0.30 per step exactly (rng.random()<0.30), URL=/app#/{step_mod}, DOM_before=SHA256(L||step_mod) per frozen, S_next=hash(url_after|title_after regime L_next), H=0.962 bits, valid_strata 9, leakage 0%, unique_titles 6.
- **Synthetic independent-noise:** same FSM P=0.30 but DOM variant i.i.d. per step independent of L (rand_draw), title_before URL-only, H=0.986 bits.
- **CMI execution:** For each of 5 representations (R1 visible_text_hash, R2 a11y_tree_hash, R3 title_before, R4 combined, corr perfect L||step), built strata C=(URL_norm, HKactions, Action_leakageFree) filtered <5 excluded, computed observed PMI Laplace+MM weighted, ran 1000 grouped cross-trajectory block permutations (trajectory_id unit, flatten-rechunk preserving within-trajectory sequences, seed 42), computed Bonferroni p=raw*6, Cohen d, 95% CI percentiles, delta accuracy 70/30 grouped split with grouped perm p_delta.
- **Baselines:** TF-IDF cosine executed (sklearn TfidfVectorizer 500 max_features fit train only else Jaccard fallback), trajectory-memory executed, leakage diagnostic same estimator, random DOM, action-freq shuffle.
- **Barrier exploratory:** counted revisits to same (URL,DOM) with divergent futures, dwell, autocorr.

## 4. Results (raw)
### Gate0
- **Qualifying SPAs: 0/5 candidates => MEASUREMENT_INVALID substrate_unavailable** (not falsification). No production SPA primary evaluated.

### Positive correlated (P=0.30, grouped)
- R1: observed 0.07946 perm_mean 0.00423 perm_std 0.01528 **BC 0.0752** p_raw 0.001 p_bonf6 0.00599 d 4.92 ci [-0.0178,0.03927] delta 0.30 p_delta 0.01
- R2: identical 0.0752 p 0.001 d 4.92 delta 0.30
- R3/R4/corr: identical 0.0752 (all encode same L||step bit)
- **History Markov 0.483, history+DOM 0.783 delta 0.30 passes delta threshold, DOM-similarity TFIDF 0.467 (R1) /0.600 (R2) < history+DOM**
- **Threshold check:** BC 0.075 <0.5 **FAIL** despite p<0.005 and d>2.0 and delta>0.10. Theoretical channel capacity I(L;L_next)=1-H(0.3)=0.119 bits, so 0.5 unreachable by construction.

### Independent-noise synthetic
- R1: observed 0.3056 perm_mean 0.3056 BC -0.0 perm_std 0.0 p 1.0 degenerate
- R2: BC -0.0 p 1.0 std 0.0 degenerate
- Bias floor 0.305 observed due to Laplace alpha 1.0 on unique hashes; permutation invariant when each DOM unique → std 0 degenerate.

### Barrier
- branched_revisit_count 0 total 3 divergent_rate 0.0 feasible false (needs >=10).

## 5. Controls Assessment
- **Positive control:** **FAIL** (|expected BC>=0.5 raw p<0.005 d>2.0 delta>=0.10| observed BC 0.075 p 0.001 d 4.92 delta 0.30|) – BC fails, other metrics pass. Construction frozen P=0.30 DOM=SHA256(L||step_mod) exactly, grouped. Failure is threshold–construction mismatch, not estimator blindness to correlated regime (detected p 0.001 d 4.92).
- **Null shuffled DOM:** POS null well-centered |mean| 0.00423 <3*0.01528, std 0.01528>0.01 true; NEG degenerate std 0 fails std>0.01.
- **Independent-noise null:** BC passes <=0.05 p>0.10 but std 0 degenerate => MEASUREMENT_INVALID for that representation per frozen rule; matches parent degenerate finding.
- **B-HISTORY-MARKOV:** pass, baseline 0.483.
- **B-DOM-SIMILARITY:** executed as frozen (TFIDF fit train only), accuracy 0.467 vs 0.783, gap shows CMI beyond similarity but below threshold.
- **B-TRAJECTORY-MEMORY / B-ACTION-FREQ / B-RANDOM-DOM / B-LEAKAGE:** all executed, leakage delta 0.0% by construction.

## 6. Interpretation (distinct from observations)
- **Primary hypothesis NOT tested** on production SPAs due Gate0 failure; outcome is infrastructure substrate_unavailable, not scientific falsification. C-WEB-DYNAMICS remains HYPOTHESIS.
- Positive control reveals **spec inconsistency:** BC>=0.5 threshold expects I>0.5 but BSC(p=0.30) capacity is 0.119 bits; observed 0.075 is 63% of capacity and statistically significant (p 0.001 d 4.92). Pipeline is sensitive to correlated regime but threshold miscalibrated for P=0.30. Parent substituted P=0.0 to guarantee 0.5, which is outcome-informed protocol violation corrected here.
- NEG degeneracy shows Laplace hash-DOM bias floor 0.305 is permutation-invariant when DOM cardinality high; valid null centering requires coarser discretization or alpha 0, not hash.

## 7. Validity Threats
- Target leakage excluded via A_leakageFree (href never in A); synthetic leakage 0% by construction.
- Split leakage prevented via trajectory_id grouping and TFIDF fit train only.
- Grouped permutation correctly uses trajectory_id unit with flatten-rechunk; item-level would inflate perm variance (audit FINDING-2).
- Representation loss: hash truncates 5k chars, collision negligible.
- Determinism via PYTHONHASHSEED=0 numpy 42.
- H=0 ceiling avoided via Gate0 H>0.2.

## 8. Consequences
- **If SURVIVES (not observed):** would validate DOM_before latent-state detector as mechanical prior beyond memory/similarity, product applicability guard.
- **If FALSIFIED (not tested):** would bound hash-DOM factorization on this regime, pivot to barrier/committor or timescale per director_mandate.
- **MEASUREMENT_INVALID (actual):** No claim update. Report exact gate failed, per-SPA table 0 rows, unresolved substrate. Retry requires Intel manifest with title-varying branching SPAs (shopping/account/personalized) with Gate0, and recalibration of positive control threshold to <=0.10 or P to ~0.10 to make BC>=0.5 reachable, plus addressing hash degeneracy for null centering.

## 9. Evidence Paths
- `gate0_table.json` (sha256 5f7cb7e2…), `raw_cmi_results.json` (07155ecb…), `synthetic_positive_control.json` (49ab4ea1…), `synthetic_negative_control.json` (bbbcd315…), `execute.py` (79cfe181…), frozen hashes in `freeze.json`.
- Re-executable from commit 2f9520f2 with `python research/experiments/EXP-PHYSICS-35756224948/execute.py` <10 min, deterministic.

## 10. Unresolved
- Intel Gate0 manifest availability; production BC/ p /d /delta on real SPAs; threshold recalibration; null degeneracy remedy; barrier feasibility on real revisits; Playwright self-collection scope.

*Generated per packet contract; observations distinct from interpretation.*
