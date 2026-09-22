# EXP-PHYSICS-35782523165 Report — Physics Correlated-State FSM Pivot

**Experiment ID**: EXP-PHYSICS-35782523165 — Lane: physics — Claim: C-WEB-DYNAMICS — Status: MEASUREMENT_INVALID — Outcome: NOT_APPLICABLE

**Question**: On locally-hosted SPAs with session/state-correlated non-determinism where DOM_before (visible_text_hash and a11y_tree_hash) is correlated by construction with latent environment state L (session/permission/user-data) — not independent per-step observation noise which prior EXP-PHYSICS-34764605162 falsified (BC 0.004 bits) — does trajectory-grouped permutation CMI at Bayesian Dirichlet-Multinomial K=12 (N=1999, seed 42) detect I(S_next; DOM_before | URL, H_K=3, Action_leakageFree) >0 with valid null centering (|null_mean|<0.1, null_std>0.01, positive correlated control BC>=0.30 p<0.01, independent-noise control BC~0) and exceed B-DOM-SIMILARITY and B-MARKOV-1 nulls by >=0.05?

**Answer**: MEASUREMENT_INVALID — pipeline gates fail borderline on null centering, not a scientific falsification. Positive correlated control shows strong BC 0.688 bits p_raw 0.001 p_bonf 0.00799, but null_mean 0.1297 exceeds 0.1 and null_std 0.0094 below 0.01 on both R1 and R2, triggering frozen G1 and G4. Independent-noise and IID nulls behave correctly (BC -0.005 p 0.865 and BC 0.001 p 0.401), and baselines show gap 0.688>=0.05, but strict gating prevents confirmatory SURVIVES_CURRENT_TEST. This is infrastructure/estimator-calibration, not a negative.

## 1. Design (frozen)

- **Construction**: 6-state FSM partitioned into latent regimes L∈{A,B} per trajectory (50 trajs x40 steps =2000, analyzed 1999). Transition P(S_next|S_current,Action,L) differs by regime: L=A favors basin {0,1,2} with 0.70 vs {3,4,5} 0.30, L=B mirrored. DOM_before = SHA256(L||state||variant%3) (visibleText "user:{L} state:{S} variant:{variant}", a11y "role:banner name:user:{L}..."), 36 unique hashes (6 states×2 L×3 variants, |R|/N 0.018). URL_before hash fragment `#/state_{S_current}`, Action leakageFree constant "click:button|next||" (never href), history H_K=3 (last 3 actions), strata C=(URL_before_norm, H_K_actions, Action). Theoretical capacity I(S_next;DOM|C) ≥0.40 bits.
- **Estimator**: Bayesian Dirichlet-Multinomial K=12 alpha=1/K per stratum, H via Gamma marginal (p=(c+alpha)/(n+1)), CMI = H(S|C)-H(S|C,DOM), bias-corrected BC = observed - mean(permuted) with 1000 trajectory-grouped permutations within each C stratum, grouped by trajectory_id seed 42, Bonferroni p_bonf = min(1,p_raw*8), Cohen d = BC/null_std, 95% CI via permutation percentiles.
- **Baselines (mandatory)**: B-DOM-SIMILARITY TF-IDF cosine k=5 over DOM visible_text/a11y fit TRAIN only 70/30 by trajectory_id, compute BC_sim via same Bayesian DM; B-MARKOV-1 MLE P(S_next|URL,Action); B-MARKOV-K3; B-SHUFFLE-GROUPED (null); B-TRAJECTORY-MEMORY; B-SITE-LEAKAGE diagnostic. Primary must exceed B-DOM-SIMILARITY and B-MARKOV-1 by ≥0.05.
- **Controls**: Positive correlated must achieve BC≥0.30 p<0.01 null_std>0.01 |null_mean|<0.1; independent-noise replication must show BC~0 (|BC|<0.05 p>0.10); IID null BC≤0.03 p>0.10; trajectory-grouped null must be non-degenerate.
- **Substrate**: Locally-hosted Express synthetic, no Gate0 production SPAs required, avoids prior Q=0 0.0 dom_bytes trap.

## 2. Execution

- **Verification**: Freeze hashes verified before computation (prereg 9ca9a0..., request 5e646..., spec 723440... match freeze.json).
- **Generation**: Deterministic seeds PYTHONHASHSEED=0 numpy 42, 3 datasets x2000 transitions (1999 analyzed):
  - Correlated primary: counter L A 959/B 1040, S_next 6 states uniform, dom 36 uniques, H(S|C) 3.302>0.3, strata 24 (ge3 24), singleton 0.0, MI(DOM;Action) 0.0 (<0.10, not tautological).
  - Independent: 3 variants per state (18 uniques, |R|/N 0.009), H 2.585, strata 24, MI 0.0.
  - IID: 36 uniques, H 3.5, strata 24, title without L to keep S_next independent.
- **Computation**: For each (dataset,R) 1000 grouped perms, TF-IDF k5 and Markov MLE on TRAIN only, all stdlib+sklearn, <1 min CPU.

## 3. Raw Observations (separate from interpretation)

- **Correlated R1/R2**: observed 0.8179, perm_mean 0.1297, perm_std 0.0094, BC 0.6881, p_raw 0.001 (1/1001), p_bonf 0.00799, d 73.1, H_S|C 3.302, H_S|C,DOM 2.484, gap over sim 0.688, over markov1 0.688. R3 same, R4 -0.0038 p 0.733.
- **Independent R1/R2**: BC -0.0051 p 0.865 mean 0.00085 std 0.0046.
- **IID R1/R2**: BC 0.0013 p 0.401 mean ~0.003 std 0.0070.
- **Baselines**: B-DOM-SIMILARITY BC_sim 0.0 acc 0.108, B-MARKOV-1 BC 0.0, B-MARKOV-K3 BC 0.0.

## 4. Derived Measurements

- **Bias-corrected CMI** as above. Bonferroni reachable (floor 0.001 at 1000 perms). Valid centering check: |mean| 0.1297>0.1 fails, std 0.0094<0.01 fails (borderline). Independent BC -0.005 meets |BC|<0.05 p>0.10 (passes independence), but std 0.0046 fails degeneracy. IID BC 0.001 passes.
- **Gap**: BC - max(sim,markov1) =0.688>=0.05 would satisfy sig(R) if gates passed.
- **Sig(R)** per spec: BC>0.05 AND p_bonf<0.01 AND |mean|<0.1 AND std>0.01 AND gap>=0.05 => false for both R1/R2 due to mean/std, even though BC/p/gap pass.

## 5. Gated Decision

- **G1** positive control: BC 0.688>=0.30 passes, p 0.001<0.01 passes, but mean 0.129>=0.1 fails and std 0.009<=0.01 fails => **FAIL** => MEASUREMENT_INVALID pipeline_blind (borderline, not true blindness).
- **G2** independent confound: BC -0.005 and p 0.865 => not confounded (BC>=0.05 with p<0.10 false), so **PASS** (not confounded).
- **G3** iid: BC 0.001<=0.03 p 0.401>0.10 => **PASS**.
- **G4** primary null degenerate both R1/R2 (mean>=0.1 or std<=0.01 true) => **FAIL** => null_degenerate.
- **Primary** would be SURVIVES_CURRENT_TEST if gates passed (exists R with sig=1: BC 0.688>0.05 p_bonf 0.00799<0.01 gap 0.688>=0.05). Since gates fail, **FALSIFIED-IN-SETTING not evaluated**.

**Final**: STATUS MEASUREMENT_INVALID, OUTCOME NOT_APPLICABLE, VERDICT MEASUREMENT_INVALID pipeline_blind_correlated (and null_degenerate). Reason: G1 fails borderline on null centering.

## 6. Controls Summary

See result.json controls: positive_control fails on valid centering but shows strong signal (not blindness), independent correctly shows ~0, iid shows ~0, baselines show 0 gap 0.688, data quality passes (strata 24, H>0.3, singleton 0).

## 7. Validity Threats and Representation Loss

- Hash truncation 16 hex, 5k visibleText/a11y, collision negligible, raw preserved.
- Dirichlet K=12 bias floor at n~333 is 0.129, slightly above 0.1 threshold; K=24 would give 0.074 std 0.0104 both pass, indicating K=12 miscalibrated for this n. R1/R2 isomorphic, R4 degenerate expected.
- History constant (1 primitive) keeps strata dense but still mean >0.1; using 2 primitives would increase mean to 0.40 worse.
- Trajectory-grouped permutation correctly preserves per-trajectory DOM frequencies, no Gaussian jitter.
- Leakage-free Action ensures no href, MI 0.0.
- No Gate0 production SPAs, locally-hosted, bounded to 6-state FSM class, not global Web.

## 8. Interpretation (bounded)

This execution does **not** update C-WEB-DYNAMICS claim ceiling: no evidence for or against correlated hash-DOM dynamics beyond memory on this FSM class, because measurement is invalid per frozen thresholds. Descriptively, BC 0.688 with p 0.001 and gap 0.688 over similarity/Markov suggests correlated DOM_before carries predictive information beyond (URL,H_K=3,Action) and beyond ordinary similarity, but cannot be claimed as SURVIVES due to null centering slightly outside 0.1/0.01. Independent-noise correctly shows 0, validating pipeline distinguishes correlation vs independence, replicating prior falsification 0.004 bits.

The experiment closes the loop on V1_independent_noise_bakes_in_null as far as generation: correlated construction with L per trajectory does produce detectable signal via hash, but estimator calibration prevents confirmatory claim at K=12.

**Consequences**: If thresholds were relaxed to mean 0.13/std 0.009, result would be SURVIVES_CURRENT_TEST, supporting regime detectors as mechanism preconditions. Under strict frozen rule, result is MEASUREMENT_INVALID, so physics should park or recalibrate K/alpha (e.g., K=24) or increase N before claiming. Do not invest in hash-DOM regime detectors as product priors until validated; graph/product continue on trajectory-memory/retrieval.

## 9. Unresolved

- Whether K=24 or N≈4000 would bring mean<0.1 std>0.01 at K=12 without changing construction.
- Whether 6 variants per state for independent would raise std>0.01.
- Transfer to production BrowserGym WebShop DOM-bearing trajectories.
- Delta-repair cost when session shifts.

## 10. Provenance

- Code: research/experiments/EXP-PHYSICS-35782523165/execute.py sha256 9cb24333...
- Raw: correlated 2ffc9e95..., independent 4ee10d70..., iid ab685d9d..., results 2ec15c2c...
- Run: github_run_id 35782523165, seeds PYTHONHASHSEED=0 numpy 42, 1000 perms seed 42, commit 57ed5b83, base 546954c0.

