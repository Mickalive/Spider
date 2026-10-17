# EXP-FRONTIER-38940047535 preregistration

Status: DESIGN (design-contract v2). Awaiting independent design review and freeze.

Lane: `frontier`. Request: `research/experiments/EXP-FRONTIER-38940047535/request.json`
(`request_id` `ac7428b2685bd7294137e1b5`, `request_hash`
`e1ca787fe83eafb5d624b59cb384d38a664dc988f03bc99d8e984471cfd7c05d`, base_sha
`677bd0d2d29128493c03c652bd08d0959a70bc72`, cycle `38939560846`).

Director mandate: action `CONTINUE`, target claim `C-CROSSSITE`, `cognitive_reset=true`,
reason `global-director-CONTINUE`, parent handoff `EXP-FRONTIER-38188815194`
(sha256 `17775eed6e3f69c29457cd00171de2fcc4cf4c0a01627b6944ec56a33311f650`).

This packet refines the Director's strategic question into the smallest rigorous
falsifiable measurement that can still be completed inside the harness envelope. It
does not drift to the parent handoff's proposal, it does not re-run the parent's
frozen packet, and it does not enlarge the ladder the Director told us to shrink.

## 1. Identity, claim binding, and scope

- Target claim: `C-CROSSSITE` (registry status `HYPOTHESIS`; product capability
  "cross-site inheritance"; `next_gate` "true website holdout without site identity
  leakage"). `claim_ids=["C-CROSSSITE"]` stays inside the frontier lane charter
  (`C-WEB-DYNAMICS`, `C-RESIDUAL-NOVELTY`, `C-SEMANTIC-RESOLVE`, `C-CROSSSITE`).
- This experiment measures the **maintenance/invalidation economics of a persisted
  deep-path store** on four live documentation sites. It does **not** validate
  cross-site transfer of a learned mechanism, it does not test the discovery axis
  (validly closed at 0/208 by `EXP-FRONTIER-38184956362`), and it does not promote
  any claim under any branch.
- Substrate: credential-free, GET-only, stdlib `urllib`; single runner vantage; no
  model endpoint, no browser, no Docker, no credentials. Cost is measured in HTTP
  GETs (primary), response bytes and wall-clock seconds.
- **Cost-model scope boundary (hard):** the cost model counts Web work only - GETs
  and bytes. It excludes model calls, tokens, reasoning and tool latency. Any
  product-level cost conclusion is therefore about Web work, not about end-to-end
  agent economics. This is disclosed, not corrected, and matches the parent thread's
  scope.
- Invalidation statistics are bounded to the **session regime** by V7. The legacy
  program already established that day-scale staleness is undecidable on committed
  corpora, so no day-scale hazard or freshness-detector claim is permitted here.

## 2. Legacy and pre-2.0 disposition

`LEGACY: DISTINCT_EXTENSION` with one rigorous replication component.

- WP-002B (archived Codex section 1; archive blob
  `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`) measured 901 one-step next-state
  transitions from 300 trajectories (rule 0.6238 vs NN 0.6295 vs shuffle 0.5706)
  with no website holdout. WP-003 (artifact sha
  `292e3243d9bc7a3b88712788a7cb05709eb74eb9`) is MEASUREMENT_INVALID for
  `prev_action` target leakage and a mislabeled bootstrap. WP-003B (sha
  `f6cfdfc749cae9eb4d9fcc4b11b94b63a2bcfb6e`) reports action-only MSE 0.756 vs
  full 0.735 on 875 rows. **None of these measures persistence maintenance,
  revalidation cost, or invalidation economics**, so there is no pre-2.0 design to
  duplicate and none is repeated. The binding guard adopted from WP-003B is "avoid
  rerunning near-identical state-feature tests"; this packet tests a cost and
  hazard object, not a state-feature predictor.
- P2-REPLAY-COST (pre-2.0 artifact 4.114, sha
  `9687ff787f2d74460bb7006826008852f5b4416b`) withdrew an 8.5x replay speed claim:
  2.822 s cold vs 2.816 s replay = 1.002x on matched tasks. Binding guards adopted:
  (i) fully-loaded counterfactual costs, measured not asserted; (ii) exact-path
  replay is a **baseline**, never an assumed win - hence
  `B-NAIVE-EXACT-PATH-REPLAY` is instrumented for safety instead of being dismissed;
  (iii) never frame scripted replay as real-agent economics - reinforced by the
  Web-work-only scope boundary in section 1.
- P2-BLIND-COMPOSITION (artifact 4.697, sha
  `017a80aeb9a6759c8f6913a37031ff1616ec1bda`): 3/3 unseen compositions vs 0/3 weak
  baselines, with keyword and oracle dependence. Guards adopted: no keyword or
  oracle-guided stopping here (the crawl policy is purely mechanical FIFO + static
  `<a>` links with a frozen budget), and the comparator is the strongest fair
  alternative measured in the same run rather than a cold/single-shot straw man.
- P2-AUTOMATION (archived Codex section 2) operational lesson: separate workflow
  completion from scientific validity, per-item recovery, hash-pinned inheritance.
  This packet implements it directly: every operational abort has a distinct
  pre-registered disposition and no abort can be encoded as a negative.

**Replication component (policy, not defect).** The BFS reconstruction policy, the
four min-hop seeds, the 10% material-margin pay rule and the per-item/batch
comparison forms are replicated verbatim from `EXP-FRONTIER-38184956362` and
`EXP-FRONTIER-38188815194`, so that a live result is comparable with the frozen
926-URL / 208-item frame. What is repaired rather than replicated is listed in
section 4.

**Search limitation, stated honestly.** The legacy screen used
`codex/legacy_brief.json` plus the four artifacts named above; no additional
`codex/legacy_artifact_index.json` entry was read as primary source for this packet,
because the screened findings already establish that the pre-2.0 program contains
no persistence-maintenance/invalidation cost measurement. Absence of a hit in the
compact brief is not proof of absence from the 1401-artifact archive, so this is a
bounded screen, not an exhaustive one.

## 3. Parent-handoff disposition (four-way, preserved)

Source: `research/experiments/EXP-FRONTIER-38188815194/handoff.json`.

- **established**: (i) the parent's frozen instrument is sound - code identity and
  all nine offline controls passed under its own scoring code, so its failure was
  not instrumental; (ii) the frozen structural frame arithmetic reproduces exactly
  (250+250+176+250 = 926 discovered URLs on the four hosts; 208 admitted live deep
  items at hops 3-4; per-item BFS ordinal mean 166.0144, min 31, max 250;
  fully-loaded per-item 926/208 = 4.451923; batch threshold 833.4; per-item
  threshold 4.006731); (iii) that frame has aged out of the live Web under the
  frozen policy (179/208 reconstructible, 29 misses concentrated on
  `docs.pytest.org` 26 and `doc.rust-lang.org` 3), a pre-registered V3
  representation-loss trigger; (iv) the harness envelope mismatch is an
  infrastructure fact (3000 s in-process ladder, >=3558 s minimum wall clock,
  versus `SPIDER_MODEL_MAX_RUNTIME_SECONDS` default 1200 s with group kill plus
  `git reset --hard` / `git clean` on retry).
- **rejected**: nothing. The parent is MEASUREMENT_INVALID / NOT_APPLICABLE with
  every outcome metric null; this packet claims no direction from it.
- **unknown (exactly what this packet measures)**: whether the population can be
  registered live and still be non-degenerate; the store's true maintenance cost;
  the session-scale change/dead/false-accept rates; whether endpoint-only liveness
  suffices; whether any measurement fits the current envelope.
- **do_not_assume**: the parent's null metrics are not zeros and not priors; the
  parent's frozen packet must not be re-run (its V3 is deterministic on an aged
  frame and its ladder is unreachable); nothing here validates `C-CROSSSITE`
  transfer; no hazard statement leaves the session regime; the parent's producer
  hypothesis (site restructuring caused the 29 misses) is a hypothesis, not an
  observation.

## 4. What is repaired relative to the parent packet (three defects)

1. **Aged external frame as denominator.** The parent's V3 demanded that every item
   of a *frozen external* `items.jsonl` be reconstructed live; 29/208 were not, so
   the packet was deterministically MEASUREMENT_INVALID and no outcome was
   produced. Repair: the population is registered **by the very crawl that also
   supplies the cold baseline**, so coverage is definitional - `n_paths ==
   n_admitted` - and an aged list can never produce a miss. The parent's list
   survives only as the covariate `M-CENSUS-OVERLAP-PARENT208`. The mandate
   explicitly authorizes this: "register a fresh admitted set", and states that the
   833.4 / 4.006731 constants "no longer denote a live population". The same frozen
   10% margin rule is therefore applied to **live-measured** cold cost and the
   **live-registered** population.
2. **Structural unreachability.** The parent's ladder slept 3000 s in-process and
   spent >5500 GETs inside a 1200 s process envelope whose timeout also resets and
   cleans the worktree, so the confirmatory measurement could not have completed
   even with an intact frame. Repair: 3 opportunistic revalidation cycles with 60 s
   inter-cycle sleeps, one GET per *distinct* stored page per cycle, an exact
   endpoint-only ablation at **zero** extra GET cost, a per-host 100 s census
   deadline, a 3200 GET ledger ceiling, and a 620 s module budget with
   latency-based cycle admission. The census gate is evaluated **before** any
   revalidation GET, exactly as the mandate's "evaluate the V3 path-recovery gate
   before spending the ladder" requires.
3. **Cost accounting that straddled the decision threshold.** The parent's frozen
   module refetched each item's *full path* - physically spending
   `sum|path_i|` (~931 GETs for the 208-item frame) - while *reporting*
   `reval_unique_gets` as the size of the *union* of paths (~201 on the 179-item
   surviving subset, 4.6x lower), and then compared that reported union against the
   833.4 threshold. Its disclosed a-priori expectation ("`reval_unique_gets ~
   931 > 833.4` -> FALSIFIES") therefore contradicts its own metric definition
   (`distinct path pages per window, store-level`) and its own code, which would
   have returned SUPPORTS. Repair: **one accounting is physical.** The fixed module
   fetches each distinct stored page exactly once per cycle, so
   `M-REVAL-UNIQUE-GETS` is simultaneously the reported store cost and the measured
   spend, certified by the new offline control `C-STORE-DEDUP-ACCOUNTING`; the
   no-sharing accounting is retained as the named sensitivity
   `B-STORE-NO-SHARING` / `S-NOSHARE`; and V12 makes any future mismatch between
   reported cost and physical spend a hard gate failure.

Defects 1 and 2 are the two the parent auditor named as required fixes. Defect 3 was
found by DESIGN from the parent's own frozen code and raw evidence and is
independent of the parent's disposition.

## 5. Question and hypotheses

**Question.** On a population registered by the same live crawl that supplies both
the cold baseline and the persisted store, does maintaining a persisted deep
state-carrying path store cost less Web work than cold re-derivation, and does it pay
per item as well as in aggregate; and, at session-scale horizons only, what is the
invalidation hazard of the stored pages, the per-item false-accept rate of 0-GET
naive exact-path replay with its 95% upper bound, and the cost-optimal revalidation
interval implied by that bound?

- **H1 (aggregate economics, B).** Cross-item page sharing is large on this frame,
  so the store's per-cycle maintenance cost `|union of paths|` is far below
  `0.9 * M-COLD-BATCH-GETS`; the strongest fair alternative (re-derive everything
  with a cold host sweep) loses to maintaining the store.
- **H2 (per-item economics, A).** The same mechanism does **not** pay for an
  isolated item: the mean path length is comparable to the amortized cold per-item
  share, because on this frame the crawl is dominated by the deep stratum. So `A`
  is expected to fail while `B` succeeds, and the decision-relevant quantity becomes
  the measured sharing factor `sum|path| / |union|` and the reuse density, i.e. the
  minimum multi-item workload at which the store pays.
- **H3 (invalidation; the genuinely unknown axis).** At session-scale horizons the
  stored documentation pages are expected to be nearly or exactly invariant, so
  `M-CHANGE-RATE`, `M-DEAD-RATE` and `M-FALSE-ACCEPT-NAIVE` are expected to be 0 or
  near 0. The informative output is therefore not the point estimate but the
  censoring-aware bound `M-HAZARD-RATE-UB95` (exact Poisson upper bound on the
  per-page-second incidence rate; rule of three at zero events), the derived
  `M-FALSE-ACCEPT-UB95`, and the tolerance ladder `M-TAU-LADDER` that states which
  product staleness tolerances are and are not certifiable inside one session.
- **H4 (fallback sufficiency).** Interior (non-endpoint) stored pages are few
  relative to endpoints on this frame, so endpoint-only revalidation should detect
  essentially every invalidation that full-path detection catches.
  `M-INTERIOR-ONLY-FAILS` measures the residual it would miss.

## 6. Population, frame, and substrate

**Four bound min-hop seeds** (identical to the parent's frame, so the crawl is
comparable with the frozen 926-URL reference):

| host | seed |
| --- | --- |
| `doc.rust-lang.org` | `https://doc.rust-lang.org/stable/book/` |
| `pandas.pydata.org` | `https://pandas.pydata.org/docs/` |
| `docs.readthedocs.io` | `https://docs.readthedocs.io/en/stable/` |
| `docs.pytest.org` | `https://docs.pytest.org/en/stable/` |

**Crawl policy (frozen, byte-identical transport helpers to the bound parent
`execute_module.py`)**: same-host static `<a>` links only; asset-extension
excluded; item-blind FIFO in document order; per-seed budget `BUDGET = 250`;
`DEPTH = 6`; each URL fetched at most once; the same-host anchor is the netloc of
the seed's **final** URL after redirects (this is why the `docs.readthedocs.io`
items remain reachable: the seed canonicalises to `docs.readthedocs.com`). Only
*recording* is extended relative to the parent (status, final URL, sha256, body
length, content-type, ETag, Last-Modified, elapsed, per-fetch GET ledger); the link
discovery and traversal logic is copied verbatim, so reconstruction identity with
the frozen frame holds by construction rather than by assertion.

**Admission rule (frozen).** A crawled URL is *admitted* iff `hop >= 3`
(`ADMIT_MIN_HOP`), its fetch returned HTTP 200, and a parent chain exists in the
crawl. `n_admitted = N`. Because admission is a property of the same crawl that
supplies the cold baseline, `n_paths == N` is definitional (gate V4c). Discovered
but unfetched URLs (budget or time truncation) are counted, not admitted, and
reported per host.

**Cold cost (measured in-run).** `M-COLD-BATCH-GETS` = the ACTUAL number of GETs
the crawl spent (`sum_h gets_h`), with `M-COLD-BATCH-DISCOVERED` and
`M-COLD-BATCH-REF-STRUCT` (the frozen 20-host reference counts) reported alongside.
The frozen-frame reference was 926 discovered URLs; a live value near 926 confirms
the policy reproduced the frame, a materially different value is itself a
fidelity observation, not a failure.

**Store.** For each admitted item, the root-to-item path. The store's page set is
`union of paths`, size `K`. Baseline signatures (status, final URL, sha256,
content-type, ETag, Last-Modified) and first-fetch times are recorded for every
stored page during the census at zero extra GET cost.

**Substrate limits.** Single runner vantage; credential-free GET-only; no cookies
(plain `urllib` without a cookie processor); `User-Agent: spider-r2/1.0`; per-request
timeout `REQUEST_TIMEOUT = 12.0 s`; per-host crawl deadline
`CENSUS_HOST_BUDGET_S = 100 s` with `time_truncated` recorded per host.

## 7. Arms (stable ids)

- **`T-PERSIST-PATH-STORE`** (treatment): maintain the store by revalidating each
  **distinct** stored page once per cycle. Physical cycle cost = `K` GETs; that is
  also the reported `M-REVAL-UNIQUE-GETS`. Pessimistic accounting recorded
  separately as `M-REVAL-NOSHARE-GETS = sum_i len(path_i)`.
- **`B-COLD-BATCH-CRAWL`** (strongest fair memoryful alternative): one cold crawl
  per host per cycle under the identical policy, re-deriving everything. Measured
  live on the same population.
- **`B-COLD-AMORTIZED-PER-ITEM`** (per-item decision comparator):
  `M-COLD-BATCH-GETS / n_admitted`, fully loaded.
- **`B-COLD-BFS-PER-ITEM`** (mandate comparator, descriptive only): live per-item
  BFS discovery ordinals (`M-COLD-ITEM-ORDINAL`).
- **`B-NAIVE-EXACT-PATH-REPLAY`** (competitor-strength floor baseline): 0 GETs per
  use, no revalidation. Safety measured: `M-FALSE-ACCEPT-NAIVE`,
  `M-FALSE-ACCEPT-UB95`, `M-TAU-LADDER`.
- **`B-COLD-PARENT-START`** (generality bound, reported only): targeted
  re-derivation from the item's parent = 1 GET/item = `N` GETs for the whole set.
  This is the cheapest cold alternative and bounds when the store can pay at all.
- **`A-ENDPOINT-ONLY-REVALIDATE`** (mandated fallback, executed): every admitted
  endpoint is already in `union`, so the arm is read **exactly** from the same cycle
  rows at zero extra GET cost. Cost = `N` GETs/cycle (`M-ENDPOINT-GETS`); residual
  risk = `M-INTERIOR-ONLY-FAILS`.
- **`B-STORE-NO-SHARING`** (pessimistic accounting sensitivity): the aggregate
  comparison with cost `M-REVAL-NOSHARE-GETS`; reported verdict `S-NOSHARE`.

Cost accounting is fully loaded: every HTTP request counts as one GET (redirects
followed by `urllib` are folded into the single logical GET and the final URL is
recorded); bytes are received body bytes; elapsed is wall clock.

## 8. Frozen metric ids

Preserved from the parent thread where the quantity still exists:
`M-COLD-BATCH-GETS`, `M-COLD-BATCH-DISCOVERED`, `M-COLD-BATCH-BYTES`,
`M-COLD-ITEM-ORDINAL`, `M-REVAL-PATH-GETS`, `M-REVAL-UNIQUE-GETS`,
`M-REVAL-PATH-BYTES`, `M-REVAL-PATH-ELAPSED`, `M-CHANGE-RATE`, `M-DEAD-RATE`,
`M-FALSE-ACCEPT-NAIVE`, `M-ENDPOINT-GETS`, `M-BREAK-EVEN-HOP` (reported as null
with reason: hop is fixed by admission and cannot vary), `M-BREAK-EVEN-DENSITY`
(= `K / n_admitted`, stored pages per item), `M-BREAK-EVEN-CYCLES`
(= `M-COLD-BATCH-GETS / K`).

New ids introduced here:
`M-CENSUS-n_admitted`, `M-CENSUS-n_union_pages`, `M-CENSUS-n_interior_pages`,
`M-CENSUS-mean_path_len`, `M-CENSUS-max_path_len`, `M-CENSUS-GETS`,
`M-CENSUS-OVERLAP-PARENT208`, `M-COLD-BATCH-REF-STRUCT`,
`M-STORE-SHARING-FACTOR` (= `sum|path| / K`), `M-REUSE-ITEMS-PER-PAGE`
(= `n_admitted / interior pages`), `M-REVAL-NOSHARE-GETS`, `M-INTERIOR-ONLY-FAILS`,
`M-CHANGE-EVENTS`, `M-DEAD-EVENTS`, `M-MOVED-EVENTS`, `M-N-PAGES-EVER-INVALID`,
`M-PAGES-OBSERVED`, `M-STORE-PAGE-SECONDS`, `M-HAZARD-RATE-UB95` (per page-second),
`M-PAGE-INVALID-UB95` (Wilson), `M-FALSE-ACCEPT-UB95`, `M-TAU-LADDER`,
`M-LIVE-POS-CHANGE`, `M-LIVE-NULL-CHANGED`, `M-WINDOWS-COMPLETED`,
`M-TOTAL-GETS`, `M-MODULE-ELAPSED-S`.

`M-REVAL-PATH-GETS` keeps the parent's meaning (mean per-item persisted path
length, a logical per-item cost) and `M-REVAL-UNIQUE-GETS` keeps the parent's own
definition ("distinct path pages per window, store-level"); what changes is that the
second is now also the physical spend (V12).

## 9. Frozen control ids

**Offline, in-process HTTP fixture, no external network** - run by the same frozen
code that scores the experiment:

1. `C-BFS-PARENT-CHAIN` - parent-tracking BFS reconstructs the expected chain.
2. `C-STORE-DEDUP-ACCOUNTING` - `|union| < sum|path|` and `|union|` is the physical
   fetch count, so the two accountings are separated and the primary one is physical.
3. `C-PATH-CANARY` - every store page returns HTTP 200.
4. `C-REVAL-NOCHANGE` - an unchanged store yields only `UNCHANGED` (null).
5. `C-REVAL-CHANGE-DETECT` - a mutated endpoint is `CHANGED` while its unchanged
   sibling is not (positive, and it isolates the page state as the cause).
6. `C-LIVENESS-404` - a removed endpoint is `DEAD`.
7. `C-REVAL-MOVED-REDIRECT` - a 302 to a new final URL is classified `MOVED`, not
   silently followed (a new detector: a canonicalisation counts as invalidation).
8. `C-HAZARD-BOUND-RULE3` - the Poisson bound equals `3/N` at zero events and is
   strictly larger at five events.
9. `C-WILSON-BOUND-DIRECTION` - the Wilson bound is strictly increasing in events.
10. `C-TAU-LADDER-MONOTONE` - `tau` is strictly increasing in tolerance.
11. `C-DECISION-CANARY-SUPPORTS` - `decide(mean_path=3.0, K=300; cold=926, N=208)` -> `SUPPORTS`.
12. `C-DECISION-CANARY-MIXED` - `decide(mean_path=4.4, K=201; cold=926, N=208)` -> `MIXED` (aggregate pays, per item does not).
13. `C-DECISION-CANARY-MIXED-FLIP` - disagreement across cycles -> `MIXED`.
14. `C-DECISION-CANARY-FALSIFIES` - `decide(mean_path=5.0, K=931; cold=926, N=208)` -> `FALSIFIES`.
15. `C-DECISION-CANARY-NODATA` - empty rows -> `NO_DATA` (never a negative).

**EXECUTE-time gates and live controls:**

- `C-CODE-IDENTITY` (V1), `C-CONTROLS-GATE` (V2, all fifteen before the census),
  `C-SEED-LIVENESS` (V3), `C-CENSUS-GATE` (V4, before any revalidation GET),
  `C-CENSUS-COVERAGE` (V4c), `C-BUDGET` (V5), `C-DENOMINATOR-GUARD` (V6),
  `C-ENVELOPE` (V8), `C-ACCOUNTING-RECONCILIATION` (V12).
- `C-LIVE-POS-CHANGE` (positive, live): at least one of
  `https://www.cloudflare.com/cdn-cgi/trace`,
  `https://api.github.com/rate_limit`,
  `https://timeapi.io/api/Time/current/zone?timeZone=UTC` must change body or final
  URL between observations. This establishes **transport-level** detector
  sensitivity over real HTTP against real servers, which an in-process fixture
  cannot; it does not claim that documentation pages change.
- `C-LIVE-NULL-CHANGED` (null, live): `https://example.com/` and
  `https://www.iana.org/domains/reserved` must not change; a change is reported as
  a spurious-firing alarm.

## 10. Frozen EXECUTE module

The exact module below is the frozen EXECUTE driver (`execute_module.py`). It is
stdlib-only and credential-free. At EXECUTE it is reconstructed byte-for-byte from
this block; the extraction rule is: let `block` be the bytes strictly after the
opening marker line and strictly before the closing marker line, and
`C = block.strip()`; then `sha256(C)` must equal
`DERIVED_SHA256 = 017c8bbcab9e8751ac5718affcf6563aa36c1cef82e6e23078c4d3d880804a0a`.
`prereg.md` is itself hashed in `freeze.json.hashes`, so the module identity is
frozen even though it is not a separate repository file at freeze time.

Interface: `--stage controls|all --out <dir> [--sleep S] [--cycles N]`.
Outputs under `--out`: `raw/controls.jsonl`, `raw/control_probes.jsonl`,
`raw/census.jsonl`, `raw/paths.jsonl`, `raw/store_pages.jsonl`,
`raw/cycle_01.jsonl`.., `raw/PROGRESS.json`, `derived/metrics.json`,
`derived/decision.json`.

FROZEN_CODE_BEGIN
#!/usr/bin/env python3
"""EXP-FRONTIER-38940047535 - maintenance/invalidation economics of a persisted
deep-path store on a live-registered population.

Frozen EXECUTE driver. stdlib-only, credential-free GET-only, single vantage.
Stages:
  controls  offline in-process HTTP fixture canaries (no external network)
  all       controls, then live census (population registration), then bounded
            revalidation cycles, then the frozen decision
Emits, under --out:
  raw/controls.jsonl, raw/control_probes.jsonl, raw/census.jsonl,
  raw/paths.jsonl, raw/store_pages.jsonl, raw/cycle_XX.jsonl,
  derived/metrics.json, derived/decision.json, raw/PROGRESS.json
"""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import http.server
import json
import math
import socketserver
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# --------------------------------------------------------------------------
# frozen constants
# --------------------------------------------------------------------------
BUDGET = 250
DEPTH = 6
MIN_REL = 0.10
MIN_ABS_GETS = 5.0
ADMIT_MIN_HOP = 3
MIN_ADMITTED = 40
MIN_HOSTS = 2
TOTAL_GET_CEILING = 3200
CENSUS_HOST_BUDGET_S = 100.0
MODULE_WALL_BUDGET_S = 620.0
CYCLE_MARGIN_S = 20.0
PLANNED_CYCLES = 3
INTER_CYCLE_SLEEP_S = 60.0
REQUEST_TIMEOUT = 12.0
TOL_LADDER = (0.005, 0.01, 0.02, 0.05, 0.10)
N_CYCLE_PROBES = 6

SEEDS = [
    ("doc.rust-lang.org", "https://doc.rust-lang.org/stable/book/"),
    ("pandas.pydata.org", "https://pandas.pydata.org/docs/"),
    ("docs.readthedocs.io", "https://docs.readthedocs.io/en/stable/"),
    ("docs.pytest.org", "https://docs.pytest.org/en/stable/"),
]
PARENT_ITEMS = "research/experiments/EXP-FRONTIER-38184956362/raw/items.jsonl"
PARENT_STRUCT = "research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl"

POS_CONTROL_URLS = [
    "https://www.cloudflare.com/cdn-cgi/trace",
    "https://api.github.com/rate_limit",
    "https://timeapi.io/api/Time/current/zone?timeZone=UTC",
]
NULL_CONTROL_URLS = [
    "https://example.com/",
    "https://www.iana.org/domains/reserved",
]

ASSET_EXTS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".bz2", ".xz", ".mp3", ".mp4", ".webm", ".avi", ".mov", ".txt", ".xml",
)

T0 = time.monotonic()
GET_LEDGER = {"n": 0}


def elapsed() -> float:
    return time.monotonic() - T0


# --------------------------------------------------------------------------
# frozen decision function
# --------------------------------------------------------------------------
def pays(reference: float, candidate: float, min_abs: float = MIN_ABS_GETS) -> bool:
    need = max(MIN_REL * reference, min_abs)
    return (reference - candidate) >= need


def decide(rows, cold_batch_gets, n_items):
    """Frozen decision rule (mandate thresholds re-derived from the live census).

    A_w = per-item / no-sharing view: servicing ONE admitted item's persisted
          path costs mean_path GETs; the fair memoryful alternative is the
          amortized share of a cold re-crawl, cold_batch_gets/n_items. A_w pays
          iff mean_path <= 0.9 * (cold_batch_gets/n_items).
    B_w = store / sharing view: maintaining the WHOLE store for one cycle costs
          K_w distinct-page GETs (one fetch per distinct union page, the actual
          physical spend); the fair alternative is the cold batch re-crawl.
          B_w pays iff K_w <= 0.9 * cold_batch_gets.
    SUPPORTS  = A_w AND B_w at every measured cycle (pays per item and in aggregate).
    FALSIFIES = B_w false AND A_w false at every measured cycle (pays nowhere).
    MIXED     = every other combination. Because K <= sum_i|path_i| = N*mean_path, a
                per-item pay IMPLIES an aggregate pay, so the only MIXED sub-state this
                experiment can reach is "aggregate pays through cross-item page sharing
                while an isolated item does not pay"; the cross-cycle disagreement
                sub-state is certified by canary but cannot be produced by a frozen
                store page set.
    S-NOSHARE is the pessimistic sensitivity: the same aggregate comparison with
    a store that performs no cross-item page sharing (sum of path lengths).
    """
    if not rows or not n_items or cold_batch_gets <= 0:
        return {"outcome": "NO_DATA", "a_pays": [], "b_pays": [], "b_noshare_pays": [],
                "cold_amortized_gets": None, "batch_threshold_gets": None,
                "noshare_threshold_gets": None, "break_even_cycles": None,
                "n_items": n_items, "cycles": 0}
    cold_amort = cold_batch_gets / n_items
    batch_thr = cold_batch_gets - max(MIN_REL * cold_batch_gets, MIN_ABS_GETS)
    noshare_thr = batch_thr
    a_pays, b_pays, b_ns = [], [], []
    for r in rows:
        mp = float(r["mean_path_gets"])
        k = float(r["store_unique_gets"])
        ns = float(r["store_noshare_gets"])
        a_pays.append(pays(cold_amort, mp, min_abs=0.0))
        b_pays.append(pays(float(cold_batch_gets), k))
        b_ns.append(pays(float(cold_batch_gets), ns))
    if all(a_pays) and all(b_pays):
        outcome = "SUPPORTS"
    elif (not any(a_pays)) and (not any(b_pays)):
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"
    if all(a_pays) and all(b_ns):
        noshare = "SUPPORTS"
    elif (not any(a_pays)) and (not any(b_ns)):
        noshare = "FALSIFIES"
    else:
        noshare = "MIXED"
    return {"outcome": outcome, "a_pays": a_pays, "b_pays": b_pays,
            "b_noshare_pays": b_ns, "noshare_outcome": noshare,
            "cold_amortized_gets": cold_amort, "batch_threshold_gets": batch_thr,
            "noshare_threshold_gets": noshare_thr,
            "break_even_cycles": cold_batch_gets / rows[0]["store_unique_gets"]
            if rows[0]["store_unique_gets"] else None,
            "n_items": n_items, "cycles": len(rows)}


def wilson_upper(k: int, n: int, z: float = 1.959963984540054) -> float:
    """Wilson score 95% upper bound for a binomial proportion (0 events -> 0)."""
    if n <= 0:
        return 1.0
    p = k / n
    d = 1.0 + z * z / n
    centre = p + z * z / (2 * n)
    rad = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return min(1.0, (centre + rad) / d)


def poisson_ub(events: int, person_seconds: float) -> float:
    """Exact one-sided 95% upper bound on an incidence rate (Garwood, pure math).
    events == 0 reduces to the rule of three."""
    if person_seconds <= 0:
        return float("inf")
    if events <= 0:
        return 3.0 / person_seconds
    k = events
    while True:
        lam = k / person_seconds
        # P(X >= k | lam)
        term = math.exp(-lam)
        cum = term
        for i in range(1, k):
            term *= lam / i
            cum += term
        if (1.0 - cum) <= 0.05:
            return lam
        k += 1
        if k > 100000:
            return lam


# --------------------------------------------------------------------------
# transport (norm/is_asset/static_links/fetch mirror the bound parent policy)
# --------------------------------------------------------------------------
class _LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d = dict(attrs)
            href = d.get("href")
            if href:
                self.hrefs.append(href)


def repo_root() -> Path:
    p = Path(__file__).resolve()
    for anc in [p.parent] + list(p.parents):
        if (anc / "research" / "lanes" / "registry.json").is_file():
            return anc
    return Path.cwd()


def norm(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    if ":" in netloc and not netloc.endswith("]"):
        host, _, port = netloc.rpartition(":")
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    path = p.path or "/"
    return urllib.parse.urlunsplit((scheme, netloc, path, p.query, ""))


def is_asset(url: str) -> bool:
    return urllib.parse.urlsplit(url).path.lower().endswith(ASSET_EXTS)


def static_links(base: str, body: bytes) -> list:
    lp = _LinkParser()
    try:
        lp.feed(body.decode("utf-8", "replace"))
    except Exception:
        return []
    out = []
    for h in lp.hrefs:
        u = urllib.parse.urljoin(base, h.strip())
        if urllib.parse.urlsplit(u).scheme not in ("http", "https"):
            continue
        if is_asset(u):
            continue
        out.append(u)
    return out


def fetch(url: str, timeout: float = REQUEST_TIMEOUT, sleep: float = 0.0) -> dict:
    t0 = time.monotonic()
    GET_LEDGER["n"] += 1
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "spider-r2/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            rec = {"status": int(r.status), "body_len": len(body),
                   "sha256": hashlib.sha256(body).hexdigest(),
                   "final_url": norm(r.geturl()),
                   "content_type": (r.headers.get("Content-Type") or "").split(";")[0].strip(),
                   "etag": r.headers.get("ETag") or "",
                   "last_modified": r.headers.get("Last-Modified") or "",
                   "elapsed": time.monotonic() - t0, "error": None, "body": body}
    except urllib.error.HTTPError as e:
        try:
            e.read()
        except Exception:
            pass
        rec = {"status": int(e.code), "body_len": 0, "sha256": None,
               "final_url": norm(url), "content_type": "", "etag": "",
               "last_modified": "", "elapsed": time.monotonic() - t0,
               "error": "http_%d" % e.code, "body": b""}
    except Exception as e:
        rec = {"status": 0, "body_len": 0, "sha256": None, "final_url": norm(url),
               "content_type": "", "etag": "", "last_modified": "",
               "elapsed": time.monotonic() - t0, "error": repr(e)[:120], "body": b""}
    if sleep:
        time.sleep(sleep)
    return rec


def bfs_census(seed: str, sleep: float = 0.0,
                deadline: float | None = None) -> dict:
    """Mirror of the bound parent bfs_with_parents (same-host static <a>,
    item-blind FIFO, budget BUDGET, depth DEPTH, each URL fetched at most once,
    seed anchor = netloc of the seed's FINAL url). Only recording is extended."""
    parent, hop, ordinal = {}, {}, {}
    out = set()
    time_truncated = False
    records, requests_log = {}, []
    gets = 0
    seed_n = norm(seed)
    rec = fetch(seed_n, sleep=sleep)
    gets += 1
    records[seed_n] = rec
    requests_log.append({"url": seed_n, "status": rec["status"], "gets": gets})
    if rec["status"] != 200:
        return {"seed_error": rec["error"] or ("status=%d" % rec["status"]),
                "parent": parent, "hop": hop, "ordinal": ordinal, "out": out,
                "records": records, "gets": gets, "requests": requests_log,
                "seed_host": None, "time_truncated": False}
    seed_host = urllib.parse.urlsplit(rec["final_url"]).netloc.lower()
    parent[seed_n] = None
    hop[seed_n] = 0
    ordinal[seed_n] = 1
    out.add(seed_n)
    seed_body = rec["body"]
    queue = [(seed_n, 0)]
    while queue and len(out) < BUDGET:
        if deadline is not None and time.monotonic() > deadline:
            time_truncated = True
            break
        u, h = queue.pop(0)
        if h + 1 > DEPTH:
            continue
        body = seed_body if u == seed_n else None
        base = rec["final_url"] if u == seed_n else None
        if body is None:
            r = fetch(u, sleep=sleep)
            gets += 1
            records[u] = r
            requests_log.append({"url": u, "status": r["status"], "gets": gets})
            if r["status"] != 200:
                continue
            body = r["body"]
            base = r["final_url"]
        for raw in static_links(base, body):
            nu = norm(raw)
            if nu in out:
                continue
            if urllib.parse.urlsplit(nu).netloc.lower() != seed_host:
                continue
            parent[nu] = u
            hop[nu] = h + 1
            ordinal[nu] = len(out) + 1
            out.add(nu)
            queue.append((nu, h + 1))
            if len(out) >= BUDGET:
                break
    return {"seed_error": None, "parent": parent, "hop": hop, "ordinal": ordinal,
            "out": out, "records": records, "gets": gets, "requests": requests_log,
            "seed_host": seed_host, "time_truncated": time_truncated}


def path_to(parent, url):
    if url not in parent:
        return None
    chain = []
    x = url
    guard = 0
    while x is not None and guard < 64:
        chain.append(x)
        x = parent.get(x)
        guard += 1
    return list(reversed(chain))


def classify(base_rec, rec) -> str:
    if rec["status"] == 0:
        return "DEAD"
    if rec["status"] != 200:
        return "DEAD"
    if base_rec is None:
        return "NEW"
    if rec["final_url"] != base_rec["final_url"]:
        return "MOVED"
    if rec["sha256"] != base_rec["sha256"]:
        if base_rec["content_type"] and rec["content_type"] and \
                base_rec["content_type"] != rec["content_type"]:
            return "CHANGED_CT"
        return "CHANGED"
    return "UNCHANGED"


def reval(urls, base, sleep: float = 0.0) -> dict:
    rows = []
    nbytes = 0
    t0 = time.monotonic()
    for u in urls:
        r = fetch(u, sleep=sleep)
        nbytes += r["body_len"]
        rows.append({"url": u, "status": r["status"], "final_url": r["final_url"],
                     "content_type": r["content_type"], "body_len": r["body_len"],
                     "sha256": r["sha256"], "verdict": classify(base.get(u), r)})
    return {"rows": rows, "gets": len(urls), "bytes": nbytes,
            "elapsed": time.monotonic() - t0}


# --------------------------------------------------------------------------
# offline controls (in-process HTTP fixture; no external network)
# --------------------------------------------------------------------------
_FIXTURE = {
    "/": b"<html><body><a href='/a.html'>a</a><a href='/x.html'>x</a></body></html>",
    "/a.html": b"<html><body><a href='/b.html'>b</a><a href='/item.html'>i</a></body></html>",
    "/x.html": b"<html><body><a href='/item2.html'>i2</a></body></html>",
    "/b.html": b"<html><body><a href='/item.html'>i</a></body></html>",
    "/item.html": b"<html><body>ITEM-v1</body></html>",
    "/item2.html": b"<html><body>ITEM2-v1</body></html>",
    "/moved.html": b"<html><body>MOVED-v1</body></html>",
    "/movedtarget.html": b"<html><body>MOVEDTARGET-v1</body></html>",
}
_FIXSTATE = {"deleted": set(), "mutated": False, "redirect": False}


class _FixtureHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path in _FIXSTATE["deleted"]:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if self.path == "/moved.html" and _FIXSTATE["redirect"]:
            self.send_response(302)
            self.send_header("Location", "/movedtarget.html")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        body = _FIXTURE.get(self.path)
        if body is None:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if self.path == "/item.html" and _FIXSTATE["mutated"]:
            body = body.replace(b"ITEM-v1", b"ITEM-v2")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _run_controls(out_dir: Path) -> int:
    rows = []

    def rec(cid, passed, observed):
        rows.append({"control_id": cid, "pass": bool(passed), "observed": observed})

    srv = socketserver.TCPServer(("127.0.0.1", 0), _FixtureHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        base = "http://127.0.0.1:%d" % srv.server_address[1]
        cen = bfs_census(base + "/")
        p1 = path_to(cen["parent"], norm(base + "/item.html"))
        want = [norm(base + "/"), norm(base + "/a.html"), norm(base + "/item.html")]
        rec("C-BFS-PARENT-CHAIN", p1 == want, {"path": p1, "want": want})

        items = {norm(base + "/item.html"): p1, norm(base + "/item2.html"):
                 path_to(cen["parent"], norm(base + "/item2.html"))}
        union = sorted({u for p in items.values() for u in p})
        noshare = sum(len(p) for p in items.values())
        base_map = {}
        for u in union:
            r = fetch(u)
            base_map[u] = {"final_url": r["final_url"], "sha256": r["sha256"],
                           "content_type": r["content_type"]}
        rec("C-STORE-DEDUP-ACCOUNTING",
            len(union) < noshare and len(union) == len(set(union)),
            {"distinct_union": len(union), "noshare_sum": noshare,
             "sharing_factor": noshare / len(union) if union else None})

        sig = {u: {"final_url": base_map[u]["final_url"],
                   "sha256": base_map[u]["sha256"],
                   "content_type": base_map[u]["content_type"]} for u in union}
        r0 = reval(union, sig)
        verdicts = {r["url"]: r["verdict"] for r in r0["rows"]}
        rec("C-REVAL-NOCHANGE",
            all(v == "UNCHANGED" for v in verdicts.values()),
            {"verdicts": verdicts, "gets": r0["gets"]})
        rec("C-PATH-CANARY",
            all(r["status"] == 200 for r in r0["rows"]),
            {"gets": r0["gets"], "n_union": len(union)})

        _FIXSTATE["mutated"] = True
        r1 = reval(union, sig)
        v1 = {r["url"]: r["verdict"] for r in r1["rows"]}
        rec("C-REVAL-CHANGE-DETECT",
            v1.get(norm(base + "/item.html")) == "CHANGED"
            and v1.get(norm(base + "/item2.html")) == "UNCHANGED",
            {"verdicts": v1})

        _FIXSTATE["deleted"].add("/item.html")
        r2 = reval(union, sig)
        v2 = {r["url"]: r["verdict"] for r in r2["rows"]}
        rec("C-LIVENESS-404", v2.get(norm(base + "/item.html")) == "DEAD",
            {"verdicts": v2})

        moved_url = norm(base + "/moved.html")
        rm = fetch(moved_url)
        sig_m = {moved_url: {"final_url": rm["final_url"], "sha256": rm["sha256"],
                             "content_type": rm["content_type"]}}
        _FIXSTATE["redirect"] = True
        r3 = reval([moved_url], sig_m)
        rec("C-REVAL-MOVED-REDIRECT",
            r3["rows"][0]["verdict"] == "MOVED",
            {"verdict": r3["rows"][0]["verdict"]})
        _FIXSTATE["redirect"] = False

        ub0 = poisson_ub(0, 1000.0)
        ub5 = poisson_ub(5, 1000.0)
        rec("C-HAZARD-BOUND-RULE3",
            abs(ub0 - 0.003) < 1e-12 and ub5 > ub0 and ub5 < 0.02,
            {"ub_zero": ub0, "ub_five": ub5})
        w0 = wilson_upper(0, 400)
        w7 = wilson_upper(7, 400)
        w30 = wilson_upper(30, 400)
        rec("C-WILSON-BOUND-DIRECTION",
            0.0 < w0 < 0.02 and 0.02 < w7 < 0.05 and 0.09 < w30 < 0.15
            and w0 < w7 < w30,
            {"wilson_zero": w0, "wilson_seven": w7, "wilson_thirty": w30})
        tau = {t: (t / (ub0 * 4.0) if ub0 > 0 else None) for t in TOL_LADDER}
        rec("C-TAU-LADDER-MONOTONE",
            all(tau[TOL_LADDER[i]] < tau[TOL_LADDER[i + 1]]
                for i in range(len(TOL_LADDER) - 1)),
            {"tau": tau})

        def mkrow(cycle, mean_path, k_gets, ns_gets):
            return {"cycle": cycle, "mean_path_gets": mean_path,
                    "store_unique_gets": k_gets, "store_noshare_gets": ns_gets,
                    "n_items": 10}

        d_sup = decide([mkrow(1, 3.0, 300, 600)], 926, 208)
        rec("C-DECISION-CANARY-SUPPORTS", d_sup["outcome"] == "SUPPORTS",
            {"outcome": d_sup["outcome"], "detail": d_sup})
        d_mix = decide([mkrow(1, 4.4, 201, 788)], 926, 208)
        rec("C-DECISION-CANARY-MIXED", d_mix["outcome"] == "MIXED",
            {"outcome": d_mix["outcome"], "detail": d_mix})
        d_mixw = decide([mkrow(1, 3.0, 300, 600), mkrow(2, 3.0, 931, 931)], 926, 208)
        rec("C-DECISION-CANARY-MIXED-FLIP", d_mixw["outcome"] == "MIXED",
            {"outcome": d_mixw["outcome"]})
        d_fal = decide([mkrow(1, 5.0, 931, 931)], 926, 208)
        rec("C-DECISION-CANARY-FALSIFIES", d_fal["outcome"] == "FALSIFIES",
            {"outcome": d_fal["outcome"]})
        d_nd = decide([], 926, 208)
        rec("C-DECISION-CANARY-NODATA", d_nd["outcome"] == "NO_DATA",
            {"outcome": d_nd["outcome"]})
    finally:
        srv.shutdown()

    (out_dir / "raw").mkdir(parents=True, exist_ok=True)
    with (out_dir / "raw" / "controls.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    ok = all(r["pass"] for r in rows)
    print(json.dumps({"stage": "controls", "all_pass": ok, "n": len(rows),
                      "failed": [r["control_id"] for r in rows if not r["pass"]]}))
    return 0 if ok else 1


# --------------------------------------------------------------------------
# live census + bounded revalidation cycles
# --------------------------------------------------------------------------
def _load_reference(root: Path):
    parent_urls, parent_ordinals = set(), {}
    p = root / PARENT_ITEMS
    if p.is_file():
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            it = json.loads(line)
            if it.get("live"):
                parent_urls.add(norm(it["url"]))
                parent_ordinals[norm(it["url"])] = it.get("ordinal")
    struct_ref = {}
    s = root / PARENT_STRUCT
    if s.is_file():
        for line in s.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            urls = {k: v for k, v in row.items() if isinstance(v, dict) and "hop" in v}
            if urls:
                struct_ref[row["host"]] = len(urls)
    return parent_urls, parent_ordinals, struct_ref


def _probe_controls(base, sleep: float = 0.0):
    rows = []
    for role, urls in (("pos", POS_CONTROL_URLS), ("null", NULL_CONTROL_URLS)):
        for u in urls:
            r = fetch(u, sleep=sleep)
            rows.append({"role": role, "url": u, "status": r["status"],
                         "sha256": r["sha256"], "final_url": r["final_url"],
                         "body_len": r["body_len"], "error": r["error"]})
    return rows


def _run_live(out_dir: Path, sleep: float, cycles: int):
    root = repo_root()
    raw = out_dir / "raw"
    der = out_dir / "derived"
    raw.mkdir(parents=True, exist_ok=True)
    der.mkdir(parents=True, exist_ok=True)
    parent_urls, parent_ordinals, struct_ref = _load_reference(root)

    gets0 = GET_LEDGER["n"]
    probes_t0 = _probe_controls(None, sleep=sleep)
    with (raw / "control_probes.jsonl").open("w") as fh:
        for r in probes_t0:
            fh.write(json.dumps({"obs": 0, **r}, sort_keys=True) + "\n")

    census_hosts, seed_errors = {}, {}
    for label, seed in SEEDS:
        cen = bfs_census(seed, sleep=sleep,
                         deadline=time.monotonic() + CENSUS_HOST_BUDGET_S)
        if cen["seed_error"]:
            seed_errors[label] = cen["seed_error"]
            continue
        census_hosts[label] = cen

    live_hosts = sorted(census_hosts)
    admitted, per_host = [], {}
    base_rec, t_first = {}, {}
    with (raw / "census.jsonl").open("w") as fh:
        for label in live_hosts:
            cen = census_hosts[label]
            host_adm = 0
            for u in sorted(cen["out"]):
                rec = cen["records"].get(u)
                h = cen["hop"].get(u, -1)
                ordv = cen["ordinal"].get(u, -1)
                row = {"host": label, "url": u, "hop": h, "ordinal": ordv,
                       "status": (rec or {}).get("status"),
                       "body_len": (rec or {}).get("body_len"),
                       "content_type": (rec or {}).get("content_type"),
                       "etag": (rec or {}).get("etag", ""),
                       "last_modified": (rec or {}).get("last_modified", ""),
                       "sha256": (rec or {}).get("sha256"),
                       "final_url": (rec or {}).get("final_url"),
                       "admitted": False, "in_parent_208": u in parent_urls,
                       "parent_ordinal": parent_ordinals.get(u)}
                if rec is not None and rec["status"] == 200:
                    base_rec[u] = {"final_url": rec["final_url"],
                                   "sha256": rec["sha256"],
                                   "content_type": rec["content_type"],
                                   "etag": rec["etag"],
                                   "last_modified": rec["last_modified"]}
                    t_first.setdefault(u, elapsed())
                if h >= ADMIT_MIN_HOP and rec is not None and rec["status"] == 200:
                    p = path_to(cen["parent"], u)
                    if p:
                        row["admitted"] = True
                        row["path_len"] = len(p)
                        admitted.append({"url": u, "host": label, "hop": h,
                                         "ordinal": ordv, "path": p})
                        host_adm += 1
                fh.write(json.dumps(row, sort_keys=True) + "\n")
            per_host[label] = {"n_admitted": host_adm,
                               "n_discovered": len(cen["out"]),
                               "gets": cen["gets"],
                               "n_crawled_at_record_time": len(cen["records"]),
                               "time_truncated": bool(cen["time_truncated"])}
    admitted.sort(key=lambda a: a["url"])
    with (raw / "paths.jsonl").open("w") as fh:
        for a in admitted:
            fh.write(json.dumps({"url": a["url"], "host": a["host"], "hop": a["hop"],
                                 "path": a["path"], "len": len(a["path"])},
                                sort_keys=True) + "\n")

    union_pages = sorted({u for a in admitted for u in a["path"]})
    endpoints = [a["url"] for a in admitted]
    endpoint_set = set(endpoints)
    interior_pages = [u for u in union_pages if u not in endpoint_set]
    with (raw / "store_pages.jsonl").open("w") as fh:
        for u in union_pages:
            fh.write(json.dumps({"url": u, "baseline": base_rec.get(u),
                                 "t_first_s": t_first.get(u)}, sort_keys=True) + "\n")

    n_admitted = len(admitted)
    path_lens = [len(a["path"]) for a in admitted]
    mean_path = (sum(path_lens) / n_admitted) if n_admitted else 0.0
    noshare_spend = sum(path_lens)
    cold_batch_gets = sum(per_host[h]["gets"] for h in per_host)
    cold_discovered = sum(per_host[h]["n_discovered"] for h in per_host)
    parent_overlap = sum(1 for a in admitted if a["url"] in parent_urls)

    lat = [r["elapsed"] for cen in census_hosts.values()
           for r in cen["records"].values() if r["status"] == 200]
    per_get = (sum(lat) / len(lat)) if lat else 0.2

    metrics = {
        "n_live_hosts": len(live_hosts), "seed_errors": seed_errors,
        "per_host": per_host,
        "M-CENSUS-n_admitted": n_admitted,
        "M-CENSUS-n_union_pages": len(union_pages),
        "M-CENSUS-mean_path_len": mean_path,
        "M-CENSUS-max_path_len": max(path_lens) if path_lens else 0,
        "M-COLD-BATCH-GETS": cold_batch_gets,
        "M-COLD-BATCH-DISCOVERED": cold_discovered,
        "M-COLD-BATCH-BYTES": sum((r or {}).get("body_len", 0)
                                  for cen in census_hosts.values()
                                  for r in cen["records"].values()),
        "M-COLD-BATCH-REF-STRUCT": struct_ref,
        "M-COLD-ITEM-ORDINAL": {
            "n": n_admitted,
            "mean": (sum(a["ordinal"] for a in admitted) / n_admitted) if n_admitted else None,
            "min": min((a["ordinal"] for a in admitted), default=None),
            "max": max((a["ordinal"] for a in admitted), default=None)},
        "M-CENSUS-OVERLAP-PARENT208": parent_overlap,
        "M-STORE-SHARING-FACTOR": (noshare_spend / len(union_pages)) if union_pages else None,
        "M-CENSUS-n_interior_pages": len(interior_pages),
        "M-REUSE-ITEMS-PER-PAGE": (n_admitted / len(interior_pages))
        if interior_pages else None,
        "M-CENSUS-GETS": GET_LEDGER["n"] - gets0,
        "census_elapsed_s": elapsed(),
    }

    census_gate = {
        "V3_seed_liveness": {"n_live_hosts": len(live_hosts),
                             "pass": len(live_hosts) >= MIN_HOSTS},
        "V3b_census_min_admitted": {"n_admitted": n_admitted, "min": MIN_ADMITTED,
                                    "pass": n_admitted >= MIN_ADMITTED},
        "V3c_coverage_definitional": {"n_paths": n_admitted,
                                      "n_admitted": n_admitted, "pass": True},
        "V6_denominator": {"cold_batch_gets": cold_batch_gets,
                           "n_admitted": n_admitted,
                           "pass": cold_batch_gets > 0 and n_admitted > 0},
    }
    metrics["gates_census"] = census_gate
    metrics["decision"] = {"outcome": "NO_DATA", "census_gate_failed": True,
                           "census_gate": census_gate}
    if not all(g["pass"] for g in census_gate.values()):
        metrics["M-WINDOWS-COMPLETED"] = 0
        metrics["M-TOTAL-GETS"] = GET_LEDGER["n"]
        metrics["M-MODULE-ELAPSED-S"] = elapsed()
        (der / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
        (der / "decision.json").write_text(json.dumps(metrics["decision"], indent=2,
                                                     sort_keys=True) + "\n")
        print(json.dumps({"stage": "live", "census_gate": "FAIL",
                          "gates": census_gate, "gets": GET_LEDGER["n"],
                          "elapsed_s": round(elapsed(), 1)}))
        return 0

    rows, cycle_rows = [], []
    invalid_pages, item_invalid, exposure = set(), {}, {}
    pos_changed, null_changed = False, False
    probe_base = {r["url"]: r for r in probes_t0}
    cycle = 0
    while cycle < cycles:
        est = (len(union_pages) + N_CYCLE_PROBES) * per_get \
            + INTER_CYCLE_SLEEP_S + CYCLE_MARGIN_S
        if elapsed() + est > MODULE_WALL_BUDGET_S:
            break
        if cycle > 0:
            time.sleep(INTER_CYCLE_SLEEP_S)
        cycle += 1
        t_cycle = elapsed()
        res = reval(union_pages, base_rec, sleep=sleep)
        for r in res["rows"]:
            if r["verdict"] in ("CHANGED", "DEAD", "MOVED", "CHANGED_CT"):
                invalid_pages.add(r["url"])
            if r["verdict"] == "UNCHANGED":
                exposure[r["url"]] = t_cycle - t_first.get(r["url"], 0.0)
        vmap = {x["url"]: x["verdict"] for x in res["rows"]}
        bad_v = ("CHANGED", "DEAD", "MOVED", "CHANGED_CT")
        bad = {}
        for a in admitted:
            bad_pages = [u for u in a["path"] if vmap.get(u) in bad_v]
            if bad_pages:
                item_invalid[a["url"]] = bad_pages
        # Endpoint-only ablation is a strict SUBSET of the full-path arm: every
        # admitted endpoint is already in the store's union page set, so its
        # verdicts and byte cost are read from the same cycle rows at zero extra
        # GET cost and its request count is exactly n_admitted.
        abl_bad = {u: vmap[u] for u in endpoints
                   if vmap.get(u) in ("CHANGED", "DEAD", "MOVED", "CHANGED_CT")}
        probes = _probe_controls(None, sleep=sleep)
        with (raw / "control_probes.jsonl").open("a") as fh:
            for r in probes:
                b = probe_base.get(r["url"])
                diff = bool(b) and (b["sha256"] != r["sha256"] or
                                    b["final_url"] != r["final_url"])
                if r["role"] == "pos" and diff:
                    pos_changed = True
                if r["role"] == "null" and diff:
                    null_changed = True
                fh.write(json.dumps({"obs": cycle, **r, "differs_from_obs0": diff},
                                    sort_keys=True) + "\n")
        interior_only = sorted(set(item_invalid) - set(abl_bad))
        row = {"cycle": cycle, "t_cycle_s": t_cycle,
               "n_items": n_admitted,
               "store_unique_gets": res["gets"],
               "store_unique_bytes": res["bytes"],
               "store_unique_elapsed_s": res["elapsed"],
               "store_noshare_gets": noshare_spend,
               "mean_path_gets": mean_path,
               "n_invalid_pages": len(invalid_pages),
               "n_items_invalid": len(item_invalid),
               "n_items_invalid_interior_only": len(interior_only),
               "ablation_endpoint_gets": len(endpoints),
               "ablation_endpoint_invalid": len(abl_bad),
               "ablation_endpoint_bytes": sum(x["body_len"] for x in res["rows"]
                                              if x["url"] in endpoint_set)}
        rows.append(row)
        cycle_rows.append({"cycle": cycle, "rows": res["rows"]})
        (raw / ("cycle_%02d.jsonl" % cycle)).write_text(
            "".join(json.dumps(x, sort_keys=True) + "\n" for x in res["rows"]))
        (raw / "PROGRESS.json").write_text(json.dumps(
            {"cycle": cycle, "elapsed_s": elapsed(), "gets": GET_LEDGER["n"],
             "n_invalid_pages": len(invalid_pages)}, indent=2) + "\n")

    metrics["M-WINDOWS-COMPLETED"] = len(rows)
    metrics["M-TOTAL-GETS"] = GET_LEDGER["n"]
    metrics["M-MODULE-ELAPSED-S"] = elapsed()
    if rows:
        metrics["M-REVAL-PATH-GETS"] = mean_path
        metrics["M-REVAL-UNIQUE-GETS"] = rows[0]["store_unique_gets"]
        metrics["M-REVAL-NOSHARE-GETS"] = noshare_spend
        metrics["M-REVAL-PATH-BYTES"] = rows[0]["store_unique_bytes"]
        metrics["M-REVAL-PATH-ELAPSED"] = rows[0]["store_unique_elapsed_s"]
        metrics["M-ENDPOINT-GETS"] = rows[0]["ablation_endpoint_gets"]
        metrics["M-BREAK-EVEN-DENSITY"] = (rows[0]["store_unique_gets"] / n_admitted
                                           if n_admitted else None)
        metrics["M-BREAK-EVEN-CYCLES"] = (cold_batch_gets / rows[0]["store_unique_gets"]
                                          if rows[0]["store_unique_gets"] else None)
        metrics["M-CHANGE-EVENTS"] = sum(1 for a in admitted for u in a["path"]
                                         if u in invalid_pages)
        metrics["M-DEAD-EVENTS"] = sum(
            1 for cr in cycle_rows for x in cr["rows"] if x["verdict"] == "DEAD")
        metrics["M-MOVED-EVENTS"] = sum(
            1 for cr in cycle_rows for x in cr["rows"] if x["verdict"] == "MOVED")
        metrics["M-CHANGE-RATE"] = (len(invalid_pages) / len(union_pages)
                                    if union_pages else None)
        metrics["M-DEAD-RATE"] = (metrics["M-DEAD-EVENTS"] /
                                  max(1, sum(len(cr["rows"]) for cr in cycle_rows)))
        metrics["M-FALSE-ACCEPT-NAIVE"] = (len(item_invalid) / n_admitted
                                           if n_admitted else None)
        n_pages_obs = sum(len(cr["rows"]) for cr in cycle_rows)
        ps = sum(exposure.values()) or 0.0
        ev = len(invalid_pages)
        metrics["M-STORE-PAGE-SECONDS"] = ps
        metrics["M-PAGES-OBSERVED"] = n_pages_obs
        metrics["M-N-PAGES-EVER-INVALID"] = ev
        metrics["M-HAZARD-RATE-UB95"] = poisson_ub(ev, ps) if ps > 0 else None
        metrics["M-PAGE-INVALID-UB95"] = wilson_upper(ev, len(union_pages))
        lmax = metrics["M-CENSUS-max_path_len"]
        hz = metrics["M-HAZARD-RATE-UB95"]
        if hz and lmax:
            fa = 1.0 - (1.0 - min(1.0, hz * metrics["M-MODULE-ELAPSED-S"])) ** lmax
            metrics["M-FALSE-ACCEPT-UB95"] = fa
            metrics["M-TAU-LADDER"] = {str(t): (t / (hz * lmax)) for t in TOL_LADDER}
        else:
            metrics["M-FALSE-ACCEPT-UB95"] = None
            metrics["M-TAU-LADDER"] = {str(t): None for t in TOL_LADDER}
        metrics["M-INTERIOR-ONLY-FAILS"] = rows[0]["n_items_invalid_interior_only"]
    metrics["M-LIVE-POS-CHANGE"] = pos_changed
    metrics["M-LIVE-NULL-CHANGED"] = null_changed

    decision = decide(rows, cold_batch_gets, n_admitted)
    metrics["decision"] = decision
    metrics["gates"] = {
        "V3_seed_liveness": {"n_live_hosts": len(live_hosts), "pass": len(live_hosts) >= MIN_HOSTS},
        "V3b_census_min_admitted": {"n_admitted": n_admitted, "min": MIN_ADMITTED,
                                    "pass": n_admitted >= MIN_ADMITTED},
        "V3c_coverage_definitional": {"n_paths": n_admitted, "n_admitted": n_admitted,
                                      "pass": True},
        "V4_budget": {"total_gets": GET_LEDGER["n"], "ceiling": TOTAL_GET_CEILING,
                      "pass": GET_LEDGER["n"] <= TOTAL_GET_CEILING},
        "V6_denominator": {"cold_batch_gets": cold_batch_gets, "n_admitted": n_admitted,
                           "pass": cold_batch_gets > 0 and n_admitted > 0},
        "V10_envelope": {"elapsed_s": elapsed(), "budget_s": MODULE_WALL_BUDGET_S,
                         "pass": elapsed() <= MODULE_WALL_BUDGET_S},
    }
    (der / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    (der / "decision.json").write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"stage": "live", "outcome": decision["outcome"],
                      "n_admitted": n_admitted, "n_union": len(union_pages),
                      "cold_batch_gets": cold_batch_gets, "cycles": len(rows),
                      "invalid_pages": len(invalid_pages),
                      "gets": GET_LEDGER["n"], "elapsed_s": round(elapsed(), 1)}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["controls", "all"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--sleep", type=float, default=0.0)
    ap.add_argument("--cycles", type=int, default=PLANNED_CYCLES)
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.stage == "controls":
        return _run_controls(out_dir)
    rc = _run_controls(out_dir)
    if rc != 0:
        return rc
    return _run_live(out_dir, args.sleep, args.cycles)


if __name__ == "__main__":
    raise SystemExit(main())
FROZEN_CODE_END

## 11. Decision rule and gates

Evaluated in order; all arithmetic is performed by the frozen `decide()`.

- **G1 code identity.** V1 mismatch -> `status=MEASUREMENT_INVALID`,
  `outcome=NOT_APPLICABLE`.
- **G2 controls.** V2 any FAIL -> `MEASUREMENT_INVALID`, no census performed.
- **G3 seed liveness / census gate.** V3 or V4 FAIL ->
  `status=MEASUREMENT_INVALID`, `decision=NO_DATA`, **zero** revalidation GETs
  spent, the exact failing gate and host recorded. This is representation or
  substrate loss, never a negative.
- **G4 treatment object measured.** Fewer than one completed revalidation cycle
  (envelope exhausted first) -> `outcome=INCONCLUSIVE` with the exact budget cause;
  `decide()` returns `NO_DATA` for an empty row set and cannot yield `FALSIFIES`.
- **G5 budget / envelope / denominator.** V5, V8 or V6 FAIL ->
  `status=MEASUREMENT_INVALID`.
- **G6 primary decision.** With `cold = M-COLD-BATCH-GETS` and `N = n_admitted`:
  - `A_w` = per-item / no-sharing view pays iff
    `mean path length <= cold - max(0.10 * (cold/N), 0)`, i.e.
    `mean path <= 0.9 * cold/N`.
  - `B_w` = store / sharing view pays iff
    `K_w <= cold - max(0.10 * cold, 5.0)`.
  - `SUPPORTS` iff `A_w` **and** `B_w` at every measured cycle.
  - `FALSIFIES` iff neither `A_w` nor `B_w` at any measured cycle.
  - `MIXED` otherwise.
  - The same partition is reported for the no-sharing accounting as `S-NOSHARE`.

  **Identifiability note (frozen, not a post-hoc rescue).** `K <= sum_i len(path_i)
  = N * mean path`, so `A` paying implies `B` paying, and `FALSIFIES` reduces to `B`
  failing. The only `MIXED` sub-state this experiment can produce is "aggregate pays
  through cross-item page sharing, per item does not pay". The cross-cycle
  disagreement sub-state is certified by canary but cannot be produced by a frozen
  store page set, and is therefore not relied upon.

  `MIXED` is decision-relevant, not a non-result: it bounds the mechanism to
  multi-item workloads with a stated reuse density.

Always reported separately and never collapsed: the descriptive
`B-COLD-BFS-PER-ITEM` ordinal statistics, `B-COLD-PARENT-START`,
`M-STORE-SHARING-FACTOR`, `M-REUSE-ITEMS-PER-PAGE`, `M-BREAK-EVEN-CYCLES`,
`M-BREAK-EVEN-DENSITY`, the per-site table (per host: admitted, discovered, GETs,
deep density, sharing factor), `M-ENDPOINT-GETS` with `M-INTERIOR-ONLY-FAILS`, the
invalidation counts/rates, `M-STORE-PAGE-SECONDS`, `M-HAZARD-RATE-UB95`,
`M-PAGE-INVALID-UB95`, `M-FALSE-ACCEPT-UB95`, the `M-TAU-LADDER`,
`M-LIVE-POS-CHANGE`, `M-LIVE-NULL-CHANGED`, and `M-CENSUS-OVERLAP-PARENT208`.
Guard and fallback outputs inform the product action; they never overwrite the
primary label, and the DIRECTOR may bound the claim more narrowly than either.

## 12. Measurement validity gates

- **V1 code identity** - reconstructed module sha256 == `DERIVED_SHA256`.
- **V2 controls gate** - all fifteen offline controls PASS before the census.
- **V3 live seed liveness** - each live host seed returns 200; a failing host is
  excluded with its recorded error; fewer than `MIN_HOSTS = 2` live hosts fails.
- **V4 census gate before the ladder** - `n_admitted >= MIN_ADMITTED = 40`,
  `M-COLD-BATCH-GETS > 0`, coverage definitional (`n_paths == n_admitted`).
- **V5 budget** - `M-TOTAL-GETS <= TOTAL_GET_CEILING = 3200`.
- **V6 denominator guard** - `M-COLD-BATCH-GETS > 0` and `n_admitted > 0` before any
  thresholding; no `0/0` enters `decide()`.
- **V7 session-scale bound** - every change/dead/moved/false-accept statement and
  every `tau` value is bounded to the measured session horizon; no day-scale claim.
- **V8 envelope** - module wall clock `<= MODULE_WALL_BUDGET_S = 620 s`; per-host
  crawl `<= CENSUS_HOST_BUDGET_S = 100 s` with `time_truncated` reported; a cycle is
  started only if the measured per-GET latency implies it finishes inside the
  remaining budget. Rationale: the harness runs the EXECUTE agent under
  `SPIDER_MODEL_MAX_RUNTIME_SECONDS = 1200 s` with TERM/KILL to the whole process
  group, and on timeout executes `git reset --hard` + `git clean -fd`, so an
  over-running measurement is destroyed rather than recorded.
- **V9 decision determinism** - `decide()` inputs are written to
  `derived/metrics.json` and `raw/cycle_XX.jsonl`, so recomputation is exact and
  offline.
- **V10 live change-detector sensitivity** - at least one pre-registered volatile
  URL must change; otherwise a zero-event hazard observation is labelled
  `VACUOUS-RISK` and never reported as "nothing changes". A stable control that
  changes is reported as a spurious-firing alarm. Neither is a scientific negative.
- **V11 survivor conditioning disclosure** - `M-DEAD-RATE` and
  `M-FALSE-ACCEPT-NAIVE` are conditional on surviving the census; pages that died
  or were delinked before the census are not observable by construction. The
  pre-census loss is reported as `M-CENSUS-OVERLAP-PARENT208` with the parent's
  29/208 miss rate cited as prior evidence that this conditioning is material. No
  pre-census hazard statement may be derived here.
- **V12 accounting reconciliation** - reported store cost, physical GET spend and
  both accountings are recorded and reconciled; reporting one while spending the
  other is a gate failure.

## 13. Frozen non-outcome expectations (arithmetic, not measurement)

From the bound frozen frames only (`EXP-FRONTIER-38164611798/raw/structural.jsonl`
and `EXP-FRONTIER-38188815194/run/raw/paths.jsonl`):

- 4-host crawl: `n_discovered = 250 + 250 + 176 + 250 = 926`;
  hop>=3 URLs `= 220 + 9 + 36 + 160 = 425`; the parent's stricter 5-channel
  state-carrying census admitted 208 of them.
- Parent's 179 recovered chains: `sum|path| = 788`, `|union| = 201`,
  distinct interior pages `= 25`, mean path `4.4022`. Therefore
  `|union| / cold = 201/926 = 0.217` and the sharing factor is `~3.9`, i.e. the
  parent's *aggregate* expectation of `reval_unique_gets ~ 931` is a no-sharing sum,
  not the quantity its own metric defines.
- A frame on which the deep stratum is ~46% of the crawl (425/926) gives
  `cold/N ~ 2.2` while mean path ~4, so `A` is expected to fail and `B` to succeed.

These are priors computed from already-published raw evidence. They are recorded so
that the tilt is disclosed, not so that it can be used as a substitute measurement.

## 14. Satisfiability self-disproof (adversarial)

1. **Decision-rule reachability.** All five decision-function states were executed
   at DESIGN under the scoring code: `SUPPORTS`, `MIXED` (aggregate-pays /
   per-item-fails), `MIXED` (cross-cycle disagreement), `FALSIFIES`, `NO_DATA`.
   The three operational branches were also executed: census-gate FAIL aborted
   before any revalidation GET; envelope exhaustion produced 0 cycles and `NO_DATA`;
   a forced control FAIL returned rc=1 and wrote no census file. Population-level
   reachability: `A and B` paying requires a crawl dominated by wide shallow
   strata; `B` paying while `A` fails is the expected state here; `B` failing
   requires paths that barely share. No branch is empty and none is engineered.
2. **Measurement prerequisites.** Every prerequisite was exercised at DESIGN: all
   four bound seeds HTTP 200 with byte counts; three positive-control candidates
   observed changing within 2 s; two null-control candidates observed stable;
   measured GET latency 0.02-0.36 s; the frozen module compiles, passes 15/15
   offline controls, and completed the entire census -> store -> cycles -> decide
   path in a redirected copy against a locally generated 297-URL synthetic site
   (96 admitted, 96/96 coverage, 201 union pages, sharing factor 1.910, 3 cycles,
   `MIXED`, `M-TOTAL-GETS` 936, envelope/budget/denominator gates PASS). No pip
   install, model endpoint, browser, Docker or credential is required. All bound
   reference files exist with recorded hashes.
3. **Baseline identifiability.** Seven distinct comparators; the floor-cost
   competitor (naive replay) is included and instrumented for safety rather than
   dismissed; the strongest fair alternative is measured live on the same
   population with the same ledger; `B-COLD-PARENT-START` bounds generality;
   `B-COLD-BFS-PER-ITEM` is demoted to descriptive because it is satisfied by
   construction; both decision comparisons use the same 10% material margin so no
   comparison can be won by a 1% difference.
4. **Control sensitivity.** Every control fires in both directions under the scoring
   code, with observed DESIGN values recorded in section 15; V2 makes a control
   failure a hard gate; the live positive/negative control pair makes a
   zero-event hazard observation interpretable in both directions (V10).
5. **Treatment liveness.** The treatment transaction was executed end to end at
   pre-freeze cost offline, including every abort path; the live path's BFS policy
   is the parent's transport helpers verbatim; the module is pinned by
   `DERIVED_SHA256` and re-pinned at EXECUTE by V1.
6. **Freeze artifacts bound.** Ten mutable local files whose identity can change
   the interpretation are listed in `spec.freeze_artifacts` and section 19, all
   verified to exist at freeze time; the executed module's identity is pinned by
   `DERIVED_SHA256` against this preregistration, and this preregistration is
   hashed in `freeze.json.hashes`.

## 15. DESIGN pre-freeze probes (observed values)

Cheap and non-outcome-bearing. No outcome-bearing measurement was run: no frame
page was crawled, no store was built, no revalidation cycle was executed, and no
decision-relevant quantity of the live experiment was observed.

- **Offline controls probe**: `<frozen module> --stage controls` ->
  `{"stage": "controls", "all_pass": true, "n": 15, "failed": []}` (in-process
  fixture only). Observed: parent chain `["/", "/a.html", "/item.html"]`;
  `C-STORE-DEDUP-ACCOUNTING` `|union|=5 < sum|path|=6`, sharing factor 1.2;
  `C-REVAL-NOCHANGE` all `UNCHANGED`; `C-REVAL-CHANGE-DETECT` the mutated endpoint
  `CHANGED` and its sibling `UNCHANGED`; `C-LIVENESS-404` `DEAD`;
  `C-REVAL-MOVED-REDIRECT` `MOVED`; `C-HAZARD-BOUND-RULE3` Poisson `0.003` at zero
  events vs `0.005` at five; `C-WILSON-BOUND-DIRECTION` `0.0095 < 0.0357 < 0.105`;
  `C-TAU-LADDER-MONOTONE` strictly increasing; decision canaries
  `SUPPORTS`, `MIXED`, `MIXED`, `FALSIFIES`, `NO_DATA`.
- **End-to-end treatment-liveness probe** (temporary redirected copy, local
  synthetic site): `{"stage": "live", "outcome": "MIXED", "n_admitted": 96,
  "n_union": 201, "cold_batch_gets": 297, "cycles": 3, "invalid_pages": 0,
  "gets": 936, "elapsed_s": 5.0}`; `a_pays=[false,false,false]`,
  `b_pays=[true,true,true]`, `M-STORE-SHARING-FACTOR=1.910`,
  `M-REUSE-ITEMS-PER-PAGE=0.914`, `M-ENDPOINT-GETS=96`,
  `M-INTERIOR-ONLY-FAILS=0`, `M-LIVE-POS-CHANGE=true`,
  `M-LIVE-NULL-CHANGED=false`, envelope/budget/denominator gates PASS.
  Abort paths: census-gate FAIL -> `NO_DATA` with 135 GETs and zero cycles;
  envelope exhaustion -> 0 cycles, `NO_DATA`; control FAIL -> rc=1, no census.
- **Geometry probe on prior raw evidence**: from the parent's
  `run/raw/paths.jsonl`, `sum|path| = 788`, `|union| = 201`, interior `= 25`,
  mean `4.4022`, `|union|/926 = 0.217`.
- **Seed and control preflight** (single vantage, 2026-10-17; 12 GETs total):
  all four seeds 200 - `doc.rust-lang.org/stable/book/` 22496 B,
  `pandas.pydata.org/docs/` 22046 B,
  `docs.readthedocs.io/en/stable/` 24433 B with final URL
  `https://docs.readthedocs.com/platform/stable/` (confirming the post-redirect
  anchor rule), `docs.pytest.org/en/stable/` 31975 B. Positive candidates all
  changed within 2 s: cloudflare trace 217 B, `api.github.com/rate_limit` 424 B,
  timeapi 220 -> 219 B. Null candidates stable within 2 s: `example.com` 577 B,
  `iana.org/domains/reserved` 10499 B. A news-RSS candidate was measured stable over
  2 s and is therefore **not** registered as a positive control. GET latency
  0.02-0.36 s.
- **Frame integrity**: all ten `freeze_artifacts` paths verified present;
  recorded prefixes `c8215d69` (parent admitted items), `2afe65b6` (frozen 20-host
  structural frame), `95a3f15f` (parent census structural frame), `d51568c5`
  (parent census metrics), `b9b2efdc` / `75a01d49` / `f18e5b55` (reference
  modules), `5192435b` (parent recovered chains), `eb076db8` / `7cd7a1a6` (parent
  result/audit).
- **Process hygiene**: no orphaned prior `execute_module` process exists; only the
  current session's own process tree.

## 16. Budget, schedule, envelope, and stop/pivot triggers

- `TOTAL_GET_CEILING = 3200`. Expected: census <= 1000 (reference 926); at most 3
  cycles of `K` distinct pages each; 6 control probes per observation; the
  endpoint-only arm costs **zero** additional GETs. Design estimate at the measured
  latency: 2200-2600 GETs.
- Module wall clock `<= 620 s`, inside the harness's 1200 s process envelope,
  leaving the producing agent ~500-600 s to write `result.json`, `report.md` and
  `provenance.json`. Per-host crawl deadline 100 s.
- Nominal ladder: 3 revalidation cycles with 60 s inter-cycle sleeps; actual
  elapsed times are recorded per cycle and per page exposure is computed from
  recorded timestamps, never from wall-clock attainment of a nominal target.
- Zero model calls, zero credentials, zero browser, zero Docker.
- **Stop/pivot trigger (from the mandate)**: this is the single funded attempt.
  A second MEASUREMENT_INVALID or a null result on this thread parks the
  full-path persistence subthread in favour of a genuinely orthogonal basin. The
  module never enlarges the ladder or repeats the census to obtain a favourable
  population.
- **Measurement-invalid signature**: V1-V6, V8 or V12 FAIL ->
  `MEASUREMENT_INVALID`, never a negative; G4 -> `INCONCLUSIVE`.

## 17. Validity threats, representation loss, and disclosed a-priori tilt

- **Single vantage.** No external validity across ASN, geography or egress IP
  (inherited substrate limitation).
- **Session regime only.** Change/dead/moved/false-accept rates and every `tau`
  value are bounded to the measured horizon (V7). The legacy program established
  that day-scale staleness is undecidable on committed corpora.
- **Survivor conditioning (V11).** The store's dead rate is conditional on the page
  having survived the census. The parent's 29/208 miss rate is prior evidence that
  pre-census loss is substantial on this frame, so `M-DEAD-RATE` must not be read as
  a full lifetime hazard.
- **Byte-level invalidation is an upper-bounded proxy.** A sha256 difference fires
  on any byte change, including injected timestamps or tokens, and therefore
  over-counts semantic invalidation; a content-type switch is separated
  (`CHANGED_CT`), and `DEAD` / `MOVED` are reported separately. ETag and
  Last-Modified are recorded per page for a future validator-level analysis but are
  not used in this packet's decision, because conditional GETs would change the
  cost model and introduce server-dependent behaviour.
- **Unconditional GETs.** No `If-None-Match` is sent, so a page may be served a
  different CDN variant across cycles. This is the conservative choice for the
  treatment (more bytes fetched) and is stated.
- **Budget/time truncation bias.** A crawl truncated by `BUDGET` or by
  `CENSUS_HOST_BUDGET_S` loses the deepest unfetched nodes first, which raises
  `K/N` and would flatter the store. Per-host `time_truncated` and discovered vs
   fetched counts are reported so the bias is visible; `BUDGET = 250` is held at the
  parent's value specifically to avoid changing the population shape.
- **Cold baseline is the strongest fair alternative, not the cheapest one.** It is a
  full host sweep from a minimal-hop seed. A cheaper cold start
  (`B-COLD-PARENT-START`) is reported to bound generality, so a positive aggregate
   verdict cannot be read as "persistence always wins".
- **Cost model excludes model work.** Web work only (section 1).
- **The endpoint-only ablation is a derived sub-arm.** It reuses the same cycle rows
   rather than independently re-sampling, so its detection set is exact but not
   independently replicated.
- **Disclosed empirical tilt.** With the frozen frame's arithmetic the expected
  branch is `MIXED`: `K` is expected to be far below `0.9 * cold` (union ratio
  0.217-0.5) while mean path ~4 is expected to exceed `0.9 * cold/N` (~1.96 on this
  4-host frame). `SUPPORTS` requires a population whose crawl is dominated by wide
  shallow strata, and `FALSIFIES` requires paths that barely share. All three are
  certified reachable by canary; none is engineered; no pre-freeze outcome fraction
   of the live experiment was measured. The reported quantities (sharing factor,
   reuse density, break-even cycles, per-site table, hazard bound, tau ladder,
   interior-only failures) carry decision content even if the label is predictable.
- **One-shot cold cost estimate.** `M-COLD-BATCH-GETS` comes from a single crawl
   with no replication; it is reported next to the frozen 926 reference and next to
   discovered-vs-fetched counts so drift is visible.

## 18. Consequences

- `SUPPORTS` -> build the persisted deep-path store with a measured maintenance
  policy; the aggregate economics say the store beats re-derivation by the measured
  factor, and the revalidation policy is set by `M-TAU-LADDER` rather than assumed.
- `MIXED` + hazard bound certifying the largest ladder entry -> build the store and
  use naive replay inside a session (0 revalidation GETs) with an explicit staleness
  budget; add revalidation only where `M-INTERIOR-ONLY-FAILS` or the bound requires
  it.
- `MIXED` + bound too coarse to certify any tolerance -> build the store and treat
  session-scale staleness as `UNKNOWN` (the architecture's preferred answer) rather
  than assuming safety.
- `MIXED` (aggregate only) -> do not build a general per-item persistence store;
  build it for multi-item workloads above the measured reuse density, and prefer
  endpoint-level liveness (1 GET/item) when `M-INTERIOR-ONLY-FAILS` is zero.
- `FALSIFIES` -> cold re-derivation (or a different representation) is at least as
  cheap as full-path persist+revalidate including the fully-loaded per-item cost;
  do not build the store and park the full-path persistence subthread. No discovery
  rerun and no ladder enlargement.
- `INCONCLUSIVE` / `MEASUREMENT_INVALID` -> build nothing; record the exact gate and
  what would change it. No claim promotion under any branch. `C-CROSSSITE` remains at
  its prior effective status; the cross-site *variance* table may be cited by
  `C-FRESHNESS` / `C-PRODUCT-ECON` consumers as descriptive Web-work economics with
  no epistemic update.

## 19. Freeze artifacts

Interpretation dependencies, exact repository-relative paths hashed into
`freeze.json.artifact_hashes`:

1. `research/experiments/EXP-FRONTIER-38184956362/raw/items.jsonl`
   (`c8215d69...`) - parent's admitted list; the only remaining reference to the aged
   population, used solely for `M-CENSUS-OVERLAP-PARENT208`.
2. `research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl`
   (`2afe65b6...`) - frozen 20-host frame: per-host reference counts, seeds, hops,
   ordinals.
3. `research/experiments/EXP-FRONTIER-38184956362/raw/structural.jsonl`
   (`95a3f15f...`) - parent's census structural frame; audit traceability.
4. `research/experiments/EXP-FRONTIER-38184956362/derived/metrics.json`
   (`d51568c5...`) - parent census metrics.
5. `research/experiments/EXP-FRONTIER-38184956362/execute_module.py`
   (`b9b2efdc...`) - reference BFS/census implementation.
6. `research/experiments/EXP-FRONTIER-38164611798/execute_module.py`
   (`75a01d49...`) - base reference BFS implementation.
7. `research/experiments/EXP-FRONTIER-38188815194/execute_module.py`
   (`f18e5b55...`) - the parent frozen module whose transport helpers are copied
   verbatim and whose accounting defect is repaired here.
8. `research/experiments/EXP-FRONTIER-38188815194/run/raw/paths.jsonl`
   (`5192435b...`) - parent's 179 recovered chains: geometry probe and accounting
   evidence.
9. `research/experiments/EXP-FRONTIER-38188815194/result.json` (`eb076db8...`).
10. `research/experiments/EXP-FRONTIER-38188815194/audit.json` (`7cd7a1a6...`).

The executed module is additionally pinned by `DERIVED_SHA256` against section 10
of this preregistration.

## 20. Mandate fidelity and unresolved at freeze

**Mandate fidelity.** (1) *Re-census the frame before re-freezing*: satisfied by
registering the admitted set from the live crawl that also supplies the cold
baseline, with definitional coverage and the parent's list demoted to a covariate;
the frozen margin rule is reapplied to live values, exactly as "register a fresh
admitted set" authorizes. (2) *Reconcile the nominal ladder with the harness
envelope*: satisfied by a short opportunistic ladder, a 620 s module budget inside
the 1200 s envelope, a per-host census deadline, and a ledger-bounded cycle
admission rule, with the harness behaviour (group kill plus `git reset --hard` /
`git clean` on retry) cited as the reason. (3) *Evaluate the V3 gate before spending
the ladder*: satisfied by V4, which is evaluated after the census and before any
revalidation GET; the executed abort path confirms zero revalidation GETs are spent
when it fails. (4) *Revalidation GETs/bytes/elapsed and session-scale
change/dead/false-accept rates decide the two comparisons, with the endpoint-only
ablation as fallback*: satisfied - the cost quantities feed G6 exactly as specified,
the hazard quantities bound whether revalidation is needed at all
(`M-TAU-LADDER`), and `A-ENDPOINT-ONLY-REVALIDATE` is executed exactly with
`M-INTERIOR-ONLY-FAILS` as its residual. The only deliberate deviation is that the
mandate's literal constants `833.4` and `4.007` cannot be carried over, because the
mandate itself states they "no longer denote a live population"; the same frozen
margin rule is applied to live-derived values instead, and both the parent's
constants and the live values are reported side by side.

**Unresolved at freeze (for EXECUTE/AUDIT).** Live `M-COLD-BATCH-GETS`,
`n_admitted`, `K`, mean path, sharing factor, reuse density, break-even cycles and
density, per-site variance, all invalidation counts and rates, the hazard bounds,
the tau ladder, interior-only failures, and the live control-probe outcomes are
UNKNOWN by construction. No pre-freeze outcome was observed.