# R1 CYCLE 1 — REPAIR ROUND 2 REPORT

Repair of cycle R1-1 per the independent REVISE audit gate
`CYCLE_32921019845_RUNTIME` (team snapshot run 32921019845, tip `9e1875d`;
repair round 2 = run 32924286888). Repair starts from the exact rejected
team snapshot (`cycle/runtime/32921019845/team` @ `9e1875d`, linear
successor commits, no amend/rebase — freeze chain `e95e4a9 → 1b5ae4d →
20f285e → 9ddd723 → 66468f4 → 93f374a → 9e1875d` preserved bit-for-bit).

Scope honored exactly: **only** `required_fixes` RF-4..RF-5. The frozen
prereg, task set, thresholds, success oracle, win/verdict rule, all
wording ceilings and ALL outcome artifacts (offline policy sweep, live-arm
streams/results, negative controls, wb-v2 capsule + derivation manifest,
events stream) are untouched — verified mechanically (`git diff` vs base
empty on every protected path; sha256s re-pinned to their round-1 values
in the regenerated artifact's `repair_round_2_provenance` block). No live
arm was re-run (none authorized; none needed). The B-KILLED scientific
core is quoted verbatim, unchanged.

## RF↔fix mapping

### RF-4 — residual construction double count in the write-side aggregate (moderate)

Defect: op `put_fresh` is timed as `store.put(fresh_record(...))`, so ONE
FULL record construction (schema validation + canonical content hashing)
executes inside its timed region; op `build_record` measures that same
construction standalone; `ObservationStore.put` re-computes the content
sha as an integrity check, so persistence itself does not include
construction. The prior aggregate summed both ops and counted construction
twice (~0.5155 ms/cycle, ~22%).

Containment relation (one line): **op `build_record` ⊂ op `put_fresh`,
because the bench times fresh persistence as
`store.put(fresh_record(...))`; summing the two ops counted one underlying
construction twice.**

| Surface | Before | After |
|---|---|---|
| `runtime/economics.py::break_even_table` | `write_side = build_record+put_fresh+hygiene_filter+derive_successors+registry_append` | construct-once flow `put_fresh+hygiene_filter+derive_successors+registry_append` + new `write_side_containment_note` |
| `results/runtime/economics/wb_maintenance_results.json` `.write_side_median_ms_per_cycle` | `2.3187` | `1.8032` (= committed put_fresh+hygiene+derive+append medians, full stored precision) |
| same `.write_side_incl_put_idempotent_median_ms_per_cycle` | `2.4173` | `1.9018` |
| same `.write_side_scope` | listed `build_record` in the summed path | names the containment ("construction counted exactly ONCE via put_fresh because build_record ⊂ put_fresh"); retains "EXCLUDES put_idempotent" verbatim |
| `results/runtime/r1_cycle1_state.json` `.p3_write_back_economics.write_side_*` | `2.32` / `2.42` | `1.8032` / `1.9018` (+ `write_side_containment_definition` mirroring the RF-1 `recurring_tax_definition` pattern) |
| `reports/runtime/R1_CYCLE1_REPORT.md` §Priority-3 | "≈2.32 / ≈2.42 ms/cycle" | "≈**1.80** / ≈**1.90** ms/cycle [corrected in repair round 2 … audit RF-4]" + ops-table caption tags `build_record` as a decomposition component |

Prior totals are preserved ONLY as labeled superseded upper bounds inside
the artifact's provenance note and this report — never quotable as current
figures.

Containment witness (not merely code-read):
`tests/runtime/test_repair_r2.py::TestWriteContainment` runs the REAL
`run_benchmark()` with counting wrappers over `build_record` and
`ObservationStore.put` plus a `_timed` region spy, and requires EXACTLY
one timed region embedding REPS constructions with REPS persistences
(equality, so both undercount-by-hoisting and overcount-by-duplication
refactors fail loudly), a standalone-construction region, a
no-construction idempotent region, and the full structural fingerprint
(2·REPS constructions inside timed regions + exactly 1 outside). Source
witnesses additionally pin that `ObservationStore.put` performs integrity
re-hashing without referencing `build_record`. Formula pins lock the
corrected aggregate against the committed artifact and forbid the return
of the double count.

Regeneration method (no hand-editing, no re-measurement): identical
discipline to repair round 1 — `runtime/repair_r2.py` transcribes per-op
summaries from the committed events stream `wb_maintenance_events.jsonl`
(byte-untouched; sha256 re-pinned to the round-1 value as an explicit STOP
rule), asserts EXACT deep equality with the prior `operations[]` array,
pins canonical serialization by reproducing the prior bytes first,
sanity-checks that the input is EXACTLY the audited defective state
(2.3187/2.4173) and the output lands EXACTLY on the auditor-prescribed
aggregates (1.8032/1.9018), applies the surgical transform via the
repaired `economics.break_even_table()`, enforces the enumerated diff
budget (changed keys {write_side_median_ms_per_cycle,
write_side_incl_put_idempotent_median_ms_per_cycle, write_side_scope};
added keys {write_side_containment_note} ∪ {repair_round_2_provenance};
nothing removed; frozen fields — including the entire
`repair_round_1_provenance` block — deep-identical pre/post), then writes.
A verify mode reconstructs the pre-repair document from constants and
proves the committed file is the bit-for-bit fixed point of the transform
(`--check` passes cleanly; also pinned as a test).

Direction disclosure (preempting "outcome-improving edit" reading): this
correction LOWERS the quoted write-side overhead (~22%), i.e. flatters
the write-back mechanism. Mitigations unchanged by the repair:
`reuse_yield` stays UNDEFINED (numerator structurally absent); no gate
consumed either figure; the B-KILLED verdict rests on stream-counted
browser actions, not economics. As in round 1, fidelity to measurement
truth is treated as non-directional.

Disclosed residual shared-primitive overlap (found during this repair,
NOT silently re-derived): `hygiene_filter ⊂ derive_successors` — both
execute `strip_value_tokens` (`runtime/writeback.py`). Magnitude
≤ 0.08% of the corrected aggregate (0.0014 ms/cycle); direction
conservative (inflates the overhead denominator); LEFT AT THE
AUDITOR-PRESCRIBED AGGREGATION pending auditor disposition, disclosed in
the artifact's containment note, this report, and pinned by test.

### RF-5 — stale lane-state fields left by repair round 1 (minor)

`results/runtime/r1_cycle1_state.json`: the stale bare `tests.lane_suite`
"109 passing" figure is replaced by the explicit count lineage —
"109 passing at outcomes commit 9ddd723; 120 after repair round 1 (run
32921019845); 129 after repair round 2 (run 32924286888)" — and a
top-level `repair_round_2` block records this repair's run id, base tip,
gate, required fixes and report pointer (mirroring the round-1 block;
history not rewritten).

## Propagation completeness sweep

All durable surfaces carrying the defective figures were enumerated by
grep and corrected: results JSON `break_even_table` (via deterministic
regeneration), lane state JSON `p3_write_back_economics`, cycle report
§Priority-3 (text + ops-table caption marking `build_record ⊂
put_fresh` symmetric to the RF-1 `index_read_all` treatment),
`economics.py` formula/docstrings/op-list/ASYMPTOTIC_ORDERS. Intentionally
UNAMENDED historical quotations (disclosed, superseded by durable memory):
`reports/runtime/R1_CYCLE1_REPAIR_ROUND1.md` §RF-3a quotes ≈2.32/≈2.42 as
then-current values (historical document, bytes preserved), immutable
commit messages of runs 32916020607/32921019845 (`9ddd723` "~2.3ms/cycle
write-side", `9ddd723` "~0.6ms/resolve"), and the pre-repair bytes of the
results JSON (hash-recorded in the provenance block). No other file in the
repo quotes 2.3187/2.4173/2.32/2.42 for this economics telemetry outside
these disclosed locations.

The denominator scenario term that consumes the write side moves
consistently: e.g. 1 stale-free cycle at 7 resolutions costs ≈ 1.80 +
7×0.38 = 4.49 ms (was 6.00 under the double-counted aggregates);
`resolves_per_cycle_assumed`, recovery term and numerator definitions are
untouched.

## Immutable-history discrepancy (disclosed, not repaired)

As in round 1: no frozen document or commit message is amended. Git
history stays append-only (W4-freeze-chain discipline). This report and
the regenerated artifacts supersede superseded wording for anyone reading
durable memory.

## Tests

- After repair round 2: **129/129 passing** (`pytest tests/runtime`,
  Python 3.12.3, pytest 9.1.1) — 120 preserved from round 1 + 9 new
  repair-round-2 pins (`tests/runtime/test_repair_r2.py`): live-bench
  containment witness, two source witnesses, corrected-aggregate formula
  pin, scope/disclosure-text pins (including the residual-overlap
  disclosure), deterministic-regeneration fixed-point pin, and three
  lane-state propagation pins. No existing test was weakened; the
  round-1 suite passes unchanged.
- Bench re-runs during testing exercised the strengthened RF-2 guard
  end-to-end on real accepted paths (pre/post digest comparison clean);
  these runs' timings are NON-GOVERNING diagnostics written to temporary
  paths only, never near the committed measurement artifacts.

## Protected artifacts (mechanical proof of non-interference)

`git diff 9e1875d -- <path>` empty for: frozen prereg, policy-sweep
probe, negative-controls probe, entire `r1_strong/` evidence tree, wb
registry (index + v1/v2 capsules + derivation manifest), observation
store, events stream, audited R0-2 modules, gating modules, and all
Director-owned surfaces (`docs/RUNTIME_LEDGER.md`, `docs/NEXT_RUNTIME.md`,
`state/runtime_loop.json`, `directives/RUNTIME.md`). sha256s of the seven
headline outcome artifacts are embedded in the regenerated results JSON's
`repair_round_2_provenance.outcome_artifacts_untouched_sha256` and equal
the round-1 recorded values.

## Evidence tier

Cycle R1-1 remains **DURABLE_UNAUDITED** until the independent auditor
accepts this repair round. Nothing here self-upgrades a tier; the
scientific core (B-KILLED at prereg ceilings) is quoted verbatim,
unchanged.

Durable negative knowledge added by this repair: two aggregate
double-counts of the same disease class were found in one decomposition
bench (RF-1 consumer side, RF-4 producer side) — aggregates over
decomposed operations must ship with mechanically pinned containment
relations, or a second instance will hide behind the first fix.

## Files changed by this repair

| Path | Change |
|---|---|
| `runtime/economics.py` | RF-4 construct-once aggregate + containment/scope notes; put_fresh embedding stated in module docstring, ASYMPTOTIC_ORDERS and bench comments; break_even_table docstring updated |
| `runtime/repair_r2.py` | NEW deterministic regeneration script (stop rules inline; events-sha re-pin; fixed-point verify mode) |
| `tests/runtime/test_repair_r2.py` | NEW live-bench containment witness + source witnesses + formula/disclosure pins + regeneration pin + state propagation pins |
| `results/runtime/economics/wb_maintenance_results.json` | surgical RF-4 aggregate correction + additive containment note + repair_round_2_provenance block |
| `results/runtime/r1_cycle1_state.json` | RF-4 propagated figures/definitions + RF-5 count-lineage + repair_round_2 block |
| `reports/runtime/R1_CYCLE1_REPORT.md` | Priority-3 corrections with inline tags + round-2 header notice |
| `reports/runtime/R1_CYCLE1_REPAIR_ROUND2.md` | NEW (this file) |

Not touched: everything else — including Director-owned
`docs/RUNTIME_LEDGER.md`, `docs/NEXT_RUNTIME.md`,
`state/runtime_loop.json`, `directives/RUNTIME.md`.
