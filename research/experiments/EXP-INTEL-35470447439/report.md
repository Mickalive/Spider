# EXP-INTEL-35470447439 — Execution Report

## Status: BLOCKED (Infrastructure Failure)

**This is an infrastructure failure, not a scientific negative.** The full DOM hypothesis remains **UNTESTED**.

## Summary

The frozen experiment attempted to re-collect full DOM locatable_sample data from the Magento Docker container (`am1n3e/webarena-verified-shopping:latest`) for 7 tasks, removing the `< 20` cap that truncated all locatable_sample arrays to exactly 20 elements in the parent experiment (EXP-INTEL-34782350557).

**Blocking failure:** The Docker image `am1n3e/webarena-verified-shopping:latest` is not available in the execution environment. Docker pull timed out after 120 seconds. The image may need to be pulled from a registry, built from a Dockerfile, or restored from a cache.

Without the Docker container, the Magento site at `localhost:8080` is inaccessible, preventing any data collection.

## What was executed

1. **Docker substrate check:** `docker images am1n3e/webarena-verified-shopping` returned empty (image not present locally). `docker pull` timed out after 120 seconds.

2. **Baseline context:** The frozen `analyze.py` from EXP-INTEL-35462974425 was run on existing truncated-first-20 data to provide baseline context. Results confirm:
   - **C3 gate:** 0/7 tasks have locatable_sample >20 elements (FAIL)
   - **PC1 (positive control):** All three features achieve eta2=1.0 on truncated-first-20 (PASS)
   - **NC1 (null control):** Normalized hierarchy density eta2=0.0 (PASS)
   - **Non-recipe pipeline:** Max eta2=0.999645 on truncated-first-20
   - **Ranking preservation:** All feature×definition combinations preserve listing > detail ranking

3. **No data collection:** Phase A (collection) could not proceed due to Docker unavailability. Phase B (analysis) was not attempted on full DOM data because no full DOM data exists.

## Frozen design readiness

The frozen experiment design is **ready for re-execution**:
- `analyze.py` (sha256: 79721d4668c679d4fb2695b092b848a2c1d8b3bcbdf262f81a5641c6ddc1b459) processes full-DOM data and evaluates C1-C7 decision gates
- Decision rule C3 gate will automatically pass if ≥5 tasks have locatable_sample >20 after full-DOM collection
- Baselines, definitions, and sampling protocol are frozen and unchanged
- The 7 tasks (3 listing, 3 detail, 1 cart) with full locatable_sample are the intended input

## Consequences

### Positive outcome remains possible
If the Docker substrate becomes available and full DOM data is collected:
- **If C5 AND C6 PASS (≥80% canonical agreement):** Ranking instability was a truncation artifact. MIXED program unblocked. Product lane can use recipe density.
- **If C5 FAILS (<65.95%):** Ranking instability is structural regardless of element count. Recipe density design path permanently closed for this framework.

### No evidence accumulated
- No data was collected for or against the full-DOM hypothesis
- No decision gates (C1-C7) were evaluated on full DOM
- The BLOCKED status is an infrastructure failure, not a scientific result

## Smallest next action

**Make Docker image `am1n3e/webarena-verified-shopping:latest` available in the execution environment.** Options:
1. Pull from Docker registry (if accessible)
2. Build from Dockerfile (if available in repository)
3. Restore from CI/CD cache
4. Use alternative Magento container with identical DOM structure

Once Docker is available, re-run this frozen experiment. The design is ready.
