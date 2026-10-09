# EXECUTE report — EXP-FRONTIER-37950626378

- **Lane:** `frontier`
- **Target claim:** `C-RESIDUAL-NOVELTY`
- **Director cycle:** `37949204501` (action `CONTINUE`, `parent_handoff_disposition = USE`)
- **Parent packet:** `EXP-FRONTIER-37385647440` (MEASUREMENT_INVALID — all admitted items at hop <= 1)
- **Status:** `COMPLETE`
- **Outcome (frozen decision rule):** `SUPPORTS` — pooled verdict **GROWING** (H1)
- **Frozen inputs re-hashed at EXECUTE:** `request.json`, `spec.json`, `prereg.md` all **MATCH** freeze.json
- **Execution:** GitHub run `37975522921` (attempt 1), branch `lab2/frontier`, HEAD `89c5dea1358f74a8197e69cae94c104ab92fe654`
- **No commit / no push.** No frozen file was modified. No product code was modified.

> **Scope of any claim from this experiment (read before the numbers):** the frozen ratio is
> measured, and the frozen decision rule returns `GROWING`, but the `RED` arm is a level-order BFS
> prefix that is *forced* to be >= the persisted-path arm by the frozen baseline-ordering proof.
> The GROWING ratio is therefore substantially a property of the frozen estimator's branching
> factor, not independent evidence about Web acquisition economics. The producer records this in
> `validity_notes[VN-V9]` and does **not** self-promote the claim. Details in *Interpretation*.

---

## 1. RAW EVIDENCE (gathered, not interpreted)

Persisted verbatim under `research/experiments/EXP-FRONTIER-37950626378/`:

| Artifact | Records | sha256 (first 16) |
|---|---|---|
| `raw/http.jsonl` | 4257 HTTP response records (one per GET: url, final_url, status, body_bytes, body_sha256, elapsed_s, hop, session, site, truncated, error) | `4cf6fa27929d1134` |
| `raw/observations.jsonl` | 1559 admitted-item observation rows (all per-item fields for both sessions) | `33e7baf21767503e` |
| `raw/controls.jsonl` | 1 row with the 4 control verdicts | `b579f8132eacfa53` |
| `derived/metrics.json` | computed pooled/per-site/per-item metrics | `a02e2fe473b227e1` |
| `derived/analysis.json` | band medians, host composition, session agreement | `75a74280b9a16d00` |
| `derived/implementation_choices.json` | IC-01..IC-07 ambiguity resolutions | `00032839197d712c` |
| `derived/site_<site>_s{0,1}.json` | 12 per-session site reports | (see `provenance.json`) |
| `research/frontier/run_execute_37950626378.py` | shipped executor | `2b9d144ab0d13e7b` |

Substrate: credential-free GET-only Python stdlib `urllib`; UA
`SPIDER-research-frontier-37950626378/1.0`; timeout 12 s; max body 600000 B; TLS verified; redirects
followed; no cookies/credentials/browser/Docker/model key/write verb. Wall clock **572.43 s**.

## 2. CONTROLS (Step 0) — all four PASS

Live-reproduced under the frozen policy; all four equal the pre-freeze certificate.

| Control id | Kind | Expected | Observed | Pass |
|---|---|---|---|---|
| `POS_KNOWN_HOP_CONTROL` | positive | found=true, hop=1, status=200 | found=true, hop=1, requests=3, cum_bytes=653222, status=200 | ✅ |
| `NEG_UNREACHABLE_CONTROL` | null/negative | found=false | found=false | ✅ |
| `NARROW_CHAIN_CALIBRATION` | FLAT calibration | R<=3.0 | requests {hop1:2, hop2:3, hop3:4}, **R=2.0** | ✅ |
| `BROAD_FANOUT_CALIBRATION` | GROWING calibration | R>3.0 | requests {hop1:2, hop3:932}, **R=466.0** | ✅ |

`M = 3.0` remains strictly bracketed by two live-measured ratios (2.0 and 466.0), so the decision
boundary is demonstrated satisfiable in both directions (evidence: `raw/controls.jsonl`,
`raw/http.jsonl`).

## 3. OBSERVATIONS (facts about the run)

- **OBS-01** All four frozen controls reproduced live and PASS with the exact pre-freeze values.
- **OBS-02** All 12 structural sessions (6 roots x 2) completed with a 200 seed and `n_get=250`
  (budget exhausted); `sessions_ok=true` for all six sites. Cumulative fetched bytes were identical
  across the two sessions for 5 of 6 sites; `forums.gentoo.org` session B was exactly +1 byte
  (6732475 vs 6732474) and carried all 16 item-level byte differences.
- **OBS-03** `ADMISSION_GATE_V1` **PASS**: site-row counts admitted_DEEP=26, admitted_NEAR=419,
  admitted_MID=1114, distinct_seed_hosts=4; after `item_id` dedup DEEP=25, NEAR=408, MID=1099.
- **OBS-04** Every admitted DEEP item is on `doc.rust-lang.org` (mdBook): 26 site rows
  (rust_book 12, rust_cargo 10, rust_nomicon 4) → 25 deduped (rust_book 12, rust_cargo 9,
  rust_nomicon 4). No DEEP item on www.gnu.org, quotes.toscrape.com or forums.gentoo.org within
  B=250/D=6.
- **OBS-05** Pooled (deduped) RED medians: requests DEEP=158 vs NEAR=30; bytes DEEP=9704744 vs
  NEAR=1327357.
- **OBS-06** Per-site session-A ratios: rust_book 10.625/7.622; rust_cargo 28.75/13.572;
  rust_nomicon 44.5/40.962 (all GROWING). gnu, quotes, gentoo are UNDEFINED (0 DEEP items).
- **OBS-07** Persisted-path cost is near-linear in hop: median `RACQ_PATH.requests` DEEP=4 vs
  NEAR=2 (ratio **2.0**); median `RACQ_PATH.bytes` DEEP=711368 vs NEAR=63384 (ratio 11.22);
  `RACQ_URL.requests=1` for every item.
- **OBS-08** Median eligible-item break-even reuse counts: DEEP requests=0.02597 (25/25 eligible),
  bytes=0.09918; NEAR requests=0.06452 (382/408), bytes=0.04755; MID requests=0.02222
  (1099/1099), bytes=0.01791. Every DEEP item is break-even eligible.
- **OBS-09** `path_len == hop+1` for 1532/1532 deduped admitted items.
- **OBS-10** Two-session agreement: `RED.requests` identical for all 1559 admitted rows (no site
  flagged unstable by VN-V4); `RED.bytes` differs in 16/1559 rows, all on forums.gentoo.org.
- **OBS-11** Substrate: 4257 GETs (3000 real-root = 6x2x250, 250 pos_control, 1000 broad_fanout,
  7 narrow_chain). Raw records carry no method field; executor implements only urllib GET.
- **OBS-12** `tiktoken` not importable (ModuleNotFoundError) and absent from `pyproject.toml`; all
  token fields are `null`.
- **OBS-13** Items kept per site after two-session agreement: rust_book 36, rust_cargo 160,
  rust_nomicon 41, gnu 1300, quotes 6, gentoo 16; `items_shared == items_kept` for every site.

## 4. DERIVED MEASUREMENTS (computed from the observations)

Pooled, deduped (`n_duplicate_rows_removed=27`, `n_items_deduped=1532`):

```
R_req   = median(RED.requests|DEEP) / median(RED.requests|NEAR) = 158 / 30     = 5.2667
R_bytes = median(RED.bytes   |DEEP) / median(RED.bytes   |NEAR) = 9704744 / 1327357 = 7.3113
M = 3.0
```

Frozen decision rule: `GROWING` iff `R_req > M` and `R_bytes > M`. Both exceed 3.0 →
**pooled verdict GROWING**; `falsifier_triggered = true`.

Band medians and re-acquisition arms:

| band | n | median RED req | median RED bytes | median RACQ_PATH req | median RACQ_PATH bytes | median saving req |
|---|---|---|---|---|---|---|
| NEAR | 408 | 30 | 1,327,357 | 2 | 63,384 | 28 |
| MID  | 1099 | 138 | 4,462,155 | 3 | 78,106 | 135 |
| DEEP | 25 | 158 | 9,704,744 | 4 | 711,368 | 154 |

Break-even reuse counts (median over eligible): see OBS-08. `controls_metric`: all 8 control/baseline
arms pass. Admission gate: `pass=true` at 26 DEEP / 419 NEAR / 4 hosts. Full machine-readable values
in `derived/metrics.json` and `derived/analysis.json`.

## 5. INTERPRETATION (producer-bounded, not a promotion)

**What the frozen rule outputs.** Under the frozen estimator and comparator, the unconditional
re-derivation cost of admitted DEEP state items exceeds that of admitted NEAR items by 5.27x in GETs
and 7.31x in body bytes. The frozen rule therefore scores **SUPPORTS (H1)** and the falsifier is
triggered. The pooled DEEP set is entirely `doc.rust-lang.org` mdBook; the per-site mdBook ratios are
all GROWING, so the effect holds *within* mdBook.

**Why this is weaker than it looks (VN-V9).** `RED` is defined as the item-blind FIFO BFS prefix.
The frozen baseline-ordering proof already establishes `RED.requests >= RACQ_PATH.requests`, and on
any frontier with branching > 1 the BFS fetches every shallower page before a depth-h page. A
DEEP/NEAR ratio above M=3 is thus largely forced by level-order enumeration; it is not independent
evidence that *the Web* charges more for deeper instances. The FLAT branch was only producible on
the detour-free linear chain (`NARROW_CHAIN_CALIBRATION`, R=2.0), consistent with this reading.

**The more direct re-acquisition reading.** The persisted-path arm is near-linear in depth
(median 4 vs 2 GETs, ratio 2.0), and DEEP re-derivation saves a median 154 GETs. The break-even
reuse counts are all much less than 1, i.e. a persisted path pays for itself after a single reuse —
but this is exactly the ordering proof, so it does not discriminate O(1) from depth-growing.

**Bounded conclusion.** Established by this experiment: under the frozen item-blind BFS estimator
on a credential-free GET-only stdlib substrate, the billed re-derivation cost ratio between depth>=3
mdBook state items and hop<=1 items is R_req=5.27, R_bytes=7.31 at M=3.0, with all controls passing
and a passed admission gate. **Not** established: that this ratio reflects Web structure rather
than the estimator; that it generalizes to non-mdBook hosts (0 DEEP items admitted elsewhere); or
anything about real economics (no token/latency/dollar channel). No mechanism, cache or product
change is promoted; the decision moves only to a possible bounded successor under a new mandate.

## 6. VALIDITY THREATS (full list in `result.json.validity_notes`)

- **VN-V1** tokenizer unavailable; only GET counts and body bytes measured (token fields null).
- **VN-V2** static `<a href>` only; JS-generated navigation is not an edge.
- **VN-V3** same-host navigation only.
- **VN-V4** K=2 sessions/site; requests agreed 1559/1559, bytes drifted only on gentoo (16 rows).
- **V5** all six seed hosts reachable (`network=AVAILABLE`).
- **VN-V6** stdlib HTML-parser heuristic misses JS-rendered controls.
- **VN-V7** hop==2 (MID) descriptive only, excluded from the primary contrast.
- **VN-V8** DEEP band is single-host/single-engine (mdBook); cross-host generalization not claimed.
- **VN-V9** construct-validity: the ratio is substantially estimator-imposed (see §5).
- **VN-V10** arms are strictly paired on the same session/items; no duplicate GET per arm.
- **VN-V11** calibration fixtures used page budget 1000 (IC-03); real roots used B=250.
- **VN-V12** pooled ratio dedupes shared doc.rust-lang.org items by `item_id` (IC-07).
- **VN-V13** gnu/quotes/gentoo UNDEFINED is a budget/depth fact, not a FLAT measurement.
- **VN-V14** no latency/dollar cost imputed.

## 7. CONSEQUENCES (both directions, per prereg)

- **Observed (GROWING):** a measurable amortization surface is reported for `C-RESIDUAL-NOVELTY`,
  `C-FRESHNESS` staleness economics and the `C-WEB-DYNAMICS` timescales axis, **bounded to the frozen
  estimator** and to mdBook. A bounded successor may evaluate a path/procedure cache under a separate
  verdict; this experiment promotes no mechanism.
- **Counterfactual (FLAT, not observed):** acquisition would be O(1) in site structure and path
  persistence deprioritized. Because the GROWING result is estimator-bound (VN-V9), a successor that
  removes the level-order forcing remains the decisive test between these readings.

## 8. UNRESOLVED

`UR-1` cross-host DEEP generalization (no non-mdBook DEEP admitted at B=250); `UR-2` separating Web
structure from estimator branching (needs a non-level-order estimator); `UR-3` real economics
(latency/dollars/tokens); `UR-4` JS-rendered control detection; `UR-5` the 16 gentoo byte-drift rows.
See `result.json.unresolved`.

## 9. PROVENANCE / INTEGRITY NOTES

- Frozen inputs re-hashed at EXECUTE: `request.json`, `spec.json`, `prereg.md` MATCH freeze.json;
  nothing frozen was edited.
- `provenance.json` records origin run `37950626378`, execute run `37975522921`, base_sha
  `455f25d...`, HEAD `89c5dea...`, the exact command, environment, safety flags and all artifact
  hashes.
- **Superseded receipts (not scientific evidence):** `failure.json` (run `37962922070`,
  EXECUTION_FAILURE), `model_execute.json` (run `37975522921`, status `retry`, attempt 4) and
  `execution_checkpoint.json` (origin run `37950626378`) are workflow-runner receipts left in
  place. They were not edited. This EXECUTE completes the frozen design; `result.json` /
  `report.md` / `provenance.json` are the authoritative stage output.
- `derived/implementation_choices.json` (IC-01..IC-07) records every ambiguity resolution
  (blocking/non-blocking) applied during EXECUTE.
