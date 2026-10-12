# EXP-GRAPH-38180711589 — EXECUTE report

- **Lane:** graph
- **Claim:** C-SEMANTIC-RESOLVE (bounded sub-mechanism only)
- **Status:** COMPLETE
- **Outcome:** FALSIFIES (D-PRIMARY = GATE-NOT-MET); D-ALTLEX = BLOCKED, D-HELDOUT = BLOCKED
- **Primary metric:** M-GATE-TRIPLET-PRIMARY
- **Frozen runner:** `prereg.md#FROZEN-RUNNER`, sha256 `5811a49524a012ba25483d61f78a0d696ccc82f0971386507217c0d9e2c9d6e5`, exit 0
- **Raw evidence:** `raw_evidence/runner_result_raw.json` (sha256 `860f9dbe…`)

## 1. What was executed

The frozen stdlib-only runner was extracted verbatim from the hash-bound
`prereg.md` (V12-B PASS, block sha == file sha) and executed unchanged. It builds
the three axes, screens contamination, calibrates the integer ambiguity signal
`S` on a disjoint calibration split, and scores the test split. All frozen input
hashes and all eight CANONICAL-HASHES blocks were re-verified before scoring
(V4/V12); the frozen runner does not emit the PC/NC/baseline/V-gate checks, so
those were computed by an EXECUTE-side harness (`execute_controls.py`) from the
same frozen runner functions and the same model-free arm definitions in
`research/harness/candidate_resolver.py`. No number in this packet is re-typed;
`result.json` is assembled from raw evidence by `assemble_result.py`.

## 2. Primary result (D-PRIMARY)

AXIS-PRIMARY bound set: **113 applicable**, **38 out-of-scope** (160-goal bank
minus 9 V3 flags — 7 applicable, 2 out-of-scope), exactly reproducing the frozen
DESIGN counts. Calibration is `CAL-FEASIBLE` at **t\* = 0**.

| metric (test split @ t\*=0) | value | target | met |
|---|---|---|---|
| pooled_false_accept | **0.1667** (3/18) | ≤ 0.10 | **NO** |
| coverage | **0.9464** (53/56) | ≥ 0.50 | yes |
| unknown_precision | **1.0000** (2/2) | ≥ 0.85 | yes |
| unknown_precision_inclusive | 0.8333 | diagnostic | — |
| selective_acc (executed) | 0.9057 | — | — |
| executed / abstained-resolved / unresolved-applicable | 56 / 2 / 3 | — | — |

The calibration split itself was feasible (coverage 0.8596, pooled_false_accept
**0.1000**, unknown_precision 1.0000), but the disjoint test split misses the
false-accept target by 0.0667. The gate abstains on only 2 resolved test goals
(both out-of-scope) plus 3 structurally unresolved applicable goals, so the
`unknown_precision = 1.0` is carried by 2 abstentions.

**Decision: GATE-NOT-MET.** All D-PRIMARY-invalidating validity gates PASS
(V2, V3, V5, V6, V7, V8, V9, V10, V13; V12 PASS; V11 NOT_APPLICABLE — the
retention bootstrap was never attempted). Under the frozen precedence this is a
valid scientific negative, not a measurement failure, so `status=COMPLETE` and
`outcome=FALSIFIES`.

## 3. Controls, nulls and baselines

| id | observed | expected | verdict |
|---|---|---|---|
| PC-LIVENESS-AND-INTEGRITY | fixture uniqueness 20/20; incumbent verbatim 20/20; resolver self-match 20/20 | 3×20/20 | PASS |
| NC-SHUFFLED-LABEL | 5/113 = 0.0442 (fixed derangement, seed 3820973221) | ≤ 0.20 | PASS |
| NC-CONSTANT-SIGNAL | t\*=1 (`CAL-ABSTAIN-ALL`), unknown_precision = None | not ≥ 0.85 | PASS |
| CTRL-EXEC-ALL (= B-LEX-ONLY) | cov 0.9464, FA 0.2778 | precision floor | observed |
| CTRL-ABSTAIN-ALL | cov 0.0, FA 0.0 | coverage floor | observed |
| CTRL-RANDOM-GATE (18 matched abstentions) | FA 0.7222, unknown_precision 0.2778 | must not reach treatment precision | observed |
| B-LEXTOK-JACCARD | 10/113 = 0.0885 | near/below chance | observed |
| B-RANDOM-ROLE (RandomState 4242) | 21/113 = 0.1858 | ≤ 0.35 | PASS |
| B-INCUMBENT-KERNEL | 0/113 = 0.0 | 0.0 by construction | observed |
| B-INTERNAL-ID-ORACLE | 113/113 = 1.0 | 1.0 | PASS |
| A-EMBED-COSINE | could not load (ModuleNotFoundError) | structurally live | UNKNOWN / BLOCKED |

The treatment is live (V7: 102 executed applicable, strictly between 0 and 113)
and non-tautological (V9: B-LEX-ONLY and T-LEX-AMBIG execution vectors differ on
9 primary goals; the frozen source references no embedder token before the
optional retention block at line 285). The gate reduces B-LEX-ONLY's test
false-accept rate from 0.2778 to 0.1667 but does not reach 0.10.

B-LEX-STRONG selection accuracy on the primary applicable set is
**97/113 = 0.8584** (test split 48/56 = 0.8571), confirming the parent's
selection finding is intact on this axis.

## 4. Secondary retention (D-ALTLEX / D-HELDOUT)

The pinned embedding comparator (`sentence-transformers/all-MiniLM-L6-v2`) could
not be loaded at EXECUTE, so the paired family-blocked bootstrap was never run
and both retention decisions are **BLOCKED** — pre-declared as allowed and
independent of D-PRIMARY (V11 NOT_APPLICABLE). The deterministic sides remain
computable and are reported without the comparator:

| axis | t\* | coverage | pooled_false_accept | unknown_precision | B-LEX-STRONG acc (test) |
|---|---|---|---|---|---|
| AXIS-ALTLEX | 0 | 0.9464 | 0.1667 | 1.0000 | 0.9464 |
| AXIS-HELDOUT | 0 | 0.9750 | 0.2000 | 1.0000 | 0.9750 |

`M-EMB-ACC-*` and `M-PAIRED-DIFF-DET-MINUS-EMB-*` are `null`.

## 5. Contamination and set sizes

- `M-N-PRIMARY-APPLICABLE` = 113; `M-N-PRIMARY-OOS` = 38; calibration 57/20, test 56/18.
- `M-N-CONTAM-FLAGGED` = 9 (≤ 20, V3 PASS); `M-CONTAM-MAX-JACCARD` = token 0.5714 (< 0.60), trigram 0.5882 (< 0.75).
- AXIS-HELDOUT 0 flags.

## 6. Interpretation and product consequence

Within the frozen scope, no model-free ambiguity gate reaches the operating
point on this fixture: the deterministic resolver's own integer signal
`S = 1[famNONE]+1[opNONE]+1[opTIE]+1[noslot]+1[quant]` supplies too few
abstentions on the test split to bring pooled false-accept below 0.10. This is
the negative branch the frozen `product_consequence_negative` names: `resolve()`
must not ship deterministic-plus-gate for unseen goals on this evidence, and the
next step is an architectural change (structured slot/parameter reasoning, or a
retrieval model trained on independently authored goals) rather than another
threshold re-tune. C-SEMANTIC-RESOLVE is **not** promoted; the parent's 97/113
selection number is corroborated but is not load-bearing, and the retention
advantage remains unmeasured (BLOCKED). This report does not exceed the frozen
claim and does not contradict `result.json`.

## 7. Validity notes (summary; full list in `result.json`)

- The embedding stack is unavailable; only the secondary retention checks are affected.
- The raw runner snapshot shows embedding_status `No module named numpy` because it ran before numpy was bootstrapped; numpy was used only by the EXECUTE-side harness.
- The EXECUTE-side harness re-implements the model-free arms in stdlib/numpy because `candidate_resolver.py` imports the unavailable stack at module top; it is used only for controls/baselines, never for the D-PRIMARY decision.
- The frozen `CAL-ABSTAIN-ALL` fallback label is observed as-is (t\*=max(S)+1 executes all resolved goals under `EXECUTE iff S<=t`); it is not repaired post hoc.
- `unknown_precision_inclusive` is a secondary diagnostic, not the primary metric.
