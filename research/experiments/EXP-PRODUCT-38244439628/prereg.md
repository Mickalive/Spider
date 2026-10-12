# EXP-PRODUCT-38244439628 preregistration

**Lane:** product  
**Claim:** `C-RESIDUAL-NOVELTY` (codex effective status: EXPERIMENTAL)  
**Design contract:** v2  
**Origin run:** 38244439628 · base_sha `922eee8638c6fed694076d611433d41a5ef75b21`  
**Parent handoff:** `research/experiments/EXP-PRODUCT-38234098353/handoff.json` sha256 `afd535847e31c0939734c09e898bf2b0fff40a85910be3c930ab5bfeef9a3e40` (continuity evidence only; the binding direction is the 38244439628 `director_mandate`)

## 0. STATUS: DESIGN NOT FROZEN — NON-IDENTIFIABLE / DESIGN FAILURE

This preregistration specifies the experiment the mandate requests, then records the
pre-freeze satisfiability attack required by the DESIGN rules and by
`research/EXPERIMENT_PACKET.md` §2. That attack finds the mandate **cannot be frozen as
written** on the named instrument:

1. **Treatment/comparator identity.** The mandated treatment
   `T-MULTIRES` (parameterized inheritance *with decomposable/multi-resolution structure*)
   and the mandated strongest baseline `B-PROCEDURAL` (*compiled procedural lookup*) are
   counter- and success-identical on `SBA-CREDENTIAL-FREE-V3`.
2. **Arithmetically impossible prediction.** The mandate predicts the treatment's
   advantage *grows with controlled residual novelty rather than full task length*. On this
   bank the margin is exactly `1/K` (a function of task length only) and is **constant**
   across the scored novelty ladder; the cost-per-success advantage actually **decreases**
   in `K`.
3. **Ceiling grid points.** At novelty 0.0 and 0.25 the mechanism is inactive and every arm
   scores 1.0, so half the residual-novelty grid has zero discriminating signal.
4. **Duplicate contrast.** The only live contrast on this instrument
   (mechanism-containing inheritance vs memorization: flat cache / nearest-neighbour /
   empty registry) is already certified `ROBUST` with audit `PASS` by
   `EXP-RUNTIME-38194351940`, whose frozen `result.json` already contains the full 56-cell
   success matrix, the per-instance counters and the residual-novelty grid.

Per `research/EXPERIMENT_PACKET.md` §2, "A treatment structurally incapable of becoming
EXECUTABLE is a DESIGN failure, not a scientific result." No outcome-bearing run is
authorized. The `freeze_eligibility` checks `decision_rule_reachability`,
`baseline_identifiability` and `treatment_liveness` are `FAIL`; `freeze_artifacts_bound` is
`NOT_APPLICABLE`; the design is not freeze-eligible. A minimal Director re-scope is proposed
in §7.

---

## 1. Binding mandate (verbatim question)

> On the certified non-ceiling credential-free bank (SBA-CREDENTIAL-FREE-V3) with the
> shipped byte-identical parameterized carrier, does the founding multi-scale
> representation/work-compression hypothesis hold — i.e., does parameterized inheritance
> with decomposable/multi-resolution structure achieve strictly lower counter-cost
> (http_requests + retrieval_calls + verification_calls + repair_attempts) per VERIFIED SAFE
> success than strong internal baselines (flat exact-state cache, nearest-neighbour/retrieval,
> compiled procedural lookup, and the empty-registry inheritance ablation) at matched
> correctness, and does the advantage grow with controlled residual novelty rather than full
> task length — with NO LLM agent required, as a bounded prerequisite/derisk for the gated
> four-arm flagship rather than the flagship itself?

Binding constraints from the mandate: `action=PIVOT`, `claim_id=C-RESIDUAL-NOVELTY`,
`cognitive_reset=true`, `parent_handoff_disposition=PARK`, **no agent arm / no LLM**. The
inherited B11 `C-PARAM-INHERIT` next-question is parked and is *not* the direction.

## 2. Intended design (as mandated, fully specified)

* **Substrate.** `SBA-CREDENTIAL-FREE-V3` (Session-Mechanism-Inheritance), reconstructed
  byte-faithfully from the frozen construction in `EXP-RUNTIME-38194351940`: hidden
  bank-wide affine mechanism `M(x) = (a*x + b) mod P`, `P = 2**40 - 87 = 1099511627689`,
  derived deterministically from `RUN_SEED = "SPIDER-RUNTIME-SBA-V3-2026"`; families
  `F1-RECORDS` (K=8) and `F2-WIDGETS` (K=10); novelty ladder `[0.0, 0.25, 0.5, 0.75]`;
  scored band `novelty >= 0.50`; exactly one `chain` task per scored session (index `K-3`
  at 0.50, `K-1` at 0.75 where the required answer is the composed `M(M(x_q))`).
* **Shipped carrier.** `src/spider/kernel.py` sha256
  `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` (byte-identical,
  unmodified). It induces a single-level support regex; it is a **flat** parameterized
  procedure and cannot solve the bank's numeric chain task.
* **Arms.** `T-MULTIRES` (treatment), `B-FLAT-CACHE`, `B-NN`, `B-PROCEDURAL`, `B-EMPTY`
  (mandated baselines), `PC-EXACT-REPLAY` (positive control), `B-CROSS-SESSION-COMPILE`
  (disclosed identity control), `NC-MECHANISM-OFF` (null/sensitivity).
* **Metric.** `M-COST-PER-VERIFIED-SAFE-SUCCESS(arm, family, novelty) =
  (http_requests + retrieval_calls + verification_calls + repair_attempts) / (# VERIFIED SAFE
  successes)`, at matched correctness (`>= 0.80` floor), over the residual-novelty grid and
  the two family lengths.
* **Decision rule.** `SUPPORTS` iff `T-MULTIRES` is strictly cheapest than **all four**
  baselines at every scored cell **and** `M-NOVELTY-GROWTH > 0` **and**
  `M-LENGTH-GROWTH <= 0`; `FALSIFIES` if not; `MIXED` if it dominates only the memorization
  baselines; `MEASUREMENT_INVALID` on any V1–V8 gate failure.

## 3. Pre-freeze satisfiability attack (required)

The DESIGN rules require actively trying to disprove satisfiability. Findings:

| Failure mode | Present? | Evidence |
|---|---|---|
| treatment/comparator identity | **YES** | §4 |
| unreachable branch | **YES** | §4 |
| arithmetic impossibility | **YES** | §4 |
| ceiling/floor baselines | **YES** | novelty 0.0/0.25 all arms 1.0 |
| insensitive controls | no (for the live sub-contrast) | `NC-MECHANISM-OFF` fires; `V8_retention_counter_distinctness` >= 2 dims |
| missing prerequisites | no | substrate certified; carrier present |
| unbound mutable artifacts | N/A | not freezing |

## 4. Identifiability analysis (decisive)

### 4.1 Counter-invariance lemma
All four counters are incremented **only** inside the HTTP helpers (`_sess`, `_task`,
`_commit`) and a fixed per-task verification increment. Local representation
build/inference/reuse/composition cost is **not instrumented**. To answer the unique chain
task correctly, any mechanism-containing representation must execute the same minimal call
sequence: one calibration session + `K` calibration task/commit calls + one scored session +
`K` scored task calls + `K` scored commit calls. Therefore **any two mechanism-containing
representations are counter-identical**.

Measured on the frozen instrument (`EXP-RUNTIME-38194351940` `result.json`
`metrics.per_instance_counters_at_0.5`):

| cell | `T-MECHANISM-INHERIT` | `B-CROSS-SESSION-COMPILE` | `PC-EXACT-REPLAY` |
|---|---|---|---|
| F1-RECORDS (http/retr/ver/rep) | 34/0/16/0 | 34/0/16/0 | 34/0/16/0 |
| F2-WIDGETS (http/retr/ver/rep) | 42/0/20/0 | 42/0/20/0 | 42/0/20/0 |

`V8_identity_disclosure = true` is the runtime's own recorded measurement of exactly this
identity.

### 4.2 The mandate's "compiled procedural lookup" baseline is the treatment
Under the only reading that makes `B-PROCEDURAL` a **strong** baseline (it generalizes), it
recovers `(a, b)` from the labelled calibration examples and applies them — which *is* the
runtime's `T-MECHANISM-INHERIT`. It is therefore success-identical (1.0) and
counter-identical (F1 total 50, F2 total 62) to the treatment at every scored cell. Under
the exact-key reading it duplicates `B-FLAT-CACHE` (0.875/0.900). In neither case does a
`T-MULTIRES`-vs-`B-PROCEDURAL` advantage exist.

### 4.3 The novelty-growth prediction is arithmetically false
The scored session contains **exactly one** chain task at *both* scored novelties, so the
memorization comparators score exactly `(K-1)/K` (F1 0.875, F2 0.900) at 0.50 **and** 0.75,
and the treatment scores 1.0. The success margin is therefore `1/K` = 0.125 (F1) / 0.100
(F2), **identical** at both novelties. In cost per verified safe success:

| cell | T total | T succeeds | T cost/safe | flat-cache total | flat succeeds | flat cost/safe | ratio |
|---|---|---|---|---|---|---|---|
| F1 @0.50 | 50 | 8 | 6.250 | 53 | 7 | 7.571 | 1.2114 |
| F1 @0.75 | 50 | 8 | 6.250 | 53 | 7 | 7.571 | 1.2114 |
| F2 @0.50 | 62 | 10 | 6.200 | 65 | 9 | 7.222 | 1.1649 |
| F2 @0.75 | 62 | 10 | 6.200 | 65 | 9 | 7.222 | 1.1649 |

The advantage is **constant across residual novelty** and **decreasing in task length `K`**
— the exact opposite of the mandate's discriminating prediction.

### 4.4 Ceiling grid points
At novelty 0.0 and 0.25 the mechanism is inactive (`mechanism_active` requires
`novelty >= 0.50`) and every arm scores 1.0. Half the residual-novelty grid carries no
signal.

### 4.5 The live contrast is already certified
`EXP-RUNTIME-38194351940` (`status=COMPLETE`, `outcome=SUPPORTS`, `decision=ROBUST`,
audit `PASS`, `determinism_ok=true`, 56 cells x 20 sessions) already measured
mechanism-containing inheritance (`1.0`) vs memorization (`(K-1)/K`). Its frozen
`result.json` already contains the success matrix, the counters and the residual-novelty
grid. A new EXECUTE would re-derive existing numbers.

## 5. Freeze eligibility verdict

| check | status | reason (abridged) |
|---|---|---|
| `decision_rule_reachability` | **FAIL** | `SUPPORTS` unreachable (T ≡ B-PROCEDURAL); novelty-growth requirement arithmetically impossible |
| `measurement_prerequisites` | PASS | substrate certified/deterministic; carrier present (bank harness on `origin/lab2/runtime`, must be reconstructed) |
| `baseline_identifiability` | **FAIL** | `B-PROCEDURAL` is not separable from `T-MULTIRES` on this instrument |
| `control_sensitivity` | PASS | `NC-MECHANISM-OFF` / `PC-EXACT-REPLAY` / counter-distinctness sensitive for the live sub-contrast; none can separate two mechanism-containing representations |
| `treatment_liveness` | **FAIL** | no decomposable/multi-resolution structure exists on the bank; the specified treatment collapses onto the plain compiled mechanism |
| `freeze_artifacts_bound` | NOT_APPLICABLE | not proceeding to freeze; no new mutable artifact introduced |

`freeze_artifacts = []`. The design is **not freeze-eligible**.

## 6. Consequence of each outcome (decision counterfactual)

* **Win (mandated SUPPORTS):** would justify investing in a decomposable/multi-resolution
  inherited representation and keep `C-RESIDUAL-NOVELTY` as a live flagship discriminator.
* **Lose/FALSIFIES (expected):** the multi-scale representation/work-compression moat is
  **UNPROVEN on this substrate and must not be assumed** (POLICY: "do not assume graph
  structure saves tokens"); the only evidenced lever is inheritance-vs-memorization
  (generalization), already certified.
* **Invalid (MEASUREMENT_INVALID):** instrumentation/prerequisite defect.

On this instrument the outcome is essentially **known a priori** (win is unreachable; the
live contrast is already certified), so no branch changes a product decision. Per POLICY's
decision-counterfactual rule this argues for PARK/redesign rather than a new EXECUTE.

## 7. Minimal re-scope (proposed to the Global Research Director; NOT adopted silently)

* **R1 — make the structure live (representation-economics goal).** Authorize a substrate
  with *genuinely decomposable* structure and/or extend the counter model with an
  instrumented local representation-cost dimension (build/compile/inference/reuse). The
  frozen network-only counters cannot represent any local representation effect.
* **R2 — derive, do not re-run (product-economics goal).** The cost-per-VERIFIED-SAFE-success
  summary is a deterministic function of the existing `EXP-RUNTIME-38194351940` raw counters
  and success matrix; compute it in a DIRECTOR/analysis step instead of a new experiment.
* **R3 — residual-novelty mechanism goal is not testable on this bank.** `SBA-CREDENTIAL-FREE-V3`
  has exactly one chain task per scored session at every scored novelty; testing
  "advantage grows with residual novelty" requires a bank with a monotone chain-count ladder
  (e.g. 1..m chain tasks per session).

## 8. What was done at DESIGN (and what was not)

* **Done (non-outcome-bearing):** read the exact mandate and parent handoff; read the frozen
  `EXP-RUNTIME-38194351940` packet (`spec.json`, `result.json`, `handoff.json`, harness);
  inspected the shipped carrier; reconstructed the counter/success arithmetic above.
* **NOT done:** no outcome-bearing measurement; no new harness authored or executed; no
  files frozen; no code promoted; no claim advanced.

## 9. Evidence references

* `research/experiments/EXP-PRODUCT-38244439628/request.json` (mandate, `design_contract_version=2`)
* `research/experiments/EXP-RUNTIME-38194351940/{spec,result,handoff}.json` on `origin/lab2/runtime`
  (certified SBA-CREDENTIAL-FREE-V3; `metrics.per_instance_counters_at_0.5`,
  `metrics.success_rate_matrix`, `metrics.gates`, `metrics.determinism_ok`)
* `research/experiments/EXP-PRODUCT-37989728440/` (prior `C-RESIDUAL-NOVELTY` dynamic-range-certificate failure)
* `src/spider/kernel.py` sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`
* `research/EXPERIMENT_PACKET.md` §2 (v2 treatment liveness), §3 (spec fields)
* `research/portfolio/POLICY.md` (multi-scale ablation; decision counterfactual; strongest fair baseline)
