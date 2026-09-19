# EXP-PRODUCT-35434772331 Preregistration

## Experiment Identity

- **experiment_id**: EXP-PRODUCT-35434772331
- **lane**: product
- **claim_ids**: C-PRODUCT-ECON, C-FRESHNESS
- **created_at**: 2026-09-19T09:28:26.218475+00:00
- **parent_handoff**: EXP-PRODUCT-35409929216 (sha256: f3ce339a1c8fbff4309caa9b968844292e232ac49aefc367f600add506b59d26)

## Parent Handoff Carry-Forward

### Established (from parent)
1. The 5.42% token savings margin (1067 tokens) is analytically robust to completion token estimation error under frozen assumptions: break-even differential bias threshold 33.3 tokens/task, bootstrap survival 96.1% under ±50% Normal(CV=0.5) variation — from EXP-PRODUCT-35409929216
2. Selection prompt savings (112 tokens) are fixed and independent of completion estimates — measured via tiktoken from EXP-PRODUCT-35330741529
3. Completion savings (955 tokens) are the dominant component of the 1067-token margin but represent 5.05% of completion cost
4. Analytical deduplication economics on synthetic 32-task corpus: parameterized 25 vs literal 32 mechanisms (21.9% reduction), net workflow savings 1067 tokens (5.42%) — from EXP-PRODUCT-35330741529
5. Browser+verification cost is a constant offset across conditions by construction, total 1499 token-equivalents — from EXP-PRODUCT-35389141536
6. COLD baseline at 77 tokens/task (analytical) is 3.7-7.5x cheaper than PARAMETERIZED even when doubled to 5000 tokens

### Rejected (from parent)
1. Hypothesis that the 5.42% margin is fragile to completion token estimation error: FALSIFIED
2. Hypothesis H1 (break-even < 2 tokens/task): FALSIFIED (observed 33.3)
3. Hypothesis H3 (bootstrap survival < 30%): FALSIFIED (observed 96.1%)
4. Token savings as a general claim for short-value URL patterns: FALSIFIED (EXP-PRODUCT-35209109455)
5. Token savings as a general claim for long-value URL patterns: FALSIFIED (EXP-PRODUCT-35262262156)
6. Hypothesis that browser/verification costs differentially offset token savings: FALSIFIED by construction

### Unknown (from parent)
1. Whether real LLM completion outputs average 2/15/20 tokens or heavier-tailed — unmeasured, analytical prior only across 4 consecutive experiments
2. Whether COLD baseline achieves >=90% success rate with real LLM API calls — 0/32 measured across all product experiments
3. Whether 5.42% token savings is economically meaningful in real SPIDER workflows — requires real LLM measurement
4. Whether differential completion bias could approach 29.8 tokens/task in practice — no model for per-condition length correlation
5. Whether production endpoint latency/auth/rate-limiting changes absolute cost magnitude
6. Whether larger registries (100+ mechanisms) would increase selection saving dominance

### Do Not Assume (from parent)
1. Do not assume 5.42% workflow savings generalizes to real SPIDER corpus
2. Do not assume C1 100% success — assumed analytically, not measured with real LLM calls
3. Do not assume completion tokens are accurate — hard-coded estimates (2/15/20) not measured from model outputs
4. Do not assume C-PRODUCT-ECON is measured — remains HYPOTHESIS with zero real LLM calls
5. Do not assume C-PARAM-INHERIT is PRODUCT_CORE — remains EXPERIMENTAL
6. Do not assume COLD baseline is or is not viable — 77 tokens/task is analytical prompt-only counting
7. Do not assume the break-even 33.3 tokens/task applies to systematic (uniform) bias
8. Do not assume the bootstrap 96.1% survival tests the full 1067-token margin
9. Do not assume that four consecutive experiments without real LLM measurement means API access is permanently unavailable
10. Do not assume n=32 tasks establishes statistical significance — deterministic synthetic analysis, not a sample

## Scientific Question

Should the product lane close C-PRODUCT-ECON (token-based deduplication economics) and redirect to C-FRESHNESS product integration — specifically, can the validated behavioral+structural parallel-channel architecture detect auth/session/API drift in real SPIDER kernel workflows using the existing HTTP fingerprint substrate, without requiring new LLM calls or browser automation?

## Hypothesis

C-PRODUCT-ECON is not viable at current scale (5.42% thin margin, COLD 7.5x cheaper, 4 consecutive experiments with zero real LLM calls, analytical line exhausted). The product lane should close token-based economics and redirect to C-FRESHNESS: the validated behavioral+structural parallel-channel architecture (orthogonality confirmed at delta=0.15 under stochastic mock, EXP-GRAPH-35353011131) can detect auth/session/API drift in real SPIDER kernel workflows by integrating the HTTP fingerprint substrate (C-MEAS-VALID, EXP-RUNTIME-33902315583) as the structural signal and JWT/session validation as the behavioral signal, achieving TP>=0.85 and FP<=0.15 on drift-vs-noise discrimination.

## Falsifier

FALSIFIED if:
- (F1) the HTTP fingerprint substrate cannot discriminate auth-state changes on real SPIDER kernel endpoints (discrimination <= 0.5), OR
- (F2) behavioral signals (JWT validation, session state) cannot detect auth drift on real kernel workflows (TP < 0.85), OR
- (F3) structural+behavioral signals are not orthogonal on real kernel workflows (CI upper bound on |r| >= 0.15 at delta=0.15)

MIXED if one signal family works but the other fails or orthogonality is not confirmed.

## Baselines

### B-COLD-ANALYTICAL
Current COLD baseline at 77 tokens/task (analytical prompt-only counting). Carried forward from EXP-PRODUCT-35330741529. COLD success rate unmeasured. Not re-measured in this experiment.

### B-PARAMETERIZED-ANALYTICAL
Current PARAMETERIZED baseline at 18624 tokens (analytical). Carried forward from EXP-PRODUCT-35330741529. Selection savings 112 tokens, completion savings 955 tokens. All estimated, not measured. Not re-measured in this experiment.

### B-FRESHNESS-STRUCTURAL
HTTP fingerprint substrate discrimination on real SPIDER kernel endpoints (jsonplaceholder.typicode.com). Structural signal from EXP-RUNTIME-33902315583 (discrimination 0.833, null FP 0.0%). Expected: full-vector discrimination > 0.5 on auth-state changes.

### B-FRESHNESS-BEHAVIORAL
JWT/session validation behavioral signals on real SPIDER kernel endpoints. Behavioral signal from EXP-GRAPH-35353011131 (TP=1.0, FP=0.0, AUC=1.0 on stochastic mock). Expected: TP >= 0.85 on auth drift detection.

## Controls

### Positive Control
Auth-state change detection on jsonplaceholder.typicode.com using HTTP fingerprint substrate (replicates EXP-RUNTIME-33902315583 positive control). Validated discrimination 0.833 > 0.5. Expected: full-vector discrimination > 0.5 on auth-state changes (valid_token vs no_auth vs expired_token).

### Null Control
Structural noise tolerance: optional field additions, timing jitter, response variation that do NOT represent auth drift. FP rate <= 0.15 on noise-only samples. Expected: FP <= 0.15 on structural noise samples.

## Measurement Validity

1. HTTP fingerprint substrate measurements use the validated FLASK+JWT HS256 localhost pattern from EXP-RUNTIME-33902315583 (discrimination 0.833, null FP 0.0%)
2. Behavioral signals use the validated graded session_status_check pattern from EXP-GRAPH-35353011131 (TP=1.0, FP=0.0, orthogonality confirmed at delta=0.15)
3. Orthogonality tested via TOST equivalence test with delta=0.15 (CI upper bound < 0.15 confirms shared variance < 2.25%)
4. All measurements use deterministic mock server (Flask 3.1.3 + PyJWT 2.13.0 HS256) on localhost, not production APIs
5. N >= 480 paired samples (60 per condition x 8 co-occurring conditions) for orthogonality test
6. This experiment does NOT make real LLM calls — it tests the structural/behavioral signal architecture for freshness detection, not token economics

## Decision Rule

SURVIVES_CURRENT_TEST requires ALL of:
- (C1) HTTP fingerprint discrimination > 0.5 on auth-state changes (positive control)
- (C2) behavioral TP >= 0.85 on auth drift
- (C3) structural+behavioral orthogonality confirmed at delta=0.15 (CI upper bound < 0.15, TOST p_upper < 0.05)
- (C4) FP <= 0.15 on structural noise
- (C5) C-PRODUCT-ECON closure decision documented with rationale

FALSIFIED if any of C1-C4 fail.
MIXED if C1-C2 pass but C3 or C4 fail.

## Product Consequence

### If SURVIVES
C-PRODUCT-ECON is closed (token-based deduplication economics not viable at current scale). Product lane redirects to C-FRESHNESS integration: behavioral+structural parallel-channel architecture justified for production deployment. Freshness guards become the next product gate. C-FRESHNESS advances toward PRODUCT_CORE.

### If FALSIFIED
C-PRODUCT-ECON closure is premature — there may be a path to token economics with real LLM measurement (option A from parent handoff). Product lane must provision LLM API credentials or pivot to alternative mechanisms (C-RESIDUAL-NOVELTY, C-LLM-INHERIT).

## Estimated Cost

Zero new LLM calls. Uses existing HTTP fingerprint substrate code (src/spider/kernel.py) and behavioral signal infrastructure. Flask mock server startup + JWT generation + HTTP requests = ~5 minutes wall clock. No API keys required.

## Expected Information Gain

HIGH: This experiment directly resolves the parent handoff's three-way decision (A/B/C). Either (a) C-PRODUCT-ECON is closed and product lane redirects to C-FRESHNESS (changing product direction), or (b) C-FRESHNESS integration fails and product lane must provision LLM API credentials (changing infrastructure requirements). Either outcome changes a product decision.

## Inherited State Not Modified

- C-PRODUCT-ECON remains HYPOTHESIS until Director verdict
- C-PARAM-INHERIT remains EXPERIMENTAL at committed-code synthetic single-slot ceiling
- C-FRESHNESS remains EXPERIMENTAL with orthogonality confirmed at delta=0.15 under stochastic mock
- No product promotion authorized by this experiment
- No code changes to production without Director approval
