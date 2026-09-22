# EXP-PHYSICS-35793566080 Preregistration — Physics Orthogonal Barrier/Committor & Timescale with Richer DOM and Analytic DM (PIVOT)

**Status: DESIGN — FROZEN BEFORE OUTCOME (2026-09-22). No outcome-bearing measurements for the orthogonal barrier/committor/timescale decision have been inspected.**

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35793566080
- **Lane**: physics
- **Claim**: C-WEB-DYNAMICS — Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity (status HYPOTHESIS per codex/claim_state.json, 65+ prior experiments, last verdict MEASUREMENT_INVALID on EXP-PHYSICS-35787698409)
- **Directive**: Global Research Director PIVOT on C-WEB-DYNAMICS (request.json director_mandate cycle 35793060550, allocation PIVOT cognitive_reset true, parent_handoff_disposition SUPERSEDE, claim_id C-WEB-DYNAMICS). Binding strategic question verbatim in request.json director_mandate.question. For NEW governed experiments, director mandate is binding research direction; inherited parent_handoff is continuity evidence only and MUST NOT silently override SUPERSEDE/PIVOT decision (AGENTS.md §Work discipline, EXPERIMENT_PACKET.md §2).
- **Parent handoff**: `research/experiments/EXP-PHYSICS-35787698409/handoff.json` (sha256 9daed76d163629417ac4b7a2ded7a3654c99cfd1f577eca3fc586b74c1c5fa8f) — MEASUREMENT_INVALID borderline null_std 0.00967 ≤0.01 by 0.00033 (mean 0.0748 passes) on correlated 6-state FSM at K=24 N=1999. Its established/rejected/unknown/do_not_assume distinctions preserved below (§2). Director comparative reasoning SUPERSEDE: vs continuing recalibrated correlated-FSM CMI with same hash-truncated visible_text_hash/a11y at K=24 (high risk repeated null_std degeneracy) and vs exhaustive BrowserGym/CAP/Mind2Web SPA enumeration (0/3 after 80+ exps) — orthogonal barrier/committor/timescale with richer DOM and analytic DM has higher marginal information.
- **Dependencies (binding per mandate)**: intel (existing TodoMVC/BrowserGym WebShop trajectory banks reused, no new Gate0 SPA discovery), runtime (locally-hosted correlated FSM harness already provisioned + 1280x720 AX tree substrate). No new Gate0 production SPA substrate required.
- **Pre-2.0 / codex baseline**: WP-002B rule minus shuffle +0.0532 no holdout, WP-003 MEASUREMENT_INVALID (leakage, Gaussian jitter, hash(site) seed). Frontier 61 pooled TV/KDE/binned blind spots (kNN fails scaling rho -0.12, KDE fails rotation rho 0.286, CV>0.5, 95% attenuation non-stationary). Physics correlated hash FSMs: EXP-PHYSICS-34764605162 falsified independent-noise BC 0.004/0.025 p=1.0, EXP-PHYSICS-35782523165 MEASUREMENT_INVALID |null_mean|0.1297>0.1 null_std 0.0094<0.01 BC 0.688 p 0.001 gap 0.688, EXP-PHYSICS-35787698409 MEASUREMENT_INVALID |null_mean|0.0748<0.1 null_std 0.00967<0.01 BC 0.707 p 0.001. Audit diagnoses absolute null_std>0.01 floor structurally incompatible — perm std scales DOWN with N/strata, K recalibration fixes mean not variance.

## 2. Inherited Scientific State (from parent handoff — continuity evidence, not agenda)

Per AGENTS.md and EXPERIMENT_PACKET.md, parent handoff `next_question` is advisory local proposal only; director_mandate PIVOT SUPERSEDE is binding. Preserved distinctions per request:

### Established (justified at stated ceiling, recomputed, continuity only)

- Descriptive correlated-state signal at K=24 alpha=1/24 N=1999 (50 traj x40 steps, L per trajectory A 959/B 1040, 36 SHA256(L||state||variant%3) hashes |R|/N 0.018, dom_bytes 24 a11y_bytes 24, H(S_next|C) 3.334 >0.3 strata 24 ge3 24 singleton 0.0, MI(DOM;Action) 0.0, leakageFree): observed CMI 0.781 perm_mean 0.07482 perm_std 0.009673 BC 0.70663 p_raw 0.001 p_bonf 0.00799 gap 0.7066 over B-DOM-SIMILARITY 0.0 and B-MARKOV-1 0.0 on R1 visible_text_hash and R2 a11y_tree_hash (isomorphic) and R3 multi_feature same, R4 numeric-structural BC -0.0039 p 0.736 degenerate, Cohen d 73 CI [0.057,0.094] (result.json metrics primary_BC_R1/R2, audit recomputed identical)
- Independent-noise replication RECALIBRATED 6 variants per state BC -0.000627 p 0.529 perm_mean -0.0555 perm_std 0.00648 H 2.610 |BC|<0.05 replicates prior falsification parent -0.005109; G2 not triggered
- IID synthetic null BC 0.0016 p 0.393 |BC|≤0.03 confirms correlated 0.707 not estimator bias alone
- Baselines executed frozen 70/30 by trajectory_id TRAIN-only: B-DOM-SIMILARITY TF-IDF cosine k5 BC 0.0 acc 0.108 gap 0.706, B-MARKOV-1 0.0, B-MARKOV-K3 0.0, B-SHUFFLE-GROUPED grouped permutation null above, B-SITE-LEAKAGE gap 0.6703 MI 0.0
- Data quality and provenance: locally-hosted synthetic substrate_available by construction, PYTHONHASHSEED=0 numpy 42 sklearn 1.9.1 deterministic trajectory_id 1000 grouped perms seed 42, freeze hashes MATCH, raw_transitions 2ffc9e95 / 7215be08 / ab685d9d byte-identical structures
- Measurement status: G1 positive correlated control fails only on null_std>0.01 by 0.00033 (BC 0.706≥0.30 p 0.001 mean 0.0748<0.1 all pass) and G4 primary null degenerate both R1/R2 same std => per frozen gated rule status MEASUREMENT_INVALID outcome NOT_APPLICABLE verdict MEASUREMENT_INVALID pipeline_blind_or_miscalibrated, not scientific falsification; audit MEASUREMENT_INVALID producer_claim_supported false verifies threshold misspecification not blindness
- Calibration diagnosis: K=12->K=24 mean 0.1297->0.0748 corrects bias floor ~0.13 bits vs Laplace 0.3056 floor but perm_std 0.00941->0.00967 (+0.00026) still ≤0.01; audit flags perm variance N/strata property scaling down with N, so larger N worsens not fixes, requires distribution-aware/std check or analytic DM

### Rejected (bounded)

- No bounded rejection of correlated DOM_before beyond-memory dynamics via visible_text_hash or a11y_tree_hash on locally-hosted session-correlated FSMs — primary sig(R) not evaluated due G1/G4 MEASUREMENT_INVALID; descriptive BC 0.706>>thresholds but null degeneracy prevents adjudication
- No rejection of richer representations outside hash truncation (visual layout, computed CSS, interaction event sequences) — bounded to SHA256 16-hex truncated 5k
- No rejection of correlated regime due to independent-noise falsification; independent with 6 variants still BC~0 p>0.10 shows discrimination

### Unknown (open)

- Whether replacing absolute null_std>0.01 floor with distribution-aware or analytic Dirichlet-Multinomial bias-corrected degeneracy check would convert BC 0.707 into valid SURVIVES vs reveal true FALSIFIED if gap collapses
- What strata coarseness / fewer-longer trajectories / higher within-stratum DOM diversity raises grouped-permutation null_std above 0.01 while preserving BC gap 0.70
- Whether per-15-step regime P(flip)=0.07 vs per-trajectory L persistence yields different null centering
- What BC/null_mean/std/p/gap/Cohen d would be observed on true production BrowserGym WebShop DOM-bearing trajectories with session/permission correlated regimes outside hash truncation with richer visual/computed DOM
- What delta-repair cost, regime detector transfer, cross-site holdout would be if validated under relaxed thresholds
- Whether R1/R2 isomorphism double-counts for Bonferroni max 8
- Whether analytic DM could replace trajectory-grouped permutation for this n/strata

### Do Not Assume (dangerous non-conclusions, binding)

- Do not assume C-WEB-DYNAMICS falsified/supported/bounded-rejected — packet is MEASUREMENT_INVALID borderline null_std 0.00967≤0.01 by 0.00033, not scientific negative; magnitude thresholds pass decisively (BC 0.707>>0.30 p 0.001 gap 0.707)
- Do not assume pipeline blind or correlated construction failed — audit confirms NOT blind (BC far exceeds 0.30 gap far exceeds 0.05 H 3.334)
- Do not assume 0.707 BC is valid beyond-memory — bias floor 0.0748 accounts ~9.5% and null degenerate invalidates confirmatory claim; no post-hoc subtraction without new preregistration
- Do not assume larger N fixes degeneracy — grouped-permutation std scales DOWN with N per stratum, N~4000 worsens G1/G4; K only fixes mean not std
- Do not assume independent 0.00649 degenerate implies confound — G2 correctly not triggered
- Do not assume R1/R2 independent — isomorphic by construction identical BC expected
- Do not assume hash-DOM regime detectors product-ready — no SURVIVES, no transfer, no delta-repair, no visual representation test
- Do not assume locally-hosted 6-state Express synthetics substitute for production correlated latent regimes with larger state spaces, visual layout, computed style outside 5k hash truncation
- Do not assume null centering thresholds arbitrary — they correct Laplace floor 0.3056; do not relax post hoc without frozen rule
- Do not assume audit MEASUREMENT_INVALID implies claim falsified — audit claim_ceiling MEASUREMENT_INVALID bounds to calibration

This PIVOT directly implements audit required_fixes: replace absolute std floor with analytic DM + richer DOM, test orthogonal barrier/committor/timescale on existing trajectories, superseding hash-FSM K/N tuning loop.

## 3. Scientific Question (binding, refined to falsifiable experiment)

Director strategic question (request.json director_mandate.question verbatim, binding):

> On existing TodoMVC/BrowserGym WebShop trajectories without requiring new Gate0 production SPAs, does an orthogonal falsifiable program — barrier/committor (≥10 revisits to same URL,DOM with divergent futures, committor calibration) or timescale separation (autocorrelation decay/lag structure) with trajectory-grouped permutation (unit trajectory_id, N=1000-1999 seed 42), richer DOM (visual layout, computed style, event sequences, AX tree embedding not hash-truncated visible_text_hash/a11y) and analytic Dirichlet-Multinomial bias-corrected degeneracy — reveal beyond-memory predictive structure with valid null centering (|null_mean|<0.1, calibrated null_std via analytic DM) and BC>0.05 p_bonf<0.01 gap≥0.05 over B-DOM-SIMILARITY/B-MARKOV-1, where independent-noise control remains BC~0?

Refined falsifiable experiment: On existing locally-hosted correlated FSM bank (50x40=2000 N=1999, L per trajectory basin 0.70/0.30, 36 hashes baseline) regenerated with richer DOM observables (visual bbox, computed style, event n-grams, AX embedding, not SHA256 5k-truncated) and, if available, existing BrowserGym WebShop trajectories with DOM/AX at 1280x720 (reused bank, N=1000-1999, no new collection), with trajectory-grouped permutation (1000 perms unit trajectory_id seed 42) and analytic Dirichlet-Multinomial bias correction, does barrier/committor (≥10 revisits to same canonical state s=(URL, DOM_rich_cluster, H_K=3) with divergent futures, committor q(s) calibration ECE≤0.15) or timescale separation (autocorrelation decay tau>5 vs null ~1, lag-MI gap≥0.05) reveal I(S_next;DOM_rich|URL,H_K,Action)>0.05 bits with p_bonf<0.01, |null_mean_analytic|<0.1, calibrated analytic null_std valid and perm-analytic consistency <0.03, gap≥0.05 over B-DOM-SIMILARITY (TF-IDF k5) and B-MARKOV-1, while independent-noise rich-DOM replication remains BC~0 (|BC|<0.05 p>0.10) and IID null BC≤0.03? Either valid SURVIVES (first beyond-memory correlated richer-DOM dynamics via barrier/timescale without Gate0, with valid centering and calibrated null) or valid FALSIFIED (richer DOM insufficient even with constructed correlation and calibrated correction) changes claim/product decision without Gate0 or hash-FSM K/N loop.

## 4. Motivation & Why This Is the Smallest High-Information Test

### 4.1 Why PIVOT is required (tunnel diagnosis)

- Parent recalibration K=12->K=24 fixed bias floor (mean 0.1297->0.0748 passes |null_mean|<0.1) but not variance (std 0.00941->0.00967 fails null_std>0.01 by 0.00033 on BOTH R1/R2). Audit diagnoses absolute floor 0.01 as structurally incompatible — perm variance scales DOWN with N/strata, so N~4000 at K=12 worsens degeneracy (0.0094-> expected ~0.006), and K conflates smoothing bias with permutation spread. Repeated same hash-truncated K/N tuning is low marginal information (director comparative: 9/10 frontier scaling failures rho~0 CV>0.5, Gate0 0/3 real SPAs after 80+ exps blocked). Continuing this loop repeats measurement-invalid transaction without new representation.
- Exhaustive Gate0 SPA search 0/2-0/3 after 80+ exps and last BrowserGym/CAP/Mind2Web-2/WebJudge enumeration closes production-SPA CMI path that required title>=2 and H>0.2 gating; TodoMVC hash-SPAs have 0.0 dom_bytes and constant title entropy 0.0. Another Gate0 retry repeats blocked path.
- Frontier TV/KDE/binned 61 experiments show persistent estimator-specific blind spots (kNN fails scaling, KDE fails rotation) and 95% non-stationary attenuation — another alpha/bandwidth/K tweak near zero information.
- Director portfolio: 260 canonical exps, 65 WEB-DYNAMICS HYPOTHESIS, no PRODUCT_CORE, physics IDLE tunnel_flag true, first C1+C3-passing Bayesian DM still absolute BF negative on real TodoMVC. Orthogonal program on existing trajectories avoids discovery cost and tests qualitatively different dynamics (barrier = metastable basin hopping, committor = probabilistic branching, timescale = slow latent regime separation) that are identifiable via revisits/lag structure with history-conditioned baselines required by identifiability.

### 4.2 Why orthogonal barrier/committor/timescale with richer DOM is falsifiable and not physics-as-graph

- Physics claims require operational mathematical object, observable, falsifier, strong nulls, identifiability (MASTER_PROMPT §15). Graph reuse is not Physics. This design provides:
  - Operational object: barrier as -log P_transition between basins, committor q(s)=P(hit B before A | s), timescale tau from ACF decay.
  - Observable: revisits to same canonical state s with divergent futures (≥10 revisits, both basins observed), lagged DOM_rich -> S_next.
  - Falsifier: BC≤0.05 or p≥0.01 or gap<0.05 or ECE>0.15 while gates pass => FALSIFIED-IN-SETTING bounded to tested richer reps.
  - Strong nulls: B-DOM-SIMILARITY (ordinary similarity), B-MARKOV-1/K3 (Markov), trajectory-grouped shuffle (history-conditioned), independent-noise calibrated null (policy-matched), time-shuffle (timescale).
  - Identifiability: ≥10 revisits per s, divergent futures fraction, H(S_next|C)>0.2 ensures not deterministically forced, MI(DOM;Action)<0.10 ensures not action tautology, trajectory_id grouping preserves dependency structure.
- Prior hash truncation 5k visibleText/a11y_tree_hash isomorphic (36 hashes for 6*2L*3 variants, both SHA256(L||state||variant%3)) lost visual/computed/event information that may carry L. Richer DOM (visual bbox, computed style color/visibility, event n-grams, AX embedding) bypasses this loss without requiring new SPA discovery.
- Analytic DM bias correction: closed-form E[CMI|null] via Gamma functions for Dirichlet-Multinomial at K=12/24 separates smoothing bias floor (|null_mean|<0.1) from permutation variance. Calibrated null_std via analytic variance + perm_std consistency check replaces absolute 0.01 floor that was degenerate. This directly addresses audit required_fixes without conflating K tuning with variance calibration.

### 4.3 Interdisciplinary alignment (director agent priors, distinguished from SPIDER evidence)

- Agent prior: prompt-immediate salience overfits — motivates history-conditioned nulls B-DOM-SIMILARITY/B-MARKOV-1 and ablating adopt-any-observed-key inflation; not presented as Codex fact.
- Prior: compounding errors over 10-15 step rollouts needs trajectory-grouped permutation (unit trajectory_id N=1000-1999 seed 42) and task-specific start_url; not Codex evidence.
- Prior: caching vs verification tradeoff ECE≤0.15 false_accept≤0.10 — motivates calibrated committor abstention gate; not Codex evidence.
- Prior: retrieval locality dominates cost — motivates residual-novelty economics downstream; not tested here.

### 4.4 Why smallest high-information

- Positive or negative outcome with valid analytic gates changes C-WEB-DYNAMICS ceiling and product decision without Gate0: SURVIVES => first validated beyond-memory correlated dynamics via richer DOM barrier/committor/timescale (gap over similarity/Markov, calibrated centering, independent ~0), justifies regime detector as mechanical prior; FALSIFIED => parks hash-based FSM approach and shows even richer DOM insufficient on tested bank with calibration, forcing PARK and awaiting larger production manifest; MEASUREMENT_INVALID (positive blind or independent confounded or Q<10 revisits) is informative refusing false negative and documenting substrate Q.
- Marginal information gain per director portfolio assessment vastly exceeds another K=24 hash FSM or Gate0 SPA or CAP 567MB LFS search. Estimated cost <2h (reuses existing trajectories, stdlib, no LLM).

## 5. Hypotheses (frozen, exhaustive)

### H_barrier_committor (primary orthogonal, richer DOM)

On existing banks (correlated FSM rich-DOM 50x40 N=1999 H~3.3 strata 24 AND BrowserGym WebShop bank if available N=1000-1999), for states s=(URL_normalized, DOM_rich_cluster, H_K=3) with ≥10 revisits and divergent futures, committor q(s) is calibrated (ECE≤0.15) and BC = I(S_next; DOM_rich | URL, H_K=3, Action) >0.05 bits with trajectory-grouped permutation p_bonf<0.01 (Bonferroni max 8, floor 0.001 at 1000 perms or analytic p), |null_mean_analytic|<0.1, calibrated null_std valid (analytic_std and perm_std consistency |perm-analytic|<0.03), gap_R≥0.05 over B-DOM-SIMILARITY and B-MARKOV-1 on ≥1 richer DOM representation (R_visual, R_computed_style, R_event_seq, R_AX_embedding). Mechanism: DOM_rich carries latent L/session-state biasing S_next beyond history and similarity.

### H_timescale (co-primary orthogonal)

Slow latent regime L per trajectory induces timescale separation: autocorrelation decay tau_correlated >5 steps vs tau_independent ~1 and lag-1..5 MI I(S_{t+k}; DOM_t|C) >0.05 at lag 1-3 with p<0.01 and gap over time-shuffled null (B-TIMESCALE-SHUFFLE) ≥0.05, with valid analytic centering as above. Used if barrier revisits sufficient; if <5 states meet ≥10 revisits, timescale becomes primary.

### H_positive_control_rich

Same pipeline on synthetic correlated rich-DOM must achieve BC≥0.30 p<0.01 |null_mean_analytic|<0.1 calibrated std valid consistency<0.03 and committor ECE≤0.15 Brier gap≥0.05 over Markov on R_rich. Theoretical capacity ≥0.40 bits (binary L * 0.70/0.30 basin bias). Failure => MEASUREMENT_INVALID pipeline blind to constructed correlation. Any outcome-informed change to construction EXPLORATORY.

### H_null_independent_rich (negative control, recalibrated richer)

Identical analytic DM + 1000 grouped perms on independent-noise rich-DOM replication (≥6 variants/state independent per-step, same FSM without L, richer DOM sampled independently of S_next, 50x40 N=1999) must show BC~0 |BC|<0.05 p>0.10 |null_mean_analytic|<0.1 calibrated std valid. If BC≥0.05 p<0.10 with valid null => MEASUREMENT_INVALID pipeline confounds.

### H_null_iid

IID synthetic null (same marginal P(S) i.i.d. S_next seed 42, DOM_rich still correlated with phantom L) must show BC≤0.03 p>0.10 |null_mean_analytic|<0.1 calibrated std valid.

### H_null_shuffled (permutation + analytic)

Within-strata grouped shuffle DOM_rich on correlated bank: analytic mean accurate within 0.03 of perm mean and |null_mean_analytic|<0.1 calibrated std valid; degenerate on BOTH richer sets triggers MEASUREMENT_INVALID not falsification.

## 6. Data Generation & Reuse (no new Gate0 discovery)

### 6.1 Primary correlated rich-DOM bank (locally-hosted, same FSM class as parent but richer observables)

- **Construction** (frozen deterministic PYTHONHASHSEED=0 numpy 42): 6-state FSM states 0-5, 4 primitives uniform (click/fill/navigate/submit), target_sig role+name+testId never href. Latent L in {A,B} per trajectory primary (50 trajectories x40 steps =2000 transitions N=1999 analyzed; exploratory per-15-step regime P(flip)=0.07 documented but not primary). Transition: P(S_next|S_current,Action,L=A) favors basin {0,1,2} 0.70/0.30, L=B mirrored 0.30/0.70, p_stay 0.70. URL_before = `https://spa.local/#/state_{S}` hash fragment preserved. **Richer DOM_before** (replaces 5k SHA256 truncation): R_visual = AX bbox (x,y,w,h quantized) + element_count/tree_depth/interactive_density; R_computed_style = dict {color, background, visibility, display, opacity} sampled per (L,state,variant) from finite vocab (6 variants/state); R_event_seq = n-gram of last 3 A primitives; R_AX_embedding = TF-IDF embedding of a11y names (k-means into 20 clusters fit TRAIN only). Each R sampled from family correlated with L: e.g., visual x = 100+50*L_indicator + variant%3*10. Thus |R|/N ~0.02-0.15 (higher than hash 0.018 but finite). Generate N=1999, 36-120 hashes equivalent richness. Seeds identical to parent to allow direct hash comparison.
- **Recalibration**: analysis uses Bayesian DM K=12 alpha=1/K (1/12≈0.083) primary and K=24 alpha=1/K exploratory; no generation change aside from richer observables.
- **Sample size**: 2000 transitions gives 24 strata avg ~83 largest ~333, power for BC 0.10 at calibrated std ~0.01-0.02, BF calibration N/K≥83 at K=24. Revisits expectation: URL fragment 6 states but richer DOM clusters 20 -> ~100 states, revisits per state expectation ~20, so ≥5 states with ≥10 revisits achievable (if not, timescale becomes primary and Q failure triggers MEASUREMENT_INVALID).

### 6.2 Independent-noise rich-DOM replication (null control)

Same FSM without L, transition uniform basins p_stay 0.50, DOM_rich variant independent per-step among ≥6 richer variants per state (rng.choice(6) seeded per step independent of S_next, same richer vocab as above). Generate 50x40=2000 N=1999. Expect BC~0 per prior -0.005 but with richer diversity calibrated std valid > analytic floor.

### 6.3 IID synthetic null

Same marginal P(S) estimated from correlated rich bank but S_next i.i.d. per step seed 42, DOM_rich still sampled from L-correlated family but S_next independent => BC~0 BF favors order1. Same K analytic.

### 6.4 Existing BrowserGym WebShop / TodoMVC reuse (no new collection)

If research/intel/manifest.json or runtime bank provides trajectories with DOM/AX at 1280x720 and URL+title, include as secondary primary (N=1000-1999, trajectory_id grouping). No new browsing; reuse raw bytes already collected. Report Q (revisits), dom_bytes presence, |R|/N, H(S_next|C). If Q<5 states with ≥10 revisits, WebShop secondary is diagnostic only, not gating.

### 6.5 Sample size & power (analytic corrected)

Channel capacity binary L with bias 0.70/0.30: theoretical I(S_next;L|C) ~0.40 bits pooling across S_current; at 60% DOM_rich->L recovery expected BC ~0.30-0.35 at K=12. Analytic null_mean expected ~0.07 at K=12, ~0.05 at K=24 (lower smoothing bias), so BC 0.30 gives d ~15-30 vs calibrated std 0.01-0.02. Power via analytic CI width ~2*std ~0.02-0.04. Independent with 6 richer variants expected analytic std ~0.012 > floor while BC~0.

## 7. State, Action, History, DOM Operational Definitions

### 7.1 State S_next
Primary S_next = SHA256(normalize(URL_after)|'|'|normalize(title_after)) normalize(URL)=lowercase, strip query ?session=/?token=, preserve SPA hash fragment #/, strip trailing slash; normalize(title)=trim lowercased 200 chars (constant allowed). Exploratory S_URLonly SHA256(norm URL). S_next at t+1 distinct from DOM_before at t. Report unique_titles, title_entropy, H(S_next|C).

### 7.2 Action A_leakageFree
A=(primitive,target_sig) primitive in {click,fill,navigate,select,submit,hover} target_sig=role+name+testId+aria-label never href/URL/src. Diagnostic A_leaky=+href for leakage gap only. Report MI(DOM_rich;Action) must be <0.10 else tautological.

### 7.3 History H_K=3
H_K=(A_{t-2},A_{t-1},A_t, S_{t-2},S_{t-1},S_t) last 3 steps; strata key C=(URL_before_normalized, H_K_actions) URL_without_title to avoid leakage. Require strata_count≥5 unique C with ≥3 per stratum; singleton_SA_rate<70%; report H(S_next|C) ceiling must be >0.2 (if ≤0.2 barrier/committor forced 0 => MEASUREMENT_INVALID environment ceiling) and strata_ge3 count.

### 7.4 DOM_rich representations (tested independently, not hash-truncated)

- R_visual: AX bbox x,y,w,h quantized into 10 bins + element_count/tree_depth/interactive_density/form_count numeric structural (expected 0.0 prior but now continuous)
- R_computed_style: computed CSS {color, backgroundColor, visibility, display, opacity} discretized vocab 6 variants/state per L
- R_event_seq: n-gram of last 3 primitives (e.g., 'click_fill_click')
- R_AX_embedding: serialized AX role/name/value up to 5k chars via simulated Accessibility.getFullAXTree, TF-IDF k-means 20 clusters fit TRAIN only, embedding cosine not hash

Raw observables preserved (visual JSON, style dict, event seq string, a11y_bytes 5k truncated documented). Primary requires ≥1 R visual/style/event/AX_embedding; all expected to correlate with L but with varying fidelity. Document truncation/clustering loss.

### 7.5 Barrier/Committor operational

Canonical state s = (URL_before_normalized, DOM_rich_cluster_label, H_K_actions) clustered joint. Revisits table: count visits per s across trajectories. For s with ≥10 revisits, collect futures horizon 10: label hit B if S_next enters {3,4,5} before {0,1,2} (or empirically discovered basins via per-trajectory L frequency). Estimate q(s)=P(hit B before A | s). Require ≥5 states with ≥10 revisits and at least 2 states with divergent futures (0.2<q<0.8) for identifiability. Report divergent fraction.

## 8. Measures

### 8.1 Primary: Bayesian DM analytic bias-corrected CMI + barrier/committor + timescale

For each (dataset, R in richer set):
```
H(S_next|C) DM K analytic Gamma
H(S_next|C,DOM_rich_cluster) similarly
CMI_obs = H(S_next|C) - H(S_next|C,DOM)
analytic_null_mean, analytic_null_std closed-form Gamma ratios for Dirichlet alpha=1/K
perm Null: 1000 trajectory-grouped shuffles within each C stratum grouped by trajectory_id seed 42 => perm_mean, perm_std, p_raw
BC = CMI_obs - analytic_null_mean (primary) ; also BC_perm = CMI_obs - perm_mean diagnostic
consistency = |perm_mean - analytic_mean| must be <0.03
calibrated_std = max(analytic_std, perm_std, 0.005 floor analytic) ; require calibrated_std valid
p_bonf = min(1, p_raw * n_tests) n_tests = n_R * (1 primary +2 baselines) max 8, floor 0.001 at 1000 perms
Cohen d = BC / calibrated_std, 95% CI via permutation percentiles
BF_10 for order3 vs order1 via DM log BF nats; calibration on IID must favor order1 (nats<0)
Revisits per s, divergent futures, q(s), ECE, Brier, ACF tau, lag-MI
Report: BC, analytic_mean, perm_mean, consistency, calibrated_std, p_raw/p_bonf, d, CI, cardinality |R|/N, strata stats, H ceiling, MI(DOM;Action), revisits table
```

### 8.2 Baselines (same estimator K analytic+perm, same grouping)

- B-DOM-SIMILARITY BC_sim: TF-IDF or embedding cosine k=5 fit TRAIN only -> BC_sim via same DM; gap delta_sim = BC - BC_sim must be ≥0.05
- B-MARKOV-1 BC_markov1: MLE P(S_next|URL,A) fit TRAIN -> gap ≥0.05
- B-MARKOV-K3 BC_hist accuracy
- B-SHUFFLE-GROUPED null distribution
- B-TIMESCALE-SHUFFLE for autocorr
- B-TRAJECTORY-MEMORY, B-SITE-LEAKAGE gaps

### 8.3 Auxiliary per dataset per R

NL, strata_count, strata_ge3, singleton_rate, leakage_validOnly, link_share, H(S_next|C), unique_DOM_clusters, |R|/N (expected 0.02-0.15 richer vs 0.018 hash), analytic_mean/std, perm_mean/std, consistency, Cohen d, CI, MI(DOM;Action), q(s) distribution, ECE/Brier, ACF 0..5 tau, BF nats, card stats, dom_bytes/a11y_bytes/visual_bytes, revisits Q.

## 9. Null Models & Baselines (strong, all executed as frozen)

Enumerated in spec baselines §8.2. All executed with identical grouping (trajectory_id), seeds 42, preprocessing fit TRAIN only (70/30 by trajectory_id), Dirichlet prior alpha=1/K, N=1999. Mandatory B-DOM-SIMILARITY and B-MARKOV-1 must be executed; gap gating for SURVIVES. Analytic DM provides calibrated null_std, not absolute permutation floor alone. No silent omission: if baseline cannot be computed or no s meets ≥10 revisits, publish validity_note and trigger MEASUREMENT_INVALID for that representation/branch, not FALSIFIED.

## 10. Statistical Tests & Uncertainty (frozen, corrected per audits)

- **Permutation+Analytic**: 1000 trajectory-grouped shuffles DOM_rich within each C stratum grouped by trajectory_id seed 42 deterministic + closed-form analytic DM mean/std via Gamma. Consistency |perm-analytic|<0.03 required for calibrated inference; primary BC uses analytic mean. Resampling unit trajectory_id; no Gaussian jitter.
- **p-value**: p_raw one-sided (1+#{perm>=CMI_obs})/1001, or analytic p via Dirichlet tail where 1000 perms gives floor 0.001 <0.01 reachable. Bonferroni primary p_bonf = min(1, p_raw * n_tests) n_tests≤8, alpha 0.01. Report raw and Bonferroni; BC also gates via absolute 0.05.
- **BF**: log BF via Gamma, no resampling; BF>10 (nats>2.3) auxiliary but primary gates on BC not BF; calibrated on IID must be <0.
- **Effect size**: Cohen d = BC / calibrated_std (calibrated_std valid required); 95% CI via grouped permutation percentiles, NOT Gaussian.
- **Seed determinism**: PYTHONHASHSEED=0, numpy 42, sklearn 42; builtin hash() never used; SHA256 for S_next hashing.
- **Valid centering**: |analytic_null_mean|<0.1 and calibrated_std valid and consistency<0.03 required; else MEASUREMENT_INVALID. This replaces absolute null_std>0.01 alone (which scaled down with N) with analytic+consistency calibration addressing audit diagnosis.

## 11. Controls (frozen)

### Positive control (correlated rich-DOM, analytic)

Synthetic correlated rich must achieve BC≥0.30 p_raw<0.01 |analytic_null_mean|<0.1 calibrated std valid consistency<0.03 and committor ECE≤0.15 Brier gap≥0.05 or tau gap on ≥1 R_rich. Failure => MEASUREMENT_INVALID pipeline blind. Frozen construction latent L per trajectory bias 0.70/0.30 richer DOM family per (L,state,variant) K=12 (or K=24 exploratory). Any outcome-informed change EXPLORATORY violation.

### Null controls (recalibrated richer + analytic)

- Independent-noise rich replication ≥6 variants/state must show |BC|<0.05 p>0.10 |analytic_null_mean|<0.1 calibrated std valid consistency<0.03 (replicates prior 0.004 but with valid analytic variance). If BC≥0.05 p<0.10 with valid null => MEASUREMENT_INVALID pipeline_confounds.
- IID null must show BC≤0.03 p>0.10 |analytic_mean|<0.1 valid.
- Trajectory-grouped permutation analytic null on correlated bank must be |analytic_mean|<0.1 calibrated std valid consistency<0.03; degenerate on BOTH richer representations triggers MEASUREMENT_INVALID.
- Timescale shuffle must show tau~1 BC_lag~0.

### Data-quality / identifiability controls

NL=1999 (2000 generated) or BrowserGym N=1000-1999, strata≥5 with ≥3 per stratum, singleton<70%, H(S_next|C)>0.2, |R|/N expected 0.02-0.15 richer, trajectory count ≥20, leakage_validOnly not gating but reported, revisits Q≥5 states with ≥10 visits and divergent futures required; if Q=0 => MEASUREMENT_INVALID substrate_insufficient (not falsification) preserving physics red flag barrier identifiability.

## 12. Validity Threats & Mitigations

| Threat | Mitigation |
|---|---|
| Target leakage href==URL | Leakage-free A excludes href; DOM_before distinct timestep; diagnostic gap; MI(DOM;Action)<0.10; state normalized without title in C |
| Split leakage | TF-IDF/embedding vocab / k-means centroids / Dirichlet counts fit TRAIN trajectories only (70/30 by trajectory_id); site identity never feature |
| Sampling/policy confounding | Document FSM policy (50x40 uniform among primitives per trajectory) and WebShop policy as collected; separate policy regularity; determinism via seeds; trajectory_id unit |
| Uncertainty mis-specification (prior item-level shuffle, Gaussian jitter) | Grouped permutation by trajectory_id fixes item-level; analytic DM corrects bias floor; no Gaussian jitter; calibrated std via analytic+perm consistency; degeneracy=>MEASUREMENT_INVALID |
| Representation loss (hash 5k truncation, K smoothing, clustering) | Replace hash truncation with richer raw observables (visual bbox, computed style, event n-grams, AX embedding clusters fit TRAIN only); preserve raw JSON; document quantization/k=20; sensitivity hash vs richer exploratory |
| Synthetic-to-real gap | Claim bounded to existing locally-hosted rich FSM + BrowserGym bank, not production correlated regimes outside bank; audit identifiability mitigated by gap over similarity/Markov and MI checks |
| H=0 determinism ceiling / Q<10 revisits | Report H(S_next|C) and revisits Q; if H≤0.2 or Q<5 states with ≥10 divergent => MEASUREMENT_INVALID environment ceiling, not falsification |
| Hash tautology action->DOM or DOM->S_next leakage | DOM_rich correlated with L not with Action; report MI(DOM;Action)<0.10 and MI(DOM;Action_FREQuency) gap; barrier requires divergent futures (not unique mapping) |
| Unreachable Bonferroni | N=1999 1000 perms floor 0.001 <0.01 reachable; report raw and Bonferroni; BC also gates; analytic p supplements |
| K bias floor degeneracy 0.129>0.1 | Analytic DM correction with consistency check replaces absolute floor; K=12 primary, K=24 exploratory; no post-hoc relaxation without new prereg |
| Independent null_std degenerate 0.0046 | Richer 6-variant DOM and analytic std expected calibrated > analytic floor; if still degenerate report and trigger MEASUREMENT_INVALID per G2, not silent |
| Committor manufactured from sparse topology (red flag) | Require ≥10 revisits per s and divergent futures (both basins observed) before estimating q(s); report revisits table; if Q=0 validly halt |
| Timescale spurious autocorrelation | Compare tau vs time-shuffled null B-TIMESCALE-SHUFFLE; require tau gap >4 and lag-MI gap≥0.05 |
| Result/report drift | All metrics recomputed from raw_results.json + raw_transitions; freeze hashes verified before execution; byte-identical re-executable |

## 13. Decision Rules (frozen, pre-outcome)

### Pipeline gates (in order, any triggers MEASUREMENT_INVALID, no claim update)

- G1: positive correlated rich control BC<0.30 OR p≥0.01 OR |analytic_null_mean|≥0.1 OR calibrated_std degenerate (analytic_std≤0.005 and perm_std≤0.01) OR |perm-analytic|≥0.03 => pipeline_blind_or_miscalibrated (prevents false negative; prior hash BC 0.688 p 0.001 but perm_std 0.0094 borderline)
- G2: independent-noise rich replication BC≥0.05 and p<0.10 with valid analytic null (|analytic_mean|<0.1 calibrated std valid consistency<0.03) => pipeline_confounds
- G3: IID null BC>0.03 and p<0.10 with valid null => null miscentered
- G4: identifiability fails: no s meets ≥10 revisits with divergent futures on ≥5 states OR H(S_next|C)≤0.2 => null_degenerate_no_branching (not falsification, per physics red flag)
- G5: primary analytic-perm consistency fails on BOTH richer representation sets (|perm-analytic|≥0.03) => model_mismatch
- If any G fails, verdict=MEASUREMENT_INVALID, publish gate_table, do not evaluate primary

### Primary decision (only if gates pass)

For each R in {R_visual,R_computed_style,R_event_seq,R_AX_embedding}, compute BC_R, p_bonf_R, analytic_null_mean_R, calibrated_std_R, consistency_R, BC_sim_R, BC_markov1_R, gap_R = BC_R - max(BC_sim_R,BC_markov1_R), d_R, CI, ECE_R, Brier_gap_R, tau_R/lag_MI_gap_R

Define sig(R)=1 if BC_R>0.05 AND p_bonf_R<0.01 AND |analytic_null_mean_R|<0.1 AND calibrated_std_R valid AND consistency_R<0.03 AND gap_R≥0.05 AND (ECE_R≤0.15 OR tau gap validated)

- If EXISTS R with sig(R)==1 => SURVIVES_CURRENT_TEST — richer DOM barrier/committor or timescale reveals predictive information beyond (URL,H_K,Action) and beyond ordinary similarity/Markov on existing bank without Gate0, with valid analytic centering and calibrated null, while independent remains ~0
- If FORALL R, BC≤0.05 OR p≥0.01 OR gap<0.05 OR calibration fails while gates pass => FALSIFIED-IN-SETTING — richer DOM barrier/committor/timescale does not carry detectable predictive information beyond memory/similarity via analytic pipeline, bounded to tested richer reps and existing bank (locally-hosted rich FSM + WebShop reuse) and K analytic
- Sensitivity (hash vs richer comparison, K=12 vs 24, S_URLonly, R multi_feature, H_K=2/4, per-15-step regime) not gating; report exploratory but do not alter primary verdict

### Exploratory (only if FALSIFIED and gates passed)

Report H(S_next|C,D) decomposition, per-strata CMI histogram, MI(L;DOM_rich) vs MI(L;S_next), TF-IDF gap, independent 6-variant stability, ACF tables, committor q(s) scatter. These do NOT alter primary FALSIFIED verdict but inform park vs richer production manifest.

## 14. Consequences

### If SURVIVES (valid analytic gates)

- C-WEB-DYNAMICS ceiling expands to: barrier/committor or timescale beyond-memory dynamics via richer DOM (visual/computed/event/AX embedding) on existing bank without Gate0 via Bayesian analytic DM + trajectory-grouped permutation with BC>0.05 p<0.01 gap≥0.05 calibrated centering independent~0 and ECE≤0.15. First orthogonal beyond-memory correlated dynamics outside hash truncation and outside synthetic 2D TV/KDE pooled blind spots and beyond independent-noise 0.004 falsification.
- Product: distill richer-DOM regime detector as mechanism preconditions/barrier guards/freshness sentinels (regime-aware retrieval grouped by latent L cluster, visual+AX embedding signature, event-seq guard) into kernel resolve/verify; prioritize BrowserGym/runtime collection on session-correlated sites (auth/cart/personalization) at 1280x720 with Accessibility.getFullAXTree where latent regimes amplify; quantify delta-repair cost when session shifts and cross-site holdout transfer; measure residual-novelty economics via regime detection work-compression.
- Physics next: test invariance across site types and latent regimes (permission vs user-data vs external API), larger state spaces, quantify transfer, test on production correlated SPAs when intel manifests larger (now justified).

### If FALSIFIED (valid analytic gates)

- C-WEB-DYNAMICS remains HYPOTHESIS but orthogonal richer-DOM barrier/committor/timescale program closed for this bank and richer representations at K analytic N=1000-1999: even with DOM_rich correlated by construction with latent L determining S_next, richer DOM does not carry detectable predictive information beyond history and similarity/Markov via analytic pipeline (gap<0.05 or BC≤0.05 or p≥0.01). Combined with prior hash-only falsifications (-0.005, 0.0, borderline 0.707 degenerate) this parks hash-truncated FSM approach and indicates even richer DOM barrier not mechanistically productive on tested bank.
- Product: do NOT invest in DOM regime detectors on this representation class; Graph/Product rely on trajectory memory/retrieval without physics prior; economics via retrieval/verification/repair amortization alone (C-RESIDUAL-NOVELTY). High-value as it prevents wasted physics spend on richer DOM barrier.
- Physics next per director rationale: PARK correlated-DOM barrier/committor/timescale on richer DOM pending larger production manifest with real session/permission latent regimes and larger state spaces before further physics spend; do not loop K/N tuning beyond this analytic recalibration; consider frontier MemoryArena or alternative Web-Physics mechanisms.

### If MEASUREMENT_INVALID (analytic gates still fail)

- No claim update. Report exact gate failed, per-dataset table, analytic_mean/std, perm_mean/std, consistency, revisits Q, H ceiling, unresolved substrate. Retry not scientific negative. Preserve epistemic discipline. Next unblock per mandate would be larger production manifest with real session latent regimes, not silent threshold relaxation.

## 15. Analysis Plan (deterministic order, no outcome peeking before freeze)

1. **Verify freeze integrity**: check request.json sha256, spec.json, prereg.md hashes match freeze.json before any computation; record commit HEAD and parent 9daed76d...
2. **Assemble banks** (deterministic PYTHONHASHSEED=0 numpy 42): (a) correlated rich-DOM primary 50x40=2000 N=1999 via generate_correlated_rich.py frozen (same L per trajectory bias 0.70/0.30 but richer observables), (b) independent-noise rich replication 50x40 ≥6 variants per state via generate_independent_rich.py frozen, (c) IID synthetic null via generate_iid_rich.py frozen, (d) reuse BrowserGym WebShop/TodoMVC raw bank if available at research/intel/manifest.json (read-only, no new browser). Save raw_transitions_*.json with fields {trajectory_id, step, URL_before/after, title, Action_primitive, target_sig, DOM_rich_visual JSON, DOM_rich_computed_style dict, event_seq, AX_tree, AX_embedding_cluster, S_next hash, latent L, variant_mod}. Compute sha256 per file.
3. **Compute strata**: for each dataset build C=(URL_before_normalized, H_K=3 actions) with H_K as defined, report strata_count, strata_ge3, singleton rate, H(S_next|C), leakage diagnostics, cardinality |R|/N per richer R, dom_bytes/visual_bytes, revisits Q table (counts per s).
4. **For each (dataset,R in {R_visual,R_computed_style,R_event_seq,R_AX_embedding, R_multi_exploratory})**: compute Bayesian DM analytic Gamma marginal H(S_next|C) and H(S_next|C,DOM_rich_cluster) K=12 (and K=24 exploratory) => CMI_obs, analytic_null_mean/std, BC, run 1000 trajectory-grouped permutations within each C stratum grouped by trajectory_id seed 42 => perm_mean/std, p_raw/p_bonf, d, CI percentiles, BF_10; compute B-DOM-SIMILARITY TF-IDF/embedding k5 fit TRAIN only => BC_sim; compute B-MARKOV-1/K3 MLE fit TRAIN => BC_markov gap; compute B-TRAJECTORY-MEMORY, B-SITE-LEAKAGE, MI(DOM;Action); for barrier states with ≥10 revisits compute q(s) ECE Brier tau ACF lag-MI vs time-shuffle.
5. **Apply gated decision rule** §13 in order, publish per-representation table, revisits table, ACF table, permutation+analytic histograms, strata tables, gate/control tables, provenance with sha256; no metric built from report before freeze hash.
6. **Commit** all raw transitions, richer DOM JSON, hashes, strata tables, permutation+analytic distributions, revisits/ACF tables, code paths (generate_*.py, analyze.py) with sha256 in provenance.json; verify re-executable aside from elapsed; include exploratory N BrowserGym secondary if time permits but not gating.

## 16. Freeze Statement

This preregistration is frozen before any outcome data for the orthogonal barrier/committor/timescale with richer DOM and analytic DM decision is inspected. Richer DOM representations (visual bbox, computed style, event n-grams, AX embedding clusters) and analytic Dirichlet-Multinomial bias correction (closed-form Gamma, consistency <0.03) replace prior SHA256 5k hash truncation that caused null_std degeneracy (perm_std 0.0097 scaling down with N, mean 0.0748 vs absolute floor). Trajectory-grouped permutation (1000 perms unit trajectory_id seed 42, N=1000-1999) preserves history-conditioned nulls required by identifiability (≥10 revisits divergent futures, H>0.2) and director mandate B-DOM-SIMILARITY/B-MARKOV-1 gap≥0.05. Correlated construction (L per trajectory bias 0.70/0.30, richer DOM family per L/state/variant) and independent-noise recalibrated to ≥6 richer variants are defined by construction, not by peeking at correlated BC under richer DOM. Gate0 not required is intentional substrate_available design (no exhaustive 567MB LFS/CAP search), not weakened gate. Any deviation after freeze is labeled EXPLORATORY and cannot support confirmatory SURVIVES/FALSIFIED. A new confirmatory claim requires new preregistration and untouched evidence. Estimated cost <2h wall-clock, no LLM calls, stdlib only, on existing banks.

## 17. References to Prior Evidence

- Parent EXP-PHYSICS-35787698409 (MEASUREMENT_INVALID borderline |null_mean|0.0748<0.1 null_std0.00967<0.01 BC 0.707 p 0.001 gap 0.706 H 3.334) — direct predecessor; audit required_fixes replace absolute std floor with analytic/distribution-aware and test richer DOM outside hash truncation; this PIVOT supersedes its next_question
- EXP-PHYSICS-35782523165 (MEASUREMENT_INVALID |null_mean|0.1297 null_std 0.0094 BC 0.688) — K=12->K=24 mean fix not std fix
- EXP-PHYSICS-34764605162 (FALSIFIED-IN-SETTING independent-noise BC 0.004/0.025 p=1.0 audit V1_independent_noise_bakes_in_null flags correlated open) — independent falsified, correlated open setting tested here orthogonally
- Frontier 61 pooled TV/KDE/binned tunnel (kNN fails scaling rho -0.12, KDE fails rotation rho 0.286, CV>0.5, attenuation 95%) — orthogonal pivot per director
- EXP-INTEL-35773136560 (0/3 Gate0 exhaustive BrowserGym/CAP/Mind2Web) and Gate0 0/3 after enumeration — closes production-SPA PMI path, justifies locally-hosted rich synthesis
- Bayesian DM K=12 N=1999 validated C1+C3 but absolute BF -10 to -15 nats on real TodoMVC — reused analytic here
- Codex C-WEB-DYNAMICS HYPOTHESIS 65 exps, physics IDLE tunnel_flag true, claim registry sha 3511a788, lane registry physics priority C-WEB-DYNAMICS
- SPIDER_MASTER_PROMPT §15-22 (validity gates, strong nulls, identifiability, representation loss, cluster≠attractor, committor requires branched evidence), SPIDER_ARCHITECTURE_RESEARCH2 §4-6 (packet, Codex, freeze), AGENTS.md transmission discipline, POLICY.md director mandate, research/EXPERIMENT_PACKET.md mandatory fields (§3 spec, §4 result) and agent priors (distinguished from SPIDER evidence) per director_mandate.agent_priors_used

