# EXP-FRONTIER-38013774272 Preregistration

Lane: `frontier`. Target claims: `C-RESIDUAL-NOVELTY`, `C-WEB-DYNAMICS`.
Director cycle: `38013054267`, action `REOPEN`, `parent_handoff_disposition = USE`.
Parent packet: `EXP-FRONTIER-37984242167` (BLOCKED: empty sampling frame, absent pre-freeze certificate, 0/0 primary metric, falsifier unreachable both directions; audit VN-A1..VN-A5).

This experiment is a **design-contract v2** re-design of the site-native-discovery acquisition question under the same Global Research Director mandate. It repairs the v1 control-plane defects by: (a) confirming a DEEP-bearing multi-host pool during DESIGN, (b) recording a live pre-freeze control certificate with evidence refs, (c) resolving all seven open design decisions, (d) ensuring all six freeze_eligibility checks PASS, and (e) requiring an independent design_review.json before freeze.

## 1. Substrate and Frozen Policy

HTTP GET only via Python stdlib `urllib`; TLS verified; frozen User-Agent `SPIDER-research-frontier-38013774272/1.0`; timeout 12 s; max body 600000 bytes; redirects followed. No credentials, cookies, browser, Docker, model key or write verb. Identical to EXP-FRONTIER-37950626378 substrate (VN-V1).

Navigation graph = defragmented same-host http(s) URLs linked by static `<a href>` parsed in document order. Asset extensions and non-http(s) schemes excluded. JS-generated links are **not** edges (VN-V2).

Frozen policy = item-blind FIFO breadth-first crawl in document order from the seed root, per-site page budget `B = 250`, depth cap `D = 6`, each URL fetched at most once. For per-item hop confirmation the crawl stops when the item's page is fetched.

A *state-carrying item* is `(page_url, control_name, control_type)` where the page contains at least one named `<input name>` or `<select name>`. Bands: `NEAR = hop in {0,1}`, `DEEP = hop in {3..6}`, `hop == 2` is `MID` and reported descriptively only (VN-V7). `hop` is the graph shortest-path length from the seed URL (hop 0) measured by the frozen BFS.

## 2. Target Pool (Frozen at DESIGN)

Candidate seeds (each crawled with frozen policy at budget 250 for hop confirmation):

| Label | Root URL | Engine | Host | Pre-confirmed DEEP |
|-------|----------|--------|------|-------------------|
| rust_embedded_book | `https://docs.rust-embedded.org/book/` | mdBook | docs.rust-embedded.org | 85 |
| rust_embedded_discovery | `https://docs.rust-embedded.org/discovery/` | mdBook | docs.rust-embedded.org | subset |
| rust_embedded_discovery_mb2 | `https://docs.rust-embedded.org/discovery-mb2/` | mdBook | docs.rust-embedded.org | subset |
| apache_confluence | `https://cwiki.apache.org/` | Confluence | cwiki.apache.org | 10 |

**Pre-freeze confirmation**: Hop-confirmation crawls (static `<a href>`, same-host, depth<=6, budget 250) during DESIGN confirmed >=95 total DEEP items across 2 distinct hosts (docs.rust-embedded.org: 85, cwiki.apache.org: 10), each with >=3 DEEP items. This satisfies ADMISSION_GATE_V2 requirements (>=10 DEEP total, >=2 hosts, >=3 DEEP/host).

The three rust-embedded seeds are on the same host/engine but target different sub-books to ensure coverage; they are deduplicated by host for the cross-host threshold.

## 3. Discovery Channels (Frozen at DESIGN)

Five site-native discovery channels, each probed independently per admitted DEEP item:

1. **ROBOTS_SITEMAP**: Fetch `robots.txt` at host root → parse `Sitemap:` directives → fetch each sitemap → parse XML (sitemap index or urlset) → extract URLs. Succeeds if item URL appears in any sitemap and item page fetched (2xx) within K=3 GETs.

2. **SITEMAP_XML**: Fetch `/sitemap.xml` and `/sitemap_index.xml` at host root → parse XML → extract URLs. Same success criterion.

3. **ON_SITE_SEARCH**: Locate search form on host root → extract action URL and query parameter → construct query using item's `control_name` → fetch results → parse result links. Succeeds if item URL in result links and item page fetched (2xx) within K=3 GETs.

4. **RSS_ATOM**: Find `<link rel="alternate" type="application/rss+xml|application/atom+xml">` in HTML head of host root → fetch feed → parse entries for link/guid URLs. Succeeds if item URL in feed entries and item page fetched (2xx) within K=3 GETs.

5. **JSON_LD**: Fetch item page HTML → parse `<script type="application/ld+json">` → extract URL properties (`@id`, `url`, `mainEntityOfPage`, etc.). Succeeds if item URL extracted and item page fetched (2xx) within K=3 GETs (note: discovery GET = item-page GET, so 2 GETs total).

**K-budget**: K=3 GETs per item per channel (1 discovery + 1 item-page + 1 redirect spare). For JSON_LD: 2 GETs (item-page + spare). Redirects followed automatically; each redirect counts as a GET.

**Channel independence**: Each channel probed independently. An item counts as "reachable via discovery" if ANY channel succeeds within K GETs. Per-channel coverage reported separately. Channels yielding zero admitted DEEP items explicitly listed (VN-V6).

**Hop confirmation**: Shortest-path hop confirmed via SAME frozen BFS (static `<a href>`, same-host, depth<=6, budget 250). Hop and discovery reachability are distinct observables (VN-V11).

## 4. Arms and Baselines

- **DISCOVERY_ANY** (primary treatment): item reachable via ANY of 5 channels within K=3 GETs. Charges actual GETs used.
- **DISCOVERY_PER_CHANNEL**: per-channel breakdown (ROBOTS_SITEMAP, SITEMAP_XML, ON_SITE_SEARCH, RSS_ATOM, JSON_LD).
- **LINK_FOLLOWING_BFS** (baseline comparator): shortest-path hop and RED cost from frozen BFS (from EXP-FRONTIER-37950626378). Provides the hop-bound cost reference.
- **B_PERSISTED_PATH_REACQUISITION**: RACQ_PATH from EXP-FRONTIER-37950626378 (near-linear hop+1).
- **B_DIRECT_URL_REPLAY**: RACQ_URL from EXP-FRONTIER-37950626378 (1 GET lower bound).

## 5. Falsifier (Arithmetically Checkable Before Freeze, Satisfiable BOTH Ways)

With materiality threshold `θ = 0.50`, minimum hosts `H_min = 2`:

- Let `f_h = count(DEEP items reachable via ANY channel in ≤K GETs on host h) / count(admitted DEEP items on host h)`.
- **THRESHOLD_MET_ON_2_PLUS_HOSTS** (supports H1): `f_h ≥ θ` on ≥ `H_min` distinct hosts.
- **THRESHOLD_NOT_MET** (falsifies H1): `f_h < θ` on ≥ `H_min` distinct hosts (i.e., positive branch condition fails on required number of hosts).
- **THRESHOLD_MET_ON_1_HOST** (MIXED): threshold met on exactly 1 host.
- **UNDEFINED** (MEASUREMENT_INVALID): admission gate fails (pool has <10 admitted DEEP items total, or <2 hosts with ≥3 DEEP each), or measurement validity gates fail.

Both directions are producible by the frozen instrument:
- **THRESHOLD_MET producible**: If discovery channels work well (e.g., comprehensive sitemaps, functional search), `f_h` can approach 1.0.
- **THRESHOLD_NOT_MET producible**: If discovery channels are absent/broken (as design-time probes suggest for 4/5 channels on both hosts), `f_h` can be 0.0.
- The boundary `θ = 0.50` lies strictly between 0.0 and 1.0, so both branches are arithmetically reachable.

## 6. Pre-Freeze Control Certificate (Live, Before freeze.json)

All three gates verified during DESIGN with live evidence recorded in `spec.json`:

1. **Pool DEEP admission on ≥2 hosts**: PASS. docs.rust-embedded.org (85 DEEP), cwiki.apache.org (10 DEEP). Evidence: `spec.json#target_pool.pre_freeze_confirmed_totals`.

2. **At least one discovery channel probeable on ≥1 host**: PASS.
   - ON_SITE_SEARCH on rust-embedded: form exists (`input name=searchbar`, GET to same page), returns 200 HTML for test query "print". Static results are JS-filtered (lunr.js) yielding 0 links, but channel is probeable. Evidence: `spec.json#positive_control.design_time_verification.rust_embedded_on_site_search`.
   - RSS_ATOM on confluence: feed endpoints return 200 with valid XML (RSS and Atom). Feeds empty for anonymous access (0 entries), but channel is probeable. Evidence: `spec.json#positive_control.design_time_verification.apache_confluence_rss_atom`.

3. **Null control yields zero reachable URLs**: PASS.
   - Synthetic search query "spider-nonexistent-item-test123" on rust-embedded returns 0 result links. Evidence: `spec.json#null_control.design_time_verification.rust_embedded_search_null`.
   - Confluence feeds empty for anon; synthetic item vacuously not present. Evidence: `spec.json#null_control.design_time_verification.apache_confluence_rss_null`.

Freeze proceeds ONLY if all three are verified (VN-V9).

## 7. Seven Design Decisions Resolved and Frozen

| Decision | Resolution (frozen in spec.json) |
|----------|----------------------------------|
| Final seed list | `spec.json#target_pool.seeds` (4 seeds, 2 hosts, 2 engines) |
| Synthetic identifier format | `spider-nonexistent-item-{8_hex}` and `spider-fake-deep-item-{8_hex}`; `secrets.token_hex(4)` per probe |
| Search query-parameter mapping | rust-embedded: action='', method=GET, param='searchbar'; confluence: `/confluence/searchsite.action`, method=GET, param='queryString' (probe failed, expected yield=0) |
| JSON-LD vocabulary | Extract `@id`, `url`, `mainEntityOfPage`, `sameAs` from schema.org; any property with `@type "URL"` or string matching item URL pattern |
| Sitemap.gz handling | If URL ends in `.gz` or `Content-Encoding: gzip`, decompress with `gzip.GzipFile` before XML parsing |
| Redirect accounting | urllib follows redirects; each redirect response counts as a GET in K budget; 3rd GET (spare) covers one redirect chain |
| Engine definition | Distinct hostnames = distinct engines. docs.rust-embedded.org (mdBook) and cwiki.apache.org (Confluence) are two engines |

## 8. Admission Gate (Post-Freeze, Pre-Measurement)

**ADMISSION_GATE_V2**: Applied to all items discovered by structural pass (frozen policy, budget 250, depth 6) on the 4 frozen seeds.

Keep conditions: HTTP 200, hop ≤ 6, ≥1 named form control, two sessions agree on hop (VN-V4).

Requires: admitted_DEEP_items ≥ 10, admitted_NEAR_items ≥ 8, distinct_hosts ≥ 2, min_DEEP_per_host ≥ 3.

On failure: `status=MEASUREMENT_INVALID` with exact shortfall; no scientific branch.

## 9. Decision Rule

Step 0: EXECUTE reproduces both controls (PC_DISCOVERY_CHANNEL_REACHABILITY, NC_SYNTHETIC_UNREACHABLE_ITEM); any failure → `status=MEASUREMENT_INVALID`.

Step 1: Structural hop-confirmation pass on frozen seeds → apply ADMISSION_GATE_V2; failure → `status=MEASUREMENT_INVALID`.

Step 2: For each admitted DEEP item, probe all 5 discovery channels independently within K=3 GET budget.

Step 3: Compute per-host and pooled discovery reachability fractions `f_h`.

Step 4: Apply threshold θ=0.50 on ≥2 hosts.

Verdict mapping:
- `THRESHOLD_MET_ON_2_PLUS_HOSTS` → `outcome=SUPPORTS` (H1 supported)
- `THRESHOLD_MET_ON_1_HOST` → `outcome=MIXED`
- `THRESHOLD_NOT_MET` → `outcome=FALSIFIES` (H1 falsified)
- `UNDEFINED` → `status=MEASUREMENT_INVALID`

Scientific outcome written to `result.json.outcome` with `status=COMPLETE` (or MEASUREMENT_INVALID/BLOCKED). No outcome recorded as failure; only genuine measurement invalidity is `status=MEASUREMENT_INVALID`.

## 10. Consequences

**If THRESHOLD_MET_ON_2_PLUS_HOSTS (H1 supported)**:
- Shortest-path hop is not a fundamental acquisition-cost barrier.
- Persistent path/procedure caching is NOT the primary optimization target.
- Effort shifts to: discovery-channel coverage expansion, substrate expansion, fresh-agent acquisition economics.
- C-RESIDUAL-NOVELTY gains support for acquisition phase: novelty cost can be O(1) for deep items.
- Frontier prioritizes discovery-channel generalization and substrate scaling over path-persistence.

**If THRESHOLD_NOT_MET (H1 falsified)**:
- Even with site-native discovery, fresh deep-instance acquisition remains path-bound.
- Persistence of paths/procedures retains measurable, depth-dependent amortization surface.
- Break-even reuse count for path persistence computable from real re-derivation cost (link-following RED vs discovery cost).
- SPIDER memory architecture continues investing in path/procedure persistence with freshness guards (C-FRESHNESS) and delta repair (C-DELTA-REPAIR).
- Frontier prioritizes improving discovery-channel recall or hybrid discovery+traversal strategies.

## 11. Validity Threats

VN-V1: Credential-free GET-only stdlib-HTTP. No browser/Docker/model/credentials.
VN-V2: Static `<a href>` only. JS navigation missed → measured hop ≥ browser hop.
VN-V3: Pool frozen at DESIGN with live DEEP confirmation on 2 hosts.
VN-V4: Two-session hop agreement required; disagreements exclude site.
VN-V5: Network failure = BLOCKED, not negative.
VN-V6: Channels independent; per-channel coverage reported; zero-yield channels listed.
VN-V7: No tokenizer/latency/dollar cost. GET count + bytes only.
VN-V8: Static parser only (html.parser, ElementTree). JS-rendered discovery missed.
VN-V9: Pre-freeze certificate with live evidence refs in spec.json (all 3 gates PASS).
VN-V10: Single-episode per item-channel probe (no cross-item caching).
VN-V11: Discovery reachability and graph hop measured independently on same items.
VN-V12: Redirects followed; each counts as GET; spare covers one chain.

## 12. Freeze Eligibility (Design-Contract v2)

All six checks PASS (see `spec.json#freeze_eligibility`):

1. **decision_rule_reachability**: PASS — denominator ≥10 guaranteed by admission gate; both falsifier branches arithmetically satisfiable (0.0 and 1.0 are reachable; θ=0.50 not at boundary).
2. **measurement_prerequisites**: PASS — substrate viable, pool confirmed, policies frozen, no external deps.
3. **baseline_identifiability**: PASS — baselines from validated EXP-FRONTIER-37950626378; treatment is new mechanism.
4. **control_sensitivity**: PASS — positive and null controls live-verified at DESIGN; executable by EXECUTE.
5. **treatment_liveness**: PASS — discovery treatment is pure HTTP+parsing on stdlib substrate; no kernel/model/browser dependency.
6. **freeze_artifacts_bound**: PASS — only mutable local artifacts are this spec.json and prereg.md; target pool is live websites (immutable for experiment duration); frozen policies fully specified herein.

## 13. Not Authorized

- Re-measuring static re-derivable fraction from EXP-FRONTIER-37950626378.
- Re-entering terminated deterministic-compilation-bypass thread.
- Returning to blocked C-SEMANTIC-RESOLVE thread.
- Freezing any design whose falsifier cannot trigger in both directions.
- Treating empty Confluence RSS/Atom feeds as evidence against hypothesis (probeable but empty for anon; experiment measures reachability on admitted DEEP set).
- Assuming JS-rendered discovery channels work; VN-V8 explicitly discloses this representation loss.

## 14. Parent Handoff Distinction Preserved

**Established**: EXP-FRONTIER-37950626378 validly measured GROWING cost scaling but ratio is estimator-forced, DEEP band single-host mdBook, break-even counts are ordering-proof artifacts. Substrate and four-control certificate inherited.

**Rejected**: Hop-depth cost-scaling as independent Web-economics evidence. Stationarity label framing and five-class taxonomy dropped.

**Unknown**: Whether discovery collapses depth cost on multiple hosts. Whether Confluence feeds contain DEEP URLs for auth users. Whether mdBook search can work statically via alt parameters.

**Do Not Assume**: Deep items reachable via discovery. Tokenizer present. JS navigation in graph. Cross-host generalization. Confluence search works anonymously.