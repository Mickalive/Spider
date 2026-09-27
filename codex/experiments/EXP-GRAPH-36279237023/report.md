# EXP-GRAPH-36279237023 — EXECUTE report

**Lane:** graph · **Claim under test:** `C-SEMANTIC-RESOLVE`
**Status:** `MEASUREMENT_INVALID` · **Outcome:** `INCONCLUSIVE`
**Execution base:** commit `7f5879fc` · **CI run:** `36279237023`

---

## 1. Verdict in one paragraph

The frozen design could not be executed compliantly, and it failed for a reason that has nothing to do with the
candidate: **V9 requires outcome-bearing code to be hashed into the freeze, and `freeze.json` hashes three design
documents and zero code files.** The only freezer in the repository, `scripts/freeze_experiment.py`, is outside the
graph lane's allowed code roots, and `freeze.json` is immutable. `prereg.md` §7.1 evaluates measurement validity
first and short-circuits, so the packet's status is `MEASUREMENT_INVALID`.

That status is a statement about the validity of the measurement *transaction*, not a scientific negative. So this
report also reports every gate in full, because discarding them would throw away real measurements. The short version
of what was measured: **the candidate did not beat the lexical null, and it lost to an uncalibrated baseline that
does strictly less.** On the frozen primary metric the candidate scored `36/52 = 0.6923` against the lexical null's
`36/52 = 0.6923` — an exact tie, `p = 0.5943` — while the declared substitute leg `A-REFERENCE-EMBEDARGMAX` scored
`45/52 = 0.8654`. Four of the nine secondary gates fail.

## 2. Why `MEASUREMENT_INVALID` and not a clean negative

| condition | verdict | note |
|---|---|---|
| V1–V8 | PASS | see `result.json.frozen_decision_rule_evaluation.measurement_validity_conditions` |
| **V9 code hashed into freeze** | **FAIL** | `freeze.json` lists 3 files, all design documents, 0 code files |
| V10, V11 | PASS | 5 family blocks × 10 000 resamples; fixture discrimination verified |

The V9 failure is structural: no execution of *this* design, by *this* lane, at *any* time, could have passed it. I did
not repair it. Repairing it would have meant either editing an immutable frozen file or editing an out-of-scope
script, and both are prohibited. The per-file `sha256` values in `result.json.artifacts` are recorded so an auditor
can verify which code produced the evidence; they are explicitly **not** offered as satisfying V9.

Recorded separately, and independently of V9:

| gate | verdict | observed |
|---|---|---|
| degeneracy screen (V8) | PASS | lexical 0.45 on all 80 vs 0.90 threshold; substitute leg non-empty |
| PC-VERBATIM-INTENT | PASS | 12/12 correct, 0 false accepts |
| oracle ceiling | PASS | 52/52 |
| NC-NO-APPLICABLE | PASS | 8/8 abstained |
| calibration fitted (V4) | PASS | `w = 2.6927`, `b = 0.1853`; `w` moves across refits (spread 1.1230) |
| **primary** | **FAIL** | vs lexical: Δ = 0.0, one-sided lower 95% = −0.0652, `p = 0.5943` |
| **secondary** | **FAIL** | 4 of 9 fail: `pooled_false_accept`, `unknown_precision`, `ece_global`, `ece_per_class_max` |

## 3. The primary result is a cancellation, not a tie

This is the most decision-relevant thing in the packet, and it is *not* what the headline number suggests. The two
arms win different goals in almost equal number, but the per-category decomposition shows why:

| category | n (applicable) | A-CANDIDATE | B-LEXICAL-OVERLAP | A-REFERENCE-EMBEDARGMAX | candidate − lexical |
|---|---|---|---|---|---|
| verbatim | 12 | **12/12** | 12/12 | 12/12 | 0 |
| paraphrased | 20 | **19/20** | 15/20 | 19/20 | **+4** |
| underspecified | 10 | **0/10** | 5/10 | 9/10 | **−5** |
| composite | 10 | 5/10 | 4/10 | 5/10 | +1 |
| **total** | **52** | **36/52** | **36/52** | **45/52** | **0** |

The semantic route is **genuinely better than lexical overlap on paraphrase** — the actual generalisation test — by
four goals. That gain is then entirely destroyed by the `underspecified` category, where the candidate abstains on
all 10 and scores zero, while lexical gets 5 and the uncalibrated baseline gets 9.

The exact `0.0` pooled tie is a compositional cancellation of `+4`, `−5` and `+1`. It is not evidence that the two
arms are equivalent. Contingency counts agree: both correct on 29, candidate-only on 7, lexical-only on 7, neither
on 9.

Two further facts sharpen this. First, the candidate's correct set is a strict **subset** of the uncalibrated
argmax's: 36 shared, 0 candidate-only, 9 argmax-only. The fitted gate never helps selection and sometimes loses it.
Second, the whole deficit against `A-REFERENCE-EMBEDARGMAX` is the 10 `underspecified` goals; on paraphrased and
composite the candidate ties it.

## 4. The calibrated gate is inert, and that explains the ECE failures

The gate was genuinely fitted — logistic coefficients learned by maximum likelihood on a train split, moving across
independent refits, so it is not a fixed algebraic transform of `cos_sim`. It is also **completely inert**:

- fitted `p` over the 52 applicable goals spans **0.6785 – 0.9468**;
- the selected threshold is **0.02**;
- **0 of 52** goals fall below it.

So **all 28 candidate abstentions came from the parameter slot filler, not from the gate** (`abstain_reason =
unfilled_parameter_slots` on every one). This has three consequences that matter more than the gate verdicts
themselves:

1. **The ECE gates are not clean tests of the candidate's decision rule.** Global ECE `0.2030` and ABSTAIN-class ECE
   `0.7885` are computed over rows the gate never decided. They score the slot filler's abstentions against a
   confidence the gate never acted on. The gate's formal "fittedness" passes while the thing actually abstaining is
   uncalibrated by construction.
2. **Inertness is not an artifact of the threshold-selection rule.** A post-hoc diagnostic maximising the *accept*
   class F1 instead of the frozen commit/abstain F1 also selected `t = 0.02`, and every threshold in `(0.02, 0.68]`
   would abstain on 0 of 52 goals. It is a property of the fitted coefficients on this fixture.
3. **The gate costs accuracy and buys nothing.** Under `prereg` §6.1 an abstention is an incorrect outcome, so each
   abstention costs a mechanism-identity point, while contributing nothing to the pooled false-accept gate.

`UNKNOWN precision` is `0.6071` (17 TP / 11 FP) against a 0.85 requirement. Note this is genuinely a precision over
abstentions, verified by unit test — not an OOD abstention rate, which the parent packet conflated.

## 5. A defect I introduced, disclosed rather than repaired

**The coded `false_accept_rate` is computed on inconsistent denominators across arms.** All four defensible readings
of the frozen phrase "pooled false-accept rate":

| arm | R1 wrong/applicable | R2 wrong/all-80 | R3 wrong/applicable-executable | coded value |
|---|---|---|---|---|
| A-CANDIDATE | **5/52 = 0.0962** | 16/80 = 0.2000 | 5/41 = 0.1220 | **16/52 = 0.3077** |
| A-REFERENCE-EMBEDARGMAX | 7/52 = 0.1346 | 35/80 = 0.4375 | 7/52 = 0.1346 | 0.4375 |
| B-LEXICAL-OVERLAP | 16/52 = 0.3077 | 44/80 = 0.5500 | 16/52 = 0.3077 | 0.5500 |
| B-RANDOM-ROLE | 45/52 = 0.8654 | 73/80 = 0.9125 | 45/52 = 0.8654 | 0.9125 |

The coded value equals R2 for every arm **except** the candidate, where it equals R4 — a hybrid pairing an all-80
numerator with an applicable-only denominator. It is the only such cell in the table and the most pessimistic one.

**The false-accept gate verdict is therefore interpretation-dependent**: R1 gives the candidate `0.0962`, which
**passes** 0.10, while the lexical null scores `0.3077` and fails. R2, R3 and R4 all fail. I found this after the
outcomes were visible and did **not** repair it, because changing a metric after seeing the outcome is precisely
what the freeze exists to prevent. The gate is reported as coded and flagged
`interpretation_dependent: true`.

This is the **only** gate whose verdict depends on that choice. UNKNOWN precision, global ECE, per-class ECE and the
primary gate all fail under every reading, so nothing in the packet's conclusion rests on the ambiguity.

## 6. What the frozen metrics structurally cannot see

On the 20 `ood` goals — which have **no applicable mechanism at all** — the candidate produced **11 EXECUTABLE
decisions** at `p` between 0.6925 and 0.8407 (mean 0.7787), and abstained on 9. Those 11 wrong executions:

- carry no weight in the primary metric, which only scores the 52 applicable goals;
- carry no weight in the pooled false-accept numerator under reading R1;
- carry no weight in either ECE gate, because the gate is fitted only on goals that *have* an applicable mechanism.

So the candidate's most product-relevant failure mode — confidently executing against a mechanism that does not
exist — is invisible to every frozen gate. This is a metric-suite gap, not an implementation bug.

Two further structural gaps:

- **V8a is non-binding by construction.** The headroom screen is computed on all 80 goals, but 28 have no applicable
  mechanism, capping any arm at `52/80 = 0.65`. It cannot detect lexical adequacy, and the lexical null is far
  stronger than the screen anticipates: 36/52, including 12/12 verbatim and 15/20 paraphrased.
- **The primary metric penalises conservative behaviour.** It scores abstention as incorrect, which costs the
  candidate all 10 `underspecified` goals for declining to guess.

## 7. Controls and baselines

| id | role | verdict | evidence |
|---|---|---|---|
| `PC-VERBATIM-INTENT` | positive control | **PASS** | 12/12 correct, 0 false accepts |
| `NC-NO-APPLICABLE` | null control | **PASS** | 8/8 abstained, 0 EXECUTABLE |
| `B-LEXICAL-OVERLAP` | strong null | **PASS as screen condition, weak as a null** | 36/52; beats the 0.90 screen by construction alone |
| `B-RANDOM-ROLE` | chance null | **PASS** | 7/52 = 0.1346, *below* the 0.2 chance level |
| `B-INTERNAL-ID-ORACLE` | difficulty ceiling | **PASS** | 52/52; ceiling is reachable, so 0.6923 is a real gap |
| `A-INCUMBENT` | incumbent leg | **EMPTY** | 0/80 EXECUTABLE, all UNKNOWN |
| `A-REFERENCE-EMBEDARGMAX` | declared substitute | **PASS, and stronger than the candidate** | 45/52 = 0.8654 |

Two control caveats the auditor should not skip:

- **PC descriptive expectation missed by 0.0532.** The prereg expects ECE = 0.0 for a perfect control. All 12
  verbatim goals bind and select correctly, but every one carries `p = 0.9468`, not 1.0, because `cos = 1.0` maps
  through the fitted gate to 0.9468. Observed descriptive ECE is `0.0532`. The control's *decision* gate (accuracy
  = 1.0, denominator > 0) is met. UNKNOWN precision is vacuously 1.0 — the arm never abstains here.
- **NC passed for the wrong reason.** All 8 abstentions came from the slot filler, not the calibrated gate, which
  abstained on 0 of them.
- **The incumbent leg is empty by code certainty, not by measurement.** `kernel.py:resolve()` requires exact
  intent-string equality *and* all template slots present in the supplied params; V11 forbids empty
  `parameter_slots`, and this arm supplies `params={}`. The prereg's own expectation that the incumbent's
  mechanisms carry `parameter_slots=[]` contradicts V11 inside the same frozen document.

## 8. Measurement hygiene — what this run did fix

Independently of the claim, this run repairs a defect recorded against the parent experiment
`EXP-GRAPH-36272373909`:

- **Byte-reproducible.** Two independent full executions produced byte-identical
  `raw_evidence/task_results.jsonl` and byte-identical `derived_evidence/*`. The only field that varies anywhere is
  `wall_clock_seconds`. The parent's unseeded `uuid4` made its numbers irreproducible; all five seeds
  (`36279237023` goals, `20260926` arm order, `990017` split, `4242` random role, `36279237023` bootstrap) are now
  fixed and logged.
- **State isolation verified.** All 80 tasks began from a single identical state hash
  (`89172fde…`), with the store reset before every arm request.
- **Order effects controlled.** 78 distinct arm orderings across 80 tasks, against a frozen minimum of 43.
- **Estimators unit-tested before use.** Closed top-bin ECE and the TP/FP UNKNOWN-precision definition are each
  verified by an explicit test, run as the V5/V6 precondition. The UNKNOWN-precision test confirms a single
  abstention on an applicable goal scores 0.0, i.e. it is *not* an OOD abstention rate.

These are operational improvements to the measurement substrate. They are **not** evidence about
`C-SEMANTIC-RESOLVE`.

## 9. What I am not claiming

- I am **not** claiming `C-SEMANTIC-RESOLVE` is refuted. The packet is `MEASUREMENT_INVALID`; a VALIDATED or
  REJECTED promotion cannot rest on it.
- I am **not** claiming the semantic route is worthless. §3 shows a real +4-goal gain over lexical on paraphrase.
  The candidate's design, not the semantic mechanism, is what failed.
- I am **not** claiming the uncalibrated baseline is the answer. `A-REFERENCE-EMBEDARGMAX` never abstains and
  executes on all 20 `ood` goals, so it is not shippable. It is a ceiling on what the embedding signal alone
  provides.
- I am **not** repairing the V9 failure or the false-accept denominator, and I have not weakened any threshold,
  preregistered criterion or gate after seeing outcomes.
- I am **not** treating the per-category decomposition in §3 as a preregistered analysis. It is a diagnosis offered
  from the raw rows, and it did not alter any gate verdict.

## 10. Open questions for the Director

1. **Re-freeze or re-design?** The evidence points at re-design, not re-freeze. A new freeze that hashes code would
   repair V9 and change nothing else: the gate is inert, the false-accept metric is ambiguous, the safety-relevant
   OOD failures are invisible to the frozen gates, and the primary failure decomposes into a category-specific
   abstention policy.
2. **If re-designed, the highest-information change is a negative class in the calibration set.** The candidate fires
   on 11 of 20 goals that have no applicable mechanism, and the frozen fitting set contains no negative examples, so
   the gate can never learn to abstain on them. This is the one change that would let the frozen metric suite even
   see the failure it most needs to see.
3. **The metric suite needs a definition of "pooled false-accept"** that fixes the numerator/denominator pairing and
   counts executions on goals with no applicable mechanism. Both current readings let real false accepts through.
4. **The applicable-goal count remains unresolved** (52 vs the prereg's arithmetically inconsistent 60). Every
   denominator in this packet depends on it.
5. **The 0.15 ECE / 0.85 UNKNOWN-precision targets are not currently reachable by any abstaining design on this
   fixture**, because abstention is uncalibrated while non-abstention is scored for confidence. Whether those targets
   are the right targets is a design question, not a tuning question.

---

### Packet index

`result.json` (authoritative) · `provenance.json` · `derived_evidence/gate_table.json` (machine-derived frozen gate
table) · `raw_evidence/task_results.jsonl` (480 raw rows) · `derived_evidence/metrics.json` ·
`derived_evidence/calibration.json` · `derived_evidence/degeneracy_screen.json` ·
`derived_evidence/design_facts.json`

**This report interprets `result.json`; it does not exceed it. Where the two could be read as differing,
`result.json` governs.**
