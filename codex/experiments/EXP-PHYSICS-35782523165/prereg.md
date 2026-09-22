# EXP-PHYSICS-35782523165 Preregistration — Physics Correlated-State FSM Pivot (PIVOT cognitive_reset, SUPERSEDE)

**Status: DESIGN — FROZEN BEFORE OUTCOME (2026-09-22). No outcome-bearing measurements on correlated-state vs independent-noise FSMs have been inspected for the frozen Bayesian CMI decision.**

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35782523165
- **Lane**: physics
- **Claim**: C-WEB-DYNAMICS — Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity (status HYPOTHESIS per codex/claim_state.json, 63 total experiments, 9/10 recent on C-WEB-DYNAMICS, tunnel true, IDLE after EXP-PHYSICS-35774039080 MEASUREMENT_INVALID)
- **Directive**: Global Research Director PIVOT on C-WEB-DYNAMICS (request.json director_mandate cycle 35781743260, allocation PIVOT cognitive_reset true, parent_handoff_disposition SUPERSEDE, claim_id C-WEB-DYNAMICS). Binding strategic question verbatim in request.json director_mandate.question. Parent handoff is continuity evidence only and MUST NOT override the SUPERSEDE decision (AGENTS.md, EXPERIMENT_PACKET.md, POLICY.md).
- **Parent handoff**: research/experiments/EXP-PHYSICS-35774039080/handoff.json (sha256 b11f1beb12bcd073defaca9635879ac553b1b944f3c606b6640b7b4b0d29fc32) — established/rejected/unknown/do_not_assume distinctions preserved below (§2). Parent was MEASUREMENT_INVALID substrate_insufficient Q=0 qualifying DOM-bearing datasets (dom_bytes 0.0 a11y 0.0 on 10/10 reused TodoMVC raws), not falsification; its frozen question was orthogonal timescale/barrier delta_ACF/Var(q) on TodoMVC/WebShop DOM-bearing hash — superseded by this correlated-state program per director comparative reasoning.
- **Dependencies (binding per mandate)**: runtime, intel (intel manifest still absent per parent handoff: research/intel/ does not exist, /tmp/browsergym_cache absent). Portfolio assessment: Gate0 0/3 real SPAs after 20+61 exhaustive enumerations, C-SEMANTIC-RESOLVE synthetic 1.0 vs verbatim 1.0 gap not live, Bayesian DM K=12 N=1999 first to pass synthetic C1+C3 but BF -10 to -15 nats favoring memory on real TodoMVC.
- **Pre-2.0 / codex baseline**: WP-002B rule minus shuffle +0.0532 no holdout, WP-003 MEASUREMENT_INVALID (leakage, Gaussian jitter, hash(site) seed), frontier 61 pooled TV/KDE/binned blind spots (kNN fails scaling rho -0.12 vs KDE fails rotation rho 0.286), availability_only synthetic estimator tuning 44-deep runtime tunnel, EXP-PHYSICS-34764605162 falsified independent-noise DOM_before (BC 0.004 bits random_API, 0.025 bits timing_dependent, R2 0.003, Bonferroni p=1.0) with audit V1_independent_noise_bakes_in_null flagging correlated regime as open setting.

## 2. Inherited Scientific State (from parent handoff — continuity evidence, not agenda)

Per AGENTS.md, EXPERIMENT_PACKET.md and POLICY.md, parent handoff `next_question` is advisory local continuity only. Director mandate PIVOT SUPERSEDE is binding and explicitly reasons: timescale/barrier program would repeat MEASUREMENT_INVALID on same TodoMVC variants (all 5 have zero DOM fields) and absent WebShop trajectories, while correlated FSM constructs correlation by design and has higher measurement readiness.

### Established (justified at stated ceiling)

- Q=0 qualifying datasets under frozen relaxed sufficiency verified by independent audit recompute: 5/5 TodoMVC variants NL 85-107 (>=50), strata_ge3 12-13, singleton 0.0, leakage 0.1769-0.2846, but dom_bytes coverage 0.0 and a11y coverage 0.0 on all variants => qualifies false (gate_table.json Q=0 fe0474a07..., audit VF-GATE-CORRECT).
- DOM/a11y absence is field absence, not small DOM: 10/10 reused raws contain only keys {site,session,url_before,url_after,title_before,title_after,action_primitive,action_target,timestamp,error} with no dom_bytes/visibleText or a11y_tree (audit VF-DOM-ABSENCE-VERIFIED critical).
- WebShop/BrowserGym substrate absent: research/intel/ absent, /tmp/browsergym_cache absent, 0 browsergym files under research/ (audit VF-PROVENANCE-REPRODUCIBILITY).
- Freeze integrity: all hashes MATCH freeze.json before computation; 10/10 reused raw sha256 MATCH prior result.json artifacts; PYTHONHASHSEED=0 stdlib only deterministic gate path.
- Frozen halt compliance: Q==0 => MEASUREMENT_INVALID substrate_insufficient, do not test H_T/H_B, do not run PC-METASTABLE/PC-BARRIER or nulls — correctly NOT_RUN unknown per audit VF-CONTROLS-NOT-RUN, pipeline blindness unknown.
- Leakage control: fragment-preserving normalization (lowercase, strip query, preserve #/, strip trailing slash) leakage 0.1769-0.2846 (audit VF-LEAKAGE-NORMALIZATION).
- C-WEB-DYNAMICS remains HYPOTHESIS, MEASUREMENT_INVALID substrate_insufficient, no mechanical prior validated (codex 59 events).

### Rejected (bounded)

- No bounded rejection of timescale/barrier via R1/R2 on TodoMVC/WebShop — primary S==0 not evaluated due Q==0; C-WEB-DYNAMICS not closed on this regime.

### Unknown (open, partially superseded)

- What delta_ACF(3), Var(q), dip etc. would be observed on qualifying DOM-bearing substrate — entirely unknown, zero bits toward H_T/H_B — superseded; new unknown is what Bayesian CMI BC detects on correlated-state vs independent-noise FSMs.
- What branched_revisit_count, Var(q) etc. would be observed — superseded.
- Whether synthetic positive controls (delta_ACF>=0.12 BF>10, Var>=0.12) pass — superseded; new controls are correlated BC>=0.30 vs independent BC~0.
- Whether DOM-bearing trajectories can be obtained via re-collection or intel — remains unknown but NOT required for this pivot (director explicitly: does not require new Gate0 production SPAs).
- Whether singleton rate, strata>=5, H ceiling, null_std>0.01 remain satisfiable on richer substrate — carries forward as risk, now mitigated by hosting own correlated FSM where H>0.3 by construction.
- Angular hash normalization ambiguity — to be resolved pre-freeze for future SPAs.

### Do Not Assume

- Do not assume C-WEB-DYNAMICS falsified/supported — no production orthogonal measurement exists; Q==0 is infrastructure, not falsification.
- Do not assume pipeline blind or validated — controls NOT_RUN at Q==0, blindness unknown; do not encode degenerate null_std==0 as falsification.
- Do not assume URL|title-only hash can substitute for DOM — H_T required B-DOM-SIMILARITY gap incomputable without DOM; this experiment CORRECTLY hosts DOM by construction via SHA256(L||state).
- Do not assume locally-hosted Express synthetics substitute for TodoMVC/WebShop under relaxed sufficiency — forbidden under parent spec, but this pivot is ALLOWED to host correlated synthetic FSM as primary because mandate explicitly says locally-hosted SPAs with session-correlated non-determinism, no Gate0 production SPAs required — distinction is intentional: parent forbade substituting Express for TodoMVC/WebShop *under relaxed sufficiency for timescale*; this design constructs its own substrate via frozen correlated chain, bounded to that FSM class.
- Do not assume pooled TV/KDE/binned, history CMI, timescale ACF, barrier committor are interchangeable — they are orthogonal (director: pooled density vs within-strata conditional PMI vs lag autocorrelation/dwell vs revisit variance); prior complementary blind spots do not imply CMI null.
- Do not assume audit PASS means SURVIVES — audit confirms correct MEASUREMENT_INVALID handling, claim_ceiling remains HYPOTHESIS.
- Do not assume 10/10 sha256 MATCH implies substrate sufficient — coverage must be explicitly checked (dom_bytes>=500).

This design preserves all distinctions and explains why SUPERSEDE to correlated FSM is correct: timescale/barrier repeats gating failure, correlated FSM is substrate_available by design and tests the audit-flagged open setting.

## 3. Scientific Question (binding, refined to falsifiable experiment)

Director strategic question (request.json director_mandate.question verbatim):

> On locally-hosted SPAs with session/state-correlated non-determinism where DOM_before (visible_text_hash and a11y_tree_hash) is correlated by construction with latent environment state (session/permission/user data) - not independent per-step observation noise which prior EXP-PHYSICS-34764605162 falsified (BC 0.004 bits, R2 0.003) - does trajectory-grouped permutation CMI at Bayesian Dirichlet-Multinomial K=12 (N=1999, seed 42) detect I(S_next; DOM_before | URL, H_K=3, Action_leakageFree) >0 with valid null centering (|null_mean|<0.1, null_std>0.01, positive correlated control BC>=0.30 p<0.01, independent-noise control BC~0) and exceed B-DOM-SIMILARITY and B-MARKOV-1 nulls by >=0.05, thereby providing the first falsifiable beyond-memory dynamics test that does not require new Gate0 production SPAs?

Refined falsifiable experiment: On a locally-hosted 6-state Express SPA where latent L (session/permission regime persisting per trajectory, 50 trajectories x40 steps =2000 transitions) correlates DOM_before hash family with S_next transition bias, does Bayesian DM K=12 N=1999 trajectory-grouped permutation CMI detect I(S_next; DOM_before | URL, H_K=3, Action_leakageFree) >0.05 with p<0.01, |null_mean|<0.1 null_std>0.01, exceeding B-DOM-SIMILARITY and B-MARKOV-1 by >=0.05 on R1 or R2, while independent-noise replication (same pipeline on per-step independent DOM variant) remains BC~0 (|BC|<0.05 p>0.10) and positive correlated control achieves BC>=0.30 p<0.01? Either SURVIVES (first correlated beyond-memory DOM dynamics without Gate0) or FALSIFIED (hash DOM insufficient even with constructed correlation) changes claim/product decision.

## 4. Motivation & Why This Is the Smallest High-Information Test

### 4.1 Tunnel diagnosis (why not another timescale/barrier or estimator tuning)

- Prior correlated vs independent gap: EXP-PHYSICS-34764605162 tested independent per-step observation noise (3 variants random_API, 4 variants timing_dependent, each step independent RNG) and found BC 0.004/0.025 bits p=1.0 indistinguishable from null, determinism 0.361/0.308 confirming non-determinism introduced but reflecting DOM variant multiplicity not FSM transition non-determinism (audit V5). Audit explicitly flagged V1_independent_noise_bakes_in_null: independent noise bakes in null by construction; correlated DOM_before|latent state is the open setting where DOM correlates with latent session determining S_next. Re-tuning TV/KDE bandwidth or alpha on same 12-state synthetic SPA yields diminishing returns (director agent_priors: 44+ streak yielding FALSIFIED per-function heterogeneity).
- Gate0 exhaustive failure: 0/3 real SPAs after 20+61 enumerations (BrowserGym/CAP/Mind2Web/Docker), dom_bytes 0.0 on reused TodoMVC, /tmp/browsergym_cache absent — any experiment requiring new DOM-bearing BrowserGym trajectories repeats MEASUREMENT_INVALID substrate_insufficient (parent Q=0). Timescale/barrier pivot (EXP-PHYSICS-35774039080) already reused TodoMVC raws and correctly halted at Q=0 before any H_T/H_B test; re-freezing same program without new substrate would reproduce same halt.
- Bayesian DM K=12 N=1999 is first estimator to pass synthetic C1+C3 null-centering (log BF 168-643) but absolute BF -10 to -15 nats favors memory on real TodoMVC (2 effective isomorphs) — not pipeline bug, calibrated negative. Reusing this validated estimator on a *correlated* construction where signal is planted is the smallest change that can flip bit from null to detection without requiring new production infrastructure.

### 4.2 Why correlated FSM is orthogonal and substrate_available

- Independent noise: DOM variant independent of S_next given C => I(S_next;DOM|C)=0 by construction (bakes in null). Correlated regime: L -> (DOM, S_next) jointly, so DOM_before is noisy proxy for L which biases transition => I>0 even after conditioning on URL and H_K=3. Mathematically distinct: independent falsification does not imply correlated null; they test different graphical models (L->DOM independent vs L->DOM and L->S_next).
- Substrate_available: locally-hosted Express SPA with synthetic L per trajectory (or 15-step regime) is constructible in <100 lines, no browser, no intel manifest, no dom_bytes gate. Provides at least 3 DOM hashes per (S,L) but L uniquely identifiable from hash family, ensuring BC>=0.30 reachable (theoretical capacity >=0.40 bits at P(L=A)=0.5 and transition bias 0.70/0.30). This bypasses 0/5 No_SPA_FOUND and 0.0 dom_bytes traps entirely.
- Strong nulls exceed requirement: B-DOM-SIMILARITY (TF-IDF k5) mandatory per mandate tests ordinary similarity, B-MARKOV-1 tests Markov order-1, independent-noise replication is within-lane exact falsified control. Trajectory-grouped permutation with |null_mean|<0.1 null_std>0.01 fixes Laplace floor 0.3056 degenerate on near-unique hash DOMs seen in prior.

### 4.3 Why smallest high-information

- Positive or negative outcome changes C-WEB-DYNAMICS ceiling and product decision: SURVIVES => first beyond-memory dynamics via correlated hash DOM without Gate0, justifies SPA regime detectors as mechanical priors for parameterized inheritance; FALSIFIED => closes correlated hash-DOM on locally-hosted regime FSMs after independent already closed, forcing physics to park or await richer visual/computed-style representations outside hash truncation — either materially changes product architecture (distill or not distill DOM hash regime). MEASUREMENT_INVALID (positive control <0.30 or independent confounded or null degenerate) is also informative and refuses false negative, documenting pipeline blindness.
- Uses validated pipeline (Bayesian DM K=12) with trajectory-grouped permutation (fixes item-level shuffle audit finding), reachable Bonferroni p<0.01 at N=1000/1999 (floor 0.001/0.0005), and mandatory baselines — no new estimator invention.

## 5. Hypotheses (frozen, exhaustive)

### H_correlated (primary, beyond-memory correlated dynamics)

On correlated-state SPA dataset (50 trajectories x40 steps, L per trajectory, 2000 transitions, H(S_next|C)>0.3), Bayesian DM K=12 N=1999 bias-corrected CMI BC = I(S_next; DOM_before | URL, H_K=3, Action_leakageFree) >0.05 with trajectory-grouped permutation Bonferroni p<0.01 (over R1/R2 x baselines, max 8 tests), |null_mean|<0.1 null_std>0.01, exceeding B-DOM-SIMILARITY BC_sim and B-MARKOV-1 BC_markov1 by >=0.05 bits on R1 visible_text_hash or R2 a11y_tree_hash. Cohen d = BC/null_std reported, 95% CI via permutation percentiles.

### H_positive_control_correlated

Same pipeline on correlated synthetic (identical to H_correlated but designated positive control) must achieve BC>=0.30 p<0.01 null_std>0.01 |null_mean|<0.1 on R1 or R2. Pipeline blind if fails. Theoretical capacity >=0.40 bits ensures 0.30 reachable; frozen construction uses L in {A,B} with transition bias 0.70/0.30 and DOM hash family SHA256(L||state||step%3). Any outcome where BC<0.30 triggers MEASUREMENT_INVALID, not falsification.

### H_null_independent (negative control)

Identical Bayesian DM K=12 N=1999 trajectory-grouped permutation on independent-noise replication (per-step independent DOM variant 3-4 hashes per state, same FSM but L absent, DOM variant independent of S_next) must show BC~0 (|BC|<0.05) with p>0.10 and null_std>0.01 |null_mean|<0.1, replicating prior falsification 0.004 bits. If BC>=0.05 p<0.01, pipeline confounds independence => MEASUREMENT_INVALID.

### H_null_iid

I.i.d. synthetic null (same marginal P(S) as correlated but S_next drawn i.i.d. per step, seed 42) must show BC<=0.03 p>0.10 BF nats<0; degenerate null_std<=0.01 => MEASUREMENT_INVALID.

### H_null_shuffled (permutation null on primary)

Within-strata grouped shuffle DOM_before labels on correlated dataset: null distribution with |null_mean|<0.1 and p>0.10 for null datasets with null_std>0.01; degenerate triggers MEASUREMENT_INVALID.

## 6. Data Generation & Reuse

### 6.1 Primary correlated-state SPA (locally-hosted, no external dependency)

- **Construction** (frozen in generate_correlated.py, seeds PYTHONHASHSEED=0 numpy 42): 6-state FSM states 0-5, 4 Action primitives uniform (click/fill/navigate/submit), target_sig = role+name+testId (never href). Latent L in {A,B} sampled per trajectory (or per 15-step regime with P(flip)=0.07, document which and use per-trajectory for primary to maximize correlation). Transition: P(S_next | S_current, Action, L=A) favors basin {0,1,2} with 0.70 vs 0.30 for {3,4,5}, L=B mirrored (0.30/0.70). Add p_stay 0.70 within basin. This gives H(S_next|C) ~0.9 bits, determinism 0.60-0.75 (not 1.0). URL_before = `https://spa.local/#/state_{S_current}` (hash fragment preserved, lowercased). DOM_before = SHA256(str(L) + '|' + str(S_current) + '|' + str(step%3)) -> hex truncated but family distinct per L; visibleText = f"user:{L} state:{S_current} variant:{step%3}" innerText, a11y tree = serialized AX with role `banner` name `user:{L}`. Thus R1/R2 hashes correlate with L but are not identical to S_next, requiring inference. Generate 50 trajectories x40 steps =2000 transitions, analyze N=1999 (drop last incomplete). Report unique_L per trajectory distribution, Dom_family count, S transition matrix per L.
- **Sample size**: 2000 transitions (N=1999) gives ~200 strata (URL x H_K actions) with avg 10 per stratum, power for BC 0.10 at SE ~0.03 with 1000 perms, BF calibration N/K=166 per state >1.
- **Provenance**: record FSM code sha256, seeds, action sequences, DOM snapshots with hashes, latent L per step.

### 6.2 Independent-noise replication (null control, reuses prior logic but regenerated for pipeline parity)

- Same 6-state FSM but without L: DOM variant = independent RNG draw among 3 hashes per state (variant_mod = rng.choice(3) seeded per step, independent of S_next). Transition without L bias (uniform across basins, p_stay 0.50). Generate 50x40 =2000 transitions. Expect BC~0 per prior 0.004 bits. This is the exact V1_independent_noise setting that bakes in null.

### 6.3 I.i.d. synthetic null

- Same marginal P(S) as correlated (estimated from correlated run) but S_next drawn i.i.d. independent per step (seed 42), DOM_before still correlated with phantom L but S_next independent => BC should be 0, BF favors order1.

### 6.4 No reuse of TodoMVC/WebShop trajectories for primary

- Prior TodoMVC raws have 0.0 dom_bytes and title=1 degeneracy, and would require relaxed gate; they are not used as primary here to avoid Q=0 halt. Their gate_table is still published as diagnostic but not gating. If BrowserGym WebShop manifests appear at research/intel/manifest.json they are documented but not required; primary is self-hosted correlated FSM.

### 6.5 Sample size & power calibration

- Theoretical channel capacity at binary L with transition bias 0.70/0.30: I(S_next; L | C) = 1 - Hb(0.3)=0.1187? Actually with L biasing basin, capacity ~0.40 bits when pooling across S_current marginal; with per-stratum conditioning, achievable CMI ~0.35-0.45 bits at full L recovery. At 60% DOM->L recovery (hash family leaks 2/3 variants), expected BC ~0.30-0.35, exceeding 0.05 primary and 0.30 positive control. Power via permutation CI width ~2*null_std; null_std on correlated hash expected 0.02-0.04 (non-degenerate because DOM families not near-unique, unlike prior near-unique hash where Laplace floor 0.3056 degenerate; here DOM families =2 per state x3 variants =6 unique hashes per state, cardinality |R|/N ~0.02, null_std>0.01 satisfied).

## 7. State, Action, History, DOM Operational Definitions

### 7.1 State S_next

Primary S_next = SHA256(normalize(URL_after) || '|' || normalize(title_after)) where normalize(URL)=lowercase, strip query ?session=/?token=, preserve SPA hash fragment #/, strip trailing slash; normalize(title)=trim lowercased truncated 200 chars (constant title allowed, title_before not required). Exploratory: S_URLonly SHA256(norm(URL_after)) only, S_hashFragmentOnly. S_next distinct timestep from DOM_before (t -> t+1, no post-state leak). Report unique_titles, title_entropy, URL fragment distribution.

### 7.2 Action A_leakageFree

A=(primitive, target_sig) primitive in {click, fill, navigate, select}, target_sig=role+name+testId+aria-label (never href/URL/src). Link target_href never enters A. Diagnostic A_leaky = A+href for leakage gap only; B-SITE-LEAKAGE-DIAGNOSTIC reports BC_leaky - BC_leakageFree. Action distribution per dataset reported; policy regularity separated.

### 7.3 History H_K=3

H_K=(A_{t-2},A_{t-1},A_t, S_{t-2},S_{t-1},S_t) last 3 steps; strata key C=(URL_before_normalized, H_K_actions) where URL_before_normalized is URL_only without title to avoid state leakage into condition. Require strata_count>=5 unique C with >=3 per stratum; singleton_SA_rate<70%; report H(S_next|C) ceiling (must be >0.2, else CMI mathematically forced 0 => MEASUREMENT_INVALID) and strata_ge3 count. Rare strata <3 excluded from BC point estimate but counted in validity_notes.

### 7.4 DOM_before representations (tested independently, not ensembled)

- R1 visible_text_hash: SHA256(visibleText[0:5000] innerText, e.g., "user:A state:2 variant:1")
- R2 a11y_tree_hash: SHA256(serialized AX tree role/name/value up to 5k chars via simulated Accessibility.getFullAXTree, e.g., `role:banner name:user:A`)
- R3 multi_feature_hash: SHA256(R1 || R2) exploratory
- R4 numeric_structural: element_count/tree_depth/interactive_density/form_count exploratory (expected degenerate as prior 0.0)

Raw observables preserved (dom_bytes truncated 5k, a11y_bytes 5k) with documented truncation; hash collision/truncation loss disclosed. Primary claim requires R1 or R2 only.

## 8. Measures

### 8.1 Primary: Bayesian DM bias-corrected CMI

For each (dataset, R in {R1,R2}):
```
H(S_next|C) Dirichlet-Multinomial K=12 alpha=1/K: log P(counts | alpha) via Gamma
H(S_next|C,DOM) similarly stratified by (C,DOM_hash)
CMI_obs = H(S_next|C) - H(S_next|C,DOM)  (plug-in via posterior mean)
BC = CMI_obs - mean(CMI_perm_grouped)  bias-corrected
Null distribution: 1000 trajectory-grouped permutations of DOM_before labels within each C stratum, grouped by trajectory_id seed 42, preserving per-trajectory DOM frequencies
Report: BC, null_mean, null_std, p_raw = (1+#{perm>=CMI_obs})/1001 one-sided, p_bonf = min(1, p_raw * n_tests) n_tests up to 8, Cohen d = BC/null_std, 95% CI via permutation percentiles (2.5th/97.5th), cardinality |R|/N, strata stats, H ceiling
Primary is BC_R1 / BC_R2; also report CMI_obs uncorrected for diagnostic
BF_10 for order3 vs order1 Markov via same DM K=12 N=1999 (closed-form Gamma) on TRAIN counts, log BF nats; calibrate on i.i.d. null must favor order1 (nats<0)
```

### 8.2 Baselines (same estimator, same grouping)

- B-DOM-SIMILARITY BC_sim: TF-IDF cosine k=5 over DOM visible_text/a11y text fit on TRAIN only, predict S_next via similarity, compute BC_sim via same Bayesian DM on (C, NN_pred); report gap delta_sim = BC - BC_sim must be >=0.05
- B-MARKOV-1 BC_markov1: MLE transition matrix P(S_next|URL_before,A) fit TRAIN grouped, predict S_next, compute BC_markov1 via same CMI estimator; gap delta_markov1 = BC - BC_markov1 >=0.05 required
- B-MARKOV-K3 accuracy and BC_hist reported
- B-SHUFFLE-GROUPED null distribution already described
- B-TRAJECTORY-MEMORY memorization ratio
- B-SITE-LEAKAGE gap

### 8.3 Auxiliary per dataset per R

NL, strata_count, strata_ge3, singleton_rate, leakage_validOnly, link_share, H(S_next|C), unique_DOM_hashes, |R|/N, null_mean/std, Cohen d, CI, MI(DOM;Action) tautology check, action distribution, BF nats, card stats.

## 9. Null Models & Baselines (strong, all executed as frozen)

Enumerated in spec baselines / §8.2. All executed with identical grouping (trajectory_id), seeds 42, preprocessing fit on TRAIN only, Dirichlet prior alpha=1/K K=12, N up to 1999. Mandatory B-DOM-SIMILARITY and B-MARKOV-1 must be executed; their gap is gating for SURVIVES. No silent omission: if baseline cannot be computed (singleton strata), publish validity_note and trigger MEASUREMENT_INVALID for that representation.

## 10. Statistical Tests & Uncertainty (frozen, corrected per audits)

- **Permutation**: 1000 trajectory-grouped shuffles of DOM_before labels within each C stratum, preserving per-trajectory frequencies and within-trajectory DOM sequences, seed 42 deterministic, grouped by trajectory_id. Null = BC_perm distribution. Resampling unit = trajectory_id; no Gaussian jitter.
- **p-value**: p_raw one-sided per above, Bonferroni primary p_bonf = min(1, p_raw * n_tests) where n_tests = n_R * (1 primary +2 baselines) up to 8, alpha 0.01 (director). Also report raw. Positive control single test raw p<0.01 reachable at N=1000 floor 0.001; N=1999 permutation distinct but use 1000 grouped perms per spec, floor 0.001.
- **BF**: log BF computed exactly via Gamma functions, no resampling; BF nats >2.3 corresponds BF>10 strong, but primary gates on CMI BC not BF; BF reported as auxiliary and calibrated on i.i.d. null (must be <0).
- **Effect size**: Cohen d = BC / null_std (null_std>0.01 required); 95% CI via grouped permutation percentiles, NOT Gaussian.
- **Seed determinism**: PYTHONHASHSEED=0, numpy seed 42, sklearn random_state 42; builtin hash() with PYTHONHASHSEED=0 deterministic but still use SHA256 for state hashing; do NOT use hash() for grouping.
- **Valid centering**: |null_mean|<0.1 (bias floor <0.1 bits, tightening from prior 0.3056 degenerate) and null_std>0.01 required; else MEASUREMENT_INVALID.

## 11. Controls (frozen)

### Positive control (correlated-state)

Synthetic correlated-state must achieve BC>=0.30 p_raw<0.01 |null_mean|<0.1 null_std>0.01 on R1 or R2 with frozen construction (L per trajectory, bias 0.70/0.30, DOM family SHA256(L||state||step%3)). Failure => MEASUREMENT_INVALID pipeline_blind_correlated. Construction exactly as spec positive_control; any change after seeing real BC is EXPLORATORY violation.

### Null controls

- Independent-noise replication must show |BC|<0.05 p>0.10 |null_mean|<0.1 null_std>0.01 on R1/R2 (replicates prior 0.004 bits). If BC>=0.05 p<0.01 => MEASUREMENT_INVALID pipeline_confounds_independent (cannot distinguish correlation from independent noise, would make positive control trivial).
- I.i.d. null must show BC<=0.03 p>0.10 BF nats<0 |null_mean|<0.1 null_std>0.01; degenerate triggers MEASUREMENT_INVALID.
- Trajectory-grouped permutation null on correlated dataset must be |null_mean|<0.1 null_std>0.01; degenerate triggers MEASUREMENT_INVALID for that representation.

### Data-quality controls

NL=1999 (2000 generated), strata>=5 with >=3 per stratum, singleton<70%, H(S_next|C)>0.3, |R|/N between 0.01 and 0.20 (avoid near-unique degeneracy), trajectory count >=20. Report leakage_validOnly (expected <60% with fragment-preserving normalization) but not gating.

## 12. Validity Threats & Mitigations

| Threat | Mitigation |
|---|---|
| Target leakage href==URL | Leakage-free A excludes href; filter not needed for synthetic but report diagnostic gap; DOM_before distinct timestep from S_next; action_with_href gap reported. |
| Split leakage | TF-IDF vocab / transition matrix / Dirichlet counts fit on TRAIN trajectories only (70/30 by trajectory_id); site identity never feature. |
| Sampling/policy confounding | Document FSM policy (50x40 uniform action sampling), separate policy regularity; determinism via seeds; trajectory_id resampling unit. |
| Uncertainty mis-specification | Grouped permutation by trajectory_id (fixes item-level shuffle audit finding); no Gaussian jitter; report null_std and singleton rate; degeneracy=>MEASUREMENT_INVALID (tightened bias floor 0.1). |
| Representation loss | Preserve raw DOM/a11y strings, test R1,R2 primary plus R3/R4 exploratory; require R1 or R2; document hash truncation 5k; sensitivity S_URLonly. |
| Synthetic-to-real gap | Primary is synthetic correlated regime by mandate (substrate_available); claim bounded to locally-hosted correlated FSM class, not production correlated regimes or richer visual representations; audit V10 identifiability: state alias not emergent dynamics — mitigated by reporting MI(DOM;Action) and requiring gap over B-DOM-SIMILARITY. |
| H=0 determinism ceiling | Report H(S_next|C); if H=0 then BC=0 mathematically forced => MEASUREMENT_INVALID environment ceiling, not falsification; construction ensures H~0.9. |
| Hash tautology action->DOM | DOM_before correlated with L not with Action; report MI(DOM_before; Action) must be <0.10 bits (or if high, require BC not explained by action alone via B-ACTION-FREQ shuffled). |
| Unreachable Bonferroni | N=1000 raw p<0.01 reachable (floor 0.001); report both raw and Bonferroni; BC also gates via absolute 0.05. |
| Laplace floor 0.3056 degenerate | Tightened to |null_mean|<0.1 and null_std>0.01; DOM families not near-unique (6 per state) avoids degeneracy unlike prior near-unique hash where perm_std~0. |
| Result/report drift | All metrics recomputed from raw_results.json; freeze hashes verified before execution; byte-identical aside from elapsed. |
| Missing baselines | B-DOM-SIMILARITY/B-MARKOV-1/B-SHUFFLE-GROUPED all executed as frozen with same grouping; omission => invalid. |

## 13. Decision Rules (frozen, pre-outcome)

### Pipeline gates (in order, any triggers MEASUREMENT_INVALID, no claim update)

- G1: positive correlated control BC<0.30 or p_raw>=0.01 or null_std<=0.01 or |null_mean|>=0.1 => pipeline_blind_correlated.
- G2: independent-noise replication BC>=0.05 and p<0.10 with valid null (|null_mean|<0.1 null_std>0.01) => pipeline_confounds_independent (cannot distinguish).
- G3: i.i.d. null BC>0.03 and p<0.10 with valid null => null miscentered.
- G4: primary null degenerate on BOTH R1 and R2 (null_std<=0.01 or |null_mean|>=0.1) => null_degenerate.
- If any G fails, verdict = MEASUREMENT_INVALID, publish gate_table, control tables, unresolved substrate, do not evaluate primary.

### Primary decision (only if gates pass)

For each R in {R1,R2}, compute BC_R, p_bonf_R, null_mean_R, null_std_R, BC_sim_R, BC_markov1_R, gap_R = BC_R - max(BC_sim_R, BC_markov1_R), d_R, CI.

Define sig(R)=1 if BC_R>0.05 AND p_bonf_R<0.01 AND |null_mean_R|<0.1 AND null_std_R>0.01 AND gap_R>=0.05.

- If EXISTS R with sig(R)==1 => SURVIVES_CURRENT_TEST — correlated DOM_before carries predictive information beyond (URL, H_K=3, Action_leakageFree) and beyond ordinary similarity / Markov baselines on locally-hosted correlated-regime SPA via R1 or R2, bounded to tested FSM class and hash truncation, providing first falsifiable beyond-memory dynamics without Gate0 production SPAs.
- If FORALL R, BC_R<=0.05 OR p_bonf_R>=0.01 OR gap_R<0.05 while gates pass => FALSIFIED-IN-SETTING — hash-DOM does not carry predictive information beyond memory/similarity even with constructed session-correlated non-determinism via Bayesian K=12 N=1999 pipeline, bounded to hash-based DOM and tested K/alpha/pipeline.
- Sensitivity (nosmooth Dirichlet, S_URLonly, R3/R4, H_K=2/4, per-strata CMI distribution) not gating.

### Exploratory (only if FALSIFIED and gates passed)

- Report H(S_next|C,D) vs H(S_next|C) decomposition, per-strata CMI histogram, action-conditioned vs marginal, MI(L;DOM) vs MI(L;S_next), TF-IDF gap vs hash gap, dwell spectra if any. These do NOT alter primary FALSIFIED verdict but inform park vs richer representation.

## 14. Consequences

### If SURVIVES

- C-WEB-DYNAMICS ceiling expands to: correlated-state beyond-memory dynamics via hash DOM_before (R1 or R2) on locally-hosted session-regime SPAs via Bayesian DM K=12 N=1999 grouped permutation with BC>0.05 p<0.01 exceeding similarity/Markov by >=0.05. First real (hosted) beyond-memory signal beyond independent-noise 0.004 bits and beyond synthetic 2D TV/KDE and beyond TodoMVC title degeneracy.
- Product: distill DOM hash regime detector as mechanism precondition and exploration prior (regime-aware retrieval, barrier guard, freshness sentinel for session shift). Prioritize intel collection on session-correlated production sites (auth/cart/personalization) where latent regimes amplify. Next: scope across site types, cross-site holdout transfer, delta-repair cost when session shifts.
- Physics next: test invariance across site types and latent regime definitions (permission vs user-data vs external API), quantify transfer, and test on production correlated SPAs when intel manifests available.

### If FALSIFIED

- C-WEB-DYNAMICS remains HYPOTHESIS but correlated hash-DOM program closed for this FSM class and representation: even with DOM_before correlated by construction with latent L determining S_next, visible_text_hash / a11y_tree_hash truncated 5k does not carry detectable predictive information beyond history and similarity/Markov via current pipeline. Combined with prior independent-noise falsification (0.004 bits) and deterministic 0.0 replication, this closes both independent and correlated hash-DOM factorization on tested FSMs.
- Product: do NOT invest in hash-DOM regime detectors; Graph/Product rely on trajectory memory/retrieval without physics prior; economics via retrieval/verification/repair amortization alone.
- Physics next per director rationale: park correlated-DOM program on this representation or await richer visual/computed-style representations (visual layout, computed CSS, interaction sequences) outside hash truncation, or true production SPA correlated latent regimes with larger state spaces, before further physics spend; do not loop estimator tuning on 12-state synthetic SPA.

### If MEASUREMENT_INVALID

- No claim update. Report exact gate failed, per-dataset table, control tables, null_mean/std, unresolved substrate. Retry not a scientific negative. Preserve epistemic discipline (refuse false negative from degenerate constants or pipeline blindness). Document smallest unblock (recalibrate K/alpha, enlarge regime bias, fix grouping).

## 15. Analysis Plan (deterministic order, no outcome peeking before freeze)

1. **Verify freeze integrity**: check request.json sha256 25aaef941fcc4aecc7b4a23be9f84202f9c66c113c650b1610db7d28d645c206, spec.json and prereg.md hashes match freeze.json before any computation (if freeze.json not yet present, record hashes).
2. **Generate datasets** (deterministic seeds PYTHONHASHSEED=0 numpy 42): (a) correlated-state primary 50x40=2000 transitions N=1999 via generate_correlated.py frozen, (b) independent-noise replication 50x40 via generate_independent.py frozen, (c) i.i.d. null via generate_iid.py frozen. Save raw_transitions.json with fields {trajectory_id, step, URL_before, URL_after, title, Action_primitive, target_sig, DOM_before_visibleText[0:5000], DOM_before_a11y[0:5000], S_next hash, latent L}. Compute sha256 per file.
3. **Compute strata**: for each dataset, build C=(URL_before_normalized, H_K=3 actions) with H_K as defined, report strata_count, strata_ge3, singleton rate, H(S_next|C), leakage diagnostics.
4. **For each (dataset, R in {R1,R2,R3,R4})**: compute Bayesian DM CMI observed, run 1000 trajectory-grouped permutations within each C stratum grouped by trajectory_id seed 42 => BC, null_mean/std, p_raw/p_bonf, d, CI percentiles; compute BF_10 via Dirichlet-Multinomial Gamma closed-form on TRAIN counts K=12 alpha=1/K; compute B-DOM-SIMILARITY TF-IDF k5 fit TRAIN only => BC_sim; compute B-MARKOV-1/ K3 MLE fit TRAIN => BC_markov1/hist gap; compute B-TRAJECTORY-MEMORY, B-SITE-LEAKAGE.
5. **Apply gated decision rule** §13, publish per-representation table, permutation histograms, strata tables, gate/control tables, provenance with sha256; no metric built from report before freeze hash.
6. **Commit** all raw transitions, hashes, strata tables, permutation distributions, code paths (generate_*.py, analyze.py) with sha256 in provenance.json; verify byte-identical re-executable aside from elapsed.

## 16. Freeze Statement

This preregistration is frozen before any outcome data on correlated-state vs independent-noise FSMs is inspected for the frozen Bayesian CMI decision. Correlated construction (L per trajectory, bias 0.70/0.30, DOM family SHA256(L||state||step%3)) and independent-noise replication are defined by construction, not by peeking at real correlated BC. Trajectory-grouped permutation (fixes item-level shuffle), Bayesian DM K=12 N=1999 (first to pass synthetic C1+C3, calibrated |null_mean|<0.1 null_std>0.01), reachable p<0.01 at N=1000/1999 floor 0.001, and mandatory B-DOM-SIMILARITY/B-MARKOV-1 execution correct parent audit required_fixes before any new outcome is observed. Relaxed Gate0 not required by mandate is intentional substrate_available design, not weakened gate. Any deviation after freeze is labeled EXPLORATORY and cannot support confirmatory SURVIVES/FALSIFIED. A new confirmatory claim requires a new preregistration. Estimated cost <3h wall-clock, no LLM calls.

## 17. References to Prior Evidence

- Parent EXP-PHYSICS-35774039080 (MEASUREMENT_INVALID Q=0, PASS audit) — gate_table.json Q=0, VF-DOM-ABSENCE-VERIFIED, VF-CONTROLS-NOT-RUN preserved; threshold-construction infeasibility (capacity 0.1187) motivates off-CMI pivot but now SUPERSEDE to correlated FSM per director.
- EXP-PHYSICS-34764605162 (FALSIFIED-IN-SETTING, COMPLETE) — independent-noise BC 0.004/0.025 p=1.0 audit V1_independent_noise_bakes_in_null flags correlated open setting; |R| isomorphic, numeric 0.0 — this design is direct falsifiable follow-up on that gap.
- EXP-PHYSICS-35756224948 etc. — synthetic capacity and null floor analysis.
- EXP-INTEL-35766523457 / Bayesian DM K=12 N=1999 — validated estimator (log BF 168-643) but absolute BF -10 to -15 nats on real TodoMVC; reused here with valid centering.
- Frontier 61 pooled TV/KDE/binned tunnel — complementary blind spots, 95% non-stationary attenuation; orthogonal pivot per director comparative reasoning.
- Codex 251 experiments, tunnel_flag true, director PIVOT cognitive_reset true, portfolio_assessment Gate0 0/3, physics IDLE.
- SPIDER_MASTER_PROMPT §15-22 (physics validity gates, strong nulls, identifiability, representation loss), SPIDER_ARCHITECTURE_RESEARCH2 §4-6 (packet, Codex, freeze, lane registry), AGENTS.md transmission discipline, POLICY.md director mandate, research/EXPERIMENT_PACKET.md mandatory fields.

