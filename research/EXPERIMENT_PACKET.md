# Standard Research 2.0 experiment packet

Path: `research/experiments/<experiment_id>/`

The machine creates `request.json`. The DESIGN stage fills `spec.json` and `prereg.md`. The deterministic freezer then creates `freeze.json`. After that, frozen inputs are immutable.

## `spec.json` required fields

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

## Execution outputs

`result.json` must contain `status`, `metrics`, `controls`, and `artifacts`.

`provenance.json` must identify the GitHub run, exact commits, datasets/fixtures, code paths and environment needed to understand the measurement.

`report.md` explains what happened without exceeding the frozen claim.

## Independent audit

`audit.json` must contain:

- `status`: `PASS | REVISE | FAIL | MEASUREMENT_INVALID | BLOCKED`
- `producer_claim_supported`: boolean
- `required_fixes`
- `validity_findings`
- `baseline_findings`
- `recomputed_metrics`
- `claim_ceiling`

The auditor may not modify producer evidence.

## Verdict

`verdict.json` must contain `decision`, `claim_updates`, `product_action`, `promote_to_product`, `continue`, `next_question`, and `reason`.

A `continue=false` decision disables only immediate chaining. It does not permanently close a broad lane; scheduled pulses may still ask the lane for a materially orthogonal next question unless a human pause exists.

## Failure

If any stage cannot complete, `failure.json` records stage, category, message, retryability and exact next action. Infrastructure failure is not scientific falsification.
