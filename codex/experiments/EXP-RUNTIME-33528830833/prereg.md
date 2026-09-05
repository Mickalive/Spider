# EXP-RUNTIME-33528830833 Preregistration

## Status

DESIGN ONLY — not yet frozen.

## Experiment

**ID:** EXP-RUNTIME-33528830833  
**Lane:** Runtime  
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)  
**Date:** 2026-09-01

## Scientific Question

Can a stdlib-only HTTP observation substrate produce measurement-valid, discriminating observations that correctly attribute response differences to auth/session state changes rather than confounds?

## Hypothesis

An HTTP observation substrate built on Python stdlib (`urllib.request`, `http.server`, `json`, `hashlib`) captures response fingerprints (HTTP status, response headers, body SHA-256, redirect chain) that satisfy three validity conditions:

1. **Reproducibility:** Identical server state produces identical fingerprints (variance <5%).
2. **Discrimination:** Different auth/session states produce distinguishable fingerprints (similarity <95%).
3. **Validity:** Observed differences are attributable to state changes, not timing jitter or server randomness.

## State Representation

- **Server state:** Controlled by a local `http.server` with deterministic responses keyed by auth header and session token.
- **Observation vector:** `(status_code, frozenset(headers.items()), body_sha256, redirect_chain_tuple)`.
- **Fingerprint:** SHA-256 of the serialized observation vector.

## Action Representation

- HTTP GET/POST requests via `urllib.request` with controlled headers.
- No browser automation. No external network.

## Target

Fingerprint discriminability across five server states:
1. No auth header → public response
2. Valid auth token → authenticated response
3. Expired auth token → degraded/auth-error response
4. Modified (invalid) auth token → auth-error response
5. Valid session cookie → session-bound response

## Sampling Policy

- 10 repetitions per state for reproducibility measurement.
- States are tested in randomized order to prevent ordering confounds.
- Server timing jitter: none (deterministic local server).

## Unit of Analysis

One observation vector per (request, server-state) pair.

## Holdout

- Fingerprints for states 1-4 are computed during measurement.
- State 5 (session-cookie) is held out: the substrate must discriminate it without having seen it during fingerprint calibration.
- This tests generalization to unseen auth mechanisms.

## Null Models / Baselines

| ID | Description | Purpose |
|----|-------------|---------|
| B-URL-HASH | SHA-256 of URL string only | Tests whether HTTP observation adds signal beyond endpoint identity |
| B-RANDOM | Random 256-bit fingerprint | Tests whether substrate discriminates above chance level |
| B-TIMING | Fingerprint of request timestamp only | Tests whether timing confound explains any observed differences |

## Primary Metric

**Discrimination score** = 1 - (mean intra-state fingerprint Jaccard similarity / mean inter-state fingerprint Jaccard similarity).

Range: 0 (no discrimination) to 1 (perfect discrimination).  
Threshold for survival: discrimination score > 0.5.

## Expected Direction

Positive: HTTP observation adds meaningful signal beyond URL identity, random, and timing baselines.

## Uncertainty Method

- Bootstrap 1000 resamples of the 10 repetitions per state.
- Report 95% CI for discrimination score.
- Report per-state fingerprint variance.

## Adequacy Rule

Experiment is adequate if:
- All 5 server states are successfully served (verified by raw observation log).
- At least 10 repetitions per state are completed.
- No measurement errors (network failures, server crashes) exceed 10% of attempts.

## Falsification / Survival Rule

**C-MEAS-VALID survives for HTTP-level observation if and only if:**

1. Null-control false-positive rate < 5% (repeated identical requests produce different fingerprints in <5% of cases).
2. Positive-control true-positive rate > 95% (auth-state change produces different fingerprint in >95% of cases).
3. Fingerprint reproducibility variance < 5% across 10 repetitions of same state.
4. Drift signal is monotonic across valid → near-expiry → expired token states.
5. Held-out session-cookie state is correctly discriminated (not confused with any seen state).
6. All three baselines (URL-HASH, RANDOM, TIMING) have discrimination score < our substrate's discrimination score.

**If any criterion fails:** HTTP-level observation alone is insufficient for C-MEAS-VALID. The smallest next action is to install Playwright and design a DOM-level observation experiment.

## Validity Threats

1. **Local-server ecological validity:** Controlled server may not reflect live-site complexity. This is accepted for a foundational validity test; generalization to live sites is a separate experiment.
2. **Fingerprint function bias:** SHA-256 of a structured vector may over/under-weight certain fields. Mitigated by reporting per-field discrimination separately.
3. **Observation vector completeness:** We observe (status, headers, body-hash, redirects) but not timing distribution, TLS state, or server-side logs. These omissions are documented.
4. **Deterministic server removes natural variance:** Real servers have timing jitter, caching, CDN effects. Our null-control is conservative (easier to pass); a live-site experiment would be harder.

## Consequences

| Outcome | Implication |
|---------|-------------|
| **Survives** | HTTP-level observation is a valid foundation layer. Runtime can build auth/session/drift detection without browser automation for basic state discrimination. Product can ship HTTP-level freshness guards. |
| **Fails (discrimination)** | HTTP observation cannot distinguish auth states. Runtime must prioritize browser-level substrate. C-MEAS-VALID gate requires DOM/accessibility-tree observation. |
| **Fails (reproducibility)** | Even identical HTTP requests produce unstable observations. The observation vector is insufficient; richer raw capture is needed. |
| **Fails (validity)** | Differences are explained by timing or confounds, not state. The measurement design is invalid; a different substrate architecture is required. |
