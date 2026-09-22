# EXP-PRODUCT-35752564139 — Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-35752564139
- **Lane**: product
- **Claim**: C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers" (registry status EXPERIMENTAL, owner_lanes graph/product, next_gate learn on resource A succeed on never-observed B vs cold/replay/retrieval)
- **Director mandate**: REOPEN C-PARAM-INHERIT (action REOPEN, parent_handoff_disposition SUPERSEDE, cycle 35751960273)
- **Date**: 2026-09-22
- **Status**: DESIGN — NOT YET FROZEN
- **Parent handoff**: research/experiments/EXP-PRODUCT-35741913862/handoff.json (REVISE, C-RESIDUAL-NOVELTY HYPOTHESIS at synthetic mock ceiling; superseded for this NEW governed experiment)
- **Binding strategic question** (director_mandate.question): Does a real LLM agent (same model/tools/budget) learning mechanisms on resource A succeed on never-observed resource B for multi-parameter (path+body+headers) parameterized inheritance with EXECUTABLE binding on unseen identifiers vs COLD vs instructions vs retrieval/RAG vs 0-token replay, measuring end-to-end tokens+browser+retrieval+verification+repair latency and amortized maintenance on WebArena-Verified v2 family hold-out (>=10 families, 192 tasks, 49 templates, duplication 0.9479) — demonstrating transfer beyond 5.42% synthetic single-param ceiling and reporting false_accept and UNKNOWN abstention?

This prereg converts the Director's strategic question into the smallest rigorous high-information falsifiable experiment that can change C-PARAM-INHERIT and product decisions.

## 2. Scientific Question (refined for falsifiability)

Does multi-parameter (path segment + body field + header value) parameterized mechanism induction — learning distinct parameter slots per varying field from demonstrations on resource A and registering via SpiderKernel (registry + required_slots | template_slots + _bind + confidence/freshness gating) — enable a real LLM agent with identical model/tools/budget to succeed on never-observed resource B identifiers (zero training overlap) with EXECUTABLE binding, beating COLD, instructions, retrieval/RAG, and 0-token exact replay baselines on end-to-end success and amortized cost per success, on a family hold-out evaluation (target >=10 families, 192 tasks / 49 templates per WebArena-Verified v2; minimum 60 valid tasks for decision) while maintaining false_accept <=0.10 and calibrated UNKNOWN abstention?

## 3. Background and Motivation

### 3.1 What the Codex establishes for C-PARAM-INHERIT

**Established (accepted Codex):**

- EXP-PRODUCT-33528829801 (audit PASS, decision SURVIVES synthetic POC): `distill_parameterized()` with `_extract_varying_values()` correctly induces one parameter slot for isomorphic action paths sharing common prefix/suffix and resolves EXECUTABLE with correct bound_action for all 10 unseen single-char identifiers. All four frozen decision-rule conditions satisfied. **Claim ceiling narrow**: single-parameter, single-field, common-prefix heuristic, deterministic synthetic data, hardcoded confidence 0.5, simulated baselines. 5.42% token saving ceiling referenced in Director mandate corresponds to this narrow POC (see portfolio_assessment).
- EXP-PRODUCT-33741671686 (audit PASS, MULTI-PARAM-SURVIVES): induces >=2 distinct slots for path+body and >=3 for path+body+headers (21/21 EXECUTABLE, 21/21 binding correct, 0 unsubstituted templates) with structure-similarity >=0.75 and field-path relevance. **Ceiling remains narrow**: synthetic POC implemented only in run_experiment.py (not kernel.py), single-intent deterministic observations, trivial full-replacement for body fields, tautological confidence gate, fragile positional slot-to-param mapping. **Do NOT promote to Product Core** per verdict.
- EXP-GRAPH-33816735314 (COMPETITION-SAFE) and related graph fixes: parameter-slot-count secondary tie-break eliminates 5/5 false accepts at equal confidence without breaking cold/literal/param-only baselines, but scope limited to harness.

**Rejected / bounded falsifications:**

- No broader rejection of C-PARAM-INHERIT. Prior kernel integration attempts KERNEL-INTEGRATION-FALSIFIED (EXP-PRODUCT-33974562602), FIXES-FALSIFIED (EXP-PRODUCT-33993747223, 34003641840), KERNEL-INTEGRATION-PARTIAL (EXP-PRODUCT-34015741916) show harness-only multi-param does not yet survive kernel integration with noise-field filtering — blocked at realistic-input handling, not closed globally.
- Product last direction C-RESIDUAL-NOVELTY synthetic mocks REVISE/MEASUREMENT_INVALID with hit_rate 0/100 at 0% novelty, bijective cost formula, p=0.0167 >0.01 — superseded per Director comparative_reasoning ("Supersedes synthetic residual-novelty pipeline 20/20 exact-repeat mock which is measurement-invalid").

### 3.2 Inherited continuity (parent_handoff EXP-PRODUCT-35741913862) — preserved distinctions per AGENTS.md

**Established** (carry_forward.established):
- Harness can execute SPIDER resolve/bind via actual SpiderKernel.resolve + MechanismRegistry with required_slots check, _bind, freshness (0.25) and confidence (<0.80 -> UNKNOWN) exercised (M-UNKNOWN-RATE 0.0/0.0/0.0/1.0/1.0, observations UNKNOWN at n>=0.75).
- B-LENGTH-PROPORTIONAL flat-cost falsifier reachable (rho 0.0) proving MIXED reachable.
- Descriptive synthetic costs at L=10 mock exist but not confirmatory.
- Substrate can measure 0-token replay cost (50 tok verification only) in isolation.
- Prior C-RESIDUAL-NOVELTY ceiling remains HYPOTHESIS at bounded mock; C-PRODUCT-ECON logistic REJECTED.

**Rejected** (carry_forward.rejected — bounded, not global):
- That the prior packet demonstrated SURVIVES for C-RESIDUAL-NOVELTY (C2 honest per-hit ratio 25.0 vs reported 0.239 diluted, C3 p 0.017 fails two-sided 0.01).
- That rho 0.97/R2 0.927 demonstrate work compression (deterministic gating artifact, variance 0 at 4/5 bins).
- That NC1/NC2 validated mapping/ranking (flat 5750 by construction).
- No broader rejection of residual-novelty economics globally — untested, not REJECTED.

**Unknown** (carry_forward.unknown — remains open):
- Whether 20/20 exact repeats at 0% with honest per-hit accounting would still beat RAG/REPLAY.
- Whether per-task verification variance at all bins would yield rho>=0.60 with p<0.01.
- Whether synthetic mock generalizes to WebArena-Verified DOM, cross-site transfer, or production hosting.

**Do not assume** (carry_forward.do_not_assume — high severity):
- Do not assume C-RESIDUAL-NOVELTY SURVIVES or rho 0.97 demonstrates compression.
- Do not assume SPIDER beats strong baselines at low novelty (RAG/REPLAY starved 1/20 hits).
- Do not assume NC1/NC2 proved mapping matters.
- Do not assume 5.42% saving generalizes beyond single-param narrow heuristic.
- Do not assume WebArena has official instance splits or inflated M1=0.818 (corrected 0.311).

**Director disposition**: SUPERSEDE — the parent's next_question (repaired residual-novelty pipeline with 20/20 exact repeats, verification variance) is advisory continuity only. The binding direction is the Director's REOPEN on C-PARAM-INHERIT with real LLM+Playwright+verify() vs strong baselines on family hold-out. This prereg follows the mandate and does not silently drift back to synthetic residual-novelty mock repair.

### 3.3 Why this experiment is the smallest high-information step

- **Starved claim**: C-PARAM-INHERIT 0/60 recent experiments, 37 total, last MEASUREMENT_INVALID 0/32 tasks (no LLM keys). Only narrow synthetic ceilings (5.42% single-param, harness-only 21/21 multi-param) exist — no real execution with LLM.
- **Gate prerequisite**: C-LLM-INHERIT (real LLM benefits beyond retrieval/instructions) and C-PRODUCT-ECON (amortized cost per success after retrieval/verification/maintenance) cannot advance without first validating parameterized execution on unseen identifiers (portfolio_assessment).
- **Tunnel flags consume capacity** on marginal mocks (graph 9/10 FRESHNESS, frontier 13/15 TV translation-only) with diminishing info gain — breadth on real LLM+Playwright is highest leverage.
- **Smallest falsifiable**: Family hold-out with multi-param slots directly tests the parameterized inheritance gate (A -> B). Four strong baselines (cold/instructions/RAG/0-token replay) distinguish caching vs generalization and quantify economics beyond the 5.42% ceiling. False_accept and UNKNOWN are required product safety signals (freshness/UNKNOWN abstention prior) and distinguish valid transfer from contamination.
- **Not repeating pre-2.0**: No prior experiment tested real LLM agent inheritance on WebArena-Verified families with end-to-end Playwright verification and amortized cost.

## 4. Hypothesis

H0 (null): Parameterized mechanisms induced from A do not transfer to unseen B beyond literal replay or retrieval; SPIDER success on B equals COLD/RAG/REPLAY within measurement noise, or EXECUTABLE binding fails (collision, unsubstituted ${}), or false_accept exceeds safety threshold.

H1 (alternative — this experiment's hypothesis): A multi-parameter induction mechanism with distinct slot naming per field-path (path, body.*, headers.*), structure-similarity >=0.75, field-path relevance filter, and registry storage at confidence 0.90, when executed by the same LLM agent (same model/tools/budget), achieves on never-observed B (zero value overlap for parameterized slots, family hold-out):

- **H1-success**: M-SUCCESS-SPIDER >=0.65 and > each baseline (B-COLD, B-RAG, B-REPLAY) by >=0.12 absolute, > B-INSTR by >=0.10, family-stratified bootstrap CI not overlapping
- **H1-mechanism**: M-EXECUTABLE-SPIDER >=0.75 and M-BINDING-CORRECT >=0.90 with zero unsubstituted templates
- **H1-safety**: M-FALSE-ACCEPT-SPIDER <=0.10, M-UNKNOWN-RATE on valid B in [0.00,0.15] (no excessive abstention), B-LITERAL success <=0.15 on same B
- **H1-economics**: M-AMORTIZED-COST-SPIDER at f=10 (distill 1000 tok amortized only to SPIDER) >=25% cheaper per success than B-COLD and <=0.85x B-RAG on held-out families, demonstrating transfer beyond retrieval/replay and beyond 5.42% single-param synthetic ceiling

If all H1 components hold, C-PARAM-INHERIT advances from EXPERIMENTAL (narrow synthetic) to VALIDATED at bounded real-LLM multi-param ceiling.

## 5. Falsification Criteria

Falsified if ANY primary gate fails (C1-C4 in decision_rule):

- **F1-success**: SPIDER success <0.50 or not > B-COLD by >=0.12 and not > B-RAG by >=0.12 and not > B-REPLAY by >=0.12 (no advantage over strongest memory baseline)
- **F2-mechanism**: EXECUTABLE <0.50 or binding correctness <0.70 or any EXECUTABLE contains unsubstituted `${...}`
- **F3-safety**: false_accept >0.15 or UNKNOWN miscalibrated (>0.40 on valid B, or 0.0 when should abstain leading to contamination), or B-LITERAL success >0.15 (literal already solves families, indicating template duplication 0.9479 makes parameterization unnecessary)
- **F4-economics**: amortized cost per success SPIDER >= B-COLD and >= B-RAG (no saving despite success)

MIXED if F1 fails but F2 passes (binds correctly but agent fails downstream verification/repair — mechanism quality vs agent execution separated).

MEASUREMENT_INVALID if: harness cannot induce distinct slots (collision e.g., both path.id and body.user_id -> ${id}), registry/resolve not exercising real required_slots/_bind, Playwright verification broken (no postcondition check, all success forced), <60 valid tasks after dedup 0.9479 filtering, or LLM API unavailable for >50% of trials. Infrastructure failure is not scientific falsification.

## 6. Experimental Conditions and Materials

### 6.1 Task source

- **Primary**: WebArena-Verified v2 (portfolio target: 192 tasks, 49 templates, duplication 0.9479, >=10 families). Load via repo cache (`/tmp/webarena`, `data/webarena_verified_v2.json`, or `https://github.com/web-arena-x/webarena`). Deduplicate by (template_id, intent, action_template hash); keep one exemplar per duplicate cluster. Require >=10 families with >=3 tasks each, each family has template parameterization (e.g., `https://shop.example.com/product/${product_id}`, body `{\"quantity\": ${qty}}`, header `X-CSRF: ${token}`).
- **Fallback** (disclosed ceiling): If WebArena-Verified inaccessible after 3 fetch attempts, use synthetic Flask catalog mock replicating WebArena structure (12 store instances sharing platform per EXP-INTEL-35651934683 M1=0.311 corrected, 996-task structure) as isomorphic proxy with same family/template/duplication structure and multi-param fields. Fallback logged in provenance.json and bounds claim ceiling to synthetic/WebArena-inspired mock without Docker/full-DOM complexity.

### 6.2 Family hold-out design

- For each family, partition resource pools: pool A identifiers (e.g., A_SKU_001..050, A_STORE_01..06) and pool B identifiers (B_SKU_001..050, B_STORE_07..12) with **zero exact value overlap** for parameterized slots (verified by set intersection =0). Training uses 3-5 exemplars sampled from A only (one per template variant). Test uses B only (never-observed). Families are hold-out units (not random task split) to prevent site identity leakage; hold-out families never seen during distill.
- Target: 12 families x12 tasks =144 tasks (or 16x12=192 if budget allows). **Minimum for decision**: 10 families x6 tasks =60 valid tasks after dedup/filtering. Power: n=60 per condition gives >0.80 power to detect 0.12 success delta (baseline 0.45, alpha 0.05, paired).
- Novelty is family-level (all B slots are novel), not synthetic fractional bins. The 5.42% ceiling comparison is via amortized saving, not fractional novelty.

### 6.3 Agent and kernel

- **LLM**: gpt-4o-mini-2024-07-18 (or equivalent approved: claude-3-5-haiku, gemini-1.5-flash) with temperature 0, seed 42 where supported, max 15 steps per task, max 4096 output tokens, same prompt scaffold across conditions (system prompt fixed, only memory/instructions injection varies). All conditions use identical Playwright toolset: `navigate(url)`, `click(selector)`, `fill(selector, value)`, `type`, `select`, `goBack`, `observe()` (DOM snapshot). Browser via localhost Playwright (chromium headless) on WebArena-Verified cached HTML (no external network for determinism) or Flask mock server.
- **Kernel**: harness-level `distill_parameterized()` with `_extract_varying_values()` supporting path+body+headers, distinct slot naming per field-path, structure-similarity >=0.75, field-path relevance filter (only url/path, body.*, headers.*). Mechanism per family at confidence 0.90 via actual `MechanismRegistry.write/read`. At resolve: `required_slots = set(parameter_slots) | template_slots(action_template)`; freshness `behavioral_score >=0.25` (JWT mock probe if available) and `confidence >=0.80` else UNKNOWN; if EXECUTABLE then `bound_action = _bind(template, params)` via actual `_bind` and Playwright execution + `_matches(postconditions, observed_state)` verification. On verification failure charge repair (1 LLM step, 500 tok +2 browser calls) and count false_accept if binding wrong but verification passed. Code must be kernel-integrated (`src/spider/kernel.py` or `src/spider/param_induction.py`), not only `run_experiment.py` copy, verified by audit (import path check).

## 7. Metrics (stable identities for EXECUTE/AUDIT)

All metrics are JSON keys in `result.json.metrics`:

- **Primary success** (family-stratified):
  - `M-SUCCESS-SPIDER` (float 0-1, Wilson 95% CI)
  - `M-SUCCESS-COLD`, `M-SUCCESS-INSTR`, `M-SUCCESS-RAG`, `M-SUCCESS-REPLAY`, `M-SUCCESS-LITERAL`
  - `M-SUCCESS-DELTA-SPIDER-vs-COLD`, `M-SUCCESS-DELTA-SPIDER-vs-RAG`, `M-SUCCESS-DELTA-SPIDER-vs-REPLAY` (absolute deltas with family-stratified bootstrap 95% CI)
  - `M-SUCCESS-PER-FAMILY` (dict family->success per condition)
- **Mechanism quality**:
  - `M-EXECUTABLE-SPIDER` (fraction EXECUTABLE among SPIDER attempts)
  - `M-BINDING-CORRECT` (fraction bound_action correct among EXECUTABLE, audited by exact param substitution check)
  - `M-UNSUBSTITUTED-TEMPLATES` (count of EXECUTABLE with remaining `${}`)
  - `M-BINDING-CORRECT-PER-FAMILY`
- **Safety**:
  - `M-FALSE-ACCEPT-SPIDER` (fraction EXECUTABLE where verification passed but postconditions wrong per audit, or binding wrong but marked success)
  - `M-FALSE-ACCEPT-RAG`, `M-FALSE-ACCEPT-REPLAY`
  - `M-UNKNOWN-RATE-SPIDER` (fraction UNKNOWN among SPIDER attempts, per family)
  - `M-UNKNOWN-RATE-RAG`
  - `M-ECE-SPIDER` (expected calibration error, confidence vs success)
- **Cost / economics** (tokens, browser, latency):
  - `M-TOKENS-SPIDER-PER-TASK` (mean input+output tokens per task, raw)
  - `M-TOKENS-COLD-PER-TASK`, `M-TOKENS-RAG-PER-TASK`, `M-TOKENS-REPLAY-PER-TASK`, `M-TOKENS-INSTR-PER-TASK`
  - `M-BROWSER-CALLS-SPIDER-PER-TASK`, `M-LATENCY-SPIDER-MS-PER-TASK` (and per baseline)
  - `M-RETRIEVAL-COST-SPIDER` (tokens + ms)
  - `M-VERIFICATION-COST-SPIDER` (tokens + ms)
  - `M-REPAIR-COST-SPIDER` (tokens + ms, count)
  - `M-AMORTIZED-COST-PER-SUCCESS-SPIDER-F10` ( (total_tokens + distill_tokens/f)/success_rate, f=10, distill 1000 tok only SPIDER)
  - `M-AMORTIZED-COST-PER-SUCCESS-COLD-F10`, `M-AMORTIZED-COST-PER-SUCCESS-RAG-F10`, `M-AMORTIZED-COST-PER-SUCCESS-REPLAY-F10`
  - `M-COST-RATIO-SPIDER-vs-COLD-F10` (amortized), `M-COST-RATIO-SPIDER-vs-RAG-F10`, `M-COST-RATIO-SPIDER-vs-REPLAY-F10` with bootstrap 95% CI
  - Also report f=1 and f=100 amortizations (sensitivity)
  - `M-DISTILL-TOKENS` (fixed 1000, amortized)
- **Controls**:
  - `M-PC1-HIT-RATE-REPLAY-SAME-A` (expected 1.0)
  - `M-PC1-COST-REPLAY-SAME-A` (50 tok)
  - `M-PC2-EXECUTABLE-SAME-A`, `M-PC2-BINDING-SAME-A`, `M-PC2-SUCCESS-SAME-A`
  - `M-NC1-SHUFFLED-SUCCESS`, `M-NC1-SHUFFLED-FALSE-ACCEPT`, `M-NC1-SHUFFLED-BINDING`
  - `M-NC2-RANDOM-SUCCESS`, `M-NC2-RANDOM-FALSE-ACCEPT`
  - `M-B-LITERAL-SUCCESS` (should be <=0.15)
- **Validity / diagnostics**:
  - `M-NUM-FAMILIES`, `M-NUM-TASKS-TOTAL`, `M-NUM-TASKS-PER-FAMILY`, `M-DUPLICATION-RATE` (measured duplication)
  - `M-VERIFICATION-AUROC` (if runtime verification substrate available)
  - `M-VALUE-OVERLAP-A-vs-B` (must be 0 for parameterized slots)
  - `M-LLM-CALLS-TOTAL`, `M-LLM-FAILURE-RATE` (API errors)

## 8. Controls (stable identifiers)

- **Positive control PC-PARAM-REGRESSION-AND-LITERAL-HIT** (id `PC-PARAM-REGRESSION-AND-LITERAL-HIT`):
  - PC1: 5 tasks where test identifiers == training A (same-resource). B-REPLAY must hit at 1.0 with 50 tok verification only, success 1.0 — validates 0-cost measurement and Playwright verification.
  - PC2: Multi-param same-A (3 A observations -> mechanism, test on same A pool). Must be EXECUTABLE 1.0, binding 1.0, success >=0.90. Validates induction works before generalization test.
  - Expected: both pass. Failure due to harness binding errors -> MEASUREMENT_INVALID.

- **Null controls NC-SHUFFLED-AND-RANDOM** (id `NC-SHUFFLED-AND-RANDOM`):
  - NC1 shuffled slot mapping (swap ${sku}<->${store_id}) on held-out B via real registry/_bind/verify — expected success <= COLD+0.05, false_accept >=0.25, binding <0.50.
  - NC2 random retrieval (random registry entry) — expected false_accept >=0.30 or success <= COLD.
  - Both go through actual binding/verification so they CAN fail expected pattern if mapping matters (not guaranteed flat). If NC1 success >= SPIDER -0.05, SPIDER effect is spurious.

- **Fail-able literal baseline B-LITERAL** (id `B-LITERAL`): literal mechanisms without slots must fail on B (success <=0.15), proving parameterization is necessary and duplication 0.9479 does not trivialize task.

## 9. Baselines (strong, per Director mandate)

All baselines use identical LLM/tools/budget and identical held-out B set, with costs measured in same units:

- **B-COLD** (id `B-COLD`): cold LLM, no memory. Upper-bound cost. No distill.
- **B-INSTR** (id `B-INSTR`): hand-authored instructions (200 tok amortized 200/f, f=10 -> 20 tok/task) + LLM exploration for B identifiers.
- **B-RAG** (id `B-RAG`): Jaccard retrieval (threshold 0.30) over training A trajectories, verbatim replay without parameterization, fallback to COLD on mismatch. Retrieval cost 200 tok+150ms.
- **B-REPLAY-TERX** (id `B-REPLAY-TERX`): 0-token exact replay with LLM fallback on miss (exact action_template string equality). Hit cost 50 tok verification only; miss cost = COLD.
- **B-LITERAL** included as mechanism ablation.

These are the strongest memory/instruction/replay baselines required to claim inheritance beyond "memory beating no memory" (AGENTS.md §13). Prior 5.42% ceiling was vs weak simulated baselines; this experiment vs real LLM retrieval/replay is the next gate.

## 10. Decision Rule (frozen)

**SURVIVES_CURRENT_TEST** requires ALL of (C1)-(C6) via actual LLM+Playwright pipeline:

- **C1 success margin**: `M-SUCCESS-SPIDER` >=0.65 and `M-SUCCESS-DELTA-SPIDER-vs-COLD` >=0.12 (family-stratified bootstrap 95% CI lower >0.02) and delta vs RAG >=0.12 and vs REPLAY >=0.12 and vs INSTR >=0.10. Wilson CI for SPIDER success lower >=0.55.
- **C2 mechanism**: `M-EXECUTABLE-SPIDER` >=0.75 and `M-BINDING-CORRECT` >=0.90 (Wilson lower >=0.80) and `M-UNSUBSTITUTED-TEMPLATES` ==0.
- **C3 safety**: `M-FALSE-ACCEPT-SPIDER` <=0.10 and `M-UNKNOWN-RATE-SPIDER` in [0.00,0.15] on valid B and `M-SUCCESS-LITERAL` <=0.15 on same B (literal fails, parameterization necessary).
- **C4 economics**: `M-COST-RATIO-SPIDER-vs-COLD-F10` <=0.75 (>=25% saving, bootstrap CI upper <1.0) and `M-COST-RATIO-SPIDER-vs-RAG-F10` <=0.85 (cheaper than retrievable RAG). Report f=1 and f=100 as sensitivity, but f=10 is primary (audit will check consistent amortization: distill only SPIDER, instructions only INSTR).
- **C5 controls**: `M-PC1-HIT-RATE-REPLAY-SAME-A` ==1.0 with cost 50 tok and success 1.0 PASS, and `M-PC2-EXECUTABLE-SAME-A` ==1.0 with binding 1.0 and success >=0.90 PASS.
- **C6 null controls**: `M-NC1-SHUFFLED-SUCCESS` <= B-COLD +0.05 and `M-NC1-SHUFFLED-FALSE-ACCEPT` >=0.25, and `M-NC2-RANDOM` false_accept >=0.30 or success <= COLD (verification-derived, not flat guarantee). Also `M-ECE-SPIDER` <=0.15 and UNKNOWN cases have confidence <0.80 or required_slots missing.

**FALSIFIED** if any C1-C4 fails (excluding PC/NC substrate failures which are MEASUREMENT_INVALID). **MIXED** if C1 fails but C2 passes (mechanism binds correctly but agent fails downstream — e.g., Playwright execution or verification fails — mechanism quality separated from agent execution). **MEASUREMENT_INVALID** if: induction collision (distinct fields -> same slot name), registry/resolve not exercising real required_slots/_bind (audit import check fails), verification broken (no postcondition check, all success forced 1.0), <60 valid tasks after dedup, or LLM API unavailable for >50% of trials (retry 3x per task with exponential backoff, log failures). Infrastructure failure is not scientific falsification.

Single primary outcome is C1 success margin; economics and safety are co-primary gates for product. All thresholds frozen before execution.

## 11. Measurement Validity and Threats

| # | Threat | Mitigation |
|---|--------|------------|
| 1 | LLM non-determinism / cost variance | Temperature 0, fixed seed 42, same model version pinned, family-stratified bootstrap CIs, report per-family variance. Sensitivity at ±50% token price. |
| 2 | Playwright flake / verification tautology | Deterministic postcondition `_matches` on DOM/state (not LLM-as-judge), PC1 validates verification path, report verification AUROC if runtime substrate available, sample traces. |
| 3 | WebArena duplication 0.9479 trivializes hold-out | Family hold-out (not random), zero value overlap check, B-LITERAL control must fail (<=0.15) to prove parameterization necessary; duplication rate reported. |
| 4 | Synthetic-to-real gap if WebArena inaccessible | Fallback disclosed as WebArena-inspired Flask mock with same family/template/duplication structure; claim ceiling bounded to mock, not production. Logged in provenance. |
| 5 | Slot collision (prior harness bug) | Distinct slot naming per field-path (not hardcoded `id`), audit checks slot distinctness, NC1 shuffled must elevate false_accept. |
| 6 | Amortization dishonesty (prior VF-C2-PER-HIT-VS-MEAN) | Distill 1000 tok added only to SPIDER, instructions 200 tok amortized only to INSTR, per-task and amortized reported separately with same-unit bootstrap CIs. |
| 7 | LLM API / cost blocking | Retry 3x per task, fallback to MEASUREMENT_INVALID if >50% fail (not falsification), budget cap $60, early abort if cost exceeds estimate with receipt. |
| 8 | Site identity leakage | Family hold-out, no cross-family retrieval; audit checks retrieved mechanism family == test family would be leak (should be mismatch on hold-out). |
| 9 | Confidence miscalibration / UNKNOWN gaming | Report ECE, UNKNOWN rate per family, and that UNKNOWN requires confidence <0.80 or missing required_slots (not deterministic gating at 0.75 threshold as in parent). |

Representation loss and validity notes will be disclosed per AGENTS.md §17-18: what observables are preserved (DOM, action target, browser events) and what is abstracted.

## 12. Procedure (step-by-step, no outcome inspection)

1. **Census**: Load WebArena-Verified v2 task definitions (or Flask mock fallback). Deduplicate, count families/templates/duplication, verify >=10 families with >=3 tasks and A/B disjoint pools. Log hashes.
2. **Split**: For each family, sample 3-5 A exemplars for training, hold out 6-12 B tasks for test. Verify value overlap =0 for parameterized slots. Seed 42.
3. **Distill**: For each family, call `distill_parameterized()` on A exemplars, induce distinct slots per varying field (path+body+headers), store mechanism per family at confidence 0.90 via actual registry.
4. **Agent runs**: For each test task, run all 5 conditions (SPIDER/COLD/INSTR/RAG/REPLAY) with same LLM/tools/budget (15 steps, Playwright). SPIDER condition injects family mechanism via `resolve(intent, context, params)` with B params; others inject per baseline. Measure tokens, browser calls, latency, verification, UNKNOWN, false_accept.
5. **Controls**: Run PC1 (5 same-A replay hits), PC2 (multi-param same-A), NC1 shuffled, NC2 random, B-LITERAL on same B set, all via real pipeline.
6. **Logging**: Per-task CSV with all metrics, registry JSON, cost_config, Playwright trace samples, provenance (model version, prompts, seeds, hashes).
7. **Analysis**: Compute stable metrics (M-*) with family-stratified bootstrap, Wilson CIs, McNemar paired tests. Apply frozen decision_rule. No post-hoc threshold tuning.

## 13. Consequences

### If SURVIVES

- C-PARAM-INHERIT advances from EXPERIMENTAL (5.42% single-param synthetic + harness-only 21/21) to VALIDATED at bounded real-LLM multi-param ceiling (family hold-out, path+body+headers, real Playwright verification, beats cold/instructions/retrieval/0-token replay with false_accept <=0.10). Establishes first audited evidence that multi-parameter mechanisms learned on A generalize to unseen B via EXECUTABLE binding.
- Unblocks C-LLM-INHERIT (real LLM inheritance vs strong baselines gate) and C-PRODUCT-ECON (amortized economics) for Docker full-DOM scale-up. Quantifies saving vs TERX exact-replay dominance (SPIDER wins where replay misses, within 2x where replay hits).
- Authorizes kernel promotion of distinct-slot `distill_parameterized` to `src/spider/kernel.py` (promotion_ready=true, pending kernel tests). No SHIPPED until replication on production hosting and freshness hardening.

### If FALSIFIED (or MIXED)

- C-PARAM-INHERIT remains EXPERIMENTAL at narrow synthetic ceiling (or bounded REJECTED for multi-param real-LLM setting). If MIXED (binds but no success margin), mechanism quality separates from agent execution — next action is agent/verification repair, not induction redesign.
- If SPIDER not beating RAG/REPLAY on family hold-out (where replay hits ~0), multi-param inheritance adds no economics beyond retrieval/replay, supporting caching-vs-generalization tension that exact replay dominates at this template duplication. Product must pivot to C-FRESHNESS (freshness guards, UNKNOWN abstention, distributed session per Director dependencies runtime), C-DELTA-REPAIR (localized repair on verified nginx HIT/SWR/SIE substrate per runtime), or C-SEMANTIC-RESOLVE (calibrated resolution) and defer C-PRODUCT-ECON scale-up.
- If MEASUREMENT_INVALID (collision, verification broken, <60 tasks, LLM unavailable), priority is fixing kernel integration and runtime verification AUROC substrate before re-testing param-inherit — do not weaken prereg after outcomes.

Both positive and negative outcomes are high-information: they definitively inform whether parameterized inheritance justifies productization vs redirection after 37 total attempts.

## 14. Analysis Plan

- **Primary**: Family-stratified paired comparison of SPIDER success vs each baseline (McNemar + bootstrap delta CI). Success requires > baseline by frozen margins with CI lower >0 (C1).
- **Mechanism**: EXECUTABLE rate and binding correctness with Wilson CIs; check zero unsubstituted templates (C2).
- **Safety**: False_accept and UNKNOWN rate with Wilson CIs; B-LITERAL must be <=0.15 (C3).
- **Economics**: Amortized cost per success at f=10 (distill only SPIDER) with family-stratified bootstrap cost ratio CI (C4). Sensitivity at f=1/100.
- **Controls**: PC1/PC2 must pass; NC1/NC2 must show expected null pattern (C5-C6). Audit recomputes all M-* from raw per-task CSV and registry.
- **Diagnostics**: Report per-family breakdown, duplication rate, value overlap, verification AUROC/ECE, token/browsing/latency decomposition, Playwright failure taxonomy.

## 15. Deviation Policy

Any deviation from this preregistration (e.g., changing family split, adding LLM calls, tuning thresholds after seeing outcomes) will be labeled **EXPLORATORY** and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration and untouched evidence (AGENTS.md §17-19, EXPERIMENT_PACKET invariants). If mandate infeasible (e.g., WebArena inaccessible and Flask fallback also fails), fail loudly with failure.json (DO NOT invent substitute direction) per POLICY.md.

## 16. Freeze Statement

This preregistration is frozen BEFORE any outcome-bearing measurement (no LLM agent runs, no Playwright executions, no binding success readouts). The experiment will be executed exactly as specified in `spec.json` and this `prereg.md`; `freeze.json` will hash request/spec/prereg before execution begins. EXECUTE may not mutate frozen inputs.

## 17. References to Packet and Charter

- Lane charter: `research/lanes/registry.json` product — "Turn audited capabilities into coherent external-agent product and continuously test product economics"
- Claim registry: `research/claims/registry.json` C-PARAM-INHERIT — next_gate "learn on resource A, succeed on never-observed B against cold/replay/retrieval baselines"
- Director mandate: `request.json` director_mandate REOPEN C-PARAM-INHERIT with agent priors (freshness/UNKNOWN, strong baselines, deterministic verification + delta-repair, exploration/exploitation) distinguished from SPIDER evidence
- Parent handoff: `research/experiments/EXP-PRODUCT-35741913862/handoff.json` (preserved established/rejected/unknown/do_not_assume per AGENTS.md)
- Dependencies: intel WebArena-Verified v2 family census + AX consistency fix, runtime verification AUROC + byte-preserving replay substrate (Director dependencies)
- Validity gates: AGENTS.md §§17-18 (target/split/sampling/uncertainty/representation integrity), EXPERIMENT_PACKET.md §3-4 (spec/result shapes), POLICY.md (Global Director REOPEN supersedes local next_question)

