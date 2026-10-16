# EXECUTE report — EXP-RUNTIME-38182129488

- Experiment: `EXP-RUNTIME-38182129488` (lane `runtime`, design contract v2)
- Claim: `C-MEAS-VALID` (substrate validity only; no claim-status change, no promotion)
- Frozen decision label: **PARTIAL**
- Canonical `result.json` mapping: `status = COMPLETE`, `outcome = MIXED` (`spec.decision_rule.outcome_enum_mapping`)
- Frozen inputs: `request.json`, `spec.json`, `prereg.md`, `freeze.json`, `design_review.json` — hashes verified on disk against `freeze.json.hashes` before execution.

## 1. What was run

The exact frozen harness embedded in `prereg.md` / `spec.design_satisfiability_probe.source`
(sha256 `8ee0de445efc5c4c3c32e090a9799b24c092785d6d2bf31321aea3255334f987`) was written to
`run_experiment.py` and executed in its `--mode scored` path. That path runs the frozen
80-cell matrix (2 families × 4 novelty bands × 10 arms, 20 sessions/cell) **twice** for a
determinism check, measures the EXECUTE-only controls, verifies the transport/leak protocol
invariants, records the V1 code-fidelity manifest, evaluates gates V1–V8 and applies the
frozen memory-lattice decision rule (`classify_mem`). The `--mode probe` and `--mode selftest`
paths are non-outcome-bearing and were used only as cross-checks.

No model, browser, credential, external network, or external dataset was used. Wall clock for
the scored run: ~28m38s, all on loopback stdlib HTTP.

## 2. Result

**`decision_label = PARTIAL`.** All twelve measured gates are true
(`V1_code_fidelity_manifest`, `V2_transport_conformance`, `V3_no_leak`, `V4_determinism`,
`V5_arm_liveness`, `V6_counter_instrumentation`, `V7_matched_correctness`, `V8_ceiling_band`,
`V8_m0_counter_distinctness`, `V8_mechanism_off`, `V8_memory_off_attribution`,
`V8_reveal_order_attribution`), and the two matrix passes are byte-identical
(`determinism_ok = true`).

Success rates at the scored bands (novelty ≥ 0.50; 20 sessions/cell):

| arm | F1-RECORDS 0.50 | F1 0.75 | F2-WIDGETS 0.50 | F2 0.75 |
|---|---|---|---|---|
| `T-AMORTIZED-DISCOVERY` (treatment) | 1.000 | 1.000 | 1.000 | 1.000 |
| `PC-EXACT-REPLAY` (positive control) | 1.000 | 1.000 | 1.000 | 1.000 |
| `B-KNOWLEDGE-NO-MEMORY` (M-K) | 0.875 | 0.875 | 0.900 | 0.900 |
| `B-COLD-RE-DERIVE` (M0) | 0.875 | 0.875 | 0.900 | 0.900 |
| `B-RETRIEVAL-SHAPED` (M0 + retrieval) | 0.875 | 0.875 | 0.900 | 0.900 |
| `B-MEMORY-STATE` (M1) | 0.875 | 0.875 | 0.900 | 0.900 |
| `B-MEMORY-WINDOW-1` (M2a) | 1.000 | 0.875 | 1.000 | 0.900 |
| `B-MEMORY-WINDOW-2` (M2b) | 1.000 | 1.000 | 1.000 | 1.000 |
| `B-MEMORY-RECEIPT` (M3, PRIMARY) | 1.000 | 1.000 | 1.000 | 1.000 |
| `B-RETRIEVAL-MEMORYFUL` (M3 + retrieval) | 1.000 | 1.000 | 1.000 | 1.000 |

Every measured rate equals the frozen closed-form prediction exactly; the measured
**capacity threshold** is `1` retained commit receipt at novelty `0.50` and `2` at novelty
`0.75`, on both families — identical to `spec.memory_lattice_arithmetic.capacity_threshold_predicted`.
At novelty 0.00 and 0.25 all ten arms are 1.0 (ceiling band; the rule is not evaluated there).
`matched_correctness == success_rate` in all 80 cells; the minimum arm success rate over all
cells is 0.875.

## 3. Interpretation (bounded)

The hypothesis is confirmed. The predecessor's `(K-1)/K` separation is a function of
**comparator within-session memory capacity**, not of the treatment mechanism:

- It survives a state-only comparator (`B-MEMORY-STATE`, retains observed GET state but no
  receipts) and sub-distance receipt memory: `B-MEMORY-WINDOW-1` (1 receipt) survives at
  novelty `0.50` (chain-to-precursor distance 1) and collapses at `0.75` (distance 2).
- It **collapses** as soon as the comparator retains enough commit receipts to span the
  chain-to-precursor distance: `B-MEMORY-WINDOW-2` (2 receipts) and the PRIMARY full-log
  comparator `B-MEMORY-RECEIPT` reach the treatment level (1.0) at both scored bands.
- The full-receipt comparator is not merely rate-identical to the treatment; it is also
  counter-identical (margin 0, 0/4 counter dimensions distinct). This is disclosed in
  `design_review.json` as the substantive collapse mechanism on a single-success-path
  substrate, not an accidental identity. The comparison is non-vacuous because
  `mem_certifies` requires a positive margin, so an identical comparator can never certify,
  and the distinct weaker comparators (`B-MEMORY-STATE`, `B-MEMORY-WINDOW-1`) carry the
  discriminating signal and the capacity threshold.

Controls behave as pre-declared and are measured on the scored schedule:
`NC-MECHANISM-OFF` raises cold to 1.0 on both families and destroys the predecessor
certificate; `NC-MEMORY-OFF` and `NC-REVEAL-ORDER-FLIPPED` both return to `(K-1)/K`
(0.875 F1 / 0.900 F2), isolating receipt retention and the precursor first-commit reveal as
the causes; `NC-RETRIEVAL-REDUNDANT` holds (retrieval-memoryful equals receipt-memoryful);
`NC-WINDOW-MONOTONIC` holds; `NC-CEILING-BAND` and `NC-NO-LEAK` hold.

`NC-NO-DISCOVERY-DIRECT` and `NC-BINDING-UNIQUENESS` are probe-verified
(`artifacts/probe_mode.json`), since the scored driver does not exercise those policy paths.

## 4. What this does and does not mean

- **Does:** convert the predecessor's disclosed, uninstrumented `NC-MEMORYFUL` boundary into a
  measured, quantitative capacity threshold. The certified bank cannot supply discriminative
  dynamic range against a comparator arm that retains a full within-session commit-receipt log
  (or ≥ 2 receipts at novelty `0.75`, ≥ 1 at `0.50`).
- **Does not:** promote any mechanism or the bank into Product Core; change `C-MEAS-VALID`
  status; generalize beyond `SBA-CREDENTIAL-FREE-V2` with `K ∈ {8,10}`; or say anything about
  natural Web tasks, external agents, or baseline strength. It is not a re-run of the
  memoryless certificate (mandate stop trigger honored).

## 5. Consequence

Per `spec.product_consequence_negative` and the mandate stop trigger: the negative is
decision-changing, not an infrastructure failure. Product receives the concrete bank-design
requirement — a hardened `V3` whose success requires mechanism- or composition-dependent
behaviour rather than mere receipt retention — together with the measured capacity threshold
(1 receipt at novelty `0.50`, 2 at `0.75`). No further memoryless re-run is authorized by this
packet. The bank-design question is handed to Product / the Global Research Director.

## 6. Provenance and integrity

- EXECUTE harness sha256 `8ee0de44…` equals `spec.design_satisfiability_probe.source_sha256`
  and the `prereg.md` `BEGIN/END SBA-MEM-HARNESS` block; recorded in `result.json.artifacts`
  and the V1 manifest with `python 3.12.15`.
- Probe stdout sha256 `f8c58794…` and selftest stdout sha256 `74a833f6…` reproduce the frozen
  `prereg.md` DESIGN values byte-for-byte (two executions each).
- Raw evidence: `artifacts/run_scored.json` (full cells, controls, gates, lattice detail),
  `artifacts/probe_mode.json`, `artifacts/selftest_stdout.json`, `artifacts/run_scored.stderr`.
- `freeze.artifact_hashes` is empty (no mutable local interpretation dependency; the harness is
  frozen in `prereg.md`/`spec.json`).
