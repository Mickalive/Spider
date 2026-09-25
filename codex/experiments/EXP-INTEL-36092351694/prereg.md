# Preregistration — EXP-INTEL-36092351694

**Lane:** intel — Find, reproduce and stress-test datasets, baselines and prior art only when they can alter a live SPIDER claim
**Experiment ID:** EXP-INTEL-36092351694
**Claim IDs:** C-CROSSSITE (primary — Director PIVOT target)
**Request ID:** fb0edd2f9fb38a185021819d • **Request hash:** 74ca455fc6381692589bbdf451d667d696ef0183c2065795e3b52b2ff60a68a5
**Director mandate:** PIVOT • **Target claim:** C-CROSSSITE • **Cognitive reset:** true • **Parent handoff disposition:** SUPERSEDE — parent handoff is continuity evidence only and MUST NOT silently override Director PIVOT
**Freeze status:** DESIGN — no outcome-bearing measurements inspected. Spec and prereg frozen before EXECUTE.

---

## 1. Strategic question (Director binding — PIVOT)

> Can Intel deliver a minimal viable shared manifest without exhaustive 567MB LFS/test.zip: pin WebArena-Verified v2 812 + Hard258 258 via GHCR ghcr.io/servicenow/browsergym:0.14.3 and am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (64-char hash, byte-identical SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30) plus rebuilt 192/36 synthetic Jaccard<0.30 disjoint L=8-14 via deterministic random.Random(35725763380).sample and product-subtree anchoring 1280x720 CDP AX>10 (mean>15 std>5 DOM>=2000, SHA stability before==after identical and before!=after on mutation) proving >=10 families constructible with deterministic get_task_start_url __SHOPPING__ expansion, and publish trajectory-grouped artifact for Graph/Frontier/Physics reuse while documenting WebGym 292k HF_TOKEN smallest-next-action (scope/quota/mirror) if UNAVAILABLE, avoiding further exhaustive enumeration?

Director `comparative_reasoning`: Versus continuing parent handoff's WebGym 300k >=50 eTLD+1 sampled diverse census (requires HF_TOKEN resolution, 2000 family-level bootstrap, threshold sweeps 0.818/0.900 vs 0.9479) which has failed twice with smallest-next-action already documented, minimal viable manifest pivot unblocks three dependent lanes this cycle and stops burning cycles on LFS enumeration. External baseline reproductions (DSM 99% compilation, TraceCompiler, Stagehand HIT/MISS) on same 192/36 remain secondary and can be added after manifest is durable.

Director `rationale`: Intel 28-deep CROSSSITE tunnel_flag true, last 6 H3/H4 censuses MEASUREMENT_INVALID on genuine WebGym 292k HF_TOKEN UNAVAILABLE (401/404) and BrowserGym AX census <5 families adequacy. Exhaustive 567MB LFS enumeration is blocked by token/census and has not delivered beyond single-store vacuity (0.9479 duplication). The unblocking deliverable for Graph zero-overlap param pilot and Frontier heterogeneous BrowserGym reuse is already achievable from pinned 812+258+192/36 without WebGym diversity; delivering that durable manifest has immediate portfolio value versus another HF_TOKEN retry that Scout notes requires smallest-next-action documentation only.

Director `agent_priors_used` (labeled not SPIDER evidence):
- Long-horizon path-dependence/salience bias prior — correct-family gating (softmax 0.15+jitter, no cross-family key adoption) is load-bearing; without it Pareto gains illusory
- Web lacks free compiler/test oracle — verification must be cheap deterministic snapshot-diff/contract (AX subtree SHA after dynamic-token stripping); LLM-as-judge (~68% agreement) cannot calibrate false_accept/ECE
- Honest amortized cost prior — per-trajectory hard-reset integer sum counters with |rho_shuffled|<0.20 via block-permutation; jitter/n*3200/f*6.0/bijective proxies bake in null and cause degenerate CIs — explains ~80% recent MEASUREMENT_INVALID
- Compression/pruning prior — token reduction alone does not prove residual-novelty economics unless novelty fraction explicitly controlled train-A/test-B
- Exploratory tunneling diagnostic prior — Frontier 7-deep and Intel 28-deep streaks are expected after architecture shift, judged on marginal information vs pivoting

Director `portfolio_assessment`: 366 canonical experiments: C-MEAS-VALID single-node EXPERIMENTAL restored (EXP-RUNTIME-36089494979 SUPPORTS stable-header HMAC-SHA256) but distributed n>=800 HIT remains UNKNOWN; Graph 8 param-inherit pilots MEASUREMENT_INVALID; Frontier residual-novelty FALSIFIED non-Pareto under honest counters; Intel 28-deep CROSSSITE blocked on HF_TOKEN/WebGym 567MB LFS. Highest-leverage sequence is Runtime distributed honesty gate + Graph contamination-free 192/36 pilot + Frontier live heterogeneous compilation bypass + Intel minimal manifest pivot.

This converts to the smallest rigorous falsifiable test below. We do **not** re-attempt exhaustive 567MB LFS test.zip / CAP 420-task full enumeration nor another HF_TOKEN-only retry without synthetic diversity. We test whether a minimal viable manifest (durable 812+Hard258+GHCR/Docker + rebuilt 192/36 Jaccard<0.30 + >=10 families 1280x720 CDP + trajectory-grouped shared manifest + WebGym smallest-next-action) can replace exhaustive holdout prerequisites for Graph/Physics/Frontier.

---

## 2. Inherited state (parent handoff EXP-INTEL-36084509510 — audit REVISE, MIXED, bounded 4/10 ceiling)

Parent reference: `research/experiments/EXP-INTEL-36084509510/handoff.json` sha `d8f64f7e5f6acf34d146d79491b8df719c5ac6cd7d24c159eea21e428dc4de82` — disposition **SUPERSEDE** per request.json: parent next_question is advisory continuity only; binding direction is director_mandate question §1.

**Established (preserved, not re-assumed beyond evidence):**

- WebArena-Verified v2 812 durable pin survives single-node 1280x720 CDP: manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 927596 bytes byte-identical x2 via 2 fresh GitHub raw 200 (github_cross_source_attempts.json sha 7580a892...), Docker Hub am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb via Hub API 200 + docker images --digests a5b6fb47ee9f, container localhost:7770 HTTP 200 — audit MV2 PASS_PARTIAL_SINGLE_SOURCE
- Census demographics: 36 families_ge3 [101,136,137,138,139,145,147,153,154,155,156,159,160,162,163,165,169,171,172,180,186,189,191,194,196,197,204,206,207,208,211,212,213,214,222,370], 4 product_page families [136,145,196,222] 21 tasks — webarena_census.json sha 1652d7ef...; BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 tldextract 5.3.2 viewport 1280x720 pip freeze 263 lines sha b68aff78... grammar live 273eafbcb... body regex <body[^>]*>.*?</body> DOTALL +9 base+expanded stripping present
- Deterministic sampling Random(35725763380).sample(sorted families_ge3,10) executed TWICE with seed reset S1==S2==[191,180,162,197,153,213,163,137,136,222] x2 on primary census verified recomputed; WebGym diverse correctly ERROR ValueError Sample larger than population x2 on empty families_ge3 0 with n_unique 0 logged per MV5 EACH census — deterministic_family_samples.json sha 3dd3cfa6...
- Constructibility ceiling bounded to 4 distinct product families [136,145,196,222] under frozen product-subtree anchoring (heading2 price6 add_to_cart2 main226-365 contentinfo31 node_count>1, DOTALL body regex +9 base+expanded {form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp} stripping via page.evaluate after page.content()+Accessibility.getFullAXTree, SHA before==after TRUE 12/12 mutated !=TRUE 12/12 at 1280x720 CDP Accessibility.getFullAXTree via cdp_session) — audit MV5 PASS_MEASUREMENT_VALID_BUT_GATE_FAIL; recomputed median AX 707.0 mean 742.416 std 138.174, DOM median 202526.5 all exceed gates >10/>15/>5/>=2000
- Full-tree multi-anchor AX_consistency quantitatively logged: mean 0.454 CI95 [0.396,0.516] B=2000 family-level variance 0.0047 vs truncated [:20] mean 0.875 variance 0 degenerate CI [0.875,0.875], delta real -0.4207 shuffled mean -0.379 p95 0.0056 per-shuffle truncated mean 0.834, shuffle |rho| 0.084 <0.20 PASS — audit B-TRUNCATED FAIL_INVERTED
- Durable attempt accounting valid per MV1: HF WebGym 6x401, HF WebArena 2x401, GitHub 2x200, GHCR 5x 403/404/denied, Docker Hub 2x200 all with URL/status/bytes/sha256/64-char digest timeout>=300s logged — audit MV1 PASS; HF_TOKEN present false correctly logged with smallest next action
- Shared manifest published at research/experiments/EXP-INTEL-36084509510/artifacts/derived/shared_diverse_manifest.json sha dd96d083... with deterministic seed S1/S2 per census, anchoring 1280x720 CDP, manifest SHAs (WebArena d6527566, WebGym null UNAVAILABLE), family histogram, bootstrap CI for AX_consistency (not duplication), sweep table UNAVAILABLE, Jaccard diagnostic, constructibility S1/S2, pip freeze + grammar + viewport; path+sha stored in provenance.json — audit MV8 PASS_WITH_DELTA_FAIL
- PC-C synthetic parameterization control passes: prevalence 0.8958 8958/10000 within +-0.05 — audit recomputed true but synthetic only, not real-manifest

**Rejected (bounded, do not re-attempt without genuinely new source):**

- H_SAMPLED_CENSUS_REPLACES_EXHAUSTIVE_REOPEN SURVIVES on attempted censuses: bounded MIXED/FALSIFIED to 4 families under frozen anchoring+SHA at 1280x720 CDP on WebArena 812 plus HF-unavailable WebGym diverse slice; union 4 <10 does NOT replace exhaustive 567MB LFS for Graph N>=120 or Physics banks — bounded not global impossibility beyond HF_TOKEN + independent hosting
- Full-tree multi-anchor AX_consistency gate mean>=0.6 CI lower>0.5 delta>=0.20 on 4-family slug-URL substrate — bounded FAIL inverted (mean 0.454 <0.6 delta -0.420)
- Claim that GHCR BrowserGym 0.14.3 cross-source digest is verifiable on this run — bounded UNAVAILABLE after 5 genuine 403/404/denied attempts
- Real-manifest parameterization prevalence via PC-C synthetic as satisfying MV6 diverse-bytes requirement — rejected per audit MV6 REVISE_SYNTHETIC_ONLY
- Degenerate CI treating UNAVAILABLE null as zero width — rejected

**Unknown (this PIVOT partly retargets — cognitive_reset true):**

- Whether WebGym 292k/127k manifest when HF_TOKEN provisioned contains >=50 distinct eTLD+1 and yields family-level B=2000 CI — requires HF_TOKEN; this PIVOT documents it as UNAVAILABLE with smallest-next-action (scope/quota/mirror) rather than blocking on it
- Threshold sweep at 0.818/0.900/0.9479 on sampled diverse bytes with byte-identical SHA and Jaccard<0.30 orthogonality — UNTESTED via HF 401; this PIVOT tests synthetic 192/36 Jaccard<0.30 disjoint L=8-14 as minimal viable orthogonality instead of requiring WebGym diverse sweep for SURVIVES
- Real-manifest parameterization prevalence 0.8958 on sampled diverse bytes — UNAVAILABLE pending HF_TOKEN
- Whether union WebArena 812 + synthetic 192/36 yields >=10 distinct product families constructible under frozen protocol with SHA both directions at 1280x720 CDP — unknown; this PIVOT directly tests it as primary gate
- Whether GHCR 0.14.3 cross-verifiable — UNAVAILABLE after 5 attempts
- Whether full-tree delta >=0.20 achievable on >=10-family set — unknown because 4-family delta inverted -0.420; synthetic orthogonal set is new test
- Whether shared manifest with trajectory-grouped artifact consumable by Graph/Frontier/Physics without LFS — published but unvalidated until WebGym diverse branch available; this PIVOT publishes minimal viable manifest with synthetic diversity and trajectory grouping

**Do-not-assume (preserved and extended):**

- Do not assume >=10-family constructibility from pinned WebArena 812 alone or shared manifest with UNAVAILABLE WebGym branches — union is 4 families bounded ceiling, not replacement for LFS
- Do not assume HF_TOKEN present or WebGym fetchable or cross-source byte-identity verified (HF 6x401 UNAVAILABLE; only Docker single-source durable — do not assume equality) — next run must log 2x300s attempts with 64-hex digests and HF_TOKEN present true/false plus smallest next action (scope/quota/mirror) when 401/404
- Do not conflate PC-C synthetic prevalence 0.8958 with real-diverse manifest prevalence; MV6 real clause remains UNAVAILABLE pending HF_TOKEN
- Do not use producer median 716 / DOM 203748 as exact without recomputed 707.0 / 202526.5; all gates median>10 mean>15 std>5 must be computed from fresh 1280x720 CDP captures
- Do not treat WebGym ERROR Sample larger than population from empty families_ge3 as diversity success; it is correct UNAVAILABLE logging
- Do not claim delta>=0.20 without quantitative per-shuffle delta table; prior delta -0.4207 is fail inverted
- Do not treat degenerate CIs [0,0]/[1,1] variance 0 as high-precision; family-level B=2000 with variance>0 is interior but fails gate mean>=0.6
- Do not assume GHCR fetchable or reused AX captures equal fresh CDP probe — fresh live 1280x720 CDP via cdp_session required
- Do not assume Jaccard<0.30 without pairwise product-subtree token Jaccard matrix on full-tree expanded stripping; diagnostic 0.5417/0.4611 on 4 WebArena families does NOT decide diverse gate
- Do not equate synthetic alias-OOD harness metrics with live wall-clock/browser steps
- Do not infer global C-CROSSSITE impossibility from bounded 4-family falsification; C-CROSSSITE remains HYPOTHESIS globally with durable 4-family single-node ceiling
- Do not re-attempt exhaustive 567MB LFS test.zip or CAP 420-task full enumeration or N=20 longest-prefix on same 4-family slug-URL substrate without HF_TOKEN-provisioned diverse hosting; expected MIXED/MEASUREMENT_INVALID
- **NEW PIVOT:** Do not assume WebGym >=50 required for SURVIVES in this experiment; WebGym branch is UNAVAILABLE with smallest-next-action documented, not falsification — durable 812+Hard258+synthetic 192/36 + >=10 families + shared manifest are the SURVIVES gates

**Director disposition:** Parent `next_question` is SUPERSEDE with PIVOT and cognitive_reset true — minimal viable manifest without exhaustive LFS is binding; parent handoff four-way distinctions above are continuity evidence only. Do not drift back to WebGym 300k >=50 threshold sweep as required gate for SURVIVES.

---

## 3. Hypotheses

### H_MINIMAL_VIABLE_MANIFEST_PIVOT (primary, C-CROSSSITE)

A minimal viable manifest pivot replaces the blocked exhaustive 567MB LFS / WebGym 300k >=50 eTLD+1 sampled census (which has failed twice with smallest-next-action already documented) with durable pins + synthetic diversity:

- **(i)** WebArena-Verified v2 812 manifest is byte-identical SHA `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` 927596 bytes verified via 2 fresh GitHub raw 200 and Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` 64-hex via Hub API 200 and/or GHCR `ghcr.io/servicenow/browsergym:0.14.3` (BrowserGym-core 0.14.3 AgentLab 0.4.2) 64-hex equality or documented UNAVAILABLE with 2x attempts >=300s; Hard258 258 subset reproducibly derived from same base with histogram preserved;
- **(ii)** rebuilt synthetic 192 tasks / 36 families disjoint `L=8-14` via deterministic `random.Random(35725763380).sample(sorted families_ge3,10)` executed TWICE S1==S2 logged plus product-subtree anchoring (heading/price/add-to-cart/main/contentinfo node_count>1), full-tree expanded stripping `{form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp}` + DOTALL body regex `<body[^>]*>.*?</body>` yields pairwise Jaccard<0.30 (max<0.30 or p95<0.30) with gap vs shuffled >=0.20;
- **(iii)** union of WebArena 812 families_ge3 (36) + synthetic 36 families via deterministic sampling plus deterministic `get_task_start_url __SHOPPING__` expansion yields >=10 distinct product families constructible under frozen protocol: product-subtree anchoring heading2 price6 add_to_cart2 main226-365 contentinfo31 node_count>1, distinct outerHTML SHA256 via page.evaluate after page.content()+Accessibility.getFullAXTree before==after TRUE and after DOM textContent mutation !=TRUE, at 1280x720 CDP Accessibility.getFullAXTree via cdp_session median AX>10 mean>15 std>5 DOM>=2000 on canonical 136/145/196/222 (12 captures) and on sampled families;
- **(iv)** full-tree multi-anchor AX_consistency vs truncated [:20] delta >=0.20 real vs shuffled<0.05 with family-level B=2000 variance>0 non-degenerate;
- **(v)** shared manifest JSON with trajectory-grouped family-level artifact (deterministic seeds S1/S2 per census, anchoring definition, manifest SHAs, family histograms, synthetic Jaccard matrix, constructibility S1/S2 SHA both directions, pip freeze + grammar hash + viewport) is published with path+sha256 in provenance.json and is consumable by Graph zero-overlap param pilot (N>=120) and Frontier heterogeneous BrowserGym reuse without downloading 567MB LFS;
- **(vi)** WebGym 292k/127k HF_TOKEN attempt is documented with >=2 genuine 300s attempts and smallest-next-action (scope/quota/mirror) if UNAVAILABLE.

If WebGym remains UNAVAILABLE after 2 genuine 401/404 attempts, the hypothesis is not falsified on diverse criteria but smallest next action must be documented — overall SURVIVES still requires durable+synthetic+>=10+shared-manifest+delta>=0.20.

---

## 4. Falsifier

**H falsified if** after **>=2 genuine attempts per durable source** (WebArena-Verified v2 812 via GitHub raw 200 byte-identical SHA `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` 927596 bytes + Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945...` Hub API 200 and/or GHCR BrowserGym 0.14.3 `ghcr.io/servicenow/browsergym:0.14.3` with 64-char digest, each `timeout>=300s`, URL/HTTP status/bytes/sha256 hex/64-char digest logged, `HF_TOKEN present true/false` logged, 401/404 captured, stderr/stdout in artifacts, WebGym UNAVAILABLE branch documents smallest next action: token scope/quota/mirror) any primary gate fails:

- **(A)** manifest SHA !=`d652756608...` or bytes !=927596 or Docker/GHCR digest 64-hex equality not proven and not documented as UNAVAILABLE with 2x attempts, or Hard258 258 not reproducible, or synthetic 192/36 not rebuilt with deterministic Random(35725763380) disjoint L=8-14 and pairwise Jaccard >=0.30 (max and p95 both >=0.30) or Jaccard gap vs shuffled <0.20, or union constructible product families <10 distinct with anchoring true + SHA both directions TRUE and CDP 1280x720 median AX>10 mean>15 std>5 DOM>=2000 fails on canonical 12 captures, or full-tree delta <0.20 real or shuffled >=0.05, or shared manifest not published with deterministic sampling + anchoring + SHA provenance + trajectory-grouped artifact consumable.

Single-module fail → **MIXED**, all fail → **FALSIFIED**, all pass → **SURVIVES**. No inference if `MEASUREMENT_INVALID` gating fails. WebGym 292k/127k diverse >=50 is UNAVAILABLE (not falsified) when HF_TOKEN absent after 2 genuine 401/404 attempts with smallest-next-action logged but overall H still requires durable+synthetic+>=10+delta>=0.20+shared-manifest to `SURVIVE`; vacuous `0.9479` alone does not satisfy diversity.

---

## 5. Baselines (stable IDs for EXECUTE/AUDIT reuse)

| ID | Type | Description | Expected |
|---|---|---|---|
| B-DURABLE-PIN-812 | durability | WebArena-Verified v2 812 tasks manifest SHA `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` 927596 bytes byte-identical x2 via GitHub raw 200 + Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945...` 64-char digest Hub API 200 + `docker pull --digests` or `docker load` fallback | SHA 64-hex equality, 927596 bytes, Docker digest 64-hex equality, families_ge3 >=30, container localhost:7770 HTTP 200 if pulled, median AX>10 mean>15 std>5 DOM>=2000 SHA both directions TRUE |
| B-HARD258-258 | durability | Hard258 subset 258 tasks reproducibly derived from 812 with documented filter and histogram preserved | 258 tasks, deterministic derivation from 812 SHA, histogram documented, no extra network fetch |
| B-GHCR-BROWSERGYM-0143 | durability | BrowserGym substrate pin: GHCR `ghcr.io/servicenow/browsergym:0.14.3` and/or Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945...` BrowserGym-core==0.14.3 AgentLab==0.4.2 Playwright==1.63.0 tldextract==5.3.2, >=2 genuine attempts logged | 64-char digest equality when both succeed; if one 403/404/denied after 2 attempts => UNAVAILABLE with attempts logged, not assumed equal; pip freeze sha nonempty, viewport 1280x720 |
| B-SYNTHETIC-192-36-JACCARD030 | dataset | Rebuilt synthetic diversity without LFS: 192 tasks / 36 families disjoint L=8-14 via deterministic random.Random(35725763380).sample TWICE S1==S2, product-subtree anchored, full-tree expanded stripping + DOTALL body regex | 192 tasks, 36 families_ge3 disjoint L=8-14, S1==S2, pairwise Jaccard max<0.30 or p95<0.30, gap vs shuffled >=0.20, manifest published with SHA |
| B-VACUOUS-SINGLE-STORE | null_baseline | Vacuous single-store duplication prevalence 0.9479 (prior 18/20 identical homepage/template Magento AX artifact) | Prevalence ~0.9479 on single-store slice; synthetic diverse Jaccard<0.30 and delta>=0.20 prove non-vacuous; degenerate CI [0,0]/[1,1] flagged not counted |
| B-EXHAUSTIVE-LFS-567M | cost_baseline | Exhaustive baseline to replace: 567MB LFS test.zip / CAP 420-task full enumeration (prior 27-streak repeated BLOCKED). Reference cost only | Not executed; reference wall 5-7h, 567MB, repeated BLOCKED; minimal manifest wall ~1.5-2.5h, <80MB, no LFS download |
| B-TRUNCATED-VS-FULLTREE | representation | Selectors/AX tokens [:20] truncated vs full-tree multi-anchor with expanded stripping. Delta = fulltree - truncated | Delta >=0.20 real vs <0.05 shuffled; validates that before==after SHA uses full body+expanded stripping not truncated 20-token proxy |

Per-census deterministic samples `S1/S2` and per-family anchoring json required for each census. Shared minimal manifest path+sha must be provenance-logged. All CIs family/trajectory-grouped unit=family/eTLD+1, never transition-level.

---

## 6. Controls

### Positive control — PC-MINIMAL-MANIFEST-DURABLE-SYNTHETIC

- **PC-A** Durable SHA fixture: WebArena manifest `d652756608...` 64-hex byte-identical x2 via 2 fresh GitHub raw 200 + Docker/GHCR digest 64-hex via Hub/GHCR API 200 verification; plus synthetic Flask product fixture at 1280x720 fixed DOM `heading+price+add-to-cart+main+contentinfo` localhost, AX tree ~17 nodes deterministic, pipeline must capture `median AX>10 mean>15 std>5 DOM>=2000` and `SHA before==after TRUE 12/12` plus `mutated textContent SHA !=TRUE 12/12` and 12 captures on canonical families 136/145/196/222 `median AX>=627 mean>15 DOM>=195052`. Also grammar hash live via `research/intel/grammar_fulltree_*.py` body regex DOTALL + expanded stripping `fotorama\d{6,}` — not hardcoded. GHCR/Docker UNAVAILABLE after 2x attempts is acceptable per MV1 but must be logged.
- **PC-B** Synthetic Jaccard sanity: rebuilt 192/36 disjoint L=8-14 yields pairwise Jaccard<0.30 max or p95 <0.30 with gap vs shuffled >=0.20 and delta fulltree-vs-truncated >=0.20 non-degenerate.
- **PC-C** Shared manifest + trajectory grouping: shared manifest JSON at `research/experiments/EXP-INTEL-36092351694/artifacts/derived/shared_minimal_manifest.json` containing deterministic Random(35725763380) S1/S2 per census (WebArena + synthetic), product-subtree anchoring definition, manifest SHAs (WebArena d6527566 927596 bytes + synthetic SHA + WebGym null UNAVAILABLE with smallest-next-action), family histograms, Jaccard matrix + shuffled baseline, constructibility per-family anchoring S1/S2 SHA both directions (AX median>10 mean>15 std>5 DOM>=2000) with trajectory-grouped family-level grouping documented, pip freeze + grammar hash + viewport versions; path+sha256 stored in provenance.json and freeze.json.

*Expected:* PC-A `median AX>10 mean>15 std>5 DOM>=2000 SHA both directions TRUE median AX>=627` and GHCR/Docker digest 64-hex or UNAVAILABLE with 2x logs; PC-B Jaccard max<0.30 or p95<0.30 gap>=0.20 delta>=0.20; PC-C shared manifest published trajectory-grouped consumable. Fail on any `TRUE` gate is control failure, not `UNAVAILABLE`.

### Null controls — NC-SHUFFLED-SINGLESTORE-TRUNCATED (all family/trajectory-level)

- **NC1** Family-label shuffle for synthetic Jaccard and AX_consistency (`B=1000` perms family-label shuffle): `|rho_shuffled|<0.20`, shuffle Jaccard mean ~chance, `gap = real - shuffle >=0.20`, shuffled AX mean `<<0.6 p>0.05`.
- **NC2** Vacuous single-store: duplication prevalence on single-store slice remains `~0.9479` even after synthetic rebuild; diverse Jaccard<0.30 proves diversity not vacuous. Prior 18/20 identical rejected as non-diverse baseline.
- **NC3** Truncated `[:20]` vs full-tree: `delta_vs_truncated = fulltree - truncated` `>=0.20` real must hold; shuffled variant `<0.05`; degenerate CIs `[0,0]` or `[1,1]` variance 0 flagged per prior prereg not counted as width; product-subtree Jaccard shuffle control expects |Jaccard_shuffled - chance| <0.10.

*Expected:* NC1 `|rho|<0.20 p>0.05 gap>=0.20`, NC2 vacuous `0.9479` preserved and beaten by synthetic Jaccard<0.30 delta>=0.20, NC3 `delta<0.05 shuffled`, no degenerate CI counted as high-precision. All CIs trajectory-grouped family-level, not transition-level. When HF_TOKEN UNAVAILABLE, NC1/NC2 on WebGym diverse slice are UNAVAILABLE with next action, not failed; synthetic nulls remain required.

All CIs trajectory-grouped family-level bootstrap 95% percentile where applicable. Degenerate `[0,0]` or `[1,1]` variance 0 flagged not counted as width. Integer sum counters with |rho_shuffled|<0.20 via block-permutation required for honest cost metrics per director prior.

---

## 7. Measurement validity (gating, frozen)

1. **MV1_DURABLE_ATTEMPTS:** Each durable source (GitHub raw for WebArena 812 + Hard258 derived, GHCR BrowserGym 0.14.3 `ghcr.io/servicenow/browsergym:0.14.3`, Docker Hub `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945...`) requires **>=2 genuine attempts** logged with URL/HTTP status/returncode, bytes, sha256 hex (64 hex), 64-char Docker digest substring check, `timeout>=300s` or `docker load` fallback captured (`docker pull ... --digests` or `docker load < tar, docker images --digests`), stderr/stdout. Single-attempt success → `MEASUREMENT_INVALID`. `HF_TOKEN present true/false` separately logged for WebGym 292k/127k with >=2 attempts 300s each; when `UNAVAILABLE` after 2 genuine 401/404, document smallest next action: token scope/quota/mirror. Evidence: `artifacts/raw/github_cross_source_attempts.json`, `artifacts/raw/ghcr_browsergym_attempts.json`, `artifacts/raw/docker_hub_api_attempts.json`, `artifacts/raw/hf_webgym_manifest_attempts.json`, `provenance.json` hashes.

2. **MV2_BYTE_IDENTITY:** Manifest SHA exactly `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (927596 bytes, 64 hex) equality stored via 2 independent fresh GitHub raw fetches 200 (byte-identical x2); GHCR BrowserGym image digest 64-char hex equality with GHCR API 200 when GHCR succeeds; Docker digest exactly `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` (64 hex after colon) Hub API 200. If one source succeeds, single sha256 pinned file + log suffices but cross-source equality explicitly `UNAVAILABLE` not assumed equal. WebGym 292k/127k SHA separately 64-hex logged when `HF_TOKEN` succeeds via 2 fetches, else UNAVAILABLE with attempts logged. Reuse prior pinned file allowed only with `+2` fresh verification attempts logged this experiment with cognitive_reset true.

3. **MV3_SYNTHETIC_192_36_JACCARD030:** Rebuilt synthetic census must be deterministically rebuilt without LFS: 192 tasks / 36 families disjoint L=8-14 via deterministic `random.Random(35725763380).sample(sorted synthetic_families_ge3,10)` executed TWICE S1==S2 logged plus documentation of disjoint construction. Pairwise Jaccard of product-subtree token sets (full-tree multi-anchor, expanded stripping + DOTALL body regex) across synthetic families must be <0.30 for max or p95 documented with Jaccard matrix logged in synthetic_census.json. Shuffled Jaccard baseline (1000 family-label perms) logged with gap >=0.20 vs real. Evidence: `artifacts/derived/synthetic_192_36_census.json`.

4. **MV4_CONSTRUCTIBILITY_10FAM:** Deterministic constructibility executed exactly on **BOTH** WebArena 812 census and synthetic 192/36 census: sorted `families_ge3` from census json, two independent draws `Random(35725763380).sample(sorted_families_ge3,10)` with seed reset `S1` and `S2` logged on **EACH** census (`S1==S2` expected but both logged). Each sampled family probed via `get_task_start_url __SHOPPING__` expansion + product-subtree anchoring `heading/price/add-to-cart/main/contentinfo node_count>1` distinct SHA256 with body regex `<body[^>]*>.*?</body>` DOTALL + 9 base + expanded `{form_key,uenc,store,session,nonce,fotorama\d{6,},timestamp}` stripping before SHA via `page.evaluate` recomputed after `page.content()+Accessibility.getFullAXTree`, **SHA before==after TRUE and after mutation !=TRUE**. Viewport strictly `1280x720`, **CDP `Accessibility.getFullAXTree` via `cdp_session` required** (fallback `accessibility.snapshot` → `MEASUREMENT_INVALID` for this gate). Metrics `median AX>10 mean>15 std>5 median DOM>=2000` on canonical 136/145/196/222 (12 captures) and on union achieving >=10. Without `BOTH` samples logged per census → `MEASUREMENT_INVALID` for that clause. BrowserGym-core==0.14.3 AgentLab==0.4.2 Playwright==1.63.0 `pip freeze sha256` nonempty; cognitive_reset true requires fresh captures.

5. **MV5_AX_LIVENESS_AND_SHA_STABILITY:** Canonical product families 136/145/196/222 probed at 1280x720 CDP via cdp_session: 12 captures must show median AX>10 mean>15 std>5 DOM>=2000 and SHA before==after TRUE 12/12 and mutated textContent !=TRUE 12/12. Synthetic sampled families also probed with same gates. Body regex DOTALL + 9 base + expanded stripping via page.evaluate present with grammar hash live. Without fresh CDP captures or stripping regex absent => MEASUREMENT_INVALID for liveness gate.

6. **MV6_WEBGYM_SMALLEST_NEXT_ACTION:** WebGym 292k/127k HF_TOKEN attempt must be logged with >=2 genuine 300s attempts (`hf_webgym_manifest_attempts.json`) and HF_TOKEN present true/false. If UNAVAILABLE (401/404) after 2 genuine attempts, document smallest-next-action exactly: scope/quota/mirror per director mandate. This branch is UNAVAILABLE not falsified when attempts genuine; missing smallest-next-action or <2 attempts => MEASUREMENT_INVALID for this module. No exhaustive 567MB LFS enumeration required.

7. **MV7_SHARED_MANIFEST_AND_DELTA:** Shared manifest publication plus representation non-vacuity: (a) publish shared manifest JSON at `research/experiments/EXP-INTEL-36092351694/artifacts/derived/shared_minimal_manifest.json` containing: deterministic sampling seed 35725763380 S1/S2 per census (WebArena + synthetic), product-subtree anchoring definition (1280x720 CDP, heading/price/add-to-cart/main/contentinfo node_count>1, DOTALL body regex + 9 base + expanded stripping), manifest SHAs (WebArena d6527566 927596 bytes + synthetic SHA + WebGym null UNAVAILABLE with smallest-next-action), family histograms, synthetic Jaccard<0.30 matrix + shuffled baseline gap>=0.20, constructibility per-family anchoring S1/S2 with SHA both directions (AX median>10 mean>15 std>5 DOM>=2000), trajectory-grouped artifact metadata (family-level grouping, B=2000 CI where applicable but not degenerate), pip freeze + grammar hash + viewport versions, and WebGym smallest-next-action; path+sha256 stored in provenance.json and freeze.json. (b) Full-tree multi-anchor AX_consistency vs truncated [:20] delta >=0.20 real vs shuffled <0.05 with family-level B=2000 variance>0 non-degenerate, delta table logged, degenerate CIs flagged. Missing shared manifest or delta table or trajectory-grouping doc => MEASUREMENT_INVALID for that module.

8. **MV8_PROVENANCE:** Every artifact `path+sha256` stored in `provenance.json` and `freeze.json`: `request/spec/prereg/freeze` hashes, `pip freeze` hash nonempty, `docker images --digests` hash, GHCR/Docker Hub attempts, HF manifest attempts with smallest-next-action, WebArena census summary, Hard258 histogram, synthetic_192_36_census.json, per-family anchoring json S1/S2 per census, AX probe logs with `grammar_fulltree` hash live, delta table, shared minimal manifest path+sha, command logs. Missing provenance for any durability/synthetic/constructibility/Jaccard/shared-manifest path → `MEASUREMENT_INVALID` for that module.

---

## 8. Decision rule (frozen three-way, after MEASUREMENT_INVALID check)

**(A) MEASUREMENT_INVALID** if any mandatory `MV1-MV2`/`MV4-MV5`/`MV7-MV8` gating fails: `<2` genuine attempts per required durable source (GitHub WebArena 812, GHCR, Docker Hub), missing 64-char digest or manifest SHA `d652756608...` 927596 bytes, `pip freeze` empty or version/viewport mismatch (`BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 1280x720`), fallback AX snapshot used instead of CDP Accessibility.getFullAXTree, body regex absent, deterministic sampling not executed exactly TWICE S1==S2 on BOTH WebArena and synthetic censuses, synthetic Jaccard matrix not logged with shuffled baseline, shared manifest not published with deterministic sampling + anchoring + SHA provenance + trajectory-grouped artifact + delta table, or provenance missing, or WebGym UNAVAILABLE without smallest next action documented. `MV3` synthetic Jaccard<0.30 alone failing does NOT trigger INVALID but feeds (C). `MV6` WebGym UNAVAILABLE alone does **not** trigger `INVALID` when 2 genuine 401/404 attempts with smallest-next-action logged (marked `UNAVAILABLE` not failed).

**(B) SURVIVES_CURRENT_TEST** iff `A` passes **AND** all H gates pass: `(SRC_GHCR_SUCCESS OR SRC_DOCKER_SUCCESS)` with byte-identical WebArena SHA and Hard258 258 reproducible + synthetic 192/36 Jaccard max<0.30 or p95<0.30 with gap>=0.20 vs shuffled + union constructible >=10 distinct product families anchoring true SHA both directions TRUE at 1280x720 CDP median AX>10 mean>15 std>5 DOM>=2000 on canonical 136/145/196/222 plus sampled synthetic families + full-tree delta>=0.20 vs truncated shuffled<0.05 + shared minimal manifest published trajectory-grouped consumable. All metrics recomputed with trajectory-grouped family-level reporting; cognitive_reset true requires fresh execution.

**(C) Otherwise** if `A` passes but not all `B`: **FALSIFIED** if union still `<=4` families (bounded ceiling on attempted censuses) and synthetic Jaccard>=0.30 or delta<0.20 persisting; **MIXED** if any module passes (e.g., durable+synthetic Jaccard<0.30 passes but constructibility 4/10, or durable+constructibility >=10 but Jaccard>=0.30). Audit may bound ceiling narrower than `SURVIVES`. WebGym UNAVAILABLE does not prevent SURVIVES when durable+synthetic gates pass. Vs exhaustive 567MB LFS, MIXED still not replacement without >=10 families.

All metrics recomputed with trajectory-grouped family-level reporting; transition-grouped treated as `MEASUREMENT_INVALID` per prior audits. Mean>15 std>5 computed from fresh CDP captures at 1280x720, not from prior captures. Integer sum counters with block-permutation |rho_shuffled|<0.20 required for honest cost per director prior.

---

## 9. Metrics and control identities (stable for downstream)

**Primary metrics:**

- `M_MANIFEST_SHA_WEBARA` — `d652756608...` byte-identity (bool)
- `M_MANIFEST_BYTES_WEBARA` — 927596 bytes (int)
- `M_MANIFEST_SHA_WEBGYM` — WebGym 64-hex logged or null UNAVAILABLE (bool/null)
- `M_HF_TOKEN_PROVISIONED` — HF_TOKEN present true/false plus smallest next action when false (scope/quota/mirror)
- `M_HARD258_COUNT` — 258 tasks derived (int, gate 258)
- `M_SYNTHETIC_TASK_COUNT` — 192 tasks rebuilt (int, gate 192)
- `M_SYNTHETIC_FAMILIES_GE3` — 36 synthetic families_ge3 (int, gate 36)
- `M_SYNTHETIC_JACCARD_MAX` — max pairwise Jaccard product-subtree (gate <0.30)
- `M_SYNTHETIC_JACCARD_P95` — 95th percentile pairwise Jaccard (gate <0.30 if max documented)
- `M_SYNTHETIC_JACCARD_GAP_VS_SHUFFLED` — real - shuffled gap (gate >=0.20)
- `M_DELTA_FULLTREE_VS_TRUNCATED` — `fulltree - truncated[:20]` (gate >=0.20 real, <0.05 shuffled)
- `M_CONSTRUCTIBLE_FAMILIES` — distinct union product families anchoring true + SHA both directions TRUE (gate >=10)
- `M_CONSTRUCTIBLE_FAMILIES_WEBARA_ONLY` — WebArena 812 alone diagnostic (expected 4)
- `M_CONSTRUCTIBLE_FAMILIES_SYNTHETIC_ONLY` — synthetic 192/36 alone diagnostic
- `M_AX_MEDIAN` / `M_AX_MEAN` / `M_AX_STD` / `M_DOM_MEDIAN` — median AX, mean AX, std AX, median DOM (gates >10 / >15 / >5 / >=2000)
- `M_SHA_STABILITY_TRUE` — `before==after TRUE` 12/12
- `M_SHA_MUTATION_SENSITIVITY` — `after mutation !=TRUE` 12/12
- `M_AX_VALID_CAPTURES` / `M_AX_PRODUCT_FAMILY_COUNT` — AX liveness gates (median>10 mean>15 std>5, >=10 families)
- `M_RHO_SHUFFLED` — `|rho_shuffled|` family-level (gate <0.20)
- `M_SHARED_MANIFEST_PUBLISHED` — shared minimal manifest path+sha256 provenance bool (gate true)
- `M_TRAJECTORY_GROUPED_ARTIFACT` — artifact family/trajectory-grouped metadata bool (gate true)

Controls and baselines keyed by IDs in §5-6 preserved in `result.json:controls` exactly. Jaccard matrix, shuffled baseline, sweep table reference vs vacuous 0.9479, and delta vs truncated logged as derived artifacts. All AX stats recomputed fresh with cognitive_reset true.

---

## 10. Product consequences

**If SURVIVES:** Intel delivers Codex-accepted minimal viable shared manifest without 567MB LFS: pinned WebArena SHA `d6527566` 927596 bytes + Hard258 258 + GHCR 0.14.3 / Docker `3e8cb9b9...` 64-hex (or documented UNAVAILABLE) + rebuilt synthetic 192/36 Jaccard<0.30 disjoint L=8-14 deterministic S1==S2 + >=10 constructible product families under frozen SHA-anchoring at 1280x720 CDP median>10 mean>15 std>5 DOM>=2000 SHA both directions + full-tree delta>=0.20 vs truncated + **shared minimal manifest published trajectory-grouped** for heterogeneous reuse, **replacing exhaustive 567MB LFS/CAP 420 enumeration**. This unblocks Graph single-family zero-template-overlap param-inherit gate (N>=120 hold-out without re-probing liveness) and Physics website-holdout banks (true family-level hold-out with Jaccard orthogonality) and Frontier heterogeneous BrowserGym reuse including O(1) compilation baselines, without further exhaustive fetches; satisfies `C-MEAS-VALID` single-node health gate before distributed `n>=800`. `C-CROSSSITE` advances from `HYPOTHESIS` toward `EXPERIMENTAL` at synthetic orthogonal + parameterization + >=10 constructibility ceiling; WebGym smallest-next-action documented.

**If FALSIFIED:** Deterministically proven that even minimal viable manifest pivot (durable 812+Hard258+GHCR/Docker + synthetic 192/36) still yields <10 constructible product families with anchoring+SHA stability, or synthetic Jaccard>=0.30 not orthogonal (gap<0.20) or delta<0.20 or shared manifest not publishable trajectory-grouped, so Graph >=10-family hold-out remains **BLOCKED** on these censuses and Physics/Frontier banks remain unmet; minimal manifest does **NOT** replace exhaustive 567MB LFS without orthogonal eTLD+1 hosting. Requires next **orthogonal** census via independent `eTLD+1` hosting beyond current synthetic+Magento slice (new family sampling with independent hosting) or definition expansion beyond `shopping` vs `shopping_admin`, and must **not** re-attempt exhaustive `567MB LFS` or `N=20 longest-prefix` on same 4-family slug-URL substrate (expected `MEASUREMENT_INVALID`). If synthetic Jaccard passes but constructibility 4/10, result is **MIXED** — downstream lanes can reuse synthetic orthogonality but not >=10-family hold-out. If WebGym UNAVAILABLE with smallest-next-action logged, `HF_TOKEN` provisioning or alternative WebGym hosting (scope/quota/mirror) is smallest repair, not another LFS enumeration. `C-CROSSSITE` stays `HYPOTHESIS` at 4-family ceiling; non-degenerate trajectory-grouped CI and delta gates prevent promoting degenerate [0,0]/[1,1] artifacts.

**If MIXED:** One module passes while other fails — e.g., durable+synthetic Jaccard<0.30 passes but constructibility 4/10, or durable+constructibility >=10 but Jaccard>=0.30, or WebGym UNAVAILABLE with documented next action but synthetic gaps. Decision documents which blocking artifact remains and which downstream lane is unblocked. Same smallest next action rule applies.

**If MEASUREMENT_INVALID:** No claim update; smallest repair per `MV1-MV8` (genuine attempts `>=2`, versions `0.14.3`, CDP full-tree, deterministic samples on BOTH censuses, `B=2000` trajectory-grouped where applicable, synthetic Jaccard<0.30 matrix + shuffled baseline, AX_consistency multi-anchor, expanded stripping, `AX>10 mean>15 std>5`, shared manifest publication trajectory-grouped, HF_TOKEN next action when UNAVAILABLE) and re-run identical frozen design with cognitive_reset true.

---

## 11. Validity threats and mitigations

- **Single-node vs distributed gap:** Factory tunneled on `MEASUREMENT_INVALID` via AX substrate and WebGym diverse fetch. Runtime single-node health-gated harness (`BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 1280x720 CDP`) is explicit dependency; all Gates require `median AX>10 mean>15 std>5` before distributed `n>=800` promotion. This experiment runs **single-node only**, documenting that ceiling, not claiming distributed. Cognitive_reset true requires fresh CDP captures.
- **Template overlap independence threat:** Hard258 derived from same Magento base as 812 — not fully independent. This design tests a **genuinely orthogonal** synthetic census via deterministically rebuilt 192/36 disjoint `L=8-14` product-subtree-anchored families with `Jaccard<0.30` orthogonality + `delta>=0.20` + `gap>=0.20` vs shuffled; if union `<10`, result is **bounded FALSIFIED** not global rejection — orthogonal independent eTLD+1 hosting remains next step per `do_not_assume` (previously bounded `0` WebMall/Mind2Web after `401/404`, not global impossibility). Do not claim cross-site transfer without website holdout.
- **Path dependence / salience bias:** Director prior requires per-trajectory hard-reset integer sum counters with `|rho_shuffled|<0.20` block-permutation; jitter/n*3200 bijective proxies bake in null and cause degenerate CIs. This PIVOT uses rebuilt synthetic families with trajectory-grouped artifact (family-level grouping) and block-permutation shuffled baseline for Jaccard/delta, avoiding prior degenerate CI failure mode (~80% of recent MEASUREMENT_INVALID).
- **Verification cheap prior:** `AX subtree SHA after dynamic-token stripping` is cheap deterministic contract vs LLM-as-judge (~68% agreement cannot calibrate false_accept/ECE). SHA before==after TRUE and mutation !=TRUE are required per family, not LLM judge.
- **Synthetic-to-real gap:** 192/36 synthetic families are intentionally disjoint and orthogonal by construction (L=8-14, Jaccard<0.30) to prove non-vacuous diversity without WebGym 292k; they do not prove real eTLD+1 diversity. Claim ceiling is bounded to synthetic orthogonality + durable 812 pin at single-node CDP; WebGym real diversity remains UNKNOWN until HF_TOKEN provisioned with smallest-next-action resolved. Do not promote synthetic diversity as real site holdout beyond this bounded ceiling.
- **GHCR/Docker availability:** GHCR BrowserGym 0.14.3 has failed with 403/404/denied on 5 attempts in prior MIXED runs; this PIVOT requires 2x attempts and explicitly marks cross-source equality UNAVAILABLE when one source fails, not assumed equal. Docker single-source durable suffices for SURVIVES if 2x fresh verification passes; exhaustive cross-source byte-identity is not required to block minimal manifest.
- **HF_TOKEN exhaustion:** WebGym 292k/127k has failed 6x401 on 300s attempts; this PIVOT does **not** require 292k >=50 for SURVIVES and mandates smallest-next-action (scope/quota/mirror) documentation when UNAVAILABLE, preventing burn of cycles on LFS enumeration per comparative_reasoning. Graph N>=120 and Frontier heterogeneous reuse can proceed on synthetic+812 without waiting for HF_TOKEN.
- **Degenerate CI / truncation proxy:** Prior delta inverted -0.420 (truncated 0.875 > fulltree 0.454) proves not vacuous proxy but fails frozen representation superiority gate. This PIVOT retains delta>=0.20 vs shuffled<0.05 with family-level B=2000 variance>0 non-degenerate and flags degenerate [0,0]/[1,1] variance 0, preventing prior measurement invalidity. Full-tree expanded stripping + DOTALL regex validated by SHA both-directions TRUE.
- **Cognitive reset:** `cognitive_reset true` per director mandate requires fresh deterministic sampling Random(35725763380) S1==S2 logged on EACH census (WebArena + synthetic) and fresh 1280x720 CDP captures and +2 fresh GitHub verification attempts, not reuse of prior 401 logs or prior 12 captures alone. Chain_depth 0 indicates fresh pivot.

---

## 12. Execution checklist (for EXECUTE, not DESIGN measurements)

- [ ] Provision environment: BrowserGym-core==0.14.3 AgentLab==0.4.2 Playwright==1.63.0 tldextract==5.3.2 pip freeze nonempty
- [ ] Log >=2 genuine attempts per durable source: GitHub raw WebArena 812 2x byte-identical SHA d6527566... 927596 bytes, GHCR BrowserGym 0.14.3, Docker Hub am1n3e/webarena-verified-shopping@sha256:3e8cb9b945..., HF WebGym 292k/127k 2x 300s with HF_TOKEN present true/false + smallest-next-action scope/quota/mirror
- [ ] Verify byte-identity: 2 fresh GitHub raw 200 + Docker/GHCR 64-hex digest substring
- [ ] Census demographics: WebArena 812 + Hard258 258 histograms preserved; synthetic 192/36 rebuilt disjoint L=8-14 deterministic sample
- [ ] Deterministic sampling: Random(35725763380).sample(sorted families_ge3,10) TWICE S1==S2 on BOTH WebArena and synthetic censuses
- [ ] Product-subtree anchoring + get_task_start_url __SHOPPING__ expansion + DOTALL body regex + 9 base + expanded stripping via page.evaluate, SHA before==after TRUE 12/12 and mutation !=TRUE 12/12
- [ ] CDP Accessibility.getFullAXTree via cdp_session at 1280x720 median AX>10 mean>15 std>5 DOM>=2000 on canonical 136/145/196/222 (12 captures) + synthetic sampled families
- [ ] Synthetic Jaccard<0.30 pairwise matrix + shuffled gap >=0.20 + full-tree delta >=0.20 vs truncated shuffled<0.05 family-level B=2000
- [ ] Publish shared minimal manifest at artifacts/derived/shared_minimal_manifest.json trajectory-grouped with deterministic seeds, anchoring definition, manifest SHAs, family histograms, Jaccard matrix, constructibility S1/S2 SHA both directions, pip freeze + grammar hash + viewport, WebGym smallest-next-action
- [ ] Store provenance: all paths+sha256 in provenance.json and freeze.json including pip freeze, grammar, delta table, attempt logs

---

*No outcome-bearing measurements were inspected during DESIGN. All gates are frozen before EXECUTE.*
