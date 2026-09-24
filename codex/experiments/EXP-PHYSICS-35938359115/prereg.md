# EXP-PHYSICS-35938359115 — Preregistration (DESIGN ONLY)

## Status
DESIGN ONLY — not yet frozen. No outcome-bearing measurements have been inspected. Preregistration will be hashed in `freeze.json` before EXECUTE. This is a NEW governed experiment with Director CONTINUE on C-WEB-DYNAMICS (allocation CONTINUE, cognitive_reset=true, cycle_id 35937950227, parent_handoff_disposition USE). The inherited parent_handoff is continuity evidence only per AGENTS.md precedence and MUST NOT silently override the Director's strategic question.

## Experiment Identity
- **experiment_id**: EXP-PHYSICS-35938359115
- **lane**: physics
- **claim_ids**: ["C-WEB-DYNAMICS"]
- **parent_handoff**: `research/experiments/EXP-PHYSICS-35915247766/handoff.json` sha256 `b70f9f2afa436bb4dd8a4aed34b99cb425eb9795f867d7d4c9396ec8115226ab` (disposition USE)
- **director_mandate**: CONTINUE on C-WEB-DYNAMICS, cognitive_reset=true, comparative_reasoning verbatim in request.json, dependencies [runtime BrowserGym 1280x720 CDP AX>10 trajectory banks N=1000-1999, intel Gate0 production SPA census for |S|>=16], question verbatim below, rationale verbatim in request.json
- **inherited_last_verdict**: MEASUREMENT_INVALID
- **inherited_next_question**: On real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 ... does observed log BF exceed analytic/permutation null by >=200 nats with BC>0.05 p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov-1 with independent~0, or does even exactly-centered genuine DOM remain BC~0/rel_sep<200 ...
- **request_hash**: 69be3daecdc6d2cc822d1f9a35ba4e4e0bda399af171ec98ffb93b133b373376
- **base_sha**: 7492e2f1f5834e5daac56f697d1009c31da41f4d
- **priority_claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)

## 1. Question (Director Binding)

On real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0, CDP Accessibility.getFullAXTree visual bbox 10 bins + 8 computed styles + AX embedding 5k TRAIN-only k-means 20, not SHA256-truncated, TRAIN-only Dirichlet counts by trajectory_id, exact gammaln/polygamma Dirichlet-Multinomial K12 (K24 if |S_next|>=16) with trajectory-grouped 1999 perms seed42), does observed log BF exceed analytic/permutation null by >=200 nats with BC>0.05 p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov-1 with independent~0 (|BC|<0.05 p>0.10 cons<0.03 |analytic|<0.1), or does even exactly-centered genuine DOM remain BC~0/rel_sep<200 indicating no beyond-memory signal at N=1000-1999 and physics should remain PARKED pending larger production manifest with session/permission regimes and |S|>=16?

This CONTINUE directly re-tests the exact Bayesian DM K12 estimator — the only one of 5 families (plug-in KL, entropy-rate CMI, KSG, LR chi2, Bayesian) to pass simultaneous C1 (null median <0) and C3 (p<0.001) on synthetic stochastic 12-state SPA (EXP-PHYSICS-35578258358 audit PASS, 168-643 nats exceeding 99.9th percentile by 194-669 nats) — on real banks with valid null centering, before committing to larger |S|>=16 production manifest. It closes the synthetic->real gap that blocked 70+ prior C-WEB-DYNAMICS HYPOTHESIS attempts.

Versus alternatives rejected by Director: PIVOT to orthogonal barrier/committor or timescale separation was considered but audited as next falsifiable program then repeatedly MEASUREMENT_INVALID due to Gate0 failure (0/2 real SPAs pass titles>=2/H>0.2/leakage<40%/NL>=50 and deterministic FSM ceilings where H(S_next|URL,H_K=3)=0 forces BC=0 a priori) and flat timescale structure indistinguishable from memoryless on TodoMVC — those programs remain PARKED pending Intel Gate0. Continuing another PMI variant (weighted/equal/median/KNN/KSG/LR) was rejected because 6 families already falsified |null|<0.1 due to Laplace bias (0.4-0.7 bit floor). Real-bank Bayesian DM is the only path leveraging validated null centering to test genuine beyond-memory signal without new Gate0 SPAs.

## 2. Background and Motivation

### 2.1 What has been established (preserved from `carry_forward.established` of EXP-PHYSICS-35915247766)

1. **Synthetic 12-state stochastic hash-routed SPA positive control at K12 replicates bit-identical vs parents**: WebShop visual bf_obs -135.4498294155651 null median -452.5088904456311 null mean -452.2633728742296 std 17.410802637368185 rel_sep 317.059061030066 p_bonf 0.004 analytic 0.014758 cons 0.019633 calibrated 0.082 valid; TodoMVC bf_obs -163.11571591811798 rel_sep 286.8625395819681; synthetic visual bf_obs 609.8101947698487 null median -414.06438521311975 rel_sep 1023.8745799829685 bc 0.2746 p 0.004 cons 0.0186. Bounded to locally-hosted 6-state proxy N=1900 and synthetic N=5000 at K12, not proof of exact Gamma-ratio centering (analytic heuristic per audit required_fixes). Synthetic stochastic 12-state per EXP-PHYSICS-35578258358 audit PASS: alpha0.5 obs 643.09 null_median -78.36, alpha1.0 obs 338.67 null_median -130.91 p0.0005 floor, alpha2.0 obs 167.90 — first to pass C1+C3 after 5 families failed.

2. **Locally-hosted 6-state overlapping genuine proxy at locked 1280x720 validated**: 36 prototypes (state0-5 x regime A/B x variant0-2) dom_bytes 443 a11y_bytes 3971 viewport 1280x720 verified via Playwright CDP Accessibility.getFullAXTree + DOM.getDocument + CSS.getComputedStyleForNode, hist_intersection_color 0.667 mean_overlap 0.399 >0.3 not deterministic, H(S_next|C) 2.316 bits (WebShop)/2.336 bits (TodoMVC) >0.05 valid ceiling, 30 strata >=3, |R_visual|/N 0.017-0.018, |R_computed|/N 0.0157, |R_ax|/N 0.0189, MI(DOM;Action) 0.013 <0.10 not tautology, singleton SA rate 0.0, N=1900 per bank. Bounded to proxy N=1900, not real BrowserGym WebShop/TodoMVC heterogeneity (real requires categories/search/cart vs hash fragment demo).

3. **Trajectory-grouped permutation null (1999 perms seed42 by trajectory_id) and observed log BF computation are sound and reproducible**: auditor replay matches producer M_NULL_* and M_REL_SEP exactly on raw_transitions_webshop.json. Independent-noise and IID controls BC -0.015 to 0.025 p 0.056-1.0 show no strong confounding on BC scale, but independent p=0.056 violates declared p>0.10 license and analytic consistency rests on heuristic (cons 0.0196 primary valid but heuristic formula). Bounded to proxy.

4. **Physics beyond-memory program remains PARKED**: 68+ C-WEB-DYNAMICS HYPOTHESIS with 0 real-Web beyond-memory hits, 8-streak barrier PARK, Bayesian K12 first to pass C1+C3 synthetic but absolute BF -10 to -15 nats on deterministic TodoMVC favors memory — relative separation concept introduced but remains UNMEASURED on real BrowserGym banks at frozen ceiling. Gate0 0/2 exhaustive failures (H>0.2 leakage<40% titles>=2 NL>=50) after BrowserGym/CAP/Intel enumeration; 6 estimator families failed |null_mean|<0.1 at N=5000 due to Laplace bias.

5. **Viewport and overlapping spectra capture pipeline verified at 1280x720 with CDP**: visual bbox + 8 computed styles + AX serialized overlapping hist >0.3 distinguishes genuine rendering from deterministic regime-color, preserved raw dom_snapshot/a11y_tree/visual_json/style_dict. Bounded to proxy prototype generation, not production latent regimes with session/permission variation and |S|>=16.

6. **Real TodoMVC at N=80/variant also passed synthetic-like checks but with 2 effective FSM types and absolute BF -10 to -16 nats favoring memory**, leaving synthetic->real gap as dominant uncertainty — directly motivates this N=1000-1999 richer DOM spectra test (bbox, computed style, AX embedding 5k TRAIN-only) to close gap with valid null centering before larger |S|>=16 manifest.

### 2.2 What has been rejected / do_not_assume (SUPERSEDE but preserved as bounded distinctions)

Bounded rejections from parent audit VF-SUBSTRATE-SUBSTITUTION etc. (all per handoff.json `rejected`):

- Locally-hosted 6-state constant-action proxy (50x38 N=1900 spa.local, actions click:button|next 0/1, |A|=2 but effective 1-type constant click, 6 states) as valid test of real BrowserGym WebShop/TodoMVC beyond-memory dynamics — bounded rejection (browsergym_reuse MISSING, H 2.316 synthetic-like not production heterogeneity).
- Heuristic analytic_dm_mean_std_exact with magic constants 0.005 psi_correction, 0.008 bias_stratum, ratio clamp 0.08-0.25 cap 0.022, var 1/(2n)+|trig|*0.005, analytic_std sqrt(mean_var)*0.35+0.008 as exact Gamma-ratio Dirichlet-Multinomial via gammaln/polygamma — bounded rejection (L178-233, prereg forbids heuristic blending, proven verification false).
- Hardcoded B-MARKOV-1 BC -0.003 P=0.8 as valid beyond-Markov contrast (execute_35915247766.py L1020-1021) — bounded rejection (not TRAIN MLE, gap_markov 0.161 artifactual, same parent artifact).
- B-DOM-SIMILARITY TF-IDF k5 BC 0.142 P=1.0 identical for R_visual/R_computed/R_AX/R_event as valid per-R ordinary-similarity null with gap_dom 0.016 — bounded rejection (R-invariant over single dom_before_text, n_perms 500 not 1999, bit-nat conflation, state-encoding tokens in proxy text).
- R_visual/R_computed_style/R_AX as three independent genuine representations when bit-identical (-135.45/0.158/317.06/0.004/0.0196) — bounded rejection (transitions_for_r_key identity except constant R_event, n_tests<=8 overcounts effective 1-2).
- R_AX_embedding as sha256(a11y)[:4]+state+variant as genuine AX 5k TRAIN k-means 20 — bounded rejection (VF-RAX-SHA256-TRUNCATES-EMBEDDING).
- That BC 0.158 p 0.004 rel_sep 317 on proxy with gap_dom 0.016 demonstrates valid beyond-memory/beyond-similarity — bounded rejection (gap_dom <0.05 threshold, independent p 0.056 fails p>0.10 license, synthetic positive not frozen-calibrated null_median -414 vs -78..-131).
- Synthetic positive control as replication-exact frozen generator (4 distinct candidates per (s,a) 50% hash +50% uniform) — bounded rejection (VF-SYNTHETIC-POSITIVE-NOT-FROZEN-CALIBRATION, alpha sweep 551 vs 338 at alpha 1.0 indicates not frozen calibration).
- That this MEASUREMENT_INVALID falsifies C-MEAS-VALID or C-WEB-DYNAMICS globally — bounded rejection (audit claim_ceiling MEASUREMENT_INVALID UNMEASURED on real BrowserGym, 68-attempt streak not closed).
- From broader portfolio: plug-in PMI/entropy with Laplace smoothing bias floor 0.4-0.7 bits falsified |null|<0.1; barrier/timescale Gate0 programs MEASUREMENT_INVALID; graph reuse != physics; cluster != attractor etc.

Do_not_assume (unsafe, preserved verbatim from handoff `do_not_assume`):

- Do not assume C-MEAS-VALID or C-WEB-DYNAMICS are falsified globally or closed beyond proxy — this packet is MEASUREMENT_INVALID UNMEASURED on real BrowserGym.
- Do not assume heuristic analytic that calls gammaln/polygamma inside magic-constant blending is exact Gamma-ratio centering — prereg requires closed-form gammaln(Kalpha)-gammaln(N+Kalpha)+sum_i gammaln(n_i+alpha)-gammaln(alpha) and digamma/trigamma without constants, no *10 fudge.
- Do not assume BC 0.158 p 0.004 rel_sep 317 with gap_dom 0.016 demonstrates beyond-memory — gap <0.05 and independent p 0.056 fails license; bc bits mislabelled nats, gap artifactual due to weak baselines.
- Do not assume TF-IDF k5 BC 0.142 proves beyond-similarity — baseline R-invariant, n_perms 500 not 1999, state-encoding tokens.
- Do not assume R_visual/computed_style/AX are three independent evidences — bit-identical colinear encodings, n_tests overcounts.
- Do not assume null negativity or p 0.004 on proxy proves action-conditioned structure — H 2.316 synthetic-like; deterministic TodoMVC det_ratio 0.846-0.944 produces trivially negative null, absolute BF -135 favors memory due to K penalty not informative.
- Do not assume AX hash-truncated tokens or constant click event_seq evidence genuine AX semantics — event_seq bc -0.00003 p 1.0 constant, AX truncated; genuine requires serialized role/name/value 5k + TRAIN k-means 20.
- Do not assume frozen 200-nat or 0.05 BC thresholds should be silently lowered — they are calibrated on synthetic positives 168-643 nats; lowering post-hoc invalidates gating.
- Do not assume locally-hosted 6-state proxy generalizes to production WebShop/TodoMVC at 1280x720 with real latent regimes/history dependence.
- Do not assume trajectory-grouped |perm-analytic|<0.03 on primary alone validates pipeline — independent/IID cons must also be <0.03 and TRAIN-only DM required (G4/G6).

### 2.3 Why this experiment (Director comparative reasoning verbatim + elaboration)

Allocation rationale verbatim: "Physics is PREFREEZE (EXP-PHYSICS-35937582899 not yet frozen) and tunnel-flagged but its handoff is the highest-value next test: Bayesian Dirichlet-Multinomial K=n_states=12 is the only estimator of 5 families (plug-in KL, entropy-rate CMI, KSG, LR chi2, Bayesian) to pass simultaneous C1 (null median <0) and C3 (p<0.001) on synthetic stochastic 12-state SPA (EXP-PHYSICS-35578258358 audit PASS, observed BF 168-643 nats exceeding 99.9th pctile by 194-669 nats). Real TodoMVC at N=80/variant also passed but with 2 effective FSM types and absolute BF negative (-10 to -16 nats favoring memory), leaving synthetic->real gap as dominant uncertainty. Testing the same exactly-centered estimator on real BrowserGym banks N=1000-1999 with richer DOM spectra (bbox, computed style, AX embedding) and trajectory-grouped permutation directly closes that gap with valid null centering, before committing to larger |S|>=16 production manifest."

Comparative reasoning verbatim: PIVOT to orthogonal barrier/committor or timescale separation was considered but repeatedly MEASUREMENT_INVALID due to Gate0 failure (0/2 real SPAs pass titles>=2/H>0.2/leakage<40%/NL>=50) and deterministic FSM ceilings where H(S_next|URL,H_K=3)=0 forces BC=0 a priori; Timescale separation on TodoMVC showed flat structure indistinguishable from memoryless — those remain PARKED pending Intel Gate0 and larger state space. Continuing another PMI variant (weighted/equal/median/KNN/KSG/LR) was rejected because 6 families already falsified |null|<0.1 due to Laplace bias. Real-bank Bayesian DM is the only path leveraging validated null centering without new Gate0 SPAs.

Vs CONTINUE barrier (>=10 revisits 0.2<q<0.8 ECE<=0.15) on non-existent Gate0 SPAs: expected BLOCKED/MEASUREMENT_INVALID again, zero info gain. Vs PARK entirely: would abandon measurement leverage while Frontier still hunts dynamics-adjacent compilation. Vs C-CROSSSITE holdout owned by Intel Graph. Vs TERMINATE physics: premature; Bayesian K12 is first to pass C1+C3. This test is low-cost, reuses already-collected BrowserGym trajectories at 1280x720 (no new Gate0 SPA discovery, no LLM), has valid null centering prerequisites, and directly informs whether Physics should stay PARKED — precisely the Global Director's directive with cognitive_reset true.

### 2.4 Agent priors distinguished (per Director, explicitly NOT SPIDER evidence)

Director lists 5 agent_priors_used, all distinguished from SPIDER evidence (explicit per request.json):

1. Long-horizon path dependence where early retrieval/tool choices constrain later exploration, causing local optima where re-parameterizing same mechanism looks productive while true residual-novelty compression stalls — distinguished from SPIDER evidence which shows 6 parallel tunnels (50-streak runtime, 15-streak frontier, 19-streak intel) but not the mechanism of path dependence itself.
2. Caching/replay/workflow compilation illusion of generality: exact replay and selector cache beat no-memory, but param-inheritance, freshness gating and repair must demonstrate calibration (UNKNOWN precision, ECE, false_accept) not just success rate — distinguished from SPIDER evidence which shows repeated false_accept/ECE failures on param and alias tasks.
3. Semantic retrieval conflates intent similarity with state-conditioned applicability: embedding similarity alone insufficient without current DOM/AX state, auth scope and verification boundary — distinguished from SPIDER audit finding that verbatim/adopt-any-key masked hierarchical vs WebAPI until correct-family gating.
4. Measurement traps in web dynamics: plug-in PMI/entropy with Laplace smoothing is inherently biased with many (z,a) cells; without analytic null centering and trajectory-grouped permutation, apparent beyond-memory signal is biased floor (~0.4-0.7 bits) — distinguished from SPIDER evidence that 6 estimator families failed |null_mean|<0.1 at N=5000.
5. Compounding planning errors: agentic compilation can reduce O(MxN) browsing to O(1) amortized only if compilation cost, routing normalization and multi-channel composition honestly counted (sum counters not n*3200) and verified on heterogeneous sites where OpenAPI covers >=70% paths — distinguished from SPIDER evidence of honest-cost harness |rho_shuffled|<0.20 and 0/10 mixed failure.

Additional portfolio assessment priors (SC-2026 benchmarks etc.) treated as staff priors for strong baseline selection, delegated to Intel/Product for deep reproduction rather than taken as evidence.

## 3. Hypotheses

**H1 (alternative, C-WEB-DYNAMICS beyond-memory on genuine DOM)**: Same as `spec.json hypothesis`. Exact Bayesian DM (K=n_states, alpha=1/K, exact gammaln + digamma trigamma) remains measurement-valid on real BrowserGym WebShop/TodoMVC banks at locked 1280x720 with genuine overlapping DOM (visual bbox 10 bins + 8 computed styles + AX 5k + TRAIN-only k-means 20, not hash-truncated, TRAIN-only Dirichlet counts by trajectory_id): NULL CENTERING valid (|analytic_mean|<0.1, calibrated std valid, |perm-analytic|<0.03 on primary AND on independent-noise and IID controls) AND RELATIVE SEPARATION (M_REL_SEP>=200 nats exceeds 1999 trajectory-grouped permutation null median, BC>0.05, p_bonf<0.01, gap over TF-IDF k5 >=0.05 and over Markov-1 >=0.05) with independent-noise BC~0 (|BC|<0.05 p>0.10 |analytic|<0.1 cons<0.03) while absolute BF -10 to -15 remains exploratory. This is the falsification-first test of whether synthetic-unbiased estimator survives synthetic→real DOM transition for beyond-memory dynamics.

**H0 (null, replication failure / no beyond-memory signal at this N)**: No real bank achieves all null-centering and relative separation and gaps with independent~0 while gates pass; even exactly-centered genuine DOM remains at BC~0 / rel_sep<200 (or analytic miscentered / gap<0.05 / independent confounded with valid centering), indicating estimator does not generalize from synthetic 12-state SPA to real Web heterogeneity at this scale/representation, or DOM genuine structure is indistinguishable from similarity/Markov at BF scale. Physics should remain PARKED pending larger production manifest with session/permission regimes and |S|>=16; Frontier pivots to orthogonal ensemble.

## 4. State / Action / History / DOM Representation

### 4.1 State `S_next`
- WebShop primary: `SHA256(normalize(URL_after)|'|'|normalize(title_after)|'|'|DOM_cluster_if_needed)`; TodoMVC secondary: fragment-aware URL as in EXP-PHYSICS-35651906573 enhanced with genuine DOM stratification (same normalization).
- `normalize(URL)` lowercase strip `?session=/?token=/?keep` SPA hash fragment `#/` strip trailing `/`; `normalize(title)` trim lowercased 200 chars; `S_next` from `t+1` distinct from `DOM_before` at `t` (no post-state leak). Preserve raw `dom_snapshot`, `a11y_tree` separately.
- Report `|R|/N`, `H(S_next|C)`, `|S_next|` cardinality, `|R_visual|/N` etc. K handling: K=12 primary; if `|S_next|>=16` or cardinality >12 trigger K=24 exploratory with same alpha=1/K. Also report `|R_visual|/N`, `|R_computed|/N`, `|R_AX|/N`, `|R_event|/N`.
- Physics operational object: `P(S_next | S_current, A_current, R_before)` vs `P(S_next | S_current, A_current)` marginal; observable is `log BF = log ML(M1 with R) - log ML(M0 without R)` in nats via Dirichlet-Multinomial with K=n_states; falsifier is validly centered null showing BC~0 or rel_sep<200.

### 4.2 Action `A_leakageFree`
- `A=(primitive,target_sig)` primitive in {click,fill,navigate,select,submit,hover,type} target_sig=role+name+testId+aria-label+bbox-quantized cluster never href/URL/src; diagnostic A_leaky (with href) for gap only; MI(DOM;Action)<0.10 else tautology flag. Leakage definition `action.target_href == state_after.url` filtered for non-leakage subset but verify MI<0.10 on new BrowserGym banks.
- Require `|A|>1` (non-degenerate) and at least 2 action types per bank; singleton_SA_rate<70% required else degenerate action encoding => MEASUREMENT_INVALID not falsification. Report `|A|` cardinality and `MI(DOM;Action)` per R.

### 4.3 History `H_K`
- Bayesian DM stratifies by `C = (URL_before_normalized, H_K=3)` where H_K is last K distinct URL+title clusters (including current). Require >=5 unique C with >=3 per stratum for valid CMI/BF; also compute `H_K=2` sensitivity exploratory but primary BF is M1: P(S_next|S_current,A,R) vs M0: P(S_next|S_current,A) conditioned on C via Dirichlet-multinomial per stratum. History conditioning via C stratification already incorporates H_K=3. Report `H(S_next|C)` and `singleton_SA_rate`; require `H(S_next|C)>0.05` else degenerate ceiling => MEASUREMENT_INVALID (deterministic FSM where H=0 forces BC=0 a priori — prior TodoMVC det_ratio 0.846-0.944 produces this failure).
- Trajectory unit is `trajectory_id` (BrowserGym episode), not transition; correlated transitions within trajectory not treated as independent.

### 4.4 Genuine DOM (not SHA256 truncated) — operational definitions
- `R_visual`: AX bounding box (x,y,w,h quantized 10 bins each 0-1279/719 normalized) + element_count/tree_depth/interactive_density derived from dom_bytes (DOM.getDocument element count, max depth, interactive role density). Preserved as `visual_json` with bbox histogram.
- `R_computed_style`: 8-value computed CSS via CSS.getComputedStyleForNode on top-20 visible nodes: {color, backgroundColor, visibility, display, opacity, border, position, fontSize} quantized (color bins 16, opacity 10, etc.), aggregated as multiset per state. Preserved as `style_dict` with per-node values.
- `R_event_seq`: n-gram last 3 primitives (e.g., click->fill->click) diagnostic — expected near-constant on TodoMVC (BC~0).
- `R_AX_embedding`: Accessibility.getFullAXTree serialized sequence of (role, name, value) for up to 5k tokens per snapshot, then TRAIN-only (70/30 by trajectory_id) TF-IDF vocabulary or k-means 20 clusters (fit TRAIN only) over AX embedding vectors — never SHA256 truncation to 4 hex chars + state. Preserved raw `a11y_tree` bytes (>0) plus serialized JSON.
- Preservation: raw `dom_snapshot` (443 bytes proxy -> expect >1k real), `a11y_tree` (3971 bytes proxy -> expect >5k real), `visual_json`, `style_dict`, `event_seq`, `AX_bytes`; document quantization (10 bins, 8 styles, k=20, AX 5k). Primary requires >=1 R genuine with overlapping spectra verified (style/visual/AX distributions hist_intersection >0.3 not deterministic regime-color like red vs blue constant) and `|R|/N` in 0.01-0.30 (finite vocab genuine, not hash-unique nor constant).
- Viewport: locked 1280x720 via Playwright CDP `Page.setViewportSize` + `window.innerWidth/Height` check; verify `viewport == 1280x720` in provenance; mismatch => MEASUREMENT_INVALID substrate missing. Report `dom_bytes`, `a11y_bytes`, `visual_json` length, `computed_style` dict size.

## 5. Estimator, Bias Correction, Operationalization

- **Exact Dirichlet-Multinomial marginal likelihood** via `scipy.special.gammaln` and `scipy.special.polygamma` (digamma polygamma(0), trigamma polygamma(1)): for each stratum c with `N_c` observations and counts `n_i` over `K=n_states` (12 primary, 24 exploratory) with symmetric `alpha=1/K`: `log ML_c = gammaln(K*alpha) - gammaln(N_c + K*alpha) + sum_i [gammaln(n_i + alpha) - gammaln(alpha)]`. Sum over strata `c` partitioned by `C=(URL, H_K=3)`. Then `log ML(M1)` uses stratification by `(C,R)` vs `log ML(M0)` by `C` only? Director binding: `log BF = log ML(M1: S_next | C, R) - log ML(M0: S_next | C)` where both use same K, alpha, TRAIN-only Dirichlet counts by trajectory_id. Alternative operationalization per audit: stratified per-C counts fit on TRAIN only (70/30 by trajectory_id), test holdout scoring is exploratory. Primary gating uses TRAIN-only counts (no test leakage). Report for `alpha_prior` in {0.5,1.0,2.0} sensitivity, primary reporting at `alpha=1.0`. `log BF` in nats (natural log). Analytic null `mean/std` via exact Gamma-ratio using digamma/trigamma expectations under permutation null (closed-form sum of digamma ratios), not heuristic `0.015/0.035/0.005/0.35` constants nor `sqrt(mean_var)*0.35+0.008` nor `/100*0.1` blending. `BC = M_OBS - M_ANALYTIC_MEAN` in nats; also report `BC_bits = BC / ln(2)` diagnostic but gating on nats.
- Code path `research/physics/run_experiment.py::_dirichlet_multinomial_log_marginal` with `K=n_states` (not len(counts)), `alpha=1/K`, `gammaln` and `polygamma` calls verified via `grep gammaln` and `grep polygamma` logged in `provenance.json`. Audit verifies source contains `gammaln` and `polygamma` and does not contain heuristic constants `0.005 psi_correction`, `0.008 bias_stratum`, `0.35`, `0.022` nor `*10` fudge.
- **Permutation**: 1999 trajectory-grouped shuffles of genuine DOM labels (`R_before`) within each `C` stratum grouped by `trajectory_id` using `numpy seed42` deterministic; null distribution `M_NULL_MEAN/STD/MEDIAN/MAX`; `p_raw = (count_ge + 1)/2000` where `count_ge` is number of permuted log BF >= observed; `p_bonf = min(1, p_raw * n_tests)` with `n_tests <=8` (Bonferroni) floor `0.0005`; resampling unit is `trajectory_id` not transition; no Gaussian jitter; `calibrated_std = max(analytic_std, perm_std)` floor `0.005` analytic /`0.01` perm; consistency `M_CONS = |perm_mean - analytic_mean|` required `<0.03` on primary and controls. Permutation seeds deterministic across processes (`PYTHONHASHSEED=0`, `numpy seed42`).
- **Relative vs absolute BF discipline**: Report `M_OBS_BF` (absolute observed log BF), `M_REL_SEP = M_OBS - M_NULL_MEDIAN` (relative separation, must be >=200 nats), `M_BC = M_OBS - M_ANALYTIC_MEAN` (bias-corrected, >0.05), `M_ABSOLUTE_BF = M_OBS` explicitly labeled exploratory (expected -10 to -15 nats favoring memory at K12 on deterministic TodoMVC due to K over-penalty and `H~0`, not gating). Also compute plug-in CMI bits diagnostic but primary gating on BF nats. Distinguish measurement failure (G gates) from scientific negative (BC~0/rel_sep<200 with valid gates).
- **TRAIN-only Dirichlet counts**: Dirichlet posterior counts `n_i + alpha` fit on TRAIN only (70/30 split by `trajectory_id`); holdout test scoring exploratory; `site` identity never feature; leakage check `MI(DOM;Action)<0.10`.

## 6. Data Collection and Sampling

### 6.1 Trajectory banks
- **Primary WebShop**: BrowserGym WebShop at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 pinned) via CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode. Reuse existing WebShop/TodoMVC 1280x720 banks if manifest (`research/intel/manifest.json` or `codex/browsergym_manifest.json` or `provenance.browsergym_reuse`) shows `browsergym_reuse` with `dom_bytes>0 a11y_bytes>0 viewport 1280x720` and `N=1000-1999` (target 50 sessions x20-40 steps per site). Check `research/lanes/physics/state.json` dependencies.
- **Secondary TodoMVC**: BrowserGym TodoMVC same pipeline (richer genuine DOM vs prior SHA256 URL-only). Both banks `N=1000-1999` (if manifest available, use as-is; if not, collect new WebShop categories/search/cart/checkout and TodoMVC at locked 1280x720 with honest cost, no `*6.0` jitter, no hash truncation).
- **Positive control bank**: Synthetic 12-state stochastic hash-routed SPA N=5000 (50 sessions x100 steps) seed42 with 12 states, 4 candidates per (s,a), 50% hash routing +50% uniform random — same as EXP-PHYSICS-35578258358 — run offline with same exact estimator; no browser needed.
- **Independent-noise bank**: Same WebShop/TodoMVC FSM but action-state dependence destroyed via per-step independent within-trajectory shuffle of genuine DOM labels (regime-independent overlapping spectra, not `S_current%2`, same 1280x720 viewport, same K); identical DM + grouped perms 1999 seed42. Must show BC~0 with independent~0.
- **IID bank**: Same marginal `P(S)` i.i.d. with genuine DOM still sampled but `S_next` resampled i.i.d. seed42; identical DM + grouped perms.
- If banks not available and collection fails due to BrowserGym install/network, write `failure.json` with `status=BLOCKED`, category `BLOCKED`, message and smallest unblock action (e.g., `pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.63.0 && npx playwright install chromium`) and `retryable=true`, not falsification. Synthetic positive still runnable offline must be reported.

### 6.2 Collection details and adequacy
- `PYTHONHASHSEED=0`, `numpy seed42`, never `hash(site)`; `trajectory_id` as resampling unit; `VIEWPORT 1280x720` verified before claiming genuine (`dom_bytes>0 a11y_bytes>0 visual_json>0 computed_style>0` per snapshot). At least 100 NL transitions per bank or report `H(S_next|C)` and `|R|/N`; `H(S_next|C)<=0.05` => MEASUREMENT_INVALID ceiling not falsification. Report `N_transitions`, `N_strata`, `N_trajectories`.
- Honest cost: sum counters `resolve+bind+verify+freshness+browser_steps`, no `n*3200` or `*6.0` inflation, report `|rho_shuffled|<0.20` if applicable.
- Sampling integrity: BrowserGym trajectories as collected with AgentLab tool-use policy (click/fill/navigate) at 1280x720; action distribution not degenerate to constant click; verify `|A|>1` before analysis.
- Dependencies: runtime `BrowserGym 1280x720 CDP AX>10` trajectory banks `N=1000-1999` and intel `Gate0 production SPA census for |S|>=16 follow-up` — this experiment does not block on Gate0 discovery; it reuses existing BrowserGym banks.

## 7. Baselines and Controls

### 7.1 Baselines (stable identities for AUDIT reuse)
- **B-DOM-SIMILARITY-TFIDF-K5** (B-DOM-SIMILARITY): TF-IDF cosine `k=5` over genuine DOM text tokens (visual text + bbox quantized tokens + AX role/name/value tokens + 8 computed-style tokens) fit TRAIN only 70/30 by `trajectory_id`, 5-NN predicting `S_next` without `C` stratification; `BC_sim` via same exact Gamma-ratio `K` analytic+perm (gammaln/polygamma, alpha=1/K, K=n_states grouped trajectory_id 1999 perms seed42, analytic mean/std via gammaln/polygamma). Reports `BC_sim`, `p_bonf`, `|analytic_mean|`, `cons`, `rel_sep`. Primary must exceed by gap `G_DOM = M_BC - B_DOM_BC >=0.05` nats for beyond-similarity. Expected TF-IDF may capture ~0.02-0.16 nats if similarity explains variation; valid only if `|analytic|<0.1 cons<0.03` else invalid baseline. Prior proxy artifact: R-invariant `BC 0.142 P=1.0` identical across Rs due to single `dom_before_text` — rejected; this design fixes per-R genuine text.
- **B-MARKOV-1** (B-MARKOV-1): First-order Markov memory null `P(S_next | S_current, A_leakageFree)` MLE on TRAIN by trajectory_id without DOM; `BC_markov1` via same exact analytic DM `K` and 1999 trajectory-grouped perms seed42. Reports `BC`, `p`, `|analytic|`, `cons`, `rel_sep`. Required gap `G_MARKOV = M_BC - B_MARKOV_BC >=0.05` isolates genuine DOM beyond-Markov signal. Expected `-0.003` to `0.02` on deterministic TodoMVC if history sufficient; valid only if `|analytic|<0.1 cons<0.03`.
- **B-SHUFFLE-GROUPED-PERM**: trajectory-grouped 1999 within-`C` shuffles grouped by `trajectory_id` seed42 => perm `mean/std/median/max/p_raw/p_bonf` floor 0.0005; analytic `mean/std` via gammaln/polygamma digamma/trigamma for `|perm-analytic|<0.03` and `|analytic|<0.1` and `null_std>0.01`. Unit trajectory_id, no jitter, `calibrated_std=max(analytic_std,perm_std)` floor 0.005/0.01.
- **B-INDEPENDENT-NOISE-GENUINE**: independent per-step genuine DOM `>=6` variants/state same 1280x720 but regime-independent overlapping sampling (hist_intersection>0.3), identical DM + grouped perms 1999; `|BC|<0.05 p>0.10 |analytic|<0.1 cons<0.03` required else MEASUREMENT_INVALID confounded (G1).
- **B-IID-NULL**: i.i.d. `S_next` same marginal `P(S)` seed42; `|BC|<=0.05 p>0.10 |analytic|<0.1 cons<0.03` (G2).
- **B-TRAJECTORY-MEMORY diagnostics**: exact `(URL,H_K,Action)->S_next` memorization ratio, href-leakage gap (`action.target_href==state_after.url`), `MI(DOM;Action)<0.10`, `H(S_next|C)` ceiling, `|R|/N` cardinality, `singleton_SA_rate`.

### 7.2 Positive control
- **CTRL_POS_SYNTHETIC** (positive_control): Synthetic 12-state stochastic hash-routed SPA N=5000 (50x100 seed42, 12 states, 4 candidates per (s,a), 50% hash routing +50% uniform random) — same as EXP-PHYSICS-35578258358 audit PASS. Known validation at K12 alpha=1/K: alpha0.5 obs 643.09 null_median -78.36 p0.0005 floor, alpha1.0 obs 338.67 null_median -130.91 p0.0005, alpha2.0 obs 167.90 null_median -116.10 p0.0005, `|perm-analytic|<0.03` replication-exact, `|analytic|<0.1`, calibrated_std valid. Must replicate with exact DM K12 and trajectory-grouped 1999 perms seed42: observed log BF >>0 exceeds null median by >=200 nats, p_bonf<0.01, |analytic_mean|<0.1, calibrated_std valid, cons<0.03. Failure => MEASUREMENT_INVALID (pipeline blind/miscalibrated) and no primary claim. Also report K24 exploratory if `|S_next|>=16` and deterministic SPA log BF>>0 sanity. Locally-hosted 6-state overlapping proxy secondary not gating.

### 7.3 Null controls (stable identities)
- **CTRL_NULL_GROUPED_PERM** (null_control permutation): Trajectory-grouped 1999 perms seed42 on real banks, grouped by trajectory_id, within `C` strata; require `|analytic_mean|<0.1`, `calibrated_std>0.01` or analytic>0.005, `|perm-analytic|<0.03`, `p_bonf` floor 0.0005. Perm negativity alone not signal — must be validly centered.
- **CTRL_ANALYTIC_CENTERING**: `|analytic_mean|<0.1` on BF/BC scale, `consistency=|perm-analytic|<0.03`, calibrated valid; failure on primary => MEASUREMENT_INVALID (G4).
- **CTRL_INDEPENDENT_NOISE** (null_control independent): `|BC|<0.05 p_bonf>0.10 |analytic|<0.1 cons<0.03` valid; if `|BC|>=0.05 p<0.10` valid => MEASUREMENT_INVALID confounded (G1) — prior proxy independent p=0.056 violates p>0.10 license.
- **CTRL_IID_NULL**: `|BC|<=0.05 p>0.10 |analytic|<0.1 cons<0.03` (G2).
- Audit verifies source contains `gammaln` and `polygamma` and not heuristic `sqrt(mean(1/(2n)))` or `0.015/0.035/0.005/0.35` constants; `provenance.json` logs call sites via `grep`.

## 8. Measurement Validity (pre-registered gates G0-G6)

All listed in `spec.json measurement_validity` and reiterated:

- **Substrate locked 1280x720**: via Playwright CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode at pins 0.14.3/0.4.2/1.63.0. Reuse BrowserGym WebShop/TodoMVC banks if manifest shows dom_bytes>0 a11y_bytes>0 viewport 1280x720 N=1000-1999; else collect new. Verify viewport and overlapping spectra hist_intersection>0.3 (not SHA256 hash-truncated single value). Preserve raw dom_snapshot/a11y_tree/visual_json/style_dict/event_seq/AX_bytes; document quantization/viewport. Mismatch or dom_bytes==0 => G5 MEASUREMENT_INVALID.
- **State S_next**: `SHA256(normalize(URL_after)|'|'|normalize(title_after)|'|'|DOM_cluster_if_needed)` keep SPA hash fragment `#/` for TodoMVC; report `|R|/N`, `H(S_next|C)`, `|S_next|`. K12 primary; if `|S_next|>=16` trigger K24 exploratory same alpha=1/K. Also report per-R cardinalities. Verify not tautological with action (MI<0.10).
- **Action**: `A_leakageFree=(primitive,target_sig)` never href/URL/src; diagnostic A_leaky gap only. Verify `|A|>1` and `MI(DOM;Action)<0.10` else G3 degenerate. Require H_K=3 strata `C=(URL_before, H_K=3)` >=5 unique C >=3 per stratum; `singleton_SA_rate<70%`; `H(S_next|C)>0.05` else G3 degenerate ceiling (deterministic FSM where H=0 forces BC=0 a priori — not falsification).
- **DOM genuine**: visual bbox 10 bins + element_count/tree_depth/interactive_density; computed 8 styles; event n-gram 3 diagnostic; AX serialized 5k + TRAIN-only k-means 20 not SHA256 truncated. Primary requires >=1 R genuine with overlapping spectra and `|R|/N` 0.01-0.30.
- **Estimator exact**: gammaln/polygamma closed-form sum_c[...] with K=n_states NOT len(counts), alpha=1/K, TRAIN-only counts by trajectory_id, log BF nats, analytic null via digamma/trigamma without heuristics. Code path `research/physics/run_experiment.py` with grep verification. Plug-in CMI bits diagnostic not gating.
- **Permutation**: 1999 trajectory_id grouped within-C shuffles seed42, p_bonf n_tests<=8 floor 0.0005, calibrated_std floor 0.005/0.01, cons<0.03 required on primary AND controls (G4). No Gaussian jitter.
- **Split integrity**: TF-IDF vocab/embedding centroids/Dirichlet counts/k-means fit TRAIN only 70/30 by trajectory_id; holdout gaps; site identity never feature.
- **Sampling/uniqueness/representation**: PYTHONHASHSEED=0 seed42 never hash(site); trajectory_id unit; raw preserved/losses documented; MI<0.10; genuine vs SHA256 distinguished; overlapping required.
- **Absolute vs relative discipline**: Absolute BF -10 to -15 exploratory not gating; primary is relative sep >=200 nats + BC>0.05 p<0.01 gap>=0.05 with independent~0. Must report both and label absolute exploratory.
- **Auditability**: raw transitions, genuine DOM JSON, strata tables, perm+analytic distributions committed sha256 in provenance.json; freeze hashes verified; viewport verified; gammaln/polygamma call sites logged.
- **Gate hygiene**: G0 synthetic positive M_REL_SEP>=200 p<0.01 |mean|<0.1 cons<0.03; G1 independent BC~0; G2 IID BC~0; G3 degenerate ceiling H>0.05 N>=100 etc.; G4 primary |perm-analytic|<0.03; G5 substrate viewport genuine; G6 TRAIN trajectory_id. Any fails => MEASUREMENT_INVALID. Cognitive reset: barrier/committor/timescale de-scoped (PARKED) to focus on Bayesian DM smallest high-information step.

## 9. Decision Rule (frozen, verbatim from `spec.json decision_rule`)

Gated execution in order; any validity gate triggers MEASUREMENT_INVALID and prevents primary SURVIVES/FALSIFIED claim.

Gates (MEASUREMENT_INVALID if any fail):
- G0 synthetic positive: `M_OBS<=0 OR p_bonf>=0.01 OR |analytic_mean|>=0.1 OR calibrated_std degenerate (analytic_std<=0.005 and perm_std<=0.01) OR |perm-analytic|>=0.03` => pipeline blind/miscalibrated.
- G1 independent-noise: `|BC|>=0.05 and p_bonf<0.10` with valid `|analytic|<0.1 cons<0.03` => confounded.
- G2 IID null: `|BC|>0.05 p<0.10` valid => null miscentered.
- G3 degenerate ceiling: `H(S_next|C)<=0.05 OR N<100 OR <5 strata with >=3 OR |R|/N outside 0.01-0.30 OR |A|<=1 OR MI(DOM;Action)>=0.10 OR singleton_SA_rate>=70%` => degenerate.
- G4 primary `|perm-analytic|>=0.03` on primary K12 both banks => model mismatch.
- G5 viewport/DOM genuine fails (no dom_bytes/visual/computed/AX >0 OR viewport !=1280x720 OR SHA256 truncation detected) => substrate missing.
- G6 TRAIN leakage or trajectory_id not used => split invalid.

If no G fails, primary per real-Web bank (WebShop primary, TodoMVC secondary) for K12 (and K24 if `|S_next|>=16`): compute `M_OBS_BF, M_NULL_MEDIAN/MEAN/STD/MAX, M_ANALYTIC_MEAN/STD, M_CONS=|perm-analytic|, M_REL_SEP=OBS-NULL_MEDIAN, M_BC=OBS-ANALYTIC_MEAN, M_ABSOLUTE_BF=OBS, p_raw=(count_ge+1)/2000, p_bonf=min(1,p_raw*n_tests) n_tests<=8 floor 0.0005, gaps G_DOM=M_BC-B_DOM_BC, G_MARKOV=M_BC-B_MARKOV_BC`.

`sig(bank,K,R)=1` if `M_BC>0.05 AND p_bonf<0.01 AND M_REL_SEP>=200 AND |analytic_mean|<0.1 AND calibrated valid (>0.005 analytic or >0.01 perm) AND cons<0.03 AND G_DOM>=0.05 AND G_MARKOV>=0.05 AND independent~0 (|M_BC_INDEPENDENT|<0.05 p>0.10 |analytic|<0.1 cons<0.03) AND |R|/N 0.01-0.30`.

If EXISTS bank,R with sig==1 (on K12, or K24 if triggered where `|S_next|>=16`) => SURVIVES_CURRENT_TEST — exact-centered genuine DOM beyond-memory signal detected, C-WEB-DYNAMICS supported bounded to that bank/K/R, absolute BF reported exploratory (-10 to -15 expected) but not gating. Must also show B-DOM-SIMILARITY and B-MARKOV-1 individually valid (`|analytic|<0.1 cons<0.03`) else gap not licensed.

If FORALL banks/R sig fails while gates pass => FALSIFIED-IN-SETTING — even correctly centered genuine DOM remains BC~0/rel_sep<200 or gap<0.05 while independent~0 and null centering valid, indicating no beyond-memory signal at N=1000-1999 with this scale/representation; physics should remain PARKED pending larger production manifest with session/permission regimes and `|S|>=16`. Bounded to N=1000-1999 genuine BrowserGym banks at 1280x720 with exact Gamma-ratio.

K24 exploratory consistency reported but not gating unless K12 sig already (same thresholds). SITE pooling across WebShop+TodoMVC exploratory only, not primary.

## 10. Primary Metrics (stable identities for AUDIT reuse)

For each bank (WebShop primary, TodoMVC secondary), each alpha {0.5,1.0,2.0} primary 1.0, each K {12 primary, 24 exploratory if `|S_next|>=16`}, each R {VISUAL, COMPUTED, AX, EVENT}:

- `M_OBS_BF_K12`, `M_OBS_BF_K24` (nats, absolute log BF)
- `M_ABSOLUTE_BF_K12 = M_OBS_BF_K12` (exploratory, -10 to -15 expected on TodoMVC deterministic)
- `M_NULL_MEDIAN_K12`, `M_NULL_MEAN_K12`, `M_NULL_STD_K12`, `M_NULL_MAX_K12`, `M_ANALYTIC_MEAN_K12`, `M_ANALYTIC_STD_K12`, `M_CONSISTENCY_K12 = |perm_mean - analytic_mean|` (nats, cons<0.03)
- `M_BC_BF_K12 = M_OBS - M_ANALYTIC_MEAN` (nats, must be >0.05), `M_BC_BITS_K12 = M_BC_BF_K12 / ln(2)` (bits diagnostic, not gating)
- `M_REL_SEP_K12 = M_OBS - M_NULL_MEDIAN` (nats, must be >=200)
- `M_P_RAW_K12`, `M_P_BONF_K12` (Bonferroni n_tests<=8 floor 0.0005, must be <0.01)
- `M_GAP_DOM_K12`, `M_GAP_MARKOV_K12` (nats, must be >=0.05 each)
- `M_CALIBRATED_STD_K12 = max(analytic_std, perm_std)` (floor 0.005/0.01)
- `M_INDEPENDENT_BC_K12`, `M_INDEPENDENT_P_K12`, `M_INDEPENDENT_ANALYTIC_MEAN_K12`, `M_INDEPENDENT_CONS_K12`, `M_INDEPENDENT_REL_SEP_K12`
- `M_IID_BC_K12`, `M_IID_P_K12`, `M_IID_ANALYTIC_MEAN_K12`, `M_IID_CONS_K12`
- `M_BASELINE_DOM_TFIDF_K5_BC_K12`, `M_BASELINE_DOM_TFIDF_K5_P_K12`, `M_BASELINE_DOM_TFIDF_K5_ANALYTIC_K12`, `M_BASELINE_DOM_TFIDF_K5_CONS_K12`, `M_BASELINE_DOM_TFIDF_K5_REL_SEP_K12`
- `M_BASELINE_MARKOV1_BC_K12`, `M_BASELINE_MARKOV1_P_K12`, `M_BASELINE_MARKOV1_ANALYTIC_K12`, `M_BASELINE_MARKOV1_CONS_K12`
- `M_H_SNEXT_GIVEN_C_K12`, `M_R_OVER_N_K12`, `M_R_VISUAL_OVER_N`, `M_R_COMPUTED_OVER_N`, `M_R_AX_OVER_N`, `M_SINGLETON_SA_RATE_K12`, `M_N_TRANSITIONS_K12`, `M_N_STRATA_K12`, `M_A_CARDINALITY_K12`, `M_MI_DOM_ACTION_K12`
- `M_VIEWPORT`, `M_DOM_BYTES_MEAN`, `M_A11Y_BYTES_MEAN`, `M_OVERLAP_HIST_INTERSECTION`
- Corresponding K24 metrics suffixed `_K24` if triggered; per-R variants suffixed `_VISUAL`/`_COMPUTED`/`_AX`/`_EVENT`. Stable control IDs: `CTRL_POS_SYNTHETIC`, `CTRL_NULL_GROUPED_PERM`, `CTRL_INDEPENDENT_NOISE`, `CTRL_IID_NULL`, `B-DOM-SIMILARITY-TFIDF-K5`, `B-MARKOV-1`, `B-SHUFFLE-GROUPED-PERM`.

All baselines/controls use same K, alpha, grouping, n_tests, and exact gammaln/polygamma analytic as primary; gaps computed on same bank/K/R with same units (nats). Bit/nat conflation forbidden — report bits diagnostic only.

## 11. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Deterministic FSM (TodoMVC det_ratio 0.846-0.944, H~0): H(S_next|C) near 0, perm null heavily negative, absolute BF -10 to -15 favoring memory due to K=12 over-penalty on |S|=3-4** | Report H(S_next|C) per bank; require H>0.05 else G3 MEASUREMENT_INVALID ceiling not falsification; WebShop bank provides stochastic heterogeneity (categories/search/cart); acknowledge absolute BF negative exploratory; primary is relative sep >=200 + BC>0.05 with independent~0 guard, not absolute. Trigger K24 only if |S|>=16 where K penalty less harsh. |
| **K=12 over-penalty on S=3-4: BF -10 to -15 even when relative signal exists** | K12 frozen primary; report K12 absolute exploratory; gaps use same K so penalty cancels; relative sep >=200 is scale-invariant to penalty but requires stochasticity. Document penalty explanation per EXP-PHYSICS-35578258358. |
| **Isomorphic replication inflating n (vanillajs/react/svelte bit-identical): Effective replications 2 not 5** | Treat WebShop vs TodoMVC as distinct banks; do not pool 5 TodoMVC variants as independent; gate on bank level; note isomorphism in report. |
| **Genuine DOM vs SHA256 truncation collapse (VF-RAX-SHA256)** | Verify dom_bytes>0 a11y_bytes>0 visual bbox+computed 8-value+AX 5k preserved; audit grep checks source contains gammaln/polygamma not SHA256-only truncation; report \|R\|/N 0.01-0.30 genuine finite vocab with overlapping hist >0.3 vs deterministic. |
| **Viewport heterogeneity 1024 vs 1280 changes bbox normalized coordinates** | Lock 1280x720 via CDP Page.setViewportSize + window.innerWidth check; verify viewport in provenance; reject if !=1280x720 => G5 MEASUREMENT_INVALID. |
| **Trajectory grouping vs transition-level shuffle inflates p / heuristic analytic masquerading as exact** | Enforce trajectory_id unit, 1999 perms seed42, cons<0.03 guard; require exact gammaln/polygamma closed-form sum_c[...] and digamma/trigamma without 0.015/0.035/0.005/0.35 constants; audit grep verification; independent-noise BC~0 confirms not S_current%2 leakage. |
| **Heuristic bias correction (0.005 psi, 0.008 bias_stratum, 0.35 scaling, *10 fudge)** | Forbid heuristic blending; require closed-form Gamma-ratio; provenance logs grep sites; prior heuristic proxy audit VF-HEURISTIC-ANALYTIC-NOT-EXACT rejected — this design mandates exact. |
| **Multiple testing inflation (n_tests<=8 isomorphic Rs effective 1-2)** | p_bonf=min(1,p_raw*n_tests) floor 0.0005; note effective 2-3 for colinear Rs; report both p_raw and p_bonf; Bonferroni conservative. G_DOM/G_MARKOV gaps computed per-R not pooled. |
| **Small N (80 NL prior) vs target 1000-1999 power limited** | Require N>=100 valid per bank H>0.05; WebShop/TodoMVC manifest should provide >=1000; else if N<100 report G3 MEASUREMENT_INVALID ceiling not falsification; acknowledge power. |
| **Action encoding degeneracy (\|A\|=1 constant click)** | Use A_leakageFree never href; verify \|A\|>1 and MI(DOM;Action)<0.10; report degenerate_action diagnostic log BF 0 if fails => G3 MEASUREMENT_INVALID. |
| **BrowserGym installation/network unavailable** | Write failure.json BLOCKED with retryable unblock (pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.63.0 + npx playwright install chromium); not falsification. Synthetic positive still runnable offline. |
| **Absolute BF gating confusion (6-state proxy BC 0.158 rel_sep 317 bit-nat conflation)** | Enforce discipline: absolute BF exploratory only; primary gating is relative sep >=200 + BC>0.05 + p<0.01 + gaps; document both; label bits diagnostic. Prior proxy gap_dom 0.016<0.05 correctly rejected. |
| **TF-IDF baseline R-invariant (single dom_before_text) and Markov hardcoded -0.003** | Implement genuine per-R TF-IDF k5 TRAIN-only 70/30 over visual+AX+style tokens fit per-R, not single text; Markov MLE on TRAIN by trajectory_id not hardcoded. Prior artifacts bounded rejected. |
| **Independent p=0.056 violations and perm-analytic heuristic cons 0.0357** | Require exact analytic and p>0.10 license plus cons<0.03 on both independent and IID and primary; otherwise G1/G4 MEASUREMENT_INVALID. |
| **K24 over-penalty and consistency generalization** | Report K24 exploratory only; require same cons<0.03 and valid centering; not gating unless K12 sig already but document. |

## 12. Product Consequences

- **Positive (SURVIVES with valid exact centering |analytic|<0.1 cons<0.03 and relative sep >=200 nats p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov-1 with independent~0 on >=1 real BrowserGym bank at 1280x720)** : First real-Web Bayesian beyond-memory measurement-validity replication despite absolute BF -10 to -15 favoring memory. Bridges the 70+ experiment synthetic→real gap that blocked C-WEB-DYNAMICS (all prior HYPOTHESIS/MEASUREMENT_INVALID/BLOCKED, 0 real-Web beyond-memory hits, 6 Laplace-biased families). Justifies UNPARKING Physics for production manifest with real session/permission latent regimes and larger state spaces (|S|>=16 triggering K24) where |S| cardinality supports K24 and session diversity may increase H(S_next|C). Product: distill validated exact Bayesian DM as freshness/barrier guard candidate (regime-aware retrieval grouped by latent DOM cluster, visual+AX signature, event-seq guard) into kernel `resolve/verify`; quantify delta-repair and cross-site holdout transfer at K12/K24 with exact correction; measure work-compression via regime detection vs strong baselines (RAG, Stagehand, SGDR). No generic promotion until transfer validated; report absolute BF separately exploratory; update `research/lanes/physics/state.json` to CONTINUE with next_question toward production manifest.

- **Negative (FALSIFIED-IN-SETTING with valid gates: null centering valid |mean|<0.1 cons<0.03 std>0.01 but BC~0 / rel_sep<200 / gap<0.05 while independent~0 holds on both banks at N=1000-1999)** : Closes Bayesian beyond-memory measurement-validity program on existing BrowserGym WebShop/TodoMVC at N=1000-1999 with genuine DOM at 1280x720 at K12 (and K24 if triggered) even correctly centered — exactly-centered genuine DOM shows no beyond-memory signal. Combined with 70+ prior HYPOTHESIS, -15 nats absolute, frontier density blind spots (kNN scaling rho -0.12, KDE rotation 0.286, CV 0.57-0.75), barrier BC 0.171<0.30 gap 0.011, and 6 Laplace families failing |null|<0.1, confirms estimator does not generalize beyond synthetic 12-state SPA to real Web at this scale/representation and physics should remain PARKED pending larger production manifest with real session/permission latent regimes and larger state spaces |S|>=16; Frontier should pivot to orthogonal MemoryArena/WebAPI-bypass/tool-compilation/alias-catalog per runtime dependencies and Director comparative reasoning (vs weighted PMI variants). SPIDER must NOT invest in DOM Bayesian beyond-memory detection as mechanical prior at current N/scale. Graph/Product continue via retrieval/verification/repair amortization for C-RESIDUAL-NOVELTY. Bounded falsification at N=1000-1999 genuine banks with exact Gamma-ratio, not global Web closure; C-WEB-DYNAMICS remains HYPOTHESIS not REJECTED globally, C-MEAS-VALID stays EXPERIMENTAL/MEASUREMENT_INVALID not REJECTED globally. No silent threshold lowering.

## 13. Estimated Cost / Expected Information Gain

- **Estimated cost**: Low: reuses existing BrowserGym trajectory banks (WebShop/TodoMVC at 1280x720 if available per intel manifest — no new LLM, no network beyond localhost replay for synthetic positive) plus optional locally-hosted 6-state overlapping proxy genuine capture at 1280x720 via CDP (<10 min headless) only if banks missing. Analysis: exact Dirichlet-Multinomial via gammaln/polygamma + 1999 trajectory-grouped perms x (1 synthetic positive N=5000 +1 WebShop primary N=1000-1999 +1 TodoMVC secondary +1 independent +1 IID) x 3 alpha {0.5,1.0,2.0} x 2 K (12 primary, 24 exploratory if |S|>=16) x 4 genuine Rs x 3 baselines <5 min wall-clock per bank; scipy+sklearn+headless Chromium if needed; total <2h wall-clock, <8GB RAM, no GPU, stdlib+scipy+sklearn. Honest cost sum counters not n*3200.

- **Expected information gain**: Very high and tunnel-breaking per Director comparative reasoning: vs CONTINUE barrier/committor/timescale on non-existent Gate0 SPAs (0/2 pass titles>=2/H>0.2/leakage<40%/NL>=50, H(S_next|URL,H_K=3)=0 forces BC=0 a priori — expected BLOCKED/MEASUREMENT_INVALID again, zero info gain), vs PARK entirely (abandons leverage), vs continuing another weighted/equal/median/KNN/KSG/LR PMI variant (6 families already falsified |null|<0.1 biased floor 0.4-0.7 bits — rejected), vs C-CROSSSITE holdout owned by Intel, this low-cost real-bank Bayesian DM K12 test is the only estimator to pass C1 (null median<0) and C3 (p<0.001) on synthetic SPA (168-643 nats exceeding 99.9th percentile by 194-669 nats, audit PASS) and directly tests synthetic→real generalizability at N=1000-1999 with richer DOM spectra (bbox 10 bins + 8 computed styles + AX 5k TRAIN k-means 20) and trajectory-grouped permutation with valid null centering before committing to larger |S|>=16 manifest. Positive (rel_sep>=200 p<0.01 gap>=0.05 valid centering independent~0) establishes first real-Web measurement-valid beyond-memory estimator despite absolute -10 to -15; persistent BC~0/rel_sep<200 with valid centering justifies remaining PARKED and pivoting Frontier to orthogonal ensemble. Orthogonal falsifiable program per C-WEB-DYNAMICS next_gate (orthogonal falsifiable programs on effect factorization, barriers, timescales, geometry, multiscale dynamics) and first real-Web test needing no new site discovery (70+ prior HYPOTHESIS, 0 real-Web beyond-memory hits, tunnel_flag true). DIRECTLY INFORMATIVE for Global Director UNPARK/PARK decision and Frontier/Intel allocation.

## 14. Inherited Parent Handoff Carry-Forward (exact, USE disposition per Director — preserved distinctions)

### Established (from EXP-PHYSICS-35915247766, preserved per USE)
1. Synthetic 12-state stochastic hash-routed SPA machinery replays bit-identically: WebShop visual bf_obs -135.4498294155651 null median -452.5088904456311 rel_sep 317.059061030066 p_bonf 0.004 analytic 0.014758 cons 0.019633 calibrated 0.082 valid; TodoMVC bf_obs -163.11571591811798 rel_sep 286.8625395819681; synthetic visual bf_obs 609.8101947698487 null median -414.06438521311975 rel_sep 1023.8745799829685 bc 0.2746 p 0.004 cons 0.0186. Bounded to locally-hosted 6-state proxy N=1900 and synthetic N=5000, not proof of exact Gamma-ratio centering (analytic heuristic per audit required_fixes 1-9).
2. Locally-hosted 6-state overlapping genuine proxy at locked 1280x720 validated: 36 prototypes (state0-5 x regime A/B x variant0-2) dom_bytes 443 a11y_bytes 3971 viewport 1280x720 verified via Playwright CDP, hist_intersection_color 0.667 mean_overlap 0.399 >0.3 not deterministic, H(S_next|C) 2.316/2.336 bits >0.05 valid ceiling, 30 strata >=3, |R_visual|/N 0.017-0.018, MI 0.013 <0.10 not tautology, singleton SA 0.0, N=1900. Bounded to proxy, not real BrowserGym heterogeneity.
3. Trajectory-grouped permutation null (1999 perms seed42 by trajectory_id) and observed log BF computation reproducible: auditor replay matches producer exactly on raw_transitions_webshop.json. Independent-noise and IID controls BC -0.015 to 0.025 p 0.056-1.0 show no strong confounding on BC scale but p=0.056 violates p>0.10 license and heuristic cons borderline. Bounded to proxy.
4. Physics beyond-memory program remains PARKED: 70+ C-WEB-DYNAMICS HYPOTHESIS with 0 real-Web beyond-memory hits, 8-streak barrier PARK, Bayesian K12 first to pass C1+C3 synthetic but absolute BF -10 to -15 favors memory on deterministic TodoMVC — relative separation UNMEASURED on real BrowserGym banks.
5. Viewport and overlapping spectra capture pipeline verified at 1280x720 with CDP: visual bbox + 8 computed styles + AX serialized overlapping hist >0.3, raw preserved. Bounded to proxy prototype generation, not production latent regimes.
6. Real TodoMVC N=80/variant also passed but 2 effective FSM types and absolute BF -10 to -16 favoring memory, synthetic->real gap dominant uncertainty — this N=1000-1999 test closes gap.

### Rejected (bounded, preserved)
- Locally-hosted 6-state constant-action proxy as valid test of real BrowserGym beyond-memory dynamics — bounded rejection (audit VF-SUBSTRATE-SUBSTITUTION, browsergym_reuse MISSING).
- Heuristic analytic with magic constants as exact Gamma-ratio — bounded rejection (VF-HEURISTIC-ANALYTIC-NOT-EXACT, L178-233).
- Hardcoded B-MARKOV-1 BC -0.003 and TF-IDF k5 BC 0.142 R-invariant as valid baselines — bounded rejection (VF-BASELINE-MARKOV1-HARDCODED, VF-BASELINE-INVALID, n_perms 500).
- R_visual/R_computed_style/R_AX bit-identical as three independent evidences — bounded rejection (VF-PER-R-IDENTITY-NOMINAL, n_tests overcounts).
- R_AX sha256[:4]+state as genuine AX 5k TRAIN k-means 20 — bounded rejection (VF-RAX-SHA256-TRUNCATES-EMBEDDING).
- That BC 0.158 p 0.004 rel_sep 317 with gap 0.016 demonstrates valid beyond-memory — bounded rejection (gap<0.05, p 0.056 fails).
- Synthetic positive not frozen-calibrated — bounded rejection (VF-SYNTHETIC-POSITIVE-NOT-FROZEN-CALIBRATION).
- That MEASUREMENT_INVALID falsifies C-WEB-DYNAMICS globally — bounded rejection (claim_ceiling MEASUREMENT_INVALID UNMEASURED).

### Unknown (must not assume, preserved + updated)
- Whether real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 via CDP) exist or can be collected in this environment (provenance browsergym_reuse MISSING in parent) and what H(S_next|C), |R|/N 0.01-0.30, |A|>1, MI<0.10, title/session heterogeneity they would show at N=1000-1999.
- What exact closed-form DM log BF in nats (K=n_states=12/24 alpha=1/K gammaln/polygamma digamma/trigamma) observed/null/analytic mean/std/p_bonf/gap would be on real banks with trajectory_id grouping and TRAIN-only DM counts, and whether G4 |perm-analytic|<0.03 would pass and independent~0 (|BC|<0.05 p>0.10) would hold.
- Whether correcting analytic to exact Gamma-ratio sum_c[gammaln(Kalpha)-gammaln(N+Kalpha)+sum_i gammaln(n_i+alpha)-gammaln(alpha)] with polygamma variance and implementing genuine per-R TF-IDF k5 TRAIN-only 70/30 and Markov MLE would change BC/gap by >0.03 and flip consistency on independent/IID nulls.
- Whether larger production manifest with real session/permission latent regimes, larger state spaces |S_next|>=16 triggering K24, richer multi-feature genuine DOM (visual bbox 10 bins + 8 computed styles + AX embedding 5k combined without tautology) and non-degenerate action set would achieve BC>0.05 gap>=0.05 rel_sep>=200 or remain BC~0.
- Whether Bonferroni n_tests<=8 floor 0.0005 overcounts isomorphic visual/style/AX (effective 1-2) and how K24 consistency generalizes at real scale.
- Independent-noise residual BC 0.0249 p 0.056 and synthetic null_median -414 vs frozen calibration -78..-131 mismatch origin.

### Do Not Assume (unsafe, preserved)
- Do not assume C-WEB-DYNAMICS or C-MEAS-VALID falsified globally — this packet is MEASUREMENT_INVALID UNMEASURED on real BrowserGym; 70-attempt streak remains HYPOTHESIS/EXPERIMENTAL not REJECTED.
- Do not assume heuristic analytic with magic constants is exact Gamma-ratio centering.
- Do not assume BC 0.158 p 0.004 rel_sep 317 with gap 0.016 demonstrates beyond-memory barrier/timescale.
- Do not assume TF-IDF k5 BC 0.142 proves beyond-similarity or hardcoded -0.003 Markov proves beyond-Markov — both invalid per audit.
- Do not assume R_visual/computed_style/AX bit-identical are three independent evidences.
- Do not assume null negativity or small p proves structure — absolute BF -135 favors memory due to K penalty, not informative.
- Do not assume AX hash-truncated or constant event_seq evidences genuine semantics.
- Do not assume frozen 200-nat or 0.05 BC thresholds silently lowerable — calibrated on synthetic 168-643 nats.
- Do not assume locally-hosted 6-state proxy with 443-byte prototypes generalizes to production WebShop/TodoMVC.
- Do not assume trajectory-grouped |perm-analytic|<0.03 on primary alone validates pipeline — independent/IID cons must also be <0.03 and TRAIN-only DM required.

## 15. Preregistration Freeze Checklist

- [ ] `spec.json` frozen with above question/hypothesis/falsifier/baselines/positive_control/null_control/measurement_validity/decision_rule and stable metric/control identities (M_OBS_BF_K12, M_BC_BF_K12, M_REL_SEP_K12, |null_mean|<0.1 null_std valid cons<0.03 rel_sep>=200 p_bonf<0.01 gap>=0.05 independent~0 absolute exploratory -10 to -15)
- [ ] `prereg.md` (this file) frozen with above exact gammaln/polygamma closed-form, 1999 trajectory-grouped perms seed42, genuine 1280x720 verification (visual bbox 10 bins + 8 computed styles + AX 5k TRAIN-only k-means 20 not SHA256-truncated, TRAIN-only Dirichlet counts by trajectory_id), gates G0-G6, validity threats, absolute vs relative discipline, H>0.05 |R|/N 0.01-0.30 TRAIN-only trajectory_id grouping, cognitive_reset true, inherited distinctions preserved
- [ ] `request.json` director_mandate stored immutable with agent_priors_used[5] distinguished from SPIDER evidence, allocation CONTINUE C-WEB-DYNAMICS, dependencies noted
- [ ] `freeze.json` deterministic hashes of request.json + spec.json + prereg.md before EXECUTE (freezer code, not research agent)
- [ ] No outcome-bearing measurements inspected during DESIGN (synthetic positive control numbers are parent evidence from EXP-PHYSICS-35915247766 and EXP-PHYSICS-35578258358, not this experiment's outcomes)
- [ ] Dependencies: runtime BrowserGym 1280x720 CDP AX>10 N=1000-1999 trajectory banks and intel Gate0 production SPA census for |S|>=16 noted but not blocking this reuse-bank experiment; failure.json BLOCKED if substrate unavailable
- [ ] Physics validity gate: target/split/sampling/uncertainty/representation integrity pre-declared per SPIDER_MASTER_PROMPT.md §18

## 16. References

- Parent handoff: `research/experiments/EXP-PHYSICS-35915247766/handoff.json` sha256 b70f9f2afa436bb4dd8a4aed34b99cb425eb9795f867d7d4c9396ec8115226ab (MEASUREMENT_INVALID, parent_handoff_disposition USE per Director)
- Parent spec/prereg: `research/experiments/EXP-PHYSICS-35915247766/spec.json` `prereg.md` (exact gammaln/polygamma 1280x720 genuine trajectory_id grouping)
- Grandparent: `research/experiments/EXP-PHYSICS-35903177055/handoff.json` sha256 61e860a4e18a4b1fb4f335ec374dcd559610166709032feac97eec4a3f893971
- Director mandate: `research/experiments/EXP-PHYSICS-35938359115/request.json` director_mandate CONTINUE C-WEB-DYNAMICS cognitive_reset true cycle_id 35937950227
- Synthetic Bayesian validated: `research/experiments/EXP-PHYSICS-35578258358` (SURVIVES synthetic K12 exact, 168-643 nats, audit PASS, only estimator to pass C1+C3)
- Real TodoMVC Bayesian N=80: `research/experiments/EXP-PHYSICS-35651906573` (SURVIVES synthetic-bounded but absolute -10 to -15 nats real, isomorphic 2 effective) — synthetic->real gap
- Barrier exact audit: `research/experiments/EXP-PHYSICS-35860320716` (MEASUREMENT_INVALID BC 0.171<0.30 gap 0.011 exact valid centering) and `research/experiments/EXP-PHYSICS-35915247766/audit.json` (MEASUREMENT_INVALID required_fixes 1-9 VF-SUBSTRATE etc., claim_ceiling proxy-bounded)
- Physics state: `research/lanes/physics/state.json` (PARKED, active_experiment EXP-PHYSICS-35938359115, last_verdict MEASUREMENT_INVALID, next_question verbatim)
- Codex: `codex/index.json` and `codex/claim_state.json` (C-WEB-DYNAMICS HYPOTHESIS 70+ attempts, 0 real-Web beyond-memory hits) and `research/claims/registry.json` C-WEB-DYNAMICS HYPOTHESIS next_gate orthogonal falsifiable programs
- Code reuse: `research/physics/run_experiment.py::_dirichlet_multinomial_log_marginal` (K=n_states), `research/physics/execute_35915247766.py` (heuristic analytic rejected — must replace with exact), `research/physics/execute_35860320716.py` analytic_dm_mean_std_exact (heuristic rejected)
- Substrate pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, honest cost no *6.0 jitter |rho_shuffled|<0.20, PYTHONHASHSEED=0 seed42, never hash(site)
- Lane registry: `research/lanes/registry.json` physics priority_claims [C-MEAS-VALID, C-WEB-DYNAMICS, C-CROSSSITE]

---
*End of preregistration. EXECUTE must run exactly this frozen design, preserving raw evidence -> observation -> derived measurement -> interpretation distinction, with `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved` in `result.json`. Product lane scope not used. Never git commit/push/switch/reset. Fix all 9 audit required_fixes from EXP-PHYSICS-35915247766: FIX-SUBSTRATE (real BrowserGym banks not 6-state proxy), FIX-METRIC (exact BF/BC nats not bits*ln2), FIX-ANALYTIC-EXACT (remove 0.005/0.008/0.022/0.35 heuristic), FIX-ACTION-DEGENERACY (|A|>1), FIX-AX-REPRESENTATION (serialized AX 5k TRAIN-only k-means 20 not sha256), FIX-BASELINE (genuine per-R TF-IDF k5 TRAIN-only 70/30 1999 perms and Markov MLE), FIX-TRAIN (DM counts TRAIN-only), FIX-CONSISTENCY (|perm-analytic|<0.03 on all banks), FIX-SHA256-TRUNCATION.*
