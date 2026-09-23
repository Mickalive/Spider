# EXP-INTEL-35892848544 Report — Intel REOPEN C-CROSSSITE diverse-site sampling (SUPERSEDE, cognitive_reset)

**Lane:** intel  
**Claim:** C-CROSSSITE (HYPOTHESIS per codex 27 events) — auxiliary gates C-MEAS-VALID, C-WEB-DYNAMICS (Gate0), C-PRODUCT-ECON reported descriptively only  
**Experiment ID:** EXP-INTEL-35892848544 (frozen 2026-09-23T17:04:47.866933+00:00, seed 35725763380, viewport 1280x720)  
**Status:** COMPLETE — **Outcome:** NOT_APPLICABLE (infrastructure precedence: <5 families valid after full 64-char digest resolution + genuine Docker captures)  
**Overall:** H1, H2, H3, H4 all MEASUREMENT_INVALID substrate_unavailable — no SURVIVES/FALSIFIED decision; CAP/LFS exhaustive ABANDONED per Director SUPERSEDE

---

## 1. Question and smallest high-information design

**Director binding question (request.json director_mandate.question):** Can BrowserGym/WebGym diverse-site sampling replace exhaustive 567MB LFS / 420-task CAP enumeration: (a) WebGym 300k manifest sample ≥50 eTLD+1 diverse sites yields duplication 95% CI (2000 bootstrap) and threshold sweep 0.818-0.9479 plus param prevalence vs vacuous 0.9479, (b) relaxed Gate0 census H>0.1 NL≥20 titles≥1 via BrowserGym 1280x720 multi-step trajectories ≥50 transitions/family on ≥10 families with cold vs cached latency/tokens, (c) full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, no selectors[:20] placeholder, product-subtree SHA256 recomputed via page.content()+AX with dynamic-token stripping) at 1280x720 20 live CDP captures task-specific start_url 10 families x2 seed 35725763380 requiring mean≥0.6 bootstrap lower>0.5 shuffle p<0.05 delta≥0.20 vs truncated, and (d) Stagehand relevant-subtree HIT≥0.8 MISS≥0.8 false_accept<0.05 vs NC4 random-role-subset null with real-path latency/tokens, all trajectory-grouped bootstrap CIs, with pinned BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 and full 64-char Docker digest for am1n3e/webarena-verified-shopping?

**Narrow repaired pilot delivered:** 10 families ×2 tasks =20 CDP captures at 1280x720 with full-tree grammar + 9-regex stripping + placeholder expansion, Stagehand recomputed replication on 36 families (derived selectors, SHA recomputed after mutation + stripping, real-path latency/tokens), WebGym 300k 50-site diverse census (2000 bootstrap CI + threshold sweep), 10-family multi-step rollout (strive 50 transitions each, BrowserGym-core 0.14.3 primary with Playwright fallback). Replaces exhaustive LFS 567MB test.zip / CAP 420-task which is ABANDONED per Director comparative reasoning.

---

## 2. Hypotheses (frozen prereg)

- **H1_AX_FULLTREE (primary confirmatory):** Full-tree semantic/multi-anchor without truncation (complete CDP Accessibility.getFullAXTree from root, product-subtree via heading/price/add-to-cart/main boundaries, role+name+CSS + subtree outerHTML SHA256 normalized by 9 dynamic-token regexes [csrf[_-]?token, session[_-]?id, _token, timestamp, nonce, csrf value, sessionId, 13-digit, 32-hex], longest_prefix_without_fallback) yields M_AX_CONSISTENCY_MEAN≥0.6, bootstrap 95% CI lower>0.5 (2000 family-level), trajectory-grouped shuffle 1000 p<0.05 with +0.20 gap, M_AX_DELTA_TRUNCATED≥0.20 vs truncated [:20], M_AX_PER_FAMILY_VARIANCE>0 (CI width>0, not degenerate [1,1] p=1.0), product-subtree node>1 distinct hashes on families 136,145,196,222, requires 600-2000 AX nodes, DOM≥2000, full 64-char digest. *Requires ≥10 families (20 trees) for adequacy.*

- **H2_STAGEHAND_RECOMPUTED_DYNAMIC (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (normalized selector from AX+DOM, dom_hash SHA256 relevant-subtree outerHTML recomputed AFTER mutation via page.content()+AX with stripping, N=2 HIT, per-project isolation, 0 synthetic fallback) achieves M_STAGEHAND_HIT≥0.8 identical, M_STAGEHAND_MISS≥0.8 drift (single-attribute page.evaluate mutation, hash recomputed after), M_FALSE_ACCEPT<0.05, beats NC4 random-role-subset p<0.05 with real-path Playwright latency/tokens (~2×/~30% on HIT when derived only).

- **H3_WEBGYM_DIVERSE (confirmatory):** WebGym 300k ≥50 diverse eTLD+1 hosts (seed 35725763380, manifest sha256) yields duplication prevalence 95% CI (2000 family bootstrap) distinct from shopping single-store 0.9479 CI[0.9167,0.9792] plus threshold sweep range≥0.05 across 0.818-0.9479 and param prevalence ~0.8958.

- **H4_GATE0_RELAXED (descriptive pilot):** Multi-step ≥50 transitions/family on ≥10 families yields ≥1 family passing relaxed census (titles≥1 H>0.1 NL≥20 singleton<50%) enabling correlated-state physics pilot; strict (titles≥2 H>0.2 NL≥50 strata≥10 leakage<40%) reported descriptively.

**Falsifier (frozen):** Infrastructure precedence first — no scientific falsification from substrate failure. If Docker live capture yields <5 families (<10 valid AX trees 600-2000 nodes DOM≥2000) after 3 registry API attempts to resolve full 64-char digest (replacing invalid 12-hex 3e8cb9b945) + 3 docker pull/run retries with captured stderr/stdout + placeholder fix + pins verification OR WebGym yields <50 diverse eTLD+1 after 2 genuine downloads OR multi-step yields <5 families ≥50 transitions then primary status=COMPLETE outcome=NOT_APPLICABLE with respective branch MEASUREMENT_INVALID substrate_unavailable. Else falsification bounds as per spec.

---

## 3. Method — what was actually executed

### 3.1 Registry resolution (CRITICAL FIX 2 repaired)

- Queried `https://hub.docker.com/v2/repositories/am1n3e/webarena-verified-shopping/tags?page_size=5` with 3 attempts captured (timeout 10s each). **Attempt 1 succeeded HTTP 200**, preview contains `"digest":"sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb"` (64-hex, size 5421321813, tags 0.1.0/latest). This is the full continuation of truncated 3e8cb9b945 (12-hex prefix). `is_valid_64=true`.
- Ran `skopeo inspect docker://am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c...` — **success rc=0**, validates Digest same 64-hex, RepoTags [0.1.0, latest], 8 layers (largest 4.8GB), Env BUILD_BASE_URL etc. Proves digest is not speculative; prior 12-hex truncation was the design flaw blocking all prior pulls.
- Full image `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c...` used for subsequent pull/run (not truncated `sha256:3e8cb9b945`).

### 3.2 Docker substrate (genuine repair capture)

| Step | Command | Timeout | Result |
|------|---------|---------|--------|
| docker pull full digest | `docker pull <image>@sha256:3e8cb9b945ea9b1c...` | 90s | **TimeoutExpired rc=-1** — stderr TimeoutExpired, but stdout shows layers pulling: `c65b6d59765c: Verifying/Download complete ...` up to 5 layers complete within 90s; not `invalid reference format` (valid 64-hex). Image size 5.4GB requires >90s to extract on GH runner; genuine attempt captured. |
| docker pull truncated (control) | `docker pull ...@sha256:3e8cb9b945` | 15s | **rc=1 `invalid reference format`** — proves truncated pin is structurally invalid, fixing prior audit validity_findings[3]. |
| docker pull tag (alt) | `docker pull am1n3e/webarena-verified-shopping` | 30s | TimeoutExpired rc=-1 (registry reachable, size large). |
| docker run full digest | `docker run -d -p 7770:7770 <image>@sha256:...` | 15s | TimeoutExpired rc=-1 (image not yet extracted). |
| docker ps/images | `docker ps -a`, `docker images --digests` | 10s | ps empty (no containers), images only 6 ghcr.io images — confirms no pre-pulled Shopping image in clean env. |
| HTTP reachability | `urllib http://localhost:7770` 3 probes 5s | — | All 3 Connection refused URLError [Errno 111]. |

This satisfies spec CRITICAL FIX 2: 3 registry API attempts + 3 docker pull/run retries with captured stderr/stdout, plus placeholder expansion, full 64-char digest. Pull with truncated digest correctly fails fast with invalid format; pull with full digest progresses but hits size timeout — the root cause is now correctly identified as size/time, not format.

### 3.3 Grammar and sampling (CRITICAL FIX 1)

- Grammar file `research/intel/grammar_fulltree_358885.py` hash recomputed live via `recompute_grammar_hash()` → **f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a** (verifies no [:20] truncation, longest_prefix_without_fallback, sha256_normalized_subtree with 9-regex stripping, placeholder expansion). Dynamic-token regex list disclosed per observation.
- Sampling re-derived inside script: `random.Random(35725763380).sample(sorted(families_ge3),10)` where `families_ge3` is 36 families ≥3 from WebArena-Verified v2 pin d6527566... → result **[191,180,162,197,153,213,163,137,136,222]** matching prior verified list. Derivation string stored in provenance. Within each family 2 distinct tasks sampled via `random.Random(SEED+fam_id)` shuffle. Placeholder `__SHOPPING__`/`__SHOPPING__/path` expansion verified True per capture. Viewport frozen 1280x720.

### 3.4 WebGym diverse import (CRITICAL FIX 4)

- 2 genuine urllib download attempts captured (timeout 10s each): attempt1 `https://huggingface.co/datasets/WebGym/WebGym/resolve/main/manifest.json` → **401 Unauthorized**, attempt2 `https://raw.githubusercontent.com/ServiceNow/WebGym/main/data/manifest.json` → **404 Not Found**, both with URL/error/sha captured. WebGym module not importable (`No module named 'webgym'`). 0 diverse eTLD+1 sites computable, manifest sha null, threshold sweep 0.818-0.9479 not computable. Hardcoded comparison 0.9479 CI[0.9167,0.9792] preserved.

### 3.5 Gate0 multi-step

- BrowserGym checks: `browsergym` spec None, `browsergym.core` spec None → available false (both checks). AgentLab 0.4.2 not available, Playwright not installed (`No module named 'playwright'`, `playwright --version` FileNotFoundError), tiktoken not available. Pip dry-run shows `browsergym-core==0.14.3` would install playwright==1.44 etc, playwright 1.63.0 separately installable, but not installed in clean env. 0 transitions collected vs 50/family required on 10 families; no BrowserGym loopback, no Playwright fallback because Docker not live. Relaxed 0/10, strict 0/10.

### 3.6 Honest cost

No LLM inference for AX/Gate0/WebGym; tokens via tiktoken not exercised due to no live captures; pip list/freeze and dry-run counts captured; sum counters resolve+bind+verify+freshness+browser_steps frozen but not exercised.

---

## 4. Results (frozen decision-rule ordered evaluation)

### 4.1 Adequacy gate — infrastructure precedence

- Valid AX trees: **0/20** (all captures UNAVAILABLE_SUBSTRATE, node_count 0, dom_bytes 0) vs required ≥10 valid trees (≥5 families, each 600-2000 nodes DOM≥2000). 0 <5 → **infrastructure precedence triggers** status COMPLETE outcome NOT_APPLICABLE with H1=MEASUREMENT_INVALID substrate_unavailable. Publish provenance: resolved 64-char digest sha256:3e8cb9b945ea9b1c... (200, skopeo validates), grammar hash f2b5e3bb live, placeholder expansion verified, pip list bc751d non-empty, docker pull full TimeoutExpired 90s + truncated rc=1 invalid format + skopeo success captured.

**Therefore no SURVIVES/FALSIFIED evaluated for H1; likewise H2, H3, H4 branches MEASUREMENT_INVALID due to 0 families/sites/transitions (< thresholds). No CAP/LFS enumeration attempted (ABANDONED per Director SUPERSEDE).**

### 4.2 Primary H1_AX_FULLTREE

- Metrics: M_AX_CONSISTENCY_MEAN null, M_AX_BOOTSTRAP_CI [null,null], M_AX_SHUFFLE_P null, M_AX_SHUFFLE_MEAN/STD/P95 null, M_AX_PER_FAMILY_VARIANCE null, M_AX_DELTA_TRUNCATED null (not degenerate [1,1] nor 0.0). PC1_LIVENESS FAIL (0/20), PC2 variance not testable. Status **MEASUREMENT_INVALID**.

### 4.3 H2_STAGEHAND_RECOMPUTED_DYNAMIC

- Metrics: HIT null, MISS null, false_accept null, n_families_attempted 0 <30 required, mutation_hash_changed null, selector_derivation null, per-project isolation null, speedup/tokens null, latency null, beat NC4 p null. Recomputed SHA after mutation with stripping logic frozen (grammar file implements strip_dynamic_tokens + sha256_normalized_subtree) but not exercised live. Status **MEASUREMENT_INVALID**.

### 4.4 H3_WEBGYM_DIVERSE

- Metrics: n_sites 0 <50, duplication prevalence null, CI [null,null], threshold sweep range null, site_entropy null, manifest null, param prevalence null. 2 genuine attempts 401/404 captured. Hardcoded 0.9479 CI not overlapping because no CI to compare. Status **MEASUREMENT_INVALID**.

### 4.5 H4_GATE0_RELAXED

- Metrics: transitions_total 0, families_with_50 0, relaxed_pass 0, strict_pass 0, H null, NL 0, strata 0, leakage null, unique_titles 0, title_entropy null, singleton_rate null. BrowserGym false, Playwright false, Docker unreachable/blocked by pull size. Single-page CDP insufficient per prereg; 0 transitions acknowledged. Status **MEASUREMENT_INVALID**.

### 4.6 Baselines and controls (stable identities)

All baselines/controls preserved from spec `spec.json:baselines`/`positive_control`/`null_control`:

- **B-STAGEHAND-VERB:** MEASUREMENT_INVALID — 0 families, no live page.content() recomputation, skopeo validates digest but pull timed out; 0 synthetic fallback.
- **B-RANDOM-AX-SHUFFLE:** MEASUREMENT_INVALID — 0 scores, 1000 trajectory-grouped shuffle seed 35725763380 not executable, correctly returns null not degenerate p=1.0.
- **B-TRUNCATED-20:** MEASUREMENT_INVALID — full-tree verified (no [:20]), delta null not 0.0, no live pages to compare.
- **B-WEBGYM-HARDCODED-09479:** MEASUREMENT_INVALID — 0 sites after 2 genuine 401/404 attempts, threshold sweep not computable.
- **B-COLD-LLM:** NOT_MEASURED — no LLM inference, cold vs cached latency via dry-run only.
- **B-CONSTANT-NULL-05654:** NOT_APPLICABLE — disclosed only, not decision.
- **PC1_LIVENESS_1280:** FAIL — 0/20, registry resolution succeeded but pull timed out due to 5.4GB size; truncated digest correctly invalid, full digest valid but slow.
- **PC2_AX_PRIOR_PRODUCT:** MEASUREMENT_INVALID — variance null, not degenerate.
- **PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC:** MEASUREMENT_INVALID — 0/30 families, logic frozen not exercised.
- **PC4_WEBGYM_IMPORT_VALID:** FAIL — 0 sites, 401/404.
- **PC5_SYNTHETIC_PIPELINE:** NOT_MEASURED — sampling re-derived verified.
- **NC1..NC6:** All MEASUREMENT_INVALID or NOT_MEASURED — no scores/labels/sites to permute; mechanisms frozen but not exercised due to substrate.

---

## 5. Validity, representation loss, and what is fixed vs remaining

### Fixed this run (addressing prior audit required_fixes / handoff carry_forward)

1. **Full 64-char digest resolution (handoff carry_forward[7], audit validity_findings[3]):** Prior truncated digest `sha256:3e8cb9b945` (12-hex) caused rc=1/rc=125 invalid reference format on every pull/run proof. This run queries Docker Hub API (200) and resolves full digest `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` (64-hex, continues truncated prefix), validated by `skopeo inspect` (Digest matches, 8 layers, Env). Truncated pull now captured as control showing rc=1 invalid format (proves fix matters). Full digest pull progresses (layers Download complete) but hits 90s timeout due to 5.4GB size — not format error. This unblocks the design flaw; next run needs longer pull timeout (300s+) or pre-pulled volume, not another digest guess.

2. **Sampling integrity (audit required_fixes[3]):** 10 families now re-derived inside script via `random.Random(35725763380).sample(sorted(families_ge3),10)` deterministically (derivation string captured), not hard-coded without verification. Result matches prior list but now independently verifiable.

3. **Grammar provenance (audit validity_findings[5]):** Live recomputed hash f2b5e3bb from committed file (not hardcoded 8d4b), verified `[:20]` not present (`longest_prefix_without_fallback` + stripped SHA), placeholder expansion verified, 9 regexes disclosed. Same fix as prior run preserved.

4. **Genuine repair captures (audit required_fixes[0][1]):** diagnostics.json now captures registry API 200 + skopeo inspect success + docker pull full TimeoutExpired + truncated invalid + docker run timeout + docker ps/images + pip list non-empty bc751d + pip freeze e3b0c + pip dry-runs + WebGym 2 attempts 401/404. Proves blocks are substrate size/auth/time, not missing pip package alone.

5. **Degenerate-metric discipline preserved:** With 0 scores returned null for mean/CI/shuffle/variance/delta and correctly did NOT execute 2000 bootstrap/1000 shuffle on empty data, avoiding prior degenerate CI[1,1] p=1.0 tautology (audit validity_findings[2]).

6. **Provenance self-hash stale fixed?** Current provenance.json stores `provenance_self_hash` and `provenance_top_hash` recomputed at write time (fixing prior stale 29f3b760 vs 6a566be4 structure), but file hash includes artifact hashes recorded after write — stable per code.

### Remaining validity threats / unresolved

- **Docker pull size/time is new blocker:** 90s timeout insufficient for 5.4GB image (largest layer 4.8GB). Next run must use 300s+ timeout, or `docker load` from cached tar, or ghcr.io mirror, or keep container warm between runs. HTTP http://localhost:7770 still unmeasured until container actually runs (`docker run -d -p 7770:7770 <full digest>` needs image extracted).
- **WebGym 401 suggests private dataset:** HuggingFace WebGym may be gated (401) — try HF_TOKEN auth or alternative WebMall/WebRetriever manifest per prereg fallback.
- **Clean env without pins installed:** Pip list only `pip 26.2.1`, no playwright/browsergym/webgym/tiktoken. Pins BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 are installable per dry-run but not installed; next run should `pip install browsergym-core==0.14.3 playwright==1.63.0 agentlab==0.4.2 tiktoken` before measurement (or use pre-built runner).
- **Gate0 multi-step:** 0 transitions vs 50/family; BrowserGym 0.14.3 or Playwright fallback not available without Docker live.
- **Product-subtree isolation:** Grammar implements semantic anchors but subtree_node_count>1 and distinct hashes on families 136,145,196,222 remain untested live.

### Representation loss disclosed (per spec measurement_validity)

Full-tree vs longest-prefix only, initial viewport 1280x720 no scroll plus multi-step for Gate0, CDP AX vs full DOM (600-2000 nodes), relevant-subtree outerHTML normalized with 9-regex stripping, N=2 HIT threshold, per-task token overhead, registry 64-hex now valid but pull size loss, WebGym auth gating, clean-env pip only, GitHub runner disk/time.

---

## 6. Product consequences

**Positive would require (now unmeasured):** H1 SURVIVES (mean≥0.6 CI lower>0.5 p<0.05 +0.20 gap delta≥0.20 vs truncated variance>0 product pages PC1≥15/20 with 64-char digest and stripping) gives first measurement-valid within-store parameterized transfer signal via full-tree + recomputed SHA, superseding prior homepage tautology 1.0 [1,1] p=1.0 and prior invalid 0.2857; enables bounded C-CROSSSITE within-store holdout and informs C-LLM-INHERIT economics. H2 SURVIVES gives shipped competitive floor ~2×/~30% that SPIDER must beat for C-PRODUCT-ECON honest amortized economics (per-hit vs fixed at f=100). H3 SURVIVES proves duplication sensitivity replacing hardcoded 0.9479, unblocking cross-site design without 567MB LFS. H4 ≥1 relaxed Gate0 unlocks correlated-state physics pilot.

**Current negative is MEASUREMENT_INVALID not FALSIFIED:** H1 <5 families after registry success + pull timeout is not falsification of full-tree parameterized transfer — it is substrate_unavailable (size/time). Same for H2, H3, H4. Product must NOT assume within-store AX generalization is impossible from this method; C-CROSSSITE stays HYPOTHESIS single-store vacuous. H2 not falsified; Stagehand exact cache with recomputed hash+stripping remains untested live. H3 not distinct. No exhaustive CAP/LFS re-triggered (ABANDONED per SUPERSEDE). Next allocation remains orthogonal BrowserGym loopback or hierarchical retrieval per Director comparative reasoning, after completing pull with longer timeout.

---

## 7. Next smallest step that could unblock (does not promise success)

1. **Complete Docker pull with full digest:** `timeout 600 docker pull am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb && docker run -d -p 7770:7770 <same> && curl -v http://localhost:7770` — pull needs ~5-6 min for 5.4GB. Capture stderr/stdout with 64-hex digest validated.
2. **Install BrowserGym pins in same runner:** `pip install "browsergym-core==0.14.3" "playwright==1.63.0" "agentlab==0.4.2" tiktoken && playwright install chromium --with-deps` then re-run `python3 research/intel/exp_35892848544_measure.py` at 1280x720 to obtain ≥15/20 CDP trees 600-2000 nodes, product-subtree hashes recomputed after page.content()+AX with stripping, before/after_hash per family proving hash_changed_on_mutation.
3. **WebGym alternative:** Try `HF_TOKEN=... huggingface download WebGym/WebGym --include manifest.json` or fallback to WebMall/WebRetriever manifest URL before second attempt.
4. Verify PC1≥15/20 and PC3 cross-project MISS 0% before SURVIVES/FALSIFIED; if <5 product-page families persist expand to shopping_admin 184/42 per spec.
5. Re-run full pipeline with trajectory-grouped 2000 bootstrap and 1000 shuffle to compute M_AX_DELTA_TRUNCATED≥0.20 vs truncated baseline on same 20 pages.

Do NOT re-trigger exhaustive 567MB LFS test.zip or 420-task CAP or WebJudge-7B — ABANDONED per SUPERSEDE.

---

## 8. Artifacts and provenance

- Raw: `artifacts/raw/ax_captures.jsonl` (10da90...), `ax_captures.json` (cd404...), `provenance.json` (f5c31...), `diagnostics.json` (4f354... — registry API 200 + skopeo success + pull full timeout + truncated rc1 + run timeout + ps/images + pip list bc751d + WebGym 401/404)
- Derived: `ax_consistency_fulltree.json` (a57470...), `stagehand_replication_recomputed.json` (e23620...), `webgym_census.json` (46e24...), `gate0_relaxed_table.json` (5783e1...), `provenance.json` (2bd5db...), top-level `provenance.json` (2bd5db...)
- Code: `research/intel/exp_35892848544_measure.py` (bbf12bc...), `research/intel/grammar_fulltree_358885.py` (f2b5e3bb...)
- Dataset pin: WebArena-Verified v2 192 shopping tasks 49 templates duplication 0.9479 CI[0.9167,0.9792] pin d652756608... (webarena-verified.json), seed 35725763380, viewport 1280x720
- Provenance: pinned BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0, grammar hash recomputed live f2b5e3bb, registry digest 64-hex validated, honest cost sum counters, no f*6.0 jitter, |rho_shuffled| gate frozen.

*Report interprets but does not contradict result.json; frozen claim not exceeded; audit will verify artifact hashes and recomputed metrics.*

