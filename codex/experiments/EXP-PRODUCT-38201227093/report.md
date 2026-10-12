# EXECUTE report — EXP-PRODUCT-38201227093

- Lane: `product`
- Claim target (binding Director mandate): `C-PARAM-INHERIT`
- Dependency claims: `C-MEAS-VALID`, `C-SEMANTIC-RESOLVE`
- `design_contract_version`: 2
- Status: **COMPLETE** · Outcome: **SUPPORTS**
- Decision: `DECLARED_GUARD_SAFE_AND_COMPLETE__OBSERVATIONAL_GUARD_UNSAFE`
- Canonical machine handoff: `result.json`, `provenance.json`; raw evidence in `raw_evidence/`.
- This report explains the packet; it does not exceed the frozen claim and does not advance any claim.

## 1. What was run

The frozen runner (`harness/run_guard.py`, materialized byte-for-byte from the FROZEN
RUNNER block in `prereg.md`) measured, on the byte-identical shipped parameterized carrier
(`src/spider/kernel.py` sha256 `718efa6a...` == git blob `b15ed848...`), whether a
**not-purely-data-driven applicability guard** can hold zero false accepts / zero
out-of-grammar HTTP / zero refusal-semantics violations while raising SAFE coverage on an
extended seven-family bank:

- `T-DECLARED-GUARD` (PRIMARY) — ingested declared grammar adopted only after a
  training-consistency check, else fall back to the shipped support.
- `T-AMBIGUITY-GUARD` (SECONDARY, discriminating) — purely observational pre-bind refusal of
  a widening whose absorbed common-prefix run shares the remainder's class and whose observed
  terminal remainder saturates that class.

Bank: 524 unique-bid items, 120 IN / 404 OUT; per-family in/out A 16/56, B 18/55, C 19/53,
D 10/65 (pinned subrange `region-00[0-9]`), E 16/55, F 12/61 (`case-z[a-z]{2}`, non-digit,
not observably pinned), G 29/59 (`token-ab[a-z]`, saturating alpha). Oracle: stdlib
`ThreadingHTTPServer` on `127.0.0.1:0`, 200 iff the path fullmatches the declared grammar,
else 404. The whole evaluation ran twice (`PC-DETERMINISM-REPEAT`).

## 2. Primary result — declared-grammar guard is safe and complete

`T-DECLARED-GUARD` (primary decision metric `M-DECLARED-GUARD-FALSE-ACCEPT-COUNT`):

| metric | value |
|---|---|
| `M-DECLARED-GUARD-FALSE-ACCEPT-COUNT` | **0** |
| `M-DECLARED-GUARD-HTTP-ON-OUT` | **0** |
| `M-DECLARED-GUARD-REFUSAL-EXECUTED-COUNT` | **0** |
| `M-DECLARED-GUARD-SILENT-FALSE-ACCEPT-COUNT` | 0 |
| `M-DECLARED-GUARD-FALSE-REJECT-COUNT` | 0 |
| `M-DECLARED-GUARD-COVERAGE` | **1.0 (120/120)** |
| adopted (7 families) | all `True` |

Per-family coverage is 1.0 for A, B, C, D, E, F, G. This is **safe+complete on every
family**, including the pinned FAM-D subrange that broke the pure data-driven rule and the
non-pinned FAM-F / FAM-G. Coverage rose from the shipped `0.6750` (81/120) to `1.0`
(`M-COVERAGE-DELTA = +0.325`).

## 3. Secondary result — purely observational guard is UNSAFE (bounded negative)

`T-AMBIGUITY-GUARD`:

| metric | value |
|---|---|
| `M-OBSERVATIONAL-GUARD-FALSE-ACCEPT-COUNT` | **4** |
| `M-OBSERVATIONAL-GUARD-HTTP-ON-OUT` | 4 |
| `M-OBSERVATIONAL-GUARD-REFUSAL-EXECUTED-COUNT` | 0 |
| `M-OBSERVATIONAL-GUARD-FALSE-REJECT-COUNT` | 10 |
| `M-OBSERVATIONAL-GUARD-COVERAGE` | 0.9167 (110/120) |
| refused families | D, G |
| disposition | **UNSAFE** |

The four false accepts are all FAM-F: `FF-OG-ALPHA-ALL` (`case-abc`),
`FF-OG-WRONGRANGE00/01/02` (`case-aab`, `case-bcd`, `case-xyz`). The widened
`^case\-[a-z]{3}$` absorbs the non-saturating alpha shared run `z` because the observed
terminals (`case-zab..case-zij`) never saturate the class, so the refusal condition never
fires. This exactly reproduces the frozen DESIGN point-prediction and shows the purely
observational route is a **general identifiability limit** (digit or alpha shared runs), not
a FAM-D artifact. This is a bounded negative about the observational mechanism class, a
mandatory co-report, **not** the packet falsifier and **not** a claim advance.

## 4. Baselines and controls

| arm | `false_accept_count` | coverage | false rejects | http-on-out | reading |
|---|---|---|---|---|---|
| `B-SHIPPED` | 0 | 0.6750 (81/120) | 39 | 0 | safe but over-conservative |
| `B-DECLARED-FULL` (ceiling) | 0 | 1.0000 (120/120) | 0 | 0 | safe+complete support exists |
| `B-DATA-WIDENED` (parent) | 18 | 0.9167 | 10 | 18 | D 9 + F 4 + G 5 |
| `T-DECLARED-GUARD` | 0 | 1.0000 | 0 | 0 | safe+complete |
| `T-AMBIGUITY-GUARD` | 4 | 0.9167 | 10 | 4 | UNSAFE (FAM-F) |
| `PC-UNSAFE-COARSE` | 271 | 1.0 | 0 | 250 | sensitivity fires |
| `PC-OVERWIDE-OPEN` | 91 | 1.0 | 0 | 91 | sensitivity fires |
| `PC-DECL-UNDER` | 0 | 0.675 | 39 | 0 | gate refuses; shipped fallback |
| `BP-DECL-OVERWIDE` | 201 | 1.0 | 0 | 180 | unsound declaration adopted |
| `NC-REJECT-ALL` | 0 | 0.0 | 120 | 0 | null floor |

`B-DATA-WIDENED` extends the parent's bounded negative to the new families: 18 false accepts
(FAM-D 9, FAM-F 4, FAM-G 5), all executed and 404. The gate controls behave as preregistered:
`PC-DECL-UNDER` is refused by the training-consistency gate (adopted all-false, FA 0) and
falls back to the safe shipped support; `BP-DECL-OVERWIDE` is training-consistent so the gate
adopts it and the arm inherits 201 false accepts. Together these exercise **both directions of
the gate** and show that declaration soundness is external to the gate.

## 5. Validity gates (all PASS)

- `V8_FREEZE_BINDING` PASS: `sha256(prereg.md)=d1148472...` == `freeze.json.hashes`;
  running source == FROZEN RUNNER block after normalization
  (`norm(runner)` sha256 `f7ebfe4c...`); all six `freeze.artifact_hashes` match.
- `M-IDENTITY` PASS: shipping kernel sha256 `718efa6a...` == frozen carrier `b15ed848...`.
- `M-SUPPORT-IDENTITY` PASS: seven induced shipped supports, widened supports and
  ambiguity-guard supports equal the frozen DESIGN constants.
- `M-REGRESSION` PASS: `tests/test_kernel.py` 3/3 (failures 0, errors 0).
- `PC-DETERMINISM-REPEAT` PASS; `PC-EXACT-REPLAY` 61/61 EXECUTABLE.
- `B-LITERAL-KERNEL` PASS: literal pre-promotion blob has no `distill_parameterized`.
- `B-SHIPPED` (FA==0) and `B-DECLARED-FULL` (FA==0 AND coverage==1.0) PASS (bank/label-rule
  consistency anchors).
- Sensitivity gate PASS: `PC-UNSAFE-COARSE` 271≥1, `PC-OVERWIDE-OPEN` 91≥1,
  `PC-DECL-UNDER` adopted all-false + FA 0, `NC-REJECT-ALL` accept 0 / http 0.
- `M-REFUSAL-SEMANTICS-VIOLATIONS` = 0 in every arm.

## 6. Interpretation and product consequence (bounded)

The mandate's existence question is answered **YES by the declared-grammar route**: a
shipped-candidate, not-purely-data-driven guard (ingested declared grammar + training
consistency gate + shipped fallback) held zero false accepts, zero out-of-grammar HTTP and
full coverage on the extended bank, including the pinned FAM-D subrange and the non-pinned
FAM-F/FAM-G. The shipped conservative carrier can raise safe coverage from `0.6750` to `1.0`
by ingesting declared applicability grammars, subject to a **separate implementation +
regression packet** before any shipped change (the guards here are in-run support descriptors,
not shipped bytes).

The complementary bounded negative is that the **purely observational** ambiguity refusal does
NOT generalize: it is UNSAFE on FAM-F (4 false accepts). Therefore the product must not ship
automatic widening without an external declared grammar; the carrier ships conservative until
a declaration is available. `BP-DECL-OVERWIDE` further bounds the mechanism: a soundness
failure in the ingested declaration is not detectable by the training-consistency gate.

## 7. Claim status semantics (no self-promotion)

Per the frozen decision rule, `C-PARAM-INHERIT` remains `EXPERIMENTAL` and
`C-SEMANTIC-RESOLVE` remains `HYPOTHESIS` in all branches. This packet produced evidence
only; it does not advance, promote or ship any claim. Final adjudication belongs to AUDIT and
DIRECTOR. No end-to-end product economics were measured (`model_calls=0`, `model_tokens=0`,
loopback only).

## 8. Unresolved

- Full space of observational refusal rules (only the one frozen rule is bounded UNSAFE).
- Behaviour under adversarially unsound / partially observable declarations (soundness
  assumed external; `BP-DECL-OVERWIDE` shows the gate cannot detect an over-wide declaration).
- Real-world feasibility/cost/staleness of obtaining sound declared grammars (not measured).
- The registered `C-PARAM-INHERIT` four-arm `C-LLM-INHERIT` next_gate remains unmet and
  unfunded (Runtime B2, Intel B3, new Director mandate).
