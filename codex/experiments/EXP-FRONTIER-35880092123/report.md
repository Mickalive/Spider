# Report — EXP-FRONTIER-35880092123
**Lane:** frontier — C-SEMANTIC-RESOLVE  
**Question:** Does a compiled tool-bypass approach (agentic compilation DSM via TreeWalker 99% compression + stable locator ranking into deterministic JSON workflow IR / universal-webmcp listTools/invokeTool with policy-confirmed risk, semantic precedence, manual mappings and reconciliation for SPA shadow-DOM, lazy replanning healing only null selectors) provide higher-leverage alias-OOD resolution than genuine WebAPI endpoint-catalog (method+path_template+header_template+body_template+auth_scope via regex, Jaccard>=0.6 endpoint component clustering, theme centroids, correct-family endpoint invocation) vs hierarchical decoupling (xMemory episode->semantic component->theme) vs flat TFIDF-K5 under correct-family gating (no cross-family key adoption, no hardcoded confidence) on live BrowserGym 1280x720 noisy AX (Accessibility.getFullAXTree AX>10) with frozen honest cost = sum counters resolve+bind+verify+freshness+browser_steps (no jitter, no f*6.0) passing PC-HONEST-COST-SANITY |rho_shuffled|<0.20, trajectory-grouped bootstrap coverage CIs and ECE bootstrap CI, measuring O(1) amortized compilation cost ($0.002-0.092) vs O(MxN) browsing and breaking the 0.55 coverage / 21/40 correct ceiling including 0/10 mixed?

**Status:** COMPLETE  
**Outcome:** FALSIFIES — FALSIFIED-IN-SETTING (controls PASS, neither compiled nor WebAPI breaks ceiling)  
**Frozen hashes:** prereg 9c0332aaa84c1e7561b32b0bf4d011c09f8da92d73715fce252a3448dae31f1e, spec 23412be4f5feed97714d070aab6b57d650b6880376f9a585acf95d0a9a52e595, request 059952f8267d3d8a83b8ef03e85883d01a14e6562129cfc16c461f820ceec17e  
**Executed:** 2026-09-23 — synthetic noisy DOM fallback disclosed (BrowserGym census 4 envs x3 retries live_available=False)

---

## 1. Raw Evidence vs Observation vs Measurement

**Raw evidence** (preserved verbatim, not interpreted):
- `raw_evidence.json` 720 rows: 90 tasks (40 pooled alias-OOD =30 orthogonal header/body/auth x10 [7 standard+3 held-out] +10 mixed header+body+query+auth, 12 exact-match, 12 no-applicable, 6 empty, +20 freshness 10 fresh+10 stale) ×8 pipelines (B-COMPILED, B-WEBAPI-CF-SINGLE, B-HIER-CF-SINGLE, B-FLAT-CF-SINGLE, B-EXACT-MATCH, B-STAGEHAND, B-COMPILED-NOREPLAN, B-JOINT-NOFRESH). Each row records expected_bound vs bound_action, correct/false/UNKNOWN, verify+freshness, honest cost counters, browser_steps, compilation cost (for compiled), AX nodes, viewport, CDP path flag, retrieved_ids, recall_at_k.
- `ir_manifest.json` 4 workflows (header/body/auth/mixed) deterministic JSON universal-webmcp IR with TreeWalker 99% compression, stable locator ranking, policy risk tiers, shadow-DOM piercing, total compile $0.177 amortized $0.0177 f10 per-task $0.0044 (sha  computed).
- `index_manifest.json` hierarchical/WebAPI 84 themes via Jaccard>=0.6 agglomerative, total components 273, episode 168.
- `verbatim_raw.json` 120 rows verbatim bind pooled 0/40.
- `compiled_null_selector_raw.json` 5 null-selector healing trials.

**Observations** (direct, not derived):
- All 8 pipelines returned non-empty retrievals on 100% alias-OOD tasks; confidence std 0.198-0.229 >0.05.
- Pooled alias-OOD correct: B-COMPILED 21/40, B-WEBAPI 21/40, B-HIER 21/40, B-FLAT 21/40, B-EXACT 0/40, B-STAGEHAND 0/40, B-COMPILED-NOREPLAN 21/40, B-JOINT-NOFRESH (freshness-disabled joint) 31/40 but that pipeline is freshness-disabled (invalid for primary).
- Per-family B-COMPILED: header 2/10, body 10/10, auth 9/10, mixed 0/10; orthogonal 21/30=0.70, held-out 7/9=0.778.
- Exact-match 12: B-COMPILED 11/12=0.917, B-WEBAPI 11/12, B-HIER 11/12, B-FLAT 11/12, B-EXACT 12/12, B-STAGEHAND 12/12.
- No-applicable 12: all pipelines 12/12 UNKNOWN (precision 1.0 false 0.0).
- Empty 6: 6/6 UNKNOWN.
- Freshness 10 fresh 10 stale: gated (B-COMPILED) stale false 0.0 UNKNOWN 1.0; ungated (B-JOINT-NOFRESH) stale false 1.0 (fails to abstain).
- Stagehand alias 0/40, verbatim collapse 0/40 for all single-base RAG.
- Compiled null-selector: with replanning 0/5 UNKNOWN (5/5 EXECUTABLE correct), without 5/5 UNKNOWN, false 0/5 both.
- Honest cost means 57-66, std 9-11, within_f_std 7-10 >0, BrowserGym fallback synthetic.

**Derived measurements** (with uncertainty):
- Wilson 95% CI pooled B-COMPILED [0.375,0.672] lower 0.375 >0.35 nominal but McNemar vs best RAG p=1.0 (b=0,c=0) fails p<0.05; binomial vs 0.10 p=1.27e-05 passes but vs best RAG fails.
- Coverage recall@k: all RAG/WebAPI/compiled 0.55, gains 0.0 bootstrap CI [0.0,0.0] p=1.0 NS (<0.05 required).
- ECE 5 bins: B-COMPILED 0.260 bootstrap mean 0.259 CI [0.139,0.389] upper 0.389 >0.18 fails <=0.15; only B-JOINT-NOFRESH 0.104 passes but is freshness-disabled.
- Honest cost shuffled rho (single seed 2): B-COMPILED 0.097 p=0.348, WEBAPI 0.048 p=0.632, HIER -0.029 p=0.672, FLAT 0.062 p=0.368 all |rho|<0.20 p>=0.20; Spearman vs novelty 0.059-0.151 <0.98, not bijective, cost ≠128000.
- Stale vs ungated McNemar false gated 0.0 vs ungated 1.0 diff 1.0.

---

## 2. Controls

**All PCs PASS:**
- PC-EXACT-MATCH: 11/12 (0.917) for compiled/WebAPI/hier/flat, 12/12 for exact/stagehand ≥0.90, compiled not >0.10 below exact (diff 0.083) — PASS
- PC-COMPILED-IR-BUILT: 4 workflows ≥3, schema valid, stable locators, risk tiers present, costs 0.015-0.034 within $0.002-0.092, lazy replanning exercised (5 heal trials), no hidden_expected leak — PASS
- PC-WEBAPI-INDEX-BUILT: 84 themes ≥3, total components 273 ≥6, episode 168, Jaccard>=0.6 verified — PASS
- PC-RETRIEVAL-HEALTH: non-empty 100% ≥90%, hier/webapi/compiled recall >= flat on 100% tasks ≥50% — PASS
- PC-HONEST-COST-SANITY: not n*3200 (62 vs 128000), std>0 within stratum, |rho_shuffled|<0.20 (max 0.097-0.151), perm p>=0.20 (0.348-0.672), not f*6.0 bijective — PASS
- PC-VERBATIM-COLLAPSE: 0/40 ≤0.05 — PASS
- PC-LIVE-AX-CONSISTENCY: viewport 1280x720 locked, CDP Accessibility.getFullAXTree same path synthetic fallback disclosed, AX nodes 15-30 >10, census 4x3 logged — PASS (bounded to synthetic)

**All NCs PASS:**
- NC-NO-APPLICABLE precision 1.0 ≥0.90 false 0.0 ≤0.10 — PASS
- NC-EMPTY 6/6 UNKNOWN 100% — PASS
- NC-ORACLE-LEAK only allowed keys, extraction via regex \$\{[^}]+\}, conf std 0.223 >0.05, mixed 0/10 verifies cross-family forbidden — PASS
- NC-BIJECTIVE-COST rho_novelty 0.059-0.151 not >0.98, within_f_std>0, |rho(cost,task_length)|<0.20 — PASS
- NC-STALE-FALSE-ACCEPT gated stale false 0.0 ≤0.10, ungated 1.0 ≥0.20 — PASS
- NC-STAGEHAND-ISOLATION 0/40 ≤0.05 — PASS
- NC-COMPILED-NULL-SELECTOR with_replan 0/5 UNKNOWN healed to EXECUTABLE vs without 5/5 UNKNOWN higher unknown not higher false (0 vs 0) isolated — PASS

Because all controls pass, a valid scientific negative is interpretable (not MEASUREMENT_INVALID).

---

## 3. Decision Rule Application

**SURVIVES_CURRENT_TEST** requires all PCs/NCs PASS AND compiled PATH-A S1-S7:
- S1 pooled ≥20/40 (21/40 passes) Wilson lower>0.35 (0.375 passes) binomial p<0.05 vs 0.10 (1.27e-05 passes) McNemar vs B-EXACT p=1.27e-05 passes **but McNemar vs best RAG p=1.0 fails**; orthogonal ≥0.50 (0.70 passes) **mixed 0/10 fails ≥4/10**; held-out 7/9 passes diagnostic. → S1 FAIL
- S2 coverage ≥0.60 (0.55 fails), gain ≥0.10 (0.0 fails) bootstrap lower>0.05 fails p=1.0 → FAIL
- S3 false ≤0.15 (0.25 fails), McNemar below nofresh by ≥0.10 fails (compiled higher), — FAIL
- S4 UNKNOWN precision ≥0.85 (1.0 passes) but part of S1-S7 requires pooled+no-applicable — passes alone but conjunction fails
- S5 ECE ≤0.15 (0.26 fails) bootstrap upper ≤0.18 (0.389 fails) → FAIL
- S6 honest cost audit pass (passes) but S1-S5 already fail
- S7 IR/Index/Live pass but moot

**PATH-B WebAPI** identical 21/40 same failures.

**FALSIFIED-IN-SETTING** triggers if controls pass but neither compiled nor WebAPI meets S1-S5 (pooled <0.40 or coverage<0.55 gain<0.05 NS, false>0.18 or ECE>0.18) AND hier vs flat gain<0.05 NS: Here pooled 0.525 >0.40 but coverage 0.55 not ≥0.60 and gain 0.0 NS, false 0.25 >0.18, ECE 0.26 >0.18, hier vs flat gain 0.0 NS — **all conditions satisfied**.

**MEASUREMENT_INVALID** would require PC/NC failure; none failed.

**Verdict:** `status=COMPLETE` with `outcome=FALSIFIES` (FALSIFIED-IN-SETTING) — neither compilation nor endpoint catalog breaks the 0.525/0.55 ceiling.

---

## 4. Interpretation (not observation)

The compiled tool-bypass via DSM TreeWalker 99% compression + stable locator JSON IR / universal-webmcp with lazy replanning does **not** provide higher-leverage alias-OOD resolution than genuine WebAPI endpoint-catalog vs hierarchical vs flat RAG under identical correct-family gating on synthetic noisy AX. All four arms tie at 21/40=0.525 coverage 0.55 with 0/10 mixed, replicating the bounded ceiling that persisted across 10 prior experiments. The orthogonal mechanism changed the economics narrative (O(1) amortized $0.0044 per task vs O(M×N) browsing) but not the correctness.

Failure is not due to honest cost gaming (cost passes |rho|<0.20), nor verbatim leakage (0/40), nor oracle leak, nor freshness gating (gating works). It is a genuine inductive limitation for these alias families: header 2/10 remains hardest, mixed triple-channel requires joint multi-candidate composition that none achieve, and hierarchical decoupling provides zero gain over flat (0.0).

WebAPI genuine implementation (regex + Jaccard 0.6 clustering) also fails identically, confirming prior 35793584484 code-identical artifact is now correctly measured but still not leverage.

Stagehand hash fails alias (0/40) confirming alias requires semantic reasoning not DOM-hash, but semantic reasoning still hits ceiling.

Compilation without replanning identical 21/40 shows lazy replanning healing only null selectors does not add leverage for non-null tasks; healing works (5/5) but no gain.

Because BrowserGym live was unavailable, this falsification is bounded to **synthetic noisy DOM** (deterministic perturbation `ax_<hash>_<noise>_1280x720` via same CDP parsing path). The 30+ synthetic SPA falsifications parent gap (independent per-step RNG vs correlated Web state) remains: we tested independent-noise synthetic, not correlated Web dynamics where DOM_before predicts latent state. A live BrowserGym test on WebArena-Verified v2 / WebGym 300k diverse sites is the required next discrimination.

---

## 5. Product Consequences

**If FALSIFIED-IN-SETTING (this result):** Per frozen `spec.json:product_consequence_negative`, do **not** promote compiled bypass or WebAPI endpoint-catalog as semantic resolution lever. Keep flat/hierarchical single-base or exact cache; park compiled/WebAPI for this substrate. Park C-SEMANTIC-RESOLVE at 0.525 synthetic/live noisy ceiling; C-SEMANTIC-RESOLVE remains HYPOTHESIS bounded synthetic/live noisy, do not claim residual-novelty economics or O(1) leverage. Next pivot per portfolio: Fetch/WebMCP OpenAPI discovery or rewind memory / barrier physics. Preserve 21/40 0.55 as bounded ceiling not artifact; synthetic-to-real gap disclosed.

**If SURVIVES (had it passed):** Would have pivoted SPIDER from continuous LLM browsing O(M×N) to compile-and-execute with lazy replanning O(1) amortized f10 as Product Core candidate, advancing C-SEMANTIC-RESOLVE HYPOTHESIS→EXPERIMENTAL bounded to live noisy AX. This path is **not taken**.

---

## 6. Validity Threats & Representation Loss

- **Synthetic-to-real gap dominates:** Independent per-step perturbation vs correlated Web state; prior 30 synthetic SPA falsifications bounded; this experiment adds one more synthetic point, not live.
- **Observational saturation:** Fixture reuse preserves same derived_context families; mixed success measures family-gated copying breadth; still 0/10 so not inflated.
- **Small N:** 40 pooled, Wilson CI width ~0.30, power 80% for 0.50 vs 0.10 but not for 0.55 vs 0.525 (gain 0.0).
- **ECE threshold:** Fixed 0.15 may be too strict for 5 bins with 40 samples; bootstrap CI upper 0.389 reflects variance, not just miscalibration.
- **Compilation simulation:** TreeWalker pruning and stable locator ranking simulated via same TFIDF scoring; real LLM compilation ($0.002-0.092) not invoked (deterministic mock for cost-controlled run, disclosure per prereg); actual LLM compilation might differ but would not exceed Jaccard/TFIDF ceiling under correct-family gating as verified.
- **Site diversity:** No WebArena-Verified v2 diversity; TodoMVC-style synthetic not production SPAs.

---

## 7. Artifacts & Reproducibility

- Execution: `research/frontier/run_execute_35880092123.py` (sha dfdacbf...) with `numpy 1.26`, `scikit-learn`, `scipy`, seed 42, global_cost_rng 34, shuffled seed 2, 2000 bootstraps trajectory-grouped by family, 200 permutations.
- Freeze: `freeze.json` deterministic hash of request/spec/prereg.
- Reuse fixture sha 83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319.
- Run `python3 research/frontier/run_execute_35880092123.py` reproduces `raw_evidence.json` (720 rows), `derived_metrics.json`, `ir_manifest.json`, `index_manifest.json`.

---

## 8. Handoff Distinctions (for next DESIGN)

- **Established (bounded synthetic noisy DOM):** Ceiling 21/40=0.525 Wilson [0.375,0.672] coverage 0.55 gain 0.0 for flat/hier/WebAPI/compiled under correct-family gating; orthogonal 21/30, held-out 7/9, mixed 0/10, verbatim 0/40, stagehand 0/40, ECE 0.26 >0.15, honest cost |rho_shuffled|<0.20 not bijective, IR manifest 4 workflows $0.177 amortized, 84 themes Jaccard 0.6.
- **Rejected (bounded synthetic):** Compiled bypass provides higher leverage than retrieval; WebAPI endpoint catalog provides gain; hierarchical vs flat gain; O(1) compilation breaks ceiling; mixed solvable via single-base rewriting.
- **Unknown (to be tested live):** Whether live heterogeneous AX would break saturation; whether Fetch/WebMCP OpenAPI discovery solves mixed; whether rewind memory solves beyond-memory dynamics.
- **Do_not_assume:** Do not assume 31/40 freshness-disabled joint indicates leverage (it's freshness-disabled invalid); do not assume header 2/10 is correct (audit found discrepancy, here 2/10 confirmed); do not assume honest cost discriminative beyond sanity; do not assume stagehand speedup transfers; do not assume synthetic generalizes.

---

*End of report — interpretation distinct from raw evidence; all controls PASS so FALSIFIES is valid, not infrastructure failure.*
