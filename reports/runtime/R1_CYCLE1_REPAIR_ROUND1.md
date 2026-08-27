# R1 CYCLE 1 — REPAIR ROUND 1 REPORT

Repair of cycle R1-1 per the independent REVISE audit gate
`CYCLE_32916020607_RUNTIME` (team run 32916020607, tip `66468f4`; repair
round 1 = run 32921019845). Repair starts from the exact rejected team
snapshot (`cycle/runtime/32916020607/team` @ `66468f4`, linear successor
commits, no amend/rebase — freeze chain `e95e4a9 → 1b5ae4d → 20f285e →
9ddd723 → 66468f4` preserved bit-for-bit).

Scope honored exactly: **only** `required_fixes` RF-1..RF-3. The frozen
prereg, task set, thresholds, success oracle, win/verdict rule and ALL
outcome artifacts (offline policy sweep, live-arm streams/results,
negative controls, wb-v2 capsule + derivation manifest) are untouched —
verified mechanically (git diff vs base empty on every protected path;
sha256s recorded in the regenerated artifact's provenance block). No live
arm was re-run (none authorized; none needed).

## RF↔fix mapping

### RF-1 — double-counted recurring consumer-side tax (moderate)

Defect: `resolver.resolve()` executes `Registry.all_latest()` internally
(`runtime/resolver.py:59`), so op `index_read_all` measures work already
contained in op `resolve_e2e`. The aggregate summed both.

| Surface | Before | After |
|---|---|---|
| `runtime/economics.py::break_even_table` | `per_resolve = ops["index_read_all"] + ops["resolve_e2e"]` | `per_resolve = ops["resolve_e2e"]` + containment/scope notes + repair_provenance field |
| `results/runtime/economics/wb_maintenance_results.json` `.break_even_table.per_resolve_recurring_ms` | `0.5794` | `0.3839` (= committed resolve_e2e median, full stored precision) |
| `results/runtime/r1_cycle1_state.json` `.p3_write_back_economics.recurring_per_resolve_ms` | `0.58` | `0.3839` (+ `recurring_tax_definition` stating the containment relation) |
| `reports/runtime/R1_CYCLE1_REPORT.md` §Priority-3 | "recurring consumer-side tax ≈ 0.58 ms/resolve" | "≈ 0.38 ms/resolve = resolve_e2e ALONE [corrected … RF-1]" |

Containment relation (one line, as demanded): **op `index_read_all`
(`Registry.all_latest()`) ⊂ op `resolve_e2e`, because
`resolver.resolve()` executes `Registry.all_latest()` internally;
summing the two ops counted one underlying operation twice.** The
containment is mechanically witnessed, not merely code-read:
`tests/runtime/test_repair_r1.py::TestRecurringContainment` counts
`all_latest` invocations inside a live `resolve()` (≥1 required) and pins
the corrected formula against the bench doc, so a future refactor that
removes the internal index read fails loudly instead of silently
invalidating the note.

Regeneration method (no hand-editing, no re-measurement): the primary
measurement record is the committed events stream
`wb_maintenance_events.jsonl` — byte-untouched by this repair. Its note
discriminators carry complete per-op cold/min/median/max/reps summaries.
`runtime/repair_r1.py` transcribes those summaries, asserts EXACT deep
equality with the prior `operations[]` array at stored precision
(pre-committed stop rule: any mismatch aborts without writing), pins the
canonical serialization by reproducing the prior file bytes first, applies
the surgical transform via the repaired
`economics.break_even_table()`, enforces an enumerated diff budget
(only `per_resolve_recurring_ms` may change inside `break_even_table`;
one top-level key `repair_round_1_provenance` may be added; frozen fields
deep-identical pre/post), then writes. Per-op medians remain the original
committed measurements; rep-level samples were never emitted, so nothing
was re-derived beyond transcription — disclosed rather than overclaimed.

Disclosed stop-rule event: during development the script's own diff-budget
check aborted once (top-level budget evaluated before the provenance block
was added) and once more on a stale test-path reference inside note text;
both aborted BEFORE any write, were fixed in the script, and the
regeneration was re-run from the pristine prior document. No output was
produced under a relaxed rule.

Direction disclosure (preempting "outcome-improving edit" reading): this
correction LOWERS the quoted overhead, i.e. flatters the write-back
mechanism. Mitigations unchanged by the repair: `reuse_yield` stays
UNDEFINED (numerator structurally absent); no gate consumed either figure;
the B-KILLED verdict rests on stream-counted browser actions, not
economics. The paired RF-3a correction moves the OPPOSITE direction
(write-side disclosure gains the previously omitted branch): fidelity to
measurement truth is non-directional here.

### RF-2 — accepted-state guard did not match its claim (minor)

Defect: prereg/report said "accepted-path byte identity asserted after";
the implemented guard checked existence + registry cardinalities only.
The FROZEN prereg sentence cannot be edited (Director-owned freeze), so
the stronger option was taken: make the claim true going forward and
disclose the history.

Implementation (`runtime/economics.py`):
- `accepted_state_digests()` — per-file sha256 over the WHOLE accepted
  trees (parent registry, wb registry incl. both derivation manifests,
  observation store incl. all records) plus the bench input snapshot;
  whole-tree walk so unreferenced live files cannot escape; referenced-
  artifact existence validation from each index; fail-closed (symlinks/
  non-regular files flagged, vanished files are errors — never skipped).
- `assert_accepted_state_untouched(pre_digests, roots,
  check_cardinality=True)` — compares post-run digests to pre-run;
  called WITHOUT pre-digests it deliberately returns an explicit
  "byte identity NOT asserted" error instead of silently passing
  (fail-closed against silent claim weakening). Cardinality checks
  retained as belt-and-suspenders.
- `run_benchmark()` wiring: records digests BEFORE cloning and RAISES
  post-run on any difference — the runner itself now asserts, not just
  tests (`test_repair_r1.py::TestAcceptedStateGuardRF2::
  test_bench_runner_wires_the_guard` proves the wiring with a spy).
- Tamper detection proven on INJECTED temporary trees only (modified /
  removed / added / symlink-swapped files) — real accepted paths are
  never mutated by tests (R0-1 C7 invariant preserved). A digest-root
  helper provides a compact provenance scalar while the per-file map
  remains diagnostic ground truth.

Honesty framing: prospective strengthening ONLY. It proves THIS run (and
future runs) touched nothing; it does not retroactively re-verify the
original outcome-time run, whose protection argument remains /tmp-bench
confinement by code inspection plus a clean tracked tree. Report wording
updated accordingly; module/guard docstrings updated to describe what is
actually done.

### RF-3 — economics wording precision (minor)

(a) put_idempotent exclusion NAMED everywhere the write-side figure
appears: report now states fresh-write total ≈ 2.32 ms/cycle EXCLUDES
`put_idempotent` (0.099 ms, reported separately) and gives ≈ 2.42 ms/cycle
including it; `break_even_table` gained `write_side_scope`,
`put_idempotent_median_ms`,
`write_side_incl_put_idempotent_median_ms_per_cycle`; state JSON gained
`write_side_scope` with the same content.
(b) "dual-named rows" description DROPPED from the economics surfaces
(report §Priority-3 + `run_benchmark` docstring): these are single-schema
`spider.cost_event/v0` SINGLE-written rows riding note discriminators; no
new envelope fields (auditor-verified). Pilot-era files that genuinely
emit twin rows are out of scope and unchanged.
(c) Non-gating status of `context_signature.observed_entry_hosts` stated
explicitly in the report's wb-v2 section AND converted into a checked
invariant:
`tests/runtime/test_repair_r1.py::TestNonGatingContextSignature` scans the
gating modules (retrieval/resolver/predicates/validate — the auditor's
scope) for any reference; prose claim became mechanical pin.

## Propagation completeness sweep

All durable surfaces carrying either defective figure were enumerated by
grep and corrected: results JSON `break_even_table`, lane state JSON
`p3_write_back_economics`, cycle report §Priority-3 (text + ops-table
caption marking `index_read_all` as a decomposition component),
`economics.py` formula/docstrings. No other file quotes 0.5794/0.58 or
"dual-named" for the economics telemetry. The denominator scenario term
that consumes `per_resolve` (7 resolutions/cycle) moves 4.06 → 2.69
ms/cycle consistently with the same correction.

## Immutable-history discrepancy (disclosed, not repaired)

Outcomes commit `9ddd723`'s message says "~0.6ms/resolve recurring". Git
history is NOT amended (W4-freeze-chain discipline; rewriting would
destroy the audited git-orderable freeze chain). This report and the
regenerated artifacts supersede that message text for anyone reading
durable memory.

## Tests

- Before repair: 109/109 passing (auditor-reproduced baseline).
- After repair: **120/120 passing** (`pytest tests/runtime`, Python
  3.12.3) — 109 preserved + 11 new repair-round-1 pins
  (`tests/runtime/test_repair_r1.py`) + contract update of one existing
  economics test to the fail-closed guard semantics.
- Bench re-runs during testing exercised the strengthened guard end-to-end
  (pre/post digest comparison clean on real accepted paths); these runs'
  timings are NON-GOVERNING diagnostics and were not written anywhere
  near the committed measurement artifacts.

## Protected artifacts (mechanical proof of non-interference)

`git diff HEAD -- <path>` empty for: frozen prereg, policy-sweep probe,
negative-controls probe, entire `r1_strong/` evidence tree, wb registry
(index + v1/v2 capsules + manifest), audited R0-2 modules, gating modules.
sha256s of the seven headline outcome artifacts are embedded in the
regenerated results JSON's `repair_round_1_provenance.
outcome_artifacts_untouched_sha256` for auditor recomputation.

## Evidence tier

Cycle R1-1 remains **DURABLE_UNAUDITED** until the independent auditor
accepts this repair. Nothing here self-upgrades a tier; the scientific
core (B-KILLED at prereg ceilings) is quoted verbatim, unchanged.

## Files changed by this repair

| Path | Change |
|---|---|
| `runtime/economics.py` | RF-1 formula + notes; RF-2 digest guard + runner wiring; RF-3b docstring |
| `runtime/repair_r1.py` | NEW deterministic regeneration script (stop rules inline) |
| `tests/runtime/test_repair_r1.py` | NEW containment witness, formula pin, guard tamper/wiring, non-gating pin |
| `tests/runtime/test_economics.py` | guard-contract update (fail-closed semantics) |
| `results/runtime/economics/wb_maintenance_results.json` | surgical RF-1 aggregate correction + additive scope/note/provenance fields |
| `results/runtime/r1_cycle1_state.json` | propagated figures + repair pointer |
| `reports/runtime/R1_CYCLE1_REPORT.md` | Priority-3 corrections with inline tags + header notice |
| `reports/runtime/R1_CYCLE1_REPAIR_ROUND1.md` | NEW (this file) |

Not touched: everything else — including Director-owned
`docs/RUNTIME_LEDGER.md`, `docs/NEXT_RUNTIME.md`,
`state/runtime_loop.json`, `directives/RUNTIME.md`.
