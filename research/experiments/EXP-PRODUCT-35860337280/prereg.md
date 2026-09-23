# EXP-PRODUCT-35860337280 preregistration — Product honest residual-novelty economics (Director PIVOT C-RESIDUAL-NOVELTY honest-cost gate)

**Lane:** product — `PIVOT C-RESIDUAL-NOVELTY` per Global Research Director mandate cycle 35859819467 (SUPERSEDE disposition, parent_handoff EXP-PRODUCT-35797365772)
**Claims:** C-RESIDUAL-NOVELTY (primary), C-PRODUCT-ECON (economics via same thresholds)
**Status before:** HYPOTHESIS (prior EXP-PRODUCT-35797365772 FALSIFIED boundedly: ρ 0.82 R² 0.75 but SPIDER/RAG per_hit 1.0→1.57 >0.85, SPIDER/TERX 1.0 at n≥0.5 not <1.0, 71.9% UNKNOWN fallback to COLD makes ρ/R² binary-gating artifact not proportional tracking; prior 26+8 product experiments MEASUREMENT_INVALID via bijective cost formula int(n*3200) and hardcoded confidence and inflated hit costs 400 tok)
**Date frozen:** 2026-09-23Txx:xx freeze.json (no outcome-bearing measurement before freeze)

## 1. Strategic question (Director mandate binding, verbatim refinement)

With genuine branch-derived cost from actual kernel resolve/_bind/verify/freshness gating 0.25/UNKNOWN<0.80 (no n*3200 formula, no token shuffling, verification-derived UNKNOWN precision and ECE from kernel softmax temp 0.15+jitter), family-specific slot induction (not generic path/store), honest Stagehand/TERX 50-tok hit costs, 5000 family-stratified bootstraps and block-permutation on WebArena-Verified v2 36 families >=3 (192 tasks, 49 templates, duplication 0.9479, param_task 0.8958) with controlled novelty fraction 0/25/50/75/100% (train A test never-observed B), does later-agent cost (tokens+browser+retrieval+reconstruction+verification+repair amortized at f=10) track residual novelty (Spearman rho_novelty>=0.60 R2_delta>=0.50) rather than full task length (|rho_length| per stratum <0.20) with honest saving>=25% vs COLD at f=10 and <=0.85x vs RAG-EMBED and parity <=1.20x at n=0 to Stagehand DOM-hash, false_accept<=0.10 UNKNOWN_precision>=0.85 ECE<=0.15, reporting Pareto vs gpt-4o-mini+Playwright Docker replication?

Inherited `parent_handoff` EXP-PRODUCT-35797365772 is continuity evidence only. Per Director PIVOT/SUPERSEDE, its `established/rejected/unknown/do_not_assume` are preserved below but do not override mandate. Its `next_question` (0.25→0.50 threshold sweep alone) is advisory; mandate question above is binding and we retain gating 0.25 as mandated (not 0.50) to test honest-cost without threshold relaxation.

## 2. What is established / rejected / unknown (from handoff carry_forward, preserved exactly)

**Established to reuse:**
- WebArena-Verified v2 proxy file-based census 192 tasks /36 families /49 templates /duplication 0.9479 /param_task 0.8958 /L 8-14 family-specific slots ${sku},${store_id},${variant},${category} via actual src/spider/kernel.py distill_parameterized Jaccard>=0.75 constant-anchor structure-similarity>=0.75 field-path relevance exists as committed code (artifacts/registry.jsonl 36 mechanisms distinct, fixtures/tasks.json sha f9537168, provenance kernel hash 04ca13d0)
- Positive controls PASS via genuine kernel resolve/_bind/verify with non-vacuous MockEnv p=0.15: PC1 B-TERX and B-STAGEHAND hit_rate 1.0 at n0 per_hit 50 tok success 1.0 (n=36), PC2 SPIDER binding_correctness 1.0 at n0 via _bind (36/36), PC3 NC2 forced wrong-bound false_accept 0.3125 in [0.10,0.60] proving mock can fail
- C3/C4 technically PASS on per_hit isolated metric M_per_hit=(M_total_f10 - retrieval - distill)/L: rho_novelty_per_hit 0.8199 CI[0.749,0.876] block-perm p0.0002 slope 432 p<1e-9, R2_delta_per_hit 0.751, |rho_length| per stratum 0.0 to -0.001 (all <0.20) via honest branch-derived cost sums no bijective formula no shuffling (5000 bootstrap/permutation seeds PYTHONHASHSEED0/42)
- RAG-EMBED under QCR frozen bank TFIDF Jaccard TAU0.30 same ranker demonstrates proportional cost scaling: per_hit 50 at n0, 203 at n0.25, 340.6 at n0.5, 453 at n0.75, 500 at n1 proving census can express residual-novelty-proportional economics
- Family-stratified bootstrap 5000 and block-permutation 5000 correctly implemented in stdlib Random42, deterministic, no degenerate [1,1] beyond disclosed

**Rejected (bounded, not global):**
- SPIDER parameterized inheritance with frozen behavioral freshness gating 0.25 does NOT achieve per_hit parity/advantage to shipped baselines under QCR on this proxy census: SPIDER/RAG per_hit 1.0 at n0 (>0.85) and 1.573 at n0.25 (>0.85), SPIDER/TERX per_hit 1.0 at n>=0.5 not <1.0, SPIDER/STAGEHAND per_hit 1.0 at n0 passes parity but SPIDER more expensive per_hit than RAG at partial novelty
- SPIDER per_hit novelty tracking and R2_delta are not proportional pay-for-novelty: 71.9% UNKNOWN means SPIDER mean per_hit = COLD 500 at n>=0.5 and 319.7 vs RAG 203 at n0.25, rho 0.82 and R2 0.75 reflect binary gating step (hit at n0 vs UNKNOWN fallback) not step-level parameterization
- Per_hit isolation alone does not rescue product economics: C5 total saving >=25% vs COLD holds (0.163 at n0) but C5-perhit still fails shipped baseline advantage where baselines honestly hit under QCR; Stagehand/TERX binary at n0 only, RAG proportional retrievable at n0.25 is stronger baseline
- UNKNOWN_precision 1.0 and ECE_exec 0.025 on EXEC n=54 with 4/5 empty bins are not validated abstention/calibration when SPIDER falls back to COLD with 71.9% UNKNOWN

**Unknown targeted (this experiment):**
- Whether honest branch-derived cost with family-specific slots and 50-tok Stagehand/TERX hits and non-vacuous MockEnv yields rho>=0.60 R2_delta>=0.50 per_hit |rho_length|<0.20 with saving>=25% vs COLD at f=10 and beating RAG <=0.85x per_hit and parity to Stagehand <=1.20x — closing or opening work-compression claim per Director
- Whether SPIDER maintains UNKNOWN_precision>=0.85 ECE<=0.15 and false_accept<=0.10 if it actually executes at n>0 with non-vacuous wrong-bound rate 0.15 discriminating calibration (not vacuous fallback)
- Whether proxy branch-derived costs correlate with real gpt-4o-mini+Playwright Docker tokens/browser/latency and preserve Pareto vs COLD/RAG/Stagehand (exploratory replication)
- Whether per_hit metric including vs excluding verification_tokens (50 per task ~6.25/step) changes parity (disclosed) — we exclude retrieval+distill per_hit as mandated
- Whether QCR frozen-bank same-ranker with trajectory-grouped CIs removes retriever-tuning illusion

**Do-not-assume (preserved):**
- Do not assume rho 0.82 / R2 0.75 / slope 432 demonstrate proportional tracking; they are driven by binary freshness gating (UNKNOWN fallback) not parameterized step reuse
- Do not assume C4 per_hit |rho_length|<0.20 success alone validates product economics; C5 per_hit vs shipped RAG/TERX still fails under QCR with proportional RAG at n0.25
- Do not assume success 1.0 / false_accept 0 / UNKNOWN_precision 1.0 / ECE 0.025 indicate calibrated abstention; SPIDER mean success 1.0 with 71.9% UNKNOWN fallback to always-success COLD makes precision vacuous and EXEC ECE based on n=54 with 4/5 empty bins
- Do not assume NC1 shuffled control validates absence of confounding if hardcoded COLD fallback; must be actual kernel shuffled execution
- Do not assume file-based synthetic census 192/36 transfers to production WebArena Docker full-DOM 2000 nodes 1280x720 or cross-site or 800-element full-DOM or real LLM token economics
- Do not assume per_hit formula excluding verification_tokens is neutral; disclose when comparing absolute values
- Do not assume audit REVISE is PASS; producer_claim_supported false bars VALIDATED/PRODUCT_CORE until required fixes 1-6 addressed
- Do not assume total-cost saving at f10 (0.163) alone proves commercial viability; Pareto tokens/browser/latency/retrieval/verification not dominated until per_hit baseline parity achieved

Per Director comparative_reasoning: continuing another novelty sweep with bijective cost produces vacuous rho>0.60 with zero information gain; honest-cost file census with non-vacuous UNKNOWN/ECE + family-stratified bootstrap + block permutation is feasible now on existing 192/36 census and, if it fails per-hit <=0.85x RAG, definitively closes current work-compression claim and forces pivot to curated exploration + auditor harness (MEA pattern).

## 3. Hypothesis (falsifiable)

Later-agent cost under SPIDER parameterized inheritance (family-specific slot induction Jaccard>=0.75 constant-anchor structure-similarity>=0.75 field-path relevance body.*|headers.*|url, behavioral freshness probe Flask JWT HS256 0.8 on 401/403 vs 0 on 200 gating 0.25, confidence softmax temp0.15+jitter uniform [-0.05,0.05] UNKNOWN<0.80 ECE<=0.15, verify+repair 500 tok+2 calls on fail fallback to COLD) tracks residual novelty fraction n ∈ {0,0.25,0.50,0.75,1.00} (train A test B within family) with per_hit Spearman rho_novelty>=0.60 (p<0.01, 5000 bootstrap CI lower>0.35, slope>0 p<0.01) and R2_delta>=0.50 (R2_novelty>=0.30) while per_hit cost vs length within each stratum is flat (|rho_length| per stratum <0.20 on M_per_hit). At n=0 honest saving >=25% vs B-COLD on M_total_f10 (SPIDER/COLD <=0.75) with per_hit parity to shipped caches (M_per_hit SPIDER/STAGE <=1.20 at n=0, SPIDER/RAG <=0.85 at 0 and 0.25, SPIDER/TERX <1.0 at >=0.25 under QCR). At n=1 UNKNOWN fallback keeps total cost <=1.10x COLD with false_accept<=0.10 UNKNOWN_precision>=0.85 ECE_exec<=0.15 verification-derived non-vacuous (MockEnv wrong-bound p=0.15).

Null: flat per_hit cost vs novelty (rho~0 R2_delta~0) or no honest saving/per_hit advantage vs strong QCR baselines (Stagehand/TERX 50-tok hits, RAG proportional at n0.25).

## 4. State / action / observation representation

**State representation:** file-based task `state` dict with WebArena family workflow fields (category, product_spec, cart, auth mock) plus `preconditions` (family-specific workflow search→filter→open→select→add→checkout→verify). If /tmp/webarena census JSON present, use real intents/params; else synthetic mock exactly replicating 36/49 structure, disclosed ceiling synthetic/WebArena-inspired not production DOM (2000-node DOM simulated via hash if Playwright not used). Duplication 0.9479 param_task 0.8958.

**Action representation:** SPIDER `Mechanism.action_template` with family-specific slots `${sku},${store_id},${variant},${category}` (field-path-relevant body.*, headers.*, url only) not generic ['path','store']. Bound via `src/spider/kernel.py _bind` checking `required_slots = parameter_slots | template_slots`. Template slots induced via `_extract_varying_values` with Jaccard>=0.75 constant-anchor + structure-similarity>=0.75.

**Observation:** `Observation(intent, state, action, next_state, success, provenance)` per `src/spider/models.py`. `SpiderKernel.observe` hashes raw; `distill_parameterized` induces one parameterized `Mechanism` per family from 5 A demos gathering varying values via Jaccard>=0.75 + structure-similarity>=0.75 + constant-value anchor + field-path filter (excludes top-level metadata). Registry `MechanismRegistry` exercised and hashed.

**Non-deterministic MockEnv extension (non-vacuous):** Deterministic branch (evidence-membership) retained for SPIDER correct binding, but NC1 shuffled / NC2 random forced-execute branches emit wrong-bound action with p=0.15 (seeded Random42) that fails verify (postcondition mismatch) -> false_accept>0. Correct SPIDER binding at n=0 never triggers wrong-bound. This makes false_accept and UNKNOWN_precision discriminating while preserving honest cost branches (audit required_fix5). Confidence via softmax temp0.15+jitter not linear 0.95-n*0.12.

All representations preserved raw in `artifacts/raw_per_task.csv` (adds realized_n, M_per_hit, M_total_f10, retrieval_ms, verification_ms) and `registry.jsonl` plus `qcr_bank_manifest.json`. Representation loss (mock vs real WebArena AX tree/DOM 2000 nodes, generic vs family-specific, wrong-bound rate 0.15 synthetic) disclosed in validity_notes.

## 5. Target (primary outcome)

Per-task costs (Director f=10 only):
```
M_total_f10  = retrieval(200 tok+150ms) + verify(50 tok+120ms) + sum_step[ hit 50tok+1 call | novel/failed 500tok+2 calls | repair 500tok+2 calls on fail ] + distill 1000/10 (100 SPIDER else 0)
M_per_hit    = (M_total_f10 - retrieval - distill_amort) / L   // cost per step excluding fixed overhead, primary for |rho_length| and QCR parity per Director per_hit gate
```
All genuine branch-derived sums, not bijective formulas (no 250+500*int(10n), no n*3200). Latency ms reported but primary metric is token+call derived cost. If gpt-4o-mini+Playwright available, report real tokens/browser calls alongside proxy with ±50% sensitivity and correlation rho_proxy_real as exploratory Pareto appendix (does not gate SURVIVES).

Primary statistical target: `Spearman rho_novelty` between `M_per_hit` and `realized_n` (family-stratified, realized_n = round_half_up(labelled_n*S)/S for S=1/2). Secondary rho on M_total_f10. Also R2_delta_per_hit = R2_novelty - R2_length pooled and per stratum.

## 6. Sampling policy and hold-out (QCR, Director honest-cost)

- **Census:** 192 tasks across 36 families >=3 (49 templates). Attempt /tmp/webarena or repo-cached JSON; if absent generate synthetic mock exactly matching family/template/duplication 0.9479/param_task 0.8958 ratios, disclose synthetic ceiling. All tasks carry labelled_n and realized_n. Manifest+hashes+seeds logged.
- **Within-family hold-out under QCR:** per family disjoint `A(train)` / `B(test never-observed)` identifier pools with zero overlap, frozen bank manifest hash for all retrievers. Controlled `n` fractions realized by sampling test tasks where `n` fraction of parameterizable slots drawn from `B` and `1-n` from `A`, stratified by slot position and family. `n=0` tasks are exact-repeat sequences (test seq == training trajectory) so TERX/Stagehand hit_rate 1.0 reachable inside compared set (fixes prior starvation).
- **Train:** 5 demos per family on `A` only. Registry one parameterized mechanism per family via actual `distill_parameterized` (not hard-coded). All fitting (TFIDF/embedding, distill) on TRAIN only. QCR ranker identical for RAG/SPIDER/TERX/Stagehand bank (TFIDF Jaccard TAU0.30 or all-MiniLM-L6-v2 if available, logged).
- **Test:** all 192 tasks evaluated once per method (paired design) at each `n` level. Total 5*192=960 +3 controls ~576 =1536 trials. Non-deterministic wrong-bound branches seeded Random42.
- **Length:** `L` family-specific 8-14 constant within family varies across families; `n` and `L` orthogonal within strata by design.
- **Seeds:** `PYTHONHASHSEED=0 random.seed42 numpy RandomState42` for sampling, jitter, wrong-bound p=0.15, permutation. Deterministic. No outcome-bearing measurement before freeze.

## 7. Baselines, positive and null controls (strong baselines required, QCR, 50-tok honest hits)

**Baselines (identical 192-task splits, same verify fallback to B-COLD on miss, same frozen bank/ranker, 50-tok hit costs not 400):**
- `B-COLD` cold start no memory upper bound.
- `B-RAG-EMBED` QCR semantic retrieval top-1 verbatim bind Jaccard/embedding retrieval 200+150ms, proportionally retrievable at n=0.25 (not binary n=0-only) — varies only post-retrieval.
- `B-STAGEHAND-CACHE` shipped DOM-hash serverCache 50 tok+120ms hit iff DOM identical at n=0 (2000 nodes 1280x720) — honest 50 tok not 400.
- `B-TERX-REPLAY` 0-token exact replay 50 tok verify exact equality hit at n=0 — honest 50 tok not 400.
- `P-SPIDER-PARAM` SUT as above with non-deterministic mock, reports M_total_f10, M_per_hit, calibration.

**Positive controls** `PC-BINDING-AND-EXACT-REPEAT`: PC1 exact-repeat cache must `hit_rate=1.0` at n=0 per_hit 50 tok success 1.0; PC2 parameterized binding on seen `A` 5/5 per family correctness 1.0 via `_bind`; PC3 non-vacuous verification: NC2 forced wrong-bound must yield false_accept in [0.10,0.60] proving mock can fail. Failure of any PC → `MEASUREMENT_INVALID`. BrowserGym health not gating (file-based) but report if Playwright used (health>=80% AX>10).

**Null controls** `NC-SHUFFLE-RANDOM-LENGTH`: NC1 shuffled slot mapping permute learned slots before resolve expect `|rho_per_hit|<0.25 p>=0.05` success<=COLD or false_accept 0.10-0.60; NC2 random mechanism `false_accept>=0.10` or `|rho|<0.35`; NC3 length-proportional `cost=L*500` expect `|rho|<0.25 R2<0.15` on both M_per_hit and M_total_f10 proving environment can express MIXED/FALSIFIED. All via actual pipeline with non-vacuous mock.

**Control identities frozen for EXECUTE/AUDIT:** `PC-BINDING-AND-EXACT-REPEAT`, `NC-SHUFFLE-RANDOM-LENGTH`, `B-COLD`, `B-RAG-EMBED`, `B-STAGEHAND-CACHE`, `B-TERX-REPLAY`, `P-SPIDER-PARAM`.

## 8. Primary metric, expected direction, uncertainty method, adequacy

- **Primary metric:** `rho_novelty_per_hit = Spearman(M_per_hit, realized_n)` family-stratified pooled N~192.
- **Expected direction:** `>0` monotonic increasing with residual novelty. Secondary `rho_total`, `R2_delta_per_hit>0`, `|rho_length_per_hit|per_stratum|<0.20` flat vs length.
- **Uncertainty:** family-stratified bootstrap 5000 resamples (resample families with replacement then tasks within family) for 95% CI on `rho_per_hit, R2_delta_per_hit, cost ratios per_hit and total, rho_length_per_hit`. Block-permutation on family labels 5000 perms for two-sided `p` (Director-mandated 5000). Wilson 95% CI for rates. Heteroscedasticity-robust SE for slopes on both M_per_hit and M_total_f10. Degenerate CI [1,1] flagged degenerate not precision.
- **Adequacy rule:** `power>0.95` to detect `rho>=0.60 alpha0.01` requires `n>=44` (192 satisfies). ECE 5-bin on EXEC rows only derived confidence vs verify correctness `std>0.05`; 2-3 empty bins disclosed; bootstrap 2000 for ECE CI. No token shuffling. Per_hit isolation requires reporting both per_hit and total; Pareto appendix not gating but required.
- **QCR adequacy:** frozen bank hash logged; same ranker string logged; vary only post-retrieval verified via code inspection; proportional RAG at n=0.25 verified; trajectory-grouped CIs (family-stratified) respect dependency per Director agent prior.

## 9. Decision / falsification / survival rule

Compute pooled family-stratified N~192 (file-based; gpt-4o-mini Docker exploratory if available does not gate):

- `success, false_accept, UNKNOWN_precision, ECE_exec 5-bin, M_total_f10, M_per_hit per task, rho_novelty per_hit & total, R2_novelty, R2_length per stratum & pooled R2_delta per_hit, rho_length per stratum per_hit, Wilson CIs, bootstrap5000 CIs, block-permutation 5000 p, Pareto tokens/browser/latency`.

**SURVIVES_CURRENT_TEST iff ALL hold:**
- **C1** correctness+calibration: SPIDER `success at n0 >=0.85 (Wilson lower>=0.72)` mean across bins `>=0.80` `false_accept<=0.10` `UNKNOWN_precision>=0.85` `ECE_exec<=0.15` (derived confidence `std>0.05`, disclosed empty bins, PC3 non-vacuous verified) verification-derived.
- **C2** positive controls: PC1 `B-TERX and B-STAGEHAND hit_rate 1.0 at n0` inside compared set per_hit 50 tok success 1.0, PC2 SPIDER `5/5 per family binding 1.0` at n0 via `_bind`, PC3 NC2 `false_accept in [0.10,0.60]` when forced execute; failure → `MEASUREMENT_INVALID`.
- **C3** novelty tracking: `rho_novelty_per_hit>=0.60` `p<0.01` bootstrap95% lower `>0.35` `slope_per_hit>0 p<0.01`.
- **C4** residual explanatory power: `R2_delta_per_hit>=0.50 (R2_novelty_per_hit>=0.30)` and each stratum `|rho_length_per_hit|<0.20` (5 strata, no shuffling, per_hit metric).
- **C5** work compression honest: **C5-total** `SPIDER/COLD on M_total_f10 <=0.75 at n0 (>=25% saving per Director)` AND `SPIDER/COLD on M_total_f10 <=1.10 at n1 via UNKNOWN`; **C5-perhit** `SPIDER/STAGEHAND on M_per_hit <=1.20 at n0` and `SPIDER/RAG-EMBED on M_per_hit <=0.85 at n0 and n0.25` and `SPIDER/TERX on M_per_hit <1.0 at every n>=0.25` under QCR with honest 50-tok hits.
- **C6** null controls: NC1 shuffled on M_per_hit `|rho|<0.25 p>=0.05 success<=COLD or false_accept 0.10-0.60`, NC2 `false_accept>=0.10 or |rho|<0.35`, NC3 `|rho|<0.25 R2<0.15` on M_per_hit.

**Precedence:** If C2 fails → `MEASUREMENT_INVALID` irrespective of C3-C6. If C2 passes but C3 or C4 fail with C1 pass → `MIXED` (correct but per_hit cost flat — novelty tracking fails). If C2 passes but C5-total or C5-perhit fails → `FALSIFIED` (no honest saving or no QCR advantage per Director). If NC1 shows `rho>=0.35 significant` → `MEASUREMENT_INVALID` (novelty confounded). Degenerate bootstrap or shuffling manipulation → `MEASUREMENT_INVALID`. Pareto appendix required but not gating. All thresholds two-sided `alpha0.01` primary, calibration alpha0.05 secondary.

Director comparative reasoning applied: failing per-hit <=0.85x RAG even with rho>=0.60 definitively closes current work-compression claim and forces pivot to curated exploration + auditor harness (fresh-context execution + external verified state MEA pattern).

## 10. Validity threats and mitigations

- **VF1 bijective formula:** mitigated by branch-derived cost sum inspection; auditor checks `run_experiment.py` has no `250+500*int(10n)` or `n*3200` or `int(n*3200)`; cost is sum of branches per Director.
- **VF2 shuffling/token shuffling:** forbidden; `|rho_length_per_hit|` reported honest per stratum without within-strata shuffling; agent prior flags cost=250+500*10*novelty tautology — blocked via branch-derived cost.
- **VF3/VF4 hardcoded calibration + vacuous mock (71% UNKNOWN fallback):** verification-derived correctness, `softmax temp0.15+jitter` confidence not linear 0.95-n*0.12, `UNKNOWN_precision/ECE` derived not assigned; non-deterministic wrong-bound p=0.15 ensures false_accept can be >0; PC3 checks non-vacuity; auditor checks confidence generation and wrong-bound branch; trajectory-grouped CIs respect dependency (Director prior on inflated rho when cost bijective).
- **VF5 generic slots ['path','store']:** family-specific induction verified via `registry.jsonl` — all 36 mechanisms must have distinct ${sku},${store_id},${variant},${category} not identical generic; field-path relevance check body.*|headers.*|url.
- **VF6 inflated hit costs (400 tok):** Stagehand/TERX hits fixed 50 tok not 400 per Director honest 50-tok hit costs; auditor recomputes cost_config with per_hit/total split; prior SPIDER/STAGE 1.50x was artifact of total-cost including retrieval/distill — per_hit isolation fixes.
- **VF7 structural unsatisfiability of C4/C5 under total cost:** mitigated by per_hit isolation (M_per_hit) per handoff insight — RAG proportional at n0.25 proves environment can express proportional scaling; decision rule grades per_hit primary for |rho_length| and QCR parity.
- **VF8 Context rot / long-horizon compounding errors:** mitigated by fresh-context execution + external verified state pattern per Director prior — not tested here but motivates UNKNOWN gate; we measure UNKNOWN_precision/ECE to require independent verification before state update.
- **VF9 Caching/replay baseline deceptively strong on deterministic SPA (recall@k=1.0 when registry<=k, Stagehand 80% speedup):** mitigated by QCR frozen-bank same-ranker, correct-family-required binding, header/body/auth parameterization, and per_hit <=0.85x RAG at n0.25 (not just n0) where registry<=k tautology would still give RAG hit but SPIDER must still win via parameterization.
- **VF10 synthetic ceiling:** disclosed as file-based mock not production DOM/cross-site/2000-node full-DOM 2k tokens; `validity_notes[0]` carries ceiling; scale-up to Docker/full-DOM gated behind this honest-cost gate per Director (do not wait for full Docker before fixing file census).
- **VF11 QCR violation (retriever tuning illusion):** mitigated by frozen bank + same ranker protocol; retrieval quality saturates — post-retrieval adaptation is measured; auditor verifies ranker identity and bank hash TAU0.30; proportional RAG at n0.25 verifies not binary.
- **VF12 History-dependence / family correlation:** family-stratified bootstrap + block-permutation respects task-family correlation per Director trajectory-grouped CIs; 5000 iterations.
- **Leakage:** no test `B` identifier in train registry verbatim; TFIDF/distill from `A` only; `hidden_expected` not passed except verify; realized_n vs labelled_n disclosed S=1/2 collapse.
- **Degenerate CI / empty ECE bins:** `[1,1]` flagged degenerate not high-precision; ECE with 2-3 empty bins disclosed, ECE_exec on EXEC rows only n=54 in prior shows risk — we require std>0.05 and 2000 bootstrap for ECE CI.
- **Wrong-bound rate misspecification:** p=0.15 chosen to make NC2 false_accept ~0.15 separable from SPIDER <=0.10; sensitivity disclosed.

## 11. Product consequences (Director binding)

**If SURVIVES family-stratified per_hit and total at f=10:** C-RESIDUAL-NOVELTY `HYPOTHESIS→EXPERIMENTAL` bounded to WebArena-Verified v2 file-based census 192/36 proxy with genuine kernel+freshness 0.25+UNKNOWN<0.80+non-vacuous mock under QCR (ECE<=0.15 precision>=0.85 false_accept<=0.10). First honest per-hit-isolated evidence later-agent cost tracks residual novelty (rho>=0.60 R2_delta>=0.50 not length |r|<0.20) with honest saving >=25% vs COLD beating retrievable RAG (<=0.85x per_hit) and parity to shipped Stagehand/TERX under QCR. Unblocks `C-PRODUCT-ECON` amortized scale-up to Docker full-DOM+real LLM (runtime replication prerequisites, effect size for f=10, Pareto tokens/browser/latency/retrieval/verification) and `C-LLM-INHERIT` QCR advantage. No `PRODUCT_CORE` promotion; replication with production Docker hosting+real LLM+kernel-committed distill required before promotion. Use measured rho/R2/saving as pricing prior and Pareto frontier (accuracy vs total cost vs median latency, 50-tok hit honest).

**If FALSIFIED (controls PASS non-vacuous but rho_per_hit<0.35 or R2_delta_per_hit<0.15 or saving<25% on M_total_f10 or not beating Stagehand/RAG/TERX per_hit where they honestly hit under QCR):** parameterization as ported does not yield residual-novelty-proportional compression on this aliasing mix, or only via miscalibration, or constant overhead dominates even per_hit (`MIXED` if rho passes but economics fails). Product must NOT claim pay-cost-of-novelty for `C-RESIDUAL-NOVELTY/C-PRODUCT-ECON` on this setting; prioritize caching (Stagehand 2000-node DOM-hash already ships 80% speedup zero tokens) or freshness/delta-repair or semantic-resolve orthogonal before revisiting economics. Per Director comparative reasoning, failing per_hit <=0.85x RAG definitively closes current work-compression claim and forces pivot to curated exploration + auditor harness (fresh-context execution + external verified state). Bounded REJECTED for proxy per_hit honest-cost setting only, not global falsification. No promotion; invest in kernel or richer DOM/QCR post-retrieval before re-testing. Pareto will show where cost accumulates.

**If MEASUREMENT_INVALID:** C-RESIDUAL-NOVELTY remains `HYPOTHESIS`; exact `failure.json` reason and smallest next action (e.g., fix kernel `distill_parameterized` Jaccard/field-path filter, adjust per_hit formula, restore 50-tok hit accounting, fix wrong-bound p=0.15, restore frozen bank TAU0.30, restore family-stratified bootstrap/block-permutation 5000).

## 12. Estimated cost and information gain

**Cost:** Low-moderate: 192 tasks ×5 conditions +3 controls ≈1536 resolve/_bind/verify trials plus offline TFIDF retrieval. File-based no Docker required; wall <40min CPU proxy (<90min if Playwright 2000 nodes 1280x720); if gpt-4o-mini 15 steps Playwright ~2000 calls <$12. Storage per-task CSV ~1536 rows registry JSONL cost_config traces QCR bank manifest. No LLM keys required for proxy; ~$8-12 if real LLM exploratory Docker replication.

**Expected information gain:** Very high — Director-designated honest-cost file census gate to resolve 271-experiment stall (zero VALIDATED/PRODUCT_CORE, 60 synthetic harnesses re-testing tautologies). First test on existing 192/36 census without waiting for BrowserGym Docker isolation but with genuine branch-derived cost (fixes bijective rho 0.97-0.995), family-specific slots (fixes generic ['path','store']), 50-tok honest Stagehand/TERX hits (fixes 400-tok inflation), non-vacuous UNKNOWN/ECE via softmax temp0.15+jitter p=0.15, and trajectory-grouped family-stratified bootstrap+block-permutation 5000 (fixes inflated novelty-cost correlation when cost bijective). Either valid positive (rho>=0.60 R2_delta>=0.50 per_hit |r|<0.20 beating shipped RAG <=0.85x) or valid negative (fails per_hit despite rho, SPIDER/RAG 1.12-1.57 as before) decisively changes product architecture decision (mechanism distillation vs selector cache vs fine-tuning) and determines whether C-PRODUCT-ECON Docker scale-up justified vs premature. Provides DolphinBench-style Pareto (accuracy vs total cost vs median latency, tokens/browser/latency/retrieval/verification) for commercial viability without another MEASUREMENT_INVALID loop.

## 13. Consequences of positive and negative outcomes (product decision)

- **Positive (all C1-C6 pass per_hit at f=10 as above):** advance claim ceiling to `EXPERIMENTAL` bounded to file-based proxy, keep `HYPOTHESIS` for production transfer; schedule Docker full-DOM 2000-node + real `gpt-4o-mini` replication before any `PRODUCT_CORE`/`SHIPPED`; use measured `rho_per_hit`/`R2_delta_per_hit`/`saving_f10`/`per_hit parity ratios` as effect-size priors for pricing pay-for-novelty and Pareto frontier; prioritize mechanism distillation productization despite Stagehand dominance at exact repeat via per_hit economics.
- **Negative (FALSIFIED/MIXED with controls PASS non-vacuous, per_hit fails <=0.85x RAG or saving<25%):** reframe pay-for-novelty claim, park `C-RESIDUAL-NOVELTY` for this kernel/cost model/QCR census per Director termination of bounded thread, redirect product lane to Stagehand caching 80% speedup + freshness gating (TTL/ETag SWR verification probe) + delta-repair orthogonal levers until stronger mechanism (curated exploration + auditor harness MEA) found; per_hit isolation insight preserved for next design but current work-compression claim closed.

## 14. Artifacts and provenance (for AUDIT)

- `research/experiments/EXP-PRODUCT-35860337280/run_experiment.py` (produces branch-derived per_hit/total cost, non-deterministic wrong-bound p=0.15, QCR frozen bank TAU0.30, 5000 bootstrap/permutation)
- `artifacts/raw_per_task.csv` (task_id,family_id,labelled_n,realized_n,novelty_fraction,length,system,success,false_accept,unknown,precision,tokens,browser_calls,latency_ms,retrieval_ms,verification_ms,reused_steps,hit,verify_passed,repair_triggered,confidence,ECE_bin,M_total_f10,M_per_hit,wrong_bound,qcr_bank_hit)
- `artifacts/registry.jsonl` (per-family mechanisms, parameter_slots distinct family-specific, confidence, templates, evidence_values, distill hash)
- `artifacts/cost_config.json` (retrieval 200/verify 50/hit 50/repair 500/distill 1000/f10 constants, f=10, per_hit formula (M_total_f10 - retrieval - distill)/L, honest 50-tok Stagehand/TERX verification)
- `artifacts/branch_traces.json` (executed branch per task, wrong-bound counts p=0.15)
- `artifacts/qcr_bank_manifest.json` (frozen bank hash, ranker name TFIDF Jaccard TAU0.30 same-ranker verification, 36 families)
- `artifacts/derived_metrics.json` (rho_per_hit, R2_delta_per_hit, per_hit parity ratios SPIDER/RAG/STAGEHAND/TERX, bootstrap 5000 CIs, block-permutation 5000 p, Pareto table accuracy vs total cost vs median latency)
- `fixtures/tasks.json` (census manifest hash, 192 tasks with labelled_n and realized_n, 49 templates duplication 0.9479 param_task 0.8958)
- `provenance.json` (run id, commits, hashes, seeds PYTHONHASHSEED0/42, Playwright/BrowserGym version pin if used, embedding model name, QCR bank hash, Docker availability flag, numpy unavailable disclosure, cost_config hash)
- No outcome file edited after freeze; `freeze.json` hashes request/spec/prereg before `result.json`. Deterministic seeds logged.

*Preregistered without inspecting outcomes. Outcome-bearing code not executed before freeze. Any post-freeze analysis change is exploratory and requires new preregistration for confirmatory claim. Branch-derived cost before outcome inspection.*
