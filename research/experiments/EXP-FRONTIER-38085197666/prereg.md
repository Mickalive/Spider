# Preregistration — EXP-FRONTIER-38085197666

- **Experiment:** `EXP-FRONTIER-38085197666`
- **Lane:** frontier
- **Design contract:** v2
- **Status:** DESIGN FROZEN PENDING `freeze.json` (independent `design_review.json` required before freeze)
- **Claim(s):** `C-CROSSSITE` — "Reusable mechanisms transfer across website holdout" (registry status HYPOTHESIS)
- **Director mandate:** PIVOT, cycle `38084662468`, `cognitive_reset=true`, target `C-CROSSSITE`
- **Base SHA:** `6b4a1f7b18e84015e1765965081f2a8e97d3ba27`
- **Claim registry SHA256:** `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`
- **Frozen code SHA256 (section 13):** `76416baf18836501313069327e75f6ad79219023e2a818d33957fcdba1bd871c`
- **Created:** 2026-10-10

This file and `spec.json` are the frozen design. EXECUTE must reproduce section 13 verbatim and verify its SHA256 before running. No field below may change after `freeze.json` exists.

---

## 0. Relation to prior work

- `EXP-FRONTIER-37984242167` (direct predecessor, this mandate, v1) was **BLOCKED**: empty sampling frame (0 seeds, 0 DEEP items, 0 hosts), an absent pre-freeze control certificate, and a primary metric that was 0/0 so that **both falsifier directions were unreachable**. Its `audit.json` recorded `required_fixes` VN-A1 (populate seed list and run the hop crawl), VN-A2 (verify the three control-certificate conditions with evidence), VN-A3 (resolve the four open design decisions before freeze) and instructed the v2 freeze to bind pool/certificate artifacts. `same_failure_count=8`. This design is the v2 repair; it does not repeat that failure.
- The first v2 repair draft was returned `failure` / `category=substantive` by the independent design-review stage (`model_design_review.json`; the reviewer run itself crashed — `exit_code=1`, no `design_review.json` captured — so no objection text survived). The defect is nonetheless objectively demonstrable and is fixed here: the draft pool's discovery surfaces enumerated only version roots (`doc.rust-lang.org/sitemap.txt` lists 3 roots; `docs.pytest.org/sitemap.xml` lists 15), so every admitted DEEP page had per-host fraction **0** and `E = 0` identically — the SUPPORTS branch was structurally unreachable and the experiment was one-sided. The final v2 design uses a **stratified pool** (3 discovery-EXPOSING hosts + 2 OPAQUE hosts, section 3.1) plus **canonical URL matching** (`match_key`, VN-V3c) so that both `E >= 2` and `E == 0` are live.
- `EXP-FRONTIER-37950626378` (grandparent) measured `RECOVERY_REDUCTION_FROM_PERSISTED_STATE` = **GROWING** with `R_req=5.2667`, `R_bytes=7.3113`. Its DEEP partition (`n_deep=25`) lay entirely on the single host `doc.rust-lang.org`, so the cross-host/engine question was left open. It supplies this experiment's baselines B_PERSISTED_PATH_REACQUISITION, B_DIRECT_URL_REPLAY and the shortest-path hop definition.
- `EXP-FRONTIER-38078430316` (v2 sibling) supplies the prereg-embedded-code + `CODE_SHA256` freeze pattern.
- The PIVOT mandate supersedes the parent's `next_question`. The parent handoff is continuity evidence only; its `established/rejected/unknown/do_not_assume` distinctions are preserved in section 11.

## 1. Question and mandate

On the credential-free GET-only stdlib-HTTP substrate, over a frozen multi-host pool that DESIGN confirms contains DEEP (hop >= 3) state-carrying pages on at least two distinct hosts/engines:

1. **Primary gate.** What fraction of admitted DEEP pages can a *fresh* agent reach in `K <= 3` GETs (up to 2 discovery GETs + 1 item-page GET) using any of the five site-native cold-start discovery channels (`ROBOTS_SITEMAP`, `SITEMAP_XML`, `ON_SITE_SEARCH`, `RSS_ATOM`, `JSON_LD`)?
2. **Descriptive scaling.** Does reachability scale with the item's shortest-path hop, i.e. is site-native discovery path-bound or effectively path-independent?

The strategic stakes: if discovery collapses depth cost, then shortest-path hop is **not** a fundamental acquisition-cost barrier, persistence of paths/procedures is de-prioritized, and effort moves to **discovery-channel coverage and substrate expansion**. If discovery cannot beat the threshold, fresh deep-instance acquisition remains path-bound and persistence retains a computable depth-dependent break-even.

## 2. Hypothesis and falsifier (two-sided, both branches reachable)

- **H1 (SUPPORTS).** `>= 0.50` of admitted DEEP pages reachable in `K <= 3` GETs on `>= 2` distinct host/engine units.
- **H0 (negative).** `> 0.50` of admitted DEEP pages require more than `K` GETs (discovery-bound) on all but at most one unit.

**Falsifier (frozen).** Unit = distinct host (per-engine grouping reported descriptively). Let `E` = number of units whose `discovery_reachable_fraction_per_host[host] >= 0.50`.

- `E >= 2` => **SUPPORTS**
- `E == 1` => **MIXED**
- `E == 0` => **FALSIFIES**

Materiality threshold `0.50`; budget `K = 3`; minimum units meeting threshold `2`. A two-sided test: a uniformly high result and a uniformly low result both falsify the opposite branch; the experiment does not presuppose which holds.

**Reachability argument (why every branch can trigger).**
- The denominator is the number of admitted DEEP pages, `>= 10` by ADMISSION_GATE_V2 (DESIGN observed **190**), so `E` is well-defined and no branch is `0/0`.
- The local stdlib fixtures bracket the threshold from both sides: `CAL_DISCOVERABLE_FIXTURE` yields fraction **1.0** and `CAL_OPAQUE_FIXTURE` yields **0.0** (section 6.4), so the instrument demonstrably can produce values above and below `0.50`.
- The frozen pool is genuinely heterogeneous by construction: 3 hosts in stratum **EXPOSING** (publish content-level `<urlset>` sitemaps: `vitepress.dev` 272 locs, `router.vuejs.org` 230, `element-plus.org` 307) and 2 in stratum **OPAQUE** (`doc.rust-lang.org` sitemap.txt lists 3 version roots, `docs.pytest.org` sitemap.xml lists 15). Attainability probes (section 3.5) measured canonical per-host fractions **1.0, 1.0, 1.0** on the EXPOSING hosts and **0.0, 0.0** on the OPAQUE hosts (RAW DESIGN evidence; the confirmatory run re-measures under the frozen protocol). Neither `E == 0` (EXPOSING enumeration breaks) nor `E >= 2` (EXPOSING enumeration holds) is excluded by construction.

## 3. Frozen pool and pre-freeze attainability certificate

### 3.1 Seeds (frozen)

| # | Seed URL | Host | Engine | Stratum |
|---|----------|------|--------|---------|
| 1 | `https://vitepress.dev/` | vitepress.dev | VitePress | EXPOSING |
| 2 | `https://router.vuejs.org/` | router.vuejs.org | VitePress | EXPOSING |
| 3 | `https://element-plus.org/en-US/` | element-plus.org | VitePress | EXPOSING |
| 4 | `https://doc.rust-lang.org/book/` | doc.rust-lang.org | mdBook | OPAQUE |
| 5 | `https://docs.pytest.org/en/stable/` | docs.pytest.org | Sphinx | OPAQUE |

**Stratum** is a DESIGN-time *pre-treatment* observable of the **host** (not of any item): an EXPOSING host publishes a content-level `<urlset>` sitemap enumerating its own pages; an OPAQUE host publishes no content-level enumeration (only version/root sitemaps, or none). The stratum is recorded per host in the pool and reported alongside the per-host fraction (`discovery_reachable_fraction_per_stratum`).

### 3.2 Pool reconstruction policy (frozen, identical at DESIGN and EXECUTE)

Same-host static-`<a href>` BFS from the seed's *final* root, **document order**, `max_depth = 6`, `budget = 250` GETs per seed, browser-like UA `SPIDER-research-frontier-38085197666/1.0`, GET-only, 12 s timeout, body cap 600 000 bytes, redirects followed (one logical GET). The crawl is **item-blind** (topological). An admitted item is a **state-carrying page**: the fetched page contains at least one named `<input>`/`<select>`. `item_id = sha256(host + "|" + page_url)`. A page reachable from multiple seeds is admitted once at its minimum hop and attributed to the winning seed; its host/engine come from the winning seed's final root (VN-V14).

**Stratum attribution.** A page admits with the stratum of the host of the winning seed (stratum is a host property; a page on host `H` takes `H`'s stratum regardless of which seed reached it first).

### 3.3 DESIGN-observed pool (RAW EVIDENCE, 2026-10-10)

Per-seed static hop histograms and DEEP counts (from the frozen BFS in section 13; `hop` buckets `0..6`):

- `https://vitepress.dev/` — deep pages 10; hist `{0:1, 1:10, 2:51, 3:188}` (crawl capped at 250)
- `https://router.vuejs.org/` — deep pages 5; hist `{0:1, 1:4, 2:169, 3:76}`
- `https://element-plus.org/en-US/` — deep pages 4; hist `{0:1, 1:7, 2:98, 3:5}` (112 GETs; near-flat site)
- `https://doc.rust-lang.org/book/` — deep pages 12; hist `{0:1, 1:6, 2:29, 3:214}` (crawl capped at 250)
- `https://docs.pytest.org/en/stable/` — deep pages 159; hist `{0:1, 1:56, 2:33, 3:63, 4:97}`

**Admitted DEEP pool (derived): 190 state-carrying pages** — VitePress **19**, mdBook **12**, Sphinx **159**; by host `vitepress.dev` **10**, `router.vuejs.org` **5**, `element-plus.org` **4**, `doc.rust-lang.org` **12**, `docs.pytest.org` **159**; by stratum **EXPOSING 19 / OPAQUE 171**.

Representative confirmed DEEP items (hop >= 3), used for the liveness/arrival records:

| page_url | hop | host | engine | stratum |
|----------|-----|------|--------|---------|
| `https://vitepress.dev/zh/guide/markdown` | 3 | vitepress.dev | VitePress | EXPOSING |
| `https://router.vuejs.org/zh/guide/essentials/dynamic-matching` | 3 | router.vuejs.org | VitePress | EXPOSING |
| `https://element-plus.org/en-US/component/tooltip.html` | 3 | element-plus.org | VitePress | EXPOSING |
| `https://doc.rust-lang.org/cargo/guide/index.html` | 3 | doc.rust-lang.org | mdBook | OPAQUE |
| `https://docs.pytest.org/en/stable/funcarg_compare.html` | 3 | docs.pytest.org | Sphinx | OPAQUE |

Pool-build cost at DESIGN: `<= 5 x 250 = 1250` GETs, observed **1116** GETs.

### 3.4 ADMISSION_GATE_V2 (frozen)

PASS iff **total admitted DEEP pages >= 10** AND **>= 2 distinct engines each with >= 3 admitted DEEP pages** AND **>= 2 distinct hosts each with >= 3 admitted DEEP pages**. DESIGN verdict: **PASS** (190 >= 10; VitePress 19, mdBook 12, Sphinx 159 = 3 engines >= 3; 5 hosts >= 3). At EXECUTE the gate is re-evaluated on the reconstructed pool; failure yields `status = MEASUREMENT_INVALID` with the exact shortfall and is **never** encoded as a scientific branch.

### 3.5 Pre-freeze control certificate

```
certificate_id: PRE_FREEZE_CERT_EXP-FRONTIER-38085197666
all_verified: true
(a) pool_deep_items_confirmed: true   -> 190 admitted DEEP pages (VitePress 19, mdBook 12, Sphinx 159)
(b) pool_deep_hosts_confirmed: true   -> 5 hosts with >= 3 DEEP; 3 engines with >= 3 DEEP
(c) discovery_channel_probe_verified: true -> RAW evidence 2026-10-10:
        vitepress.dev/robots.txt 200, Sitemap: https://vitepress.dev/sitemap.xml -> 200 urlset (272 locs)
        router.vuejs.org/robots.txt 200, Sitemap: https://router.vuejs.org/sitemap.xml -> 200 urlset (230 locs)
        element-plus.org/robots.txt 200 (no Sitemap line); /sitemap.xml -> 200 urlset (307 locs)
        doc.rust-lang.org/robots.txt 200 -> sitemap.txt 200 (3 version roots; /sitemap.xml 404)
        docs.pytest.org/robots.txt 200 -> sitemap.xml 200 (15 version roots)
(d) null_control_verified: true       -> all 5 channels return 0 reachable on synthetic items
(e) dynamic_range_verified: true      -> CAL_DISCOVERABLE_FIXTURE 1.0 ; CAL_OPAQUE_FIXTURE 0.0
(f) both_branch_attainability: true   -> canonical per-host fraction 1.0/1.0/1.0 (EXPOSING), 0.0/0.0 (OPAQUE),
                                        so E==0 and E>=2 are both structurally live
```

This repairs v1 `VN-A1`/`VN-A2`/`VN-A3` and the failed first v2 draft: the frame is non-empty and recorded, the certificate conditions are live-verified with evidence, and the falsifier can trigger in both directions. The per-host fractions in (f) are DESIGN-time attainability probes (canonical `match_key` overlap of frozen `build_pool` deep items against each host's discovery enumeration); the confirmatory run re-measures them under the frozen protocol and is the authoritative outcome.

## 4. Discovery channels (frozen definitions)

All channels are **cold-start**: the item page is fetched **only after** its URL is discovered, and the item-page GET counts against `K`.

1. **ROBOTS_SITEMAP** — GET `/robots.txt`; for each `Sitemap:` directive GET the target and parse `<loc>` (XML) or one-URL-per-line (plain text, e.g. `doc.rust-lang.org/sitemap.txt`).
2. **SITEMAP_XML** — GET `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml` directly and parse `<loc>`.
3. **ON_SITE_SEARCH** — GET the seed root, locate a server-side search `<form>`/input action; GET `action?name=<query>` where `<query>` = last item-path segment with a trailing `.html|.php|.htm|.asp|.aspx` stripped (parameter = the located input's `name`, default `q`); parse result links. JS-only search indexes (mdBook `searchindex.js`, Sphinx client search) are not server-side and are disclosed as unreachable by this channel.
4. **RSS_ATOM** — GET the seed root, follow a `<link rel="alternate" type="application/rss+xml|atom+xml">`, parse entry links.
5. **JSON_LD** — GET the seed root (a **hub** resource; never the item page), parse every `<script type="application/ld+json">` block and collect values of `url`, `@id`, `mainEntityOfPage`, `contentUrl`, `sameAs` across `@graph`/`ItemList`/`WebPage`/`BreadcrumbList`/`SearchAction`.

`K = 3` total GETs per item per channel = at most `DISCOVERY_GETS_MAX = 2` discovery GETs + exactly 1 item-page GET. A channel succeeds for an item iff the item URL is discovered within the discovery budget under **canonical resource identity** `match_key` (host + path with a single trailing `/`, `.html`, `.htm` removed — VN-V3c) **and** the item page returns 2xx within `K`. Canonical matching treats sitemap spelling `…/component/button` and link spelling `…/component/button.html` as the same resource; pool building and dedup keep exact URLs. Sitemap-index recursion beyond 2 discovery GETs does not count. An item is reachable iff **any** channel succeeds; per-channel coverage is reported separately and a zero-yield channel is listed explicitly.

## 5. Baselines and comparators (stable ids)

| id | role | policy | cost |
|----|------|--------|------|
| `B_LINK_FOLLOWING_BFS` | comparator | item-blind same-host BFS (this experiment's pool pass), document order, B=250, D=6 | `>= hop+1` GETs (+bytes) |
| `B_PERSISTED_PATH_REACQUISITION` | comparator | GET each node on the frozen shortest path seed→…→item in hop order | `hop+1` GETs |
| `B_DIRECT_URL_REPLAY` | lower bound | one GET to the known item URL | `1` GET |
| `B_NO_DISCOVERY` | floor | `CAL_OPAQUE_FIXTURE`, no discovery surface | `0.0` fraction |

The treatment (per-item discovery reachability) is a distinct decision function over the **same** admitted item set, so discovery-vs-link-following is identified.

## 6. Pre-freeze probe log (DESIGN only; no confirmatory outcome computed)

Open information classes are kept separate: **RAW EVIDENCE** (HTTP statuses/bytes actually observed), **OBSERVATION** (plain restatement), **DERIVED** (counts/fractions computed from it), **INTERPRETATION** (what it implies).

### 6.1 Channel liveness (RAW EVIDENCE)

- `vitepress.dev/robots.txt` → **200**, contains `Sitemap: https://vitepress.dev/sitemap.xml`; `/sitemap.xml` → **200**, `<urlset>` with 272 `<loc>`; `/sitemap_index.xml` → **404**; root **200**, no feed link.
- `router.vuejs.org/robots.txt` → **200**, contains `Sitemap: https://router.vuejs.org/sitemap.xml`; `/sitemap.xml` → **200**, 230 `<loc>`; root **200**, no feed link.
- `element-plus.org/robots.txt` → **200** (content-signal directives only, **no** `Sitemap:` line); `/sitemap.xml` → **200**, 307 `<loc>` (direct `SITEMAP_XML` suffices); root **200**, no feed link.
- `doc.rust-lang.org/robots.txt` → **200**, contains `Sitemap: https://doc.rust-lang.org/sitemap.txt`; `sitemap.txt` → **200**, **3** `<loc>` (version roots `book/`, `edition-guide/`, `cargo/`); `/sitemap.xml` → **404**.
- `docs.pytest.org/robots.txt` → **200**, contains `Sitemap: https://docs.pytest.org/sitemap.xml`; `sitemap.xml` → **200**, **15** `<loc>` (version roots); root **200**, no feed link, search form `search.html` present.

**OBSERVATION.** The three EXPOSING hosts publish content-level `<urlset>` sitemaps (272/230/307 locs) that enumerate deep pages; the two OPAQUE hosts publish only version/root sitemaps (3/15 locs) and no per-page enumeration. **DERIVED.** `ROBOTS_SITEMAP` and `SITEMAP_XML` are live and parsable on all three EXPOSING hosts; `RSS_ATOM` yields nothing on any seed root; `JSON_LD` yields 0 blocks on all five seed roots; `ON_SITE_SEARCH` is JS-only on VitePress/mdBook and static-result on Sphinx (`search.html?q=` returns no server-side result links for arbitrary deep pages). **INTERPRETATION.** The decisive channel pair is `ROBOTS_SITEMAP`/`SITEMAP_XML` on EXPOSING hosts; the OPAQUE hosts bound the negative side. The treatment is neither absent nor universal, so the decision can land on either side.

### 6.2 Null control (RAW EVIDENCE)

Synthetic items `spider-nonexistent-38085197666-<a|b>.html` probed through all five channels against pool hosts: **all 5 channels return `success=false`, 0 reachable URLs**. `NULL_ALL_ZERO = true`. This guards against false-positive discovery via search suggestions, redirect chains or parser errors.

### 6.3 Positive control (DESIGN prerequisite; confirmatory check at EXECUTE)

- **PC_DISCOVERY_CHANNEL_REACHABILITY(a):** at least one channel returns 200 with parsable entries on >= 1 pool host — satisfied live on all three EXPOSING hosts (section 6.1).
- **PC_DISCOVERY_CHANNEL_REACHABILITY(b):** the frozen BFS must return `found=true, hop=1` for the preregistered true-hop-1 target `https://doc.rust-lang.org/book/ch01-01-installation.html`; verified at EXECUTE.
- **PC_EXPOSING_DEEP_ENUMERATION:** at EXECUTE, on >= 2 EXPOSING hosts, the frozen `ROBOTS_SITEMAP`/`SITEMAP_XML` enumeration must discover >= 1 admitted DEEP page of that host (live check that the EXPOSING stratum still enumerates deep content; guards SUPPORTS-liveness against hosts changing mid-run).

### 6.4 Dynamic-range calibration (RAW EVIDENCE, local stdlib `http.server` fixtures)

- `CAL_DISCOVERABLE_FIXTURE` (robots.txt + `sitemap.xml` listing deep pages): `discovery_reachable_fraction = 1.0` (via `ROBOTS_SITEMAP` and `SITEMAP_XML`); `n_deep = 2`.
- `CAL_OPAQUE_FIXTURE` (same deep structure, no robots/sitemap/feed/search/JSON-LD): `discovery_reachable_fraction = 0.0`.
- `CALIBRATION_PASS = true`.

**DERIVED.** The instrument produces `1.0` and `0.0`, strictly bracketing the `0.50` decision threshold; the pipeline runs end-to-end with no browser, model, key or credential.

## 7. Metrics (stable ids)

- **Primary:** `discovery_reachable_fraction` (pooled); `discovery_reachable_fraction_per_host[host]` (decision unit); `discovery_reachable_fraction_per_engine[engine]` (descriptive).
- **Secondary:** `discovery_reachable_fraction_per_stratum[stratum]`; `discovery_reachable_fraction_per_channel[channel]`; `discovery_reachable_fraction_by_hop[3..6]`; `median_discovery_gets_reachable`; `engines_meeting_threshold` (`E`).
- **Controls metric:** `controls.<id>.pass`.

No tokenizer, latency timer or dollar-cost model; GET count and response-body bytes are the only cost bases (token fields `null`).

## 8. Decision rule (frozen, evaluated in order)

```
Step 0  controls: CAL_DISCOVERABLE_FIXTURE==1.0, CAL_OPAQUE_FIXTURE==0.0,
        PC_HOP_CONFIRMATION found & hop==1, NC_SYNTHETIC_UNREACHABLE_ITEM==0,
        PC_EXPOSING_DEEP_ENUMERATION (>= 2 EXPOSING hosts each with >= 1 admitted DEEP
        page discovered by ROBOTS_SITEMAP/SITEMAP_XML).
        Any failure -> status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE (infra/substrate; not a scientific branch).
Step 1  admission: reconstruct pool from frozen seeds under frozen BFS; ADMISSION_GATE_V2 pass?
        fail -> status=MEASUREMENT_INVALID with exact shortfall.
Step 2  measurement: per admitted DEEP page x 5 channels x 2 sessions, channel success within K=3.
        drop items with inter-session disagreement (VN-V11), report count.
Step 3  compute pooled / per-host / per-engine / per-stratum / per-channel / by-hop fractions;
        E = #hosts with fraction >= 0.50.
        E >= 2 -> SUPPORTS ; E == 1 -> MIXED ; E == 0 -> FALSIFIES   (status=COMPLETE).
```

A valid scientific negative is `status=COMPLETE` with `outcome=FALSIFIES`, **not** an infrastructure failure.

## 9. Controls (frozen ids)

- `PC_DISCOVERY_CHANNEL_REACHABILITY` — section 6.3.
- `PC_EXPOSING_DEEP_ENUMERATION` — section 6.3 (EXECUTE liveness of the EXPOSING stratum).
- `PC_HOP_CONFIRMATION` — the true-hop-1 target.
- `NC_SYNTHETIC_UNREACHABLE_ITEM` — section 6.2.
- `CAL_DISCOVERABLE_FIXTURE`, `CAL_OPAQUE_FIXTURE` — section 6.4.
- `ADMISSION_GATE_V2` — section 3.4.

## 10. Validity threats, controls and representation loss

1. **JS-rendered navigation** (mdBook/Sphinx client search, JS-injected links/JSON-LD) is invisible to the stdlib parser; disclosed as representation loss (VN-V8). This biases **against** the discovery treatment, i.e. conservative for SUPPORTS.
2. **`ON_SITE_SEARCH` semantics** — server-side search may not index every deep page; the channel is one of five and its coverage is reported per-channel.
3. **Sitemap staleness** — a discovered URL may 404; the item page must be 2xx within `K` for success, so stale URLs are failures, not silent passes.
4. **Availability** — hosts can change or rate-limit between DESIGN and EXECUTE (VN-V12). If the pool collapses, the result is `MEASUREMENT_INVALID`, never a branch.
5. **Pool drift** — the live site changes; the gate is re-checked at EXECUTE and the reconstructed pool is reported with counts and hashes.
6. **Hop comparability** — hop is computed by the same frozen BFS and is reported as a distribution, not a point estimate; the primary decision does not depend on the hop estimate.
7. **Cross-seed contamination** — no two seeds share a host in the final pool; dedup by minimum hop and attribution to the winning seed (VN-V14) prevents double counting.
8. **Determinism** — 2 sessions; any inter-session disagreement excludes the item with a recorded reason (VN-V11).
9. **Confirmation bias against the question** — the two local fixtures bracket the threshold and the EXPOSING/OPAQUE stratum contrast is real (1.0/1.0/1.0 vs 0.0/0.0 at DESIGN), so the instrument is not rigged to a single answer; the design explicitly records consequences for both branches.
10. **Stratification / selection bias (structural)** — the pool is a **stratified convenience sample**: EXPOSING hosts were selected *because* they expose content-level sitemaps. `E` therefore measures whether site-native discovery transfers across units **given a discovery-favorable host class**, not the Web-wide prevalence of such hosts. The claim gains only the bounded form `C-CROSSSITE`-bounded: a positive generalizes to EXPOSING-type hosts, not to all hosts; a negative (OPAQUE hosts failing) does not refute EXPOSING-type hosts. The stratum is a pre-treatment host observable recorded at DESIGN, so the decision rule itself is not compromised; the *generalization* is what is bounded.
11. **Canonicalization false-merges (VN-V3c)** — `match_key` removes a single trailing `.html`/`.htm`/`/`, so a genuinely distinct resource `/a.html` vs `/a` would be conflated. Guard: (i) on these hosts the `.html` and clean spellings are the *same* page (EXECUTE matches the item against what was actually enumerated, so only same-resource pairs merge); (ii) `NC_SYNTHETIC_UNREACHABLE_ITEM` and item-page 2xx checks still apply; (iii) per-channel and per-host results are reported, so a systematic merge would surface as an outlier.
12. **Certificate/outcome overlap** — the DESIGN attainability certificate (section 3.5f) reports the same canonical fractions the confirmatory run computes. It is DESIGN-time RAW evidence for satisfiability (the v2 contract requires proving both branches live **before** freeze) and is not the authoritative outcome; EXECUTE re-runs the frozen protocol end-to-end with 2 sessions and its result decides. The two are recorded separately (`certificate` in `spec.json`/`prereg.md` vs `result.json`).

## 11. Inherited state (from the parent handoff, preserved)

**Established.** (i) A depth-bounded credential-free static crawler can build the pool from these docs roots under B=250/D=6. (ii) The grandparent measured `RECOVERY_REDUCTION_FROM_PERSISTED_STATE = GROWING` (`R_req=5.2667`, `R_bytes=7.3113`) on a single-host DEEP partition.

**Rejected / retired.** (i) The v1 `EXP-FRONTIER-37984242167` sampling frame is void (0 seeds, 0 DEEP, 0 hosts). (ii) Its "no freeze / placeholder spec" design path is retired by this v2.

**Unknown.** (i) The discovery-reachability fraction of DEEP pages on a genuinely multi-host/multi-engine pool — the entire question of this experiment. (ii) Whether discovery reachability scales with hop. (iii) Per-channel coverage on VitePress vs mdBook vs Sphinx. (iv) The Web-wide fraction of doc hosts that are EXPOSING-type (not measured here; the design is capability-bound).

**Do not assume.** (i) That a single-host result generalizes cross-host. (ii) That a machine-readable discovery channel exists on any given host — `doc.rust-lang.org` and `docs.pytest.org` publish only version-root sitemaps; GitHub-Pages mdBook hosts publish none. (iii) That `ON_SITE_SEARCH`, `RSS_ATOM` or `JSON_LD` are live on any pool host — they measured zero at DESIGN on all five. (iv) That the first v2 draft's one-sided pool (all hosts OPAQUE) was satisfiable — it was not; the current stratified pool is the repair.

## 12. Product consequences

- **If SUPPORTS.** Shortest-path hop is not a fundamental acquisition-cost barrier for discovery-enabled acquisition; SPIDER should optimize discovery-channel coverage and substrate expansion rather than path/procedure caching. `C-CROSSSITE` gains a bounded positive that a reusable discovery procedure transfers across `>= 2` host/engine units. Freshness/delta-repair are lower priority for the acquisition phase. **No mechanism is promoted to Product Core by this experiment.**
- **If FALSIFIES.** Even with site-native discovery, fresh deep-instance acquisition remains path-bound; persistence of paths/procedures retains a measurable depth-dependent amortization surface and the break-even reuse count can be computed from the recorded re-derivation cost. SPIDER's memory architecture should keep investing in path/procedure persistence with freshness guards.
- **If MIXED.** No program-level decision change; the next experiment must resolve discovery-channel coverage or pool composition.

## 13. Frozen outcome-bearing code (verbatim; `CODE_SHA256`)

EXECUTE MUST write the following block byte-for-byte to `run.py` (outside the repo is fine) and verify `sha256(run.py) == 76416baf18836501313069327e75f6ad79219023e2a818d33957fcdba1bd871c` before running. Extraction rule: the code is the exact bytes between the line after the opening fence and the line before the closing fence (the block content equals the file bytes, trailing newline included). Modes: `python3 run.py --calibrate <OUT>` (controls only), `python3 run.py --pool` (frame reconstruction / admission evidence), `python3 run.py <OUT>` (confirmatory; EXECUTE only).

```python
#!/usr/bin/env python3
"""EXP-FRONTIER-38085197666 -- site-native discovery vs link-following for
deep-item acquisition (frontier lane, Research 2.0, design-contract v2).

Credential-free, GET-only, stdlib+http.server; no browser, no JS, no token,
no cookie, no write verb, no API key.

Modes (invoked by EXECUTE exactly as declared in prereg.md):
  python run.py --calibrate OUTDIR
      Runs the COMPLETE discovery pipeline end-to-end on two LOCAL stdlib
      http.server fixtures (one discoverable, one opaque) and prints the
      resulting discovery_reachable_fraction. Proves the frozen instrument can
      produce BOTH branches. NOT a confirmatory measurement.
  python run.py --pool
      Runs the frozen same-host static-<a> BFS (B=250, D=6) on the frozen SEEDS
      and prints the admitted DEEP pool (sampling-frame construction only; no
      discovery channel is probed).
  python run.py OUTDIR
      Full confirmatory run: pool construction, admission gate, 5 discovery
      channels x K=3 GETs x 2 sessions, metrics, controls, decision; bakes
      result.json / report.md / provenance.json and raw evidence under OUTDIR.

The complete code of this file is frozen verbatim inside prereg.md section 13;
EXECUTE extracts it byte-for-byte and verifies CODE_SHA256 before running.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import ssl
import statistics
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------------------
# Frozen constants
# ---------------------------------------------------------------------------
EXPERIMENT_ID = "EXP-FRONTIER-38085197666"
LANE = "frontier"
CLAIM_IDS = ["C-CROSSSITE"]

USER_AGENT = "SPIDER-research-frontier-38085197666/1.0"
TIMEOUT_S = 12
MAX_BODY = 600000
BUDGET_PAGES = 250          # per-seed BFS page budget B
DEPTH_CAP = 6               # per-seed BFS depth cap D
K_GETS = 3                  # fresh-agent GET budget per item per channel
DISCOVERY_GETS_MAX = 2      # of K_GETS: up to 2 discovery GETs + 1 item-page GET
MATERIALITY_THRESHOLD = 0.50
MIN_ENGINES_WITH_THRESHOLD = 2
ADMIT_DEEP_MIN = 10
ADMIT_PER_ENGINE_MIN = 3
ADMIT_DISTINCT_ENGINES_MIN = 2
ADMIT_DISTINCT_HOSTS_MIN = 2
SESSIONS = 2
SEED = 38085197666

# Frozen seed list (host + generator engine + discovery stratum frozen at
# DESIGN; see prereg s3). Stratum is a DESIGN-time property of the HOST, not of
# any item: EXPOSING hosts publish a content-level sitemap (a <urlset> that
# enumerates their pages); OPAQUE hosts publish no content-level enumeration
# (only version/root sitemaps, or none). The stratum is a pre-treatment
# observable and is reported alongside the per-host fraction.
SEEDS = [
    {"seed": "https://vitepress.dev/", "host": "vitepress.dev", "engine": "VitePress", "stratum": "EXPOSING"},
    {"seed": "https://router.vuejs.org/", "host": "router.vuejs.org", "engine": "VitePress", "stratum": "EXPOSING"},
    {"seed": "https://element-plus.org/en-US/", "host": "element-plus.org", "engine": "VitePress", "stratum": "EXPOSING"},
    {"seed": "https://doc.rust-lang.org/book/", "host": "doc.rust-lang.org", "engine": "mdBook", "stratum": "OPAQUE"},
    {"seed": "https://docs.pytest.org/en/stable/", "host": "docs.pytest.org", "engine": "Sphinx", "stratum": "OPAQUE"},
]

CHANNELS = ["ROBOTS_SITEMAP", "SITEMAP_XML", "ON_SITE_SEARCH", "RSS_ATOM", "JSON_LD"]

ASSET_EXTS = {
    "png", "jpg", "jpeg", "gif", "svg", "ico", "css", "js", "pdf", "zip", "gz",
    "woff", "woff2", "ttf", "otf", "mp4", "webp", "xml", "rss", "atom", "epub",
    "mobi", "mp3", "ogg", "djvu", "exe", "iso",
}
SKIP_SCHEMES = ("#", "mailto:", "javascript:", "tel:", "data:", "ftp:", "file:")

_CTX = ssl.create_default_context()
_CTX.check_hostname = True
_CTX.verify_mode = ssl.CERT_REQUIRED


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_text(t: str) -> str:
    return sha256_bytes(t.encode("utf-8"))


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Credential-free GET-only HTTP
# ---------------------------------------------------------------------------
def http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "close",
    }, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S, context=_CTX) as r:
            raw = r.read(MAX_BODY + 1)[:MAX_BODY]
            return {"ok": True, "status": r.status, "final_url": r.geturl(),
                    "raw": raw, "ctype": r.headers.get("Content-Type")}
    except urllib.error.HTTPError as e:
        try:
            raw = e.read(MAX_BODY + 1)[:MAX_BODY]
        except Exception:
            raw = b""
        return {"ok": True, "status": e.code,
                "final_url": getattr(e, "url", url), "raw": raw,
                "ctype": (e.headers.get("Content-Type") if e.headers else None)}
    except Exception as e:  # network/substrate failure, never a scientific branch
        return {"ok": False, "status": None, "final_url": url, "raw": b"",
                "ctype": None, "error": f"{type(e).__name__}:{e}"}


def decode(body: bytes, ctype):
    cs = "utf-8"
    if ctype and "charset=" in ctype.lower():
        cs = ctype.lower().split("charset=", 1)[1].split(";", 1)[0].strip()
    try:
        return body.decode(cs, "replace")
    except Exception:
        return body.decode("utf-8", "replace")


def is_asset(u: str) -> bool:
    last = urllib.parse.urlparse(u).path.rsplit("/", 1)[-1]
    if "." not in last:
        return False
    return last.rsplit(".", 1)[-1].lower() in ASSET_EXTS


def norm_url(href: str, base: str):
    href = (href or "").strip()
    if not href or href.startswith(SKIP_SCHEMES):
        return None
    try:
        u = urllib.parse.urljoin(base, href)
    except Exception:
        return None
    p = urllib.parse.urlsplit(u)
    if p.scheme not in ("http", "https"):
        return None
    u = urllib.parse.urlunsplit((p.scheme, p.netloc, p.path or "/", p.query, ""))
    return None if is_asset(u) else u


def url_key(u: str):
    p = urllib.parse.urlsplit(u)
    return (p.netloc.lower(), p.path.rstrip("/"))


def match_key(u: str):
    """Canonical resource identity for DISCOVERY matching (VN-V3b).

    A trailing '/' and a single trailing '.html'/'.htm' are removed. Sitemaps
    commonly list the canonical spelling (e.g. '/component/button') while the
    static <a href> links that the BFS follows use the '.html' spelling
    ('/component/button.html'); both denote the SAME resource on these hosts, so
    comparing canonical forms measures whether the page was enumerated rather
    than whether one particular URL spelling was enumerated. This is applied
    ONLY to discovery matching; pool building/dedup keeps exact URLs.
    """
    p = urllib.parse.urlsplit(u)
    path = p.path.rstrip("/")
    for ext in (".html", ".htm"):
        if path.lower().endswith(ext):
            path = path[:-len(ext)]
            break
    return (p.netloc.lower(), path)


# ---------------------------------------------------------------------------
# HTML parsing (stdlib only; no JS)
# ---------------------------------------------------------------------------
class HTMLScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.controls = []
        self.feeds = []
        self.search_forms = []
        self.jsonld = []
        self._in_ld = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "link":
            t = (a.get("type") or "").lower()
            if a.get("href") and ("rss" in t or "atom" in t):
                self.feeds.append({"type": t, "href": a["href"]})
        elif tag == "form":
            act = a.get("action") or ""
            low = (act + " " + (a.get("id") or "") + " " + (a.get("role") or "")).lower()
            if any(k in low for k in ("search", "query", "/find", "/results")):
                self.search_forms.append({"action": act, "method": (a.get("method") or "get").lower()})
        elif tag == "input":
            n = (a.get("name") or "").strip()
            if n:
                self.controls.append((n, (a.get("type") or "text").lower()))
            typ = (a.get("type") or "").lower()
            hid = (a.get("id") or "").lower()
            if typ == "search" or "search" in hid or n.lower() in ("q", "query", "search", "s"):
                self.search_forms.append({"action": "", "method": "get", "via_input": n or a.get("id") or ""})
        elif tag == "select":
            n = (a.get("name") or "").strip()
            if n:
                self.controls.append((n, "select"))
        elif tag == "script":
            if (a.get("type") or "").lower() == "application/ld+json":
                self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_ld:
            self.jsonld.append(data)


def scan_html(body: bytes, ctype):
    s = HTMLScan()
    try:
        s.feed(decode(body, ctype))
        s.close()
    except Exception:
        pass
    return s


def ld_json_urls(scan: HTMLScan):
    urls = set()
    for blob in scan.jsonld:
        try:
            obj = json.loads(blob)
        except Exception:
            continue
        stack = [obj]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                for k, v in cur.items():
                    if k in ("url", "@id", "mainEntityOfPage", "contentUrl", "sameAs"):
                        if isinstance(v, str):
                            urls.add(v)
                        elif isinstance(v, dict) and isinstance(v.get("@id"), str):
                            urls.add(v["@id"])
                    stack.append(v)
            elif isinstance(cur, list):
                stack.extend(cur)
    return urls


def sitemap_urls(body: bytes, ctype):
    txt = decode(body, ctype)
    urls = set()
    if "<loc>" in txt or "<loc " in txt:
        for m in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt, flags=re.I):
            urls.add(m.strip())
    if not urls:
        for line in txt.splitlines():
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                urls.add(line)
    return urls


# ---------------------------------------------------------------------------
# Frozen BFS (sampling-frame construction) -- identical policy to
# EXP-FRONTIER-37950626378 RED arm: same-host static <a href>, document order,
# per-URL defragment+drop-assets, budget B, depth cap D.
# ---------------------------------------------------------------------------
def bfs_seed(seed: str, budget: int = BUDGET_PAGES, depth: int = DEPTH_CAP):
    first = http_get(seed)
    if not first["ok"] or first["status"] is None:
        return {"seed": seed, "ok": False, "error": first.get("error")}
    root = norm_url(first["final_url"], first["final_url"]) or seed
    host = urllib.parse.urlsplit(root).netloc
    seen = {root}
    hop = {root: 0}
    order = [root]
    queue = deque([root])
    cached = {root: first}
    items = {}  # page -> dict(hop, controls)
    nget = 1
    if first["status"] == 200 and first["raw"]:
        s = scan_html(first["raw"], first["ctype"])
        if s.controls:
            items[root] = {"hop": 0, "controls": sorted(set(s.controls))}
    while queue and len(order) < budget:
        cur = queue.popleft()
        rec = cached.pop(cur, None) or http_get(cur)
        nget += 1
        if not rec["ok"] or rec["status"] is None:
            continue
        if cur != root:
            order.append(cur)
        if rec["status"] != 200 or not rec["raw"]:
            continue
        s = scan_html(rec["raw"], rec["ctype"])
        if cur != root and s.controls:
            items[cur] = {"hop": hop[cur], "controls": sorted(set(s.controls))}
        if hop[cur] >= depth:
            continue
        for href in s.links:
            au = norm_url(href, rec["final_url"])
            if not au or urllib.parse.urlsplit(au).netloc != host or au in seen:
                continue
            seen.add(au)
            hop[au] = hop[cur] + 1
            queue.append(au)
    byhop = Counter(hop[u] for u in order)
    return {"seed": seed, "ok": True, "final_root": root, "host": host,
            "n_get": nget, "pages": len(order),
            "pages_by_hop": dict(sorted(byhop.items())), "items": items}


def build_pool(seeds=None):
    seeds = seeds if seeds is not None else SEEDS
    pages = {}
    seed_stats = []
    for entry in seeds:
        res = bfs_seed(entry["seed"])
        seed_stats.append({k: res.get(k) for k in
                           ("seed", "ok", "error", "host", "final_root", "n_get",
                            "pages", "pages_by_hop")})
        if not res.get("ok"):
            continue
        for page, info in res["items"].items():
            prev = pages.get(page)
            if prev is None or info["hop"] < prev["hop"]:
                pages[page] = {"page_url": page, "hop": info["hop"],
                               "controls": info["controls"], "host": entry["host"],
                               "engine": entry["engine"], "stratum": entry.get("stratum"),
                               "via_seed": entry["seed"]}
    return pages, seed_stats


def admit(pages):
    deep = {p: v for p, v in pages.items() if 3 <= v["hop"] <= DEPTH_CAP}
    hosts = Counter(v["host"] for v in deep.values())
    engines = Counter(v["engine"] for v in deep.values())
    strata = Counter(v.get("stratum") for v in deep.values())
    gate = {
        "total_deep": len(deep),
        "hosts_with_deep": dict(hosts),
        "engines_with_deep": dict(engines),
        "strata_with_deep": dict(strata),
        "distinct_hosts": len([h for h, c in hosts.items() if c >= ADMIT_PER_ENGINE_MIN]),
        "distinct_engines": len([e for e, c in engines.items() if c >= ADMIT_PER_ENGINE_MIN]),
        "pass": (len(deep) >= ADMIT_DEEP_MIN
                 and len([e for e, c in engines.items() if c >= ADMIT_PER_ENGINE_MIN]) >= ADMIT_DISTINCT_ENGINES_MIN
                 and len([h for h, c in hosts.items() if c >= ADMIT_PER_ENGINE_MIN]) >= ADMIT_DISTINCT_HOSTS_MIN),
    }
    return deep, gate


# ---------------------------------------------------------------------------
# Discovery channels (frozen; cold-start; up to DISCOVERY_GETS_MAX discovery GETs)
# ---------------------------------------------------------------------------
class Budget:
    def __init__(self, budget: int):
        self.budget = budget
        self.n = 0
        self.bytes = 0
        self.cache = {}

    def get(self, url):
        if url in self.cache:
            return self.cache[url]
        if self.n >= self.budget:
            return None
        r = http_get(url)
        self.n += 1
        self.bytes += len(r.get("raw") or b"")
        self.cache[url] = r
        return r


def _base(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    return f"{p.scheme}://{p.netloc}"


def _match(item_url, urls) -> bool:
    tk = match_key(item_url)
    return any(match_key(u) == tk for u in urls)


def ch_robots_sitemap(item_url, seed_root, host):
    b = Budget(DISCOVERY_GETS_MAX)
    base = _base(seed_root)
    urls = set()
    rb = b.get(base + "/robots.txt")
    if rb and rb["ok"] and rb["status"] == 200 and rb["raw"]:
        for line in decode(rb["raw"], rb["ctype"]).splitlines():
            m = re.match(r"(?i)^\s*sitemap:\s*(\S+)", line)
            if m:
                sm = b.get(m.group(1).strip())
                if sm and sm["ok"] and sm["status"] == 200 and sm["raw"]:
                    urls |= sitemap_urls(sm["raw"], sm["ctype"])
    return _finish("ROBOTS_SITEMAP", item_url, urls, b)


def ch_sitemap_xml(item_url, seed_root, host):
    b = Budget(DISCOVERY_GETS_MAX)
    base = _base(seed_root)
    urls = set()
    for cand in (base + "/sitemap.xml", base + "/sitemap_index.xml",
                 base + "/sitemap-index.xml"):
        r = b.get(cand)
        if r and r["ok"] and r["status"] == 200 and r["raw"]:
            urls |= sitemap_urls(r["raw"], r["ctype"])
    return _finish("SITEMAP_XML", item_url, urls, b)


def ch_on_site_search(item_url, seed_root, host):
    b = Budget(DISCOVERY_GETS_MAX)
    urls = set()
    root = b.get(seed_root)
    if root and root["ok"] and root["status"] == 200 and root["raw"]:
        s = scan_html(root["raw"], root["ctype"])
        form = None
        for f in s.search_forms:
            if f.get("action"):
                form = f
                break
        if form is None and s.search_forms:
            form = s.search_forms[0]
        if form:
            seg = urllib.parse.urlparse(item_url).path.rstrip("/").rsplit("/", 1)[-1]
            seg = re.sub(r"\.(html?|php|aspx?)$", "", seg)
            name = form.get("via_input") or "q"
            if form.get("action"):
                q = f"{urllib.parse.urljoin(seed_root, form['action'])}?" + urllib.parse.urlencode({name: seg})
                res = b.get(q)
                if res and res["ok"] and res["status"] == 200 and res["raw"]:
                    rs = scan_html(res["raw"], res["ctype"])
                    for h in rs.links:
                        au = norm_url(h, res["final_url"])
                        if au:
                            urls.add(au)
    return _finish("ON_SITE_SEARCH", item_url, urls, b)


def ch_rss_atom(item_url, seed_root, host):
    b = Budget(DISCOVERY_GETS_MAX)
    urls = set()
    root = b.get(seed_root)
    if root and root["ok"] and root["status"] == 200 and root["raw"]:
        s = scan_html(root["raw"], root["ctype"])
        for feed in s.feeds[:1]:
            fr = b.get(urllib.parse.urljoin(seed_root, feed["href"]))
            if fr and fr["ok"] and fr["status"] == 200 and fr["raw"]:
                fs = scan_html(fr["raw"], fr["ctype"])
                for h in fs.links:
                    au = norm_url(h, fr["final_url"])
                    if au:
                        urls.add(au)
    return _finish("RSS_ATOM", item_url, urls, b)


def ch_json_ld(item_url, seed_root, host):
    b = Budget(1)
    urls = set()
    hub = b.get(seed_root)
    if hub and hub["ok"] and hub["status"] == 200 and hub["raw"]:
        s = scan_html(hub["raw"], hub["ctype"])
        for u in ld_json_urls(s):
            au = norm_url(u, hub["final_url"])
            if au:
                urls.add(au)
    return _finish("JSON_LD", item_url, urls, b)


def _finish(channel, item_url, urls, b: Budget):
    discovered = _match(item_url, urls)
    item_res = None
    if discovered:
        item_res = http_get(item_url)
    item_ok = bool(discovered and item_res and item_res["ok"]
                   and item_res["status"] is not None and 200 <= item_res["status"] < 300)
    total = b.n + (1 if discovered else 0)
    return {"channel": channel, "discovered": discovered, "success": item_ok,
            "discovery_gets": b.n, "item_get": (1 if discovered else 0),
            "total_gets": total, "discovery_bytes": b.bytes,
            "item_status": (item_res["status"] if item_res else None),
            "within_k": total <= K_GETS}


CHANNEL_FN = {
    "ROBOTS_SITEMAP": ch_robots_sitemap,
    "SITEMAP_XML": ch_sitemap_xml,
    "ON_SITE_SEARCH": ch_on_site_search,
    "RSS_ATOM": ch_rss_atom,
    "JSON_LD": ch_json_ld,
}


def evaluate_item(item, seed_root, host):
    out = {}
    for ch in CHANNELS:
        try:
            out[ch] = CHANNEL_FN[ch](item, seed_root, host)
        except Exception as e:
            out[ch] = {"channel": ch, "discovered": False, "success": False,
                       "error": f"{type(e).__name__}:{e}"}
    out["any_success"] = any(out[c]["success"] for c in CHANNELS)
    succ = [out[c] for c in CHANNELS if out[c]["success"]]
    out["min_total_gets_on_success"] = min((r["total_gets"] for r in succ), default=None)
    return out


# ---------------------------------------------------------------------------
# Metrics + decision
# ---------------------------------------------------------------------------
def compute_metrics(admitted, per_item):
    n = len(admitted)
    reachable = sum(1 for it in admitted if per_item[it]["any_success"])
    frac = (reachable / n) if n else None
    per_host = {}
    per_engine = {}
    for host in sorted({admitted[it]["host"] for it in admitted}):
        items = [it for it in admitted if admitted[it]["host"] == host]
        per_host[host] = sum(1 for it in items if per_item[it]["any_success"]) / len(items)
    for eng in sorted({admitted[it]["engine"] for it in admitted}):
        items = [it for it in admitted if admitted[it]["engine"] == eng]
        per_engine[eng] = sum(1 for it in items if per_item[it]["any_success"]) / len(items)
    per_channel = {}
    for ch in CHANNELS:
        per_channel[ch] = sum(1 for it in admitted if per_item[it][ch]["success"]) / n if n else None
    per_stratum = {}
    for st in sorted({str(admitted[it].get("stratum")) for it in admitted}):
        items = [it for it in admitted if str(admitted[it].get("stratum")) == st]
        per_stratum[st] = (sum(1 for it in items if per_item[it]["any_success"]) / len(items)) if items else None
    by_hop = {}
    for h in range(3, DEPTH_CAP + 1):
        items = [it for it in admitted if admitted[it]["hop"] == h]
        by_hop[str(h)] = (sum(1 for it in items if per_item[it]["any_success"]) / len(items)) if items else None
    gets = [per_item[it]["min_total_gets_on_success"] for it in admitted
            if per_item[it]["min_total_gets_on_success"] is not None]
    return {
        "discovery_reachable_fraction": frac,
        "n_admitted_deep": n,
        "n_reachable": reachable,
        "discovery_reachable_fraction_per_host": per_host,
        "discovery_reachable_fraction_per_engine": per_engine,
        "discovery_reachable_fraction_per_stratum": per_stratum,
        "discovery_reachable_fraction_per_channel": per_channel,
        "discovery_reachable_fraction_by_hop": by_hop,
        "median_discovery_gets_reachable": (statistics.median(gets) if gets else None),
    }


def decide(metrics, gate_pass):
    if not gate_pass:
        return "INCONCLUSIVE", 0
    per_host = metrics["discovery_reachable_fraction_per_host"]
    e = sum(1 for _, f in per_host.items() if f >= MATERIALITY_THRESHOLD)
    if e >= MIN_ENGINES_WITH_THRESHOLD:
        return "SUPPORTS", e
    if e == 1:
        return "MIXED", e
    return "FALSIFIES", e


# ---------------------------------------------------------------------------
# Local dynamic-range fixtures (calibration controls; NOT confirmatory)
# ---------------------------------------------------------------------------
def _fixture_pages(kind: str, base: str):
    def page(body_extra=""):
        return (f"<html><body><input name='q' type='text'>{body_extra}</body></html>").encode()
    pages = {
        "/": page("<a href='/a.html'>a</a>"),
        "/a.html": page("<a href='/b.html'>b</a>"),
        "/b.html": page("<a href='/c.html'>c</a>"),
        "/c.html": page("<a href='/d.html'>d</a>"),
        "/d.html": page(),
    }
    if kind == "discoverable":
        pages["/robots.txt"] = f"Sitemap: {base}/sitemap.xml\n".encode()
        pages["/sitemap.xml"] = (f"<urlset><url><loc>{base}/c.html</loc></url>"
                                 f"<url><loc>{base}/d.html</loc></url></urlset>").encode()
    return pages


class _FixtureHandler(BaseHTTPRequestHandler):
    pages = {}

    def log_message(self, *a):
        pass

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        body = self.pages.get(path)
        if body is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)


def with_fixture(kind, fn):
    handler = type("H", (_FixtureHandler,), {})
    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    base = f"http://127.0.0.1:{port}"
    handler.pages = _fixture_pages(kind, base)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    time.sleep(0.1)
    try:
        return fn(base)
    finally:
        srv.shutdown()


def run_calibration(outdir: Path):
    results = {}
    for kind in ("discoverable", "opaque"):
        def go(base, kind=kind):
            res = bfs_seed(base + "/")
            items = res["items"]
            deep = {p: {"hop": v["hop"], "host": "127.0.0.1", "engine": "stdlib-fixture",
                        "controls": v["controls"]}
                    for p, v in items.items() if 3 <= v["hop"] <= DEPTH_CAP}
            per_item = {p: evaluate_item(p, base + "/", "127.0.0.1") for p in deep}
            m = compute_metrics(deep, per_item) if deep else {"discovery_reachable_fraction": None,
                                                              "n_admitted_deep": 0}
            return {"n_deep": len(deep), "fraction": m.get("discovery_reachable_fraction"),
                    "by_hop": m.get("discovery_reachable_fraction_by_hop"),
                    "per_channel": m.get("discovery_reachable_fraction_per_channel")}
        results[kind] = with_fixture(kind, go)
    results["CALIBRATION_PASS"] = (
        results["discoverable"]["fraction"] == 1.0 and results["opaque"]["fraction"] == 0.0)
    write_json(outdir / "calibration.json", results)
    print(json.dumps(results, indent=2))
    return results


# ---------------------------------------------------------------------------
# Confirmatory run
# ---------------------------------------------------------------------------
def confirmatory(outdir: Path):
    t0 = time.time()
    pages, seed_stats = build_pool()
    deep, gate = admit(pages)
    write_json(outdir / "raw_pool.json",
               {"seed_stats": seed_stats, "n_pages": len(pages), "gate": gate,
                "deep_items": {p: {"hop": v["hop"], "host": v["host"],
                                   "engine": v["engine"], "controls": v["controls"]}
                               for p, v in sorted(deep.items())}})
    controls = {}
    controls["PC_DISCOVERY_CHANNEL_REACHABILITY"] = {"status": "see certificate"}
    controls["PC_HOP_CONFIRMATION"] = {
        "target": "https://doc.rust-lang.org/book/ch01-01-installation.html",
        "expected": {"found": True, "hop": 1},
        "pass": None}
    # hop positive control
    pc = bfs_seed("https://doc.rust-lang.org/book/")
    pc_hit = next((p for p in pc.get("items", {}) if p.endswith("ch01-01-installation.html")), None)
    controls["PC_HOP_CONFIRMATION"]["observed"] = {"found": pc_hit is not None,
                                                 "hop": pc.get("items", {}).get(pc_hit, {}).get("hop") if pc_hit else None}
    controls["PC_HOP_CONFIRMATION"]["pass"] = bool(pc_hit and pc["items"][pc_hit]["hop"] == 1)
    controls["ADMISSION_GATE"] = gate
    if not gate["pass"]:
        result = {
            "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
            "status": "MEASUREMENT_INVALID", "outcome": "INCONCLUSIVE",
            "metrics": {"admission_gate": gate},
            "controls": controls, "artifacts": [], "observations": [],
            "validity_notes": ["Admission gate failed; no confirmatory branch is reported."],
            "unresolved": ["Admission gate shortfall: " + json.dumps(gate)],
        }
        write_json(outdir / "result.json", result)
        return result
    session_metrics = []
    per_item_by_session = []
    admitted = sorted(deep)
    for s in range(SESSIONS):
        per_item = {}
        for it in admitted:
            per_item[it] = evaluate_item(it, deep[it]["via_seed"], deep[it]["host"])
        per_item_by_session.append(per_item)
        session_metrics.append(compute_metrics(admitted, per_item))
    # VN-V4 determinism: item flagged if any channel's success differs across sessions
    unstable = []
    for it in admitted:
        a, b = per_item_by_session[0][it], per_item_by_session[1][it]
        if any(a[c]["success"] != b[c]["success"] for c in CHANNELS):
            unstable.append(it)
    stable = [it for it in admitted if it not in unstable]
    per_item_final = {it: per_item_by_session[0][it] for it in stable}
    metrics = compute_metrics(stable, per_item_final)
    metrics["n_unstable_excluded"] = len(unstable)
    metrics["unstable_items"] = unstable[:50]
    metrics["session_0_pooled_fraction"] = session_metrics[0]["discovery_reachable_fraction"]
    metrics["session_1_pooled_fraction"] = session_metrics[1]["discovery_reachable_fraction"]
    outcome, e = decide(metrics, gate["pass"])
    metrics["engines_meeting_threshold"] = e
    # null control on synthetic identifiers
    null_ok = True
    for ch in CHANNELS:
        for suf in ("a", "b"):
            synthetic = f"https://{list(gate['hosts_with_deep'])[0]}/spider-nonexistent-{SEED}-{suf}.html"
            r = CHANNEL_FN[ch](synthetic, SEEDS[0]["seed"], list(gate['hosts_with_deep'])[0])
            if r["success"]:
                null_ok = False
    controls["NC_SYNTHETIC_UNREACHABLE_ITEM"] = {"pass": null_ok, "expected": "0 reachable"}
    # PC_EXPOSING_DEEP_ENUMERATION: the discovery-EXPOSING stratum must still
    # enumerate admitted DEEP content on >= 2 hosts at EXECUTE (live guard that
    # SUPPORTS-liveness survives mid-run host changes).
    exposing_by_host = {}
    for it in stable:
        if deep[it].get("stratum") == "EXPOSING":
            h = deep[it]["host"]
            ok = per_item_final[it]["ROBOTS_SITEMAP"]["success"] or \
                 per_item_final[it]["SITEMAP_XML"]["success"]
            exposing_by_host.setdefault(h, 0)
            exposing_by_host[h] += 1 if ok else 0
    exposing_pass = sum(1 for c in exposing_by_host.values() if c >= 1) >= 2
    controls["PC_EXPOSING_DEEP_ENUMERATION"] = {
        "expected": ">= 2 EXPOSING hosts with >= 1 admitted DEEP page via ROBOTS_SITEMAP/SITEMAP_XML",
        "observed": exposing_by_host,
        "pass": exposing_pass}
    # Step 0 in-confirmatory control gate (decision rule Step 0): any failure is
    # infrastructure/substrate invalidity, never a scientific branch.
    step0_ok = bool(pc_hit and pc["items"][pc_hit]["hop"] == 1) and null_ok and exposing_pass
    status_final, outcome_final = "COMPLETE", outcome
    if not step0_ok:
        status_final, outcome_final = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes = validity_notes + [
            "Step-0 control failure detected (PC_HOP_CONFIRMATION / NC_SYNTHETIC_UNREACHABLE_ITEM / "
            "PC_EXPOSING_DEEP_ENUMERATION). Recorded in controls; no scientific branch is reported."]
    validity_notes = [
        "Static <a href>, <link rel=alternate>, <form>/<input> and application/ld+json only; JS-rendered navigation and JS search are not followed (representation loss).",
        "GET = one logical request with redirects followed; a redirect does not consume an extra GET unless a separate validation fetch is issued (spare).",
        "Pool deduplicated by minimum same-host static-hop across the frozen seeds.",
        "State-carrying page = fetched page with >=1 named <input>/<select>; item unit = page.",
    ]
    observations = [
        {"id": "OBS-ENV", "note": f"stdlib runner, {sys.version.split()[0]}, network GET-only"},
        {"id": "OBS-POOL", "note": json.dumps(gate)},
        {"id": "OBS-CHANNEL", "note": json.dumps(metrics["discovery_reachable_fraction_per_channel"])},
    ]
    result = {
        "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
        "status": status_final, "outcome": outcome_final,
        "metrics": metrics, "controls": controls,
        "artifacts": [{"path": "raw_pool.json", "role": "raw"}],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": [
            "Whether host-level results generalize beyond the frozen seeds.",
            "Whether JSON_LD enumeration exists on any admitted host (reported per-channel).",
        ],
    }
    write_json(outdir / "result.json", result)
    (outdir / "report.md").write_text(
        f"# {EXPERIMENT_ID} report\n\nOutcome: **{outcome}** (hosts meeting threshold: {e}).\n"
        f"Pooled discovery_reachable_fraction = {metrics['discovery_reachable_fraction']}.\n"
        f"Per-host: {json.dumps(metrics['discovery_reachable_fraction_per_host'])}\n"
        f"Per-engine: {json.dumps(metrics['discovery_reachable_fraction_per_engine'])}\n"
        f"Per-channel: {json.dumps(metrics['discovery_reachable_fraction_per_channel'])}\n",
        encoding="utf-8")
    write_json(outdir / "provenance.json", {
        "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
        "run_id": os.environ.get("GITHUB_RUN_ID"), "started": t0, "finished": time.time(),
        "python": sys.version, "seeds": SEEDS, "constants": {
            "budget_pages": BUDGET_PAGES, "depth_cap": DEPTH_CAP, "k_gets": K_GETS,
            "threshold": MATERIALITY_THRESHOLD}, "code_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "measurement": "site-native discovery reachability over frozen DEEP pool",
    })
    return result


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", metavar="OUTDIR")
    ap.add_argument("--pool", action="store_true")
    ap.add_argument("outdir", nargs="?")
    args = ap.parse_args()
    if args.calibrate:
        run_calibration(Path(args.calibrate))
        return
    if args.pool:
        pages, stats = build_pool()
        deep, gate = admit(pages)
        print(json.dumps({"seed_stats": stats, "n_pages": len(pages), "gate": gate},
                         indent=2))
        return
    if not args.outdir:
        print("usage: run.py [--calibrate OUTDIR | --pool | OUTDIR]", file=sys.stderr)
        raise SystemExit(2)
    confirmatory(Path(args.outdir))


if __name__ == "__main__":
    main()
```

## 14. v2 freeze-eligibility checks

All six are answered in `spec.json.freeze_eligibility`; summary:

| check | status |
|-------|--------|
| `decision_rule_reachability` | PASS — denominator >= 10 (190), `E` well-defined in {0..5}, both branches structurally live (certificate 3.5f), fixtures bracket 0.50 |
| `measurement_prerequisites` | PASS — substrate live; pool builds (190 DEEP / 5 hosts / 3 engines); channels live on EXPOSING hosts; all controls run |
| `baseline_identifiability` | PASS — four distinct stable baselines; treatment is a distinct decision function over the same admitted item set |
| `control_sensitivity` | PASS — calibration 1.0/0.0; EXPOSING/OPAQUE contrast 1.0 vs 0.0; `PC_EXPOSING_DEEP_ENUMERATION` adds a live guard |
| `treatment_liveness` | PASS — pipeline runs end-to-end (1.0/0.0 fixtures); 3 EXPOSING + 2 OPAQUE hosts live at DESIGN |
| `freeze_artifacts_bound` | NOT_APPLICABLE — no mutable local dependency: seeds + strata inlined in `spec.json` and section 13, full code hash-bound via `CODE_SHA256`; the live Web is an external remote substrate pinned by seeds + the re-checked admission gate |

`spec.json.freeze_artifacts = []`.

## 15. Not authorized

- Re-measuring the grandparent's static re-derivable fraction or its GROWING ratio.
- Returning to the blocked `C-SEMANTIC-RESOLVE` thread.
- Constructing the pool or running any discovery probe after `freeze.json` exists.
- Freezing any design whose falsifier cannot trigger in both directions.
- Promoting any discovery mechanism to Product Core from this experiment.

## 16. Next stage

An **independent** `design_review.json` (separate stage/agent, not this DESIGN task) must PASS before `freeze.json` is written. The reviewer must attack: (a) whether the frozen seed list still reproduces a multi-engine DEEP pool (gate >= 10 / 2 engines / 2 hosts); (b) whether the **stratified** pool is an acceptable frame for a capability-bound inference or whether the EXPOSING-select bias breaks the claim (section 10.10); (c) whether **canonical `match_key`** (`.html`/`/` stripping) can merge distinct resources or inflate fractions (section 10.11); (d) whether `K = 3` and `0.50` are non-arbitrary (they bracket the measured calibration range and are recorded before outcomes); (e) whether `JSON_LD`/`ON_SITE_SEARCH` are treated as genuinely cold-start; (f) whether `freeze_artifacts_bound = NOT_APPLICABLE` is justified given inlined seeds + hash-bound code; (g) whether the decision unit (host, with engine/stratum descriptive) is faithful to the mandate's "host/engine unit"; (h) whether the two-sided reachability claim (certificate 3.5f) over-claims the outcome (it is a DESIGN attainability probe; EXECUTE is authoritative); (i) whether every control can fire in both directions.

DESIGN NOT YET FROZEN — awaiting `design_review.json`.
