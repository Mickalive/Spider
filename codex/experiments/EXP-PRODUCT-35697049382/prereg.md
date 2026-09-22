# EXP-PRODUCT-35697049382 — Preregistration

**Experiment:** C-FRESHNESS Kernel Integration  
**Lane:** product  
**Claim:** C-FRESHNESS  
**Created:** 2026-09-22  
**Director Mandate:** PIVOT from C-FRESHNESS overlap discrimination (BLOCKED) to C-FRESHNESS kernel integration  

---

## 1. Question

Can the validated behavioral+structural parallel-channel freshness-detection architecture be wired into the SPIDER kernel (src/spider/kernel.py) as a freshness-check subprocess that runs without new LLM calls, using HTTP requests to the mechanism's target endpoint to detect auth/session/API drift?

## 2. Background and Inherited State

### 2.1 What is established (from prior experiments)

The behavioral+structural parallel-channel architecture for C-FRESHNESS has been validated across 6+ independent localhost mock experiments:

- **Orthogonality confirmed at delta=0.15:** pooled r = 0.002-0.046, CI upper 0.06-0.135, all TOST PASS, n=480 each
  - EXP-GRAPH-35353011131: r=0.046, CI upper 0.135, audit PASS
  - EXP-GRAPH-35389145821: r=0.002, CI upper 0.092, audit PASS (HTTP caching exercised)
  - EXP-PRODUCT-35445596342: r=-0.026, CI upper 0.064, audit PASS (product-lane replication)
  - EXP-GRAPH-35530590140: r=0.041, CI upper 0.116, audit PASS (production-like LOCAL)
  - Additional replications in EXP-PRODUCT-35538865048, EXP-GRAPH-35611618323

- **Behavioral drift detection validated:** TP=1.0 on expired tokens, session invalidation, permission boundary changes. Threshold 0.20-0.25 achieves TP=1.0, FP=0.0 on 240 noise-only samples.

- **Structural signal validated:** discrimination 0.8333 (HTTP fingerprint substrate, headers-only). Structural noise tolerance FP=0.0 on 4 noise types.

- **Six structural signal families falsified** for C-FRESHNESS frozen gate: Jaccard, TF-IDF, response-time KS, linear ensemble, field-usage, schema comparison. Behavioral signals remain the validated detection dimension.

### 2.2 What is NOT established

- Whether the architecture can be wired into kernel.py without losing detection/orthogonality properties
- Whether the kernel's resolve() path can host a freshness subprocess without regression
- Whether the subprocess adds acceptable latency for production use
- Whether the architecture generalizes beyond localhost mock to production OAuth/OIDC/CDN

### 2.3 Director mandate (binding)

The Global Research Director issued a PIVOT mandate:
- **Action:** PIVOT from C-FRESHNESS overlap discrimination (BLOCKED after EXP-PRODUCT-35651924708)
- **Target claim:** C-FRESHNESS
- **Strategic question:** Can the validated architecture be wired into the kernel as a freshness-check subprocess?
- **Rationale:** "Product is BLOCKED on LLM API keys. The highest-leverage work that does NOT require LLM calls is integrating the validated C-FRESHNESS parallel-channel architecture into the SPIDER kernel. This advances C-FRESHNESS toward PRODUCT_CORE using existing validated evidence."
- **Parent handoff disposition:** SUPERSEDE — the parent's C-FRESHNESS overlap discrimination thread is superseded; this is a new direction.

## 3. Hypothesis

A `freshness_check()` subprocess added to SpiderKernel that probes the mechanism's endpoint via HTTP and computes a behavioral_score and a structural_score will:

1. Detect expired/invalid tokens with TP >= 0.85
2. Tolerate structural noise with FP <= 0.10
3. Maintain behavioral-structural orthogonality at delta=0.15
4. Correctly gate resolution (return STALE for stale mechanisms)
5. Add < 200ms latency overhead per resolution call
6. Not regress existing kernel tests

## 4. Design

### 4.1 Freshness gate architecture

```
resolve(intent, context, params) → Resolution:
  1. [existing] candidate selection (intent match, preconditions, guards, slots)
  2. [NEW] for each candidate mechanism:
     a. freshness_check(mechanism, context) → FreshnessResult
     b. if behavioral_score > THRESHOLD_BEHAVIORAL (0.25):
        → return Resolution(STALE, mechanism_id, "freshness gate: auth/session drift detected")
     c. if structural_score > THRESHOLD_STRUCTURAL (0.15):
        → log warning but continue (structural drift is informational)
  3. [existing] confidence threshold and resolution
```

### 4.2 Freshness check subprocess

```python
def freshness_check(self, mechanism: Mechanism, context: dict) -> FreshnessResult:
    """Probe mechanism endpoint and compute freshness scores.
    
    Uses HTTP requests to extract:
    - behavioral_score: token validation failure, session state change, auth boundary shift
    - structural_score: ETag/Cache-Control header cardinality, request_id entropy
    
    Returns FreshnessResult(behavioral_score, structural_score, is_stale, latency_ms)
    """
```

### 4.3 Signal extraction (matching validated protocol)

- **Behavioral signal:** Composite of (a) HTTP status code anomaly (401/403 for valid credentials = drift), (b) session-state flag change, (c) permission-level shift. Score: 0.0 (fresh) to 1.0 (stale). Threshold: 0.25.
- **Structural signal:** Cardinality of (ETag, Cache-Control, X-Request-Id) header set + request_id entropy. Score: 0 (no variation) to N (unique values). Threshold: informational only (no gating).
- **Orthogonality:** Behavioral and structural signals must be extracted from independent HTTP response attributes. No shared variables between signal domains (spec measurement_validity #7-8).

### 4.4 Testbed

Reuse the existing validated mock infrastructure:
- Flask 3.1.3 + PyJWT 2.14.0 HS256 + SQLite WAL-mode
- TTL cache 0.5s + jitter 1-100ms
- 3 endpoints: /api/user/profile, /api/data/list, /api/session/status
- Token management: single HS256 shared secret (TESTBED_SECRET)
- Drift types: expired token, session invalidation, permission boundary
- Noise types: optional_field_addition, description_change, response_time_jitter, field_type_normalization

## 5. Conditions

### 5.1 Phase A — Drift detection (positive control)

3 drift types x 3 endpoints x 20 samples = 180 paired samples.

Each sample:
1. Store mechanism in kernel registry with auth_scope matching mock JWT
2. Call kernel.resolve() with the mechanism's intent and context
3. Record FreshnessResult behavioral_score, structural_score, is_stale, latency_ms
4. Record whether resolve() returned STALE or EXECUTABLE

### 5.2 Phase B — Co-occurring conditions (orthogonality)

2 drift types x 4 noise types x 3 endpoints x 20 samples = 480 paired samples.

Each sample:
1. Activate drift (expired token or permission boundary) AND noise simultaneously
2. Call kernel.resolve()
3. Record behavioral_score, structural_score, latency_ms
4. Compute endpoint-stratified pooled Pearson r on non-304 samples

### 5.3 Phase C — Noise-only (null control)

4 noise types x 3 endpoints x 20 samples = 240 samples.

No drift active. All behavioral_score values must be < 0.25 (threshold). FP = count(behavioral_score >= 0.25) / 240.

### 5.4 Phase D — Regression

Run tests/test_kernel.py unmodified. All 3 tests must pass.

### 5.5 Phase E — Latency

100 resolve() calls with freshness gate active. Record median and p95 latency overhead.

## 6. Metrics

| Metric | ID | Definition | Gate |
|--------|-----|-----------|------|
| Drift TP | C1_TP | mean TP across 3 endpoints on Phase A | >= 0.85 |
| Noise FP | C2_FP | FP rate on Phase C (240 samples) | <= 0.10 |
| Variance | C3_VAR | endpoints with std > 0.05 in Phase B | >= 2/3 |
| Orthogonality | C4_ORTHO | CI upper of stratified pooled r | < 0.15 |
| TOST | C4_TOST | TOST p_upper at delta=0.15 | < 0.05 |
| Regression | C5_REG | tests/test_kernel.py pass rate | 3/3 |
| Latency | C6_LAT | median ms per freshness_check() | < 200ms |

## 7. Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:
- C1: TP >= 0.85 across all 3 endpoints (Phase A)
- C2: FP <= 0.10 on 240 noise-only samples (Phase C)
- C3: >= 2/3 endpoints have behavioral_std > 0.05 AND >= 2/3 have structural_std > 0.05 (Phase B)
- C4: CI upper < 0.15 AND TOST p_upper < 0.05 at delta=0.15 (Phase B, non-304 only)
- C5: 3/3 existing kernel tests pass (Phase D)
- C6: median latency < 200ms (Phase E)

**FALSIFIED** if ANY condition fails.

**MEASUREMENT_INVALID** if mock endpoint unreachable or testbed construction fails.

## 8. Validity Threats

1. **Mock-only ceiling:** All measurements on localhost Flask mock. No inference to production OAuth/OIDC, CDN, network RTT, or DB-backed sessions. The parent's orthogonality confirmation is also mock-only; this experiment tests kernel wiring, not generalization.

2. **Threshold tautology:** The calibrated threshold 0.25 may be at the boundary of behavioral score modes (bimodal 0.35/0.65 vs noise 0.05). This is inherited from the validated architecture and limits discriminating power under overlapping distributions.

3. **Latency measurement environment:** Localhost measurements may not reflect production network RTT. The < 200ms gate is a ceiling check, not a performance guarantee.

4. **Regression coverage:** tests/test_kernel.py has only 3 tests. A broader test suite would provide stronger regression guarantees. The 3 tests cover the core resolve path (UNKNOWN default, parameterized binding, invalidation).

5. **Freshness gate scope:** The gate only checks freshness at resolve-time. Staleness that develops after resolution (mechanism becomes stale between resolve and execute) is not detected. This is a known limitation of the parallel-channel architecture.

## 9. Scope and Claim Ceiling

This experiment tests kernel wiring of the validated C-FRESHNESS architecture. If SURVIVES:

- C-FRESHNESS advances from EXPERIMENTAL with bounded kernel-integration confirmation
- Parallel-channel architecture justified for kernel integration at localhost mock ceiling
- Does NOT reach VALIDATED or PRODUCT_CORE (requires distributed/CDN validation)
- Does NOT generalize beyond localhost mock

If FALSIFIED:

- C-FRESHNESS remains EXPERIMENTAL
- The specific integration failure mode identifies the blocker
- Product must redesign the freshness gate or accept standalone subprocess

## 10. Parent Handoff Disposition

The parent handoff (EXP-PRODUCT-35651924708, C-LLM-INHERIT) is carried forward as continuity evidence but is NOT the research direction for this experiment. The Director mandate PIVOTs from C-LLM-INHERIT (BLOCKED on LLM API keys) to C-FRESHNESS kernel integration. The parent's carry_forward categories are preserved:

- **Established:** Frozen design for C-LLM-INHERIT is validated and executable (not relevant to this experiment)
- **Rejected:** None relevant to C-FRESHNESS kernel integration
- **Unknown:** Whether C-FRESHNESS kernel integration preserves the validated architecture properties (this experiment answers this)
- **Do not assume:** BLOCKED status on C-LLM-INHERIT does not imply C-FRESHNESS is blocked; they are orthogonal claims with orthogonal infrastructure dependencies
