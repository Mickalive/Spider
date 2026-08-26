# INTEL CYCLE 1 — REPAIR ROUND 3 RESTORATION NOTE

- Answers: `INTEL_AUDIT cycle1_run32796176172` (gate **REVISE**; round 2 delivered an empty snapshot,
  tree identical to base `0a55649`). Required fixes addressed here: **RF-A…RF-E**.
- Nature of this round: **restoration of commit `1e51a5c`** ("Intel cycle 1 repair 1: reproduction")
  byte-exact, plus **documentary deltas only**. No data, raw evidence, code logic, metric definition,
  condition, exclusion rule, or success-rule element changed. The preregistered test is neither
  weakened nor retuned.

## Pre-edit integrity check (RF-A precondition)

`sha256sum -c results/intel/reproductions/cycle1_repair1_SHA256SUMS.txt` executed immediately after
materializing the 23 restored paths and **before any edit**: **18/18 OK**. The manifest itself is
byte-identical to round 1; its scope statement needed no refresh because none of its 18 listed files
changed.

## Changed files (complete enumeration)

| Path | Fix | Change |
|---|---|---|
| `reports/intel/reproductions/cycle1_report.md` | RF-B, RF-C, RF-E | §2 erratum: constant-dummy-text clause replaced by the stable-controls sentence from gate `CYCLE_32792931901` RF1; cost footnote restated as "≈12–13 total; exact split unreconciled at artifact level; no metric impact"; REPAIR ROUND 3 delivery banner added |
| `state/intel_reproduction.json` | RF-D (+RF-B, RF-C) | `repair_round` 1→3; new `repair_round_3_provenance` block enumerating this round; `honest_caveats[2]` stable-controls sentence; `honest_caveats[3]` reconciled cost wording; `strongest_defensible_wording` + ceiling note aligned verbatim to the round-1 gate's binding maximum-defensible text; forbidden-wordings item on constant-dummy-text citations added; `awaiting` updated |
| `results/intel/reproductions/cycle1_repair3_restoration_note.md` | RF-D | this note |

## Byte-identical frozen materials (unchanged)

- `intel/experiments/sgdr_repro/` — 10 code files
- `intel/prereg/cycle1_sgdr_prereg.md`, `intel/prereg/cycle1_repair1_provenance_attestation.md`
- `results/intel/reproductions/cycle1/` — 8 evidence files
- `results/intel/reproductions/cycle1_repair1_SHA256SUMS.txt`

## Delivery verification (RF-E)

1. Repro branch tip ≠ `origin/lab/intel` (`0a55649`) after commit.
2. All restored/updated paths present: 10 code + 2 prereg + 1 report + 8 evidence + 1 manifest +
   1 state + this note = **24 paths**.
3. Rerunning `sgdr_repro.evaluate` on the restored caches regenerates
   `results/intel/reproductions/cycle1/retrieval_eval.json` **byte-identically**
   (sha256 `342ec130d0a052d0201ecaf9e9ce0ef6876f1d4a529e6987390a859c99db5061`);
   `python3 -m sgdr_repro.selftest` → **7/7 PASS**.
