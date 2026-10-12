# EXP-PRODUCT-38186502935 — report

**Lane:** product · **Claim:** C-PARAM-INHERIT (registry status EXPERIMENTAL in all branches) ·
**Status:** `COMPLETE` · **Outcome:** `SUPPORTS` · **Primary metric:** `M-E2E-PASS = true`

Shipped-carrier end-to-end execution readiness demonstration (readiness condition (1)),
per the binding Director mandate in `request.json#director_mandate.allocation.question`.
This is a READ-ONLY measurement of the as-installed shipping kernel through the public package
API. The runner never wrote `src/spider/`.

## 1. What was asked

Does the now-promoted, byte-identical shipped parameterized carrier (git blob
`b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` / sha256 `718efa6a...`, with a frozen D0–D4+V8
certificate PASS and an independent PASS audit) actually execute the full shipped path
`distill_parameterized -> resolve -> execute -> verify/UNKNOWN` on a credential-free substrate,
producing BOTH one known-positive on a never-observed identifier AND one known-negative refusal
(abstention) at shipped thresholds — thereby discharging readiness condition (1)?

## 2. What was measured

The exact frozen runner (materialized verbatim from `prereg.md` §14) was executed in EXECUTE mode
with **no** `EXP_*` overrides, shipped `min_confidence=0.8`, against a stdlib loopback fixture on
`127.0.0.1:0`. Raw evidence: `run_e2e.out.json` (stdout) and `run_e2e.log` (stderr; unittest
banner only). A second identical run (`run_e2e.repeat.out.json`) checked determinism.

### Identity (E2E-IDENTITY)
`src/spider/kernel.py` sha256 = `718efa6a…` = recomputed sha256 of git blob `b15ed848…`. The
promotion merge is in effect and the measured bytes are the frozen carrier. No tracked `src/`,
`tests/` or `pyproject.toml` file was modified; the only dirty tracked files are the canonical
Codex sync metadata (`SPIDER_CODEX.md`, `codex/claim_state.json`, `codex/index.json`), which are
outside Product scope and not measured (see validity note GIT-TREE CAVEAT).

### Positive (E2E-POSITIVE) — PASS
Five induction GETs (`item-001..item-005`, each fixture 200) produced mechanism
`mech-1cfc19af1d03f157` with slots `['item']`, support `^item\-00[0-9]{1}$`, confidence `0.9`.
The **never-observed** identifier `item-000` (0 occurrences in a repo-wide sweep of all prior
artifacts — V5) resolved `EXECUTABLE` at confidence `0.9` with bound action
`GET http://127.0.0.1:<port>/api/items/item-000`; executing it returned fixture status `200`;
`verify(...) == true`.

### Abstention (E2E-ABSTENTION) — PASS
All 7 refusal probes returned `bound_action = null`, a non-empty reason, and status ≠ `EXECUTABLE`:
`item-010` (designated known-negative), `item-999`, `item-xyz` → `EXPLORE` "parameter 'item'
outside inferred support"; `{}` and `{'wrong_key':'x'}` → `EXPLORE` "missing required parameter
'item'"; `delete_item` → exactly `UNKNOWN`; `never_seen_intent` → exactly `UNKNOWN`. The
runner-side fixture request counter delta across the whole abstention phase was **0** — a refusal
issued no HTTP.

### Counters (E2E-COUNTERS) — PASS
`retrieval_calls=9`, `verification_calls=1`, `repair_attempts=1` — exactly the invocation
transcript (`retrieval == #resolve + #rebind`, `verification == #verify`, `repair == #rebind`);
`model_calls=0`, `model_tokens=0`. Runner-side HTTP total = **6** (5 induction + 1 positive
execute), matching `http_expected_legs=6`; abstention phase contributed 0.

### Controls (E2E-CONTROLS) — PASS
`B-LITERAL-KERNEL` (pre-promotion literal blob `cfec9866…`) has no `distill_parameterized`, so
the positive is attributable to the installed carrier only. `PC-EXACT-REPLAY` = 5/5 `EXECUTABLE`.
Regression suite `tests/test_kernel.py` = 3 tests, 0 failures, 0 errors.

### Binding (V8) — PASS
`freeze.json` present; prereg sha matched; running source == FROZEN RUNNER block; all six freeze
artifact hashes matched — including `src/spider/kernel.py`, frozen here because this experiment
never mutates it. All six re-hashed unchanged after both runs.

## 3. Interpretation (bounded)

On the current shipping tree, the installed carrier executes the full shipped end-to-end path
`distill_parameterized -> resolve -> execute -> verify/UNKNOWN` at shipped thresholds, with a
known positive on a genuinely never-observed identifier and a zero-HTTP known-negative refusal.
**Readiness condition (1) is discharged.**

This is NOT a claim advance and NOT a promotion. `C-PARAM-INHERIT` remains `EXPERIMENTAL`. The
four-arm C-LLM-INHERIT benchmark was not run (readiness (2)/(3) unmet; policy forbids funding),
COLD/INSTRUCTIONS/RETRIEVAL arms were not compared, the promotion certificate and the
mandatory-discovery REST certificate were not re-run, and no economics/wall-clock claim is made
(`model_calls = model_tokens = 0`, `latency_ms = 0`).

## 4. Consequences

- **Positive branch (observed):** readiness condition (1) discharged. The flagship four-arm
  benchmark's treatment arm is real and instrumentable. The lane waits on readiness (2) (Intel:
  budget-stable credential-free endpoint), readiness (3) (Runtime: certified asymmetric-discovery
  task bank), and a NEW Global Research Director mandate before any benchmark spend.
- **Negative branch (not observed):** would have recorded the exact failing clause as an
  engineering-fix specification inside Product, leaving readiness (1) open.
- **BLOCKED/MEASUREMENT_INVALID branch (not observed):** none of the identity/binding/
  infrastructure failures fired.

## 5. Validity threats and caveats

- **Scope/representation loss:** the fixture is a minimal deterministic GET/JSON loopback server
  over a single resource shape; correctness/refusal is established only for the induced
  single-digit-suffix support grammar, not for free-form payload values.
- **`mechanism_id` is not cross-run stable:** it is `mech-` + sha256({intent, template, slots}),
  where `template` embeds the action URL (ephemeral loopback port). The two runs produced
  different `mechanism_id`s and port-bearing URLs while every decision-relevant status, counter
  and control was identical. Refer to the mechanism by its induced support/slots/confidence.
- **Global git tree not clean** only for canonical Codex sync metadata; the measured shipping
  path and all freeze artifacts are byte-clean. The frozen runner implements the identity clause
  as the carrier-sha check, not a global git-clean check; disclosed rather than hidden.
- **Kernel `http_requests=0` by construction** (`TrajectoryCounters` does not auto-increment it);
  the gated counter is the runner-side fixture counter, per the prereg.

Raw evidence, observations, derived measurements and interpretation are kept distinct:
`run_e2e.out.json` is the raw artifact; `result.json` holds derived metrics/controls; this report
is interpretation. No frozen input was modified after freeze.
