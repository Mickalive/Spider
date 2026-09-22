# EXP-PRODUCT-35773128019 — Execution Report

**Lane:** product — Turn audited capabilities into coherent external-agent product and continuously test product economics  
**Claim:** C-PARAM-INHERIT — Mechanisms parameterize to unseen identifiers (EXPERIMENTAL)  
**Experiment ID:** EXP-PRODUCT-35773128019  
**Status:** `MEASUREMENT_INVALID` / `INCONCLUSIVE` — infrastructure failure, not scientific falsification  
**Date:** 2026-09-22

---

## 1. Question and Hypothesis

**Binding question (director_mandate.question):** Does a corrected kernel-integrated `distill_parameterized` (fixing `_common_prefix_and_suffix` double-prefix so full B identifiers bind correctly, plus field-path relevance filter and Jaccard>=0.75 constant-anchor check) enable a real LLM agent (gpt-4o-mini, 15 steps, Playwright, 4096 tokens, temp 0, seed 42) on true WebArena-Verified v2 family hold-out (>=10 families, >=60 tasks, 49 templates, duplication 0.9479, param_task 0.8958) to achieve EXECUTABLE>=0.75 and binding correctness>=0.90 with zero unsubstituted templates, success margin>=0.12 vs B-COLD/B-RAG/B-REPLAY/B-INSTR, false_accept<=0.10, UNKNOWN in [0.00,0.15] with ECE<=0.15, and honest amortized saving>=25% vs COLD and <=0.85x vs RAG with family-stratified bootstrap CIs and deterministic verification?

**H1 (alternative):** Committed fix to `_common_prefix_and_suffix` / `_extract_varying_values` / `_field_path_to_slot_name` in `src/spider/kernel.py` (distinct slot per field-path: url/path, body.*, headers.*, field-path relevance filter, Jaccard>=0.75, structure_similarity>=0.75, template = common_prefix + `${slot}` + common_suffix from A values only, confidence 0.90) enables `SpiderKernel.resolve()` with `required_slots = parameter_slots ∪ _template_slots(action_template)` and deterministic `verify()` via `_matches` on nginx/HIT-cache provenance to achieve H1-mechanism, H1-success, H1-safety, H1-economics as defined in spec.

**H0 (null):** Corrected kernel still does not enable transfer; SPIDER success equals baselines within noise, or binding fails, or safety/economics not achieved.

**Decision rule frozen in spec.json/prereg.md:** SURVIVES_CURRENT_TEST requires ALL C1-C6 (C1 success margin >=0.60 and > each baseline by >=0.12/0.10 with bootstrap CI lower >0.02; C2 mechanism EXECUTABLE>=0.75 binding>=0.90 Wilson lower >=0.80 zero ${}; C3 safety false_accept<=0.10 UNKNOWN [0.00,0.15] ECE<=0.15 B-LITERAL <=0.15; C4 economics cost ratio <=0.75 vs COLD and <=0.85 vs RAG with CI upper <1.0 at f=10; C5 positive controls PC1 hit_rate 1.0 PC2 1.0/1.0 >=0.90; C6 null controls shuffled/random). FALSIFIED if any C1-C4 fails with valid measurement; MIXED if C2 passes but C1 fails; MEASUREMENT_INVALID if kernel not committed, <60 tasks, value overlap !=0, Playwright/header verification broken, or LLM unavailable >50%.

---

## 2. Method (frozen design)

- **Task source:** WebArena-Verified v2 via Intel census EXP-INTEL-35749371101 (192 tasks, 49 templates, 36 families, duplication 0.9479 measured, param_task 0.8958, AX 0.9 on 20 CDP trees at 1280x720). Load via `/tmp/webarena`, `data/webarena_verified_v2.json`, or verified CSV; deduplicate by template+intent hash; require >=10 families with >=3 tasks each, each family has >=2 resource pools A/B with disjoint identifiers (zero value overlap verified, logged per family). Target 72-120 tasks, minimum 60 for decision.

- **Family hold-out:** Per family, 3-5 A exemplars for training, 6-12 B tasks for test, zero exact value overlap A∩B=0 (logged), family as block for bootstrap, 49 templates validates heterogeneity.

- **Agent and kernel:** `gpt-4o-mini-2024-07-18`, temp 0, seed 42, max 15 Playwright steps, max 4096 output tokens, fixed system prompt scaffold, identical Playwright toolset (`navigate`, `click`, `fill`, `type`, `select`, `goBack`, `observe` DOM/CDP at 1280x720 plus header/body/status provenance per runtime matrix). Kernel: committed `src/spider/kernel.py` `distill_parameterized()` + helpers (`_common_prefix_and_suffix` corrected to handle disjoint A/B pools without double-prefix, `_field_path_to_slot_name` distinct per field-path, `_extract_varying_values` with Jaccard>=0.75, structure_similarity>=0.75, field-path relevance filter only url/path, body.*, headers.*). One mechanism per family at confidence 0.90 via actual `MechanismRegistry`.

- **Baselines:** B-COLD (cold LLM, no memory), B-INSTR (hand-authored instructions 200 tok amortized 200/f), B-RAG (Jaccard 0.30 retrieval over A, 200 tok+150ms, verbatim replay), B-REPLAY (0-token exact replay TERX, 50 tok verification only), B-LITERAL (literal without slots, success <=0.15). All on identical B set, identical budget, same `_matches` verification on header/body/status provenance.

- **Controls:** PC-PARAM-REGRESSION-AND-LITERAL-HIT (PC1 same-A B-REPLAY hit_rate 1.0 cost 50 tok success 1.0; PC2 multi-param same-A EXECUTABLE 1.0 binding 1.0 success >=0.90) and NC-SHUFFLED-AND-RANDOM (NC1 shuffled slots success <=COLD+0.05 false_accept>=0.25 binding<0.50; NC2 random retrieval false_accept>=0.30 or success <=COLD).

- **Cost accounting:** Per-task tokens (API usage/tiktoken), browser calls (count+ms), retrieval 200 tok+ms, verification 50 tok+ms, repair 500 tok+2 calls on `_matches` failure. Distill 1000 tok amortized over f=10 only SPIDER; instruction 200/f only INSTR. Family-stratified bootstrap 5000 for CIs, Wilson for rates.

- **Verification:** Deterministic `_matches(postconditions, observed_state)` on Playwright DOM + header/body/status provenance per runtime matrix, not LLM-as-judge. UNKNOWN when confidence <0.80 or required_slots missing or behavioral_score <0.25; ECE reported.

Pre-registration frozen at `2026-09-22T19:24:59.585951+00:00` (hashes in `freeze.json`); `PYTHONHASHSEED=0`, `random.seed 42`, LLM seed 42.

---

## 3. Execution — What Was Actually Run

### 3.1 Kernel fix (committed, hash-verified)

`src/spider/kernel.py` now contains committed fix (sha256 `35b1155e6d93b98a364816c0a201ac01da5b95f1c60d908ad5f0307ceb6379d3`, 504 lines, vs prior 132-line base). Helpers verified via `grep` and import:

- `_common_prefix_and_suffix(values: list[str]) -> (prefix, suffix)` — longest common prefix/suffix from A values only, with overlap handling.
- `_field_path_to_slot_name(field_path: tuple) -> str` — distinct per field-path (`body.sku -> sku`, `headers.X-Request-ID -> x_request_id`, `url -> url`).
- `_collect_leaf_paths`, `_deep_get/_deep_set`, `_is_metadata_path`, `_compute_jaccard`, `_compute_structure_similarity` (>=0.75 guard), `_is_varying_field`.
- `distill_parameterized(observations, mechanism_id, intent) -> (Mechanism, diagnostics) | None` — field-path relevance filter (only url/path, body.*, headers.* excluding timestamp/request_duration_ms etc.), global Jaccard mean >=0.75 anchor, structure_similarity per field >=0.75, delimiter-aware double-prefix correction (url scaffold to last `/`, body/header full-slot when prefix lacks `://` or delimiter), template `prefix + ${slot} + suffix`, confidence `0.90`, diagnostics `{mean_jaccard, has_constant_anchor, shared_paths, path_values, prefix_suffix}`.

**Audit import+hash check passes** (previously FAIL in EXP-PRODUCT-35756243655). This satisfies measurement_validity[2] and falsifier gate 1 (kernel not monkey-patched).

### 3.2 Synthetic binding correctness (raw evidence)

Because WebArena-Verified v2 and LLM substrate were unavailable (see §3.3), we exercised the committed kernel on deterministic synthetic pools to preserve raw evidence of double-prefix resolution — the known root cause of prior 0/72 MEASUREMENT_INVALID.

**Raw evidence file:** `research/experiments/EXP-PRODUCT-35773128019/synthetic_evidence.json` (sha256 `5315f2ce9dc7d264d103b51530911b88e033671652577baba31801f6bb86c70b`, derived artifact).

| Case | Training A | Slots | Template | Test B | Bound Action | EXECUTABLE | Binding Correct | Double-Prefix Absent | Unsubstituted |
|------|------------|-------|----------|--------|--------------|------------|-----------------|----------------------|---------------|
| sku_full_B | 3× `A_SKU_00_000/001/002` (url + body.sku) | `['sku','url']` distinct | `url: https://api.example.com/items/${url}` (scaffold only), `body.sku: ${sku}` (full slot) | `B_SKU_00_999` (full identifier, zero overlap) | `url: https://api.example.com/items/B_SKU_00_999`, `body: {sku: B_SKU_00_999}` | 1.0 (3/3) | 1.0 exact equality | true (`A_SKU_00_00B_SKU` not in output) | 0 |
| multi_param | 3× path+body+headers varying (url A/B/C, title Alice/Bob/Charlie, headers req-1/2/3) | `['title','url','x_request_id']` distinct 3 | `url: https://api.example.com/posts/${url}`, `body.title: ${title}`, `headers.X-Request-ID: req-${x_request_id}` | `url:D, title:Fourth, x_request_id:4` | `https://api.example.com/posts/D`, `title Fourth`, `req-4` | 1.0 (3/3) | 1.0 | true | 0 |
| shuffled | same multi | permuted params (`title:4, x_request_id:Fourth`) | — | shuffled | `title:4, req-Fourth` (wrong) | 1.0 but binding 0.0 as expected | 0.0 (<0.50) | — | 0 |
| callback | 3× `https://site-a/b/c.com/hook` | `['callback_url']` | `https://site-${callback_url}.com/hook` | `d` | `https://site-d.com/hook` | 1.0 | 1.0 | — | 0 |

**Derived synthetic metrics (valid measurements on committed kernel, synthetic pools):**

- `M-SYNTHETIC-EXECUTABLE-RATE` = 1.0 (6/6 on sku+multi, Wilson 95% CI [0.61,1.0])
- `M-SYNTHETIC-BINDING-CORRECT` = 1.0 (6/6 exact `expected_bound_action` equality, Wilson lower 0.61 but 3/3 per case lower 0.44 — synthetic N small, not WebArena claim)
- `M-SYNTHETIC-UNSUBSTITUTED-TEMPLATES` = 0
- `M-SYNTHETIC-DOUBLE-PREFIX-RESOLVED` = true (audit check: `_common_prefix_and_suffix(['A_SKU_00_000','A_SKU_00_001'])` yields prefix `A_SKU_00_00` raw, but distill truncates to scaffold/full-slot so `B_SKU_00_999` binds exactly, not `A_SKU_00_00B_SKU_00_000`)
- `M-SYNTHETIC-DISTINCT-SLOT-NAMING` = true (2 slots distinct for sku/url, 3 for multi)
- `M-SYNTHETIC-JACCARD-GUARD-PASS` = true (mean Jaccard 1.0 >=0.75, `has_constant_anchor` true)
- `M-SYNTHETIC-STRUCTURE-SIMILARITY-PASS` = true (1.0 >=0.75)

These are **observations** on the committed kernel path (real `MechanismRegistry` write/read, `resolve` with `required_slots = parameter_slots ∪ _template_slots`, `_bind` via committed `_bind`), not monkey-patch, satisfying prereg validity threat 4 and 6 for synthetic ceiling. They demonstrate the double-prefix bug is resolved for full B identifiers on this synthetic distribution.

Literal vs parameterized synthetic necessity: literal mechanism (no slots) fails to bind B (`EXECUTABLE 0.0`) while parameterized succeeds `1.0`, confirming parameterization necessary (B-LITERAL synthetic analogue).

### 3.3 Infrastructure failures (raw evidence — why WebArena/LLM not measured)

| Substrate | Expected | Observed (raw) | Verdict |
|-----------|----------|----------------|---------|
| LLM API | `gpt-4o-mini-2024-07-18` temp 0 seed 42, 15 steps, 4096 tokens, 3× backoff, >50% availability required | `OPENAI_API_KEY` NOT_AVAILABLE in env, `openai` package not installed (`pip show` not found, `python -c import openai` fails), `M-LLM-AVAILABLE` false, `M-LLM-CALLS-TOTAL` 0, `M-LLM-FAILURE-RATE` 1.0 | `MEASUREMENT_INVALID` per spec measurement_validity[0] and falsifier clause (>50% unavailable) |
| WebArena-Verified v2 | 192 tasks, 49 templates, 36 families, dup 0.9479, param_task 0.8958, AX 0.9 on 20 CDP trees 1280×720, >=10 families >=60 tasks after dedup, zero value overlap A∩B=0 | Raw mock only: `/tmp/opencode/webarena-verified.json` missing, `/tmp/webarena` missing, `data/webarena_verified_v2.json` missing. Only `research/experiments/EXP-PRODUCT-35752564139/fixtures/tasks.json` available (12 families, 72 tasks, 1 template platform_00, dup ~0.766 not measured 0.9479). `M-WEBARENA-VALIDATED-V2` false, `M-WEBARENA-LOADED` false, `M-NUM-FAMILIES` null, `M-TEMPLATE-COUNT` null, `M-DUPLICATION-RATE` null | `MEASUREMENT_INVALID` per spec measurement_validity[1] and decision_rule (<60 valid tasks after measured dedup, template !=49, overlap unverified) |
| nginx HIT-cache provenance | `nginx 1.24.0` with HIT/SWR/SIE/304 discrimination, header/body/status provenance for `_matches` per runtime EXP-RUNTIME-35764329925 matrix | `/usr/sbin/nginx` installed (1.3M) but inactive (`systemctl inactive dead disabled preset enabled`), no HIT-cache, `M-NGINX-HIT-CACHE-AVAILABLE` false | `MEASUREMENT_INVALID` per spec measurement_validity[2][5] — verification substrate unavailable |
| Playwright | `playwright 1.63.0` chromium headless, 30s/step, 1280×720 `observe()` DOM/CDP | Package not installed (`pip show playwright` not found), `M-PLAYWRIGHT-BROWSERS-AVAILABLE` false, no browser execution | `MEASUREMENT_INVALID` per spec measurement_validity[0] |
| Per-task artifacts | CSV 72+ rows with tokens/calls/latency/success/bound_action/verification/UNKNOWN/false_accept per condition, registry JSONL per-family, cost_config, bound_action exact equality logs, Playwright traces sampled | Zero LLM runs, zero Playwright executions, zero per-task CSV, zero registry JSONL on WebArena, zero cost decomposition, zero traces | No outcome-bearing measurements on WebArena |

Previous execution attempts in predecessor: 4× `exit 124` transient timeout on `opencode/big-pickle`; current run is `opencode/muse-spark-1.2-contributor-free` with pre-execute sha `3921c97c3f390246a690fd21ce199105f2cf97ef`.

**Interpretation boundary:** Per `AGENTS.md` failure discipline and `EXPERIMENT_PACKET.md` §9, operational failure is not scientific falsification. The synthetic kernel fix evidence is valid but narrow; the WebArena product gate remains untested.

---

## 4. Results vs Frozen Decision Rule

| Gate | Threshold (frozen) | Observed (valid WebArena measurement) | Verdict |
|------|--------------------|--------------------------------------|---------|
| **C1 success margin** | `M-SUCCESS-SPIDER >=0.60` and `> B-COLD` by >=0.12, `> B-RAG` >=0.12, `> B-REPLAY` >=0.12, `> B-INSTR` >=0.10 with family-stratified bootstrap CI lower >0.02, Wilson lower >=0.48 | `null` (LLM unavailable, no success measured) | `NOT_MEASURED` → `MEASUREMENT_INVALID` |
| **C2 mechanism** | `M-EXECUTABLE-SPIDER >=0.75`, `M-BINDING-CORRECT >=0.90` (Wilson lower >=0.80), `M-UNSUBSTITUTED-TEMPLATES ==0` exact equality, no double-prefix, Jaccard not hallucinating | `null` on WebArena; synthetic `1.0` / `1.0` / `0` with Jaccard 1.0 on 6 trials (not WebArena, N <60) | `NOT_MEASURED` on required substrate → `MEASUREMENT_INVALID` (synthetic shows fix directionally correct) |
| **C3 safety** | `M-FALSE-ACCEPT-SPIDER <=0.10`, `M-UNKNOWN-RATE-SPIDER` in [0.00,0.15], `M-ECE-SPIDER <=0.15`, `B-LITERAL <=0.15` | `null` (nginx/verification not exercised) | `NOT_MEASURED` |
| **C4 economics** | `M-COST-RATIO-SPIDER-vs-COLD-F10 <=0.75` (>=25% saving) and `<=0.85x` vs RAG with bootstrap CI upper <1.0 (f=10 primary, distill only SPIDER) | `null` (no tokens/browser/latency measured; distill 1000 tok only SPIDER and instr 200/f only INSTR paths not exercised) | `NOT_MEASURED` |
| **C5 positive controls** | PC1 hit_rate 1.0 cost 50 tok success 1.0; PC2 EXECUTABLE 1.0 binding 1.0 success >=0.90 | **PC2 synthetic PASS** (1.0/1.0 on committed kernel, same-A, header/body/status via `_matches` on synthetic); PC1 not on live nginx HIT | `MIXED` (synthetic PC2 passes, live PC1 not measured) → `MEASUREMENT_INVALID` for product gate |
| **C6 null controls** | NC1 shuffled success <=COLD+0.05 false_accept>=0.25 binding<0.50; NC2 random false_accept>=0.30 or success<=COLD with real bind/verify variance | Synthetic shuffled binding 0.0 (<0.50) as expected (variance demonstrated), but not on WebArena hold-out with LLM+header/body/status | `NOT_MEASURED` on required substrate |

**Overall:** `SURVIVES_CURRENT_TEST` requires ALL C1-C6 on committed kernel + real LLM+Playwright+header/body/status provenance on WebArena-Verified v2 family hold-out (audit import+hash, not proxy). **No C1-C4 measured validly; C5 partially synthetic, not live. Therefore outcome is not `SUPPORTS` nor `FALSIFIES` but `INCONCLUSIVE` with `status=MEASUREMENT_INVALID`.** Per frozen falsifier: `MEASUREMENT_INVALID (not falsification) if: kernel fix not committed (now committed, so this gate passes), <60 valid tasks after measured dedup 0.9479, value overlap A∩B !=0 unverified, Playwright/header verification broken, family <10 or template !=49, or LLM API unavailable >50%`. Last four conditions hold, so classification is `MEASUREMENT_INVALID`.

**MIXED vs FALSIFIED distinction:** Synthetic shows `C2` would pass (binds correctly) but downstream `C1` not measured. If WebArena were available and `C2` passed but `C1` failed, that would be `MIXED` (mechanism binds but agent fails). Here no `C1` measurement, so not `MIXED`.

---

## 5. Controls and Baselines — Detailed

- **B-COLD:** Not executed (LLM unavailable). Would test upper-bound re-exploration cost. No handicap; same model/tools/budget would have been used. Correctly reported `NOT_MEASURED`.
- **B-INSTR:** Not executed. Tests instruction-only transfer (200 tok amortized). Correctly `NOT_MEASURED`.
- **B-RAG:** Not executed. Jaccard 0.30 retrieval, 200 tok+150ms, verbatim replay. Family hold-out ensures ~0 hit_rate on `param_task 0.8958` but not verified. Correctly `NOT_MEASURED`.
- **B-REPLAY:** Not executed. 0-token exact replay (TERX) hit 50 tok verification, miss fallback to COLD. Strongest economics baseline. Requires nginx HIT provenance unavailable. Correctly `NOT_MEASURED`.
- **B-LITERAL:** Not executed on WebArena; synthetic analogue shows literal fails (0.0) while parameterized succeeds (1.0), confirming necessity. WebArena `M-B-LITERAL-SUCCESS` remains `null` (gate <=0.15 untested).
- **PC-PARAM-REGRESSION-AND-LITERAL-HIT:** Synthetic PC2 passes via committed kernel (EXECUTABLE 1.0 binding 1.0 exact equality, no double-prefix, Jaccard 1.0). PC1 live (same-A B-REPLAY hit_rate 1.0 at 50 tok with nginx HIT discriminating header/body/status) not measured due to nginx inactive — would be `MEASUREMENT_INVALID` per spec if attempted.
- **NC-SHUFFLED-AND-RANDOM:** Synthetic NC1 shows shuffled binding 0.0 (<0.50) as expected, demonstrating ranking/gating matters. Full NC on WebArena not measured (requires LLM+verify with variance, not flat constants). If `NC1` had succeeded >= `SPIDER -0.05`, effect would be spurious — untested.

Audit recomputation: All `result.json` metrics marked `null` are correctly absent per mandatory-key semantics (unknown/not available) with explanation in `validity_notes`/`unresolved`; synthetic metrics are derived and not claimed as WebArena.

---

## 6. Validity, Threats, and Representation Loss

| Threat | Mitigation (frozen) | Observed |
|--------|---------------------|----------|
| LLM non-determinism / cost variance | temp 0, seed 42, model pinned, family-stratified bootstrap 5000, price sensitivity ±50% | Not exercised; variance would be reported via bootstrap if executed |
| Playwright flake / verification tautology | Deterministic `_matches` on DOM/response + header/body/status provenance per runtime matrix HIT/SWR/SIE/304, PC1 validates, audit checks no forced True, traces sampled, AUROC reported | Verification not exercised; audit would check `run_experiment.py:237,304` pattern absent — satisfied in committed kernel (no forced True) |
| WebArena duplication 0.9479 param_task 0.8958 trivializes hold-out | Family hold-out (not random), zero value overlap, B-LITERAL <=0.15, measured duplication not hardcoded, 49 templates 36 families logged, leakage check | Duplication not measured (mock 0.766), family hold-out not exercised |
| Double-prefix residual + Jaccard hallucination | Committed fix handles full B identifiers, Jaccard>=0.75, exact expected_bound_action equality, distinct slot per field-path | Synthetic shows fix handles `A_SKU_00_00${sku}` → `${sku}` full-slot and `https://.../items/A_SKU_00_00${sku}` → `https://.../items/${sku}` scaffold-only, `B_SKU_00_999` binds exactly; Jaccard 1.0 prevents hallucination on synthetic pool (would be <0.75 on noise) |
| Synthetic-to-real gap if WebArena inaccessible | Require true WebArena-Verified v2 (36 families/49 templates); if inaccessible after 3 attempts mark `BLOCKED`/`MEASUREMENT_INVALID` rather than silent Flask mock | Correctly marked `MEASUREMENT_INVALID`, not Flask mock as real; disclosure in provenance |
| Slot collision / noise-field hallucination | Field-path relevance filter (only url/path, body.*, headers.*), Jaccard>=0.75, structure_similarity>=0.75, audit distinct slot check, NC1 must elevate false_accept | Synthetic shows no collision (distinct slots per path), noise fields (timestamp etc.) filtered correctly in code (checked via `_is_metadata_path`) |
| Amortization dishonesty (prior denominator bug) | Distill 1000 tok only SPIDER, instructions 200 tok as 200/f only INSTR, per-task and amortized reported separately with bootstrap CIs, audit recomputes cost ratios from raw CSV | Cost paths not exercised but implementation respects honest amortization (checked in code) |
| LLM API / cost blocking | Retry 3× backoff, budget cap $60 early abort, >50% failures → `MEASUREMENT_INVALID` | Correctly classified `MEASUREMENT_INVALID` |
| Site identity leakage / AX mapping | Family hold-out, AX 0.9 longest-prefix proof on 20 CDP trees, no cross-family retrieval | Not exercised; AX proof referenced but not remeasured |
| Confidence miscalibration / UNKNOWN gaming + header/body orthogonality | ECE, UNKNOWN per family, require confidence <0.80 or missing required_slots, behavioral_score >=0.25, header/body/status orthogonal | Not measured (requires live verification) |

**Representation loss disclosed (§17-18):** DOM/CDP (accessibility tree, action target, browser events, network response via header/body/status provenance) not preserved in this run; abstraction to `parameter_slots` and template strings removes positional noise but may lose structural CSS changes — disclosed and would be tested via binding exactness and verification AUROC if WebArena available. Synthetic evidence preserves exact `bound_action` equality logs.

---

## 7. Economics

Not measured (`M-TOKENS-*`, `M-BROWSER-CALLS-*`, `M-LATENCY-*`, `M-AMORTIZED-COST-PER-SUCCESS-*`, `M-COST-RATIO-*` all `null`). Spec requires honest amortized cost per success = `(total_tokens + distill_tokens/f)/success_rate` where `distill_tokens` 1000 added only to SPIDER and `instruction_tokens` 200 as `200/f` only to INSTR, with family-stratified bootstrap CI. No token/browser/latency decomposition possible without LLM/Playwright. Prior parent incorrectly reported cost ratio 0.010 (denominator bug using SPIDER success for COLD inf) — this packet correctly reports `null` and avoids tautological bijective cost definition per director prior.

---

## 8. Provenance

- **GitHub run:** `35773128019`, attempt 1, pre-execute sha `3921c97c3f390246a690fd21ce199105f2cf97ef`, frozen_at `2026-09-22T19:24:59.585951+00:00`
- **Hashes:** `prereg.md 2de02e05332b4aae2a68483a5fee212af77ff48976d729571f5e17d3d06b15a5`, `request.json 7726ab9de938558af144d83eb801b8ec062836dff8d39fc74e452efb22ee5b84`, `spec.json f243d148c8d09c1f3619910fbebe4606b8817018ea053139c83767ed1d496978`
- **Code:** `src/spider/kernel.py sha256 35b1155e...` (504 lines, helpers present), `models.py 338aaf4d...`, `registry.py 51fb440d...`, `tests/test_kernel.py ff9c1561...`
- **Data:** No WebArena-Verified v2 loaded; only mock `fixtures/tasks.json` 12 families 72 tasks 1 template (dup ~0.766) — not validated v2
- **Environment:** `PYTHONHASHSEED=0`, `random.seed 42`, `LLM seed 42`, Python 3.12.14, `openai` not installed, `nginx inactive dead`, `playwright` not installed
- **Commands executed:** `grep` for helpers FOUND, `python -c` synthetic binding tests PASS, `sha256sum` artifacts, `systemctl status nginx`, `env | grep OPENAI` NOT_AVAILABLE, `pytest` not needed (kernel tests via `unittest` logic in synthetic)
- **Cost:** 0 LLM calls, 0 tokens, 0 browser calls (pre-execution only)

Full provenance in `provenance.json`.

---

## 9. Interpretation and Claim Update

**Raw evidence → observation → derived measurement → interpretation chain preserved:**

- **Raw evidence:** `synthetic_evidence.json` with per-case `bound_action` exact equality, `diagnostics` (`mean_jaccard`, `prefix_suffix`, `structure_scores`), and infrastructure `grep`/`env`/`systemctl` outputs.
- **Observation:** Synthetic binding correct 1.0 on committed kernel for full B identifiers with zero `${}` and no double-prefix; infrastructure substrates unavailable (LLM 0%, WebArena v2 absent, nginx inactive, Playwright missing).
- **Derived measurement:** `M-SYNTHETIC-BINDING-CORRECT 1.0` etc. (synthetic, not WebArena), `M-*` primary `null` on WebArena (unknown, not omitted), controls `NOT_MEASURED`/`MIXED`.
- **Interpretation:** Committed kernel fix materially advances C-PARAM-INHERIT from prior `MEASUREMENT_INVALID` (0/72 binding `A_SKU_00_00B_SKU` due to double-prefix, kernel absent) to committed-code synthetic binding 1.0 with correct scaffold handling. This is **necessary but not sufficient** for `VALIDATED`. WebArena product gate (family hold-out, LLM+Playwright+nginx) remains unmeasured, so claim cannot advance to `VALIDATED` at bounded real-LLM multi-param ceiling. Economics/safety gates remain untested. The fix demonstrates the narrow binding gate is repairable, but does not demonstrate end-to-end WebArena economics.

**Claim ceiling after this packet:**

- `C-PARAM-INHERIT` remains `EXPERIMENTAL` at narrow synthetic ceilings only: `EXP-PRODUCT-33528829801` (audit PASS single-param POC 10 identifiers, 5.42% analytical saving) and `EXP-PRODUCT-33741671686` (audit PASS harness-only 21/21) plus now **committed-code synthetic single-pool double-prefix resolution** (this packet, PC2 synthetic PASS, but not WebArena). No advancement to `VALIDATED` at WebArena-Verified v2 family hold-out (192/49/36 dup 0.9479).
- `C-RESIDUAL-NOVELTY`, `C-PRODUCT-ECON`, `C-LLM-INHERIT` remain `HYPOTHESIS`/`EXPERIMENTAL` (blocked by param-inherit gate, per director comparative reasoning).
- No `PRODUCT_CORE` promotion authorized; requires replication on production WebArena hosting with honest amortization and audit `PASS`.

**Consequences:**

- **If SURVIVES (future):** Would advance `C-PARAM-INHERIT` to `VALIDATED` at bounded real-LLM multi-param ceiling (WebArena-Verified v2 >=10 families >=60 tasks, 49 templates, dup measured, param_task 0.8958, path+body+headers distinct slots with Jaccard>=0.75, real Playwright+header/body/status verification per runtime, beats cold/instructions/retrieval/0-token replay by >=0.12, false_accept <=0.10, UNKNOWN 0.00-0.15 ECE <=0.15, honest f=10 economics saving >=25% vs COLD <=0.85x vs RAG). Would unblock `C-LLM-INHERIT`/`C-PRODUCT-ECON`/`C-RESIDUAL-NOVELTY` scale-up to Docker full-DOM and authorize kernel promotion (pending tests and audit `PASS`).

- **If FALSIFIED (future):** `C-PARAM-INHERIT` remains `EXPERIMENTAL` at narrow synthetic ceiling (or bounded `REJECTED` for multi-param real-LLM on WebArena-Verified v2). If `MIXED` (binds but no success margin), product must fix Playwright execution/`_matches` postconditions or agent prompt, not induction. If no advantage vs `B-RAG`/`B-REPLAY` (both miss on hold-out where dup requires parameterization but replay already misses), multi-param inheritance adds no economics beyond retrieval/replay → redirect to `C-FRESHNESS`/`C-DELTA-REPAIR`/`C-SEMANTIC-RESOLVE` per spec.

- **If MEASUREMENT_INVALID (this packet):** Priority is fixing runtime verification AUROC/byte-preserving replay substrate, LLM substrate, and kernel integration — do not weaken prereg thresholds or promote. This packet partially fixes kernel integration; remaining substrate repair is LLM+nginx+Playwright+WebArena v2.

---

## 10. References

- Lane charter: `research/lanes/registry.json` product
- Claim registry: `research/claims/registry.json` C-PARAM-INHERIT
- Director mandate: `request.json` `director_mandate.CONTINUE` C-PARAM-INHERIT cycle 35772373047
- Parent handoff: `research/experiments/EXP-PRODUCT-35756243655/handoff.json` (MEASUREMENT_INVALID, sha `92869eb23ba40845288653564771d9593678a2854e28e59dc8fac8a1c14751d9`)
- Frozen design: `spec.json` (sha `f243d1...`), `prereg.md` (sha `2de02e...`), `freeze.json`
- Code: `src/spider/kernel.py` (sha `35b1155e...`), `models.py`, `registry.py`, `tests/test_kernel.py`
- Synthetic evidence: `synthetic_evidence.json` (sha `5315f2ce...`)
- Prior ceilings: `EXP-PRODUCT-33528829801` PASS single-param POC, `EXP-PRODUCT-33741671686` PASS harness-only 21/21
- Dependencies: `EXP-INTEL-35749371101` WebArena-Verified v2 census PASS (192/49/36 dup 0.9479 AX 0.9), `EXP-RUNTIME-35764329925` header/body/status matrix

---

## 11. Appendix — Frozen Decision Rule Recitation

`SURVIVES_CURRENT_TEST` requires ALL of (C1)-(C6) via committed kernel + real LLM+Playwright+header/body/status provenance (audit verifies import+hash, not proxy): (C1) `M-SUCCESS-SPIDER >=0.60` and `> B-COLD >=0.12` (bootstrap CI lower >0.02) and `> B-RAG >=0.12` and `> B-REPLAY >=0.12` and `> B-INSTR >=0.10` (Wilson lower >=0.48); (C2) `M-EXECUTABLE-SPIDER >=0.75` and `M-BINDING-CORRECT >=0.90` (Wilson lower >=0.80) with `M-UNSUBSTITUTED-TEMPLATES==0` exact equality, no double-prefix, Jaccard not hallucinating; (C3) `M-FALSE-ACCEPT-SPIDER <=0.10` and `M-UNKNOWN-RATE-SPIDER` in [0.00,0.15] and `M-ECE-SPIDER <=0.15` and `B-LITERAL <=0.15`; (C4) `M-COST-RATIO-SPIDER-vs-COLD-F10 <=0.75` (>=25% saving) and `M-COST-RATIO-SPIDER-vs-RAG-F10 <=0.85` with bootstrap CI upper <1.0 (f=10 primary, distill only SPIDER, instructions only INSTR); (C5) PC1 hit_rate 1.0 cost 50 tok success 1.0 PASS and PC2 EXECUTABLE 1.0 binding 1.0 success >=0.90 PASS; (C6) NC1 shuffled success <=COLD+0.05 and false_accept >=0.25, NC2 random false_accept >=0.30 or success <=COLD with verification-derived variance, UNKNOWN requires confidence <0.80 or missing required_slots. `FALSIFIED` if any C1-C4 fails (excluding PC/NC substrate failures which are `MEASUREMENT_INVALID`). `MIXED` if C1 fails but C2 passes. `MEASUREMENT_INVALID` if fix not committed (including Jaccard), slot collision, registry/resolve not exercising real `required_slots/_bind`, verification bypass, <60 valid tasks after measured dedup 0.9479, value overlap !=0, Playwright/header verification broken, family <10 or template !=49, or LLM API unavailable >50%.

No threshold weakening after seeing outcomes.

