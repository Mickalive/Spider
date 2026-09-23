# Preregistration — EXP-FRONTIER-35880092123

**Lane:** frontier  
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids)  
**Mode:** DESIGN ONLY — no outcome-bearing measurements run in this stage (AGENTS.md, EXPERIMENT_PACKET.md DESIGN->EXECUTE).  
**Director mandate:** PIVOT with cognitive_reset=true, SUPERSEDE parent_handoff, allocation claim_id C-SEMANTIC-RESOLVE per `request.json` `director_mandate` (global-director-PIVOT). Parent handoff `research/experiments/EXP-FRONTIER-35860354553/handoff.json` is continuity evidence only.  
**Experiment ID:** EXP-FRONTIER-35880092123  
**Created:** 2026-09-23

---

## 1. Question (Director binding)

> Does a compiled tool-bypass approach (agentic compilation DSM via TreeWalker 99% compression + stable locator ranking into deterministic JSON workflow IR / universal-webmcp listTools/invokeTool with policy-confirmed risk, semantic precedence, manual mappings and reconciliation for SPA shadow-DOM, lazy replanning healing only null selectors) provide higher-leverage alias-OOD resolution than genuine WebAPI endpoint-catalog (method+path_template+header_template+body_template+auth_scope via regex, Jaccard≥0.6 endpoint component clustering, theme centroids, correct-family endpoint invocation) vs hierarchical decoupling (xMemory episode→semantic component→theme) vs flat TFIDF-K5 under correct-family gating (no cross-family key adoption, no hardcoded confidence) on live BrowserGym 1280×720 noisy AX (Accessibility.getFullAXTree AX>10) with frozen honest cost = sum counters resolve+bind+verify+freshness+browser_steps (no jitter, no f*6.0) passing PC-HONEST-COST-SANITY |ρ_shuffled|<0.20, trajectory-grouped bootstrap coverage CIs and ECE bootstrap CI, measuring O(1) amortized compilation cost ($0.002–0.092) vs O(M×N) browsing and breaking the 0.55 coverage / 21/40 correct ceiling including 0/10 mixed?

Smaller discriminating test derived from this: compare the four arms under identical correct-family gating and honest cost on the same frozen fixture, with live-vs-synthetic AX provenance declared, using the same statistical gates that previously bounded the ceiling (21/40=0.525, coverage 0.55, mixed 0/10, ECE 0.26, ρ_shuffled=+0.2297 violation).

---

## 2. Hypothesis (falsifiable)

**H1 (compiled leverage):** On live BrowserGym 1280×720 noisy AX where `derived_context` contains heterogeneous `dom_ax_hash`/`dom_text_hash` from `Accessibility.getFullAXTree` (AX>10 nodes) rather than synthetic minimal-derived-dict tautology (`derived_context == expected_bound` verbatim), the compiled bypass achieves higher-leverage alias-OOD resolution under identical correct-family gating than genuine WebAPI vs hierarchical vs flat RAG.

Operationally, **H1 predicts:**

- Pooled alias-OOD correct ≥20/40 =0.50 (Wilson lower >0.35, one-sided binomial p<0.05 vs chance 0.10, McNemar p<0.05 vs B-EXACT-MATCH 0/40 and vs best correct-family RAG ≈21/40)
- Coverage ≥0.60 with absolute gain ≥0.10 over best RAG (trajectory-grouped block bootstrap 2000, CI lower >0.05, p<0.05)
- Per-family header ≥4/10 (vs prior 2/10) and mixed ≥4/10 (vs prior 0/10) diagnostic
- false_accept ≤0.15, UNKNOWN precision ≥0.85, ECE ≤0.15 with bootstrap CI upper ≤0.18
- Honest cost passes |ρ_shuffled|<0.20 with permutation p≥0.20 and is not bijective (≠ n×3200, std>0 within same novelty stratum)
- O(1) amortized compilation cost $0.002–0.092 at amortization factor f=10 vs O(M×N) browsing steps, with lazy replanning healing only null selectors

**Null expectations (no leverage):** All four arms remain at the bounded ceiling 21/40 pooled, coverage 0.55, mixed 0/10, with coverage gain 0.0 bootstrap NS, and/or honest cost shows bijective or shuffled correlation.

This preregistration does not claim broader C-RESIDUAL-NOVELTY or C-PRODUCT-ECON promotion; economics is measured as amortized cost within C-SEMANTIC-RESOLVE.

---

## 3. State representation (frozen)

**Registry/fixture (byte-identical reuse):** `tasks_expanded.json` sha `83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319` (same as EXP-FRONTIER-35860354553/35793584484): 40 pooled alias-OOD =30 orthogonal (header 10 / body 10 / auth 10, each 7 standard +3 held-out) +10 mixed (header+body+query+auth co-occurring), plus 12 exact-match, 12 no-applicable, 6 empty, +20 freshness (10 fresh +10 stale), per-task registry 8 (1 training +2 same-family +2 cross-family +2 mixed +1 random). Preserved invariants: 0/40 leak, 0/9 held-out leak, 0/10 mixed leak, 9 held-out total, 84 themes via Jaccard≥0.6 in prior (recomputed).

**Live noisy AX extension (frozen protocol):** `derived_context` enriched via CDP `Accessibility.getFullAXTree` at locked viewport 1280×720. Fields exposed to retrieval/mining/compilation: `url`, `method`, `url_path`, `url_query`, `url_segments`, `headers_observed`, `body_observed`, `dom_ax_hash`, `dom_text_hash`, `freshness_watermark`/`version`, and compressed AX snapshot (TreeWalker output 99% pruned). Forbidden keys never present (audited): `alias_family`, `query_key`, `target_prefix`, `routing_prefix`, `target_style`, `path_style`, `header_key`, `body_field`, `auth_scope`, `expected_template`, `expected_endpoint`, `staleness` label, `hidden_expected`.

**Fallback rule (disclosed):** If BrowserGym 0.3.0/0.4.2 + Playwright 1280×720 unavailable after exhaustive census (4 envs: WebArena/WebShop/WebLINX/WorkArena ×3 retries, installs `browsergym-core==0.3.0`/`0.4.2`, `playwright==1.63.0`, `agentlab==0.4.2`, AX>10 validation), harness simulates noisy AX via deterministic perturbation `ax_<hash>_<noise>_1280x720` using the **same** `Accessibility.getFullAXTree` parsing code path. Claim then bounded to *synthetic noisy DOM*, not live, and reported as such (validity note, not hidden).

**Dependencies (Director):** `runtime: BrowserGym 0.3.0/0.4.2 + Playwright 1280x720 with CDP Accessibility.getFullAXTree AX>10 and honest counters`; `intel: WebArena-Verified v2 and WebGym 300k manifests` for site diversity census.

---

## 4. Action representation (frozen)

- **RAG/WebAPI action_template:** URL/header/body/auth template with `${slot}` placeholders for mixed triple-channel (e.g., `X-Api-Key: ${tok}`, `body.api_token=${tok}`, `query.permission=${perm}`).
- **WebAPI endpoint spec:** tuple `(method, path_template, header_template, body_template, auth_scope)` parsed from template strings via regex `\$\{[^}]+}` + splitting; component sets `{path_segments, query_keys, header_keys, body_fields, auth_scopes}` Jaccard≥0.6 agglomerative revisable clustering, theme centroids, complementary top-down selection (entropy>0.4, distinct coverage<2, adaptive k 2–5).
- **Compiled IR:** deterministic JSON workflow IR (universal-webmcp `listTools`/`invokeTool` pattern) with `toolId`, stable locator (`role`, `name`, `testId`, CSS fallback, shadow-DOM piercing), `policy_risk` (confirmed), `semantic_precedence`, manual mappings, SPA shadow-DOM reconciliation. Execution is deterministic; **lazy replanning** heals only the step whose selector is null (single LLM call), not full browsing.

**Pipeline isolation (frozen):** Single-base RAG/WebAPI pipelines rewrite at most one candidate per family; joint RAG/WebAPI pipelines rewrite up to 3 candidates with complementary families jointly; compiled pipeline executes IR deterministically; all share identical correct-family gating and `verify`+`freshness` gates except ablations. Confidence = softmax over candidate/endpoint/tool scores with temperature 0.15 + jitter, gated `UNKNOWN` if max <0.80. No hardcoded confidence.

---

## 5. Target

**Primary target (per-task trichotomy):**

- `correct` — `bound_action`/`tool_binding` == `expected_bound` after correct-family rewrite/joint composition/IR execution **and** passes `kernel.verify()` and `freshness_check`, including all channels for mixed (header+body+query+auth) and correct endpoint/method/auth_scope for WebAPI/compiled.
- `false_accept` — wrong template/endpoint/tool, bound mismatch, or should have abstained (stale or no-applicable or unhealed null selector).
- `UNKNOWN` — correctly abstained via confidence <0.80 or freshness TTL exceeded or auditor/replanning correctly withheld.

Derived aggregate metrics (stable identities): `metric_pooled_correct` (pooled 40), `metric_per_family_correct` [header/body/auth/mixed], `metric_coverage` (mean recall@k under correct-family), `metric_coverage_gain` (vs best RAG), `metric_false_accept`, `metric_unknown_precision`, `metric_ece` (5 bins), `metric_ece_bootstrap_ci`, `metric_honest_cost` (frozen sum), `metric_rho_shuffled`, `metric_rho_shuffled_perm_p`, `metric_amortized_compile_cost` (compile_cost/f), `metric_browser_steps`.

---

## 6. Sampling policy and holdout

**Stratified alias-OOD (frozen):** Train registry/catalog/IR built from train-only alias forms; test evaluates unseen alias forms within same family (header/body/auth) and held-out forms (3 per family, 9 total) and mixed composition (10) never seen during training (0/40 leak enforced). TFIDF, hierarchical/WebAPI theme centroids, and compiled locator ranking fit on **train only**.

**Holdout unit:** Task alias instance (header/body/auth family + mixed composition). Trajectory-grouped block bootstrap by family (4 groups) preserves dependency.

**Freshness holdout:** Fresh vs stale labels from watermark/version drift, evaluated on held-out stale stratum (10 stale +10 fresh) not used for TTL tuning.

**BrowserGym site holdout:** If live, sites from WebArena-Verified v2 / WebGym 300k manifests not overlapping fixture families; if synthetic fallback, site diversity simulated via AX hash perturbation but disclosed.

No pipeline tuned on test alias forms/mixed/stale/freshness drifts.

---

## 7. Baselines (strong, discriminating)

| ID | Description | Role |
|---|---|---|
| `B-COMPILED` | Compiled bypass: DSM TreeWalker 99% compression → stable locator ranking → deterministic JSON IR / universal-webmcp with lazy replanning (heal only null selectors) | Experimental (Director PIVOT) |
| `B-WEBAPI-CF-SINGLE` | **Genuine** WebAPI endpoint-catalog: regex + Jaccard≥0.6 endpoint component clustering, theme centroids, correct-family endpoint invocation (fixes prior `webapi_mine==hierarchical_retrieve` artifact) | Strong tool-catalog baseline |
| `B-HIER-CF-SINGLE` | Hierarchical xMemory episode→component→theme Jaccard≥0.6, TFIDF centroids, complementary selection, single-base CF | Decoupling-before-aggregation baseline |
| `B-FLAT-CF-SINGLE` | Flat TFIDF cosine top-5 (fit train only) + single-base CF rewrite | Flat RAG strong baseline (21/40 ceiling) |
| `B-EXACT-MATCH` | `SpiderKernel.resolve` exact intent equality L97, min_confidence 0.8 | Chance null (0/40) |
| `B-STAGEHAND` | Stagehand exact-selector + DOM-hash at 1280×720, deterministic cache | Replay/hash economics baseline |
| `B-COMPILED-NOREPLAN` | Compiled IR without lazy replanning (null → UNKNOWN) | Ablation: replanning contribution |
| `B-JOINT-NOFRESH` | Best RAG/WebAPI joint freshness-disabled (inherit even if stale) | Ablation: freshness TTL effect |

All baselines share correct-family gating, verify+freshness semantics, and frozen honest cost.

---

## 8. Controls (frozen IDs, reused downstream)

### Positive controls (must pass → else MEASUREMENT_INVALID)

- `PC-EXACT-MATCH` — exact 12: all pipelines correct ≥0.90 false ≤0.10
- `PC-COMPILED-IR-BUILT` — ≥3 workflow IRs, JSON schema valid, stable locators ranked, risk tiers present, cost logged $0.002–0.092, lazy replanning exercised, no `hidden_expected` leak, manifest hash audited
- `PC-WEBAPI-INDEX-BUILT` — ≥3 endpoint themes, ≥6 endpoint components, episode==registry size per family, no leak, index hash audited, Jaccard≥0.6 verified
- `PC-RETRIEVAL-HEALTH` — alias-OOD 40 all pipelines non-empty ≥90% under CF, hierarchical/WebAPI/compiled distinct coverage ≥ flat on ≥50% tasks
- `PC-HONEST-COST-SANITY` — frozen cost `= sum(kernel.resolve + _bind + verify + freshness_check) + browser_steps` (no jitter, no `f*6.0`), not ≈ n×3200 within 1%, std>0 within same novelty stratum, not `f*6.0` bijective, `|ρ_shuffled|<0.20` with permutation p≥0.20 (200 shuffles), jitter terms `914-921` absent (audit inspects code)
- `PC-VERBATIM-COLLAPSE` — verbatim bind pooled ≤0.05 for all single-base RAG (confirms CF required, adopt-any-key artifact absent)
- `PC-LIVE-AX-CONSISTENCY` — viewport 1280×720 locked, `Accessibility.getFullAXTree` same path for live & synthetic fallback, AX>10 validated, census 4×3 logged, claim bounded if synthetic

### Null controls (must pass → else MEASUREMENT_INVALID)

- `NC-NO-APPLICABLE` — no-applicable 12: UNKNOWN precision ≥0.90 false ≤0.10
- `NC-EMPTY` — empty registry/IR 6: 100% UNKNOWN
- `NC-ORACLE-LEAK` — `derived_context` contains only allowed keys, extraction parses only template/IR strings, confidence std>0.05, cross-family verified (header never solved by body-only, mixed requires all families)
- `NC-BIJECTIVE-COST` — `ρ(cost,novelty)` not >0.98 with zero residual, within same f stratum `|ρ(cost,task_length)|<0.20` and std>0 and cost≠n×3200 and permutation p≥0.20
- `NC-STALE-FALSE-ACCEPT` — stale 12 false≤0.10 precision≥0.85 gated, freshness-disabled ≥0.20 confirming gating
- `NC-STAGEHAND-ISOLATION` — Stagehand alias-OOD pooled ≤0.05
- `NC-COMPILED-NULL-SELECTOR` — compiled null-selector heals only that step, noreplan shows higher UNKNOWN not higher false_accept

---

## 9. Primary metrics and uncertainty

- **Pooled correct** 40: Wilson 95% CI, one-sided binomial vs chance 0.10 (p<0.05), McNemar paired vs B-EXACT-MATCH and vs best RAG 21/40
- **Coverage** mean recall@k under CF + **coverage gain** vs best RAG: block bootstrap 2000 trajectory-grouped by family (header/body/auth/mixed), CI lower>0.05 p<0.05
- **ECE** 5 bins + bootstrap CI 2000 (upper ≤0.18 for survival)
- **Honest cost** Spearman ρ vs novelty, within-stratum ρ, shuffled ρ 200 permutations, permutation p≥0.20, not bijective
- **Adequacy rule:** Minimum for confirmatory: pooled N≥32, mixed≥8, stale-fresh≥16, ≥4 families for grouped bootstrap. Power N=40 gives 80% to detect 0.50 vs 0.10 at α=0.05.

---

## 10. Decision rule (frozen, exhaustive)

> All thresholds on pooled 40 under correct-family unless noted as verbatim check. Wilson CI, binomial vs 0.10, McNemar paired, block bootstrap 2000 trajectory-grouped, Spearman economics, ECE 5 bins bootstrap.

**SURVIVES_CURRENT_TEST** iff all PCs/NCs pass **and** PATH-A (compiled) meets S1–S7:

- **S1** pooled B-COMPILED ≥20/40=0.50 Wilson lower>0.35 binomial p<0.05 vs 0.10 McNemar p<0.05 vs B-EXACT-MATCH and vs best RAG; orthogonal ≥0.50 mixed ≥4/10 held-out ≥4/9 diagnostic
- **S2** coverage ≥0.60 Wilson lower>0.45 with gain ≥0.10 over best RAG bootstrap lower>0.05 p<0.05
- **S3** false_accept ≤0.15 McNemar p<0.05 below B-JOINT-NOFRESH by ≥0.10
- **S4** UNKNOWN precision ≥0.85 pooled+no-applicable
- **S5** ECE ≤0.15 bootstrap upper ≤0.18
- **S6** PC-HONEST-COST-SANITY |ρ_shuffled|<0.20 perm p≥0.20 not bijective, std>0
- **S7** PC-COMPILED-IR-BUILT + PC-WEBAPI-INDEX-BUILT + PC-LIVE-AX-CONSISTENCY pass

Diagnostic alternative: if compiled fails but B-WEBAPI alone meets S1–S6, report WebAPI as surviving tool-catalog alternative (PATH-B).

**FALSIFIED-IN-SETTING** if controls pass but neither compiled nor WebAPI meets S1–S6 (pooled <0.40 or coverage <0.55 gain<0.05 NS, false>0.18 or ECE>0.18) AND hierarchical vs flat gain <0.05 NS replicating prior ceiling (21/40=0.525).

**MEASUREMENT_INVALID** otherwise: any PC/NC fail, verbatim>0.05, cost bijective or |ρ_shuffled|≥0.20 or p<0.20, viewport mismatch, IR/index leak, AX≤10, or permutation/bootstrap not computed (single shuffle seed 7 insufficient).

No prereg after outcome inspection may weaken thresholds; any changed analysis is exploratory and requires new prereg on untouched evidence.

---

## 11. Product consequences (frozen)

**If SURVIVES (PATH-A compiled):** Compiled bypass provides higher-leverage alias-OOD resolution than endpoint-catalog or retrieval diversity under correct-family gating on noisy AX where DOM-hash/template rewriting fails. Product pivots from continuous LLM browsing O(M×N) to compile-and-execute with lazy replanning O(1) amortized f=10 ($0.002–0.092 vs browsing): implement agentic compilation (TreeWalker 99% compression, stable locator ranking, deterministic JSON IR, policy risk, SPA shadow-DOM reconciliation) as Product Core candidate. Advance C-SEMANTIC-RESOLVE HYPOTHESIS→EXPERIMENTAL bounded to live noisy AX (or synthetic noisy fallback if disclosed) at 0.50/0.60 ceiling with calibration. If WebAPI alone survives while compiled falsified, promote endpoint-catalog instead.

**If FALSIFIED-IN-SETTING:** Neither compilation nor endpoint discovery nor retrieval diversity breaks 21/40=0.525 coverage 0.55 mixed 0/10 ceiling under correct-family gating and noisy AX and honest cost. Tool compilation and endpoint mining not higher-leverage than template rewriting for these families; mixed triple-channel remains unsolved without OpenAPI/HATEOAS, routing normalization, or alias catalogs. Do **not** promote compiled/WebAPI; park C-SEMANTIC-RESOLVE at 0.525 ceiling bounded synthetic/live noisy, keep flat/hierarchical or exact cache, force next pivot to Fetch/WebMCP OpenAPI or rewind memory / barrier physics per portfolio. Preserve 21/40 0.55 as bounded ceiling not artifact; disclose synthetic-to-real gap if live N=0.

---

## 12. Estimated cost & expected information gain

**Cost:** Low-medium. ~90 tasks/pipeline ×8 pipelines ≈720 kernel calls plus hierarchical/WebAPI indexing and compiled IR generation offline <2 min each (TFIDF/Jaccard, TreeWalker), BrowserGym CDP `Accessibility.getFullAXTree` at 1280×720 if live (~2 min install, 40 page loads <10 min) else synthetic perturbation <1 min same path disclosed, cost audit <1 min, embed <40s or TFIDF <2s. Wall-clock <45 min single runner, <20 min without live, <10 min TFIDF-only. Compiled: ≤4 compilation LLM calls + ≤10 replanning heals at $0.002–0.092 each (or deterministic mock for cost-controlled run). Reuses `tasks_expanded.json` sha `83b7c52d`.

**Information gain:** Very high per cost and decisive for product architecture. This is the Director-mandated **cognitive reset PIVOT** out of 10-deep C-SEMANTIC-RESOLVE synthetic tunnel where flat/hierarchical/(code-identical)WebAPI all tied 21/40 coverage 0.55 mixed 0/10 with 0.0 gain, and joint 31/40 was family-gated copying on observationally-saturated `derived_context` (=`expected_bound` verbatim) disclosed in handoff `do_not_assume` (webapi_mine==hierarchical, frozen cost jitter, ρ_shuffled violation, header 2/10 vs 4/10 discrepancy). Continuing retrieval tuning has near-zero marginal info (Scout 70% recent MEASUREMENT_INVALID, 45/12/10/7 streaks). Compiled bypass (Agentic Compilation 80–94% zero-shot O(1), universal-webmcp, dom-distiller 99% compression, FCPAgent 200µs/step hybrid verification) is the first genuinely orthogonal mechanism per Frontier charter (observe→distill→registry→resolve→execute→verify→repair/UNKNOWN). Genuine WebAPI (regex+Jaccard when actually implemented) vs hierarchical vs flat under correct-family gating is the discriminating tool-catalog contrast previously unmeasured. Either positive (compiled breaks ceiling with honest cost) or negative (all fail honestly) cleanly decides selector-replay vs tool-compilation architecture and unblocks residual-novelty economics (f=10 amortization), or parks both and forces the next orthogonal pivot — closing the local optimum identified by Director.

---

## 13. Validity threats and how they are disclosed

| Threat | Mitigation / disclosure |
|---|---|
| **Observational saturation** (mixed `derived_context` already contains `expected_bound` verbatim, e.g., `X-Api-Key==tok`) | Prior 31/40 joint was copying not inference (`do_not_assume`); this design retains same fixture for comparability but declares that mixed success measures family-gated copying breadth unless live AX heterogeneity breaks tautology. Report per-family verbatim audit and mixed diagnostic separately. |
| **Synthetic-to-real gap** (independent per-step RNG vs correlated Web state) | Bounded claim: live BrowserGym heterogeneous AX required; if synthetic fallback used, claim bounded to synthetic noisy DOM, not live. Prior 30+ synthetic SPA falsifications bounded. |
| **Honest cost gaming** (jitter, `f*6.0` bijective) | Frozen cost `sum counters + browser_steps` (no jitter, no `f*6.0`), audit inspects code 914–921-style terms, shuffled ρ 200 permutations, bijective checks, std>0 within stratum. Prior violation |ρ|=0.2297 explicitly rejected. |
| **Confidence miscalibration** (hardcoded 0.85*softmax+0.12+jitter, ECE std 0.198–0.277, empty bins) | ECE bootstrap CI required; `UNKNOWN` precision and false_accept thresholds gate calibration; confidence std>0.05 audited. |
| **Cross-family key adoption** (inflated prior 0.975 to true 0.525) | Correct-family gating enforced (family overlap alphabetically), cross-family verified via null control, Jaccard and component parsing audited. |
| **Stagehand/BrowserUse proxy fiction** | Simulated proxies disclosed; Stagehand isolation NC requires ≤0.05 pooled; do not claim token leverage from proxies. |
| **Bias from small N** | Wilson CI, binomial vs 0.10, McNemar paired, block bootstrap 2000 trajectory-grouped; permutation p on shuffled cost; adequate N rules. |

---

## 14. Artifacts (to be produced by EXECUTE, not in DESIGN)

- `raw_evidence.json` — per-task rows (expected vs bound, correct/false/UNKNOWN, verify/freshness, honest cost counters, browser_steps, compilation cost, AX nodes, viewport, CDP path flag)
- `derived_metrics.json` — pooled/per-family Wilson CI, binomial/McNemar, coverage bootstrap CI, ECE bootstrap CI, shuffled permutation distribution, amortization math
- `index_manifest.json` + `ir_manifest.json` — endpoint themes/components and compiled IR themes with hashes, no-leak attestation
- `provenance.json` — git run id, commits, dataset sha, BrowserGym/Playwright versions, census log, AX>10 validation, cost accounting code path

---

## 15. Inherited continuity (parent handoff distinctions preserved per AGENTS.md)

**Established (bounded, not assumed to transfer to live):** synthetic fixture integrity (sha `83b7c52d`, 40=30+10, leak 0/40), single-base ceiling 21/40=0.525 Wilson [0.375,0.671] coverage 0.55 gain 0.0 for flat/hier/(code-identical)WebAPI, joint 31/40=0.775 via family-gated copying (not endpoint mining), 0/40 Stagehand/BrowserUse proxies, BrowserGym fallback synthetic perturbation at 1280×720, MEA auditor rejection-only effect (21/40→21/40).

**Rejected (bounded synthetic):** hierarchical vs flat gain 0.0, single-base WebAPI lever (unimplemented), honest cost 20–23 vs 3200 bijective claim, coverage 0.55 as resolution proxy, binomial p 7.1e-08 misreported.

**Unknown (to be tested live):** whether genuine WebAPI or compiled bypass provides gain on heterogeneous live AX, whether joint 9/10 mixed persists without saturation, header 2/10 diagnosable, honest cost |ρ_shuffled|<0.20 passes, MEA fresh-context vs rule-based filter.

**Do_not_assume (explicit non-transfer):** Do not assume 31/40 indicates WebAPI mining leverage, 21/40 header/auth splits correct (audit found 2/10 vs 4/10 discrepancy), honest cost discriminative, joint mixed demonstrates inference, Stagehand speedup transfers, ECE calibrated, synthetic fallback generalizes, Jaccard valid.

Director disposition `SUPERSEDE` means Frog design does **not** re-test the same retrieval basin; it tests compiled vs catalog vs retrieval under honest measurement on live noisy AX — highest portfolio leverage per `director_mandate.comparative_reasoning`.

---

## 16. Freeze attestation

This file, together with `spec.json`, is frozen **before** any outcome-bearing execution of EXP-FRONTIER-35880092123. No `result.json`, `report.md`, or `provenance.json` was inspected to write this preregistration. The deterministic freezer will hash `request.json` + `spec.json` + `prereg.md` into `freeze.json` before EXECUTE. Any post-freeze change is exploratory and requires a new experiment id.

