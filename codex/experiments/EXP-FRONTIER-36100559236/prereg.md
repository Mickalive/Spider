# EXP-FRONTIER-36100559236 Preregistration — Heterogeneous Residual-Novelty Verification Economics (Director PIVOT)

**Lane:** frontier — C-RESIDUAL-NOVELTY (pay-novelty-not-length)
**Mode:** DESIGN ONLY — no outcome-bearing measurements executed
**Director mandate:** PIVOT cognitive_reset true, allocation C-RESIDUAL-NOVELTY, question verbatim from `request.json:director_mandate.question`, SUPERSEDE over synthetic 36-family non-Pareto (36042599040) and alias ceiling 21/40=0.525
**Parent handoff:** `research/experiments/EXP-FRONTIER-36099072254/handoff.json` sha256 ef479f0688ce9d207ce3a207cda6f52683ec845e3182286c33c37d4ff5c686b7 — continuity evidence only, disposition USE, not authorization; established/rejected/unknown/do_not_assume carried forward and explicitly superseded where Director mandates

## 1. Question
On WebChoreArena 532 tedious/memory heterogeneous tasks (massive-memory/cross-site/long-horizon where human 50.2% vs GPT-5 48.3% gap shows compressible structure) plus WebArena-Verified Hard 192/36 Jaccard<0.30 disjoint L=8-14 holdout (1280x720 CDP AX>10 mean>15 std>5 DOM>=2000, deterministic random.Random(35725763380), whole-trajectory holdout) plus Hard258 shared manifest (total pooled >=10 families pairwise Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2), does honest residual-novelty verification economics with per-trajectory hard-reset integer sum counters (resolve+bind+verify+freshness+browser_steps no jitter/n*3200/f*6.0, |rho_shuffled|<0.20 centered |mean|<0.05 std<0.15, 5000 family-stratified bootstrap +5000 block-permutation+5000 global permutation, real TF-IDF TAU0.30 over train-A, controlled novelty 0/25/50/75/100% train-A/test-B trajectory-grouped holdout, calibrated UNKNOWN precision>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18 with freshness TN>=0.85) demonstrate rho_novelty>=0.60 lower>0.40 p<0.05 vs pooled |rho_length|<0.20 upper<0.25 and per-stratum |rho_length|<0.20 upper<0.30 and Pareto M_total_f10 saving>=25% lower>15% p<0.05 strict dominance vs cold and vs RAG k5 at f10/f100 (+-50% build sensitivity), testing pay-novelty-not-length where synthetic 36-family rho0.48 was validly falsified non-Pareto?

## 2. Hypothesis
**H1 PRIMARY (SUPERSEDE):** On heterogeneous WebChoreArena tedious/memory + WebArena-Verified Hard families (532 + 192/36 L=8-14 + Hard258, combined manifest >=10 families pairwise canonical bigram Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 at 1280x720 CDP AX>10 mean>15 std>5 DOM>=2000 per family, deterministic seed 35725763380, TRAIN-only vocab isolation 0 leakage, whole-trajectory holdout), SPIDER honest verification economics with executed per-trajectory hard-reset integer sum counters (TAU0.30 topology-gated + freshness TN>=0.85, softmax temp 0.15 + deterministic hashlib.sha256(task_id) jitter 0.02 UNKNOWN<0.80, correct-family-required exact key-set equality after alias resolution, counted build = actual offline vectors/index/SQLite ops frozen before outcomes) will demonstrate:

- (S1) rho_novelty (Spearman executed_honest_total_cost_TAU-gated vs residual_novelty_fraction) >=0.60 lower>0.40 block p<0.05
- (S2) decoupled pooled |rho_length|<0.20 upper<0.25 p>=0.05
- (S3) per-stratum |rho_length|<0.20 upper<0.30 for every novelty stratum and length-tertile (N>=30, per-family N>=3, coverage >=8/10 pooled>=40)
- (S4) calibrated UNKNOWN precision>=0.85 false<=0.10 ECE<=0.15 upper<=0.18 with freshness TN>=0.85
- (S5) Pareto M_total_SPIDER(f=10) <=0.75*M_total_COLD saving>=25% lower>15% p<0.05 strict vs cold and vs flat RAG k5 at f10 and f100 robust +-50% build
- (S6) honest gap rho_novelty-|rho_shuffled|>0.35, |rho_proxy|<0.60, global |rho_shuffled|<0.20 centered |mean|<0.05 std<0.15

**H0:** If PCs/NCs PASS but any S1-S6 fails, pay-novelty-not-length is validly non-Pareto on heterogeneous WebChoreArena even where compressible structure exists (bounded heterogeneous falsification, supersedes synthetic rho 0.4837).

Agent priors in director_mandate.agent_priors_used are labeled priors, not SPIDER evidence.

## 3. State representation (pre-registered)
- **derived_context** = ONLY mechanism template strings + observed key sets canonical sorted after alias resolution + train-A registry, BrowserGym 1280x720 CDP AX tree hash + DOM TreeWalker-compressed representation, HTTP mix via Playwright CDP and Runtime HS256 sticky Flask WAL stable-header/proxy_cache HIT counters, freshness TN>=0.85 gate from Graph C-FRESHNESS.
- MUST NOT contain residual_novelty_fraction, length_label, target_resource_id, expected_key_set.
- Alias/catalog/index TF-IDF fitted on train-A only; test-B trajectories trajectory-grouped holdout never indexed. Correctness = deterministic exact expected key-set equality canonicalized after alias resolution, TAU+freshness-gated.

## 4. Action representation
- **resolve** = TF-IDF cosine candidate scoring over train-A mechanisms (real TAU0.30 topology gate)
- **bind** = slot extraction via catalog lookup on derived_context observed_keys (count novel slots only for candidates passing TAU0.30, >=3 demos per family, field-path relevant body/headers/url)
- **verify+freshness** = execution per candidate only if TAU>=0.30, including freshness gate TN>=0.85
- **browser_steps** = BrowserGym Playwright CDP steps only where navigation triggered, counted per-trajectory hard-reset
- UNKNOWN gate from softmax temp 0.15 + deterministic hashlib.sha256(task_id) jitter 0.02, threshold UNKNOWN<0.80

## 5. Target (dependent variables)
Primary: Spearman rho_novelty (honest total cost vs residual_novelty_fraction, TAU+freshness-gated). Secondary: pooled/per-stratum rho_length, UNKNOWN precision/false_accept/ECE (5 adaptive bins), M_total(f)=build+f*mean_per_task at f=10/100, gap and shuffled proxies.

## 6. Sampling policy
- Intel manifest: WebChoreArena 532 + Hard258 + WebArena-Verified Hard 192/36 L=8-14 disjoint, pooled >=10 families pairwise Jaccard<0.30 mean<0.15 product-subtree depth>=2, 1280x720 CDP AX>10 mean>15 std>5 DOM>=2000 per family raw N>=500 >=50/family, deterministic sampling random.Random(35725763380) + numpy RandomState(42) + hashlib.sha256 jitter shards.
- Controlled novelty 0/25/50/75/100% via family-resource holdout + WebChoreArena massive-memory stratification, crossed with length tertiles.
- Runtime health-gated sticky HS256 Flask + nginx WAL at /tmp/spider-runtime/shared.db, n_non304>=360 single-node else >=800 distributed stratified >=80/family X-Worker-Pid>=10 If-None-Match/304 proxy_cache HIT, per-trajectory hard-reset integer counters.

## 7. Unit of analysis
Trajectory = one task execution (one WebChoreArena/WebArena-Verified task with 0/25/…100% novelty label). Family = task family (eTLD+1 anchored product subtree). All CIs/perm resampling unit = trajectory, stratified/blocked by family. Block permutation block=family unit=trajectory.

## 8. Holdout & leakage controls
- Trajectory-grouped whole-trajectory holdout: catalog/index/freshness gates fit train-A families only; test-B families/trajectories never indexed. Includes L=8-14 disjoint for 192/36.
- TRAIN-only vocab isolation verified 0 leakage; audit verifies 0 forbidden reads of test-B resource id or residual_novelty_fraction via static harness inspection of derived_context keys.
- AX>10 ensures non-degenerate observation.

## 9. Baselines & controls
**Baselines (frozen, paired per-trajectory holdout):**
- B-COLD-LLM: cold LLM no inheritance, build 0
- B-FLAT-RAG-K5: flat TF-IDF k=5 over train-A only, TAU0.30 gated, correct-family-required single adoption, softmax 0.15+jitter UNKNOWN<0.80, honest gated cost + embedding counter
- B-SPIDER-RESIDUAL (PRIMARY): SPIDER parameterized inheritance honest gated counters topology-gated as above, build = offline vector/index ops frozen before outcomes
- B-RANDOM-GATE: same plumbing but random ranking/threshold, calibrates chance
- BINDING-RULE for all: identical acceptance predicate (exact key-set equality canonicalized), same softmax/jitter/UNKNOWN gate (except COLD always attempts), same verify+freshness TAU0.30+freshness TN>=0.85, same per-trajectory hard-reset counters, same 5000 bootstrap/block/global, honest build vs UNKNOWN, coverage >=8/10 pooled>=40 per-family per-stratum N>=3 else N/A, no n*3200/f*6.0/jitter in total

**Positive controls (all must PASS else MEASUREMENT_INVALID):**
- PC-HONEST-COST-SANITY: diff 0 TAU+freshness-gated, within-family std>0, zero_cells 0, gap>0.35 |rho_proxy|<0.60 |rho_shuffled|<0.20 centered, traces with per-op integers + TAU mask logged, forbidden-read 0
- PC-WEBCHORE-MANIFEST-ORTHOGONAL: >=10 families 532+192/36 L=8-14+Hard258 Jaccard<0.30 mean<0.15 depth>=2 1280x720 AX>10 DOM>=2000 raw >=500 >=50/family 0 leakage seed 35725763380
- PC-TRAIN-TEST-DISJOINT: 0 test-B resources/families in registry/index/DAG, 0 forbidden reads whole-trajectory holdout
- PC-CALIBRATION-DERIVED: confidence solely from actual TAU0.30+freshness softmax+jitter, std>0.05, imperfect accuracy 0.35-0.78 deterministic gated correctness
- PC-NOVELTY-MONOTONICITY: mean cost 100% >0% block p<0.05 d>0.8
- PC-BUILD-COST-ISOLATED: auditable offline ops frozen before outcomes
- PC-BROWSERGYM-SUBSTRATE: n_non304>=360 single-node else >=800 distributed X-Worker-Pid>=10 If-None-Match/304 HIT AX>10 or diagnostic MEASUREMENT_INVALID
- PC-FRESHNESS-GATED-BAILOUT: freshness TN>=0.85 >=30 stale probes, bailout to UNKNOWN correctly, ECE upper and false_accept gated

**Null controls (all must PASS else MEASUREMENT_INVALID):**
- NC-EMPTY-REGISTRY: N=6 empty registry -> UNKNOWN 100% precision 1.0 below TAU0.30
- NC-NO-APPLICABLE: N=12 OOD no covering family, every pipeline UNKNOWN precision>=0.85 false<=0.15 TAU+freshness, gated reduction >=0.20 vs ungated
- NC-ORACLE-LEAK: derived_context allowed keys only URL/method/url_path/url_query/headers_observed/body_observed + templates + AX hash + freshness contracts; must not contain residual_novelty_fraction/target_resource_id/length_label/expected_key_set, read count 0 trajectory-grouped
- NC-BIJECTIVE-COST: honest cost not bijective with n*3200 nor f*6.0 nor TAU candidate-count proxy, gap>0.35 |rho_proxy|<0.60 gated
- NC-SHUFFLED-NULL: global stratified permutation unit=trajectory family-stratified 5000 perms |rho_shuffled|<0.20 p>=0.20 centered |mean|<0.05 std<0.15; primary S1/S2 p-values use separate 5000 family-block permutation block=family
- NC-GUARD-SPECIFICITY: shuffled guard+freshness ablation N>=12 precision drop>=30% vs real

Any PC/NC failure => MEASUREMENT_INVALID (validity gate, not negative result). Do not substitute synthetic Jaccard 0.0 disjoint fixture if heterogeneous manifest unavailable.

## 10. Primary metric & expected direction
Primary survival: rho_novelty >=0.60 lower>0.40 p<0.05 favors novelty-monotonic cost; pooled/per-stratum |rho_length|<0.20 favors decoupling; calibrated UNKNOWN and Pareto saving>=25% favor honest economics.

## 11. Uncertainty method
- 5000 family-stratified trajectory-grouped bootstrap (resample trajectories stratified by family) for all CIs (rho, ECE, precision, M_total, saving)
- 5000 family-block permutation (block=family unit=trajectory) for primary p-values S1/S2/S3
- 5000 global stratified permutation (unit=trajectory family-stratified) for NC-SHUFFLED-NULL centering
- All TAU+freshness-gated, deterministic hashlib.sha256 shards, 95% CIs.

## 12. Adequacy rule
- Pooled >=40 tasks, per-stratum N>=30 post TAU+freshness else N/A (not PASS), per-family per-stratum N>=3 coverage >=8/10 families, mixed/cross-site >=10, calibration >=30 pooled imperfect accuracy, freshness stale >=30, within-family std>0 zero_cells 0, TRAI- vocab 0 leakage, n_non304 >=360 single-node else >=800 else diagnostic MEASUREMENT_INVALID (not falsification).

## 13. Falsification / survival rule (frozen)
- MEASUREMENT_INVALID if any PC or NC fails (per thresholds above) — no SURVIVES/FALSIFIES inference, distinguishes infrastructure/validity failure from scientific negative.
- SURVIVES_CURRENT_TEST iff ALL PCs PASS && ALL NCs PASS && (S1 rho>=0.60 lower>0.40 p<0.05) && (S2 pooled |rho_length|<0.20 upper<0.25 p>=0.05) && (S3 per-stratum |rho_length|<0.20 upper<0.30 for every stratum with N>=30 per-family N>=3 pooled>=40 coverage>=8/10) && (S4 precision>=0.85 false<=0.10 ECE<=0.15 upper<=0.18 freshness TN>=0.85) && (S5 Pareto M_total_SPIDER(f10)<=0.75*M_total_COLD saving>=25% lower>15% p<0.05 && M_total_SPIDER<M_total_RAGk5 at f10 and f100 CI lower>0 strict && +-50% build sensitivity not inverting) && (S6 gap>0.35 |rho_proxy|<0.60 global |rho_shuffled|<0.20 centered |mean|<0.05 std<0.15) — all TAU+freshness-gated.
- FALSIFIED-IN-SETTING if PCs/NCs PASS but any S1-S6 fails (bounded heterogeneous falsification on WebChoreArena 532+Hard258+192/36 L=8-14 live gate; supersedes synthetic rho0.4837 but does not globally close residual-novelty).
- WebChoreArena heterogeneous gate is 532 tedious/memory + 192/36 L=8-14 + Hard258 pooled >=10 families; synthetic 36-family Jaccard 0.0 disjoint fixture must NOT be substituted as heterogeneous evidence per frozen measurement_validity[0] BINDING-RULE.

## 14. Validity threats & representation loss
- **Jitter/n*3200/f*6.0 bijective proxy:** guarded by NC-BIJECTIVE-COST gap>0.35 and PC-HONEST-COST-SANITY; honest integer sum reset counters with TAU mask, no injected jitter besides deterministic 0.02 UNKNOWN jitter.
- **Header 0.0 variance / Jaccard orthogonality:** mitigated by Jaccard<0.30 mean<0.15 gate on product-subtree anchored bigram, not header-only; diversity from WebChoreArena massive-memory/cross-site.
- **Ceiling CI [1.0,1.0] degeneracy:** avoided by requiring within-family std>0, zero_cells 0, derived std>0.05, imperfect accuracy 0.35-0.78.
- **Hash PMI 0 / constant response:** deterministic correctness from key-set equality, not hash PMI; constant-response check via |rho_shuffled| centering and PC-HONEST-COST-SANITY.
- **SHA instability from dynamic tokens:** deterministic hashlib.sha256(task_id) only, not Python hash(); freshness gate isolates dynamic freshness tokens.
- **Leakage via derived_context:** NC-ORACLE-LEAK forbidden-read audit 0, TRAIN-only vocab isolation, trajectory-grouped holdout, whole-trajectory holdout includes L=8-14 disjoint.
- **Small-N null bias |mean|<0.05:** 5000 global + 5000 block permutations centered check prevents Laplace/small-N artifact.
- **Freshness miscalibration:** PC-FRESHNESS-GATED-BAILOUT TN>=0.85 stale>=30 ensures bailout to UNKNOWN discriminates, not tautological.
- **Build cost gaming:** PC-BUILD-COST-ISOLATED requires auditable offline ops frozen before outcomes, honest vs calibrated tradeoff, +-50% sensitivity.

## 15. Product consequences
- **Positive (SURVIVES with all PCs/NCs PASS):** First valid heterogeneous-gate evidence breaking 21/40=0.525 alias ceiling and synthetic TAU0.30 non-Pareto rho0.4837; residual-novelty economics validated pay-novelty-not-length where compressible structure exists (human 50.2% vs GPT-5 48.3% unsaturated). Authorizes next cross-site holdout replication with true website/family holdout + measured LLM tokens/latency/browser work (Runtime n>=800 distributed) and Intel larger manifest (WebGym 292k 50 eTLD+1) before PRODUCT_CORE; C-RESIDUAL-NOVELTY HYPOTHESIS->EXPERIMENTAL heterogeneous-gate-passed.
- **Negative (FALSIFIED-IN-SETTING with PCs/NCs PASS):** Honest economics remains length-coupled/miscalibrated/non-Pareto even on heterogeneous L=8-14 where structure exists; supersedes synthetic falsification with valid heterogeneous negative, preserves alias 21/40 as frontier ceiling. Per Director comparative_reasoning (cognitive_reset true, PIVOT, 4x MEASUREMENT_INVALID compilation), PARK frontier C-RESIDUAL-NOVELTY verification economics and pivot to orthogonal basins (barrier-physics in Physics lane, per-value alias via Runtime diverse substrate, production SPA substrates) rather than 18th alias permutation.

## 16. Estimated cost
~1710-2490 gated calls (570-830 per pipeline *3 pipelines) + <5s build, <90s permutations, BrowserGym 1280x720 capture ~15-30 min if substrate present else 0.06s diagnostic MEASUREMENT_INVALID, <100 MB artifacts hashed, <$2 compute, /tmp <800 MB, <45 min wall-clock; if Runtime single-node missing diagnostic <5 min CPU-only. No outcome-bearing measurements run in DESIGN.

## 17. Expected information gain
Very high as Director-mandated PIVOT with cognitive_reset true SUPERSEDE: continues the pay-novelty-not-length hypothesis to orthogonal heterogeneous basin where earlier JIT 10.4x prior suggests leverage but SPIDER synthetic evidence bounded non-Pareto; versus single JIT-compilation bakeoff (presumes novelty economics holds), versus continuing synthetic alias TAU0.30 tuning (VOI~0, routing gain 0.0 p=1.0), versus PARKing Frontier (wastes IDLE reactivation while 532+Hard258+192/36 L=8-14 manifest now available). Minimal discriminating test before Runtime distributed n>=800 or per-value alias; SURVIVES validates work-compression product leverage, FALSIFIED cleanly parks residual-novelty and forces orthogonal pivot — either outcome with valid controls is decision-relevant irrespective of sign and addresses prior traps (hash/Laplace/null bias, bijective gap, TAU+freshness gating, calibrated UNKNOWN).

## 18. Inherited state preservation (parent_handoff ef479f0)
- **Established (carry forward, not overwritten by MEASUREMENT_INVALID):** alias catalog+routing+hierarchical xMemory bounded 21/40=0.525 Wilson [0.352,0.648] 0/10 mixed routing gain 0.0 p=1.0 (17-deep tunnel); synthetic 36-family TAU0.30 Jaccard 0.0 non-Pareto rho 0.4837 CI[0.410,0.552] ECE 0.216 bounded to synthetic gate (36042599040 PASS all 11 PCs/NCs); substrate diagnostic MEASUREMENT_INVALID audit PASS with live_available false preserved; frozen design integrity verified; heterogeneous residual-novelty shootout TAU+freshness remains UNTESTED (S1-S6 unevaluated)
- **Rejected (bounded only):** retrieval-diversity achieving heterogeneous Pareto NOT rejected by MEASUREMENT_INVALID; WebChoreArena heterogeneous economics NOT rejected; routing gain 0.0 bounded to alias ceiling not global; WebMCP/compilation bypass NOT rejected (substrate-gated)
- **Unknown (this experiment targets):** S1 rho>=0.60 lower>0.40, S2/S3 |rho|<0.20 decoupling, S4 calibration precision>=0.85 ECE<=0.15 freshness TN>=0.85, S5 Pareto saving>=25% vs cold/RAG f10/f100 +-50% build, S6 gap>0.35 centered, L=8-14 heterogeneity, Runtime health gate n_non304>=360/800
- **Do_not_assume:** synthetic Jaccard 0.0 != heterogeneous Jaccard 0.30-0.60; agent priors != SPIDER evidence; chromium present != BrowserGym available; cross-family key adoption invalid; centered permutation required; DOM hash tautology triggers MEASUREMENT_INVALID; do not retry with synthetic fixture as live evidence; barrier-physics belongs to Physics lane per comparative_reasoning

## 19. Code paths & determinism
Allowed roots: `research/harness`, `research/frontier` only. Seeds: `numpy.random.RandomState(42)`, `random.Random(35725763380)`, `hashlib.sha256` for jitter/sharding/permutation/TAU tie-breaking. Trajectory-grouped holdout, per-trajectory hard-reset integer counters (resolve+bind+verify+freshness+browser_steps), honest sum + freshness mask persisted with sha256.

## 20. References
- request.json: `research/experiments/EXP-FRONTIER-36100559236/request.json` (director_mandate PIVOT 36100194801, target C-RESIDUAL-NOVELTY)
- Parent handoff: `research/experiments/EXP-FRONTIER-36099072254/handoff.json` sha256 ef479f0...
- Prior ceilings: `research/experiments/EXP-FRONTIER-36042599040/audit.json` PASS synthetic rho0.4837, alias tunnel 21/40=0.525
- Lane charter: `research/lanes/registry.json` frontier must_continue_beyond_pre2 true
- Claim registry: `research/claims/registry.json` C-RESIDUAL-NOVELTY HYPOTHESIS
- Dependencies: `research/intel/diverse_site_manifest.json` (Intel), `research/runtime/state.json` WAL health gate, `substrates/browsergym` pins, `research/graph/state.json` freshness TN>=0.85

*No outcome data inspected. Spec frozen before execution per Research 2.0 transaction REQUEST->DESIGN->FREEZE->EXECUTE.*
