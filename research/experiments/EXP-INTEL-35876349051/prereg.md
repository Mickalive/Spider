# EXP-INTEL-35876349051 preregistration — Intel PIVOT to C-CROSSSITE (SUPERSEDE)

**Lane:** intel — `research/intel` only (no cross-lane writes)  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout (registry HYPOTHESIS); auxiliary gates C-MEAS-VALID, C-WEB-DYNAMICS (Gate0), C-PRODUCT-ECON (Stagehand economics) reported descriptively but not promoted beyond C-CROSSSITE ceiling  
**Director mandate:** PIVOT, cognitive_reset true, parent_handoff_disposition SUPERSEDE (EXP-INTEL-35860344410 MEASUREMENT_INVALID); expires exhaustive 567MB LFS / 420-task CAP enumeration (0/3 strict MEASUREMENT_INVALID not falsification, degenerate 0.2857->1.0 CI[1,1] p=1.0 due to [:20] truncation). Target pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, full-tree semantic/multi-anchor without truncation plus dynamic-token stripping, WebGym 300k diverse holdout >=50 eTLD+1, multi-step >=50 transitions/family >=10 families. Dependencies: [runtime] (shared substrate + AX isolation, non-blocking).  
**Inherited state consumed:** Read `research/experiments/EXP-INTEL-35860344410/handoff.json` sha 5c5b4ddc189258e0f62bbccf576424047101aef164374c5d3f9730dbe6bc30e9; preserved established/rejected/unknown/do_not_assume verbatim in §10. This NEW governed experiment follows the Director's strategic question, not the parent handoff's `next_question` (which is advisory continuity only per AGENTS.md global direction discipline). No outcome-bearing measurement run during DESIGN. Verifies 12-streak C-CROSSSITE tunnel_flag and degenerate AX 1.0 p=1.0 blocking Physics Gate0.

---

## 1. Strategic question (Director binding) → falsifiable experiment

**Director question (binding, from request.json director_mandate.question):** Replace exhaustive 567MB LFS / 420-task enumeration with BrowserGym/WebGym diverse-site sampling: import WebGym 300k manifest, sample >=50 eTLD+1 diverse sites, measure duplication 0.9479 95% CI (2000 bootstrap) and threshold sweep 0.818-0.9479 plus parameterization prevalence 0.8958 without exhaustive LFS; deliver relaxed Gate0 census H>0.1 NL>=20 titles>=1 via BrowserGym 1280x720 multi-step trajectories >=50 transitions/family on >=10 families (WebArena shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) with cold vs cached latency/tokens; plus full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, no selectors[:20] placeholder, product-subtree/product-page SHA256 recomputed after page.content()+AX via page.evaluate with dynamic-token stripping) at 1280x720 with 20 live CDP captures task-specific start_url 10 families x2 seeds (35725763380) requiring mean>=0.6 bootstrap lower>0.5 shuffle p<0.05 delta>=0.2 vs truncated baseline; and Stagehand relevant-subtree HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 random-role-subset null with real-path latency/tokens, all trajectory-grouped bootstrap CIs.

**Smallest high-information translation (this prereg):** Narrow repaired pilot on WebArena-Verified v2 shopping product pages (10 families ×2 tasks =20 CDP captures at 1280x720 with dynamic-token stripping) + Stagehand recomputed replication on same 36 families (derived selectors only, SHA recomputed after mutation + stripping, real-path latency/tokens) + WebGym 300k 50-site diverse census (2000 bootstrap CI + threshold sweep) + 10-family multi-step rollout (strive 50 transitions each, BrowserGym-core 0.14.3 primary with Playwright fallback). Any narrower (single metric) would leave Stagehand competitive floor or WebGym diversity untested and risk another degenerate pass; any broader (exhaustive LFS/CAP) repeats blocked path with zero marginal information gain per Director comparative reasoning ("Vs continuing mandated shopping_admin 184-task/42-family expansion ... still exhaustive, high infra cost, and last 2 attempts already degenerate due to same truncation; marginal info gain low"). Already-frozen experiments resume independently; pre-freeze work is superseded per mandate.

---

## 2. Hypotheses (confirmatory)

- **H1_AX_FULLTREE (primary, confirmatory):** Full-tree semantic/multi-anchor without truncation (complete CDP Accessibility.getFullAXTree traversal from root, product-specific subtree anchored on heading/price/add-to-cart/main/contentinfo boundaries, role+name+CSS path + subtree outerHTML SHA256 normalized by stripping CSRF/timestamp/session IDs/tokens, no token truncation, longest-prefix without fallback) yields discriminating within-store AX_consistency on N=20 live product-page captures with mean≥0.6, bootstrap 2000 family-level 95% CI lower>0.5, trajectory-grouped permutation 1000 p<0.05 vs NC1 (>0.20 above null mean/p95), delta≥0.20 vs truncated [:20] baseline on same pages, per-family variance>0 (CI width>0, not degenerate [1.0,1.0] homepage tautology with p=1.0), product-subtree node counts>1 distinct hashes on path families.

- **H2_STAGEHAND_RECOMPUTED_DYNAMIC (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (exact normalized selector from AX node+DOM attributes + SHA256 of relevant subtree outerHTML recomputed AFTER mutation via page.content()+AX Accessibility.getFullAXTree via page.evaluate, HIT after N=2 identical results, per-project isolation, 0 synthetic fam_task fallback, dynamic-token stripping before hash) reports HIT≥0.8 on identical DOM, MISS≥0.8 on single-attribute drifted DOM (page.evaluate mutation, hash recomputed after), false_accept<0.05, beats NC4 random-role-subset null p<0.05, with cold vs cached latency/tokens via real Playwright dispatch path (navigation + hash + cache lookup, tiktoken/provider counts) delivering ~2× speedup and ~30% token saving on HIT when selectors exclusively derived.

- **H3_WEBGYM_DIVERSE (confirmatory):** WebGym 300k-task async corpus (>=50 diverse eTLD+1 hosts, stratified deterministic seed 35725763380, manifest sha256) yields duplication prevalence 95% CI (2000 family-level bootstrap) distinct from hardcoded WebArena-Verified v2 single-store duplication 0.9479 CI[0.9167,0.9792] (192 tasks 49 templates 36 families) and corpus-level deduplication threshold sweep range ≥0.05 across 0.818–0.9479, plus parameterization prevalence near 0.8958 computable without exhaustive 567MB LFS, proving distribution diversity matters more than hierarchical depth.

- **H4_GATE0_RELAXED (descriptive pilot, not confirmatory physics claim):** Multi-step trajectories ≥50 transitions/family on ≥10 families yield ≥1 family passing relaxed census (titles≥1 H(S_next|URL,H_K=3)>0.1 NL≥20 singleton<50%) enabling correlated-state physics pilot; strict Gate0 (H>0.2 NL≥50 strata≥10 leakage_validOnly<40%) reported descriptively — 0/10 strict is MEASUREMENT_INVALID insufficient density not falsification or physics closure.

---

## 3. State / action / target representation (frozen)

**State before/after:** URL (full, fragments preserved for hash-SPAs; normalized href vs state_after.url for leakage), document.title, CDP Accessibility.getFullAXTree full tree (600–2000 nodes required, DOM bytes≥2000, sha256 per capture), product-subtree/product-page outerHTML SHA256 via page.content() relevant subtree normalized and stripped of dynamic tokens (CSRF, timestamp, session, nonce) before hash, DOM bytes sha256. Browser state at 1280×720 via CDP, no scroll initial viewport for AX; multi-step trajectories provide temporal history for Gate0.

**Action representation:** AX node role+name + CSS path + normalized selector (derived from AX+DOM attributes, no synthetic fam_task fallback), action.target_href where present, primitive action type (click/type/navigate) for multi-step.

**Target (derived measurements):**
- M_AX_CONSISTENCY_MEAN = mean longest-prefix consistency over 10 families (per-family score = longest common prefix length / max length of full-tree tokenized pattern, no truncation), family is unit, reported with per-family scores.
- M_AX_DELTA_TRUNCATED = M_AX_FULLTREE - M_AX_TRUNCATED20 on same 20 pages (must be ≥0.20).
- M_STAGEHAND_HIT, M_STAGEHAND_MISS, M_FALSE_ACCEPT = HIT rate identical (recomputed SHA+stripping), MISS rate drift (recomputed SHA), false_accept = HIT despite drift.
- M_WEBGYM_DUP_PREVALENCE + 95% CI (2000 bootstrap), M_WEBGYM_THRESHOLD_RANGE, M_WEBGYM_PARAM_PREVALENCE.
- M_GATE0_RELAXED_PASS_COUNT, M_GATE0_STRICT_PASS_COUNT, per-family H, NL, strata, singleton rate, leakage_validOnly, unique_titles, title_entropy.

---

## 4. Sampling policy & unit of analysis

**Population:** WebArena-Verified v2 shopping families (36 families ≥3 tasks, hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30) plus shopping_admin 184-task/42-family superset if <5 product-page families achievable with 36; WebGym 300k diverse sites; BrowserGym families (WebArena shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena).  
**Sampling:** Deterministic seed 35725763380 for ALL random choices: sample 10 families without replacement from 36 (stratified to maximize product-page families; expand to admin 42-family if needed), within each family sample 2 distinct tasks. WebGym: stratified sample ≥50 diverse eTLD+1 hosts from 300k corpus. Multi-step: same 10 families. No post-hoc seed change.  
**Unit:** Family for AX (N=10 families, 20 captures), per-transition for Gate0 PMI/CMI with trajectory-grouped permutation (grouped by trajectory/family not step) to avoid degenerate bootstrap CI[1,1] variance 0 p=1 and singleton strata (require ≥5 per stratum for PMI/CMI else undefined).  
**Exclusions:** Captures with <600 nodes or DOM bytes<2000 or placeholder not expanded → invalid, counts toward <5 families substrate_unavailable, not toward mean.

---

## 5. Holdout & leakage control

- Within-store longest-prefix has no train/test leakage (descriptive consistency), but preprocessing (full-tree grammar + dynamic-token regex) is frozen before capture, not fit on held-out outcome.
- Stagehand cache: per-project isolation test (NC5) ensures no cross-project identity leakage; HIT threshold N=2 frozen.
- WebGym: site-label shuffle null (NC6) tests duplication prevalence vs site identity leakage; shard held-out is eTLD+1 (not task shuffle).
- Gate0: trajectory-grouped permutation (grouped by trajectory, not transition) and singleton SA exclusion (≥5 per stratum for H) prevent degenerate p and SHA256-truncated DOM tautology.
- Dynamic-token stripping regex frozen before hash recomputation; not fit on outcome.

---

## 6. Baselines & controls (stable identities for EXECUTE/AUDIT/DIRECTOR)

**Baselines (strong):**
- B-STAGEHAND-VERB — shipped Stagehand ~2×/~30% (must use recomputed SHA+stripping, derived selectors)
- B-RANDOM-AX-SHUFFLE — trajectory-grouped shuffle 1000 perms (primary null)
- B-TRUNCATED-20 — same 20 pages with [:20] truncation + selectors[:20] placeholder (root-cause test, requires ≥0.20 delta)
- B-WEBGYM-HARDCODED-09479 — hardcoded 0.9479 CI[0.9167,0.9792] null
- B-COLD-LLM — cold agent latency/tokens via Stagehand cold path (honest economics)
- B-CONSTANT-NULL-05654 — REJECTED 0.5654 (disclosed only, not decision)

**Positive controls:**
- PC1_LIVENESS_1280 — ≥15/20 captures 600–2000 nodes at 1280×720, Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 reachable 3 retries
- PC2_AX_PRIOR_PRODUCT — ≥1 family discriminates vs degenerate homepage 1.0 with variance>0
- PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC — 3 consecutive identical subtree SHA + selector with dynamic stripping → HIT on 2nd/3rd with per-project isolation (cross-project MISS 0%)
- PC4_WEBGYM_IMPORT_VALID — WebGym import parses ≥50 sites, manifest sha256, sweep computable
- PC5_SYNTHETIC_PIPELINE — synthetic data pipeline sanity (is_synthetic true, not decision)

**Null controls:**
- NC1_AX_SHUFFLE_TRAJECTORY_GROUPED — permute per-family scores 1000 perms, require p<0.05 and mean+0.20 gap; std 0 → FAIL
- NC2_RANDOM_PATTERN — random family pattern <0.2 expected
- NC3_DOM_DRIFT_RECOMPUTED_DYNAMIC — page.evaluate mutation + SHA recomputed AFTER via page.content()+AX with dynamic stripping, require MISS≥0.8 false_accept<0.05, verify hash change per family (before_hash vs after_hash)
- NC4_RANDOM_CACHE_ROLE_SUBSET — shuffle HIT/MISS labels 1000 perms (random-role-subset) ~50%, require true beats p<0.05
- NC5_CROSS_PROJECT_LEAKAGE — cross-project same key must MISS 0%
- NC6_WEBGYM_SHUFFLE — site-label shuffle 1000 perms for duplication (trajectory-grouped)

All perms seed 35725763380; 2000 family-level bootstraps (percentile) for CIs.

---

## 7. Primary metric, expected direction, uncertainty

**Primary:** M_AX_CONSISTENCY_MEAN on N=20 product pages. Expected direction: full-tree + stripping mean > truncated mean by ≥0.20 and > shuffle null by >0.20. Secondary: HIT/MISS/false_accept, WebGym duplication CI + sweep, Gate0 relaxed pass count.  
**Uncertainty:** 2000 family-level bootstraps (resample families with replacement, recompute mean) → 95% percentile CI; 1000 trajectory-grouped permutations for p = (1+ count perm≥true)/(1+1000). Report CI lower, variance, delta vs truncated, shuffle mean/std/p95, hash_changed_on_mutation flag. All CIs trajectory-grouped (family/trajectory), not step-level, to avoid dependence violation.

---

## 8. Adequacy & validity gate (pre-outcome)

- Adequacy: ≥10 families (20 trees) captured with 600–2000 nodes, placeholder expanded, full-tree grammar verified no truncation via code sha on 4 path families product subtree distinct hashes>1, SHA256 recomputed AFTER page.content()+AX with dynamic-token stripping verified per drift family (hash_changed_on_mutation true), BrowserGym/Playwright pins logged (pip freeze). Else MEASUREMENT_INVALID substrate_unavailable.
- Validity gate: target integrity (no post-state in pre-state, recomputed SHA after mutation with stripping), split integrity (trajectory-grouped permutation, train-only preprocessing), sampling integrity (frozen seed deterministic), uncertainty integrity (family-level bootstrap, not arbitrary jitter, trajectory-grouped), representation integrity (full-tree not truncated, relevant-subtree not full-page, CDP AX preserved, dynamic-token list disclosed). Violation → MEASUREMENT_INVALID, no SURVIVES/FALSIFIED.

---

## 9. Decision & falsification / survival rule (frozen ordered evaluation — infrastructure precedence)

1. If <5 families with product pages captured (<10 valid trees) after 3 Docker retries + grammar verification (no truncation + stripping regex) + placeholder fix → status COMPLETE outcome NOT_APPLICABLE, H1=MEASUREMENT_INVALID substrate_unavailable (publish provenance: grammar hash, dynamic-token regex, Docker digest, pip freeze). Same for WebGym <50 sites (H3 branch) or multi-step <5 families ≥50 transitions (H4 branch) → branch MEASUREMENT_INVALID only (does not invalidate other branches).

2. Else if captured ≥10 families (20 trees 600–2000 nodes each, placeholder expanded, full-tree without truncation verified, product-subtree SHA recomputed after page.content()+AX with dynamic stripping) and mean≥0.6 AND bootstrap CI lower>0.5 AND trajectory-grouped shuffle p<0.05 with +0.20 gap AND delta vs truncated ≥0.20 AND PC1≥15/20 AND per-family variance>0 (CI width>0, not degenerate [1.0,1.0] homepage tautology) then H1=SURVIVES (full-tree parameterized transfer identifiable within-store capturing product-specific subtree beyond truncation). Else if captured ≥10 families but mean<0.6 OR CI lower≤0.5 OR p≥0.05 OR delta<0.20 OR variance=0 → H1=FALSIFIED-IN-SETTING bounded to this method/families/page-type (does NOT reject alternative grammars, slot syntax, hierarchical/WebAPI retrieval, or AX semantic similarity).

3. H2_STAGEHAND_RECOMPUTED_DYNAMIC: If <30/36 families attempted or SHA not recomputed after mutation with stripping then H2=MEASUREMENT_INVALID. Else if HIT≥0.8 AND MISS≥0.8 AND false_accept<0.05 AND real-path speedup/tokens reported AND beats NC4 p<0.05 AND 0 synthetic fallback AND PC3 isolation 0.0 → SURVIVES. Else if executed ≥30 but HIT<0.8 or MISS<0.8 or false_accept≥0.05 or NC4 p≥0.05 → FALSIFIED-IN-SETTING on this substrate (bounded to exact-match + stripping construction).

4. H3_WEBGYM_DIVERSE: If <50 sites → MEASUREMENT_INVALID branch. Else if CI non-overlapping 0.9479 CI OR threshold sweep range≥0.05 (0.818–0.9479) → SURVIVES. Else if ≥50 sites but CI overlaps AND range<0.05 → FALSIFIED-IN-SETTING (single-store not distinct, diversity does not explain duplication).

5. H4_GATE0_RELAXED descriptive: If <5 families ≥50 transitions → MEASUREMENT_INVALID Gate0 branch. Else if ≥1 relaxed pass (H>0.1 NL≥20 titles≥1 singleton<50%) → SURVIVES pilot feasibility; 0/10 relaxed with adequate NL density (≥50 transitions/family, H computable with ≥5/stratum) → FALSIFIED-IN-SETTING for relaxed pilot on this site mix (insufficient density, not physics closure). 0/10 strict is MEASUREMENT_INVALID not global falsification per Director SUPERSEDE.

Overall outcome: SUPPORTS if H1 and H2 SURVIVE, MIXED if split, FALSIFIES if both H1 and H2 falsified, INCONCLUSIVE if H1 MEASUREMENT_INVALID; CAP/LFS exhaustive ABANDONED per Director SUPERSEDE not attempted. Trajectory-grouped bootstrap/permutation throughout; degenerate CI[1,1] p=1.0 flagged invalid.

---

## 10. Inherited carry-forward (exact preservation from EXP-INTEL-35860344410 handoff — Director SUPERSEDE disposition)

This handoff is continuity evidence only per AGENTS.md. Director mandate SUPERSEDE takes precedence; its `next_question` is advisory. Four-way distinction preserved:

**Established (do not re-prove, reuse artifacts; 7 items):**
- Docker substrate LIVE at 1280x720 with Playwright 1.63.0 + BrowserGym-core 0.14.3 + AgentLab 0.4.2 + CDP Accessibility.getFullAXTree yielding 20/20 valid AX trees (node counts 668-1426, DOM bytes 196958-251734, all ≥600/2000 thresholds, PC1 PASS) at seed 35725763380 with placeholder __SHOPPING__ and __SHOPPING__/path expansion verified (provenance docker_reachable true retry 1, viewport 1280x720, artifacts/raw/ax_captures.json:9990b66d)
- Trajectory-grouped permutation correctly implemented (1000 perms seed 35725763380 recomputing mean per perm) with degenerate binary scoring 8×1.0 homepage +2×0.0 product yielding shuffle mean 0.8 p95 0.8 p=1.0 (audit VF2, derived ax_consistency_fulltree.json:11955f37)
- Full-tree semantic/multi-anchor grammar without [:20] truncation implemented and verified vs prior truncation; on homepage-dominated sample full-tree mean 0.8 equals truncated mean 0.8 delta 0.0 (pattern_length 30 homepage <20 threshold vs product 59-215) so truncation not discriminating for short patterns (audit VF3)
- Selector derivation from AX tree feasible without synthetic fam_task fallback (ax_node_count 1426 role+name+CSS path) and per-project isolation enforced (cross-project MISS 0.0 on 5 tests, NC5 PASS); mutation via page.evaluate correctly changes hash (before b14722d1fb88ec9a vs after ca9fe6ffb64a4a51, hash_changed_on_mutation true) via page.content() recomputation (stagehand_replication_recomputed.json:b92665)
- Full DOM SHA256 unsuitable as Stagehand cache key on dynamic Magento pages: identical URL reload yields different hash (family 101 capture1 9fb422deea4d vs capture2 a5a64375c876 due to CSRF/session/timestamps) causing HIT 0.0; relevant-subtree normalized outerHTML not yet tested — this experiment tests normalized subtree + dynamic-token stripping remediation
- WebArena-Verified v2 census remains 192 shopping tasks 49 intent_templates 36 families ≥3 (34 ≥4, 33 ≥5) duplication 0.9479 95% CI [0.9167,0.9792] exact-copy 0.0781 param_task 0.8958 param_template 0.8367 (provenance hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30) – preserved
- Descriptive Gate0 multi-step baseline on shopping: 9 transitions collected, all action.target_href == state_after.url leakage_validOnly 1.0, 9 unique titles URL-level only (gate0_relaxed_table.json:fc6a41dd)

**Rejected (bounded, not global; 4 items):**
- Full DOM SHA256 + exact normalized selector as Stagehand verb cache HIT≥0.8 MISS≥0.8 false_accept<0.05 ~2x/~30% on dynamic shopping pages with n=10 and full-DOM hash – rejected bounded to this full-DOM construction only (HIT 0.0 MISS 1.0, audit VF4); does NOT reject normalized relevant-subtree SHA with dynamic-token stripping on ≥30 families
- AX_consistency mean≥0.6 with longest-prefix full-tree as evidence of same-mechanism within-store transfer on homepage-dominated sampling (8 homepage 1.0 vs 2 product 0.0) with degenerate shuffle p=1.0 and delta_truncated 0.0 – bounded FALSIFIED-IN-SETTING if adequacy met; does NOT reject parameterized slot syntax or hierarchical/WebAPI retrieval
- Truncated [:20] generic-token grammar as discriminating predictor – delta 0.0 shows no gain over full-tree for short homepage patterns on this storefront (audit VF3); bounded to this sampling/page-type
- WebArena-Verified v2 as cross-site testbed with cross-store overlap – vacuous null (single Magento store, 0.9479 is within-store reuse) rejected as dataset property for v2 (B-WEBGYM-HARDCODED baseline)

**Unknown (this experiment tests; 7 items + admin expansion):**
- Whether shopping_admin 184-task/42-family expansion yields ≥5 product-page families with distinct product-subtree isolation (subtree_node_count>1 distinct hashes on path families 136,145,196,222) and variance>0 with non-degenerate shuffle and delta≥0.20 – requires this expansion re-run if 36-family insufficient
- Whether normalized relevant-subtree outerHTML SHA256 with dynamic-token stripping (CSRF/timestamp/session) is stable across reloads and can achieve HIT≥0.8 MISS≥0.8 false_accept<0.05 beats NC4 p<0.05 with per-project isolation on ≥30 families and real-path latency/tokens delivering ~2x/~30% for derived selectors only
- Whether WebGym 300k-task async corpus diverse eTLD+1 census (manifest sha256, ≥50 hosts stratified seed 35725763380, duplication 2000 bootstrap CI, threshold sweep 0.818-0.9479 range ≥0.05, site entropy) overlaps hardcoded 0.9479 CI[0.9167,0.9792] and whether diversity>depth holds – requires WebGym-specific import not WebArena overlap
- Whether BrowserGym loopback or Playwright multi-step with scroll/click can collect ≥50 transitions/family on ≥10 families to compute H(S_next|URL,H_K=3), NL≥20, strata≥2, leakage_validOnly, title entropy and relaxed Gate0 H>0.1 vs strict H>0.2 NL≥50 strata≥10
- Whether alternative representations (slot syntax, hierarchical/WebAPI retrieval, AX semantic similarity vs token longest-prefix) could yield discriminating within-store transfer where longest-prefix failed – bounded falsification does not close these
- Product-subtree semantic anchoring: heading-to-product boundary not distinct enough (subtree_node_count=1 prior) on Magento template; code hash for full-tree grammar not persisted – this experiment persists code hash
- True spec-compliant cross-website overlap at TF-IDF(k=5000 ngram1-2 min_df2) → k-means k=min(50,unique_tasks/20) train-only remains unmeasured due to Mind2Web HF single-split limitation (diagnostic only)

**Do_not_assume (9 prohibitions preserved verbatim):**
- Do NOT assume mean AX_consistency 0.8 is evidence of same-mechanism transfer – artifact of binary 8×1.0 homepage vs 2×0.0 product with degenerate shuffle p=1.0 and CI lower 0.5 not >0.5
- Do NOT assume full-tree provides >0.10 gain over truncated [:20] on this site – delta 0.0 because homepage patterns length 30 <20 threshold; truncation fix not tested on product pages with longer patterns 59-215 due to scarcity 4/20 captures (this experiment requires 10 product families and delta≥0.20)
- Do NOT assume Stagehand false_accept 0.0 until recomputed relevant-subtree + dynamic stripping tested – full DOM instability (HIT 0.0 MISS 1.0) proves full DOM hash invalid, not Stagehand impossible
- Do NOT assume Gate0 0/10 relaxed failure is global impossibility – 9 transitions vs ≥50/family required is MEASUREMENT_INVALID insufficient density, not physics closure
- Do NOT assume WebGym LIMITED 50 non-standard hosts from WebArena overlap equals diverse eTLD+1 50-site census – duplication_ci null threshold_sweep null manifest null; do not use B-WEBGYM-HARDCODED null as predictor
- Do NOT assume within-store 0.9 or homepage 1.0 implies cross-site transfer – WebArena-Verified v2 is single-store vacuous null, cross-site requires multi-store dataset
- Do NOT assume infrastructure live (Docker reachable, Playwright 1.63.0) equals scientific success – adequacy gates (product families ≥5, n≥30 families, stable cache key with stripping, 50 transitions/family) must still pass before SURVIVES; degenerate CI[1,1] flagged invalid
- Do NOT assume product economics ~2x/~30% Stagehand floor validated – speedup null tokens null not measured without Stagehand server and wrong cache key; per-hit vs fixed at f=100 not assessable until this recomputed+stripping replication
- Do NOT carry forward producer MIXED outcome – frozen rule requires COMPLETE NOT_APPLICABLE/INCONCLUSIVE with H1=MEASUREMENT_INVALID when <5 product families; MIXED is audit VIOLATION to be corrected

---

## 11. Product consequences

**Positive (SURVIVES):** H1 SURVIVES (full-tree+stripping mean≥0.6 CI lower>0.5 p<0.05 vs trajectory-grouped shuffle delta≥0.20 vs truncated variance>0 product pages PC1≥15/20) gives first measurement-valid within-store parameterized transfer signal on WebArena-Verified v2 shopping product pages via full-tree semantic/multi-anchor + recomputed SHA with dynamic-token stripping, superseding prior homepage tautology 1.0 [1,1] p=1.0 and prior invalid 0.2857. Enables bounded C-CROSSSITE within-store holdout (mechanisms learned on product A transfer to product B without retraining) and informs C-LLM-INHERIT within-store economics where sharing frequency threshold determines SPIDER vs Stagehand choice. H2 SURVIVES recomputed+stripping (HIT≥0.8 MISS≥0.8 false_accept<0.05 vs NC4 with real-path latency/tokens derived-only) gives shipped competitive floor Stagehand ~2x/~30% that SPIDER must beat for C-PRODUCT-ECON honest amortized economics (per-hit vs fixed at f=100 separated). H3 SURVIVES WebGym 50 diverse-site census proves duplication sensitivity and distribution diversity effect replacing hardcoded 0.9479, unblocking cross-site holdout design without exhaustive LFS/420-task CAP. H4 ≥1 relaxed Gate0 pass unlocks correlated-state physics pilot (session-correlated latent regimes, not independent noise). Artifacts become reusable substrate for Mind2Web-2 upgrade.

**Negative (FALSIFIED or MEASUREMENT_INVALID):** H1 FALSIFIED (captured ≥10 product families but full-tree+stripping mean<0.6 or CI lower≤0.5 or p≥0.05 or delta<0.20 or variance=0) → full-tree longest-prefix insufficient for product-specific transfer, requires parameterized slot syntax or hierarchical/WebAPI retrieval; C-CROSSSITE stays HYPOTHESIS single-store vacuous, C-LLM-INHERIT within-store stays HYPOTHESIS. H2 FALSIFIED (≥30 executed but HIT<0.8 or MISS<0.8 or false_accept≥0.05 after recomputation+stripping) → Stagehand exact cache not discriminating on shopping even with stripping — its 2x/~30% does not transfer to these families; use B-RAG-EMBED-FLAT or SPIDER verification baseline and C-PRODUCT-ECON stays HYPOTHESIS. Any MEASUREMENT_INVALID branch (<5 product families, <50 WebGym sites, <5 multi-step families) → no falsification, repair Docker/WebGym or use BrowserGym loopback before claiming impossibility; exhaustive CAP/LFS not re-triggered per Director SUPERSEDE (ABANDONED not falsified). H3 FALSIFIED duplication overlaps 0.9479 means single-store census not distinct — still not cross-site holdout evidence.

---

## 12. Cost & information gain

**Cost:** LOW-MEDIUM, no LLM inference for AX/Gate0/WebGym; ~3–4h wall-clock, <15GB /tmp, stdlib+playwright+browsergym/agentlab+tiktoken. Docker pull am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 (~1-2GB) + BrowserGym-core 0.14.3 + AgentLab 0.4.2/0.3.0 + Playwright 1.63.0 Chromium (~300MB). Reuse WebArena census hash d652... for pin verification; no exhaustive enumeration.

**Expected information gain:** MAXIMUM per Director comparative reasoning — directly repairs 8 audit-required degeneracies (truncation, SHA not recomputed + stripping, degenerate p=1.0, singleton strata, homepage dominance) with deterministic fixes delivering falsifiable variance>0 transfer proof or bounded rejection (delta≥0.20 discriminability), re-derives Stagehand with hash-after-mutation+stripping competitive floor informing per-hit vs fixed at f=100 amortized economics, WebGym diverse import tests diversity>depth without LFS, multi-step relaxed Gate0 H>0.1 NL≥20 unlocks physics correlated-state pilot. Either SURVIVES unlocks product within-store holdout + WebGym cross-site baseline + physics pilot, or FALSIFIED-IN-SETTING redirects product to hierarchical/WebAPI retrieval and avoids re-triggering blocked exhaustive path — highest global leverage vs synthetic FSM TV continuation (44-deep frontier tunnel closed). Falsifiability: agent priors (path dependence, work-compression h~8%, verification false_accept cost, tool-ordering invariant protocols) are priors to be tested, not assumed evidence.

---

## 13. Preregistration freeze

Hypothesis, state/action representation (including dynamic-token stripping regex), sampling policy (seed 35725763380), holdout/leakage controls, baselines/nulls/positive controls, primary metric, expected direction, uncertainty method (2000 family bootstrap, 1000 trajectory-grouped permutations), adequacy rule, and falsification/survival rule frozen before any outcome-bearing measurement on this experiment_id. Any analysis change after seeing outcomes is exploratory; new confirmatory claim requires new preregistration and untouched evidence. Raw artifacts preserved with sha256 per spec.json §measurement_validity; report.md may interpret but not contradict result.json or exceed frozen claim. CAP/LFS exhaustive enumeration explicitly ABANDONED and not attempted; 0/10 strict Gate0 remains MEASUREMENT_INVALID not falsification.

