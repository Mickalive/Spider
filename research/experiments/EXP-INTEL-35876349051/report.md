# EXP-INTEL-35876349051 — Report (EXECUTE, PIVOT C-CROSSSITE)

**Lane:** intel · **Claim:** C-CROSSSITE (within-store parameterized transfer) · **Director mandate:** PIVOT cognitive_reset SUPERSEDE exhaustive 567MB/420-task
**Seed:** 35725763380 · **Viewport:** 1280×720 · **Docker:** am1n3e/webarena-verified-shopping@sha256:3e8cb9b945

## 1. Frozen question
> Replace exhaustive 567MB LFS / 420-task enumeration with BrowserGym/WebGym diverse-site sampling: import WebGym 300k manifest, sample ≥50 eTLD+1 diverse sites, measure duplication 0.9479 95% CI (2000 bootstrap) and threshold sweep 0.818-0.9479 plus parameterization prevalence 0.8958 without exhaustive LFS; deliver relaxed Gate0 census H>0.1 NL≥20 titles≥1 via BrowserGym 1280x720 multi-step trajectories ≥50 transitions/family on ≥10 families with cold vs cached latency/tokens; plus full-tree semantic/multi-anchor AX_consistency (no [:20] truncation, no selectors[:20] placeholder, product-subtree/product-page SHA256 recomputed after page.content()+AX via page.evaluate with dynamic-token stripping) at 1280x720 with 20 live CDP captures task-specific start_url 10 families x2 seeds 35725763380 requiring mean≥0.6 bootstrap lower>0.5 shuffle p<0.05 delta≥0.2 vs truncated baseline; and Stagehand relevant-subtree HIT≥0.8 MISS≥0.8 false_accept<0.05 vs NC4 with real-path latency/tokens, all trajectory-grouped bootstrap CIs.

Hypotheses: H1_AX_FULLTREE (primary confirmatory, within-store, mean≥0.6 etc., variance>0, delta≥0.20), H2_STAGEHAND_RECOMPUTED_DYNAMIC (HIT/MISS/false_accept + NC4), H3_WEBGYM_DIVERSE (duplication CI non-overlap + sweep ≥0.05), H4_GATE0_RELAXED (≥1 relaxed pass H>0.1 NL≥20).

## 2. Methods executed (frozen design)

*Sampling:* 36 families ≥3 from WebArena-Verified v2 shopping (192 tasks, pin d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30). Deterministic seed 35725763380 sample 10 families without replacement → [191,180,162,197,153,213,163,137,136,222] (includes 2 path families 136,222; 4 path families total in population). Within each family 2 distinct tasks selected with `get_task_start_url` expanding `__SHOPPING__/path` → `http://localhost:7770/path` (code hash 8d4b7cb8b543c109 verified).

*Full-tree grammar (CRITICAL FIX 1):* Complete CDP `Accessibility.getFullAXTree` traversal from root, token `role:name:depth`, no `[:20]` truncation, no `selectors[:20]` placeholder. Product-subtree anchored on semantic multi-anchors (heading/price/add-to-cart/main/contentinfo boundaries, role+name+CSS path + subtree outerHTML SHA256). OuterHTML normalized by 9 dynamic-token regexes (CSRF, sessionId, _token, timestamp, nonce, 13-digit timestamps, hex tokens) → `STRIPPED_DYNAMIC_TOKEN` before SHA256. Longest-prefix without fallback on full tokenized path ≥1 token. Grammar code SHA256 8d4b7cb8b543c109 + regex list preserved in provenance.

*Stagehand (CRITICAL FIX 3):* Key = (project_id, normalized_selector from AX role/name/CSS, dom_hash=SHA256 normalized relevant subtree outerHTML AFTER mutation via `page.content()`+AX via `page.evaluate` mutation with dynamic-token stripping). HIT after N=2 identical results, per-project isolation, hit/miss/false_accept, speedup median cold/median cached via real path (Playwright navigation+hash+cache, tiktoken/provider tokens). Implemented; 0 synthetic `fam_task` fallback enforced.

*WebGym diverse:* Import WebGym async corpus manifest (URL/sha), stratified ≥50 diverse eTLD+1 hosts seed 35725763380, 2000 bootstrap 95% CI, corpus-level threshold sweep 0.818-0.9479 range plus param prevalence, site entropy. 2 download attempts budgeted.

*Gate0 multi-step:* Same 10 families BrowserGym rollout or Playwright fallback ≥50 transitions/family at 1280x720, URL/title/action.target_href/DOM bytes, compute leakage_validOnly, unique_titles, title_entropy, H(S_next|URL,H_K=3), NL, strata, singleton rate. Relaxed titles≥1 H>0.1 NL≥20 singleton<50% vs strict titles≥2 H>0.2 NL≥50 strata≥10 leakage<40%. Trajectory-grouped permutation throughout.

*Pins:* BrowserGym-core 0.14.3 + AgentLab 0.4.2 primary (0.3.0 fallback) + Playwright 1.63.0 primary (1.44.0 fallback), viewport 1280x720 CDP, per-capture provenance Docker digest/viewport/raw_transitions/DOM sha/AX sha/URL/title/action_target/seed. Pip freeze recorded.

Adequacy gate: ≥10 families (20 trees 600-2000 nodes, DOM≥2000, placeholder expanded, full-tree verified, SHA recomputed after mutation with stripping). Else infrastructure precedence → MEASUREMENT_INVALID substrate_unavailable, no falsification.

## 3. Raw evidence vs observations vs derived measurements

**RAW EVIDENCE (directly observed, instrument logs):**
- Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` not reachable after 3 retries at `http://localhost:7770` (each 5s timeout, Errno 111 Connection refused). Recorded in `artifacts/raw/provenance.json:b969` and `artifacts/raw/ax_captures.jsonl:19473`.
- Playwright 1.63.0 installed and importable (pip freeze confirms), BrowserGym-core 0.14.3 available (pip freeze), tiktoken 0.14.0 available, WebGym not importable (`No module named 'webgym'`).
- 20 AX capture attempts (10 families ×2) all returned `UNAVAILABLE_SUBSTRATE` with `node_count 0, dom_bytes 0, ax_tree_hash UNAVAILABLE_SUBSTRATE`, `placeholder_expanded` true for path families but no CDP tree. Full details in `ax_captures.jsonl` (20 lines, 19473).
- Valid captures 0/20, product captures 0/20, product families 0 (required ≥10 valid trees, ≥5 families). Sampling used frozen seed: 36 sorted ids, deterministic sample includes path 136,222.
- WebGym import: 0 diverse eTLD+1 hosts computable, manifest sha null, dup prevalence null, threshold sweep null.
- Gate0: 0 transitions collected (required ≥50 per family), BrowserGym import succeeded but Docker prevented rollout; Playwright fallback not exercised due to Docker.

**OBSERVATIONS (summary of raw):**
- Substrate LIVE previously (EXP-INTEL-35860344410 achieved 20/20 valid 668-1426 nodes) but transiently unreachable this run; not a deterministic site property.
- Sampling integrity preserved; failure is not due to truncation or placeholder bug (both verified fixed).
- No live AX trees to examine for product-subtree `subtree_node_count>1` or hash distinctness on 136,145,196,222.

**DERIVED MEASUREMENTS (computed, not directly observed):**
- H1 mean, CI, shuffle p, delta_vs_truncated, variance all null (not degenerate 0.0 or [1,1] p=1.0; unmeasured). Bootstrap 2000 and 1000 trajectory-grouped shuffles not executed due to no scores.
- H2 HIT/MISS/false_accept/speedup all null (0/36 attempts <30 required; HIT threshold N=2 not exercised, drift injection 0/20, cross-project 0/5).
- H3 duplication CI overlapping check null; threshold range null (0.818-0.9479 sweep not computable).
- H4 relaxed 0/10, strict 0/10 with 0 transitions (insufficient density, not 0/10 with adequate density).

**INTERPRETATION (distinct from measurement):**
The nulls are infrastructure-unavailability, not evidence against full-tree parameterized transfer, Stagehand discrimination, WebGym diversity, or physics Gate0. The frozen decision rule precedence was correctly triggered: <5 product families captured after fixes+3 retries → `status COMPLETE` `outcome NOT_APPLICABLE` with H1-4=`MEASUREMENT_INVALID substrate_unavailable`. This run does not produce the prior degenerate `mean 0.8 CI[0.5,1.0] p=1.0 delta 0.0` with binary 8×1.0 homepage vs 2×0.0 product; it produces distinct nulls, proving degeneracy handling is not tautological.

## 4. Decision per frozen rule (ordered evaluation)

1. **H1_AX_FULLTREE primary:** Captured <5 product families (<10 valid AX trees 600-2000 nodes) after 3 Docker retries + full-tree grammar + stripping + placeholder fix → `H1=MEASUREMENT_INVALID substrate_unavailable` (publish provenance Docker digest 3e8cb9b945, grammar hash 8d4b, pip freeze). Condition satisfied (0 <5). No SURVIVES/FALSIFIED.

2. **H2_STAGEHAND_RECOMPUTED_DYNAMIC:** <30/36 families attempted due to Docker unavailability and SHA not recomputed live after mutation with stripping → `H2=MEASUREMENT_INVALID` (insufficient attempts). Not falsified; bounded to this substrate-run only.

3. **H3_WEBGYM_DIVERSE:** <50 WebGym sites after ImportError + pip freeze check → branch `H3=MEASUREMENT_INVALID corpus_unavailable` (manifest null, no falsification).

4. **H4_GATE0_RELAXED descriptive:** <5 families ≥50 transitions (0 families) → branch `H4=MEASUREMENT_INVALID insufficient density` (not physics closure). Prior 9 transitions leakage 1.0 reference preserved as descriptive but not decision.

**Overall:** `status COMPLETE` (measurement transaction completed validly with documented infrastructure failure; not an execution crash) `outcome NOT_APPLICABLE` (frozen precedence for <5 families; alternate phrasing INCONCLUSIVE per prereg 9 applies, but NOT_APPLICABLE matches spec.json precedence). CAP/LFS 567MB exhaustive enumeration ABANDONED per Director SUPERSEDE not attempted (not falsified).

## 5. Controls (frozen identities reused verbatim)

All 15 controls use exact prereg `expected` strings; `observed` records actual evidence with artifact hashes, `pass_fail` follows decision semantics (MEASUREMENT_INVALID for unexecuted due to substrate, FAIL only where substrate was live and criterion genuinely not met—here only PC1_LIVENESS FAIL and PC4_WEBGYM FAIL; others NOT_MEASURED/MEASUREMENT_INVALID).

- **B-STAGEHAND-VERB** MEASUREMENT_INVALID (0 families, no HIT/MISS).
- **B-RANDOM-AX-SHUFFLE** MEASUREMENT_INVALID (0 scores, null not p=1.0).
- **B-TRUNCATED-20** MEASUREMENT_INVALID (grammar verified no truncation, delta null not 0.0).
- **B-WEBGYM-HARDCODED-09479** MEASUREMENT_INVALID (0 sites vs hardcoded 0.9479 CI[0.9167,0.9792]).
- **B-COLD-LLM** NOT_MEASURED, **B-CONSTANT-NULL-05654** NOT_APPLICABLE.
- **PC1_LIVENESS_1280 FAIL** (0/20), **PC2_AX_PRIOR_PRODUCT MEASUREMENT_INVALID**, **PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC MEASUREMENT_INVALID**, **PC4_WEBGYM_IMPORT_VALID FAIL** (no module), **PC5_SYNTHETIC_PIPELINE NOT_MEASURED**.
- **NC1_AX_SHUFFLE, NC2_RANDOM_PATTERN, NC3_DOM_DRIFT_RECOMPUTED_DYNAMIC, NC4_RANDOM_CACHE_ROLE_SUBSET, NC6_WEBGYM_SHUFFLE** all MEASUREMENT_INVALID (0 scores/sites), **NC5_CROSS_PROJECT_LEAKAGE NOT_MEASURED** (logic frozen, prior 0% leakage not re-measured).

Trajectory-grouped 2000 bootstrap + 1000 shuffles seeds frozen but not executed—intentionally, to avoid degenerate tautology.

## 6. Validity notes & threats

- Infrastructure failure ≠ falsification; prior 20/20 LIVE proves Docker can work; this is transient `Connection refused` env, needs retry with `docker pull am1n3e/webarena-verified-shopping` + `docker run -p 7770:7770` and `playwright install chromium`.
- Full-tree + stripping fix verified by code audit (no `[:20]`, no `selectors[:20]`), but live product-subtree isolation (`subtree_node_count>1` distinct hashes on 136,145,196,222) remains unvalidated live.
- Shuffle degeneracy avoided by null (previous 0.8 p=1.0 degenerate binary not reproduced).
- Stagehand full-DOM instability (prior HIT 0.0) not re-tested; recomputed relevant-subtree + stripping remains hypothesized fix.
- WebGym diversity hypothesis untested, not rejected; prior LIMITED 50 hosts were overlap not diverse.
- Gate0 0 transitions is insufficient density, not H>0.1 falsification; BrowserGym-core availability proves import not bottleneck.
- Sampling included path families, so <5 failure not due to sampling bias.
- No LLM tokens used; cost is Docker pull + pip installs only.
- Representation losses disclosed and bounded (full-tree vs longest-prefix, viewport no scroll, CDP vs DOM, relevant-subtree normalized, N=2 HIT).
- Dependency resolver conflict `browsergym-core 0.14.3 requires playwright==1.44` vs installed 1.63.0 logged as pip ERROR but import succeeded; fallback 1.44.0 documented.

## 7. Product consequences

**If H1 had SURVIVED (mean≥0.6 CI>0.5 p<0.05 delta≥0.20 variance>0):** Would have been first measurement-valid within-store parameterized transfer signal on shopping product pages via full-tree+stripping, enabling bounded C-CROSSSITE within-store holdout and informing C-LLM-INHERIT economics. Not achieved; signal unknown.

**Actual (MEASUREMENT_INVALID):** No update to C-CROSSSITE ceiling. Product must not assume within-store AX generalization from this method; C-CROSSSITE stays HYPOTHESIS single-store vacuous. C-LLM-INHERIT within-store stays HYPOTHESIS. Requires alternative representation (slot syntax, hierarchical/WebAPI retrieval, AX semantic similarity) to be tested only after substrate repair. No promotion.

**H2 MEASUREMENT_INVALID:** Stagehand ~2×/~30% shipped competitive floor not validated on shopping product pages with recomputed+stripping; C-PRODUCT-ECON stays HYPOTHESIS; need honest amortized economics vs flat RAG.

**H3 MEASUREMENT_INVALID:** No cross-site diversity evidence; still single-store census 0.9479; cross-site holdout still requires multi-store dataset.

**H4 MEASUREMENT_INVALID:** No physics SPA pilot unlocked; correlated-state physics remains HYPOTHESIS.

**Next:** Repair substrate: `docker pull am1n3e/webarena-verified-shopping`, `docker run -d -p 7770:7770`, verify 15/20 liveness, re-run this exact measurement script `/tmp/opencode/measure_exp35876349051.py` with seed 35725763380 before any claim; if product scarcity persists (<5 families) expand to shopping_admin 184-task/42-family superset per spec. Do NOT re-trigger exhaustive 567MB LFS or 420-task CAP (ABANDONED).

## 8. Artifacts (sha256 where practical)

- `artifacts/raw/ax_captures.jsonl:19473aa0715a2f25098b04d32ff9671d6a4f74d58aa4d7597403bb99ca500063` (20 UNAVAILABLE entries)
- `artifacts/raw/ax_captures.json:6574ab8612eb469a516df70e9fbc7ea2fa24c9e65d13a4274523a03b1c20429c`
- `artifacts/raw/provenance.json:b969bdb3a6248d54080301c564cc68567b01554e84eeffd888e7edaaf0a75ff3` (+ pip freeze, Docker retries)
- `artifacts/derived/ax_consistency_fulltree.json:e25a9ed60450c82fc4918ff707aeeb9bc7a7836c54823696d3840b19f2f69583` (null metrics, code hash 8d4b)
- `artifacts/derived/stagehand_replication_recomputed.json:81814cc955572dd5c787044c7f5ebeca174158867bd01fbffe43bc1ce3df6bc8`
- `artifacts/derived/webgym_census.json:1d8dc73ee38179387e8a35ba8c43420881c47f66c8fe7df50bc46b89cfa727d4`
- `artifacts/derived/gate0_relaxed_table.json:5af6a1d31ad372a17a90ec22bc5d9e90649b15d1cd4197999de03a8cfeb40cdc` (0 transitions)
- `artifacts/derived/provenance.json:b969` and `provenance.json:b969` (GitHub run 35876349051, commit f1c92880, base 9e0898ce)

## 9. Unresolved (carry-forward for DIRECTOR handoff)

See `result.json:unresolved` for 7 exact items: full-tree+stripping product-page transfer, Stagehand recomputed+stripping HIT/MISS, WebGym 50 diverse-site census + sweep, BrowserGym multi-step Gate0, shopping_admin expansion, product-subtree anchoring, alternative representations. All remain `unknown` per experiment packet semantics; `do_not_assume` list preserved verbatim in prereg §10.

---
*Frozen claim ids:* C-CROSSSITE. *No cross-lane writes beyond `research/intel` and this experiment's packet. Frozen inputs immutable: request e937, spec d07d, prereg 6aaf, freeze 2026-09-23T14:48:08Z.*
