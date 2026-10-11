# EXP-GRAPH-38175554380 — EXECUTE report

Lane: `graph`. Claim: `C-SEMANTIC-RESOLVE` (unchanged status HYPOTHESIS; only a DIRECTOR verdict may move it).
Design contract: v2. Frozen experiment id: `EXP-GRAPH-38175554380`.

Canonical machine handoff is `result.json` (plus `provenance.json` and the derived/raw artifacts). This
report explains and interprets; it does not extend the frozen claim and does not override `result.json`.

## 1. What was run

The frozen runner embedded in `prereg.md` (`<!-- BEGIN FROZEN RUNNER -->` … `<!-- END FROZEN RUNNER -->`)
was extracted verbatim to `run_experiment.py` and executed once from the repository root:

```
python3 research/experiments/EXP-GRAPH-38175554380/run_experiment.py
```

Exit code 0. Console output is preserved at `raw_evidence/runner_stdout.txt` and
`raw_evidence/runner_stderr.txt`. The runner re-verified its own source against the frozen block (V12-B),
the `prereg.md` hash against `freeze.json` (V12-A), all eight `freeze.json.artifact_hashes` (V12-C), and
each embedded data block against the `CANONICAL-HASHES` block (V4). All V1–V12 validity gates PASS;
`V13-GATE-VALIDITY` is true (both split classes non-empty).

The CPU scientific stack was installed to match the parent packet's recorded pins: python 3.12.15,
numpy 1.26.4, scipy 1.17.1, scikit-learn 1.5.1, torch 2.4.0+cpu, sentence-transformers 3.0.1. This is
the bootstrap the frozen `estimated_cost` anticipated; it succeeded, so status is COMPLETE, not BLOCKED.

Frozen setup: a 160-goal independently authored bank (120 applicable = 5 families × 4 CRUD ops × 6
phrasings; 40 out-of-scope), a bank-blind fixed operation-synonym + resource-noun lexicon, a
contamination screen over 248 prior surfaces (token-Jaccard ≥ 0.60 OR char-trigram-Jaccard ≥ 0.75), and
a calibration/test split defined by within-cell phrasing index (cal 57 app/20 oos; test 56 app/18 oos).

## 2. RAW EVIDENCE (not interpretation)

- `derived/predictions.json` — per-goal selections for every arm plus embedding features.
- `derived/contamination.json` — max token/trigram Jaccard per goal against all prior surfaces.
- `derived/measurements.json` — full runner output (metrics, controls, gates, env).
- `derived/kernel_registry.jsonl` — the 20-intent fixture used by the incumbent kernel.
- `raw_evidence/runner_stdout.txt`, `raw_evidence/runner_stderr.txt`, `raw_evidence/environment.json`.

Screen: 9/160 goals flagged (`app_004, app_049, app_052, app_073, app_076, app_097, app_100, oos_024,
oos_026`), leaving `|primary| = 113`, exactly as the DESIGN structural probe predicted. All 5 families
are represented (users 23, posts 24, comments 22, albums 22, photos 22).

Arm accuracies on the primary set (numerator/denominator = 113):

| Arm | Accuracy | Notes |
| --- | --- | --- |
| `A-EMBED-COSINE` (treatment) | 78/113 = 0.6903 | 20 distinct valid selections (V7 live) |
| `B-LEX-STRONG` (**primary comparator**) | 97/113 = 0.8584 | 11 abstentions; 14/38 unflagged OOS false accepts |
| `B-LEX-STRONG-LEARNED` | 15/113 = 0.1327 | sensitivity only; disjoint test phrasings |
| `B-LEXTOK-JACCARD` | 10/113 = 0.0885 | parent weak null |
| `B-RANDOM-ROLE` | 19/113 = 0.1681 | floor (≤ 0.35) |
| `B-INCUMBENT-KERNEL` | 0/113 | structural (exact-intent equality) |
| `B-INTERNAL-ID-ORACLE` | 113/113 = 1.0 | structural ceiling |

Paired family-blocked bootstrap (5 families, B = 10000, alpha = 0.05, seed 3815816012):

- `M-PAIRED-DIFF-EMBED-MINUS-STRONGLEX`: obs_diff = **−0.1681**, 95% CI **[−0.3077, −0.0268]**.
- `M-PAIRED-DIFF-EMBED-MINUS-LEARNED` (sensitivity): obs_diff = 0.5575, 95% CI [0.3694, 0.7727].

The primary bootstrap was independently re-derived from `derived/predictions.json` with the frozen
`experiment_runner.paired_bootstrap` and the same seed; it reproduced the recorded triple exactly.

## 3. Direct observations

- `OBS-D-RESOLVER`: the paired difference is negative and the 95% interval lies strictly below zero.
- `OBS-D-GATE(2F)`: `GATE-NOT-MET` — `feasible=false`, `t*=1.0`, test coverage 0.0,
  pooled false-accept 0.0, unknown-precision 0.2432.
- `OBS-D-GATE(global)`: identical `GATE-NOT-MET` triplet.
- `OBS-NON-TAUTOLOGY`: the comparator disagrees with the treatment on 40/113 goals and abstains on 11.
- `OBS-CHECKPOINT`: the frozen revision `c9745ed1…` was unavailable; the runner fell back to the
  unpinned model and resolved `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, identical to the parent
  packet's resolved checkpoint.
- `OBS-ALL-GATES`: V1–V12 all PASS.

## 4. Derived measurement / decision

`D-RESOLVER` (claim-bearing, frozen rule): `FALSIFIES` because all gates that could invalidate the
primary metric PASS and `upper_ci ≤ 0`. Equivalently, on this frozen primary set the strong
deterministic lexical resolver exceeds the dense embedding argmax; the parent packet's measured 0.3978
advantage does not survive the replacement of the weak token-Jaccard null with the strong comparator the
Director mandate required.

`D-GATE` (secondary, decoupled, non-gating): `GATE-NOT-MET` for both `G-LOGISTIC-2F` and the global
single-threshold gate. Neither the two-feature gate nor the parent-style single-threshold gate could
reach the calibration objective `pooled_false_accept ≤ 0.10 AND unknown_precision ≥ 0.85`; the frozen
fallback therefore selected `t* = 1.0`, which abstains on everything (coverage 0.0). Per the frozen
decoupling this does **not** downgrade `D-RESOLVER` and does **not** make the packet
MEASUREMENT_INVALID.

Overall: `status = COMPLETE`, `outcome = FALSIFIES` (the `D-RESOLVER` outcome). A measurement-valid
scientific negative, not an infrastructure failure.

## 5. Interpretation (explicitly interpretation)

Within the frozen fixture scope — 20 mechanisms, 5 resource families, one 160-goal bank, one resolved
all-MiniLM-L6-v2 checkpoint — the embedding-max-cosine path is **not needed** for unseen-goal mechanism
selection: a fixed, bank-blind, model-free deterministic resolver built from an operation-synonym
dictionary plus a resource-noun lexicon selects the correct mechanism materially more often (0.8584 vs
0.6903) and the paired advantage is statistically negative. The two structural tautologies
(`B-INCUMBENT-KERNEL = 0.0`, `B-INTERNAL-ID-ORACLE = 1.0`) carry no discriminative weight and are not
corroboration. The low `B-LEX-STRONG-LEARNED` value is a property of its disjoint train/test phrasings,
not evidence against `B-LEX-STRONG`.

The separate applicability-gate sub-question remains unanswered in the affirmative: neither frozen gate
met the calibration targets, so the parent's finding that a single global cosine threshold is
insufficient is replicated here rather than resolved. The gate result is a bounded negative for the
gate sub-mechanism only.

## 6. Consequences (both preregistered branches)

The prereg `product_consequence_*` fields are unchanged and remain binding. Observed branch:
`D-RESOLVER = FALSIFIES` and `D-GATE = GATE-NOT-MET` — the fourth prereg branch. Per the frozen
consequences, the deterministic lexical resolver is an adequate `resolve()` mechanism for this alias
space, but neither mechanism is shippable as a *gated* unseen-goal resolver from this packet, because
the gate is infeasible on this fixture class; `resolve()` must remain UNKNOWN on low-confidence input
and the next step must change gate geometry/architecture rather than retune thresholds. No claim above
`EXPERIMENTAL` is licensed by this packet, and `C-SEMANTIC-RESOLVE` stays at HYPOTHESIS pending a
DIRECTOR verdict.

## 7. Validity threats and limitations

- **Authorship (VN-07):** blind prompts and the V4 no-intent-leak/near-surface checks bound but cannot
  cryptographically exclude latent pretrained knowledge of the intent strings.
- **Checkpoint drift (VN-08):** the frozen revision was unavailable; results are interpretable only for
  the resolved checkpoint `1110a243…`. The deterministic comparator, controls, screen and bootstrap do
  not depend on the checkpoint.
- **Load notice (VN-10):** sentence-transformers emitted a mean-pooling fallback notice on stderr; the
  treatment remained live (20 distinct valid selections, self-match 20/20), but AUDIT should judge
  whether the fallback altered embedding semantics.
- **Comparator curation (VN-14 / unresolved):** the fixed synonym breadth is an authoring choice; the
  learned sensitivity arm cannot cleanly bound it on this disjoint-phrasing split.
- **Single bank / single model (VN-03):** the family-blocked bootstrap has only 5 blocks; generalization
  beyond this fixture/family set is explicitly out of scope.
- **Scope:** parameter binding, HTTP execution, cross-app generalization and ECE gating were not
  measured; ECE is descriptive only.

## 8. Epistemic ceiling

This packet establishes, at most: on the frozen contamination-screened 113-goal primary set, dense
embedding max-cosine selection does not strictly exceed — and in fact falls below — a fixed
bank-blind deterministic operation-synonym + resource-noun resolver; and neither frozen applicability
gate meets the preregistered false-accept/coverage/precision targets on the disjoint test split. It does
not establish or refute `C-SEMANTIC-RESOLVE` globally, does not transfer to other fixtures/checkpoints,
and grants no product promotion.
