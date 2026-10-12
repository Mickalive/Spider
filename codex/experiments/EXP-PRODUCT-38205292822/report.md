# EXECUTE report — EXP-PRODUCT-38205292822

- Lane: `product`
- Claim target (binding Director mandate): `C-PARAM-INHERIT` (EXPERIMENTAL, retained); `C-SEMANTIC-RESOLVE` carried to retain HYPOTHESIS only (not measured)
- `design_contract_version`: 2
- Status: **COMPLETE** · Outcome: **SUPPORTS**
- Decision: `SHIPPED_CERTIFICATE_SAFE_AND_COMPLETE__REFUSES_AUDITED_OVERWIDE__CLOSED_WORLD_BOUNDARY_FA=7`
- Canonical machine handoff: `result.json`, `provenance.json`; raw evidence in `raw_evidence/`.
- This report explains the packet; it does not exceed the frozen claim and does not advance any claim status (frozen `spec.json#decision_rule.claim_status_semantics` mandates RETAINED in all branches).

## 1. What was run

The frozen runner (`harness/run_guard.py`, materialized byte-for-byte from the FROZEN
RUNNER block in `prereg.md`, sha256 `f644a5e7...`, V8-normalized equality PASS) executed in
EXECUTE mode against the repo. It installed the frozen POST kernel
(`src/spider/kernel.py` sha256 `3a6caf97...`, pre-state verified as the frozen carrier
`718efa6a...` == git blob `b15ed848...`) on top of the byte-identical promoted carrier —
this is the ACTUAL shipped code change mandated by the Director — and measured the
**ingested-declared-grammar applicability guard with a closed-world soundness certificate**:

- `T-CERT-GUARD` (PRIMARY) — the shipped `SpiderKernel.ingest_declaration` + module-level
  `certify_declaration` code path: a declaration is adopted as the slot's parameter support
  only if it is a valid regex that accepts every training positive AND rejects every value of
  the frozen audited negative bank `CERT_NEG`; otherwise the shipped inferred support is
  preserved unchanged and the declaration is recorded REFUSED (UNKNOWN-first abstention).

Four frozen declaration regimes were applied: `R-SOUND` (each family's true declared
grammar), `R-OVERWIDE` (`^<prefix>.*$`, training-consistent but unsound — the adopted
BP-DECL-OVERWIDE regime), `R-EVASION` (true grammar union the single held-out blind-spot
negative, certificate-passing but unsound), `R-UNDER` (first training value only, too
narrow). Comparators: `C-TRAINING-GATE` (parent training-consistency gate, verbatim
reproduction), `A-RAW-DECL` (unconditional adoption ablation), `B-SHIPPED` (safety floor),
`B-DECLARED-FULL` (safe+complete ceiling), `NC-REJECT-ALL` (null floor).

Bank: 524 unique-bid items, 120 IN / 404 OUT; per-family IN/OUT A 16/56, B 18/55, C 19/53,
D 10/65 (pinned subrange `region-00[0-9]`), E 16/55, F 12/61 (`case-z[a-z]{2}`, non-pinned),
G 29/59 (`token-ab[a-z]`, non-pinned). Audited negative bank sizes A 38, B 37, C 35, D 46,
E 37, F 42, G 41, each excluding exactly the family's single held-out blind spot. Oracle:
stdlib `ThreadingHTTPServer` on `127.0.0.1:0`, 200 iff the path fullmatches the declared
grammar, else 404. The whole evaluation ran twice (`PC-DETERMINISM-REPEAT`).

## 2. Primary result — the shipped certificate is safe and complete on sound declarations

`T-CERT-GUARD` under `R-SOUND` (primary metric `M-CERT-SOUND-FALSE-ACCEPT-COUNT`):

| metric | value |
|---|---|
| `M-CERT-SOUND-FALSE-ACCEPT-COUNT` | **0** |
| `M-CERT-SOUND-HTTP-ON-OUT` | **0** |
| `M-CERT-SOUND-REFUSAL-EXECUTED-COUNT` | **0** |
| `M-CERT-SOUND-COVERAGE` | **1.0 (120/120)** |
| adopted (7 families) | all `CERTIFIED` |
| coverage by family | A/B/C/D/E/F/G all 1.0 |

This is safe+complete on every family including the pinned FAM-D `region-00[0-9]` subrange
and the non-pinned FAM-F / FAM-G. Safe coverage rose from the shipped `0.6750` (81/120) to
`1.0` (`M-COVERAGE-DELTA-VS-SHIPPED = +0.325`) with zero false accepts — a strict
safe-coverage gain, no regression on the frozen zero-false-accept boundary.

## 3. Discrimination — the certificate refuses what the incumbent gate adopts

Under `R-OVERWIDE` (training-consistent, partially-observable over-wide declaration):

| arm | `false_accept_count` | coverage | disposition |
|---|---|---|---|
| `T-CERT-GUARD` (shipped certificate) | **0** | 0.6750 | REFUSED 7/7; shipped support preserved |
| `C-TRAINING-GATE` (incumbent) | **201** | 1.0 | adopted 7/7; over-accepts |
| `A-RAW-DECL` (ablation) | **201** | 1.0 | unconditional adoption |

`M-GATE-OVERWIDE-FALSE-ACCEPT-COUNT = 201` reproduces the recorded BP-DECL-OVERWIDE
boundary exactly; `A-RAW-DECL` shows the over-acceptance is intrinsic to the declaration,
not introduced by any arm. `PC-DISCRIMINATION` PASS (cert FA=0 vs gate FA=201): the shipped
certificate strictly dominates the parent training-consistency gate on the audited over-wide
class. Refusal semantics hold byte-exactly: `PC-INGEST-ABSTAIN` PASS (parameter_supports
preserved unchanged on every REFUSED family, `declaration_certificate.status == "REFUSED"`),
zero refusal-semantics violations (`M-REFUSAL-SEMANTICS-VIOLATIONS = 0`). `R-UNDER` is also
refused 7/7 (`M-CERT-UNDER-FALSE-ACCEPT-COUNT = 0`, coverage back to 0.675 shipped floor) —
the certificate is not a rubber stamp.

## 4. Closed-world boundary — the guarantee's extent, made operational

`BP-EVASION-CERT-PASS` (required to fire): `certify_declaration` ADMITS `R-EVASION` (true
grammar union one held-out blind-spot negative) for all seven families, and
`M-CERT-EVASION-FALSE-ACCEPT-COUNT = 7` (bids `FA-OG-ALPHA-ALL`, `FB-OG-ALPHA-ALL`,
`FC-OG-ALPHA-ALL`, `FD-OG-WRONGRANGE01`, `FE-OG-ALPHA-ALL`, `FF-OG-WRONGRANGE00`,
`FG-OG-WRONGRANGE00`), with `M-CERT-EVASION-HTTP-ON-OUT`-equivalent http_on_out_label = 7.

This is the operational proof that the certificate is **closed-world**: declaration
soundness is not certifiable in general by this mechanism — any unsound declaration whose
over-accept is withheld from the audited negative bank passes the certificate and inherits
false accepts. The shipped product boundary is therefore: an audited allowlist (the frozen
`CERT_NEG` under change control) plus UNKNOWN-first abstention for uncertified declarations.
This directly answers the Director's second question: soundness is not certifiable in the
general case, and the bounded closed-world trust boundary is the shipped kernel's contract.

## 5. Baselines, controls and null

| arm | `false_accept_count` | coverage | http-on-out | reading |
|---|---|---|---|---|
| `B-SHIPPED` | 0 | 0.6750 (81/120) | 0 | safe but over-conservative floor |
| `B-DECLARED-FULL` (ceiling) | 0 | 1.0000 (120/120) | 0 | safe+complete support is attainable |
| `C-TRAINING-GATE` (incumbent) | 201 (R-OVERWIDE) | 1.0 | 180 | adopts training-consistent unsound declaration |
| `A-RAW-DECL` (ablation) | 201 (R-OVERWIDE) | 1.0 | 180 | unsoundness intrinsic to declaration |
| `NC-REJECT-ALL` (null) | 0 accepts, 0 HTTP | — | 0 | detector is not null-tautological |

Positive controls all fired on the real code path: `PC-CERT-ADMITS-SOUND` (CERTIFIED 7/7),
`PC-CERT-REFUSES-OVERWIDE` (REFUSED 7/7), `PC-CERT-REFUSES-UNDER` (REFUSED 7/7),
`PC-INGEST-ABSTAIN` (preserved 7/7), `PC-UNSAFE-RAW` (FA=201 >= 1), `PC-DISCRIMINATION`
(cert 0 vs gate 201), `BP-EVASION-CERT-PASS` (admitted 7/7, FA=7).

## 6. Identity, binding and regression

- `V8_FREEZE_BINDING` PASS: prereg sha matches `freeze.json.hashes['prereg.md']`; running
  runner source == FROZEN RUNNER block (normalized); all five freeze `artifact_hashes`
  re-hash identically after the run.
- `M-CARRIER-PRE` PASS (`718efa6a...`), `M-INSTALL-POST` PASS (`3a6caf97...`),
  `B-LITERAL-KERNEL` PASS (pre-promotion literal `cfec9866...` lacks
  `distill_parameterized`), `M-SUPPORT-IDENTITY` PASS (seven induced shipped supports ==
  frozen `EXPECTED_SHIPPED`; single-slot mechanisms at confidence 0.9 >= 0.8),
  `PC-EXACT-REPLAY` PASS (61/61 training ids EXECUTABLE on the installed package),
  `PC-DETERMINISM-REPEAT` PASS (two independent full runs identical),
  `M-REGRESSION` PASS (tests_run=3, failures=0, errors=0 on the installed package).
- All 22 frozen gates PASS; no BLOCKED/MEASUREMENT_INVALID mapping was triggered.

## 7. Decision and consequences

Frozen decision function: all gates PASS and `M-CERT-SOUND-FALSE-ACCEPT-COUNT==0`,
`M-CERT-SOUND-COVERAGE==1.0`, `M-CERT-OVERWIDE-FALSE-ACCEPT-COUNT==0`,
`M-GATE-OVERWIDE-FALSE-ACCEPT-COUNT>=1` → **SUPPORTS** (SHIPPED_CERTIFICATE_SAFE_AND_COMPLETE).

Product consequence (frozen `spec.json#product_consequence_positive`): ship
`SpiderKernel.ingest_declaration` + `certify_declaration` in `src/spider/kernel.py`; external
agents (or a mechanism registry) can supply declared grammars that raise safe coverage from
0.6750 to 1.0 on the frozen bank, while training-consistent over-wide declarations are
refused and the carrier abstains (UNKNOWN) rather than executing out-of-grammar targets. The
documented closed-world trust boundary (audited negative bank + UNKNOWN-first abstention) is
the product contract for declaration ingestion. Per the frozen `claim_status_semantics`,
`C-PARAM-INHERIT` is RETAINED at EXPERIMENTAL and `C-SEMANTIC-RESOLVE` is RETAINED at
HYPOTHESIS in this branch; this packet authorizes no promotion (promotion requires a
downstream DIRECTOR decision on the audited evidence).

## 8. Validity and representation limits

- V10: the bank is a local synthetic seven-family declared-grammar construction (524 items)
  on a loopback oracle; results are bounded to this bank and this installed carrier and are
  NOT an end-to-end external-agent measurement. No economics/latency/staleness accounting.
- V11: all identity/freeze/regression/control gates passed; measurement failure semantics
  never triggered.
- The certificate's guarantee is closed-world by construction (proven live by
  `BP-EVASION-CERT-PASS` FA=7); it is NOT a general declaration-soundness proof.