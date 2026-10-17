# EXP-FRONTIER-38940047535 — EXECUTE report

Packet: `research/experiments/EXP-FRONTIER-38940047535/` (design-contract v2, frozen
2026-10-17T00:29:40Z). Lane `frontier`. Target claim `C-CROSSSITE` (unchanged).
Producer outcome, stated once and not restated in weaker or stronger words anywhere
else in this file:

> **status = MEASUREMENT_INVALID, outcome = NOT_APPLICABLE.**
> Frozen gate **V4 (census gate) FAILED**: `n_admitted = 31 < MIN_ADMITTED = 40`.
> Zero revalidation GETs were spent. `decide()` returned `NO_DATA` and cannot yield a
> negative. This is representation loss, **not** a scientific falsification of
> persistence economics.

---

## 1. What was executed, exactly

1. **V1 code identity (PASS).** The frozen EXECUTE driver was reconstructed from the
   `FROZEN_CODE` block of the frozen `prereg.md` §10 by the prereg's own extraction
   rule (bytes strictly between the marker lines, `.strip()`, sha256). Recomputed
   digest `017c8bbcab9e8751ac5718affcf6563aa36c1cef82e6e23078c4d3d880804a0a` equals
   `DERIVED_SHA256` exactly. The reconstruction was written to `execute_module.py`
   (sha256 `6b6a1f39…`; the only added byte is a trailing newline).
2. **V2 controls gate (PASS).** `--stage controls` → `{"stage":"controls",
   "all_pass": true, "n": 15, "failed": []}`, run twice (standalone probe and inside
   the scored run). All fifteen offline fixture controls, including the five decision
   canaries (SUPPORTS / MIXED / MIXED-FLIP / FALSIFIES / NO_DATA), pass under the
   scoring code that produced this run's output.
3. **Live stage, one attempt, frozen defaults.** `python3 execute_module.py --stage
   all --out run/` — no `--sleep`, no `--cycles` override, no retry of the census,
   no re-run to obtain a better population (prereg §16 forbids exactly that).
   Commands and hashes: `provenance.json`.

Frozen inputs were re-verified as immutable **before and after** the run: all ten
`freeze.json.artifact_hashes` and all four `freeze.json.hashes` match. Nothing in
`request.json`, `spec.json`, `prereg.md`, `freeze.json` or `design_review.json` was
edited. No commit, push, branch switch or reset was performed.

## 2. RAW EVIDENCE (as recorded; no interpretation)

| raw artifact | sha256 (first 12) | content |
|---|---|---|
| `run/raw/controls.jsonl` | `aa1ce4036074` | 15 control rows, all `pass=true` |
| `run/raw/control_probes.jsonl` | `70e0bae5bd13` | observation-0 probes only: 3 positive + 2 null control URLs, all HTTP 200 |
| `run/raw/census.jsonl` | `37f3d87b4908` | 926 discovered-URL rows (hop, ordinal, status, bytes, sha256, final_url, `in_parent_208`, `admitted`) |
| `run/raw/paths.jsonl` | `5dc7d91a4f5b` | 31 admitted root→item chains |
| `run/raw/store_pages.jsonl` | `56d940eaf1d5` | 42 store pages with baseline signature + `t_first_s` |
| `run/raw/module_stdout.log` | `4b56266e00c1` | `controls 15/15` then `{"stage":"live","census_gate":"FAIL", …}` |
| `run/derived/metrics.json` | `97de07cf0b22` | module metrics, `gates_census`, `decision=NO_DATA` |
| `run/derived/decision.json` | `4cd637e1f901` | `census_gate_failed: true`, `outcome: NO_DATA` |

Directly recorded quantities:

- **Seeds:** 4/4 bound seeds HTTP 200, `seed_errors = {}`, `n_live_hosts = 4`.
- **Discovery:** 926 URLs (250 + 250 + 176 + 250) — *numerically identical to the
  frozen 4-host reference frame*.
- **Actual GET spend:** **302** GETs (10 / 13 / 176 / 103 per host), 20,560,422 body
  bytes, 32.0 s wall clock, `time_truncated = false` on all four hosts.
- **Deep stratum:** of 402 discovered URLs at hop ≥ 3, **363 were never fetched**, 39
  were fetched, 31 returned 200, and 31 items were admitted (29 at hop 3, 2 at hop 4).
- **Coverage:** definitional, as designed — `n_paths = n_admitted = 31`, zero misses
  (the parent's aged-external-list failure mode is structurally eliminated).
- **Overlap covariate:** `M-CENSUS-OVERLAP-PARENT208 = 31` — every admitted item is in
  the parent's frozen 208-item list.
- **Gate ledger:** 28 fixture GETs + 5 observation-0 probes + 302 census GETs = **335**
  = `M-TOTAL-GETS`, ceiling 3200.
- **Gate record:** `V3_seed_liveness` PASS, `V3b_census_min_admitted` **FAIL**
  (31 vs min 40), `V3c_coverage_definitional` PASS, `V6_denominator` PASS
  (cold = 302 > 0, N = 31 > 0).

## 3. DERIVED MEASUREMENTS (from the recorded raw rows; census stage only)

Per-site table (the mandated per-site report):

| host | discovered | GETs | hop ≥3 discovered | hop ≥3 → 200 | admitted | truncated |
|---|---|---|---|---|---|---|
| doc.rust-lang.org | 250 | 10 | 207 | 0 | 0 | false |
| pandas.pydata.org | 250 | 13 | 9 | 0 | 0 | false |
| docs.readthedocs.io | 176 | 176 | 36 | 28 | 28 | false |
| docs.pytest.org | 250 | 103 | 150 | 3 | 3 | false |

Census geometry of the gate-failed population (all `M-NON-DECISIONAL-*` or
gate-input quantities; **none of these is a decision input**):
store pages `K = 42`, interior pages 11, `sum|path| = 126`, mean path 4.0645,
sharing factor 3.0, reuse 2.818 items per interior page, per-item BFS discovery
ordinal mean 150.13 (min 101, max 174), never-fetched share of all discovered URLs
67.39 %, 8 of 39 fetched deep URLs non-200 (6 transport errors, 2 × HTTP 404).

**Decision quantities, all `null`:** `M-REVAL-PATH-GETS`, `M-REVAL-UNIQUE-GETS`,
`M-REVAL-NOSHARE-GETS`, `M-REVAL-PATH-BYTES`, `M-REVAL-PATH-ELAPSED`,
`M-ENDPOINT-GETS`, `M-INTERIOR-ONLY-FAILS`, `M-BREAK-EVEN-CYCLES`,
`M-BREAK-EVEN-DENSITY`, `M-CHANGE-RATE`, `M-DEAD-RATE`, `M-CHANGE-EVENTS`,
`M-DEAD-EVENTS`, `M-MOVED-EVENTS`, `M-N-PAGES-EVER-INVALID`, `M-PAGES-OBSERVED`,
`M-STORE-PAGE-SECONDS`, `M-HAZARD-RATE-UB95`, `M-PAGE-INVALID-UB95`,
`M-FALSE-ACCEPT-NAIVE`, `M-FALSE-ACCEPT-UB95`, `M-TAU-LADDER`,
`M-LIVE-POS-CHANGE`, `M-LIVE-NULL-CHANGED`. Each is null because
`M-WINDOWS-COMPLETED = 0`: the revalidation ladder was never entered. `null` here
means *not measured*, never *zero*.

## 4. INTERPRETATION (producer-level, bounded)

**4.1 The gate that fired and its exact mechanical cause.** The frozen traversal is
item-blind FIFO that stops *fetching* as soon as *discovery* reaches `BUDGET = 250`
(`while queue and len(out) < BUDGET`, with an inner `break` on `len(out) >= BUDGET`).
On the two hosts with wide shallow strata the discovery budget is exhausted before any
deep node is dequeued: pandas.pydata.org places 234 of its 250 discovered URLs at hop
2 and doc.rust-lang.org exposes 207 hop-3 URLs from only 4 fetched hop-2 pages. The
deep stratum is therefore **discovered but unfetched** (363 of 402 = 90.3 %), not
absent. The population that the frozen design requires (≥ 40 admitted items with live
status and parent chains) could not be registered, so the treatment — a persisted deep
path store revalidated over session cycles — was never instantiated or measured.
The census gate did exactly what it exists for: it stopped the ladder before any
revalidation GET was spent.

**4.2 This is not a negative for persistence economics.** No comparison was evaluated.
`A_w` and `B_w` have no inputs; the endpoint-only fallback arm never ran; the
invalidation hazard was never observed; the live positive/null control pair was
fetched once and never re-observed, so it is *not exercised*, not *passed*. Any
statement of the form "the store does / does not pay" is unsupported by this packet in
either direction, and `M-LIVE-POS-CHANGE = null` must never be read as "nothing
changes".

**4.3 Disclosed non-decisional counterfactual.** Had the 31-item population been
admitted, the frozen `decide()` inputs (`cold = 302`, `N = 31`, `mean_path = 4.0645`,
`|union| = 42`) would have satisfied both margin tests (`cold/N = 9.742`;
`A: 5.677 ≥ 0.974`; `B: 260 ≥ 30.2`). This arithmetic is recorded **only** to make
visible that `MIN_ADMITTED = 40` removed a store-favourable population, and to warn a
downstream reader that the same starvation inflates `cold/N` and so flatters the store.
`decide()` was not applied to these rows, no cycle ran, the label is fixed by frozen
G3, and this must not be used as a substitute measurement, as licence to lower
`MIN_ADMITTED`, or as evidence that the mechanism wins.

**4.4 An inherited unit defect surfaced (about the constants, not about this run).**
The mandate's constants `833.4` (batch) and `4.006731` (per item) derive from
`cold_batch_gets = 926`, and `926` is the frozen frame's per-host **discovered-URL**
count, not a GET count: this run rediscovered exactly 926 URLs while spending **302**
GETs under the identical policy, and the parent's own cited per-GET artifact
(`EXP-FRONTIER-38188815194/run/raw/economics.jsonl`) does not exist in the repository.
The inherited thresholds were therefore computed against a different unit from the one
`M-COLD-BATCH-GETS` is defined to be. This run's own accounting is internally
consistent (ledger-measured GETs reported as GETs, discovery reported separately, and
28 + 5 + 302 = 335 reconciled), but any future packet that reuses 926 as a GET count
would reintroduce the defect. This finding is about the historical constants; it is not
a measurement of this experiment and it changes no frozen value here.

**4.5 Repair status against the three defects the repair claimed.** Defect 1 (aged
external frame as denominator) is **confirmed repaired**: definitional coverage held
(`n_paths = n_admitted`), zero misses. Defect 2 (structural unreachability of the
ladder inside the harness envelope) is **confirmed repaired as an envelope fact**:
32.0 s used of a 620 s module budget, no per-host truncation, 335 of 3200 GETs — the
ladder would have fitted had the population existed, so the mechanism's blocking
defect is now population registration, not runtime. Defect 3 (cost-accounting
inconsistency) is **not re-observable**: with zero cycles there is no store cost to
reconcile, so `C-ACCOUNTING-RECONCILIATION` is UNKNOWN rather than PASS/FAIL.

## 5. Validity threats carried forward

Single runner vantage; session regime only (no day-scale claim is possible or
permitted — the legacy program established day-scale staleness is undecidable on
committed corpora); survivor conditioning in both directions (admitted items survived
the census, 8 of 39 fetched deep URLs were already dead/errored, and 363 deep URLs have
unknown status, so no lifetime or pre-census hazard statement may be derived); cost
model counts Web work only (GETs and bytes — no model calls, tokens or latency); base
SHA drift disclosed and non-threatening (executed at HEAD `07610b79…` vs
`pre_execute_sha 02e4034d…` / `request.base_sha 677bd0d2…`, with all fourteen frozen
hashes matching); worktree contains unrelated canonical Codex outputs that this lane
neither wrote nor modified; process hygiene clean (one module process, exited normally,
no orphan).

## 6. Consequence for the frozen product branches

Per frozen §18, an invalid branch builds nothing and records the exact gate. The gate
that fired is `V4_census_min_admitted`, and the exact unblocking condition is: **a
census policy that actually fetches the deep stratum it discovers** (e.g. fetch-until-
budget rather than discover-until-budget, or a budget/pruning rule that does not let a
wide shallow sidebar consume the whole queue) on the same four bound seeds, which would
have to re-register ≥ 40 admitted items before any revalidation GET is spent. That is a
substrate/policy change owned by runtime / `C-MEAS-VALID`, not a weakening of this
preregistration: the gate, the margin rule, the control set and the module identity are
all unchanged, and this packet proposes no re-run.

The mandate's stop rule is now live: it funded exactly one bounded attempt and stated
that a second invalid or null parks the full-path persistence subthread in favour of a
genuinely orthogonal basin. This attempt was invalid. Whether to park, or to authorise a
policy-level repair upstream of Frontier, is a Global Research Director decision; this
lane does not self-authorize a further attempt.

**No claim promotion.** `C-CROSSSITE` stays at its prior effective status
(`codex/claim_state.json.effective_event_by_claim[C-CROSSSITE]` = parent
`EXP-FRONTIER-38188815194`, decision MEASUREMENT_INVALID, registry status HYPOTHESIS).
Nothing in this packet is citable as support for or against `C-CROSSSITE`,
`C-PRODUCT-ECON` or any other claim.

## 7. Information classes, explicitly separated

- **RAW EVIDENCE** → §2 and `run/raw/*`, plus `execute_module.py`.
- **DERIVED MEASUREMENTS** → §3, `run/derived/*`, and `metrics` in `result.json`
  (with every non-measured frozen id explicitly `null`).
- **INTERPRETATION** → §4 (producer reasoning, bounded and labelled, including the
  non-decisional counterfactual and the inherited-unit finding).
- **AUDIT FINDING / DECISION / HANDOFF** → not produced here. They belong to the
  independent AUDIT and lane DIRECTOR stages, which will receive this packet, this
  report and `provenance.json`.