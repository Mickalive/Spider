# Preregistration — EXP-INTEL-36042590671

**Lane:** intel — Find, reproduce and stress-test datasets, baselines and prior art only when they can alter a live SPIDER claim  
**Experiment ID:** EXP-INTEL-36042590671  
**Claim IDs:** C-CROSSSITE (primary — Director PIVOT target)  
**Request ID:** ff2143ae510ed74d27560fe6 • **Request hash:** b2b66b0d26889a5e7b2e1ace53b6574f249e855fcb621c138a81dd7915f9b3fd  
**Director mandate:** PIVOT • **Target claim:** C-CROSSSITE • **Cognitive reset:** true • **Parent handoff disposition:** SUPERSEDE (EXP-INTEL-36037208652 preserved as continuity evidence only — do not re-test longest-prefix on 4-family slug-URL)  
**Freeze status:** DESIGN — no outcome-bearing measurements inspected. Spec and prereg frozen before EXECUTE.

---

## 1. Strategic question (Director binding)

> Can HF_TOKEN-provisioned WebGym 292k/127k manifests replace exhaustive 567MB LFS test.zip/CAP 420-task enumeration by delivering: (a) sampled >=50 diverse eTLD+1 sites via HF_TOKEN for duplication prevalence 95% CI (2000 family-level bootstrap, non-degenerate width>0) and threshold sweep at 0.818 and 0.9479 range>=0.05 monotonic (vs vacuous single-store 0.9479), parameterization prevalence 0.8958 with byte-identical manifest SHA verification, (b) WebArena-Verified v2 812 via pinned GHCR am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (SHA d652756608) proving >=10 constructible product families via deterministic random.Random(35725763380).sample(sorted families_ge3,10)x2 with get_task_start_url __SHOPPING__ expansion and product-subtree anchoring (heading/price/add-to-cart) with SHA stability before==after identical and before!=after on mutation at 1280x720 CDP Accessibility.getFullAXTree AX>10, thereby unblocking Graph single-family zero-overlap and Physics banks without further exhaustive enumeration?

Director `comparative_reasoning`: Continuing Intel's parent handoff (18/20 identical homepage/template Magento AX, unstable Stagehand exact-match, Gate0 0 transitions) re-tests longest-prefix on non-product pages and exact-cache without expanded stripping — bounded FALSIFIED with no product-page transfer. Orthogonal WebMCP prevalence counting is lower leverage than delivering the sampled diversity census that all of Graph/Physics/Product depend on. Sampled WebGym manifest with family-level bootstrap is higher expected information per attempt than 26th exhaustive LFS attempt.

Director `rationale`: Intel IDLE 25-streak C-CROSSSITE tunnel, last MIXED 36037208652, all recent MIXED/MEASUREMENT_INVALID from exhaustive 567MB LFS, CAP Docker, ModuleNotFoundError browsergym, HF 401/404. Exhaustive enumeration repeatedly BLOCKED and has not delivered true website holdout. WebGym 292k/127k (292k tasks 127k sites) already scaled RL 26%->42.9% OOD beating GPT-4o and provides durable diverse census via HF_TOKEN that SPIDER has not leveraged; deterministic sampling proof + product-subtree SHA is the minimal unblocking census for cross-site parameterization vs vacuous duplication baseline.

Director `agent_priors_used` (labeled not SPIDER evidence): O(1) compilation dominance, alias tunnel diminishing returns after 17 trials at regex ${slot}+Jaccard>=0.6, calibrated abstention need (ECE<=0.15 etc), memory-beats-no-memory is weak baseline vs RAG k5 / Stagehand/TERX strong replay, Graph reuse != Physics.

This converts to the smallest rigorous falsifiable test below. We do **not** re-exhaust HF 567MB LFS test.zip nor re-probe the same 4-family slug-URL with N=20 longest-prefix, nor re-run full Gate0 multi-step collection (deprecated for this pivot). We test whether a sampled >=50 eTLD+1 slice via HF_TOKEN + byte-identical pin + threshold sweep can replace exhaustive holdout prerequisites for Graph/Physics.

---

## 2. Inherited state (parent handoff EXP-INTEL-36037208652 — audit REVISE, producer_claim_supported false, bounded 4-family ceiling)

Parent reference: `research/experiments/EXP-INTEL-36037208652/handoff.json` sha `63329ba4519279d4f87b0aa7690d8a2eefe4abdf4e9f082a44da84470ddff0aa`, inherited_next_question = orthogonal census + AX + Stagehand + Gate0 on >=10 families (Now SUPERSEDED).

**Established (preserved, not re-assumed beyond evidence):**

- Durable single-source pin: WebArena-Verified manifest SHA `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` 927596 bytes byte-identical x2 via GitHub raw 200x2 + Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` Hub API 200x3 digest true `SRC_DOCKER_SUCCESS` (GHCR UNAVAILABLE after 6 genuine attempts token403/manifest404/pull denied, single-source suffices per prior prereg). `result.json` B-DURABLE-PIN-812 PASS audit MV1 PASS MV2 PASS.
- Census demographics: primary 812 total 192 shopping 36 families_ge3 21 product tasks 4 product_page families [136,145,196,222]; Hard258 258 total 61 shopping 11 families_ge3 6 product 2 families [136,145] subset of pin; deterministic `random.Random(35725763380).sample(sorted families_ge3,10) x2 S1==S2` exact per census logged.
- Constructibility at 1280x720 CDP `Accessibility.getFullAXTree` (BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 Chromium 153): exactly 4 families constructible with product-subtree anchoring heading2 price6 add_to_cart2 main226-365 contentinfo31 + distinct outerHTML SHA256 body regex `<body[^>]*>.*?</body>` DOTALL + 9 base + expanded `{form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp}` before SHA via `page.evaluate` recomputed after `page.content()+AX`, SHA before==after TRUE and after mutation !=TRUE 12/12 median AX717 min627 DOM203748 min195052; median AX 702.5 DOM218149 PASS on 4-family captured set.
- Full-tree multi-anchor `AX_consistency` pipeline validated as non-vacuous on 4-family slug-URL: mean 0.45426266 CI[0.39603,0.51637] B=2000 family-level gap0.143 shuffle mean0.311 p0 variance0.004755 delta_vs_truncated0.427 truncated_mean0.027 median AX>10 DOM>=2000 PASS; shuffle distinguishes (p0) but gates FAIL >=0.6/>0.5/>=0.20 on this substrate vs parent 0.6208 catalog-id — substrate sensitivity disclosed.
- Synthetic alias-OOD 40-task blind harness byte-identical 409 rows: DSM 0.75 [0.625,0.875] interior non-degenerate, HITL drop 0.50, USD 0.0353, WebMCP prevalence 0.725, Stagehand HIT_post 0.775 HIT_pre 0.0 lift0.775 per-channel header1.0 auth1.0 body0.7 mixed0.4, BMEM [0,0] degenerate flagged, ROUTING/WebMCP [1,1] degenerate flagged, |rho_shuffled|0.1936 PASS <0.20 honest per-trajectory counters.

**Rejected (bounded, do not re-attempt without genuinely new source):**

- H_A >=10 distinct product families from pinned WebArena 812 + Hard258 union under frozen anchoring+SHA — bounded FALSIFIED to 4 families deterministically (union still 4, homepage 16 identical localhost:7770/ excluded per MV4 product_page requirement — counting them is measurement fraud). Not global impossibility beyond new eTLD+1 hosting.
- Full-tree mean>=0.6 CI lower>0.5 gap>=0.20 on 4-family slug-URL — bounded FAIL 0.454/0.396/0.143 on this substrate; not falsified on >=10-family set untestable and not on catalog-id 0.6208 substrate.
- Stagehand exact selector+relevant-subtree SHA256 HIT>=0.8 — bounded FALSIFIED to 0.775 (31/40) lift0.775 mixed 0.4 caps ceiling pre-strip 0.0.
- NC2 shuffled-variant delta <0.05 with literal token-reassignment — unfalsifiable structural floor ~0.31; requires mutation-sensitivity adjudication not literal reassignment.
- Degenerate CIs [0,0] BMEM and [1,1] ROUTING/WebMCP as high-precision — rejected per audit validity_findings.

**Unknown (this experiment targets, now reframed by Director):**

- Whether >=10 constructible product families exist in the **union** of pinned 812 plus a HF_TOKEN-sampled WebGym diverse slice (not just 812+Hard258) under identical frozen anchoring+SHA stability at 1280x720 CDP.
- Whether WebGym 292k/127k sampled >=50 diverse eTLD+1 with family-level B=2000 CI width>0 and threshold sweep at 0.818 and 0.9479 range>=0.05 monotonic (vs vacuous 0.9479) can be delivered via HF_TOKEN and replace 567MB LFS test.zip artifacts.
- Parameterization prevalence 0.8958 on diverse bytes with byte-identical SHA verification.
- Whether GHCR BrowserGym 0.14.3 64-char digest + Docker Hub digest cross-source equality is verifiable (previously UNAVAILABLE) and whether fresh live CDP probe (not reused captures) satisfies AX>10 health gate.
- Real production Stagehand/WebMCP economics on live Magento and hold-out transfer N>=120 — remains unknown; this census only provides the prerequisite artifact.

**Do-not-assume (preserved):**

- Do not assume >=10-family constructibility from pinned WebArena 812 or Hard258 union or homepage probes (16 identical localhost:7770/ with heading2 price4 — excluded per frozen MV4).
- Do not assume GHCR fetchable or cross-source byte-identity verified (GHCR 6 attempts token403/manifest404/pull denied UNAVAILABLE, HF 2x401 UNAVAILABLE; only Docker single-source durable).
- Do not treat degenerate CIs [0,0] or [1,1] as high-precision; flag variance 0 per prereg 12.7.
- Do not equate synthetic M_total work units or USD patch-cost with wall-clock/browser steps; false_accept 0.0 structural artifact not safety claim.
- Do not assume 0.4543 generalizes to >=10-family gate or parent 0.6208 catalog-id implies slug-URL passes; substrate sensitivity open delta 0.427 only proves non-vacuous vs truncated not gate satisfaction.
- Do not assume Stagehand HIT 0.775 ~0.80 or NC2 floor 0.311 <0.05 achievable under literal reassignment.
- Do not assume WebGym UNAVAILABLE (401) implies falsified duplication 0.9479 or sweep unnecessary — sweep remains untested per MV5 exception.
- Do not assume reused AX captures equal fresh live CDP probe for Codex acceptance — fresh live probe required.
- Do not infer global C-CROSSSITE impossibility from bounded 4-family falsification; C-CROSSSITE remains HYPOTHESIS globally with durable 4-family ceiling.

**Director disposition:** Parent `next_question` (orthogonal WebMall/Mind2Web-2 + GHCR Gate0) is **SUPERSEDED**. Director PIVOT with `cognitive_reset:true` is binding: stop refining same representation (regex `${slot}+Jaccard>=0.6` after 17 trials), stop exhaustive LFS enumeration, deliver the sampled diversity census via HF_TOKEN that Graph/Physics/Product depend on. Handoff categories above are continuity evidence only and MUST NOT silently override Director decision.

---

## 3. Hypotheses

### H_SAMPLED_CENSUS_REPLACES_EXHAUSTIVE (primary)

A HF_TOKEN-provisioned sampled census from WebGym 292k tasks / 127k sites manifests plus the pinned WebArena-Verified v2 812 manifest jointly replace exhaustive 567MB LFS enumeration:

- **(i)** sampled slice of **>=50 distinct eTLD+1** sites (family-level grouping preserved, eTLD+1 via `tldextract`/publicsuffix documented, deterministic or sequential slice with seed logged) yields **family-level bootstrap B=2000 95% percentile CI** for duplication prevalence with **width>0** non-degenerate (`variance>0`, degenerate `[0,0]/[1,1]` flagged) vs vacuous single-store `0.9479` baseline;
- **(ii)** **threshold sweep at Jaccard/template similarity 0.818 and 0.9479** on the same diverse set is **monotonic decreasing** with **range = prev(0.818) - prev(0.9479) >=0.05**;
- **(iii)** **parameterization prevalence = 0.8958 +-0.05** (field where varying value extraction yields template slot, `prevalence = param_slots / total_candidate_fields`, tolerance documented) with **byte-identical manifest SHA verification** (WebArena `d652756608...` 927596 bytes + Docker `sha256:3e8cb9b945...` 64-hex + WebGym manifest 64-hex);
- **(iv)** the **union of WebArena 812 families_ge3 plus sampled WebGym families yields >=10 distinct product families constructible** under identical frozen protocol: deterministic `random.Random(35725763380).sample(sorted families_ge3,10)` executed **TWICE with seed reset `S1==S2` logged on EACH census**, `get_task_start_url __SHOPPING__` expansion, product-subtree anchoring `heading/price/add-to-cart/main/contentinfo node_count>1`, distinct outerHTML SHA256 with `<body[^>]*>.*?</body>` DOTALL + 9 base + expanded `{form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp}` stripping before SHA via `page.evaluate` recomputed after `page.content()+Accessibility.getFullAXTree`, **SHA before==after TRUE and after DOM textContent mutation !=TRUE**, at **1280x720 CDP `Accessibility.getFullAXTree` median AX>10 DOM>=2000** on canonical families [136,145,196,222] (12 captures).

This census provides the durable diverse artifact for Graph single-family zero-template-overlap parameterization and Physics website-holdout banks.

---

## 4. Falsifier

**H falsified if** after **>=2 genuine attempts per durable source** (HF_TOKEN-authenticated fetch for WebGym 292k / 127k site manifests and WebArena 812 via GitHub raw, plus GHCR BrowserGym 0.14.3 and Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945...`, each `timeout>=300s` or `docker load` fallback, URL/HTTP status/bytes/sha256 hex/64-char digest logged, `HF_TOKEN present true/false` logged, 401/404 captured, stderr/stdout in artifacts) any primary gate fails:

- **(A)** `M_WEBGYM_DIVERSE_ETLD <50`, or family-level `B=2000` bootstrap 95% CI **not computed or degenerate width==0** (variance pooled collapses to single-store, flagged per prior audits), or threshold sweep at `0.818` and `0.9479` **not computable / not monotonic decreasing / `M_WEBGYM_SWEEP_RANGE <0.05`** (vs vacuous `0.9479` not beaten), or `M_PARAM_PREVALENCE` outside `0.8958 +-0.05` or manifest byte-identity fails (`SHA != d652756608...` or Docker digest mismatch), **OR**
- **(B)** `M_CONSTRUCTIBLE_FAMILIES <10` distinct with anchoring true + SHA both-directions TRUE and CDP `1280x720` `median AX>10 / DOM>=2000` fails on canonical 12 captures.

Single-module fail → **MIXED**, all fail → **FALSIFIED**, all pass → **SURVIVES**. No inference if `MEASUREMENT_INVALID` gating fails. When `HF_TOKEN` absent after 2 genuine 401/404 attempts, duplication/threshold clause is **UNAVAILABLE** (not falsified) but overall H still requires `(B) >=10` to `SURVIVE`; vacuous `0.9479` alone does not satisfy `(A)`.

---

## 5. Baselines (stable IDs for EXECUTE/AUDIT reuse)

| ID | Type | Description | Expected |
|---|---|---|---|
| B-DURABLE-PIN-812 | durability | WebArena-Verified v2 812 tasks manifest SHA `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` 927596 bytes byte-identical x2 via GitHub raw 200 + Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945...` 64-char digest Hub API 200 + `docker pull --digests` or `docker load` fallback | SHA 64-hex equality, 927596 bytes, Docker digest 64-hex equality, families_ge3 >=30, container localhost:7770 HTTP 200 if pulled |
| B-WEBGYM-292K-SAMPLED-50 | dataset | Sampled diverse census replacing exhaustive 567MB LFS: HF_TOKEN-gated fetch of WebGym 292k/127k manifests, extract >=50 distinct eTLD+1 via tldextract/publicsuffix with family-level grouping preserved, duplication prevalence via Jaccard/template>=threshold (documented exact threshold) family-level B=2000 95% CI, and threshold sweep at 0.818 and 0.9479 | If HF valid: diverse >=50, CI width>0 non-degenerate, sweep range>=0.05 monotonic; if HF absent after 2 genuine 401/404 => UNAVAILABLE not zero with attempts logged per MV5 |
| B-VACUOUS-SINGLE-STORE | null_baseline | Vacuous single-store duplication prevalence 0.9479 (prior 18/20 identical homepage/template Magento AX). Diverse census must beat this via sweep range, not reproduce it | Prevalence ~0.9479 on single-store slice; diverse sample lower; sweep range 0.818-0.9479 >=0.05 proves non-vacuous |
| B-EXHAUSTIVE-LFS-567M | cost_baseline | Exhaustive baseline to replace: 567MB LFS test.zip / CAP 420-task full enumeration (prior 25-streak repeated BLOCKED). Reference cost only; sampled census must deliver durable SHA+CI+sweep without full download | Not executed; reference wall 5-7h, 567MB, repeated BLOCKED; sampled wall ~2.5-4h, <80MB, succeeds via HF_TOKEN |
| B-TRUNCATED-VS-FULLTREE | representation | Selectors/AX tokens [:20] truncated vs full-tree multi-anchor with expanded stripping. Delta = fulltree - truncated | Delta >=0.20 real vs <0.05 shuffled; validates that before==after SHA uses full body+expanded stripping not truncated proxy |

Per-census deterministic samples `S1/S2` and per-family anchoring json required for each census baseline.

---

## 6. Controls

### Positive control — PC-DURABLE-SHA-FIXTURE-SWEEP-SANITY

- **PC-A** Durable SHA fixture: WebArena manifest `d652756608...` 64-hex byte-identical x2 + Docker digest `64-hex` via Hub/GHCR API 200 verification; plus synthetic Flask product fixture at 1280x720 fixed DOM `heading+price+add-to-cart+main+contentinfo` localhost, AX tree ~17 nodes deterministic, pipeline must capture `median AX>10 DOM>=2000` and `SHA before==after TRUE 12/12` plus `mutated textContent SHA !=TRUE 12/12` and 12 captures on canonical families 136/145/196/222 `median AX>=627 DOM>=195052`. Also grammar hash live via `research/intel/grammar_fulltree_*.py` body regex DOTALL + expanded stripping `fotorama\d{6,}` — not hardcoded.
- **PC-B** Sweep sanity (gated `HF_TOKEN`): sampled diverse `>=50` yields duplication prevalence in `[0.30,0.99]` CI computable width>0 non-degenerate and threshold sweep monotonic at 0.818 and 0.9479 `range>=0.05`; when HF fails PC-B is `UNAVAILABLE` not failed.
- **PC-C** Parameterization sanity: parameterization prevalence `0.8958 +-0.05` on fresh manifest bytes; synthetic field-path harness with known 0.8958 prevalence returns inside tolerance and byte-identity passes.

*Expected:* PC-A `median AX>10 DOM>=2000 SHA both directions TRUE median AX>=627`; PC-B monotonic CI non-degenerate when HF succeeds else `UNAVAILABLE`; PC-C prevalence `0.8958 +-0.05` and byte-identity pass. Fail on any `TRUE` gate is control failure, not `UNAVAILABLE`.

### Null controls — NC-SHUFFLED-SINGLESTORE-TRUNCATED (all family-level)

- **NC1** Family-label shuffle for duplication prevalence (`B=2000` family-level) and AX_consistency (`B=1000` perms family-label shuffle): `|rho_shuffled|<0.20`, shuffle mean ~chance, `gap = real - shuffle >=0.20`, shuffled AX mean `<<0.6 p>0.05`.
- **NC2** Vacuous single-store: duplication prevalence on single-store slice remains `~0.9479` even after diverse sampling; diverse census prevalence must be distinct with `sweep range>=0.05` monotonic, proving diversity not vacuous. Prior 18/20 identical rejected as non-diverse baseline.
- **NC3** Truncated `[:20]` vs full-tree: `delta_vs_truncated = fulltree[0.818] - truncated` `>=0.20` real must hold; shuffled variant `<0.05`; degenerate CIs `[0,0]` or `[1,1]` variance 0 flagged per prior prereg 12.7 not counted as width.

*Expected:* NC1 `|rho|<0.20 p>0.05 gap>=0.20`, NC2 vacuous `0.9479` preserved and beaten by diverse sweep `range>=0.05`, NC3 `delta<0.05 shuffled`, no degenerate CI counted as high-precision. All CIs trajectory-grouped family-level (unit=`family`/`eTLD+1`), not transition-grouped.

All CIs trajectory-grouped family-level bootstrap 95% percentile. Degenerate `[0,0]` or `[1,1]` variance 0 flagged not counted as width.

---

## 7. Measurement validity (gating, frozen)

1. **MV1_DURABLE_ATTEMPTS:** Each durable source (HF for WebGym 292k + WebGym 127k sites + WebArena 812, GHCR for BrowserGym 0.14.3, Docker Hub `webarena-verified-shopping@sha256:3e8cb9b945...`) requires **>=2 genuine attempts** logged with URL/HTTP status/returncode, bytes, sha256 hex (64 hex), 64-char Docker digest substring check, `timeout>=300s` or `docker load` fallback captured (`docker pull ... --digests` or `docker load < tar, docker images --digests`), stderr/stdout. Single-attempt success → `MEASUREMENT_INVALID`. `HF_TOKEN present true/false` logged. GHCR and Docker Hub API digest 200 required. Evidence: `artifacts/raw/hf_webgym_manifest_attempts.json`, `artifacts/raw/hf_webarena_attempts.json`, `artifacts/raw/ghcr_browsergym_attempts.json`, `artifacts/raw/docker_hub_api_attempts.json`, `artifacts/raw/orthogonal_census_provenance.json`, `provenance.json` hashes.

2. **MV2_BYTE_IDENTITY:** Manifest SHA exactly `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (927596 bytes, 64 hex) equality stored via 2 independent HF raw fetches; GHCR BrowserGym image digest 64-char hex equality with GHCR API 200; Docker digest exactly `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` (64 hex after colon) Hub API 200. If one source succeeds, single sha256 pinned file + log suffices but cross-source equality explicitly `UNAVAILABLE` not assumed equal. WebGym 292k/127k SHA separately 64-hex logged when `HF_TOKEN` succeeds via 2 fetches. Reuse prior pinned file allowed only with `+2` fresh verification attempts logged this experiment.

3. **MV3_SAMPLED_DIVERSE_50:** WebGym sampled diverse census must document eTLD+1 extraction method (`tldextract` or publicsuffix list version pinned via `pip freeze`), family-level grouping preserved (site-family = eTLD+1 or task family as defined), sampling procedure (deterministic `random.Random` seed or sequential slice with seed logged, 300s handling), distinct eTLD+1 count `>=50` on success; if `HF_TOKEN` absent/401 after 2 genuine attempts `>=300s` each, count `null UNAVAILABLE` with attempts logged not zero. Duplication prevalence computed with documented Jaccard/template threshold, **family bootstrap B=2000 unit=family 95% percentile CI non-degenerate width>0**; grouping via family-level resampling not transition-level. Evidence: `artifacts/derived/webgym_sampled_census.json` (manifest SHA, bytes, extraction method, family histogram, eTLD+1 list, `B=2000` CI).

4. **MV4_THRESHOLD_SWEEP_0818_09479:** Threshold sweep at exactly `0.818` and `0.9479` on same sampled diverse set with same family grouping, prevalence at each threshold documented, **range = prev(0.818)-prev(0.9479) >=0.05**, **monotonic decreasing** (`prev@0.818 >= prev@0.9479`). Sweep table with per-threshold prevalence + CI logged. When `HF_TOKEN` fails sweep `null UNAVAILABLE` not zero. Vacuous single-store prevalence `0.9479` baseline separately computed or referenced as `B-VACUOUS` to prove diverse sweep is not vacuous; degenerate CI `[0,0]/[1,1]` width 0 flagged not counted.

5. **MV5_CONSTRUCTIBILITY_10FAM:** Deterministic constructibility executed exactly on **BOTH** WebArena 812 census and sampled WebGym diverse census: sorted `families_ge3` from census json, two independent draws `Random(35725763380).sample(sorted_families_ge3,10)` with seed reset `S1` and `S2` logged on **EACH** census (`S1==S2` expected but both logged). Each sampled family probed via `get_task_start_url __SHOPPING__` expansion + product-subtree anchoring `heading/price/add-to-cart/main/contentinfo node_count>1` distinct SHA256 with body regex `<body[^>]*>.*?</body>` DOTALL + 9 base + expanded `{form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp}` stripping before SHA via `page.evaluate` recomputed after `page.content()+Accessibility.getFullAXTree`, **SHA before==after TRUE and after mutation !=TRUE**. Viewport strictly `1280x720`, **CDP `Accessibility.getFullAXTree` via `cdp_session` required** (fallback `accessibility.snapshot` → `MEASUREMENT_INVALID` for this gate). Metrics `median AX>10 median DOM>=2000` on canonical 136/145/196/222 (12 captures) and on any sampled families achieving >=10. Without `BOTH` samples logged per census → `MEASUREMENT_INVALID` for that clause. BrowserGym-core==0.14.3 AgentLab==0.4.2 Playwright==1.63.0 `pip freeze sha256` nonempty.

6. **MV6_PARAM_PREVALENCE_08958:** Parameterization prevalence `0.8958` computed on sampled diverse bytes with documented field definition (`parameterizable slot = field where varying value extraction yields template slot`), **prevalence = param_slots / total_candidate_fields**, tolerance `+-0.05`, byte-identical manifest SHA verification required (depends MV2). Manifest bytes hashed before parsing; prevalence table with numerator/denominator logged. Synthetic positive control harness must reproduce `0.8958` inside tolerance on fixture. Missing manifest or tolerance not documented → `MEASUREMENT_INVALID` for prevalence clause.

7. **MV7_PROVENANCE:** Every artifact `path+sha256` stored in `provenance.json` and `freeze.json`: `request/spec/prereg/freeze` hashes, `pip freeze` hash nonempty, `docker images --digests` hash, GHCR/Docker Hub attempts, HF manifest sha/bytes or 401 log, WebGym sampled census json (manifest SHA, diverse eTLD+1 list, family histogram, B=2000 CI, sweep table), WebArena census summary, per-family anchoring json `S1/S2`, AX probe logs with `grammar_fulltree` hash live (`research/intel/grammar_fulltree_*.py` body regex present), threshold sweep table, param prevalence table, command logs. Missing provenance for any durability/diverse/sweep/constructibility path → `MEASUREMENT_INVALID` for that module.

---

## 8. Decision rule (frozen three-way, after MEASUREMENT_INVALID check)

**(A) MEASUREMENT_INVALID** if any mandatory `MV1-MV3`/`MV5-MV7` gating fails: `<2` genuine attempts per required durable source (HF WebGym 292k/127k, HF WebArena 812, GHCR, Docker Hub), missing 64-char digest or manifest SHA `d652756608...`, `pip freeze` empty or version/viewport mismatch (`0.14.3/0.4.2/1.63.0 1280x720`), fallback AX snapshot used, body regex absent, deterministic sampling not executed exactly as specified on **BOTH** primary (812) and sampled WebGym diverse census, family-level `B=2000` bootstrap not trajectory-grouped, or provenance missing. `MV4` sweep clause alone does **not** trigger `INVALID` when `HF_TOKEN` absent after 2 genuine 401/404 attempts but is marked `UNAVAILABLE` (`PC-B UNAVAILABLE`).

**(B) SURVIVES_CURRENT_TEST** iff `A` passes (`MV4` either `PASS` or documented `UNAVAILABLE` with at least sampled diverse `>=50` and threshold sweep either `PASS` or `UNAVAILABLE`) **AND** `H_A_SURVIVES`: `(SRC_GHCR_SUCCESS OR SRC_DOCKER_SUCCESS)` with byte-identical WebArena SHA, sampled diverse `>=50` distinct eTLD+1 with `B=2000` CI `width>0` non-degenerate and when HF succeeds sweep `0.818-0.9479 range>=0.05` monotonic (when HF fails this subgate `UNAVAILABLE`), parameterization prevalence `0.8958 +-0.05` with byte-identity, **AND** union constructibility `>=10` distinct product families anchoring true `SHA both directions TRUE` at `1280x720` CDP `median AX>10 & DOM>=2000` on canonical `136/145/196/222`. All metrics recomputed with trajectory-grouped family-level bootstrap.

**(C) Otherwise** if `A` passes but not all `B`: **FALSIFIED** if union still `<=4` families (bounded ceiling on attempted censuses) and diverse `<50` or sweep `range<0.05`; **MIXED** if any module passes (e.g., diverse `>=50 +` sweep passes but constructibility 4/10, or diverse `UNAVAILABLE` but constructibility `>=10`). Audit may bound ceiling narrower than `SURVIVES`.

All metrics recomputed with trajectory-grouped family-level bootstrap; transition-grouped treated as `MEASUREMENT_INVALID` per prior audits.

---

## 9. Metrics and control identities (stable for downstream)

**Primary metrics:**

- `M_WEBGYM_DIVERSE_ETLD` — distinct eTLD+1 count (gate `>=50`)
- `M_WEBGYM_DUP_PREVALENCE_MEAN` — duplication prevalence mean on diverse slice
- `M_WEBGYM_DUP_PREVALENCE_CI_LOWER` / `M_WEBGYM_DUP_PREVALENCE_CI_UPPER` — `B=2000` 95% CI bounds
- `M_WEBGYM_DUP_PREVALENCE_CI_WIDTH` — `upper-lower` (gate `>0` non-degenerate)
- `M_WEBGYM_SWEEP_AT_0818` — prevalence at 0.818
- `M_WEBGYM_SWEEP_AT_09479` — prevalence at 0.9479
- `M_WEBGYM_SWEEP_RANGE` — `prev0.818 - prev0.9479` (gate `>=0.05`)
- `M_WEBGYM_SWEEP_MONOTONIC` — `prev0.818 >= prev0.9479` (bool)
- `M_PARAM_PREVALENCE` — `param_slots/total` (gate `0.8958 +-0.05`)
- `M_MANIFEST_SHA_WEBARA` — `d652756608...` byte-identity (bool)
- `M_MANIFEST_SHA_WEBGYM` — WebGym 64-hex logged (bool)
- `M_CONSTRUCTIBLE_FAMILIES` — distinct union product families anchoring true + SHA stability both directions TRUE among `S1|S2` union + canonical + diverse census (gate `>=10`)
- `M_CONSTRUCTIBLE_FAMILIES_WEBARA_ONLY` — WebArena 812 alone diagnostic
- `M_CONSTRUCTIBLE_FAMILIES_DIVERSE_ONLY` — sampled diverse alone diagnostic
- `M_AX_MEDIAN` / `M_DOM_MEDIAN` — median AX nodes / DOM bytes (gates `>10` / `>=2000`)
- `M_SHA_STABILITY_TRUE` — `before==after TRUE` 12/12
- `M_SHA_MUTATION_SENSITIVITY` — `after mutation !=TRUE` 12/12
- `M_AX_VALID_CAPTURES` / `M_AX_PRODUCT_FAMILY_COUNT` — AX liveness gates (median AX>10, >=10 families)
- `M_RHO_SHUFFLED` — `|rho_shuffled|` family-level (gate `<0.20`)
- `M_WEBGYM_FAMILIES_GE3` — families_ge3 diagnostic for provenance

Controls and baselines keyed by IDs in §5-6 preserved in `result.json:controls` exactly.

---

## 10. Product consequences

**If SURVIVES:** Intel delivers Codex-accepted durable sampled census artifacts (pinned WebArena SHA `d6527566` 927596 bytes + GHCR `0.14.3` + Docker `3e8cb9b9...` 64-hex + sampled WebGym `>=50` diverse eTLD+1 with `B=2000` CI `width>0` and sweep `0.818-0.9479 range>=0.05` monotonic vs vacuous `0.9479`, param prevalence `0.8958`) and `>=10` constructible product families under frozen SHA-anchoring at `1280x720` CDP, **replacing exhaustive 567MB LFS/CAP 420 enumeration**. This unblocks Graph single-family zero-template-overlap param-inherit gate (`N>=120` hold-out without re-probing liveness) and Physics website-holdout banks (true `eTLD+1` hold-out with family-level CI) without further exhaustive fetches; shared substrate satisfies `C-MEAS-VALID` single-node health gate before distributed `n>=800`. `C-CROSSSITE` advances from `HYPOTHESIS` toward `EXPERIMENTAL` at diverse-holdout + parameterization ceiling; external `O(1)` compilation baselines (Stagehand/TERX) can now be compared against honest diverse hold-out.

**If FALSIFIED:** Deterministically proven that pinned WebArena 812 (4 families [136,145,196,222]) plus HF_TOKEN-sampled WebGym diverse slice available after provisioned attempts still yields `<10` constructible product families with anchoring+SHA stability, or diverse `<50 / B=2000 degenerate / sweep range<0.05` not monotonic / param prevalence outside `0.8958 +-0.05`, so Graph `>=10`-family hold-out remains **BLOCKED** on these censuses and Physics banks remain unmet; sampled census does **NOT** replace exhaustive 567MB LFS. Requires next **orthogonal** census via independent `eTLD+1` hosting beyond current WebGym slice (new family sampling with independent hosting) or definition expansion beyond `shopping` vs `shopping_admin`, and must **not** re-attempt exhaustive `567MB LFS` or `N=20 longest-prefix` on same 4-family slug-URL substrate (expected `MEASUREMENT_INVALID`). If diverse `UNAVAILABLE` due `HF 401/404` after 2 attempts, `HF_TOKEN` provisioning or alternative WebGym hosting is smallest repair. `C-CROSSSITE` stays `HYPOTHESIS` at 4-family ceiling, `C-MEAS-VALID` remains without diverse bank.

**If MEASUREMENT_INVALID:** No claim update; smallest repair per `MV1-MV7` (genuine attempts `>=2`, versions `0.14.3`, CDP full-tree, deterministic samples on BOTH censuses, `B=2000` trajectory-grouped, threshold sweep, `AX_consistency` multi-anchor, expanded stripping, `AX>10`) and re-run identical frozen design.

---

## 11. Validity threats and mitigations

- **Single-node vs distributed gap:** Factory tunneled on `MEASUREMENT_INVALID` via AX substrate and WebGym diverse fetch. Runtime single-node health-gated harness (`BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 1280x720 CDP`) is explicit dependency; all Gates require `median AX>10` before distributed `n>=800` promotion. This experiment runs **single-node only**, documenting that ceiling, not claiming distributed. Pivoted design drops prior multi-step Gate0 `>=50 transitions/family` collection — that 5-7h cost repeately BLOCKED via `GHCR 404`/API mismatch (prior `0/50` and `110` with `NL=3` insufficient); delivering the diverse census is higher leverage per Director.
- **Template overlap independence threat:** Hard258 derived from same base as primary — not fully independent. This design tests a **genuinely orthogonal** sampled census via `WebGym 292k/127k` independent `eTLD+1` hosting (127k sites by construction diverse), with `eTLD+1` histogram diagnostic; if union `<10`, result is **bounded FALSIFIED** not global rejection — orthogonal census remains next step per `do_not_assume` (previously bounded `0` WebMall/Mind2Web after `401/404`, not global impossibility).
- **Degenerate CIs:** Prior audit flagged `BMEM [0,0]` and `ROUTING/WebMCP [1,1]` variance 0 invalid width; this prereg requires **interior non-degenerate width when variance>0** and explicit `UNAVAILABLE` flag when `HF_TOKEN` fails — prevents misreading zero-variance as high-precision. Family-level bootstrap required (`unit=family`/`eTLD+1`).
- **Synthetic-to-real gap:** Synthetic alias harness not used for census gates; real `WebGym diverse eTLD+1` is real site diversity. Real WebArena hold-out transfer remains **unknown until Graph runs `N>=120` zero-overlap hold-out** with this census — this experiment only delivers the **census artifact**, not the hold-out transfer itself.
- **Work compression honesty:** Prior `per_hit 1.005>0.85` falsified superseded by `M_total` Pareto. This pivot enforces **honest family-level bootstrap** (`B=2000` unit=`family`) and `|rho_shuffled|<0.20` if Pareto later computed; prohibits `n*constant` proxies and transition-grouped CIs (→ `MEASUREMENT_INVALID` per audits).
- **HF_TOKEN availability:** WebGym diverse clause alone **does not gate `MEASUREMENT_INVALID`** if `HF_TOKEN` absent after `2` genuine `401/404` attempts; then `PC-B UNAVAILABLE` and sweep `null`, but `H_A` can still `SURVIVE` on constructibility `>=10` alone with documented `UNAVAILABLE` — prevents infrastructure failure masquerading as falsification, yet overall `SURVIVES` still requires diverse `>=50` when HF succeeds and at least `>=10` families in either case.
- **GHCR/Docker 404 stale pin threat:** Prior `GHCR manifest404` x2 + `pull denied` x2 after `6` attempts correctly logged `UNAVAILABLE` not zero. This design requires `>=2` fresh attempts with `docker load` fallback per `MV1`; single-source Docker pin (`sha256:3e8cb9b9...`) suffices per prior audit but cross-source equality explicitly `UNAVAILABLE` not assumed equal.
- **Representation loss:** Body regex `DOTALL` + 9 base + expanded stripping documented with live `grammar_fulltree` hash; truncated `[:20]` also computed for `delta>=0.20` diagnostic per `B-TRUNCATED`.

---

## 12. Preregistration freeze

- Hypothesis, state/action representations, sampling policy (`Random(35725763380).sample x2` per census, `get_task_start_url __SHOPPING__` expansion, product-subtree `node_count>1`, `B=2000` family-level), target (`>=10` families, `>=50` eTLD+1), holdout (deterministic `10` per census), nulls/baselines, primary metrics, expected directions, uncertainty method (trajectory-grouped family-level `B=2000` percentile CI, `1000` perms AX shuffle, `2000` family-level WebGym duplication), adequacy rule (`median AX>10 DOM>=2000`, `CI width>0`, `sweep range>=0.05 monotonic`, `prevalence 0.8958 +-0.05`, `constructible >=10`), falsification/survival rule (§8) frozen before outcome.
- Any changed analysis after seeing outcomes is **exploratory**. New confirmatory claim requires new preregistration and untouched evidence.
- **DESIGN did not inspect outcome measurements.** EXECUTE must execute exactly this frozen design; may not mutate frozen inputs.

---

## 13. Estimated cost and information gain

**Compute:** 2.5-4h runner wall (HF_TOKEN-gated manifests `2x` attempts per source WebGym 292k/127k + WebArena 812 each `300s` or cached ~10min, GHCR pull BrowserGym 0.14.3 5.4GB if not cached else `docker load` fallback ~20min, Docker Hub `webarena-shopping` pull ~10min, `pip freeze` + `playwright install --with-deps chromium` if needed ~10min, sampled diverse eTLD+1 extraction + `B=2000` bootstrap + threshold sweep `0.818/0.9479` ~20min, param prevalence extraction ~10min, deterministic sampling `x2` per census + `get_task_start_url __SHOPPING__` + anchored CDP probe on `>=10` families at `1280x720` CDP ~90min worst (12 canonical + up to 10 sampled each `AX+DOM+SHA` both directions), no multi-step Gate0 collection in this pivoted design — deliberate 2h saving vs parent 5-7h). Network `2x` attempts + API 200 + WebGym download only if `HF_TOKEN` valid. No LLM calls required. USD ~`$3-5` GH runner + `$0` if `HF_TOKEN` cached. Artifact storage `<80MB`.

**Expected information gain:** **High**, Director-ranked `PIVOT` gating, `cognitive_reset true`, `SUPERSEDE` parent handoff. Directly answers whether `25`-deep Intel tunnel can escape `4`-family ceiling via genuinely orthogonal sampled census and whether `567MB LFS` exhaustive is replaceable by threshold-sweep CI plus whether BrowserGym substrate can prove `>=10` constructible families for physics/Graph banks — unblocking the two central factory-blocked artifacts (Graph `N>=120` hold-out and Physics `N=1000-1999` PMI) that prior 8 pilots left `MEASUREMENT_INVALID` due census contamination and API mismatch. Quantifies sampled diverse duplication Pareto (`width>0`, `range>=0.05` monotonic) and `SHA` stability at `1280x720` CDP with body+expanded stripping. Bounded negative equally decision-changing. Higher leverage than another `N=20` homepage `AX_consistency` or exhaustive LFS per Director comparative reasoning and Scout `4/10 MEASUREMENT_INVALID` diagnosis.

---

## 14. Provenance and reproducibility

Every artifact `path+sha256` stored in `provenance.json` and `freeze.json`. Required: `request/spec/prereg/freeze` hashes, `pip freeze` hash nonempty, `docker images --digests` hash, `ghcr_browsergym_attempts`, `docker_hub_api_attempts`, `huggingface manifest sha/bytes or 401 log`, WebGym sampled census json (manifest SHA, diverse eTLD+1 list, family histogram, `B=2000` CI, sweep table, param prevalence table), per-family anchoring json `S1/S2`, `ax` captures/probe logs, `grammar` hash live, `Hard258` not required but WebArena census summary. Missing provenance → `MEASUREMENT_INVALID` for that module.

Pipeline versions pinned: `BrowserGym-core 0.14.3`, `AgentLab 0.4.2`, `Playwright 1.63.0`, viewport `1280x720`, `CDP Accessibility.getFullAXTree`, `grammar_fulltree_*.py` body regex DOTALL, expanded stripping regex `fotorama\d{6,}` + `{form_key,uenc,store,session,nonce,timestamp}`. Deterministic seeds `35725763380` (census) and `random.Random` reset per census.

---

*End of preregistration — frozen before execution. Any deviation during EXECUTE must be logged as validity_notes and may trigger MEASUREMENT_INVALID per §8.*

