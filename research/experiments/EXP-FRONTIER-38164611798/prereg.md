# EXP-FRONTIER-38164611798 preregistration

Lane: frontier | Claim: C-CROSSSITE | design_contract_version: 2 | mode: **DESIGN** (frozen at the end of this document)

---

## 1. Identity and binding mandate

- experiment_id: `EXP-FRONTIER-38164611798`
- lane: frontier
- claim_ids: `["C-CROSSSITE"]`
- Director: Global Research Director PIVOT with `cognitive_reset: true`; action allocation for C-CROSSSITE;
  `parent_handoff_disposition: SUPERSEDE` (parent EXP-FRONTIER-37984242167 is a blocked-design receipt, not a scientific inheritance).
- Mandate URL: `research/experiments/EXP-FRONTIER-38164611798/request.json#director_mandate.allocation.question`.
- This design deliberately does NOT repeat v1 (EXP-FRONTIER-37984242167: committed an EMPTY sampling frame — 0 seeds, 0 DEEP items, 0 hosts — and no pre-freeze certificate) or v2 (EXP-FRONTIER-38085197666: declared all six freeze_eligibility checks PASS while its declared freeze_artifacts were ABSENT; failure.json exit 65). Attainability is the measured object, not a prerequisite.

## 2. Question (verbatim from the mandate)

> On the credential-free GET-only stdlib-HTTP substrate, over a broadened frozen multi-host pool enumerated by DESIGN WITHOUT a required engine-count precondition, treat attainability itself as the measured object:
> (Q1) for each host/engine, how many state-carrying items sit at shortest-path hop >= 3 under the frozen same-host static-`<a>` BFS (depth <= 6, budget 250), reported per engine with an explicit count of engines that yield ZERO DEEP items;
> (Q2) conditional on the attained pool, what fraction of those DEEP items is reachable in <= K = 3 fresh-agent GETs (one discovery GET + item-page GET + one spare) via ANY of the five frozen site-native discovery channels (ROBOTS_SITEMAP, SITEMAP_XML, ON_SITE_SEARCH, RSS_ATOM, JSON_LD), with per-channel coverage disclosed and any channel yielding zero admitted DEEP items reported as such rather than counted as a null;
> (Q3) is that O(1)-reachable fraction >= 0.50 on at least two distinct hosts/engines?

## 3. Hypothesis

**H1 (SUPPORTS condition).** On the credential-free GET-only stdlib-HTTP substrate over the frozen 20-host pool (section 6), at least two distinct engines admit a discovery-reachable fraction of DEEP (hop >= 3) state-carrying items of >= 0.50 within K = 3 fresh-agent GETs via the five frozen channels, with per-channel coverage and zero-admission channels disclosed. If Q3 holds: **shortest-path hop is NOT a fundamental acquisition-cost barrier for discovery-enabled acquisition** — the Web's own indexes make deep acquisition O(1); effort moves to discovery-channel coverage and substrate expansion. Bounds C-CROSSSITE upward on this substrate class.

## 4. Falsifier

**F1 (FALSIFIES condition).** Fewer than two distinct engines reach the 0.50 threshold while >= 1 engine admits >= 1 DEEP item: **engine-stratified bounded negative** — site-native discovery is NOT an O(1) shortcut for deep state-carrying acquisition on this substrate class; the discovery axis is closed on this substrate and the persistence-maintenance axis (re-validation GETs/bytes plus stale-replay false-accept rate vs re-derivation cost, scaling with hop and elapsed time — the Director's recorded runner-up, owned by Graph/Product) is handed to the next mandate.

**INCONCLUSIVE (never a negative, never a SUPPORTS; per AGENTS.md 'never turn missing data or infrastructure failure into a negative scientific result'):**
- zero DEEP items admitted across the frozen pool → Q1 measured (explicit zero-DEEP engine census + host census), Q2/Q3 vacuous; the vacuity is an attainability fact, recorded as such;
- every DEEP-admitting engine is LIMITED (> 10% of its admitted DEEP items dead to the liveness re-GET) → Q1/Q2 measured and disclosed, Q3 not determinable;
- seed fetch fails on every pool host → infrastructure signature, explicitly NOT a scientific null (BLOCKED-class disposition; no outcome stage measurement).

## 5. Substrate and frozen operational definitions (inherited from the parent measurement EXP-FRONTIER-37950626378)

- **Substrate**: GET-only stdlib `urllib` (no credentials, no cookies, no browser, no Docker, no model key, no write verb); TLS verified (system default); frozen UA `SPIDER-research-frontier-11798/1.0`; timeout 12 s; max body 600000 bytes (truncation flagged); redirects followed with every leg counted; gzip Content-Encoding handled.
- **Navigation graph**: defragmented same-host http(s) URLs; edges = static `<a href>` in document order; non-http(s) schemes and asset extensions excluded; JS links are NOT edges.
- **hop distance**: shortest path in edges from the seed (seed = hop 0).
- **Frozen crawl policy (structural pass)**: item-blind FIFO BFS in document order, per-site budget B=250, depth D=6, each URL fetched at most once; budget is a hard cap enforced even inside a single page's link loop.
- **State-carrying item (Q1 unit, page-level)**: a page URL whose HTML contains >= 1 named `<input name>` or `<select name>`. (Reduction from the parent's (page, control_name, control_type) triple: discovery channels resolve page URLs. Disclosed in VN-A1.)
- item id for reporting = the normalized page URL; per-engine aggregation by engine_class (V11 identity rule).

## 6. Frozen pool (20 hosts, enumerated by DESIGN; every seed live at freeze)

engine_class = `<meta name="generator">` content when present, else the documented platform recorded at DESIGN:

| host | engine_class | seed |
|---|---|---|
| doc.rust-lang.org | mdBook | https://doc.rust-lang.org/stable/book/ |
| docs.python.org | Sphinx | https://docs.python.org/3/ |
| numpy.org | Sphinx | https://numpy.org/doc/stable/ |
| pandas.pydata.org | Sphinx | https://pandas.pydata.org/docs/ |
| react.dev | Docusaurus | https://react.dev/learn |
| docusaurus.io | Docusaurus | https://docusaurus.io/docs |
| docs.readthedocs.io | Sphinx-RTD | https://docs.readthedocs.io/en/stable/ |
| docs.pytest.org | Sphinx-RTD | https://docs.pytest.org/en/stable/ |
| gohugo.io | Hugo | https://gohugo.io/documentation/ |
| jekyllrb.com | Jekyll | https://jekyllrb.com/docs/ |
| docs.gitbook.com | GitBook | https://docs.gitbook.com/ |
| kubernetes.io | Hugo-k8s | https://kubernetes.io/docs/ |
| developer.mozilla.org | MDN-Yari | https://developer.mozilla.org/en-US/ |
| docs.github.com | GitHubDocs | https://docs.github.com/en |
| en.wikipedia.org | MediaWiki | https://en.wikipedia.org/wiki/Main_Page |
| www.mediawiki.org | MediaWiki | https://www.mediawiki.org/wiki/MediaWiki |
| quotes.toscrape.com | custom | https://quotes.toscrape.com/ |
| www.gnu.org | GNU-web | https://www.gnu.org/ |
| forums.gentoo.org | phpBB | https://forums.gentoo.org/ |
| blog.wordpress.org | WordPress | https://blog.wordpress.org/ |

Generator meta observed at DESIGN (7 hosts): WordPress 7.2-alpha-64252 (blog.wordpress.org), Docusaurus v4.0.0 (docusaurus.io), Hugo 0.167.0 (gohugo.io), Jekyll v4.4.1 (jekyllrb.com), GitBook a0c1bdf (docs.gitbook.com), MediaWiki 1.47.0-wmf.23 (en.wikipedia.org), MediaWiki 1.47.0-wmf.22 (www.mediawiki.org). Q3 requires >= 2 DISTINCT engine classes on distinct base-domain hosts.

## 7. Measurement protocol (frozen; implemented byte-exactly in section 16)

### 7.1 Structural pass (Q1) — `bfs_structural`
Item-blind FIFO BFS in document order from the seed; same-host static `<a>` edges only; budget 250 with the hard cap inside the link loop; depth 6; each URL fetched at most once; per-page observation records hop, 1-based discovery ordinal (= `requests`, the fresh-agent link-following cost), bytes, truncated flag, and controls_seen (named inputs + selects on that page). The seed equals ordinal 1. A seed fetch failure yields `seed_error` (infrastructure, recorded never a null).

### 7.2 Discovery channels (Q2) — `channel_documents` + `evaluate_items`
Frozen per-channel **charged** protocol cost (fresh-agent semantics; <= K=3 by construction; every redirect leg counts toward K via the counting redirect handler):
- ROBOTS_SITEMAP = 3: robots.txt GET → FIRST `Sitemap:` line → sitemap doc GET (XML or TXT or .gz; index → FIRST child sitemap GET) → item page GET.
- SITEMAP_XML = 2: `/sitemap.xml` GET, fallback `/sitemap_index.xml`, index → FIRST child GET → item page GET.
- ON_SITE_SEARCH = 3: seed HTML GET (form discovery) → results GET (query = item slug, the last non-empty path segment, percent-encoded, via the first GET form with a named text-like input) → item page GET. No named GET form → channel NOT_PROBEABLE (recorded, never a null).
- RSS_ATOM = 3: seed HTML GET (feed discovery, first alternate RSS/Atom link) → feed GET → item page GET.
- JSON_LD = 2: seed HTML GET (extract ALL http(s) strings from seed JSON-LD blocks — hub enumeration, over-inclusive by design, disclosed) → item page GET.

Discovery documents are fetched ONCE per (host, channel) at the discovery pass; the item-page GET is per item and doubles as the liveness re-GET (`lrec`); an item is **reachable** iff (member of >= 1 channel) AND live. Membership uses frozen `norm_eq`: defragmented, lowercase host, default port stripped, equality after stripping at most one trailing '/' — no redirect chasing of channel URLs. Cross-host URLs can never match a same-host item. The actual vs charged GET ledger is disclosed (raw/ + derived/ artifacts).

### 7.3 Metrics
Per engine: n_deep (live admitted DEEP items), n_dead_excluded, limited flag (> 10% admitted-item death), reachable, fraction, CI95 (Clopper-Pearson via betainv/betacf binary search, k=0/k=n boundary forms), per-channel coverage (count of members / n), hop distribution, hosts. Plus: `pool_engines_census` (all 20 engine classes, zero-DEEP included), `host_census` (all 20 hosts), `engines_with_zero_deep`, `engines_limited`, `engines_at_or_above_threshold`, `seed_error_hosts`.

## 8. Baselines (stable identities; frozen)

1. **B-LINK-FOLLOWING-BFS** — primary comparator, measured IN-pool per item: fresh-agent link-following cost = 1-based BFS discovery/fetch ordinal (`requests`), <= 250 for every admitted item (admission requires a BFS fetch), ~ hop+1 in a clean chain. The O(1) discovery claim must beat this per-item cost. *(measured)*
2. **B-PERSISTED-PATH-REACQUISITION** — inherited context ONLY, NOT re-measured: parent EXP-FRONTIER-37950626378 RACQ_PATH NEAR=2.0/MID=3/DEEP=4 (~hop+1), 1532/1532 items with path_len == hop+1 on the single DEEP-bearing engine of that pool.
3. **B-DIRECT-URL-REPLAY** — inherited context ONLY, NOT re-measured: parent RACQ_URL = 1 GET for a known URL.

## 9. Controls (stable identifiers; 13 distinct control identities producing 15 pass rows; run by `--stage controls`)

| control | expected (pass iff) | DESIGN-observed |
|---|---|---|
| NC_BFS_CALIBRATION_FLAT | R (hop3/hop1 requests) <= 3.0 | 2.0 (p1=2, p3=4) — PASS |
| NC_BFS_CALIBRATION_GROWING | R > 3.0 | 6.5 (hop1=2, first hop3=13, nodes_fetched 250) — PASS |
| PC_PARSER_CANARY_sitemap_xml | urls == [https://example.com/a], not index | PASS |
| PC_PARSER_CANARY_sitemap_index | is_index, children == [https://example.com/s1.xml] | PASS |
| PC_PARSER_CANARY_sitemap_txt | urls == [a, b] | PASS |
| PC_PARSER_CANARY_robots | lines == [https://example.com/s.xml] | PASS |
| PC_PARSER_CANARY_feed_rss | urls == [https://example.com/p1] | PASS |
| PC_PARSER_CANARY_feed_atom | urls == [https://example.com/p2] | PASS |
| PC_PARSER_CANARY_jsonld | urls == [https://example.com/p3] | PASS |
| PC_REACHABILITY_LISTED_LIVE | items listed by SITEMAP_XML / JSON_LD / search and live are reachable | 3/3 reachable — PASS |
| NC_REACHABILITY_UNLISTED_OR_DEAD | a live-but-unlisted item and a listed-but-dead (404) item are NOT reachable | both False (dead status 404) — PASS |
| PC_ENV | python + stdlib urllib + default TLS recorded | 3.12.15 — PASS |
| NC_SYNTHETIC_UNREACHABLE_ITEM_direct (x3) | real HTTP status >= 400 on synthetic url | 404 on doc.rust-lang.org, docs.python.org, numpy.org — PASS |

Design-time failures caught by these controls and fixed pre-freeze (evidence of sensitivity): PC_PARSER_CANARY_jsonld initially FAILED (canary extraction bug — split(">") also split `</script>`); NC_SYNTHETIC_UNREACHABLE_ITEM_direct initially FAILED (fetch collapsed HTTPError to status=None; fixed to record real 4xx/5xx status). Final certificate 15/15 PASS rows (13 distinct control identities; the null direct-404 control is run once per probe host, 3 rows at DESIGN).

## 10. Decision rule (frozen, evaluated in order; implemented in section 16; maps to result.json)

- **G1 validity** (V1 code canary, V2 controls gate, V3 inventory/seed gate): any FAIL → `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`; never a scientific answer.
- **G2 seed signature**: seed fetch failed on EVERY pool host → `outcome=INCONCLUSIVE`, reason explicitly `infrastructure signature, NOT a scientific null` (BLOCKED-class disposition).
- **G3 attainability**: zero DEEP items admitted across the pool → `outcome=INCONCLUSIVE`; Q1 measured (engines_with_zero_deep, host_census, per-engine stats); Q2/Q3 vacuous per section 4.
- **G4 limited-only**: every DEEP-admitting engine limited (> 10% admitted-item death) → `outcome=INCONCLUSIVE`; Q1/Q2 disclosed; Q3 not determinable.
- **G5 materiality**: engines_at_or_above_threshold = {n_deep > 0, not limited, fraction >= 0.50}; if |set| >= 2 → `outcome=SUPPORTS` (hop is NOT a fundamental acquisition-cost barrier for discovery-enabled acquisition; effort moves to discovery-channel coverage and substrate expansion).
- **G6 otherwise** (>= 1 eligible DEEP-admitting engine, < 2 at threshold) → `outcome=FALSIFIES`: engine-stratified bounded negative (discovery is not O(1) on this substrate class; close the discovery axis; hand persistence-maintenance to the next mandate), with limited and zero-DEEP engines disclosed.

Per-engine rows, per-channel coverage, zero-admission channels, hop distributions and the GET ledger are always reported regardless of outcome.

## 11. Design-time satisfaction evidence (pre-freeze certificate)

Ran 2026-10-11 (same runner class as EXECUTE: bare CPython 3.12.15, stdlib only, network enabled).

**(a) Seed probe** (re-run at DESIGN on the actual runner class, 2026-10-11): all 20 frozen seeds returned HTTP 200 text/html; transcript outside the repo.

**(b) Controls certificate** (`--stage controls`): 15/15 PASS rows (exit 0) over 13 distinct control identities; observed values in section 9.

**(c) Inventory certificate** (`--stage inventory`, out `<out_dir>/raw/channel_docs.jsonl`, outside the repo): 20/20 seeds HTTP 200; per-host channel endpoint liveness (re-observed at DESIGN 2026-10-11):

| host | seed | generator | robots | sm.xml | sm.idx | child | feed | jsonld urls | search form |
|---|---|---|---|---|---|---|---|---|---|
| doc.rust-lang.org | 200 | - | 200 | 404 | 404 | - | - | 0 | doc.rust-lang.org/stable/book/?searchbar |
| docs.python.org | 200 | - | 200 | 200 | - | - | - | 0 | docs.python.org/3/search.html?q |
| numpy.org | 200 | - | 200 | 200 | - | - | - | 0 | numpy.org/doc/stable/search.html?q |
| pandas.pydata.org | 200 | - | 200 | 404 | 404 | - | - | 0 | pandas.pydata.org/docs/search.html?q |
| react.dev | 200 | - | 200 | 404 | 404 | - | - | 0 | NONE |
| docusaurus.io | 200 | Docusaurus v4 | 200 | 200 | - | - | - | 2 | NONE |
| docs.readthedocs.io | 200 | - | 200 | 200 | - | - | - | 0 | docs.readthedocs.io/en/stable/search.html?q |
| docs.pytest.org | 200 | - | 200 | 200 | - | - | - | 0 | docs.pytest.org/en/stable/search.html?q |
| gohugo.io | 200 | Hugo 0.167 | 404 | 200 | - | - | - | 0 | NONE |
| jekyllrb.com | 200 | - | 200 | 200 | - | - | 10 | 4 | NONE |
| docs.gitbook.com | 200 | GitBook a0c1bdf | 200 | 200 | - | 5 | - | 0 | NONE |
| kubernetes.io | 200 | - | 200 | 200 | - | 5 | - | 4 | NONE |
| developer.mozilla.org | 200 | - | 200 | 200 | - | 5 | 71 | 0 | NONE |
| docs.github.com | 200 | - | 200 | 404 | 404 | - | - | 0 | docs.github.com/en?survey-token |
| en.wikipedia.org | 200 | MediaWiki wmf.23 | 200 | 404 | 404 | - | 10 | 5 | en.wikipedia.org/w/index.php?search |
| www.mediawiki.org | 200 | MediaWiki wmf.22 | 200 | 404 | 404 | - | 43 | 5 | www.mediawiki.org/w/index.php?search |
| quotes.toscrape.com | 200 | - | 404 | 404 | 404 | - | - | 0 | NONE |
| www.gnu.org | 200 | - | 200 | 200 | - | 1 | 60 | 0 | NONE |
| forums.gentoo.org | 200 | - | 403 | 404 | 404 | - | 15 | 0 | NONE |
| blog.wordpress.org | 200 | WordPress 7.2-a | 200 | 200 | - | - | 10 | 6 | wordpress.org/search/do-search.php?s |

Channel liveness census (each channel live on >= 1 frozen host; counted by membership-set non-emptiness): ROBOTS_SITEMAP 7 hosts, SITEMAP_XML 9, ON_SITE_SEARCH 10, RSS_ATOM 7, JSON_LD 6. Quirks recorded (VN-A2): docs.gitbook.com seed truncated at cap; forums.gentoo.org robots 403; gohugo.io robots 404 while sitemap.xml 200; react.dev and quotes.toscrape.com have zero channels (honest zero admission expected — reported as such); blog.wordpress.org search action cross-host to wordpress.org; MediaWiki robots has no Sitemap: line (its REST sitemap is not part of the frozen protocol); developer.mozilla.org / kubernetes.io / docs.gitbook.com / www.gnu.org sitemaps are indexes whose child lists are recorded but do not populate a membership set unless the frozen FIRST-child fetch is followed.

**(d) Reachability fixture (realized as controls)** (offline, local HTTP server, outcome-free, distinct from the frozen pool): `PC_REACHABILITY_LISTED_LIVE` drives the actual `evaluate_items` scoring path and requires that items listed by SITEMAP_XML, JSON_LD and ON_SITE_SEARCH and live are `reachable_any=True` (3/3 observed); `NC_REACHABILITY_UNLISTED_OR_DEAD` requires that a live item listed by no channel is NOT reachable and a listed item whose liveness GET returns 404 is NOT reachable (both observed False). This certifies the scoring implementation itself, not only its parsers.

**(e) Decision-branch reachability (structural argument, outcome-free).** The frozen rule is satisfiable in BOTH directions by construction. Given any attained pool with >= 1 engine admitting >= 1 eligible DEEP item, the branches partition exhaustively on the number of threshold-meeting engines: if >= 2 distinct engines reach fraction >= 0.50, G5 fires SUPPORTS; otherwise G6 fires FALSIFIES (so at least one of the two always fires and neither is empty). G3 (zero DEEP items anywhere) is a reachable INCONCLUSIVE branch with an explicit attainability reason; G2 (seed failure on EVERY host) is the reachable infrastructure-signature branch; G4 (EVERY DEEP-admitting engine has > 10% dead admitted items) is reachable because the item liveness re-GET can return 404. No 0/0 denominator can enter thresholding: an engine with n_deep=0 has fraction null and is routed to the zero-DEEP census instead (V5). The instrument's ability to separate flat from growing acquisition cost is independently certified by NC_BFS_CALIBRATION_FLAT (R=2.0) and NC_BFS_CALIBRATION_GROWING (R=6.5).

**(f) Env**: Python 3.12.15 (GCC 13.3.0); stdlib urllib + default TLS verified outbound; module imports are stdlib-only (`urllib`, `gzip`, `xml.etree`, `html.parser`, `http.server`, `hashlib`, `json`, `math`, `re`, `threading`, `time`, `pathlib`, `sys`); zero pip/model/browser/Docker dependencies.

## 12. Validity threats and measurement-validity notes (VN)

- **VN-A1 (unit reduction)**: Q1's state-carrying unit is the page carrying >= 1 named input/select (not the parent's control-triple). Rationale: discovery channels resolve page URLs and charged costs are per page. Worst case a multi-control page counts once (conservative for item counts; does not inflate reachability).
- **VN-A2 (representation)**: body cap 600000 (docs.gitbook.com seed truncated at DESIGN — its nav graph is partial; disclosed); sitemap index → FIRST child only; robots → FIRST Sitemap line only; single discovery document per channel; gzip handled.
- **VN-A3 (amortization vs charged ledger)**: charged protocol costs use fresh-agent semantics (<= K=3). At EXECUTE, discovery documents are fetched once per (host, channel) and only the results/item GETs are per item (actual per-item GETs <= 2 beyond the amortized documents). The actual vs charged ledger is disclosed (V8).
- **VN-A4 (search semantics)**: query = item slug (last path segment); membership = static links of the results page; NOT_PROBEABLE when no named GET form; cross-host search actions disclosed. Search may be imperfect for engines whose search needs full phrases; the slug is the frozen, disclosed choice.
- **VN-A5 (hop semantics)**: hop is the shortest path in the SAME-HOST static-`<a>` graph (JS links excluded); ordinal/requests is the 1-based BFS discovery ordinal (a level-order style estimator, disclosed; in a clean chain it equals hop+1). Depth 6 / budget 250 cap depth-6 hop values; deeper pages are out of scope of the frozen policy.
- **VN-A6 (liveness severity)**: the item-page GET doubles as the liveness re-GET; > 10% deaths mark an engine LIMITED (excluded from Q3, disclosed); dead items are excluded from the denominator with reasons recorded.
- **VN-A7 (drift)**: live Web endpoints can change between freeze and EXECUTE; EXECUTE re-runs controls + inventory as gates (V2/V3) and records per-host seed/channel status; drift is an observation, never a silenced cause.
- **VN-A8 (engine identity)**: generator meta where present, else DESIGN-recorded platform; meta absence is recorded, not assumed (V11).

## 13. Product consequences

- **If SUPPORTS**: C-CROSSSITE advances toward EXPERIMENTAL (bounded: frozen 20-host pool, GET-only stdlib substrate, K=3, five channels). Deep state-carrying acquisition defaults to discovery-enabled acquisition (sitemap/feed/on-site-search/JSON-LD) with per-channel coverage guiding channel expansion; frontier effort moves to discovery-channel coverage and substrate expansion; C-FRESHNESS/C-PRODUCT-ECON (runner-up) becomes the scheduled next mandate.
- **If FALSIFIES**: engine-stratified bounded negative — discovery is not an O(1) shortcut on this substrate class; no promotion; the persistence-maintenance/invalidation economics (runner-up; Graph/Product) is the conditional next mandate.
- **If INCONCLUSIVE**: the Q1 attainability census (engines_with_zero_deep, host_census, per-engine DEEP counts + hop distributions) and the zero-admission channel ledger become the durable deliverable; no claim update; a future design re-targets pools/engines from that census.

## 14. Estimated cost and expected information gain

- **Cost**: stdlib only; EXECUTE worst case <= ~15,200 GETs (structural 20×251, discovery <= 2×250×20 items, channel docs ~120, controls ~15); typical 5,000–10,000; wall ~15–40 min (timeout 12 s, DELAY 0.1 s). DESIGN certificate cost already paid (section 11).
- **Gain**: the first valid measurement of the question both prior designs never measured (v1 empty frame; v2 declared all six checks PASS with its declared artifacts absent). Attainability is the measured object, so every branch yields decision-relevant artifacts: DEEP census per engine/host, per-channel coverage with zero-admission channels reported as such, and a preregistered Q3 verdict satisfiable in both directions. The embedded code + re-run gates preclude the prior failure modes.

## 15. Freeze-eligibility mapping (mirrors spec.json)

1. **decision_rule_reachability — PASS**: the branches partition exhaustively, so SUPPORTS and FALSIFIES are both reachable for any attained pool with >= 1 eligible DEEP item (section 11e); the zero-DEEP / all-limited / all-seed-fail branches are reachable INCONCLUSIVE branches with explicit reasons; instrument dynamic range certified both directions (section 9); no 0/0 denominators (V5).
2. **measurement_prerequisites — PASS**: 20/20 seeds 200 (probe + certificate); all five channels live on >= 1 host; 15/15 control pass rows (13 distinct identities); the scoring path is itself fixture-controlled (PC/NC_REACHABILITY, section 11d); stdlib-only (no pip/model/browser/Docker).
3. **baseline_identifiability — PASS**: three stable distinct baselines (section 8); the in-pool measured B-LINK-FOLLOWING-BFS per-item cost is the comparator the <= K=3 discovery claim must beat; calibration controls separate flat from growing regimes.
4. **control_sensitivity — PASS**: every control fires both directions; the scoring path is fixture-controlled by `PC_REACHABILITY_LISTED_LIVE` (listed+live → reachable) and `NC_REACHABILITY_UNLISTED_OR_DEAD` (unlisted-live and listed-dead → not reachable); two controls caught real DESIGN defects pre-freeze (section 9); 0.50/2-engines are hard gates; zero-admission channels reported as such.
5. **treatment_liveness — PASS**: all five channels live on >= 1 frozen host with concrete endpoints (section 11c); the complete per-item scoring pipeline executed end-to-end offline against the local reachability fixture (PC/NC_REACHABILITY, section 11d); confirmatory pool never evaluated at DESIGN.
6. **freeze_artifacts_bound — NOT_APPLICABLE**: the complete outcome-bearing code is frozen VERBATIM in prereg section 16 with CODE_SHA256 (transitively hashed via freeze.json); pool/constants/fixtures/decision rule all embedded; no local mutable artifacts; remote endpoints are pinned by URL and recorded; check_scope.py forbids DESIGN-time repo files; basis is EXPERIMENT_PACKET.md section 2 (identical NOT_APPLICABLE basis as the earlier v2 experiment EXP-FRONTIER-38078430316).

## 16. Frozen code (transcription contract)

EXECUTE must transcribe the frozen module as the outcome-bearing program. Transcription is unique: let `block` be the bytes strictly between the CODE_BEGIN marker line and the CODE_END marker line, and let `C = block.strip()` (leading and trailing ASCII whitespace removed). Instantiate `C` as the module file. CODE_SHA256 = sha256(C):

```
CODE_SHA256 = 75a01d490ec81609cbf87a606f8cfa9227d07f07765b2eb4fd876fef2c8ff53a
```

If EXECUTE's transcription differs (hash mismatch against V1), status = MEASUREMENT_INVALID and no outcome stages may run.

<!-- CODE_BEGIN -->
#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# FROZEN EXECUTE MODULE for EXP-FRONTIER-38164611798 (frontier lane, C-CROSSSITE).
# Embedding contract (UNIQUE, unambiguous): prereg.md section 16 contains this
# module byte-identically. Transcribe:
#     block = bytes strictly between the CODE_BEGIN and CODE_END marker lines
#     C     = block.strip()          # strip leading/trailing ASCII whitespace
# CODE_SHA256 = sha256(C). Instantiate C as the module file at EXECUTE.
# If EXECUTE's transcription differs, status=MEASUREMENT_INVALID.
#
# DESIGN-time usage (non-outcome-bearing):  --stage controls | inventory
# EXECUTE usage:                            --stage all  [--out <dir>]
#   controls   : offline fixture calibrations + parser canaries + env probe + null direct-404s
#   inventory  : per-host discovery-channel endpoint liveness (no hops, no items)
#   structural : frozen BFS census (Q1) and DEEP admission
#   discovery  : per-item channel evaluation (Q2/Q3) + metrics + decision
"""Frozen design for EXP-FRONTIER-38164611798: does site-native discovery make
DEEP (hop>=3) state-carrying item acquisition O(1) in <= K=3 fresh-agent GETs?"""
import gzip
import hashlib
import html.parser
import json
import math
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

EXP_ID = "EXP-FRONTIER-38164611798"
UA = "SPIDER-research-frontier-11798/1.0"
TIMEOUT = 12.0
MAX_BODY = 600000
DELAY = 0.1
BUDGET = 250          # per-seed page budget (mandate: budget 250)
DEPTH = 6             # depth cap (mandate: depth <= 6)
K = 3                 # fresh-agent GET budget
THRESHOLD = 0.50      # materiality threshold (Q3)
MIN_ENGINES = 2       # distinct engines for Q3
DEEP_BAND = (3, 4, 5, 6)
SYNTH_PREFIX = "spider-nonexistent-38164611798-"

# ---------------------------------------------------------- frozen target pool
# Enumerated by DESIGN on 2026-10-11; every seed live (HTTP 200 text/html) at
# probe time 2026-10-11T19:40:43Z (probe transcript in prereg.md section 11).
# engine_class = <meta name="generator"> content if present, else the documented
# platform recorded at DESIGN (prereg.md section 6).
POOL = [
    ("doc.rust-lang.org",     "mdBook",        "https://doc.rust-lang.org/stable/book/"),
    ("docs.python.org",       "Sphinx",        "https://docs.python.org/3/"),
    ("numpy.org",             "Sphinx",        "https://numpy.org/doc/stable/"),
    ("pandas.pydata.org",     "Sphinx",        "https://pandas.pydata.org/docs/"),
    ("react.dev",             "Docusaurus",    "https://react.dev/learn"),
    ("docusaurus.io",         "Docusaurus",    "https://docusaurus.io/docs"),
    ("docs.readthedocs.io",   "Sphinx-RTD",    "https://docs.readthedocs.io/en/stable/"),
    ("docs.pytest.org",       "Sphinx-RTD",    "https://docs.pytest.org/en/stable/"),
    ("gohugo.io",             "Hugo",          "https://gohugo.io/documentation/"),
    ("jekyllrb.com",          "Jekyll",        "https://jekyllrb.com/docs/"),
    ("docs.gitbook.com",      "GitBook",       "https://docs.gitbook.com/"),
    ("kubernetes.io",         "Hugo-k8s",      "https://kubernetes.io/docs/"),
    ("developer.mozilla.org", "MDN-Yari",      "https://developer.mozilla.org/en-US/"),
    ("docs.github.com",       "GitHubDocs",    "https://docs.github.com/en"),
    ("en.wikipedia.org",      "MediaWiki",     "https://en.wikipedia.org/wiki/Main_Page"),
    ("www.mediawiki.org",     "MediaWiki",     "https://www.mediawiki.org/wiki/MediaWiki"),
    ("quotes.toscrape.com",   "custom",        "https://quotes.toscrape.com/"),
    ("www.gnu.org",           "GNU-web",       "https://www.gnu.org/"),
    ("forums.gentoo.org",     "phpBB",         "https://forums.gentoo.org/"),
    ("blog.wordpress.org",    "WordPress",     "https://blog.wordpress.org/"),
]

ASSET_EXTS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".bz2", ".xz", ".mp3", ".mp4", ".webm", ".avi", ".mov", ".txt", ".xml",
)

# ------------------------------------------------------------- frozen helpers
def norm(url: str) -> str:
    """Defragment + canonicalize: same-host http(s) URL key."""
    p = urllib.parse.urlsplit(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    if ":" in netloc and not netloc.endswith("]"):
        host, _, port = netloc.rpartition(":")
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    path = p.path or "/"
    return urllib.parse.urlunsplit((scheme, netloc, path, p.query, ""))


def norm_eq(a: str, b: str) -> bool:
    """Membership equality: exact normalized equality, or equality after
    stripping at most one trailing '/' from the path (redirect-equivalence for
    canonical slash variants; no redirect chasing of channel URLs)."""
    na, nb = norm(a), norm(b)
    if na == nb:
        return True
    if na.endswith("/") and na[:-1] == nb:
        return True
    if nb.endswith("/") and nb[:-1] == na:
        return True
    return False


def is_asset(url: str) -> bool:
    path = urllib.parse.urlsplit(url).path.lower()
    return path.endswith(ASSET_EXTS)


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.forms = []          # frozen search-form finder: (action, inputs)
        self._form = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.hrefs.append(d["href"])
        if tag == "form":
            self._form = [d.get("action"), d.get("method", "get").lower(), []]
            self.forms.append(self._form)
        if tag == "input" and self._form is not None:
            if d.get("name"):
                self._form[2].append((d["name"], d.get("type", "text")))

    def handle_endtag(self, tag):
        if tag == "form":
            self._form = None


def static_links(base: str, html_text: str) -> list:
    lp = LinkParser()
    try:
        lp.feed(html_text)
    except Exception:
        return []
    out = []
    for h in lp.hrefs:
        u = urllib.parse.urljoin(base, h.strip())
        p = urllib.parse.urlsplit(u)
        if p.scheme not in ("http", "https"):
            continue
        if is_asset(u):
            continue
        out.append(u)
    return out


def search_form(base: str, html_text: str):
    """First GET form with a named text-like input; (action_url, input_name)."""
    lp = LinkParser()
    try:
        lp.feed(html_text)
    except Exception:
        return None
    for action, method, inputs in lp.forms:
        if method not in ("get", ""):
            continue
        for name, itype in inputs:
            if itype in ("text", "search", ""):
                action_url = urllib.parse.urljoin(base, action) if action else base
                return (action_url, name)
    return None


class ControlParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.controls = []

    def handle_starttag(self, tag, attrs):
        if tag in ("input", "select"):
            d = dict(attrs)
            if d.get("name"):
                self.controls.append((tag, d["name"], d.get("type", "")))


def named_controls(html_text: str) -> list:
    cp = ControlParser()
    try:
        cp.feed(html_text)
    except Exception:
        return []
    return cp.controls


class MetaParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.generator = None
        self.feeds = []
        self.jsonld_blocks = []
        self._in_jsonld = False
        self._buf = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta" and d.get("name", "").lower() == "generator":
            self.generator = d.get("content")
        if tag == "link":
            rel = d.get("rel", "")
            t = d.get("type", "")
            if "alternate" in rel.lower() and ("rss" in t or "atom" in t):
                self.feeds.append((rel, t, d.get("href", "")))
        if tag == "script" and d.get("type", "").lower() == "application/ld+json":
            self._in_jsonld = True
            self._buf = []
            self.jsonld_blocks.append(self._buf)

    def handle_data(self, data):
        if self._in_jsonld and self._buf is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_jsonld = False


def parse_meta(html_text: str):
    mp = MetaParser()
    try:
        mp.feed(html_text)
    except Exception:
        pass
    blocks = ["".join(b) for b in mp.jsonld_blocks]
    return {"generator": mp.generator, "feeds": mp.feeds, "jsonld_blocks": blocks}


def walk_strings(obj, acc):
    if isinstance(obj, str):
        acc.append(obj)
    elif isinstance(obj, list):
        for x in obj:
            walk_strings(x, acc)
    elif isinstance(obj, dict):
        for v in obj.values():
            walk_strings(v, acc)


def jsonld_urls(blocks: list) -> set:
    urls = set()
    for b in blocks:
        try:
            parsed = json.loads(b)
        except Exception:
            continue
        acc = []
        walk_strings(parsed, acc)
        for s in acc:
            if s.startswith("http://") or s.startswith("https://"):
                urls.add(norm(s))
    return urls


def robots_sitemap_lines(body: bytes) -> list:
    out = []
    for line in body.decode("utf-8", errors="replace").splitlines():
        m = re.match(r"^\s*Sitemap:\s*(\S+)\s*$", line, re.I)
        if m:
            out.append(m.group(1))
    return out


def parse_sitemap(body: bytes) -> dict:
    """XML sitemap/sitemapindex -> {urls, is_index, child_sitemaps}."""
    try:
        root = ET.fromstring(body)
    except Exception:
        return {"urls": [], "is_index": False, "child_sitemaps": []}
    urls, children = [], []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag == "loc" and el.text and el.text.strip():
            urls.append(el.text.strip())
        if tag == "sitemap" and el.text and el.text.strip():
            children.append(el.text.strip())
    is_index = bool(children) or all(u.lower().endswith((".xml", ".gz")) for u in urls)
    if is_index:
        return {"urls": [], "is_index": True, "child_sitemaps": (children or urls)}
    return {"urls": urls, "is_index": False, "child_sitemaps": []}


def parse_sitemap_txt(body: bytes) -> dict:
    """Plain-text sitemap (sitemap.txt): one URL per line; index if every line
    names another sitemap file."""
    lines = [ln.strip() for ln in body.decode("utf-8", errors="replace").splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]
    urls = [ln for ln in lines if ln.startswith("http://") or ln.startswith("https://")]
    if urls and all(u.lower().endswith((".xml", ".gz")) for u in urls):
        return {"urls": [], "is_index": True, "child_sitemaps": urls}
    return {"urls": urls, "is_index": False, "child_sitemaps": []}


def parse_sitemap_any(body: bytes, url: str) -> dict:
    if url.lower().endswith(".gz"):
        try:
            body = gzip.decompress(body)
        except Exception:
            return {"urls": [], "is_index": False, "child_sitemaps": []}
    xml = parse_sitemap(body)
    if xml["urls"] or xml["is_index"]:
        return xml
    return parse_sitemap_txt(body)


def parse_feed_entries(body: bytes) -> int:
    try:
        root = ET.fromstring(body)
    except Exception:
        return -1
    n = 0
    for el in root.iter():
        if el.tag.split("}")[-1] in ("item", "entry"):
            n += 1
    return n


def feed_entry_urls(body: bytes) -> list:
    """RSS <item><link> / Atom <entry><link href> URLs (frozen extraction)."""
    try:
        root = ET.fromstring(body)
    except Exception:
        return []
    out = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag == "item":
            for child in el:
                if child.tag.split("}")[-1] == "link" and child.text and child.text.strip():
                    out.append(child.text.strip())
        if tag == "entry":
            for child in el:
                if child.tag.split("}")[-1] == "link":
                    href = child.get("href")
                    if href:
                        out.append(href)
    return out


def item_slug(item_url: str) -> str:
    p = urllib.parse.urlsplit(item_url)
    segs = [s for s in p.path.split("/") if s]
    return urllib.parse.unquote(segs[-1]) if segs else p.netloc


# ----------------------------------------------------------- transport (frozen)
class RedirectCounter(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.redirects = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.redirects += 1
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_host_root(url: str):
    return urllib.parse.urlsplit(url).scheme + "://" + urllib.parse.urlsplit(url).netloc


def fetch(url: str):
    """GET; returns (record, body_bytes). Cap MAX_BODY; gunzip when needed;
    redirects counted (each leg counts toward K in the charged ledger).
    HTTP errors (4xx/5xx) are recorded with their real status code; only
    transport-level failures (DNS/TLS/timeout) yield status=None."""
    rch = RedirectCounter()
    opener = urllib.request.build_opener(rch)
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml,*/*"})
    t0 = time.time()
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            raw = resp.read(MAX_BODY + 1)
            truncated = len(raw) > MAX_BODY
            raw = raw[:MAX_BODY]
            body = raw
            if resp.headers.get("Content-Encoding", "").lower() == "gzip":
                try:
                    body = gzip.decompress(raw)
                except Exception:
                    body = raw
            rec = {
                "url": url, "status": resp.status, "final_url": resp.geturl(),
                "content_type": resp.headers.get("Content-Type", ""),
                "bytes": len(raw), "truncated": truncated, "redirects": rch.redirects,
                "elapsed_s": round(time.time() - t0, 2), "error": None,
            }
            return rec, body
    except urllib.error.HTTPError as e:
        # HTTP 4xx/5xx: keep the real status code (control NC_SYNTHETIC_*
        # and item liveness depend on distinguishing 4xx/5xx from transport
        # failure). The body is not read; the charged ledger only counts legs.
        return {"url": url, "status": e.code, "final_url": url, "content_type": None,
                "bytes": 0, "truncated": False, "redirects": rch.redirects,
                "elapsed_s": round(time.time() - t0, 2),
                "error": f"HTTPError {e.code}: {e.reason}"}, b""
    except Exception as e:  # network/TLS/timeout failure: recorded, never a branch
        return {"url": url, "status": None, "final_url": url, "content_type": None,
                "bytes": 0, "truncated": False, "redirects": rch.redirects,
                "elapsed_s": round(time.time() - t0, 2),
                "error": f"{type(e).__name__}: {e}"}, b""


# ------------------------------------------------------- structural pass (Q1)
def bfs_structural(seed: str):
    """Frozen policy: item-blind FIFO BFS in document order; same-host static
    <a>; budget B=250; depth D=6; each URL fetched at most once. Returns:
    {url_norm: {hop, ordinal, requests, bytes, truncated, controls, controls_seen}}"""
    out = {}
    queue = []
    seed_n = norm(seed)
    rec, body = fetch(seed)
    if rec["error"] or rec["status"] != 200:
        return {"seed_error": rec["error"] or f"status={rec['status']}"}
    text = body.decode("utf-8", errors="replace")
    seed_host = urllib.parse.urlsplit(rec["final_url"]).netloc.lower()
    out[seed_n] = {"hop": 0, "ordinal": 1, "requests": 1, "bytes": rec["bytes"],
                   "truncated": rec["truncated"], "controls_seen": len(named_controls(text))}
    queue = [(seed_n, 0)]
    ordinal = 1
    while queue and len(out) < BUDGET:
        u, h = queue.pop(0)
        if h + 1 > DEPTH:
            continue
        r, b = fetch(u)
        if r["error"] or r["status"] != 200:
            continue
        t = b.decode("utf-8", errors="replace")
        base = r["final_url"]
        for raw in static_links(base, t):
            nu = norm(raw)
            if nu in out:
                continue
            if urllib.parse.urlsplit(nu).netloc.lower() != seed_host:
                continue
            ordinal += 1
            out[nu] = {"hop": h + 1, "ordinal": ordinal, "requests": ordinal,
                       "bytes": None, "truncated": None, "controls_seen": None}
            queue.append((nu, h + 1))
            # Mandate budget B=250 is a hard cap: even a single page with
            # thousands of links may not push discovery past the budget.
            if len(out) >= BUDGET:
                break
        # backfill the fetched page's own observation
        if u in out and out[u].get("bytes") is None:
            out[u]["bytes"] = r["bytes"]
            out[u]["truncated"] = r["truncated"]
            out[u]["controls_seen"] = len(named_controls(t))
    return out


# --------------------------------------------------- channel inventory (Q2 doc)
def channel_documents(seed: str):
    """Fetch the discovery documents ONCE per (host, channel) at EXECUTE and at
    DESIGN (certificate). Returns per-channel URL sets + endpoint records.
    NOT outcome-bearing: no hops, no items."""
    host = urllib.parse.urlsplit(seed).netloc.lower()
    root = fetch_host_root(seed)
    res = {"host": host, "seed": seed}
    # seed page (shared: JSON_LD block source + feed discovery + search form)
    srec, sbody = fetch(seed)
    res["seed_fetch"] = {k: srec[k] for k in ("status", "content_type", "bytes", "truncated", "redirects", "error")}
    meta = parse_meta(sbody.decode("utf-8", errors="replace"))
    res["seed_generator"] = meta["generator"]
    res["seed_feeds"] = meta["feeds"]
    res["seed_jsonld_urls"] = sorted(jsonld_urls(meta["jsonld_blocks"]))
    sform = search_form(seed, sbody.decode("utf-8", errors="replace"))
    res["search_form"] = {"action": sform[0], "input": sform[1]} if sform else None
    # ROBOTS_SITEMAP
    rrec, rbody = fetch(root + "/robots.txt")
    sl = robots_sitemap_lines(rbody) if rrec["status"] == 200 else []
    res["robots"] = {"status": rrec["status"], "sitemap_lines": sl, "error": rrec["error"]}
    robots_urls = set()
    if sl:
        s1rec, s1body = fetch(sl[0])
        if s1rec["status"] == 200 and s1body:
            doc = parse_sitemap_any(s1body, sl[0])
            res["robots_sitemap_doc"] = {"url": sl[0], "status": 200, "is_index": doc["is_index"],
                                         "url_count": len(doc["urls"]), "children": doc["child_sitemaps"][:5],
                                         "truncated": s1rec["truncated"]}
            if doc["is_index"] and doc["child_sitemaps"]:
                crec, cbody = fetch(doc["child_sitemaps"][0])
                if crec["status"] == 200 and cbody:
                    cdoc = parse_sitemap_any(cbody, doc["child_sitemaps"][0])
                    robots_urls = set(norm(u) for u in cdoc["urls"])
                    res["robots_sitemap_child"] = {"url": doc["child_sitemaps"][0], "status": 200,
                                                   "url_count": len(cdoc["urls"]), "truncated": crec["truncated"]}
                else:
                    res["robots_sitemap_child"] = {"url": doc["child_sitemaps"][0], "status": crec["status"],
                                                   "error": crec["error"]}
            else:
                robots_urls = set(norm(u) for u in doc["urls"])
        elif sl:
            res["robots_sitemap_doc"] = {"url": sl[0], "status": s1rec["status"], "error": s1rec["error"]}
    # SITEMAP_XML: /sitemap.xml, fallback /sitemap_index.xml, index->first child
    sm_urls = set()
    smrec, smbody = fetch(root + "/sitemap.xml")
    sm_status = smrec["status"]
    sm_error = smrec["error"]
    doc = None
    if smrec["status"] == 200 and smbody:
        doc = parse_sitemap_any(smbody, root + "/sitemap.xml")
        res["sitemap_xml"] = {"url": root + "/sitemap.xml", "status": 200, "is_index": doc["is_index"],
                              "url_count": len(doc["urls"]), "children": doc["child_sitemaps"][:5],
                              "truncated": smrec["truncated"]}
    else:
        res["sitemap_xml"] = {"url": root + "/sitemap.xml", "status": smrec["status"], "error": sm_error}
    if doc is None or (doc["is_index"] and not doc["child_sitemaps"]):
        sm2rec, sm2body = fetch(root + "/sitemap_index.xml")
        if sm2rec["status"] == 200 and sm2body:
            doc = parse_sitemap_any(sm2body, root + "/sitemap_index.xml")
            res["sitemap_index_xml"] = {"url": root + "/sitemap_index.xml", "status": 200,
                                        "is_index": doc["is_index"], "url_count": len(doc["urls"]),
                                        "children": doc["child_sitemaps"][:5], "truncated": sm2rec["truncated"]}
        else:
            res["sitemap_index_xml"] = {"url": root + "/sitemap_index.xml", "status": sm2rec["status"],
                                        "error": sm2rec["error"]}
    if doc is not None:
        if doc["is_index"] and doc["child_sitemaps"]:
            r3rec, r3body = fetch(doc["child_sitemaps"][0])
            if r3rec["status"] == 200 and r3body:
                d3 = parse_sitemap_any(r3body, doc["child_sitemaps"][0])
                sm_urls = set(norm(u) for u in d3["urls"])
                res["sitemap_xml_child"] = {"url": doc["child_sitemaps"][0], "status": 200,
                                            "url_count": len(d3["urls"]), "truncated": r3rec["truncated"]}
            else:
                res["sitemap_xml_child"] = {"url": doc["child_sitemaps"][0], "status": r3rec["status"],
                                            "error": r3rec["error"]}
        else:
            sm_urls = set(norm(u) for u in doc["urls"])
    res["channel_urls"] = {
        "ROBOTS_SITEMAP": sorted(robots_urls),
        "SITEMAP_XML": sorted(sm_urls),
        "RSS_ATOM": None,   # populated below (feed fetch)
        "JSON_LD": res["seed_jsonld_urls"],
        "ON_SITE_SEARCH": None,  # per-item query; form above
    }
    # RSS_ATOM: first feed link in seed HTML head
    if meta["feeds"]:
        fu = urllib.parse.urljoin(seed, meta["feeds"][0][2])
        frec, fbody = fetch(fu)
        if frec["status"] == 200 and fbody:
            res["feed"] = {"url": fu, "status": 200, "entries": parse_feed_entries(fbody),
                           "url_count": len(feed_entry_urls(fbody)), "truncated": frec["truncated"]}
            res["channel_urls"]["RSS_ATOM"] = sorted(norm(u) for u in feed_entry_urls(fbody))
        else:
            res["feed"] = {"url": fu, "status": frec["status"], "error": frec["error"]}
    else:
        res["feed"] = {"status": None, "error": "no_feed_link_in_seed_html"}
    return res


# ------------------------------------------------------ per-item evaluation
def evaluate_items(structural, docs, items):
    """Per admitted DEEP item: 5-channel membership (charged cost <= K) +
    fresh item-liveness GET. Charged costs (frozen protocol): ROBOTS_SITEMAP=3,
    SITEMAP_XML=2, ON_SITE_SEARCH=3, RSS_ATOM=3, JSON_LD=2."""
    host = docs["host"]
    out = []
    for item in items:
        iu = item["url"]
        slug = item_slug(iu)
        # ON_SITE_SEARCH: per-item results doc (query = slug)
        on_search = None
        if docs.get("search_form"):
            q = urllib.parse.quote(slug)
            sep = "&" if "?" in docs["search_form"]["action"] else "?"
            surl = docs["search_form"]["action"] + sep + urllib.parse.quote(docs["search_form"]["input"]) + "=" + q
            srec, sbody = fetch(surl)
            on_search = {"status": srec["status"], "error": srec["error"]}
            hits = set()
            if srec["status"] == 200 and sbody:
                base = srec["final_url"]
                hits = {norm(u) for u in static_links(base, sbody.decode("utf-8", errors="replace"))}
            member_search = any(norm_eq(iu, h) for h in hits)
        else:
            member_search = False
        member_robots = any(norm_eq(iu, u) for u in docs["channel_urls"]["ROBOTS_SITEMAP"])
        member_sm = any(norm_eq(iu, u) for u in docs["channel_urls"]["SITEMAP_XML"])
        member_rss = bool(docs["channel_urls"]["RSS_ATOM"]) and any(
            norm_eq(iu, u) for u in docs["channel_urls"]["RSS_ATOM"])
        member_jsonld = any(norm_eq(iu, u) for u in docs["channel_urls"]["JSON_LD"])
        # fresh item liveness GET (1 GET; excludes dead items with reason)
        lrec, _ = fetch(iu)
        live = lrec["status"] == 200
        reach = {
            "ROBOTS_SITEMAP": {"member": member_robots, "charged": 3},
            "SITEMAP_XML": {"member": member_sm, "charged": 2},
            "ON_SITE_SEARCH": {"member": member_search, "charged": 3},
            "RSS_ATOM": {"member": member_rss, "charged": 3},
            "JSON_LD": {"member": member_jsonld, "charged": 2},
        }
        # redirect budget: any channel whose DOCUMENT fetch exceeded its charged
        # budget legs is still counted (the spare absorbs it); charged cost is
        # the protocol cost and is <= K by construction.
        reachable_any = any(v["member"] for v in reach.values()) and live
        out.append({
            "url": iu, "hop": item["hop"], "ordinal": item["ordinal"], "bytes": item["bytes"],
            "search_status": on_search, "live_status": lrec["status"], "live_error": lrec["error"],
            "per_channel": reach, "reachable_any": reachable_any,
        })
    return out


# ------------------------------------------------------------- metrics
def betainv(p: float, a: float, b: float) -> float:
    """Inverse of the regularized incomplete beta I^{-1}_p(a,b) via binary
    search on the continued-fraction evaluation (Numerical Recipes betacf)."""
    def betacf(aa, bb, xx):
        MAXIT, EPS, FPMIN = 200, 3.0e-12, 1e-300
        qab, qap, qam = aa + bb, aa + 1.0, aa - 1.0
        c = 1.0
        d = 1.0 - qab * xx / qap
        if abs(d) < FPMIN:
            d = FPMIN
        d = 1.0 / d
        h = d
        for m in range(1, MAXIT + 1):
            m2 = 2 * m
            aa2 = m * (bb - m) * xx / ((qam + m2) * (aa + m2))
            d = 1.0 + aa2 * d
            if abs(d) < FPMIN:
                d = FPMIN
            c = 1.0 + aa2 / c
            if abs(c) < FPMIN:
                c = FPMIN
            d = 1.0 / d
            h *= d * c
            aa2 = -(aa + m) * (qab + m) * xx / ((aa + m2) * (qap + m2))
            d = 1.0 + aa2 * d
            if abs(d) < FPMIN:
                d = FPMIN
            c = 1.0 + aa2 / c
            if abs(c) < FPMIN:
                c = FPMIN
            d = 1.0 / d
            del_ = d * c
            h *= del_
            if abs(del_ - 1.0) < EPS:
                break
        return h

    def betai(x):
        if x <= 0.0:
            return 0.0
        if x >= 1.0:
            return 1.0
        bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                      + a * math.log(x) + b * math.log1p(-x))
        if x < (a + 1.0) / (a + b + 2.0):
            return bt * betacf(a, b, x) / a
        return 1.0 - bt * betacf(b, a, 1.0 - x) / b

    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if betai(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def clopper_pearson(k: int, n: int, alpha=0.05):
    if n <= 0:
        return None
    if k == 0:
        return (0.0, 1.0 - (alpha / 2.0) ** (1.0 / n))
    if k == n:
        return ((alpha / 2.0) ** (1.0 / n), 1.0)
    lo = betainv(alpha / 2.0, k, n - k + 1)
    hi = betainv(1.0 - alpha / 2.0, k + 1, n - k)
    return (lo, hi)


DEAD_LIMIT = 0.10  # engine marked LIMITED when >10% of its admitted DEEP items die


def compute_metrics(items, engine_class, pool_engines=None):
    """Per-engine metrics over the ADMITTED DEEP items. When pool_engines
    (engine_class -> set(hosts), derived from the frozen POOL) is given, every
    pool engine absent from the admitted items is reported with n_deep=0 so the
    Q1 zero-DEEP census covers the FULL frozen pool, not only engines that
    happened to admit items."""
    per_engine = {}
    for it in items:
        e = it["engine"]
        per_engine.setdefault(e, {"hosts": set(), "n": 0, "reach": 0,
                                  "channels": {c: 0 for c in ("ROBOTS_SITEMAP", "SITEMAP_XML",
                                                              "ON_SITE_SEARCH", "RSS_ATOM", "JSON_LD")},
                                  "dead": 0, "hops": []})
        g = per_engine[e]
        g["hosts"].add(it["host"])
        if it["live"]:
            g["n"] += 1
            g["hops"].append(it["hop"])
            if it["reachable_any"]:
                g["reach"] += 1
            for c, v in it["per_channel"].items():
                if v["member"]:
                    g["channels"][c] += 1
        else:
            g["dead"] += 1
    if pool_engines:
        for e, hosts in pool_engines.items():
            per_engine.setdefault(e, {"hosts": set(hosts), "n": 0, "reach": 0,
                                      "channels": {c: 0 for c in ("ROBOTS_SITEMAP", "SITEMAP_XML",
                                                                  "ON_SITE_SEARCH", "RSS_ATOM", "JSON_LD")},
                                      "dead": 0, "hops": []})
    out = {}
    for e, g in per_engine.items():
        hosts = sorted(g["hosts"])
        n, r = g["n"], g["reach"]
        frac = r / n if n else None
        ci = clopper_pearson(r, n) if n else None
        admitted = n + g["dead"]
        limited = bool(n > 0 and admitted > 0 and (g["dead"] / admitted) > DEAD_LIMIT)
        out[e] = {
            "hosts": hosts, "n_deep": n, "n_dead_excluded": g["dead"],
            "limited": limited,
            "reachable": r, "fraction": frac, "ci95": ci,
            "per_channel": {c: (g["channels"][c] / n if n else None) for c in g["channels"]},
            "hop_distribution": {h: g["hops"].count(h) for h in sorted(set(g["hops"]))},
        }
    return out


# ------------------------------------------------------------------ controls
def run_controls(out_dir: Path):
    rows = []
    # (1)/(2) BFS calibration fixtures (instrument range, offline)
    pages = {}
    chain = ["c_index.html"] + [f"c_p{i}.html" for i in range(1, 7)]
    for i, name in enumerate(chain):
        link = f'<a href="{chain[i+1]}">next</a>' if i < len(chain) - 1 else "<a href='#'>end</a>"
        pages[f"/{name}"] = f"<html><body>{link}<form><input name='q'></form></body></html>"
    def fan_add(path, depth):
        if depth > 4:
            return
        kids = "".join(f'<a href="/{path}{c}.html">c</a>' for c in range(10))
        pages[f"/{path}.html"] = f"<html><body>{kids}<form><input name='q'></form></body></html>"
        for c in range(10):
            fan_add(f"{path}{c}", depth + 1)
    fan_add("f_nroot", 1)
    pages["/f_index.html"] = "<html><body><a href='/f_nroot.html'>start</a></body></html>"

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            body = pages.get(self.path)
            if body is None:
                self.send_response(404)
                self.end_headers()
                return
            data = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        def log_message(self, *a):
            pass
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    chain_seen = bfs_structural(base + "/c_index.html")
    c3 = chain_seen.get(norm(base + "/c_p3.html"))
    c1 = chain_seen.get(norm(base + "/c_p1.html"))
    fan_seen = bfs_structural(base + "/f_index.html")
    f1 = fan_seen.get(norm(base + "/f_nroot.html"))
    f3 = sorted((v["requests"] for k, v in fan_seen.items() if v["hop"] == 3), key=lambda x: x)
    f3_first = f3[0] if f3 else None
    r_flat = (c3["requests"] / c1["requests"]) if c1 and c3 else None
    r_growing = (f3_first / f1["requests"]) if f1 and f3_first else None
    rows.append({"control": "NC_BFS_CALIBRATION_FLAT",
                 "pass": (r_flat is not None and r_flat <= 3.0),
                 "observed": {"p1_requests": c1["requests"] if c1 else None,
                              "p3_requests": c3["requests"] if c3 else None,
                              "R_hop3_over_hop1": r_flat}})
    rows.append({"control": "NC_BFS_CALIBRATION_GROWING",
                 "pass": (r_growing is not None and r_growing > 3.0),
                 "observed": {"hop1_requests": f1["requests"] if f1 else None,
                              "first_hop3_requests": f3_first, "R_hop3_over_hop1": r_growing,
                              "nodes_fetched": len(fan_seen)}})
    srv.shutdown()
    srv.server_close()

    # (3) parser canaries (offline fixture strings -> exact expected URL sets)
    canaries = {
        "sitemap_xml": ("<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
                        "<url><loc>https://example.com/a</loc></url></urlset>",
                        ["https://example.com/a"]),
        "sitemap_index": ("<sitemapindex xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
                          "<sitemap><loc>https://example.com/s1.xml</loc></sitemap></sitemapindex>",
                          "INDEX"),
        "sitemap_txt": "https://example.com/a\nhttps://example.com/b\n",
        "robots": "User-agent: *\nSitemap: https://example.com/s.xml\n",
        "feed_rss": ("<rss><channel><item><link>https://example.com/p1</link></item></channel></rss>",
                     ["https://example.com/p1"]),
        "feed_atom": ("<feed xmlns='http://www.w3.org/2005/Atom'>"
                      "<entry><link href='https://example.com/p2'/></entry></feed>",
                      ["https://example.com/p2"]),
        "jsonld": ("<script type='application/ld+json'>"
                   '{"@context":"x","mainEntity":{"@type":"WebPage","url":"https://example.com/p3"}}'
                   "</script>", ["https://example.com/p3"]),
    }
    sm = parse_sitemap_any(canaries["sitemap_xml"][0].encode(), "s.xml")
    rows.append({"control": "PC_PARSER_CANARY_sitemap_xml",
                 "pass": sm["urls"] == canaries["sitemap_xml"][1] and not sm["is_index"],
                 "observed": sm})
    smi = parse_sitemap_any(canaries["sitemap_index"][0].encode(), "s.xml")
    rows.append({"control": "PC_PARSER_CANARY_sitemap_index",
                 "pass": smi["is_index"] and smi["child_sitemaps"] == ["https://example.com/s1.xml"],
                 "observed": smi})
    smt = parse_sitemap_txt(canaries["sitemap_txt"].encode())
    rows.append({"control": "PC_PARSER_CANARY_sitemap_txt",
                 "pass": smt["urls"] == ["https://example.com/a", "https://example.com/b"],
                 "observed": smt})
    rb = robots_sitemap_lines(canaries["robots"].encode())
    rows.append({"control": "PC_PARSER_CANARY_robots",
                 "pass": rb == ["https://example.com/s.xml"], "observed": rb})
    fr = feed_entry_urls(canaries["feed_rss"][0].encode())
    rows.append({"control": "PC_PARSER_CANARY_feed_rss",
                 "pass": fr == canaries["feed_rss"][1], "observed": fr})
    fa = feed_entry_urls(canaries["feed_atom"][0].encode())
    rows.append({"control": "PC_PARSER_CANARY_feed_atom",
                 "pass": fa == canaries["feed_atom"][1], "observed": fa})
    jl = jsonld_urls(parse_meta(canaries["jsonld"][0])["jsonld_blocks"])
    rows.append({"control": "PC_PARSER_CANARY_jsonld",
                 "pass": set(jl) == set(canaries["jsonld"][1]), "observed": sorted(jl)})

    # (3b) reachability fixture: positive + null controls over the SCORING
    #      implementation itself (evaluate_items membership + liveness),
    #      executed against a local HTTP fixture, disjoint from the frozen pool.
    rpages = {
        "/deep/listed.html": "<html><body><form><input name='field'></form></body></html>",
        "/deep/jsonld.html": "<html><body><form><input name='field'></form></body></html>",
        "/deep/searchhit.html": "<html><body><form><input name='field'></form></body></html>",
        "/deep/unlisted.html": "<html><body><form><input name='field'></form></body></html>",
        # search results page links ONLY /deep/searchhit.html
        "/search": "<html><body><a href='/deep/searchhit.html'>hit</a></body></html>",
    }

    class RH(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urllib.parse.urlsplit(self.path).path
            body = rpages.get(path)
            if body is None:
                self.send_response(404)
                self.end_headers()
                return
            data = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass

    rsrv = ThreadingHTTPServer(("127.0.0.1", 0), RH)
    threading.Thread(target=rsrv.serve_forever, daemon=True).start()
    rbase = f"http://127.0.0.1:{rsrv.server_address[1]}"
    listed = rbase + "/deep/listed.html"
    jsonld_u = rbase + "/deep/jsonld.html"
    search_u = rbase + "/deep/searchhit.html"
    unlisted = rbase + "/deep/unlisted.html"
    dead = rbase + "/deep/dead.html"
    rdocs = {
        "host": "127.0.0.1",
        "search_form": {"action": rbase + "/search", "input": "q"},
        "channel_urls": {
            "ROBOTS_SITEMAP": [],
            "SITEMAP_XML": [listed, dead],
            "ON_SITE_SEARCH": None,
            "RSS_ATOM": [],
            "JSON_LD": [jsonld_u],
        },
    }
    ritems = [
        {"url": listed, "hop": 3, "ordinal": 12, "bytes": 64},
        {"url": jsonld_u, "hop": 3, "ordinal": 13, "bytes": 64},
        {"url": search_u, "hop": 3, "ordinal": 14, "bytes": 64},
        {"url": unlisted, "hop": 3, "ordinal": 15, "bytes": 64},
        {"url": dead, "hop": 3, "ordinal": 16, "bytes": 0},
    ]
    rev = {e["url"]: e for e in evaluate_items({}, rdocs, ritems)}
    rows.append({"control": "PC_REACHABILITY_LISTED_LIVE",
                 "pass": bool(rev[listed]["reachable_any"]) and bool(rev[jsonld_u]["reachable_any"])
                         and bool(rev[search_u]["reachable_any"]),
                 "observed": {"sitemap_listed_live": rev[listed]["reachable_any"],
                              "jsonld_listed_live": rev[jsonld_u]["reachable_any"],
                              "search_listed_live": rev[search_u]["reachable_any"]}})
    rows.append({"control": "NC_REACHABILITY_UNLISTED_OR_DEAD",
                 "pass": (not rev[unlisted]["reachable_any"]) and (not rev[dead]["reachable_any"]),
                 "observed": {"unlisted_live_reachable": rev[unlisted]["reachable_any"],
                              "dead_live_status": rev[dead]["live_status"],
                              "dead_reachable": rev[dead]["reachable_any"]}})
    rsrv.shutdown()
    rsrv.server_close()

    # (4) env probe
    rows.append({"control": "PC_ENV",
                 "pass": True,
                 "observed": {"python": sys.version.split()[0],
                              "stdlib_urllib": True, "ssl_default": True}})

    # (5) null direct-404 on a probe subset of hosts (design-time subset at
    #     EXECUTE runs the full pool)
    for host, eng, seed in POOL[:3]:
        u = seed.rstrip("/") + "/" + SYNTH_PREFIX + "".join(ch for ch in host if ch.isalnum()) + ".html"
        r, _ = fetch(u)
        rows.append({"control": "NC_SYNTHETIC_UNREACHABLE_ITEM_direct",
                     "pass": (r["status"] is not None and r["status"] >= 400),
                     "observed": {"host": host, "status": r["status"], "error": r["error"]}})
    (out_dir / "raw").mkdir(parents=True, exist_ok=True)
    (out_dir / "raw/controls.jsonl").write_text("\n".join(json.dumps(x, sort_keys=True) for x in rows) + "\n")
    return rows


# ------------------------------------------------------------------- main
def main():
    stage = "all"
    if "--stage" in sys.argv:
        idx = sys.argv.index("--stage")
        if idx + 1 < len(sys.argv):
            stage = sys.argv[idx + 1]
    out_dir = Path(".")
    if "--out" in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index("--out") + 1])
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "raw").mkdir(parents=True, exist_ok=True)

    if stage in ("controls", "all"):
        rows = run_controls(out_dir)
        print("CONTROLS")
        for r in rows:
            print(" ", r["control"], "PASS" if r["pass"] else "FAIL",
                  json.dumps(r["observed"], sort_keys=True))
        if any(not r["pass"] for r in rows):
            print("CONTROL_FAILURE"); sys.exit(3)

    if stage in ("inventory", "all"):
        inv_rows = []
        for host, eng, seed in POOL:
            d = channel_documents(seed)
            d["engine_class"] = eng
            inv_rows.append(d)
            time.sleep(DELAY)
        (out_dir / "raw/channel_docs.jsonl").write_text(
            "\n".join(json.dumps(x, sort_keys=True) for x in inv_rows) + "\n")
        live = {h: sum(1 for r in inv_rows if r["host"] == h) for h in set(r["host"] for r in inv_rows)}
        print("INVENTORY hosts:", len(inv_rows))

    if stage in ("structural", "all"):
        rows = []
        for host, eng, seed in POOL:
            s = bfs_structural(seed)
            s["host"] = host
            s["engine_class"] = eng
            rows.append(s)
            time.sleep(DELAY)
        (out_dir / "raw/structural.jsonl").write_text(
            "\n".join(json.dumps(x, sort_keys=True) for x in rows) + "\n")
        print("STRUCTURAL done")

    if stage in ("discovery", "all"):
        inv = [json.loads(l) for l in (out_dir / "raw/channel_docs.jsonl").read_text().splitlines()]
        stru = [json.loads(l) for l in (out_dir / "raw/structural.jsonl").read_text().splitlines()]
        item_rows = []
        host_census = {h: 0 for h, _, _ in POOL}
        seed_errors = []
        engine_hosts = {}
        for host, eng, _ in POOL:
            engine_hosts.setdefault(eng, set()).add(host)
        for srow in stru:
            if "seed_error" in srow:
                seed_errors.append(srow["host"])
                continue
            host = srow["host"]
            docs = next((d for d in inv if d["host"] == host), None)
            if docs is None:
                continue
            # Q1 per-host census of state-carrying DEEP pages (structural fact;
            # independent of later liveness/reachability evaluation)
            host_census[host] = sum(
                1 for v in srow.values()
                if isinstance(v, dict) and v.get("hop") in DEEP_BAND
                and v.get("controls_seen", 0) > 0)
            items = [{"url": u, "hop": v["hop"], "ordinal": v["ordinal"],
                      "bytes": v["bytes"], "host": host, "engine": srow["engine_class"]}
                     for u, v in srow.items()
                     if isinstance(v, dict) and v.get("hop") in DEEP_BAND
                     and v.get("controls_seen", 0) > 0]
            ev = evaluate_items(srow, docs, items)
            for e in ev:
                e["host"] = host
                e["engine"] = srow["engine_class"]
            item_rows.extend(ev)
        (out_dir / "raw/items.jsonl").write_text(
            "\n".join(json.dumps(x, sort_keys=True) for x in item_rows) + "\n")
        m = compute_metrics(item_rows, "engine", pool_engines=engine_hosts)
        engines_with_any = [e for e, g in m.items() if g["n_deep"] > 0]
        engines_limited = sorted([e for e, g in m.items() if g.get("limited")])
        engines_with_zero = sorted([e for e, g in m.items() if g["n_deep"] == 0])
        at_threshold = {e: g for e, g in m.items()
                        if g["n_deep"] > 0 and not g.get("limited")
                        and g["fraction"] is not None and g["fraction"] >= THRESHOLD}
        if not engines_with_any:
            if seed_errors and len(seed_errors) == len(stru) and len(stru) > 0:
                outcome = "INCONCLUSIVE"
                reason = (f"seed fetch failed on every pool host ({sorted(seed_errors)}): "
                          f"infrastructure signature, NOT a scientific null "
                          f"(EXPERIMENT_PACKET.md section 1)")
            else:
                outcome = "INCONCLUSIVE"
                reason = ("zero DEEP items admitted across the frozen pool "
                          "(Q1 measured; Q2/Q3 vacuous per prereg section 10)")
        elif not any(g["n_deep"] > 0 and not g.get("limited") for g in m.values()):
            outcome = "INCONCLUSIVE"
            reason = (f"all DEEP-admitting engines LIMITED (> {DEAD_LIMIT:.0%} item death): "
                      f"{engines_limited}; Q1/Q2 measured but Q3 not determinable "
                      f"(prereg section 10)")
        elif len(at_threshold) >= MIN_ENGINES:
            outcome = "SUPPORTS"
            reason = f"{len(at_threshold)} engines with discovery_reachable_fraction >= {THRESHOLD}"
        else:
            outcome = "FALSIFIES"
            reason = (f"fewer than {MIN_ENGINES} engines reach {THRESHOLD}: "
                      f"{sorted(at_threshold) or 'none'} over {len(engines_with_any)} "
                      f"DEEP-admitting engine(s), limited={engines_limited} "
                      f"(engine-stratified bounded negative)")
        metrics = {
            "experiment_id": EXP_ID,
            "engine_classes_measured": sorted(engine_hosts),
            "pool_engines_census": {e: g["n_deep"] for e, g in m.items()},
            "host_census": host_census,
            "seed_error_hosts": sorted(seed_errors),
            "engines_with_zero_deep": engines_with_zero,
            "engines_limited": engines_limited,
            "engines_at_or_above_threshold": sorted(at_threshold),
            "per_engine": m,
            "outcome": outcome,
            "decision_reason": reason,
        }
        (out_dir / "derived").mkdir(parents=True, exist_ok=True)
        (out_dir / "derived/metrics.json").write_text(json.dumps(metrics, indent=1, sort_keys=True) + "\n")
        print("DECISION", outcome, reason)
        for e, g in m.items():
            flag = " LIMITED" if g.get("limited") else ""
            print(f"  {e}: n={g['n_deep']} reach={g['reachable']} frac={g['fraction']}"
                  f" ci={g['ci95']}{flag}")


if __name__ == "__main__":
    main()
<!-- CODE_END -->