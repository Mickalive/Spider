# EXP-INTEL-35881414325 preregistration — Intel REOPEN to C-CROSSSITE (SUPERSEDE)

**Lane:** intel — `research/intel` only (no cross-lane writes)  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout (registry HYPOTHESIS); auxiliary gates C-MEAS-VALID, C-WEB-DYNAMICS (Gate0), C-PRODUCT-ECON (Stagehand economics) reported descriptively but not promoted beyond C-CROSSSITE ceiling  
**Director mandate:** REOPEN, cognitive_reset true, parent_handoff_disposition SUPERSEDE (EXP-INTEL-35876349051 MEASUREMENT_INVALID substrate_unavailable 0/20 Docker unreachable); expires exhaustive 567MB LFS / 420-task CAP enumeration (0/3 strict MEASUREMENT_INVALID not falsification, degenerate 0.2857->1.0 CI[1,1] p=1.0 due to [:20] truncation). Target pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, full-tree semantic/multi-anchor without truncation plus dynamic-token stripping, WebGym 300k diverse holdout >=50 eTLD+1, multi-step >=50 transitions/family >=10 families. Dependencies: [runtime BrowserGym 1280x720 CDP AX>10 provisioning] (non-blocking but required for live branch).  
**Inherited state consumed:** Read `research/experiments/EXP-INTEL-35876349051/handoff.json` sha 35dde70eac99810052e6a8e26c29d20ad679a08f271fa9fb390ad8c62b1b6352; preserved established/rejected/unknown/do_not_assume verbatim in §10. This NEW governed experiment follows the Director's strategic question (REOPEN C-CROSSSITE), not the parent handoff's `next_question` (which is advisory continuity only per AGENTS.md global direction discipline). No outcome-bearing measurement run during DESIGN. Verifies 13-streak C-CROSSSITE tunnel_flag and degenerate AX variance 0 p=1.0 blocking Physics Gate0.
**Agent priors (Director, distinguished from SPIDER evidence):** (1) path dependence & salience bias — later-agent cost tracks history length not residual novelty without novelty budgeting, (2) caching/replay strong on deterministic SPAs where URL hash encodes state — beyond-memory PMI 0 by construction, (3) distributed substrate fails silently on auth/session with per-node SQLite — shared WAL minimum viable, (4) exact-intent matching fails on semantic aliasing — only family-required rewriting + multi-candidate composition breaks ceiling, (5) failed bounded programs do not close domains. These are priors to be tested, not assumed.

---

## 1. Strategic question (Director binding) → falsifiable experiment

**Director question (binding, from request.json director_mandate.question):** Can BrowserGym/WebGym diverse-site sampling replace exhaustive 567MB LFS/420-task enumeration: (a) WebGym 300k manifest sample >=50 eTLD+1 diverse sites yields duplication 0.9479 95% CI (2000 bootstrap) and threshold sweep 0.818-0.9479 plus parameterization prevalence 0.8958 without exhaustive LFS, (b) relaxed Gate0 census H>0.1 NL>=20 titles>=1 via BrowserGym 1280x720 multi-step trajectories >=50 transitions/family on >=10 families (WebArena shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) with cold vs cached latency/tokens, (c) full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, no selectors[:20] placeholder, product-subtree SHA256 recomputed after page.content()+AX via page.evaluate with dynamic-token stripping) at 1280x720 with 20 live CDP captures task-specific start_url 10 families x2 seed 35725763380 requiring mean>=0.6 bootstrap lower>0.5 shuffle p<0.05 delta>=0.20 vs truncated, and (d) Stagehand relevant-subtree HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 random-role-subset null with real-path latency/tokens, all trajectory-grouped bootstrap CIs 2000?

**Smallest high-information translation (this prereg):** Narrow repaired pilot on WebArena-Verified v2 shopping product pages (10 families ×2 tasks =20 CDP captures at 1280x720 with dynamic-token stripping) + Stagehand recomputed replication on same 36 families (derived selectors only, SHA recomputed after mutation + stripping, real-path latency/tokens) + WebGym 300k 50-site diverse census (2000 bootstrap CI + threshold sweep) + 10-family multi-step rollout (strive 50 transitions each, BrowserGym-core 0.14.3 primary with Playwright fallback). Any narrower (single metric) would leave Stagehand competitive floor or WebGym diversity untested and risk another degenerate pass; any broader (exhaustive LFS/CAP) repeats blocked path with zero marginal information gain per Director comparative reasoning ("Exhaustive LFS/CAP search is closed per scout." / "Continuing same-store AX_consistency enumeration or Mind2Web official splits with TF-IDF k-means repeats Gate0 single-train measurement-invalid mode (0/3 SPAs). WebGym 300k diverse sampling has higher marginal value"). Already-frozen experiments resume independently; pre-freeze work is superseded per mandate.

---

## 2. Hypotheses (confirmatory)

- **H1_AX_FULLTREE (primary, confirmatory):** Full-tree semantic/multi-anchor without truncation (complete CDP Accessibility.getFullAXTree traversal from root, product-specific subtree anchored on heading/price/add-to-cart/main/contentinfo boundaries, role+name+CSS path + subtree outerHTML SHA256 normalized by stripping CSRF/timestamp/session IDs/tokens, no token truncation, longest-prefix without fallback) yields discriminating within-store AX_consistency on N=20 live product-page captures with mean≥0.6, bootstrap 2000 family-level 95% CI lower>0.5, trajectory-grouped permutation 1000 p<0.05 vs NC1 (>0.20 above null mean/p95), delta≥0.20 vs truncated [:20] baseline on same pages, per-family variance>0 (CI width>0, not degenerate [1.0,1.0] homepage tautology with p=1.0), product-subtree node counts>1 distinct hashes on path families.

- **H2_STAGEHAND_RECOMPUTED_DYNAMIC (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (exact normalized selector from AX node+DOM attributes + SHA256 of relevant subtree outerHTML recomputed AFTER mutation via page.content()+AX Accessibility.getFullAXTree via page.evaluate, HIT after N=2 identical results, per-project isolation, 0 synthetic fam_task fallback, dynamic-token stripping before hash) reports HIT≥0.8 on identical DOM, MISS≥0.8 on single-attribute drifted DOM (page.evaluate mutation, hash recomputed after), false_accept<0.05, beats NC4 random-role-subset null p<0.05, with cold vs cached latency/tokens via real Playwright dispatch path (navigation + hash + cache lookup, tiktoken/provider counts) delivering ~2× speedup and ~30% token saving on HIT when selectors exclusively derived.

- **H3_WEBGYM_DIVERSE (confirmatory):** WebGym 300k-task async corpus (>=50 diverse eTLD+1 hosts, stratified deterministic seed 35725763380, manifest sha256) yields duplication prevalence 95% CI (2000 family-level bootstrap) distinct from hardcoded WebArena-Verified v2 single-store duplication 0.9479 CI[0.9167,0.9792] (192 tasks 49 templates 36 families) and corpus-level deduplication threshold sweep range ≥0.05 across 0.818–0.9479, plus parameterization prevalence near 0.8958 computable without exhaustive 567MB LFS, proving distribution diversity matters more than hierarchical depth.

- **H4_GATE0_RELAXED (descriptive pilot, not confirmatory physics claim):** Multi-step trajectories ≥50 transitions/family on ≥10 families yield ≥1 family passing relaxed census (titles≥1 H(S_next|URL,H_K=3)>0.1 NL≥20 singleton<50%) enabling correlated-state physics pilot; strict Gate0 (H>0.2 NL≥50 strata≥10 leakage_validOnly<40%) reported descriptively — 0/10 strict is MEASUREMENT_INVALID insufficient density not falsification or physics closure.

---

## 3. State / action / target representation (frozen)

**State before/after:** URL (full, fragments preserved for hash-SPAs; normalized href vs state_after.url for leakage), document.title, CDP Accessibility.getFullAXTree full tree (600–2000 nodes required, DOM bytes≥2000, sha256 per capture), product-subtree/product-page outerHTML SHA256 via page.content() relevant subtree normalized and stripped of dynamic tokens (CSRF, timestamp, session, nonce, 13-digit, hex) before hash, DOM bytes sha256. Browser state at 1280×720 via CDP, no scroll initial viewport for AX; multi-step trajectories provide temporal history for Gate0.

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

## 10. Inherited carry-forward (exact preservation from EXP-INTEL-35876349051 handoff — Director SUPERSEDE disposition)

This handoff is continuity evidence only per AGENTS.md. Director mandate SUPERSEDE takes precedence; its `next_question` is advisory. Four-way distinction preserved:

**Established (do not re-prove, reuse artifacts; 7 items):**
- Transient substrate failure correctly classified as MEASUREMENT_INVALID not falsification: Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 unreachable after 3 retries (Errno 111 Connection refused, M_AX_VALID_CAPTURES 0/20, M_AX_PRODUCT_FAMILY_COUNT 0, PC1_LIVENESS FAIL) per result.json metrics M_AX_VALID_CAPTURES, M_AX_PC1_LIVENESS_DETAIL and audit validity_findings[0]; prior 20/20 live proof (668-1426 nodes, DOM 196958-251734 bytes, seed 35725763380) on same image preserved via EXP-INTEL-35860344410 artifacts/raw/ax_captures.json:9990b66d — this run's 0/20 is environment, not site impossibility
- Full-tree semantic/multi-anchor grammar without [:20] truncation + 9 dynamic-token regexes (csrf/session/_token/timestamp/nonce/13-digit/hex) + placeholder expansion __SHOPPING__/path -> http://localhost:7770/path verified by code audit grammar_code_hash 8d4b7cb8b543c10912f5d4325ccee0e5ae839f64c534a354f5ac8e7b1a364a45 per result.json M_AX_GRAMMAR_CODE_HASH, provenance code_artifacts.grammar_code_hash and audit validity_findings[2]; unexercised live on product pages — fixes root-cause truncation degeneracy but remains hypothesis
- Deterministic sampling integrity preserved: 10 families [191,180,162,197,153,213,163,137,136,222] sampled without replacement from 36 families >=3 via frozen seed 35725763380, includes 2 path families 136,222 as intended; no post-hoc seed change; trajectory-grouped 2000 bootstrap/1000 shuffle protocols frozen but correctly not executed on 0 scores avoiding degenerate CI[1,1] p=1.0 per audit validity_findings[3]
- Stagehand recomputed+stripping logic frozen (key = (project_id, normalized_selector from AX role/name/CSS, dom_hash=SHA256 normalized relevant-subtree outerHTML AFTER page.content()+AX via page.evaluate with 9 regex stripping), N=2 HIT threshold, per-project isolation, 0 synthetic fam_task fallback) per result.json controls B-STAGEHAND-VERB and audit validity_findings[5]; not exercised live (0/36 families) — prior full-DOM instability documented but not retested
- WebArena-Verified v2 census pin preserved 192 shopping tasks 49 intent_templates 36 families >=3 (34 >=4, 33 >=5) duplication 0.9479 95% CI [0.9167,0.9792] exact-copy 0.0781 param_task 0.8958 param_template 0.8367 hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 per provenance datasets.webarena_verified; not newly established this run
- CAP 567MB LFS exhaustive enumeration and 420-task CAP correctly ABANDONED per Director SUPERSEDE (request.json director_mandate.parent_handoff_disposition SUPERSEDE, spec.json product_consequence_negative, result.json validity_notes CAP ABANDONED) — not attempted, not falsified; remaining gap is minimal 10-family expansion + 36-family Stagehand + 50-site WebGym + 10-family multi-step only
- Infrastructure precedence correctly applied per spec.json decision_rule ordered evaluation and prereg s9: <5 families triggers MEASUREMENT_INVALID substrate_unavailable and outcome NOT_APPLICABLE (result.json outcome NOT_APPLICABLE, audit claim_ceiling MEASUREMENT_INVALID) — producer MIXED violation corrected in prior but this producer correctly uses COMPLETE NOT_APPLICABLE

**Rejected (bounded, not global; 4 items):**
- No new bounded rejections in this run — 0 valid captures prevents SURVIVES/FALSIFIED-IN-SETTING evaluation. Prior bounded rejections preserved verbatim from EXP-INTEL-35860344410 handoff: (1) full DOM SHA256 + exact selector as Stagehand verb cache HIT>=0.8 bound to full-DOM construction (HIT 0.0), (2) homepage-dominated AX_consistency mean 0.8 as transfer evidence degenerate p=1.0 delta 0.0, (3) truncated [:20] grammar as discriminating predictor, (4) WebArena-Verified v2 as cross-site testbed (single-store vacuous) — none extended or closed globally by this MEASUREMENT_INVALID run

**Unknown (this experiment tests; 7 items + admin expansion):**
- H1_AX_FULLTREE: whether full-tree semantic/multi-anchor product-subtree AX_consistency achieves mean>=0.6 bootstrap CI lower>0.5 trajectory-grouped shuffle p<0.05 delta>=0.20 vs truncated baseline with variance>0 on WebArena-Verified v2 shopping product pages at 1280x720 with dynamic-token stripping — requires Docker live 20 captures (10 families x2 via get_task_start_url) with 600-2000 nodes each and distinct hashes on path families 136,145,196,222 (audit unresolved 0, result.json unresolved 0)
- H2_STAGEHAND_RECOMPUTED_DYNAMIC: whether normalized relevant-subtree outerHTML SHA256 with stripping achieves HIT>=0.8 MISS>=0.8 false_accept<0.05 beats NC4 random-role-subset p<0.05 with per-project isolation 0% and real-path Playwright latency/tokens ~2x/~30% derived selectors only on >=30/36 families — requires recomputed SHA after page.evaluate mutation + drift injection >=20 families + cross-project >=5 (audit unresolved 1, result.json unresolved 1)
- H3_WEBGYM_DIVERSE: whether WebGym 300k 50 diverse eTLD+1 sites yield duplication 95% CI (2000 bootstrap) distinct from hardcoded 0.9479 CI[0.9167,0.9792] and threshold sweep range>=0.05 across 0.818-0.9479 plus param prevalence ~0.8958 — requires WebGym manifest import and dedup sweep (audit unresolved 2, result.json unresolved 2)
- H4_GATE0_RELAXED: whether BrowserGym 0.14.3 or Playwright fallback multi-step achieves >=50 transitions/family on >=10 families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) to compute H(S_next|URL,H_K=3), NL>=20, strata>=2, leakage_validOnly, title entropy and relaxed Gate0 H>0.1 NL>=20 singleton<50% vs strict H>0.2 NL>=50 — requires loopback rollout at 1280x720 (audit unresolved 3, result.json unresolved 3)
- Whether shopping_admin 184-task/42-family expansion (available in provenance admin_tasks 184 admin_families 42) yields >=5 product-page families with product-subtree node_count>1 distinct hashes and variance>0 where 36-family sample yielded 0/20 due to Docker failure — not tested this run
- Whether product-subtree semantic anchoring (heading/price/add-to-cart/main/contentinfo boundaries) isolates distinct product boundary on Magento template vs prior subtree_node_count=1 failure — code hash 8d4b persisted but live distinctness on 136,145,196,222 not validated
- Whether alternative representations (parameterized slot syntax, hierarchical/WebAPI retrieval, AX semantic similarity vs token longest-prefix) could yield discriminating transfer where longest-prefix fails — bounded falsification does not close orthogonal mechanisms per falsifier

**Do_not_assume (10 prohibitions preserved verbatim):**
- Do NOT assume 0/20 valid captures (Connection refused after 3 retries) is evidence that full-tree parameterized transfer is impossible — it is MEASUREMENT_INVALID transient substrate_unavailable per audit validity_findings[0] and result.json validity_notes[0]; prior 20/20 live on same image proves Docker can work, repair is docker pull + run -p 7770:7770 and playwright install
- Do NOT assume mean null / CI [null,null] / shuffle p null / delta null equals degenerate mean 0.8 CI[0.5,1.0] p=1.0 delta 0.0 from prior homepage-dominated run — this run avoids degenerate tautology by returning null not binary 8x1.0+2x0.0; trajectory-grouped bootstrap/shuffle not executed is correct
- Do NOT assume full-tree provides any gain over truncated [:20] on product pages — delta_vs_truncated null (not 0.0) because no live pages to compare; code audit verifies no truncation but live delta>=0.20 remains untested
- Do NOT assume Stagehand full-DOM HIT 0.0 proves Stagehand impossible — full DOM instability (CSRF/session/timestamp causing 9fb422deea4d vs a5a64375c876 on reload) proves full-DOM key invalid, not Stagehand; recomputed relevant-subtree + 9 regex stripping remains untested and per-project isolation 0% from prior not re-measured this run
- Do NOT assume Gate0 0/10 relaxed (0 transitions) is global physics closure — 0 vs >=50/family required is MEASUREMENT_INVALID insufficient density per audit validity_findings[5] and result.json validity_notes[5]; BrowserGym-core 0.14.3 available proves import not bottleneck, Docker is; single-page CDP acknowledged insufficient per prereg
- Do NOT assume WebGym LIMITED 50 non-standard hosts from WebArena overlap equals diverse eTLD+1 50-site census — duplication_ci null threshold_sweep null manifest null; do not use hardcoded 0.9479 CI as predictor per audit validity_findings[4]
- Do NOT assume within-store AX_consistency or homepage 1.0 implies cross-site transfer — WebArena-Verified v2 is single Magento One Stop Market store (single container), cross-site requires multi-store diverse dataset; C-CROSSSITE remains HYPOTHESIS single-store vacuous
- Do NOT assume infrastructure live (Playwright 1.63.0 + BrowserGym-core 0.14.3 installed, tiktoken 0.14.0 available) equals scientific success — adequacy gates (product families >=5 with 600-2000 nodes, n>=30 families stable cache key with stripping, 50 transitions/family) must still pass before SURVIVES per measurement_validity; degenerate CI[1,1] and singleton strata flagged invalid
- Do NOT assume product economics ~2x/~30% Stagehand floor validated — HIT/MISS/speedup/tokens null not measured without Stagehand server and live captures; per-hit vs fixed at f=100 not assessable
- Do NOT re-trigger exhaustive 567MB LFS test.zip or 420-task CAP enumeration or WebJudge-7B exhaustive search — explicitly ABANDONED per Director SUPERSEDE comparative_reasoning and spec product_consequence_negative; next test is minimal 10-family expansion + 36-family Stagehand + 50-site WebGym + 10-family multi-step only, with rewritten normalized fragment logic and full-tree multi-anchor at 1280x720

---

## 11. Product consequences

**Positive (SURVIVES):** H1 SURVIVES (full-tree+stripping mean≥0.6 CI lower>0.5 p<0.05 vs trajectory-grouped shuffle delta≥0.20 vs truncated variance>0 product pages PC1≥15/20) gives first measurement-valid within-store parameterized transfer signal on WebArena-Verified v2 shopping product pages via full-tree semantic/multi-anchor + recomputed SHA with dynamic-token stripping, superseding prior homepage tautology 1.0 [1,1] p=1.0 and prior invalid 0.2857. Enables bounded C-CROSSSITE within-store holdout (mechanisms learned on product A transfer to product B without retraining) and informs C-LLM-INHERIT within-store economics where sharing frequency threshold determines SPIDER vs Stagehand choice. H2 SURVIVES recomputed+stripping (HIT≥0.8 MISS≥0.8 false_accept<0.05 vs NC4 with real-path latency/tokens derived-only) gives shipped competitive floor Stagehand ~2x/~30% that SPIDER must beat for C-PRODUCT-ECON honest amortized economics (per-hit vs fixed at f=100 separated). H3 SURVIVES WebGym 50 diverse-site census proves duplication sensitivity and distribution diversity effect replacing hardcoded 0.9479, unblocking cross-site holdout design without exhaustive LFS/420-task CAP. H4 ≥1 relaxed Gate0 pass unlocks correlated-state physics pilot (session-correlated latent regimes, not independent noise). Artifacts become reusable substrate for Mind2Web-2 upgrade.

**Negative (FALSIFIED or MEASUREMENT_INVALID):** H1 FALSIFIED (captured ≥10 product families but full-tree+stripping mean<0.6 or CI lower≤0.5 or p≥0.05 or delta<0.20 or variance=0) → full-tree longest-prefix insufficient for product-specific transfer, requires parameterized slot syntax or hierarchical/WebAPI retrieval; C-CROSSSITE stays HYPOTHESIS single-store vacuous, C-LLM-INHERIT within-store stays HYPOTHESIS. H2 FALSIFIED (≥30 executed but HIT<0.8 or MISS<0.8 or false_accept≥0.05 after recomputation+stripping) → Stagehand exact cache not discriminating on shopping even with stripping — its 2x/~30% does not transfer to these families; use B-RAG-EMBED-FLAT or SPIDER verification baseline and C-PRODUCT-ECON stays HYPOTHESIS. Any MEASUREMENT_INVALID branch (<5 product families, <50 WebGym sites, <5 multi-step families) → no falsification, repair Docker/WebGym or use BrowserGym loopback before claiming impossibility; exhaustive CAP/LFS not re-triggered per Director SUPERSEDE (ABANDONED not falsified). H3 FALSIFIED duplication overlaps 0.9479 means single-store census not distinct — still not cross-site holdout evidence.

---

## 12. Cost & information gain

**Cost:** LOW-MEDIUM, no LLM inference for AX/Gate0/WebGym; ~3–4h wall-clock, <15GB /tmp, stdlib+playwright+browsergym/agentlab+tiktoken. Docker pull am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 (~1-2GB) + BrowserGym-core 0.14.3 + AgentLab 0.4.2/0.3.0 + Playwright 1.63.0 Chromium (~300MB). Reuse WebArena census hash d652... for pin verification; no exhaustive enumeration.

**Expected information gain:** MAXIMUM per Director comparative reasoning — directly repairs 8 audit-required degeneracies (truncation, SHA not recomputed + stripping, degenerate p=1.0, singleton strata, homepage dominance) with deterministic fixes delivering falsifiable variance>0 transfer proof or bounded rejection (delta≥0.20 discriminability), re-derives Stagehand with hash-after-mutation+stripping competitive floor informing per-hit vs fixed at f=100 amortized economics, WebGym diverse import tests diversity>depth without LFS, multi-step relaxed Gate0 H>0.1 NL≥20 unlocks physics correlated-state pilot. Either SURVIVES unlocks product within-store holdout + WebGym cross-site baseline + physics pilot, or FALSIFIED-IN-SETTING redirects product to hierarchical/WebAPI retrieval and avoids re-triggering blocked exhaustive path — highest global leverage vs synthetic FSM TV continuation (closed). Falsifiability: agent priors are priors to be tested, not assumed evidence.

---

## 13. Preregistration freeze

Hypothesis, state/action representation (including dynamic-token stripping regex), sampling policy (seed 35725763380), holdout/leakage controls, baselines/nulls/positive controls, primary metric, expected direction, uncertainty method (2000 family bootstrap, 1000 trajectory-grouped permutations), adequacy rule, and falsification/survival rule frozen before any outcome-bearing measurement on this experiment_id. Any analysis change after seeing outcomes is exploratory; new confirmatory claim requires new preregistration and untouched evidence. Raw artifacts preserved with sha256 per spec.json §measurement_validity; report.md may interpret but not contradict result.json or exceed frozen claim. CAP/LFS exhaustive enumeration explicitly ABANDONED and not attempted; 0/10 strict Gate0 remains MEASUREMENT_INVALID not falsification.

