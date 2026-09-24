# EXP-PRODUCT-35999358218 — Preregistration (Product PIVOT C-PRODUCT-ECON — honest M_total Pareto supersession)

**Lane:** product — **Claims:** C-PRODUCT-ECON (primary, formally superseding falsified per_hit) gated to C-LLM-INHERIT / C-RESIDUAL-NOVELTY / C-FRESHNESS sub-evaluations + ST-WebAgentBench safety  
**Director mandate:** PIVOT with cognitive_reset=true, SUPERSEDE, action PIVOT, claim_id C-PRODUCT-ECON, comparative reasoning vs C-LLM-INHERIT same-model hold-out without Pareto, vs per_hit proxy, vs WebMCP bypass — M_total Pareto supersession dominates  
**Parent:** EXP-PRODUCT-35961222077 handoff MEASUREMENT_INVALID sha 8e914b008279fb4dcb8cb4bac49d0d99750613b53cc7a11be8206d06cde5184b — inherited state preserved per §2, Director PIVOT governs this design (parent next_question advisory)  
**Status:** DESIGN — frozen inputs immutable after freeze.json; no outcome inspection permitted

---

## 1. Background & inherited scientific state (from parent handoff + Codex + Scout + Director)

**Director binding (research/EXPERIMENT_PACKET.md §2, POLICY.md):**
- Target claim C-PRODUCT-ECON: "SPIDER saves total cost per successful task after retrieval, verification and maintenance" — currently HYPOTHESIS, next gate "end-to-end amortized economics on real agents".
- Strategic question verbatim: *On health-gated single-node HS256 sticky $request_uri If-None-Match/W/body_sha->304 substrate (n_non304>=800 stratified 400/endpoint, TTL 60s max-age conditional probe ETag W/body_sha ~50% stale at n=0.25 vs ~1.0 at n=0) plus Docker BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10 + real gpt-4o-mini 15-step Playwright same model/tools/budget (honest per-trajectory-reset sum counters resolve+bind+verify+freshness+browser_steps no jitter/no n*3200/no f*6.0, |rho_shuffled|<0.20 rho_proxy_real>=0.50 per-stratum |rho_length|<0.20, 5000 family-stratified trajectory-grouped bootstrap + 5000 block-permutation, verification AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18, correlated probe saving>=30% accuracy>=0.90 vs seeded-42 random 0.53, DSM 714/2147 80-94% $0.002-0.092 amortized), does honest M_total_f10/f100 Pareto (tokens+browser+latency+retrieval+verification+freshness at f=10/100) demonstrate dominance vs RAG-EMBED TAU0.30/QCR k5, Stagehand selector+DOM-hash cache 2x speedup ~30% cost, and DSM/SGDR/AWM (Pareto saving >=25% vs COLD and <=0.85x vs RAG at both f=10/100, margin >=0.12 vs each baseline) formally superseding falsified per_hit=(M_total-retrieval-distill/auditor)/L 1.005>0.85 rho 0.363<0.60 as PRODUCT_CORE viability gate with ST-WebAgentBench safety?*
- Rationale: per_hit falsified (1.005>0.85 rho_novelty 0.363<0.60) and 14 recent C-PRODUCT-ECON attempts MEASUREMENT_INVALID without real browser cost; synthetic file-proxy per_hit is artifact-contaminated (jitter, n*3200, f*6.0). The next decisive gate is honest amortized Pareto M_total at f=10/100 with real BrowserGym tokens/browser/latency and freshness probe vs strong baselines (RAG TAU0.30, Stagehand cache, DSM O(1) $0.002-0.092, SGDR/AWM) — changes PRODUCT_CORE promotion decision and formally supersedes per_hit.
- Agent priors used (distinguished from SPIDER evidence): long-horizon planning error compounding / local optima (Frontier 17-deep, Intel 22-deep streaks), Tool/API bypass vs hierarchical retrieval, Laplace smoothing / hash-truncated DOM measurement traps (|perm-analytic|<0.03 etc without Gamma-ratio), end-to-end economics amortized compilation O(1) $0.002-0.092 vs retrieval only if verification+freshness excluded (rho>=0.60 stronger than raw margin), cross-task transfer requires website/family holdout with trajectory-grouped resampling.
- Comparative reasoning adopted verbatim per mandate §4.

**Established (bounded, from parent handoff carry_forward.established):**
- Single-node HS256 sticky substrate CAN be provisioned health-gated at /tmp/spider-runtime/shared.db WAL journal_mode=wal distinct_worker_pids=[69030] single_worker gunicorn 23.0.0 single-worker HS256 PyJWT 2.14.0 nginx 1.24.0 $request_uri sticky hash upstream 127.0.0.1:18929 with n_non304_total 840 stratified 420/420 (>=800 and >=400/endpoint) n_requests 846 if_none_match_exercised_fraction 1.0 errors 0 — bounded operational ceiling not claim validation (artifacts/substrate_probe.json ef115499).
- Correlated TTL 60s max-age ETag W/body_sha conditional probe discriminates fresh vs stale: probe_correlated_n0 304-hit 1.0 (n=150) probe_correlated_n025 accuracy 1.0 stale 0.5 false_accept 0.0 token_saving 0.40 vs seeded-42 random 0.487/0.267 delta 0.513 — substrate-level diagnostic not task success/Pareto.
- PC3 MockEnv calibration pipeline non-vacuous MV10: AUROC_verif_true 0.919 >=0.75 AUROC_shuffled_null 0.482, precision_verif 0.968, wrong_accept 0.169, confidence_std 0.453, UNKNOWN_precision 0.983, ECE 0.103 — demonstrates verification can discriminate on MockEnv not real LLM trajectories.
- Kernel dot-regex fix r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}' at src/spider/kernel.py sha d926279d 5/5 EXECUTABLE confidence 0.85 wrong-family UNKNOWN via artifacts/mv2_kernel_spot_check.json — now durable in working tree and HEAD 58fc8fe4 base per audit recomputed (requires commit durability).
- Cross-family orthogonality sub-gate passes: cross_family_jaccard_max 0.0 on 630 pairs via A-pool first-slot bigram Jaccard <0.30 — orthogonality does not imply holdout disjointness.
- Stagehand exact-repeat hit_rate 1.0 5/5 per_hit 50 tokens on hit via disclosed file-proxy body/DOM hash — file-proxy disclosed insufficient for SURVIVES per frozen no-surrogation rule.
- Pins now compliant: gunicorn 23.0.0 PASS pyjwt 2.14.0 PASS flask 3.1.3 numpy 2.5.3 scipy 1.18.1 sklearn 1.9.1 pandas 3.0.6 python 3.12.14 per provenance/env_audit.
- No bijective n*3200/f*6.0/jitter proxy used; counters are per-trajectory honest sums and frozen hashes preserved.
- Prior bounded file-proxy economics ceiling remains standing but not extended: WebArena-Verified v2 192/36 per_hit StagehandTTL 1.045 CI[1.034,1.056]>0.85 at n0 rho 0.472<0.60 remains only claim-level economics evidence — this experiment adds null not contradiction.

**Rejected (bounded):**
- Canonical 192/36 fallback census sha 391e8f6c REJECTED as contamination-free holdout: value_set_A intersect B non-empty on 18/36 even-index families at both pool and usage level via rotation B[k]=A[(k+5)%10] — violates MV2.
- NC1 shuffled null construction as implemented (rng random n_eff + optional b_positions clear leaving Spearman coupling) REJECTED as valid null control: rho_shuffled 0.778 CI[0.709,0.830] p0.0002 exceeds |rho|>=0.35 p<0.01 degenerate threshold — degeneracy is construction artifact not hypothesis evidence.
- No rejection of C-LLM-INHERIT globally nor of C-PRODUCT-ECON on honest substrate: MEASUREMENT_INVALID is bounded to infrastructure triggers not to economics mechanism — claim remains HYPOTHESIS per audit ceiling.
- Per_hit falsified as PRODUCT_CORE gate on file-proxy: per_hit 1.005>0.85 rho 0.363<0.60 is bounded rejection of per_hit metric design on file-proxy, not rejection of M_total Pareto on health-gated real substrate; this experiment must not reopen per_hit without real-token replication.

**Unknown (this experiment must resolve):**
- All primary C-PRODUCT-ECON / C-LLM-INHERIT Pareto/margin gates remain unknown (null not zero) because clause1 fired before clause3: M_total_f10/f100 Pareto tokens vs browser+latency vs accuracy+ST-WebAgentBench safety at f=10/100 vs EACH baseline (COLD/RAG-k5/Stagehand/DSM 714/2147/SGDR-AWM), success_margin >=0.12 at both f, calibration (false_accept, UNKNOWN, ECE, AUROC), rho_novelty per-stratum, rho_length, rho_proxy_real pooled+per-stratum, probe saving/accuracy/TN, DSM amortized $ — all unmeasured due to Docker/BrowserGym/OPENAI contamination gates.
- Whether GHCR authorization for ghcr.io/servicenow/browsergym:0.14.3 and OPENAI_API_KEY provisioning plus playwright 1.63.0 install can restore Docker BrowserGym 2000-node 1280x720 CDP AX>10 and gpt-4o-mini 15-step real-token measurement enabling rho_proxy_real>=0.50 pooled+per-stratum.
- Whether contamination-free holdout (Hard258 pip census or rebuilt 192/36 where value_set_A intersect B empty on all 36 families TRAIN-only Jaccard<0.30 630 pairs 0.0 preserved) can be staged with L=8-14 family-specific invariants and frozen TAU0.30 QCR bank.
- Why NC1 shuffled retains rho 0.778 — hypothesised n_novel rounding coupling; requires redesign before future null battery without weakening |rho_shuffled|<0.20 thresholds.
- Whether dedicated PC4 frozen-formula parity artifact within 1e-6 plus rho_proxy_real logging with 5000 bootstrap can be completed once real tokens exist.
- Full M_total Pareto supersession of per_hit as PRODUCT_CORE gate with ST-WebAgentBench safety remains untested end-to-end.

**Do_not_assume (must not be inferred from invalid prior):**
- Do not treat MEASUREMENT_INVALID as scientific FALSIFICATION or SUPPORTS of C-PRODUCT-ECON — outcome INCONCLUSIVE per EXPERIMENT_PACKET s9, producer correctly kept claim metrics null not zero and baselines UNKNOWN.
- Do not assume single-node substrate half PASS (n_non304 840) + correlated probe delta 0.513 implies Pareto validated — probe and substrate diagnostics are substrate-level not M_total Pareto; all claim economics still null.
- Do not assume working-tree kernel patch d926279d durable across clean checkouts without commit.
- Do not assume installable stack or compliant pins imply BrowserGym/Docker/OPENAI health — env_audit shows docker pull denied and openai absent; file-proxy fallback banned for SURVIVES.
- Do not assume cross-family Jaccard max 0.0 implies holdout disjointness — Jaccard over A-pool first-slot values not value_set intersection.
- Do not assume prior-run artifacts qcr/dsm/391e8f6c are staged TRAIN-only for this experiment just because they exist repo-wide — fixture_checks showed only fallback staged byte-identical and contaminated; Hard258 not staged.
- Do not assume PC3 MockEnv AUROC transfers to real LLM trajectories.
- Do not assume NC1 degenerate rho indicates real novelty-cost coupling — it is null-control construction degeneracy and must not be read as falsified rho.
- Do not assume per_hit superseded by M_total Pareto without honest single-node health-gated n_strat>=400 AUROC>=0.75 rho_proxy>=0.50 and correlated vs random delta>0.10 evidence.
- Do not promote to PRODUCT_CORE without Director promote_to_product true and audit PASS.

---

## 2. Research question (Director binding, refined to falsifiable gate)

**Director Question (binding):** On health-gated single-node HS256 sticky $request_uri If-None-Match/W/body_sha->304 substrate (n_non304>=800 stratified 400/endpoint, TTL 60s max-age conditional probe ETag W/body_sha ~50% stale at n=0.25 vs ~1.0 at n=0) plus Docker BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10 + real gpt-4o-mini 15-step Playwright same model/tools/budget (honest per-trajectory-reset sum counters resolve+bind+verify+freshness+browser_steps no jitter/no n*3200/no f*6.0, |rho_shuffled|<0.20 rho_proxy_real>=0.50 per-stratum |rho_length|<0.20, 5000 family-stratified trajectory-grouped bootstrap + 5000 block-permutation, verification AUROC>=0.75 precision>=0.80 false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18, correlated probe saving>=30% accuracy>=0.90 vs seeded-42 random 0.53, DSM 714/2147 80-94% $0.002-0.092 amortized), does honest M_total_f10/f100 Pareto (tokens+browser+latency+retrieval+verification+freshness at f=10/100) demonstrate dominance vs RAG-EMBED TAU0.30/QCR k5, Stagehand selector+DOM-hash cache 2x speedup ~30% cost, and DSM/SGDR/AWM (Pareto saving >=25% vs COLD and <=0.85x vs RAG at both f=10/100, margin >=0.12 vs each baseline) formally superseding falsified per_hit=(M_total-retrieval-distill/auditor)/L 1.005>0.85 rho 0.363<0.60 as PRODUCT_CORE viability gate with ST-WebAgentBench safety?

**Refined falsifiable gate for this experiment:** Same health-gated substrate + BrowserGym + gpt-4o-mini honest counters and family hold-out (train A test never-observed B value_set_A intersect B empty, Jaccard<0.30, L=8-14) with SPIDER SUT (freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic localized repair + correct-family reconstruction verified_state MEA auditor, TTL 60s ETag W/body_sha) vs B-COLD vs B-RAG-EMBED k5 vs B-STAGEHAND-CACHE vs B-DSM-O1 (714/2147 80-94% $0.002-0.092) vs B-SGDR/AWM — does honest M_total_f10/f100 Pareto decomposed tokens vs browser+latency vs accuracy vs ST-WebAgentBench CuP safety show SPIDER saving >=25% vs COLD and ratio <=0.85 vs RAG at BOTH f=10 and f=100 with browser+latency >=20% and margin >=0.12 vs EACH baseline at both f, calibration AUROC>=0.75 etc, rho_novelty>=0.60 per-stratum, and safety non-inferior, thereby superseding per_hit?

This is the smallest high-information gate that can change C-PRODUCT-ECON from HYPOTHESIS to EXPERIMENTAL on valid substrate (or PARK it) and retire the contested per_hit gate — never before tested end-to-end with honest real-token Pareto and safety.

---

## 3. Hypothesis

H1 (primary, C-PRODUCT-ECON): With health-gated single-node HS256 sticky substrate and correlated ETag freshness (fresh ~1.0 at n0 vs ~50% stale at n0.25, n_non304>=800 stratified 400/endpoint, nginx 1.24.0 $request_uri sticky hash + single gunicorn Flask HS256 PyJWT 2.14.0 WAL shared.db) and BrowserGym 0.14.3 2000-node 1280x720 CDP AX + gpt-4o-mini 15-step same model/tools/budget, SPIDER freshness-gated inheritance (Jaccard 0.95/0.85 alias 0.85 + deterministic localized repair single-field re-bind + correct-family reconstruction via dot-regex + TTL 60s conditional probe 10tok+30ms + verified_state MEA auditor softmax temp0.15+jitter UNKNOWN<0.80) and family hold-out zero-overlap orthogonal will:

- (a) achieve Pareto dominance: M_total saving >=25% vs B-COLD and ratio <=0.85 vs B-RAG at both f=10 and f=100 (bootstrap CI lower excludes 0), plus browser+latency >=20% vs COLD at both f with accuracy>=0.85 Pareto decomposed, DSM O(1) $0.002-0.092 logged;
- (b) achieve success margin >=0.12 vs EACH of B-COLD, B-RAG-EMBED k5, B-STAGEHAND-CACHE, B-DSM-O1, B-SGDR/AWM at f=10 and f=100 (Wilson + bootstrap CI), success at n0>=0.85, safety CuP non-inferior (>= best baseline -0.02);
- (c) satisfy calibration: false_accept<=0.10, UNKNOWN>=0.85, ECE<=0.15 upper<=0.18 per-class 5-bin, AUROC>=0.75 precision>=0.80 conf_std>0.05;
- (d) track residual novelty rho_novelty>=0.60 pooled+per-stratum with |rho_length|<0.20 and |rho_shuffled|<0.20 p>=0.20 and rho_proxy_real>=0.50 per-stratum where BrowserGym real tokens measured;
- (e) correlate probe saving>=30% accuracy>=0.90 TN>=0.85 stratified and delta >10% vs seeded-42 random 0.53.

Supersession: if per_hit remains >0.85 at n0/n0.25 but M_total Pareto dominates decisively, recommend formal supersession of per_hit with M_total Pareto as gate.

Null for controls: Shuffled bindings/probe/registry, length-constant cost, and random-key entry are uncorrelated with novelty/length and have AUROC~0.5, M_total not dominant, per spec NC.

---

## 4. State / Action / Target representation

- **State representation:** Mechanism preconditions = family+intent+site (+ state_key=family+DOM_hash for SGDR if exercised from BrowserGym CDP AX 2000 nodes, viewport 1280x720, SHA256 ordered AX tree truncated 2000 nodes). Freshness = ETag W/body_sha + TTL max-age 60s + probeHit (200 vs 304) stratified 400/endpoint. Family orthogonality Jaccard<0.30 ensures state distinctness; Hard258 pip heterogeneous or disclosed 192/36 fallback census defines task distribution.
- **Action representation:** Mechanism action_template with parameter slots `${param}` using dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` (supports nested e.g., `${user.profile.id}`) via _bind full-match/substring + kernel.verify postconditions + MEA auditor verified_state.
- **Target (economics primary):** Per-trajectory M_total_f10/f100 = sum_tokens + sum_browser_steps + latency_ms_equiv + retrieval (200) + verification (50 tok+120ms per verify) + freshness probe (10tok+30ms per step) + DSM tool (15) / SGDR (180) where exercised + safety scoring, with per-trajectory-reset honest sum counters (no n*3200). Derived M_per_hit = (M_total - retrieval/tool/SGDR - distill/compile - auditor)/L (probe stays in) — secondary superseded gate. Novelty fraction n from B (test) vs Curated-A (train) per family stratified 0/0.25/0.5/0.75/1.0; L 8-14 family-specific constant within family orthogonal to n.
- **Calibration target:** Verification confidence (softmax temp0.15+jitter [-0.05,0.05]) vs correctness (EXEC rows). AUROC, precision, false_accept, UNKNOWN_precision, per-class ECE 5-bin.
- **Safety target:** ST-WebAgentBench CuP safety score per trajectory (policy violation / unsafe execute rate) for SPIDER and each baseline where BrowserGym exercised; non-inferior bound SPIDER >= best_baseline -0.02 at both f.
- **Cost model:** Honest sum counters; probe 10 vs retrieval 200 vs SGDR 180 vs DSM 15 (if exercised) honored; no bijective proxy; DSM amortized $0.002-0.092 at f=10/100 logged.

---

## 5. Sampling policy & holdout

- **Census:** Pip-installable WebArena-Verified Hard258 as primary heterogeneous pool via `pip install browsergym webarena` or repo pip. If Docker image ghcr.io/servicenow/browsergym:0.14.3 unavailable or Hard258 pip manifest missing, fallback to WebArena-Verified v2 192 tasks across 36 orthogonal alias families (A/B disjoint alphabets, Jaccard<0.30 630 pairs via qcr_bank_manifest.json 8c69804b, tasks.json 391e8f6c) as disclosed heterogeneous subset — same as parent but rebuilt contamination-free (Hard258 preferred; fallback must be rebuilt with value_set_A intersect B empty on all families per MV2).
- **Splits:** Per-family disjoint Curated-A (train, registry induction + qcr bank + sgdr + dsm) / B (test, orthogonal slots) zero overlap value_set_A intersect B empty verified. Frozen qcr_bank_manifest TAU0.30 same ranker TFIDF for RAG/SGDR. Registry 714/2147 equiv from Curated-A TRAIN only. Test tasks never in curation. Rebuild required vs contaminated 391e8f6c rotation.
- **Conditions:** 6 conditions x 5 novelty levels =30 cells family-stratified (B-COLD, B-RAG-EMBED k5, B-STAGEHAND-CACHE, B-DSM-O1, B-SGDR-AWM, P-SPIDER-ECON-PARETO; B-INSTRUCTIONS as sensitivity if budget permits). Plus 4 null controls trajectory-grouped permutations + ablations + safety scoring. Same model/tools/budget per condition.
- **Browser substrate:** Docker BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree, Playwright 1.63.0, gpt-4o-mini 15-step same model/tools/budget across conditions. If Docker pull denied or OPENAI_API_KEY absent, primary gate is MEASUREMENT_INVALID (no fallback to file-proxy for SURVIVES per Director).
- **Single-node substrate (where needed):** /tmp/spider-runtime/shared.db SQLite WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri sticky hash + PyJWT 2.14.0 HS256, If-None-Match/ETag W/body_sha conditional probe health-gated n_non304>=800 stratified 400/endpoint, TN>=0.85.

---

## 6. Unit of analysis & holdout integrity

- Unit = trajectory (family-stratified, trajectory-grouped). Bootstrap and permutation respect trajectory grouping (block-permutation by trajectory/family, not transition). Stratified by family (36 families if fallback, up to Hard258 heterogeneous) and novelty fraction, with stratified endpoint counts for n_non304 where applicable.
- Holdout = per-family train/test disjoint; frozen bank and registry TRAIN-only. Verify value_set_A intersect B empty via hash check; contamination => PC MEASUREMENT_INVALID.
- Preprocessing fit on TRAIN only (TFIDF, QCR bank). No post-state leakage into pre-state features. BrowserGym AX tree snapshot is pre-state only. Same gpt-4o-mini model/tools/budget across conditions ensures policy confounding controlled; safety CuP scoring same policy.
- Per-hit isolation: M_per_hit reported per trajectory excluding fixed retrieval/distill but including probe; M_total reported for economics. Probe stays in numerator to avoid per_hit artifact; Pareto vs per_hit artifact explicitly disclosed.
- Trajectory-grouped unit = trajectory not transition; 5000 family-stratified bootstrap + 5000 block-permutation per spec.

---

## 7. Baselines & controls (stable identities for AUDIT/DIRECTOR)

**Baselines (honest same splits, same probe/verify fallback, honest f=10/f=100 amortized, stratified, same LLM budget):**
- B-COLD: no memory, 500 tok +2 browser_steps +50+120ms verify per step. Denominator for saving and safety.
- B-RAG-EMBED-TAU030-QCR-K5: TFIDF/Jaccard TAU0.30 top-k=5 (k1 sensitivity) QCR frozen bank, 200 tok+150ms retrieval, verbatim bind only — primary <=0.85x comparator.
- B-STAGEHAND-CACHE: DOM-hash selector cache without TTL, hit iff DOM identical (1.0 at n0, 0 at n>=0.25), 50 tok+120ms +1 step hit — 2x speedup ~30% claim.
- B-DSM-O1-COMPILE: DSM 714/2147 O(1) compiled tools $0.002-0.092 amortized at f=10/100, 80-94% compile success required.
- B-SGDR-AWM: SGDR state_key retrieval 180 tok + AWM workflow memory.
- P-SPIDER-ECON-PARETO (SUT): selector-cache + correlated 60s ETag probe 10tok+30ms health-gated n_non304>=800 stratified + correct-family reconstruction + deterministic localized repair + verified_state MEA auditor — reports M_total Pareto at f=10/100 vs each baseline plus supersede per_hit and safety.

**Positive control PC-SINGLE-NODE-ECON-PARETO-CORRELATED (any fail => MEASUREMENT_INVALID):**
- PC1 exact-repeat 1.0 hit at n0 5/5 spot-check via health-gated sticky,
- PC2 orthogonal Jaccard<0.30 max 0.0 + kernel dot-regex 5/5 EXECUTABLE confidence>=0.80 + value_set disjoint + correlated probe fresh~1.0 stale~50% accuracy>=0.90 saving>=30% TN>=0.85 stratified + registry 714/2147 80-94%,
- PC3 non-vacuous verify false_accept [0.10,0.60] confidence_std>0.05 AUROC null~0.5 true>=0.75,
- PC4 frozen formula within 1e-6 vs summed counters + n_non304 stratified + rho_proxy_real pooled+per-stratum 5000 bootstrap logged + DSM cost logged,
- PC5 health-gate n_non304>=800 stratified 400/endpoint sticky single-worker HS256 + If-None-Match exercised + Docker BrowserGym 0.14.3 + gpt-4o-mini 15-step health AX>10 + safety instrumentation.

**Null control NC-SHUFFLE-ECON-PARETO (via actual pipeline, no simulated correctness):**
- NC1 shuffled slots + TTL map random 0.53 vs correlated + correct-family keys permuted trajectory-grouped: expect |rho|<0.25 ns, |rho_shuffled|<0.20 p>=0.20 per-stratum, |rho_length|<0.20, |rho_shuffled_proxy|<0.20, AUROC 0.45-0.60, success<=COLD, UNKNOWN>=0.80, M_total ratio ~1.0.
- NC2 random family/state keys: false_accept>=0.10 AUROC~0.5, M_total not dominant.
- NC3 length-constant cost L*500: |rho|~0 R2<0.15.
- NC4 ablations: correlated vs random delta>10% saving, DSM compile off vs on delta, single-node TN 0.85 vs per-node 0.667, rho_proxy_real shuffled <0.20. B=5000 trajectory-grouped.

---

## 8. Metrics (stable names, with units)

- `M_total_f10` , `M_total_f100` (tokens+browser_steps+latency+retrieval/verification/freshness per trajectory honest sum) + Pareto decompose `M_tokens`, `M_browser_latency`, `accuracy`, `safety_CuP` at f=10 and f=100 — primary economics
- `M_total_saving_vs_COLD_f10`, `M_total_saving_vs_COLD_f100` (>=25%) and `M_total_ratio_vs_RAG_f10`, `M_total_ratio_vs_RAG_f100` (<=0.85) with family-stratified bootstrap 5000 CI
- `DSM_amortized_cost_f10`, `DSM_amortized_cost_f100` ($0.002-0.092, 80-94% compile) vs SPIDER amortized
- `success_rate` per condition/n (binary, Wilson 95% CI) and `success_margin_vs_baseline_f10/f100` (SPIDER minus each baseline, bootstrap CI) — must be >=0.12
- `false_accept` (EXECUTABLE wrong binding failing verify via MockEnv 15% wrong-bound) <=0.10
- `UNKNOWN_precision` = TP_UNKNOWN/(TP+FP_UNKNOWN) >=0.85
- `ECE_5bin_per_class` + bootstrap upper per-class (EXEC rows only, 3 empty bins disclosed, 5-bin) <=0.15 upper<=0.18
- `AUROC_verif` , `precision_verif` (confidence vs correctness) >=0.75 / >=0.80
- `M_per_hit` = (M_total - retrieval/tool/SGDR - distill/compile - auditor)/L (probe stays IN) — secondary superseded gate (parent falsified 1.005>0.85)
- `rho_novelty` (Spearman M_per_hit vs n pooled + per-stratum stratified, 95% CI 5000 bootstrap) >=0.60 with `R2_novelty`
- `rho_length` (|rho| M_per_hit vs L, pooled+per-stratum) must be <0.20
- `rho_proxy_real` (Spearman proxy cost vs real gpt-4o-mini tokens+browser+latency pooled+per-stratum) >=0.50 where Docker measured
- `rho_shuffled` (|rho| shuffled null pooled+per-stratum, block-permutation 5000 p) <0.20 p>=0.20, plus `rho_shuffled_proxy` per-stratum <0.20
- `probeHit_correlated` vs `probeHit_random`, `n_non304` stratified, `TN_freshness` (>=0.85), `probe_saving` (>=30%), `probe_accuracy` (>=0.90)
- `safety_CuP` per condition/f (ST-WebAgentBench completion under policy) + `safety_delta_vs_best_baseline`
- All metrics report family-stratified trajectory-grouped bootstrap 5000 CIs and Wilson 95% for rates. Within-family std>0 required; degenerate CI[1,1] flags MEASUREMENT_INVALID. Stratified n_non304 counts required where substrate exercised. Per-hit supersede logged.

---

## 9. Decision rule (frozen, precedence ordered)

Computed on health-gated single-node n_non304>=800 stratified 400/endpoint where substrate needed + Docker BrowserGym 0.14.3 2000-node heterogeneous real tokens branch-derived f=10/100 honest per-trajectory-reset counters TRAIN-warmed. Same model/tools/budget across conditions.

1. **MEASUREMENT_INVALID** if any PC1-PC5 fails OR n_non304<800 stratified where substrate required OR $request_uri sticky violated OR If-None-Match not exercised where required OR single-node HS256 not at /tmp/spider-runtime/shared.db WAL single-worker OR Docker BrowserGym 0.14.3 + gpt-4o-mini 15-step unavailable (rho_proxy_real unmeasurable) OR fixtures missing (Hard258 pip or disclosed 192/36 fallback with disclosure, qcr TAU0.30 630 pairs 0.0, dsm 714/2147, sgdr 36, cost_config, kernel dot-regex not patched) OR TRAIN contamination (value_set_A intersect B non-empty) OR bijective proxy detected OR degenerate null (|rho_shuffled|>=0.35 p<0.01 or within-std==0 or CI[1,1] or confidence_std<=0.05 or DSM cost degenerate) — irrespective of Pareto, no file-proxy fallback for SURVIVES.

2. Else **FALSIFIED** if controls PASS non-degenerate but any primary gate fails: M_total saving <25% vs COLD OR ratio >0.85 vs RAG at f=10 or f=100 OR browser+latency <20% OR accuracy<0.85 OR safety regresses >0.02 below best baseline OR success margin <0.12 vs any baseline at f=10 or f=100 (CI includes <=0) OR success at n0<0.85 OR false_accept>0.10 OR UNKNOWN<0.85 OR ECE>0.15 bootstrap upper>0.18 OR AUROC<0.75 OR precision<0.80 OR rho_novelty<0.60 (CI lower<0.50 pooled or <0.45 per-stratum) OR |rho_length|>=0.20 OR rho_proxy_real<0.50 per-stratum OR |rho_shuffled|>=0.20 p<0.20 per-stratum OR probe saving<30% accuracy<0.90 TN<0.85. Controls must be PASS non-degenerate.

3. Else **SURVIVES** (C-PRODUCT-ECON -> EXPERIMENTAL, PRODUCT_CORE viability gate) iff ALL hold with PC PASS non-degenerate stratified with correct frozen controls: (C1 Pareto economics primary) tokens saving >=25% vs COLD and ratio <=0.85 vs RAG at BOTH f=10 and f=100 (bootstrap CI excludes 0, family-stratified) AND browser+latency saving >=20% at both f with accuracy>=0.85 Pareto decomposed + DSM $0.002-0.092 logged; (C2 correctness+margin+safety) margin >=0.12 vs EACH baseline (B-COLD/B-RAG-k5/B-STAGEHAND/B-DSM-O1/B-SGDR-AWM) at f=10 and f=100 (Wilson+bootstrap CI >0, success>=0.85 at n0) AND safety CuP non-inferior (>= best_baseline -0.02 at both f); (C3 calibration) false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18 AND AUROC>=0.75 precision>=0.80 conf_std>0.05; (C4 residual-novelty) rho>=0.60 pooled CI>=0.50 per-stratum>=0.45 with |rho_length|<0.20 pooled+per-stratum and rho_proxy_real>=0.50 per-stratum with |rho_shuffled|<0.20 p>=0.20; (C5 probe) saving>=30% accuracy>=0.90 TN>=0.85 stratified and correlated vs random 0.53 delta >10%. Family-stratified trajectory-grouped B=5000 both.

**SUPERSEDE clause (Director rationale binding):** If per_hit CI clears >0.85 at BOTH n0 and n0.25 (parent falsified 1.005>0.85 rho 0.363<0.60, 5000 bootstrap) but all C1-C5 Pareto/margin/calibration/rho/safety dominate decisively with rho>=0.60 per-stratum n_strat>=400 AUROC>=0.75 safety non-inferior correlated delta>10% vs random 0.53, then per_hit artifact demonstrated and M_total Pareto formally supersedes falsified per_hit 1.005>0.85 as PRODUCT_CORE viability gate — verdict recommends supersession, not per_hit promotion. Previous per_hit falsification bounded to file-proxy with rho 0.363<0.60 is NOT reopened without health-gated real-token replication. DSM O(1) comparison informs architecture pricing.

---

## 10. Product consequences

**Positive (SURVIVES):** C-PRODUCT-ECON HYPOTHESIS → EXPERIMENTAL bounded to WebArena-Verified Hard258 heterogeneous (or disclosed rebuilt 192/36 fallback) single-node health-gated 1280x720 stratified with same gpt-4o-mini 15-step Playwright (freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic localized repair + correct-family reconstruction + TTL 60s ETag W/body_sha + verified_state MEA auditor + honest M_total Pareto + ST-WebAgentBench safety). C-FRESHNESS → EXPERIMENTAL for correlated probe, C-RESIDUAL-NOVELTY validated at rho>=0.60, C-LLM-INHERIT sub-gate EXPERIMENTAL via margin >=0.12. First valid single-node+real-token evidence that honest amortized Pareto dominates vs RAG k5 (<=0.85x), Stagehand cache, and DSM/SGDR/AWM 80-94% $0.002-0.092 at both f=10/100 with safety non-inferior, formally retiring falsified per_hit 1.005>0.85 rho 0.363<0.60. Justifies shipping SPIDER inheritance as interim vs Stagehand cache-only, with Pareto frontier and rho as pricing prior for compilation vs inheritance choice. No PRODUCT_CORE without explicit DIRECTOR promote_to_product true and audit PASS; Codex records supersession proposal.

**Negative (FALSIFIED with controls PASS n_strat>=400 rho_proxy>=0.50 AUROC>=0.75 safety measured):** Honest M_total Pareto does NOT yield saving >=25% vs COLD or <=0.85 vs RAG at f=10/100 or margin >=0.12 or accuracy/safety non-inferior even on honest substrate; PARK C-PRODUCT-ECON/C-LLM-INHERIT economics even on honest correlated substrate per Director PIVOT, pivoting Product to ST-WebAgentBench CuP optimization, Intel diverse-site grounding, richer SPA sampling, or DSM/SGDR O(1) compilation architecture before PRODUCT_CORE. Joint falsification triggers architecture choice: inheritance vs O(1) compilation. Bounded REJECTED for this mechanism on health-gated BrowserGym 0.14.3 gpt-4o-mini 15-step setting, not global falsification. If SUPERSEDE condition met (per_hit>0.85 but Pareto dominates) -> per_hit artifact formally demonstrated, recommend superseding contested per_hit<=0.85 with M_total_f10 Pareto tokens vs browser+latency vs accuracy+ safety at f=10/100 as primary gate per Director rationale, runtime single-node + BrowserGym + fresh probe + safety validated, metric-design change not mechanism promotion.

**Measurement invalid:** No claim update; handoff carries smallest next action (runtime single-node hardening, gunicorn 23.0.0/PyJWT 2.14.0 pin, nginx $request_uri sticky, BrowserGym GHCR pull/OPENAI_API_KEY, n_non304>=800 stratified, If-None-Match loop, kernel patch commit, NC1 redesign, Hard258 rebuild) without inventing economics. Preserves established/rejected/unknown/do_not_assume distinctions.

---

## 11. Validity threats & controls

- **Representation loss:** DOM truncation at 2000 nodes, file-proxy hash fallback disclosed but banned for SURVIVES; browser events/network/auth/session preserved via Flask HS256 + BrowserGym AX 2000 nodes.
- **Policy confounding:** Same gpt-4o-mini + same 15-step budget/tools/viewport/CDP AX>10 across conditions + ST-WebAgentBench same safety policy; trajectory-grouped permutation isolates policy regularity.
- **Site/task leakage:** Frozen qcr_bank TAU0.30 same ranker, orthogonal families Jaccard<0.30 value_set_A intersect B empty, site gating mandatory; audit recomputes parity within 1e-6 stratified; DSM registry TRAIN-only.
- **Bijective proxy:** Honest per-trajectory sum counters enforced; any n*3200/f*6.0/jitter => MEASUREMENT_INVALID; rho_proxy_real>=0.50 per-stratum required.
- **Verification calibration threat:** Softmax temp0.15+jitter prevents linear 0.95-n*0.12 tautology; confidence_std>0.05 and AUROC vs shuffled null required; empty ECE bins disclosed stratified per-class.
- **Stale freshness:** Seeded-42 0.53 decorrelated contrast vs correlated ETag W/body_sha fresh~1.0 isolates novelty correlation; TN>=0.85 health-gated stratified vs per-node 0.667 artifact.
- **Cost model threat:** Honest sum counters; probe 10 vs retrieval 200 vs SGDR 180 vs DSM 15 honored; per_hit excludes retrieval/tool but M_total includes them — Pareto vs per_hit artifact disclosed with supersede clause. Family-stratified CIs prevent degenerate [1.0,1.0]. DSM $0.002-0.092 amortized decomposed at both f.
- **LLM non-determinism & safety:** Same model seed temp0; gpt-4o-mini 15-step fixed; trajectory-grouped bootstrap respects correlation; safety CuP scored identically.
- **Stratification threat:** n_non304 must be ≥400 per endpoint; pooled 800 without stratification insufficient.
- **Contamination:** TRAIN-only induction; test B never in curation; hash verification; rebuild required vs 391e8f6c rotation.
- **Economics vs calibration coupling:** Pareto saving and accuracy vs calibration AUROC jointly required; browser+latency decomposed prevents token-only dominance.

---

## 12. Cost & information gain

**Estimated cost:** Moderate single-node health-gated stratified + LLM replication + ST-WebAgentBench safety: 258 (or 192 fallback 36 families) x6 conditions x5 levels =1290-1548 trajectories + ~600-750 nulls + ~200 probe ablations + ~200-300 DSM/safety sensitivity = ~2290-2800 deterministic resolve/bind/verify/probe trials on single-node HS256 sticky WAL + TFIDF offline. Wall <90min CPU proxy (<160min if Docker BrowserGym 0.14.3 2000-node loopback health-gated n_non304>=800 heterogeneous). Storage per-trajectory CSV ~3000-4500 rows branch_traces. If Docker+gpt-4o-mini: 258x6x15 steps Playwright ~3600-5500 browser_calls ~2880-4500 gpt-4o-mini calls <$35 plus safety snapshots/logs. Honest sum counters, no bijective n*3200.

**Expected information gain:** Decisive gating per Director PIVOT cognitive_reset SUPERSEDE: C-PRODUCT-ECON is the blocking PRODUCT_CORE viability gate (falsified per_hit 1.005>0.85 rho 0.363<0.60; 14 recent MEASUREMENT_INVALID without real browser cost, synthetic per_hit artifact-contaminated). This is the smallest high-information test that can convert the gate from contested per_hit to honest M_total Pareto at f=10/100 vs three complementary strong baselines (RAG k5 TAU0.30, Stagehand 2x cache, DSM O(1) $0.002-0.092 / SGDR) with same model/tools/budget and safety non-inferior, directly deciding commercial viability and supersession. Positive reopens C-PRODUCT-ECON to EXPERIMENTAL and retires per_hit, justifying interim shipping with Pareto pricing; per_hit artifact supersession formally replaces contested metric with M_total Pareto even if per_hit fails; double failure PARKs product economics even on honest substrate and pivots to CuP/richer SPA/DSM compilation. Vs another per_hit 1.005 optimization or 18th alias 0.525 permutation marginal ~0. High leverage.

---

## 13. Execution checklist (frozen, must log or MEASUREMENT_INVALID)

- [ ] Pin gunicorn 23.0.0 and PyJWT 2.14.0 exactly before SURVIVES (provenance + env_audit).
- [ ] Provision /tmp/spider-runtime/shared.db WAL single-worker sticky, nginx 1.24.0 $request_uri hash, If-None-Match/ETag W/body_sha 200 vs 304, n_non304>=800 stratified 400/endpoint health-gated TN>=0.85 where substrate needed.
- [ ] Pip-install WebArena-Verified Hard258 + BrowserGym 0.14.3 2000-node 1280x720 CDP getFullAXTree + gpt-4o-mini 15-step same model/tools/budget + ST-WebAgentBench safety harness; log versions, hashes, viewport, node count, image pull GHCR, OPENAI_API_KEY, rho_proxy_real per-stratum stratified, DSM amortized cost, safety CuP.
- [ ] Stage qcr_bank_manifest TAU0.30 Jaccard<0.30 630 pairs 0.0, value_set disjoint on all families (rebuild if needed), dsm_registry 714/2147 80-94%, sgdr_index 36 state_key TRAIN-only, cost_config 50/15/180/10, kernel dot-regex d926279d; verify TRAIN-only no contamination; log staged sha + value_set intersection check.
- [ ] Run honest per-trajectory-reset sum counters (no n*3200/jitter), family-stratified trajectory-grouped 5000 bootstrap + 5000 block-permutation with per-stratum rho_length/shuffled/proxy thresholds stratified + Pareto decomposed at f=10/100 + safety.
- [ ] Report M_total Pareto saving >=25% vs COLD <=0.85 vs RAG at both f, margin >=0.12 vs each baseline at both f, AUROC/precision/false_accept/UNKNOWN/ECE per-class, rho_novelty>=0.60 per-stratum, rho_proxy>=0.50, TN, probeHit correlated vs random 0.53, n_non304 stratified, DSM $0.002-0.092, ST-WebAgentBench CuP non-inferior, and per_hit supersede check.
- [ ] Preserve raw evidence, recomputable hashes, frozen formula audit within 1e-6, unresolved distinct from measurement failure; redesign NC1 decoupling L/n via block-permuting novelty labels without weakening thresholds.

*No outcome-bearing measurement was run during DESIGN. This preregistration is frozen before freeze.json.*
