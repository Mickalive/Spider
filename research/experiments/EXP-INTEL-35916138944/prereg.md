# EXP-INTEL-35916138944 preregistration — Intel REOPEN C-CROSSSITE (SUPERSEDE, cognitive_reset)

**Lane:** intel — `research/intel` only (no cross-lane writes)  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout (registry HYPOTHESIS); auxiliary gates C-MEAS-VALID, C-WEB-DYNAMICS (Gate0), C-PRODUCT-ECON (Stagehand economics), C-WEB-DYNAMICS Frontier compilation via WebMCP prevalence reported descriptively  
**Director mandate:** REOPEN, cognitive_reset true, parent_handoff_disposition SUPERSEDE (EXP-INTEL-35903200136 MIXED H1/H2 FALSIFIED-IN-SETTING bounded to homepage/template + unstable SHA, H3/H4 MEASUREMENT_INVALID). Target pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, full-tree semantic/multi-anchor without truncation plus 9 base regex + expanded Magento form_key/uenc/store/session/timestamp/nonce stripping, WebGym 292k (292k tasks 127k sites 2026) + Mind2Web-2 130-task Agent-as-Judge diverse holdout >=50 eTLD+1, multi-step >=50 transitions/family >=10 families, full 64-char Docker digest via registry API/skopeo with timeout >=300s or cached tar, WebMCP prevalence. Dependencies: [] per request.json.  
**Inherited state consumed:** Read `research/experiments/EXP-INTEL-35903200136/handoff.json` sha 77d51f20b5f9bff3a25c528f08ae0e22ab8ce5f20b3daa79daa8fb1dc41c05ba; preserved established/rejected/unknown/do_not_assume verbatim in §10. This NEW governed experiment follows the Director's strategic question (REOPEN C-CROSSSITE pinned WebGym 292k + Mind2Web-2 replacing exhaustive 567MB LFS 420-task CAP), not the parent handoff's `next_question` which is advisory continuity only per AGENTS.md global direction discipline and request.json director_mandate SUPERSEDE. No outcome-bearing measurement run during DESIGN. Verifies degenerate homepage/template variance and SHA instability blocking within-store transfer.

**Agent priors (Director, distinguished from SPIDER evidence — testable, not assumed):** (1) Path dependence/salience trap — 0.9479 duplication and 1.0 verbatim false_accept demonstrates salience trap requiring correct-family gating and calibrated UNKNOWN before measuring economics, distinguished from SPIDER evidence falsified per_hit at f=10; (2) Calibrate-Then-Act — exploration cost tracks residual uncertainty not task length, rho_novelty requires hitRate 0.3-0.6 and ECE<=0.15 before separable; (3) Compounding planning errors cause long-horizon failure — 0/10 mixed triple-channel joint failure as composition not ranking problem, motivates joint multi-candidate test; (4) Workflow compilation O(1) only when frequency f honestly high and endpoint catalog covers task paths, f=10 insufficient, requires f=100 and Docker BrowserGym 2000-node replication; (5) Local optima trap — 7 consecutive MEASUREMENT_INVALID with single-prefix/Jaccard tweaks without escaping basin, Frontier required orthogonal mechanism. Priors justify orthogonal alias families and calibration gates, not presented as Web observations.

---

## 1. Strategic question (Director binding) → falsifiable experiment

**Director question (binding, from request.json director_mandate.question):** Can pinned WebGym 292k (292k tasks 127k sites 2026) + Mind2Web-2 130-task Agent-as-Judge replace exhaustive 567MB LFS 567.7MB test.zip / CAP 420-task 108-site enumeration: (a) sample >=50 eTLD+1 diverse sites from WebGym 300k manifest for duplication 95% CI (2000 bootstrap) and threshold sweep 0.818-0.9479 plus parameterization prevalence vs vacuous 0.9479 single-store, (b) relaxed Gate0 census H>0.1 NL>=20 titles>=1 via BrowserGym 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 1280x720 multi-step trajectories >=50 transitions/family on >=10 families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) with cold vs cached latency/tokens, (c) full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, product-subtree SHA256 recomputed via page.content()+CDP Accessibility.getFullAXTree with dynamic-token stripping) at 1280x720 with 20 live CDP captures task-specific start_url 10 families x2 seed 35725763380 requiring mean>=0.6 bootstrap lower>0.5 shuffle p<0.05 delta>=0.20 vs truncated, and (d) Stagehand selector+relevant-subtree SHA256 HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 random-role-subset null, plus WebMCP tool registration prevalence across top WebGym sites, all trajectory-grouped 2000 bootstrap CIs and pinned 64-char Docker digest am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb?

**Smallest high-information translation (this prereg):** Narrow repaired pilot on WebArena-Verified v2 shopping product pages (10 families ×2 tasks =20 CDP captures at 1280x720 with 64-char digest resolution timeout>=300s + expanded dynamic stripping) + Stagehand recomputed replication on 36 families (derived selectors only, SHA recomputed after mutation + expanded stripping, real-path latency/tokens) + WebGym 292k 50-site diverse census (2000 bootstrap CI + threshold sweep) + Mind2Web-2 130-task Judge fallback + 10-family multi-step rollout (strive 50 transitions each, BrowserGym-core 0.14.3 primary with Playwright fallback) + WebMCP prevalence scan. Any narrower (single metric) would leave Stagehand floor or WebGym diversity or WebMCP leverage untested; any broader (exhaustive LFS 567MB test.zip / CAP 420-task) repeats blocked path with zero marginal gain per Director comparative reasoning: vs CONTINUE exhaustive LFS 567MB/CAP 420-task enumeration that produced 0/3 qualified SPAs after exhaustive BrowserGym/CAP/Mind2Web-2 enumeration and is MEASUREMENT_INVALID substrate_unavailable, marginal value near zero, pinned WebGym/Mind2Web-2 diverse sampling has higher leverage and external validity. Already-frozen experiments resume independently; pre-freeze work is superseded per mandate.

---

## 2. Hypotheses (confirmatory)

- **H1_AX_FULLTREE (primary, confirmatory):** Full-tree semantic/multi-anchor without truncation (complete CDP Accessibility.getFullAXTree traversal from root, product-specific subtree anchored on heading/price/add-to-cart/main/contentinfo boundaries, role+name+CSS path + subtree outerHTML SHA256 normalized by stripping 9 base dynamic-token regexes [csrf[_-]?token, session[_-]?id, _token, timestamp, nonce, csrf value, sessionId, \b\d{13}\b, \b[a-f0-9]{32,}\b] plus expanded Magento form_key/uenc/store/session/timestamp/nonce HTML-attribute stripping before hash, no token truncation, longest_prefix_without_fallback and sha256_normalized_subtree with expanded stripping but not yet exercised on live product-page trees) yields discriminating within-store AX_consistency on N=20 live product-page captures with M_AX_CONSISTENCY_MEAN≥0.6, 2000 family-level bootstrap 95% CI lower>0.5, trajectory-grouped permutation 1000 p<0.05 vs NC1 (>0.20 above null mean/p95), M_AX_DELTA_TRUNCATED≥0.20 vs truncated [:20] baseline on same pages, M_AX_PER_FAMILY_VARIANCE>0 (CI width>0, not degenerate [1.0,1.0] homepage tautology with p=1.0), product-subtree node counts>1 distinct hashes on path families 136,145,196,222. Requires 600-2000 AX nodes per capture, DOM bytes≥2000, full 64-char Docker digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb resolved with timeout>=300s or cached tar.

- **H2_STAGEHAND_RECOMPUTED_DYNAMIC (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (exact normalized selector from AX+DOM + SHA256 of relevant subtree outerHTML recomputed AFTER mutation via page.content()+AX Accessibility.getFullAXTree via page.evaluate, HIT after N=2 identical results, per-project isolation, 0 synthetic fam_task fallback, 9+expanded dynamic stripping before hash) reports M_STAGEHAND_HIT≥0.8 on identical DOM, M_STAGEHAND_MISS≥0.8 on single-attribute drifted DOM (page.evaluate mutation, hash recomputed after), M_FALSE_ACCEPT<0.05, beats NC4 random-role-subset null p<0.05, with cold vs cached latency/tokens via real Playwright dispatch path (navigation + hash + cache lookup, tiktoken counts) delivering ~2× speedup and ~30% token saving on HIT when selectors exclusively derived.

- **H3_WEBGYM_DIVERSE (confirmatory):** WebGym 292k-task async corpus (>=50 diverse eTLD+1 hosts, stratified deterministic seed 35725763380, manifest sha256, 292k tasks 127k sites) plus Mind2Web-2 130-task Agent-as-Judge alternative yields duplication prevalence 95% CI (2000 family-level bootstrap) distinct from hardcoded WebArena-Verified v2 single-store duplication 0.9479 CI[0.9167,0.9792] (192 tasks 49 templates 36 families) and corpus-level deduplication threshold sweep range ≥0.05 across 0.818–0.9479, plus parameterization prevalence near 0.8958 computable without exhaustive 567MB LFS, proving distribution diversity matters more than hierarchical depth.

- **H4_GATE0_RELAXED (descriptive pilot, not confirmatory physics claim):** Multi-step trajectories ≥50 transitions/family on ≥10 families yield ≥1 family passing relaxed census (titles≥1 H(S_next|URL,H_K=3)>0.1 NL≥20 singleton<50%) enabling correlated-state physics pilot; strict Gate0 (H>0.2 NL≥50 strata≥10 leakage_validOnly<40%) reported descriptively — 0/10 strict is MEASUREMENT_INVALID insufficient density not falsification or physics closure.

- **H5_WEBMCP_PREVALENCE (descriptive):** WebMCP tool registration prevalence across top WebGym sites and Mind2Web-2 catalog informs frontier compilation bet — O(1) amortized lookup only when frequency f honestly high (f=100) and endpoint catalog covers task paths; prevalence at f=10 vs f=100 reported with 2000 bootstrap CIs, no survival gate but informs product f=100 vs f=10 Pareto.

---

## 3. State / action / target representation (frozen)

**State before/after:** URL (full, fragments preserved for hash-SPAs; normalized href vs state_after.url for leakage), document.title, CDP Accessibility.getFullAXTree full tree (600–2000 nodes required, DOM bytes≥2000, sha256 per capture), product-subtree/product-page outerHTML SHA256 via page.content() relevant subtree normalized and stripped of 9+expanded dynamic tokens before hash, DOM bytes sha256. Browser state at 1280×720 via CDP, no scroll initial viewport for AX; multi-step trajectories provide temporal history for Gate0.

**Action representation:** AX node role+name + CSS path + normalized selector (derived from AX+DOM attributes, no synthetic fam_task fallback), action.target_href where present, primitive action type (click/type/navigate) for multi-step. WebMCP tool registration as action catalog entry.

**Target (derived measurements):**
- M_AX_CONSISTENCY_MEAN = mean longest-prefix consistency over 10 families (per-family score = longest common prefix length / max length of full-tree tokenized pattern, no truncation), family is unit, reported with per-family scores.
- M_AX_DELTA_TRUNCATED = M_AX_FULLTREE - M_AX_TRUNCATED20 on same 20 pages (must be ≥0.20).
- M_AX_BOOTSTRAP_CI_LOWER/UPPER, M_AX_SHUFFLE_P/MEAN/STD/P95, M_AX_PER_FAMILY_VARIANCE.
- M_STAGEHAND_HIT, M_STAGEHAND_MISS, M_FALSE_ACCEPT = HIT rate identical (recomputed SHA+expanded stripping), MISS rate drift (recomputed SHA), false_accept = HIT despite drift.
- M_WEBGYM_DUP_PREVALENCE + 95% CI (2000 bootstrap), M_WEBGYM_THRESHOLD_RANGE, M_WEBGYM_PARAM_PREVALENCE, M_WEBGYM_SITE_ENTROPY.
- M_GATE0_RELAXED_PASS_COUNT, M_GATE0_STRICT_PASS_COUNT, per-family H, NL, strata, singleton rate, leakage_validOnly, unique_titles, title_entropy.
- M_WEBMCP_PREVALENCE_F10, M_WEBMCP_PREVALENCE_F100, tool coverage per site.
- Honest cost: sum counters resolve+bind+verify+freshness+browser_steps, tiktoken/provider token counts, cold vs cached latency; no f*6.0 jitter, |rho_shuffled|<0.20 gate.

---

## 4. Sampling policy & unit of analysis

**Population:** WebArena-Verified v2 shopping families (36 families ≥3 tasks, hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30) plus shopping_admin 184-task/42-family superset if <5 product-page families achievable with 36; WebGym 292k diverse sites (292k tasks 127k sites); Mind2Web-2 130 tasks; BrowserGym families (WebArena shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena).  
**Sampling:** Deterministic seed 35725763380 for ALL random choices: sample 10 families without replacement from 36 INSIDE measurement script (re-derive via `random.Random(35725763380).sample(sorted(families_ge3),10)`, do not hardcode prior [191,180,162,197,153,213,163,137,136,222] without verification), within each family sample 2 distinct tasks. WebGym: stratified sample ≥50 diverse eTLD+1 hosts from 292k corpus seed 35725763380; Mind2Web-2 130-task census. Multi-step: same 10 families. WebMCP: top WebGym sites. No post-hoc seed change.  
**Unit:** Family for AX (N=10 families, 20 captures), per-transition for Gate0 PMI/CMI with trajectory-grouped permutation (grouped by trajectory/family not step) to avoid degenerate bootstrap CI[1,1] variance 0 p=1 and singleton strata (require ≥5 per stratum for PMI/CMI else undefined). WebGym site is unit for duplication bootstrap.  
**Exclusions:** Captures with <600 nodes or DOM bytes<2000 or placeholder not expanded → invalid, counts toward <5 families substrate_unavailable, not toward mean. Require genuine docker pull/run with 64-char digest timeout>=300s (or cached tar) + pip list non-empty + placeholder verification. WebMCP requires catalog parse success.

---

## 5. Holdout & leakage control

- Within-store longest-prefix has no train/test leakage (descriptive consistency), but preprocessing (full-tree grammar + 9+expanded dynamic-token regex) is frozen before capture, not fit on held-out outcome; grammar source file sha256 recomputed live from `research/intel/grammar_fulltree_358885.py` per audit validity_findings.
- Stagehand cache: per-project isolation test (NC5) ensures no cross-project identity leakage; HIT threshold N=2 frozen.
- WebGym: site-label shuffle null (NC6) tests duplication prevalence vs site identity leakage; held-out is eTLD+1 (not task shuffle); manifest sha256 and 2 genuine download attempts captured per audit required_fixes (401 Unauthorized suggests HF auth gating, not permanent unavailability — try HF_TOKEN or WebMall alternative or Mind2Web-2 fallback).
- Gate0: trajectory-grouped permutation (grouped by trajectory, not transition) and singleton SA exclusion (≥5 per stratum for H) prevent degenerate p and SHA256-truncated DOM tautology.
- Dynamic-token stripping regex frozen before hash recomputation; not fit on outcome; expanded attributes disclosed before capture.
- Docker digest validated as 64 hex sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (not 12-hex 3e8cb9b945) with skopeo inspect or docker images --digests; pull requires timeout >=300s for 5.4GB image (prior 90s TimeoutExpired insufficient per handoff) or docker load from cached tar/ghcr mirror.
- Provenance self-hash recomputed at write time excluding self-keys or dropped (fixes stale hash) per audit required_fixes.
- Honest cost counters summed (resolve+bind+verify+freshness+browser_steps) with |rho_shuffled|<0.20 gate; no f*6.0 jitter.
- Mind2Web-2 Judge labels are held-out from WebGym sampling; no cross-contamination.

---

## 6. Baselines & controls (stable identities for EXECUTE/AUDIT/DIRECTOR)

**Baselines (strong):**
- B-STAGEHAND-VERB — shipped Stagehand ~2×/~30% (must use recomputed SHA+expanded stripping, derived selectors)
- B-RANDOM-AX-SHUFFLE — trajectory-grouped shuffle 1000 perms (primary null)
- B-TRUNCATED-20 — same 20 pages with [:20] truncation + selectors[:20] placeholder (root-cause test, requires ≥0.20 delta)
- B-WEBGYM-HARDCODED-09479 — hardcoded 0.9479 CI[0.9167,0.9792] null
- B-COLD-LLM — cold agent latency/tokens via Stagehand cold path (honest sum-counter economics)
- B-MIND2WEB2-JUDGE — Mind2Web-2 130-task diverse holdout alternative
- B-WEBMCP-TOOL-PREV — WebMCP tool registration prevalence at f=10 vs f=100
- B-CONSTANT-NULL-05654 — REJECTED 0.5654 (disclosed only, not decision)

**Positive controls:**
- PC1_LIVENESS_1280 — ≥15/20 captures 600–2000 nodes at 1280×720, Docker am1n3e/webarena-verified-shopping resolved to full 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb reachable 3 retries with captured docker pull/run output (64 hex validated, timeout>=300s or cached tar, docker images --digests or skopeo inspect)
- PC2_AX_PRIOR_PRODUCT — ≥1 family discriminates vs degenerate homepage 1.0 with variance>0
- PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC — 3 consecutive identical subtree SHA + selector with expanded stripping → HIT on 2nd/3rd with per-project isolation (cross-project MISS 0%)
- PC4_WEBGYM_IMPORT_VALID — WebGym 292k import parses ≥50 sites with 2 genuine download attempts captured, manifest sha256, sweep computable; Mind2Web-2 fallback
- PC5_SYNTHETIC_PIPELINE — synthetic data pipeline sanity (is_synthetic true, not decision)
- PC6_WEBMCP_DETECT — WebMCP prevalence pipeline detects tool registrations on >=1 top site

**Null controls:**
- NC1_AX_SHUFFLE_TRAJECTORY_GROUPED — permute per-family scores 1000 perms, require p<0.05 and mean+0.20 gap; std 0 → FAIL
- NC2_RANDOM_PATTERN — random family pattern <0.2 expected
- NC3_DOM_DRIFT_RECOMPUTED_DYNAMIC — page.evaluate mutation + SHA recomputed AFTER via page.content()+AX with 9+expanded stripping, require MISS≥0.8 false_accept<0.05, verify hash change per family (before_hash vs after_hash)
- NC4_RANDOM_CACHE_ROLE_SUBSET — shuffle HIT/MISS labels 1000 perms ~50%, require true beats p<0.05
- NC5_CROSS_PROJECT_LEAKAGE — cross-project same key must MISS 0%
- NC6_WEBGYM_SHUFFLE — site-label shuffle 1000 perms for duplication (trajectory-grouped)
- NC7_WEBMCP_RANDOM — random endpoint assignment null for WebMCP prevalence

All perms seed 35725763380; 2000 family-level bootstraps (percentile) for CIs.

---

## 7. Primary metric, expected direction, uncertainty

**Primary:** M_AX_CONSISTENCY_MEAN on N=20 product pages. Expected direction: full-tree + 64-char digest timeout>=300s + expanded stripping mean > truncated mean by ≥0.20 and > shuffle null by >0.20. Secondary: HIT/MISS/false_accept, WebGym duplication CI + sweep, Gate0 relaxed pass count, WebMCP prevalence.  
**Uncertainty:** 2000 family-level bootstraps (resample families with replacement, recompute mean) → 95% percentile CI; 1000 trajectory-grouped permutations for p = (1+ count perm≥true)/(1+1000). Report CI lower, variance, delta vs truncated, shuffle mean/std/p95, hash_changed_on_mutation. All CIs trajectory-grouped (family/trajectory), not step-level, to avoid dependence violation. 95% CIs for WebGym duplication and WebMCP prevalence via 2000 family/site-level bootstrap; threshold sweep range computed corpus-level. Honest cost reported with |rho_shuffled|<0.20.

---

## 8. Adequacy & validity gate (pre-outcome)

- Adequacy: ≥10 families (20 trees) captured with 600–2000 nodes, placeholder expanded, full-tree grammar verified no truncation via source-file sha256 live recomputed, SHA256 recomputed AFTER page.content()+AX with 9+expanded stripping verified per drift family (hash_changed_on_mutation true), Docker 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb resolved and pull/run captured with timeout>=300s or cached tar, BrowserGym/Playwright pins logged (pip list non-empty, docker pull/run captured). Else MEASUREMENT_INVALID substrate_unavailable (12-hex vs 64-char noted, 90s insufficient for 5.4GB — prior TimeoutExpired not invalid format proves repairability with >=300s). WebMCP requires catalog parse; else descriptive only.
- Validity gate: target integrity (no post-state in pre-state, recomputed SHA after mutation with expanded stripping), split integrity (trajectory-grouped permutation, train-only preprocessing), sampling integrity (frozen seed deterministic derived inside script, no hardcoded list without re-derivation), uncertainty integrity (family-level bootstrap, not arbitrary jitter, trajectory-grouped), representation integrity (full-tree not truncated, relevant-subtree not full-page, CDP AX preserved, dynamic-token list disclosed, 64-char digest). Violation → MEASUREMENT_INVALID, no SURVIVES/FALSIFIED.

---

## 9. Decision & falsification / survival rule (frozen ordered evaluation — infrastructure precedence)

1. If <5 families with product pages captured (<10 valid trees) after 3 Docker 64-char digest-resolution retries with timeout>=300s (or cached tar load) + grammar verification (no truncation + 9+expanded stripping + source-file hash live recomputed) + placeholder fix → status COMPLETE outcome NOT_APPLICABLE, H1=MEASUREMENT_INVALID substrate_unavailable (publish provenance: resolved 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb or registry API failure evidence with captured output, grammar hash, dynamic-token regex, pip list hash, docker pull/run output including timeout). Same for WebGym <50 sites (H3 branch) or multi-step <5 families ≥50 transitions (H4 branch) → branch MEASUREMENT_INVALID only (does not invalidate other branches). Prior 12-hex digest 3e8cb9b945 vs full 64-char and prior 90s timeout documented root causes; do not retry 12-hex, use >=300s. Mind2Web-2 attempted before declaring H3 invalid.

2. Else if captured ≥10 families (20 trees 600–2000 nodes each, placeholder expanded, full-tree without truncation verified, product-subtree SHA recomputed after page.content()+AX with expanded stripping, 64-char digest) and M_AX_CONSISTENCY_MEAN≥0.6 AND bootstrap CI lower>0.5 AND trajectory-grouped shuffle p<0.05 with +0.20 gap AND M_AX_DELTA_TRUNCATED≥0.20 AND PC1≥15/20 AND per-family variance>0 (CI width>0, not degenerate [1.0,1.0]) then H1=SURVIVES (full-tree parameterized transfer identifiable within-store).

3. Else if captured ≥10 families but M_AX_CONSISTENCY_MEAN<0.6 OR CI lower≤0.5 OR p≥0.05 OR delta<0.20 OR variance=0 → H1=FALSIFIED-IN-SETTING bounded to this method/families/page-type (does NOT reject alternative grammars, slot syntax, hierarchical/WebAPI retrieval, or AX semantic similarity).

4. H2_STAGEHAND_RECOMPUTED_DYNAMIC: If <30/36 families attempted or SHA not recomputed after mutation with expanded stripping then H2=MEASUREMENT_INVALID. Else if M_STAGEHAND_HIT≥0.8 AND M_STAGEHAND_MISS≥0.8 AND M_FALSE_ACCEPT<0.05 AND real-path speedup/tokens reported AND beats NC4 p<0.05 AND 0 synthetic fallback AND PC3 isolation 0% → SURVIVES. Else if executed ≥30 but HIT<0.8 or MISS<0.8 or false_accept≥0.05 or NC4 p≥0.05 → FALSIFIED-IN-SETTING bounded to exact-match + expanded stripping construction.

5. H3_WEBGYM_DIVERSE: If <50 sites (after WebGym + Mind2Web-2 attempts) → MEASUREMENT_INVALID branch. Else if CI non-overlapping 0.9479 CI OR threshold sweep range≥0.05 (0.818–0.9479) → SURVIVES. Else if ≥50 sites but CI overlaps AND range<0.05 → FALSIFIED-IN-SETTING (single-store not distinct).

6. H4_GATE0_RELAXED descriptive: If <5 families ≥50 transitions → MEASUREMENT_INVALID Gate0 branch. Else if ≥1 relaxed pass (H>0.1 NL≥20 titles≥1 singleton<50%) → SURVIVES pilot feasibility; 0/10 relaxed with adequate NL density (≥50 transitions/family, H computable with ≥5/stratum) → FALSIFIED-IN-SETTING for relaxed pilot on this site mix (insufficient density, not physics closure). 0/10 strict is MEASUREMENT_INVALID not global falsification per Director SUPERSEDE.

7. H5_WEBMCP_PREVALENCE descriptive: no SURVIVES/FALSIFIED gate; prevalence at f=10 vs f=100 reported with CIs informs frontier compilation bet.

Overall outcome: SUPPORTS if H1 and H2 SURVIVE, MIXED if split, FALSIFIES if both H1 and H2 falsified, INCONCLUSIVE if H1 MEASUREMENT_INVALID; CAP/LFS exhaustive ABANDONED per Director SUPERSEDE not attempted. Trajectory-grouped bootstrap/permutation throughout; degenerate CI[1,1] p=1.0 flagged invalid. Honest cost gate |rho_shuffled|<0.20 enforced.

---

## 10. Inherited carry-forward (exact preservation from EXP-INTEL-35903200136 handoff sha 77d51f20 — Director SUPERSEDE disposition)

This handoff is continuity evidence only per AGENTS.md. Director mandate SUPERSEDE with cognitive_reset takes precedence; its `next_question` is advisory and its `parent_handoff_disposition: SUPERSEDE` plus `allocation.action: REOPEN` are binding. Four-way distinction preserved verbatim:

**Established (6 items):**
- Docker full 64-char digest am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb validated via docker images --digests / skopeo inspect, container hardcore_northcutt LIVE on port 7770 HTTP 200 at 1280x720, bypassing prior 90s TimeoutExpired blocker — provenance.json + audit V8
- CDP Accessibility.getFullAXTree adequacy achieved: 20/20 valid captures 600-2000 nodes (PC1 PASS) at 1280x720 Playwright 1.44.0, grammar_fulltree_358885.py hash f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a verified no [:20] truncation and 9 dynamic-token regexes present — audit recomputed via hashlib.sha256
- Sampling and reporting integrity on this run: seed 35725763380, 36-family WebArena-Verified v2 census 812 tasks/192 shopping hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30, 20 captures family/task/start_url/viewport/AX_sha/DOM_sha preserved in ax_captures.jsonl, BrowserGym-core 0.14.3 AgentLab 0.4.2 installed per pip list
- H3 WebGym diverse-site and H4 Gate0 multi-step correctly classified MEASUREMENT_INVALID per frozen infrastructure precedence with 2 genuine 401/404 attempts captured (webgym_census.json) and 0 transitions BrowserGym API mismatch (gate0_relaxed_table.json), trajectory-grouped bootstrap/shuffle correctly not executed on empty data avoiding degenerate CI[1,1] p=1.0 — audit V7 info
- Stagehand per-project isolation holds (NC5 PASS, cross-project MISS 0% leakage), selector derivation feasible, but 9-regex stripping insufficient as established by hash instability — marginal established control passes despite H2 falsification
- Exhaustive 567MB LFS test.zip / 420-task CAP enumeration correctly ABANDONED per Director SUPERSEDE, not attempted not falsified — do not re-trigger

**Rejected (bounded, not global; 2 items):**
- Full-tree semantic/multi-anchor longest_prefix_without_fallback + 9-regex stripping REJECTED (FALSIFIED-IN-SETTING bounded) for within-store discriminating AX_consistency on Magento One Stop Market homepage/template at 1280x720: mean 0.9 from family_scores [1.0x9,0.0], bootstrap CI recomputed [0.7,1.0] contains mean but lower not >0.5, shuffle p=1.0 gap 0.0 <0.20, delta_vs_truncated null <0.20 — variance>0 would PASS on recomputed pop 0.09 but degenerate template dominance falsifies this longest-prefix/template signal (audit V1-V4)
- Stagehand exact normalized-selector + relevant-subtree outerHTML SHA256 with 9-regex stripping recomputed after page.content+AX via page.evaluate REJECTED (FALSIFIED-IN-SETTING bounded) on this Magento template: HIT 0.0 <0.8 on 36/36 families, hash_changed_on_every access without mutation (before_hash!=after_hash all families, V6), so MISS 1.0 tautological and false_accept 0.0 vacuous — shipped ~2x/~30% floor not reproduced on this corpus with this stripping (audit V6, baseline_findings B-STAGEHAND-VERB FAIL)
- Rejection is BOUNDED: does NOT reject product-page transfer with proper task-specific start_url sampling (10 distinct product URLs, shopping_admin 184/42 fallback) + product-subtree anchoring, expanded normalization beyond 9 regex, parameterized slot syntax, hierarchical/WebAPI retrieval, or AX semantic similarity; also does NOT reject multi-store cross-site transfer — single-store Magento vacuous 0.9479 remains distinct from diverse-site hypothesis

**Unknown (this experiment tests; 7 items):**
- Whether proper product-page sampling (10/10 families with task-specific __SHOPPING__/path product URLs, not homepage) plus product-subtree isolation (heading/price/add-to-cart/main/contentinfo, role+name+CSS path + subtree outerHTML SHA normalized) yields variance>0, shuffle p<0.05 gap>=0.20, delta_vs_truncated>=0.20 and bootstrap lower>0.5 — requires re-run with get_task_start_url expansion verified and subtree node_count>1 distinct hashes on path families 136/145/196/222 (spec CRITICAL FIX 1/2, unresolved, audit required_fixes 4-5)
- Whether expanded dynamic-token normalization (additional Magento attributes form_key/uenc/store/session/timestamp/nonce, HTML-attribute stripping before outerHTML SHA) stabilizes relevant-subtree SHA to achieve Stagehand HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 random-role-subset with real-path latency/tokens ~2x/~30% on derived selectors only — requires grammar_fulltree_358885.py:strip_dynamic_tokens fix and 36-family re-run with recomputed after mutation
- M_AX_DELTA_TRUNCATED on same 20 product pages vs truncated [:20] baseline — currently null UNKNOWN, required for SURVIVES delta>=0.20 gate
- WebGym 292k diverse-site and Mind2Web-2 130-task duplication 95% CI (2000 family-level bootstrap) and corpus-level dedup threshold sweep range 0.818-0.9479 plus param_task prevalence vs vacuous 0.9479 single-store CI[0.9167,0.9792] — remains 0/50 sites UNKNOWN after 2 genuine 401/404, requires HF_TOKEN or verified WebMall/Mind2Web-2 alternative with manifest sha256
- Gate0 relaxed census H>0.1 NL>=20 titles>=1 singleton<50% and strict H>0.2 NL>=50 strata>=10 leakage_validOnly<40% with BrowserGym multi-step >=50 transitions/family on >=10 families at 1280x720, trajectory-grouped permutation, title_entropy, leakage metrics — remains 0 transitions UNKNOWN due to BrowserGym API structure mismatch
- Whether alternative orthogonal representations where longest-prefix fails (parameterized slot syntax, hierarchical retrieval, WebAPI, AX semantic similarity) yield within-store or cross-site transfer — bounded falsification does not close
- Whether diverse eTLD+1 multi-store WebGym 292k sampling yields cross-site holdout evidence beyond within-store template similarity — requires diverse-site design untouched by prior homepage/template failure
- WebMCP tool registration prevalence across top WebGym sites at honest f=10 vs f=100 — UNKNOWN, informs frontier compilation bet

**Do_not_assume (12 prohibitions preserved verbatim + WebMCP):**
- Do NOT assume homepage/template tautology (18/20 identical 1430-node captures at http://localhost:7770 /) implies product-page transfer impossible — product-page sampling was violated, only family 6 (864/668 nodes) was product-page, spec required 10 families x2 task-specific start_url with shopping_admin fallback; 0/10 strict Gate0 on this site mix would be MEASUREMENT_INVALID insufficient density not physics closure
- Do NOT assume producer M_AX_BOOTSTRAP_CI [1.0,1.0] / M_AX_SHUFFLE_MEAN 1.0 / M_AX_PER_FAMILY_VARIANCE 0.0 are valid — audit recomputed CI [0.7,1.0], shuffle_mean 0.9, pop variance 0.09/sample 0.10 from [1.0x9,0.0]; do NOT ingest producer CI/variance/shuffle until corrected per required_fixes 1-2, degenerate CI does not contain estimate and variance 0 is flag not statistical variance
- Do NOT assume M_AX_DELTA_TRUNCATED measured or that full-tree provides gain over truncated [:20] — delta null UNKNOWN, SURVIVES impossible without delta>=0.20 on same 20 pages (B-TRUNCATED-20 UNKNOWN)
- Do NOT assume Stagehand false_accept 0.0 / MISS 1.0 are informative — vacuous because HIT never occurs due to hash instability on every access (before_hash!=after_hash all 36), MISS is tautological when SHA always changes; HIT=0 correctly falsifies H2 but root cause is unstabilized relevant-subtree not discriminating drift detection (audit V6)
- Do NOT assume full-tree failure closes orthogonal mechanisms — parameterized slot syntax, hierarchical/WebAPI retrieval, AX semantic similarity, expanded normalization remain open; truncation artifact rejection does not predict full-tree ceiling per B-CONSTANT-NULL-05654 disclosure
- Do NOT assume WebGym 401/404 or Gate0 0 transitions are negative evidence — both correctly MEASUREMENT_INVALID per frozen 2-attempt infrastructure precedence and multi-step density requirement, not permanent unavailability without HF_TOKEN or API fix or Mind2Web-2 alternative
- Do NOT assume product-subtree semantic anchoring validated live — node_count>1 distinct SHA on path families 136/145/196/222 not measured, grammar f2b5e3bb not yet exercised on live product trees beyond generic template
- Do NOT assume within-store 0.9 mean or 1.0 CI implies cross-site transfer — single Magento store single eTLD, cross-site requires >=50 diverse eTLD+1 hosts and multi-store holdout untouched by this experiment
- Do NOT assume infrastructure LIVE equals scientific success — adequacy gates (product-page family count, variance, p, delta, recomputed SHA) still fail; nor assume pip list proves BrowserGym functional for multi-step rollout without genuine trajectory capture
- Do NOT re-trigger exhaustive 567MB LFS test.zip or 420-task CAP enumeration — ABANDONED per Director SUPERSEDE parent disposition, 0/3 strict Gate0 on prior runs was MEASUREMENT_INVALID not falsification, diverse-site threshold sweep is designated replacement
- Do NOT assume hardcoded sampled_families equals true seeded draw without re-derivation inside measurement script via random.Random(35725763380).sample(sorted(families_ge3),10) — prior hardcoded list requires verification
- Do NOT assume browsergym_available / playwright_installed flags equal multi-step Gate0 feasibility — next run must capture genuine BrowserGym 1280x720 trajectories with URL/title/action_target/DOM bytes provenance
- Do NOT assume WebMCP prevalence known — requires live scan of top WebGym sites for tool catalog coverage at honest f

---

## 11. Product consequences

**Positive (SURVIVES):** H1 SURVIVES (full-tree+64-char digest timeout>=300s+expanded stripping mean≥0.6 CI lower>0.5 p<0.05 vs shuffle delta≥0.20 vs truncated variance>0 PC1≥15/20) gives first measurement-valid within-store parameterized transfer signal superseding homepage tautology. Enables bounded C-CROSSSITE within-store holdout and informs C-LLM-INHERIT economics. H2 SURVIVES gives competitive floor ~2x/~30% for C-PRODUCT-ECON honest economics. H3 SURVIVES proves diversity effect without exhaustive LFS/CAP (WebGym 292k + Mind2Web-2). H4 ≥1 relaxed Gate0 pass unlocks physics pilot. H5 WebMCP prevalence informs frontier f=100 compilation leverage. Artifacts reusable substrate.

**Negative (FALSIFIED or MEASUREMENT_INVALID):** H1 FALSIFIED (≥10 families but mean<0.6 or CI lower≤0.5 or p≥0.05 or delta<0.20) → full-tree longest-prefix insufficient, requires slot syntax or hierarchical/WebAPI retrieval; C-CROSSSITE stays HYPOTHESIS single-store vacuous. H2 FALSIFIED (≥30 executed but HIT<0.8 or MISS<0.8 or false_accept≥0.05) → exact cache not discriminating even with expanded stripping. Any MEASUREMENT_INVALID (<5 families, <50 sites, <5 multi-step) → no falsification, repair Docker (timeout>=300s/cached tar/ghcr mirror) or WebGym (HF_TOKEN or Mind2Web-2) before claiming impossibility; exhaustive CAP/LFS not re-triggered per SUPERSEDE. H3 FALSIFIED duplication overlaps 0.9479 — not cross-site evidence.

---

## 12. Cost & information gain

**Cost:** LOW-MEDIUM, no LLM inference for AX/Gate0/WebGym/WebMCP; ~3.5–4.5h wall-clock, <15GB /tmp, stdlib+playwright+browsergym/agentlab+tiktoken. Docker pull 64-char digest 5.4GB timeout>=300s (`timeout 600 docker pull ...@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb`) or cached tar + BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 Chromium (~300MB). Reuse WebArena census hash d65275... for pin.

**Expected information gain:** MAXIMUM per Director REOPEN comparative reasoning — directly repairs 6 root-cause blockers (64-char digest with timeout>=300s/cached tar, truncation degenerate p=1.0, SHA not recomputed + expanded stripping, singleton strata, pip freeze empty + stale self-hash, 401 gating) plus adds pinned WebGym 292k (largest open 292k/127k) + Mind2Web-2 130 Judge external validity and WebMCP prevalence. Narrow repaired pilot + diverse import is highest-probability discriminating test that can change claim/product decisions: delivers falsifiable variance>0 transfer proof or bounded rejection (delta≥0.20), re-derives Stagehand with hash-after-mutation+expanded stripping competitive floor informing per-hit vs fixed at f=100 honest economics, WebGym diverse import tests diversity>depth without LFS, multi-step relaxed Gate0 H>0.1 NL≥20 unlocks physics correlated-state pilot, WebMCP prevalence tests O(1) compilation premise at honest frequency. Either SURVIVES unlocks product within-store holdout + WebGym cross-site baseline + physics pilot, or FALSIFIED-IN-SETTING redirects product to hierarchical retrieval and avoids blocked exhaustive path — highest global leverage vs local retrieval tuning (closed) and vs CONTINUE LFS/CAP (marginal zero). Falsifiability: 5 Director agent priors are priors to be tested, not assumed evidence.

---

## 13. Preregistration freeze

Hypothesis, state/action representation (including 9+expanded stripping, full 64-char digest timeout>=300s resolution, honest sum-counter cost), sampling policy (seed 35725763380 derived inside script), holdout/leakage controls, baselines/nulls/positive controls, primary metric, expected direction, uncertainty method (2000 family bootstrap, 1000 trajectory-grouped permutations, |rho_shuffled|<0.20 gate), adequacy rule, and falsification/survival rule frozen before any outcome-bearing measurement on this experiment_id. Any analysis change after seeing outcomes is exploratory; new confirmatory claim requires new preregistration and untouched evidence. Raw artifacts preserved with sha256 per spec.json §measurement_validity; report.md may interpret but not contradict result.json or exceed frozen claim. CAP/LFS exhaustive enumeration explicitly ABANDONED and not attempted; 0/10 strict Gate0 remains MEASUREMENT_INVALID not falsification. Pinned versions: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, tiktoken, Docker digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb, WebGym 292k + Mind2Web-2 130.

