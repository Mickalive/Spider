# EXP-PRODUCT-35538865048 — Preregistration

## Status

DESIGN FROZEN — no outcome data inspected before design completion.

---

## 1. Question

When token_refresh behavioral scores are produced as a continuous severity gradient (not bimodal 0.35/0.65), can a calibrated discriminating threshold be found that achieves TP >= 0.85 AND FP <= 0.10 simultaneously — and does behavioral-structural orthogonality (TOST delta=0.15, n>=480) survive at that calibrated threshold under co-occurring production-like structural noise?

## 2. Motivation

The parent experiment (EXP-PRODUCT-35481773764) passed all 5 frozen conditions on localhost mock but received audit REVISE due to three high-severity findings:

- **V-THRESHOLD-TAUTOLOGY** (high): Detection threshold 0.25 lies below both behavioral modes (0.35 failure, 0.65 success), so TP=1.0 is tautological — any threshold 0.15-0.35 yields identical TP=1.0. The guard's discrimination capacity is untested.
- **V-BIMODAL-DISCRETE** (medium): Behavioral variance is driven solely by Bernoulli mixture of two discrete points, not continuous severity. Limits generalizability to production.
- **V-ERROR-FORMAT-INERT** (high): error_format_variation noise not expressed on wire; effective coverage 3/4 types.

Five independent mock experiments confirm orthogonality at delta=0.15 (r=0.016-0.046, CI upper 0.053-0.135), but all at the tautological threshold. The product lane has exhausted mock-ceiling designs at threshold 0.25.

**This experiment addresses V-THRESHOLD-TAUTOLOGY and V-BIMODAL-DISCRETE simultaneously** by introducing continuous severity variation and calibrating a non-tautological threshold.

## 3. Hypothesis

A continuous severity model mapping token_refresh outcome quality to behavioral_score in [0.2, 0.8] range yields a calibrated threshold in [0.40, 0.60] where:
1. TP >= 0.85 on token_refresh samples
2. FP <= 0.10 on noise-only samples
3. Pearson r(behavioral, structural) CI upper < 0.15 at n=480

## 4. Falsifier

No threshold in [0.20, 0.80] achieves TP >= 0.85 AND FP <= 0.10 on continuous scores, OR orthogonality TOST fails at delta=0.15 at the best-F1 threshold on n=480 co-occurring samples.

## 5. State Representation

### 5.1 Behavioral Signal
- Endpoint: `/api/session/status` (behavioral channel)
- Source: `session_quality` field in JSON response body
- Continuous mapping: token_refresh outcome quality → [0.2, 0.8]
  - Full refresh success (200 + valid new token): 0.70-0.80 (uniform draw)
  - Partial refresh (200 + stale/old token): 0.50-0.69 (uniform draw)
  - Refresh failure (401/expired): 0.20-0.39 (uniform draw)
- Normalization: raw `session_quality` divided by 1.0 = behavioral_score in [0,1]
- Parent discrete model (0.35/0.65) replaced; continuous model is the intervention under test

### 5.2 Structural Signal
- Endpoint: `/api/schema` (structural channel)
- Observable: cardinality (body_key_count + semantic_header_count + status_code)
- Unchanged from parent: X-Request-Id/Date/Server/Content-Length/Connection excluded

### 5.3 Server
- Flask 3.1.3 + SQLite WAL + TTLCache TTL 0.5s + jitter 10-100ms
- JWT: HS256 + RS256 dual-algorithm
- 4 auth states: no_auth, valid_token, expired_token, invalid_token
- Port: 18951 (or next available)
- Threaded=False, sequential client

## 6. Action Representation

Token refresh via `POST /api/auth/refresh` with expired_token. Server draws `p_refresh_success=0.7` from seeded RNG. Continuous behavioral_score assigned per 5.1 mapping.

## 7. Sampling Policy

### Phase A — Threshold Calibration (n=480)
- 240 token_refresh samples (stochastic drift, p_refresh_success=0.7)
- 240 noise-only samples (no drift, 4 noise types x 60)
- All paired: each sample reads behavioral from /api/session/status AND structural from /api/schema
- Threshold sweep: [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80] at 0.05 increments
- Calibrated threshold = argmax F1(T) subject to TP(T) >= 0.85 AND FP(T) <= 0.10

### Phase B — Orthogonality at Calibrated Threshold (n=480)
- 480 paired samples across 4 co-occurring conditions (token_refresh x 4 noise types, 120 each)
- Behavioral and structural signals measured simultaneously
- Pearson r, Fisher-z CI, TOST at delta=0.15

### Phase C — Positive Control (n=40)
- 40 HTTP probes across 4 auth states (10 each)
- Full-vector discrimination > 0.5 required

## 8. Unit of Analysis

Each unit is one paired (behavioral_score, structural_signal) observation from a single HTTP request cycle.

## 9. Holdout

No train/test split. All analysis is on collected data. Threshold calibration and orthogonality are on independent phases (A and B) to prevent overfitting.

## 10. Null Controls

- **NC-NOISE-FP**: Noise-only samples at calibrated threshold. Expected FP <= 0.10.
- **NC-ORTHOGONALITY**: Pearson r ~ 0 at n=480. TOST null: |r| < 0.15.

## 11. Baselines

- **B-TAUT-025**: Threshold 0.25 on bimodal scores (parent). TP=1.0, tautological.
- **B-MODE-MID-050**: Threshold 0.50 on bimodal scores. TP ~0.70.
- **B-PARENT-N480-MOCK**: Parent n=480 result. TP=1.0, TOST PASS.
- **B-5X-ORTHO-MOCK**: Five prior n=480 mock experiments. All TOST PASS.

## 12. Primary Metric

**F1 score at calibrated threshold** on Phase A data, subject to TP >= 0.85 AND FP <= 0.10 constraint.

Secondary metrics:
- TP rate at calibrated threshold (Wilson lower bound)
- FP rate at calibrated threshold
- Orthogonality: Pearson r, Fisher-z 95% CI, TOST at delta=0.15
- Threshold sweep TP/FP/F1 curve across [0.20, 0.80]
- Behavioral variance: std across all samples and per-condition

## 13. Expected Direction

Higher F1 at a non-tautological threshold (>0.35) supports the hypothesis that the behavioral signal can discriminate refresh quality. Orthogonality surviving at the calibrated threshold supports production viability.

## 14. Uncertainty Method

- Wilson score interval for TP/FP rates
- Fisher-z transformation for Pearson r CI
- TOST equivalence test at delta=0.15 for orthogonality

## 15. Adequacy Rule

- n=480 per phase (matching parent) provides >80% power to detect r=0.10 at alpha=0.05 (two-sided)
- 13 threshold candidates at 0.05 increments covers the discriminating range [0.20, 0.80]
- 240 noise-only samples provide adequate FP estimation (SE < 0.02 at FP=0.10)

## 16. Decision Rule

### SURVIVES_CURRENT_TEST requires ALL of:
- **C1**: full-vector discrimination > 0.5 (positive control)
- **C2**: TP >= 0.85 at calibrated threshold (Wilson lower >= 0.80)
- **C3**: behavioral_std > 0.05 on all 4 co-occurring conditions AND Pearson r CI upper < 0.15 at n=480
- **C4**: FP <= 0.10 at calibrated threshold on 240 noise-only samples
- **C5**: TOST equivalence pass at delta=0.15 on n=480 co-occurring samples

### FALSIFIED if:
- No threshold achieves TP >= 0.85 AND FP <= 0.10 (C2 AND C4 jointly fail at all thresholds)
- OR calibrated threshold TOST fails at delta=0.15 (C5 fails)
- OR C1 fails

### MEASUREMENT_INVALID if:
- Continuous score injection fails (behavioral scores remain bimodal, <5 unique values)
- OR error_format_variation remains inert (structural_std equals baseline jitter)
- OR sample count < 480 after exclusions

## 17. Validity Threats

1. **Mock-only ceiling**: All measurements on localhost mock; no inference to production (inherited V-MOCK-ONLY-CEILING)
2. **Continuous score design**: The severity mapping [0.2, 0.8] is hand-designed; production may have different distribution
3. **Error_format_variation fix**: Must be verified as effective (structural_std > baseline) before claiming 4/4 coverage
4. **Threshold selection bias**: Calibrated threshold selected on Phase A data; Phase B uses the same threshold (acceptable since threshold is pre-declared, not data-driven on Phase B)

## 18. Product Consequence

**Positive**: Threshold tautology resolved; calibrated operating point exists; claim ceiling upgraded. C-FRESHNESS moves toward VALIDATED (still bounded to mock).

**Negative**: No calibrated threshold exists or orthogonality breaks. C-FRESHNESS fundamentally limited to tautological detection. Claim ceiling downgraded; production viability questioned.

## 19. Estimated Cost

~780 HTTP request cycles + threshold sweep computation. Runtime ~120s. No LLM cost.
