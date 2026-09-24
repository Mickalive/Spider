# EXP-FRONTIER-36049636798 preregistration — Frontier PIVOT to deterministic compilation bypass (C-RESIDUAL-NOVELTY)

**Lane:** frontier  
**Claim:** C-RESIDUAL-NOVELTY — Later-agent cost tracks residual novelty rather than full task length (work compression economics)  
**Director mandate:** PIVOT SUPERSEDE with cognitive_reset true (cycle 36049089810) — leave 17-deep alias-catalog/routing/WebMCP tunnel bounded at 21/40=0.525, valid non-Pareto under honest per-trajectory hard-reset sum counters on 36-family orthogonal Jaccard<0.30 fixture; test orthogonal compilation bypass with guard bailout as code-approval vs LLM-proposal leverage.  
**Inheritance:** Parent handoff EXP-FRONTIER-36046077922 MEASUREMENT_INVALID — established 21/40 ceiling and honest non-Pareto remain, history-conditioned PMI BC~0 unchanged, dependencies absent (BrowserGym missing, manifest 0 families, Runtime WAL absent). Preserved as established/rejected/unknown/do_not_assume per handoff carry_forward; parent next_question (barrier-physics PMI) is advisory and SUPERSEDED by Director target.

## 1. Question
After alias/routing bounded at pooled 21/40=0.525 with 0/10 mixed triple-channel (header+body+query+auth) and routing gain 0.0 p=1.0, and honest residual-novelty economics validly falsified non-Pareto vs cold and vs TF-IDF RAG k5 at f=10/100 on orthogonal TAU0.30 fixture (EXP-FRONTIER-36042599040 PASS), does deterministic compilation bypass (AgentJIT/TraceCompiler/COVENANT pattern: first-run BrowserGym 1280x720 trajectory -> TreeWalker 99% compression + stable locator ranking + deterministic JSON/Python DAG with speculative guards + bailout fallback to LLM, 0 tokens 0.09s on repeat, SQLite INSERT OR IGNORE canonical) versus alias catalog+routing+hierarchical xMemory achieve honest M_total_f10/f100 Pareto dominance (tokens+browser+latency vs accuracy, per-trajectory-reset sum counters, |rho_shuffled|<0.20, 5000 family-stratified bootstrap + 5000 block-permutation) and break mixed 0/10 to >=4/10 with pooled coverage>=0.60 on heterogeneous WebArena-Verified v2 / WebGym mixed triple-channel tasks with trajectory-grouped CIs?

## 2. Hypothesis (falsifiable)
H1: On heterogeneous mixed triple-channel tasks (WebArena-Verified v2 192/36 or WebGym 292k dedup manifest >=10 families pairwise bigram Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 at 1280x720 CDP AX>10, header+body+query+auth mixed triple tagged, deterministic seed 42, TRAIN-only vocabulary isolation, trajectory-grouped holdout), deterministic compilation bypass will achieve:
- honest M_total(f)=build+f*mean_per_task where build = actual TreeWalker+locator+DAG+SQLite INSERT OR IGNORE ops frozen before outcomes, per_task = sum(resolve+bind+verify+freshness+browser_steps) hard-reset integers + LLM tokens (0 on guard-pass) + wall latency, achieving saving>=25% vs cold at f=10 (lower>15% p<0.05) and strict dominance vs TF-IDF RAG k5 and vs alias at f=10 and f=100 (CI lower>0, +/-50% build sensitivity not inverting),
- mixed triple-channel >=4/10 (exact binomial) with pooled coverage>=0.60 Wilson lower>=0.45, exceeding alias pooled 0.525 gap>=0.07 p<0.05,
- latency Pareto hot-path guard-pass mean <200ms median <100ms 0 tokens vs LLM median >=3000ms, resolve+bind reduction >=40% vs alias,
- calibration false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18 and |rho_shuffled|<0.20 centered |mean|<0.05 std<0.15,
revealing code-approval + guard bailout compresses work where retrieval-diversity alone bounded.

H0 (bounded falsification): Even with compilation bypass, honest economics remains non-Pareto or ceiling not broken (<4/10 mixed or pooled <0.60 or calibration fails), indicating pay-novelty-not-length not achievable via compilation at this heterogeneity.

## 3. State representation
- **Observed state:** BrowserGym 1280x720 CDP accessible tree (Playwright CDP) + DOM TreeWalker-compressed representation (99% compression fidelity verified via round-trip postcondition equality) + HTTP triple-channel observation (headers_observed, body_observed canonical hash, url_path, url_query, auth presence). AX node count >10 required per page (mean>15 std>5 across manifest). Timestamped trajectory steps with action target locator tier.
- **Compiled state:** Deterministic JSON/Python DAG with stable locator ranking (tier: data-testid > role+name > text > XPath fallback), parameter slots inferred from varying values across >=3 demonstrations per family (field-path relevant only: body.*, headers.*, url.* excluding metadata), speculative guards (URL pattern regex, DOM precondition hash, auth-header presence), postcondition verification hash, SQLite canonical row (INSERT OR IGNORE, sha256 of DAG).
- **Forbidden representation:** Must NOT contain expected mixed triple values (header+body+query+auth ground truth), novelty_fraction, length_label, expected_key_set, target_resource_id. Derived_context = observed keys + template strings only. Audit via static harness inspection.
- **Loss disclosure:** TreeWalker discards style/computed layout/visual pixels; stable locator ranking discards volatile XPath positions; guard set limited to three predicates (not full permission lattice); Jaccard <0.30 manifest isolates factorization from natural 0.30-0.60 overlap — synthetic 36-family gap remains dominant threat but not conflated with live heterogeneity.

## 4. Action representation
- **Compilation actions:** TreeWalker compress, locator rank, DAG codegen (parameter slot extraction via field-path relevance), guard synthesis, SQLite compile, deterministic replay execution, guard evaluation per task, bailout fallback to LLM cold path on guard fail.
- **Baseline actions:** Alias catalog lookup + TF-IDF retrieval (cosine TAU0.30 gate), hierarchical xMemory routing, flat TF-IDF top-k=5, TERX naive replay.
- All actions logged as integer counters per trajectory (resolve = candidates scored/Tier rank ops, bind = slots bound, verify+freshness = guard/postcondition evaluations, browser_steps = CDP steps executed). LLM tokens counted via tokenizer, latency wall-clock.

## 5. Target
Primary targets:
- **Economics:** M_total(f)=build+f*mean_per_task at f=10 and f=100 (honest build vs cold, alias, RAGk5).
- **Coverage:** Pooled accuracy pooled_coverage = correct / pooled N with trajectory-grouped Wilson CI; mixed triple-channel subset accuracy mixed_accuracy = correct_mixed / 10+ with exact binomial.
- **Latency/Token Pareto:** mean/median latency and tokens per task honest counters vs accuracy frontier.
- **Calibration:** false_accept_rate, UNKNOWN rate/precision, ECE (5 adaptive bins).
Secondary: rho_novelty vs rho_length decoupling (|rho_shuffled|), guard bailout rate, resolve+bind reduction.

## 6. Sampling policy
Deterministic seed 42 via numpy.random.RandomState(42) and hashlib.sha256(task_id) for jitter/sharding/permutation — never Python hash(). Heterogeneous manifest sampling: deterministic family selection over WebGym 292k dedup (>=50 eTLD+1 candidate pool) or WebArena-Verified v2 192/36 with product-subtree anchoring depth>=2, pairwise Jaccard<0.30, AX>10 filter. Trajectory capture: BrowserGym 1280x720 CDP single-worker sticky, one trajectory per task per baseline paired design, per-trajectory hard reset. Family-stratified holdout: whole trajectories of train-A families indexed, test-B families never indexed for catalog/retrieval/compilation fit. No tuning on test-B. No outcome-bearing measurements during DESIGN.

## 7. Unit of analysis
Unit = trajectory (one task execution). Resampling unit = trajectory nested in family (block=family). Mixed triple-channel subset counted separately but drawn from same pooled unit. Cost counters summed per trajectory then aggregated via family-stratified bootstrap.

## 8. Holdout
Trajectory-grouped holdout: >=10 families total, train-A/test-B disjoint at family level (0 test-B families in train-A registry/catalog/compiled DAG). TF-IDF / alias catalog / compiled DAG fit train-A only; vocabulary isolation verified 0 leakage. Whole trajectories held out (not steps). Validation via manifest disjointness and static forbidden-read audit (0 test-B resource id, 0 expected triple reads). No site-identity leakage beyond family stratification labels.

## 9. Nulls / baselines
- **Nulls:** NC-EMPTY-COMPILE (empty registry 100% UNKNOWN), NC-NO-APPLICABLE-MIXED (OOD 12 tasks precision>=0.85), NC-ORACLE-LEAK (forbidden reads 0), NC-BIJECTIVE-COST (gap>0.35 |rho_proxy|<0.60), NC-SHUFFLED-NULL (|rho_shuffled|<0.20 p>=0.20 centered |mean|<0.05 std<0.15 global+block 5000), NC-GUARD-SPECIFICITY (shuffled guard drop>=30%). Strong trajectory-grouped permutation nulls isolate chance.
- **Baselines:** B-COLD-LLM (no inheritance), B-ALIAS-CATALOG-ROUTING (17-deep tunnel ceiling 0.525), B-FLAT-RAG-K5 (TF-IDF k5 TAU0.30), B-COMPILE-BYPASS (primary), B-TERX-REPLAY (naive deterministic replay ablation). All share identical verification predicate (exact mixed triple-channel equality), UNKNOWN<0.80 gate, softmax temp 0.15 jitter 0.02, honest per-trajectory counters topology+guard-gated.

## 10. Primary metric & expected direction
Primary for Pareto: M_total_f10 saving vs cold >=25% and strict dominance vs RAG/alias at f10 and f100 (compilation < others, lower>0). Expected direction if H1 true: compilation dominates (lower cost) despite one-time build amortization. Secondary primary for breakthrough: mixed_accuracy >=4/10 and pooled_coverage>=0.60 exceeding alias 0.525 gap>=0.07. Tertiary: false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 and |rho_shuffled|<0.20 centered. Positive direction = compilation lower cost, higher accuracy on mixed, lower latency/tokens with calibration.

## 11. Uncertainty method
Family-stratified bootstrap 5000 (resample trajectories within families, stratify by family) for all CIs (M_total saving, pooled coverage Wilson, ECE, rho). Family-block permutation 5000 (block=family unit=trajectory) for primary p-values (Pareto, gap, latency). Global trajectory-grouped permutation 5000 for NC-SHUFFLED-NULL centering. Wilson binomial for pooled/mixed coverage with trajectory-grouped bootstrap supplement. Bonferroni where multiple strata tested but primary gate uses single pooled comparison.

## 12. Adequacy rule
- Heterogeneity adequacy: manifest >=10 families pairwise Jaccard<0.30 mean<0.15 product-subtree anchored AX>10 else MEASUREMENT_INVALID.
- Coverage adequacy: pooled N >=40 across heterogeneous tasks, mixed subset N >=10 else underpowered MEASUREMENT_INVALID (not PASS).
- Calibration adequacy: pooled tasks for ECE N>=30 imperfect accuracy 0.35-0.78 not degenerate.
- Cost adequacy: per-family per-cell std>0 naturally (else MEASUREMENT_INVALID), 0 forbidden reads.
- Substrate adequacy: BrowserGym 1280x720 CDP available and Runtime single-worker sticky n_non304 health-gated where required or diagnostic mode disclosed as MEASUREMENT_INVALID (no silent synthetic substitution). All adequacy declared before inference; underpowered => MEASUREMENT_INVALID with required_fixes, not negative result.

## 13. Falsification / survival rule (frozen decision_rule)
All thresholds on heterogeneous mixed triple-channel gate >=40 pooled (>=10 mixed) 1280x720 CDP trajectory-grouped holdout with honest per-trajectory counters + tokens + latency, 5000 bootstrap + 5000 block permutation + 5000 global.

- **SURVIVES_CURRENT_TEST** iff ALL PCs PASS AND ALL NCs PASS AND:
  S1: M_total_COMPILE(f=10) <=0.75*M_total_COLD (saving>=25% bootstrap lower>15% p<0.05) AND < M_total_ALIAS and < M_total_RAGk5 with dominance CI lower>0 at f=10 AND same strict dominance at f=100 with +/-50% build cost sensitivity not inverting;
  S2: compilation mixed >=4/10 and pooled_coverage>=0.60 Wilson lower>=0.45 and gap vs alias pooled 0.525 >=0.07 p<0.05;
  S3: hot-path guard-pass mean latency <200ms median <100ms 0 tokens vs alias/RAG median >=3000ms p<0.01, resolve+bind reduction >=40% vs alias;
  S4: UNKNOWN>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18 and global |rho_shuffled|<0.20 p>=0.20 centered |mean|<0.05 std<0.15 gap rho - |rho_shuffled|>0.35.

- **FALSIFIED-IN-SETTING** if PCs/NCs PASS but any S1-S4 fails (bounded falsification on heterogeneous mixed gate; compilation does not achieve honest Pareto or break 0/10->4/10).

- **MEASUREMENT_INVALID** if any PC/NC fails or manifest <10 families or pooled<40 or mixed<10 or n_non304 insufficient or BrowserGym/CDP missing or guard pipeline fidelity <90% or locator top-1 <95% — no inference to product; requires substrate repair (Intel WebGym 292k 50 eTLD+1 or WebArena-Verified v2, Runtime single-worker sticky health-gated n>=800, playwright browsergym-core display).

## 14. Positive / negative controls (summary)
PC-COMPILATION-PIPELINE: TreeWalker >=90% fidelity, locator top-1 >=95%, DAG exec succeeds, SQLite round-trip, guard <5ms bailout 100% on injection. PC-HONEST-COST-SANITY: diff 0 hard-reset, std>0, gap>0.35. PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST: Jaccard<0.30 AX>10 N>=500. PC-TRAIN-TEST-DISJOINT: 0 leakage forbidden reads. PC-CALIBRATION-DERIVED: std>0.05 imperfect accuracy. PC-BROWSERGYM-SUBSTRATE: n_non304 health gate or diagnostic flag. NC suite: EMPTY-COMPILE 100% UNKNOWN, NO-APPLICABLE precision>=0.85, ORACLE-LEAK 0, BIJECTIVE gap, SHUFFLED centered, GUARD-SPECIFICITY drop>=30%.

## 15. Validity threats & mitigations
- **Substrate missing (BrowserGym, manifest, Runtime WAL):** Mitigate by declaring live_available false diagnostic MEASUREMENT_INVALID with required_fixes; do not synthesize Jaccard 0.0 alphabets as live evidence. Prior synthetic ceiling disclosed.
- **Site-identity leakage / vocabulary leakage:** TRAIN-only vocab, whole-trajectory holdout, static audit, trajectory-grouped resampling.
- **Compilation tautology (action->own-request):** Guard specificity control (shuffled guard ablation) and bailout cost fully counted; postcondition equality not derived from action encoding.
- **Hash-state determinism vs true heterogeneity:** Heterogeneous WebArena/WebGym manifest with real sites, not locally-hosted Express SPA hash tautology.
- **Token/latency formula bias:** Actual tokenizer counters + wall clock, not n*3200/f*6.0; gap>0.35 vs proxy controls enforce honests.
- **Small-N mixed subset (10):** Exact binomial + Wilson, trajectory-grouped CI, require N>=10 else N/A.
- **Visual/layout loss:** TreeWalker discards style; disclose AX>10 compensates but visual representation not tested.

## 16. Product consequences
- **Positive (SURVIVES):** Validates orthogonal compilation bypass basin: code-approval + guard bailout beats retrieval diversity, breaking 0.525 ceiling and non-Pareto barrier. C-RESIDUAL-NOVELTY HYPOTHESIS -> EXPERIMENTAL on heterogeneous live gate (not VALIDATED/PRODUCT_CORE until cross-site holdout replication with same-model/same-budget LLM-inherit and distributed Runtime). Authorizes product promotion of SQLite canonical compile + postcondition guard + bailout to kernel (promotion_ready pending audit).
- **Negative (FALSIFIED-IN-SETTING with valid controls):** Bounded falsification: compilation also non-Pareto / not breaking mixed 0/10 on heterogeneous gate — pay-novelty-not-length non-Pareto even with code-approval leverage. PARK compilation alongside alias/RAG per Director comparative_reasoning; frontier should not run 19th compilation permutation, instead explore per-value alias via Runtime diverse substrate or leave barrier-physics to Physics lane pending Runtime gate.
- **Measurement invalid:** No product promotion; repair Intel manifest (WebGym 292k >=50 eTLD+1 or WebArena-Verified v2) and Runtime single-worker sticky health-gated n>=800 before retest.

## 17. Estimated cost & information gain
Cost: ~15-30 min BrowserGym capture for >=40 tasks + ~5 min alias/RAG replays + <60s bootstrap/permutation, <100 MB traces, <$2 compute; diagnostic invalid path 0.035s CPU-only if substrate missing. Gain: Very high — minimal discriminating test that can change claim/product decision per Director: either validates compilation as higher leverage than 17-deep alias diversity (justifying Runtime/Intel investment and architecture shift LLM proposes/code approves) or parks both retrieval and compilation as bounded non-Pareto (forcing orthogonal pivot, avoiding wasteful 18th alias permutation). Either outcome decision-relevant with valid controls.

## 18. Frozen thresholds (no post-hoc tuning)
- Pooled coverage>=0.60 Wilson lower>=0.45, mixed >=4/10 gap>=0.07 p<0.05
- Pareto saving>=25% lower>15% p<0.05 strict dominance vs RAG/alias at f10 and f100 lower>0 +/-50% build
- Latency mean <200ms median <100ms 0 tokens guard-pass vs LLM median >=3000ms
- Calibration UNKNOWN>=0.85 false<=0.10 ECE<=0.15 upper<=0.18
- |rho_shuffled|<0.20 p>=0.20 centered |mean|<0.05 std<0.15 gap>0.35
- TreeWalker fidelity >=90%, locator top-1 >=95%, guard <5ms
All frozen before observing outcomes; agent priors from director_mandate distinguished as priors not SPIDER evidence.

---
*Prereg hash will be frozen by deterministic freezer before EXECUTE. Any deviation after seeing outcomes is exploratory and requires new preregistration.*
