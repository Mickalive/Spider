# EXP-PRODUCT-35551517868 preregistration

## Experiment Overview

**Experiment ID:** EXP-PRODUCT-35551517868  
**Lane:** product  
**Claim:** C-FRESHNESS (freshness guard detects stale tokens)  
**Parent Handoff:** EXP-PRODUCT-35538865048  
**Date:** 2026-09-21  

## Background

Previous experiments (6 independent mock confirmations) established orthogonality (TOST delta=0.15) at calibrated threshold 0.20 with FP=0.0. However, the calibrated threshold is at the lower bound of the tested range because the FP constraint is never binding: noise scores (0.05-0.14) are fully separated from failure minimum (0.20) by design. This threshold tautology prevents testing discrimination under overlapping distributions.

## Research Question

What is the FP-TP tradeoff curve when noise and refresh quality distributions overlap, and does the calibrated threshold remain at 0.20 under overlapping distributions?

## Hypothesis

The calibrated threshold will increase as overlap increases, and the FP constraint will become binding, revealing a discriminating operating point.

## Falsifier

- If the calibrated threshold remains at 0.20 even with overlapping distributions (FP constraint never binding), OR
- If orthogonality (TOST delta=0.15) breaks under overlap.

## Design

### Independent Variable
Overlap degree between noise and refresh quality distributions: 0%, 25%, 50%, 75%, 100%.

### Dependent Variables
- Calibrated threshold (argmax F1)
- FP rate at threshold 0.20
- TP rate at threshold 0.20
- Orthogonality (Pearson r, TOST delta=0.15)
- Behavioral-structural correlation

### Controls
- **Baseline:** Current design (0% overlap) replicates EXP-PRODUCT-35538865048.
- **Positive Control:** Known stale token detection with high overlap should yield FP > 0 at threshold 0.20.
- **Null Control:** No overlap replicates baseline FP=0.0.

### Sample Size
- 480 samples per overlap condition (total 2400).
- This matches previous experiments for TOST comparability.

### Measurement Validity
- Noise and refresh distributions must be designed with controlled overlap degrees.
- Overlap is achieved by shifting the noise distribution upward and/or the refresh distribution downward.
- The overlap degree is defined as the proportion of the noise distribution that overlaps with the failure region.

### Decision Rule
- If calibrated threshold increases with overlap and FP > 0 at threshold 0.20 for overlap >=25%, then the claim about discriminating operating point is supported.
- If threshold remains 0.20 and FP remains 0.0 for all overlaps, the claim is falsified.

## Consequences

- **Positive:** If discrimination exists under overlap, we can calibrate a production threshold and move toward PRODUCT_CORE.
- **Negative:** If no discrimination under overlap, the freshness guard cannot distinguish noise from real refresh failures in production, blocking PRODUCT_CORE.

## Estimated Cost

Medium: redesigning noise/refresh injection with controlled overlap, running 5 conditions x 480 samples.

## Expected Information Gain

High: resolves the open question about discriminating operating point and threshold tautology.

## Parent Handoff Carry-Forward

### Established
- C-FRESHNESS freshness guard achieves TP>=0.85 and FP<=0.10 at calibrated threshold 0.20 with orthogonality TOST PASS at delta=0.15 (n=480, r=-0.0065, CI upper 0.0831) on localhost stochastic mock with continuous severity gradient.
- Continuous severity injection verified: 451 unique behavioral scores, not bimodal.
- error_format_variation fixed and verified effective (4/4 noise types).
- Orthogonality confirmed across 6 independent mock experiments at n=480.

### Rejected
- Hypothesis that calibrated threshold would be in [0.40,0.60]: FALSIFIED — calibrated threshold at 0.20.
- Hypothesis that bimodal discrete scores are necessary for detection: FALSIFIED — continuous severity gradient produces same orthogonality.

### Unknown
- Whether calibrated threshold 0.20 generalizes to production refresh quality distributions where noise and low-quality refresh may overlap more.
- Whether orthogonality survives on production-like substrate with real OAuth/OIDC, CDN, network RTT, DB-backed sessions.

### Do Not Assume
- Do not assume C-FRESHNESS is VALIDATED or PRODUCT_CORE — it remains EXPERIMENTAL.
- Do not assume calibrated threshold 0.20 is a discriminating operating point — FP constraint is never binding.
- Do not assume that because 6 mock experiments confirm orthogonality, production endpoints will behave identically.

## Dependencies

- Runtime lane must build production-like HTTP observation substrate before product lane attempts integration.
- Any non-mock re-measurement must use TOST delta=0.15 with n>=480 for comparability.
- Token_refresh behavioral_score must use overlapping noise/refresh distributions where FP > 0 at calibrated threshold.

## Evidence References

- research/experiments/EXP-PRODUCT-35538865048/result.json
- research/experiments/EXP-PRODUCT-35538865048/audit.json
- research/experiments/EXP-PRODUCT-35538865048/spec.json
- research/experiments/EXP-PRODUCT-35538865048/prereg.md
- codex/claim_state.json C-FRESHNESS status EXPERIMENTAL across 40+ prior experiments

## Status

DESIGN NOT YET FROZEN.