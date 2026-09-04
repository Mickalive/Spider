# EXP-RUNTIME-33767375933 — Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-33767375933
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-RUNTIME-33528830833 (NARROW_SUCCESS, audit REVISE, 6 required fixes)
- **Date**: 2026-09-03

## 2. Scientific Question

After applying deterministic fingerprint serialization, Date header exclusion, strong single-field baselines, and calibrated timing jitter, does the HTTP observation substrate maintain discrimination on the fixed toy server — and does it discriminate on a non-tautological external endpoint where response variation is not hand-programmed?

## 3. Background and Motivation

### What the parent experiment (EXP-RUNTIME-33528830833) established
- Stdlib HTTP observation substrate CAN produce deterministic fingerprints within a single Python process on a local deterministic http.server
- 5/5 states discriminated, 0% intra-state variance, all controls pass
- Fingerprint mechanism (SHA-256 of status+headers+body_hash+redirect_chain) CAN achieve perfect discrimination when response bodies/headers vary across states
- Body hash and custom headers each achieve per-field discrimination of 1.0 on the toy server

### What the parent audit found (6 required fixes)
1. **Fingerprint instability**: `repr(frozenset(...))` is hash-randomized (PYTHONHASHSEED). Audit recompute produced 50/50 mismatches.
2. **Date header leakage**: Date included in headers frozenset but constant only because all requests executed within one second. Would inject spurious variance under multi-second execution.
3. **Straw-man baselines**: B-URL-HASH, B-RANDOM, B-TIMING all score 0.0 by construction. Producer's own per-field results show status-only=0.833, body_hash=1.0, header_set=1.0 — full vector adds no discrimination over components.
4. **Held-out drift vacuous**: Novelty check is trivial because substrate is deterministic SHA-256 with no calibration. Any new state with distinct body passes.
5. **Timing confound untested**: Elapsed times varied 0.27ms-71ms but never entered fingerprint. No measurement of timing contribution.
6. **Ecological validity**: Server is tautological (hand-programmed responses). No evidence for live-site performance.

### What this experiment tests
Three mandatory fixes from the parent audit, plus ecological validity:
- Fix: Deterministic fingerprint serialization (sorted tuple, exclude Date/Server headers)
- Fix: Strong single-field baselines (B-STATUS-ONLY, B-BODY-ONLY)
- Fix: Calibrated jitter injection (0-200ms random delays)
- Test: External non-tautological endpoint (httpbin.org)

## 4. Hypotheses

### H1: Mechanism Integrity (Phase A — Toy Server)
After applying fixes, the substrate maintains discrimination score > 0.5 on the jittered toy server.

### H2: Ecological Validity (Phase B — External Endpoint)
The fixed substrate achieves discrimination score > 0.5 on httpbin.org/status endpoints.

### H3: Jitter Tolerance
Null control FP rate < 5% on jittered toy server (jitter does not cause false fingerprint variation).

### H4: Substrate Value-Added
B-STATUS-ONLY and B-BODY-ONLY achieve lower discrimination than the full substrate on the toy server (substrate adds information beyond single fields).

## 5. Design Overview

Two-phase design within one experiment:

**Phase A (Positive Control):** Fixed toy server with jitter
- Same 5 states as parent (no_auth, valid_token, expired_token, invalid_token, session_cookie)
- 10 reps per state = 50 requests
- 0-200ms random jitter between requests
- Validates mechanism integrity after fixes

**Phase B (Ecological Validity):** External endpoint
- httpbin.org/status/{200, 401, 403}
- 10 reps per state = 30 requests
- 0-200ms random jitter between requests
- Tests discrimination on real server

Phase A must pass before Phase B results are interpretable.

## 6. Fingerprint Function (Fixed)

```python
def fingerprint(observation: dict) -> str:
    """Deterministic fingerprint: SHA-256 of sorted-tuple vector, excluding Date/Server."""
    body_hash = hashlib.sha256(observation["body"]).hexdigest()
    redirect_chain = observation.get("redirect_url") or ""
    # Exclude Date and Server headers (volatile, non-informative)
    excluded = {"date", "server"}
    headers_filtered = {k: v for k, v in observation["headers"].items()
                        if k.lower() not in excluded}
    vector = (
        observation["status"],
        tuple(sorted(headers_filtered.items())),
        body_hash,
        redirect_chain,
    )
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()
```

Key changes from parent:
- `tuple(sorted(...))` instead of `frozenset(...)` — deterministic across processes
- Date and Server headers explicitly excluded — prevents spurious variance
- Same SHA-256 base — preserves 256-bit fingerprint structure

## 7. Server States

### Phase A: Toy Server (5 states)

| State | Auth | Status | Body | Extra Headers |
|-------|------|--------|------|---------------|
| no_auth | none | 200 | public page | X-Auth-Level: public |
| valid_token | Bearer tok_valid_abc123 | 200 | private dashboard | X-Auth-Level: full, X-User: alice |
| expired_token | Bearer tok_expired_xyz789 | 401 | token expired error | X-Error: token_expired |
| invalid_token | Bearer tok_invalid_wrong | 403 | invalid token error | X-Error: invalid_token |
| session_cookie | Cookie: sess_cookie_def456 | 200 | session-bound data | X-Auth-Level: session, X-User: bob |

### Phase B: External Endpoint (3 states)

| State | URL | Expected Status |
|-------|-----|-----------------|
| ext_200 | httpbin.org/status/200 | 200 |
| ext_401 | httpbin.org/status/401 | 401 |
| ext_403 | httpbin.org/status/403 | 403 |

Note: httpbin.org/status returns minimal body for all codes. Discrimination primarily from status code, potentially from response headers.

## 8. Baselines

| ID | Description | Expected Discrimination | Purpose |
|----|-------------|------------------------|---------|
| B-URL-HASH | SHA-256 of URL string | 0.0 (URL constant) | Straw-man: identity only |
| B-RANDOM | Random 256-bit fingerprints | ~0.0 | Straw-man: chance level |
| B-TIMING | SHA-256 of timestamp string | ~0.0 | Straw-man: timing confound |
| B-STATUS-ONLY | SHA-256 of status code string | >0, < substrate (toy) | Strong: single-field upper bound |
| B-BODY-ONLY | SHA-256 of response body bytes | 1.0 (toy), variable (external) | Strong: single-field upper bound |

Strong baseline survival criterion: substrate must exceed best strong baseline with margin. On toy server, B-BODY-ONLY is expected to be 1.0 (body fully discriminates), so substrate may not exceed it — this is acceptable if substrate equals it. On httpbin.org, B-BODY-ONLY is expected to be low (bodies similar across status codes), so substrate should exceed it.

## 9. Controls

### 9.1 Positive Control (Phase A)
- Flip auth header from absent to present on toy server
- Expect fingerprint change in >95% of cases
- Verifies: mechanism detects real auth state changes

### 9.2 Null Control (Phase A)
- Repeat identical request 10 times to same toy server state with jitter
- Expect FP rate < 5%
- Verifies: jitter does not cause false fingerprint variation

### 9.3 Drift Control (Phase A)
- Measure Jaccard distance between valid_token, expired_token, invalid_token
- Require monotonic distance increase: valid→expired < valid→invalid < expired→invalid
- Note: parent audit found Jaccard values demonstrate discriminability, not monotonicity. This control tests the fixed definition.

### 9.4 Held-Out Control (Phase A)
- Calibration set: states 1-4 (no_auth, valid_token, expired_token, invalid_token)
- Test: state 5 (session_cookie)
- Require: session_cookie fingerprint not in calibration set (exact equality)
- Note: parent audit found this vacuous for deterministic substrates. Still included as regression check.

### 9.5 Baseline Superiority (Phase A)
- Substrate discrimination > max(B-URL-HASH, B-RANDOM, B-TIMING)
- Substrate discrimination >= B-STATUS-ONLY (must not be worse than single-field)
- Substrate discrimination >= B-BODY-ONLY on toy server (must not be worse than single-field)

## 10. Metrics

### Primary Metric
- **discrimination_score** = intra_match_rate - inter_match_rate (exact fingerprint equality)
- Range: [-1, 1]. Perfect discrimination = 1. No discrimination = 0.
- Survival threshold: > 0.5

### Secondary Metrics
- intra_match_rate: fraction of same-state fingerprint pairs that are identical
- inter_match_rate: fraction of different-state fingerprint pairs that are identical
- mean_intra_jaccard: mean bitwise Jaccard similarity within states
- mean_inter_jaccard: mean bitwise Jaccard similarity between states
- bootstrap_95ci: 95% confidence interval for discrimination score (1000 bootstrap resamples)
- per_field_discrimination: discrimination for each individual observation field
- baseline_discrimination: discrimination for each baseline

## 11. Statistical Tests

### 11.1 Primary Test
- Discrimination score > 0.5 on each phase
- Bootstrap 95% CI lower bound > 0.3 (conservative survival threshold)

### 11.2 Control Tests
- Null control: one-sided binomial test, H0: FP rate >= 0.05, H1: FP rate < 0.05
- Positive control: one-sided binomial test, H0: TP rate <= 0.95, H1: TP rate > 0.95
- Baseline superiority: paired comparison, substrate > best strong baseline

### 11.3 Effect Size
- Cohen's d for substrate vs best baseline (if applicable)
- Jaccard distance effect size for drift pairs

## 12. Validity Threats

### 12.1 External Endpoint Simplicity
httpbin.org/status returns minimal body variation. Discrimination may primarily come from status codes. **Mitigation:** This is the point — we're testing whether status-only observation suffices on real servers. If it does, that's informative. If it doesn't, that's also informative.

### 12.2 Rate Limiting
httpbin.org may rate-limit rapid requests. **Mitigation:** 0-200ms jitter between requests, 30 total requests, execution time < 10 seconds.

### 12.3 Network Variability
External requests may fail due to network issues. **Mitigation:** 10 reps per state provides redundancy. If >20% of requests fail, phase is MEASUREMENT_INVALID.

### 12.4 Synthetic-to-Real Gap
httpbin.org is a testing service, not a production website with auth middleware, caching, CDN. **Mitigation:** This is the ecological validity gate. Success here is necessary but not sufficient for production deployment. Real-site testing is the next experiment tier.

### 12.5 Fingerprint repr() Dependency
`repr(vector)` is still Python-version-dependent. **Mitigation:** Documented. Reproduction requires same Python major version. Future fix: use JSON serialization instead of repr.

## 13. Decision Rules

### 13.1 C-MEAS-VALID SURVIVES
If ALL of:
1. Phase A discrimination > 0.5
2. Phase A null FP rate < 5%
3. Phase A positive TP rate > 95%
4. Phase A B-STATUS-ONLY discrimination < substrate discrimination
5. Phase A B-BODY-ONLY discrimination <= substrate discrimination (on toy server)
6. Phase B discrimination > 0.5

### 13.2 C-MEAS-VALID FALSIFIED
If Phase A passes but Phase B discrimination <= 0.5.

### 13.3 MEASUREMENT_INVALID
If Phase A fails (discrimination <= 0.5 or FP rate >= 5%). Phase B results are not interpretable.

### 13.4 NARROW_SURVIVAL
If Phase A passes but Phase B discrimination is between 0.3 and 0.5 (marginal). Claim ceiling limited to toy server.

## 14. Expected Outcomes

### 14.1 Best Case (SURVIVES)
- Phase A: discrimination = 1.0 (fixes preserve mechanism)
- Phase B: discrimination > 0.5 (substrate works on real server)
- Consequence: C-MEAS-VALID advances, Runtime measurement pipeline validated, Product can build drift detection

### 14.2 Narrow Survival (NARROW_SURVIVAL)
- Phase A: discrimination = 1.0
- Phase B: 0.3 < discrimination <= 0.5
- Consequence: C-MEAS-VALID limited to controlled environments, real-server testing needs stronger substrate

### 14.3 Ecological Failure (FALSIFIED)
- Phase A: discrimination = 1.0
- Phase B: discrimination <= 0.5
- Consequence: C-MEAS-VALID does not survive for general HTTP observation, Runtime must use alternative substrates

### 14.4 Mechanism Failure (MEASUREMENT_INVALID)
- Phase A: discrimination <= 0.5
- Consequence: Fixes broke the mechanism, need to re-examine code changes

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 16. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
