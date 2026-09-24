# Preregistration — EXP-INTEL-36037208652

**Lane:** intel — Find, reproduce and stress-test datasets, baselines and prior art only when they can alter a live SPIDER claim
**Experiment ID:** EXP-INTEL-36037208652
**Claim IDs:** C-CROSSSITE (primary), C-MEAS-VALID, C-WEB-DYNAMICS
**Request ID:** f1847e89e2204da72275e9da  •  **Request hash:** b890f8a03f2b8e2448090ff28658caf991541a2d9d877e4d13a5c2ff8c4f90e4
**Director mandate:** CONTINUE • **Target claim:** C-CROSSSITE • **Cognitive reset:** true • **Parent handoff disposition:** USE (EXP-INTEL-36020904615 preserved as continuity evidence only)
**Freeze status:** DESIGN — no outcome-bearing measurements inspected. Spec and prereg frozen before EXECUTE.

---

## 1. Strategic question (Director binding)

> Can an orthogonal census beyond the pinned WebArena-Verified v2 812 + Hard258 258 (WebMall/Mind2Web-2 BrowserGym loopback 130-task, Mind2Web shopping vs shopping_admin definition expansion with verified product_page heuristics, or WebGym-derived 292k families with independent eTLD+1 hosting and HF_TOKEN-provisioned duplication CI + threshold sweep 0.818-0.9479 range>=0.05) deliver >=10 distinct product families constructible under the identical deterministic random.Random(35725763380).sample + get_task_start_url __SHOPPING__ + product-subtree anchoring + SHA stability protocol at 1280x720 CDP full-tree expanded stripping, and achieve full-tree multi-anchor AX_consistency mean>=0.6 CI lower>0.5 gap>=0.20 on that >=10 set while Stagehand HIT>=0.8 via rotation-insensitive relevant-subtree or freshness-gated SHA, plus close WebGym 292k >=50 diverse eTLD+1 duplication CI (2000 bootstrap) and >=50 transitions/family on >=10 families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) for physics Gate0?

Director `comparative_reasoning`: Versus fixing BrowserGym multi-step collection alone or blind reproducing external SOTA on synthetic 40-task alias-OOD: SOTA reproduction sets O(1) bar product must beat but is meaningless without a valid diverse site census; combined census + Gate0 H>0.1 NL>=20 closes both cross-site prevalence and physics sampling integrity in one allocation, avoiding 24th C-CROSSSITE iteration on same 2-site bounds. `allocation.rationale`: Intel has delivered partial census (pinned Docker digest, 812+258 manifests byte-identical) but remains tunnel_flag true with 23-streak C-CROSSSITE; closing HF_TOKEN 50-site duplication CI and 10-family >=50 transitions census is durable artifact unblocking physics beyond-memory N=1000-1999 and graph param-inherit Hard258 pilots, higher leverage than reproducing baselines which assume census stability.

This converts to the smallest rigorous falsifiable test below. We do **not** re-probe the same pinned 812+Hard258 union alone to reach >=10 (already bounded to 4 families deterministically), nor exhaustively download 567MB LFS test.zip; instead we test escape via genuinely orthogonal census with independent eTLD+1 diversity while verifying full-tree pipeline and Gate0 multi-step collection under identical frozen protocol.

---

## 2. Inherited state (parent handoff EXP-INTEL-36020904615 — audit PASS, producer_claim_supported true, bounded ceiling)

**Established (preserved):**
- Durable single-source pin: WebArena-Verified manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 927596 bytes byte-identical x2 (github_cross_source 200) + Docker Hub am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb Hub API 200x2 docker pull rc0 x2 container localhost:7770 HTTP200x3 SRC_DOCKER_SUCCESS (GHCR UNAVAILABLE after 6 genuine attempts, single-source suffices per prereg, audit MV1 PASS MV2 PASS).
- Census demographics: primary 812 total 192 shopping 36 families_ge3 21 product tasks 4 product_page families [136,145,196,222]; Hard258 258 total 61 shopping 11 families_ge3 6 product tasks 2 families [136,145] task_ids subset of pin; deterministic random.Random(35725763380).sample(sorted families_ge3,10) x2 S1==S2 exact per census logged (artifacts/derived/deterministic_family_samples.json, census_summary.json).
- Constructibility at 1280x720 CDP Accessibility.getFullAXTree (BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 Chromium 153.0.8010.12): exactly 4 families constructible with product-subtree anchoring heading2 price6 add_to_cart2 main226-365 contentinfo31 + distinct outerHTML SHA256 with body regex + 9 base + expanded {form_key,uenc,store,session,nonce,fotorama\d{6,}} before SHA via page.evaluate recomputed after page.content()+AX, SHA before==after TRUE and after mutation != TRUE 12/12 median AX717 min627 DOM203748 min195052 (37 AX probes 0 errors, grammar hash 273eafbcb817e... live).
- Full-tree multi-anchor AX_consistency pipeline validated as non-vacuous on 4-family slug-URL set: mean 0.4543 CI[0.3960,0.5164] B=2000 family-level gap0.143 shuffled mean0.311 p0.0 variance0.00476 delta_vs_truncated0.4271 truncated_mean0.0271 median AX>10 DOM>=2000 PASS; shuffle distinguishes (p0.0) but mean/CI-lower/gap fail >=0.6/>0.5/>=0.20 gates on this substrate (vs parent 0.6208 CI[0.5514,0.6902] on catalog-id substrate substrate-sensitivity disclosed).
- Synthetic alias-OOD 40-task (seed360360 sha6f42bc82 30 orthogonal header/body/auth +10 mixed) blind harness b11ea970 byte-identical 409 rows: DSM 0.75 [0.625,0.875] HITL drop0.50 USD0.0353 M_total_f10 DSM22.6 vs ALIAS30.1 prevalence0.725 vs Stagehand coverage0.475 HIT_post0.775 HIT_pre0.0 lift0.775 vs BMEM0.0 degenerate; |rho_shuffled|0.1936<0.20 honest sum-counters verified.

**Rejected (bounded, do not re-attempt without orthogonal source):**
- H_A >=10 distinct product families constructible from pinned WebArena-Verified v2 812 + Hard258 258 union under frozen anchoring+SHA protocol at 1280x720 CDP — bounded FALSIFIED to 4 families deterministically (primary 4 + Hard258 2 union still 4, audit recomputed), not global impossibility; homepage probes 16 identical localhost:7770/ excluded per MV4 product_page requirement.
- Full-tree AX_consistency mean>=0.6 CI lower>0.5 gap>=0.20 on 4-family slug-URL substrate — bounded FAIL (mean0.454 CI lower0.396 gap0.143) on this substrate; not falsified on >=10-family set (untestable) and not on catalog-id substrate where parent 0.6208 passed.
- Stagehand exact selector+relevant-subtree SHA256 HIT>=0.8 on synthetic alias-OOD with expanded stripping — bounded FALSIFIED to 0.775 (31/40) lift0.775 per-channel mixed HIT0.4 caps ceiling; pre-strip0.0 lift proves stripping load-bearing but threshold not met.
- Degenerate CIs [0,0] BMEM and [1,1] ROUTING/WebMCP as high-precision, homepage-only [:20] truncated AX_consistency, incomplete form_key-only stripping, and synthetic M_total as USD/wall-clock — rejected as measurement-invalid per audit.

**Unknown (this experiment targets):**
- Whether any orthogonal census beyond WebArena+Hard258 (WebMall/Mind2Web-2 BrowserGym loopback 130-task, shopping vs shopping_admin 404 definition expansion with verified product_page heuristics, WebGym-derived 292k/127k families with independent hosting) contains >=10 product_page families constructible under identical protocol at 1280x720 CDP.
- Whether full-tree multi-anchor AX_consistency reaches mean>=0.6 CI lower>0.5 gap>=0.20 on a genuine >=10-family product-page set (frozen gates untestable on 4-family slug-URL substrate; substrate sensitivity unresolved).
- WebGym 292k/127k diverse eTLD+1 >=50 duplication prevalence family-level B=2000 CI and threshold sweep 0.818-0.9479 range>=0.05 monotonic pending HF_TOKEN (2x401 UNAVAILABLE per MV5 exception, not falsified) — needed to replace 567MB LFS.
- Stagehand rotation-insensitive ceiling: whether freshness-gated relevant-subtree or API/tool bypass variant clears HIT>=0.8.
- BrowserGym multi-step collection >=50 transitions/family on >=10 families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) for physics Gate0 — previously 0 transitions API mismatch, now requires honest per-trajectory counters.

**Do-not-assume (preserved):**
- Do not assume >=10-family constructibility from pinned WebArena-Verified v2 812 or Hard258 union or homepage probes (16 identical localhost:7770/ with heading2 price4 add_to_cart2 main485 contentinfo31 meet anchors but excluded per frozen MV4 — counting them is measurement fraud).
- Do not assume GHCR BrowserGym 0.14.3 image fetchable or cross-source byte-identity verified (GHCR 6 genuine attempts UNAVAILABLE, HF 2x401 UNAVAILABLE; only Docker single-source pin is durable).
- Do not treat degenerate CIs [0,0] BMEM or [1,1] ROUTING/WebMCP as high-precision; correctly flag per prereg 12.7 and do not count as valid width.
- Do not equate synthetic M_total_f10 work units with USD/wall-clock or browser steps; USD mean is patch-cost only and false_accept 0.0 is structural verification artifact.
- Do not assume full-tree AX_consistency 0.4543 generalizes to >=10-family threshold or that parent 0.6208 on catalog-id implies slug-URL passes; substrate sensitivity open.
- Do not assume Stagehand HIT 0.775 ~0.80 or that NC2 shuffled delta 0.311 <0.05 can be achieved under literal token-reassignment (structural floor ~0.31 disclosed).
- Do not assume WebGym UNAVAILABLE (401) implies falsified duplication 0.9479 or that threshold sweep 0.818-0.9479 is unnecessary.
- Do not assume synthetic alias-OOD structured collapse implies real website hold-out or that another N=20 longest-prefix probe on same 4-family substrate will escape ceiling — bounded FALSIFIED requires orthogonal census.
- Do not assume BrowserGym multi-step collection is trivial; prior Gate0 0/50 due API mismatch, requires per-trajectory counters and leakage <40% to be valid.

**Director disposition:** Parent `next_question` (orthogonal census WebMall/Mind2Web-2 130-task, Mind2Web definition expansion shopping vs shopping_admin 404, or WebGym-derived families independent hosting) is advisory. Director mandate CONTINUE with cognitive_reset true refines it to the exact orthogonal census + Gate0 question above. DESIGN preserves inherited established/rejected/unknown/do_not_assume distinctions but follows Director's binding target — prior Hard258 union ceiling remains rejected, new orthogonal census is the discriminating test.

---

## 3. Hypotheses

### H_A_ORTHO_CENSUS_10FAM (primary)
An orthogonal census beyond the pinned WebArena-Verified v2 812 + Hard258 258 — at least one of (a) WebMall/Mind2Web-2 BrowserGym loopback 130-task with independent eTLD+1 hosting, (b) Mind2Web shopping vs shopping_admin definition expansion with verified product_page heuristics and get_task_start_url __SHOPPING__ expansion, or (c) WebGym-derived 292k/127k-site families with HF_TOKEN-provisioned manifest and independent eTLD+1 hosting — yields >=10 distinct product families constructible under the identical frozen protocol (deterministic random.Random(35725763380).sample(sorted families_ge3,10) x2 S1==S2 logged plus get_task_start_url __SHOPPING__ placeholder expansion plus product-subtree anchoring heading/price/add-to-cart/main/contentinfo node_count>1 and distinct outerHTML SHA256 with body regex DOTALL + 9 base + expanded {form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp} before SHA via page.evaluate recomputed after page.content()+AX, SHA before==after TRUE and after mutation != TRUE, 1280x720 CDP Accessibility.getFullAXTree median AX>10 DOM>=2000 proven on canonical families [136,145,196,222]) and achieves on that >=10-family product_page set full-tree multi-anchor longest-prefix-without-fallback AX_consistency mean>=0.6 bootstrap 95% percentile CI lower>0.5 trajectory-grouped family-level B=2000 gap>=0.20 vs family-label shuffle p<0.05 variance>0 delta_vs_truncated>=0.20 vs [:20] truncated baseline, while Stagehand selector+relevant-subtree SHA256 (rotation-insensitive or freshness-gated SHA) HIT>=0.8 overall with stripping lift>=0.40 vs pre-strip, plus WebGym diverse >=50 distinct eTLD+1 with B=2000 duplication prevalence non-degenerate CI width>0 and threshold sweep at 0.818 and 0.9479 range>=0.05 monotonic decreasing replacing exhaustive 567MB LFS, and BrowserGym multi-step >=50 transitions/family on >=10 families across >=6 site families (shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena) satisfying physics Gate0.

### H_B_PHYSICS_GATE0 (secondary, informs C-MEAS-VALID/C-WEB-DYNAMICS)
The same orthogonal census and BrowserGym multi-step substrate that satisfies H_A also closes Gate0 for physics beyond-memory tests (sufficient NL>=50/family, leakage <40%, state diversity |S|>=16). This is not a new dynamical law but the sampling integrity prerequisite that 14 consecutive MEASUREMENT_INVALID physics experiments lacked due to 2-site bounds.

---

## 4. Falsifier

**H_A falsified if** after >=2 genuine attempts per durable source (HF for WebArena 812+Hard258+WebGym 292k with HF_TOKEN true/false logged, GHCR BrowserGym 0.14.3, Docker Hub webarena-verified-shopping@sha256:3e8cb9b945..., each timeout>=300s, docker pull --digests or docker load fallback, Hub/GHCR API 200, stderr/stdout captured) no orthogonal census beyond the 4-family union [136,145,196,222] yields >=10 distinct product families with anchoring true and SHA stability both directions TRUE and CDP 1280x720 median AX>10 & DOM>=2000 on canonical families, OR full-tree AX_consistency mean<0.6 or CI lower<=0.5 or shuffle p>=0.05 or gap<0.20 or variance==0 or delta_vs_truncated<0.20 on the >=10 set (homepage-only [:20] truncation or incomplete stripping rejected), OR Stagehand HIT post-strip <0.8 and lift <0.40 and rotation-insensitive/freshness-gated variant not improving, OR when HF_TOKEN succeeds WebGym diverse <50 distinct eTLD+1 or B=2000 CI not computed non-degenerate or sweep 0.818-0.9479 range<0.05 or not monotonic (when HF_TOKEN fails after 2 genuine 401/404 attempts this clause is UNAVAILABLE not falsified), OR Gate0 <50 transitions/family on <10 families or leakage >=40%. Single-module failure -> MIXED, all fail -> FALSIFIED, all pass -> SURVIVES. No inference if MEASUREMENT_INVALID gating fails.

---

## 5. Baselines (stable IDs for EXECUTE/AUDIT reuse)

| ID | Type | Description | Expected |
|---|---|---|---|
| B-DURABLE-PIN-812 | durability | WebArena-Verified v2 812 tasks manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (927596 bytes) byte-identical + Docker Hub am1n3e/webarena-verified-shopping@sha256:3e8cb9b945... 64-char digest Hub API 200 + docker pull --digests | SHA equality, 64-char digest equality, localhost:7770 HTTP 200, families_ge3 >=30 |
| B-ORTHO-WEBMALL-MIND2WEB-130 | dataset | Orthogonal census A: WebMall/Mind2Web-2 BrowserGym loopback 130-task independent eTLD+1 hosting slice, verified product_page heuristics + get_task_start_url __SHOPPING__ expansion, same deterministic Random(35725763380).sample x2 + anchoring at 1280x720 CDP | If hosting succeeds contributes >=10 families union; if unavailable after 2 attempts logged UNAVAILABLE not zero |
| B-ORTHO-MIND2WEB-EXPANSION | dataset | Orthogonal census B: Mind2Web shopping vs shopping_admin definition expansion (404 candidate) with verified product_page heuristics, same deterministic sampling/anchoring protocol | Expanded definition yields additional families beyond 4 only if verified heuristics + SHA stability hold |
| B-WEBGYM-292K-DIVERSE | dataset | WebGym 292k/127k sites diverse eTLD+1 slice >=50 distinct, duplication prevalence family-level B=2000 bootstrap, threshold sweep 0.818 and 0.9479 range>=0.05 monotonic — replaces 567MB LFS | diverse >=50, CI width>0, sweep range>=0.05 monotonic decreasing |
| B-TRUNCATED-20 | fragment | Selectors/AX tokens [:20] truncated vs full-tree multi-anchor; delta_vs_truncated diagnostic | delta >=0.20 if full-tree non-vacuous; shuffled <0.05 |
| B-BROWSERGYM-GATE0-MULTISTEP | physics_substrate | BrowserGym multi-step transitions across shopping_admin, Reddit, GitLab, Wikipedia, VisualWebArena, WorkArena; >=50 transitions/family on >=10 families, trajectory grouping, leakage <40% | >=50 transitions/family on >=10 families, leakage valid-only <0.40, diversity documented |
| B-STAGEHAND-SELECTOR | external_sota | Stagehand selector + relevant-subtree SHA256 HIT/MISS with expanded stripping {form_key,uenc,store,session,nonce,fotorama\d{6,}} plus rotation-insensitive/freshness-gated SHA variant | HIT >=0.8 after stripping vs <0.4 before, lift>=0.40, per-channel breakdown |
| B-COLD-LLM | cold | Cold LLM no-memory floor same model/tools/budget | Floor reference for future product economics, not gating H_A |

Per-orthogonal-census deterministic samples S1/S2 and per-family anchoring json required for each baseline census.

---

## 6. Controls

### Positive control — PC-SYNTHETIC-FIXTURE-TOY-STAGEHAND-WEBGYM-GATE0-SANITY
- **PC-A** Synthetic Flask product fixture at 1280x720 fixed DOM heading+price+add-to-cart+main+contentinfo localhost, AX ~17 nodes deterministic; pipeline must capture median AX>10 DOM>=2000, SHA before==after TRUE 12/12, mutated textContent SHA != 12/12. Also 12 product captures on canonical families 136/145/196/222 median AX688 min627 DOM200413 min195052; full-tree AX_consistency mean>=0.6 CI lower>0.5 shuffle p<0.05 gap>=0.20 variance>0 delta>=0.20.
- **PC-B** Toy single-header param: Stagehand minimal selector+subtree HIT 1.0 after expanded stripping.
- **PC-C** (gated HF_TOKEN) WebGym diverse-sanity >=50 diverse yields prevalence in [0.3,0.99] and sweep monotonic.
- **PC-D** Gate0 fixture: synthetic BrowserGym trace parsing yields families_ge3 >=2 on fixture proving counter logic handles >=50/family threshold correctly.
*Expected:* PC-A VALID captures median AX>10 DOM>=2000 SHA both directions TRUE anchored 12/12 AND AX_consistency gates; PC-B 1.0; PC-C monotonic and CI computable when HF succeeds else UNAVAILABLE not failed; PC-D parse PASS.

### Null controls — NC-SHUFFLED-TRUNCATION-STAGEHAND-GATE0-AX (all trajectory-grouped family-level)
- **NC1** Family-label shuffle (1000 perms coverage, 2000 family-level WebGym duplication, 1000 shuffle AX): |rho_shuffled|<0.20, shuffle mean ~ chance, gap real-shuffle >=0.20, AX shuffled mean <<0.6 p>0.05.
- **NC2** Truncated B-TRUNCATED-20 vs full-tree: delta_vs_truncated >=0.20 real must hold; shuffled variant <0.05; previous degenerate CI[0.7,1.0] p=1.0 rejected.
- **NC3** Stagehand stripping ablation: HIT with expanded stripping vs without delta >=0.40; without stripping HIT <0.5.
- **NC4** AX_consistency family permutation: shuffled mean <0.6 p>0.05 variance 0 vs real variance>0 gap>=0.20.
- **NC5** Gate0 leakage shuffle: shuffled transition labels produce leakage >> real if collection leakage-free; shuffled leakage not <0.40 correctly distinguished.
*Expected:* NC1 |rho|<0.20 p>0.05 shuffled, NC2 delta<0.05 shuffled, NC3 lift>=0.40, NC4 shuffled <<0.6, NC5 shuffled leakage degenerate correctly distinguished. All CIs trajectory-grouped family-level, not transition-grouped.

All CIs trajectory-grouped bootstrap 95% percentile. Degenerate [0,0] or [1,1] variance 0 flagged per prior prereg 12.7 not counted as valid width.

---

## 7. Measurement validity (gating, frozen)

1. **MV1_DURABLE_ATTEMPTS:** Each durable source (HF WebArena 812+Hard258+WebGym 292k, GHCR BrowserGym 0.14.3, Docker Hub webarena-verified-shopping) requires >=2 genuine attempts logged with URL, HTTP status/returncode, bytes, sha256 hex, 64-char digest check, timeout >=300s or docker load fallback captured, stderr/stdout. Single-attempt success -> MEASUREMENT_INVALID. HF_TOKEN present true/false logged. GHCR and Hub API digest 200 required. Evidence: artifacts/raw/webarena_verified_pin.json, hf_manifest_attempts.json, hf_webgym_manifest_attempts.json, ghcr_browsergym_attempts.json, docker_hub_api_attempts.json, orthogonal_census_provenance.json, provenance.json hashes.

2. **MV2_BYTE_IDENTITY:** Manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (927596 bytes, 64 hex) equality stored; GHCR digest 64-char hex equality with GHCR API 200; Docker digest exactly sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (64 hex after colon) Hub API 200. If one source succeeds, single sha256 pinned file + log suffices but cross-source equality explicitly UNAVAILABLE not assumed equal. WebGym SHA separately logged when HF_TOKEN succeeds. Orthogonal census SHA separately pinned, families_ge3 histogram recorded. Reuse prior pinned file allowed only with +2 fresh verification attempts this experiment.

3. **MV3_AX_REPAIR_FULLTREE:** BrowserGym-core==0.14.3, AgentLab==0.4.2, Playwright==1.63.0, playwright install --with-deps chromium verified via pip freeze sha256 nonempty and playwright --version + browser validation; viewport 1280x720 strict; CDP Accessibility.getFullAXTree via cdp_session required — fallback accessibility.snapshot -> MEASUREMENT_INVALID for H_A. Metrics median AX>10, DOM>=2000, body regex <body[^>]*>.*?</body> DOTALL + 9 base + expanded stripping (form_key/uenc/store/session/nonce/timestamp/fotorama\d{6,}) before SHA256 via page.evaluate recomputed after page.content()+AX, grammar hash live via research/intel/grammar_fulltree_*.py hash 273eafbcb... live not hardcoded. Full-tree multi-anchor AX_consistency on full tree (not [:20]) with Runtime.evaluate getBoundingClientRect heading/price/add-to-cart/main/contentinfo node_count>1; truncated [:20] also computed for delta gate.

4. **MV4_ORTHOGONAL_CONSTRUCTIBILITY:** Deterministic test executed exactly: sorted families_ge3 from webarena_census.json (812) AND each orthogonal census (WebMall/Mind2Web-2 130-task and Mind2Web expansion and WebGym-derived families if available), two independent Random(35725763380).sample(sorted families_ge3,10) with seed reset logged S1 and S2 on EACH census (S1==S2 expected but both logged), each probed via get_task_start_url __SHOPPING__ expansion + product-subtree anchoring heading/price/add-to-cart/main/contentinfo node_count>1 distinct SHA256 on canonical 136/145/196/222 at 1280x720 CDP (12 captures median AX688 DOM200413), per-family anchoring json; constructible = distinct families anchoring true among S1|S2 plus canonical plus orthogonal union; gate >=10 distinct; full-tree AX_consistency mean>=0.6 CI lower>0.5 B=2000 gap>=0.20 p<0.05 variance>0 delta>=0.20 on >=10 family set. Without BOTH samples logged per census -> MEASUREMENT_INVALID for that clause. Runtime single-node health-gated harness availability documented.

5. **MV5_WEBGYM_DIVERSE_AND_THRESHOLD_SWEEP:** WebGym 292k/127k sites when HF_TOKEN succeeds sampled >=50 distinct eTLD+1 documented extraction, family-level grouping preserved, duplication prevalence Jaccard/template duplication >= threshold (exact choice documented), family bootstrap B=2000 unit=family 95% CI non-degenerate width>0, sweep at 0.818 and 0.9479 range = prevalence_0.818 - prevalence_0.9479 >=0.05 monotonic decreasing to replace 567MB LFS. If HF_TOKEN 401 after 2 attempts >=300s each, diverse count explicitly UNAVAILABLE with attempts logged not zero; then clause alone does not trigger MEASUREMENT_INVALID but H_A partially unavailable, PC-C UNAVAILABLE.

6. **MV6_STAGEHAND_STRIP_FRESHNESS:** Stagehand selector+relevant-subtree SHA256 HIT/MISS implemented with expanded stripping before SHA256 via page.evaluate recomputed after page.content()+AX, both with and without expanded set logged for ablation (lift>=0.40). Rotation-insensitive or freshness-gated SHA variant explicitly tested (document variant: relevant-subtree bounding box rotation-insensitive or SHA recomputed only if freshness header/ETag unchanged). Prohibited to use exact full-DOM SHA256 instability as MISS tautology.

7. **MV7_GATE0_TRANSITIONS:** BrowserGym multi-step collection for physics Gate0 must be per-trajectory-reset counters (transitions counted per trajectory not aggregated) documented with site family label, site URL, transition count per family, total families probed, leakage measurement valid-only <0.40, state diversity (|S|>=16 or unique titles/URLs per family). Requires >=50 transitions/family on >=10 families across >=6 site families with deterministic seeds logged. If BrowserGym API mismatch or substrate unavailable after 2 genuine attempts, logged UNAVAILABLE per MV1 not zero.

8. **MV8_PROVENANCE:** Every artifact path+sha256 stored in provenance.json and freeze.json: request/spec/prereg/freeze hashes, pip freeze hash nonempty, docker images --digests hash, ghcr/docker_hub attempts, HF manifest sha/bytes or 401 log, WebGym sha when available, orthogonal census provenance (WebMall/Mind2Web manifests, histograms, S1/S2), Hard258 census sha, anchoring json, ax captures/probe logs, threshold sweep table, AX_consistency fulltree json, Stagehand stripping delta, Gate0 per-family transition counts, leakage logs, command logs pull/load/run. Missing provenance for any durability/AX_consistency/Stagehand/Gate0 path -> MEASUREMENT_INVALID for that module.

---

## 8. Decision rule (frozen three-way, after MEASUREMENT_INVALID check)

**(A) MEASUREMENT_INVALID** if any MV1-MV4/MV6-MV8 mandatory gating fails: <2 genuine attempts per required durable source (GHCR 0.14.3, Docker Hub webarena, HF WebArena/Hard258/WebGym), missing 64-char digest or manifest SHA d6527566, pip freeze empty or version/viewport mismatch (requires 0.14.3/0.4.2/1.63.0 1280x720), fallback AX snapshot used, body regex absent, deterministic sampling not executed exactly as specified on BOTH primary and at least one orthogonal census, AX_consistency not full-tree multi-anchor trajectory-grouped B=2000, Stagehand expanded stripping not ablated, Gate0 not per-trajectory counts or leakage not measured, or provenance missing — then no SURVIVES/FALSIFIED inference.

MV5 WebGym diversity clause alone defaults to UNAVAILABLE not INVALID when HF_TOKEN absent after 2 genuine attempts (marked null with attempts logged, PC-C UNAVAILABLE).

**(B) SURVIVES_CURRENT_TEST** iff A passes (MV5 either PASS or documented UNAVAILABLE with at least one orthogonal census achieving >=10 families) AND **H_A_SURVIVES**: (SRC_GHCR_SUCCESS OR SRC_DOCKER_SUCCESS) with orthogonal census artifact manifest + census demographics + deterministic constructibility >=10 distinct product families anchoring true SHA both directions TRUE CDP 1280x720 median AX>10 & DOM>=2000 on canonical 136/145/196/222 AND full-tree AX_consistency mean>=0.6 CI lower>0.5 B=2000 gap>=0.20 p<0.05 variance>0 delta>=0.20 on >=10 family set AND Stagehand HIT>=0.8 after expanded stripping lift>=0.40 with rotation-insensitive/freshness-gated variant AND (WebGym diverse >=50 CI non-degenerate sweep 0.818-0.9479 range>=0.05 monotonic when HF succeeds OR explicitly unavailable with 2 attempts logged) AND Gate0 >=50 transitions/family on >=10 families leakage <0.40.

**(C) Otherwise** if A passes but not all B conditions: **FALSIFIED** if orthogonal union still <=4 families only and AX_consistency fails and WebGym <50 and Gate0 <10 families (bounded FALSIFIED to 4-family ceiling on these censuses); **MIXED** if any module passes (e.g., orthogonal >=10 families survives but WebGym UNAVAILABLE, or AX survives but Stagehand <0.8). Audit may bound ceiling narrower than SURVIVES.

All metrics recomputed with trajectory-grouped family-level bootstrap; transition-grouped treated as MEASUREMENT_INVALID per prior audits.

---

## 9. Metrics and control identities (stable for downstream)

**Primary metrics:**
- `M_CONSTRUCTIBLE_FAMILIES` — distinct product families anchoring true + SHA stability both directions TRUE among S1|S2 union + canonical + orthogonal census (gate >=10)
- `M_CONSTRUCTIBLE_FAMILIES_ORTHO_ONLY` — count from orthogonal census alone (diagnostic)
- `M_AX_CONSISTENCY_MEAN` — full-tree multi-anchor AX_consistency mean on >=10 family set (gate >=0.6)
- `M_AX_CONSISTENCY_CI_LOWER` — bootstrap 95% lower (gate >0.5)
- `M_AX_SHUFFLE_P` — trajectory-grouped family-label shuffle p (gate <0.05)
- `M_AX_GAP` — mean - shuffle mean (gate >=0.20)
- `M_AX_DELTA_TRUNCATED` — full-tree - [:20] truncated (gate >=0.20)
- `M_AX_VALID_CAPTURES` / `M_AX_PRODUCT_FAMILY_COUNT` — AX liveness gates (median AX>10, >=10 families)
- `M_WEBGYM_DIVERSE_ETLD` — distinct eTLD+1 count (gate >=50)
- `M_WEBGYM_DUP_PREVALENCE` — duplication prevalence CI non-degenerate
- `M_WEBGYM_SWEEP_RANGE` — prevalence_0.818 - prevalence_0.9479 (gate >=0.05)
- `M_STAGEHAND_HIT_POST_STRIP` — Stagehand HIT after expanded stripping (gate >=0.8)
- `M_STAGEHAND_LIFT` — post minus pre stripping (gate >=0.40)
- `M_STAGEHAND_HIT_ROTATION_INSENSITIVE` — variant HIT with rotation-insensitive/freshness-gated SHA
- `M_GATE0_TRANSITIONS_PER_FAMILY` — per-family transition counts dict (gate >=50 each on >=10 families)
- `M_GATE0_FAMILIES_MEETING_THRESHOLD` — number families >=50 (gate >=10)
- `M_GATE0_LEAKAGE_VALID_ONLY` — leakage valid-only (gate <0.40)
- `M_RHO_SHUFFLED` — |rho_shuffled| family-level (gate <0.20)
- `M_HARD258_FAMILIES_GE3` — Hard258 families_ge3 diagnostic (for provenance)

Controls and baselines keyed by IDs in §5-6 preserved in result.json:controls exactly.

---

## 10. Product consequences

**If SURVIVES:** Intel delivers Codex-accepted durable orthogonal census artifacts (pinned manifest SHA d6527566 927596 bytes + GHCR 0.14.3 digest + Docker digest 3e8cb9b9... 64 hex + orthogonal census >=10 families with deterministic Random(35725763380).sample + WebGym diverse-sample duplication CI B=2000 sweep 0.818-0.9479 range>=0.05 replacing 567MB LFS + Gate0 >=50 transitions/family on >=10 families) unblocking Graph >=10-family product hold-out N>=120 without re-probing liveness and Physics Gate0 N=1000-1999 beyond-memory tests; repaired 1280x720 CDP full-tree multi-anchor AX_consistency mean>=0.6 CI lower>0.5 gap>=0.20 + body+expanded stripping + Stagehand HIT>=0.8 rotation-insensitive/freshness-gated becomes shared substrate satisfying runtime:C-MEAS-VALID dependency; external Stagehand ceiling defines verification gate product must beat for residual-novelty economics. C-CROSSSITE advances toward EXPERIMENTAL at durable-artifact+diverse-holdout+Gate0 ceiling with full-tree validity, C-MEAS-VALID gains health-gated single-node substrate before distributed n>=800, C-WEB-DYNAMICS gains valid diverse family bank for beyond-memory PMI.

**If FALSIFIED:** Deterministically proven that BOTH pinned 812+Hard258 union (4 families [136,145,196,222]) AND attempted orthogonal censuses (WebMall/Mind2Web-2 130-task, Mind2Web expansion, WebGym-derived families available after HF_TOKEN) contain <10 constructible product families with anchoring+SHA stability or AX_consistency fails <0.6 or Stagehand HIT <0.8 even after rotation-insensitive/freshness-gated variant, or Gate0 <50/family on <10 families — so Graph >=10-family hold-out remains BLOCKED on these censuses and Physics Gate0 remains unmet, requiring further orthogonal census (independent eTLD+1 hosting with verified product_page heuristics beyond current 130-task or new 292k family sampling) or definition expansion beyond shopping vs shopping_admin 404, and must not re-attempt longest-prefix or N=20 probe on same 4-family slug-URL substrate (expected MEASUREMENT_INVALID). If WebGym diverse <50 or sweep <0.05, single-store duplication vacuous remains. C-CROSSSITE stays HYPOTHESIS/EXPERIMENTAL at 4-family ceiling, C-MEAS-VALID/C-WEB-DYNAMICS remain HYPOTHESIS. 

**If MEASUREMENT_INVALID:** No claim update; smallest repair per MV1-MV8 (genuine attempts >=2, versions 0.14.3, CDP full-tree, deterministic samples on BOTH censuses, expanded stripping ablation, honest Gate0 counters, trajectory-grouped B=2000, threshold sweep, AX_consistency multi-anchor) and re-run identical frozen design.

---

## 11. Validity threats and mitigations

- **Single-node vs distributed gap:** Director portfolio notes factory tunneled on MEASUREMENT_INVALID via AX substrate and WebGym diverse fetch. Runtime single-node health-gated harness is explicit dependency; all Gates require median AX>10 before distributed n>=800 promotion. This experiment runs single-node only, documenting that ceiling, not claiming distributed.
- **Template overlap independence threat:** Hard258 derived from same base as primary — not fully independent. This design tests genuinely orthogonal census (WebMall/Mind2Web-2 independent eTLD+1 hosting, WebGym families) with template overlap diagnostic; if union <10, result is bounded FALSIFIED not global rejection — truly orthogonal census remains next step per do_not_assume.
- **Degenerate CIs:** Prior audit flagged BMEM [0,0] and ROUTING/WebMCP [1,1] variance 0 invalid width; this prereg requires interior non-degenerate width when variance>0 and explicit flag when degenerate — prevents misreading zero-variance as high-precision. Trajectory-grouped family-level bootstrap required.
- **Synthetic-to-real gap:** Synthetic orthogonal baseline not used here; real WebGym diverse eTLD+1 and BrowserGym multi-step are real site diversity. Real WebArena hold-out transfer remains unknown until Graph runs N>=120 hold-out with this census — this experiment only delivers the census artifact, not the hold-out transfer itself.
- **Work compression honesty:** Prior per_hit 1.005>0.85 falsified superseded by M_total Pareto. This experiment enforces honest per-trajectory-reset counters for Gate0, prohibits n*constant proxies, requires trajectory-grouped bootstrap and |rho_shuffled|<0.20 if Pareto later computed.
- **BrowserGym API mismatch:** Prior Gate0 0/50 due API mismatch and 110 transitions/family with NL=3 insufficient density. This prereg pins BrowserGym-core 0.14.3 AgentLab 0.4.2 and requires per-trajectory counters with leakage measurement; if API mismatch persists after 2 genuine attempts logged UNAVAILABLE not zero.
- **Stagehand instability:** Prior exact full-DOM SHA256 hash_changed_on_every access 36/36 tautological MISS. This prereg requires relevant-subtree SHA256 recomputed after page.content()+AX via page.evaluate with expanded stripping and rotation-insensitive/freshness-gated variant to test true stability vs drift.
- **HF_TOKEN availability:** WebGym diverse clause alone does not gate MEASUREMENT_INVALID if HF_TOKEN absent after 2 genuine 401/404 attempts; then PC-C UNAVAILABLE and sweep null correctly, but H_A can still SURVIVE on orthogonal census alone with documented UNAVAILABLE — prevents infrastructure failure masquerading as falsification.

---

## 12. Preregistration freeze

- Hypothesis, state/action representations, sampling policy (Random(35725763380).sample x2 per census, get_task_start_url __SHOPPING__ expansion, product-subtree node_count>1), target (>=10 families), holdout (deterministic 10 per census), nulls/baselines, primary metrics, expected directions, uncertainty method (trajectory-grouped family-level B=2000 percentile CI, 1000 perms AX shuffle, 2000 family-level WebGym duplication), adequacy rule (median AX>10 DOM>=2000, CI lower>0.5, gap>=0.20, sweep range>=0.05, Gate0 >=50/family on >=10), falsification/survival rule (§8) frozen before outcome.
- Any changed analysis after seeing outcomes is exploratory. New confirmatory claim requires new preregistration and untouched evidence.
- DESIGN did not inspect outcome measurements. EXECUTE must execute exactly this frozen design; may not mutate frozen inputs.

---

## 13. Estimated cost and information gain

**Compute:** 5-7h runner wall (GHCR 5.4GB if not cached + Docker webarena-shopping pull, 2x genuine attempts per source HF+GHCR+Hub each 300s or docker load fallback ~20-35min, orthogonal census derive/parse WebMall/Mind2Web-2 130-task + Mind2Web 404 expansion + WebGym 292k parse/sample threshold sweep 0.818-0.9479 ~20min, deterministic sampling x2 per census + anchored AX probe on >=10 families per census + Gate0 multi-step collection >=50 transitions/family on >=10 families across 6 site families via BrowserGym loop ~60-90min at 1280x720 CDP, Stagehand relevant-subtree vs full-DOM HIT ablation x2 ~20min + B=2000 bootstraps + truncation delta ~30min). Network 2x attempts + API 200 + WebGym download only if HF_TOKEN valid. No LLM calls required. USD ~$5-7 GH runner + $0 if HF_TOKEN cached. Artifact storage <120MB.

**Expected information gain:** High, Director-ranked CONTINUE gating, cognitive_reset true, USE parent_handoff. Directly answers whether 23-deep Intel tunnel can escape 4-family ceiling via genuinely orthogonal census (not Hard258 union) and whether 567MB LFS exhaustive is replaceable by sweep CI plus whether BrowserGym multi-step can deliver Gate0 >=50 transitions/family on >=10 families for physics beyond-memory tests — unblocking the two central factory-blocked artifacts (Graph N>=120 hold-out and Physics N=1000-1999 PMI) that prior 8 pilots left MEASUREMENT_INVALID due census contamination, homepage-only AX substrate and API mismatch. Quantifies full-tree AX_consistency Pareto and Stagehand HIT>=0.8 rotation-insensitive ceiling plus WebGym diverse duplication CI for site diversity. Bounded negative equally decision-changing. Higher leverage than another N=20 homepage AX_consistency or exhaustive LFS per Director comparative_reasoning and Scout 4/10 MEASUREMENT_INVALID diagnosis.

---

## 14. Provenance and reproducibility

Every artifact path+sha256 stored in provenance.json and freeze.json. Required: request/spec/prereg/freeze hashes, pip freeze hash nonempty (263 lines), docker images --digests, ghcr_browsergym_attempts, docker_hub_api_attempts, command logs pull/load/run, HF manifest sha/bytes or 401 log, WebGym sha when available, orthogonal census provenance (WebMall/Mind2Web manifests, histograms, S1/S2 samples), Hard258 census sha, synthetic generation sha if used, census derived jsons primary+orthogonal, ax captures/probe logs, threshold sweep table, AX_consistency fulltree json, Stagehand stripping delta, Gate0 per-family transition counts and leakage logs, grammar hash live. Missing provenance -> MEASUREMENT_INVALID for that module.

Pipeline versions pinned: BrowserGym-core 0.14.3, AgentLab 0.4.2, Playwright 1.63.0, viewport 1280x720, CDP Accessibility.getFullAXTree, grammar_fulltree_*.py body regex DOTALL, expanded stripping regex fotorama\d{6,} + {form_key,uenc,store,session,nonce,timestamp}. Deterministic seeds 35725763380 (census) and 360360 if synthetic needed.

---

*End of preregistration — frozen before execution. Any deviation during EXECUTE must be logged as validity_notes and may trigger MEASUREMENT_INVALID per §8.*
