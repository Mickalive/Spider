# EXP-FRONTIER-35860354553 — Preregistration

**Lane:** frontier — Search outside current solution basin for high-upside falsifiable mechanisms.
**Experiment ID:** EXP-FRONTIER-35860354553
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids) — HYPOTHESIS per registry; owned by graph/product/frontier.
**Director mandate:** PIVOT with cognitive_reset true, SUPERSEDE parent handoff, allocation action PIVOT to C-SEMANTIC-RESOLVE per request.json director_mandate. Strategic question verbatim in spec.json `question`. This prereg converts that strategic question into the smallest rigorous high-information falsifiable experiment.

## 1. Background and why this is the smallest high-information experiment

Frontier is tunnel_flagged true with 9/10 recent C-SEMANTIC-RESOLVE experiments on the same synthetic orthogonal header/body/auth + mixed multi-channel harness (tasks_expanded.json sha 83b7c52d) showing:
- under powerful adopt-any-observed-key reconstruction: 39-40/40 correct (0.975) coverage 1.0 for any non-empty retrieval set (artifact, structural)
- under discriminating RULE-CORRECTFAMILY (cross-family forbidden, correct-family-required rewriting, pool 8>k=5): collapse to 21/40=0.525 Wilson [0.375,0.671] coverage 0.55 with 0.0 gain for hierarchical xMemory vs flat TFIDF-K5 vs WebAPI endpoint mining, per-family body 10/10 auth 9/10 header 2/10 mixed 0/10, ECE 0.257>0.15 false 0.25>0.15 (EXP-FRONTIER-35793584484 audit PASS, EXP-FRONTIER-35796871743 audit MEASUREMENT_INVALID with 31/40 hardcoded).

Re-tuning Jaccard 0.6, entropy 0.4, k, or adding another alias family re-enters the same basin where recall@k=1.0 for any set and cross-family adoption masks solution. The inherited next_question (joint multi-candidate composition with honest cost on same synthetic noisy DOM) is another parameterization of that sweep (Director comparative reasoning). Per Frontier charter and portfolio assessment, highest leverage is to leave the basin: test orthogonal levels of description on live BrowserGym 1280x720 noisy DOM/AX where minimal-derived-dict tautology (headers_observed directly contains aliased key) and DOM-hash selector replay fail, and where honest kernel-gated cost (branch-derived counters) replaces bijective f*6.0 that inflated rho to 0.97-0.995.

Two orthogonal alternatives dominate per Director rationale and Scout brief:
1. **Tool/API bypass:** WebAPI endpoint+method+auth-scope mining (direct endpoint discovery + describe) vs template rewriting — tests whether SPIDER should remain selector replay or become tool compilation (endpoint invocation vs rewriting).
2. **MEA auditor architecture:** fresh-context executor + independent auditor (verified facts only) — tests whether independent verification before state update breaks the 0.55 coverage ceiling without denoising, motivated by prior that long-horizon context rot is linear and MEA pattern outperforms in-context memory.

This experiment tests both in one frozen substrate: primary PATH-A WebAPI bypass vs hierarchical vs flat under identical correct-family gating on live BrowserGym noisy AX; conditional PATH-B MEA fresh+auditor if PATH-A fails. Either outcome changes claim/product decision (promotion to tool compilation or verified-state architecture vs park both and pivot to compile-and-execute blueprint / Fetch/WebMCP).

## 2. Scientific question (frozen)

Does WebAPI endpoint+method+auth-scope mining provide higher-leverage alias-OOD resolution than hierarchical decoupling-before-aggregation vs flat top-k RAG on live BrowserGym 1280x720 noisy DOM/AX (not synthetic minimal-derived-dict) — testing correct endpoint invocation vs template rewriting under correct-family-required gating (no cross-family key adoption, no hardcoded confidence) on orthogonal header/body/auth + mixed splits (40 pooled 30 orthogonal 10 mixed 9 held-out): alias-OOD correct >=0.50 (binomial p<0.05 vs 0.10, McNemar p<0.05 vs exact matcher), false_accept <=0.15, UNKNOWN precision >=0.85, ECE <=0.15, trajectory-grouped bootstrap CIs, plus honest kernel-gated cost vs Stagehand — and if not, does MEA-pattern fresh-context executor + independent auditor (verified facts only) break the 0.55 coverage and 21/40 correct ceiling?

## 3. Hypothesis (frozen)

On live BrowserGym 1280x720 noisy DOM/AX (Accessibility.getFullAXTree at locked viewport, dom_ax_hash/dom_text_hash noisy) hierarchical and WebAPI single-base retrieval diversity alone does not break the 21/40=0.525 coverage 0.55 ceiling (0/10 mixed, ECE>0.15). Under correct-family-required gating, WebAPI endpoint discovery (endpoint theme mining, endpoint invocation via correct-family rewrite) achieves pooled correct >=0.50 and coverage >=0.60 with gain >=0.10 over best flat, false<=0.15 precision>=0.85 ECE<=0.15 with honest kernel-gated cost vs Stagehand (Stagehand 80% speedup zero tokens on hit baseline). If WebAPI does not dominate, the MEA auditor pattern (fresh-context executor none Shared memory + independent verifier that promotes only verified facts) breaks the same ceiling with identical calibration gates, demonstrating verification architecture leverage over denoising.

## 4. Claim linkage

- **Primary:** C-SEMANTIC-RESOLVE (HYPOTHESIS, owner frontier/graph/product) — next_gate: unseen-goal resolution with applicability/abstention calibration. Positive requires pooled correct significance, coverage gain, calibration, and honest cost isolation vs Stagehand.
- **Secondary (economics, not promoted):** Informs C-RESIDUAL-NOVELTY and C-PRODUCT-ECON via honest cost measurement but does not advance them; reuse same honest-cost accounting to avoid bijective artifact flagged by Director priors (cost=250+500*10*novelty guarantees rho~1.0).
- **Supercedes:** Parent handoff EXP-FRONTIER-35796871743 carry_forward is continuity evidence only. Per director_mandate parent_handoff_disposition SUPERSEDE and cognitive_reset true, we do not continue its synthetic joint-composition tuning; we preserve its established ceiling (21/40=0.525 coverage 0.55 mixed 0/10 under CF, verbatim 0/40 collapse, bijective rho 0.995 rejected) as bounded, not as agenda.

## 5. Experimental design (frozen)

### 5.1 Substrate and fixtures — live with disclosed synthetic fallback

Reuse byte-identical intents/expected from tasks_expanded.json sha 83b7c52d / tasks.json sha 4abf14872 (40 pooled =30 orthogonal header/body/auth x10 [7 standard+3 held-out] +10 mixed header+body+query+auth co-occurring, 12 exact, 12 no-applicable, 6 empty =70 tasks; per-task registry 8: 1 train 0.9 +2 same-family 0.9 +2 cross-family 0.9 +2 mixed 0.85 +1 random 0.8). Verify 0/40 leak 0/9 held-out 0/10 mixed.

**Live extension:** derived_context for retrieval/mining/composition/auditor is enriched via Playwright CDP Accessibility.getFullAXTree at locked 1280x720 viewport (browsergym-core 0.14.3 + agentlab 0.4.2 + playwright 1.63.0 per Scout pin correction). Parse heterogeneous WebShop/WebArena/ALFWorld stubs or minimal TodoMVC with injected DOM noise to dom_ax_hash/dom_text_hash + header/body/query families using identical parsing code. If BrowserGym unavailable after exhaustive enumeration (4 envs x3 retries logged, agentlab pin verified on PyPI, playwright check), fallback is deterministic perturbation of synthetic dom_ax_hash with same 1280x720 parsing code path, disclosed as synthetic noisy DOM; claim then bounded to synthetic noisy DOM not live (validity note). Viewport and parsing path frozen, audited via PC-LIVE-AX-CONSISTENCY.

Correct-family gating and auditor verification status are recorded per task.

### 5.2 Pipelines (baselines) — stable IDs

All pipelines share same CF rule and freshness TTL except ablations; confidence via softmax temp 0.15 + jitter gated UNKNOWN<0.80.

- B-EXACT-MATCH (B-EXACT-MATCH)
- B-FLAT-TFIDF-K5-CF (B-FLAT-CF-SINGLE) — flat TFIDF top-5 + CF single rewrite
- B-HIERARCHICAL-CF (B-HIER-CF-SINGLE) — xMemory Jaccard>=0.6 adaptive k 2-5 + CF single rewrite
- B-WEBAPI-CF-SINGLE (B-WEBAPI-CF-SINGLE) — WebAPI endpoint mining + CF endpoint invocation (endpoint components parsed via regex \${[^}]+}, Jaccard 0.6 clustering, theme centroids)
- B-WEBAPI-JOINT-CF (B-WEBAPI-JOINT-CF) — WebAPI endpoint pool + joint composer (up to 3 complementary families, joint rewrite, joint verify+freshness)
- B-STAGEHAND-DOMHASH (B-STAGEHAND) — Stagehand exact-selector+DOM-hash, deterministic cache
- B-BROWSERUSE-CACHE (B-BROWSERUSE) — exact replay cache 99% hit
- B-MEA-FRESH-AUDITOR (B-MEA-AUDITOR) — fresh-context executor + independent auditor (separate context, verified facts only)
- B-MEA-FRESH-NOAUDIT (B-MEA-NOAUDIT) — fresh executor without auditor (ablation)
- B-FRESHNESS-DISABLED-JOINT (B-JOINT-NOFRESH) — WebAPI joint without freshness TTL (ablation)

Staleness/freshness labels from watermark/version drift, not test signals.

### 5.3 Controls — stable IDs (must pass before any SURVIVES/FALSIFIES)

**Positive controls (PC):**
- PC-EXACT-MATCH: exact N12 >=0.90 correct <=0.10 false for all pipelines.
- PC-RETRIEVAL-HEALTH: alias-OOD pooled non-empty >=90%, hierarchical/WebAPI distinct coverage >= flat on >=50%.
- PC-WEBAPI-INDEX-BUILT: WebAPI endpoint index >=3 themes >=6 components episode==registry size no leak.
- PC-MEA-AUDITOR-HEALTH: auditor on exact/no-applicable verified precision>=0.90, stale UNKNOWN precision>=0.85, Jaccard valid vs stale <0.5, promotions subset of verified facts.
- PC-HONEST-COST-SANITY: honest cost = sum kernel counters + browser steps, not n*3200 within 1%, varies within stratum std>0, shuffled rho |<0.20, audit inspects function for f*6.0 bijective term.
- PC-VERBATIM-COLLAPSE: verbatim pooled <=0.05 for single-base (confirm alias not in registry).
- PC-LIVE-AX-CONSISTENCY: viewport 1280x720 locked, Accessibility.getFullAXTree same path for live and fallback.

**Null controls (NC):**
- NC-NO-APPLICABLE: N12 UNKNOWN precision>=0.90 false<=0.10.
- NC-EMPTY: N6 empty registry 100% UNKNOWN.
- NC-ORACLE-LEAK: derived_context allowed keys only, endpoint extraction parses template strings only, confidence std>0.05, cross-family forbidden verified.
- NC-BIJECTIVE-COST: rho(cost,novelty) not >0.98 zero variance, within-stratum std>0 |rho(length)|<0.20 permutation p>=0.20.
- NC-AUDITOR-HALLUCINATION: auditor false<=0.10 precision>=0.85 on stale/no-applicable; with-auditor false at least 0.10 below without-auditor.
- NC-STALE-FALSE-ACCEPT: stale N12 gated false<=0.10 precision>=0.85, ungated false>=0.20.
- NC-STAGEHAND-ISOLATION: Stagehand pooled <=0.05 alias-OOD (hash insufficient).

Any PC/NC failure => MEASUREMENT_INVALID (validity_notes explain, unresolved list).

### 5.4 Metrics — stable identities for EXECUTE/AUDIT/DIRECTOR transmission

- `alias_OOD_pooled_correct` (40 pooled, 30 orthogonal 10 mixed) — binomial vs 0.10, Wilson 95% CI, McNemar vs B-EXACT-MATCH and vs B-FLAT-CF and vs Stagehand
- `alias_OOD_coverage` (mean recall@k under CF+joint/auditor) and `coverage_gain` vs best flat-CF — block bootstrap 2000 trajectory-grouped by family (header/body/auth/mixed), CI lower
- `per_family_correct` header/body/auth/mixed, `held_out_correct` (9 held-out), `orthogonal_correct` (30)
- `false_accept_rate` pooled + per pipeline — McNemar
- `unknown_precision` pooled alias-OOD + no-applicable
- `auditor_verified_precision` (for MEA)
- `ece` 5 bins + `ece_ci` bootstrap, `confidence_std`
- `honest_cost` per task (branch-derived counters + browser steps) — audit for bijectivity, mean/std per stratum, `rho_shuffled`, `leverage_vs_stagehand` narrative
- `stale_false_accept`, `no_applicable_unknown_precision`, `empty_unknown_rate`
- `index_manifest` hash/lists for endpoint themes/components

All metrics recorded in result.json under stable names above.

### 5.5 Sample size and power

Alias-OOD pooled N=40 gives 80% power for 0.50 vs 0.10 null at alpha 0.05 one-sided binomial (requires 20/40). Mixed diagnostic N=10 requires >=4/10 to claim mixed improvement vs 0/10 parent (Fisher exact). Exact/no-applicable/stale-fresh meet minimums (>=12/6/16). Bootstrap 2000 gives stable coverage/ECE CIs. Pool>k (8>5) already satisfied.

### 5.6 Determinism

numpy RandomState 42, random.seed 42, hashlib.sha256 not Python hash(), TFIDF/embed normalized deterministic, clustering deterministic, paired per-task evaluation. BrowserGym viewport locked, CDP parsing deterministic, retry enumeration logged.

## 6. Decision rule (frozen, requires all PCs/NCs)

Surfaces in spec.json `decision_rule`. Summary:

**MEASUREMENT_INVALID** if any mandatory PC/NC fails or pooled N<32 or live claim made without live census or verbatim collapse not disclosed.

**SURVIVES_CURRENT_TEST** iff controls pass AND at least one path passes:

- PATH-A WebAPI: S1 pooled WebAPI-CF (or WebAPI-JOINT-CF) >=20/40=0.50 Wilson lower>0.35 binomial p<0.05 vs 0.10 McNemar p<0.05 vs B-EXACT-MATCH and vs B-FLAT-CF; orthogonal >=0.50 mixed >=4/10; S1b coverage >=0.60 lower>0.45 gain >=0.10 lower>0.05 p<0.05; S2 false<=0.15 McNemar below B-JOINT-NOFRESH >=0.10 and below Stagehand; S3 unknown precision>=0.85; S4 ECE<=0.15 CI upper<=0.18; S5 honest cost audit pass + Stagehand comparison narrative.

- OR PATH-B MEA: if PATH-A falsified, MEA-FRESH-AUDITOR pooled >=20/40=0.50 binomial p<0.05 vs 0.10 McNemar p<0.05 vs B-EXACT-MATCH and vs B-MEA-NOAUDIT and vs best flat-CF; coverage >=0.60 gain>=0.10 lower>0.05; auditor verified precision>=0.85 false<=0.15 ECE<=0.15.

**FALSIFIED-IN-SETTING** if controls pass but neither PATH-A nor PATH-B meets S1-S4 (pooled <0.40 or p>=0.05, coverage <0.55 or gain<0.05 NS, false>0.18 or precision<0.80 or ECE>0.18).

**MIXED** if controls pass but intermediate (pooled 0.40-0.49 or mixed 2-3/10 or ECE 0.15-0.18 or gain 0.05-0.09 p>=0.05) — bounded ceiling, no promotion.

All tests pre-freeze: no outcome inspection during DESIGN.

## 7. Validity threats and mitigations

- **Minimal-derived-dict tautology:** Mitigated by requiring live noisy AX enrichment; synthetic fallback disclosed and claim bounded; dom_ax_hash adds non-trivial copy where flat was trivial.
- **Bijective cost rho 0.97-0.995:** Mitigated by PC-HONEST-COST-SANITY and NC-BIJECTIVE-COST (branch-derived counters, no f*6.0, within-stratum variance checks, shuffled permutation p).
- **Hardcoded confidence override:** Mitigated by auditing softmax temp 0.15 + jitter pipeline, confidence std>0.05, not constant.
- **Adopt-any-key contamination (39/40):** Held as PC-VERBATIM-COLLAPSE <=0.05 verbatim, confirming 21/40 CF ceiling is real.
- **Cross-family key adoption masking 0.0 gain:** Mitigated by correct-family gating and NC-ORACLE-LEAK cross-family audit; hierarchical/WebAPI distinct coverage must exceed flat only when family matches.
- **Stagehand DOM-hash 80% speedup confound:** Stagehand baseline included head-to-head on alias-OOD where hash fails (NC-STAGEHAND-ISOLATION <=0.05) to show alias requires semantic/endpoint reasoning.
- **BrowserGym substrate unavailability (0/4 envs prior):** Exhaustive census logged, synthetic fallback with same parsing path disclosed, claim ceiling bounded to synthetic noisy DOM if live unavailable; follows runtime lane dependency per Director.
- **Auditor hallucination:** NC-AUDITOR-HALLUCINATION gates false_accept and precision; MEA no-audit ablation isolates fresh context vs verification.
- **Insufficient holdout:** Holdout 9 families + mixed 10 ensures generalization not memorization; leak 0/40 verified.

## 8. Product consequences (frozen)

**If SURVIVES via PATH-A:** WebAPI tool/API bypass is higher-leverage than template rewriting on noisy DOM/AX — promote endpoint discovery+describe (catalog mining Jaccard 0.6, endpoint theme selection adaptive k 2-5, CF endpoint invocation) to Product Core candidate with honest cost accounting vs Stagehand; C-SEMANTIC-RESOLVE HYPOTHESIS->EXPERIMENTAL bounded to live (or synthetic noisy) at 0.50/0.60 ceiling with calibration.

**If SURVIVES via PATH-B only:** MEA verified-state architecture breaks ceiling without denoising — promote fresh-context executor + independent auditor (verified facts only, rewind memory, trajectory-grouped CIs) to Product Core; tool compilation not required but verification required.

**If FALSIFIED (both paths):** Neither endpoint mining nor MEA auditor breaks 0.525/0.55 ceiling under honest cost and correct-family gating on header/body/auth+mixed with noisy DOM/AX — park both retrieval-diversity and endpoint/MEA for these families at 0.525 ceiling; product must keep exact cache/Stagehand for hits and pursue orthogonal basins: compile-and-execute blueprint, Fetch/WebMCP OpenAPI/HATEOAS discovery (dependencies runtime+intel), or Physics barrier/committor approaches. C-SEMANTIC-RESOLVE remains HYPOTHESIS/EXPERIMENTAL bounded synthetic/live noisy; do not claim residual-novelty economics.

## 9. Estimation and execution notes for EXECUTE

- EXECUTE must not mutate frozen spec/request/prereg/freeze.
- Keep RAW EVIDENCE (browser AX trees, kernel counter logs, index manifests, per-task raw_evidence.json) distinct from OBSERVATIONS (correct/false/unknown per pipeline per family) and DERIVED MEASUREMENTS (rates, Wilson, binomial, McNemar, bootstrap CIs, ECE).
- Preserve raw evidence hashes in artifacts with role raw/derived/fixture/code.
- Write result.json with schema_version 1, required top-level shape per EXPERIMENT_PACKET.md (status COMPLETE/BLOCKED/MEASUREMENT_INVALID, outcome SUPPORTS/FALSIFIES/MIXED/INCONCLUSIVE/NOT_APPLICABLE, metrics, controls, artifacts, observations, validity_notes, unresolved).
- Provenance.json must record git run id, commits, BrowserGym/census logs, agentlab/playwright versions, viewport, seed, dataset sha, code paths.
- Do not hardcode alias-OOD outcomes or confidence; derive from bind_joint_CF->verify->freshness->auditor pipeline; cost from counters not formula.
- Trajectory-grouped bootstrap: group by header/body/auth/mixed family, 2000 resamples, report CIs and p values.
- Honest cost: sum counters['resolve']+counters['bind']+counters['verify']+counters['freshness_check']+browser_steps; remove any f*6.0 or n*3200 term; audit will inspect cost function.

## 10. Expected information gain

Very high per cost (<45 min, no LLM tokens, CPU + optional live page loads) and decisive: forks product architecture (selector replay vs tool compilation vs verified-state). Either positive isolates orthogonal leverage beyond retrieval tuning basin where 9/10 experiments tunneled, or negative cleanly closes both endpoint and auditor for these families under honest noisy substrate and forces next Frontier pivot to blueprint synthesis or OpenAPI bypass per Director comparative reasoning. Preserves comparability via byte-identical fixture and honest cost, avoiding another alias family sweep with diminished marginal information.

---
*Preregistration frozen before outcome inspection. Any deviation after seeing outcomes is exploratory and requires new prereg and untouched evidence.*
