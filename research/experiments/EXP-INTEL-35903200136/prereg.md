# EXP-INTEL-35903200136 preregistration — Intel PIVOT to C-CROSSSITE (SUPERSEDE, cognitive_reset)

**Lane:** intel — `research/intel` only (no cross-lane writes)  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout (registry HYPOTHESIS); auxiliary gates C-MEAS-VALID, C-WEB-DYNAMICS (Gate0), C-PRODUCT-ECON (Stagehand economics) reported descriptively  
**Director mandate:** PIVOT, cognitive_reset true, parent_handoff_disposition SUPERSEDE (EXP-INTEL-35892848544 MEASUREMENT_INVALID substrate_unavailable: 0/20 Docker unreachable due to 5.4GB pull TimeoutExpired 90s on full 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb, clean env without BrowserGym/Playwright, 16-streak C-CROSSSITE tunnel). Target pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, full-tree semantic/multi-anchor without truncation plus 9-regex dynamic-token stripping, WebGym 300k diverse holdout >=50 eTLD+1, multi-step >=50 transitions/family >=10 families, full 64-char Docker digest via registry API/skopeo with timeout >=300s or cached tar. Dependencies: [] per request.json.  
**Inherited state consumed:** Read `research/experiments/EXP-INTEL-35892848544/handoff.json` sha fc9913b28096ddfbd0bd132684461022589e2667aca1f0de3679b1cbabd1a9b7; preserved established/rejected/unknown/do_not_assume verbatim in §10. This NEW governed experiment follows the Director's strategic question (PIVOT C-CROSSSITE BrowserGym/WebGym diverse sampling replacing exhaustive 567MB LFS 420-task CAP), not the parent handoff's `next_question` which is advisory continuity only per AGENTS.md global direction discipline. No outcome-bearing measurement run during DESIGN. Verifies exhaustive-LFS tunnel and degenerate AX variance 0 blocking Physics Gate0.

**Agent priors (Director, distinguished from SPIDER evidence):** (1) Compounding planning errors over long horizons — 0/10 mixed header+body+query+auth joint failure from 0.5^3 while header 10/10 and body 10/10 succeed implies factorization needed; (2) Path dependence/salience — agents overweight early tools, require OOD family hold-out where literally correct path absent; (3) Diminishing returns to local tuning — 12 C-SEMANTIC-RESOLVE +5 C-PARAM-INHERIT consecutive failures low marginal vs orthogonal tool-compilation; (4) Caching/replay fails via staleness/false_accept (UNKNOWN calibration ECE<=0.15 precision>=0.85 false_accept<=0.10 harder than recall); (5) Representation loss dominates — hash-truncated AX[:20] discards controlling variables. Priors are testable, not assumed.

---

## 1. Strategic question (Director binding) → falsifiable experiment

**Director question (binding, from request.json director_mandate.question):** Can BrowserGym/WebGym diverse-site sampling replace exhaustive 567MB LFS 420-task CAP enumeration: (a) WebGym 300k manifest sample >=50 eTLD+1 diverse sites yields duplication 95% CI 2000 bootstrap and threshold sweep 0.818-0.9479 plus param_task prevalence vs vacuous 0.9479 single-store, (b) relaxed Gate0 census H>0.1 NL>=20 titles>=1 via BrowserGym 1280x720 multi-step trajectories >=50 transitions/family on >=10 families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) with cold vs cached latency/tokens, (c) full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, product-subtree SHA256 recomputed via page.content()+AX with dynamic-token stripping) at 1280x720 with 20 live CDP captures task-specific start_url 10 families x2 seed 35725763380 requiring mean>=0.6 bootstrap lower>0.5 shuffle p<0.05 delta>=0.20 vs truncated, and (d) Stagehand relevant-subtree HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 random-role-subset null with trajectory-grouped bootstrap CIs, with pinned BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 and full 64-char Docker digest am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb?

**Smallest high-information translation (this prereg):** Narrow repaired pilot on WebArena-Verified v2 shopping product pages (10 families ×2 tasks =20 CDP captures at 1280x720 with 64-char digest resolution timeout>=300s + dynamic stripping) + Stagehand recomputed replication on 36 families (derived selectors only, SHA recomputed after mutation + stripping, real-path latency/tokens) + WebGym 300k 50-site diverse census (2000 bootstrap CI + threshold sweep) + 10-family multi-step rollout (strive 50 transitions each, BrowserGym-core 0.14.3 primary with Playwright fallback). Any narrower (single metric) would leave Stagehand floor or WebGym diversity untested; any broader (exhaustive LFS 567MB test.zip / CAP 420-task) repeats blocked path with zero marginal gain per Director comparative reasoning: “Repeating Docker pull with timeout>=300s without fixing AX grammar or moving to WebGym sampling repeats degenerate 1.0 CI[1,1] p=1.0 measurement. Diverse-site threshold sweep and full-tree AX with trajectory-grouped permutation directly tests same-mechanism overlap vs shuffled null >=0.10, which exhaustive LFS cannot deliver.” Already-frozen experiments resume independently; pre-freeze work is superseded per mandate.

---

## 2. Hypotheses (confirmatory)

- **H1_AX_FULLTREE (primary, confirmatory):** Full-tree semantic/multi-anchor without truncation (complete CDP Accessibility.getFullAXTree traversal from root, product-specific subtree anchored on heading/price/add-to-cart/main/contentinfo boundaries, role+name+CSS path + subtree outerHTML SHA256 normalized by stripping 9 dynamic-token regexes [csrf[_-]?token, session[_-]?id, _token, timestamp, nonce, csrf value, sessionId, \b\d{13}\b, \b[a-f0-9]{32,}\b], no token truncation, longest_prefix_without_fallback and sha256_normalized_subtree with stripping but not yet exercised on live trees) yields discriminating within-store AX_consistency on N=20 live product-page captures with M_AX_CONSISTENCY_MEAN≥0.6, 2000 family-level bootstrap 95% CI lower>0.5, trajectory-grouped permutation 1000 p<0.05 vs NC1 (>0.20 above null mean/p95), M_AX_DELTA_TRUNCATED≥0.20 vs truncated [:20] baseline on same pages, M_AX_PER_FAMILY_VARIANCE>0 (CI width>0, not degenerate [1.0,1.0] homepage tautology with p=1.0), product-subtree node counts>1 distinct hashes on path families 136,145,196,222. Requires 600-2000 AX nodes per capture, DOM bytes≥2000, full 64-char Docker digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb resolved with timeout>=300s or cached tar.

- **H2_STAGEHAND_RECOMPUTED_DYNAMIC (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (exact normalized selector from AX+DOM + SHA256 of relevant subtree outerHTML recomputed AFTER mutation via page.content()+AX Accessibility.getFullAXTree via page.evaluate, HIT after N=2 identical results, per-project isolation, 0 synthetic fam_task fallback, 9-regex dynamic stripping before hash) reports M_STAGEHAND_HIT≥0.8 on identical DOM, M_STAGEHAND_MISS≥0.8 on single-attribute drifted DOM (page.evaluate mutation, hash recomputed after), M_FALSE_ACCEPT<0.05, beats NC4 random-role-subset null p<0.05, with cold vs cached latency/tokens via real Playwright dispatch path (navigation + hash + cache lookup, tiktoken counts) delivering ~2× speedup and ~30% token saving on HIT when selectors exclusively derived.

- **H3_WEBGYM_DIVERSE (confirmatory):** WebGym 300k-task async corpus (>=50 diverse eTLD+1 hosts, stratified deterministic seed 35725763380, manifest sha256) yields duplication prevalence 95% CI (2000 family-level bootstrap) distinct from hardcoded WebArena-Verified v2 single-store duplication 0.9479 CI[0.9167,0.9792] (192 tasks 49 templates 36 families) and corpus-level deduplication threshold sweep range ≥0.05 across 0.818–0.9479, plus parameterization prevalence near 0.8958 computable without exhaustive 567MB LFS, proving distribution diversity matters more than hierarchical depth.

- **H4_GATE0_RELAXED (descriptive pilot, not confirmatory physics claim):** Multi-step trajectories ≥50 transitions/family on ≥10 families yield ≥1 family passing relaxed census (titles≥1 H(S_next|URL,H_K=3)>0.1 NL≥20 singleton<50%) enabling correlated-state physics pilot; strict Gate0 (H>0.2 NL≥50 strata≥10 leakage_validOnly<40%) reported descriptively — 0/10 strict is MEASUREMENT_INVALID insufficient density not falsification or physics closure.

---

## 3. State / action / target representation (frozen)

**State before/after:** URL (full, fragments preserved for hash-SPAs; normalized href vs state_after.url for leakage), document.title, CDP Accessibility.getFullAXTree full tree (600–2000 nodes required, DOM bytes≥2000, sha256 per capture), product-subtree/product-page outerHTML SHA256 via page.content() relevant subtree normalized and stripped of 9 dynamic tokens before hash, DOM bytes sha256. Browser state at 1280×720 via CDP, no scroll initial viewport for AX; multi-step trajectories provide temporal history for Gate0.

**Action representation:** AX node role+name + CSS path + normalized selector (derived from AX+DOM attributes, no synthetic fam_task fallback), action.target_href where present, primitive action type (click/type/navigate) for multi-step.

**Target (derived measurements):**
- M_AX_CONSISTENCY_MEAN = mean longest-prefix consistency over 10 families (per-family score = longest common prefix length / max length of full-tree tokenized pattern, no truncation), family is unit, reported with per-family scores.
- M_AX_DELTA_TRUNCATED = M_AX_FULLTREE - M_AX_TRUNCATED20 on same 20 pages (must be ≥0.20).
- M_AX_BOOTSTRAP_CI_LOWER/UPPER, M_AX_SHUFFLE_P/MEAN/STD/P95, M_AX_PER_FAMILY_VARIANCE.
- M_STAGEHAND_HIT, M_STAGEHAND_MISS, M_FALSE_ACCEPT = HIT rate identical (recomputed SHA+stripping), MISS rate drift (recomputed SHA), false_accept = HIT despite drift.
- M_WEBGYM_DUP_PREVALENCE + 95% CI (2000 bootstrap), M_WEBGYM_THRESHOLD_RANGE, M_WEBGYM_PARAM_PREVALENCE.
- M_GATE0_RELAXED_PASS_COUNT, M_GATE0_STRICT_PASS_COUNT, per-family H, NL, strata, singleton rate, leakage_validOnly, unique_titles, title_entropy.
- Honest cost: sum counters resolve+bind+verify+freshness+browser_steps, tiktoken/provider token counts, cold vs cached latency; no f*6.0 jitter, |rho_shuffled|<0.20 gate.

---

## 4. Sampling policy & unit of analysis

**Population:** WebArena-Verified v2 shopping families (36 families ≥3 tasks, hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30) plus shopping_admin 184-task/42-family superset if <5 product-page families achievable with 36; WebGym 300k diverse sites; BrowserGym families (WebArena shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena).  
**Sampling:** Deterministic seed 35725763380 for ALL random choices: sample 10 families without replacement from 36 INSIDE measurement script (re-derive via `random.Random(35725763380).sample(sorted(families_ge3),10)`, do not hardcode prior [191,180,162,197,153,213,163,137,136,222] without verification), within each family sample 2 distinct tasks. WebGym: stratified sample ≥50 diverse eTLD+1 hosts from 300k corpus seed 35725763380. Multi-step: same 10 families. No post-hoc seed change.  
**Unit:** Family for AX (N=10 families, 20 captures), per-transition for Gate0 PMI/CMI with trajectory-grouped permutation (grouped by trajectory/family not step) to avoid degenerate bootstrap CI[1,1] variance 0 p=1 and singleton strata (require ≥5 per stratum for PMI/CMI else undefined).  
**Exclusions:** Captures with <600 nodes or DOM bytes<2000 or placeholder not expanded → invalid, counts toward <5 families substrate_unavailable, not toward mean. Require genuine docker pull/run with 64-char digest timeout>=300s (or cached tar) + pip list non-empty + placeholder verification.

---

## 5. Holdout & leakage control

- Within-store longest-prefix has no train/test leakage (descriptive consistency), but preprocessing (full-tree grammar + 9 dynamic-token regex) is frozen before capture, not fit on held-out outcome; grammar source file sha256 recomputed live from `research/intel/grammar_fulltree_358885.py` (expected f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a) per audit validity_findings[5].
- Stagehand cache: per-project isolation test (NC5) ensures no cross-project identity leakage; HIT threshold N=2 frozen.
- WebGym: site-label shuffle null (NC6) tests duplication prevalence vs site identity leakage; held-out is eTLD+1 (not task shuffle); manifest sha256 and 2 genuine download attempts captured per audit required_fixes[1] (401 Unauthorized suggests HF auth gating, not permanent unavailability — try HF_TOKEN or WebMall alternative).
- Gate0: trajectory-grouped permutation (grouped by trajectory, not transition) and singleton SA exclusion (≥5 per stratum for H) prevent degenerate p and SHA256-truncated DOM tautology.
- Dynamic-token stripping regex frozen before hash recomputation; not fit on outcome.
- Docker digest validated as 64 hex sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (not 12-hex 3e8cb9b945) with skopeo inspect or docker images --digests; pull requires timeout >=300s for 5.4GB image (prior 90s TimeoutExpired insufficient per handoff) or docker load from cached tar/ghcr mirror.
- Provenance self-hash recomputed at write time excluding self-keys or dropped (fixes stale hash) per audit required_fixes[2].
- Honest cost counters summed (resolve+bind+verify+freshness+browser_steps) with |rho_shuffled|<0.20 gate; no f*6.0 jitter.

---

## 6. Baselines & controls (stable identities for EXECUTE/AUDIT/DIRECTOR)

**Baselines (strong):**
- B-STAGEHAND-VERB — shipped Stagehand ~2×/~30% (must use recomputed SHA+stripping, derived selectors)
- B-RANDOM-AX-SHUFFLE — trajectory-grouped shuffle 1000 perms (primary null)
- B-TRUNCATED-20 — same 20 pages with [:20] truncation + selectors[:20] placeholder (root-cause test, requires ≥0.20 delta)
- B-WEBGYM-HARDCODED-09479 — hardcoded 0.9479 CI[0.9167,0.9792] null
- B-COLD-LLM — cold agent latency/tokens via Stagehand cold path (honest sum-counter economics)
- B-CONSTANT-NULL-05654 — REJECTED 0.5654 (disclosed only, not decision)

**Positive controls:**
- PC1_LIVENESS_1280 — ≥15/20 captures 600–2000 nodes at 1280×720, Docker am1n3e/webarena-verified-shopping resolved to full 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb reachable 3 retries with captured docker pull/run output (64 hex validated, timeout>=300s or cached tar, docker images --digests or skopeo inspect)
- PC2_AX_PRIOR_PRODUCT — ≥1 family discriminates vs degenerate homepage 1.0 with variance>0
- PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC — 3 consecutive identical subtree SHA + selector with dynamic stripping → HIT on 2nd/3rd with per-project isolation (cross-project MISS 0%)
- PC4_WEBGYM_IMPORT_VALID — WebGym import parses ≥50 sites with 2 genuine download attempts captured, manifest sha256, sweep computable
- PC5_SYNTHETIC_PIPELINE — synthetic data pipeline sanity (is_synthetic true, not decision)

**Null controls:**
- NC1_AX_SHUFFLE_TRAJECTORY_GROUPED — permute per-family scores 1000 perms, require p<0.05 and mean+0.20 gap; std 0 → FAIL
- NC2_RANDOM_PATTERN — random family pattern <0.2 expected
- NC3_DOM_DRIFT_RECOMPUTED_DYNAMIC — page.evaluate mutation + SHA recomputed AFTER via page.content()+AX with 9-regex stripping, require MISS≥0.8 false_accept<0.05, verify hash change per family (before_hash vs after_hash)
- NC4_RANDOM_CACHE_ROLE_SUBSET — shuffle HIT/MISS labels 1000 perms ~50%, require true beats p<0.05
- NC5_CROSS_PROJECT_LEAKAGE — cross-project same key must MISS 0%
- NC6_WEBGYM_SHUFFLE — site-label shuffle 1000 perms for duplication (trajectory-grouped)

All perms seed 35725763380; 2000 family-level bootstraps (percentile) for CIs.

---

## 7. Primary metric, expected direction, uncertainty

**Primary:** M_AX_CONSISTENCY_MEAN on N=20 product pages. Expected direction: full-tree + 64-char digest timeout>=300s + stripping mean > truncated mean by ≥0.20 and > shuffle null by >0.20. Secondary: HIT/MISS/false_accept, WebGym duplication CI + sweep, Gate0 relaxed pass count.  
**Uncertainty:** 2000 family-level bootstraps (resample families with replacement, recompute mean) → 95% percentile CI; 1000 trajectory-grouped permutations for p = (1+ count perm≥true)/(1+1000). Report CI lower, variance, delta vs truncated, shuffle mean/std/p95, hash_changed_on_mutation. All CIs trajectory-grouped (family/trajectory), not step-level, to avoid dependence violation. 95% CIs for WebGym duplication via 2000 family-level bootstrap; threshold sweep range computed corpus-level. Honest cost reported with |rho_shuffled|<0.20.

---

## 8. Adequacy & validity gate (pre-outcome)

- Adequacy: ≥10 families (20 trees) captured with 600–2000 nodes, placeholder expanded, full-tree grammar verified no truncation via source-file sha256 live recomputed (f2b5e3bb), SHA256 recomputed AFTER page.content()+AX with 9-regex stripping verified per drift family (hash_changed_on_mutation true), Docker 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb resolved and pull/run captured with timeout>=300s or cached tar, BrowserGym/Playwright pins logged (pip list non-empty, docker pull/run captured). Else MEASUREMENT_INVALID substrate_unavailable (invalid 12-hex vs 64-char noted, 90s insufficient for 5.4GB — prior TimeoutExpired not invalid format proves repairability with >=300s).
- Validity gate: target integrity (no post-state in pre-state, recomputed SHA after mutation with stripping), split integrity (trajectory-grouped permutation, train-only preprocessing), sampling integrity (frozen seed deterministic derived inside script, no hardcoded list without re-derivation), uncertainty integrity (family-level bootstrap, not arbitrary jitter, trajectory-grouped), representation integrity (full-tree not truncated, relevant-subtree not full-page, CDP AX preserved, dynamic-token list disclosed, 64-char digest). Violation → MEASUREMENT_INVALID, no SURVIVES/FALSIFIED.

---

## 9. Decision & falsification / survival rule (frozen ordered evaluation — infrastructure precedence)

1. If <5 families with product pages captured (<10 valid trees) after 3 Docker 64-char digest-resolution retries with timeout>=300s (or cached tar load) + grammar verification (no truncation + 9-regex stripping + source-file hash live recomputed) + placeholder fix → status COMPLETE outcome NOT_APPLICABLE, H1=MEASUREMENT_INVALID substrate_unavailable (publish provenance: resolved 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb or registry API failure evidence with captured output, grammar hash f2b5e3bb, dynamic-token regex, pip list hash, docker pull/run output including timeout). Same for WebGym <50 sites (H3 branch) or multi-step <5 families ≥50 transitions (H4 branch) → branch MEASUREMENT_INVALID only (does not invalidate other branches). Prior invalid 12-hex digest 3e8cb9b945 vs full 64-char and prior 90s timeout documented root causes; do not retry 12-hex, use >=300s.

2. Else if captured ≥10 families (20 trees 600–2000 nodes each, placeholder expanded, full-tree without truncation verified, product-subtree SHA recomputed after page.content()+AX with stripping, 64-char digest) and M_AX_CONSISTENCY_MEAN≥0.6 AND bootstrap CI lower>0.5 AND trajectory-grouped shuffle p<0.05 with +0.20 gap AND M_AX_DELTA_TRUNCATED≥0.20 AND PC1≥15/20 AND per-family variance>0 (CI width>0, not degenerate [1.0,1.0]) then H1=SURVIVES (full-tree parameterized transfer identifiable within-store).

3. Else if captured ≥10 families but M_AX_CONSISTENCY_MEAN<0.6 OR CI lower≤0.5 OR p≥0.05 OR delta<0.20 OR variance=0 → H1=FALSIFIED-IN-SETTING bounded to this method/families/page-type (does NOT reject alternative grammars, slot syntax, hierarchical/WebAPI retrieval, or AX semantic similarity).

4. H2_STAGEHAND_RECOMPUTED_DYNAMIC: If <30/36 families attempted or SHA not recomputed after mutation with stripping then H2=MEASUREMENT_INVALID. Else if M_STAGEHAND_HIT≥0.8 AND M_STAGEHAND_MISS≥0.8 AND M_FALSE_ACCEPT<0.05 AND real-path speedup/tokens reported AND beats NC4 p<0.05 AND 0 synthetic fallback AND PC3 isolation 0% → SURVIVES. Else if executed ≥30 but HIT<0.8 or MISS<0.8 or false_accept≥0.05 or NC4 p≥0.05 → FALSIFIED-IN-SETTING bounded to exact-match + stripping construction.

5. H3_WEBGYM_DIVERSE: If <50 sites → MEASUREMENT_INVALID branch. Else if CI non-overlapping 0.9479 CI OR threshold sweep range≥0.05 (0.818–0.9479) → SURVIVES. Else if ≥50 sites but CI overlaps AND range<0.05 → FALSIFIED-IN-SETTING (single-store not distinct).

6. H4_GATE0_RELAXED descriptive: If <5 families ≥50 transitions → MEASUREMENT_INVALID Gate0 branch. Else if ≥1 relaxed pass (H>0.1 NL≥20 titles≥1 singleton<50%) → SURVIVES pilot feasibility; 0/10 relaxed with adequate NL density (≥50 transitions/family, H computable with ≥5/stratum) → FALSIFIED-IN-SETTING for relaxed pilot on this site mix (insufficient density, not physics closure). 0/10 strict is MEASUREMENT_INVALID not global falsification per Director SUPERSEDE.

Overall outcome: SUPPORTS if H1 and H2 SURVIVE, MIXED if split, FALSIFIES if both H1 and H2 falsified, INCONCLUSIVE if H1 MEASUREMENT_INVALID; CAP/LFS exhaustive ABANDONED per Director SUPERSEDE not attempted. Trajectory-grouped bootstrap/permutation throughout; degenerate CI[1,1] p=1.0 flagged invalid. Honest cost gate |rho_shuffled|<0.20 enforced.

---

## 10. Inherited carry-forward (exact preservation from EXP-INTEL-35892848544 handoff sha fc9913b2 — Director SUPERSEDE disposition)

This handoff is continuity evidence only per AGENTS.md. Director mandate SUPERSEDE with cognitive_reset takes precedence; its `next_question` is advisory. Four-way distinction preserved verbatim:

**Established (8 items):**
- Full 64-char Docker digest for am1n3e/webarena-verified-shopping resolved and validated: sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb via Docker Hub API 200 + skopeo inspect rc=0 (8 layers 5.4GB). Truncated 12-hex sha256:3e8cb9b945 is true prefix but structurally invalid for by-digest pull (rc=1 invalid reference format). Provenance independently re-fetched by audit.
- Infrastructure-precedence and null-discipline correctly applied: 0/20 valid AX trees after 3 HTTP probes Connection refused despite registry success, genuine docker pull TimeoutExpired 90s (not invalid format) + truncated invalid + tag pull timeout 30s — producer returned null (not 0.0) for M_AX_CONSISTENCY_MEAN etc and correctly did NOT execute bootstrap/shuffle on empty data, avoiding degenerate CI[1,1] p=1.0 tautology.
- WebArena-Verified v2 census pin independently recomputed: 812 total tasks, 192 shopping tasks, 49 intent_templates, 36 families >=3, duplication 0.9479 95% CI [0.9167,0.9792], hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30.
- Full-tree semantic/multi-anchor grammar provenance: research/intel/grammar_fulltree_358885.py hash f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a (no [:20] slice, 9 dynamic-token regexes, placeholder expansion). Implemented but not yet exercised on live AX trees 600-2000 nodes.
- Stagehand recomputed+stripping logic frozen but not exercised live: 0/36 families attempted, HIT/MISS null.
- WebGym 401 gating independently reproduced: 2 genuine urllib downloads (401/404) satisfying frozen 2-attempt clause; 0 sites null duplication.
- Gate0 multi-step insufficient density correctly classified: 0 transitions vs >=50 required, BrowserGym absent, Docker pull timeout — MEASUREMENT_INVALID insufficient density.
- Freeze integrity verified: request/spec/prereg hashes match freeze.json exactly; audit PASS confirms.

**Rejected (bounded, not global; 0 new this run):**
- No new bounded rejections in this run — 0/20 valid captures prevents SURVIVES/FALSIFIED evaluation. Prior bounded rejections preserved: (1) full DOM SHA256 + exact selector HIT>=0.8, (2) homepage-dominated AX_consistency mean 0.8 degenerate p=1.0, (3) truncated [:20] grammar, (4) WebArena single-store as cross-site testbed vacuous — none closed globally.

**Unknown (this experiment tests; 9 items):**
- H1_AX_FULLTREE whether full-tree achieves mean>=0.6 CI lower>0.5 p<0.05 delta>=0.20 vs truncated variance>0 — requires Docker live 20 captures timeout>=300s with 600-2000 nodes.
- H2_STAGEHAND_RECOMPUTED_DYNAMIC whether recomputed+stripping achieves HIT>=0.8 MISS>=0.8 false_accept<0.05 beats NC4.
- H3_WEBGYM_DIVERSE whether 50 diverse eTLD+1 sites yield duplication CI distinct from 0.9479 and sweep range>=0.05 — requires HF_TOKEN or WebMall alternative.
- H4_GATE0_RELAXED whether multi-step >=50 transitions/family on >=10 families at 1280x720 computes H>0.1 NL>=20 relaxed Gate0.
- Whether shopping_admin 184/42 expansion yields >=5 product-page families where 36-family sample scarce after Docker repair.
- Whether product-subtree anchoring isolates distinct product boundary — grammar f2b5e3bb not validated live.
- Whether alternative representations could yield transfer where longest-prefix fails — bounded falsification does not close orthogonal mechanisms.
- Full 64-char Docker digest pull completion on GH runner with timeout>=300s or cached tar — requires verification.
- WebGym manifest canonical acquisition path — HF_TOKEN-gated vs verified WebMall URL.

**Do_not_assume (13 prohibitions preserved verbatim):**
- Do NOT assume 0/20 valid captures is evidence transfer impossible — it is MEASUREMENT_INVALID transient substrate_unavailable plus 90s timeout insufficient for 5.4GB (not digest invalid after fix), prior 20/20 live proof proves repairability with >=300s or cached tar.
- Do NOT assume mean null equals degenerate 0.8 CI[1,1] p=1.0 — this run correctly returns null not binary.
- Do NOT assume full-tree provides gain over truncated — delta null not 0.0 because no live pages.
- Do NOT assume Stagehand full-DOM HIT 0.0 proves impossible — recomputed relevant-subtree remains untested live.
- Do NOT assume Gate0 0/10 relaxed is global physics closure — insufficient density.
- Do NOT assume WebGym 401 means permanent unavailability without HF token.
- Do NOT assume within-store 1.0 implies cross-site transfer — single Magento store, cross-site requires multi-store.
- Do NOT assume infrastructure live equals scientific success — adequacy gates must still pass.
- Do NOT assume product economics ~2x/~30% validated — null not measured.
- Do NOT re-trigger exhaustive 567MB LFS test.zip or 420-task CAP enumeration — ABANDONED per Director SUPERSEDE.
- Do NOT assume hardcoded sampled_families equals true seeded draw without re-derivation.
- Do NOT assume truncated digest pullable — genuine capture proves invalid format; do not assume 90s sufficient for 5.4GB.
- Do NOT assume pip list proves BrowserGym installed — version fields are pins not installed states.

---

## 11. Product consequences

**Positive (SURVIVES):** H1 SURVIVES (full-tree+64-char digest timeout>=300s+stripping mean≥0.6 CI lower>0.5 p<0.05 vs shuffle delta≥0.20 vs truncated variance>0 PC1≥15/20) gives first measurement-valid within-store parameterized transfer signal superseding homepage tautology. Enables bounded C-CROSSSITE within-store holdout and informs C-LLM-INHERIT economics. H2 SURVIVES gives competitive floor ~2x/~30% for C-PRODUCT-ECON honest economics. H3 SURVIVES proves diversity effect without exhaustive LFS/CAP. H4 ≥1 relaxed Gate0 pass unlocks physics pilot. Artifacts reusable substrate.

**Negative (FALSIFIED or MEASUREMENT_INVALID):** H1 FALSIFIED (≥10 families but mean<0.6 or CI lower≤0.5 or p≥0.05 or delta<0.20) → full-tree longest-prefix insufficient, requires slot syntax or hierarchical/WebAPI retrieval; C-CROSSSITE stays HYPOTHESIS single-store vacuous. H2 FALSIFIED (≥30 executed but HIT<0.8 or MISS<0.8 or false_accept≥0.05) → exact cache not discriminating even with stripping. Any MEASUREMENT_INVALID (<5 families, <50 sites, <5 multi-step) → no falsification, repair Docker (timeout>=300s/cached tar/ghcr mirror) or WebGym (HF_TOKEN) before claiming impossibility; exhaustive CAP/LFS not re-triggered per SUPERSEDE. H3 FALSIFIED duplication overlaps 0.9479 — not cross-site evidence.

---

## 12. Cost & information gain

**Cost:** LOW-MEDIUM, no LLM inference for AX/Gate0/WebGym; ~3–4h wall-clock, <15GB /tmp, stdlib+playwright+browsergym/agentlab+tiktoken. Docker pull 64-char digest 5.4GB timeout>=300s (`timeout 600 docker pull ...@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb`) or cached tar + BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 Chromium (~300MB). Reuse WebArena census hash d65275... for pin.

**Expected information gain:** MAXIMUM per Director PIVOT comparative reasoning — directly repairs 6 root-cause blockers (64-char digest with timeout>=300s/cached tar, truncation degenerate p=1.0, SHA not recomputed + stripping, singleton strata, pip freeze empty + stale self-hash, 401 gating) with deterministic fixes delivering falsifiable variance>0 transfer proof or bounded rejection (delta≥0.20), re-derives Stagehand with hash-after-mutation+stripping competitive floor informing per-hit vs fixed at f=100 honest economics, WebGym diverse import tests diversity>depth without LFS, multi-step relaxed Gate0 H>0.1 NL≥20 unlocks physics pilot. Either SURVIVES unlocks product within-store holdout + WebGym cross-site baseline + physics pilot, or FALSIFIED-IN-SETTING redirects product to hierarchical retrieval and avoids blocked exhaustive path — highest global leverage vs local retrieval tuning (closed). Falsifiability: 5 Director agent priors are priors to be tested, not assumed evidence.

---

## 13. Preregistration freeze

Hypothesis, state/action representation (including 9-regex stripping, full 64-char digest timeout>=300s resolution, honest sum-counter cost), sampling policy (seed 35725763380 derived inside script), holdout/leakage controls, baselines/nulls/positive controls, primary metric, expected direction, uncertainty method (2000 family bootstrap, 1000 trajectory-grouped permutations, |rho_shuffled|<0.20 gate), adequacy rule, and falsification/survival rule frozen before any outcome-bearing measurement on this experiment_id. Any analysis change after seeing outcomes is exploratory; new confirmatory claim requires new preregistration and untouched evidence. Raw artifacts preserved with sha256 per spec.json §measurement_validity; report.md may interpret but not contradict result.json or exceed frozen claim. CAP/LFS exhaustive enumeration explicitly ABANDONED and not attempted; 0/10 strict Gate0 remains MEASUREMENT_INVALID not falsification. Pinned versions: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, tiktoken, Docker digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb.

