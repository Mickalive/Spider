# QUARANTINED NON-EVIDENCE — cycle 9 attempt-1 dataset

**Status: QUARANTINED NON-EVIDENCE, OBSERVATION TIER ONLY. Figures in this
directory must NEVER be cited as SPIDER results or as strengthening evidence.**

Integrated byte-faithfully by the INTEL_RESEARCH_DIRECTOR (2026-08-26) from
scout tip `47bccf3` ("Intel cycle 9 repair 0: Scout snapshot",
`origin/cycle/intel/32935080145/scout`, also re-pushed unchanged at
`origin/cycle/intel/32941504002/scout`). Source verified with `diff -r` at
integration time.

## What this is

The FIRST of the TWO live collections of the frozen powered round-4 protocol
(`unbrowse-route-capture-replay-ladder`, confirmatory dispatch run
32935080145). Internal clock 2026-08-26T05:51:04Z -> 06:04:34Z; throwaway
account `spiderc81787723464702` (distinct from the sealed run's
`spiderc81787724909702`). It entered git through the scout persist step's
unscoped `git add -A` (RF-5 infra defect) and was not disclosed by the
original delivery; disclosure, causal attestation and quarantine were
delivered in repair round 1 (`reports/intel/reproductions/cycle8_report.md`
DISCLOSURE ERRATUM D1; `results/intel/reproductions/cycle9_repair1/`) and
verified by audit PASS run 32941504002 (75/75 checks).

## Why it is NOT evidence

- It contains NO `SHA256SUMS.txt`, NO `decision_rule_evaluation.json`, NO
  `evaluator_invocations.json` — mechanically, it was NEVER an evaluator
  input. The single guarded evaluation read only the sealed tree
  (`results/intel/reproductions/cycle8/`).
- All 32 instrument modules are sha256-identical between this tree and the
  sealed tree (both equal erratum table E1.3), so no code differed between
  attempts; the duplication was strictly sequential with distinct session
  materials.
- Verdict INVARIANCE across both datasets was proven twice independently
  (auditor recompute and Reproducer-owned recompute):
  `results/intel/reproductions/cycle9_repair1/dual_collection_robustness.{json,md}`.

## Binding wording constraints (gate CYCLE_32941504002_INTEL_GATE.json)

- Scout-tree figures (petstore 83.58x, cookie 17.90x, form 12.83x,
  demoblaze 30.57x) are barred forever as SPIDER results or strengthening
  evidence. Canonical figures are the sealed tree's
  9.40x / 5.67x / 18.20x / 37.46x.
- Cycle 9 may only be described as a "single GUARDED EVALUATION", never a
  literal single-shot/single-execution/single-collection event; every
  citation of the verdict must carry the dual-collection caveat.

Retained because lane discipline forbids destroying evidence; its existence
and this quarantine label are part of the permanent process-defect record.
