# EXECUTE report — EXP-PRODUCT-38197856050

- Lane: `product`
- Frozen inputs: `request.json` (global-director-REOPEN of `C-PARAM-INHERIT`), `spec.json`, `prereg.md`, `freeze.json`, `design_review.json` — all byte-identical to freeze (see `validity_notes` in `result.json`).
- Status: **COMPLETE** — the measurement transaction completed validly on the exact shipped carrier.
- Outcome: **FALSIFIES** (decision `WIDENING_UNSAFE`), exactly the frozen DESIGN point-prediction.
- Claims: `C-PARAM-INHERIT` stays `EXPERIMENTAL`, `C-SEMANTIC-RESOLVE` stays `HYPOTHESIS`. No advance, no promotion (frozen claim-status semantics observed by this EXECUTE stage; the verdict is the DIRECTOR's).

## 1. What was executed

The FROZEN RUNNER block embedded in `prereg.md` was materialized byte-for-byte (V8 clause B `norm`-match verified) to
`harness/run_bank.py` and executed once for real (two full evaluation passes inside the runner for the determinism anchor).
The runner is READ-ONLY on the repository: it never writes `src/spider/` or any freeze artifact (confirmed by post-run re-hash).

Arms, all built from the SAME four frozen induced mechanisms on the SAME 292-item bank against the SAME loopback oracle:

- `T-WIDENED-PRINCIPLED` (treatment): induced supports rewritten in-run to the frozen data-driven widening rule `widen_support(train values)`.
- `B-SHIPPED` (shipped baseline): unmodified greedy shared-prefix supports.
- `B-DECLARED-FULL` (strong comparator): supports rewritten to the declared grammars (ceiling).
- `PC-UNSAFE-COARSE` / `PC-OVERWIDE-OPEN` (sensitivity positives), `NC-REJECT-ALL` (null floor), `B-LITERAL-KERNEL` (ablation), `PC-EXACT-REPLAY` (25/25 validity anchor), `PC-DETERMINISM-REPEAT`.

## 2. RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION

### RAW EVIDENCE
`raw_run_output.json` (sha256 `ba894b69...`) — the runner's complete JSON certificate; `raw_run_stderr.txt` (sha256 `50e0b058...`) — unittest output (`Ran 3 tests ... OK`).

### OBSERVATION (direct, non-interpretive)
- Shipping kernel sha256 == frozen carrier sha256 (`718efa6a...`); tree clean apart from this packet's own outputs.
- Induced shipped supports equal the four frozen constants; widened supports equal the four frozen `EXPECTED_WIDENED` constants.
- The treatment arm issued HTTP on 9 OUT-labelled items, all in family D (`FD-OG-WRONGRANGE00..08`); the oracle answered 404 to each.
- Both evaluation passes agreed on every treatment/shipped/declared number and on support identity.
- The regression suite ran 3 tests with 0 failures/errors.

### DERIVED MEASUREMENT (values from the certificate, stable ids as frozen)
| metric | value |
|---|---|
| `M-BANK` | 292 items: 63 IN / 229 OUT (A 16/56, B 18/55, C 19/53, D 10/65) |
| `M-T-WIDENED-FALSE-ACCEPT-COUNT` | **9** (frozen prediction 9) |
| `M-T-WIDENED-SILENT-FALSE-ACCEPT-COUNT` | 0 |
| `M-T-WIDENED-HTTP-ON-OUT` | **9** (frozen prediction 9) |
| `M-T-WIDENED-REFUSAL-EXECUTED-COUNT` | 0 |
| `M-T-WIDENED-FALSE-REJECT-COUNT` | 10 (all FAM-C) |
| `M-T-WIDENED-COVERAGE` | 0.8413 = 53/63 (frozen prediction 0.8413) |
| `M-B-SHIPPED-COVERAGE` | 0.5079 = 32/63 (frozen prediction 0.5079) |
| `M-COVERAGE-DELTA` | +0.3333 |
| `M-B-DECLARED-FULL-FALSE-ACCEPT-COUNT` | 0 |
| `M-B-DECLARED-FULL-COVERAGE` | 1.0 |
| `M-CONTROL-PC-COARSE-FALSE-ACCEPT-COUNT` | 153 (frozen prediction 153) |
| `M-CONTROL-PC-OVERWIDE-FALSE-ACCEPT-COUNT` | 33 (frozen prediction 33) |
| `M-CONTROL-NC-REJECT-ALL-ACCEPT-COUNT` / `-HTTP-TOTAL` | 0 / 0 |
| Validity anchors | V8 PASS, M-IDENTITY PASS, M-SUPPORT-IDENTITY PASS, M-REGRESSION 3/3, PC-DETERMINISM-REPEAT PASS, PC-EXACT-REPLAY 25/25, B-LITERAL-KERNEL PASS (no `distill_parameterized`) |

Per-family widening boundary (frozen `M-WIDENED-SUPPORT-BY-FAMILY`):
- FAM-A `^item\-[0-9]{3}$` — safe (FA=0) **and complete** (coverage 1.0).
- FAM-B `^acct\-[0-9]{4}$` — safe **and complete**.
- FAM-C `^doc\-[0-9]{2}$` — safe (FA=0, HTTP-on-OUT=0) but **incomplete** (coverage 9/19 = 0.4737): observed width 2 is a strict subset of the declared 1..4-digit grammar; the 10 false rejects are the width-1/width-4 IN ids (`doc-0`, `doc-1`, `doc-9`, `doc-100`, `doc-123`, `doc-999`, `doc-1000`, `doc-9999`, plus two the bank labels IN by declared grammar: `doc-0`, `doc-0000`).
- FAM-D `^region\-[0-9]{3}$` — **unsafe**: 9 false accepts (region-010..region-999), all executed, all 404. The shared run `region-00` is pinned by the declared grammar `^region\-00[0-9]$` but is observationally indistinguishable from a coincidental shared run; a purely data-driven rule cannot tell them apart. This is the frozen H4 identifiability limit, not a runner bug.

### INTERPRETATION
- H1 ("a principled widening rule attains coverage 1.0 with zero false accepts on all four families") is **falsified** by the FAM-D over-acceptance: `M-T-WIDENED-FALSE-ACCEPT-COUNT = 9 > 0` and `M-T-WIDENED-HTTP-ON-OUT = 9 > 0` on a verified carrier. All nine offences are exactly the frozen DESIGN-predicted bids `FD-OG-WRONGRANGE00..08`.
- H0 ("no such principled rule exists for all families") is **supported in the bounded sense**: for the pinned-subrange family the observed grammar does not uniquely identify a safe superset. The strong comparator `B-DECLARED-FULL` (FA=0, coverage=1.0) simultaneously proves the shortfall is an *information/identifiability* limit of purely data-driven inference, not a bank ceiling — a safe+complete support for this exact bank exists when the declared grammar is available.
- Product consequence (frozen `product_consequence_negative`): the purely data-driven homogeneous-run widening **must not be shipped**; the product ships conservative (the over-narrow shipped supports stay). The finding is the specification for a mandatory independent grammar/applicability guard (ingested declared grammar, or a pre-bind verification/repair step) before any shipped widening. No external agent may consume an auto-widened support on the basis of this packet.
- Product consequence (frozen `product_consequence_positive`) is NOT triggered: widening is not safe, so no licensing of a shipped widening; FAM-A/B's safe+complete result is bounded to uniform-width families and is a partial, not a product-level, positive.
- The frozen `WIDENING_SAFE_BUT_INCOMPLETE` branch was not selected because the decision function has precedence FALSIFIES over MIXED and FAM-D fired; its content is nonetheless realized for FAM-C as a per-family sub-result, which is exactly the information lost by the frozen precedence report: FAM-A and FAM-B demonstrate that the data-driven rule is safe and complete whenever the observed run is not pinned; FAM-C demonstrates the safe-but-incomplete (variable-width) case; FAM-D demonstrates the unsafe (pinned-run) case.

## 3. Decision-rule trace

Precedence `MEASUREMENT_INVALID > FALSIFIES > (SUPPORTS | MIXED)`:

1. Validity gate: ALL PASS (V8, M-IDENTITY, M-SUPPORT-IDENTITY, M-REGRESSION 3/3, PC-DETERMINISM-REPEAT, PC-EXACT-REPLAY 25/25, B-LITERAL-KERNEL).
2. Sensitivity gate: PASS (153 >= 1, 33 >= 1, null floor 0/0).
3. `M-T-WIDENED-FALSE-ACCEPT-COUNT = 9 > 0` → **FALSIFIES / WIDENING_UNSAFE** (runner sets `status=COMPLETE`, `outcome=FALSIFIES`, `decision=WIDENING_UNSAFE`).

This is a valid scientific negative: status COMPLETE means the certificate measured what it was frozen to measure; it is not an infrastructure or substrate failure.

## 4. Threats and boundaries (honest ceiling)

- The certificate's scope is the four frozen declared grammars on loopback 127.0.0.1 with a deterministic oracle; it says nothing about real heterogeneous Web identifier populations, auth/session variability, or stochastic services.
- Coverage/HTTP counts are the frozen definitions; `http_on_out_label` counts real 404 responses issued for OUT-labelled items the arm executed. No economy (cost per success, latency, amortization) was measured — the four-arm benchmark remains unfunded.
- FAM-A/B (uniform width, non-pinned) show safe+complete widening is achievable *data-driven*; but because FAM-D shows the same rule is not unconditionally safe, the packet's overall answer is the bounded negative, as frozen.
- The 19th FAM-C IN item bound by the treatment is `doc-00` (2-digit, declared-valid), explaining accept_count 9 vs my naive width-2 hand count of 8; all counts are the frozen runner's deterministic output, identical across two passes.

## 5. Files produced

- `result.json` — canonical producer handoff (required packet shape).
- `provenance.json` — reproduction provenance.
- `raw_run_output.json`, `raw_run_stderr.txt` — raw evidence.
- `harness/run_bank.py` — frozen runner materialization (V8-bound).