# EXP-PHYSICS-35787698409 Preregistration — Physics Correlated-State FSM Recalibrated (REOPEN)

**Status: DESIGN — FROZEN BEFORE OUTCOME (2026-09-22). No outcome-bearing measurements for the recalibrated K=24 decision have been inspected.**

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35787698409
- **Lane**: physics
- **Claim**: C-WEB-DYNAMICS — Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity (status HYPOTHESIS per codex/claim_state.json, 64+ prior C-WEB-DYNAMICS experiments, physics IDLE tunnel_flag true after 14 recent MEASUREMENT_INVALID/FALSIFIED bounded to synthetic 2D or minimal SPAs)
- **Directive**: Global Research Director REOPEN on C-WEB-DYNAMICS (request.json director_mandate cycle 35787189488, allocation REOPEN cognitive_reset true, parent_handoff_disposition USE, claim_id C-WEB-DYNAMICS). Binding strategic question verbatim in request.json director_mandate.question. Parent handoff is continuity evidence only and MUST NOT silently override the REOPEN recalibration decision.
- **Parent handoff**: research/experiments/EXP-PHYSICS-35782523165/handoff.json (sha256 247a634df0c252fe90e8d153f71084540ced3d54df527553e8a02061c4146d7f) — MEASUREMENT_INVALID borderline null centering, not falsification. Its established/rejected/unknown/do_not_assume distinctions preserved below (§2). Director rationale: Bayesian K=12 first estimator to pass C1+C3 on stochastic SPA (SURVIVES) but absolute BF negative on real TodoMVC; correlated non-determinism where DOM_before correlates with latent state is the only falsifiable beyond-memory program not requiring new Gate0 SPAs, and independent per-step noise already falsified (0.004 bits). Converts borderline 0.688-bit signal into confirmatory test via K=24 or N~4000.
- **Dependencies (binding per mandate)**: runtime:local correlated FSM harness already provisioned, no new Gate0 SPA required; intel:Gate0 SPA enumeration bounds claim ceiling to synthetic correlated state. `research/intel/` manifest absence does not gate this locally-hosted synthesis.
- **Pre-2.0 / codex baseline**: WP-002B rule minus shuffle +0.0532 no holdout, WP-003 MEASUREMENT_INVALID (leakage, Gaussian jitter, hash(site) seed), frontier 61 pooled TV/KDE/binned blind spots (kNN fails scaling rho -0.12, KDE fails rotation rho 0.286, CV>0.5), EXP-PHYSICS-34764605162 falsified independent-noise DOM_before (BC 0.004 random_API, 0.025 timing_dependent, R2 0.003, p=1.0) with audit V1_independent_noise_bakes_in_null flagging correlated regime as open.

## 2. Inherited Scientific State (from parent handoff — continuity evidence, not agenda)

Per AGENTS.md, EXPERIMENT_PACKET.md and POLICY.md, parent handoff `next_question` is advisory; director_mandate REOPEN is binding. Comparative reasoning: vs another synthetic TV/KDE variant marginal information near zero (9/10 frontier scaling failures, CV>0.5), vs production SPA CMI blocked by Gate0 0/3 (titles/entropy/leakage), vs BrowserGym harness belongs to runtime — correlated FSM provides discriminating positive vs independent-noise null on same substrate.

### Established (justified at stated ceiling, recomputed)

- Correlated-state primary descriptive signal: Bayesian DM K=12 N=1999 observed CMI 0.8179 perm_mean 0.1297 perm_std 0.0094 BC 0.6881 p_raw 0.001 p_bonf 0.00799 gap 0.688 over B-DOM-SIMILARITY 0.0 and B-MARKOV-1 0.0 on both R1 visible_text_hash and R2 a11y_tree_hash (isomorphic SHA256(L||state||variant%3)), H(S_next|C) 3.302 >0.3 strata 24 ge3 24 singleton 0.0 |R|/N 0.018 (36 hashes 6*2L*3 variants) MI(DOM;Action) 0.0 <0.10 not tautological, dom_bytes 24 a11y_bytes 24, leakage 0.0, trajectory_id resampling unit 1000 grouped perms seed 42 (result.json metrics primary_BC_R1/R2 0.688 audit recomputed identical)
- Independent-noise replication replicates prior falsification: same pipeline BC -0.0051 p 0.865 perm_mean 0.00085 perm_std 0.0046 |BC|<0.05 p>0.10, 18 hashes |R|/N 0.009 H 2.585 strata 24, confirming pipeline distinguishes correlation from independent per-step noise (G2 not triggered)
- IID synthetic null correctly centered: BC 0.0013 p 0.401 perm_std 0.0070 |BC|<=0.03 p>0.10, confirming correlated 0.688 not estimator bias alone (controls null_control_iid pass true)
- Baselines executed as frozen with valid gaps: B-DOM-SIMILARITY TF-IDF cosine k=5 fit TRAIN only 70/30 by trajectory_id BC_sim 0.0 acc 0.108 gap 0.688, B-MARKOV-1 MLE BC 0.0 gap 0.688, B-MARKOV-K3 BC 0.0, B-SHUFFLE-GROUPED null as above, B-SITE-LEAKAGE gap 0.0 MI 0.0 no href tautology
- Data quality and provenance: locally-hosted Express synthetic FSM substrate_available by construction (no Gate0, avoids Q=0 0.0 dom_bytes trap), 50 trajectories x40 steps =2000 transitions 1999 analyzed L per trajectory A 959/B 1040, freeze hashes MATCH (prereg 9ca9a0 request 5e646d spec 723440 freeze 640ab7b), PYTHONHASHSEED=0 numpy 42 deterministic, raw_transitions sha256 2ffc9e95..., 4ee10d70..., ab685d9d..., raw_results 2ec15c2c..., execute.py 9cb24333...
- Measurement status: G1 positive correlated control fails strict valid centering (|null_mean| 0.1297>0.1 by 0.03 null_std 0.0094<0.01 by 0.0006) borderline, G4 primary null degenerate on both R1/R2 same values, so per frozen rule MEASUREMENT_INVALID pipeline_blind_correlated / null_degenerate, not scientific falsification; audit status MEASUREMENT_INVALID producer_claim_supported false verifies borderline calibration not blindness (audit validity_findings, gate_G1 false gate_G2 false gate_G3 true gate_G4 true primary_sig false); pipeline NOT blind with bias floor ~0.13 bits. Producer notes K=24 would give mean 0.074 std 0.0104 passing both
- C-WEB-DYNAMICS claim ceiling remains HYPOTHESIS after parent: no confirmatory SURVIVES or bounded FALSIFIED on correlated hash-DOM factorization, no physics mechanical prior validated

### Rejected (bounded)

- No bounded rejection of correlated DOM_before beyond-memory dynamics via visible_text_hash or a11y_tree_hash on locally-hosted session-correlated FSMs — primary sig(R) not evaluated due G1/G4 MEASUREMENT_INVALID; C-WEB-DYNAMICS not closed on this regime, not falsified even though magnitude would satisfy sig if gates passed (audit claim_ceiling bounded to bias floor calibration, not to hash truncation insufficiency)
- No rejection of richer representations outside hash truncation (visual layout, computed CSS, interaction sequences) or true production SPA correlated latent regimes — bounded to SHA256 hash truncated 5k visibleText/a11y_tree 16 hex, 6-state FSM class, K=12 N=1999 pipeline

### Unknown (open)

- Whether Bayesian DM recalibrated to K=24 (alpha=1/K) at N=1999 (producer notes mean 0.074 std 0.0104 would pass) or to N≈4000 at K=12 brings |null_mean|<0.1 and null_std>0.01 without changing construction, converting present BC 0.688 into valid SURVIVES or revealing true FALSIFIED if gap collapses — smallest unblock per audit required_fixes (THIS EXPERIMENT)
- Whether independent-noise control with >=6 variants per state (instead of 3) raises null_std from 0.0046 to >0.01 without confounding, making independent null a valid pipeline discrimination control
- Whether per-15-step regime with P(flip)=0.07 (frozen but only per-trajectory tested) vs per-trajectory L persistence yields different null centering under trajectory-grouped permutation (grouped unit trajectory_id assumes L constant within trajectory)
- What BC, null_mean/std, p, gap over sim/markov, Cohen d, CI would be observed on true production BrowserGym WebShop DOM-bearing trajectories with correlated latent regimes (session/permission/user data) outside hash truncation and with richer visual/computed-style DOM, at N=1999 or larger — bounded to locally-hosted 6-state FSM here
- What delta-repair cost, regime detector transfer across site types, and cross-site holdout performance would be if correlated dynamics were considered validated (SURVIVES) under relaxed thresholds (mean 0.13 std 0.009)
- Whether B-SHUFFLE-GROUPED with trajectory_id preserves correct null when latent regime persists per trajectory vs per regime, and whether analytic bias correction for Dirichlet-Multinomial could replace permutation threshold

### Do Not Assume

- Do not assume C-WEB-DYNAMICS falsified, supported, or bounded-rejected — parent is measurement_invalid borderline (0.1297>0.1, 0.0094<0.01), not scientific negative; all magnitude thresholds pass (BC 0.688>>0.30 p 0.001<0.01 gap 0.688>>0.05) so do not encode as FALSIFIED-IN-SETTING on hash-DOM correlated regime
- Do not assume pipeline blind or correlated construction failed — audit confirms pipeline NOT blind, signal far exceeds positive control threshold (BC 0.688 vs 0.30) and independent correctly shows 0, so construction bias 0.70/0.30 and DOM family SHA256(L||state||variant%3) is correct
- Do not assume present 0.688-bit BC is valid beyond-memory dynamics — bias floor 0.129 accounts for ~19% of observed CMI, null degenerate invalidates confirmatory claim; do not subtract floor post hoc to claim SURVIVES without new preregistration at K=24 or larger N
- Do not assume independent null_std 0.0046 degeneracy implies confound — G2 not triggered (BC -0.005 not >=0.05 with p<0.10); degeneracy is representation loss (low DOM diversity 3/state) not confounding
- Do not assume R1 and R2 are independent — they are isomorphic by construction (both encode L via same SHA256 family), so identical BC/gap expected; R3 multi_feature same, R4 numeric structural correctly degenerate BC -0.0038 p 0.733
- Do not assume hash-DOM regime detectors are product-ready — no SURVIVES, no transfer across site types, no delta-repair cost; do not distill into kernel until recalibrated validation
- Do not assume locally-hosted 6-state Express synthetics substitute for production correlated latent regimes with larger state spaces, visual layout, or computed-style DOM outside 5k hash truncation — claim bounded to tested FSM class and hash representations, global Web production remains untested
- Do not assume trajectory-grouped permutation thresholds (|null_mean|<0.1 null_std>0.01) are arbitrary — they correct Laplace floor 0.3056 degeneracy on near-unique hashes; do not relax post hoc without new frozen decision_rule
- Do not assume audit PASS means SURVIVES — audit status is MEASUREMENT_INVALID, producer_claim_supported false, claim_ceiling HYPOTHESIS

This design preserves all distinctions and directly implements the audit required_fixes: recalibrate K=24 (or N~4000) and increase independent variants to >=6.

## 3. Scientific Question (binding, refined to falsifiable experiment)

Director strategic question (request.json director_mandate.question verbatim):

> On locally-hosted 6-state correlated FSM construction (L per trajectory 50x40 steps, basin bias 0.70/0.30, DOM_before SHA256(L||state||variant%3) 36 hashes |R|/N 0.018, independent-noise control falsified at BC 0.004 bits), with Bayesian Dirichlet-Multinomial recalibrated to K=24 (alpha=1/K) or N~4000 and trajectory-grouped permutation 1000 perms seed 42, does trajectory-grouped CMI achieve valid null centering (|null_mean|<0.1 null_std>0.01) with BC>0.05 p_bonf<0.01 and gap >=0.05 over B-DOM-SIMILARITY and B-MARKOV-1 on R1 visible_text_hash or R2 a11y_tree_hash while independent-noise replication remains BC~0 (|BC|<0.05 p>0.10 null_std>0.01), without requiring new Gate0 production SPAs?

Refined falsifiable experiment: On the same locally-hosted 6-state Express correlated FSM (L per trajectory 50x40, bias 0.70/0.30, DOM_before family SHA256(L||state||variant%3), 36 hashes, |R|/N 0.018) but with Bayesian DM recalibrated to K=24 alpha=1/K N=1999 seed 42 (or exploratory N~4000), does trajectory-grouped permutation CMI (1000 perms seed 42, resampling unit trajectory_id) achieve valid null centering (|null_mean|<0.1 null_std>0.01) with BC>0.05 p_bonf<0.01 gap>=0.05 over B-DOM-SIMILARITY (TF-IDF k5 0.0) and B-MARKOV-1 (0.0) on R1 or R2, while independent-noise replication recalibrated to >=6 variants per state and same K=24 remains BC~0 (|BC|<0.05 p>0.10 null_std>0.01 |null_mean|<0.1) and IID null BC<=0.03 p>0.10? Either valid SURVIVES (first beyond-memory correlated DOM dynamics without Gate0) or valid FALSIFIED (hash DOM insufficient even with constructed correlation) changes claim/product decision without new Gate0 production SPAs.

## 4. Motivation & Why This Is the Smallest High-Information Test

### 4.1 Tunnel diagnosis (why not another synthetic estimator variant)

- Parent's borderline is purely calibration: BC 0.688 >>0.30, p 0.001 <<0.01, gap 0.688 >>0.05, H 3.302, independent -0.005, IID 0.0013, baselines 0.0 — all magnitude thresholds pass decisively; only G1/G4 valid centering fails by 0.03 bits mean and 0.0006 std at K=12 n~333 per stratum (bias floor 0.129 vs threshold 0.1). Audit required_fix explicitly notes K=24 gives mean 0.074 std 0.0104 passing both without changing construction, and independent needs >=6 variants to raise std 0.0046>0.01. This is the smallest change that can flip MEASUREMENT_INVALID to SURVIVES/FALSIFIED.
- Director portfolio: 64 C-WEB-DYNAMICS experiments bounded to synthetic 2D [0,1]^2 or 3-state minimal SPAs, scaling rho~0 and CV>0.5 persist; 9/10 frontier TV/KDE/kNN density-divergence variants show persistent scaling failure, rotation blind spots, CV>0.5 at 250/type; marginal information from another alpha/K/bandwidth tweak near zero. Gate0 exhaustive enumeration 0/3 real SPAs (EXP-INTEL-35773136560) after BrowserGym/CAP/Mind2Web-2/WebJudge closes production-SPA PMI path; TodoMVC hash-SPAs have 0.0 dom_bytes field absence and constant title degeneracy. Correlated FSM is only falsifiable beyond-memory program not requiring new Gate0 SPAs (director) and directly tests audit-flagged open setting V1_independent_noise_bakes_in_null (independent per-step noise bakes in null, correlated regime where DOM correlates with latent state is open).
- Independent-noise already falsified twice (0.004 bits random_API, 0.025 timing_dependent, now -0.005 recalibrated) with 0.70/0.30 basin construction; correlated regime tests distinct graphical model (L->DOM and L->S_next vs L absent) — not repeating same hypothesis. Re-tuning pooled TV/KDE or Laplace alpha on 12-state synthetic SPA gives diminishing returns (director agent_priors: commodity replay floor TERX 0.09s/0-token, measurement degeneracy at ceiling when SA singleton PMI 0 tautologically forced, pooling vs per-type false-positive).

### 4.2 Why recalibrated K=24 is orthogonal and substrate_available

- Independent noise: DOM variant independent of S_next given C => I=0 by construction. Correlated regime: L jointly determines DOM and S_next bias => I>0 even after conditioning on URL and H_K=3. Mathematically distinct; independent falsification does not imply correlated null.
- Substrate_available: locally-hosted Express SPA with synthetic L per trajectory is constructible stdlib-only, no browser, no intel manifest, no dom_bytes gate. K=24 alpha=1/K recalibration keeps same generation (50x40 L per trajectory, 36 hashes) and same 1000 grouped perms seed 42, only changing Dirichlet concentration. Provides theoretical capacity >=0.40 bits (binary L * bias) so BC>=0.30 reachable. Increasing independent variants 3->6 raises |R|/N from 0.018 to ~0.036 and per-stratum diversity, expected to raise null_std above 0.01 without confounding.
- Strong nulls exceed requirement: B-DOM-SIMILARITY (TF-IDF k5) mandatory per mandate tests ordinary similarity; B-MARKOV-1 tests Markov order-1; independent-noise recalibrated is within-lane exact falsified control with valid variance; trajectory-grouped permutation with |null_mean|<0.1 null_std>0.01 fixes prior Laplace floor 0.3056 degeneracy on near-unique hash DOMs.

### 4.3 Why smallest high-information

- Positive or negative outcome with valid gates changes C-WEB-DYNAMICS ceiling and product decision: SURVIVES => first beyond-memory dynamics via correlated hash DOM without Gate0, justifies DOM hash regime detectors as mechanical priors; FALSIFIED => closes correlated hash-DOM on locally-hosted regime FSMs after independent already closed, forcing physics to PARK or await richer visual/computed-style representations outside hash truncation — either materially changes product architecture. MEASUREMENT_INVALID (positive control <0.30 or independent confounded or null degenerate) is also informative and refuses false negative. Marginal gain vastly exceeds another synthetic TV/KDE tuning or Gate0 CMI retry.

## 5. Hypotheses (frozen, exhaustive)

### H_correlated (primary, beyond-memory correlated dynamics, recalibrated)

On correlated-state SPA dataset (50 trajectories x40 steps, L per trajectory, 2000 transitions, H(S_next|C)>0.3, 36 hashes |R|/N 0.018), Bayesian DM K=24 alpha=1/K N=1999 bias-corrected CMI BC = I(S_next; DOM_before | URL, H_K=3, Action_leakageFree) >0.05 with trajectory-grouped permutation Bonferroni p<0.01 (over R1/R2 x baselines max 8 tests, floor 0.001 at 1000 perms), |null_mean|<0.1 null_std>0.01, exceeding B-DOM-SIMILARITY BC_sim and B-MARKOV-1 BC_markov1 by >=0.05 bits on R1 visible_text_hash or R2 a11y_tree_hash. Cohen d = BC/null_std, 95% CI via permutation percentiles. H_correlated predicts recalibrated K=24 corrects bias floor 0.129->0.074 and std 0.0094->0.0104, preserving BC magnitude ~0.6-0.7 and gap ~0.6.

### H_positive_control_correlated

Same pipeline on correlated synthetic (identical to H_correlated but designated positive control) must achieve BC>=0.30 p<0.01 null_std>0.01 |null_mean|<0.1 on R1 or R2. Pipeline blind/miscalibrated if fails. Theoretical capacity >=0.40 bits ensures 0.30 reachable; frozen construction uses L in {A,B} with basin bias 0.70/0.30 and DOM hash family SHA256(L||state||step%3). Any outcome where BC<0.30 triggers MEASUREMENT_INVALID, not falsification. Parent K=12 already gave BC 0.688 p 0.001 but borderline centering; K=24 should pass centering.

### H_null_independent (negative control, recalibrated)

Identical Bayesian DM K=24 N=1999 trajectory-grouped permutation on independent-noise replication with >=6 variants per state (independent per-step draw, same FSM but L absent, DOM variant independent of S_next, 50x40 2000 transitions) must show BC~0 (|BC|<0.05) with p>0.10 and null_std>0.01 |null_mean|<0.1, replicating prior falsification but now with valid variance. If BC>=0.05 p<0.01 with valid null, pipeline confounds independence => MEASUREMENT_INVALID. Also validates prior 0.004-bit finding not due to K=12 miscalibration.

### H_null_iid

I.i.d. synthetic null (same marginal P(S) as correlated but S_next drawn i.i.d. per step, seed 42) must show BC<=0.03 p>0.10 |null_mean|<0.1 null_std>0.01; degenerate triggers MEASUREMENT_INVALID.

### H_null_shuffled (permutation null on primary)

Within-strata grouped shuffle DOM_before labels on correlated dataset: null distribution with |null_mean|<0.1 and null_std>0.01; degenerate triggers MEASUREMENT_INVALID for that representation.

## 6. Data Generation & Reuse

### 6.1 Primary correlated-state SPA (locally-hosted, no external dependency, SAME as parent)

- **Construction** (frozen, seeds PYTHONHASHSEED=0 numpy 42, same generate_correlated.py as parent except K change in analysis only): 6-state FSM states 0-5, 4 Action primitives uniform (click/fill/navigate/submit), target_sig = role+name+testId (never href). Latent L in {A,B} sampled per trajectory (primary per-trajectory; per 15-step regime with P(flip)=0.07 documented as exploratory variant, not primary). Transition: P(S_next | S_current, Action, L=A) favors basin {0,1,2} with 0.70 vs 0.30 for {3,4,5}, L=B mirrored (0.30/0.70), plus p_stay 0.70 within basin. Gives H(S_next|C) ~3.3 bits, determinism ~0.60-0.75. URL_before = `https://spa.local/#/state_{S_current}` (hash fragment preserved). DOM_before = SHA256(str(L)+'|'+str(S_current)+'|'+str(step%3)) -> 36 hashes (6*2L*3 variants), visibleText = f"user:{L} state:{S_current} variant:{step%3}", a11y tree = serialized AX role `banner` name `user:{L}`. Thus R1/R2 hashes correlate with L but not identical to S_next, requiring inference. Generate 50 trajectories x40 steps =2000 transitions, analyze N=1999. Report unique_L distribution, Dom_family count, S transition matrix per L, |R|/N, dom_bytes 24.
- **Recalibration**: analysis only changes K=12->24 alpha=1/K (1/12≈0.083 -> 1/24≈0.0417), no generation change. Optional exploratory N~4000 via 100 trajectories x40 or 50x80 documented but not primary.
- **Sample size**: 2000 transitions N=1999 gives 24 strata avg 83 per stratum largest ~333, power for BC 0.10 at SE ~0.01 with 1000 perms, BF calibration N/K=83 at K=24.

### 6.2 Independent-noise replication RECALIBRATED (null control)

- Same 6-state FSM but without L: DOM variant = independent RNG draw among >=6 hashes per state (variant_mod = rng.choice(6) seeded per step, independent of S_next, vs prior 3). Transition without L bias (uniform basins, p_stay 0.50). Generate 50x40 =2000 transitions. Expect BC~0 per prior -0.005 bits but now null_std>0.01 due to higher diversity (heuristically expected std ~0.007-0.012 vs prior 0.0046). This directly implements audit required_fix.

### 6.3 I.i.d. synthetic null

- Same marginal P(S) as correlated (estimated from correlated run) but S_next drawn i.i.d. independent per step (seed 42), DOM_before still correlated with phantom L but S_next independent => BC should be 0, BF favors order1. Same K=24.

### 6.4 No reuse of TodoMVC/WebShop trajectories for primary

- Prior TodoMVC raws have 0.0 dom_bytes and title=1 degeneracy; they are not used as primary to avoid Q=0 halt. Their gate_table still available as diagnostic but not gating. BrowserGym manifests optional for generalization, not gating.

### 6.5 Sample size & power calibration (recalibrated)

- Channel capacity at binary L with bias 0.70/0.30: theoretical I(S_next;L|C) ~0.40 bits pooling across S_current; at 60% DOM->L recovery (hash family leaks 2/3 variants) expected BC ~0.30-0.35 at K=12, slightly lower at K=24 due to stronger smoothing but still >0.30 per producer notes (mean floor drops 0.129->0.074, so observed 0.8179 -0.074 ≈0.74 vs prior 0.688). At K=24 N=1999, n_per_stratum_avg 83, alpha=0.0417, null_std expected 0.0104 (per producer) >0.01, |null_mean| 0.074 <0.1, so gates pass. Power via permutation CI width ~2*null_std ~0.02, BC 0.6 gives Cohen d ~58. Independent with 6 variants per state expected null_std ~0.010-0.012 >0.01 while BC ~0.

## 7. State, Action, History, DOM Operational Definitions

### 7.1 State S_next

Primary S_next = SHA256(normalize(URL_after)||'|'||normalize(title_after)) where normalize(URL)=lowercase, strip query ?session=/?token=, preserve SPA hash fragment #/, strip trailing slash; normalize(title)=trim lowercased truncated 200 chars (constant title allowed). Exploratory: S_URLonly SHA256(norm(URL_after)) only. S_next distinct timestep from DOM_before (t -> t+1, no post-state leak). Report unique_titles, title_entropy, URL fragment distribution, H(S_next|C).

### 7.2 Action A_leakageFree

A=(primitive, target_sig) primitive in {click, fill, navigate, select}, target_sig=role+name+testId+aria-label (never href/URL/src). Link target_href never enters A. Diagnostic A_leaky = A+href for leakage gap only; B-SITE-LEAKAGE-DIAGNOSTIC reports BC_leaky - BC_leakageFree. Action distribution per dataset reported.

### 7.3 History H_K=3

H_K=(A_{t-2},A_{t-1},A_t, S_{t-2},S_{t-1},S_t) last 3 steps; strata key C=(URL_before_normalized, H_K_actions) where URL_before_normalized is URL_only without title to avoid state leakage. Require strata_count>=5 unique C with >=3 per stratum; singleton_SA_rate<70%; report H(S_next|C) ceiling (must be >0.3 else CMI forced 0 => MEASUREMENT_INVALID) and strata_ge3 count.

### 7.4 DOM_before representations (tested independently)

- R1 visible_text_hash: SHA256(visibleText[0:5000] innerText, e.g., "user:A state:2 variant:1")
- R2 a11y_tree_hash: SHA256(serialized AX tree role/name/value up to 5k chars via simulated Accessibility.getFullAXTree)
- R3 multi_feature_hash: SHA256(R1 || R2) exploratory
- R4 numeric_structural: element_count/tree_depth/interactive_density/form_count exploratory (expected degenerate ~0.0)

Raw observables preserved (dom_bytes truncated 5k, a11y_bytes 5k) with documented truncation; hash collision negligible. Primary requires R1 or R2 only, but both expected isomorphic.

## 8. Measures

### 8.1 Primary: Bayesian DM bias-corrected CMI (RECALIBRATED K=24)

For each (dataset, R in {R1,R2}):
```
H(S_next|C) Dirichlet-Multinomial K=24 alpha=1/K: log P(counts|alpha) via Gamma
H(S_next|C,DOM) similarly stratified by (C,DOM_hash)
CMI_obs = H(S_next|C) - H(S_next|C,DOM)
BC = CMI_obs - mean(CMI_perm_grouped)  bias-corrected
Null distribution: 1000 trajectory-grouped permutations of DOM_before labels within each C stratum, grouped by trajectory_id seed 42, preserving per-trajectory DOM frequencies
Report: BC, null_mean, null_std, p_raw = (1+#{perm>=CMI_obs})/1001 one-sided, p_bonf = min(1,p_raw * n_tests) n_tests up to 8, Cohen d = BC/null_std, 95% CI via permutation percentiles (2.5th/97.5th), cardinality |R|/N, strata stats, H ceiling, MI(DOM;Action)
Primary is BC_R1 / BC_R2; also report CMI_obs uncorrected
BF_10 for order3 vs order1 Markov via same DM K=24 N=1999 on TRAIN counts, log BF nats; calibration on i.i.d. null must favor order1 (nats<0)
```

### 8.2 Baselines (same estimator K=24, same grouping)

- B-DOM-SIMILARITY BC_sim: TF-IDF cosine k=5 over DOM visible_text/a11y text fit on TRAIN only, predict S_next via similarity, compute BC_sim via same Bayesian DM on (C, NN_pred); report gap delta_sim = BC - BC_sim must be >=0.05
- B-MARKOV-1 BC_markov1: MLE P(S_next|URL_before,A) fit TRAIN grouped, compute BC_markov1; gap delta_markov1 >=0.05 required
- B-MARKOV-K3 BC_hist, accuracy reported
- B-SHUFFLE-GROUPED null distribution already described
- B-TRAJECTORY-MEMORY memorization ratio
- B-SITE-LEAKAGE gap

### 8.3 Auxiliary per dataset per R

NL, strata_count, strata_ge3, singleton_rate, leakage_validOnly, link_share, H(S_next|C), unique_DOM_hashes, |R|/N (expected 0.018 correlated with 36 hashes, ~0.027-0.036 with 6 variants independent), null_mean/std, Cohen d, CI, MI(DOM;Action) tautology check, action distribution, BF nats, card stats, dom_bytes/a11y_bytes.

## 9. Null Models & Baselines (strong, all executed as frozen)

Enumerated in spec baselines / §8.2. All executed with identical grouping (trajectory_id), seeds 42, preprocessing fit on TRAIN only, Dirichlet prior alpha=1/K=24, N=1999. Mandatory B-DOM-SIMILARITY and B-MARKOV-1 must be executed; gap gating for SURVIVES. No silent omission: if baseline cannot be computed, publish validity_note and trigger MEASUREMENT_INVALID for that representation. Independent-noise now with >=6 variants to achieve valid variance.

## 10. Statistical Tests & Uncertainty (frozen, corrected per audits)

- **Permutation**: 1000 trajectory-grouped shuffles of DOM_before labels within each C stratum, grouped by trajectory_id seed 42 deterministic. Null = BC_perm distribution. Resampling unit = trajectory_id; no Gaussian jitter.
- **p-value**: p_raw one-sided per above, Bonferroni primary p_bonf = min(1,p_raw * n_tests) where n_tests = n_R * (1 primary +2 baselines) up to 8, alpha 0.01. Also report raw. Floor 0.001 at 1000 perms reachable for p<0.01; report both raw and Bonferroni; BC also gates via absolute 0.05.
- **BF**: log BF via Gamma functions, no resampling; BF>10 (nats>2.3) reported auxiliary but primary gates on BC not BF; calibrated on i.i.d. null must be <0.
- **Effect size**: Cohen d = BC / null_std (null_std>0.01 required); 95% CI via grouped permutation percentiles, NOT Gaussian.
- **Seed determinism**: PYTHONHASHSEED=0, numpy seed 42, sklearn random_state 42; builtin hash() not used; SHA256 for state hashing.
- **Valid centering**: |null_mean|<0.1 and null_std>0.01 required; else MEASUREMENT_INVALID. Recalibration K=24 explicitly targets this (prior K=12 mean 0.1297 std 0.0094 borderline; expected 0.074/0.0104 at K=24).

## 11. Controls (frozen)

### Positive control (correlated-state, recalibrated)

Synthetic correlated-state must achieve BC>=0.30 p_raw<0.01 |null_mean|<0.1 null_std>0.01 on R1 or R2 with frozen construction (L per trajectory, bias 0.70/0.30, DOM family SHA256(L||state||step%3), K=24). Failure => MEASUREMENT_INVALID pipeline_blind. Any change after seeing BC is EXPLORATORY violation. Note K=24 expected to pass both centering thresholds per producer sensitivity.

### Null controls (recalibrated)

- Independent-noise replication with >=6 variants per state must show |BC|<0.05 p>0.10 |null_mean|<0.1 null_std>0.01 on R1/R2 (replicates prior 0.004 bits but with valid variance). If BC>=0.05 p<0.01 with valid null => MEASUREMENT_INVALID pipeline_confounds_independent.
- I.i.d. null must show BC<=0.03 p>0.10 |null_mean|<0.1 null_std>0.01; degenerate triggers MEASUREMENT_INVALID.
- Trajectory-grouped permutation null on correlated dataset must be |null_mean|<0.1 null_std>0.01; degenerate on BOTH R1 and R2 triggers MEASUREMENT_INVALID.

### Data-quality controls

NL=1999 (2000 generated), strata>=5 with >=3 per stratum, singleton<70%, H(S_next|C)>0.3, |R|/N expected 0.018 correlated (36 hashes) and ~0.027 independent with 6 variants (between 0.01 and 0.20), trajectory count >=20, leakage_validOnly expected <60% with fragment-preserving normalization but not gating. Independent ind_H ~2.5 bits.

## 12. Validity Threats & Mitigations

| Threat | Mitigation |
|---|---|
| Target leakage href==URL | Leakage-free A excludes href; DOM_before distinct timestep; diagnostic gap reported; MI(DOM;Action) <0.10 required |
| Split leakage | TF-IDF vocab / Dirichlet counts fit on TRAIN trajectories only (70/30 by trajectory_id); site identity never feature |
| Sampling/policy confounding | Document FSM policy (50x40 uniform among primitives per trajectory), separate policy regularity; determinism via seeds; trajectory_id resampling unit |
| Uncertainty mis-specification (prior audit found item-level shuffle) | Grouped permutation by trajectory_id (fixes item-level); no Gaussian jitter; degeneracy=>MEASUREMENT_INVALID (tightened bias floor 0.1); Cohen d only if std>0.01 |
| Representation loss (hash truncation 5k, K smoothing) | Preserve raw strings, test R1,R2 primary plus R3/R4 exploratory; document truncation and alpha=1/K=24 effect; sensitivity S_URLonly and K=12 vs K=24 comparison exploratory |
| Synthetic-to-real gap | Claim bounded to locally-hosted correlated FSM class, not production correlated regimes or richer visual representations; audit V10 identifiability mitigated by gap over B-DOM-SIMILARITY and MI(DOM;Action) check |
| H=0 determinism ceiling | Report H(S_next|C); if H=0 then BC=0 forced => MEASUREMENT_INVALID environment ceiling; construction ensures H~3.3 |
| Hash tautology action->DOM or DOM->S_next leakage | DOM_before correlated with L not with Action; report MI(DOM;Action) must be <0.10; require BC not explained by action alone |
| Unreachable Bonferroni | N=1999 floor 0.001 <0.01 reachable; report raw and Bonferroni; BC also gates |
| K=12 bias floor 0.129 >0.1 degenerate | Recalibrate to K=24 alpha=1/K (mean 0.074 std 0.0104 expected passing); prior K=12 failure documented as MEASUREMENT_INVALID not falsification; no post hoc relaxation without new prereg |
| Independent null_std degenerate 0.0046 <0.01 | Increase independent variants 3->>=6 per state to raise std>0.01; if still degenerate, report degenerate null_std and trigger MEASUREMENT_INVALID per G2/G4, not silent |
| Result/report drift | All metrics recomputed from raw_results.json; freeze hashes verified before execution; byte-identical re-executable |
| Missing baselines | B-DOM-SIMILARITY/B-MARKOV-1/B-SHUFFLE-GROUPED all executed as frozen with same K=24 grouping; omission => invalid |

## 13. Decision Rules (frozen, pre-outcome)

### Pipeline gates (in order, any triggers MEASUREMENT_INVALID, no claim update)

- G1: positive correlated control BC<0.30 or p_raw>=0.01 or null_std<=0.01 or |null_mean|>=0.1 => pipeline_blind_or_miscalibrated (prevents false negative; prior K=12 BC 0.688 p 0.001 but mean 0.1297>0.1 std 0.0094<0.01 borderline)
- G2: independent-noise replication BC>=0.05 and p<0.10 with valid null (|null_mean|<0.1 null_std>0.01) => pipeline_confounds_independent (cannot distinguish; prior independent BC -0.005 p 0.865 not confounded but degenerate std 0.0046; recalibrated >=6 variants must achieve std>0.01 while |BC|<0.05 to pass)
- G3: i.i.d. null BC>0.03 and p<0.10 with valid null => null miscentered
- G4: primary null degenerate on BOTH R1 and R2 (null_std<=0.01 or |null_mean|>=0.1) => null_degenerate (prior both R1/R2 0.1297/0.0094 borderline; K=24 expected 0.074/0.0104 passing)
- If any G fails, verdict = MEASUREMENT_INVALID, publish gate_table, do not evaluate primary

### Primary decision (only if gates pass)

For each R in {R1,R2}, compute BC_R, p_bonf_R, null_mean_R, null_std_R, BC_sim_R, BC_markov1_R, gap_R = BC_R - max(BC_sim_R, BC_markov1_R), d_R, CI

Define sig(R)=1 if BC_R>0.05 AND p_bonf_R<0.01 AND |null_mean_R|<0.1 AND null_std_R>0.01 AND gap_R>=0.05

- If EXISTS R with sig(R)==1 => SURVIVES_CURRENT_TEST — correlated DOM_before carries predictive information beyond (URL, H_K=3, Action_leakageFree) and beyond ordinary similarity/Markov baselines on locally-hosted correlated-regime SPA via R1 or R2 with recalibrated K=24 valid centering, bounded to tested 6-state FSM class and hash truncation, providing first falsifiable beyond-memory dynamics without Gate0
- If FORALL R, BC_R<=0.05 OR p_bonf_R>=0.01 OR gap_R<0.05 while gates pass => FALSIFIED-IN-SETTING — hash-DOM does not carry predictive information beyond memory/similarity even with constructed session-correlated non-determinism via Bayesian K=24 pipeline, bounded to hash-based DOM and tested K/alpha/pipeline
- Sensitivity (nosmooth, S_URLonly, R3/R4, H_K=2/4, per-15-step regime, N~4000 at K=12 or K=24) not gating; report exploratory but do not alter primary verdict

### Exploratory (only if FALSIFIED and gates passed)

- Report H(S_next|C,D) decomposition, per-strata CMI histogram, MI(L;DOM) vs MI(L;S_next), TF-IDF gap, independent 6-variant stability. These do NOT alter primary FALSIFIED verdict but inform park vs richer representation.

## 14. Consequences

### If SURVIVES (valid gates, recalibrated)

- C-WEB-DYNAMICS ceiling expands to: correlated-state beyond-memory dynamics via hash DOM_before (R1 or R2) on locally-hosted session-regime SPAs via Bayesian DM K=24 N=1999 grouped permutation with BC>0.05 p<0.01 gap>=0.05 valid centering and independent BC~0. First validated beyond-memory correlated signal beyond independent-noise 0.004 bits and beyond synthetic 2D TV/KDE pooled blind spots and beyond TodoMVC title degeneracy.
- Product: distill DOM hash regime detector as mechanism precondition and exploration prior (regime-aware retrieval grouped by latent L, barrier guard for session shifts, freshness sentinel for DOM_before distribution change) into kernel resolve; prioritize BrowserGym/intel collection on session-correlated production sites (auth/cart/personalization) where latent regimes amplify; measure delta-repair cost when session shifts and cross-site holdout transfer; quantify work-compression leverage via regime detection.
- Physics next: test invariance across site types and latent regimes (permission vs user-data vs external API), quantify transfer, test on production correlated SPAs when intel manifests available (now justified).

### If FALSIFIED (valid gates, recalibrated)

- C-WEB-DYNAMICS remains HYPOTHESIS but correlated hash-DOM program closed for this FSM class and K=24 representation: even with DOM_before correlated by construction with latent L determining S_next, visible_text_hash / a11y_tree_hash truncated 5k does not carry detectable predictive information beyond history and similarity/Markov via current pipeline (gap<0.05 or BC<=0.05 or p>=0.01). Combined with prior independent-noise falsification (-0.005) and deterministic 0.0 replication, this closes both independent and correlated hash-DOM factorization on tested FSMs at K=24.
- Product: do NOT invest in hash-DOM regime detectors; Graph/Product rely on trajectory memory/retrieval without physics prior; economics via retrieval/verification/repair amortization alone (C-RESIDUAL-NOVELTY). Still high-value as it prevents wasted physics spend on hash truncation.
- Physics next per director rationale: PARK correlated-DOM program on hash representation or await richer visual/computed-style DOM, interaction event sequences, or true production SPA correlated latent regimes with larger state spaces before further physics spend; do not loop K/N tuning beyond this recalibration; consider orthogonal programs (timescale/barrier superseded, frontier MemoryArena).

### If MEASUREMENT_INVALID (recalibrated still borderline)

- No claim update. Report exact gate failed, per-dataset table, null_mean/std, independent variance, unresolved substrate. Retry not a scientific negative. Preserve epistemic discipline. Smallest unblock already attempted (K=24, >=6 variants); next unblock would be N~4000 per mandate or analytic bias correction, not silent threshold relaxation.

## 15. Analysis Plan (deterministic order, no outcome peeking before freeze)

1. **Verify freeze integrity**: check request.json sha256, spec.json, prereg.md hashes match freeze.json before any computation; record commit HEAD and parent 247a634...
2. **Generate datasets** (deterministic PYTHONHASHSEED=0 numpy 42): (a) correlated-state primary 50x40=2000 N=1999 via generate_correlated.py frozen (same as parent, 36 hashes), (b) independent-noise replication RECALIBRATED 50x40 with >=6 variants per state via generate_independent.py frozen (independent per-step draw), (c) i.i.d. null via generate_iid.py frozen. Save raw_transitions_*.json with fields {trajectory_id, step, URL_before, URL_after, title, Action_primitive, target_sig, DOM_before_visibleText[0:5000], DOM_before_a11y[0:5000], S_next hash, latent L, variant_mod}. Compute sha256 per file.
3. **Compute strata**: for each dataset, build C=(URL_before_normalized, H_K=3 actions) with H_K as defined, report strata_count, strata_ge3, singleton rate, H(S_next|C), leakage diagnostics, cardinality |R|/N, dom_bytes/a11y_bytes.
4. **For each (dataset, R in {R1,R2,R3,R4})**: compute Bayesian DM K=24 alpha=1/K CMI observed, run 1000 trajectory-grouped permutations within each C stratum grouped by trajectory_id seed 42 => BC, null_mean/std, p_raw/p_bonf, d, CI percentiles, BF_10 via Dirichlet-Multinomial Gamma; compute B-DOM-SIMILARITY TF-IDF k5 fit TRAIN only => BC_sim; compute B-MARKOV-1/ K3 MLE fit TRAIN => BC_markov gap; compute B-TRAJECTORY-MEMORY, B-SITE-LEAKAGE, MI(DOM;Action).
5. **Apply gated decision rule** §13, publish per-representation table, permutation histograms, strata tables, gate/control tables, provenance with sha256; no metric built from report before freeze hash.
6. **Commit** all raw transitions, hashes, strata tables, permutation distributions, code paths (generate_*.py, analyze.py) with sha256 in provenance.json; verify re-executable aside from elapsed; include exploratory N~4000 sensitivity if time permits but not gating.

## 16. Freeze Statement

This preregistration is frozen before any outcome data for the recalibrated K=24 (or N~4000) Bayesian CMI decision is inspected. Correlated construction (L per trajectory, bias 0.70/0.30, DOM family SHA256(L||state||step%3), 36 hashes) and independent-noise recalibrated to >=6 variants are defined by construction, not by peeking at correlated BC under K=24. Trajectory-grouped permutation (1000 perms seed 42, unit trajectory_id), Bayesian DM K=24 alpha=1/K N=1999 (recalibrated from K=12 to correct bias floor 0.129->0.074 std 0.0094->0.0104 per producer sensitivity), reachable p<0.01 floor 0.001, and mandatory B-DOM-SIMILARITY/B-MARKOV-1 with gap >=0.05 correct parent audit required_fixes before any new outcome. Gate0 not required by mandate is intentional substrate_available design, not weakened gate. Any deviation after freeze is labeled EXPLORATORY and cannot support confirmatory SURVIVES/FALSIFIED. A new confirmatory claim requires new preregistration. Estimated cost <3h wall-clock, no LLM calls, stdlib only.

## 17. References to Prior Evidence

- Parent EXP-PHYSICS-35782523165 (MEASUREMENT_INVALID borderline |null_mean| 0.1297>0.1 null_std 0.0094<0.01, but BC 0.688 p 0.001 gap 0.688, H 3.302, independent -0.005, IID 0.0013, baselines 0.0, audit NOT blind, K=24 mean 0.074 std 0.0104 would pass) — direct predecessor; this recalibration converts its borderline into confirmatory test
- EXP-PHYSICS-34764605162 (FALSIFIED-IN-SETTING) — independent-noise BC 0.004/0.025 p=1.0 audit V1_independent_noise_bakes_in_null flags correlated open setting; |R| isomorphic, numeric 0.0
- EXP-PHYSICS-35774039080 (MEASUREMENT_INVALID Q=0 substrate_insufficient, PASS audit) — gate_table Q=0, VF-DOM-ABSENCE-VERIFIED on TodoMVC, motivates locally-hosted synthesis
- Frontier 61 pooled TV/KDE/binned tunnel — complementary blind spots (kNN fails scaling, KDE fails rotation, CV>0.5), 95% non-stationary attenuation; orthogonal pivot per director
- EXP-INTEL-35773136560 (0/3 Gate0 exhaustive enumeration) and Gate0 0/3 after BrowserGym/CAP/Mind2Web enumeration — closes production-SPA PMI path, justifies locally-hosted correlated FSM
- Bayesian DM K=12 N=1999 validated estimator (log BF 168-643) but absolute BF -10 to -15 nats on real TodoMVC (2 isomorphs) — reused here recalibrated to K=24
- Codex C-WEB-DYNAMICS HYPOTHESIS, 254 canonical experiments, director REOPEN cognitive_reset true, portfolio_assessment IDLE tunnel_flag true
- SPIDER_MASTER_PROMPT §15-22 (validity gates, strong nulls, identifiability, representation loss), SPIDER_ARCHITECTURE_RESEARCH2 §4-6 (packet, Codex, freeze), AGENTS.md transmission discipline, POLICY.md director mandate, research/EXPERIMENT_PACKET.md mandatory fields (§3 spec.json, §4 result.json)

