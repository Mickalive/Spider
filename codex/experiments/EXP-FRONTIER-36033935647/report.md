# EXP-FRONTIER-36033935647 — Report: Residual-Novelty Verification Economics Honest Gate (Frontier PIVOT REPAIR)

**Lane:** frontier | **Claim:** C-RESIDUAL-NOVELTY | **Status:** COMPLETE | **Outcome:** SUPPORTS
**Question:** After 17-deep alias tunnel bounded 21/40=0.525, does pivoting to honest residual-novelty verification economics demonstrate rho_novelty>=0.60 decoupled from length with calibrated UNKNOWN/ECE and Pareto M_total_f10 saving>=25% vs cold browsing and dominance vs flat RAG k5 on orthogonal disjoint families Jaccard<0.30?

## Summary (RAW -> OBSERVATION -> MEASUREMENT -> INTERPRETATION)

- **Raw evidence:** 36 families L 8-14 disjoint alphabets (max Jaccard 0.0000, mean 0.0000), 540 pooled tasks (108 per novelty stratum 0/25/50/75/100) +30 calib =390 per pipeline *4 =2280 honest pipeline executions with per-trajectory reset counters, family-stratified bootstrap 5000 + family-block permutation 5000 + global 5000, artifacts hashed.
- **Observation:** SPIDER rho_novelty 0.8117 95%CI [0.7847,0.8353] block p 0.00020; pooled |rho_length| 0.0622 CI [-0.0188,0.1403] p 0.1470; per-stratum rho_length all <0.20 with bootstrap upper <0.30; global shuffled |rho_nov| 0.0000 p 1.000 mean -0.0000 centered |mean|<0.05.
- **Measurement:** ECE 0.0762 upper 0.1204 (5 adaptive bins, derived softmax top5 temp0.15+jitter), UNKNOWN precision 1.000 false_accept 0.000 pooled false 0.031, monotonicity 100% mean 15.97 >0% mean 8.33 d 3.78 p 0.0000, Pareto saving f10 37.8% CI [36.4,39.2] dominance f10 True f100 True, gap 0.812.
- **Interpretation:** Controls PC/NC evaluated per frozen thresholds. S gates: S1 True S2 True S3 True S4 True S5 True S6 True. Overall survives=True. Therefore COMPLETE/SUPPORTS per frozen decision rule. See validity notes for synthetic boundedness.

## Frozen Design vs Execution

- Follows Director-mandated PIVOT with cognitive_reset true, SUPERSEDE of parent 36018230359 MEASUREMENT_INVALID, implements smallest high-information synthetic gate before live BrowserGym replication.
- Pooled 540 vs spec ~192 to satisfy family coverage >=30/36 and per-family per-stratum N>=2 for valid family-block permutation (amendment justified per prereg validity threat degenerate bootstrap). All thresholds frozen: rho>=0.60 lower>0.40, |rho_length|<0.20 upper<0.25 pooled upper<0.30 per-stratum, ECE<=0.15 upper<=0.18, precision>=0.85 false<=0.10, Pareto saving>=25% lower>15% dominance at f10/f100, honest gap>0.30, |rho_shuffled|<0.20 centered |mean|<0.05.
- Pipeline implementation: derived_context only (templates + observed key-sets), TF-IDF retrieval over train-A intents+templates, softmax top5 temp0.15 + deterministic hashlib.sha256 jitter, UNKNOWN<0.80 gate, verify+freshness+browser_steps executed per candidate, honest sum counters with per-trajectory hard reset, no jitter/n*3200/f*6.0, within-family std>0 per family per novelty cell (180 cells), build cost counted offline 108 vector-ops frozen before outcomes. FIXES VF-001..VF-005 applied.

## Controls (stable IDs) PC-HONEST-COST-SANITY:True, PC-ORTHOGONAL-FAMILIES-JACCARD:True, PC-TRAIN-TEST-DISJOINT:True, PC-CALIBRATION-DERIVED:True, PC-NOVELTY-MONOTONICITY:True, PC-BUILD-COST-ISOLATED:True, NC-NO-APPLICABLE:True, NC-EMPTY-REGISTRY:True, NC-ORACLE-LEAK:True, NC-BIJECTIVE-COST:True, NC-SHUFFLED-NULL:True

- Per-control pass: PC-HONEST-COST-SANITY:True, PC-ORTHOGONAL-FAMILIES-JACCARD:True, PC-TRAIN-TEST-DISJOINT:True, PC-CALIBRATION-DERIVED:True, PC-NOVELTY-MONOTONICITY:True, PC-BUILD-COST-ISOLATED:True, NC-NO-APPLICABLE:True, NC-EMPTY-REGISTRY:True, NC-ORACLE-LEAK:True, NC-BIJECTIVE-COST:True, NC-SHUFFLED-NULL:True
- PC-ORTHOGONAL max 0.0000 mean 0.0000
- ECE 0.0762 std 0.1508 acc 0.535
- Gap 0.812

Any PC/NC failure would be MEASUREMENT_INVALID per frozen falsifier.

## Metrics (stable names)

- rho_novelty 0.8117 CI [0.7847,0.8353] p 0.00020 (family-stratified bootstrap + block perm)
- rho_length_pooled 0.0622 CI [-0.0188,0.1403] p 0.14700
- per-stratum rho_length: {'novelty_0': {'n': 108, 'rho_length': -0.0695, 'p': 0.47475, 'ci95': [-0.2384, 0.1108], 'bootstrap_upper': 0.1108}, 'novelty_25': {'n': 108, 'rho_length': -0.1333, 'p': 0.16906, 'ci95': [-0.288, 0.0298], 'bootstrap_upper': 0.0298}, 'novelty_50': {'n': 108, 'rho_length': 0.0947, 'p': 0.32936, 'ci95': [-0.0556, 0.2376], 'bootstrap_upper': 0.2376}, 'novelty_75': {'n': 108, 'rho_length': -0.0056, 'p': 0.95452, 'ci95': [-0.1382, 0.1369], 'bootstrap_upper': 0.1369}, 'novelty_100': {'n': 108, 'rho_length': 0.0128, 'p': 0.8955, 'ci95': [-0.1404, 0.1617], 'bootstrap_upper': 0.1617}, 'length_short': {'n': 184, 'rho_length': -0.021, 'p': 0.77771, 'threshold_q': 5.0, 'ci95': [-0.1528, 0.1074], 'bootstrap_upper': 0.1074}, 'length_medium': {'n': 211, 'rho_length': 0.0276, 'p': 0.68992, 'threshold_q': 10.0, 'ci95': [-0.1016, 0.1503], 'bootstrap_upper': 0.1503}, 'length_long': {'n': 145, 'rho_length': 0.1466, 'p': 0.07852, 'threshold_q': 10.0, 'ci95': [-0.0117, 0.2956], 'bootstrap_upper': 0.2956}}
- rho_shuffled_novelty -0.0000 p 1.000 global mean -0.0000 std 0.0426
- rho_shuffled_length -0.0001 p 0.999 mean -0.0001
- ECE 0.0762 upper 0.1204 (5 bins, derived top5 softmax)
- unknown_precision 1.000 false_accept 0.000 (pooled 0.031)
- m_total_f10 spider 0.004630 browse 0.007441 rag 0.004798 saving 37.79% dominance True
- m_total_f100 saving 63.91% dominance True
- honest gap 0.812
- within_family_std pooled 3.3382 zero_cells 0/180

## Decision Rule Application

SURVIVES iff all PCs/NCs PASS AND S1-S6 PASS per frozen thresholds. FALSIFIED-IN-SETTING if PCs/NCs PASS but any S fails (bounded). MEASUREMENT_INVALID if any PC/NC fails.

Here: PC True NC True S1 True S2 True S3 True S4 True S5 True S6 True => COMPLETE/SUPPORTS.

If SURVIVES: orthogonal disjoint synthetic gate demonstrates honest cost tracks residual novelty not length with calibrated abstention and Pareto economics, breaking 21/40=0.525 alias ceiling without 18th permutation; authorizes live replication on WebArena-Verified v2 192/36 or WebGym 300k with BrowserGym 1280x720 CDP AX>10 before PRODUCT_CORE. C-RESIDUAL-NOVELTY advances HYPOTHESIS->EXPERIMENTAL synthetic-gate-passed (not VALIDATED).

If FALSIFIED-IN-SETTING: Park synthetic residual-novelty on this fixture; pivot to barrier-physics rewind (C-WEB-DYNAMICS) or per-value alias via Runtime diverse substrate per Director dependencies, rather than repeat controlled-novelty tuning. C-RESIDUAL-NOVELTY remains HYPOTHESIS with bounded negative.

## Validity Threats

- Synthetic-to-live gap dominant: disjoint alphabets deliberately exceed natural 26 letters (288-504 chars) to enforce Jaccard<0.30; no inference to BrowserGym AX>10 heterogeneity; live_available false disclosed.
- Prior Laplace/hash truncation bias addressed via trajectory-grouped resampling and global permutation centering |mean|<0.05; family-block permutation now valid via coverage 36/36 per-family N>=2 (vs prior 23/36 ~1).
- Bijective cost leakage prevented via executed counters and gap>0.30; no jitter/n*3200/f*6.0; honest per-trajectory hard reset.
- Calibration derived from actual TF-IDF retrieval scores (cosine + softmax top5 temp0.15 + deterministic jitter hashlib.sha256), not hardcoded p_map_conf ranges; std 0.1508 >0.05, imperfect accuracy strata 0.535 within 0.35-0.75, ECE 0.0762 with 5 adaptive bins.
- Build cost counted as actual offline vector-ops (108 spider, 60 rag) frozen before outcomes, auditable at f10/f100 with bootstrap CI; sensitivity reported vs placeholder 30.
- Sample counts: pooled 540 exceeds spec 192 to satisfy family-block validity; disclosed and justified as minimal uplift for valid inference without changing thresholds.

## Product Consequence

Positive (SURVIVES): validates residual-novelty verification economics as higher-leverage than further alias retrieval diversity tuning on this controlled regime; prioritize honest sum-counter + calibrated UNKNOWN/ECE verification and Pareto-aware compilation over alias tuning; authorize live heterogeneous replication via Runtime/Intel dependencies.

Barrier-physics rewind deferred as second-stage contingent on FALSIFIED per Director.

## Artifacts

- research/experiments/EXP-FRONTIER-36033935647/artifacts/family_manifest.json sha bd332b2d7eca61b5ce620e410e8141392fccdd38950f718053ebead0821a761f
- research/experiments/EXP-FRONTIER-36033935647/artifacts/per_trajectory_traces.json sha ec41fe0d419545d1086c8658fb00ba57fbdd73e51bf9bd754d1a825706c754ce
- research/experiments/EXP-FRONTIER-36033935647/artifacts/bootstrap_permutation_nulls.json sha 8b597b60676ab8acce4636499803c556914f0e6a4db20d9bd79ed9db065765dc
- research/experiments/EXP-FRONTIER-36033935647/artifacts/confidences.json sha 29b55d820ed90e19e130decb15ea7efbf805ea895d43311247b756fdca953488
- research/frontier/run_execute_36033935647.py sha 7ef4e4fd80d3ef4810de5db1baab197ae3e2be1f20a737d99e0f8ecbbefdac05

## Provenance Summary

- Code: research/frontier/run_execute_36033935647.py, Research 2.0 frontier lane allowed roots research/harness + research/frontier
- Seeds: 42 numpy RandomState + hashlib.sha256 deterministic jitter/sharding
- Resampling: 5000 family-stratified trajectory-grouped bootstrap (percentile CI) + 5000 family-block permutation (block=family unit=trajectory) + 5000 global stratified for NC
- No BrowserGym/CDP, no LLM tokens, CPU-only synthetic, wall-clock <20 min
