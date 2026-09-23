# EXP-INTEL-35798952720 preregistration — intel PIVOT (Director PIVOT C-CROSSSITE, cognitive_reset true, SUPERSEDE)

**Lane:** intel  
**Experiment:** EXP-INTEL-35798952720  
**Director mandate:** PIVOT C-CROSSSITE — After replacing truncated [:20] element-pattern grammar with full-tree semantic/multi-anchor traversal (no truncation, capturing product-specific subtree) and recomputing relevant-subtree SHA256 after DOM mutation, and importing WebGym 300k-task async corpus as diverse site holdout replacement for exhaustive LFS 567MB search (sample >=50 diverse sites to measure duplication/parameterization prevalence vs hardcoded 0.9479), plus collecting multi-step Playwright/BrowserGym trajectories >=50 transitions on >=10 families at 1280x720 with cold vs cached latency/tokens, does N=20 product-page AX_consistency achieve >=0.6 (bootstrap CI lower>0.5 shuffle p<0.05) vs prior degenerate 1.0 CI[1,1], and does Stagehand selector+relevant-subtree SHA256 achieve HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4, enabling bounded within-store parameterized transfer and Gate0 H>0.1 NL>=20 census without exhaustive enumeration?  
**Agent priors used (prior not SPIDER evidence, per request.json):** Synthetic alias grammars induce local optima memorizing truncated [:20] generic tokens inflates 40/40 synthetic while failing mixed heterogeneity; parameterized slot syntax +${slot}+ per-task token penalty -15.8% amortizes only when sharing frequency exceeds threshold; long-horizon path-dependent branch backtracking dominates later-agent cost requiring residual-novelty separation at f=100; measurement traps degenerate bootstrap CI[1,1] variance 0 p=1, singleton SA pairs, SHA256-truncated DOM make PMI/CMI 0 or tautologically 1, deterministic FSMs with independent per-step noise bake in null — replaced by session-correlated regimes and trajectory-grouped permutation.  
**Parent handoff:** research/experiments/EXP-INTEL-35789942386/handoff.json sha d67078871aba1d30f80101eed04dc401e90b9629e73db8aab17ccf3acef38be1 — SUPERSEDE disposition per Director: use continuity evidence verbatim for established/rejected/unknown/do_not_assume distinctions, but strategic question is binding Director question above (not inherited next_question alone).  
**Frozen before outcome:** DESIGN ONLY — no outcome-bearing measurements inspected; spec/prereg freeze before execution per AGENTS.md and research/EXPERIMENT_PACKET.md.  
**Seed:** 35725763380 (all sampling, shuffles, bootstraps deterministic; trajectory-grouped)  
**Substrate:** (A) Live: WebArena-Verified v2 shopping Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770, BrowserGym-core 0.14.3 + AgentLab 0.4.2 primary (0.3.0 fallback) + Playwright 1.63.0 primary (1.44.0 fallback) at 1280x720, CDP Accessibility.getFullAXTree. (B) Offline: WebGym 300k-task async corpus (AsyncWebRL 4-5x speedup source) for diverse site holdout. No CAP 420-task/108-site or Mind2Web LFS 567MB test.zip exhaustive search (ABANDONED per Director SUPERSEDE).

---

## 1. Question and inherited state

**Director question (frozen, binding per request.json director_mandate.question):** After replacing truncated [:20] element-pattern grammar with full-tree semantic/multi-anchor traversal (no truncation, capturing product-specific subtree) and recomputing relevant-subtree SHA256 after DOM mutation, and importing WebGym 300k-task async corpus as diverse site holdout replacement for exhaustive LFS 567MB search (sample >=50 diverse sites to measure duplication/parameterization prevalence vs hardcoded 0.9479), plus collecting multi-step Playwright/BrowserGym trajectories >=50 transitions on >=10 families at 1280x720 with cold vs cached latency/tokens, does N=20 product-page AX_consistency achieve >=0.6 (bootstrap CI lower>0.5 shuffle p<0.05) vs prior degenerate 1.0 CI[1,1], and does Stagehand selector+relevant-subtree SHA256 achieve HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4, enabling bounded within-store parameterized transfer and Gate0 H>0.1 NL>=20 census without exhaustive enumeration?

**Design refinement (smallest high-information falsifiable conversion):** Same question converted to executable gates: (a) Replace extract_element_pattern [:20] truncation with full-tree semantic/multi-anchor traversal capturing product-specific subtree and recompute SHA256 of relevant subtree outerHTML AFTER DOM mutation via page.content() — re-capture 20 AX trees on task-specific product/category/cart pages (not homepage), compute full-tree longest-prefix without fallback mean 95% CI and trajectory-grouped shuffle null with variance>0 check and delta vs truncated baseline; (b) Re-derive Stagehand key from AX node+DOM normalized selector and relevant-subtree SHA256 recomputed after mutation (not synthetic fam_task + full-page hash), execute drift MISS and random null with real-path latency/tokens via tiktoken; (c) Import WebGym 300k corpus and sample >=50 diverse sites to compute duplication prevalence 95%CI and threshold sweep 0.818-0.9479 vs hardcoded 0.9479; (d) Collect multi-step BrowserGym/Playwright trajectories (>=50 transitions per family, >=10 families) for relaxed Gate0 (H>0.1 NL>=20) vs strict. No exhaustive 420-task/567MB LFS or CAP exhaustive search (ABANDONED).

**Priority claim:** C-CROSSSITE (target per mandate, primary). Registry status HYPOTHESIS on live substrate. Downstream affected: C-LLM-INHERIT and C-PRODUCT-ECON (shipped Stagehand baseline economics) and C-RESIDUAL-NOVELTY (per-hit vs amortized at f=100) — reported but not primary claim_id.

**Inherited established (carry forward verbatim from handoff carry_forward.established, not re-measured as SURVIVES this cycle):**
- Placeholder fix get_task_start_url __SHOPPING__/path -> http://localhost:7770/path verified working in research/intel/exp_35789942386_measure.py sha 839aaa5306f9f2374298fff3d29362c3a9bba9b95c9d766b5679356610bade61 : 4 path families (136,145,196,222) load 8 distinct product pages with node counts 626-1150 distinct AX tree/DOM hashes, titles distinct, within 600-2000 window at 1280x720 — provenance.json placeholder_fix verified 4
- Substrate stack LIVE at 1280x720: Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 reachable after 1 retry at http://localhost:7770, BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.44.0 (spec 1.63.0 fallback documented, pip freeze hash) CDP Accessibility.getFullAXTree functional with 20/20 valid captures 600-2000 nodes DOM bytes>>2000 — artifacts/raw/ax_captures.jsonl sha 324313f6e5cb6986, provenance.json
- WebArena-Verified v2 shopping census replicated: 192 tasks, 49 intent_templates, 36 families >=3 (34 >=4, 33 >=5), duplication 0.9479 95%CI[0.9167,0.9792] exact-copy 0.0781 param_task 0.8958 — carry-forward from parent EXP-INTEL-35782546046 artifacts/raw/webarena_census.json sha1923e6fa
- Sampling seed 35725763380 deterministic for family sampling/bootstrap2000/shuffle1000; Docker digest, provenance hashes, viewport, CDP method recorded — provenance.json sha 3d4124dbde714a0d
- Prior single-family AX_consistency 0.9 CI[0.7,1.0] longest-prefix without fallback remains prior positive control (EXP-INTEL-35749371101) but not discriminable from degenerate 1.0 on product pages with truncated grammar — audit V1, baseline_findings PC2 FAIL_VARIANCE_ZERO
- Gate0 precedence and exhaustive-search ABANDONED per Director SUPERSEDE: no CAP 420-task/108-site or Mind2Web LFS 567MB test.zip or WebJudge-7B required; CAP outside ServiceNow/cap exhaustive 0/3 strict remains MEASUREMENT_INVALID not falsification — spec measurement_validity #6

**Inherited rejected (bounded, must not assume — from handoff carry_forward.rejected):**
- Bounded rejection: truncated element-pattern grammar (first 20 tokens generic/tablist/listitem/link:Skip to Content) yielding AX_consistency 1.0 CI[1.0,1.0] variance 0 shuffle p=1.0 on 10 families (6 homepage tautology +4 product but truncated) is NOT discriminating evidence for identifiable same-mechanism parameterized transfer via longest-prefix; reflects layout identity not transfer — does NOT reject longest-prefix with full-tree semantic/subtree/multi-anchor grammar on task-specific product pages (unmeasured)
- Bounded rejection: product URL scarcity as currently measured — only 4/36 shopping families contain __SHOPPING__/path product URLs (136,145,196,222) so 6/10 sample forced homepage-only fails adequate-run >=10 diverse families; N=20 product-page diverse test not achieved — does NOT reject existence of product diversity in shopping_admin 184 tasks 42 families or alternative start_url extraction
- Bounded rejection: Stagehand replication with synthetic fam_task fallback selectors + full-page hash + dict-lookup microsecond latency (0.0954x inverted) + hardcoded 1000 tokens + drift injection not recomputed after mutation (drift_miss 0.0 false_accept 1.0) is NOT spec-compliant replication of shipped Stagehand Feb2026 exact selector+relevant-subtree SHA256 HIT after N=2 per-project 2x/~30% baseline — does NOT show Stagehand generalizes or fails on shopping product pages
- Bounded rejection: relaxed Gate0 0/20 and strict 0/20 on 20 single-page viewport-only captures (transitions 0 NL0 strata1 singleton1.0 H undefined) is descriptive viewport-only census, not evidence for/against relaxed Gate0 H>0.1 NL>=20 feasibility on multi-step trajectories
- Prior closed path remains: 6-model density extrapolation to full-DOM n=50/82 as L=0.5654 logistic (4 points/3 params, k=10.75 saturates, Hill h=20 at bound) is informationally vacuous and definitively CLOSED — Docker direct full-DOM measurement only remaining path (EXP-INTEL-35551517470 audit VF2-VF4)
- Prior coarse 33-mechanism overlap 0.8139 and model-extrapolation L=0.5654 as TF-IDF proxy for C-CROSSSITE is REJECTED as vacuous vs null 0.998; single-store v2 overlap vacuous by construction not cross-site evidence

**Unknowns this experiment narrows (from handoff unknown 1-6 plus WebGym):**
- Whether replacing truncated [:20] pattern with full AX tree or product-relevant semantic subtree traversal (semantic, multi-anchor) yields discriminating AX_consistency variance>0 bootstrap CI lower>0.5 shuffle p<0.05 delta>=0.2 vs prior 0.2857 on same 4 product families, and discriminates vs prior 0.9 single-family inflated
- Whether expanding product URL source beyond 4/36 families (shopping_admin 184 tasks 42 families or alternative extraction) can achieve >=10 families with diverse product pages per decision_rule, versus persistent substrate ceiling responsible for MEASUREMENT_INVALID precedence
- Whether fixing Stagehand to recompute SHA256 of relevant subtree outerHTML AFTER DOM mutation, using exclusively derived normalized selector (no fam_task fallback), and measuring cold vs cached latency via real dispatch path (Playwright navigation + hash compute + cache lookup) with tiktoken/provider token counts achieves MISS>=0.8 false_accept<0.05 beats NC4 random p<0.05 and recovers real ~2x/~30%
- Whether multi-step BrowserGym trajectories (>=50 transitions on >=10 families) or Playwright-based rollout can be made importable to compute H(S_next|URL,H_K=3) with >=5/stratum, NL, strata, leakage_validOnly, singleton and yields >=1 relaxed Gate0 pass H>0.1 NL>=20 titles>=1 to unblock physics correlated-state H>0.1 pilot, and whether strict H>0.2 NL>=50 ever passes on shopping
- Whether WebGym 50 diverse-site sample yields duplication prevalence distinct from hardcoded 0.9479 and shows threshold sensitivity 0.818-0.9479, and whether corpus-level deduplication must be measured separately from per-hit cost
- Whether Playwright 1.63.0 vs required 1.44.0 fallback and AgentLab 0.4.2 vs 0.3.2 affect CDP node counts/AX fidelity and outcome directionally

**Do-not-assume guards (from handoff do_not_assume, binding):**
- Do not assume AX_consistency 1.0 CI[1.0,1.0] p=1.0 on 10 families implies parameterized same-mechanism transfer works on product pages — reflects truncated [:20] generic layout identity, zero variance, shuffle degenerate tautology (audit V1/V2 critical)
- Do not assume delta 0.7143 vs prior 0.2857 fallback is scientifically meaningful — prior used fallback, current truncated longest-prefix on insufficient diverse pages; comparison on same page type and full-tree grammar required
- Do not assume Stagehand hit_rate 0.9485 on identical DOM implies shipped 2x/~30% transfers — inflated by identical homepage DOMs and synthetic fallback selectors, drift MISS 0.0 false_accept recomputed 1.0 not 0.0, speedup inverted, tokens hardcoded (audit V3)
- Do not assume false_accept 0.0 is safe — no drift MISS measured until SHA256 recomputed after mutation per NC3 (<0.05) and NC4 random null p<0.05 beaten
- Do not assume relaxed Gate0 0/20 on single-page captures implies pilot infeasible — requires multi-step trajectories with H>=5/stratum and NL>=20; single-page H undefined is unmeasured not falsification (audit V4)
- Do not assume exhaustive CAP 420-task 108-site or Mind2Web LFS 567MB exhaustive search is required — Director SUPERSEDE ABANDONED per prior 0/3 exhaustive MEASUREMENT_INVALID; next allocation is narrow repair pilot plus WebGym diverse import not exhaustive enumeration
- Do not assume Playwright 1.63.0 compatible with BrowserGym-core 0.14.3 — provenance shows 1.44.0 fallback required; document pip freeze hash
- Do not assume cross-project isolation 0/5 or PC3 3-consecutive HIT generalizes to 36 families without per-family verification
- Do not assume within-store shopping AX generalizes to cross-site C-CROSSSITE — single Magento store only; cross-site needs multi-store dataset (Mind2Web/WebArena cross-template or WebGym diverse sites)
- Do not re-use truncated-first-20 constant null F(n)=0.5654 as plateau predictor — REJECTED vacuous extrapolation
- Do not assume hardcoded duplication 0.9479 transfers to WebGym diverse 300k corpus — must be measured with threshold sweep 0.818-0.9479 and reported with CI
- Do not assume SHA256 recomputed from unmutated page.content() is valid — must recompute AFTER single-attribute DOM mutation per NC3

---

## 2. Hypotheses

**H1_AX_FULLTREE (confirmatory, primary):** Full-tree semantic/multi-anchor traversal without truncation (traversing complete AX tree from root, extracting product-specific subtree anchored on heading/price/add-to-cart/main, tokenizing complete selector path) yields mean AX_consistency across 10 families (2 tasks each, longest-prefix without fallback, task-specific product pages at 1280x720) >=0.6 with bootstrap 95% CI lower >0.5, permutation p<0.05 vs NC1 trajectory-grouped shuffle null, delta vs prior invalid 0.2857 >=0.20, delta vs truncated [:20] same pages >=0.10, and per-family variance >0 (not degenerate [1.0,1.0]), demonstrating identifiable same-mechanism parameterized transfer capturing product-specific subtree. Discrimination vs prior inflated 0.9: report CI overlap and variance.

**H2_STAGEHAND_RECOMPUTED (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (exact normalized selector + relevant subtree outerHTML SHA256 recomputed AFTER mutation, HIT after N=2 identical results, per-project scope) replicated on >=30/36 families (drift test >=20) reports HIT on identical DOM >=0.8, MISS on single-attribute drifted DOM >=0.8, false_accept <0.05, beats NC4 random HIT/MISS null p<0.05, and reports measured cold vs cached latency/tokens via real dispatch path (not synthetic microsecond) delivering ~2x/~30% bound vs B-RAG-EMBED-FLAT / B-SPIDER-0TOKEN / B-COLD-LLM.

**H3_WEBGYM_DIVERSITY (confirmatory census):** WebGym 300k-task async corpus diverse sample (>=50 sites distinct eTLD+1/hosts) yields duplication/parameterization prevalence 95%CI distinct from hardcoded shopping 0.9479 [0.9167,0.9792] (non-overlapping or variation >=0.05 across threshold sweep 0.818-0.9479), showing diversity in training distribution matters more than hierarchical depth and that full-tree grammar with diverse sites is required before any Graph within-store claim can be bounded.

**H4_GATE0_MULTI (descriptive, unblocking):** On same 10 families with multi-step BrowserGym/Playwright trajectories (>=50 transitions per family, at least 10 families), relaxed Gate0 pass count (titles>=1, H>0.1, NL>=20, singleton<50%) and strict Gate0 pass count (titles>=2, H>0.2, NL>=50, strata>=10, leakage_validOnly<40%) reported with bootstrap CIs; >=1 relaxed pass suggests next physics can run correlated-state H>0.1 pilot without exhaustive search. Single-page NL=0 is unmeasured, not falsification.

---

## 3. State, action, target, observable

**State representation:** Raw CDP Accessibility.getFullAXTree nodes (role, name, value, properties) plus DOM outerHTML relevant-subtree SHA256 (normalized, full subtree not truncated) for Stagehand key. Title = document.title string; URL = normalized page URL (lowercase, strip query/fragment for leakage). For Gate0, state for H computed as (URL, H_K=3 history) with >=5 per stratum. No PCA/TF-IDF embedding for AX_consistency; full-tree semantic traversal operates on complete tokenized selector path from full AX tree.

**Action representation:** Element-pattern: normalized selector pattern derived from full AX tree + DOM attributes for product-specific subtree target (role+name+CSS path tokenized over complete tree, no truncation). Multi-anchor: heading/price/add-to-cart/main anchors define subtree boundary. Longest-prefix: longest common prefix of tokenized pattern (>0 tokens) across family tasks, no fallback.

**Target/observable:** Primary metric M-AX-CONSISTENCY = mean per-family indicator (1 if both tasks in family map to same full-tree longest-prefix pattern, else 0) across 10 families, range [0,1], per-family variance reported. Secondary: M-STAGEHAND-HITRATE, M-STAGEHAND-MISSRATE, M-STAGEHAND-FALSE-ACCEPT (recomputed after mutation), M-STAGEHAND-SPEEDUP, M-STAGEHAND-TOKENS-SAVED. Census: M-WEBGYM-DUP-PREVALENCE, M-WEBGYM-THRESHOLD-SWEEP, M-GATE0-RELAXED-PASS count/rate and M-GATE0-STRICT-PASS count/rate.

**Unit of analysis:** Family for H1/H4 (n=10 families, 20 tasks, family-level bootstrap), per-family task for Stagehand (n=36 families, up to 72 tasks plus drift variants), site for WebGym (n>=50 diverse sites).

---

## 4. Sampling policy

- **Family sampling (live):** From 36 WebArena-Verified v2 shopping families with >=3 tasks (census 36 ge3), sample 10 families without replacement using seed 35725763380 (Python random, deterministic). Record ordered list. Prior list [136,208,211,172,191,139,138,222,101,194] expected but recompute deterministically.
- **Task sampling (live):** Within each of 10 families, sample 2 distinct tasks without replacement (seed 35725763380) prioritizing distinct start_url categories (category, product detail, cart). Task IDs and expanded start_urls pinned in ax_captures.jsonl. Fixed placeholder expansion required for families with __SHOPPING__/path.
- **Full-tree vs truncated comparison:** Compute AX_consistency both with truncated [:20] grammar (for delta) and full-tree grammar on same 20 captures to measure truncation effect (delta >=0.10 required).
- **Stagehand replication:** Attempt all 36 families (>=30 required for H2 validity, >=20 for drift recomputed), sampling 2 tasks per family where possible; seed 35725763380; report blocked families.
- **WebGym diverse sampling:** Import WebGym 300k corpus, enumerate distinct sites/hosts, sample >=50 diverse sites (distinct eTLD+1, stratified by template) without replacement seed 35725763380; compute duplication prevalence per site and pooled with 95% CI and threshold sweep 0.818-0.9479 corpus-level deduplication.
- **Multi-step Gate0 rollouts:** For each of 10 families, attempt BrowserGym rollout or Playwright rollout collecting >=50 transitions per family; at least 10 families with multi-step required for census validity, else flag.
- **No CAP/Online-Mind2Web/Mind2Web LFS exhaustive sampling this cycle** — explicitly ABANDONED per Director SUPERSEDE.

---

## 5. Holdout and contamination controls

- AX_consistency has no train/test split — within-family consistency of full-tree longest-prefix, no fitting on held-out families. Truncated vs full-tree comparison done on same captures to isolate grammar effect.
- WebGym census is offline holdout diversity measurement; no site identity leakage into AX live branch; WebGym sample computed independently with deterministic seed.
- Stagehand cache: keys fitted on first occurrence per (project_id, normalized_selector, relevant-subtree hash recomputed after mutation) and tested on second occurrence within same family (intra-family HIT) and cross-project isolation test; no cross-family key reuse that would inflate hit_rate. Drift injection is single-attribute mutation on relevant subtree with hash recomputed AFTER mutation.
- Trajectory-grouped permutation for all shuffle nulls (grouped by family/trajectory, not step) to avoid independent per-step noise baking in null; session-correlated latent regimes where applicable.
- All 20 AX captures at 1280x720 initial viewport no scroll; below-fold or post-interaction AX after scroll/add-to-cart only via multi-step trajectory branch (which records post-interaction transitions for Gate0).
- BrowserGym/AgentLab/Playwright versions pinned and recorded; no post-hoc pin change after seeing AX scores. Full-tree grammar code hash and placeholder fix verified by code hash before capture.

---

## 6. Nulls, baselines, and controls (stable IDs for EXECUTE/AUDIT)

**Baselines:**
- B-STAGEHAND-VERB (shipped Feb 2026 exact selector+relevant-subtree SHA256 2x/~30%, per-project) — H2 must match with recomputed drift test
- B-RAG-EMBED-FLAT (flat retrieval without DOM-hash guard)
- B-SPIDER-0TOKEN (verbatim 0-token replay)
- B-RANDOM-AX-SHUFFLE (1000 perms family-label shuffle, trajectory-grouped)
- B-CONSTANT-NULL-05654 (REJECTED vacuous 0.5654) — disclosed only to prevent reuse
- B-COLD-LLM (cold agent from scratch, descriptive upper bound for honest economics at f=10 and f=100)
- B-WEBGYM-HARDCODED-09479 (hardcoded 0.9479 [0.9167,0.9792] single-store duplication null)
- B-WEBGYM-TFIDF (Mind2Web TF-IDF website-holdout with synthetic shuffles)

**Positive controls:**
- PC1_AX_LIVENESS_1280: >=15/20 AX trees 600-2000 nodes, DOM bytes >=2000, Docker reachable after 3 retries at http://localhost:7770
- PC2_AX_PRIOR_REPLICATION: >=1 family replicates prior 0.9 CI[0.7,1.0] longest-prefix but now on diverse product pages with full-tree variance>0
- PC3_STAGEHAND_HIT_IDENTICAL_RECOMPUTED: On stable family with 3 consecutive identical relevant-subtree hash (recomputed after mutation)+normalized selector, HIT on 2nd/3rd call with per-project isolation
- PC4_WEBGYM_IMPORT_VALID: WebGym corpus loads >=50 diverse sites, manifest hash recorded, threshold sweep computable
- PC5_SYNTHETIC_PIPELINE: Synthetic validation retained but is_synthetic true, not decision input

**Null controls:**
- NC1_AX_SHUFFLE_NULL: 1000 family-label perms seed35725763380 trajectory-grouped, true must exceed p95+0.30 with p<0.05
- NC2_AX_RANDOM_PATTERN: Random full-tree pattern from different family expected <0.2
- NC3_STAGEHAND_DOM_DRIFT_RECOMPUTED: Single-attribute DOM mutation on relevant subtree expecting MISS with SHA recomputed AFTER mutation; false_accept <0.05 and MISS>=0.8
- NC4_STAGEHAND_RANDOM_CACHE: Random HIT/MISS shuffling ~50% hit_rate ~1.0 speedup; true must beat p<0.05 (1000 perms)
- NC5_CROSS_PROJECT_LEAKAGE: Same key different project must MISS, cross-project HIT 0%
- NC6_WEBGYM_DUP_SHUFFLE: Site-label shuffle null for WebGym duplication prevalence, 1000 perms trajectory-grouped, true must beat p<0.05 and show threshold sensitivity >0.05

---

## 7. Primary metric and expected direction

**Primary confirmatory metric (live):** M-AX-CONSISTENCY (mean [0,1] full-tree) with bootstrap 95% CI and NC1 shuffle null, plus per-family variance and delta vs 0.2857 and vs truncated [:20] baseline.

**Expected direction under H1:** True >=0.6, CI lower >0.5, permutation p<0.05 trajectory-grouped, delta >=0.20 above prior invalid 0.2857, delta vs truncated >=0.10, variance>0 (not tautological), and discriminable vs single-family inflated 0.9 (CI width >0). If H1 holds, this is first measurement-valid within-store parameterized transfer on product pages capturing product-specific subtree (vs generic layout).

**H2 primary:** M-STAGEHAND-HITRATE >=0.8 on identical (recomputed), M-STAGEHAND-MISSRATE >=0.8 on drift recomputed, M-STAGEHAND-FALSE-ACCEPT <0.05, speedup and tokens_saved reported via real path, beats NC4 p<0.05.

**H3 primary:** M-WEBGYM-DUP-PREVALENCE 95%CI distinct from 0.9479 CI and threshold sweep range >=0.05 indicating diversity matters more than depth.

No threshold changed after seeing outcomes. Full-tree semantic/multi-anchor without truncation only; placeholder expansion verified; SHA recomputed after mutation verified.

---

## 8. Uncertainty method and resampling unit

- Bootstrap 2000 percentile 95% CIs for M-AX-CONSISTENCY (resampling families, not tasks, to respect family-grouped dependency) and for Stagehand hit/miss rates (resampling families) and WebGym duplication prevalence (resampling sites; threshold sweep per threshold). Report lower, mean, upper.
- Permutation 1000 for NC1 shuffle null (permute family labels across 10 families, preserve per-family 2 tasks, trajectory-grouped), seed 35725763380; report mean/std/p95 and permutation p = (1 + count perm >= true)/(1+1000). Same seed for NC4 random cache null (1000 perms shuffling HIT/MISS labels) and NC6 WebGym shuffle (permute site labels across sampled sites, grouped by site). Trajectory-grouped permutation required to avoid degenerate bootstrap CI[1,1] variance 0 p=1 trap.
- All seeds deterministic; Python hash randomization not used. Resampling unit = family for AX, family/task for Stagehand, site for WebGym. Family-level bootstrap for AX avoids task-level independence violation. Singleton SA pairs excluded requiring >=5 per stratum for H/NL strata.

---

## 9. Adequacy and validity rules

**Adequate H1 run:** >=10 families (20 trees) with node counts 600-2000, viewport 1280x720, CDP hash recorded, full-tree semantic/multi-anchor without truncation verified by code hash, placeholder correctly expanded for __SHOPPING__/path families, per-family URL/title confirms product-page diversity, truncated vs full-tree delta computed; else MEASUREMENT_INVALID insufficient data (not FALSIFIED).

**Adequate H2 run:** >=30/36 families attempted with derived selector+relevant-subtree SHA256 cache logic recomputed after mutation (N=2, per-project), with >=20 families for drift injection recomputed and >=5 for cross-project isolation; else MEASUREMENT_INVALID. Dict-lookup microsecond or unmutated SHA not adequate.

**Adequate H3 run:** WebGym corpus imported with >=50 diverse sites sampled, manifest hash recorded, duplication prevalence 95%CI and threshold sweep 0.818-0.9479 computed; else MEASUREMENT_INVALID for WebGym branch (<30 sites).

**Adequate Gate0 census:** Multi-step trajectory with >=50 transitions per family for H/NL/strata; raw transitions per capture recorded even if <50, but H undefined if <5 per stratum flagged and excluded from H gate but still reported. Single-page capture alone cannot compute H/NL/strata => flag as descriptive viewport-only with unmeasured and do not use to claim relaxed infeasible.

**Representation loss disclosed:** Full-tree vs longest-prefix only comparison disclosed, initial viewport no scroll for AX plus multi-step for Gate0, CDP AX vs full DOM, DOM-hash relevant-subtree outerHTML choice (normalized), N=2 HIT threshold, Playwright version deviation if 1.44.0 fallback, WebGym sample size 50 vs 300k full.

---

## 10. Falsification / survival / invalidity rules (frozen, no post-hoc change)

```
IF Docker/CDP yields <5 families with task-specific product pages (<10 trees 600-2000 nodes) after 3 retries + full-tree grammar verification + placeholder fix verification:
  H1 = MEASUREMENT_INVALID substrate_unavailable (status COMPLETE outcome NOT_APPLICABLE)
  publish failure provenance, do not falsify, next pulse repair substrate
ELIF WebGym import yields <30 diverse sites after 2 attempts:
  H3 = MEASUREMENT_INVALID corpus_unavailable (does not invalidate H1/H2 live branch)
ELIF captured >=10 families (20 trees, placeholder expanded, full-tree semantic/multi-anchor verified):
  IF mean >=0.6 AND ci_lower >0.5 AND perm_p <0.05 trajectory-grouped AND delta_vs_0.2857 >=0.20 AND delta_vs_truncated >=0.10 AND PC1 >=15/20 AND variance>0 AND not degenerate [1.0,1.0] p=1.0:
    H1 = SURVIVES (full-tree parameterized transfer identifiable capturing product-specific subtree)
    discriminate vs prior 0.9: report CI overlap [0.7,1.0] and whether variance indicates inflated point estimate
  ELSE:
    H1 = FALSIFIED-IN-SETTING (bounded to WebArena v2 shopping full-tree on product pages, does NOT reject Stagehand or alternative grammars)
    // variance=0 or p=1.0 despite diverse product pages and full-tree => FALSIFIED, not SURVIVES

IF Stagehand attempted <30/36 families due to Docker unavailability OR SHA not recomputed after mutation:
  H2 = MEASUREMENT_INVALID
ELIF attempted >=30 with derived selector+relevant-subtree SHA256 recomputed after mutation:
  IF hit_on_identical >=0.8 AND miss_on_drift_recomputed >=0.8 AND false_accept <0.05 AND speedup/tokens reported via real path AND beats NC4 p<0.05 AND PC3 isolation 0.0 AND selector derived from AX+DOM (not synthetic fam_task) AND relevant-subtree SHA256 recomputed after mutation (not full-page, not pre-mutation):
    H2 = SURVIVES (Stagehand baseline replicable competitive floor delivered)
  ELSE:
    H2 = FALSIFIED-IN-SETTING (selector+hash not discriminating on this shopping substrate even with recomputed hash)

IF WebGym attempted >=50 diverse sites sampled:
  IF duplication prevalence 95%CI does NOT overlap hardcoded 0.9479 CI [0.9167,0.9792] AND threshold sweep range >=0.05 (0.818-0.9479):
    H3 = SURVIVES (diversity matters more than hierarchical depth)
  ELSE IF measured but CI overlaps and sweep range <0.05:
    H3 = FALSIFIED-IN-SETTING (single-store census not distinct on diverse sample)
  ELSE:
    H3 = MIXED (report CI and sweep, bounded)
ELSE IF sampled <30 sites:
  H3 = MEASUREMENT_INVALID

H4 census descriptive (does not gate SURVIVES):
  Report relaxed_pass = count with titles>=1 & H>0.1 & NL>=20 & singleton<50 (multi-step, >=5/stratum)
  and strict_pass = count with titles>=2 & H>0.2 & NL>=50 & strata>=10 & leakage_validOnly<40%
  with bootstrap CIs; >=1 relaxed pass on multi-step suggests next physics relaxed pilot feasible
  0/16 on single-page alone = unmeasured not falsification; degenerate bootstrap CI[1,1] variance 0 p=1 not valid

Overall SURVIVES if H1 SURVIVES and H2 at least SURVIVES or honest recomputed false_accept<0.05 and H3/H4 reporting valid;
H1 FALSIFIED alone suffices to reject full-tree AX method for product within-store claim.
No CAP/LFS exhaustive search changes verdict; exhaustive remains ABANDONED per Director SUPERSEDE.
Measurement traps (singleton SA, SHA-truncated DOM, independent per-step noise) flagged MEASUREMENT_INVALID not SURVIVES/FALSIFIED if violated.
```

All control/baseline/metrics IDs frozen for EXECUTE/AUDIT: B-STAGEHAND-VERB, B-RAG-EMBED-FLAT, B-SPIDER-0TOKEN, B-RANDOM-AX-SHUFFLE, B-CONSTANT-NULL-05654, B-COLD-LLM, B-WEBGYM-HARDCODED-09479, B-WEBGYM-TFIDF, PC1_AX_LIVENESS_1280, PC2_AX_PRIOR_REPLICATION, PC3_STAGEHAND_HIT_IDENTICAL_RECOMPUTED, PC4_WEBGYM_IMPORT_VALID, PC5_SYNTHETIC_PIPELINE, NC1_AX_SHUFFLE_NULL, NC2_AX_RANDOM_PATTERN, NC3_STAGEHAND_DOM_DRIFT_RECOMPUTED, NC4_STAGEHAND_RANDOM_CACHE, NC5_CROSS_PROJECT_LEAKAGE, NC6_WEBGYM_DUP_SHUFFLE, M-AX-CONSISTENCY, M-AX-CI-LOWER, M-AX-CI-UPPER, M-AX-SHUFFLE-P, M-AX-SHUFFLE-MEAN, M-AX-SHUFFLE-P95, M-AX-DELTA-VS-PRIOR, M-AX-DELTA-VS-TRUNCATED, M-STAGEHAND-HITRATE, M-STAGEHAND-MISSRATE, M-STAGEHAND-SPEEDUP, M-STAGEHAND-TOKENS-SAVED, M-STAGEHAND-FALSE-ACCEPT, M-STAGEHAND-CROSS-PROJECT-LEAKAGE, M-WEBGYM-DUP-PREVALENCE, M-WEBGYM-THRESHOLD-SWEEP, M-GATE0-RELAXED-PASS, M-GATE0-STRICT-PASS.

---

## 11. Product consequence

**Positive (H1 SURVIVES + H2 recomputed SURVIVES + H3/H4 valid):** Delivers measurement-valid within-store parameterized transfer (10 families product pages, correct pins, full-tree semantic/multi-anchor >=0.6 discriminating with recomputed SHA and variance>0) and shipped Stagehand baseline (hit>=0.8/miss>=0.8/false_accept<0.05 vs random, real latency/tokens, derived selector+subtree) plus WebGym 50 diverse-site census proving duplication sensitivity 0.818-0.9479 — product can decide whether SPIDER parameterized inheritance beyond exact cache is justified and physics can run relaxed H>0.1 NL>=20 pilot on same families without inventing 4-point logistic/Hill extrapolation or 567.7MB LFS. Artifacts become reusable substrate for next cross-site holdout and Mind2Web-2 upgrade (second step after this fix, not substitute). C-CROSSSITE remains single-store so cross-site still HYPOTHESIS, but within-store family hold-out (C-LLM-INHERIT) advances toward VALIDATED with honest per-hit vs amortized economics at f=100 separated and corpus deduplication threshold sensitivity measured.

**Negative (H1 FALSIFIED or H2 FALSIFIED or H3 FALSIFIED or MEASUREMENT_INVALID):** If H1 FALSIFIED, full-tree without truncation does not achieve identifiable transfer or no improvement vs truncated — product must try alternative pattern grammar (semantic/subtree/multi-anchor with parameterized slot +${slot}+ overhead -15.8% or hierarchical retrieval) or use RAG-EMBED/hierarchical retrieval, not assume within-store generalization; alias-grammar local optima explains synthetic 40/40 inflation. H2 FALSIFIED means Stagehand 2x/30% does not transfer to shopping families even with recomputed hash; product economics must use alternative baseline and C-PRODUCT-ECON stays HYPOTHESIS with threshold sensitivity vs per-hit cost disambiguated. H3 FALSIFIED means WebGym duplication overlaps 0.9479 — single-store census not distinct on diverse sample, still not cross-site holdout. If MEASUREMENT_INVALID (<5 families with product pages after fix + 3 retries OR <30 WebGym sites), no falsification, repair Docker/WebGym/pins and re-run orthogonal BrowserGym loopback or hierarchical retrieval, not exhaustive LFS/CAP. H2 MEASUREMENT_INVALID if SHA not recomputed after mutation retains false_accept 1.0 trap. H4 0 relaxed passes on multi-step keeps physics pilot blocked on shopping substrate. No exhaustive search re-triggered regardless.

---

## 12. Cost and information

**Cost:** LOW-MEDIUM, no LLM API calls for AX/Gate0/WebGym census (token estimation via tiktoken if needed), Docker (~1-2GB) + BrowserGym-core 0.14.3 + AgentLab 0.4.2/0.3.0 + Playwright 1.63.0 Chromium (~300MB), 20 AX captures on product pages (full-tree vs truncated delta) + Stagehand derived-key sweep recomputed (36 families) + WebGym 300k import + 50 diverse-site sample + duplication sweep (~30-45 min) + multi-step rollouts (10x50 transitions) ~3-4h wall-clock, <15GB /tmp, stdlib+playwright+browsergym/agentlab+tiktoken. Reuses prior census d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 for pin only.

**Information:** MAXIMUM per Director PIVOT comparative reasoning with cognitive_reset — directly repairs last-mile truncation and single-store duplication root causes plus SHA-recomputation trap that caused degenerate 1.0 p=1.0 and false_accept 1.0, with deterministic low-cost fix delivering discriminating full-tree test, spec-compliant baseline that determines SPIDER vs Stagehand economics with per-hit cost separated from fixed amortisation at f=100 and threshold sensitivity measured, and WebGym diverse site holdout replacing exhaustive 567.7MB LFS/CAP exhaustive search that yielded 0/16. Either SURVIVES unlocks product within-store holdout and WebGym cross-site baseline and physics pilot, or FALSIFIED-IN-SETTING redirects to alternative representations and archives truncated-grammar local optima vs hierarchical retrieval, both decision-changing vs repeating stale exhaustive plan or synthetic FSM TV variants. Beats synthetic bandwidth tuning after 44-deep frontier tunnel and vacuous F=0.5654 extrapolation (closed).

---

## 13. Execution plan (frozen, no outcome inspection)

1. Pin and verify: pip install browsergym-core==0.14.3 agentlab==0.4.2 (fallback 0.3.0) playwright==1.63.0, playwright install --with-deps + chromium, record pip freeze sha256, verify CDP Accessibility.getFullAXTree, record versions.
2. Fix research/intel/exp_35789942386_measure.py:get_task_start_url to expand `__SHOPPING__/path` -> `http://localhost:7770/path` (base+path), verify via code hash and unit test on families 136/222 product paths, record hash.
3. Implement full-tree semantic/multi-anchor grammar: replace [:20] truncation with full AX tree traversal from root, multi-anchor product subtree extraction (heading/price/add-to-cart/main), verify full-tree hash distinct from generic truncated hash, record code hash.
4. Bring up Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770, record digest, sample 10 families from 36 (>=3) seed35725763380, 2 tasks per family with task-specific expanded start_url.
5. Capture 20 AX trees via CDP at 1280x720 initial no scroll (600-2000 nodes), compute AX_consistency both truncated [:20] and full-tree longest-prefix without fallback (tokenized), bootstrap 2000 family-level, shuffle 1000 trajectory-grouped perms, report delta vs 0.2857 and vs 0.9 and truncated-vs-full-tree with per-family variance and per-family URL/title/node_count/subtree hash.
6. Replicate Stagehand selector+relevant-subtree SHA256 (N=2, per-project) on 36 families with derived normalized selector and relevant subtree outerHTML hash recomputed AFTER DOM drift via page.content(), inject single-attribute DOM drift on >=20 families, test cross-project isolation on >=5, report hit/miss/false_accept recomputed vs NC4 random null (1000 trajectory-grouped perms) and measured cold vs cached latency/tokens via real path vs B-RAG-EMBED-FLAT/B-SPIDER-0TOKEN.
7. Import WebGym 300k corpus: download/verify manifest (URL+sha256), parse task JSON, sample >=50 diverse sites (distinct eTLD+1 stratified) seed35725763380, compute duplication prevalence pooled and per-site with 95% bootstrap CI, threshold sweep 0.818-0.9479 corpus-level deduplication sensitivity, trajectory-grouped site-label shuffle null, preserve webgym_census.json with sha256.
8. Collect multi-step BrowserGym/Playwright trajectories (>=50 transitions per family, 10 families) at 1280x720, compute relaxed vs strict Gate0 census (titles, H with >=5/stratum NL>=20, strata, leakage_validOnly, singleton) with bootstrap CIs and preserve raw artifacts with sha256 + provenance; disclose representation loss; perform trajectory-grouped permutation with session-correlated regimes; no CAP/LFS exhaustive search.
