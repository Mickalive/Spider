# EXP-PRODUCT-35797365772 preregistration — Product honest residual-novelty economics (per-hit isolated, QCR, non-vacuous)

**Lane:** product — `REOPEN C-RESIDUAL-NOVELTY` per Global Research Director mandate cycle 35796935672 (SUPERSEDE disposition)
**Claims:** C-RESIDUAL-NOVELTY (primary), C-PRODUCT-ECON, C-LLM-INHERIT downstream
**Status before:** HYPOTHESIS (prior EXP-PRODUCT-35793576245 FALSIFIED boundedly on proxy census: rho 0.608 passes but R2_delta 0.400<0.50, per-stratum |rho_length|~1.0, SPIDER/STAGE 1.50x, SPIDER/RAG 1.13x, SPIDER/TERX 1.05x at n>=0.5 under total-cost model; mock vacuous false_accept 0)
**Date frozen:** 2026-09-22T23:xx freeze.json (no outcome-bearing measurement before freeze)

## 1. Strategic question (Director mandate binding, verbatim refinement)

On WebArena-Verified v2 36 families >=3 (192 tasks, 49 templates, duplication 0.9479) with matched task families controlling novelty fraction (0%,25%,50%,75%,100% unseen identifiers, train on resource A test on never-observed B) and genuine kernel resolve/bind/verify with freshness 0.25 and UNKNOWN<0.80 abstention (ECE<=0.15 precision>=0.85, no bijective cost formula, non-vacuous false_accept), does SPIDER parameterized inheritance achieve rho_novelty>=0.60 R2_delta>=0.50 |rho_length|<0.20 and honest amortized saving >=25% vs COLD and <=0.85x vs RAG with parity at n=0 to shipped Stagehand DOM-hash HIT cache (2000 nodes 1280x720), TERX 50-token replay and RAG-EMBED (QCR protocol: frozen bank, same ranker, vary only post-retrieval support) with family-stratified bootstrap + block permutation, and report tokens/browser/latency/retrieval/verification Pareto vs gpt-4o-mini+Playwright Docker replication?

Inherited `parent_handoff` EXP-PRODUCT-35793576245 is continuity evidence only. Per Director REOPEN/SUPERSEDE, its `established/rejected/unknown/do_not_assume` are preserved below but do not override mandate. Its `next_question` is advisory; mandate question is binding.

## 2. What is established / rejected / unknown (from handoff carry_forward)

**Established to reuse:**
- First genuine branch-derived cost measurement with no bijective formula (no 250+500*int(10n), no n*3200) verified via run_experiment.py and audit V6; Cost = retrieval200+150ms + verify50+120ms + hit50 vs repair500+2 + distill1000/f honest sum.
- Positive controls PASS: PC1 TERX hit_rate 1.0 at n=0 mean 50 tok, Stagehand hit_rate 1.0 at n=0 mean 595 tok, PC2 SPIDER binding correctness 1.0 at n=0 via actual src/spider/kernel.py _bind (36/36).
- SPIDER tracks residual novelty on census: rho 0.6077 p 0.0002 CI [0.48,0.717] slope 4652 R2_novelty 0.509 (audit recomputed).
- Family-specific slot induction verified: all 36 mechanisms distinct ${sku},${store_id},${variant},${category}, none generic ['path','store']; Jaccard>=0.75 constant-anchor structure-similarity>=0.75 field-path relevance; B-pool never leaks into registry.
- WebArena-Verified v2 file-based census 192/36/49 structure hash e824ab3157cbd299, now with realized A/B pools seed42 and realized_novelty per task (fixtures/tasks.json sha 0e153ed8). Synthetic ceiling disclosed (not Docker/full-DOM).
- Statistics: 5000 family-stratified bootstrap and 5000 block-permutation correctly implemented in stdlib (Random42, PYTHONHASHSEED0).

**Rejected (bounded, not global):**
- SPIDER parameterized inheritance under frozen total-cost model does NOT pay only residual novelty vs honest baselines on this 192/36 file-based census — bounded FALSIFIED: SPIDER/STAGE 1.503 CI[1.409,1.611] >1.20, SPIDER/RAG 1.126 CI[1.066,1.190] >0.85 per_hit-equivalent, SPIDER/TERX 1.054 >1 at n>=0.5.
- R2_delta>=0.50 and per-stratum |rho_length|<0.20 on total cost is structurally unsatisfiable when cost scales with L (audit critical).
- Null NC1 shuffled rho 0.313 p 0.0002 exceeds |rho|<0.25 bound (strict C6 fail) — abstention schedule correlates with novelty for single-slot families where permutation is identity; below 0.35 invalidation bound.
- Pay-cost-of-residual-novelty commercial promise under kernel/total-cost model on proxy census — bounded rejection only, not global. Deterministic mock vacuity (success 1.0 false_accept 0) non-discriminating.

**Unknown targeted (this experiment):**
- Whether per-hit cost isolation (M_per_hit = (total - retrieval - distill)/L) excluding fixed overhead makes C4 |rho_length|<0.20 and C5 parity (<=1.20x Stagehand, <=0.85x RAG per_hit) satisfiable and changes FALSIFIED verdict.
- Whether revised amortization f=100 (distill 10 vs 100) makes total saving >=25% vs COLD survivable.
- Whether non-deterministic mock (wrong-bound p=0.15) yields non-vacuous false_accept in [0.10,0.60] and discriminating UNKNOWN_precision/ECE.
- Whether QCR frozen-bank same-ranker with proportional RAG at n=0.25 changes SPIDER/RAG ratio (currently 0.671 SPIDER cheaper at n=0.25 but binary RAG miss) and whether continuous similarity novelty changes boundary.
- Whether gpt-4o-mini+Playwright 1280x720 Docker replication correlates with proxy branch economics (real tokens/browser/latency) and preserves Pareto.
- Whether C-PRODUCT-ECON commercial viability holds at f=10/100 with Pareto cost decomposition.

**Do-not-assume:**
- Synthetic 192/36 file-based census != production DOM, cross-site, 800-element full-DOM WebArena — ceiling synthetic file-based.
- Prior success 1.0 false_accept 0 UNKNOWN_precision 1.0 ECE_exec 0.025 are non-discriminating artefacts of deterministic mock — do not assume calibration validated.
- Prior rho 0.608 alone does NOT prove economics — SPIDER still 1.50x Stagehand total under frozen constants.
- C4 failure (R2_delta 0.400, rho_length~1.0 total) does NOT mean SPIDER does not track novelty — C3 passes; failure is design artefact of total cost scaling with L — per_hit isolation required.
- Stagehand 595 tok vs TERX 50 tok at n=0 ratios floor at ~1.35-1.7 for L<=14 by total-cost construction — per_hit needed.
- C-RESIDUAL-NOVELTY is globally HYPOTHESIS bounded FALSIFIED for proxy total-cost setting only, not global.

## 3. Hypothesis (falsifiable)

Later-agent cost under SPIDER parameterized inheritance (family-specific slot induction Jaccard>=0.75 constant-anchor structure-similarity>=0.75 field-path relevance, behavioral freshness gating 0.25, confidence softmax temp0.15+jitter UNKNOWN<0.80 ECE<=0.15, verify+repair fallback) tracks residual novelty fraction n ∈ {0,0.25,0.50,0.75,1.00} (train A test B within family) with per_hit Spearman rho_novelty>=0.60 (p<0.01, 5000 bootstrap CI lower>0.35, slope>0) and R2_delta>=0.50 (R2_novelty>=0.30) while per_hit cost vs length within each stratum is flat (|rho_length|per_stratum|<0.20). At n=0 honest saving >=25% vs B-COLD on M_total_f10 (or f=100 sensitivity) with per_hit parity to shipped caches (M_per_hit SPIDER/STAGE <=1.20, SPIDER/RAG <=0.85 at 0 and 0.25, SPIDER/TERX <1.0 at >=0.25 under QCR). At n=1 UNKNOWN fallback keeps total cost <=1.10x COLD with false_accept<=0.10 UNKNOWN_precision>=0.85 ECE_exec<=0.15 non-vacuously.

Null: flat per_hit cost vs novelty (rho~0 R2_delta~0) or no honest saving/per_hit advantage vs strong QCR baselines.

## 4. State / action / observation representation

**State representation:** file-based task `state` dict with WebArena family workflow fields (category, product_spec, cart, auth mock) plus `preconditions` (family-specific workflow search→filter→open→select→add→checkout→verify). If /tmp/webarena census JSON present, use real intents/params; else synthetic mock exactly replicating 36/49 structure, disclosed ceiling synthetic/WebArena-inspired not production DOM (2000-node DOM simulated via hash if Playwright not used). Duplication 0.9479 param_task 0.8958.

**Action representation:** SPIDER `Mechanism.action_template` with family-specific slots `${sku},${store_id},${variant},${category}` (field-path-relevant body.*, headers.*, url only) not generic ['path','store']. Bound via `src/spider/kernel.py _bind` checking `required_slots = parameter_slots | template_slots`.

**Observation:** `Observation(intent, state, action, next_state, success, provenance)` per `src/spider/models.py`. `SpiderKernel.observe` hashes raw; `distill_parameterized` induces one parameterized `Mechanism` per family from 5 A demos gathering varying values via Jaccard>=0.75 + structure-similarity>=0.75 + constant-value anchor + field-path filter (excludes top-level metadata). Registry `MechanismRegistry` exercised and hashed.

**Non-deterministic MockEnv extension:** Deterministic branch (evidence-membership) retained for SPIDER correct binding, but NC1 shuffled / NC2 random forced-execute branches emit wrong-bound action with p=0.15 (seeded Random42) that fails verify (postcondition mismatch) -> false_accept>0. Correct SPIDER binding at n=0 never triggers wrong-bound. This makes false_accept and UNKNOWN_precision discriminating while preserving honest cost branches.

All representations preserved raw in `artifacts/raw_per_task.csv` (adds realized_n, M_per_hit, M_total_f10/f100, retrieval_ms, verification_ms) and `registry.jsonl` plus `qcr_bank_manifest.json`. Representation loss (mock vs real WebArena AX tree/DOM 2000 nodes, generic vs family-specific, wrong-bound rate 0.15 synthetic) disclosed in validity_notes.

## 5. Target (primary outcome)

Per-task costs:
```
M_total_f10  = retrieval(200+150ms) + verify(50+120ms) + sum_step[ hit 50+1 call | novel/repair 500+2 ] + distill 1000/10 (100 SPIDER else 0) + instruction 200/10
M_total_f100 = same with distill 1000/100 (10) and instruction 200/100 (2)
M_per_hit    = (M_total_f10 - retrieval - distill_amort) / L   // cost per step excluding fixed overhead, primary for |rho_length| and QCR parity
```
All genuine branch-derived sums, not bijective formulas. Latency ms reported but primary metric is token+call derived cost. If gpt-4o-mini+Playwright available, report real tokens/browser calls alongside proxy with ±50% sensitivity and correlation rho_proxy_real.

Primary statistical target: `Spearman rho_novelty` between `M_per_hit` and `realized_n` (family-stratified, realized_n = round_half_up(labelled_n*S)/S). Secondary rho on M_total_f10.

## 6. Sampling policy and hold-out (QCR)

- **Census:** 192 tasks across 36 families >=3 (49 templates). Attempt /tmp/webarena or repo-cached JSON; if absent generate synthetic mock exactly matching family/template/duplication/param_task ratios, disclose synthetic ceiling. All tasks carry labelled_n and realized_n.
- **Within-family hold-out under QCR:** per family disjoint `A(train)` / `B(test never-observed)` identifier pools with zero overlap, frozen bank manifest hash for all retrievers. Controlled `n` fractions realized by sampling test tasks where `n` fraction of parameterizable slots drawn from `B` and `1-n` from `A`, stratified by slot position and family. `n=0` tasks are exact-repeat sequences (test seq == training trajectory) so TERX/Stagehand hit_rate 1.0 reachable inside compared set.
- **Train:** 5 demos per family on `A` only. Registry one parameterized mechanism per family via actual `distill_parameterized` (not hard-coded). All fitting (TFIDF/embedding, distill) on TRAIN only. QCR ranker identical for RAG/SPIDER/TERX/Stagehand bank.
- **Test:** all 192 tasks evaluated once per method (paired design) at each `n` level. Total ~6*192=1152 +3 controls ~576 =1728 trials. Non-deterministic wrong-bound branches seeded.
- **Length:** `L` family-specific 8-14 constant within family varies across families; `n` and `L` orthogonal within strata by design.
- **Seeds:** `PYTHONHASHSEED=0 random.seed42 numpy RandomState42` for sampling, jitter, wrong-bound p=0.15, permutation. Deterministic. No outcome-bearing measurement before freeze.

## 7. Baselines, positive and null controls (strong baselines required, QCR)

**Baselines (identical 192-task splits, same verify fallback to B-COLD on miss, same frozen bank/ranker):**
- `B-COLD` cold start no memory upper bound.
- `B-INSTRUCTION` hand-authored instruction (200 tok amortized f=10 and f=100).
- `B-RAG-EMBED` QCR semantic retrieval top-1 verbatim bind Jaccard/embedding cosine retrieval 200+150ms, proportionally retrievable at n=0.25 (not binary n=0-only).
- `B-STAGEHAND-CACHE` shipped DOM-hash serverCache 50 tok+120ms hit iff DOM identical at n=0 (2000 nodes 1280x720).
- `B-TERX-REPLAY` 0-token exact replay 50 tok verify exact equality hit at n=0.
- `P-SPIDER-PARAM` SUT as above with non-deterministic mock, reports M_total_f10, M_total_f100, M_per_hit.

**Positive controls** `PC-BINDING-AND-EXACT-REPEAT`: PC1 exact-repeat cache must `hit_rate=1.0` at n=0 per_hit 50 tok success 1.0; PC2 parameterized binding on seen `A` 5/5 per family correctness 1.0 via `_bind`; PC3 non-vacuous verification: NC2 forced wrong-bound must yield false_accept in [0.10,0.60] proving mock can fail. Failure of any PC → `MEASUREMENT_INVALID`. BrowserGym health not gating (file-based) but report if Playwright used.

**Null controls** `NC-SHUFFLE-RANDOM-LENGTH`: NC1 shuffled slot mapping permute learned slots before resolve expect `|rho_per_hit|<0.25 p>=0.05` success<=COLD or false_accept 0.10-0.60; NC2 random mechanism `false_accept>=0.10` or `|rho|<0.35`; NC3 length-proportional `cost=L*500` expect `|rho|<0.25 R2<0.15` on both M_per_hit and M_total proving environment can express MIXED/FALSIFIED. All via actual pipeline with non-vacuous mock.

**Control identities frozen for EXECUTE/AUDIT:** `PC-BINDING-AND-EXACT-REPEAT`, `NC-SHUFFLE-RANDOM-LENGTH`, `B-COLD`, `B-RAG-EMBED`, `B-STAGEHAND-CACHE`, `B-TERX-REPLAY`, `P-SPIDER-PARAM`, `B-INSTRUCTION`, `B-LENGTH-PROPORTIONAL`.

## 8. Primary metric, expected direction, uncertainty method, adequacy

- **Primary metric:** `rho_novelty_per_hit = Spearman(M_per_hit, realized_n)` family-stratified pooled N~192.
- **Expected direction:** `>0` monotonic increasing with residual novelty. Secondary `rho_total`, `R2_delta_per_hit>0`, `|rho_length_per_hit|per_stratum|<0.20` flat vs length.
- **Uncertainty:** family-stratified bootstrap 5000 resamples (resample families with replacement then tasks within family) for 95% CI on `rho_per_hit, R2_delta_per_hit, cost ratios per_hit and total, rho_length_per_hit`. Block-permutation on family labels 5000 perms for two-sided `p`. Wilson 95% CI for rates. Heteroscedasticity-robust SE for slopes on both M_per_hit and M_total_f10. Degenerate CI [1,1] flagged degenerate not precision.
- **Adequacy rule:** `power>0.95` to detect `rho>=0.60 alpha0.01` requires `n>=44` (192 satisfies). ECE 5-bin on EXEC rows only derived confidence vs verify correctness `std>0.05`; 2-3 empty bins disclosed; bootstrap 2000 for ECE CI. No token shuffling. Per_hit isolation requires reporting both per_hit and total; Pareto appendix not gating.
- **QCR adequacy:** frozen bank hash logged; same ranker string logged; vary only post-retrieval verified via code inspection; proportional RAG at n=0.25 verified.

## 9. Decision / falsification / survival rule

Compute pooled family-stratified N~192 (file-based; gpt-4o-mini Docker exploratory if available does not gate):

- `success, false_accept, UNKNOWN_precision, ECE_exec 5-bin, M_total_f10, M_total_f100, M_per_hit per task, rho_novelty per_hit & total, R2_novelty, R2_length per stratum & pooled R2_delta per_hit, rho_length per stratum per_hit, Wilson CIs, bootstrap5000 CIs, block-permutation p, Pareto tokens/browser/latency`.

**SURVIVES_CURRENT_TEST iff ALL hold:**
- **C1** correctness+calibration: SPIDER `success at n0 >=0.85 (Wilson lower>=0.72)` mean across bins `>=0.80` `false_accept<=0.10` `UNKNOWN_precision>=0.85` `ECE_exec<=0.15` (derived confidence `std>0.05`, disclosed empty bins, PC3 non-vacuous verified) verification-derived.
- **C2** positive controls: PC1 `B-TERX and B-STAGEHAND hit_rate 1.0 at n0` inside compared set per_hit 50 tok success 1.0, PC2 SPIDER `5/5 per family binding 1.0` at n0 via `_bind`, PC3 NC2 `false_accept in [0.10,0.60]` when forced execute; failure → `MEASUREMENT_INVALID`.
- **C3** novelty tracking: `rho_novelty_per_hit>=0.60` `p<0.01` bootstrap95% lower `>0.35` `slope_per_hit>0 p<0.01`.
- **C4** residual explanatory power: `R2_delta_per_hit>=0.50 (R2_novelty_per_hit>=0.30)` and each stratum `|rho_length_per_hit|<0.20` (5 strata, no shuffling, per_hit metric).
- **C5** work compression honest: **C5-total** `SPIDER/COLD on M_total_f10 <=0.75 at n0 (>=25% saving) OR on M_total_f100 <=0.75 at n0 (sensitivity — if f=10 fails but f=100 passes grade MIXED not FALSIFIED; both fail ->FALSIFIED) AND SPIDER/COLD on M_total_f10 <=1.10 at n1 via UNKNOWN; **C5-perhit** `SPIDER/STAGEHAND on M_per_hit <=1.20 at n0` and `SPIDER/RAG-EMBED on M_per_hit <=0.85 at n0 and n0.25` and `SPIDER/TERX on M_per_hit <1.0 at every n>=0.25` under QCR.
- **C6** null controls: NC1 shuffled on M_per_hit `|rho|<0.25 p>=0.05 success<=COLD or false_accept 0.10-0.60`, NC2 `false_accept>=0.10 or |rho|<0.35`, NC3 `|rho|<0.25 R2<0.15` on M_per_hit (and total).

**Precedence:** If C2 fails → `MEASUREMENT_INVALID` irrespective of C3-C6. If C2 passes but C3 or C4 fail with C1 pass → `MIXED` (correct but per_hit cost flat — overhead dominates even after isolation). If C2 passes but C5-total both f fail or C5-perhit fails → `FALSIFIED` (no honest saving or no QCR advantage). If NC1 shows `rho>=0.35 significant` → `MEASUREMENT_INVALID` (novelty confounded). Degenerate bootstrap or shuffling manipulation → `MEASUREMENT_INVALID`. Pareto Appendix required but not gating. All thresholds two-sided `alpha0.01` primary.

## 10. Validity threats and mitigations

- **VF1 bijective formula:** mitigated by branch-derived cost sum inspection; auditor checks `run_experiment.py` has no `250+500*int(10n)` or `n*3200`.
- **VF2 shuffling:** forbidden; `|rho_length_per_hit|` reported honest per stratum without within-strata shuffling loop.
- **VF3/VF4 hardcoded calibration + vacuous mock:** verification-derived correctness, `softmax temp0.15+jitter` confidence not linear, `UNKNOWN_precision/ECE` derived not assigned; non-deterministic wrong-bound p=0.15 ensures false_accept can be >0; PC3 checks non-vacuity; auditor checks confidence generation and wrong-bound branch.
- **VF5 generic slots:** family-specific induction verified via `registry.jsonl` — all 36 mechanisms must not share identical `['path','store']`; field-path relevance check.
- **VF6 inflated hit costs:** Stagehand/TERX hits fixed 50 tok not 400; auditor recomputes cost_config with per_hit/total split.
- **VF7 structural unsatisfiability of C4/C5 under total cost:** mitigated by per_hit isolation (M_per_hit) and f=100 sensitivity; decision rule grades per_hit primary and allows MIXED if f=10 fails but f=100 passes.
- **VF10 synthetic ceiling:** disclosed as file-based mock not production DOM/cross-site/2000-node full-DOM; `validity_notes[0]` carries ceiling; scale-up to Docker/full-DOM gated behind this isolation.
- **VF11 QCR violation (retriever tuning illusion):** mitigated by frozen bank + same ranker protocol; retrieval quality saturates — post-retrieval adaptation is measured; auditor verifies ranker identity and bank hash.
- **History-dependence:** family-stratified bootstrap + block-permutation respects task-family correlation.
- **Leakage:** no test `B` identifier in train registry verbatim; TFIDF/distill from `A` only; `hidden_expected` not passed except verify; realized_n vs labelled_n disclosed.
- **Degenerate CI / empty ECE bins:** `[1,1]` flagged degenerate not high-precision; ECE with 2-3 empty bins disclosed, ECE_exec on EXEC rows only.
- **Wrong-bound rate misspecification:** p=0.15 chosen to make NC2 false_accept ~0.15 separable from SPIDER <=0.10; sensitivity ±50% proxy appendix if Docker replication available.

## 11. Product consequences

**If SURVIVES family-stratified per_hit and total (either f):** C-RESIDUAL-NOVELTY `HYPOTHESIS→EXPERIMENTAL` bounded to WebArena-Verified v2 file-based census 192/36 proxy with genuine kernel+freshness 0.25+UNKNOWN<0.80+non-vacuous mock under QCR. First per-hit-isolated non-bijective no-shuffling evidence later-agent cost tracks residual novelty (not length) with calibrated abstention and honest saving >=25% (f=10 or f=100) beating retrievable RAG (<=0.85x per_hit) and parity to shipped Stagehand/TERX under QCR. Unblocks `C-PRODUCT-ECON` amortized scale-up to Docker full-DOM + real LLM (effect size for f=100, Pareto tokens/browser/latency/retrieval/verification) and `C-LLM-INHERIT` QCR advantage. No `PRODUCT_CORE` promotion; replication with production Docker+real LLM+kernel-committed distill required before promotion.

**If FALSIFIED (controls PASS non-vacuous but rho_per_hit<0.35 or R2_delta_per_hit<0.15 or both f saving<25% or not beating Stagehand/RAG/TERX per_hit):** parameterization as ported does not yield residual-novelty-proportional compression on this aliasing mix, or only via miscalibration, or constant overhead dominates even per_hit (`MIXED` if per_hit rho passes but total economics fails). Product must NOT claim pay-cost-of-novelty for `C-RESIDUAL-NOVELTY/C-PRODUCT-ECON` on this setting; prioritize caching (Stagehand 2x ships) or freshness/delta-repair or semantic-resolve orthogonal before revisiting economics. Bounded REJECTED for proxy per_hit setting only, not global falsification.

**If MEASUREMENT_INVALID:** C-RESIDUAL-NOVELTY remains `HYPOTHESIS`; exact `failure.json` reason and smallest next action (e.g., fix kernel `distill_parameterized` double-prefix/Jaccard/field-path filter, adjust per_hit formula, restore 50-tok hit accounting, fix wrong-bound p, restore frozen bank).

## 12. Estimated cost and information gain

**Cost:** Low-moderate: 192 tasks ×6 conditions +3 controls ≈1152-1728 resolve/_bind/verify trials plus offline retrieval. File-based no Docker required; wall <40min CPU proxy (<90min if Playwright 2000 nodes); if gpt-4o-mini 15 steps Playwright ~2300 calls <$12. Storage per-task CSV ~1728 rows registry JSONL traces QCR manifest. No keys required proxy; ~$8-12 if real LLM exploratory.

**Expected information gain:** Very high — first per-hit-isolated non-bijective non-starved non-vacuous test after 2× MEASUREMENT_INVALID and 1× bounded FALSIFIED due to total-cost artefacts. Directly tests Director's per-hit/f=100 and non-vacuous mock hypotheses. Either valid positive (rho>=0.60 R2_delta>=0.50 per_hit |r|<0.20 beating shipped caches per_hit under QCR) or valid negative/MIXED (flat per_hit or no honest saving even at f=100 under QCR) decisively changes product decision: (1) whether `C-PRODUCT-ECON` Docker+real-LLM scale-up justified vs premature, (2) whether parameterized inheritance justifies productization despite exact-repeat cache dominance via per_hit economics, (3) whether residual-novelty holds beyond total-cost artefact to per_hit WebArena family hold-out with family-stratified CIs and Pareto decomposition. Resolves 44-deep frontier tunnel opportunity cost.

## 13. Consequences of positive and negative outcomes (product decision)

- **Positive (all C1-C6 pass per_hit):** advance claim ceiling to `EXPERIMENTAL`, keep `HYPOTHESIS` for production transfer; schedule Docker full-DOM + real `gpt-4o-mini` replication before any `PRODUCT_CORE`/`SHIPPED`; use measured `rho_per_hit`/`R2_delta_per_hit`/`saving_f10/f100`/`per_hit parity` as effect-size prior for pricing pay-for-novelty and Pareto frontier.
- **Negative (FALSIFIED/MIXED with controls PASS non-vacuous):** reframe pay-for-novelty claim, park `C-RESIDUAL-NOVELTY` for this kernel/cost model/QCR census, redirect product to Stagehand caching + freshness gating + delta-repair until stronger mechanism found; per_hit insight preserved for next design.

## 14. Artifacts and provenance (for AUDIT)

- `research/experiments/EXP-PRODUCT-35797365772/run_experiment.py` (produces branch-derived per_hit/total cost, non-deterministic wrong-bound branches)
- `artifacts/raw_per_task.csv` (task_id,family_id,labelled_n,realized_n,novelty_fraction,length,system,success,false_accept,unknown,precision,tokens,browser_calls,latency_ms,retrieval_ms,verification_ms,reused_steps,hit,verify_passed,repair_triggered,confidence,ECE_bin,M_total_f10,M_total_f100,M_per_hit,wrong_bound)
- `artifacts/registry.jsonl` (per-family mechanisms, parameter_slots, confidence, templates, evidence_values)
- `artifacts/cost_config.json` (retrieval/verify/hit/repair/distill constants, f=10/f=100, per_hit formula)
- `artifacts/branch_traces.json` (executed branch per task, wrong_bound counts)
- `artifacts/qcr_bank_manifest.json` (frozen bank hash, ranker name/version, same-ranker verification)
- `artifacts/derived_metrics.json` (rho_per_hit, R2_delta_per_hit, per_hit parity ratios, bootstrap CIs, Pareto table)
- `fixtures/tasks.json` (census manifest hash, 192 tasks with labelled_n and realized_n)
- `provenance.json` (run id, commits, hashes, seeds, Playwright/BrowserGym version pin, embedding model name, Docker availability flag)
- No outcome file edited after freeze; `freeze.json` hashes request/spec/prereg before `result.json`.

*Preregistered without inspecting outcomes. Outcome-bearing code not executed before freeze. Any post-freeze analysis change is exploratory and requires new preregistration for confirmatory claim.*

