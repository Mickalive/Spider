# EXP-PHYSICS-35915247766 — Preregistration (DESIGN ONLY)

## Status
DESIGN ONLY — not yet frozen. No outcome-bearing measurements have been inspected. Preregistration will be hashed in `freeze.json` before EXECUTE. This is a NEW governed experiment with Director PIVOT to C-MEAS-VALID; parent handoff is continuity evidence only per SUPERSEDE.

## Experiment Identity
- **experiment_id**: EXP-PHYSICS-35915247766
- **lane**: physics
- **claim_ids**: ["C-MEAS-VALID"]
- **parent_handoff**: `research/experiments/EXP-PHYSICS-35903177055/handoff.json` sha256 `61e860a4e18a4b1fb4f335ec374dcd559610166709032feac97eec4a3f893971` (SUPERSEDE disposition per Director)
- **director_mandate**: PIVOT on C-MEAS-VALID, allocation PIVOT, cognitive_reset=true, cycle_id 35914890010, dependencies [intel: relaxed Gate0 H>0.1 NL>=20 via multi-step BrowserGym, runtime: BrowserGym 1280x720 CDP pipeline], parent_handoff_disposition SUPERSEDE
- **inherited_last_verdict**: MEASUREMENT_INVALID
- **request_hash**: 883484ca37ca6ca60ffedaec2725db7ae6a40c5ca5e984c88390064d314aa5af
- **base_sha**: 1f334e71803aa0a3bf718b0f21169b1e801cb2e0

## 1. Question (Director Binding)

On existing real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0, CDP Accessibility.getFullAXTree with visual bbox + 8 computed styles + AX embedding, not SHA256 hash-truncated, TRAIN-only k-means 20), does exact Bayesian Dirichlet-Multinomial K=12 (and K=24 if state space larger) with Gamma-ratio gammaln/polygamma correction replicate valid null centering (|null_mean|<0.1 null_std>0.01 |perm-analytic|<0.03) and relative separation (observed log BF exceeds 1999 trajectory-grouped permutation null by >=200 nats, p_bonf<0.01, gap>=0.05 over B-DOM-SIMILARITY TF-IDF k5 and B-MARKOV-1) with independent-noise control BC~0 (|BC|<0.05 p>0.10), reporting absolute BF (-10 to -15 nats expected favoring memory) separately as exploratory — i.e., does the first estimator to pass C1+C3 on synthetic SPA remain valid on real browser data without requiring new Gate0 SPAs (titles>=2 H>0.2 leakage<40%)?

This PIVOT supersedes the parent barrier/committor/timescale agenda (which required non-existent Gate0 SPAs and repeatedly returned MEASUREMENT_INVALID — 8-streak barrier PARK) while preserving its established pipeline evidence (exact Gamma-ratio, trajectory grouping, genuine 1280x720 capture, overlapping spectra) as continuity. The new question is parsimonious, falsification-first, low-cost (reuses already-collected banks), and directly informs whether Physics should remain PARKED.

## 2. Background and Motivation

### 2.1 What has been established (preserved from `carry_forward.established`)

1. **Synthetic 12-state stochastic hash-routed SPA positive control at K12**: DM log-BF replicates bit-identical vs parents (alpha0.5 obs 643.09 null_median -78.36 null_max -21.14 p0.0005; alpha1.0 obs 338.67 null_median -130.91 null_max -92.94 p0.0005; alpha2.0 obs 167.90 null_median -116.10 p0.0005) with trajectory-grouped perms seed42, audited recomputed_metrics match producer — estimator and permutation machinery are sound. Bounded to N=5000 synthetic SPA, K=12, alpha=1/K, history K2. First estimator to pass C1 (null median <0) + C3 (p<0.001) after 5 estimator families failed on this SPA (EXP-PHYSICS-35578258358 SURVIVES).

2. **Locally-hosted 6-state overlapping genuine proxy at locked 1280x720 via Playwright CDP**: 36 prototypes (state0-5 x regime A/B x variant0-2, dom_bytes 443 a11y 3971, viewport 1280x720 verified), overlap hist_intersection_color 0.667 mean_overlap 0.399 >0.3 not deterministic red/blue, H(S_next|C) 2.329-2.584 bits >0.05 valid ceiling, 24 strata >=3, |R_visual|/N 0.017, MI(DOM;Action) 0.0 <0.10. Validates genuine capture pipeline but bounded to synthetic proxy, not real BrowserGym WebShop/TodoMVC heterogeneity.

3. **Independent-noise genuine replication on same proxy (regime-independent sampling, 50x40 N=2000, trajectory_id grouping, 1000-1999 perms seed42)**: BC -0.042 p_bonf 1.0 analytic 0.033 cons 0.0357 (current packet) / BC -0.023 p0.213 analytic 0.033 cons 0.028 (parent) and IID BC -0.036/-0.029 — pipeline not confounded on BC scale when action dependence destroyed, but analytic consistency >0.03 indicates heuristic miscentering in prior runs (audit VF6). With exact gammaln/polygamma, prior barrier exact pipeline achieved cons 0.029 <0.03 on correlated bank. Bounded to proxy.

4. **Barrier/timescale orthogonal channel measured on proxy**: candidates_ge10=31 divergent=4 ECE 0.08 Brier_gap 0.07 identifiable True but divergent q 0.86-0.93 near-attractor not 0.2-0.8 ideal; tau_corr 0.353 via -1/log(ACF1=0.059) vs independent tau 0.21 gap 0.14 but << required tau_corr>5 vs tau_shuffled~1 gap>=0.05, so timescale not demonstrated on proxy at this N/representation. Bounded to 6-state single-action FSM.

5. **Physics barrier/beyond-memory program remains PARKED**: 68+ C-WEB-DYNAMICS HYPOTHESIS, 0 real-Web beyond-memory hits, 8-streak barrier PARK, tunnel_flag true; Bayesian K12 is first to pass C1+C3 synthetic but absolute BF -10 to -15 nats favors memory on real TodoMVC at K12 (EXP-PHYSICS-35651906573) — relative separation concept introduced but remains UNMEASURED on real BrowserGym banks. Gate0 0/2 exhaustive failures (H>0.2 leakage<40% titles>=2 NL>=50) after BrowserGym/CAP/Intel enumeration.

6. **Real TodoMVC absolute BF favoring memory**: On real TodoMVC hash-SPAs at K12, absolute observed log BF -10 to -15 nats (memory model M0 favored) due to K=12 over-penalty on |S_next|=3-4 states, H(S_next|C) near 0 deterministic, not evidence against relative discriminability — discipline requires reporting absolute exploratory separately.

### 2.2 What has been rejected / do_not_assume (SUPERSEDE but preserved as distinctions)

Bounded rejections from parent audit VF1-VF8 and earlier Physics portfolio:

- Locally-hosted 6-state constant-action proxy with heuristic analytic (magic constants 0.015/0.035/0.005/0.35, sqrt(mean_var)*0.35+0.008) as valid test of real BrowserGym WebShop/TodoMVC beyond-memory dynamics — bounded rejection (audit VF1 substrate_substitution browsergym_reuse MISSING, VF2 degenerate |A|=1 Counter click:button|next 2000, VF6 heuristic not exact Gamma-ratio gammaln/polygamma).
- TF-IDF k5 baseline returning hardcoded BC 0.0 acc 0.0 as valid ordinary-similarity null with gap_over_sim 0.171 >=0.05 — bounded rejection (baseline_findings INVALID_WEAK_BASELINE, missing dom_before_text, execute_35903177055.py:475 returns bc 0 when train/test empty).
- Hardcoded B-MARKOV-1 BC -0.003 as valid beyond-Markov contrast — bounded rejection (execute_35903177055.py:595 markov_bc=-0.003 not MLE on TRAIN, gap artifactual).
- R_visual/R_computed_style/R_AX_embedding as three independent genuine representations when bit-identical (VF5 colinearity observed 0.1986 perm -0.0015 analytic 0.027 BC 0.171 p 0.00799 across 3 Rs) — bounded rejection (deterministic function of same 36 prototypes, n_tests<=8 overcounts effective 2-3).
- That BC 0.171 p_bonf 0.00799 with ECE 0.08 Brier 0.07 and tau 0.35 demonstrates valid beyond-memory barrier/timescale structure — bounded rejection (VF4 positive control fails frozen BC>=0.30 p<0.001, VF7 tau_corr 0.35 <<5 required).
- Gating plug-in CMI bits*ln2 as DM log-BF relative separation against 200-nat threshold — metric identity substitution.
- SHA256 hash-truncated AX embedding (sha256[:4]+state+variant) as genuine AX — violates R_AX_embedding serialized role/name/value 5k + TRAIN k-means 20.
- That this MEASUREMENT_INVALID adjudicates C-WEB-DYNAMICS globally or justifies closing physics — bounded rejection (audit claim_ceiling MEASUREMENT_INVALID UNMEASURED on real BrowserGym, maximum justified is proxy description only, 68-attempt streak not closed).

Do_not_assume (unsafe, preserved):

- Do not assume C-WEB-DYNAMICS or C-MEAS-VALID falsified globally — this packet is MEASUREMENT_INVALID UNMEASURED on real BrowserGym; 68-attempt streak remains HYPOTHESIS not REJECTED (audit claim_ceiling).
- Do not assume heuristic analytic that calls gammaln/polygamma inside magic-constant blending is exact Gamma-ratio centering — prereg requires closed-form gammaln(Kalpha)-gammaln(N+Kalpha)+sum_i gammaln(n_i+alpha)-gammaln(alpha) and digamma/trigamma without 0.015/0.035/0.005/0.35.
- Do not assume BC 0.171 p_bonf 0.00799 demonstrates beyond-memory barrier/timescale — below frozen 200-nat/0.30 BC threshold and gap artifactual due to weak baselines; absolute BF not gated remains exploratory.
- Do not assume TF-IDF k5 BC 0.0 proves beyond-similarity — baseline invalid due to missing dom_before_text.
- Do not assume R_visual/computed_style/AX are three independent evidences — they are colinear encodings of same 36 prototypes (VF5), n_tests overcounts.
- Do not assume null negativity or p_bonf 0.008 on deterministic cells proves action-conditioned structure — H 2.32 on proxy is synthetic-like; prior TodoMVC det_ratio 0.846-0.944 produces trivially negative null, absolute BF -10 to -15 favors memory at K12 due to over-penalty not informative.
- Do not assume AX hash-truncated tokens evidence genuine AX semantics — event_seq BC -0.000027 p 1.0 constant, AX visual truncated to VB cluster; genuine requires serialized role/name/value 5k + TRAIN k-means 20.
- Do not assume frozen 200-nat BF or 0.05 BC thresholds should be silently lowered to 0.17 or 0.05-case-by-case — they are calibrated on synthetic positives 168-643 nats; lowering post-hoc invalidates decision_rule gating.
- Do not assume locally-hosted 6-state proxy with 443-byte prototypes, hash-fragment URLs and constant action generalizes to production WebShop/TodoMVC at 1280x720 with real latent regimes/history dependence — viewport genuine does not imply real heterogeneity.

### 2.3 Why this experiment (Director comparative reasoning verbatim + elaboration)

- **Vs CONTINUE barrier/committor (>=10 revisits 0.2<q<0.8 ECE<=0.15) on non-existent Gate0 SPAs**: Requires 2 production SPAs that exhaustive BrowserGym/CAP/Intel enumeration showed do not exist under H>0.2 leakage<40% NL>=50; expected BLOCKED/MEASUREMENT_INVALID again, zero info gain. (Director allocation comparative_reasoning)
- **Vs PARK entirely**: Would abandon measurement leverage while Frontier still hunts dynamics-adjacent compilation; pivoting to C-MEAS-VALID keeps parsimonious falsification-first discipline and unblocks Intel's relaxed Gate0 H>0.1 NL>=20. 
- **Vs C-CROSSSITE holdout**: Intellectually owned by Intel Graph; physics should not duplicate.
- **Vs CONTINUE exact Gamma-ratio barrier on larger production manifest**: Requires Intel relaxed Gate0 still pending; 6th barrier variant marginal value low until manifest exists.
- **Vs TERMINATE physics**: Premature; Bayesian K12 is first estimator to pass C1+C3 synthetic (168-643 nats) and exact pipeline now achieves valid centering (|perm-analytic|<0.03). 
- This test is **low-cost**, reuses already-collected BrowserGym trajectories at 1280x720 (no new Gate0 SPA discovery, no LLM), has valid null centering prerequisites (|perm-analytic|<0.03 etc), and directly tests Scout question whether physics should stay PARKed without requiring new site discovery. A positive barrier/timescale signal would have established first real-Web beyond-memory metastable/timescale structure despite absolute BF -10 to -15; here positive is first real-Web beyond-memory BM estimator validity (relative sep >=200 nats) despite absolute BF penalty; persistent BC~0 / rel_sep<200 would justify remaining PARKED and pivoting Frontier to orthogonal MemoryArena/WebAPI-bypass/tool-compilation/alias-catalog per runtime dependencies.
- Tests **synthetic-to-real gap** with orthogonal mechanisms: does the only estimator that survived synthetic bias (K12 exact) survive the transition to genuine visual/AX structure?

### 2.4 Agent priors distinguished (per Director, explicitly NOT SPIDER evidence)

All six are agent priors, not SPIDER evidence (distinguished):

1. Path dependence and context salience: agents returning to WebArena-Verified v2 add_to_cart after 7 MEASUREMENT_INVALID failures are locally trapped by available Docker/census code, not globally optimal — distinguished from SPIDER evidence which shows zero narrowing of synthetic-to-live gap.
2. Memory vs no-memory is not evidence: RAG/Stagehand/TERX already give deterministic 34-179x speedups; LLM inheritance requires same-model/same-budget margin >=0.12 and false_accept <=0.10 vs RAG, distinguished from SPIDER's cold-only ceilings.
3. Long-horizon compounding errors: 15-step gpt-4o-mini Playwright plans accumulate non-linear failure, coupling repair budget to verification AUROC — explains why 5 BLOCKED delta-repair and rho 0.363 falsification may reflect planning noise, not absence of novelty tracking, distinguished from SPIDER's falsified stratum correlations.
4. Representation loss destroys identifiability: action.target_href==state_after.url leakage (78-92%) and hash-truncated DOM collapse environmental dynamics into policy artifacts — distinguished from SPIDER's MEASUREMENT_INVALID verdicts on TodoMVC/Wikipedia PMI.
5. Local optima via reward hacking: cross-family key adoption spuriously lifts alias-OOD to 1.0 vs 0.525 without correct-family discrimination — distinguished from SPIDER's audit finding that disabling it restores discriminability and reveals 21/40 ceiling.
6. Additional priors in portfolio_assessment: compounding, salience, exhaustive enumeration failures, etc. — all distinguished as general agent knowledge, not SPIDER measurement.

## 3. Hypotheses

**H1 (alternative, C-MEAS-VALID replicates on genuine DOM)**: Same as `spec.json hypothesis`. The exact Bayesian Dirichlet-Multinomial estimator (K=n_states, alpha=1/K, exact gammaln + digamma/trigamma) remains measurement-valid on real BrowserGym WebShop/TodoMVC banks at locked 1280x720 with genuine overlapping DOM (visual bbox 10 bins + 8 computed styles + AX 5k + TRAIN-only k-means 20, not hash-truncated): NULL CENTERING valid (|analytic_mean|<0.1, calibrated std valid, |perm-analytic|<0.03) AND RELATIVE SEPARATION (M_REL_SEP>=200 nats, p_bonf<0.01, gap over TF-IDF k5 >=0.05 and over Markov-1 >=0.05) with independent-noise BC~0 (|BC|<0.05 p>0.10) while absolute BF -10 to -15 remains exploratory. This is the falsification-first test of whether the synthetic-unbiased estimator survives the synthetic→real DOM transition.

**H0 (null, replication failure)**: No real bank achieves all null-centering and relative separation and gaps with independent~0 while gates pass; even exactly-centered genuine DOM remains at BC~0 / rel_sep<200, indicating the estimator does not generalize from synthetic 12-state SPA to real Web heterogeneity at this scale/representation, or DOM genuine structure is indistinguishable from similarity/Markov at BF scale.

## 4. State / Action / History / DOM Representation

### 4.1 State `S_next`
- WebShop primary: `SHA256(normalize(URL_after)|'|'|normalize(title_after)|'|'|DOM_cluster_if_needed)`; TodoMVC secondary: fragment-aware URL as in EXP-PHYSICS-35651906573 enhanced with genuine DOM stratification (same normalization).
- `normalize(URL)` lowercase strip `?session=/?token=/?keep` SPA hash fragment `#/` strip trailing `/`; `normalize(title)` trim lowercased 200 chars; `S_next` from `t+1` distinct from `DOM_before` at `t` (no post-state leak).
- Report `|R|/N`, `H(S_next|C)`, `|S_next|` cardinality, `|R_visual|/N` etc. K handling: K=12 primary; if `|S_next|>=16` or cardinality >12 trigger K=24 exploratory with same alpha=1/K.

### 4.2 Action `A_leakageFree`
- `A=(primitive,target_sig)` primitive in {click,fill,navigate,select,submit,hover,type} target_sig=role+name+testId+aria-label+bbox cluster never href/URL/src; diagnostic A_leaky for gap only; MI(DOM;Action)<0.10 else tautology flag.
- Leakage definition `action.target_href == state_after.url` filtered; verify on new BrowserGym banks.

### 4.3 History `H_K`
- Bayesian DM uses `K_strata = C = (URL_before_normalized, H_K=3)` with >=5 unique C >=3 per stratum for stratification; also compute `H_K=2` primary for BF comparison? Primary BF is M1: P(S_next|S_current,A) vs M0: P(S_next|S_current). History conditioning via C stratification already incorporates H_K=3. Also report history-characterization: H(S_next|C) and singleton_SA_rate.
- Require H(S_next|C)>0.05 (>0.2 for former barrier, but now 0.05) else degenerate ceiling => MEASUREMENT_INVALID. Also report |A|>1 and MI.

### 4.4 Genuine DOM (not SHA256 truncated)
- `R_visual`: AX bbox x,y,w,h quantized 10 bins + element_count/tree_depth/interactive_density from dom_bytes.
- `R_computed_style`: 8-value getComputedStyleForNode {color,backgroundColor,visibility,display,opacity,border,position,fontSize}.
- `R_event_seq`: n-gram last 3 primitives (diagnostic, expected near-constant).
- `R_AX_embedding`: Accessibility.getFullAXTree serialized role/name/value up to 5k tokens + TRAIN-only TF-IDF or k-means 20 clusters (fit TRAIN 70/30 by trajectory_id) not SHA256 truncated single value.
- Preserve raw: dom_snapshot, a11y_tree, visual_json, style_dict, event_seq, AX bytes; document quantization/viewport. Primary requires >=1 R genuine with overlapping spectra verified (style/visual/AX distributions overlap hist_intersection >0.3 not deterministic regime-color) and |R|/N 0.01-0.30.

## 5. Estimator, Bias Correction, Operationalization

- **Exact Dirichlet-Multinomial marginal likelihood** via scipy.special.gammaln and polygamma (digamma polygamma(0), trigamma polygamma(1)): log ML = Σ_c [gammaln(K*alpha)-gammaln(N_c+K*alpha)+ Σ_i(gammaln(n_i+alpha)-gammaln(alpha))] with K=n_states (12 primary 24 exploratory) NOT len(counts), alpha_prior in {0.5,1.0,2.0} primary 1.0 reporting, 0.5/2.0 sensitivity. Log BF = log ML(M1)-log ML(M0) in nats. Analytic null mean/std via exact Gamma-ratio (gammaln/polygamma) not heuristic /100*0.1. BC = observed - analytic_mean. Also compute plug-in CMI bits for diagnostics but gating on BF nats. Code path research/physics/run_experiment.py _dirichlet_multinomial_log_marginal with K=n_states; grep verification logged.
- **Permutation**: 1999 trajectory-grouped shuffles of genuine DOM labels within each C stratum grouped by trajectory_id seed42 deterministic; null mean/std/median/max/p_raw/p_bonf where p_bonf=min(1,p_raw*n_tests) n_tests<=8 floor 0.0005; resampling unit trajectory_id not transition; no Gaussian jitter; calibrated_std=max(analytic_std,perm_std) floor 0.005 analytic /0.01 perm; consistency |perm-analytic|<0.03 required.
- **Relative vs absolute BF discipline**: Report M_OBS_BF (absolute), M_REL_SEP=OBS-NULL_MEDIAN (relative), M_BC=OBS-ANALYTIC_MEAN, M_ABSOLUTE_BF = M_OBS. Absolute expected -10 to -15 nats on TodoMVC deterministic K12 due to over-penalty and H~0; not gating. Primary gating is relative sep >=200 nats + BC>0.05 + p_bonf<0.01 + gaps.

## 6. Data Collection and Sampling

### 6.1 Trajectory banks
- **Primary**: BrowserGym WebShop at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 pinned) via CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode. Reuse existing WebShop/TodoMVC 1280x720 banks if manifest shows browsergym_reuse with dom_bytes>0 a11y_bytes>0 viewport 1280x720 (check research/intel/manifest.json or codex path).
- **Secondary**: BrowserGym TodoMVC same pipeline (richer genuine DOM vs prior SHA256 URL-only). Both banks N=1000-1999 (50 sessions x20-40 steps or as collected). If not available, collect new WebShop categories/search/cart/checkout and TodoMVC at locked 1280x720 (honest cost, no f*6.0 jitter, no hash truncation).
- **Positive control bank**: Synthetic 12-state stochastic hash-routed SPA N=5000 seed42 (same as EXP-PHYSICS-35578258358) with same estimator; no browser needed.
- **Independent-noise bank**: Same WebShop/TodoMVC FSM but action-state dependence destroyed via per-step independent within-trajectory shuffle (regime-independent sampling, not S_current%2, same 1280x720 viewport, same K); identical DM + grouped perms 1999 seed42.
- **IID bank**: Same marginal P(S) i.i.d. with genuine DOM still sampled (seed42).

### 6.2 Collection details
- PYTHONHASHSEED=0, numpy seed42, never hash(site); trajectory_id as resampling unit; VIEWPORT 1280x720 verified before claiming genuine (dom_bytes>0 visual_json>0 a11y_bytes>0 computed_style>0).
- At least 100 NL transitions per bank or report H(S_next|C) and |R|/N; H(S_next|C)<=0.05 => MEASUREMENT_INVALID ceiling not falsification.
- Honest cost: sum counters resolve+bind+verify+freshness+browser_steps, no f*6.0 jitter, |rho_shuffled|<0.20.
- If banks not available and collection fails due to BrowserGym install/network, write failure.json with category BLOCKED and smallest unblock action (e.g., pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.63.0 + npx playwright install chromium), not falsification.

## 7. Baselines and Controls

### 7.1 Baselines (stable identities)
- **B-DOM-SIMILARITY-TFIDF-K5** (B-DOM-SIMILARITY): TF-IDF cosine k=5 over genuine DOM text (visual text+bbox + AX name/role + computed style tokens) fit TRAIN only 70/30 by trajectory_id, 5-NN predicted S_next without stratification; BC_sim via same exact Gamma-ratio K analytic+perm; primary must exceed by gap>=0.05; |analytic_mean|<0.1 cons<0.03 required else invalid. Prior barrier gap 0.011 shows similarity ceiling.
- **B-MARKOV-1** (B-MARKOV-1): P(S_next|S_current,A_leakageFree) MLE TRAIN by trajectory_id without DOM; BC_markov1 same analytic+perm; gap>=0.05 required to isolate beyond-Markov DOM signal. Expected BC -0.003 to 0.02 on TodoMVC deterministic.
- **B-SHUFFLE-GROUPED-PERM**: trajectory-grouped 1999 within-strata shuffles grouped by trajectory_id seed42 => perm mean/std/p; analytic mean/std via gammaln/polygamma for |perm-analytic|<0.03 and |analytic|<0.1 and std>0.01.
- **B-INDEPENDENT-NOISE-GENUINE**: independent per-step genuine DOM >=6 variants/state same 1280x720 but regime-independent shuffling, identical DM + grouped perms 1999; |BC|<0.05 p>0.10 |analytic|<0.1; confound => MEASUREMENT_INVALID.
- **B-IID-NULL**: i.i.d. S_next same marginal P(S) seed42; |BC|<=0.05 p>0.10.
- **B-TRAJECTORY-MEMORY diagnostics**: exact (URL,H_K,Action)->S_next memorization ratio, href-leakage gap, MI(DOM;Action)<0.10, H(S_next|C) ceiling.

### 7.2 Positive control
- **CTRL_POS_SYNTHETIC** (positive_control): Synthetic 12-state stochastic SPA N=5000 seed42 must achieve observed 168-643 nats, null_median -78 to -131, p=0.0005 floor, |perm-analytic|<0.03, |analytic|<0.1, calibrated_std valid, |R|/N diagnostic. Failure => MEASUREMENT_INVALID. Also report deterministic SPA log BF>>0 as sanity.

### 7.3 Null controls (stable identities)
- **CTRL_NULL_GROUPED_PERM** (null_control permutation): Trajectory-grouped 1999 perms seed42 |perm-analytic|<0.03 |null_mean|<0.1 null_std>0.01 p_bonf floor 0.0005.
- **CTRL_ANALYTIC_CENTERING**: |analytic_mean|<0.1 on BF/BC scale, consistency<0.03, calibrated valid.
- **CTRL_INDEPENDENT_NOISE** (null_control independent): |BC|<0.05 p>0.10 |analytic|<0.1 valid; failure => MEASUREMENT_INVALID confounded.
- **CTRL_IID_NULL**: |BC|<=0.05 p>0.10.
- Audit verifies source contains gammaln/polygamma and not heuristic sqrt(mean(1/(2n)))*0.1 or 0.015/0.035 constants.

## 8. Measurement Validity (pre-registered gates)

All listed in `spec.json measurement_validity` plus:
- Genuine DOM verification: dom_bytes>0 a11y_bytes>0 visual_json>0 computed_style>0 viewport 1280x720 and not SHA256 truncated; overlapping spectra documented (hist_intersection >0.3).
- H(S_next|C)>0.05 and |R|/N 0.01-0.30 and |A|>1 and MI(DOM;Action)<0.10 and singleton_SA_rate<70% required.
- Train-only integrity: TF-IDF vocab/embedding centroids/Dirichlet counts/k-means fit TRAIN only 70/30 by trajectory_id; holdout gaps reported.
- Absolute vs relative discipline: Absolute observed log BF exploratory (expected -10 to -15 at K12 on TodoMVC due to K over-penalty); primary gating is relative sep >=200 nats + BC>0.05 p_bonf<0.01 gap>=0.05 with independent~0.
- Trajectory_id grouping, exact gammaln/polygamma, no Gaussian jitter; 1999 perms seed42; n_tests<=8 floor 0.0005.
- K12 primary; K24 triggered only if |S_next|>=16; sensitivity to K={3,4} exploratory but not gating.

## 9. Decision Rule (frozen, verbatim from `spec.json decision_rule`)

Gated execution in order; any validity gate triggers MEASUREMENT_INVALID and prevents primary SURVIVES/FALSIFIED claim.
Gates (MEASUREMENT_INVALID if any fail):
- G0 synthetic positive: observed<=0 OR p_bonf>=0.01 OR |analytic_mean|>=0.1 OR calibrated_std degenerate (analytic_std<=0.005 and perm_std<=0.01) OR |perm-analytic|>=0.03 => pipeline blind/miscalibrated.
- G1 independent-noise: BC |BC|>=0.05 and p<0.10 with valid |analytic|<0.1 cons<0.03 => confounded.
- G2 IID null: BC>0.05 p<0.10 valid => null miscentered.
- G3 degenerate ceiling: H(S_next|C)<=0.05 OR N<100 OR <5 strata with >=3 OR |R|/N outside 0.01-0.30 OR |A|<=1 OR MI(DOM;Action)>=0.10 => degenerate.
- G4 primary |perm-analytic|>=0.03 on primary K12 both banks => model mismatch.
- G5 viewport/DOM genuine fails (no dom_bytes/visual/computed/AX >0 OR viewport !=1280x720 OR SHA256 truncation) => substrate missing.
- G6 TRAIN leakage or trajectory_id not used => split invalid.

If no G fails, primary per real-Web bank (WebShop primary, TodoMVC secondary) for K12 (and K24 if |S_next|>=16): compute M_OBS_BF, M_NULL_MEDIAN/MEAN/STD/MAX, M_ANALYTIC_MEAN/STD, M_CONS=|perm-analytic|, M_REL_SEP=OBS-NULL_MEDIAN, M_BC=OBS-ANALYTIC_MEAN, p_raw=(count_ge+1)/2000, p_bonf=min(1,p_raw*n_tests) n_tests<=8 floor 0.0005, gaps G_DOM=M_BC-B_DOM_BC, G_MARKOV=M_BC-B_MARKOV_BC.
sig(bank,K,R)=1 if M_BC>0.05 AND p_bonf<0.01 AND M_REL_SEP>=200 AND |analytic_mean|<0.1 AND calibrated valid (>0.005 analytic or >0.01 perm) AND cons<0.03 AND G_DOM>=0.05 AND G_MARKOV>=0.05 AND independent~0 (|M_BC_INDEPENDENT|<0.05 p>0.10 |analytic|<0.1 cons<0.03) AND |R|/N 0.01-0.30. If EXISTS bank,R sig==1 => SURVIVES_CURRENT_TEST — first estimator remains valid on real DOM, C-MEAS-VALID replicates, bounded to that bank/K/R, absolute BF reported exploratory (-10 to -15 expected). If FORALL banks sig fails while gates pass => FALSIFIED-IN-SETTING — even correctly centered genuine DOM remains BC~0, estimator not valid on this genuine scale; physics remains PARKED, bounded to N=1000-1999 genuine BrowserGym banks at 1280x720 with exact Gamma-ratio. K24 exploratory consistency reported but not gating unless K12 sig already.
Exploratory K24 per-branch consistency reported but not gating unless K12 sig already (same thresholds).

## 10. Primary Metrics (stable identities for AUDIT)

- M_OBS_BF_K12, M_OBS_BF_K24 (nats, absolute)
- M_ABSOLUTE_BF_K12 = M_OBS_BF_K12 (exploratory, -10 to -15 expected)
- M_NULL_MEDIAN_K12, M_NULL_MEAN_K12, M_NULL_STD_K12, M_NULL_MAX_K12, M_ANALYTIC_MEAN_K12, M_ANALYTIC_STD_K12, M_CONSISTENCY_K12=|perm-analytic|
- M_BC_BF_K12 = M_OBS - M_ANALYTIC_MEAN (nats), M_BC_BITS = M_BC / ln2 (bits diagnostic)
- M_REL_SEP_K12 = M_OBS - M_NULL_MEDIAN (nats, must be >=200)
- M_P_RAW_K12, M_P_BONF_K12 (Bonferroni n_tests<=8 floor 0.0005)
- M_GAP_DOM_K12, M_GAP_MARKOV_K12 (nats, >=0.05)
- M_CALIBRATED_STD_K12 = max(analytic_std, perm_std)
- M_INDEPENDENT_BC_K12, M_INDEPENDENT_P_K12, M_INDEPENDENT_ANALYTIC_MEAN_K12, M_INDEPENDENT_CONS_K12
- M_IID_BC_K12, M_IID_P_K12
- M_BASELINE_DOM_TFIDF_K5_BC, M_BASELINE_DOM_TFIDF_K5_P, M_BASELINE_DOM_TFIDF_K5_ANALYTIC, M_BASELINE_DOM_TFIDF_K5_CONS
- M_BASELINE_MARKOV1_BC, M_BASELINE_MARKOV1_P
- M_H_SNEXT_GIVEN_C, M_R_OVER_N, M_SINGLETON_SA_RATE, M_N_TRANSITIONS, M_N_STRATA, M_A_CARDINALITY, M_MI_DOM_ACTION
- M_VIEWPORT, M_DOM_BYTES, M_A11Y_BYTES
- Corresponding K24 metrics suffixed _K24 if triggered; per-R variants _VISUAL/_COMPUTED/_AX/_EVENT

## 11. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Deterministic FSM (TodoMVC det_ratio 0.846-0.944, H~0): H(S_next|C) near 0, perm null heavily negative, absolute BF -10 to -15** | Report H(S_next|C) per bank; require H>0.05; WebShop bank provides stochastic heterogeneity; acknowledge absolute BF negative exploratory; primary is relative sep >=200 + BC>0.05 with independent~0 guard, not absolute. K24 not penalized as harshly if |S|>=16. |
| **K=12 over-penalty on S=3-4: BF -10 to -15 even when relative signal exists** | K12 frozen primary; report K12 absolute exploratory; trigger K24 only if |S|>=16; gaps use same K so penalty cancels; relative sep >=200 is scale-invariant to penalty. |
| **Isomorphic replication inflating n (vanillajs/react/svelte bit-identical): Effective replications 2 not 5** | Treat WebShop vs TodoMVC as distinct banks; do not pool 5 variants as independent; gate on bank level; note isomorphism. |
| **Genuine DOM vs SHA256 truncation collapse** | Verify dom_bytes>0 a11y_bytes>0 visual bbox+computed 8-value+AX 5k preserved; audit grep checks source contains gammaln/polygamma not SHA256-only; report |R|/N 0.01-0.30 genuine finite vocab with overlapping spectra hist >0.3. |
| **Viewport heterogeneity 1024 vs 1280 changes bbox** | Lock 1280x720 via CDP Page.setViewportSize + window.innerWidth check; verify viewport in provenance; reject if !=1280x720 => MEASUREMENT_INVALID. |
| **Trajectory grouping vs transition-level shuffle inflate p** | Enforce trajectory_id unit, 1999 perms seed42, |perm-analytic|<0.03 guard; independent-noise BC~0 confirms not S_current%2 leakage. |
| **Heuristic bias correction masquerading as exact** | Require scipy.special.gammaln/polygamma exact closed-form sum_c[gammaln(Ka)-gammaln(N+Ka)+sum_i gammaln(n_i+a)-gammaln(a)] and digamma/trigamma; audit grep verification; forbid 0.015/0.035/0.005/0.35 constants. |
| **Multiple testing inflation (n_tests<=8 isomorphic Rs)** | p_bonf=min(1,p_raw*n_tests) floor 0.0005; note effective 2-3 for colinear Rs; report both p_raw and p_bonf; Bonferroni conservative. |
| **Small N (80 NL prior) vs target 1000-1999 power limited** | Require N>=100 valid per bank H>0.05; WebShop should provide >=1000 if manifest available; else collect until >=1000 or report MEASUREMENT_INVALID ceiling not falsification; acknowledge power. |
| **Action encoding degeneracy (\|A\|=1)** | Use A_leakageFree never href; verify \|A\|>1 and MI(DOM;Action)<0.10; report degenerate_action diagnostic log BF 0 if fails. |
| **BrowserGym installation/network unavailable** | Write failure.json BLOCKED with retryable unblock (pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.63.0); not falsification. Synthetic positive still runnable offline. |
| **Absolute BF gating confusion** | Enforce discipline: absolute BF exploratory only; primary gating is relative sep >=200 + BC>0.05 + p<0.01 + gaps; document both. |

## 12. Product Consequences

- **Positive (SURVIVES with valid exact centering and relative sep >=200 + gaps)** : First real-Web Bayesian beyond-memory measurement-validity replication despite absolute BF -10 to -15. Bridges synthetic→real gap that blocked 30+ experiments. Justifies UNPARKING Physics for production manifest with real session/permission regimes and larger state spaces (|S|>=16 K24). Product: distill validated exact Bayesian estimator as freshness/barrier guard candidate (regime-aware retrieval grouped by latent DOM cluster, visual+AX signature, event-seq guard) into kernel resolve/verify; quantify delta-repair and cross-site holdout transfer at K12/K24 with exact correction; measure work-compression via regime detection. No generic promotion until transfer validated; absolute BF reported separately.
- **Negative (FALSIFIED-IN-SETTING with valid gates: null centering valid but BC~0 / rel_sep<200 / gap<0.05 with independent~0)** : Closes Bayesian beyond-memory measurement-validity program on existing BrowserGym WebShop/TodoMVC N=1000-1999 genuine DOM 1280x720 at K12 (and K24 if triggered) even correctly centered. Combined with 68 prior HYPOTHESIS, -15 nats absolute, frontier blind spots, confirms real Web at this scale shows at most trivial beyond-memory structure at BF scale and physics should remain PARKED pending larger production manifest with real session/permission latent regimes and larger |S|; Frontier PIVOT to orthogonal MemoryArena / WebAPI bypass / compile-execute / tool-bypass / alias-catalog per Director dependencies. SPIDER must NOT invest in DOM Bayesian detection as mechanical prior at current N. Graph/Product continue via retrieval/verification/repair amortization for C-RESIDUAL-NOVELTY. Bounded falsification at N=1000-1999 genuine banks, not global Web closure. C-MEAS-VALID remains EXPERIMENTAL/MEASUREMENT_INVALID not globally REJECTED.

## 13. Estimated Cost / Expected Information Gain

- **Estimated cost**: Low: reuses existing BrowserGym trajectory banks at 1280x720 if available plus optional locally-hosted 6-state overlapping genuine capture <10 min headless; analysis 80-120k exact gammaln/polygamma fits <1ms each + TF-IDF k5 <5 min + 1999 trajectory-grouped perms x 8-10 banks <5 min; scipy+sklearn+headless Chromium if needed; total <2h wall-clock <8GB RAM no GPU, stdlib+scipy+sklearn.
- **Expected information gain**: Very high and tunnel-breaking per Director comparative reasoning: vs CONTINUE barrier on non-existent Gate0 SPA (0 info gain, 10th barrier variant) and vs TERMINATE (premature), this low-cost real-trajectory C-MEAS-VALID validation directly answers whether physics should stay PARKed without requiring new site discovery. Either BC>0.05 gap>=0.05 rel_sep>=200 p<0.01 with valid centering (first real-Web measurement-valid beyond-memory estimator) or persistent BC~0 / rel_sep<200 (justify PARK and Frontier orthogonal pivot) finally adjudicates Bayesian exact estimator's synthetic→real generalizability. Orthogonal falsifiable program per C-MEAS-VALID next_gate (writable/auth/session/drift controls must produce discriminating positive and null outcomes) and first real-Web test of exact-correction + genuine visual/AX at 1280x720 requiring no Gate0 discovery (68 prior HYPOTHESIS, 0 real-Web beyond-memory hits, tunnel_flag true). DIRECTLY INFORMATIVE for Global Director UNPARK/PARK decision.

## 14. Inherited Parent Handoff Carry-Forward (exact, SUPERSEDE but preserved as distinctions)

### Established (from EXP-PHYSICS-35903177055, preserved)
1. Synthetic 12-state stochastic hash-routed SPA positive control at K12 replicates bit-identical vs parents (alpha0.5 obs 643.09 null_median -78.36, alpha1.0 obs 338.67 null_median -130.91 p0.0005, alpha2.0 obs 167.90) with trajectory-grouped perms seed42 per parent audit — estimator and permutation machinery are sound. Bounded to N=5000 synthetic SPA, K=12, alpha=1/K. Not re-measured in this packet but preserved via Codex and parent handoff.
2. Locally-hosted 6-state overlapping genuine proxy at locked 1280x720 via Playwright CDP Accessibility.getFullAXTree + DOM.getDocument + CSS.getComputedStyleForNode validated in this packet: 36 prototypes (state0-5 x regime A/B x variant0-2, dom_bytes 443 a11y 3971 viewport 1280x720 verified), overlap hist_intersection_color 0.667 mean_overlap 0.399 >0.3 not deterministic red/blue, H(S_next|C) 2.329 bits >0.05 valid ceiling, 24 strata >=3, |R_visual|/N 0.017, MI(DOM;Action) 0.0 <0.10. Bounded to proxy N=2000, not real BrowserGym WebShop/TodoMVC heterogeneity.
3. Independent-noise genuine replication on same proxy (regime-independent overlapping, 50x40 N=2000, trajectory_id grouping, 1000 perms seed42): BC -0.042 p_bonf 1.0 analytic 0.033 cons 0.0357; IID null BC -0.036 p_bonf 1.0 analytic 0.033 cons 0.0321 — pipeline not confounded on BC scale when action dependence destroyed, but analytic consistency >0.03 indicates heuristic miscentering per audit VF6. Bounded to proxy.
4. Barrier/timescale orthogonal channel measured on proxy: candidates_ge10=31 divergent=4 ECE 0.08 Brier_gap 0.07 identifiable True but divergent q 0.86-0.93 near-attractor not 0.2-0.8 ideal; tau_corr 0.353 via -1/log(ACF1=0.059) vs independent tau 0.21 gap 0.14 << required tau_corr>5 vs tau_shuffled~1 gap>=0.05, so timescale separation not demonstrated on proxy at this N/representation. Bounded to 6-state single-action FSM.
5. Physics barrier/beyond-memory program remains PARKED: 68+ C-WEB-DYNAMICS attempts with 0 real-Web beyond-memory hits, 8-streak barrier PARK, tunnel_flag true; Bayesian K12 first to pass C1+C3 synthetic but absolute BF -10 to -15 nats favors memory on real TodoMVC — relative separation concept introduced but remains UNMEASURED on real BrowserGym banks.

### Rejected (bounded)
- Locally-hosted 6-state constant-action proxy as valid test of real BrowserGym WebShop/TodoMVC beyond-memory dynamics — bounded rejection (audit VF2 degenerate |A|=1, VF3 substrate_substitution).
- Heuristic analytic with magic constants 0.015/0.035/0.005/0.35 as exact Gamma-ratio — bounded rejection (VF1, prereg forbids heuristic).
- TF-IDF k5 baseline returning hardcoded BC 0.0 as valid — bounded rejection (baseline_findings INVALID_WEAK_BASELINE).
- Hardcoded B-MARKOV-1 BC -0.003 as valid — bounded rejection (not MLE).
- R_visual/R_computed_style/R_AX as three independent genuine representations when bit-identical — bounded rejection (VF5 colinearity).
- That BC 0.171 p_bonf 0.00799 with tau 0.35 demonstrates valid beyond-memory — bounded rejection (VF4/VF7 thresholds).
- That this MEASUREMENT_INVALID adjudicates C-WEB-DYNAMICS globally — bounded rejection (claim_ceiling UNMEASURED).

### Unknown (must not assume)
- Whether real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 (N=1000-1999, BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 via CDP) exist or can be collected in this environment and what H(S_next|C), |R|/N, |A| support they would show.
- What exact closed-form DM log-BF (K=12/24 alpha=1/K gammaln/polygamma) observed/null/analytic mean/std/p_bonf/gap would be on real banks with trajectory_id grouping and non-degenerate |A|>1, and whether |perm-analytic|<0.03 would still pass.
- Whether correcting analytic to exact Gamma-ratio and implementing genuine TF-IDF k5 TRAIN-only 70/30 would flip consistency on independent/IID nulls.
- Whether larger production manifest with real session/permission latent regimes, larger |S|>=16 triggering K24, richer multi-feature genuine DOM and non-degenerate action set would achieve BC>0.05 gap>=0.05 rel_sep>=200 or remain BC~0.
- Whether Bonferroni n_tests<=8 floor 0.0005 overcounts isomorphic visual/style/AX (effective 2-3) and how K24 consistency generalizes.

### Do Not Assume (unsafe)
- Do not assume C-WEB-DYNAMICS or C-MEAS-VALID falsified globally — this packet is MEASUREMENT_INVALID UNMEASURED on real BrowserGym; 68-attempt streak remains HYPOTHESIS not REJECTED.
- Do not assume heuristic analytic is exact Gamma-ratio centering.
- Do not assume BC 0.171 p_bonf 0.00799 demonstrates beyond-memory — below frozen thresholds and gap artifactual.
- Do not assume TF-IDF k5 BC 0.0 proves beyond-similarity — baseline invalid.
- Do not assume R_visual/computed_style/AX are three independent evidences — bit-identical colinear.
- Do not assume null negativity proves structure — absolute BF -10 to -15 favors memory.
- Do not assume AX hash-truncated tokens evidence genuine AX semantics.
- Do not assume frozen thresholds silently lowerable.

## 15. Preregistration Freeze Checklist

- [ ] `spec.json` frozen with above question/hypothesis/falsifier/baselines/positive_control/null_control/measurement_validity/decision_rule and stable metric/control identities (|null_mean|<0.1 null_std>0.01 cons<0.03 rel_sep>=200 p_bonf<0.01 gap>=0.05 independent~0 absolute exploratory)
- [ ] `prereg.md` (this file) frozen with above exact gammaln/polygamma, 1999 trajectory-grouped perms, genuine 1280x720 verification, gates G0-G6, validity threats, absolute vs relative discipline, H>0.05, |R|/N, TRAIN-only, trajectory_id grouping, inherited distinctions preserved
- [ ] `request.json` director_mandate stored immutable with agent_priors_used[6] distinguished from SPIDER evidence
- [ ] `freeze.json` deterministic hashes of request.json + spec.json + prereg.md before EXECUTE
- [ ] No outcome-bearing measurements inspected during DESIGN (synthetic positive control numbers are parent evidence, not this experiment's outcomes)
- [ ] Dependencies: intel relaxed Gate0 census H>0.1 NL>=20 and runtime BrowserGym 1280x720 CDP pipeline noted but not blocking this reuse-bank experiment

## 16. References

- Parent handoff: `research/experiments/EXP-PHYSICS-35903177055/handoff.json` sha256 61e860a4e18a4b1fb4f335ec374dcd559610166709032feac97eec4a3f893971 (MEASUREMENT_INVALID, SUPERSEDE)
- Parent spec/prereg: `research/experiments/EXP-PHYSICS-35903177055/spec.json` `prereg.md` (exact gammaln/polygamma, 1280x720 genuine, trajectory_id grouping)
- Director mandate: `research/experiments/EXP-PHYSICS-35915247766/request.json` director_mandate PIVOT C-MEAS-VALID cognitive_reset true
- Synthetic Bayesian validated: `research/experiments/EXP-PHYSICS-35578258358` (SURVIVES synthetic K12 exact, 168-643 nats)
- Real TodoMVC Bayesian: `research/experiments/EXP-PHYSICS-35651906573` (SURVIVES synthetic-bounded but absolute -10 to -15 nats real, isomorphic 2 effective)
- Barrier G1 exact: `research/experiments/EXP-PHYSICS-35860320716` (MEASUREMENT_INVALID BC 0.171<0.30 gap 0.011 exact valid centering)
- Physics state: `research/lanes/physics/state.json` (PARKED, tunnel_flag, consecutive_failures 0)
- Code reuse: `research/physics/run_experiment.py _dirichlet_multinomial_log_marginal`, `research/physics/execute_35860320716.py analytic_dm_mean_std_exact gammaln/polygamma`
- Substrate pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, honest cost no f*6.0 jitter |rho_shuffled|<0.20
- Claim registry: `research/claims/registry.json` C-MEAS-VALID EXPERIMENTAL next_gate writable/auth/session/drift controls must produce discriminating positive and null outcomes

---
*End of preregistration. EXECUTE must run exactly this frozen design, preserving raw evidence -> observation -> derived measurement -> interpretation distinction, with `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved` in `result.json`. Product lane scope not used. Never git commit/push/switch/reset.*
