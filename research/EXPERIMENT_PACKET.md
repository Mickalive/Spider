# SPIDER Research 2.0 — canonical experiment packet and inter-agent transmission contract

Path: `research/experiments/<experiment_id>/`

This document is the binding transmission protocol between autonomous agents. Agents do not hand work to one another through chat memory, Actions logs, unstated assumptions or prose summaries. They hand over the canonical experiment packet below.

The machine creates `request.json`. DESIGN fills `spec.json` and `prereg.md`. The deterministic freezer creates `freeze.json`. After freeze, those inputs are immutable. EXECUTE adds measurements. AUDIT adds an independent attack. DIRECTOR adds the bounded decision and durable handoff. Downstream stages may read upstream files but must never rewrite them.

## 1. Transmission invariants

Every stage must preserve these identities exactly: `experiment_id`, `lane`, frozen claim ids, frozen decision rule, control identities and evidence paths.

Information classes must remain distinct:

`RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION -> AUDIT FINDING -> DECISION -> HANDOFF`

A downstream agent may challenge an upstream interpretation, but it may not silently turn an interpretation into an observation or a missing measurement into a negative result.

Mandatory-key semantics are strict:

- omitted mandatory key = invalid packet;
- `null` = explicitly unknown/not available;
- `[]` or `{}` = explicitly checked and empty/not applicable;
- infrastructure or substrate failure must never be encoded as scientific falsification;
- if a value cannot be obtained, keep the mandatory key and explain why in `validity_notes`, `required_fixes`, `unresolved` or the appropriate stage field.

No material fact required by the next stage may exist only in an Actions log. Human-readable Markdown is explanatory; canonical JSON is the machine handoff.

Evidence references should use stable repository-relative paths and, where practical, hashes. Do not cite a vague narrative when an exact artifact, metric, control or packet field exists.

## 2. Stage-to-stage contract

### REQUEST -> DESIGN

DESIGN receives:

- `request.json`;
- lane charter and claim registry;
- accepted Codex evidence;
- when present, the exact `parent_handoff` referenced by `request.json`.

If a parent handoff exists, DESIGN must preserve its four-way distinction: `established`, `rejected`, `unknown`, `do_not_assume`. It may depart from the recommended next action when newer evidence warrants it, but must not silently invert inherited evidence.

DESIGN emits only `spec.json` and `prereg.md`.

### DESIGN -> EXECUTE

EXECUTE receives the exact frozen `request.json`, `spec.json`, `prereg.md`, `freeze.json`. It executes the frozen design rather than re-designing after outcomes are visible.

EXECUTE emits `result.json`, `report.md`, `provenance.json` plus raw/derived artifacts where practical.

### EXECUTE -> AUDIT

AUDIT receives the entire frozen design plus producer `result.json`, `report.md`, `provenance.json` and referenced raw evidence. It must use the same metric/control identifiers when recomputing or disputing them.

AUDIT emits only `audit.json` and never edits producer evidence.

### AUDIT -> DIRECTOR

DIRECTOR receives frozen design, producer evidence and independent audit. It may bound a claim more narrowly than either producer or auditor, but may not create new measurements.

DIRECTOR emits only `verdict.json` and `handoff.json`.

### DIRECTOR -> NEXT DESIGN / CODEX

`handoff.json` is the durable bridge to the next experiment. `prepare_lane.py` records an immutable path+hash reference to the prior handoff in the next `request.json` when one exists. The Codex also consumes finalized packets.

Cross-lane scientific inheritance should occur through accepted Codex evidence or exact immutable packet/artifact references, never through an agent's unrecorded recollection of another lane.

## 3. `spec.json` required fields

- `experiment_id`
- `lane`
- `claim_ids`
- `question`
- `hypothesis`
- `falsifier`
- `baselines`
- `positive_control`
- `null_control`
- `measurement_validity`
- `decision_rule`
- `product_consequence_positive`
- `product_consequence_negative`
- `estimated_cost`
- `expected_information_gain`

The scientific content of these fields is deliberately flexible. The contract standardizes transmission, not the scientific hypothesis.

## 4. `result.json` — producer handoff

Required top-level shape:

```json
{
  "schema_version": 1,
  "experiment_id": "EXP-...",
  "lane": "graph|physics|runtime|product|intel|frontier",
  "status": "COMPLETE|BLOCKED|MEASUREMENT_INVALID",
  "outcome": "SUPPORTS|FALSIFIES|MIXED|INCONCLUSIVE|NOT_APPLICABLE",
  "metrics": {},
  "controls": {},
  "artifacts": [],
  "observations": [],
  "validity_notes": [],
  "unresolved": []
}
```

`status` describes whether the measurement transaction completed validly; it is not the scientific answer. A valid negative experiment is normally `status=COMPLETE` with `outcome=FALSIFIES` or `MIXED`, not an execution failure.

`metrics` is a JSON object with stable names and explicit values/units where relevant. It may be empty only when the frozen experiment is genuinely non-quantitative, with that fact explained in `validity_notes`.

`controls` is a JSON object keyed by stable control/baseline identifiers. Each entry should record expected behavior, observed behavior, pass/fail/unknown and exact evidence references where practical.

`artifacts` is a JSON list. Prefer entries like `{"path":"...","sha256":"...","role":"raw|derived|fixture|code"}`. Empty is valid only when no durable artifact beyond the canonical packet exists.

`observations` contains direct observations, not interpretations. `validity_notes` records representation loss, environment limitations and measurement caveats. `unresolved` records questions the producer cannot settle from this run.

`report.md` may explain and interpret these fields but must not exceed the frozen claim or contradict `result.json` silently.

## 5. `provenance.json`

It must identify enough provenance to understand or reproduce the measurement: GitHub run id, relevant commits, datasets/fixtures, code paths, environment and hashes/paths of material artifacts where practical. Exact commands may be included when they materially affect reproduction.

## 6. `audit.json` — independent handoff

Required top-level shape:

```json
{
  "schema_version": 1,
  "experiment_id": "EXP-...",
  "lane": "...",
  "status": "PASS|REVISE|FAIL|MEASUREMENT_INVALID|BLOCKED",
  "producer_claim_supported": false,
  "required_fixes": [],
  "validity_findings": [],
  "baseline_findings": [],
  "recomputed_metrics": {},
  "claim_ceiling": "...",
  "evidence_refs": [],
  "unresolved": []
}
```

The auditor references producer metric/control identifiers rather than renaming them. Disagreement is explicit. `producer_claim_supported=false` means the producer's claimed ceiling is not justified as written; it does not automatically mean the underlying scientific hypothesis is globally false.

## 7. `verdict.json` — bounded decision

Required top-level shape:

```json
{
  "schema_version": 1,
  "experiment_id": "EXP-...",
  "lane": "...",
  "decision": "...",
  "claim_updates": [],
  "product_action": "...",
  "promote_to_product": false,
  "continue": false,
  "next_question": null,
  "reason": "...",
  "evidence_refs": []
}
```

Every `claim_updates` event is an object with `claim_id`, registry-valid `status`, and `reason`. The Director must ground decisions in upstream evidence/audit references rather than restating confidence as evidence.

`continue` controls immediate chaining only. `false` may still carry a `next_question` for the scheduled pulse or another lane.

## 8. `handoff.json` — durable inheritance

Required top-level shape:

```json
{
  "schema_version": 1,
  "experiment_id": "EXP-...",
  "lane": "...",
  "target_lane": "graph|physics|runtime|product|intel|frontier|null",
  "next_question": null,
  "why_next": "...",
  "carry_forward": {
    "established": [],
    "rejected": [],
    "unknown": [],
    "do_not_assume": []
  },
  "dependencies": [],
  "evidence_refs": [],
  "recommended_action": "..."
}
```

`handoff.json` is not a summary of everything that happened. It is the minimum lossless bridge needed for another fresh-context agent to continue correctly.

`established` contains only what the finalized packet justifies at the stated claim ceiling. `rejected` contains bounded rejected hypotheses/mechanisms, not broader domains unless the evidence really closes them. `unknown` contains unresolved facts. `do_not_assume` explicitly preserves dangerous non-conclusions, invalid measurements, scope boundaries and tempting over-generalizations.

`next_question` must equal `verdict.json.next_question`. `target_lane` is advisory routing metadata; it does not itself authorize cross-lane writes. `dependencies` identifies exact prerequisites. `evidence_refs` should point to the packet/artifacts that justify the carry-forward state.

## 9. Failure transmission

If a stage cannot complete, `failure.json` records stage, category, message, retryability and durable diagnostic context. Operational failure is not scientific falsification. A later retry must resume from the last valid checkpoint and must not rewrite frozen scientific inputs.
