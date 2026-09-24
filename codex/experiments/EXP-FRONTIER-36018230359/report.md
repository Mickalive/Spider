# EXP-FRONTIER-36018230359 — Report: Residual-Novelty Verification Economics Honest Gate (Frontier PIVOT)

**Lane:** frontier | **Claim:** C-RESIDUAL-NOVELTY | **Status:** COMPLETE | **Outcome:** SUPPORTS
**Question:** After 17-deep alias tunnel bounded 21/40=0.525, does pivoting to honest residual-novelty verification economics demonstrate rho_novelty>=0.60 decoupled from length with calibrated UNKNOWN/ECE and Pareto M_total_f10 saving>=25% vs cold browsing and dominance vs flat RAG k5 on orthogonal disjoint families Jaccard<0.30?

## Summary (RAW -> OBSERVATION -> MEASUREMENT -> INTERPRETATION)

- **Raw evidence:** 36 families L 8-14 disjoint alphabets (max Jaccard 0.0000, mean 0.0000), 360 pooled tasks (72 per novelty stratum 0/25/50/75/100) +30 calib =390 per pipeline *4 =1560 honest pipeline executions with per-trajectory reset counters, family-stratified bootstrap 5000 + family-block permutation 5000 + global 5000, artifacts hashed.
- **Observation:** SPIDER rho_novelty 0.8998 95%CI [0.8791,0.9177] block p 0.00000; pooled |rho_length| 0.0391 CI [-0.0620,0.1374] p 0.4578; per-stratum rho_length all <0.20 with bootstrap upper <0.30; global shuffled |rho_nov| 0.0010 p 0.984 mean -0.0010 centered |mean|<0.05.
- **Measurement:** ECE 0.0185 upper 0.0766 (5 adaptive bins, derived softmax temp0.15+jitter), UNKNOWN precision 1.000 false_accept 0.000 pooled false 0.019, monotonicity 100% mean 12.26 >0% mean 5.33 d 5.65 p 0.0000, Pareto saving f10 34.5% CI [32.8,36.3] dominance f10 True f100 True, gap 0.899.
- **Interpretation:** Controls PC/NC all PASS per amended dual-permutation (global centered, family-block valid via coverage 36/36 per-family N>=2). S gates: S1 True S2 True S3 True S4 True S5 True S6 True. Overall survives=True. Therefore COMPLETE/SUPPORTS per frozen decision rule. See validity notes for synthetic boundedness.

## Frozen Design vs Execution

- Follows Director-mandated PIVOT with cognitive_reset true, SUPERSEDE of parent 35999373906 MEASUREMENT_INVALID, implements smallest high-information synthetic gate before live BrowserGym replication.
- Deviations from frozen spec estimated counts: pooled 360 vs spec ~192 to satisfy family coverage >=30/36 and per-family per-stratum N>=2 for valid family-block permutation (amendment justified per prereg validity threat degenerate bootstrap). All other thresholds frozen: rho>=0.60 lower>0.40, |rho_length|<0.20 upper<0.25 pooled upper<0.30 per-stratum, ECE<=0.15 upper<=0.18, precision>=0.85 false<=0.10, Pareto saving>=25% lower>15% dominance at f10/f100, honest gap>0.30, |rho_shuffled|<0.20 centered |mean|<0.05.
- Pipeline implementation: derived_context only (templates + observed key-sets), TF-IDF retrieval over train-A intents+templates, softmax temp0.15 + deterministic hashlib.sha256 jitter, UNKNOWN<0.80 gate, verify+freshness+browser_steps executed per candidate, honest sum counters with per-trajectory hard reset, no jitter/n*3200/f*6.0, within-family std>0, build cost counted offline vector-ops frozen before outcomes.

## Controls (stable IDs) PC-HONEST-COST-SANITY:True, PC-ORTHOGONAL-FAMILIES-JACCARD:True, PC-TRAIN-TEST-DISJOINT:True, PC-CALIBRATION-DERIVED:True, PC-NOVELTY-MONOTONICITY:True, PC-BUILD-COST-ISOLATED:True, NC-NO-APPLICABLE:True, NC-EMPTY-REGISTRY:True, NC-ORACLE-LEAK:True, NC-BIJECTIVE-COST:True, NC-SHUFFLED-NULL:True

- Per-control pass: PC-HONEST-COST-SANITY:True, PC-ORTHOGONAL-FAMILIES-JACCARD:True, PC-TRAIN-TEST-DISJOINT:True, PC-CALIBRATION-DERIVED:True, PC-NOVELTY-MONOTONICITY:True, PC-BUILD-COST-ISOLATED:True, NC-NO-APPLICABLE:True, NC-EMPTY-REGISTRY:True, NC-ORACLE-LEAK:True, NC-BIJECTIVE-COST:True, NC-SHUFFLED-NULL:True
- PC-ORTHOGONAL max 0.0000 mean 0.0000
- ECE 0.0185 std 0.2212 acc 0.561
- Gap 0.899

Any PC/NC failure would be MEASUREMENT_INVALID.

## Metrics (stable names)

- rho_novelty 0.8998 CI [0.8791,0.9177] p 0.00000 (family-stratified bootstrap + block perm)
- rho_length_pooled 0.0391 CI [-0.0620,0.1374] p 0.45780
- per-stratum rho_length: {'novelty_0': {'n': 72, 'rho_length': 0.0365, 'p': 0.76052, 'ci95': [-0.1295, 0.1934], 'bootstrap_upper': 0.1934}, 'novelty_25': {'n': 72, 'rho_length': -0.0718, 'p': 0.5491, 'ci95': [-0.2452, 0.0914], 'bootstrap_upper': 0.0914}, 'novelty_50': {'n': 72, 'rho_length': 0.0835, 'p': 0.48566, 'ci95': [-0.0827, 0.2526], 'bootstrap_upper': 0.2526}, 'novelty_75': {'n': 72, 'rho_length': 0.0298, 'p': 0.80402, 'ci95': [-0.1371, 0.1803], 'bootstrap_upper': 0.1803}, 'novelty_100': {'n': 72, 'rho_length': -0.0969, 'p': 0.41797, 'ci95': [-0.2728, 0.0855], 'bootstrap_upper': 0.0855}, 'length_short': {'n': 131, 'rho_length': -0.0775, 'p': 0.37879, 'threshold_q': 5.0, 'ci95': [-0.2208, 0.072], 'bootstrap_upper': 0.072}, 'length_medium': {'n': 119, 'rho_length': -0.0398, 'p': 0.66739, 'threshold_q': 9.0, 'ci95': [-0.1863, 0.1131], 'bootstrap_upper': 0.1131}, 'length_long': {'n': 110, 'rho_length': 0.1369, 'p': 0.15383, 'threshold_q': 9.0, 'ci95': [-0.0064, 0.279], 'bootstrap_upper': 0.279}}
- rho_shuffled_novelty -0.0010 p 0.984 global mean -0.0010 std 0.0524
- rho_shuffled_length 0.0008 p 0.989 mean 0.0008
- ECE 0.0185 upper 0.0766 (5 bins, derived)
- unknown_precision 1.000 false_accept 0.000 (pooled 0.019)
- m_total_f10 spider 0.002401 browse 0.003668 rag 0.002674 saving 34.53% dominance True
- m_total_f100 saving 49.26% dominance True
- honest gap 0.899
- within_family_std pooled 2.7312

## Decision Rule Application

SURVIVES iff all PCs/NCs PASS AND S1-S6 PASS per frozen thresholds. FALSIFIED-IN-SETTING if PCs/NCs PASS but any S fails (bounded). MEASUREMENT_INVALID if any PC/NC fails.

Here: PC True NC True S1 True S2 True S3 True S4 True S5 True S6 True => COMPLETE/SUPPORTS.

If SURVIVES: orthogonal disjoint synthetic gate demonstrates honest cost tracks residual novelty not length with calibrated abstention and Pareto economics, breaking 21/40=0.525 alias ceiling without 18th permutation; authorizes live replication on WebArena-Verified v2 192/36 or WebGym 300k with BrowserGym 1280x720 CDP AX>10 before PRODUCT_CORE. C-RESIDUAL-NOVELTY advances HYPOTHESIS->EXPERIMENTAL synthetic-gate-passed (not VALIDATED).

If FALSIFIED-IN-SETTING: Park synthetic residual-novelty on this fixture; pivot to barrier-physics rewind (C-WEB-DYNAMICS) or per-value alias via Runtime diverse substrate per Director dependencies, rather than repeat controlled-novelty tuning.

## Validity Threats

- Synthetic-to-live gap dominant: disjoint alphabets deliberately exceed natural 26 letters (288-504 chars) to enforce Jaccard<0.30; no inference to BrowserGym AX>10 heterogeneity; live_available false disclosed.
- Prior Laplace/hash truncation bias addressed via trajectory-grouped resampling and global permutation centering |mean|<0.05; family-block permutation now valid via coverage 36/36 per-family N>=2 (vs prior 23/36 ~1).
- Bijective cost leakage prevented via executed counters and gap>0.30; no jitter/n*3200/f*6.0.
- Calibration derived from actual retrieval scores (TF-IDF cosine + softmax temp0.15 + deterministic jitter hashlib.sha256), not hard-coded ranges; std 0.2212 >0.05, imperfect accuracy strata 0.561.
- Build cost hand-chosen risk mitigated via counted offline vector-ops frozen before outcomes (30 spider, 20 rag ops*0.00002), auditable at f10/f100 with bootstrap CI.
- Sample counts: pooled 360 exceeds spec 192 to satisfy family-block validity; disclosed and justified as minimal uplift for valid inference without changing thresholds.

## Product Consequence

Positive (SURVIVES): validates residual-novelty verification economics as higher-leverage than further alias retrieval diversity tuning on this controlled regime; prioritize honest sum-counter + calibrated UNKNOWN/ECE verification and Pareto-aware compilation over alias tuning; authorize live heterogeneous replication via Runtime/Intel dependencies.

Barrier-physics rewind deferred as second-stage contingent on FALSIFIED per Director.

## Artifacts

- research/experiments/EXP-FRONTIER-36018230359/artifacts/family_manifest.json sha bd332b2d7eca61b5ce620e410e8141392fccdd38950f718053ebead0821a761f
- research/experiments/EXP-FRONTIER-36018230359/artifacts/per_trajectory_traces.json sha 2a85896f9bb34b1b59ee6d84a31e19b13e2c6c0dd2f44a048ed54902f6c366c4
- research/experiments/EXP-FRONTIER-36018230359/artifacts/bootstrap_permutation_nulls.json sha 3c9cc7bafcb837d49357d0c0d4433a27bcc1ab8b5b21e50bbb1114e9891119fa
- research/experiments/EXP-FRONTIER-36018230359/artifacts/confidences.json sha b46feb6db4026293526d836e2c2dccc9401db9c5cbfb7ef9749df679ce38b59f
- research/frontier/run_execute_36018230359.py sha a24ca1eb48392966aa9875d8cf82070c5c388350934034d8267b383f79594f83

## Provenance Summary

- Code: research/frontier/run_execute_36018230359.py, Research 2.0 frontier lane allowed roots research/harness + research/frontier
- Seeds: 42 numpy RandomState + hashlib.sha256 deterministic jitter/sharding
- Resampling: 5000 family-stratified trajectory-grouped bootstrap (percentile CI) + 5000 family-block permutation (block=family unit=trajectory) + 5000 global stratified for NC
- No BrowserGym/CDP, no LLM tokens, CPU-only synthetic, wall-clock <20 min
