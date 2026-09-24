# Preregistration — EXP-INTEL-36020904615

**Lane:** intel — Find, reproduce and stress-test datasets, baselines and prior art only when they can alter a live SPIDER claim
**Experiment ID:** EXP-INTEL-36020904615
**Claim IDs:** C-CROSSSITE (primary), C-PRODUCT-ECON, C-RESIDUAL-NOVELTY
**Request ID:** e71a5aa98f8db354c2b167b9  •  **Request hash:** fc51c42ba38b536fa37fb0b44f0c01e793cab4bb2737f6a79878ea3f45c1bd44
**Director mandate:** PIVOT • **Parent handoff disposition:** SUPERSEDE (carry_forward from EXP-INTEL-36006513166 preserved as continuity evidence only)
**Freeze status:** DESIGN — no outcome-bearing measurements inspected. Spec and prereg frozen before EXECUTE.

---

## 1. Strategic question (Director binding)

> Can Intel deliver (a) a durable census without exhaustive 567MB LFS: Hard258 + WebArena-Verified v2 812 via pinned GHCR ghcr.io/servicenow/browsergym:0.14.3 and am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (64-char hash, byte-identical manifest SHA d6527566) proving ≥10 constructible families (deterministic random.Random(35725763380).sample, get_task_start_url expansion, product-subtree distinct SHA on path families 136/145/196/222 at 1280x720 CDP AX>10) and WebGym 292k 127k sites ≥50 diverse eTLD+1 duplication 95% CI via threshold sweep 0.818–0.9479 (2000 family bootstrap, HF_TOKEN) replacing exhaustive test.zip, plus (b) blind external baseline reproductions on SPIDER synthetic 40-task alias-OOD (30 orthogonal+10 mixed): Agentic Compilation DSM 99% TreeWalker+JSON IR $0.002–0.092, Stagehand selector+relevant-subtree SHA256 HIT/MISS ≥0.8 after expanded stripping {form_key,uenc,store,session,nonce}, and browser-memory catalog deterministic replay — with trajectory-grouped bootstrap coverage/CIs, honest M_total_f10 Pareto vs SPIDER catalog/routing/WebMCP, as the unblocking deliverable for Graph/Physics/Product?

This converts to the smallest rigorous falsifiable test below. We do **not** re-probe the same 812-task primary pin alone (already bounded to 4 families) nor exhaustively download 567MB LFS test.zip; instead we test escape from the 4-family ceiling via Hard258 union and replace exhaustive LFS with threshold-sweep CI.

---

## 2. Inherited state (parent handoff EXP-INTEL-36006513166 — audit PASS, producer_claim_supported=false)

**Established (preserved):**
- Durable single-source pin: manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 927596 bytes pinned, Docker digest sha256:3e8cb9b9... digest_valid true, container HTTP 200.
- Deterministic protocol exact: random.Random(35725763380).sample(sorted families_ge3,10) x2 S1==S2 logged [191,180,162,197,153,213,163,137,136,222] primary 36 etc., canonical families 136/145/196/222 median AX 633.5 DOM 197353.5 anchoring true.
- Full-tree multi-anchor AX_consistency pipeline validated on 4-family substrate: mean 0.6208 CI[0.5514,0.6902] lower>0.5 shuffle p0.0 gap0.242 delta_vs_truncated 0.5871, median AX>10 CDP 1280x720 BrowserGym-core 0.14.3.
- Blind SOTA on 40-task alias-OOD: DSM 0.75 [0.625,0.875], HITL drop 0.50, honest M_total_f10 DSM22.6 vs ALIAS30.1 vs WebMCP28, |rho|0.1592<0.20.

**Rejected (bounded, do not re-attempt without orthogonal source):**
- H_A ≥10 families from pinned 812-task census alone — rejected to 4 families [136,145,196,222] deterministically.
- shopping_admin 184-task filtered fallback as independent census — rejected (filtered primary, 0 product_page families).
- Re-running same 812 pin to reach ≥10 — deterministically impossible, would be MEASUREMENT_INVALID.
- Degenerate CIs [0,0] BMEM and [1,1] ROUTING/WebMCP, homepage-only [:20] truncated AX_consistency — rejected as invalid width.

**Unknown (this experiment targets):**
- Cross-source byte-identity Docker vs HF — requires HF_TOKEN (2x401 previously UNAVAILABLE).
- WebGym 292k diverse 127k-site ≥50 eTLD+1 duplication CI and sweep 0.818–0.9479 — UNAVAILABLE pending HF_TOKEN (not failed).
- Whether orthogonal census (Hard258, WebMall/Mind2Web-2 loopback, WebGym-derived) contains ≥10 product_page families under identical protocol at 1280x720 CDP.
- Real WebArena hold-out transfer and real-cost Pareto vs O(1) ceiling.
- Product-subtree AX_consistency beyond 4 families.

**Do-not-assume (preserved):**
- Do not assume ≥10-family constructibility from 812 pin or filtered shopping_admin.
- Do not assume cross-source byte-identity (HF 401 prevents verification).
- Do not treat degenerate CIs or homepage truncation as high-precision.
- Do not equate synthetic M_total work units with USD/wall-clock or browser steps.
- Do not assume shopping_admin fallback independence (template overlap).
- Do not assume runtime harness availability — explicitly depend on runtime:C-MEAS-VALID single-node health-gated harness (dependency declared in director mandate).

**Director supersede note:** Parent handoff's `next_question` (orthogonal census WebMall/Mind2Web-2 loopback 130-task, Mind2Web definition expansion shopping vs shopping_admin 404, or WebGym-derived families) is advisory. Director mandate PIVOT+SUPERSEDE replaces it with the Hard258+GHCR+Stagehand scope above. DESIGN refines the Director question into a rigorous test but does not drift back to the parent's shopping_admin-only continuation.

---

## 3. Hypotheses

### H_A_DURABLE_CENSUS_HARD258_V3
A byte-identical durable pin verified as manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (927596 bytes) with GHCR image ghcr.io/servicenow/browsergym:0.14.3 pinned digest and Docker digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (64 hex) via ≥2 genuine attempts per source (HF_TOKEN bearer Authorization: Bearer, Hub/GHCR API 200, docker pull --digests / docker load fallback, timeout ≥300s) yields verifiable census: WebArena-Verified v2 812 tasks (700–812 total, families_ge3 ≥30) plus Hard258 hard slice (≥200 hard tasks, documented hardness/product_page filter) and with deterministic random.Random(35725763380).sample(sorted families_ge3,10) executed TWICE with get_task_start_url __SHOPPING__ expansion and product-subtree anchoring (heading/price/add-to-cart/main/contentinfo node_count>1, distinct outerHTML SHA256 before==after identical TRUE and after mutation != TRUE on canonical path families 136/145/196/222 at 1280x720 CDP Accessibility.getFullAXTree median AX>10 median DOM≥2000 proven) proves ≥10 distinct product families constructible (union of Hard258 and primary 812, counted as distinct families with anchoring true and SHA stability both directions TRUE), achieving full-tree multi-anchor AX_consistency mean≥0.6 bootstrap 95% percentile CI lower>0.5 (trajectory-grouped family-level B=2000) gap≥0.20 vs shuffle p<0.05 variance>0 delta_vs_truncated≥0.20 on the ≥10 family set, plus WebGym 292k/127k sites diverse sample ≥50 distinct eTLD+1 with family-level B=2000 duplication prevalence CI non-degenerate and threshold sweep 0.818–0.9479 range≥0.05 monotonic, replacing exhaustive 567MB LFS.

### H_B_SOTA_CEILING_HONEST_PARETO_V3
On SPIDER deterministic synthetic 40-task alias-OOD (research/intel/synthetic_alias_ood_40.json seed 360360, generator sha 5311a581, 10 header-param +10 body-param +10 auth-param orthogonal +10 mixed header+body+auth triple-channel, per-task channel orthogonality verified no cross-channel leakage) blind reproduction per published recipe of B-AGENTIC-DSM (DSM 99% TreeWalker + deterministic JSON IR + HITL patch $0.002–0.092 per task, 80–94% compile ceiling), B-STAGEHAND (selector + relevant-subtree SHA256 HIT/MISS with expanded stripping {form_key,uenc,store,session,nonce} achieving ≥0.8 after vs <0.4 before) and B-BMEM-CATALOG (browser-memory catalog deterministic replay, expected 0.0 collapse) plus SPIDER internal baselines B-SPIDER-ALIAS/B-ROUTING/B-WEBMCP, all executed blind without tuning to split labels with per-task logs, yields interior non-degenerate trajectory-grouped bootstrap CIs for coverage (width>0, variance>0 when not structurally degenerate) and honest per-trajectory-reset sum-counter M_total_f10/f100 Pareto (DSM F10 ~22.6 USD $0.035/task vs ALIAS F10 ~30.1 vs WebMCP amortized F10 2.9/F100 0.725) distinguishing DSM structured collapse on mixed/auth (0.3) vs single-channel (0.9–1.0) and Stagehand stripping lift ≥0.40, with |rho_shuffled|<0.20 and HITL drop≥0.30.

---

## 4. Falsifier

**H_A falsified if** after ≥2 genuine attempts per durable source (HF for WebArena 812+Hard258+WebGym 292k, GHCR for BrowserGym 0.14.3, Docker Hub for webarena-verified-shopping, each timeout≥300s, docker load/ghcr mirror fallback, HF_TOKEN true/false logged, Hub/GHCR digest 200 verification) no byte-identical manifest SHA d6527566 with 64-char digest sha256:3e8cb9b9... is produced with pinned census artifacts (primary 700–812, Hard258 ≥200, families_ge3 ≥30), OR deterministic Random(35725763380).sample x2 + anchoring fails to reach ≥10 distinct families with SHA stability both directions TRUE and CDP 1280x720 median AX>10 on canonical 136/145/196/222 on both primary and Hard258 union (if union <10, bounded FALSIFIED to 4 families remains), OR full-tree AX_consistency mean<0.6 or CI lower≤0.5 or shuffle p≥0.05 or gap<0.20 or variance==0 or delta_vs_truncated<0.20 (degenerate [:20] truncation or incomplete stripping rejected), OR WebGym diverse <50 or B=2000 CI not computed non-degenerate or sweep 0.818–0.9479 range<0.05 when HF_TOKEN succeeds.

**H_B falsified if** external baselines cannot be executed blind with per-task logs producing trajectory-grouped CIs and honest M_total_f10/f100 (when variance>0 width>0; degenerate BMEM [0,0] and ROUTING/WebMCP [1,1] flagged not counted as valid), OR DSM/Stagehand indistinguishable from null controls (coverage within null permutation 95% CI, |rho|≥0.20, HITL drop<0.30, Stagehand lift <0.20, delta_vs_truncated<0.20), OR Stagehand HIT after expanded stripping <0.8 and not significantly above pre-stripping, OR DSM does not show structured per-channel collapse (mixed 0.3 vs single-channel 0.9–1.0) distinguishing it from flat ALIAS p>0.05, OR honest Pareto not measurable (proxy n*3200 detected).

Single-module falsification → overall MIXED; both fail → FALSIFIED; both pass → SURVIVES. No silent drift from Director's target.

---

## 5. Baselines (stable IDs for EXECUTE/AUDIT reuse)

| ID | Type | Description | Expected |
|---|---|---|---|
| B-GHCR-BROWSERGYM-0.14.3 | durability | GHCR ghcr.io/servicenow/browsergym:0.14.3 pinned digest via GHCR API 200, docker pull --digests or docker load cached tar; BrowserGym-core 0.14.3 pip-show verified | 64-char digest verified + local docker images --digests + pip freeze 0.14.3 |
| B-WEBARENA-SHOPPING-DOCKER | durability | Docker Hub am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb, Hub API 200, docker pull --digests or load fallback, curl localhost:7770 3 retries | 64-char digest equality + reachable 200 |
| B-HARD258-CENSUS | dataset | Hard258 hard-filtered subset (hard difficulty + product_page) ≥200 tasks, documented filter provenance, derived from base SHA d6527566, probed with identical Random(35725763380).sample x2 + anchoring at 1280x720 | total ≥200, families_ge3 ≥10, union constructible ≥10 |
| B-WEBGYM-292K-DIVERSE | dataset | WebGym 292k/127k sites diverse eTLD+1 slice ≥50 distinct, duplication prevalence via family-level B=2000 bootstrap, threshold sweep 0.818 and 0.9479 range≥0.05 monotonic — replaces 567MB LFS | diverse ≥50, CI width>0, sweep range≥0.05 monotonic |
| B-TRUNCATED-20 | fragment | Selectors/AX tokens [:20] truncated vs full-tree multi-anchor; delta_vs_truncated diagnostic | delta ≥0.20 if full-tree non-vacuous; shuffled <0.05 |
| B-AGENTIC-DSM | external_sota | Agentic Compilation DSM 99% TreeWalker + JSON IR + HITL $0.002–0.092, 80–94% compile ceiling; blind per paper | coverage 0.75 [0.625,0.875] single-channel header1.0 body1.0 auth0.7 mixed0.3 USD $0.035/task HITL drop≥0.30 |
| B-STAGEHAND-SELECTOR | external_sota | Stagehand selector + relevant-subtree SHA256 HIT/MISS with expanded stripping {form_key,uenc,store,session,nonce,fotorama\d{6,}} | HIT ≥0.8 after stripping vs <0.4 before, lift≥0.40, per-channel breakdown |
| B-BMEM-CATALOG | external_sota | browser-memory catalog deterministic replay exact outerHTML, no alias handling | coverage ~0.0/40 degenerate CI [0,0] flagged |
| B-SPIDER-ALIAS | spider | SPIDER alias-catalog literal catalog with per-value alias handling, honest sum-counters | coverage flat p>0.05 ~0.925, cost F10 ~30.1 vs DSM22.6 |
| B-SPIDER-ROUTING | spider | SPIDER mechanism routing score+param-slot tie-break 0.95/0.85 | coverage 1.0 degenerate CI[1,1] flagged, cost F10 ~33.0 |
| B-SPIDER-WEBMCP | spider | SPIDER WebMCP tool prevalence emulation tool/API bypass at f=10/100 | prevalence 0.725 [0.575,0.85] amortized F10 2.9 F100 0.725 |
| B-COLD-LLM | cold | Cold LLM no-memory floor same model/tools/budget | coverage ~0.25 floor [0.125,0.375] M_total 38.0 |

Per-task logs for all 40 tasks × 7 baselines + Stagehand ablation required in artifacts/derived/sota_blind_results.jsonl with trajectory-grouped bootstrap B=2000.

---

## 6. Controls

### Positive control — PC-SYNTHETIC-FIXTURE-TOY-DSM-STAGEHAND-WEBGYM-SANITY
- **PC-A** Synthetic Flask product fixture at 1280x720 fixed DOM heading+price+add-to-cart+main+contentinfo localhost, AX ~17 nodes deterministic; pipeline must capture median AX>10 DOM≥2000, SHA before==after identical TRUE 12/12, mutated textContent SHA != 12/12. Also 12 product captures on canonical families 136/145/196/222 median AX688 min627 DOM200413 min195052; full-tree AX_consistency mean≥0.6 CI lower>0.5 shuffle p<0.05 gap≥0.20 variance>0 delta≥0.20.
- **PC-B** Toy single-header param task: DSM minimal JSON IR compile 1.0 blind, Stagehand minimal selector+subtree HIT 1.0 after expanded stripping.
- **PC-C** (gated HF_TOKEN) WebGym diverse-sanity ≥50 diverse yields prevalence in [0.3,0.99] and sweep monotonic.
- **PC-D** Hard258 fixture: synthetic hard-task manifest parsing yields families_ge3 ≥2 on fixture.
*Expected:* PC-A VALID captures median AX>10 DOM≥2000 SHA both directions TRUE anchored 12/12 AND AX_consistency gates; PC-B 1.0; PC-C monotonic and CI computable when HF succeeds else UNAVAILABLE not failed; PC-D parse PASS.

### Null controls — NC-SHUFFLED-TRUNCATION-NOHITL-STAGEHAND-STRIP-AX (all trajectory-grouped family-level, not transition-grouped)
- **NC1** Family-label shuffle (1000 perms coverage, 2000 family-level WebGym, AX_consistency shuffle): |rho_shuffled|<0.20, shuffle mean ~ chance, gap real-shuffle ≥0.20, AX shuffled mean <<0.6 p>0.05.
- **NC2** Truncated B-TRUNCATED-20 vs full-tree: delta_vs_truncated ≥0.20 real must hold; shuffled variant <0.05; previous degenerate CI[0.7,1.0] p=1.0 rejected.
- **NC3** HITL disabled/random patch: DSM coverage drop ≥0.30 vs HITL (observed 0.50).
- **NC4** Stagehand stripping ablation: HIT with expanded stripping vs without delta ≥0.40; without stripping HIT <0.5.
- **NC5** AX_consistency family permutation: shuffled mean <0.6 p>0.05 variance 0 vs real variance>0 gap≥0.20.
*Expected:* NC1 |rho|<0.20 p>0.05 shuffled, NC2 delta<0.05 shuffled, NC3 drop≥0.30, NC4 lift≥0.40, NC5 shuffled <<0.6.

All CIs trajectory-grouped bootstrap 95% percentile. Degenerate [0,0] BMEM and [1,1] ROUTING/WebMCP flagged per prereg 12.7 variance==0 not counted as valid width.

---

## 7. Measurement validity (gating, frozen)

1. **MV1_DURABLE_ATTEMPTS:** Each durable source (HF WebArena 812+Hard258+WebGym 292k, GHCR BrowserGym 0.14.3, Docker Hub webarena-verified-shopping) requires ≥2 genuine attempts logged with URL, HTTP status/returncode, bytes, sha256 hex, 64-char digest check, timeout ≥300s or docker load fallback captured, stderr/stdout. Single-attempt success → MEASUREMENT_INVALID. HF_TOKEN present true/false logged. GHCR and Hub API digest 200 required. Evidence: artifacts/raw/webarena_verified_pin.json, hf_manifest_attempts.json, hf_webgym_manifest_attempts.json, ghcr_browsergym_attempts.json, docker_hub_api_attempts.json, hard258_census.json, provenance.json hashes.

2. **MV2_BYTE_IDENTITY:** Manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (927596 bytes, 64 hex) equality stored; GHCR digest 64-char hex equality with GHCR API 200; Docker digest exactly sha256:3e8cb9b9... (64 hex after colon) Hub API 200. If one source succeeds, single sha256 pinned file + log suffices but cross-source equality explicitly UNAVAILABLE not assumed equal. WebGym SHA separately logged when HF_TOKEN succeeds. Hard258 SHA separately pinned, families_ge3 histogram recorded. Reuse prior pinned file allowed only with +2 fresh verification attempts this experiment.

3. **MV3_AX_REPAIR_FULLTREE:** BrowserGym-core==0.14.3, AgentLab==0.4.2, Playwright==1.63.0, playwright --with-deps chromium verified via pip freeze sha256 nonempty (263 lines) and browser validation; viewport 1280x720 strict; CDP Accessibility.getFullAXTree via cdp_session required — fallback accessibility.snapshot → MEASUREMENT_INVALID for H_A. Metrics median AX>10, DOM≥2000, body regex <body[^>]*>.*?</body> DOTALL + 9 base + expanded stripping (form_key/uenc/store/session/nonce/timestamp/fotorama\d{6,}) before SHA256 via page.evaluate, recomputed after page.content()+AX, grammar hash live via research/intel/grammar_fulltree_*.py hash 273eafbcb... live not hardcoded. Provenance: ax_captures.jsonl, derived/ax_analysis.json, ax_consistency_fulltree.json, grammar sha live. Full-tree multi-anchor AX_consistency on full tree (not [:20]) with Runtime.evaluate getBoundingClientRect heading/price/add-to-cart/main/contentinfo node_count>1; truncated [:20] also computed for delta gate.

4. **MV4_PRODUCT_FAMILY_CONSTRUCTIBILITY_HARD258:** Deterministic test executed exactly: sorted families_ge3 from webarena_census.json (812) AND Hard258 census, two independent Random(35725763380).sample(sorted families_ge3,10) with seed reset logged S1 and S2 on EACH census (S1==S2 expected but both logged), each probed via get_task_start_url __SHOPPING__ expansion + product-subtree anchoring heading/price/add-to-cart/main/contentinfo node_count>1 distinct SHA256 on canonical 136/145/196/222 at 1280x720 CDP (12 captures median AX688 DOM200413), per-family anchoring json; constructible = distinct families anchoring true among S1|S2 plus canonical plus Hard258 union; gate ≥10 distinct; full-tree AX_consistency mean≥0.6 CI lower>0.5 B=2000 gap≥0.20 p<0.05 variance>0 delta≥0.20 on ≥10 family set. Without BOTH samples logged per census → MEASUREMENT_INVALID for that clause. Runtime single-node health-gated harness availability must be documented (dependency).

5. **MV5_WEBGYM_DIVERSE_AND_THRESHOLD_SWEEP:** WebGym 292k/127k sites when HF_TOKEN succeeds sampled ≥50 distinct eTLD+1 documented extraction, family-level grouping preserved, duplication prevalence Jaccard/template duplication ≥ threshold (exact Jaccard/regex choice documented), family bootstrap B=2000 unit=family 95% CI non-degenerate, sweep at 0.818 and 0.9479 range = prevalence_0.818 - prevalence_0.9479 ≥0.05 monotonic decreasing to replace 567MB LFS. If HF_TOKEN 401 after 2 attempts ≥300s each, diverse count explicitly UNAVAILABLE with attempts logged not zero; then clause alone does not trigger MEASUREMENT_INVALID but H_A partially unavailable, PC-C UNAVAILABLE.

6. **MV6_SYNTHETIC_ALIAS_OOD:** Synthetic 40 tasks seed 360360 generation sha 5311a581 preserved in research/intel/synthetic_alias_ood_40.json sha 6f42bc82..., split 30 orthogonal (10 header/10 body/10 auth) +10 mixed triple-channel, orthogonality verified no cross-channel leakage (header/body/auth isolation). If missing, generate deterministically and hash generation script. Mixed tasks combine all three channels independent alias rotations. Harness sha b11ea970 byte-identical re-run verified.

7. **MV7_HONEST_COST:** M_total_f10/f100 per-trajectory-reset sum-counters (resolve+bind+verify+freshness_check+browser_steps) reset per trajectory/task summed then amortized at f=10/100 sum/min(f,N) verified. Prohibited proxies n*3200, f*6.0, Gaussian jitter, n*constant → MEASUREMENT_INVALID. Trajectory-grouped bootstrap B=2000 unit=task/trajectory 95% CI non-degenerate when variance>0; degenerate [0,0] or [1,1] flagged per 12.7 not valid width but not invalid gate. Negative shuffle |rho|<0.20 trajectory-grouped. Honest USD also reported DSM $0.002–0.092 (midpoint $0.047) and Stagehand $0 if selector-only.

8. **MV8_EXTERNAL_BLINDNESS:** Baselines implemented blind per recipe citations without tuning to 40-task split labels; code paths, recipe docs (DSM TreeWalker IR schema, Stagehand selector+subtree HIT/MISS with expanded stripping {form_key,uenc,store,session,nonce}, catalog replay selector) stored; per-task logs for all 40 tasks per baseline required artifacts/derived/sota_blind_results.jsonl including toy+40×7 baselines byte-identical re-run, per-channel breakdown. Same 40-task split all baselines one run. Harness sha logged and re-run byte-identity verified. Hard258 probes logged blind to family labels. Stagehand ablation logged both with/without expanded set.

9. **MV9_PROVENANCE:** Every artifact path+sha256 stored in provenance.json: request/spec/prereg/freeze hashes, pip freeze hash nonempty, docker images --digests hash, ghcr/docker_hub attempts, command logs pull/load/run, HF manifest sha/bytes (or 401 log), WebGym sha when available, Hard258 census sha, generation script hash, per-baseline jsonl, census derived jsons (primary+Hard258), ax captures/probe logs, threshold sweep table, AX_consistency fulltree json, Stagehand stripping delta. Missing provenance for any durability/cost/AX path → MEASUREMENT_INVALID for that module.

---

## 8. Decision rule (frozen three-way, after MEASUREMENT_INVALID check)

**(A) MEASUREMENT_INVALID** if any MV1–MV4/MV6–MV9 mandatory gating fails: <2 genuine attempts per required durable source (GHCR 0.14.3, Docker Hub webarena, HF WebArena/Hard258/WebGym), missing 64-char digest or manifest SHA d6527566, pip freeze empty or version/viewport mismatch (requires 0.14.3/0.4.2/1.63.0 1280x720), fallback AX snapshot used, body regex absent, deterministic sampling not executed exactly on BOTH primary and Hard258 censuses, AX_consistency not full-tree multi-anchor with bootstrap/trajectory-grouped, Stagehand expanded stripping not ablated, honest-cost proxy/ungrouped CI detected, or provenance missing — then no SURVIVES/FALSIFIED inference.

MV5 WebGym diversity clause alone defaults to UNAVAILABLE not INVALID when HF_TOKEN absent after 2 genuine attempts (marked null with attempts logged, PC-C UNAVAILABLE).

**(B) SURVIVES_CURRENT_TEST** iff A passes (MV5 either PASS or documented UNAVAILABLE) AND **H_A_SURVIVES**: (SRC_GHCR_SUCCESS OR SRC_DOCKER_SUCCESS) with census artifact manifest_sha256=d6527566 total 700–812 primary plus Hard258 ≥200 families_ge3 ≥30 (or union ≥10) AND deterministic constructibility ≥10 distinct product families anchoring true SHA both directions TRUE CDP 1280x720 median AX>10 & DOM≥2000 on canonical 136/145/196/222 AND full-tree AX_consistency mean≥0.6 CI lower>0.5 B=2000 gap≥0.20 p<0.05 variance>0 delta≥0.20 on ≥10 family set AND (WebGym diverse ≥50 duplication CI non-degenerate sweep 0.818–0.9479 range≥0.05 monotonic when HF succeeds OR explicitly unavailable with 2 attempts logged) AND **H_B_SURVIVES**: all three external baselines B-AGENTIC-DSM/B-STAGEHAND-SELECTOR/B-BMEM-CATALOG executed blind with per-task logs + per-channel breakdown producing interior non-degenerate trajectory-grouped CIs where variance>0, and Stagehand HIT ≥0.8 after stripping lift ≥0.40, and |rho|<0.20 and HITL drop≥0.30 and delta≥0.20 real vs <0.05 shuffled, and honest M_total_f10/f100 Pareto vs SPIDER alias/routing/WebMCP quantified with bootstrap (DSM F10 ~22.6 vs ALIAS 30.1 vs WebMCP 2.9).

**(C) Otherwise** if A passes but not all B conditions: **FALSIFIED** if primary census still 4 families only and WebGym sweep fails and baselines at null level; **MIXED** if one module passes (e.g., census 10 families survives but WebGym UNAVAILABLE, or DSM survives but Stagehand lift fails). Audit may bound ceiling narrower than SURVIVES.

All metrics recomputed with trajectory-grouped family-level bootstrap; transition-grouped treated as MEASUREMENT_INVALID per prior audit.

---

## 9. Metrics and control identities (stable for downstream)

**Primary metrics:**
- `M_CONSTRUCTIBLE_FAMILIES` — distinct product families anchoring true + SHA stability both directions TRUE among S1|S2 union + canonical + Hard258 (gate ≥10)
- `M_AX_CONSISTENCY_MEAN` — full-tree multi-anchor AX_consistency mean on ≥10 family set (gate ≥0.6)
- `M_AX_CONSISTENCY_CI_LOWER` — bootstrap 95% lower (gate >0.5)
- `M_AX_SHUFFLE_P` — trajectory-grouped shuffle p (gate <0.05)
- `M_AX_GAP` — mean - shuffle mean (gate ≥0.20)
- `M_AX_DELTA_TRUNCATED` — full-tree - [:20] truncated (gate ≥0.20)
- `M_WEBGYM_DIVERSE_ETLD` — distinct eTLD+1 count (gate ≥50)
- `M_WEBGYM_DUP_PREVALENCE` — duplication prevalence CI non-degenerate
- `M_WEBGYM_SWEEP_RANGE` — prevalence_0.818 - prevalence_0.9479 (gate ≥0.05)
- `M_DSM_COVERAGE_OVERALL` — DSM coverage overall [0.625,0.875] interior
- `M_DSM_COVERAGE_PER_CHANNEL` — header/body/auth/mixed breakdown (mixed 0.3 vs single 0.9–1.0)
- `M_STAGEHAND_HIT_POST_STRIP` — Stagehand HIT after expanded stripping (gate ≥0.8)
- `M_STAGEHAND_LIFT` — post minus pre stripping (gate ≥0.40)
- `M_BMEM_COVERAGE` — BMEM 0.0 degenerate flagged
- `M_TOTAL_F10_DSM/ALIAS/ROUTING/WEBMCP/COLD` — honest sum-counter amortized f=10 (DSM22.6 vs ALIAS30.1 vs WebMCP2.9)
- `M_TOTAL_F100_*` — amortized f=100 (DSM5.65 vs ALIAS7.53 vs WebMCP0.725)
- `M_RHO_SHUFFLED` — |rho_shuffled| cost vs length (gate <0.20)
- `M_HITL_DROP` — DSM coverage with vs without HITL (gate ≥0.30)
- `M_USD_DSM_MEAN` — DSM USD mean $0.0353 [0.0294,0.0411]

Controls and baselines keyed by IDs in §5–6 preserved in result.json:controls exactly.

---

## 10. Product consequences

**If SURVIVES:** Intel delivers Codex-accepted durable census artifacts (pinned manifest SHA d6527566 927596 bytes + GHCR 0.14.3 digest + Docker digest 3e8cb9b9... 64 hex + Hard258 ≥200/union ≥10 + WebGym diverse CI B=2000 sweep 0.818–0.9479) unblocking Graph ≥10-family product hold-out design — next Graph can use deterministic Random(35725763380).sample hold-out without re-probing liveness; repaired BrowserGym fragment pipeline (1280x720 CDP AX>10 full-tree multi-anchor mean≥0.6 CI lower>0.5 p<0.05 gap≥0.20 + body+expanded stripping + anchored geometry) becomes shared substrate satisfying runtime:C-MEAS-VALID dependency; external ceilings define O(1) compilation (DSM $0.002–0.092 F10 22.6 USD $0.035/task, Stagehand HIT 0.8+ lift 0.40, BMEM 0.0) that SPIDER must beat for residual-novelty economics; hybrid WebMCP bypass 0.725 prevalence establishes tool-bypass vs browsing dispatch Pareto — Product can run Stagehand/WebMCP vs compilation Pareto to decide VALIDATED vs hybrid dispatch. C-CROSSSITE advances toward EXPERIMENTAL at durable-artifact+diverse-holdout ceiling with full-tree validity, C-RESIDUAL-NOVELTY/C-PRODUCT-ECON gain honest Pareto baseline with single-node gate before distributed scaling.

**If FALSIFIED:** Deterministically proven BOTH pinned 812 and Hard258 union contain only 4 constructible families (136/145/196/222) with AX_consistency failing — Graph ≥10-family hold-out remains BLOCKED on these censuses, requires orthogonal census beyond Hard258 (WebMall/Mind2Web-2 130-task loopback, WebGym-derived families independent hosting) or definition expansion (shopping vs shopping_admin 404) and must not re-attempt N=20 longest-prefix on same 4-family substrate (expected MEASUREMENT_INVALID). If WebGym diverse <50 or sweep <0.05, single-store duplication vacuous remains — holdout without diversity not replaced. If AX_consistency fails, homepage-only degenerate remains — requires full-tree repair before claiming C-CROSSSITE. If external baselines falsify (Stagehand <0.8 even after stripping, DSM at null), O(1) ceilings not transferable to SPIDER alias-OOD or synthetic design misaligned — requires redesign of alias-OOD channels or HITL/stripping model before Product claims economics; SPIDER alias-catalog flat p=0.626 vs DSM collapse indicates site-stability not alias robustness. C-CROSSSITE stays HYPOTHESIS/EXPERIMENTAL at 4-family ceiling, others remain HYPOTHESIS.

**If MEASUREMENT_INVALID:** No claim update; smallest repair per MV1–MV9 (genuine attempts ≥2, versions 0.14.3, CDP full-tree, deterministic samples both censuses, expanded stripping ablation, honest counters, family-level bootstrap, threshold sweep, AX_consistency multi-anchor) and re-run identical frozen design.

---

## 11. Validity threats and mitigations

- **Single-node vs distributed gap:** Director portfolio notes factory tunneled on MEASUREMENT_INVALID via AX_consistency product-page sampling (HIT 0.0 incomplete stripping) and WebGym diverse fetch (0/50 Gate0). Runtime single-node health-gated harness is explicit dependency; all Gates require median AX>10 before distributed n≥800 promotion. This experiment runs single-node only, documenting that ceiling.
- **Template overlap independence threat:** Hard258 derived from same WebArena-Verified v2 base as primary — not fully independent census. Provenance logs filter query and template overlap diagnostic; if union <10, result is bounded FALSIFIED not global rejection — truly orthogonal census (WebMall/Mind2Web-2) remains next step per handoff do_not_assume.
- **Degenerate CIs:** Prior audit flagged BMEM [0,0] and ROUTING/WebMCP [1,1] variance 0 invalid width; this prereg requires interior non-degenerate width when variance>0 and explicit flag when degenerate — prevents misreading zero-variance as high-precision.
- **Synthetic-to-real gap:** Synthetic 40-task alias-OOD is orthogonal estimator benchmark, not real DOM heterogeneity/compression until production regime (|S|≥16, H>0.2, AX>10) provisioned — prior informs priority, not SPIDER law. Real WebArena hold-out transfer remains unknown until Graph runs N≥120 hold-out.
- **Work compression honesty:** Per_hit derivation 1.005>0.85 falsified per audit, superseded by M_total_f10 Pareto at f=10 and f=100. This experiment enforces honest per-trajectory-reset sum-counters, prohibits n*3200/f*6.0 proxies, requires trajectory-grouped bootstrap and |rho_shuffled|<0.20, aligning with Director agent prior 2.
- **Deterministic replay + selector healing:** Minimal viable product per Director prior 4 is deterministic replay + healing + verification/UNKNOWN abstention with freshness gate — single-node honesty before distributed scaling (Stagehand/ActCache evolution). Stagehand HIT ≥0.8 after expanded stripping tests that minimal gate.
- **Tool/API bypass leverage:** Director prior 5 tool/API bypass via OpenAPI/HATEOAS and JSON IR higher leverage than template rewriting when alias heterogeneity spans header+body+query+auth jointly; mixed 0/10 bottleneck tests composition not retrieval. Stagehand relevant-subtree SHA256 vs DSM JSON IR directly evaluates this.
- **O(1) compilation economics:** Prior 6 O(1) compilation ($0.002–0.092) vs O(MxN) browsing requires Pareto dominance at f=10 and f=100 vs shipped caches before PRODUCT_CORE. Honest M_total_f10/f100 with USD reported tests this threshold.

---

## 12. Preregistration freeze

- Hypothesis, state/action representations, sampling policy (Random(35725763380).sample x2 per census, get_task_start_url __SHOPPING__ expansion, product-subtree node_count>1), target (≥10 families), holdout (deterministic 10 per census), nulls/baselines, primary metrics, expected directions, uncertainty method (trajectory-grouped family-level B=2000 percentile CI, 1000 perms for coverage, 2000 for WebGym duplication), adequacy rule (median AX>10 DOM≥2000, CI lower>0.5, gap≥0.20, sweep range≥0.05), falsification/survival rule (§8) frozen before outcome.
- Any changed analysis after seeing outcomes is exploratory. New confirmatory claim requires new preregistration and untouched evidence.
- DESIGN did not inspect outcome measurements. EXECUTE must execute exactly this frozen design; may not mutate frozen inputs.

---

## 13. Estimated cost and information gain

**Compute:** 4–6h runner wall (GHCR 5.4GB if not cached + Docker webarena pull, 2× genuine attempts per source HF+GHCR+Hub each 300s or docker load fallback ~15–30min, Hard258 derive +2 attempts 10min, WebGym 292k parse/sample sweep 0.818–0.9479 ~15min, deterministic sampling x2 per census + anchored AX probe ≥10 families per census ~30–45min at 1280x720 CDP, synthetic 40×7=280 task executions + Stagehand ablation 40 extra + B=2000 bootstraps ~60–90min). Network 2× attempts + API 200 + WebGym download only if HF_TOKEN valid. No LLM calls required. USD ~$4–6 GH runner. Artifact storage <100MB.

**Expected information gain:** High, Director-ranked PIVOT gating, cognitive_reset SUPERSEDE. Directly answers whether 23-deep Intel tunnel can escape 4-family ceiling via Hard258 union and whether 567MB LFS exhaustive is replaceable by sweep CI — unblocking Physics Gate0 and Graph ≥10-family N≥120 that prior 8 pilots left MEASUREMENT_INVALID, and quantifying O(1) compilation vs Stagehand stripping Pareto (DSM F10 22.6 vs ALIAS 30.1, WebMCP 2.9) deciding residual-novelty rho≥0.60 economics vs tool-bypass hybrid dispatch. Bounded negative equally decision-changing. Higher leverage than another N=20 homepage AX_consistency or exhaustive LFS per Director comparative reasoning (falsified 18/20 identical 1430-node captures p=1.0, HIT 0.0 incomplete stripping, blocked 292k exhaustive).

---

## 14. Provenance and reproducibility

Every artifact path+sha256 stored in provenance.json and freeze.json. Required: request/spec/prereg/freeze hashes, pip freeze 264 lines sha, docker images --digests, ghcr/docker_hub attempts, HF manifest sha/bytes or 401 log, WebGym sha when available, Hard258 census sha, synthetic generation sha 5311a581, sota_blind_results.jsonl 327+ rows + stripping delta, census derived jsons primary+Hard258, ax captures/probe logs, threshold sweep table, AX_consistency fulltree json, command logs pull/load/run, threshold sweep monotonic proof. Missing provenance → MEASUREMENT_INVALID for that module.

Pipeline versions pinned: BrowserGym-core 0.14.3, AgentLab 0.4.2, Playwright 1.63.0, viewport 1280x720, CDP Accessibility.getFullAXTree, grammar_fulltree_358885.py body regex DOTALL, expanded stripping regex fotorama\d{6,} + {form_key,uenc,store,session,nonce}. Deterministic seed 35725763380, 360360 for synthetic.

---

*End of preregistration — frozen before execution. Any deviation during EXECUTE must be logged as validity_notes and may trigger MEASUREMENT_INVALID per §8.*
