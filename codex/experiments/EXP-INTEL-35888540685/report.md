# EXP-INTEL-35888540685 Report — Intel PIVOT C-CROSSSITE (SUPERSEDE) — Fourth Narrow Pilot with Genuine Repair Capture

**Lane:** intel — `research/intel` only  
**Claim:** C-CROSSSITE (HYPOTHESIS) — auxiliary C-MEAS-VALID, C-WEB-DYNAMICS (Gate0), C-PRODUCT-ECON (Stagehand economics) descriptive  
**Experiment ID:** EXP-INTEL-35888540685 — seed 35725763380 — Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770 @1280x720 — grammar f2b5e3bb live  
**Status:** COMPLETE — **Outcome: NOT_APPLICABLE — MEASUREMENT_INVALID substrate_unavailable (all 4 branches)** — *Infrastructure precedence prevents any SURVIVES/FALSIFIED inference*  
**Execution model:** muse-spark-1.2-contributor-free — measurement script research/intel/exp_35888540685_measure.py:271b72746f667dcf |

---

## 1. Frozen question (Director binding, PIVOT cognitive_reset SUPERSEDE)

> Can BrowserGym/WebGym diverse-site sampling replace exhaustive 567MB LFS/420-task CAP enumeration: (a) WebGym 300k manifest sample >=50 eTLD+1 diverse sites yields duplication 95% CI (2000 bootstrap) and threshold sweep 0.818-0.9479 plus param_task prevalence vs vacuous 0.9479, (b) relaxed Gate0 census H>0.1 NL>=20 titles>=1 via BrowserGym 1280x720 multi-step trajectories >=50 transitions/family on >=10 families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) with cold vs cached latency/tokens, (c) full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, product-subtree SHA256 recomputed via page.content()+AX with dynamic-token stripping) at 1280x720 20 live CDP captures task-specific start_url 10 families x2 seed 35725763380 requiring mean>=0.6 bootstrap lower>0.5 shuffle p<0.05 delta>=0.20 vs truncated, and (d) Stagehand relevant-subtree HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 random-role-subset null with real-path latency/tokens, all trajectory-grouped bootstrap CIs?

Smallest high-information pilot per prereg: 10 families ×2 product pages (20 CDP at 1280x720 with dynamic stripping) + 36-family Stagehand recomputed+stripping (derived selectors only, hash recomputed after mutation) + WebGym 300k 50-site diverse census + 10-family multi-step strive 50 transitions each. No CAP/LFS exhaustive (ABANDONED per Director SUPERSEDE, not attempted).

---

## 2. What was actually measured (RAW EVIDENCE separate from interpretation)

### 2.1 Substrate and genuine repair capture (CRITICAL FIX compliance)

- **Docker reachable probe:** 3 HTTP retries to http://localhost:7770 → `URLError [Errno 111] Connection refused` each 5s timeout. `docker_reachable false` in diagnostics.json and provenance.
- **Genuine docker pull (new vs prior importlib-only probe):** `docker pull am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` captured rc=1 stderr=`invalid reference format` (truncated 12-char digest invalid; Docker requires 64 hex chars). Alternative `docker pull am1n3e/webarena-verified-shopping` timed out after 30s (registry/network blocked). This proves the Director's digest pin `3e8cb9b945` is itself invalid reference format independent of network - a design flaw not captured in prior runs that only did `urllib` probe + `importlib.find_spec`.
- **Genuine docker run:** `docker run -d -p 7770:7770 am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` captured rc=125 stderr=`invalid reference format` same root cause.
- **Docker ps/images:** `docker ps -a` shows no containers; `docker images --digests` shows only ghcr.io runner images (firewall, api-proxy, etc.) - proves no Shopping image pre-pulled in this clean runner (vs prior handoff's 20/20 success on same image name but different env where image was pre-pulled).
- **Viewports:** 1280×720 frozen but not validated live due to substrate failure.
- **Environment:** Docker 28.0.4 available, pip 26.2.1, python 3.12.14, linux. Prior env had playwright 1.63.0 + browsergym-core 0.14.3 installed but same connection failure; this env is cleaner (only pip installed).

### 2.2 AX captures — full-tree with live grammar hash

- **Sampling re-derived inside script (fixes audit required_fixes[3]):** `random.Random(35725763380).sample(sorted(families_ge3),10)` deterministically re-derived inside measurement script, not hardcoded via constant without verification. Result [[191,180,162,197,153,213,163,137,136,222]] matches prior but now verified live; pool is 36 families >=3 sorted [101,136,137,...,370]. Derivation string stored in provenance `webarena_families_derivation` and `M_AX_SAMPLING_DERIVATION`.
- **Grammar hash recomputed live (fixes audit validity_findings[4]):** `research/intel/grammar_fulltree_358885.py` hash `f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a` recomputed via `hashlib.sha256(file.read())` at runtime, not hardcoded `8d4b7cb8b543c10912f5d4325ccee0e5ae839f64c534a354f5ac8e7b1a364a45` from prior unverifiable constant. File contains `extract_element_pattern_fulltree` with no `[:20]` slice, `strip_dynamic_tokens` with 9 regexes, `sha256_normalized_subtree`, `get_task_start_url` expansion, and `recompute_grammar_hash()`. Verified by grep audit.
- **Placeholder expansion:** `__SHOPPING__ -> http://localhost:7770/` and `__SHOPPING__/path -> http://localhost:7770/path` via `grammar_fulltree_358885.get_task_start_url` code hash verified, applied to each of 20 captures.
- **AX results:** 20 attempts (10 families ×2 per-family RNG SEED+fam_id shuffled) all `UNAVAILABLE_SUBSTRATE` node_count 0 dom_bytes 0, no `product_subtree_sha256` recomputed. Full-tree traversal code exists but not exercised on live CDP trees (no trees in 600-2000 node range). `longest_prefix_without_fallback` verified in code.

### 2.3 Stagehand recomputed+stripping

- **Status:** 0/36 families attempted (require >=30 HIT, >=20 drift, >=5 cross-project). No `page.content()+AX` recomputed SHA after `page.evaluate` mutation, no `before_hash`/`after_hash`, no `selector derivation` on live trees. Per-project isolation key `(project_id, normalized_selector, dom_hash_stripped)` frozen in grammar but not re-measured live. Synthetic fallback count 0.
- **Prior evidence preserved:** Full-DOM HIT 0.0 instability (hashes 9fb4... vs a5a6... on reload) still bounds full-DOM construction as invalid, but not Stagehand recomputed+stripping.

### 2.4 WebGym diverse holdout — 2 genuine download attempts captured (fixes prior importlib-only)

- **Module check:** `No module named 'webgym'` (same as prior).
- **Attempt 1:** `https://huggingface.co/datasets/WebGym/WebGym/resolve/main/manifest.json` → 401 Unauthorized (captured URL, status, error, sha256 null, bytes 0).
- **Attempt 2:** `https://raw.githubusercontent.com/ServiceNow/WebGym/main/data/manifest.json` → 404 Not Found.
- **Manifest sha256 null**, 0 sites, threshold sweep 0.818-0.9479 uncomputable. Hardcoded WebArena 0.9479 CI[0.9167,0.9792] pin d652... preserved as comparison only.
- **Fixes audit required_fixes[1]:** Now 2 genuine `urllib.request.urlopen` attempts with URL/error/sha256 capture per spec, not just `find_spec`. Shows huggingface auth required for WebGym dataset, not just missing pip package.

### 2.5 Gate0 relaxed census — multi-step trajectories

- **BrowserGym checks:** Both `browsergym` and `browsergym.core` specs None → `available false` double-verified (not single probe). Prior env had 0.14.3 but still Docker-blocked.
- **Transitions:** 0 total vs 50/family ×10 =500 required. H(S_next|URL,H_K=3) not computable (requires NL >=5 per stratum), leakage `validOnly` null, unique_titles 0.
- **Result:** `MEASUREMENT_INVALID` insufficient density (0 vs required), not physics closure.

### 2.6 Pip / provenance capture fixes

- **pip list:** `pip list` captured 47 bytes `pip 26.2.1` sha `bc751d3e417bb9ab202566f411a75268ac7f4ce2212283e8becab471aa0cebd0` non-empty (fixes prior `e3b0c442=sha('')` empty weak evidence per audit required_fixes[4]). `pip --version` also captured.
- **pip freeze:** Still empty 0 bytes sha `e3b0c442` because clean runner has only pip installed outside system - but now pip list proves non-empty capture, so empty freeze is correct for clean env not weak evidence.
- **pip install dry-run:** `pip install playwright==1.63.0 --dry-run` shows would install `greenlet-3.5.6 playwright-1.63.0 pyee-13.0.1` - proves installability but not installed.
- **playwright --version:** FileNotFound, confirms not installed.
- **Provenance self-hash recomputed at write time (fixes prior stale 132af476 vs 75fb17a3):** Both `artifacts/derived/provenance.json` and `provenance.json` share hash `6a566be48d2db131831f905346cc577271a052252636fffef3eee417056f7654` and correctly embed `provenance_self_hash` after rewrite.
- **Artifact hashes (sha256) — new live recomputed:**
  - `artifacts/raw/ax_captures.jsonl:10da90465c7aff84a904337ea5fb92fdef284af7604b05609de64e660c6bdf5` (20 UNAVAILABLE, not prior 65c3381c)
  - `artifacts/raw/ax_captures.json:cd404e58308f1cafae15a265e7fddc7e489b9bd9d0ce33d1209c416528c99fc3`
  - `artifacts/raw/provenance.json:b316c9d1b978fae2d8d330ec3bd16f41156f63e05b660d770692e8b88980b527`
  - `artifacts/raw/diagnostics.json:bf5b03783f45c002faf4b1399faafc80a457d31347313bd99a629b607453ecc7` (new: captures genuine docker pull/run/ps/images + pip list + WebGym download evidence)
  - `artifacts/derived/ax_consistency_fulltree.json:6232cedabfac5ced4c63063cfe9a2a2a6cd7fe88631061e61379811a80a8f9c0`
  - `artifacts/derived/stagehand_replication_recomputed.json:0adbbc69a268f759136e9501890840e226e5fe0a34091fbcce6b78a9d1b0c40c`
  - `artifacts/derived/webgym_census.json:cd8e35ca62b432725ffd100ceade26bd2a766a95022ef1adf341ad59754a31b6`
  - `artifacts/derived/gate0_relaxed_table.json:63ff74ddb8b683bcdb4293feead7943f1c8d59549cb985cf49e0dbcb152a2187`
  - `artifacts/derived/provenance.json:6a566be48d2db131831f905346cc577271a052252636fffef3eee417056f7654`
  - `provenance.json:6a566be48d2db131831f905346cc577271a052252636fffef3eee417056f7654`
  - `research/intel/exp_35888540685_measure.py:271b72746f667dcf33e72b730e3f5b768eb575e77102b0b83ba5bb2a1a6976d5`
  - `research/intel/grammar_fulltree_358885.py:f2b5e3bb0fe5cab452f24d3d1ed18205813ae207de579870b1a16f5f156d542a` (live recomputed)

### 2.7 Derived measurements — null not degenerate

All primary metrics `null` per infrastructure precedence, not degenerate numeric values:

- `M_AX_CONSISTENCY_MEAN null`, `M_AX_BOOTSTRAP_CI_LOWER/UPPER null`, `M_AX_SHUFFLE_P null`, `M_AX_DELTA_TRUNCATED null`, `M_AX_PER_FAMILY_VARIANCE null` — adequacy gate (<5 families <10 trees) fails → H1 MEASUREMENT_INVALID.
- `M_STAGEHAND_HIT_RATE null`, `M_STAGEHAND_MISS_RATE null`, `false_accept null`, `speedup null` → H2 MEASUREMENT_INVALID (<30 families).
- `M_WEBGYM_DUP_PREVALENCE null`, `M_WEBGYM_THRESHOLD_SWEEP_RANGE null` → H3 MEASUREMENT_INVALID (0/50 sites after 2 genuine attempts).
- `M_GATE0_TRANSITIONS 0`, `M_GATE0_RELAXED_PASS_COUNT 0` → H4 MEASUREMENT_INVALID (0 vs 50/family).

No 2000 bootstrap / 1000 shuffle executed on missing scores (correctly avoided degenerate CI[1,1] p=1.0 tautology per validity).

### 2.8 Controls — stable identifiers

| ID | Expected | Observed | Verdict |
|---|---|---|---|
| B-STAGEHAND-VERB | HIT>=0.8 MISS>=0.8 false<0.05 beats NC4 ~2x/~30% real-path derived only | 0 families; genuine pull/run invalid digest captured; recomputed+stripping code f2b5e3bb frozen | MEASUREMENT_INVALID |
| B-RANDOM-AX-SHUFFLE | trajectory-grouped p<0.05 mean+0.20 | 0 scores null not degenerate | MEASUREMENT_INVALID |
| B-TRUNCATED-20 | delta>=0.20 vs [:20] | full-tree f2b5e3bb verified no truncation but no live delta | MEASUREMENT_INVALID |
| B-WEBGYM-HARDCODED-09479 | CI non-overlap + sweep>=0.05 | 2 genuine attempts 401/404 → 0 sites | MEASUREMENT_INVALID |
| B-COLD-LLM | cold bound tokens/latency per-hit vs fixed f=100 | no LLM live, dry-run shows installable | NOT_MEASURED |
| B-CONSTANT-NULL-05654 | disclose | not used | NOT_APPLICABLE |
| PC1_LIVENESS_1280 | >=15/20 600-2000 nodes DOM>=2000 proven by genuine pull/run capture | 0/20 FAIL; pull rc1 invalid reference, run rc125 | FAIL |
| PC2_AX_PRIOR_PRODUCT | >=1 family variance>0 vs degenerate 1.0 | not testable 0 captures | MEASUREMENT_INVALID |
| PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC | 3 consecutive HIT 2nd/3rd per-project 0% | 0 families, code f2b5e3bb frozen | MEASUREMENT_INVALID |
| PC4_WEBGYM_IMPORT_VALID | >=50 sites manifest+sweep | FAIL 0 sites; 2 genuine attempts captured | FAIL |
| PC5_SYNTHETIC_PIPELINE | diagnostic only | sampling re-derived verified | NOT_MEASURED |
| NC1_AX_SHUFFLE | p<0.05 +0.20 | not computed 0 scores | MEASUREMENT_INVALID |
| NC2_RANDOM_PATTERN | <0.2 | not computed | MEASUREMENT_INVALID |
| NC3_DOM_DRIFT | MISS>=0.8 false<0.05 hash change per family | not executed 0 families; code f2b5e3bb verified | MEASUREMENT_INVALID |
| NC4_RANDOM_CACHE_ROLE_SUBSET | beats p<0.05 | not computed 0 labels | MEASUREMENT_INVALID |
| NC5_CROSS_PROJECT_LEAKAGE | 0% | not re-measured (prior 0% with stripping) | NOT_MEASURED |
| NC6_WEBGYM_SHUFFLE | p<0.05 range>0.05 | not computed | MEASUREMENT_INVALID |

---

## 3. Decision rule evaluation (frozen ordered, infrastructure precedence)

Per spec.json decision_rule + prereg §9 + falsifier, CAP/LFS ABANDONED per SUPERSEDE:

1. **H1 gateway** (`<5 families <10 trees after 3 Docker HTTP probes +  full-tree + stripping + placeholder`): TRUE (0/20). → `H1=MEASUREMENT_INVALID substrate_unavailable`. No SURVIVES/FALSIFIED. **New diagnostic:** truncated digest `3e8cb9b945` itself is invalid reference format, so even with retries no pull can succeed until Director pin corrected to 64-char digest.
2. **H2** (`<30/36 families or SHA not recomputed with stripping`): TRUE (0/30, no live before_hash). → `H2=MEASUREMENT_INVALID`.
3. **H3** (`<50 WebGym sites after 2 genuine attempts`): TRUE (0/50, 401/404 captured). → `H3=MEASUREMENT_INVALID` branch only.
4. **H4** (`<5 families >=50 transitions`): TRUE (0/5). → `H4=MEASUREMENT_INVALID` (not physics closure).

Overall `SUPPORTS only if H1 and H2 SURVIVE` not met; `INCONCLUSIVE if H1 MEASUREMENT_INVALID` → outcome `NOT_APPLICABLE` (infrastructure invalid, not scientific).

---

## 4. Interpretation — deliberate non-collapse

- **No falsification of full-tree hypothesis:** 0/20 with invalid digest truncation is not evidence parameterized transfer at mean>=0.6 is impossible. Grammar fix (f2b5e3bb no truncation, stripping, longest-prefix without fallback, placeholder expansion) remains hypothesis, now verifiable via committed file hash (not prior 8d4b unverifiable). Delta>=0.20 vs truncated remains untested (null not 0.0).
- **No falsification of Stagehand:** Prior full-DOM HIT 0.0 (hash instability) proves full-DOM key invalid, not Stagehand impossible. Recomputed relevant-subtree+stripping (grammar f2b5e3bb `strip_dynamic_tokens` + `sha256_normalized_subtree`) remains untested; HIT/MISS/false_accept vs NC4 with real-path ~2x/~30% still unknown.
- **WebGym diversity>depth untested:** No manifest after 2 genuine attempts (401 suggests hf auth required), so no 0.818-0.9479 sweep. Exhaustive CAP/LFS correctly not re-triggered.
- **Gate0 not closed:** 0 transitions is MEASUREMENT_INVALID insufficient density, not H>0.1 or NL>=20 impossibility. Shopping_admin 184/42 expansion not yet needed but available per spec if product scarcity persists after repair.
- **Digest truncation discovery:** Genuine pull/run capture reveals Director's digest `3e8cb9b945` (12 hex) will always be `invalid reference format` regardless of network; this explains 0/20 across all recent Intel PIVOT retries even where prior env had 20/20 with pre-pulled image. Next experiment's smallest unblocking step must resolve full 64-char digest via registry inspection on the env that achieved 20/20 (EXP-INTEL-35860344410).

Product consequences: C-CROSSSITE stays single-store vacuous HYPOTHESIS, C-LLM-INHERIT within-store stays HYPOTHESIS, C-PRODUCT-ECON Stagehand floor stays unvalidated. No promotion.

---

## 5. Validity threats & representation loss (honest cost disclosure)

- **Single-store vacuous:** WebArena v2 is single Magento One Stop Market container; within-store ≠ cross-site. Disclosed.
- **Infrastructure vs science:** Null metrics avoid degenerate CI[1,1] p=1.0; trajectory-grouped bootstrap/shuffle correctly not executed on missing data per validity.
- **Representation loss disclosed:** full-tree vs longest-prefix only, relevant-subtree outerHTML normalized+stripped (9 regexes) with `form_key` stripping choice, N=2 HIT, initial viewport 1280×720 no scroll, CDP AX 600-2000 vs full DOM, per-task token overhead, plus truncated digest design loss. All bounded.
- **Digest truncation as validity threat:** Truncated digest is now the primary measured failure mode (rc1/125 invalid format) distinct from connection-refused; correct fix is 64-char digest resolution before any live measurement validity can be claimed.
- **CAP/LFS ABANDONED** per Director comparative_reasoning correct; 0/10 strict Gate0 is MEASUREMENT_INVALID not global falsification.

All artifact CIs are trajectory-grouped / family-level (2000 bootstrap for future live, 1000 permutation) to avoid degenerate dependence, now correctly not executed on empty data.

---

## 6. What remains unknown (carry-forward, 9 items)

- H1 full-tree mean>=0.6 CI lower>0.5 p<0.05 delta>=0.20 variance>0 on shopping product pages with stripping at 1280×720.
- H2 Stagehand HIT/MISS/false_accept beats NC4 with real-path latency/tokens derived-only on >=30 families.
- H3 WebGym 50 diverse eTLD+1 duplication CI non-overlap 0.9479 + threshold sweep >=0.05.
- H4 relaxed Gate0 H>0.1 NL>=20 via 50 transitions/family >=10 families.
- Shopping_admin 184/42 expansion whether >=5 product families needs testing after digest fix.
- Product-subtree anchoring distinctness on Magento template (grammar f2b5e3bb not validated live).
- Orthogonal mechanisms (slot syntax, hierarchical/WebAPI, AX semantic similarity) excluded not closed.
- Pip freeze empty in clean env: explained by pip list non-empty, but next run should have playwright/browsergym installed for richer pip freeze.
- Docker digest truncation: full 64-char digest still unknown — must be recovered from prior successful env or registry API before next pull.

---

## 7. Next action — smallest unblocking step (repair and retry narrow pilot)

`REPAIR_AND_RETRY_NARROW_PILOT` (await Global Director scheduled pulse; do not self-authorize): Resolve full Docker digest for `am1n3e/webarena-verified-shopping` (inspect `docker images --digests` or `skopeo inspect` on prior successful runner that achieved 20/20, or query Docker Hub API for image@sha256:64char), then execute genuine `docker pull <image>@sha256:<64char>` + `docker run -d -p 7770:7770` with captured output, plus `pip install playwright==1.63.0 browsergym-core==0.14.3 tiktoken==0.14.0` with `pip list` non-empty capture and 2 WebGym manifest attempts with auth token, then re-run `research/intel/exp_35888540685_measure.py` seed 35725763380 at 1280×720. Verify PC1 >=15/20 before SURVIVES/FALSIFIED; if <5 product families persist, expand to shopping_admin 184/42. Do NOT re-trigger CAP 567MB LFS/420-task. Fix is blocked on Director digest correction + runtime BrowserGym 1280×720 provisioning dependency.

---

*Provenance:* `research/experiments/EXP-INTEL-35888540685/provenance.json:6a566be48d2db131831f905346cc577271a052252636fffef3eee417056f7654` — base_sha 0fed24199561113cd749cbcba2b61b4aa21c1b70, commit pending, seed 35725763380, Docker unreachable 3 retries + genuine pull rc1/run rc125 invalid reference format captured, webarena pin d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30, grammar f2b5e3bb live recomputed, WebGym 2 attempts 401/404 captured, pip list bc751d non-empty.
