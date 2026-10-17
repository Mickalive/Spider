# EXP-FRONTIER-39039638199 preregistration

Status: DESIGN, not yet frozen. Frozen inputs are immutable once
`scripts/freeze_experiment.py` writes `freeze.json`.

Lane: `frontier`. Design contract: v2. Director target claim: `C-WEB-DYNAMICS`.

---

## 1. Identity, claim binding, and scope

- `experiment_id`: `EXP-FRONTIER-39039638199`
- `lane`: `frontier`
- `claim_ids`: `["C-WEB-DYNAMICS"]` (frontier charter priority claim;
  `research/lanes/registry.json`)
- `director_mandate`: `CONTINUE`, claim `C-WEB-DYNAMICS`, cycle `39038720186`,
  `request.json#director_mandate.allocation`.
- `parent_handoff`: `research/experiments/EXP-FRONTIER-38940047535/handoff.json`
  sha256 `6ad3d1291db49d05ecafd88ae58c4ce0d27f633f9d3dc01a62f741dfd5dd555e`,
  disposition `USE` (continuity evidence only; its `next_question` is advisory
  and its PARK instruction on the persistence-economics subthread is honoured).

Scope, stated as exclusions because they are the mandate's exclusions and also
because the parent thread is parked:

- **no** persistence store,
- **no** revalidation ladder and no multi-cycle measurement,
- **no** cold-vs-store or any other cost comparison, and no GET economics at all,
- **no** model calls, tokens or latency accounting,
- **no** re-run of the parked C-CROSSSITE persistence-economics design.

What this packet does measure: the per-page probability that the server-rendered
HTML text of a credential-free documentation page changes within a measured
session-scale separation, separately for a shallow stratum (`hop <= 2`) and a deep
stratum (`hop >= 3`), with censoring-aware one-sided bounds, plus a separately
reported page-gone channel.

---

## 2. Legacy and pre-2.0 disposition

**LEGACY: DISTINCT_EXTENSION** of the pre-2.0 frontier
`web-physics-volatility-freshness` thread, plus **REPLICATION** of one of its
instrument lessons, with **NO_MATCH** against the next-state precedents named in
the Director mandate.

The mandate screened only the compact legacy set. A targeted lookup of
`codex/legacy_artifact_index.json` for staleness / invalidation / freshness /
TTL / hazard / session / drift / age surfaces a substantial pre-2.0 thread that
the compact set does not summarise, and the primary sources were read from the
pinned archive `.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md` (blob
`9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`). What it established, and how this
design differs:

### 2.1 `CENSUS_REPORT_V3.md` / `CYCLE_32968938133_REPORT.md` — sha `81aba1e898d96fe3c49ae9cd0f4ef00dfdad46a4` (artifact 4.1052/4.1053)

A census-first, **zero-network, structure-only** census over already-committed
corpora denied the days-to-weeks staleness question *structurally*: maximum
same-target revisit gap 0.021812 d (31.4 min), median gap 2707 ms, 26 separated
pairs (its own definition: Δt ≥ 300 s), expected events 26 versus a floor of 64
required. It also mined validation-tier priors: openlibrary double-reset drift
7/12 at seconds scale, and 62/62 placebo zero-drift pairs.

**Relation here — DISTINCT_EXTENSION.** That denial is a fact about *committed
bytes* and about the *days-to-weeks* band. This packet builds a new **live
longitudinal two-observation frame**, which is the single path the legacy cycle
report itself names as discriminating ("Exactly one discriminating path exists:
an authorized longitudinal collection"), and it scopes the estimand to the band
legacy actually measured mass for. Two concrete inheritances:

- `DT_MIN_S = 300 s` is not invented: 300 s is the legacy separated-pair
  threshold and is ~110× the legacy median revisit gap, so below it the
  instrument cannot separate page dynamics from navigation/reset noise.
- The seconds-scale drift prior (7/12 on a dynamic site) and the 62/62 placebo
  strata are carried as **priors, not evidence**, and are re-measured here by
  live controls rather than cited.

No day-scale claim is made, and the legacy contract's ban on seconds-to-days
extrapolation is honoured literally: every bound this packet produces carries its
measured window.

### 2.2 `results/intel/reproductions/cycle8/ttl_window1.json` — sha `43d21a4a384bc5a242c6bb6f4725e4093982f0fb` (artifact 4.443)

A frozen change-detection rule: *CHANGED iff ETag differs; if ETag is absent on
either side, CHANGED iff head-hash differs*, with two findings that matter: a
resource **varies bytewise under one unchanged ETag** (ETag-only detection is
demonstrably insensitive), and `httpbin /get` is volatile because it embeds a
per-request trace id (volatility without content change).

**Relation here — REPLICATION + REPAIR.** The lesson is replicated and made
load-bearing on real HTML: `ETag`/`Last-Modified` is recorded as covariate
`B-TRANSPORT-CHANNEL` and **never** defines an event; the event channels are
body-hash based. This packet additionally measures the *reverse* error, which the
legacy rule could not see: `M-CHANGE-ATTR-ONLY-<stratum>` counts pages that
changed bytewise without changing text, so the width of the primary channel's
blind spot is a reported quantity rather than an assumption.

### 2.3 `CHANGE_EVENT_TAXONOMY_V0.md` / `FRESHNESS_SIGNAL_CONTRACT_V0.md` — sha `f41395817d98f153f098df42cf2cd48f0052eceb` / `0a53685fd4188dfc17beefca9950c1e6921d4a39` (artifacts 4.1247/4.1248)

CE-1/CE-2/CE-3/CE-5 are the admissible environment-side classes; CE-4
(session/auth) is excluded by design; CE-6 (cosmetic churn below tolerance) is by
construction not an event; CE-5 (outage) must not be misread as staleness; and
seconds-scale extrapolation plus controller-side replica-store rates are declared
invalid as environment hazard.

**Relation here — ADOPTED AS THE EVENT TAXONOMY**, instantiated rather than
re-derived: text-channel change = CE-1/CE-2/CE-3; attribute/script-only churn =
CE-6, counted separately; 404/410 and 5xx = the death/availability channels, never
folded into the change rate; no CE-4 class exists because every fetch is a
credential-free GET with a canonical per-URL identity.

### 2.4 Intel TTL windows (artifacts 4.253/4.380/4.381/4.443-4.446, cycles 6-9)

Window 2 was repeatedly declared `NOT_EXECUTED_THIS_RUN` because it required a
≥ 24 h calendar gap that no cycle could wait inside its own harness, with a
window-regress cap of 3 windows.

**Relation here — this is the gap this packet attacks.** The `B-RETRO-LONG-DT`
channel obtains a longer-window two-observation comparison at **zero additional
waiting** by reusing the parent's already-frozen observation-0 hashes as a real
first observation. That is exactly the second longitudinal point the legacy
protocol was blocked from taking, and it is declared SECONDARY so it can never
manufacture a primary result.

### 2.5 Mandate-named precedents — NO_MATCH

`P2-WP002B` (901 true next-state transitions; rule DIM-ACC 0.6238 vs NN 0.6295 vs
shuffle 0.5706) and `P2-WP003B` (sha `f6cfdfc749cae9eb4d9fcc4b11b94b63a2bcfb6e`;
action-only MSE 0.756 vs full 0.735; pre-state mechanics < 3 % additional
variance) are one-step next-state prediction and action-feature mechanics on
committed trajectory corpora. `P2-WP003` (sha `292e3243d9bc7a3b88712788a7cb05709eb74eb9`)
is `MEASUREMENT_INVALID` for `prev_action` leakage. None measures per-page
invalidation probability over a wall-clock window on a live frame; none is
repeated here.

### 2.6 Research 2.0 non-duplication

`EXP-FRONTIER-37950626378` (hop-scaling cost law) is a different estimand.
`EXP-FRONTIER-38184956362` (bounded negative, 0/208 deep items via site-native
discovery) is inherited as accepted evidence and **not** re-run.
`EXP-FRONTIER-38940047535` produced no hazard quantity at all (every `M-CHANGE-*`,
`M-DEAD-*`, `M-HAZARD-*`, `M-TAU-LADDER` is null), so nothing here repeats it.

---

## 3. Parent-handoff disposition (four-way, preserved)

**established**

- The parent's scoring instrument was sound (code identity, 15/15 offline
  controls, 4/4 seed liveness), so its failure was not instrumental; the audit
  ceiling supports no statement about persistence economics in either direction
  and `C-CROSSSITE` stays `HYPOTHESIS`.
- Definitional coverage held (`n_paths == n_admitted`), so the
  EXP-FRONTIER-38188815194 aged-external-list miss mode is structurally
  eliminated.
- The blocking defect is **census policy**, not runtime: fetching stopped when
  discovery hit `BUDGET=250`; 363 of 402 discovered deep URLs (90.3 %) were never
  fetched; admitted items came from 2 of 4 hosts.
- 926 is a **discovered-URL count, not a GET count** (302 GETs were spent under
  the identical policy), and the parent's cited `economics.jsonl` does not exist in
  the repository.
- Design satisfiability on the bound seeds was never demonstrated: treatment-liveness
  probes ran only on synthetic sites (`n_admitted` 96/120) while the review states
  "No frame page was crawled for this review".

**rejected**

- Site-native discovery: 0/208 deep state-carrying items within ≤ 3 charged GETs
  on that substrate class (inherited accepted evidence). Does not close other
  axes.
- Any reuse of 926 / 833.4 / 4.006731 as GET-based thresholds. No cost quantity is
  computed here at all, so the unit defect cannot recur.
- The parent's `MIN_ADMITTED=40` reachability claim. No threshold is inherited
  from it.

**unknown addressed here**

- VN-7 / U-1 / U-2: no invalidation observation of any kind; deep population never
  fetched; page-gone indistinguishable from unreachable. Addressed by the
  fetch-complete frame, the two-observation diff and the separate death channel.
- U-5: reachability of any census population gate under any policy on these seeds.
  Addressed by DESIGN probes on the bound hosts themselves.
- U-3: all hazard metrics null. This packet's estimand.
- U-4 (VN-4 counterfactual arithmetic, non-decisional): not carried forward; no
  arithmetic substitute appears anywhere in this design.

**do_not_assume carried forward**

- `MEASUREMENT_INVALID` is not falsification of persistence economics or of
  `C-CROSSSITE`.
- A zero here is not "nothing changes". It is interpretable only if the positive
  control fired, both null families stayed silent and the frame gate passed — and
  even then it is a **bound at a measured window**, never an absence claim.
- Nothing here extrapolates to the days-to-weeks band, to JavaScript-rendered or
  authenticated pages, or to another egress vantage.
- A certified tolerance is not a shipped freshness mechanism.
- Do not re-run or weaken the parked persistence-economics design.

---

## 4. What is repaired relative to the parent packet

| # | Parent defect | Repair | Verified at DESIGN |
|---|---|---|---|
| R1 | Discover-until-budget starvation: 90.3 % of discovered deep URLs never fetched; deep stratum admitted from 2 of 4 hosts | Stratum-reserved level-ordered BFS (`SHALLOW_CAP_PER_HOST=140` for levels 0-2, `DEEP_CAP_PER_HOST=220` for levels ≥ 3); when the shallow budget is exhausted the sweep **skips** the level but keeps descending, so the deep stratum is always fetched | P8: deep 686 / shallow 421, 4 of 4 hosts in both strata; tiny-cap smoke: 4 of 4 hosts still reached hop 3, 24/24 HTTP 200 |
| R2 | No arm separating page-gone from page-delinked from unreachable (parent U-2) | `M-DEAD-404-<stratum>` + `M-DEAD-UB95-<stratum>` as an independent channel; 429/403/503 as `M-RATE-LIMITED-<stratum>`; only 200-at-both pairs enter the change estimand | Offline control `C-CENSOR-404-DETECTED`; pipeline control `C-SUMMARY-CENSOR-AND-DEAD` |
| R3 | Live positive control never exercised (parent VN-7): all five control URLs fetched once, so a zero-event result would have been uninterpretable | 3 pre-registered volatile URLs + 2 static null anchors fetched at **both** observations, plus an in-frame self-pair determinism null over 10 census pages | P4 candidate pool probed with the exact detector (3 of 6 fired, disclosed in §15) |
| R4 | Design satisfiability shown only on synthetic sites (audit `AUD-DESIGN-SATIFIABILITY-GAP`) | Four DESIGN probes on the **bound hosts**, including a full-cap observation-0 sweep of the exact frozen module | P2 23/24 deep URLs 200; P3 24/24 shallow 200; P5 10.05 GET/s; P8 1119 rows in 37.26 s |
| R5 | Envelope risk from in-process waiting (parent-of-parent used a 3000 s ladder against `SPIDER_MODEL_MAX_RUNTIME_SECONDS=1200`) | Separation frozen at 360 s with hard bounds [300, 900] s; per-stage checkpoints; measured throughput basis; GET ceilings per observation; observation-0 artifacts written **before** the sleep | P5 + P8 throughput basis; §16 budget table |

---

## 5. Question and hypotheses

**Question.** Is session-scale invalidation hazard concentrated in the deep
stratum (`hop ≥ 3`) rather than the shallow stratum (`hop ≤ 2`), and can a
two-observation census diff on a fetch-complete frame certify, or explicitly
refuse to certify, named zero-GET staleness tolerances for the two strata inside
one session?

- **H1 (certification).** Over a measured separation `DT ≥ 300 s`, the per-page
  probability that the server-rendered HTML text of a credential-free GET-only
  documentation page changes is small enough that a zero-GET intra-session
  freshness guard is unnecessary, at a named certified level `L ∈ {0.01, 0.02,
  0.05}`, separately per stratum.
- **H2 (mandate contrast).** Hazard is **not** concentrated in the deep stratum:
  the one-sided exact binomial p-value for `p_deep > p_shallow` is > 0.05 and both
  stratum bounds sit at or below the same certified level.
- **H3 (bounded negative, equally acceptable).** The deep bound exceeds the
  shallow certified level, or the contrast rejects → a guard is required only
  where `hop ≥ 3` state is reused.
- **H4 (declared UNKNOWN, not tested).** The days-to-weeks band; JavaScript-rendered
  content; authenticated pages; any vantage other than this runner's egress.

**Falsifier.** H1 is falsified for a stratum when its exact one-sided 95 %
Clopper-Pearson upper bound exceeds 0.05, or its observation-1 censoring fraction
exceeds 0.20, or its eligible paired `n` is below 60. H2 is falsified when the
exact one-sided p ≤ 0.05. The measurement is **invalidated, never falsified**, when
the positive control does not fire, any null control or self-pair changes, a seed
fails, the separation falls outside [300, 900] s, or the GET ceiling is exceeded.

---

## 6. Population, frame, and substrate

Seeds (frozen, identical to the parent so the documented 402-deep-URL topology
remains comparable design-time evidence):

```
doc.rust-lang.org    https://doc.rust-lang.org/stable/book/
docs.pytest.org      https://docs.pytest.org/en/stable/
docs.readthedocs.io  https://docs.readthedocs.io/en/stable/
pandas.pydata.org    https://pandas.pydata.org/docs/
```

Crawl policy (frozen):

| constant | value | role |
|---|---|---|
| `DEPTH` | 6 | maximum BFS level |
| `SHALLOW_MAX_HOP` | 2 | `hop ≤ 2` = SHALLOW, `hop ≥ 3` = DEEP |
| `SHALLOW_CAP_PER_HOST` | 140 | fetch budget for the shallow stratum |
| `DEEP_CAP_PER_HOST` | 220 | fetch budget for the deep stratum |
| `PER_HOST_WALL_S` | 150.0 | per-host sweep wall budget |
| `GET_CEILING_OBS0` | 1500 | observation-0 GET ceiling |
| `GET_CEILING_OBS1` | 1600 | observation-1 GET ceiling |
| `GET_CEILING_TOTAL` | 3200 | total live GET ceiling |
| `OBS1_TARGET_CAP` | 1200 | safety valve on the observation-1 target list |
| `SEPARATION_S` | 360.0 | requested in-process separation |
| `DT_MIN_S` / `DT_MAX_S` | 300.0 / 900.0 | eligible-pair floor / protocol ceiling |
| `MODULE_WALL_BUDGET_S` | 900.0 | module wall budget |
| `REQUEST_TIMEOUT` | 12.0 | per-GET timeout |
| `MAX_BODY_BYTES` | 8000000 | body truncation ceiling |
| `WORKERS` / `PER_HOST_CONCURRENCY` / `PER_HOST_SPACING_S` | 6 / 2 / 0.10 | transport concurrency and politeness |
| `UA` | `spider-r2/1.0` | identical to the parent's UA, required for the retrospective channel |

Link policy is the parent's, reused verbatim: same-host `<a href>` only, assets
excluded by extension list, `norm()` canonicalisation, `DEPTH` levels. Bodies are
hashed and link-extracted at fetch time and then dropped, so peak memory is
independent of frame size.

**Population bound (arithmetic, from the DESIGN sweep, not from the parent).**
Per-host shallow GET counts in the parent (10 / 100 / 140 / 13) are all ≤
`SHALLOW_CAP_PER_HOST`, so the frozen shallow budget never truncates below the
set of fetches that generated the parent's documented discovery, and the
discovery set is a superset of the parent's 402 deep URLs. Measured directly
(P8): deep 686, shallow 421.

---

## 7. Arms and channels (stable ids)

There is no treatment/comparator pair in the classical sense; the arms are
**channels** over one live frame, and the comparators are listed in
`spec.json#baselines`.

| id | definition | role |
|---|---|---|
| `CH-TEXT` (PRIMARY) | `sha256(canon(body))`, where `canon` removes comments, `<script>`, `<style>` and all tags, unescapes six entities, collapses whitespace, lowercases | defines the certified event |
| `CH-BYTE` | `sha256(full body)` | conservative sensitivity channel |
| `CH-TRANSPORT` | `ETag` / `Last-Modified` difference | covariate only, never a decision variable (§2.2) |
| `OBS0` | fetch-complete census over the frozen seeds with the frozen policy | registers the frame and its hop labels |
| `OBS1` | re-fetch of **exactly** the observation-0 admitted set after the separation | produces the pairs |
| `OBS-SELFPAIR` | 10 admitted pages fetched twice inside observation 1, gap ≤ 5 s | in-frame detector-noise null |
| `OBS-RETRO` | re-fetch of the 292 URLs the parent already fetched, compared to the parent's frozen `sha256` | **secondary** longer-window channel |
| `CH-DEAD` | observation-1 HTTP 404/410 | page-gone channel, right-censored for the change estimand |
| `CH-UNREACHABLE` | transport error, timeout, 429/403/503 | censored, reported separately |

---

## 8. Frozen metric ids

See `spec.json#metric_ids` for the complete list of 88 identifiers, which
EXECUTE, AUDIT and DIRECTOR must reuse verbatim. The load-bearing ones:

- frame: `M-N-ADMITTED`, `M-N-PAIR-DEEP`, `M-N-PAIR-SHALLOW`,
  `M-N-PAIR-EXCLUDED-BELOW-DT-MIN`, `M-GETS-OBS0`, `M-GETS-OBS1`, `M-GETS-TOTAL`
- primary: `M-CHANGE-TEXT-DEEP`, `M-CHANGE-TEXT-SHALLOW`,
  `M-HAZARD-TEXT-UB95-DEEP`, `M-HAZARD-TEXT-UB95-SHALLOW`,
  `M-CERT-LEVEL-TEXT-DEEP`, `M-CERT-LEVEL-TEXT-SHALLOW`
- sensitivity: `M-CHANGE-BYTE-*`, `M-HAZARD-BYTE-UB95-*`, `M-CHANGE-ATTR-ONLY-*`,
  `M-CHANGE-TRANSPORT-*`
- censoring and death: `M-CENSOR-FRAC-*`, `M-DEAD-404-*`, `M-DEAD-UB95-*`,
  `M-UNREACHABLE-*`, `M-RATE-LIMITED-*`
- window: `M-DT-MIN-S`, `M-DT-MEDIAN-S`, `M-DT-P90-S`, `M-DT-MAX-S`
- identifiability: `M-HOST-TABLE`, `M-HOSTS-WITH-BOTH-STRATA`,
  `M-HOST-CONC-MAX-*`, `M-CLASS-FRAC-*`, `M-CHANGE-BY-CLASS-*`
- contrast: `M-CONCENTRATION-P-ONE-SIDED`, `M-CONCENTRATION-DETECTED`,
  `M-CONCENTRATION-MDC-RATE`
- controls: `M-LIVE-POS-CHANGED`, `M-LIVE-POS-OK`, `M-LIVE-NULL-CHANGED`,
  `M-LIVE-NULL-OK`, `M-SELFPAIR-CHANGED`, `M-SELFPAIR-N`, `M-OFFLINE-CONTROLS-PASS`
- secondary: `M-RETRO-N-*`, `M-RETRO-CHANGE-BYTE-*`, `M-RETRO-UB95-*`,
  `M-RETRO-CERT-LEVEL-*`, `M-RETRO-INFO`

---

## 9. Frozen control ids

See `spec.json#control_ids` (44 identifiers). Families:

- **detector specificity** `C-DETECT-TEXT-INJECTION`, `C-DETECT-ATTR-ONLY`,
  `C-DETECT-SCRIPT-ONLY`, `C-CANON-IDEMPOTENT`, `C-LIVE-DETECTOR-ON-FIXTURE`
- **censoring** `C-CENSOR-404-DETECTED`
- **exact statistics** `C-CP-BOUND-N60`, `C-CP-BOUND-N150`, `C-CP-BOUND-N299`,
  `C-CP-BOUND-K1N400`, `C-CERT-LEVEL-LADDER`, `C-CONTRAST-POWER`
- **decision reachability** `C-DECIDE-*` (10) and `C-SUMMARY-*` (11)
- **live** `C-LIVE-POS-SENSITIVITY` (≥ 1 of 3 changes between observations),
  `C-LIVE-NULL-STABILITY` (0 of 2), `C-SELFPAIR-DETERMINISM` (0 of 10)
- **frame/transport** `C-FRAME-DEPTH-PRESENT`, `C-SEED-LIVENESS`,
  `C-LEDGER-RECONCILIATION`, `C-CODE-IDENTITY`
- **secondary** `C-RETRO-INSTRUMENT-ADMISSION`

Frozen control URLs (selection disclosure in §15):

```
pos:  https://www.cloudflare.com/cdn-cgi/trace
      https://api.github.com/rate_limit
      https://timeapi.io/api/Time/current/zone?timeZone=UTC
null: https://example.com/
      https://www.iana.org/domains/reserved
```

---

## 10. Frozen EXECUTE module

The exact module below is the frozen EXECUTE driver. It is stdlib-only,
credential-free, GET-only, single-vantage, and runs entirely in one process.
Extraction rule (identical to the parent packet's convention): the module is the
block of bytes strictly after the opening marker line and strictly before the
closing marker line that delimit it below — the opening marker line is the single
line reading FROZEN underscore CODE underscore BEGIN, and the closing marker line
is the single line reading FROZEN underscore CODE underscore END. These tokens are
deliberately written out in words here so that the only literal occurrences of
them in this file are the marker lines themselves, so a naive first-occurrence
extractor cannot pick up this paragraph. With `C = block.strip()`, then
`sha256(C)` must equal

```
DERIVED_SHA256 = 5d2509f691193c610a9797e4c473ee9425c010c1a4bd35f65b43e3aca672c573
```

`prereg.md` is itself hashed in `freeze.json.hashes`, so the module identity is
frozen even though it is not a separate repository file at freeze time. The module
additionally records its own self-hash into `derived/code_identity.json` and into
`derived/metrics.json` (`V1-CODE-IDENTITY` re-pins it at EXECUTE).

Interface: `--stage controls|all --out <dir> [--sleep S] [--smoke]`.
`--stage controls` runs the 35 offline controls only. `--smoke` stops after
observation 0 (used at DESIGN to verify the live path without creating any
two-observation pair). Outputs under `--out`: `raw/controls.jsonl`,
`raw/control_probes.jsonl`, `raw/census.jsonl`, `raw/obs1.jsonl`,
`raw/selfpair.jsonl`, `raw/retro.jsonl`, `raw/PROGRESS.json`,
`derived/metrics.json`, `derived/decision.json`, `derived/code_identity.json`.

FROZEN_CODE_BEGIN
#!/usr/bin/env python3
"""EXP-FRONTIER-39039638199 - session-scale invalidation hazard on a
fetch-complete documentation-Web census frame, stratified by hop depth, with
censoring-aware one-sided Clopper-Pearson bounds and a named tolerance
certification / refusal decision.

Frozen EXECUTE driver.  stdlib-only, credential-free GET-only, single egress
vantage, no browser, no JavaScript execution, no persistence store, no
revalidation ladder, no cold-vs-store cost comparison.

Stages:
  controls  offline in-process HTTP fixture canaries + exact-bounds canaries
            (no external network)
  all       controls -> obs0 fetch-complete census -> separation sleep ->
            obs1 re-fetch of the admitted set -> retrospective longer-window
            channel -> frozen decision

Emits, under --out:
  raw/controls.jsonl, raw/control_probes.jsonl, raw/census.jsonl,
  raw/obs1.jsonl, raw/selfpair.jsonl, raw/retro.jsonl, raw/PROGRESS.json,
  derived/metrics.json, derived/decision.json
"""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import http.server
import json
import math
import re
import socketserver
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# frozen constants
# --------------------------------------------------------------------------
SEEDS = [
    ("doc.rust-lang.org", "https://doc.rust-lang.org/stable/book/"),
    ("docs.pytest.org", "https://docs.pytest.org/en/stable/"),
    ("docs.readthedocs.io", "https://docs.readthedocs.io/en/stable/"),
    ("pandas.pydata.org", "https://pandas.pydata.org/docs/"),
]
DEPTH = 6
SHALLOW_MAX_HOP = 2
SHALLOW_CAP_PER_HOST = 140
DEEP_CAP_PER_HOST = 220
PER_HOST_GET_CEILING = 420
PER_HOST_WALL_S = 150.0
GET_CEILING_OBS0 = 1500
GET_CEILING_OBS1 = 1600
GET_CEILING_TOTAL = 3200
OBS1_TARGET_CAP = 1200
SEPARATION_S = 360.0
DT_MIN_S = 300.0
DT_MAX_S = 900.0
MODULE_WALL_BUDGET_S = 900.0
REQUEST_TIMEOUT = 12.0
MAX_BODY_BYTES = 8_000_000
WORKERS = 6
PER_HOST_CONCURRENCY = 2
PER_HOST_SPACING_S = 0.10
UA = "spider-r2/1.0"
ASSET_EXTS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".bz2", ".xz", ".mp3", ".mp4", ".webm", ".avi", ".mov", ".txt", ".xml",
)
CERT_GRID = (0.01, 0.02, 0.05)
MIN_N_PER_STRATUM = 60
MIN_HOST_STRATUM_N = 25
MIN_HOSTS_BOTH = 2
CENSOR_MAX = 0.20
HOST_CONC_WARN = 0.60
VERSION_PINNED_FRAC_WARN = 0.80
ALPHA = 0.05
SELFPAIR_N = 10
SELFPAIR_MAX_GAP_S = 5.0
POS_CONTROL_URLS = [
    "https://www.cloudflare.com/cdn-cgi/trace",
    "https://api.github.com/rate_limit",
    "https://timeapi.io/api/Time/current/zone?timeZone=UTC",
]
NULL_CONTROL_URLS = [
    "https://example.com/",
    "https://www.iana.org/domains/reserved",
]
PARENT_CENSUS = ("research/experiments/EXP-FRONTIER-38940047535/"
                 "run/raw/census.jsonl")
PARENT_PROVENANCE = ("research/experiments/EXP-FRONTIER-38940047535/"
                     "provenance.json")
RETRO_MIN_WINDOW_H = 6.0
RETRO_MAX_WINDOW_D = 30.0
VER_RE = re.compile(r"(^|/)(\d+\.\d+(\.\d+)?(\.x)?|v\d+(\.\d+)*)(/|$)")
MOV_RE = re.compile(
    r"/(stable|latest|dev|dev-requirements|main|master|trunk|edge|nightly)(/|$)")

_T0 = time.monotonic()
_GET_LOCK = threading.Lock()
_GETS = {"n": 0}
_HOST_SEM: dict = {}
_HOST_NEXT: dict = {}


def elapsed() -> float:
    return time.monotonic() - _T0


def gets() -> int:
    with _GET_LOCK:
        return _GETS["n"]


def _host_sem(host: str) -> threading.BoundedSemaphore:
    with _GET_LOCK:
        if host not in _HOST_SEM:
            _HOST_SEM[host] = threading.BoundedSemaphore(PER_HOST_CONCURRENCY)
        return _HOST_SEM[host]


def repo_root() -> Path:
    p = Path(__file__).resolve()
    for anc in [p.parent] + list(p.parents):
        if (anc / "research" / "lanes" / "registry.json").is_file():
            return anc
    return Path.cwd()


def iso(ts: float | None) -> str:
    if ts is None:
        return ""
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


# --------------------------------------------------------------------------
# canonicalisation (PRIMARY change channel) and URL classification
# --------------------------------------------------------------------------
_COMMENT_RE = re.compile(r"(?is)<!--.*?-->")
_SCRIPT_RE = re.compile(r"(?is)<script\b.*?</script\s*>")
_STYLE_RE = re.compile(r"(?is)<style\b.*?</style\s*>")
_TAG_RE = re.compile(r"(?s)<[^>]*>")
_WS_RE = re.compile(r"\s+")


def canon(body: bytes) -> str:
    """Frozen structural-text canonicalisation of a fetched body.

    Removes comments, <script> and <style> blocks and every remaining tag,
    unescapes the six standard entities, collapses whitespace runs, lowercases.
    HTML attributes are therefore NOT observable on this channel by
    construction; the byte channel is reported alongside precisely so that
    attribute-only and script-only churn stays visible instead of silently
    vanishing.
    """
    t = body.decode("utf-8", "replace")
    t = _COMMENT_RE.sub(" ", t)
    t = _SCRIPT_RE.sub(" ", t)
    t = _STYLE_RE.sub(" ", t)
    t = _TAG_RE.sub(" ", t)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return _WS_RE.sub(" ", t).strip().lower()


def text_sha(body: bytes) -> str:
    return hashlib.sha256(canon(body).encode("utf-8")).hexdigest()


def url_class(url: str) -> str:
    p = urllib.parse.urlsplit(url).path
    if VER_RE.search(p):
        return "VERSION_PINNED"
    if MOV_RE.search(p):
        return "MOVING_ALIAS"
    return "OTHER"


# --------------------------------------------------------------------------
# exact one-sided Clopper-Pearson bounds (no scipy dependency)
# --------------------------------------------------------------------------
def binom_tail(k: int, n: int, p: float) -> float:
    if n <= 0:
        return 1.0
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 1.0 if k >= n else 0.0
    return sum(math.comb(n, i) * p ** i * (1.0 - p) ** (n - i)
               for i in range(0, k + 1))


def cp_ub95(k: int, n: int, alpha: float = ALPHA) -> float | None:
    """sup{p : P(X <= k | n, p) > alpha}: one-sided upper 95% binomial bound."""
    if n <= 0:
        return None
    if k >= n:
        return 1.0
    if binom_tail(k, n, 1.0) > alpha:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if binom_tail(k, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
    return hi


def cert_level(k: int, n: int) -> float | None:
    """Tightest level in CERT_GRID certified by the one-sided 95% bound."""
    if n <= 0:
        return None
    ub = cp_ub95(k, n)
    if ub is None:
        return None
    for level in CERT_GRID:
        if ub <= level:
            return level
    return None


def contrast_p(kd: int, nd: int, ks: int, ns: int) -> float:
    """Exact one-sided p-value for p_deep > p_shallow under the pooled rate."""
    tot, k = nd + ns, kd + ks
    if tot <= 0 or k <= 0 or ns <= 0:
        return 1.0
    return binom_tail(ks, ns, k / tot)


def mdc_deep_rate(nd: int, ns: int, cap: int = 60) -> float | None:
    """Smallest deep rate detectable at ALPHA when the shallow stratum has none."""
    if nd <= 0 or ns <= 0:
        return None
    for kd in range(1, cap + 1):
        if contrast_p(kd, nd, 0, ns) <= ALPHA:
            return kd / nd
    return None


# --------------------------------------------------------------------------
# transport (norm / is_asset / static_links / fetch mirror the bound parent policy)
# --------------------------------------------------------------------------
class _LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def norm(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    if ":" in netloc and not netloc.endswith("]"):
        host, _, port = netloc.rpartition(":")
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    return urllib.parse.urlunsplit((scheme, netloc, p.path or "/", p.query, ""))


def is_asset(url: str) -> bool:
    return urllib.parse.urlsplit(url).path.lower().endswith(ASSET_EXTS)


def static_links(base: str, body: bytes) -> list:
    lp = _LinkParser()
    try:
        lp.feed(body.decode("utf-8", "replace"))
    except Exception:
        return []
    out = []
    for href in lp.hrefs:
        try:
            u = urllib.parse.urljoin(base, href.strip())
        except Exception:
            continue
        if urllib.parse.urlsplit(u).scheme not in ("http", "https"):
            continue
        if is_asset(u):
            continue
        out.append(u)
    return out


def fetch(url: str, want_links: bool = False,
          timeout: float = REQUEST_TIMEOUT) -> dict:
    """One credential-free GET.  Returns a RAW observation record only.

    The body is hashed and (optionally) link-extracted at fetch time and then
    dropped: no body is ever retained, which keeps peak memory independent of
    frame size.  Bytes are never masked, so a server that returns different
    bytes for different User-Agent strings is observable as a byte-channel
    change and is not silently absorbed.
    """
    host = urllib.parse.urlsplit(url).netloc.lower()
    rec = {"url": norm(url), "status": None, "body_len": None, "sha256": None,
           "text_sha256": None, "final_url": None, "content_type": "",
           "etag": "", "last_modified": "", "truncated": False, "error": None,
           "t_start": None, "t_end": None}
    links: list = []
    with _host_sem(host):
        with _GET_LOCK:
            wait = _HOST_NEXT.get(host, 0.0) - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        rec["t_start"] = time.monotonic()
        body = b""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read(MAX_BODY_BYTES + 1)
                rec["status"] = int(r.status)
                rec["final_url"] = norm(r.geturl())
                rec["content_type"] = (
                    r.headers.get("Content-Type") or "").split(";")[0].strip()
                rec["etag"] = r.headers.get("ETag") or ""
                rec["last_modified"] = r.headers.get("Last-Modified") or ""
                if len(raw) > MAX_BODY_BYTES:
                    raw = raw[:MAX_BODY_BYTES]
                    rec["truncated"] = True
                body = raw
                if want_links:
                    links = static_links(rec["final_url"], body)
        except urllib.error.HTTPError as e:
            try:
                e.read()
            except Exception:
                pass
            rec["status"] = int(e.code)
            rec["final_url"] = norm(url)
            rec["error"] = "http_%d" % e.code
        except Exception as e:
            rec["final_url"] = norm(url)
            rec["error"] = repr(e)[:120]
        rec["t_end"] = time.monotonic()
        with _GET_LOCK:
            _HOST_NEXT[host] = time.monotonic()
            _GETS["n"] += 1
    rec["body_len"] = len(body)
    if body:
        rec["sha256"] = hashlib.sha256(body).hexdigest()
        rec["text_sha256"] = text_sha(body)
    rec["_links"] = links
    return rec


def fetch_many(urls: list, want_links: bool = False,
               workers: int = WORKERS) -> list:
    """Concurrent GETs.  Records are returned in input order."""
    out: list = [None] * len(urls)
    lock = threading.Lock()
    idx = {"i": 0}

    def run() -> None:
        while True:
            with lock:
                i = idx["i"]
                if i >= len(urls):
                    return
                idx["i"] = i + 1
            out[i] = fetch(urls[i], want_links=want_links)

    ths = [threading.Thread(target=run, daemon=True)
           for _ in range(max(1, workers))]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    return out


# --------------------------------------------------------------------------
# fetch-complete, stratum-reserved, level-ordered BFS census (one host)
# --------------------------------------------------------------------------
def sweep_host(label: str, seed: str) -> dict:
    """Level-ordered BFS with a stratum-reserved fetch policy.

    Levels 0..SHALLOW_MAX_HOP form the SHALLOW stratum and are capped at
    SHALLOW_CAP_PER_HOST fetches; levels >= SHALLOW_MAX_HOP+1 form the DEEP
    stratum and are capped at DEEP_CAP_PER_HOST fetches.  Fetching therefore
    stops when the stratum's fetch budget is exhausted, never when discovery is
    exhausted.  This is the repair of the parent's discover-until-budget
    starvation, in which 363 of 402 discovered deep URLs were never fetched.
    """
    deadline = time.monotonic() + PER_HOST_WALL_S
    recs: dict = {}
    hop: dict = {}
    shallow_fetches = 0
    deep_fetches = 0
    seed_n = norm(seed)
    seed_rec = fetch(seed_n, want_links=True)
    recs[seed_n] = seed_rec
    hop[seed_n] = 0
    seed_host = urllib.parse.urlsplit(
        seed_rec["final_url"] or seed_n).netloc.lower()
    if seed_rec["status"] != 200:
        return {"host": label, "seed": seed_n,
                "seed_error": seed_rec["error"] or ("status=%s" % seed_rec["status"]),
                "recs": recs, "hop": hop, "shallow_fetches": 0, "deep_fetches": 0,
                "shallow_capped": False, "deep_capped": False,
                "time_truncated": False, "gets_host": gets()}
    seen = {seed_n}
    frontier = [seed_n]
    for lvl in range(DEPTH):
        if not frontier:
            break
        if lvl <= SHALLOW_MAX_HOP:
            if shallow_fetches >= SHALLOW_CAP_PER_HOST:
                # shallow stratum budget exhausted: skip (do not fetch) this
                # level but keep descending so the DEEP stratum is still
                # fetched from whatever was already discovered.
                continue
            budget = min(len(frontier), SHALLOW_CAP_PER_HOST - shallow_fetches)
        else:
            if deep_fetches >= DEEP_CAP_PER_HOST:
                break
            budget = min(len(frontier), DEEP_CAP_PER_HOST - deep_fetches)
        batch, frontier = frontier[:budget], frontier[budget:]
        if gets() >= GET_CEILING_OBS0 or gets() >= GET_CEILING_TOTAL:
            break
        if time.monotonic() > deadline:
            break
        got = fetch_many(batch, want_links=True, workers=PER_HOST_CONCURRENCY)
        if lvl <= SHALLOW_MAX_HOP:
            shallow_fetches += len(got)
        else:
            deep_fetches += len(got)
        nxt: list = []
        for u, rec in zip(batch, got):
            recs[u] = rec
            hop[u] = lvl
            if rec["status"] != 200:
                continue
            for raw in rec.get("_links", []):
                nu = norm(raw)
                if nu in seen:
                    continue
                if urllib.parse.urlsplit(nu).netloc.lower() != seed_host:
                    continue
                seen.add(nu)
                nxt.append(nu)
        frontier = frontier + nxt
    for rec in recs.values():
        rec.pop("_links", None)
    return {"host": label, "seed": seed_n, "seed_error": None, "recs": recs,
            "hop": hop, "shallow_fetches": shallow_fetches,
            "deep_fetches": deep_fetches,
            "shallow_capped": shallow_fetches >= SHALLOW_CAP_PER_HOST,
            "deep_capped": deep_fetches >= DEEP_CAP_PER_HOST,
            "time_truncated": time.monotonic() > deadline,
            "gets_host": gets()}


# --------------------------------------------------------------------------
# frozen decision function
# --------------------------------------------------------------------------
def decide(m: dict) -> dict:
    """Total function on the frozen metrics.  Every branch is reachable and no
    branch depends on anything not present in `m`.

    m keys used: control_ok, frame_ok, n_deep, n_shallow, k_text_deep,
    k_text_shallow, censor_frac_deep, censor_frac_shallow, host_conc_deep,
    host_conc_shallow, hosts_both, verpin_frac_deep, verpin_frac_shallow.
    """
    if not m["control_ok"] or not m["frame_ok"]:
        return {"label": "NO_DATA_CONTROL_OR_FRAME_FAIL", "status": "MEASUREMENT_INVALID",
                "certified_deep": None, "certified_shallow": None,
                "reason": "frozen validity gates failed before a certification is possible"}
    if m["n_deep"] < MIN_N_PER_STRATUM or m["n_shallow"] < MIN_N_PER_STRATUM:
        return {"label": "REFUSE_CERTIFY_INSUFFICIENT_N", "status": "COMPLETE",
                "certified_deep": None, "certified_shallow": None,
                "reason": "paired per-stratum n below MIN_N_PER_STRATUM=%d "
                          "(deep=%d shallow=%d)" % (MIN_N_PER_STRATUM, m["n_deep"],
                                                    m["n_shallow"])}
    if (m["censor_frac_deep"] > CENSOR_MAX or m["censor_frac_shallow"] > CENSOR_MAX):
        starved = []
        if m["censor_frac_deep"] > CENSOR_MAX:
            starved.append("DEEP")
        if m["censor_frac_shallow"] > CENSOR_MAX:
            starved.append("SHALLOW")
        return {"label": "REFUSE_CERTIFY_CENSORED_" + "_".join(starved),
                "status": "COMPLETE", "certified_deep": None,
                "certified_shallow": None,
                "reason": "observation-1 censoring above CENSOR_MAX=%.2f; the "
                          "surviving-pair bound would not generalise to the "
                          "admitted population" % CENSOR_MAX}
    ld = cert_level(m["k_text_deep"], m["n_deep"])
    ls = cert_level(m["k_text_shallow"], m["n_shallow"])
    if ld is None and ls is None:
        label = "GUARD_REQUIRED_BOTH_STRATA"
    elif ld is None:
        label = "CERTIFY_SHALLOW_GUARD_DEEP"
    elif ls is None:
        label = "CERTIFY_DEEP_GUARD_SHALLOW"
    else:
        label = "CERTIFY_BOTH_AT_" + ("%g" % max(ld, ls)).replace(".", "P")
    tags = []
    if m["hosts_both"] < MIN_HOSTS_BOTH:
        tags.append("DEPTH_NOT_IDENTIFIABLE")
    if max(m["host_conc_deep"], m["host_conc_shallow"]) >= HOST_CONC_WARN:
        tags.append("HOST_CONCENTRATED")
    if max(m["verpin_frac_deep"], m["verpin_frac_shallow"]) >= VERSION_PINNED_FRAC_WARN:
        tags.append("BOUNDED_TO_VERSION_PINNED")
    out = {"label": label + ("__" + "_".join(tags) if tags else ""),
           "status": "COMPLETE", "certified_deep": ld, "certified_shallow": ls,
           "tags": tags}
    if ld is None:
        out["reason"] = ("deep-stratum per-page text-change upper bound exceeds the "
                         "coarsest certified level (%.2f)" % CERT_GRID[-1])
    elif ls is None:
        out["reason"] = ("shallow-stratum per-page text-change upper bound exceeds the "
                         "coarsest certified level (%.2f)" % CERT_GRID[-1])
    else:
        out["reason"] = ("both strata certify zero-GET tolerance at the measured "
                         "separation; coarsest certified level %g" % max(ld, ls))
    if "DEPTH_NOT_IDENTIFIABLE" in tags:
        out["reason"] += ("; depth-concentration claim REFUSED because fewer than "
                          "%d hosts populate both strata" % MIN_HOSTS_BOTH)
    return out


# --------------------------------------------------------------------------
# offline controls (in-process HTTP fixture; no external network)
# --------------------------------------------------------------------------
FIXTURES = {
    "/static.html": (200, b"<html><head><title>Static</title></head><body>"
                     b"<h1>Static Page</h1><p>alpha beta gamma</p></body></html>"),
    "/textmut.html": (200, b"<html><head><title>Static</title></head><body>"
                      b"<h1>Static Page</h1><p>alpha beta DELTA</p></body></html>"),
    "/attr.html": (200, b"<html><head><title>Static</title></head><body class=\"a\" "
                   b"data-n=\"7\"><h1>Static Page</h1><p>alpha beta gamma</p></body></html>"),
    "/script.html": (200, b"<html><head><title>Static</title><script nonce=\"zzz\">"
                     b"var a=1;</script></head><body><h1>Static Page</h1>"
                     b"<p>alpha beta gamma</p></body></html>"),
    "/gone.html": (200, b"<html><body><h1>Temporary</h1><p>temp page</p></body></html>"),
}


def offline_controls() -> list:
    rows: list = []
    state = {"gone_404": False}

    class H(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/gone.html" and state["gone_404"]:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            if path not in FIXTURES:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            code, body = FIXTURES[path]
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]

    def rec(cid, expect, ok, detail):
        rows.append({"control": cid, "expected": expect, "observed": detail,
                     "pass": bool(ok)})

    a = fetch(base + "/static.html")
    b = fetch(base + "/static.html")
    rec("C-CANON-IDEMPOTENT", "canon(canon(x))==canon(x)",
        canon(canon(a and FIXTURES["/static.html"][1]).encode()) == canon(FIXTURES["/static.html"][1]),
        "static text_sha stable=%s" % (a["text_sha256"] == b["text_sha256"]))
    mut = fetch(base + "/textmut.html")
    rec("C-DETECT-TEXT-INJECTION", "visible-text change -> TEXT differs",
        mut["text_sha256"] != a["text_sha256"],
        "text_changed=%s byte_changed=%s" % (mut["text_sha256"] != a["text_sha256"],
                                              mut["sha256"] != a["sha256"]))
    attr = fetch(base + "/attr.html")
    rec("C-DETECT-ATTR-ONLY", "attribute-only change -> TEXT same, BYTE differs",
        attr["text_sha256"] == a["text_sha256"] and attr["sha256"] != a["sha256"],
        "text_same=%s byte_diff=%s" % (attr["text_sha256"] == a["text_sha256"],
                                        attr["sha256"] != a["sha256"]))
    scr = fetch(base + "/script.html")
    rec("C-DETECT-SCRIPT-ONLY", "script-nonce change -> TEXT same, BYTE differs",
        scr["text_sha256"] == a["text_sha256"] and scr["sha256"] != a["sha256"],
        "text_same=%s byte_diff=%s" % (scr["text_sha256"] == a["text_sha256"],
                                        scr["sha256"] != a["sha256"]))
    st = fetch(base + "/gone.html")
    st2 = fetch(base + "/gone.html")
    state["gone_404"] = True
    gone = fetch(base + "/gone.html")
    rec("C-CENSOR-404-DETECTED", "404 at obs1 -> censored channel, not a text event",
        gone["status"] == 404 and st["status"] == 200,
        "obs0=%s obs1=%s" % (st["status"], gone["status"]))
    rec("C-LIVE-DETECTOR-ON-FIXTURE", "two identical fixture GETs -> no change",
        st["text_sha256"] == st2["text_sha256"],
        "text_same=%s" % (st["text_sha256"] == st2["text_sha256"]))
    for (k, n), cid, want in (((0, 60), "C-CP-BOUND-N60", 0.048703),
                              ((0, 150), "C-CP-BOUND-N150", 0.019773),
                              ((0, 299), "C-CP-BOUND-N299", 0.009969),
                              ((1, 400), "C-CP-BOUND-K1N400", 0.011804)):
        got = cp_ub95(k, n)
        rec(cid, "exact one-sided 95%% UB at k=%d,n=%d" % (k, n),
            abs(got - want) < 5e-6, "ub=%.6f expected=%.6f" % (got, want))
    rec("C-CERT-LEVEL-LADDER", "cert_level(0,299)=0.01, (0,150)=0.02, (0,60)=0.05, (1,400)=0.02",
        cert_level(0, 299) == 0.01 and cert_level(0, 150) == 0.02
        and cert_level(0, 60) == 0.05 and cert_level(1, 400) == 0.02,
        "levels=%s" % [cert_level(0, 299), cert_level(0, 150), cert_level(0, 60),
                       cert_level(1, 400)])
    rec("C-CONTRAST-POWER", "contrast_p(6,380,0,420)<=0.05 and contrast_p(5,380,0,420)>0.05",
        contrast_p(6, 380, 0, 420) <= 0.05 and contrast_p(5, 380, 0, 420) > 0.05,
        "p6=%.5f p5=%.5f mdc=%s" % (contrast_p(6, 380, 0, 420),
                                     contrast_p(5, 380, 0, 420),
                                     mdc_deep_rate(380, 420)))
    base_m = {"control_ok": True, "frame_ok": True, "n_deep": 380, "n_shallow": 420,
              "k_text_deep": 0, "k_text_shallow": 0, "censor_frac_deep": 0.02,
              "censor_frac_shallow": 0.02, "host_conc_deep": 0.5, "host_conc_shallow": 0.4,
              "hosts_both": 3, "verpin_frac_deep": 0.05, "verpin_frac_shallow": 0.02}
    canaries = [
        ("C-DECIDE-CERTIFY-BOTH", dict(base_m)),
        ("C-DECIDE-GUARD-BOTH", dict(base_m, k_text_deep=12, k_text_shallow=9)),
        ("C-DECIDE-GUARD-DEEP", dict(base_m, k_text_deep=12)),
        ("C-DECIDE-GUARD-SHALLOW", dict(base_m, k_text_shallow=12)),
        ("C-DECIDE-INSUFFICIENT-N", dict(base_m, n_deep=40)),
        ("C-DECIDE-CENSORED", dict(base_m, censor_frac_deep=0.55)),
        ("C-DECIDE-CONTROL-FAIL", dict(base_m, control_ok=False)),
        ("C-DECIDE-NOT-IDENTIFIABLE", dict(base_m, hosts_both=1)),
        ("C-DECIDE-HOST-CONCENTRATED", dict(base_m, host_conc_deep=0.91)),
        ("C-DECIDE-VERSION-PINNED", dict(base_m, verpin_frac_shallow=0.85)),
    ]
    seen_labels = []
    for cid, mm in canaries:
        d = decide(mm)
        seen_labels.append(d["label"])
        rec(cid, "reachable decision branch: %s" % d["label"], True,
            "status=%s certified_deep=%s certified_shallow=%s"
            % (d["status"], d["certified_deep"], d["certified_shallow"]))
    rec("C-DECIDE-BRANCHES-DISTINCT", ">=9 distinct decision labels", 
        len(set(seen_labels)) >= 9, "labels=%s" % sorted(set(seen_labels)))
    srv.shutdown()
    return rows


# --------------------------------------------------------------------------
# live measurement
# --------------------------------------------------------------------------
def obs0_census() -> dict:
    out: dict = {}
    lock = threading.Lock()

    def run(label, seed):
        res = sweep_host(label, seed)
        with lock:
            out[label] = res

    ths = [threading.Thread(target=run, args=(l, s), daemon=True) for l, s in SEEDS]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    return out


def parent_window() -> tuple:
    p = json.loads((repo_root() / PARENT_PROVENANCE).read_text(encoding="utf-8"))
    tl = p.get("timeline_utc", {})

    def parse(s):
        s = (s or "").split(" ")[0].strip()
        if not s.endswith("Z"):
            return None
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc).timestamp()

    return parse(tl.get("scored_run_started")), parse(tl.get("scored_run_finished"))




def summarize(rows0: list, rows1: list, selfpairs: list, probes0: list,
              retro_rows: list, retro_info: dict, census: dict, controls: list,
              code_sha: str, sleep_s: float, gets_controls: int, gets_obs0: int,
              gets_total: int) -> dict:
    """Pure derivation: RAW rows -> DERIVED metrics -> frozen decision.

    Extracted as a pure function so that the whole measurement -> decision path
    can be exercised offline on synthetic rows (control C-SUMMARY-PIPELINE)
    without any external network traffic.
    """
    host_of = {r["url"]: r["host"] for r in rows0}
    hop_of = {r["url"]: r["hop"] for r in rows0}
    paired_all = [r for r in rows1 if r["status"] == 200 and r["host"] is not None
                  and r["hop"] is not None and r["dt_s"] is not None]
    # ELIGIBLE analysis set: pages whose measured separation is at least
    # DT_MIN_S.  The rule is timestamp-based and outcome-independent, so it
    # cannot select on whether a page changed; pages below the floor are
    # reported, never silently analysed at too short a lag.
    paired = [r for r in paired_all if r["dt_s"] >= DT_MIN_S]
    all_cens = [r for r in rows1 if r["host"] is not None and r["hop"] is not None
                and r["status"] != 200]

    def stratum(name: str):
        deep = name == "DEEP"
        sel = [r for r in paired if (r["hop"] >= SHALLOW_MAX_HOP + 1) == deep]
        cens = [r for r in all_cens if (r["hop"] >= SHALLOW_MAX_HOP + 1) == deep]
        return sel, cens

    metrics: dict = {"M-GETS-TOTAL": gets_total}
    for name in ("DEEP", "SHALLOW", "ALL"):
        if name == "ALL":
            sel, cens = paired, all_cens
        else:
            sel, cens = stratum(name)
        n = len(sel)
        k_text = sum(1 for r in sel if r["text_changed"])
        k_byte = sum(1 for r in sel if r["byte_changed"])
        metrics["M-N-PAIR-" + name] = n
        metrics["M-CHANGE-TEXT-" + name] = k_text
        metrics["M-CHANGE-BYTE-" + name] = k_byte
        metrics["M-CHANGE-RATE-TEXT-" + name] = (k_text / n) if n else None
        metrics["M-CHANGE-ATTR-ONLY-" + name] = sum(
            1 for r in sel if r["byte_changed"] and not r["text_changed"])
        metrics["M-CHANGE-TRANSPORT-" + name] = sum(
            1 for r in sel if r["transport_changed"])
        metrics["M-HAZARD-TEXT-UB95-" + name] = cp_ub95(k_text, n)
        metrics["M-HAZARD-BYTE-UB95-" + name] = cp_ub95(k_byte, n)
        metrics["M-CERT-LEVEL-TEXT-" + name] = cert_level(k_text, n)
        metrics["M-CENSORED-" + name] = len(cens)
        metrics["M-CENSOR-FRAC-" + name] = (len(cens) / float(n + len(cens))) if (n + len(cens)) else None
        if name == "ALL":
            continue
        dead = sum(1 for r in cens if r["status"] in (404, 410))
        metrics["M-DEAD-404-" + name] = dead
        metrics["M-DEAD-UB95-" + name] = cp_ub95(dead, n + len(cens))
        metrics["M-UNREACHABLE-" + name] = len(cens) - dead
        metrics["M-RATE-LIMITED-" + name] = sum(
            1 for r in cens if r["status"] in (429, 403, 503))
        if n:
            for c in ("VERSION_PINNED", "MOVING_ALIAS", "OTHER"):
                metrics["M-CLASS-FRAC-%s-%s" % (c, name)] = sum(
                    1 for r in sel if r["url_class"] == c) / float(n)
                metrics["M-CHANGE-BY-CLASS-%s-%s" % (c, name)] = sum(
                    1 for r in sel if r["url_class"] == c and r["text_changed"])
        else:
            for c in ("VERSION_PINNED", "MOVING_ALIAS", "OTHER"):
                metrics["M-CLASS-FRAC-%s-%s" % (c, name)] = None
                metrics["M-CHANGE-BY-CLASS-%s-%s" % (c, name)] = 0
        hc: dict = {}
        for r in sel:
            hc[r["host"]] = hc.get(r["host"], 0) + 1
        metrics["M-HOST-CONC-MAX-" + name] = (max(hc.values()) / float(n)) if (n and hc) else None
    dts = sorted(r["dt_s"] for r in paired)
    dts_all = sorted(r["dt_s"] for r in paired_all)
    metrics["M-N-PAIR-EXCLUDED-BELOW-DT-MIN"] = len(paired_all) - len(paired)
    metrics["M-DT-MIN-S"] = dts[0] if dts else None
    metrics["M-DT-MEDIAN-S"] = dts[int(0.5 * (len(dts) - 1))] if dts else None
    metrics["M-DT-P90-S"] = dts[int(0.9 * (len(dts) - 1))] if dts else None
    metrics["M-DT-MAX-S"] = dts_all[-1] if dts_all else None
    metrics["M-DT-MEDIAN-ALLPAIRS-S"] = (dts_all[int(0.5 * (len(dts_all) - 1))]
                                         if dts_all else None)
    hosts_both = 0
    host_table: dict = {}
    for h in sorted({r["host"] for r in paired}):
        d = [r for r in paired if r["host"] == h and r["hop"] >= SHALLOW_MAX_HOP + 1]
        s = [r for r in paired if r["host"] == h and r["hop"] <= SHALLOW_MAX_HOP]
        host_table[h] = {"n_deep": len(d),
                         "k_text_deep": sum(1 for r in d if r["text_changed"]),
                         "n_shallow": len(s),
                         "k_text_shallow": sum(1 for r in s if r["text_changed"])}
        if len(d) >= MIN_HOST_STRATUM_N and len(s) >= MIN_HOST_STRATUM_N:
            hosts_both += 1
    metrics["M-HOST-TABLE"] = host_table
    metrics["M-HOSTS-WITH-BOTH-STRATA"] = hosts_both
    metrics["M-CONCENTRATION-P-ONE-SIDED"] = contrast_p(
        metrics["M-CHANGE-TEXT-DEEP"], metrics["M-N-PAIR-DEEP"],
        metrics["M-CHANGE-TEXT-SHALLOW"], metrics["M-N-PAIR-SHALLOW"])
    metrics["M-CONCENTRATION-MDC-RATE"] = mdc_deep_rate(
        metrics["M-N-PAIR-DEEP"], metrics["M-N-PAIR-SHALLOW"])
    metrics["M-CONCENTRATION-DETECTED"] = bool(
        metrics["M-CONCENTRATION-P-ONE-SIDED"] <= ALPHA
        and metrics["M-CHANGE-TEXT-DEEP"] > metrics["M-CHANGE-TEXT-SHALLOW"])
    pos = [r for r in probes0 if r["role"] == "pos"]
    null = [r for r in probes0 if r["role"] == "null"]
    metrics["M-LIVE-POS-CHANGED"] = sum(
        1 for r in pos if r["obs"] == 1 and r["status"] == 200 and r.get("text_changed"))
    metrics["M-LIVE-POS-OK"] = sum(1 for r in pos if r["obs"] == 1 and r["status"] == 200)
    metrics["M-LIVE-NULL-CHANGED"] = sum(
        1 for r in null if r["obs"] == 1 and r["status"] == 200 and r.get("text_changed"))
    metrics["M-LIVE-NULL-OK"] = sum(1 for r in null if r["obs"] == 1 and r["status"] == 200)
    metrics["M-SELFPAIR-CHANGED"] = sum(1 for r in selfpairs if r["text_changed"])
    metrics["M-SELFPAIR-BYTE-CHANGED"] = sum(1 for r in selfpairs if r["byte_changed"])
    metrics["M-SELFPAIR-N"] = len(selfpairs)
    metrics["M-SELFPAIR-MAX-GAP-S"] = max([r["gap_s"] for r in selfpairs], default=None)
    metrics["M-OFFLINE-CONTROLS-PASS"] = "%d/%d" % (
        sum(1 for c in controls if c["pass"]), len(controls))
    metrics["M-OFFLINE-CONTROLS-FAILING"] = [c["control"] for c in controls if not c["pass"]]
    metrics["M-GETS-CONTROLS-OFFLINE"] = gets_controls
    metrics["M-GETS-OBS0"] = gets_obs0 - gets_controls
    metrics["M-GETS-OBS1"] = gets_total - gets_obs0
    metrics["M-N-DISCOVERED"] = len(rows0)
    metrics["M-N-ADMITTED"] = sum(1 for r in rows0 if r["status"] == 200)
    metrics["M-N-TRUNCATED"] = sum(1 for r in rows0 if r.get("truncated"))
    metrics["M-TIME-TRUNCATED-HOSTS"] = sum(1 for r in census.values() if r["time_truncated"])
    metrics["M-SHALLOW-CAPPED-HOSTS"] = sum(1 for r in census.values() if r["shallow_capped"])
    metrics["M-DEEP-CAPPED-HOSTS"] = sum(1 for r in census.values() if r["deep_capped"])
    metrics["M-SEED-ERRORS"] = {k: v["seed_error"] for k, v in census.items()
                                if v.get("seed_error")}
    metrics["M-SEPARATION-REQUESTED-S"] = sleep_s
    metrics["M-WALL-S"] = round(elapsed(), 2)
    metrics["M-PARTIAL"] = bool(elapsed() > MODULE_WALL_BUDGET_S)

    comparable = [r for r in retro_rows if r["obs1_status"] == 200]
    retro_dt_h = (sorted([r["dt_h"] for r in comparable])[len(comparable) // 2]
                  if comparable else None)
    per_host: dict = {}
    for r in comparable:
        slot = per_host.setdefault(r["host"], [0, 0])
        slot[1] += 1
        if r["byte_changed"]:
            slot[0] += 1
    max_host_rate = max([v[0] / float(v[1]) for v in per_host.values() if v[1]],
                        default=None)
    retro_info = dict(retro_info)
    retro_info.update({
        "n_comparable": len(comparable),
        "n_byte_changed": sum(1 for r in comparable if r["byte_changed"]),
        "dt_h_min": min([r["dt_h"] for r in comparable], default=None),
        "dt_h_median": sorted([r["dt_h"] for r in comparable])[len(comparable) // 2]
        if comparable else None,
        "dt_h_max": max([r["dt_h"] for r in comparable], default=None),
        "max_per_host_change_rate": max_host_rate,
        "negotiation_suspected": bool(max_host_rate is not None and max_host_rate >= 0.90)})
    retro_info["admitted"] = bool(
        comparable and retro_dt_h is not None
        and RETRO_MIN_WINDOW_H <= retro_dt_h <= RETRO_MAX_WINDOW_D * 24.0
        and not retro_info["negotiation_suspected"])
    if not retro_info["admitted"]:
        retro_info["not_admitted_reason"] = (
            "no comparable pages" if not comparable else
            ("negotiation artifact suspected" if retro_info["negotiation_suspected"]
             else ("measured window %.3f h outside [%.1f h, %.1f d]"
                   % (retro_dt_h, RETRO_MIN_WINDOW_H, RETRO_MAX_WINDOW_D))))
    for name in ("ALL", "SHALLOW", "DEEP"):
        if name == "ALL":
            sel = comparable
        else:
            sel = [r for r in comparable
                   if (r["hop"] >= SHALLOW_MAX_HOP + 1) == (name == "DEEP")]
        k = sum(1 for r in sel if r["byte_changed"])
        metrics["M-RETRO-N-" + name] = len(sel)
        metrics["M-RETRO-CHANGE-BYTE-" + name] = k
        metrics["M-RETRO-UB95-" + name] = cp_ub95(k, len(sel))
        metrics["M-RETRO-CERT-LEVEL-" + name] = cert_level(k, len(sel))
    metrics["M-RETRO-INFO"] = retro_info

    control_ok = (metrics["M-LIVE-POS-CHANGED"] >= 1
                  and metrics["M-LIVE-NULL-CHANGED"] == 0
                  and metrics["M-SELFPAIR-CHANGED"] == 0
                  and metrics["M-LIVE-POS-OK"] >= 2
                  and metrics["M-LIVE-NULL-OK"] == 2
                  and metrics["M-SELFPAIR-N"] == SELFPAIR_N
                  and not metrics["M-OFFLINE-CONTROLS-FAILING"])
    dt_max = metrics["M-DT-MAX-S"]
    frame_ok = (not metrics["M-SEED-ERRORS"]
                and sleep_s >= DT_MIN_S
                and dt_max is not None and dt_max <= DT_MAX_S
                and metrics["M-N-PAIR-ALL"] > 0
                and (gets_total - gets_controls) <= GET_CEILING_TOTAL)
    decision = decide({
        "control_ok": control_ok, "frame_ok": frame_ok,
        "n_deep": metrics["M-N-PAIR-DEEP"], "n_shallow": metrics["M-N-PAIR-SHALLOW"],
        "k_text_deep": metrics["M-CHANGE-TEXT-DEEP"],
        "k_text_shallow": metrics["M-CHANGE-TEXT-SHALLOW"],
        "censor_frac_deep": metrics["M-CENSOR-FRAC-DEEP"] or 0.0,
        "censor_frac_shallow": metrics["M-CENSOR-FRAC-SHALLOW"] or 0.0,
        "host_conc_deep": metrics["M-HOST-CONC-MAX-DEEP"] or 0.0,
        "host_conc_shallow": metrics["M-HOST-CONC-MAX-SHALLOW"] or 0.0,
        "hosts_both": metrics["M-HOSTS-WITH-BOTH-STRATA"],
        "verpin_frac_deep": metrics["M-CLASS-FRAC-VERSION_PINNED-DEEP"] or 0.0,
        "verpin_frac_shallow": metrics["M-CLASS-FRAC-VERSION_PINNED-SHALLOW"] or 0.0})
    return {"metrics": metrics, "decision": decision,
            "validity": {"control_ok": control_ok, "frame_ok": frame_ok,
                         "retro_admitted": retro_info["admitted"]},
            "code_sha256_stripped": code_sha}

def synthetic_rows(n_deep: int, n_shallow: int, k_deep: int, k_shallow: int,
                   censored: int = 0, dead: int = 0, dt: float = 360.0,
                   changed_deep_only: bool = False, hosts: int = 3):
    """Deterministic synthetic RAW rows for the offline pipeline control.

    Pages are spread over `hosts` hosts in BOTH strata, so the host
    identifiability and host-concentration tags are exercised with the same
    shapes the live frame is expected to have rather than with a degenerate
    one-host-per-stratum frame.
    """
    rows0: list = []
    rows1: list = []
    ks = 0 if changed_deep_only else k_shallow
    uid = 0
    names = ["h%d" % i for i in range(hosts)]
    for stratum_name, total, k in (("DEEP", n_deep, k_deep),
                                   ("SHALLOW", n_shallow, ks)):
        hop = 3 if stratum_name == "DEEP" else 2
        for i in range(total):
            uid += 1
            host = names[i % hosts]
            url = "https://%s.test/%s%05d.html" % (host, stratum_name.lower(), uid)
            cls = "VERSION_PINNED" if (uid % 25 == 0) else "MOVING_ALIAS"
            rows0.append({"url": url, "host": host, "hop": hop, "obs": 0,
                          "status": 200, "sha256": "a", "text_sha256": "t",
                          "body_len": 100, "etag": "e", "last_modified": "lm",
                          "final_url": url, "content_type": "text/html",
                          "truncated": False, "error": None, "t_start": 0.0,
                          "t_end": 0.0, "url_class": cls})
            rows1.append({"url": url, "host": host, "hop": hop, "obs": 1,
                          "status": 200, "sha256": "b" if i < k else "a",
                          "text_sha256": "u" if i < k else "t",
                          "body_len": 100, "etag": "e", "last_modified": "lm",
                          "final_url": url, "content_type": "text/html",
                          "truncated": False, "error": None, "t_start": dt,
                          "t_end": dt + 0.1, "url_class": cls,
                          "dt_s": dt, "text_changed": i < k,
                          "byte_changed": i < k,
                          "transport_changed": i < k})
    for i in range(dead):
        uid += 1
        url = "https://h0.test/dead%05d.html" % uid
        rows0.append({"url": url, "host": "h0", "hop": 3, "obs": 0, "status": 200,
                      "sha256": "a", "text_sha256": "t", "body_len": 100,
                      "etag": "e", "last_modified": "lm", "final_url": url,
                      "content_type": "text/html", "truncated": False,
                      "error": None, "t_start": 0.0, "t_end": 0.0,
                      "url_class": "MOVING_ALIAS"})
        rows1.append({"url": url, "host": "h0", "hop": 3, "obs": 1, "status": 404,
                      "sha256": None, "text_sha256": None, "body_len": 0,
                      "etag": "", "last_modified": "", "final_url": url,
                      "content_type": "", "truncated": False, "error": "http_404",
                      "t_start": dt, "t_end": dt + 0.1, "url_class": "MOVING_ALIAS",
                      "dt_s": dt, "text_changed": False, "byte_changed": False,
                      "transport_changed": False})
    for i in range(max(0, censored - dead)):
        uid += 1
        url = "https://h0.test/err%05d.html" % uid
        rows0.append({"url": url, "host": "h0", "hop": 3, "obs": 0, "status": 200,
                      "sha256": "a", "text_sha256": "t", "body_len": 100,
                      "etag": "e", "last_modified": "lm", "final_url": url,
                      "content_type": "text/html", "truncated": False,
                      "error": None, "t_start": 0.0, "t_end": 0.0,
                      "url_class": "MOVING_ALIAS"})
        rows1.append({"url": url, "host": "h0", "hop": 3, "obs": 1, "status": 0,
                      "sha256": None, "text_sha256": None, "body_len": 0,
                      "etag": "", "last_modified": "", "final_url": url,
                      "content_type": "", "truncated": False, "error": "timeout",
                      "t_start": dt, "t_end": dt + 0.1, "url_class": "MOVING_ALIAS",
                      "dt_s": dt, "text_changed": False, "byte_changed": False,
                      "transport_changed": False})
    return rows0, rows1


def summary_control() -> list:
    """Offline end-to-end control of the RAW->DERIVED->decision path.

    Exercises every reachable decision label with synthetic RAW rows so that no
    branch of the frozen decision function is untested before freeze.
    """
    rows: list = []
    census = {"h0": {"time_truncated": False, "shallow_capped": False,
                     "deep_capped": False, "seed_error": None}}
    probes: list = []
    for u in ("u1", "u2", "u3"):
        probes.append({"role": "pos", "url": u, "obs": 0, "status": 200,
                       "sha256": "x", "text_sha256": "x"})
        probes.append({"role": "pos", "url": u, "obs": 1, "status": 200,
                       "sha256": "y", "text_sha256": "y", "text_changed": True,
                       "byte_changed": True})
    for u in ("n1", "n2"):
        probes.append({"role": "null", "url": u, "obs": 0, "status": 200,
                       "sha256": "x", "text_sha256": "x"})
        probes.append({"role": "null", "url": u, "obs": 1, "status": 200,
                       "sha256": "x", "text_sha256": "x", "text_changed": False,
                       "byte_changed": False})
    pairs = [{"url": "p%d" % i, "status_a": 200, "status_b": 200, "gap_s": 0.4,
              "text_changed": False, "byte_changed": False} for i in range(SELFPAIR_N)]
    ctl = [{"control": "SYNTH", "pass": True}]

    def run(nd, ns, kd, ks, cens=0, dead=0, changed_deep_only=False, dt=360.0,
            hosts=3, sep=360.0):
        r0, r1 = synthetic_rows(nd, ns, kd, ks, censored=cens, dead=dead, dt=dt,
                                changed_deep_only=changed_deep_only, hosts=hosts)
        return summarize(r0, r1, pairs, probes, [], {}, census, ctl, "sha", sep,
                         0, 10, 20)

    a = run(380, 420, 0, 0)
    rows.append({"control": "C-SUMMARY-ZERO-EVENTS",
                 "expected": "CERTIFY_BOTH_AT_0P01, no tags, n=380/420, 3 hosts span both strata",
                 "observed": "%s deep=%s shallow=%s tags=%s ub_deep=%.6f" % (
                     a["decision"]["label"], a["decision"]["certified_deep"],
                     a["decision"]["certified_shallow"], a["decision"]["tags"],
                     a["metrics"]["M-HAZARD-TEXT-UB95-DEEP"]),
                 "pass": a["decision"]["label"] == "CERTIFY_BOTH_AT_0P01"
                 and a["metrics"]["M-N-PAIR-DEEP"] == 380
                 and a["metrics"]["M-HOSTS-WITH-BOTH-STRATA"] == 3
                 and abs(a["metrics"]["M-HAZARD-TEXT-UB95-DEEP"] - 0.007853) < 5e-6})
    b = run(380, 420, 8, 0, changed_deep_only=True)
    rows.append({"control": "C-SUMMARY-DEEP-EVENTS",
                 "expected": "CERTIFY_BOTH_AT_0P05 with concentration detected (p=0.01468)",
                 "observed": "%s p=%.5f detected=%s deep_level=%s" % (
                     b["decision"]["label"],
                     b["metrics"]["M-CONCENTRATION-P-ONE-SIDED"],
                     b["metrics"]["M-CONCENTRATION-DETECTED"],
                     b["decision"]["certified_deep"]),
                 "pass": b["decision"]["label"] == "CERTIFY_BOTH_AT_0P05"
                 and b["metrics"]["M-CONCENTRATION-DETECTED"] is True
                 and abs(b["metrics"]["M-CONCENTRATION-P-ONE-SIDED"] - 0.01468) < 5e-5})
    c = run(380, 420, 0, 0, cens=40, dead=25)
    rows.append({"control": "C-SUMMARY-CENSOR-AND-DEAD",
                 "expected": "page-gone separated from change: 25 dead -> UB 0.082146; censoring 9.5% tolerated",
                 "observed": "dead_deep=%s ub=%s cens_frac=%s label=%s" % (
                     c["metrics"]["M-DEAD-404-DEEP"],
                     round(c["metrics"]["M-DEAD-UB95-DEEP"], 6),
                     round(c["metrics"]["M-CENSOR-FRAC-DEEP"], 4),
                     c["decision"]["label"]),
                 "pass": c["metrics"]["M-DEAD-404-DEEP"] == 25
                 and abs(c["metrics"]["M-DEAD-UB95-DEEP"] - 0.082146) < 5e-6
                 and c["metrics"]["M-CENSOR-FRAC-DEEP"] < CENSOR_MAX
                 and c["decision"]["label"] == "CERTIFY_BOTH_AT_0P01"})
    d = run(380, 420, 0, 0, cens=200)
    rows.append({"control": "C-SUMMARY-CENSOR-REFUSAL",
                 "expected": "REFUSE_CERTIFY_CENSORED_DEEP (stratum-specific) above CENSOR_MAX",
                 "observed": "%s cens_frac=%.3f" % (
                     d["decision"]["label"], d["metrics"]["M-CENSOR-FRAC-DEEP"]),
                 "pass": d["decision"]["label"] == "REFUSE_CERTIFY_CENSORED_DEEP"
                 and d["metrics"]["M-CENSOR-FRAC-DEEP"] > CENSOR_MAX
                 and d["metrics"]["M-CENSOR-FRAC-SHALLOW"] < CENSOR_MAX})
    e = run(40, 420, 0, 0)
    rows.append({"control": "C-SUMMARY-INSUFFICIENT-N",
                 "expected": "REFUSE_CERTIFY_INSUFFICIENT_N",
                 "observed": e["decision"]["label"],
                 "pass": e["decision"]["label"] == "REFUSE_CERTIFY_INSUFFICIENT_N"})
    f = run(380, 420, 20, 20)
    rows.append({"control": "C-SUMMARY-GUARD-BOTH",
                 "expected": "GUARD_REQUIRED_BOTH_STRATA (UB>0.05 in both strata)",
                 "observed": "%s ub_deep=%.5f ub_shallow=%.5f" % (
                     f["decision"]["label"],
                     f["metrics"]["M-HAZARD-TEXT-UB95-DEEP"],
                     f["metrics"]["M-HAZARD-TEXT-UB95-SHALLOW"]),
                 "pass": f["decision"]["label"] == "GUARD_REQUIRED_BOTH_STRATA"})
    g = run(380, 420, 20, 0, changed_deep_only=True)
    rows.append({"control": "C-SUMMARY-GUARD-DEEP-ONLY",
                 "expected": "CERTIFY_SHALLOW_GUARD_DEEP",
                 "observed": "%s deep=%s shallow=%s" % (
                     g["decision"]["label"], g["decision"]["certified_deep"],
                     g["decision"]["certified_shallow"]),
                 "pass": g["decision"]["label"] == "CERTIFY_SHALLOW_GUARD_DEEP"})
    h = run(380, 420, 0, 20)
    rows.append({"control": "C-SUMMARY-GUARD-SHALLOW-ONLY",
                 "expected": "CERTIFY_DEEP_GUARD_SHALLOW",
                 "observed": "%s deep=%s shallow=%s" % (
                     h["decision"]["label"], h["decision"]["certified_deep"],
                     h["decision"]["certified_shallow"]),
                 "pass": h["decision"]["label"] == "CERTIFY_DEEP_GUARD_SHALLOW"})
    i = run(380, 420, 0, 0, dt=120.0, sep=120.0)
    rows.append({"control": "C-SUMMARY-SHORT-SEPARATION",
                 "expected": "NO_DATA_CONTROL_OR_FRAME_FAIL when requested separation<DT_MIN_S",
                 "observed": "%s dt_median=%s control_ok=%s frame_ok=%s" % (
                     i["decision"]["label"], i["metrics"]["M-DT-MEDIAN-S"],
                     i["validity"]["control_ok"], i["validity"]["frame_ok"]),
                 "pass": i["decision"]["label"] == "NO_DATA_CONTROL_OR_FRAME_FAIL"})
    i2 = run(380, 420, 0, 0, dt=260.0, sep=360.0)
    rows.append({"control": "C-SUMMARY-ELIGIBLE-DT-FLOOR",
                 "expected": "pairs below DT_MIN_S excluded, not analysed at too short a lag",
                 "observed": "eligible=%s excluded=%s label=%s" % (
                     i2["metrics"]["M-N-PAIR-ALL"],
                     i2["metrics"]["M-N-PAIR-EXCLUDED-BELOW-DT-MIN"],
                     i2["decision"]["label"]),
                 "pass": i2["metrics"]["M-N-PAIR-EXCLUDED-BELOW-DT-MIN"] == 800
                 and i2["metrics"]["M-N-PAIR-ALL"] == 0
                 and i2["decision"]["label"] == "NO_DATA_CONTROL_OR_FRAME_FAIL"})
    j = run(380, 420, 0, 0, hosts=1)
    rows.append({"control": "C-SUMMARY-DEPTH-NOT-IDENTIFIABLE",
                 "expected": "DEPTH_NOT_IDENTIFIABLE tag when <MIN_HOSTS_BOTH hosts span both strata",
                 "observed": "%s hosts_both=%s" % (
                     j["decision"]["label"], j["metrics"]["M-HOSTS-WITH-BOTH-STRATA"]),
                 "pass": "DEPTH_NOT_IDENTIFIABLE" in j["decision"]["tags"]})
    k = run(380, 420, 0, 0)
    rows.append({"control": "C-SUMMARY-MDC-REPORTED",
                 "expected": "M-CONCENTRATION-MDC-RATE reported even with zero events (0.0158)",
                 "observed": "mdc=%s p=%s" % (
                     round(k["metrics"]["M-CONCENTRATION-MDC-RATE"], 5),
                     k["metrics"]["M-CONCENTRATION-P-ONE-SIDED"]),
                 "pass": k["metrics"]["M-CONCENTRATION-MDC-RATE"] is not None
                 and abs(k["metrics"]["M-CONCENTRATION-MDC-RATE"] - 0.015789) < 5e-5})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["controls", "all"], default="all")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sleep", type=float, default=SEPARATION_S)
    ap.add_argument("--smoke", action="store_true",
                    help="obs0-only single-observation transport smoke test")
    args = ap.parse_args()
    root = repo_root()
    out = root / args.out if not args.out.startswith("/") else Path(args.out)
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "derived").mkdir(parents=True, exist_ok=True)

    def write_jsonl(rel: str, rows: list) -> None:
        (out / rel).write_text(
            "".join(json.dumps(r, sort_keys=True, default=str) + "\n" for r in rows),
            encoding="utf-8")

    code_sha = hashlib.sha256(
        Path(__file__).resolve().read_bytes().strip()).hexdigest()
    progress = {"stage": args.stage, "code_sha256_stripped": code_sha,
                "smoke": bool(args.smoke), "started_utc": iso(time.time()),
                "wall_budget_s": MODULE_WALL_BUDGET_S}

    controls = offline_controls() + summary_control()
    write_jsonl("raw/controls.jsonl", controls)
    (out / "derived" / "code_identity.json").write_text(
        json.dumps({"code_sha256_stripped": code_sha,
                    "path": str(Path(__file__).resolve())}, indent=2), encoding="utf-8")
    gets_controls = gets()
    progress["gets_after_offline_controls"] = gets_controls
    progress["offline_controls"] = {"n": len(controls),
                                    "passed": sum(1 for c in controls if c["pass"])}
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    if args.stage == "controls":
        progress["finished_utc"] = iso(time.time())
        (out / "raw" / "PROGRESS.json").write_text(
            json.dumps(progress, indent=2, default=str), encoding="utf-8")
        print(json.dumps(progress["offline_controls"]))
        return

    # ---- observation 0: fetch-complete, stratum-reserved census --------------
    census = obs0_census()
    rows0: list = []
    for label, res in sorted(census.items()):
        ordered = sorted(res["recs"].items(),
                         key=lambda kv: (res["hop"].get(kv[0], 99), kv[0]))
        for u, rec in ordered:
            row = {k: v for k, v in rec.items() if k != "_links"}
            row.update({"host": label, "hop": res["hop"].get(u), "obs": 0,
                        "url_class": url_class(u)})
            rows0.append(row)
    write_jsonl("raw/census.jsonl", rows0)
    admitted = [r for r in rows0 if r["status"] == 200]
    progress["obs0"] = {"gets_ledger": gets(), "n_fetched": len(rows0),
                        "n_admitted": len(admitted), "wall_s": round(elapsed(), 2)}
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    if args.smoke:
        progress["finished_utc"] = iso(time.time())
        (out / "raw" / "PROGRESS.json").write_text(
            json.dumps(progress, indent=2, default=str), encoding="utf-8")
        print(json.dumps(progress["obs0"], default=str))
        return

    # ---- control probes at observation 0 -------------------------------------
    probes: list = []
    for u in POS_CONTROL_URLS:
        rec = {k: v for k, v in fetch(u).items() if k != "_links"}
        rec.update({"role": "pos", "obs": 0})
        probes.append(rec)
    for u in NULL_CONTROL_URLS:
        rec = {k: v for k, v in fetch(u).items() if k != "_links"}
        rec.update({"role": "null", "obs": 0})
        probes.append(rec)

    # ---- separation ----------------------------------------------------------
    sleep_s = max(0.0, min(args.sleep, DT_MAX_S))
    progress["separation_requested_s"] = sleep_s
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    time.sleep(sleep_s)

    # ---- observation 1: re-fetch of exactly the observation-0 admitted set ---
    host_of = {r["url"]: r["host"] for r in rows0}
    hop_of = {r["url"]: r["hop"] for r in rows0}
    targets = [r["url"] for r in admitted]
    if len(targets) > OBS1_TARGET_CAP:
        stride = len(targets) / float(OBS1_TARGET_CAP)
        targets = [targets[int(i * stride)] for i in range(OBS1_TARGET_CAP)]
    progress["obs1_targets"] = len(targets)
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    got = fetch_many(targets, want_links=False, workers=WORKERS)
    by0 = {r["url"]: r for r in rows0}
    rows1: list = []
    for rec in got:
        base = by0.get(rec["url"])
        dt = None
        if base and base.get("t_end") and rec.get("t_start"):
            dt = rec["t_start"] - base["t_end"]
        row = {k: v for k, v in rec.items() if k != "_links"}
        both200 = bool(base is not None and base["status"] == 200 and rec["status"] == 200)
        row.update({"obs": 1, "host": host_of.get(rec["url"]),
                    "hop": hop_of.get(rec["url"]), "url_class": url_class(rec["url"]),
                    "dt_s": round(dt, 2) if dt is not None else None,
                    "text_changed": bool(both200 and base["text_sha256"] != rec["text_sha256"]),
                    "byte_changed": bool(both200 and base["sha256"] != rec["sha256"]),
                    "transport_changed": bool(
                        both200 and (base["etag"] != rec["etag"]
                                     or base["last_modified"] != rec["last_modified"]))})
        rows1.append(row)
    write_jsonl("raw/obs1.jsonl", rows1)

    # ---- within-round self-pair determinism control -------------------------
    pair_pool = targets[::max(1, len(targets) // SELFPAIR_N)][:SELFPAIR_N]
    selfpairs: list = []
    for u in pair_pool:
        a = fetch(u)
        b = fetch(u)
        selfpairs.append({"url": u, "status_a": a["status"], "status_b": b["status"],
                          "gap_s": round(b["t_start"] - a["t_end"], 3),
                          "text_changed": bool(a["status"] == 200 and b["status"] == 200
                                               and a["text_sha256"] != b["text_sha256"]),
                          "byte_changed": bool(a["status"] == 200 and b["status"] == 200
                                               and a["sha256"] != b["sha256"])})
    write_jsonl("raw/selfpair.jsonl", selfpairs)

    # ---- control probes at observation 1 -------------------------------------
    for rec0 in [p for p in probes if p["obs"] == 0]:
        rec = {k: v for k, v in fetch(rec0["url"]).items() if k != "_links"}
        rec.update({"role": rec0["role"], "obs": 1,
                    "text_changed": bool(rec0["status"] == 200 and rec["status"] == 200
                                         and rec0["text_sha256"] != rec["text_sha256"]),
                    "byte_changed": bool(rec0["status"] == 200 and rec["status"] == 200
                                         and rec0["sha256"] != rec["sha256"])})
        probes.append(rec)
    write_jsonl("raw/control_probes.jsonl", probes)

    # ---- retrospective longer-window channel (secondary, cannot relabel) -----
    p_start, p_end = parent_window()
    retro_rows: list = []
    retro_info: dict = {"parent_window_start_utc": iso(p_start),
                        "parent_window_end_utc": iso(p_end),
                        "parent_window_s": (p_end - p_start)
                        if (p_start and p_end) else None,
                        "min_window_h": RETRO_MIN_WINDOW_H,
                        "max_window_d": RETRO_MAX_WINDOW_D}
    if p_start and p_end:
        pref: dict = {}
        with (root / PARENT_CENSUS).open(encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("status") == 200 and r.get("sha256"):
                    pref[r["url"]] = r
        refs = fetch_many(sorted(pref), want_links=False, workers=WORKERS)
        for rec in refs:
            ref = pref.get(rec["url"])
            if not ref:
                continue
            retro_rows.append({
                "url": rec["url"], "host": ref.get("host"), "hop": ref.get("hop"),
                "obs1_status": rec["status"], "obs1_sha256": rec["sha256"],
                "parent_sha256": ref["sha256"], "parent_body_len": ref.get("body_len"),
                "obs1_body_len": rec["body_len"], "parent_etag": ref.get("etag"),
                "obs1_etag": rec.get("etag"),
                "byte_changed": bool(rec["status"] == 200
                                     and rec["sha256"] != ref["sha256"]),
                "dt_h": round((rec["t_start"] - p_end) / 3600.0, 3),
                "url_class": url_class(rec["url"])})
    write_jsonl("raw/retro.jsonl", retro_rows)

    # ---- derived measurements and the frozen decision -----------------------
    payload = summarize(rows0, rows1, selfpairs, probes, retro_rows, retro_info,
                        census, controls, code_sha, sleep_s,
                        gets_controls, progress["obs0"]["gets_ledger"], gets())
    payload["retro_info"] = retro_info
    payload["constants"] = {
        "SEPARATION_S": SEPARATION_S, "DT_MIN_S": DT_MIN_S, "DT_MAX_S": DT_MAX_S,
        "SHALLOW_CAP_PER_HOST": SHALLOW_CAP_PER_HOST,
        "DEEP_CAP_PER_HOST": DEEP_CAP_PER_HOST, "MIN_N_PER_STRATUM": MIN_N_PER_STRATUM,
        "CERT_GRID": list(CERT_GRID), "CENSOR_MAX": CENSOR_MAX,
        "GET_CEILING_TOTAL": GET_CEILING_TOTAL, "DEPTH": DEPTH,
        "WORKERS": WORKERS, "PER_HOST_CONCURRENCY": PER_HOST_CONCURRENCY,
        "PER_HOST_SPACING_S": PER_HOST_SPACING_S, "MAX_BODY_BYTES": MAX_BODY_BYTES}
    (out / "derived" / "metrics.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")
    (out / "derived" / "decision.json").write_text(
        json.dumps(payload["decision"], indent=2, sort_keys=True), encoding="utf-8")
    progress["finished_utc"] = iso(time.time())
    progress["wall_s"] = round(elapsed(), 2)
    progress["decision"] = payload["decision"]["label"]
    (out / "raw" / "PROGRESS.json").write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8")
    m = payload["metrics"]
    print(json.dumps({"decision": payload["decision"]["label"], "gets": gets(),
                      "n_deep": m["M-N-PAIR-DEEP"], "n_shallow": m["M-N-PAIR-SHALLOW"],
                      "k_deep": m["M-CHANGE-TEXT-DEEP"],
                      "k_shallow": m["M-CHANGE-TEXT-SHALLOW"],
                      "dt_median_s": m["M-DT-MEDIAN-S"],
                      "pos": m["M-LIVE-POS-CHANGED"], "null": m["M-LIVE-NULL-CHANGED"],
                      "selfpair": m["M-SELFPAIR-CHANGED"]}, default=str))


if __name__ == "__main__":
    main()
FROZEN_CODE_END

---

## 11. Decision rule and gates

`decide(m)` is a total, ordered, disjoint function over ten frozen inputs. It
consumes nothing that is not listed here, and no post-hoc redefinition of a
metric can move a page between branches because the canonicalisation, class
regexes, caps, bounds and thresholds all live inside the hashed module.

**Step 0 — validity (fail closed).** If any of `V1-CODE-IDENTITY`,
`V2-CONTROLS`, `V3-SEED-LIVENESS`, `V5-SEPARATION-WINDOW`, or the GET-ledger
reconciliation fails, **or** the positive control does not fire, **or** any null
control or self-pair changes, **or** any of the 35 offline controls fails:

```
label   = NO_DATA_CONTROL_OR_FRAME_FAIL
status  = MEASUREMENT_INVALID
outcome = NOT_APPLICABLE
```

This is never a scientific negative and may not be reported as one.

**Step 1 — frame.** Else if `M-N-PAIR-DEEP < 60` or `M-N-PAIR-SHALLOW < 60`:

```
label   = REFUSE_CERTIFY_INSUFFICIENT_N
status  = COMPLETE ; outcome = INCONCLUSIVE
```

**Step 2 — censoring.** Else if `M-CENSOR-FRAC-DEEP > 0.20` or
`M-CENSOR-FRAC-SHALLOW > 0.20` (stratum-specific; both may fire):

```
label   = REFUSE_CERTIFY_CENSORED_DEEP [__SHALLOW]
status  = COMPLETE ; outcome = INCONCLUSIVE
```

**Step 3 — certification.** Else, per stratum
`L = cert_level(k_text, n)` = the tightest `L` in `{0.01, 0.02, 0.05}` whose exact
one-sided 95 % Clopper-Pearson upper bound is at most `L`, else `None`:

| condition | label | status / outcome | product meaning |
|---|---|---|---|
| both `None` | `GUARD_REQUIRED_BOTH_STRATA` | COMPLETE / FALSIFIES | guard mandatory in both strata |
| deep `None`, shallow certified | `CERTIFY_SHALLOW_GUARD_DEEP` | COMPLETE / MIXED | guard only where `hop >= 3` state is reused |
| shallow `None`, deep certified | `CERTIFY_DEEP_GUARD_SHALLOW` | COMPLETE / MIXED | guard only where `hop <= 2` state is reused |
| both certified | `CERTIFY_BOTH_AT_<max L>` | COMPLETE / SUPPORTS | no intra-session zero-GET guard for this page class at lags up to `DT` |

**Step 4 — contrast (independent of the label).**
`M-CONCENTRATION-P-ONE-SIDED` is the exact one-sided binomial tail
`P(X_shallow <= k_shallow | pooled rate)` testing `p_deep > p_shallow` at
`ALPHA = 0.05`; `M-CONCENTRATION-DETECTED` is true only when that p is at most
0.05 **and** `k_deep > k_shallow`. `M-CONCENTRATION-MDC-RATE` always reports the
smallest deep rate this frame could have detected, so "no concentration
detected" can never be rendered as "no concentration".

**Step 5 — narrowing tags.** Append, in this order:
`__DEPTH_NOT_IDENTIFIABLE` if `M-HOSTS-WITH-BOTH-STRATA < 2`;
`__HOST_CONCENTRATED` if `max(M-HOST-CONC-MAX-DEEP, M-HOST-CONC-MAX-SHALLOW) >= 0.60`;
`__BOUNDED_TO_VERSION_PINNED` if a stratum is at least 0.80 version-pinned. Tags
only narrow the claim ceiling.

**Step 6 — secondary channel.** `M-RETRO-*` is reported with its own measured
window, `n`, `k`, bound and certified level, and is **admitted** only when it is
not negotiation-suspected (no single host showing at least 0.90 of its comparable
pages changed, the signature of User-Agent or edge content negotiation rather than
invalidation) and its median window lies in `[6 h, 30 d]`. It **cannot** change the
primary label.

Nine distinct labels plus three tags were produced by offline canaries before
freeze (§15). No branch is empty and none is engineered.

---

## 12. Measurement validity gates

`V1`-`V12` are specified in full in `spec.json#measurement_validity`. Summary of
the ones that can void a measurement:

| gate | rule | disposition |
|---|---|---|
| V1 code identity | stripped module hash equals `DERIVED_SHA256` | MEASUREMENT_INVALID |
| V2 controls | 35/35 offline plus live positive plus both null families | MEASUREMENT_INVALID |
| V3 seed liveness | 4/4 seeds HTTP 200 at observation 0 | MEASUREMENT_INVALID |
| V5 separation | requested at least 300 s; every eligible pair `dt >= 300 s`; `M-DT-MAX-S <= 900 s` | NO_DATA |
| V6 censoring | per-stratum censoring fraction at most 0.20 | REFUSE_CERTIFY_CENSORED |
| V8 envelope | ledger reconciles, at most 3200 live GETs, at most 900 s wall | M-PARTIAL reported |
| V9 detector | injections prove text sensitivity and quantify its blindness | MEASUREMENT_INVALID |
| V10 confound | host table, host concentration, URL-class composition | tags |
| V12 timing | nothing two-observation exists at freeze | n/a |

---

## 13. Frozen non-outcome expectations (arithmetic, not measurement)

Computed offline before freeze. These constrain the decision rule's behaviour and
are **not** predictions of the outcome:

- one-sided 95 % CP upper bound at `k = 0`: `n=59 -> 0.049508`, `n=149 -> 0.019905`,
  `n=299 -> 0.009969`; minimum `n` for a certified level 0.05 / 0.02 / 0.01 is
  **59 / 149 / 299**.
- the first event costs a level: at `n=299`, `k=1 -> 0.0158` (level 0.02); at
  `n=380`, `k=12 -> 0.05066` (level `None`); at `n=420`, `k=14 -> 0.05162`.
- contrast power at `n_deep=380`, `n_shallow=420` with zero shallow events: the
  first detectable deep count is **6**, i.e. rate 0.0158 (`p = 0.042`); 5 events
  give `p = 0.072`. Declared **minimum detectable concentration about 1.6 %**.
- frame arithmetic from the frozen caps: at most `4 x (140 + 220) + 4 = 1444`
  observation-0 GETs; measured 1123 live GETs.
- frame arithmetic from the DESIGN sweep: deep 686, shallow 421, both well above
  299, so a 1 % certification is *reachable* if the event count is zero, and the
  frame is not a ceiling (version-pinned share 3.2 % deep / 0.2 % shallow).

---

## 14. Satisfiability self-disproof (adversarial)

Each attack below was answered before freeze; residual attacks are recorded in
§17 rather than hidden.

1. **Empty branch?** No. Nine labels were produced by canaries from synthetic raw
   rows covering `n` and `k` combinations, censoring above and below the ceiling,
   a too-short separation, control failure, and the identifiability tag
   (`C-DECIDE-*`, `C-SUMMARY-*`; 35/35 offline).
2. **Arithmetic impossibility?** No. `n_deep = 686 >= 299` and
   `n_shallow = 421 >= 299` were measured on the bound hosts, so the 1 % level is
   reachable; the guard branches need `k_deep >= 12` or `k_shallow >= 14`, both
   plausible states of the world rather than engineered outcomes.
3. **Ceiling baseline?** No. The deep stratum is 96.8 % `MOVING_ALIAS` content
   (release-mutable), so a zero would be measured rather than true by
   construction; the 0.80 version-pinned guard exists precisely for that failure
   mode and is not expected to bind.
4. **Floor baseline?** No. `example.com` and `iana.org` stay byte-identical, so a
   zero is achievable and therefore meaningful; the detector is proven to fire on
   injected visible-text change.
5. **Insensitive control?** Attacked on three fronts: injection controls that
   prove the primary channel's sensitivity *and* its blindness; a positive-control
   pool probed with the exact detector before registration; and an in-frame
   self-pair null that a small external anchor cannot replace. Any of the three
   failing voids the measurement.
6. **Treatment/comparator identity?** There is no treatment arm. The mandatory
   analogue is the matched shallow comparator on the same live frame at the same
   measured `DT` — same instrument, same vantage, same transport, same host mix —
   so no difference can be attributed to the frame rather than to depth.
7. **Missing prerequisite?** None. Egress, deep-URL fetchability, shallow
   fetchability, throughput, exact statistics and every decision branch were
   exercised on the real substrate or offline before freeze.
8. **Mutable local dependency?** Ten artifacts, all existing files, listed in §19
   and hashed by the freezer. The module itself is pinned by `DERIVED_SHA256`
   inside a hashed `prereg.md`.
9. **Unbound discretion?** The observation-1 target order is the observation-0
   admitted order (deterministic); the self-pair pool is a fixed stride; the
   retrospective URL set is exactly the parent's fetched set; class assignment is
   two frozen regexes; `canon` is frozen text.
10. **Scope drift from the mandate?** The primary channel is the session-scale
    hazard the mandate names. The longer-window retrospective channel is declared
    **secondary**, cannot relabel the primary result, and exists because the
    pre-2.0 TTL protocol was structurally blocked from ever taking a second
    observation (§2.4). No store, no ladder, no cost comparison, no C-CROSSSITE
    re-run.

---

## 15. DESIGN pre-freeze probes (observed values)

Probes ran 2026-10-17T14:25Z-14:36Z. **Boundary: every URL was fetched at most
once, except the six control candidates which were fetched twice within 5 s for
instrument selection. No page of the measured frame has a two-observation pair, so
no hazard, change, dead-page, tolerance or concentration quantity was computed at
DESIGN.**

| probe | what it establishes | observed |
|---|---|---|
| P1 seed liveness | egress from this vantage | 4/4 HTTP 200; 22496/31975/24433/22046 B; 0.128/0.366/0.449/0.375 s |
| P2 deep fetchability | the parent's never-established deep stratum exists and is fetchable | 24 previously-unfetched deep URLs sampled deterministically from the parent census: 23/24 HTTP 200, 1x 404 (`pandas.pydata.org/donate.html`), 0.113-0.483 s, 7974 B - 1.5 MB |
| P3 shallow fetchability | shallow re-fetch is reliable | 24/24 HTTP 200, mean 0.144 s |
| P4 control pool | which control URLs can actually fire this detector | fired: `cloudflare.com/cdn-cgi/trace`, `api.github.com/rate_limit`, `timeapi.io/...`; did not fire: `api.github.com/repos/rust-lang/rust/releases/latest`, `api.github.com/repos/python/cpython/events?per_page=10` (stable within 5 s), `worldtimeapi.org` (unreachable); static nulls stable: `example.com`, `iana.org/domains/reserved`, `api.github.com/repos/octocat/Hello-World`, `rfc-editor.org/rfc/rfc9110.html` |
| P5 transport cost | wall-clock basis for the budget | 32 GETs, 6 workers, per-host concurrency 2, 0.10 s spacing: 3.18 s wall, **10.05 GET/s**, latency p50 0.149 s / p90 0.233 s / max 0.473 s, 32/32 2xx, 2.96 MB |
| P6 exact-bound arithmetic | certification ladder and contrast power | see §13 |
| P7 offline controls | the instrument and the whole decision path work | **35/35 PASS**, including 10 decision-branch and 11 pipeline canaries |
| P8 full-cap observation-0 sweep | the frozen frame on the bound hosts, with the exact frozen module (self-hash `5d2509f6...`) | 1123 live GETs + 8 fixture GETs, 1119 rows, 1107 HTTP 200 / 6x 404 / 6 transport errors, 100.9 MB, **37.26 s**; deep 686 {rust 220, pytest 219, readthedocs 28, pandas 219}, shallow 421 {43, 98, 140, 140}; hop histogram {0:4, 1:138, 2:281, 3:550, 4:145, 5:1}; classes deep {MOVING_ALIAS 439, OTHER 225, VERSION_PINNED 22}, shallow {274, 146, 1}; max host concentration 0.321; max version-pinned fraction 0.032 |
| P8b tiny-cap sweep | the descent rule survives an exhausted shallow budget (`SHALLOW_CAP=22`, `DEEP_CAP=6`) | 4/4 hosts reached hop 3, 24/24 deep pages HTTP 200 |

Frozen a-priori tilt, disclosed: on documentation sites the most likely outcome is
a small or zero event count, which would produce `CERTIFY_BOTH_AT_*`. That branch
is therefore the one most likely to be reached — not because it was engineered,
but because the frame is dominated by release-mutable generated documentation. The
design's protection against that tilt is that the informative content survives a
zero: the exact certified level, the ~1.6 % minimum detectable concentration, the
byte-channel bound, the page-gone bound, and the longer-window retrospective
comparison. A zero-event outcome therefore still changes a product decision and is
not a degenerate measurement.

---

## 16. Budget, schedule, envelope, and stop/pivot triggers

| item | frozen | basis |
|---|---|---|
| observation-0 live GETs | ~1123 (ceiling 1500) | P8 measured 1123 |
| observation-1 live GETs | ~1107 + 292 retro + ~20 control/self-pair (ceiling 1600) | P8 admitted 1107; retro set is the parent's 292 fetched rows |
| total live GETs | ~2542 (ceiling 3200) | arithmetic |
| bytes | ~220 MB | P8 measured 100.9 MB per full sweep |
| observation-0 wall | 37.3 s measured | P8 |
| separation | 360 s requested, hard-bounded [300, 900] s | `DT_MIN_S` justified in §2.1 |
| module wall budget | 900 s | projected ~460 s |
| harness envelope | `SPIDER_MODEL_MAX_RUNTIME_SECONDS = 1200` | `.github/scripts/run-opencode-resilient.sh` |
| money | zero (free model, no browser, no endpoint, no credentials) | — |

Checkpoints: `raw/PROGRESS.json` is written after the offline controls, after
observation 0 (before the sleep), after the separation, and after observation 1. If
the process is killed, observation-0 artifacts survive, EXECUTE emits an honest
`MEASUREMENT_INVALID`, and the next stage can recompute the blocker.

**Stop / pivot triggers.**

1. Positive control does not fire, or any null control / self-pair changes ->
   `NO_DATA_CONTROL_OR_FRAME_FAIL`; do not weaken a control.
2. A seed fails -> `NO_DATA_CONTROL_OR_FRAME_FAIL`; do not substitute a seed.
3. GET ceiling or wall budget exhausted -> report `M-PARTIAL` and the exact GET
   count; do not lower `MIN_N_PER_STRATUM` to fit.
4. Deep stratum below 60 paired pages -> `REFUSE_CERTIFY_INSUFFICIENT_N`; do not
   lower the floor (that is precisely the parent's post-outcome weakening).
5. Retrospective window outside [6 h, 30 d], or a single host showing at least
   0.90 of its comparable pages changed -> retro channel reported but **not
   admitted**; never relabelled as a primary result.
6. Two consecutive `MEASUREMENT_INVALID` on this packet -> the session-scale
   staleness question is PARKED for Frontier and the guard-design burden returns to
   Graph/Runtime, rather than a third attempt.

---

## 17. Validity threats, representation loss, and disclosed power limits

1. **Single vantage.** One runner, one egress IP. Nothing here transfers to
   another vantage, and the pre-2.0 C-FRESHNESS line already shows endpoint
   classes can be vantage-specific.
2. **No JavaScript.** Client-rendered content is not measured. A page whose
   server HTML is stable but whose rendered DOM changes would be counted as
   unchanged. This is a first-order limitation for the product question and is
   stated in the certification scope.
3. **Attribute blindness of the primary channel.** By construction and by offline
   test. Quantified live as `M-CHANGE-ATTR-ONLY-*` and bounded by
   `M-HAZARD-BYTE-UB95-*`.
4. **Four hosts, one page class.** Same-host `<a>` navigation inside four
   documentation sites is not a sample of the Web. The `C-CROSSSITE` question is
   untouched by this packet.
5. **Survivor conditioning.** Only pages 200 at both observations enter the change
   estimand. Pages that die or become unreachable are reported separately
   (`M-DEAD-*`, `M-UNREACHABLE-*`) and a stratum above 20 % censoring refuses
   certification rather than certifying on survivors.
6. **Host x depth confound.** Partly irreducible on this frame: pandas and rust
   dominate different strata differently. Handled by `M-HOST-TABLE`,
   `M-HOSTS-WITH-BOTH-STRATA`, the `__HOST_CONCENTRATED` and
   `__DEPTH_NOT_IDENTIFIABLE` tags, and by refusing the concentration claim when
   fewer than two hosts span both strata.
7. **URL-class confound.** Deep pages are overwhelmingly `MOVING_ALIAS`; shallow
   pages are more mixed. Reported per stratum as `M-CLASS-FRAC-*` with per-class
   change counts, and guarded by `__BOUNDED_TO_VERSION_PINNED`.
8. **Power ceiling on the contrast.** About 1.6 % deep hazard (§13). A
   `M-CONCENTRATION-DETECTED = false` result bounds concentration at that level and
   says nothing about smaller real differences.
9. **Certification is window-scoped.** Every bound carries `M-DT-MEDIAN-S`. Reuse
   at lags beyond the measured `DT` is outside the certification, and the
   days-to-weeks band remains structurally undecidable on this evidence (pre-2.0,
   sha `81aba1e898d9`).
10. **Transport noise.** Two GETs of the same URL seconds apart could differ for
    CDN or compression reasons. Bounded by the in-frame self-pair null, the static
    null anchors, and the byte-vs-text disagreement metrics. The `Date` header is
    not hashed because it is outside the body.
11. **Retrospective instrument instance.** The retrospective comparison uses a
    *different execution* of the same code with the same UA. If a host serves
    content that varies by User-Agent or edge, the signature is a single host
    dominating its own change rate, which is exactly the `negotiation_suspected`
    gate.
12. **Residual attack accepted.** A single ~6-minute window cannot characterise a
    full human session; a multi-session or multi-day characterisation would need
    the harness to hold a frame for days, which the pre-2.0 program already
    demonstrated it cannot do. This is why the retrospective channel exists and
    why its absence is a stated limit, not a hidden one.

---

## 18. Consequences

**Positive (`CERTIFY_BOTH_AT_0P01` / `_0P02`).** Product may skip a zero-GET
intra-session freshness guard for a named stratum of credential-free,
server-rendered documentation pages at reuse lags up to `DT`, at the certified
level, for this host class and vantage. `CERTIFY_SHALLOW_GUARD_DEEP` converts an
open question into a hop-depth-scoped guard requirement — exactly the Director's
stated counterfactual, and exactly where Graph's resolver and Runtime's denylist
work would need a guard. A non-zero retrospective channel at 0.5-2 days would
license a TTL-shaped policy (reuse without GET, revalidate after `T`) instead of an
unconditional intra-session guard. **No promotion, no Product Core entry, no
shipped number.**

**Negative (`GUARD_REQUIRED_*`, `CERTIFY_*_GUARD_*`).** The guard question stays
open and becomes hop-depth-scoped; guard design must target the stratum whose
bound failed, with the measured sensitivity as the requirement.

**Refusal / invalid (`REFUSE_CERTIFY_*`, `NO_DATA_*`).** The decision stays
exactly where it is — unknown — with a named blocker, at a cost of ~460 s instead
of an open-ended cycle.

**In every branch**, `C-WEB-DYNAMICS` stays `HYPOTHESIS`. A certification is a
bounded measurement about a page class, not evidence of predictive dynamical
structure; a guard-required outcome is likewise a bounded measurement. No
self-promotion is available or permitted (`spec.json#claim_ceiling_rules`).

---

## 19. Freeze artifacts

Mutable local files whose identity can change the interpretation, to be hashed by
the freezer into `freeze.json.artifact_hashes`:

| path | why it binds |
|---|---|
| `research/experiments/EXP-FRONTIER-38940047535/execute_module.py` | the transport / `norm` / `is_asset` / `static_links` / `fetch` policy this module reuses verbatim |
| `research/experiments/EXP-FRONTIER-38940047535/run/raw/census.jsonl` | design-time deep-stratum topology evidence **and** the retrospective channel's observation-0 reference |
| `research/experiments/EXP-FRONTIER-38940047535/provenance.json` | the observation-0 window timestamps from which the retrospective separation is computed |
| `research/experiments/EXP-FRONTIER-38940047535/result.json` | the parent defect metrics this packet repairs |
| `research/experiments/EXP-FRONTIER-38940047535/audit.json` | the audit findings that define the repairs (R1-R5) |
| `research/experiments/EXP-FRONTIER-38940047535/handoff.json` | the four-way continuity state carried in §3 |
| `research/experiments/EXP-FRONTIER-38940047535/freeze.json` | the hash chain verifying the parent's census identity |
| `codex/claim_state.json` | effective epistemic state of `C-WEB-DYNAMICS` / `C-CROSSSITE` / `C-FRESHNESS` |
| `research/claims/registry.json` | claim ids, statuses and owner lanes |
| `research/lanes/registry.json` | lane-charter authority for `claim_ids` |

The executed module is pinned by `DERIVED_SHA256` inside this hashed `prereg.md`.

---

## 20. Mandate fidelity and unresolved at freeze

**Fidelity.** The Director's question is answered as asked: a two-observation
census diff on a fetch-complete frame (fetch-until-budget with a stratum-reserved
policy, not discover-until-budget), with a demonstrated live positive sensitivity
control, stable null controls, censoring-aware exact per-page bounds, explicit
certification or refusal of named zero-GET staleness tolerances inside one
session, no persistence store, no revalidation ladder, no cold-vs-store cost
comparison, and the claim carried by `C-WEB-DYNAMICS` rather than `C-CROSSSITE`.
The design is materially different from the pre-2.0 precedents in question,
substrate, treatment, statistic, falsifier and control (§2); it replicates and
repairs one pre-2.0 instrument lesson (§2.2); it instantiates the pre-2.0 event
taxonomy rather than re-deriving it (§2.3); and it closes the exact gap the
pre-2.0 TTL protocol was blocked from closing (§2.4).

**Unresolved at freeze (not to be settled by re-design after outcomes).**

- Whether the *product* tolerance should be 1 %, 2 % or 5 % is a Product decision;
  this packet certifies what the data support and leaves the choice explicit.
- Whether a hop-depth-stratified guard or a single global TTL is the better
  architecture depends on how often `hop >= 3` state is actually reused, which this
  packet does not measure.
- The days-to-weeks band, JavaScript-rendered content, authenticated pages and
  additional vantages remain open.
- `C-FRESHNESS` guard calibration (owner lanes graph/runtime/product) consumes the
  certified tolerances but is not in scope here.