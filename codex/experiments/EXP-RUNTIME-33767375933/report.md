# EXP-RUNTIME-33767375933 — Execution Report

## Experiment Summary

- **Experiment ID**: EXP-RUNTIME-33767375933
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Status**: COMPLETE
- **Outcome**: SUPPORTS

## Scientific Question

After applying deterministic fingerprint serialization, Date header exclusion, strong single-field baselines, and calibrated timing jitter, does the HTTP observation substrate maintain discrimination on the fixed toy server — and does it discriminate on a non-tautological external endpoint where response variation is not hand-programmed?

## Design

Two-phase design:

**Phase A (Positive Control):** Toy server with 5 auth states × 10 reps = 50 requests, 0-200ms random jitter between requests. Tests mechanism integrity after all mandatory fixes.

**Phase B (Ecological Validity):** httpbin.org/status/{200, 401, 403} — 3 states × 10 reps = 30 requests, 0-200ms random jitter. Tests discrimination on a real external server where response variation is not hand-programmed.

## Fixes Applied (from parent audit EXP-RUNTIME-33528830833)

1. **Deterministic fingerprint**: `tuple(sorted(...))` replaces `frozenset(...)` — eliminates PYTHONHASHSEED non-determinism
2. **Date/Server header exclusion**: Volatile headers excluded from fingerprint vector — prevents spurious variance under multi-second execution
3. **Strong baselines**: B-STATUS-ONLY and B-BODY-ONLY added as competitive baselines (replacing straw-man B-URL-HASH, B-RANDOM, B-TIMING)
4. **Calibrated jitter**: 0-200ms random delays between requests — tests fingerprint stability under timing variation
5. **External endpoint**: httpbin.org — non-tautological server where response bodies are not hand-programmed

## Results

### Phase A: Toy Server

| Metric | Value | Threshold | Pass |
|--------|-------|-----------|------|
| Discrimination score | 1.000000 | > 0.5 | ✓ |
| Bootstrap 95% CI | [1.0, 1.0] | LB > 0.3 | ✓ |
| Null FP rate | 0.0% | < 5% | ✓ |
| Positive TP rate | 100.0% | > 95% | ✓ |
| Drift discriminability | All pairs < 0.5 | All < 0.5 | ✓ |
| Baseline superiority | Substrate ≥ best (1.0) | ≥ best | ✓ |
| Held-out novelty | 10/10 novel | Novel | ✓ |

**Phase A baselines:**
- B-URL-HASH: 0.0 (straw-man, URL constant)
- B-RANDOM: 0.0 (straw-man, chance level)
- B-TIMING: 0.0 (straw-man, timing confound)
- B-STATUS-ONLY: 0.7 (strong, single-field)
- B-BODY-ONLY: 1.0 (strong, single-field — body fully discriminates)

### Phase B: External Endpoint (httpbin.org)

| Metric | Value | Threshold | Pass |
|--------|-------|-----------|------|
| Discrimination score | 1.000000 | > 0.5 | ✓ |
| Bootstrap 95% CI | [1.0, 1.0] | LB > 0.3 | ✓ |
| Error rate | 0.0% | < 20% | ✓ |

**Phase B baselines:**
- B-URL-HASH: 1.0 (URLs differ across states — httpbin.org/status/200 vs /401 vs /403)
- B-RANDOM: 0.0 (straw-man)
- B-TIMING: 0.0 (straw-man)
- B-STATUS-ONLY: 1.0 (status codes differ: 200, 401, 403)
- B-BODY-ONLY: 0.0 (bodies are minimal/identical across status codes)

### Interpretation

**Phase A confirms mechanism integrity.** The fixed substrate (deterministic SHA-256 of sorted-tuple vector, excluding Date/Server headers) achieves perfect discrimination (1.0) on the jittered toy server. All controls pass: null FP rate 0.0%, positive TP rate 100%, drift pairs discriminable, held-out session_cookie novel. The fixes did not break the mechanism.

**Phase B confirms ecological validity on httpbin.org.** The substrate achieves perfect discrimination (1.0) on a real external server. The 0% error rate indicates reliable request execution. Critically, httpbin.org/status returns minimal bodies — discrimination comes primarily from status codes. The full substrate (status + headers + body + redirects) equals but does not exceed B-STATUS-ONLY (1.0 = 1.0) on this endpoint.

**Key observation from Phase B:** On httpbin.org, B-BODY-ONLY = 0.0 (bodies are identical across status codes), while B-STATUS-ONLY = 1.0 (status codes differ). The full substrate adds no discrimination over status-only observation on this endpoint. This is informative: on servers where response bodies don't vary with auth state, status code alone suffices for discrimination.

## Decision Rule Evaluation

Per prereg Section 13.1, C-MEAS-VALID SURVIVES if ALL of:
1. Phase A discrimination > 0.5 → **1.0 ✓**
2. Phase A null FP rate < 5% → **0.0% ✓**
3. Phase A positive TP rate > 95% → **100% ✓**
4. Phase A B-STATUS-ONLY discrimination < substrate → **0.7 < 1.0 ✓**
5. Phase A B-BODY-ONLY discrimination ≤ substrate → **1.0 ≤ 1.0 ✓** (equality acceptable per prereg Section 8)
6. Phase B discrimination > 0.5 → **1.0 ✓**

**Verdict: C-MEAS-VALID SURVIVES.**

## Claim Ceiling

C-MEAS-VALID survives for HTTP-level observation using deterministic SHA-256 fingerprinting of (status, sorted headers excluding Date/Server, body hash, redirect chain) on:
- Local deterministic toy server with 5 auth states and 0-200ms jitter
- httpbin.org/status with 3 HTTP status codes (200, 401, 403)

**Does NOT yet cover:**
- Production servers with auth middleware, caching, CDN
- Servers where response bodies vary independently of status codes
- Continuous session drift detection
- Cross-origin or CORS-restricted endpoints

## Validity Threats

1. **Phase A toy server is still hand-programmed** — discrimination guaranteed by construction. Phase B is the ecological validity test.
2. **httpbin.org is a testing service** — not production auth middleware. Success here is necessary but not sufficient for production.
3. **Fingerprint uses `repr(vector)`** — Python-version-dependent serialization. Reproduction requires same Python major version.
4. **httpbin.org bodies are minimal** — on servers where bodies vary with auth state, B-BODY-ONLY may achieve higher discrimination, changing the baseline superiority calculation.
5. **No timing jitter in server processing** — jitter was injected between requests, not within server response generation.

## Unresolved Questions

1. How does fingerprinting perform against production servers with caching, CDN, non-deterministic responses?
2. Does body-only or header-only observation suffice on real servers, making full vector unnecessary?
3. Can substrate detect continuous session drift as a continuous signal?
4. What is the discrimination score with production auth middleware (OAuth, JWT validation)?
