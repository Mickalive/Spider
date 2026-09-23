# EXP-PHYSICS-35903177055 — Preregistration (DESIGN ONLY)

## Status
DESIGN ONLY — not yet frozen. No outcome-bearing measurements have been inspected. Preregistration will be hashed in `freeze.json` before EXECUTE.

## Experiment Identity
- **experiment_id**: EXP-PHYSICS-35903177055
- **lane**: physics
- **claim_ids**: ["C-WEB-DYNAMICS"]
- **parent_handoff**: `research/experiments/EXP-PHYSICS-35892828492/handoff.json` sha256 `877357202c2ff798e2292e5e2b2c73d0e03ce37890bfd8f3d685ae819004e6c8` (SUPERSEDE disposition per Director)
- **director_mandate**: PIVOT on C-WEB-DYNAMICS, allocation PIVOT, cognitive_reset=true, cycle_id 35902787476, dependencies [runtime], parent_handoff_disposition SUPERSEDE
- **inherited_last_verdict**: MEASUREMENT_INVALID (synthetic 12-state positive replication-exact but webshop CMI treated as BF, heuristic analytic with magic constants, |A|=1 degeneracy, SHA256 hash-truncated AX, regime confound — audit VF1-VF9 UNMEASURED on real BrowserGym)
- **request_hash**: 2b4827d4fe19c61d79e21f85ee80642eb0648d706e6a5a73e6037d6338055dff

## 1. Question (Director Binding)

On existing BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0, CDP Accessibility.getFullAXTree visual bbox + 8 computed styles + AX embedding, not SHA256 hash-truncated, TRAIN-only k-means 20), with exact Bayesian Dirichlet-Multinomial K=12/24 Gamma-ratio correction (scipy gammaln/polygamma, trajectory-grouped permutation N=1000-1999 seed 42, |perm-analytic|<0.03, |null_mean|<0.1, null_std>0.01), does barrier/committor (>=10 revisits to same canonical state URL+DOM_cluster+H_K=3 with divergent futures 0.2<q<0.8, ECE<=0.15, Brier gap>=0.05 over B-MARKOV-1) or timescale separation (autocorrelation tau_corr>5 vs tau_shuffled~1, gap>=0.05 over Markov-1) reveal valid beyond-memory structure (BC>0.05 p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov) where independent-noise control remains BC~0 (|BC|<0.05 p>0.10), or does even exactly-centered genuine DOM remain at BC~0 indicating no detectable beyond-memory dynamics and physics should remain PARKED while Frontier pursues memory/Tool-bypass?

This PIVOT supersedes the parent Bayesian relative-separation (>=200 nats) agenda while preserving its established pipeline evidence (exact Gamma-ratio, trajectory grouping, genuine capture) as continuity. The new question adds orthogonal falsifiable channels — metastable barriers (committor calibration) and timescale separation (autocorrelation) — that require no new Gate0 SPA discovery (titles>=2 H>0.2) and directly informs Frontier to abandon DOM-predictive dynamics vs retrieval diversity if negative.

## 2. Background and Motivation

### 2.1 What has been established (preserved from `carry_forward.established`)

1. **Synthetic 12-state stochastic hash-routed SPA positive control at K12**: DM log-BF replicates bit-identical vs parents (alpha0.5 obs 643.09 null_median -78.36 p0.0005; alpha1.0 obs 338.67 null_median -130.91 p0.0005; alpha2.0 obs 167.90 p0.0005) with trajectory-grouped perms seed42, audited recomputed_metrics match producer — estimator and permutation machinery are sound. Bounded to N=5000 synthetic SPA, K=12, alpha=1/K, history K2.
2. **Locally-hosted 6-state overlapping proxy at locked 1280x720 via Playwright CDP Accessibility.getFullAXTree + DOM.getDocument + CSS.getComputedStyleForNode**: 36 prototypes (state0-5 x regime A/B x variant0-2, dom_bytes 443 a11y 3971, viewport 1280x720 verified), overlap hist_intersection_color 0.667 mean_overlap 0.399 >0.3 overlapping not deterministic red/blue, H(S_next|C) 2.577-2.584 bits >0.05 valid ceiling, 24/12 strata >=3, |R_visual|/N 0.017 — validates genuine capture pipeline but bounded to synthetic proxy, not real BrowserGym.
3. **Independent-noise genuine replication on same proxy (regime-independent sampling, 50x40 N=2000, trajectory_id grouping, 1000 perms seed42)**: BC -0.023 p0.213 analytic 0.033 cons 0.028; IID null BC -0.029 p0.283 — pipeline not confounded on proxy when action dependence destroyed (VF5 still heuristic). Bounded to proxy.
4. **Barrier/beyond-memory program remains PARKed**: 68 C-WEB-DYNAMICS attempts with 0 real-Web beyond-memory hits, 8-streak barrier PARK, tunnel_flag true; Bayesian K12 is first to pass C1+C3 synthetic but absolute BF -15 nats favors memory on real TodoMVC (EXP-PHYSICS-35651906573) — relative separation concept introduced but not yet measured on real BrowserGym.
5. **Exact Gamma-ratio barrier at 1280x720 with overlapping genuine DOM**: On locally-hosted 6-state proxy, exact gammaln/polygamma (alpha=1/K, no heuristic blending) achieves valid centering |analytic_mean| 0.027<0.1 cons 0.029<0.03, BC 0.171 p_bonf 0.008 d1.99 but fails G1 BC>=0.30 gap 0.011<0.05 tau 1.0 — demonstrates sensitivity limits, not global falsification. Valid to reuse pipeline on real banks.

### 2.2 What has been rejected / do_not_assume (SUPERSEDE but preserved as distinctions)

Bounded rejections from parent audit VF1-VF9:
- Locally-hosted 6-state regime-colored constant-action proxy as valid test of real BrowserGym beyond-memory dynamics — action degeneracy |A|=1 makes DM-BF identically 0, CMI fully attributable to injected DOM<->regime channel.
- Gating plug-in CMI bits*ln2 as Dirichlet-Multinomial log-BF relative separation against 200-nat threshold — metric identity substitution, threshold-scale artifact 0.034 <<200.
- Heuristic analytic with magic constants 0.015/0.005/0.035 as exact Gamma-ratio — prereg forbids heuristic blending/ln100 scaling.
- SHA256 hash-truncated AX embedding (sha256[:4]+state+variant) as genuine AX — violates R_AX_embedding (serialized role/name/value 5k + TRAIN k-means 20) and SHA256 truncation clause.
- Borrowing parent barrier BC 0.171 / Markov -0.0035 as this run's measurement — identity mixing.
- That prior FALSIFIES adjudicates real-Web dynamics or globally closes C-WEB-DYNAMICS — audit claim_ceiling UNMEASURED.

Do_not_assume:
- Do not assume C-WEB-DYNAMICS falsified globally — remains HYPOTHESIS, UNMEASURED on real BrowserGym.
- Do not assume plug-in CMI = DM log-BF marginal likelihood.
- Do not assume small CMI 0.052 bits with rel_sep 0.034 nats demonstrates beyond-memory structure — regime-conditioned CMI vanishes by construction.
- Do not assume heuristic analytic is exact Gamma-ratio.
- Do not assume local 6-state proxy generalizes to production WebShop/TodoMVC heterogeneity.
- Do not assume null negativity on deterministic cells proves action-conditioned structure — absolute BF -10 to -15 favors memory.
- Do not assume AX hash-truncated tokens evidence genuine semantics or visual/AX/computed are independent — they were bit-identical on proxy.
- Do not assume frozen 200-nat or 0.30 thresholds silently lowerable.

### 2.3 Why this experiment (Director comparative reasoning)

- **Vs CONTINUE Bayesian on new production SPAs**: Requires Intel to deliver >=2 Gate0 SPAs which has failed 4 exhaustive enumerations (0/2 to 0/3). Marginal information low.
- **Vs CONTINUE exact Gamma-ratio barrier on larger production manifest**: Requires Intel relaxed Gate0 H>0.1 NL>=20 still pending; would be 6th barrier variant after 5 MEASUREMENT_INVALID — marginal value low until manifest exists.
- **Vs TERMINATE physics entirely**: Premature; Bayesian K12 is first estimator to pass C1+C3 synthetic (168-643 nats) and barrier exact pipeline now achieves valid centering (|perm-analytic|<0.03). PARKing entirely loses only physics program not blocked by site discovery.
- **Vs PIVOT to C-CROSSSITE website holdout**: Requires same missing SPAs, not measurement-ready.
- This test is **low-cost**, reuses already-collected BrowserGym trajectories at 1280x720 (no new Gate0), has valid prerequisites, and directly answers whether physics should stay PARKed. Either BC>0.05 with ECE/tau gaps (first real-Web beyond-memory barrier/timescale detection despite absolute BF -10 to -15) or persistent BC~0 / tau~1 / ECE>0.15 (justify PARK and Frontier orthogonal pivot to MemoryArena/WebAPI-bypass/tool-compilation/alias-catalog per runtime dependency).
- Tests **synthetic-to-real gap** with orthogonal mechanisms (tool compilation, alias catalog, rewind memory candidate if negative) vs more retrieval diversity.

### 2.4 Agent priors distinguished (per Director)

All six are agent priors, not SPIDER evidence:
1. Compounding planning errors over long horizons (0/10 mixed header+body+query+auth joint failure from 0.5^3 while single-channel 10/10 succeed — implies factorization needed).
2. Path dependence/salience: agents reuse recently seen fragments, overweighting early tool choices — requires OOD family hold-out where literally correct path absent.
3. Diminishing returns to local tuning: 12 consecutive C-SEMANTIC-RESOLVE and 5 consecutive C-PARAM-INHERIT failures with unchanged method vs orthogonal mechanism.
4. Caching/replay architectures fail via staleness/false accepts (UNKNOWN ECE<=0.15 precision>=0.85 false_accept<=0.10) harder than raw recall.
5. Representation loss dominates estimator choice (hash-truncated AX[:20] or visible_text_hash discards variables controlling transitions).
Each distinguished from SPIDER evidence which shows only bounded falsification/measurement-invalid, not global closure.

## 3. Hypotheses

**H1 (alternative)**: Same as `spec.json hypothesis`. Genuine browser DOM at locked 1280x720 carries latent regime/session information beyond (URL, H_K=3, leakage-free Action) detectable as barrier/committor or timescale with exact Gamma-ratio and trajectory-grouped permutation: EXISTS R with BC_R >0.05 p_bonf<0.01 |analytic|<0.1 calibrated valid cons<0.03 gap>=0.05 over TF-IDF k5 and Markov-1, AND (ECE<=0.15 Brier gap>=0.05 with >=10 revisits divergent 0.2<q<0.8 OR tau_corr>5 vs tau_shuffled~1 gap>=0.05) while independent-noise BC~0.

**H0 (null)**: No R achieves BC>0.05 p_bonf<0.01 gap>=0.05 and committor/timescale gaps under valid centering/consistency and independent~0; even exactly-centered genuine DOM remains at BC~0.

## 4. State / Action / History / DOM Representation

### 4.1 State `S_next`
- Primary WebShop: `SHA256(normalize(URL_after)|'|'|normalize(title_after)|'|'|DOM_cluster_if_needed)`; TodoMVC: fragment-aware URL as in EXP-PHYSICS-35651906573 enhanced with genuine DOM stratification.
- `normalize(URL)` lowercase strip `?session=/?token=/?keep` SPA hash fragment `#/` strip trailing `/`; `normalize(title)` trim lowercased 200 chars; `S_next` from `t+1` distinct from `DOM_before` at `t` (no post-state leak).
- Report `|R|/N`, `H(S_next|C)`, `|S_next|` cardinality. K handling: K=12 primary; if `|S_next|>=16` or cardinality >12 trigger K=24 exploratory same alpha=1/K.

### 4.2 Action `A_leakageFree`
- `A=(primitive,target_sig)` primitive in {click,fill,navigate,select,submit,hover,type} target_sig=role+name+testId+aria-label+bbox cluster never href/URL/src; diagnostic A_leaky for gap only; MI(DOM;Action)<0.10 else tautology.
- Leakage definition `action.target_href == state_after.url` filtered; verify on new BrowserGym banks.

### 4.3 History `H_K`
- Bayesian DM uses `K2=(S_current, last 2 URLs/states)` primary and `H_K=3` for barrier/timescale strata: `C=(URL_before_normalized, H_K=3)` with >=5 unique C >=3 per stratum for CMI; singleton_SA_rate<70%; `H(S_next|C)>0.05` (>0.2 for barrier) required else degenerate ceiling => MEASUREMENT_INVALID.
- Also compute H_K=3 exploratory for BF.

### 4.4 Genuine DOM (not SHA256 truncated)
- `R_visual`: AX bbox x,y,w,h quantized 10 bins + element_count/tree_depth/interactive_density from dom_bytes.
- `R_computed_style`: 8-value getComputedStyleForNode {color,backgroundColor,visibility,display,opacity,border,position,fontSize}.
- `R_event_seq`: n-gram last 3 primitives.
- `R_AX_embedding`: Accessibility.getFullAXTree serialized role/name/value up to 5k + TRAIN-only TF-IDF/k-means 20 clusters or AX embedding; not SHA256 truncated single value.
- Preserve raw: dom_snapshot, a11y_tree, visual_json, style_dict, event_seq, AX bytes; doc quantization/viewport. Primary requires >=1 R genuine with overlapping spectra verified (style/visual/AX distributions overlap not deterministic regime-color).

## 5. Estimator, Bias Correction, Barrier/Timescale Operationalization

- **Exact Dirichlet-Multinomial marginal likelihood** via scipy.special.gammaln and polygamma (digamma polygamma(0), trigamma polygamma(1)): log ML = Σ_c [gammaln(K*alpha)-gammaln(N+K*alpha)+ Σ_i(gammaln(n_i+alpha)-gammaln(alpha))] with K=n_states (12 primary 24 exploratory) NOT len(counts), alpha_prior in {0.5,1.0,2.0} primary 1.0 reporting, 0.5/2.0 sensitivity. Log BF = log ML(M1)-log ML(M0) in nats. Analytic null mean/std via exact Gamma-ratio (gammaln/polygamma) not heuristic /100*0.1. BC = observed - analytic_mean. Also compute plug-in CMI bits for barrier diagnostics via same strata; primary gating on BC>0.05 p_bonf<0.01 gap>=0.05. Code path research/physics/run_experiment.py _dirichlet_multinomial_log_marginal with K=n_states; grep verification logged.
- **Barrier/committor**: canonical s=(URL_normalized, DOM_cluster, H_K=3) with >=10 revisits across trajectories; for each s collect futures horizon 10 labeling hit B before A (basins empirical via metastable clustering with overlapping spectra verification); q(s)=#hit_B/(#hit_B+#hit_A); require >=5 states with >=10 revisits and >=2 with divergent 0.2<q<0.8 for identifiability (cluster!=attractor); report revisits table, divergent fraction, basin sizes, ECE<=0.15 Brier gap>=0.05 over B-MARKOV-1.
- **Timescale**: autocorr ACF(lag) of DOM embedding/state indicator and lag-MI I(S_{t+k};DOM_t|C); tau via exp fit -1/log(ACF1) or -1/slope log ACF; require tau_corr>5 vs tau_shuffled~1 and BC_lag gap>=0.05 over shuffle null; report ACF 0..5 table.
- **Permutation**: 1000-1999 trajectory-grouped shuffles of genuine DOM labels within each C stratum grouped by trajectory_id seed42 deterministic; null mean/std/p_raw/p_bonf where p_bonf=min(1,p_raw*n_tests) n_tests<=8 floor 0.0005; resampling unit trajectory_id not transition; no Gaussian jitter; calibrated_std=max(analytic_std,perm_std) floor 0.005 analytic /0.01 perm; consistency |perm-analytic|<0.03 required.

## 6. Data Collection and Sampling

### 6.1 Trajectory banks
- **Primary**: BrowserGym WebShop at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 pinned) via CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode. Reuse existing WebShop/TodoMVC 1280x720 banks if manifest research/intel/manifest.json shows browsergym_reuse with dom_bytes>0 a11y_bytes>0 viewport 1280x720.
- **Secondary**: BrowserGym TodoMVC same pipeline (richer genuine DOM vs prior SHA256 URL-only). Both banks N=1000-1999 (50 sessions x20-40 steps or as collected). If not available, collect new WebShop categories/search/cart/checkout and TodoMVC at locked 1280x720 (honest cost, no f*6.0 jitter).
- **Positive control bank**: Synthetic 12-state stochastic hash-routed SPA N=5000 seed42 (same as EXP-PHYSICS-35578258358) with same estimator; no browser needed; also locally-hosted 6-state overlapping genuine proxy (50x40 N=2000, dom_bytes 443 a11y 3971) as secondary genuine-positive expectation BC 0.171 p0.008 valid but fails G1 threshold — demonstrates sensitivity without guaranteeing SURVIVES.
- **Independent-noise bank**: Same WebShop/TodoMVC FSM but action-state dependence destroyed via per-step independent within-trajectory shuffle (regime-independent sampling, not S_current%2, same 1280x720 viewport, same K).
- **IID bank**: Same marginal P(S) i.i.d. with genuine DOM still sampled.

### 6.2 Collection details
- PYTHONHASHSEED=0, numpy seed42, never hash(site); trajectory_id as resampling unit; VIEWPORT 1280x720 verified before claiming genuine (dom_bytes>0 visual_json>0 a11y_bytes>0).
- At least 100 NL transitions per bank or report H(S_next|C) and |R|/N; H(S_next|C)<=0.05 (0.2 for barrier) => MEASUREMENT_INVALID ceiling not falsification.
- Honest cost: sum counters resolve+bind+verify+freshness+browser_steps, no f*6.0 jitter, |rho_shuffled|<0.20.

## 7. Baselines and Controls

### 7.1 Baselines (stable identities)
- **B-DOM-SIMILARITY-TFIDF-K5** (B-DOM-SIMILARITY): TF-IDF cosine k=5 over genuine DOM text (visual text+bbox + AX name/role) fit TRAIN only 70/30 by trajectory_id, 5-NN predicted S_next without stratification; BC_sim via same exact Gamma-ratio K analytic+perm; primary must exceed by gap>=0.05; |analytic_mean|<0.1 cons<0.03 required else invalid.
- **B-MARKOV-1** (B-MARKOV-1): P(S_next|S_current,A_leakageFree) MLE TRAIN by trajectory_id without DOM; BC_markov1 same analytic+perm; gap>=0.05 required.
- **B-MARKOV-K3** (B-MARKOV-K3): P(S_next|S_current,H_K=3) stratified majority; reports BC_hist, accuracy, H; H>0.05 diagnostic.
- **B-SHUFFLE-GROUPED-PERM**: trajectory-grouped 1000-1999 within-strata shuffles grouped by trajectory_id seed42 => perm mean/std/p; analytic mean/std via gammaln/polygamma for |perm-analytic|<0.03 and |analytic|<0.1.
- **B-INDEPENDENT-NOISE-GENUINE**: independent per-step genuine DOM >=6 variants/state same 1280x720 but regime-independent shuffling, identical DM + grouped perms N=1000-1999; |BC|<0.05 p>0.10 |analytic|<0.1; confound => MEASUREMENT_INVALID.
- **B-IID-NULL**: i.i.d. S_next same marginal P(S) seed42; |BC|<=0.05 p>0.10.
- **B-TIMESCALE-SHUFFLE**: time-shuffled genuine trajectories destroying lag structure; tests autocorr tau vs null (tau_null~1, BC_autocorr~0) and lag-MI gap>=0.05 required for timescale claim.
- **B-TRAJECTORY-MEMORY diagnostics**: exact (URL,H_K,Action)->S_next memorization ratio and accuracy, href-leakage gap, MI(DOM;Action)<0.10 tautology check, S_URLonly SHA256(URL) sensitivity, H(S_next|C) ceiling.

### 7.2 Positive control
- **CTRL_POS_SYNTHETIC** (positive_control): Synthetic 12-state stochastic SPA N=5000 seed42 must achieve observed 168-643 nats, null_median -78 to -131, p=0.0005 floor, |perm-analytic|<0.03, |analytic|<0.1, calibrated_std valid, |R|/N diagnostic. Failure => MEASUREMENT_INVALID. Also report deterministic SPA log BF>>0 and locally-hosted 6-state overlapping genuine expectation BC 0.171 p0.008 valid but below 0.30 threshold.

### 7.3 Null controls (stable identities)
- **CTRL_NULL_GROUPED_PERM** (null_control permutation): Trajectory-grouped 1000-1999 perms seed42 |perm-analytic|<0.03 |null_mean|<0.1 null_std>0.01 p_bonf floor 0.0005.
- **CTRL_ANALYTIC_CENTERING**: |analytic_mean|<0.1 on BC scale, consistency<0.03.
- **CTRL_INDEPENDENT_NOISE** (null_control independent): |BC|<0.05 p>0.10 |analytic|<0.1 valid; failure => MEASUREMENT_INVALID confounded.
- **CTRL_IID_NULL**: |BC|<=0.05 p>0.10.
- **CTRL_TIMESCALE_SHUFFLE**: tau_shuffled~1 BC_lag~0.
- Audit verifies source contains gammaln/polygamma and not heuristic sqrt(mean(1/(2n)))*0.1.

## 8. Measurement Validity (pre-registered gates)

All listed in `spec.json measurement_validity` plus:
- Genuine DOM verification: dom_bytes>0 a11y_bytes>0 visual_json>0 computed_style>0 viewport 1280x720 and not SHA256 truncated; overlapping spectra documented.
- H(S_next|C)>0.05 (0.2 for barrier) and |R|/N 0.01-0.30 non-degenerate required.
- Train-only integrity: TF-IDF vocab/embedding centroids/Dirichlet counts/k-means fit TRAIN only 70/30 by trajectory_id; holdout gaps reported.
- Absolute vs relative discipline: Absolute observed log BF exploratory (expected -10 to -15 at K12 on TodoMVC due to K over-penalty); primary gating is barrier/timescale BC>0.05 relative with ECE/tau.
- Trajectory_id grouping, exact gammaln/polygamma, no Gaussian jitter.

## 9. Decision Rule (frozen, verbatim from `spec.json decision_rule`)

Gated execution in order; any validity gate triggers MEASUREMENT_INVALID and prevents primary SURVIVES/FALSIFIED claim.
Gates (MEASUREMENT_INVALID if any fail):
- G0 synthetic positive: observed<=0 OR perm p>=0.001 OR |analytic_mean|>=0.1 OR calibrated_std degenerate OR |perm-analytic|>=0.03 => pipeline blind/miscalibrated.
- G1 independent-noise: BC |BC|>=0.05 p<0.10 valid => confounded.
- G2 IID null: BC>0.05 p<0.10 valid => null miscentered.
- G3 H(S_next|C)<=0.05 OR N<100 OR <5 strata >=3 OR Q<5 states with >=10 divergent revisits => degenerate ceiling/identifiability.
- G4 primary |perm-analytic|>=0.03 on primary K12 both banks => model mismatch.
- G5 viewport/DOM genuine fails (no dom_bytes/visual/computed/AX>0 OR viewport!=1280x720 OR SHA256 truncation) => substrate missing.
- G6 TRAIN leakage or trajectory_id not used => split invalid.

If no G fails, primary per real-Web bank (WebShop primary, TodoMVC secondary): for K12 (and K24 if |S_next|>=16) compute M_OBS_BF, M_NULL_MEDIAN/MEAN/STD/MAX, M_ANALYTIC_MEAN/STD, M_CONS=|perm-analytic|, M_REL_SEP= M_OBS - M_NULL_MEDIAN (nats), M_BC= M_OBS - M_ANALYTIC_MEAN, p_raw=(count_ge+1)/(N_perm+1), p_bonf=min(1,p_raw*n_tests) n_tests<=8 floor 0.0005, gaps G_DOM= M_BC - B_DOM_BC and G_MARKOV= M_BC - B_MARKOV_BC, plus ECE, Brier_gap, tau_corr, tau_shuffled.
sig(bank,K,R)=1 if M_BC>0.05 AND p_bonf<0.01 AND |analytic_mean|<0.1 AND calibrated valid (>0.005 analytic or >0.01 perm) AND cons<0.03 AND G_DOM>=0.05 AND G_MARKOV>=0.05 AND independent~0 (|BC|<0.05 p>0.10) AND |R|/N 0.01-0.30 AND (ECE<=0.15 Brier_gap>=0.05 OR tau_corr>5 vs tau_shuffled~1 gap>=0.05).
- If EXISTS bank,R sig==1 => SURVIVES_CURRENT_TEST: real Web shows detectable barrier/committor or timescale beyond-memory structure at exact centering, bounded to that bank/K/R. Report absolute BF exploratory (-10 to -15 expected) separately.
- If FORALL banks sig fails while gates pass => FALSIFIED-IN-SETTING: even correctly centered genuine DOM remains BC~0, no barrier/timescale beyond-memory at N=1000-1999 with this representation; physics remains PARKed.
Exploratory K24 per-branch consistency reported but not gating unless K12 sig already.

## 10. Primary Metrics (stable identities for AUDIT)

- M_OBS_BF_K12, M_OBS_BF_K24 (nats)
- M_NULL_MEDIAN_K12, M_NULL_MEAN_K12, M_NULL_STD_K12, M_NULL_MAX_K12, M_ANALYTIC_MEAN_K12, M_ANALYTIC_STD_K12, M_CONSISTENCY_K12=|perm-analytic|
- M_BC_BF_K12 = M_OBS - M_ANALYTIC_MEAN (nats) and M_BC_BITS (bits) for CMI
- M_REL_SEP_K12 = M_OBS - M_NULL_MEDIAN (nats) — exploratory for BF scale
- M_P_RAW_K12, M_P_BONF_K12 (Bonferroni n_tests<=8 floor 0.0005)
- M_GAP_DOM_K12, M_GAP_MARKOV_K12 (nats, >=0.05)
- M_ABSOLUTE_BF_K12 (same as M_OBS, exploratory -10 to -15 expected)
- M_ECE_K12, M_BRIER_GAP_K12 (barrier calibration)
- M_TAU_CORR_K12, M_TAU_SHUFFLED_K12, M_TAU_GAP_K12
- M_REVISITS_TABLE, M_DIVERGENT_FRACTION, M_Q_DIVERGENT
- M_INDEPENDENT_BC_K12, M_INDEPENDENT_P_K12, M_INDEPENDENT_ANALYTIC_MEAN_K12
- M_IID_BC_K12, M_BASELINE_DOM_TFIDF_K5_BC, M_BASELINE_MARKOV1_BC
- M_H_SNEXT_GIVEN_C, M_R_OVER_N, M_CALIBRATED_STD_K12 = max(analytic_std, perm_std)
- Corresponding K24 metrics suffixed _K24 if triggered; per-R variants _VISUAL/_COMPUTED/_AX/_EVENT

## 11. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Deterministic FSM (TodoMVC det_ratio 0.846-0.944, B2 1.0): H(S_next|C) near 0, perm null heavily negative** | Report H(S_next|C) per bank; require H>0.05 (0.2 barrier); WebShop bank provides stochastic heterogeneity; acknowledge absolute BF negative exploratory; primary is barrier/ECE/tau not absolute BF, with independent~0 guard. |
| **K=12 over-penalty on S=3-4: BF -10 to -15 even when relative signal exists** | K12 frozen primary; report K12 absolute exploratory; trigger K24 only if |S_next|>=16; sensitivity to K={3,4,5} reported exploratory; gaps use same K so penalty cancels. |
| **Isomorphic replication inflating n (vanillajs/react/svelte bit-identical): Effective replications 2 not 5** | Treat WebShop vs TodoMVC as distinct banks; do not pool 5 variants as independent; report per-variant but gate on bank level; note isomorphism. |
| **Genuine DOM vs SHA256 truncation collapse** | Verify dom_bytes>0 a11y_bytes>0 visual bbox+computed 8-value+AX embedding preserved; audit checks source not SHA256-only; report |R|/N 0.01-0.30 genuine finite vocab with overlapping spectra. |
| **Viewport heterogeneity 1024 vs 1280 changes bbox** | Lock 1280x720 via CDP + Page.setViewportSize; verify viewport in provenance; reject if !=1280x720. |
| **Trajectory grouping vs transition-level shuffle inflate p** | Enforce trajectory_id unit, 1000-1999 perms seed42, |perm-analytic|<0.03 guard; independent-noise BC~0 confirms not S_current%2. |
| **Heuristic bias correction masquerading as exact** | Require scipy.special.gammaln/polygamma exact; audit grep verification; no sqrt(mean(1/(2n)))*0.1 or +0.012 floor. |
| **Multiple testing inflation (n_tests<=8 isomorphic)** | p_bonf=min(1,p_raw*n_tests) floor 0.0005; note effective 2-3 for isomorphic Rs; report both p_raw and p_bonf. |
| **Small N (80 NL prior) vs target 1000-1999 power limited** | Require N>=100 valid per bank H>0.05; WebShop should provide >=1000 if manifest available; else collect until >=1000 or report MEASUREMENT_INVALID ceiling. |
| **Cluster=attractor fallacy, frequent endpoint=attractor** | Require >=10 revisits divergent futures 0.2<q<0.8 and ECE<=0.15 Brier gap>=0.05; report revisits table; cluster!=attractor check. |
| **Low PCA dimension = low physical dimension** | Not claimed; we test tau_corr>5 vs tau_shuffled~1 and BC gap, not PCA dimension. |
| **Action encoding degeneracy** | Use A_leakageFree never href; verify MI(DOM;Action)<0.10; report degenerate_action diagnostic log BF 0. |

## 12. Product Consequences

- **Positive (SURVIVES)**: First real-Web barrier/timescale beyond-memory signal at exact centering (|analytic|<0.1 cons<0.03 std>0.01) with BC>0.05 p_bonf<0.01 gap>=0.05 and ECE<=0.15/Brier gap or tau>5 on >=1 real bank at 1280x720 genuine DOM while independent~0 bridges synthetic-to-real gap; absolute BF -10 to -15 remains exploratory. Unparks Physics for production manifest with real session/permission regimes and larger state spaces; product distills barrier/timescale detector as freshness/barrier guard (regime-aware retrieval, visual+AX signature, event-seq guard) into kernel resolve/verify; quantify delta-repair cost and cross-site holdout transfer; no generic promotion until transfer validated.
- **Negative (FALSIFIED-IN-SETTING with valid gates)**: Closes barrier/committor and timescale beyond-memory program on BrowserGym WebShop/TodoMVC N=1000-1999 genuine 1280x720 even correctly centered => no detectable beyond-memory structure at this scale/representation; physics remains PARKed pending larger production manifest with real session/permission latent regimes and larger |S|; Frontier PIVOT to orthogonal MemoryArena / WebAPI bypass / compile-execute / tool-bypass / alias-catalog. Do NOT invest in this DOM barrier dynamics as mechanical prior at current N.

## 13. Estimated Cost / Expected Information Gain

- **Estimated cost**: Low: reuses existing BrowserGym trajectory banks at 1280x720 if available plus optional locally-hosted 6-state genuine capture <10 min headless; analysis 80-120k exact gammaln/polygamma fits <1ms each + TF-IDF <5 min + revisits/ACF fits <5 min; scipy+sklearn+headless Chromium if needed; total <2h wall-clock <8GB RAM no GPU.
- **Expected information gain**: Very high and tunnel-breaking per Director: vs CONTINUE barrier on larger manifest (requires Gate0 still pending) and vs TERMINATE (premature) this low-cost real-trajectory test directly answers whether physics should stay PARKed. Either BC>0.05 gap>=0.05 with ECE/tau (first real-Web beyond-memory metastable/timescale despite absolute -10 to -15) or persistent BC~0 / tau~1 / ECE>0.15 (justify PARK and Frontier orthogonal pivot) finally adjudicates barrier/timescale program without requiring new Gate0. Orthogonal falsifiable program per C-WEB-DYNAMICS next_gate and first real-Web test of exact-correction + genuine DOM barrier/timescale; directly tests Director's combined exact Gamma-ratio + genuine visual/AX spectra + barrier/committor/timescale with trajectory-grouped permutation and independent-noise BC~0 control.

## 14. Inherited Parent Handoff Carry-Forward (exact, SUPERSEDE but preserved as distinctions)

### Established (from EXP-PHYSICS-35892828492)
1. Synthetic 12-state stochastic hash-routed SPA positive control at K12: DM log-BF replicates bit-identical vs parents (alpha0.5 obs 643.09 null_median -78.36 null_max -21.14 p0.0005; alpha1.0 obs 338.67 null_median -130.91 null_max -92.94 p0.0005; alpha2.0 obs 167.90 null_median -116.10 p0.0005) with trajectory-grouped perms seed42 — estimator and permutation machinery are sound. Bounded to N=5000 synthetic SPA, K=12, alpha=1/K, history K2.
2. Locally-hosted 6-state overlapping proxy at locked 1280x720: 36 prototypes (state0-5 x regime A/B x variant0-2, dom_bytes 443 a11y 3971, viewport 1280x720 verified), overlap hist_intersection_color 0.667 mean_overlap 0.399 >0.3, H(S_next|C) 2.577-2.584 bits >0.05, 24/12 strata >=3, |R_visual|/N 0.017 — validates genuine capture pipeline but bounded to synthetic proxy, not real BrowserGym.
3. Independent-noise genuine replication on same proxy (regime-independent sampling, 50x40 N=2000, trajectory_id grouping, 1000 perms seed42): BC -0.023 p0.213 analytic 0.033 cons 0.028; IID null BC -0.029 p0.283 — pipeline not confounded when action dependence destroyed.
4. Barrier/beyond-memory program remains PARKed: 68 C-WEB-DYNAMICS attempts with 0 real-Web beyond-memory hits, 8-streak barrier PARK, tunnel_flag true; Bayesian K12 is first to pass C1+C3 synthetic but absolute BF -15 nats favors memory on real TodoMVC — relative separation concept introduced but not yet measured on real BrowserGym.

### Rejected
- Locally-hosted 6-state regime-colored constant-action proxy as valid test of real BrowserGym dynamics — bounded rejection (audit VF1 substrate substitution, |A|=1 makes DM-BF 0, CMI signal fully attributable to injected DOM<->regime channel).
- Gating plug-in CMI bits*ln2 as DM log-BF relative separation against 200-nat threshold — bounded rejection (metric identity substitution).
- Heuristic analytic with magic constants as exact Gamma-ratio — bounded rejection (VF5).
- SHA256 hash-truncated AX embedding as genuine AX — bounded rejection (VF6).
- Borrowing parent barrier BC 0.171 as this run's measurement — bounded rejection (VF9).
- That prior FALSIFIES adjudicates real-Web dynamics globally — bounded rejection (claim_ceiling UNMEASURED).

### Unknown (must not assume)
- Whether real BrowserGym WebShop/TodoMVC trajectory banks at 1280x720 (50x40 N=1000-1999) exist or can be collected in this environment (intel/manifest.json absent at audit) and what H(S_next|C), |R|/N, |A| support they would show.
- What exact closed-form DM log-BF marginal likelihood (K=12/24, alpha=1/K, gammaln/polygamma) observed/null/analytic mean/std/p_bonf/gap/ECE/Brier/tau would be on real banks with trajectory_id grouping and non-degenerate |A|>1, and whether G4 |perm-analytic|<0.03 would still pass.
- Whether larger production manifest with real session/permission latent regimes and richer multi-feature genuine DOM (visual bbox+computed+AX combined without tautology) would achieve BC>0.05 gap>=0.05 or remain BC~0.
- Correct Dirichlet-Multinomial variance formula for stratified CMI/BF under trajectory grouping and whether 200-nat BF threshold calibrated on synthetic positives is reachable on real Web where null is -25 to -40 nats.

### Do Not Assume (unsafe)
- Do not assume C-WEB-DYNAMICS falsified globally — this run prior was MEASUREMENT_INVALID and UNMEASURED on real BrowserGym; 68-attempt streak remains HYPOTHESIS, not REJECTED.
- Do not assume plug-in CMI equals DM log-BF — frozen primary gates on BF nats threshold 200 is BF-scale.
- Do not assume small CMI with rel_sep 0.034 demonstrates beyond-memory — regime-conditioned CMI vanishes.
- Do not assume heuristic analytic is exact Gamma-ratio.
- Do not assume local 6-state proxy generalizes to production WebShop/TodoMVC heterogeneity.
- Do not assume null negativity proves action-conditioned structure — absolute BF -10 to -15 favors memory.
- Do not assume AX hash-truncated tokens evidence genuine AX semantics.
- Do not assume frozen thresholds should be silently lowered.

## 15. Preregistration Freeze Checklist

- [ ] `spec.json` frozen with above question/hypothesis/falsifier/baselines/positive_control/null_control/measurement_validity/decision_rule and stable metric/control identities
- [ ] `prereg.md` (this file) frozen with above 8.1 exact gammaln/polygamma, barrier/timescale operationalization, gates G0-G6, validity threats, absolute vs relative discipline, H>0.05, |R|/N, TRAIN-only, trajectory_id grouping
- [ ] `request.json` director_mandate stored immutable with agent_priors_used[6] distinguished
- [ ] `freeze.json` deterministic hashes of request.json + spec.json + prereg.md before EXECUTE
- [ ] No outcome-bearing measurements inspected during DESIGN (synthetic positive control numbers are parent evidence, not this experiment's outcomes)

## 16. References

- Parent synthetic Bayesian: `research/experiments/EXP-PHYSICS-35578258358` (SURVIVES synthetic K12 exact)
- Real TodoMVC Bayesian: `research/experiments/EXP-PHYSICS-35651906573` (SUPPORTS formally but REVISE audit absolute BF -10 to -15, isomorphic 2 effective)
- Barrier G1: `research/experiments/EXP-PHYSICS-35860320716` (MEASUREMENT_INVALID BC 0.171<0.30 gap 0.011 exact gammaln/polygamma valid centering)
- Prior proxy failure: `research/experiments/EXP-PHYSICS-35892828492` (MEASUREMENT_INVALID VF1-VF9 UNMEASURED, heuristic analytic, constant action, hash-truncated)
- Code reuse: `research/physics/run_experiment.py _dirichlet_multinomial_log_marginal`, `research/physics/execute_35860320716.py analytic_dm_mean_std_exact gammaln/polygamma`
- Substrate pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, honest cost sum resolve+bind+verify+freshness+browser_steps no f*6.0 jitter |rho_shuffled|<0.20

---
*End of preregistration. EXECUTE must run exactly this frozen design, preserving raw evidence -> observation -> derived measurement -> interpretation distinction, with `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved` in `result.json`.*
