# EXP-GRAPH-38197849043 — EXECUTE report

| identity | value |
| --- | --- |
| experiment_id | `EXP-GRAPH-38197849043` |
| lane | `graph` |
| design_contract_version | `2` |
| target claim | `C-DELTA-REPAIR` |
| status | `COMPLETE` |
| outcome | `MIXED` |
| frozen decision | `MIXED-TRADEOFF` |
| runner self-sha256 | `0322d92cfbc1314437a92eb0cdfeac43a8ecd3c5cdd520bae0a443c8d669eed1` |
| raw result | `raw_evidence/runner_result_raw.json` (`00c805de25116807f729e944a437bb2ec88a58bfd0e4c01d2ad87f79085537e4`) |

This report interprets the frozen measurements. It does not exceed the frozen claim or
silently contradict `result.json`.

## 1. What was run

The frozen `FROZEN-RUNNER` block was extracted verbatim from `prereg.md` and verified
against `CANONICAL-RUNNER-SHA256` before execution. It was run once as the scored
confirmatory transaction: 36 trials (12 per perturbation class `P1-ENDPOINT`,
`P2-STRUCTURE`, `P3-PERMISSION`, targets rotating over `users`/`posts`/`comments`),
using the shipped parameterized carrier (`src/spider/kernel.py`:
`distill_parameterized -> resolve -> execute -> verify`, plus `rebind`) on a
credential-free in-process stdlib `ThreadingHTTPServer`. No LLM, network, credential or
browser was involved. The `--mechanics-only` canary was run twice and was byte-identical.

## 2. Measurement-validity gates (all PASS; `invalid_reasons=[]`)

V1 freeze binding, V2 substrate isolation, V3 determinism, V4 perturbation bites,
V5 cold baseline live, V6 no-repair inert, V7 guard liveness, V8 no target leakage,
V9 integer counters, V10 thresholds not fitted, V11 n=12 per class, V12 positive control.
Evidence: `result.json.validity_notes` and `raw_evidence/runner_result_raw.json`.

## 3. Results by hypothesis

**H1 (functional) — supported.** Local repair restored end-to-end success on 12/12 trials
in every class (`M-REPAIR-SUCCESS=1.0`; Wilson 95% lower `0.7575 >= 0.60`), and the
deterministic guard fired on 12/12 perturbed trials (`M-GUARD-FIRE-RATE=1.0`).

**H2 (locality) — supported.** The write set was exactly one mechanism in all 36 trials
(`M-WRITE-SET-MAX=1`, mean 1.0). Behavioural contamination of the four unaffected
resources was `0/48` (`M-CONTAMINATION-RATE=0.0`). The deliberately over-broad control
`NC-OVERBROAD-REPAIR` was detected as contaminated (`M-OVERBROAD-CONTAMINATION-RATE=4.0`).
`NC-NO-PERTURBATION` and `NC-NOISE` both stayed fresh (`stale=false`). `B-LITERAL-REPLAY`
and `B-NO-REPAIR` failed in every class, so the perturbation genuinely bites, while
`B-COLD` succeeded 12/12.

**H3 (cost) — falsified as a strict win; network-cheaper but product-counter regression.**
Per class the repair cost ratio vs cold re-derivation (L=3) was:

| class | product counter ratio | fetch ratio | verdict |
| --- | --- | --- | --- |
| `P1-ENDPOINT` | 1.05263 | 0.77778 | `MIXED-TRADEOFF` |
| `P2-STRUCTURE` | 1.05263 | 0.66667 | `MIXED-TRADEOFF` |
| `P3-PERMISSION` | 1.05263 | 0.77778 | `MIXED-TRADEOFF` |

The repair uses fewer live fetches (mean 7/6/7 vs 9 for cold) but the registered product
counter (equal-weight `{http_requests, retrieval_calls, verification_calls,
repair_attempts}`) is ~5.3% higher because the repair pays one `repair_attempt` plus its
probe fetch and additional retrieval/verification work. The product ratio is stable across
cold budgets and always `>= 1.0` (L=2 -> 1.1111, L=3 -> 1.05263, L=4 -> 1.0). There is no
cold budget at which the repair is strictly cheaper on the product counter.

## 4. Frozen aggregate decision

All three classes are `MIXED-TRADEOFF`, therefore the frozen aggregate rule yields
`decision = MIXED-TRADEOFF`, `status = COMPLETE`, `outcome = MIXED` (network-cheaper but
not product-counter-cheaper).

## 5. Interpretation (bounded)

At this single credential-free-substrate ceiling, a deterministic freshness guard plus a
signal-driven local repair of the shipped parameterized carrier is **functional and local**:
it restores success, touches exactly one mechanism, and does not contaminate unaffected
resources. It is **not** strictly cheaper than cold re-derivation on the mandate's
registered product counter; the win exists only on live network fetches. Per the frozen
negative consequence, this is a `MIXED-TRADEOFF`: local repair is not promoted, and
`C-DELTA-REPAIR` is bounded to a network-cost-only maintenance benefit at this scope.

This does **not**:
- validate local repair on the live Web (the substrate is a local stdlib HTTP app);
- establish a strict product-economics win;
- establish cross-site or structural generality.

## 6. Raw-vs-derived separation

All numbers above are derived from `raw_evidence/runner_result_raw.json`. Interpretive
statements are confined to this section and `result.json.observations` presents only direct
observations. The `NC-OVERBROAD-REPAIR` prediction miss (it contaminated all classes, not
only `P2-STRUCTURE`) is recorded as an observation and a validity note; it did not affect
the decision.
