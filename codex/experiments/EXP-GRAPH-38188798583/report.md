# EXECUTE report — EXP-GRAPH-38188798583 (graph, design_contract_version 2)

Frozen inputs were consumed exactly; none was modified. The canonical runner was extracted
byte-for-byte from `prereg.md` and its sha256 verified before any outcome-bearing execution.
This report keeps RAW EVIDENCE, OBSERVATIONS, DERIVED MEASUREMENTS and INTERPRETATION distinct.

## 0. What was run

Exactly as prereg §11 requires:

```
python3 research/experiments/EXP-GRAPH-38188798583/raw_evidence/runner_tframe.py \
    > raw_evidence/runner_result_raw.json 2> raw_evidence/runner_stderr.txt      # exit 0, empty stderr
python3 research/experiments/EXP-GRAPH-38188798583/raw_evidence/runner_tframe.py --mechanics-only \
    > raw_evidence/mechanics_raw.json 2> raw_evidence/mechanics_stderr.txt        # exit 0, empty stderr
```

Runner extraction check: the FROZEN-RUNNER block (`re.search(r"<!-- BEGIN FROZEN-RUNNER -->\n(.*?)\n<!-- END FROZEN-RUNNER -->", ..., re.S)`
plus one trailing newline) has sha256 `4abc67b1bf435940823b7dc1968c3ddfc4fa23f803b6b124f769d95157d2bc62`,
equal to `CANONICAL-RUNNER-SHA256` and to the runner's own runtime `runner_self_sha`. No runner edit was made.

## 1. RAW EVIDENCE (verbatim, uninterpreted)

- `raw_evidence/runner_result_raw.json` (sha256 `b65fb055371ff67290d5087e03b63c0197447167ea05fe98bacf3bc032460608`)
  — full confirmatory output: `status="COMPLETE"`, `invalid_reasons=[]`, `decision="DECIDE_SHIP_A_SCOPED"`,
  `gates={"AXIS-PRIMARY":true,"AXIS-ALTLEX":true,"AXIS-HELDOUT":false}`, `selection_preserved=true`,
  `test_n={"AXIS-PRIMARY":[56,18],"AXIS-ALTLEX":[56,18],"AXIS-HELDOUT":[40,20]}`,
  `embedding_status="BLOCKED: ModuleNotFoundError: No module named 'numpy'"`.
- `raw_evidence/runner_stderr.txt` — empty (sha256 of empty file `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
- `raw_evidence/mechanics-only output` (`raw_evidence/mechanics_raw.json`, sha256
  `339673528147a23f482ea352e5435425b470108a02fef2745803cc98e3aefdae`) — prerequisite/validity evidence:
  calibration `cal_feasible_tframe=true` on all three axes; liveness `tframe_cal_executed=49`,
  `tframe_cal_unresolved=8`; `embedding_status` BLOCKED.
- `raw_evidence/mechanics_stderr.txt` — empty.

Raw per-goal evidence (mechanism, executed boolean, clause booleans, S, target, text hash) is preserved in
`derived/execution_vectors.json` (extracted unmodified from the raw runner output).

## 2. OBSERVATIONS (direct, no interpretation)

- The frozen runner executed to completion with empty stderr on both the confirmatory and mechanics-only passes.
- On the disjoint test split the treatment T-FRAME produced these triplets (coverage / pooled_false_accept / unknown_precision):
  - AXIS-PRIMARY: `0.9464` / `1/18 = 0.05556` / `1.0` (executed 53 of 56 applicable; 4 resolved abstentions; 3 unresolved applicable).
  - AXIS-ALTLEX: `0.9464` / `1/18 = 0.05556` / `1.0` (identical population; executed 53; 4 resolved abstentions).
  - AXIS-HELDOUT: `0.9250` / `2/20 = 0.1000` / `0.8000` (executed 37 of 40 applicable; 10 resolved abstentions; 1 unresolved applicable).
- Selective accuracy on executed applicable goals: PRIMARY `0.90566`, ALTLEX `1.0`, HELDOUT `1.0`.
  PRIMARY test selection is 48/53 (0.90566); the parent's B-LEX-STRONG was 48/56 = 0.8571.
- The single failing gate criterion is HELDOUT `unknown_precision = 0.8000 < 0.85`. HELDOUT `pooled_false_accept`
  is exactly at target (`2/20 = 0.10`) and coverage is met. HELDOUT `unknown_precision_inclusive = 0.85714 >= 0.80`
  (diagnostic passes).
- HELDOUT test false accepts are `oos_010` (`mech_files_create`, S=0) and `oos_014` (`mech_tickets_create`, S=0).
  The 10 HELDOUT test resolved abstentions are 8 OOS rows plus 2 applicable rows (`app_052`, `app_066`, both `C4-COMPLEMENT`).
- Controls under the same runner on the test split:
  - B-LEX-ONLY / gate-free pooled_false_accept `0.2778 / 0.2778 / 0.500`; unknown_precision `null` (0 resolved abstentions).
  - T-LEX-AMBIG (incumbent integer signal) pooled_false_accept `0.1667 / 0.1667 / 0.200`.
  - CTRL-RANDOM-GATE at matched abstention count (20/20/21): pooled_false_accept `0.6111 / 0.6111 / 0.600`, unknown_precision `0.350 / 0.350 / 0.381`.
  - NC-SHUFFLED-LABEL `0.0189 / 0.0377 / 0.0811`; B-RANDOM-ROLE `0.0943 / 0.1132 / 0.0270`; B-INCUMBENT-KERNEL `0.0`; CTRL-ABSTAIN-ALL coverage `0.0`, unknown_precision `1.0`.
- Contamination fingerprint reproduced exactly: flagged 9 on AXIS-PRIMARY, 9 on AXIS-ALTLEX, 0 on AXIS-HELDOUT;
  max token Jaccard `0.5714` (band 0.60) and max trigram Jaccard `0.5882` (band 0.75) on PRIMARY/ALTLEX over the
  bound population; HELDOUT `0.5714` / `0.5455`.

## 3. DERIVED MEASUREMENTS

Stable identifiers live in `derived/measurements.json`; per-goal vectors in `derived/execution_vectors.json`.

`M-GATE-TRIPLET-PRIMARY` gate_met=true; `M-GATE-TRIPLET-ALTLEX` gate_met=true; `M-GATE-TRIPLET-HELDOUT` gate_met=false.
`M-SELECTION-B-LEX-STRONG` = {PRIMARY 0.90566, ALTLEX 1.0, HELDOUT 1.0}, selection_preserved=true
(>= 0.80 on every axis and >= 0.8584 on PRIMARY). `M-NON-TAUTOLOGY`: T-FRAME's execution vector differs from
gate-free on 47 goals and from the incumbent on 13 goals (all rows). `M-EMBEDDING-STATUS` = BLOCKED (numpy absent).

Independent EXECUTE-side recomputation (not the auditor):
- freeze binding: all four packet hashes (`request/spec/prereg/design_review`) and all three `freeze_artifacts`
  hashes match `freeze.json`; runner sha matches `CANONICAL-RUNNER-SHA256` (`derived/verification.json`).
- split disjointness by construction: no `gid` is both calibration and test on any axis.
- independent recomputation of every test and calibration metric from `execution_vectors` + frozen banks
  matches the raw runner output exactly (0 mismatches over coverage, pooled_false_accept, unknown_precision,
  unknown_precision_inclusive, executed, executed_app, executed_oos, abstained_resolved, selective_acc, unresolved_applicable).
- selection identity: `runner_tframe.comp()` and the parent `runner_frozen.comp()` agree on **all** bound rows
  (422 rows; 306 applicable; 0 mechanism differences), so the preserved selection half is the same code path.
- branch precedence recomputed from the frozen rule yields exactly `DECIDE_SHIP_A_SCOPED`.

## 4. INTERPRETATION

The frozen decision rule fired **branch 3** (`DECIDE_SHIP_A_SCOPED`): on the disjoint test split Arm A (T-FRAME)
meets the gate on AXIS-PRIMARY and AXIS-ALTLEX and preserves the deterministic selection half, but the
held-out mechanism/lexicon axis AXIS-HELDOUT misses one gate criterion, `unknown_precision 0.80 < 0.85`.
The measurement is valid (`VALID=true`): the treatment is live on PRIMARY test (0 < 53 < 56) and unknown_precision
is defined on every test axis, so `status=COMPLETE` (not MEASUREMENT_INVALID).

Top-level `outcome=MIXED` is the honest mapping of this scoped branch: the primary architecture and the frozen
selection half are supported, while the all-three-axis generalization hypothesis stated in `spec.hypothesis` is
partially disconfirmed (HELDOUT alone). Per `spec.falsifier`, a bounded negative on AXIS-HELDOUT alone "falsifies
only the generalization claim (DECIDE_SHIP_A_SCOPED), not the primary architecture". This packet does **not**
self-promote `C-SEMANTIC-RESOLVE`; DIRECTOR/AUDIT adjudicate any claim advance. No product behaviour change is
made and `promote_to_product` is not asserted here.

Direction of the improvement is unambiguous relative to the incumbents on all three axes: T-FRAME
`0.0556/0.0556/0.1000` vs the parent integer-signal gate `0.1667/0.1667/0.2000` vs gate-free
`0.2778/0.2778/0.5000`. The residual HELDOUT precision miss is narrow (8/10 resolved abstentions are OOS; two
applicable `C4-COMPLEMENT` rows dilute the precision), and the inclusive diagnostic (`0.8571`) passes.

Arm B (retrieval/embedding) was not run: the embedding stack is absent (`ModuleNotFoundError: No module named 'numpy'`).
This is recorded as an operational BLOCKED prerequisite, never as a scientific negative, and is not required for a
valid Arm A decision.

## 5. Validity, threats and representation loss

- Design degrees of freedom (disclosed in prereg §9, not removed here): the clause set (C1-SUBOP, C3, C4, C5, C6)
  was developed during DESIGN using the calibration split, the parent's published aggregate failure, and frozen
  OOS-bank phrasings. T-FRAME has zero tunable parameters, so this is not a threshold fit; the confirmatory test
  split was untouched by DESIGN probes.
- Single-split identifiability: pass/fail is bounded to these frozen banks, lexicons and split; no generalization
  beyond them is claimed.
- Contamination: near-threshold goals remain (max token Jaccard 0.5714 vs 0.60; 9 flagged rows removed), the same
  envelope as the parent.
- `unknown_precision` on the test split rests on small resolved-abstention counts (4/4/10); HELDOUT's miss is one
  abstention away from 0.9. This is reported, not hidden.
- Digit stripping (`tokens()` keeps `[a-z]+`) means bare numeric identifiers are unbindable and force C3 abstention:
  a conservative coverage cost, not a false-accept source.
- Arm B BLOCKED is an unavailable-dependency state, not a loss.

## 6. Product consequence

Per `spec.product_consequence_positive`, this scoped outcome licenses T-FRAME only on the generalization surface
actually measured (PRIMARY + ALTLEX). The HELDOUT family is a named generalization gap: `resolve()` must stay
UNKNOWN on inputs resembling that held-out mechanism/lexicon family until repaired. No product change was made by
this stage; no claim was promoted.
