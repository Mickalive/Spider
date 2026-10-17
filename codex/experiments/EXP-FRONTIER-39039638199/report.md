# EXP-FRONTIER-39039638199 — EXECUTE report

**Lane:** frontier · **Status:** `COMPLETE` · **Outcome:** `SUPPORTS`
**Frozen decision label:** `CERTIFY_BOTH_AT_0P01` (no narrowing tags)
**Claim:** `C-WEB-DYNAMICS` (frontier-owned; stays `HYPOTHESIS` — see *Claim ceiling*)

Question: on the live documentation Web, is session-scale invalidation hazard
concentrated in the deep stratum (`hop>=3`) rather than the shallow stratum
(`hop<=2`), and can a two-observation census diff on a **fetch-complete** frame
certify, or explicitly refuse to certify, named zero-GET staleness tolerances
inside one session?

Answer, in one line: **both strata certify a zero-GET tolerance of 1 % at the
measured ~6.8-minute separation, with zero events in 1107 paired pages and a
live positive sensitivity control that fired on all three frozen volatile URLs.**

---

## 1. What was actually executed

The frozen EXECUTE module (`prereg.md#10`, stripped sha256
`5d2509f691193c610a9797e4c473ee9425c010c1a4bd35f65b43e3aca672c573`) was
reconstructed byte-exactly from the hashed preregistration block and run
unmodified:

```
python3 research/experiments/EXP-FRONTIER-39039638199/run/execute_module.py \
        --stage all --out research/experiments/EXP-FRONTIER-39039638199/run
```

It completed **every primary stage**: 35/35 offline controls → observation-0
fetch-complete census → 360 s separation → observation-1 re-fetch of the whole
admitted set → 10 in-frame self-pairs → 10 live control probes. It then raised
`ValueError` in `parent_window()` while entering the **secondary** retro channel
(`prereg.md#11` step 6), *after* all primary RAW evidence had been written and
*before* it could write `derived/metrics.json`.

`derived/metrics.json` / `derived/decision.json` were therefore produced by
**importing the unmodified frozen module and replaying its own pure
`summarize()` / `decide()` over its own RAW rows** — no frozen file was edited,
and every hash in `freeze.json` re-verifies OK. The four values the frozen
process could not emit (`M-WALL-S`, `M-PARTIAL`, `M-TIME-TRUNCATED-HOSTS`, the
observation-1 GET ledger) are reconstructed from the module's own checkpoints
and are itemised in `run/derived/metrics.json#reconstruction_notes`. This is a
disclosed reconstruction, not a silent substitution.

## 2. RAW EVIDENCE (observations, not measurements)

| # | observation | evidence |
|---|---|---|
| O1 | obs-0 census: 1119 rows written, 1107 HTTP 200, 6×404, 6 transport errors, 100.9 MB, 36.59 s, 1123 GETs | `run/raw/PROGRESS.json`, `run/raw/census.jsonl` |
| O2 | all 1107 admitted pages re-fetched at obs-1: **1107/1107 HTTP 200**, zero censoring | `run/raw/obs1.jsonl` |
| O3 | measured separations: min 377.06 s, median 407.97 s, p90 430.52 s, max 439.83 s; 0 pairs below the frozen 300 s floor | `run/derived/metrics.json` |
| O4 | **3 of 3** frozen positive-control URLs changed on the primary text channel | `run/raw/control_probes.jsonl` |
| O5 | **0 of 2** null anchors changed; **0 of 10** in-frame self-pairs changed (text *or* byte), max intra-pair gap 0.006 s | `run/raw/control_probes.jsonl`, `run/raw/selfpair.jsonl` |
| O6 | **0 of 1107** pairs changed on the primary structural-text channel | `run/derived/metrics.json` |
| O7 | **7 of 1107** pairs changed on the byte channel (3 deep, 4 shallow) — all attr-only/script-only churn | `run/derived/metrics.json` |
| O8 | **359 of 1107** pairs show an ETag/Last-Modified difference while their canonical text is unchanged | `run/derived/metrics.json` |
| O9 | frame reproduces the frozen DESIGN sweep almost exactly (deep 686 / shallow 421, 1107 admitted, 1119 rows) | `run/derived/metrics.json`, `prereg.md#15` |

## 3. DERIVED MEASUREMENTS

| stratum | n pairs | k text | text UB95 | byte UB95 | certified level |
|---|---|---|---|---|---|
| DEEP (`hop>=3`) | 686 | 0 | **0.004357** | 0.011264 | **0.01** |
| SHALLOW (`hop<=2`) | 421 | 0 | **0.007090** | 0.021610 | **0.01** |
| ALL | 1107 | 0 | 0.002703 | 0.011844 | — |

Censoring: **0.0** in both strata (nothing died, nothing was unreachable, nothing
was rate-limited). Page-gone channel: `M-DEAD-404-*` = 0, bound 0.004357 (deep)
/ 0.007090 (shallow). Host composition: all **4** hosts span both strata
(deep/shallow: rust 220/43, pytest 219/98, readthedocs 28/140, pandas 219/140);
max host concentration 0.321 (deep) / 0.333 (shallow), below the 0.60 warning.
Version-pinned share 3.21 % (deep) / 0.24 % (shallow), far below the 0.80
`BOUNDED_TO_VERSION_PINNED` guard — the zero is **measured, not true by
construction**. Ledger: 8 + 1123 + 1137 = **2268** GETs of 3200; wall 463.32 s of
900; 0 truncated bodies; `M-PARTIAL = false`.

Mandate contrast: `M-CONCENTRATION-P-ONE-SIDED = 1.0`,
`M-CONCENTRATION-DETECTED = false`, `M-CONCENTRATION-MDC-RATE = 0.011662`.

## 4. INTERPRETATION

1. **H1 supported.** For this page class and vantage, a zero-GET intra-session
   freshness guard is unnecessary in **both** strata at reuse lags up to the
   measured separation (median 408 s), certified at the 1 % level. The
   certification is an upper bound, not an absence claim: at n=686/421 with zero
   events the exact 95 % bounds are 0.44 % (deep) and 0.71 % (shallow).
2. **H2 falsified, H3 not reached.** Hazard is **not** detected as concentrated in
   the deep stratum — but with the frame's power ceiling
   (`M-CONCENTRATION-MDC-RATE = 1.17 %`) that bounds concentration *at that
   level*; it is not evidence that the strata are identical. The
   certification outcome is symmetric (`CERTIFY_BOTH_AT_0P01`), so no
   hop-depth-scoped guard is indicated by this measurement.
3. **Instrument sensitivity was demonstrated, not assumed.** All three volatile
   URLs fired between observations while both static anchors and all ten in-frame
   self-pairs stayed silent. A zero from this instrument at this window is
   therefore interpretable, which is exactly what the parent packet could never
   say.
4. **The narrow primary channel is not hiding much.** The byte channel finds only
   7 attribute/script-only changes in 1107 pairs (deep UB 1.13 %, shallow UB
   2.16 %), so the primary channel's structural blindness costs roughly one order
   of magnitude in bound width here, not a change of decision.
5. **The pre-2.0 cycle-8 lesson replicates at scale.** 359 of 1107 pairs moved
   their ETag/Last-Modified while their canonical text did not change. An
   ETag-only detector would have called ~32 % of pairs "changed"; the frozen
   design correctly keeps that channel a covariate. This is a replication of an
   instrument lesson, on real HTML, at 1107-pair scale.
6. **Product consequence.** For credential-free, server-rendered documentation
   pages on this host class and vantage, an agent may inherit knowledge from
   `hop<=2` **and** `hop>=3` pages without a freshness GET for lags up to ~7
   minutes. This is a session-scale bound for a declared page class — **not** a
   shipped freshness mechanism, **not** a TTL, and **not** a promotion.

## 5. Secondary channel: executed, NOT admitted

The retro channel was run in a separate labelled pass: **292** parent reference
pages re-fetched, **0** byte changes, max per-host change rate 0.00 (so *not*
negotiation-suspected). It is nevertheless **NOT ADMITTED**, for two independent
frozen-module defects, both confined to the secondary path:

1. `parent_window()` uses `strptime("%Y-%m-%dT%H:%M:%SZ")` against the real frozen
   value `2026-10-17T00:45:32.184Z` → `ValueError` (this is what crashed the run).
2. Even with a tolerant read, the retro gate computes
   `dt_h = (rec.t_start - p_end)/3600` where `t_start` is a `time.monotonic()`
   reading and `p_end` is a POSIX epoch value, mixing two clocks and yielding a
   `−497831.61 h` median window, outside the frozen `[6 h, 30 d]` admission band.

By frozen design this channel **cannot change the primary label**. The
days-to-weeks band therefore remains undecided, exactly as `prereg.md#17` item 9
already declared. Its observational content (0/292 byte changes over ~0.5–1 day)
is recorded in `run/raw/retro.jsonl` and `run/derived/retro_secondary.json` as a
**non-decisional secondary observation**, not as a bound.

## 6. Validity threats carried forward

* **No JavaScript.** Client-rendered content is not measured at all — a page
  whose server HTML is stable but whose rendered DOM changes counts as unchanged.
  This is first-order for the product question and is inside the certification
  scope.
* **Attribute blindness of the primary channel.** By construction; quantified as
  7 pairs and bounded by the byte channel.
* **Window scope.** Valid at the measured separation only (median 408 s, max
  440 s). Not extrapolable to hours, days, JavaScript pages, authenticated pages
  or another egress vantage.
* **Four hosts, one page class, same-host `<a>` navigation.** Not a sample of the
  Web; `C-CROSSSITE` is untouched.
* **Power ceiling ~1.17 %** on the deep-vs-shallow contrast.
* **Host × depth × URL-class confounding** is reduced (4/4 hosts span both strata,
  no version-pinned ceiling) but not eliminated; `M-HOST-TABLE` is published so
  the reader can see per-host n and k.
* **359 unexplained transport moves** (O8) are not explained by this packet.

## 7. Claim ceiling

Per `spec.json#claim_ceiling_rules`: `C-WEB-DYNAMICS` **stays `HYPOTHESIS`**
(CC-C). A certification is a bounded measurement about a page class, not evidence
of predictive dynamical structure. No `EXPERIMENTAL`/`PRODUCT_CORE` promotion is
available from this packet and the producer does not self-promote. `C-FRESHNESS`
(guard calibration) is owned by graph/runtime/product and is not updated here.

## 8. Smallest next actions for the blockers

1. **Repair the two frozen retro defects at DESIGN** (tolerant timestamp parse +
   POSIX-epoch `dt_h`) and re-freeze; that alone would let the pre-2.0 TTL
   protocol's missing longitudinal point finally be taken, at ~292 GETs.
2. **Decide the product tolerance** (1 % / 2 % / 5 %) — the data certify 1 %;
   the choice is Product's.
3. **Do not reuse the 359 transport moves as evidence of staleness**; the frozen
   design correctly excludes them, and nothing here identifies their cause.