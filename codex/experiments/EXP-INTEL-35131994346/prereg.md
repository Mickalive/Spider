# EXP-INTEL-35131994346 Preregistration

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35131994346
- **Lane**: intel
- **Parent Handoff**: EXP-INTEL-35124660457
- **Inherited Verdict**: MEASUREMENT_INVALID
- **Inherited Next Question**: After the runtime lane removes the first-20 locatableSample cap, does full DOM enumeration confirm that the a→link-inclusive page-type ordering changes between truncated and full-DOM, and does the null-model pairwise agreement exceed chance on full-DOM data?

## Scientific Context

The parent experiment (EXP-INTEL-35124660457) investigated whether first-20 document-order truncation introduces page-type-dependent bias in a→link-inclusive interactive density. The experiment found:

1. **Established**: Truncation discards 62-95% of locatable elements with document-order selection bias
2. **Established**: Random ROLE_MAP null mean 0.52 > observed 0.3, falsifying the hypothesis that 0.3 exceeds chance
3. **Blocked**: The measurement is invalid due to provenance mismatch (committed analyze.py doesn't reproduce stored results)

The provenance mismatch is the immediate blocking issue. The committed `analyze.py` yields FALSIFIED-IN-SETTING (8 tasks, all-role density, C3=false) while the stored `analysis_results.json` yields SURVIVES_CURRENT_TEST (7 tasks, 3-definition filtered, C3=true per DEF-FULL-MAP only).

## Question

Given the provenance mismatch, can the canonical analysis script be identified by reconstructing the 3-definition per-role-filtered analysis from raw evidence, and does this reconstruction match either the committed script or the stored results?

## Hypothesis

The stored analysis_results.json was produced by an uncommitted script that applies per-definition role filtering:
- DEF-FULL-MAP: roles a+button+input+combobox
- DEF-FORM-ONLY: roles button+combobox  
- ISOLATED-A-LINK: role a only

This script also deduplicates cart_1 to 7 tasks. This script can be reconstructed from the raw evidence and the stored results, creating a reproducible canonical analysis.

## Falsifier

If ANY of the following conditions hold, the provenance mismatch is irreconcilable:
1. No reconstructed script reproduces the stored 3-definition results within tolerance (±0.001 density, identical ordering, identical C3 pass/fail per definition)
2. The reconstructed script requires information not present in the raw evidence
3. The reconstructed script contradicts the frozen preregistration in ways that invalidate the stored verdict

## Baselines

### B1: Committed Script Reproduction
- Run committed `analyze.py` on frozen raw evidence from EXP-INTEL-34782350557
- Expected: FALSIFIED-IN-SETTING (8 tasks, all-role density, C3=false)
- This confirms the committed script is runnable and its output is stable

### B2: Stored Results Structure
- Load stored `analysis_results.json`
- Verify 3-definition structure (DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK)
- Verify 7-task deduplication (cart_1 removed)
- This confirms the stored results are structurally valid

### B3: Reconstruction Attempt
- Attempt to reconstruct the analysis pipeline from raw evidence + stored results
- Document each step and intermediate artifact
- Identify the missing script or parameterization

## Controls

### Positive Control
The committed analyze.py must reproduce its known output (FALSIFIED-IN-SETTING, 8 tasks, all-role density) when run on the frozen raw evidence. This confirms the raw evidence is intact and the committed script is functional.

### Null Control
If the reconstruction attempt produces results that match neither committed script nor stored results, this is a null outcome confirming the provenance gap is irreconcilable.

## Measurement Validity

1. Raw evidence from EXP-INTEL-34782350557 must be accessible at the frozen path
2. Committed analyze.py must be runnable on the raw evidence
3. Stored analysis_results.json must be loadable and structurally valid
4. The reconstruction attempt must be documented step-by-step with intermediate artifacts

## Decision Rule

- **PROVENANCE_RESOLVED**: Reconstruction reproduces stored results within tolerance (±0.001 density, identical ordering, identical C3 pass/fail per definition)
- **PROVENANCE_PARTIAL**: Reconstruction fails but committed script is confirmed as alternative analysis (committed script is canonical, stored results are exploratory)
- **PROVENANCE_IRRECONCILABLE**: Both reconstruction and committed script fail to match stored results (stored results cannot be verified, must be marked exploratory)

## Consequences

### If PROVENANCE_RESOLVED
- The measurement from EXP-INTEL-35124660457 can be unblocked
- The FALSIFIED verdict from EXP-INTEL-35112013458 can be re-evaluated with verified analysis
- The canonical script can be committed and used for future re-runs

### If PROVENANCE_PARTIAL
- The committed script is accepted as the canonical analysis
- The stored results are marked as exploratory
- The FALSIFIED verdict from the committed script stands until a re-run with full DOM enumeration

### If PROVENANCE_IRRECONCILABLE
- The stored results from EXP-INTEL-35124660457 must be marked exploratory
- The measurement must be re-run from scratch with a committed canonical script
- The FALSIFIED verdict from EXP-INTEL-35112013458 remains until a valid re-run

## Scope and Limitations

This experiment is pure code analysis and reconstruction. It does not:
- Collect new data
- Interact with browsers or websites
- Resolve the substrate fix needed for full DOM enumeration
- Change the claim status of C-CROSSSITE or C-LLM-INHERIT

It resolves only the provenance mismatch, which is a blocking dependency for re-evaluation of the parent experiment's measurement.
