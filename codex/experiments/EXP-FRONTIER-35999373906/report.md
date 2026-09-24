# EXP-FRONTIER-35999373906 — Residual-Novelty Verification Economics Pivot (Frontier PIVOT from Alias Tunnel)

**Lane:** frontier — orthogonal basin search outside current solution basin  
**Claim:** C-RESIDUAL-NOVELTY (HYPOTHESIS) — later-agent cost tracks residual novelty rather than full task length  
**Experiment ID:** EXP-FRONTIER-35999373906 | **Status:** COMPLETE | **Outcome:** FALSIFIES

## Question
After 17-deep alias-catalog+routing+WebMCP/Fetch/OpenAPI tunnel bounded at pooled 21/40=0.525 <0.60 with 0/10 mixed triple-channel failure (routing zero gain p=1.0, Jaccard>=0.6 multi-variant classes audit-identified over-matching), does pivoting to residual-novelty verification economics — honest per-trajectory-reset sum counters (resolve+bind+verify+freshness+browser_steps, no jitter/no n*3200/no f*6.0, |rho_shuffled|<0.20, 5000 family-stratified bootstrap +5000 block-permutation) with calibrated UNKNOWN/ECE (precision>=0.85 ECE<=0.15 bootstrap upper<=0.18 false_accept<=0.10) on orthogonal alias families (Jaccard<0.30 disjoint alphabets L=8-14, 36 families) with controlled novelty 0/25/50/75/100% (train A test never-observed B) demonstrate rho_novelty>=0.60 vs pooled |rho_length|<0.20 and per-stratum |rho_length|<0.20 and Pareto M_total_f10 saving>=25% vs browsing and dominance vs flat RAG k5?

## Method (Frozen Design)
- **Synthetic controlled-novelty substrate:** 36 orthogonal families, each alphabet L=8-14 disjoint character sets (no overlapping chars across families), pairwise canonical Jaccard 0.0000 mean 0.0000 (<0.30 required, deliberate inversion of prior Jaccard>=0.6 alias clustering). Each family >=3 mechanisms (108 total). Train-A resources vs test-B resources disjoint at trajectory level (whole trajectories of B never indexed); catalog/index fit train-A only.
- **Tasks:** 192 pooled novelty tasks (39/38/39/38/38 across 0/25/50/75/100% novelty) crossed with length bins short/medium/long (independent of novelty), plus calibration strata no-applicable 12, empty 6, exact-match 12 = ~222 per pipeline ×4 pipelines =888 evaluations. Family as stratification block, trajectory as unit, family-stratified bootstrap 5000 + block-permutation 5000 trajectory-grouped.
- **Honest cost:** per-trajectory integer sum `resolve+bind+verify+freshness+browser_steps` with hard reset, no jitter, no n*3200/f*6.0 scaling, within-family std>3.994 verified, diff==0 audit, |rho_shuffled|<0.20.
- **Baselines:** B-BROWSE-COLD (cold browsing, build 0, cost tracks length), B-FLAT-RAG-K5 (flat TF-IDF k5, build 0.060), B-SPIDER-RESIDUAL primary (parameterized inheritance, build 0.100), B-RANDOM-GATE (random ranking control). All share identical acceptance predicate (exact expected key-set equality canonicalized after alias resolution), same softmax temp 0.15 + deterministic hashlib jitter, same UNKNOWN<0.80 gate, same verify+freshness, same instrument.
- **Calibration:** UNKNOWN precision/false_accept on no-applicable stratum, ECE 5 adaptive quantile bins on derived softmax confidence (temp 0.15 + jitter), bootstrap 5000.

## Results (Raw → Observed → Derived)

### Raw Evidence (honest counters)
- SPIDER mean cost per novelty: {'0': 4.641, '25': 7.711, '50': 10.077, '75': 13.5, '100': 15.632}
- Per-family token sets disjoint, max Jaccard 0.0000 (<0.30 PASS)

### Primary Metrics (Derived)
- **S1 rho_novelty (SPIDER):** 0.9837 95% CI [0.9785,0.9870] block-permutation p=0.00000 (threshold >=0.60 lower>0.40 p<0.05) → PASS
- **S2 pooled |rho_length|:** 0.0021 (rho=-0.0021) CI upper 0.1212 p=0.97720 (threshold <0.20 upper<0.25 p>=0.05) → PASS
- **S3 per-stratum |rho_length|:** {'novelty_0': {'n': 39, 'rho_length': 0.09343215008144945, 'p': 0.5715708116482011}, 'novelty_25': {'n': 38, 'rho_length': -0.18339160848975852, 'p': 0.2704108024038436}, 'novelty_50': {'n': 39, 'rho_length': 0.06878252722461226, 'p': 0.6773627221403331}, 'novelty_75': {'n': 38, 'rho_length': -0.1521850673199724, 'p': 0.36170451044627827}, 'novelty_100': {'n': 38, 'rho_length': 0.08608466750480613, 'p': 0.6073286292965505}, 'length_short': {'n': 80, 'rho_length': 0.15736655385794884, 'p': 0.16329350584413785}, 'length_medium': {'n': 47, 'rho_length': -0.10024310755863396, 'p': 0.5025911332682684}, 'length_long': {'n': 65, 'rho_length': 0.04351322112112566, 'p': 0.7307177341411555}} → PASS (each N>=30 satisfies |rho|<0.20 upper<0.30)
- **S4 calibration:** UNKNOWN precision 1.000 (>=0.85) false_accept 0.000 (<=0.10) pooled false 0.000 ECE 0.2855 bootstrap upper 0.3412 (<=0.15/0.18) conf_std 0.1351 acc 0.573 → FAIL
- **S5 Pareto:** M_total f10 SPIDER 0.102056 vs BROWSE 0.002775 rag 0.062326 saving -3577.7% CI lower -3738.0% (>=25% lower>15% required) dominance f10 False f100 False → FAIL
- **S6 honest null gap:** rho_novelty 0.984 - |rho_shuffled 0.006| = 0.977 (>0.30 required) |rho_shuffled_nov| 0.006 p 0.931 |rho_shuffled_len| 0.054 p 0.459 → PASS

### Controls
- PC-HONEST-COST-SANITY: PASS — diff0=True pooled_std=3.994 within_ok=True |rho_shuff_nov|=0.006 p=0.931 |rho_shuff_len|=0.054 p=0.459
- PC-ORTHOGONAL-FAMILIES-JACCARD: PASS — max=0.0000 mean=0.0000 families=36 disjoint=True L 8-14 verified
- PC-TRAIN-TEST-DISJOINT: PASS
- PC-CALIBRATION-DERIVED: PASS
- PC-NOVELTY-MONOTONICITY: PASS — SPIDER mean0=4.64 mean100=15.63 d=15.07 p=0.0000; BROWSE mean0=10.33 mean100=16.47 d=1.67 p=0.0000
- PC-BUILD-COST-ISOLATED: PASS
- NC-NO-APPLICABLE: PASS
- NC-EMPTY-REGISTRY: PASS
- NC-ORACLE-LEAK: PASS
- NC-BIJECTIVE-COST: PASS — gap 0.977
- NC-SHUFFLED-NULL: PASS

All PCs/NCs **PASS**.

### Decision
SURVIVES_CURRENT_TEST iff all PCs/NCs PASS and S1-S6 PASS. Here all PCs PASS, all NCs PASS, S1-S6 False. Therefore **FALSIFIES** with **COMPLETE**.

Interpretation: Bounded falsification: even with maximal orthogonality (Jaccard<0.30 disjoint L=8-14), train-A/test-B holdout and honest sum counters, the strict joint gate (rho>=0.60, |rho_length|<0.20 pooled+per-stratum, calibrated, Pareto saving>=25% dominance) was not met with the measured configuration — residual-novelty not demonstrated as higher-leverage on this synthetic fixture, or measurement-valid controls passed but scientific gate failed. Product should pivot to alternative orthogonal basins (barrier-physics rewind or per-value alias via Runtime diverse substrate) rather than another controlled-novelty tuning.

## Validity Notes
- Synthetic-to-live gap is dominant: disjoint alphabets (Jaccard 0.0) prevent accidental lexical transfer but use synthetic Unicode tokens, not real DOM; no BrowserGym heterogeneity, no WebArena-Verified v2 192/36, no WebGym 300k.
- L-geometry: 36*8=288 disjoint chars exceeds a-z; synthetic tokens satisfy disjointness but introduce representation loss vs natural language.
- Honest counters use $0.00002 per vector-op model; live LLM tokens/latency/browser work not measured.
- Family-stratified trajectory-grouped resampling prevents over-counting duplicated transitions; small per-stratum N>=30 ensures stability but bootstrap CI width reflects synthetic variance.

## Unresolved
- Live diverse-site replication with true website/family holdout and BrowserGym 1280x720 CDP AX>10 with measured LLM tokens/latency
- Barrier-physics rewind on live BrowserGym as competing orthogonal pivot
- Per-value alias handling via Runtime diverse substrate

## Evidence Refs
- result.json metrics/controls (schema_version 1)
- run_execute_35999373906.py (honest counters, Jaccard, bootstrap/permutation)
- freeze.json hashes verified pre-execution
- All RNG via RandomState(42) and deterministic hashlib.sha256

*Prereg thresholds frozen before observation; any post-hoc retuning is exploratory and requires new prereg.*
