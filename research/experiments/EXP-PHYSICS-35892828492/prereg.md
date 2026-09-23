# EXP-PHYSICS-35892828492 — Preregistration (DESIGN ONLY)

## Status
DESIGN ONLY — not yet frozen. No outcome-bearing measurements have been inspected. Preregistration will be hashed in `freeze.json` before EXECUTE.

## Experiment Identity
- **experiment_id**: EXP-PHYSICS-35892828492
- **lane**: physics
- **claim_ids**: ["C-WEB-DYNAMICS"]
- **parent_handoff**: `research/experiments/EXP-PHYSICS-35860320716/handoff.json` sha256 `93b1bb019c2450cea6678c09e834cf2b010325b918d1f3dd6ad8a27d176a441b` (SUPERSEDE disposition per Director)
- **director_mandate**: PIVOT on C-WEB-DYNAMICS, PIVOT disposition, cognitive_reset=true, cycle_id 35892263700
- **inherited_last_verdict**: MEASUREMENT_INVALID (barrier/committor 6-state overlapping proxy BC 0.171 <0.30 gap 0.011 <0.05 tau 1.0 despite valid centering)

## 1. Question (Director Binding)

Does Bayesian Dir-Multinomial K=12 (and K=24 if state space larger) with exact Gamma-ratio gammaln/polygamma bias correction and trajectory-grouped permutation (unit trajectory_id 1000-1999 perms, seed 42, `|perm-analytic|<0.03`, `|null_mean|<0.1` `null_std>0.01`) detect action-conditioned structure beyond memory on real BrowserGym trajectories (WebShop/TodoMVC at locked 1280x720 CDP `Accessibility.getFullAXTree` with genuine DOM visual bbox, computed style 8 values, AX embedding — not SHA256 hash-truncated) via relative separation (observed log BF exceeds 1999 shuffled null by ≥200 nats, `p_bonf<0.01`) and gap ≥0.05 over B-DOM-SIMILARITY TF-IDF k5 and B-MARKOV-1, where independent-noise control remains BC~0 (`|BC|<0.05 p>0.10`) and analytic null remains centered, reporting absolute BF (expected −10 to −15 nats favoring memory) separately as exploratory, thereby testing whether real Web shows any action-conditioned relative signal without requiring new Gate0 SPAs (`titles≥2 H>0.2 leakage<40%`)?

## 2. Background and Motivation

### 2.1 What has been established (preserved from `carry_forward.established`)

- **TodoMVC hash-SPA infrastructure at 1280x720** is valid for URL-level non-leakage PMI (EXP-PHYSICS-35209110569 PARTIAL_FALSIFICATION, EXP-PHYSICS-35262258744 FALSIFIED-IN-SETTING bounded). Leakage 0.213-0.285 valid-only, achievable NL 357-394 at 500 raw, titles=1 constant (replicates EXP-PHYSICS-34266105229).
- **Synthetic 12-state stochastic SPA**: True `I(Y;A|Z)=1.52` bits. Bayesian DM K=12 is **first estimator to pass C1+C3** on synthetic: observed 167.9-643.1 nats, null_median −78 to −131 nats, `p=0.0005` floor, replication-exact (EXP-PHYSICS-35578258358 SURVIVES synthetic, EXP-PHYSICS-35651906573 positive control replication-exact sha256 `8cff7c33...`).
- **Real TodoMVC Bayesian at K=12**: On 5 TodoMVC variants (vanillajs/react/svelte isomorphic 4-state, vue/angular 3-state, 80 NL/112 valid/144 raw per variant, 6 sessions, deterministic `det_ratio 0.846-0.944`, B2 `accuracy K3=1.0`), Bayesian DM K=12 shows **relative separation real**: observed −10.4 to −15.6 nats vs null_median −24.8 to −39.7 nats, `null_max` −19 to −30 nats, exceeds all 1999 shuffled perms `p=0.0005` on all 15 `(variant×alpha)` cells (EXP-PHYSICS-35651906573 SUPPORTS formally) but **absolute BF negative favoring memory** (M0 wins). Audit REVISE: recomputed BF matches producer bit-identical, but notes effective replications=2 (isomorphic groups), K=12 over-penalizes S=3-4, null negativity trivially from deterministic cells mixing, actionable ceiling is relative-detection not absolute beyond-memory (claim_ceiling bounded to relative separation).
- **Barrier/committor program**: Exact closed-form Dirichlet-Multinomial Gamma-ratio via `scipy.special.gammaln`/`polygamma` (digamma `polygamma(0)`, trigamma `polygamma(1)`, `alpha=1/K`, no heuristic `/100*0.1` blending) with trajectory-grouped perms `seed 42 |perm-analytic|<0.03` achieves **valid centering** (`|analytic_mean| 0.027<0.1 cons 0.029<0.03`) vs heuristic proxy baseline `0.133>0.1` parent (EXP-PHYSICS-35860320716). Correlated genuine overlapping DOM (visual bbox+computed 8-value+AX at 1280x720, 36 prototypes `dom_bytes 443 a11y_bytes 3971`, overlap `hist_intersection 0.667 mean 0.399`) shows `BC 0.171 p_bonf 0.008 d 1.99` but **fails G1** `BC 0.171<0.30 gap 0.011<0.05 tau 1.0` with independent `BC −0.029 p1.0` valid, calibrated `std 0.086`. Bounded to `N=2000` locally-hosted 6-state overlapping proxy at exact `K12/24`. Not falsified globally, only bounded to this bank.
- **Physics program liveness**: 68 attempts, 0 real-Web beyond-memory hits, `C-WEB-DYNAMICS` remains `HYPOTHESIS` (68 prior hypothesis events, 8-streak barrier PARKed, `tunnel_flag true`). `SPIDER at 285 canonical experiments is measurement-constrained`.

### 2.2 What has been rejected / do_not_assume (SUPERSEDE but preserved as distinctions)

- Heuristic `lgamma`-diff proxy `BC 0.689-0.716` with miscentered baseline `0.133>0.1` is **invalid**; exact `gammaln/polygamma` replication drops BC to 0.171 with valid centering.
- Barrier/committor/timescale beyond-memory on this 6-state genuine overlapping-DOM proxy at `N=2000` with exact Gamma-ratio is **bounded rejection** (gap `0.011<0.05`, `tau 1.0 vs 1.0`), not global falsification.
- Repeating same 6-state `66%` overlapping proxy with heuristic `K/N` tuning or deterministic red/blue color would rescue G1 is **bounded rejection** (`K24 cons 0.076>0.03` worse).
- **Do not assume**: C-WEB-DYNAMICS validated; gap `0.011` demonstrates beyond-similarity; barrier `ECE 0.08 Brier 0.07` demonstrates metastable barrier (basins generating, `cluster≠attractor`); `tau 1.0` demonstrates separation; visual/AX/computed_style provide independent evidence (byte-identical `BC 0.171`); BrowserGym WebShop/TodoMVC trajectories were tested (none available per `provenance browsergym_reuse none`); larger N alone fixes blindness; threshold `0.30` may be silently lowered to `0.17`.

### 2.3 Why this experiment (Director comparative reasoning)

- **Vs CONTINUE** exact Gamma-ratio barrier on larger production manifest: Requires Intel relaxed Gate0 `H>0.1 NL≥20` still pending, would be 6th barrier variant after 5 `MEASUREMENT_INVALID`, marginal value low until manifest exists.
- **Vs TERMINATE** physics entirely: Premature given first estimator validation (Bayesian K12 `SURVIVES` synthetic).
- **Vs PIVOT to C-CROSSSITE** website holdout: Requires same missing SPAs, not measurement-ready.
- This test is **low-cost**, uses already-collected BrowserGym trajectories at 1280x720 (`intel relaxed Gate0 optional`), has valid null centering prerequisites (`|perm-analytic|<0.03` etc), and directly answers Scout's question whether physics should stay PARKed. If `BC~0` again, physics remains PARKed while Frontier pivots to `tool-bypass`.
- Tests **synthetic-to-real gap** without demanding new Gate0 SPAs (`titles≥2 H>0.2 leakage<40%`).

### 2.4 Agent priors distinguished (per Director)

All six priors are agent priors, not SPIDER evidence: path dependence `kernel 0.9 exact-intent → 1.0 false_accept`; prompt salience `['path','store'] vs ${sku}`; cached RAG `k=5 cosine 0.55 plateau`; bijective cost `n*3200` masking QCR; self-generated subproblem trap on SPA vs acquiring real distribution `H>0.2`; workflow compilation `WebMCP 714/2147 O(1) vs O(MxN)`. Each distinguished from SPIDER evidence which shows only bounded falsification/measurement-invalid.

## 3. Hypotheses

**H1 (alternative)**: Same as `spec.json hypothesis`. Bayesian DM `K=12` (`K=24` exploratory if `|S_next|≥16`) with exact Gamma-ratio and trajectory-grouped permutation detects action-conditioned structure beyond memory on real BrowserGym trajectories via **relative** separation (`observed - perm_median ≥200 nats, p_bonf<0.01`) and gap `≥0.05` nats over `B-DOM-SIMILARITY TF-IDF k5` and `B-MARKOV-1`, where independent-noise `|BC|<0.05 p>0.10` and analytic centered `|mean|<0.1 cons<0.03`, while absolute BF is `−10 to −15` nats favoring memory (exploratory, not gating).

**H0 (null)**: No real-Web bank achieves relative `≥200 p_bonf<0.01 gap≥0.05` under valid centering/consistency and independent `~0`.

## 4. State / Action / History / DOM Representation

### 4.1 State `S_next`
- Primary WebShop: `SHA256(normalize(URL_after)|normalize(title_after)|DOM_cluster)`; TodoMVC: fragment-aware URL as in EXP-PHYSICS-35651906573 but enhanced with genuine DOM stratification.
- `normalize(URL)` lowercase strip `?session=/?token=` keep `#/` strip trailing `/`; `normalize(title)` trim lowercased 200 chars; `S_next` from `t+1` distinct from `DOM_before` at `t` (no post-state leak).
- Report `|R|/N`, `H(S_next|C)`, `|S_next|` cardinality. `K` handling: `K=12` primary; if `|S_next|≥16` trigger `K=24` exploratory same `alpha=1/K`.

### 4.2 Action `A_leakageFree`
- `A=(primitive,target_sig)` `primitive ∈ {click,fill,navigate,select,submit,hover,type}` `target_sig=role+name+testId+aria-label+bbox cluster` never `href/URL/src`; diagnostic `A_leaky` for gap only; `MI(DOM;Action)<0.10` else tautology.
- Leakage definition `action.target_href == state_after.url` already filtered on prior NL but verify on new BrowserGym banks.

### 4.3 History `H_K`
- Bayesian DM uses `K2=(S_current, last 2 S)` i.e. `(url_before + 2 prev URLs/states)` for `M0 vs M1` as in EXP-PHYSICS-35651906573. Exploratory `H_K=3` also computed.
- Strata key `C=(S_current,H_K)` with `≥5` unique `C ≥3` per stratum; `H(S_next|C)>0.05` required else degenerate ceiling → `MEASUREMENT_INVALID`.

### 4.4 Genuine DOM (not SHA256 truncated)
- `R_visual`: AX bbox `x,y,w,h` quantized 10 bins + `element_count/tree_depth/interactive_density` from `dom_bytes`.
- `R_computed_style`: 8-value `getComputedStyleForNode {color,backgroundColor,visibility,display,opacity,border,position,fontSize}`.
- `R_event_seq`: n-gram last 3 primitives.
- `R_AX_embedding`: `Accessibility.getFullAXTree` serialized `role/name/value` up to 5k + TRAIN-only `TF-IDF k-means 20` clusters or AX embedding; not SHA256 hash-truncated single value.
- Preserve raw: `dom_snapshot, a11y_tree, visual_json, style_dict, event_seq, AX bytes`; doc quantization/viewport. Primary requires `≥1 R` genuine. Overlapping spectra verification documented (style/visual/AX distributions overlap not deterministic regime-color).

## 5. Estimator and Bias Correction

- **Exact Dirichlet-Multinomial marginal likelihood** via `scipy.special.gammaln` and `polygamma` (`digamma polygamma(0)`, `trigamma polygamma(1)`): `log ML = Σ_c [gammaln(K*alpha)-gammaln(N+K*alpha)+ Σ_i(gammaln(n_i+alpha)-gammaln(alpha))]` with `K=n_states (12 primary 24 exploratory)` **not** `len(counts)`, `alpha_prior ∈ {0.5,1.0,2.0}` primary `1.0` reporting, `0.5/2.0` sensitivity. `log BF = log ML(M1)-log ML(M0)` in nats. Code path `research/physics/run_experiment.py _dirichlet_multinomial_log_marginal` with `K=n_states`; verification `grep gammaln polygamma` logged in provenance.
- **Analytic null** `mean/std` via exact Gamma-ratio from DM (`gammaln/polygamma`) **not** heuristic `/100*0.1` or `sqrt(mean(1/(2n)))*0.1` blending (audit rejection). `BC = observed - analytic_mean`.
- Also compute plug-in CMI bits for gap diagnostics via same strata.

## 6. Data Collection and Sampling

### 6.1 Trajectory banks
- **Primary**: BrowserGym WebShop at locked `1280×720` (`BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0` pinned) via `CDP Accessibility.getFullAXTree` + `DOM.getDocument` + `DOM.getBoxModel` + `CSS.getComputedStyleForNode`. Reuse existing WebShop/TodoMVC `1280×720` banks if manifest `research/intel/manifest.json` shows `browsergym_reuse` with `dom_bytes>0 a11y_bytes>0 viewport 1280x720`.
- **Secondary**: BrowserGym TodoMVC same pipeline (richer genuine DOM vs prior SHA256 URL-only). Both banks `N=1000-1999` (50 sessions ×20-40 steps or as collected). If not available, collect new WebShop `categories/search/cart/checkout` and TodoMVC at locked `1280×720` (honest cost, no `f*6.0` jitter).
- **Positive control bank**: Synthetic 12-state stochastic hash-routed SPA `N=5000 seed 42` (same as EXP-PHYSICS-35578258358) with same estimator; no browser needed.
- **Independent-noise bank**: Same WebShop/TodoMVC FSM but action-state dependence destroyed via per-step independent within-trajectory shuffle (regime-independent sampling, not `S_current%2`, same 1280×720 viewport, same `K`).
- **IID bank**: Same marginal `P(S)` i.i.d. with genuine DOM still sampled.

### 6.2 Collection details
- `PYTHONHASHSEED=0`, `numpy seed 42`, never `hash(site)`; `trajectory_id` as resampling unit; `VIEWPORT 1280×720` verified before claiming genuine (`dom_bytes>0 visual_json>0 a11y_bytes>0`).
- At least `100` NL transitions per bank or report `H(S_next|C)` and `|R|/N`; `H(S_next|C)≤0.05` → `MEASUREMENT_INVALID` ceiling not falsification.
- Honest cost: `sum counters resolve+bind+verify+freshness+browser_steps`, no `f*6.0` jitter, `|rho_shuffled|<0.20` per Director Scout discipline.

## 7. Baselines and Controls

### 7.1 Baselines (stable identities)

- **B-DOM-SIMILARITY-TFIDF-K5** (`B-DOM-SIMILARITY`): `TF-IDF cosine k=5` over genuine DOM text (`visual text+bbox + AX name/role`) fit **TRAIN only** `70/30` by `trajectory_id`, `5-NN` predicted `S_next` without stratification; `BC_sim` via same exact Gamma-ratio `K analytic+perm gammaln/polygamma`; primary must exceed by `gap≥0.05 nats`; `|analytic_mean|<0.1 cons<0.03` required else invalid.
- **B-MARKOV-1** (`B-MARKOV-1`): `P(S_next|S_current,A_leakageFree)` MLE `TRAIN` by `trajectory_id` without DOM; `BC_markov1` same analytic+perm; `gap≥0.05` required.
- **B-MARKOV-K3** (`B-MARKOV-K3`): `P(S_next|S_current,H_K=3)` stratified majority; reports `BC_hist, accuracy, H`; `H>0.05` diagnostic.
- **B-SHUFFLE-GROUPED-PERM**: trajectory-grouped 1000-1999 within-strata shuffles of action labels by `trajectory_id seed 42` → `perm mean/std/p`; analytic `mean/std` via `gammaln/polygamma` for `|perm-analytic|<0.03` and `|analytic|<0.1`.
- **B-INDEPENDENT-NOISE-GENUINE**: independent per-step genuine DOM `≥6 variants/state` same `1280×720` but regime-independent shuffling, identical DM + grouped perms `N=1000-1999`; `|BC|<0.05 p>0.10 |analytic|<0.1`; confound → `MEASUREMENT_INVALID`.
- **B-IID-NULL**: `i.i.d. S_next` same marginal `P(S)` `seed 42`; `|BC|≤0.05 p>0.10`.

### 7.2 Positive control
- **CTRL_POS_SYNTHETIC** (`positive_control`): Synthetic 12-state stochastic SPA `N=5000 seed42` must achieve `observed 168-643 nats`, `null_median −78 to −131`, `p=0.0005` floor, `|perm-analytic|<0.03`, `|analytic|<0.1`, `calibrated_std valid`, `|R|/N` diagnostic. Failure → `MEASUREMENT_INVALID`. Secondary deterministic SPA `log BF≫0`.

### 7.3 Null controls (stable identities)
- **CTRL_NULL_GROUPED_PERM** (`null_control` permutation): Trajectory-grouped 1000-1999 perms `seed42 |perm-analytic|<0.03 |null_mean|<0.1 null_std>0.01 p_bonf<0.01` for significance.
- **CTRL_ANALYTIC_CENTERING**: `|analytic_mean|<0.1` on BC scale, `consistency<0.03`.
- **CTRL_INDEPENDENT_NOISE** (`null_control` independent): `|BC|<0.05 p>0.10 |analytic|<0.1 valid`; failure → `MEASUREMENT_INVALID` confounded (including prior `S_current%2` style).
- **CTRL_IID_NULL**: `|BC|≤0.05 p>0.10`.
- Audit verifies source contains `gammaln/polygamma` and not heuristic `sqrt(mean(1/(2n)))*0.1`.

## 8. Measurement Validity (pre-registered gates)

All listed in `spec.json measurement_validity` plus:
- **Genuine DOM verification**: `dom_bytes>0 a11y_bytes>0 visual_json>0 computed_style>0 viewport 1280×720` and not SHA256 truncated; overlapping spectra documented.
- **Absolute vs relative discipline**: Absolute `observed log BF` is exploratory (expected `−10 to −15` at `K12` on TodoMVC due to `K` over-penalty on `S=3-4`; report per `alpha_prior 0.5/1.0/2.0`); primary gating is **relative** `observed - perm_median ≥200`.
- **Train-only integrity**: `TF-IDF vocab/embedding centroids/Dirichlet counts/k-means` fit `TRAIN only 70/30 by trajectory_id`; holdout gaps reported; site identity never feature.
- `H(S_next|C)>0.05` and `|R|/N 0.01-0.30` non-degenerate required.

## 9. Decision Rule (frozen, verbatim from `spec.json decision_rule`)

Gated execution in order; any validity gate triggers `MEASUREMENT_INVALID` and prevents primary `SURVIVES/FALSIFIED` claim.

Gates (`MEASUREMENT_INVALID` if any fail):
- **G0** synthetic positive: `observed≤0 OR perm p≥0.001 OR |analytic_mean|≥0.1 OR calibrated_std degenerate OR |perm-analytic|≥0.03` → `pipeline blind/miscalibrated`.
- **G1** independent-noise: `BC independent |BC|≥0.05 p<0.10 valid` → `confounded`.
- **G2** IID null: `BC>0.05 p<0.10 valid` → `null miscentered`.
- **G3** `H(S_next|C)≤0.05 OR N<100 OR <5 strata ≥3` → `degenerate ceiling`.
- **G4** primary `|perm-analytic|≥0.03` on primary `K12` (both WebShop and TodoMVC banks) → `model mismatch`.
- **G5** viewport/DOM genuine fails (`no dom_bytes/visual/computed/AX>0 OR viewport≠1280×720 OR SHA256 truncation`) → `substrate missing`.
- **G6** `TRAIN` leakage or `trajectory_id` not used → `split invalid`.

If no G fails, primary per real-Web bank (`WebShop` primary, `TodoMVC` secondary): for `K12` (and `K24` if `|S_next|≥16`) compute `M_OBS_BF, M_NULL_MEDIAN/MEAN/STD/MAX, M_ANALYTIC_MEAN/STD, M_CONS=|perm-analytic|, M_REL_SEP=M_OBS-M_NULL_MEDIAN (nats), M_BC=M_OBS-M_ANALYTIC_MEAN, p_raw=(count_ge+1)/(N_perm+1), p_bonf=min(1,p_raw*n_tests) n_tests≤8 floor 0.0005, gaps G_DOM=M_REL_SEP−B_DOM_REL_SEP and G_MARKOV=M_REL_SEP−B_MARKOV_REL_SEP`. `sig(bank,K)=1` if `M_REL_SEP≥200 nats AND p_bonf<0.01 AND |analytic_mean|<0.1 AND calibrated_std valid (>0.005 analytic or >0.01 perm) AND cons<0.03 AND G_DOM≥0.05 AND G_MARKOV≥0.05 AND independent~0 (|BC|<0.05 p>0.10) AND |R|/N 0.01-0.30`.

- **If EXISTS bank `sig==1` → `SURVIVES_CURRENT_TEST`**: real Web shows detectable action-conditioned **relative** structure beyond memory/similarity at exact centering, bounded to that `bank/K`. Report absolute BF exploratory (`−10 to −15` expected) separately and do **not** gate on its sign.
- **If FORALL banks sig fails while gates pass → `FALSIFIED-IN-SETTING`**: even correctly centered Bayesian DM with trajectory-grouped permutation shows `BC~0 / relative <200 / gap<0.05` on real BrowserGym WebShop/TodoMVC at `1280×720` with genuine DOM, no detectable beyond-memory action-conditioned relative signal at `N=1000-1999` with this representation; physics remains `PARKed`.

Exploratory `K24` per-branch `BC 0.126 style` consistency reported but not gating unless `K12 sig` already.

## 10. Primary Metrics (stable identities for AUDIT)

- `M_OBS_BF_K12`, `M_OBS_BF_K24` (nats)
- `M_NULL_MEDIAN_K12`, `M_NULL_MEAN_K12`, `M_NULL_STD_K12`, `M_NULL_MAX_K12`, `M_ANALYTIC_MEAN_K12`, `M_ANALYTIC_STD_K12`, `M_CONSISTENCY_K12=|perm-analytic|`
- `M_BC_BF_K12 = M_OBS - M_ANALYTIC_MEAN` (nats)
- `M_REL_SEP_K12 = M_OBS - M_NULL_MEDIAN` (nats) — primary gating ≥200
- `M_P_RAW_K12`, `M_P_BONF_K12` (Bonferroni `n_tests≤8` floor `0.0005`)
- `M_GAP_DOM_K12`, `M_GAP_MARKOV_K12` (nats, ≥0.05)
- `M_ABSOLUTE_BF_K12` (same as `M_OBS`, exploratory −10 to −15 expected)
- `M_INDEPENDENT_BC_K12`, `M_INDEPENDENT_P_K12`, `M_INDEPENDENT_ANALYTIC_MEAN_K12`
- `M_IID_BC_K12`, `M_BASELINE_DOM_TFIDF_K5_BC`, `M_BASELINE_MARKOV1_BC`
- `M_H_SNEXT_GIVEN_C`, `M_R_OVER_N`, `M_CALIBRATED_STD_K12 = max(analytic_std, perm_std)`

Corresponding `K24` metrics suffixed `_K24` if triggered.

## 11. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Deterministic FSM (TodoMVC `det_ratio 0.846-0.944`, `B2 1.0`):** `H(S_next|C)` near 0, perm null heavily negative from mixing deterministic cells (prior `null_median −24 to −39`), trivial `C1 |null|<0`? | Report `H(S_next|C)` per bank; require `H>0.05`; WebShop bank provides stochastic heterogeneity; acknowledge absolute BF negative exploratory; primary is **relative** not absolute, with independent~0 guard. |
| **K=12 over-penalty on S=3-4:** `K*alpha=12*1` dominates `N` per cell, `BF −10 to −15` even when relative signal exists (EXP-PHYSICS-35651906573 validity_notes[4]) | `K12` frozen primary; report `K12` absolute exploratory; trigger `K24` only if `|S_next|≥16`; sensitivity to `K={3,4,5}` reported exploratory not gating; gap over baselines uses same `K` so penalty cancels. |
| **Isomorphic replication inflating n (`vanillajs/react/svelte` bit-identical):** Effective replications `2` not `5` (audit REVISE) | Treat `WebShop` vs `TodoMVC` as distinct banks; do not pool `5` TodoMVC variants as independent; report `per-variant` but gate on `bank` level; note isomorphism in `validity_notes`. |
| **Genuine DOM vs SHA256 truncation:** Prior representation collapse (single hash truncated `|R|/N 0.017`) | Verify `dom_bytes>0 a11y_bytes>0 visual bbox+computed 8-value+AX embedding` preserved; audit checks source not SHA256-only; report `|R|/N 0.01-0.30` genuine finite vocab with overlapping spectra. |
| **Viewport heterogeneity:** Prior 1024×768 vs mandated 1280×720 changes bbox | Lock `1280×720` via `CDP` + `Page.setViewportSize`; verify `viewport 1280×720` in provenance; reject if `≠1280×720`. |
| **Trajectory grouping vs transition-level shuffle:** Transition-level inflate `p` vs trajectory-level valid (handoff `31/4 divergent ECE 0.08` but `S_current%2` confound) | Enforce `trajectory_id` unit, `1000-1999` perms `seed42`, `|perm-analytic|<0.03` guard; independent-noise `BC~0` confirms not `S_current%2`. |
| **Heuristic bias correction masquerading as exact:** Parent `0.689-0.716 BC` with `/100*0.1` blending invalid | Require `scipy.special.gammaln/polygamma` exact; audit `grep` verification; no `sqrt(mean(1/(2n)))*0.1` or `+0.012` floor. |
| **Multiple testing inflation (`n_tests≤8` isomorphic):** Bonferroni overcounts visual/AX/computed | `p_bonf=min(1,p_raw*n_tests) n_tests≤8 floor 0.0005`; note effective `2-3` for isomorphic Rs; report both `p_raw` and `p_bonf` per Rs. |
| **Small N (80 NL prior) vs target 1000-1999:** Power limited, `calibrated_std` degenerate `0.006 perm 0.086 analytic` | Require `N≥100` valid per bank `H>0.05`; WebShop bank should provide `≥1000` if manifest available; else collect until `≥1000` or report `MEASUREMENT_INVALID` ceiling. |
| **Action encoding degeneracy (`action_target None` constant `log BF 0`):** prereg `target_href` only meaningful for leakages filtered | Use `A_leakageFree=(primitive,target_sig)` never `href`; verify `MI(DOM;Action)<0.10` tautology check; report `degenerate_action_target` diagnostic `log BF 0.000` as in prior. |

## 12. Product Consequences

- **Positive (`SURVIVES`)**: First real-Web action-conditioned **relative** signal beyond memory at exact centering (`|analytic|<0.1 cons<0.03 std>0.01`) with `relative ≥200 p_bonf<0.01 gap≥0.05` on `≥1` real bank at `1280×720` genuine DOM while `independent~0` bridges synthetic-to-real gap; absolute BF `−10 to −15` remains exploratory (memory wins absolutely at `K12` due to penalty). Unparks Physics for production manifest with real session/permission regimes and larger state spaces; product distills relative-signal detector as `freshness/barrier guard` (`regime-aware retrieval`, `visual+AX signature`, `event-seq guard`) into `kernel resolve/verify`; quantify `delta-repair` cost and cross-site holdout transfer; no generic promotion until absolute BF and transfer validated.
- **Negative (`FALSIFIED-IN-SETTING` with valid gates)**: Closes Bayesian relative-signal program on `BrowserGym WebShop/TodoMVC N=1000-1999 genuine 1280×720` even correctly centered → no detectable beyond-memory relative signal at this scale/representation; physics remains `PARKed` pending larger production manifest with real session/permission latent regimes and larger `|S|`; Frontier `PIVOT` to orthogonal `MemoryArena / WebAPI bypass / compile-execute / tool-bypass`. Do **not** invest in this Bayesian DOM-conditioned dynamics as mechanical prior at current `N`.

## 13. Estimated Cost / Expected Information Gain

- **Estimated cost**: Low: reuses existing BrowserGym trajectory banks at `1280×720` if available plus optional locally-hosted `6-state` genuine capture `<10 min headless`; analysis `80-120k` exact `gammaln/polygamma` fits `<1ms` each + `TF-IDF` `<5 min`; `scipy+sklearn+headless Chromium` if needed; total `<2h wall-clock <8GB RAM no GPU`.
- **Expected information gain**: Very high and tunnel-breaking per Director: `vs CONTINUE barrier` on larger manifest (requires `Gate0` still pending) and `vs TERMINATE` (premature) this low-cost real-trajectory test directly answers whether physics should stay `PARKed`. Either `relative ≥200 gap≥0.05` (first real-Web beyond-memory relative detection despite absolute `−10 to −15`) or persistent `BC~0 / relative <200` (justify `PARK` and Frontier orthogonal pivot) finally adjudicates barrier program without requiring new Gate0.

## 14. Inherited Parent Handoff Carry-Forward (exact, SUPERSEDE but preserved as distinctions)

### Established (from EXP-PHYSICS-35860320716)
1. Descriptive at locked `1280×720` via `Playwright CDP Accessibility.getFullAXTree` on locally-hosted `6-state SPA (50×40 N=2000, latent regime per-trajectory A/B bias 0.70/0.30 mirrored basins {0,1,2} vs {3,4,5}, p_stay 0.70, URL fragment https://spa.local/#/state_S)`: `36` genuine prototypes (`state 0-5 × regime A/B × variant 0-2, dom_bytes 443 a11y_bytes 3971`), overlap `hist_intersection_color 0.667 mean_overlap 0.399>0.3` verified overlapping not deterministic red/blue, `MI(DOM;Action) 0.0<0.10` leakage-free `Action (primitive,target_sig)` never `href`, `|R_visual|/N 0.017 |R_computed_style|/N 0.006 |R_ax|/N 0.018`, `H(S_next|C) 2.329 bits>0.2` valid ceiling, `24/24` strata `≥3 singleton 0.0`, viewport verified.
2. Exact closed-form `Dirichlet-Multinomial Gamma-ratio` analytic bias correction via `scipy.special.gammaln/polygamma` (`alpha=1/K K=12 primary K=24 exploratory`, no heuristic blending, no `sqrt(mean(1/(2n)))*0.1`) with `trajectory_id` grouped `1000` perms `seed42`: correlated `R_visual/AX/computed_style` observed `CMI 0.199 perm −0.002 analytic_mean 0.027 cons 0.029 BC 0.171 p_bonf 0.008 d 1.99`; `R_event_seq BC −0.000 p1.0`; `calibrated_std 0.086 valid (>0.005)`, `|analytic_mean| 0.027<0.1` valid; `K24 BC 0.126 cons 0.076 vs K12 0.171`.
3. Baselines same exact `K analytic+perm TRAIN-only 70/30 by trajectory_id: B-DOM-SIMILARITY TF-IDF k5 R_visual BC_sim 0.161 analytic_mean 0.026 cons 0.027 acc 0.277` (now valid centering `|analytic|<0.1 cons<0.03` vs parent `0.133/0.053`); `B-MARKOV-1 BC −0.0035 acc 0.20 gap 0.011 (<0.05 required)`; `B-MARKOV-K3 BC −0.0035 acc 0.17`; `B-SHUFFLE-GROUPED perm −0.002 analytic 0.027 cons 0.029` valid.
4. Independent-noise genuine overlapping replication (`50×40 N=2000 ≥6 variants/state` regime-independent via same `1280×720` overlapping prototypes, not `S_current%2`) verified fix: `R_visual BC −0.029 p1.0 analytic 0.033 cons 0.035`, `computed_style −0.029`, `AX −0.029`, `event −0.000` all `|BC|<0.05 p>0.10 |analytic|<0.1` — pipeline not confounded.
5. `Pipeline blindness quantified: G1 requires BC≥0.30` for genuine correlated overlapping proxy with `66%` color bias and valid analytic centering; observed `0.171<0.30` fails despite `p_bonf 0.008 cons 0.029 ECE 0.08` — exact estimator correctly centered but insensitive at this overlapping fidelity and `N/K`.

### Rejected
- Heuristic `lgamma`-diff proxy `BC 0.689-0.716` with `0.133>0.1` is invalid bounded rejection; barrier beyond-memory on this `6-state` proxy at `N=2000` bounded rejection; `tau_corr>5` bounded rejection; gap `0.011<0.05` bounded rejection; `event_seq` beyond-memory bounded rejection; repeating same `6-state 66%` proxy with heuristic tuning bounded rejection.

### Unknown (must not assume)
- What `BC/analytic/std/p_bonf/gap/ECE/Brier/tau` would be on **genuine BrowserGym WebShop/TodoMVC** at `1280×720` via `CDP` with genuine `visual bbox+computed 8-value+AX embedding` under exact `gammaln/polygamma` and `trajectory_id` grouping (`N=1000-1999 K12/24 |perm-analytic|<0.03`) — none available per `research/intel/manifest.json` provenance.
- Whether larger production-proxy with real `session/permission latent regime` and richer multi-feature genuine DOM would achieve `G1 BC≥0.30 gap≥0.05` or remain `BC~0`.
- Correct `Dirichlet-Multinomial variance` formula for stratified CMI and whether multi-feature `R` combining visual+computed+AX improves gap beyond `0.011` without tautology.

### Do Not Assume (unsafe)
- `C-WEB-DYNAMICS` validated; `FALSIFIED-IN-SETTING` globally closes dynamics (bounded to `N=2000 6-state` proxy); gap `0.011` demonstrates beyond-similarity; barrier `ECE 0.08` demonstrates metastable barrier (`cluster≠attractor`); `tau 1.0` demonstrates separation; `analytic 0.027` heuristic; visual/AX/computed independent; BrowserGym trajectories tested; larger `N` alone fixes blindness; allow silent threshold relaxation to `0.17` (`G1 BC≥0.30` frozen).

## 15. Preregistration Freeze Checklist

- [ ] `spec.json` frozen with above `question/hypothesis/falsifier/baselines/positive_control/null_control/measurement_validity/decision_rule` and stable metric/control identities
- [ ] `prereg.md` (this file) frozen with above 8.1 exact `gammaln/polygamma`, 7 barrier/timescale, 10-13 gates G1-G6, validity threats, absolute vs relative discipline, `H>0.05`, `|R|/N`, `TRAIN-only`, `trajectory_id` grouping
- [ ] `request.json` `director_mandate` stored immutable with `agent_priors_used[6]` distinguished
- [ ] `freeze.json` deterministic hashes of `request.json` + `spec.json` + `prereg.md` before EXECUTE
- [ ] No outcome-bearing measurements inspected during DESIGN (synthetic positive control numbers are parent evidence, not this experiment's outcomes)

## 16. References

- Parent synthetic Bayesian: `research/experiments/EXP-PHYSICS-35578258358` (`SURVIVES` synthetic `K12` exact)
- Real TodoMVC Bayesian: `research/experiments/EXP-PHYSICS-35651906573` (`SUPPORTS` formally but `REVISE` audit `absolute BF −10 to −15` gap relative, isomorphic `2` effective)
- Barrier G1: `research/experiments/EXP-PHYSICS-35860320716` (`MEASUREMENT_INVALID BC 0.171<0.30 gap 0.011` exact `gammaln/polygamma` valid centering)
- Code reuse: `research/physics/run_experiment.py _dirichlet_multinomial_log_marginal`, `research/physics/execute_35860320716.py analytic_dm_mean_std_exact gammaln/polygamma`, `research/experiments/EXP-PHYSICS-35651906573/run_experiment.py`
- Substrate pins: `BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0` at `1280×720`, honest cost `sum resolve+bind+verify+freshness+browser_steps` no `f*6.0` jitter `|rho_shuffled|<0.20`

---
*End of preregistration. EXECUTE must run exactly this frozen design, preserving raw evidence → observation → derived measurement → interpretation distinction, with `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved` in `result.json`.*
