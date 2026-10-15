# EXP-GRAPH-38385040804 EXECUTE report — Graph abstention-boundary retest: BLOCKED (frozen-runner defect, no measurements)

## 1. What was asked

Under a pre-registered exclusive-vs-inclusive `unknown_precision` denominator and against an honest out-of-sample retrieval comparator (`B-RETRIEVAL-OOS`, pooled FIT-TRAIN ≥2× parent n, disjoint FIT-SELECT, hard `mu>0`), decide whether the AXIS-G2-RETEST shortfall persists as a no-refit structural bound (H1) and whether Product's retrieval-B requirement stands as specified (H2), via the frozen T-FRAME cascade and five-value retrieval fork.

## 2. What happened (RAW EVIDENCE → OBSERVATION)

- **Extraction (valid):** the `FROZEN-RUNNER` block from frozen `prereg.md#13` was extracted to `raw_evidence/runner_tframe_g3_oos.py` with exactly one trailing newline; sha256 `7816fbd2…1ed2c9b` equals the declared `CANONICAL-RUNNER-SHA256`. Extraction is byte-faithful.
- **Execution (failed, both entry points):** `runner … --mechanics-only` (twice) and the full scored run each exited `1` with empty stdout and byte-identical stderr (`raw_evidence/mech_stderr.txt`, `raw_evidence/run_stderr.txt`, sha `1fefefe3…5320`):
  `UnboundLocalError: cannot access local variable 'a' …` at runner line 479, `select_gids=[f"{a}:…" for _, r in sel_app] + …`.
- **Root cause (frozen, not environmental):** the defect is verbatim in the frozen `prereg.md#13` block — the `train_gids` comprehension binds `a` (`for a, r in train`) while both `select_gids` comprehensions bind `_` yet interpolate `{a}`; since `a` is assigned later in `main()` by statement-level loops, the line reads a local before assignment on every invocation. Banks loaded and axes built normally up to that statement, so no dependency (Python stdlib, `goal_generator`, bank blocks) is implicated.
- **Consequence:** zero TEST rows scored, zero metrics/controls/gates emitted. `result.json` carries `status=BLOCKED`, `outcome=NOT_APPLICABLE`, empty `metrics`/`controls`, and the four raw/derived artifacts with hashes.

## 3. DERIVED MEASUREMENTS

None. There is deliberately no `run_output.json`: the runner never reached measurement code.

## 4. INTERPRETATION (bounded)

- This packet answers neither H1 nor H2 and changes nothing about `C-SEMANTIC-RESOLVE`: the effective event stays the parent `EXP-GRAPH-38291080992` decision (`DECIDE_REQUIRE_RETRIEVAL_B`, HYPOTHESIS retained, no promotion), cited here as inherited context only — no parent number was re-measured.
- The BLOCKED status is an infrastructure/design-implementation failure, not a scientific negative, per the packet contract: it must not be read as falsification of the no-refit bound or of honest-retrieval viability.
- Process finding for AUDIT/DIRECTOR: the v2 satisfiability probes and independent `design_review.json` (all six PASS) evidently never executed the frozen block's `main()` construction path — any invocation with the frozen banks present crashes before any measurement. Review gates for future frozen runners should require actually running the frozen block's entry points, not scanning them.

## 5. What EXECUTE did not do (immutability)

No frozen file (`request.json`, `spec.json`, `prereg.md`, `freeze.json`, `design_review.json`, or any of the four `freeze.json.artifact_hashes` files — all re-verified hash-identical) was modified, and the one-token-class repair was deliberately not applied: fixing the runner inside this packet would break the canonical hash and the frozen transaction. The repair belongs to a new DESIGN transaction (see `failure.json#smallest_next_action`).

## 6. Handoff pointers

- `result.json`: machine handoff (`BLOCKED` / `NOT_APPLICABLE`, observations, validity notes, unresolved).
- `failure.json`: stage failure record with durable diagnostic and smallest next action.
- `provenance.json`: reproduction commands, hashes, environment.
- Raw evidence: `raw_evidence/runner_tframe_g3_oos.py`, `mech_stdout.json` (empty), `mech_stderr.txt`, `run_stdout.json` (empty), `run_stderr.txt`.
