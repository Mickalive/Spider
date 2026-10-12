# EXP-PRODUCT-38315290076 preregistration

**Lane:** product
**Claim:** `C-RESIDUAL-NOVELTY` (codex effective status: EXPERIMENTAL; registry HYPOTHESIS is stale)
**Design contract:** v2
**Origin run:** 38315290076 · base_sha `8094b3480afb7ff5bc4f3af5b880ff4b78d3b897`
**Parent handoff:** `research/experiments/EXP-PRODUCT-38234098353/handoff.json` sha256 `afd535847e31c0939734c09e898bf2b0fff40a85910be3c930ab5bfeef9a3e40` (continuity evidence only; binding direction is this request's `director_mandate`, action CONTINUE, parent disposition PARK)

## 0. STATUS: DESIGN NOT FROZEN — NON-IDENTIFIABLE / DESIGN FAILURE

This preregistration specifies the experiment the mandate requests, then records the
pre-freeze satisfiability attack required by the DESIGN rules and by
`research/EXPERIMENT_PACKET.md` §2. That attack — independently re-verified for this
request against frozen accepted evidence and the current shipped tree at HEAD
`a3d677b2`, not copied from any prior design — finds the mandate **cannot be frozen
as written** on the named instrument:

1. **Treatment/comparator identity.** The mandated treatment `T-MULTIRES`
   (parameterized inheritance *with decomposable/multi-resolution structure*) and the
   mandated strongest baseline `B-PROCEDURAL` (*compiled procedural lookup*) are
   counter- and success-identical on `SBA-CREDENTIAL-FREE-V3` under the only reading
   that makes the baseline strong.
2. **Arithmetically impossible prediction.** The mandate predicts the treatment's
   advantage *grows with controlled residual novelty rather than full task length*. On
   this bank the success margin is exactly `1/K` (a function of task length only),
   constant across the scored novelty ladder (`M-NOVELTY-GROWTH = 0.0` exactly), and the
   cost advantage **decreases** in `K` (1.2114 → 1.1649) — the opposite of the
   prediction in both dimensions.
3. **Degenerate monotonicity statistic.** Only `n = 2` scored novelty points exist with
   tied advantage values, so any rank-monotonicity test is degenerate
   (permutation `p = 1.0`); a `rho > 0.5, p < 0.05`-style growth bar is unreachable.
4. **Ceiling grid points.** At novelty 0.0 and 0.25 the mechanism is inactive and every
   arm scores 1.0, so half the residual-novelty grid has zero discriminating signal.
5. **Carrier incapability (two-horn liveness failure).** The named shipped carrier
   (`src/spider/kernel.py`, sha256 `3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3`,
   working tree clean at this HEAD) induces single-level string-template
   slots with regex supports and performs no arithmetic function learning, so it cannot
   solve the bank's `M(x) = (a*x+b) mod P` chain task; the abstract multi-resolution
   treatment has no distinct executable instantiation either.
6. **Duplicate contrast.** The only live contrast (mechanism-containing inheritance vs
   memorization) is already certified `ROBUST` with audit `PASS` by
   `EXP-RUNTIME-38194351940`, whose frozen `result.json` already contains the full
   success matrix, per-instance counters, counter-distinctness and the novelty grid.

Per `research/EXPERIMENT_PACKET.md` §2, "A treatment structurally incapable of becoming
EXECUTABLE is a DESIGN failure, not a scientific result." No outcome-bearing run is
authorized. `freeze_eligibility` records `decision_rule_reachability = FAIL`,
`baseline_identifiability = FAIL`, `treatment_liveness = FAIL`,
`measurement_prerequisites = PASS`, `control_sensitivity = PASS` (bounded),
`freeze_artifacts_bound = NOT_APPLICABLE`; the design is not freeze-eligible. A minimal
Director re-scope (R1/R2/R3) is proposed in §7; the R2 economic summary is already
derived in §5 from frozen evidence so no EXECUTE is needed to answer it.

Relation to sibling DESIGN failures (`EXP-PRODUCT-38244439628`, `EXP-PRODUCT-38291106470`,
same mandate question, both `DESIGN_FAILURE_NON_IDENTIFIABLE_NOT_FROZEN`): this packet
is NOT an identical repeat. It re-executes every satisfiability probe at this request's
base/HEAD (carrier re-hashed, frozen runtime packet re-read, decision table
recomputed, primary sources re-read in targeted form), re-binds the current shipped
carrier identity, and records the failure with this experiment's own evidence
references. The degenerate structure is a Research-2.0 instrument property of V3, not a
pre-2.0 inheritance; repeating the *finding* with fresh verification is the
fail-loud duty, while repeating the *EXECUTE* would be the forbidden duplicate.

---

## 1. Binding mandate (verbatim question)

> Resume the pre-freeze experiment: on the certified non-ceiling credential-free bank
> (SBA-CREDENTIAL-FREE-V3) with the shipped byte-identical parameterized carrier, does
> the founding multi-scale representation/work-compression hypothesis hold — i.e. does
> parameterized inheritance with decomposable/multi-resolution structure achieve strictly
> lower counter-cost (http_requests + retrieval_calls + verification_calls +
> repair_attempts) per VERIFIED SAFE success than strong internal baselines (flat
> exact-state cache, nearest-neighbour/retrieval, compiled procedural lookup, and the
> empty-registry inheritance ablation) at matched correctness, and does the advantage
> grow with controlled residual novelty rather than full task length — with NO LLM agent
> required, as a bounded prerequisite/derisk for the gated four-arm flagship rather than
> the flagship itself?

Binding constraints: `action=CONTINUE`, `claim_id=C-RESIDUAL-NOVELTY`,
`cognitive_reset=true`, `parent_handoff_disposition=PARK`, **no agent arm / no LLM**,
**frozen V3 bank only** (dependencies note `C-MEAS-VALID B2 discharged`; `B1/B3` still
gate the flagship), stop trigger (treatment/comparator distinction collapses → abort).
The inherited B11 `C-PARAM-INHERIT` next-question is parked and is *not* the direction.
This DESIGN refines nothing away: it specifies the mandate exactly, then proves it
unfreezable. No nearby objective is substituted; if the Director disagrees with the
proof, the failure record pinpoints the exact step to rebut.

## 2. Intended design (as mandated, fully specified)

* **Substrate.** `SBA-CREDENTIAL-FREE-V3` (Session-Mechanism-Inheritance) per the frozen
  construction in `EXP-RUNTIME-38194351940`: hidden bank-wide affine mechanism
  `M(x) = (a*x + b) mod P`, `P = 2**40 - 87 = 1099511627689` (prime), derived
  deterministically from `RUN_SEED = "SPIDER-RUNTIME-SBA-V3-2026"`; families
  `F1-RECORDS` (K=8) and `F2-WIDGETS` (K=10); novelty ladder `[0.0, 0.25, 0.5, 0.75]`;
  scored band `novelty >= 0.50`; exactly one `chain` task per scored session (index `K-3`
  at 0.50, `K-1` at 0.75 where the required answer is the composed `M(M(x_q))`).
* **Shipped carrier.** `src/spider/kernel.py` at working-tree sha256
  `3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3` (working tree
  clean at HEAD `a3d677b2`; matches the parent handoff's frozen carrier identity and
  the sibling 38291106470 binding). Verified by reading `distill_parameterized`:
  single-level slots over observed identifier strings with `_infer_support` regexes;
  no arithmetic induction — a flat parameterized procedure that cannot solve the bank's
  numeric chain task.
* **Arms.** `T-MULTIRES` (treatment), `B-FLAT-CACHE`, `B-NN`, `B-PROCEDURAL`, `B-EMPTY`
  (mandated baselines), `PC-EXACT-REPLAY` (positive control), `B-CROSS-SESSION-COMPILE`
  (disclosed identity control), `NC-MECHANISM-OFF` + `NC-REPEAT-INPUT` +
  `NC-EXAMPLES-ISOLATION` + `NC-CEILING-BAND` (null/sensitivity/band controls).
* **Metric.** `M-COST-PER-VERIFIED-SAFE-SUCCESS(arm, family, novelty) = (http_requests +
  retrieval_calls + verification_calls + repair_attempts) / (# VERIFIED SAFE successes)`,
  at matched correctness (`>= 0.80` floor), over the residual-novelty grid and both
  family lengths. A VERIFIED SAFE success is a task whose commit returned 200 for the
  expected value with no leak.
* **Decision rule.** `SUPPORTS` iff `T-MULTIRES` is strictly cheapest than **all four**
  baselines at every scored cell **and** `M-NOVELTY-GROWTH > 0` **and**
  `M-LENGTH-GROWTH <= 0`; `FALSIFIES` if not strictly cheapest than `B-PROCEDURAL` or
  the growth pattern fails; `MIXED` if it dominates only the memorization baselines;
  `MEASUREMENT_INVALID` on any V1–V8 gate failure.

## 3. Pre-freeze satisfiability attack (required; independently executed)

| Failure mode | Present? | Evidence |
|---|---|---|
| treatment/comparator identity | **YES** | §4.1–§4.2 |
| unreachable positive branch | **YES** | §4.3, §5 |
| arithmetic impossibility | **YES** | §4.3 (growth = 0.0; degenerate n=2 statistic) |
| ceiling/floor baselines | **YES** | novelty 0.0/0.25 all arms 1.0 (frozen matrix) |
| insensitive controls | no (live sub-contrast only) | `NC-MECHANISM-OFF` fires; distinctness ≥ 2 dims |
| missing prerequisites | no | substrate certified; carrier present |
| unbound mutable artifacts | N/A | not freezing; workspace search finds no V3 harness files |

Cheap non-outcome-bearing probes actually run at DESIGN for this request: (P1) verified
HEAD/base, hashed the current carrier (`3a6caf97…`) and checked a clean tree; (P2)
re-read the frozen V3 `result.json` success matrix, per-instance counters, gates and
determinism flag and recomputed every number in §5; (P3) read the carrier's
`distill_parameterized` implementation to settle the capability question from code, not
memory; (P4) screened the legacy brief/index and read targeted primary-source sections
from the mounted pre-2.0 archive (§6: blind-composition F1/F2; economics withdrawal).
No outcome-bearing measurement was run or inspected for this experiment.

## 4. Identifiability analysis (decisive)

### 4.1 Counter-invariance lemma

All four counters are functions of the HTTP protocol call sequence plus fixed per-task
verification increments; local representation build/inference/reuse/composition cost is
**not instrumented**. To answer the unique chain task correctly, any
mechanism-containing representation must execute the same minimal call sequence (one
calibration session + `K` calibration task/commit calls + one scored session + `K`
scored task calls + `K` scored commit calls). Therefore **any two mechanism-containing
representations are counter-identical**. Frozen measured
(`metrics.per_instance_counters_at_0.5`, re-read for this request):

| cell | `T-MECHANISM-INHERIT` | `B-CROSS-SESSION-COMPILE` | `PC-EXACT-REPLAY` |
|---|---|---|---|
| F1 (http/retr/ver/rep) | 34/0/16/0 | 34/0/16/0 | 34/0/16/0 |
| F2 (http/retr/ver/rep) | 42/0/20/0 | 42/0/20/0 | 42/0/20/0 |

`V8_identity_disclosure = true` is the runtime's own recorded measurement of exactly
this identity.

### 4.2 The mandated "compiled procedural lookup" baseline is the treatment

Under the only reading that makes `B-PROCEDURAL` a **strong** baseline (it
generalizes), it recovers `(a, b)` from the labelled calibration examples and applies
them — which *is* the runtime's `T-MECHANISM-INHERIT`: success-identical (1.0) and
counter-identical (per-instance totals F1 50, F2 62) at every scored cell. Under the
exact-key reading it duplicates `B-FLAT-CACHE` (0.875/0.900). A deliberately partial
generalizer would be a strawman baseline forbidden by POLICY's strongest-fair-baseline
rule. In no fair specification does a `T-MULTIRES`-vs-`B-PROCEDURAL` advantage exist.

### 4.3 The novelty-growth prediction is arithmetically false in both dimensions

The scored session contains **exactly one** chain task at *both* scored novelties, so
memorization comparators score exactly `(K-1)/K` at 0.50 **and** 0.75 while the
treatment scores 1.0 (frozen matrix, re-read). Margin `= 1/K` at both points. Cost per
verified safe success (recomputed at DESIGN from frozen counters):

| cell | T total / succeeds / cost-per-safe | flat total / succeeds / cost-per-safe | ratio |
|---|---|---|---|
| F1 @0.50 and @0.75 | 50 / 8 / 6.2500 | 53 / 7 / 7.5714 | 1.2114 |
| F2 @0.50 and @0.75 | 62 / 10 / 6.2000 | 65 / 9 / 7.2222 | 1.1649 |

`M-NOVELTY-GROWTH = 0.0` exactly at both families (fails mandated `> 0`); with `n = 2`
tied scored points any rank statistic is degenerate (permutation `p = 1.0`). The
advantage **decreases** in task length `K` (margin 0.125 → 0.100; ratio 1.2114 →
1.1649) — the exact opposite of the mandated novelty-driven, length-invariant pattern.
NN totals (F1 61/7 = 8.7143; F2 75/9 = 8.3333) and empty-registry totals (F1 58/7 =
8.2857; F2 72/9 = 8.0000) confirm T dominates the memorization trio strictly — the
already-certified result, not news.

### 4.4 The live contrast is already certified

`EXP-RUNTIME-38194351940` (`status=COMPLETE`, `outcome=SUPPORTS`,
`decision_label=ROBUST`, audit `PASS`, `determinism_ok=true`, all gates true) already
measured mechanism-containing inheritance (1.0) vs memorization (`(K-1)/K`) with the
full matrix, counters, distinctness and novelty grid in frozen evidence. A new EXECUTE
would re-derive existing numbers at ~15–40 minutes for zero information gain.

## 5. Derived decision table (answers the mandate's economic question without EXECUTE)

Deterministic arithmetic on frozen evidence (see `spec.json#derived_decision_table` for
the full table): T strictly cheaper per verified safe success than the memorization
trio at both scored cells (ratios 1.2114/1.1649), **ties** `B-PROCEDURAL`-generalizing
(6.25 vs 6.25; 6.20 vs 6.20), `M-NOVELTY-GROWTH = 0.0`, length pattern opposite to
prediction. **Branch entailed: FALSIFIES** (with the MIXED sub-contrast — dominance
over memorization — simultaneously entailed as the already-certified ROBUST result).
No branch of a new EXECUTE could change a product decision.

## 6. Legacy comparison (targeted primary-source reads, not wholesale ingest)

* **P2-REPLAY-COST (4.114, sha `9687ff78…`).** 8.5× withdrawn to 1.002× on 3 matched
  tasks; scripted agents on live sites; 69.6% reuse POC with hand-specified subgoals.
  Never raced representation baselines on cost per verified-safe success. Guards
  replicated here: matched cells, fully loaded costs. Targeted archive reads confirm
  the economics-withdrawal language (economics gates PASS yet "do not license a
  work-compression claim"; repeat-cell phrase "UNSUPPORTED … and is withdrawn here").
* **P2-BLIND-COMPOSITION (4.697, sha `017a80ae…`).** 3/3 vs 0/3 with keyword/oracle
  confounds and weak baselines. Guard replicated here: no oracle stopping; strongest
  fair baselines. Targeted archive reads confirm finding F1 (content-derived addressing
  beats replay/cold on identical knowledge; BFS has no edges beyond trained prefixes)
  and limitation F2 (ordinal/positional goals UNADDRESSABLE).
* **P2-MIND2WEB.** 6/176 exact matches, 4/176 strict causal chains, 47/176 retrieval;
  consistent with requiring strong baselines; no matching compression-economics test.

**Classification: LEGACY: DISTINCT_EXTENSION.** Material difference: real certified
non-ceiling bank, shipped executable carrier, four honest counters, controlled novelty
grid, strong internal baselines. Rigorous replication: matched comparisons, fully
loaded counterfactual costs, no oracle stopping. The degenerate structure is a
Research-2.0 instrument property of V3, not a pre-2.0 repeat. No identical
invalid/degenerate EXECUTE is repeated — the prior siblings' failure is re-verified,
not re-run.

## 7. Minimal re-scope (proposed to the Global Research Director; NOT adopted silently)

* **R1 — make the structure live (representation-economics goal).** Authorize a substrate
  with *genuinely decomposable* structure and/or an instrumented local
  representation-cost dimension (build/compile/inference/reuse). Frozen network-only
  counters cannot represent any local representation effect.
* **R2 — derive, do not re-run (product-economics goal).** Done in §5 above: adopt the
  derived cost-per-verified-safe-success table in a DIRECTOR/analysis step.
* **R3 — residual-novelty mechanism goal needs a new bank.** Testing "advantage grows
  with residual novelty" requires a monotone chain-count ladder (e.g. 1..m chain tasks
  per session); V3 has exactly one per scored session. This contradicts the mandate's
  "frozen V3 bank only" batch limit, so it needs explicit Director authorization.

## 8. Consequence of each outcome (decision counterfactual)

* **Win (SUPPORTS):** unreachable as specified — would have justified investing in a
  decomposable/multi-resolution inherited representation and keeping
  `C-RESIDUAL-NOVELTY` as a flagship discriminator.
* **Lose (FALSIFIES, entailed):** the multi-scale representation/work-compression moat
  is **UNPROVEN on this substrate and must not be assumed** (POLICY: "do not assume
  graph structure saves tokens"); the only evidenced lever is inheritance-vs-
  memorization (generalization), already certified; the flagship's residual-novelty
  mechanism stays untested pending R1/R3.
* **Invalid (MEASUREMENT_INVALID):** instrumentation/prerequisite defect — not the case
  here (all V1–V8 gates frozen true).

## 9. Freeze eligibility verdict

| check | status | reason (abridged) |
|---|---|---|
| `decision_rule_reachability` | **FAIL** | SUPPORTS unreachable (T ≡ B-PROCEDURAL-generalizing); growth requirement arithmetically impossible; FALSIFIES entailed a priori |
| `measurement_prerequisites` | PASS | substrate certified/deterministic; carrier present at `3a6caf97…`, clean tree (bank harness on `origin/lab2/runtime`, reconstruct byte-faithfully if ever run) |
| `baseline_identifiability` | **FAIL** | `B-PROCEDURAL` inseparable from `T-MULTIRES` on this instrument |
| `control_sensitivity` | PASS | sensitive for the live sub-contrast only; none separates two mechanism-containing representations |
| `treatment_liveness` | **FAIL** | two-horn failure: abstract treatment has no distinct executable; named carrier arithmetically incapable |
| `freeze_artifacts_bound` | NOT_APPLICABLE | not freezing; no new mutable artifact; no V3 harness files in workspace |

`freeze_artifacts = []`. The design is **not freeze-eligible**.

## 10. What was done at DESIGN (and what was not)

* **Done (non-outcome-bearing):** read the exact mandate and parent handoff (four-way
  state preserved in `spec.json`); read the frozen `EXP-RUNTIME-38194351940` packet
  (`result`/`gates`/`determinism`); verified HEAD/base, hashed the current carrier and
  checked a clean tree; read the carrier's `distill_parameterized` implementation;
  screened the legacy brief/index and read targeted primary-source sections from the
  mounted pre-2.0 archive; recomputed the full decision table from frozen numbers.
* **NOT done:** no outcome-bearing measurement for this experiment; no harness
  authored or executed; no files frozen; no code written or promoted; no claim advanced;
  no drift back to the parked B11 handoff; no silent re-scope adopted.

## 11. Evidence references

* `research/experiments/EXP-PRODUCT-38315290076/request.json` (mandate,
  `design_contract_version=2`, base `8094b348…`)
* `codex/experiments/EXP-RUNTIME-38194351940/result.json`
  (certified V3; success matrix, per-instance counters, gates, determinism)
* `research/experiments/EXP-PRODUCT-37989728440/` (prior C-RESIDUAL-NOVELTY
  certificate failure on the mandatory-discovery REST class)
* `research/experiments/EXP-PRODUCT-38234098353/handoff.json` (parked parent state)
* `research/experiments/EXP-PRODUCT-38244439628/` and
  `research/experiments/EXP-PRODUCT-38291106470/` (sibling DESIGN-failure packets on
  the same mandate question; re-verified here, not copied as authority)
* `src/spider/kernel.py` (shipped carrier, sha256 `3a6caf97…`)
* Mounted pre-2.0 primary sources: `SPIDER_CODEX_ULTIME.md` blind-composition and
  economics-withdrawal sections (targeted reads); `codex/legacy_brief.json`;
  `codex/legacy_artifact_index.json`
* `research/EXPERIMENT_PACKET.md` §2 (v2 treatment liveness; mandate refinement bounds;
  fail-loud rule) and §3 (spec fields); `research/portfolio/POLICY.md`
  (decision counterfactual; strongest fair baseline; non-duplication check)
