# Preregistration: EXP-FRONTIER-38078430316

**Lane:** frontier
**Claim:** C-SEMANTIC-RESOLVE
**Experiment ID:** EXP-FRONTIER-38078430316
**Design contract:** v2 (six freeze-eligibility checks + independent design_review.json before freeze)
**Date:** 2026-10-10
**Status:** DESIGN COMPLETE, NOT YET FROZEN

---

## 1. Strategic Context

This experiment implements the Global Research Director's PIVOT mandate
(`director_mandate.allocation`: action=PIVOT, claim_id=C-SEMANTIC-RESOLVE,
cognitive_reset=true, parent_handoff_disposition=SUPERSEDE). The parent
frontier packet EXP-FRONTIER-37984242167 is superseded: its site-native-discovery
frame was BLOCKED with an empty sampling frame (0 seeds / 0 DEEP items / 0 hosts,
same_failure_count=8) and a 0/0 primary metric unreachable in both falsifier
directions. The mandate's comparative reasoning describes this experiment
explicitly: "The modern test re-runs addressing at larger n with independent
authorship provenance and an explicit token-overlap null -- a bounded replication
that repairs the known validity threat rather than a duplicate. Not a pointless
rerun: the exact gate (authoring-provenance separation + contamination screen
against every registry intent) is new and directly targets the MEASUREMENT_INVALID
cause of EXP-GRAPH-36287167610."

The prior graph packet EXP-GRAPH-36287167610 (claimed bounded positive on
C-SEMANTIC-RESOLVE, final status MEASUREMENT_INVALID, audit agreeing:
producer_claim_supported=false, claim ceiling at HYPOTHESIS) failed for two
interlocking reasons this design removes up front:

1. **Joint-authorship confound**: the goal generator's paraphrase vocabulary
   shared surfacing tokens with the intent strings (same authoring process), so
   lexical-overlap null accuracy was inflated (0.57 on paraphrases) and the
   embedding's apparent advantage may have been partly surface-form overlap.
2. **Over-determined measurement invalidity**: gate 7 (V13 instrument dynamic
   range) and gate 5 (NC-NO-APPLICABLE) both fired; the fitted applicability
   gate was inert on applicable goals (fires on 0/52) because the negative class
   was weak and the gate was the sole decision instrument.

This design neutralizes both: (a) two-process authorship (process A writes
intents, process G writes goals from a pre-declared disjoint synonym vocabulary),
with a contamination screen against EVERY registry intent plus an
authoring-provenance record (vocab disjointness, substring leakage, seeds,
fixture hashes); (b) the primary claim does NOT depend on the fitted gate at all
-- it is a fitting-free paired comparison of embedding max-cosine selection vs
token-overlap selection on the independently-authored set -- and the calibrated
applicability gate is a separate, secondary arm with its own frozen thresholds,
so its behavior can never over-determine the primary answer. The mandate's own
agent-prior list is honored: benchmark dynamic range is a **prerequisite**
(certified by a degeneracy screen C10 before outcome interpretation, and by the
structural lexical floor ~0 of the disjoint-vocabulary primary set), not an
outcome to discover.

---

## 2. Hypothesis and Falsifier

**H1.** On goals authored independently of the mechanism intents (process-G
vocabulary disjoint from process-A vocabulary at the content-word level; no
intent string appears in any goal and vice versa; contamination screen against
every registry intent passes), the all-MiniLM-L6-v2 embedding max-cosine
resolver (B-EMBEDDING-ARGMAX) resolves the applicable mechanism at higher
mechanism-identity accuracy than the token-overlap lexical null
(B-LEXICAL-OVERLAP) on the 60-goal primary set, and higher than the topic-only
baseline (B-FAMILY-ONLY-EMBEDDING) -- so the advantage is operation-level, not
mere topic clustering -- while the dual-class fitted applicability gate with an
explicit abstention region (max-cosine floor `lambda` + top1-top2 margin floor
0.10) satisfies the frozen calibration bounds (pooled false-accept <= 0.10 on
ALL goals, coverage >= 0.50, selective risk <= argmax reference + 0.05, unknown
precision >= 0.85, ECE <= 0.15 with bootstrap upper <= 0.18, abstention >= 0.50
on no-applicable goals).

**F1.** The family-blocked paired one-sided 95% bootstrap lower bound of
(treatment accuracy - lexical accuracy) on the primary set is <= 0, OR the
corresponding (treatment - family-only) bound is <= 0, OR the lexical null is
already at ceiling (degeneracy screen C10 fails). A fired F1 is a bounded
replication negative: on this substrate and model, the prior graph advantage is
explained as joint-authorship surface-form overlap rather than robust semantic
addressing, and C-SEMANTIC-RESOLVE remains HYPOTHESIS with a negative bound for
this mechanism class.

---

## 3. Claim Mapping and Epistemic Consequence

| Frozen outcome | Consequence for C-SEMANTIC-RESOLVE |
|---|---|
| SUPPORTS | Advance to EXPERIMENTAL, bounded to: controlled 20-mechanism registry, all-MiniLM-L6-v2, independent-authorship protocol. Product follows (see spec.json product_consequence_positive). |
| MIXED | Stay HYPOTHESIS; record selection-level semantics without calibrated applicability; resolver not deployable as-is. |
| FALSIFIES | Stay HYPOTHESIS with bounded negative for this mechanism class/substrate. |
| MEASUREMENT_INVALID | Claim untouched (packet-level disposition only). |

All claim updates in `verdict.json` must use registry-valid statuses; this table
states which packet outcomes justify which updates and at which ceiling.

---

## 4. Fixture Specification (frozen in this file; see §13 for code and digests)

### 4.1 Mechanism registry (process A authorship)

20 mechanisms = 5 resource families x 4 roles, materialized as
`src.spider.models.Mechanism` with `mechanism_id = mech_{family}_{role}`:

| family | create | read | update | delete | slots (create) |
|---|---|---|---|---|---|
| user | create a new user | retrieve a user by id | update a user | delete a user | name, email |
| post | create a new post | retrieve a post by id | update a post | delete a post | title, body |
| comment | create a new comment | retrieve a comment by id | update a comment | delete a comment | body |
| album | create a new album | retrieve an album by id | update an album | delete an album | title |
| photo | create a new photo | retrieve a photo by id | update a photo | delete a photo | caption |

- Every action template's `${param}` placeholders are a subset of the declared
  `parameter_slots` (programmatic check `template_binding.all_templates_bound ==
  true`, DESIGN-verified).
- Intent content vocabulary (process A): `V_A = {create, retrieve, update,
  delete, user, post, comment, album, photo, new, id}`.

### 4.2 Goals (process G authorship, vocabulary disjoint from V_A)

140 goals, deterministic enumeration (no RNG anywhere in fixture data):

| Category | Count | Applicable | Role in experiment |
|---|---|---|---|
| independent_paraphrase | 60 (12 per family: 3 phrasings x 4 roles) | yes | **PRIMARY set** (contamination-screened) |
| overlap_paraphrase | 40 (2 per mechanism) | yes | contamination-gradient contrast (contaminated by construction) |
| verbatim | 10 (2 per family, create/read) | yes | positive control C1 (contaminated by construction) |
| no_applicable | 30 (15 out-of-domain + 15 near-miss) | no | null control C2 / calibration negatives |

Process-G synonym vocabulary (pre-declared, disjoint from V_A at the content-word
level; enforced by the screen):

- create verbs: provision, register, add, set up, make, open, establish, initialize, stand up
- read verbs: fetch, look up, pull, get, show, display, load, view, find
- update verbs: amend, modify, change, edit, adjust, revise, alter, refresh
- delete verbs: remove, purge, drop, erase, wipe, deactivate, destroy, clear
- user: account, member, profile, login, subscriber
- post: article, entry, story, piece, writing
- comment: reply, note, remark, feedback, response
- album: gallery, collection, set, folder, showcase
- photo: image, picture, snapshot, shot, capture

Independent-phrasing templates (3 per role) contain no V_A content word;
examples: "provision a fresh account for the platform", "fetch the details of one
article", "amend an existing reply", "purge an obsolete gallery". Overlap
paraphrases deliberately reuse V_A words ("please create the user we discussed").
Near-miss no-applicable goals are semantically adjacent to registry operations
("resize an uploaded avatar image", "summarize the key points of the article").

### 4.3 Contamination screen (against EVERY registry intent) and authoring provenance

For every goal, max token Jaccard (content words after stopword removal) against
every one of the 20 intent strings is computed. The PRIMARY set requires
`max_jaccard < 0.20` for every member. Authoring-provenance record:

- Vocab disjointness: `V_A ∩ V_G = {}` (content words of the 60 independent
  goals vs V_A).
- Substring independence: no intent string is a substring of any primary goal and
  vice versa (0 violations on the primary set; verbatim/overlap arms are
  contaminated by construction and reported separately).
- Generation seeds and fixture digests (SECTION 11).

**DESIGN-probe values (computed with `run.py --freeze-fixture`, non-outcome):
`max_jaccard_primary = 0.0`, `vocab_overlap = []`,
`n_primary_substring_violations = 0`, `n_substring_violations = 18` (all in
verbatim/overlap arms), `all_templates_bound = true`, category counts as in
§4.2 table.** The lexical-null contamination gradient is built in: verbatim
Jaccard = 1.0, overlap range 0.33..1.0, primary = 0.0, no-applicable max 0.20.

### 4.4 Embedding model (frozen)

- Model: `sentence-transformers/all-MiniLM-L6-v2` via CPU ONNX Runtime (same
  weights as the prior graph run, whose torch path pinned revision
  c9745ed1d9f...; the current official HEAD revision is
  `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, verified below).
- Files (exact, DESIGN-verified): `onnx/model.onnx` sha256
  `6fd5d72fe4589f189f8ebc006442dbb529bb7ce38f8082112682524616046452` (90.4 MB);
  `tokenizer.json` sha256
  `be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037`.
- Representation: mean pooling of last hidden state over attention mask,
  L2-normalized, dim 384 (equals sentence-transformers' `1_Pooling` mean config).

### 4.5 Fixture identity canaries (frozen numbers)

```
FIXTURE_SHA256 = 60c8ce3edda7079ea846612ab9f3f744f2501b63b3dfe43fa40c9c6dcd097872
GOALS_SHA256   = 359558610442ad5ab2a8852b2f3cb7eeb03cc814f2812b3767442b9d2ea81007
CODE_SHA256    = 1eb69dbc47861426493453a58cac6d5d9c90996f230bc0bfedaad3eb027dffa3
```

`run.py --freeze-fixture` regenerates fixture.json/goals.json deterministically;
EXECUTE must observe exactly these digests (canary V2) before any outcome-bearing
measurement. `CODE_SHA256` is the digest of the verbatim code block in §13.

---

## 5. Arms, Baselines and Controls (stable identities; reused by EXECUTE/AUDIT verbatim)

### 5.1 Arms

| ID | Function | Decision rule | Abstention |
|---|---|---|---|
| A-CANDIDATE-GATED | treatment with calibration | p_applicable >= lambda AND margin >= 0.10 -> EXECUTABLE argmax; else UNKNOWN | explicit: max-cosine floor + margin floor |
| B-EMBEDDING-ARGMAX | treatment reference | argmax cosine(goal, intent) | never |
| B-LEXICAL-OVERLAP | null comparator | argmax token Jaccard vs every intent (first max wins) | never |
| B-RANDOM | chance null | uniform over 20 mechanisms (declared per-goal seeds) | never |
| B-FAMILY-ONLY-EMBEDDING | topic-confound control | family = argmax cosine to family centroid (mean of its 4 intents); uniform member | never |
| B-ROLE-ONLY-EMBEDDING | topic-confound control | role = argmax mean cosine over role members; uniform member | never |
| B-INTERNAL-ID-ORACLE | ceiling | returns true target | never |
| NC-EMBEDDING-SHUFFLE | sensitivity | label-permuted embedding argmax (declared seeds) | never |

Per-goal arm execution order is randomized with seed 38078430316 and recorded
(OBS-10); arm outputs are saved per goal in `evidence/per_goal_arms.json`.

### 5.2 Controls (all recorded in result.json `controls`, expected/pass/none)

- **C1-PC-VERBATIM** (positive): 10 verbatim goals; accuracy == 1.0, denom 10 > 0.
- **C2-NC-NO-APPLICABLE** (null): abstention >= 0.50 on the 30 no-applicable goals at the frozen gate.
- **C3-ORACLE-CEILING**: B-INTERNAL-ID-ORACLE == 1.0.
- **C4-SHUFFLE-SENSITIVITY**: NC-EMBEDDING-SHUFFLE accuracy <= 0.5.
- **C5-RANDOM-SANITY**: B-RANDOM within 0.10 of 0.05.
- **C6-CONTAMINATION-SCREEN**: primary max Jaccard < 0.20, vocab disjoint, zero primary substring violations.
- **C7-MODEL-CANARY**: model.onnx/tokenizer.json sha256 match §4.4.
- **C8-FIXTURE-CANARY**: regenerated fixture/goals digests == §4.5.
- **C9-CODE-CANARY**: sha256(run.py) == CODE_SHA256.
- **C10-DEGENERACY-SCREEN**: lexical null on primary < 0.90 AND oracle == 1.0 (benchmark dynamic-range certificate).

---

## 6. Execution Protocol

### 6.1 Scope and code root

EXECUTE runs inside the repo (worktree on `lab2/frontier`). Code and evidence go
under `research/frontier/exp_38078430316/` (frontier lane allowed code root);
`result.json`, `report.md`, `provenance.json` are written into
`research/experiments/EXP-FRONTIER-38078430316/`. No other paths may change.

### 6.2 Prerequisite certificate (DESIGN-verified; EXECUTE repeats with hash checks)

1. `pip install numpy==1.26.4 onnxruntime==1.19.2 tokenizers==0.20.3`
   (wheels verified downloadable from pypi.org at DESIGN time; import-verified).
2. Download into `research/frontier/exp_38078430316/model/`:
   - `https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/onnx/model.onnx`
   - `https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/tokenizer.json`
   - verify both sha256 against §4.4 BEFORE any embedding (Embedder.__init__
     re-verifies at runtime).
3. Python >= 3.10 (design runner: CPython 3.12).

### 6.3 DESIGN probe log (evidence for freeze_eligibility, non-outcome)

- Address reachability + wheels: numpy 1.26.4, onnxruntime 1.19.2, tokenizers
  0.20.3 downloaded from pypi.org and `import` verified in the DESIGN runner.
- Model files: both pinned files downloaded from huggingface.co with the exact
  §4.4 sha256 values; `onnxruntime` CPU session loads; embeddings dim 384.
- Semantic dynamic range of the treatment (probe phrases, not confirmatory):
  "add a new user" vs "create a new user account" cos = 0.800; vs "register a
  fresh account for someone" cos = 0.501; "search the web for a topic" vs "find
  pages about a subject" cos = 0.600; "convert a document to pdf" vs "export a
  file as pdf format" cos = 0.770; unrelated pairs cos in [-0.057, 0.017].
- Fixture screen + canaries: §4.3/§4.5 (all values listed there).

### 6.4 Outcome-bearing code (frozen verbatim in §13)

EXECUTE must (1) extract the fenced Python block of §13 byte-for-byte into
`research/frontier/exp_38078430316/run.py`; (2) verify
`sha256sum run.py == CODE_SHA256` (§4.5); (3) run in this order:

```bash
pip install numpy==1.26.4 onnxruntime==1.19.2 tokenizers==0.20.3
python run.py --freeze-fixture research/frontier/exp_38078430316/fixture_build
#   -> printed FIXTURE_SHA256 / GOALS_SHA256 must equal section 4.5 values
python run.py research/frontier/exp_38078430316/model research/frontier/exp_38078430316   --expected-code-sha256 1eb69dbc47861426493453a58cac6d5d9c90996f230bc0bfedaad3eb027dffa3
```

Any canary mismatch or control failure is a MEASUREMENT_INVALID, logged with the
exact failing gate; no threshold or metric may be weakened after seeing outputs.

### 6.5 Liveness / satisfiability probes already executed at DESIGN (non-confirmatory)

- `run.py --smoke <model_dir> <out>`: toy 5-goal fixture end-to-end through the
  embedder + arms (status smoke_ok, dim 384) -- toy concepts (widget/gadget)
  differ from the confirmatory fixture so no confirmatory outcome was produced.
- `run.py --toy-full <model_dir> <out>`: the COMPLETE measurement path
  (splits -> gate fitting -> all arms -> metrics -> controls -> frozen decision
  labels) executes without errors on the toy fixture. The toy's
  MEASUREMENT_INVALID label (random-sanity fail on a 4-mechanism toy) is a toy
  artifact, not a defect.

### 6.6 Splits (frozen)

Stratified by family (applicable: 110 goals -> 60/20/20% by family) and by
category (no-applicable: 30 goals -> 60/20/20%), fixed seed 38078430316,
logged before fitting (OBS-2). The gate is fit on train (both classes), lambda
chosen on validation (Youden index), and all calibration numbers are reported
for the frozen gate.

---

## 7. Metrics (stable identities; values in result.json `metrics`)

| ID | Definition | Unit |
|---|---|---|
| m_primary_treatment_acc | B-EMBEDDING-ARGMAX accuracy on the 60 primary goals | proportion |
| m_primary_lexical_acc | B-LEXICAL-OVERLAP accuracy on the 60 primary goals | proportion |
| m_primary_treatment_advantage_over_lexical | paired per-goal mean difference | proportion |
| m_primary_advantage_lower95 | family-blocked paired one-sided 95% lower bound (10,000 re-samples, seed 38078430316) | proportion |
| m_primary_treatment_vs_family_only_advantage / _lower95 | same for (treatment - B-FAMILY-ONLY-EMBEDDING) | proportion |
| m_primary_family_only_acc / m_primary_role_only_acc / m_primary_random_acc / m_primary_shuffle_acc / m_oracle_acc | topic-confound, chance and sensitivity controls | proportion |
| m_overlap_treatment_acc / m_overlap_lexical_acc / m_overlap_treatment_advantage | contamination-gradient arm on 40 overlap goals | proportion |
| m_advantage_gradient_interaction | (disjoint advantage) - (overlap advantage); informative, NOT a gate | proportion |
| m_verbatim_acc | positive control accuracy | proportion |
| contamination_max_jaccard_primary / n_primary_passed_screen / vocab_overlap / n_primary_substring_violations | authoring-barrier screen values | mixed |
| cal_pooled_false_accept | wrong EXECUTABLE / total EXECUTABLE over ALL 140 goals at frozen gate | proportion |
| cal_coverage | EXECUTABLE applicable / all applicable | proportion |
| cal_selective_risk | error rate on answered applicable | proportion |
| cal_selective_risk_ref_argmax | B-EMBEDDING-ARGMAX error rate on applicable (reference) | proportion |
| cal_unknown_precision | TP_abstain / (TP_abstain + FP_abstain) | proportion |
| cal_ece_global / cal_ece_upper95 | ECE, 10 equal-width bins, closed top bin [0.9,1.0]; bootstrap upper (1,000 reps) | proportion |
| cal_abstain_applicable_rate / cal_abstain_noapply_rate | abstention rates per class at frozen gate | proportion |
| cal_lambda / cal_gate_w / cal_gate_b / cal_gate_mu / cal_gate_sd | fitted gate identity | mixed |
| n_primary / n_overlap / n_goals_total / n_applicable / n_no_applicable / n_executed / n_abstained | denominators | count |

---

## 8. Decision Rule (frozen; identical to spec.json decision_rule)

1. **G1 validity**: V1..V10 (spec.json measurement_validity), equivalently
   controls C1..C10 all `pass`. Any FAIL -> `status=MEASUREMENT_INVALID`,
   `outcome=NOT_APPLICABLE`.
2. **G2 primary** (SUPPORTS requires both):
   - P1 `m_primary_advantage_lower95 > 0` (treatment vs lexical null);
   - P2 `m_primary_treatment_vs_family_only_lower95 > 0` (beyond topic).
3. **G3 calibration** (SUPPORTS requires all): pooled false-accept <= 0.10;
   coverage >= 0.50; selective risk <= ref + 0.05; unknown precision >= 0.85;
   ECE <= 0.15 and upper <= 0.18; abstention on no-applicable >= 0.50.
4. Outcomes: SUPPORTS = G1^G2^G3; MIXED = G1^G2^!G3; FALSIFIES = G1^!G2;
   MEASUREMENT_INVALID = !G1.

---

## 9. Validity Threats and Mitigations

| Threat | Mitigation |
|---|---|
| Joint-authorship confound (prior cause of MEASUREMENT_INVALID) | Two-process authorship, disjoint vocabularies, contamination screen vs EVERY intent, substring + vocab provenance record (C6/V4) |
| Comparator at ceiling (Director agent-prior 1) | Lexical floor ~0 by construction on primary set; degeneracy screen C10 (lexical < 0.90, oracle == 1.0) hard-gates before interpretation |
| Gate inert / over-determining (prior V13 failure) | Primary claim is fitting-free; gate+abstention is a separate secondary arm with its own frozen bounds; no gate can veto the primary |
| Topic clustering masquerading as semantics | B-FAMILY-ONLY-EMBEDDING + B-ROLE-ONLY-EMBEDDING controls; P2 requires beating family-only |
| False-accept denominator ambiguity (prior audit finding) | Single frozen definition: wrong EXECUTABLE / total EXECUTABLE over ALL 140 goals |
| Pseudoreplication / family clustering | Family-blocked paired bootstrap, 10,000 reps, seed fixed |
| Model drift / non-reproducibility | Pinned revision + per-file sha256 + runtime re-verification (C7/V1) |
| Code or fixture drift between DESIGN and EXECUTE | Verbatim code embedded in §13 (hash-gated), deterministic fixture regeneration with canary digests (C8/C9/V2/V3) |
| Calibration fitted on test data | Train/val/test split by seed, logged before fitting; lambda chosen on validation only; test reported |
| ECE binning defects (prior V5) | 10 equal-width bins, closed top bin [0.9, 1.0], no rows dropped |
| Underpowered decision | n=60 primary goals (vs prior n=8 Intel arm), 20 mechanisms, 5 families; chance = 0.05 |
| Toy contamination of results | Toy/smoke runs use distinct concepts (widget/gadget) and are never merged with confirmatory outputs |

---

## 10. No-Go Rules (Do Not Weaken After Seeing Outcomes)

- Do not change the primary set (60 independent_paraphrase goals) or its screen
  threshold 0.20.
- Do not substitute an applicable-only false-accept denominator.
- Do not replace the family-blocked paired bootstrap with an unblocked or
  two-sample test.
- Do not drop C1/C2/C3/C4/C5/C6/C10 or their frozen pass conditions.
- Do not accept an uncalibrated fixed threshold as the 'fitted' gate (lambda is
  chosen on validation by Youden index and parameters are logged).
- Do not merge overlap/verbatim/no-applicable goals into the primary denominator.
- Do not run the confirmatory evaluation before all canaries (V1-V3) pass.
- Do not edit any frozen file after freeze.json exists; do not weaken thresholds
  because a result is disappointing.

---

## 11. Provenance Requirements

- Git commit of the worktree at freeze time; `base_sha`
  176ab633ebcd2e066f6c21701a591faf0e128d18 (request.json).
- Python version (design runner CPython 3.12.15), numpy 1.26.4, onnxruntime
  1.19.2, tokenizers 0.20.3; model revision
  1110a243fdf4706b3f48f1d95db1a4f5529b4d41; per-file sha256 §4.4.
- Fixture digests §4.5; run.py digest CODE_SHA256 §4.5.
- Seeds: split/bootstrap/shuffle/arm-order 38078430316 (declared in code).
- GitHub run id, execution timestamps, evidence paths
  (`research/frontier/exp_38078430316/evidence/*`).

---

## 12. Freeze-Eligibility Recap (full reasons in spec.json)

| Check | Status |
|---|---|
| decision_rule_reachability | PASS |
| measurement_prerequisites | PASS |
| baseline_identifiability | PASS |
| control_sensitivity | PASS |
| treatment_liveness | PASS |
| freeze_artifacts_bound | NOT_APPLICABLE (fixture + outcome-bearing code frozen verbatim in this prereg, hash-bound; no mutable local dependency; remote model pinned by revision + sha256) |

---

## 13. Frozen Outcome-Bearing Code (verbatim; sha256 == CODE_SHA256 ==
1eb69dbc47861426493453a58cac6d5d9c90996f230bc0bfedaad3eb027dffa3)

```python
#!/usr/bin/env python3
"""
EXP-FRONTIER-38078430316 -- C-SEMANTIC-RESOLVE (frontier lane, Research 2.0)
Deterministic, stdlib + numpy + onnxruntime + tokenizers pipeline.

Modes (invoked by EXECUTE exactly as declared in prereg.md section 6.4):
  python run.py --freeze-fixture OUTDIR
      Materialize fixture.json + goals.json + contamination screen + authoring
      provenance checks. NO embeddings, NO arms, NO outcome values. Used in
      DESIGN to fix the fixture hash, and by EXECUTE as a reproducibility
      canary before any outcome-bearing measurement.
  python run.py --smoke MODEL_DIR OUTDIR
      Toy-fixture end-to-end pipeline. DESIGN/design-review liveness probe only;
      the toy fixture uses different concepts and never affects confirmatory
      results.
  python run.py MODEL_DIR OUTDIR
      Full confirmatory run. Embeds mechanisms + goals, runs every frozen arm,
      computes metrics, bakes result.json / report.md / provenance.json into
      the experiment packet, and writes raw evidence below OUTDIR.

The complete code of this file is frozen verbatim inside prereg.md; EXECUTE
must reproduce it byte-for-byte and verify CODE_SHA256 before running. The
fixture and goals are regenerated deterministically and their sha256 must
equal FIXTURE_SHA256 / GOALS_SHA256 declared here (and in prereg.md).

Authoring barrier (frozen):
  - Process A (mechanism author) wrote the canonical intent strings using
    vocabulary V_A = {create, retrieve, update, delete, user, post, comment,
    album, photo, new, by, id}.
  - Process G (goal author) wrote the independent goal paraphrases using
    vocabulary V_G (VERB_SYN / UNIT_SYN below) disjoint from V_A at the
    content-word level.
  - The contamination screen below measures max token Jaccard of every goal
    against EVERY registry intent; the primary set requires < CONTAM_THRESHOLD.
  - No intent string is a substring of any goal string and vice versa.
Deterministic generation: fixed literal tables + fixed enumeration order; no
random draws are used to build the fixture (only for splits/bootstrap/arm
order, using declared fixed seeds).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import random
import re
import statistics
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Frozen constants
# ---------------------------------------------------------------------------
EXPERIMENT_ID = "EXP-FRONTIER-38078430316"
LANE = "frontier"
CLAIM_IDS = ["C-SEMANTIC-RESOLVE"]

MODEL_REPO = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
MODEL_ONNX_SHA256 = "6fd5d72fe4589f189f8ebc006442dbb529bb7ce38f8082112682524616046452"
TOKENIZER_JSON_SHA256 = "be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037"
MODEL_ONNX_FILENAME = "model.onnx"
TOKENIZER_FILENAME = "tokenizer.json"

# Fixture identity canaries (values fixed at DESIGN time by --freeze-fixture;
# EXECUTE regenerates deterministically and must observe the same digests).
FIXTURE_SHA256 = "60c8ce3edda7079ea846612ab9f3f744f2501b63b3dfe43fa40c9c6dcd097872"
GOALS_SHA256 = "359558610442ad5ab2a8852b2f3cb7eeb03cc814f2812b3767442b9d2ea81007"
CONTAM_THRESHOLD = 0.20          # max token Jaccard allowed on the primary set
MARGIN_ABSTAIN_THRESHOLD = 0.10  # top1-top2 cosine margin below which A-CANDIDATE abstains
N_BOOTSTRAP = 10_000             # family-blocked paired bootstrap resamples
ALPHA = 0.05                     # one-sided significance
SEED_SPLIT = 38078430316
SEED_BOOTSTRAP = 38078430316
SEED_SHUFFLE = 38078430316
SEED_ARM_ORDER = 38078430316

STOPWORDS = frozenset(
    "a an the by for with of to and or on in at my their her his its it me us "
    "please could you would we discussed one about from into after before over "
    "under around between through during without within along behind beyond "
    "first additionally respectively same".split()
)

FAMILIES = ["user", "post", "comment", "album", "photo"]
ROLES = ["create", "read", "update", "delete"]

V_A_CONTENT = ["create", "retrieve", "update", "delete", "user", "post", "comment",
               "album", "photo", "new", "id"]

VERB_SYN = {
    "create": ["provision", "register", "add", "set up", "make", "open", "establish", "initialize", "stand up"],
    "read": ["fetch", "look up", "pull", "get", "show", "display", "load", "view", "find"],
    "update": ["amend", "modify", "change", "edit", "adjust", "revise", "alter", "refresh"],
    "delete": ["remove", "purge", "drop", "erase", "wipe", "deactivate", "destroy", "clear"],
}
UNIT_SYN = {
    "user": ["account", "member", "profile", "login", "subscriber"],
    "post": ["article", "entry", "story", "piece", "writing"],
    "comment": ["reply", "note", "remark", "feedback", "response"],
    "album": ["gallery", "collection", "set", "folder", "showcase"],
    "photo": ["image", "picture", "snapshot", "shot", "capture"],
}

# Deterministic goal templates.  Independent paraphrases (process G) must not
# contain any V_A content word; enforced by the contamination screen.
TEMPLATE_INDEPENDENT = {
    "create": ["provision a fresh {unit} for the platform",
               "register an extra {unit}",
               "set up an additional {unit}"],
    "read": ["fetch the details of one {unit}",
             "look up a specific {unit}",
             "pull the current {unit} record"],
    "update": ["amend an existing {unit}",
               "modify the stored {unit}",
               "adjust the saved {unit}"],
    "delete": ["remove a given {unit}",
               "purge an obsolete {unit}",
               "wipe the selected {unit}"],
}
# Deliberately contaminated applicable paraphrases (share V_A words with the
# family intent) for the contamination-gradient contrast.
TEMPLATE_OVERLAP = ["please {verb} the {unit} we discussed",
                    "could you {verb} {art} {unit} for me"]

NO_APPLICABLE_GOALS = [
    # out-of-domain (15)
    "schedule a recurring reminder for the team",
    "archive a finished project workspace",
    "publish a newsletter to subscribers",
    "notify my colleagues about the meeting",
    "calculate the total balance of the invoice",
    "encrypt a confidential document before sharing",
    "translate this paragraph into french",
    "send a welcome email to new signups",
    "check the weather forecast for tomorrow",
    "book a meeting room for the afternoon",
    "generate a monthly sales report in pdf",
    "merge the two spreadsheet tabs",
    "scan a qr code from the poster",
    "reboot the staging server instance",
    "monitor uptime of the public api",
    # near-miss (15): semantically adjacent to registry operations
    "resize an uploaded avatar image",
    "summarize the key points of the article",
    "remove a photo filter from the shot",
    "replace the profile picture of the account",
    "append a caption below the gallery photo",
    "split the album into two smaller sets",
    "report the comment that looks like spam",
    "pin the reply to the top of the discussion",
    "sticky the note inside the shared folder",
    "verify the data captured by the last sync",
    "export the audit log to csv",
    "import contacts from a previous platform",
    "restore the previous backup snapshot",
    "invite a teammate to the shared board",
    "deduplicate the address list for the campaign",
]

ARTICLES = {"album": "an"}
INTENT_TEMPLATE = {
    "create": "create a new {family}",
    "read": "retrieve a {family} by id",
    "update": "update a {family}",
    "delete": "delete a {family}",
}


def article(family: str) -> str:
    return ARTICLES.get(family, "a")


def content_words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z]+", text.lower()) if w not in STOPWORDS]


# ---------------------------------------------------------------------------
# Fixture: mechanism registry (grounded in src.spider.models.Mechanism)
# ---------------------------------------------------------------------------
def sys_path_setup() -> Path:
    """Locate the SPIDER repo root (contains src/spider) above this file."""
    env = os.environ.get("SPIDER_REPO_ROOT")
    if env and (Path(env) / "src" / "spider" / "models.py").exists():
        if env not in sys.path:
            sys.path.append(env)
        return Path(env)
    here = Path(__file__).resolve()
    for cand in [here] + list(here.parents):
        if (cand / "src" / "spider" / "models.py").exists():
            if str(cand) not in sys.path:
                sys.path.append(str(cand))
            return cand
    raise RuntimeError("repo root with src/spider/models.py not found above " + str(here))


def make_mechanisms() -> list[dict]:
    from src.spider.models import Mechanism

    mechs: list[Mechanism] = []
    for family in FAMILIES:
        plural = family + "s"
        create_slots = {
            "user": ["name", "email"],
            "post": ["title", "body"],
            "comment": ["body"],
            "album": ["title"],
            "photo": ["caption"],
        }[family]
        for role in ROLES:
            intent = INTENT_TEMPLATE[role].format(family=family)
            if role == "create":
                slots = create_slots
                template = {"method": "POST", "path": f"/{plural}",
                            "body": {s: "${" + s + "}" for s in slots}}
            else:
                fid = family + "_id"
                slots = [fid] + (["fields"] if role == "update" else [])
                body = {"${" + fid + "}": "value"}
                if role == "update":
                    body["fields"] = "${fields}"
                template = {"method": {"read": "GET", "update": "PATCH", "delete": "DELETE"}[role],
                            "path": f"/{plural}/${{{fid}}}", "body": body}
            mech = Mechanism(
                mechanism_id=f"mech_{family}_{role}",
                intent=intent,
                preconditions={"auth": "none", "state": "service ready"},
                action_template=template,
                postconditions={"applied": True},
                parameter_slots=slots,
                auth_scope=None,
                freshness={"source": "frozen registry", "checked_at": "frozen"},
                applicability_guards={"registry_only": True},
                verification_rule={"type": "registry_identity"},
                failure_boundary={"abstain_region": "declared"},
                repair_scope={},
                evidence=["EXP-FRONTIER-38078430316 fixture (frozen)"],
                confidence=1.0,
                invalidated=False,
            )
            mechs.append(mech)
    # deterministic order: families then roles as listed
    return [m.as_dict() for m in mechs]


def make_goals() -> list[dict]:
    """Deterministic goal enumeration; no RNG involved in fixture data."""
    goals: list[dict] = []
    # 1) independent paraphrases (primary, process G vocabulary)
    idx = 0
    for family in FAMILIES:
        syns = UNIT_SYN[family]
        for role in ROLES:
            for t in TEMPLATE_INDEPENDENT[role]:
                unit = syns[idx % len(syns)]
                idx += 1
                text = t.format(unit=unit)
                goals.append({
                    "goal_id": f"g_ind_{family}_{role}_{len([g for g in goals if g['target'] == f'mech_{family}_{role}' and g['category']=='independent_paraphrase'])}",
                    "text": text,
                    "category": "independent_paraphrase",
                    "applicable": True,
                    "target": f"mech_{family}_{role}",
                })
    # 2) overlap paraphrases (contamination gradient, process A vocabulary reuse)
    for family in FAMILIES:
        for role in ROLES:
            for t in TEMPLATE_OVERLAP:
                text = t.format(verb=role, unit=family, art=article(family))
                goals.append({
                    "goal_id": f"g_ovl_{family}_{role}_{len([g for g in goals if g['target'] == f'mech_{family}_{role}' and g['category']=='overlap_paraphrase'])}",
                    "text": text,
                    "category": "overlap_paraphrase",
                    "applicable": True,
                    "target": f"mech_{family}_{role}",
                })
    # 3) verbatim positive control (exact intent strings, 2 per family)
    for family in FAMILIES:
        for role in ["create", "read"]:
            goals.append({
                "goal_id": f"g_verb_{family}_{role}",
                "text": INTENT_TEMPLATE[role].format(family=family),
                "category": "verbatim",
                "applicable": True,
                "target": f"mech_{family}_{role}",
            })
    # 4) no-applicable null control
    for i, text in enumerate(NO_APPLICABLE_GOALS):
        goals.append({
            "goal_id": f"g_na_{i:02d}",
            "text": text,
            "category": "no_applicable",
            "applicable": False,
            "target": None,
        })
    return goals


def template_binding_check(mechs: list[dict]) -> dict:
    """Every ${param} in an action template must be declared in parameter_slots."""
    report = {}
    bad = []
    for m in mechs:
        slots = set(m["parameter_slots"])
        used = set(re.findall(r"\$\{([^}]+)\}", json.dumps(m["action_template"])))
        if not used.issubset(slots):
            bad.append({"mechanism_id": m["mechanism_id"], "missing": sorted(used - slots)})
    report["all_templates_bound"] = len(bad) == 0
    report["unbound"] = bad
    report["n_mechanisms"] = len(mechs)
    report["n_families"] = len(FAMILIES)
    report["n_roles"] = len(ROLES)
    return report


# ---------------------------------------------------------------------------
# Contamination screen + authoring provenance (frozen definitions)
# ---------------------------------------------------------------------------
def tokenize_contam(text: str) -> set[str]:
    return set(content_words(text))


def contamination_screen(mechs: list[dict], goals: list[dict]) -> dict:
    intents = [m["intent"] for m in mechs]
    intent_sets = [tokenize_contam(i) for i in intents]
    rows = []
    max_jaccard_primary = 0.0
    for g in goals:
        gs = tokenize_contam(g["text"])
        vals = []
        for iset in intent_sets:
            union = gs | iset
            j = len(gs & iset) / len(union) if union else 0.0
            vals.append(j)
        mj = max(vals)
        if g["category"] == "independent_paraphrase":
            max_jaccard_primary = max(max_jaccard_primary, mj)
        rows.append({
            "goal_id": g["goal_id"],
            "category": g["category"],
            "max_jaccard_vs_all_intents": mj,
            "argmax_intent": intents[vals.index(mj)] if vals else None,
            "passed_screen": mj < CONTAM_THRESHOLD,
        })
    # vocab disjointness (content words only)
    vg = set()
    for g in goals:
        if g["category"] == "independent_paraphrase":
            vg |= tokenize_contam(g["text"])
    va = set(V_A_CONTENT)
    vocab_overlap = sorted(vg & va)
    # substring independence: no intent string inside any goal and vice versa.
    # The provenance gate is the PRIMARY (independent) set; the verbatim and
    # overlap arms are contaminated BY CONSTRUCTION and are reported but never
    # part of the primary set.
    substr_violations = []
    for g in goals:
        low = g["text"].lower()
        for m in mechs:
            il = m["intent"].lower()
            if il in low or low in il:
                substr_violations.append({"goal_id": g["goal_id"], "intent": m["intent"]})
    primary_substr = [v for v in substr_violations if v["goal_id"].startswith("g_ind_")]
    primary = [r for r in rows if r["passed_screen"]]
    return {
        "contam_threshold": CONTAM_THRESHOLD,
        "n_goals": len(rows),
        "n_primary_eligible": len([g for g in goals if g["category"] == "independent_paraphrase"]),
        "n_primary_passed": len([r for r in rows if r["category"] == "independent_paraphrase" and r["passed_screen"]]),
        "max_jaccard_primary": max_jaccard_primary,
        "vocab_a": sorted(va),
        "vocab_g": sorted(vg),
        "vocab_overlap": vocab_overlap,
        "substring_violations": substr_violations,
        "n_substring_violations": len(substr_violations),
        "primary_substring_violations": primary_substr,
        "n_primary_substring_violations": len(primary_substr),
        "screen_rows": rows,
    }


# ---------------------------------------------------------------------------
# Embedding (all-MiniLM-L6-v2 via ONNX Runtime, CPU, deterministic)
# ---------------------------------------------------------------------------
class Embedder:
    def __init__(self, model_dir: Path):
        import onnxruntime as ort
        from tokenizers import Tokenizer

        onnx_path = model_dir / MODEL_ONNX_FILENAME
        tok_path = model_dir / TOKENIZER_FILENAME
        for p, expected in ((onnx_path, MODEL_ONNX_SHA256), (tok_path, TOKENIZER_JSON_SHA256)):
            got = hashlib.sha256(p.read_bytes()).hexdigest()
            if got != expected:
                raise RuntimeError(f"model canary mismatch for {p.name}: {got} != {expected}")
        self.tok = Tokenizer.from_file(str(tok_path))
        self.sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        self.input_names = {i.name for i in self.sess.get_inputs()}
        self.dim = self.sess.get_outputs()[0].shape[-1]

    def embed(self, texts: list[str]):
        import numpy as np

        encs = self.tok.encode_batch(texts)
        maxlen = max(len(e.ids) for e in encs) if encs else 1
        ids = np.zeros((len(encs), maxlen), dtype=np.int64)
        am = np.zeros((len(encs), maxlen), dtype=np.int64)
        tt = np.zeros((len(encs), maxlen), dtype=np.int64)
        for i, e in enumerate(encs):
            L = len(e.ids)
            ids[i, :L] = e.ids
            am[i, :L] = e.attention_mask
            tt[i, :L] = e.type_ids
        feeds = {"input_ids": ids, "attention_mask": am}
        if "token_type_ids" in self.input_names:
            feeds["token_type_ids"] = tt
        out = self.sess.run(None, feeds)[0]  # (batch, seq, hidden)
        mask = am[..., None].astype(np.float32)
        summed = (out * mask).sum(axis=1)
        counts = mask.sum(axis=1)
        emb = summed / counts
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return emb / norms


def cosine_matrix(E: Embedder, a: list[str], b: list[str]):
    import numpy as np

    A = E.embed(a)  # (n_a, d)
    B = E.embed(b)  # (n_b, d)
    return A @ B.T  # n_a x n_b


# ---------------------------------------------------------------------------
# Lexical null and arm outputs
# ---------------------------------------------------------------------------
def tokenize_lex(t: str) -> set[str]:
    return set(content_words(t))


def lexical_argmax(goal_text: str, intents: list[str], ids: list[str]) -> str:
    gs = tokenize_lex(goal_text)
    best, best_j = None, -1.0
    for iid, it in zip(ids, intents):
        ts = tokenize_lex(it)
        union = gs | ts
        j = len(gs & ts) / len(union) if union else 0.0
        if j > best_j + 1e-12:
            best, best_j = iid, j
    return best  # deterministic: first maximum wins in frozen id order


def fitted_logistic_gate(train_x: list[float], train_y: list[int],
                         val_x: list[float], val_y: list[int],
                         seed: int):
    """1-D logistic gate on max-cosine; threshold via Youden on validation."""
    import numpy as np

    x = np.asarray(train_x, dtype=np.float64)
    y = np.asarray(train_y, dtype=np.float64)
    mu = float(x.mean())
    sd = float(x.std())
    if sd < 0.05:  # numerical floor: avoid pathological saturation
        sd = 0.05
    z = (x - mu) / sd
    w0, b0 = 0.0, 0.0
    lr, epochs = 0.2, 3000
    for _ in range(epochs):
        lin = np.clip(w0 * z + b0, -30.0, 30.0)
        p = 1.0 / (1.0 + np.exp(-lin))
        err = p - y
        gw = float(np.mean(err * z))
        gb = float(np.mean(err))
        w0 -= lr * gw
        b0 -= lr * gb
    def p_of(xx):
        zz = (np.asarray(xx, dtype=np.float64) - mu) / sd
        lin = np.clip(w0 * zz + b0, -30.0, 30.0)
        return (1.0 / (1.0 + np.exp(-lin))).tolist()
    # threshold selection: Youden (TPR - FPR) over unique validation p values
    vp = p_of(val_x)
    cands = sorted(set(vp))
    best_l, best_youden = None, -1e18
    for lam in cands:
        tp = sum(1 for p, yv in zip(vp, val_y) if p >= lam and yv == 1)
        fn = sum(1 for p, yv in zip(vp, val_y) if p < lam and yv == 1)
        fp = sum(1 for p, yv in zip(vp, val_y) if p >= lam and yv == 0)
        tn = sum(1 for p, yv in zip(vp, val_y) if p < lam and yv == 0)
        tpr = tp / (tp + fn) if (tp + fn) else 0.0
        fpr = fp / (fp + tn) if (fp + tn) else 0.0
        youden = tpr - fpr
        if youden > best_youden + 1e-15:
            best_youden, best_l = youden, lam
    return {
        "w": float(w0), "b": float(b0), "mu": mu, "sd": sd,
        "lambda": best_l, "youden_val": best_youden,
        "p_of": p_of,
    }


def family_only_argmax(cos: list[tuple[str, float]], families: list[str]) -> str:
    """Topic-only baseline: resolve family by max cosine to its 4 intents,
    then pick a random member of that family (declared seed)."""
    rng = random.Random(SEED_SHUFFLE)
    best_family = None
    best = -1e18
    fam_avg = {}
    for f in families:
        vals = [c for iid, c in cos if iid.startswith(f"mech_{f}_")]
        fam_avg[f] = sum(vals) / len(vals)
    for f, v in fam_avg.items():
        if v > best + 1e-15:
            best, best_family = v, f
    members = [iid for iid, _ in cos if iid.startswith(f"mech_{best_family}_")]
    return rng.choice(members)


def role_only_argmax(cos: list[tuple[str, float]], roles: list[str]) -> str:
    """Role-only baseline: resolve role from cosine to role-name embeddings
    (already folded into the mechanism-level matrix by proxy: use the mean of
    cos over mechanisms of each role), then random member of the role."""
    rng = random.Random(SEED_SHUFFLE + 1)
    role_avg = {}
    for r in roles:
        mem = [c for iid, c in cos if iid.endswith("_" + r)]
        role_avg[r] = sum(mem) / len(mem) if mem else 0.0
    best_role = max(role_avg, key=lambda r: role_avg[r])
    members = [iid for iid, _ in cos if iid.endswith("_" + best_role)]
    return rng.choice(members)


def shuffled_argmax(cos: list[tuple[str, float]], intents: list[str], seed: int) -> str:
    """Sensitivity control: permute the intent labels, then argmax. Must be ~chance."""
    rng = random.Random(seed)
    ids = [i for i, _ in cos]
    perm = list(ids)
    rng.shuffle(perm)
    return perm[max(range(len(cos)), key=lambda k: cos[k][1])]


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def family_blocked_paired_bootstrap(diff: list[tuple[str, float]], n: int = N_BOOTSTRAP,
                                    alpha: float = ALPHA) -> dict:
    """diff = (family, value) pairs over goals. Resample families with
    replacement, average resampled values; return one-sided lower alpha bound."""
    rng = random.Random(SEED_BOOTSTRAP)
    fams = sorted({f for f, _ in diff})
    by_fam = {f: [v for ff, v in diff if ff == f] for f in fams}
    means = []
    for _ in range(n):
        picks = [by_fam[f][rng.randrange(len(by_fam[f]))] for f in fams]
        means.append(sum(picks) / len(picks))
    means.sort()
    return {
        "n_goals": len(diff),
        "n_families": len(fams),
        "bootstrap_n": n,
        "mean": sum(v for _, v in diff) / len(diff),
        "lower_" + str(1 - alpha): means[int(n * alpha)],
        "upper_" + str(alpha): means[int(n * (1 - alpha)) - 1],
    }


def ece_global(ps: list[float], ys: list[int], n_bins: int = 10) -> tuple[float, list[dict]]:
    bins = [[] for _ in range(n_bins)]
    for p, y in zip(ps, ys):
        idx = min(n_bins - 1, int(p * n_bins))  # closed top bin
        bins[idx].append((p, y))
    ece = 0.0
    detail = []
    for i, b in enumerate(bins):
        if not b:
            detail.append({"bin": i, "n": 0})
            continue
        acc = sum(y for _, y in b) / len(b)
        conf = sum(p for p, _ in b) / len(b)
        w = len(b) / len(ps)
        ece += w * abs(acc - conf)
        detail.append({"bin": i, "n": len(b), "acc": acc, "conf": conf})
    return ece, detail


# ---------------------------------------------------------------------------
# Main runners
# ---------------------------------------------------------------------------
def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build_fixture(outdir: Path):
    mechs = make_mechanisms()
    goals = make_goals()
    bind = template_binding_check(mechs)
    screen = contamination_screen(mechs, goals)
    registry = {"schema_version": 1, "experiment_id": EXPERIMENT_ID,
                "mechanisms": mechs, "goals": goals,
                "template_binding": bind, "contamination_screen": screen,
                "model": {"repo": MODEL_REPO, "revision": MODEL_REVISION,
                          "onnx_sha256": MODEL_ONNX_SHA256,
                          "tokenizer_sha256": TOKENIZER_JSON_SHA256},
                "constants": {"contam_threshold": CONTAM_THRESHOLD,
                              "margin_abstain_threshold": MARGIN_ABSTAIN_THRESHOLD}}
    write_json(outdir / "fixture.json", registry)
    write_json(outdir / "goals.json", {"schema_version": 1, "experiment_id": EXPERIMENT_ID,
                                       "goals": goals})
    write_json(outdir / "contamination.json", screen)
    write_json(outdir / "template_binding.json", bind)
    fsha = sha256_bytes((outdir / "fixture.json").read_bytes())
    gsha = sha256_bytes((outdir / "goals.json").read_bytes())
    return fsha, gsha, registry


def check_fixture_canary(outdir: Path) -> None:
    fsha = sha256_bytes((outdir / "fixture.json").read_bytes())
    gsha = sha256_bytes((outdir / "goals.json").read_bytes())
    if fsha != FIXTURE_SHA256 or gsha != GOALS_SHA256:
        raise RuntimeError(f"fixture canary mismatch: fixture={fsha} (declared {FIXTURE_SHA256}) "
                           f"goals={gsha} (declared {GOALS_SHA256})")


def split_goal_indices(goals: list[dict]) -> dict:
    """Stratified train/val/test by family (applicable) and by category
    (no-applicable), fixed seed, logged before fitting."""
    applicable = [i for i, g in enumerate(goals) if g["applicable"]]
    noapply = [i for i, g in enumerate(goals) if not g["applicable"]]
    rng = random.Random(SEED_SPLIT)
    fam_map: dict[str, list[int]] = {}
    for i in applicable:
        fam = goals[i]["target"].split("_")[1]
        fam_map.setdefault(fam, []).append(i)
    tr, va, te = [], [], []
    for fam, idxs in fam_map.items():
        rng.shuffle(idxs)
        n = len(idxs)
        tr += idxs[: int(n * 0.6)]
        va += idxs[int(n * 0.6): int(n * 0.8)]
        te += idxs[int(n * 0.8):]
    na = sorted(noapply)
    rng.shuffle(na)
    nna = len(na)
    na_tr, na_va, na_te = na[: int(nna * 0.6)], na[int(nna * 0.6): int(nna * 0.8)], na[int(nna * 0.8):]
    return {"train": sorted(tr + na_tr), "val": sorted(va + na_va), "test": sorted(te + na_te)}


TOY_FIXTURE = {
    "families": ["widget", "gadget"],
    "roles": ["create", "read"],
    "intents": ["build a widget", "find a widget by id", "build a gadget", "find a gadget by id"],
    "ids": ["mech_widget_create", "mech_widget_read", "mech_gadget_create", "mech_gadget_read"],
    "goals": [
        {"goal_id": "t1", "text": "assemble a sprocket", "category": "independent_paraphrase",
         "applicable": True, "target": "mech_widget_create"},
        {"goal_id": "t2", "text": "locate a sprocket", "category": "independent_paraphrase",
         "applicable": True, "target": "mech_widget_read"},
        {"goal_id": "t3", "text": "construct a doodad", "category": "independent_paraphrase",
         "applicable": True, "target": "mech_gadget_create"},
        {"goal_id": "t4", "text": "build a widget", "category": "verbatim", "applicable": True,
         "target": "mech_widget_create"},
        {"goal_id": "t5", "text": "rotate the turbine blades", "category": "no_applicable",
         "applicable": False, "target": None},
    ],
}


def run_smoke(model_dir: Path, outdir: Path) -> dict:
    """Toy end-to-end pipeline for DESIGN liveness probing only."""
    outdir.mkdir(parents=True, exist_ok=True)
    fx = TOY_FIXTURE
    E = Embedder(model_dir)
    intents, ids = fx["intents"], fx["ids"]
    goals = fx["goals"]
    cos_all = cosine_matrix(E, [g["text"] for g in goals], intents)
    import numpy as np
    rows = []
    for gi, g in enumerate(goals):
        cos = [(ids[j], float(cos_all[gi, j])) for j in range(len(ids))]
        argmax = max(cos, key=lambda t: t[1])[0]
        lex = lexical_argmax(g["text"], intents, ids)
        rows.append({"goal_id": g["goal_id"], "cos_argmax": argmax, "lexical": lex,
                     "target": g["target"]})
    write_json(outdir / "smoke_evidence.json", rows)
    return {"status": "smoke_ok", "n_goals": len(goals), "embedding_dim": E.dim, "rows": rows}


def run_confirmatory(model_dir: Path, outdir: Path, packet_out: Path, expected_code_sha256: str,
                    toy: bool = False) -> dict:
    import numpy as np

    t0 = time.time()
    if toy:
        fx = TOY_FIXTURE
        mechs = [{"mechanism_id": mid, "intent": intent, "parameter_slots": [], "action_template": {},
                  "preconditions": {}, "postconditions": {}, "auth_scope": None, "freshness": {},
                  "applicability_guards": {}, "verification_rule": {}, "failure_boundary": {},
                  "repair_scope": {}, "evidence": [], "confidence": 1.0, "invalidated": False}
                 for mid, intent in zip(fx["ids"], fx["intents"])]
        goals = fx["goals"]
        screen = {"max_jaccard_primary": 0.0, "n_primary_passed": 0, "vocab_overlap": [],
                  "n_substring_violations": 0, "n_primary_substring_violations": 0}
        intents = list(fx["intents"])
        ids = list(fx["ids"])
        families = [mid.split("_")[1] for mid in ids]
        fsha = gsha = "toy"
    else:
        # ---------- fixture + canaries ----------
        fsha, gsha, registry = build_fixture(outdir / "fixture_build")
        if fsha != FIXTURE_SHA256 or gsha != GOALS_SHA256:
            raise RuntimeError(f"fixture canary mismatch at EXECUTE: {fsha} != {FIXTURE_SHA256} or {gsha} != {GOALS_SHA256}")
        mechs = registry["mechanisms"]
        goals = registry["goals"]
        screen = registry["contamination_screen"]
        intents = [m["intent"] for m in mechs]
        ids = [m["mechanism_id"] for m in mechs]
        families = [m["mechanism_id"].split("_")[1] for m in mechs]
    # ---------- splits ----------
    splits = split_goal_indices(goals)
    write_json(outdir / "evidence/splits.json", splits)
    # ---------- embedder + per-goal cosine ----------
    E = Embedder(model_dir)
    goal_texts = [g["text"] for g in goals]
    cos_all = cosine_matrix(E, goal_texts, intents).tolist()
    dim = E.dim
    # ---------- arms ----------
    rng_arm = random.Random(SEED_ARM_ORDER)
    arm_order = ["A-CANDIDATE-GATED", "B-EMBEDDING-ARGMAX", "B-LEXICAL-OVERLAP",
                 "B-FAMILY-ONLY-EMBEDDING", "B-ROLE-ONLY-EMBEDDING", "B-RANDOM",
                 "B-INTERNAL-ID-ORACLE", "NC-EMBEDDING-SHUFFLE"]
    rng_arm.shuffle(arm_order)
    per_goal = []
    applicable_idx = [i for i, g in enumerate(goals) if g["applicable"]]
    noapply_idx = [i for i, g in enumerate(goals) if not g["applicable"]]
    for i, g in enumerate(goals):
        cos = [(ids[j], cos_all[i][j]) for j in range(len(ids))]
        row = {
            "goal_id": g["goal_id"], "text": g["text"], "category": g["category"],
            "applicable": g["applicable"], "target": g["target"],
            "family": (g["target"] or "").split("_")[1] if g["target"] else None,
            "max_cos": max(c for _, c in cos),
            "arginmax_cos_id": max(cos, key=lambda t: t[1])[0],
        }
        row["arm_embedding_argmax"] = max(cos, key=lambda t: t[1])[0]
        row["arm_lexical"] = lexical_argmax(g["text"], intents, ids)
        row["arm_family_only"] = family_only_argmax(cos, sorted(set(families)))
        row["arm_role_only"] = role_only_argmax(cos, ROLES)
        row["arm_random"] = random.Random(SEED_SHUFFLE + i).choice(ids)
        row["arm_oracle"] = g["target"]
        row["arm_shuffle"] = shuffled_argmax(cos, intents, SEED_SHUFFLE + i)
        per_goal.append(row)
    write_json(outdir / "evidence/per_goal_arms.json", per_goal)
    # ---------- gate fitting ----------
    tr = [i for i in splits["train"]]
    va = [i for i in splits["val"]]
    te = [i for i in splits["test"]]
    train_x = [per_goal[i]["max_cos"] for i in tr]
    train_y = [1 if goals[i]["applicable"] else 0 for i in tr]
    val_x = [per_goal[i]["max_cos"] for i in va]
    val_y = [1 if goals[i]["applicable"] else 0 for i in va]
    gate = fitted_logistic_gate(train_x, train_y, val_x, val_y, seed=SEED_SPLIT)
    # apply gate + margin abstention to every goal
    for i, g in enumerate(goals):
        p = gate["p_of"]([per_goal[i]["max_cos"]])[0]
        cos = [(ids[j], cos_all[i][j]) for j in range(len(ids))]
        sorted_cos = sorted(cos, key=lambda t: -t[1])
        margin = sorted_cos[0][1] - sorted_cos[1][1]
        abstain = (p < gate["lambda"]) or (margin < MARGIN_ABSTAIN_THRESHOLD)
        per_goal[i]["p_applicable"] = p
        per_goal[i]["margin"] = margin
        per_goal[i]["gated"] = "UNKNOWN" if abstain else sorted_cos[0][0]
    write_json(outdir / "evidence/per_goal_full.json", per_goal)
    # ---------- primary metrics (independent paraphrase set) ----------
    primary = [r for r in per_goal if r["category"] == "independent_paraphrase"]
    if (not toy) and screen["max_jaccard_primary"] >= CONTAM_THRESHOLD:
        raise RuntimeError("contamination screen failed on primary set")
    def acc(rows, key):
        a = [1 for r in rows if r[key] == r["target"]]
        return len(a) / len(rows) if rows else None
    m_primary_treatment = acc(primary, "arm_embedding_argmax")
    m_primary_lexical = acc(primary, "arm_lexical")
    m_primary_family_only = acc(primary, "arm_family_only")
    m_primary_role_only = acc(primary, "arm_role_only")
    m_primary_random = acc(primary, "arm_random")
    m_primary_shuffle = acc(primary, "arm_shuffle")
    m_oracle = acc([r for r in primary if r["applicable"]], "arm_oracle")
    diff_tl = [(r["family"], (1 if r["arm_embedding_argmax"] == r["target"] else 0) -
                            (1 if r["arm_lexical"] == r["target"] else 0)) for r in primary]
    boot_tl = family_blocked_paired_bootstrap(diff_tl)
    diff_tf = [(r["family"], (1 if r["arm_embedding_argmax"] == r["target"] else 0) -
                             (1 if r["arm_family_only"] == r["target"] else 0)) for r in primary]
    boot_tf = family_blocked_paired_bootstrap(diff_tf)
    overlap = [r for r in per_goal if r["category"] == "overlap_paraphrase"]
    o_treat = acc(overlap, "arm_embedding_argmax")
    o_lex = acc(overlap, "arm_lexical")
    m_verbatim = acc([r for r in per_goal if r["category"] == "verbatim"], "arm_embedding_argmax")
    # ---------- calibration metrics ----------
    executed = [r for r in per_goal if r["gated"] != "UNKNOWN"]
    wrong_exec = [r for r in executed if r["gated"] != r["target"]]
    pooled_fa = len(wrong_exec) / len(executed) if executed else None
    answered_appl = [r for r in executed if r["applicable"]]
    coverage = len(answered_appl) / len(applicable_idx) if applicable_idx else None
    sel_risk = sum(1 for r in answered_appl if r["gated"] != r["target"]) / len(answered_appl) if answered_appl else None
    ref_answered = [r for r in per_goal if r["applicable"]]
    ref_risk = sum(1 for r in ref_answered if r["arm_embedding_argmax"] != r["target"]) / len(ref_answered) if ref_answered else None
    abst = [r for r in per_goal if r["gated"] == "UNKNOWN"]
    tp_abstain = sum(1 for r in abst if not r["applicable"])
    fp_abstain = sum(1 for r in abst if r["applicable"])
    unk_prec = tp_abstain / (tp_abstain + fp_abstain) if (tp_abstain + fp_abstain) else None
    ps = [r["p_applicable"] for r in per_goal]
    ys = [1 if r["applicable"] else 0 for r in per_goal]
    ece, ece_detail = ece_global(ps, ys)
    # ECE bootstrap upper (resample goals, 1000 reps)
    rng_ece = random.Random(SEED_BOOTSTRAP + 1)
    ece_vals = []
    for _ in range(1000):
        samp = [rng_ece.randrange(len(per_goal)) for _ in per_goal]
        s_ps = [ps[k] for k in samp]
        s_ys = [ys[k] for k in samp]
        e, _ = ece_global(s_ps, s_ys)
        ece_vals.append(e)
    ece_upper = sorted(ece_vals)[950]
    abst_applicable = sum(1 for r in answered_appl if r["gated"] == "UNKNOWN") / len(answered_appl) if answered_appl else None
    na_set = [r for r in per_goal if not r["applicable"]]
    abst_noapply = sum(1 for r in na_set if r["gated"] == "UNKNOWN") / len(na_set) if na_set else None
    # ---------- metrics + controls assembly ----------
    metrics = {
        "m_primary_treatment_acc": m_primary_treatment,
        "m_primary_lexical_acc": m_primary_lexical,
        "m_primary_treatment_advantage_over_lexical": boot_tl["mean"],
        "m_primary_advantage_lower95": boot_tl["lower_0.95"],
        "m_primary_treatment_vs_family_only_advantage": boot_tf["mean"],
        "m_primary_treatment_vs_family_only_lower95": boot_tf["lower_0.95"],
        "m_primary_family_only_acc": m_primary_family_only,
        "m_primary_role_only_acc": m_primary_role_only,
        "m_primary_random_acc": m_primary_random,
        "m_primary_shuffle_acc": m_primary_shuffle,
        "m_oracle_acc": m_oracle,
        "m_overlap_treatment_acc": o_treat,
        "m_overlap_lexical_acc": o_lex,
        "m_overlap_treatment_advantage": (o_treat or 0.0) - (o_lex or 0.0),
        "m_advantage_gradient_interaction": boot_tl["mean"] - ((o_treat or 0.0) - (o_lex or 0.0)),
        "m_verbatim_acc": m_verbatim,
        "n_primary": len(primary), "n_overlap": len(overlap), "n_goals_total": len(goals),
        "n_applicable": len(applicable_idx), "n_no_applicable": len(noapply_idx),
        "embedding_dim": dim,
        "contamination_max_jaccard_primary": screen["max_jaccard_primary"],
        "n_primary_passed_screen": screen["n_primary_passed"],
        "vocab_overlap": screen["vocab_overlap"],
        "n_substring_violations": screen["n_substring_violations"],
        "n_primary_substring_violations": screen["n_primary_substring_violations"],
        "cal_pooled_false_accept": pooled_fa,
        "cal_coverage": coverage,
        "cal_selective_risk": sel_risk,
        "cal_selective_risk_ref_argmax": ref_risk,
        "cal_unknown_precision": unk_prec,
        "cal_ece_global": ece,
        "cal_ece_upper95": ece_upper,
        "cal_abstain_applicable_rate": abst_applicable,
        "cal_abstain_noapply_rate": abst_noapply,
        "cal_lambda": gate["lambda"],
        "cal_gate_w": gate["w"], "cal_gate_b": gate["b"],
        "cal_gate_mu": gate["mu"], "cal_gate_sd": gate["sd"],
        "n_executed": len(executed), "n_abstained": len(abst),
    }
    controls = {
        "C1-PC-VERBATIM": {"expected": 1.0, "observed": m_verbatim,
                           "pass": m_verbatim == 1.0, "note": "10 verbatim intent goals, applicable"},
        "C2-NC-NO-APPLICABLE": {"expected": "abstention >= 0.50 on no-applicable",
                                "observed": abst_noapply, "pass": (abst_noapply or 0.0) >= 0.50,
                                "note": "gate+margin abstention on no-applicable goals"},
        "C3-ORACLE-CEILING": {"expected": 1.0, "observed": m_oracle,
                              "pass": m_oracle == 1.0, "note": "B-INTERNAL-ID-ORACLE"},
        "C4-SHUFFLE-SENSITIVITY": {"expected": "~chance <= 0.5", "observed": m_primary_shuffle,
                                   "pass": (m_primary_shuffle or 1.0) <= 0.5,
                                   "note": "label-permuted embedding argmax"},
        "C5-RANDOM-SANITY": {"expected": "~1/20 = 0.05", "observed": m_primary_random,
                             "pass": abs((m_primary_random or 1.0) - 0.05) <= 0.10,
                             "note": "uniform random over 20 mechanisms"},
        "C6-CONTAMINATION-SCREEN": {"expected": "primary set: max Jaccard < 0.20, vocab disjoint, zero substrings",
                                    "observed": {"max_jaccard_primary": screen["max_jaccard_primary"],
                                                 "vocab_overlap": screen["vocab_overlap"],
                                                 "n_primary_substring_violations": screen["n_primary_substring_violations"]},
                                    "pass": (screen["max_jaccard_primary"] < CONTAM_THRESHOLD
                                             and not screen["vocab_overlap"]
                                             and screen["n_primary_substring_violations"] == 0),
                                    "note": "authoring provenance screen against EVERY registry intent"},
        "C7-MODEL-CANARY": {"expected": "onnx/tokenizer sha256 match",
                            "observed": {"onnx": MODEL_ONNX_SHA256, "tokenizer": TOKENIZER_JSON_SHA256},
                            "pass": True, "note": "verified inside Embedder init"},
        "C8-FIXTURE-CANARY": {"expected": f"fixture={FIXTURE_SHA256} goals={GOALS_SHA256}",
                              "observed": {"fixture": fsha, "goals": gsha},
                              "pass": toy or (fsha == FIXTURE_SHA256 and gsha == GOALS_SHA256),
                              "note": "deterministic regeneration"},
        "C9-CODE-CANARY": {"expected": f"run.py sha256 == {expected_code_sha256}",
                           "observed": sha256_bytes(Path(__file__).read_bytes()),
                           "pass": sha256_bytes(Path(__file__).read_bytes()) == expected_code_sha256,
                           "note": "byte-identical transcription from prereg.md"},
        "C10-DEGENERACY-SCREEN": {"expected": "lexical floor < 0.90, oracle == 1.0",
                                  "observed": {"lexical": m_primary_lexical, "oracle": m_oracle},
                                  "pass": (m_primary_lexical or 1.0) < 0.90 and m_oracle == 1.0,
                                  "note": "benchmark dynamic range certificate"},
    }
    # ---------- decision rule (frozen) ----------
    validity_fail = [cid for cid, c in controls.items() if not c["pass"]]
    primary_pass = (metrics["m_primary_advantage_lower95"] > 0.0
                    and metrics["m_primary_treatment_vs_family_only_lower95"] > 0.0)
    cal_gates = {
        "pooled_false_accept_le_0.10": (pooled_fa or 1.0) <= 0.10,
        "coverage_ge_0.50": (coverage or 0.0) >= 0.50,
        "selective_risk_le_ref_plus_0.05": (sel_risk or 1.0) <= (ref_risk or 1.0) + 0.05,
        "unknown_precision_ge_0.85": (unk_prec or 0.0) >= 0.85,
        "ece_global_le_0.15": ece <= 0.15,
        "ece_upper_le_0.18": ece_upper <= 0.18,
        "abstain_noapply_ge_0.50": (abst_noapply or 0.0) >= 0.50,
    }
    cal_pass = all(cal_gates.values())
    if validity_fail:
        status, outcome = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
    elif primary_pass and cal_pass:
        status, outcome = "COMPLETE", "SUPPORTS"
    elif primary_pass and not cal_pass:
        status, outcome = "COMPLETE", "MIXED"
    else:
        status, outcome = "COMPLETE", "FALSIFIES"
    observations = [
        {"id": "OBS-1-MODEL-PROBE", "value": {"dim": dim,
             "probe": "synonyms ~0.5-0.8, unrelated ~0.0 (design-time probe; not confirmatory)"}},
        {"id": "OBS-2-SPLITS", "value": {"train": len(splits["train"]), "val": len(splits["val"]),
                                         "test": len(splits["test"])}},
        {"id": "OBS-3-GATE-FITTED", "value": {"w": metrics["cal_gate_w"], "b": metrics["cal_gate_b"],
                                              "lambda": metrics["cal_lambda"]}},
        {"id": "OBS-4-ABSTAIN-RATES", "value": {"applicable": abst_applicable, "no_applicable": abst_noapply}},
        {"id": "OBS-5-CONTAMINATION", "value": {"max_jaccard_primary": screen["max_jaccard_primary"],
                                                 "n_primary_passed": screen["n_primary_passed"]}},
        {"id": "OBS-6-AUTHORING-PROVENANCE", "value": {"vocab_overlap": screen["vocab_overlap"],
                                                        "n_substring_violations": screen["n_substring_violations"],
                                                        "n_primary_substring_violations": screen["n_primary_substring_violations"]}},
        {"id": "OBS-7-ECE", "value": {"ece": ece, "upper95": ece_upper, "detail": ece_detail}},
        {"id": "OBS-8-CANARIES", "value": {"fixture": fsha, "goals": gsha,
                                            "code": sha256_bytes(Path(__file__).read_bytes())}},
        {"id": "OBS-9-RUNTIME-SECONDS", "value": round(time.time() - t0, 1)},
        {"id": "OBS-10-ARM-ORDER", "value": arm_order},
    ]
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": [
            {"path": str(outdir / "fixture_build/fixture.json"), "sha256": fsha, "role": "fixture"},
            {"path": str(outdir / "fixture_build/goals.json"), "sha256": gsha, "role": "fixture"},
            {"path": str(outdir / "evidence/per_goal_full.json"), "sha256": sha256_bytes((outdir / "evidence/per_goal_full.json").read_bytes()), "role": "raw"},
            {"path": str(outdir / "evidence/per_goal_arms.json"), "sha256": sha256_bytes((outdir / "evidence/per_goal_arms.json").read_bytes()), "role": "raw"},
            {"path": str(outdir / "evidence/splits.json"), "sha256": sha256_bytes((outdir / "evidence/splits.json").read_bytes()), "role": "derived"},
        ],
        "observations": observations,
        "validity_notes": [],
        "unresolved": [],
    }
    if not toy:
        write_json(packet_out / "result.json", result)
    else:
        write_json(outdir / "toy_metric_run.json", result)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze-fixture", metavar="OUTDIR")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--toy-full", action="store_true")
    ap.add_argument("--expected-code-sha256", metavar="SHA256")
    ap.add_argument("model_dir", nargs="?")
    ap.add_argument("outdir", nargs="?")
    args = ap.parse_args()
    sys_path_setup()
    if args.freeze_fixture:
        out = Path(args.freeze_fixture)
        fsha, gsha, registry = build_fixture(out)
        print("FIXTURE_SHA256=" + fsha)
        print("GOALS_SHA256=" + gsha)
        print("N_MECHANISMS=" + str(len(registry["mechanisms"])))
        print("N_GOALS=" + str(len(registry["goals"])))
        cats = {}
        for g in registry["goals"]:
            cats[g["category"]] = cats.get(g["category"], 0) + 1
        print("CATEGORY_COUNTS=" + json.dumps(cats))
        s = registry["contamination_screen"]
        print("MAX_JACCARD_PRIMARY=" + str(s["max_jaccard_primary"]))
        print("VOCAB_OVERLAP=" + json.dumps(s["vocab_overlap"]))
        print("N_SUBSTRING_VIOLATIONS=" + str(len(s["substring_violations"])))
        print("ALL_TEMPLATES_BOUND=" + str(registry["template_binding"]["all_templates_bound"]))
        return 0
    if args.smoke:
        if not args.model_dir or not args.outdir:
            ap.error("--smoke requires MODEL_DIR OUTDIR")
        r = run_smoke(Path(args.model_dir), Path(args.outdir))
        print(json.dumps(r, indent=2, default=str))
        return 0
    if not args.model_dir or not args.outdir:
        ap.error("MODEL_DIR OUTDIR required")
    if args.toy_full:
        model_dir = Path(args.model_dir)
        outdir = Path(args.outdir)
        result = run_confirmatory(model_dir, outdir, outdir, "toy", toy=True)
        print(json.dumps({"status": result["status"], "outcome": result["outcome"],
                          "metrics": result["metrics"]}, indent=2, default=str))
        return 0
    if not args.expected_code_sha256 or len(args.expected_code_sha256) != 64:
        ap.error("--expected-code-sha256 required (declared in prereg.md)")
    model_dir = Path(args.model_dir)
    outdir = Path(args.outdir)
    packet_out = Path(__file__).resolve().parents[2] / "experiments" / EXPERIMENT_ID
    result = run_confirmatory(model_dir, outdir, packet_out, args.expected_code_sha256)
    print(json.dumps({k: result[k] for k in ("status", "outcome", "metrics")}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())```


---

## 14. Declaration

This preregistration is complete prior to any outcome-bearing execution. All
design choices, thresholds, decision rules, fixture data, model pinning and the
entire outcome-bearing code are declared above and frozen by the deterministic
freezer (freeze.json hashes this file). No modification will be made after
freeze.json exists. The primary scientific comparison is fitting-free; the
calibration arm is secondary; every control has a non-empty, construction-
guaranteed denominator; every outcome branch is reachable.

**Frozen by:** [deterministic freezer at freeze time]
**Freeze timestamp:** [recorded in freeze.json]
