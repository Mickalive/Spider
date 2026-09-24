# EXP-PHYSICS-35952152826 — Preregistration (DESIGN ONLY)

## Status
DESIGN ONLY — not yet frozen. No outcome-bearing measurements have been inspected. Preregistration will be hashed in `freeze.json` before EXECUTE. This is a NEW governed experiment with Director REOPEN on C-WEB-DYNAMICS (allocation REOPEN, cognitive_reset=false, cycle_id 35951734014, parent_handoff_disposition USE). The inherited parent_handoff is continuity evidence only per AGENTS.md precedence and MUST NOT silently override the Director's REOPEN strategic question. Thresholds are frozen; no post-hoc lowering.

## Experiment Identity
- **experiment_id**: EXP-PHYSICS-35952152826
- **lane**: physics
- **claim_ids**: ["C-WEB-DYNAMICS"]
- **parent_handoff**: `research/experiments/EXP-PHYSICS-35938359115/handoff.json` sha256 `752b1b06e2ba913a8f56a0f8f8299b23129d6a0b742cafad9d83c46c97c10548` (disposition USE)
- **director_mandate**: REOPEN on C-WEB-DYNAMICS, cognitive_reset=false, comparative_reasoning verbatim in request.json, dependencies [runtime BrowserGym 0.14.3 + Playwright 1.63.0 1280x720 CDP AX visual bbox+computed styles substrate], question verbatim below, rationale verbatim in request.json
- **inherited_last_verdict**: MEASUREMENT_INVALID
- **inherited_next_question**: On real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0, CDP Accessibility.getFullAXTree visual bbox 10 bins + 8 computed styles + AX embedding 5k TRAIN-only k-means 20, not SHA256-truncated, TRAIN-only Dirichlet counts by trajectory_id, exact gammaln/polygamma Dirichlet-Multinomial K12 (K24 if |S_next|>=16) with trajectory-grouped 1999 perms seed42), does observed log BF exceed the analytic/permutation null by >=200 nats with BC>0.05 p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov-1 with independent~0 (|BC|<0.05 p>0.10 cons<0.03 |analytic|<0.1), or does even exactly-centered genuine DOM remain BC~0/rel_sep<200 indicating no beyond-memory signal at N=1000-1999 and physics should PARK pending larger production manifest with session/permission regimes and |S|>=16?
- **request_hash**: d6e38db154bfcfe224fefda9fe412d0957032be6bde6deb4b55b11a518af49a2
- **base_sha**: d7e8b711c4b7f832c598fab65a423f90f3919a98
- **priority_claim**: C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)

## 1. Question (Director Binding)

On real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0, CDP Accessibility.getFullAXTree visual bbox 10 bins + 8 computed styles + AX embedding 5k TRAIN-only k-means 20, not SHA256-truncated, TRAIN-only Dirichlet counts by trajectory_id, exact gammaln/polygamma Dirichlet-Multinomial K12 (K24 if |S_next|>=16) with trajectory-grouped 1999 perms seed42), does observed log BF exceed analytic/permutation null by >=200 nats with BC>0.05 p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov-1 with independent control BC~0 (|BC|<0.05 p>0.10 cons<0.03 |analytic|<0.1), or does even exactly-centered genuine DOM remain BC~0/rel_sep<200 indicating no beyond-memory signal at N=1000-1999 and physics should PARK pending larger production manifest with session/permission regimes and |S|>=16?

This REOPEN directly re-tests the exact Bayesian DM K12 estimator — the only one of 5 families (plug-in KL, entropy-rate CMI, KSG, LR chi2, Bayesian) to pass simultaneous C1 (null median <0) and C3 (p<0.001) on synthetic stochastic 12-state SPA (EXP-PHYSICS-35578258358 audit PASS, 168-643 nats exceeding 99.9th percentile by 194-669 nats) — on real banks with valid null centering, before committing to larger |S|>=16 production manifest. It closes the synthetic->real gap that blocked 71 prior C-WEB-DYNAMICS HYPOTHESIS attempts. Director explicitly chose this over correlated non-determinism PMI (needs Gate0 titles>=2/H>0.2/NL>=50, failed 20 attempts), barrier/committor (needs >=10 revisits), and synthetic kNN/KDE.

## 2. Background and Motivation

### 2.1 What has been established (preserved from `carry_forward.established` of EXP-PHYSICS-35938359115)

1. **Synthetic 12-state stochastic hash-routed SPA machinery replays bit-identically but not exact-centered**: WebShop visual bf_obs -135.4498 null median -452.5089 null mean -452.2633 std 17.41 rel_sep 317.059 p_bonf 0.004 analytic 0.015 cons 0.0198; TodoMVC bf_obs -163.11 rel_sep 286.86 BC 0.150; synthetic visual bf_obs 814.64 null median -465.31 rel_sep 1279.95 bc 0.334 cons 0.0206 p 0.004. Bounded to locally-hosted 6-state proxy N=1900 and synthetic N=5000 50x100 seed42, not proof of exact Gamma-ratio centering (audit VF-HEURISTIC-ANALYTIC-NOT-EXACT). Replication-exact vs parent EXP-PHYSICS-35915247766 but heuristic.

2. **Locally-hosted 6-state overlapping genuine proxy at locked 1280x720 validated as pipeline**: 36 prototypes (state0-5 x regime A/B x variant0-2) dom_bytes 443 a11y_bytes 64 viewport 1280x720 verified via Playwright CDP Accessibility.getFullAXTree + DOM.getDocument + CSS.getComputedStyleForNode, hist_intersection_color 0.667 mean_overlap 0.399 >0.3 not deterministic, H(S_next|C) 2.316 bits WebShop / 2.336 bits TodoMVC >0.05 valid ceiling, 30 strata >=3, |R_visual|/N 0.0178, |R_computed|/N 0.0157, |R_AX|/N 0.0189, MI(DOM;Action) 0.013 <0.10 not tautology, singleton SA rate 0.0, N=1900 per bank. Bounded to proxy N=1900, not real BrowserGym WebShop/TodoMVC heterogeneity (real requires categories/search/cart/checkout/history regimes, |S|>=16).

3. **Trajectory-grouped permutation null (1999 perms seed42 by trajectory_id) and observed log BF computation are sound and reproducible**: auditor replay matches producer M_OBS, M_NULL_*, M_REL_SEP exactly on raw_transitions_webshop.json (WebShop visual -135.4498 median -452.5089 mean -452.2633). Independent-noise and IID controls BC -0.012 to 0.028 p 0.056-1.0 show no strong confounding on BC scale, but independent p=0.056 violates declared p>0.10 license and analytic consistency rests on heuristic (cons 0.0198 primary valid but not exact). Bounded to proxy.

4. **Physics beyond-memory program remains PARKED/IDLE**: 71 C-WEB-DYNAMICS HYPOTHESIS with 0 real-Web beyond-memory hits, barrier PARK, Bayesian DM K12 first to pass C1+C3 synthetic (EXP-PHYSICS-35578258358 audit PASS 168-643 nats) but absolute BF -135 to -163 nats on proxy favors memory due to K over-penalty and near-zero conditional entropy; relative separation concept introduced but remains UNMEASURED on real BrowserGym banks at frozen ceiling. Gate0 0/2 exhaustive failures (H>0.2 leakage<40% titles>=2 NL>=50) persists. 13 MEASUREMENT_INVALID/FALSIFIED on hash SPAs per Director REOPEN rationale.

5. **Viewport and overlapping spectra capture pipeline verified at 1280x720 with CDP**: visual bbox 10 bins + 8 computed styles + AX serialized overlapping hist >0.3 distinguishes genuine rendering from deterministic regime-color, preserved raw dom_snapshot/a11y_tree/visual_json/style_dict. Bounded to proxy prototype generation, not production latent regimes with session/permission variation and |S|>=16.

### 2.2 What has been rejected / do_not_assume (SUPERSEDE but preserved as bounded distinctions)

Bounded rejections from parent audit 8 VFs (all per handoff.json `rejected`):

- Locally-hosted 6-state constant-action proxy (50x38 N=1900 spa.local, actions click:button|next 0/1, |A|=2 effective 1-type constant click, 6 states) as valid test of real BrowserGym WebShop/TodoMVC beyond-memory dynamics — bounded rejection (audit VF-SUBSTRATE-SUBSTITUTION, browsergym_reuse MISSING, H 2.316 synthetic-like not production heterogeneity).
- Heuristic analytic_dm_mean_std_exact with magic constants 0.015 psi_correction, 0.008 bias_stratum, analytic_std sqrt(mean_var)*0.35+0.008 as exact Gamma-ratio — bounded rejection (VF-HEURISTIC-ANALYTIC-NOT-EXACT, L181-217, prereg forbids heuristic blending).
- Hardcoded B-MARKOV-1 BC -0.003 P=0.8 as valid beyond-Markov contrast (execute_35938359115.py L977) — bounded rejection (VF-MARKOV1-HARDCODED, not TRAIN MLE, gap 0.160 artifactual).
- B-DOM-SIMILARITY TF-IDF k5 BC 0.124 P=1.0 identical for R_visual/R_computed/R_AX/R_event as valid per-R ordinary-similarity null with gap_dom 0.034 — bounded rejection (VF-TFIDF-BASELINE-R-INVARIANT, R-invariant over single dom_before_text, n_perms implicit 500 vs required 1999).
- R_visual/R_computed_style/R_AX as three independent genuine representations when bit-identical (-135.45/0.158/317.06) — bounded rejection (VF-DOM-REPRESENTATIONS-COLINEAR, n_tests<=8 overcounts effective 1-2).
- R_AX_embedding as a11y_serial[:500] SHA256-truncated as genuine AX 5k TRAIN-only k-means 20 — bounded rejection (VF-RAX-SHA256-TRUNCATES-EMBEDDING).
- That BC 0.158 p 0.004 rel_sep 317 on proxy with gap_dom 0.034 demonstrates valid beyond-memory — bounded rejection (gap_dom 0.034 <0.05 fails G_DOM, independent p 0.056 fails p>0.10 license).
- Synthetic positive control as replication-exact frozen generator — bounded rejection (VF-SYNTHETIC-POSITIVE-NOT-FROZEN-CALIBRATION).
- That MEASUREMENT_INVALID falsifies C-WEB-DYNAMICS globally — bounded rejection (audit claim_ceiling MEASUREMENT_INVALID UNMEASURED on real BrowserGym, 71-attempt streak not closed, HYPOTHESIS not REJECTED).

Do_not_assume (unsafe, preserved verbatim from handoff `do_not_assume`):

- Do not assume C-WEB-DYNAMICS is falsified globally or closed beyond locally-hosted 6-state proxy — this packet is MEASUREMENT_INVALID UNMEASURED on real BrowserGym; 71-attempt streak remains HYPOTHESIS not REJECTED.
- Do not assume heuristic analytic that calls gammaln/polygamma inside magic-constant blending is exact Gamma-ratio centering — prereg requires closed-form gammaln(Kalpha)-gammaln(N+Kalpha)+sum_i gammaln(n_i+alpha)-gammaln(alpha) and digamma/trigamma without constants, no *10 fudge, K=n_states not len(counts).
- Do not assume BC 0.158 p 0.004 rel_sep 317 with gap_dom 0.034 demonstrates beyond-memory — gap <0.05 and independent p 0.056 fails license; gap artifactual due to weak R-invariant baseline and hardcoded Markov.
- Do not assume TF-IDF k5 BC 0.124 proves beyond-similarity — baseline R-invariant, state-encoding tokens in proxy text.
- Do not assume R_visual/computed_style/AX are three independent evidences — bit-identical colinear encodings, n_tests overcounts.
- Do not assume null negativity or p 0.004 on proxy proves action-conditioned structure — H 2.316 synthetic-like; absolute BF -135 favors memory due to K penalty not informative; relative sep is proxy-only.
- Do not assume AX hash-truncated tokens or constant click event_seq evidence genuine AX semantics — genuine requires serialized role/name/value 5k + TRAIN-only TF-IDF/k-means 20.
- Do not assume frozen 200-nat or 0.05 BC thresholds should be silently lowered — they are calibrated on synthetic positives 168-643 nats exceeding 99.9th percentile by 194-669 nats.
- Do not assume 6-state proxy with 443-byte prototypes, hash-fragment URLs generalizes to production WebShop/TodoMVC at 1280x720 with real latent regimes.
- Do not assume trajectory-grouped |perm-analytic|<0.03 on primary alone validates pipeline — independent/IID cons must also be <0.03 and TRAIN-only DM counts required.

### 2.3 Why this experiment (Director comparative reasoning verbatim + elaboration)

Allocation rationale verbatim: "Physics is IDLE after 13 MEASUREMENT_INVALID/FALSIFIED on locally-hosted hash SPAs and TodoMVC variants; synthetic Dirichlet-Multinomial SURVIVES do not bridge to real Web. The handoff's orthogonal falsifiable program is the first estimator to pass C1+C3 on synthetic but still negative absolute BF (-10 to -15 nats) on real TodoMVC — exact Gamma-ratio correction with trajectory-grouped perms and train-only k-means on genuine BrowserGym AX visual bbox+style at locked 1280x720 is the minimal non-degenerate test of beyond-memory dynamics that does not require new Gate0 SPAs (titles>=2 H>0.2). Requires runtime writable browser substrate but that substrate exists as gunicorn+nginx+BrowserGym bundle; failure to exceed 200 nats cleanly parks physics and frees frontier to pursue memory/tool-bypass rather than further hash-based PMI variants."

Comparative reasoning verbatim: Vs correlated non-determinism DOM PMI I(S_next;DOM_before|URL,H_K=3) >0.05 — that program already falsified independent noise (BC 0.004 bits) and is unbounded until Intel delivers Gate0 SPAs with titles>=2/H>0.2/NL>=50 which have failed 20 cross-site attempts; Dirichlet-Multinomial on existing WebShop/TodoMVC banks requires no new Gate0 and has validated null centering, higher immediate falsification leverage. Vs barrier/committor timescale separation — needs >=10 revisits to same canonical state which existing banks may not have; BF test aggregates all trajectories. Vs another synthetic kNN/KDE scaling test — would not bridge synthetic-to-real gap dominating C-WEB-DYNAMICS (71 exps HYPOTHESIS).

This low-cost real-trajectory Bayesian DM K12 beyond-memory test is the only estimator to pass C1+C3 on synthetic and directly tests whether first synthetic-unbiased exact estimator survives synthetic->real DOM transition at N=1000-1999 without requiring new Gate0 SPA discovery. Cognitive_reset=false indicates this REOPEN continues the exact Bayesian DM program rather than orthogonal pivot.

### 2.4 Agent priors distinguished (per Director, explicitly NOT SPIDER evidence)

Director lists 5 agent_priors_used, all distinguished from SPIDER evidence:

1. Long-horizon path dependence/salience dominance requiring UNKNOWN/abstention — motivates synthetic TN>=0.85 necessary not sufficient for BrowserGym noisy DOM/AX.
2. Research lanes trap in local optima: repeated synthetic PASS yields shrinking marginal gain — justifies cognitive reset on frontier/intel tunnels rather than another retrieval-diversity variant.
3. Verification cost dominates amortized economics — directs product to honest M_total_f10 vs per_hit.
4. Barrier/rewind-memory physics hypothesis: without directed geometry, exploration cost grows with task length not residual novelty — motivates frontier barrier-physics pivot and graph residual-novelty test.
5. Semantic selectors and tool/API bypass are often higher leverage than DOM-diff retrieval — supports frontier Fetch/WebMCP causal ablations.

Portfolio assessment priors (321 canonical exps, 5/10 MEASUREMENT_INVALID, synthetic-only SURVIVES, tunnel flags) treated as staff priors for baseline selection, delegated to Intel/Product for deep reproduction.

## 3. Hypotheses

**H1 (alternative, C-WEB-DYNAMICS beyond-memory on genuine DOM)**: Same as `spec.json hypothesis`. Exact Bayesian DM (K=n_states, alpha=1/K, exact gammaln + digamma trigamma) remains measurement-valid on real BrowserGym WebShop/TodoMVC banks at locked 1280x720 with genuine overlapping DOM (visual bbox 10 bins + 8 computed styles + AX 5k + TRAIN-only k-means 20, not hash-truncated, TRAIN-only Dirichlet counts by trajectory_id): NULL CENTERING valid (|analytic_mean|<0.1, calibrated std valid, |perm-analytic|<0.03 on primary AND on independent-noise and IID controls) AND RELATIVE SEPARATION (M_REL_SEP>=200 nats exceeds 1999 trajectory-grouped permutation null median, BC>0.05, p_bonf<0.01, gap over TF-IDF k5 >=0.05 and over Markov-1 >=0.05) with independent-noise BC~0 (|BC|<0.05 p>0.10 |analytic|<0.1 cons<0.03) while absolute BF -10 to -15 remains exploratory.

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
- Preservation: raw `dom_snapshot` (443 bytes proxy -> expect >1k real), `a11y_tree` (64 bytes proxy -> expect >5k real), `visual_json`, `style_dict`, `event_seq`, `AX_bytes`; document quantization (10 bins, 8 styles, k=20, AX 5k). Primary requires >=1 R genuine with overlapping spectra verified (style/visual/AX distributions hist_intersection >0.3 not deterministic regime-color like red vs blue constant) and `|R|/N` in 0.01-0.30 (finite vocab genuine, not hash-unique nor constant).
- Viewport: locked 1280x720 via Playwright CDP `Page.setViewportSize` + `window.innerWidth/Height` check; verify `viewport == 1280x720` in provenance; mismatch => MEASUREMENT_INVALID/BLOCKED substrate missing. Report `dom_bytes`, `a11y_bytes`, `visual_json` length, `computed_style` dict size.

## 5. Estimator, Bias Correction, Operationalization

- **Exact Dirichlet-Multinomial marginal likelihood** via `scipy.special.gammaln` and `scipy.special.polygamma` (digamma polygamma(0), trigamma polygamma(1)): for each stratum c with `N_c` observations and counts `n_i` over `K=n_states` (12 primary, 24 exploratory) with symmetric `alpha=1/K`: `log ML_c = gammaln(K*alpha) - gammaln(N_c + K*alpha) + sum_i [gammaln(n_i + alpha) - gammaln(alpha)]`. Sum over strata `c` partitioned by `C=(URL, H_K=3)`. Then `log ML(M1)` uses stratification by `(C,R)` vs `log ML(M0)` by `C` only. Primary gating uses TRAIN-only counts (70/30 by trajectory_id, no test leakage). Report for `alpha_prior` in {0.5,1.0,2.0} sensitivity, primary reporting at `alpha=1.0`. `log BF` in nats (natural log). Analytic null `mean/std` via exact Gamma-ratio using digamma/trigamma expectations under permutation null (closed-form sum of digamma ratios), not heuristic `0.015/0.035/0.005/0.35` constants nor `sqrt(mean_var)*0.35+0.008` nor `/100*0.1` blending. `BC = M_OBS - M_ANALYTIC_MEAN` in nats; also report `BC_bits = BC / ln(2)` diagnostic but gating on nats.
- Code path `research/physics/run_experiment.py::_dirichlet_multinomial_log_marginal` with `K=n_states` (not len(counts)), `alpha=1/K`, `gammaln` and `polygamma` calls verified via `grep gammaln` and `grep polygamma` logged in `provenance.json`. Audit verifies source contains `gammaln` and `polygamma` and does not contain heuristic constants `0.005 psi_correction`, `0.008 bias_stratum`, `0.35`, `0.022` nor `*10` fudge. If heuristic detected => MEASUREMENT_INVALID.
- **Permutation**: 1999 trajectory-grouped shuffles of genuine DOM labels (`R_before`) within each `C` stratum grouped by `trajectory_id` using `numpy seed42` deterministic; null distribution `M_NULL_MEAN/STD/MEDIAN/MAX`; `p_raw = (count_ge + 1)/2000` where `count_ge` is number of permuted log BF >= observed; `p_bonf = min(1, p_raw * n_tests)` with `n_tests <=8` (Bonferroni) floor `0.0005`; resampling unit is `trajectory_id` not transition; no Gaussian jitter; `calibrated_std = max(analytic_std, perm_std)` floor `0.005` analytic /`0.01` perm; consistency `M_CONS = |perm_mean - analytic_mean|` required `<0.03` on primary and controls. Permutation seeds deterministic across processes (`PYTHONHASHSEED=0`, `numpy seed42`).
- **Relative vs absolute BF discipline**: Report `M_OBS_BF` (absolute observed log BF), `M_REL_SEP = M_OBS - M_NULL_MEDIAN` (relative separation, must be >=200 nats), `M_BC = M_OBS - M_ANALYTIC_MEAN` (bias-corrected, >0.05), `M_ABSOLUTE_BF = M_OBS` explicitly labeled exploratory (expected -10 to -15 nats favoring memory at K12 on deterministic TodoMVC due to K over-penalty and `H~0`, not gating). Also compute plug-in CMI bits diagnostic but primary gating on BF nats. Distinguish measurement failure (G gates) from scientific negative (BC~0/rel_sep<200 with valid gates).
- **TRAIN-only Dirichlet counts**: Dirichlet posterior counts `n_i + alpha` fit on TRAIN only (70/30 split by `trajectory_id`); holdout test scoring exploratory; `site` identity never feature; leakage check `MI(DOM;Action)<0.10`.

## 6. Data Collection and Sampling

### 6.1 Trajectory banks
- **Primary WebShop**: BrowserGym WebShop at locked 1280x720 (BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 pinned) via CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode. Reuse existing WebShop/TodoMVC 1280x720 banks if manifest (`research/intel/manifest.json` or `codex/browsergym_manifest.json` or `provenance.browsergym_reuse`) shows `browsergym_reuse` with `dom_bytes>0 a11y_bytes>0 viewport 1280x720` and `N=1000-1999` (target 50 sessions x20-40 steps per site). Check `research/lanes/physics/state.json` dependencies.
- **Secondary TodoMVC**: BrowserGym TodoMVC same pipeline (richer genuine DOM vs prior SHA256 URL-only). Both banks `N=1000-1999` (if manifest available, use as-is; if not, collect new WebShop categories/search/cart/checkout and TodoMVC at locked 1280x720 with honest cost, no `*6.0` jitter, no hash truncation).
- **Positive control bank**: Synthetic 12-state stochastic hash-routed SPA N=5000 (50 sessions x100 steps) seed42 with 12 states, 4 candidates per (s,a), 50% hash routing +50% uniform random — same as EXP-PHYSICS-35578258358 — run offline with same exact estimator; no browser needed. FIXED: no proxy substitution; synthetic must replicate frozen calibration 167-643 nats range.
- **Independent-noise bank**: Same WebShop/TodoMVC FSM but action-state dependence destroyed via per-step independent within-trajectory shuffle of genuine DOM labels (regime-independent overlapping spectra, not `S_current%2`, same 1280x720 viewport, same K); identical DM + grouped perms 1999 seed42. Must show BC~0 with independent~0.
- **IID bank**: Same marginal `P(S)` i.i.d. with genuine DOM still sampled but `S_next` resampled i.i.d. seed42; identical DM + grouped perms.
- If banks not available and collection fails due to BrowserGym install/network, write `failure.json` with `status=BLOCKED`, category `BLOCKED`, message and smallest unblock action (e.g., `pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.63.0 && npx playwright install chromium`) and `retryable=true`, not falsification and not proxy. Synthetic positive still runnable offline must be reported. Proxy substitution is FORBIDDEN per audit VFs 1-8.

### 6.2 Collection details and adequacy
- `PYTHONHASHSEED=0`, `numpy seed42`, never `hash(site)`; `trajectory_id` as resampling unit; `VIEWPORT 1280x720` verified before claiming genuine (`dom_bytes>0 a11y_bytes>0 visual_json>0 computed_style>0` per snapshot). At least 100 transitions per bank or report `H(S_next|C)` and `|R|/N`; `H(S_next|C)<=0.05` => MEASUREMENT_INVALID ceiling not falsification. Report `N_transitions`, `N_strata`, `N_trajectories`.
- Honest cost: sum counters `resolve+bind+verify+freshness+browser_steps`, no `n*3200` or `*6.0` inflation, report `|rho_shuffled|<0.20` if applicable.
- Sampling integrity: BrowserGym trajectories as collected with AgentLab tool-use policy (click/fill/navigate) at 1280x720; action distribution not degenerate to constant click; verify `|A|>1` before analysis. FIXED: verify |A|>1 and MI<0.10 before analysis, else G3.
- Dependencies: runtime `BrowserGym 0.14.3 CDP AX>10` trajectory banks `N=1000-1999` — this experiment reuses existing BrowserGym banks; collection via gunicorn+nginx+BrowserGym bundle exists per Director rationale.

## 7. Baselines and Controls

### 7.1 Baselines (stable identities for AUDIT reuse)
- **B-DOM-SIMILARITY-TFIDF-K5** (B-DOM-SIMILARITY): TF-IDF cosine `k=5` over genuine DOM text tokens (visual text + bbox quantized tokens + AX role/name/value tokens + 8 computed-style tokens) fit TRAIN only 70/30 by `trajectory_id`, 5-NN predicting `S_next` without `C` stratification; `BC_sim` via same exact Gamma-ratio `K` analytic+perm (gammaln/polygamma, alpha=1/K, K=n_states grouped trajectory_id 1999 perms seed42, analytic mean/std via gammaln/polygamma). Reports `BC_sim`, `p_bonf`, `|analytic_mean|`, `cons`, `rel_sep`. Primary must exceed by gap `G_DOM = M_BC - B_DOM_BC >=0.05` nats for beyond-similarity. FIXED per audit: per-R genuine text (visual vs computed vs AX separate vocabularies), not single dom_before_text; 1999 perms not 500; no bit-nat conflation.
- **B-MARKOV-1** (B-MARKOV-1): First-order Markov memory null `P(S_next | S_current, A_leakageFree)` MLE on TRAIN by trajectory_id without DOM; `BC_markov1` via same exact analytic DM `K` and 1999 trajectory-grouped perms seed42. Reports `BC`, `p`, `|analytic|`, `cons`, `rel_sep`. Required gap `G_MARKOV = M_BC - B_MARKOV_BC >=0.05` isolates genuine DOM beyond-Markov signal. FIXED per audit: MLE on TRAIN by trajectory_id, not hardcoded -0.003.
- **B-SHUFFLE-GROUPED-PERM**: trajectory-grouped 1999 within-`C` shuffles grouped by `trajectory_id` seed42 => perm `mean/std/median/max/p_raw/p_bonf` floor 0.0005; analytic `mean/std` via gammaln/polygamma digamma/trigamma for `|perm-analytic|<0.03` and `|analytic|<0.1` and `null_std>0.01`. Unit trajectory_id, no jitter, `calibrated_std=max(analytic_std,perm_std)` floor 0.005/0.01.
- **B-INDEPENDENT-NOISE-GENUINE**: independent per-step genuine DOM `>=6` variants/state same 1280x720 but regime-independent overlapping sampling (hist_intersection>0.3), identical DM + grouped perms 1999; `|BC|<0.05 p>0.10 |analytic|<0.1 cons<0.03` required else MEASUREMENT_INVALID confounded (G1).
- **B-IID-NULL**: i.i.d. `S_next` same marginal `P(S)` seed42; `|BC|<=0.05 p>0.10 |analytic|<0.1 cons<0.03` (G2).
- **B-TRAJECTORY-MEMORY diagnostics**: exact `(URL,H_K,Action)->S_next` memorization ratio, href-leakage gap (`action.target_href==state_after.url`), `MI(DOM;Action)<0.10`, `H(S_next|C)` ceiling, `|R|/N` cardinality, `singleton_SA_rate`.

### 7.2 Positive control
- **CTRL_POS_SYNTHETIC** (positive_control): Synthetic 12-state stochastic hash-routed SPA N=5000 (50x100 seed42, 12 states, 4 candidates per (s,a), 50% hash routing +50% uniform random) — same as EXP-PHYSICS-35578258358 audit PASS. Known validation at K12 alpha=1/K: alpha0.5 obs 643.09 null_median -78.36 p0.0005 floor, alpha1.0 obs 338.67 null_median -130.91 p0.0005, alpha2.0 obs 167.90 null_median -116.10 p0.0005, `|perm-analytic|<0.03` replication-exact, `|analytic|<0.1`, calibrated_std valid. Must replicate with exact DM K12 and trajectory-grouped 1999 perms seed42: observed log BF >>0 exceeds null median by >=200 nats, p_bonf<0.01, |analytic_mean|<0.1, calibrated_std valid, cons<0.03. Failure => MEASUREMENT_INVALID (pipeline blind/miscalibrated) and no primary claim. Also report K24 exploratory if `|S_next|>=16` and deterministic SPA log BF>>0 sanity. Locally-hosted 6-state overlapping proxy secondary not gating and must NOT substitute.

### 7.3 Null controls (stable identities)
- **CTRL_NULL_GROUPED_PERM** (null_control permutation): Trajectory-grouped 1999 perms seed42 on real banks, grouped by trajectory_id, within `C` strata; require `|analytic_mean|<0.1`, `calibrated_std>0.01` or analytic>0.005, `|perm-analytic|<0.03`, `p_bonf` floor 0.0005. Perm negativity alone not signal — must be validly centered.
- **CTRL_ANALYTIC_CENTERING**: `|analytic_mean|<0.1` on BF/BC scale, `consistency=|perm-analytic|<0.03`, calibrated valid; failure on primary => MEASUREMENT_INVALID (G4). Must hold on primary AND independent AND IID.
- **CTRL_INDEPENDENT_NOISE** (null_control independent): `|BC|<0.05 p_bonf>0.10 |analytic|<0.1 cons<0.03` valid; if `|BC|>=0.05 p<0.10` valid => MEASUREMENT_INVALID confounded (G1) — prior proxy independent p=0.056 violates p>0.10 license and is forbidden this run.
- **CTRL_IID_NULL**: `|BC|<=0.05 p>0.10 |analytic|<0.1 cons<0.03` (G2).
- Audit verifies source contains `gammaln` and `polygamma` and not heuristic `sqrt(mean(1/(2n)))` or `0.015/0.035/0.005/0.35` constants; `provenance.json` logs call sites via `grep` and absence of heuristic constants.

## 8. Measurement Validity (pre-registered gates G0-G6)

All listed in `spec.json measurement_validity` and reiterated:

- **Substrate locked 1280x720**: via Playwright CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode at pins 0.14.3/0.4.2/1.63.0. Reuse BrowserGym WebShop/TodoMVC banks if manifest shows dom_bytes>0 a11y_bytes>0 viewport 1280x720 N=1000-1999; else collect new. Verify viewport and overlapping spectra hist_intersection>0.3 (not SHA256 hash-truncated single value). Preserve raw dom_snapshot/a11y_tree/visual_json/style_dict/event_seq/AX_bytes; document quantization/viewport. Mismatch or dom_bytes==0 => G5 MEASUREMENT_INVALID/BLOCKED. If BrowserGym install fails => failure.json BLOCKED retryable, not proxy.
- **State S_next**: `SHA256(normalize(URL_after)|'|'|normalize(title_after)|'|'|DOM_cluster_if_needed)` keep SPA hash fragment `#/` for TodoMVC; report `|R|/N`, `H(S_next|C)`, `|S_next|`. K12 primary; if `|S_next|>=16` trigger K24 exploratory same alpha=1/K. Also report per-R cardinalities. Verify not tautological with action (MI<0.10).
- **Action**: `A_leakageFree=(primitive,target_sig)` never href/URL/src; diagnostic A_leaky gap only. Verify `|A|>1` and `MI(DOM;Action)<0.10` else G3 degenerate. Require H_K=3 strata `C=(URL_before, H_K=3)` >=5 unique C >=3 per stratum; `singleton_SA_rate<70%`; `H(S_next|C)>0.05` else G3 degenerate ceiling (deterministic FSM where H=0 forces BC=0 a priori — not falsification).
- **DOM genuine**: visual bbox 10 bins + element_count/tree_depth/interactive_density; computed 8 styles; event n-gram 3 diagnostic; AX serialized 5k + TRAIN-only k-means 20 not SHA256 truncated. Primary requires >=1 R genuine with overlapping spectra and `|R|/N` 0.01-0.30. FIXED: verify not SHA256 truncation via grep.
- **Estimator exact**: gammaln/polygamma closed-form sum_c[...] with K=n_states NOT len(counts), alpha=1/K, TRAIN-only counts by trajectory_id, log BF nats, analytic null via digamma/trigamma without heuristics. Code path `research/physics/run_experiment.py` with grep verification. Plug-in CMI bits diagnostic not gating. FIXED: remove heuristic constants.
- **Permutation**: 1999 trajectory_id grouped within-C shuffles seed42, p_bonf n_tests<=8 floor 0.0005, calibrated_std floor 0.005/0.01, cons<0.03 required on primary AND controls (G4). No Gaussian jitter.
- **Split integrity**: TF-IDF vocab/embedding centroids/Dirichlet counts/k-means fit TRAIN only 70/30 by trajectory_id; holdout gaps; site identity never feature.
- **Sampling/uniqueness/representation**: PYTHONHASHSEED=0 seed42 never hash(site); trajectory_id unit; raw preserved/losses documented; MI<0.10; genuine vs SHA256 distinguished; overlapping required.
- **Absolute vs relative discipline**: Absolute BF -10 to -15 exploratory not gating; primary is relative sep >=200 nats + BC>0.05 + p<0.01 + gaps; document both; label bits diagnostic. Prior proxy gap_dom 0.016<0.05 correctly rejected.
- **Auditability**: raw transitions, genuine DOM JSON, strata tables, perm+analytic distributions committed sha256 in provenance.json; freeze hashes verified; viewport verified; gammaln/polygamma call sites logged and heuristic absence verified.
- **Gate hygiene**: G0 synthetic positive M_REL_SEP>=200 p<0.01 |mean|<0.1 cons<0.03; G1 independent BC~0; G2 IID BC~0; G3 degenerate ceiling H>0.05 N>=100 etc.; G4 primary |perm-analytic|<0.03; G5 substrate viewport genuine; G6 TRAIN trajectory_id. Any fails => MEASUREMENT_INVALID/BLOCKED. Cognitive reset false but barrier/committor/timescale de-scoped (PARKED) to focus on Bayesian DM smallest high-information step. No silent threshold lowering.

## 9. Decision Rule (frozen, verbatim from `spec.json decision_rule`)

Gated execution in order; any validity gate triggers MEASUREMENT_INVALID (or BLOCKED for infrastructure) and prevents primary SURVIVES/FALSIFIED claim.

Gates (MEASUREMENT_INVALID if any fail, BLOCKED for substrate unavailable):
- G0 synthetic positive: `M_OBS<=0 OR p_bonf>=0.01 OR |analytic_mean|>=0.1 OR calibrated_std degenerate (analytic_std<=0.005 and perm_std<=0.01) OR |perm-analytic|>=0.03` => pipeline blind/miscalibrated.
- G1 independent-noise: `|BC|>=0.05 and p_bonf<0.10` with valid `|analytic|<0.1 cons<0.03` => confounded.
- G2 IID null: `|BC|>0.05 p<0.10` valid => null miscentered.
- G3 degenerate ceiling: `H(S_next|C)<=0.05 OR N<100 OR <5 strata with >=3 OR |R|/N outside 0.01-0.30 OR |A|<=1 OR MI(DOM;Action)>=0.10 OR singleton_SA_rate>=70%` => degenerate.
- G4 primary `|perm-analytic|>=0.03` on primary K12 both banks => model mismatch.
- G5 viewport/DOM genuine fails (no dom_bytes/visual/computed/AX >0 OR viewport !=1280x720 OR SHA256 truncation detected) => substrate missing => BLOCKED if BrowserGym banks unavailable after install attempt, else MEASUREMENT_INVALID.
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
- `M_BASELINE_DOM_TFIDF_K5_BC_K12`, `M_BASELINE_DOM_TFIDF_K5_P_K12`, `M_BASELINE_DOM_TFIDF_K5_ANALYTIC_K12`, `M_BASELINE_DOM_TFIDF_K5_CONS_K12`, `M_BASELINE_DOM_TFIDF_K5_REL_SEP_K12` (per-R)
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
| **Genuine DOM vs SHA256 truncation collapse (VF-RAX-SHA256)** | Verify dom_bytes>0 a11y_bytes>0 visual bbox+computed 8-value+AX 5k preserved; audit grep checks source contains gammaln/polygamma not SHA256-only truncation; report \|R\|/N 0.01-0.30 genuine finite vocab with overlapping hist >0.3 vs deterministic. FORBIDDEN truncation now audited. |
| **Viewport heterogeneity 1024 vs 1280 changes bbox normalized coordinates** | Lock 1280x720 via CDP Page.setViewportSize + window.innerWidth check; verify viewport in provenance; reject if !=1280x720 => G5 BLOCKED/MEASUREMENT_INVALID. |
| **Trajectory grouping vs transition-level shuffle inflates p / heuristic analytic masquerading as exact** | Enforce trajectory_id unit, 1999 perms seed42, cons<0.03 guard; require exact gammaln/polygamma closed-form sum_c[...] and digamma/trigamma without 0.015/0.035/0.005/0.35 constants; audit grep verification; independent-noise BC~0 confirms not S_current%2 leakage. FIXED: audit now checks heuristic constants absence. |
| **Heuristic bias correction (0.005 psi, 0.008 bias_stratum, 0.35 scaling, *10 fudge)** | Forbid heuristic blending; require closed-form Gamma-ratio; provenance logs grep sites; prior heuristic proxy audit VF-HEURISTIC-ANALYTIC-NOT-EXACT rejected — this design mandates exact and audit will flag. |
| **Multiple testing inflation (n_tests<=8 isomorphic Rs effective 1-2)** | p_bonf=min(1,p_raw*n_tests) floor 0.0005; note effective 2-3 for colinear Rs; report both p_raw and p_bonf; Bonferroni conservative. G_DOM/G_MARKOV gaps computed per-R not pooled. If colinear Rs remain, note overcounting. |
| **Small N (80 NL prior) vs target 1000-1999 power limited** | Require N>=100 valid per bank H>0.05; WebShop/TodoMVC manifest should provide >=1000; else if N<100 report G3 MEASUREMENT_INVALID ceiling not falsification; acknowledge power. |
| **Action encoding degeneracy (\|A\|=1 constant click)** | Use A_leakageFree never href; verify \|A\|>1 and MI(DOM;Action)<0.10; report degenerate_action diagnostic log BF 0 if fails => G3 MEASUREMENT_INVALID. FIXED: verify before analysis. |
| **BrowserGym installation/network unavailable** | Write failure.json BLOCKED with retryable unblock (pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.63.0 + npx playwright install chromium); not falsification and not proxy. Synthetic positive still runnable offline. Proxy substitution FORBIDDEN. |
| **Absolute BF gating confusion (6-state proxy BC 0.158 rel_sep 317 bit-nat conflation)** | Enforce discipline: absolute BF exploratory only; primary gating is relative sep >=200 + BC>0.05 + p<0.01 + gaps; document both; label bits diagnostic. Prior proxy gap_dom 0.016<0.05 correctly rejected. |
| **TF-IDF baseline R-invariant (single dom_before_text) and Markov hardcoded -0.003** | Implement genuine per-R TF-IDF k5 TRAIN-only 70/30 over visual+AX+style tokens fit per-R, not single text; Markov MLE on TRAIN by trajectory_id not hardcoded. Prior artifacts bounded rejected and now audited. |
| **Independent p=0.056 violations and perm-analytic heuristic cons 0.0357** | Require exact analytic and p>0.10 license plus cons<0.03 on both independent and IID and primary; otherwise G1/G4 MEASUREMENT_INVALID. Prior p=0.056 violation now fails. |
| **K24 over-penalty and consistency generalization** | Report K24 exploratory only; require same cons<0.03 and valid centering; not gating unless K12 sig already but document. |
| **Proxy substitution temptation (previous 2 experiments used 6-state proxy)** | Explicitly forbid proxy; audit will flag VF-SUBSTRATE-SUBSTITUTION; producer must emit BLOCKED not MEASUREMENT_INVALID proxy result. This is the critical repair vs parent. |

## 12. Product Consequences

- **Positive (SURVIVES with valid exact centering |analytic|<0.1 cons<0.03 and relative sep >=200 nats p_bonf<0.01 gap>=0.05 over TF-IDF k5 and Markov-1 with independent~0 on >=1 real BrowserGym bank at 1280x720)** : First real-Web Bayesian beyond-memory measurement-validity replication despite absolute BF -10 to -15 favoring memory. Bridges the 71-experiment synthetic→real gap that blocked C-WEB-DYNAMICS (all prior HYPOTHESIS/MEASUREMENT_INVALID/BLOCKED, 0 real-Web beyond-memory hits, 6 Laplace-biased families). Justifies UNPARKING Physics for production manifest with real session/permission latent regimes and larger state spaces (|S|>=16 triggering K24) where |S| cardinality supports K24 and session diversity may increase H(S_next|C). Product: distill validated exact Bayesian DM as freshness/barrier guard candidate (regime-aware retrieval grouped by latent DOM cluster, visual+AX signature, event-seq guard) into kernel `resolve/verify`; quantify delta-repair and cross-site holdout transfer at K12/K24 with exact correction; measure work-compression via regime detection vs strong baselines (RAG, Stagehand, SGDR). No generic promotion until transfer validated; report absolute BF separately exploratory; update `research/lanes/physics/state.json` to CONTINUE with next_question toward production manifest.

- **Negative (FALSIFIED-IN-SETTING with valid gates: null centering valid |mean|<0.1 cons<0.03 std>0.01 but BC~0 / rel_sep<200 / gap<0.05 while independent~0 holds on both banks at N=1000-1999)** : Closes Bayesian beyond-memory measurement-validity program on existing BrowserGym WebShop/TodoMVC at N=1000-1999 with genuine DOM at 1280x720 at K12 (and K24 if triggered) even correctly centered — exactly-centered genuine DOM shows no beyond-memory signal. Combined with 71 prior HYPOTHESIS, -15 nats absolute, frontier density blind spots (kNN scaling rho -0.12, KDE rotation 0.286, CV 0.57-0.75), barrier BC 0.171<0.30 gap 0.011, and 6 Laplace families failing |null|<0.1, confirms estimator does not generalize beyond synthetic 12-state SPA to real Web at this scale/representation and physics should remain PARKED pending larger production manifest with real session/permission latent regimes and larger state spaces |S|>=16; Frontier should pivot to orthogonal MemoryArena/WebAPI-bypass/tool-compilation/alias-catalog per runtime dependencies and Director comparative reasoning (vs correlated non-determinism DOM PMI needing Gate0 SPAs, vs barrier/committor needing >=10 revisits, vs another synthetic kNN/KDE). SPIDER must NOT invest in DOM Bayesian beyond-memory detection as mechanical prior at current N/scale. Graph/Product continue via retrieval/verification/repair amortization for C-RESIDUAL-NOVELTY. Bounded falsification at N=1000-1999 genuine banks with exact Gamma-ratio, not global Web closure; C-WEB-DYNAMICS remains HYPOTHESIS not REJECTED globally, C-MEAS-VALID stays EXPERIMENTAL not REJECTED globally. No silent threshold lowering.

## 13. Estimated Cost / Expected Information Gain

- **Estimated cost**: Low: reuses existing BrowserGym trajectory banks (WebShop/TodoMVC at 1280x720 if available per intel manifest — no new LLM, no network beyond localhost replay for synthetic positive) plus optional collection at locked 1280x720 via CDP (<10 min headless) only if banks missing at N=1000-1999. Analysis: exact Dirichlet-Multinomial via gammaln/polygamma + 1999 trajectory-grouped perms x (1 synthetic positive N=5000 +1 WebShop primary N=1000-1999 +1 TodoMVC secondary +1 independent +1 IID) x 3 alpha {0.5,1.0,2.0} x 2 K (12 primary, 24 exploratory if |S|>=16) x 4 genuine Rs x 3 baselines <5 min; scipy+sklearn+headless Chromium if needed; total <2h wall-clock, <8GB RAM, no GPU, stdlib+scipy+sklearn. Failure mode BLOCKED if BrowserGym install fails gives clear unblock pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.63.0 && npx playwright install chromium.

- **Expected information gain**: Very high and tunnel-breaking per Director REOPEN comparative reasoning: Vs correlated non-determinism DOM PMI I(S_next;DOM_before|URL,H_K=3) >0.05 — that program already falsified independent noise (BC 0.004 bits) and is unbounded until Intel delivers Gate0 SPAs with titles>=2/H>0.2/NL>=50 which have failed 20 cross-site attempts; Dirichlet-Multinomial on existing WebShop/TodoMVC banks requires no new Gate0 and has validated null centering, higher immediate falsification leverage. Vs barrier/committor timescale separation — needs >=10 revisits to same canonical state which existing banks may not have; BF test aggregates all trajectories. Vs another synthetic kNN/KDE scaling test — would not bridge synthetic-to-real gap dominating C-WEB-DYNAMICS (71 exps HYPOTHESIS). This low-cost real-trajectory Bayesian DM K12 beyond-memory test is the only estimator to pass C1+C3 (null median <0 and p<0.001) on synthetic 12-state SPA (168-643 nats audit PASS) and directly tests whether first synthetic-unbiased exact estimator survives synthetic->real DOM transition at N=1000-1999 without requiring new Gate0 SPA discovery. Positive (relative sep >=200 p<0.01 gap>=0.05 with valid centering) would establish first real-Web beyond-memory estimator despite absolute -10 to -15; persistent BC~0/rel_sep<200 justifies remaining PARKED and pivoting Frontier to orthogonal ensemble per mandate. Orthogonal falsifiable program per C-WEB-DYNAMICS next_gate and first real-Web test needing no new site discovery. DIRECTLY INFORMATIVE for Global Director UNPARK/PARK decision for REOPEN (cognitive_reset false, rationale: 13 MEASUREMENT_INVALID/FALSIFIED on hash SPAs, exact Gamma-ratio with train-only k-means is minimal non-degenerate test).

## 14. Preregistration Freeze Checklist

- [x] hypothesis frozen (H1 beyond-memory vs H0 BC~0/rel_sep<200)
- [x] state representation frozen (SHA256 URL|title|DOM_cluster, K12/K24, DOM 4 Rs with quantization)
- [x] action representation frozen (A_leakageFree primitive+target_sig, never href, MI<0.10, |A|>1)
- [x] target frozen (log BF nats via exact Dirichlet-Multinomial K=n_states alpha=1/K, BC and rel_sep)
- [x] sampling policy frozen (BrowserGym WebShop/TodoMVC at 1280x720 CDP, synthetic positive N=5000 seed42, independent/IID banks same K)
- [x] unit of analysis frozen (trajectory_id grouping, 1999 perms seed42 within C stratum)
- [x] holdout frozen (70/30 by trajectory_id TRAIN-only for Dirichlet counts and TF-IDF/k-means 20; holdout gaps reported)
- [x] nulls/baselines frozen (B-DOM-SIMILARITY-TFIDF-K5 per-R 1999 perms, B-MARKOV-1 MLE, B-SHUFFLE-GROUPED-PERM, B-INDEPENDENT-NOISE, B-IID-NULL, CTRL_POS_SYNTHETIC, 4 null controls)
- [x] primary metric frozen (M_OBS_BF_K12, M_REL_SEP_K12 >=200, M_BC_BF_K12 >0.05, M_P_BONF_K12 <0.01, M_GAP_DOM/MARKOV >=0.05 with valid centering |analytic|<0.1 cons<0.03)
- [x] expected direction frozen (H1: rel_sep>=200 and BC>0.05 p<0.01 gaps>=0.05; H0: BC~0/rel_sep<200)
- [x] uncertainty method frozen (trajectory_id permutation 1999 seed42, analytic gammaln/polygamma digamma/trigamma, calibrated_std floor 0.005/0.01, Bonferroni n_tests<=8 floor 0.0005)
- [x] adequacy rule frozen (H>0.05 N>=100 strata>=5 |R|/N 0.01-0.30 |A|>1 MI<0.10 singleton<70% viewport 1280x720 dom>0; synthetic positive must pass G0 else MEASUREMENT_INVALID)
- [x] falsification/survival rule frozen (G0-G6 gated; sig(bank,K,R)=1 iff all thresholds; EXISTS sig=>SURVIVES_CURRENT_TEST else FORALL fail with gates pass=>FALSIFIED-IN-SETTING; proxy substitution forbidden => MEASUREMENT_INVALID/BLOCKED)
- [x] product consequences frozen (positive UNPARK to production manifest with session/permission |S|>=16; negative PARK and pivot Frontier to MemoryArena/WebAPI-bypass/tool-compilation per Director comparative reasoning)
- [x] no outcome-bearing measurements inspected after 2026-09-24T03:36:51.679387Z request creation
