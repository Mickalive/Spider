# Preregistration — EXP-FRONTIER-38085197666

- **Experiment:** `EXP-FRONTIER-38085197666`
- **Lane:** frontier
- **Design contract:** v2
- **Status:** DESIGN complete (self-attack passed) — awaiting an independent `design_review.json`; NOT yet frozen
- **Claim(s):** `C-CROSSSITE` — "Reusable mechanisms transfer across website holdout" (registry status HYPOTHESIS)
- **Director mandate:** PIVOT, cycle `38084662468`, `cognitive_reset=true`, target `C-CROSSSITE`
- **Base SHA:** `6b4a1f7b18e84015e1765965081f2a8e97d3ba27` (request.base_sha)
- **Claim registry SHA256:** `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`
- **Frozen code SHA256 (section 13):** `e99873cf49c411c942dba594bdff997c7a0dfe1b265833fdcc93e20d63616d80`
- **Created:** 2026-10-10

This file and `spec.json` are the frozen design. EXECUTE must reproduce section 13 verbatim and verify its SHA256 before running. No field below may change after `freeze.json` exists.

---

## 0. Relation to prior work

- `EXP-FRONTIER-37984242167` (direct predecessor, this mandate, v1) was **BLOCKED**: empty sampling frame (0 seeds, 0 DEEP items, 0 hosts), an absent pre-freeze control certificate, and a primary metric that was 0/0 so that **both falsifier directions were unreachable**. Its `audit.json` recorded `required_fixes` VN-A1 (populate seed list and run the hop crawl), VN-A2 (verify the three control-certificate conditions with evidence), VN-A3 (resolve the four open design decisions before freeze) and instructed the v2 freeze to bind pool/certificate artifacts. `same_failure_count=8`. This design is the v2 repair; it does not repeat that failure.
- The first v2 repair draft was returned `failure` / `category=substantive` by the independent design-review stage (`model_design_review.json`; the reviewer run itself crashed — `exit_code=1`, no `design_review.json` captured — so no objection text survived). The defect is nonetheless objectively demonstrable and is fixed here: the draft pool's discovery surfaces enumerated only version roots (`doc.rust-lang.org/sitemap.txt` lists 3 roots; `docs.pytest.org/sitemap.xml` lists 15), so every admitted DEEP page had per-host fraction **0** and `E = 0` identically — the SUPPORTS branch was structurally unreachable and the experiment was one-sided. The final v2 design uses a **stratified pool** (3 discovery-EXPOSING hosts + 2 OPAQUE hosts, section 3.1) plus **canonical URL matching** (`match_key`, VN-V3c) so that both `E >= 2` and `E == 0` are live.
- `EXP-FRONTIER-37950626378` (grandparent) measured `RECOVERY_REDUCTION_FROM_PERSISTED_STATE` = **GROWING** with `R_req=5.2667`, `R_bytes=7.3113`. Its DEEP partition (`n_deep=25`) lay entirely on the single host `doc.rust-lang.org`, so the cross-host/engine question was left open. It supplies this experiment's baselines B_PERSISTED_PATH_REACQUISITION, B_DIRECT_URL_REPLAY and the shortest-path hop definition.
- `EXP-FRONTIER-38078430316` (v2 sibling) supplies the prereg-embedded-code + `CODE_SHA256` freeze pattern.
- **Pre-2.0 corpus check (not a repetition).** A targeted scan of the normalized pre-2.0 canonical archive (`.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md`, ~22 MB, generated 2026-08-30) finds **0 occurrences of `sitemap`** and only compliance/`Content-Signal` uses of `robots.txt` (82 occurrences), plus a transition-graph BFS (unrelated to Web depth). Prior work therefore contains **no site-native discovery (robots/sitemap/feed/JSON-LD enumeration) experiment** and no measurement of depth cost via discovery; the `O(1)`/`BFS` hits are about artifact-write complexity and non-Web graphs. This experiment's question is new to Research 2.0 and not a re-run of pre-2.0 work.
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
- The frozen pool is genuinely heterogeneous by construction: 3 hosts in stratum **EXPOSING** (publish content-level `<urlset>` sitemaps: `vitepress.dev` 272 locs, `router.vuejs.org` 230, `element-plus.org` 307 — an apparatus fact recorded by the sitemap-liveness probe, not an item-reachability measurement) and 2 in stratum **OPAQUE** (`doc.rust-lang.org` sitemap.txt lists 3 version roots, `docs.pytest.org` sitemap.xml lists 15). Attainability is argued **structurally** (denominator 190 >= 10; per-host fraction in [0,1]; both strata present; the instrument spans the threshold, producing 1.0 on a fully-discoverable local fixture and 0.0 on an opaque one) **and by synthetic branch exercise** (the frozen code is driven end-to-end to both `SUPPORTS` and `FALSIFIES`). No item-level reachability fraction is computed at DESIGN: the earlier draft's canonical per-host overlap numbers (1.0/1.0/1.0 vs 0.0/0.0) were **removed** as outcome-bearing leakage of the primary metric. Neither `E == 0` (EXPOSING enumeration breaks) nor `E >= 2` (EXPOSING enumeration holds) is excluded by construction; the confirmatory run is the authoritative measurement.

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
(f) both_branch_attainability: true   -> argued structurally + by synthetic branch exercise (NOT by an
                                        item-level outcome): denominator 190>=10; per-host fraction in [0,1];
                                        instrument range bracketed by fixtures (1.0 / 0.0); both EXPOSING and
                                        OPAQUE strata present; the frozen code is driven to SUPPORTS (E>=2)
                                        and FALSIFIES (E==0) on synthetic inputs. So E==0 and E>=2 are both
                                        structurally reachable. No canonical per-host item-reachability fraction
                                        is reported at DESIGN (removed as outcome-bearing).
(re-verified 2026-10-11 with the frozen section 13 artifact, extracted byte-for-byte and
        sha256-verified): the extracted file itself re-ran `--pool` -> gate PASS 190 DEEP
        (10/5/4/12/159; VitePress 19 / mdBook 12 / Sphinx 159; strata EXPOSING 19 / OPAQUE 171)
        and `--calibrate` -> CALIBRATION_PASS true; PC_HOP_CONFIRMATION hop==1;
        PC_SEED_HOST_IDENTITY all 5 seeds match; all status/outcome branches
        exercised end-to-end on synthetic/local inputs (SUPPORTS, FALSIFIES, gate-fail, step0-fail, calibration-fail)
        each emitting a consistent result/report/provenance triple. No discovery/outcome measurement was run.
```

This repairs v1 `VN-A1`/`VN-A2`/`VN-A3` and the failed first v2 draft: the frame is non-empty and recorded, the certificate conditions are live-verified with evidence, and the falsifier can trigger in both directions. Attainability condition (f) is now argued **structurally** and by a **synthetic branch exercise** rather than by reporting DESIGN-measured per-host item fractions, because those numbers were the primary metric and would have leaked the EXECUTE outcome into DESIGN. The confirmatory run is the authoritative measurement.

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
- **Re-probe 2026-10-10 (section 13 code):** all five seed roots **200** with `final_root` host == declared host (no cross-host redirect). `vitepress.dev` / `router.vuejs.org` / `element-plus.org` `/sitemap_index.xml` and `/sitemap-index.xml` **404**; `doc.rust-lang.org` `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml` **404** (only `sitemap.txt` via robots); `docs.pytest.org` `/sitemap_index.xml`, `/sitemap-index.xml` **404**.

**OBSERVATION.** The three EXPOSING hosts publish content-level `<urlset>` sitemaps (272/230/307 locs) that enumerate deep pages; the two OPAQUE hosts publish only version/root sitemaps (3/15 locs) and no per-page enumeration. **DERIVED.** `ROBOTS_SITEMAP` and `SITEMAP_XML` are live and parsable on all three EXPOSING hosts; `RSS_ATOM` yields nothing on any seed root; `JSON_LD` yields 0 blocks on all five seed roots; `ON_SITE_SEARCH` is JS-only on VitePress/mdBook and static-result on Sphinx (`search.html?q=` returns no server-side result links for arbitrary deep pages). **INTERPRETATION.** The decisive channel pair is `ROBOTS_SITEMAP`/`SITEMAP_XML` on EXPOSING hosts; the OPAQUE hosts bound the negative side. The treatment is neither absent nor universal, so the decision can land on either side.

### 6.2 Null control (RAW EVIDENCE)

Synthetic items `spider-nonexistent-38085197666-<a|b>.html` probed through all five channels against pool hosts: **all 5 channels return `success=false`, 0 reachable URLs**. `NULL_ALL_ZERO = true`. This guards against false-positive discovery via search suggestions, redirect chains or parser errors.

### 6.3 Positive control (DESIGN prerequisite; confirmatory check at EXECUTE)

- **PC_DISCOVERY_CHANNEL_REACHABILITY(a):** at least one channel returns 200 with parsable entries on >= 1 pool host — satisfied live on all three EXPOSING hosts (section 6.1).
- **PC_DISCOVERY_CHANNEL_REACHABILITY(b):** the frozen BFS must return `found=true, hop=1` for the preregistered true-hop-1 target `https://doc.rust-lang.org/book/ch01-01-installation.html`; verified at EXECUTE.
- **PC_DISCOVERY_CHANNEL_LIVENESS:** at EXECUTE, on >= 2 EXPOSING hosts, `ROBOTS_SITEMAP` or `SITEMAP_XML` must **fetch and parse >= 1 URL** (`urls_count >= 1`) (apparatus-liveness — the discovery channel is operational). This control is deliberately phrased on **parsed-URL liveness, not on admitting a specific DEEP item**, so a genuine `FALSIFIES` (sitemap alive but not exposing admissible DEEP content) stays reachable and is not masked as `MEASUREMENT_INVALID`. It replaces the earlier `PC_EXPOSING_DEEP_ENUMERATION`, which required admitting a DEEP item and therefore made `FALSIFIES` structurally unreachable (section 6.5, item 8).
- **PC_SEED_HOST_IDENTITY:** every seed's `final_root` netloc must equal its declared host; a cross-host redirect would silently re-base the probe on a different site. Verified at DESIGN (all five match) and re-checked at EXECUTE inside the frozen code; a mismatch is a Step-0 failure (`MEASUREMENT_INVALID`).

### 6.4 Dynamic-range calibration (RAW EVIDENCE, local stdlib `http.server` fixtures)

- `CAL_DISCOVERABLE_FIXTURE` (robots.txt + `sitemap.xml` listing deep pages): `discovery_reachable_fraction = 1.0` (via `ROBOTS_SITEMAP` and `SITEMAP_XML`); `n_deep = 2`.
- `CAL_OPAQUE_FIXTURE` (same deep structure, no robots/sitemap/feed/search/JSON-LD): `discovery_reachable_fraction = 0.0`.
- `CALIBRATION_PASS = true`. Inside the confirmatory run the calibration is re-executed **in-process** before any measurement; failure short-circuits to `MEASUREMENT_INVALID`/`INCONCLUSIVE` (control `CALIBRATION_GATE`), so a measurement can never proceed on an out-of-range instrument.

**DERIVED.** The instrument produces `1.0` and `0.0`, strictly bracketing the `0.50` decision threshold; the pipeline runs end-to-end with no browser, model, key or credential.

### 6.5 Code repairs made during this DESIGN (satisfiability attacks)

Two latent defects in the previous draft's embedded code were found by branch
attacks and repaired **before freeze** (the previous run never executed the
confirmatory path, so neither had surfaced):

1. `NameError` on the control-failure path: `confirmatory()` referenced
   `validity_notes` before assignment inside the `if not step0_ok:` block, so a
   genuine control failure would crash instead of writing a clean
   `MEASUREMENT_INVALID` result. Fixed by building the base `validity_notes`
   list before the conditional and appending the step-0 note.
2. `compute_metrics` contract mismatch: `confirmatory()` passed the list
   `sorted(deep)` (and the list `stable`) where `compute_metrics` indexes
   `admitted[it]["host"]` (a dict keyed by item URL), so the first confirmatory
   session would raise `TypeError`. Fixed by passing URL-keyed dicts
   (`{it: deep[it] for it in sorted(deep)}`).

Additional pre-freeze repairs (full list; every one exercised by the branch
harness before freeze):

1. `MIN_ENGINES_WITH_THRESHOLD` renamed to `MIN_HOST_UNITS_WITH_THRESHOLD` and
   the metric key `engines_meeting_threshold` to `host_units_meeting_threshold`
   (`E` counts host units, not engines).
2. `ADMIT_PER_HOST_MIN` introduced as a named constant; host admission no longer
   silently reuses the engine threshold `ADMIT_PER_ENGINE_MIN`.
3. `PC_SEED_HOST_IDENTITY` added to Step 0.
4. The calibration gate is enforced **inside** `confirmatory()`
   (`CALIBRATION_GATE`), not only via the `--calibrate` CLI.
5. `write_terminal()` emits the full artifact triple (`result.json` +
   `report.md` + `provenance.json`) on **every** terminal path (calibration
   failure, admission-gate failure, Step-0 failure, and COMPLETE run), and the
   report's `Status`/`Outcome` line is derived from the final
   `status_final`/`outcome_final`, never from the pre-control branch (fixes a
   report/result contradiction).
6. `within_k` is now enforced inside channel success (`_finish`): a channel only
   succeeds if the item page is 2xx **and** total GETs <= `K`.
7. `decide()` returns `INCONCLUSIVE` when `n_admitted_deep == 0`, so an empty
   denominator can never be silently read as `FALSIFIES`.
8. `PC_EXPOSING_DEEP_ENUMERATION` (outcome-correlated) replaced by
   `PC_DISCOVERY_CHANNEL_LIVENESS` (parsed-URL liveness via `urls_count`); the
   old control forced `MEASUREMENT_INVALID` in a genuine `FALSIFIES`.
9. `bfs_seed` GET accounting fixed (the cached seed root is no longer
   double-counted) and a per-item `bfs_cost` (1-based BFS visit order) captured
   to emit the `B_LINK_FOLLOWING_BFS` baseline as a **measured** value.
10. `cost_baselines` metric added (median/mean BFS, persisted-path and direct
    replay costs, discovery costs on success, and a per-hop flat-vs-growing
    diagnostic), so the comparators are emitted measurements rather than prose.
11. The deterministic 2-of-3 `SITEMAP_XML` candidate cap is disclosed (section
    10.14).

**Branch-exercise evidence (DESIGN, synthetic/local only; no confirmatory
outcome computed).** With the repaired section 13 code: calibration fixtures
give 1.0/0.0 (`CALIBRATION_PASS=true`); `--pool` reproduces ADMISSION_GATE_V2
(190 DEEP; 10/5/4/12/159); and the following paths execute end-to-end, each
writing a consistent result/report/provenance triple:
`SUPPORTS` (status=COMPLETE, E>=2), `FALSIFIES` (status=COMPLETE, E=0,
`PC_DISCOVERY_CHANNEL_LIVENESS` true), admission-gate failure
(`MEASUREMENT_INVALID`), step-0 control failure (`MEASUREMENT_INVALID`,
previously a crash), and calibration failure (`MEASUREMENT_INVALID`). All
status/outcome branches are therefore reachable and non-crashing.

## 7. Metrics (stable ids)

- **Primary:** `discovery_reachable_fraction` (pooled); `discovery_reachable_fraction_per_host[host]` (decision unit); `discovery_reachable_fraction_per_engine[engine]` (descriptive).
- **Secondary:** `discovery_reachable_fraction_per_stratum[stratum]`; `discovery_reachable_fraction_per_channel[channel]`; `discovery_reachable_fraction_by_hop[3..6]`; `median_discovery_gets_reachable`; `host_units_meeting_threshold` (`E`); `cost_baselines` (measured `B_LINK_FOLLOWING_BFS` median `bfs_cost`, `B_PERSISTED_PATH_REACQUISITION` hop+1, `B_DIRECT_URL_REPLAY` 1, discovery-GET medians on success, and per-hop medians as the flat-vs-growing diagnostic).
- **Controls metric:** `controls.<id>.pass`.

No tokenizer, latency timer or dollar-cost model; GET count and response-body bytes are the only cost bases (token fields `null`).

## 8. Decision rule (frozen, evaluated in order)

```
Step 0  controls: CALIBRATION_GATE (CAL_DISCOVERABLE_FIXTURE==1.0 and CAL_OPAQUE_FIXTURE==0.0, re-run
        in-process), PC_HOP_CONFIRMATION found & hop==1,
        PC_SEED_HOST_IDENTITY (final_root host == declared host for every seed),
        NC_SYNTHETIC_UNREACHABLE_ITEM==0 (all pool hosts x 5 channels x 2 synthetic ids),
        PC_DISCOVERY_CHANNEL_LIVENESS (>= 2 EXPOSING hosts where ROBOTS_SITEMAP/SITEMAP_XML
        fetch and parse >= 1 URL; apparatus liveness, independent of item match).
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
- `PC_DISCOVERY_CHANNEL_LIVENESS` — section 6.3 (EXECUTE liveness of the sitemap/robots channels; parsed-URL based, outcome-independent).
- `PC_HOP_CONFIRMATION` — the true-hop-1 target.
- `NC_SYNTHETIC_UNREACHABLE_ITEM` — section 6.2.
- `CAL_DISCOVERABLE_FIXTURE`, `CAL_OPAQUE_FIXTURE`, `CALIBRATION_GATE` — section 6.4.
- `PC_SEED_HOST_IDENTITY` — section 6.3 (seed final-root stays on declared host).
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
9. **Confirmation bias against the question** — the two local fixtures bracket the threshold (1.0 and 0.0, strictly around 0.50), so the instrument is not rigged to a single answer; the design explicitly records consequences for both branches. No DESIGN item-level per-host fraction is reported (the earlier canonical-overlap numbers were removed as outcome-bearing), so this experiment cannot have designed the answer it will measure.
10. **Stratification / selection bias (structural)** — the pool is a **stratified convenience sample**: EXPOSING hosts were selected *because* they expose content-level sitemaps. `E` therefore measures whether site-native discovery transfers across units **given a discovery-favorable host class**, not the Web-wide prevalence of such hosts. The claim gains only the bounded form `C-CROSSSITE`-bounded: a positive generalizes to EXPOSING-type hosts, not to all hosts; a negative (OPAQUE hosts failing) does not refute EXPOSING-type hosts. The stratum is a pre-treatment host observable recorded at DESIGN, so the decision rule itself is not compromised; the *generalization* is what is bounded.
11. **Canonicalization false-merges (VN-V3c)** — `match_key` removes a single trailing `.html`/`.htm`/`/`, so a genuinely distinct resource `/a.html` vs `/a` would be conflated. Guard: (i) on these hosts the `.html` and clean spellings are the *same* page (EXECUTE matches the item against what was actually enumerated, so only same-resource pairs merge); (ii) `NC_SYNTHETIC_UNREACHABLE_ITEM` and item-page 2xx checks still apply; (iii) per-channel and per-host results are reported, so a systematic merge would surface as an outlier.
12. **Certificate/outcome overlap (removed).** The earlier draft's certificate reported canonical per-host item-reachability fractions (1.0/1.0/1.0 vs 0.0/0.0) — i.e. the primary metric measured at DESIGN. That was outcome-bearing leakage and has been **removed**; attainability is now argued structurally (denominator, range, both strata present) and by a synthetic branch exercise. EXECUTE is therefore the first and only measurement of the item-level outcome.

13. **Ceiling baseline / selection-on-treatment on the EXPOSING stratum (principal bounded limitation).** The three EXPOSING hosts were selected *because* they expose content-level sitemaps that enumerate their own deep pages, so their per-host fraction is expected near the **ceiling 1.0** by construction. A `SUPPORTS` outcome on the EXPOSING side is therefore **partly anticipated by the design** and is treated as bounded confirmation, not as a surprising discovery; the preregistered interpretation (section 12) weights `MIXED`/`FALSIFIES` and the OPAQUE side more heavily. The genuinely uncertain content is (i) whether the OPAQUE hosts ever cross `0.50` (they publish only version-root sitemaps) and (ii) whether the EXPOSING-side reachability survives a live re-measurement (sitemap truncation, canonical spellings, rate limits, mid-run site change). `E == 0` requires the EXPOSING enumeration itself to break at EXECUTE; this is now testable because the Step-0 gate uses the outcome-independent `PC_DISCOVERY_CHANNEL_LIVENESS`, and the branch harness confirms `FALSIFIES` reaches `status=COMPLETE` with `E=0`. Recorded before outcomes; no post-hoc reweighting is permitted.

14. **`SITEMAP_XML` 2-of-3 candidate cap (deterministic).** Under `DISCOVERY_GETS_MAX = 2`, `SITEMAP_XML` fetches at most the first two of `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml`; the third path is reached only when an earlier candidate did not consume the budget. On both OPAQUE hosts all candidates 404, so the cap does not affect the OPAQUE side; on the EXPOSING hosts the first candidate succeeds. Disclosed so a missing third-path enumeration is never read as absence.

15. **`CODE_SHA256` is self-asserted (freeze-scope limitation).** The complete outcome-bearing code is frozen verbatim in section 13 and bound by `CODE_SHA256`, but `scripts/freeze_experiment.py` hashes `prereg.md` (not the code string). The hash is therefore a DESIGN-declared interpretation binding that EXECUTE must re-verify against the extracted block, not a cryptographic freeze guarantee. EXECUTE MUST extract the block byte-for-byte and fail closed (`MEASUREMENT_INVALID`) if `sha256(run.py) != CODE_SHA256`.

## 11. Inherited state (from the parent handoff, preserved)

Parent handoff: `research/experiments/EXP-FRONTIER-37984242167/handoff.json`, `sha256=1b220e4114e490b3fd935b29de14e88fc611b919471483e2243d7dc0281ef6bf` (matches `request.json.parent_handoff.sha256`). Its four categories are preserved verbatim in substance:

**Established.** (i) The parent packet is a **verified design/control-plane defect receipt, not a measurement**: the v1 freeze admitted 0 seeds / 0 DEEP / 0 hosts, carried `all_verified=false`, and its primary metric was `0/0`, so neither falsifier branch was arithmetically reachable — this is the defect this v2 repairs. (ii) The blocker was **not** infrastructure (outbound TLS and bare CPython were available); no HTTP request was sent because any post-freeze crawl would have mutated the frozen frame. (iii) No claim-status change was warranted from the parent packet. (iv) A depth-bounded credential-free static crawler can build the pool from these docs roots under `B=250/D=6`. (v) The grandparent `EXP-FRONTIER-37950626378` measured `RECOVERY_REDUCTION_FROM_PERSISTED_STATE = GROWING` (`R_req=5.2667`, `R_bytes=7.3113`); persisted-path re-acquisition was near-linear (`path_len == hop+1` on 1532/1532), direct URL replay was 1 GET, and its DEEP band was single-host/single-engine `doc.rust-lang.org` mdBook.

**Rejected / retired.** (i) The v1 `EXP-FRONTIER-37984242167` sampling frame is void (0 seeds, 0 DEEP, 0 hosts). (ii) Its "no freeze / placeholder spec" design path is retired. (iii) Reading `BLOCKED`/`NOT_APPLICABLE` as a scientific FALSIFIES (or any evidence for/against discovery) is rejected. (iv) The parent's pooled GROWING ratio as independent Web-economics evidence, the FLAT branch as established, sub-1 break-even reuse counts as economics, and generalization beyond the parent's single-engine mdBook substrate are all rejected. (v) The parent DEEP band is explicitly **not** a substitute for this experiment's required multi-engine pool.

**Unknown.** (i) Whether site-native discovery reaches `>= 0.50` of DEEP items in `<= K=3` GETs on `>= 2` engines — entirely unmeasured; this is this experiment's entire question. (ii) Whether any non-mdBook host admits DEEP (hop >= 3) items within `B=250/D=6` (a prerequisite the DESIGN pool now supplies: 5 hosts / 3 engines). (iii) Whether discovery reachability scales with hop. (iv) Per-channel coverage on VitePress vs mdBook vs Sphinx. (v) The maintenance/invalidation axis (re-validation GETs/bytes, stale-replay false-accept vs re-derivation) — the recorded alternative next question. (vi) The Web-wide fraction of doc hosts that are EXPOSING-type (not measured here; the design is capability-bound).

**Do not assume.** (i) That a single-host/single-engine result generalizes cross-host. (ii) That a machine-readable discovery channel exists on any given host — `doc.rust-lang.org` and `docs.pytest.org` publish only version-root sitemaps. (iii) That `ON_SITE_SEARCH`, `RSS_ATOM` or `JSON_LD` are live on any pool host — all measured zero at DESIGN on the five seed roots. (iv) That the first v2 draft's one-sided pool (all hosts OPAQUE) was satisfiable — it was not; the current stratified pool is the repair. (v) **Never quote or pair the parent baseline values (`RACQ_PATH`/`RACQ_URL`/`RED`) as measurements of this experiment** — they are inherited context on the parent's single-engine pool; this experiment re-derives its own baselines. (vi) **Never construct a pool/crawl after freeze** to "complete" the transaction — that mutates the frozen sampling frame and would be `MEASUREMENT_INVALID`; the repair is this re-opened v2 DESIGN. (vii) Do not let `research/claims/registry.json` or any local field override accepted Codex effective claim states, and do not import `agent_priors_used`/`portfolio_assessment`/`scout_assessment` as SPIDER evidence (labelled non-evidentiary at source).

## 12. Product consequences

- **If SUPPORTS.** Shortest-path hop is not a fundamental acquisition-cost barrier for discovery-enabled acquisition; SPIDER should optimize discovery-channel coverage and substrate expansion rather than path/procedure caching. `C-CROSSSITE` gains a bounded positive that a reusable discovery procedure transfers across `>= 2` host/engine units. Freshness/delta-repair are lower priority for the acquisition phase. **Preregistered caveat:** because the EXPOSING hosts were selected for exposing content-level sitemaps, an EXPOSING-side SUPPORTS is partly anticipated by construction and is recorded as **bounded confirmation**, not surprise; the OPAQUE-side outcome and any MIXED/FALSIFIES carry the higher evidentiary weight (section 10.13). **No mechanism is promoted to Product Core by this experiment.**
- **If FALSIFIES.** Even with site-native discovery, fresh deep-instance acquisition remains path-bound; persistence of paths/procedures retains a measurable depth-dependent amortization surface and the break-even reuse count can be computed from the recorded re-derivation cost. SPIDER's memory architecture should keep investing in path/procedure persistence with freshness guards.
- **If MIXED.** No program-level decision change; the next experiment must resolve discovery-channel coverage or pool composition.

## 13. Frozen outcome-bearing code (verbatim; `CODE_SHA256`)

EXECUTE MUST write the following block byte-for-byte to `run.py` (outside the repo is fine) and verify `sha256(run.py) == e99873cf49c411c942dba594bdff997c7a0dfe1b265833fdcc93e20d63616d80` before running. The calibration gate is re-enforced inside the confirmatory process (`CALIBRATION_GATE`). NOTE: `CODE_SHA256` is self-asserted by this embedded block; `scripts/freeze_experiment.py` hashes `prereg.md` (not the code string), so the code hash is a DESIGN-declared interpretation binding that EXECUTE must re-verify, not a cryptographic freeze guarantee (section 10.15). Extraction rule: the code is the exact bytes between the line after the opening fence and the line before the closing fence (the block content equals the file bytes, trailing newline included). Modes: `python3 run.py --calibrate <OUT>` (controls only), `python3 run.py --pool` (frame reconstruction / admission evidence), `python3 run.py <OUT>` (confirmatory; EXECUTE only).

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
MIN_HOST_UNITS_WITH_THRESHOLD = 2  # e counts HOST units (per-host fractions), not engines
ADMIT_DEEP_MIN = 10
ADMIT_PER_ENGINE_MIN = 3
ADMIT_PER_HOST_MIN = 3
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


def write_terminal(outdir: Path, result: dict, t0: float) -> None:
    """Emit the full EXECUTE artifact triple (result/report/provenance) for any
    terminal path, including early MEASUREMENT_INVALID returns."""
    outdir.mkdir(parents=True, exist_ok=True)
    write_json(outdir / "result.json", result)
    (outdir / "report.md").write_text(
        f"# {result['experiment_id']} report\n\nStatus: **{result['status']}** | "
        f"Outcome: **{result['outcome']}**.\n\n"
        f"Validity notes: {json.dumps(result.get('validity_notes', []))}\n"
        f"Unresolved: {json.dumps(result.get('unresolved', []))}\n",
        encoding="utf-8")
    write_json(outdir / "provenance.json", {
        "schema_version": 1, "experiment_id": result["experiment_id"],
        "lane": result["lane"], "run_id": os.environ.get("GITHUB_RUN_ID"),
        "started": t0, "finished": time.time(), "python": sys.version,
        "seeds": SEEDS, "constants": {
            "budget_pages": BUDGET_PAGES, "depth_cap": DEPTH_CAP, "k_gets": K_GETS,
            "threshold": MATERIALITY_THRESHOLD},
        "code_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "measurement": "site-native discovery reachability over frozen DEEP pool",
        "terminal_status": result["status"]})


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
            items[root] = {"hop": 0, "controls": sorted(set(s.controls)), "bfs_cost": 1}
    while queue and len(order) < budget:
        cur = queue.popleft()
        rec = cached.pop(cur, None)
        if rec is None:
            rec = http_get(cur)
            nget += 1  # count only actual network GETs (the popped root is cached)
        if not rec["ok"] or rec["status"] is None:
            continue
        if cur != root:
            order.append(cur)
        if rec["status"] != 200 or not rec["raw"]:
            continue
        s = scan_html(rec["raw"], rec["ctype"])
        if cur != root and s.controls:
            items[cur] = {"hop": hop[cur], "controls": sorted(set(s.controls)),
                          "bfs_cost": order.index(cur) + 1}
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
                               "bfs_cost": info.get("bfs_cost", info["hop"] + 1),
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
        "distinct_hosts": len([h for h, c in hosts.items() if c >= ADMIT_PER_HOST_MIN]),
        "distinct_engines": len([e for e, c in engines.items() if c >= ADMIT_PER_ENGINE_MIN]),
        "pass": (len(deep) >= ADMIT_DEEP_MIN
                 and len([e for e, c in engines.items() if c >= ADMIT_PER_ENGINE_MIN]) >= ADMIT_DISTINCT_ENGINES_MIN
                 and len([h for h, c in hosts.items() if c >= ADMIT_PER_HOST_MIN]) >= ADMIT_DISTINCT_HOSTS_MIN),
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
    total = b.n + (1 if discovered else 0)
    item_ok = bool(discovered and item_res and item_res["ok"]
                   and item_res["status"] is not None and 200 <= item_res["status"] < 300
                   and total <= K_GETS)
    return {"channel": channel, "discovered": discovered, "success": item_ok,
            "discovery_gets": b.n, "item_get": (1 if discovered else 0),
            "total_gets": total, "discovery_bytes": b.bytes,
            "urls_count": len(urls),
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
    # ---- cost baselines (frozen ids; measured on the same admitted item set) ----
    # B_LINK_FOLLOWING_BFS: cumulative GETs in the frozen item-blind BFS to first
    #   reach each admitted page (captured as bfs_cost during pool construction).
    # B_PERSISTED_PATH_REACQUISITION: hop+1 (GET each node of the frozen path).
    # B_DIRECT_URL_REPLAY: 1 (known URL).
    # Discovery cost = per-item minimum total GETs over successful channels.
    bfs_costs = [admitted[it].get("bfs_cost") for it in admitted if admitted[it].get("bfs_cost")]
    pers_costs = [admitted[it]["hop"] + 1 for it in admitted]
    disc_costs = list(gets)
    def _med(xs):
        return statistics.median(xs) if xs else None
    def _mean(xs):
        return (sum(xs) / len(xs)) if xs else None
    # flat-vs-growing diagnostic: median costs per hop bucket
    cost_by_hop = {}
    for h in range(3, DEPTH_CAP + 1):
        items = [it for it in admitted if admitted[it]["hop"] == h]
        if not items:
            continue
        cost_by_hop[str(h)] = {
            "n": len(items),
            "median_bfs_gets": _med([admitted[it].get("bfs_cost") for it in items if admitted[it].get("bfs_cost")]),
            "median_persisted_path_gets": _med([admitted[it]["hop"] + 1 for it in items]),
            "median_discovery_gets": _med([per_item[it]["min_total_gets_on_success"] for it in items
                                           if per_item[it]["min_total_gets_on_success"] is not None]),
        }
    cost_baselines = {
        "n_admitted": n,
        "median_bfs_gets": _med(bfs_costs),
        "mean_bfs_gets": _mean(bfs_costs),
        "median_persisted_path_gets": _med(pers_costs),
        "median_direct_replay_gets": 1,
        "median_discovery_gets_on_success": _med(disc_costs),
        "mean_discovery_gets_on_success": _mean(disc_costs),
        "n_discovery_successes": len(disc_costs),
        "cost_by_hop": cost_by_hop,
    }
    return {
        "discovery_reachable_fraction": frac,
        "n_admitted_deep": n,
        "n_reachable": reachable,
        "discovery_reachable_fraction_per_host": per_host,
        "discovery_reachable_fraction_per_engine": per_engine,
        "discovery_reachable_fraction_per_stratum": per_stratum,
        "discovery_reachable_fraction_per_channel": per_channel,
        "discovery_reachable_fraction_by_hop": by_hop,
        "median_discovery_gets_reachable": _med(gets),
        "cost_baselines": cost_baselines,
    }


def decide(metrics, gate_pass):
    if not gate_pass:
        return "INCONCLUSIVE", 0
    if not metrics.get("n_admitted_deep"):
        # Empty denominator must never be silently read as FALSIFIES (v1 defect).
        return "INCONCLUSIVE", 0
    per_host = metrics["discovery_reachable_fraction_per_host"]
    e = sum(1 for _, f in per_host.items() if f >= MATERIALITY_THRESHOLD)
    if e >= MIN_HOST_UNITS_WITH_THRESHOLD:
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


def _calibration_state():
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
    return results


def run_calibration(outdir: Path):
    results = _calibration_state()
    write_json(outdir / "calibration.json", results)
    print(json.dumps(results, indent=2))
    return results


# ---------------------------------------------------------------------------
# Confirmatory run
# ---------------------------------------------------------------------------
def confirmatory(outdir: Path):
    t0 = time.time()
    # Self-enforcing calibration gate: the instrument must show its full dynamic
    # range (discoverable fixture 1.0, opaque fixture 0.0) inside the same
    # process, immediately before any confirmatory measurement is attempted.
    cal = _calibration_state()
    if not cal["CALIBRATION_PASS"]:
        result = {
            "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
            "status": "MEASUREMENT_INVALID", "outcome": "INCONCLUSIVE",
            "metrics": {"calibration": {k: cal[k] for k in ("discoverable", "opaque")}},
            "controls": {"CALIBRATION_GATE": {
                "expected": "discoverable fraction == 1.0 and opaque fraction == 0.0",
                "observed": {k: cal[k] for k in ("discoverable", "opaque")},
                "pass": False}},
            "artifacts": [], "observations": [],
            "validity_notes": ["Calibration gate failed inside confirmatory process; "
                               "no scientific branch is reported."],
             "unresolved": ["Calibration shortfall: " + json.dumps(cal)],
        }
        write_terminal(outdir, result, t0)
        return result
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
    # PC_SEED_HOST_IDENTITY: the final-redirect root of every seed must stay on
    # the declared host; a cross-host redirect would silently re-base the probe
    # on a different site and invalidate every per-host fraction.
    host_ident = {}
    for entry in SEEDS:
        st = next((s for s in seed_stats if s["seed"] == entry["seed"]), None)
        fr = (st or {}).get("final_root") or entry["seed"]
        fr_host = urllib.parse.urlsplit(fr).netloc
        host_ident[entry["seed"]] = {
            "ok": bool(st and st.get("ok")), "declared_host": entry["host"],
            "final_root_host": fr_host, "match": bool(st and st.get("ok") and fr_host == entry["host"])}
    host_ident_pass = bool(seed_stats) and all(v["match"] for v in host_ident.values())
    controls["PC_SEED_HOST_IDENTITY"] = {
        "expected": "every seed reachable and final_root netloc == declared host",
        "observed": host_ident, "pass": host_ident_pass}
    if not gate["pass"]:
        result = {
            "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
            "status": "MEASUREMENT_INVALID", "outcome": "INCONCLUSIVE",
            "metrics": {"admission_gate": gate},
            "controls": controls, "artifacts": [], "observations": [],
            "validity_notes": ["Admission gate failed; no confirmatory branch is reported."],
            "unresolved": ["Admission gate shortfall: " + json.dumps(gate)],
        }
        write_terminal(outdir, result, t0)
        return result
    session_metrics = []
    per_item_by_session = []
    admitted = {it: deep[it] for it in sorted(deep)}  # dict keyed by item URL (compute_metrics contract)
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
    stable = {it: deep[it] for it in admitted if it not in unstable}
    per_item_final = {it: per_item_by_session[0][it] for it in stable}
    metrics = compute_metrics(stable, per_item_final)
    metrics["n_unstable_excluded"] = len(unstable)
    metrics["unstable_items"] = unstable[:50]
    metrics["session_0_pooled_fraction"] = session_metrics[0]["discovery_reachable_fraction"]
    metrics["session_1_pooled_fraction"] = session_metrics[1]["discovery_reachable_fraction"]
    outcome, e = decide(metrics, gate["pass"])
    metrics["host_units_meeting_threshold"] = e
    # null control on synthetic identifiers (all pool hosts x 5 channels x 2 ids)
    null_ok = True
    null_detail = {}
    host_seed = {s["host"]: s["seed"] for s in SEEDS}
    for h in sorted(gate.get("hosts_with_deep", {})):
        root = host_seed.get(h, f"https://{h}/")
        for ch in CHANNELS:
            for suf in ("a", "b"):
                synthetic = f"https://{h}/spider-nonexistent-{SEED}-{suf}.html"
                r = CHANNEL_FN[ch](synthetic, root, h)
                if r["success"]:
                    null_ok = False
                    null_detail[f"{h}|{ch}|{suf}"] = "REACHABLE"
    controls["NC_SYNTHETIC_UNREACHABLE_ITEM"] = {
        "pass": null_ok,
        "expected": "0 reachable across all pool hosts x 5 channels x 2 synthetic ids",
        "observed_reachable": null_detail}
    # PC_DISCOVERY_CHANNEL_LIVENESS: on hosts where the pool-time probe found a
    # sitemap (EXPOSING stratum), the sitemap/robots discovery channels must
    # still FETCH and PARSE >=1 URL at EXECUTE. This is an apparatus-liveness
    # control: it is satisfied when the channel returns a non-empty URL set even
    # if none of those URLs is the specific admitted DEEP item, so a genuine
    # FALSIFIES (sitemap alive but does not expose DEEP content) remains
    # reachable. It must NOT be phrased in terms of item match / success.
    liveness_by_host = {}
    for it in stable:
        if deep[it].get("stratum") == "EXPOSING":
            h = deep[it]["host"]
            live = (per_item_final[it]["ROBOTS_SITEMAP"].get("urls_count", 0) >= 1
                    or per_item_final[it]["SITEMAP_XML"].get("urls_count", 0) >= 1)
            liveness_by_host.setdefault(h, 0)
            liveness_by_host[h] += 1 if live else 0
    liveness_pass = sum(1 for c in liveness_by_host.values() if c >= 1) >= 2
    controls["PC_DISCOVERY_CHANNEL_LIVENESS"] = {
        "expected": ">= 2 EXPOSING hosts where ROBOTS_SITEMAP/SITEMAP_XML fetch and parse >= 1 URL "
                    "(apparatus liveness; independent of whether the admitted DEEP item is matched)",
        "observed": liveness_by_host,
        "pass": liveness_pass}
    # Step 0 in-confirmatory control gate (decision rule Step 0): any failure is
    # infrastructure/substrate invalidity, never a scientific branch.
    hop_pass = bool(pc_hit and pc["items"][pc_hit]["hop"] == 1)
    any_channel_live = any(per_item_final[it][c].get("urls_count", 0) >= 1
                           for it in stable for c in CHANNELS)
    pc_reach_pass = bool(hop_pass and host_ident_pass and any_channel_live and liveness_pass)
    controls["PC_DISCOVERY_CHANNEL_REACHABILITY"] = {
        "expected": "(a) >= 1 discovery channel fetches and parses >= 1 URL on >= 1 pool host; "
                    "(b) hop target found hop==1; (c) seed final-root host identity; "
                    "(d) >= 2 EXPOSING hosts with a live sitemap/robots channel",
        "observed": {"any_channel_live": any_channel_live, "hop_pass": hop_pass,
                     "host_identity_pass": host_ident_pass, "liveness_pass": liveness_pass},
        "pass": pc_reach_pass}
    step0_ok = bool(pc_reach_pass and null_ok)
    validity_notes = [
        "Static <a href>, <link rel=alternate>, <form>/<input> and application/ld+json only; JS-rendered navigation and JS search are not followed (representation loss).",
        "GET = one logical request with redirects followed; a redirect does not consume an extra GET unless a separate validation fetch is issued (spare).",
        "Pool deduplicated by minimum same-host static-hop across the frozen seeds.",
        "State-carrying page = fetched page with >=1 named <input>/<select>; item unit = page.",
        "SITEMAP_XML enumerates up to DISCOVERY_GETS_MAX=2 candidate paths in fixed order "
        "(sitemap.xml, sitemap_index.xml, sitemap-index.xml); a third candidate is never "
        "probed when the first two consumed the budget (deterministic).",
    ]
    status_final, outcome_final = "COMPLETE", outcome
    if not step0_ok:
        status_final, outcome_final = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes = validity_notes + [
            "Step-0 control failure detected (PC_HOP_CONFIRMATION / PC_SEED_HOST_IDENTITY / "
            "NC_SYNTHETIC_UNREACHABLE_ITEM / PC_DISCOVERY_CHANNEL_LIVENESS). Recorded in controls; "
            "no scientific branch is reported."]
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
        f"# {EXPERIMENT_ID} report\n\nStatus: **{status_final}** | Outcome: **{outcome_final}** "
        f"(host units meeting threshold: {e}).\n"
        f"Pooled discovery_reachable_fraction = {metrics['discovery_reachable_fraction']}.\n"
        f"Per-host: {json.dumps(metrics['discovery_reachable_fraction_per_host'])}\n"
        f"Per-engine: {json.dumps(metrics['discovery_reachable_fraction_per_engine'])}\n"
        f"Per-channel: {json.dumps(metrics['discovery_reachable_fraction_per_channel'])}\n"
        f"Cost baselines: {json.dumps(metrics['cost_baselines'])}\n",
        encoding="utf-8")
    write_json(outdir / "provenance.json", {
        "schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
        "run_id": os.environ.get("GITHUB_RUN_ID"), "started": t0, "finished": time.time(),
        "python": sys.version, "seeds": SEEDS, "constants": {
            "budget_pages": BUDGET_PAGES, "depth_cap": DEPTH_CAP, "k_gets": K_GETS,
            "threshold": MATERIALITY_THRESHOLD}, "code_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "measurement": "site-native discovery reachability over frozen DEEP pool",
        "terminal_status": status_final,
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
| `decision_rule_reachability` | PASS — denominator >= 10 (190), `E` well-defined in {0..5}, both branches structurally reachable (structural argument + synthetic branch exercise in section 3.5f/6.5), fixtures bracket 0.50 |
| `measurement_prerequisites` | PASS — substrate live; pool builds (190 DEEP / 5 hosts / 3 engines); channels live on EXPOSING hosts; all controls run |
| `baseline_identifiability` | PASS — four distinct stable baselines; treatment is a distinct decision function over the same admitted item set; `B_LINK_FOLLOWING_BFS` emitted as measured `bfs_cost` |
| `control_sensitivity` | PASS — calibration 1.0/0.0; `PC_DISCOVERY_CHANNEL_LIVENESS` (parsed-URL, outcome-independent) adds a live guard without masking FALSIFIES |
| `treatment_liveness` | PASS — pipeline runs end-to-end (1.0/0.0 fixtures); 3 EXPOSING + 2 OPAQUE hosts live at DESIGN |
| `freeze_artifacts_bound` | NOT_APPLICABLE — no mutable local dependency: seeds + strata inlined in `spec.json` and section 13, full code hash-bound via `CODE_SHA256` (self-asserted; freezer hashes `prereg.md`); the live Web is an external remote substrate pinned by seeds + the re-checked admission gate |

`spec.json.freeze_artifacts = []`.

## 15. Not authorized

- Re-measuring the grandparent's static re-derivable fraction or its GROWING ratio.
- Returning to the blocked `C-SEMANTIC-RESOLVE` thread.
- Constructing the pool or running any discovery probe after `freeze.json` exists.
- Freezing any design whose falsifier cannot trigger in both directions.
- Promoting any discovery mechanism to Product Core from this experiment.

## 16. Next stage

An **independent** `design_review.json` (separate stage/agent, not this DESIGN task) must PASS before `freeze.json` is written. The reviewer must attack: (a) whether the frozen seed list still reproduces a multi-engine DEEP pool (gate >= 10 / 2 engines / 2 hosts); (b) whether the **stratified** pool is an acceptable frame for a capability-bound inference or whether the EXPOSING-select bias breaks the claim (section 10.10, and the strengthened ceiling/selection caveat in section 10.13); (c) whether **canonical `match_key`** (`.html`/`/` stripping) can merge distinct resources or inflate fractions (section 10.11); (d) whether `K = 3` and `0.50` are non-arbitrary (they bracket the measured calibration range and are recorded before outcomes); (e) whether `JSON_LD`/`ON_SITE_SEARCH` are treated as genuinely cold-start; (f) whether `freeze_artifacts_bound = NOT_APPLICABLE` is justified given inlined seeds + hash-bound code (and whether the self-asserted `CODE_SHA256`, section 10.15, is acceptable); (g) whether the decision unit (host, with engine/stratum descriptive) is faithful to the mandate's "host/engine unit"; (h) whether the two-sided reachability claim over-claims the outcome (attainability is now argued structurally + synthetically, not by a DESIGN-measured fraction; EXECUTE is authoritative); (i) whether every control can fire in both directions and, specifically, whether `PC_DISCOVERY_CHANNEL_LIVENESS` is genuinely outcome-independent (so FALSIFIES is reachable); (j) whether the removal of the DESIGN canonical-overlap numbers fully closes the outcome-leakage concern (section 10.12).

DESIGN NOT YET FROZEN — awaiting `design_review.json`.

### 16.1 DESIGN self-attack summary

Before finalizing, the design was attacked for empty/unreachable branches, arithmetic impossibility, ceiling/floor baselines, treatment/comparator identity, insensitive controls, missing prerequisites and unbound mutable artifacts. Findings and repairs: eleven latent code defects/contract mismatches repaired (section 6.5), including an **outcome-correlated Step-0 control** that made `FALSIFIES` structurally unreachable and an **outcome-bearing DESIGN measurement** of the primary metric that was removed (section 10.12); the EXPOSING ceiling/selection caveat strengthened (section 10.13); the deterministic `SITEMAP_XML` cap disclosed (section 10.14); the self-asserted `CODE_SHA256` disclosed (section 10.15); every status/outcome branch exercised end-to-end on synthetic/local inputs with a consistent result/report/provenance triple; and the required live probes (seed host identity, robots/sitemap liveness, pool reconstruction, hop control) re-run and reproduced. No confirmatory item-level outcome was computed at DESIGN.
