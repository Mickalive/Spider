# EXP-FRONTIER-39053910903 preregistration

Lane: `frontier`. Target claim: `C-WEB-DYNAMICS`. Design contract: v2.
Status at DESIGN: **NOT YET FROZEN.** This file, together with `request.json` and `spec.json`,
is hashed by `scripts/freeze_experiment.py` before any live observation of the frozen question
exists. Nothing in it may be edited after `freeze.json` exists.

---

## 1. Identity and binding direction

| field | value |
|---|---|
| experiment_id | `EXP-FRONTIER-39053910903` |
| lane | frontier (`research/lanes/registry.json`: enabled, priority_claims `[C-WEB-DYNAMICS, C-RESIDUAL-NOVELTY, C-SEMANTIC-RESOLVE, C-CROSSSITE]`, allowed_code_roots `[research/harness, research/frontier]`) |
| director_mandate | `CONTINUE`, claim `C-WEB-DYNAMICS`, cycle `39052673008`, cognitive_reset performed, parent_handoff_disposition `USE` |
| parent_handoff | `research/experiments/EXP-FRONTIER-39039638199/handoff.json`, sha256 `92aef32b7467ff478e4b50343eed451b2bedde4268ab9b21c0e0ae0dea00add2` (read in full at DESIGN) |
| frozen claim_ids | `["C-WEB-DYNAMICS"]` — the only claim in the frontier lane charter's priority list that this packet may update. `C-FRESHNESS` and `C-PRODUCT-ECON` are declared **consumers**, not in-scope claim updates (`freeze_experiment.py` rejects claim ids outside the lane charter) |
| effective claim status at DESIGN | `codex/claim_state.json` `effective_event_by_claim["C-WEB-DYNAMICS"] = HYPOTHESIS` |

The Director's mandate is binding and this design follows it without drift: hash-pinned
observation-0 census as a genuine first observation, exactly the two named DESIGN repairs,
an envelope-safe checkpointed structure spanning more than the harness window, a certify-or-refuse
decision at lags inside the mandated `[6 h, 30 d]` band, and an explicit refusal path. The parent
handoff's `next_question` is advisory continuity state; its PARK instruction on the
C-CROSSSITE persistence-economics subthread is honoured (this packet contains no store, no
revalidation ladder and no cold-versus-store cost comparison).

---

## 2. Question, hypothesis, falsifier

**Question.** Using the frozen observation-0 census of `EXP-FRONTIER-39039638199`
(1107 admitted pages with per-page structural-text and byte hashes captured
`2026-10-17T15:10:35.398909Z .. 15:11:11.988909Z`) as a genuine first observation, with the two
admission defects the parent audit verified repaired by construction, can an envelope-safe,
checkpointed second observation certify — or explicitly refuse to certify — a zero-GET
structural-text tolerance at realistic session-reuse lags inside `[6 h, 30 d]`, on the same
four-host credential-free server-rendered documentation frame: does the accepted ~7-minute
`CERTIFY_BOTH_AT_0P01` bound hold as the window grows, decay into a TTL-shaped revalidation
requirement whose interval is licensed by nesting, or decay into a mandatory guard; and what is the
first live per-page hazard bound for the hours-to-days band that the pre-2.0 program structurally
could never measure?

**H1 (primary, certification).** For the frozen 1107-page frame at a measured separation `W`
inside `[6 h, 30 d]`, the exact one-sided 95 % Clopper–Pearson upper bound on the per-page
probability that the primary structural-text channel differs between the frozen observation-0
capture and this packet's second observation is at or below a named level `L ∈ {0.01, 0.02, 0.05}`,
separately for the `hop<=2` (SHALLOW) and `hop>=3` (DEEP) strata.

**H2 (window-growth contrast; the decision-relevant novelty).** A matched same-page, same-instrument,
same-vantage comparison of the long window `W` against an in-launch short window of 360 s over the
identical 1107 URLs either fails to separate at this power (fewer than 5 long-window-only discordant
pages, exact one-sided conditional-binomial `p > 0.05`) or detects positive growth (≥5
long-window-only discordant pages at `p ≤ 0.05`). Any short-window-only discordant page is declared
**REVERTING CHURN** — a page that differed between the two in-launch observations but equalled the
frozen observation-0 capture — which lowers the completeness of the differ-at-instant-`W` bound
without making it wrong for a single reuse point.

**H3 (bounded negative alternative, equally acceptable).** If either stratum's bound exceeds the
coarsest grid level `0.05`, or either stratum's censoring exceeds `CENSOR_MAX = 0.20`, or either
stratum's paired `n` falls below `MIN_N_PER_STRATUM = 60`, or `W` falls outside `[6 h, 30 d]`, the
packet **refuses to certify** and reports the guard requirement at its measured sensitivity.

**H4 (declared UNKNOWN, explicitly not tested).** JavaScript-rendered content; authenticated pages;
any egress vantage other than this runner; every lag beyond `W`; the `>72 h` sub-band unless the
launch delay actually lands there; the product's choice among 1 % / 2 % / 5 %; and whether
hop-depth-scoped guarding beats one global TTL in real sessions.

**Falsifier.** H1 is falsified for a stratum when its exact one-sided 95 % UB95 exceeds `0.05`
(first reachable at 25/686 deep or 14/421 shallow), or its censoring exceeds `0.20`, or its paired
`n < 60`, or `W` is outside the band. H2 is falsified in the growth direction when the exact
one-sided `p` for long-window-only discordant pages is `≤ 0.05`, and in the reverse direction when
short-window-only pages dominate. The **measurement** (never the science) is invalidated when any
offline canary fails, the repaired parser cannot reproduce the four frozen epoch anchors, the
anchor-consistency check fails, the frozen census hash mismatches, the frozen×frozen 14.4 h byte
canary fails to reproduce bit-for-bit, no live positive control fires, any null anchor or in-frame
self-pair changes, the GET ledger does not reconcile within 3200, or the module's self-hash is not
recorded.

---

## 3. Inherited state, preserved exactly

### 3.1 Established (accepted Codex evidence, not re-litigated here)

- `EXP-FRONTIER-39039638199`: 0/1107 structural-text changes at a median separation of 407.97 s;
  exact one-sided 95 % UB95 = `0.004357435376452668` (deep, n=686) and `0.007090496587222661`
  (shallow, n=421); frozen label `CERTIFY_BOTH_AT_0P01`; `audit.json` status `PASS`,
  `producer_claim_supported=true`, `required_fixes=[]`; Director-recomputed match on every
  load-bearing metric. **Its window is 7 minutes. This packet measures a window ≥ 60× longer and
  does not re-adjudicate that label.**
- Instrument sensitivity demonstrated live, not assumed: 3/3 volatile URLs changed, 2/2 static
  anchors and 10/10 in-frame self-pairs stayed silent, 35/35 offline controls passed. The same
  control set is reused here unchanged.
- A fetch-complete, stratum-reserved, level-ordered crawl produced the frozen population
  (deep 686 / shallow 421, all four hosts in both strata, no starvation). This packet **inherits
  that population** and performs no crawl at all.
- Page-gone is a distinct event class from content change (404/410 with its own bound; 429/403/503
  counted separately).
- `C-WEB-DYNAMICS` remains `HYPOTHESIS`; the parent's frozen ceiling `CC-C`/`CC-D` forbids
  promotion from a page-class hazard measurement, and this packet adopts the same ceiling (§17).

### 3.2 Rejected (preserved, not weakened, not reused as evidence)

- The parent's retrospective channel is **not** cited as a bound: its recorded window was
  `-497831.608 h`. What is reused is its frozen *input* (the grandparent census and its
  fractional-second provenance anchors) and its recorded arithmetic, recomputed here as a
  deterministic zero-GET canary.
- A transport-channel validity gate is **rejected**. In the parent's accepted raw rows all 359 of
  1107 transport moves came from `pandas.pydata.org` `Last-Modified` values moving with zero text
  change, so such a gate would test one host's header policy, not the measurement.
- Byte-identity at 0.01 is not certifiable on this frame (parent byte UB95 `0.011264` deep,
  `0.021609` shallow, even at 7 minutes). A product requiring byte-identity needs a guard whatever
  the text channel certifies; this packet keeps byte tags for exactly that reason.
- Site-native discovery stays closed (0/208 within ≤3 charged GETs, `EXP-FRONTIER-38184956362`) and
  is not re-run. C-CROSSSITE stays `HYPOTHESIS` and its persistence-economics thread stays parked.

### 3.3 Unknown (this packet addresses or explicitly does not)

| inherited unknown | disposition here |
|---|---|
| hours-to-days band UNDECIDED; long-window channel NOT ADMITTED | **addressed** — the channel is rebuilt with both repairs, gated by its own admission rule, and is the primary estimand |
| does 0.01 hold as the lag grows | **addressed** — matched short-window contrast, growth contrast, three-point byte ladder, nesting lemma |
| cause of the 359 transport moves | **not solved** — stays a covariate; the cause remains open and is stated, not guessed |
| which tolerance (1 % / 2 % / 5 %) the product should adopt | **not decided here** — Product's decision; this packet certifies only what the data support |
| whether C-FRESHNESS should record a bounded negative for the guard requirement | **consumer-lane decision** — this packet supplies the bound and does not take the decision |

### 3.4 Do-not-assume carried forward verbatim (plus this packet's own)

1. Do **not** read the parent's `CERTIFY_BOTH_AT_0P01` as "no freshness guard is ever needed": it
   is a structural-text-channel, four-host, one-vantage, credential-free, GET-only, server-rendered
   bound at a 7-minute window.
2. Do **not** extrapolate any bound to the days-to-weeks band or any other timescale. This packet's
   bound carries its own measured window and its own sub-band, and `L1-WINDOW-NESTING` extends a
   certification only to **smaller** lags.
3. Do **not** cite the re-admitted legacy byte ladder as a structural-text result: the grandparent
   census carries no text hashes, so it is byte-only and shallow-biased.
4. Do **not** treat the `VERSION_PINNED` class as certified: at n=23 a zero would be true by
   construction; the frozen power gate declares it underpowered.
5. Do **not** read "no window-growth detected" as "no window-growth": the contrast is underpowered
   below 5 long-window-only discordant pages and its MDC is reported.
6. Do **not** treat the frozen frame as a sample of the Web.
7. Do **not** promote `C-WEB-DYNAMICS` from this packet under any branch.

---

## 4. The frozen population and its epoch anchor

**Population.** Exactly the 1107 rows of
`research/experiments/EXP-FRONTIER-39039638199/run/raw/census.jsonl`
(sha256 `45e426fd298af4cbfb7b5167a8c7498504ef6db36314053f6b3cf45c299a21ff`) with `status == 200`
and a non-null `text_sha256`, unique by URL, carrying `hop` and `host` from the same rows.

Structure, computed at DESIGN from that frozen file (structure only — it contains no second
observation and therefore no hazard quantity):

| quantity | value |
|---|---|
| rows / admitted / excluded | 1119 / 1107 / 12 |
| excluded reasons | 6× HTTP 404, 6× malformed-URL transport errors (`InvalidURL`, readthedocs Terms-of-Service hrefs) |
| deep (hop≥3) / shallow (hop≤2) | 686 / 421 |
| hop histogram | {0:4, 1:138, 2:279, 3:543, 4:143} |
| host × stratum | rust 220/43, pytest 219/98, readthedocs 28/140, pandas 219/140 |
| classes ALL | MOVING_ALIAS 713, OTHER 371, VERSION_PINNED 23 |
| classes deep / shallow | 439/225/22 and 274/146/1 |
| max host concentration | 0.321 deep, 0.333 shallow (warn 0.60) |
| version-pinned share | 0.032 deep, 0.002 shallow (warn 0.80) |

**Epoch anchor.** The observation-0 rows carry only the parent process's `time.monotonic()`
`t_start`/`t_end`, which are not convertible to epoch. The epoch window therefore comes from three
cross-checked frozen artifacts:

| artifact | field | value | role |
|---|---|---|---|
| `.../39039638199/run/raw/PROGRESS.json` | `started_utc` | `2026-10-17T15:10:35.398909+00:00` | observation-0 window **start** |
| `.../39039638199/run/raw/PROGRESS.json` | `obs0.wall_s` | `36.59` | window **width** → end `15:11:11.988909Z` |
| `.../39039638199/provenance.json` | `commands[0].started_utc` | `2026-10-17T15:10:35.398909Z` | cross-anchor (byte-identical; Δ = 0.000000000 s) |
| `.../39039638199/freeze.json` | `frozen_at` | `2026-10-17T14:46:23.389566Z` | must be ≤ start (measured 1452.0 s before) |
| `.../39039638199/provenance.json` | `commands[0].died_utc` | `2026-10-17T15:18:18.715476Z` | must be ≥ end |
| `.../38940047535/provenance.json` | `timeline_utc.scored_run_finished` | `2026-10-17T00:46:04.288Z (module wall clock 32.004 s by its own monotonic clock)` | secondary-ladder anchor (fractional seconds **and** trailing suffix) |

Legacy ladder anchor endpoint: `2026-10-17T00:46:04.288Z` (epoch `1792197964.288000`);
observation-0 anchor endpoint: epoch `1792249871.988909`.

Secondary-ladder census:
`research/experiments/EXP-FRONTIER-38940047535/run/raw/census.jsonl`
sha256 `37f3d87b49083e77b117bc5796f2ac9a3c4784e61e4acbf644a3c4fea1e487d7` — 926 rows, 292 admitted
with a byte hash, **no `text_sha256` and no epoch stamps**, which is why the ladder is byte-only and
why its anchor must come from the provenance timeline rather than from the rows. Its 292 admitted
URLs are a strict subset of the frozen population (overlap 292, legacy-only 0).

---

## 5. Frozen constants

Every value here is inherited verbatim from `EXP-FRONTIER-39039638199/spec.json` or from the
Director's mandate. None was chosen after any outcome was observed.

```
ALPHA = 0.05                     CERT_GRID = (0.01, 0.02, 0.05)
MIN_N_PER_STRATUM = 60           MIN_HOST_STRATUM_N = 25          MIN_HOSTS_BOTH = 2
CENSOR_MAX = 0.20                HOST_CONC_WARN = 0.60            VERSION_PINNED_FRAC_WARN = 0.80
SHALLOW_MAX_HOP = 2              (DEEP := hop >= SHALLOW_MAX_HOP + 1)
MIN_WINDOW_H = 6.0               MAX_WINDOW_D = 30.0               (mandated band)
SUBBANDS = HOURS [6,24) | DAY [24,72) | DAYS [72,720) hours
SHORT_SEPARATION_S = 360.0       DT_MIN_S = 300.0                 DT_MAX_S = 900.0
INTER_SWEEP_GAP_S = 30.0         GROWTH_ALPHA = 0.05              GROWTH_MDC_COUNT = 5
CLASS_POWER_MIN_N = {0.01: 299, 0.02: 149, 0.05: 59}
SELFPAIR_N = 10                  SELFPAIR_MAX_GAP_S = 5.0
GET_CEILING_TOTAL = 3200         GET_CEILING_PER_SWEEP = 1300      PER_HOST_GET_CEILING_PER_SWEEP = 800
CIRCUIT_BREAK_RATE_LIMIT_N = 10  (halts a host's remaining fetches; can only lose power)
MODULE_WALL_BUDGET_S = 900.0     WORKERS = 6   PER_HOST_CONCURRENCY = 2   PER_HOST_SPACING_S = 0.10
REQUEST_TIMEOUT = 12.0           MAX_BODY_BYTES = 8_000_000       UA = "spider-r2/1.0"
POS_CONTROL_URLS = [ https://www.cloudflare.com/cdn-cgi/trace,
                     https://api.github.com/rate_limit,
                     https://timeapi.io/api/Time/current/zone?timeZone=UTC ]
NULL_CONTROL_URLS = [ https://example.com/ , https://www.iana.org/domains/reserved ]
```

Transport policy is imported from the hash-pinned parent module and is **identical on both sweeps**,
so the short/long contrast cannot be explained by sweep policy.

---

## 6. The two mandated repairs, and three further defects this DESIGN found

### R1 — closed, fractional-second-tolerant anchor parser (mandated)

The parent's `parse()` used `datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")` and returned `None` for
anything not ending in `Z`. DESIGN reproduced **two distinct** failure modes on the real artifacts:

| input | parent's parser |
|---|---|
| `2026-10-17T15:10:35.398909+00:00` | returns `None` **silently** (does not end in `Z`) |
| `2026-10-17T00:45:32.184Z` | raises `ValueError` |
| `2026-10-17T00:46:04.288Z` | raises `ValueError` |

The silent `None` is the more dangerous of the two: it converts a parse failure into "no window"
rather than into an error.

Frozen replacement:

```python
TS_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})')

def parse_epoch(s, field):
    """Strict ISO-8601 instant -> POSIX epoch seconds. NEVER returns None."""
    if not isinstance(s, str):
        raise ValueError("anchor %s: not a string: %r" % (field, s))
    m = TS_RE.match(s.strip())
    if not m:
        raise ValueError("anchor %s: unparseable ISO-8601 prefix: %r" % (field, s))
    y = int(m.group(1))
    if not (2000 <= y <= 2100):
        raise ValueError("anchor %s: year out of range: %r" % (field, s))
    frac = m.group(7) or ".0"
    off = "+00:00" if m.group(8) == "Z" else m.group(8)
    iso = "%04d-%02d-%02dT%02d:%02d:%02d%s%s" % (y, int(m.group(2)), int(m.group(3)),
                                                 int(m.group(4)), int(m.group(5)),
                                                 int(m.group(6)), frac, off)
    try:
        return datetime.fromisoformat(iso).timestamp()
    except ValueError as exc:
        raise ValueError("anchor %s: out-of-range ISO-8601 instant %r (%s)"
                         % (field, s, exc)) from exc
```

The trailing parenthetical in the legacy `scored_run_finished` value is removed by the
`^`-anchored match, never by ad-hoc string surgery, and the field name is carried into the error so
a failure names which anchor broke. The parser is *closed*: every non-conforming input raises.

Verified at DESIGN on the four real anchors → epochs `1792249835.398909`, `1792249835.398909`,
`1792197932.184000`, `1792197964.288000`.

### R2 — single POSIX-epoch clock (mandated)

The parent computed `dt_h = (rec["t_start"] - p_end)/3600` where `rec["t_start"]` is
`time.monotonic()` from inside `fetch()` and `p_end` is a POSIX epoch: two different clocks.
Its own `run/derived/retro_secondary.json` records `dt_h_min -497831.61`, `dt_h_median
-497831.608`, `dt_h_max -497831.606`, which is why the channel was not admitted.

Frozen rule: **every duration in this packet is a difference of two POSIX-epoch values.**
`time.monotonic()` is confined to wall-budget accounting and is never subtracted from or added to
an epoch value. DESIGN reproduced the prohibited construction on this runner and obtained about
`-497832 h`, confirming the mechanism; the repaired path yields `W = 7.756 h`.

### D3 — anchor consistency (found by this DESIGN, not in the parent audit)

The parent had no anchor-consistency check, so one mis-sourced timestamp would have silently
defined the whole window. Frozen control `C-ANCHOR-CONSISTENCY` over the four artifacts of §4,
failure ⇒ `NO_DATA_CONTROL_OR_INPUT_FAIL`.

### D4 — window quantisation declared and bounded (found by this DESIGN)

Per-page `dt` at the long window is not directly recoverable (obs0 rows carry monotonic stamps only),
and the imported `fetch()` may not be modified. Frozen rule `V7`: wrap every live fetch so that
`time.time()` is read immediately **before** and immediately **after** the parent `fetch()` call,
giving every OBS1 and OBS2 page its own epoch bracket `[epoch_pre, epoch_post]` on the same POSIX
clock. Then, per page,

```
dt_h_min(p) = (epoch_pre(p)  - observation0_window_END)   / 3600
dt_h_max(p) = (epoch_post(p) - observation0_window_START) / 3600
```

The admission gate uses the **most conservative single number available**,
`W = min over pages of dt_h_min(p)`; `M-W-H-PRIMARY-MEDIAN` and `M-W-H-PRIMARY-MAX` are reported
alongside; every bound is stated at the admitted `W`. Observation-side quantisation is 36.59 s
(**0.131 %** of a 7.756 h window); the fetch-side bracket adds at most the 12 s request timeout plus
transfer time, which widens the interval only in the conservative direction. Per-page `dt` for the
in-launch short window is exact to the same bracket and is admitted under `V9`.

### D5 — the legacy ladder costs zero extra GETs (found by this DESIGN)

The parent spent 292 GETs re-fetching the grandparent census. DESIGN verified that census is a
**strict subset** of the frozen observation-0 population: overlap **292**, legacy-only **0**
(deep 31 / shallow 261; readthedocs 168, pytest 101, pandas 13, rust 10). The same three window
points are therefore obtained from already-frozen rows plus this packet's OBS1 rows at **zero**
marginal GET cost, and every foreign input is hash-bound in `freeze.json.artifact_hashes`.

---

## 7. Measurement design

Stdlib-only Python 3.12. No browser, no JavaScript engine, no LLM, no credentials, no `pip
install`, no Docker. The detector, canonicalisation, fetch policy and bound arithmetic are
**imported** from the hash-pinned parent module, so the instrument is literally the audited one.

### 7.1 Instrument identity

`research/experiments/EXP-FRONTIER-39039638199/run/execute_module.py`
sha256 `5d2509f691193c610a9797e4c473ee9425c010c1a4bd35f65b43e3aca672c573`, in
`spec.freeze_artifacts`, re-verified at load time **and** against its own recomputed stripped
self-hash. Reused: `canon`, `text_sha`, `norm`, `is_asset`, `url_class`, `fetch`, `fetch_many`,
`binom_tail`, `cp_ub95`, `cert_level`, `contrast_p`, `mdc_deep_rate`, `offline_controls`,
`summary_control`, `synthetic_rows`.

### 7.2 Stage order and envelope

```
S0  offline controls (in-process HTTP fixture; 8 fixture GETs) + anchor/population/legacy canaries
S1  OBS1_LONG   re-fetch all 1107 frozen URLs            (~45 s, 1107 GETs)
    -> atomic write raw/obs1_long.jsonl + PROGRESS checkpoint
S2  inter-sweep politeness gap                          (30 s, 0 GETs)
S3  short-window separation                            (360 s in-process sleep)
S4  OBS2_SHORT  re-fetch the same 1107 URLs             (~45 s, 1107 GETs)
    -> atomic write raw/obs2_short.jsonl + PROGRESS checkpoint
S5  self-pair determinism control (10 pages x 2 GETs, gap <= 5 s) + control probes (5 URLs x 2)
S6  legacy 14.4 h byte rung (0 GETs) + derived metrics, decision, legacy/class/contrast derivations
```

Projected wall ≈ **490 s** against `MODULE_WALL_BUDGET_S = 900` and the harness envelope
`SPIDER_MODEL_MAX_RUNTIME_SECONDS = 1200`. Projected live GETs ≈ **2234** against a ceiling of 3200
(1107 + 1107 + 20 + 10 live, +8 offline fixture) — **12 % fewer than the parent's 2268** while adding
a second full-frame sweep.

### 7.3 Checkpoint and envelope-safe structure

This is the mandate's "checkpointed across launches so the separation fits the envelope instead of
the ≤900 s in-process window". Concretely:

1. **The separation is obtained for free across launches.** The first observation already happened
   in a *previous* launch and is frozen with an epoch anchor; the second happens in this launch.
   Nothing sleeps for hours.
2. Every stage writes its raw artefact atomically (temp file + rename) and then updates
   `raw/PROGRESS.json` with a `launch_id`, the stage, the epoch bracket of the stage, the GET ledger
   and the module self-hash. A killed launch therefore never leaves a partial file that a later run
   can mistake for a complete one.
3. Rows from different `launch_id`s are never mixed inside one decision. If a launch dies, its rows
   are discarded and the next launch recomputes the window from its own epoch stamps — which is
   still inside the band, so the retry is a fresh valid measurement rather than a patched one.
4. The persisted, epoch-stamped `raw/obs1_long.jsonl` is the **anchor for a successor rung**: if the
   30 d band ceiling is missed and the packet refuses, a later transaction can measure from these
   rows instead of re-crawling. A paid-for observation is never wasted.

---

## 8. Window admission, sub-bands, and the nesting lemma

- Admission band: `6.0 h ≤ W ≤ 720 h`, where `W = min over pages of dt_h_min(p)` (the most
  conservative separation any page could have had; see §6/D4). Below ⇒
  `REFUSE_LONG_WINDOW_BELOW_BAND`; above ⇒ `REFUSE_LONG_WINDOW_ABOVE_BAND`. Both are
  `status=COMPLETE, outcome=INCONCLUSIVE` — a measurement-valid refusal, never a scientific negative.
- Sub-band (informational, part of the label): `HOURS [6,24)`, `DAY [24,72)`, `DAYS [72,720)`.
  Expected at DESIGN completion: primary **HOURS** (7.756 h); legacy ladder **HOURS**, entering
  **DAY** after `2026-10-18T00:46:04.288Z`.
- **Hard deadline.** The 30 d ceiling corresponds to `2026-11-16T15:11:11.988909Z`. After that the
  admission gate legitimately fails and the successor-rung property of §7.3.4 applies. The deadline
  is stated now, before freeze, so no one can be surprised by it.
- **L1-WINDOW-NESTING (frozen structural lemma, not a fitted regularity).** For a fixed page set, a
  fixed detector and fixed 200-at-both-ends, the event "the structural text at `t2` differs from the
  text at `t1`" is monotone increasing in `t2 − t1`. Therefore (i) certification at the largest
  measured window `W` implies certification at every smaller window on the same page set, and (ii) an
  upper bound at `W` bounds every smaller window. Hence **`M-TTL-LICENSED-LAG-H` is exactly the
  measured `W`** in every certifying branch, and nothing beyond it may be claimed. The lemma is void
  where reverting churn exists — which is precisely why the short-window channel is measured and its
  short-window-only discordant pages are reported.

---

## 9. Comparators, contrasts and decompositions (all reported; none can change the primary label)

1. **Matched short-window comparator.** Identical URLs, instrument, vantage, sweep policy and clock;
   only `Δt` differs (360 s vs `W`). Supplies the short-window hazard bound
   (`M-SHORT-HAZARD-TEXT-UB95-*`, `M-SHORT-CERT-LEVEL-*`), the second half of the paired growth
   contrast, an in-run demonstration that the repaired code detects change on this frame, and a direct
   replication of the parent's nominal separation under this packet's code.
2. **Inherited accepted comparator.** `EXP-FRONTIER-39039638199`'s audited 7-minute result
   (`0/1107`, UB95 `0.004357` / `0.007090`, `CERTIFY_BOTH_AT_0P01`). Cited, never combined
   arithmetically with the long window.
3. **Window-growth contrast.** Per page: `L = 1` if text changed obs0→OBS1, `S = 1` if text changed
   OBS1→OBS2. `a` = long-only, `b` = short-only. Exact one-sided conditional-binomial
   `p = 2^(−(a+b)) · Σ_{i≤b} C(a+b, i)`, direction "long > short"; `a ≤ b ⇒ p = 1`. Classification:
   `GROWTH_DETECTED_LONG` (`a>b`, `p ≤ 0.05`), `GROWTH_NOT_DETECTED`, `GROWTH_UNDERPOWERED`
   (`a=b=0`). Exact values, DESIGN-verified: `a=5,b=0 → 0.03125`; `a=4,b=0 → 0.0625`; `a=6,b=1 →
   0.0625`. **`GROWTH_MDC_COUNT = 5`** is the minimum detectable discordant count and is frozen.
4. **Depth contrast, two-sided.** Exact one-sided tails in **both** directions for `p_deep` vs
   `p_shallow`, plus MDC rates for both. Reported only. A one-directional test would be rigged: the
   most active host (readthedocs, 168 pages) contributes 140 of its pages to SHALLOW, so the
   shallow>deep direction is a live possibility at an hours window.
5. **Per-class decomposition with a frozen power gate.** For `MOVING_ALIAS`, `OTHER`,
   `VERSION_PINNED` over ALL: `n`, `k`, UB95, `cert_level`, and a verdict
   `CERTIFIABLE` / `CLASS_UNDERPOWERED` where a class certifies nothing unless
   `n ≥ 299 / 149 / 59` for level `0.01 / 0.02 / 0.05`. DESIGN-expected verdicts at `k=0`:
   MOVING_ALIAS (n=713) UB `0.00419` → 0.01 **CERTIFIABLE**; OTHER (n=371) UB `0.00804` → 0.01
   **CERTIFIABLE**; VERSION_PINNED (n=23) UB `0.12212` → **CLASS_UNDERPOWERED**. This decomposition is
   the one the 7-minute zero made impossible, and it is the one that would license a
   class-scoped (version-pin-the-URL) guard policy instead of one global policy.
6. **Secondary three-point byte ladder (0 extra GETs), on the 292-page subset, SECONDARY:**

   | rung | window | channel | n | source |
   |---|---|---|---|---|
   | P0 (`M-LEGACY14H-*`) | ≈14.4 h | byte | 292 | grandparent anchor → frozen obs0 (frozen × frozen) |
   | P3 (`M-LEGACYPLUS-*`) | ≈`W` | byte | 292 | frozen obs0 → this packet's OBS1 (subset of primary rows) |
   | P4 (`M-LONGPLUS-*`) | ≈`W`+14.4 h | byte | 292 | grandparent anchor → this packet's OBS1 |

   P0 is simultaneously a **deterministic zero-GET reproduction canary** (§13, control family 3).
   The whole ladder is byte-only, shallow-biased, nested inside the primary population, and can
   never be stronger than the primary bound.

---

## 10. Frozen metric identities

Full list in `spec.json#metric_ids` (143 ids). Naming convention:
`M-W-H-*` window, `M-N-PAIR-*` paired n, `M-CHANGE-TEXT-*` primary channel events,
`M-CHANGE-BYTE-*` conservative channel, `M-CHANGE-ATTR-ONLY-*` the channel's measured blind spot,
`M-CHANGE-TRANSPORT-*` covariate, `M-HAZARD-*-UB95-*` exact bounds, `M-CERT-LEVEL-*` ladder levels,
`M-CENSORED-*` / `M-CENSOR-FRAC-*` / `M-DEAD-*` / `M-RATE-LIMITED-*` censoring channels,
`M-SHORT-*` in-launch short-window channel, `M-GROWTH-*` growth contrast, `M-DEPTH-CONTRAST-*` depth
contrast, `M-CLASS-*` class decomposition, `M-LEGACY14H-*` / `M-LEGACYPLUS-*` / `M-LONGPLUS-*` the
secondary ladder rungs, `M-TTL-LICENSED-LAG-H` the nesting-limited TTL, `M-LIVE-POS-*` /
`M-LIVE-NULL-*` / `M-SELFPAIR-*` live control families, `M-GETS-*` the ledger, `M-LAUNCH-ID` /
`M-WALL-S` / `M-PARTIAL` provenance, `M-DECISION-LABEL` the frozen label.

Identity mapping to the parent packet (so AUDIT and downstream agents can compare across packets):
`M-RETRO-{N,CHANGE-BYTE,UB95,CERT-LEVEL}-{ALL,DEEP,SHALLOW}` in
`EXP-FRONTIER-39039638199` corresponds to `M-LEGACYPLUS-*` here — the same comparison structure with
a **repaired** window instead of `-497831.608 h`. The parent's `M-RETRO-INFO` is not inherited: its
`admitted=false` state is superseded by this packet's own admission gate, and its value is retained
as the P0 canary expectation.

---

## 11. Frozen decision rule

`decide(m)` is a total, ordered, disjoint function over thirteen frozen inputs. Full source and
canary table in §12.

- **Step 0 — validity (never a scientific negative).** Not `control_ok` or not `obs0_integrity_ok`
  ⇒ `NO_DATA_CONTROL_OR_INPUT_FAIL`, `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.
  `control_ok` covers every offline canary, the repaired parser reproducing the four anchors, the
  anchor-consistency check, the frozen census hash, the 14.4 h reproduction canary, ≥1 live positive
  control firing, 0 null-anchor changes and 0 self-pair changes. Ledger not reconciling within 3200
  ⇒ `NO_DATA_LEDGER_FAIL`, `MEASUREMENT_INVALID`.
- **Step 1 — frame power.** `n_deep < 60 or n_shallow < 60` ⇒ `REFUSE_LONG_INSUFFICIENT_N`
  (`COMPLETE`, `INCONCLUSIVE`).
- **Step 2 — window admission.** `W < 6 h` ⇒ `REFUSE_LONG_WINDOW_BELOW_BAND`; `W > 720 h` ⇒
  `REFUSE_LONG_WINDOW_ABOVE_BAND` (both `COMPLETE`, `INCONCLUSIVE`). Else `band` = HOURS / DAY / DAYS.
- **Step 3 — censoring.** `censor_frac_s > 0.20` ⇒ `REFUSE_LONG_CENSORED_{DEEP|SHALLOW|DEEP_SHALLOW}`.
- **Step 4 — primary certification.** `L = cert_level(k_text, n)` per stratum. Both `None` ⇒
  `GUARD_REQUIRED_LONG_BOTH_STRATA` (`COMPLETE`, `FALSIFIES`). Deep `None` only ⇒
  `GUARD_REQUIRED_LONG_DEEP_ONLY` (`COMPLETE`, `MIXED`). Shallow `None` only ⇒
  `GUARD_REQUIRED_LONG_SHALLOW_ONLY` (`COMPLETE`, `MIXED`). Both ⇒
  `CERTIFY_LONG_BOTH_AT_<max(L_deep,L_shallow)>` (`COMPLETE`, `SUPPORTS`).
- **Step 5 — narrowing tags only.** `BAND_<sub-band>` (informational), `DEPTH_NOT_IDENTIFIABLE`
  (`hosts_both < 2`), `HOST_CONCENTRATED` (≥0.60), `BOUNDED_TO_VERSION_PINNED` (≥0.80),
  `BYTE_IDENTITY_NOT_CERTIFIED_<stratum>`, `CIRCUIT_BROKEN`.
- **Step 6 — reported, never decided.** Growth contrast, depth contrast, class decomposition and the
  byte ladder have **no** power over the label. Their only influence is on what the label may be
  *interpreted* to mean, and that ceiling is written down in advance (§17).

### 11.1 Reachability of every branch (exact arithmetic, DESIGN-verified)

| branch | required state at this frame size | reachable? |
|---|---|---|
| `CERTIFY_LONG_BOTH_AT_0P01` | `k_deep ≤ 2`, `k_shallow = 0` | yes — `UB95(0,686)=0.004357`, `UB95(0,421)=0.007090` |
| `..._0P02` | `3 ≤ k_deep ≤ 7` or `1 ≤ k_shallow ≤ 3` | yes |
| `..._0P05` | `8 ≤ k_deep ≤ 24` or `4 ≤ k_shallow ≤ 13` | yes |
| `GUARD_REQUIRED_LONG_*` | `k_deep ≥ 25` (deep), `k_shallow ≥ 14` (shallow) | yes — 25/686 = 0.0364, 14/421 = 0.0333; the frame's most active host alone contributes 168 pages |
| `REFUSE_LONG_CENSORED_*` | >20 % of a stratum's pages not 200 at OBS1 | yes — documentation pages are deleted; the parent's own sweep already contained 6 such 404s |
| `REFUSE_LONG_INSUFFICIENT_N` | a stratum collapses below 60 paired pages | yes, if the frozen population partially rots |
| `REFUSE_LONG_WINDOW_ABOVE_BAND` | launch after `2026-11-16T15:11:11.988909Z` | yes — a named deadline |
| `REFUSE_LONG_WINDOW_BELOW_BAND` | `W < 6 h` | **provably NOT reachable in this transaction** — the observation-0 anchor is frozen >7.7 h before DESIGN completion and the epoch clock is monotone, so `W` can only grow. Retained as defensive totality, unreachability declared here, and exercised by `C-DECIDE-LONG-WINDOW-BELOW` so the branch is known to work |
| `NO_DATA_*` | an instrument or input-integrity failure | yes — 10 offline canaries and 3 live families can each fail |

### 11.2 Self-attack log: defects this DESIGN found in its own frozen rule

1. `subband()` initially accepted `5.9 h` as `HOURS` because its first edge was `0.0` instead of
   `MIN_WINDOW_H`. **Fixed** (first edge = 6.0) and the canary table re-verified.
2. The label join emitted four underscores (`label + "__" + tags` where the tag already carried a
   leading `"__"`). **Fixed** and re-verified.
3. `growth()` returned a non-interpretable p when `a ≤ b` (e.g. `0.75` for `a=b=1`). **Fixed** to
   return `p = 1.0` with `GROWTH_NOT_DETECTED`, since the one-sided test in the hypothesised
   direction is not applicable in that direction.
4. `subband(None)` returned `ABOVE_BAND`, which is a wrong-direction error for a missing window.
   **Fixed** to `BELOW_BAND`.

---

## 12. FROZEN REFERENCE DECISION SOURCE AND CANARY TABLE (the freeze vehicle)

Because this packet's DESIGN was restricted to `spec.json` and `prereg.md`, it could not author and
byte-hash the executable module. The freeze is therefore **behavioural for this packet's own
module** (frozen rule text + frozen constants + the canary table below, all inside the hash-pinned
`prereg.md`) and **byte-hash for every external interpretation dependency** (`spec.freeze_artifacts`).
This limitation is declared, not concealed (§18).

Reference source, sha256 of the exact text in the block:
`89cafdcd4ed181682367d58a9e466ab34b5779a8babc515bdef4c4b9b06c7817`

```python
#!/usr/bin/env python3
"""FROZEN reference decision function for EXP-FRONTIER-39053910903 (design-contract v2).
Every threshold below is inherited verbatim from EXP-FRONTIER-39039638199/spec.json or
from request.json#director_mandate.allocation.question.  None was chosen after any
outcome was observed.  cp_ub95()/cert_level() are the hash-pinned parent functions."""
ALPHA = 0.05
CERT_GRID = (0.01, 0.02, 0.05)
MIN_N_PER_STRATUM = 60
CENSOR_MAX = 0.20
MIN_HOSTS_BOTH = 2
HOST_CONC_WARN = 0.60
VERSION_PINNED_FRAC_WARN = 0.80
MIN_WINDOW_H = 6.0
MAX_WINDOW_D = 30.0
GET_CEILING_TOTAL = 3200
SUBBANDS = (("HOURS", 6.0, 24.0), ("DAY", 24.0, 72.0), ("DAYS", 72.0, 720.0))
GROWTH_ALPHA = 0.05
GROWTH_MDC_COUNT = 5
CLASS_POWER_MIN_N = {"0.01": 299, "0.02": 149, "0.05": 59}


def subband(w_h):
    if w_h is None:
        return "BELOW_BAND"
    for name, lo, hi in SUBBANDS:
        if w_h is not None and lo <= w_h < hi:
            return name
    return "BELOW_BAND" if w_h < MIN_WINDOW_H else "ABOVE_BAND"


def growth(a, b):
    """Exact one-sided binomial (McNemar) test that long-window-only events (a)
    outnumber short-window-only events (b) at GROWTH_ALPHA; a is the count in the
    hypothesised direction.  Returns (p, classification)."""
    import math
    n = a + b
    if n == 0:
        return 1.0, "GROWTH_UNDERPOWERED"
    if a <= b:
        return 1.0, "GROWTH_NOT_DETECTED"
    p = sum(math.comb(n, i) for i in range(0, b + 1)) / (2.0 ** n)
    return p, ("GROWTH_DETECTED_LONG" if p <= GROWTH_ALPHA else "GROWTH_NOT_DETECTED")


def decide(m):
    # STEP 0 -- measurement validity (never a scientific negative)
    if not m["control_ok"] or not m["obs0_integrity_ok"]:
        return {"label": "NO_DATA_CONTROL_OR_INPUT_FAIL", "status": "MEASUREMENT_INVALID",
                "outcome": "NOT_APPLICABLE", "certified_deep": None, "certified_shallow": None,
                "reason": "a frozen offline/live control, or the obs0 anchor integrity check, failed"}
    if not m["ledger_ok"]:
        return {"label": "NO_DATA_LEDGER_FAIL", "status": "MEASUREMENT_INVALID",
                "outcome": "NOT_APPLICABLE", "certified_deep": None, "certified_shallow": None,
                "reason": "GET ledger did not reconcile within GET_CEILING_TOTAL"}
    # STEP 1 -- frozen population power
    if m["n_deep"] < MIN_N_PER_STRATUM or m["n_shallow"] < MIN_N_PER_STRATUM:
        return {"label": "REFUSE_LONG_INSUFFICIENT_N", "status": "COMPLETE",
                "outcome": "INCONCLUSIVE", "certified_deep": None, "certified_shallow": None,
                "reason": "paired n below MIN_N_PER_STRATUM=60"}
    # STEP 2 -- window admission against the Director's [6 h, 30 d] band
    w = m["w_h"]
    if w is None or w < MIN_WINDOW_H:
        return {"label": "REFUSE_LONG_WINDOW_BELOW_BAND", "status": "COMPLETE",
                "outcome": "INCONCLUSIVE", "certified_deep": None, "certified_shallow": None,
                "reason": "measured window below the mandated 6 h floor"}
    if w > MAX_WINDOW_D * 24.0:
        return {"label": "REFUSE_LONG_WINDOW_ABOVE_BAND", "status": "COMPLETE",
                "outcome": "INCONCLUSIVE", "certified_deep": None, "certified_shallow": None,
                "reason": "measured window above the mandated 30 d ceiling"}
    # STEP 3 -- censoring gate, per stratum
    hot = [s for s in ("DEEP", "SHALLOW")
           if m["censor_frac_" + s.lower()] > CENSOR_MAX]
    if hot:
        return {"label": "REFUSE_LONG_CENSORED_" + "_".join(hot), "status": "COMPLETE",
                "outcome": "INCONCLUSIVE", "certified_deep": None, "certified_shallow": None,
                "reason": "observation-1 censoring above CENSOR_MAX=0.20 in " + "_".join(hot)}
    # STEP 4 -- primary certification on the structural-text channel at window w
    ld, ls = m["cert_deep"], m["cert_shallow"]
    if ld is None and ls is None:
        label, outcome = "GUARD_REQUIRED_LONG_BOTH_STRATA", "FALSIFIES"
    elif ld is None:
        label, outcome = "GUARD_REQUIRED_LONG_DEEP_ONLY", "MIXED"
    elif ls is None:
        label, outcome = "GUARD_REQUIRED_LONG_SHALLOW_ONLY", "MIXED"
    else:
        label = "CERTIFY_LONG_BOTH_AT_" + ("%g" % max(ld, ls)).replace(".", "P")
        outcome = "SUPPORTS"
    tags = ["BAND_" + subband(w)]
    if m["hosts_both"] < MIN_HOSTS_BOTH:
        tags.append("DEPTH_NOT_IDENTIFIABLE")
    if max(m["host_conc_deep"], m["host_conc_shallow"]) >= HOST_CONC_WARN:
        tags.append("HOST_CONCENTRATED")
    if max(m["verpin_frac_deep"], m["verpin_frac_shallow"]) >= VERSION_PINNED_FRAC_WARN:
        tags.append("BOUNDED_TO_VERSION_PINNED")
    if m["byte_ub_deep"] is not None and m["cert_deep"] is not None \
            and m["byte_ub_deep"] > m["cert_deep"]:
        tags.append("BYTE_IDENTITY_NOT_CERTIFIED_DEEP")
    if m["byte_ub_shallow"] is not None and m["cert_shallow"] is not None \
            and m["byte_ub_shallow"] > m["cert_shallow"]:
        tags.append("BYTE_IDENTITY_NOT_CERTIFIED_SHALLOW")
    if m["circuit_broken_hosts"]:
        tags.append("CIRCUIT_BROKEN")
    out = {"label": label + "__" + "_".join(t for t in tags), "status": "COMPLETE",
           "outcome": outcome, "certified_deep": ld, "certified_shallow": ls, "tags": tags,
           "band": subband(w)}
    if outcome == "SUPPORTS":
        out["reason"] = ("both strata certify zero-GET structural-text reuse at the measured "
                         "window (sub-band %s); nesting licenses all lags <= the measured "
                         "window on this same page set" % subband(w))
    elif label == "GUARD_REQUIRED_LONG_BOTH_STRATA":
        out["reason"] = ("both strata exceed the coarsest grid level 0.05 at the measured "
                         "window; a freshness guard is mandatory and its required sensitivity "
                         "is the reported UB95")
    else:
        out["reason"] = ("the %s stratum certifies while the other exceeds 0.05; a guard is "
                         "required only for the non-certifying stratum"
                         % ("deep" if ld is None else "shallow"))
    return out
```

### 12.1 Frozen canary table — every executed at DESIGN, all expected labels matched

Canary metric states use the frozen-frame defaults `n_deep=686, n_shallow=421,
censor_frac=0.02/0.02, hosts_both=4, host_conc=0.321/0.333, verpin_frac=0.032/0.002,
W=8.3 h` unless the row overrides them; `cert_*` values come from the hash-pinned parent
`cert_level`.

| control id | expected label | status | outcome |
|---|---|---|---|
| `C-DECIDE-LONG-CERTIFY-0P01` | `CERTIFY_LONG_BOTH_AT_0P01__BAND_HOURS` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-HOURS-EDGE-6H` (W=6.0) | `CERTIFY_LONG_BOTH_AT_0P01__BAND_HOURS` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-CERTIFY-0P02` (`cert_deep=cert_level(4,686)`, `cert_shallow=cert_level(2,421)`) | `CERTIFY_LONG_BOTH_AT_0P02__BAND_HOURS` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-CERTIFY-0P05` (`cert_level(9,686)`, `cert_level(5,421)`) | `CERTIFY_LONG_BOTH_AT_0P05__BAND_HOURS` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-GUARD-BOTH` | `GUARD_REQUIRED_LONG_BOTH_STRATA__BAND_HOURS` | COMPLETE | FALSIFIES |
| `C-DECIDE-LONG-GUARD-DEEP-ONLY` | `GUARD_REQUIRED_LONG_DEEP_ONLY__BAND_HOURS` | COMPLETE | MIXED |
| `C-DECIDE-LONG-GUARD-SHALLOW-ONLY` | `GUARD_REQUIRED_LONG_SHALLOW_ONLY__BAND_HOURS` | COMPLETE | MIXED |
| `C-DECIDE-LONG-INSUFFICIENT-N` (`n_deep=40`) | `REFUSE_LONG_INSUFFICIENT_N` | COMPLETE | INCONCLUSIVE |
| `C-DECIDE-LONG-WINDOW-BELOW` (W=4.9) | `REFUSE_LONG_WINDOW_BELOW_BAND` | COMPLETE | INCONCLUSIVE |
| `C-DECIDE-LONG-WINDOW-ABOVE` (W=760) | `REFUSE_LONG_WINDOW_ABOVE_BAND` | COMPLETE | INCONCLUSIVE |
| `C-DECIDE-LONG-CENSORED-DEEP` (0.31) | `REFUSE_LONG_CENSORED_DEEP` | COMPLETE | INCONCLUSIVE |
| `C-DECIDE-LONG-CENSORED-BOTH` (0.31 / 0.25) | `REFUSE_LONG_CENSORED_DEEP_SHALLOW` | COMPLETE | INCONCLUSIVE |
| `C-DECIDE-LONG-CONTROL-FAIL` | `NO_DATA_CONTROL_OR_INPUT_FAIL` | MEASUREMENT_INVALID | NOT_APPLICABLE |
| `C-DECIDE-LONG-INPUT-INTEGRITY-FAIL` | `NO_DATA_CONTROL_OR_INPUT_FAIL` | MEASUREMENT_INVALID | NOT_APPLICABLE |
| `C-DECIDE-LONG-LEDGER-FAIL` | `NO_DATA_LEDGER_FAIL` | MEASUREMENT_INVALID | NOT_APPLICABLE |
| `C-DECIDE-LONG-DEPTH-NOT-IDENTIFIABLE` (`hosts_both=1`) | `...__BAND_HOURS_DEPTH_NOT_IDENTIFIABLE` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-HOST-CONCENTRATED` (0.91) | `...__BAND_HOURS_HOST_CONCENTRATED` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-VERSION-PINNED` (0.85) | `...__BAND_HOURS_BOUNDED_TO_VERSION_PINNED` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-BYTE-NOT-CERTIFIED` (0.031 / 0.044) | `...__BAND_HOURS_BYTE_IDENTITY_NOT_CERTIFIED_DEEP_BYTE_IDENTITY_NOT_CERTIFIED_SHALLOW` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-CIRCUIT-BROKEN` | `...__BAND_HOURS_CIRCUIT_BROKEN` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-BAND-DAY` (W=30) | `CERTIFY_LONG_BOTH_AT_0P01__BAND_DAY` | COMPLETE | SUPPORTS |
| `C-DECIDE-LONG-BAND-DAYS` (W=120) | `CERTIFY_LONG_BOTH_AT_0P01__BAND_DAYS` | COMPLETE | SUPPORTS |

**22 canaries, 20 distinct labels, 2 intentional aliases**: the 6 h boundary canary coincides with
the `0P01` canary, and the control-failure canary coincides with the input-integrity canary because
step 0 merges them by design.

---

## 13. Controls — every one must be able to fire in both directions

1. **Inherited offline suite (35 canaries), unchanged.** Fixture detector/canonicalisation controls
   (`C-CANON-IDEMPOTENT`, `C-DETECT-TEXT-INJECTION`, `C-DETECT-ATTR-ONLY`, `C-DETECT-SCRIPT-ONLY`,
   `C-CENSOR-404-DETECTED`, `C-LIVE-DETECTOR-ON-FIXTURE`), exact-bound controls
   (`C-CP-BOUND-N60/N150/N299/K1N400`), `C-CERT-LEVEL-LADDER`, `C-CONTRAST-POWER`, 10
   `C-DECIDE-*` branch canaries + `C-DECIDE-BRANCHES-DISTINCT`, and 11 `C-SUMMARY-*` raw→derived→
   decision pipeline canaries. **DESIGN re-ran all 35 on this runner: 35/35 pass.**
2. **New repair controls.**
   `C-PARSE-FRACTIONAL-ANCHORS` — the four real anchors parse to
   `1792249835.398909 / 1792249835.398909 / 1792197932.184000 / 1792197964.288000` **and** the
   parent's strict parser demonstrably fails on them.
   `C-PARSE-REFUSES-GARBAGE` — `""`, `"   "`, `None`, a non-string, a bare date, a timezone-less
   datetime, year 1899, a leading-garbage string and an out-of-range instant
   (`2026-13-45T99:99:99Z`) all raise `ValueError` naming the anchor field; **no input may return
   `None`**.
   `C-CLOCK-EPOCH-ONLY` — epoch-only arithmetic gives `7.756 h`; the prohibited monotonic-minus-epoch
   construction gives about `-497832 h` and is unreachable in the frozen code path.
   `C-ANCHOR-CONSISTENCY` — the four-artifact check of §4, including Δ = 0.000000000 s between the
   two independent start anchors.
   `C-POPULATION-MANIFEST` — admitted = 1107, unique URLs = 1107, deep 686 / shallow 421, host table
   as in §4, source file sha256 matches the frozen artifact hash, 12 excluded rows enumerated.
   `C-NESTING-LEMMA-CANARY` — on synthetic monotone change schedules the derived UB is non-decreasing
   in the window; a non-monotone derivation fails.
   `C-GROWTH-EXACT-P` — `a=5,b=0 → 0.03125`; `a=4,b=0 → 0.0625`; `a=6,b=1 → 0.0625`;
   `a=b=1 → 1.0`; `a=b=0 → 1.0, GROWTH_UNDERPOWERED`.
   `C-CLASS-POWER-GATE` — a class with `n < 59` yields `CLASS_UNDERPOWERED` and no certified level;
   `n = 713` at `k=0` yields level 0.01.
3. **Deterministic zero-GET reproduction (null family 3).** `C-NULL-FAMILY-DETERMINISTIC-REPRODUCTION`
   / control id `C-LEGACY-REPRODUCTION`: recompute the grandparent-overlap byte comparison over the
   frozen × frozen rows and require `n = 292`, `k = 0`, `UB95 = 0.010206909410248878` at full float
   equality with the value the parent packet itself recorded in
   `run/derived/retro_secondary.json#retro_metrics.M-RETRO-UB95-ALL`, and
   `M-LEGACY14H-W-H ∈ [13.0, 16.0] h`. **This value was computed at DESIGN and is disclosed here
   (§15, probe D7).** It is a null for the entire derivation path — pair construction, byte
   comparison, and bound arithmetic — computed by a *different* process in a *different* packet, and
   it costs zero GETs.
4. **Live families, unchanged from the accepted parent.** `C-LIVE-POS-SENSITIVITY` (3 volatile URLs
   across the 360 s in-launch separation; ≥1 must fire, ≥2 must be 200);
   `C-LIVE-NULL-STABILITY` (2 static anchors, 0 changes);
   `C-SELFPAIR-DETERMINISM` (10 in-frame pages twice, gap ≤5 s, 0 changes — the strongest family,
   because it runs inside the measured frame on multi-megabyte pages).
5. **Frame and ledger.** `C-FRAME-DEPTH-PRESENT` (`n ≥ 60` per stratum, ≥2 hosts with ≥25 paired
   pages in both strata), `C-CODE-IDENTITY` (parent module hash + own self-hash recorded),
   `C-LEDGER-RECONCILIATION`.

**Declared scope limit on the controls.** No live positive control can span the ~8 h primary window,
because no live fetch exists at the observation-0 epoch. The three null families establish detector
noise and derivation exactness, not origin freshness. That residual risk is carried as `V13` with
four reported diagnostics and is the reason `CC-A` speaks about what two credential-free GETs
returned rather than about origin content.

---

## 14. Validity checks (full text in `spec.json#measurement_validity`)

`V1` code/instrument identity · `V2` offline control suite · `V3` anchor parser closedness ·
`V4` single-clock discipline · `V5` anchor consistency · `V6` frozen population identity ·
`V7` window quantisation · `V8` window admission and sub-band · `V9` short-window eligibility floor ·
`V10` censoring and page-gone · `V11` detector sensitivity and specificity ·
`V12` host/stratum confounding · `V13` fetch freshness at the long window *(disclosed residual)* ·
`V14` representation loss · `V15` envelope and ledger · `V16` preregistration timing ·
`V17` nested-window lemma.

Failure dispositions are frozen per check: `MEASUREMENT_INVALID` for instrument/input failures
(`V1–V5`, `V11`, `V16`), `REFUSE_LONG_*` for measurement-valid refusals (`V8`, `V9`, `V10`, `V12`),
`NO_DATA_LEDGER_FAIL` for `V15`, and disclosed ceiling limits for `V7`, `V13`, `V14`, `V17`.

---

## 15. DESIGN probe log — cheap satisfiability probes, with exact outputs

Executed 2026-10-17T22:53Z..23:05Z. **21 live URLs fetched AT MOST ONCE each. No two-observation
pair of any kind exists for the frozen question.** One outcome-bearing computation over
already-accepted frozen artifacts was performed and is disclosed with its exact value (D7); it set
no threshold (§15.1 last paragraph).

**D1 — parser and anchor consistency (OFFLINE).**
Parent strict parser: `None` on `2026-10-17T15:10:35.398909+00:00`; `ValueError` on
`2026-10-17T00:45:32.184Z` and `2026-10-17T00:46:04.288Z`.
Repaired parser: `1792249835.398909` (obs0 start), `1792249835.398909` (provenance anchor,
Δ = 0.000000000 s), `1792197932.184000` (legacy start), `1792197964.288000` (legacy end, trailing
suffix stripped). `frozen_at 1792248383.389566 ≤ 1792249835.398909` (1452.0 s before);
`died_utc 1792250298.715476 ≥ 1792249871.988909`. Observation-0 window width 36.59 s.

**D2 — clock discipline (OFFLINE).** `W_primary = 7.756 h` (sub-band HOURS);
`W_legacy = 22.175 h` (HOURS; enters DAY after `2026-10-18T00:46:04.288Z`); prohibited
monotonic-minus-epoch ⇒ about `-497832 h`; quantisation = 0.131 % of `W_primary`.
Deadlines: primary 30 d cap `2026-11-16T15:11:11.988909+00:00`; legacy 30 d cap
`2026-11-16T00:46:04.288000+00:00`.

**D3 — bound arithmetic (OFFLINE, hash-pinned parent `cp_ub95`/`cert_level`).**
`UB95(0,686)=0.004357`, `UB95(0,421)=0.007090` (parent's accepted values reproduced).
Min `n` for a certified level: **299 / 149 / 59** at 0.01 / 0.02 / 0.05.
First `k` with `UB95 > 0.05`: **25/686** deep (0.0364), **14/421** shallow (0.0333).
First `k` dropping deep below 0.01: `k=3`; below 0.05: `k=8`.
Censoring is **not** the binding gate: even at 35 % censoring the deep stratum still certifies 0.01
(`n=446`, UB 0.00669) — so a censoring refusal requires genuine mass deletion, which is why the
ceiling on censoring, not censoring alone, is the real risk.

**D4 — growth-contrast power (OFFLINE).** `a=5,b=0 → 0.03125`; `4 → 0.0625`; `6,1 → 0.0625`;
`0,0 → underpowered`. `GROWTH_MDC_COUNT = 5` frozen.

**D5 — live liveness (LIVE, 9 single GETs, 2026-10-17T22:56Z).** Seeds 4/4 HTTP 200
(22496 / 31975 / 24433 / 22046 B). Positive controls 3/3 HTTP 200. Null anchors 2/2 HTTP 200.
**Reachability only — never volatility; creates no pair.**

**D6 — population liveness (LIVE, 12 single GETs, ~23:00Z).** Deterministic sample, one page per
host × stratum × class bucket over the first 12 of 14 buckets: **12/12 HTTP 200**, covering all six
stratum × class combinations including deep `VERSION_PINNED` (population n=22) and shallow
`VERSION_PINNED` (n=1). The frozen population is still fetchable ~8 h after observation 0, so the
censoring gate has real headroom without being vacuous.

**D7 — DISCLOSED existing-data point (OFFLINE, frozen × frozen, 0 GETs).** Grandparent overlap vs
frozen observation-0: `n=292`, `byte_changed=0`, `UB95=0.010206909410248878`, `cert_level=0.02`, true
window ≈14.4 h, `transport_changed=13`. Bit-identical to the value the parent packet recorded at
`run/derived/retro_secondary.json#retro_metrics.M-RETRO-UB95-ALL`. Adopted as
`C-NULL-FAMILY-DETERMINISTIC-REPRODUCTION` and as rung P0.
**No threshold was derived from it:** `CERT_GRID`, `ALPHA`, `MIN_N_PER_STRATUM`,
`MIN_HOST_STRATUM_N`, `MIN_HOSTS_BOTH`, `CENSOR_MAX`, `HOST_CONC_WARN`,
`VERSION_PINNED_FRAC_WARN`, `DT_MIN_S`, `DT_MAX_S`, `SHALLOW_MAX_HOP`, `SELFPAIR_N`, the band edges
and the whole control URL set are inherited verbatim from `EXP-FRONTIER-39039638199`.

**D8 — instrument reproduction (OFFLINE).** Hash-pinned parent module self-hash reproduces
`5d2509f691193c610a9797e4c473ee9425c010c1a4bd35f65b43e3aca672c573`; 35/35 offline controls pass;
replaying its own `summarize()`/`decide()` over its own frozen raw rows reproduces every
load-bearing accepted metric exactly — `n 686/421`, text changes `0/0`, UB95 `0.004357`/`0.007090`,
hosts spanning both strata `4`, live positives `3`, nulls `0`, self-pairs `0`, label
`CERTIFY_BOTH_AT_0P01`. This is a **reproduction of already-accepted numbers** and yields no new
information about the long window; it establishes only that the import-and-reuse path is exact
before a single live GET is spent.

**D9 — population structure (OFFLINE, frozen census).** See the table in §4.

**D10 — decision-branch reachability (OFFLINE, frozen reference source).** All 22 canaries produce
exactly their expected labels; 20 distinct; 4 defects in the author's own rule were found and fixed
before freeze (§11.2).

**Probe consequence.** Both mandated repairs are demonstrated working and their failure modes
demonstrated unreachable; the frozen population is intact, host-diverse, non-ceiling and still
fetchable; every decision branch is reachable at realistic frame sizes with exact arithmetic; the
instrument reuse path reproduces the accepted parent numbers bit-for-bit; and the total live budget
is ~2234 GETs at a projected 490 s wall. **No unresolved prerequisite remains for this packet to
freeze.**

---

## 16. Cost and politeness

| item | value |
|---|---|
| live GETs | ≈2234 of 3200 (1107 OBS1 + 1107 OBS2 + 20 self-pair + 10 probes) + 8 offline fixture GETs |
| bytes | ≈205 MB (two full-frame sweeps of ≈100.9 MB, matching the parent's measured observation-0 volume) |
| module wall | ≈490 s projected vs `MODULE_WALL_BUDGET_S=900` and `SPIDER_MODEL_MAX_RUNTIME_SECONDS=1200` |
| compute | stdlib-only Python 3.12; no browser, no JS engine, no LLM, no credential, no `pip install`; financial cost zero |
| design cost already spent | 21 single-observation liveness GETs + offline probes |
| politeness | each page fetched at most twice per launch; per-host concurrency 2; ≥0.10 s spacing; 30 s inter-sweep gap; frozen rate-limit circuit breaker at 10 rate-limit responses per host; ≈554 requests per host across both sweeps |

---

## 17. Claim ceiling (frozen, `spec.json#claim_ceiling_rules`)

- **CC-A.** At most a per-page structural-text invalidation upper bound, per hop-depth stratum, for
  credential-free GET-only server-rendered documentation pages on four documentation hosts, from one
  egress vantage, at the measured window `W`, on a frozen population of 1107 URLs. Because no live
  control spans `W`, the bound is a statement about what two credential-free GETs at two instants
  returned — **not** a claim about origin content.
- **CC-B.** A certified level is a statement about the observed pairs at the measured window only.
  `L1-WINDOW-NESTING` carries it to every **smaller** lag on the same page set and to nothing
  larger. `M-TTL-LICENSED-LAG-H` equals the measured `W` and is the maximum lag any downstream
  statement may use.
- **CC-C.** `C-WEB-DYNAMICS` stays `HYPOTHESIS` regardless of outcome. No `EXPERIMENTAL`,
  `VALIDATED`, `PRODUCT_CORE` or `SHIPPED` status is available from this packet, and no
  self-promotion is permitted.
- **CC-D.** `NO_DATA_*` and `REFUSE_LONG_*` are packet/measurement dispositions; they do not move
  the effective epistemic status of `C-WEB-DYNAMICS`.
- **CC-E.** The secondary ladder, growth contrast, depth contrast and class decomposition are cited
  only with their own window, population, channel and power limit; the 292-page ladder is byte-only,
  shallow-biased and nested inside the primary population, so it can never be stronger than the
  primary bound; a class below 299 / 149 / 59 certifies nothing at 0.01 / 0.02 / 0.05.
- **CC-F.** The frozen frame is a frozen population, not a sample of the Web; hop depth remains
  partly confounded with host and URL class even though all four hosts span both strata.
- **CC-G.** This packet measures a page-level property. It does not measure SPIDER's inheritance
  economics, does not price a store-versus-cold comparison, does not compare a TTL ladder against
  any alternative guard architecture, and must not be cited as evidence for or against any of those.

---

## 18. Freeze mechanism, its declared limitation, and what AUDIT must re-run

**What is byte-frozen.** `request.json`, `spec.json`, this `prereg.md` and (v2) `design_review.json`
are hashed by `scripts/freeze_experiment.py`. Seventeen external interpretation dependencies are
hashed into `freeze.json.artifact_hashes` from `spec.freeze_artifacts`: the parent's `census.jsonl`
(the frozen population), `PROGRESS.json` (the epoch anchor), `obs1.jsonl` and `control_probes.jsonl`
(the inherited comparator and control set), `execute_module.py` (**the imported instrument**),
`provenance.json`, `freeze.json`, `result.json`, `audit.json`, `handoff.json`; the grandparent
`census.jsonl`, `provenance.json`, `execute_module.py`, `freeze.json`; and
`codex/claim_state.json`, `research/claims/registry.json`, `research/lanes/registry.json`.

**Declared limitation.** This packet's own executable module is not a repository file at freeze
time, because DESIGN was restricted to `spec.json` and `prereg.md` and therefore could not author
and byte-hash it (the parent packet could, and did — its `V1` code-identity check compares a
`DERIVED_SHA256` that no longer exists here). The freeze is therefore **behavioural** for that
module: frozen constants (§5), frozen rule text and reference source with its sha256 (§12), and a
22-entry canary table with expected labels (§12.1), all inside the hash-pinned `prereg.md`. This is
stated up front rather than discovered at audit.

**What AUDIT must re-run.** All 22 `C-DECIDE-LONG-*` canaries against the module's **own** `decide()`
function, requiring the exact labels of §12.1; `C-PARSE-REFUSES-GARBAGE` (proving no input returns
`None`); `C-ANCHOR-CONSISTENCY` and the four epoch anchors recomputed from the frozen artifacts;
`C-LEGACY-REPRODUCTION` at full float equality; the 35 inherited offline controls; recomputation of
every load-bearing metric from `run/raw/*.jsonl` alone; and an independent recomputation of the
window from the recorded epoch stamps. Any deviation from §12.1 is a required fix, because it means
the executed rule is not the frozen rule.

---

## 19. Legacy disposition

`LEGACY: DISTINCT_EXTENSION` of the pre-2.0 frontier volatility/freshness thread, plus **REPLICATION**
of its instrument lesson and a **REPAIR** of the one long-window channel it structurally could not
execute; **NO_MATCH** on the pre-2.0 next-state work named in the Director mandate.

Screening method: topic-keyword screening of `codex/legacy_artifact_index.json` (1401 artifacts,
blob sha `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`) for
`fresh|stale|ttl|window|census|volatil|timescale|hazard|stationar|invalidation|revalidat|stability|drift`
over paths, roles and verdict tokens returned 89 candidates; five load-bearing artifacts were then
read at their exact indexed line ranges from the mounted `.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md`.
The 22 MB source was not loaded wholesale, and the absence of a keyword hit was never treated as
proof of absence.

| artifact | sha | what it established | relation here |
|---|---|---|---|
| `frontier/web-physics-volatility-freshness/reports/CENSUS_REPORT_V3.md` (4.1052) | `81aba1e898d96fe3c49ae9cd0f4ef00dfdad46a4` | Largest same-target revisit in any committed corpus = 0.021812 d (31.4 min); 26 separated pairs vs 64 required; "Days-to-weeks staleness band strata: OUT OF SCOPE on committed bytes"; openlibrary 7/12 double-reset drift at seconds scale, CP CI [0.276670, 0.848348]; 62/62 placebo zero-drift | **DISTINCT_EXTENSION.** Not re-run. The seconds-scale drift figure is carried as a labelled PRIOR, never as evidence. No day-scale claim unless the measured sub-band says so — which is why the sub-band is inside the label |
| `frontier/web-physics-volatility-freshness/reports/CYCLE_32968938133_REPORT.md` (4.1053) | `869b3d6d9484cc675795797ffccf6e6b3cfee74a` | "provably undecidable without new time-axis data"; "Exactly one discriminating path exists: an authorized longitudinal collection (sentinel pilot → panel)" | **THIS PACKET IS THAT AUTHORISED LONGITUDINAL COLLECTION** at the smallest possible scale: bounded, over an already-frozen population, with a frozen rule, an exact bound and a full control suite. It does not claim to close the charter's broader sentinel programme |
| `results/intel/reproductions/cycle6/ttl_window2_protocol.json` (4.243) and cycle8 (4.445, 4.446) | `383df5cee7e2241d73a6174361d9f635381816c9` / `7ce37c3ea7a9b1531d71797cb7b4f777bf2e1f56` / `fa21a4e0d157a24ba60058975743f832c5025cb5` | Window 2 `NOT_EXECUTED_THIS_RUN`, `required_gap_hours: 24`, reason "single-session constraint disclosed at freeze time; >=24h calendar gap required", explicit `window2_eligibility_ts_ms`, positive-differential STALE_TTL attribution, window-regress cap of 3 | **DISTINCT_EXTENSION; the clearest structural precedent attacked.** Two differences are load-bearing: the substrate (legacy measured replay-artifact staleness via discovery-vs-replay differentials on route records and replica-store fingerprints over application hosts; this packet measures per-page structural-text invalidation of a documentation frame — the word "window" coincides, the estimand does not) and the constraint (the legacy protocol could not leave a session; this packet's separation exceeds the harness envelope by construction). The legacy ≥24 h floor is the DAY sub-band boundary, recorded so the comparison is exact rather than rhetorical |
| `results/intel/reproductions/cycle8/ttl_window1.json` (4.443) | `43d21a4a384bc5a242c6bb6f4725e4093982f0fb` | Frozen rule "CHANGED iff ETag differs; if ETag absent on either side, CHANGED iff head-hash differs", plus: a resource can vary bytewise under one unchanged ETag, and a per-request trace identifier makes a resource volatile without content change | **REPLICATION + REPAIR.** Adopted as `B-TRANSPORT-CHANNEL`: transport is a covariate and never defines an event. This packet additionally reports the reverse error (byte-changed-but-text-unchanged, 7 pages in the parent's own accepted rows). DESIGN verified all 359 of the parent's transport moves came from one host's `Last-Modified`, which is why a transport gate was explicitly rejected here |
| `contracts/CHANGE_EVENT_TAXONOMY_V0.md` / `FRESHNESS_SIGNAL_CONTRACT_V0.md` (4.1247, 4.1248) | `f41395817d98f153f098df42cf2cd48f0052eceb` / `0a53685fd4188dfc17beefca9950c1e6921d4a39` | CE-1/2/3/5 admissible, CE-4 excluded by design, CE-6 not an event, CE-5 (outage) must not be misread as staleness, seconds-scale extrapolation declared INVALID | **ADOPTED, not re-derived.** Text change → CE-1/2/3; attribute/script churn → CE-6, counted separately; 404/410 and 5xx → CE-5/death channels, never folded into the change rate; no session/auth class exists. The extrapolation ban is why `CC-B` extends certifications only downward in window |

**Non-duplication of Research 2.0 precedents.** `EXP-FRONTIER-39039638199` measured the same estimand
at the 7-minute window; this is a new measurement at a window ≥60× longer and does not re-adjudicate
its label. `EXP-FRONTIER-37950626378` (hop-scaling cost law) is a different estimand (cost vs N).
`EXP-FRONTIER-38184956362` closed the site-native discovery axis and is inherited, not re-run.
`EXP-FRONTIER-38940047535` and `-38188815194` are the twice-`MEASUREMENT_INVALID`
persistence-economics thread, parked by mandate, used here **only** as a frozen epoch anchor and a
frozen byte census.

---

## 20. What EXECUTE must emit

```
research/experiments/EXP-FRONTIER-39053910903/run/
  execute_module.py                 stdlib-only; imports the hash-pinned parent module
  raw/PROGRESS.json                 launch_id, stage, epoch brackets, GET ledger, module self-hash
  raw/obs1_long.jsonl               1107 rows (obs=1), epoch-stamped, atomic
  raw/obs2_short.jsonl              1107 rows (obs=2), epoch-stamped, atomic
  raw/controls.jsonl                every offline canary of §13
  raw/selfpair.jsonl                10 rows
  raw/control_probes.jsonl          10 rows (3 pos + 2 null × 2 observations)
  raw/obs0_manifest.json            the 1107-URL population with hop/host/class + source hashes
  derived/code_identity.json        own stripped self-hash + parent module hash verification
  derived/metrics.json              every M-* id of spec.metric_ids
  derived/decision.json             decide() output: label, status, outcome, certified levels, tags, band
  derived/legacy_ladder.json        the three secondary byte rungs + the reproduction canary result
  derived/class_decomposition.json  per-class n/k/UB95/level/power verdict
```

plus `result.json` (schema per `research/EXPERIMENT_PACKET.md` §4, with `schema_version`,
`experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`,
`validity_notes`, `unresolved`), `report.md` and `provenance.json` (§5).

**EXECUTE may not** modify `request.json`, `spec.json`, `prereg.md`, `design_review.json` or any file
listed in `freeze.json.artifact_hashes`; may not re-fetch anything outside the frozen population and
the frozen control URLs; may not change any threshold; and may not fall back on the parent's derived
files — every derived number must be recomputed from this packet's own raw rows.

**Smallest unblocking actions, named in advance.** If the module cannot import the parent module
(hash mismatch), stop and report: the packet's instrument identity is broken and no re-implementation
may be substituted. If the population manifest fails, stop and report: the frozen population is not
the admitted set. If the launch misses `2026-11-16T15:11:11.988909Z`, the packet refuses by its own
frozen gate and its persisted `raw/obs1_long.jsonl` becomes the anchor for a successor rung.