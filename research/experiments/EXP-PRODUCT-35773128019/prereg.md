# EXP-PRODUCT-35773128019 — Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-35773128019
- **Lane**: product (allowed_code_roots `src`, `tests`, `sdk`, `pyproject.toml`)
- **Claim**: C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers" (registry status EXPERIMENTAL, owner_lanes graph/product, next_gate learn on resource A succeed on never-observed B against cold/replay/retrieval baselines; informs C-RESIDUAL-NOVELTY and C-PRODUCT-ECON per Director comparative reasoning)
- **Director mandate**: CONTINUE C-PARAM-INHERIT (action CONTINUE, parent_handoff_disposition USE, cycle 35772373047, comparative_reasoning prioritizes corrected distill_parameterized family hold-out over C-RESIDUAL-NOVELTY bijective-cost economics and C-FRESHNESS mock because no live-browser inheritance demonstrated and 0-token TERX remains honest baseline, cognitive_reset false)
- **Date**: 2026-09-22
- **Status**: DESIGN — NOT YET FROZEN (freeze.json will hash request/spec/prereg before EXECUTE)
- **Parent handoff**: research/experiments/EXP-PRODUCT-35756243655/handoff.json (MEASUREMENT_INVALID, sha256 92869eb23ba40845288653564771d9593678a2854e28e59dc8fac8a1c14751d9)
- **Binding strategic question** (director_mandate.question verbatim): Does a corrected kernel-integrated distill_parameterized (fixing _common_prefix_and_suffix double-prefix so full B identifiers bind correctly, plus field-path relevance filter and Jaccard>=0.75 constant-anchor check) enable a real LLM agent (gpt-4o-mini, 15 steps, Playwright, 4096 tokens, temp 0, seed 42) on true WebArena-Verified v2 family hold-out (>=10 families, >=60 tasks, 49 templates, duplication 0.9479, param_task 0.8958) to achieve EXECUTABLE>=0.75 and binding correctness>=0.90 with zero unsubstituted templates, success margin>=0.12 vs B-COLD/B-RAG/B-REPLAY/B-INSTR, false_accept<=0.10, UNKNOWN in [0.00,0.15] with ECE<=0.15, and honest amortized saving>=25% vs COLD and <=0.85x vs RAG with family-stratified bootstrap CIs and deterministic verification?

This prereg converts that binding question into the smallest rigorous falsifiable experiment that can change C-PARAM-INHERIT and product decisions. It does not drift back to the parent's advisory next_question except as continuity evidence, per AGENTS.md and EXPERIMENT_PACKET.md.

## 2. Scientific Question (refined for falsifiability)

Does a committed kernel fix to `distill_parameterized()` in `src/spider/kernel.py` — correcting `_common_prefix_and_suffix` double-prefix handling so that training on A values (e.g., `A_SKU_00_000`) yields template `${sku}`-style (prefix/suffix from longest common prefix/suffix of A pool only) and binding full B identifiers (e.g., `B_SKU_00_000`) substitutes the varying middle without retaining prefix duplication, with distinct slot naming per field-path and Jaccard>=0.75 constant-anchor plus field-path relevance filtering to prevent spurious slot hallucination — enable a real LLM agent with identical model/tools/budget to succeed on never-observed B identifiers (zero value overlap, family hold-out) with EXECUTABLE binding, beating cold, instructions, RAG, and 0-token exact replay on success and honest amortized cost, while maintaining calibrated abstention and honor header/body/status provenance?

Minimality: single family-hold-out with multi-param slots (path+body+headers) on WebArena-Verified v2 directly tests the parameterized inheritance gate (A->B) that blocks C-LLM-INHERIT, C-RESIDUAL-NOVELTY and C-PRODUCT-ECON. Four strong baselines distinguish caching vs generalization; 0-token TERX is the hardest economics baseline (hits at 0% on hold-out only if design is valid). Jaccard>=0.75 and field-path relevance are the minimal guards against tautological cost definitions flagged in Director agent_priors.

## 3. Background and Motivation

### 3.1 What the Codex establishes

**Established (accepted Codex, ceiling narrow):**

- EXP-PRODUCT-33528829801 (audit PASS, SURVIVES synthetic POC): `distill_parameterized()` with `_extract_varying_values()` induces one parameter slot for isomorphic action paths and resolves EXECUTABLE with correct bound_action for 10 unseen single-char identifiers. 5.42% token saving ceiling is this narrow POC, not product economics.
- EXP-PRODUCT-33741671686 (audit PASS, MULTI-PARAM-SURVIVES): induces >=2 distinct slots path+body and >=3 path+body+headers, 21/21 EXECUTABLE 21/21 binding correct 0 unsubstituted templates, but harness-only in `run_experiment.py` not kernel, deterministic synthetic, fragile positional mapping. Do NOT promote.
- EXP-GRAPH-33816735314 (COMPETITION-SAFE) and related: parameter-slot-count secondary tie-break eliminates 5/5 false accepts at equal confidence on synthetic, but scope limited and fix not committed to HEAD in many later attempts (BLOCKED closures).
- Intel census EXP-INTEL-35749371101 (audit PASS): WebArena-Verified v2 extended to element-pattern level validated separately — 192 tasks, 49 templates, 36 families, duplication 0.9479, exact_copy 0.0781, param_task 0.8958, AX_consistency 0.9 on 20 live CDP trees across 10 families (1280x720) — but NOT yet tested in product family hold-out (portfolio_assessment: census validated, no live inheritance measured).
- Runtime narrow successes on Flask/JWT + runtime EXP-RUNTIME-35764329925 header/body/status discrimination matrix for verify() establish measurement-valid substrate for header+body+status discrimination but bounded to localhost/controlled; no validated header/body+query mixed multi-channel yet (Director prior #4).
- Codex has one narrow EXPERIMENTAL substrate C-MEAS-VALID (oracle-free but bootstrap degenerate) and no validated production freshness substrate (distribution TN=0.667).

**Rejected / bounded falsifications:**

- No global rejection of C-PARAM-INHERIT. Prior kernel integration attempts repeatedly falsified on realistic inputs: KERNEL-INTEGRATION-FALSIFIED (33974562602: 6/13 fail, double-prefix 0.0, noise spurious slots), FIXES-FALSIFIED (33993747223: Fix B filters genuine body fields, Fix C threshold 0.3 too low), KERNEL-INTEGRATION-PARTIAL (34015741916: 9/10 pass but C2 double-prefix dead code), and 5 MEASUREMENT_INVALID closures for non-commit of fix (most recently EXP-PRODUCT-35756243655 with 0/72 binding correctness due to A_SKU_00_00${sku} double-prefix).
- Product economics C-PRODUCT-ECON REJECTED after 6 vacuous extrapolations (logistic saturates 0.5654 = constant null), token savings 5.42% analytically fragile, residual-novelty cost tautologically bijective and TERX/RAG baselines structurally blocked (Director prior #2).
- C-WEB-DYNAMICS HYPOTHESIS after 61 attempts; C-FRESHNESS orthogonality r~0.02 on mock but kernel freshness_check r=-0.53 degenerate Phase B.

### 3.2 Inherited continuity (parent EXP-PRODUCT-35756243655) — preserved distinctions per AGENTS.md

**Established** (carry_forward.established — only what packet justifies):

- C-PARAM-INHERIT remains EXPERIMENTAL at narrow ceilings only: EXP-PRODUCT-33528829801 audit PASS single-param in-kernel POC (10 single-char identifiers, EXECUTABLE 1.0 binding 1.0, 5.42% analytical saving, 4/4 gates) and EXP-PRODUCT-33741671686 audit PASS harness-only multi-param 21/21 EXECUTABLE 21/21 binding 1.0 0 unsubstituted — this packet provides zero live-browser family hold-out evidence (audit claim_ceiling, result status MEASUREMENT_INVALID, recomputed_metrics null).
- Committed-code synthetic single-slot Fix1(suffix guard)/Fix2(delimiter-bound)/Fix3(protocol-only) ceiling with prefix metadata remains narrow VALIDATED synthetic only (recent codex Fix3 audit PASS: P1/G1/G2/G3/G5 binding 1.0, nulls 0) — not advanced by this packet.
- WebArena-Verified v2 census separately validated (EXP-INTEL-35749371101 audit PASS: 192/49/36 duplication 0.9479 param_task 0.8958 AX 0.9 on 20 CDP trees 1280x720) but NOT tested in this packet's family hold-out (raw /tmp/opencode/webarena-verified.json 812/190 dup~0.766 not validated v2 per provenance and audit V3).
- Base SpiderKernel substrate valid: src/spider/kernel.py sha 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61 lines 132 with distill/resolve/verify/invalidate/observe and helpers _matches/_template_slots/_bind, tests/test_kernel.py 3/3 pass — but distill_parameterized and helpers absent.
- Infrastructure-failure classification validated: LLM API unavailable >50% correctly yields MEASUREMENT_INVALID not falsification (AGENTS.md failure discipline).

**Rejected** (bounded, not global):

- That this packet demonstrated SURVIVES for C-PARAM-INHERIT multi-param real-LLM transfer (no EXECUTABLE/binding/success/cost measured; result metrics null).
- That synthetic constants (prior packet M-TOKENS 50/5000/200/50/20 latency 0 ratio 0.010) demonstrate economics — bounded rejection as hardcoded not measured; this packet correctly reports no ratios and avoids denominator bug.
- That current _common_prefix_and_suffix on full identifiers yields correct templates for disjoint A/B pools — bounded rejection as implemented would produce A_SKU_00_00${sku} double-prefix A_SKU_00_00B_SKU_00_000 (parent audit 0/72).
- That raw /tmp/opencode/webarena-verified.json (812 tasks 190 templates dup~0.766) represents WebArena-Verified v2 diversity (192/49/36 0.9479/AX 0.9/param_task 0.8958) — bounded as raw mock only.
- That LLM API unavailability is scientific falsification — rejected: MEASUREMENT_INVALID per spec and AGENTS.md.

**Unknown** (carry_forward.unknown — remains open, this experiment aims to close):

- Does corrected _common_prefix_and_suffix with Jaccard>=0.75 anchor on disjoint A/B pools achieve EXECUTABLE>=0.75 and binding>=0.90 with zero ${} and exact expected_bound_action equality?
- What is real LLM success on held-out B for SPIDER vs B-COLD/B-INSTR/B-RAG/B-REPLAY with identical gpt-4o-mini temp0 seed42 15 steps 4096 tokens Playwright and deterministic _matches on header/body/status provenance?
- What is honest amortized cost per success at f=10 (distill 1000 tok only SPIDER, instr 200/f only INSTR, retrieval 200 tok verification 50 tok repair 500 tok+2 calls) and does SPIDER achieve >=25% saving vs COLD and <=0.85x vs RAG with family-stratified bootstrap?
- What are false_accept and UNKNOWN abstention rates with correct _matches postconditions and ECE<=0.15, and does UNKNOWN correctly abstain when confidence <0.80 or required_slots missing?
- Can family hold-out on true WebArena-Verified v2 (192/49/36 0.9479 param_task 0.8958 AX0.9) be loaded with >=10 families >=60 tasks and zero value overlap A∩B=0 and does multi-param transfer generalize with field-path relevance?
- Does kernel survive Jaccard>=0.75 anchor and structure_similarity >=0.75 without spurious slot hallucination on real browser observations?
- Is freshness guard behavioral_score >=0.25 and confidence >=0.80 -> UNKNOWN calibrated with ECE <=0.15 required vs excessive abstention?

**Do not assume** (carry_forward.do_not_assume — high severity, must not be silently reintroduced):

- Do not assume M-SUCCESS 1.0, EXECUTABLE 1.0, binding 1.0, false_accept 0.0, UNKNOWN 0.0 are empirical for this packet — they are null (no measurement); prior packet 1.0 values were synthetic with verification bypass (run_experiment.py:237,304) and recomputed 0/72.
- Do not assume EXECUTABLE implies correct binding or task success — required_slots check necessary not sufficient; zero ${} trivially true with wrong prefix retained.
- Do not assume baseline successes 0.0 or token costs 5000/200/50/20 are measured — previous hardcoded constants, this packet correctly reports NOT_MEASURED.
- Do not assume cost ratio 0.010 or any ratio from this packet is economic evidence — no ratios measured, prior ratio had denominator bug uses SPIDER success for COLD inf.
- Do not assume raw 812-task file demonstrates 49-template 36-family hold-out or measured duplication 0.9479 param_task 0.8958 — duplication ~0.766 vs 0.9479, template_count 190 vs 49, no family A/B disjoint proof.
- Do not assume src/spider/kernel.py currently contains distill_parameterized/_common_prefix_and_suffix — sha 46929b3a has only base class; fix must be committed and hash-verified before re-execution.
- Do not assume infrastructure failure (LLM API unavailable, Playwright no browsers) is scientific FALSIFIED — per spec MEASUREMENT_INVALID and AGENTS.md failure discipline it is not negative evidence.
- Do not assume future economics without per-family induction via registry at confidence 0.90 and family-stratified Wilson/bootstrap CIs for C1-C6 gating — spec requires one mechanism per family via required_slots/_template_slots/_bind and honest amortization (distill only SPIDER, instructions only INSTR), plus Jaccard>=0.75 prevents tautological 0% novelty cost.

**Director disposition**: USE (not SUPERSEDE ignoring parent, but also not silently overriding CONTINUE). The Director's CONTINUE is binding; parent handoff is continuity evidence. This design preserves parent's four-way distinctions above while executing the Director's question exactly, adding the Jaccard>=0.75 and runtime header/body/status dependency that were flagged as missing guards.

### 3.3 Why this experiment is the smallest high-information step

- **Starved claim**: C-PARAM-INHERIT 0/60 recent, 37 total, last MEASUREMENT_INVALID 0/72 binding correctness, prior ceiling only narrow synthetic (5.42% single-param, harness-only 21/21) — no live-browser inheritance demonstrated despite WebArena census validated (192/49/36). Closing EXECUTABLE>=0.75/binding>=0.90 with zero templates is minimal viable falsifier before any honest residual-novelty economics (matched 0/25/50/75/100% novelty with block-permutation p<0.01 and 0-token TERX that hits at 0%) can be interpreted (Director rationale).
- **Gate prerequisite**: C-RESIDUAL-NOVELTY (novelty fraction -> work compression), C-PRODUCT-ECON (amortized saving) and C-LLM-INHERIT depend on param inheritance succeeding first; prioritizing param holdout tests the blocking gate vs orthogonal freshness kernel promotion where r~0.02 on mock but r=-0.53 degenerate pooled (Director comparative reasoning: vs jumping directly to economics would be uninterpretable while binding still fails and cost is bijective).
- **Tunnel flags**: runtime 43-experiment decompression tunnel and physics estimator cycling vs continuing immediate child — distinguished as justified cognitive reset. Prior suggests fixing only hash-fragment SPAs misses heterogeneity; mixed multi-channel header+body+query tests required (runtime dependency). This experiment uses header/body/status provenance per runtime 960/960 matrix.
- **Smallest falsifiable**: Fixing double-prefix in committed kernel + Jaccard>=0.75 anchor + field-path relevance + family hold-out with deterministic header/body/status verification and 4 strong baselines directly upgrades MEASUREMENT_INVALID -> valid SURVIVES or FALSIFIED/MIXED, determining PRODUCT_CORE per Director rationale "missing direct test of SPIDER's central promise" and whether to redirect to C-FRESHNESS/C-DELTA-REPAIR/C-SEMANTIC-RESOLVE.
- **Not repeating pre2**: No prior experiment tested corrected kernel-integrated multi-param induction with true WebArena-Verified v2 family hold-out (36 families, 49 templates, param_task 0.8958), real LLM tool-calling, header/body/status HIT provenance, Jaccard>=0.75 constant-anchor, field-path relevance and honest amortization vs TERX-equivalent 0-token replay where 0-token actually hits at 0% — all novel vs pre2.
- **Agent priors distinguished**: Path dependence/local optima, residual-novelty tautology, calibration/ECE gate, orthogonal DOM/header/body channels — used only to guard against drift, per director_mandate.agent_priors_used, not as SPIDER evidence.

### 3.4 Dependencies (Director allocation.dependencies — must be satisfied or disclosed)

- intel: WebArena-Verified v2 family stratification (192 tasks, 49 templates, 36 families, param_task 0.8958, duplication 0.9479 measured, AX 0.9 longest-prefix on 20 CDP trees at 1280x720, EXP-INTEL-35749371101 PASS). Must load via /tmp/webarena or verified CSV; log 3 fetch attempts if inaccessible; duplication 0.9479 param_task 0.8958 measured not hardcoded, 49 templates logged.
- runtime: header/body/status discrimination matrix for verify() via _matches(postconditions, observed DOM/response) with HIT/SWR/SIE/304 discrimination — required for deterministic verification and freshness behavioral_score >=0.25 (spec measurement_validity[3][6]), and mixed header+body+query channel heterogeneity (Director prior #4).
- graph: committed kernel fix for _common_prefix_and_suffix double-prefix (distinct slot per field-path path/body/headers, structure_similarity >=0.75, field-path relevance, Jaccard>=0.75 constant-anchor, template prefix+${slot}+suffix, binding full B identifiers without double-prefix) in src/spider/kernel.py — audit import+hash verification not monkey-patch.

If mandate infeasible (WebArena inaccessible, LLM keys unavailable, nginx/header substrate unavailable), fail loudly with failure.json (DO NOT invent substitute direction) per POLICY.md.

## 4. Hypothesis

H0 (null): Corrected kernel still does not enable transfer; SPIDER success on B equals COLD/RAG/REPLAY/INSTR within noise, or EXECUTABLE/binding fails (double-prefix residual, slot collision, Jaccard<0.75 hallucination, field-path filter false negative), or false_accept exceeds threshold, or saving not achieved, or header/body/status verification shows no discrimination beyond body.

H1 (alternative — this experiment): A committed fix that extracts longest common prefix/suffix from A pool only (not full identifiers across disjoint pools), builds template `prefix + ${slot} + suffix` per field-path with distinct slot names, Jaccard>=0.75 constant-anchor guard and field-path relevance filter (only url/path, body.*, headers.*), and binds by substituting varying middle (handling full B identifiers correctly, no `A_SKU_00_00B_SKU_00_000`, structure_similarity>=0.75), stored per family at confidence 0.90, when executed by same LLM agent (gpt-4o-mini-2024-07-18, temp 0, seed 42, 15 Playwright steps, 4096 tokens) via `resolve()` + `_matches` verification on header/body/status provenance per runtime matrix, achieves on held-out B (zero value overlap, family hold-out, 49 templates, 36 families, duplication 0.9479 param_task 0.8958 measured, AX 0.9):

- **H1-mechanism**: M-EXECUTABLE-SPIDER >=0.75, M-BINDING-CORRECT >=0.90 (exact equality), M-UNSUBSTITUTED-TEMPLATES ==0
- **H1-success**: M-SUCCESS-SPIDER >=0.60 and > each baseline B-COLD/B-RAG/B-REPLAY by >=0.12, > B-INSTR by >=0.10 (family-stratified bootstrap 95% CI lower >0.02)
- **H1-safety**: M-FALSE-ACCEPT-SPIDER <=0.10, M-UNKNOWN-RATE-SPIDER in [0.00,0.15], M-ECE-SPIDER <=0.15, M-SUCCESS-LITERAL <=0.15
- **H1-economics**: M-COST-RATIO-SPIDER-vs-COLD-F10 <=0.75 (>=25% saving) and M-COST-RATIO-SPIDER-vs-RAG-F10 <=0.85, bootstrap CI upper <1.0, distill 1000 tok only SPIDER, f=10 primary (f=1/100 sensitivity), verification discriminates header/body/status beyond body-only per runtime.

If all hold, C-PARAM-INHERIT advances EXPERIMENTAL -> VALIDATED at bounded real-LLM multi-param ceiling; unblocks C-LLM-INHERIT, C-PRODUCT-ECON and C-RESIDUAL-NOVELTY scale-up.

## 5. Falsification Criteria

Falsified (status COMPLETE outcome FALSIFIES) if any primary gate C1-C4 fails under valid measurement:

- **F1-mechanism**: EXECUTABLE <0.75 or binding correctness <0.90 (Wilson lower <0.80) or any EXECUTABLE contains `${...}` or Jaccard hallucination persists.
- **F2-success**: SPIDER success <0.60 or not > B-COLD by >=0.12 and not > B-RAG by >=0.12 and not > B-REPLAY by >=0.12 or not > B-INSTR by >=0.10 (family-stratified bootstrap CI includes 0).
- **F3-safety**: false_accept >0.15 or UNKNOWN on valid B outside [0.00,0.15] or ECE >0.15 or B-LITERAL success >0.15 or header/body/status false_accept not gated.
- **F4-economics**: amortized cost ratio vs COLD >0.75 (saving <25%) or vs RAG >0.85 (CI crossing 1.0) or TERX 0-token baseline still dominates despite correct binding.

MIXED if F2 fails but F1 passes (mechanism binds correctly per exact equality but downstream agent/verification/repair fails — separates induction quality from execution).

MEASUREMENT_INVALID (status MEASUREMENT_INVALID, not falsification, per AGENTS.md) if: kernel fix not committed to src/spider/kernel.py (audit hash/import fails, monkey-patch only including missing Jaccard check); distinct-slot collision; registry/resolve not exercising real required_slots/_bind; verification bypass (no _matches on header/body/status, forced True, bypass table shows true binding 0/72 case); <60 valid tasks after dedup/filtering where duplication 0.9479 param_task 0.8958 is hardcoded not measured; value overlap A∩B !=0 for parameterized slots; Playwright verification broken (no DOM/response or no header/body/status discrimination per runtime dependency); family count <10 or template_count !=49; LLM API unavailable >50% after 3x backoff (distinguish from valid negative). No threshold weakening after seeing outcomes.

Single primary outcome is C1 success margin together with C2 mechanism quality; economics/safety are co-primary gates for product. Header/body/status discrimination is co-validity (runtime dependency).

## 6. Experimental Conditions and Materials

### 6.1 Task source

- **Primary**: WebArena-Verified v2 (192 tasks, 49 templates, 36 families, duplication 0.9479 measured, param_task 0.8958, exact_copy 0.0781, AX 0.9 longest-prefix on 20 CDP trees at 1280x720, PC1_WEB_SEARCH PASS via EXP-INTEL-35749371101). Load via repo cache (/tmp/webarena, data/webarena_verified_v2.json, or verified CSV). Deduplicate by (template_id, intent, action_template hash); keep one per duplicate cluster. Require >=10 families with >=3 tasks each, each template has parameterization (path, body, headers) mixed channels. Log 3 fetch attempts if inaccessible, source hash in provenance.json. Measured duplication/param_task (not hardcoded) and AX mapping proof logged.
- **Disclosure**: If WebArena-Verified inaccessible after 3 attempts, fallback to disclosed Flask mock replicating same family/template/duplication structure is NOT acceptable as proof for product promotion; this experiment requires true WebArena-Verified v2 family hold-out — fallback would make claim ceiling bounded to mock and decision would be MEASUREMENT_INVALID for product gate (different from prior synthetic fallback that was MEASUREMENT_INVALID anyway). Prefer BLOCKED with failure.json over silent mock-as-real.

### 6.2 Family hold-out design

- For each family, partition resource pools: pool A identifiers (e.g., A_SKU_001..050, A_STORE_01..06) and pool B identifiers (B_SKU_001..050, B_STORE_07..12) with zero exact value overlap for parameterized slots (verified value set intersection =0 per family, logged). Training uses 3-5 exemplars from A only (one per template variant). Test uses B only (never-observed). Families are hold-out units (not random task split) to prevent site identity leakage; hold-out families never seen during distill; retrieved mechanism family must be test family (otherwise leak). Target 12 families x6-10 tasks =72-120 tasks; minimum for decision 10 families x6 tasks =60 valid tasks after dedup/filtering. Power: n=60 per condition gives >0.80 power to detect 0.12 delta (baseline 0.45, alpha 0.05, paired).
- Novelty is family-level (all B slots novel). Duplication 0.9479 param_task 0.8958 is measured and B-LITERAL control must still fail (<=0.15) to prove parameterization necessary — if B-LITERAL succeeds, task is trivial at this duplication and hold-out design is invalid. 49 templates validates heterogeneity beyond single-template mock (parent had template_count 1).

### 6.3 Agent and kernel

- **LLM**: gpt-4o-mini-2024-07-18, temperature 0, seed 42 where supported, max 15 steps per task, max 4096 output tokens, fixed system prompt scaffold across conditions (only memory/instructions injection varies). All conditions use identical Playwright toolset: `navigate(url)`, `click(selector)`, `fill(selector,value)`, `type`, `select`, `goBack`, `observe()` (DOM/CDP snapshot at 1280x720 plus header/body/status provenance per runtime matrix). Browser via Playwright chromium headless on WebArena-Verified cached HTML + header/body/status provenance layer (or localhost nginx lifecycle as bounded ceiling if CDN HIT not available, disclosed). 30s/step timeout.
- **Kernel**: committed `src/spider/kernel.py` `distill_parameterized()` + helpers (`_common_prefix_and_suffix` corrected to handle disjoint A/B pools without double-prefix, `_field_path_to_slot_name` distinct per field-path, `_extract_varying_values` with Jaccard>=0.75 constant-anchor, structure_similarity >=0.75, field-path relevance filter only url/path, body.*, headers.*). One parameterized mechanism per family at confidence 0.90 via actual `MechanismRegistry` write/read. At resolve: `required_slots = set(parameter_slots) | _template_slots(action_template)`; freshness `behavioral_score >=0.25` (header/body/status probe if available) and `confidence >=0.80` else UNKNOWN (with ECE calibration); if UNKNOWN -> fallback to COLD LLM cost; if EXECUTABLE -> `bound_action = _bind(template, params)` via committed `_bind` (full-value B handling) and Playwright execution + `verify()` via `_matches(postconditions, observed_state)` on actual DOM/response header/body/status. On verification failure charge repair (1 LLM step 500 tok +2 browser calls) and count false_accept if binding wrong but verification passed. Code path must be kernel-integrated, not only `run_experiment.py` copy — audit verifies import path and hash and that Jaccard>=0.75 prevents hallucination.

## 7. Metrics (stable identities for EXECUTE/AUDIT — must appear in result.json.metrics)

- **Primary success (family-stratified)**:
  - `M-SUCCESS-SPIDER` (float 0-1, Wilson 95% CI), `M-SUCCESS-COLD`, `M-SUCCESS-INSTR`, `M-SUCCESS-RAG`, `M-SUCCESS-REPLAY`, `M-SUCCESS-LITERAL`
  - `M-SUCCESS-DELTA-SPIDER-vs-COLD`, `vs-RAG`, `vs-REPLAY`, `vs-INSTR` (absolute deltas with family-stratified bootstrap 95% CI, 5000 resamples)
  - `M-SUCCESS-PER-FAMILY` (dict family->success per condition)
- **Mechanism quality**:
  - `M-EXECUTABLE-SPIDER` (fraction EXECUTABLE among SPIDER attempts)
  - `M-BINDING-CORRECT` (fraction bound_action exact equality among EXECUTABLE, audit exact expected_bound_action check, no double-prefix residual, Jaccard anchor verified)
  - `M-UNSUBSTITUTED-TEMPLATES` (count EXECUTABLE with remaining `${}`)
  - `M-BINDING-CORRECT-PER-FAMILY`, `M-VALUE-OVERLAP-A-vs-B` (must 0)
- **Safety / abstention / calibration**:
  - `M-FALSE-ACCEPT-SPIDER` (EXECUTABLE where verification passed but postconditions wrong per header/body/status _matches, or binding wrong but marked success), `M-FALSE-ACCEPT-RAG`, `M-FALSE-ACCEPT-REPLAY`
  - `M-UNKNOWN-RATE-SPIDER` (fraction UNKNOWN among SPIDER attempts, per family), `M-UNKNOWN-RATE-RAG`
  - `M-ECE-SPIDER` (expected calibration error, confidence vs success)
- **Cost / economics (tokens, browser, latency)**:
  - `M-TOKENS-SPIDER-PER-TASK` (mean input+output per task raw), `M-TOKENS-COLD-PER-TASK`, `M-TOKENS-RAG-PER-TASK`, `M-TOKENS-REPLAY-PER-TASK`, `M-TOKENS-INSTR-PER-TASK`
  - `M-BROWSER-CALLS-SPIDER-PER-TASK`, `M-LATENCY-SPIDER-MS-PER-TASK` (and per baseline)
  - `M-RETRIEVAL-COST-SPIDER` (tokens+ms), `M-VERIFICATION-COST-SPIDER` (header/body/status), `M-REPAIR-COST-SPIDER` (count)
  - `M-AMORTIZED-COST-PER-SUCCESS-SPIDER-F10` ((total_tokens +1000/f)/success_rate, f=10 distill only SPIDER), `M-AMORTIZED-COST-PER-SUCCESS-COLD-F10`, `...RAG-F10`, `...REPLAY-F10`
  - `M-COST-RATIO-SPIDER-vs-COLD-F10`, `vs-RAG-F10`, `vs-REPLAY-F10` with bootstrap 95% CI (also f=1/100 sensitivity)
  - `M-DISTILL-TOKENS` (fixed 1000 amortized), `M-INSTRUCTION-TOKENS` (200 amortized 200/f only INSTR)
- **Controls**:
  - `M-PC1-HIT-RATE-REPLAY-SAME-A` (expected 1.0), `M-PC1-COST-REPLAY-SAME-A` (50 tok), `M-PC1-SUCCESS-SAME-A`
  - `M-PC2-EXECUTABLE-SAME-A`, `M-PC2-BINDING-SAME-A`, `M-PC2-SUCCESS-SAME-A`
  - `M-NC1-SHUFFLED-SUCCESS`, `M-NC1-SHUFFLED-FALSE-ACCEPT`, `M-NC1-SHUFFLED-BINDING`
  - `M-NC2-RANDOM-SUCCESS`, `M-NC2-RANDOM-FALSE-ACCEPT`
  - `M-B-LITERAL-SUCCESS`
- **Validity / diagnostics**:
  - `M-NUM-FAMILIES`, `M-NUM-TASKS-TOTAL`, `M-NUM-TASKS-PER-FAMILY`, `M-DUPLICATION-RATE` (measured duplication 0.9479), `M-PARAM-TASK-RATE` (0.8958), `M-TEMPLATE-COUNT` (49 expected), `M-FAMILY-COUNT` (36 available, >=10 used)
  - `M-VERIFICATION-AUROC` (header/body/status discrimination per runtime), `M-AX-CONSISTENCY` (0.9 proof), `M-JACCARD-ANCHOR-PASS-RATE` (>=0.75 guard)
  - `M-LLM-CALLS-TOTAL`, `M-LLM-FAILURE-RATE`, `M-LLM-AVAILABLE` (bool)

All metrics JSON keys stable for AUDIT recomputation. Raw evidence preserved per task (CSV with tokens, calls, latency, success, bound_action, verification, UNKNOWN, false_accept per condition), registry JSONL, cost_config, bound_action exact equality logs, Playwright traces sampled, provenance (model version, prompt hash, seeds, hashes, AX proof, Jaccard proof, header/body/status matrix).

## 8. Controls (stable identifiers)

- **Positive control PC-PARAM-REGRESSION-AND-LITERAL-HIT** (id `PC-PARAM-REGRESSION-AND-LITERAL-HIT`):
  - PC1: 5 tasks where test identifiers == training A (same-resource). B-REPLAY must hit at 1.0 with 50 tok verification only, success 1.0, validates 0-cost measurement and header/body/status verification per runtime.
  - PC2: Multi-param same-A (3 A observations -> mechanism via committed kernel with Jaccard>=0.75 and field-path relevance, test on same A pool). Must be EXECUTABLE 1.0, binding 1.0, success >=0.90 via actual registry/required_slots/_bind/verify including header/body/status.
  - Expected: both pass. Failure due to residual double-prefix, Jaccard filter false negative, or verification bypass -> MEASUREMENT_INVALID (audit checks verification path, not forced True).

- **Null controls NC-SHUFFLED-AND-RANDOM** (id `NC-SHUFFLED-AND-RANDOM`):
  - NC1 shuffled slot mapping (swap slots) on held-out B via real registry/_bind/verify — expected success <= COLD+0.05, false_accept >=0.25, binding <0.50. Goes through actual binding/verification so CAN show variance (not flat guarantee).
  - NC2 random retrieval (random registry entry, UNKNOWN disabled) — expected false_accept >=0.30 or success <= COLD.
  - If NC1 success >= SPIDER -0.05, SPIDER effect spurious (task difficulty confounded) -> measurement invalid for param-inherit claim.

- **Fail-able literal baseline B-LITERAL** (id `B-LITERAL`): literal mechanisms without slots must fail on B (success <=0.15), proving parameterization necessary and duplication 0.9479 param_task 0.8958 does not trivialize task. Validates template diversity (49 templates, not single-template mock) and Jaccard guard not over-permissive.

## 9. Baselines (strong, per Director mandate and AGENTS.md §13)

All baselines use identical held-out B family set, identical LLM/tools/budget, same header/body/status verification `_matches` on provenance, costs in same units, and same 36-family/49-template census:

- **B-COLD** (id `B-COLD`): cold LLM, no memory. Upper-bound.
- **B-INSTR** (id `B-INSTR`): hand-authored instructions (200 tok amortized 200/f, f=10 ->20 tok/task) + exploration.
- **B-RAG** (id `B-RAG`): Jaccard retrieval (threshold 0.30) over training A, verbatim replay without parameterization, fallback to COLD on mismatch. Retrieval 200 tok+150ms.
- **B-REPLAY** (id `B-REPLAY`): 0-token exact replay (TERX/BrowserBash) with LLM fallback on miss (exact action_template equality). Hit cost 50 tok verification only; miss cost = COLD. Tests whether caching alone suffices vs parameterization.
- **B-LITERAL** ablation as above.

Prior 5.42% ceiling vs weak simulated baselines is the null to beat; this experiment vs real LLM retrieval/replay with deterministic header/body/status verification and honest amortization is the next gate. RAG/TERX at 0% novelty must hit; at 100% novelty must miss — tautological cost definitions are blocked by non-bijective honest accounting and calibrated abstention (Director prior #2).

## 10. Decision Rule (frozen)

**SURVIVES_CURRENT_TEST** requires ALL of (C1)-(C6) via committed kernel + real LLM+Playwright+header/body/status provenance (audit verifies):

- **C1 success margin**: `M-SUCCESS-SPIDER` >=0.60 and `M-SUCCESS-DELTA-SPIDER-vs-COLD` >=0.12 (family-stratified bootstrap 95% CI lower >0.02) and delta vs RAG >=0.12 and vs REPLAY >=0.12 and vs INSTR >=0.10. Wilson lower for SPIDER >=0.48.
- **C2 mechanism**: `M-EXECUTABLE-SPIDER` >=0.75 and `M-BINDING-CORRECT` >=0.90 (Wilson lower >=0.80) and `M-UNSUBSTITUTED-TEMPLATES` ==0 (exact equality, no double-prefix, Jaccard not hallucinating).
- **C3 safety**: `M-FALSE-ACCEPT-SPIDER` <=0.10 and `M-UNKNOWN-RATE-SPIDER` in [0.00,0.15] on valid B and `M-ECE-SPIDER` <=0.15 and `M-SUCCESS-LITERAL` <=0.15 on same B.
- **C4 economics**: `M-COST-RATIO-SPIDER-vs-COLD-F10` <=0.75 (>=25% saving) and `M-COST-RATIO-SPIDER-vs-RAG-F10` <=0.85 with bootstrap CI upper <1.0 (f=10 primary; f=1/100 sensitivity reported; distill only SPIDER, instructions only INSTR — audit checks consistent amortization).
- **C5 controls**: `M-PC1-HIT-RATE-REPLAY-SAME-A` ==1.0 cost 50 tok success 1.0 PASS and `M-PC2-EXECUTABLE-SAME-A` ==1.0 binding 1.0 success >=0.90 PASS.
- **C6 null/freshness**: `M-NC1-SHUFFLED-SUCCESS` <= B-COLD +0.05 and `M-NC1-SHUFFLED-FALSE-ACCEPT` >=0.25, and `M-NC2-RANDOM` false_accept >=0.30 or success <= COLD (verification-derived variance), and UNKNOWN cases have confidence <0.80 or required_slots missing, ECE <=0.15.

**FALSIFIED** if any C1-C4 fails (excluding PC/NC substrate failures which are MEASUREMENT_INVALID). **MIXED** if C1 fails but C2 passes (binds correctly but agent fails downstream — mechanism vs execution separated). **MEASUREMENT_INVALID** if: fix not committed (including Jaccard check), slot collision, registry/resolve not exercising real required_slots/_bind, verification bypass, <60 valid tasks after measured dedup 0.9479 param_task 0.8958, value overlap !=0, Playwright/header verification broken, family <10 or template !=49, or LLM API unavailable >50% (retry 3x, backoff, logged; AGENTS.md failure discipline). No post-hoc threshold tuning; single primary outcome is C1+C2 together.

All thresholds frozen before execution; `freeze.json` hashes request/spec/prereg.

## 11. Measurement Validity and Threats

| # | Threat | Mitigation |
|---|--------|------------|
| 1 | LLM non-determinism / cost variance (temperature, sampling) | Temp 0, seed 42, model pinned gpt-4o-mini-2024-07-18, family-stratified bootstrap CIs (5000), per-family variance reported, price sensitivity ±50% |
| 2 | Playwright flake / verification tautology (bypass) | Deterministic _matches on DOM/response + header/body/status provenance per runtime EXP-RUNTIME-35764329925 HIT/SWR/SIE/304, PC1 validates verification path, audit checks no forced True (run_experiment.py:237,304 pattern), traces sampled, AUROC reported |
| 3 | WebArena duplication 0.9479 param_task 0.8958 trivializes hold-out | Family hold-out (not random), zero value overlap, B-LITERAL must fail <=0.15, duplication/param_task measured not hardcoded, 49 templates 36 families logged, site identity leakage check |
| 4 | Double-prefix residual (disjoint A/B pools) + Jaccard hallucination | Committed fix handles full B identifiers (A_SKU_00_000 -> template, B_SKU_00_000 binds exactly), Jaccard>=0.75 constant-anchor prevents spurious slots, exact expected_bound_action equality audit, distinct slot naming per field-path |
| 5 | Synthetic-to-real gap if WebArena inaccessible | Require true WebArena-Verified v2 (36 families/49 templates); if inaccessible after 3 attempts log failure.json and mark BLOCKED/MEASUREMENT_INVALID rather than silent Flask mock-as-real; mock only discloses mock ceiling |
| 6 | Slot collision / noise-field hallucination | Field-path relevance filter, Jaccard>=0.75, structure_similarity >=0.75, audit distinct slot check, NC1 shuffled must elevate false_accept; prior noisy-browser failures preserved as do_not_assume |
| 7 | Amortization dishonesty (prior denominator bug, bijective cost) | Distill 1000 tok only SPIDER, instructions 200 tok as 200/f only INSTR, per-task and amortized reported separately with same-unit bootstrap CIs, audit recomputes cost ratios from raw CSV, non-bijective cost (Director prior #2) |
| 8 | LLM API / cost blocking | Retry 3x exponential backoff per task, budget cap $60 early abort with receipt, >50% failures -> MEASUREMENT_INVALID not falsification (AGENTS.md) |
| 9 | Site identity leakage / AX mapping error | Family hold-out, AX 0.9 longest-prefix proof on 20 CDP trees, no cross-family retrieval; audit checks retrieved mechanism family; 36-family stratification |
|10 | Confidence miscalibration / UNKNOWN gaming + header/body channel orthogonality | Report ECE, UNKNOWN per family, require confidence <0.80 or missing required_slots for UNKNOWN; behavioral_score >=0.25 exercise; header/body/status orthogonal affordances tested via mixed header+body+query (Director prior #4) |

Representation loss disclosed per AGENTS.md §17-18: DOM/CDP (accessibility tree, action target, browser events, network response via header/body/status provenance) preserved; abstraction to parameter_slots and template strings removes positional noise but may lose structural CSS changes — disclosed and tested via binding exactness, verification AUROC, and Jaccard guard.

## 12. Procedure (step-by-step, no outcome inspection)

1. **Census**: Load WebArena-Verified v2 via Intel cache (/tmp/webarena etc.), deduplicate, count families/templates/duplication/param_task (target 192/49/36 0.9479/0.8958), verify AX 0.9 mapping, log hashes and 3 fetch attempts. Require >=10 families with A/B disjoint pools, measured duplication/param_task not hardcoded, 49 templates.
2. **Split**: Per family sample 3-5 A exemplars for training, hold out 6-12 B tasks for test. Verify value intersection =0 for parameterized slots per family, seed 42, log split manifest. 36-family pool ensures heterogeneity beyond single-template mock.
3. **Kernel fix**: Apply committed fix to `src/spider/kernel.py` (`_common_prefix_and_suffix`, `_field_path_to_slot_name`, `_extract_varying_values`, `distill_parameterized`) with distinct slot naming, Jaccard>=0.75, structure_similarity >=0.75, field-path relevance. Verify import+hash not monkey-patch.
4. **Distill**: For each family call `distill_parameterized()` on A exemplars, induce distinct slots per varying field (path+body+headers) with Jaccard guard, store one mechanism per family at confidence 0.90 via actual `MechanismRegistry`.
5. **Agent runs**: For each test B task run all 5 conditions (SPIDER/COLD/INSTR/RAG/REPLAY) + B-LITERAL with same LLM/tools/budget (15 steps, 4096 tokens, Playwright, header/body/status provenance). SPIDER via `resolve(intent,context,params)` with B params; others per baseline injection. Measure tokens, browser calls, latency, retrieval/verification/repair, UNKNOWN, false_accept via header/body/status _matches.
6. **Controls**: Run PC1 (5 same-A replay hits), PC2 (multi-param same-A), NC1 shuffled slot, NC2 random retrieval on same B set via real registry/_bind/verify with variance and header/body/status checks.
7. **Logging**: Per-task CSV (all conditions), registry JSONL (per-family slots/templates/confidence, Jaccard pass logs), cost_config.json (distill 1000, f=10), bound_action exact equality logs, Playwright traces sampled, provenance (model version, prompt hash, seeds, hashes, LLM_API_available, AX proof, header matrix, Jaccard threshold).
8. **Analysis**: Compute M-* with Wilson CIs, family-stratified bootstrap (5000) deltas/cost ratios, McNemar paired family-block tests. Apply frozen decision_rule C1-C6. No threshold tuning after outcomes. Audit recomputes from raw CSV/registry and verifies Jaccard>=0.75 not bypassed.

## 13. Consequences

### If SURVIVES

- C-PARAM-INHERIT EXPERIMENTAL (5.42% synthetic single-param + harness-only 21/21, plus prior 0/72 double-prefix MEASUREMENT_INVALID) -> VALIDATED at bounded real-LLM multi-param ceiling (WebArena-Verified v2 >=10 families >=60 tasks, 49 templates, 36 families, duplication measured, param_task 0.8958, path+body+headers distinct slots with Jaccard>=0.75, real Playwright+header/body/status verification per runtime, beats cold/instructions/retrieval/0-token replay by >=0.12, false_accept <=0.10, UNKNOWN 0.00-0.15 ECE <=0.15, honest f=10 economics saving >=25% vs COLD <=0.85x vs RAG). First live-browser family hold-out evidence that multi-param mechanisms generalize to unseen B via correct binding (header/body/status).
- Unblocks C-LLM-INHERIT (real LLM inheritance vs strong baselines) and C-PRODUCT-ECON (amortized economics with honest distill accounting, closing 6 vacuous extrapolations) and C-RESIDUAL-NOVELTY for Docker full-DOM scale-up. Quantifies win vs TERX exact-replay where replay misses, within 2x where replay hits; informs API-bypass vs DOM/header/body heterogeneity (Director prior #4).
- Authorizes kernel promotion of corrected `distill_parameterized` (promotion_ready true, pending kernel tests and independent audit PASS, Jaccard>=0.75 verified). No SHIPPED until replication on production hosting and freshness hardening.

### If FALSIFIED (or MIXED)

- C-PARAM-INHERIT remains EXPERIMENTAL at narrow synthetic ceiling (or bounded REJECTED for multi-param real-LLM on WebArena-Verified v2: corrected kernel with Jaccard>=0.75 does not beat baselines on held-out families). If MIXED (C2 passes but C1 fails), mechanism binds but downstream agent/verification fails -> fix Playwright/_matches/prompt not induction.
- If no advantage vs RAG/REPLAY (both miss on hold-out where duplication requires parameterization but replay hit_rate ~0), multi-param inheritance adds no economics beyond retrieval/replay, supporting caching-vs-generalization tension; Product redirects to C-FRESHNESS (freshness guards, UNKNOWN, distributed session per runtime), C-DELTA-REPAIR (localized repair on header/body/status substrate), C-SEMANTIC-RESOLVE (calibrated resolution) and defers C-PRODUCT-ECON Docker scale-up.
- If MEASUREMENT_INVALID (fix not committed incl. Jaccard, verification broken incl. header/body/status, <60 tasks, overlap !=0, LLM unavailable >50%, or header discrimination absent), priority is fixing kernel integration and runtime verification AUROC substrate — do not weaken prereg thresholds or promote.

Both outcomes high-information: definitively inform whether parameterized inheritance justifies productization vs redirection after 37 attempts, closing synthetic->real gap and determining PRODUCT_CORE per Director.

## 14. Analysis Plan

- **Primary**: Family-stratified paired comparison SPIDER success vs each baseline (McNemar + bootstrap delta CI 5000, family block). Requires C1 margin with CI lower >0.02.
- **Mechanism**: EXECUTABLE rate and binding correctness with Wilson CIs; zero `${}` check; per-family breakdown; exact expected_bound_action equality audit for double-prefix + Jaccard hallucination check.
- **Safety**: False_accept/UNKNOWN with Wilson CIs; B-LITERAL gate; ECE calibration; UNKNOWN requires confidence <0.80 or missing required_slots; header/body/status false_accept gated.
- **Economics**: Amortized cost per success at f=10 (distill only SPIDER) with family-stratified bootstrap cost ratio CI; sensitivity f=1/100; separate token/browser/latency decomposition and retrieval/verification/repair breakdown including header/body/status verification cost.
- **Controls**: PC1/PC2 must pass; NC1/NC2 must show expected null pattern via real bind/verify with header checks; audit recomputes all M-* from raw per-task CSV and registry JSONL.
- **Diagnostics**: Per-family success/cost, duplication/param_task/template/family counts, value overlap, verification AUROC/ECE (header/body/status), token/browsing/latency split, Playwright failure taxonomy, AX 0.9 proof, Jaccard anchor pass rate, header vs body discrimination.

## 15. Deviation Policy

Any deviation (changing family split, adding LLM calls, tuning thresholds/Jaccard after outcomes, using synthetic mock as real, monkey-patching instead of committed kernel) will be labeled **EXPLORATORY** and cannot support confirmatory claims. New confirmatory claim requires new preregistration and untouched evidence (AGENTS.md §17-19, EXPERIMENT_PACKET invariants). If mandate infeasible (WebArena inaccessible, LLM keys unavailable, header/body/status substrate unavailable), fail loudly with failure.json (DO NOT invent substitute direction) per POLICY.md.

## 16. Freeze Statement

This preregistration is frozen BEFORE any outcome-bearing measurement (no LLM agent runs, no Playwright executions, no binding success readouts, no header/body/status provenance). The experiment will be executed exactly as specified in `spec.json` and this `prereg.md`; `freeze.json` will hash request/spec/prereg before execution begins. EXECUTE may not mutate frozen inputs; AUDIT recomputes from raw evidence and verifies Jaccard>=0.75 and header/body/status discrimination. DESIGN did not inspect outcome data.

## 17. References to Packet and Charter

- Lane charter: `research/lanes/registry.json` product — "Turn audited capabilities into coherent external-agent product and continuously test product economics"
- Claim registry: `research/claims/registry.json` C-PARAM-INHERIT — next_gate "learn on resource A, succeed on never-observed B against cold/replay/retrieval baselines"
- Director mandate: `request.json` director_mandate CONTINUE C-PARAM-INHERIT with 4 agent priors (path dependence/local optima, residual-novelty tautology/0-token TERX, calibration/ECE, orthogonal DOM/header/body channels) distinguished from SPIDER evidence, and dependencies intel 192/49/36 AX 0.9, runtime header/body/status matrix
- Parent handoff: `research/experiments/EXP-PRODUCT-35756243655/handoff.json` (preserved established/rejected/unknown/do_not_assume per AGENTS.md; `next_question` advisory, Director question binding per POLICY.md)
- Dependencies: intel WebArena-Verified v2 census 192/49/36 0.9479 param_task 0.8958 AX 0.9, runtime header/body/status HIT/SWR/SIE/304 provenance for verify(), graph _common_prefix_and_suffix fix with Jaccard>=0.75
- Validity gates: AGENTS.md §§17-18 (target/split/sampling/uncertainty/representation integrity), EXPERIMENT_PACKET.md §3-4 (spec/result/audit/handoff shapes), POLICY.md (Global Director CONTINUE supersedes local next_question only as USE), ARCHITECTURE_RESEARCH2.md §5 (REQUEST->DESIGN->FREEZE->EXECUTE->AUDIT->DIRECTOR)
