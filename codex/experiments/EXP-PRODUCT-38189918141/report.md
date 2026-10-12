# EXP-PRODUCT-38189918141 — EXECUTE report

**Lane:** product | **Contract:** design_contract_version 2 (frozen) | **Status:** COMPLETE
**Outcome:** `MIXED` | **Decision:** `SAFE_BUT_CONSERVATIVE`
**Primary claim:** `C-PARAM-INHERIT` (retained EXPERIMENTAL) — **Secondary:** `C-SEMANTIC-RESOLVE` (retained HYPOTHESIS)
**Frozen treatment:** shipped carrier `src/spider/kernel.py`, git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`.

This report explains `result.json`; it does not exceed the frozen claim and does not silently
contradict the JSON. No claim is advanced or promoted in any branch.

## 1. What was executed

The FROZEN RUNNER block was extracted verbatim from the hash-bound `prereg.md` into
`harness/run_bank.py` and executed with **no env overrides** in EXECUTE mode, twice as independent
processes. It evaluates the byte-identical installed carrier over the frozen 78-item bank using an
in-process `http.server` oracle on `127.0.0.1:0`. Raw evidence: `run_bank.out.json`,
`run_bank.repeat.out.json`, `run_bank.log`, `run_bank.repeat.log`.

## 2. Validity and sensitivity gates (all PASS)

| Gate | Observed |
| --- | --- |
| `V8_FREEZE_BINDING` | PASS — prereg sha, runner==frozen block, six artifact hashes |
| `M-IDENTITY` | PASS — shipping kernel sha `718efa6a…` == frozen carrier |
| `M-REGRESSION` | PASS — 3 tests, 0 failures, 0 errors |
| `PC-EXACT-REPLAY` | PASS — 5/5 training ids EXECUTABLE |
| `B-LITERAL-KERNEL` | PASS — literal kernel lacks `distill_parameterized` |
| `PC-DETERMINISM-REPEAT` | PASS — internal two-run identity (port-invariant) |
| `PC-UNSAFE-COARSE` | PASS — 38 false accepts (>= 1 required; detector non-vacuous) |
| `NC-REJECT-ALL` | PASS — 0 accepts, 0 HTTP |

In addition, the primary and the independent repeat **external process runs produced byte-identical
stdout JSON** (sha256 `7c8e9001…`), i.e. determinism held beyond the runner's own internal repeat.

## 3. Primary measurement (T-SHIPPED)

Bank: 78 unique bids, 19 IN / 59 OUT, 0 class/label mismatches.

- `M-FALSE-ACCEPT-COUNT = 0` (rate 0/59 = 0.0)
- `M-SILENT-FALSE-ACCEPT-COUNT = 0`
- `M-REFUSAL-ZERO-HTTP = 0` HTTP requests on the 59 out-of-grammar payloads (`http_total = 10`,
  all on the 10 accepted in-grammar items)
- `M-FALSE-REJECT-COUNT = 9`; `M-COVERAGE = 10/19 = 0.5263`
- `M-BOUNDARY`: induced support `^item\-00[0-9]{1}$`, slots `['item']`, confidence `0.9` (>= shipped
  default `min_confidence 0.8`). The **accepted** in-grammar set is exactly
  `{item-000 … item-009}`; the **refused** declared 3-digit ids are
  `{item-010, item-011, item-042, item-099, item-100, item-123, item-256, item-500, item-999}`.
- Refusal semantics: all 59 refusals have `bound_action=null`, a non-empty reason,
  `status != EXECUTABLE`, and 0 HTTP. The 7 context/intent/param-mismatch routes returned exactly
  `UNKNOWN` (5: wrong resource type, unauthenticated, missing auth, empty context, wrong intent) or
  `EXPLORE` missing-parameter (2: wrong param key, empty params).

All three non-string/context/intent payload classes (10 non-string types, whitespace, separator `/`,
injection strings) were refused, so the conservative single-pattern support binds **only** the
cylinder `{item-000..item-009}`.

## 4. Controls / comparators

- `PC-UNSAFE-COARSE` (carrier's own `__COARSE__` fallback): **38** false accepts on the OUT set,
  35 of which issued an HTTP request (404). The safety oracle is demonstrably sensitive.
- `NC-REJECT-ALL` (empty registry): **0** accepts, **0** HTTP — null floor holds.
- `B-WIDENED-3` (support `^item\-[0-9]{3}$`): **0** false accepts, **coverage 1.0** (19/19 IN accepted,
  0/59 OUT accepted). A safe, complete alternative to the over-narrow support therefore exists on
  this bank.
- `B-LITERAL-KERNEL`: structurally lacks `distill_parameterized`, so the positive is attributable to
  the installed carrier.

## 5. Decision mapping (frozen rule)

`M-FALSE-ACCEPT-COUNT == 0` and `M-REFUSAL-ZERO-HTTP == 0` but `M-FALSE-REJECT-COUNT > 0` maps to
**`MIXED` / `SAFE_BUT_CONSERVATIVE`** (precedence: `MEASUREMENT_INVALID > FALSIFIES > (SUPPORTS vs MIXED)`).
No fake negatives: the carrier's refusal of declared-but-out-of-support ids is an over-conservative
coverage limitation, **not** a safety defect.

## 6. Interpretation (bounded)

The shipped UNKNOWN-preferring path is **safe to expose to external agents on this materially
varied / out-of-grammar bank**: nothing out-of-grammar binds and out-of-grammar payloads issue zero
HTTP. Its boundary is **over-conservative**: the single-observation-length support learned from
`item-001..005` refuses 9 of 19 legitimate declared 3-digit ids. `B-WIDENED-3` shows the limitation
is **avoidable** with a safe complete widening. That widening is a candidate remediation for the
Director/Product to weigh; this packet does not authorize it.

No economics were measured (`model_calls=0`, `model_tokens=0`, `browser_actions=0`), and the four-arm
`C-LLM-INHERIT` benchmark remains externally gated. `C-PARAM-INHERIT` stays EXPERIMENTAL and
`C-SEMANTIC-RESOLVE` stays HYPOTHESIS.

## 7. Reproduce

```
python3 research/experiments/EXP-PRODUCT-38189918141/harness/run_bank.py        # EXECUTE mode, no env overrides
```

The runner is read-only: it never writes `src/spider/` or any freeze artifact. Post-run re-hash of
all six freeze artifacts matched `freeze.json.artifact_hashes`.
