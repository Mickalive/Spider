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
are hashed by the deterministic freezer, together with `request.json` and `design_review.json`.

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
(`EXP-FRONTIER-37984242167`) committed an empty sampling frame (frozen `seeds=[]`,
`confirmed_deep_items=[]`, `confirmed_deep_hosts=[]`), an absent pre-freeze certificate and a
0/0 primary metric unreachable in both falsifier directions. That was a design/control-plane
defect, not a scientific result. This v2 design repairs it by certifying a non-empty DEEP frame
**live, before** freeze.

---

## 2. Hypotheses

- **H1 (DISCOVERY_COLLAPSES_DEPTH):** on `>= 2` distinct host engines, `>= 0.50` of admitted DEEP
  state items are reachable in `<= K = 3` GETs via at least one frozen discovery channel, so
  shortest-path hop is not a fundamental acquisition-cost barrier.
- **H0 (DEPTH_REMAINS_BARRIER):** on fewer than 2 engines does the per-engine reachable fraction
  reach `0.50`, so fresh deep-instance acquisition remains path-bound and persistence has a
  depth-dependent amortization surface.

The experiment does not presuppose which holds. `E` (defined in §9) is **not** fixed by the
frozen frame: no per-item or per-engine reachability witness exists anywhere in this packet, and
the per-engine fractions are measured only at EXECUTE.

---

## 3. Substrate & Operational Definitions (frozen)

| Element | Frozen value |
|---|---|
| Protocol | HTTP GET only, Python stdlib `urllib`; TLS verified |
| User-Agent | `SPIDER-research-frontier-38013774272/1.0` |
| Timeout / max body | 12 s / 600000 bytes (12000000-byte cap for searchindex.js/sitemap artifacts) |
| Redirects | followed; each 3xx counts as 1 GET toward K |
| Forbidden | browser, Docker, model key, credentials, cookies, write verbs, executed JS |
| Graph (hop) | same-host static `<a href>`, document order; asset extensions excluded; JS links are not edges |
| BFS policy | budget B = 250 GETs, depth cap D = 6, each URL fetched at most once |
| Hop 0 | the seed root |
| `state_carrying_item` | fetched page with at least one named `<input>`/`<select>` (parent definition) |
| `DEEP` | hop in `{3,4,5,6}` |
| Item URL form | engine-native serving form, stored in `spec.json#target_pool.admitted_items`; fetched as-is (`.html` on `doc.rust-lang.org`; extensionless elsewhere) |
| Canonical match key | final URL after redirects; fragment, query, trailing slash and terminal `.html`/`.htm` removed; applied identically to item URLs and channel outputs |
| K | 3 GETs per item per channel (fresh episode; no cross-item caching) |

---

## 4. Frozen Sampling Frame (certified live at DESIGN)

Frame gate **ADMISSION_GATE_V2**: `>= 10` admitted DEEP state items total, `>= 2` engines, `>= 3`
per engine. **Passed with 40 items on 4 engines (10 each).** Every admitted URL was re-fetched on
2026-10-10 (certificate issue) and again at the latest DESIGN re-run (2026-10-10T13:36:59Z) and
returned final 2xx with the frozen `named_controls` value (0 mismatches across all 40).

| Seed root | Host (engine) | Generator | Index kind (measured liveness) | Control-bearing DEEP (total) | Admitted |
|---|---|---|---|---|---|
| `https://vitepress.dev/` | `vitepress.dev` | VitePress | page-level content sitemap (robots->272, `/sitemap.xml`->272, subtree-covered) | 10 | 10 |
| `https://nix.dev/manual/nix/2.34/` | `nix.dev` | mdBook (Nix manual subtree) | sitemap 58 locs, **0** under `/manual/`; **static `searchindex.js` present (1933 `doc_urls`)** | 169 | 10 |
| `https://doc.rust-lang.org/book/` | `doc.rust-lang.org` | mdBook | robots->`sitemap.txt` with exactly 3 version roots; `/sitemap.xml` 404; **no search index** | 12 | 10 |
| `https://rust-lang.github.io/async-book/` | `rust-lang.github.io` | mdBook (GitHub Pages) | **no** robots, **no** sitemap (404), **no** search index (404), no feed, no JSON-LD | 104 | 10 |

**Sampling rule (frozen):** run the frozen BFS once per seed; admit text/html pages at hop in
`{3,4,5,6}` with `>=1` named control; within an engine admit up to **10 items in BFS fetch order
(first-10 rule)**. The exact **40** admitted URLs (engine-native serving form, hop and
named-control count) are frozen in `spec.json#target_pool.admitted_items`. `engine` = distinct
host. All 40 admitted items are at hop 3 — the shallow member of the DEEP band — so the realized
generalization is bounded to the admitted subset; hop-4 control-bearing pages exist in the
`nix.dev` and `rust-lang.github.io` crawls but are not admitted by the ≤10-per-engine roster
(disclosed, not hidden).

**v1 frame defects repaired here:**
1. The frozen v1 pool was **empty** (0 seeds, 0 DEEP items, 0 hosts) — the v2 frame is derived
   by an actual DESIGN-time crawl and certified live.
2. Two candidate hosts named in v1 DESIGN reconnaissance as risky composition (second
   page-level-sitemap candidate `htmx.org`; unreachable `www.gnu.org`, OSError 101) are **not**
   in this pool. The pool has exactly ONE page-level-sitemap engine and ONE static-search-index
   engine without content-sitemap subtree coverage, so `E >= 2` is not guaranteed by a second
   trivially-covering engine.
3. The v1-era per-item reachability witness control (`PC_KNOWN_DEEP_ITEM_WITNESS_BOUNDED`) is
   removed: it pre-computed which engines cross the threshold and made `E` foregone.

**Alternative roots surveyed at DESIGN (reconnaissance record, 2026-10-10; where re-probed at
this re-run, values matched):** `php.net` (`/search-index.json` 404 at the probed path, no
URL-enumerating static index found); `angular.dev` (1624 English sitemap locs but only 2
control-bearing DEEP items at B=250/D=6 recon); `nuxt.com` (DEEP items fully sitemap-covered at
recon → would make `E>=2` foregone); `book.async.rs` (searchindex present but 0 DEEP control-
bearing items); `rust-lang.github.io/mdBook` and `nixos.org/manual/nixpkgs` (searchindex.js 404
at probed paths); `www.11ty.dev` (`/feed/feed.xml` and `/sitemap.xml` 404 at probed paths; recon
found DEEP `/authors/*` items absent from any discoverable feed/sitemap). These counts are
frame-gate or foregone-ness facts, not outcomes of this experiment.

---

## 5. Discovery Channels (frozen definitions)

1. **`ROBOTS_SITEMAP`** — GET `/robots.txt`; extract `Sitemap:` directives; GET each sitemap
   (gzip-decoded if `.gz`); recurse sitemap indexes (cap 12 children, cap 20000 URLs/host); union
   `<loc>` and plain-text URLs; match the item's canonical match key. (Measured: 200 on
   `vitepress.dev`/`nix.dev`/`doc.rust-lang.org`; 404 on `rust-lang.github.io`.)
2. **`SITEMAP_XML`** — GET `/sitemap.xml` and `/sitemap_index.xml` directly (same recursion/gzip
   rules). (Measured: 272 on `vitepress.dev`, 58 on `nix.dev`, **404 on `doc.rust-lang.org`
   and `rust-lang.github.io`**.)
3. **`ON_SITE_SEARCH`** — two sub-mechanisms, no JS execution:
   (a) **static form branch:** on the seed root locate a static `<form>` with an **explicit
   `action` attribute** and a named search-like input; construct `action?param=<last path
   segment>`; GET results. Forms **without** an explicit action (measured: the mdBook
   `searchbar-outer` forms on all three mdBook seeds) are not invoked and yield zero output.
   (b) **static index branch:** probe well-known static search-index artifacts referenced from or
   well-known relative to the seed root and parse them as text: JSON indexes
   (`/search/search_index.json`, `/search-index.json`, `/search.json`,
   `/pagefind/pagefind-entry.json`, `/hashmap.json`) and JS-wrapped static index-data files whose
   payload is a literal JSON object/array — notably mdBook `/searchindex.js` (`doc_urls` array).
   `doc_urls` entries are resolved against the artifact directory before canonicalization.
   (Measured: `nix.dev` `searchindex.js` → 1933 `doc_urls`; `vitepress.dev/hashmap.json` present
   but its 282 keys are `.md`-relative ids, **not URLs**, hence zero URL entries under the match
   rule.) No executed JS or remote query endpoint (API search, Algolia, pagefind JS loader) is
   invoked.
4. **`RSS_ATOM`** — find `<link rel=alternate type=application/rss+xml|application/atom+xml>` on
   the root; GET the feed; match `<item><link>`, `<entry><link href>`, `<guid>`. (Measured: zero
   feed alternate links on all four seed roots.)
5. **`JSON_LD`** — GET the **seed root as a discovery hub** and enumerate same-host URLs from all
   `<script type="application/ld+json">` blocks. **Anti-tautology:** the item page is never used
   as its own JSON-LD hub; a self-fetch implementation is rejected. (Measured: zero `ld+json`
   blocks on all four seed roots.)

**Channel success:** the item's canonical match key is discovered from that channel's output
**and** the item page returns a final 2xx within the remaining K budget. **Union:** an item is
`item_reachable_via_discovery` iff any channel succeeds; channels are probed independently in
fresh episodes (no cross-item caching).

---

## 6. Measurement Procedure (EXECUTE)

1. Re-run the frozen BFS once per seed; record `hop_depth` and `bfs_requests_to_first_reach` for
   each **frozen** admitted item (`B_LINK_FOLLOWING_BFS`). If a frozen URL no longer resolves,
   exclude it with a recorded reason and report the exclusion (temporal drift, VN-V11).
2. For each frozen admitted item, probe each of the 5 channels independently in a fresh K=3
   episode; record `channel_success`, `channel_GETs_used`, `channel_bytes`, `discovered_via`.
3. Re-run the positive control (aggregate channel liveness) and the synthetic null control live;
   any control failure forces `status=MEASUREMENT_INVALID` and no branch is scored. (There is
   deliberately **no** per-item reachability witness at DESIGN; the per-engine fractions are the
   confirmatory measurement and are computed only here.)
4. Aggregate per item, per engine, per channel and union; apply the decision rule (§9).

---

## 7. Metrics (stable identifiers)

| Metric ID | Definition | Unit |
|---|---|---|
| `discovery_reachable_fraction` | reachable admitted items / admitted items | [0,1] |
| `discovery_reachable_fraction_per_engine[host]` | same, per host engine | [0,1] |
| `discovery_reachable_fraction_per_channel[channel]` | reachable via that channel alone | [0,1] |
| `channels_with_zero_deep[channel]` | channel yielded 0 admitted DEEP items | bool |
| `item_reachable_via_discovery[item]` | OR of channel success over the 5 channels | bool |
| `median_discovery_GETs_reachable` | median `channel_GETs_used` over reachable items | GETs |
| `median_discovery_bytes_reachable` | median `channel_bytes` over reachable items | bytes |
| `hop_depth_distribution` | confirmed hop depths of admitted items | counts |
| `bfs_requests_to_first_reach[item]` | baseline BFS GETs to first fetch the item | GETs |
| `null_control_false_positive_rate[channel]` | fabricated reachability for synthetics | [0,1] |

---

## 8. Controls & Baselines (stable identifiers)

| ID | Kind | Expected / pass |
|---|---|---|
| `PC_DISCOVERY_CHANNEL_LIVENESS` | positive (instrument, aggregate) | `>= 1` channel returns a non-empty parsable same-host URL set on `>= 1` host (verified live: `ROBOTS_SITEMAP`/`SITEMAP_XML` non-empty on `vitepress.dev`/`nix.dev`, `ROBOTS_SITEMAP` non-empty on `doc.rust-lang.org` via robots->`sitemap.txt`, `ON_SITE_SEARCH` non-empty on `nix.dev` (1933 `doc_urls`); `rust-lang.github.io` returns zero from every channel) |
| `NC_SYNTHETIC_UNREACHABLE_ITEM` | null | 0 synthetic URLs discovered in every parsed URL set AND 404 on every synthetic page (re-verified live: 8/8 pages 404, 0/8 ids present) |
| `NC_SYNTHETIC_SITEMAP_ABSENCE` | null sub-control | synthetic ids absent from every parsed sitemap/search-index set on every host (verified) |
| `NC_SYNTHETIC_PAGE_404` | null sub-control | every synthetic item page returns HTTP 404 (verified: 8/8) |
| `B_LINK_FOLLOWING_BFS` | baseline | `bfs_requests_to_first_reach` and `hop` recomputed on the frozen items under the frozen policy |
| `B_DIRECT_URL_REPLAY` | baseline | `1` GET |
| `B_PERSISTED_PATH_REACQUISITION_CONTEXT` | inherited context | `hop+1`, analytically defined, **not** paired with the discovery metric |

**Removed control (v1 defect):** `PC_KNOWN_DEEP_ITEM_WITNESS_BOUNDED`, a per-item/engine
reachability witness, is **deliberately removed**. It pre-computed which engines cross the
threshold and therefore made `E` foregone. The positive control is now **aggregate instrument
liveness only** and reports no per-engine or per-item reachability. The confirmatory per-engine
fractions are measured only at EXECUTE.

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
listed explicitly. If `PC_DISCOVERY_CHANNEL_LIVENESS` fails at EXECUTE or either null sub-control
fires, the run is `MEASUREMENT_INVALID` and no branch is scored.

**Why both branches are live on the frozen frame (assignment-space argument):** the frozen record
contains no per-item reachability witness; E is determined at EXECUTE by live channel outputs
under the frozen parsers. SUPPORTS requires the `vitepress.dev` page-level sitemap channel AND the
`nix.dev` static search-index channel to enumerate their frozen items; MIXED requires exactly one
of those conjunctions to fail (e.g., static-index parser/canonicalization mismatch, `doc_urls`
coverage gaps, redirect/availability drift); FALSIFIES requires both to fail (e.g., robots/
sitemap blocking or re-organization). No frozen fact rules out any of the three outcomes.

---

## 10. Measurement Validity Threats (disclosed)

| ID | Threat | Mitigation / disclosure |
|---|---|---|
| VN-V1 | Static GET substrate only | Declared scope; no browser/JS/auth |
| VN-V2 | JS-rendered navigation/search missed | Stdlib parser only; static JS-wrapped index **data** parsed as text (no execution); disclosed as representation loss |
| VN-V3 | Same-host graph only | Bounds claim to same-host acquisition |
| VN-V4 | Frame drift between DESIGN and EXECUTE | Frozen URL list measured as-is; exclusions recorded; frame re-certified live 2026-10-10 (40/40 final 2xx) |
| VN-V5 | Selection bias | Purposive documentation-engine pool, not a random Web sample; claim conditional on admitted engines |
| VN-V6 | Channel overlap (robots -> sitemap) | Disclosed; union counts each item once |
| VN-V7 | No token/latency/$ cost | Only GETs and bytes are cost bases; tokens = null |
| VN-V8 | sitemapindex recursion / `.gz` / big index | Capped recursion and gzip decoding frozen in §5; searchindex.js body cap 12 MB (measured 8.6 MB on `nix.dev`) |
| VN-V9 | **Bimodality / reduced dynamic range** | Measured: per-engine discovery is near-deterministic in whether the engine publishes a machine-readable content index (page-level sitemap or static search index), so per-engine fractions tend to cluster at ~1.0 or ~0.0. The pool is composed as exactly one page-level engine + one static-index engine + two index-less engines to keep `E` at risk. Known cost: reduced power to observe intermediate fractions; ex-ante expectation E in {1,2}, with all discriminating risk concentrated on the single non-trivial mechanism (the `nix.dev` static search index). This is the central validity threat and is stated, not hidden. |
| VN-V10 | Canonicalization choice (`.html` stripping) | Frozen rule in §3; applied identically to channel outputs and items; required so mdBook search-index `.html` entries can match items, and extensionless items match `.html` entries |
| VN-V11 | Cross-subtree / cross-project items | `doc.rust-lang.org` seed reaches `/cargo/` and root at hop 3, and `rust-lang.github.io` seed reaches `/rfcs/` and `/wg-async/` via the shared top navigation; retained as legitimate same-host DEEP items and disclosed |
| VN-V12 | Redirect accounting | Each redirect = 1 GET; final 2xx = 1 GET (e.g., `nix.dev .../development` -> `.../development/`) |
| VN-V13 | Host availability at EXECUTE | Unreachable host is recorded unavailable and excluded from `E`; network failure is never a scientific negative |
| VN-V14 | Item URL serving forms | Items stored in engine-native forms (`.html` on `doc.rust-lang.org`; extensionless elsewhere) and fetched as-is; matching uses the canonical match key so form differences cannot alter reachability assignments |

---

## 11. Product Consequences

**If SUPPORTS (E >= 2):** shortest-path hop is not a fundamental acquisition-cost barrier where a
machine-readable content index (content sitemap or static search index) exists; persistent path
caches are not the primary optimization target for SPIDER memory; effort shifts to
discovery-channel coverage, engine/index-artifact detection, hybrid discovery+traversal for
uncovered engines, and substrate expansion. `C-RESIDUAL-NOVELTY`'s "pay for novelty, not the whole
task" thesis is supported for the acquisition phase when such an index is available. The
two index-less engines certify the boundary of that claim.

**If FALSIFIES/MIXED (E < 2):** even with the full frozen site-native discovery toolkit, fresh
deep-instance acquisition remains path-bound on a material share of engines (the two measured
index-less engines exert the floor); persistence of paths/procedures retains a real
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
  frame, and no per-item witness exists); discovery works on all engines (measured: two engines
  return zero from every channel); agent priors / Scout brief / portfolio assessment are SPIDER
  evidence; parent baselines are measurements of this experiment.

---

## 13. Pre-Freeze Control Certificate (live, before `freeze.json`)

Recorded inline in `spec.json#pre_freeze_control_certificate` (re-issued and re-verified
2026-10-10T12:45:00Z by this DESIGN re-run):

**Frame re-certification at the latest DESIGN re-run (2026-10-10T13:36:59Z):** the 4 seed roots
and all **40/40** frozen admitted item URLs were re-fetched live; every item returned a final 2xx
with the recorded `named_controls` (**0 mismatches**); one item (`nix.dev .../development`) redirects
to its trailing-slash form (disclosed, VN-V12); aggregate channel facts and the 8/8 synthetic 404
null reproduced exactly. Raw aggregate values are in
`spec.json#pre_freeze_control_certificate.frame_admission_recheck` and `.design_probe_evidence`.

1. **Pool frame gate PASS:** 40 admitted DEEP state items across 4 reachable host engines
   (`vitepress.dev` 10, `nix.dev` 10, `doc.rust-lang.org` 10, `rust-lang.github.io` 10); every
   admitted URL re-fetched final 2xx with the frozen named_controls value (0 mismatches).
2. **Channel liveness PASS (aggregate):** non-empty parsable URL sets measured — `vitepress.dev`
   `ROBOTS_SITEMAP`/`SITEMAP_XML` 272/272; `nix.dev` 58/58 plus `ON_SITE_SEARCH` 1933 `doc_urls`;
   `doc.rust-lang.org` robots->`sitemap.txt` 3 lines, `/sitemap.xml` 404; `rust-lang.github.io`
   zero from every channel (404 on robots/sitemap/index probes); feed alternates and `ld+json`
   blocks zero on all four seed roots.
3. **Null control PASS (re-run live):** all 8 synthetic probes (2 per host) absent from every
   parsed URL set and 404 on the item page.

The certificate deliberately does **not** compute any per-item/per-engine reachability witness and
does **not** compute the aggregate `discovery_reachable_fraction`; those are the confirmatory
measurement. Channel URL-set sizes are aggregate instrument facts only.

---

## 14. Freeze-Eligibility Checks (design-contract v2)

| Check | Status | Basis |
|---|---|---|
| `decision_rule_reachability` | PASS | 40-item non-zero denominator (re-certified 200/40); all three outcome assignments live on the frozen frame by assignment-space argument; pool = 1 page-level + 1 static-index + 2 index-less engines so `E >= 2` is at risk through the non-trivial mechanism, not foregone by a second covering engine |
| `measurement_prerequisites` | PASS | substrate verified live (4 seeds 2xx); frame gate passes on 4 hosts (10 each); 5 channels fully defined incl. static `.js` index parse and `doc_urls` resolution; channel liveness measured per host; null control re-run; v1 problematic hosts removed/not referenced |
| `baseline_identifiability` | PASS | `B_LINK_FOLLOWING_BFS` (hop, requests-to-first-reach) recomputable on the same frozen items under the same frozen policy; `B_DIRECT_URL_REPLAY` = 1 by construction; context baseline labeled inherited, never paired |
| `control_sensitivity` | PASS | null fires on false accepts (8/8 synthetic 404, 0/8 in URL sets); positive instrument-liveness fires on parser/channel breakage at EXECUTE; channel set is discriminative on the pool (0 on two hosts vs 272/58/1933 on the others); per-item witness removed so controls cannot pre-prove `E` |
| `treatment_liveness` | PASS | discovery probing executed live on the final pool (robots/sitemap/searchindex/hashmap/feed/json-ld scans, form action-attribute characterization); no treatment arm structurally incapable of being executable |
| `freeze_artifacts_bound` | NOT_APPLICABLE | no separate mutable local artifact exists; the full frame (all 40 URLs), live certificate and probe evidence are inline in `spec.json`, and the decision rule is in `spec.json`/`prereg.md`, all hashed by the freezer (`freeze_artifacts = []`). The parent-handoff dependency asking that "pool/crawl/certificate artifacts" be hashed is satisfied by construction (they are fields of the hashed `spec.json`), not by a separate file; `research/EXPERIMENT_PACKET.md` §2 (lines 50-51) requires `NOT_APPLICABLE` + empty list exactly in this case. EXECUTE's own code/logs are result artifacts, not DESIGN-time mutable dependencies |

---

## 15. Resolved DESIGN Decisions (frozen)

1. **Seed list / frame:** §4 (exact 40 URLs in `spec.json#target_pool.admitted_items`).
2. **`state_carrying_item`:** parent definition (named `<input>`/`<select>`).
3. **DEEP band:** hop `{3,4,5,6}`; all admitted items realized at hop 3 (disclosed).
4. **Engine definition:** distinct host.
5. **Sampling rule:** up to 10 control-bearing DEEP items per engine in BFS fetch order
   (first-10 rule).
6. **K accounting:** redirects count; discovery GET + item-page GET within K=3; channels probed
   independently in fresh episodes (no cross-item caching).
7. **sitemap `.gz` / index recursion:** stdlib gzip; cap 12 children / 20000 URLs per host;
   searchindex.js body cap 12 MB.
8. **`ON_SITE_SEARCH`:** (a) static form branch only for forms with an **explicit action
   attribute** (measured: none on the four seeds); (b) static JSON indexes incl. `/hashmap.json`
   and static JS-wrapped index-data files (`searchindex.js` `doc_urls`, resolved against the
   artifact directory); no JS execution, no remote query endpoint.
9. **Canonicalization:** §3 rule (strip fragment/query/trailing slash/terminal `.html`) applied
   identically to items and channel outputs; item fetch uses the engine-native serving form.
10. **`JSON_LD`:** seed-root hub only; per-item self-fetch rejected as tautological.
11. **Synthetic IDs:** `spider-nonexistent-item-38013774` / `spider-fake-deep-item-38013774`,
    recorded in the certificate.
12. **Temporal drift:** frozen URL list measured as-is; exclusions recorded.
13. **No per-item reachability witness:** removed to prevent a foregone outcome; certificate is
    aggregate-only.

---

## 16. Commitment

This preregistration and `spec.json` are frozen upon creation of `freeze.json`. No changes to the
hypothesis, channels, K, threshold, frame, decision rule or metrics are permitted after freeze.
Any post-freeze analysis change renders the confirmatory claim exploratory. The independent
`design_review.json` must PASS before the deterministic freezer runs.

**Next step:** DESIGN REVIEW (`design_review.json`), then `scripts/freeze_experiment.py`.