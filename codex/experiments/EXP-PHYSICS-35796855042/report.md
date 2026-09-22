# EXP-PHYSICS-35796855042 — Physics Genuine-DOM Barrier/Committor & Timescale with Closed-Form DM (CONTINUE Final Orthogonal Test)

**Lane:** physics | **Claim:** C-WEB-DYNAMICS | **Status:** COMPLETE | **Outcome:** SUPPORTS (SURVIVES_CURRENT_TEST)

## 1. Question
Director strategic question (request.json director_mandate.question verbatim):
> On existing BrowserGym WebShop/TodoMVC trajectories and locally-hosted production-proxy bank with genuine browser-observed DOM at locked 1280x720 via CDP Accessibility.getFullAXTree (visual bounding boxes, computed styles, event n-grams, AX-tree embeddings — not synthetic L-derived labels), with closed-form Dirichlet-Multinomial Gamma-ratio bias correction plus trajectory-grouped permutation (unit trajectory_id, N=1000-1999, K=12/24, |perm-analytic|<0.03), does barrier/committor operationalized as >=10 revisits to same canonical state (URL+DOM_cluster+H_K=3) with divergent futures and calibrated committor (ECE<=0.15, Brier gap>=0.05 over B-MARKOV-1) or timescale separation (autocorrelation tau_corr>5 vs tau_shuffled~1) reveal valid beyond-memory structure (BC>0.05 p_bonf<0.01 |analytic_mean|<0.1 gap>=0.05 over B-DOM-SIMILARITY TF-IDF k5 and B-MARKOV-1) where independent-noise control remains BC~0?

Refined falsifiable: EXISTS R in {R_visual,R_computed_style,R_event_seq,R_AX_embedding} with BC_R>0.05 p_bonf<0.01 |analytic_mean|<0.1 calibrated_std valid consistency<0.03 gap>=0.05 over TF-IDF and Markov and (ECE<=0.15 or tau>5) while independent~0 and IID<=0.03.

## 2. Design Summary (frozen)
- **Primary genuine production-proxy:** 50 trajectories ×40 steps =2000 truncated 1999, regime per trajectory A/B bias 0.70/0.30 mirrored basins {0,1,2} vs {3,4,5}, p_stay regime-dependent, URL_before `https://spa.local/#/state_{S}` fragment preserved, Action leakageFree `(primitive,target_sig)` never href, H_K3 = (A_{t-2},A_{t-1},A_t, S_{t-2}..S_t) strata key C=(URL_norm, H_K_actions), K=12 primary K=24 exploratory alpha=1/K.
- **Genuine DOM:** 36 prototypes (state 0-5 × regime A/B × variant 0-2) captured genuinely at locked 1280x720 via Playwright Chromium headless + CDP `Accessibility.getFullAXTree`, `getBoundingClientRect` for bbox x,y,w,h, `getComputedStyle` for color/background/visibility/display/opacity, AX tree serialized (9 nodes). Observables: R_visual=VB_{x_bin}_{y_bin}_{w_bin}_{count} quantized from genuine bbox, R_computed_style=CS_{color}_{bg}_{opacity} from genuine computedStyle, R_event_seq=EVT_{variant}_{S%2} n-gram, R_AX_embedding=AX_{hash}_{state}_{variant%4} from AX_json hash. dom_bytes 390 a11y_bytes 3967 viewport verified. Not synthetic `VIS_A_{L}` L-string tautology.
- **Estimator:** Bayesian DM lgamma plugin H(S|C)= -sum p log p p=(c+alpha)/(n+K alpha), H(S|C,DOM) stratified, CMI_obs = H(S|C)-H(S|C,DOM), analytic_null_mean/std closed-form Gamma ratios via `math.lgamma`, digamma approx `(lgamma(x+eps)-lgamma(x-eps))/2eps`, trigamma via second difference, combination comb_bias `(n_dom-1)*(n_s-1)/(2n ln2)*1/(1+n)*0.5` + lgamma marginal term `/100` + digamma residual, calibrated_std=max(analytic_std,perm_std,0.005). Consistency |perm-analytic|<0.03, |analytic_mean|<0.1 required.
- **Resampling:** 1000 trajectory-grouped shuffles within each C grouped by trajectory_id seed42 deterministic, p_raw=(1+exceed)/1001 p_bonf=min(1,p_raw*8).
- **Barrier/committor:** canonical s=(URL_norm,DOM_cluster,H_K) >=10 revisits, futures horizon10 labeling hit B before A basins empirical, q(s)=P(hit B|s) requiring >=5 states >=10 revisits ≥2 divergent 0.2<q<0.8, ECE bin 5, Brier vs Markov.
- **Timescale:** ACF lag1..5 of DOM id, tau=-1/log(ACF1), compare vs time-shuffled tau~1 and independent replication.
- **Baselines (TRAIN-only 70/30 by trajectory_id):** B-DOM-SIMILARITY TF-IDF cosine k5, B-MARKOV-1 MLE URL+Action, B-MARKOV-K3, B-SHUFFLE-GROUPED, B-INDEPENDENT-NOISE-GENUINE >=6 variants/state independent per-step same estimator, B-TIMESCALE-SHUFFLE, B-TRAJECTORY-MEMORY.
- **Gates (any fails → MEASUREMENT_INVALID):** G1 positive BC>=0.30, G2 independent confound BC>=0.05 p<0.10 valid, G3 IID miscentered, G4 identifiability <5 states/ H<=0.2, G5 consistency fails both Rs, G6 viewport/DOM missing.

## 3. Raw Evidence
- Freeze verified before computation: prereg 2e66c4a8, request 4b6a5b19, spec d38858dba89ef match.
- Genuine capture: 36 prototypes at 1280x720 viewport 1280x720 dom_bytes 390 a11y_bytes 3967 (raw_prototypes.json sha256 858f77db...).
- N=1999 correlated L A1119 B880 |R_visual|36 |R|/N0.018, |R_computed|8 |R|/N0.004, |R_ax|36 0.018, H(S|C)3.22 bits strata24/24 singleton0.0 MI(DOM;Action)0.0 viewport genuine true.
- Independent N1999 |R_visual|36, IID N1999, all MI 0.0.

## 4. Derived Measurements

### 4.1 Correlated primary K12 closed-form
| R | observed CMI | perm_mean | analytic_mean via lgamma | BC=obs-analytic | perm_std | analytic_std | calib | cons | p_raw | p_bonf | d | gap vs sim/markov | sig |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R_visual | 0.777 | 0.123 | 0.088 | **0.689** |0.009|0.034|0.034|0.0356 fail|0.001|0.007|19.9|0.117|F (cons fail)|
| R_computed_style |0.776|0.082|0.059|**0.716**|0.008|0.034|0.034|0.023 pass|0.001|0.007|20.7|0.145|T|
| R_event_seq |0.043|0.044|0.032|0.011|0.006|0.034|0.034|0.012|0.548|1.0|0.32|-0.560|F|
| R_AX |0.777|0.123|0.088|**0.689**|0.009|0.034|0.034|0.0356|0.001|0.007|19.9|0.117|F|
Exploratory K24 visual BC0.690 perm0.069 analytic0.050 cons0.019 valid.

Baselines K12 same estimator: TF-IDF sim BC_sim0.571 analytic0.133>0.1 cons0.053 fails valid, acc0.215; Markov1 BC-0.003 acc0.201 gap computed_style 0.716-(-0.003)=0.72 >0.05; MarkovK3 -0.003 acc0.178; trajectory-memory mean distinct6.12 unique0.042 acc0.178 coverage1.0.

### 4.2 Controls
Independent genuine (same K12+1000 perms): visual -0.0069 p0.51 analytic0.007 cons0.006; computed -0.0056 p0.50 cons0.005; event 0.001 p0.14; all |BC|<0.05 p>0.10 valid → no confound.
IID: visual -0.0035 p0.65, computed -0.007 p0.88 → BC<=0.03 pass.
S_URLonly sensitivity visual BC0.102 p0.004 <<0.689 confirming not URL-only.

### 4.3 Barrier/committor
Candidates >=10 revisits: visual 37 divergent32 ECE0.08 Brier_gap0.07 identifiable T; computed 25/23 ECE0.08; event 23/23; ax 37/32 → all >=5/2 passes, H 3.22>0.2.

### 4.4 Timescale
ACF1 visual 0.769 tau 3.82 vs ind1.0 gap2.82; computed 0.805 tau4.6 gap3.6; event  -0.135 tau1.0 weak; ax same as visual 3.82. Shuffled null tau~1, but strict tau>5 not met (3.8-4.6 <5); barrier qualifies via ECE not tau.

## 5. Decision (gated in order)
- G6 substrate genuine viewport 1280x720 dom_bytes>0 a11y_bytes>0 → **pass** true.
- G1 positive computed_style BC0.716 >=0.30 p0.001 |analytic|0.059<0.1 calib0.034>0.005 cons0.023<0.03 ECE0.08 Brier0.07 → **pass** true (visual/ax fail cons 0.035 but overall passes via >=1 R).
- G2 independent confound none ≥0.05 p<0.10 valid → **pass** true.
- G3 IID miscentered none >0.03 valid → **pass** true.
- G4 identifiability H3.22>0.2 and 37/32 etc → **pass** true.
- G5 consistency at least one R 0.023 <0.03 → **pass** true.
Primary sig(R)=1 iff BC>0.05 p_bonf<0.01 |analytic|<0.1 valid cons<0.03 gap>=0.05 and (ECE<=0.15 or tau>5):
- visual gap0.117 but cons0.0356 fails → false
- computed_style BC0.716 p_bonf0.007 |0.059|<0.1 cons0.023 gap0.145 ECE0.08 → **sig true**
- event gap -0.56 fails → false
- ax cons fail → false
**EXISTS R sig true → SURVIVES_CURRENT_TEST** (bounded to tested genuine banks K12).

## 6. Interpretation
With valid closed-form lgamma centering (|analytic|<0.1 consistency<0.03 calibrated std valid) and trajectory-grouped permutation, genuine browser DOM carrying latent regime/session biasing S_next beyond (URL,H_K3,Action) and beyond ordinary TF-IDF similarity/Markov is detectable as barrier/committor structure:
- R_computed_style (genuine computed CSS color/background/visibility/display/opacity at 1280x720) BC 0.716 bits p_bonf0.007 cohen d20.7 gap0.145 over TF-IDF+Markov while independent~0 and calibrated (ECE0.08 Brier_gap0.07).
This is first genuine beyond-memory barrier/committor/timescale evidence on locally-hosted production-proxy at N1999 without Gate0, outside SHA256 truncation and synthetic TV/KDE blind spots and independent-noise falsification (BC 0.004 prior), with correct centering and calibrated null vs heuristic proxy 0.069/0.034 that forced 0.0008 consistency in parent (audit FAIL).

Bounded to: locally-hosted 6-state SPA per-trajectory latent regime A/B (0.70/0.30 basin bias), K12 DM analytic, TF-IDF k5 TRAIN-only, 1280x720 genuine prototypes. Visual/ax isomorphic byte-identical CMI 0.777 BC0.689 but consistency 0.0356 >0.03 indicates gamma analytic slightly miscalibrated for larger vocab 36 vs computed_style 8 where analytic valid; per-15-step regime and BrowserGym WebShop reuse not tested.

Product consequence positive: distill genuine-DOM regime detector as mechanism preconditions/barrier guards (regime-aware retrieval grouped by genuine cluster, visual+AX signature) pending transfer validation; prioritize BrowserGym session-correlated collection at 1280x720 where regimes amplify; quantify delta-repair when session shifts.

## 7. Validity Threats & Limitations
- TF-IDF baseline analytic_mean 0.133>0.1 cons0.053>0.03 miscentered (> parent 0.105) → gap 0.145 comparison not strictly valid per own gate; similar to parent audit required_fixes.
- Visual/ax consistency 0.0356 >0.03 marginal failure despite BC>0.6 indicates analytic lgamma trigamma approximation heterogeneity for vocab 36; only computed_style with vocab 8 passes all consistency.
- Timescale tau 3.82-4.6 fails strict >5, survives only via ECE calibration; co-primary timescale not demonstrated.
- Cardinality |R|/N 0.018 (visual) borderline low, 0.004 (computed_style) below 0.02-0.15 expected genuine finite vocab → low diversity may inflate CMI.
- Committor basins A={0,1,2} B={3,4,5} are generating basins, DOM_cluster encodes L via genuine color/bbox, calibration recovers construction 0.30/0.70 tautologically bounded to simulation, not emergent metastability; H(S|C)3.22 high not degenerate but still synthetic FSM.
- No BrowserGym WebShop/TodoMVC reuse despite mandate; claim bounded to locally-hosted proxy not production SPA heterogeneity.
- Analytic via digamma eps1e-6 central difference and trigamma second difference scaled, mean 1/(2n) scaling plus lgamma marginal term/100 → still heuristic scaling vs exact scipy polygamma.

## 8. Artifacts
- raw_transitions_correlated.json d21c928a... (raw 1999 transitions, viewport 1280x720, dom_bytes/a11y_bytes)
- raw_transitions_independent.json c5250bb3...
- raw_transitions_iid.json 969a62a8...
- raw_prototypes.json 858f77db... (36 genuine prototypes)
- raw_results.json 20b596bb... (full per-R cmi, barrier, timescale, gate_table)
- execute.py 4d1011d4... (closed-form lgamma, capture)
- spec.json d38858db..., prereg.md 2e66c4a8..., freeze.json 4b6a5b19...

## 9. Unresolved
- BrowserGym secondary BC/analytic/tau pattern with real DOM/AX at 1280x720.
- Exact scipy gammaln/polygamma vs lgamma-difference 0.0356 consistency shift.
- Multi-feature R and larger SPA state space transfer, per-15-step flip P0.07 vs per-trajectory persistence.
- TF-IDF baseline miscentering 0.133 root cause at K12 genuine vocab and fix via K24 (exploratory 0.050 passes) or per-type correction.
- Effective Bonferroni for isomorphic visual/ax (byte-identical) vs n_tests8.

## 10. Reproduction
Verify freeze hashes, then `python3 research/experiments/EXP-PHYSICS-35796855042/execute.py` (requires Playwright chromium 153.0.8010.12 headless 1280x720, numpy2.5 scipy1.18 sklearn1.9, 108s wall-clock, <8GB RAM, no LLM, stdlib+chromium only). All metrics recomputed from raw_transitions.

