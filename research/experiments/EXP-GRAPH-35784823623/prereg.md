# EXP-GRAPH-35784823623 preregistration — REOPEN C-PARAM-INHERIT

**Lane:** graph | **Claim:** C-PARAM-INHERIT (EXPERIMENTAL) | **Director action:** REOPEN (cognitive_reset true, SUPERSEDE) | **Cycle:** 35784282398
**Frozen:** BEFORE any outcome-bearing measurement; code, fixtures, model, thresholds hashed in freeze.json.

## 0. Binding direction

Director mandate question (binding):
> After fixing kernel distill_parameterized bugs (double-prefix in _common_prefix_and_suffix, Jaccard >=0.75 constant-anchor check, field-path relevance filter for body/headers/url only) and porting to src/spider/kernel.py, does real-LLM parameterized inheritance on WebArena-Verified v2 family hold-out (train on resource A, test on never-observed B, >=10 families >=60 tasks, 49 templates, duplication 0.9479) achieve EXECUTABLE >=0.75 and binding correctness >=0.90 with zero unsubstituted templates, success margin >=0.12 vs B-COLD/B-RAG/B-REPLAY/B-INSTR, false_accept <=0.10, UNKNOWN in [0.00,0.15] ECE <=0.15, and honest amortized saving >=25% vs COLD and <=0.85x vs RAG (family-stratified bootstrap CIs, deterministic verification, tokens+browser+retrieval+verification amortized f=10)?

The inherited parent handoff (EXP-GRAPH-35764315683, 5th consecutive DELTA-REPAIR BLOCKED) asked the same C-DELTA-REPAIR single-resource nginx question. Per Director `parent_handoff_disposition=SUPERSEDE` and `cognitive_reset=true`, that question is continuity evidence only. We do NOT repeat DELTA-REPAIR; we PIVOT to PARAM-INHERIT kernel fix. Its `carry_forward` distinctions are preserved below (§10) but do not drive this design.

## 1. Hypothesis

A corrected `distill_parameterized()` fixing three mechanical bugs that falsified prior integration — (1) `_common_prefix_and_suffix` double-prefix causing truncated B identifiers, (2) missing Jaccard >=0.75 constant-anchor check allowing pattern-absence hallucination, (3) missing field-path relevance filter allowing noise fields (metadata/provenance) to create spurious slots — ported to `src/spider/kernel.py` with distinct slot naming per field-path and `required_slots = set(parameter_slots) | template_slots`, will enable a real LLM agent (same model/tools/budget) trained on 3-5 exemplars per family on resource pool A to resolve `EXECUTABLE` with correct `bound_action` on never-observed resource pool B (zero exact value overlap, family hold-out) and achieve end-to-end success and honest amortized economics beating all strong baselines.

Specific expectations: `M-EXECUTABLE-SPIDER >=0.75`, `M-BINDING-CORRECT >=0.90`, `M-UNSUBSTITUTED-TEMPLATES =0`, success margin `>=0.12` vs each of B-COLD/B-RAG/B-REPLAY/B-INSTR, `M-FALSE-ACCEPT <=0.10`, `M-UNKNOWN-RATE in [0.00,0.15]`, `ECE <=0.15`, `M-AMORTIZED-SAVING-vs-COLD >=25%` at `f=10` and `M-COST-RATIO-RAG <=0.85` (family-stratified bootstrap CIs, deterministic `_matches` verification, tokens+browser+retrieval+verification+repair amortized).

## 2. Why this is the smallest high-information test

- **Unblocks product economics:** 41 prior C-PARAM-INHERIT attempts left KERNEL-INTEGRATION-FALSIFIED/PARTIAL; last 3 PRODUCT MEASUREMENT_INVALID due to same double-prefix bug. Synthetic single-param (10/10) and harness-only multi-param (21/21) SURVIVE but never ported; kernel fix is the mechanical prerequisite for C-RESIDUAL-NOVELTY/C-PRODUCT-ECON/C-LLM-INHERIT.
- **Beats synthetic ceiling tautology:** Bijective cost mocks (rho=1.0, RAG hit 1/100) ruled MEASUREMENT_INVALID; this design uses measured LLM+Playwright tokens+browser+retrieval+verification at `f=10`.
- **Avoids blocked DELTA-REPAIR:** Repeating 48-instance nginx HIT/SWR/SIE with real LLM reproduces BLOCKED (BrowserGym AX unavailable, SQLite session replication broken). PARAM-INHERIT needs only Playwright localhost per Director dependencies, maximizing executability.
- Not merely repeating pre-2.0: No prior experiment tested real-LLM family hold-out on WebArena-Verified v2 with field-path-aware multi-param induction via `src/spider/kernel.py` against COLD/RAG/REPLAY/INSTR with calibration and amortized f=10.

## 3. Experiment structure

### 3.1 Kernel fix (prerequisite, audited)

Patch `src/spider/kernel.py`:
- `distill_parameterized(observations: list[Observation]) -> Mechanism`: new method alongside literal `distill`.
- `_common_prefix_and_suffix(values: list[str]) -> (prefix,suffix)`: fix double-prefix (previous returned `prefix+prefix+variable+suffix` for full-B bind; corrected returns `prefix + ${slot} + suffix` once, tested on `B_...` values longer than A).
- `_extract_varying_values(observations)`: restrict to paths `url`, `body.*`, `headers.*` only; exclude top-level `provenance`, `state` metadata. Uses field-path relevance set.
- `structure_similarity(values): Jaccard >=0.75` on tokenized constant prefix/suffix; if below, reject induction (E1 pattern-absence).
- Distinct slot naming: map field-path -> slot name (e.g., `body.product_id -> ${product_id}`) via longest-prefix field registry; collision check distinct.
- Confidence `0.90`, `parameter_slots`, `action_template` with `${}`.

Audit validates diff and hash; tested by `tests/test_kernel_param_inherit.py` regression (B1/B4 clean synthetic still pass, D1 noisy over-param and E1 hallucination now correctly handled).

### 3.2 Data: WebArena-Verified v2 family hold-out

- **Source:** `data/webarena_verified_v2.json` or ` /tmp/webarena` or verified CSV `https://github.com/web-arena-x/webarena` pinned; fallback only after 3 fetch attempts logged, ceiling explicitly downgraded to synthetic mock (then MEASUREMENT_INVALID for WebArena claim).
- **Census verification (preflight):** 192 shopping tasks, 49 intent_templates, 36 families >=3 (34 >=4,33 >=5), duplication 0.9479 CI [0.9167,0.9792], exact-copy 0.0781 CI [0.0417,0.1198], param_task 0.8958, param_template 0.8367, AX_consistency 0.9 (prior EXP-INTEL-35749371101 PASS 20 trees 1280x720). Log hashes.
- **Dedup:** by `(template_id, intent, action_template hash)` keep one exemplar per cluster.
- **Family selection:** require >=10 families each >=3 tasks with >=2 resource pools A/B disjoint. Each family has template parameterization (e.g., `https://shop.example.com/product/${product_id}`, body `{"qty": ${qty}}`, header `X-CSRF: ${token}`).
- **Hold-out:** train 3-5 exemplars from A only; test B values have zero exact value overlap (`value_set_A ∩ value_set_B = ∅`, verified intersection=0). Family hold-out (families never seen during distill). Minimum 60 valid tasks (6/family) for decision; target 120-192 if budget allows. Stratified sampling seed 42, `PYTHONHASHSEED=0`.
- **Zero-overlap logging:** per-family value sets, intersection counts, provenance JSON.

### 3.3 Conditions (all on same held-out B set, same model/tools/budget)

- **SPIDER:** registry with one parameterized mechanism per family (confidence 0.90) via `distill_parameterized` + `registry.add`. Resolve with `required_slots | template_slots`, freshness 0.25 / confidence 0.80 -> UNKNOWN, else `_bind` + Playwright execute + deterministic `_matches` verification. Costs measured.
- **B-COLD:** cold LLM, no memory.
- **B-RAG:** Jaccard 0.30 retrieval, verbatim replay without slots, verification-gated fallback.
- **B-REPLAY-TERX:** exact action_template string equality 0-token replay + 50 tok verification, fallback to COLD.
- **B-INSTR:** 200 tok instructions amortized 200/f.
- **B-LITERAL:** literal `distill` without slots.

LLM: `gpt-4o-mini-2024-07-18` (or approved haiku/flash), temp 0.0, seed 42, 15 steps, 4096 tokens, system prompt fixed, Playwright `navigate/click/fill/type/select/goBack/observe` on localhost cached WebArena HTML (no external net for determinism) or Flask mock if disclosure. Browser chromium headless.

Positive controls PC1 (same-A literal hit 1.0, 50 tok) and PC2 (same-A multi-param 1.0/1.0/>=0.90) before B evaluation. Null controls NC1 shuffled slots and NC2 random retrieval via real bind/verify.

### 3.4 Cost accounting (honest)

Per-task: LLM input+output tokens (API usage), browser calls+ms, retrieval 200 tok+ms, verification 50 tok+ms, repair 1 LLM step if fail. Distill ~1000 tok amortized over `f=10` added ONLY to SPIDER; INSTR 200/f. Report raw and amortized `f=1,10,100` with family-stratified bootstrap 5000 (family as block, seed 42). Token, browser, latency separate and combined.

## 4. Metrics (stable IDs for downstream transmission)

- Primary: `M-SUCCESS-SPIDER`, `M-SUCCESS-COLD`, `M-SUCCESS-RAG`, `M-SUCCESS-REPLAY`, `M-SUCCESS-INSTR`, `M-SUCCESS-LITERAL`, deltas `M-DELTA-vs-COLD etc.`
- Mechanism: `M-EXECUTABLE-SPIDER` (resolve EXECUTABLE rate), `M-BINDING-CORRECT` (bound_action == ground truth among EXECUTABLE), `M-UNSUBSTITUTED-TEMPLATES` (count `${` left), `M-REUSED-ACTIONS` if applicable.
- Safety: `M-FALSE-ACCEPT-SPIDER` (incorrect bind passed verification / contamination), `M-UNKNOWN-RATE-SPIDER`, `ECE` (10 bins), `M-CONTAMINATION` (cross-family leakage <0.10), `M-UNKNOWN-PRECISION` (>=0.85 where measurable).
- Economics: `M-COST-SPIDER-RAW`, `M-COST-COLD-RAW`, `M-COST-RAG-RAW`, `M-AMORTIZED-SAVING-SPIDER-vs-COLD` (at f=10), `M-COST-RATIO-RAG` (SPIDER/RAG per success), `M-TOKENS-SPIDER`, `M-BROWSER-SPIDER`, `M-RETRIEVAL-COST`, `M-VERIFICATION-COST`.
- Controls: `PC1-HIT-RATE`, `PC1-COST`, `PC1-SUCCESS`, `PC2-EXECUTABLE`, `PC2-BINDING`, `PC2-SUCCESS`, `NC1-SUCCESS`, `NC1-FALSE-ACCEPT`, `NC1-BINDING`, `NC2-…`
- All with Wilson 95% CI for rates, family-stratified bootstrap 95% CI for ratios/deltas.

## 5. Decision rule (frozen)

**SURVIVES** requires ALL (C1)-(C6) via real LLM+Playwright deterministic verification:

- (C1) `M-SUCCESS-SPIDER >=0.65` and `> B-COLD >=0.12` and `> B-RAG >=0.12` and `> B-REPLAY >=0.12` and `> B-INSTR >=0.10`, family-stratified bootstrap 95% CI lower bound >0.02 for each margin, McNemar two-sided p<0.05.
- (C2) `M-EXECUTABLE-SPIDER >=0.75` (Wilson lower >=0.65) and `M-BINDING-CORRECT >=0.90` (Wilson lower >=0.80) with `M-UNSUBSTITUTED-TEMPLATES =0`.
- (C3) `M-FALSE-ACCEPT <=0.10` and `M-UNKNOWN-RATE in [0.00,0.15]` and `B-LITERAL success <=0.15` (literal fails) and `M-CONTAMINATION <0.10` where measurable.
- (C4) `M-AMORTIZED-SAVING >=25%` vs COLD at `f=10` (CI not crossing 1.0) and `M-COST-RATIO-RAG <=0.85` (CI upper <1.0).
- (C5) `PC1` hit_rate 1.0 cost 50 tok success 1.0 PASS and `PC2` EXECUTABLE 1.0 binding 1.0 success >=0.90 PASS; `NC1` success <= B-COLD+0.05 false_accept >=0.25, `NC2` false_accept >=0.30 or success <= B-COLD (through real bind/verify).
- (C6) UNKNOWN confidence <0.80 or missing required_slots, `ECE <=0.15` (10 bins), verification AUROC >=0.75 where measurable.

**FALSIFIED** if any C1-C4 fails on valid substrate (PC/NC failures alone are MEASUREMENT_INVALID). **MIXED** if C1 margin fails but C2 passes (binds correctly but agent downstream fails). **MEASUREMENT_INVALID** if kernel not ported to `src/spider/kernel.py` via real `required_slots|template_slots/_bind`, <60 tasks after dedup/zero-overlap, WebArena census not verified, LLM API unavailable >50%, or verification broken — substrate failure not falsification per `EXPERIMENT_PACKET.md` §9.

Prereg thresholds frozen; single primary outcome is C1 margin plus C2/C4 gates.

## 6. Controls and baselines (falsification strength)

- **B-LITERAL** isolates parameterization necessity (expected ~0 on B; if >0.15, hold-out leakage).
- **B-RAG/B-REPLAY** are strong memory baselines; duplication 0.9479 is parameterized reuse (91.8% differ in `instantiation_dict`), so literal replay must fail and RAG hit ~0.05; SPIDER must beat both, proving slot induction > retrieval.
- **B-INSTR** tests that instructions alone (≈AWM 24.6%/51.1% gain) do not explain transfer.
- **NC1 shuffled** tests that correct slot mapping matters; **NC2 random** tests ranking matters — both via real bind/verify so variability is genuine.
- **PC1/PC2** validate substrate can measure 0-cost and multi-param same-A before B generalization.
- **Null expectation for family hold-out:** exact-copy fraction 0.0781, so B-REPLAY/ RAG hit_rate ~0 is not tautological overhead but dataset property.

## 7. Validity threats

- Site-identity leakage via template leakage -> mitigated by family hold-out (not random), zero-overlap check, B-LITERAL gate.
- Token proxy tautology (bijective cost) -> mitigated by measured API usage + browser+retrieval+verification at f=10; Approach directly addresses Director prior #3.
- Verification tautology (LLM-as-judge) -> mitigated by deterministic `_matches` postconditions.
- Calibration circularity (confidence == threshold) -> mitigated by ECE 10 bins and PC2 0.90 >0.80 separation.
- Contamination from registry cross-family -> mitigated by family-stratified block bootstrap, contamination <0.10 via unrelated mechanisms.
- Tool/API bypass stratum (Director prior #4) -> disclosed; WebArena-Verified shopping is browser-workflow dominated; bypass vs browser saving stratified in report but not gating.
- BrowserGym AX optional -> per Director dependencies, Playwright alone suffices; if AX unavailable, disclosed not blocking.
- LLM provider failure -> retryable with fallback model hash logged; >50% unavailable -> MEASUREMENT_INVALID with retry hint `OPENAI_API_KEY`.
- Representation loss (AX 0.9 not full DOM) -> disclosed; this gate uses Playwright DOM + deterministic verification, AX is auxiliary.

## 8. Product consequences

**Positive (SURVIVES):** C-PARAM-INHERIT EXPERIMENTAL -> VALIDATED (bounded real-LLM multi-param). First demonstration that `distill_parameterized` with distinct field-path slots generalizes A->B with honest economics. Unblocks C-LLM-INHERIT and C-PRODUCT-ECON/C-RESIDUAL-NOVELTY scale-up; informs SPIDER vs TERX (70% hit prefix-exact only) dominance; authorizes `src/spider/kernel.py` promotion (promotion_ready true).

**Negative (FALSIFIED):** Remains EXPERIMENTAL (or bounded REJECTED for multi-param real-LLM). If MIXED, diagnosis shifts to agent/verification not induction. If RAG/REPLAY not beaten, exact replay/caching dominates at this duplication — next cycle per Director portfolio pivots to C-FRESHNESS distributed, C-DELTA-REPAIR nginx verified, or C-SEMANTIC-RESOLVE, deferring economics to Docker.

## 9. Estimated cost & expected information gain

**Cost:** 60-120 tasks x5 conditions =300-600 runs +10 PCs +60-120 NCs =370-730 runs; ~12-18k tok/run ~$0.04-$0.08 => $15-$60. Wall-clock 60-90 min (4 concurrent). No Docker required. See spec `estimated_cost`.

**Gain:** HIGH. Resolves 41-attempt starved bottleneck, closes mechanical kernel bug falsified by 3 PRODUCT MEASUREMENT_INVALID, and decisively tests central promise (residual-novelty amortized tokens+browser+retrieval+verification) vs strong AWM/TVCACHE/Browser-use baselines that portfolio notes are currently NOT_MEASURED. Either outcome changes `handoff.next_question` and promotion decision.

## 10. Inherited parent_handoff preservation (SUPERSEDE)

From EXP-GRAPH-35764315683 (BLOCKED):

- **established:** [] (no valid DELTA-REPAIR evidence; result metrics {} controls {}).
- **rejected (bounded):** Cost-bounded localized repair (<50% tokens <40% browser) FOR SIMULATION ONLY with hardcoded `COLD_TOKENS_BASE 2250` etc. — rejected in `EXP-GRAPH-35741890679` audit REVISE (ratio 0.613 CI[0.569,0.661] failing) — does NOT reject DELTA-REPAIR on real substrate.
- **unknown:** Whether real LLM achieves repair/token/browser/verification/contamination/byte-identity/per-family heterogeneity on nginx/Playwright — all remain unknown but are NOT this experiment's question (SUPERSEDE). Our unknowns are WebArena-Verified v2 family hold-out EXECUTABLE/binding/success delta/false_accept/UNKNOWN/ECE/amortized saving per §1.
- **do_not_assume:** Do not assume BLOCKED == falsification; frozen C1-C3 PASS in simulation was synthetic not measurement-valid; token ratios 0.613 etc. are simulation not real gpt-4o-mini; AUROC 1.0 artefactual; contamination 0.0046 hardcoded; per-family n=8 Wilson half-width 0.26 not powered; no inference to multi-resource/distributed/CDN — all per handoff §do_not_assume preserved.

This design carries forward `established/rejected/unknown/do_not_assume` exactly but treats `next_question` (48-instance nginx delta-repair) as advisory, replaced by Director mandate REOPEN C-PARAM-INHERIT question.

## 11. Execution checklist (for EXECUTE, not run now)

- Freeze hashes for `src/spider/kernel.py` patch, `data/webarena_verified_v2.json`, model pin, thresholds.
- Preflight census verification (192/49/36/dup 0.9479/AX 0.9) with hashes.
- Run PC1/PC2 -> gate MEASUREMENT_INVALID if fail.
- Run SPIDER/COLD/RAG/REPLAY/INSTR/LITERAL on B with family-stratified block bootstrap, deterministic verification.
- Run NC1/NC2.
- No simulation fallback for LLM; if `OPENAI_API_KEY` missing -> `status=MEASUREMENT_INVALID outcome=NOT_APPLICABLE` with `validity_notes` and `unresolved`, not falsification.
- Preserve raw CSV, registry JSON, cost_config, traces, provenance.
