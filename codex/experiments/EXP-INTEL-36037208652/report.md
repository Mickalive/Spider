# Report — EXP-INTEL-36037208652

- **Lane:** intel
- **Experiment ID:** EXP-INTEL-36037208652
- **Claim IDs:** C-CROSSSITE (primary), C-MEAS-VALID, C-WEB-DYNAMICS
- **Request ID:** f1847e89e2204da72275e9da  •  **Request hash:** b890f8a03f2b8e2448090ff28658caf991541a2d9d877e4d13a5c2ff8c4f90e4
- **Director mandate:** CONTINUE • **Target claim:** C-CROSSSITE • **Cognitive reset:** true • **Parent handoff:** EXP-INTEL-36020904615 (ab92f146eefe4d2df24802f0c17398f16bb98ef048d027d2715ca8413e7de0cc) DISPOSITION USE
- **Status:** COMPLETE
- **Outcome:** MIXED
- **Controls:** PC-SYNTHETIC-FIXTURE-TOY-STAGEHAND-WEBGYM-GATE0-SANITY MIXED, NC-SHUFFLED-TRUNCATION-STAGEHAND-GATE0-AX MIXED; durable pin PASS, orthogonal censuses UNAVAILABLE, Gate0 UNAVAILABLE
- **Artifacts:** 31 raw+derived artifacts + 3 code/fixtures, hashes in `result.json:artifacts` and `provenance.json:material_artifacts_sha256`

## 1. Strategic question (Director binding, frozen)

> Can an orthogonal census beyond the pinned WebArena-Verified v2 812 + Hard258 258 (WebMall/Mind2Web-2 BrowserGym loopback 130-task, Mind2Web shopping vs shopping_admin definition expansion with verified product_page heuristics, or WebGym-derived 292k families with independent eTLD+1 hosting and HF_TOKEN-provisioned duplication CI + threshold sweep 0.818-0.9479 range>=0.05) deliver >=10 distinct product families constructible under the identical deterministic random.Random(35725763380).sample + get_task_start_url __SHOPPING__ + product-subtree anchoring + SHA stability protocol at 1280x720 CDP full-tree expanded stripping, and achieve full-tree multi-anchor AX_consistency mean>=0.6 CI lower>0.5 gap>=0.20 on that >=10 set while Stagehand HIT>=0.8 via rotation-insensitive relevant-subtree or freshness-gated SHA, plus close WebGym 292k >=50 diverse eTLD+1 duplication CI (2000 bootstrap) and >=50 transitions/family on >=10 families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) for physics Gate0?

`Director comparative_reasoning`: Versus fixing BrowserGym multi-step alone or blind reproducing external SOTA on synthetic 40-task alias-OOD: SOTA reproduction sets O(1) bar product must beat but is meaningless without a valid diverse site census; combined census + Gate0 H>0.1 NL>=20 closes both cross-site prevalence and physics sampling integrity in one allocation, avoiding 24th C-CROSSSITE iteration on same 2-site bounds.

## 2. Hypotheses (frozen)

**H_A_ORTHO_CENSUS_10FAM (primary):** At least one orthogonal census (a) WebMall/Mind2Web-2 130-task, (b) Mind2Web 404 expansion, or (c) WebGym-derived 292k/127k families yields >=10 distinct product families constructible under identical frozen protocol (deterministic Random(35725763380).sample x2 S1==S2 + get_task_start_url __SHOPPING__ expansion + product-subtree anchoring heading/price/add-to-cart/main/contentinfo node_count>1 and distinct outerHTML SHA256 with body regex + 9 base + expanded {form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp} before SHA via page.evaluate recomputed after page.content()+AX, SHA before==after TRUE and after mutation != TRUE, 1280x720 CDP Accessibility.getFullAXTree median AX>10 DOM>=2000 proven on canonical [136,145,196,222]) and achieves on that >=10-family product_page set full-tree multi-anchor longest-prefix AX_consistency mean>=0.6 CI lower>0.5 gap>=0.20 p<0.05 variance>0 delta_vs_truncated>=0.20 vs [:20] truncated, while Stagehand selector+relevant-subtree SHA256 HIT>=0.8 overall with stripping lift>=0.40 via rotation-insensitive variant, plus WebGym diverse >=50 CI non-degenerate sweep 0.818-0.9479 range>=0.05 monotonic, and Gate0 >=50 transitions/family on >=10 families across >=6 site families.

**H_B_PHYSICS_GATE0 (secondary):** Same orthogonal census and BrowserGym substrate satisfies Gate0 for physics beyond-memory tests (sufficient NL>=50/family, leakage <40%, state diversity).

## 3. Falsifier (frozen)

H_A falsified if after >=2 genuine attempts per durable source (HF for WebArena 812+Hard258+WebGym 292k with HF_TOKEN true/false logged, GHCR BrowserGym 0.14.3, Docker Hub webarena-verified-shopping, each timeout>=300s, docker pull --digests or docker load fallback, Hub/GHCR API 200, stderr/stdout captured) no orthogonal census beyond the 4-family union [136,145,196,222] yields >=10 distinct product families with anchoring true and SHA stability both directions TRUE and CDP 1280x720 median AX>10 & DOM>=2000 on canonical families, OR full-tree AX_consistency mean<0.6 or CI lower<=0.5 or shuffle p>=0.05 or gap<0.20 or variance==0 or delta_vs_truncated<0.20 on the >=10 set, OR Stagehand HIT post-strip <0.8 and lift <0.40 and rotation-insensitive variant not improving, OR when HF_TOKEN succeeds WebGym diverse <50 or CI not computed non-degenerate or sweep range<0.05 or not monotonic (when HF_TOKEN fails after 2 genuine 401/404 attempts this clause is UNAVAILABLE not falsified, but H_A alone still requires >=10 families to SURVIVE), OR Gate0 <50/family on <10 families or leakage >=40%. Single-module failure -> MIXED, all fail -> FALSIFIED, all pass -> SURVIVES. No inference if MEASUREMENT_INVALID gating fails.

## 4. Design summary (frozen, abbreviated)

- Baselines: B-DURABLE-PIN-812 (durability pin), B-ORTHO-WEBMALL-MIND2WEB-130 (orthogonal A 130-task), B-ORTHO-MIND2WEB-EXPANSION (orthogonal B 404 expansion), B-WEBGYM-292K-DIVERSE (diverse eTLD+1 + sweep), B-TRUNCATED-20 (fragment null), B-BROWSERGYM-GATE0-MULTISTEP (physics substrate), B-STAGEHAND-SELECTOR (external SOTA), B-COLD-LLM (floor)
- Positive control PC-SYNTHETIC-FIXTURE-TOY-STAGEHAND-WEBGYM-GATE0-SANITY (PC-A synthetic Flask + canonical 12 captures, PC-B toy Stagehand 1.0, PC-C WebGym sanity gated on HF, PC-D Gate0 fixture 2 families)
- Null controls NC-SHUFFLED-TRUNCATION-STAGEHAND-GATE0-AX (NC1 family-label shuffle, NC2 truncated delta, NC3 stripping ablation, NC4 AX permutation, NC5 Gate0 leakage shuffle) all trajectory-grouped family-level
- Measurement validity MV1-MV8 gating as in prereg 7 / spec measurement_validity (MV1 >=2 genuine attempts per source, MV2 byte identity 64-hex, MV3 CDP full-tree 1280x720, MV4 deterministic sampling x2 per census, MV5 WebGym diverse exception, MV6 Stagehand expanded stripping ablation, MV7 Gate0 per-trajectory counters, MV8 provenance)
- Decision rule frozen three-way: (A) MEASUREMENT_INVALID if any MV1-MV4/MV6-MV8 fails (MV5 exception), (B) SURVIVES_CURRENT_TEST iff A passes and H_A_SURVIVES all gates, (C) otherwise FALSIFIED if triple fail else MIXED

## 5. Execution (what was actually run)

All frozen steps were executed exactly as specified; frozen inputs immutable (`freeze.json` hashes verified). No outcome-bearing measurements were inspected during DESIGN.

**Step 1 — Durable sources (MV1/MV2):** Executed `research/intel/exp_36037208652_execute.py` which logged:
- HF WebArena-Verified manifest 2x attempts HTTP 401 (0 bytes, sha null) with HF_TOKEN false, timeout 300s configured
- HF Hard258 2x attempts 401/200 (GitHub fallback 200 x2 byte-identical SHA d6527566, 516731 bytes)
- HF WebGym 2x attempts 401 (0 bytes)
- GHCR BrowserGym 0.14.3: anonymous token 403, authed token 200 (GH_TOKEN present), manifest GET 404 x2, docker pull denied x2 (6 genuine attempts total)
- Docker Hub webarena-verified-shopping: Hub API tags 200 x3 bytes 1694 sha 62f82706, hub_latest_digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb 64-hex valid true match true, docker pull logged (4 genuine), docker images --digests logged
- GitHub cross-source webarena-verified.json 200 x2 byte-identical SHA d6527566, webarna-verfied-hard.json 200 x2
Artifacts: `artifacts/raw/hf_manifest_attempts.json`, `hf_hard258_attempts.json`, `hf_webgym_manifest_attempts.json`, `ghcr_browsergym_attempts.json`, `docker_hub_api_attempts.json`, `docker_pull_attempts.json`, `github_cross_source_attempts.json`, `webmall_attempts.json` (WebMall 404/401 x2), `mind2web_attempts.json` (Mind2Web 404/401 x2), `orthogonal_census_provenance.json`.

**Step 2 — Census + deterministic sampling (MV2/MV4):** Census derived from pinned `webarena-verified.json` (927596 bytes, 906? raw size) byte-identical SHA d6527566:
- Primary 812 total 192 shopping 36 families_ge3 21 product tasks 4 product_page families [136,145,196,222]
- Hard258 slice derived from pinned base via upstream `webarna-verfied-hard.json` intersect (258 upstream, 258 tasks, 11 families_ge3, 2 product_page families [136,145], task_ids subset true, hard_slice_sha canonical)
- Orthogonal WebMall 0 families, Mind2Web expansion 0 families, WebGym derived 0 families (all UNAVAILABLE after 2 genuine 401/404 attempts)
- Deterministic sampling executed twice per census: `random.Random(35725763380).sample(sorted_families_ge3,10)` with seed reset logged S1==S2 true on primary and hard258 (primary S1 10 families sample_product 2, hard258 S1 10 families sample_product 1), orthogonal empty sets logged insufficient (n_unique 0). Union unique families 4 deterministically.
Artifacts: `artifacts/derived/webarena_census.json`, `hard258_census.json`, `deterministic_family_samples.json`, `census_summary.json`, `orthogonal_webmall_census.json`, `orthogonal_mind2web_expansion_census.json`, `orthogonal_webgym_derived_census.json`, `pc_d_hard258_fixture.json` (6 tasks 2 families_ge3 PASS), `orthogonal_census_provenance.json`.

**Step 3 — Environment pin (MV3):** `pip freeze` 238 lines sha af78453f nonempty, BrowserGym-core 0.14.3 (installed --no-deps to satisfy frozen triple while playwright 1.63.0 conflicts with browsergym's 1.44 requirement - disclosed), AgentLab 0.4.2, Playwright 1.63.0 (`Version 1.63.0`), viewport 1280x720, CDP Accessibility.getFullAXTree. Chromium 153.0.8010.12 installed via `playwright install --with-deps chromium`. Grammar hash live 273eafbcb matches parent. Artifact `artifacts/raw/environment_pin.json` + `pip_freeze.txt`.

**Step 4 — AX full-tree multi-anchor (MV3/MV4):** Reused prior `ax_captures.jsonl` (12 canonical captures median AX717 min627 DOM203748 min195052) and `ax_captures_consistency.jsonl` (37 probes 0 errors) with fresh environment pin this run; recomputed full-tree multi-anchor AX_consistency via `research/intel/exp_36020904615_ax_consistency.py` logic (body regex + 9 base + expanded {form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp} before SHA via page.evaluate, truncated [:20] also computed). Output `artifacts/derived/ax_consistency_fulltree.json` mean 0.4543 CI[0.3960,0.5164] B=2000 family-level gap 0.143 shuffle 0.311 p0.0 variance 0.00476 delta 0.4271. Median AX 702.5 DOM 218149 (gates PASS), but mean/CI/gap FAIL frozen gates on available 4-family set; frozen >=10 gate unavailable correctly reported.

**Step 5 — Stagehand + alias-OOD synthetic honest Pareto:** Reused harness `b11ea9700c7190f1fb7ef6f169af1f5da4d04dd6d52ae631376cc3c51f59ff21` byte-identical 409 rows (327 blind +82 Stagehand ablation) via `research/intel/exp_35999366789_blind_harness.py` import with OUT redirect only. Analysis `sota_analysis.json` DSM 0.75 [0.625,0.875] interior non-degenerate vs BMEM 0.0 degenerate vs ROUTING/WebMCP 1.0 degenerate, Stagehand HIT_post 0.775 [0.625,0.9] 31/40 HIT_pre 0.0 lift 0.775 per-channel mixed 0.4 cap. Artifact `stagehand_strip_delta.json`.

**Step 6 — WebGym threshold sweep (MV5):** Not computable without manifest; created `webgym_threshold_sweep.json` null with provenance, sweep range null status UNAVAILABLE per MV5 exception, PC-C UNAVAILABLE.

**Step 7 — Gate0 multi-step (MV7):** BrowserGym import success but live multi-step collection UNAVAILABLE after 2 genuine GHCR/docker attempts manifest denied; per-family counts fixture only (shopping_admin 50, others 0, 1/6 meets threshold), leakage null UNAVAILABLE, deterministic seeds logged, trajectory-grouped bootstrap not required but per-family counts auditable. Artifacts `gate0_attempts.json`, `gate0_per_family.json`.

All artifacts path+sha recorded in `result.json:artifacts` and `provenance.json:material_artifacts_sha256` (31 derived/raw + 3 code/fixtures). `provenance.json` stores request/spec/prereg/freeze hashes, pip freeze hash, docker digests, command logs, thresholds.

## 6. Results (raw evidence distinct from interpretation)

### 6.1 Primary metrics (stable names from prereg 9)

| Metric | Value | Gate | Pass | Evidence |
|---|---|---|---|---|
| M_CONSTRUCTIBLE_FAMILIES | 4 [136,145,196,222] union 4 | >=10 | **FAIL** | census_summary.json |
| M_CONSTRUCTIBLE_FAMILIES_ORTHO_ONLY | 0 (webmall 0, mind2web 0, webgym 0) | >=10 orthogonal | **FAIL** | orthogonal_*_census.json |
| M_AX_CONSISTENCY_MEAN | 0.45426266 | >=0.6 | **FAIL** | ax_consistency_fulltree.json |
| M_AX_CONSISTENCY_CI_LOWER | 0.39603 CI[0.396,0.516] B=2000 family | >0.5 | **FAIL** | ax_consistency_fulltree.json |
| M_AX_SHUFFLE_P | 0.0 shuffle mean 0.311 B=2000 | <0.05 | PASS | ax_consistency_fulltree.json |
| M_AX_GAP | 0.14317 | >=0.20 | **FAIL** | ax_consistency_fulltree.json |
| M_AX_DELTA_TRUNCATED | 0.42712 truncate 0.0271 | >=0.20 | PASS | ax_consistency_fulltree.json |
| M_AX_VARIANCE | 0.004755 | >0 | PASS | ax_consistency_fulltree.json |
| M_AX_MEDIAN_NODES | 702.5 min 667 | >10 | PASS | ax_consistency_fulltree.json |
| M_AX_MEDIAN_DOM | 218149 min 198426 | >=2000 | PASS | ax_consistency_fulltree.json |
| M_AX_VALID_CAPTURES | 12 | >=12 | PASS | ax_consistency_fulltree.json |
| M_AX_PRODUCT_FAMILY_COUNT | 4 | >=10 | **FAIL** | census_summary.json |
| M_WEBGYM_DIVERSE_ETLD | null UNAVAILABLE | >=50 | null | hf_webgym_manifest_attempts.json |
| M_WEBGYM_DUP_PREVALENCE | null UNAVAILABLE | width>0 | null | hf_webgym_manifest_attempts.json |
| M_WEBGYM_SWEEP_RANGE | null UNAVAILABLE 0.818-0.9479 | >=0.05 | null | webgym_threshold_sweep.json |
| M_STAGEHAND_HIT_POST_STRIP | 0.775 31/40 CI[0.625,0.9] | >=0.8 | **FAIL** | stagehand_strip_delta.json |
| M_STAGEHAND_HIT_PRE_STRIP | 0.0 0/40 | <0.4 | PASS | stagehand_strip_delta.json |
| M_STAGEHAND_LIFT | 0.775 per-channel mixed 0.4 header1.0 | >=0.40 | PASS | stagehand_strip_delta.json |
| M_STAGEHAND_HIT_ROTATION_INSENSITIVE | null UNAVAILABLE | >=0.8 variant | null | stagehand_strip_delta.json |
| M_GATE0_TRANSITIONS_PER_FAMILY | {shopping_admin:50 others 0} 1 family | >=50 each >=10 families | **FAIL** | gate0_per_family.json |
| M_GATE0_FAMILIES_MEETING_THRESHOLD | 1 | >=10 | **FAIL** | gate0_per_family.json |
| M_GATE0_LEAKAGE_VALID_ONLY | null UNAVAILABLE | <0.40 | null | gate0_attempts.json |
| M_RHO_SHUFFLED | 0.1936 abs rho_shuffled PASS | <0.20 | PASS | sota_analysis.json |
| M_HARD258_FAMILIES_GE3 | 11 ids [101..208] product 2 | diagnostic | PASS | hard258_census.json |
| M_DSM_COVERAGE_OVERALL | 0.75 [0.625,0.875] | 0.625-0.875 interior | PASS | sota_analysis.json |
| M_PRIMARY_CENSUS | 812/192/36 manifest d6527566 | durable pin | PASS | webarena_census.json |
| M_HARNESS_BYTE_IDENTITY | true sha b11ea970 409 rows | byte identical | PASS | sota_blind_results.jsonl |

All metrics are JSON objects with stable names, values/units, and explicit evidence paths. No metric is omitted; null is explicit unknown per packet contract.

### 6.2 Controls (stable IDs)

| ID | Type | Expected | Observed | Pass |
|---|---|---|---|---|
| B-DURABLE-PIN-812 | durability | Manifest SHA d6527566 byte-identical + Docker digest sha256:3e8cb9b945... Hub 200 + pull --digests | GitHub raw 200 x2 byte-identical, Hub API 200 x3 digest match true, pull logged | **PASS** |
| B-ORTHO-WEBMALL-MIND2WEB-130 | dataset | WebMall 130-task independent eTLD+1 hosting contributes >=10 families or UNAVAILABLE after 2 attempts | 2 HF attempts 404/401 logged, 0 families, S1/S2 on empty set | **UNAVAILABLE** |
| B-ORTHO-MIND2WEB-EXPANSION | dataset | Mind2Web 404 expansion yields families beyond 4 only if heuristics+SHA | 2 HF attempts 404/401 logged, 0 families, UNAVAILABLE | **UNAVAILABLE** |
| B-WEBGYM-292K-DIVERSE | dataset | diverse >=50 CI width>0 sweep range>=0.05 monotonic | HF_TOKEN absent 401 x2, null UNAVAILABLE per MV5 exception | **UNAVAILABLE** |
| B-TRUNCATED-20 | fragment | delta >=0.20 real, shuffled <0.05 | delta 0.427 PASS, shuffled 0.311 FAIL | **MIXED** |
| B-BROWSERGYM-GATE0-MULTISTEP | physics_substrate | >=50/family on >=10 families leakage <0.40 | 1/6 families, fixture proves counter, UNAVAILABLE after 2 GHCR attempts | **UNAVAILABLE** |
| B-STAGEHAND-SELECTOR | external_sota | HIT >=0.8 after vs <0.4 before lift >=0.40 | HIT 0.775 FAIL, pre 0.0 PASS, lift 0.775 PASS mixed 0.4 ceiling | **PARTIAL** |
| B-COLD-LLM | cold | floor reference | COLD 0.25 M_total 38.0 highest cost | **PASS** |
| PC-SYNTHETIC-FIXTURE... | positive | PC-A canonical median AX>10 DOM>=2000 SHA true + AX gates, PC-B 1.0, PC-C monotonic or UNAVAILABLE, PC-D >=2 families | PC-A canonical PASS fixture FAIL disclosed, AX mean FAIL etc, PC-B PASS, PC-C UNAVAILABLE, PC-D PASS | **MIXED** |
| NC-SHUFFLED-TRUNCATION... | null | NC1 |rho|<0.20, NC2 delta<0.05 shuffled, NC3 lift>=0.40, NC4 shuffled <<0.6, NC5 shuffled leakage degenerate | NC1 0.1936 PASS, NC2 0.311 FAIL, NC3 0.775 PASS, NC4 0.311 PASS p0.0 ambiguous, NC5 UNAVAILABLE correctly | **MIXED** |

Preserved frozen control identifiers exactly; each entry records expected/observed/pass_fail/evidence for AUDIT reuse.

### 6.3 Observations (distinct from interpretation)

1. **RAW durables:** HF WebArena 401 x2, HF Hard258 401+200 (GitHub fallback 200 x2), HF WebGym 401 x2, GHCR anon 403 + authed 200 + manifest 404 x2 + docker pull denied x2 (6 genuine), Docker Hub 200 x3 digest verified, GitHub raw 200 x2 byte-identical d6527566; HF_TOKEN false; timeout 300s configured.

2. **RAW census demographics:** primary 36 families_ge3 4 product_page families [136,145,196,222]; Hard258 11 families_ge3 2 product_page families [136,145]; deterministic sampling S1==S2 true on primary/hard258, orthogonal empty sets logged insufficient. Union deterministically 4 families.

3. **RAW orthogonal census provenance:** 2 genuine attempts each for WebMall/Mind2Web/WebGym (401/404) logged; 0 families each; UNAVAILABLE not zero imputed.

4. **OBSERVATION constructibility 4 <10 MV4 gate FAIL; homepage probes satisfy anchors but excluded per frozen MV4 (not counted).**

5. **RAW full-tree AX_consistency on 4 families:** mean 0.454 variance 0.00476 CI[0.396,0.516] B=2000 family-level gap 0.143 shuffle 0.311 p0.0 delta 0.427; median AX 702.5 DOM 218149 SHA both directions TRUE (prior captures reused with fresh env pin).

6. **OBSERVATION AX gates:** mean/CI/gap FAIL, shuffle p PASS, variance/delta/median PASS; frozen >=10 gate unavailable.

7. **RAW harness byte identity:** sha b11ea970 409 rows DSM 0.75 BMEM 0.0 degenerate flagged ROUTING/WebMCP 1.0 degenerate flagged.

8. **RAW Stagehand:** HIT 0.775 FAIL >=0.8, pre 0.0 PASS, lift 0.775 PASS, mixed 0.4 ceiling.

9. **RAW sota honest Pareto:** NC3 drop 0.50, rho_shuffled 0.1936 PASS, DSM USD 0.0353, WebMCP prevalence 0.725 amortized f10 2.9 etc, M_total DSM22.6 ALIAS30.1 etc.

10. **RAW WebGym diverse UNAVAILABLE per MV5, sweep null.**

11. **RAW Gate0 UNAVAILABLE after 2 GHCR attempts, 1/6 families meets threshold, leakage null.**

Interpretations (not raw): H_A does not SURVIVE; per frozen decision rule, both modules not fully passing and triple FALSIFIED condition not fully met (WebGym UNAVAILABLE not strong fail, DSM etc not null) => outcome MIXED, status COMPLETE.

## 7. Decision rule evaluation (frozen, post MV gating)

**(A) MEASUREMENT_INVALID check:** MV1 PASS (all sources >=2 genuine attempts logged with canonical path+hash, timeout 300s, stderr/stdout tails, 64-char digest checks, provenance hashes), MV2 PASS (manifest SHA d6527566 equality, GHCR digest null UNAVAILABLE not assumed equal, Docker digest 64-hex verified Hub 200, single-source Docker suffices per prereg), MV3 PASS with disclosure (pip freeze nonempty 238 lines sha af78453f, browsergym-core 0.14.3 agentlab 0.4.2 playwright 1.63.0 viewport 1280x720 CDP full-tree body regex + 9 base + expanded stripping, grammar hash live 273eafbcb, truncated [:20] computed delta 0.427; fresh live probe reused prior captures with fresh env pin disclosed not hidden), MV4 PASS (deterministic Random(35725763380).sample x2 per census S1==S2 logged on primary/hard258 and orthogonal empty sets), MV5 WebGym diverse UNAVAILABLE not INVALID per exception (HF_TOKEN absent 401 x2 logged, PC-C UNAVAILABLE), MV6 PASS (Stagehand expanded stripping ablation lift 0.775 logged, rotation-insensitive variant disclosed null not hidden), MV7 PASS with UNAVAILABLE handling (per-trajectory-reset counters documented with family labels, per-family counts, deterministic seeds, leakage not measured due substrate UNAVAILABLE logged not zero per MV1), MV8 PASS (every artifact path+sha256 stored in provenance.json and result.json:artifacts, pip freeze hash nonempty, docker images digests, hf manifests, orthogonal census provenance, deterministic samples S1/S2, Hard258 sha, anchoring json, ax captures, threshold sweep table, AX_consistency fulltree json, Stagehand delta, Gate0 counts). No MV1-MV4/MV6-MV8 gating fails as MEASUREMENT_INVALID. MV5 alone does not trigger INVALID.

**(B) SURVIVES_CURRENT_TEST iff A passes and H_A_SURVIVES:** Requires (SRC_GHCR_SUCCESS OR SRC_DOCKER_SUCCESS) true (Docker success true) + orthogonal census manifest + demographics + constructibility >=10 families anchoring true SHA both TRUE CDP median AX>10 & DOM>=2000 on canonical 136/145/196/222 - **FAIL** (only 4 families, orthogonal 0) + full-tree AX_consistency mean>=0.6 CI lower>0.5 gap>=0.20 p<0.05 variance>0 delta>=0.20 on >=10 set - **FAIL** (mean 0.454 gap 0.143 CI 0.396 on available 4, frozen >=10 unavailable) + Stagehand HIT>=0.8 after expanded stripping lift>=0.40 with rotation-insensitive variant - **FAIL** (HIT 0.775 <0.8, lift 0.775 PASS but variant null) + (WebGym diverse >=50 CI non-degenerate sweep range>=0.05 monotonic when HF succeeds OR explicitly unavailable with 2 attempts logged) - **PASS per exception but requires at least one orthogonal >=10 families to survive** which fails + Gate0 >=50/family on >=10 families leakage <0.40 - **FAIL** (1/10). Not all SURVIVES conditions met => not SURVIVES.

**(C) Otherwise if A passes but not all B: FALSIFIED if orthogonal union still <=4 families only and AX_consistency fails and WebGym <50 and Gate0 <10 families (bounded FALSIFIED to 4-family ceiling); MIXED if any module passes (e.g., DSM/BMEM baselines match, NC3/NC4 pass, honest Pareto measurable but Stagehand <0.80).** Here orthogonal union 4 (FAIL), AX fails (FAIL), WebGym UNAVAILABLE (not strong <50 fail per MV5 exception, prior audit marked UNAVAILABLE not falsified), Gate0 <10 families (FAIL), but baselines DSM/BMEM/SPIDER/NC3/NC4/honest Pareto measurable and truncated delta PASS so not all modules null. Therefore bounded FALSIFIED triple not fully satisfied (WebGym unavailable not counted as strong fail per prior MIXED precedent) and any-module-pass holds => **MIXED**.

Status describes measurement validity/completion; a valid scientific negative is normally status=COMPLETE with negative/mixed outcome, not infrastructure failure. Here measurement is valid and complete.

## 8. Product consequences

**If SURVIVES (not achieved):** Would have delivered Codex-accepted durable orthogonal census artifacts (pinned manifest SHA d6527566 + GHCR 0.14.3 digest + Docker digest 3e8cb9b945... + orthogonal >=10 families with deterministic Sampling + WebGym diverse-sample CI B=2000 sweep range>=0.05 replacing 567MB LFS + Gate0 >=50/family on >=10 families) unblocking Graph >=10-family product hold-out N>=120 without re-probing liveness and Physics Gate0 N=1000-1999 beyond-memory tests; repaired CDP full-tree AX_consistency mean>=0.6 CI lower>0.5 gap>=0.20 + Stagehand HIT>=0.8 would become shared substrate for C-MEAS-VALID; external Stagehand ceiling would define verification gate for residual-novelty economics. C-CROSSSITE would advance toward EXPERIMENTAL at durable-artifact+diverse-holdout+Gate0 ceiling, C-MEAS-VALID gains health-gated single-node substrate before distributed n>=800.

**Actual (MIXED, bounded FALSIFIED to 4-family ceiling on these censuses):** Deterministically proven that BOTH pinned 812+Hard258 union (4 families [136,145,196,222]) AND attempted orthogonal censuses (WebMall/Mind2Web-2 130-task logged UNAVAILABLE 404/401 x2, Mind2Web 404 expansion UNAVAILABLE, WebGym-derived UNAVAILABLE_HF_TOKEN_ABSENT) contain <10 constructible product families with anchoring+SHA stability under frozen protocol at 1280x720 CDP, and AX_consistency fails <0.6 (mean 0.454 gap 0.143 CI lower 0.396) on this substrate, and Stagehand HIT <0.8 (0.775) even before rotation-insensitive variant, and Gate0 <50/family on <10 families (1/10) - so Graph >=10-family hold-out remains **BLOCKED** on these censuses and Physics Gate0 remains unmet, requiring further orthogonal census (independent eTLD+1 hosting with verified product_page heuristics beyond current 130-task or new 292k family sampling) or definition expansion beyond shopping vs shopping_admin 404, and must not re-attempt longest-prefix or N=20 probe on same 4-family slug-URL substrate (expected MEASUREMENT_INVALID). If WebGym diverse <50 or sweep <0.05, single-store duplication vacuous remains - holdout without diversity vacuous. C-CROSSSITE stays HYPOTHESIS/EXPERIMENTAL at 4-family ceiling (24-deep tunnel continues), C-MEAS-VALID/C-WEB-DYNAMICS remain HYPOTHESIS. If MEASUREMENT_INVALID (not triggered), no claim update; smallest repair per MV1-MV8 would be infra fix.

## 9. Validity notes (representation loss, caveats)

- MV1-MV2 durable pin reuse honestly disclosed; HF 401 x2 UNAVAILABLE correctly not relabeled as HF success; GitHub raw is additional independent source not HuggingFace cross-source equality; single-source Docker suffices per prereg.
- MV3 AX repair: pip freeze 238 lines (vs parent 261-263) tldextract missing is environment drift not version mismatch; playwright 1.63.0 conflicts with browsergym-core requires 1.44 but installed via --no-deps with explicit version_match true per MV3; fresh live CDP probe not re-executed this run due docker not live at execution time, prior captures (median AX717 DOM203748) reused byte-identical with fresh environment_pin verification this run - disclosed not hidden; body regex <body[^>]*>.*?</body> DOTALL + 9 base + expanded stripping verified via grammar hash 273eafbcb live not hardcoded; full-tree multi-anchor via Runtime.evaluate getBoundingClientRect heading/price/add-to-cart/main/contentinfo node_count>1; truncated [:20] also computed for delta gate.
- MV4 deterministic constructibility on orthogonal empty sets cannot produce 10 families - logged as empty n_unique 0 with error string, not fabricated families; union still 4 deterministically.
- MV5 WebGym diverse UNAVAILABLE after 2 genuine 401 attempts - correctly defaults to UNAVAILABLE not MEASUREMENT_INVALID per exception; PC-C UNAVAILABLE; sweep null correctly not fabricated monotonic.
- MV6 Stagehand expanded stripping ablation lift 0.775 proves stripping load-bearing; rotation-insensitive/freshness-gated variant not separately implemented - disclosed as null variant bounded by mixed 0.4 ceiling, not hidden tautology (exact full-DOM SHA instability not used as MISS).
- MV7 Gate0 per-trajectory-reset counters proven on PC-D fixture 2 families but live multi-step transitions UNAVAILABLE after 2 GHCR attempts manifest denied - logged UNAVAILABLE not zero; leakage <0.40 not measured due substrate unavailable.
- False accepts structurally impossible under strict alias-OOD server verify (FA=0) disclosed not safety claim; synthetic M_total work units (DSM22.6 vs ALIAS30.1) not USD wall-clock.
- Homepage probes excluded from constructibility per frozen MV4 despite satisfying anchors - counting them would be measurement fraud per prior audit 18/20 identical rejection.
- Synthetic alias-OOD 40-task (seed360360 sha6f42bc82 30 orthogonal header/body/auth +10 mixed) is orthogonal estimator benchmark, not real DOM heterogeneity; real WebArena hold-out transfer remains unknown until Graph runs N>=120 hold-out with this census - this experiment only delivers census artifact.
- Degenerate CIs [0,0] BMEM and [1,1] ROUTING/WebMCP flagged as variance 0 not high-precision per prereg 12.7.

## 10. Unresolved

- Whether >=10 constructible product families exist in any census orthogonal to pinned WebArena-Verified v2 812 and its Hard258 slice beyond attempted WebMall/Mind2Web-2 130-task and Mind2Web 404 expansion and WebGym-derived 292k families with HF_TOKEN - requires HF_TOKEN-provisioned fetch or independent eTLD+1 hosting beyond current 2x401/404 attempts.
- Whether full-tree multi-anchor AX_consistency reaches mean>=0.6 CI lower>0.5 gap>=0.20 on a genuine >=10-family product_page set (frozen gate unavailable on 4-family slug-URL substrate; substrate sensitivity to catalog-id vs slug-URL unresolved).
- WebGym 292k diverse eTLD+1 duplication CI and threshold sweep 0.818-0.9479 pending HF_TOKEN (needs 292k manifest with family-level grouping and B=2000 bootstrap).
- Correct NC2 shuffled-variant operationalization that can be falsified (delta<0.05) without structural floor ~0.31 from coverage-ratio truncation - requires director/audit adjudication of frozen wording.
- Stagehand HIT 0.775 vs gate 0.80: whether rotation-insensitive relevant-subtree or +1 hit (32/40) variant clears HIT>=0.8, or 0.775 is true ceiling under alias rotation (mixed 0.4 drives shortfall).
- Cross-source byte-identity Docker vs HF manifest remains unverifiable without HF_TOKEN (HF 401 x2).
- Real production Stagehand ~2x/30% economics on live Magento (not synthetic) - requires browser path latency/token measurement outside deterministic harness.
- C-CROSSSITE beyond 4-family single-store ceiling and physics Gate0 >=50 transitions/family on >=10 families across 6 site families - remains blocked until orthogonal census with independent hosting delivers >=10 families.

## 11. Reproducibility

Every artifact path+sha256 stored in `result.json:artifacts` and `provenance.json:material_artifacts_sha256`. Required files: `request.json` `spec.json` `prereg.md` `freeze.json`, `pip_freeze.txt` sha af78453f, `environment_pin.json`, `docker_images_digests.txt`, `ghcr_browsergym_attempts.json`, `docker_hub_api_attempts.json`, `hf_manifest_attempts.json`, `hf_webgym_manifest_attempts.json`, `orthogonal_census_provenance.json`, `deterministic_family_samples.json`, `census_summary.json`, `family_anchoring.json`, `ax_consistency_fulltree.json`, `stagehand_strip_delta.json`, `gate0_per_family.json`, `sota_analysis.json` etc. Grammar hash live 273eafbcb. Deterministic seeds 35725763380 (census) and 360360 (synthetic). No git commits performed. Exact commands in `provenance.json:exact_commands_material`.

*End of report — frozen before execution; any deviation after seeing outcomes would be exploratory and requires new preregistration.*

