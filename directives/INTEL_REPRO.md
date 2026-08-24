# SPIDER INTEL — REPRODUCTION CONTRACT

The reproducer receives ONE externally sourced mechanism candidate selected by the Intel Scout.

Goal: determine whether the useful effect attributed to that mechanism can be reproduced or clean-room adapted in a SPIDER-relevant setting.

## Mandatory before outcome observation

Freeze in a preregistration file under `intel/prereg/`:
- external mechanism/claim being tested;
- faithful reproduction vs SPIDER adaptation distinction;
- task/data slice;
- metric(s);
- strongest baseline/null;
- success/failure rule;
- contamination and licensing notes;
- implementation version/hash.

## Reproduction rules

- Isolate the mechanism; do not reproduce an entire product unless necessary.
- Use public evidence only.
- Public code may be inspected subject to license notes; incompatible/proprietary code must not be copied.
- Prefer clean-room minimal implementation.
- Do not quietly add stronger models, privileged labels, benchmark hints, hand-authored decompositions or easier tasks that the original mechanism did not require without labeling the adaptation.
- Compare against SPIDER's current relevant baseline and the strongest obvious simple baseline.
- Measure action count/exploration, success, cost/tokens/latency/reliability when relevant, not merely headline accuracy.
- A failed reproduction is a valid result.

## Durable outputs

Write only Intel-scoped code/data/results/reports, principally:
- `intel/experiments/`
- `intel/prereg/`
- `results/intel/reproductions/`
- `reports/intel/reproductions/`
- `state/intel_reproduction.json`

The state file must identify the mechanism_id, source Scout run, exact artifacts, verdict proposed (`REPRODUCED_USEFUL`, `REPRODUCED_NO_ADVANTAGE`, `FAILED_TO_REPRODUCE`, `INCONCLUSIVE`, `MEASUREMENT_INVALID`) and the strongest defensible wording.

Do not edit Graph, Physics, Product, workflows, or accepted Intel ledgers.