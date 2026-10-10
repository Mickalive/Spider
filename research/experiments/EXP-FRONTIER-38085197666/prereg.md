# Preregistration — EXP-FRONTIER-38085197666

- **Experiment:** `EXP-FRONTIER-38085197666`
- **Lane:** frontier
- **Design contract:** v2
- **Status:** DESIGN FROZEN PENDING `freeze.json` (independent `design_review.json` required before freeze)
- **Claim(s):** `C-CROSSSITE` — "Reusable mechanisms transfer across website holdout" (registry status HYPOTHESIS)
- **Director mandate:** PIVOT, cycle `38084662468`, `cognitive_reset=true`, target `C-CROSSSITE`
- **Base SHA:** `6b4a1f7b18e84015e1765965081f2a8e97d3ba27`
- **Claim registry SHA256:** `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`
- **Frozen code SHA256 (section 13):** `14c501399721603bab35817c7a5a4ad0f25f84d7bd825633b71ee636cc51d96b`
- **Created:** 2026-10-10

This file and `spec.json` are the frozen design. EXECUTE must reproduce section 13 verbatim and verify its SHA256 before running. No field below may change after `freeze.json` exists.

---

## 0. Relation to prior work

- `EXP-FRONTIER-37984242167` (direct predecessor, this mandate, v1) was **BLOCKED**: empty sampling frame (0 seeds, 0 DEEP items, 0 hosts), an absent pre-freeze control certificate, and a primary metric that was 0/0 so that **both falsifier directions were unreachable**. Its `audit.json` recorded `required_fixes` VN-A1 (populate seed list and run the hop crawl), VN-A2 (verify the three control-certificate conditions with evidence), VN-A3 (resolve the four open design decisions before freeze) and instructed the v2 freeze to bind pool/certificate artifacts. `same_failure_count=8`. This design is the v2 repair; it does not repeat that failure.
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
- The denominator is the number of admitted DEEP pages, `>= 10` by ADMISSION_GATE_V2 (DESIGN observed **267**), so `E` is well-defined and no branch is `0/0`.
- The local stdlib fixtures bracket the threshold from both sides: `CAL_DISCOVERABLE_FIXTURE` yields fraction **1.0** and `CAL_OPAQUE_FIXTURE` yields **0.0** (section 6.4), so the instrument demonstrably can produce values above and below `0.50`.
- The frozen pool is genuinely heterogeneous: two hosts publish machine-readable enumerations (`doc.rust-lang.org`, `docs.pytest.org`) and two do not (`rust-lang.github.io`, `wasm-bindgen.github.io`), so neither `E == 0` nor `E >= 2` is excluded by construction.

## 3. Frozen pool and pre-freeze attainability certificate

### 3.1 Seeds (frozen)

| # | Seed URL | Host | Engine |
|---|----------|------|--------|
| 1 | `https://doc.rust-lang.org/book/` | doc.rust-lang.org | mdBook |
| 2 | `https://doc.rust-lang.org/edition-guide/` | doc.rust-lang.org | mdBook |
| 3 | `https://rust-lang.github.io/rust-clippy/master/` | rust-lang.github.io | mdBook |
| 4 | `https://wasm-bindgen.github.io/wasm-bindgen/` | wasm-bindgen.github.io | mdBook |
| 5 | `https://docs.pytest.org/en/stable/` | docs.pytest.org | Sphinx |

### 3.2 Pool reconstruction policy (frozen, identical at DESIGN and EXECUTE)

Same-host static-`<a href>` BFS from the seed's *final* root, **document order**, `max_depth = 6`, `budget = 250` GETs per seed, browser-like UA `SPIDER-research-frontier-38085197666/1.0`, GET-only, 12 s timeout, body cap 600 000 bytes, redirects followed (one logical GET). The crawl is **item-blind** (topological). An admitted item is a **state-carrying page**: the fetched page contains at least one named `<input>`/`<select>`. `item_id = sha256(host + "|" + page_url)`. A page reachable from multiple seeds is admitted once at its minimum hop and attributed to the winning seed; its host/engine come from the winning seed's final root (VN-V14).

### 3.3 DESIGN-observed pool (RAW EVIDENCE, 2026-10-10)

Per-seed static hop histograms and DEEP counts (from the frozen BFS; `hop` buckets `0..6`):

- `doc.rust-lang.org/book/` — deep pages 12; hist `{0:1, 1:6, 2:29, 3:214}` (crawl capped at 250)
- `doc.rust-lang.org/edition-guide/` — deep pages 79; hist `{0:1, 1:2, 2:99, 3:148}`
- `rust-lang.github.io/rust-clippy/master/` — deep pages 18; hist `{0:1, 1:4, 2:17, 3:8, 4:5, 5:5, 6:5}`
- `wasm-bindgen.github.io/wasm-bindgen/` — deep pages 6; hist `{0:1, 1:4, 2:44, 3:201}`
- `docs.pytest.org/en/stable/` — deep pages 159; hist `{0:1, 1:56, 2:33, 3:63, 4:97}`

**Admitted DEEP pool (derived): 267 state-carrying pages** — mdBook **108**, Sphinx **159**; by host `doc.rust-lang.org` **84**, `rust-lang.github.io` **18**, `wasm-bindgen.github.io` **6**, `docs.pytest.org` **159**.

Representative confirmed DEEP items (hop >= 3):

| page_url | hop | host | engine |
|----------|-----|------|--------|
| `https://doc.rust-lang.org/book/ch09-01-unrecoverable-errors-with-panic.html` | 3 | doc.rust-lang.org | mdBook |
| `https://doc.rust-lang.org/book/ch03-02-data-types.html` | 3 | doc.rust-lang.org | mdBook |
| `https://rust-lang.github.io/rfcs/0001-private-fields.html` | 5 | rust-lang.github.io | mdBook |
| `https://wasm-bindgen.github.io/wasm-bindgen/examples/wasm-in-web-worker.html` | 3 | wasm-bindgen.github.io | mdBook |
| `https://docs.pytest.org/en/latest/backwards-compatibility.html` | 3 | docs.pytest.org | Sphinx |

Pool-build cost at DESIGN: `<= 5 x 250 = 1250` GETs, observed wall time ~62 s.

### 3.4 ADMISSION_GATE_V2 (frozen)

PASS iff **total admitted DEEP pages >= 10** AND **>= 2 distinct engines each with >= 3 admitted DEEP pages** AND **>= 2 distinct hosts each with >= 3 admitted DEEP pages**. DESIGN verdict: **PASS** (267 >= 10; mdBook 108, Sphinx 159; 4 hosts >= 3). At EXECUTE the gate is re-evaluated on the reconstructed pool; failure yields `status = MEASUREMENT_INVALID` with the exact shortfall and is **never** encoded as a scientific branch.

### 3.5 Pre-freeze control certificate

```
certificate_id: PRE_FREEZE_CERT_EXP-FRONTIER-38085197666
all_verified: true
(a) pool_deep_items_confirmed: true   -> 267 admitted DEEP pages (mdBook 108, Sphinx 159)
(b) pool_deep_hosts_confirmed: true   -> 4 hosts with >= 3 DEEP; 2 engines with >= 3 DEEP
(c) discovery_channel_probe_verified: true -> ROBOTS_SITEMAP live on doc.rust-lang.org and docs.pytest.org;
                                            SITEMAP_XML live on docs.pytest.org; ON_SITE_SEARCH forms present
(d) null_control_verified: true       -> all 5 channels return 0 reachable on synthetic items
(e) dynamic_range_verified: true      -> CAL_DISCOVERABLE_FIXTURE 1.0 ; CAL_OPAQUE_FIXTURE 0.0
```

This repairs v1 `VN-A1`/`VN-A2`/`VN-A3`: the frame is non-empty and recorded, the three certificate conditions are live-verified with evidence, and the falsifier can trigger in both directions.

## 4. Discovery channels (frozen definitions)

All channels are **cold-start**: the item page is fetched **only after** its URL is discovered, and the item-page GET counts against `K`.

1. **ROBOTS_SITEMAP** — GET `/robots.txt`; for each `Sitemap:` directive GET the target and parse `<loc>` (XML) or one-URL-per-line (plain text, e.g. `doc.rust-lang.org/sitemap.txt`).
2. **SITEMAP_XML** — GET `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml` directly and parse `<loc>`.
3. **ON_SITE_SEARCH** — GET the seed root, locate a server-side search `<form>`/input action; GET `action?name=<query>` where `<query>` = last item-path segment with a trailing `.html|.php|.htm|.asp|.aspx` stripped (parameter = the located input's `name`, default `q`); parse result links. JS-only search indexes (mdBook `searchindex.js`, Sphinx client search) are not server-side and are disclosed as unreachable by this channel.
4. **RSS_ATOM** — GET the seed root, follow a `<link rel="alternate" type="application/rss+xml|atom+xml">`, parse entry links.
5. **JSON_LD** — GET the seed root (a **hub** resource; never the item page), parse every `<script type="application/ld+json">` block and collect values of `url`, `@id`, `mainEntityOfPage`, `contentUrl`, `sameAs` across `@graph`/`ItemList`/`WebPage`/`BreadcrumbList`/`SearchAction`.

`K = 3` total GETs per item per channel = at most `DISCOVERY_GETS_MAX = 2` discovery GETs + exactly 1 item-page GET. A channel succeeds for an item iff the item URL (host+path, normalized) is discovered within the discovery budget **and** the item page returns 2xx within `K`. Sitemap-index recursion beyond 2 discovery GETs does not count. An item is reachable iff **any** channel succeeds; per-channel coverage is reported separately and a zero-yield channel is listed explicitly.

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

- `doc.rust-lang.org/robots.txt` → **200**, contains `Sitemap: https://doc.rust-lang.org/sitemap.txt`; `sitemap.txt` → **200** (plain-text URL list); `/sitemap.xml` → **404**; root **200**, no feed link, search form present.
- `docs.pytest.org/robots.txt` → **200**, contains `Sitemap: https://docs.pytest.org/sitemap.xml`; `sitemap.xml` → **200** with **15** `<loc>`; root **200**, no feed link, search form `search.html` present.
- `rust-lang.github.io/robots.txt` → **404**, no sitemap; root page populated but path `/` **404**.
- `wasm-bindgen.github.io/robots.txt` → **404**, no sitemap; path `/` **404**.

**OBSERVATION.** Two of four pool hosts publish a machine-readable page enumeration; two publish none. **DERIVED.** `ROBOTS_SITEMAP` and `SITEMAP_XML` are live and parsable on at least one pool host; `RSS_ATOM` yields nothing on any seed root; `JSON_LD` yields 0 blocks on all four seed roots. **INTERPRETATION.** The treatment is neither absent nor universal; the cross-host contrast is real, so the decision can land on either side.

### 6.2 Null control (RAW EVIDENCE)

Synthetic items `spider-nonexistent-38085197666-<a|b>.html` probed through all five channels against pool hosts: **all 5 channels return `success=false`, 0 reachable URLs**. `NULL_ALL_ZERO = true`. This guards against false-positive discovery via search suggestions, redirect chains or parser errors.

### 6.3 Positive control (DESIGN prerequisite; confirmatory check at EXECUTE)

- **PC_DISCOVERY_CHANNEL_REACHABILITY(a):** at least one channel returns 200 with parsable entries on >= 1 pool host — satisfied live (section 6.1).
- **PC_DISCOVERY_CHANNEL_REACHABILITY(b):** the frozen BFS must return `found=true, hop=1` for the preregistered true-hop-1 target `https://doc.rust-lang.org/book/ch01-01-installation.html`; verified at EXECUTE.

### 6.4 Dynamic-range calibration (RAW EVIDENCE, local stdlib `http.server` fixtures)

- `CAL_DISCOVERABLE_FIXTURE` (robots.txt + `sitemap.xml` listing deep pages): `discovery_reachable_fraction = 1.0` (via `ROBOTS_SITEMAP` and `SITEMAP_XML`); `n_deep = 2`.
- `CAL_OPAQUE_FIXTURE` (same deep structure, no robots/sitemap/feed/search/JSON-LD): `discovery_reachable_fraction = 0.0`.
- `CALIBRATION_PASS = true`.

**DERIVED.** The instrument produces `1.0` and `0.0`, strictly bracketing the `0.50` decision threshold; the pipeline runs end-to-end with no browser, model, key or credential.

## 7. Metrics (stable ids)

- **Primary:** `discovery_reachable_fraction` (pooled); `discovery_reachable_fraction_per_host[host]` (decision unit); `discovery_reachable_fraction_per_engine[engine]` (descriptive).
- **Secondary:** `discovery_reachable_fraction_per_channel[channel]`; `discovery_reachable_fraction_by_hop[3..6]`; `median_discovery_gets_reachable`; `engines_meeting_threshold` (`E`).
- **Controls metric:** `controls.<id>.pass`.

No tokenizer, latency timer or dollar-cost model; GET count and response-body bytes are the only cost bases (token fields `null`).

## 8. Decision rule (frozen, evaluated in order)

```
Step 0  controls: CAL_DISCOVERABLE_FIXTURE==1.0, CAL_OPAQUE_FIXTURE==0.0,
        PC_HOP_CONFIRMATION found & hop==1, NC_SYNTHETIC_UNREACHABLE_ITEM==0.
        Any failure -> status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE (infra/substrate; not a scientific branch).
Step 1  admission: reconstruct pool from frozen seeds under frozen BFS; ADMISSION_GATE_V2 pass?
        fail -> status=MEASUREMENT_INVALID with exact shortfall.
Step 2  measurement: per admitted DEEP page x 5 channels x 2 sessions, channel success within K=3.
        drop items with inter-session disagreement (VN-V11), report count.
Step 3  compute pooled / per-host / per-engine / per-channel / by-hop fractions; E = #hosts with fraction >= 0.50.
        E >= 2 -> SUPPORTS ; E == 1 -> MIXED ; E == 0 -> FALSIFIES   (status=COMPLETE).
```

A valid scientific negative is `status=COMPLETE` with `outcome=FALSIFIES`, **not** an infrastructure failure.

## 9. Controls (frozen ids)

- `PC_DISCOVERY_CHANNEL_REACHABILITY` — section 6.3.
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
7. **Cross-seed contamination** — two seeds share `doc.rust-lang.org`; dedup by minimum hop and attribution to the winning seed (VN-V14) prevents double counting.
8. **Determinism** — 2 sessions; any inter-session disagreement excludes the item with a recorded reason (VN-V11).
9. **Confirmation bias against the question** — the two local fixtures bracket the threshold and the cross-host channel liveness is heterogeneous, so the instrument is not rigged to a single answer; the design explicitly records consequences for both branches.

## 11. Inherited state (from the parent handoff, preserved)

**Established.** (i) A depth-bounded credential-free static crawler can build the pool from these docs roots under B=250/D=6. (ii) The grandparent measured `RECOVERY_REDUCTION_FROM_PERSISTED_STATE = GROWING` (`R_req=5.2667`, `R_bytes=7.3113`) on a single-host DEEP partition.

**Rejected / retired.** (i) The v1 `EXP-FRONTIER-37984242167` sampling frame is void (0 seeds, 0 DEEP, 0 hosts). (ii) Its "no freeze / placeholder spec" design path is retired by this v2.

**Unknown.** (i) The discovery-reachability fraction of DEEP pages on a genuinely multi-host/multi-engine pool — the entire question of this experiment. (ii) Whether discovery reachability scales with hop. (iii) Per-channel coverage on mdBook vs Sphinx.

**Do not assume.** (i) That a single-host result generalizes cross-host. (ii) That a machine-readable discovery channel exists on any given host (two of four lack one). (iii) That `ON_SITE_SEARCH` or `JSON_LD` are live on any pool host — `RSS_ATOM` and `JSON_LD` measured zero at DESIGN.

## 12. Product consequences

- **If SUPPORTS.** Shortest-path hop is not a fundamental acquisition-cost barrier for discovery-enabled acquisition; SPIDER should optimize discovery-channel coverage and substrate expansion rather than path/procedure caching. `C-CROSSSITE` gains a bounded positive that a reusable discovery procedure transfers across `>= 2` host/engine units. Freshness/delta-repair are lower priority for the acquisition phase. **No mechanism is promoted to Product Core by this experiment.**
- **If FALSIFIES.** Even with site-native discovery, fresh deep-instance acquisition remains path-bound; persistence of paths/procedures retains a measurable depth-dependent amortization surface and the break-even reuse count can be computed from the recorded re-derivation cost. SPIDER's memory architecture should keep investing in path/procedure persistence with freshness guards.
- **If MIXED.** No program-level decision change; the next experiment must resolve discovery-channel coverage or pool composition.

## 13. Frozen outcome-bearing code (verbatim; `CODE_SHA256`)

EXECUTE MUST write the following block byte-for-byte to `run.py` (outside the repo is fine) and verify `sha256(run.py) == 14c501399721603bab35817c7a5a4ad0f25f84d7bd825633b71ee636cc51d96b` before running. Extraction rule: the code is the exact bytes between the line after the opening fence and the line before the closing fence (the block content equals the file bytes, trailing newline included). Modes: `python3 run.py --calibrate <OUT>` (controls only), `python3 run.py --pool` (frame reconstruction / admission evidence), `python3 run.py <OUT>` (confirmatory; EXECUTE only).

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

# Frozen seed list (host + generator engine frozen at DESIGN; see prereg s4).
SEEDS = [
    {"seed": "https://doc.rust-lang.org/book/", "host": "doc.rust-lang.org", "engine": "mdBook"},
    {"seed": "https://doc.rust-lang.org/edition-guide/", "host": "doc.rust-lang.org", "engine": "mdBook"},
    {"seed": "https://rust-lang.github.io/rust-clippy/master/", "host": "rust-lang.github.io", "engine": "mdBook"},
    {"seed": "https://wasm-bindgen.github.io/wasm-bindgen/", "host": "wasm-bindgen.github.io", "engine": "mdBook"},
    {"seed": "https://docs.pytest.org/en/stable/", "host": "docs.pytest.org", "engine": "Sphinx"},
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
                               "engine": entry["engine"],
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


def _match(target_key, urls) -> bool:
    return any(url_key(u) == target_key for u in urls)


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
    target = url_key(item_url)
    discovered = _match(target, urls)
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
        "status": "COMPLETE", "outcome": outcome,
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
| `decision_rule_reachability` | PASS — denominator >= 10, `E in {0,1,...}`, both branches arithmetic-reachable, fixtures bracket 0.50 |
| `measurement_prerequisites` | PASS — substrate live, pool builds, channels live, controls run |
| `baseline_identifiability` | PASS — four distinct stable baselines; treatment is a distinct function on the same item set |
| `control_sensitivity` | PASS — all controls two-sided; calibration 1.0/0.0; heterogeneous liveness |
| `treatment_liveness` | PASS — pipeline runs end-to-end (1.0/0.0); two hosts live, two dark |
| `freeze_artifacts_bound` | NOT_APPLICABLE — no mutable local dependency; seeds inlined in `spec.json`, full code hash-bound in section 13; live Web is an external remote resource pinned by seeds + gate |

`spec.json.freeze_artifacts = []`.

## 15. Not authorized

- Re-measuring the grandparent's static re-derivable fraction or its GROWING ratio.
- Returning to the blocked `C-SEMANTIC-RESOLVE` thread.
- Constructing the pool or running any discovery probe after `freeze.json` exists.
- Freezing any design whose falsifier cannot trigger in both directions.
- Promoting any discovery mechanism to Product Core from this experiment.

## 16. Next stage

An **independent** `design_review.json` (separate stage/agent, not this DESIGN task) must PASS before `freeze.json` is written. The reviewer must attack: (a) whether the frozen seed list still reproduces a multi-engine DEEP pool; (b) whether `K = 3` and `0.50` are non-arbitrary (they bracket the measured calibration range and are recorded before outcomes); (c) whether `JSON_LD`/`ON_SITE_SEARCH` are treated as genuinely cold-start; (d) whether `freeze_artifacts_bound = NOT_APPLICABLE` is justified given the inlined seeds + hash-bound code; (e) whether the decision unit (host, with engine descriptive) is faithful to the mandate's "host/engine unit"; (f) whether the null/positive/calibration controls can each fire in both directions.

DESIGN NOT YET FROZEN — awaiting `design_review.json`.
