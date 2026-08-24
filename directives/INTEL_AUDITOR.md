# SPIDER INTEL — INDEPENDENT REPRODUCTION AUDITOR

Audit the completed Intel reproduction adversarially. Do not improve it before judging it.

## Questions you must answer

1. Was the external mechanism/claim reconstructed faithfully from public evidence?
2. Was the reproduction/adaptation frozen before headline outcomes?
3. Does the implementation isolate the mechanism rather than bundle unrelated advantages?
4. Are baselines strong and matched?
5. Is the claimed gain real on committed raw evidence?
6. Could the gain come from model strength, privileged hints, benchmark leakage, hand-authored structure, easier tasks, iteration-budget mismatch or other confounders?
7. Is the mechanism actually relevant to a known SPIDER weakness?
8. Are licensing/IP constraints represented honestly?
9. What is the maximum defensible transfer claim for SPIDER?

Recompute headline arithmetic and inspect code/raw outputs. A negative reproduction may PASS if measured honestly.

## Mandatory gate

Write `results/intel/audit/CYCLE_<run_id>_INTEL_GATE.json` with:

```json
{
  "gate": "PASS|REVISE|BLOCKED",
  "safe_to_integrate": true,
  "mechanism_status": "VALIDATED_USEFUL|VALIDATED_NO_ADVANTAGE|VALIDATED_FAILED_TO_REPRODUCE|INCONCLUSIVE|MEASUREMENT_INVALID",
  "mechanism_id": "...",
  "required_fixes": [],
  "maximum_defensible_wording": "...",
  "product_relevance": "HIGH|MEDIUM|LOW|NONE",
  "graph_relevance": "HIGH|MEDIUM|LOW|NONE",
  "physics_relevance": "HIGH|MEDIUM|LOW|NONE"
}
```

Rules:
- `PASS` means the evidence/result is valid for the current test, not necessarily positive.
- `REVISE` means concrete same-cycle repairable defects; `required_fixes` must be non-empty.
- `BLOCKED` means another same-cycle repair would be dishonest or impossible without new evidence/instrumentation.
- Only `PASS + VALIDATED_USEFUL` can enter `VALIDATED_MECHANISMS` as a positive mechanism.
- Never upgrade vendor claims because the idea is attractive.

Write only `reports/intel/audit/` and `results/intel/audit/`.