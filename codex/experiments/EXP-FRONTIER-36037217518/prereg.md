# EXP-FRONTIER-36037217518 — Preregistration: Residual-Novelty Verification Economics Honest Gate (REPAIR v3, Director CONTINUE — Executed-Counter Repair)

**Lane:** frontier — orthogonal basin search outside current solution basin per `research/lanes/registry.json:frontier` charter and `SPIDER_ARCHITECTURE_RESEARCH2.md:Frontier` (exploratory high-upside falsifiable mechanisms). Allowed roots `research/harness` `research/frontier` only.

**Claim:** `C-RESIDUAL-NOVELTY` (Later-agent cost tracks residual novelty rather than full task length). Status `HYPOTHESIS` per `research/claims/registry.json` (`HYPOTHESIS`, owner lanes graph/product). This experiment is a Director-mandated **CONTINUE** (`request.json:director_mandate.action=CONTINUE`, `parent_handoff_disposition=USE`, `cognitive_reset=false`, `claim_id=C-RESIDUAL-NOVELTY`) after two consecutive `MEASUREMENT_INVALID` on the same honest-gate (`EXP-FRONTIER-36018230359` 5 fixes, `EXP-FRONTIER-36033935647` 6 fixes with 3 CRITICAL). Parent handoff `research/experiments/EXP-FRONTIER-36033935647/handoff.json` (`sha256:8d1b35e3c7807a40d08aa07d862ae2a86236243c0ab2442e971e0c24ff12644e`) is continuity evidence — its `carry_forward.{established,rejected,unknown,do_not_assume}` are preserved as inherited state but do not override the Director's binding `CONTINUE` question and `SUPERSEDE/PIVOT` history.

**Frozen before outcome.** DESIGN has not inspected confirmatory measurements. All thresholds, representations, baselines, controls, resampling protocols, and falsification rules are frozen here per `SPIDER_MASTER_PROMPT.md:Preregistration` and `research/EXPERIMENT_PACKET.md` transmission invariants. No outcome-bearing measurement was run during DESIGN (read-only packet inspection only).

---

## 1. Strategic Question (Director binding) → Falsifiable Operational Question

**Director strategic question (verbatim binding, `request.json:director_mandate.question`):**

> After repairing harness to implement the frozen pipelines as executed mechanism operations (real resolve+bind+verify+freshness+browser_steps on derived_context with per-trajectory hard reset and per-family std>0, real TF-IDF retrieval over train-A with softmax temp 0.15+hashlib.sha256 jitter-derived confidence, counted build cost via actual vector-ops) and correcting within-family std, build-cost realism, and bijective-cost threshold, does honest cost track residual novelty rho_novelty>=0.60 (lower>0.40 p<0.05) vs pooled |rho_length|<0.20 (upper<0.25) and per-stratum |rho_length|<0.20 (upper<0.30 N>=30) with calibrated UNKNOWN precision>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18 and Pareto M_total_f10 saving>=25% vs cold browsing and strict dominance vs flat RAG k5 at f=10 and f=100 on the same 36-family Jaccard<0.30 disjoint L=8-14 synthetic gate — or if validly non-Pareto under QCR, does barrier-physics rewind on live BrowserGym 1280x720 CDP AX>10 heterogeneous sites reveal predictive structure beyond memory?

**Operationalized falsifiable question for this bounded synthetic gate (smallest high-information experiment):**

On a **synthetic controlled-novelty substrate** — 36 orthogonal families with pairwise canonical Jaccard<0.30 and pairwise disjoint character alphabets (each family alphabet size L=8-14, no overlapping characters across families, total alphabet 288-504 synthetic tokens) and deliberately controlled novelty fractions 0/25/50/75/100% with train-A/test-B trajectory-grouped holdout (learn on resource set A, evaluate on never-observed resource set B, catalog/index fit train-A only) — does SPIDER's **executed honest per-trajectory-reset total cost** (sum of instrumented integer counters `resolve+bind+verify+freshness+browser_steps` measured as executed operations on `derived_context` with hard reset, TF-IDF retrieval over train-A intents+templates with softmax temp 0.15 + deterministic `hashlib.sha256(task_id)` jitter range 0.02, UNKNOWN<0.80 gating, correctness deterministically from `correct-family-required` exact key-set equality after alias resolution, counted build cost = actual 108 mechanism vectors frozen before outcomes, no artificial std fixup, strengthened bijective threshold `gap>0.35 |rho_proxy|<0.60`) track **residual novelty fraction** with Spearman `rho_novelty>=0.60` while being **decoupled from raw task length** (`|rho_length|<0.20` pooled and per-stratum with bootstrap uppers) with calibrated `UNKNOWN` abstention (`precision>=0.85` `ECE<=0.15` bootstrap `upper<=0.18` `false_accept<=0.10`) and achieve **Pareto amortized saving** `M_total(f)=build+f*per_task` saving `>=25%` vs cold browsing and strict dominance vs flat RAG k5 at `f=10` and `f=100` — thereby testing pay-cost-of-novelty vs pay-cost-of-length with valid honest counters, with live `WebArena-Verified v2` / `BrowserGym` heterogeneity explicitly **deferred** to a later replication contingent on `SURVIVES` and with the `OR` clause barrier-physics rewind as a **deferred second-stage** only if this gate is validly `FALSIFIED-IN-SETTING` under QCR (not concurrent)?

---

## 2. Hypothesis & Falsifier

**H1 (primary):** Later-agent executed honest cost will be strongly monotonic in residual novelty and weakly coupled to task length when mechanisms are parameterized to unseen identifiers and verification/abstention is calibrated via executed operations. Formally:

- `rho_novelty = Spearman(executed_honest_total_cost, novelty_fraction)` `>=0.60` with family-stratified trajectory-grouped bootstrap 5000 95% CI `lower>0.40` and family-block permutation (5000 perms, block=family, unit=trajectory) two-sided `p<0.05`;
- `rho_length = Spearman(executed_honest_total_cost, task_length)` satisfies `|rho_length|<0.20` pooled with bootstrap 95% CI `upper<0.25` and block-permutation `p>=0.05` (fail to reject null of no length coupling);
- **Per-stratum decoupling:** within each novelty stratum (`0,25,50,75,100`, each `N=108`) and within each length-quantile stratum (tertiles, each `N>=180`), `|rho_length|<0.20` with bootstrap `upper<0.30`; requires `N>=30` overall and `per-family per-stratum N>=3` and family coverage `>=30/36` else stratum declared `N/A (underpowered)` not counted as pass (repairs degenerate ~1 task/family that invalidated `EXP-FRONTIER-36018230359` and the artificial `std` fixup that invalidated `EXP-FRONTIER-36033935647`);
- Calibration: `UNKNOWN` precision `>=0.85` on no-applicable stratum (N=12), `false_accept<=0.10`, `ECE<=0.15` (5 adaptive bins on derived softmax confidence `temp 0.15+jitter` deterministic via `hashlib.sha256` over actual TF-IDF scores) with bootstrap 5000 `upper<=0.18`; accuracy on pooled tasks must be imperfect `0.35-0.78` (not degenerate 0 or 1) to make ECE informative; correctness **deterministically** from retrieval outcome (exact key-set equality), not sampled `base_p`;
- Pareto: `M_total_SPIDER(f=10) <=0.75*M_total_BROWSE` (saving `>=25%` with bootstrap `lower>15%` `p<0.05`) and `M_total_SPIDER(f=10) < M_total_RAG(k5)` and same strict dominance at `f=100` with bootstrap CI for dominance `lower>0`; build cost is actual offline vector-ops (108 mechanism vectors frozen before outcomes, `$0.00002` placeholder for comparability, sensitivity `+/-50%` does not invert dominance);
- Honest-null gap: global-shuffled `|rho_shuffled_novelty|<0.20` `p>=0.20` centered `|mean|<0.05` `std<0.15` and shuffled-length `|rho_shuffled_length|<0.20` `p>=0.20`, with `rho_novelty - |rho_shuffled_novelty| >0.35` and strengthened bijective check `|rho_proxy|<0.60` (proxy = Spearman cost vs `n*3200` and vs `f*6.0`).

**H0 (bounded falsification):** Even with orthogonal disjoint families (`Jaccard<0.30` disjoint `L=8-14`), train-A/test-B trajectory holdout, and executed honest sum counters with per-trajectory hard reset, cost remains coupled to length or not strongly monotonic in novelty or miscalibrated or not Pareto-dominant — i.e., any of `rho_novelty<0.60`, pooled or per-stratum `|rho_length|>=0.20`, `ECE>0.15` `upper>0.18`, `precision<0.85`, `false_accept>0.10`, or saving `<25%` / not dominating RAG at f=10 or f=100. This bounded `FALSIFIED-IN-SETTING` does not globally close `C-RESIDUAL-NOVELTY` — claim stays `HYPOTHESIS` pending live diverse-site replication with measured LLM tokens/latency/browser work. It **does** trigger the deferred barrier-physics rewind as next orthogonal basin per Director `comparative_reasoning`, but that rewind is a **separate packet** contingent on QCR-valid non-Pareto, not measured here.

**Validity gate:** `MEASUREMENT_INVALID` if any positive/null control fails (executed `honest==sum` diff 0 with per-family `std>0` naturally `zero_cells==0` no fixup, bijective `gap>0.35 |rho_proxy|<0.60`, `Jaccard<0.30` disjoint, train-test leakage 0, derived confidence `std>0.05` imperfect accuracy `0.35-0.78`, monotonicity, build isolated auditable 108 ops, oracle leak 0, shuffled-null bias `|mean|>=0.05` or `|rho|>=0.20`, per-family coverage `<30/36` or per-family per-stratum `<3`). A measurement-invalid packet never supports falsification or survival per Physics validity gate. Prior packets `EXP-FRONTIER-36018230359` (`MEASUREMENT_INVALID` 5 required_fixes) and `EXP-FRONTIER-36033935647` (`MEASUREMENT_INVALID` 6 required_fixes, CORE tautology) are preserved; no inference from their tautological `rho 0.8998/0.8117` / `|rho|0.0391/0.0622` / `ECE 0.0185/0.0762` / `saving 34.53%/37.79%`.

---

## 3. State & Observation Representation (frozen)

**Synthetic controlled-novelty substrate (no BrowserGym required for this gate):**

- 36 orthogonal families each with `>=3` mechanism templates; each template `L=8-14` tokens sampled from family-private alphabet (pairwise character sets disjoint across families, verified, total alphabet 288-504 chars deliberately exceeding natural 26 to isolate factorization). This deliberately inverts prior within-family `Jaccard>=0.6` alias clustering.
- Pairwise canonical bigram Jaccard across families `<0.30` (max `<0.30`, mean `<0.15`) — verified via family manifest `artifacts/family_manifest.json` with sha256; catalog built train-A only.
- Per-task construction: 5 novelty fractions `0/25/50/75/100%` crossed with task length bins (short/medium/long); pooled `540` tasks (`108` per novelty stratum, `3` per family per stratum ensuring `per-family per-stratum N>=3`) plus calibration strata (`no-applicable 12`, `empty 6`, `exact-match 12`) = `570` per pipeline; trajectory-grouped holdout.
- Train-A resources vs test-B resources disjoint at trajectory level (whole trajectories of B never indexed, 15/15 split per family); `derived_context` for harness contains **only** mechanism template strings and observed key sets with canonical sorted keys after alias resolution plus train-A registry; forbidden keys (`novelty_fraction`, `length_label`, `target_resource_id`, `expected_key_set`, `alias_family`) never exposed. Correctness requires exact expected key-set equality canonicalized after alias resolution (deterministic, not value-only `bounds_equal`).
- Audit verifies no forbidden reads via harness code inspection `research/frontier/run_execute_36037217518.py` (must never import `novelty_fraction`) and manifest disjointness. Representation loss disclosed: synthetic alphabets deliberately disjoint to test factorization; prior Laplace/hash-truncated DOM bias addressed via trajectory-grouped resampling; realistic Jaccard `0.3-0.6` gap addressed as exploratory sensitivity (see §10).

**Instrumentation (executed, not formula — the core repair):**

- Per-trajectory honest `total = resolve+bind+verify+freshness+browser_steps` as **executed instrumented integers** with hard reset per trajectory; `resolve` = number of TF-IDF candidates scored (actual index lookup ops), `bind` = number of slots extracted/bound via catalog lookup on `derived_context` observed_keys (count of keys not in train-A catalog for that family, binding B test resources), `verify`/`freshness` = gate evaluations executed per candidate, `browser_steps` = steps actually executed to verify/bind (instrumented, derived from operations not `length*coeff`). No jitter added to total; no global scaling `n*3200` or `f*6.0`; `within-family std>0` required naturally per family/novelty cell (180 cells), not pooled; any zero-std cell (`zero_cells>0`) triggers `MEASUREMENT_INVALID` rather than silent increment (removes `run_execute_36033935647.py:395-407` fixup).
- Confidence derived **solely** from actual TF-IDF retrieval scores via softmax `temp 0.15 + deterministic jitter `hashlib.sha256(task_id)` range 0.02` (not hard-coded 0.85-0.95 ranges). Correctness derived **deterministically** from retrieval outcome: `correct` iff top-k retrieval contains the family whose key-set exactly equals observed canonical key-set; no `base_p = confidence*0.78+0.12` simulation.
- Build cost counted offline once as actual mechanism vectors `108` (36 families *3) frozen before outcomes for `M_total(f)` at `f=10,100`; `$0.00002/vector-op` is comparability placeholder; artifact logs actual ops count; sensitivity `+/-50%` reported.

---

## 4. Action & Cost Isolation

- **B-BROWSE-COLD (ID B-BROWSE-COLD):** Cold browsing no inheritance; cost = `browser_steps_cold` via same executed `browser_steps` instrument; `build=0`. Accepts always (no UNKNOWN). Executed steps scale with operations needed to browse blindly (still derived from `derived_context` length and catalog miss, but not hand-tuned `length*2.8 + novelty*12` guarantee).
- **B-FLAT-RAG-K5 (ID B-FLAT-RAG-K5):** Flat TF-IDF over train-A intents+templates ONLY, cosine top-`k=5`, correct-family-required single adoption, softmax `temp 0.15 + deterministic jitter (hashlib.sha256(task_id))` over actual scores, gated `UNKNOWN<0.80`, verify+freshness executed, honest cost includes per-query embedding counter (resolve) plus `verify+freshness+browser_steps`.
- **B-SPIDER-RESIDUAL (ID B-SPIDER-RESIDUAL, primary):** SPIDER parameterized inheritance fit train-A only on orthogonal disjoint families; `resolve+bind` via catalog/parameter slots trained on A resources binding to B test resources on `derived_context`; verify+freshness per candidate executed; same honest total with per-trajectory reset; same `UNKNOWN` gating; correctness deterministic; build cost offline vector-ops `108`.
- **B-RANDOM-GATE (ID B-RANDOM-GATE):** Random ranking control; same executed cost plumbing but shuffled resolve order via hash-seeded RNG.

All share identical acceptance predicate (exact key-set canonicalized), same `UNKNOWN` threshold `<0.80` (except BROWSE always attempts), same verify+freshness executed, same trajectory-grouped bootstrap `5000` / family-block permutation `5000` (block=family, unit=trajectory) plus global `5000` for NC centering, same family-stratified resampling. Build and per-query costs use same `$0.00002/vector-op` placeholder for comparability (live token/latency not modeled at this gate); secondary sensitivity discloses gap to measured economics.

---

## 5. Sampling, Holdout & Sample Counts

- Partition by trajectory-grouped holdout: resources partitioned into train-A / test-B sets (15 each per family); whole trajectories of B held out; `36` families as resampling blocks, `unit=trajectory` not transition.
- Resampling: `5000` family-stratified trajectory-grouped bootstrap (percentile CI) and `5000` family-block permutation (block=family) for primary `rho`/`ECE`/`M_total` tests plus `5000` global stratified permutation for `NC-SHUFFLED-NULL` centering (dual-permutation design to resolve prior `mean 0.1976>0.05` inconsistency). Both nulls reported.
- Sample counts: pooled `540` (36 families *5 novelty *3 per family per stratum =108 per novelty stratum); `no-applicable` `12`, `empty` `6`, `exact-match` `12`; total `570` per pipeline x4 = `2280` evaluations paired. Per-length tertiles each `N>=180`; novelty `0%`/`100%` each `108`; intermediate each `108`; per-family per-stratum `N=3` ensures within-family `std` estimable; family coverage `>=30/36` required else underpowered disclosure (`N/A` not PASS).
- Live replication explicitly **not required** for this bounded gate; `live_available` may be `false` disclosed as synthetic gate not `MEASUREMENT_INVALID`. Synthetic-to-live gap to `WebArena-Verified v2 192/36` / `WebGym 300k` + `BrowserGym 1280x720 CDP AX>10` is dominant unknown and not inferred.
- Determinism: Seeds `42` for all RNG via `numpy.random.RandomState(42)` and `hashlib.sha256` for jitter/sharding; not `hash()`; each task evaluated once per baseline paired design; `M_total` bootstrap resamples trajectories with family stratification; per-trajectory operation integers logged deterministically.

---

## 6. Baselines & Controls

**Baselines (stable IDs for `result.json:controls` and `audit.json:recomputed_metrics`):**

- `B-BROWSE-COLD` — cold browsing upper bound (no inheritance).
- `B-FLAT-RAG-K5` — flat TF-IDF retrieval `k5` strong baseline (fit train-A only).
- `B-SPIDER-RESIDUAL` — SPIDER residual-novelty primary (executed honest counters).
- `B-RANDOM-GATE` — random chance calibration.

**Positive controls (ID, expected, pass criterion — all must PASS else MEASUREMENT_INVALID):**

- `PC-HONEST-COST-SANITY` — executed `honest==sum` diff 0, `within-family std>0` per family/novelty cell naturally (180 cells `N>=3` each, `zero_cells==0`, no artificial increment), not bijective with `n*3200`/`f*6.0` (`gap>0.35` and `|rho_proxy|<0.60`), `|rho_shuffled|<0.20` `p>=0.20` `|mean|<0.05` `std<0.15` both novelty/length on global permutation, forbidden-read 0, operation trace logged. *Repairs prior tautology where audit found formula self-sum not instrumented and pooled std masked zero-std cells and `gap>0.30 |rho|<1.0` was weak.*
- `PC-ORTHOGONAL-FAMILIES-JACCARD` — `36` families, pairwise `Jaccard<0.30` max verified, alphabets pairwise disjoint char sets, each `L=8-14`, catalog built train-A only.
- `PC-TRAIN-TEST-DISJOINT` — `0` test-B resources in train-A index, `0` forbidden reads, trajectory-grouped holdout verified via code hash and static inspection that `novelty_fraction` never imported.
- `PC-CALIBRATION-DERIVED` — derived confidence `std>0.05`, `5` adaptive bins, imperfect accuracy `0.35-0.78` not degenerate `0/100`, confidence from actual TF-IDF softmax+jitter, correctness deterministic from retrieval outcome. *Repairs prior hard-coded 0.85-0.95/0.55-0.75 and `base_p` simulation.*
- `PC-NOVELTY-MONOTONICITY` — mean executed cost `100%` > `0%` with block-permutation `p<0.05` `d>0.8` for SPIDER and BROWSE (instrument sensitive).
- `PC-BUILD-COST-ISOLATED` — `M_total(f)=build + f*per_task` with auditable offline vector-op counts (108 vectors) at `f=10,100` frozen before outcomes, sensitivity `+/-50%` reported. *Repairs prior hand-chosen 30 ops that flipped Pareto sign (-8.2% with actual 108).*

**Null controls (ID, expected, pass criterion — any fail => MEASUREMENT_INVALID):**

- `NC-NO-APPLICABLE` — on `N=12` OOD intents with no covering family, `precision>=0.85` `false<=0.15`, gated reduction `>=0.20` vs ungated.
- `NC-EMPTY-REGISTRY` — `N=6` empty registry → `UNKNOWN 100%` `precision=1.0`.
- `NC-ORACLE-LEAK` — `0` forbidden-key reads (`novelty_fraction`, `target_resource_id`, `expected_key_set`, `length_label`), block structure preserved, catalog never reads B, static inspection passes.
- `NC-BIJECTIVE-COST` — not bijective: `gap rho_novelty - |rho_shuffled| >0.35` and `|rho_proxy|<0.60` for both `n*3200` and `f*6.0` proxies (strengthened from `gap>0.30 |rho|<1.0`).
- `NC-SHUFFLED-NULL` — **AMENDED**: global trajectory-grouped stratified permutation (5000) for shuffled novelty/length each `|rho_shuffled|<0.20` `p>=0.20`, null mean `|mean|<0.05` `std<0.15`; primary inference block-permutation (5000, block=family) used for S1/S2 p-values separately. *Amendment resolves prior family-block `mean 0.1976>0.05` caused by degenerate coverage; now requires `per-family per-stratum N>=3` and coverage `>=30/36`.*
- **Exploratory (non-gating)** realistic-Jaccard sensitivity: same pipelines on auxiliary `Jaccard 0.3-0.6` vocabularies (natural overlap) reported as disclosure to address audit `VF-005` without invalidating frozen disjoint gate; does not gate `SURVIVES/MEASUREMENT_INVALID`.

Any PC/NC failure → `MEASUREMENT_INVALID` regardless of `S1-S6`.

---

## 7. Metrics (stable names for `result.json:metrics`)

- `rho_novelty` — Spearman executed honest cost vs novelty fraction, pooled, with family-stratified bootstrap `5000` CI `[lower,upper]` and family-block permutation `5000` `p_value`, `effect_d`.
- `rho_length_pooled` — Spearman executed honest cost vs task length, pooled, same inference (block-permutation).
- `rho_length_per_stratum` — dict of `|rho_length|` per novelty stratum and per length-tertile stratum with `N`, `CI`, `p`, `upper` (requires N>=30 and per-family N>=3 else N/A).
- `rho_shuffled_novelty` / `rho_shuffled_length` — global-shuffled null `|rho|` with `CI` `p` `mean` `std` (5000 global) plus family-block counterparts for audit.
- `ece` — ECE (`5` adaptive bins) on derived confidence with bootstrap CI `5000` `[lower,upper]`, `ece_bootstrap_upper`, `conf_std`, `acc_pooled`.
- `unknown_precision` / `false_accept_rate` — on no-applicable stratum with bootstrap CI and gated-vs-ungated delta, plus `pooled_false`.
- `m_total_f10_spider`, `m_total_f10_browse`, `m_total_f10_rag`, `m_total_f100_*`, `saving_f10_pct`, `saving_f10_ci`, `saving_f100_pct`, `dominance_f10` (bool), `dominance_f100` (bool), `sensitivity_build_pm50` — each with bootstrap CI; build cost reported as ops count `108` and `$` placeholder.
- `honest_cost_mean_per_novelty` — dict `0,25,50,75,100` means with CI and monotonicity `p`/`d`.
- `within_family_std` — pooled `std`, per-family check (`within_ok` bool, `zero_cells` count must be 0).
- `max_jaccard` / `mean_jaccard` — family manifest orthogonality.
- `gap_rho_vs_shuffled` and `rho_proxy_*` — bijective checks.
- `controls` — dict keyed by stable PC/NC IDs with `{expected,observed,pass,evidence_ref}`.
- `artifacts` — list of `{path,sha256,role}` for family manifest (`role:fixture`), per-trajectory counter traces with per-op integers (`role:raw`), confidence values derived TF-IDF (`role:raw`), bootstrap/permutation nulls (`role:derived`), code path `research/frontier/run_execute_36037217518.py` (`role:code`), freeze hash.

All metrics use `trajectory` as independent unit; `family` as stratification block; no transition-level resampling. Within-family `std>0` naturally and `|rho_shuffled|<0.20 centered` are measurement validity, not outcome metrics.

---

## 8. Decision Rule (frozen, exhaustive)

**SURVIVES_CURRENT_TEST** iff **all** hold (family-stratified trajectory-grouped bootstrap `5000` + family-block permutation `5000` + global `5000` for NC, percentile CIs):

1. All PCs PASS per frozen thresholds (executed `diff==0`, per-family `std>0` naturally `zero_cells==0`, forbidden-read 0, global `|rho_shuffled|<0.20` both, `Jaccard<0.30` disjoint, `0` leakage trajectory-grouped, `std>0.05` imperfect accuracy `0.35-0.78` deterministic correctness, monotonic `100%>0%` `p<0.05` `d>0.8`, build isolated auditable 108 ops).
2. All NCs PASS per amended `NC-SHUFFLED-NULL` (precision `>=0.85` false `<=0.15` with gated reduction `>=0.20`, empty `100%`, `0` forbidden reads, not bijective `gap>0.35` and `|rho_proxy|<0.60`, global shuffled `|rho|<0.20` `p>=0.20` centered `|mean|<0.05` `std<0.15`).
3. **S1** `rho_novelty>=0.60` bootstrap 95% `lower>0.40` family-block permutation `p<0.05` two-sided.
4. **S2** pooled `|rho_length|<0.20` bootstrap `upper<0.25` family-block permutation `p>=0.05`.
5. **S3** per-stratum `|rho_length|<0.20` for every novelty stratum and length-tertile with `N>=30` (and per-family `N>=3`) with bootstrap `upper<0.30`; `N<30` or coverage `<30/36` or per-family `<3` declared `N/A (underpowered)` not counted.
6. **S4** calibration: `UNKNOWN` `precision>=0.85` `false_accept<=0.10` `ECE<=0.15` bootstrap `upper<=0.18` (`5` adaptive bins, derived confidence) on pooled imperfect-accuracy tasks.
7. **S5** Pareto: `M_total_SPIDER(f=10) <=0.75*M_total_BROWSE` (saving `>=25%` bootstrap `lower>15%` `p<0.05`) and `M_total_SPIDER(f=10) < M_total_RAG` and same at `f=100` with bootstrap dominance CI `lower>0` (strict) and `+/-50%` build-cost sensitivity does not invert dominance.
8. **S6** honest gap `rho_novelty - |rho_shuffled_novelty| >0.35` (global) and not bijective `|rho_proxy|<0.60` and pooled `|rho_length|` not significantly above its global-shuffled null.

**FALSIFIED-IN-SETTING** if PCs/NCs PASS but any `S1-S6` fails (bounded falsification of pay-cost-of-novelty on this orthogonal disjoint synthetic control with QCR; not global closure of `C-RESIDUAL-NOVELTY`; valid non-Pareto under QCR triggers authorized deferred barrier-physics rewind per Director `OR` clause as orthogonal second-stage, not concurrent with this packet).

**MEASUREMENT_INVALID** if any PC/NC fails (prevents false falsification via bijective `n*3200`/jitter/oracle leak/small-N/centering bias or artificial `std` fixup or simulated `base_p` per Physics validity gate) — no scientific survival/falsification claim may follow, regardless of `S1-S6`. Prior packet's `COMPLETE/SUPPORTS` with all PCs `true` was invalid due to tautological controls; this packet's `controls` must be code-verified executed operations with `zero_cells==0` naturally.

Reported with exact bootstrap percentile CIs and family-block permutation `p` for every `rho`/`ECE`/`saving`; plus global permutation `mean`/`std` for NC; `live_available` flag disclosed.

---

## 9. Product Consequences

**If SURVIVES with all PCs/NCs PASS (including strengthened `gap>0.35 |rho_proxy|<0.60 no fixup actual 108 ops`):** Orthogonal disjoint-alphabet synthetic control demonstrates executed honest cost tracks residual novelty not length with calibrated abstention and Pareto `>=25%` saving vs browsing and strict dominance vs flat RAG `k5` at `f=10` and `100`, inverting prior `Jaccard>=0.6` alias rescue and bypassing `0/10` mixed failure — breaking the `21/40=0.525` alias ceiling without 18th alias/routing permutation. This would be first valid synthetic-gate evidence that pay-cost-of-novelty is measurable honestly. Validates residual-novelty verification economics as higher-leverage than further alias retrieval diversity tuning on this controlled regime; authorizes live replication on `WebArena-Verified v2 192/36` or `WebGym 300k` with true website/family holdout and `BrowserGym 1280x720 CDP AX>10` with measured LLM tokens/latency/browser work (Runtime health-gated single-worker sticky required per `request.json:director_mandate.dependencies=[runtime,intel]`) and trajectory-grouped resampling before `PRODUCT_CORE` promotion. `C-RESIDUAL-NOVELTY` advances `HYPOTHESIS→EXPERIMENTAL` synthetic-gate-passed (not `VALIDATED`/`PRODUCT_CORE` until live diverse-site replication with external LLM agent vs strong baselines shows end-to-end amortized saving and cross-site transfer). Product should prioritize executed honest sum-counter + calibrated `UNKNOWN/ECE` verification and Pareto-aware compilation over further alias retrieval diversity tuning; realistic-Jaccard exploratory sensitivity informs live vocab design.

**If FALSIFIED-IN-SETTING with PCs/NCs PASS (validly non-Pareto under QCR):** Executed honest cost remains length-coupled or not novelty-monotonic or miscalibrated or not Pareto-dominant vs browsing/RAG even with maximal orthogonality (`Jaccard<0.30` disjoint `L=8-14`), train-A/test-B holdout, honest per-trajectory reset, and `|rho_shuffled|<0.20` validity — pay-cost-of-length dominates pay-cost-of-novelty in this setting; central promise not demonstrated outside alias tunnel. Park synthetic residual-novelty economics on this fixture; per Director `comparative_reasoning` and parent handoff `OR` clause, **PIVOT frontier to remaining orthogonal basins**: barrier-physics rewind `C-WEB-DYNAMICS` on live `BrowserGym` heterogeneous `AX>10` with trajectory-grouped permutation per `SPIDER_MASTER_PROMPT.md:Physics` validity gate (history-conditioned PMI beyond memory), or per-value alias handling via Runtime diverse substrate with Intel diverse manifest — rather than another controlled-novelty tuning. `C-RESIDUAL-NOVELTY` stays `HYPOTHESIS` with bounded negative on this fixture; 17-deep alias ceiling `21/40=0.525` remains frontier ceiling until Runtime northstar and Intel diverse manifest unblock live test. Barrier-physics rewind is then the dispatched next frontier packet, not inferred from this one.

**If MEASUREMENT_INVALID:** Fix executed-cost validity (`|rho_shuffled|<0.20` centered `|mean|<0.05` trajectory-grouped, per-family `std>0` naturally, forbidden-read 0, operation traces logged), disjointness `Jaccard<0.30`, calibration derived not simulated, bijective threshold, or block/global permutation plumbing before re-test; no inference to live heterogeneity. Do not cite prior packets' `rho 0.8998/0.8117`/`|rho|0.0391/0.0622`/`ECE 0.0185/0.0762`/`saving 34.53%/37.79%` as they were generator tautologies with hard-coded confidences, formulaic costs, artificial fixup, and constant build cost per audits.

---

## 10. Validity Threats & Mitigations

- **CORE tautology (`novelty_prop` formula) masquerading as honest cost:** Mitigated by requiring `honest total = sum(resolve+bind+verify+freshness+browser_steps)` where each counter is derived from actual TF-IDF retrieval and catalog lookup on `derived_context` observed_keys, not `novelty_fraction`. Static audit verifies `honest_pipeline_cost_and_retrieval` never reads `novelty_fraction`/`target_resource`; `PC-HONEST-COST-SANITY` checks `diff==0` and operation trace logging. Prior packet's `S1 rho 0.8117` was `novelty*coeff` formula; now code-verified sum over executed ops.
- **Artificial variance injection (prior 395-407):** Mitigated by design `per-family per-stratum N=3` (540 pooled) ensures natural variance; `zero_cells==0` required naturally, any zero-std cell forces `MEASUREMENT_INVALID` not silent `browser_steps+=1`. Audit checks `within_family_std.zero_cells`.
- **Simulated calibration (`base_p = confidence*0.78+0.12 - novelty*0.15`):** Eliminated. Correctness is deterministic retrieval outcome (exact key-set equality). ECE computed on derived confidence vs deterministic correctness, not sampled probability. `PC-CALIBRATION-DERIVED` requires `std>0.05` and imperfect accuracy `0.35-0.78`; low ECE must emerge from calibrated retrieval, not simulation.
- **Hand-tuned baselines and build cost flipping Pareto (prior `length*2.8`/`*0.6`/`*0.005` and `108/60/0` guarantee):** Build cost now actual counted ops `108` vectors frozen before outcomes; per-task costs are counts of executed ops, not hand-tuned coefficients. `PC-BUILD-COST-ISOLATED` requires auditable ops count and `+/-50%` sensitivity. If baselines remain formulaic, `PC-HONEST-COST-SANITY` bijective check (`|rho_proxy|<0.60 gap>0.35`) will fail.
- **Null bias from Laplace smoothing / hash-truncation / small-N:** Mitigated via family-stratified trajectory-grouped bootstrap/permutation (unit=trajectory, block=family), plus dual-permutation (global + block) with `|mean|<0.05` centering. Per-stratum now requires `N>=30` and `per-family N>=3`; prior degenerate `~1 task/family` repaired by `N=3` per family per stratum.
- **Single-store duplication and Jaccard>=0.6 over-matching:** Disjoint alphabets `L=8-14` and `Jaccard<0.30` cross-family orthogonality plus trajectory-grouped holdout prevent inflation; family-block permutation preserves structure.
- **Degenerate per-stratum N:** Per-stratum `|rho|<0.20` now requires `N>=30` and `coverage>=30/36` and `per-family per-stratum N>=3` else `N/A`; pooled tests remain primary; global permutation provides centered null even when family-block sparse.
- **Synthetic-to-live gap (dominant):** Explicitly disclosed as bounded synthetic gate; live `WebArena-Verified v2` / `WebGym 300k` heterogeneity and `BrowserGym AX>10` not inferred; next replication requires Runtime health-gated single-worker sticky harness and Intel diverse manifest per Director `dependencies`. Exploratory `Jaccard 0.3-0.6` sensitivity run reported as non-gating disclosure to address audit `VF-005` without weakening frozen gate.
- **Prior agent priors vs SPIDER evidence:** Director priors (path dependence, salience, composition via multi-step vs flat RAG `21/40=0.525 0/10`, calibrated `UNKNOWN` precision `>=0.85 ECE<=0.15`, harness bugs `wsgi/nginx/ETag`, `KV` recomputation) labeled `general prior, not SPIDER evidence` per `request.json:director_mandate.agent_priors_used` and not counted as `established`.

---

## 11. Estimated Cost & Expected Information Gain

**Cost:** Low CPU-only synthetic: `36` families `540` pooled +`30` calib `=570` per pipeline x4 pipelines `=2280` executed evaluations on `derived_context` + offline `Jaccard<0.30` disjoint build `<5s`, TFIDF fit train-A only (<108 docs) `<3s`, bootstrap `5000` + block-permutation `5000` + global `5000` `<60s`; no `BrowserGym`/`playwright`/`browsergym-core` install, no live sites, no LLM tokens; `<25 min` wall-clock, `<800 MB` `/tmp`, `<$1` compute. No large datasets committed. Live replication would be separate packet with measured tokens/latency/browser work (tail `OR` clause).

**Information gain:** Very high per cost as mandated **CONTINUE** after two `MEASUREMENT_INVALID` on the honest-gate blocking the central product promise `pay-cost-of-novelty`. Where 18th alias/routing permutation marginal VOI ~0 per information-gain rule (`17`-deep `C-SEMANTIC-RESOLVE` alias tunnel `15/15` recent `FALSIFIED-IN-SETTING`/`MEASUREMENT_INVALID`, pooled `0.525<0.60`, routing `0.0` gain), this repair directly addresses all 6 `required_fixes` blocking a valid measurement: honest executed counters vs formula, no artificial `std` fixup, deterministic correctness vs `base_p` simulation, actual 108 vector-ops build vs hand-tuned guarantee, strengthened bijective `gap>0.35 |rho_proxy|<0.60` vs weak `gap>0.30 |rho|<1.0`, and realistic-Jaccard exploratory sensitivity vs disjoint-only. Joint outcome space changes architecture/product decision irrespective of sign: **SURVIVES** validates verification economics and justifies investing Runtime northstar + Intel manifest in live `WebArena-Verified v2 192/36` / `WebGym 300k` health-gated BrowserGym replication; **FALSIFIED-IN-SETTING** with valid controls cleanly parks synthetic residual-novelty under QCR and forces authorized orthogonal pivot to barrier-physics rewind (`C-WEB-DYNAMICS` memory beyond history on live heterogeneous sites with trajectory-grouped permutation, history-conditioned PMI) or per-value alias via Runtime diverse substrate, avoiding another synthesis loop and informing Physics program cost. Addresses prior `MEASUREMENT_INVALID` root causes and the `|mean| 0.1976>0.05` protocol inconsistency before any live heterogeneity claim. Directly competes with external `O(1)` compile-and-execute IR (`$0.002-0.10`) and hierarchical caching `76.5%` baselines noted by Scout at equal cost under `C-PRODUCT-ECON`.

---

## 12. Preregistration Checklist (frozen)

- [x] Question and target claim (`C-RESIDUAL-NOVELTY`) frozen with Director mandate quote and operationalization including `OR` barrier-physics contingent.
- [x] Hypothesis `H1`/`H0` with directional expectations (`rho>=0.60` vs `|rho_length|<0.20`) frozen with executed-counter definition.
- [x] State/observation and holdout representation frozen (disjoint alphabets `L=8-14` `Jaccard<0.30`, train-A/test-B trajectory-grouped, executed pipelines on `derived_context` with per-family `N>=3` coverage `>=30/36`, deterministic correctness).
- [x] Sampling policy (family as block, unit=trajectory, stratified `5000+5000+5000` dual-permutation) frozen.
- [x] Baselines (`B-BROWSE-COLD`, `B-FLAT-RAG-K5`, `B-SPIDER-RESIDUAL`, `B-RANDOM-GATE`) and PC/NC stable IDs frozen with strengthened `PC-HONEST-COST-SANITY` (no fixup `zero_cells==0`), `NC-BIJECTIVE-COST` (`gap>0.35 |rho_proxy|<0.60`), `NC-SHUFFLED-NULL` dual, `PC-BUILD-COST-ISOLATED` actual 108 ops.
- [x] Primary metrics (`rho_novelty`, `rho_length` pooled+per-stratum, `ECE` `precision` `false_accept`, `M_total` saving/dominance, `|rho_shuffled|` gap, `rho_proxy`) and uncertainty method frozen.
- [x] Adequacy rule (`per-stratum N>=30` with per-family `N>=3` else `N/A`, coverage `>=30/36`) frozen.
- [x] Falsification/survival rule (`SURVIVES` iff `S1-S6` + all PCs/NCs with strengthened thresholds; `FALSIFIED-IN-SETTING` if PCs/NCs pass but any `S` fails with QCR; `MEASUREMENT_INVALID` if any PC/NC fails including zero-std fixup or simulated calibration) frozen with barrier-physics deferred clause.
- [x] Product consequences for positive (advance to `EXPERIMENTAL` synthetic-gate-passed, authorize live replication) and negative (park synthetic, pivot to barrier-physics per Director `comparative_reasoning` under QCR) frozen.
- [x] Estimated cost and expected information gain frozen.
- [x] Inherited parent handoff distinctions preserved (`established`/`rejected`/`unknown`/`do_not_assume` per `research/experiments/EXP-FRONTIER-36033935647/handoff.json` sha `8d1b35e3c7807a40d08aa07d862ae2a86236243c0ab2442e971e0c24ff12644e` and `EXP-FRONTIER-36018230359`) with `USE` disposition noted and Director `CONTINUE` binding respected (realistic-Jaccard as exploratory not frozen gate, per mandate `same 36-family Jaccard<0.30` gate).
- [x] Validity threats and mitigations including `6 required_fixes` (formula → executed, fixup removal, `base_p` → deterministic, hand-tuned build → actual 108 ops, weak bijective → `gap>0.35 |rho|<0.60`, disjoint-only → exploratory `0.3-0.6`) frozen.

Any analysis change after seeing confirmatory outcomes is exploratory; a new confirmatory claim requires a new preregistration and untouched evidence per `SPIDER_MASTER_PROMPT.md:Preregistration` and `research/EXPERIMENT_PACKET.md` transmission invariants. Barrier-physics rewind is not tested in this packet; it is authorized only upon valid `FALSIFIED-IN-SETTING` under QCR.

---

*Lane charter:* `research/lanes/registry.json:frontier` — search outside current solution basin for high-upside falsifiable mechanisms that could radically reduce agent exploration or change SPIDER architecture. Allowed roots `research/harness` `research/frontier` only.

*Pre-2.0 lesson:* `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md` — measurement validity precedes interpretation; workflow success is not epistemic success; 17-deep alias tunnel bounded `21/40=0.525`.

*Parent packet:* `research/experiments/EXP-FRONTIER-36033935647/handoff.json` `sha256:8d1b35e3c7807a40d08aa07d862ae2a86236243c0ab2442e971e0c24ff12644e` — `MEASUREMENT_INVALID` (6 required_fixes, CORE tautology `332-342`, fixup `395-407`, `base_p` `348-363`, hand-tuned `288/312/339`, build `624-631`, `max_jaccard 0.0`), `carry_forward` preserved above, Director `CONTINUE` `cognitive_reset:false` `USE`.

*Grandparent:* `research/experiments/EXP-FRONTIER-36018230359/handoff.json` `sha256:0558a366ec547a3059b18edd1e2d65344ba03ff48513d891c859dbc2a3f75b68` — `MEASUREMENT_INVALID` (5 required_fixes).

*Director mandate:* `research/experiments/EXP-FRONTIER-36037217518/request.json:director_mandate` `claim_id:C-RESIDUAL-NOVELTY` `action:CONTINUE` `cognitive_reset:false` `question: (see §1)` with `agent_priors_used` (priors not SPIDER evidence, distinguished in `do_not_assume`) and `comparative_reasoning` vs 18th alias permutation / barrier-physics rewind / per-value alias and `dependencies:[runtime,intel]` (synthetic gate independent; live replication dependencies deferred to SURVIVES stage).

*Codex:* `codex/claim_state.json` `C-RESIDUAL-NOVELTY` remains `HYPOTHESIS` (last valid sibling `EXP-INTEL-35999366789` `EXPERIMENTAL` synthetic work-unit `rho_real 0.8656 |rho_shuffled|0.1592` not extended by invalid parents; prior `EXP-FRONTIER-36033935647` did not advance claim per audit `claim_ceiling`).

