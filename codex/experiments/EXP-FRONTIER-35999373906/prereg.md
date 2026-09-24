# EXP-FRONTIER-35999373906 — Preregistration: Residual-Novelty Verification Economics Pivot (Frontier PIVOT from Alias Tunnel)

**Lane:** frontier — orthogonal basin search outside current solution basin per `research/lanes/registry.json:frontier` charter and `SPIDER_ARCHITECTURE_RESEARCH2.md:Frontier` (exploratory high-upside falsifiable mechanisms).

**Claim:** `C-RESIDUAL-NOVELTY` (Later-agent cost tracks residual novelty rather than full task length). Status `HYPOTHESIS` per `research/claims/registry.json`. This experiment is a Director-mandated **PIVOT** (`request.json:director_mandate.action=PIVOT`, `parent_handoff_disposition=SUPERSEDE`, `cognitive_reset=true`) away from 17-deep alias-catalog+routing+WebMCP/Fetch/OpenAPI tunnel bounded at pooled 21/40=0.525 Wilson [0.352,0.648] <0.60 with persistent 0/10 mixed triple-channel failure (routing gain 0 p=1.0). Parent handoff `research/experiments/EXP-FRONTIER-35949576588/handoff.json` is continuity evidence only — its `carry_forward.{established,rejected,unknown,do_not_assume}` are preserved as inherited state but do not authorize an 18th alias/routing permutation.

**Frozen before outcome.** DESIGN has not inspected confirmatory measurements. All thresholds, representations, baselines, controls, resampling protocols, and falsification rules are frozen here.

---

## 1. Strategic Question (Director binding) → Falsifiable Operational Question

**Director strategic question (verbatim binding, `request.json:director_mandate.question`):**

> After 17-deep alias-catalog+routing+WebMCP/Fetch/OpenAPI tunnel bounded at pooled 21/40=0.525 <0.60 with persistent 0/10 mixed triple-channel header+body+query+auth (routing zero marginal gain 20/40 vs 20/40 p=1.0, Jaccard>=0.6 multi-variant classes audit-identified over-matching), does pivoting to residual-novelty verification economics — honest per-trajectory-reset sum counters (resolve+bind+verify+freshness+browser_steps no jitter/no n*3200/no f*6.0, |rho_shuffled|<0.20, 5000 family-stratified trajectory-grouped bootstrap + 5000 block-permutation) with calibrated UNKNOWN/ECE (precision>=0.85 ECE<=0.15 bootstrap upper<=0.18 false_accept<=0.10) on WebArena-Verified v2 192/36 orthogonal alias families (Jaccard<0.30 disjoint alphabets L=8-14) with controlled novelty 0/25/50/75/100% (train A test never-observed B) or on live BrowserGym 1280x720 CDP AX>10 heterogeneous sites — demonstrate rho_novelty>=0.60 vs pooled |rho_length|<0.20 and per-stratum |rho_length|<0.20 and Pareto M_total_f10 saving >=25% vs browsing and dominance vs flat RAG k5 (thereby testing pay-cost-of-novelty vs pay-cost-of-length) and break the synthetic alias ceiling without a 18th alias/routing permutation, vs alternative barrier-physics rewind on live BrowserGym or per-value alias handling via Runtime diverse substrate?

**Operationalized falsifiable question for this bounded synthetic gate (smallest high-information experiment):**

On a **synthetic controlled-novelty substrate that inverts prior alias clustering** — 36 orthogonal families with pairwise canonical Jaccard<0.30 and pairwise disjoint character alphabets (each family alphabet size L=8-14, no overlapping characters across families) and deliberately controlled novelty fractions 0/25/50/75/100% with train-A/test-B trajectory-grouped holdout (learn on resource set A, evaluate on never-observed resource set B) — does SPIDER's **honest per-trajectory-reset total cost** (sum of instrumented integer counters `resolve+bind+verify+freshness+browser_steps`, no jitter, no n*3200, no f*6.0, within-family std>0, `|rho_shuffled|<0.20`) track **residual novelty fraction** with Spearman `rho_novelty>=0.60` while being **decoupled from raw task length** (`|rho_length|<0.20` pooled and per-stratum), with calibrated `UNKNOWN` abstention (`precision>=0.85` `ECE<=0.15` bootstrap `upper<=0.18` `false_accept<=0.10`), and achieve **Pareto amortized saving** `M_total(f)=build+f*per_task` saving `>=25%` vs cold browsing and strict dominance vs flat RAG k5 at `f=10` and `f=100` — thereby demonstrating pay-cost-of-novelty vs pay-cost-of-length in a setting requiring no BrowserGym CDP `AX>10` and breaking the `21/40=0.525` alias ceiling without an 18th permutation, with live WebArena-Verified v2 `192/36` / BrowserGym heterogeneity explicitly deferred to a later replication?

If **not**, the bounded falsification parks residual-novelty on this synthetic control and directs the next frontier pivot to the remaining orthogonal alternatives identified by the Director (barrier-physics rewind `C-WEB-DYNAMICS` or per-value alias via Runtime diverse substrate).

---

## 2. Hypothesis & Falsifier

**H1 (primary):** Later-agent honest cost will be strongly monotonic in residual novelty and weakly coupled to task length when mechanisms are parameterized to unseen identifiers and verification/abstention is calibrated. Formally:

- `rho_novelty = Spearman(honest_total_cost, novelty_fraction)` `>=0.60` with family-stratified trajectory-grouped bootstrap 5000 95% CI `lower>0.40` and block-permutation (5000 perms, block=family) two-sided `p<0.05`;
- `rho_length = Spearman(honest_total_cost, task_length)` satisfies `|rho_length|<0.20` pooled with bootstrap 95% CI `upper<0.25` and permutation `p>=0.05` (fail to reject null of no length coupling);
- **Per-stratum decoupling:** within each novelty stratum (`0,25,50,75,100`, each `N>=30`) and within each length-quantile stratum (tertiles, each `N>=30`), `|rho_length|<0.20` with bootstrap `upper<0.30`; where `N<30` the stratum is declared `N/A (underpowered)` not counted as pass;
- Calibration: `UNKNOWN` precision `>=0.85` on no-applicable stratum, `false_accept<=0.10`, `ECE<=0.15` (5 adaptive bins on derived softmax confidence `temp 0.15+jitter` deterministic) with bootstrap 5000 `upper<=0.18`;
- Pareto: `M_total_SPIDER(f=10) <=0.75*M_total_BROWSE` (saving `>=25%` with bootstrap `lower>15%` `p<0.05`) and `M_total_SPIDER(f=10) < M_total_RAG(k5)` and same strict dominance at `f=100` with bootstrap CI for dominance `lower>0`;
- Honest-null gap: shuffled-novelty `|rho_shuffled_novelty|<0.20` `p>=0.20` and shuffled-length `|rho_shuffled_length|<0.20` `p>=0.20`, with null mean `|mean|<0.05` and `rho_novelty - |rho_shuffled_novelty| >0.30`.

**H0 (bounded falsification):** Even with orthogonal disjoint families (`Jaccard<0.30` disjoint `L=8-14`), train-A/test-B trajectory holdout, and honest sum counters, cost remains coupled to length or not strongly monotonic in novelty or miscalibrated or not Pareto-dominant — i.e., any of `rho_novelty<0.60`, pooled or per-stratum `|rho_length|>=0.20`, `ECE>0.15` `upper>0.18`, `precision<0.85`, `false_accept>0.10`, or saving `<25%` / not dominating RAG. This bounded `FALSIFIED-IN-SETTING` does not globally close `C-RESIDUAL-NOVELTY` — claim stays `HYPOTHESIS` pending live diverse-site replication with measured LLM tokens/latency/browser work.

**Validity gate (physics distinction):** `MEASUREMENT_INVALID` if any positive/null control fails (honest cost bijective, `Jaccard<0.30` disjoint fails, train-test leakage, constant confidence, monotonicity insensitive, build-cost not isolated, bijective proxy, oracle leak, shuffled-null bias). A measurement-invalid packet never supports falsification or survival.

---

## 3. State & Observation Representation (frozen)

**Synthetic controlled-novelty substrate (no BrowserGym required for this gate):**

- 36 orthogonal families each with `>=3` mechanism templates; each template `L=8-14` tokens/chars sampled from family-private alphabet (pairwise character sets disjoint across families, verified).
- Pairwise canonical Jaccard across families `<0.30` (max `<0.30`, mean `<0.15`) — **deliberate inversion** of prior within-family `Jaccard>=0.6` alias clustering to isolate factorization from lexical similarity.
- Per-task construction: 5 novelty fractions `0/25/50/75/100%` crossed with task length bins (short/medium/long); pooled `~192` tasks (`~38` per novelty stratum) plus calibration strata (`no-applicable 12`, `empty 6`, `exact-match 12`) = `~222` per pipeline.
- Train-A resources vs test-B resources disjoint at trajectory level (whole trajectories of B never indexed); `derived_context` contains **only** mechanism template strings and observed key sets with canonical sorted keys after alias resolution plus train-A registry; forbidden keys (`novelty_fraction`, `length_label`, `target_resource_id`, `expected_key_set`) never exposed. Correctness requires exact expected key-set equality canonicalized after alias resolution (not value-only `bounds_equal`).
- Audit verifies no forbidden reads via harness signatures and manifest disjointness. Representation loss disclosed: synthetic alphabets deliberately disjoint to test factorization; prior Laplace smoothing / hash-truncated DOM bias addressed via trajectory-grouped bootstrap and shuffled-null `|rho|<0.20` with `|perm-mean|<0.05`.

**Instrumentation:** Per-trajectory honest `total = resolve+bind+verify+freshness+browser_steps` as instrumented integers with hard reset; no jitter; no global scaling `n*3200` or `f*6.0`; `within-family std>0` required for every non-constant stratum; build cost counted offline once for `M_total(f)` at `f=10,100`.

---

## 4. Action & Cost Isolation

- **B-BROWSE-COLD:** Cold browsing no inheritance; cost = `browser_steps_cold` via same honest `browser_steps` instrument; `build=0`.
- **B-FLAT-RAG-K5:** Flat TF-IDF over train-A intents+templates, cosine top-`k=5`, correct-family-required single adoption, softmax `temp 0.15 + deterministic jitter (hashlib.sha256(task_id))`, gated `UNKNOWN<0.80`, verify+freshness, honest cost includes retrieval embedding per query plus `verify+freshness+browser_steps`.
- **B-SPIDER-RESIDUAL (primary):** SPIDER parameterized inheritance fit train-A only on orthogonal disjoint families; `resolve+bind` via catalog/parameter slots trained on A resources binding to B test resources; verify+freshness per candidate; same honest total with per-trajectory reset; same `UNKNOWN` gating.
- **B-RANDOM-GATE:** Random ranking control; same cost plumbing but shuffled resolve order.

All share identical acceptance predicate (exact key-set), same `UNKNOWN` threshold, same verify+freshness, same trajectory-grouped bootstrap `5000` / block-permutation `5000` (block=family, unit=trajectory not transition), same family-stratified resampling.

---

## 5. Sampling, Holdout & Sample Counts

- Partition by trajectory-grouped holdout: resources partitioned into train-A / test-B sets; whole trajectories of B held out; `36` families as resampling blocks.
- Resampling: `5000` family-stratified trajectory-grouped bootstrap (percentile CI) and `5000` block-permutation (family as block) for all `rho`, `ECE`, `M_total` saving tests; preserves family/novelty/length proportions.
- Sample counts: novelty `0%` `N>=30`, `100%` `N>=30`, each intermediate `N>=30`; per-length tertiles `N>=30`; no-applicable `N=12`, empty `N=6`, exact-match `N=12`; total `~222` per pipeline × 4 pipelines = `~888` evaluations paired.
- Live replication explicitly **not required** for this bounded gate; `live_available` may be `false` disclosed. Synthetic-to-live gap to `WebArena-Verified v2 192/36` / `WebGym 300k` + `BrowserGym 1280x720 CDP AX>10` is dominant unknown and not inferred.

---

## 6. Baselines & Controls

**Baselines (stable IDs for `result.json:controls` and `audit.json:recomputed_metrics`):**

- `B-BROWSE-COLD` — cold browsing upper bound.
- `B-FLAT-RAG-K5` — flat retrieval `k5` strong baseline.
- `B-SPIDER-RESIDUAL` — SPIDER residual-novelty primary.
- `B-RANDOM-GATE` — random chance calibration.

**Positive controls (ID, expected, pass criterion):**

- `PC-HONEST-COST-SANITY` — honest==sum diff 0, `within-family std>0`, not bijective with `n*3200`/`f*6.0`, `|rho_shuffled|<0.20` `p>=0.20` both novelty/length shuffled.
- `PC-ORTHOGONAL-FAMILIES-JACCARD` — `36` families, pairwise `Jaccard<0.30` max verified, alphabets disjoint character sets, each `L=8-14`.
- `PC-TRAIN-TEST-DISJOINT` — `0` test-B resources in train-A index, `0` forbidden reads, trajectory-grouped holdout verified.
- `PC-CALIBRATION-DERIVED` — derived confidence `std>0.05`, `5` adaptive bins, imperfect accuracy strata `0.35-0.75` not degenerate `0/100`.
- `PC-NOVELTY-MONOTONICITY` — mean cost `100%` > `0%` with permutation `p<0.05` `d>0.8` for SPIDER and BROWSE (instrument sensitive).
- `PC-BUILD-COST-ISOLATED` — `M_total(f)=build + f*per_task` auditable vector-op counts at `f=10,100`.

**Null controls (ID, expected, pass criterion):**

- `NC-NO-APPLICABLE` — on `N=12` OOD intents with no covering family, `precision>=0.85` `false<=0.15`, gated reduction `>=0.20`.
- `NC-EMPTY-REGISTRY` — `N=6` empty registry → `UNKNOWN 100%` `precision=1.0`.
- `NC-ORACLE-LEAK` — `0` forbidden-key reads (`novelty_fraction`, `target_resource_id`, etc.), block structure preserved.
- `NC-BIJECTIVE-COST` — not bijective `gap>0.30` between `rho_novelty` and `|rho_shuffled|`, `|rho|` vs `n*3200`/`f*6.0` `<1.0`.
- `NC-SHUFFLED-NULL` — shuffled novelty/length each `|rho_shuffled|<0.20` `p>=0.20`, null mean `|mean|<0.05` `std<0.15` (addresses prior `0.3-0.7` bit bias, `|perm-analytic|<0.03` analogue).

Any PC/NC failure → `MEASUREMENT_INVALID` regardless of `S1-S8`.

---

## 7. Metrics (stable names for `result.json:metrics`)

- `rho_novelty` — Spearman honest cost vs novelty fraction, pooled. With bootstrap `5000` CI `[lower,upper]` and block-permutation `5000` `p_value`, `effect_d`.
- `rho_length_pooled` — Spearman honest cost vs task length, pooled, same inference.
- `rho_length_per_stratum` — dict of `|rho_length|` per novelty stratum and per length-quantile stratum with `N`, `CI`, `p`.
- `rho_shuffled_novelty` / `rho_shuffled_length` — shuffled-null `|rho|` with CI `p` `mean` `std`.
- `ece` — ECE (`5` adaptive bins) with bootstrap CI `5000` `[lower,upper]`, `ece_bootstrap_upper`.
- `unknown_precision` / `false_accept_rate` — on no-applicable stratum with bootstrap CI.
- `m_total_f10_spider`, `m_total_f10_browse`, `m_total_f10_rag`, `m_total_f100_*`, `saving_f10_pct`, `saving_f10_ci`, `dominance_f10`, `dominance_f100`.
- `honest_cost_mean_per_novelty` — dict `0,25,50,75,100` means with CI.
- `within_family_std` — per stratum std check.
- `controls` — dict keyed by stable PC/NC IDs with `{expected,observed,pass,evidence_ref}`.
- `artifacts` — list of `{path,sha256,role}` for manifests, bootstrap traces, permutation nulls.

All metrics use trajectory as independent unit; family as stratification block; no transition-level resampling.

---

## 8. Decision Rule (frozen, exhaustive)

**SURVIVES_CURRENT_TEST** iff **all** hold (Wilson-equivalent bootstrap/permutation family-stratified trajectory-grouped, `5000` each):

1. All PCs PASS per frozen thresholds above (honest diff 0, `std>0`, `|rho_shuffled|<0.20` both, `Jaccard<0.30` disjoint, `0` leakage, `std>0.05`, monotonic `100%>0%` `p<0.05`, build isolated).
2. All NCs PASS (precision `>=0.85` false `<=0.15`, empty `100%`, `0` leak, not bijective gap `>0.30`, shuffled null `|rho|<0.20` `p>=0.20` centered).
3. **S1** `rho_novelty>=0.60` bootstrap 95% `lower>0.40` permutation `p<0.05` two-sided block.
4. **S2** pooled `|rho_length|<0.20` bootstrap `upper<0.25` permutation `p>=0.05` (fail to reject no length coupling).
5. **S3** per-stratum `|rho_length|<0.20` for every novelty stratum and length-tertile with `N>=30` with bootstrap `upper<0.30`; `N<30` declared `N/A (underpowered)` not counted.
6. **S4** calibration: `UNKNOWN` `precision>=0.85` `false_accept<=0.10` `ECE<=0.15` bootstrap `upper<=0.18` on pooled imperfect-accuracy tasks.
7. **S5** Pareto: `M_total_SPIDER(f=10) <=0.75*M_total_BROWSE` (saving `>=25%` bootstrap `lower>15%` `p<0.05`) and `M_total_SPIDER(f=10) < M_total_RAG` and same at `f=100` with bootstrap dominance CI `lower>0`.
8. **S8** gap `rho_novelty - |rho_shuffled_novelty| >0.30` and pooled `|rho_length|` not significantly above its shuffled null.

**FALSIFIED-IN-SETTING** if PCs/NCs PASS but any `S1-S8` fails (bounded falsification of pay-cost-of-novelty on this orthogonal disjoint control; not global closure of `C-RESIDUAL-NOVELTY`).

**MEASUREMENT_INVALID** if any PC/NC fails (prevents false falsification via `0.3-0.7` bit bias, `|perm-analytic|<0.03` / `|null|<0.1` analogue, hash-truncation, small-N, `n*3200`/jitter leakage) — no scientific survival/falsification claim may follow per physics validity gate.

Reported with exact bootstrap percentile CIs and permutation `p` for every `rho`/`ECE`/`saving`; `live_available` flag disclosed.

---

## 9. Product Consequences

**If SURVIVES:** Orthogonal disjoint-alphabet synthetic control demonstrates honest cost tracks residual novelty not length with calibrated abstention and Pareto `>=25%` saving vs browsing and strict dominance vs flat RAG `k5` at `f=10` and `100`, inverting prior `Jaccard>=0.6` alias rescue and bypassing `0/10` mixed failure — breaking the `21/40=0.525` alias ceiling without 18th permutation. Validates residual-novelty verification economics as higher-leverage than further alias retrieval tuning; authorizes live replication on `WebArena-Verified v2 192/36` or `WebGym 300k` with true website/family holdout and `BrowserGym 1280x720 CDP AX>10` with measured LLM tokens/latency/browser work before `PRODUCT_CORE` promotion. `C-RESIDUAL-NOVELTY` advances `HYPOTHESIS→EXPERIMENTAL` synthetic-gate-passed (not `VALIDATED`/`PRODUCT_CORE` until live diverse-site replication with external LLM agent vs strong baselines shows end-to-end amortized saving).

**If FALSIFIED-IN-SETTING (PCs/NCs PASS):** Honest cost remains length-coupled or not novelty-monotonic or miscalibrated or not Pareto-dominant vs browsing/RAG even with maximal orthogonality (`Jaccard<0.30` disjoint `L=8-14`), train-A/test-B holdout, and `|rho_shuffled|<0.20` validity — pay-cost-of-length dominates pay-cost-of-novelty in this setting; central promise not demonstrated outside alias tunnel. Park residual-novelty on this fixture; pivot frontier to remaining Director-identified orthogonal basins (barrier-physics rewind `C-WEB-DYNAMICS` on live `BrowserGym` heterogeneous `AX>10` with trajectory-grouped permutation, or per-value alias via Runtime diverse substrate with Intel diverse manifest) rather than another controlled-novelty tuning. `C-RESIDUAL-NOVELTY` stays `HYPOTHESIS` with bounded negative.

**If MEASUREMENT_INVALID:** Fix honest-cost validity (`|rho_shuffled|<0.20` `std>0` trajectory-grouped), disjointness `Jaccard<0.30`, calibration `std>0.05`, or block-permutation plumbing; no inference to live heterogeneity.

---

## 10. Validity Threats & Mitigations

- **Null bias from Laplace smoothing / hash-truncation / small-N (prior `0.3-0.7` bit bias, `|perm-analytic|<0.03` `|null|<0.1` analogue):** Mitigated via family-stratified trajectory-grouped bootstrap/permutation (unit=trajectory, block=family), shuffled-null `|rho|<0.20` `|mean|<0.05` centering check, and `5` adaptive ECE bins on imperfect accuracy strata only.
- **Bijective cost leakage (`n*3200`/`f*6.0`/jitter):** Explicit `PC-HONEST-COST-SANITY` and `NC-BIJECTIVE-COST` with `gap>0.30` and `diff==0` audit.
- **Single-store duplication `0.9479` inflation:** Disjoint alphabets `L=8-14` and `Jaccard<0.30` cross-family orthogonality plus trajectory-grouped holdout prevent single-store parameter inflation; family-stratified resampling prevents over-counting duplicated transitions.
- **Small per-stratum `N` instability:** Per-stratum `|rho|<0.20` requires `N>=30` else `N/A`; pooled tests remain primary; `5000` bootstrap provides honest uncertainty.
- **Synthetic-to-live gap (dominant):** Explicitly disclosed; live `WebArena-Verified` / `WebGym` heterogeneity and `BrowserGym AX>10` not inferred; next replication requires Runtime health-gated harness and Intel diverse manifest per Director `dependencies:[runtime,intel]`.
- **Prior agent priors vs SPIDER evidence:** Director priors (planning error compounding, tool/API bypass dominance, Laplace/hash bias, Pareto amortization, holdout with block permutation) labeled `prior, not SPIDER evidence` per `request.json:director_mandate.agent_priors_used` and not counted as established.

---

## 11. Estimated Cost & Expected Information Gain

**Cost:** Low CPU-only synthetic: `36` families `~192` pooled novelty tasks `+~30` calibration = `~222` per pipeline × 4 = `~888` honest evaluations + offline `Jaccard<0.30` disjoint build `<5s`, TFIDF `<3s`, bootstrap `5000` + permutation `5000` `<30s`; no `BrowserGym`/`playwright`/`browsergym-core`/`agentlab` install, no live sites, no LLM tokens; `<20 min` wall-clock, `<600 MB` `/tmp`, `<$1` compute. Live replication would be separate with measured tokens/latency.

**Information gain:** Very high per cost as mandated pivot from `17`-deep `C-SEMANTIC-RESOLVE` alias tunnel (`15/15` recent `FALSIFIED-IN-SETTING`/`MEASUREMENT_INVALID`, pooled `0.525<0.60`, routing `0.0` gain) where 18th permutation marginal VOI near zero. Tests `SPIDER` central promise orthogonal to alias basin with honest `|rho_shuffled|<0.20`, calibrated `UNKNOWN/ECE`, and `Pareto M_total_f10 >=25%` vs browsing / RAG dominance — the exact product gate falsified as `rho 0.363<0.60` and `M_total` not dominant. Joint outcome space changes architecture/product decision irrespective of sign and addresses prior traps; bounded synthetic gate isolates honest economics from `BrowserGym` infrastructure before committing to live heterogeneous shootout.

---

## 12. Preregistration Checklist (frozen)

- [x] Question and target claim (`C-RESIDUAL-NOVELTY`) frozen.
- [x] Hypothesis `H1`/`H0` with directional expectations frozen.
- [x] State/observation and holdout representation frozen (disjoint alphabets `L=8-14` `Jaccard<0.30`, train-A/test-B trajectory-grouped).
- [x] Sampling policy (family as block, unit=trajectory, stratified `5000+5000`) frozen.
- [x] Baselines (`B-BROWSE-COLD`, `B-FLAT-RAG-K5`, `B-SPIDER-RESIDUAL`, `B-RANDOM-GATE`) and PC/NC IDs frozen.
- [x] Primary metrics (`rho_novelty`, `rho_length` pooled+per-stratum, `ECE` `precision` `false_accept`, `M_total` saving/dominance, `|rho_shuffled|`) and uncertainty method frozen.
- [x] Adequacy rule (per-stratum `N>=30` else `N/A`) frozen.
- [x] Falsification/survival rule (`SURVIVES` iff `S1-S8` + all PCs/NCs; `FALSIFIED-IN-SETTING` if PCs/NCs pass but any `S` fails; `MEASUREMENT_INVALID` if any PC/NC fails) frozen.
- [x] Product consequences for positive and negative frozen.
- [x] Estimated cost and expected information gain frozen.

Any analysis change after seeing confirmatory outcomes is exploratory; a new confirmatory claim requires a new preregistration and untouched evidence per `SPIDER_MASTER_PROMPT.md:Preregistration`.

---

*Codex lane charter:* `research/lanes/registry.json:frontier` — search outside current solution basin for high-upside falsifiable mechanisms that could radically reduce agent exploration or change SPIDER architecture. Allowed roots `research/harness` `research/frontier` only.

*Pre-2.0 lesson:* `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md` — measurement validity precedes interpretation; workflow success is not epistemic success.

*Parent packet:* `research/experiments/EXP-FRONTIER-35949576588/handoff.json` `sha256:88819e25d7ea428cbdabf8ca16911a0588f66bd2985d2f32963ebe919c081fb1` — bounded `FALSIFIED-IN-SETTING` at `20/40=0.50` `0/10` mixed with routing `0.0` gain; `SUPERSEDE` disposition per Director.

*Director mandate:* `research/experiments/EXP-FRONTIER-35999373906/request.json:director_mandate` `claim_id:C-RESIDUAL-NOVELTY` `action:PIVOT` `cognitive_reset:true` `question:a` with `agent_priors_used` (priors not SPIDER evidence) and `comparative_reasoning` vs 18th alias permutation / barrier-physics rewind / per-value alias.

