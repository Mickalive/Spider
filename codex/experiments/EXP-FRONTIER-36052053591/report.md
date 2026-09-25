# EXP-FRONTIER-36052053591 EXECUTE Report

**Lane:** frontier  
**Claim:** C-SEMANTIC-RESOLVE — Goals can be resolved to applicable mechanisms without internal ids (semantic resolution)  
**Director Mandate:** REOPEN with cognitive_reset true (cycle 36051627529) — PIVOT SUPERSEDE from 17-deep alias-catalog/routing/WebMCP tunnel to deterministic compilation bypass shootout  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE (infrastructure failure, not scientific falsification)  
**Elapsed:** 0.00095s diagnostic (0.035s-style per spec measurement_validity[0])  
**Timestamp:** 2026-09-24T20:06:50Z  
**Frozen Inputs Verified:** request.json 7d1b3531, spec.json 7c6dbabb, prereg.md e9550dec, freeze.json 75be8c5a — all match freeze.json hashes

## Frozen Design Summary

This experiment was a Director-mandated REOPEN with cognitive_reset=true after:
- 17-deep alias-catalog/routing/WebMCP tunnel bounded validly at **21/40 = 0.525** pooled Wilson [0.352,0.648], **0/10 mixed triple-channel**, routing gain **0.0 p=1.0**
- Honest residual-novelty economics validly **FALSIFIED non-Pareto** under QCR on 36-family orthogonal Jaccard<0.30 synthetic gate (EXP-FRONTIER-36042599040 **PASS** all 11 PCs/NCs, rho=0.4837 CI[0.4102,0.5523] <0.60, ECE 0.216>0.15, RAG dominance false at f10/f100, TAU0.30 topology gate)

The frozen hypothesis H1 (C-SEMANTIC-RESOLVE deterministic compilation bypass PIVOT SUPERSEDE): On heterogeneous mixed triple-channel tasks (WebArena-Verified v2 192/36 or WebGym 292k dedup manifest >=10 families pairwise bigram Jaccard<0.30 mean<0.15, product-subtree anchored depth>=2 at **1280x720 CDP AX>10 mean>15 std>5**, header+body+query+auth triple-channel tasks explicitly tagged, deterministic seed 42, TRAIN-only vocabulary isolation, trajectory-grouped holdout where whole trajectories of test families never indexed), deterministic compilation bypass — first-run BrowserGym 1280x720 CDP trajectory capture -> **TreeWalker 99% compression** + **stable locator ranking** (data-testid > role+name > text > XPath fallback) + deterministic JSON/Python DAG (parameter slots from >=3 demos per family, field-path relevant body/headers/url only) with **speculative guards** (URL pattern, DOM precondition hash, auth presence) and **bailout fallback** to LLM cold path on guard failure — will achieve semantic resolution without internal ids under correct-family gating (no cross-family key adoption, softmax temp 0.15 + deterministic hashlib.sha256(task_id) jitter 0.02 UNKNOWN<0.80, verify+freshness gates) AND honest end-to-end economics Pareto dominance versus cold LLM, alias catalog+routing+hierarchical xMemory (bounded 0.525), flat TF-IDF RAG k5, and WebMCP tool bypass (Fetch/OpenAPI+HATEOAS+routing normalization+invokeTool).

Specific frozen thresholds for **SURVIVES_CURRENT_TEST** (all required):
- **PCs PASS** (7) + **NCs PASS** (7) per thresholds
- **S1 Pareto:** M_total_COMPILE(f=10) saving>=25% vs cold (bootstrap 95% lower>15% p<0.05) AND strict dominance vs RAG k5 AND vs alias AND vs WebMCP at f=10 **and** f=100 with bootstrap dominance CI lower>0, +/-50% build sensitivity not inverting
- **S2 Mixed breakthrough:** compilation >=4/10 mixed (exact binomial Wilson lower, trajectory-grouped CI) with pooled >=0.60 Wilson lower>=0.45 AND gap vs alias 0.525 >=0.07 p<0.05 (and vs WebMCP >=0.07)
- **S3 Latency Pareto:** hot-path mean <200ms median <100ms 0 tokens on guard-pass vs alias/RAG/WebMCP/cold median >=3000ms, resolve+bind reduction >=40% vs alias
- **S4 Calibration:** UNKNOWN>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18 AND |rho_shuffled|<0.20 p>=0.20 centered |mean|<0.05 std<0.15 gap>0.35, guard specificity drop>=30%

FALSIFIED-IN-SETTING if PCs/NCs PASS but any S1-S4 fails (bounded falsification on heterogeneous mixed gate). MEASUREMENT_INVALID if any PC/NC fails or manifest <10 families or pooled<40 or mixed<10 or BrowserGym missing etc. — no inference to product.

## Substrate Diagnostic Results (RAW EVIDENCE)

| Substrate Component | Required | Available | Observed Details |
|---|---|---|---|
| BrowserGym (browsergym-core) | Yes | **NO** | `ModuleNotFoundError: No module named 'browsergym'` (tested `import browsergym` and `import browsergym.core`) |
| Playwright (CDP support) | Yes | **NO** | `ModuleNotFoundError: No module named 'playwright'` |
| WebGym 292k data | Yes | **NO** | Directory not found at `/home/runner/work/Spider/Spider/data/webgym_292k` |
| WebArena-Verified v2 data | Yes (alternative) | **NO** | Directory not found at `data/webarena_verified` |
| Intel diverse_site_manifest.json | Yes (>=10 families Jaccard<0.30 mean<0.15) | **NO** | File not found; glob `research/intel/*manifest*.json` -> 0 files; data/ directory does not exist |
| Runtime WAL (`/tmp/spider-runtime/shared.db`) | Yes (n_non304>=800 stratified) | **NO** | File not found |
| Heterogeneity adequacy (frozen) | >=10 families, Jaccard mean<0.15, max<0.30, AX>10 mean>15 std>5 | **FAIL** | 0 families, mean=None, max=None |
| Coverage adequacy (frozen) | Pooled>=40, Mixed>=10 | **FAIL** | pooled=0, mixed=0 |
| Live available (overall) | true for SURVIVES | **false** | false per `live_available` metric |
| WebMCP registry | Yes (>=95% OpenAPI fetch) | **NO** | Dependent on BrowserGym/CDP and manifest — not built |
| Honest counters / guard pipeline | Yes (per-trajectory hard-reset integers + tokens + latency) | **NO** | No trajectories captured, no guard eval <5ms |

**Evidence artifact:** `artifacts/substrate_diagnostic.json` sha256 `999091e631256d8fe2afe12df781b0bfbe0971bd6e217dc91af837c1e1224317` (raw diagnostic, timestamp 2026-09-24T20:06:50Z, elapsed 0.00095s).

Additional artifacts produced to preserve frozen pipeline intent without inventing data:
- `artifacts/compilation_pipeline_check.json` sha256 `291fbe9f5979d18a817cc7ba8868db11fb83976277620e46a8482af6bf674646` — TreeWalker/locator/DAG/SQLite/guard/WebMCP status NOT_RUN with reason
- `artifacts/per_trajectory_traces.json` sha256 `f8192d2a014b7bb33bbde48d7cb73011bcc682ad43f9af5583dfdf45bc21567c` — 0 trajectories, honest counters empty
- `artifacts/honest_cost_audit.json` sha256 `b604e67dbd8e25e75670d3db5a38d6dcd432fc0b2db625808fa9c4edfdd24307` — no counters to audit

## Controls Evaluation (Frozen Identifiers Preserved)

### Positive Controls (ALL must PASS for SURVIVES)

| Control | Status | Expected | Observed | Pass | Reason |
|---|---|---|---|---|---|
| PC-COMPILATION-PIPELINE | NOT_RUN | TreeWalker >=90% fidelity, locator top-1 >=95%, DAG exec succeeds, SQLite INSERT OR IGNORE round-trip, guard <5ms, bailout 100% on N>=6 injections | BrowserGym/CDP missing - no DOM to compress, no locator ranking, no DAG codegen | false | BrowserGym/CDP missing |
| PC-HONEST-COST-SANITY | NOT_RUN | honest==sum diff0 std>0 per family/novelty cell naturally TAU+guard-gated not bijective gap>0.35 \|rho_proxy\|<0.60 | No trajectories captured - no counters to audit | false | No trajectories captured |
| PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST | **FAIL** | >=10 families pairwise Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 1280x720 AX>10 mean>15 std>5 raw N>=500 | Manifest families=0 <10, Jaccard mean=None, no diverse_site_manifest.json, no WebGym 292k dir | false | Manifest families=0 <10 |
| PC-TRAIN-TEST-DISJOINT | NOT_RUN | 0 test-B families in train-A catalog/index/compiled DAG/WebMCP registry; 0 forbidden reads via static harness inspection; trajectory-grouped holdout | No train/test split without manifest and trajectories | false | No train/test split without manifest |
| PC-CALIBRATION-DERIVED | NOT_RUN | confidence derived solely from retrieval/compilation guard confidence, std>0.05 imperfect accuracy 0.35-0.78, 5 adaptive bins, TAU0.30 gate | No live data to compute calibration | false | No live data |
| PC-BROWSERGYM-SUBSTRATE | **FAIL** | BrowserGym 1280x720 CDP single-worker sticky AX>10 mean>15 std>5 n_non304 health-gated or diagnostic MEASUREMENT_INVALID | browsergym_available=False, playwright_available=False, browsergym_core_available=False | false | BrowserGym/Playwright missing |
| PC-WEBMCP-REGISTRY | NOT_RUN | OpenAPI fetch >=95% invokeTool exec succeeds, HATEOAS parsing, routing normalization, guard <5ms | No WebMCP registry built - depends on BrowserGym/CDP and manifest | false | Substrate missing |

**PC All Pass:** False (2 FAIL, 5 NOT_RUN)

### Null Controls (ALL must PASS for SURVIVES)

| Control | Status | Expected | Observed | Pass | Reason |
|---|---|---|---|---|---|
| NC-EMPTY-COMPILE | NOT_RUN | Empty compilation registry N=6 -> 100% UNKNOWN fallback precision 1.0 no false accepts | No compilation pipeline to test empty registry | false | No compilation pipeline |
| NC-WEBMCP-EMPTY | NOT_RUN | Empty WebMCP registry N=6 -> 100% UNKNOWN fallback precision 1.0 | No WebMCP registry to test empty case | false | No WebMCP registry |
| NC-NO-APPLICABLE-MIXED | NOT_RUN | On no-applicable stratum N=12 OOD mixed triple-channel intents, every pipeline UNKNOWN precision>=0.85 false<=0.15 gated reduction >=0.20 | No mixed triple-channel tasks to test | false | No mixed tasks |
| NC-ORACLE-LEAK | NOT_RUN | 0 forbidden-key reads of mixed triple expected values, novelty_fraction, length_label | No live data to audit | false | No live data to audit |
| NC-BIJECTIVE-COST | NOT_RUN | Executed honest cost not bijective gap>0.35 \|rho_proxy\|<0.60 for n*3200/f*6.0/TAU-count proxies | No honest counters executed | false | No honest counters |
| NC-SHUFFLED-NULL | NOT_RUN | \|rho_shuffled\|<0.20 p>=0.20 centered \|mean\|<0.05 std<0.15 global 5000 + block 5000 trajectory-grouped | No trajectories for permutation | false | No trajectories |
| NC-GUARD-SPECIFICITY | NOT_RUN | Random guard ablation N>=12 shows guard precision drop >=30% vs real guards for both compilation/WebMCP | No guard pipeline to ablate | false | No guard pipeline |

**NC All Pass:** False (all 7 NOT_RUN)

### Baselines (All NOT_RUN — no trajectories)

| Baseline | Status | Reason |
|---|---|---|
| B-COLD-LLM (no inheritance) | NOT_RUN | No trajectories - substrate missing |
| B-ALIAS-CATALOG-ROUTING (17-deep tunnel ceiling 0.525) | NOT_RUN | No trajectories - substrate missing |
| B-FLAT-RAG-K5 (TF-IDF k=5 TAU0.30) | NOT_RUN | No trajectories - substrate missing |
| B-WEBMCP-TOOL-BYPASS (Fetch/OpenAPI+HATEOAS+invokeTool) | NOT_RUN | No trajectories - substrate missing |
| B-COMPILE-BYPASS (primary: TreeWalker+locator+DAG+guards+bailout) | NOT_RUN | BrowserGym/CDP missing |
| B-TERX-REPLAY (naive deterministic replay ablation) | NOT_RUN | No trajectories - substrate missing |

## Survival Criteria (Frozen Decision Rule — Not Evaluable)

| Criterion | Required | Result |
|---|---|---|
| All PCs PASS | Yes | **FAIL** (0/7 PASS) |
| All NCs PASS | Yes | **FAIL** (0/7 PASS) |
| S1 Pareto: saving>=25% vs cold (lower>15% p<0.05) + strict dominance vs RAG/alias/WebMCP at f10 and f100 with CI lower>0, +/-50% build sensitivity not inverting | Yes | NOT_EVALUATED (no M_total computed) |
| S2 Mixed: >=4/10 mixed pooled>=0.60 Wilson lower>=0.45 gap>=0.07 vs alias/WebMCP | Yes | NOT_EVALUATED (0 tasks) |
| S3 Latency: hot-path mean<200ms median<100ms 0 tokens vs >=3000ms, resolve+bind >=40% reduction vs alias | Yes | NOT_EVALUATED (no guard-pass timings) |
| S4 Calibration: UNKNOWN>=0.85 false<=0.10 ECE<=0.15 upper<=0.18 \|rho_shuffled\|<0.20 gap>0.35 guard specificity drop>=30% | Yes | NOT_EVALUATED (no live data) |

**Decision:** Because PC/NC thresholds fail, frozen decision_rule mandates **MEASUREMENT_INVALID** (status MEASUREMENT_INVALID, outcome NOT_APPLICABLE) per:
> "MEASUREMENT_INVALID if any frozen positive or null control fails per thresholds below; this prevents scientific falsification/survival per validity gate and must be distinguished from negative result."
> "If BrowserGym/CDP or Intel diverse manifest unavailable or n_non304 stratified insufficient, declare live_available=false and MEASUREMENT_INVALID diagnostic (0.035s-style) without falsifying claim — do not substitute synthetic disjoint alphabets as live evidence."

This is **not** FALSIFIES for C-SEMANTIC-RESOLVE. The experiment provides no evidence for or against compilation bypass leverage; it preserves RAW EVIDENCE -> OBSERVATION chain without collapsing interpretation into observation.

## Metrics (Raw Diagnostic)

All metrics in `result.json` are diagnostic infrastructure metrics, not economic/coverage estimates:

- `live_available`: false
- `browsergym_available`: false
- `browsergym_core_available`: false
- `playwright_available`: false
- `manifest_families`: 0
- `manifest_jaccard_mean`: null (no manifest to compute)
- `manifest_jaccard_max`: null
- `runtime_wal_exists`: false
- `webmcp_registry_available`: false
- `heterogeneity_adequate`: false
- `coverage_adequate`: false
- `pooled_tasks`: 0 (required >=40)
- `mixed_tasks`: 0 (required >=10)
- `treewalker_fidelity`: null
- `locator_top1`: null
- `guard_eval_ms`: null
- `elapsed_seconds`: 0.00095

No bootstrap CIs computed (requires >=40 pooled trajectories for family-stratified bootstrap 5000 + block-permutation 5000 + global 5000). No M_total_f10/f100 Pareto, no mixed breakthrough, no latency, no calibration, no rho_shuffled.

## Prior Valid Evidence Preserved (Per Parent Handoff EXP-FRONTIER-36049636798 carry_forward.established)

1. **Alias-catalog/routing/WebMCP tunnel bounded** at 21/40 = 0.525 pooled Wilson [0.352,0.648], 0/10 mixed triple-channel, routing gain 0.0 p=1.0 on synthetic diverse substrate — remains valid bounded negative ceiling.
2. **Honest residual-novelty economics validly FALSIFIED non-Pareto** under QCR on 36-family orthogonal Jaccard<0.30 synthetic gate (EXP-FRONTIER-36042599040 audit PASS, all 11 PCs/NCs PASS, rho_novelty 0.4837 CI[0.4102,0.5523] <0.60 threshold, ECE 0.216 >0.15, RAG dominance false at f10/f100, TAU0.30 topology-gated). This is the correct comparator for honest counter methodology.
3. **Director mandate PIVOT SUPERSEDE with cognitive_reset true** remains binding after validly bounding alias tunnel and falsifying synthetic economics — this diagnostic does not invalidate the PIVOT direction to orthogonal compilation basin.
4. **C-SEMANTIC-RESOLVE remains HYPOTHESIS** per `codex/claim_state.json` (no VALIDATED/EXPERIMENTAL promotion without live heterogeneous gate).

No new establishment for C-SEMANTIC-RESOLVE beyond honest MEASUREMENT_INVALID handling. Claim ceiling unchanged.

## Validity Notes & Threats

- **Substrate missing is not hypothesis falsification:** Per frozen `measurement_validity[0]` and `decision_rule`, BrowserGym/CDP missing, Intel manifest absent (0 families), Runtime WAL absent, heterogeneity gate fails, coverage gate fails — all mandate MEASUREMENT_INVALID with required fixes, not product promotion or falsification. Audit must verify substrate absent via recomputation of artifact hashes.
- **No synthetic substitution:** Prior synthetic 36-family Jaccard 0.0 fixture (disjoint alphabets L 8-14) remains bounded negative evidence only. Per spec: "do not substitute synthetic disjoint alphabets as live evidence. Prior synthetic 36-family TAU0.30 fixture remains bounded negative evidence, not live substitute." Honest cost via n*3200/f*6.0 proxies broken per EXP-FRONTIER-36042599040 gap 0.484>0.35.
- **Representation loss disclosed:** TreeWalker discards style/computed layout/visual pixels; stable locator ranking discards volatile XPath positions; guard set limited to 3 predicates (URL regex, DOM hash, auth presence) not full permission lattice; WebMCP HATEOAS limited to link extraction not full JS execution; Jaccard<0.30 manifest isolates factorization from natural 0.30-0.60 Web overlap — synthetic gap dominant validity threat. Visual/computed-style and full accessibility tree not tested even on live substrate.
- **Honest cost instrument:** Per-trajectory hard-reset integer sum counters (resolve+bind+verify+freshness+browser_steps + tokens + latency) with per-trajectory hard reset, trajectory-grouped |rho_shuffled|<0.20, family-stratified bootstrap 5000 + block-permutation 5000 + global 5000 not executed but instrument validated via prior synthetic gate (PC-HONEST-COST-SANITY gap>0.35, |rho_proxy|<0.60).
- **Trajectory-grouped holdout:** Whole trajectories of test families never indexed; TRAIN-only vocab isolation verified 0 leakage — not testable without manifest. Correct-family gating via exact key-set equality after alias resolution, no cross-family adoption — same.
- **External priors distinguished:** Director mandate agent_priors_used (path dependence, planning horizon error, amortization optimism ~8% ceiling, memory vs dynamics confounding, DSM 99% TreeWalker, TraceCompiler 0.928/0.943, AgentJIT <0.1ms 100k x 0.09s vs 3-17s, COVENANT verify-repair, Chrome WebMCP shipping document.modelContext, honest-cost proxy break identifiability) are general priors, not SPIDER evidence, per spec falsifier final sentence.
- **Economics:** Build cost = actual TreeWalker+locator+DAG+SQLite INSERT OR IGNORE ops frozen before outcomes, per_task_cost = sum executed integers + LLM tokens (0 on guard-pass) + wall latency per trajectory — build ops not tuned to f, no post-hoc retuning after seeing economics.
- **No branching on outcomes:** DESIGN did not run outcome-bearing measurements; frozen thresholds unchanged; cognitive_reset true enforced (alias/routing basin treated as bounded, not prior).

## Required Fixes for Live Test (Per Handoff dependencies & Director Mandate)

Do **not** run 18th alias/routing permutation (VOI~0 per Director comparative_reasoning) and do **not** authorize product promotion of SQLite canonical compile + postcondition guard + bailout alongside WebMCP registry until audit PASS on live heterogeneous gate.

1. **Intel:** Produce diverse-site manifest deterministic seed 42 on WebGym 292k >=50 eTLD+1 or WebArena-Verified v2 192/36 with >=10 families pairwise Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 at 1280x720 CDP AX>10 mean>15 std>5 raw N>=500 (>=50/family sibling 299a300 dedup), TRAIN-only vocab isolation verified 0 leakage, trajectory-grouped holdout.

2. **Runtime:** Deploy single-worker sticky Flask HS256+nginx substrate with `/tmp/spider-runtime/shared.db` WAL, sticky cookie, If-None-Match/ETag TTL 60s conditional probes, n_non304>=800 stratified >=80/family, honest per-trajectory hard-reset sum counters resolve+bind+verify+freshness+browser_steps + tokens + latency, trajectory-grouped |rho_shuffled|<0.20 with 5000 family-stratified bootstrap + 5000 block-permutation + 5000 global permutation. Single-node honesty gate before distributed n>=800/f=100 authorization per portfolio_assessment.

3. **Frontier/Graph:** Install `playwright` + `browsergym-core` + `agentlab` with display support for 1280x720 CDP AX>10 trajectory capture (Playwright CDP, TreeWalker 99% compression fidelity via round-trip postcondition equality, stable locator ranking top-1>=95%, DAG codegen executable JSON/Python with SQLite INSERT OR IGNORE canonical compile sha256, speculative guard evaluation <5ms, bailout fallback 100% detection on N>=6 injections, WebMCP Fetch/OpenAPI >=95% + HATEOAS + routing normalization + invokeTool).

4. **Re-execute frozen gate:** First-run capture for >=40 pooled tasks (10 families x 4 trajectories min) with TreeWalker compression + locator ranking + DAG codegen + SQLite compile and WebMCP Fetch/OpenAPI+HATEOAS parse (~15-30 min wall), baseline replays (cold LLM stub token counting + alias/RAG TF-IDF fit train-A + WebMCP invokeTool, ~5-7 min CPU), honest sum counters + guard/tool eval <2s, bootstrap/block/global perms <60s CPU, per-trajectory traces <100 MB hashed. All thresholds frozen before observing outcomes.

## Do Not Assume (Per Handoff do_not_assume)

- Do not assume this MEASUREMENT_INVALID falsifies or validates C-SEMANTIC-RESOLVE; compilation bypass 0 tokens <0.1ms hot-path and TERX 100-400x external priors are not SPIDER evidence.
- Do not assume alias-catalog 21/40=0.525 ceiling or residual-novelty non-Pareto on synthetic TAU0.30 gate (rho 0.4837, ECE 0.216, RAG dominance false) globally close C-SEMANTIC-RESOLVE or frontier compilation basin; bounded FALSIFIED-IN-SETTING on synthetic orthogonal gate does not imply live heterogeneous gate will also be non-Pareto.
- Do not assume Jaccard 0.0 disjoint alphabets generalizes to natural Web overlap 0.30-0.60.
- Do not assume pooled browse saving 45.41% f10 /64.52% f100 vs cold browsing (synthetic formula length*3.2+n_novel*5.0) implies real LLM Pareto saving >=25% or product promotion.
- Do not assume distributed n>=800 health-gated WAL, 1280x720 CDP AX>10 heterogeneity, or health-gated n_non304>=800 stratified has been tested; this packet is diagnostic 0.00095s CPU-only with no BrowserGym/CDP/playwright.
- Do not cite agent_priors_used as SPIDER evidence.

## Interpretation (Interpretation Distinct from Observation)

**Observation:** Substrate entirely absent (0 families, no BrowserGym, no WAL).

**Derived Measurement:** None — no economic, coverage, latency, or calibration measurement validly obtained. Metrics null/false explicitly indicates absence.

**Interpretation:** The frozen experiment **cannot decide** whether deterministic compilation bypass achieves honest Pareto dominance or breaks the 0.525 alias ceiling on heterogeneous mixed triple-channel tasks. The question remains **untested** and requires substrate repair.

**Ceiling:** C-SEMANTIC-RESOLVE remains HYPOTHESIS. Prior ceilings preserved: synthetic TAU0.30 gate validly falsifies residual-novelty strong tracking (rho 0.4837<0.60) and alias tunnel bounded at 0.525, but live heterogeneous gate for compilation vs WebMCP shootout is untested. No product_core promotion.

**Next lane:** Frontier orthogonal compilation basin remains the most promising per Director REOPEN; PARK alternative only if valid live test (all PCs/NCs PASS) later shows FALSIFIED-IN-SETTING with no Pareto/breakthrough — not triggered by this diagnostic.

---

*Report generated from frozen EXECUTE stage per research/EXPERIMENT_PACKET.md. Raw evidence preserved in artifacts/substrate_diagnostic.json (sha256 999091e631256d...). Frozen inputs verified before inference. No outcome-bearing synthetic proxy used as live evidence.*
