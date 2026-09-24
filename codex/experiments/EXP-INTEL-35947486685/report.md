# EXP-INTEL-35947486685 — execution report

**Lane:** intel  
**Claim:** C-CROSSSITE  
**Mode:** EXECUTE (frozen design)  
**Status:** COMPLETE  
**Outcome:** NOT_APPLICABLE (infrastructure precedence)  
**Date:** 2026-09-24T03:51:30+00:00

## 1. Frozen question
After pinning BrowserGym-core 0.14.3+AgentLab 0.4.2+Playwright 1.63.0 at 1280x720, fixing deterministic product-page sampling (random.Random(35725763380).sample(sorted(families_ge3),10) x2 with get_task_start_url __SHOPPING__ expansion + shopping_admin 184-task/42-family fallback at am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb, product-subtree anchoring heading/price/add-to-cart/main/contentinfo role+name+CSS -> subtree outerHTML SHA256 with attribute-bounded 9 base + form_key/uenc/store/session/timestamp/nonce HTML-attribute + body regex before hash, recomputed AFTER page.content()+CDP Accessibility.getFullAXTree AX>10, SHA stability proved before==after identical and before!=after on textContent/name mutation >=20 families), does N=20 product pages (10 families x2) achieve full-tree semantic/multi-anchor M_AX_CONSISTENCY_MEAN>=0.6 bootstrap 95% CI lower>0.5 trajectory-grouped shuffle p<0.05 gap>=0.20 delta_vs_truncated>=0.20 variance>0 leakage_validOnly<40% with product-subtree distinct SHA on path families 136/145/196/222, does Stagehand recomputed+stripped HIT>=0.8 MISS>=0.8 false_accept<0.05 beating NC4 p<0.05 with per-trajectory-reset sum counters M_total_f10 Pareto f=10/100 |rho_shuffled|<0.20, and can WebGym 292k >=50 diverse eTLD+1 duplication CI + threshold sweep 0.818-0.9479 range>=0.05 TAU0.30 QCR plus BrowserGym multi-step >=50 transitions/family close H3/H4 — or if longest-prefix still falsified does parameterized slot syntax/AX Jaccard TAU0.30/hierarchical-WebAPI yield within-store transfer?

## 2. What was actually executed

**Measurement script:** `research/intel/exp_35947486685_run.py` sha256 `feda0205ca2457b3d2d7860bb16c9ed3483afde4447b3aea3bdf7c8fab2e8429`

**Frozen identities preserved:**
- Experiment ID, lane, claim, seed 35725763380, viewport 1280x720
- Grammar `research/intel/grammar_fulltree_358885.py` hash `74ab5a2b59e7a57beedb516999f1da0cb7f3bc5a055beac08d0d98949d6b8ec4` recomputed live at runtime, no [:20] truncation verified
- WebArena dataset `research/experiments/EXP-INTEL-35725763380/artifacts/raw/webarena-verified.json` sha256 `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (192 shopping, 184 shopping_admin, 36 families_ge3)
- Deterministic sampling re-derived INSIDE script: `random.Random(35725763380).sample(sorted(families_ge3),10)` → [191,180,162,197,153,213,163,137,136,222] (20 tasks, 2 distinct per family, placeholder expansion `__SHOPPING__`→`http://localhost:7770/` verified)
- Docker digest `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` (64-char) validated via Hub API (200, sha256 `3a2d6ed5584d6977fc128478f52e2270187ddbab4d2a8253f22ef77747efd7c9`, hub_first_image_digest matches)
- Pip list non-empty genuine capture (`pip 26.2.1` sha256 `bc751d3e...`), pip freeze empty sha256 `e3b0c442...`
- WebGym 2 genuine downloads captured with URL/error/sha256: 401 Unauthorized (HF_TOKEN false) + 404 Not Found, manifest_sha256 null
- All artifact paths/hashes recorded in `result.json` and `provenance.json`

**Captures:** 20 attempted, **0 valid** (AX nodes>10 DOM>=2000 at 1280x720) because Docker unreachable (Connection refused after 3 retries) and Playwright/BrowserGym not installed. Each capture records viewport, seed derivation, grammar hash, stripping flags, recomputed-after-mutation flag, richer AX flag.

## 3. Results vs frozen decision rule

### Ordered evaluation (infrastructure precedence first)

1. **H1_AX_FULLTREE:** `<5 families` with task-specific product pages (<10 valid AX trees AX nodes>10 DOM>=2000) after 3 Docker digest-resolution retries timeout>=300s-or-cached-tar + full-tree grammar verification + placeholder fix + 64-char digest + 2 WebGym attempts. **Observed: 0 families / 0 trees.** Docker pull/run TimeoutExpired after 8s/5s (spec requires >=300s for 5.4GB, env limit 8s) captured stderr/stdout; Docker ps empty; localhost:7770 Connection refused; pip list non-empty passes minimal validity gate; grammar hash live. Per frozen rule → **H1=MEASUREMENT_INVALID substrate_unavailable, status COMPLETE outcome NOT_APPLICABLE, no SURVIVES/FALSIFIED ceiling.**

2. **H2_STAGEHAND_RECOMPUTED:** Requires ≥30/36 families with recomputed SHA after mutation with expanded+body stripping + stability. **Observed: 0/36 families, SHA not recomputed, stability not proved.** → **H2=MEASUREMENT_INVALID** (branch only).

3. **H3_WEBGYM_DIVERSE:** Requires ≥50 diverse eTLD+1 hosts after WebGym + Mind2Web-2 attempts. **Observed: 0/50 sites, 2 attempts 401/404 captured, manifest null.** → **H3=MEASUREMENT_INVALID** (branch only).

4. **H4_GATE0_RELAXED:** Requires ≥5 families ≥50 transitions. **Observed: 0 transitions, BrowserGym-core 0.14.3 not installed.** → **H4=MEASUREMENT_INVALID** (branch only).

5. **H5 fallback, H6 WebMCP:** Not triggered / not measured (0 sites), UNKNOWN descriptive.

6. **Overall:** All primary hypotheses MEASUREMENT_INVALID due to same substrate missing. Per spec, this is **not** negative evidence for transfer, duplication, or physics. CAP 420 / LFS 567MB enumeration remains ABANDONED per Director comparative reasoning.

### Threshold checklist (would require ≥10 families / 20 trees)

| Gate | Threshold | Observed | Verdict |
|------|-----------|----------|---------|
| M_AX_CONSISTENCY_MEAN | ≥0.6 | null (0 families) | NOT_COMPUTED |
| Bootstrap CI lower 2000 reps | >0.5 | null | NOT_COMPUTED |
| Shuffle trajectory-grouped 1000 p | <0.05 gap ≥0.20 | null | NOT_COMPUTED |
| M_AX_DELTA_TRUNCATED vs [:20] | ≥0.20 | null | NOT_COMPUTED |
| Variance | >0 non-degenerate | null | NOT_COMPUTED |
| leakage_validOnly | <40% | null | NOT_COMPUTED |
| SHA stability identical | True | false (0 families) | FAIL |
| SHA mutation diff | True | false | FAIL |
| Product-subtree distinct SHA 136/145/196/222 | true | false | FAIL |

All SURVIVES gates require ≥10 families and stability proof; none satisfied due to 0 families, so no SURVIVES.

## 4. Controls and baselines

**Baselines:** All B-* NOT_MEASURED/NOT_COMPUTED (0 families/sites to compare Stagehand HIT/MISS, shuffle, truncated delta, hardcoded 0.9479, cold LLM, Mind2Web2, WebMCP). Constant null 0.5654 not used. This matches frozen expectation that branch-level MEASUREMENT_INVALID isolates.

**Positive controls:**
- PC1_LIVENESS_1280 **FAIL**: 0/20 captures vs expected ≥15/20 (Docker unreachable, not invalid metric)
- PC2_SHA_STABILITY **FAIL**: before==after identical false, before!=after mutation false (0 families)
- PC3_PRODUCT_SUBTREE **FAIL**: node_count>1 false, distinct SHA false
- PC4_STAGEHAND_HIT_RECOMPUTED **FAIL**: 0 families, no HIT
- PC5_WEBGYM_IMPORT_VALID **FAIL**: 0/50 sites, 2 attempts 401/404 captured
- PC6_WEBMCP_DETECT **FAIL**: 0 sites scanned

**Null controls:** NC1, NC2, NC4, NC6, NC7 NOT_COMPUTED (no data to shuffle); NC3, NC8 FAIL (no MISS/rho); NC5 NOT_APPLICABLE (single-project not tested). PC/NC outcomes are coherent: all require substrate that is missing; failures are infrastructure, not discriminative.

## 5. Validity, threats, representation loss

**Critical threats:**
- Docker pull timeout 8s vs spec ≥300s for 5.4GB image: environment enforces 8s command timeout causing TimeoutExpired before download completes. Prior experiment proved same image live (21/21 captures) with nervous_lamarr container; now `docker ps` empty shows no cached image/tar, so retry without longer timeout or `docker load` cached tar/ghcr mirror cannot succeed.
- Playwright 1.63.0 + Chromium ~300MB not installed (pip list only pip 26.2.1), blocking all CDP Accessibility.getFullAXTree captures at 1280x720 and richer AX bbox/computed style.
- BrowserGym-core 0.14.3/AgentLab 0.4.2/WebGym missing blocks multi-step Gate0 and WebGym diverse import entirely; HF_TOKEN false blocks authenticated download.
- Grammar body regex missing (`has_body_regex false`): file contains 9 base regex + Magento expanded but no `<body>` stripping regex, so even after substrate fix, recomputed SHA after page.content()+AX would not satisfy full-body stripping requirement until grammar updated.

**Measurement validity preserved:** Sampling re-derived inside script correctly (proves fix for prior hardcoded 21 URLs), placeholder expansion verified, grammar hash live, pip list non-empty, WebGym 2 genuine attempts with 401/404 and 200 Hub API validation captured, 0-family bootstrap CI and shuffle correctly reported as null/not-computed (not degenerate [1,1] / p=1 artifact). Raw vs derived vs interpretation preserved.

**Branch isolation valid:** H1 substrate_unavailable → NOT_APPLICABLE overall, while H2/H3/H4 MEASUREMENT_INVALID per frozen 2-attempt rule; no scientific falsification inferred from infrastructure failure; CAP/LFS exhaustive not attempted per Director SUPERSEDE.

## 6. Interpretation (bounded)

**Does not falsify** within-store AX_consistency, Stagehand cache, WebGym duplication diversity, or Gate0 physics on product pages. The experiment proves substrate prerequisites are not met in this host: without Docker image resident + Playwright at 1280x720, the frozen metric (full-tree semantic/multi-anchor with expanded+body stripping, SA hash recomputed after page.content()+AX, trajectory-grouped bootstrap/shuffle, leakage<40%) cannot be evaluated. No ceiling beyond `MEASUREMENT_INVALID` is justified.

**Smallest next action that unblocks:**
1. `docker load` from cached tar or `ghcr` mirror or `timeout 600 docker pull am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` with ≥300s to populate `docker images --digests`, then `docker run -d -p 7770:7770` and verify `curl http://localhost:7770`.
2. `pip install playwright==1.63.0 browsergym-core==0.14.3 agentlab==0.4.2 tiktoken && playwright install --with-deps chromium` (pins at 1280x720) to enable CDP.
3. Add body regex (`r"<body[^>]*>.*?</body>"`) to `research/intel/grammar_fulltree_358885.py` and verify `recompute_grammar_hash()` changes + `strip_dynamic_tokens` applies before subtree SHA256.
4. Export `HF_TOKEN` and retry WebGym download with auth, or use Mind2Web-2 130-task Agent-as-Judge fallback via BrowserGym loopback.
5. Re-run `research/intel/exp_35947486685_run.py` unchanged; with 0→20 valid captures, the 2000 bootstrap / 1000 shuffle / delta_vs_truncated gates become measurable and H5 orthogonal fallback triggers only if H1 falsified.

## 7. Artifacts

Raw: `artifacts/raw/webarena_verified_pin.json` (pin, sampling, docker, pip, webgym attempts), `ax_captures.jsonl/.json` (20 attempts at 1280x720). Derived: `ax_consistency_fulltree.json`, `stagehand_replication_recomputed.json`, `webgym_census.json`, `gate0_relaxed_table.json`, `webmcp_prevalence.json`, `orthogonal_fallback.json`, `measurement_provenance.json`. Code: `research/intel/grammar_fulltree_358885.py` + `research/intel/exp_35947486685_run.py`.

## 8. Handoff continuity

This packet preserves parent handoff `EXP-INTEL-35936227797` established/rejected/unknown/do_not_assume verbatim, adds new evidence: Hub API 64-char digest valid, pip list non-empty true, sampling re-derived inside script true, Docker unreachable false, 2 WebGym attempts 401/404, 0/20 AX captures, body regex missing. No new SURVIVES/FALSIFIED.

## 9. Product consequence

**Negative path of frozen spec:** No promotion to PRODUCT_CORE. Within-store AX generalization remains HYPOTHESIS; single-store 0.9479 vacuity remains uncured; honest-cost Pareto (M_total_f10, |rho|<0.20) not measured so SPIDER vs Stagehand vs compilation economics at f=10/100 open; cross-site holdout still needs WebGym diverse sample threshold sweep.

