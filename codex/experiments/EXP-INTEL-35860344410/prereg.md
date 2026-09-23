# EXP-INTEL-35860344410 preregistration — Intel PIVOT to C-CROSSSITE (SUPERSEDE)

**Lane:** intel — `research/intel` only (no cross-lane writes)  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout (registry HYPOTHESIS)  
**Director mandate:** PIVOT from 8-repair mega-question to three minimal unblocking measurements; cognitive_reset true; parent_handoff SUPEREDE (EXP-INTEL-35798952720 MEASUREMENT_INVALID); expires exhaustive 567MB LFS / 420-task CAP enumeration (0/3 strict MEASUREMENT_INVALID not falsification). Target pins: BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720, full-tree semantic/multi-anchor (no [:20] truncation, no selectors[:20] placeholder, product-subtree SHA256 recomputed after DOM mutation via page.content() + Accessibility.getFullAXTree), WebGym 300k diverse holdout >=50 eTLD+1 sites, multi-step >=50 transitions/family >=10 families.  
**Inherited state consumed:** Read `research/experiments/EXP-INTEL-35798952720/handoff.json` sha a0930677a1195b051b03e1077ddeadc8cd262cf1c41f6ceb704380007d8e8ca6; preserved established/rejected/unknown/do_not_assume verbatim in §10. No outcome-bearing measurement run during DESIGN. Verifies Scout pin correction and biography of 11/14 C-CROSSSITE tunnel_flag degenerate AX 1.0 p=1.0 blocking Physics Gate0.

---

## 1. Strategic question (Director binding) → falsifiable experiment

**Director question:** After pinning BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720 and fixing full-tree traversal + WebGym 300k diverse holdout + multi-step trajectories >=50 transitions/family, does N=20 product-page AX_consistency achieve mean≥0.6 (bootstrap CI lower>0.5, trajectory-grouped shuffle p<0.05, delta≥0.2 vs truncated) and Stagehand selector+relevant-subtree SHA256 achieve HIT≥0.8 MISS≥0.8 false_accept<0.05 vs NC4, plus relaxed Gate0 H>0.1 NL≥20 titles≥1 to unblock physics/within-store transfer without exhaustive LFS/CAP?

**Smallest high-information translation (this prereg):** Narrow repaired pilot on WebArena-Verified v2 shopping single-store product pages (10 families ×2 tasks =20 CDP captures) + Stagehand replication on same 36 families + WebGym 300k 50-site diverse census + 10-family multi-step rollout (strive 50 transitions each). Any narrower (single metric) would leave Stagehand competitive floor or WebGym diversity untested and risk another degenerate pass; any broader (exhaustive LFS/CAP) repeats blocked path with zero information gain per Director comparative reasoning. Already-frozen experiments resume independently; this NEW experiment follows Director mandate, not inherited next_question.

---

## 2. Hypotheses (confirmatory)

- **H1_AX_FULLTREE (primary, confirmatory):** Full-tree semantic/multi-anchor without truncation (complete CDP Accessibility.getFullAXTree traversal, product-specific subtree anchored on heading/price/add-to-cart/main/contentinfo boundaries, role+name+CSS path + subtree outerHTML SHA256, no token truncation, longest-prefix without fallback) yields discriminating within-store AX_consistency on N=20 live product-page captures with mean≥0.6, bootstrap 2000 family-level 95% CI lower>0.5, trajectory-grouped permutation 1000 p<0.05 vs NC1 (>0.20 above null), delta≥0.20 vs prior invalid 0.2857 fallback, delta≥0.10 vs truncated [:20] baseline on same pages, per-family variance>0 (CI width>0, not degenerate [1.0,1.0] homepage tautology).

- **H2_STAGEHAND_RECOMPUTED (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (exact normalized selector from AX node+DOM attributes + SHA256 of relevant subtree outerHTML recomputed AFTER mutation via page.content() + page.evaluate, HIT after N=2 identical results, per-project isolation) reports HIT≥0.8 on identical DOM, MISS≥0.8 on single-attribute drifted DOM, false_accept<0.05, beats NC4 random HIT/MISS null p<0.05, with cold vs cached latency/tokens via real Playwright dispatch path (navigation+hash+cache lookup, tiktoken/provider counts) delivering ~2× speedup and ~30% token saving on HIT when selectors exclusively derived (0 synthetic fam_task fallback).

- **H3_WEBGYM_DIVERSE (confirmatory):** WebGym 300k-task async corpus (>=50 diverse eTLD+1 hosts, stratified deterministic seed 35725763380) yields duplication prevalence 95%CI distinct from hardcoded WebArena-Verified v2 single-store duplication 0.9479 CI[0.9167,0.9792] (192 tasks 49 templates 36 families) and corpus-level deduplication threshold sweep range ≥0.05 across 0.818–0.9479, proving distribution diversity matters more than hierarchical depth without exhaustive 567MB LFS.

- **H4_GATE0_RELAXED (descriptive pilot, not confirmatory physics claim):** Multi-step trajectories ≥50 transitions/family on ≥10 families yield ≥1 family passing relaxed census (titles≥1 H(S_next|URL,H_K=3)>0.1 NL≥20 singleton<50%) enabling correlated-state physics pilot; strict Gate0 (H>0.2 NL≥50 strata≥10 leakage_validOnly<40%) reported descriptively — 0/10 strict is MEASUREMENT_INVALID insufficient density not falsification.

---

## 3. State / action / target representation (frozen)

**State before/after:** URL (full, fragments preserved for hash-SPAs; normalized href vs state_after.url for leakage), document.title, CDP Accessibility.getFullAXTree full tree (600–2000 nodes required, DOM bytes≥2000, sha256 per capture), product-subtree outerHTML SHA256 via page.content() relevant subtree (normalized outerHTML, not SHA256-truncated DOM), DOM bytes sha256. Browser state at 1280×720, CDP method, no scroll initial viewport; multi-step trajectories provide temporal history for Gate0.

**Action representation:** AX node role+name + CSS path + normalized selector (derived from AX+DOM attributes, no synthetic fam_task fallback), action.target_href where present, primitive action type (click/type/navigate) for multi-step.

**Target (derived measurements):**
- M_AX_CONSISTENCY_MEAN = mean longest-prefix consistency over 10 families (per-family score = longest common prefix length / max length of full-tree tokenized pattern, no truncation), family is unit, reported with per-family scores.
- M_AX_DELTA_TRUNCATED = M_AX_FULLTREE - M_AX_TRUNCATED20 on same 20 pages.
- M_STAGEHAND_HIT, M_STAGEHAND_MISS, M_FALSE_ACCEPT = HIT rate identical, MISS rate drift (recomputed SHA), false_accept = HIT despite drift.
- M_WEBGYM_DUP_PREVALENCE + 95%CI, M_WEBGYM_THRESHOLD_RANGE.
- M_GATE0_RELAXED_PASS_COUNT, M_GATE0_STRICT_PASS_COUNT, per-family H, NL, strata, singleton rate, leakage_validOnly.

---

## 4. Sampling policy & unit of analysis

**Population:** WebArena-Verified v2 shopping families (36 families ≥3 tasks, hash d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30) + WebGym 300k diverse sites.  
**Sampling:** Deterministic seed 35725763380 for ALL random choices: sample 10 families without replacement from 36 (stratified to maximize product-page families; expand to shopping_admin 184-task/42-family corpus if <5 product-page families achievable with 36), within each family sample 2 distinct tasks. WebGym: stratified sample ≥50 diverse eTLD+1 hosts from corpus. Multi-step: same 10 families. No post-hoc seed change.  
**Unit:** Family for AX (N=10 families, 20 captures), per-transition for Gate0 PMI/CMI with trajectory-grouped permutation (grouped by trajectory/family not step) to avoid degenerate bootstrap CI[1,1] variance 0 p=1 and singleton strata (require ≥5 per stratum for PMI/CMI else undefined).  
**Exclusions:** Captures with <600 nodes or DOM bytes<2000 or placeholder not expanded → invalid, counts toward <5 families substrate_unavailable, not toward mean.

---

## 5. Holdout & leakage control

- Within-store longest-prefix has no train/test leakage (descriptive consistency), but preprocessing (full-tree grammar) is frozen before capture, not fit on held-out outcome.
- Stagehand cache: per-project isolation test (NC5) ensures no cross-project identity leakage; HIT threshold N=2 frozen.
- WebGym: site-label shuffle null (NC6) tests duplication prevalence vs site identity leakage; shard held-out is eTLD+1 (not task shuffle).
- Gate0: trajectory-grouped permutation (grouped by trajectory, not transition) and singleton SA exclusion (≥2 per stratum normally, ≥5 for H) prevent degenerate p.

---

## 6. Baselines & controls (stable identities for EXECUTE/AUDIT/DIRECTOR)

**Baselines (strong):**
- B-STAGEHAND-VERB — shipped Stagehand ~2×/~30% (must use recomputed SHA, derived selectors)
- B-RANDOM-AX-SHUFFLE — trajectory-grouped shuffle 1000 perms
- B-TRUNCATED-20 — same pages with [:20] truncation + selectors[:20] placeholder (root-cause test)
- B-WEBGYM-HARDCODED-09479 — hardcoded 0.9479 CI[0.9167,0.9792] null
- B-COLD-LLM — cold agent latency/tokens via Stagehand cold path
- B-CONSTANT-NULL-05654 — REJECTED 0.5654 (disclosed only, not decision)

**Positive controls:**
- PC1_LIVENESS_1280 — ≥15/20 captures 600–2000 nodes at 1280×720, Docker reachable 3 retries
- PC2_AX_PRIOR_PRODUCT — ≥1 family discriminates vs degenerate homepage 1.0 with variance>0
- PC3_STAGEHAND_HIT_RECOMPUTED — 3 consecutive identical subtree SHA + selector → HIT on 2nd/3rd with per-project isolation
- PC4_WEBGYM_IMPORT_VALID — WebGym import parses ≥50 sites, sweep computable
- PC5_SYNTHETIC_PIPELINE — synthetic data pipeline sanity (is_synthetic true, not decision)

**Null controls:**
- NC1_AX_SHUFFLE_TRAJECTORY_GROUPED — permute per-family scores 1000 perms, require p<0.05 and mean+0.20 gap; std 0 → FAIL
- NC2_RANDOM_PATTERN — random family pattern <0.2 expected
- NC3_DOM_DRIFT_RECOMPUTED — page.evaluate mutation + SHA recomputed AFTER via page.content(), require MISS≥0.8 false_accept<0.05, verify hash change
- NC4_RANDOM_CACHE — shuffle HIT/MISS labels 1000 perms ~50%, require true beats p<0.05
- NC5_CROSS_PROJECT_LEAKAGE — cross-project same key must MISS 0%
- NC6_WEBGYM_SHUFFLE — site-label shuffle 1000 perms for duplication

All perms seed 35725763380; 2000 family-level bootstraps (percentile) for CIs.

---

## 7. Primary metric, expected direction, uncertainty

**Primary:** M_AX_CONSISTENCY_MEAN on N=20 product pages. Expected direction: full-tree mean > truncated mean and > shuffle null. Secondary: HIT/MISS/false_accept, WebGym duplication CI, Gate0 relaxed pass count.  
**Uncertainty:** 2000 family-level bootstraps (resample families with replacement, recompute mean) → 95% percentile CI; 1000 trajectory-grouped permutations for p = (1+ count perm≥true)/(1+1000). Report CI lower, variance, delta vs truncated and vs 0.2857, shuffle mean/std/p95.

---

## 8. Adequacy & validity gate (pre-outcome)

- Adequacy: ≥10 families (20 trees) captured with 600–2000 nodes, placeholder expanded, full-tree grammar verified no truncation via code sha on 4 path families product subtree distinct hashes, SHA256 recomputed AFTER mutation verified per drift family, BrowserGym/Playwright pins logged (pip freeze). Else MEASUREMENT_INVALID substrate_unavailable.
- Validity gate: target integrity (no post-state in pre-state, recomputed SHA after mutation), split integrity (trajectory-grouped permutation), sampling integrity (frozen seed deterministic), uncertainty integrity (family-level bootstrap, not arbitrary jitter), representation integrity (full-tree not truncated, relevant-subtree not full-page, CDP AX preserved). Violation → MEASUREMENT_INVALID, no SURVIVES/FALSIFIED.

---

## 9. Decision & falsification / survival rule (frozen ordered evaluation — infrastructure precedence)

1. If <5 families with product pages captured (<10 valid trees) after 3 Docker retries + grammar verification + placeholder fix → status COMPLETE outcome NOT_APPLICABLE, H1=MEASUREMENT_INVALID substrate_unavailable (publish provenance, no falsification). Same for WebGym <50 sites (H3 branch) or multi-step <5 families ≥50 transitions (H4 branch) → branch MEASUREMENT_INVALID only.

2. Else if captured ≥10 families (20 trees) and mean≥0.6 AND CI lower>0.5 AND p<0.05 vs NC1 AND delta vs 0.2857 ≥0.20 AND full-tree vs truncated delta ≥0.10 AND PC1≥15/20 AND variance>0 then H1=SURVIVES (full-tree parameterized transfer identifiable within-store capturing product-specific subtree). Else if captured ≥10 families but mean<0.6 OR CI lower≤0.5 OR p≥0.05 OR delta<0.20 OR full-tree delta<0.10 OR variance=0 → H1=FALSIFIED-IN-SETTING bounded to this method/families/page-type (does NOT reject alternative grammars or cross-site with hierarchical retrieval).

3. H2_STAGEHAND_RECOMPUTED: If <30/36 families attempted or SHA not recomputed after mutation → H2=MEASUREMENT_INVALID. Else if HIT≥0.8 AND MISS≥0.8 AND false_accept<0.05 AND real-path speedup/tokens reported AND beats NC4 p<0.05 AND 0 synthetic fallback AND PC3 isolation 0.0 → SURVIVES. Else if executed ≥30 but HIT<0.8 or MISS<0.8 or false_accept≥0.05 or NC4 p≥0.05 → FALSIFIED-IN-SETTING on this substrate.

4. H3_WEBGYM_DIVERSE: If <50 sites → MEASUREMENT_INVALID branch. Else if CI non-overlapping 0.9479 CI OR threshold range≥0.05 → SURVIVES. Else if ≥50 sites but CI overlaps AND range<0.05 → FALSIFIED-IN-SETTING (single-store not distinct).

5. H4_GATE0_RELAXED descriptive: If <5 families ≥50 transitions → MEASUREMENT_INVALID Gate0 branch. Else if ≥1 relaxed pass (H>0.1 NL≥20) → SURVIVES pilot feasibility; 0/10 relaxed with adequate NL density → FALSIFIED-IN-SETTING for relaxed pilot on Magento (insufficient density not physics closure). 0/10 strict is MEASUREMENT_INVALID not global falsification.

Overall outcome: SUPPORTS if H1 and H2 SURVIVE, MIXED if split, FALSIFIES if both falsified, INCONCLUSIVE if H1 MEASUREMENT_INVALID; CAP/LFS exhaustive ABANDONED per Director SUPERSEDE not attempted.

---

## 10. Inherited carry-forward (exact preservation from EXP-INTEL-35798952720 handoff)

**Established (do not re-prove, reuse artifacts):** Docker substrate LIVE at 1280×720 (am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 reachable after 1 retry, CDP 20/20 captures 626–1430 nodes documented, BrowserGym-core 0.14.3 import fails but AgentLab 0.4.2 + Playwright 1.44.0 functional — carry-forward pinned remedy 1.63.0/0.14.3); WebArena-Verified v2 census 192 tasks 49 templates 36 families ≥3 duplication 0.9479 CI[0.9167,0.9792]; placeholder fix __SHOPPING__/path→http://localhost:7770/path verified but limited to 4/36 families (136,145,196,222) causing 2/10 product families — this audit V1 drives shopping_admin 42-family expansion; full-tree grammar applied but subtree_node_count=1 hash='' and selectors[:20] remaining — audit V2 drives verified fix; shuffle tautology V3, drift string-replace V4, fallback selectors V6, sub-ms artifact V5, WebGym unavailable V8, Gate0 110 transitions NL3 V9 — all 8 fixes required verbatim.

**Rejected (bounded, not global):** Truncated [:20] grammar 1.0 CI[1,1] p=1.0 NOT evidence of transfer (bounded); 4/36 scarcity not rejection of admin 42-family; Stagehand 0.943 HIT with fallback+string-replace NOT spec-compliant; 6-model density extrapolation F(n)=0.5654 REJECTED vacuous; CAP/LFS exhaustive search ABANDONED not falsified.

**Unknown (this experiment tests):** 7 questions from §10 (shuffle variance, admin ≥5 product families with subtree>1, page.evaluate MISS≥0.8 with real path ≥30 families, HIT≥0.8 without fallback, WebGym duplication distinct, Gate0 relaxed with ≥5/stratum, Playwright 1.63.0 vs 1.44.0 effect).

**Do_not_assume:** 9 prohibitions preserved verbatim (AX 0.8 homepage-dominated, delta vs fallback, Stagehand 0.943 inflated, false_accept 0.0 until recomputed, Gate0 0/10 not impossibility, exhaustive CAP/LFS not required, Playwright 1.63 compatibility, within-store not cross-site, truncated-first-20 null + hardcoded 0.9479 as predictors, SHA without recompute invalid, subtree_count=1 not isolation) — see handoff do_not_assume for exact wording.

---

## 11. Product consequences

**Positive (SURVIVES):** H1+H2 SURVIVES gives first measurement-valid within-store transfer signal + shipped Stagehand competitive floor (~2×/~30% with recomputation guard) determining SPIDER vs Stagehand investment threshold for C-PRODUCT-ECON honest economics (per-hit vs fixed at f=100); H3 gives WebGym diversity census replacing hardcoded 0.9479 and unblocking cross-site holdout; H4 relaxed ≥1 pass unlocks correlated-state physics pilot; artifacts become reusable substrate for Mind2Web-2.

**Negative (FALSIFIED or MEASUREMENT_INVALID):** H1 FALSIFIED → full-tree longest-prefix insufficient for product-specific transfer, requires parameterized slot syntax or hierarchical/WebAPI retrieval; C-CROSSSITE stays HYPOTHESIS single-store vacuous. H2 FALSIFIED → Stagehand exact cache not discriminating on shopping even with recomputation, use RAG/SPIDER verification baseline. Any MEASUREMENT_INVALID branch (<5 product families, <50 WebGym sites, <5 multi-step families) → no falsification, repair substrate (Docker/WebGym/BrowserGym loopback) before claiming impossibility; exhaustive CAP/LFS not re-triggered per SUPERSEDE.

---

## 12. Cost & information gain

**Cost:** LOW-MEDIUM, no LLM inference for AX/Gate0/WebGym; ~3–4h wall-clock, <15GB /tmp, stdlib+playwright+browsergym/agentlab+tiktoken. Reuse WebArena census hash d652... for pin verification; no exhaustive CAP/LFS.

**Expected information gain:** MAXIMUM per Director comparative reasoning — directly repairs 8 audit-required degeneracies with deterministic fixes delivering falsifiable variance>0 transfer proof or bounded rejection, re-derives Stagehand with hash-after-mutation competitive floor informing amortized economics, WebGym diverse import tests diversity>depth, multi-step relaxed Gate0 unlocks physics pilot. Either outcome changes product decision (invest vs pivot) without re-triggering blocked exhaustive path — highest global leverage vs synthetic FSM TV continuation (44-deep tunnel closed).

---

## 13. Preregistration freeze

Hypothesis, representation, sampling, holdout, nulls, metric, direction, uncertainty, adequacy and falsification rules frozen before any outcome-bearing measurement on this experiment_id. Any analysis change after seeing outcomes is exploratory; new confirmatory claim requires new preregistration and untouched evidence. Raw artifacts preserved with sha256 per §8–9 of spec.json; report.md may interpret but not contradict result.json or exceed frozen claim.
