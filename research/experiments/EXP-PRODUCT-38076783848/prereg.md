# EXP-PRODUCT-38076783848 preregistration — Product lane

Experiment: `EXP-PRODUCT-38076783848`  Lane: `product`  Claim: `C-PARAM-INHERIT`
Design contract: v2. Frozen request: `request.json` (immutable). Base SHA: `176ab633ebcd2e066f6c21701a591faf0e128d18`.

## 0. Mandate and scope

The Global Research Director's mandate (`request.json.director_mandate`) is binding: `action=CONTINUE`,
target claim `C-PARAM-INHERIT`, parent-handoff disposition `SUPERSEDE`. This experiment lands the
already-audited parameterized-inheritance carrier
(`research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`, git blob
`b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256
`718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`) byte-identically at the shipped
path `src/spider/kernel.py`, evidenced by an arm-differentiation certificate that includes:

(i) a known-positive inherited-parameter round trip on a **real task** (loopback HTTP against the frozen
    substrate, server-side success state, `verify()` true);
(ii) a known-negative refusal case (out-of-support identifier, missing parameter, wrong intent —
    `bound_action == null`, non-empty reason, zero executions);
(iii) an explicit treatment-vs-comparator contrast showing the shipped-kernel treatment differs from the
    `INSTRUCTIONS` baseline over the exact same cases (success and abstention discriminators, with a
    degenerate injection proving the metric is not tautological);
(iv) shipped-kernel identity (sha256 + git blob equality, unchanged siblings, pre-install unreachability)
    and promoted tests (`tests/test_ship_kernel.py` with enumerated non-vacuous assertions, plus the
    existing regression suite);
(v) promotion-pinned accounting (deterministic counters owned by the shipped kernel, per-trajectory
    accounting fidelity against a seeded scripted trajectory, `pre_execute_sha` recorded for the
    `product-promote.yml` src/tests diff).

Explicitly **NOT** run: the four-arm benchmark (T-SPIDER-PARAM / B-COLD-RE-DERIVE / B-RETRIEVAL-SHAPED /
INSTRUCTIONS success-rate or budget semantics of the parent's frozen four-arm design) or any real-LLM
benchmark (C11). Money/latency accounting is out of scope this cycle (it requires B2). This experiment
does not promote the claim itself; it produces a promotion-pinned certificate that the AUDIT/DIRECTOR
stages consume and that clears readiness condition B1 (a shipped parameterized-inheritance carrier plus a
known-negative refusal).

## 1. Inherited evidence (preserved distinctions, not re-tested)

The parent handoff (`EXP-PRODUCT-37989728440`, sha256 `911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`)
carries these distinctions, which this packet preserves as inherited state:

- **established**: carrier and shipped-kernel integrity intact (carrier blob `b15ed848` / sha256
  `718efa6a…`; shipped `src/spider/kernel.py` unchanged blob `cfec9866…`); measurement-valid
  deterministic run of the parent's four-arm design (all arms success_rate 1.0, 30/30 known negatives,
  `model_calls == 0`, literal kernel 0.0 success, live localhost HTTP); **bounded substrate-class
  negative**: the mandatory-discovery deterministic credential-free REST certificate is unsatisfiable
  (cold and retrieval at the 1.0 ceiling, novelty >= 0.5, families F1/F2) and counter-only economics
  tie/worsen versus cold; the parent's C3 'PASS' is latency_ms/1000 noise, not an advantage; governance
  defect: the freeze step did not enforce a certificate gate.
- **rejected** (bounded to that substrate class and arm design): certified dynamic range on the
  mandatory-discovery REST substrate; counter-only work compression versus cold/retrieval there;
  latency-inclusive cost as a discriminating metric; asserted (non-enforced) certificate gating.
- **unknown**: whether *any* credential-free deterministic substrate can show certified dynamic range
  for that arm design; whether an asymmetric/amortized-discovery substrate would let the treatment save
  work; whether the external four-arm C-LLM-INHERIT benchmark can run (needs a programmatic,
  budget-stable, credential-free model endpoint — Intel found none); whether the kernel's support
  predicates applied to free-form payload values are a defect; when the freeze script is repaired.
- **do_not_assume**: do not read the parent negative as evidence against C-RESIDUAL-NOVELTY or
  C-PARAM-INHERIT economics in general (claim ceiling preserved); do not treat 1.0 correctness as
  evidence inheritance lacks value; do not treat parent 'PASS' rows as work compression; do not assume
  the *shipped* kernel contains the parameterized path (it is still blob `cfec9866…`); do not assume the
  freeze step enforces certificate gates; do not re-run the mandatory-discovery REST certificate (three
  consecutive failures); do not promote parent scaffolding (`promote_to_product = false`); do not read
  `model_calls == 0` as a measured zero-cost claim (zero by construction); C-MEAS-VALID /
  C-RESIDUAL-NOVELTY events were retentions, no status change.

The active mandate SUPERSEDES the parent's `next_question` (four-arm C-LLM-INHERIT benchmark): that
benchmark is not funded until B1/B2/B3 hold. B1 is this experiment.

### 1.1 Material differences from prior same-mandate attempts and pre-2.0 precedents

- **EXP-PRODUCT-38072222177** and **EXP-PRODUCT-38074828779** (identical mandate) each reached a complete
  spec/prereg of the same shape but their independent design-review stage crashed before any content
  adjudication (`model_design_review.json`: status=failure, model `opencode/exo-free`, exit_code=1,
  category=substantive, attempts=4, identical fingerprint `3b9ff5e4e9e73f23e368efb4`; no
  `design_review.json` was ever written). The failure is reviewer-infrastructure, not a scientific
  rejection of the design content: this packet is not an identical rerun of an invalid/degenerate design.
  It (a) re-verifies every satisfiability claim empirically instead of analytically, adding DESIGN-time
  end-to-end probes on the exact frozen real substrate (§4, probes B/C), (b) records the frozen artifact
  hashes and symbol absence against this run's immutable `base_sha 176ab633…`, (c) tightens
  `freeze_artifacts_bound` and `measurement_prerequisites` rationales with that evidence, and (d) carries
  the same stable control/metric IDs (T-SPIDER-SHIPPED, B-INSTRUCTIONS, B-LITERAL-KERNEL,
  B-SHIPPED-PRE-INSTALL, PC-PARAM-BINDING, PC-NULL-REFUSAL, C0–C12) so AUDIT can reuse them regardless
  of which attempt's certificate is consumed.
- **Pre-2.0 guards** (from the mandate's comparative reasoning, `request.json`): P2-REPLAY-COST
  (sha `9687ff78…`, scripted replay not proven to save net runtime) — this experiment never claims
  economics from replay; it reports counter-only accounting and gates identity/behavior, not
  replay-cost savings. P2-BLIND-COMPOSITION (sha `017a80ae…`, 3/3 unseen compositions with
  keyword/oracle-guided stopping and weak baselines) — this experiment's contrast removes keyword/oracle
  shortcuts: the only 'oracle' is the frozen slot-name→value mapping fixed in
  `#real-tier-cases`, applied identically to every case, with a degenerate injection and a
  non-vacuity gate on the promoted test.
- **No located pre-2.0 artifact shipped a parameterized-inheritance carrier with a known-negative
  refusal and a treatment-vs-INSTRUCTIONS contrast** (mandate's comparative reasoning); the object is
  new, and the prior product failures all died on the mandatory-discovery dynamic-range
  certificate, which this experiment deliberately does not gate (C11; the parent's bounded negative is
  preserved in §1).

## 2. Design (frozen inputs and the one new apparatus)

Frozen inputs are pinned by `freeze_artifacts` and re-hashed into `freeze.json.artifact_hashes`:

| artifact | role | sha256 |
|---|---|---|
| `EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` | treatment bytes (installed at `src/spider/kernel.py`) | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` (blob `b15ed848…`) |
| `EXP-PRODUCT-37989728440/harness/substrate.py` | real localhost HTTP task bank + environment | `0f9f9182cb90ac9e379000e4420a93ba2d2e6a167906c59bd9eac8a8392395af` |
| `EXP-PRODUCT-37950607128/harness/fixture.py` | frozen synthetic bank (`SYNTH-INDUCTION-BANK-v1`) | `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` |
| `EXP-PRODUCT-37950607128/harness/run_certificate.py` | frozen, already-audited synthetic scoring engine | `59895ddd9a85b6b3f75f9bfef6d39c423740679517df24505d26965918525970` |
| `src/spider/models.py` | shipped support (unchanged) | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` |
| `src/spider/registry.py` | shipped support (unchanged) | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` |
| `src/spider/__init__.py` | shipped support (unchanged) | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` |
| `tests/test_kernel.py` | existing regression suite (unchanged) | `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` |

`src/spider/kernel.py` is deliberately **excluded** (it is the treatment subject EXECUTE replaces);
C0 pins it to the carrier artifact above (installed sha256 == carrier sha256 AND git blob equality,
plus unchanged siblings).

Tier 1 (synthetic, fully frozen): the frozen runner (grammatically: imports `spider.kernel` at the
shipped path, `fixture` from `harness/`) exercises positives F1–F6, 24 negatives, the action-identity
contrast and its degenerate-variant injection, accounting fidelity, identity binding and the literal
floor. EXECUTE byte-copies `fixture.py` and `run_certificate.py` into this experiment's `harness/`;
because the copy's own path defines its `EXPERIMENT_DIR`, running it writes its raw
`raw_fixture/`/`raw_certificate/` outputs into **this** experiment's directory (the frozen sibling's
outputs are never mutated). A copy whose sha256 does not equal the frozen hash invalidates the
measurement. The runner's embedded `EXPERIMENT_ID = "EXP-PRODUCT-37950607128"` is the instrument's origin
identifier; it is disclosed, never rewritten, and this experiment's identity is carried by its own
packet files.

Tier 2 (real, frozen substrate + one EXECUTE-authored deterministic driver): EXECUTE byte-copies
`substrate.py` into `harness/` and authors `harness/run_real_certificate.py`, a deterministic driver
with **no tunable parameters** that transcribes the frozen rules in `#real-tier-cases` (which were
themselves executed end-to-end at DESIGN time in probes B/C). It imports the shipped `spider` package
(to certify the shipped path, not the carrier copy) and the frozen substrate; its sha256 is recorded in
`provenance.json`, and every decision quantity is recomputed by AUDIT from the raw request/response and
resolve-decision logs. Because the driver does not exist at freeze it cannot be listed in
`freeze_artifacts`; the real task bank and environment it depends on (`substrate.py`) is bound, and all
thresholds are frozen in this prereg and `spec.json` (§5).

## 3. Pre-freeze arm-differentiation certificate (satisfiability, no confirmatory outcome data)

- **Arms differ by construction, and the contrasts are sensitivity-bearing.**
  - Treatment `T-SPIDER-SHIPPED`: `distill_parameterized` over real training demonstrations induces a
    mechanism with slots; `resolve` rebinds them to a held-out identifier; the bound action contains the
    held-out id and executes live (200 + `body.success true` + `verify()` true).
  - `B-INSTRUCTIONS`: literal demonstration replay (no slots, no guard) whose action contains the
    *training* id, so it cannot succeed on held-out ids (404) and never abstains on out-of-support ids.
  - `B-LITERAL-KERNEL`: confidence `0.5 < 0.8` → non-`EXECUTABLE`, 0 held-out executables.
  - `B-SHIPPED-PRE-INSTALL`: parameterized symbols absent, positive arm unreachable (`AttributeError`).
- **Arithmetic bound.** Real success >= 5/5 (exactly 10 held-out novelty-0.0 tasks, 5 per family, no
  selection freedom); refusal battery = 3 constructions × the same 10 tasks; synthetic 6/6 and 24/24;
  real equivalence discriminators `== 1.0` with degenerate injection `0.0/0.0`; literal floor 0; exit
  code 0. No outcome depends on an unbounded/stochastic quantity.
- **Total precedence.** `spec.json#decision_rule.precedence` is ordered (BLOCKED → C0 →
  C1–C7 FALSIFIES → C8–C12 MEASUREMENT_INVALID → SUPPORTS); the region {a core fails and an integrity
  check fails} is assigned to FALSIFIES, so no evaluated state is undefined.
- **No ceiling/floor trap.** `B-COLD-RE-DERIVE` is provably at the 1.0 correctness ceiling on this
  substrate (parent BOUNDED_SUBSTRATE_CLASS_NEGATIVE), so it is a reported cost reference and explicitly
  **non-gating**, and the four-arm benchmark is not run (C11). The gated real contrast (C3) is an
  equivalence test between the treatment and `B-INSTRUCTIONS`: its discriminators are `== 1.0` only
  when the treatment binds (success `1.0`) and refuses (refusal `1.0`); a treatment that behaves like
  `B-INSTRUCTIONS` (failing to bind or over-accepting) drives them to 0, and the degenerate injection
  makes that collapse explicit. The synthetic contrast (C6) is credited only after EXECUTE/AUDIT verify
  from the raw certificate JSON that all treatment actions are non-null and `EXECUTABLE`, so it cannot
  be passed by a broken treatment via `None != action`.

## 4. Design-time satisfiability probes

Run in DESIGN against isolated `/tmp/opencode/probe` copies of the frozen bytes (carrier
`kernel.py` + shipped `models.py`/`registry.py`/`__init__.py` + frozen `substrate.py`); they consume no
confirmatory held-out positive outcome (no held-out task from `build_test_tasks()` at novelty 0.0 was
resolved or executed) and hit no commit path. All outputs below are raw observed transcript, recorded
here verbatim.

**Probe A — frozen identity and hashes.** At base_sha `176ab633…`: `src/spider/kernel.py` →
blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` (verified via `git rev-parse
176ab633…:src/spider/kernel.py`); symbol scan on those bytes shows only `_bind` (line 35) and `distill`
(line 74) — `distill_parameterized`, `_infer_support`, `_support_accepts`, `TrajectoryCounters` all
absent. Carrier → blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256
`718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`. All eight freeze artifacts
match the table in §2 exactly.

**Probe B — carrier liveness at the shipping position (toy ids).** Carrier copied into a `spider/`
package with the shipped `models.py`/`registry.py`/`__init__.py`; two toy observations with varying
URL identifier segment:

```
CARRIER_MECHANISM {"conf": 0.9, "id": "mech-053e3b63ee958f0d", "slots": ["session_token", "property", "value", "doc"],
  "supports": {"doc": "^doc\\-0[0-9]{2}$", "property": "^[a-z]+$", "session_token": "^tok\\-[a-z]{3}$", "value": "^draft\\-[0-9]{1}$"}}
CARRIER_RESOLVE EXECUTABLE {"headers": {"X-Session-Token": "tok-ccc"}, "json": {"property": "status", "value": "draft-7"},
  "method": "POST", "url": "http://127.0.0.1:9000/api/doc/doc-077/update"}
CARRIER_REFUSE_OUT_OF_SUPPORT EXPLORE None "parameter 'doc' outside inferred support"
CARRIER_REFUSE_MISSING EXPLORE None "missing required parameter 'doc'"
CARRIER_REFUSE_WRONG_INTENT UNKNOWN None 'no applicable validated mechanism'
LITERAL_CONF 0.5
LITERAL_RESOLVE EXPLORE None
COUNTERS {"browser_actions": 0, "http_requests": 0, "latency_ms": 0.0, "model_calls": 0, "model_tokens": 0,
  "repair_attempts": 0, "retrieval_calls": 4, "verification_calls": 0}
```

Interpretation: the carrier at the shipping position induces a parameterized mechanism
(`confidence 0.9 >= 0.8`), rebinds an unseen identifier (`doc-077`) into an `EXECUTABLE` bound action,
the shipped literal floor is preserved (`0.5` → non-`EXECUTABLE`), refusal directions are non-`EXECUTABLE`
with `bound_action = null` and non-empty reasons, and counters are owned by the kernel
(`retrieval_calls` incremented only by `resolve`; 4 increments over 4 `resolve` calls).

**Probe C — REAL-tier end-to-end on the frozen substrate (training tasks only).** Ran the frozen
`substrate.py` on 127.0.0.1; captured demonstrations for the 5 F1/documents **training** tasks
(`doc-011/022/033/044/055` — training ids are not confirmatory); induced one mechanism; resolved a
non-confirmatory in-support id `doc-077` (not a training id, not a held-out id) and executed live:

```
TRAIN_IDS ['doc-011', 'doc-022', 'doc-033', 'doc-044', 'doc-055']
MECHANISM {"conf": 0.9, "id": "mech-6b68facb44925911", "slots": ["session_token", "property", "value", "document"]}
SUPPORTS {"document": "^doc\\-0[0-9]{2}$", "property": "^[a-z]+$", "session_token": "^tok\\-[a-z0-9]{16}$", "value": "^draft\\-[0-9]{1}$"}
RESOLVE EXECUTABLE {"headers": {"Content-Type": "application/json", "X-Session-Token": "tok-…"},
  "json": {"property": "status", "value": "draft-7"}, "method": "POST", "url": "http://127.0.0.1:<port>/api/documents/doc-077/update"}
EXEC_STATUS 200 {"id": "doc-077", "property": "status", "success": true, "type": "documents", "value": "draft-7"}
SUCCESS True VERIFY True
COUNTERS {"browser_actions": 0, "http_requests": 0, "latency_ms": 0.0, "model_calls": 0, "model_tokens": 0,
  "repair_attempts": 0, "retrieval_calls": 1, "verification_calls": 1}
```

Interpretation: the exact real-tier recipe (induce from training demos → slot-name→value mapping →
`resolve` → live execute → `verify`) is satisfiable end-to-end on the frozen substrate with the exact
carrier bytes and shipped support. The `document` slot name derives from the URL static segment
(`documents` → `document`) and is covered by the otherwise-unmapped → `target_identifier` rule
(`#real-tier-cases`). `retrieval_calls == 1` and `verification_calls == 1` after one `resolve` and one
`verify`, confirming kernel ownership (T4).

**Probe D — held-out reachability, grammar, disjointness, refusal, and INSTRUCTIONS 404 (structural +
training-induced mechanism).** No held-out positive was resolved.

```
TRAIN_TOTAL 20
TRAIN_FT ('F1', 'documents') ['doc-011', 'doc-022', 'doc-033', 'doc-044', 'doc-055']
TRAIN_FT ('F1', 'records')   ['rec-011', 'rec-022', 'rec-033', 'rec-044', 'rec-055']
TRAIN_FT ('F2', 'gadgets')   ['gad-011', 'gad-022', 'gad-033', 'gad-044', 'gad-055']
TRAIN_FT ('F2', 'widgets')   ['wid-011', 'wid-022', 'wid-033', 'wid-044', 'wid-055']
HELDOUT0_TOTAL 10 TOTAL_ALL_NOVELTY 40
HELDOUT0_FAMILY F1 n 5 grammar_ok True disjoint_from_train True
HELDOUT0_FAMILY F2 n 5 grammar_ok True disjoint_from_train True
HELDOUT0_FT [('F1','documents'), ('F1','records'), ('F2','gadgets'), ('F2','widgets')] all_have_training True
TRAIN_VALUES ['draft-0'..'draft-4'] HELD_VALUES ['draft-5'..'draft-9'] held_in_support True
REAL_MECH_SLOTS ['session_token', 'property', 'value', 'document'] conf 0.9
REAL_REFUSE OUT_OF_SUPPORT EXPLORE None "parameter 'document' outside inferred support"
REAL_REFUSE MISSING_PARAM  EXPLORE None "missing required parameter 'document'"
REAL_REFUSE WRONG_INTENT   UNKNOWN None 'no applicable validated mechanism'
INSTRUCTIONS_REPLAY_URL http://127.0.0.1:<port>/api/documents/doc-011/update STATUS 404
COUNTERS {..., "model_calls": 0, "model_tokens": 0, "retrieval_calls": 3, "verification_calls": 0}
```

Interpretation: at novelty 0.0, `build_test_tasks()` yields exactly 10 tasks (5 per family, spanning
both families; ids alternate across a family's two resource types from 013/026/039/052/065), all inside
the induced support grammar `^<type>-0[0-9]{2}$` and disjoint from training ids (`<type>-011/022/033/044/055`).
Every held-out `(family, resource_type)` has a training mechanism; held-out values `draft-5..9` stay in
support (`^draft\-[0-9]{1}$`). The real training-induced mechanism refuses out-of-support, missing-param
and wrong-intent cases with `bound_action = null` and non-empty reasons. `B-INSTRUCTIONS` success is
structurally 0.0: the replayed training id (here `doc-011`) is absent from the held-out-shaped scenario
and the substrate returns HTTP 404; `B-INSTRUCTIONS` never abstains by construction.

No confirmatory held-out positive, real held-out identifier or arm success metric is produced by these
probes.

## 5. Treatment, comparator, controls, and exact pass conditions

Controls (stable ids reused downstream): `T-SPIDER-SHIPPED` (treatment), `B-INSTRUCTIONS` (mandate
comparator, deterministic proxy), `B-LITERAL-KERNEL` (shipped floor), `B-SHIPPED-PRE-INSTALL` (identity
baseline), `B-RETRIEVAL-SHAPED` (frozen synthetic comparator, non-gating), `B-COLD-RE-DERIVE` (reported,
non-gating), `PC-PARAM-BINDING` (positive control), `PC-NULL-REFUSAL` = `B-EMPTIED-REGISTRY` (null
control / emptied registry).

Pass conditions (full text in `spec.json#decision_rule.checks`):

- **C0 identity**: installed sha256 `== 718efa6a…` and blob `== b15ed848…`; siblings unchanged; all
  `freeze.artifact_hashes` match; harness copies match frozen hashes. (gate: MEASUREMENT_INVALID)
- **C1 real positive**: the full novelty-0.0 held-out set, 5 disjoint in-support ids per family,
  both families; resolve `EXECUTABLE`, bound action contains the held-out id, live HTTP 200 with
  `body.success true`, `verify()` true; success `== 1.0`. (FALSIFIES)
- **C2 real negative**: out-of-support / missing-param / wrong-intent → non-`EXECUTABLE`,
  `bound_action == null`, non-empty reason; refusal `== 1.0`, zero executions. (FALSIFIES)
- **C3 real INSTRUCTIONS contrast**: equivalence test over the frozen cases (`#real-tier-cases`):
  treatment success `== 1.0` and INSTRUCTIONS success `== 0.0` (discriminator `== 1.0`); treatment
  refusal `== 1.0` and INSTRUCTIONS refusal `== 0.0`; treatment action non-null on all held-out cases;
  degenerate injection (treatment := INSTRUCTIONS) collapses both discriminators to `0.0` and is
  flagged. (FALSIFIES)
- **C4/C5/C6 synthetic**: frozen runner AD-POSITIVE `6/6`, AD-NEGATIVE `24/24`,
  AD-TREATMENT-CONTRAST real rate `== 1.0` and `degenerate_variant_detected == true`, with
  EXECUTE/AUDIT verifying from the raw certificate JSON that all treatment actions are non-null and
  `EXECUTABLE`. (FALSIFIES)
- **C7 promotion suite**: `compileall -q src` exit 0; `unittest discover -s tests` exit 0 (existing
  `tests/test_kernel.py` + new `tests/test_ship_kernel.py` whose required assertions T1–T5 are
  enumerated in `#required-promotion-regression-test` and verified non-vacuous by AUDIT);
  `validate_repo.py` exit 0. (FALSIFIES)
- **C8 literal floor**: literal confidence `< 0.8`; 0 held-out `EXECUTABLE` synthetic and real.
  (MEASUREMENT_INVALID)
- **C9 accounting**: the frozen `PC-ACCOUNTING-FIDELITY` check deliberately builds a seeded scripted
  trajectory with `scripted.add` (declared `retrieval_calls=3, verification_calls=2, repair_attempts=1`,
  plus an injected `model_calls=1/model_tokens=128` event labelled injected-not-observed) to test
  counter arithmetic; on the actual execution path the harness must not hand-set counters (only the
  shipped kernel increments them), verified by recomputation from raw; observed `model_calls == 0`,
  `model_tokens == 0`. (MEASUREMENT_INVALID)
- **C10 pre-install unreachable**: probed from the immutable `base_sha` bytes
  (`git show 176ab633…:src/spider/kernel.py`, blob `cfec9866…`) loaded in isolation, not from the
  post-install path; the positive arm raises `AttributeError`. (MEASUREMENT_INVALID)
- **C11 no benchmark**: no four-arm arm executed; observed `model_calls == 0`. (MEASUREMENT_INVALID)
- **C12 real-HTTP validity**: substrate live, non-200 for malformed/literal cases (DESIGN verified:
  replay of training id `doc-011` → HTTP 404), loopback only. (MEASUREMENT_INVALID)

Outcome precedence is total (BLOCKED → C0 → C1–C7 FALSIFIES → C8–C12 MEASUREMENT_INVALID → SUPPORTS).

### Real-tier cases

To leave the EXECUTE driver no selection or threshold freedom, the real tier's cases and predicates are
fixed here (hashed in `freeze.json.hashes`); the driver is a mechanical transcription of this section
(and matches DESIGN probes C/D).

- **Task bank.** Training tasks = `substrate.build_train_tasks()`; held-out tasks =
  `substrate.build_test_tasks()` (frozen `substrate.py`). **Held-out positive set = all of
  `build_test_tasks()` evaluated at novelty 0.0** (10 tasks, 5 per family, both families); no subset
  selection is permitted.
- **Demonstrations.** For each training task: `server.set_scenario(build_scenario(task))`, then
  `GET /api/session`, `GET /api/resources`, `GET /api/schema/{resource_type}`, then
  `POST /api/{resource_type}/{target_identifier}/update` with header `X-Session-Token` from
  `/api/session` and JSON `{property: target_property, value: target_value}`. Record one
  `update_resource` `Observation` per task with `state={family, resource_type, base_url}` and the exact
  action executed. Induce one mechanism per `(family, resource_type)` with `distill_parameterized`
  (this is a parameterized-inheritance induction on a *real* task, satisfying mandate item (i), and the
  frozen recipe was executed at DESIGN in probe C).
- **Positive execution.** For each held-out task: `set_scenario`; the `resolve` params are derived from
  the discovered slot names by the frozen fixed mapping — a token-named slot receives the fresh session
  token, a property-named slot receives `target_property`, a value-named slot receives `target_value`,
  and an id-named slot (`id`/`doc`/identifier-named) or any otherwise-unmapped slot receives
  `target_identifier` (covers the observed `document`/`record` slot names);
  `resolve` must return `EXECUTABLE` with a non-null bound action whose URL contains the held-out
  identifier; execute that action; success predicate = `status == 200 AND body.success is True`;
  `verify()` must return true.
- **Negative cases (fixed composition).** For each held-out task, three cases: (a) out-of-support id =
  replace the held-out id with `doc-999` for type `doc` (analogous out-of-pattern id for `rec`/`wid`/`gad`);
  (b) missing-param = call `resolve` with the identifier-bearing slot omitted; (c) wrong-intent = call
  `resolve` with intent `"wrong_intent_" + intent`. Refusal predicate = `status != EXECUTABLE AND
  bound_action is None AND reason` non-empty; no case may execute an HTTP action.
- **INSTRUCTIONS (`B-INSTRUCTIONS`).** For each held-out task, take the verbatim update action recorded
  for the first training task of the same `(family, resource_type)` (an action targeting a training
  identifier) and execute it unchanged with a fresh session token; success uses the same predicate.
  Refusal is defined as never abstaining (it always attempts the literal action), so its refusal rate is
  `0.0` by construction; its success rate is `== 0.0` (required, not merely expected) because the
  training identifier is absent from the held-out scenario (substrate returns 404, violated only if the
  substrate or the server-state construction is misused, which C12's non-200 check catches).
- **Degenerate injection.** Recompute C3 with the treatment results replaced by the `B-INSTRUCTIONS`
  results; both discriminators must become `0.0` and be flagged.
- **Accounting.** No `TrajectoryCounters` field is hand-set by the driver; the shipped kernel increments
  `retrieval_calls` on `resolve` and `verification_calls` on `verify`, and the driver only reads them.

### Required promotion regression test

Because `tests/test_ship_kernel.py` is EXECUTE-authored and ships in the promotion diff, its required
assertions are frozen here (binding via `freeze.json.hashes["prereg.md"]`) so C7 cannot be satisfied by
a vacuous test. The test file MUST import the installed `spider` package (no network, no model calls)
and assert, with concrete expected values/statuses (all four semantics were verified satisfiable at
DESIGN time in probes B/C):

- `T1` parameterized round trip: `distill_parameterized` over >= 2 in-support observations returns a
  mechanism with >= 1 slot and `confidence >= 0.8`; `resolve` with a bound in-support identifier returns
  status `EXECUTABLE` with a non-null `bound_action` whose URL contains that identifier.
- `T2` literal floor: `distill()` on the same observations returns `confidence == 0.5` (`< 0.8`), and
  the resulting `resolve` returns a non-`EXECUTABLE` status (not `EXECUTABLE`).
- `T3` refusal: a wrong-intent and an out-of-support `resolve` each return a non-`EXECUTABLE` status with
  `bound_action is None` and a non-empty `reason`.
- `T4` counter ownership: after one `resolve` and one `verify`, `TrajectoryCounters.retrieval_calls == 1`
  and `verification_calls == 1`, incremented by the kernel (not set by the test).
- `T5` non-vacuity: the same test module, run against the pre-install kernel bytes (C10), fails with
  `AttributeError` on `distill_parameterized`; AUDIT verifies the file contains these exact
  status/value assertions (no `assertTrue(True)` placeholders).

AUDIT independently re-parses the test file and confirms each frozen assertion is present and specific
to the listed status/value; the raw result of `unittest discover` is recorded in `result.json`.

## 6. Procedure (EXECUTE, exactly as frozen)

1. Verify `freeze.json.artifact_hashes` against the working tree; abort to MEASUREMENT_INVALID on any
   mismatch, or BLOCKED if a prerequisite file is missing.
2. Byte-copy the carrier to `src/spider/kernel.py`; assert C0. Byte-copy `models.py`/`registry.py`/
   `__init__.py` unchanged; byte-copy `fixture.py`, `run_certificate.py`, `substrate.py` into `harness/`
   and re-hash.
3. Tier 1: run the copied `run_certificate.py` against the installed shipped kernel; preserve this
   experiment's `raw_fixture/` and `raw_certificate/`. (Its embedded `EXPERIMENT_ID` is the instrument's
   origin `EXP-PRODUCT-37950607128`; disclosed, not rewritten.)
4. Tier 2: run `harness/run_real_certificate.py` (transcription of `#real-tier-cases`, matching DESIGN
   probes C/D): start the frozen `SubstrateServer` on 127.0.0.1; capture training demonstrations for both
   families and all types (`GET /api/session`, `GET /api/resources`, `GET /api/schema/{type}`, then
   `POST /api/{type}/{id}/update` with the discovered session token and the task property/value); induce
   one mechanism per `(family, resource_type)` via `distill_parameterized`; resolve the full held-out
   novelty-0.0 batch, execute live and `verify()`; run the negative battery; run `B-INSTRUCTIONS`
   (literal training action replay) and the degenerate injection; run the null control
   `B-EMPTIED-REGISTRY`; persist every raw request/response, server log and resolve decision.
5. Write `tests/test_ship_kernel.py` implementing the frozen assertions T1–T5
   (`#required-promotion-regression-test`) and run the promotion suite.
6. Compute metrics from raw; write `result.json` / `report.md` / `provenance.json` per
   `research/EXPERIMENT_PACKET.md`; record `execution_checkpoint.json.pre_execute_sha` for
   promotion-pinned accounting.

## 7. Validity threats and disclosures

- **`INSTRUCTIONS` proxy:** `B-INSTRUCTIONS` is a deterministic literal-replay stand-in for a real LLM
  `INSTRUCTIONS` arm; it establishes separability (action identity + success + abstention), **not**
  benchmark superiority over a real instruction-following LLM.
- **C3 comparator is a structural constant:** because `B-INSTRUCTIONS` never abstains and its replayed
  training identifier is absent from every held-out scenario (404), its success and refusal rates are
  constants (0.0/0.0). C3 is therefore an absolute test of the treatment's binding/refusal behaviour
  framed as a contrast; the discriminating (non-constant) comparator is the frozen synthetic
  `B-RETRIEVAL-SHAPED` inside C6, whose nearest-training-action replay returns a genuinely wrong literal
  action, and both C3 and C6 include degenerate injections that must collapse to 0.0 and be detected.
- **EXECUTE-authored real-tier driver:** the driver is a mechanical transcription of the frozen
  `#real-tier-cases` section with no selection or threshold freedom — the exact task bank
  (`substrate.py`), the exact held-out set, negative composition, success/refusal predicates,
  INSTRUCTIONS action and degenerate injection are frozen in this prereg (hashed in `freeze.json.hashes`),
  and the recipe was executed end-to-end at DESIGN (probes B/C/D). Its sha256 is recorded in provenance,
  and AUDIT verifies the raw logged cases equal these rules and recomputes every metric. It cannot be
  freeze-listed because it does not exist at freeze and `freeze_artifacts` requires existing files.
- **Synthetic bank reuse:** `SYNTH-INDUCTION-BANK-v1` is small and author-designed; results are a
  certificate, not generalization evidence beyond it.
- **Hard-coded runner id:** the frozen runner embeds `EXP-PRODUCT-37950607128`; disclosed, not an
  identity claim for this experiment.
- **Weaker built-in identity check:** the frozen runner's `AD-IDENTITY-BINDING` only asserts a pre-blob
  was recorded and differs from the post-install blob; C0 is the authoritative identity gate.
- **Injected model counters:** the frozen `PC-ACCOUNTING-FIDELITY` check deliberately injects a synthetic
  `model_calls=1` / `model_tokens=128` event; it is labelled injected-not-observed and is not real model
  usage. Observed `model_calls`/`model_tokens` are `0`.
- **Loopback HTTP:** the "real task" is a localhost server, not the open Web; it is real
  request/response execution with server-side state verification, not Web-scale generalization.
- **Novelty 0.0 selection:** the real positive tier uses novelty 0.0 (the full set) because the parent
  degeneracy lives there; this is the worst case for arm differentiation, which is why the gated
  contrast is an equivalence test against `B-INSTRUCTIONS` (success and abstention) rather than success
  rate alone. Residual-novelty economics are explicitly out of scope (C11; parent bounded negative
  preserved, §1).
- **Support-grammar scope:** held-out identifiers are inside the induced support grammar `^<type>-0[0-9]{2}$`
  by construction (values follow the training grammar); this certifies the shipped mechanism's behavior
  on in-support generalization, not free-form identifier novelty (parent `unknown` preserved).
- **No claim self-promotion:** only a certificate and a promotion recommendation are produced; claim
  adjudication is downstream.

## 8. Consequences

Positive (all C0–C12 pass): the audited parameterized-inheritance mechanism is established on the shipped
path on a real task with refusal, INSTRUCTIONS separation, identity and accounting; readiness condition
B1 is cleared; the product lane may ship the installed bytes (via `product-promote.yml`'s
`git diff --binary --full-index <pre_execute_sha> <verdict_commit> -- src tests`, still gated by audit
PASS and `verdict.promote_to_product`) and proceed to integration/economics work, bounded to in-support
held-out identifiers from an observed family.
Negative (`FALSIFIES`): do not promote; the failing check names the next bounded repair.
`MEASUREMENT_INVALID`: the instrument, not the mechanism, is the problem — repair the named gate and
re-run. `BLOCKED`: restore the missing prerequisite or grant scope.
