# EXP-RUNTIME-38244432934 — EXECUTE report (runtime, design_contract_version 2)

**Producer stage:** EXECUTE. **Frozen inputs are immutable; nothing in this packet was re-designed after outcomes were visible.**

| field | value |
| --- | --- |
| experiment_id | `EXP-RUNTIME-38244432934` |
| lane | `runtime` |
| target claim | `C-DELTA-REPAIR` (CONTINUE; parent disposition USE) |
| status | `COMPLETE` |
| outcome | `MIXED` |
| frozen decision (classifier) | `SUPPORTS-COUNTER-DEPENDENT` |
| per-class cost verdict | `STRICT-WIN-COUNTER-DEPENDENT` on `P1-ENDPOINT`, `P2-STRUCTURE`, `P3-PERMISSION` |
| runner self-sha256 | `d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608` (60855 bytes) |
| seed | `3884694566` (= origin_github_run_id `38244432934` mod 2**32) |
| raw result artifact | `raw_evidence/runner_result_raw.json` (`b2ac28d4e5e9528b2dbe9390518cc9075cfb262e06d10a9cca72c0330f8b996c`) |

The frozen classifier is the scientific answer. This report explains it; it does not exceed it.

## 1. Frozen-input integrity (audit F3/F5)

Frozen inputs were verified before execution and are unchanged:

- `request.json` = `c8ee0a20…`, `spec.json` = `bcdd3529…`, `prereg.md` = `1bd397fe…`,
  `design_review.json` = `78028002…`, all equal to `freeze.json.hashes`.
- carrier artifacts equal `freeze.json.artifact_hashes`: `src/spider/kernel.py` = `3a6caf97…`,
  `src/spider/models.py` = `338aaf4d…`, `src/spider/registry.py` = `51fb440d…`.
- the frozen runner was extracted from `prereg.md` section 12 by the literal marker split with the
  trailing newline preserved (audit F5 fix); the extracted file is 60855 bytes and hashes to
  `CANONICAL-RUNNER-SHA256 = d4871091…`.

## 2. What was run

Credential-free, stdlib-only, in-process `ThreadingHTTPServer` JSON API on `127.0.0.1` (ephemeral
port). No LLM, external network, browser, credential, proxy or datastore exists, so live fetches are
the scarce accounting resource. Carrier: shipped `distill_parameterized -> resolve -> execute ->
verify`. `TASK_IDS=[14,15,16,17,18]`, `LEARN_IDS=[11,12,13]` (disjoint; both in the carrier-inferred
support `^1[0-9]{1}$`), `IN_SUPPORT_PROBE_ID = 14` (the F1 fix replacing the out-of-support `id="1"`).
3 perturbation classes × 12 rotating targets = 36 trials. Arms: `T-REPAIR-REUSE` (treatment),
`T-REPAIR-CONSERVATIVE`, `T-REPAIR-LEGACY`, `B-COLD`/`B-COLD-MIN`/`B-COLD-DEEP`,
`B-LITERAL-REPLAY`, `B-NO-REPAIR`, plus `PC-BASE-LIVENESS` scored inside every trial and the three
`NC-*` controls.

Commands:

```
python3 raw_evidence/runner_delta_repair_reuse_v2.py --mechanics-only   # x2 (determinism canary)
python3 raw_evidence/runner_delta_repair_reuse_v2.py > raw_evidence/runner_result_raw.json
```

## 3. RAW EVIDENCE / direct observations

Raw evidence is `raw_evidence/runner_result_raw.json` (unmodified runner stdout) and the two canary
files. Direct observations only:

- runner exit 0; raw `status=COMPLETE`, `invalid_reasons=[]`; 36/36 trials `valid`.
- `repair_success` 36/36, `repair_guard_fired` 36/36, `cold_success` 36/36, `base_liveness` 36/36.
- `literal_replay_success` 0/36; `norepair_success` 0/36.
- integral equal-weight product counters, identical in every trial of a class:
  `T-REPAIR-REUSE = 17`, `B-COLD-MIN (L=2) = 18`, `B-COLD (L=3) = 19`,
  `B-COLD-DEEP (L=4) = 20`, `T-REPAIR-CONSERVATIVE = 18`, `T-REPAIR-LEGACY = 20`.
- same-target contamination: `M-CONTAMINATION-RATE = 0.0` (0/48 per class; 0/144 total), now a
  **live** measurement, not the parent's structural pin.
- over-broad rewrite: `overbroad_contamination_n = 4` in all 36 trials (all 4 unaffected probes
  broken); per-class `M-OVERBROAD-CONTAMINATION-RATE = 4.0`.
- `M-WRITE-SET-MAX = 1`; `write_set_n = 1` in all 36 trials.
- `NC-NO-PERTURBATION` and `NC-NOISE` both `stale=false` (jaccard 1.0).
- oplogs present in every trial; `M-OPLOG-REPAIR-LEN-MEAN = 17`, `M-OPLOG-LEGACY-LEN-MEAN = 19`.
- two `--mechanics-only` runs byte-identical.

## 4. DERIVED MEASUREMENTS (per class; raw values transcribed exactly)

| metric | P1-ENDPOINT | P2-STRUCTURE | P3-PERMISSION |
| --- | --- | --- | --- |
| `M-REPAIR-SUCCESS` | 1.0 | 1.0 | 1.0 |
| `M-REPAIR-SUCCESS-WILSON-LOWER` | 0.7574992425007574 | 0.7574992425007574 | 0.7574992425007574 |
| `M-GUARD-FIRE-RATE` | 1.0 | 1.0 | 1.0 |
| `M-CONTAMINATION-RATE` | 0.0 | 0.0 | 0.0 |
| `M-OVERBROAD-CONTAMINATION-RATE` | 4.0 | 4.0 | 4.0 |
| `M-WRITE-SET-MAX` | 1 | 1 | 1 |
| `M-PRODUCT-RATIO-REUSE-L2` | 0.9444444444444444 | 0.9444444444444444 | 0.9444444444444444 |
| `M-PRODUCT-RATIO-REUSE-L3` | 0.8947368421052632 | 0.8947368421052632 | 0.8947368421052632 |
| `M-PRODUCT-RATIO-REUSE-L4` | 0.85 | 0.85 | 0.85 |
| `M-COST-FETCH-RATIO-L3` | 0.6666666666666666 | 0.5555555555555556 | 0.6666666666666666 |
| `M-PRODUCT-RATIO-CONSERVATIVE-L2` | 1.0 | 1.0 | 1.0 |
| `M-PRODUCT-RATIO-CONSERVATIVE-L3` | 0.9473684210526315 | 0.9473684210526315 | 0.9473684210526315 |
| `M-PRODUCT-RATIO-LEGACY-L2` | 1.1111111111111112 | 1.1111111111111112 | 1.1111111111111112 |
| `M-PRODUCT-RATIO-LEGACY-L3` | 1.0526315789473684 | 1.0526315789473684 | 1.0526315789473684 |
| `M-WEIGHT-ROBUST-BOTH` | 0.7777777777777778 | 0.6666666666666666 | 0.7777777777777778 |
| `M-WEIGHT-CRITICAL-REPAIR-WEIGHT-L2` | 2.0 | 2.0 | 2.0 |
| `M-WEIGHT-CRITICAL-REPAIR-WEIGHT-L3` | 3.0 | 3.0 | 3.0 |
| classifier `cost_verdict` | STRICT-WIN-COUNTER-DEPENDENT | STRICT-WIN-COUNTER-DEPENDENT | STRICT-WIN-COUNTER-DEPENDENT |

Aggregate: `M-LEGACY-REGRESSION-REPRODUCED=true`, `M-TRIALS-TOTAL=36`,
`M-BASE-LIVENESS 36/36`, `M-CONTAMINATION-PROBES-TOTAL=144`,
`M-OVERBROAD-CONTAMINATION-RATE-MEAN=4.0`, `M-NOISE-FALSE-TRIGGER-RATE=0.0`,
`M-NO-PERTURBATION-FALSE-TRIGGER-RATE=0.0`.

The frozen classifier and an independent re-implementation of the same pure functions from the raw
metrics produce identical results (`SUPPORTS-COUNTER-DEPENDENT`).

## 5. Controls

All 12 frozen controls passed as expected; see `result.json.controls` for expected/observed/evidence
per stable id. In brief: `B-COLD` live (success 1.0, product 19 at L=3), `B-COLD-MIN` 18, `B-COLD-DEEP`
20, `B-LITERAL-REPLAY` 0.0, `B-NO-REPAIR` 0.0, `T-REPAIR-REUSE` product 17 with the strict ratios,
`T-REPAIR-CONSERVATIVE` exactly 1.00 at L=2, `T-REPAIR-LEGACY` regression reproduced (>1.00 at L=2),
`PC-BASE-LIVENESS` true 36/36, `NC-NO-PERTURBATION`/`NC-NOISE` not firing, and `NC-OVERBROAD-REPAIR`
detected (4/4 probes broken every trial). The parent's structurally-unable-to-fire over-broad control
is now sensitive.

## 6. Validity gates

V1–V15 all PASS; the exact gate dispositions are enumerated in `result.json.validity_notes`. The
critical fixes relative to the parent are: V1 (trailing-newline extraction, audit F5), V12
(in-scored-trial positive control, audit F4) and V15 (live contamination instrument, audit F1/F2).
Metric-shape caveat recorded: `M-OVERBROAD-CONTAMINATION-RATE` is a mean count out of 4 probes
(0–4), not a 0–1 fraction, despite the name; the value 4.0 is unambiguously above the 0.10 bar.

## 7. Interpretation (bounded to the frozen scope)

1. **The strict equal-weight cost win reproduces.** Under the preregistered reuse accounting,
   `T-REPAIR-REUSE` costs 17 equal-weight product units versus cold re-derivation 18 (L=2) / 19
   (L=3) / 20 (L=4), i.e. ratios `0.9444` / `0.8947` / `0.85`, with L=3 fetch ratio `0.6667`
   (`P1`/`P3`) and `0.5556` (`P2`). This is the mandate's strict-inequality condition and it holds
   on every class.
2. **The contamination half is now measured, not vacuous.** Same-target contamination is 0.0 with a
   live in-support probe, and the deliberately over-broad rewrite is detected at 4/4 probes in every
   trial. The parent's H2 locality assertion is therefore now supported on this substrate; the
   F1 degenerate-helper defect is corrected.
3. **The strict win is counter-dependent, so the mandate's second conjunct fails.** On the
   predeclared `{1,2,3}^4` grid, repair beats cold at **both** L=2 and L=3 on only `0.7778` / `0.6667` /
   `0.7778` of the counter weightings for `P1` / `P2` / `P3` — below the preregistered `ROBUST` bar of
   `1.0`. Some permitted monotone reweighting reverses the sign. `critical_repair_weight` is `2.0`
   (L=2) and `3.0` (L=3): the win tolerates the one repair attempt being weighted up to ~2–3× a
   single fetch/retrieval/verify, but not arbitrarily. The conservative re-resolve bound is
   `0.947` at L=3 (`1.00` at L=2), which by itself does not reverse the sign; the reversal is driven
   by the weight grid.
4. **The replication premise holds.** `T-REPAIR-LEGACY` still reproduces the prior ~5.3% regression
   (`1.1111` at L=2, `1.0526` at L=3), so the difference between arms is attributable to the repair
   system's accounting, not to the substrate or baseline.
5. Therefore, exactly as the frozen falsifier specifies, the result is `COUNTER-DEPENDENT`: the strict
   win exists under the registered equal-weight counter but is not sign-invariant under permitted
   reweightings. The correct reading of the equal-weight strict win is **real but counter-contingent**,
   not a robust product-counter advantage.

This is a valid `COMPLETE`/`MIXED` scientific result. It is not a measurement failure and not a
falsification of the functional repair mechanism.

## 8. Product consequence (per frozen spec, not a promotion)

Per `spec.product_consequence_negative`, the `SUPPORTS-COUNTER-DEPENDENT` branch means the win is
counter-dependent; localized repair must **not** be treated as robustly product-counter-cheaper, and
the ~5.3% product-counter regression should be treated as effectively intrinsic/accounting-dependent
for the product story. This packet does not promote or demote `C-DELTA-REPAIR` (it remains
`EXPERIMENTAL`); any advance, adoption into the product story, or flagship `C-PRODUCT-ECON` funding is
a DIRECTOR adjudication after independent audit.

## 9. Unresolved

See `result.json.unresolved`: transfer to real Web tasks / production carrier / external agents is
not measured; whether the registered equal-weight counter is the product-correct counter is not
settled (the result is counter-dependent by construction); `T-REPAIR-LEGACY` is a product-counter
reconstruction, not an independently known operation sequence; and the structural reason the P2
weight-robust fraction (0.6667) is lower than P1/P3 (0.7778) is the P2 reuse vector shape
`(5,5,6,1)` versus `(6,5,5,1)` on the predeclared grid.
