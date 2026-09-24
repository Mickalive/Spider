# EXP-INTEL-35999366789 — preregistration

## 1. Experiment Identity
- **experiment_id:** EXP-INTEL-35999366789
- **lane:** intel
- **claim_ids:** C-CROSSSITE (primary), C-RESIDUAL-NOVELTY, C-PRODUCT-ECON (downstream economics ceiling)
- **parent_handoff:** research/experiments/EXP-INTEL-35956094394/handoff.json sha256 75a71dd1e1b483712a31f8838a82c4609b47e4f53a051a8de16d8733fea81771
- **parent disposition:** **USE** per Global Director mandate cycle 35998407068 (CONTINUE). Inherited handoff is continuity evidence with four-way distinction (established/rejected/unknown/do_not_assume) preserved below; it does NOT override the binding Director strategic question.
- **binding direction:** request.json `director_mandate.allocation.question` (action CONTINUE, target C-CROSSSITE, cognitive_reset true). This prereg converts the Director's strategic question into the smallest falsifiable experiment; it refines — not drifts from — the Director mandate.

## 2. Director's Strategic Question (verbatim, binding)

> Can Intel deliver the durable census and external baseline substrate that unblocks cross-site transfer: (1) acquire WebArena-Verified v2 812-task census via durable pinned source (HuggingFace OpenEnv BrowserGym hosted layer or Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb with 64-char hash byte-identical manifest, SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 verified, HF_TOKEN for WebGym 292k 292k tasks/127k sites manifest sample >=50 diverse eTLD+1 for duplication CI (2000 family-level bootstrap) and threshold sweep 0.818-0.9479 to replace exhaustive 567MB LFS test.zip) and prove >=10 product families constructible (deterministic random.Random(35725763380).sample(sorted families_ge3,10)x2 with get_task_start_url __SHOPPING__ expansion + product-subtree anchoring heading/price/add-to-cart/main/contentinfo node_count>1 distinct SHA on path families 136/145/196/222 at 1280x720 CDP AX>10), and (2) blindly reproduce external SOTA baselines (Agentic Compilation DSM 99% TreeWalker+deterministic JSON IR+HITL $0.002-0.092 80-94% compile, TraceCompiler def-use 0.928/0.943, browser-memory catalog) on SPIDER synthetic 40-task alias-OOD (30 orthogonal header/body/auth+10 mixed) with trajectory-grouped bootstrap coverage/CIs and honest per-trajectory-reset sum-counter M_total_f10 Pareto f=10/100 vs SPIDER alias-catalog/routing/WebMCP, measuring where SPIDER must beat O(1) compilation to claim residual-novelty economics and whether hybrid WebMCP bypass 0.725 prevalence dominates?

Agent priors labeled in mandate (compounding planning errors trapped in alias families, tool/API bypass prevalence, Laplace/Gamma-ratio bias traps, residual-novelty rho>=0.60, trajectory-grouped resampling requirement) are priors, not SPIDER evidence, and are tested via the prereg gated metrics below.

## 3. Why this CONTINUE refines the parent, not merely repeats it

Parent EXP-INTEL-35956094394 delivered BOUNDED_PARTIAL_SURVIVES: single-source Docker pin verified (manifest SHA d6527566..., 927596 bytes, Docker digest 3e8cb9b9... 64 hex, container quirky_ishizaka reachable HTTP200, census 812 tasks shopping192 shopping_admin182 families_ge3 36) with repaired CDP pipeline (BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 chromium 153.0.8010.12 viewport 1280x720 CDP Accessibility.getFullAXTree median AX 698 DOM 201305 SHA 16/16 both directions, fotorama\d{6,} + body regex stripping, anchored geometry replacement 13/13) and synthetic 40-task alias-OOD blind reproduction (DSM 0.75 [0.625,0.875] single-channel 0.90 vs SPIDER-ALIAS 0.925 [0.85,1.0] flat p=0.626, TRACE 0.25 BMEM 0.0, honest M_total_f10 DSM22.6 ALIAS30.1 WEBMCP28.0, |rho_shuffled|0.1592, HITL drop 0.50, WebMCP prevalence 0.725). Audit downgraded ceiling to **4 product_page families [136,145,196,222]** not >=10, single-source pin only (HF 401x3, HF_TOKEN absent), synthetic work units only (no wall-clock/LLM cost), degenerate CIs BMEM[0,0] ROUTING/WEBMCP[1,1], and WebGym 292k duplication/threshold sweep null.

Director portfolio: Intel is 22-deep C-CROSSSITE tunnel with textbook local-optima trap where further Jaccard/regex tuning will not escape without orthogonal basin. Vs exhaustive LFS 567MB/CAP 420-task enumeration (proven vacuous duplication 0.9479 single-store) and vs another N=20 AX_consistency without fixing census (would repeat 18/20 identical captures), the highest marginal information per Scout is **durable census + diverse holdout + blind SOTA O(1) ceiling** that unblocks Graph >=10-family hold-out, Product Pareto, and Physics Gate0 |S|>=16.

This CONTINUE therefore keeps the two-module durable-census + blind-SOTA structure but upgrades it with the five remaining required_fixes explicitly enumerated in handoff: (1) prove >=10 families via deterministic random.Random(35725763380).sample x2 with get_task_start_url expansion + product-subtree anchoring (not just census count), (2) acquire HF_TOKEN WebGym 292k diverse >=50 eTLD+1 duplication CI family-level B=2000 and threshold sweep 0.818-0.9479 replacing 567MB LFS, (3) re-measure SHA stability on >=10 families with anchoring node_count>1 distinct SHA on canonical path 136/145/196/222, (4) retain honest per-trajectory-reset sum-counters + trajectory-grouped bootstrap Pareto for residual-novelty rho>=0.60 economics vs O(1) compilation, (5) quantify hybrid WebMCP bypass dominance. It does not merely replay the parent's 4-family probe.

## 4. Inherited scientific state (four-way distinction from parent handoff)

**Established (reuse, do not re-prove):**
- Docker-pinned WebArena-Verified v2 manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (927596 bytes) verified via Hub API digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (64 hex), container quirky_ishizaka reachable http://localhost:7770 HTTP200 — artifacts/raw/webarena_verified_pin.json sha 8a529cc824, derived/webarena_census.json sha 6fcdc04f (total812 shopping192 shopping_admin182, 36 families_ge3, product_page_tasks 7).
- Repaired fragment pipeline at 1280x720: BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 chromium 153.0.8010.12, CDP Accessibility.getFullAXTree, median AX 698 (min626) median DOM 201305 (min195052) on 13 real product pages +3 synthetic, outerHTML SHA256 recomputed AFTER page.content()+AX with 9 base + expanded (fotorama\d{6,}) + body regex <body[^>]*>.*?</body> DOTALL live grammar hash 273eafbc..., SHA stability 16/16 identical +16/16 mutated, AXNode.boundingBox/computedStyle absent 0/16 Chromium153 fact with anchored Runtime.evaluate replacement 13/13.
- Synthetic 40-task alias-OOD deterministic fixture research/intel/synthetic_alias_ood_40.json sha 6f42bc82 seed360360 split 10 header +10 body +10 auth +10 mixed orthogonal, generator sha 5311a581..., channel labels verified.
- Blind external SOTA reproduction with honest per-trajectory-reset sum-counters and trajectory-grouped B=2000 bootstrap (sota_blind_results.jsonl sha 3c5ab5af byte-identical re-run, analysis sha 199570b64): DSM 0.75 [0.625,0.875] single-channel 0.90 mixed 0.3, TRACE 0.25 body1.0 only, BMEM 0.0, SPIDER-ALIAS 0.925 [0.85,1.0] flat p=0.626, ROUTING/WEBMCP 1.0 degenerate, M_total_f10 DSM22.6 TRACE10.0 ALIAS30.1 ROUTING33.0 WEBMCP28.0 COLD38.0 F100 proportional, |rho_shuffled|0.1592 pass, HITL drop 0.50, prevalence 0.725 [0.575,0.85].

**Rejected (bounded):**
- H_A requiring >=10 product_page families at 1280x720 from this pin — falsified to 4 families [136,145,196,222] among 36 families_ge3 on current census; richer AX via AXNode.boundingBox/computedStyle on Chromium153 rejected 0/16; exact-catalog deterministic replay B-BMEM-CATALOG rejected 0.0/40; TraceCompiler def-use rejected except body; DSM 99% ceiling on alias-OOD partially rejected 0.90 interior; degenerate CIs [0,0]/[1,1] rejected as valid width; H_B non-degenerate CI requirement for saturating points rejected.

**Unknown:**
- Cross-source byte-identity (Docker vs HF raw) — unverifiable without HF_TOKEN (401x3); whether >=10 product_page families exist in any alternative census (WebMall/Mind2Web-2 loopback, expanded shopping_admin 404) — current pin ceiling 4; WebGym 292k diverse eTLD+1 slice and duplication 0.818-0.9479 sweep — null; real WebArena product-family hold-out transfer vs synthetic; real-cost Pareto wall-clock/LLM tokens vs O(1) $0.035/task; causal step for DSM auth 0.7 vs SPIDER 1.0; harness SHA discrepancy origin.

**Do_not_assume:**
Do not assume C-CROSSSITE validated, >=10-family constructibility from this pin, cross-source byte-identity, degenerate CIs are high-precision, M_total synthetic work units = USD/wall-clock, M_FALSE_ACCEPT 0 is empirical, richer AX bbox via CDP available, family permutation p=1.0 lack of transfer, DSM 99% transfers to alias-OOD, BMEM/ROUTING/WEBMCP 0/1 are CI-validated, synthetic deterministic world = real Web volatility.

## 5. Hypotheses (falsifiable, per spec)

**H_A_DURABLE_CENSUS_EXPANDED:** A byte-identical durable pin verified as manifest SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (927596 bytes) with Docker digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb (64 hex) via >=2 genuine attempts per source (HF_TOKEN bearer capture, Hub API 200, docker pull --digests / docker load fallback, 300s timeout) yields verifiable WebArena-Verified v2 census (total 812 +-10, shopping 192, families_ge3 >=30) and, with deterministic random.Random(35725763380).sample(sorted families_ge3,10) executed TWICE with get_task_start_url __SHOPPING__ expansion and product-subtree anchoring (heading/price/add-to-cart/main/contentinfo node_count>1, distinct SHA before==after identical TRUE and after mutation != TRUE on canonical path families 136/145/196/222 at 1280x720 CDP Accessibility.getFullAXTree median AX>10 median DOM>=2000), proves >=10 distinct product families constructible with anchoring and SHA stability (16/16 both directions on probed families) plus WebGym 292k diverse sample >=50 distinct eTLD+1 with family-level B=2000 bootstrap duplication prevalence CI and threshold sweep 0.818-0.9479 range >=0.05 replacing exhaustive 567MB LFS test.zip.

**H_B_SOTA_CEILING_HONEST_PARETO:** On SPIDER deterministic synthetic 40-task alias-OOD (research/intel/synthetic_alias_ood_40.json seed 360360, 10 header-param +10 body-param +10 auth-param +10 mixed multi-channel orthogonal, generator sha logged) blind reproduction per published recipe of B-AGENTIC-DSM (DSM 99% TreeWalker + deterministic JSON IR + HITL patch $0.002-0.092 80-94% compile), B-TRACECOMPILER-DEFUSE (def-use 0.928/0.943), B-BMEM-CATALOG (deterministic replay) alongside identically-measured SPIDER baselines B-SPIDER-ALIAS, B-SPIDER-ROUTING, B-SPIDER-WEBMCP and B-COLD-LLM yields trajectory-grouped B=2000 95% CIs for coverage and for honest per-trajectory-reset sum-counter M_total_f10 and M_total_f100 (resolve+bind+verify+freshness+browser_steps, amortized f=10/100) with |rho_shuffled|<0.20, revealing the O(1) compilation ceiling that SPIDER must beat for C-RESIDUAL-NOVELTY (rho>=0.60) and whether hybrid WebMCP tool-bypass 0.725 amortized f10/f100 dominates.

## 6. Designs — coordinated two-module experiment

### 6.1 Module A — Durable census, deterministic family constructibility, WebGym diverse duplication

**A1. Durable-source acquisition (each >=2 genuine attempts, 300s timeout):**
- SRC-HF: GET https://huggingface.co/datasets/ServiceNow/WebArena-Verified or OpenEnv BrowserGym hosted layer manifest raw + Hub API /v2/repositories/.../tags, with `Authorization: Bearer HF_TOKEN` when token set (token presence logged true/false, not required true). Capture URL, HTTP status, bytes, sha256 hex, manifest byte length (expect d6527566... 927596 bytes when succeeds).
- SRC-DOCKER: Verify 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb via Hub API 200 + local `docker pull am1n3e/webarena-verified-shopping@sha256:...` (timeout >=300s) or `docker load < cached.tar` / ghcr mirror fallback. Capture `docker images --digests`, pull stdout/stderr/returncode, Hub API digest 64 hex. Health `curl http://localhost:7770` 3 retries.
- WebGym 292k fetch (HF-gated): GET HF dataset manifest for 292k tasks/127k sites (HF_TOKEN bearer) — capture bytes/sha256/eTLD+1 slice (below).
- Byte-identical manifest: SHA equality stored. If only one source succeeds, single pinned sha256 + 2 log files suffices; cross-source equality explicitly marked unavailable, not assumed. Census artifact `research/experiments/EXP-INTEL-35999366789/artifacts/raw/webarena_verified_pin.json` with pinned URL, digest 64 hex, byte length, download logs, census counts: total, shopping, families_ge3, family histogram, product_page_families [136,145,196,222], derived/webarena_census.json sha verification.

**A2. Deterministic family constructibility with product-subtree anchoring:**
- Load census families_ge3 sorted list (36 families) from derived/webarena_census.json. Execute `random.Random(35725763380).sample(sorted_families_ge3, 10)` TWICE (two independent draws with same seed reset, logging both sample lists S1 and S2 — they will be identical but proves determinism). For each family in S1 ∪ S2 (up to 10 unique if overlapping, up to 20 if expanded census), probe constructibility:
  - Use `get_task_start_url` expansion of `__SHOPPING__` placeholder (BrowserGym get_task_start_url logic) to resolve product_page URL, or container localhost:7770 product path when available.
  - At 1280x720 viewport via CDP Accessibility.getFullAXTree, capture AX tree and DOM outerHTML with MV3 stripping before SHA256 (recomputed AFTER page.content()+AX, body regex + 9 base + expanded fotorama\d{6,}).
  - Count anchored product-subtree nodes: heading/price/add-to-cart/main/contentinfo present with node_count>1 (via anchored Runtime.evaluate getBoundingClientRect scan, not AXNode bbox). Require node_count>1 to count family as anchorable.
  - Prove distinct SHA: SHA stability before==after identical TRUE and after visible textContent/name mutation != TRUE (price/heading token mutation via page.evaluate, re-capture, compare SHA).
- Canonical path verification: families 136/145/196/222 (known 4 product_page families) must be probed at 1280x720 with median AX>10, DOM>=2000, anchoring true on each — this replicates parent's median 698/201305 and anchors replacement geometry proof (13/13 web pages).
- Constructible count = distinct families among S1 ∪ S2 ∪ [136,145,196,222] where anchoring true + SHA both directions TRUE. Gate: >=10 distinct => H_A constructibility survives; 4 => bounded falsified (documents hard ceiling).
- Artifacts: `artifacts/derived/deterministic_family_samples.json` (S1, S2, seed, sorted_families_ge3), `artifacts/derived/family_anchoring.json` (per-family node_count, SHA identical/mutated, AX nodes, DOM bytes), `artifacts/raw/ax_captures.jsonl` (CDP captures), `artifacts/derived/ax_analysis.json` (medians, bootstrap).

**A3. WebGym 292k diverse eTLD+1 duplication CI and threshold sweep (HF-gated):**
- When HF_TOKEN succeeds: parse WebGym 292k manifest, extract eTLD+1 per task site (via tldextract/publicsuffix or hostname suffix list, documented), sample >=50 distinct eTLD+1 with family grouping preserved (family = site family or duplication-template family; trajectory-grouped unit preserved). Compute duplication prevalence at threshold T: proportion of tasks where template/Jaccard duplication >= T (T defined as normalized template similarity or header/body/auth alias duplication; document exact Jaccard/regex choice). Compute point estimate + family-level bootstrap B=2000 95% percentile CI [lower,upper] (resampling unit = family, not task) for threshold 0.90 (primary) and for sweep endpoints 0.818 and 0.9479. Compute range = prevalence_0.9479 - prevalence_0.818; require range >=0.05 and monotonic (prevalence at 0.818 <= prevalence at 0.9479? depending on threshold direction, document and ensure monotonic). This sweep replaces exhaustive 567MB LFS test.zip (which was vacuous 0.9479 single-store).
- Diverse sample test: eTLD+1 distinct count >=50, duplication CI width >0, sweep table logged.
- When HF_TOKEN absent after 2 genuine attempts (401/404 logged with sha null): record diverse_etld_plus1=null, duplication_prevalence=null, sweep=null with attempts artifact — explicitly UNAVAILABLE, not assumed zero; does not alone trigger MEASUREMENT_INVALID but H_A partially bounded (same as parent UNRES-WEBGYM).
- Artifacts: `artifacts/derived/webgym_diverse_sample.json` (sample list, eTLD+1 counts, duplication prevalence, CI, sweep table, param prevalence if available), `artifacts/raw/hf_webgym_manifest_attempts.json` (HF 292k attempts).

### 6.2 Module B — External SOTA blind reproduction on synthetic 40-task alias-OOD with honest Pareto

**B0. Synthetic fixture:** `research/intel/synthetic_alias_ood_40.json` (generate deterministically if missing; seed 360360, generation script sha 5311a581... logged). 40 tasks: 10 header-param orthogonal, 10 body-param orthogonal, 10 auth-param orthogonal, 10 mixed multi-channel (header+body+auth). Each task records channel label orthogonality (no cross-channel leakage). Alias shift: train alias A != test alias B per channel; seed deterministic.

**B1. External baselines (BLIND — implement per paper recipe without tuning to synthetic channel labels):**
- B-AGENTIC-DSM: TreeWalker deep-structure model template → deterministic JSON IR → HITL patch hook ($0.002-0.092 per patch, 80-94% compile simulated via USD midpoint $0.047 when HITL true). Measure coverage (EXECUTABLE+verify pass) and cost: USD + M_total honest counter. Blind: template resolves only page-rendered slots, HITL hook is the only mechanism for alias slot fill.
- B-TRACECOMPILER-DEFUSE: trace → def-use chain → IR compilation per 0.928/0.943 spec. Coverage likewise.
- B-BMEM-CATALOG: exact selector replay without alias slot handling (deterministic). Expected to dominate on no-shift, collapse on alias-OOD.
- Constraint: same 40-task split in single run, per-task log written (`artifacts/derived/sota_blind_results.jsonl` with task_id, baseline id, success bool, per-channel label, cost counters resolve/bind/verify/freshness/browser_steps, IR snippet hash, USD).

**B2. SPIDER baselines (identically-measured honest costs for Pareto):**
- B-SPIDER-ALIAS, B-SPIDER-ROUTING, B-SPIDER-WEBMCP, B-COLD-LLM. Each runs on identical 40-task split, same honest sum-counter harness (per-trajectory reset). WebMCP prevalence logged as tool bypass rate (first-attempt success), amortized f=10 and f=100 (prevalence *100/ f). Routing includes param-slot-count tie-break + recalibrated confidence 0.95/0.85.

**B3. Honest cost instrumentation (replaces pre-2.0 invalid proxies):**
- Per-trajectory-reset sum-counter: M_total(task) = resolve + bind + verify + freshness_check + browser_steps (each counted per attempt, reset at trajectory start). Sum across 40 tasks → M_total_f10 amortized (sum / min(f,N) with f=10) and M_total_f100 (f=100). No `n*3200`, no `f*6.0`, no Gaussian jitter. Logged per task; total and per-channel breakdowns in sota_analysis.json.
- Trajectory-grouped bootstrap: B=2000 resamples with replacement on task/trajectory unit (not transition), 95% percentile CI [lower,upper] for coverage and for M_total_f10/f100 — non-degenerate width reported, variance>0; degenerate [0,0]/[1,1] flagged per prereg 12.7 and NOT counted as valid width but not invalid.
- Shuffle control |rho_shuffled| and coverage shuffle: within-family permutation of family/alias mapping, 1000 perms trajectory-grouped for coverage, 2000 family-level for WebGym duplication; residual-novelty gate rho_real 0.8656 vs |rho_shuffled|0.1592<0.20 demonstrates cost tracks residual novelty not length.
- HITL ablation NC3: DSM with HITL hook replaced by no-op/random patch must drop >=0.30 to isolate patch contribution.

## 7. Baselines table (stable IDs downstream can reuse)

| ID | Type | Purpose | Expected vs null |
|---|---|---|---|
| B-DURABLE-HF | durability | HF pin SHA d6527566... | 200 + byte-identical 64-hex |
| B-DURABLE-DOCKER | durability | Docker digest 3e8cb9b9... + reachable | digest_valid + reachable true |
| B-WEBGYM-292K-DIVERSE | dataset | 292k diverse eTLD+1 + duplication CI + sweep | >=50 eTLD+1, CI width>0, sweep range>=0.05 |
| B-TRUNCATED-20 | fragment null | [:20] truncation vs full-tree | delta_vs_truncated >=0.20 |
| B-AGENTIC-DSM | external_sota | O(1) compilation ceiling TreeWalker IR HITL | 0.80-0.99 single-channel, $0.002-0.092 80-94% compile |
| B-TRACECOMPILER-DEFUSE | external_sota | def-use ceiling | 0.25 overall body1.0 collapse |
| B-BMEM-CATALOG | external_sota | exact replay ceiling | collapses 0.0 on alias shift |
| B-SPIDER-ALIAS | spider | SPIDER alias-catalog flat vs structured | ~0.925 flat p>0.05 |
| B-SPIDER-ROUTING | spider | routing + slot-count tie-break | 1.0 degenerate on synthetic |
| B-SPIDER-WEBMCP | spider | tool bypass prevalence hybrid | 0.725 [0.575,0.85] f10 2.9 f100 0.725 |
| B-COLD-LLM | cold | floor no-memory | ~0.25 lowest ceiling |

## 8. Controls (stable IDs)

**Positive controls (must pass or MEASUREMENT_INVALID):**
- PC-A (PC-SYNTHETIC-FIXTURE): synthetic Flask product fixture at 1280x720, ~17 AX nodes fixed. Expect median AX>10, DOM>=2000, SHA before==after identical TRUE (16/16), SHA after textContent mutation != TRUE (16/16). Validates CDP AX pipeline.
- PC-B (PC-TOY-DSM): toy single-header param task compiles via DSM TreeWalker IR to 1.0 coverage blind. Validates harness not scaffolding-broken.
- PC-C (PC-WEBGYM-SANITY, gated on HF success): WebGym diverse sample sanity — >=50 eTLD+1 sample yields duplication prevalence within [0.3,0.99] and sweep monotonic (0.818 prevalence relation to 0.9479 monotonic) demonstrating pipeline not vacuous. When HF absent, PC-C marked UNAVAILABLE not failed.

**Null controls (must be computed trajectory-grouped family-level):**
- NC1-SHUFFLED: family-label permutation of duplication prevalence (WebGym, 2000 family-level perms) and coverage (40 tasks, 1000 perms). Expect |rho_shuffled|<0.20 (cost vs length), coverage shuffle mean ~ chance, gap real-shuffle >=0.20, shuffled p>0.05 while real p<0.05 for structured mechanisms. SPIDER-ALIAS expected flat p>0.05 (0.626) — operational gate is |rho_shuffled|<0.20 not p.
- NC2-TRUNCATED (B-TRUNCATED-20): tokens[:20] vs full-tree sensitivity delta_vs_truncated >=0.20 (full-tree non-vacuous); shuffled version <0.05. On synthetic fixture truncated sensitive, on real WebArena pages full sensitive truncated insensitive (delta 0.6667).
- NC3-NO-HITL: Agentic DSM with HITL hook no-op/random must drop coverage >=0.30 vs HITL (empirical 0.75->0.25 drop 0.50).

## 9. Metrics (stable names for result.json / audit.json)

Census & deterministic constructibility & WebGym (Module A):
- M_A_MANIFEST_SHA256 (hex, expect d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30), M_A_MANIFEST_BYTES (int), M_A_DOCKER_DIGEST_VALID (bool 64 hex), M_A_CENSUS_TOTAL_TASKS (int 700-812), M_A_FAMILIES_GE3 (int >=30), M_A_SHOPPING (int), M_A_PRODUCT_PAGE_FAMILIES_COUNT (int), M_A_PRODUCT_PAGE_FAMILIES_LIST (list), M_A_DETERMINISTIC_S1 (list 10 ints), M_A_DETERMINISTIC_S2 (list 10 ints), M_A_CONSTRUCTIBLE_LIST (list), M_A_CONSTRUCTIBLE_COUNT (int, gate >=10), M_A_ANCHORING_PER_FAMILY (dict node_count, SHA identical/mutated), M_AX_VALID_CAPTURES (int), M_AX_FAMILIES_FOUND (int), M_AX_NODES_MEDIAN (int >10), M_AX_NODES_MIN (int), M_DOM_BYTES_MEDIAN (int >=2000), M_SHA_STABILITY_IDENTICAL (bool), M_SHA_MUTATION_CHANGED (bool), M_AX_RICHER_BBOX_VIA_EVALUATE (bool, expect true 13/13), M_WEBGYM_DIVERSE_N (int >=50 or null), M_WEBGYM_DIVERSE_ETLD_PLUS1_DISTINCT (int), M_WEBGYM_DUPLICATION_PREVALENCE (float), M_WEBGYM_DUPLICATION_CI_LOWER/UPPER (float, family-level B=2000), M_WEBGYM_THRESHOLD_SWEEP_0818 (float), M_WEBGYM_THRESHOLD_SWEEP_09479 (float), M_WEBGYM_SWEEP_RANGE (float >=0.05), M_WEBGYM_SWEEP_MONOTONIC (bool)

Blind reproduction & economics (Module B):
- M_COV_AGT_DSM, CI_LOWER/UPPER, M_COV_TRACE, M_COV_BMEM, M_COV_SPIDER_ALIAS/ROUTING/WEBMCP/COLD (prop, per-channel split header/body/auth/mixed)
- M_TOTAL_F10_AGT_DSM, TRACE, BMEM, SPIDER_ALIAS/ROUTING/WEBMCP, COLD with CI_LOWER/UPPER each (honest sum-counter B=2000)
- M_TOTAL_F100_* same amortized f=100
- M_COST_USD_AGT_DSM_MEAN, CI, TOTAL_40, N_PATCH_TASKS
- M_RHO_REAL, M_RHO_SHUFFLED, M_RHO_SHUFFLED_GATE_ABS_LT_0_20 (bool), M_RHO_P, M_FALSE_ACCEPT (structural 0.0)
- M_PREVALENCE_WEBMCP_TOOL_BYPASS, CI, AMORTIZED_F10, AMORTIZED_F100
- M_HITL_DROP, M_HITL_DROP_GE_0_30 (bool), M_AX_DELTA_TRUNCATED

## 10. Measurement validity gates (MV1-MV9 — see spec.json)

Failure on any mandatory MV is MEASUREMENT_INVALID, not falsification (exception: MV5 WebGym diverse clause may be documented UNAVAILABLE with 2 genuine 401 attempts when HF_TOKEN absent). Detailed gates:
- MV1 >=2 genuine attempts per durable source (HF WebArena 812, HF WebGym 292k, Docker) with logged evidence (URL/status/bytes/sha256/64-char digest, timeout >=300s or docker load fallback).
- MV2 manifest SHA d6527566... + Docker digest 64 hex explicit, cross-source equality not assumed.
- MV3 versions/viewport/CDP path/grammar hash live recomputed, body regex <body[^>]*>.*?</body> DOTALL present, fallback snapshot = invalid.
- MV4 deterministic Random(35725763380).sample x2 + get_task_start_url __SHOPPING__ expansion + product-subtree anchoring node_count>1 distinct SHA on canonical path 136/145/196/222 at 1280x720 with both samples logged.
- MV5 WebGym diverse >=50 eTLD+1 family-level B=2000 duplication CI + threshold sweep 0.818-0.9479 range>=0.05 when HF succeeds; UNAVAILABLE with 2 attempts logged when HF 401, not invalid.
- MV6 synthetic 40-task deterministic orthogonal split preserved.
- MV7 honest per-trajectory-reset sum-counters only, trajectory-grouped B=2000, no n*3200/jitter, degenerate CIs flagged not counted.
- MV8 blind implementation per recipe, per-task logs for all 40*7, harness sha logged + byte-identical re-run.
- MV9 provenance path+sha256 for every durability/cost path captured.

Representation loss disclosed: DOM outerHTML normalized before hash loses scroll/visual computed style beyond anchored bbox; AX tree at 1280x720 loses mobile variance; synthetic alias-OOD loses real site DOM volatility, auth/session expiry, network latency — bounded synthetic ceiling stated.

## 11. Decision rule (frozen, three-way — precedence A > B > C)

**A. MEASUREMENT_INVALID** if any mandatory MV1-MV4/MV6-MV9 fails (fewer than 2 genuine attempts, missing manifest SHA d6527566... / digest 3e8cb9b9..., pip freeze empty or version/viewport mismatch, fallback AX snapshot, body regex absent, deterministic sampling not executed, honest-cost proxy or ungrouped CI, missing provenance). MV5 alone defaults to UNAVAILABLE not INVALID when HF 401 after 2 attempts. Then no SURVIVES/FALSIFIED inference.

**B. SURVIVES_CURRENT_TEST** iff A passes (with MV5 either PASS or documented UNAVAILABLE) AND: H_A_SURVIVES: (SRC_HF_SUCCESS OR SRC_DOCKER_SUCCESS) with census artifact manifest_sha256=d6527566... total 700-812 families_ge3>=30 AND deterministic constructibility >=10 distinct product families with anchoring true + SHA stability both directions TRUE and CDP 1280x720 median AX>10 median DOM>=2000 on canonical path families 136/145/196/222 plus WebGym diverse >=50 eTLD+1 with family-level B=2000 duplication CI non-degenerate and sweep range>=0.05 when HF succeeds (or explicitly unavailable) AND H_B_SURVIVES: all three external baselines executed blind on 40 alias-OOD with per-task logs, coverage point estimates + trajectory-grouped 95% CIs interior non-degenerate for DSM/ALIAS (degenerate BMEM/ROUTING/WEBMCP flagged not counted), honest M_total_f10/f100 with CIs, |rho_shuffled|<0.20, SPIDER baselines measured identically for Pareto, WebMCP prevalence 0.725 CI measured, PC-A/PC-B passed (PC-C pass when HF succeeds).

Degenerate signals [0,0]/[1,1] variance0 explicitly NOT counted as valid width per prereg 12.7; single-family degenerate full-page LCP 0.0 variance explicitly NOT counted as valid AX signal.

**C. FALSIFIED_IN_SETTING** if A passes (measurement valid) but B thresholds fail after genuine attempts: e.g., durable sources 401/404 persistent, or deterministic sampling still yields only 4 product families (136/145/196/222) not >=10 (bounded FALSIFIED for 10-family gate), or AX median <=10 / SHA false, or WebGym diverse <50 or sweep range<0.05 when HF succeeds, or external baselines fail blind or indistinguishable from NC1/NC2/NC3 shuffles (coverage within null CI, |rho|>=0.20, delta_vs_truncated<0.05, HITL drop<0.30). Outcome MIXED if one module survives and the other falsified.

All thresholds frozen; single-family or degenerate full-page LCP 0.0 variance explicitly NOT counted as valid.

## 12. Validity threats and mitigations

- **Network/HF_TOKEN variability:** mitigated by >=2 attempts each source + HF_TOKEN true/false logged; MV5 UNAVAILABLE does not penalize Docker pin; cross-source equality not assumed.
- **Docker pull size/time 5.4GB:** mitigated by >=300s timeout + docker load cached tar/ghcr fallback; script-imposed 8s cap is MEASUREMENT_INVALID per parent audit FIX-A.
- **Determinism (PYTHONHASHSEED):** mitigated by random.Random(35725763380) integer seed (not hash) for within-family sampling and deterministic synthetic generation seed + hash.
- **Body regex miss:** grammar sha256 without <body[^>]*>.*?</body> DOTALL fails MV3 — must repair file and re-verify live.
- **Deterministic sampling fidelity:** must be exactly `random.Random(35725763380).sample(sorted_families_ge3, 10)` x2 with identical seed reset; any other seed or sorted order is MEASUREMENT_INVALID.
- **Anchoring vs bbox confusion:** AXNode.boundingBox 0/16 is Chromium protocol fact — replacement is anchored getBoundingClientRect scan with node_count>1; MV4 requires anchored count, not AX field.
- **Threshold sweep definition:** Jaccard/template similarity must be documented; sweep monotonic direction must be documented; range >=0.05 is replacement gate for exhaustive LFS.
- **Synthetic orthogonal leakage:** header/body/auth channels independently parameterized; generation script asserts cross-channel independence; mixed tasks combine all three.
- **Honest cost contamination:** per-trajectory reset counters prevent n*3200 inflation; trajectory-grouped family-level bootstrap prevents transition-independence pseudoreplication; residual-novelty rho>=0.60 gate distinguishes novelty from length.
- **Blindness leakage:** external baselines coded from paper recipe docs before seeing synthetic labels; code hash logged pre-run; same 40-task split for all baselines.
- **Degenerate CI misinterpretation:** prereg 12.7 variance0 width0 [0,0]/[1,1] flagged not counted as valid-width — interior estimators DSM/ALIAS drive Pareto comparison.

## 13. Estimated cost and information gain

Cost: 3-5h runner (docker pull 5.4GB if not cached 2x attempts 300s or load fallback 15-30min; WebGym fetch 15min if HF_TOKEN valid; deterministic family sampling + get_task_start_url expansion + anchored AX probe on >=10 families 20-30min; synthetic 40-task x7 baselines 280 executions + B=2000 bootstrap + sweep 60-90min). Network: HF manifests + Hub digest. Tokens: none (synthetic harness only). USD $3-5 GH runner.

Information gain: High — Director-ranked gating for entire product thread. First test of specified deterministic family constructibility protocol decides whether 22-deep Intel tunnel's 4-family ceiling is census hard ceiling or protocol artifact (unblocking/removing Graph >=10-family hold-out and Physics |S|>=16). WebGym diverse 292k duplication CI with family-level B=2000 and 0.818-0.9479 threshold sweep decides whether 567MB LFS exhaustive enumeration is replaceable and whether single-store 0.9479 duplication is vacuous without site diversity. Honest Pareto with rho>=0.60 vs O(1) $0.002-0.092 compilation and 0.725 WebMCP prevalence decides whether SPIDER must beat compilation ceiling or pivot to hybrid tool-bypass dispatch — directly answering Global Director comparative reasoning and preventing another repeat of same AX substrate.

## 14. Consequences

**If SURVIVES:** Census artifacts (pinned manifest SHA d6527566... + Docker digest + WebGym diverse duplication sweep) become Codex dependencies; Graph next can attempt deterministic Random(35725763380).sample parameterized hold-out on durable pin; Product can run Stagehand/WebMCP vs compilation Pareto with honest costs to decide promotion; Intel census substrate considered delivered (artifact dependency promotion, not kernel code). C-CROSSSITE advances toward EXPERIMENTAL at diverse-holdout ceiling, C-RESIDUAL-NOVELTY/C-PRODUCT-ECON gain honest baseline.

**If FALSIFIED:** Deterministically proven that pinned 812-task census contains only 4 constructible product families (136/145/196/222) even with specified anchoring — Graph >=10-family hold-out remains BLOCKED on this pin and must select alternative census (WebMall/Mind2Web-2 loopback, shopping_admin 184-task 42-family superset, or Mind2Web definition). If WebGym diverse <50 or sweep fails, duplication substrate remains vacuous without site diversity. If external baselines falsify at null level, O(1) ceilings not blindly transferable to alias-OOD — redesign synthetic channels/HITL model before Product economics. C-CROSSSITE stays HYPOTHESIS/EXPERIMENTAL at 4-family ceiling, C-RESIDUAL-NOVELTY/C-PRODUCT-ECON remain HYPOTHESIS. If MEASUREMENT_INVALID, no claim update; smallest repair is infra fix per MV1-MV9 and re-run identical frozen design.

**If MEASUREMENT_INVALID:** No claim update; smallest next fix is MV1-MV9 repair and re-run.

## 15. Execution plan (no outcome-bearing measurements in DESIGN)

1. Resolve durable sources: 2 genuine HF manifest GETs (WebArena 812 + WebGym 292k) with HF_TOKEN bearer + 2 docker pulls/loads with Hub digest verification, write byte-identical pin with SHA d6527566... and digest 3e8cb9b9...
2. Run census counts on pinned manifest; write derived/webarena_census.json with families_ge3 36, product_page_families [136,145,196,222], atmos.
3. Provision BrowserGym-stack (BrowserGym-core 0.14.3 AgentLab 0.4.2 Playwright 1.63.0 playwright install --with-deps, viewport 1280x720), verify pip freeze nonempty, dump AX protocol.
4. Repair grammar file to include body regex <body[^>]*>.*?</body> DOTALL + fotorama\d{6,} expanded, recompute live sha 273eafbc...
5. Execute deterministic family sampling: random.Random(35725763380).sample(sorted families_ge3,10) x2, log S1/S2; for each family probe get_task_start_url __SHOPPING__ expansion + anchored product-subtree node_count>1 + SHA both directions at 1280x720 CDP, covering canonical path 136/145/196/222 + sampled families (up to 10); also synthetic fixture PC-A x3.
6. When HF_TOKEN succeeds, fetch WebGym 292k manifest, sample >=50 diverse eTLD+1 family-grouped, compute family-level B=2000 duplication CI and threshold sweep 0.818-0.9479; else log 401 attempts as UNAVAILABLE.
7. Load/generate synthetic 40 tasks (or reuse research/intel/synthetic_alias_ood_40.json sha 6f42bc82), verify 30+10 orthogonal split.
8. Blind-run 7 baselines (3 external + 3 SPIDER + cold) on identical 40-task split with honest per-trajectory-reset sum-counters; collect per-task logs 280 rows + toy PC-B row.
9. Compute trajectory-grouped B=2000 95% CIs, family-level duplication CIs, sweep range, NC shuffles (1000 coverage, 2000 WebGym), NC2 truncation delta, NC3 HITL ablation.
10. Emit result.json (schema_version 1, status COMPLETE/MEASUREMENT_INVALID/BLOCKED, outcome SUPPORTS/FALSIFIES/MIXED/NOT_APPLICABLE, metrics with stable names, controls with pass/fail, artifacts path+sha256), report.md, provenance.json with all path+sha256, plus durable/threshold/sampling artifacts.

## 16. Preregistration freeze

This prereg.md together with spec.json (hashes in freeze.json) constitute the frozen design. Any analysis change after outcomes is exploratory; a new confirmatory claim requires a new prereg and untouched evidence. This design does not inspect outcome measurements; only the binding request/director mandate (CONTINUE C-CROSSSITE), parent handoff four-way carry_forward, and Codex/recent audit statistics were consulted. Never use chat history or Actions logs to transmit scientific state.
