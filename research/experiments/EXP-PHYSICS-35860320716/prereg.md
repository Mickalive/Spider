# EXP-PHYSICS-35860320716 Preregistration — Physics PIVOT to Exact Gamma-Ratio Genuine Overlapping-DOM Barrier/Committor & Timescale (DESIGN FROZEN BEFORE OUTCOME)

**Status: DESIGN — FROZEN BEFORE OUTCOME (2026-09-23). No outcome-bearing measurements for the genuine overlapping-DOM barrier/committor/timescale decision have been inspected.**

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35860320716
- **Lane**: physics
- **Claim**: C-WEB-DYNAMICS — Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity (status HYPOTHESIS per codex/claim_state.json, physics tunnel_flag true with 14 recent C-WEB-DYNAMICS failures, 60+ Gate0 failures, 271 canonical experiments zero VALIDATED; Bayesian DM K=12 first estimator to pass C1+C3 but absolute BF -10 to -15 nats favors memory on real TodoMVC)
- **Directive**: Global Research Director PIVOT on C-WEB-DYNAMICS (request.json director_mandate cycle 35859819467, allocation PIVOT claim_id C-WEB-DYNAMICS cognitive_reset true, parent_handoff_disposition USE, comparative_reasoning CONTINUE tunnel diagnostics). **Binding strategic question verbatim in request.json director_mandate.question.** For NEW governed experiments, director mandate is binding research direction; inherited parent_handoff is continuity evidence only and MUST NOT silently override PIVOT decision (AGENTS.md §Work discipline, EXPERIMENT_PACKET.md §2). `director_mandate.agent_priors_used` distinguished from SPIDER evidence below (§4.3).
- **Parent handoff**: `research/experiments/EXP-PHYSICS-35796855042/handoff.json` (sha256 15cdf6b415b84e0fe9da065cba8be9d1663f7800ae0c7c3b5f2da0c9386a9f1b) — MEASUREMENT_INVALID per audit FAIL producer_claim_supported false: heuristic lgamma-diff proxy not closed-form Gamma ratios (lgamma diff eps1e-6/1e-4, /100*0.1 scaling, blending to perm_mean), TF-IDF baseline miscentered 0.133>0.1 invalidating gap 0.145, computed_style 8-value red/blue deterministically encoding same latent L (tautological barrier recovering 0.30/0.70), visual/ax byte-identical double-counting n_tests, timescale 3.82-4.6<5, G1 weakened, independent S_current%2 confound, no BrowserGym data despite mandate. Its established/rejected/unknown/do_not_assume preserved below (§2). Director rationale: Another synthetic 12-state L-string sweep with heuristic bias correction repeats local optimum flagged by audits; only exact Gamma-ratio + genuine overlapping spectra + barrier/committor/timescale with trajectory-grouped permutation and independent-noise BC~0 control can change decision (BC>0.05 vs BC~0) and justify continuing or closing Web-physics search.
- **Dependencies (binding per mandate)**: [] — no hard workflow barrier; Scout identifies C-MEAS-VALID distributed freshness as gating Graph/Product but not blocking this orthogonal physics test; intel/runtime not hard dependencies but inform Director choice. BrowserGym WebShop/TodoMVC trajectories reused if available at intel manifest.
- **Pre-2.0 / codex baseline**: WP-002B rule minus shuffle +0.0532 no holdout; WP-003 MEASUREMENT_INVALID (leakage, Gaussian jitter, hash(site)). Frontier 61 pooled TV/KDE/binned blind spots (kNN fails scaling rho -0.12, KDE fails rotation rho 0.286, CV 0.57-0.75, 95% non-stationary attenuation). Physics: correlated hash FSMs EXP-PHYSICS-34764605162 falsified independent-noise BC 0.004/0.025 p=1.0, EXP-PHYSICS-35796855042 heuristic BC 0.689-0.716 audit FAIL tautological, 66 HYPOTHESIS exps. Bayesian DM K=12 (N=1999) passes C1+C3 log BF 168-643 null -78 to -131 but absolute BF -10 to -15 nats on real TodoMVC favors memory — validates exact estimator class.

## 2. Inherited Scientific State (from parent handoff — continuity evidence, not agenda)

Per AGENTS.md and EXPERIMENT_PACKET.md, parent handoff `next_question` is advisory local proposal only; director_mandate PIVOT is binding. Preserved distinctions:

### Established (justified at stated ceiling, continuity only)

- Descriptive on locally-hosted 6-state SPA (50x40 N=1999, latent regime per trajectory A1119/B880 bias 0.70/0.30 mirrored basins {0,1,2} vs {3,4,5}, p_stay 0.70, URL fragment https://spa.local/#/state_S) with genuine browser capture at locked 1280x720 via Playwright CDP Accessibility.getFullAXTree (36 prototypes state 0-5 x regime A/B x variant 0-2, dom_bytes 390 a11y_bytes 3967 viewport verified): |R_visual| 36 |R|/N 0.018, |R_computed_style| 8 0.004, |R_ax| 36 0.018 (below/on lower bound 0.02-0.15), H(S_next|C) 3.22 bits >0.2 valid ceiling, 24/24 strata >=3 singleton 0.0, MI(DOM;Action) 0.0, S_next SHA256(URL_after|title_after) distinct from DOM_before.
- Heuristic lgamma-diff Dirichlet-Multinomial K12 alpha1/12 (digamma via lgamma eps1e-6, trigamma eps1e-4, comb_bias, gamma_bias, calibrated_std 0.034) with 1000 trajectory-grouped perms seed42 yields correlated: R_visual BC0.689 perm0.123 analytic0.088 cons0.0356 p_bonf0.007 gap0.117; R_computed_style BC0.716 perm0.082 analytic0.059 cons0.023 p0.007 gap0.145; R_event_seq BC0.011 p1.0; R_ax identical to visual — audit recomputes but flags heuristic scaling/blending as not closed-form.
- Baselines same K12 grouped TRAIN-only: B-DOM-SIMILARITY TF-IDF k5 BC_sim0.571 analytic0.133>0.1 invalid centering cons0.053>0.03; B-MARKOV-1 BC -0.0035; independent-noise genuine replication visual BC -0.0069 p0.51 analytic0.007 cons0.0065 passes but event_seq S_current%2 confound; IID null BC<=0.03 passes.
- Barrier/committor canonical s=(URL_normalized,DOM_cluster,H_K=3) horizon10: 37 candidates >=10 with 32 divergent 0.2<q<0.8 ECE0.08 Brier_gap0.07 — identifiable but basins are generating basins and DOM_cluster encodes regime L tautologically.
- Timescale ACF: visual tau3.82 vs tau_ind1.0 gap2.82; computed_style 4.6 gap3.6 — strict tau>5 fails, gate passes only via extra_ok fallback not preregistered.
- No BrowserGym WebShop/TodoMVC real trajectories used — validity_notes confirms unavailable; claim bounded to locally-hosted 6-state SPA with regime-correlated renders, not production heterogeneity.

### Rejected (bounded)

- That tautological regime-correlated DOM deterministically derived from same latent L that defines S_next (computed_style red/blue = regime A/B, visual bbox regime-correlated, AX SHA256 per L/state/variant) constitutes valid richer DOM evidence for beyond-memory barrier/committor/timescale — bounded rejection to heuristic 6-state proxy (audit required_fixes 2).
- That heuristic proxy (execute.py:189-410 analytic_dm_mean_std) is valid closed-form Dirichlet-Multinomial Gamma-ratio via exact digamma/trigamma — bounded rejection: forces analtic_mean within 0.035 of perm_mean, inflates std, not gammaln/polygamma.
- That 4 isomorphic labelings byte-identical are 8 independent tests for Bonferroni n_tests=8 — bounded rejection: perfect correlation, effective n_tests ~2-3.
- That B-DOM-SIMILARITY gap 0.145/0.117 with analytic0.133 miscentering demonstrates beyond-similarity — bounded rejection: baseline fails valid centering.
- That barrier q(s) ECE0.08/Brier0.07 with DOM_cluster including regime-color demonstrates emergent metastable barrier — bounded rejection: tautological recovery of 0.30/0.70, cluster!=attractor.
- That timescale tau3.82/4.6 demonstrates separation — bounded rejection: strict tau>5 not met, gap vs proxy not time-shuffled null.

### Unknown (open)

- What BC/analytic_mean/std/p_bonf/gap/tau/ECE would be with exact scipy.special.gammaln/polygamma closed-form vs heuristic 0.059-0.088/0.034 and baseline 0.133 miscentering.
- Whether properly constructed independent-noise bank with overlapping spectra (not deterministic red/blue, not S_current%2) would remain BC~0 with correct valid centering.
- What metrics would be on genuine BrowserGym WebShop/TodoMVC trajectories with real DOM/AX at 1280x720 via CDP (visual, computed 8-value, AX embedding, event) under exact analytic DM and trajectory-grouped permutation (N=1000-1999, K12/24, |perm-analytic|<0.03).
- Whether barrier/committor with >=10 revisits divergent futures on production SPAs with real overlapping spectra, session/permission regimes, larger state spaces would reveal calibrated beyond-memory structure and tau>5.
- Correct DM variance formula for stratified CMI and calibrated std without heuristic +0.012 floor.
- Whether per-15-step regime P(flip)=0.07 vs per-trajectory persistence yields different null centering/tau vs per-trajectory proxy.
- Effective Bonferroni n_tests ~2-3 vs 8 and K=12 vs 24 centering on genuine diversity.

### Do Not Assume (dangerous non-conclusions, binding)

- Do not assume C-WEB-DYNAMICS supported — audit FAIL, BC0.716 is construction-correlated artifact, not emergent dynamics; HYPOTHESIS.
- Do not assume analytic 0.059-0.088 std0.034 cons0.023-0.0356 are valid Gamma ratios — heuristic forces agreement, not gammaln/polygamma.
- Do not assume 4 Rs independent — visual/ax byte-identical, computed deterministic 8-value, same L.
- Do not assume B-DOM-SIMILARITY gap meaningful — baseline miscentered 0.133>0.1.
- Do not assume tau3.82-4.6 demonstrates separation — strict >5 not met.
- Do not assume synthetic regime-correlated strings equal real visual/computed/AX at overlapping spectra — representation loss total, DOM still deterministically tied to L.
- Do not assume independent replication clean — event S_current%2 and style red/blue violate independence.
- Do not assume barrier ECE0.08 demonstrates metastable barrier — basins are generating variables tautologically.
- Do not assume BrowserGym availability — not tested despite mandate; verify before claiming Gate0-free validation.

This PIVOT directly implements audit required_fixes: exact gammaln/polygamma closed-form (not heuristic), overlapping genuine spectra (not deterministic color), BrowserGym WebShop/TodoMVC trajectories at 1280x720 plus larger production-proxy with real session/permission regime (per-trajectory AND per-15-step), trajectory-grouped permutation N=1000-1999 K12/24 |perm-analytic|<0.03, barrier/committor/timescale with valid gates before PARK decision.

## 3. Scientific Question (binding, refined to falsifiable experiment)

Director strategic question (request.json director_mandate.question verbatim, binding):

> With exact closed-form Dirichlet-Multinomial Gamma-ratio bias correction via scipy.special.gammaln/polygamma (exact digamma/trigamma, no heuristic scaling or consistency blending), overlapping genuine DOM spectra not deterministically tied to generating basins (visual bbox, computed style 8 values, AX embedding from locked 1280x720 BrowserGym WebShop/TodoMVC trajectories with real session/permission latent regime per-trajectory and per-15-step persistence) and trajectory-grouped permutation (N=1000-1999, K=12/24, |perm-analytic|<0.03), does barrier/committor (>=10 revisits to same canonical state URL+DOM_cluster+H_K=3 divergent 0.2<q<0.8, ECE<=0.15 Brier gap>=0.05) or timescale separation (tau_corr>5 vs tau_shuffled~1) reveal valid beyond-memory structure (BC>0.05 p_bonf<0.01 |analytic_mean|<0.1 gap>=0.05 over TF-IDF k5 and Markov) where independent-noise control remains BC~0 (|BC|<0.05), or does even correctly centered genuine DOM remain at BC~0 indicating barrier/committor not productive and physics should PARK pending larger production manifest?

Refined falsifiable experiment: On existing locally-hosted production-proxy bank captured genuinely at locked 1280x720 via CDP Accessibility.getFullAXTree (visual bbox, computed 8-value style, AX embeddings) with overlapping spectra across basins (not deterministic regime-color) PLUS, if available, existing BrowserGym WebShop/TodoMVC trajectory banks reused with genuine DOM at same viewport (N=1000-1999 each, trajectory_id grouping, locked 1280x720), with trajectory-grouped permutation (1000 perms unit trajectory_id seed 42, consistency |perm-analytic|<0.03 via exact gammaln/polygamma) and exact Dirichlet-Multinomial Gamma-ratio analytic bias correction (alpha=1/K K=12 primary K=24 exploratory, no heuristic scaling), does barrier/committor (≥10 revisits to same canonical state s=(URL_normalized, DOM_rich_cluster, H_K=3) with divergent futures 0.2<q<0.8, committor calibration ECE≤0.15 Brier gap≥0.05 over Markov) or timescale separation (autocorrelation tau>5 vs tau_shuffled~1, lag-MI gap≥0.05) reveal I(S_next; DOM_rich | URL, H_K=3, Action)>0.05 bits with p_bonf<0.01, |analytic_null_mean|<0.1, calibrated std valid and gap≥0.05 over TF-IDF k5 and Markov, while independent-noise genuine replication with overlapping spectra remains BC~0 (|BC|<0.05 p>0.10) and IID null BC≤0.03? Either valid SURVIVES (first genuine beyond-memory barrier/timescale with exact centering) or valid FALSIFIED (even correctly centered genuine overlapping DOM remains BC~0) changes claim/product and decides PARK — without new Gate0 discovery.

## 4. Motivation & Why This Is the Smallest High-Information Test

### 4.1 Why PIVOT with exact Gamma-ratio + overlapping spectra is required (tunnel diagnosis per director)

- Parent recalibration achieved BC 0.689-0.716 but via tautological regime-correlated categorical DOM (all 4 Rs byte-identical or 8-value deterministic red/blue encoding regime L) and heuristic analytic proxy forcing analytic_mean within 0.035 of perm_mean and inflating std via sqrt(mean(1/(2n)))*0.1+0.012 — not closed-form Gamma ratios required by prereg 8.1. Baseline analytic_mean miscentered 0.133>0.1 with consistency 0.053>0.03, so gap invalid; independent event_seq S_current%2 confounded; timescale 3.82-4.6<5 failed; no WebShop DOM used despite AND mandate. Repeating synthetic 12-state L-string sweep with heuristic bias correction repeats local optimum flagged by audits (permuted-null still biased 0.2-0.7 >0.1, Laplace smoothing) — near-zero marginal information. Bayesian DM K=12 (K=n_states=12, N=1999) is first estimator to pass C1+C3 log BF 168-643 null -78 to -131 but absolute BF -10 to -15 nats on real TodoMVC favors memory, motivating orthogonal barrier/committor rather than another PMI/KL tweak. Director comparative_reasoning: PARKing without testing genuine overlapping spectra wastes validated exact estimator; timescale alone on deterministic TodoMVC FSM cannot achieve H>0.2. The combined exact Gamma-ratio + genuine visual/AX spectra + barrier/committor/timescale with trajectory-grouped permutation and independent-noise BC~0 control is the only path that can change decision (BC>0.05 vs BC~0 with |analytic|<0.1 gap>=0.05 over TF-IDF k5/Markov).
- Frontier 61 pooled TV/KDE/binned experiments show complementary blind spots (kNN fails scaling rho -0.12, KDE fails rotation rho 0.286, CV 0.57-0.75 >0.5 instability at 250/type, 95% non-stationary attenuation) — another alpha/bandwidth/PCA tweak near zero information. Physics tunnel_flag 14 recent C-WEB-DYNAMICS exps, 60+ Gate0 failures (0/2-3 SPAs qualify) indicate synthetic L-derived bias is estimator-intrinsic; orthogonal estimator switch (Bayesian DM) is only escape per director prior 5. This PIVOT tests exactly that switch with genuine data.
- Gate0-free but genuine-DOM-dependent: reuses existing BrowserGym traces (no new SPA discovery) plus locally-hosted proxy with genuine renders — verifies dom_bytes/visual_bytes/a11y_bytes>0 and 1280x720 before claiming validation, as parent failed to provision BrowserGym despite mandate. Per-trajectory AND per-15-step regime persistence tests both correlation structures (director explicitly requires both).

### 4.2 Why genuine overlapping spectra + exact DM is falsifiable and not physics-as-graph

- Physics requires operational mathematical object, observable, falsifier, strong nulls, identifiability (MASTER_PROMPT §15). Graph reuse is not Physics. This design provides: operational barrier as -log P_transition between basins, committor q(s)=P(hit B before A | s) with ECE/Brier, timescale tau from ACF decay/lag-MI; observable revisits to same canonical s with divergent futures (≥10 revisits, both basins observed), lagged genuine overlapping DOM_rich -> S_next; falsifier BC≤0.05 or p≥0.01 or gap<0.05 or ECE>0.15 while gates pass => FALSIFIED-IN-SETTING bounded to genuine overlapping banks at N=1000-1999; strong nulls TF-IDF similarity (ordinary similarity), Markov K1/K3 (memory), trajectory-grouped shuffle (history-conditioned), independent-noise genuine same estimator with overlapping spectra (policy-matched), time-shuffle (timescale); identifiability via ≥10 revisits per s, divergent futures fraction, H(S_next|C)>0.2, MI(DOM;Action)<0.10, trajectory_id grouping, locked viewport, overlapping spectra verification.
- Prior hash truncation 5k SHA256 lost visual/computed information and allowed tautological isomorphism (36 hashes for 6*2*3 variants) plus deterministic regime-color (8 values). Overlapping genuine DOM via CDP Accessibility.getFullAXTree bypasses: visual bbox are layout geometry, computed 8-value styles are rendering with overlap across basins, AX embedding is accessibility semantics — none deterministically tied to single latent L, and overlap verified via distribution intersection.
- Exact DM bias correction: E[CMI|null] via Gamma functions for Dirichlet-Multinomial at K=12/24 via scipy.special.gammaln/polygamma exact digamma/trigamma separates smoothing bias floor (|analytic_mean|<0.1) from permutation variance. Calibrated std via analytic trigamma variance + perm_std consistency |perm-analytic|<0.03 replaces heuristic inflated floor that passed trivially (0.034). Addresses audit required_fixes 4,11.

### 4.3 Interdisciplinary alignment (director agent_priors_used, distinguished from SPIDER evidence)

Per request.json director_mandate.agent_priors_used (general priors, not SPIDER evidence, labeled separately per AGENTS.md):

- Prior 1 (long-horizon compounding / MEA auditor pattern): fresh-context execution + external verified state outperforms in-context memory; motivates independent verification before state update and trajectory-grouped permutation (correct resampling unit) not Gaussian jitter.
- Prior 2 (caching/replay baselines, Stagehand selector 80% speedup): non-empty retrieval on deterministic SPAs achieves recall@k=1.0 when registry<=k; motivates correct-family-required binding and header/body parametrization tests; explains Frontier 0.0 coverage gain as structural, motivates beyond-similarity gap over TF-IDF.
- Prior 3 (cost bijective with novelty rho~1.0): flags Product rho 0.97-0.995 as MEASUREMENT_INVALID until honest branch-derived costs; motivates calibration gates ECE<=0.15 Brier gap>=0.05 not inflated novelty correlations.
- Prior 4 (multi-channel freshness): auth/session/permission/DOM/endpoint/temporal not scalar orthogonality; cheap TTL/probe dominates learned calibration; cautions against another adaptive Jaccard sweep after FP=1.0 falsifications — motivates latent session/permission regime per-trajectory and per-15-step.
- Prior 5 (local optima / Laplace smoothing): repeating same SPA family with heuristic chunking or L-derived DOM locks Physics/Frontier in basin where null bias is estimator-intrinsic; orthogonal estimator switch (Bayesian DM via gammaln/polygamma) is only escape — justifies exact closed-form pivot.

### 4.4 Why smallest high-information

- Positive or negative outcome with valid exact gates changes C-WEB-DYNAMICS ceiling and product decision without new Gate0 discovery: SURVIVES => first genuine beyond-memory barrier/committor/timescale dynamics on overlapping DOM outside hash truncation and synthetic blind spots, with valid centering/calibration, gap over similarity/Markov, independent~0, ECE<=0.15 or tau>5 — justifies regime detector as mechanical prior; FALSIFIED => parks genuine-DOM barrier approach — even properly captured overlapping visual/style/AX barrier not mechanistically productive at N=1000-1999 despite exact analytic — forces PARK pending larger production manifest with real session/permission regimes and larger state spaces; frontier pivots to MemoryArena/API-bypass; not looping K/N heuristic tuning. MEASUREMENT_INVALID (positive blind or independent confounded or Q<10 or viewport/spectra fails) is informative refusing false negative. Marginal gain vastly exceeds another synthetic variant. Estimated cost <2h (reuses traces, scipy gammaln/polygamma, no LLM).

## 5. Hypotheses (frozen, exhaustive)

### H_barrier_committor (primary orthogonal, genuine overlapping DOM)

On banks (correlated genuine-DOM production-proxy 50x40 N=1000-1999 with overlapping spectra AND BrowserGym WebShop/TodoMVC secondary if available N=1000-1999), for states s=(URL_normalized, DOM_rich_cluster, H_K=3) with ≥10 revisits and divergent futures, committor q(s) calibrated ECE≤0.15 and Brier gap≥0.05 over B-MARKOV-1 plus BC = I(S_next; DOM_rich | URL, H_K=3, Action_leakageFree) >0.05 bits with trajectory-grouped permutation p_bonf<0.01 (Bonferroni max 8 floor 0.001), |analytic_null_mean|<0.1 (exact gammaln/polygamma), calibrated std valid, gap_R≥0.05 over B-DOM-SIMILARITY TF-IDF k5 and B-MARKOV-1 on ≥1 genuine overlapping DOM R (visual/computed 8-value/AX_embedding/event). Mechanism: genuine overlapping DOM carries latent regime/session biasing S_next beyond history/similarity.

### H_timescale (co-primary orthogonal)

Slow regime per trajectory (and per-15-step P(flip)=0.07 exploratory) induces timescale separation: autocorr decay tau_corr>5 vs tau_shuffled~1 and lag-MI I(S_{t+k};DOM_t|C)>0.05 at lag 1-3 with p<0.01 and gap over B-TIMESCALE-SHUFFLE ≥0.05, with same valid exact centering.

### H_positive_control_genuine

Same exact pipeline on genuine overlapping correlated must achieve BC≥0.30 p<0.01 |analytic_mean|<0.1 calibrated std valid consistency<0.03 and ECE≤0.15 Brier gap≥0.05 or tau>5 on ≥1 R. Theoretical capacity ≥0.30 bits (binary regime 0.70/0.30 basin bias at overlapping fidelity). Failure => MEASUREMENT_INVALID pipeline blind to exact correction. Construction frozen; any outcome-informed change EXPLORATORY.

### H_null_independent_genuine (negative control, overlapping spectra recalibrated)

Identical exact DM + 1000 grouped perms on independent-noise genuine replication (≥6 variants/state independent per-step genuine captures with overlapping spectra, same FSM without regime, not S_current%2) must show BC~0 |BC|<0.05 p>0.10 |analytic_mean|<0.1 valid. If BC≥0.05 p<0.10 valid => MEASUREMENT_INVALID confounded.

### H_null_iid

IID synthetic null (same marginal P(S) i.i.d., genuine overlapping DOM still sampled) must show BC≤0.03 p>0.10 |analytic_mean|<0.1.

### H_null_shuffled (perm + analytic genuine)

Within-strata grouped shuffle genuine overlapping DOM on correlated bank: analytic mean accurate within 0.03 of perm mean and |analytic_mean|<0.1 valid; degenerate on BOTH Rs triggers MEASUREMENT_INVALID not falsification.

## 6. Data Generation & Reuse (no new Gate0 discovery, but genuine overlapping browser capture)

### 6.1 Primary genuine production-proxy bank (locally-hosted, locked viewport, overlapping spectra)

- **Construction** (frozen deterministic PYTHONHASHSEED=0 numpy 42): 5-6 state production-proxy SPAs (TodoMVC React/Vue + auth/cart proxy) hosted locally (Flask/Express) with locked viewport 1280x720. Headless Chromium via Playwright/CDP: for each step, call CDP Accessibility.getFullAXTree and DOM.getBoxModel / getComputedStyle to capture genuine visual bbox (x,y,w,h), computed style 8 values (color, backgroundColor, visibility, display, opacity, border, position, fontSize), event sequence n-gram of last 3 primitives, AX-tree embedding (serialized role/name/value). **Overlapping spectra requirement**: styles/visual/AX distributions overlap across basins A/B (e.g., color palettes shared, bbox variance within-state > between-regime variance); verify via histogram intersection >0.3 and reject deterministic red/blue per regime. Latent regime per trajectory primary (50 trajectories x40 steps =2000 N=1000-1999 analyzed; exploratory per-15-step P(flip)=0.07 branch documented as second dataset, both N=1000-1999). Transition P(S_next|S,A,regime) basin A favors {0,1,2} 0.70/0.30 mirrored for B, p_stay 0.70. URL_before = `https://spa.local/#/state_{S}` hash fragment preserved. Genuine DOM_before observed via browser with overlapping spectra — NOT string `VIS_A_{L}_{state}` tautology, NOT deterministic 8-value. |R|/N ~0.02-0.15 expected genuine finite vocab. Seeds identical to allow comparison with prior heuristic but observables are browser bytes with overlap, not L strings. Verify dom_bytes>0 a11y_bytes>0 visual_bytes>0 viewport 1280x720 logged plus overlap metric.
- **Sample size**: 2000 transitions gives 24 strata avg ~83, power for BC 0.10 at calibrated std ~0.01-0.02, BF calibration N/K≥83 at K=24. Revisits expectation: URL fragment 6 states but genuine DOM clusters 20 with overlapping => ~100 canonical states, revisits per state ~20, so ≥5 states with ≥10 revisits achievable; if not, timescale primary and Q failure triggers MEASUREMENT_INVALID (not falsification).
- **Viewport lock**: Playwright viewport 1280x720, deviceScaleFactor 1, headless, CDP session; log viewport, dom_bytes, a11y_bytes per transition plus overlap histograms; failure => MEASUREMENT_INVALID G6.

### 6.2 Independent-noise genuine replication with overlapping spectra (null control)

Same proxy FSM without regime, transition uniform p_stay 0.50, genuine DOM variant independent per-step among ≥6 variants per state with overlapping spectra: for each step, randomly select among 6 pre-captured genuine overlapping DOM snapshots for that state (captured at same viewport, overlapping across basins, regime-independent), seeded per step independent of S_next and independent of S_current parity (not S_current%2), same genuine vocab with overlap. Generate 50x40=2000 N=1000-1999. Expect BC~0 per prior falsification but with exact calibrated std valid.

### 6.3 IID synthetic null with genuine overlapping DOM sampling

Same marginal P(S) estimated from correlated genuine bank but S_next i.i.d. per step seed 42, genuine overlapping DOM still sampled from correlated family but S_next independent => BC~0.

### 6.4 Existing BrowserGym WebShop / TodoMVC reuse (no new collection, if available)

If `research/intel/manifest.json` or `codex/` provides BrowserGym WebShop/TodoMVC trajectories with DOM/AX at 1280x720 and URL+title (already collected via Playwright at locked viewport), include as secondary primary (N=1000-1999, trajectory_id grouping, viewport verified, overlapping spectra assessed). No new browsing beyond proxy; reuse raw bytes already collected. Report Q (revisits), dom_bytes, visual_bytes, |R|/N, H(S_next|C), overlap metric. If Q<5 states with ≥10 revisits, WebShop secondary diagnostic only, not gating. If unavailable, primary is locally-hosted genuine overlapping proxy only, and validity_notes records BrowserGym reuse unavailable but proxy genuine with overlap satisfies mandate's locally-hosted branch; PIVOT still informative.

### 6.5 Sample size & power (exact-corrected)

Channel capacity binary regime bias 0.70/0.30: theoretical I(S_next;regime|C) ~0.40 bits pooling; at ~70% genuine overlapping DOM->regime recovery expected BC ~0.25-0.35 at K=12 with genuine fidelity slightly lower than synthetic 0.30. Exact analytic null_mean expected ~0.04-0.06 at K=12, ~0.02-0.04 at K=24, so BC 0.30 gives d ~15-30 vs calibrated std 0.01-0.02. Power via analytic CI width ~0.02-0.04. Independent with 6 genuine overlapping variants expected analytic std ~0.012 valid while BC~0. Per-15-step regime doc power similar but tau_corr expected smaller.

## 7. State, Action, History, DOM Operational Definitions

### 7.1 State S_next
Primary S_next = SHA256(normalize(URL_after)|'|'|normalize(title_after)) normalize(URL)=lowercase, strip query ?session=/?token=, preserve SPA hash fragment #/, strip trailing slash; normalize(title)=trim lowercased 200 chars (constant allowed). Exploratory S_URLonly SHA256(norm URL). S_next at t+1 distinct from DOM_before at t. Report unique_titles, title_entropy, H(S_next|C), S_URLonly BC.

### 7.2 Action A_leakageFree
A=(primitive,target_sig) primitive in {click,fill,navigate,select,submit,hover} target_sig=role+name+testId+aria-label never href/URL/src. Diagnostic A_leaky=+href for leakage gap only. Report MI(DOM_rich;Action) must be <0.10 else tautology, and not S_current%2 correlated.

### 7.3 History H_K=3
H_K=(A_{t-2},A_{t-1},A_t, S_{t-2},S_{t-1},S_t) last 3 steps; strata key C=(URL_before_normalized, H_K_actions) URL_without_title to avoid leakage. Require strata_count≥5 with ≥3 per stratum; singleton_SA_rate<70%; report H(S_next|C) must be >0.2.

### 7.4 DOM_rich genuine overlapping representations (independently tested, NOT L-derived, NOT deterministic color)

- R_visual: genuine AX bbox x,y,w,h quantized 10 bins + element_count/tree_depth/interactive_density from dom_bytes with overlapping spectra across basins
- R_computed_style: genuine computed CSS 8 values {color, backgroundColor, visibility, display, opacity, border, position, fontSize} from getComputedStyle at locked viewport with overlapping histogram >0.3
- R_event_seq: n-gram of last 3 interaction events (primitive+target_sig) from browser event log
- R_AX_embedding: genuine Accessibility.getFullAXTree serialized role/name/value up to 5k chars, TF-IDF k-means 20 clusters fit TRAIN only, embedding cosine not hash, overlapping across basins

Raw observables preserved (visual JSON, style dict with 8 values, event seq string, a11y_bytes, dom_bytes, overlap histograms). Primary requires ≥1 R genuine overlapping; all expected to correlate with regime but with imperfect fidelity vs synthetic 1.0. Document truncation/clustering loss, viewport, overlap metric.

### 7.5 Barrier/Committor operational
Canonical state s = (URL_before_normalized, DOM_rich_cluster, H_K_actions) clustered joint with overlapping verification. Revisits table: count visits per s. For s with ≥10 revisits, collect futures horizon 10: label hit B if S_next enters {3,4,5} before {0,1,2} (or empirically discovered basins via per-trajectory regime frequency with overlap). Estimate q(s)=P(hit B before A | s). Require ≥5 states with ≥10 revisits and ≥2 with divergent 0.2<q<0.8 for identifiability. Report divergent fraction, ECE, Brier, overlap per s.

## 8. Measures

### 8.1 Primary: exact Bayesian DM analytic (gammaln/polygamma) + barrier/committor + timescale
For each (dataset, R in genuine overlapping set):
```
H(S_next|C) via exact gammaln/polygamma DM
H(S_next|C,DOM_cluster) via gammaln/polygamma
CMI_obs = H(S_next|C) - H(S_next|C,DOM)
analytic_null_mean, analytic_null_std exact via gammaln/polygamma digamma/trigamma for Dirichlet alpha=1/K (scipy.special.gammaln, polygamma(0), polygamma(1), no heuristic proxy)
perm Null: 1000 trajectory-grouped shuffles within each C stratum grouped by trajectory_id seed 42 => perm_mean, perm_std, p_raw
BC = CMI_obs - analytic_null_mean (primary); BC_perm diagnostic
consistency = |perm_mean - analytic_mean| must be <0.03
calibrated_std = max(analytic_std, perm_std, 0.005 floor)
p_bonf = min(1, p_raw * n_tests) n_tests<=8 (effective 2-3 for visual/AX noted), floor 0.001
Cohen d = BC / calibrated_std, 95% CI via permutation percentiles
BF_10 for order3 vs order1 via gammaln log BF nats
Revisits per s, divergent futures, q(s), ECE, Brier, ACF tau, lag-MI, overlap histogram intersection
Report: BC, analytic_mean, perm_mean, consistency, calibrated_std, p_raw/p_bonf, d, CI, cardinality |R|/N, strata stats, H ceiling, MI(DOM;Action), revisits table, overlap metric
Verify: dom_bytes>0 viewport 1280x720 overlapping spectra for genuine; else G6; code contains gammaln/polygamma not sqrt(mean(1/(2n)))
```

### 8.2 Baselines (same exact K analytic+perm, same grouping, TRAIN-only fits, overlapping verification)
- B-DOM-SIMILARITY BC_sim TF-IDF k5 fit TRAIN only => gap delta_sim = BC - BC_sim must be ≥0.05 and analytic_mean<0.1
- B-MARKOV-1 BC_markov1 MLE => gap ≥0.05
- B-MARKOV-K3 BC_hist accuracy
- B-SHUFFLE-GROUPED null
- B-TIMESCALE-SHUFFLE for autocorr
- B-TRAJECTORY-MEMORY, B-SITE-LEAKAGE gaps

### 8.3 Auxiliary per dataset per R
NL, strata_count, strata_ge3, singleton_rate, leakage_validOnly, H(S_next|C), unique_DOM_clusters, |R|/N, analytic_mean/std (gammaln/polygamma), perm_mean/std, consistency, d, CI, MI(DOM;Action), q(s) distribution, ECE/Brier, ACF 0..5 tau, BF nats, card stats, dom_bytes/a11y_bytes/visual_bytes, viewport, revisits Q, gap, overlap intersection.

## 9. Null Models & Baselines (strong, all executed as frozen)

Enumerated in spec baselines. All executed with identical grouping (trajectory_id), seeds 42, preprocessing fit TRAIN only (70/30 by trajectory_id), Dirichlet alpha=1/K, N=1000-1999, locked viewport, exact gammaln/polygamma (no heuristic). Mandatory B-DOM-SIMILARITY and B-MARKOV-1 must be executed with valid centering |analytic_mean|<0.1; gap gating for SURVIVES. Exact DM provides calibrated null_std via polygamma, not heuristic floor. No silent omission: if baseline cannot be computed or Q<10 revisits, publish validity_note and trigger MEASUREMENT_INVALID for that branch, not FALSIFIED. All raw genuine overlapping DOM JSON committed with overlap histograms.

## 10. Statistical Tests & Uncertainty (frozen, corrected per audits, exact)

- **Permutation+exact Analytic**: 1000 trajectory-grouped shuffles genuine overlapping DOM within each C stratum grouped by trajectory_id seed 42 + exact analytic DM mean/std via scipy.special.gammaln + polygamma (digamma=polygamma(0), trigamma=polygamma(1)) for Dirichlet alpha=1/K. Consistency |perm-analytic|<0.03 required; primary BC uses analytic mean. Resampling unit trajectory_id; no Gaussian jitter.
- **p-value**: p_raw one-sided (1+#{perm>=CMI_obs})/1001, or analytic p via Dirichlet tail where 1000 perms floor 0.001 <0.01 reachable. Bonferroni primary p_bonf = min(1, p_raw * n_tests) n_tests<=8 (effective 2-3 for isomorphic visual/AX noted exploratory), alpha 0.01. Report raw and Bonferroni; BC also gates via 0.05.
- **BF**: log BF via gammaln, no resampling; calibrated on IID must be <0.
- **Effect size**: Cohen d = BC / calibrated_std (valid required); 95% CI via grouped permutation percentiles, NOT Gaussian.
- **Seed determinism**: PYTHONHASHSEED=0, numpy 42, sklearn 42; builtin hash() never used; SHA256 for S_next; viewport locked 1280x720; gammaln/polygamma call sites logged.
- **Valid centering**: |analytic_null_mean|<0.1 and calibrated_std valid (>0.005 analytic or >0.01 perm) and consistency<0.03 required; else MEASUREMENT_INVALID. Heuristic proxy (sqrt(mean(1/(2n)))*0.1+0.012, /100 scaling, blending) is audit-rejected and must not appear in analyze.py.
- **Implementation check**: audit will verify source contains `scipy.special.gammaln` and `polygamma` and does NOT contain `sqrt(mean(1/(2n)))` or `/100*0.1` heuristic.

## 11. Controls (frozen, genuine overlapping DOM + exact)

### Positive control (genuine overlapping correlated, exact)
Genuine correlated overlapping proxy must achieve BC≥0.30 p_bonf<0.01 |analytic_mean|<0.1 calibrated std valid consistency<0.03 and ECE≤0.15 Brier gap≥0.05 or tau>5 on ≥1 R with overlapping spectra verified. Failure => MEASUREMENT_INVALID pipeline blind to exact correction. Construction frozen genuine browser captures with overlap; any outcome-informed change EXPLORATORY. Verify viewport, dom_bytes, overlap >0.3.

### Null controls (recalibrated genuine overlapping + exact)
- Independent-noise genuine overlapping ≥6 variants/state with overlapping spectra (not S_current%2, not deterministic color) must show |BC|<0.05 p>0.10 |analytic_mean|<0.1 valid and consistency<0.03. If BC≥0.05 p<0.10 valid => MEASUREMENT_INVALID confounded.
- IID null must show BC≤0.03 p>0.10 |analytic_mean|<0.1 valid.
- Trajectory-grouped perm analytic null on correlated bank must be |analytic_mean|<0.1 valid consistency<0.03; degenerate both Rs => MEASUREMENT_INVALID.
- Timescale shuffle tau~1 BC_lag~0.

### Data-quality / identifiability / substrate controls
NL=1000-1999 (proxy) or BrowserGym N=1000-1999, strata≥5 with ≥3 per stratum, singleton<70%, H(S_next|C)>0.2, |R|/N 0.02-0.15 genuine overlapping, trajectory count ≥20, leakage_validOnly reported, revisits Q≥5 states with ≥10 visits and divergent futures required; if Q=0 => MEASUREMENT_INVALID substrate_insufficient (not falsification). Viewport 1280x720 verified, dom_bytes/a11y_bytes>0, genuinely observed overlapping spectra not L-string nor deterministic color; S_current%2 independence verified.

## 12. Validity Threats & Mitigations

| Threat | Mitigation |
|---|---|
| Target leakage href==URL / synthetic L-string tautology / deterministic color | Leakage-free A excludes href; genuine DOM_before distinct timestep via browser; overlapping spectra verified (>0.3 intersection) not deterministic red/blue; diagnostic gap; MI(DOM;Action)<0.10; state normalized without title in C; genuine not deterministic L-string (audit code contains no `VIS_A_{L}` and no deterministic color per regime) |
| Split leakage | TF-IDF vocab / embedding k-means centroids / Dirichlet counts fit TRAIN only (70/30 by trajectory_id); site identity never feature |
| Sampling/policy confounding | Document FSM policy (50x40 uniform among primitives per regime, per-trajectory AND per-15-step P=0.07) and BrowserGym policy as collected; trajectory_id unit; viewport locked |
| Uncertainty mis-specification (heuristic proxy) | Exact gammaln/polygamma Gamma ratios for DM; grouped permutation by trajectory_id; no Gaussian jitter; consistency <0.03; heuristic proxy audit rejection documented; degeneracy=>MEASUREMENT_INVALID; code audit for gammaln/polygamma |
| Representation loss (quantization, clustering, viewport, overlapping) | Preserve genuine raw observables (bbox JSON, 8-value style dict, event n-grams, AX bytes at 5k); document quantization 10 bins, k=20; verify 1280x720 + overlap histograms; sensitivity overlapping vs deterministic exploratory |
| Synthetic-to-real gap / infrastructure attraction | Claim bounded to existing genuine overlapping proxy + BrowserGym banks, not production correlated regimes outside; audit identifiability mitigated by gap over similarity/Markov and MI + overlap checks; final test before PARK |
| H=0 determinism ceiling / Q<10 revisits | Report H and Q; if H≤0.2 or Q<5 with ≥10 divergent => MEASUREMENT_INVALID ceiling, not falsification |
| Hash tautology action->DOM | Genuine overlapping DOM correlated with regime not Action; report MI<0.10; barrier requires divergent futures not unique mapping; verify not S_current%2 |
| Unreachable Bonferroni | N=1000-1999 1000 perms floor 0.001 <0.01 reachable; analytic p supplements; effective n_tests 2-3 for visual/AX noted |
| K bias floor degeneracy | Exact DM with gammaln/polygamma consistency replaces absolute floor; K=12 primary K=24 exploratory; no post-hoc relaxation without new prereg |
| Independent null_std degenerate / spurious style S_current%2 / deterministic color | Genuine 6-variant overlapping DOM and exact polygamma std expected calibrated > floor; verify DOM independent of S_current (not S_current%2) and overlapping not deterministic color; if still degenerate => MEASUREMENT_INVALID per G2; overlap verification required |
| Committor manufactured from sparse topology (red flag cluster!=attractor) | Require ≥10 revisits per s and divergent futures before q(s); report revisits table + overlap per s; if Q=0 validly halt MEASUREMENT_INVALID |
| Timescale spurious autocorrelation | Compare tau vs time-shuffled null B-TIMESCALE-SHUFFLE; require tau gap >4 and lag-MI gap≥0.05 with overlapping spectra |
| Heuristic analytic inflation (audit FAIL) | Code audit must show `gammaln`/`polygamma` not `sqrt(mean(1/(2n)))` or `/100`; consistency <0.03 gates genuine calculation; blending prohibited |
| Viewport / genuine substrate / overlap missing | G6 gates dom_bytes/visual_bytes>0 and 1280x720 and overlap >0.3; if WebShop unavailable proxy genuine overlapping still satisfies mandate's locally-hosted branch; deterministic color => MEASUREMENT_INVALID |
| Result/report drift | All metrics recomputed from raw_results.json + raw_transitions; freeze hashes verified before execution; byte-identical re-executable |

## 13. Decision Rules (frozen, pre-outcome)

### Pipeline gates (in order, any triggers MEASUREMENT_INVALID, no claim update)

- G1: genuine overlapping positive correlated control BC<0.30 OR p_bonf>=0.01 OR |analytic_null_mean|>=0.1 OR calibrated_std degenerate (analytic_std<=0.005 and perm_std<=0.01) OR |perm-analytic|>=0.03 OR no overlapping spectra verified => pipeline_blind_or_miscalibrated_to_exact_Gamma
- G2: independent-noise genuine overlapping replication BC>=0.05 and p<0.10 with valid analytic null (|analytic_mean|<0.1 valid std consistency<0.03) => pipeline_confounds (including prior spurious S_current%2 / deterministic color)
- G3: IID null BC>0.03 and p<0.10 with valid null => null miscentered
- G4: identifiability fails: no s meets ≥10 revisits with divergent futures on ≥5 states OR H(S_next|C)≤0.2 => null_degenerate_no_branching (not falsification, cluster!=attractor)
- G5: primary analytic-perm consistency fails on BOTH genuine overlapping representation sets (|perm-analytic|≥0.03) => model_mismatch
- G6: substrate fails: no genuine dom_bytes/visual_bytes/a11y_bytes>0 or viewport !=1280x720 or spectra deterministic non-overlapping (overlap <0.3) on proxy => substrate_missing (parent scope reduction failure)
- If any G fails, verdict=MEASUREMENT_INVALID, publish gate_table, do not evaluate primary

### Primary decision (only if all gates pass)

For each R in {R_visual,R_computed_style,R_AX_embedding,R_event_seq}, compute BC_R, p_bonf_R, analytic_null_mean_R (exact gammaln/polygamma), calibrated_std_R, consistency_R, BC_sim_R, BC_markov1_R, gap_R = BC_R - max(BC_sim_R,BC_markov1_R), d_R, CI, ECE_R, Brier_gap_R, tau_R/lag_MI_gap_R, viewport, overlap_intersection

Define sig(R)=1 if BC_R>0.05 AND p_bonf_R<0.01 AND |analytic_null_mean_R|<0.1 AND calibrated_std_R valid AND consistency_R<0.03 AND gap_R≥0.05 AND overlap_verified AND (ECE_R≤0.15 OR tau_R>5 gap validated) AND independent~0 on that R

- If EXISTS R with sig(R)==1 => SURVIVES_CURRENT_TEST — genuine richer overlapping DOM barrier/committor or timescale reveals predictive information beyond (URL,H_K,Action) and beyond ordinary similarity/Markov on existing genuine overlapping banks without Gate0, with valid exact centering and calibrated null, while independent remains ~0 and calibrated (bounded to tested genuine overlapping banks and K analytic, N=1000-1999)
- If FORALL R, BC≤0.05 OR p≥0.01 OR gap<0.05 OR calibration fails while gates pass => FALSIFIED-IN-SETTING — genuine overlapping DOM barrier/committor/timescale does not carry detectable predictive information beyond memory/similarity via exact pipeline, bounded to tested genuine overlapping representations and existing banks (genuine overlapping proxy + WebShop reuse) and K analytic with trajectory-grouped permutation
- Sensitivity (K12 vs24, S_URLonly, R multi_feature, H_K=2/4, per-15-step regime) exploratory not gating

### Exploratory (only if FALSIFIED and gates passed)

Report H(S_next|C,D) decomposition, per-strata CMI histogram, MI(regime;DOM) vs MI(regime;S_next), TF-IDF gap, independent overlapping 6-variant stability, ACF tables, committor q(s) scatter, overlap histograms. Do NOT alter primary verdict.

## 14. Consequences

### If SURVIVES (valid exact Gamma gates, overlapping spectra verified)

- C-WEB-DYNAMICS ceiling expands to: genuine overlapping barrier/committor or timescale beyond-memory dynamics via richer DOM (visual bbox, computed 8-value style, AX embedding, event at 1280x720, overlapping spectra) on existing banks without Gate0 via exact analytic DM + trajectory-grouped permutation with BC>0.05 p_bonf<0.01 gap≥0.05 calibrated centering independent~0 and ECE≤0.15 or tau>5. First genuine beyond-memory correlated dynamics outside SHA256 truncation and synthetic TV/KDE blind spots and independent-noise falsification; first valid barrier/committor identifiability outside tautological basins with exact correction.
- Product: distill genuine-DOM regime detector as mechanism preconditions/barrier guards/freshness sentinels (regime-aware retrieval grouped by genuine overlapping cluster, visual+AX embedding signature, event-seq guard) into kernel resolve/verify; prioritize BrowserGym/runtime collection on session-correlated sites (auth/cart/personalization) at 1280x720 where regimes amplify; quantify delta-repair cost when session shifts and cross-site holdout transfer; measure residual-novelty economics via regime detection work-compression.
- Physics next: test invariance across site types and regimes (permission vs user-data vs external API), larger state spaces (BrowserGym WebShop categories), quantify transfer, test on production correlated SPAs when intel manifests larger (now justified); not PARK; Frontier to continue orthogonal MemoryArena.

### If FALSIFIED (valid exact gates, overlapping spectra verified)

- C-WEB-DYNAMICS remains HYPOTHESIS but orthogonal genuine overlapping-DOM barrier/committor/timescale program closed for these banks and genuine overlapping representations at K analytic N=1000-1999: even with genuine DOM correlated by construction with latent regime determining S_next (positive BC≥0.30 passing with exact analytic) and calibrated centering |analytic_mean|<0.1, genuine overlapping DOM does not carry detectable predictive information beyond history and similarity/Markov (gap<0.05 or BC≤0.05 or p≥0.01) and calibrated ECE/tau fail. Combined with prior 66+ HYPOTHESIS, frontier blind spots, exhaustive Gate0 0/3, heuristic proxy rejection, and Bayesian absolute BF -10 to -15 nats favoring memory on real TodoMVC, this parks genuine overlapping barrier approach — even correctly centered genuine overlapping DOM is BC~0 — indicating barrier/committor not mechanistically productive on tested banks despite exact correction. Audit partial-discrimination (2 hashes vs 1) resolved as genuine dose-response bounded.
- Product: do NOT invest in DOM regime detectors on this representation class; Graph/Product rely on retrieval/verification/repair amortization alone (C-RESIDUAL-NOVELTY). High-value as it prevents wasted physics spend on genuine overlapping DOM barrier and justifies PARK next cycle per director rationale.
- Physics next per director rationale: PARK barrier/committor/timescale on genuine overlapping DOM pending larger production manifest with real session/permission latent regimes and larger state spaces before further physics spend; do not loop K/N heuristic tuning beyond this exact recalibration; consider frontier MemoryArena or alternative Web-Physics mechanisms (WebAPI bypass, compile-and-execute); negative result justifies PARK next cycle.

### If MEASUREMENT_INVALID (exact gates still fail)

- No claim update. Report exact gate failed, per-dataset table, analytic_mean/std (gammaln/polygamma), perm_mean/std, consistency, revisits Q, H ceiling, viewport/dom_bytes/overlap metric, unresolved substrate. Retry not scientific negative. Preserve discipline. Next unblock per mandate would be larger production manifest with real session regimes or intel AX isolation fix, or runtime exact analytic fix, not silent threshold relaxation; if G6 viewport/overlap fails, runtime must fix 1280x720 CDP capture and overlapping generation.

## 15. Analysis Plan (deterministic order, no outcome peeking before freeze)

1. **Verify freeze integrity**: check request.json sha256 5a2ac9903e13..., spec.json, prereg.md hashes match freeze.json before any computation; record commit HEAD 00da54cecc6ed and parent 15cdf6b415b.
2. **Assemble banks** (deterministic PYTHONHASHSEED=0 numpy 42): (a) genuine overlapping correlated proxy primary 50x40=2000 N=1000-1999 via generate_correlated_genuine.py frozen with overlapping spectra (regime per trajectory primary + per-15-step branch, genuine CDP captures at 1280x720 — no `VIS_A_{L}` string, no deterministic color), (b) independent-noise genuine overlapping replication 50x40 ≥6 variants per state via generate_independent_genuine.py frozen (overlapping snapshots regime-independent, not S_current%2), (c) IID synthetic null via generate_iid_genuine.py frozen, (d) reuse BrowserGym WebShop/TodoMVC raw bank if available at research/intel/manifest.json or codex trajectories (read-only, verify viewport/dom_bytes/overlap). Save raw_transitions_*.json with fields {trajectory_id, step, URL_before/after, title, Action_primitive/target_sig, DOM_visual bbox JSON, DOM_computed_style 8-value dict, event_seq, AX_tree bytes, AX_embedding_cluster, S_next hash, regime, per15_regime, viewport, dom_bytes, a11y_bytes, overlap_group}. Compute sha256 per file.
3. **Compute strata**: for each dataset build C=(URL_before_normalized, H_K=3) with H_K as defined, report strata_count, strata_ge3, singleton rate, H(S_next|C), leakage_validOnly, |R|/N per genuine overlapping R, dom_bytes/visual_bytes/a11y_bytes, viewport, revisits Q table (counts per s), overlap intersection histogram, ECE pre-check.
4. **For each (dataset,R in {R_visual,R_computed_style,R_AX_embedding,R_event_seq,R_multi_exploratory})**: compute exact Bayesian DM gammaln/polygamma H(S_next|C) and H(S_next|C,DOM_cluster) K=12 (K=24 exploratory) => CMI_obs, analytic_null_mean/std via exact Gamma ratios (scipy.special.gammaln, polygamma), BC, run 1000 trajectory-grouped perms within each C grouped by trajectory_id seed 42 => perm_mean/std, p_raw/p_bonf, d, CI, BF; compute B-DOM-SIMILARITY TF-IDF k5 fit TRAIN only => BC_sim; compute B-MARKOV-1/K3 MLE fit TRAIN => BC_markov gap; compute B-TRAJECTORY-MEMORY, MI(DOM;Action); for barrier states with ≥10 revisits compute q(s) ECE Brier tau ACF lag-MI vs time-shuffle with overlap verification.
5. **Apply gated decision rule** §13 in order, publish per-representation table (BC, analytic_mean via gammaln, perm_mean, consistency, gap, ECE/Brier/tau, overlap), revisits table, ACF table, permutation+analytic histograms, strata tables, gate/control tables, provenance with sha256; verify analytic code contains `gammaln`/`polygamma` and not heuristic formula; no metric built before freeze hash.
6. **Commit** all raw transitions, genuine overlapping DOM JSON with overlap proof, hashes, strata tables, perm+analytic distributions, revisits/ACF tables, code paths (generate_*.py, analyze.py) with sha256 in provenance.json; re-executable aside from elapsed; include exploratory BrowserGym secondary and per-15-step branch if available but not gating unless primary passes.

## 16. Freeze Statement

This preregistration is frozen before any outcome data for the genuine overlapping-DOM barrier/committor/timescale with exact DM decision is inspected. Genuine browser-observed overlapping DOM at locked 1280x720 via CDP Accessibility.getFullAXTree (visual bbox, computed 8-value style, AX embeddings, event n-grams with overlapping spectra across basins) replaces prior SHA256 5k L-derived deterministic labels and regime-color proxy that caused isomorphic tautological BC 0.689-0.716 and heuristic analytic inflation (audit FAIL). Exact Dirichlet-Multinomial Gamma-ratio bias correction via scipy.special.gammaln/polygamma (exact digamma/trigamma, no /100*0.1 scaling or blending) replaces heuristic proxy forcing 0.0008-0.0356 consistency. Trajectory-grouped permutation (1000 perms unit trajectory_id seed 42, N=1000-1999, K=12/24, |perm-analytic|<0.03) preserves history-conditioned nulls required by identifiability (≥10 revisits divergent 0.2<q<0.8, H>0.2, ECE≤0.15, tau>5) and director mandate gaps ≥0.05 over TF-IDF similarity and Markov with independent overlapping ~0 and overlapping spectra verification. Correlated genuine overlapping construction (regime per trajectory bias 0.70/0.30 + per-15-step P(flip)=0.07, genuine overlapping DOM family per regime/state captured via browser with intersection >0.3) and independent-noise genuine overlapping 6 variants are defined by construction, not by peeking at correlated BC under genuine DOM. BrowserGym WebShop/TodoMVC reuse at locked viewport satisfies Gate0-free without exhaustive LFS search. Any deviation after freeze is EXPLORATORY and cannot support confirmatory SURVIVES/FALSIFIED. A new claim requires new preregistration and untouched evidence. Estimated cost <2h wall-clock, no LLM, stdlib+scipy+headless Chromium for genuine capture only.

## 17. References to Prior Evidence

- Parent EXP-PHYSICS-35796855042 (MEASUREMENT_INVALID audit FAIL heuristic 0.059-0.088/0.034 BC 0.689-0.716 tautological regime-color, baseline 0.133, tau 3.82-4.6<5, no WebShop DOM, S_current%2 confound) — direct predecessor; audit required_fixes implement exact gammaln/polygamma + overlapping spectra + BrowserGym WebShop trajectories at 1280x720 with per-trajectory/per-15-step regime; this PIVOT supersedes with exact closed-form genuine overlapping capture
- EXP-PHYSICS-35793566080 (MEASUREMENT_INVALID heuristic 0.069/0.034 BC 0.671 tautological L-strings) — parent of parent; closed-form required
- EXP-PHYSICS-35787698409 (MEASUREMENT_INVALID borderline |null_mean|0.0748 null_std0.00967 BC 0.707) — heuristic proxy borderline; exact required
- EXP-PHYSICS-34764605162 (FALSIFIED-IN-SETTING independent-noise BC 0.004/0.025 p=1.0) — independent falsified, correlated open setting now tested genuinely overlapping
- Frontier 61 pooled TV/KDE/binned tunnel (kNN fails scaling rho -0.12, KDE fails rotation rho 0.286, CV 0.57-0.75, 95% non-stationary attenuation) — orthogonal pivot per director comparative reasoning
- Bayesian DM K=12 N=1999 passes C1+C3 log BF 168-643 null -78 to -131 but absolute BF -10 to -15 nats on real TodoMVC favors memory — validates exact estimator class but shows real data favors memory
- Intel 0/3 Gate0 exhaustive BrowserGym/CAP/Mind2Web closes production SPA enumeration — motivates reuse not discovery

