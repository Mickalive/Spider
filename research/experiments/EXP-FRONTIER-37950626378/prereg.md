# EXP-FRONTIER-37950626378 preregistration

Lane: `frontier`. Target claim: `C-RESIDUAL-NOVELTY`. Director cycle: `37949204501`, action `CONTINUE`,
`parent_handoff_disposition = USE`. Parent packet: `EXP-FRONTIER-37385647440` (MEASUREMENT_INVALID; every admitted
item at `max_hop_of_any_admitted_item <= 1`, so the re-acquisition-vs-re-derivation contrast was exercised only in the
extreme-favourable case for persistence).

This experiment does the smallest rigorous thing that can change a C-RESIDUAL-NOVELTY product decision: it measures
whether the *unconditional* cost of obtaining one fresh valid instance of a state-carrying item grows with the item's
shortest-path hop depth. It does not re-measure the static re-derivable fraction, does not reopen the terminated
deterministic-compilation-bypass thread, does not touch the blocked `C-SEMANTIC-RESOLVE` thread, and drops the
five-class stationarity taxonomy entirely (precondition 4).

## Substrate and frozen policy

HTTP GET only via Python stdlib `urllib`; TLS verified; frozen User-Agent
`SPIDER-research-frontier-37950626378/1.0`; timeout 12 s; max body 600000 bytes; redirects followed. No credentials,
cookies, browser, Docker, model key or write verb.

Navigation graph = defragmented same-host http(s) URLs linked by static `<a href>` parsed in document order. Asset
extensions and non-http(s) schemes are excluded. JS-generated links are **not** edges (validity note VN-V2).

Frozen policy = item-blind FIFO breadth-first crawl in document order from the seed root, per-site page budget
`B = 250`, depth cap `D = 6`, each URL fetched at most once. For a per-item re-derivation cost the crawl stops when
the item's page is fetched.

A *state-carrying item* is `(page_url, control_name, control_type)` where the page contains at least one named
`<input name>` or `<select name>`. Bands: `NEAR = hop in {0,1}`, `DEEP = hop in {3..6}`, `hop == 2` is `MID` and is
reported descriptively only (VN-V7). `hop` is the graph shortest-path length from the seed URL (hop 0).

## Target pool

Candidate roots (each crawled with the frozen policy at budget 250): `https://doc.rust-lang.org/book/`,
`https://doc.rust-lang.org/cargo/`, `https://doc.rust-lang.org/nomicon/`, `https://www.gnu.org/`,
`https://quotes.toscrape.com/`, `https://forums.gentoo.org/`. Pre-reconnaissance confirmed named `searchbar` inputs at
hop >= 3 in the mdBook books. Admission gate `ADMISSION_GATE_V1`: keep items with HTTP 200, hop <= 6, >= 1 named
control, and two-session agreement on hop. The gate requires >= 5 admitted DEEP items, >= 8 admitted NEAR items and
>= 2 distinct seed hosts; otherwise `status = MEASUREMENT_INVALID` with the exact shortfall and **no** scientific
branch. The pool is mdBook-dominated; generalization is reported per host and bounded (VN-V8).

## Arms and baselines

- `RED_re_derivation` (comparator): item-blind BFS as above; charges every GET and body byte up to the item page.
- `RACQ_PATH_re_acquisition` (primary re-acquisition): GET the frozen shortest path in hop order; charges `h+1` GETs.
- `RACQ_URL_re_acquisition`: one GET to the item page (absolute lower bound).
- `STRUCTURAL_MINIMUM`: `h+1` GETs and path-page bytes (floor for the ordering proof only).

Primary channel = GET requests (always valid on the stdlib substrate). Co-primary size channel = response-body bytes.
`cl100k_base` tokens are recorded **only** if EXECUTE can `import tiktoken` and records its version; otherwise token
fields are `null` and no token figure is presented as satisfying the cost basis (VN-V1, repairing parent VN-11).

### Baseline-ordering proof (precondition 2, proven before freeze)

`RED.requests >= RACQ_PATH.requests >= RACQ_URL.requests` and the same in bytes, by construction: the BFS fetches a
superset of the shortest-path pages, and `h+1 > 1` for `h >= 1`. Strict `RED > RACQ_PATH` holds whenever the BFS takes
at least one detour before the item page (whether some level `< h` has breadth > 1 or a preceding level-`h` page
exists); it fails only on a detour-free linear chain. Therefore the break-even denominator
`RED.requests - RACQ_PATH.requests` is strictly positive and the accept region is non-empty for every item with a
detour. Pre-freeze witness: the hop-1 positive-control target had `RED.requests = 3 > RACQ_PATH.requests = 2 >
RACQ_URL.requests = 1`; the broad-fanout calibration had `RED.requests(hop3) = 932` vs `RACQ_PATH.requests = 4`.

### Paired medians and break-even guard (precondition 3)

Within each band, `RED`, `RACQ_PATH` and `RACQ_URL` are measured over the **same** admitted item set, so every
break-even is a per-item quantity:

- `break_even_reuse_count_requests = RACQ_PATH.requests / (RED.requests - RACQ_PATH.requests)`
- `break_even_reuse_count_bytes   = RACQ_PATH.bytes    / (RED.bytes    - RACQ_PATH.bytes)`

Eligibility guard: `saving_requests >= 1` **and** `saving_bytes >= 1024`; items failing the guard get
`break_even_reuse_count = null` with the reason recorded, and a band whose eligible count is 0 is not interpreted.
This prevents a tiny denominator from manufacturing a small break-even.

## Falsifier (arithmetically checkable before freeze, satisfiable BOTH ways)

With materiality factor `M = 3.0`:

- `R_req   = median(RED.requests | DEEP) / median(RED.requests | NEAR)`
- `R_bytes = median(RED.bytes    | DEEP) / median(RED.bytes    | NEAR)`
- **FLAT** (falsifies H1): `R_req <= M` and `R_bytes <= M`.
- **GROWING** (supports H1): `R_req > M` and `R_bytes > M`.
- Otherwise **MIXED**: report the per-channel direction and make no O(1) claim.

If either band median is `null` or the admission gate fails, the ratio is undefined and the experiment is
`MEASUREMENT_INVALID`, never a scientific branch.

**Both directions are producible by the frozen instrument**, demonstrated by the two pre-freeze calibration controls:
`NARROW_CHAIN_CALIBRATION` measured `R = 2.0 <= 3.0` (FLAT) and `BROAD_FANOUT_CALIBRATION` measured `R = 466.0 > 3.0`
(GROWING). `M = 3.0` lies strictly between the two live-measured ratios, so the decision boundary is bracketed by
observed behaviour rather than assumed.

## Pre-freeze control certificate (precondition 1; live, before freeze.json)

All four controls were run live by the DESIGN runner on 2026-10-09 under the frozen policy; all four PASS, with
observations recorded inline in `spec.json` and here.

1. `POS_KNOWN_HOP_CONTROL` — seed `https://doc.rust-lang.org/book/`, target
   `https://doc.rust-lang.org/book/ch01-01-installation.html` (a direct same-host `<a href>` on the seed). Observed
   `found = true, hop = 1, requests = 3, cum_bytes = 653222, status = 200`. **PASS.**
2. `NEG_UNREACHABLE_CONTROL` — same seed, target
   `https://doc.rust-lang.org/book/__spider_nonexistent_37950626378__.html`. Observed `found = false`. **PASS.**
3. `NARROW_CHAIN_CALIBRATION` — local stdlib `http.server` 7-page linear chain (index -> p1 -> ... -> p6, each page
   links only to the next). Observed requests `{hop1: 2, hop2: 3, hop3: 4}`, `R = 2.0`. **PASS.**
4. `BROAD_FANOUT_CALIBRATION` — local stdlib `http.server` 30-fanout 4-deep tree. Observed requests
   `{hop1: 2, hop3: 932}`, `R = 466.0`. **PASS.**

EXECUTE must reproduce all four under the frozen policy and persist raw artifacts. If any control fails, or a seed
host is unreachable, the run is `status = MEASUREMENT_INVALID` or `BLOCKED` (with the exact error) — never a
scientific negative.

## Decision rule

Step 0: reproduce the four controls (any failure -> `MEASUREMENT_INVALID`). Step 1: structural pass + admission gate
(failure -> `MEASUREMENT_INVALID` with shortfall). Step 2: measure all three arms per admitted item in `K = 2`
independent sessions. Step 3: compute per-site and pooled ratios with `M = 3.0` and classify FLAT / GROWING / MIXED.
Step 4: report band medians and eligible-item break-even reuse counts. `result.json.outcome` is `SUPPORTS`
(GROWING), `FALSIFIES` (FLAT) or `MIXED`, with `status = COMPLETE`; only genuine measurement invalidity is
`status = MEASUREMENT_INVALID`.

## Consequences

- **If GROWING:** persistence of paths and procedures has a measurable amortization surface; hand the first real
  depth-derived re-derivation cost and break-even reuse count to `C-RESIDUAL-NOVELTY`, `C-FRESHNESS` staleness
  economics and the `C-WEB-DYNAMICS` timescales axis. A bounded successor may then evaluate a path/procedure cache in
  the product kernel under a separate verdict; this experiment promotes no mechanism.
- **If FLAT:** fresh-instance acquisition on this substrate class is O(1) in site structure; persistent state cannot
  buy a depth-growing work reduction. Treat acquisition as a constant-cost deterministic procedure, stop optimizing
  it here, and move effort to substrate expansion; path persistence is deprioritized with recorded evidence.

## Validity threats

VN-V1 tokenizer unavailable in DESIGN (byte channel is the size basis; token channel gated on a versioned import).
VN-V2 static links only, so hop can exceed a browser-observed hop. VN-V3 same-host only, so real depth may be
understated and the claim is bounded accordingly. VN-V4 sites whose two sessions disagree on hop/request count are
flagged and excluded. VN-V5 network failure is `BLOCKED`, not negative. VN-V6 JS-rendered controls are missed; detection
rate is reported per site. VN-V7 `hop == 2` excluded from the primary contrast. VN-V8 pool is mdBook-dominated;
generalization across hosts/engines is not claimed.

## Not authorized

Re-measuring the static re-derivable fraction; re-entering the terminated deterministic-compilation-bypass thread;
returning to the blocked `C-SEMANTIC-RESOLVE` thread; freezing any design whose falsifier cannot trigger; the
five-class stationarity taxonomy.
