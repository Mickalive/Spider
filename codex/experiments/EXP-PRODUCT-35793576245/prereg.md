# EXP-PRODUCT-35793576245 preregistration — Product honest residual-novelty economics

**Lane:** product — `REOPEN C-RESIDUAL-NOVELTY` per Global Research Director mandate cycle 35793060550
**Claim:** C-RESIDUAL-NOVELTY (C-PRODUCT-ECON downstream)
**Status before:** HYPOTHESIS (prior 2 product experiments MEASUREMENT_INVALID — bijective cost formula, token shuffling, hardcoded calibration, generic slots, inflated 400-tok hits)
**Date frozen:** 2026-09-22T22:xx freeze.json (no outcome-bearing measurement before freeze)

## 1. Strategic question (Director mandate verbatim refinement)
With genuine branch-derived cost from actual kernel `resolve/_bind/verify/freshness gating 0.25 / UNKNOWN<0.80` (no `n*3200` formula, no token shuffling to force `|rho_length|<0.20`, verification-derived UNKNOWN precision and ECE from kernel softmax `temp 0.15+jitter`), family-specific slot induction (not generic `['path','store']`), honest Stagehand/TERX 50-tok hit costs, 5000 family-stratified bootstraps and block-permutation on WebArena-Verified v2 36 families >=3 with controlled novelty fraction `0/25/50/75/100%` (train A test never-observed B), does later-agent cost (`tokens+browser+retrieval+reconstruction+verification+repair` amortized at `f=10`) track residual novelty (`Spearman rho_novelty>=0.60 R2_delta>=0.50`) rather than full task length (`rho_length|stratum|<0.20`) with honest saving `>=25% vs COLD at f=10` and calibrated abstention `false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15`?

Inherited `parent_handoff` EXP-PRODUCT-35782537266 is continuity evidence only. Per Director REOPEN/USE disposition, its `established/rejected/unknown/do_not_assume` are preserved below but do not override mandate. Its `next_question` is advisory; mandate question is binding.

## 2. What is established / rejected / unknown (from handoff carry_forward)

**Established to reuse:** WebArena-Verified v2 file-based census structure (192 tasks/36 families/49 templates/duplication 0.9479/param_task 0.8958) as mock when `/tmp/webarena` absent — disclosed synthetic ceiling; retrievability at `n=0` exact-repeat makes TERX/Stagehand/RAG `hit_rate=1.0` reachable by construction; cost model definitions (retrieval 200+150ms verify 50+120ms novel/repair 500+2 calls distill 1000/f only SPIDER instruction 200/f) frozen but not yet honestly executed; kernel `distill_parameterized Jaccard>=0.75` specified but harness fallback still used.

**Rejected (bounded, not global):** `M=250+500*int(10n)` or `n*3200+jitter` bijective formula with `rho~1.0 CI[1,1] R2~0.99` does NOT demonstrate compression (VF1); token shuffling within strata to force `|rho_length|<0.20` is data manipulation (VF2); hardcoded success/UNKNOWN precision 0.92 and linear `0.95-n*0.12` confidence are invalid (VF3-VF4, VF8); generic `['path','store']` does NOT demonstrate family-specific induction `${sku}/${store_id}/${variant}/${category}` (VF5); Stagehand/TERX 400-tok hits vs spec 50-tok do NOT demonstrate beating shipped Stagehand 2x/30% at exact repeat (VF6). No broader rejection of residual-novelty hypothesis globally.

**Unknown targeted:** whether genuine parameterized inheritance with honest baselines on WebArena family hold-out yields `rho_novelty>=0.60 R2_delta>=0.50` with calibrated abstention; whether `Jaccard>=0.75` family-specific induction generalizes to real family templates; whether `UNKNOWN` fallback keeps `n=1` cost `<=1.10x COLD`; whether SPIDER beats retrievable RAG/Stagehand/TERX at `n=0` with 5000-CI; kernel commit survivability beyond mock.

**Do-not-assume:** synthetic 36-family mock != production DOM/cross-site/800-element pages; prior `rho 0.98 R2 0.99` are formula artefacts; `false_accept 0.047 UNKNOWN precision 0.915 ECE 0.021` were hardcoded; Stagehand/TERX 1.02 vs RAG 0.68 at `n=0` were cost-inflated; generic slots != family-specific; 2000 bootstraps != 5000 required; C-RESIDUAL-NOVELTY remains HYPOTHESIS not EXPERIMENTAL/PRODUCT_CORE; C-PRODUCT-ECON commercial viability remains unmeasured.

## 3. Hypothesis (falsifiable)

Later-agent amortized cost under SPIDER parameterized inheritance (family-specific Jaccard>=0.75 constant-anchor, freshness 0.25, confidence `softmax temp0.15+jitter` UNKNOWN<0.80 ECE<=0.15, verify+repair) tracks residual novelty fraction `n ∈ {0,0.25,0.50,0.75,1.00}` (train A test never-observed B within same WebArena family) with `rho_novelty>=0.60 (p<0.01, 5000 family-stratified bootstrap CI lower>0.35, slope>0)` and `R2_delta>=0.50 (R2_novelty>=0.30)` while `|rho_length| per novelty stratum <0.20`. At `n=0` SPIDER `>=25%` cheaper amortized `f=10` than `B-COLD` and `<=1.20x B-STAGEHAND-CACHE`; beats `B-RAG-EMBED` at 0/25% and beats `B-TERX` at `≥25%`; at `n=1` via UNKNOWN fallback `<=1.10x COLD` with `false_accept<=0.10 UNKNOWN_precision>=0.85 ECE<=0.15`.

Null: flat cost vs novelty (`rho~0 R2_delta~0`) or no honest saving vs strong baselines.

## 4. State / action / observation representation

**State representation:** file-based task `state` dict with WebArena family workflow fields (`category, product_spec, cart, auth` mock) plus `preconditions` (family-specific workflow search→filter→open→select→add→checkout→verify). If `/tmp/webarena` census JSON present, use real task intents/params; else synthetic mock exactly replicating 36/49 structure, disclosed ceiling synthetic/WebArena-inspired not production DOM. Reported duplication 0.9479 param_task 0.8958.

**Action representation:** SPIDER `Mechanism.action_template` with family-specific slots `${sku}, ${store_id}, ${variant}, ${category}` (field-path-relevant `body.*, headers.*, url` only) not generic `['path','store']`. Bound via `src/spider/kernel.py _bind` checking `required_slots = parameter_slots | template_slots`. No TEMPLATE slot leakage.

**Observation:** `Observation(intent, state, action, next_state, success, provenance)` per `src/spider/models.py`. `SpiderKernel.observe` hashes raw; `distill_parameterized` induces one parameterized `Mechanism` per family from 5 A demos gathering varying values via Jaccard>=0.75 + `structure-similarity>=0.75` + `constant-value anchor` + field-path filter (excludes top-level metadata). Registry `MechanismRegistry` exercised and hashed.

All representations preserved raw in `artifacts/raw_per_task.csv` and `registry.jsonl`. Representation loss (mock vs real WebArena AX tree/DOM, generic vs family-specific slots) disclosed in validity_notes.

## 5. Target (primary outcome)

Per-task amortized cost at `f=10`:
```
cost_task = retrieval(200 tok+150ms) + verify(50+120ms)
          + sum_step [ if hit/bind+verify passes: 50+1 call
                       elif novel/failed: 500 tok+2 calls
                       elif repair: 500 tok+2 calls ]
          + distill_amort (1000/f only SPIDER, else 0)
          + instruction_amort (200/f only B-INSTRUCTION)
          / success (verify-derived, not assigned)
```
Genuine branch-derived sum, **not** `M=250+500*int(10n)` or `n*3200+jitter`. Latency ms reported but primary metric is token+call derived cost (proxy for browser+retrieval+reconstruction+verification+repair). If `gpt-4o-mini` + Playwright available, report real tokens/browser calls alongside proxy with ±50% sensitivity.

Primary statistical target: `Spearman rho_novelty` between `cost_task` and `n` (family-stratified).

## 6. Sampling policy and hold-out

- **Census:** 192 tasks across 36 families `>=3` (49 templates). Attempt `/tmp/webarena` or repo-cached JSON; if absent generate synthetic mock exactly matching family/template/duplication/param_task ratios, disclose synthetic ceiling.
- **Within-family hold-out:** per family disjoint `A(train)` / `B(test never-observed)` identifier pools with zero overlap. Controlled `n` fractions realized by sampling test tasks where `n` fraction of parameterizable slots drawn from `B` and `1-n` from `A`, stratified by slot position and family. `n=0` tasks are exact-repeat sequences (test seq == training trajectory) so `B-TERX/B-STAGEHAND hit_rate=1.0` reachable inside compared set (fixes prior 0/100 starvation).
- **Train:** 5 demos per family on `A` only. Registry one parameterized mechanism per family via actual `distill_parameterized` (not hard-coded constant). All fitting (TFIDF/embedding, distill) on TRAIN only.
- **Test:** all 192 tasks evaluated once per method (paired design) at each `n` level. Total `~6*192=1152` + 3 controls `~576` = ~1728 trials.
- **Length:** `L` family-specific 8-14 constant within family varies across families; `n` and `L` orthogonal within strata by design.
- **Seeds:** `PYTHONHASHSEED=0 random.seed42 numpy RandomState42` for sampling, jitter, permutation. Deterministic. No outcome-bearing measurement before freeze.

## 7. Baselines, positive and null controls (strong baselines required)

**Baselines (identical 192-task splits, same verify fallback to B-COLD on miss):**
- `B-COLD` cold start no memory upper bound.
- `B-INSTRUCTION` site-specific hand-authored instruction prompt (200 tok amortized).
- `B-RAG-EMBED` semantic retrieval top-1 verbatim bind Jaccard/embedding cosine retrieval 200 tok+150ms retrievable at `n=0` by construction.
- `B-STAGEHAND-CACHE` shipped DOM-hash serverCache 2x/~30% hit 50 tok+120ms exact-selector+DOM-hash (spec 50 not 400) hit iff DOM identical at `n=0`.
- `B-TERX-REPLAY` 0-token exact replay 50 tok verify exact string equality hit at `n=0`.
- `P-SPIDER-PARAM` SUT as above (distill 1000/f only SPIDER).

**Positive controls** `PC-BINDING-AND-EXACT-REPEAT`: PC1 exact-repeat cache must `hit_rate=1.0` at `n=0` 50 tok verify success1.0; PC2 parameterized binding on seen `A` 5/5 per family `correctness 1.0` via `_bind`. Failure → `MEASUREMENT_INVALID` (substrate broken, not falsification). BrowserGym health not gating (file-based) but report if Playwright used.

**Null controls** `NC-SHUFFLE-RANDOM-LENGTH`: NC1 shuffled slot mapping permute learned slots before resolve expect `|rho|<0.25 p>=0.05 success<=COLD`; NC2 random mechanism `false_accept>=0.30` or `|rho|<0.25`; NC3 length-proportional `cost=L*unitCost` expect `|rho|<0.25 R2<0.15` proving environment can express MIXED/FALSIFIED. All via actual pipeline.

**Control identities frozen for EXECUTE/AUDIT:** `PC-BINDING-AND-EXACT-REPEAT`, `NC-SHUFFLE-RANDOM-LENGTH`, `B-COLD`, `B-RAG-EMBED`, `B-STAGEHAND-CACHE`, `B-TERX-REPLAY`, `P-SPIDER-PARAM`, `B-INSTRUCTION`, `B-LENGTH-PROPORTIONAL`.

## 8. Primary metric, expected direction, uncertainty method, adequacy

- **Primary metric:** `rho_novelty = Spearman(cost_f10, n)` family-stratified pooled `N~192`.
- **Expected direction:** `>0` monotonic increasing with residual novelty. Secondary `R2_delta>0`, `|rho_length|per_stratum|<0.20` flat vs length.
- **Uncertainty:** family-stratified bootstrap 5000 resamples (resample families with replacement then tasks within family) for 95% CI on `rho, R2_delta, cost ratios, rho_length`. Block-permutation on family labels 5000 perms for two-sided `p`. Wilson 95% CI for rates. Heteroscedasticity-robust SE for slopes. Degenerate CI `[1,1]` flagged degenerate not precision.
- **Adequacy rule:** `power>0.95` to detect `rho>=0.60 alpha0.01` requires `n>=44` (192 satisfies). ECE computed 5 bins derived confidence vs verify correctness `std>0.05`; 3 empty bins disclosed; bootstrap 2000 for ECE CI. No token shuffling (VF2 forbidden).

## 9. Decision / falsification / survival rule

Compute pooled family-stratified `N~192` (file-based, not live BrowserGym):
- `success, false_accept, UNKNOWN_precision, ECE 5-bin, cost/task, amortized cost/success f10, rho_novelty, R2_novelty, R2_length per stratum & pooled R2_delta, rho_length per stratum, Wilson CIs, bootstrap5000 CIs, block-permutation p`.

**SURVIVES_CURRENT_TEST iff ALL hold:**
- **C1** correctness+calibration: SPIDER `success at n0 >=0.85 (Wilson lower>=0.72)` mean across bins `>=0.80` `false_accept<=0.10` `UNKNOWN_precision>=0.85` `ECE<=0.15` (derived confidence `std>0.05`, disclosed empty bins) verification-derived.
- **C2** positive controls: PC1 `B-TERX` and `B-STAGEHAND hit_rate 1.0 at n0` inside compared set 50 tok verify-only success1.0, PC2 SPIDER `5/5 per family binding 1.0` at `n0` via `_bind`; failure → `MEASUREMENT_INVALID`.
- **C3** novelty tracking: `rho_novelty>=0.60` `p<0.01` bootstrap95% lower `>0.35` `slope>0 p<0.01`.
- **C4** residual explanatory power: `R2_delta>=0.50 (R2_novelty>=0.30)` and each stratum `|rho_length|<0.20` (5 strata, no shuffling).
- **C5** work compression honest: `SPIDER/COLD f10 <=0.75 at n0 (>=25% saving)` and `<=1.20x B-STAGEHAND-CACHE at n0` and `SPIDER beats B-RAG-EMBED at n0,n0.25 ratio<=0.80` and `beats B-TERX at every n>=0.25`; at `n1 SPIDER/COLD<=1.10` via UNKNOWN.
- **C6** null controls: NC1 shuffled `|rho|<0.25 p>=0.05 success<=COLD`, NC2 `false_accept>=0.30 or |rho|<0.25`, NC3 `|rho|<0.25 R2<0.15`.

**Precedence:** If C2 fails → `MEASUREMENT_INVALID` irrespective of C3-C6. If C2 passes but C3 or C4 fail with C1 pass → `MIXED` (correct but flat cost overhead dominates). If C2 passes but C5 fails → `FALSIFIED` (no honest saving). If NC1 shows `rho>=0.35 significant` → `MEASUREMENT_INVALID` (novelty confounded). Degenerate bootstrap or shuffling manipulation → `MEASUREMENT_INVALID`. All thresholds two-sided `alpha0.01` primary.

## 10. Validity threats and mitigations

- **VF1 bijective formula:** mitigated by branch-derived cost sum inspection; auditor checks `run_experiment.py` has no `250+500*int(10n)` or `n*3200`.
- **VF2 shuffling:** forbidden; `|rho_length|` reported honest per stratum without shuffling loop.
- **VF3/VF4 hardcoded calibration:** verification-derived correctness, `softmax temp0.15+jitter` confidence not linear, `UNKNOWN_precision/ECE` derived not assigned; auditor checks confidence generation.
- **VF5 generic slots:** family-specific induction verified via `registry.jsonl` — all 36 mechanisms must not share identical `['path','store']`; field-path relevance check.
- **VF6 inflated hit costs:** Stagehand/TERX hits fixed 50 tok not 400; auditor recomputes cost_config.
- **VF10 synthetic ceiling:** disclosed as file-based mock not production DOM/cross-site; `validity_notes[0]` carries ceiling; scale-up to Docker/full-DOM gated behind this isolation.
- **History-dependence:** family-stratified bootstrap + block-permutation respects task-family correlation; not treating transitions as independent.
- **Leakage:** no test `B` identifier in train registry verbatim; TFIDF/distill from `A` only; `hidden_expected` not passed except verify.
- **Degenerate CI:** `[1,1]` flagged degenerate not high-precision; ECE with 3 empty bins disclosed.
- **Agent prior tuple `__SHOPPING__` placeholder / hash SPA optima:** not applicable here (file-based census, not BrowserGym live), but viewport 1280x720 and AX hash logic pinned if Playwright used.

## 11. Product consequences

**If SURVIVES family-stratified:** C-RESIDUAL-NOVELTY `HYPOTHESIS→EXPERIMENTAL` bounded to WebArena-Verified v2 file-based census 192/36 proxy (or gpt-4o-mini 15-step Playwright where available) harness or committed kernel `Jaccard>=0.75`. First non-bijective evidence later-agent cost tracks residual novelty (not length) with calibrated abstention and honest saving `>=25%` beating retrievable RAG and shipped Stagehand at `>0%` novelty. Unblocks `C-PRODUCT-ECON` amortized scale-up to Docker full-DOM + real LLM (intel overlap + runtime replication prerequisites, effect size for `f=100`). No `PRODUCT_CORE` promotion; replication with production hosting + real LLM + kernel-committed distill required.

**If FALSIFIED (controls PASS but rho<0.35 or R2_delta<0.15 or saving<25% or not beating Stagehand/RAG/TERX):** parameterization as ported does not yield residual-novelty-proportional compression on this aliasing mix, or only via miscalibration, or constant overhead dominates (`MIXED`). Product must NOT claim pay-cost-of-novelty for `C-RESIDUAL-NOVELTY/C-PRODUCT-ECON` on this setting; prioritize caching (Stagehand 2x ships) or freshness/delta-repair or semantic-resolve orthogonal before revisiting economics. Bounded REJECTED for proxy setting only, not global falsification.

**If MEASUREMENT_INVALID:** C-RESIDUAL-NOVELTY remains `HYPOTHESIS`; exactly `failure.json` reason and smallest next action to unblock (e.g., fix kernel `distill_parameterized` double-prefix/Jaccard/field-path filter, add family-specific templates, restore 50-tok hit accounting).

## 12. Estimated cost and information gain

**Cost:** Low-moderate: 192 tasks ×6 conditions +3 controls ≈1152-1350 resolve/_bind/verify trials plus offline retrieval. File-based no Docker required; wall <30min CPU proxy (<90min if Playwright `gpt-4o-mini`). Storage per-task CSV ~1350 rows registry JSONL traces. No keys required proxy; ~$8-12 if real LLM.

**Expected information gain:** Very high — first non-bijective non-starved test after `2× MEASUREMENT_INVALID`; decisive for whether `C-PRODUCT-ECON` Docker+real-LLM scale-up justified vs premature and whether parameterized inheritance justifies productization despite Stagehand exact-repeat dominance.

## 13. Consequences of positive and negative outcomes (product decision)

- **Positive (all C1-C6 pass):** advance claim ceiling to `EXPERIMENTAL`, keep `HYPOTHESIS` for production transfer; schedule Docker full-DOM + real `gpt-4o-mini` replication before any `PRODUCT_CORE`/`SHIPPED`; use measured `rho`/`R2_delta`/`saving` as effect-size prior for `f=100` amortization and for pricing pay-for-novelty.
- **Negative (FALSIFIED/MIXED with controls PASS):** reframe pay-for-novelty claim, park `C-RESIDUAL-NOVELTY` for this kernel/cost model, redirect product to Stagehand caching + freshness gating + delta-repair until stronger mechanism found; frontier retrieval complementarity remains advantage at `f=10`.

## 14. Artifacts and provenance (for AUDIT)

- `research/experiments/EXP-PRODUCT-35793576245/run_experiment.py` (produces branch-derived cost)
- `artifacts/raw_per_task.csv` (task_id,family_id,novelty_fraction,length,system,success,false_accept,unknown,precision,tokens,browser_calls,latency_ms,reused_steps,hit,verify_passed,repair_triggered,confidence,ECE_bin)
- `artifacts/registry.jsonl` (per-family mechanisms, parameter_slots, confidence, templates)
- `artifacts/cost_config.json` (retrieval/verify/novel/repair/distill constants)
- `artifacts/branch_traces.json` (executed branch per task)
- `fixtures/tasks.json` (census manifest hash)
- `provenance.json` (run id, commits, hashes, seeds, Playwright/BrowserGym version pin, embedding model name)
- No outcome file edited after freeze; `freeze.json` hashes request/spec/prereg before `result.json`.

*Preregistered without inspecting outcomes. Outcome-bearing code not executed before freeze. Any post-freeze analysis change is exploratory and requires new preregistration for confirmatory claim.*

