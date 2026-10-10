# Preregistration: EXP-FRONTIER-38013774272
## Site-Native Discovery vs Link-Following for DEEP State-Item Acquisition (design-contract v2)

**Experiment ID:** EXP-FRONTIER-38013774272
**Lane:** frontier
**Claim IDs:** `C-RESIDUAL-NOVELTY`
**Director mandate:** `request.json#director_mandate` — `action=REOPEN`, target claim `C-RESIDUAL-NOVELTY`
**Design contract version:** 2
**Status:** PREREGISTERED (pre-freeze; `freeze.json` does not yet exist)
**Parent handoff:** `research/experiments/EXP-FRONTIER-37984242167/handoff.json` (sha256 `1b220e4114e490b3fd935b29de14e88fc611b919471483e2243d7dc0281ef6bf`)

This preregistration must be read together with `spec.json`; the frozen sampling frame,
channel definitions and decision rule live in `spec.json` and are summarized here. Both files
are hashed by the deterministic freezer.

---

## 1. Scientific Question

On the credential-free GET-only stdlib-HTTP substrate frozen by `EXP-FRONTIER-37950626378`,
over a frozen 4-engine pool of **DEEP** (shortest-path hop in `{3,4,5,6}`) **state-carrying
items** (a page whose HTML contains at least one named `<input>`/`<select>`), what fraction of
those items is reachable in **<= K = 3 fresh-agent GETs** (1 discovery GET + 1 item-page GET +
1 spare for redirect/validation) via **ANY** of five frozen site-native discovery channels —
`ROBOTS_SITEMAP`, `SITEMAP_XML`, `ON_SITE_SEARCH`, `RSS_ATOM`, `JSON_LD` — with a preregistered
materiality threshold of **0.50 on >= 2 distinct host engines**?

The threshold decides between:

- (**positive**) shortest-path hop is **not** a fundamental acquisition-cost barrier for
  discovery-enabled acquisition, so persistent path/procedure caching is not a core optimization
  target; or
- (**negative**) even with site-native discovery, fresh deep-instance acquisition remains
  **path-bound** and persistence retains a computable, depth-dependent amortization surface.

This directly continues the mandate's v1 question, which was **never measured**: the v1 freeze
(`EXP-FRONTIER-37984242167`) committed an empty sampling frame (0 seeds, 0 DEEP items, 0 hosts),
an absent pre-freeze certificate and a 0/0 primary metric unreachable in both falsifier
directions. That was a design/control-plane defect, not a scientific result. This v2 design
repairs it by certifying a non-empty DEEP frame **before** freeze.

---

## 2. Hypotheses

- **H1 (DISCOVERY_COLLAPSES_DEPTH):** on `>= 2` distinct host engines, `>= 0.50` of admitted DEEP
  state items are reachable in `<= K = 3` GETs via at least one frozen discovery channel, so
  shortest-path hop is not a fundamental acquisition-cost barrier.
- **H0 (DEPTH_REMAINS_BARRIER):** on fewer than 2 engines does the per-engine reachable fraction
  reach `0.50`, so fresh deep-instance acquisition remains path-bound and persistence has a
  depth-dependent amortization surface.

The experiment does not presuppose which holds. `E` (defined in §9) is **not** fixed by the
frozen frame. The pool deliberately contains exactly **one** page-level content-sitemap engine
(`vitepress.dev`), **one** engine that publishes no content sitemap for the seed subtree but
**does** publish a static content search index (`nix.dev`, mdBook `searchindex.js`), and **two**
index-less engines (`doc.rust-lang.org`, `rust-lang.github.io`). The materiality boundary
`E >= 2` is therefore genuinely at risk: it requires the **non-trivial** `ON_SITE_SEARCH`
static-index channel to enumerate the `nix.dev` items **and** the single page-level sitemap to
cover the `vitepress.dev` items. Both `E >= 2` (SUPPORTS) and `E <= 1` (MIXED/FALSIFIES) are live.

---

## 3. Substrate & Operational Definitions (frozen)

| Element | Frozen value |
|---|---|
| Protocol | HTTP GET only, Python stdlib `urllib`; TLS verified |
| User-Agent | `SPIDER-research-frontier-38013774272/1.0` |
| Timeout / max body | 12 s / 600000 bytes |
| Redirects | followed; each 3xx counts as 1 GET toward K |
| Forbidden | browser, Docker, model key, credentials, cookies, write verbs |
| Graph (hop) | same-host static `<a href>`, document order; asset extensions excluded; JS links are not edges |
| BFS policy | budget B = 250 GETs, depth cap D = 6, each URL fetched at most once |
| Hop 0 | the seed root |
| `state_carrying_item` | fetched page with at least one named `<input>`/`<select>` (parent definition) |
| `DEEP` | hop in `{3,4,5,6}` |
| `canonicalization` | final URL after redirects; fragment+query removed; trailing slash removed; terminal `.html`/`.htm` removed from the last path segment (search-index `.html` entries therefore match extensionless item URLs). Channel outputs canonicalized identically before matching |
| K | 3 GETs per item per channel |

---

## 4. Frozen Sampling Frame (certified live at DESIGN)

Frame gate **ADMISSION_GATE_V2**: `>= 10` admitted DEEP state items total, `>= 2` engines, `>= 3`
per engine. **Passed with 40 items on 4 engines (10 each):**

| Seed root | Host (engine) | Generator | Index kind | Control-bearing DEEP (total) | Admitted |
|---|---|---|---|---|---|
| `https://vitepress.dev/` | `vitepress.dev` | VitePress | page-level content sitemap (272 locs) | 10 | 10 |
| `https://nix.dev/manual/nix/2.34/` | `nix.dev` | mdBook (Nix manual subtree) | sitemap excludes seed subtree (58 locs, **0** manual) **+ static `searchindex.js`** | 168 | 10 |
| `https://doc.rust-lang.org/book/` | `doc.rust-lang.org` | mdBook | version-level sitemap only (`sitemap.txt`, 3 locs), **no** search index | 12 | 10 |
| `https://rust-lang.github.io/async-book/` | `rust-lang.github.io` | mdBook (GitHub Pages) | **no** sitemap, **no** search index | 94 | 10 |

**Sampling rule (frozen):** run the frozen BFS once per seed; admit text/html pages at hop in
`{3,4,5,6}` with `>=1` named control; within an engine admit up to **10 items in BFS fetch order**.
The exact **40** admitted URLs (with hop and named-control count) are frozen in
`spec.json#target_pool.admitted_items`. `engine` = distinct host. All admitted items are hop 3 in
the frozen B=250 crawls (the shallow member of the DEEP band), so the realized generalization is
bounded to hop 3 and the claim is stated for the DEEP band as realized; deeper control-bearing
pages exist in the crawls (`nix.dev` hop 4) but are not admitted by the ≤10-per-engine roster.

**v1 frame defects repaired here:**
1. `www.gnu.org` was **unreachable** from the runner (OSError 101, "Network is unreachable") and is
   **removed**. Every seed in this frame returned a 2xx and produced a non-empty BFS at DESIGN.
2. The v1 pool contained **two** page-level-sitemap engines (`vitepress.dev`, `htmx.org`), which
   made `E >= 2` foregone. Exactly **one** page-level engine is retained.
3. The v1 seed/items mismatch (`doc.rust-lang.org` seeded at `/book/` but admitting `/cargo/*`)
   was re-verified as **reproducible** (the shared rust-docs top navigation reaches `/cargo/` at
   hop 3); the cross-subtree origin is disclosed rather than removed.

**Why other candidate roots were rejected (DESIGN reconnaissance):** `php.net` (static
`search-index.json` has no URLs); `angular.dev` (1624 English sitemap locs but only 2
control-bearing DEEP items); `nuxt.com` (all 49 DEEP items covered by sitemap → not challenging);
`book.async.rs` (search index but 0 DEEP items); `doc.rust-lang.org/{nomicon,rustc,reference}`,
`rust-lang.github.io/mdBook`, `nixos.org/manual/nixpkgs` (no search index); `www.11ty.dev/docs`
(854 DEEP items are `/authors/*`, absent from feed and sitemap).

---

## 5. Discovery Channels (frozen definitions)

1. **`ROBOTS_SITEMAP`** — GET `/robots.txt`; extract `Sitemap:` directives; GET each sitemap
   (gzip-decoded if `.gz`); recurse sitemap indexes (cap 12 children, cap 20000 URLs/host); union
   `<loc>` / plain-text URLs; match the item's canonical URL.
2. **`SITEMAP_XML`** — GET `/sitemap.xml` and `/sitemap_index.xml` directly (same recursion/gzip
   rules).
3. **`ON_SITE_SEARCH`** — locate a static `<form>` search action on the seed root and construct
   `action?param=<last path segment>`; additionally probe well-known **static** search-index
   artifacts and parse them **without executing JS**: JSON indexes (`/search/search_index.json`,
   `/search-index.json`, `/search.json`, `/pagefind/pagefind-entry.json`) **and JS-wrapped static
   index-data files whose payload is a literal JSON object/array — notably mdBook `/searchindex.js`
   containing a `doc_urls` array**. This static-`.js` extension is required for two-sidedness: some
   mdBook engines publish no sitemap coverage for the seed subtree and expose their content only
   through this static index, so excluding it would manufacture a floor (a v1 defect). No executed
   JS or remote query endpoint is invoked.
4. **`RSS_ATOM`** — find `<link rel=alternate type=application/rss+xml|application/atom+xml>` on
   the root; GET the feed; match `<item><link>`, `<entry><link href>` and `<guid>`.
5. **`JSON_LD`** — GET the **seed root as a discovery hub** and enumerate same-host URLs from all
   `<script type="application/ld+json">` blocks. **Anti-tautology:** the item page is never used
   as its own JSON-LD hub; a self-fetch implementation is rejected.

**Channel success:** the canonical item URL is discovered from that channel's output **and** the
item page returns a final 2xx within the remaining K budget. **Union:** an item is
`item_reachable_via_discovery` iff any channel succeeds; channels are probed independently in
fresh episodes (no cross-item caching).

---

## 6. Measurement Procedure (EXECUTE)

1. Re-run the frozen BFS per seed; record `hop_depth` and `bfs_requests_to_first_reach` for each
   **frozen** admitted item (`B_LINK_FOLLOWING_BFS`). If a frozen URL no longer resolves, exclude
   it with a recorded reason and report the exclusion (temporal drift, VN-V11).
2. For each frozen admitted item, probe each of the 5 channels independently; record
   `channel_success`, `channel_GETs_used`, `channel_bytes`, `discovered_via`.
3. Re-run the positive control and the synthetic null control; any control failure forces
   `status=MEASUREMENT_INVALID` and no branch is scored. (There is deliberately **no** per-item
   reachability witness; see §8.)
4. Aggregate per item, per engine, per channel and union.

---

## 7. Metrics (stable identifiers)

| Metric ID | Definition | Unit |
|---|---|---|
| `discovery_reachable_fraction` | reachable admitted items / admitted items | [0,1] |
| `discovery_reachable_fraction_per_engine[host]` | same, per host engine | [0,1] |
| `discovery_reachable_fraction_per_channel[channel]` | reachable via that channel alone | [0,1] |
| `channels_with_zero_deep[channel]` | channel yielded 0 admitted DEEP items | bool |
| `median_discovery_GETs_reachable` | median `channel_GETs_used` over reachable items | GETs |
| `median_discovery_bytes_reachable` | median `channel_bytes` over reachable items | bytes |
| `hop_depth_distribution` | confirmed hop depths of admitted items | counts |
| `bfs_requests_to_first_reach[item]` | baseline BFS GETs to first fetch the item | GETs |
| `null_control_false_positive_rate[channel]` | fabricated reachability for synthetics | [0,1] |

---

## 8. Controls & Baselines (stable identifiers)

| ID | Kind | Expected / pass |
|---|---|---|
| `PC_DISCOVERY_CHANNEL_LIVENESS` | positive (instrument, aggregate) | `>= 1` channel returns a non-empty parsable same-host URL set on `>= 1` host (verified live: sitemap channels on all 4 hosts; `ON_SITE_SEARCH` on `nix.dev`) |
| `NC_SYNTHETIC_UNREACHABLE_ITEM` | null | 0 synthetic URLs discovered; 404 on every synthetic page (verified: all 8 probes) |
| `B_LINK_FOLLOWING_BFS` | baseline | `bfs_requests_to_first_reach` and `hop` recomputed on the frozen items |
| `B_DIRECT_URL_REPLAY` | baseline | `1` GET |
| `B_PERSISTED_PATH_REACQUISITION_CONTEXT` | inherited context | `hop+1`, analytically defined, **not** paired with the discovery metric |

**Removed control (v1 defect):** `PC_KNOWN_DEEP_ITEM_WITNESS_BOUNDED`, a per-item/engine
reachability witness, is **deliberately removed**. It pre-computed which engines cross the
threshold and therefore made `E` foregone (a ceiling defect flagged in the v1 design review). The
positive control is now **aggregate instrument liveness only** and reports no per-engine or
per-item reachability. The confirmatory per-engine fractions are measured only at EXECUTE.

---

## 9. Decision Rule (formal, two-sided)

Let `E = |{ engines with discovery_reachable_fraction_per_engine >= 0.50 }|` over engines
available at EXECUTE.

```python
def apply_decision_rule(admission_gate_pass, controls_ok, per_engine):
    if not admission_gate_pass or not controls_ok:
        return "INCONCLUSIVE/MEASUREMENT_INVALID"
    E = sum(1 for f in per_engine.values() if f >= 0.50)
    if E >= 2:  return "SUPPORTS"     # depth not fundamental (materiality boundary met)
    if E == 1:  return "MIXED"        # negative branch (sub-case of E < 2)
    return "FALSIFIES"                # E == 0; depth remains a barrier
```

**Materiality boundary:** the preregistered boundary is `E >= 2`. `SUPPORTS` requires `E >= 2`;
both `MIXED` (`E == 1`) and `FALSIFIES` (`E == 0`) belong to the **negative** branch (depth
remains an acquisition barrier). Frozen parameters: threshold `0.50`, `min_engines = 2`, `K = 3`.
Per-channel coverage is mandatory for all 5 channels; any channel with zero admitted DEEP items is
listed explicitly. If `PC_DISCOVERY_CHANNEL_LIVENESS` fails or either null sub-control fires, the
run is `MEASUREMENT_INVALID` and no branch is scored.

---

## 10. Measurement Validity Threats (disclosed)

| ID | Threat | Mitigation / disclosure |
|---|---|---|
| VN-V1 | Static GET substrate only | Declared scope; no browser/JS/auth |
| VN-V2 | JS-rendered navigation/search missed | Stdlib parser only; static JS-wrapped index **data** parsed as text (no execution); disclosed as representation loss |
| VN-V3 | Same-host graph only | Bounds claim to same-host acquisition |
| VN-V4 | Frame drift between DESIGN and EXECUTE | Frozen URL list measured as-is; exclusions recorded |
| VN-V5 | Selection bias | Purposive documentation-engine pool, not a random Web sample; claim conditional on admitted engines |
| VN-V6 | Channel overlap (robots → sitemap) | Disclosed; union counts each item once |
| VN-V7 | No token/latency/$ cost | Only GETs and bytes are cost bases; tokens = null |
| VN-V8 | sitemapindex recursion / `.gz` | Capped recursion and gzip decoding frozen in §5 |
| VN-V9 | **Bimodality / reduced dynamic range** | Discovery is near-deterministic in whether an engine publishes a machine-readable content index, so per-engine fractions tend to cluster at ~1.0 or ~0.0. The pool is composed as exactly one page-level engine + one static-index engine + two index-less engines to keep `E` at risk. Known cost: reduced power to observe intermediate fractions. This is the central validity threat. |
| VN-V10 | Canonicalization choice (`.html` stripping) | Frozen rule in §3; applied identically to channel outputs and items; required so mdBook search-index `.html` entries can match extensionless item URLs |
| VN-V11 | Cross-subtree / cross-project items | `doc.rust-lang.org` seed reaches `/cargo/` and `rust-lang.github.io` seed reaches `/rfcs/`,`/wg-async/` via shared top navigation; retained as legitimate same-host DEEP items and disclosed |
| VN-V12 | Redirect accounting | Each redirect = 1 GET; final 2xx = 1 GET |
| VN-V13 | Host availability at EXECUTE | Unreachable host is recorded unavailable and excluded from `E`; network failure is never a scientific negative |

---

## 11. Product Consequences

**If SUPPORTS (E >= 2):** shortest-path hop is not a fundamental acquisition-cost barrier where a
machine-readable content index (content sitemap or static search index) exists; persistent path
caches are not the primary optimization target for SPIDER memory; effort shifts to
discovery-channel coverage, engine/index-artifact detection, hybrid discovery+traversal for
uncovered engines, and substrate expansion. `C-RESIDUAL-NOVELTY`'s "pay for novelty, not the whole
task" thesis is supported for the acquisition phase when such an index is available.

**If FALSIFIES/MIXED (E < 2):** even with site-native discovery, fresh deep-instance acquisition
remains path-bound on a material share of engines; persistence of paths/procedures retains a real
depth-dependent amortization surface whose break-even can be computed from measured re-derivation
cost; memory architecture should keep investing in persistence with freshness guards and delta
repair, and Frontier should improve discovery recall or adopt hybrid strategies.

Either outcome changes a program-level architectural decision and is decision-changing.

---

## 12. Inherited State (four-way, from `EXP-FRONTIER-37984242167`)

- **Established:** the discovery question remains entirely unmeasured; the v1 failure was a
  control-plane/empty-frame defect with a known v2 repair; parent `EXP-FRONTIER-37950626378`
  validly measured persisted-path re-acquisition as near-linear (`hop+1`), direct URL replay = 1
  GET, and a GROWING ratio (`R_req=5.27`, `R_bytes=7.31` at `M=3.0`) that is
  construct-validity-bounded by the BFS estimator on a single mdBook host.
- **Rejected:** reading `BLOCKED`/`NOT_APPLICABLE` as a scientific `FALSIFIES`; any post-freeze
  construction of the sampling frame; the parent's single-engine/mdBook DEEP band as a substitute
  for the required multi-engine pool; a per-item reachability witness as a control (it pre-proves
  the outcome).
- **Unknown:** whether `>= 0.50` of DEEP items are reachable in `<= K` GETs via discovery on
  `>= 2` engines (this experiment); whether the maintenance/invalidation axis is the better next
  question.
- **Do not assume:** this DESIGN pre-judges the outcome (the falsifier is two-sided on the frozen
  frame); discovery works on all engines; agent priors / Scout brief / portfolio assessment are
  SPIDER evidence; parent baselines are measurements of this experiment.

---

## 13. Pre-Freeze Control Certificate (live, before `freeze.json`)

Recorded inline in `spec.json#pre_freeze_control_certificate` (verified 2026-10-10T12:02:41Z):

1. **Pool frame gate PASS:** 40 admitted DEEP state items across 4 reachable host engines
   (`vitepress.dev` 10, `nix.dev` 10, `doc.rust-lang.org` 10, `rust-lang.github.io` 10).
2. **Channel liveness PASS (aggregate):** sitemap channels return non-empty parsable URL sets on
   all 4 hosts; `ON_SITE_SEARCH` returns a non-empty URL set on `nix.dev` (mdBook `searchindex.js`).
3. **Null control PASS:** all 8 synthetic probes (2 per host) are absent from the parsed URL sets
   and 404 on the item page.

The certificate deliberately does **not** compute any per-item/per-engine reachability witness and
does **not** compute the aggregate `discovery_reachable_fraction`; those are the confirmatory
measurement.

---

## 14. Freeze-Eligibility Checks (design-contract v2)

| Check | Status | Basis |
|---|---|---|
| `decision_rule_reachability` | PASS | 40-item denominator; pool is 1 page-level + 1 static-index + 2 index-less engines, so `E` is at risk at the `E >= 2` boundary; SUPPORTS/MIXED/FALSIFIES all live |
| `measurement_prerequisites` | PASS | substrate, frame (4 reachable hosts), 5 channels, controls certified live in DESIGN; v1 unreachable `www.gnu.org` removed |
| `baseline_identifiability` | PASS | `B_LINK_FOLLOWING_BFS` and `B_DIRECT_URL_REPLAY` computable on the same frozen items; context baseline labeled inherited |
| `control_sensitivity` | PASS | null fires on false positives; positive instrument-liveness fires on parser/channel failure; per-item witness removed so controls cannot pre-prove `E` |
| `treatment_liveness` | PASS | discovery probing executed live; sitemap channels parsable on all 4 hosts; `ON_SITE_SEARCH` static-index parse works on `nix.dev` |
| `freeze_artifacts_bound` | NOT_APPLICABLE | no separate mutable local artifact exists; the full frame and decision rule are inline in `spec.json`/`prereg.md`, hashed by the freezer (`freeze_artifacts = []`) |

---

## 15. Resolved DESIGN Decisions (frozen)

1. **Seed list / frame:** §4 (exact 40 URLs in `spec.json`).
2. **`state_carrying_item`:** parent definition (named `<input>`/`<select>`).
3. **DEEP band:** hop `{3,4,5,6}`.
4. **Engine definition:** distinct host.
5. **Sampling rule:** up to 10 control-bearing DEEP items per engine in BFS order.
6. **K accounting:** redirects count; discovery GET + item-page GET within K=3.
7. **sitemap `.gz` / index recursion:** stdlib gzip; cap 12 children / 20000 URLs per host.
8. **`ON_SITE_SEARCH`:** static form + well-known static JSON search-index files + static
   JS-wrapped index-data files (`searchindex.js` `doc_urls`); no JS execution, no remote endpoint.
9. **Canonicalization:** §3 rule (strip fragment/query/trailing slash/terminal `.html`).
10. **`JSON_LD`:** seed-root hub only; per-item self-fetch rejected as tautological.
11. **Synthetic IDs:** `spider-nonexistent-item-38013774` / `spider-fake-deep-item-38013774`,
    recorded in the certificate.
12. **Temporal drift:** frozen URL list measured as-is; exclusions recorded.
13. **No per-item reachability witness:** removed to prevent a foregone outcome.

---

## 16. Commitment

This preregistration and `spec.json` are frozen upon creation of `freeze.json`. No changes to the
hypothesis, channels, K, threshold, frame, decision rule or metrics are permitted after freeze.
Any post-freeze analysis change renders the confirmatory claim exploratory. The independent
`design_review.json` must PASS before the deterministic freezer runs.

**Next step:** DESIGN REVIEW (`design_review.json`), then `scripts/freeze_experiment.py`.
