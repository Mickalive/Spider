# Report — EXP-INTEL-36020904615

**Lane:** intel · **Claims:** C-CROSSSITE (primary), C-PRODUCT-ECON, C-RESIDUAL-NOVELTY  
**Status:** COMPLETE · **Outcome:** MIXED  
**Director mandate:** PIVOT+SUPERSEDE parent EXP-INTEL-36006513166 (Hard258 + GHCR + Stagehand scope)

---

## 1. What was executed

Frozen design executed without mutating `request.json` / `spec.json` / `prereg.md` / `freeze.json`.

| Module | Substance | Result |
|---|---|---|
| A — durable census | ≥2 genuine attempts per source; Hard258 union; deterministic constructibility; full-tree AX | Constructibility **4 < 10**; AX mean/gap/CI-lower fail on available set; WebGym **UNAVAILABLE** (HF 401) |
| B — blind SOTA + Pareto | Byte-identical harness re-run + Stagehand NC4 ablation + honest M_total | Baselines execute with interior CIs; DSM structure matches expectations; Stagehand HIT **0.775 < 0.80** |

**Decision-rule evaluation:** (A) MEASUREMENT_INVALID does **not** fire — durable sources have ≥2 genuine attempts each, Docker digest and manifest SHA `d6527566…` present, versions/viewport pinned, CDP full-tree used, Stagehand ablated, honest counters, provenance complete; MV5 alone defaults to UNAVAILABLE. (B) SURVIVES fails: H_A constructibility 4<10 and AX gates fail; H_B Stagehand HIT gate fails. (C) FALSIFIED triple-condition (census still 4 **and** WebGym sweep fails **and** baselines at null) is **not** met — WebGym is unavailable not failed, baselines are not at null (DSM 0.75 with structured collapse). Therefore **MIXED**.

---

## 2. Module A — durable census and AX

### Durable sources (RAW)

- **Docker Hub** `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb`: Hub API 200 ×2, `docker pull` rc=0 ×2, digest verified, `localhost:7770` HTTP 200 ×3 → **SRC_DOCKER_SUCCESS**.
- **GitHub cross-source**: `webarena-verified.json` 927596 bytes SHA `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` byte-identical ×2; Hard258 `webarna-verfied-hard.json` (upstream typo) 516731 bytes SHA `4fccaef4…`, 258/258 task_ids ⊆ pin.
- **HuggingFace**: HF_TOKEN absent → 401 ×2 per endpoint (WebArena, Hard258, WebGym) → **UNAVAILABLE**, not a negative scientific result.
- **GHCR** `ghcr.io/servicenow/browsergym:0.14.3`: 2 genuine attempts, image unavailable → **UNAVAILABLE** (infra fact). BrowserGym-core 0.14.3 already present locally via pip.

### Census (OBSERVATION)

| | primary | Hard258 |
|---|---|---|
| total | 812 | 258 |
| shopping | 192 | 61 |
| families_ge3 | 36 | 11 |
| product-page families | [136,145,196,222] | [136,145] |

Deterministic `Random(35725763380).sample(…,10)` executed twice per census, S1==S2 both times.

### Constructibility (frozen MV4)

Constructible = **4** families (`fam136, fam145, fam196, fam222`) — each with ≥1 product-page probe, all 5 anchors node_count>1, SHA stability both directions. Gate ≥10 **FAIL**.

Homepage probes (16 records) satisfy all anchors (heading 2, price 4, add_to_cart 2, main 485, contentinfo 31) but every homepage is the same URL `http://localhost:7770/` (identical DOM). Frozen MV4 requires a product-page probe; prior audit rejected identical homepage captures (p=1.0). **Homepages were not counted** — counting them would be measurement fraud.

### Full-tree multi-anchor AX_consistency (4 constructible families, 3 captures each)

| metric | value | gate | pass |
|---|---|---|---|
| mean | 0.4543 | ≥0.6 | ✗ |
| bootstrap 95% CI (B=2000, unit=family) | [0.3960, 0.5164] | lower >0.5 | ✗ |
| shuffle p (B=2000) | 0.0 | <0.05 | ✓ |
| gap (mean − shuffle mean) | 0.1432 | ≥0.20 | ✗ |
| variance | 0.00476 | >0 | ✓ |
| delta vs truncated[:20] | 0.4271 (trunc mean 0.0271) | ≥0.20 | ✓ |
| median AX / DOM | 702.5 / 218149 | >10 / ≥2000 | ✓ |

**Frozen ≥10-family gate set unavailable** — only 4 constructible families exist in primary∪Hard258. Substrate URL choice: census `get_task_start_url` product slugs (frozen protocol). Parent’s 0.6208 used `/catalog/product/view/id/{N}/` which serves *different* products (family_id ≠ product_id) — documented substrate difference, not pipeline failure.

Per-family full-tree: 136: 0.3745, 145: 0.4401, 196: 0.5418, 222: 0.4607.

---

## 3. Module B — blind external baselines and honest Pareto

Harness `exp_35999366789_blind_harness.py` imported **byte-identical** (sha `b11ea9700c7190f1fb7ef6f169af1f5da4d04dd6d52ae631376cc3c51f59ff21`); only module `OUT` redirected. 327 harness rows + 82 Stagehand ablation rows = **409** in `sota_blind_results.jsonl`. Analysis B=2000 trajectory-grouped, PERMS=1000, SEED=360361.

### Coverage (40 tasks)

| baseline | coverage | 95% CI | degenerate? |
|---|---|---|---|
| B-AGENTIC-DSM | 0.75 | [0.625, 0.875] | no (interior ✓) |
| B-SPIDER-ALIAS | 0.925 | [0.85, 1.0] | no |
| B-SPIDER-ROUTING | 1.0 | [1,1] | yes (flagged) |
| B-SPIDER-WEBMCP | 1.0 | [1,1] | yes (flagged) |
| B-COLD-LLM | 0.25 | [0.125, 0.375] | no |
| B-TRACECOMPILER-DEFUSE | 0.25 | [0.125, 0.375] | no |
| B-AGENTIC-DSM-NOHITL (NC3) | 0.25 | [0.125, 0.375] | no |
| B-BMEM-CATALOG | 0.0 | [0,0] | yes (flagged) |
| B-STAGEHAND-SELECTOR | 0.475 | [0.3, 0.625] | no |

### DSM structured collapse (expected)

header 1.0 · body 1.0 · auth 0.7 · **mixed 0.3** (single-channel mean 0.9) — matches frozen expectation “mixed 0.3 vs single 0.9–1.0”. USD mean $0.0353 [0.0294, 0.0411], total $1.41. HITL drop **0.50 ≥ 0.30** (NC3 PASS).

### Stagehand NC4 stripping ablation

| metric | post-strip | pre-strip | lift |
|---|---|---|---|
| HIT rate | **0.775** (31/40), CI [0.625, 0.9] | 0.0 (0/40) | **0.775** |
| coverage | 0.475 | 0.65 | — |

Gates: HIT_post ≥0.80 **FAIL** (0.775); pre <0.40 ✓; lift ≥0.40 ✓; NC4 delta ≥0.40 ✓; NC4 pre <0.50 ✓.

Per-channel HIT (post): header 1.0, auth 1.0, body 0.7, mixed 0.4. Shortfall driven by mixed/body families where session rotation changes rendered subtree content between observations — correct MISS semantics, but freezes H_B Stagehand ceiling below 0.80 on this substrate. Toy PC-B: Stagehand HIT **True** after stripping.

### Honest M_total Pareto

| | f=10 | f=100 |
|---|---|---|
| DSM | **22.6** [19.8, 26.0] | 5.65 |
| ALIAS | 30.1 | 7.53 |
| ROUTING | 33.0 | 8.25 |
| WebMCP | 28.0 | 7.00 |
| Stagehand | 29.3 | 7.33 |
| COLD | 38.0 | 9.50 |

WebMCP tool-bypass prevalence 0.725 [0.575, 0.85], amortized f10 2.9 / f100 0.725. |rho_shuffled| mean 0.1936 < 0.20 (NC1 PASS). No n×3200 / f×6.0 proxies.

---

## 4. Controls summary

| ID | result | note |
|---|---|---|
| PC-A | **FAIL** | Canonical captures pass (AX/DOM/SHA); AX mean 0.454 / CI-lower 0.396 / gap 0.143 fail; fixture DOM 384<2000 and anchors_gt1 false |
| PC-B | **PASS** | DSM toy True; Stagehand toy HIT True |
| PC-C | **UNAVAILABLE** | HF_TOKEN absent after 2 attempts |
| PC-D | **PASS** | families_ge3 2 ≥2 |
| B-GHCR | **UNAVAILABLE** | 2 attempts; image not found |
| B-WEBARENA-DOCKER | **PASS** | digest + reachability |
| B-HARD258 | **PARTIAL** | 258/11 pass; union constructible only 4 |
| B-WEBGYM | **UNAVAILABLE** | 401 |
| B-TRUNCATED-20 | **MIXED** | real delta 0.427 ✓; shuffled variant 0.311 ✗ (definitional ambiguity) |
| B-AGENTIC-DSM | **PASS** | matches all frozen numbers |
| B-STAGEHAND | **PARTIAL** | lift/pre pass; HIT 0.775<0.80 |
| B-BMEM / ALIAS / ROUTING / WEBMCP / COLD | **PASS** | as expected (degenerates flagged) |
| NC1 | **PASS** | \|rho_shuffled\|=0.1936; ALIAS p=0.626 |
| NC2 | **MIXED** | real ✓; shuffled operationalization ambiguous (see validity_notes) |
| NC3 | **PASS** | drop 0.50 |
| NC4 | **PASS** | lift 0.775, pre 0.0 |
| NC5 | **MIXED** | shuffled mean 0.311 <<0.6 ✓; gap 0.143 ✗; frozen p>0.05 directionally ambiguous |

---

## 5. Interpretation (distinct from measurements)

- **H_A does not SURVIVE.** Primary∪Hard258 deterministically yields 4 constructible product families. Full-tree AX on that set is below the frozen 0.6 / CI-lower 0.5 / gap 0.20 thresholds. WebGym diverse sweep is UNAVAILABLE (HF 401), which under the frozen MV5 clause does not by itself trigger MEASUREMENT_INVALID but leaves H_A partially unavailable. This is a **bounded negative on this substrate**, not a global rejection of cross-site transfer.
- **H_B mostly holds structurally but misses one frozen gate.** DSM, BMEM, SPIDER baselines, NC3 HITL, honest Pareto, and NC4 stripping lift all match or exceed frozen expectations with non-degenerate interior CIs where variance>0. Stagehand post-strip HIT 0.775 is a valid negative against the ≥0.80 gate (CI includes 0.80; point estimate fails). NC2 shuffled-variant fails under the literal token-reassignment operationalization and is reported with the definitional ambiguity from prior experiments.
- **MIXED, not FALSIFIED:** the frozen FALSIFIED triple requires census 4 **and** WebGym sweep fail **and** baselines at null — two of three are false (WebGym unavailable; baselines discriminative).
- **Not MEASUREMENT_INVALID:** all MV clauses that fire MEASUREMENT_INVALID under §8(A) pass; remaining issues are scientific negatives or documented UNAVAILABLE clauses.

### Consequences

- **If anything positive:** Graph can treat the 4-family constructible set + full-tree pipeline as a *validated measurement instrument* at the 4-family ceiling (median AX>10, DOM≥2000, SHA both directions, delta vs truncated 0.427). Product has an honest O(1) Pareto (DSM F10 22.6, ALIAS 30.1, WebMCP prevalence 0.725) for C-PRODUCT-ECON / C-RESIDUAL-NOVELTY deliberation. NC4 proves expanded stripping is load-bearing (lift 0.775).
- **If negative:** Graph ≥10-family hold-out remains **BLOCKED** on these two censuses — next work needs an orthogonal census (WebMall/Mind2Web-2 loopback, WebGym-derived independent hosting) or definition expansion, **not** another N=20 longest-prefix on the same 4 families. C-CROSSSITE stays HYPOTHESIS/EXPERIMENTAL at the 4-family ceiling. Stagehand as shipped ceiling does not clear 0.80 HIT on this synthetic alias-OOD without redesign (mixed-channel rotation).
- **No claim is promoted.** DIRECTOR adjudicates registry statuses; this packet only reports measurements.

---

## 6. Evidence index (selected)

| artifact | sha256 (prefix) | role |
|---|---|---|
| artifacts/derived/sota_blind_results.jsonl | `2d59aa255a0eb8db…` | raw per-task logs (409 rows) |
| artifacts/derived/sota_analysis.json | `5552c27a98ef3452…` | derived analysis |
| artifacts/derived/stagehand_strip_delta.json | `3c0ef22ab9223e32…` | NC4 table |
| artifacts/derived/ax_consistency_fulltree.json | `9bc5ad849651d9da…` | AX consistency |
| artifacts/derived/family_anchoring.json | `2472ccbac2f5ad0b…` | constructibility |
| artifacts/raw/ax_captures_consistency.jsonl | `7a9e37e7c4e52c4f…` | raw AX trees |
| artifacts/raw/docker_pull_attempts.json | `ae112f222867805e…` | SRC-Docker |
| artifacts/raw/github_cross_source_attempts.json | `33956db3aaaedad9…` | cross-source byte identity |
| research/intel/exp_35999366789_blind_harness.py | `b11ea9700c7190f1…` | byte-identical harness |

Full path+sha256 list in `provenance.json` and `result.json.artifacts`.

---

*End of report. Raw evidence → observation → derived measurement → interpretation kept distinct; interpretations are labeled and do not rewrite measurements.*
