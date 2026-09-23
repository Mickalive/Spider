# EXP-INTEL-35881414325 Report — Intel REOPEN C-CROSSSITE (SUPERSEDE) — Third Retry

**Lane:** intel — `research/intel` only  
**Claim:** C-CROSSSITE (HYPOTHESIS) — auxiliary C-MEAS-VALID, C-WEB-DYNAMICS (Gate0), C-PRODUCT-ECON (Stagehand economics) descriptive  
**Experiment ID:** EXP-INTEL-35881414325 — seed 35725763380 — Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770 @1280x720  
**Status:** COMPLETE — **Outcome: NOT_APPLICABLE — MEASUREMENT_INVALID substrate_unavailable (all 4 branches)** — *Infrastructure precedence prevents any SURVIVES/FALSIFIED inference*

---

## 1. Frozen question

Director binding (REOPEN, cognitive_reset true, SUPERSEDE): Can BrowserGym/WebGym diverse-site sampling replace exhaustive 567MB LFS/420-task enumeration via (a) WebGym 300k >=50 eTLD+1 diverse-site duplication 0.9479 95%CI 2000 bootstrap + threshold sweep 0.818-0.9479 + parameterization 0.8958, (b) relaxed Gate0 H>0.1 NL>=20 via BrowserGym 1280x720 multi-step >=50 transitions/family >=10 families with cold vs cached latency/tokens, (c) full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, SHA recomputed after page.content()+AX via page.evaluate with dynamic-token stripping) at 1280x720 with 20 live CDP captures task-specific start_url 10 families x2 requiring mean>=0.6 bootstrap lower>0.5 shuffle p<0.05 delta>=0.20 vs truncated, (d) Stagehand recomputed+stripping HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 with real-path latency/tokens, all trajectory-grouped 2000 bootstraps.

Smallest high-information pilot: 10 families x2 product pages (20 CDP) + 36-family Stagehand recomputed + 50-site WebGym diverse + 10-family multi-step strive 50 transitions each. No CAP/LFS exhaustive (ABANDONED per Director SUPERSEDE).

## 2. What was actually measured

### 2.1 Raw evidence (distinct from interpretation)

- **Docker substrate:** 3 retries to http://localhost:7770 → URLError [Errno 111] Connection refused (identical to EXP-INTEL-35876349051). `docker_reachable false` in provenance. This env has no Docker daemon bound to 7770 and no playwright/browsergym installed (vs prior env had playwright 1.63.0 + browsergym-core 0.14.3 installed but same Docker failure). 20/20 prior success on same image at 1280x720 (EXP-INTEL-35860344410: node counts 668-1426, DOM 196k-251k) proves substrate *can* be live; this is transient env failure not site impossibility.
- **AX captures:** 20 attempts (10 families [191,180,162,197,153,213,163,137,136,222] x2 tasks) — all `UNAVAILABLE_SUBSTRATE` node_count 0 dom_bytes 0. Placeholder expansion `__SHOPPING__/path -> http://localhost:7770/path` verified in each artifact (code audit), full-tree grammar without [:20] verified (code hash 8d4b7cb8b543c10912f5d4325ccee0e5ae839f64c534a354f5ac8e7b1a364a45), dynamic-token regex list 9 patterns frozen before capture. No CDP AX trees 600-2000 obtained.
- **Stagehand:** 0/36 families attempted (require >=30 HIT, >=20 drift, >=5 cross-project). No page.content() recomputed SHA after page.evaluate mutation, no before_hash/after_hash, no selector derivation. Per-project isolation key includes project_id (prior 5 tests 0% leakage) but not re-measured. 0 synthetic fam_task fallback.
- **WebGym:** Module not importable (`No module named 'webgym'`), pip freeze shows no webgym. 0 sites, manifest null, threshold sweep not computable. Hardcoded 0.9479 CI[0.9167,0.9792] pin d652... preserved.
- **Gate0 multi-step:** 0 transitions total (require 50/family x10 =500). BrowserGym-core not available in this env; prior env had 0.14.3 available but Docker still blocked rollout. Single-page fallback would be 0 families; trajectory-grouped permutation not executable.

**Artifact hashes (sha256):**
- `artifacts/raw/ax_captures.jsonl:65c3381c0ebb5e8cc10a99e1f4b590ac219d7faafac46acb8826113d301fc604` (20 UNAVAILABLE)
- `artifacts/raw/ax_captures.json:887d39e3cf8fe299d9a9fc0ddcf07df480d5e126b3c74ab2625620f0e9f46e0b`
- `artifacts/raw/provenance.json:648b4efd1a3a5cf365392d8e9de54e627dc6a323e1f475198eab88718e13893b`
- `artifacts/derived/ax_consistency_fulltree.json:d11e80309e3e00abd5f1e749eefb25a8d29486975178298136965989890b6672` (mean null, CI null, shuffle null)
- `artifacts/derived/stagehand_replication_recomputed.json:ccd1f0aecb4e6a4fbe23035bc100a7da940df5e65b9e03582becabacfbe8bb00`
- `artifacts/derived/webgym_census.json:d04f023ef1dc73d5706d9227591dbfae122465313a1585a44dadd1d9d4860137`
- `artifacts/derived/gate0_relaxed_table.json:f2d42749b05734ad2b46dd298a60035d77a143129d04a2bcf3e0143a8e4051f2`
- `artifacts/derived/provenance.json:75fb17a3beeb201f8faf322ef20f876334d9ff848c25341f98ff910c7d579820`
- `provenance.json:75fb17a3beeb201f8faf322ef20f876334d9ff848c25341f98ff910c7d579820`
- `research/intel/exp_35881414325_measure.py:5b3286d5bc924695a7fbba561362a84682cb85362d4c4f71bdfbf0e007cdca7e` (grammar hash 8d4b)

### 2.2 Derived measurements (observations → measurements)

All primary metrics are `null` with explicit `MEASUREMENT_INVALID` status, not degenerate numeric values:

- `M_AX_CONSISTENCY_MEAN null`, `M_AX_BOOTSTRAP_CI_LOWER null`, `M_AX_SHUFFLE_P null`, `M_AX_DELTA_TRUNCATED null`, `M_AX_PER_FAMILY_VARIANCE null` — adequacy gate (<5 families with <10 valid trees after 3 retries) fails, so infrastructure precedence triggers NOT_APPLICABLE. Critically this run returns `null` not binary 8×1.0+2×0.0 degenerate nor single-value 0.2857 truncated fallback, avoiding tautological CI[1,1] p=1.0.
- `M_STAGEHAND_HIT_RATE null`, `M_STAGEHAND_MISS_RATE null`, `M_STAGEHAND_FALSE_ACCEPT null`, `speedup null`, `tokens_saved null` — 0/30 families < required, no NC4 shuffle, no before_hash/after_hash.
- `M_WEBGYM_DUP_PREVALENCE null`, `M_WEBGYM_THRESHOLD_SWEEP_RANGE null`, `M_WEBGYM_MANIFEST_SHA256 null` — 0/50 sites, UNAVAILABLE.
- `M_GATE0_TRANSITIONS 0`, `M_GATE0_RELAXED_PASS_COUNT 0`, `M_GATE0_H null`, `M_GATE0_NL 0` — 0 vs 50/family required, singleton strata not computed.

No 2000 family-level bootstrap or 1000 trajectory-grouped shuffle was executed on missing scores (correctly avoided degenerate execution).

### 2.3 Controls (stable identifiers, pass/fail)

| ID | Expected | Observed | Verdict |
|---|---|---|---|
| B-STAGEHAND-VERB | HIT>=0.8 MISS>=0.8 false<0.05 beats NC4 real-path | Not executed 0 families, recomputed+stripping frozen not exercised | MEASUREMENT_INVALID |
| B-RANDOM-AX-SHUFFLE | trajectory-grouped p<0.05 mean+0.20 | Not computed 0 scores, null not degenerate | MEASUREMENT_INVALID |
| B-TRUNCATED-20 | delta>=0.20 vs [:20] | Full-tree verified 8d4b but no live delta | MEASUREMENT_INVALID |
| B-WEBGYM-HARDCODED-09479 | CI non-overlap + sweep>=0.05 | WebGym UNAVAILABLE 0 sites | MEASUREMENT_INVALID |
| B-COLD-LLM | cold upper bound tokens/latency | Not measured (no LLM, no live) | NOT_MEASURED |
| B-CONSTANT-NULL-05654 | disclose only | Not used | NOT_APPLICABLE |
| PC1_LIVENESS_1280 | >=15/20 600-2000 nodes DOM>=2000 | 0/20 FAIL Connection refused 3 retries | FAIL |
| PC2_AX_PRIOR_PRODUCT | >=1 family variance>0 vs 1.0 degenerate | Not testable 0 captures | MEASUREMENT_INVALID |
| PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC | 3 consecutive HIT 2nd/3rd per-project 0% | Not executed 0 families | MEASUREMENT_INVALID |
| PC4_WEBGYM_IMPORT_VALID | >=50 sites manifest + sweep | FAIL 0 sites | FAIL |
| PC5_SYNTHETIC_PIPELINE | diagnostic only | Not executed | NOT_MEASURED |
| NC1_AX_SHUFFLE_TRAJECTORY_GROUPED | p<0.05 +0.20 | Not computed | MEASUREMENT_INVALID |
| NC2_RANDOM_PATTERN | <0.2 | Not computed | MEASUREMENT_INVALID |
| NC3_DOM_DRIFT_RECOMPUTED_DYNAMIC | MISS>=0.8 false<0.05 hash change | Not executed 0 families | MEASUREMENT_INVALID |
| NC4_RANDOM_CACHE_ROLE_SUBSET | beats p<0.05 | Not computed 0 labels | MEASUREMENT_INVALID |
| NC5_CROSS_PROJECT_LEAKAGE | 0% | Not re-measured (prior 0% frozen) | NOT_MEASURED |
| NC6_WEBGYM_SHUFFLE | p<0.05 + range>0.05 | Not computed | MEASUREMENT_INVALID |

Infrastructure precedence: PC1 FAIL + <5 families → overall H1 MEASUREMENT_INVALID, not FALSIFIED. All other Hs branch-level MEASUREMENT_INVALID only.

## 3. Decision rule evaluation (frozen ordered)

Per spec.json decision_rule + prereg §9, infrastructure precedence over falsification; CAP/LFS ABANDONED per Director SUPERSEDE:

1. **H1 gateway:** `<5 families with task-specific product pages captured (<10 valid AX trees 600-2000 nodes) after 3 Docker retries + full-tree grammar + dynamic stripping + placeholder fix` → TRUE (0/20, 0 families). Therefore `status COMPLETE outcome NOT_APPLICABLE H1=MEASUREMENT_INVALID substrate_unavailable`. No SURVIVES/FALSIFIED evaluation permitted. Prior 20/20 proof (EXP-INTEL-35860344410) confirms repairability.

2. **H2:** `<30/36 families attempted or SHA not recomputed after mutation with stripping` → TRUE (0/30). `H2=MEASUREMENT_INVALID`.

3. **H3:** `<50 WebGym sites` → TRUE (0/50). `H3=MEASUREMENT_INVALID` branch only.

4. **H4 Gate0:** `<5 families >=50 transitions` → TRUE (0/5). `H4=MEASUREMENT_INVALID` branch only (not physics closure).

No clause triggers SURVIVES or FALSIFIED-IN-SETTING because adequacy gates not met. Overall `SUPPORTS only if H1 and H2 SURVIVE` → not met; `INCONCLUSIVE if H1 MEASUREMENT_INVALID` → outcome is NOT_APPLICABLE (infrastructure invalid, not scientific INCONCLUSIVE).

## 4. Interpretation (do not collapse into observation)

- **No falsification of full-tree hypothesis:** 0/20 is not evidence full-tree semantic/multi-anchor product-subtree AX_consistency is impossible at mean>=0.6. The grammar fix (no truncation, 9 regex stripping, longest-prefix without fallback, SHA recomputed after page.content()+AX) remains hypothesis, verified by code audit 8d4b but unexercised live. Delta>=0.20 vs truncated remains untested (null not 0.0).
- **No falsification of Stagehand:** Prior full-DOM HIT 0.0 instability (CSRF/session/timestamp hashes 9fb4 vs a5a6) proves full-DOM key invalid, not Stagehand impossible. Recomputed relevant-subtree + stripping remains untested; HIT>=0.8 MISS>=0.8 false_accept<0.05 vs NC4 with real-path latency/tokens ~2x/~30% derived-only remains unknown.
- **WebGym diversity>depth untested, not falsified:** No manifest, no 0.818-0.9479 sweep, no 50 eTLD+1 distinct from 0.9479 CI[0.9167,0.9792]. Exhaustive CAP/LFS remains ABANDONED, correctly not re-triggered.
- **Gate0 not closed:** 0 transitions is MEASUREMENT_INVALID insufficient density, not evidence H>0.1 impossible. BrowserGym loopback not the bottleneck (prior env proved 0.14.3 available); Docker is.

Product consequences of negative: C-CROSSSITE stays single-store vacuous HYPOTHESIS, C-LLM-INHERIT within-store stays HYPOTHESIS, requires alternative representation (slot syntax, hierarchical/WebAPI, AX semantic similarity) *only if* future live capture after repair still yields mean<0.6 or delta<0.20 with variance>0. Current run does not authorize that pivot.

## 5. Validity threats & representation loss

- **Single-store vacuous:** WebArena-Verified v2 is single Magento One Stop Market container; within-store transfer ≠ cross-site. This is disclosed, not assumed.
- **Infrastructure vs science:** Degenerate CI[1,1] p=1.0 avoided by null; trajectory-grouped permutation correctly not executed on missing data.
- **Representation loss (bounded):** full-tree vs longest-prefix only, relevant-subtree outerHTML normalized+stripped (choice), N=2 HIT, initial viewport no scroll for AX + multi-step for Gate0, CDP AX vs full DOM, per-task token overhead. Not exercised but hash disclosed.
- **Package availability degradation:** This env lacks playwright/browsergym/tiktoken vs prior env that had them; failure mode identical (Connection refused) so substrate_unavailable classification unchanged, but repair now requires `pip install playwright==1.63.0 browsergym-core==0.14.3 tiktoken` in addition to `docker pull + docker run -d -p 7770:7770`.
- **CAP/LFS not re-triggered** per Director comparative_reasoning correct; 0/10 strict Gate0 is MEASUREMENT_INVALID not global falsification.

## 6. What remains unknown (carry-forward)

- H1 full-tree mean>=0.6 etc on shopping product pages at 1280x720 with stripping (requires 20 live captures, path families 136,145,196,222 distinct hashes).
- H2 Stagehand recomputed+stripping HIT/MISS/false_accept beats NC4 with real-path latency/tokens derived-only on >=30 families.
- H3 WebGym 300k 50 diverse eTLD+1 duplication 95% CI non-overlap 0.9479 + threshold sweep >=0.05 + param ~0.8958.
- H4 relaxed Gate0 H>0.1 NL>=20 etc via 50 transitions/family on >=10 families (shopping_admin/Reddit/GitLab/Wikipedia/VisualWebArena/WorkArena).
- Whether shopping_admin 184-task/42-family expansion yields >=5 product-page families where 36-family sample yields scarcity.
- Product-subtree semantic anchoring failure mode (subtree_node_count=1 prior) isolation on Magento template.
- Orthogonal mechanisms (slot syntax, hierarchical/WebAPI, AX semantic similarity) as alternative to longest-prefix.

## 7. Next action (smallest unblocking step)

Per handoff recommended_action: `REPAIR_AND_RETRY_NARROW_PILOT` — `docker pull am1n3e/webarena-verified-shopping@sha256:3e8cb9b945; docker run -d -p 7770:7770; curl --retry 3 http://localhost:7770; pip install playwright==1.63.0 browsergym-core==0.14.3 tiktoken==0.14.0; playwright install chromium --with-deps` then re-run `research/intel/exp_35881414325_measure.py` with seed 35725763380 at 1280x720. Verify PC1 >=15/20 (600-2000 nodes, DOM>=2000) before claiming SURVIVES/FALSIFIED; if <5 product-page families persist with 36 families, expand to shopping_admin 184/42 superset per spec measurement_validity[1]. Re-test delta>=0.20, Stagehand >=30 families beats NC4, WebGym 50 diverse 2000-bootstrap CI + sweep, BrowserGym loopback >=50 transitions/family. Do NOT re-trigger exhaustive CAP 567MB LFS or 420-task enumeration. Await Global Director scheduled pulse.

---
*Provenance:* `research/experiments/EXP-INTEL-35881414325/provenance.json:75fb17a3beeb201f8faf322ef20f876334d9ff848c25341f98ff910c7d579820` — base_sha 207fae3645d1f7aa0d5a5c31d0614ba1d3de23a6, commit 5fb8a9379abae85c83974f89341b58fd80660371, seed 35725763380, Docker not reachable 3 retries, webarena pin d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30.

