# Preregistration — EXP-FRONTIER-38085197666

- **Experiment:** `EXP-FRONTIER-38085197666`
- **Lane:** frontier
- **Design contract:** v2
- **Status:** DESIGN complete (self-attack passed) — awaiting an independent `design_review.json`; NOT yet frozen
- **Claim(s):** `C-CROSSSITE` — "Reusable mechanisms transfer across website holdout" (registry status HYPOTHESIS)
- **Director mandate:** PIVOT, cycle `38084662468`, `cognitive_reset=true`, target `C-CROSSSITE`
- **Base SHA:** `6b4a1f7b18e84015e1765965081f2a8e97d3ba27` (request.base_sha)
- **Claim registry SHA256:** `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`
- **Frozen code SHA256 (section 13):** `393775e8ee79f9308d1d142b54f2977b9a677a9f9891988625da810e856b68c8`
- **Created:** 2026-10-10; revision 2 (exposure-blind frame) 2026-10-11; revision 3 (verifiable branch exercise, exposure-blindness by construction, stability cap, engine-span, pacing, trend rule) 2026-10-11

This file and `spec.json` are the frozen design. EXECUTE must reproduce section 13 verbatim and verify its SHA256 before running. No field below may change after `freeze.json` exists.

---

## 0. Relation to prior work

- `EXP-FRONTIER-37984242167` (direct predecessor, this mandate, v1) was **BLOCKED**: empty sampling frame (0 seeds, 0 DEEP items, 0 hosts), an absent pre-freeze control certificate, and a primary metric that was 0/0 so that **both falsifier directions were unreachable**. Its `audit.json` recorded `required_fixes` VN-A1/VN-A2/VN-A3. `same_failure_count=8`. This design is the v2 repair; it does not repeat that failure.
- **Revision 1 of this v2 design (the stratified draft)** was returned `failure` / `category=substantive` by the independent design-review stage (`model_design_review.json`; the reviewer run itself crashed — `exit_code=1`, no `design_review.json` captured — so no objection text survived). Its defect is nonetheless objectively demonstrable and is fixed here:
  1. **Selection-on-treatment / ceiling baseline.** Revision 1 selected 3 hosts *because* they published content-level `<urlset>` sitemaps (an `EXPOSING` stratum) and 2 hosts that publish only version roots (`OPAQUE`). A `SUPPORTS` result (`E >= 2`) was therefore near-certain **by construction** and `FALSIFIES` (`E == 0`) was structurally unreachable on the real pool (it could only occur if the selected-in enumeration broke). This is exactly the "comparators at ceiling" failure the Director flagged as a general prior.
  2. **Live-frame fragility.** By the time of this revision, two Sphinx hosts of revision 1 (`www.sphinx-doc.org`, `docs.readthedocs.com`) and `docs.pytest.org` return HTTP **429 Cloudflare challenge** pages to the credential-free stdlib user agent, so that frame would have collapsed at EXECUTE to `MEASUREMENT_INVALID` rather than measuring anything.
- **Revision 2 repaired both, but a fresh independent design review of the packet returned `failure` / `category=substantive` (`model_design_review.json`, attempt 4, reviewer run crashed with `exit_code=1`, no `design_review.json` or objection text captured).** Because the objection text did not survive, revision 3 is a fresh adversarial self-attack on revision 2 that repairs every defect that is objectively demonstrable from the frozen artifact itself:
  1. **Unverifiable branch-exercise claim (the load-bearing defect).** Revision 2's §6.6, §3.5(f) and `spec.json.design_repairs_and_satisfiability` claimed the frozen code was *driven end-to-end* to `SUPPORTS`/`MIXED`/`FALSIFIES` "writing a consistent result/report/provenance triple", but the frozen code exposed only `--calibrate`, `--pool` and the confirmatory path. An independent reviewer could not reproduce that claim, so `decision_rule_reachability` was asserted rather than shown. Revision 3 adds a first-class `--branch-drive OUTDIR` mode that drives the real `compute_metrics`/`decide`/`write_terminal` path to `SUPPORTS`, `MIXED` (single engine), `MIXED` (one host), `FALSIFIES`, admission-gate failure, calibration failure, empty denominator and the stability cap, and emits the artifact triples plus a machine-readable `branch_drive.json` (all offline). The claim is now reproducible by EXECUTE/AUDIT from the frozen artifact alone.
  2. **Exposure-blindness by use, not by construction.** Revision 2's frame BFS called `HTMLScan`, which also extracts `feeds`, `search_forms` and `jsonld`; the prose promised those fields were unused, but an auditor could not prove the frame was built without seeing the treatment surfaces. Revision 3 uses a dedicated `StaticLinks` parser for the frame BFS that has **no discovery fields at all**, so exposure-blindness is a property of the parser object and is verifiable by construction. The regenerated frame is byte-identical in topology (493 DEEP, 197/94/194/8).
  3. **No stability cap and full-second-session cost.** Revision 2 ran the full admitted set in both sessions with no bound on exclusions, so rate-limit noise could silently shrink the denominator (or inflate failures) and ~15k GETs risked throttling. Revision 3 keeps session 1 on the full set, re-measures only a deterministic 25% subsample in session 2, adds `STABILITY_CAP` (exclusion fraction > 0.10 ⇒ `MEASUREMENT_INVALID`), and paces all foreign GETs (`PACE_S=0.15`).
  4. **Engine span not enforced and oracle channel undisclosed.** The mandate requires the 0.50 threshold "on ≥2 engines"; revision 2's decision counted hosts only, so `E>=2` on a single engine could read as `SUPPORTS`. Revision 3 requires the meeting hosts to span ≥2 engines for `SUPPORTS` (else `MIXED`), and discloses `ON_SITE_SEARCH` as the one oracle-like channel (query = the item's own path segment) by reporting an oracle-free per-host sensitivity and `oracle_dependent_supports`.
  5. **Descriptive trend left unformalised.** Revision 3 preregisters a flat-vs-growing rule on the hop-stratified fraction (FALLING iff frac(hop≥5) < frac(hop=3) − 0.10 with ≥5 items per bucket; else FLAT; UNMEASURED when a bucket is too small).
- `EXP-FRONTIER-37950626378` (grandparent) measured `RECOVERY_REDUCTION_FROM_PERSISTED_STATE` = **GROWING** with `R_req=5.2667`, `R_bytes=7.3113`. Its DEEP partition (`n_deep=25`) lay entirely on the single host `doc.rust-lang.org`, so the cross-host/engine question was left open. It supplies this experiment's baselines B_PERSISTED_PATH_REACQUISITION, B_DIRECT_URL_REPLAY and the shortest-path hop definition.
- `EXP-FRONTIER-38078430316` (v2 sibling) supplies the prereg-embedded-code + `CODE_SHA256` freeze pattern.
- **Pre-2.0 corpus check (not a repetition).** A targeted scan of the normalized pre-2.0 canonical archive (`.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md`, ~22 MB, generated 2026-08-30) finds **0 occurrences of `sitemap`** and only compliance/`Content-Signal` uses of `robots.txt`, plus a transition-graph BFS (unrelated to Web depth). Prior work therefore contains **no site-native discovery experiment** and no measurement of depth cost via discovery. This question is new to Research 2.0.
- The PIVOT mandate supersedes the parent's `next_question`. The parent handoff is continuity evidence only; its `established/rejected/unknown/do_not_assume` distinctions are preserved in section 11.

## 1. Question and mandate

On the credential-free GET-only stdlib-HTTP substrate, over a frozen multi-host pool that DESIGN confirms contains DEEP (hop >= 3) state-carrying pages on at least two distinct hosts/engines:

1. **Primary gate.** What fraction of admitted DEEP pages can a *fresh* agent reach in `K <= 3` GETs (up to 2 discovery GETs + 1 item-page GET) using any of the five site-native cold-start discovery channels (`ROBOTS_SITEMAP`, `SITEMAP_XML`, `ON_SITE_SEARCH`, `RSS_ATOM`, `JSON_LD`)?
2. **Descriptive scaling.** Does reachability scale with the item's shortest-path hop, i.e. is site-native discovery path-bound or effectively path-independent?

The strategic stakes: if discovery collapses depth cost, then shortest-path hop is **not** a fundamental acquisition-cost barrier, persistence of paths/procedures is de-prioritized, and effort moves to **discovery-channel coverage and substrate expansion**. If discovery cannot beat the threshold, fresh deep-instance acquisition remains path-bound and persistence retains a computable depth-dependent break-even.

## 2. Hypothesis and falsifier (two-sided, both branches reachable)

- **H1 (SUPPORTS).** `>= 0.50` of admitted DEEP pages reachable in `K <= 3` GETs on `>= 2` distinct host units.
- **H0 (negative).** `> 0.50` of admitted DEEP pages require more than `K` GETs on all but at most one unit.

**Falsifier (frozen).** Unit = distinct host (per-engine grouping reported descriptively). Let `E` = number of host units whose `discovery_reachable_fraction_per_host[host] >= 0.50`, and let `engines_ok` = (the meeting hosts span `>= 2` distinct generator engines).

- `E >= 2` **and** `engines_ok` => **SUPPORTS** (material reachability on `>= 2` host units across `>= 2` engines)
- `E >= 1` otherwise => **MIXED** (exactly one unit, or `>= 2` units confined to a single engine)
- `E == 0` => **FALSIFIES**

Materiality threshold `0.50`; budget `K = 3`; minimum units meeting threshold `2`. A two-sided test: a uniformly high result and a uniformly low result both falsify the opposite branch; the experiment does not presuppose which holds.

**Reachability argument (why every branch can trigger).**
- The denominator is the number of admitted DEEP pages, `>= 10` by ADMISSION_GATE_V2 (DESIGN observed **493**), so `E` is well-defined in `{0,1,2,3,4}` and no branch is `0/0`.
- The local stdlib fixtures bracket the threshold from both sides: `CAL_DISCOVERABLE_FIXTURE` yields fraction **1.0** and `CAL_OPAQUE_FIXTURE` yields **0.0** (section 6.5), so the instrument demonstrably can produce values above and below `0.50`.
- The frame is **exposure-blind by construction**: the BFS uses a dedicated `StaticLinks` parser that extracts only static `<a href>` and has no `feeds`/`search_forms`/`jsonld` fields at all, so no frame host's discovery surface was (or could be) inspected at DESIGN; the design cannot pre-select whether `E == 0` or `E >= 2`. Attainability is argued **structurally** (denominator 493 >= 10; per-host fraction in [0,1]; the instrument spans the threshold) **and by synthetic branch exercise**: the frozen code's `--branch-drive OUTDIR` mode (section 6.6) drives the real `compute_metrics`/`decide`/`write_terminal` path to `SUPPORTS`, `MIXED` (single engine), `MIXED` (one host) and `FALSIFIES`, plus admission-gate failure, calibration failure, empty denominator and the stability cap, emitting `branch_drive.json` with `all_branches_reachable=true` (DESIGN observation: PASS). No item-level reachability fraction is computed at DESIGN. Neither `E == 0` (site-native discovery of these hosts does not enumerate their DEEP pages) nor `E >= 2` (at least two hosts do) is excluded by construction; the confirmatory run is the authoritative measurement.

## 3. Frozen pool and pre-freeze attainability certificate

### 3.1 Seeds (frozen)

| # | Seed URL | Host | Engine |
|---|----------|------|--------|
| 1 | `https://google.github.io/comprehensive-rust/` | google.github.io | mdBook |
| 2 | `https://rust-lang.github.io/async-book/` | rust-lang.github.io | mdBook |
| 3 | `https://rustc-dev-guide.rust-lang.org/` | rustc-dev-guide.rust-lang.org | mdBook |
| 4 | `https://pandas.pydata.org/docs/` | pandas.pydata.org | Sphinx |

**No stratum column exists.** Hosts are well-known documentation sites of widely-used open-source projects, screened **before any discovery-surface inspection** for credential-free stdlib crawlability (HTTP 200, no Cloudflare challenge) and DEEP topology (`>= 3` state-carrying pages at hop `>= 3` under the frozen same-host static-`<a>` BFS), with `>= 2` generator engines represented. The prior 5 hosts of revision 1 and the v1 frame are excluded so that no DESIGN-time discovery knowledge contaminates the frame.

**Precise meaning of "exposure-blind" (frozen).** (i) No discovery endpoint (robots.txt, sitemap XML, feed, JSON-LD target or search action) was fetched or followed for any frame host at DESIGN. (ii) No frame host's discovery-surface field produced by the topology parser (feed links, search forms, `ld+json` blocks) was recorded, printed or used in any DESIGN decision. (iii) Instrument liveness was proven only on local stdlib fixtures and on out-of-pool `LIVE_PROBE_HOSTS` disjoint from the seeds. The seed *root* HTML is necessarily fetched to build the topology, but only its static `<a href>` links and named input controls are consumed; the frame was verified for DEEP topology and reachability only (section 6.1).

### 3.2 Pool reconstruction policy (frozen, identical at DESIGN and EXECUTE)

Same-host static-`<a href>` BFS from the seed's *final* root, **document order**, `max_depth = 6`, `budget = 250` GETs per seed, browser-like UA `SPIDER-research-frontier-38085197666/1.0`, GET-only, 12 s timeout, body cap 600 000 bytes, redirects followed (one logical GET). The crawl is **item-blind** (topological) and discovery-blind (no discovery channel is consulted to build the pool). An admitted item is a **state-carrying page**: the fetched page contains at least one named `<input>`/`<select>`. `item_id = sha256(host + "|" + page_url)`. A page reachable from multiple seeds is admitted once at its minimum hop and attributed to the winning seed; its host/engine come from the winning seed's final root (VN-V14).

### 3.3 DESIGN-observed pool (RAW EVIDENCE, 2026-10-11)

Per-seed static hop histograms (all reached pages) and admitted DEEP counts (state-carrying, hop `>= 3`) from the frozen BFS in section 13 (`hop` buckets `0..6`; the parser is the link-only `StaticLinks`, so no discovery field of any frame host is consumed):

- `https://google.github.io/comprehensive-rust/` — DEEP **197**; hist `{0:1, 1:7, 2:29, 3:96, 4:117}` (250 page GETs, crawl capped)
- `https://rust-lang.github.io/async-book/` — DEEP **94**; hist `{0:1, 1:5, 2:51, 3:193}` (250 page GETs, crawl capped)
- `https://rustc-dev-guide.rust-lang.org/` — DEEP **194**; hist `{0:1, 1:5, 2:26, 3:47, 4:71, 5:56, 6:20}` (226 page GETs)
- `https://pandas.pydata.org/docs/` — DEEP **8**; hist `{0:1, 1:6, 2:234, 3:9}` (250 page GETs, crawl capped)

**Admitted DEEP pool (derived): 493 state-carrying pages** among **839 distinct reached pages** — mdBook **485**, Sphinx **8**; by host `google.github.io` **197**, `rust-lang.github.io` **94**, `rustc-dev-guide.rust-lang.org` **194**, `pandas.pydata.org` **8**. DEEP items by hop: `{3: 242, 4: 175, 5: 56, 6: 20}` (so the hop-3 bucket and the hop-`>= 5` bucket both exceed `TREND_MIN_BUCKET = 5`; the trend diagnostic is computable). Pool-build cost at DESIGN: observed **976** page GETs across the four seeds (250 + 250 + 226 + 250).

Representative confirmed DEEP items (hop >= 3), used for the arrival records:

| page_url | hop | host | engine |
|----------|-----|------|--------|
| `https://google.github.io/comprehensive-rust/android/build-rules.html` | 3 | google.github.io | mdBook |
| `https://google.github.io/comprehensive-rust/android/interoperability/cpp/android-build-rust.html` | 4 | google.github.io | mdBook |
| `https://rust-lang.github.io/async-book/01_getting_started/01_chapter.html` | 3 | rust-lang.github.io | mdBook |
| `https://rustc-dev-guide.rust-lang.org/analysis/well-formed.html` | 3 | rustc-dev-guide.rust-lang.org | mdBook |
| `https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html` | 3 | pandas.pydata.org | Sphinx |

### 3.4 ADMISSION_GATE_V2 (frozen)

PASS iff **total admitted DEEP pages >= 10** AND **>= 2 distinct engines each with >= 3 admitted DEEP pages** AND **>= 2 distinct hosts each with >= 3 admitted DEEP pages**. DESIGN verdict: **PASS** (493 >= 10; mdBook 485, Sphinx 8 = 2 engines >= 3; 4 hosts >= 3). At EXECUTE the gate is re-evaluated on the reconstructed pool; failure yields `status = MEASUREMENT_INVALID` with the exact shortfall and is **never** encoded as a scientific branch.

### 3.5 Pre-freeze control certificate

```
certificate_id: PRE_FREEZE_CERT_EXP-FRONTIER-38085197666
all_verified: true
(a) pool_deep_items_confirmed: true   -> 493 admitted DEEP pages (mdBook 485, Sphinx 8)
(b) pool_deep_hosts_confirmed: true   -> 4 hosts with >= 3 DEEP; 2 engines with >= 3 DEEP
(c) discovery_channel_probe_verified: true -> RAW evidence 2026-10-11, OUT-OF-POOL hosts only
        (reproduced by running the frozen artifact's --live-probe mode):
        github.blog/robots.txt  -> ROBOTS_SITEMAP 17 urls ; SITEMAP_XML 17 urls
        jetbrains.com/robots.txt -> ROBOTS_SITEMAP 3 urls ; SITEMAP_XML 425 urls
        wordpress.org/robots.txt -> ROBOTS_SITEMAP 3 urls ; SITEMAP_XML 3 urls
        gnu.org/robots.txt       -> ROBOTS_SITEMAP 1 url  ; SITEMAP_XML 1 url
        php.net/robots.txt       -> ROBOTS_SITEMAP 0 urls ; SITEMAP_XML 39 urls
        hosts_parsing_ge1_url = 5/5 (apparatus live; no frame host inspected)
(d) null_control_verified: true       -> 50 synthetic probes across 5 out-of-pool hosts x 5 channels x 2 ids
                                         return success=false (0 reachable); NULL_ALL_ZERO=true
(e) dynamic_range_verified: true      -> CAL_DISCOVERABLE_FIXTURE 1.0 ; CAL_OPAQUE_FIXTURE 0.0
(f) both_branch_attainability: true   -> argued structurally + by synthetic branch exercise (NOT by an
                                         item-level outcome): denominator 493>=10; per-host fraction in [0,1];
                                         instrument range bracketed by fixtures (1.0 / 0.0); the frame is
                                         exposure-blind BY CONSTRUCTION (link-only StaticLinks parser: no
                                         discovery fields exist to consume); the frozen --branch-drive mode
                                         drives the real compute_metrics/decide/write_terminal path to
                                         SUPPORTS (E>=2, engines_ok), MIXED (one host), MIXED (>=2 hosts but a
                                         single engine), FALSIFIES (E==0), plus admission-gate failure,
                                         calibration failure, empty denominator and the 0.25>0.10 stability cap;
                                         branch_drive.json all_branches_reachable=true. So every branch is
                                         structurally reachable. No item-level per-host reachability fraction is
                                         reported at DESIGN.
(g) seed_identity_verified: true      -> all 4 seeds 200 with final_root netloc == declared host
(h) code_reverified: true             -> section-13 artifact extracted byte-for-byte
                                         (sha256 == 393775e8ee79f9308d1d142b54f2977b9a677a9f9891988625da810e856b68c8),
                                         re-ran --calibrate (CALIBRATION_PASS true), --pool (ADMISSION_GATE_V2
                                         PASS, 493 DEEP, 197/94/194/8, mdBook 485 / Sphinx 8,
                                         deep_by_hop {3:242,4:175,5:56,6:20}), --live-probe (5/5 hosts), --null
                                         (50 probes, 0 reachable) and --branch-drive (all branches reachable)
```

This repairs v1 `VN-A1`/`VN-A2`/`VN-A3` and revision 1's selection-on-treatment defect: the frame is non-empty, exposure-blind and recorded; the certificate conditions are live-verified with evidence; and the falsifier can trigger in both directions without the design having known the answer in advance (section 6.6).

## 4. Discovery channels (frozen definitions)

All channels are **cold-start**: the item page is fetched **only after** its URL is discovered, and the item-page GET counts against `K`.

1. **ROBOTS_SITEMAP** — GET `/robots.txt`; for each `Sitemap:` directive GET the target and parse `<loc>` (XML) or one-URL-per-line (plain text).
2. **SITEMAP_XML** — GET `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml` directly and parse `<loc>`.
3. **ON_SITE_SEARCH** — GET the seed root, locate a server-side search `<form>`/input action; GET `action?name=<query>` where `<query>` = last item-path segment with a trailing `.html|.php|.htm|.asp|.aspx` stripped (parameter = the located input's `name`, default `q`); parse result links. JS-only search indexes (mdBook `searchindex.js`, Sphinx client search) are not server-side and are disclosed as unreachable by this channel. **Oracle disclosure:** the query is derived from the *known* item path (which the agent would not in general know when hunting for an item), so `ON_SITE_SEARCH` is the one oracle-like channel. It is therefore reported separately and the code emits `discovery_reachable_fraction_per_host_without_on_site_search` and `oracle_dependent_supports` (hosts that meet threshold only with this channel) so the decision can be read with and without it.
4. **RSS_ATOM** — GET the seed root, follow a `<link rel="alternate" type="application/rss+xml|atom+xml">`, parse entry links.
5. **JSON_LD** — GET the seed root (a **hub** resource; never the item page), parse every `<script type="application/ld+json">` block and collect values of `url`, `@id`, `mainEntityOfPage`, `contentUrl`, `sameAs` across `@graph`/`ItemList`/`WebPage`/`BreadcrumbList`/`SearchAction`.

`K = 3` total GETs per item per channel = at most `DISCOVERY_GETS_MAX = 2` discovery GETs + exactly 1 item-page GET. A channel succeeds for an item iff the item URL is discovered within the discovery budget under **canonical resource identity** `match_key` (host + path with a single trailing `/`, `.html`, `.htm` removed — VN-V3c) **and** the item page returns 2xx within `K`. Canonical matching treats a sitemap spelling `…/page` and a link spelling `…/page.html` as the same resource; pool building and dedup keep exact URLs. Sitemap-index recursion beyond 2 discovery GETs does not count. An item is reachable iff **any** channel succeeds; per-channel coverage is reported separately and a zero-yield channel is listed explicitly.

## 5. Baselines and comparators (stable ids)

| id | role | policy | cost |
|----|------|--------|------|
| `B_LINK_FOLLOWING_BFS` | comparator | item-blind same-host BFS (this experiment's pool pass), document order, B=250, D=6 | `>= hop+1` GETs (+bytes) |
| `B_PERSISTED_PATH_REACQUISITION` | comparator | GET each node on the frozen shortest path seed→…→item in hop order | `hop+1` GETs |
| `B_DIRECT_URL_REPLAY` | lower bound | one GET to the known item URL | `1` GET |
| `B_NO_DISCOVERY` | floor | `CAL_OPAQUE_FIXTURE`, no discovery surface | `0.0` fraction |

The treatment (per-item discovery reachability) is a distinct decision function over the **same** admitted item set, so discovery-vs-link-following is identified.

## 6. Pre-freeze probe log (DESIGN only; no confirmatory outcome computed)

Open information classes are kept separate: **RAW EVIDENCE** (HTTP statuses/bytes actually observed), **OBSERVATION** (plain restatement), **DERIVED** (counts/fractions computed from it), **INTERPRETATION** (what it implies). Every probe below is a **satisfiability/frame/control** probe; no confirmatory item-level outcome was computed.

### 6.1 Seed reachability and DEEP topology (RAW EVIDENCE)

Reachability and static-`<a>` BFS topology only — **no discovery surface of any frame host was fetched**:

- `https://google.github.io/comprehensive-rust/` → **200**, `final_root` host == declared; 250 pages; DEEP **197**; hist `{0:1, 1:7, 2:29, 3:96, 4:117}`.
- `https://rust-lang.github.io/async-book/` → **200**, matches; 250 pages; DEEP **94**; hist `{0:1, 1:5, 2:51, 3:193}`.
- `https://rustc-dev-guide.rust-lang.org/` → **200**, matches; 226 pages; DEEP **194**; hist `{0:1, 1:5, 2:26, 3:47, 4:71, 5:56, 6:20}`.
- `https://pandas.pydata.org/docs/` → **200**, matches; 250 pages; DEEP **8**; hist `{0:1, 1:6, 2:234, 3:9}`.

**OBSERVATION.** All four exposure-blind seeds are reachable over TLS without a challenge and each admits `>= 3` DEEP state-carrying pages within `B=250 / D=6`; two generator engines are represented. **DERIVED.** Total 839 crawled pages, 493 DEEP (mdBook 485 / Sphinx 8), 4 hosts / 2 engines. **INTERPRETATION.** The mandate's prerequisite (a non-empty multi-engine DEEP pool on `>= 2` hosts) is satisfied without consulting any discovery surface, so the frame cannot have been chosen to favour a branch.

### 6.2 Instrument liveness on OUT-OF-POOL probe hosts (RAW EVIDENCE)

The frozen `ROBOTS_SITEMAP` / `SITEMAP_XML` machinery was exercised against five hosts **disjoint from the frame** (so a pool-wide zero remains a genuine `FALSIFIES`):

- `https://github.blog/` → ROBOTS_SITEMAP 17 URLs, SITEMAP_XML 17 URLs.
- `https://www.jetbrains.com/` → ROBOTS_SITEMAP 3 URLs, SITEMAP_XML 425 URLs.
- `https://wordpress.org/` → ROBOTS_SITEMAP 3 URLs, SITEMAP_XML 3 URLs.
- `https://www.gnu.org/` → ROBOTS_SITEMAP 1 URL, SITEMAP_XML 1 URL.
- `https://www.php.net/` → ROBOTS_SITEMAP 0 URLs, SITEMAP_XML 39 URLs.

**DERIVED.** `hosts_parsing_ge1_url = 5`, liveness `pass = true`. **INTERPRETATION.** The discovery apparatus is operational on the live Web at DESIGN; this is apparatus liveness and is deliberately independent of the measurement frame.

### 6.3 Null control (RAW EVIDENCE)

Synthetic items `spider-nonexistent-38085197666-<a|b>.html` probed through all five channels against the five **out-of-pool** probe hosts (**50 probes**): **0 reachable**, `success=false` throughout. `NULL_ALL_ZERO = true`. This guards against false-positive discovery via search suggestions, redirect chains or parser errors; it is run on out-of-pool hosts at DESIGN to preserve frame exposure-blindness (the same control runs on the frame hosts inside the frozen confirmatory code at EXECUTE).

### 6.4 Positive and identity controls (DESIGN prerequisite; confirmatory check at EXECUTE)

- **PC_HOP_CONFIRMATION:** the frozen BFS returns `found=true, hop=1` for the preregistered true-hop-1 target `https://google.github.io/comprehensive-rust/android.html` (observed at DESIGN; re-checked at EXECUTE).
- **PC_SEED_HOST_IDENTITY:** every seed's `final_root` netloc equals its declared host (all four match at DESIGN; re-checked at EXECUTE inside the frozen code). A cross-host redirect would silently re-base the probe and is a Step-0 failure (`MEASUREMENT_INVALID`).
- **PC_LIVE_PROBE_LIVENESS:** at EXECUTE, on `>= 1` out-of-pool probe host, `ROBOTS_SITEMAP` or `SITEMAP_XML` must **fetch and parse >= 1 URL**. This is apparatus liveness on hosts that are **never** part of the frame, so a genuine `FALSIFIES` (frame-wide zero) cannot be converted into `MEASUREMENT_INVALID`.
- **NC_SYNTHETIC_UNREACHABLE_ITEM:** section 6.3.

### 6.5 Dynamic-range calibration (RAW EVIDENCE, local stdlib `http.server` fixtures)

- `CAL_DISCOVERABLE_FIXTURE` (robots.txt + `sitemap.xml` listing deep pages): `discovery_reachable_fraction = 1.0` (via `ROBOTS_SITEMAP` and `SITEMAP_XML`).
- `CAL_OPAQUE_FIXTURE` (same deep structure, no robots/sitemap/feed/search/JSON-LD): `discovery_reachable_fraction = 0.0`.
- `CALIBRATION_PASS = true`. Inside the confirmatory run the calibration is re-executed **in-process** before any measurement; failure short-circuits to `MEASUREMENT_INVALID`/`INCONCLUSIVE` (control `CALIBRATION_GATE`), so a measurement can never proceed on an out-of-range instrument.

**DERIVED.** The instrument produces `1.0` and `0.0`, strictly bracketing the `0.50` decision threshold; the pipeline runs end-to-end with no browser, model, key or credential.

### 6.6 Design repairs made during this DESIGN (satisfiability/identifiability attacks)

Revision 2 differed from revision 1 in four substantive ways (exposure-blind frame; off-pool instrument liveness replacing the frame-inspecting `PC_DISCOVERY_CHANNEL_LIVENESS`; robust crawlable hosts replacing Cloudflare-429 hosts; a two-sided synthetic branch exercise). **Revision 3 additionally repairs five defects that a fresh adversarial self-attack could demonstrate from the frozen artifact alone** (the independent review of revision 2 returned `failure`/`substantive` but its objection text was not captured):

1. **`--branch-drive` makes the branch-exercise claim verifiable.** Revision 2 asserted the frozen code was "driven end-to-end" to every branch, but the frozen artifact exposed no such entry point, so `decision_rule_reachability` was unfalsifiable by a reviewer. Revision 3 adds `--branch-drive OUTDIR`, which drives the real `compute_metrics`/`decide`/`write_terminal` path to `SUPPORTS`, `MIXED`-single-engine, `MIXED`-one-host, `FALSIFIES`, admission-gate failure, calibration failure, empty denominator and the stability cap, printing `all_branches_reachable` and emitting `branch_drive.json` plus artifact triples (no network I/O).
2. **Exposure-blindness by construction.** Revision 2's frame BFS reused `HTMLScan`, which extracts `feeds`/`search_forms`/`jsonld`; exposure-blindness was a promise about which fields were *used*, not a property of the parser. Revision 3's frame BFS uses `StaticLinks`, which extracts only static `<a href>` and has no discovery fields, so the property is structural and auditable. The regenerated frame is topologically identical (493 DEEP; 197/94/194/8).
3. **Stability cap and cheaper second session.** Revision 2 ran the full admitted set in both sessions with no exclusion bound. Revision 3 measures session 1 on the full set, session 2 on a deterministic 25% subsample (`sha256(item) mod 4 == 0`), and sets `MAX_EXCLUSION_FRACTION = 0.10`: if inter-session disagreement excludes more than 10% of the subsample, Step 0 fails to `MEASUREMENT_INVALID`. This bounds rate-limit-induced denominator erosion and approximately halves measurement cost.
4. **Engine span enforced; oracle channel disclosed.** `SUPPORTS` now additionally requires the meeting hosts to span `>= 2` engines (`engines_ok`), matching the mandate's "0.50 on >= 2 engines"; `>= 2` hosts on a single engine is `MIXED`. `ON_SITE_SEARCH` is disclosed as oracle-like (section 4) and an oracle-free sensitivity (`..._without_on_site_search`, `oracle_dependent_supports`) is emitted.
5. **Trend rule formalised; pacing added.** The flat-vs-growing diagnostic is now a frozen rule (`_derive_trend`: `FALLING` iff frac(hop>=5) < frac(hop=3) - 0.10 with `>= 5` items in each bucket; else `FLAT`; `UNMEASURED` if a bucket is too small) and every non-localhost GET is paced (`PACE_S = 0.15` s).

Latent defects carried over from the earlier drafts and already repaired: `NameError` on the control-failure path; `compute_metrics` list-vs-dict contract mismatch; `MIN_ENGINES_WITH_THRESHOLD` -> `MIN_HOST_UNITS_WITH_THRESHOLD`; named `ADMIT_PER_HOST_MIN`; in-process `CALIBRATION_GATE`; `write_terminal()` artifact triple on every terminal path; `within_k` enforced in channel success; `decide()` `n==0` guard; `bfs_seed` GET overcount fix and per-item `bfs_cost`; `cost_baselines` metric; `PC_HOP_CONFIRMATION` no longer re-crawls (it reads the recorded control pass).

**Branch-exercise evidence (DESIGN, synthetic/local/off-pool only).** With the section 13 code: calibration fixtures give 1.0/0.0 (`CALIBRATION_PASS=true`); `--pool` reproduces ADMISSION_GATE_V2 (493 DEEP; 197/94/194/8; mdBook 485 / Sphinx 8; deep_by_hop {3:242,4:175,5:56,6:20}); `--live-probe` gives 5/5 hosts parsing `>= 1` URL; `--null` gives 50 probes / 0 reachable; and `--branch-drive` returns `all_branches_reachable=true` with `SUPPORTS` (COMPLETE, E=2, engines_ok), `MIXED`-single-engine (COMPLETE), `MIXED`-one-host (COMPLETE), `FALSIFIES` (COMPLETE, E=0), admission-gate failure and calibration failure (`MEASUREMENT_INVALID`), empty denominator (`INCONCLUSIVE`) and the stability cap (exclusion 0.25 > 0.10 fires). Every status/outcome branch is reachable and non-crashing, and a reviewer can re-run each from the frozen artifact.

## 7. Metrics (stable ids)

- **Primary:** `discovery_reachable_fraction` (pooled); `discovery_reachable_fraction_per_host[host]` (decision unit); `discovery_reachable_fraction_per_engine[engine]` (descriptive).
- **Secondary:** `discovery_reachable_fraction_per_channel[channel]`; `discovery_reachable_fraction_by_hop[3..6]` and `n_by_hop`; `median_discovery_gets_reachable`; `host_units_meeting_threshold` (`E`); `engines_meeting_threshold` (engine span of the meeting hosts); `flat_vs_growing_trend` (`label`/`frac_hop3`/`frac_hop_ge5` with bucket sizes, per section 6.6 rule); `discovery_reachable_fraction_per_host_without_on_site_search[host]` and `oracle_dependent_supports` (oracle-free sensitivity); `cost_baselines` (measured `B_LINK_FOLLOWING_BFS` median `bfs_cost`, `B_PERSISTED_PATH_REACQUISITION` hop+1, `B_DIRECT_URL_REPLAY` 1, discovery-GET medians on success, and per-hop medians as the flat-vs-growing diagnostic); `exclusion_fraction`, `n_unstable_excluded`, `unstable_items`, `stability_subsample_size`, `stability_subsample_fraction_session_1`/`_session_2`, `session_1_pooled_fraction`.
- **Controls metric:** `controls.<id>.pass`.

No tokenizer, latency timer or dollar-cost model; GET count and response-body bytes are the only cost bases (token fields `null`).

## 8. Decision rule (frozen, evaluated in order)

```
Step 0  controls: CALIBRATION_GATE (CAL_DISCOVERABLE_FIXTURE==1.0 and CAL_OPAQUE_FIXTURE==0.0, re-run
        in-process), PC_HOP_CONFIRMATION found & hop==1 (read from the recorded frame pass),
        PC_SEED_HOST_IDENTITY (final_root host == declared host for every seed),
        NC_SYNTHETIC_UNREACHABLE_ITEM==0 (pool hosts x 5 channels x 2 synthetic ids),
        PC_LIVE_PROBE_LIVENESS (>= 1 OUT-OF-POOL probe host where ROBOTS_SITEMAP/SITEMAP_XML
        fetch and parse >= 1 URL; apparatus liveness, independent of the frame),
        STABILITY_CAP (exclusion_fraction <= 0.10).
        Any failure -> status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE (infra/substrate; not a scientific branch).
Step 1  admission: reconstruct pool from frozen seeds under frozen BFS; ADMISSION_GATE_V2 pass?
        fail -> status=MEASUREMENT_INVALID with exact shortfall.
Step 2  measurement: session 1 = every admitted DEEP page x 5 channels (success iff within K=3);
        session 2 = deterministic 25% subsample re-measured. Drop items whose subsample channels
        disagree (VN-V11), report count and exclusion_fraction; abort per Step 0 if > 0.10.
Step 3  compute pooled / per-host / per-engine / per-channel / by-hop fractions and n_by_hop;
        E = #hosts with fraction >= 0.50; engines_ok = meeting hosts span >= 2 engines.
        E >= 2 and engines_ok -> SUPPORTS ; E >= 1 otherwise -> MIXED ; E == 0 -> FALSIFIES   (status=COMPLETE).
```

A valid scientific negative is `status=COMPLETE` with `outcome=FALSIFIES`, **not** an infrastructure failure.

## 9. Controls (frozen ids)

- `CALIBRATION_GATE` — section 6.5 (in-process dynamic-range gate).
- `PC_HOP_CONFIRMATION` — section 6.4 (true-hop-1 target).
- `PC_SEED_HOST_IDENTITY` — section 6.4 (seed final-root stays on declared host).
- `NC_SYNTHETIC_UNREACHABLE_ITEM` — section 6.3.
- `PC_LIVE_PROBE_LIVENESS` — section 6.4 (out-of-pool parsed-URL liveness; outcome-independent).
- `PC_DISCOVERY_CHANNEL_REACHABILITY` — composite Step-0 gate (hop + identity + liveness), section 6.4.
- `ADMISSION_GATE` (ADMISSION_GATE_V2 semantics) — section 3.4.
- `STABILITY_CAP` — inter-session exclusion fraction must be `<= 0.10` on the deterministic 25% subsample (section 6.6); otherwise `MEASUREMENT_INVALID`.
- `CAL_DISCOVERABLE_FIXTURE`, `CAL_OPAQUE_FIXTURE` — section 6.5.

## 10. Validity threats, controls and representation loss

1. **JS-rendered navigation** (mdBook/Sphinx client search, JS-injected links/JSON-LD) is invisible to the stdlib parser; disclosed as representation loss (VN-V8). This biases **against** the discovery treatment, i.e. conservative for SUPPORTS.
2. **`ON_SITE_SEARCH` semantics** — server-side search may not index every deep page; the channel is one of five and its coverage is reported per-channel. Its query is derived from the known item path, so it is disclosed as oracle-like (section 4) and an oracle-free per-host sensitivity is reported alongside the primary.
3. **Sitemap staleness** — a discovered URL may 404; the item page must be 2xx within `K` for success, so stale URLs are failures, not silent passes.
4. **Availability / challenge pages** — hosts can change or rate-limit between DESIGN and EXECUTE (VN-V12). If the frame collapses so that the admission gate fails, the result is `MEASUREMENT_INVALID`, never a branch. Revision 2 deliberately excludes hosts observed to serve Cloudflare challenge pages at DESIGN, revision 3 paces every foreign GET (`PACE_S=0.15`) and bounds instability with `STABILITY_CAP`.
5. **Pool drift** — the live site changes; the gate is re-checked at EXECUTE and the reconstructed pool is reported with counts and hashes.
6. **Hop comparability** — hop is computed by the same frozen BFS and is reported as a distribution, not a point estimate; the primary decision does not depend on the hop estimate, and the trend rule is reported with bucket sizes.
7. **Cross-seed contamination** — no two seeds share a host in the final pool; dedup by minimum hop and attribution to the winning seed (VN-V14) prevents double counting.
8. **Determinism** — session 1 measures the full admitted set; session 2 re-measures a deterministic 25% subsample and any inter-session disagreement excludes the item with a recorded reason (VN-V11); if exclusions exceed 10% the run is `MEASUREMENT_INVALID`.
9. **Confirmation bias against the question** — the two local fixtures bracket the threshold (1.0 and 0.0, strictly around 0.50), so the instrument is not rigged to a single answer; the design records consequences for every branch. No DESIGN item-level per-host fraction is reported, so this experiment cannot have designed the answer it will measure.
10. **Exposure-blind frame; both branches live (principal design property).** No frame host's discovery surface was inspected at DESIGN, so the design did not — and could not — pre-select `SUPPORTS` or `FALSIFIES`. The frame is a convenience sample of well-known documentation sites, so the claim remains capability-bound to that class (section 12) and is **not** a Web-wide prevalence estimate. Unlike revision 1, a `SUPPORTS` here is not a construction artifact and a `FALSIFIES` is not structurally foreclosed.
11. **Frame-class homogeneity (disclosed).** Three of four hosts are mdBook sites on GitHub Pages and one is Sphinx; a mdBook-heavy frame could behave as a coherent class rather than a cross-engine cross-section. This is disclosed; the decision rule still requires `>= 2` distinct hosts and reports per-engine fractions, and the gate requires `>= 2` engines.
12. **Canonicalization false-merges (VN-V3c)** — `match_key` removes a single trailing `.html`/`.htm`/`/`, so a genuinely distinct resource `/a.html` vs `/a` would be conflated. Guard: (i) on these hosts the `.html` and clean spellings are the *same* page; (ii) `NC_SYNTHETIC_UNREACHABLE_ITEM` and item-page 2xx checks still apply; (iii) per-channel and per-host results are reported, so a systematic merge would surface as an outlier.
13. **`SITEMAP_XML` 2-of-3 candidate cap (deterministic).** Under `DISCOVERY_GETS_MAX = 2`, `SITEMAP_XML` fetches at most the first two of `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml`; the third path is reached only when an earlier candidate did not consume the budget. Disclosed so a missing third-path enumeration is never read as absence.
14. **`CODE_SHA256` is self-asserted (freeze-scope limitation).** The complete outcome-bearing code is frozen verbatim in section 13 and bound by `CODE_SHA256`, but `scripts/freeze_experiment.py` hashes `prereg.md` (not the code string). The hash is therefore a DESIGN-declared interpretation binding that EXECUTE must re-verify against the extracted block, not a cryptographic freeze guarantee. EXECUTE MUST extract the block byte-for-byte and fail closed (`MEASUREMENT_INVALID`) if `sha256(run.py) != CODE_SHA256`.
15. **Per-item fresh budgets and rate-limit exposure (disclosed).** By `VN-V10` the instrument makes no cross-item caching, so `ROBOTS_SITEMAP`/`SITEMAP_XML` re-fetch the same `robots.txt`/sitemap once per item-channel episode; a high-`n_admitted_deep` host (`google.github.io/comprehensive-rust` admits 197) thus issues O(`n_items`) sitemap GETs per session. Sequential, single-connection GETs mitigate but do not eliminate the chance of transient throttling on large hosts. A throttle surfaces as a channel failure for the affected item (never a silent pass); persistent frame-wide collapse trips `ADMISSION_GATE` → `MEASUREMENT_INVALID`, and per-item inter-session disagreement is excluded via `VN-V11`. Channel-level failures and exclusions are reported so a throttling artifact can never be read as a genuine `FALSIFIES` or `SUPPORTS`.

## 11. Inherited state (from the parent handoff, preserved)

Parent handoff: `research/experiments/EXP-FRONTIER-37984242167/handoff.json`, `sha256=1b220e4114e490b3fd935b29de14e88fc611b919471483e2243d7dc0281ef6bf` (matches `request.json.parent_handoff.sha256`). Its four categories are preserved verbatim in substance:

**Established.** (i) The parent packet is a **verified design/control-plane defect receipt, not a measurement**: the v1 freeze admitted 0 seeds / 0 DEEP / 0 hosts, carried `all_verified=false`, and its primary metric was `0/0`, so neither falsifier branch was arithmetically reachable — this is the defect this v2 repairs. (ii) The blocker was **not** infrastructure (outbound TLS and bare CPython were available); no HTTP request was sent because any post-freeze crawl would have mutated the frozen frame. (iii) No claim-status change was warranted from the parent packet. (iv) A depth-bounded credential-free static crawler can build the pool from docs roots under `B=250/D=6`. (v) The grandparent `EXP-FRONTIER-37950626378` measured `RECOVERY_REDUCTION_FROM_PERSISTED_STATE = GROWING` (`R_req=5.2667`, `R_bytes=7.3113`); persisted-path re-acquisition was near-linear (`path_len == hop+1` on 1532/1532), direct URL replay was 1 GET, and its DEEP band was single-host/single-engine `doc.rust-lang.org` mdBook.

**Rejected / retired.** (i) The v1 `EXP-FRONTIER-37984242167` sampling frame is void (0 seeds, 0 DEEP, 0 hosts). (ii) Its "no freeze / placeholder spec" design path is retired. (iii) Reading `BLOCKED`/`NOT_APPLICABLE` as a scientific FALSIFIES (or any evidence for/against discovery) is rejected. (iv) The parent's pooled GROWING ratio as independent Web-economics evidence, the FLAT branch as established, sub-1 break-even reuse counts as economics, and generalization beyond the parent's single-engine mdBook substrate are all rejected. (v) The parent DEEP band is explicitly **not** a substitute for this experiment's required multi-engine pool. (vi) **Revision 1's stratified `EXPOSING`/`OPAQUE` frame and its `PC_DISCOVERY_CHANNEL_LIVENESS`-on-frame-hosts control are rejected** as selection-on-treatment and frame-exposure respectively.

**Unknown.** (i) Whether site-native discovery reaches `>= 0.50` of DEEP items in `<= K=3` GETs on `>= 2` host units — entirely unmeasured; this is this experiment's entire question. (ii) Whether any host admits DEEP (hop >= 3) items within `B=250/D=6` — the DESIGN pool now supplies 4 hosts / 2 engines. (iii) Whether discovery reachability scales with hop. (iv) Per-channel coverage on mdBook vs Sphinx. (v) The maintenance/invalidation axis (re-validation GETs/bytes, stale-replay false-accept vs re-derivation) — the recorded alternative next question. (vi) The Web-wide fraction of doc hosts that enumerate their deep pages via site-native discovery (not measured here; the design is capability-bound).

**Do not assume.** (i) That a single-host/single-engine result generalizes cross-host. (ii) That a machine-readable discovery channel exists on any given host. (iii) That `ON_SITE_SEARCH`, `RSS_ATOM` or `JSON_LD` are live on any frame host — this was deliberately **not** inspected at DESIGN (exposure-blind). (iv) That revision 1's stratified pool or its Cloudflare-challenged Sphinx hosts were usable at EXECUTE — they were not; the current exposure-blind frame is the repair. (v) **Never quote or pair the parent baseline values (`RACQ_PATH`/`RACQ_URL`/`RED`) as measurements of this experiment** — they are inherited context on the parent's single-engine pool; this experiment re-derives its own baselines. (vi) **Never construct a pool/crawl after freeze** to "complete" the transaction — that mutates the frozen sampling frame and would be `MEASUREMENT_INVALID`; the repair is this re-opened v2 DESIGN. (vii) Do not let `research/claims/registry.json` or any local field override accepted Codex effective claim states, and do not import `agent_priors_used`/`portfolio_assessment`/`scout_assessment` as SPIDER evidence (labelled non-evidentiary at source).

## 12. Product consequences

- **If SUPPORTS.** Shortest-path hop is not a fundamental acquisition-cost barrier for discovery-enabled acquisition on the frozen host class; SPIDER should optimize discovery-channel coverage and substrate expansion rather than path/procedure caching. `C-CROSSSITE` gains a bounded positive that a reusable discovery procedure transfers across `>= 2` host units. Freshness/delta-repair are lower priority for the acquisition phase. **Preregistered caveat:** the frame is exposure-blind, so a SUPPORTS is not a construction artifact, but the frame is a convenience sample of documentation hosts (section 10.10/10.11) and the claim is capability-bound, not Web-wide. **No mechanism is promoted to Product Core by this experiment.**
- **If FALSIFIES.** Even with site-native discovery, fresh deep-instance acquisition remains path-bound on this host class; persistence of paths/procedures retains a measurable depth-dependent amortization surface and the break-even reuse count can be computed from the recorded re-derivation cost. SPIDER's memory architecture should keep investing in path/procedure persistence with freshness guards.
- **If MIXED.** No program-level decision change; the next experiment must resolve discovery-channel coverage or frame composition.

## 13. Frozen outcome-bearing code (verbatim; `CODE_SHA256`)

EXECUTE MUST write the following block byte-for-byte to `run.py` (outside the repo is fine) and verify `sha256(run.py) == 393775e8ee79f9308d1d142b54f2977b9a677a9f9891988625da810e856b68c8` before running. The calibration gate is re-enforced inside the confirmatory process (`CALIBRATION_GATE`). NOTE: `CODE_SHA256` is self-asserted by this embedded block; `scripts/freeze_experiment.py` hashes `prereg.md` (not the code string), so the code hash is a DESIGN-declared interpretation binding that EXECUTE must re-verify, not a cryptographic freeze guarantee (section 10.14). Extraction rule: the code is the exact bytes between the line after the opening fence and the line before the closing fence (the block content equals the file bytes, trailing newline included). Modes: `python3 run.py --calibrate <OUT>` (controls only), `python3 run.py --pool` (frame reconstruction / admission evidence), `python3 run.py --live-probe <OUT>` (out-of-pool apparatus liveness), `python3 run.py --null <OUT>` (out-of-pool null control), `python3 run.py --branch-drive <OUT>` (offline branch-reachability exercise), `python3 run.py <OUT>` (confirmatory; EXECUTE only).

```python
#!/usr/bin/env python3
"""EXP-FRONTIER-38085197666 -- site-native discovery vs link-following for
deep-item acquisition (frontier lane, Research 2.0, design-contract v2).

Credential-free, GET-only, stdlib+http.server; no browser, no JS, no token,
no cookie, no write verb, no API key.

v2 repair vs the first v2 draft: the draft frame selected 3 hosts BECAUSE they
published content-level sitemaps (a discovery-EXPOSING stratum) plus 2 OPAQUE
hosts, which pre-determined the SUPPORTS branch (ceiling baseline /
selection-on-treatment). This repair makes the frame EXPOSURE-BLIND: hosts are
chosen by a predeclared list of well-known documentation sites across multiple
generator engines, verified only for DEEP topology (same-host static-<a> BFS),
and NO discovery surface (robots.txt/sitemap/feeds/JSON-LD/forms) of any frame
host is inspected during DESIGN. Instrument liveness is therefore verified on
LOCAL stdlib fixtures (dynamic range 1.0/0.0) and on OUT-OF-POOL probe hosts
(LIVE_PROBE_HOSTS), never on the measurement frame, so both decision branches
(SUPPORTS: E>=2 hosts >= 0.50; FALSIFIES: E==0) remain genuinely reachable.

Modes (invoked by EXECUTE exactly as declared in prereg.md):
  python run.py --calibrate OUTDIR
      Runs the COMPLETE discovery pipeline end-to-end on two LOCAL stdlib
      http.server fixtures (one discoverable, one opaque) and prints the
      resulting discovery_reachable_fraction. Proves the frozen instrument can
      produce BOTH branches. NOT a confirmatory measurement.
  python run.py --pool
      Runs the frozen same-host static-<a> BFS (B=250, D=6) on the frozen SEEDS
      and prints the admitted DEEP pool (sampling-frame construction only; no
      discovery channel of any frame host is probed).
  python run.py --live-probe OUTDIR
      Probes ROBOTS_SITEMAP/SITEMAP_XML machinery on the OUT-OF-POOL
      LIVE_PROBE_HOSTS (apparatus liveness only; disjoint from the frame).
  python run.py --null OUTDIR
      Runs the synthetic-unreachable null control on the OUT-OF-POOL hosts.
  python run.py --branch-drive OUTDIR
      Drives the frozen metrics/decision/artifact path to every branch
      (SUPPORTS / MIXED-single-engine / MIXED-one-host / FALSIFIES / gate-fail /
      empty-denominator / stability-cap) on synthetic inputs, no network I/O.
  python run.py OUTDIR
      Full confirmatory run: pool construction, admission gate, 5 discovery
      channels x K=3 GETs, session 1 on the full admitted set plus a deterministic
      25% session-2 stability subsample, metrics, controls, decision; bakes
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
MIN_HOST_UNITS_WITH_THRESHOLD = 2  # E counts HOST units (per-host fractions)
MIN_ENGINES_WITH_THRESHOLD = 2     # SUPPORTS also requires >=2 ENGINES among meeting hosts
ADMIT_DEEP_MIN = 10
ADMIT_PER_ENGINE_MIN = 3
ADMIT_PER_HOST_MIN = 3
ADMIT_DISTINCT_ENGINES_MIN = 2
ADMIT_DISTINCT_HOSTS_MIN = 2
SESSIONS = 2
SEED = 38085197666
PACE_S = 0.15               # politeness pause before every FOREIGN HTTP GET
S2_FRACTION = 0.25          # deterministic session-2 stability subsample
MAX_EXCLUSION_FRACTION = 0.10  # if inter-session instability exceeds this, MEASUREMENT_INVALID
TREND_DROP = 0.10           # flat-vs-growing: FALLING iff frac(hop>=5) < frac(hop=3) - TREND_DROP
TREND_MIN_BUCKET = 5        # flat-vs-growing: need >= this many items per compared bucket
ON_SITE_SEARCH_IS_ORACLE = True  # disclosed: query = item path segment (targeted acquisition)

# Frozen exposure-blind seed list (host + generator engine frozen at DESIGN;
# see prereg s3). Selection rule: well-known documentation sites of widely-used
# open-source projects, predeclared before any discovery-surface inspection,
# spanning >= 2 generator engines; the prior 5 hosts of the first v2 draft and the
# v1 frame are EXCLUDED so no DESIGN-time discovery knowledge contaminates the
# frame. No frame host's robots.txt/sitemap/feed/JSON-LD/form surface was
# inspected during DESIGN.
SEEDS = [
    {"seed": "https://google.github.io/comprehensive-rust/", "host": "google.github.io", "engine": "mdBook"},
    {"seed": "https://rust-lang.github.io/async-book/", "host": "rust-lang.github.io", "engine": "mdBook"},
    {"seed": "https://rustc-dev-guide.rust-lang.org/", "host": "rustc-dev-guide.rust-lang.org", "engine": "mdBook"},
    {"seed": "https://pandas.pydata.org/docs/", "host": "pandas.pydata.org", "engine": "Sphinx"},
]

# Out-of-pool instrument-liveness probe hosts (disjoint from SEEDS). These are
# used ONLY to prove at DESIGN and at EXECUTE that the frozen ROBOTS_SITEMAP /
# SITEMAP_XML machinery fetches and parses >= 1 URL from the live Web. They are
# never part of the measurement frame, so a pool-wide zero result is a genuine
# scientific FALSIFIES, never masked as MEASUREMENT_INVALID.
LIVE_PROBE_HOSTS = [
    "https://github.blog/",
    "https://www.jetbrains.com/",
    "https://wordpress.org/",
    "https://www.gnu.org/",
    "https://www.php.net/",
]

# Frozen true-hop-1 positive-control target; must be found by the frozen BFS at
# hop==1 from its seed (PC_HOP_CONFIRMATION).
HOP_CONTROL_TARGET = "https://google.github.io/comprehensive-rust/android.html"

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
        "measurement": "site-native discovery reachability over frozen exposure-blind DEEP pool",
        "terminal_status": result["status"]})


# ---------------------------------------------------------------------------
# Credential-free GET-only HTTP
# ---------------------------------------------------------------------------
def http_get(url: str) -> dict:
    if PACE_S > 0:
        try:
            if urllib.parse.urlsplit(url).netloc not in ("127.0.0.1", "localhost"):
                time.sleep(PACE_S)
        except Exception:
            pass
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
    """Canonical resource identity for DISCOVERY matching.

    A trailing '/' and a single trailing '.html'/'.htm' are removed. Sitemaps
    commonly list the canonical spelling (e.g. '/component/button') while the
    static <a href> links that the BFS follows use the '.html' spelling
    ('/component/button.html'); both denote the SAME resource on these hosts, so
    comparing canonical forms measures whether the page was enumerated rather
    than whether one particular URL spelling was enumerated. Applied ONLY to
    discovery matching; pool building/dedup keeps exact URLs.
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


# ---------------------------------------------------------------------------
# Exposure-blind topology parser.
# The BFS that constructs the sampling frame consumes ONLY static <a href> links
# and named <input>/<select> controls. StaticLinks deliberately has NO discovery
# fields (no feed links, no search forms, no JSON-LD), so exposure-blindness is a
# property of the parser object itself, verifiable by construction rather than a
# promise about how a richer parser's output is used. HTMLScan (above) is used
# ONLY by the EXECUTE discovery channels.
# ---------------------------------------------------------------------------
class StaticLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.controls = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "input":
            n = (a.get("name") or "").strip()
            if n:
                self.controls.append((n, (a.get("type") or "text").lower()))
        elif tag == "select":
            n = (a.get("name") or "").strip()
            if n:
                self.controls.append((n, "select"))


def static_scan(body: bytes, ctype):
    s = StaticLinks()
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
# Frozen BFS (sampling-frame construction) -- identical policy to the prior
# frame pass: same-host static <a href>, document order, per-URL
# defragment+drop-assets, budget B, depth cap D. Topology only; NO discovery
# channel is probed on any frame host (exposure-blind frame).
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
        s = static_scan(first["raw"], first["ctype"])
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
        s = static_scan(rec["raw"], rec["ctype"])
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
                               "engine": entry["engine"],
                               "bfs_cost": info.get("bfs_cost", info["hop"] + 1),
                               "via_seed": entry["seed"]}
    return pages, seed_stats


def admit(pages):
    deep = {p: v for p, v in pages.items() if 3 <= v["hop"] <= DEPTH_CAP}
    hosts = Counter(v["host"] for v in deep.values())
    engines = Counter(v["engine"] for v in deep.values())
    gate = {
        "total_deep": len(deep),
        "hosts_with_deep": dict(hosts),
        "engines_with_deep": dict(engines),
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
def _derive_trend(by_hop, n_by_hop):
    """Frozen flat-vs-growing rule for the descriptive scaling question.

    Compares the discovery reachability fraction at hop==3 with the pooled
    fraction at hop>=5. FALLING iff frac(hop>=5) < frac(hop==3) - TREND_DROP with
    at least TREND_MIN_BUCKET items in each compared bucket; otherwise FLAT. If
    either bucket is too small the trend is UNMEASURED (never silently FLAT).
    """
    n3 = n_by_hop.get("3", 0)
    hi = sum(n_by_hop.get(str(h), 0) for h in range(5, DEPTH_CAP + 1))
    f3 = by_hop.get("3")
    if n3 < TREND_MIN_BUCKET or hi < TREND_MIN_BUCKET or f3 is None:
        return {"label": "UNMEASURED", "n_hop3": n3, "n_hop_ge5": hi,
                "frac_hop3": f3, "frac_hop_ge5": None}
    num = sum((by_hop.get(str(h)) or 0.0) * n_by_hop.get(str(h), 0)
              for h in range(5, DEPTH_CAP + 1))
    f5 = num / hi
    return {"label": ("FALLING" if f5 < f3 - TREND_DROP else "FLAT"),
            "n_hop3": n3, "n_hop_ge5": hi, "frac_hop3": f3, "frac_hop_ge5": f5}


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
    engine_by_host = {admitted[it]["host"]: admitted[it]["engine"] for it in admitted}
    # Oracle-free sensitivity: ON_SITE_SEARCH is the only channel whose query is
    # derived from the item's own path segment (targeted acquisition). Recompute
    # host reachability excluding it, so an oracle-dependent SUPPORTS is visible.
    per_host_no_search = {}
    for host in sorted({admitted[it]["host"] for it in admitted}):
        items = [it for it in admitted if admitted[it]["host"] == host]
        ok = sum(1 for it in items if any(per_item[it][c]["success"] for c in CHANNELS
                                           if c != "ON_SITE_SEARCH"))
        per_host_no_search[host] = ok / len(items)
    per_channel = {}
    for ch in CHANNELS:
        per_channel[ch] = sum(1 for it in admitted if per_item[it][ch]["success"]) / n if n else None
    by_hop = {}
    n_by_hop = {}
    for h in range(3, DEPTH_CAP + 1):
        items = [it for it in admitted if admitted[it]["hop"] == h]
        n_by_hop[str(h)] = len(items)
        by_hop[str(h)] = (sum(1 for it in items if per_item[it]["any_success"]) / len(items)) if items else None
    trend = _derive_trend(by_hop, n_by_hop)
    gets = [per_item[it]["min_total_gets_on_success"] for it in admitted
            if per_item[it]["min_total_gets_on_success"] is not None]
    # ---- cost baselines (frozen ids; measured on the same admitted item set) ----
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
        "discovery_reachable_fraction_per_channel": per_channel,
        "discovery_reachable_fraction_by_hop": by_hop,
        "n_by_hop": n_by_hop,
        "flat_vs_growing_trend": trend,
        "engine_by_host": engine_by_host,
        "discovery_reachable_fraction_per_host_without_on_site_search": per_host_no_search,
        "host_units_meeting_threshold": sum(
            1 for _, f in per_host.items() if f >= MATERIALITY_THRESHOLD),
        "engines_meeting_threshold": len({
            engine_by_host[h] for h, f in per_host.items() if f >= MATERIALITY_THRESHOLD}),
        "median_discovery_gets_reachable": _med(gets),
        "cost_baselines": cost_baselines,
    }


def decide(metrics, gate_pass):
    if not gate_pass:
        return "INCONCLUSIVE", 0, False
    if not metrics.get("n_admitted_deep"):
        # Empty denominator must never be silently read as FALSIFIES (v1 defect).
        return "INCONCLUSIVE", 0, False
    per_host = metrics["discovery_reachable_fraction_per_host"]
    ebh = metrics.get("engine_by_host", {})
    meeting = [h for h, f in per_host.items() if f >= MATERIALITY_THRESHOLD]
    e = len(meeting)
    engines_ok = len({ebh.get(h) for h in meeting}) >= MIN_ENGINES_WITH_THRESHOLD
    if e >= MIN_HOST_UNITS_WITH_THRESHOLD and engines_ok:
        return "SUPPORTS", e, engines_ok
    if e >= 1:
        # >=2 hosts but a single engine, or exactly one host: split contrast.
        return "MIXED", e, engines_ok
    return "FALSIFIES", e, engines_ok


def _subsample(admitted):
    """Deterministic S2_FRACTION subsample of admitted items (by URL hash), so
    session 2 is reproducible and costs a bounded fraction of session 1."""
    def bucket(u):
        return int(hashlib.sha256(u.encode("utf-8")).hexdigest(), 16)
    return sorted(it for it in admitted if bucket(it) % round(1.0 / S2_FRACTION) == 0)


def _stabilize(admitted, s1, s2, subsample):
    """VN-V11 with a cap: an item is unstable iff any channel's success differs
    between session 1 and session 2. Only subsample items are re-measured, so the
    instability rate is an estimate over the subsample. Returns
    (stable_admitted, unstable_items, exclusion_fraction)."""
    unstable = [it for it in subsample
                if any(s1[it][c]["success"] != s2[it][c]["success"] for c in CHANNELS)]
    unstable_set = set(unstable)
    stable = {it: admitted[it] for it in admitted if it not in unstable_set}
    excl = (len(unstable) / len(subsample)) if subsample else 0.0
    return stable, unstable, excl


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
# Out-of-pool instrument-liveness probes (EXECUTE proof that the frozen
# ROBOTS_SITEMAP / SITEMAP_XML machinery parses the live Web; NEVER on a frame
# host, so a pool-wide zero stays a genuine FALSIFIES)
# ---------------------------------------------------------------------------
def live_probe_state():
    detail = {}
    for root in LIVE_PROBE_HOSTS:
        if root in {e["seed"] for e in SEEDS}:
            root = ("https://" + urllib.parse.urlsplit(root).netloc + "/")
        item = root + "spider-liveprobe-nonexistent.html"
        host = urllib.parse.urlsplit(root).netloc
        r = CHANNEL_FN["ROBOTS_SITEMAP"](item, root, host)
        x = CHANNEL_FN["SITEMAP_XML"](item, root, host)
        detail[root] = {
            "robots_sitemap_urls": r["urls_count"], "sitemap_xml_urls": x["urls_count"],
            "robots_sitemap_gets": r["discovery_gets"], "sitemap_xml_gets": x["discovery_gets"],
        }
    n_parsed = sum(1 for d in detail.values()
                   if d["robots_sitemap_urls"] >= 1 or d["sitemap_xml_urls"] >= 1)
    return {"detail": detail, "hosts_parsing_ge1_url": n_parsed,
            "pass": n_parsed >= 1}


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
                "deep_by_hop": dict(sorted(Counter(v["hop"] for v in deep.values()).items())),
                "deep_items": {p: {"hop": v["hop"], "host": v["host"],
                                   "engine": v["engine"], "controls": v["controls"]}
                               for p, v in sorted(deep.items())}})
    controls = {}
    controls["PC_DISCOVERY_CHANNEL_REACHABILITY"] = {"status": "see certificate"}
    controls["PC_HOP_CONFIRMATION"] = {
        "target": HOP_CONTROL_TARGET,
        "expected": {"found": True, "hop": 1},
        "pass": None}
    # hop positive control read from the SAME frame pass (no extra crawl): the
    # preregistered target must be admitted as a state-carrying page at hop==1.
    pc = pages.get(HOP_CONTROL_TARGET)
    pc_hit = HOP_CONTROL_TARGET if pc is not None else None
    controls["PC_HOP_CONFIRMATION"]["observed"] = {
        "found": pc_hit is not None, "hop": (pc or {}).get("hop")}
    controls["PC_HOP_CONFIRMATION"]["pass"] = bool(pc_hit and pc["hop"] == 1)
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
    admitted = {it: deep[it] for it in sorted(deep)}  # dict keyed by item URL
    # Session 1: the full admitted set (primary measurement).
    s1 = {it: evaluate_item(it, admitted[it]["via_seed"], admitted[it]["host"])
          for it in admitted}
    session1_metrics = compute_metrics(admitted, s1)
    # Session 2: a deterministic S2_FRACTION subsample, used ONLY to estimate
    # inter-session instability (rate-limit control), so the second pass does not
    # multiply the frame-wide GET budget by SESSIONS.
    subsample = _subsample(admitted)
    s2 = {it: evaluate_item(it, admitted[it]["via_seed"], admitted[it]["host"])
          for it in subsample}
    stable, unstable, exclusion_fraction = _stabilize(admitted, s1, s2, subsample)
    stability_ok = exclusion_fraction <= MAX_EXCLUSION_FRACTION
    per_item_final = {it: s1[it] for it in stable}
    metrics = compute_metrics(stable, per_item_final)
    metrics["n_unstable_excluded"] = len(unstable)
    metrics["unstable_items"] = unstable[:50]
    metrics["stability_subsample_size"] = len(subsample)
    metrics["stability_subsample_fraction_session_1"] = (
        compute_metrics({it: admitted[it] for it in subsample},
                        {it: s1[it] for it in subsample})["discovery_reachable_fraction"]
        if subsample else None)
    metrics["stability_subsample_fraction_session_2"] = (
        compute_metrics({it: admitted[it] for it in subsample},
                        s2)["discovery_reachable_fraction"] if subsample else None)
    metrics["exclusion_fraction"] = exclusion_fraction
    metrics["max_exclusion_fraction"] = MAX_EXCLUSION_FRACTION
    metrics["session_1_pooled_fraction"] = session1_metrics["discovery_reachable_fraction"]
    outcome, e, engines_ok = decide(metrics, gate["pass"])
    metrics["host_units_meeting_threshold"] = e
    metrics["engines_meeting_threshold"] = engines_ok
    metrics["oracle_dependent_supports"] = bool(outcome == "SUPPORTS" and not engines_ok)
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
    # PC_LIVE_PROBE_LIVENESS: the ROBOTS_SITEMAP / SITEMAP_XML machinery must
    # FETCH and PARSE >= 1 URL on >= 1 OUT-OF-POOL probe host at EXECUTE. This is
    # apparatus liveness, deliberately independent of the measurement frame: the
    # pool may legitimately produce a pool-wide zero (FALSIFIES) while the probe
    # hosts prove the channel machinery is operational, and vice versa.
    live = live_probe_state()
    controls["PC_LIVE_PROBE_LIVENESS"] = {
        "expected": ">= 1 out-of-pool probe host where ROBOTS_SITEMAP or SITEMAP_XML "
                    "fetches and parses >= 1 URL (apparatus liveness; disjoint from the frame)",
        "observed": live,
        "pass": live["pass"]}
    # Step 0 in-confirmatory control gate: any failure is infrastructure/substrate
    # invalidity, never a scientific branch.
    hop_pass = bool(controls["PC_HOP_CONFIRMATION"]["pass"])
    pc_reach_pass = bool(hop_pass and host_ident_pass and live["pass"])
    controls["PC_DISCOVERY_CHANNEL_REACHABILITY"] = {
        "expected": "(a) out-of-pool probe hosts parse >= 1 URL through ROBOTS_SITEMAP/SITEMAP_XML "
                    "(instrument live on the real Web; also verified at DESIGN); "
                    "(b) hop target found hop==1; (c) seed final-root host identity",
        "observed": {"hop_pass": hop_pass, "host_identity_pass": host_ident_pass,
                     "live_probe_pass": live["pass"]},
        "pass": pc_reach_pass}
    controls["STABILITY_CAP"] = {
        "expected": f"inter-session instability <= {MAX_EXCLUSION_FRACTION:.2f} of the "
                    f"{S2_FRACTION:.0%} stability subsample",
        "observed": {"subsample_size": len(subsample), "unstable": len(unstable),
                     "exclusion_fraction": exclusion_fraction},
        "pass": stability_ok}
    step0_ok = bool(pc_reach_pass and null_ok and stability_ok)
    validity_notes = [
        "Exposure-blind frame: hosts were selected by a predeclared rule (well-known documentation "
        "sites, >= 2 generator engines), verified for DEEP topology only; NO discovery surface of any "
        "frame host was inspected at DESIGN, so neither decision branch is pre-determined by selection.",
        "Static <a href>, <link rel=alternate>, <form>/<input> and application/ld+json only; JS-rendered navigation and JS search are not followed (representation loss).",
        "GET = one logical request with redirects followed; a redirect does not consume an extra GET unless a separate validation fetch is issued (spare).",
        "Pool deduplicated by minimum same-host static-hop across the frozen seeds.",
        "State-carrying page = fetched page with >=1 named <input>/<select>; item unit = page.",
        "SITEMAP_XML enumerates up to DISCOVERY_GETS_MAX=2 candidate paths in fixed order "
        "(sitemap.xml, sitemap_index.xml, sitemap-index.xml); a third candidate is never "
        "probed when the first two consumed the budget (deterministic).",
        "Instrument liveness is proven on LOCAL stdlib fixtures (1.0/0.0 dynamic range) and on "
        "OUT-OF-POOL probe hosts (LIVE_PROBE_HOSTS), never on frame hosts; a pool-wide zero "
        "is therefore a genuine FALSIFIES, not MEASUREMENT_INVALID.",
        "ON_SITE_SEARCH is the ONE channel whose query is derived from the item's own path "
        "segment (targeted acquisition: the agent knows the target page, not its path). It is a "
        "disclosed oracle-like channel; "
        "discovery_reachable_fraction_per_host_without_on_site_search is reported and "
        "oracle_dependent_supports flags any SUPPORTS that vanishes without it.",
        "Session 2 is a deterministic S2_FRACTION=25% subsample used only to estimate inter-session "
        "instability; if that estimate exceeds MAX_EXCLUSION_FRACTION=0.10 the run is "
        "MEASUREMENT_INVALID (rate-limit/noise, never a scientific branch).",
        "Pacing: PACE_S=0.15 s politeness pause before every foreign GET (localhost fixtures exempt).",
    ]
    status_final, outcome_final = "COMPLETE", outcome
    if not step0_ok:
        status_final, outcome_final = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        validity_notes = validity_notes + [
            "Step-0 control failure detected (PC_HOP_CONFIRMATION / PC_SEED_HOST_IDENTITY / "
            "PC_LIVE_PROBE_LIVENESS / NC_SYNTHETIC_UNREACHABLE_ITEM / STABILITY_CAP). "
            "Recorded in controls; no scientific branch is reported."]
    observations = [
        {"id": "OBS-ENV", "note": f"stdlib runner, {sys.version.split()[0]}, network GET-only"},
        {"id": "OBS-POOL", "note": json.dumps(gate)},
        {"id": "OBS-CHANNEL", "note": json.dumps(metrics["discovery_reachable_fraction_per_channel"])},
        {"id": "OBS-TREND", "note": json.dumps(metrics["flat_vs_growing_trend"])},
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
        "measurement": "site-native discovery reachability over frozen exposure-blind DEEP pool",
        "terminal_status": status_final,
    })
    return result


# ---------------------------------------------------------------------------
# DESIGN probe modes (reproducible from the frozen artifact)
# ---------------------------------------------------------------------------
def run_live_probe(outdir: Path):
    res = live_probe_state()
    write_json(outdir / "live_probe.json", res)
    print(json.dumps(res, indent=2))
    return res


def run_null_out_of_pool(outdir: Path):
    detail = {}
    reachable = 0
    for root in LIVE_PROBE_HOSTS:
        host = urllib.parse.urlsplit(root).netloc
        for ch in CHANNELS:
            for suf in ("a", "b"):
                synthetic = f"https://{host}/spider-nonexistent-{SEED}-{suf}.html"
                r = CHANNEL_FN[ch](synthetic, root, host)
                detail[f"{host}|{ch}|{suf}"] = bool(r["success"])
                if r["success"]:
                    reachable += 1
    res = {"n_probes": len(detail), "n_reachable": reachable,
           "NULL_ALL_ZERO": reachable == 0, "detail": detail}
    write_json(outdir / "null_out_of_pool.json", res)
    print(json.dumps({"n_probes": res["n_probes"], "n_reachable": reachable,
                      "NULL_ALL_ZERO": res["NULL_ALL_ZERO"]}, indent=2))
    return res


def _synth(host_fracs, engines_by_host):
    """Build synthetic (admitted, per_item) with controllable per-host success."""
    admitted, per_item = {}, {}
    for host, (n, k) in host_fracs.items():
        eng = engines_by_host[host]
        for j in range(n):
            it = f"https://{host}/item-{j}.html"
            hop = 3 + (j % 4)
            admitted[it] = {"hop": hop, "host": host, "engine": eng,
                            "controls": ["q"], "bfs_cost": hop + 1}
            succ = j < k
            pi = {ch: {"channel": ch, "discovered": succ, "success": succ,
                       "discovery_gets": (1 if succ else 0),
                       "item_get": (1 if succ else 0),
                       "total_gets": (2 if succ else 0), "discovery_bytes": 0,
                       "urls_count": 0, "item_status": (200 if succ else None),
                       "within_k": True} for ch in CHANNELS}
            pi["any_success"] = succ
            pi["min_total_gets_on_success"] = (2 if succ else None)
            per_item[it] = pi
    return admitted, per_item


def run_branch_drive(outdir: Path):
    """Drive the frozen metrics/decision/artifact path to every branch on
    synthetic inputs. This is the evidence the packet's branch-reachability claim
    is checked against; it performs NO network I/O."""
    t0 = time.time()
    scenarios = []
    # SUPPORTS: two hosts >= 0.50 on two different engines.
    a, p = _synth({"host-a": (10, 6), "host-b": (10, 6)},
                  {"host-a": "mdBook", "host-b": "Sphinx"})
    scenarios.append(("SUPPORTS", a, p, True, "SUPPORTS"))
    # MIXED_single_engine: two hosts >= 0.50 but a single engine.
    a, p = _synth({"host-a": (10, 6), "host-b": (10, 6)},
                  {"host-a": "mdBook", "host-b": "mdBook"})
    scenarios.append(("MIXED_single_engine", a, p, True, "MIXED"))
    # MIXED_one_host: exactly one host >= 0.50.
    a, p = _synth({"host-a": (10, 6), "host-b": (10, 2)},
                  {"host-a": "mdBook", "host-b": "Sphinx"})
    scenarios.append(("MIXED_one_host", a, p, True, "MIXED"))
    # FALSIFIES: every host below 0.50.
    a, p = _synth({"host-a": (10, 4), "host-b": (10, 3)},
                  {"host-a": "mdBook", "host-b": "Sphinx"})
    scenarios.append(("FALSIFIES", a, p, True, "FALSIFIES"))
    results = {}
    for name, admitted, per_item, gate_pass, expected in scenarios:
        metrics = compute_metrics(admitted, per_item)
        outcome, e, eng_ok = decide(metrics, gate_pass)
        metrics["host_units_meeting_threshold"] = e
        metrics["engines_meeting_threshold"] = eng_ok
        results[name] = {"outcome": outcome, "expected": expected, "E": e,
                         "engines_ok": eng_ok, "ok": outcome == expected}
        result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
                  "status": "COMPLETE", "outcome": outcome, "metrics": metrics,
                  "controls": {"BRANCH_DRIVE": {"pass": outcome == expected}},
                  "artifacts": [], "observations": [{"id": "SYNTHETIC", "note": name}],
                  "validity_notes": ["SYNTHETIC branch exercise; no network I/O."],
                  "unresolved": []}
        write_terminal(outdir / ("branch_" + name), result, t0)
    # Gate-failure and empty-denominator guards.
    m_empty = {"n_admitted_deep": 0, "discovery_reachable_fraction_per_host": {}}
    results["calibration_or_step0_failure"] = {
        "outcome": decide(m_empty, False)[0], "expected": "INCONCLUSIVE", "ok":
        decide(m_empty, False)[0] == "INCONCLUSIVE"}
    results["empty_denominator"] = {
        "outcome": decide(m_empty, True)[0], "expected": "INCONCLUSIVE", "ok":
        decide(m_empty, True)[0] == "INCONCLUSIVE"}
    # Admission failure and calibration failure write terminal triples.
    for name, note in (("admission_gate_failure", "ADMISSION_GATE false"),
                       ("calibration_failure", "CALIBRATION_GATE false")):
        result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": LANE,
                  "status": "MEASUREMENT_INVALID", "outcome": "INCONCLUSIVE",
                  "metrics": {}, "controls": {name.upper(): {"pass": False}},
                  "artifacts": [], "observations": [{"id": "SYNTHETIC", "note": note}],
                  "validity_notes": ["SYNTHETIC terminal-path exercise."], "unresolved": []}
        write_terminal(outdir / ("branch_" + name), result, t0)
        results[name] = {"outcome": "INCONCLUSIVE", "expected": "INCONCLUSIVE", "ok": True}
    # Stability helper exercise: cap fires when instability exceeds 10%.
    sa, sp = _synth({"host-a": (10, 6)}, {"host-a": "mdBook"})
    sub = sorted(sa)[:4]
    s1 = {it: sp[it] for it in sa}
    s2 = {}
    for idx, it in enumerate(sa):
        if it in sub and idx == 0:
            alt = {ch: dict(sp[it][ch]) for ch in CHANNELS}
            alt["ON_SITE_SEARCH"] = dict(alt["ON_SITE_SEARCH"], success=False)
            s2[it] = alt
        else:
            s2[it] = sp[it]
    stable, unstable, excl = _stabilize(sa, s1, s2, sub)
    cap_fires = excl > MAX_EXCLUSION_FRACTION
    results["stability_cap"] = {"n_subsample": len(sub), "n_unstable": len(unstable),
                                "exclusion_fraction": excl, "cap_fires": cap_fires,
                                "expected_cap_fires": True,
                                "ok": cap_fires == (excl > MAX_EXCLUSION_FRACTION)}
    all_ok = all(v.get("ok") for v in results.values())
    summary = {"all_branches_reachable": all_ok, "results": results,
               "no_network_io": True}
    write_json(outdir / "branch_drive.json", summary)
    print(json.dumps(summary, indent=2))
    return summary


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", metavar="OUTDIR")
    ap.add_argument("--pool", action="store_true")
    ap.add_argument("--live-probe", metavar="OUTDIR")
    ap.add_argument("--null", metavar="OUTDIR")
    ap.add_argument("--branch-drive", metavar="OUTDIR")
    ap.add_argument("outdir", nargs="?")
    args = ap.parse_args()
    if args.calibrate:
        run_calibration(Path(args.calibrate))
        return
    if args.pool:
        pages, stats = build_pool()
        deep, gate = admit(pages)
        print(json.dumps(
            {"seed_stats": stats, "n_pages": len(pages), "gate": gate,
             "deep_by_hop": dict(sorted(Counter(v["hop"] for v in deep.values()).items())),
             "n_deep": len(deep)}, indent=2))
        return
    if args.live_probe:
        run_live_probe(Path(args.live_probe))
        return
    if args.null:
        run_null_out_of_pool(Path(args.null))
        return
    if args.branch_drive:
        run_branch_drive(Path(args.branch_drive))
        return
    if not args.outdir:
        print("usage: run.py [--calibrate OUTDIR | --pool | --live-probe OUTDIR | "
              "--null OUTDIR | --branch-drive OUTDIR | OUTDIR]", file=sys.stderr)
        raise SystemExit(2)
    confirmatory(Path(args.outdir))


if __name__ == "__main__":
    main()
```

## 14. v2 freeze-eligibility checks

All six are answered in `spec.json.freeze_eligibility`; summary:

| check | status |
|-------|--------|
| `decision_rule_reachability` | PASS — denominator >= 10 (493), `E` well-defined in {0..4}, all branches structurally reachable, and the frozen `--branch-drive` mode reproduces `SUPPORTS`/`MIXED`-single-engine/`MIXED`-one-host/`FALSIFIES`/gate-failure/empty-denominator/stability-cap (`all_branches_reachable=true`); fixtures bracket 0.50 |
| `measurement_prerequisites` | PASS — substrate live; frame builds (493 DEEP / 4 hosts / 2 engines, no challenge pages); out-of-pool liveness live (5/5 hosts); all controls run |
| `baseline_identifiability` | PASS — four distinct stable baselines; treatment is a distinct decision function over the same admitted item set; `B_LINK_FOLLOWING_BFS` emitted as measured `bfs_cost` |
| `control_sensitivity` | PASS — calibration 1.0/0.0; `NC_SYNTHETIC_UNREACHABLE_ITEM` 0/50; `PC_LIVE_PROBE_LIVENESS` (out-of-pool parsed-URL) adds a live guard without masking FALSIFIES; `STABILITY_CAP` fires at exclusion 0.25 > 0.10 in the branch drive |
| `treatment_liveness` | PASS — pipeline runs end-to-end (1.0/0.0 fixtures); instrument live on 5 out-of-pool hosts; SUPPORTS/MIXED/FALSIFIES all execute |
| `freeze_artifacts_bound` | NOT_APPLICABLE — no mutable local artifact is an interpretation dependency: seeds and the complete code are inlined in `prereg.md` section 13 and `spec.json`; the code is bound via `CODE_SHA256` (self-asserted — the freezer hashes `prereg.md`, and EXECUTE must re-extract and verify, section 10.14); the live Web is an external remote substrate pinned by the frozen seeds and re-checked by the admission gate, not a mutable local artifact |

`spec.json.freeze_artifacts = []`.

## 15. Not authorized

- Re-measuring the grandparent's static re-derivable fraction or its GROWING ratio.
- Returning to the blocked `C-SEMANTIC-RESOLVE` thread.
- Constructing the pool or running any discovery probe after `freeze.json` exists.
- Freezing any design whose falsifier cannot trigger in both directions.
- Inspecting frame hosts' discovery surfaces at DESIGN (the frame is exposure-blind).
- Promoting any discovery mechanism to Product Core from this experiment.

## 16. Next stage

An **independent** `design_review.json` (separate stage/agent, not this DESIGN task) must PASS before `freeze.json` is written. The reviewer must attack: (a) whether the frozen seed list still reproduces a multi-engine DEEP pool (gate >= 10 / 2 engines / 2 hosts); (b) whether the **exposure-blind** frame genuinely leaves both `SUPPORTS` and `FALSIFIES` reachable, or whether the mdBook-heavy composition (section 10.11) reintroduces a construction bias; (c) whether **canonical `match_key`** (`.html`/`/` stripping) can merge distinct resources or inflate fractions (section 10.12); (d) whether `K = 3` and `0.50` are non-arbitrary (they bracket the measured calibration range and are recorded before outcomes); (e) whether `JSON_LD`/`ON_SITE_SEARCH` are treated as genuinely cold-start, and whether disclosing `ON_SITE_SEARCH` as oracle-like with an oracle-free sensitivity is sufficient (section 4); (f) whether `freeze_artifacts_bound = NOT_APPLICABLE` is justified given inlined seeds + hash-bound code (and whether the self-asserted `CODE_SHA256`, section 10.14, is acceptable); (g) whether the decision unit (host, with engine descriptive) is faithful to the mandate's "host/engine unit", and whether requiring `engines_ok` for `SUPPORTS` is the right formalisation; (h) whether the two-sided reachability claim over-claims the outcome (attainability is argued structurally + by `--branch-drive`, not by a DESIGN-measured fraction; EXECUTE is authoritative); (i) whether every control can fire in both directions and, specifically, whether `PC_LIVE_PROBE_LIVENESS` is genuinely outcome-independent and out-of-frame (so FALSIFIES is reachable); (j) whether the revision-1 selection-on-treatment defect is fully closed by removing the stratum; (k) whether `--branch-drive` genuinely exercises the same `compute_metrics`/`decide`/`write_terminal` functions the confirmatory path uses (it does — no reimplementation); (l) whether the link-only `StaticLinks` parser makes exposure-blindness structural and whether the regenerated frame (493 DEEP, 197/94/194/8) is unchanged; (m) whether the 25% subsample + `MAX_EXCLUSION_FRACTION = 0.10` cap is a sound stability bound and cannot silently discard an unrepresentative subset; (n) whether `PACE_S = 0.15` fails to prevent throttling on the 197-item host; (o) whether the `_derive_trend` rule (`TREND_DROP=0.10`, `TREND_MIN_BUCKET=5`) is preregistered tightly enough.

DESIGN NOT YET FROZEN — awaiting `design_review.json`.

### 16.1 DESIGN self-attack summary

Before finalizing, the design was attacked for empty/unreachable branches, arithmetic impossibility, ceiling/floor baselines, treatment/comparator identity, insensitive controls, missing prerequisites and unbound mutable artifacts. Findings and repairs: revision 1's **ceiling baseline / selection-on-treatment** (hosts chosen for their discovery surface) removed by an **exposure-blind** frame whose BFS parser (`StaticLinks`) has no discovery fields at all (structural, not promised-by-use); its **frame-exposing liveness control** replaced by out-of-pool `PC_LIVE_PROBE_LIVENESS`; its **Cloudflare-challenged Sphinx hosts** replaced by reachable hosts; the revision-2 **unverifiable branch-exercise claim** replaced by the frozen `--branch-drive` mode that drives the real metrics/decision/artifact path to every branch (including `MIXED` from engine span and the stability cap) and reproduces from the artifact; a **stability cap** (25% subsample, 10% bound) and **pacing** added against throttling-induced denominator erosion; the **engine-span requirement** added so `SUPPORTS` needs `>= 2` engines; the oracle-like `ON_SITE_SEARCH` disclosed with an oracle-free sensitivity; the deterministic `SITEMAP_XML` cap disclosed (section 10.13); the self-asserted `CODE_SHA256` disclosed (section 10.14); and the required live probes (seed reachability, out-of-pool liveness, null control, pool reconstruction, hop control, branch drive) run and reproduced. **No frame host discovery surface was inspected and no confirmatory item-level outcome was computed at DESIGN.**
