# EXP-PRODUCT-38234098353 — EXECUTE report

Lane: **product** · design_contract_version: **2** · parent: EXP-PRODUCT-38210179652 · claim: **C-PARAM-INHERIT** (RETAINED at EXPERIMENTAL in every branch).

This is a **MEASUREMENT-ONLY** extension. It modifies no source code
(`src/spider/kernel.py` is byte-identical, sha256
`3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3`), re-runs no
parent certificate and substitutes no carrier. It executes the frozen design
exactly.

## 1. What was run

The FROZEN RUNNER block in `prereg.md` was materialized verbatim to
`raw_evidence/run_scored_adeq.py` (raw-byte sha256
`26e9fef024309d9c8ef20373786a78d7fc57a6688e8c32adec8843a63a678d47`, equal to the
declared value) and executed with the exact frozen command:

```
EXP_PROBE_MODE=1 PYTHONPATH=src SPIDER_SRC=src \
  EXP_PACKET_DIR=research/experiments/EXP-PRODUCT-38234098353 \
  python3 research/experiments/EXP-PRODUCT-38234098353/raw_evidence/run_scored_adeq.py
```

The runner is deterministic, stdlib-only, credential-free, and uses one
loopback HTTP oracle. It performs two independent `run_once` executions
internally; the command was additionally invoked twice as two independent
processes. Both full stdout captures are **byte-identical** (sha256
`d120d78556d5a4f8d4fa5349e7ed37c4f2dfc4668162ba4974492f9cb63140f5`), and the
in-process determinism flag is `True`.

V8_FREEZE_BINDING ran in **BOUND** mode: `prereg.md` sha256 matches
`freeze.json.hashes`, the running runner is normalized-identical to the frozen
block, and all six `freeze_artifacts` re-hash identically after the run.

## 2. Instrument validity and gates

All seven frozen gates **PASS**:

| gate | result |
| --- | --- |
| validity_gate | PASS |
| sensitivity_gate | PASS |
| provenance_gate | PASS |
| adequacy_gate | PASS |
| growth_gate | PASS |
| necessity_gate | PASS |
| boundary_gate | PASS |

Validity anchors: `M-MECHANISM-COUNT=11`, `M-SINGLE-SLOT=True`,
`M-CONFIDENCE-0.9=True`, `M-SUPPORT-IDENTITY=True` (all eleven induced supports
equal the frozen `EXPECTED_INDUCED`), `M-SPARSE-TOKENS-MISSED=True`,
`B-SHIPPED-FA0=True`, `B-ORACLE-CEILING=True`, `T-REFUSAL-VIOL-0=True`,
`M-ADEQ-DETERMINISTIC=True`, regression `tests_run=3`, `failures/errors=0`.

All **20** gated controls PASS (see `result.json#controls`), including the null
control `NC-REJECT-ALL`, the boundary probe `BP-TRUSTED-SPARSE-FAILS`, the
safety oracle `PC-UNSAFE-RAW` (FA=18), the discrimination/over-trust controls,
refusal semantics, and `PC-DETERMINISM-REPEAT`.

## 3. Result

`status=COMPLETE`, `outcome=SUPPORTS`,
`decision=SCORED_ADEQ_CERT_SAFE_AND_EXPANSIVE`.

### Measured provenance (M-PROV)

The trust root is **measured**, not declared. Execution-grounded certificate
agreement over the frozen 4-entry per-origin ledgers gives

```
M-REG-PROV-SCORES = {O1:1.0, O2:1.0, O3:1.0, O4:1.0, O5:0.25, O6:0.25}
M-INFERRED-ALLOWLIST = [O1, O2, O3, O4]      (tau = 0.5)
```

recovering exactly the trusted set with no operator-declared allowlist.

### Syntactic probe-adequacy detection (M-ADEQ)

`M-ADEQUACY-CLASSIFIED = {B7:false, B8:false, all others true}`. B7/B8 carry an
out-of-`PROBE_ALPHA` `[A-Z]` alternative and are flagged INADEQUATE and withheld;
no other declaration is spuriously withheld.

### Treatment vs baselines/ablations (within-envelope B1–B10, equal coverage 1.0)

| arm | role | FA | HTTP-on-OUT | refusal-viol |
| --- | --- | --- | --- | --- |
| **T-SCORED-ADEQ** | measured trust + adequacy + growth | **0** | **0** | **0** |
| A-NO-ADEQ | adequacy ablation | 6 | 6 | 0 |
| A-NO-PROV | provenance ablation | 3 | 3 | 0 |
| A-NO-GROW | growth ablation | 9 | 9 | 0 |
| C-FIAT-ADEQ | fiat allowlist + growth, no adequacy | 6 | 6 | 0 |
| C-FIAT-OVERTRUST | fiat allowlist over-trusting O5 | 3 | 3 | 0 |
| C-FROZEN-CERT | frozen-certificate incumbent | 18 | 18 | 0 |
| A-RAW-DECL | unconditional adoption | 18 | 18 | 0 |
| B-SHIPPED | conservative floor | 0 | 0 | 0 |
| A-WITHHOLD-ALL | null floor | 0 | 0 | 0 |
| B-ORACLE | true-grammar ceiling | 0 | 0 | 0 |

- **Safety:** `M-T-FALSE-ACCEPT-COUNT=0`, `M-T-HTTP-ON-OUT-COUNT=0`,
  `M-T-REFUSAL-SEMANTICS-VIOLATIONS=0`.
- **Expansion:** `M-T-COVERAGE=1.0` (44/44) vs
  `M-B-SHIPPED-COVERAGE=0.4545` (20/44), `M-T-COVERAGE-DELTA-VS-SHIPPED=+0.5455`,
  clearing the `0.6750` anchor.
- **Dominance:** T strictly dominates C-FIAT-ADEQ (FA 0 vs 6) and the
  frozen-certificate incumbent (FA 0 vs 18) at equal coverage, and is robust to
  a fiat allowlist that over-trusts O5 (C-FIAT-OVERTRUST FA=3 vs T FA=0).
- **Necessity:** each of the three mechanisms is necessary — adequacy
  (A-NO-ADEQ FA=6), measured provenance (A-NO-PROV FA=3), growth
  (A-NO-GROW FA=9).
- **Refusal semantics:** `PC-INGEST-REFUSED-ABSTAINS` PASS — the real
  `SpiderKernel.ingest_declaration` on B5 records `REFUSED` and leaves the slot
  support unchanged.

### Residual boundary (still conditional)

B11 (trusted origin O4, within-alphabet/within-length/budget-sparse literal
over-accept) is CERTIFIED by the certificate-with-growth and **false-accepts**
(`M-T-BOUNDARY-FALSE-ACCEPT-COUNT=3`; `PC-GROW-MISSES-SPARSE` and
`BP-TRUSTED-SPARSE-FAILS` both PASS). The zero-false-accept result is therefore
**within-envelope by frozen construction** and conditional on inferred
provenance AND on probe reachability — it is not a general soundness claim.

## 4. Interpretation (bounded)

On this synthetic eleven-family expansion bank, measured provenance plus a
syntactic probe-adequacy detector safely renews the declaration certificate:
it infers the trust root from execution-grounded history instead of a declared
list, detects the out-of-alphabet probe inadequacy instead of assuming probe
adequacy, holds zero false accepts at coverage 1.0 over B1–B10, and strictly
dominates both the fiat/no-adequacy and frozen-certificate incumbents. The
irreducible within-envelope budget-sparsity residual (B11) and the endogeneity
of the scorer (spec `V13`) remain. **C-PARAM-INHERIT is retained at
EXPERIMENTAL; no code is promoted and no product change is authorized.**

## 5. Validity threats and bounds

- Loopback-only, synthetic bank/ledgers/detector, fixed seeded probe space
  (seed `38234098`, `PROBE_BUDGET=256`); no external network, no model calls,
  no tokens (spec `V1`, `V10`).
- The provenance score is endogenous to the shipped certificate and here the
  inferred allowlist coincides with the correct declared set; the demonstrated
  value of measuring is robustness to an over-permissive fiat allowlist, not
  superiority over a correct one (spec `V13`).
- The adequacy detector is conservative: it would withhold a sound declaration
  whose true alphabet legitimately exceeds `PROBE_ALPHA` (coverage cost, not a
  safety hole; spec `V11`), and that cost was not measured here.
- The residual boundary B11 is reachable and fires; the guarantee is
  conditional, not general.
- No end-to-end external-agent or product-economics measurement was performed.

See `result.json` for the canonical machine handoff and `provenance.json` for
reproduction context.
